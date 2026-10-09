# -*- coding: utf-8 -*-
"""可折叠的长文本块: 标题行自绘(三角 + 标题 + 单行摘要), 默认折叠.

详情面板宽度固定, 一条训练报错动辄几百字符, 摊平会把同栏下方的按钮挤出
可视区; 折叠后只占一行, 展开时正文限高内滚动, 相邻控件的位置不受影响.

高度故意不写死: 想要的块高当 sizeHint, 只留一个很小的兜底最小值。窗口开满
时排版有富余(面板底部的 stretch), 展开吃掉的是富余; 版面本来就紧张时压到
兜底值、正文在块内滚动, 否则展开一次就把对话框的最小高度顶上去, 最大化
的窗口会把下面的按钮挤出屏幕。
"""

from PySide6.QtCore import QPointF, QRect, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFontMetrics, QPainter, QPolygonF
from PySide6.QtWidgets import (QFrame, QPlainTextEdit, QSizePolicy, QWidget)

from app.core import theme
from app.widgets.message_box import summary_of

ARROW = 8               # 三角边长
GAP_ARROW = 7
PAD_X = 2
HEADER_H = 20
BODY_MIN_H = 54         # 只有一两行时也希望留出的块高
BODY_MAX_H = 128        # 上限: 再长就在块内滚动
BODY_SQUEEZE_H = 40     # 版面不够时的兜底高度
BODY_LINE_H = 17
MIN_W = 120

class CollapsibleText(QWidget):
    """折叠块: set_content(标题, 正文) 填内容, 正文为空时整块收起."""

    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._title = ""
        self._summary = ""
        self._text = ""
        self._expanded = False
        self._hover = False
        self._tint = QColor(theme.hexof("text_2"))
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMinimumWidth(MIN_W)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)
        self.setToolTip(self.tr("点击展开 / 收起完整内容"))

        self._body = QPlainTextEdit(self)
        self._body.setObjectName("foldBody")
        self._body.setReadOnly(True)
        self._body.setFrameShape(QFrame.NoFrame)
        self._body.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self._body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.hide()

        self.hide()

    # ---------- 对外 ----------

    def set_content(self, title, text, tint=None):
        """换内容; 顺手回到折叠态(换一条记录不该继承上一条的展开状态)."""
        self._title = title or ""
        self._text = text or ""
        self._summary = summary_of(self._text) if self._text else ""
        self._tint = QColor(tint) if tint else QColor(theme.hexof("text_2"))
        self._expanded = False
        self._body.setPlainText(self._text)
        self._body.hide()
        self.setVisible(bool(self._text))
        self._apply()

    def clear(self):
        self.set_content("", "")

    def is_expanded(self):
        return self._expanded

    def set_expanded(self, on):
        if not self._text:
            return
        self._expanded = bool(on)
        self._apply()
        self.toggled.emit(self._expanded)

    def toggle(self):
        self.set_expanded(not self._expanded)

    # ---------- 尺寸 ----------

    def _body_height(self):
        """想要的正文高度: 按当前宽度换行估行数, 夹在 [MIN, MAX]."""
        if not self._expanded:
            return 0
        fm = QFontMetrics(self._body.font())
        avail = max(40, self.width() - 2 * 5 - 16)   # 减内边距与纵向滚动条
        box = fm.boundingRect(QRect(0, 0, avail, 4000), Qt.TextWordWrap, self._text)
        rows = max(1, box.height() // max(1, fm.lineSpacing()))
        return int(max(BODY_MIN_H, min(BODY_MAX_H, rows * BODY_LINE_H + 14)))

    def _apply(self):
        want = HEADER_H + (self._body_height() + 2 if self._expanded else 0)
        floor = HEADER_H + (BODY_SQUEEZE_H if self._expanded else 0)
        if self.minimumHeight() != floor:
            self.setMinimumHeight(floor)
        if self.maximumHeight() != want:
            self.setMaximumHeight(want)
        self._sync_body()
        self.updateGeometry()
        self.update()

    def _sync_body(self):
        """正文跟着控件实得高度走: 被压扁时块内滚动, 不越出控件边界."""
        h = max(0, self.height() - HEADER_H - 2) if self._expanded else 0
        self._body.setGeometry(0, HEADER_H + 2, self.width(), h)
        self._body.setVisible(self._expanded and h > 10)

    def sizeHint(self):
        return QSize(MIN_W, self.maximumHeight())

    def minimumSizeHint(self):
        return QSize(MIN_W, self.minimumHeight())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync_body()

    # ---------- 交互 ----------

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() <= HEADER_H:
            self.toggle()
            event.accept()
            return
        super().mousePressEvent(event)

    # ---------- 绘制 ----------

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        if self._hover:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(theme.hexof("hover_chip")))
            p.drawRoundedRect(QRectF(0, 0, w, HEADER_H - 1), 4, 4)

        # 三角: 折叠朝右, 展开朝下
        cx = PAD_X + ARROW / 2.0
        cy = HEADER_H / 2.0
        p.setPen(Qt.NoPen)
        p.setBrush(self._tint)
        if self._expanded:
            p.drawPolygon(QPolygonF([
                QPointF(cx - ARROW / 2.0, cy - ARROW / 4.0),
                QPointF(cx + ARROW / 2.0, cy - ARROW / 4.0),
                QPointF(cx, cy + ARROW / 2.0)]))
        else:
            p.drawPolygon(QPolygonF([
                QPointF(cx - ARROW / 4.0, cy - ARROW / 2.0),
                QPointF(cx - ARROW / 4.0, cy + ARROW / 2.0),
                QPointF(cx + ARROW / 2.0, cy)]))

        fm = QFontMetrics(self.font())
        p.setFont(self.font())
        x = PAD_X + ARROW + GAP_ARROW
        room = max(10, w - x - PAD_X)
        title = fm.elidedText(self._title, Qt.ElideRight, int(room))
        p.setPen(self._tint)
        p.drawText(QRectF(x, 0, room, HEADER_H),
                   Qt.AlignVCenter | Qt.AlignLeft, title)
        x += fm.horizontalAdvance(title) + 8
        # 展开后正文就在下面, 摘要不再重复
        avail = w - x - PAD_X
        if not self._expanded and self._summary and avail > 24:
            p.setPen(QColor(theme.hexof("text_faint")))
            p.drawText(QRectF(x, 0, avail, HEADER_H), Qt.AlignVCenter | Qt.AlignLeft,
                       fm.elidedText(self._summary, Qt.ElideRight, int(avail)))
        p.end()
