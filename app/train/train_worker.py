# -*- coding: utf-8 -*-
"""训练工作线程：以子进程方式运行 RF-DETR 训练，定时轮询指标并转发信号。"""

import collections
import copy
import csv
import io
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import traceback

from PySide6.QtCore import QThread, Signal

from app.core.utils import read_text_any

try:
    import psutil
except ImportError:
    psutil = None

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
TRAIN_RUNNER = os.path.join(WORKSPACE, "app", "train", "train_runner.py")
CLASSIFY_TRAIN_RUNNER = os.path.join(WORKSPACE, "app", "train",
                                     "classify_train_runner.py")
# 判定一个 epoch 是否已产出指标(val 有了、或 train 行到了)的列
_EPOCH_KEYS = ("val/mAP_50", "val/segm_mAP_50", "val/loss", "train/loss")

CSV_POLL_INTERVAL = 5   # 定时检查 metrics.csv 修改时间的间隔(秒)
LOG_FLUSH_SECS = 0.1

_PC_FIELDS = ("AP50-95", "AR", "F1", "Precision", "Recall")


def _is_float(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


_PC_TABLE_END = re.compile(r"^\s*[\u2514\u2517\u255A\u2570][\s\u2500-\u257F]*$")


class TrainWorker(QThread):
    """运行一次训练(子进程),通过信号上报进度/指标/完成/错误。"""

    progress = Signal(int, int)          # epoch, total_epochs
    metrics = Signal(dict)                      # {"epochs": [...], "series": {...}}
    finished_ok = Signal(dict)                  # result.json 内容
    failed = Signal(str)                        # traceback
    log = Signal(str)                           # 子进程 stdout 行

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self._config = config
        self._proc = None
        self._stop_flag = False

    def stop(self):
        """请求停止：终止子进程及其孙进程。

        只 kill 直接子进程不够：rf-detr 的 dataloader(num_workers>0) 会 fork
        孙进程，主进程被杀后它们变孤儿继续占显存，下一个训练会直接 OOM。
        """
        self._stop_flag = True
        proc = self._proc
        if proc is None or proc.poll() is not None:
            return
        if psutil is not None:
            try:
                parent = psutil.Process(proc.pid)
                children = parent.children(recursive=True)
                for child in children:
                    try:
                        child.kill()
                    except Exception:
                        pass
                try:
                    parent.kill()
                except Exception:
                    pass
                gone, _alive = psutil.wait_procs(children + [parent], timeout=5)
                return
            except Exception:
                pass
        try:
            proc.terminate()
        except Exception:
            pass
        try:
            proc.kill()
        except Exception:
            pass

    def proc_exited(self):
        """子进程是否已退出（队列据此判断显存是否可回收）。"""
        proc = self._proc
        if proc is None:
            return True
        if proc.poll() is not None:
            return True
        if psutil is not None:
            try:
                return not psutil.pid_exists(proc.pid)
            except Exception:
                return True
        return False

    @staticmethod
    def _row_map(row):
        """该行的主指标值(mAP@50, 分割任务无 box 时回退 segm); 无法解析记 0。"""
        for key in ("val/mAP_50", "val/segm_mAP_50"):
            try:
                v = float(row.get(key))
            except (TypeError, ValueError):
                continue
            if v > 0:
                return v
        return 0.0

    def _write_row(self, series, per_class, idx, row):
        """把一行的 val 指标写到各序列的 idx 位置(不足则补 None, 已存在则覆盖)。"""

        def _f(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        def _put(seq, value):
            while len(seq) < idx:
                seq.append(None)
            if len(seq) == idx:
                seq.append(value)
            else:
                seq[idx] = value

        for key, csv_key in (("mAP@50-95", "val/mAP_50_95"),
                             ("mAP@50", "val/mAP_50"),
                             ("precision", "val/precision"),
                             ("recall", "val/recall"),
                             ("F1", "val/F1"),
                             ("mAR", "val/mAR"),
                             ("ema_mAP@50", "val/ema_mAP_50"),
                             ("ema_mAP@50-95", "val/ema_mAP_50_95"),
                             ("mask_mAP@50", "val/segm_mAP_50"),
                             ("mask_mAP@50-95", "val/segm_mAP_50_95"),
                             ("train_loss", "train/loss"),
                             ("val_loss", "val/loss")):
            if csv_key not in row:
                continue
            _put(series.setdefault(key, []), _f(row.get(csv_key)))

        present = {}
        for k, v in row.items():
            # CSV 每类 5 列：val/{AP,AR,F1,Precision,Recall}/<类>
            for prefix, field in (("val/AP/", "AP50-95"), ("val/AR/", "AR"),
                                  ("val/F1/", "F1"),
                                  ("val/Precision/", "Precision"),
                                  ("val/Recall/", "Recall")):
                if k.startswith(prefix) and v not in (None, ""):
                    present[(k[len(prefix):], field)] = _f(v)
        for label in set(per_class) | {lb for lb, _ in present}:
            pc = per_class.setdefault(
                label, {"AP50-95": [], "AR": [], "F1": [],
                        "Precision": [], "Recall": []})
            for field in pc:
                _put(pc[field], present.get((label, field)))

        n_ep = len(series["epochs"])
        for seq in series.values():
            while len(seq) < n_ep:
                seq.append(None)

    def _should_apply(self, series, ep, row):
        """
        该 epoch 是否需要写入: 尚未记录, 或已记录但值无效且本行有效。

        stdout 通道会先收到训练前的预热表(全 0), 之后才是真实值(CSV 通道同样
        会补到)。若一律"先到为准", 全 0 的预热表会永久占位, mAP 永远显示 0。
        """
        eps = series.get("epochs") or []
        if ep not in eps:
            return True
        idx = eps.index(ep)
        prev = series.get("mAP@50") or series.get("mask_mAP@50") or []
        prev_v = prev[idx] if idx < len(prev) else None
        return (prev_v or 0) <= 0 and self._row_map(row) > 0

    def _accumulate(self, epochs, series, per_class, row):
        """把一行的 val 指标累积进 GUI 需要的 series 结构。"""
        ep = int(row.get("epoch", 0)) + 1   # CSV epoch 从 0 计，GUI 从 1 计
        eps = series.setdefault("epochs", [])
        if not self._should_apply(series, ep, row):
            return (epochs, series, per_class)
        if ep in eps:
            idx = eps.index(ep)          # 覆盖无效的历史值
        else:
            epochs.append(ep)
            eps.append(ep)
            idx = len(eps) - 1
        self._write_row(series, per_class, idx, row)
        return (epochs, series, per_class)

    @staticmethod
    def _build_payload(s, pc):
        """
        构造 metrics payload
        """
        p = {"epochs": copy.deepcopy(s.get("epochs", [])),
             "series": {k: copy.deepcopy(v)
                        for k, v in s.items() if k != "epochs"}}
        if pc:
            p["per_class"] = copy.deepcopy(pc)
        return p

    def _consume_stdout_line(self, line, pending, epochs, series, per_class):
        """
        从 rf-detr stdout 的 Val 表格兜底取指标（metrics.csv 不落盘时的保险）。
        """
        line = line.rstrip("\r\n")
        if pending.get("phase") == "perclass" and _PC_TABLE_END.match(line):
            self.metrics.emit(self._build_payload(series, per_class))
            pending["phase"] = None
            return
        if ("Val (Epoch " not in line
                and not any(s in line for s in ("│", "┃", "┆", "|"))):
            return
        m = re.search(r"Val \(Epoch (\d+)/", line)
        if m:
            pending["epoch"] = int(m.group(1))
            if "Per-class" in line:
                pending["phase"] = "perclass"
            elif "Overall" in line:
                pending["phase"] = "overall"
            return
        if pending.get("epoch") is None or not pending.get("phase"):
            return
        toks = re.findall(r"[│┃┆|]\s*([^│┃┆|]+?)\s*(?=[│┃┆|]|$)", line)
        if len(toks) < 6:
            return
        ep_gui = int(pending["epoch"])
        try:
            if pending["phase"] == "overall":
                if len(toks) not in (7, 9) or not all(_is_float(t)
                                                      for t in toks):
                    return
                row = {"epoch": ep_gui - 1,
                       "val/mAP_50_95": toks[0], "val/mAP_50": toks[1],
                       "val/mAR": toks[3], "val/F1": toks[4],
                       "val/precision": toks[5], "val/recall": toks[6]}
                if len(toks) == 9:
                    row["val/segm_mAP_50_95"] = toks[7]
                    row["val/segm_mAP_50"] = toks[8]
                self._accumulate(epochs, series, per_class, row)
                self.progress.emit(ep_gui, self._config["epochs"])
                self.metrics.emit(self._build_payload(series, per_class))
                pending["phase"] = None
            elif pending["phase"] == "perclass":
                if len(toks) != 6 or not all(_is_float(t) for t in toks[1:]):
                    return
                label = toks[0]
                n = len(series.get("epochs", []))
                if not n:
                    return
                idx = n - 1
                vals = [float(t) for t in toks[1:]]
                pc_row = per_class.setdefault(
                    label, {f: [] for f in _PC_FIELDS})
                stored = sum(pc_row[f][idx] or 0 for f in _PC_FIELDS
                             if idx < len(pc_row[f]))
                if stored > 0:
                    return
                for field, v in zip(_PC_FIELDS, vals):
                    seq = pc_row[field]
                    while len(seq) < idx:
                        seq.append(None)
                    if len(seq) == idx:
                        seq.append(v)
                    else:
                        seq[idx] = v
        except (ValueError, TypeError):
            pass

    def run(self):
        cfg_path = self._config["_cfg_path"]
        python = sys.executable
        runner = (CLASSIFY_TRAIN_RUNNER
                  if self._config.get("task") == "classify" else TRAIN_RUNNER)
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        env["PYTHONUNBUFFERED"] = "1"
        self._proc = subprocess.Popen(
            [python, runner, cfg_path],
            cwd=WORKSPACE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", env=env)
        out_q = queue.Queue()
        last_lines = collections.deque(maxlen=200)
        _ansi_re = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")

        def _reader():
            try:
                for line in self._proc.stdout:
                    out_q.put(line)
            except Exception:
                pass
        threading.Thread(target=_reader, daemon=True).start()

        result_emitted = False
        epochs, series, per_class = [], {}, {}
        pending = {"epoch": None, "phase": None}
        csv_path = os.path.join(self._config["timestamp_dir"], "metrics.csv")
        last_mtime = 0.0
        last_poll = 0.0
        csv_seen = set()         # 已由 CSV 写入过的 epoch(区分 stdout 预热表占的位)

        def _sync_csv():
            """
            把 CSV 全量重解析并幂等写进 series, 返回是否有变化。

            rf-detr 每个 epoch 会写多行(中间步的 lr 行、val 行、train 行), 且
            写入时间分散。若只解析"上次之后的新增行", 同一 epoch 的行一旦跨了
            轮询批次, 迟到的 train/loss 就再也补不进去(train_loss 隔帧为 None)。
            全量重解析让每轮的合并结果只取决于 CSV 内容, 与批次边界无关。
            """
            nonlocal last_mtime
            if not os.path.exists(csv_path):
                return False
            mtime = os.path.getmtime(csv_path)
            if mtime <= last_mtime and series.get("epochs"):
                return False
            try:
                text = read_text_any(csv_path)
            except OSError:
                return False
            # 文件正被写入(末行不完整)时跳过, 下次轮询再解析
            if text and not text.endswith("\n"):
                return False
            last_mtime = mtime
            try:
                rows = list(csv.DictReader(io.StringIO(text)))
            except Exception:
                return False
            by_epoch = {}
            for r in rows:
                try:
                    ep = int(r.get("epoch", 0))
                except (TypeError, ValueError):
                    continue
                merged = by_epoch.setdefault(ep, {})
                for k, v in r.items():
                    if v not in (None, ""):
                        merged[k] = v
            changed = False
            max_ep = 0
            eps = series.setdefault("epochs", [])
            for ep in sorted(by_epoch):
                row = by_epoch[ep]
                gui_ep = ep + 1
                if gui_ep in csv_seen:
                    # 本 epoch 已由 CSV 写入过: 只补行内新出现的键(如迟到的
                    # train/loss)。_write_row 只写 row 里存在的键。
                    idx = eps.index(gui_ep)
                    prev = series.get("train_loss") or []
                    if (row.get("train/loss") not in (None, "")
                            and (idx >= len(prev) or prev[idx] is None)):
                        self._write_row(series, per_class, idx, row)
                        changed = True
                elif not any(row.get(k) not in (None, "") for k in _EPOCH_KEYS):
                    # 只有 lr 的步进行: 该 epoch 还没跑完, 不建条目(否则曲线尾部
                    # 会多一个全空点)
                    continue
                else:
                    # 新 epoch, 或该位置的值来自 stdout 的预热表: CSV 才是真值,
                    # 直接覆盖(stdout 预热表的 mAP 非 0 时会挡住真实 val 值)。
                    if gui_ep in eps:
                        idx = eps.index(gui_ep)
                    else:
                        epochs.append(gui_ep)
                        eps.append(gui_ep)
                        idx = len(eps) - 1
                    self._write_row(series, per_class, idx, row)
                    csv_seen.add(gui_ep)
                    changed = True
                max_ep = max(max_ep, gui_ep)
            if changed and max_ep:
                self.progress.emit(max_ep, self._config["epochs"])
            return changed

        def _poll_csv():
            """每 CSV_POLL_INTERVAL 秒检查一次 metrics.csv，变了就累积新 epoch 并 emit。"""
            nonlocal last_poll
            now = time.time()
            if now - last_poll < CSV_POLL_INTERVAL:
                return
            last_poll = now
            if not _sync_csv():
                return
            self.metrics.emit(self._build_payload(series, per_class))

        cls_mode = self._config.get("task") == "classify"
        cls_json = (os.path.join(self._config.get("timestamp_dir", ""),
                                 "metrics.json") if cls_mode else "")
        cls_mtime = 0.0
        cls_last_poll = 0.0

        def _poll_cls():
            nonlocal cls_mtime, cls_last_poll
            if not cls_json:
                return
            now = time.time()
            if now - cls_last_poll < 2.0:
                return
            cls_last_poll = now
            if not os.path.exists(cls_json):
                return
            mt = os.path.getmtime(cls_json)
            if mt <= cls_mtime:
                return
            cls_mtime = mt
            try:
                with open(cls_json, "r", encoding="utf-8") as f:
                    m = json.load(f)
            except Exception:
                return
            ep_list = m.get("epochs") or []
            if ep_list:
                self.progress.emit(ep_list[-1], self._config.get("epochs", 0))
            self.metrics.emit(m)

        log_buf = []
        log_last_flush = 0.0

        def _flush_log(force=False):
            """把攒下的日志行合并成一条发出(force=True 时立即冲刷)。"""
            nonlocal log_buf, log_last_flush
            if not log_buf:
                return
            if not force and (time.time() - log_last_flush) < LOG_FLUSH_SECS:
                return
            self.log.emit("\n".join(log_buf))
            log_buf = []
            log_last_flush = time.time()

        poll_error = None
        while not self._stop_flag:
            try:
                try:
                    line = out_q.get(timeout=0.5)
                except queue.Empty:
                    line = None
                if line:
                    line = _ansi_re.sub("", line)
                    last_lines.append(line.rstrip())
                    log_buf.append(line.rstrip())
                    if "[train] EPOCH " in line:
                        m = re.search(r"EPOCH (\d+)/(\d+)", line)
                        if m:
                            self.progress.emit(int(m.group(1)),
                                               int(m.group(2)))
                    if "[train] METRICS " in line:
                        try:
                            m = json.loads(line.split("METRICS ", 1)[1])
                            self.metrics.emit(m)
                        except Exception:
                            pass
                    self._consume_stdout_line(line, pending, epochs, series,
                                              per_class)
                    if "[train] RESULT" in line:
                        try:
                            res = json.loads(line.split("RESULT ", 1)[1])
                        except Exception:
                            res = None
                        if isinstance(res, dict):
                            self.finished_ok.emit(res)
                            result_emitted = True
                _flush_log()
                _poll_csv()
                _poll_cls()
                if self._proc.poll() is not None and out_q.empty():
                    break
            except Exception:
                poll_error = traceback.format_exc()
                break
        _flush_log(force=True)
        last_poll = 0.0
        _poll_csv()
        rc = self._proc.poll()
        result_path = os.path.join(self._config["timestamp_dir"], "result.json")
        if poll_error:
            self.failed.emit("训练监控异常，已终止。\n\n{}".format(poll_error))
        elif rc == 0 and os.path.exists(result_path) and not result_emitted:
            try:
                with open(result_path, "r", encoding="utf-8") as f:
                    res = json.load(f)
                self.finished_ok.emit(res)
                result_emitted = True
            except Exception as e:
                self.failed.emit(
                    "训练结果文件读取失败: {}\n\n{}".format(result_path, e))
                result_emitted = True
        elif not self._stop_flag and rc != 0:
            detail = "训练进程异常退出 (code={})\n\n--- 子进程输出(尾部) ---\n{}".format(
                rc, "\n".join(last_lines))
            self.failed.emit(detail)
