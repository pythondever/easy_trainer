# -*- coding: utf-8 -*-
"""标注视图：滚轮缩放、中键平移、快捷键。"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QKeySequence, QShortcut
from PySide6.QtWidgets import QGraphicsView, QMenu

from app.annotation.box_item import AnnotationBoxItem, AnnotationPolygonItem
from app.annotation.scene import AnnotationScene


class AnnotationView(QGraphicsView):
    zoom_changed = Signal(float)
    cursor_moved = Signal(float, float)  # 图像坐标

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = AnnotationScene(self)
        self.setScene(self._scene)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setMouseTracking(True)
        self.setFrameShape(QGraphicsView.NoFrame)
        self.setBackgroundBrush(QColor("#0e0f13"))
        # 点击图像即获得焦点：保证 A/D 翻页等快捷键在点图后直接生效
        self.setFocusPolicy(Qt.ClickFocus)
        self._panning = False
        self._last_pan_pos = None
        self._space_down = False
        # 快捷键
        QShortcut(QKeySequence.ZoomIn, self, activated=self.zoom_in)
        QShortcut(QKeySequence.ZoomOut, self, activated=self.zoom_out)
        QShortcut(QKeySequence("Ctrl+0"), self, activated=self.fit_window)

    @property
    def scene_(self):
        return self._scene

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        factor = 1.18 if delta > 0 else 1 / 1.18
        self.scale(factor, factor)
        self.zoom_changed.emit(self._zoom_level())

    def _zoom_level(self):
        return self.transform().m11()

    def zoom_in(self):
        self.scale(1.18, 1.18)
        self.zoom_changed.emit(self._zoom_level())

    def zoom_out(self):
        self.scale(1 / 1.18, 1 / 1.18)
        self.zoom_changed.emit(self._zoom_level())

    def fit_window(self):
        if self._scene.image_rect is not None:
            self.fitInView(self._scene.image_rect, Qt.KeepAspectRatio)
            self.zoom_changed.emit(self._zoom_level())

    def reset_zoom(self):
        self.resetTransform()
        self.zoom_changed.emit(self._zoom_level())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self._space_down = True
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            return
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space:
            self._space_down = False
            self.setDragMode(QGraphicsView.NoDrag)
            return
        super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._last_pan_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        hit = self.scene().itemAt(scene_pos, self.transform())
        if isinstance(hit, (AnnotationBoxItem, AnnotationPolygonItem)):
            menu = QMenu(self)
            menu.addAction("删除该标注", lambda: self.scene().delete_item(hit))
            menu.exec(event.globalPos())
            event.accept()
            return
        super().contextMenuEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._last_pan_pos is not None:
            delta = event.pos() - self._last_pan_pos
            self._last_pan_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
            return
        # 坐标回显
        scene_pos = self.mapToScene(event.pos())
        if self._scene.image_rect is not None and self._scene.image_rect.contains(scene_pos):
            self.cursor_moved.emit(scene_pos.x(), scene_pos.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self._last_pan_pos = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)
