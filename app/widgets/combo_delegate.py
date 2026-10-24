# -*- coding: utf-8 -*-
"""
下拉弹层的富条目渲染: 图标 + 主标题 + 副标 + 推荐角标 + 选中对勾.

样式表只能给条目铺一层底色, 画不了图标和第二行小字, 所以这几个下拉的弹层改由
自绘 delegate 出图. 关闭态仍是控件内部那个只读 QLineEdit 在显示, 那里只有一行
文字, 弹层里的图标与副标不会跟过去.
"""

import os

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QLineEdit, QStyle, QStyledItemDelegate

from app.core.theme import color
from app.core.utils import project_root
from app.widgets.combo_utils import ClickToPopupFilter

# 条目的附加数据. Qt.UserRole 被 addItem(text, data) 占着, 这里从 +31 往后排
ROLE_SUB = Qt.UserRole + 31
ROLE_ICON = Qt.UserRole + 32
ROLE_BADGE = Qt.UserRole + 33

_ICON_SUBDIR = ("resources", "combo")

ROW_H_TWO_LINE = 44        # 带副标的两行条目
ROW_H_ONE_LINE = 32        # 无副标, 与普通下拉条目同高
ICON_PX = 14
PAD_LEFT = 10
GAP_ICON_TEXT = 10

_CACHE = {}


def combo_icon(name, tone, size=ICON_PX, dpr=2.0):
    """
    resources/combo 下的白色描边图标染成 tone 指定的颜色.

    图标本体一律画成白色, 用时按当前行状态染色(选中行纯白, 常态浅灰), 省掉
    每个图标准备两套文件. 找不到文件返回 None, 调用方按"没有图标"处理.
    """
    if not name:
        return None
    key = (name, tone, size, dpr)
    if key in _CACHE:
        return _CACHE[key]
    path = os.path.join(project_root(), *_ICON_SUBDIR, name + ".svg")
    icon = QIcon(path)
    if icon.isNull():
        _CACHE[key] = None
        return None
    src = icon.pixmap(QSize(int(size * dpr), int(size * dpr)))
    out = QPixmap(src.size())
    out.fill(Qt.transparent)
    painter = QPainter(out)
    painter.drawPixmap(0, 0, src)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(out.rect(), QColor(tone))
    painter.end()
    out.setDevicePixelRatio(dpr)
    _CACHE[key] = out
    return out


class ComboItemDelegate(QStyledItemDelegate):
    """下拉弹层条目: 左侧图标, 主标题, 可选副标与角标, 选中时右侧打勾."""

    def sizeHint(self, option, index):
        base = super().sizeHint(option, index)
        height = ROW_H_TWO_LINE if index.data(ROLE_SUB) else ROW_H_ONE_LINE
        return QSize(base.width() + 2 * PAD_LEFT + ICON_PX + GAP_ICON_TEXT,
                     height)

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        # 条目自带 2px 水平内缩, 与弹层 6px padding 叠成 8px, 高亮块离边框不贴脸
        rect = QRectF(option.rect).adjusted(2, 1, -2, -1)
        selected = bool(option.state & QStyle.State_Selected)
        enabled = bool(option.state & QStyle.State_Enabled)
        if selected:
            painter.setPen(Qt.NoPen)
            painter.setBrush(color("accent"))
            painter.drawRoundedRect(rect, 5, 5)
        elif option.state & QStyle.State_MouseOver:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 255, 255, 16))
            painter.drawRoundedRect(rect, 5, 5)

        title_font = QFont(option.font)
        base_px = title_font.pixelSize() if title_font.pixelSize() > 0 else 13
        sub_font = QFont(title_font)
        sub_font.setPixelSize(max(10, base_px - 2))
        painter.setFont(title_font)
        title_fm = painter.fontMetrics()
        painter.setFont(sub_font)
        sub_fm = painter.fontMetrics()

        sub = str(index.data(ROLE_SUB) or "")
        badge = str(index.data(ROLE_BADGE) or "")
        title = str(index.data(Qt.DisplayRole) or "")

        title_h = title_fm.height()
        sub_h = sub_fm.height() if sub else 0
        block_h = title_h + (sub_h + 1 if sub else 0)
        top = rect.top() + (rect.height() - block_h) / 2.0

        # 右侧从右往左让位: 先留对勾, 再留角标
        right = rect.right() - PAD_LEFT
        check_w = 16.0 if selected else 0.0
        right -= check_w
        badge_w = 0.0
        if badge:
            badge_w = sub_fm.horizontalAdvance(badge) + 12
            right -= (badge_w + 8)

        icon = combo_icon(index.data(ROLE_ICON),
                          "#ffffff" if selected else "#a8b0c0")
        if icon is not None:
            icon_top = top + (title_h - ICON_PX) / 2.0
            painter.drawPixmap(QRectF(rect.left() + PAD_LEFT, icon_top,
                                      ICON_PX, ICON_PX), icon, QRectF(icon.rect()))
            text_left = rect.left() + PAD_LEFT + ICON_PX + GAP_ICON_TEXT
        else:
            text_left = rect.left() + PAD_LEFT

        painter.setFont(title_font)
        title_color = QColor("#ffffff") if selected else (
            color("text") if enabled else color("text_disabled"))
        painter.setPen(title_color)
        title_text = title_fm.elidedText(title, Qt.ElideRight,
                                         max(10.0, right - text_left))
        painter.drawText(QRectF(text_left, top, right - text_left, title_h),
                         Qt.AlignLeft | Qt.AlignVCenter, title_text)

        if sub:
            painter.setFont(sub_font)
            sub_color = (QColor(255, 255, 255, 204) if selected
                         else (color("text_3") if enabled
                               else color("text_faint")))
            painter.setPen(sub_color)
            sub_text = sub_fm.elidedText(sub, Qt.ElideRight,
                                         max(10.0, right - text_left))
            painter.drawText(
                QRectF(text_left, top + title_h + 1, right - text_left, sub_h),
                Qt.AlignLeft | Qt.AlignVCenter, sub_text)

        if badge:
            self._paint_badge(painter, rect, right + 8, block_h, top,
                              badge_w, sub_font, badge, selected)

        if selected:
            self._paint_check(painter, rect, check_w, title_h, top)

        painter.restore()

    @staticmethod
    def _paint_badge(painter, rect, left, block_h, top, width, font, text,
                     selected):
        painter.setFont(font)
        fm = painter.fontMetrics()
        height = min(block_h, fm.height() + 4)
        box = QRectF(left, top + (block_h - height) / 2.0, width, height)
        if selected:
            painter.setPen(QColor(255, 255, 255, 90))
            painter.setBrush(QColor(255, 255, 255, 46))
        else:
            painter.setPen(QColor(147, 174, 240, 110))
            painter.setBrush(QColor(90, 122, 224, 40))
        painter.drawRoundedRect(box, 3, 3)
        painter.setPen(QColor("#ffffff") if selected else color("accent_text"))
        painter.drawText(box, Qt.AlignCenter, text)

    @staticmethod
    def _paint_check(painter, rect, check_w, title_h, top):
        """对勾画在主标题那条线的垂直中点上, 与左侧图标同一基准."""
        cx = rect.right() - PAD_LEFT - check_w / 2.0
        cy = top + title_h / 2.0
        pen = painter.pen()
        pen.setColor(QColor("#ffffff"))
        pen.setWidthF(1.6)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(cx - 4.2, cy, cx - 1.2, cy + 3.0)
        painter.drawLine(cx - 1.2, cy + 3.0, cx + 4.4, cy - 3.4)


def decorate_combo(combo, filters, parent=None):
    """
    把下拉装扮成"左对齐 + 富条目弹层", 并保留点击框内任意位置展开.

    与 combo_utils.style_combo 的差别是文字靠左: 弹层里图标占了左边一列, 关闭态
    再居中会与弹层的对齐轴错开; 同一排的输入框也都是左对齐的.
    """
    combo.setEditable(True)
    combo.setFocusPolicy(Qt.StrongFocus)
    line_edit = combo.lineEdit()
    line_edit.setReadOnly(True)
    line_edit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    # 内部那层 lineEdit 自带 10px 内边距和边框, 不抹掉的话文字会比旁边的输入框
    # 多缩进一截, 还会和下拉框自己的边框叠成双线
    line_edit.setObjectName("richComboLineEdit")
    view = combo.view()
    view.setMouseTracking(True)
    view.setItemDelegate(ComboItemDelegate(view))
    combo.setMaxVisibleItems(9)
    click_filter = ClickToPopupFilter(combo, parent)
    combo.installEventFilter(click_filter)
    line_edit.installEventFilter(click_filter)
    filters.append(click_filter)
    return combo
