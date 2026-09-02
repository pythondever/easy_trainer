# -*- coding: utf-8 -*-
"""标注场景：负责画框/画多边形、删除、与列表同步。"""
import math
import random
from PySide6.QtCore import QRectF, QPointF, Qt, Signal
from PySide6.QtGui import (QPen, QColor, QBrush, QPolygonF, QPainterPath,
                           QPixmap, QPainter, QImage)
from PySide6.QtWidgets import (QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem,
                               QGraphicsPathItem, QGraphicsPolygonItem)
from app.annotation.box_item import AnnotationBoxItem, AnnotationPolygonItem, label_color


def _simplify_track(pts, max_pts=32):
    """轨迹点抽稀为均匀采样的多边形顶点（首尾必保），避免顶点过多。"""
    if len(pts) <= max_pts:
        return pts
    step = (len(pts) - 1) / (max_pts - 1)
    out = [pts[0]]
    i = 1
    while i < max_pts - 1:
        out.append(pts[int(round(i * step))])
        i += 1
    out.append(pts[-1])
    return out


class AnnotationScene(QGraphicsScene):
    boxes_changed = Signal()
    box_drawn = Signal()
    selection_changed = Signal(object)
    label_change_requested = Signal(object)
    fp_mode_changed = Signal(str)
    image_pixels_changed = Signal()
    draw_cancel_requested = Signal()   # Esc 退出绘制模式

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_item = None
        self.image_rect = None
        self.draw_mode = False
        self.draw_shape = "rect"
        self.current_label = "object"
        self._preview_item = None
        self._draw_start = None
        self._polygon_points = []
        self._free_track = []   # 画笔轨迹(手绘多边形采样点)
        self._last_box = None
        self.label_colors = {}
        self.image_modified = False
        self.selectionChanged.connect(self._on_selection_changed)
        # 格式刷
        self.fp_mode = None
        self.fp_track = []
        self.fp_template = None
        self.fp_preview_item = None
        self.fp_ghost_item = None
        self._fp_undo_stack = []
        self._paste_pos = None   # 复制/粘贴: 左键点击空白处记录的粘贴锚点
        self.angle_range = (-180, 180)   # 粘贴随机旋转角度范围(由标注界面输入框设置)

    def set_image(self, pixmap):
        self.clear()
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.image_item.setZValue(0)
        self.image_modified = False
        self.fp_ghost_item = None
        self._fp_undo_stack = []
        self.addItem(self.image_item)
        self.image_rect = QRectF(0, 0, pixmap.width(), pixmap.height())
        self.setSceneRect(self.image_rect.adjusted(-50, -50, 50, 50))

    def set_draw_mode(self, draw, shape=None):
        self.draw_mode = draw
        if shape is not None:
            self.draw_shape = shape
        if not draw:
            self._cancel_polygon()
        # 进入画模式时退出格式刷
        if draw and self.fp_mode is not None:
            self.set_format_painter(False)
        flag = QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        for item in self.all_items():
            item.setFlag(flag, not draw)
            item.unsetCursor()

    # ---------------- 格式刷(轨迹描边, 模板, 刷子粘贴)----------------
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
            self.fp_preview_item.setPen(QPen(QColor("#5B8CFF"), 1.5))
            self.fp_preview_item.setBrush(Qt.NoBrush)
            self.fp_preview_item.setZValue(20)
            self.addItem(self.fp_preview_item)
        path = QPainterPath()
        if self.fp_track:
            path.moveTo(self.fp_track[0][0], self.fp_track[0][1])
            for x, y in self.fp_track[1:]:
                path.lineTo(x, y)
        self.fp_preview_item.setPath(path)

    def _extract_patch(self, pts):
        """从当前图像抠取多边形区域像素:包围盒裁剪 + 多边形 mask(外部透明)。"""
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
        mask = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
        mask.fill(Qt.transparent)
        mp = QPainter(mask)
        mp.setRenderHint(QPainter.Antialiasing)
        mp.setPen(Qt.NoPen)
        mp.setBrush(QColor(255, 255, 255))
        mp.drawPolygon(QPolygonF([QPointF(px - minx, py - miny) for px, py in pts]))
        mp.end()
        p = QPainter(patch)
        p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        p.drawImage(0, 0, mask)
        p.end()
        return patch

    def _finish_fp_trace(self):
        """松开左键：轨迹闭环成功 → 抠图生成模板并进入刷子模式；否则清空重画。"""
        pts = self.fp_track
        self.fp_track = []
        self._clear_fp_items()
        if len(pts) < 6:
            return
        first, last = pts[0], pts[-1]
        if (last[0] - first[0]) ** 2 + (last[1] - first[1]) ** 2 > 225:  # 首尾 >15px 未闭环
            return
        simplified = AnnotationScene._simplify_track(pts)
        patch = self._extract_patch(simplified)
        if patch is None:
            return
        self.fp_template = {"points": simplified, "patch": patch,
                            "w": patch.width(), "h": patch.height()}
        self.fp_mode = "paint"
        self.fp_mode_changed.emit("paint")

    def _shift_template(self, pos):
        """把模板平移到以 pos 为中心，并整体夹在图像边界内（保持形状）。"""
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
            self.fp_ghost_item.setPen(QPen(QColor(91, 140, 255, 160), 1.0))
            self.fp_ghost_item.setBrush(QBrush(QColor(91, 140, 255, 36)))
            self.fp_ghost_item.setZValue(15)
            self.addItem(self.fp_ghost_item)
        else:
            self.fp_ghost_item.setPolygon(
                QPolygonF([QPointF(*p) for p in pts]))

    def copy_template_from_item(self, item):
        """
        把选中的标注项复制为格式刷模板(区域像素 + 多边形 + 标签)。
        只支持多边形; 成功返回 True。跨图保留(A/D 切换后仍可粘贴)。
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

    @staticmethod
    def _rotate_points(pts, center, angle):
        """
        多边形点绕 center 旋转 angle 度。Qt 屏幕坐标 y 向下:
        正角度=视觉顺时针, 负角度=视觉逆时针(与 QPainter.rotate 方向一致)。
        """
        rad = math.radians(angle)
        c, s = math.cos(rad), math.sin(rad)
        cx, cy = center.x(), center.y()
        out = []
        for x, y in pts:
            dx, dy = x - cx, y - cy
            out.append([cx + dx * c - dy * s, cy + dx * s + dy * c])
        return out

    def _clamp_points_in_image(self, pts):
        """把多边形整体平移回图像内(保持形状, 不旋转): 保证完全在图内。"""
        img = self.image_rect
        if img is None:
            return pts
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        dx = dy = 0.0
        if min(xs) < img.left():
            dx = img.left() - min(xs)
        if max(xs) > img.right():
            dx = img.right() - max(xs)
        if min(ys) < img.top():
            dy = img.top() - min(ys)
        if max(ys) > img.bottom():
            dy = img.bottom() - max(ys)
        if dx or dy:
            return [[x + dx, y + dy] for x, y in pts]
        return pts

    def _paste_template(self, pos):
        """
        把模板（抠图 patch + 多边形）粘贴到 pos 为中心, 随机旋转 0~180°(正负)。
        旋转后整体夹紧回图像内(保证多边形完全在图内, 像素越界部分由 QPainter clip)。
        记录粘贴前区域像素 + 标注 item 到撤销栈（Ctrl+Z 可撤销）。
        """
        t = self.fp_template
        if not t:
            return
        lo, hi = getattr(self, "angle_range", (-180, 180))
        angle = random.uniform(lo, hi)
        # 1. 平移到以 pos 为中心(已有基础夹紧)
        shifted = self._shift_template(pos)
        # 2. 绕 pos 随机旋转(正=顺时针, 负=逆时针)
        rotated = self._rotate_points(shifted, pos, angle)
        # 3. 旋转后整体夹紧回图像内(保持形状, 避免出界)
        rotated = self._clamp_points_in_image(rotated)
        xs = [p[0] for p in rotated]
        ys = [p[1] for p in rotated]
        center = QPointF((min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0)
        pw, ph = t["patch"].width(), t["patch"].height()
        radius = math.sqrt(pw * pw + ph * ph) / 2.0
        pix = self.image_item.pixmap()
        if pix is not None and t.get("patch") is not None:
            ox = max(0, int(center.x() - radius))
            oy = max(0, int(center.y() - radius))
            bw = min(int(2 * radius) + 1, pix.width() - ox)
            bh = min(int(2 * radius) + 1, pix.height() - oy)
            before = pix.copy(ox, oy, max(0, bw), max(0, bh))
            if before.isNull():
                before = None
            p = QPainter(pix)
            p.translate(center.x(), center.y())
            p.rotate(angle)
            p.drawImage(-pw / 2.0, -ph / 2.0, t["patch"])
            p.end()
            self.image_item.setPixmap(pix)
            self.image_modified = True
            self.image_pixels_changed.emit()
        else:
            before = None
            ox = oy = 0
        if self.fp_ghost_item is not None:
            self.removeItem(self.fp_ghost_item)
            self.fp_ghost_item = None
        item = self.add_polygon(rotated, t.get("label") or self.current_label)
        if item is not None:
            item.setSelected(True)
            self._fp_undo_stack.append(
                {"before": before, "ox": ox, "oy": oy, "item": item})

    def undo_last_paste(self):
        """撤销最后一次格式刷粘贴：恢复图像区域像素 + 删除标注。"""
        if not self._fp_undo_stack:
            return False
        rec = self._fp_undo_stack.pop()
        before = rec.get("before")
        pix = self.image_item.pixmap()
        if before is not None and not before.isNull() and pix is not None:
            p = QPainter(pix)
            p.drawPixmap(rec["ox"], rec["oy"], before)
            p.end()
            self.image_item.setPixmap(pix)
        item = rec.get("item")
        if item is not None and item.scene() is self:
            self.removeItem(item)
        self.image_modified = bool(self._fp_undo_stack)
        if not self.image_modified:
            self.image_pixels_changed.emit()
        self.boxes_changed.emit()
        return True

    def set_draw_shape(self, shape):
        self.draw_shape = shape
        self._cancel_polygon()

    def toggle_draw_mode(self):
        self.set_draw_mode(not self.draw_mode)
        return self.draw_mode

    def all_items(self):
        items = []
        for item in self.items():
            if isinstance(item, (AnnotationBoxItem, AnnotationPolygonItem)):
                items.append(item)
        return items

    def box_items(self):
        items = []
        for item in self.items():
            if isinstance(item, AnnotationBoxItem):
                items.append(item)
        return items

    def polygon_items(self):
        items = []
        for item in self.items():
            if isinstance(item, AnnotationPolygonItem):
                items.append(item)
        return items

    def _resolve_color(self, label):
        color = self.label_colors.get(label)
        if color is None:
            color = label_color(label)
            self.label_colors[label] = color
        return color

    def add_box(self, x1, y1, x2, y2, label):
        rect = QRectF(x1, y1, x2 - x1, y2 - y1)
        if rect.width() < 2 or rect.height() < 2:
            return None
        color = self._resolve_color(label)
        item = AnnotationBoxItem(rect.normalized(), label, color=color)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, not self.draw_mode)
        self.addItem(item)
        self._last_box = item
        self.boxes_changed.emit()
        return item

    def add_polygon(self, points, label):
        """添加多边形标注。points: [[x, y], ...]（像素坐标），至少 3 个顶点。"""
        if len(points) < 3:
            return None
        color = self._resolve_color(label)
        item = AnnotationPolygonItem(points, label, color=color)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, not self.draw_mode)
        self.addItem(item)
        self._last_box = item
        self.boxes_changed.emit()
        return item

    def boxes(self):
        """返回标注列表：矩形 {label,x1,y1,x2,y2} / 多边形 {label,points,shape_type}（像素坐标）。"""
        result = []
        for item in self.box_items():
            x1, y1, x2, y2 = item.boxes()
            result.append({"label": item.label, "x1": x1, "y1": y1, "x2": x2, "y2": y2})
        for item in self.polygon_items():
            result.append({"label": item.label, "points": item.points(), "shape_type": "polygon"})
        return result

    def load_boxes(self, boxes):
        self.clear_boxes()
        for box in boxes:
            if box.get("shape_type") == "polygon":
                self.add_polygon(box.get("points") or [], box["label"])
            else:
                self.add_box(box["x1"], box["y1"], box["x2"], box["y2"], box["label"])
        self.boxes_changed.emit()

    def clear_boxes(self):
        for item in self.all_items():
            self.removeItem(item)
        self._preview_item = None
        self._polygon_points = []

    def selected_item(self):
        items = self.selectedItems()
        for item in items:
            if isinstance(item, (AnnotationBoxItem, AnnotationPolygonItem)):
                return item
        return None

    def set_label_of_selected(self, label):
        item = self.selected_item()
        if item is not None:
            item.set_label(label)
            self.boxes_changed.emit()

    def _force_full_redraw(self, rect=None):
        """
        删除 item 后重绘受影响区域, 避免视图缓存残留。
        """
        if rect is not None and not rect.isEmpty():
            self.update(rect)
        else:
            self.update()
        for v in self.views():
            v.resetCachedContent()
            v.viewport().update()

    def _dispose_item(self, item):
        """彻底释放 item: 隐藏 + 取消缓存, 防视图缓存残留。"""
        try:
            item.hide()
            item.setCacheMode(QGraphicsItem.NoCache)
            item.setEnabled(False)
        except Exception:
            pass
        self.removeItem(item)

    def delete_selected(self):
        item = self.selected_item()
        if item is not None:
            self._cancel_polygon()
            self._clear_fp_items()
            gone = item.sceneBoundingRect()
            self._dispose_item(item)
            self._last_box = None
            self._force_full_redraw(gone)
            self.boxes_changed.emit()
            return True
        return False

    def delete_item(self, item):
        """删除指定 item（右键菜单直接传 item，不依赖选中态）。"""
        if item is None or item.scene() is not self:
            return False
        self._cancel_polygon()
        self._clear_fp_items()
        gone = item.sceneBoundingRect()
        self._dispose_item(item)
        if self._last_box is item:
            self._last_box = None
        self._force_full_redraw(gone)
        self.boxes_changed.emit()
        return True

    def set_item_label(self, item, label):
        """修改指定标注 item 的类别（矩形/多边形通用）。"""
        if item is None or item.scene() is not self:
            return
        item.set_label(label)
        self.boxes_changed.emit()

    def select_item(self, item):
        self.clearSelection()
        if item is not None:
            item.setSelected(True)

    def _on_selection_changed(self):
        self.selection_changed.emit(self.selected_item())

    def _cancel_polygon(self):
        """取消未完成的多边形(清轨迹+预览)。"""
        self._polygon_points = []
        self._free_track = []
        if self._preview_item is not None:
            self.removeItem(self._preview_item)
            self._preview_item = None

    def mousePressEvent(self, event):
        if self.fp_mode is not None and event.button() == Qt.LeftButton and self.image_rect is not None:
            pos = self._clamp_to_image(event.scenePos())
            if self.fp_mode == "trace":
                self.fp_track = [[pos.x(), pos.y()]]
                self._update_fp_track_preview()
            else:  # paint
                self._paste_template(pos)
            event.accept()
            return
        if self.draw_mode and event.button() == Qt.LeftButton and self.image_rect is not None:
            for it in self.items(event.scenePos()):
                if isinstance(it, (AnnotationBoxItem, AnnotationPolygonItem)):
                    local = it.mapFromScene(event.scenePos())
                    p = it._chip_hit_pad()
                    if it._chip_rect_local().adjusted(-p, -p, p, p).contains(local):
                        self.label_change_requested.emit(it)
                        event.accept()
                        return
            pos = self._clamp_to_image(event.scenePos())
            if self.draw_shape == "polygon":
                self._polygon_press(pos)
            else:
                self._rect_press(pos)
            event.accept()
            return
        # 普通浏览模式: 左键点击空白处(未命中标注)记录为格式刷粘贴锚点
        if (event.button() == Qt.LeftButton and self.fp_mode is None
                and not self.draw_mode and self.image_rect is not None):
            hit = None
            for it in self.items(event.scenePos()):
                if isinstance(it, (AnnotationBoxItem, AnnotationPolygonItem)):
                    hit = it
                    break
            if hit is None:
                self._paste_pos = event.scenePos()
        super().mousePressEvent(event)

    def _rect_press(self, pos):
        self._draw_start = pos
        # 矩形预览颜色 = 当前标注标签颜色(与多边形一致, 跟随用户所选标签)
        c = QColor(self._resolve_color(self.current_label))
        pen_c = QColor(c)
        pen_c.setAlpha(230)
        brush_c = QColor(c)
        brush_c.setAlpha(40)
        self._preview_item = self.addRect(
            QRectF(pos, pos),
            QPen(pen_c, 1.5),
            QBrush(brush_c),
        )
        self._preview_item.setZValue(20)

    def _polygon_trace_color(self):
        """绘制轨迹颜色 = 当前标注标签颜色（跟随用户所选标签）。"""
        return QColor(self._resolve_color(self.current_label))

    def _polygon_press(self, pos):
        """画笔模式: 按下开始采集轨迹。"""
        self._free_track = [[pos.x(), pos.y()]]
        c = self._polygon_trace_color()
        self._preview_item = QGraphicsPathItem()
        pen_c = QColor(c)
        pen_c.setAlpha(230)
        self._preview_item.setPen(QPen(pen_c, 1.5))
        brush_c = QColor(c)
        brush_c.setAlpha(40)
        self._preview_item.setBrush(QBrush(brush_c))
        self._preview_item.setZValue(20)
        self.addItem(self._preview_item)
        self._update_polygon_preview()

    def _sample_gap_sq(self, pos, last):
        """屏幕 10px 换算 scene 间距(考虑缩放), 放大时保持恒定屏幕密度。"""
        scale = 1.0
        views = self.views()
        if views:
            t = views[0].transform()
            scale = abs(t.m11()) or 1.0
        gap = max(10.0 / scale, 2.0)
        return (pos.x()-last[0])**2 + (pos.y()-last[1])**2 >= gap * gap

    @staticmethod
    def _rdp(points, epsilon):
        """Douglas-Peucker 抽稀: 保形且顶点数合理。"""
        if len(points) < 3:
            return list(points)
        p1, p2 = points[0], points[-1]
        x1, y1 = p1; x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        dmax, idx = 0.0, 0
        for i in range(1, len(points) - 1):
            px, py = points[i]
            if abs(dx) < 1e-9 and abs(dy) < 1e-9:
                d = ((px-x1)**2 + (py-y1)**2) ** 0.5
            else:
                d = abs(dy*px - dx*py + x2*y1 - y2*x1) / (dx*dx + dy*dy) ** 0.5
            if d > dmax:
                dmax, idx = d, i
        if dmax > epsilon:
            left = AnnotationScene._rdp(points[:idx+1], epsilon)
            right = AnnotationScene._rdp(points[idx:], epsilon)
            return left[:-1] + right
        return [p1, p2]

    @staticmethod
    def _simplify_track(points, min_gap=5.0, max_angle=150.0):
        """轨迹抽稀: 间隔采样 + RDP 保形, 返回多边形顶点。"""
        pts = []
        for p in points:
            if pts and (p[0]-pts[-1][0])**2 + (p[1]-pts[-1][1])**2 < min_gap**2:
                continue
            pts.append(p)
        if len(pts) < 3:
            return pts
        return AnnotationScene._rdp(pts, 0.8)

    def _preview_pen_width(self):
        """轨迹粗细自适应: 屏幕恒定 ~2.5px(scene 宽 = 2.5/scale)。"""
        scale = 1.0
        views = self.views()
        if views:
            t = views[0].transform()
            scale = abs(t.m11()) or 1.0
        return max(0.6, 2.5 / scale)

    def _finish_polygon(self):
        # 轨迹抽稀成多边形顶点(采样间隔+共线合并),生成标注
        pts = self._simplify_track(self._free_track or self._polygon_points)
        self._cancel_polygon()
        if len(pts) < 3:
            return
        item = self.add_polygon(pts, self.current_label)
        if item is not None:
            # 画完后立即可选中(绘制模式下其余标注不可选)
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            item.setSelected(True)
            self.box_drawn.emit()

    def _update_polygon_preview(self):
        # 绘制过程只做轨迹跟随(不抽稀),抽稀延后到_finish_polygon
        pts = self._free_track
        c = self._polygon_trace_color()
        pen_c = QColor(c)
        pen_c.setAlpha(230)
        if self._preview_item is None:
            self._preview_item = QGraphicsPathItem()
            self._preview_item.setPen(QPen(pen_c, self._preview_pen_width()))
            brush_c = QColor(c)
            brush_c.setAlpha(40)
            self._preview_item.setBrush(QBrush(brush_c))
            self._preview_item.setZValue(20)
            self.addItem(self._preview_item)
        else:
            self._preview_item.setPen(QPen(pen_c, self._preview_pen_width()))
        path = QPainterPath()
        if pts:
            path.moveTo(pts[0][0], pts[0][1])
            for x, y in pts[1:]:
                path.lineTo(x, y)
        self._preview_item.setPath(path)

    def mouseMoveEvent(self, event):
        if self.fp_mode is not None and self.image_rect is not None:
            pos = self._clamp_to_image(event.scenePos())
            if self.fp_mode == "trace" and self.fp_track:
                last = self.fp_track[-1]
                if self._sample_gap_sq(pos, last):
                    self.fp_track.append([pos.x(), pos.y()])
                    self._update_fp_track_preview()
                event.accept()
                return
            if self.fp_mode == "paint" and self.fp_template:
                self._update_fp_ghost(pos)
                event.accept()
                return
        if not self.draw_mode:
            super().mouseMoveEvent(event)
            return
        if self.draw_shape == "polygon" and self._free_track:
            pos = self._clamp_to_image(event.scenePos())
            # 轨迹采样抽稀
            last = self._free_track[-1]
            if self._sample_gap_sq(pos, last):
                self._free_track.append([pos.x(), pos.y()])
                self._update_polygon_preview()
            event.accept()
            return
        if self.draw_shape == "rect" and self._draw_start is not None and self._preview_item is not None:
            pos = self._clamp_to_image(event.scenePos())
            rect = QRectF(self._draw_start, pos).normalized()
            self._preview_item.setRect(rect)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.fp_mode == "trace" and event.button() == Qt.LeftButton:
            self._finish_fp_trace()
            event.accept()
            return
        if self.draw_mode and self.draw_shape == "polygon" and self._free_track:
            self._finish_polygon()
            event.accept()
            return
        if self.draw_mode and self.draw_shape == "rect" and self._draw_start is not None:
            if self._preview_item is not None:
                rect = self._preview_item.rect()
                self.removeItem(self._preview_item)
                self._preview_item = None
                if rect.width() >= 3 and rect.height() >= 3:
                    item = self.add_box(rect.left(), rect.top(), rect.right(), rect.bottom(),
                                        self.current_label)
                    if item is not None:
                        item.setSelected(True)
                        self.box_drawn.emit()
            self._draw_start = None
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        """多边形模式：双击闭合（>=3 顶点）。"""
        if self.draw_mode and self.draw_shape == "polygon" and event.button() == Qt.LeftButton:
            if len(self._polygon_points) >= 3:
                self._finish_polygon()
                event.accept()
                return
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        """绘制模式 Esc 退出; 多边形 Enter 闭合; 格式刷 Esc 退出。"""
        if self.fp_mode is not None and event.key() == Qt.Key_Escape:
            self.set_format_painter(False)
            event.accept()
            return
        if self.draw_mode and event.key() == Qt.Key_Escape:
            self._cancel_polygon()
            self.draw_cancel_requested.emit()
            event.accept()
            return
        if self.draw_mode and self.draw_shape == "polygon" and self._free_track:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                if len(self._free_track) >= 3:
                    self._finish_polygon()
                    event.accept()
                    return
        super().keyPressEvent(event)

    def _clamp_to_image(self, pos):
        if self.image_rect is None:
            return pos
        x = max(self.image_rect.left(), min(self.image_rect.right(), pos.x()))
        y = max(self.image_rect.top(), min(self.image_rect.bottom(), pos.y()))
        return QPointF(x, y)
