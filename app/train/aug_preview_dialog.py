# -*- coding: utf-8 -*-
"""
数据增强预览: 原图 / 增强结果对照, 一次给出多个随机采样.

增强本身是随机的(翻转 p=0.5、模糊 p=0.3), 只给一张对照图经常什么变化都看不出来,
所以下面一排缩略图各是一次独立采样, 概率项的"有时生效有时不生效"才看得出来.
"""

import random

import cv2
import numpy as np
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
                               QGridLayout, QHBoxLayout, QLabel, QPushButton,
                               QVBoxLayout, QWidget)

from app.train import aug_preview as ap
from app.train.aug_params import (AUG_BOTH, AUG_FAMILIES,
                                  resolve_aug_config, resolve_yolo_aug)

SIDE = 232          # 对照图边长
CARD_H = SIDE + 40  # 卡片外框高: 标题行 + 内边距, 两侧必须等高才不显得谁被拉长
THUMB = 74          # 采样缩略图边长
SAMPLES = 6         # 一次给几个采样
MOSAIC_POOL = 8     # 马赛克另外三格的候选张数

ARCH_TEXT = {"cnn": "CNN", "transformer": "Transformer"}
BACKEND_TEXT = {"cnn": "ultralytics", "transformer": "rfdetr"}


class _Thumb(QLabel):
    """可点的采样缩略图: 点了把主视图切过去."""

    clicked = Signal(int)

    def __init__(self, index, parent=None):
        super().__init__(parent)
        self._index = index
        self.setFixedSize(THUMB + 4, THUMB + 4)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)
        self.setProperty("class", "augThumb")
        self.setProperty("on", "false")

    def mousePressEvent(self, event):
        self.clicked.emit(self._index)
        super().mousePressEvent(event)

    def set_active(self, active):
        self.setProperty("on", "true" if active else "false")
        self.style().unpolish(self)
        self.style().polish(self)


class AugPreviewDialog(QDialog):
    def __init__(self, parent, db, ds_pairs, codes, backend, task, img_size):
        super().__init__(parent)
        self.setObjectName("AugPreviewDialog")
        self.setWindowTitle(self.tr("数据增强预览"))
        self._db = db
        self._codes = list(codes)
        self._backend = backend if backend in ARCH_TEXT else "transformer"
        self._task = task
        self._size = max(160, int(img_size or 640))
        # 解析函数吃的是记录里那种逗号串, 别把 list 直接喂进去
        codes_text = ",".join(self._codes)
        self._params = (resolve_yolo_aug(codes_text) if self._backend == "cnn"
                        else resolve_aug_config(codes_text))
        self._entries = []
        self._primary = None
        self._base_img = None
        self._base_shapes = []
        self._pool = []
        self._results = []
        self._current = 0
        self._show_labels = True
        self._seed = random.randrange(1, 9000)
        self._rng = random.Random()
        self._build()
        self._collect(ds_pairs)
        self._next_image()
        self.adjustSize()

    # ---------- 界面 ----------
    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(10)

        head = QHBoxLayout()
        head.setSpacing(8)
        self._meta = QLabel("", self)
        self._meta.setProperty("class", "augMeta")
        head.addWidget(self._meta)
        head.addStretch(1)
        head.addWidget(self._tool_button(self.tr("换图"), self._next_image))
        head.addWidget(self._tool_button(self.tr("换一批"), self._next_batch))
        lay.addLayout(head)

        body = QHBoxLayout()
        body.setSpacing(12)
        self._pane_orig = self._pane()
        body.addWidget(self._card(self.tr("原图"), self._pane_orig))
        arrow = QLabel("→", self)
        arrow.setProperty("class", "augArrow")
        arrow.setAlignment(Qt.AlignCenter)
        arrow.setFixedWidth(24)
        body.addWidget(arrow)
        self._pane_aug = self._pane()
        self._sample_title = QLabel("", self)
        self._sample_title.setProperty("class", "augSampleTip")
        body.addWidget(self._card(self.tr("增强后"), self._pane_aug,
                                  self._sample_title))
        body.addWidget(self._params_panel(), 1)
        lay.addLayout(body)

        strips = QHBoxLayout()
        strips.setSpacing(6)
        self._thumbs = []
        for i in range(SAMPLES):
            thumb = _Thumb(i, self)
            thumb.clicked.connect(self._select)
            self._thumbs.append(thumb)
            strips.addWidget(thumb)
        strips.addStretch(1)
        self._hint = QLabel(self.tr("每次采样独立随机, 概率项不一定每次都生效"), self)
        self._hint.setProperty("class", "augMeta")
        strips.addWidget(self._hint)
        lay.addLayout(strips)

        foot = QHBoxLayout()
        foot.setSpacing(14)
        self._labels_box = QCheckBox(self.tr("显示标注"), self)
        self._labels_box.setChecked(True)
        self._labels_box.toggled.connect(self._on_labels_toggled)
        foot.addWidget(self._labels_box)
        self._seed_label = QLabel("", self)
        self._seed_label.setProperty("class", "augMeta")
        foot.addWidget(self._seed_label)
        foot.addStretch(1)
        close_btn = QPushButton(self.tr("关闭"), self)
        close_btn.clicked.connect(self.accept)
        foot.addWidget(close_btn)
        lay.addLayout(foot)

        self.setMinimumWidth(880)

    def _tool_button(self, text, slot):
        btn = QPushButton(text, self)
        btn.setProperty("class", "ghost")
        btn.clicked.connect(lambda: slot())
        return btn

    def _pane(self):
        label = QLabel(self)
        label.setFixedSize(SIDE, SIDE)
        label.setAlignment(Qt.AlignCenter)
        label.setProperty("class", "augPane")
        return label

    def _card(self, title, pane, subtitle=None):
        card = QFrame(self)
        card.setProperty("class", "augCard")
        card.setFixedHeight(CARD_H)
        box = QVBoxLayout(card)
        box.setContentsMargins(8, 7, 8, 8)
        box.setSpacing(6)
        head = QHBoxLayout()
        head.setSpacing(7)
        name = QLabel(title, card)
        name.setProperty("class", "augCardTitle")
        head.addWidget(name)
        if subtitle is not None:
            head.addWidget(subtitle)
        head.addStretch(1)
        box.addLayout(head)
        box.addWidget(pane)
        return card

    def _params_panel(self):
        panel = QFrame(self)
        panel.setProperty("class", "augParams")
        panel.setFixedWidth(236)
        panel.setFixedHeight(CARD_H)
        box = QVBoxLayout(panel)
        box.setContentsMargins(10, 9, 10, 10)
        box.setSpacing(7)
        head = QHBoxLayout()
        title = QLabel(self.tr("实际下发的参数"), panel)
        title.setProperty("class", "augParamHead")
        head.addWidget(title)
        head.addStretch(1)
        self._count = QLabel("", panel)
        self._count.setProperty("class", "augParamCount")
        head.addWidget(self._count)
        box.addLayout(head)

        self._grid_host = QWidget(panel)
        self._grid = QGridLayout(self._grid_host)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(8)
        self._grid.setVerticalSpacing(5)
        box.addWidget(self._grid_host)

        self._empty = QLabel(self.tr("未启用任何增强"), panel)
        self._empty.setProperty("class", "augMeta")
        box.addWidget(self._empty)
        box.addStretch(1)

        self._blocked = QLabel("", panel)
        self._blocked.setProperty("class", "augWarn")
        self._blocked.setWordWrap(True)
        box.addWidget(self._blocked)

        note = QLabel(self.tr("与训练端同一份解析"), panel)
        note.setProperty("class", "augFine")
        box.addWidget(note)
        return panel

    def _next_batch(self):
        """换一批: 同一张图重新抽一批采样, 种子也换, 否则拍出来一模一样."""
        self._seed = random.randrange(1, 9000)
        self._resample()

    # ---------- 数据 ----------
    def _collect(self, ds_pairs):
        for proj, name in (ds_pairs or []):
            info = self._db.get_dataset_import(proj, name) or {}
            self._entries.extend(ap.dataset_images(info))

    def _next_image(self):
        if not self._entries:
            self._meta.setText(self.tr("训练集里没有可读的图像"))
            self._empty.setText(self.tr("没有可预览的图像"))
            return
        entries = list(self._entries)
        self._rng.shuffle(entries)
        # 有标注的排前面: 抽到没框的图, 几何增强等于没东西可看
        entries.sort(key=lambda e: 0 if ap.has_label(e) else 1)
        primary = None
        for entry in entries:
            primary = ap.load_sample(entry)
            if primary is not None:
                break
        if primary is None:
            self._meta.setText(self.tr("训练集里没有可读的图像"))
            return
        self._primary = primary
        boxed = ap.letterbox(primary["image"], primary["shapes"], self._size)
        self._base_img, self._base_shapes = boxed
        self._source = (primary["image"], primary["shapes"])
        self._pool = []
        for entry in entries[1:]:
            if len(self._pool) >= MOSAIC_POOL:
                break
            if entry[0] == primary["path"]:
                continue
            sample = ap.load_sample(entry)
            if sample is None:
                continue
            # 马赛克要的是未 letterbox 的原图, 拼完再统一缩放
            self._pool.append((sample["image"], sample["shapes"]))
        self._describe()
        self._resample()

    def _describe(self):
        name = self._primary["name"] if self._primary else ""
        self._meta.setText(self.tr("{} · 可选 {} 张 · {} 架构 → {}").format(
            name, len(self._entries), ARCH_TEXT[self._backend],
            BACKEND_TEXT[self._backend]))
        self._fill_params()
        self._seed_label.setText(self.tr("种子 {}").format(self._seed))

    def _fill_params(self):
        while self._grid.count():
            item = self._grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        rows = ap.param_rows(self._params, self._backend)
        self._count.setText(str(len(rows)))
        self._empty.setVisible(not rows)
        for i, (name, value) in enumerate(rows):
            left = QLabel(name, self._grid_host)
            left.setProperty("class", "augParamName")
            right = QLabel(value, self._grid_host)
            right.setProperty("class", "augParamValue")
            right.setWordWrap(True)
            right.setToolTip(value)
            self._grid.addWidget(left, i, 0)
            self._grid.addWidget(right, i, 1)
        self._grid.setColumnStretch(1, 1)
        self._blocked.setText(self._blocked_text())

    def _blocked_text(self):
        names = [self.tr("模糊"), self.tr("噪声")] if self._backend == "cnn" \
            else [self.tr("马赛克")]
        return self.tr("当前架构不支持: {}").format(" / ".join(names))

    # ---------- 渲染 ----------
    def _resample(self):
        if self._base_img is None:
            return
        self._results = []
        others = self._pool if self._mosaic_on() else None
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            for i in range(SAMPLES):
                rng = random.Random(self._seed * 101 + i)
                img, boxes = ap.augment(self._base_img, self._base_shapes,
                                        self._params, self._backend, rng,
                                        others=others, source=self._source)
                self._results.append((img, boxes))
        finally:
            QApplication.restoreOverrideCursor()
        if self._current >= len(self._results):
            self._current = 0
        self._refresh()
        self._seed_label.setText(self.tr("种子 {}").format(self._seed))

    def _mosaic_on(self):
        return "mosaic" in self._codes and self._backend in AUG_FAMILIES.get(
            "mosaic", AUG_BOTH)

    def _paint(self, img, shapes):
        return ap.draw(img, shapes, self._task, self._show_labels)

    def _to_pixmap(self, img, side):
        rgb = np.ascontiguousarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        h, w = rgb.shape[:2]
        qimg = QImage(rgb.data, w, h, w * 3, QImage.Format_RGB888).copy()
        return QPixmap.fromImage(qimg).scaled(
            side, side, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def _refresh(self):
        if self._base_img is None:
            return
        self._pane_orig.setPixmap(self._to_pixmap(
            self._paint(self._base_img, self._base_shapes), SIDE))
        for i, thumb in enumerate(self._thumbs):
            if i >= len(self._results):
                thumb.clear()
                continue
            img, boxes = self._results[i]
            thumb.setPixmap(self._to_pixmap(self._paint(img, boxes), THUMB))
            thumb.set_active(i == self._current)
        self._show_current()
        self._sample_title.setText(self._sample_caption())

    def _sample_caption(self):
        text = self.tr("采样 #{}").format(self._current + 1)
        if self._mosaic_on():
            text += self.tr(" · {} 图拼接").format(4)
        return text

    def _show_current(self):
        if not self._results:
            return
        img, boxes = self._results[self._current]
        self._pane_aug.setPixmap(self._to_pixmap(self._paint(img, boxes), SIDE))

    def _select(self, index):
        if index >= len(self._results):
            return
        self._current = index
        for i, thumb in enumerate(self._thumbs):
            thumb.set_active(i == index)
        self._show_current()
        self._sample_title.setText(self._sample_caption())

    def _on_labels_toggled(self, checked):
        self._show_labels = bool(checked)
        self._refresh()
