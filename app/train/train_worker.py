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

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
TRAIN_RUNNER = os.path.join(WORKSPACE, "app", "train", "train_runner.py")
CLASSIFY_TRAIN_RUNNER = os.path.join(WORKSPACE, "app", "train",
                                     "classify_train_runner.py")

CSV_POLL_INTERVAL = 5   # 定时检查 metrics.csv 修改时间的间隔(秒)
LOG_FLUSH_SECS = 0.1


def _is_float(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


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
        """请求停止：终止子进程。"""
        self._stop_flag = True
        if self._proc is not None and self._proc.poll() is None:
            try:
                self._proc.terminate()
            except Exception:
                pass
            try:
                self._proc.kill()
            except Exception:
                pass

    def _accumulate(self, epochs, series, per_class, row):
        """把 CSV 一行的 val 指标累积进 GUI 需要的 series 结构（row 为 csv.DictReader 行）。"""
        ep = int(row.get("epoch", 0)) + 1   # CSV epoch 从 0 计，GUI 从 1 计
        epochs.append(ep)
        series.setdefault("epochs", []).append(ep)

        def _f(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        n_ep = len(series["epochs"])

        def _align(seq):
            """
            把序列补齐到上一轮长度
            """
            if len(seq) < n_ep - 1:
                seq.extend([None] * (n_ep - 1 - len(seq)))

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
            seq = series.setdefault(key, [])
            _align(seq)
            seq.append(_f(row.get(csv_key)))

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
                seq = pc[field]
                _align(seq)
                seq.append(present.get((label, field)))

        for seq in series.values():
            if len(seq) < n_ep:
                seq.append(None)
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
                if ep_gui in (series.get("epochs") or []):
                    pending["phase"] = None
                    return
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
                pc_row = per_class.setdefault(
                    label, {"AP50-95": [], "AR": [], "F1": [],
                            "Precision": [], "Recall": []})
                n = len(series.get("epochs", []))
                if len(pc_row["AP50-95"]) >= n:
                    pending["phase"] = None
                    return
                pc_row["AP50-95"].append(float(toks[1]))
                pc_row["AR"].append(float(toks[2]))
                pc_row["F1"].append(float(toks[3]))
                pc_row["Precision"].append(float(toks[4]))
                pc_row["Recall"].append(float(toks[5]))
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
        csv_rows_read = 0        # 已消费的 CSV 行数, 供增量读跳过

        def _read_new_epochs():
            """
            读 CSV 中新增的含 val 指标行(按 epoch 去重)。只解析上次之后新增的行
            """
            nonlocal last_mtime, csv_rows_read
            if not os.path.exists(csv_path):
                return []
            mtime = os.path.getmtime(csv_path)
            if mtime <= last_mtime and csv_rows_read:
                return []
            try:
                with open(csv_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception:
                return []
            if text and not text.endswith("\n"):
                return []
            last_mtime = mtime
            try:
                rows = list(csv.DictReader(io.StringIO(text)))
            except Exception:
                return []
            if len(rows) <= csv_rows_read:
                return []
            new_rows = rows[csv_rows_read:]
            csv_rows_read = len(rows)
            by_epoch = {}
            for r in new_rows:
                has_box = r.get("val/mAP_50", "") not in (None, "")
                has_mask = r.get("val/segm_mAP_50", "") not in (None, "")
                if not (has_box or has_mask):
                    continue
                ep = int(r.get("epoch", 0))
                by_epoch[ep] = r
            return [by_epoch[ep] for ep in sorted(by_epoch)
                    if (ep + 1) not in (series.get("epochs") or [])]

        def _poll_csv():
            """每 CSV_POLL_INTERVAL 秒检查一次 metrics.csv，变了就累积新 epoch 并 emit。"""
            nonlocal last_poll
            now = time.time()
            if now - last_poll < CSV_POLL_INTERVAL:
                return
            last_poll = now
            rows = _read_new_epochs()
            if not rows:
                return
            for r in rows:
                self._accumulate(epochs, series, per_class, r)
                self.progress.emit(int(r.get("epoch", 0)) + 1,
                                   self._config["epochs"])
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
