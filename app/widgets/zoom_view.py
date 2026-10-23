# -*- coding: utf-8 -*-
"""可缩放的图片视图: 滚轮以光标为锚点缩放, 放大后拖动平移, 双击回到适应窗口.

1.0 是"整图塞进控件"而不是像素 1:1: 预览图往往比控件大得多, 按像素 1:1
打开等于一上来就看局部, 对照反而无从下手. 上限不按源像素折算——那样窗口
越大上限反而越小.
"""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtWidgets import (QFrame, QSizePolicy, QStyle, QStyleOption,
                               QStylePainter)


class ZoomView(QFrame):
    """显示一张 pixmap, 支持缩放与平移. 图由 set_image 整张换入, 不做裁剪."""

    STEP = 1.18        # 滚轮一格(120)的倍率
    ZOOM_CAP = 10.0    # 相对"适应窗口"的上限
    PAD_VAL = 114      # 图外底色, 与 letterbox 补边同色

    def __init__(self, side, parent=None, pane_class="augPane"):
        super().__init__(parent)
        self.setProperty("class", pane_class)
        self._pix = QPixmap()
        self._zoom = 1.0
        self._center = QPointF()
        self._drag_from = None      # (按下处, 按下时的中心)
        # 窗口最大化时跟着长, 固定尺寸会把多出来的空间全让给空白
        self.setMinimumSize(side, side)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._reset()

    # ---------- 给外部 ----------
    def set_image(self, pixmap, keep_view=False):
        """
        换图时保持当前视口, 方便同一处对照; 图尺寸变了才复位.
        keep_view 给跨图翻页用: 每张图尺寸都不一样, 按尺寸判断等于每次都复位.
        """
        same = (not self._pix.isNull() and not pixmap.isNull()
                and pixmap.size() == self._pix.size())
        self._pix = pixmap
        if same or keep_view:
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
        painter.fillRect(self.rect(),
                         QColor(self.PAD_VAL, self.PAD_VAL, self.PAD_VAL))
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
