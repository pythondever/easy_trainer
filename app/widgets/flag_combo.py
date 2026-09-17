# -*- coding: utf-8 -*-
"""
语言下拉: 国旗与语言名贴在一起, 两者作为一组绘制.

QComboBox 默认"图标钉在左边, 文本在剩下的区域里居中", 中间会空出一大块.
而且两个状态若用两套规则(收起态居中 / 弹层靠左), 展开的一瞬间旗会横向跳一下,
看着就像"弹层没居中". 所以这里统一: 整组都从控件左缘 CONTENT_LEFT 处起排,
切语言、展开弹层, 旗都不动.
"""

from PySide6.QtCore import QEvent, QObject, QRect, Qt
from PySide6.QtGui import QFontMetrics, QIcon, QPalette
from PySide6.QtWidgets import (QStyle, QStyledItemDelegate, QStyleOptionComboBox,
                               QStylePainter)

ICON_GAP = 6        # 国旗与语言名的间距. 默认两者隔了十几到二十几像素
CONTENT_LEFT = 12   # 旗左缘距控件左缘, 收起态与弹层共用

# 弹层的列表视口比弹层窗口左右各内缩这么多(实测 134 窗口 / 124 视口),
# 所以项里再退掉它, 旗落在同一个屏幕位置.
POPUP_INSET = 5
ITEM_LEFT_PAD = CONTENT_LEFT - POPUP_INSET


def _draw_icon_text(painter, clip_rect, x, icon, text, icon_size, color, gap):
    """把"图标 + 间距 + 文字"从 x 处起画, 超出 clip_rect 就裁掉."""
    painter.setClipRect(clip_rect)      # 文案长于可用区时裁掉, 别压到箭头上
    fm = QFontMetrics(painter.font())
    text_w = fm.horizontalAdvance(text)
    icon_w = 0 if icon.isNull() else icon_size.width()
    head = icon_w + gap if icon_w else 0
    cy = clip_rect.center().y()
    if icon_w:
        icon.paint(painter, QRect(x, cy - icon_size.height() // 2,
                                  icon_w, icon_size.height()))
    painter.setPen(color)
    painter.drawText(QRect(x + head, clip_rect.y(), text_w, clip_rect.height()),
                     Qt.AlignVCenter | Qt.AlignLeft, text)


class _CollapsedPainter(QObject):
    """收起态: 自己画图标和文字, 背景/边框/箭头仍交给样式, 免得 QSS 失效.

    拦掉整个 Paint 事件而不是改 currentText - 后者是 model 的数据, 改不了.
    """

    def __init__(self, combo, gap):
        super().__init__(combo)
        self._combo = combo
        self._gap = gap

    def eventFilter(self, obj, event):
        if event.type() != QEvent.Paint:
            return False
        self._paint()
        return True

    def _paint(self):
        combo = self._combo
        opt = QStyleOptionComboBox()
        combo.initStyleOption(opt)
        # 清掉再画, 不然样式会把图标和文字按它自己的位置各画一份
        opt.currentText = ""
        opt.currentIcon = QIcon()
        painter = QStylePainter(combo)
        painter.drawComplexControl(QStyle.CC_ComboBox, opt)
        index = combo.currentIndex()
        if index >= 0:
            area = combo.style().subControlRect(
                QStyle.CC_ComboBox, opt, QStyle.SC_ComboBoxEditField, combo)
            _draw_icon_text(painter, area, CONTENT_LEFT, combo.itemIcon(index),
                            combo.itemText(index), combo.iconSize(),
                            opt.palette.buttonText().color(), self._gap)
        painter.end()


class _ItemDelegate(QStyledItemDelegate):
    """列表项: 同上, 样式只负责背景与选中态."""

    def __init__(self, combo, gap):
        super().__init__(combo.view())
        self._combo = combo
        self._gap = gap

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.text = ""
        option.icon = QIcon()

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        selected = bool(option.state & QStyle.State_Selected)
        color = option.palette.color(
            QPalette.HighlightedText if selected else QPalette.Text)
        painter.save()
        painter.setFont(option.font)
        _draw_icon_text(painter, option.rect, option.rect.x() + ITEM_LEFT_PAD,
                        index.data(Qt.DecorationRole),
                        index.data(Qt.DisplayRole) or "", self._combo.iconSize(),
                        color, self._gap)
        painter.restore()


def install_flag_combo(combo, gap=ICON_GAP):
    """就地改造, 重复调用无副作用."""
    if combo.property("flagCombo"):
        return combo
    combo.setProperty("flagCombo", True)
    combo.setItemDelegate(_ItemDelegate(combo, gap))
    combo.installEventFilter(_CollapsedPainter(combo, gap))
    return combo
