# -*- coding: utf-8 -*-
"""
标注场景-格式刷 mixin: 轨迹描边抠模板, 再拿模板当刷子贴.
宿主(AnnotationScene)提供 image_item/image_rect/fp_* 状态与 addItem/removeItem 能力.
"""

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import (QPen, QColor, QBrush, QPolygonF, QPainterPath,
                           QPainter, QImage)
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsPolygonItem

from app.annotation.box_item import AnnotationBoxItem, AnnotationPolygonItem
from app.annotation.scene_geometry import resample_track
from app.core import theme


class FormatPainterMixin:
    def set_format_painter(self, on):
        if on and self.fp_mode is None:
            self.fp_mode = "trace"
            self.fp_track = []
            self.fp_template = None
            self.fp_mode_changed.emit("trace")
        elif not on and self.fp_mode is not None:
            self.fp_mode = None
            self.fp_track = []
            self.fp_template = None
            self._clear_fp_items()
            self.fp_mode_changed.emit("")

    def _clear_fp_items(self):
        if self.fp_preview_item is not None:
            self.removeItem(self.fp_preview_item)
            self.fp_preview_item = None
        if self.fp_ghost_item is not None:
            self.removeItem(self.fp_ghost_item)
            self.fp_ghost_item = None

    def _update_fp_track_preview(self):
        if self.fp_preview_item is None:
            self.fp_preview_item = QGraphicsPathItem()
            self.fp_preview_item.setPen(QPen(theme.color("accent"), 1.5))
            self.fp_preview_item.setBrush(Qt.NoBrush)
            self.fp_preview_item.setZValue(20)
            self.addItem(self.fp_preview_item)
        path = QPainterPath()
        if self.fp_track:
            path.moveTo(self.fp_track[0][0], self.fp_track[0][1])
            for x, y in self.fp_track[1:]:
                path.lineTo(x, y)
        self.fp_preview_item.setPath(path)

    @staticmethod
    def mask_polygon(patch, pts):
        """
        按多边形把 patch 外部擦成透明(pts 为 patch 局部坐标), 就地修改.
        从外部导入的 png 可能已经被压平成不透明白底, 不重裁一次贴上去就是整块方形.
        """
        w, h = patch.width(), patch.height()
        mask = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
        mask.fill(Qt.transparent)
        mp = QPainter(mask)
        mp.setRenderHint(QPainter.Antialiasing)
        mp.setPen(Qt.NoPen)
        mp.setBrush(QColor(255, 255, 255))
        mp.drawPolygon(QPolygonF([QPointF(px, py) for px, py in pts]))
        mp.end()
        p = QPainter(patch)
        p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        p.drawImage(0, 0, mask)
        p.end()

    def _extract_patch(self, pts):
        """从当前图像抠取多边形区域像素:包围盒裁剪 + 多边形 mask(外部透明)."""
        pix = self.image_item.pixmap()
        if pix is None:
            return None
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        minx, maxx = int(min(xs)), int(max(xs))
        miny, maxy = int(min(ys)), int(max(ys))
        w, h = maxx - minx, maxy - miny
        if w < 1 or h < 1:
            return None
        img = pix.toImage().convertToFormat(QImage.Format_ARGB32_Premultiplied)
        patch = img.copy(minx, miny, w, h)
        self.mask_polygon(patch, [(px - minx, py - miny) for px, py in pts])
        return patch

    def _finish_fp_trace(self):
        """松开左键: 轨迹闭环成功就抠图生成模板并进入刷子模式; 否则清空重画."""
        pts = self.fp_track
        self.fp_track = []
        self._clear_fp_items()
        if len(pts) < 6:
            return
        first, last = pts[0], pts[-1]
        if (last[0] - first[0]) ** 2 + (last[1] - first[1]) ** 2 > 225:  # 首尾 >15px 未闭环
            return
        simplified = resample_track(pts)
        patch = self._extract_patch(simplified)
        if patch is None:
            return
        self.fp_template = {"points": simplified, "patch": patch,
                            "w": patch.width(), "h": patch.height()}
        self.fp_mode = "paint"
        self.fp_mode_changed.emit("paint")

    def _shift_template(self, pos):
        """把模板平移到以 pos 为中心, 并整体夹在图像边界内(保持形状)."""
        pts = self.fp_template["points"]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        dx = pos.x() - (min(xs) + max(xs)) / 2
        dy = pos.y() - (min(ys) + max(ys)) / 2
        shifted = [[p[0] + dx, p[1] + dy] for p in pts]
        img = self.image_rect
        if img is None:
            return shifted
        sx = [p[0] for p in shifted]
        sy = [p[1] for p in shifted]
        ox = oy = 0.0
        if min(sx) < img.left():
            ox = img.left() - min(sx)
        if max(sx) > img.right():
            ox = img.right() - max(sx)
        if min(sy) < img.top():
            oy = img.top() - min(sy)
        if max(sy) > img.bottom():
            oy = img.bottom() - max(sy)
        return [[p[0] + ox, p[1] + oy] for p in shifted]

    def _update_fp_ghost(self, pos):
        pts = self._shift_template(pos)
        if self.fp_ghost_item is None:
            self.fp_ghost_item = QGraphicsPolygonItem(
                QPolygonF([QPointF(*p) for p in pts]))
            self.fp_ghost_item.setPen(QPen(theme.alpha("accent", 160), 1.0))
            self.fp_ghost_item.setBrush(QBrush(theme.alpha("accent", 36)))
            self.fp_ghost_item.setZValue(15)
            self.addItem(self.fp_ghost_item)
        else:
            self.fp_ghost_item.setPolygon(
                QPolygonF([QPointF(*p) for p in pts]))

    def copy_template_from_item(self, item):
        """
        把选中的标注项复制为格式刷模板(区域像素 + 多边形 + 标签).
        只支持多边形; 成功返回 True. 跨图保留(A/D 切换后仍可粘贴).
        """
        if isinstance(item, AnnotationPolygonItem):
            pts = [[p.x(), p.y()] for p in item.mapToScene(item.polygon())]
        elif isinstance(item, AnnotationBoxItem):
            r = item.mapToScene(item.rect()).boundingRect()
            pts = [[r.left(), r.top()], [r.right(), r.top()],
                   [r.right(), r.bottom()], [r.left(), r.bottom()]]
        else:
            return False
        pts = [[round(float(x), 2), round(float(y), 2)] for x, y in pts]
        patch = self._extract_patch(pts)
        if patch is None:
            return False
        self.fp_template = {"points": pts, "patch": patch,
                            "w": patch.width(), "h": patch.height(),
                            "label": getattr(item, "label", self.current_label)}
        return True
