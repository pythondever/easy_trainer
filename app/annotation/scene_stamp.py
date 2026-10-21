# -*- coding: utf-8 -*-
"""
标注场景-贴图/盖章 mixin: 浮动粘贴(预览/手柄拖动/落盘)与自动粘贴.
"""
import math
import random

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (QPen, QColor, QBrush, QPolygonF, QPainter,
                           QImage)
from PySide6.QtWidgets import QGraphicsPolygonItem

from app.annotation.blend import blend_patch
from app.annotation.box_item import STAMP_ROTATE_SNAP, stamp_handle_cursor
from app.annotation.image_buf import bgra_view
from app.annotation.paste_regions import AutoPasteMark
from app.annotation.scene_geometry import rotate_points
from app.core import theme


class StampMixin:
    def _clamp_points_in_image(self, pts):
        """把多边形整体平移回图像内(保持形状, 不旋转): 保证完全在图内."""
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

    def _render_blend_layer(self, pix, patch, center, angle, rx, ry, side,
                            ox, oy, w, h, strength):
        """
        离屏渲染旋转后的 patch 并与图像 ROI 融合, 返回可绘制的 QImage.
        rx/ry/side = 离屏方框在图像中的位置和边长, ox/oy/w/h = 与图像重叠的有效区.
        """
        rot = QImage(side, side, QImage.Format_ARGB32_Premultiplied)
        rot.fill(Qt.transparent)
        rp = QPainter(rot)
        rp.setRenderHint(QPainter.Antialiasing)
        rp.translate(center.x() - rx, center.y() - ry)
        rp.rotate(angle)
        rp.drawImage(-patch.width() / 2.0, -patch.height() / 2.0, patch)
        rp.end()
        sx, sy = ox - rx, oy - ry
        src = bgra_view(rot)[sy:sy + h, sx:sx + w]
        dst_q = pix.copy(ox, oy, w, h).toImage().convertToFormat(
            QImage.Format_ARGB32)
        dst = bgra_view(dst_q)
        a = src[..., 3].astype(np.float32)
        # QImage 存的是预乘 alpha, 参与混合前要还原成真实颜色
        scale = np.where(a > 0.0, 255.0 / np.maximum(a, 1e-6), 0.0)[..., None]
        bgra = np.empty((h, w, 4), np.uint8)
        bgra[..., :3] = np.clip(src[..., :3].astype(np.float32) * scale, 0, 255)
        bgra[..., 3] = a.astype(np.uint8)
        out = np.empty((h, w, 4), np.uint8)
        out[..., :3] = blend_patch(dst[..., :3], bgra, strength)
        out[..., 3] = 255
        # 必须写进 QImage 自己的缓冲区: 用外部 bytes 构造的 QImage 不持有数据, 会悬空
        layer = QImage(w, h, QImage.Format_ARGB32)
        bgra_view(layer)[:] = out
        return layer

    @staticmethod
    def _render_stamp_layer(patch, angle, scale=1.0):
        """patch 按 angle 旋转、按 scale 缩放后渲染成紧凑 QImage(图心即旋转中心), 供浮动层直接绘制."""
        pw, ph = patch.width() * scale, patch.height() * scale
        rad = math.radians(angle)
        ca, sa = abs(math.cos(rad)), abs(math.sin(rad))
        # 减 eps 再取整: cos(90°) 不是精确 0 而是 6e-17, 不修正的话 30 会被 ceil 成 31
        w = max(1, int(math.ceil(pw * ca + ph * sa - 1e-6)))
        h = max(1, int(math.ceil(pw * sa + ph * ca - 1e-6)))
        out = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
        out.fill(Qt.transparent)
        p = QPainter(out)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.translate(w / 2.0, h / 2.0)
        p.rotate(angle)
        p.drawImage(QRectF(-pw / 2.0, -ph / 2.0, pw, ph), patch)
        p.end()
        return out

    def _stamp_patch(self, meta):
        """
        浮动层显示用的图案: 按 meta 的角度与倍数转好、缩放好的一份位图.
        只走显示这条路; 落地走 _blend_stamp_at, 而它要的是"没转过"的那份
        (旋转由它自己按 angle 施加一次, 见 commit_pastes).
        """
        return self._render_stamp_layer(meta["patch"],
                                        float(meta.get("angle", 0.0)),
                                        float(meta.get("scale", 1.0)))

    def _blend_stamp_at(self, patch, center, angle, pix=None):
        """
        把 patch 按 angle 围绕 center 融合进图像像素, 返回撤销所需的 (原图区域, ox, oy).
        patch 必须是没转过、但已按倍数缩放好的那份: 旋转在这里只做一次,
        传"已经转过"的位图进来就会变成两倍角(实测 40° 落成 80°).
        pix 由调用方传入时直接改写这一份: 一批粘贴共用同一个引用, 只有第一次会触发
        整图写时复制, 否则每贴一个都要把整幅像素拷一遍.
        """
        # 亮度还没落盘的话先写进去, 下面取到的 pix 才是最终要融合的像素
        self.drop_brightness()
        own = pix is None
        if own:
            pix = self.image_item.pixmap() if self.image_item is not None else None
        if pix is None or patch is None:
            return None
        pw, ph = patch.width(), patch.height()
        radius = math.sqrt(pw * pw + ph * ph) / 2.0
        # 旋转后的 patch 一定落在以 center 为中心, 边长 2*radius 的方框内
        rx = int(center.x() - radius)
        ry = int(center.y() - radius)
        side = int(2 * radius) + 1
        ox = max(0, rx)
        oy = max(0, ry)
        bw = min(rx + side, pix.width()) - ox
        bh = min(ry + side, pix.height()) - oy
        before = pix.copy(ox, oy, max(0, bw), max(0, bh))
        if before.isNull():
            before = None
        p = QPainter(pix)
        strength = float(getattr(self, "blend_strength", 0.0) or 0.0)
        if strength > 0.0 and bw > 0 and bh > 0:
            layer = self._render_blend_layer(
                pix, patch, center, angle, rx, ry, side, ox, oy, bw, bh,
                strength)
            p.drawImage(ox, oy, layer)
        else:
            # 预览那份位图是带抗锯齿转出来的: 这里不抗锯齿的话, 落地边缘会比预览硬一圈,
            # 看着"贴上去的和刚才预览的不是同一张"
            p.setRenderHint(QPainter.Antialiasing)
            p.translate(center.x(), center.y())
            p.rotate(angle)
            p.drawImage(-pw / 2.0, -ph / 2.0, patch)
        p.end()
        if own:
            self.image_item.setPixmap(pix)
        return before, ox, oy

    def start_stamp_ghost(self):
        """
        选中剪切板模板: 开一条跟随鼠标的多边形虚线, 让人先看清这一贴落在哪.
        角度在这里一次定死: 预览和落点必须是同一个角, 否则虚线骗人.
        """
        self.stop_stamp_ghost()
        if not self.fp_template:
            return
        lo, hi = getattr(self, "angle_range", (-180, 180))
        self._stamp_angle = random.uniform(lo, hi)
        item = QGraphicsPolygonItem()
        pen = QPen(theme.alpha("accent", 230), 1.4)
        pen.setCosmetic(True)
        pen.setStyle(Qt.DashLine)
        item.setPen(pen)
        item.setBrush(QBrush(theme.alpha("accent", 30)))
        item.setZValue(18)
        item.setAcceptedMouseButtons(Qt.NoButton)
        self.addItem(item)
        self._stamp_ghost = item

    def stop_stamp_ghost(self):
        """ESC / 换模板 / 切图: 收掉虚线预览."""
        if self._stamp_ghost is not None:
            self.removeItem(self._stamp_ghost)
            self._stamp_ghost = None
        self._stamp_angle = None

    def update_stamp_ghost(self, pos):
        """虚线跟着鼠标: 先平移居中到光标, 再按已定角度旋转, 最后夹回图内."""
        t = self.fp_template
        item = self._stamp_ghost
        if t is None or item is None or self._stamp_angle is None:
            return
        pts = t["points"]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        dx = pos.x() - (min(xs) + max(xs)) / 2
        dy = pos.y() - (min(ys) + max(ys)) / 2
        moved = [[p[0] + dx, p[1] + dy] for p in pts]
        rotated = rotate_points(moved, pos, self._stamp_angle)
        rotated = self._clamp_points_in_image(rotated)
        item.setPolygon(QPolygonF([QPointF(x, y) for x, y in rotated]))

    def _paste_template(self, pos):
        """
        以 pos 为中心把模板贴成浮动层: 只放预览, 不动图像像素, 期间可整体拖动位置.
        像素等 commit_pastes()(Ctrl+S / 切图 / 关闭)时才写进去, 可 Ctrl+Z 撤掉浮层.
        """
        t = self.fp_template
        if not t:
            return
        lo, hi = getattr(self, "angle_range", (-180, 180))
        # 有虚线预览时用预览那个角(所见即所得); 没预览(格式刷刷子)才现摇一个
        angle = self._stamp_angle if self._stamp_angle is not None \
            else random.uniform(lo, hi)
        # 1. 平移到以 pos 为中心(已有基础夹紧)
        shifted = self._shift_template(pos)
        # 2. 绕 pos 随机旋转(正=顺时针, 负=逆时针)
        rotated = rotate_points(shifted, pos, angle)
        # 3. 旋转后整体夹紧回图像内(保持形状, 避免出界)
        rotated = self._clamp_points_in_image(rotated)
        xs = [p[0] for p in rotated]
        ys = [p[1] for p in rotated]
        center = QPointF((min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0)
        if self.fp_ghost_item is not None:
            self.removeItem(self.fp_ghost_item)
            self.fp_ghost_item = None
        item = self.add_polygon(rotated, t.get("label") or self.current_label)
        if item is None:
            return
        patch = t.get("patch")
        if patch is not None:
            meta = {"patch": patch, "center": center, "angle": angle, "scale": 1.0}
            img = self._stamp_patch(meta)
            anchor = QPointF(center.x() - img.width() / 2.0,
                             center.y() - img.height() / 2.0)
            item.set_pending_stamp(img, anchor, meta)
            self._pending_pastes.append(item)
        # 粘贴不享受"刚画完仍显示"的例外: 开关关着就不出框, 也不抢占选中态
        item.set_outline_visible(self.show_annotations)
        if self.show_annotations:
            item.setSelected(True)
        # 下一次粘贴换个角度(虚线预览同步刷新, 连续贴才不会摞成一模一样的)
        if self._stamp_ghost is not None:
            self._stamp_angle = random.uniform(lo, hi)

    def has_pending_pastes(self):
        return any(i.scene() is self for i in self._pending_pastes)

    def commit_pastes(self):
        """
        把浮动粘贴写进图像像素(显式保存 / 切图 / 关闭前调用), 返回落地个数.
        拖动改的是 item.pos(), 落点要跟着平移, 否则图会落在原处、框跑别处;
        缩放按 meta["scale"] 现算一份图案, 落到像素上的才是拖动时看到的那个大小.
        """
        if not self._pending_pastes:
            return 0
        self.drop_brightness()
        pending = self._pending_pastes
        self._pending_pastes = []
        # 整批共用一份像素引用: 落到最后才回写, 中途每贴一个都回写要拷一遍整图
        pix = self.image_item.pixmap() if self.image_item is not None else None
        done = 0
        for item in pending:
            meta = getattr(item, "pending_meta", None)
            if meta is None or item.scene() is not self:
                continue
            off = item.pos()
            center = QPointF(meta["center"].x() + off.x(),
                             meta["center"].y() + off.y())
            # 这里只能送"没转过"的图案: _blend_stamp_at 自己会按 angle 转一次.
            # 送 _stamp_patch()(已按 angle 转好、只是用来显示的那份)会转成两倍角,
            # 落地出来和预览不是一个朝向(实测 angle=40° 落下去是 80°).
            res = self._blend_stamp_at(
                self._render_stamp_layer(meta["patch"], 0.0,
                                         float(meta.get("scale", 1.0))),
                center, meta["angle"], pix)
            item.clear_pending_stamp()
            # 图案已进像素, 框从此只是框: 开关关着就该整体隐藏
            item.set_outline_visible(self.show_annotations)
            if res is None:
                continue
            before, ox, oy = res
            self._fp_undo_stack.append(
                {"before": before, "ox": ox, "oy": oy, "item": item})
            done += 1
        if done:
            if pix is not None:
                self.image_item.setPixmap(pix)
            self.image_modified = True
            self.image_pixels_changed.emit()
            self._force_full_redraw()
        return done

    def auto_paste_at(self, pos):
        """
        把当前选中的剪切板模板贴到 pos 并立刻融合, 顺便返回一个轮廓项.
        与手动粘贴的区别就是"不等 Ctrl+S": 自动粘贴要的就是贴完即生效,
        每贴一次记一条, 点标记框可以只撤那一次.
        返回标记框; 没贴上返回 None.
        """
        if self.fp_template is None:
            return None
        n0 = len(self._pending_pastes)
        self._paste_template(pos)
        if len(self._pending_pastes) == n0:
            return None
        item = self._pending_pastes[-1]
        outline = QPolygonF(list(item.polygon()))
        self.commit_pastes()
        rec = self._fp_undo_stack[-1] if self._fp_undo_stack else None
        if rec is None:
            return None
        mark = AutoPasteMark(outline, rec)
        self.addItem(mark)
        self.auto_marks.append(mark)
        return mark

    def clear_auto_marks(self):
        """换图/关窗时清掉标记框: 那之后像素已经落盘, 不再是"可撤的一次"."""
        for mark in list(self.auto_marks):
            self.removeItem(mark)
        self.auto_marks = []

    def _floating_pastes(self):
        """当前所有选中的浮动粘贴(手柄/图标只长在选中的那个上)."""
        return [it for it in self._pending_pastes
                if it.scene() is self and it.is_floating() and it.isSelected()]

    def _stamp_hit(self, scene_pos):
        """
        该点命中的浮动粘贴手柄: (item, "scale"/"rotate", 手柄下标或 None).
        不能靠 items() 找父项: 转过角度后外接框的角点落在轮廓多边形之外,
        而手柄正是贴在外接框上的 —— 按 items() 判会刚好把手柄漏掉.
        """
        for it in self._floating_pastes():
            hit = it.stamp_handle_hit(scene_pos)
            if hit is not None:
                return it, "scale", hit[0]
            if it.stamp_rotate_hit(scene_pos):
                return it, "rotate", None
        return None

    def _stamp_press(self, event):
        """按优先级把左键交给浮动粘贴的手柄: 缩放手柄 > 旋转图标 > (不管, 交回图体)."""
        scene_pos = event.scenePos()
        found = self._stamp_hit(scene_pos)
        if found is None:
            return False
        item, kind, idx = found
        if kind == "scale":
            drag = item.press_stamp_scale(scene_pos)
            if drag is None:
                return False
            drag["item"] = item
            self._stamp_drag = drag
            self._set_hover_cursor(drag["cursor"])
            return True
        # 旋转: 记下按下时的角度与方位角, 之后按方位角增量累计(拖整圈也不会突然倒转)
        self._stamp_drag = {"kind": "rotate", "item": item,
                            "press_angle": float(item.pending_meta["angle"]),
                            "last_azimuth": item.stamp_rotate_drag(scene_pos),
                            "angle_acc": 0.0}
        self._set_hover_cursor(Qt.CrossCursor)
        return True

    def _stamp_hover(self, scene_pos):
        """没按键时的移动: 让缩放手柄上的光标跟着手柄方位变(手柄是手画的, 收不到悬停事件)."""
        turn = None
        found = self._stamp_hit(scene_pos)
        if found is not None:
            _item, kind, idx = found
            turn = stamp_handle_cursor(idx) if kind == "scale" else Qt.CrossCursor
        if turn is not None or self._hover_cursor is not None:
            self._set_hover_cursor(turn)

    def _set_hover_cursor(self, cursor):
        """光标改给 view: 手柄/图标都是自绘的, 收不到悬停事件, 只能在这里设."""
        self._hover_cursor = cursor
        views = self.views()
        if views:
            if cursor is None:
                views[0].unsetCursor()
            else:
                views[0].setCursor(cursor)

    def _stamp_move(self, event):
        """拖动中的浮动粘贴手柄: 只改图形项(图案/轮廓), 图像像素等 commit_pastes()."""
        drag = self._stamp_drag
        item = drag["item"]
        if drag["kind"] == "scale":
            item.drag_stamp_scale(event.scenePos(), drag["scale0"], drag["dist0"])
            return
        azimuth = item.stamp_rotate_drag(event.scenePos())
        # 只累加这一小步(归一化到 ±180): 拖过一整圈也不会因取模突然倒转
        drag["angle_acc"] += (azimuth - drag["last_azimuth"] + 180.0) % 360.0 - 180.0
        drag["last_azimuth"] = azimuth
        angle = drag["press_angle"] + drag["angle_acc"]
        if event.modifiers() & Qt.ShiftModifier:
            angle = round(angle / STAMP_ROTATE_SNAP) * STAMP_ROTATE_SNAP
        item.rotate_stamp_to(angle)
