# -*- coding: utf-8 -*-
"""标注图形项：矩形框 + 多边形，均支持选中、拖动、标签 chip 渲染。"""
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (QBrush, QColor, QPen, QFont, QFontMetrics, QPainter,
                           QPolygonF, QPainterPath)
import functools
import hashlib
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsItem
from app.core.utils import ui_font_family

# 深色背景下鲜艳的标签配色。
LABEL_COLORS = [
    "#4f7dff", "#3DDC97", "#F5B942", "#F0646E", "#C08BFF",
    "#4FC3F7", "#FF8A65", "#81C784", "#F06292", "#AED581",
    "#4DD0E1", "#FFD54F",
    "#F9779A", "#F97E72", "#E68026", "#D98A26",
    "#CC9226", "#B39F26", "#A3A626", "#72B436",
    "#52B852", "#30C391", "#30C1A5", "#32C5DC",
    "#43BFF9", "#69B9F9", "#80B4F9", "#A2A9F9",
    "#B2A2F9", "#C49AF9", "#DA8DF9", "#DF7DDE",
]


@functools.lru_cache(maxsize=None)
def label_color(label):
    """
    标签固定颜色（确定性哈希，md5 → 调色板索引）。
    同一标签名在任何进程/会话中颜色都一致
    lru_cache: 标注重绘热路径(paint)高频调用, 避免每次重复 md5 计算
    """
    try:
        digest = hashlib.md5(str(label).encode("utf-8")).hexdigest()
        idx = int(digest[:8], 16) % len(LABEL_COLORS)
    except Exception:
        idx = 0
    return QColor(LABEL_COLORS[idx])


def assign_label_color(label, used):
    """
    批量分配用: 从 label_color 的哈希位开始线性探测, 取第一个未被占用的颜色。
    used: 已分配的颜色集合(QColor.name() 小写 hex)。
    纯哈希在标签数接近调色板容量时必然撞色(N=20 撞 4 对), 探测后只要
    N <= len(LABEL_COLORS) 就能保证同批标签两两不同色。
    调色板用尽时退化成 label_color(仍确定, 只是可能与别人同色)。
    """
    try:
        digest = hashlib.md5(str(label).encode("utf-8")).hexdigest()
        start = int(digest[:8], 16) % len(LABEL_COLORS)
    except Exception:
        start = 0
    for k in range(len(LABEL_COLORS)):
        name = QColor(LABEL_COLORS[(start + k) % len(LABEL_COLORS)]).name()
        if name not in used:
            return name
    return QColor(LABEL_COLORS[start]).name()


_CHIP_FONT = None
_CHIP_FONT_METRICS = None
_CHIP_MIN_W = 30


def _chip_font():
    """chip 文字字体(含 CJK fallback), 全进程共享一份。"""
    global _CHIP_FONT
    if _CHIP_FONT is None:
        font = QFont(ui_font_family())
        if not font.exactMatch():
            font.setFamily("Noto Sans CJK SC, Microsoft YaHei, sans-serif")
        font.setStyleHint(QFont.SansSerif)
        font.setPixelSize(13)
        _CHIP_FONT = font
    return _CHIP_FONT


def _chip_font_metrics():
    """chip 文字度量, 用于算 chip 宽度; 随字体一并缓存。"""
    global _CHIP_FONT_METRICS
    if _CHIP_FONT_METRICS is None:
        _CHIP_FONT_METRICS = QFontMetrics(_chip_font())
    return _CHIP_FONT_METRICS


@functools.lru_cache(maxsize=512)
def _chip_text_width(text):
    """chip 精确宽度(按字体度量)。同一标签名在成百上千个标注上重复出现。"""
    return max(_CHIP_MIN_W, _chip_font_metrics().horizontalAdvance(text) + 12)


@functools.lru_cache(maxsize=512)
def _chip_screen_width(text):
    """chip 屏幕宽度估算(CJK 13px / ASCII 7px), 用于点击区换算。"""
    return max(_CHIP_MIN_W, sum(13 if ord(c) > 127 else 7 for c in text) + 12)


class AnnotationBoxItem(QGraphicsRectItem):
    """场景坐标下的标注框（rect 即像素坐标）。"""

    # 八向缩放手柄
    H_TL, H_TM, H_TR, H_ML, H_MR, H_BL, H_BM, H_BR = range(8)
    HANDLE_SIZE = 12.0
    HANDLE_CURSORS = {
        H_TL: Qt.SizeFDiagCursor, H_TM: Qt.SizeVerCursor, H_TR: Qt.SizeBDiagCursor,
        H_ML: Qt.SizeHorCursor, H_MR: Qt.SizeHorCursor,
        H_BL: Qt.SizeBDiagCursor, H_BM: Qt.SizeVerCursor, H_BR: Qt.SizeFDiagCursor,
    }

    def __init__(self, rect, label, editable=True, color=None):
        super().__init__(rect)
        self.label = label
        self.editable = editable
        self._handles = {}
        self._handle_selected = None
        self._press_pos = None
        self._press_rect = None
        self._color = color
        self._chip_cache = None

        pen_color = color if color is not None else label_color(label)
        self.setPen(QPen(pen_color, 2.0))
        fill = QColor(pen_color)
        fill.setAlpha(28)
        self.setBrush(QBrush(fill))

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(10)
        self._update_handles()

    # ---------------- 几何 ---------------- 
    def shape(self):
        """
        命中测试范围 = 框本体 + 标签 chip + 缩放手柄。
        QGraphicsRectItem.shape() 默认只有框本体矩形，而 chip 画在框上方
        22px（框外）、手柄一半在框外 → 场景命中测试（scene.items/itemAt）
        根本不会把点击事件派发给本 item。必须重载 shape 包含这些区域，
        否则点击标签名改类别、点手柄外侧调整大小都"没反应"。
        """
        path = QPainterPath()
        path.addRect(self.rect())
        path.addRect(self._chip_rect_local())
        if self.isSelected():
            for hrect in self._handles.values():
                path.addEllipse(hrect.adjusted(-3, -3, 3, 3))
        return path

    def _compute_handle_size(self):
        """手柄直径 [2,10], 除以 view 缩放屏幕恒定, 上限 20 防异常。"""
        r = self.rect()
        short = min(r.width(), r.height())
        s = max(2.0, min(10.0, short / 3.0))
        scale = self._view_scale()
        if scale > 1e-6:
            s = max(1.2, min(s / scale, 20.0))
        return s

    def _update_handles(self):
        """
        每个矩形固定 6 个圆形手柄：4 个角点 + 2 个长边中点。
        按实际方向判断长边是哪一对：
        - w ≥ h：长边是 top/bottom 边（长 = w）→ 中点 H_TM/H_BM（分布在水平中线 cx 上）
        - h > w：长边是 left/right 边（长 = h）→ 中点 H_ML/H_MR（分布在垂直中线 cy 上）
        中点放长边保证手柄间距足够大，避免粘连。
        """
        r = self.rect()
        s = self._compute_handle_size()
        self._handle_size = s
        cx = (r.left() + r.right()) / 2
        cy = (r.top() + r.bottom()) / 2
        self._handles = {
            # 4 角点
            self.H_TL: QRectF(r.left() - s / 2, r.top() - s / 2, s, s),
            self.H_TR: QRectF(r.right() - s / 2, r.top() - s / 2, s, s),
            self.H_BL: QRectF(r.left() - s / 2, r.bottom() - s / 2, s, s),
            self.H_BR: QRectF(r.right() - s / 2, r.bottom() - s / 2, s, s),
        }
        if r.width() >= r.height():
            self._handles.update({
                self.H_TM: QRectF(cx - s / 2, r.top() - s / 2, s, s),
                self.H_BM: QRectF(cx - s / 2, r.bottom() - s / 2, s, s),
            })
        else:
            self._handles.update({
                self.H_ML: QRectF(r.left() - s / 2, cy - s / 2, s, s),
                self.H_MR: QRectF(r.right() - s / 2, cy - s / 2, s, s),
            })

    def set_label(self, label, color=None):
        """
        修改类别。未显式传 color 时按新标签重新取色：
        优先场景标签色映射（scene.label_colors，db 自定义色），
        否则确定性哈希色——保证改类别后框和 chip 颜色跟随新标签。
        """
        self.label = label
        if color is None:
            scene = self.scene()
            if scene is not None:
                color = scene.label_colors.get(label)
            if color is None:
                color = label_color(label)
        self._color = color
        pen_color = color
        self.setPen(QPen(pen_color, 2.0))
        fill = QColor(pen_color)
        fill.setAlpha(28)
        self.setBrush(QBrush(fill))
        self.update()

    def boxes(self):
        r = self.rect().translated(self.pos())
        return [r.left(), r.top(), r.right(), r.bottom()]

    # ---------------- 交互 ---------------- 
    def handle_at(self, point):
        if not self.isSelected():
            return None
        for key, rect in self._handles.items():
            center = rect.center()
            radius = rect.width() / 2 + 3
            dx = point.x() - center.x()
            dy = point.y() - center.y()
            if dx * dx + dy * dy <= radius * radius:
                return key
        return None

    # ---------------- 标签 chip 点击（修改类别） ----------------
    def _view_scale(self):
        """
        当前 view 的缩放系数（无 view 时 1.0）。
        chip 绘制在屏幕坐标（恒定像素大小），点击检测在局部坐标，
        必须把屏幕宽度按 scale 换算回局部坐标，否则缩小视图时点不中。"""
        scene = self.scene()
        if scene is None:
            return 1.0
        views = scene.views()
        if not views:
            return 1.0
        return views[0].transform().m11() or 1.0

    def _chip_rect_local(self):
        """
        chip 点击区域, 锚定框右下角外侧(右对齐+底下方2px), 全部偏移/尺寸按缩放换算回局部坐标。
        与 _draw_label 的屏幕锚定保持一致, 否则放大视图时 chip 会离框越来越远。
        """
        r = self.rect()
        text = self.label[:12]
        scale = self._view_scale()
        key = (text, r.right(), r.bottom())
        cached = self._chip_cache
        if cached is not None and cached[0] == key and cached[1] == scale:
            return cached[2]
        s = scale if scale > 1e-6 else 1.0
        w = _chip_screen_width(text) / s
        rect = QRectF(r.right() - w, r.bottom() + 2.0 / s, w, 20.0 / s)
        self._chip_cache = (key, scale, rect)
        return rect

    def chip_scene_pos(self):
        """chip 中心点（场景坐标），用于菜单弹出定位。"""
        c = self._chip_rect_local().center()
        return QPointF(self.pos().x() + c.x(), self.pos().y() + c.y())

    def _chip_hit_pad(self, base=3.0):
        """chip 命中扩展: 屏幕恒定像素换算回局部坐标。
        若不除 scale, 放大视图后命中区膨胀成 base*scale 屏幕像素,
        菜单关闭后点击外部易误中 chip 导致菜单反复弹出(一直展开)。"""
        s = self._view_scale()
        return base / s if s > 1e-6 else base

    def hoverMoveEvent(self, event):
        scene = self.scene()
        if scene is not None and getattr(scene, "draw_mode", False):
            super().hoverMoveEvent(event)
            return
        p = self._chip_hit_pad()
        if self._chip_rect_local().adjusted(-p, -p, p, p).contains(event.pos()):
            self.setCursor(Qt.PointingHandCursor)
            super().hoverMoveEvent(event)
            return
        if self.isSelected():
            handle = self.handle_at(event.pos())
            cursor = Qt.ArrowCursor if handle is None else self.HANDLE_CURSORS[handle]
            self.setCursor(cursor)
        else:
            self.setCursor(Qt.SizeAllCursor)
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._press_geom = (self.pos(), self.rect())
            scene = self.scene()
            p = self._chip_hit_pad(2.0)
            if scene is not None and self._chip_rect_local().adjusted(-p, -p, p, p).contains(event.pos()):
                scene.label_change_requested.emit(self)
                event.accept()
                return
            self._handle_selected = self.handle_at(event.pos())
            if self._handle_selected is not None:
                self._press_pos = event.pos()
                self._press_rect = self.rect()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._handle_selected is not None:
            self._resize(event.pos())
            return
        if self.isSelected() and event.buttons() & Qt.LeftButton:
            super().mouseMoveEvent(event)
            self._update_handles()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        geom_changed = False
        if getattr(self, "_press_geom", None) is not None:
            geom_changed = (self.pos(), self.rect()) != self._press_geom
            self._press_geom = None
        self._handle_selected = None
        self._press_pos = None
        self._press_rect = None
        super().mouseReleaseEvent(event)
        if geom_changed:
            scene = self.scene()
            if scene is not None:
                scene.boxes_changed.emit()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene() is not None:
            # 移动时限制在图像范围内
            # 注意：rect 是局部坐标，场景坐标 = position + rect 偏移
            img_rect = self.scene().image_rect
            if img_rect is not None:
                scene_left = value.x() + self.rect().left()
                scene_top = value.y() + self.rect().top()
                scene_right = scene_left + self.rect().width()
                scene_bottom = scene_top + self.rect().height()
                if scene_left < img_rect.left():
                    value.setX(img_rect.left() - self.rect().left())
                if scene_top < img_rect.top():
                    value.setY(img_rect.top() - self.rect().top())
                if scene_right > img_rect.right():
                    value.setX(img_rect.right() - self.rect().right())
                if scene_bottom > img_rect.bottom():
                    value.setY(img_rect.bottom() - self.rect().bottom())
        return super().itemChange(change, value)

    def _resize(self, mouse_pos):
        r = self.rect()
        img_rect = self.scene().image_rect if self.scene() else None
        pos = self.pos()

        def clamp(v, lo, hi):
            return max(lo, min(hi, v))

        if img_rect is not None:
            lo_x = img_rect.left() - pos.x()
            hi_x = img_rect.right() - pos.x()
            lo_y = img_rect.top() - pos.y()
            hi_y = img_rect.bottom() - pos.y()
        else:
            lo_x, hi_x, lo_y, hi_y = -1e9, 1e9, -1e9, 1e9

        if self._handle_selected in (self.H_TL, self.H_ML, self.H_BL):
            r.setLeft(clamp(mouse_pos.x(), lo_x, r.right() - 4))
        if self._handle_selected in (self.H_TR, self.H_MR, self.H_BR):
            r.setRight(clamp(mouse_pos.x(), r.left() + 4, hi_x))
        if self._handle_selected in (self.H_TL, self.H_TM, self.H_TR):
            r.setTop(clamp(mouse_pos.y(), lo_y, r.bottom() - 4))
        if self._handle_selected in (self.H_BL, self.H_BM, self.H_BR):
            r.setBottom(clamp(mouse_pos.y(), r.top() + 4, hi_y))
        self.setRect(r)
        self._update_handles()
        self.update()

    # ---------------- 绘制 ---------------- 
    def boundingRect(self):
        """
        重绘范围 = 框 + 缩放手柄 + 标签 chip。
        """
        r = self.rect()
        o = getattr(self, "_handle_size", self.HANDLE_SIZE)
        base = r.adjusted(-o, -o - 24, o, o + 24)
        return base.united(self._chip_rect_local().adjusted(-o, -o, o, o))

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.pen())
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(self.brush())
        painter.drawRect(self.rect())
        label_rect = self._chip_rect_local()
        self._draw_label(painter, label_rect)
        if self.isSelected():
            painter.setPen(QPen(QColor("#4f7dff"), 1.0))
            painter.setBrush(QBrush(QColor("#ffffff")))
            s = self._compute_handle_size()
            self._handle_size = s
            for rect in self._handles.values():
                c = rect.center()
                painter.drawEllipse(QRectF(c.x() - s / 2, c.y() - s / 2, s, s))

    def _draw_label(self, painter, label_rect):
        color = self._color if self._color is not None else label_color(self.label)
        painter.save()
        transform = painter.transform()
        painter.resetTransform()
        painter.setFont(_chip_font())
        text = self.label[:12]
        w = _chip_text_width(text)
        h = 20
        r = self.rect()
        br = transform.map(QPointF(r.right(), r.bottom()))
        anchor = QPointF(br.x() - w, br.y() + 2)
        chip = QRectF(anchor.x(), anchor.y(), w, h)
        painter.setPen(QPen(QColor("#1c1e25"), 1.0))
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(chip, 4, 4)
        luminance = 0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()
        text_color = QColor("#1c1e25") if luminance > 160 else QColor("#ffffff")
        painter.setPen(text_color)
        painter.drawText(chip, Qt.AlignCenter, text)
        painter.restore()


# ---------------- 多边形标注项 ----------------

class AnnotationPolygonItem(QGraphicsPolygonItem):
    """场景坐标下的多边形标注（顶点即像素坐标）。与 BoxItem 共用 chip 渲染与配色。"""

    HANDLE_SIZE = 8.0

    def __init__(self, points, label, editable=True, color=None):
        super().__init__()
        self.label = label
        self.editable = editable
        self._color = color
        # points: [[x, y], ...]（场景/像素坐标）
        poly = QPolygonF([QPointF(p[0], p[1]) for p in points])
        self.setPolygon(poly)
        pen_color = color if color is not None else label_color(label)
        self.setPen(QPen(pen_color, 2.0))
        fill = QColor(pen_color)
        fill.setAlpha(28)
        self.setBrush(QBrush(fill))
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(10)
        self._handles = {}
        self._handle_size = 8.0
        self._vertex_idx = None
        self._press_geom = None
        # chip 区域记忆化缓存(见 _chip_rect_local)
        self._chip_cache = None
        self._update_handles()

    def _update_handles(self):
        s = self._compute_handle_size()
        self._handle_size = s
        self._handles = {
            i: QRectF(p.x() - s / 2, p.y() - s / 2, s, s)
            for i, p in enumerate(self.polygon())
        }

    def handle_at(self, point):
        if not self.isSelected():
            return None
        for idx, rect in self._handles.items():
            center = rect.center()
            radius = rect.width() / 2 + 3
            dx = point.x() - center.x()
            dy = point.y() - center.y()
            if dx * dx + dy * dy <= radius * radius:
                return idx
        return None

    def shape_type(self):
        return "polygon"

    def _compute_handle_size(self):
        """手柄直径 [2,6], 除以 view 缩放屏幕恒定, 上限 20 防异常。"""
        r = self.polygon().boundingRect()
        area = max(1.0, r.width() * r.height())
        s = max(2.0, min(6.0, area ** 0.5 * 0.25))
        scale = self._view_scale()
        if scale > 1e-6:
            s = max(1.2, min(s / scale, 20.0))
        return s

    def set_label(self, label, color=None):
        """
        修改类别。未显式传 color 时按新标签重新取色：
        优先场景标签色映射（scene.label_colors，db 自定义色），
        否则确定性哈希色——保证改类别后框和 chip 颜色跟随新标签。
        """
        self.label = label
        if color is None:
            scene = self.scene()
            if scene is not None:
                color = scene.label_colors.get(label)
            if color is None:
                color = label_color(label)
        self._color = color
        pen_color = color
        self.setPen(QPen(pen_color, 2.0))
        fill = QColor(pen_color)
        fill.setAlpha(28)
        self.setBrush(QBrush(fill))
        self.update()

    def points(self):
        """返回 [[x, y], ...]（场景/像素坐标，含 pos 偏移）。
        拖动后保存必须叠加 pos，否则关闭再打开位置丢失。"""
        pos = self.pos()
        return [[p.x() + pos.x(), p.y() + pos.y()] for p in self.polygon()]

    # ---------------- 标签 chip 点击（修改类别） ----------------
    def _view_scale(self):
        """当前 view 的缩放系数（无 view 时 1.0），供 chip 点击区域换算。"""
        scene = self.scene()
        if scene is None:
            return 1.0
        views = scene.views()
        if not views:
            return 1.0
        return views[0].transform().m11() or 1.0

    def _chip_rect_local(self):
        """chip 点击区域, 锚定外接矩形中心, 尺寸按缩放换算(记忆化, 同矩形版)。"""
        r = self.polygon().boundingRect()
        text = self.label[:12]
        scale = self._view_scale()
        key = (text, r.left(), r.top(), r.width(), r.height())
        cached = self._chip_cache
        if cached is not None and cached[0] == key and cached[1] == scale:
            return cached[2]
        w_screen = _chip_screen_width(text)
        if scale > 1e-6:
            w, h = w_screen / scale, 20.0 / scale
        else:
            w, h = w_screen, 20.0
        c = r.center()
        rect = QRectF(c.x() - w / 2, c.y() - h / 2, w, h)
        self._chip_cache = (key, scale, rect)
        return rect

    def chip_scene_pos(self):
        c = self._chip_rect_local().center()
        return QPointF(self.pos().x() + c.x(), self.pos().y() + c.y())

    # ---------------- 交互（拖动 + 图像范围限制）----------------
    def shape(self):
        """命中测试范围 = 多边形本体 + 标签 chip + 顶点手柄（选中时）。"""
        path = QPainterPath()
        path.addPolygon(self.polygon())
        path.addRect(self._chip_rect_local())
        if self.isSelected():
            for hrect in self._handles.values():
                path.addEllipse(hrect.adjusted(-3, -3, 3, 3))
        return path

    def _chip_hit_pad(self, base=3.0):
        """chip 命中扩展: 屏幕恒定像素换算回局部(与矩形一致, 防放大视图命中区膨胀)。"""
        s = self._view_scale()
        return base / s if s > 1e-6 else base

    def hoverMoveEvent(self, event):
        scene = self.scene()
        if scene is not None and getattr(scene, "draw_mode", False):
            super().hoverMoveEvent(event)
            return
        p = self._chip_hit_pad()
        if self._chip_rect_local().adjusted(-p, -p, p, p).contains(event.pos()):
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._press_geom = (self.pos(), self.polygon())
            scene = self.scene()
            p = self._chip_hit_pad(2.0)
            if scene is not None and self._chip_rect_local().adjusted(-p, -p, p, p).contains(event.pos()):
                scene.label_change_requested.emit(self)
                event.accept()
                return
            if self.isSelected():
                idx = self.handle_at(event.pos())
                if idx is not None:
                    self._vertex_idx = idx
                    self._press_poly = QPolygonF(self.polygon())
                    event.accept()
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._vertex_idx is not None:
            self._resize_vertex(event.pos())
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        geom_changed = False
        if self._vertex_idx is not None:
            self._vertex_idx = None
            if getattr(self, "_press_poly", None) is not None:
                geom_changed = self.polygon() != self._press_poly
                self._press_poly = None
            super().mouseReleaseEvent(event)
        else:
            if getattr(self, "_press_geom", None) is not None:
                geom_changed = (self.pos(), self.polygon()) != self._press_geom
                self._press_geom = None
            super().mouseReleaseEvent(event)
        if geom_changed:
            scene = self.scene()
            if scene is not None:
                scene.boxes_changed.emit()

    def _resize_vertex(self, point):
        """把顶点拖到局部坐标 point，限制在图像范围内。"""
        scene = self.scene()
        if scene is None or scene.image_rect is None:
            return
        sp = self.mapToScene(point)
        img = scene.image_rect
        x = max(img.left(), min(img.right(), sp.x()))
        y = max(img.top(), min(img.bottom(), sp.y()))
        local = self.mapFromScene(QPointF(x, y))
        pts = list(self.polygon())
        pts[self._vertex_idx] = local
        self.setPolygon(QPolygonF(pts))
        self._update_handles()
        self.update()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene() is not None:
            img_rect = self.scene().image_rect
            if img_rect is not None:
                rect = self.polygon().boundingRect()
                scene_left = value.x() + rect.left()
                scene_top = value.y() + rect.top()
                if scene_left < img_rect.left():
                    value.setX(img_rect.left() - rect.left())
                if scene_top < img_rect.top():
                    value.setY(img_rect.top() - rect.top())
                if scene_left + rect.width() > img_rect.right():
                    value.setX(img_rect.right() - rect.right())
                if scene_top + rect.height() > img_rect.bottom():
                    value.setY(img_rect.bottom() - rect.bottom())
        return super().itemChange(change, value)

    # ---------------- 绘制 ----------------
    def boundingRect(self):
        r = self.polygon().boundingRect()
        o = getattr(self, "_handle_size", self.HANDLE_SIZE)
        base = r.adjusted(-o, -o - 24, o, o + 24)
        return base.united(self._chip_rect_local().adjusted(-o, -o, o, o))

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.pen())
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(self.brush())
        painter.drawPolygon(self.polygon())

        label_rect = self._chip_rect_local()
        self._draw_label(painter, label_rect)

        if self.isSelected():
            painter.setPen(QPen(QColor("#4f7dff"), 1.0))
            painter.setBrush(QBrush(QColor("#ffffff")))
            s = self._compute_handle_size()
            self._handle_size = s
            for p in self.polygon():
                painter.drawEllipse(QRectF(p.x() - s / 2, p.y() - s / 2, s, s))

    def _draw_label(self, painter, label_rect):
        color = self._color if self._color is not None else label_color(self.label)
        painter.save()
        transform = painter.transform()
        scale = transform.m11() if abs(transform.m11()) > 1e-6 else 1.0
        painter.resetTransform()
        painter.setFont(_chip_font())
        text = self.label[:12]
        w = _chip_text_width(text)
        h = 20
        anchor = transform.map(QPointF(label_rect.left(), label_rect.top()))
        chip = QRectF(anchor.x(), anchor.y(), w, h)
        painter.setPen(QPen(QColor("#1c1e25"), 1.0))
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(chip, 4, 4)
        luminance = 0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()
        text_color = QColor("#1c1e25") if luminance > 160 else QColor("#ffffff")
        painter.setPen(text_color)
        painter.drawText(chip, Qt.AlignCenter, text)
        painter.restore()
