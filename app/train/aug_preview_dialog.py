# -*- coding: utf-8 -*-
"""
数据增强预览: 原图 / 增强结果对照, 一次给出多个随机采样.

增强本身是随机的(翻转 p=0.5、模糊 p=0.3), 只给一张对照图经常什么变化都看不出来,
所以下面一排缩略图各是一次独立采样, 概率项的"有时生效有时不生效"才看得出来.
"""

import random

import cv2
import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QImage, QPainter, QPixmap
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
                               QGridLayout, QHBoxLayout, QLabel, QPushButton,
                               QSizePolicy, QStyle, QStyleOption,
                               QStylePainter, QVBoxLayout, QWidget)

from app.train import aug_preview as ap
from app.train.aug_params import (AUG_BOTH, AUG_FAMILIES,
                                  resolve_aug_config, resolve_yolo_aug)

SIDE = 232          # 对照图最小边长, 窗口拉大时跟着变大
CARD_H = SIDE + 40  # 卡片最小高度: 标题行 + 内边距
THUMB = 74          # 采样缩略图边长
SAMPLES = 6         # 一次给几个采样
MOSAIC_POOL = 8     # 马赛克另外三格的候选张数
PREVIEW_MAX = 1600  # 预览渲染的长边上限; 原图往往比训练输入的 img_size 大得多


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


class _ZoomPane(QFrame):
    """
    主视图: 滚轮以光标为锚点缩放, 放大后按住左键平移, 双击回到适应窗口.

    1.0 是"整图塞进控件"而不是像素 1:1: letterbox 后的图比控件大得多, 按像素
    1:1 打开等于一上来就看局部, 对照反而无从下手.
    """

    STEP = 1.18        # 滚轮一格(120)的倍率
    ZOOM_CAP = 10.0    # 相对"适应窗口"的上限. 不按源像素折算, 那样窗口越大上限越小

    def __init__(self, side, parent=None):
        super().__init__(parent)
        self.setProperty("class", "augPane")
        self._pix = QPixmap()
        self._zoom = 1.0
        self._center = QPointF()
        self._drag_from = None      # (按下处, 按下时的中心)
        # 窗口最大化时这两块跟着长, 固定尺寸会把多出来的空间全让给空白
        self.setMinimumSize(side, side)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._reset()

    # ---------- 给外部 ----------
    def set_image(self, pixmap):
        """换采样时保持当前视口, 方便同一处对照; 图尺寸变了才复位."""
        same = (not self._pix.isNull() and not pixmap.isNull()
                and pixmap.size() == self._pix.size())
        self._pix = pixmap
        if same:
            self._clamp()
        else:
            self._reset()
        self.update()

    def reset_view(self):
        self._reset()
        self.update()

    # ---------- 几何 ----------
    def _fit(self):
        if self._pix.isNull():
            return 1.0
        return min(self.width() / self._pix.width(),
                   self.height() / self._pix.height())

    def _scale(self):
        return self._fit() * self._zoom

    def _max_zoom(self):
        return self.ZOOM_CAP

    def _reset(self):
        self._zoom = 1.0
        self._center = QPointF(self.width() / 2.0, self.height() / 2.0)
        self._drag_from = None
        self._update_cursor()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 控件尺寸一变 fit 比例就变, 视口要重新夹一遍才不会露白
        self._clamp()

    def _clamp(self):
        """图比控件小就居中, 比控件大就不许把边拖进控件里面."""
        if self._pix.isNull():
            return
        scale = self._scale()
        half_w = self._pix.width() * scale / 2.0
        half_h = self._pix.height() * scale / 2.0
        cx, cy = self._center.x(), self._center.y()
        if half_w * 2 <= self.width():
            cx = self.width() / 2.0
        else:
            cx = min(max(cx, self.width() - half_w), half_w)
        if half_h * 2 <= self.height():
            cy = self.height() / 2.0
        else:
            cy = min(max(cy, self.height() - half_h), half_h)
        self._center = QPointF(cx, cy)

    def _apply_zoom(self, target, anchor):
        target = max(1.0, min(self._max_zoom(), target))
        if abs(target - self._zoom) < 1e-3:
            return
        ratio = target / self._zoom
        # 光标下的那个像素保持不动
        self._center = anchor + (self._center - anchor) * ratio
        self._zoom = target
        self._clamp()
        self._update_cursor()
        self.update()

    def _update_cursor(self):
        if self._drag_from is not None:
            self.setCursor(Qt.ClosedHandCursor)
        elif self._zoom > 1.001:
            self.setCursor(Qt.OpenHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    # ---------- 绘制 ----------
    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOption()
        opt.initFrom(self)
        painter.drawPrimitive(QStyle.PE_Widget, opt)
        if self._pix.isNull():
            return
        # 图外那圈填 letterbox 同色: 不然方形图上下会各露一条近黑底, 和图像
        # 自带的灰边拼成三层, 看着像图被切了
        painter.fillRect(self.rect(), QColor(ap.PAD_VAL, ap.PAD_VAL, ap.PAD_VAL))
        scale = self._scale()
        width = self._pix.width() * scale
        height = self._pix.height() * scale
        target = QRectF(self._center.x() - width / 2.0,
                        self._center.y() - height / 2.0, width, height)
        # 缩小显示时平滑, 放大超过 1:1 就切最近邻: 双线性只会把像素拉成一团糊,
        # 最近邻至少能看清真实像素块(和标注画布放大一样)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, scale < 1.0)
        painter.drawPixmap(target, self._pix, QRectF(self._pix.rect()))
        if self._zoom > 1.001:
            self._paint_zoom_badge(painter)

    def _paint_zoom_badge(self, painter):
        text = "{}%".format(int(round(self._zoom * 100)))
        font = painter.font()
        # 界面字号是像素制的, 混用 setPointSizeF 会让角标忽大忽小
        if font.pixelSize() > 0:
            font.setPixelSize(max(9, font.pixelSize() - 1))
        else:
            font.setPointSizeF(max(7.5, font.pointSizeF() - 1.0))
        painter.setFont(font)
        metrics = painter.fontMetrics()
        room = metrics.horizontalAdvance(text) + 10
        box = QRectF(self.width() - room - 5,
                     self.height() - metrics.height() - 13,
                     room, metrics.height() + 6)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 150))
        painter.drawRoundedRect(box, 3, 3)
        painter.setPen(QColor(255, 255, 255, 230))
        painter.drawText(box, Qt.AlignCenter, text)

    # ---------- 交互 ----------
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if self._pix.isNull() or not delta:
            event.ignore()
            return
        self._apply_zoom(self._zoom * self.STEP ** (delta / 120.0),
                         event.position())
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._zoom > 1.001:
            self._drag_from = (event.position(), QPointF(self._center))
            self._update_cursor()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_from is None:
            super().mouseMoveEvent(event)
            return
        start, center = self._drag_from
        self._center = center + (event.position() - start)
        self._clamp()
        self.update()

    def mouseReleaseEvent(self, event):
        if self._drag_from is not None and event.button() == Qt.LeftButton:
            self._drag_from = None
            self._update_cursor()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.reset_view()
        event.accept()


class AugPreviewDialog(QDialog):
    def __init__(self, parent, db, ds_pairs, codes, backend, task, img_size):
        super().__init__(parent)
        self.setObjectName("AugPreviewDialog")
        self.setWindowTitle(self.tr("数据增强预览"))
        self._db = db
        self._codes = list(codes)
        self._backend = backend if backend in AUG_BOTH else "transformer"
        self._task = task
        self._size = max(160, int(img_size or 640))
        # 解析函数吃的是记录里那种逗号串, 别把 list 直接喂进去
        codes_text = ",".join(self._codes)
        self._params = (resolve_yolo_aug(codes_text) if self._backend == "cnn"
                        else resolve_aug_config(codes_text))
        self._entries = []
        self._primary = None
        self._render = self._size
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
        # 232 的对照图看细节不够, 默认就开大一点; 再大由最大化按钮接管
        self.resize(1040, 600)

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
        body.addWidget(self._card(self.tr("原图"), self._pane_orig), 1)
        arrow = QLabel("→", self)
        arrow.setProperty("class", "augArrow")
        arrow.setAlignment(Qt.AlignCenter)
        arrow.setFixedWidth(24)
        body.addWidget(arrow)
        self._pane_aug = self._pane()
        self._sample_title = QLabel("", self)
        self._sample_title.setProperty("class", "augSampleTip")
        body.addWidget(self._card(self.tr("增强后"), self._pane_aug,
                                  self._sample_title), 1)
        body.addWidget(self._params_panel())
        lay.addLayout(body, 1)

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
        zoom_hint = QLabel(self.tr("滚轮缩放 · 双击复位"), self)
        zoom_hint.setProperty("class", "augFine")
        foot.addWidget(zoom_hint)
        foot.addStretch(1)
        lay.addLayout(foot)

        # 高度交给布局算: 硬写最小值会比内容所需更矮, 缩略图行会压到卡片上
        self.setMinimumWidth(880)
        # QDialog 默认没有最大化按钮, 图要大看得清就得能拉满屏
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

    def _tool_button(self, text, slot):
        btn = QPushButton(text, self)
        btn.setProperty("class", "ghost")
        btn.clicked.connect(lambda: slot())
        return btn

    def _pane(self):
        return _ZoomPane(SIDE, self)

    def _card(self, title, pane, subtitle=None):
        card = QFrame(self)
        card.setProperty("class", "augCard")
        card.setMinimumHeight(CARD_H)
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
        panel.setMinimumHeight(CARD_H)
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
        self._render = self._render_size(primary["image"])
        boxed = ap.letterbox(primary["image"], primary["shapes"], self._render)
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
        # 换了源图就不该继承上一张的放大位置, 换采样才需要保持
        self._pane_orig.reset_view()
        self._pane_aug.reset_view()

    def _render_size(self, img):
        """
        预览用的画布边长: 取原图长边, 上限 PREVIEW_MAX.

        训练输入会被压到 img_size(通常 640), 线扫图动辄 3713 宽, 压完只剩 640,
        放大看就是一片糊 —— 预览要看清缺陷就得按原图分辨率渲染.
        """
        long_edge = max(img.shape[:2])
        return max(320, min(PREVIEW_MAX, max(self._size, long_edge)) // 2 * 2)

    def _describe(self):
        name = self._primary["name"] if self._primary else ""
        self._meta.setText(self.tr("{} · 可选 {} 张").format(
            name, len(self._entries)))
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
                                        others=others, source=self._source,
                                        ref_size=self._size)
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

    def _to_pixmap(self, img, side=None):
        rgb = np.ascontiguousarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        h, w = rgb.shape[:2]
        qimg = QImage(rgb.data, w, h, w * 3, QImage.Format_RGB888).copy()
        pix = QPixmap.fromImage(qimg)
        if side is None:
            # 主视图留着原尺寸, 放大时才不会一开始就糊
            return pix
        return pix.scaled(side, side, Qt.KeepAspectRatio,
                          Qt.SmoothTransformation)

    def _refresh(self):
        if self._base_img is None:
            return
        self._pane_orig.set_image(self._to_pixmap(
            self._paint(self._base_img, self._base_shapes)))
        for i, thumb in enumerate(self._thumbs):
            if i >= len(self._results):
                thumb.clear()
                continue
            img, boxes = self._results[i]
            # 缩略图先缩到两倍边长再画标注: 1600 的图直接画 6 遍纯属浪费
            small, small_boxes = ap.letterbox(img, boxes, THUMB * 2)
            thumb.setPixmap(self._to_pixmap(self._paint(small, small_boxes),
                                            THUMB))
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
        self._pane_aug.set_image(self._to_pixmap(self._paint(img, boxes)))

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
