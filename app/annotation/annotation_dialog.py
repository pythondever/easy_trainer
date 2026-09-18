# -*- coding: utf-8 -*-
"""
标注对话框: 封装 ui/annotation.py + annotation 引擎.
- 矩形/多边形标注(颜色 = 标签颜色, 支持中文标签)
- 左侧标签列表(点击切换当前标签), 添加标签弹窗(10 默认色 + 自定义色 + 跨数据集导入)
- A/D 切换上一张/下一张, 切换/关闭时保存 labelme json(图像同路径)
"""
import os
import json
import re
import shutil
from functools import lru_cache
from PIL import Image
from PySide6.QtCore import (Qt, Signal, QPoint, QPointF, QTimer, QSize, QThread,
                            QMutex, QMutexLocker, QEvent)
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import (QColor, QPixmap, QKeySequence, QShortcut, QPen,
                           QPainter, QImage, QIcon, QCursor, QLinearGradient,
                           QFont, QImageReader, QIntValidator, QDoubleValidator)
from PySide6.QtWidgets import (QDialog, QWidget, QApplication, QVBoxLayout,
                               QHBoxLayout, QLabel, QMessageBox,
                               QGridLayout, QLineEdit, QSpinBox, QPushButton, QFrame,
                               QSlider, QMenu, QGraphicsTextItem, QButtonGroup,
                               QFileDialog, QToolTip)

from ui.annotation import Ui_annotationDialog as AnnotationUI
from ui.add_label import Ui_addLabelDialog as AddLabelUI

from app.annotation.scene import AnnotationScene
from app.annotation.box_item import (AnnotationBoxItem, AnnotationPolygonItem,
                                     LABEL_COLORS, assign_label_color, label_color)
from app.core.label_utils import (label_sort_key, load_json_shapes,
                                  load_yolo_shapes, normalize_label,
                                  same_dir_json, shapes_to_boxes,
                                  shapes_to_labelme_json)
from app.core.utils import project_root, ui_font_family
from app.widgets.dialog_buttons import (apply_icon, add_ok_cancel,
                                        _icon_path, _tinted)
from app.widgets.message_box import MessageBox, ProgressDialog
from app.core.log import write_log
from PySide6.QtWidgets import QGraphicsView


BLEND_STRENGTH_DEFAULT = "0.7"     # 粘贴融合力度: 0=原始硬贴, 1=完全融合
FILL_COLOR_DEFAULT = "#ffffff"     # 多边形右键"填充"用的默认颜色
ANGLE_RANGE_DEFAULT = (-180, 180)  # 粘贴时随机旋转的角度范围
BRIGHTNESS_DEFAULT = "0.50"        # 多边形亮度: 0.5=原样, 1=两倍, 0=全黑

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


def _patch_local_points(t):
    """转为 patch 局部坐标, 原点取顶点外接框左上角(不是 png 的 0,0)."""
    pts = t.get("points") or []
    if not pts:
        return []
    minx = min(float(p[0]) for p in pts)
    miny = min(float(p[1]) for p in pts)
    return [[round(float(x) - minx, 2), round(float(y) - miny, 2)]
            for x, y in pts]


def _json_image_size(png_path):
    """读不到返回 (0, 0)."""
    try:
        with open(os.path.splitext(png_path)[0] + ".json", "r",
                  encoding="utf-8") as f:
            data = json.load(f)
        return int(data.get("imageWidth") or 0), int(data.get("imageHeight") or 0)
    except Exception:
        return 0, 0


def _fit_points_to_patch(pts, png_path, patch):
    """json 与 png 尺寸不一致时按比例换算."""
    jw, jh = _json_image_size(png_path)
    if jw > 0 and jh > 0 and (jw != patch.width() or jh != patch.height()):
        sx, sy = patch.width() / jw, patch.height() / jh
        return [[float(x) * sx, float(y) * sy] for x, y in pts]
    return [[float(x), float(y)] for x, y in pts]


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


# 左右两个列表行的高亮底色(左侧标签列表 / 右侧标注列表同款)
ROW_BG_SELECTED = "#2a3f6b"
ROW_BG_NORMAL = "#23262f"
_ROW_QSS = "QFrame {{ background: {0}; border-radius: 6px; }}"


@lru_cache(maxsize=128)
def _dot_icon(color):
    """
    标签颜色圆点图标. 按颜色缓存: 右侧标注列表每行取一次, 不缓存时
    每次刷新都要 new QPixmap + QPainter + QIcon, 框多时是卡顿主因之一.
    """
    pm = QPixmap(16, 16)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(color))
    p.drawEllipse(2, 2, 12, 12)
    p.end()
    return QIcon(pm)


def _set_row_background(row, selected):
    """
    列表行高亮. 已是目标底色就跳过 - setStyleSheet 会触发整行
    unpolish/polish 重绘, 上千行全量重设是标注卡顿的主因.
    """
    if row is None:
        return
    want = ROW_BG_SELECTED if selected else ROW_BG_NORMAL
    try:
        if getattr(row, "_row_bg", None) == want:
            return
        row._row_bg = want
        row.setStyleSheet(_ROW_QSS.format(want))
    except RuntimeError:
        pass    # 行已被 deleteLater 回收, 忽略


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


def _load_labelme(json_path):
    """
    读取 labelme json → [{label, x1,y1,x2,y2} 或 {label, points, shape_type}].
    解析统一走 label_utils.load_json_shapes, 这里只转成场景要的字典形态.
    """
    return shapes_to_boxes(load_json_shapes(json_path))


def _load_import_label(image_path, label_path, fmt, label_ids=None):
    """
    从导入绑定的标签目录读取标签框(yolo txt / labelme json).
    label_path 可为 str 或 list(多路径导入: 依次查找同名标签文件).
    与 _load_labelme 返回相同格式的 boxes 列表; 无标签/目录无效返回 [].
    label_ids: {txt 数字 id 字符串: 显示名} 映射(YOLO 专用),
    有映射时优先用显示名, 无映射退回数字本身.
    用于: 导入带标注的图像进入标注界面时显示导入的标注框
    (标注系统的 labelme json 保存在图像同路径, 而导入标签在 label_path 目录).
    """
    label_dirs = [label_path] if isinstance(label_path, (str,)) else list(label_path or [])
    label_dirs = [p for p in label_dirs if p and os.path.isdir(p)]
    if not label_dirs or not fmt:
        return []
    base = os.path.splitext(os.path.basename(image_path))[0]
    ext = ".txt" if fmt == ".txt" else ".json"
    label_file = ""
    for lp in label_dirs:
        candidate = os.path.join(lp, base + ext)
        if os.path.exists(candidate):
            label_file = candidate
            break
    if not label_file:
        return []
    if fmt == ".txt":
        # 尺寸读不到就给 0, load_yolo_shapes 会直接返回空(归一化坐标还原不了)
        iw = ih = 0
        try:
            with Image.open(image_path) as im:
                iw, ih = im.size
        except Exception:
            pass
        return shapes_to_boxes(load_yolo_shapes(label_file, iw, ih, label_ids))
    return shapes_to_boxes(load_json_shapes(label_file))


def save_labelme(image_path, shapes, width=None, height=None, version="5.0.1"):
    """
    保存 labelme json 到图像同路径(*.json).
    width/height 可传入已解码的宽高, 避免每次保存重复整图解码(QImage(image_path)).
    """
    if width is not None and height is not None:
        w, h = int(width), int(height)
    else:
        try:
            img = QImage(image_path)
            w, h = img.width(), img.height()
        except Exception:
            w = h = 0
    base, _ = os.path.splitext(image_path)
    json_path = base + ".json"
    payload = {
        "version": version,
        "flags": {},
        "shapes": shapes,
        "imagePath": os.path.basename(image_path),
        "imageData": None,
        "imageHeight": h,
        "imageWidth": w,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return json_path


class AddLabelDialog(QDialog):
    """
    添加标签弹窗:名称输入 + 10 个默认色按钮 + 自定义颜色 + 同项目标签导入.
    通过 load_project_label_combo 选择同项目其他数据集, 点击 load_label_btn
    导入该数据集已有标签(逗号分隔填入输入框), 确定后批量入库并沿用源颜色.
    """

    def __init__(self, parent=None, preset_name="", preset_color="",
                 db=None, project="", dataset="", edit_mode=False):
        super().__init__(parent)
        self.ui = AddLabelUI()
        self.ui.setupUi(self)
        self.setWindowTitle(self.tr("添加标签"))
        self._db = db
        self._project = project
        self._dataset = dataset
        self._source_colors = {}   # 导入的数据集标签颜色(用于确定时还原颜色)
        self._selected_color = ""
        self._imported_mode = False   # 本次弹窗是否走"导入"路径(导入后输入框只读)
        self._setup()
        if preset_name:
            self.ui.input_label_name_txt.setText(preset_name)
        if preset_color:
            self._select_color(preset_color)
        if edit_mode:
            # 编辑已有标签: 名称/数据集/导入全部锁定, 只允许改颜色
            self.setWindowTitle(self.tr("编辑标签"))
            self.ui.input_label_name_txt.setEnabled(False)
            self.ui.load_project_label_combo.setEnabled(False)
            self.ui.load_label_btn.setEnabled(False)

    def _setup(self):
        BTN_H = 36
        # 色块/自定义按钮统一 30px 圆形. 尺寸必须写进按钮自身的 QSS:
        # 全局 QDialog QPushButton{min-height:22} 会架空 setFixedSize 的下限,
        # 而 QSS 尺寸按内容盒算, 26 + 边框4 = 30
        CIRCLE_CSS = (" padding: 0; min-width: 26px; max-width: 26px;"
                      " min-height: 26px; max-height: 26px;"
                      " border-radius: 15px;")
        self._color_btns = [getattr(self.ui, "color{}_btn".format(i)) for i in range(1, 11)]
        for btn, color in zip(self._color_btns, LABEL_COLORS[:10]):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(
                "QPushButton {{ background-color: {0}; border: 2px solid transparent;{1} }}".format(
                    color, CIRCLE_CSS))
            btn.clicked.connect(lambda _=False, c=color, b=btn: self._select_color(c, b))
        self.ui.custom_color.setFixedSize(30, 30)
        self.ui.custom_color.setStyleSheet(
            "QPushButton {{ background-color: #2a2e3a; border: 2px solid #3a3f4e;{0} }}"
            "QPushButton:hover {{ border-color: #4f7dff; }}".format(CIRCLE_CSS))
        icon_path = _resource_path("颜色选择器.png")
        if icon_path:
            self.ui.custom_color.setIcon(QIcon(icon_path))
            self.ui.custom_color.setIconSize(QSize(18, 18))
            self.ui.custom_color.clicked.connect(self._pick_custom_color)
        apply_icon(self.ui.add_label_done_btn, QC.translate("DialogButtons", "确定"))
        self.ui.add_label_done_btn.clicked.connect(self.accept)
        self.ui.input_label_name_txt.setPlaceholderText(
            self.tr("标签名称, 多个用逗号分隔"))
        self._fill_project_label_combo()
        self.ui.load_label_btn.setText(self.tr("导入"))
        self.ui.load_label_btn.clicked.connect(self._load_labels_from_project)

    def _fill_project_label_combo(self):
        """填充同项目其他数据集的标签(单选): 排除当前数据集, 只列有标签的."""
        combo = self.ui.load_project_label_combo
        combo.clear()
        combo.addItem(self.tr("选择数据集..."), None)
        if not self._db or not self._project:
            combo.setEnabled(False)
            return
        for ds in self._db.get_datasets(self._project):
            ds_name = ds["dataset_name"]
            if ds_name == self._dataset:
                continue
            labels = self._db.get_dataset_labels(self._project, ds_name)
            if labels:
                combo.addItem(ds_name, ds_name)
        if combo.count() <= 1:
            combo.setEnabled(False)

    def _load_labels_from_project(self):
        """
        把所选数据集的标签以逗号分隔填入输入框, 并记住其颜色.
        导入后输入框置为只读(导入的标签以源数据集为准, 不允许手动改动),
        数据仅在用户点"确定"后才写入当前数据集.
        """
        combo = self.ui.load_project_label_combo
        src = combo.currentData()
        if not src:
            MessageBox.warning(self, self.tr("导入标签"),
                               self.tr("请先选择一个数据集"))
            return
        labels = self._db.get_dataset_labels(self._project, src)
        if not labels:
            MessageBox.warning(self, self.tr("导入标签"),
                               self.tr("数据集\"{}\"还没有标签").format(src))
            return
        self._source_colors = dict(labels)
        names = sorted(labels.keys(), key=label_sort_key)
        self.ui.input_label_name_txt.setText(", ".join(names))
        self.ui.input_label_name_txt.setReadOnly(True)
        self._imported_mode = True
        # 导入模式下颜色由源数据集决定,禁用颜色按钮避免无效点击
        for btn in self._color_btns:
            btn.setEnabled(False)
        self.ui.custom_color.setEnabled(False)

    def _select_color(self, color, btn=None):
        self._selected_color = color
        # 高亮选中按钮
        for i in range(1, 11):
            b = getattr(self.ui, "color{}_btn".format(i))
            border = "2px solid #ffffff" if (btn is not None and b is btn) else "2px solid transparent"
            b.setStyleSheet(
                "QPushButton {{ background-color: {0}; border: {1};"
                " padding: 0; min-width: 26px; max-width: 26px;"
                " min-height: 26px; max-height: 26px; border-radius: 15px; }}".format(
                    color if (btn is not None and b is btn) else LABEL_COLORS[i - 1], border))
        if btn is None:
            # 预设色:高亮对应按钮
            for i, c in enumerate(LABEL_COLORS[:10], start=1):
                if c.lower() == color.lower():
                    b = getattr(self.ui, "color{}_btn".format(i))
                    b.setStyleSheet(
                        "QPushButton {{ background-color: {0}; border: 2px solid #ffffff;"
                        " border-radius: 6px; }}".format(color))
                    break

    def _pick_custom_color(self):
        color = ColorPickerDialog.get_color(QColor(self._selected_color or "#4f7dff"), self)
        if color.isValid():
            self._select_color(color.name())

    def result_data(self):
        """
        返回 [(name, color), ...]. 多个标签以逗号分隔.
        颜色优先取导入数据集的源颜色(_source_colors),
        否则用当前选中颜色, 再否则按 label_color 哈希确定性分配.
        """
        text = self.ui.input_label_name_txt.text().strip()
        if not text:
            return []
        names = [n.strip() for n in re.split(r"[,\uff0c]+", text) if n.strip()]
        # 批量建标签时逐个哈希会撞色, 先登记已指定的颜色再对余下的做探测分配
        colors = {}
        used = set()
        for n in names:
            color = self._source_colors.get(n) or self._selected_color or ""
            if color:
                colors[n] = color
                used.add(color)
        for n in names:
            if n not in colors:
                color = assign_label_color(n, used)
                colors[n] = color
                used.add(color)
        return [(n, colors[n]) for n in names]


class _PrefetchWorker(QThread):
    """
    后台解码图像到 QImage(主线程再转 QPixmap 入缓存), 避免 D 切换时同步解码大图卡顿.
    请求队列 + 停止标志; 解码保持全尺寸
    """
    decoded = Signal(str, QImage)   # (image_path, qimg) - 用路径作缓存 key, 避免删除/切页后 index 错位

    def __init__(self, image_list, parent=None):
        super().__init__(parent)
        self.image_list = list(image_list)
        self._mutex = QMutex()
        self._pending = []
        self._stop = False

    def request(self, idx):
        with QMutexLocker(self._mutex):
            if idx not in self._pending and 0 <= idx < len(self.image_list):
                self._pending.append(idx)

    def stop(self):
        with QMutexLocker(self._mutex):
            self._stop = True

    def run(self):
        while True:
            with QMutexLocker(self._mutex):
                if self._stop:
                    return
                idx = self._pending.pop(0) if self._pending else None
            if idx is None:
                QThread.msleep(30)
                continue
            path = self.image_list[idx]
            reader = QImageReader(path)
            reader.setAutoTransform(True)
            qimg = reader.read()
            if qimg is not None and not qimg.isNull():
                self.decoded.emit(path, qimg)


class AnnotationDialog(QDialog):
    """标注主对话框: 加载图像 + 已有标注, 支持矩形/多边形绘制, 标签管理, A/D 切换保存."""

    def __init__(self, image_list, current_index, db, project, dataset, parent=None,
                 label_path="", label_fmt="", cls_mode=False):
        # parent 通常是主窗口 App(多继承 mixin), 删除图像等操作需要调回主窗口
        # _delete_images_core / show_dataset_images / _refresh_label_filter 等方法
        self._main = parent
        super().__init__(parent)
        self.setObjectName("AnnotationDialog")
        self.db = db
        self.project = project
        self.dataset = dataset
        self.label_path = label_path
        self.label_fmt = label_fmt
        self.label_ids = (db.get_dataset_label_ids(project, dataset)
                          if db else {})
        self.cls_mode = cls_mode
        self._cls_changes = []
        self._deleted_labels = []
        self.image_list = list(image_list) if image_list else []
        self.index = current_index
        self._pix_cache = {}
        self._pix_cache_max = 16
        self._pix_cache_bytes_max = 768 * 1024 * 1024
        self._pix_fmt_cache = {}
        self._pix_unsaved = False
        self._bright_unsaved = False   # 亮度改过但还没显式保存, 见 _commit_brightness
        self._closing = False
        self._prefetch_worker = _PrefetchWorker(self.image_list, self)
        self._prefetch_worker.decoded.connect(self._on_prefetch_decoded)
        self._prefetch_worker.start()
        self.view = None
        self.scene = None
        self._label_buttons = {}
        self._labeled_rows = {}
        self._labeled_sel_row = None
        self._dirty = False
        self._modified_paths = set()
        self.label_colors = dict(self.db.get_dataset_labels(project, dataset))

        self.ui = AnnotationUI()
        self.ui.setupUi(self)
        self.setWindowTitle(self.tr("标注 - {} / {}").format(project, dataset))
        self.setWindowFlags(self.windowFlags()
                            | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self._replace_view()
        self._setup_ui()
        self._setup_clipboard()
        self._setup_shortcuts()
        self.scene.label_colors = {k: QColor(v) for k, v in self.label_colors.items()}
        self._refresh_labels()
        self._load_current()

    def _replace_view(self):
        """在用户设计的 image_label_show 控件上启用标注能力(不新增控件)."""
        self.view = _upgrade_graphics_view(self.ui.image_label_show)
        self.scene = self.view.scene_

    def _setup_ui(self):
        u = self.ui
        u.draw_rect_btn.setText(self.tr("矩形"))
        u.poly_btn.setText(self.tr("多边形"))
        # uic 给的是 ../resources 相对路径, 安装版 cwd 变了就取不到, 这里用绝对路径重设
        for btn, icon_file in ((u.draw_rect_btn, "矩形.png"),
                               (u.poly_btn, "多边形.png"),
                               (u.delete_image_btn, "删除.png")):
            ipath = _icon_path(icon_file)
            if ipath:
                btn.setIcon(_tinted(ipath, "#b8c0d0"))
                btn.setIconSize(QSize(18, 18))
        u.label_list.setText(self.tr("标签列表"))
        u.labeled_list.setText(self.tr("标注信息"))
        u.pre_page_btn.setText(self.tr("上一张"))
        u.next_page_btn.setText(self.tr("下一张"))
        u.lineEdit.hide()
        u.draw_rect_btn.clicked.connect(lambda: self._start_draw("rect"))
        u.poly_btn.clicked.connect(lambda: self._start_draw("polygon"))
        # 行标签钉死 64 宽: QLabel 默认会把行内富余宽度吸走, 各行控件起始列就对不齐了
        for name in ("params_angle_label", "blend_strength_label",
                     "brightness_label", "params_fill_label",
                     "params_presets_label"):
            getattr(u, name).setFixedWidth(64)
        # 角度范围输入框: 粘贴时随机旋转的角度范围(默认 -180 ~ 180, 居中, 仅整数)
        # 高度不在这里定: __init__ 时按钮还没被 QSS 定高(36), 此时取值会偏大,
        # 统一由 #AnnotationDialog QLineEdit 的 min/max-height 与按钮对齐
        for edit, default in zip((u.min_ange_lineEdit, u.max_ange_lineEdit),
                                 ANGLE_RANGE_DEFAULT):
            edit.setText(str(default))
            edit.setAlignment(Qt.AlignCenter)
            edit.setMaxLength(100)
            edit.setValidator(QIntValidator(-3600, 3600, self))
            edit.setFixedWidth(62)
        u.label.setText("~")
        # 融合强度: 粘贴时的像素融合力度(0=原始硬贴, 1=完全融合), 滑块与输入框互相跟随
        u.blend_strength_lineEdit.setText(BLEND_STRENGTH_DEFAULT)
        u.blend_strength_lineEdit.setAlignment(Qt.AlignCenter)
        u.blend_strength_lineEdit.setValidator(QDoubleValidator(0.0, 1.0, 2, self))
        u.blend_strength_lineEdit.editingFinished.connect(self._normalize_blend_strength)
        u.blend_slider.setRange(0, 100)
        u.blend_slider.setFocusPolicy(Qt.NoFocus)
        u.blend_slider.valueChanged.connect(self._on_blend_slider)
        self._normalize_blend_strength()
        # 亮度调节: 只改选中多边形框内的像素, 拖动实时预览, 落盘等切图/Ctrl+S
        u.brightness_lineEdit.setText(BRIGHTNESS_DEFAULT)
        u.brightness_lineEdit.setAlignment(Qt.AlignCenter)
        u.brightness_lineEdit.setValidator(QDoubleValidator(0.0, 1.0, 2, self))
        u.brightness_lineEdit.editingFinished.connect(self._normalize_brightness)
        u.brightness_lineEdit.setToolTip(
            self.tr("只在选中的多边形框内生效; A/D 切图或 Ctrl+S 才写盘"))
        u.brightness_slider.setRange(0, 100)
        u.brightness_slider.setFocusPolicy(Qt.NoFocus)
        u.brightness_slider.setToolTip(u.brightness_lineEdit.toolTip())
        u.brightness_slider.valueChanged.connect(self._on_brightness_slider)
        u.brightness_slider.sliderReleased.connect(self._commit_brightness)
        self._sync_brightness_slider()
        # 填充颜色: 多边形右键"填充"写入的颜色, 色块(取色器)/ 常用色点 / 文本框三种改法
        u.fill_color_lineEdit.setText(FILL_COLOR_DEFAULT)
        u.fill_color_lineEdit.setAlignment(Qt.AlignCenter)
        u.fill_color_lineEdit.setMaxLength(18)
        # 不给上限的话 QLineEdit 的 sizeHint(247) 会成为弹层最宽的一行, 把面板顶宽 ~50px
        u.fill_color_lineEdit.setMaximumWidth(130)
        u.fill_color_lineEdit.editingFinished.connect(self._normalize_fill_color)
        u.fill_color_btn.clicked.connect(self._pick_fill_color)
        # 图标按钮与左侧色块同尺寸; 素材和添加标签弹窗的自定义色按钮共用
        u.custom_color_btn.setFixedSize(28, 28)
        u.custom_color_btn.setCursor(Qt.PointingHandCursor)
        icon_path = _resource_path("颜色选择器.png")
        if icon_path:
            u.custom_color_btn.setIcon(QIcon(icon_path))
            u.custom_color_btn.setIconSize(QSize(18, 18))
        u.custom_color_btn.clicked.connect(self._pick_fill_color)
        self._fill_dot_btns = []
        for color in FILL_COLOR_PRESETS:
            dot = QPushButton(self)
            dot.setFixedSize(20, 20)
            dot.setCursor(Qt.PointingHandCursor)
            dot.setToolTip(color)
            dot.setStyleSheet(_fill_dot_qss(color, False))
            dot.clicked.connect(lambda _=False, c=color: self._set_fill_color(c))
            u.params_presets_box.addWidget(dot)
            self._fill_dot_btns.append(dot)
        self._sync_fill_color_btn()
        u.switchButton = SwitchButton(self)
        u.switchButton.setObjectName("switchButton")
        u.switchButton.setChecked(True)
        u.switchButton.toggled.connect(self._toggle_show_boxes)
        u.show_boxes_label = QLabel(self.tr("显示标注"), self)
        u.show_boxes_label.setObjectName("show_boxes_label")
        # 参数收进"设置"弹层后, 工具条右侧只剩开关和设置按钮
        idx = u.horizontalLayout.indexOf(u.settings_btn)
        u.horizontalLayout.insertWidget(idx, u.switchButton)
        u.horizontalLayout.insertWidget(idx + 1, u.show_boxes_label)
        u.settings_btn.clicked.connect(self._toggle_params_panel)
        u.close_params_btn.clicked.connect(self._hide_params_panel)
        u.reset_params_btn.clicked.connect(self._reset_params)
        # 参数弹层不是布局成员, 不显式收起的话窗口 show 出来就叠在右侧栏上
        u.paramsPanel.hide()
        # 同理它收不到"点了别处", 装个应用级过滤器自己判落点
        QApplication.instance().installEventFilter(self)
        u.add_label.clicked.connect(self._add_label_clicked)
        u.pre_page_btn.clicked.connect(lambda: self._switch(-1))
        u.next_page_btn.clicked.connect(lambda: self._switch(1))
        u.delete_image_btn.clicked.connect(self._delete_current_image)
        self.scene.box_drawn.connect(self._on_box_drawn)
        self.scene.draw_cancel_requested.connect(self._cancel_draw_mode)
        self._labeled_refresh_timer = QTimer(self)
        self._labeled_refresh_timer.setSingleShot(True)
        self._labeled_refresh_timer.setInterval(80)
        self._labeled_refresh_timer.timeout.connect(self._refresh_labeled_list)
        self._autosave_timer = QTimer(self)
        self._autosave_timer.setSingleShot(True)
        self._autosave_timer.setInterval(150)
        self._autosave_timer.timeout.connect(self._save_current)
        self.scene.boxes_changed.connect(self._on_boxes_changed)
        self.scene.label_change_requested.connect(self._on_label_change_requested)
        # 像素级改动(粘贴/填充/撤销)不走 boxes_changed, 单独接: 同步缓存 + 落盘
        self.scene.image_pixels_changed.connect(self._on_image_pixels_changed)
        self.scene.selection_changed.connect(self._sync_labeled_selection)
        # 图像分类数据集:只读看图,禁用一切标注/绘制控件
        if self.cls_mode:
            for w in (u.draw_rect_btn, u.poly_btn,
                      u.add_label):
                w.setEnabled(False)

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
        """输入框 -> 滑块(不碰图像); 空值/非法值回默认, 返回收敛后的值."""
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
        self._apply_brightness(v)

    def _apply_brightness(self, v):
        """只改选中多边形框内的像素; 没选中或选中的是矩形就提示一下."""
        item = self.scene.selected_item() if self.scene is not None else None
        if item is None:
            QToolTip.showText(QCursor.pos(), self.tr("先在画布上点选一个多边形"))
            return
        if not self.scene.set_polygon_brightness(item, v):
            QToolTip.showText(QCursor.pos(), self.tr("亮度调节只对多边形有效"))

    def _commit_brightness(self):
        """
        亮度改完落定: 只刷新图像缓存, 不设 _pix_unsaved 也不启动 150ms 自动保存.
        后者会让"松手后随手画个框"触发的自动保存把亮度一起写掉, 等于拖一下就写一次盘;
        真正写盘统一等 _save_current 里用户显式保存的那一次.
        """
        scene = getattr(self, "scene", None)
        if scene is None or not scene.has_pending_brightness():
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

    def eventFilter(self, obj, event):
        # 弹层不在布局里, 收不到"点了别处"的信号, 只能全局盯鼠标按下.
        # 按坐标判落点而不是看 obj: QLabel 不吃鼠标事件, 会一路冒泡到 dialog 再进来
        if (event.type() == QEvent.Type.MouseButtonPress
                and not self.ui.paramsPanel.isHidden()
                and isinstance(obj, QWidget) and obj.window() is self
                and not self._hit_params_area(event.globalPosition().toPoint())):
            self._hide_params_panel()
        return super().eventFilter(obj, event)

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

    def _on_image_pixels_changed(self):
        """
        图像像素被改写(粘贴/填充/撤销) → 刷新缓存 + 标记落盘.
        QPixmap 是写时复制: 场景里 QPainter 画的是副本, _pix_cache 里那份原地不动,
        不换掉的话 A/D 翻走再翻回来会命中旧图(看起来"图像没改, 只剩多边形").
        """
        if not (0 <= self.index < len(self.image_list)):
            return
        item = getattr(self.scene, "image_item", None)
        if item is None:
            return
        pix = item.pixmap()
        if pix is None or pix.isNull():
            return
        self._put_pix_cache(self.image_list[self.index], pix)
        self._pix_unsaved = True
        self._dirty = True
        self._autosave_timer.start()

    def _on_boxes_changed(self):
        """
        标注内容变化(画/删/改类别/拖动缩放)→ 标记 dirty + 刷新右侧列表.
        load_boxes 加载时也会 emit boxes_changed, 但 _loading=True 期间不标记.
        """
        if not getattr(self, "_loading", False):
            self._dirty = True
            self._autosave_timer.start()
        self._labeled_refresh_timer.start()

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("A"), self, activated=lambda: self._switch(-1))
        QShortcut(QKeySequence("D"), self, activated=lambda: self._switch(1))
        QShortcut(QKeySequence("Delete"), self, activated=self.scene.delete_selected)
        QShortcut(QKeySequence("Ctrl+S"), self,
                  activated=lambda: self._save_current(commit_pending=True))
        QShortcut(QKeySequence("Ctrl+Z"), self, activated=self._undo_fp_paste)
        QShortcut(QKeySequence(Qt.Key_Escape), self, activated=self._cancel_draw_mode)

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

    def _load_pixmap(self, image_path):
        """全尺寸加载图像(缓存命中直接返回; 未命中 QImageReader 解码后入 LRU).
        缓存 key 用 image_path(不用 self.index) - 删除图像后列表前移, index 会指向别的图,
        若按 index 缓存会把"已删图/错位图"显示出来."""
        pix = self._pix_cache.get(image_path)
        if pix is None:
            reader = QImageReader(image_path)
            reader.setAutoTransform(True)
            qimg = reader.read()
            if qimg is None or qimg.isNull():
                return None
            pix = QPixmap.fromImage(qimg)
            self._put_pix_cache(image_path, pix, qimg.format())
            return pix

        self._put_pix_cache(image_path, pix)
        return pix

    def _put_pix_cache(self, image_path, pix, fmt=None):
        """入缓存并刷新访问顺序(dict 末尾 = 最近使用), 超出上限按 LRU 淘汰."""
        self._pix_cache.pop(image_path, None)
        self._pix_cache[image_path] = pix
        if fmt is not None:
            self._pix_fmt_cache[image_path] = fmt
        self._trim_pix_cache()

    def _trim_pix_cache(self):
        """
        LRU 淘汰: 从 dict 首项(最久未用)开始丢弃, 同步清理 format 缓存.
        先按张数, 再按估算字节数; 字节循环保留最后一项, 保证当前图不被挤掉.
        """
        while len(self._pix_cache) > self._pix_cache_max:
            self._drop_oldest_pix()
        while (len(self._pix_cache) > 1
               and self._pix_cache_bytes() > self._pix_cache_bytes_max):
            self._drop_oldest_pix()

    def _drop_oldest_pix(self):
        k = next(iter(self._pix_cache), None)
        if k is None:
            return
        self._pix_cache.pop(k, None)
        self._pix_fmt_cache.pop(k, None)

    def _pix_cache_bytes(self):
        """按 depth 估算位图占用(灰度图用 4 字节/像素会高估, 导致过度淘汰)."""
        return sum(p.width() * p.height() * p.depth() // 8
                   for p in self._pix_cache.values())

    def _on_prefetch_decoded(self, path, qimg):
        """后台解码完成: 转 QPixmap 入缓存(按 image_path 作 key), 同步记录 format."""
        if getattr(self, "_closing", False):
            return
        if qimg.isNull():
            return
        if path in self._pix_cache:
            return
        self._put_pix_cache(path, QPixmap.fromImage(qimg), qimg.format())

    def _load_current(self):
        if not (0 <= self.index < len(self.image_list)):
            return
        self._apply_draw_mode_cursor()
        image_path = self.image_list[self.index]
        pix = self._load_pixmap(image_path)
        if pix is None or pix.isNull():
            return
        self.scene.set_image(pix)
        # 预解码相邻图(后台线程), 连续 A/D 翻页时命中缓存不卡
        for nxt in (self.index + 1, self.index - 1):
            if (0 <= nxt < len(self.image_list)
                    and self.image_list[nxt] not in self._pix_cache):
                self._prefetch_worker.request(nxt)
        if self.cls_mode:
            # 图像分类: 只读看图,无框可标注;类别 = 父文件夹名
            boxes = []
            cls = os.path.basename(os.path.dirname(image_path))
            color = self.label_colors.get(cls)
            if color is None:
                color = label_color(cls).name()
            short = min(pix.width(), pix.height())
            font_size = max(4, min(48, int(short / 4)))
            max_by_width = max(4, int(pix.width() * 0.95
                                     / max(len(str(cls)), 1) / 1.4))
            font_size = min(font_size, max_by_width)
            item = _ClsLabelItem(str(cls), str(color), font_size=font_size)
            self.scene.addItem(item)
            r = item.boundingRect()
            item.setPos(pix.width() / 2 - r.width() / 2,
                        pix.height() / 2 - r.height() / 2)
            item.setZValue(10)
        else:
            json_path = same_dir_json(image_path)
            if json_path:
                boxes = _load_labelme(json_path)
            else:
                boxes = _load_import_label(image_path, self.label_path,
                                           self.label_fmt, self.label_ids)
        self._loading = True
        try:
            self.scene.load_boxes(boxes)
        finally:
            self._loading = False
        # A/D 切图保持"显示标注"开关状态(关闭时隐藏标注轮廓)
        show = getattr(self.ui, "switchButton", None) is not None and self.ui.switchButton.isChecked()
        self.scene.set_annotations_visible(show)
        self._ensure_label_colors(boxes)
        QTimer.singleShot(0, self.view.fit_window)
        channels = {
            QImage.Format_Grayscale8: 1,
            QImage.Format_Grayscale16: 1,
            QImage.Format_RGB888: 3,
            QImage.Format_RGB32: 3,
            QImage.Format_ARGB32: 4,
            QImage.Format_RGBA8888: 4,
        }.get(self._pix_fmt_cache.get(image_path, QImage.Format_RGB32), 3)
        self.ui.image_info_label.setText(
            "{} × {} × {}    ({}/{}){}".format(
                pix.width(), pix.height(), channels,
                self.index + 1, len(self.image_list),
                self.tr("    类别: {}").format(cls) if self.cls_mode else ""))
        self._refresh_labeled_list()
        self._dirty = False
        # 新载入的图以磁盘内容为准, 清掉上一张遗留的待写标记
        self._pix_unsaved = False

    def _switch(self, offset):
        if not self.image_list:
            return
        self._hide_params_panel()
        self._save_current(commit_pending=True)
        new_index = self.index + offset
        if not (0 <= new_index < len(self.image_list)):
            return
        self.index = new_index
        self._load_current()

    def _delete_current_image(self):
        """
        标注界面单张删除: 弹窗确认 -> 调 _delete_images_core 删文件+更新缓存/db
        -> 自动切到下一张(列表前移即指向原 next; 删最后一张则回退一张; 删光则清空场景)
        """
        if not (0 <= self.index < len(self.image_list)):
            return
        cur_path = self.image_list[self.index]
        # 先保存当前未提交的标注(避免画了框没保存就被删, 导致标注明文丢失)
        self._save_current(commit_pending=True)
        btn_delete = self.tr("删除本地文件")
        btn_cancel = self.tr("取消")
        clicked = MessageBox.choose(
            self, self.tr("删除图像"),
            self.tr("是否删除当前图像?\n\n{}").format(
                os.path.basename(cur_path)),
            [(btn_delete, QMessageBox.YesRole),
             (btn_cancel, QMessageBox.RejectRole)],
            informative=self.tr("图像与同名标注文件将从磁盘删除, 不可恢复"))
        if clicked is None or clicked == btn_cancel:
            return
        main = getattr(self, "_main", None)
        if main is None or not hasattr(main, "_delete_images_core"):
            MessageBox.warning(self, self.tr("删除图像"),
                               self.tr("无法访问主窗口, 删除失败"))
            return
        main._delete_images_core(self.project, self.dataset, [cur_path], True,
                                 log_msg="标注界面删除图像: {} | 方式={} | 项目={}, 数据集={}".format(
                                     os.path.basename(cur_path),
                                     "删除本地文件",
                                     self.project, self.dataset))
        self.image_list.pop(self.index)
        self._pix_cache.pop(cur_path, None)
        self._pix_fmt_cache.pop(cur_path, None)
        if not self.image_list:
            self.index = 0
            self.scene.set_image(QPixmap())
            self._refresh_labeled_list()
            self.ui.image_info_label.setText(self.tr("(无图像)"))
            return
        if self.index >= len(self.image_list):
            self.index = len(self.image_list) - 1
        self._dirty = False
        self._load_current()

    def _ensure_label_colors(self, boxes):
        """
        确保 boxes 中所有标签都在 db / label_colors 中.
        缺失的标签(如手动创建 labelme json 里的新标签)用确定性哈希色
        label_color() 入库, 保证: 同一标签在 A/D 翻页时颜色一致,
        且首页标签下拉框/下次启动都能看到
        """
        missing = {}
        used = set(self.label_colors.values())
        for lbl in sorted({normalize_label(b.get("label")) for b in boxes}):
            if lbl and lbl not in self.label_colors:
                color = assign_label_color(lbl, used)
                missing[lbl] = color
                used.add(color)
        if not missing:
            return
        merged = dict(self.db.get_dataset_labels(self.project, self.dataset))
        merged.update(missing)
        self.db.save_dataset_labels(self.project, self.dataset, merged)
        for lbl, color in missing.items():
            self.label_colors[lbl] = color
            self.scene.label_colors[lbl] = QColor(color)
        self._refresh_labels()

    def closeEvent(self, event):
        self._save_current(commit_pending=True)
        self._closing = True
        QApplication.instance().removeEventFilter(self)
        if getattr(self, "_prefetch_worker", None) is not None:
            self._prefetch_worker.stop()
            self._prefetch_worker.wait(2000)
        QApplication.restoreOverrideCursor()
        super().closeEvent(event)

    def _update_draw_buttons(self):
        """无标签或未选中标签时禁用矩形/多边形/格式刷按钮."""
        if self.cls_mode:
            # 图像分类只读,始终禁用绘制
            for w in (self.ui.draw_rect_btn, self.ui.poly_btn):
                w.setEnabled(False)
            return
        can_draw = bool(self.label_colors) and self.scene.current_label in self.label_colors
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
                self, self.tr("添加标签"),
                self.tr("请先添加标签(点击\"+\")"))

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

    def _on_box_drawn(self):
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
        """角度范围输入框 → (lo, hi); 空/非整数回默认."""
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
    CLIP_W, CLIP_H = 120, 90
    CLIP_ROWS = 3   # 剪切板可视行数, 超出后滚动

    def _clip_qss(self):
        w, h = self.CLIP_W - 4, self.CLIP_H - 4
        return ("QPushButton#clipThumb {{ border: 2px solid #3a3f4e;"
                " border-radius: 4px; padding: 0px; background: #22252d;"
                " min-width: {w}px; max-width: {w}px;"
                " min-height: {h}px; max-height: {h}px; }}"
                "QPushButton#clipThumb:hover {{ border-color: #6b8bff; }}"
                "QPushButton#clipThumb:checked {{ border-color: #4f7dff;"
                " background: #1d2735; }}").format(w=w, h=h)

    def _copy_template(self, item):
        """右键"复制"入口: 抠模板入全局剪切板并选中最新缩略图."""
        if not self.scene.copy_template_from_item(item):
            return
        _clip_templates.insert(0, dict(self.scene.fp_template))
        self._rebuild_clipboard(select=0)

    def _setup_clipboard(self):
        u = self.ui
        u.clipboard_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        u.clipboard_container.setStyleSheet(self._clip_qss())
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
            self.tr("剪切板  {}/{}").format(cur, len(_clip_templates)))

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
                self.tr("第 {} 个模板  {}x{}\n左键选中用于粘贴, "
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
        act_del = menu.addAction(self.tr("删除")) if i >= 0 else None
        if act_del is not None:
            menu.addSeparator()
        act_imp = menu.addAction(self.tr("导入"))
        act_exp = menu.addAction(self.tr("导出"))
        menu.addSeparator()
        act_clr = menu.addAction(self.tr("清空"))
        if not _clip_templates:
            act_exp.setEnabled(False)
            act_clr.setEnabled(False)
        act = menu.exec(QCursor.pos())
        if act is None:
            return
        if act is act_del:
            was_current = self.scene.fp_template is _clip_templates[i]
            _clip_templates.pop(i)
            # 删掉的正是当前粘贴模板且剪切板已空 → 置空; 手绘轨迹模板不在剪切板, 不受影响
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

    def _clip_export(self):
        """导出到目录: 一张一个 png(带 alpha) + 同名 labelme json 记多边形顶点."""
        if not _clip_templates:
            MessageBox.warning(self, self.tr("导出剪切板"),
                               self.tr("剪切板是空的, 没有可导出的模板"))
            return
        folder = QFileDialog.getExistingDirectory(self, self.tr("选择导出目录"))
        if not folder:
            return
        n = 0
        try:
            for i, t in enumerate(_clip_templates):
                patch = t.get("patch")
                if patch is None or patch.isNull():
                    continue
                path = os.path.join(folder, "stamp_{:02d}.png".format(i + 1))
                if not patch.save(path, "PNG"):
                    continue
                # 顶点跟着存进同名 json: 只存 png 的话导回来就只剩一个外接矩形
                local = _patch_local_points(t)
                if len(local) >= 3:
                    data = shapes_to_labelme_json(
                        [(t.get("label") or "object", local)],
                        path, patch.width(), patch.height())
                    with open(os.path.splitext(path)[0] + ".json", "w",
                              encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                n += 1
        except Exception as e:
            write_log("导出剪切板失败: {}".format(e))
            MessageBox.warning(self, self.tr("导出剪切板"),
                               self.tr("导出中断: {}\n(已写出 {} 个)").format(e, n))
            return
        MessageBox.information(
            self, self.tr("导出剪切板"),
            self.tr("已导出 {} 个模板(png + 同名 json)到:\n{}").format(n, folder))

    def _clip_import(self):
        """从目录读回 png: 有同名 json 就按顶点重裁 alpha, 没有才回落成矩形."""
        folder = QFileDialog.getExistingDirectory(self, self.tr("选择导入目录"))
        if not folder:
            return
        try:
            names = sorted(f for f in os.listdir(folder)
                           if f.lower().endswith(".png"))
        except OSError as e:
            MessageBox.warning(self, self.tr("导入剪切板"),
                               self.tr("读取目录失败: {}").format(e))
            return
        if not names:
            MessageBox.warning(self, self.tr("导入剪切板"),
                               self.tr("这个目录里没有 png 文件"))
            return
        new_items, rect_n, bad = [], 0, []
        for name in names:
            path = os.path.join(folder, name)
            img = QImage(path)
            if img.isNull():
                bad.append(name)
                continue
            patch = img.convertToFormat(QImage.Format_ARGB32_Premultiplied)
            label, pts = "", None
            shapes = load_json_shapes(os.path.splitext(path)[0] + ".json")
            if shapes:
                label, pts = shapes[0]
                pts = _fit_points_to_patch(pts, path, patch)
                # 外部 png 可能是压平过的白底, 按多边形重裁一遍才只贴出形状那块
                AnnotationScene.mask_polygon(patch, pts)
            if not pts:
                pts = [[0.0, 0.0], [float(patch.width()), 0.0],
                       [float(patch.width()), float(patch.height())],
                       [0.0, float(patch.height())]]
                rect_n += 1
            new_items.append({"points": pts, "patch": patch,
                              "w": patch.width(), "h": patch.height(),
                              "label": label or self.scene.current_label})
        if new_items:
            _clip_templates[:0] = new_items
            self._rebuild_clipboard(select=0)
        msg = self.tr("已导入 {} 个模板到剪切板").format(len(new_items))
        if rect_n:
            msg += self.tr("\n其中 {} 个没有同名 json, 按矩形导入").format(rect_n)
        if bad:
            msg += self.tr("\n{} 个文件读不出来, 已跳过").format(len(bad))
        MessageBox.information(self, self.tr("导入剪切板"), msg)

    def showEvent(self, event):
        super().showEvent(event)
        # QDialog 首次显示后置最大化(exec 前设置不生效)
        if not getattr(self, "_maximized_once", False):
            self._maximized_once = True
            self.setWindowState(Qt.WindowMaximized)

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

    def _label_icon(self, color):
        """标签颜色圆点图标(下拉菜单/右侧列表用). 归一成色值字符串后走模块级缓存."""
        return _dot_icon(QColor(color).name())

    def _on_label_change_requested(self, item):
        """点击标注框上的标签 chip → 弹出所有标签下拉, 选择后修改该框类别."""
        if not self.label_colors:
            return
        menu = QMenu(self)
        for name, color in sorted(self.label_colors.items(),
                                  key=lambda kv: label_sort_key(kv[0])):
            act = menu.addAction(self._label_icon(color), name)
            act.setCheckable(True)
            act.setChecked(name == item.label)
        if menu.isEmpty():
            return
        pos = QCursor.pos()
        if hasattr(item, "chip_scene_pos"):
            scene_pos = item.chip_scene_pos()
            if scene_pos is not None:
                pos = self.view.mapToGlobal(self.view.mapFromScene(scene_pos))
        chosen = menu.exec(pos)
        if chosen is not None and chosen.text() != item.label:
            if self.cls_mode:
                self._change_cls(chosen.text())
            else:
                self.scene.set_item_label(item, chosen.text())

    def _change_cls(self, new_cls):
        """分类数据集: 把当前图像移动到新类别文件夹, 记录改动供首页刷新缓存."""
        if not (0 <= self.index < len(self.image_list)):
            return
        old_path = self.image_list[self.index]
        old_cls = os.path.basename(os.path.dirname(old_path))
        if new_cls == old_cls:
            return
        root = os.path.dirname(os.path.dirname(old_path))
        new_dir = os.path.join(root, new_cls)
        os.makedirs(new_dir, exist_ok=True)
        base = os.path.basename(old_path)
        stem, ext = os.path.splitext(base)
        new_path = os.path.join(new_dir, base)
        n = 1
        while os.path.exists(new_path):
            new_path = os.path.join(new_dir, "{}_{}{}".format(stem, n, ext))
            n += 1
        try:
            os.rename(old_path, new_path)
        except Exception:
            try:
                shutil.move(old_path, new_path)
            except Exception:
                MessageBox.warning(
                    self, self.tr("修改类别"),
                    self.tr("移动图像文件失败:\n{}").format(old_path))
                return
        self.image_list[self.index] = new_path
        self._cls_changes.append((old_path, new_path, new_cls))
        write_log("分类修改: {} → {} ({})".format(
            old_cls, new_cls, os.path.basename(new_path)))
        self._load_current()

    def _refresh_labels(self):
        """刷新左侧标签列表(颜色块 + 名称), 点击切换当前标签."""
        self.label_colors = dict(self.db.get_dataset_labels(self.project, self.dataset))
        if not self.label_colors:
            self.scene.current_label = ""
            self._update_draw_buttons()
            return
        self._update_draw_buttons()
        container = self.ui.scrollAreaWidgetContents
        layout = container.layout() if container.layout() else QVBoxLayout(container)
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)
        self._label_buttons = {}
        # 按 label_sort_key 排序:纯数字按数值,其他按字符串 - 与首页下拉框一致
        for name, color in sorted(self.label_colors.items(),
                                  key=lambda kv: label_sort_key(kv[0])):
            row = QFrame(container)
            row.setFrameShape(QFrame.NoFrame)
            row.setObjectName("labelRow")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(8, 6, 8, 6)
            rl.setSpacing(8)
            # 圆形按钮显示颜色(可点击切换当前标签)
            color_btn = QPushButton(row)
            color_btn.setFixedSize(18, 18)
            color_btn.setCursor(Qt.PointingHandCursor)
            color_btn.setStyleSheet(
                "QPushButton {{ background-color: {0}; border: 1px solid #3a3f4e;"
                " border-radius: 9px; padding: 0px; margin: 0px;"
                " min-width: 0px; max-width: 18px; min-height: 0px; max-height: 18px; }}".format(color))
            color_btn.setToolTip(name)
            color_btn.clicked.connect(lambda _=False, n=name, r=row: self._select_label(n, r))
            rl.addWidget(color_btn)
            name_lbl = QLabel(name, row)
            name_lbl.setObjectName("labelRowName")
            rl.addWidget(name_lbl)
            rl.addStretch(1)
            # 行尾编辑/删除小图标按钮
            btn_style = (
                "QPushButton { background: transparent; border: none; padding: 0;"
                " margin: 0; min-width: 0; max-width: 22px; min-height: 0;"
                " max-height: 22px; border-radius: 4px; }"
                "QPushButton:hover { background: #2c303c; }")
            for icon_file, tip, handler in (
                    ("编辑.png", self.tr("编辑"), self._edit_label),
                    ("删除.png", self.tr("删除"), self._delete_label_from_list)):
                ibtn = QPushButton(row)
                ibtn.setFixedSize(22, 22)
                ibtn.setCursor(Qt.PointingHandCursor)
                ibtn.setToolTip(tip)
                ibtn.setStyleSheet(btn_style)
                ipath = _icon_path(icon_file)
                if ipath:
                    ibtn.setIcon(_tinted(ipath, "#b8c0d0"))
                    ibtn.setIconSize(QSize(14, 14))
                ibtn.clicked.connect(
                    lambda _=False, n=name, f=handler: f(n))
                rl.addWidget(ibtn)
            row.mousePressEvent = (lambda ev, n=name, r=row: self._select_label(n, r))
            layout.addWidget(row)
            self._label_buttons[name] = row
        layout.addStretch(1)

    def _edit_label(self, name):
        """编辑标签颜色: 弹编辑标签窗(名称/导入锁定), 确定后写库并即时刷新."""
        dlg = AddLabelDialog(self, preset_name=name,
                             preset_color=self.label_colors.get(name, ""),
                             db=self.db, project=self.project,
                             dataset=self.dataset, edit_mode=True)
        if dlg.exec() != QDialog.Accepted:
            return
        items = dlg.result_data()
        if not items:
            return
        new_color = items[0][1]
        if new_color == self.label_colors.get(name):
            return
        self.db.add_dataset_label(self.project, self.dataset, name, new_color)
        self.label_colors[name] = new_color
        self.scene.label_colors[name] = QColor(new_color)
        # 框颜色是 paint 时动态查 scene.label_colors, 重绘即可生效(A/D 翻页同源)
        self.scene.update()
        self._refresh_labels()
        self._refresh_labeled_list()
        write_log("修改标签颜色: {} → {} ({}/{})".format(
            name, new_color, self.project, self.dataset))

    def _dataset_image_paths(self):
        """全数据集图像路径: 优先主窗口索引(不受当前筛选视图影响), 退回当前列表."""
        cache = getattr(self._main, "dataset_cache", None) if self._main else None
        recs = {}
        if cache:
            recs = cache.get(self.project, {}).get(self.dataset, {}) or {}
        paths = [r.get("image_path", "") for r in (recs.get("all") or [])
                 if r.get("image_path")]
        return paths or list(self.image_list)

    def _count_label_in_jsons(self, needle):
        """无索引时退回统计: 扫图像同路径 json 计数该标签的 shapes."""
        paths = self._dataset_image_paths()
        progress = None
        if len(paths) > 50:
            progress = ProgressDialog(
                self.tr("删除标签"), self.tr("正在统计标注文件..."), self,
                maximum=len(paths), cancellable=False)
        try:
            total = 0
            for i, img_path in enumerate(paths):
                if progress is not None:
                    progress.set_progress(i)
                jp = same_dir_json(img_path)
                if not jp:
                    continue
                try:
                    with open(jp, "r", encoding="utf-8") as f:
                        text = f.read()
                    if needle not in text:
                        continue
                    data = json.loads(text)
                    total += sum(1 for s in data.get("shapes", [])
                                 if normalize_label(s.get("label")) == needle)
                except Exception:
                    continue
            return total
        finally:
            if progress is not None:
                progress.close()

    def _delete_label_from_list(self, name):
        """
        删除标签并同步清理其标注: db / 本地 labelme json / 当前场景.
        统计口径与数据集统计一致: 优先数主窗口内存索引的 boxes/labels
        (统计页 label_counts 同源, 即时); 无索引时退回扫描图像同路径 json.
        先统计,用户确认后才写文件(取消不落盘).
        """
        needle = normalize_label(name)
        cur_img = (self.image_list[self.index]
                   if 0 <= self.index < len(self.image_list) else "")
        scene_items = [it for it in self.scene.all_items()
                       if getattr(it, "label", None) == name]
        cache = getattr(self._main, "dataset_cache", None) if self._main else None
        index = {}
        if cache:
            index = cache.get(self.project, {}).get(self.dataset, {}) or {}
        recs = index.get("all") or []
        if recs:
            total = 0
            cur_saved = 0
            for r in recs:
                boxes = r.get("boxes") or []
                cnt = (sum(1 for b in boxes if b[-1] == name) if boxes
                       else sum(1 for l in (r.get("labels") or [])
                                if l == name))
                total += cnt
                if r.get("image_path") == cur_img:
                    cur_saved = cnt
            total += max(0, len(scene_items) - cur_saved)
        else:
            total = self._count_label_in_jsons(needle)
            total += max(0, len(scene_items))
        if total > 0:
            if not MessageBox.question(
                    self, self.tr("删除标签"),
                    self.tr("标签\"{}\"已有 {} 处标注, 删除后这些标注将被一并删除"
                            "且不可恢复.\n确定删除吗?").format(name, total),
                    default_yes=True):
                return
        else:
            if not MessageBox.question(
                    self, self.tr("删除标签"),
                    self.tr("确定删除标签\"{}\"吗?").format(name),
                    default_yes=True):
                return
        # 确认后清理图像同路径 json(外部标签目录文件由主窗口关闭后统一清理)
        paths = self._dataset_image_paths()
        progress = None
        if len(paths) > 50:
            progress = ProgressDialog(
                self.tr("删除标签"), self.tr("正在清理标注文件..."), self,
                maximum=len(paths), cancellable=False)
        try:
            for i, img_path in enumerate(paths):
                if progress is not None:
                    progress.set_progress(i)
                jp = same_dir_json(img_path)
                if not jp:
                    continue
                try:
                    with open(jp, "r", encoding="utf-8") as f:
                        text = f.read()
                    if needle not in text:
                        continue
                    data = json.loads(text)
                    before = len(data.get("shapes", []))
                    data["shapes"] = [s for s in data.get("shapes", [])
                                      if normalize_label(s.get("label")) != needle]
                    if len(data["shapes"]) != before:
                        with open(jp, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                except Exception:
                    continue
        finally:
            if progress is not None:
                progress.close()
        for item in scene_items:
            self.scene.delete_item(item)
        self.db.remove_dataset_label(self.project, self.dataset, name)
        self._deleted_labels.append(name)
        write_log("删除标签: {} ({}/{})".format(
            name, self.project, self.dataset))
        self.label_colors.pop(name, None)
        self.scene.label_colors.pop(name, None)
        if self.scene.current_label == name:
            self.scene.current_label = (sorted(self.label_colors,
                                               key=label_sort_key)[0]
                                        if self.label_colors else "")
        self._refresh_labels()
        self._refresh_labeled_list()
        self._update_draw_buttons()

    def _select_label(self, name, row):
        self.scene.current_label = name
        self._update_draw_buttons()
        for n, r in self._label_buttons.items():
            _set_row_background(r, n == name)

    def _add_label_clicked(self):
        dlg = AddLabelDialog(self, db=self.db, project=self.project,
                             dataset=self.dataset)
        if dlg.exec() != QDialog.Accepted:
            return
        items = dlg.result_data()
        if not items:
            MessageBox.warning(self, self.tr("添加标签"),
                               self.tr("标签名称不能为空"))
            return
        # 导入路径: 重复标签跳过(不覆盖已有颜色/标注);手动输入仍按原逻辑
        existing = set(self.label_colors)
        imported = getattr(dlg, "_imported_mode", False)
        added = []
        for name, color in items:
            if imported and name in existing:
                continue
            self.db.add_dataset_label(self.project, self.dataset, name, color)
            write_log("创建标签: {} 颜色={} ({}/{})".format(
                name, color, self.project, self.dataset))
            self.label_colors[name] = color
            self.scene.label_colors[name] = QColor(color)
            added.append(name)
        if not added:
            return
        self._refresh_labels()
        self.scene.current_label = added[0]
        self._update_draw_buttons()

    def _refresh_labeled_list(self):
        """
        右侧"标注信息"列表: 每行与场景框双向联动, 显示宽×高/顶点数 + 面积 px².
        行复用优化: 已有行只更新内容(不 deleteLater 重建), 仅数量变化时增删,
        避免框多时每次操作(拖动/缩放触发 boxes_changed)重建数百控件.
        """
        container = self.ui.scrollAreaWidgetContents_2
        layout = container.layout() if container.layout() else QVBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        for i in range(layout.count() - 1, -1, -1):
            it = layout.itemAt(i)
            if it is not None and it.spacerItem():
                layout.takeAt(i)
        items_with_area = []
        for item in self.scene.all_items():
            if isinstance(item, AnnotationBoxItem):
                x1, y1, x2, y2 = item.boxes()
                area = (x2 - x1) * (y2 - y1)
            else:
                area = self._polygon_area(item.points())
            items_with_area.append((area, item))
        items_with_area.sort(key=lambda kv: kv[0], reverse=True)
        rows_data = []
        for area, item in items_with_area:
            if isinstance(item, AnnotationBoxItem):
                x1, y1, x2, y2 = item.boxes()
                kind = self.tr("矩形")
                size_text = "{} × {}".format(int(round(x2 - x1)),
                                             int(round(y2 - y1)))
                area_text = "{:,} px²".format(int(round((x2 - x1) * (y2 - y1))))
            else:  # AnnotationPolygonItem
                pts = item.points()
                kind = self.tr("多边形")
                size_text = self.tr("{} 个顶点").format(len(pts))
                area_text = "{:,} px²".format(int(round(area))) if area else "-"
            color = self._resolve_item_color(item)
            rows_data.append((item, kind, size_text, area_text, color))
        old_rows = list(getattr(self, "_labeled_rows", {}).values())
        new_map = {}
        for i, (item, kind, size_text, area_text, color) in enumerate(rows_data):
            if i < len(old_rows):
                row = old_rows[i]
                self._update_labeled_row(row, item, kind, size_text, area_text, color)
            else:
                row = self._create_labeled_row(item, kind, size_text, area_text, color)
            # 按新排序重排位置
            layout.removeWidget(row)
            layout.insertWidget(i, row)
            new_map[item] = row
        # 多余旧行删除
        for row in old_rows[len(rows_data):]:
            layout.removeWidget(row)
            row.deleteLater()
        self._labeled_rows = new_map
        layout.addStretch(1)
        self._sync_labeled_selection()

    def _create_labeled_row(self, item, kind, size_text, area_text, color):
        """新建一行标注列表项; 子控件引用挂到 row._payload 供复用更新."""
        container = self.ui.scrollAreaWidgetContents_2
        row = QFrame(container)
        row.setFrameShape(QFrame.NoFrame)
        row.setObjectName("labelRow")
        row.setCursor(Qt.PointingHandCursor)
        vl = QVBoxLayout(row)
        vl.setContentsMargins(8, 6, 8, 6)
        vl.setSpacing(2)
        top = QHBoxLayout()
        top.setSpacing(8)
        dot = QLabel(row)
        dot.setFixedSize(12, 12)
        dot.setPixmap(self._label_icon(color).pixmap(12, 12))
        dot.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        top.addWidget(dot)
        name_lbl = QLabel(item.label, row)
        name_lbl.setObjectName("labelRowName")
        name_lbl.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        top.addWidget(name_lbl)
        kind_lbl = QLabel("({})".format(kind), row)
        kind_lbl.setObjectName("labelRowKind")
        kind_lbl.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        top.addWidget(kind_lbl)
        top.addStretch(1)
        vl.addLayout(top)
        info_lbl = QLabel("{} · {}".format(size_text, area_text), row)
        info_lbl.setObjectName("labelRowInfo")
        info_lbl.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        vl.addWidget(info_lbl)
        row._payload = {"dot": dot, "name": name_lbl,
                        "kind": kind_lbl, "info": info_lbl}
        row.mousePressEvent = self._make_labeled_row_click(item, row)
        return row

    def _update_labeled_row(self, row, item, kind, size_text, area_text, color):
        """行复用: 只更新内容 + 重绑点击闭包(当前行可能对应别的 item)."""
        p = row._payload
        p["dot"].setPixmap(self._label_icon(color).pixmap(12, 12))
        p["name"].setText(item.label)
        p["kind"].setText("({})".format(kind))
        p["info"].setText("{} · {}".format(size_text, area_text))
        row.mousePressEvent = self._make_labeled_row_click(item, row)

    def _resolve_item_color(self, item):
        if item._color is not None:
            try:
                return item._color.name()
            except Exception:
                pass
        return label_color(item.label).name()

    def _make_labeled_row_click(self, item, row):
        def _on_click(ev, _it=item, _row=row):
            self.scene.select_item(_it)
            self._sync_labeled_selection()
            try:
                self._focus_on_item(_it)
            except Exception:
                pass
        return _on_click

    def _focus_on_item(self, item):
        if isinstance(item, AnnotationBoxItem):
            scene_rect = item.rect().translated(item.pos()).adjusted(-20, -20, 20, 20)
        else:
            poly = item.polygon().translated(item.pos())
            scene_rect = poly.boundingRect().adjusted(-30, -30, 30, 30)
        self.view.ensureVisible(scene_rect, 60, 60)

    def _sync_labeled_selection(self, _sel=None):
        """
        场景选中 → 同步右侧行高亮(与左侧标签列表同款底色).
        只改"状态变化的那两行": 右侧列表可能有上千行, 每次全量 setStyleSheet
        会触发整行 unpolish/polish, 是框多时卡顿的主因之一.
        """
        sel = _sel if _sel is not None else self.scene.selected_item()
        self._sync_brightness_for(sel)
        row = self._labeled_rows.get(sel)
        if row is self._labeled_sel_row:
            return
        _set_row_background(self._labeled_sel_row, False)
        _set_row_background(row, True)
        self._labeled_sel_row = row

    def _sync_brightness_for(self, item):
        """
        换选标注 → 亮度滑块摆到这个框自己的值(没调过的一律 0.50).
        上一个框调的亮度不能顺延: 停在 0.80 时点另一个多边形, 再拖一下就把新框也调亮了,
        而用户看到的滑块还以为是 0.50.
        """
        v = self.scene.brightness_of(item) if item is not None \
            else float(BRIGHTNESS_DEFAULT)
        self.ui.brightness_lineEdit.setText("{:.2f}".format(v))
        slider = self.ui.brightness_slider
        slider.blockSignals(True)
        slider.setValue(int(round(v * 100)))
        slider.blockSignals(False)

    @staticmethod
    def _polygon_area(points):
        """shoelace 公式计算多边形面积(像素²), 顶点数 <3 返回 0."""
        n = len(points)
        if n < 3:
            return 0.0
        s = 0.0
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            s += x1 * y2 - x2 * y1
        return abs(s) / 2.0

    def _save_current(self, commit_pending=False):
        """
        仅在用户改动过标注(_dirty)时保存; 未改动不写文件.
        保存内容包括: 画/删/改标签/拖动缩放等触发的 boxes_changed;
        格式刷粘贴修改过图像像素时, 一并把图像写盘.

        commit_pending 只在用户显式要求保存时给(Ctrl+S / 切图 / 关闭 / 删图):
        浮动粘贴挨到这一刻才写进图像像素. 自动保存(150ms 定时器)不带它 ——
        否则刚粘上去就被烧进图里, 根本没机会拖到位.
        """
        if commit_pending:
            # 亮度只在用户显式保存时落地: 让自动保存(150ms)也带上的话, 拖一下就写一次盘
            self._commit_brightness()
            if self._bright_unsaved:
                self._bright_unsaved = False
                self._pix_unsaved = True
                self._dirty = True
            self.scene.commit_pastes()
        elif self.scene.has_pending_pastes():
            # 还有浮层没落地就写盘的话, json 里会有标注、图像里却没有对应图案
            return
        if not self._dirty:
            return
        if not (0 <= self.index < len(self.image_list)):
            return
        image_path = self.image_list[self.index]
        # 缓存里那份是改写前的拷贝, 必须换成刚写盘的内容, 否则翻回来看到旧图
        if self._pix_unsaved:
            item = getattr(self.scene, "image_item", None)
            item_pix = item.pixmap() if item is not None else None
            if item_pix is not None and not item_pix.isNull():
                if item_pix.save(image_path):
                    self._pix_unsaved = False
                else:
                    # 写失败保留标记, 下次再试, 避免静默丢改动
                    write_log("图像写盘失败(像素改动未保存): {}".format(image_path))
        base, _ = os.path.splitext(image_path)
        json_path = base + ".json"
        shapes = []
        for box in self.scene.boxes():
            if box.get("shape_type") == "polygon":
                shapes.append({
                    "label": box["label"], "points": box["points"],
                    "group_id": None, "shape_type": "polygon", "flags": {},
                })
            else:
                x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
                shapes.append({
                    "label": box["label"],
                    "points": [[x1, y1], [x2, y2]],
                    "group_id": None, "shape_type": "rectangle", "flags": {},
                })
        cur_pix = self.scene.image_item.pixmap()
        img_w = cur_pix.width() if cur_pix is not None else None
        img_h = cur_pix.height() if cur_pix is not None else None
        if shapes:
            save_labelme(image_path, shapes, width=img_w, height=img_h)
        else:
            save_labelme(image_path, [], width=img_w, height=img_h)
        self._modified_paths.add(image_path)
        self._dirty = False


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
            self._checked = not self._checked
            self.toggled.emit(self._checked)
            self.update()
            event.accept()
            return
        super().mousePressEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        track = QColor("#4f7dff") if self._checked else QColor("#3a3f4e")
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

    def __init__(self, initial=QColor("#4f7dff"), parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("选择颜色"))
        self._color = QColor(initial) if initial.isValid() else QColor("#4f7dff")

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
            btn.setStyleSheet("QPushButton { background: %s; border: 1px solid #3a3f4e; border-radius: 3px; }" % c)
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
            "QFrame { background: %s; border: 1px solid #3a3f4e; border-radius: 4px; }" % c.name())
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
