# -*- coding: utf-8 -*-
"""训练队列调度：串行执行 db 里的任务快照，逐个走与手工训练完全相同的启动链路。

依赖 TrainMixin 提供 is_training / start_training / on_train_finished / db / _log。
"""

import os
import uuid
from datetime import datetime

from PySide6.QtCore import QTimer

from app.core.log import write_log
from app.train.dialogs import (make_train_config, make_train_record,
                               params_summary)

try:
    import pynvml
except ImportError:
    pynvml = None

# 任务切换的冷却：等显存真正释放后再起下一个，避免 CUDA OOM
COOLDOWN_MS = 5000
COOLDOWN_MAX_MS = 30000

STATUS_TEXT = {
    "waiting": "等待中",
    "running": "训练中",
    "done": "已完成",
    "failed": "失败",
    "skipped": "已跳过",
    "stopped": "已停止",
    "interrupted": "已中断",
}
_DONE_STATUS = ("done", "failed", "skipped", "stopped", "interrupted")


class QueueMixin(object):
    _queue_running = False      # 队列引擎激活中
    _queue_paused = False       # 暂停：当前任务跑完不再取下一个
    _queue_current_qid = None
    _queue_finished_rids = None  # 本轮已收尾的 record_id，防重复推进
    _queue_cooling = False
    _cooldown_elapsed = 0

    # ---------- 查询 ----------
    def queue_items(self):
        return self.db.get_train_queue()

    def queue_pending_count(self):
        """未完成的任务数（工具栏角标用）。"""
        return len([it for it in self.queue_items()
                    if it.get("status") not in _DONE_STATUS])

    def queue_is_running(self):
        return bool(self._queue_running)

    def queue_is_paused(self):
        return bool(self._queue_paused)

    # ---------- 入队 ----------
    def enqueue_train(self, params):
        """把参数快照追加到队尾。不建目录、不落配置，一切推迟到出队。"""
        items = self.queue_items()
        order = max([int(it.get("order") or 0) for it in items], default=-1) + 1
        item = {
            "qid": str(uuid.uuid4()),
            "name": params_summary(params),
            "order": order,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "waiting",
            "record_id": "",
            "error": "",
            "started_at": "",
            "finished_at": "",
            "params": params,
        }
        items.append(item)
        self.db.save_train_queue(items)
        self._refresh_queue_ui()
        return item

    # ---------- 控制 ----------
    def start_train_queue(self):
        """开始/继续队列。已在训练则交给队列接管收尾，不重复启动。"""
        if self.is_training():
            return False
        self._queue_running = True
        self._queue_paused = False
        self._queue_finished_rids = set()
        write_log("训练队列已启动")
        self._refresh_queue_ui()
        self._pump_queue()
        return True

    def pause_train_queue(self):
        """暂停：当前任务继续跑完，不再取下一个。"""
        if not self._queue_running:
            return
        self._queue_paused = True
        self._log("[队列] 已暂停，当前任务完成后停止")
        self._refresh_queue_ui()

    def resume_train_queue(self):
        """从暂停恢复（引擎还活着，只是不再取任务）。"""
        if not self._queue_running:
            return False
        self._queue_paused = False
        self._log("[队列] 已继续")
        self._refresh_queue_ui()
        self._pump_queue()
        return True

    def stop_train_queue(self):
        """停止队列：暂停调度（不改动任务状态，可再次启动继续）。"""
        self._queue_paused = True
        self._queue_running = False
        self._queue_current_qid = None
        self._log("[队列] 已停止")
        self._refresh_queue_ui()

    # ---------- 队列编辑 ----------
    def queue_move(self, qid, delta):
        """上移/下移：只改 order，等待中的任务之间互换。"""
        items = self.queue_items()
        idx = next((i for i, it in enumerate(items) if it.get("qid") == qid), None)
        if idx is None:
            return
        target = idx + delta
        if target < 0 or target >= len(items):
            return
        items[idx]["order"], items[target]["order"] = (
            items[target]["order"], items[idx]["order"])
        self.db.save_train_queue(items)
        self._refresh_queue_ui()

    def queue_remove(self, qid):
        """移除任务（训练中的不允许移除）。"""
        items = self.queue_items()
        item = next((it for it in items if it.get("qid") == qid), None)
        if item is None or item.get("status") == "running":
            return False
        self.db.save_train_queue([it for it in items if it.get("qid") != qid])
        self._refresh_queue_ui()
        return True

    def queue_clear_done(self):
        """清掉已结束的任务（保留 waiting）。"""
        items = self.queue_items()
        kept = [it for it in items if it.get("status") not in _DONE_STATUS]
        if len(kept) == len(items):
            return 0
        self.db.save_train_queue(kept)
        self._refresh_queue_ui()
        return len(items) - len(kept)

    def queue_requeue(self, qid):
        """重新入队：放回队尾，状态重置为 waiting。"""
        items = self.queue_items()
        item = next((it for it in items if it.get("qid") == qid), None)
        if item is None or item.get("status") == "running":
            return False
        item["status"] = "waiting"
        item["error"] = ""
        item["record_id"] = ""
        item["started_at"] = ""
        item["finished_at"] = ""
        item["order"] = max([int(it.get("order") or 0) for it in items],
                            default=-1) + 1
        self.db.save_train_queue(items)
        self._refresh_queue_ui()
        return True

    def queue_update_params(self, qid, params):
        """「编辑」保存：只改参数快照与名称，等待中的任务可改。"""
        items = self.queue_items()
        item = next((it for it in items if it.get("qid") == qid), None)
        if item is None or item.get("status") == "running":
            return False
        item["params"] = params
        item["name"] = params_summary(params)
        self.db.save_train_queue(items)
        self._refresh_queue_ui()
        return True

    # ---------- 调度 ----------
    def _pump_queue(self):
        """取下一个任务启动；没有则结束本轮队列。"""
        if not self._queue_running or self._queue_paused:
            return
        if self.is_training():
            return
        item = self._next_waiting()
        if item is None:
            self._queue_running = False
            self._queue_current_qid = None
            self._log("[队列] 所有任务已执行完毕")
            self._refresh_queue_ui()
            return
        try:
            self._start_queue_item(item)
        except Exception as exc:
            # 出队失败不能中断整个队列：标记后继续下一个
            self._mark_item(item["qid"], "failed", error=str(exc))
            self._log("[队列] 跳过任务 {}: {}".format(item.get("name"), exc))
            write_log("队列任务启动失败 {}: {}".format(item.get("name"), exc))
            QTimer.singleShot(0, self._pump_queue)

    def _next_waiting(self):
        for it in self.queue_items():
            if it.get("status") == "waiting":
                return it
        return None

    def _start_queue_item(self, item):
        """出队五步：解析 → 校验 → 落盘 → 建记录 → 启动。"""
        params = item["params"]
        # data.yaml / 标签集合都由 make_train_config 之后的 runner 现算，
        # 这里只负责把 db 里的最新路径与 label_ids 解析进 config
        config = make_train_config(self.db, params)
        record = make_train_record(
            config, self.db, (params.get("train_ds") or [["", ""]])[0][0])
        self.db.add_train_record(record)
        if not self.start_training(config, record["id"]):
            self.db.delete_train_record(record["id"])
            raise RuntimeError("已有训练在进行中")
        self._queue_current_qid = item["qid"]
        self._mark_item(item["qid"], "running",
                        record_id=record["id"],
                        started_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self._log("[队列] 开始任务 {}/{}: {}".format(
            int(item.get("order") or 0) + 1,
            len([i for i in self.queue_items()
                 if i.get("status") != "waiting"]) + 1,
            item.get("name", "")))
        write_log("队列启动任务: {} record={}".format(
            item.get("name"), record["id"]))
        self._refresh_queue_ui()

    def _mark_item(self, qid, status, **fields):
        items = self.queue_items()
        for it in items:
            if it.get("qid") == qid:
                it["status"] = status
                it.update(fields)
                if status in _DONE_STATUS:
                    it["finished_at"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")
                break
        else:
            return
        self.db.save_train_queue(items)

    def on_queue_train_finished(self, record_id, result, stopped=False):
        """训练收尾（由 TrainMixin.on_train_finished 调用）。

        幂等：finished 信号与 finished_ok/failed 可能都触发，靠 record_id 去重，
        否则队列会一次连跳两个任务。
        """
        if self._queue_finished_rids is None:
            self._queue_finished_rids = set()
        qid = self._queue_current_qid
        if not qid:
            return
        if record_id and record_id in self._queue_finished_rids:
            return
        if record_id:
            self._queue_finished_rids.add(record_id)
        status = "stopped" if stopped else ("done" if result else "failed")
        if result is None and not stopped:
            # 失败原因取自训练记录里已写入的日志，队列项只留一行提示
            self._mark_item(qid, status, error="训练未完成，详见日志")
        else:
            self._mark_item(qid, status)
        self._queue_current_qid = None
        if not self._queue_running or self._queue_paused:
            self._refresh_queue_ui()
            return
        self._wait_gpu_then_pump()

    def _wait_gpu_then_pump(self):
        """等显存回落再启动下一个，避免上一个任务的显存还没释放就 OOM。"""
        if self._queue_cooling:
            return
        self._queue_cooling = True
        self._cooldown_elapsed = 0
        self._tick_cooldown()

    def _tick_cooldown(self):
        worker = getattr(self, "_train_worker", None)
        exited = True if worker is None else worker.proc_exited()
        if exited and self._gpu_free():
            self._queue_cooling = False
            QTimer.singleShot(0, self._pump_queue)
            return
        self._cooldown_elapsed += COOLDOWN_MS
        if self._cooldown_elapsed >= COOLDOWN_MAX_MS:
            self._queue_cooling = False
            self._log("[队列] 显存等待超时，仍继续启动下一个任务")
            QTimer.singleShot(0, self._pump_queue)
            return
        QTimer.singleShot(COOLDOWN_MS, self._tick_cooldown)

    def _gpu_free(self):
        """显存占用是否回落到阈值以下；pynvml 不可用时退化为只看进程退出。"""
        if pynvml is None:
            return True
        try:
            if self._nvml_state is None:
                pynvml.nvmlInit()
                self._nvml_state = True
            used, total = 0, 0
            for i in range(pynvml.nvmlDeviceGetCount()):
                h = pynvml.nvmlDeviceGetHandleByIndex(i)
                mem = pynvml.nvmlDeviceGetMemoryInfo(h)
                used += mem.used
                total += mem.total
            return total > 0 and used / float(total) < 0.25
        except Exception:
            return True

    # ---------- UI 回调（由主窗口/队列面板实现）----------
    def _refresh_queue_ui(self):
        """刷新工具栏角标与队列面板（存在时）。"""
        # 主窗口用 setupUi(self)，控件直接挂在 self 上（训练对话框才是 self.ui.xxx）
        btn = getattr(self, "queue_btn", None)
        if btn is not None:
            n = self.queue_pending_count()
            btn.setText("队列 {}".format(n) if n else "队列")
        dlg = getattr(self, "_queue_dialog", None)
        if dlg is not None and getattr(dlg, "isVisible", lambda: False)():
            dlg.refresh()
