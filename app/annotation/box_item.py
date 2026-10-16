# -*- coding: utf-8 -*-
"""标注图形项: 矩形框 + 多边形, 均支持选中, 拖动, 标签 chip 渲染."""
from PySide6.QtCore import QPointF, QRectF, QSizeF, Qt
from PySide6.QtGui import (QBrush, QColor, QPen, QFont, QFontMetrics, QPainter,
                           QPainterPath, QPolygonF)
import functools
import hashlib
import math
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsItem
from app.core import theme
from app.core.utils import ui_font_family

# 深色背景下鲜艳的标签配色.
# CIEDE2000 最远点贪心(MaxMin)从 HSV 候选池挑的 32 色, 表内任意两色 dE00 >= 11,
# 与三个固定色(全选红 #e03737 / 未标注黑 #000000 / 灰点 #5c6270)也 >= 12.
LABEL_COLORS = [
    "#ffff00", "#00f2ff", "#ff73ff", "#b88100",
    "#00b853", "#73a4ff", "#ff9d73", "#1ca0b8",
    "#f00084", "#73ffc7", "#66ff00", "#9d4dff",
    "#aeb853", "#ffbf00", "#37b8a4", "#d66000",
    "#ff7381", "#6072d6", "#4dc9ff", "#1c81b8",
    "#b853ae", "#ff8c00", "#ff73b2", "#b86c53",
    "#d6a760", "#ff674d", "#cff06c", "#f000f0",
    "#ffe373", "#6eb800", "#b8a01c", "#00f078",
]


@functools.lru_cache(maxsize=None)
def label_color(label):
    """
    标签固定颜色(确定性哈希, md5 取模得调色板索引).
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
    批量分配用: 从 label_color 的哈希位开始线性探测, 取第一个未被占用的颜色.
    used: 已分配的颜色集合(QColor.name() 小写 hex).
    纯哈希在标签数接近调色板容量时必然撞色(N=20 撞 4 对), 探测后只要
    N <= len(LABEL_COLORS) 就能保证同批标签两两不同色.
    调色板用尽时退化成 label_color(仍确定, 只是可能与别人同色).
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
    """chip 文字字体(含 CJK fallback), 全进程共享一份."""
    global _CHIP_FONT
    if _CHIP_FONT is None:
        font = QFont(ui_font_family())
        if not font.exactMatch():
            font.setFamily("Noto Sans CJK SC, Microsoft YaHei, sans-serif")
        font.setStyleHint(QFont.SansSerif)
        font.setPixelSize(theme.px(13))
        _CHIP_FONT = font
    return _CHIP_FONT


def _chip_font_metrics():
    """chip 文字度量, 用于算 chip 宽度; 随字体一并缓存."""
    global _CHIP_FONT_METRICS
    if _CHIP_FONT_METRICS is None:
        _CHIP_FONT_METRICS = QFontMetrics(_chip_font())
    return _CHIP_FONT_METRICS


@functools.lru_cache(maxsize=512)
def _chip_text_width(text):
    """chip 精确宽度(按字体度量). 同一标签名在成百上千个标注上重复出现."""
    return max(_CHIP_MIN_W, _chip_font_metrics().horizontalAdvance(text) + 12)


@functools.lru_cache(maxsize=512)
def _chip_screen_width(text):
    """chip 屏幕宽度估算(CJK 13px / ASCII 7px), 用于点击区换算."""
    return max(_CHIP_MIN_W, sum(13 if ord(c) > 127 else 7 for c in text) + 12)


def chip_text(item):
    """
    chip 上显示的文字: 文本框(OCR)显示所录内容, 其它标注显示类别名.
    文本框的类别是保留标签, 显示它等于没说; 录进去的内容
    才是要核对的东西, 所以有文字就优先显示文字.
    """
    return (item.text or item.label)[:12]


class _ViewScaleMixin(object):
    """view 缩放系数: chip 尺寸与顶点手柄都要按它换算成屏幕恒定像素."""

    def _view_scale(self):
        """
        当前 view 的缩放系数(无 view 时 1.0).
        chip 绘制在屏幕坐标(恒定像素大小), 点击检测在局部坐标,
        必须把屏幕宽度按 scale 换算回局部坐标, 否则缩小视图时点不中.
        """
        scene = self.scene()
        if scene is None:
            return 1.0
        views = scene.views()
        if not views:
            return 1.0
        return views[0].transform().m11() or 1.0


class _LabelChipMixin(_ViewScaleMixin):
    """矩形/多边形共用的"标签取色 + chip 缩放换算": 两份实现必须一致, 合并到一处."""

    def set_label(self, label, color=None):
        """
        修改类别. 未显式传 color 时按新标签重新取色:
        优先场景标签色映射(scene.label_colors, db 自定义色),
        否则确定性哈希色 - 保证改类别后框和 chip 颜色跟随新标签.
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


class _VertexHandleMixin(_ViewScaleMixin):
    """多边形顶点手柄: 选中后显示手柄、手柄尺寸随缩放保持屏幕恒定、拖手柄改顶点.

    常规多边形标注与粘贴区域共用这一套, 免得两边的视觉和手感各走各的.
    """

    def _compute_handle_size(self):
        """手柄直径 [2,6], 除以 view 缩放屏幕恒定, 上限 20 防异常."""
        r = self.polygon().boundingRect()
        area = max(1.0, r.width() * r.height())
        s = max(2.0, min(6.0, area ** 0.5 * 0.25))
        scale = self._view_scale()
        if scale > 1e-6:
            s = max(1.2, min(s / scale, 20.0))
        return s

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

    def _resize_vertex(self, point, idx=None):
        """把第 idx 个顶点拖到局部坐标 point(不传 = 拖 _vertex_idx), 限制在图像范围内."""
        if idx is None:
            idx = self._vertex_idx
        if idx is None:
            return
        scene = self.scene()
        if scene is None or scene.image_rect is None:
            return
        sp = self.mapToScene(point)
        img = scene.image_rect
        x = max(img.left(), min(img.right(), sp.x()))
        y = max(img.top(), min(img.bottom(), sp.y()))
        local = self.mapFromScene(QPointF(x, y))
        pts = list(self.polygon())
        pts[idx] = local
        self.setPolygon(QPolygonF(pts))
        self._update_handles()
        self.update()

    def _paint_vertex_handles(self, painter):
        """手柄画法: 主题色描边 + 白点, 与矩形缩放手柄同一套观感."""
        painter.setPen(QPen(theme.color("accent"), 1.0))
        painter.setBrush(QBrush(QColor("#ffffff")))
        s = self._compute_handle_size()
        self._handle_size = s
        for p in self.polygon():
            painter.drawEllipse(QRectF(p.x() - s / 2, p.y() - s / 2, s, s))


class AnnotationBoxItem(_LabelChipMixin, QGraphicsRectItem):
    """场景坐标下的标注框(rect 即像素坐标)."""

    # 八向缩放手柄
    H_TL, H_TM, H_TR, H_ML, H_MR, H_BL, H_BM, H_BR = range(8)
    HANDLE_SIZE = 12.0
    HANDLE_CURSORS = {
        H_TL: Qt.SizeFDiagCursor, H_TM: Qt.SizeVerCursor, H_TR: Qt.SizeBDiagCursor,
        H_ML: Qt.SizeHorCursor, H_MR: Qt.SizeHorCursor,
        H_BL: Qt.SizeBDiagCursor, H_BM: Qt.SizeVerCursor, H_BR: Qt.SizeFDiagCursor,
    }

    def __init__(self, rect, label, editable=True, color=None, text=""):
        super().__init__(rect)
        self.label = label
        self.editable = editable
        self.text = text
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
        命中测试范围 = 框本体 + 标签 chip + 缩放手柄.
        QGraphicsRectItem.shape() 默认只有框本体矩形, 而 chip 画在框上方
        22px(框外), 手柄一半在框外, 于是场景命中测试(scene.items/itemAt)
        根本不会把点击事件派发给本 item. 必须重载 shape 包含这些区域,
        否则点击标签名改类别, 点手柄外侧调整大小都"没反应".
        """
        path = QPainterPath()
        path.addRect(self.rect())
        path.addRect(self._chip_rect_local())
        if self.isSelected():
            for hrect in self._handles.values():
                path.addEllipse(hrect.adjusted(-3, -3, 3, 3))
        return path

    def _compute_handle_size(self):
        """手柄直径 [2,10], 除以 view 缩放屏幕恒定, 上限 20 防异常."""
        r = self.rect()
        short = min(r.width(), r.height())
        s = max(2.0, min(10.0, short / 3.0))
        scale = self._view_scale()
        if scale > 1e-6:
            s = max(1.2, min(s / scale, 20.0))
        return s

    def _update_handles(self):
        """
        每个矩形固定 6 个圆形手柄: 4 个角点 + 2 个长边中点.
        按实际方向判断长边是哪一对:
        - w ≥ h: 长边是 top/bottom 边(长 = w), 中点取 H_TM/H_BM(分布在水平中线 cx 上)
        - h > w: 长边是 left/right 边(长 = h), 中点取 H_ML/H_MR(分布在垂直中线 cy 上)
        中点放长边保证手柄间距足够大, 避免粘连.
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

    def boxes(self):
        r = self.rect().translated(self.pos())
        return [r.left(), r.top(), r.right(), r.bottom()]

    def set_outline_visible(self, show):
        """矩形没有浮层图案, 关掉"显示标注"就是整体隐藏."""
        self.setVisible(bool(show))

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

    def _chip_rect_local(self):
        """
        chip 点击区域, 锚定框右下角外侧(右对齐+底下方2px), 全部偏移/尺寸按缩放换算回局部坐标.
        与 _draw_label 的屏幕锚定保持一致, 否则放大视图时 chip 会离框越来越远.
        """
        r = self.rect()
        text = chip_text(self)
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
        """chip 中心点(场景坐标), 用于菜单弹出定位."""
        c = self._chip_rect_local().center()
        return QPointF(self.pos().x() + c.x(), self.pos().y() + c.y())

    def _chip_hit_pad(self, base=3.0):
        """
        chip 命中扩展: 屏幕恒定像素换算回局部坐标.
        若不除 scale, 放大视图后命中区膨胀成 base*scale 屏幕像素,
        菜单关闭后点击外部易误中 chip 导致菜单反复弹出(一直展开).
        """
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
            # 注意: rect 是局部坐标, 场景坐标 = position + rect 偏移
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
        重绘范围 = 框 + 缩放手柄 + 标签 chip.
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
            painter.setPen(QPen(theme.color("accent"), 1.0))
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
        text = chip_text(self)
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


# ---------------- 浮动粘贴的旋转图标 ----------------
# ---------------- 浮动粘贴的旋转图标 ----------------
# 图标与缩放手柄都由浮动项自己在 paint 里画: 位置用本项局部坐标算, 直径用屏幕像素 /
# view 缩放换算, 这样"画在哪"与"点在哪"永远是同一套坐标, 不再依赖 Qt 对
# ItemIgnoresTransformations 子项的映射(那套在 view 缩放后落点对不上).
STAMP_ROTATE_GAP = 28.0     # 图标离小图顶边中点的屏幕距离
STAMP_ROTATE_R = 9.0        # 图标半径(屏幕像素)
STAMP_ROTATE_PAD = 4.0      # 图标命中额外放宽(小圆点不好点)
STAMP_ROTATE_SNAP = 15.0    # 按住 Shift 吸附的角度步长(度)
# ---------------- 浮动粘贴的缩放手柄 ----------------
# 手柄由浮动项自己在 paint 里画(不再用带 ItemIgnoresTransformations 的子项):
# 那种子项在 view 缩放后, 绘制落点与 Qt/手工算的坐标都对不上, 也没法被稳定命中.
# 直接画就没有这层歧义: 位置用本项局部坐标算, 直径用屏幕像素 / view 缩放换算.
STAMP_SCALE_CORNER_R = 6.5   # 4 角手柄基准半径(屏幕像素): 略大, 一眼看出是角
STAMP_SCALE_EDGE_R = 5.0     # 4 边中点手柄基准半径: 略小, 与角区分开
STAMP_SCALE_PAD = 3.0        # 命中额外放宽(小圆点不好点)
# 外接框线 + 手柄随框缩小: 固定半径在小图上挤成一团, 框线又让手柄没有归属感
STAMP_FRAME_LINE_W = 1.5     # 外接框线宽(屏幕像素)
STAMP_HANDLE_FULL_PX = 140.0 # 外接框短边到这个屏幕尺寸才用基准半径
STAMP_HANDLE_MIN_FRAC = 0.55 # 手柄半径收缩下限: 再小就既看不清也点不中
STAMP_HANDLE_MIN_HIT = 5.5   # 命中半径下限(屏幕像素)
STAMP_EDGE_HANDLE_MIN_PX = 64.0  # 框短边小于它就不画边中点手柄(那个尺寸下没信息量)
# 缩放上下限(与 C# 那个工具一致): 定义在这里, scene 反向引用,
# 免得两个模块各写一份, 改一处漏一处
STAMP_SCALE_MIN, STAMP_SCALE_MAX = 0.1, 5.0
# 8 个手柄: 4 角 + 4 边中点. 偏移按 (半宽 u, 半高 v) 的组合给, 与旋转一起转
STAMP_HANDLE_OFFSETS = ((-1, -1), (0, -1), (1, -1),
                        (-1, 0), (1, 0),
                        (-1, 1), (0, 1), (1, 1))
STAMP_HANDLE_CORNERS = (0, 2, 5, 7)
# 外接框 4 角的连线顺序(顺时针: 左上→右上→右下→左下), 写的是 STAMP_HANDLE_OFFSETS 的下标
STAMP_FRAME_ORDER = (0, 2, 7, 5)
# 光标: 两轴都压=斜向, 只压竖轴=上下, 只压横轴=左右
STAMP_AXIS_CURSORS = {(-1, -1): Qt.SizeFDiagCursor, (1, 1): Qt.SizeFDiagCursor,
                      (1, -1): Qt.SizeBDiagCursor, (-1, 1): Qt.SizeBDiagCursor,
                      (0, -1): Qt.SizeVerCursor, (0, 1): Qt.SizeVerCursor,
                      (-1, 0): Qt.SizeHorCursor, (1, 0): Qt.SizeHorCursor}



def stamp_handle_offsets(center, frame):
    """8 个手柄的本项局部坐标: 图心 + (半宽 u, 半高 v) 的 8 种组合, 与旋转一起转."""
    u, v = frame
    out = []
    for su, sv in STAMP_HANDLE_OFFSETS:
        out.append(QPointF(center.x() + u.x() * su + v.x() * sv,
                           center.y() + u.y() * su + v.y() * sv))
    return out


def stamp_handle_radius(index):
    """第 index 个手柄的基准半径(屏幕像素): 角上略大, 边中点略小, 便于区分."""
    return (STAMP_SCALE_CORNER_R if index in STAMP_HANDLE_CORNERS
            else STAMP_SCALE_EDGE_R)


def stamp_handle_cursor(index):
    """手柄光标: 按它压的是哪两条轴给(图上转了角度也仍是同一个手感)."""
    return STAMP_AXIS_CURSORS[STAMP_HANDLE_OFFSETS[index]]


def _point_near_segment(p, a, b, tol):
    """p 到线段 ab 的距离是否在 tol 内(旋转图标的连线命中)."""
    dx, dy = b.x() - a.x(), b.y() - a.y()
    length2 = dx * dx + dy * dy
    if length2 <= 1e-9:
        return math.hypot(p.x() - a.x(), p.y() - a.y()) <= tol
    t = ((p.x() - a.x()) * dx + (p.y() - a.y()) * dy) / length2
    t = max(0.0, min(1.0, t))
    return math.hypot(p.x() - (a.x() + t * dx),
                      p.y() - (a.y() + t * dy)) <= tol


# ---------------- 多边形标注项 ----------------

class AnnotationPolygonItem(_LabelChipMixin, _VertexHandleMixin,
                            QGraphicsPolygonItem):
    """场景坐标下的多边形标注(顶点即像素坐标). 与 BoxItem 共用 chip 渲染与配色."""

    HANDLE_SIZE = 8.0

    def __init__(self, points, label, editable=True, color=None, text=""):
        super().__init__()
        self.label = label
        self.editable = editable
        self.text = text
        self._color = color
        # points: [[x, y], ...](场景/像素坐标)
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
        # 浮动粘贴(未落地): 预览图 + 图左上角的局部坐标 + 落地参数(见 scene.commit_pastes)
        self.pending_img = None
        self.pending_anchor = None
        self.pending_meta = None
        # "显示标注"关掉时只藏轮廓、保留浮层图案(见 set_outline_visible)
        self._outline_hidden = False
        self._update_handles()

    def set_outline_visible(self, show):
        """
        "显示标注"开关: 浮动粘贴的图案还没写进图像像素, 这时候连图一起藏了
        就没法预览这一贴的效果, 所以有浮层的只藏轮廓(chip/顶点手柄/虚线).
        """
        show = bool(show)
        if self.pending_img is not None:
            # 轮廓一藏, 框线/手柄/图标都不再画: 边界跟着变小, 必须先通知场景
            self.prepareGeometryChange()
            self._outline_hidden = not show
            self.setVisible(True)
        else:
            self._outline_hidden = False
            self.setVisible(show)
        self.update()

    def is_floating(self):
        """浮动层: 图案还没写进图像像素, 这期间只能整体拖动, 不能拽顶点改形状."""
        return self.pending_img is not None

    def set_pending_stamp(self, img, anchor, meta):
        # 图案尺寸(缩放/换模板)直接决定边界大小, 换之前先让场景记住旧范围
        self.prepareGeometryChange()
        self.pending_img = img
        self.pending_anchor = QPointF(anchor)
        self.pending_meta = meta
        self.update()

    def clear_pending_stamp(self):
        self.prepareGeometryChange()
        self.pending_img = None
        self.pending_anchor = None
        self.pending_meta = None
        self.update()

    # ---------------- 浮动粘贴的旋转/缩放 ----------------
    def stamp_pivot(self):
        """旋转中心(本项局部坐标): 绕它转才能保证轮廓与图案不错位."""
        meta = self.pending_meta
        if meta is not None and meta.get("center") is not None:
            return QPointF(meta["center"])
        img, anchor = self.pending_img, self.pending_anchor
        if img is None or anchor is None:
            return QPointF(0.0, 0.0)
        return QPointF(anchor.x() + img.width() / 2.0,
                       anchor.y() + img.height() / 2.0)

    def stamp_frame_center(self):
        """缩放的基准点(本项局部坐标)= 当前轮廓外接框中心.

        不能用 meta["center"]: 那是"粘贴那一刻"的图心, 整体拖动或落地夹紧后
        会与轮廓中心差半个偏移, 拿它当缩放基准会让图心在缩放中漂移,
        进而让"鼠标到图心的距离比"对不上倍数.
        """
        return self.polygon().boundingRect().center()

    def stamp_scale(self):
        """浮动粘贴当前的缩放倍数(-1 表示此刻没有浮动层)."""
        meta = self.pending_meta
        if meta is None or self.pending_img is None:
            return -1.0
        return float(meta.get("scale", 1.0))

    def rotated_frame(self):
        """图案外接框按当前角度旋转后的 (半宽向量, 半高向量).

        8 个缩放手柄的位置与命中范围都从这里算: 转过角度后手柄还贴着图边走,
        而不是认死屏幕的正方向.
        半轴长度只能取自轮廓自身在"图自身朝向"下的跨度: pending_img 是按旋转后的
        包围盒裁出来的, 比图案本体大一圈(160x120 转 30° 会裁成 198x183), 拿它的
        width/height 算手柄, 8 个圆点就整圈浮在图外 —— 用户实测"手柄散落在空中".
        """
        meta = self.pending_meta
        if meta is None or self.pending_img is None:
            return None
        poly = self.polygon()
        if poly.isEmpty():
            return None
        a = math.radians(float(meta.get("angle", 0.0)))
        ca, sa = math.cos(a), math.sin(a)
        cen = self.stamp_frame_center()
        # u=(ca,sa) 是图的宽边方向, v=(-sa,ca) 是高边方向; 半轴 = 轮廓在两轴上的最大投影
        hw = max(abs((p.x() - cen.x()) * ca + (p.y() - cen.y()) * sa) for p in poly)
        hh = max(abs(-(p.x() - cen.x()) * sa + (p.y() - cen.y()) * ca) for p in poly)
        return (QPointF(hw * ca, hw * sa),          # 图的宽边方向
                QPointF(-hh * sa, hh * ca))         # 图的高边方向

    def stamp_frame_corners(self):
        """外接框 4 角的本项局部坐标(顺时针: 左上→右上→右下→左下), 没有浮动层时空列表.

        框线与 boundingRect 都按它算: 两处必须同源, 否则框线会被自己的边界裁掉一角.
        """
        frame = self.rotated_frame()
        if frame is None:
            return []
        pts = stamp_handle_offsets(self.stamp_frame_center(), frame)
        return [pts[i] for i in STAMP_FRAME_ORDER]

    def _stamp_frame_min_screen(self):
        """外接框短边的屏幕像素(没有浮动层时 None)."""
        frame = self.rotated_frame()
        if frame is None:
            return None
        u, v = frame
        k = max(self._view_scale(), 1e-6)
        return min(math.hypot(u.x(), u.y()), math.hypot(v.x(), v.y())) * 2.0 * k

    def stamp_handle_shrink(self):
        """手柄半径的收缩系数: 框越小圆点越小(下限 STAMP_HANDLE_MIN_FRAC).

        半径固定时, 缩小后的图案周围会被同样大的圆点糊满(用户实测"顶点也比较大").
        """
        min_px = self._stamp_frame_min_screen()
        if min_px is None:
            return 1.0
        return max(STAMP_HANDLE_MIN_FRAC, min(1.0, min_px / STAMP_HANDLE_FULL_PX))

    def stamp_handle_draw_radius(self, index):
        """第 index 个手柄画出来的半径(屏幕像素) = 基准半径 × 收缩系数."""
        return stamp_handle_radius(index) * self.stamp_handle_shrink()

    def stamp_handle_hit_radius(self, index):
        """命中半径(屏幕像素): 比画出来的略大, 小圆点才点得中."""
        return max(self.stamp_handle_draw_radius(index) + STAMP_SCALE_PAD,
                   STAMP_HANDLE_MIN_HIT)

    def stamp_handle_indices(self):
        """此刻该有哪些手柄: 框小到边中点没有信息量时只留 4 个角."""
        min_px = self._stamp_frame_min_screen()
        if min_px is not None and min_px < STAMP_EDGE_HANDLE_MIN_PX:
            return list(STAMP_HANDLE_CORNERS)
        return list(range(len(STAMP_HANDLE_OFFSETS)))

    def rotate_stamp_to(self, angle):
        """把浮动粘贴转到 angle 度(绕图心, 与 _paste_template 的坐标约定一致).

        拖动中只重画小图位图和轮廓: 图像像素绝不在这里碰, 要等 commit_pastes()
        才按 meta["angle"] 融合, 否则鼠标一动就是一次整图重采样.
        """
        meta = self.pending_meta
        scene = self.scene()
        if meta is None or self.pending_img is None or scene is None:
            return
        angle = float(angle)
        delta = angle - float(meta["angle"])
        if abs(delta) < 1e-9:      # Shift 吸附后常常是同一个角度, 白重算一遍不值
            return
        pivot = self.stamp_pivot()
        rotated = scene._rotate_points(
            [[p.x(), p.y()] for p in self.polygon()], pivot, delta)
        self.prepareGeometryChange()
        self.setPolygon(QPolygonF([QPointF(x, y) for x, y in rotated]))
        # 图心恒等于旋转中心: 位图重渲染后把锚点摆回图心, 轮廓与图案才不会错位
        meta["angle"] = angle
        self._refresh_stamp_bitmap(pivot)
        self._clamp_pos_into_image()
        self.update()

    def scale_stamp_to(self, scale):
        """把浮动粘贴等比缩放到 scale 倍(绕图心), 并同步位图与轮廓.

        基准取"轮廓外接框中心"而不是它的左上角: 轮廓点正是按它缩放的,
        换个基准点缩放会让外接框中心跟着漂, 图体就越缩越偏.
        与旋转同一条规矩: 当场只重排显示, 像素等 commit_pastes() 按 meta["scale"] 落地.
        """
        meta = self.pending_meta
        scene = self.scene()
        if meta is None or self.pending_img is None or scene is None:
            return
        scale = max(STAMP_SCALE_MIN, min(STAMP_SCALE_MAX, float(scale)))
        base = float(meta.get("scale", 1.0))
        if abs(scale - base) < 1e-9:
            return               # 夹住上下限之后常常是同一个倍数, 白重算一遍不值
        bounds = self.polygon().boundingRect()
        pivot = bounds.center()
        ratio = scale / base if base > 1e-9 else 1.0
        meta["scale"] = scale
        scaled = [[pivot.x() + (p.x() - pivot.x()) * ratio,
                   pivot.y() + (p.y() - pivot.y()) * ratio]
                  for p in self.polygon()]
        self.prepareGeometryChange()
        self.setPolygon(QPolygonF([QPointF(x, y) for x, y in scaled]))
        self._refresh_stamp_bitmap(pivot)
        self.update()

    def _refresh_stamp_bitmap(self, pivot):
        """按 meta 里的角度与倍数重新渲染图案, 并把它摆回图心."""
        meta = self.pending_meta
        scene = self.scene()
        if meta is None or scene is None or not hasattr(scene, "_stamp_patch"):
            return
        img = scene._stamp_patch(meta)
        self.pending_img = img
        self.pending_anchor = QPointF(pivot.x() - img.width() / 2.0,
                                      pivot.y() - img.height() / 2.0)

    # ---------------- 浮动粘贴手柄的命中/拖动(由 scene 手动驱动) ----------------
    # 位置全用本项局部坐标算(见 stamp_handle_offsets): 手柄就是本项 paint 画的圆点,
    # 视图缩放只影响画出来的直径, 不影响它在局部坐标里的位置, 于是命中与绘制同一把尺子.
    # 只有 scene 传进来的鼠标点是场景坐标, 命中前统一 mapFromScene 换算一次.
    def stamp_frame_visible(self):
        """浮动层的外框/手柄/图标此刻该不该画出来(与选中态无关).

        与选中态无关是必须的: boundingRect 要是跟着选中态一起缩, 取消选中时
        Qt 只重绘"变小之后"的范围, 刚消失的图标/手柄那块就没人擦, 留下残影
        (用户实测"旋转按钮消失得不彻底, 残留一部分弧线/圆点").
        """
        return self.pending_img is not None and not self._outline_hidden

    def stamp_handles_visible(self):
        return self.stamp_frame_visible() and self.isSelected()

    def stamp_handle_items(self):
        """(下标, 本项局部坐标) 列表: 画/命中/扩边界都按它走, 免得多处各筛一遍筛不一致."""
        if not self.stamp_frame_visible():
            return []
        frame = self.rotated_frame()
        if frame is None:
            return []
        pts = stamp_handle_offsets(self.stamp_frame_center(), frame)
        return [(i, pts[i]) for i in self.stamp_handle_indices()]

    def stamp_handle_points(self):
        """此刻该画的手柄的本项局部坐标列表(空列表 = 此刻没有手柄)."""
        return [p for _i, p in self.stamp_handle_items()]

    def stamp_handle_hit(self, scene_pos):
        """缩放手柄命中: 返回 (手柄下标, 按下时该手柄到图心的场景距离).

        传进来的是场景坐标, 而外接框算的是本项局部坐标: 图体拖动过(pos≠0)之后
        两者差一个 pos, 不换算就整圈点不中(拖动前恰好 pos=(0,0), 所以以前看不出).
        """
        if not self.stamp_handles_visible():
            return None
        pos = self.mapFromScene(scene_pos)
        cen = self.stamp_frame_center()
        # 圆点直径是按屏幕像素画的, 命中半径也要回到屏幕像素去比
        k = max(self._view_scale(), 1e-6)
        for i, p in self.stamp_handle_items():
            r = self.stamp_handle_hit_radius(i) / k
            if math.hypot(pos.x() - p.x(), pos.y() - p.y()) <= r:
                d = QPointF(p.x() - cen.x(), p.y() - cen.y())
                return i, math.hypot(d.x(), d.y())
        return None

    def stamp_rotate_icon(self):
        """旋转图标圆心的本项局部坐标(没有浮动层时返回 None).

        挂点是"小图自身顶边中点"(跟着角度一起转), 图标再沿同一朝向往外 GAP.
        GAP 与半径都是屏幕像素, 换算回局部尺度要除以 view 缩放; 小图时按固定 GAP 摆
        会正好压在顶边中点那个缩放手柄上(手柄优先级更高), 图标就点不着了,
        所以再兜一个下限: 离顶边中点至少隔开两个手柄的半径.
        """
        if not self.stamp_frame_visible():
            return None
        base = self._stamp_rotate_base()
        if base is None:
            return None
        meta = self.pending_meta
        a = math.radians(float(meta.get("angle", 0.0)))
        k = max(self._view_scale(), 1e-6)
        gap = max(STAMP_ROTATE_GAP,
                  STAMP_ROTATE_R + STAMP_ROTATE_PAD
                  + STAMP_SCALE_EDGE_R + STAMP_SCALE_PAD + 2.0) / k
        return QPointF(base.x() + math.sin(a) * gap, base.y() - math.cos(a) * gap)

    def _stamp_rotate_base(self):
        """图标连线在小图上的起点(自身顶边中点, 本项局部坐标).

        与手柄同一约定: 半轴 v 指"朝下", 所以顶边中点是 图心 - v(H_TM 正是这么摆的).
        """
        frame = self.rotated_frame()
        if frame is None:
            return None
        cen = self.stamp_frame_center()
        return QPointF(cen.x() - frame[1].x(), cen.y() - frame[1].y())

    def stamp_rotate_hit(self, scene_pos):
        """旋转图标命中: 圆点上或那根连线上都算(与绘制共用同一套局部坐标)."""
        if not self.stamp_handles_visible():
            return False
        icon = self.stamp_rotate_icon()
        base = self._stamp_rotate_base()
        if icon is None or base is None:
            return False
        pos = self.mapFromScene(scene_pos)    # 理由同 stamp_handle_hit
        k = max(self._view_scale(), 1e-6)
        if math.hypot(pos.x() - icon.x(),
                      pos.y() - icon.y()) <= (STAMP_ROTATE_R + STAMP_ROTATE_PAD) / k:
            return True
        return _point_near_segment(pos, base, icon, STAMP_ROTATE_PAD / k)

    def stamp_rotate_drag(self, scene_pos):
        """返回鼠标相对图心的方位角(度) - 旋转拖动按方位角增量累计."""
        cen = self.mapToScene(self.stamp_frame_center())
        return math.degrees(math.atan2(scene_pos.y() - cen.y(),
                                       scene_pos.x() - cen.x()))

    def press_stamp_scale(self, scene_pos):
        """按下某个缩放手柄: 记下起始倍数与起始距离, 之后每帧按距离比换算倍数."""
        hit = self.stamp_handle_hit(scene_pos)
        if hit is None:
            return None
        idx, dist = hit
        return {"kind": "scale", "idx": idx, "scale0": self.stamp_scale(),
                "dist0": dist, "cursor": stamp_handle_cursor(idx)}

    def drag_stamp_scale(self, scene_pos, scale0, dist0):
        """拖动中: 新倍数 = 鼠标到图心的距离 / 按下时的距离 × 按下时的倍数."""
        if dist0 <= 1e-6:
            return
        cen = self.mapToScene(self.polygon().boundingRect().center())
        factor = math.hypot(scene_pos.x() - cen.x(),
                            scene_pos.y() - cen.y()) / dist0
        self.scale_stamp_to(scale0 * factor)

    def _clamp_pos_into_image(self):
        """转完可能顶出图外(轮廓和图案都会被裁), 整体平移回来: 只挪 pos, 角度不动."""
        scene = self.scene()
        img_rect = getattr(scene, "image_rect", None) if scene is not None else None
        if img_rect is None:
            return
        r = self.polygon().boundingRect()
        pos = self.pos()
        x, y = pos.x(), pos.y()
        if x + r.left() < img_rect.left():
            x = img_rect.left() - r.left()
        if y + r.top() < img_rect.top():
            y = img_rect.top() - r.top()
        if x + r.right() > img_rect.right():
            x = img_rect.right() - r.right()
        if y + r.bottom() > img_rect.bottom():
            y = img_rect.bottom() - r.bottom()
        if x != pos.x() or y != pos.y():
            self.setPos(x, y)

    def shape_type(self):
        return "polygon"

    def points(self):
        """
        返回 [[x, y], ...](场景/像素坐标, 含 pos 偏移).
        拖动后保存必须叠加 pos, 否则关闭再打开位置丢失.
        """
        pos = self.pos()
        return [[p.x() + pos.x(), p.y() + pos.y()] for p in self.polygon()]

    def _chip_rect_local(self):
        """chip 点击区域, 锚定外接矩形中心, 尺寸按缩放换算(记忆化, 同矩形版)."""
        r = self.polygon().boundingRect()
        text = chip_text(self)
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

    # ---------------- 交互(拖动 + 图像范围限制)----------------
    def shape(self):
        """命中测试范围 = 多边形本体 + 标签 chip + 顶点手柄(选中且非浮动时).

        WindingFill 不能省: 默认奇偶填充下, chip(锚在外接框中心)与本体重叠的那块
        会互相抵消成"洞" —— 小图与浮动粘贴正好chip 盖满本体, 于是点在图上也判不中,
        事件根本落不到本项和它的子项(旋转图标/缩放手柄).
        """
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addPolygon(self.polygon())
        path.addRect(self._chip_rect_local())
        if self.isSelected() and not self.is_floating():
            for hrect in self._handles.values():
                path.addEllipse(hrect.adjusted(-3, -3, 3, 3))
        return path

    def _chip_hit_pad(self, base=3.0):
        """chip 命中扩展: 屏幕恒定像素换算回局部(与矩形一致, 防放大视图命中区膨胀)."""
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
            if self.isSelected() and not self.is_floating():
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

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            # 手柄/图标只画在选中态上, 但 boundingRect 不随选中态缩(见 boundingRect):
            # 这样这里 update() 才顺手把刚消失的图标/框线那块一起重绘掉, 不留残影
            self.update()
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
        """本项可能画到的全部像素范围(局部坐标): 必须覆盖 轮廓 ∪ 图案 ∪ 外接框线 ∪
        8 个手柄 ∪ 旋转图标 ∪ 图标连线.

        Qt 把 paint 裁到 boundingRect: 少一块就是"框线看不到"; 而且 Qt 的重绘范围
        取自当前 boundingRect, 所以这个范围还不能随选中态一起缩 —— 否则取消选中时
        刚消失的图标/手柄那圈没人擦, 留残影.
        """
        r = self.polygon().boundingRect()
        o = getattr(self, "_handle_size", self.HANDLE_SIZE)
        base = r.adjusted(-o, -o - 24, o, o + 24)
        if self.pending_img is not None and self.pending_anchor is not None:
            base = base.united(QRectF(self.pending_anchor,
                                      QSizeF(self.pending_img.width(),
                                             self.pending_img.height())))
        if not self.stamp_frame_visible():
            return base.united(self._chip_rect_local().adjusted(-o, -o, o, o))
        k = max(self._view_scale(), 1e-6)
        # 外接框线: 4 个角两两之间的线段, 用一个包住 4 角的矩形兜底(矩形是凸的)
        corners = self.stamp_frame_corners()
        if corners:
            fr = QRectF(corners[0], corners[0])
            for p in corners[1:]:
                fr = fr.united(QRectF(p, p))
            pad = (STAMP_FRAME_LINE_W + 2.0) / k
            base = base.united(fr.adjusted(-pad, -pad, pad, pad))
        for i, p in self.stamp_handle_items():
            reach = (self.stamp_handle_draw_radius(i) + 2.0) / k
            base = base.united(QRectF(p.x() - reach, p.y() - reach,
                                      2 * reach, 2 * reach))
        icon = self.stamp_rotate_icon()
        if icon is not None:
            reach = (STAMP_ROTATE_R + 2.0) / k
            base = base.united(QRectF(icon.x() - reach, icon.y() - reach,
                                      2 * reach, 2 * reach))
            base_pt = self._stamp_rotate_base()
            if base_pt is not None:
                # 连线中段可能落在"图体"和"图标"两个盒子之间: 补一个跨住两端的矩形
                seg = QRectF(base_pt, icon).normalized().adjusted(-1.0 / k, -1.0 / k,
                                                                 1.0 / k, 1.0 / k)
                base = base.united(seg)
        return base.united(self._chip_rect_local().adjusted(-o, -o, o, o))

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        if self.pending_img is not None:
            # 浮层图案只是预览, 图像像素此刻还没被改写
            scene = self.scene()
            clip = getattr(scene, "image_rect", None) if scene is not None else None
            painter.save()
            if clip is not None:
                painter.setClipRect(clip)
            painter.drawImage(self.pending_anchor, self.pending_img)
            painter.restore()
        if self._outline_hidden:
            return
        pen = QPen(self.pen())
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(self.brush())
        painter.drawPolygon(self.polygon())
        if self.pending_img is not None:
            # 虚线圈出范围: 还能拖, 还没落地
            dash = QPen(QColor(255, 255, 255, 210), 1.3)
            dash.setCosmetic(True)
            dash.setStyle(Qt.DashLine)
            painter.setPen(dash)
            painter.setBrush(Qt.NoBrush)
            painter.drawPolygon(self.polygon())

        label_rect = self._chip_rect_local()
        self._draw_label(painter, label_rect)

        if self.isSelected() and not self.is_floating():
            self._paint_vertex_handles(painter)
        elif self.stamp_handles_visible():
            self._paint_stamp_frame(painter)
            self._paint_stamp_handles(painter)
            self._paint_rotate_icon(painter)

    def _paint_stamp_frame(self, painter):
        """外接框线: 把 4 个角手柄连成一个旋转后的矩形, 手柄才有归属感.

        先描一层深色底再描主题色: 图案可能是亮的, 单描主题色在亮底上看不见
        (与工程里标注的描边风格一致). 线宽按屏幕像素恒定, 放大视图不会变粗带.
        """
        corners = self.stamp_frame_corners()
        if not corners:
            return
        k = max(self._view_scale(), 1e-6)
        poly = QPolygonF(corners)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(20, 22, 28, 190),
                            (STAMP_FRAME_LINE_W + 2.0) / k))
        painter.drawPolygon(poly)
        painter.setPen(QPen(theme.color("accent"), STAMP_FRAME_LINE_W / k))
        painter.drawPolygon(poly)

    def _paint_stamp_handles(self, painter):
        """缩放手柄: 位置是本项局部坐标, 直径按屏幕像素换算(与 chip 同一套做法).

        半径随外接框缩小(见 stamp_handle_shrink), 小图上才不会糊满一圈.
        直接在本项画而不是用带 ItemIgnoresTransformations 的子项: 那种子项在
        view 缩放后绘制落点跟算出来的坐标对不上, 点也点不中.
        """
        k = max(self._view_scale(), 1e-6)
        painter.setPen(QPen(theme.color("accent"), 1.4 / k))
        painter.setBrush(QBrush(QColor(255, 255, 255, 235)))
        for i, p in self.stamp_handle_items():
            r = self.stamp_handle_draw_radius(i) / k
            painter.drawEllipse(p, r, r)

    def _paint_rotate_icon(self, painter):
        """旋转图标 + 一根细连线: 位置/半径同样按屏幕像素换算成场景尺度."""
        icon = self.stamp_rotate_icon()
        base = self._stamp_rotate_base()
        if icon is None or base is None:
            return
        k = max(self._view_scale(), 1e-6)
        painter.setPen(QPen(QColor(255, 255, 255, 200), 1.2 / k))
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(base, icon)
        accent = theme.color("accent")
        painter.setPen(QPen(accent, 1.6 / k))
        painter.setBrush(QBrush(QColor(255, 255, 255, 235)))
        r = STAMP_ROTATE_R / k
        painter.drawEllipse(icon, r, r)
        self._paint_rotate_arrow(painter, icon, accent, k)

    @staticmethod
    def _paint_rotate_arrow(painter, center, color, k):
        """弧线加箭头才看得出是"转": 光一个圆点跟缩放手柄没区别."""
        r = STAMP_ROTATE_R * 0.58 / k
        rect = QRectF(center.x() - r, center.y() - r, 2 * r, 2 * r)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(color, 1.3 / k))
        painter.drawArc(rect, int(60 * 16), int(-270 * 16))
        # 箭头落在弧末端(150°), 指向顺时针的切线方向
        ang = math.radians(150.0)
        ex = center.x() + r * math.cos(ang)
        ey = center.y() - r * math.sin(ang)
        dx, dy = math.sin(ang) * 4.5 / k, math.cos(ang) * 4.5 / k
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawPolygon(QPolygonF([
            QPointF(ex + dx, ey + dy),
            QPointF(ex - dy * 3.0 / 4.5, ey + dx * 3.0 / 4.5),
            QPointF(ex + dy * 3.0 / 4.5, ey - dx * 3.0 / 4.5)]))

    def _draw_label(self, painter, label_rect):
        color = self._color if self._color is not None else label_color(self.label)
        painter.save()
        transform = painter.transform()
        scale = transform.m11() if abs(transform.m11()) > 1e-6 else 1.0
        painter.resetTransform()
        painter.setFont(_chip_font())
        text = chip_text(self)
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
