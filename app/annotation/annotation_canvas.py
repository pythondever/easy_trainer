# -*- coding: utf-8 -*-
"""标注画布: 视图行为注入、绘制驱动、参数面板与剪切板面板."""

import os
import re
from PySide6.QtCore import Qt, Signal, QPoint, QPointF, QTimer, QSize
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import (QColor, QPixmap, QKeySequence, QShortcut, QPen,
                           QPainter, QImage, QIcon, QCursor, QLinearGradient,
                           QFont)
from PySide6.QtWidgets import (QDialog, QWidget, QApplication, QVBoxLayout,
                               QHBoxLayout, QLabel, QGridLayout, QLineEdit,
                               QSpinBox, QPushButton, QFrame, QSlider, QMenu,
                               QGraphicsTextItem, QButtonGroup, QToolTip)


from app.annotation.scene import AnnotationScene
from app.annotation.box_item import AnnotationPolygonItem
from app.core import theme
from app.core.utils import project_root, ui_font_family
from app.widgets.dialog_buttons import add_ok_cancel
from app.widgets.message_box import MessageBox
from PySide6.QtWidgets import QGraphicsView


BLEND_STRENGTH_DEFAULT = "0.7"     # 粘贴融合力度: 0=原始硬贴, 1=完全融合
FILL_COLOR_DEFAULT = "#ffffff"     # 多边形右键"填充"用的默认颜色
ANGLE_RANGE_DEFAULT = (-180, 180)  # 粘贴时随机旋转的角度范围
BRIGHTNESS_DEFAULT = "0.50"        # 多边形亮度: 0.5=原样, 1=两倍, 0=全黑
BRIGHTNESS_THROTTLE_MS = 40        # 亮度拖动节流: 每刻度都算一遍纯属浪费, 像素由预览层承担

# 填充色点(黑 白 灰 红 橙 黄 绿 青 蓝 紫)
FILL_COLOR_PRESETS = (
    "#000000", "#ffffff", "#808080", "#ff0000", "#ff8c00",
    "#ffd400", "#22c55e", "#00c2d1", "#2f6bff", "#a855f7",
)
# 色名写法: 用户不必记色码, 打 "白" 或 "white" 都能认
_FILL_COLOR_ALIASES = {
    "black": "#000000", "white": "#ffffff", "gray": "#808080", "grey": "#808080",
    "red": "#ff0000", "orange": "#ff8c00", "yellow": "#ffd400", "green": "#22c55e",
    "cyan": "#00c2d1", "blue": "#2f6bff", "purple": "#a855f7", "magenta": "#ff00ff",
    "黑": "#000000", "白": "#ffffff", "灰": "#808080", "红": "#ff0000",
    "橙": "#ff8c00", "黄": "#ffd400", "绿": "#22c55e", "青": "#00c2d1",
    "蓝": "#2f6bff", "紫": "#a855f7",
}

# 全局粘贴剪切板: 软件重启才清空.
# 元素即 scene.fp_template 的结构(points/patch/w/h/label), 最新的在下标 0.
_clip_templates = []


def _parse_rgb(text):
    """认色名/ #RRGGBB / RRGGBB / #RGB / R,G,B / R G B, 认不出返回 None."""
    s = (text or "").strip()
    if not s:
        return None
    alias = _FILL_COLOR_ALIASES.get(s.lower().rstrip("色"))
    if alias:
        s = alias
    body = s[1:] if s.startswith("#") else s
    if re.fullmatch(r"[0-9a-fA-F]{6}", body):
        return tuple(int(body[i:i + 2], 16) for i in (0, 2, 4))
    if re.fullmatch(r"[0-9a-fA-F]{3}", body):
        return tuple(int(ch * 2, 16) for ch in body)
    parts = [p for p in re.split(r"[,\s]+", s) if p]
    if len(parts) != 3:
        return None
    try:
        rgb = [int(p) for p in parts]
    except ValueError:
        return None
    if any(v < 0 or v > 255 for v in rgb):
        return None
    return tuple(rgb)


def _fill_dot_qss(color, selected):
    # 尺寸必须写进按钮自身的 QSS: 全局 QDialog QPushButton{min-height} 会架空
    # setFixedSize 的下限, 且 QSS 尺寸按内容盒算, 16 + 边框 4 = 20
    return ("QPushButton {{ background-color: {0}; border: 2px solid {1};"
            " padding: 0; min-width: 16px; max-width: 16px;"
            " min-height: 16px; max-height: 16px; border-radius: 10px; }}"
            .format(color, "#ffffff" if selected else "transparent"))


def _resource_path(name):
    """resources/ 目录下资源绝对路径(不存在返回空串)."""
    root = project_root()
    p = os.path.join(root, "resources", name)
    return p if os.path.exists(p) else ""


def _upgrade_graphics_view(view):
    """
    给 uic 生成的 image_label_show(QGraphicsView) 挂上标注视图行为:
    挂 AnnotationScene + 安装滚轮缩放/中键平移/快捷键/右键菜单(复制·填充·粘贴)等方法.
    这里用实例补丁而非子类, 是因为 .ui 里 image_label_show 是原生 QGraphicsView,
    要在 Designer 里改成提升控件才能换成子类.
    """
    scene = AnnotationScene(view)
    view.setScene(scene)
    view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
    view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
    view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
    view.setDragMode(QGraphicsView.NoDrag)
    view.setMouseTracking(True)
    view.setFrameShape(QGraphicsView.NoFrame)
    view.setBackgroundBrush(QColor("#0e0f13"))
    view._panning = False
    view._last_pan_pos = None
    view._scene = scene
    view.scene_ = scene

    class _NoopSignal:
        def emit(self, *a, **k): pass
        def connect(self, *a, **k): pass
    view.zoom_changed = _NoopSignal()
    view.cursor_moved = _NoopSignal()
    orig_resize = view.resizeEvent

    def _on_resize(ev, _o=orig_resize, _v=view):
        try:
            _o(ev)
        except Exception:
            pass
        size = (_v.width(), _v.height())
        if _v.__dict__.get('_fit_size') != size:
            _v._fit_size = size
            if getattr(_v, '_scene', None) and _v._scene.image_rect is not None:
                QTimer.singleShot(0, _v.fit_window)
    view.resizeEvent = _on_resize
    orig_show = view.showEvent

    def _on_show(ev, _o=orig_show, _v=view):
        try: _o(ev)
        except Exception: pass
        QTimer.singleShot(0, _v.fit_window)
    view.showEvent = _on_show

    def _wheel(ev, _v=view):
        delta = ev.angleDelta().y()
        factor = 1.18 if delta > 0 else 1 / 1.18
        _v.scale(factor, factor)
        ev.accept()
    view.wheelEvent = _wheel

    def _press(ev, _v=view):
        if ev.button() == Qt.MiddleButton:
            _v._panning = True
            _v._last_pan_pos = ev.pos()
            _v.setCursor(Qt.ClosedHandCursor)
            ev.accept()
            return
        QGraphicsView.mousePressEvent(_v, ev)
    view.mousePressEvent = _press

    def _move(ev, _v=view):
        if _v._panning and _v._last_pan_pos is not None:
            delta = ev.pos() - _v._last_pan_pos
            _v._last_pan_pos = ev.pos()
            _v.horizontalScrollBar().setValue(_v.horizontalScrollBar().value() - delta.x())
            _v.verticalScrollBar().setValue(_v.verticalScrollBar().value() - delta.y())
            ev.accept()
            return
        # 剪切板预览虚线跟着鼠标走(画框/格式刷期间不跟, 免得和绘制预览打架)
        _scene = _v.scene()
        if getattr(_scene, "_stamp_ghost", None) is not None:
            if not getattr(_scene, "draw_mode", False) and _scene.fp_mode is None:
                _scene.update_stamp_ghost(_v.mapToScene(ev.pos()))
        QGraphicsView.mouseMoveEvent(_v, ev)
    view.mouseMoveEvent = _move

    def _release(ev, _v=view):
        if ev.button() == Qt.MiddleButton:
            _v._panning = False
            _v._last_pan_pos = None
            _v.setCursor(Qt.ArrowCursor)
            ev.accept()
            return
        QGraphicsView.mouseReleaseEvent(_v, ev)
    view.mouseReleaseEvent = _release

    def _key_press(ev, _v=view):
        if ev.key() == Qt.Key_Space:
            _v.setDragMode(QGraphicsView.ScrollHandDrag)
            ev.accept()
            return
        QGraphicsView.keyPressEvent(_v, ev)
    view.keyPressEvent = _key_press

    def _key_release(ev, _v=view):
        if ev.key() == Qt.Key_Space:
            _v.setDragMode(QGraphicsView.NoDrag)
            ev.accept()
            return
        QGraphicsView.keyReleaseEvent(_v, ev)
    view.keyReleaseEvent = _key_release

    def _ctx_menu(ev, _v=view):
        scene_pos = _v.mapToScene(ev.pos())
        scene = _v.scene()
        hit = scene.itemAt(scene_pos, _v.transform())
        # 仅多边形标注支持"复制"(矩形不出现该菜单); 删除标注用 Delete 键
        if isinstance(hit, AnnotationPolygonItem):
            menu = QMenu(_v)
            act_copy = menu.addAction(QC.translate("AnnotationDialog", "复制"))
            act_copy.triggered.connect(lambda: _v.window()._copy_template(hit))
            act_fill = menu.addAction(QC.translate("AnnotationDialog", "填充"))
            act_fill.triggered.connect(lambda: _do_fill(scene, hit))
            menu.exec(ev.globalPos())
            ev.accept()
            return
        # 空白处: 已有模板(复制过)可粘贴; 粘贴锚点=之前左键点击的空白位置
        if getattr(scene, "fp_template", None):
            # 粘贴位置 = 当前右键场景坐标(跟随鼠标, 不受滚动/缩放影响;
            # mapToScene 已是场景坐标, 缩放只改视图变换不改变场景坐标)
            menu = QMenu(_v)
            act_paste = menu.addAction(QC.translate("AnnotationDialog", "粘贴"))
            act_paste.triggered.connect(lambda: _do_paste(scene, scene_pos))
            menu.exec(ev.globalPos())
            ev.accept()
            return
        QGraphicsView.contextMenuEvent(_v, ev)
    view.contextMenuEvent = _ctx_menu

    def _do_paste(_scene, _pos):
        dialog = view.window()   # 顶层窗口 = AnnotationDialog
        _scene.angle_range = dialog._paste_angle_range()
        _scene._paste_template(_pos)

    def _do_fill(_scene, _item):
        """多边形填充: 把区域内像素改成"填充值"输入框的 RGB 颜色, 可 Ctrl+Z 撤销."""
        dialog = view.window()
        if _scene.fill_polygon(_item, dialog._fill_value()):
            dialog._dirty = True
            dialog._autosave_timer.start()

    def _zoom_level(_v=view):
        return _v.transform().m11()
    view._zoom_level = _zoom_level

    def _fit_window(_v=view):
        if _v._scene.image_rect is not None:
            _v.fitInView(_v._scene.image_rect, Qt.KeepAspectRatio)
    view.fit_window = _fit_window

    def _zoom_in(_v=view):
        _v.scale(1.18, 1.18)
    view.zoom_in = _zoom_in

    def _zoom_out(_v=view):
        _v.scale(1 / 1.18, 1 / 1.18)
    view.zoom_out = _zoom_out

    def _reset_zoom(_v=view):
        _v.resetTransform()
    view.reset_zoom = _reset_zoom
    QShortcut(QKeySequence.ZoomIn, view, activated=view.zoom_in)
    QShortcut(QKeySequence.ZoomOut, view, activated=view.zoom_out)
    QShortcut(QKeySequence("Ctrl+0"), view, activated=view.fit_window)
    return view


class _ClsLabelItem(QGraphicsTextItem):
    """图像分类数据集: 图像中央显示类别名, 点击弹出菜单修改类别(复用 label_change_requested)."""

    def __init__(self, text, color, font_size=15):
        super().__init__(text)
        self.label = text
        self.setDefaultTextColor(QColor(color) if color else QColor("white"))
        self.setFont(QFont(ui_font_family(), font_size, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene = self.scene()
            if scene is not None:
                scene.label_change_requested.emit(self)
                event.accept()
                return
        super().mousePressEvent(event)


class _HueSatPicker(QWidget):

    def __init__(self, value=255, on_change=None):
        super().__init__()
        self.setFixedSize(280, 180)
        self.setCursor(Qt.CrossCursor)
        self._value = value
        self._on_change = on_change
        self._hue = 219
        self._sat = 80
        self._bg = None
        self._build_bg()

    def _build_bg(self):
        img = QImage(self.width(), self.height(), QImage.Format_RGB32)
        p = QPainter(img)
        h = self.height()
        for x in range(self.width()):
            hue = int(x / self.width() * 359)
            grad = QLinearGradient(0, 0, 0, h)
            grad.setColorAt(0, QColor.fromHsv(hue, 255, self._value))
            grad.setColorAt(1, QColor.fromHsv(hue, 0, self._value))
            p.fillRect(x, 0, 1, h, grad)
        p.end()
        self._bg = QPixmap.fromImage(img)
        self.update()

    def set_value(self, value):
        if value != self._value:
            self._value = value
            self._build_bg()

    def set_color(self, c):
        self._hue = max(0, c.hue())
        self._sat = c.saturation()
        self.update()

    def _pos_to_color(self, pos):
        hue = int(max(0, min(1, pos.x() / self.width())) * 359)
        sat = int((1 - max(0, min(1, pos.y() / self.height()))) * 255)
        return QColor.fromHsv(hue, sat, self._value)

    def mousePressEvent(self, ev):
        self._on_change(self._pos_to_color(ev.pos()))

    def mouseMoveEvent(self, ev):
        if ev.buttons() & Qt.LeftButton:
            self._on_change(self._pos_to_color(ev.pos()))

    def paintEvent(self, ev):
        p = QPainter(self)
        p.drawPixmap(0, 0, self._bg)
        x = self._hue / 359 * self.width()
        y = (1 - self._sat / 255) * self.height()
        p.setPen(QPen(QColor("#ffffff"), 1.5))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(x, y), 5, 5)


class SwitchButton(QWidget):

    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(36, 20)
        self.setCursor(Qt.PointingHandCursor)
        self._checked = True

    def isChecked(self):
        return self._checked

    def setChecked(self, v):
        v = bool(v)
        if v != self._checked:
            self._checked = v
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.isEnabled():
                return
            self._checked = not self._checked
            self.toggled.emit(self._checked)
            self.update()
            event.accept()
            return
        super().mousePressEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        track = theme.color("accent") if self._checked else theme.color("border_strong")
        p.setPen(Qt.NoPen)
        p.setBrush(track)
        p.drawRoundedRect(0, 0, 36, 20, 10, 10)
        p.setBrush(QColor("#ffffff"))
        cx = 18 if self._checked else 2
        p.drawEllipse(cx, 2, 16, 16)


class ColorPickerDialog(QDialog):

    BASIC_COLORS = [
        "#FF0000", "#00FF00", "#0000FF", "#FFFF00",
        "#00FFFF", "#FF00FF", "#000000", "#FFFFFF",
        "#808080", "#C0C0C0", "#FF8800", "#8800FF",
    ]

    def __init__(self, initial=theme.color("accent"), parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("选择颜色"))
        self._color = QColor(initial) if initial.isValid() else theme.color("accent")

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(18, 16, 18, 14)

        top = QHBoxLayout()
        self._preview = QFrame()
        self._preview.setFixedSize(80, 48)
        top.addWidget(self._preview)
        html_box = QVBoxLayout()
        html_box.addWidget(QLabel(self.tr("十六进制:")))
        self._html_edit = QLineEdit()
        self._html_edit.setMaximumWidth(160)
        self._html_edit.textChanged.connect(self._on_html_changed)
        html_box.addWidget(self._html_edit)
        top.addLayout(html_box)
        top.addStretch(1)
        layout.addLayout(top)
        # 可视化取色面板(点击选色)+ 明度滑块
        picker_row = QHBoxLayout()
        self._picker = _HueSatPicker(value=self._color.value(), on_change=self._set_color)
        picker_row.addWidget(self._picker)
        self._value_slider = QSlider(Qt.Vertical)
        self._value_slider.setRange(0, 255)
        self._value_slider.setValue(self._color.value())
        self._value_slider.setFixedHeight(180)
        self._value_slider.valueChanged.connect(self._on_value_changed)
        picker_row.addWidget(self._value_slider)
        picker_row.addStretch(1)
        layout.addLayout(picker_row)

        layout.addWidget(QLabel(self.tr("基本颜色:")))
        grid = QGridLayout()
        grid.setSpacing(6)
        for i, c in enumerate(self.BASIC_COLORS):
            btn = QPushButton()
            btn.setFixedSize(32, 32)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("QPushButton { background: %s; border: 1px solid " + theme.hexof("border_strong") + "; border-radius: 3px; }" % c)
            btn.clicked.connect(lambda checked=False, _c=c: self._set_color(QColor(_c)))
            grid.addWidget(btn, i // 6, i % 6)
        layout.addLayout(grid)

        layout.addWidget(QLabel(self.tr("自定义 RGB:")))
        rgb = QHBoxLayout()
        self._r_edit = QSpinBox()
        self._g_edit = QSpinBox()
        self._b_edit = QSpinBox()
        for s, lab in [(self._r_edit, "R:"), (self._g_edit, "G:"), (self._b_edit, "B:")]:
            s.setRange(0, 255)
            s.setFixedWidth(90)
            s.valueChanged.connect(self._on_rgb_changed)
            rgb.addWidget(QLabel(lab))
            rgb.addWidget(s)
        rgb.addStretch(1)
        layout.addLayout(rgb)

        btns = QHBoxLayout()
        btns.addStretch(1)
        add_ok_cancel(btns, self.accept, self.reject)
        layout.addLayout(btns)

        self._update_widgets_from_color()

    def _update_widgets_from_color(self):
        c = self._color
        self._preview.setStyleSheet(
            "QFrame { background: %s; border: 1px solid " + theme.hexof("border_strong") + "; border-radius: 4px; }" % c.name())
        self._html_edit.blockSignals(True)
        self._html_edit.setText(c.name())
        self._html_edit.blockSignals(False)
        for s, v in [(self._r_edit, c.red()), (self._g_edit, c.green()), (self._b_edit, c.blue())]:
            s.blockSignals(True)
            s.setValue(v)
            s.blockSignals(False)
        self._picker.set_color(c)
        self._picker.set_value(c.value())
        self._value_slider.blockSignals(True)
        self._value_slider.setValue(c.value())
        self._value_slider.blockSignals(False)

    def _set_color(self, c):
        if not c.isValid():
            return
        self._color = QColor(c)
        self._update_widgets_from_color()

    def _on_value_changed(self, v):
        self._picker.set_value(v)
        self._set_color(QColor.fromHsv(self._picker._hue, self._picker._sat, v))

    def _on_html_changed(self, text):
        text = text.strip()
        if not text.startswith("#"):
            text = "#" + text
        c = QColor(text)
        if c.isValid():
            self._set_color(c)

    def _on_rgb_changed(self):
        c = QColor(self._r_edit.value(), self._g_edit.value(), self._b_edit.value())
        if c.isValid() and c != self._color:
            self._set_color(c)

    def selected_color(self):
        return self._color

    @staticmethod
    def get_color(initial=QColor("#4f7dff"), parent=None):
        dlg = ColorPickerDialog(initial, parent)
        if dlg.exec() == QDialog.Accepted:
            return dlg.selected_color()
        return QColor()


# 文案 context 统一写 AnnotationDialog: self.tr 取的是实例真实类名, 换一个译文就对不上
class AnnotationCanvasMixin:
    def _normalize_blend_strength(self):
        """失焦时把融合强度收敛到 [0,1]; 空值/非法值回到默认."""
        edit = self.ui.blend_strength_lineEdit
        try:
            v = float(edit.text().strip())
        except ValueError:
            v = float(BLEND_STRENGTH_DEFAULT)
        v = min(1.0, max(0.0, v))
        edit.setText("{:.2f}".format(v))
        slider = self.ui.blend_slider
        slider.blockSignals(True)
        slider.setValue(int(round(v * 100)))
        slider.blockSignals(False)
        scene = getattr(self, "scene", None)
        if scene is not None:
            scene.blend_strength = v

    def _on_blend_slider(self, value):
        self.ui.blend_strength_lineEdit.setText("{:.2f}".format(value / 100.0))
        self._normalize_blend_strength()

    def _sync_brightness_slider(self):
        """输入框同步到滑块(不碰图像); 空值/非法值回默认, 返回收敛后的值."""
        edit = self.ui.brightness_lineEdit
        try:
            v = float(edit.text().strip())
        except ValueError:
            v = float(BRIGHTNESS_DEFAULT)
        v = min(1.0, max(0.0, v))
        edit.setText("{:.2f}".format(v))
        slider = self.ui.brightness_slider
        slider.blockSignals(True)
        slider.setValue(int(round(v * 100)))
        slider.blockSignals(False)
        return v

    def _normalize_brightness(self):
        self._apply_brightness(self._sync_brightness_slider())
        self._commit_brightness()

    def _on_brightness_slider(self, value):
        v = min(1.0, max(0.0, value / 100.0))
        self.ui.brightness_lineEdit.setText("{:.2f}".format(v))
        self._bright_pending = v
        timer = getattr(self, "_bright_timer", None)
        if timer is None:
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.setInterval(BRIGHTNESS_THROTTLE_MS)
            timer.timeout.connect(self._flush_brightness)
            self._bright_timer = timer
        if not timer.isActive():
            # 第一格立刻画, 之后攒到节流窗口结束: 起手不滞后, 拖动也不会把事件堆起来
            self._flush_brightness()
            timer.start()

    def _flush_brightness(self):
        """把节流窗口内攒下的最后一个值画到预览层."""
        v = getattr(self, "_bright_pending", None)
        self._bright_pending = None
        if v is not None:
            self._apply_brightness(v)

    def _apply_brightness(self, v):
        """把亮度画到选中多边形的预览层(像素等落定才写); 没选中或选中的是矩形就提示一下."""
        item = self.scene.selected_item() if self.scene is not None else None
        if item is None:
            QToolTip.showText(QCursor.pos(), QC.translate("AnnotationDialog", "先在画布上点选一个多边形"))
            return
        if not self.scene.set_polygon_brightness(item, v):
            QToolTip.showText(QCursor.pos(), QC.translate("AnnotationDialog", "亮度调节只对多边形有效"))

    def _commit_brightness(self):
        """
        亮度改完落定: 把攒下的值和预览层一起写进图像像素, 再只刷新图像缓存.
        不设 _pix_unsaved 也不启动 150ms 自动保存: 后者会让"松手后随手画个框"触发的
        自动保存把亮度一起写掉, 等于拖一下就写一次盘; 真正写盘统一等 _save_current
        里用户显式保存的那一次.
        """
        timer = getattr(self, "_bright_timer", None)
        if timer is not None:
            timer.stop()
        self._flush_brightness()
        scene = getattr(self, "scene", None)
        if scene is None or not scene.commit_brightness():
            return
        if not (0 <= self.index < len(self.image_list)):
            return
        pix = scene.image_item.pixmap()
        if pix is None or pix.isNull():
            return
        self._put_pix_cache(self.image_list[self.index], pix)
        self._bright_unsaved = True
        self._dirty = True

    def _set_fill_color(self, value):
        """填充色唯一入口: 色名/十六进制/三通道都从这里过, 保证文本框/色块/色点三处一致."""
        rgb = _parse_rgb(value) or _parse_rgb(FILL_COLOR_DEFAULT)
        self.ui.fill_color_lineEdit.setText("#{:02x}{:02x}{:02x}".format(*rgb))
        self._sync_fill_color_btn()

    def _normalize_fill_color(self):
        """失焦时把颜色文本规范成 #rrggbb; 解析不了回默认."""
        self._set_fill_color(self.ui.fill_color_lineEdit.text())

    def _sync_fill_color_btn(self):
        name = "#{:02x}{:02x}{:02x}".format(*self._fill_value())
        self.ui.fill_color_btn.setStyleSheet("background-color: {0};".format(name))
        for dot, color in zip(self._fill_dot_btns, FILL_COLOR_PRESETS):
            dot.setStyleSheet(_fill_dot_qss(color, color.lower() == name))

    def _pick_fill_color(self):
        color = ColorPickerDialog.get_color(QColor(*self._fill_value()), self)
        if color.isValid():
            self._set_fill_color(color.name())

    def _fill_value(self):
        """当前填充颜色 (r, g, b), 供 scene.fill_polygon 使用."""
        return (_parse_rgb(self.ui.fill_color_lineEdit.text())
                or _parse_rgb(FILL_COLOR_DEFAULT))

    def _toggle_params_panel(self):
        panel = self.ui.paramsPanel
        # 用 isHidden 而不是 isVisible: 窗口最小化时后者也是 False, 会把"再点一次收起"变成"又展开"
        if not panel.isHidden():
            panel.hide()
            return
        panel.show()
        self._place_params_panel()
        panel.raise_()

    def _hide_params_panel(self):
        self.ui.paramsPanel.hide()

    def _hit_params_area(self, gpos):
        """落点在弹层或"设置"按钮上就不算点了别处."""
        for w in (self.ui.paramsPanel, self.ui.settings_btn):
            if w.isVisible() and w.rect().contains(w.mapFromGlobal(gpos)):
                return True
        return False

    def _place_params_panel(self):
        """右边缘对齐"设置"按钮, 顶边压在工具条下沿."""
        u = self.ui
        hint = u.paramsPanel.sizeHint()
        at = u.settings_btn.mapTo(self, QPoint(0, 0))
        x = at.x() + u.settings_btn.width() - hint.width()
        u.paramsPanel.setGeometry(max(8, min(x, self.width() - hint.width() - 8)),
                                  at.y() + u.settings_btn.height() + 6,
                                  hint.width(), hint.height())

    def _reset_params(self):
        u = self.ui
        u.min_ange_lineEdit.setText(str(ANGLE_RANGE_DEFAULT[0]))
        u.max_ange_lineEdit.setText(str(ANGLE_RANGE_DEFAULT[1]))
        u.blend_strength_lineEdit.setText(BLEND_STRENGTH_DEFAULT)
        self._normalize_blend_strength()
        u.brightness_lineEdit.setText(BRIGHTNESS_DEFAULT)
        self._sync_brightness_slider()
        self.scene.drop_brightness()
        self._set_fill_color(FILL_COLOR_DEFAULT)

    def _apply_draw_mode_cursor(self):
        """按当前画模式状态同步 view 光标(多边形画笔/矩形十字 / 编辑模式恢复)."""
        # 先清空全局 override 光标栈残留, 再按状态 push, 保证不泄漏(否则 ESC 退不出)
        self._clear_override_cursor()
        if self.scene.draw_mode:
            self._apply_draw_cursor()
        else:
            self.view.unsetCursor()

    def _clear_override_cursor(self):
        """
        清空全局 override 光标栈(画模式/格式刷期间可能多次 push 未配对).
        栈空时 restoreOverrideCursor 是无副作用的 no-op, 循环调用安全.
        """
        for _ in range(8):
            QApplication.restoreOverrideCursor()

    def _update_draw_buttons(self):
        """无标签或未选中标签时禁用矩形/多边形/格式刷按钮."""
        if self.cls_mode or self.textline_mode:
            # 分类只读看图; 字条模式整张图就是一行字, 没有可画的东西
            for w in (self.ui.draw_rect_btn, self.ui.poly_btn):
                w.setEnabled(False)
            return
        can_draw = (bool(self.label_colors)
                    and self.scene.current_label in self.label_colors)
        self.ui.draw_rect_btn.setEnabled(can_draw)
        self.ui.poly_btn.setEnabled(can_draw)
        if not can_draw:
            self._set_draw_button_states(False)

    def _start_draw(self, shape):
        self._hide_params_panel()
        if self.scene.fp_mode is not None:
            self.scene.set_format_painter(False)
        self.scene.stop_stamp_ghost()
        self.scene.set_draw_mode(True, shape)
        self._apply_draw_cursor()
        self._set_draw_button_states(True)
        if not self.label_colors:
            MessageBox.information(
                self, QC.translate("AnnotationDialog", "添加标签"),
                QC.translate("AnnotationDialog", "请先添加标签(点击\"+\")"))

    def _apply_draw_cursor(self):
        """多边形=画笔光标, 矩形=十字; override 保证不被 item 光标覆盖."""
        QApplication.restoreOverrideCursor()
        if self.scene.draw_shape == "polygon":
            cur = self._pen_cursor()
        else:
            cur = Qt.CrossCursor
        QApplication.setOverrideCursor(cur)

    def _set_draw_button_states(self, drawing):
        """激活态用 QSS 动态属性控制, 对应 QSS 内 [drawActive="true"] 规则."""
        draw_shape = self.scene.draw_shape if drawing else None
        for btn, name in ((self.ui.draw_rect_btn, "rect"),
                          (self.ui.poly_btn, "polygon")):
            active = draw_shape == name
            btn.setProperty("drawActive", "true" if active else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_box_drawn(self, item=None):
        """画完一个框: 保持画模式(需求: 只有 ESC 才退出), 维持对应光标与按钮高亮."""
        self._apply_draw_cursor()
        self._set_draw_button_states(True)

    def _cancel_draw_mode(self):
        """主动退出画模式(不创建标注): 恢复光标 + 按钮样式; 顺带收掉剪切板预览虚线."""
        if self.scene.fp_mode is not None:
            self.scene.set_format_painter(False)
        self._cancel_stamp_ghost()
        self.scene.set_draw_mode(False)
        self.scene._cancel_polygon()
        self._clear_override_cursor()
        self.view.unsetCursor()
        self._set_draw_button_states(False)

    # ---------------- 复制/粘贴(格式刷改造: 右键复制多边形 + 随机旋转粘贴) ----------------
    def _toggle_show_boxes(self, checked):
        """"显示标注"开关: 关闭时隐藏标注轮廓, 右侧列表信息保留."""
        self.scene.set_annotations_visible(checked)
        self.scene.invalidate()

    def _paste_angle_range(self):
        """角度范围输入框解析成 (lo, hi); 空/非整数回默认."""
        try:
            lo = int(self.ui.min_ange_lineEdit.text())
        except (ValueError, TypeError):
            lo = ANGLE_RANGE_DEFAULT[0]
        try:
            hi = int(self.ui.max_ange_lineEdit.text())
        except (ValueError, TypeError):
            hi = ANGLE_RANGE_DEFAULT[1]
        return lo, hi

    def _cancel_stamp_ghost(self):
        """收掉剪切板预览虚线并取消缩略图选中, 回到普通鼠标模式."""
        self.scene.stop_stamp_ghost()
        self.scene.fp_template = None
        btn = None
        if (self._clip_current is not None
                and 0 <= self._clip_current < len(self._clip_btns)):
            btn = self._clip_btns[self._clip_current]
        if btn is not None and btn.isChecked():
            # 互斥组里没法直接取消选中, 临时解开再勾回去
            self._clip_group.setExclusive(False)
            btn.setChecked(False)
            self._clip_group.setExclusive(True)
        self._clip_current = None
        self._update_clip_label()

    # ---------------- 剪切板缩略图(全局粘贴模板) ----------------
    CLIP_W, CLIP_H = theme.CLIP_THUMB_W + 4, theme.CLIP_THUMB_H + 4
    CLIP_ROWS = 3   # 剪切板可视行数, 超出后滚动

    def _copy_template(self, item):
        """右键"复制"入口: 抠模板入全局剪切板并选中最新缩略图."""
        if not self.scene.copy_template_from_item(item):
            return
        _clip_templates.insert(0, dict(self.scene.fp_template))
        self._rebuild_clipboard(select=0)

    def _setup_clipboard(self):
        u = self.ui
        u.clipboard_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        u.clipboard_scroll.setMinimumHeight(
            self.CLIP_ROWS * (self.CLIP_H + 6))
        for w in (u.clipboard_container, u.clipboard_scroll,
                  u.clipboard_scroll.viewport()):
            w.setContextMenuPolicy(Qt.CustomContextMenu)
            w.customContextMenuRequested.connect(lambda _p: self._clip_menu(None))
        self._clip_group = QButtonGroup(self)
        self._clip_group.setExclusive(True)
        self._clip_group.idClicked.connect(self._on_clip_id)
        self._clip_btns = []
        self._clip_current = None
        self._rebuild_clipboard(select=0 if _clip_templates else None)

    def _update_clip_label(self):
        cur = self._clip_current + 1 if self._clip_current is not None else 0
        self.ui.clipboard_label.setText(
            QC.translate("AnnotationDialog", "剪切板  {}/{}").format(cur, len(_clip_templates)))

    def _rebuild_clipboard(self, select=None):
        """按全局剪切板重建缩略图; select=选中下标(None=无选中)."""
        self.scene.stop_stamp_ghost()
        layout = self.ui.clipboard_layout
        while layout.count():
            w = layout.takeAt(0).widget()
            if w is not None:
                self._clip_group.removeButton(w)
                # 先摘掉父控件: deleteLater 要等事件循环空闲才真销毁,
                # 不摘的话旧缩略图会在原位多画一帧(重建时表现为残影)
                w.setParent(None)
                w.deleteLater()
        self._clip_btns = []
        self._clip_current = None
        for i, t in enumerate(_clip_templates):
            btn = QPushButton(self.ui.clipboard_container)
            btn.setObjectName("clipThumb")
            btn.setCheckable(True)
            btn.setFixedSize(self.CLIP_W, self.CLIP_H)
            icon = QIcon(QPixmap.fromImage(t["patch"]))
            btn.setIcon(icon)
            btn.setIconSize(QSize(self.CLIP_W - 8, self.CLIP_H - 8))
            btn.setToolTip(
                QC.translate("AnnotationDialog", "第 {} 个模板  {}x{}\n左键选中用于粘贴, "
                        "右键 删除/导入/导出/清空").format(i + 1, t["w"], t["h"]))
            btn.setContextMenuPolicy(Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(
                lambda _pos, b=btn: self._clip_menu(b))
            self._clip_group.addButton(btn, i)
            self.ui.clipboard_layout.addWidget(btn, 0, Qt.AlignHCenter)
            self._clip_btns.append(btn)
        if select is not None and _clip_templates:
            select = max(0, min(select, len(_clip_templates) - 1))
            self._clip_btns[select].setChecked(True)
            self._clip_current = select
            self._apply_clip_template(select)
        self._update_clip_label()

    def _on_clip_id(self, i):
        self._clip_current = i
        self._update_clip_label()
        self._apply_clip_template(i)

    def _apply_clip_template(self, i):
        t = _clip_templates[i]
        # 先退出画笔态(会把 fp_template 清掉)再换模板
        if self.scene.fp_mode is not None:
            self.scene.set_format_painter(False)
        self.scene.fp_template = t
        self.scene.angle_range = self._paste_angle_range()
        self.scene.start_stamp_ghost()

    def _clip_menu(self, btn):
        i = self._clip_btns.index(btn) if btn is not None else -1
        menu = QMenu(self)
        act_del = menu.addAction(QC.translate("AnnotationDialog", "删除")) if i >= 0 else None
        if act_del is not None:
            menu.addSeparator()
        act_imp = menu.addAction(QC.translate("AnnotationDialog", "导入"))
        act_exp = menu.addAction(QC.translate("AnnotationDialog", "导出"))
        menu.addSeparator()
        act_clr = menu.addAction(QC.translate("AnnotationDialog", "清空"))
        if not _clip_templates:
            act_exp.setEnabled(False)
            act_clr.setEnabled(False)
        act = menu.exec(QCursor.pos())
        if act is None:
            return
        if act is act_del:
            was_current = self.scene.fp_template is _clip_templates[i]
            _clip_templates.pop(i)
            # 删掉的正是当前粘贴模板且剪切板已空时才置空; 手绘轨迹模板不在剪切板, 不受影响
            if was_current and not _clip_templates:
                self.scene.fp_template = None
            self._rebuild_clipboard(select=0 if _clip_templates else None)
        elif act is act_imp:
            self._clip_import()
        elif act is act_exp:
            self._clip_export()
        elif act is act_clr:
            cur = self.scene.fp_template
            if cur is not None and any(cur is t for t in _clip_templates):
                self.scene.fp_template = None
            _clip_templates.clear()
            self._rebuild_clipboard(select=None)

    def _undo_fp_paste(self):
        """Ctrl+Z: 撤浮动粘贴或最后一次像素改动(粘贴/填充)."""
        if self.scene.undo_last_paste():
            self._refresh_labeled_list()

    @staticmethod
    def _pen_cursor():
        """画笔光标 28px, 热点=笔尖(3,25)."""
        pm = QPixmap(_resource_path("画笔.png"))
        if not pm.isNull() and pm.width() > 28:
            pm = pm.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QCursor(pm, 3, 25) if not pm.isNull() else Qt.CrossCursor

