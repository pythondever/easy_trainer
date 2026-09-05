# -*- coding: utf-8 -*-
"""训练队列面板：查看/排序/编辑队列任务，控制队列的启动与暂停。"""

import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QAbstractItemView,
                               QHeaderView, QMenu)

from app.widgets.message_box import MessageBox
from app.train.dialogs import TrainDialog, params_to_record
from app.mixins.queue_mixin import STATUS_TEXT
from ui.train_queue import Ui_TrainQueueDialog

STATUS_COLOR = {
    "waiting": "#8b93a5",
    "running": "#4f7dff",
    "done": "#7be39a",
    "failed": "#ff9aa2",
    "skipped": "#ffd166",
    "stopped": "#ffd166",
    "interrupted": "#ffd166",
}
TASK_TEXT = {"detect": "检测", "segment": "分割", "classify": "分类"}


class TrainQueueDialog(QDialog):
    """非模态队列面板：关闭只是隐藏，队列继续在后台跑。"""

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.ui = Ui_TrainQueueDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("训练队列")
        self.app = app
        self._setup_table()
        self._connect()
        self.refresh()

    # ---------- 初始化 ----------
    def _setup_table(self):
        t = self.ui.queue_table
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.setSelectionBehavior(QAbstractItemView.SelectRows)
        t.setSelectionMode(QAbstractItemView.SingleSelection)
        h = t.horizontalHeader()
        widths = {
            0: (QHeaderView.ResizeToContents, 50),   # #
            1: (QHeaderView.Stretch, 0),             # 名称
            2: (QHeaderView.ResizeToContents, 70),   # 任务
            3: (QHeaderView.Interactive, 220),       # 数据集
            4: (QHeaderView.ResizeToContents, 80),   # 网络
            5: (QHeaderView.ResizeToContents, 70),   # 轮次
            6: (QHeaderView.ResizeToContents, 90),   # 状态
        }
        for i, (mode, w) in widths.items():
            h.setSectionResizeMode(i, mode)
            if w:
                t.setColumnWidth(i, w)
        h.setMinimumSectionSize(50)
        t.verticalHeader().setDefaultSectionSize(40)
        t.setContextMenuPolicy(Qt.CustomContextMenu)
        t.customContextMenuRequested.connect(self._on_menu)

    def _connect(self):
        self.ui.start_btn.clicked.connect(self._on_start_btn)
        self.ui.edit_btn.clicked.connect(self._on_edit)
        self.ui.move_up_btn.clicked.connect(lambda: self._on_move(-1))
        self.ui.move_down_btn.clicked.connect(lambda: self._on_move(1))
        self.ui.remove_btn.clicked.connect(self._on_remove)
        self.ui.clear_done_btn.clicked.connect(self._on_clear_done)
        self.ui.close_btn.clicked.connect(self.hide)
        self.ui.queue_table.doubleClicked.connect(self._on_edit)

    def closeEvent(self, event):
        self.app._queue_dialog = None
        super().closeEvent(event)

    # ---------- 渲染 ----------
    def refresh(self):
        items = self.app.queue_items()
        t = self.ui.queue_table
        t.setRowCount(len(items))
        for row, it in enumerate(items):
            params = it.get("params") or {}
            names = [p[1] for p in (params.get("train_ds") or [])]
            vals = [
                str(int(it.get("order") or 0) + 1),
                it.get("name", ""),
                TASK_TEXT.get(params.get("task", ""), params.get("task", "")),
                ", ".join(names),
                params.get("architecture", ""),
                str(params.get("epochs", "")),
                STATUS_TEXT.get(it.get("status", ""), it.get("status", "")),
            ]
            for col, text in enumerate(vals):
                cell = QTableWidgetItem(text)
                if col == 6:
                    cell.setForeground(QColor(
                        STATUS_COLOR.get(it.get("status", ""), "#e8eaf0")))
                if col == 1 and it.get("error"):
                    cell.setToolTip(it["error"])
                t.setItem(row, col, cell)
        self._update_header(items)

    def _update_header(self, items):
        running = [i for i in items if i.get("status") == "running"]
        waiting = [i for i in items if i.get("status") == "waiting"]
        done = [i for i in items if i.get("status") == "done"]
        failed = [i for i in items if i.get("status") in ("failed", "skipped")]
        if self.app.queue_is_running():
            if self.app.queue_is_paused():
                badge, tip = "已暂停", "当前任务完成后停止，可点「继续队列」恢复"
            else:
                badge, tip = "运行中", "队列正在串行执行"
        elif waiting:
            badge, tip = "待启动", "有 {} 个任务等待启动".format(len(waiting))
        elif running:
            badge, tip = "训练中", "当前有训练在进行（非队列启动）"
        else:
            badge, tip = "空闲", "队列为空，可在训练界面点「加入队列」添加任务"
        self.ui.queue_badge.setText(badge)
        self.ui.queue_badge.setToolTip(tip)
        if items:
            summary = "共 {} 个：等待 {} · 完成 {} · 失败 {}".format(
                len(items), len(waiting), len(done), len(failed))
            if running:
                summary = "正在训练「{}」 · {}".format(
                    running[0].get("name", ""), summary)
            elif waiting:
                summary = "下一个：「{}」 · {}".format(
                    waiting[0].get("name", ""), summary)
        else:
            summary = "队列为空，可在训练界面点「加入队列」添加任务"
        self.ui.summary_text.setText(summary)
        self._update_buttons(items)

    def _update_buttons(self, items):
        paused = self.app.queue_is_running() and self.app.queue_is_paused()
        self.ui.start_btn.setText("继续队列" if paused else "开始队列")
        has_waiting = any(i.get("status") == "waiting" for i in items)
        self.ui.start_btn.setEnabled(
            not self.app.is_training() and (has_waiting or paused))
        for btn in (self.ui.move_up_btn, self.ui.move_down_btn,
                    self.ui.remove_btn, self.ui.edit_btn):
            btn.setEnabled(bool(self._current_item()))
        self.ui.clear_done_btn.setEnabled(
            any(i.get("status") in ("done", "failed", "skipped",
                                    "stopped", "interrupted") for i in items))

    # ---------- 交互 ----------
    def _current_item(self):
        row = self.ui.queue_table.currentRow()
        items = self.app.queue_items()
        if 0 <= row < len(items):
            return items[row]
        return None

    def _on_start_btn(self):
        if self.app.is_training():
            MessageBox.warning(self, "队列", "已有训练在进行中，请先停止")
            return
        if self.app.queue_is_paused() and self.app.queue_is_running():
            self.app.resume_train_queue()
            self.refresh()
            return
        if not self.app.start_train_queue():
            MessageBox.warning(self, "队列", "队列启动失败，请查看日志")
        self.refresh()

    def _on_move(self, delta):
        item = self._current_item()
        if item is None or item.get("status") == "running":
            return
        row = self.ui.queue_table.currentRow()
        self.app.queue_move(item["qid"], delta)
        self.ui.queue_table.selectRow(max(0, row + delta))

    def _on_remove(self):
        item = self._current_item()
        if item is None:
            return
        if item.get("status") == "running":
            MessageBox.warning(self, "移除任务", "训练中的任务不能移除，请先停止")
            return
        if not MessageBox.question(self, "移除任务",
                                   "确定从队列中移除「{}」吗？".format(item["name"])):
            return
        self.app.queue_remove(item["qid"])

    def _on_clear_done(self):
        n = self.app.queue_clear_done()
        if not n:
            MessageBox.information(self, "清理", "没有已完成的任务")
            return
        self.app._log("[队列] 已清理 {} 个已结束任务".format(n))

    def _on_edit(self):
        item = self._current_item()
        if item is None:
            return
        if item.get("status") == "running":
            MessageBox.warning(self, "编辑任务", "训练中的任务不能编辑，请先停止")
            return
        dlg = TrainDialog(self.app, preset_record=params_to_record(
            item.get("params") or {}))
        dlg.queue_edit_qid = item["qid"]
        dlg.exec()
        dlg.deleteLater()
        self.refresh()

    def _on_menu(self, pos):
        item = self._current_item()
        if item is None:
            return
        menu = QMenu(self)
        status = item.get("status", "")
        if status in ("done", "failed", "skipped", "stopped", "interrupted"):
            menu.addAction("重新入队", lambda: self.app.queue_requeue(item["qid"]))
        act_open = menu.addAction("打开输出目录", lambda: self._open_output(item))
        act_model = menu.addAction("在模型界面查看", lambda: self._open_model(item))
        act_open.setEnabled(item.get("status") in ("done", "failed", "running")
                            or bool(item.get("record_id")))
        act_model.setEnabled(bool(item.get("record_id")))
        menu.addAction("移除", self._on_remove)
        menu.exec(self.ui.queue_table.viewport().mapToGlobal(pos))

    def _output_dir(self, item):
        """任务的真实输出目录：优先取训练记录里的 timestamp_dir。"""
        rid = item.get("record_id")
        for r in self.app.db.get_train_records():
            if r.get("id") == rid and r.get("model_path"):
                return os.path.dirname(r["model_path"])
        return (item.get("params") or {}).get("out_root", "")

    def _open_output(self, item):
        d = self._output_dir(item)
        if not d or not os.path.isdir(d):
            MessageBox.warning(self, "打开输出目录", "目录不存在：{}".format(d or "未设置"))
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(d))

    def _open_model(self, item):
        from app.widgets.model_dialog import ModelDialog
        self.hide()
        md = ModelDialog(app=self.app, project="", dataset="", parent=self.app)
        md.exec()
        md.deleteLater()
