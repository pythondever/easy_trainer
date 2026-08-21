# -*- coding: utf-8 -*-
"""首页图像列表项：点击高亮边框、可选中(单选/Ctrl多选/Ctrl+A全选)。"""
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem


class SelectablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, image_path):
        super().__init__(pixmap)
        self.image_path = image_path
        self.setData(0, image_path)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self._sel_pen = QPen(QColor("#5B8CFF"), 3)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setPen(self._sel_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect().adjusted(2, 2, -2, -2))
