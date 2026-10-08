# -*- coding: utf-8 -*-
"""对比曲线: 自绘 QWidget, 取代 matplotlib 以对齐设计稿观感(细网格 / 最优虚线 /
悬停竖线取值). 只负责画, 数据由调用方整理成 (标签, 颜色, epochs, 取值) 四元组."""

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from app.core import theme

SERIES_COLORS = ("#ff8aa0", "#3ddc84", "#f5b84c", "#6fc2ff",
                 "#c58aff", "#52d6a8", "#ff9f6e", "#7c879c")

PAD_L, PAD_R, PAD_T, PAD_B = 48, 14, 14, 26
GRID_N = 4


def series_color(index):
    return SERIES_COLORS[index % len(SERIES_COLORS)]


class CompareChart(QWidget):
    """多条训练曲线叠在一张图上; 悬停出竖线并列出各条在该 epoch 的取值."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []          # [(标签, 颜色, epochs, values)]
        self._metric = ""
        self._lower = False       # 越小越好: 最优取最小, 纵轴不 clamp
        self._fmt = None
        self._empty = ""
        self._hover = None
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(200)
        self.setCursor(Qt.CrossCursor)

    def set_series(self, items, metric="", lower_better=False, fmt=None):
        self._items = [it for it in items if it[3]]
        self._metric = metric
        self._lower = bool(lower_better)
        self._fmt = fmt
        self._empty = ""
        self._hover = None
        self.update()

    def set_empty(self, text):
        self._items = []
        self._metric = ""
        self._empty = text or ""
        self._hover = None
        self.update()

    def has_series(self):
        return bool(self._items)

    # ---------- 坐标 ----------
    def _plot(self):
        return QRect(PAD_L, PAD_T,
                     max(1, self.width() - PAD_L - PAD_R),
                     max(1, self.height() - PAD_T - PAD_B))

    def _bounds(self):
        emax = max(len(it[3]) for it in self._items)
        vmin = vmax = None
        for _label, _c, _xs, ys in self._items:
            for v in ys:
                if vmin is None or v < vmin:
                    vmin = v
                if vmax is None or v > vmax:
                    vmax = v
        span = (vmax - vmin) or 1.0
        vmin -= span * 0.08
        vmax += span * 0.08
        # 准确率类不会是负的, 别让留白把纵轴拉进负区间
        if not self._lower and vmin < 0:
            vmin = 0.0
        if vmax == vmin:
            vmax = vmin + 1.0
        return vmin, vmax, emax

    def _x_at(self, i, emax, plot):
        if emax <= 1:
            return plot.left() + plot.width() / 2.0
        return plot.left() + plot.width() * i / (emax - 1)

    def _y_at(self, v, vmin, vmax, plot):
        return plot.bottom() - plot.height() * (v - vmin) / (vmax - vmin)

    def _index_at(self, x, emax, plot):
        if emax <= 1:
            return 0
        i = round((x - plot.left()) / plot.width() * (emax - 1))
        return max(0, min(emax - 1, int(i)))

    def _text(self, v):
        if self._fmt is not None:
            return self._fmt(v)
        return "{:.3f}".format(v)

    # ---------- 绘制 ----------
    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        if not self._items:
            if self._empty:
                p.setPen(QColor(theme.hexof("text_3")))
                p.drawText(self.rect(), Qt.AlignCenter, self._empty)
            return

        vmin, vmax, emax = self._bounds()
        plot = self._plot()
        grid = QColor(theme.hexof("border_subtle"))
        tick = QColor(theme.hexof("text_faint"))

        f_tick = QFont(self.font())
        f_tick.setPointSizeF(8)
        p.setFont(f_tick)
        metrics = QFontMetrics(f_tick)

        # 横向网格 + 纵轴刻度
        for g in range(GRID_N + 1):
            v = vmin + (vmax - vmin) * g / GRID_N
            y = self._y_at(v, vmin, vmax, plot)
            p.setPen(QPen(grid, 1))
            p.drawLine(plot.left(), y, plot.right(), y)
            p.setPen(tick)
            p.drawText(QRect(0, int(y) - 9, PAD_L - 8, 18),
                       Qt.AlignRight | Qt.AlignVCenter, self._text(v))

        # 横轴刻度落在数据点上, 标的是该点真实的 epoch
        longest = max(self._items, key=lambda it: len(it[3]))
        for g in range(GRID_N + 1):
            i = round((emax - 1) * g / GRID_N)
            x = self._x_at(i, emax, plot)
            epoch = longest[2][i] if i < len(longest[2]) else i + 1
            p.setPen(tick)
            p.drawText(QRect(int(x) - 24, self.height() - PAD_B + 4, 48, 16),
                       Qt.AlignCenter, str(epoch))

        # 全体系最优: 一条水平虚线, 便于一眼看出各条离最好还差多少
        best = None
        for _label, _c, _xs, ys in self._items:
            b = min(ys) if self._lower else max(ys)
            best = b if best is None else (min(best, b) if self._lower
                                           else max(best, b))
        if best is not None:
            by = self._y_at(best, vmin, vmax, plot)
            p.setPen(QPen(QColor(theme.hexof("accent_soft")), 1, Qt.DashLine))
            p.drawLine(plot.left(), by, plot.right(), by)
            p.setPen(QColor(theme.hexof("accent_soft")))
            p.drawText(QRect(plot.left() + 6, int(by) - 18, 160, 16),
                       Qt.AlignLeft | Qt.AlignVCenter,
                       "最佳 {}".format(self._text(best)))

        # 曲线本体 + 末端圆点
        for _label, color, _xs, ys in self._items:
            pen = QPen(QColor(color), 2)
            p.setPen(pen)
            for i in range(len(ys) - 1):
                p.drawLine(self._x_at(i, emax, plot),
                           self._y_at(ys[i], vmin, vmax, plot),
                           self._x_at(i + 1, emax, plot),
                           self._y_at(ys[i + 1], vmin, vmax, plot))
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(color))
            lx = self._x_at(len(ys) - 1, emax, plot)
            ly = self._y_at(ys[-1], vmin, vmax, plot)
            p.drawEllipse(lx - 3, ly - 3, 6, 6)

        if self._hover is not None:
            self._draw_hover(p, vmin, vmax, emax, plot)

    def _draw_hover(self, p, vmin, vmax, emax, plot):
        i = min(self._hover, emax - 1)
        x = self._x_at(i, emax, plot)
        p.setPen(QPen(QColor(theme.hexof("border_strong")), 1))
        p.drawLine(x, plot.top(), x, plot.bottom())

        rows = []
        for label, color, xs, ys in self._items:
            if i >= len(ys):
                continue
            y = self._y_at(ys[i], vmin, vmax, plot)
            p.setPen(QPen(QColor(theme.hexof("bg_panel")), 1.2))
            p.setBrush(QColor(color))
            p.drawEllipse(x - 3.4, y - 3.4, 6.8, 6.8)
            rows.append((color, label, self._text(ys[i])))
        if not rows:
            return

        head = "epoch {}".format(
            self._items[0][2][i] if i < len(self._items[0][2]) else i + 1)
        if self._metric:
            head += " · {}".format(self._metric)

        f = QFont(self.font())
        f.setPointSizeF(8.5)
        p.setFont(f)
        metrics = QFontMetrics(f)
        dot_w = 14
        gap = 8
        w = max([metrics.horizontalAdvance(head)] +
                [dot_w + metrics.horizontalAdvance(l) + gap
                 + metrics.horizontalAdvance(v) for _c, l, v in rows]) + 18
        h = 8 + metrics.height() + 4 + (metrics.height() + 3) * len(rows)
        bx = x + 12
        if bx + w > self.width() - 4:
            bx = max(4, x - 12 - w)
        by = 10
        p.setPen(QPen(QColor(theme.hexof("border")), 1))
        p.setBrush(QColor(theme.hexof("bg_sunken")))
        p.drawRoundedRect(bx, by, w, h, 7, 7)

        tx = bx + 9
        ty = by + 4 + metrics.ascent()
        p.setPen(QColor(theme.hexof("text_faint")))
        p.drawText(tx, ty, head)
        ty += metrics.height() + 3
        for color, label, value in rows:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(color))
            p.drawEllipse(tx + 1, ty - metrics.ascent() + 2, 7, 7)
            p.setPen(QColor(theme.hexof("text_2")))
            p.drawText(tx + dot_w, ty, label)
            p.drawText(tx + w - 9 - metrics.horizontalAdvance(value), ty, value)
            ty += metrics.height() + 3

    # ---------- 交互 ----------
    def mouseMoveEvent(self, event):
        if not self._items:
            return
        vmin, vmax, emax = self._bounds()
        i = self._index_at(event.position().x(), emax, self._plot())
        if i != self._hover:
            self._hover = i
            self.update()

    def leaveEvent(self, _event):
        if self._hover is not None:
            self._hover = None
            self.update()

    def sizeHint(self):
        return QSize(560, 230)
