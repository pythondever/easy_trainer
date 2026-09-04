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


class TrainMixin(object):
    _nvml_state = None
    METRICS_SAVE_INTERVAL = 10.0
    _pending_metrics = None
    _metrics_saved_ts = 0.0

    def is_training(self):
        return (self._train_worker is not None
                and self._train_worker.isRunning())

    def start_training(self, config, record_id):
        if self.is_training():
            return False
        self._training_record_id = record_id
        self._train_worker = TrainWorker(config, self)
        self._train_worker.progress.connect(self._on_train_progress)
        self._train_worker.metrics.connect(self._on_train_metrics)
        self._train_worker.finished_ok.connect(self._on_train_done)
        self._train_worker.failed.connect(self._on_train_failed)
        self._train_worker.log.connect(self._on_train_log)
        self._show_train_task("{} 训练中 0/{}".format(
            config["project"], config["epochs"]), 0)
        self._train_start_ts = time.time()
        self._eta_total_epochs = int(config.get("epochs", 0))
        self._latest_map50 = None
        self._pending_metrics = None
        self._metrics_saved_ts = 0.0   # 0 = 首次指标立即落盘
        self._apply_progress_format()
        if self._eta_total_epochs > 0:
            self._eta_remain = self._eta_total_epochs * 300
            self._show_eta()
        self.stop_train_btn.show()
        self._train_worker.start()
        return True

    def stop_training(self, confirm=True):
        if confirm and not MessageBox.question(self, "停止训练", "确定要停止当前训练吗？"):
            return
        w = self._train_worker
        if w is not None:
            w.stop()
            w.wait(3000)
            self._train_worker = None
            self._log("手动停止训练: {}".format(self._training_record_id))
        self._hide_train_task()
        rid = self._training_record_id
        self._training_record_id = None
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
        # 同步最新指标到进度条文本(分类->精度, 检测/分割→mAP@50)
        s = metrics.get("series", {})
        if s.get("accuracy"):
            self._latest_map50 = float(s["accuracy"][-1])
            self._apply_progress_format()
        elif s.get("mAP@50"):
            self._latest_map50 = float(s["mAP@50"][-1])
            self._apply_progress_format()
        self._pending_metrics = metrics
        if self._training_record_id:
            self.update_train_metrics(self._training_record_id, metrics)

    def _on_train_done(self, result):
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
        rid = self._training_record_id
        self._hide_train_task()
        self._training_record_id = None
        self._train_worker = None
        if rid:
            self.on_train_finished(rid, None)
        for line in detail.splitlines():
            self._log("[train] " + line)
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
                if s.get("mAP@50"):
                    r["map50"] = "{:.3f}".format(float(s["mAP@50"][-1]))
                if s.get("accuracy"):
                    r["accuracy"] = "{:.4f}".format(float(s["accuracy"][-1]))
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
        """进度条文本:`30% | 0.556` 进度 | 精度 """
        m = self._latest_map50
        tail = "{:.3f}".format(m) if m is not None else "--"
        self.train_progress.setFormat("%p% | " + tail)

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
