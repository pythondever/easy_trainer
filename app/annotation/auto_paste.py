# -*- coding: utf-8 -*-
"""自动粘贴: 开开关后每张图倒计时 3 秒, 往模板区域里随机贴 1~3 张剪切板小图.

计时全部走 QTimer: 之前有过"GUI 线程里干重活卡 16 秒"的教训, 这里每一拍都很轻,
融合动画只动图形项(虚线/颜色), 绝不每帧重新混合像素.
"""

import math
import random

from PySide6.QtCore import QObject, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPen
from PySide6.QtWidgets import (QGraphicsRectItem, QGraphicsSimpleTextItem,
                               QGraphicsItem)

from app.annotation import annotation_canvas as canvas_mod
from app.core import theme

COUNTDOWN_MS = 3000      # 倒计时时长
TICK_MS = 100            # 倒计时刷新间隔(同时也是进度动画的帧间隔)
PULSE_MS = 480           # 贴完那一下的局部强调动画时长
PULSE_STEP_MS = 40
MIN_PASTES, MAX_PASTES = 1, 3    # 一张图贴几次
SCALE_RANGE = (0.7, 1.3)         # 缩放范围
PLACE_TRIES = 60                 # 在区域里找落点的尝试次数


class AutoPasteController(QObject):
    """自动粘贴的节拍器: 倒计时 -> 贴 1~3 次 -> 等切图 -> 再来一轮."""

    def __init__(self, dlg):
        super().__init__(dlg)
        self.dlg = dlg
        self.enabled = False
        self._elapsed = 0
        self._preview = None
        self._text = None
        self._dim = None
        self._target = None
        self._pulse_ms = 0
        self._pulse_marks = []
        self.timer = QTimer(self)
        self.timer.setInterval(TICK_MS)
        self.timer.timeout.connect(self._tick)
        self.pulse = QTimer(self)
        self.pulse.setInterval(PULSE_STEP_MS)
        self.pulse.timeout.connect(self._pulse_tick)

    # ---------------- 开关 ----------------
    def set_enabled(self, on):
        self.enabled = bool(on)
        if not self.enabled:
            self._stop_all()
            return
        if not self._can_start():
            self.enabled = False
            return False
        self._restart()
        return True

    def _can_start(self):
        if not getattr(canvas_mod, "_clip_templates", None):
            return False
        return bool(self.dlg.scene.paste_regions)

    def _restart(self):
        self._clear_overlay()
        self._target = self._pick_target()
        if self._target is None:
            self._stop_all()
            return
        self._elapsed = 0
        self._show_overlay()
        self.timer.start()

    def _stop_all(self):
        self.timer.stop()
        self.pulse.stop()
        self._clear_overlay()

    # ---------------- 选落点 ----------------
    def _pick_target(self):
        """随机区域 + 区域内随机一点 + 随机一张剪切板小图(连缩放一起定好)."""
        scene = self.dlg.scene
        regions = [r for r in scene.paste_regions if r.scene() is scene]
        if not regions:
            return None
        region = random.choice(regions)
        tpl = self._pick_template()
        if tpl is None:
            return None
        pts = [[float(p.x()), float(p.y())] for p in region.polygon()]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        # 先按缩放把模板尺寸算出来, 再要求"落点加上半个模板"仍在多边形内
        sx = random.uniform(*SCALE_RANGE)
        half_w = max(4.0, float(tpl.get("w") or 40) * sx / 2.0)
        half_h = max(4.0, float(tpl.get("h") or 40) * sx / 2.0)
        from PySide6.QtGui import QPolygonF
        from PySide6.QtCore import QPointF
        poly = QPolygonF([QPointF(x, y) for x, y in pts])
        for _ in range(PLACE_TRIES):
            cx = random.uniform(min(xs), max(xs))
            cy = random.uniform(min(ys), max(ys))
            if not poly.containsPoint(QPointF(cx, cy), Qt.OddEvenFill):
                continue
            if (poly.containsPoint(QPointF(cx - half_w, cy - half_h), Qt.OddEvenFill)
                    and poly.containsPoint(QPointF(cx + half_w, cy + half_h),
                                           Qt.OddEvenFill)):
                return {"center": (cx, cy), "region": region, "scale": sx}
        # 兜底: 区域太窄或形状太怪时上面可能一次都试不出来, 退回重心,
        # 总比整轮静默失败(开关点了没反应)强
        cx = sum(xs) / float(len(xs))
        cy = sum(ys) / float(len(ys))
        return {"center": (cx, cy), "region": region, "scale": sx}

    def _pick_template(self):
        templates = getattr(canvas_mod, "_clip_templates", None) or []
        if not templates:
            return None
        idx = random.randrange(len(templates))
        try:
            # 必须走 _apply_clip_template: 它除了放模板还准备了粘贴要用的状态,
            # 只塞 scene.fp_template 会贴不出来(试过, 标记数为 0)
            self.dlg._apply_clip_template(idx)
            tpl = self.dlg.scene.fp_template
            # 它会顺手起一个跟着鼠标的虚线预览, 自动粘贴没鼠标跟着, 立刻收掉.
            # 顺序很关键: 收 ghost 会把 fp_template 一起清空, 所以先把模板拿到手
            self.dlg._cancel_stamp_ghost()
            if tpl is not None:
                self.dlg.scene.fp_template = tpl
        except Exception:
            return None
        return tpl

    # ---------------- 倒计时 ----------------
    def _show_overlay(self):
        """倒计时是"整屏"的: 压暗整幅可见区域 + 正中一个大数字;
        落点上另外留一个虚线框, 说明这次会贴到哪.
        """
        scene = self.dlg.scene
        tpl = scene.fp_template or {}
        cx, cy = self._target["center"]
        sx = self._target["scale"]
        w = max(8.0, float(tpl.get("w") or 40) * sx)
        h = max(8.0, float(tpl.get("h") or 40) * sx)
        self._preview = QGraphicsRectItem(QRectF(cx - w / 2.0, cy - h / 2.0, w, h))
        self._preview.setZValue(30)
        self._preview.setBrush(Qt.NoBrush)
        self._preview.setAcceptedMouseButtons(Qt.NoButton)
        scene.addItem(self._preview)
        # 可见区域(跟着缩放和滚动): 倒计时铺满这一块, 而不是缩在落点上
        view = getattr(self.dlg, "view", None)
        vrect = QRectF()
        if view is not None:
            vrect = view.mapToScene(view.viewport().rect()).boundingRect()
        if vrect.isEmpty():
            vrect = QRectF(cx - 300, cy - 200, 600, 400)
        self._dim = QGraphicsRectItem(vrect)
        self._dim.setZValue(29)
        self._dim.setPen(Qt.NoPen)
        self._dim.setBrush(QColor(0, 0, 0, 96))
        self._dim.setAcceptedMouseButtons(Qt.NoButton)
        scene.addItem(self._dim)
        self._text = QGraphicsSimpleTextItem("3")
        f = QFont()
        f.setPointSize(64)
        f.setBold(True)
        self._text.setFont(f)
        self._text.setBrush(QColor(theme.color("accent_text")))
        self._text.setZValue(31)
        br = self._text.boundingRect()
        self._text.setPos(vrect.center().x() - br.width() / 2.0,
                          vrect.center().y() - br.height() / 2.0)
        scene.addItem(self._text)

    def _update_overlay(self):
        left = max(0.0, (COUNTDOWN_MS - self._elapsed) / 1000.0)
        if self._text is not None:
            self._text.setText(str(int(math.ceil(left))))
        if self._preview is not None:
            # 倒计时进度: 虚线间距随剩余时间收紧, 只在图形项上做, 不碰像素
            frac = 1.0 - min(1.0, self._elapsed / float(COUNTDOWN_MS))
            pen = QPen(QColor(theme.color("accent")), 1.8 + 1.4 * frac)
            pen.setStyle(Qt.DashLine)
            gap = 2.0 + 8.0 * frac
            pen.setDashPattern([gap, gap])
            self._preview.setPen(pen)

    def _clear_overlay(self):
        scene = self.dlg.scene
        for it in (self._preview, self._text, self._dim):
            try:
                if it is not None and it.scene() is scene:
                    scene.removeItem(it)
            except RuntimeError:
                # set_image 的 clear() 会把遮罩项的 C++ 对象一并删掉, 这时只剩
                # Python 壳, 再碰它就 RuntimeError(Python 壳比 C++ 对象活得久)
                pass
        self._preview = None
        self._text = None
        self._dim = None

    def _tick(self):
        self._elapsed += TICK_MS
        if self._elapsed >= COUNTDOWN_MS:
            self.timer.stop()
            self._clear_overlay()
            self._do_pastes()
            return
        self._update_overlay()

    # ---------------- 贴 ----------------
    def _do_pastes(self):
        from PySide6.QtCore import QPointF
        scene = self.dlg.scene
        region = self._target["region"]
        base_x, base_y = self._target["center"]
        count = random.randint(MIN_PASTES, MAX_PASTES)
        marks = []
        for _ in range(count):
            pts = [[float(p.x()), float(p.y())] for p in region.polygon()]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            cx = min(max(base_x + random.uniform(-60, 60), min(xs) + 6), max(xs) - 6)
            cy = min(max(base_y + random.uniform(-60, 60), min(ys) + 6), max(ys) - 6)
            self._scale_current_template()
            mark = scene.auto_paste_at(QPointF(cx, cy))
            if mark is not None:
                marks.append(mark)
        # _apply_clip_template 会起一个跟着鼠标的虚线预览, 自动粘贴没有鼠标跟着,
        # 不收掉它就会一直留在图上
        try:
            self.dlg._cancel_stamp_ghost()
        except Exception:
            pass
        self._start_pulse(marks)
        # 一轮贴完就等切图(A/D), 换图后重新倒计时
        self._target = None

    def _scale_current_template(self):
        """按目标缩放临时换一份模板(只换 fp_template, 不动剪切板本身)."""
        scene = self.dlg.scene
        tpl = scene.fp_template
        if not tpl:
            return
        sx = self._target["scale"] if self._target else 1.0
        patch = tpl.get("patch")
        scaled = dict(tpl)
        if patch is not None and sx != 1.0:
            try:
                scaled["patch"] = patch.scaled(
                    max(4, int(patch.width() * sx)),
                    max(4, int(patch.height() * sx)),
                    Qt.KeepAspectRatio, Qt.SmoothTransformation)
            except Exception:
                pass
        pts = tpl.get("points") or []
        if pts and sx != 1.0:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            mx, my = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0
            scaled["points"] = [[(p[0] - mx) * sx + mx, (p[1] - my) * sx + my]
                                for p in pts]
        scene.fp_template = scaled

    # ---------------- 贴完那一下的局部动画 ----------------
    def _start_pulse(self, marks):
        self._pulse_marks = [m for m in marks]
        self._pulse_ms = 0
        if self._pulse_marks:
            self.pulse.start()

    def _pulse_tick(self):
        self._pulse_ms += PULSE_STEP_MS
        phase = min(1.0, self._pulse_ms / float(PULSE_MS))
        scale = math.sin(math.pi * phase)          # 0 -> 1 -> 0
        scene = self.dlg.scene
        alive = []
        for m in self._pulse_marks:
            if m.scene() is not scene:
                continue
            pen = QPen(QColor(theme.color("accent")), 1.6 + 2.6 * scale)
            pen.setStyle(Qt.DashLine)
            pen.setDashPattern([3, 3])
            m.setPen(pen)
            alive.append(m)
        self._pulse_marks = alive
        if self._pulse_ms >= PULSE_MS or not alive:
            self.pulse.stop()
            # 闪完就删掉: 不留常驻虚线, 也不再接鼠标(撤销统一走 Ctrl+Z)
            for m in alive:
                try:
                    if m.scene() is scene:
                        scene.removeItem(m)
                    if m in scene.auto_marks:
                        scene.auto_marks.remove(m)
                except RuntimeError:
                    pass
            self._pulse_marks = []

    # ---------------- 换图 ----------------
    def on_image_changed(self):
        # 换图先无条件收掉上一张的倒计时: 否则遮罩会留在新图上, 而且倒计时
        # 走完会拿旧图的落点往新图上贴
        self.timer.stop()
        self._clear_overlay()
        self._target = None
        # 然后直接贴一轮, 不再倒计时: 倒计时只是「打开开关」那一下的仪式,
        # 每张图都干等 3 秒反而费事
        if not self.enabled or not self._can_start():
            return
        self._paste_round_now()

    def _paste_round_now(self):
        # 不下倒计时直接贴一轮(切图后用)
        self.timer.stop()
        self._clear_overlay()
        target = self._pick_target()
        if target is None:
            return
        self._target = target
        self._do_pastes()
