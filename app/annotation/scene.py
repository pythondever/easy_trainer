# -*- coding: utf-8 -*-
"""标注场景: 负责画框/画多边形, 删除, 与列表同步."""
import numpy as np
from PySide6.QtCore import QRectF, QPointF, Qt, Signal
from PySide6.QtGui import (QPen, QColor, QBrush, QPainterPath,
                           QPainter, QImage, QPixmap)
from PySide6.QtWidgets import (QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem,
                               QGraphicsPathItem)
from app.annotation.box_item import (AnnotationBoxItem, AnnotationPolygonItem,
                                     label_color)
from app.annotation.image_buf import bgra_view
from app.annotation.paste_regions import PasteRegionItem
from app.annotation.scene_brightness import BrightnessMixin
from app.annotation.scene_regions import PasteRegionMixin
from app.annotation.scene_fp import FormatPainterMixin
from app.annotation.scene_geometry import simplify_track
from app.annotation.scene_stamp import StampMixin
from app.core.label_utils import is_text_label

# 文本框(OCR)固定配色: 走标签哈希色会和用户自己的类别撞色, 一眼分不出哪个是文本框
TEXT_COLOR = "#2ec4b6"


class AnnotationScene(FormatPainterMixin, StampMixin,
                      BrightnessMixin, PasteRegionMixin,
                      QGraphicsScene):
    # 首尾距离小于该值(图像像素)认为轨迹已经圈回来, 与 StampTool Theme.CloseTolerance 一致
    CLOSE_TOLERANCE = 15.0

    boxes_changed = Signal()
    # 带 item: 文本标注画完要拿到刚建的那个框, 才能把录的字写回去
    box_drawn = Signal(object)
    # 双击已画好的文本框改文字(录错了不必删了重画)
    box_edit_requested = Signal(object)
    selection_changed = Signal(object)
    label_change_requested = Signal(object)
    fp_mode_changed = Signal(str)
    image_pixels_changed = Signal()
    draw_cancel_requested = Signal()   # Esc 退出绘制模式
    image_changed = Signal()           # 换了图(自动粘贴据此重新倒计时)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 图像
        self.image_item = None
        self.image_rect = None
        self.image_modified = False
        # 绘制中间态
        self.draw_mode = False
        self.draw_shape = "rect"
        self.current_label = "object"
        self._draw_start = None
        self._free_track = []   # 画笔轨迹(手绘多边形采样点)
        self._last_box = None
        self._preview_item = None
        self._preview_close_item = None   # 轨迹首尾靠拢时的闭合提示虚线
        # 格式刷
        self.fp_mode = None
        self.fp_track = []
        self.fp_template = None
        self.fp_preview_item = None
        self.fp_ghost_item = None
        self._fp_undo_stack = []
        # 模板粘贴
        self._paste_pos = None           # 复制/粘贴: 左键点击空白处记录的粘贴锚点
        self._pending_pastes = []        # 浮动粘贴: 图案还没写进图像像素的多边形
        # 浮动粘贴的手柄拖动: {"kind", "item", ...}. 手柄/图标是浮动项自绘的,
        # Qt 的 items() 只在"点在轮廓多边形上"时才认得它, 所以命中与拖动状态都放场景里
        self._stamp_drag = None
        self._hover_cursor = None        # 悬停缩放手柄时的光标(见 _stamp_hover)
        # 剪切板选中后的落点预览: 跟鼠标走的多边形虚线, 角度此刻定死, 预览即落点
        self._stamp_ghost = None
        self._stamp_angle = None
        self.angle_range = (-180, 180)   # 粘贴随机旋转角度范围(由标注界面输入框设置)
        self.blend_strength = 0.7        # 粘贴融合力度 0~1(由标注界面输入框设置)
        # 亮度编辑: 拖动中只画预览层, 松手才写进图像像素
        self._bright_cache = {}          # 多边形对应亮度基准, 切回同一个框再调时不叠加
        self._bright_overlay = None      # 亮度预览层: 显示还没落盘的调亮结果
        self._bright_buf = None          # 重算亮度时的临时缓冲, 见 _bright_scratch
        # 外观
        self.label_colors = {}
        # "显示标注"开关状态(由标注界面同步): 只影响粘贴出来的框, 手绘的照常显示
        self.show_annotations = True
        # 粘贴区域模板: 不是标注, 只圈定"缺陷可以贴在哪里"(见 paste_regions 模块)
        self.template_mode = False
        self._region_points = []      # 权威数据: 换图/清空标注都不该丢
        self.paste_regions = []       # 对应 item, 一律由 _region_points 重建
        self._region_drag = None      # 正在拖的顶点 (item, 下标): 拖完才回写
        self.auto_marks = []          # 自动粘贴留下的虚线标记框(每贴一次一个)
        self.selectionChanged.connect(self._on_selection_changed)

    def set_image(self, pixmap):
        self.commit_brightness()   # 旧图没落盘的亮度先写进旧像素, clear 之后就找不回它了
        self.clear()
        self._bright_overlay = None     # clear 已把预览层一并删掉, 引用要跟着作废
        self._reset_draw_state()
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.image_item.setZValue(0)
        self.image_modified = False
        self.fp_ghost_item = None
        self._fp_undo_stack = []
        self._pending_pastes = []
        self._stamp_ghost = None
        self._stamp_angle = None
        self.drop_brightness(commit=False)
        self.addItem(self.image_item)
        self.image_rect = QRectF(0, 0, pixmap.width(), pixmap.height())
        self.setSceneRect(self.image_rect.adjusted(-50, -50, 50, 50))
        # clear() 把区域 item 一并删掉了(它们不归 all_items 管), 这里按存下的点重建:
        # 一套区域复用一个数据集, 换图不该丢
        self._rebuild_paste_region_items()
        # 标记框不能跨图留: 上一张的像素已经落盘, 那个"可撤的一次"不再成立
        self.auto_marks = []
        self.image_changed.emit()

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
        # 区域不在 all_items 里, 得单独同步(画模式下左键要留给"拉多边形")
        self.refresh_paste_region_selectability()

    def undo_last_paste(self):
        """撤销最近一次粘贴/填充: 浮动层直接丢掉(像素没动过), 已落地的恢复像素 + 删标注."""
        self.drop_brightness()
        while self._pending_pastes:
            item = self._pending_pastes.pop()
            if item.scene() is not self:
                continue
            gone = item.sceneBoundingRect()
            self._dispose_item(item)
            if self._last_box is item:
                self._last_box = None
            self._force_full_redraw(gone)
            self.boxes_changed.emit()
            return True
        if not self._fp_undo_stack:
            return False
        rec = self._fp_undo_stack.pop()
        # 若这次粘贴留了标记框, 一起摘掉: 否则框还在、记录已没了, 点它会把
        # 过期快照再糊一次到图上
        for mk in list(self.auto_marks):
            if mk.record is rec:
                self.auto_marks.remove(mk)
                self.removeItem(mk)
        self._restore_paste_record(rec)
        self.image_modified = bool(self._fp_undo_stack)
        self.boxes_changed.emit()
        return True

    def _restore_paste_record(self, rec):
        """还原一条粘贴记录(恢复像素 + 删掉那次贴出来的标注), 返回是否动过像素."""
        before = rec.get("before")
        pix = self.image_item.pixmap() if self.image_item is not None else None
        restored = False
        if before is not None and not before.isNull() and pix is not None:
            p = QPainter(pix)
            p.drawPixmap(rec["ox"], rec["oy"], before)
            p.end()
            self.image_item.setPixmap(pix)
            restored = True
        item = rec.get("item")
        gone = None
        if item is not None and item.scene() is self:
            # 光 removeItem 不够: 视图(SmartViewportUpdate)可能保留旧轮廓, 表现为
            # "图案撤销了但多边形还在", 与 delete_item 走同一套释放 + 整屏重绘
            gone = item.sceneBoundingRect()
            self._dispose_item(item)
            if self._last_box is item:
                self._last_box = None
        if restored or gone is not None:
            self._force_full_redraw(gone)
        # 每次真的改了像素都要通知(含撤销), 上层据此刷新缓存并写回磁盘
        if restored:
            self.image_pixels_changed.emit()
        return restored

    def set_annotations_visible(self, show):
        """
        "显示标注"开关. 浮动粘贴(图案还没进像素)只藏轮廓留图案,
        整个 item 一起藏的话, 粘上去还没保存的效果就看不见了.
        """
        self.show_annotations = bool(show)
        for item in self.all_items():
            item.set_outline_visible(show)

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
        if is_text_label(label):
            # 必须给 QColor: 这个返回值一路喂给 QPen/QBrush, 给字符串会炸在里面
            return QColor(TEXT_COLOR)
        color = self.label_colors.get(label)
        if color is None:
            color = label_color(label)
            self.label_colors[label] = color
        return color

    def add_box(self, x1, y1, x2, y2, label, text=""):
        rect = QRectF(x1, y1, x2 - x1, y2 - y1)
        if rect.width() < 2 or rect.height() < 2:
            return None
        color = self._resolve_color(label)
        item = AnnotationBoxItem(rect.normalized(), label, color=color,
                                 text=text)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, not self.draw_mode)
        self.addItem(item)
        self._last_box = item
        self.boxes_changed.emit()
        return item

    def add_polygon(self, points, label, text=""):
        """添加多边形标注. points: [[x, y], ...](像素坐标), 至少 3 个顶点."""
        if len(points) < 3:
            return None
        color = self._resolve_color(label)
        item = AnnotationPolygonItem(points, label, color=color, text=text)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, not self.draw_mode)
        self.addItem(item)
        self._last_box = item
        self.boxes_changed.emit()
        return item

    # ---------------- 自动粘贴(阶段2) ----------------
    def boxes(self):
        """返回标注列表: 矩形 {label,x1,y1,x2,y2,text} / 多边形
        {label,points,shape_type,text}(像素坐标); 非文本标注的 text 为空串."""
        result = []
        for item in self.box_items():
            x1, y1, x2, y2 = item.boxes()
            result.append({"label": item.label, "x1": x1, "y1": y1,
                           "x2": x2, "y2": y2, "text": item.text})
        for item in self.polygon_items():
            result.append({"label": item.label, "points": item.points(),
                           "shape_type": "polygon", "text": item.text})
        return result

    def load_boxes(self, boxes):
        self.clear_boxes()
        for box in boxes:
            if box.get("shape_type") == "polygon":
                self.add_polygon(box.get("points") or [], box["label"],
                                 box.get("text", ""))
            else:
                self.add_box(box["x1"], box["y1"], box["x2"], box["y2"],
                             box["label"], box.get("text", ""))
        self.boxes_changed.emit()

    def _reset_draw_state(self):
        """
        丢弃绘制中间态. 切换图片/清空标注时 item 已被 scene 销毁,
        这些 Python 引用若不一起清掉, 后续事件会打到已删除的 C++ 对象上.
        """
        self._preview_item = None
        self._preview_close_item = None
        self._draw_start = None
        self._free_track = []
        self._last_box = None

    def clear_boxes(self):
        for item in self.all_items():
            self.removeItem(item)
        self._pending_pastes = []
        self.drop_brightness()
        self._reset_draw_state()

    def selected_item(self):
        items = self.selectedItems()
        for item in items:
            if isinstance(item, (AnnotationBoxItem, AnnotationPolygonItem)):
                return item
        return None

    def _force_full_redraw(self, rect=None):
        """
        删除 item 后重绘受影响区域, 避免视图缓存残留.
        """
        if rect is not None and not rect.isEmpty():
            self.update(rect)
        else:
            self.update()
        for v in self.views():
            v.resetCachedContent()
            v.viewport().update()

    def _dispose_item(self, item):
        """彻底释放 item: 隐藏 + 取消缓存, 防视图缓存残留."""
        if self._bright_cache.get(item, {}).get("dirty"):
            self.commit_brightness()    # 框删了但像素上的调亮要留下
        self._bright_cache.pop(item, None)
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
        # 标注优先(与左键命中的优先级一致): 标注也在选中态时, DEL 该删标注,
        # 不能把底下那个区域删掉
        for it in list(self.selectedItems()):
            if isinstance(it, PasteRegionItem):
                self.remove_paste_region(it)
                return True
        return False

    def delete_item(self, item):
        """删除指定 item(右键菜单直接传 item, 不依赖选中态)."""
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
        """修改指定标注 item 的类别(矩形/多边形通用)."""
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
        """取消未完成的多边形(清轨迹+预览)."""
        self._free_track = []
        for attr in ("_preview_item", "_preview_close_item"):
            it = getattr(self, attr)
            if it is not None:
                self.removeItem(it)
                setattr(self, attr, None)

    def mousePressEvent(self, event):
        # 浮动粘贴的手柄优先级最高(缩放手柄 > 旋转图标 > 图体 > 标注/区域 > 空白):
        # 必须赶在下面"清选中态/记粘贴锚点"之前判, 而且只能在这里判 ——
        # 手柄/图标由浮动项自绘, Qt 的 items() 只在"点在轮廓上"时才认得父项
        if (event.button() == Qt.LeftButton and not self.draw_mode
                and self.fp_mode is None and not self.template_mode
                and self._stamp_press(event)):
            event.accept()
            return
        # 区域不参与标注那套逻辑, 所以最先单独判: 点在区域上=选中它(再按 Delete 删),
        # 不能落到下面"点空白处记粘贴锚点"那条分支去
        if (event.button() == Qt.LeftButton and not self.draw_mode
                and self.fp_mode is None and not self.template_mode):
            # 标注压在上面时优先给标注(区域是大片范围, 不该抢标注的点击)
            on_annot = any(isinstance(it, (AnnotationBoxItem,
                                          AnnotationPolygonItem))
                           for it in self.items(event.scenePos()))
            hit_region = (None if on_annot
                          else self.paste_region_at(event.scenePos()))
            # 手柄只在选中态存在, 所以顶点命中必须赶在清选中态之前判
            handle = (None if hit_region is None else hit_region.handle_at(
                hit_region.mapFromScene(event.scenePos())))
            # 清掉其它区域的选中态: 放在早返回之后的话, 点标注时
            # 区域的高亮会一直留着(而且接着按 DEL 就容易删错)
            for r in self.paste_regions:
                if r.isSelected() and r is not hit_region:
                    r.setSelected(False)
            if hit_region is not None:
                self.clearSelection()
                hit_region.setSelected(True)
                if handle is not None:
                    # 拖顶点: 用 item 上那套(与标注同一个 mixin), 拖动期间不重建 item
                    self._region_drag = (hit_region, handle)
                event.accept()
                return
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
                    # 未选中的浮动粘贴不画 chip(见 chip_visible), 这里也不能认它:
                    # 认了就是"看不见却点得中、还弹改标签菜单"
                    if not it.chip_visible():
                        continue
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
        """绘制轨迹颜色 = 当前标注标签颜色(跟随用户所选标签)."""
        return QColor(self._resolve_color(self.current_label))

    def _polygon_press(self, pos):
        self._free_track = [[pos.x(), pos.y()]]
        self._ensure_polygon_preview()
        self._update_polygon_preview()

    def _ensure_polygon_preview(self):
        """
        轨迹实线与闭合提示虚线是两个 item: QPainterPath 共用一支 QPen,
        同一条路径上画不出实线+虚线两种线型.
        """
        if self._preview_item is None:
            self._preview_item = QGraphicsPathItem()
            self._preview_item.setBrush(QBrush(Qt.NoBrush))
            self._preview_item.setZValue(20)
            self.addItem(self._preview_item)
        if self._preview_close_item is None:
            self._preview_close_item = QGraphicsPathItem()
            self._preview_close_item.setBrush(QBrush(Qt.NoBrush))
            self._preview_close_item.setZValue(20)
            self._preview_close_item.setVisible(False)
            self.addItem(self._preview_close_item)

    def _sample_gap_sq(self, pos, last):
        """屏幕 10px 换算 scene 间距(考虑缩放), 放大时保持恒定屏幕密度."""
        scale = 1.0
        views = self.views()
        if views:
            t = views[0].transform()
            scale = abs(t.m11()) or 1.0
        gap = max(10.0 / scale, 2.0)
        return (pos.x()-last[0])**2 + (pos.y()-last[1])**2 >= gap * gap

    def _preview_pen_width(self):
        """轨迹粗细自适应: 屏幕恒定 ~1.8px(scene 宽 = 1.8/scale), 与 StampTool 一致."""
        scale = 1.0
        views = self.views()
        if views:
            t = views[0].transform()
            scale = abs(t.m11()) or 1.0
        return max(0.5, 1.8 / scale)

    def _finish_polygon(self):
        # 轨迹抽稀成多边形顶点(采样间隔+共线合并),生成标注
        pts = simplify_track(self._free_track)
        self._cancel_polygon()
        if len(pts) < 3:
            return
        if self.template_mode:
            # 区域模板模式: 只记区域, 不成标注、不发 box_drawn(高亮归区域按钮)
            self.add_paste_region(pts)
            return
        item = self.add_polygon(pts, self.current_label)
        if item is not None:
            # 画完后立即可选中(绘制模式下其余标注不可选)
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            item.setSelected(True)
            self.box_drawn.emit(item)

    def _update_polygon_preview(self):
        # 绘制过程只做轨迹跟随(不抽稀),抽稀延后到_finish_polygon
        pts = self._free_track
        self._ensure_polygon_preview()
        c = self._polygon_trace_color()
        pen_c = QColor(c)
        pen_c.setAlpha(230)
        pen = QPen(pen_c, self._preview_pen_width())
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        self._preview_item.setPen(pen)
        path = QPainterPath()
        if pts:
            path.moveTo(pts[0][0], pts[0][1])
            for x, y in pts[1:]:
                path.lineTo(x, y)
        self._preview_item.setPath(path)
        self._preview_close_item.setVisible(self._update_close_hint(pts, c))

    def _update_close_hint(self, pts, color):
        """
        首尾已经靠得够近(<CLOSE_TOLERANCE>px)时补一条虚线连回起点:
        告诉用户松开鼠标就会闭合成多边形, 空白处不会再多出一截直线.
        """
        # StampTool 用 >3(点数太少时闭合线反而更抢眼)
        if len(pts) <= 3:
            return False
        x1, y1 = pts[0]
        x2, y2 = pts[-1]
        tol = self.CLOSE_TOLERANCE
        if (x2 - x1) ** 2 + (y2 - y1) ** 2 > tol * tol:
            return False
        pen_c = QColor(color)
        pen_c.setAlpha(200)
        pen = QPen(pen_c, self._preview_pen_width())
        pen.setCapStyle(Qt.RoundCap)
        pen.setStyle(Qt.DashLine)
        self._preview_close_item.setPen(pen)
        path = QPainterPath()
        path.moveTo(x2, y2)
        path.lineTo(x1, y1)
        self._preview_close_item.setPath(path)
        return True

    def mouseMoveEvent(self, event):
        if self._stamp_drag is not None:
            self._stamp_move(event)
            event.accept()
            return
        if self._region_drag is not None:
            item, idx = self._region_drag
            try:
                item._resize_vertex(item.mapFromScene(event.scenePos()), idx)
            except RuntimeError:
                self._region_drag = None
            event.accept()
            return
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
            self._stamp_hover(event.scenePos())
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
        if self._stamp_drag is not None:
            self._stamp_drag = None
            self._set_hover_cursor(None)
            event.accept()
            return
        if self._region_drag is not None:
            self._finish_region_drag()
            event.accept()
            return
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
                        self.box_drawn.emit(item)
            self._draw_start = None
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        """多边形模式: 双击闭合(>=3 顶点); 浏览态双击文本框: 改文字."""
        if self.draw_mode and self.draw_shape == "polygon" and event.button() == Qt.LeftButton:
            if len(self._free_track) >= 3:
                self._finish_polygon()
                event.accept()
                return
        if not self.draw_mode and event.button() == Qt.LeftButton:
            for it in self.items(event.scenePos()):
                if (isinstance(it, (AnnotationBoxItem, AnnotationPolygonItem))
                        and is_text_label(it.label)):
                    self.box_edit_requested.emit(it)
                    event.accept()
                    return
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event):
        """绘制模式 Esc 退出; 多边形 Enter 闭合; 格式刷 Esc 退出."""
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
