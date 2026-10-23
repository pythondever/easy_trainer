# -*- coding: utf-8 -*-
"""错图检视: 把测试明细里的漏检/误检一张张看过去.

明细只记有问题的图, 所以这里是"排错"而不是"浏览全部": 左边列出有问题的图,
右边大图对照, 顶部按漏检/误检筛. 大图区复用标注预览那套缩放控件, 放大看位置
关系和标注界面一致.
"""

import os

import cv2
from PIL.Image import fromarray
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
                               QLabel, QListWidget, QListWidgetItem,
                               QPushButton, QVBoxLayout, QWidget)

from app.core.image_utils import pil_to_qimage
from app.train import pred_viewer as pv
from app.widgets.zoom_view import ZoomView


THUMB = 52          # 列表缩略图边长
SIDE = 360          # 大图区最小边长
LIST_W = 236        # 列表宽


class PredictionViewerDialog(QDialog):
    def __init__(self, parent, res, task, kind="all"):
        super().__init__(parent)
        self.setObjectName("PredictionViewerDialog")
        self.setWindowTitle(self.tr("错图检视"))
        self._task = task if task in ("detect", "segment") else "detect"
        self._rows = pv.load_rows(res.get("detail_path"))
        self._kind = kind if kind in ("all", pv.MISS, pv.FP) else "all"
        self._view = []
        self._cur = -1
        self._build()
        self._apply_filter(self._kind)

    # ---------- 界面 ----------
    def _build(self):
        self.setMinimumSize(780, 480)
        # QDialog 默认没有最大化按钮, 图要大看得清就得能拉满屏
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        head = QHBoxLayout()
        self._title = QLabel("", self)
        self._title.setProperty("class", "augGroupTitle")
        head.addWidget(self._title)
        head.addStretch()
        self._btns = {}
        for key, text in (("all", self.tr("全部")),
                          (pv.MISS, self.tr("漏检")),
                          (pv.FP, self.tr("误检"))):
            btn = QPushButton(text, self)
            btn.setProperty("class", "ghost")
            btn.clicked.connect(lambda _c, k=key: self._apply_filter(k))
            self._btns[key] = btn
            head.addWidget(btn)
        lay.addLayout(head)

        body = QHBoxLayout()
        body.setSpacing(12)
        self._list = QListWidget(self)
        self._list.setProperty("class", "predList")
        self._list.setViewMode(QListWidget.ListMode)
        self._list.setIconSize(QSize(THUMB, THUMB))
        self._list.setUniformItemSizes(True)
        self._list.setMinimumWidth(LIST_W)
        self._list.setMaximumWidth(LIST_W)
        self._list.itemClicked.connect(self._on_clicked)
        body.addWidget(self._list)

        self._pane = ZoomView(SIDE, self, "predPane")
        body.addWidget(self._pane, 1)
        self._empty = QLabel(self.tr("这次测试没有漏检和误检"), self)
        self._empty.setProperty("class", "augMeta")
        self._empty.setAlignment(Qt.AlignCenter)
        self._empty.setVisible(False)
        body.addWidget(self._empty, 1)
        lay.addLayout(body, 1)

        # 翻页按钮居中; 左下放操作提示, 右下放标注图例——不把路径写在按钮中间,
        # 文件名在左侧列表里已经有, 重复一遍只是噪音
        foot = QHBoxLayout()
        self._hint = QLabel(self.tr("滚轮缩放 · 拖动平移 · 双击复位"), self)
        self._hint.setProperty("class", "augMeta")
        foot.addWidget(self._hint)
        foot.addStretch(1)
        self._prev_btn = QPushButton(self.tr("上一张"), self)
        self._prev_btn.setProperty("class", "augTool")
        self._prev_btn.clicked.connect(lambda: self._step(-1))
        foot.addWidget(self._prev_btn)
        self._next_btn = QPushButton(self.tr("下一张"), self)
        self._next_btn.setProperty("class", "augTool")
        self._next_btn.clicked.connect(lambda: self._step(1))
        foot.addWidget(self._next_btn)
        foot.addStretch(1)
        foot.addLayout(self._legend())
        lay.addLayout(foot)

    def _legend(self):
        """图例: 色块颜色和图上画的一致, 缺了它用户分不出哪条线是什么."""
        lay = QHBoxLayout()
        lay.setSpacing(6)
        items = (
            (self.tr("漏检"), pv.GT_MISS, self.tr("真值框, 模型没有检出 (实线填充)")),
            (self.tr("误检"), pv.PRED_FP, self.tr("模型多检出来的框 (虚线)")),
            (self.tr("检出"), pv.PRED_OK, self.tr("与真值匹配上的预测框 (虚线)")),
        )
        for text, bgr, tip in items:
            chip = QFrame(self)
            chip.setFixedSize(12, 12)
            chip.setStyleSheet("background-color: rgb({}, {}, {});"
                               "border-radius: 3px;".format(bgr[2], bgr[1],
                                                            bgr[0]))
            label = QLabel(text, self)
            label.setProperty("class", "augMeta")
            label.setToolTip(tip)
            lay.addWidget(chip)
            lay.addWidget(label)
            lay.addSpacing(10)
        lay.addStretch(1)
        return lay

    # ---------- 数据 ----------
    def _apply_filter(self, kind):
        self._kind = kind
        for key, btn in self._btns.items():
            btn.setProperty("on", "true" if key == kind else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        rows = pv.select(self._rows, kind)
        self._view = rows
        self._list.clear()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            for row in rows:
                item = QListWidgetItem(self._item_text(row))
                item.setToolTip(row["img"])
                thumb = pv.thumbnail(row["img"], THUMB)
                if thumb is not None:
                    item.setIcon(QPixmap.fromImage(pil_to_qimage(thumb)))
                item.setSizeHint(QSize(0, THUMB + 14))
                self._list.addItem(item)
        finally:
            QApplication.restoreOverrideCursor()
        self._title.setText(self._head_text())
        has = bool(rows)
        self._pane.setVisible(has)
        self._empty.setVisible(not has)
        self._show(0 if rows else -1)

    def _item_text(self, row):
        name = os.path.basename(row["img"])
        tags = []
        if row["missing"]:
            tags.append(self.tr("漏检 {}").format(len(row["missing"])))
        if row["spurious"]:
            tags.append(self.tr("误检 {}").format(len(row["spurious"])))
        return "{}\n{}".format(name, " · ".join(tags))

    def _head_text(self):
        if not self._view:
            if not self._rows:
                return self.tr("没有漏检和误检")
            return self.tr("没有{}的图").format(self._kind_name())
        s = pv.summary(self._view)
        return self.tr("{} 张有问题 · 漏检 {} 框 · 误检 {} 框").format(
            len(self._view), s["miss_boxes"], s["fp_boxes"])

    def _kind_name(self):
        return {pv.MISS: self.tr("漏检"), pv.FP: self.tr("误检")}.get(
            self._kind, "")

    def _on_clicked(self, item):
        self._show(self._list.row(item))

    def _step(self, delta):
        if not self._view:
            return
        self._show((self._cur + delta) % len(self._view))

    def _show(self, index):
        self._cur = index
        row = self._view[index] if 0 <= index < len(self._view) else None
        if row is None:
            self._pane.set_image(QPixmap())
            self._list.setCurrentRow(-1)
            self._prev_btn.setEnabled(False)
            self._next_btn.setEnabled(False)
            return
        self._prev_btn.setEnabled(len(self._view) > 1)
        self._next_btn.setEnabled(len(self._view) > 1)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            img = pv.render(row, self._task)
        finally:
            QApplication.restoreOverrideCursor()
        if img is None:
            # 图读不出来时原因写在大图区, 那里本来就是空着的
            self._empty.setText(self.tr("这张图读不出来: {}").format(row["img"]))
            self._empty.setVisible(True)
            self._pane.setVisible(False)
            self._pane.set_image(QPixmap())
        else:
            self._empty.setVisible(False)
            self._pane.setVisible(True)
            self._pane.set_image(self._to_pixmap(img), keep_view=True)
        self._list.setCurrentRow(index)

    @staticmethod
    def _to_pixmap(img):
        pil = fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return QPixmap.fromImage(pil_to_qimage(pil))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_Up:
            self._step(-1)
            event.accept()
            return
        if event.key() == Qt.Key_Right or event.key() == Qt.Key_Down:
            self._step(1)
            event.accept()
            return
        super().keyPressEvent(event)
