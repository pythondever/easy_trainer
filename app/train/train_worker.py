# -*- coding: utf-8 -*-
"""训练工作线程：以子进程方式运行 RF-DETR 训练，定时轮询指标并转发信号。"""

import collections
import csv
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time

from PySide6.QtCore import QThread, Signal

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
TRAIN_RUNNER = os.path.join(WORKSPACE, "app", "train", "train_runner.py")
CLASSIFY_TRAIN_RUNNER = os.path.join(WORKSPACE, "app", "train",
                                     "classify_train_runner.py")

CSV_POLL_INTERVAL = 5   # 定时检查 metrics.csv 修改时间的间隔(秒)


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
            v = _f(row.get(csv_key))
            if v is not None:
                series.setdefault(key, []).append(v)
        for k, v in row.items():
            # CSV 每类 5 列：val/{AP,AR,F1,Precision,Recall}/<类>
            for prefix, field in (("val/AP/", "AP50-95"), ("val/AR/", "AR"),
                                  ("val/F1/", "F1"),
                                  ("val/Precision/", "Precision"),
                                  ("val/Recall/", "Recall")):
                if k.startswith(prefix) and v not in (None, ""):
                    label = k[len(prefix):]
                    pc = per_class.setdefault(
                        label, {"AP50-95": [], "AR": [], "F1": [],
                                "Precision": [], "Recall": []})
                    if len(pc[field]) < len(series.get("epochs", [])):
                        pc[field].append(_f(v))
        return (epochs, series, per_class)

    @staticmethod
    def _build_payload(s, pc):
        """构造 metrics payload（series + 可选 per_class）。"""
        p = {"epochs": s.get("epochs", []),
             "series": {k: v for k, v in s.items() if k != "epochs"}}
        if pc:
            p["per_class"] = pc
        return p

    def _consume_stdout_line(self, line, pending, epochs, series, per_class):
        """
        从 rf-detr stdout 的 Val 表格兜底取指标（metrics.csv 不落盘时的保险）。
        pending 状态机：Val (Epoch N/M) 标题行定 phase，随后 │ 分隔的数据行按列数
        区分 overall（检测 7 列/分割 9 列，末尾 2 列为 segm mAP）与 per-class（6 列）；
        与 CSV 通道共用 series/per_class 并按 epoch 去重，防双通道双写。
        """
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

        def _read_new_epochs():
            """读 CSV 中含 val 指标的新行(按 epoch 去重)。"""
            nonlocal last_mtime
            if not os.path.exists(csv_path):
                return []
            mtime = os.path.getmtime(csv_path)
            if mtime <= last_mtime:
                return []
            last_mtime = mtime
            try:
                with open(csv_path, "r", encoding="utf-8") as f:
                    rows = list(csv.DictReader(f))
            except Exception:
                return []
            by_epoch = {}
            for r in rows:
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

        while not self._stop_flag:
            try:
                line = out_q.get(timeout=0.5)
            except queue.Empty:
                line = None
            if line:
                line = _ansi_re.sub("", line)
                last_lines.append(line.rstrip())
                self.log.emit(line.rstrip())
                if "[train] EPOCH " in line:
                    m = re.search(r"EPOCH (\d+)/(\d+)", line)
                    if m:
                        self.progress.emit(int(m.group(1)), int(m.group(2)))
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
                        res = {}
                    self.finished_ok.emit(res)
                    result_emitted = True
            _poll_csv()
            _poll_cls()
            if self._proc.poll() is not None and out_q.empty():
                break
        last_poll = 0.0
        _poll_csv()
        rc = self._proc.poll()
        result_path = os.path.join(self._config["timestamp_dir"], "result.json")
        if rc == 0 and os.path.exists(result_path) and not result_emitted:
            try:
                with open(result_path, "r", encoding="utf-8") as f:
                    res = json.load(f)
                self.finished_ok.emit(res)
            except Exception:
                pass
        elif not self._stop_flag and rc != 0:
            detail = "训练进程异常退出 (code={})\n\n--- 子进程输出(尾部) ---\n{}".format(
                rc, "\n".join(last_lines))
            self.failed.emit(detail)
