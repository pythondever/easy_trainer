# -*- coding: utf-8 -*-
"""标签分布明细: 自绘滚动列表, 每类一行(色块/类名/条形/数量/占比).

取代原来的 matplotlib 位图(统计界面把 render_label_chart 的图渲染成
QPixmap 塞进 QGraphicsView): 类别多时(如 COCO 80 类)位图会把每类行高压成
几个像素, 类别名叠在一起, 数据根本没法读. 自绘列表矢量清晰,
滚动看全部, 每行都是真实数值; 悬停行高亮 + tooltip 给全名.
PDF 测试报告仍走 charts.render_label_chart(打印场景图更合适).
"""
from PySide6.QtCore import QRect, QRectF, Qt
from PySide6.QtGui import QColor, QFontMetrics, QPainter
from PySide6.QtWidgets import QToolTip, QWidget

from app.core import theme

ROW_H = 26          # 行高: 默认字号下行内留白舒适
PAD_X = 16          # 左右外边距
PAD_TOP = 12        # 上留白: 首行不顶到视区上沿
PAD_BOTTOM = 16     # 下留白: 滚到底时末行不贴视区下沿
SWATCH_W = 4        # 类别色块宽
GAP = 8             # 色块→类名 / 类名→条形 / 条形→数量 的间距
PCT_W = 54          # 占比列宽(右对齐)


class LabelBarsWidget(QWidget):
    """把 {类别: 数量} 画成明细行; 高度按行数算, 由外层 QScrollArea 滚动."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []      # [(类别, 数量, QColor)] 数量降序
        self._total = 0
        self._hover = -1
        self._empty_text = ""
        self.setMouseTracking(True)

    def set_data(self, counts, colors, empty_text=""):
        """counts: {类别: 数量}; colors: {类别: '#rrggbb'}, 缺省用主色."""
        rows = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
        self._rows = [(str(k), int(v),
                       QColor((colors or {}).get(k) or theme.hexof("accent")))
                      for k, v in rows]
        self._total = sum(v for _, v, _ in self._rows)
        self._empty_text = empty_text
        self._hover = -1
        self.setMinimumHeight(
            PAD_TOP + len(self._rows) * ROW_H + PAD_BOTTOM)
        self.update()

    def _columns(self):
        """列宽: (类名, 数量); 占比列固定, 条形区吃剩余宽度.

        类名列按数据里最长名字自适应(封顶 35% 宽), 绘制时再截断.
        """
        fm = QFontMetrics(self.font())
        name_w = min(max((fm.horizontalAdvance(n) for n, _, _ in self._rows),
                         default=0) + 12,
                     max(120, int(self.width() * 0.35)))
        val_w = max((fm.horizontalAdvance("{:,}".format(v))
                     for _, v, _ in self._rows), default=0) + 14
        return name_w, val_w

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        p.fillRect(0, 0, w, self.height(), QColor(theme.hexof("bg_panel")))
        if not self._rows:
            p.setPen(QColor(theme.hexof("text_3")))
            p.drawText(QRect(0, 0, w, self.height()),
                       Qt.AlignCenter, self._empty_text)
            return
        name_w, val_w = self._columns()
        bar_x0 = PAD_X + SWATCH_W + GAP + name_w + GAP
        bar_w = max(10, w - PAD_X - val_w - GAP - PCT_W - GAP - bar_x0)
        vmax = max(v for _, v, _ in self._rows)
        fm = QFontMetrics(self.font())
        text_c = QColor(theme.hexof("text"))
        dim_c = QColor(theme.hexof("text_3"))
        zebra_c = QColor(theme.hexof("bg_raised"))
        hover_c = QColor(theme.hexof("hover_chip"))
        for i, (name, value, color) in enumerate(self._rows):
            y = PAD_TOP + i * ROW_H
            if i == self._hover:
                p.fillRect(0, y, w, ROW_H, hover_c)
            elif i % 2:
                p.fillRect(0, y, w, ROW_H, zebra_c)
            cy = y + ROW_H // 2
            # 色块
            p.fillRect(QRectF(PAD_X, cy - 7, SWATCH_W, 14), color)
            # 类名(过长截断, 悬停 tooltip 给全名)
            shown = fm.elidedText(name, Qt.ElideRight, name_w - 4)
            p.setPen(text_c)
            p.drawText(QRect(PAD_X + SWATCH_W + GAP, y, name_w, ROW_H),
                       Qt.AlignVCenter | Qt.AlignLeft, shown)
            # 条形: 按最大值等比, 极小类也给 2px 让他们可见
            bw = bar_w * value / vmax if vmax else 0
            p.fillRect(QRectF(bar_x0, cy - 7, max(2, bw), 14), color)
            # 数量(千分位) 与 占比
            p.drawText(QRect(w - PAD_X - val_w - GAP - PCT_W, y, val_w, ROW_H),
                       Qt.AlignVCenter | Qt.AlignRight, "{:,}".format(value))
            p.setPen(dim_c)
            pct = value * 100.0 / self._total if self._total else 0.0
            p.drawText(QRect(w - PAD_X - PCT_W, y, PCT_W, ROW_H),
                       Qt.AlignVCenter | Qt.AlignRight, "{:.1f}%".format(pct))

    def _row_at(self, y):
        row = (int(y) - PAD_TOP) // ROW_H
        return row if 0 <= row < len(self._rows) else -1

    def mouseMoveEvent(self, ev):
        row = self._row_at(ev.position().y())
        if row != self._hover:
            self._hover = row
            self.update()
        if row >= 0:
            name, value, _ = self._rows[row]
            pct = value * 100.0 / self._total if self._total else 0.0
            QToolTip.showText(ev.globalPosition().toPoint(),
                              "{}: {} 个 ({:.1f}%)".format(name, value, pct))

    def leaveEvent(self, event):
        if self._hover != -1:
            self._hover = -1
            self.update()
