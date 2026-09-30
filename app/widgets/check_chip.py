# -*- coding: utf-8 -*-
"""勾选条目: 圆形对勾 + 文案(可选色点).

首页的标签筛选面板是整块自绘的(网格/滚动/展开), 抽不出独立控件, 所以画法放这里,
由面板与 CheckChip 共用一份, 免得两边的对勾形状慢慢跑偏.
"""

from PySide6.QtCore import QPointF, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFontMetrics, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QCheckBox

from app.core import theme

DOT = 15            # 左侧色点直径
CHECK = 15          # 右侧勾选圆直径
GAP = 6
SIDE = 2            # 左右各留的余量
ROW_H = 26

HOVER_BG = theme.hexof("hover_chip")
CHECK_BORDER = "#464d5e"
CHECK_BORDER_HOVER = "#5a6379"


def is_dark(color):
    """深色圆点(未标注的黑块)在深底上看不见, 需要补一圈描边."""
    return QColor(color).lightness() < 40


def paint_dot(p, cx, cy, color, dim=False):
    dot = QRectF(cx - DOT / 2.0, cy - DOT / 2.0, DOT, DOT)
    fill = QColor(color)
    if dim:
        fill.setAlpha(110)
    p.setPen(Qt.NoPen)
    p.setBrush(fill)
    p.drawEllipse(dot)
    if is_dark(fill):
        p.setPen(QPen(QColor(CHECK_BORDER), 1))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(dot)


def paint_mark(p, cx, cy, color, checked, hovered):
    """勾了是实心圆 + 白勾, 没勾是空心圆; 悬停时描边提亮."""
    mark = QRectF(cx - CHECK / 2.0, cy - CHECK / 2.0, CHECK, CHECK)
    if checked:
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(color))
        p.drawEllipse(mark)
        pen = QPen(QColor("#ffffff"), 1.8)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        p.drawPolyline(QPolygonF([
            QPointF(cx - 3.4, cy), QPointF(cx - 1.0, cy + 2.5),
            QPointF(cx + 3.5, cy - 2.4)]))
        return
    p.setPen(QPen(QColor(CHECK_BORDER_HOVER if hovered else CHECK_BORDER), 1.5))
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(mark)


class CheckChip(QCheckBox):
    """一行勾选: 圆形对勾 + 文案, 勾选态不再靠 QSS 的方框表达.

    dot 留空就只画对勾(模型管理那种列表行内、没有文案的勾选框).
    """

    def __init__(self, parent=None, dot=None, check=None):
        super().__init__(parent)
        self._dot = QColor(dot) if dot else None
        # 只有显式给了 check 才固定; 否则跟着 dot 走, setDotColor 时对勾一起变
        self._check = QColor(check) if check else None
        self._hover = False
        self.setCursor(Qt.PointingHandCursor)

    def setDotColor(self, color):
        self._dot = QColor(color) if color else None
        self.updateGeometry()
        self.update()

    def _dot_color(self):
        return self._dot or theme.color("accent")

    def _mark_color(self):
        return self._check or self._dot or theme.color("accent")

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        w = 2 * SIDE + fm.horizontalAdvance(self.text()) + GAP + CHECK
        if self._dot is not None:
            w += DOT + GAP
        return QSize(w + 2, max(theme.px(ROW_H), fm.height() + 8))

    def minimumSizeHint(self):
        return self.sizeHint()

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect())
        on = self.isEnabled()
        hovered = self._hover and on
        if hovered:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(HOVER_BG))
            p.drawRoundedRect(rect.adjusted(0, 1, -1, -1), 5, 5)

        cy = rect.center().y() + 0.5
        x = rect.x() + SIDE
        if self._dot is not None:
            paint_dot(p, x + DOT / 2.0, cy,
                      self._dot_color() if on else theme.color("text_disabled"))
            x += DOT + GAP

        # 对勾排在文字前面: 一列下来圆点对得齐, 也是勾选列表的常见排法
        paint_mark(p, x + CHECK / 2.0, cy,
                   self._mark_color() if on else theme.color("text_disabled"),
                   self.isChecked(), hovered)
        x += CHECK + GAP

        fm = QFontMetrics(self.font())
        avail = max(10.0, rect.right() - SIDE - x)
        text = fm.elidedText(self.text(), Qt.ElideRight, int(avail))
        p.setFont(self.font())
        p.setPen(theme.color("text" if on else "text_3"))
        p.drawText(QRectF(x, rect.y(), avail, rect.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, text)
