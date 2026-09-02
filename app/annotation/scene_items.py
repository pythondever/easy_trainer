# -*- coding: utf-8 -*-
"""首页图像列表项：卡片式缩略图，支持 hover 高亮、选中描边、底部标签 chip。"""
from PySide6.QtGui import QColor, QPen, QFontMetricsF
from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from app.annotation.box_item import label_color

# 卡片内边距 / 底部信息条高度
CARD_PAD = 4
INFO_H = 22


class SelectablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, image_path, labels=None):
        super().__init__(pixmap)
        self.image_path = image_path
        self.setData(0, image_path)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self._hover = False
        self._labels = list(labels or [])
        self._sel_color = QColor("#4f7dff")

    def set_labels(self, labels):
        self._labels = list(labels or [])
        self.update()

    def boundingRect(self):
        pm = self.pixmap()
        w = pm.width() + 2 * CARD_PAD
        h = pm.height() + 2 * CARD_PAD + INFO_H
        return QRectF(0, 0, w, h)

    def hoverEnterEvent(self, event):
        self._hover = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._hover = False
        self.update()
        super().hoverLeaveEvent(event)

    def _card_rect(self):
        pm = self.pixmap()
        w = pm.width() + 2 * CARD_PAD
        h = pm.height() + 2 * CARD_PAD + INFO_H
        return QRectF(0, 0, w, h)

    def paint(self, painter, option, widget=None):
        pm = self.pixmap()
        card = self._card_rect()
        # 卡片背景
        if self.isSelected():
            bg = QColor("#2c3a5e")
        elif self._hover:
            bg = QColor("#2b2f3b")
        else:
            bg = QColor("#23262f")
        painter.setPen(QPen(QColor("#353a48"), 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(card, 6, 6)
        # 图像
        painter.drawPixmap(CARD_PAD, CARD_PAD, pm)
        # hover/选中描边
        if self.isSelected():
            painter.setPen(QPen(self._sel_color, 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(card.adjusted(1, 1, -1, -1), 6, 6)
        elif self._hover:
            painter.setPen(QPen(self._sel_color, 1.5))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(card.adjusted(1, 1, -1, -1), 6, 6)
        # 底部信息条: 标签 chip(最多 3 个 + 溢出计数)
        self._draw_label_chips(painter)

    def _draw_label_chips(self, painter):
        if not self._labels:
            return
        pm = self.pixmap()
        y = CARD_PAD + pm.height() + 3
        chip_h = INFO_H - 8
        cx = CARD_PAD + 2
        painter.save()
        fm = QFontMetricsF(painter.font())
        visible = self._labels[:3]
        for lbl in visible:
            txt = str(lbl)
            tw = fm.horizontalAdvance(txt) + 12
            color = QColor(label_color(txt).name())
            color.setAlpha(210)
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawRoundedRect(QRectF(cx, y, tw, chip_h), 3, 3)
            painter.setPen(QColor("#ffffff"))
            painter.drawText(QRectF(cx + 2, y, tw - 4, chip_h),
                             Qt.AlignCenter, txt)
            cx += tw + 4
        if len(self._labels) > 3:
            more = "+{}".format(len(self._labels) - 3)
            tw = fm.horizontalAdvance(more) + 8
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(60, 66, 82))
            painter.drawRoundedRect(QRectF(cx, y, tw, chip_h), 3, 3)
            painter.setPen(QColor("#c3c9d6"))
            painter.drawText(QRectF(cx, y, tw, chip_h), Qt.AlignCenter, more)
        painter.restore()
