# -*- coding: utf-8 -*-
import sys
import os
import time

CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append(os.path.join(WORKSPACE_DIRECTORY, 'ui'))
import uuid
from datetime import datetime
from app.train.train_worker import TrainWorker
from app.widgets.message_box import MessageBox
from app.core.log import write_log
from app.core.utils import fmt_duration
from PySide6.QtCore import QTimer, QTime

try:
    from shiboken6 import isValid as _is_valid
except ImportError:
    _is_valid = lambda obj: obj is not None

try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None

try:
    import pynvml
except ImportError:
    pynvml = None


def _series_best(series, key):
    """全空返回 None: 序列尾部常有补齐的 None 占位。"""
    vals = [float(v) for v in (series.get(key) or []) if v is not None]
    return max(vals) if vals else None


def _main_map50(series):
    """优先 ema 列: rf-detr 按 ema 的 mAP@50-95 选 best checkpoint,
    界面数字必须和交付的模型同源, 否则对不上。
    """
    # 按有无 mask 系列判定, 不能按键存在性回退: 旧分割记录没有 mask_ema 列
    is_seg = bool(series.get("mask_mAP@50") or series.get("mask_ema_mAP@50"))
    keys = ("mask_ema_mAP@50", "mask_mAP@50") if is_seg else ("ema_mAP@50",
                                                              "mAP@50")
    for key in keys:
        v = _series_best(series, key)
        if v is not None:
            return v
    return None


class TrainMixin(object):
    _nvml_state = None
    METRICS_SAVE_INTERVAL = 10.0
    _pending_metrics = None
    _metrics_saved_ts = 0.0
    _best_map50 = None
    _progress_tip = ""

    def is_training(self):
        return (self._train_worker is not None
                and self._train_worker.isRunning())

    def start_training(self, config, record_id):
        if self.is_training():
            return False
        self._training_record_id = record_id
        self._train_settled = False
        self._train_stopped = False
        self._train_worker = TrainWorker(config, self)
        self._train_worker.progress.connect(self._on_train_progress)
        self._train_worker.metrics.connect(self._on_train_metrics)
        self._train_worker.finished_ok.connect(self._on_train_done)
        self._train_worker.failed.connect(self._on_train_failed)
        self._train_worker.log.connect(self._on_train_log)
        # 兜底: run() 的三个分支可能全不命中(rc=0 但没抓到 RESULT),
        # 此时没有任何结果信号, 进度条与队列会永远卡住
        self._train_worker.finished.connect(self._on_worker_thread_finished)
        self._show_train_task("{} 训练中 0/{}".format(
            config["project"], config["epochs"]), 0)
        self._train_start_ts = time.time()
        self._eta_total_epochs = int(config.get("epochs", 0))
        self._best_map50 = None
        self._progress_tip = ""
        self._pending_metrics = None
        self._metrics_saved_ts = 0.0   # 0 = 首次指标立即落盘
        self._apply_progress_format()
        if self._eta_total_epochs > 0:
            self._eta_remain = self._eta_total_epochs * 300
            self._show_eta()
        self._train_worker.start()
        return True

    def kill_training_worker(self, timeout_ms=10000):
        """杀掉训练进程树并等它真正退出，返回是否已退出。

        孙进程(dataloader)没退干净就启动下一个任务会直接 OOM，
        所以这里必须等，等不到就返回 False 让调用方放弃推进。
        """
        w = self._train_worker
        if w is None:
            return True
        w.stop()
        w.wait(timeout_ms)
        if w.isRunning():
            return False
        return True

    def _on_worker_thread_finished(self):
        """线程结束但没收到任何结果信号时的兜底收尾。"""
        # 旧 worker 的 finished 可能在新任务启动后才送达(信号排队晚于冷却
        # 定时器), 此时 _training_record_id 已被换掉, 收尾会误杀新任务
        if self.sender() is not self._train_worker:
            return
        if getattr(self, "_train_settled", True):
            return
        rid = self._training_record_id
        self._log("[train] 训练线程已结束但未返回结果，按失败收尾")
        if rid:
            self.on_train_finished(rid, None)

    def stop_training(self, confirm=True):
        """停止训练。队列激活时先问清范围，避免一次误操作停掉整夜的队列。"""
        if not self.is_training():
            self._hide_train_task()
            return
        queued = self.queue_is_running() and self.queue_pending_count() > 0
        if queued:
            choice = MessageBox.choose(
                self, "停止训练", "当前正在跑训练队列，要停止到什么范围？",
                [("仅停止当前", "primary"), ("停止队列", "danger"),
                 ("取消", "normal")])
            if choice is None or choice == "取消":
                return
            if choice == "停止队列":
                self.stop_train_queue()
        else:
            if confirm and not MessageBox.question(
                    self, "停止训练", "确定要停止当前训练吗？"):
                return
        self._train_stopped = True
        exited = self.kill_training_worker()
        self._hide_train_task()
        rid = self._training_record_id
        self._training_record_id = None
        self._train_worker = None
        self._log("手动停止训练: {}".format(rid))
        if not exited:
            self._log("[train] 训练进程 10 秒内未退出，可能有子进程残留占用显存")
            MessageBox.warning(
                self, "停止训练",
                "训练进程未能完全退出，可能仍有子进程占用显存。\n"
                "建议稍等片刻再启动下一个任务。")
        if rid:
            self.on_train_finished(rid, None)

    def _on_train_progress(self, epoch, total):
        if self._train_worker is None or self._training_record_id is None:
            return
        project = self._train_worker._config.get("project", "") if self._train_worker else ""
        self._show_train_task("{} 训练中 {}/{}".format(project, epoch, total),
                              epoch * 100.0 / total if total else 0)
        self._update_eta(epoch, total)

    def _on_train_metrics(self, metrics):
        # 分类看准确率, 检测/分割看 mAP@50
        s = metrics.get("series", {})
        acc = _series_best(s, "accuracy")
        m = _main_map50(s)
        if acc is not None:
            self._best_map50 = acc
            self._progress_tip = "进度 | 当前最好准确率"
        elif m is not None:
            self._best_map50 = m
            self._progress_tip = "进度 | 当前最好 mAP@50"
        if acc is not None or m is not None:
            self._apply_progress_format()
        self._pending_metrics = metrics
        if self._training_record_id:
            self.update_train_metrics(self._training_record_id, metrics)

    def _on_train_done(self, result):
        # 防旧 worker 的迟到信号把新任务收掉(与 _on_worker_thread_finished 同因)
        if self.sender() is not self._train_worker:
            return
        rid = self._training_record_id
        self._hide_train_task()
        self._train_worker = None
        if rid:
            self.on_train_finished(rid, result)

            def _clear():
                if self._training_record_id == rid:
                    self._training_record_id = None

            QTimer.singleShot(0, _clear)
        else:
            self._training_record_id = None

    def _on_train_failed(self, detail):
        if self.sender() is not self._train_worker:
            return
        rid = self._training_record_id
        self._hide_train_task()
        self._training_record_id = None
        self._train_worker = None
        if rid:
            self.on_train_finished(rid, None)
        for line in detail.splitlines():
            self._log("[train] " + line)
        # 队列运行时不弹模态框：无人值守时会一直等点击，整个队列停摆
        if self.queue_is_running():
            write_log("训练失败(队列模式，已跳过弹窗): {}".format(detail[:2000]))
            return
        MessageBox.critical(self, "训练失败", "训练过程中发生错误，Err：\n\n{}".format(detail))

    def _on_train_log(self, line):
        self._log("[train] " + line)

    def on_train_progress(self, project, datasets, epoch, total):
        self._show_train_task("{} / {} 训练中 {}/{}".format(
            project, datasets, epoch, total),
            epoch * 100.0 / total if total else 0)

    def update_train_metrics(self, record_id, metrics, force=False):
        """指标写入 metrics/<id>.json, 记录里只留文件名 + 摘要, 不存全量曲线。"""
        if not force and time.time() - self._metrics_saved_ts < self.METRICS_SAVE_INTERVAL:
            return
        self._metrics_saved_ts = time.time()
        for r in self.db.get_train_records():
            if r.get("id") == record_id:
                r.pop("metrics", None)
                r["metrics_file"] = self.db.save_train_metrics(record_id, metrics)
                s = metrics.get("series", {})
                m = _main_map50(s)
                if m is not None:
                    r["map50"] = "{:.3f}".format(m)
                acc = _series_best(s, "accuracy")
                if acc is not None:
                    r["accuracy"] = "{:.4f}".format(acc)
                r["metrics_epochs"] = len(metrics.get("epochs") or [])
                self.db.update_train_record(r)
                write_log("更新训练指标: record={} 已完成epoch={} map50={} acc={} 类别数={}".format(
                    record_id[:8], r.get("metrics_epochs"),
                    r.get("map50"), r.get("accuracy"),
                    len(metrics.get("per_class", {}))))
                return

    def _flush_train_metrics(self, record_id):
        """训练结束/失败时补写最后一次指标(节流可能吞掉它)。"""
        if self._pending_metrics is None:
            return
        metrics = self._pending_metrics
        self._pending_metrics = None
        self.update_train_metrics(record_id, metrics, force=True)

    def on_train_finished(self, record_id, result):
        self._train_settled = True
        self._hide_train_task()
        if record_id:
            self._flush_train_metrics(record_id)
        recs = self.db.get_train_records()
        for r in recs:
            if r.get("id") == record_id:
                r["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    t0 = datetime.strptime(r.get("start_time", ""), "%Y-%m-%d %H:%M:%S")
                    t1 = datetime.strptime(r["end_time"], "%Y-%m-%d %H:%M:%S")
                    secs = int((t1 - t0).total_seconds())
                    r["duration"] = fmt_duration(int((t1 - t0).total_seconds()))
                except Exception:
                    pass
                if result:
                    if result.get("map50"):
                        r["map50"] = "{:.3f}".format(float(result["map50"]))
                    if result.get("accuracy"):
                        r["accuracy"] = "{:.4f}".format(float(result["accuracy"]))
                    if result.get("model_path"):
                        r["model_path"] = result["model_path"]
                else:
                    r["status"] = "失败/已停止"
                self.db.update_train_record(r)
                if result and result.get("model_path"):
                    self._save_model_record(r)
                break
        stopped = bool(getattr(self, "_train_stopped", False))
        self._train_stopped = False
        if hasattr(self, "on_queue_train_finished"):
            self.on_queue_train_finished(record_id, result, stopped=stopped)

    def _save_model_record(self, train_record):
        """把训练记录副本写入 model_history(独立 id,幂等,删除不影响训练参数)。"""
        rid = train_record.get("id")
        for m in self.db.get_model_records():
            if m.get("train_id") == rid:
                return
        rec = dict(train_record)
        rec["id"] = str(uuid.uuid4())
        rec["train_id"] = rid
        self.db.add_model_record(rec)
        write_log("已保存模型记录: {} | {}".format(
            rec.get("model_path", ""), rec.get("dataset_info", "")))

    def _show_train_task(self, task_name, value=0):
        """训练开始时显示: 任务名 + 进度条 + 剩余时间 + 显存"""
        self.task_name_label.setText(task_name)
        self.train_progress.setValue(max(0, min(100, int(value))))
        self.task_name_label.show()
        self.train_progress.show()
        # 停止按钮的 show/hide 必须与 _hide_train_task 对称且都在这一处:
        # 每个 epoch 的进度回调都会走到这里, 任何一次误 hide 都能自愈
        self.stop_train_btn.show()
        self.time_count_label.show()
        self.time_count_edit.show()
        self.gpu_memory_label.show()
        self.gpu_memory_use_btn.show()
        if not self._gpu_timer.isActive():
            self._refresh_gpu_memory()
            self._gpu_timer.start()
        if not self._eta_timer.isActive():
            self._eta_timer.start()

    def _set_train_progress(self, value):
        """更新训练进度(0-100)。"""
        self.train_progress.setValue(max(0, min(100, int(value))))

    def _apply_progress_format(self):
        """进度条文本:`30% | 0.556` 进度 | 当前最好精度 """
        m = self._best_map50
        tail = "{:.3f}".format(m) if m is not None else "--"
        self.train_progress.setFormat("%p% | " + tail)
        self.train_progress.setToolTip(self._progress_tip)

    def _hide_train_task(self):
        """训练结束/无训练任务时隐藏。"""
        self.task_name_label.hide()
        self.train_progress.hide()
        self.stop_train_btn.hide()
        self.time_count_label.hide()
        self.time_count_edit.hide()
        self._eta_timer.stop()
        self._eta_remain = 0
        self._eta_total_epochs = 0

    def _update_eta(self, epoch, total):
        """progress到达时按已用时长外推剩余秒数(epoch 从 1 起,首 epoch 内无数据跳过)。"""
        if not total or epoch <= 0 or not self._train_start_ts:
            return
        elapsed = time.time() - self._train_start_ts
        if elapsed <= 0:
            return
        avg = elapsed / epoch  # 每 epoch 平均耗时
        self._eta_remain = max(0, int(avg * (total - epoch)))
        self._show_eta()

    def _update_test_eta(self, done, total):
        """测试进度推进时按已用时长外推剩余秒数（首次调用记录开始时间）。"""
        if not total:
            return
        if not self._test_start_ts:
            self._test_start_ts = time.time()
        if done <= 0:
            return
        elapsed = time.time() - self._test_start_ts
        if elapsed <= 0:
            return
        avg = elapsed / done  # 每张图平均耗时
        self._eta_remain = max(0, int(avg * (total - done)))
        self._show_eta()

    def _eta_tick(self):
        """每秒递减剩余秒数,实现持续倒计时(训练推进时由 _update_eta 重估校准)。"""
        if self._eta_remain > 0:
            self._eta_remain -= 1
        self._show_eta()

    def _show_eta(self):
        h, remain = divmod(self._eta_remain, 3600)
        m, s = divmod(remain, 60)
        self.time_count_edit.setTime(QTime(h, m, s))

    def _refresh_gpu_memory(self):
        """2s定时:查询显存使用率,>55% 显示红色。用 pynvml 避免每 2s 拉起子进程。"""
        usage = None
        if pynvml is not None:
            if TrainMixin._nvml_state is None:
                try:
                    pynvml.nvmlInit()
                    TrainMixin._nvml_state = True
                except Exception:
                    TrainMixin._nvml_state = False
            if TrainMixin._nvml_state:
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    if mem.total > 0:
                        usage = mem.used * 100.0 / mem.total
                except Exception:
                    pass
        self.gpu_memory_use_btn.setText(
            "N/A" if usage is None else "{:.0f}%".format(usage))
        high = usage is not None and usage > 55
        if high != getattr(self, "_gpu_high", None):
            self._gpu_high = high
            self.gpu_memory_use_btn.setStyleSheet(self._gpu_btn_style(high))

    @staticmethod
    def _gpu_btn_style(high):
        """显存 chip 配色:超 55% 深红发黑,否则深绿(胶囊形)。"""
        color = "#8a2424" if high else "#1f6b45"
        hover = "#a03131" if high else "#278a5a"
        return (
            "QPushButton {{ background-color: {}; color: white;"
            " border: none; border-radius: 12px; padding: 4px 14px;"
            " font-size: 12px; font-weight: 500; }}"
            "QPushButton:hover {{ background-color: {}; }}").format(color, hover)
