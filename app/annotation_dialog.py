# -*- coding: utf-8 -*-
"""标注对话框：封装 ui/annotation.py + annotation 引擎。
- 矩形/多边形标注（颜色 = 标签颜色，支持中文标签）
- 左侧标签列表（点击切换当前标签），添加标签弹窗（10 默认色 + 自定义色 + 跨数据集导入）
- A/D 切换上一张/下一张，切换/关闭时保存 labelme json（图像同路径）
"""
import os
import json
import re
import shutil

from PIL import Image

from PySide6.QtCore import Qt, Signal, QPointF, QTimer, QSize
from PySide6.QtGui import (QColor, QPixmap, QKeySequence, QShortcut, QPen,
                           QPainter, QImage, QIcon, QCursor, QLinearGradient,
                           QFont)
from PySide6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QGridLayout, QLineEdit, QSpinBox, QPushButton, QFrame,
                               QSlider, QMenu, QGraphicsTextItem)

from ui.annotation import Ui_annotationDialog as AnnotationUI
from ui.add_label import Ui_addLabelDialog as AddLabelUI

from app.annotation.scene import AnnotationScene
# from app.annotation.view import AnnotationView
from app.annotation.box_item import (AnnotationBoxItem, AnnotationPolygonItem,
                                     LABEL_COLORS, label_color)
from app.label_utils import normalize_label, label_sort_key
from app.message_box import MessageBox
from app.log import write_log

# import types
from PySide6.QtWidgets import QGraphicsView


def _resource_path(name):
    """resources/ 目录下资源绝对路径（不存在返回空串）。"""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(root, "resources", name)
    return p if os.path.exists(p) else ""


def _upgrade_graphics_view(view):
    """
    把image_label_show(QGraphicsView)提升为 AnnotationView 行为;
    挂 AnnotationScene + 安装滚轮缩放/中键平移/快捷键/右键删除等方法，
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
    view._space_down = False
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
            _v._space_down = True
            _v.setDragMode(QGraphicsView.ScrollHandDrag)
            ev.accept()
            return
        QGraphicsView.keyPressEvent(_v, ev)
    view.keyPressEvent = _key_press

    def _key_release(ev, _v=view):
        if ev.key() == Qt.Key_Space:
            _v._space_down = False
            _v.setDragMode(QGraphicsView.NoDrag)
            ev.accept()
            return
        QGraphicsView.keyReleaseEvent(_v, ev)
    view.keyReleaseEvent = _key_release

    def _ctx_menu(ev, _v=view):
        scene_pos = _v.mapToScene(ev.pos())
        hit = _v.scene().itemAt(scene_pos, _v.transform())
        if isinstance(hit, (AnnotationBoxItem, AnnotationPolygonItem)):
            menu = QMenu(_v)
            menu.addAction("删除该标注", lambda: _v.scene().delete_item(hit))
            menu.exec(ev.globalPos())
            ev.accept()
            return
        QGraphicsView.contextMenuEvent(_v, ev)
    view.contextMenuEvent = _ctx_menu

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


IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


class _ClsLabelItem(QGraphicsTextItem):
    """图像分类数据集：图像中央显示类别名，点击弹出菜单修改类别(复用 label_change_requested)。"""

    def __init__(self, text, color, font_size=15):
        super().__init__(text)
        self.label = text
        self.setDefaultTextColor(QColor(color) if color else QColor("white"))
        self.setFont(QFont("Microsoft YaHei", font_size, QFont.Bold))
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
    """读取 labelme json → [{label, x1,y1,x2,y2} 或 {label, points, shape_type}]。"""
    if not os.path.exists(json_path):
        return []
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []
    boxes = []
    for shape in data.get("shapes", []):
        label = normalize_label(shape.get("label", "object"))
        pts = shape.get("points") or []
        if shape.get("shape_type") == "polygon":
            boxes.append({"label": label, "points": [[float(p[0]), float(p[1])] for p in pts],
                          "shape_type": "polygon"})
        elif len(pts) >= 2:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            boxes.append({"label": label, "x1": min(xs), "y1": min(ys),
                          "x2": max(xs), "y2": max(ys)})
    return boxes


def _load_import_label(image_path, label_path, fmt):
    """
    从导入绑定的标签目录读取标签框（yolo txt / labelme json）。
    label_path 可为 str 或 list（多路径导入：依次查找同名标签文件）。
    与 _load_labelme 返回相同格式的 boxes 列表；无标签/目录无效返回 []。
    用于: 导入带标注的图像进入标注界面时显示导入的标注框
    （标注系统的 labelme json 保存在图像同路径，而导入标签在 label_path 目录）。
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
    iw = ih = 0
    try:
        with Image.open(image_path) as im:
            iw, ih = im.size
    except Exception:
        pass
    boxes = []
    try:
        if fmt == ".txt":
            with open(label_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) < 5:
                        continue
                    try:
                        vals = [float(x) for x in parts]
                    except ValueError:
                        continue
                    label = normalize_label(parts[0].strip())
                    if len(vals) == 5:
                        # 检测格式:cls cx cy w h
                        _, cx, cy, w, h = vals
                        boxes.append({"label": label, "x1": (cx - w / 2) * iw,
                                      "y1": (cy - h / 2) * ih,
                                      "x2": (cx + w / 2) * iw,
                                      "y2": (cy + h / 2) * ih})
                    elif (len(vals) - 1) % 2 == 0:
                        # 分割格式: cls x1 y1 x2 y2 ... xn yn(点数偶数)
                        pts = [(vals[1 + 2 * i] * iw, vals[2 + 2 * i] * ih)
                               for i in range((len(vals) - 1) // 2)]
                        boxes.append({"label": label, "points": pts,
                                      "shape_type": "polygon"})
                    else:
                        # 列数异常:降级用 bbox
                        x_coords = [vals[1 + 2 * i] for i in range(len(vals) // 2)]
                        y_coords = [vals[2 + 2 * i] for i in range(len(vals) // 2)]
                        boxes.append({"label": label, "x1": min(x_coords) * iw,
                                      "y1": min(y_coords) * ih,
                                      "x2": max(x_coords) * iw,
                                      "y2": max(y_coords) * ih})
        else:
            # labelme json(在标签目录)
            with open(label_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for shape in data.get("shapes", []):
                label = normalize_label(shape.get("label", "object"))
                pts = shape.get("points") or []
                if shape.get("shape_type") == "polygon":
                    boxes.append({"label": label,
                                  "points": [[float(p[0]), float(p[1])] for p in pts],
                                  "shape_type": "polygon"})
                elif len(pts) >= 2:
                    xs = [p[0] for p in pts]
                    ys = [p[1] for p in pts]
                    boxes.append({"label": label, "x1": min(xs), "y1": min(ys),
                                  "x2": max(xs), "y2": max(ys)})
    except Exception:
        return []
    return boxes


def save_labelme(image_path, shapes, version="5.0.1"):
    """保存 labelme json 到图像同路径（*.json）。"""
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
    """添加标签弹窗:名称输入 + 10 个默认色按钮 + 自定义颜色 + 同项目标签导入。

    通过 load_project_label_combo 选择同项目其他数据集，点击 load_label_btn
    导入该数据集已有标签（逗号分隔填入输入框），确定后批量入库并沿用源颜色。
    """

    def __init__(self, parent=None, preset_name="", preset_color="",
                 db=None, project="", dataset=""):
        super().__init__(parent)
        self.ui = AddLabelUI()
        self.ui.setupUi(self)
        self.setWindowTitle("添加标签")
        self._db = db
        self._project = project
        self._dataset = dataset
        self._source_colors = {}   # 导入的数据集标签 → 颜色（用于确定时还原颜色）
        self._selected_color = ""
        self._imported_mode = False   # 本次弹窗是否走"导入"路径（导入后输入框只读）
        self._setup()
        if preset_name:
            self.ui.input_label_name_txt.setText(preset_name)
        if preset_color:
            self._select_color(preset_color)

    def _setup(self):
        BTN_H = 36
        self._color_btns = [getattr(self.ui, "color{}_btn".format(i)) for i in range(1, 11)]
        for btn, color in zip(self._color_btns, LABEL_COLORS[:10]):
            btn.setFixedHeight(BTN_H)
            btn.setStyleSheet(
                "QPushButton {{ background-color: {0}; border: 2px solid transparent;"
                " border-radius: 6px; }}".format(color))
            btn.clicked.connect(lambda _=False, c=color, b=btn: self._select_color(c, b))
        # 自定义颜色按钮
        self.ui.custom_color.setText("自定义")
        self.ui.custom_color.setFixedHeight(BTN_H)
        icon_path = _resource_path("颜色选择器.png")
        if icon_path:
            self.ui.custom_color.setIcon(QIcon(icon_path))
            self.ui.custom_color.setIconSize(QSize(20, 20))
        self.ui.custom_color.clicked.connect(self._pick_custom_color)
        # 确定按钮
        self.ui.add_label_done_btn.setText("确定")
        self.ui.add_label_done_btn.clicked.connect(self.accept)
        self.ui.select_color.setText("选择")
        self.ui.color10_btn_2.setFixedHeight(36)
        self.ui.color10_btn_2.setStyleSheet(
            "QPushButton {{ background-color: {0}; border: 2px solid #3a3f4d;"
            " border-radius: 6px; }}".format(self._selected_color or "#5B8CFF"))
        self.ui.input_label_name_txt.setPlaceholderText(
            "标签名称，多个用逗号分隔")
        # 同项目标签导入
        self._fill_project_label_combo()
        self.ui.load_label_btn.setText("导入")
        self.ui.load_label_btn.clicked.connect(self._load_labels_from_project)

    def _fill_project_label_combo(self):
        """填充同项目其他数据集的标签（单选）：排除当前数据集，只列有标签的。"""
        combo = self.ui.load_project_label_combo
        combo.clear()
        combo.addItem("选择数据集…", None)
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
        """把所选数据集的标签以逗号分隔填入输入框，并记住其颜色。

        导入后输入框置为只读（导入的标签以源数据集为准，不允许手动改动），
        数据仅在用户点「确定」后才写入当前数据集。
        """
        combo = self.ui.load_project_label_combo
        src = combo.currentData()
        if not src:
            MessageBox.warning(self, "导入标签", "请先选择一个数据集")
            return
        labels = self._db.get_dataset_labels(self._project, src)
        if not labels:
            MessageBox.warning(self, "导入标签",
                               "数据集「{}」还没有标签".format(src))
            return
        self._source_colors = dict(labels)
        names = sorted(labels.keys(), key=label_sort_key)
        self.ui.input_label_name_txt.setText(", ".join(names))
        self.ui.input_label_name_txt.setReadOnly(True)
        self._imported_mode = True
        # 导入模式下颜色由源数据集决定，禁用颜色按钮避免无效点击
        for btn in self._color_btns:
            btn.setEnabled(False)
        self.ui.custom_color.setEnabled(False)
        self.ui.color10_btn_2.setEnabled(False)

    def _select_color(self, color, btn=None):
        self._selected_color = color
        self.ui.color10_btn_2.setStyleSheet(
            "QPushButton {{ background-color: {0}; border: 2px solid #3a3f4d;"
            " border-radius: 6px; }}".format(color))
        # 高亮选中按钮
        for i in range(1, 11):
            b = getattr(self.ui, "color{}_btn".format(i))
            border = "2px solid #ffffff" if (btn is not None and b is btn) else "2px solid transparent"
            b.setStyleSheet(
                "QPushButton {{ background-color: {0}; border: {1}; border-radius: 6px; }}".format(
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
        color = ColorPickerDialog.get_color(QColor(self._selected_color or "#5B8CFF"), self)
        if color.isValid():
            self._select_color(color.name())

    def result_data(self):
        """返回 [(name, color), ...]。多个标签以逗号分隔。

        颜色优先取导入数据集的源颜色（_source_colors），
        否则用当前选中颜色，再否则按 label_color 哈希确定性分配。
        """
        text = self.ui.input_label_name_txt.text().strip()
        if not text:
            return []
        names = [n.strip() for n in re.split(r"[,\uff0c]+", text) if n.strip()]
        items = []
        for n in names:
            color = self._source_colors.get(n) or self._selected_color or ""
            if not color:
                color = label_color(n).name()
            items.append((n, color))
        return items


class AnnotationDialog(QDialog):
    """标注主对话框：加载图像 + 已有标注，支持矩形/多边形绘制、标签管理、A/D 切换保存。"""

    def __init__(self, image_list, current_index, db, project, dataset, parent=None,
                 label_path="", label_fmt="", cls_mode=False):
        super().__init__(parent)
        self.setObjectName("AnnotationDialog")
        self.db = db
        self.project = project
        self.dataset = dataset
        self.label_path = label_path
        self.label_fmt = label_fmt
        self.cls_mode = cls_mode
        self._cls_changes = []
        self._deleted_labels = []   # 本次会话删除的标签（供主界面清理缓存）
        self.image_list = list(image_list) if image_list else []
        self.index = current_index
        self.view = None
        self.scene = None
        self._label_buttons = {}
        self._dirty = False
        self.label_colors = dict(self.db.get_dataset_labels(project, dataset))

        self.ui = AnnotationUI()
        self.ui.setupUi(self)
        self.setWindowTitle("标注 - {} / {}".format(project, dataset))
        self._replace_view()
        self._setup_ui()
        self._setup_shortcuts()
        self.scene.label_colors = {k: QColor(v) for k, v in self.label_colors.items()}
        self._refresh_labels()
        self._load_current()

    def _replace_view(self):
        """在用户设计的 image_label_show 控件上启用标注能力（不新增控件）。"""
        self.view = _upgrade_graphics_view(self.ui.image_label_show)
        self.scene = self.view.scene_

    def _setup_ui(self):
        u = self.ui
        u.draw_rect_btn.setText("矩形")
        u.poly_btn.setText("多边形")
        u.add_label.setText("添加标签")
        u.label_list.setText("标签列表")
        u.labeled_list.setText("当前图像标注")
        u.pre_page_btn.setText("上一张")
        u.next_page_btn.setText("下一张")
        u.lineEdit.hide()
        u.draw_rect_btn.clicked.connect(lambda: self._start_draw("rect"))
        u.poly_btn.clicked.connect(lambda: self._start_draw("polygon"))
        u.format_painter_btn.clicked.connect(self._toggle_format_painter)
        u.switchButton = SwitchButton(self)
        u.switchButton.setObjectName("switchButton")
        u.switchButton.setChecked(True)
        u.switchButton.toggled.connect(self._toggle_show_boxes)
        u.show_boxes_label = QLabel("显示标注", self)
        u.show_boxes_label.setObjectName("show_boxes_label")
        u.show_boxes_label.setStyleSheet("color: #cfd6e4; font-size: 13px;")
        idx = u.horizontalLayout.indexOf(u.format_painter_btn)
        u.horizontalLayout.insertWidget(idx + 1, u.switchButton)
        u.horizontalLayout.insertWidget(idx + 2, u.show_boxes_label)
        u.add_label.clicked.connect(self._add_label_clicked)
        u.pre_page_btn.clicked.connect(lambda: self._switch(-1))
        u.next_page_btn.clicked.connect(lambda: self._switch(1))
        self.scene.box_drawn.connect(self._on_box_drawn)
        self.scene.fp_mode_changed.connect(self._on_fp_mode_changed)
        self._labeled_refresh_timer = QTimer(self)
        self._labeled_refresh_timer.setSingleShot(True)
        self._labeled_refresh_timer.timeout.connect(self._refresh_labeled_list)
        self.scene.boxes_changed.connect(self._on_boxes_changed)
        self.scene.label_change_requested.connect(self._on_label_change_requested)
        self.scene.selection_changed.connect(self._sync_labeled_selection)
        # 图像分类数据集:只读看图,禁用一切标注/绘制控件
        if self.cls_mode:
            for w in (u.draw_rect_btn, u.poly_btn, u.format_painter_btn,
                      u.add_label):
                w.setEnabled(False)

    def _on_boxes_changed(self):
        """
        标注内容变化(画/删/改类别/拖动缩放)→ 标记 dirty + 刷新右侧列表。
        load_boxes 加载时也会 emit boxes_changed，但 _loading=True 期间不标记。
        """
        if not getattr(self, "_loading", False):
            self._dirty = True
        self._labeled_refresh_timer.start()

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("A"), self, activated=lambda: self._switch(-1))
        QShortcut(QKeySequence("D"), self, activated=lambda: self._switch(1))
        QShortcut(QKeySequence("Delete"), self, activated=self.scene.delete_selected)
        QShortcut(QKeySequence("Ctrl+Z"), self, activated=self._undo_fp_paste)
        QShortcut(QKeySequence(Qt.Key_Escape), self, activated=self._cancel_draw_mode)

    def _apply_draw_mode_cursor(self):
        """按当前画模式状态同步 view 光标(画模式十字 / 编辑模式恢复)。"""
        if self.scene.draw_mode:
            self.view.setCursor(Qt.CrossCursor)
        else:
            self.view.unsetCursor()

    def _load_current(self):
        if not (0 <= self.index < len(self.image_list)):
            return
        self._apply_draw_mode_cursor()
        image_path = self.image_list[self.index]
        pix = QPixmap(image_path)
        if pix.isNull():
            return
        self.scene.set_image(pix)
        base, _ = os.path.splitext(image_path)
        if self.cls_mode:
            # 图像分类：只读看图,无框可标注;类别 = 父文件夹名
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
            boxes = _load_labelme(base + ".json")
            if not boxes:
                boxes = _load_import_label(image_path, self.label_path, self.label_fmt)
        self._loading = True
        try:
            self.scene.load_boxes(boxes)
        finally:
            self._loading = False
        # A/D 切图保持"显示标注"开关状态(关闭时隐藏标注框)
        show = getattr(self.ui, "switchButton", None) is not None and self.ui.switchButton.isChecked()
        if not show:
            for item in self.scene.all_items():
                item.setVisible(False)
        self._ensure_label_colors(boxes)
        QTimer.singleShot(0, self.view.fit_window)
        channels = {
            QImage.Format_Grayscale8: 1,
            QImage.Format_Grayscale16: 1,
            QImage.Format_RGB888: 3,
            QImage.Format_RGB32: 3,
            QImage.Format_ARGB32: 4,
            QImage.Format_RGBA8888: 4,
        }.get(pix.toImage().format(), 3)
        self.ui.image_info_label.setText(
            "{} × {} × {}    ({}/{}){}".format(
                pix.width(), pix.height(), channels,
                self.index + 1, len(self.image_list),
                "    类别: {}".format(cls) if self.cls_mode else ""))
        self._refresh_labeled_list()
        self._dirty = False

    def _switch(self, offset):
        if not self.image_list:
            return
        self._save_current()
        new_index = self.index + offset
        if not (0 <= new_index < len(self.image_list)):
            return
        self.index = new_index
        self._load_current()

    def _ensure_label_colors(self, boxes):
        """
        确保 boxes 中所有标签都在 db / label_colors 中。
        缺失的标签（如手动创建 labelme json 里的新标签）用确定性哈希色
        label_color() 入库，保证：同一标签在 A/D 翻页时颜色一致，
        且首页标签下拉框/下次启动都能看到
        """
        changed = False
        for b in boxes:
            # 归一化：历史 json 里的 class_N → N,防止 class_ 标签重新入库
            lbl = normalize_label(b.get("label"))
            if lbl and lbl not in self.label_colors:
                color = label_color(lbl).name()
                self.db.add_dataset_label(self.project, self.dataset, lbl, color)
                self.label_colors[lbl] = color
                self.scene.label_colors[lbl] = QColor(color)
                changed = True
        if changed:
            self._refresh_labels()

    def closeEvent(self, event):
        self._save_current()
        super().closeEvent(event)

    def _update_draw_buttons(self):
        """无标签或未选中标签时禁用矩形/多边形/格式刷按钮。"""
        if self.cls_mode:
            # 图像分类只读,始终禁用绘制
            for w in (self.ui.draw_rect_btn, self.ui.poly_btn,
                      self.ui.format_painter_btn):
                w.setEnabled(False)
            return
        can_draw = bool(self.label_colors) and self.scene.current_label in self.label_colors
        self.ui.draw_rect_btn.setEnabled(can_draw)
        self.ui.poly_btn.setEnabled(can_draw)
        self.ui.format_painter_btn.setEnabled(can_draw)
        if not can_draw:
            self._set_draw_button_states(False)

    def _start_draw(self, shape):
        if self.scene.fp_mode is not None:
            self.scene.set_format_painter(False)
        self.scene.set_draw_mode(True, shape)
        self.view.setCursor(Qt.CrossCursor)
        self._set_draw_button_states(True)
        if not self.label_colors:
            MessageBox.information(self, "添加标签", "请先添加标签(点击「添加标签」)")

    def _set_draw_button_states(self, drawing):
        style_off = ("QPushButton { background: #2a2e3a; color: #cfd6e4;"
                     " border: 1px solid #3a3f4d; border-radius: 6px; padding: 6px 14px; }")
        style_on = ("QPushButton { background: #2c3a5e; color: #ffffff;"
                    " border: 1px solid #5b8cff; border-radius: 6px; padding: 6px 14px; }")
        self.ui.draw_rect_btn.setStyleSheet(style_on if (drawing and self.scene.draw_shape == "rect") else style_off)
        self.ui.poly_btn.setStyleSheet(style_on if (drawing and self.scene.draw_shape == "polygon") else style_off)

    def _on_box_drawn(self):
        """画完一个框：保持画模式（需求：只有 ESC 才退出），维持十字光标与按钮高亮。"""
        self.view.setCursor(Qt.CrossCursor)
        self._set_draw_button_states(True)

    def _cancel_draw_mode(self):
        """主动退出画模式（不创建标注）：恢复光标 + 按钮样式。"""
        if self.scene.fp_mode is not None:
            self.scene.set_format_painter(False)
        self.scene.set_draw_mode(False)
        self.scene._cancel_polygon()
        self.view.unsetCursor()
        self._set_draw_button_states(False)

    # ---------------- 格式刷(轨迹描边 -> 模板 -> 刷子粘贴) ----------------
    def _toggle_show_boxes(self, checked):
        """"显示标注"开关：关闭时隐藏图像上的标注框，右侧列表信息保留。"""
        for item in self.scene.all_items():
            item.setVisible(checked)

    def _toggle_format_painter(self):
        if self.scene.fp_mode is not None:
            self.scene.set_format_painter(False)
            return
        if not self.label_colors or self.scene.current_label not in self.label_colors:
            MessageBox.information(self, "格式刷", "请先选择一个标签")
            return
        if self.scene.draw_mode:
            self.scene.set_draw_mode(False)
        self.scene.set_format_painter(True)
        self.view.setCursor(self._fp_circle_cursor())
        self._set_draw_button_states(False)
        self.ui.format_painter_btn.setStyleSheet(self._style_on())

    def _undo_fp_paste(self):
        """Ctrl+Z：撤销最后一次格式刷粘贴（恢复图像像素 + 删标注）。"""
        if self.scene.undo_last_paste():
            self._refresh_labeled_list()

    def _on_fp_mode_changed(self, mode):
        if mode == "trace":
            self.view.setCursor(self._fp_circle_cursor())
            self.ui.format_painter_btn.setStyleSheet(self._style_on())
        elif mode == "paint":
            self.view.setCursor(self._fp_brush_cursor())
            self.ui.format_painter_btn.setStyleSheet(self._style_on())
        else:  # 退出
            self.view.unsetCursor()
            self._set_draw_button_states(False)
            self.ui.format_painter_btn.setStyleSheet(self._style_off())

    def _style_on(self):
        return ("QPushButton { background: #2c3a5e; color: #ffffff;"
                " border: 1px solid #5b8cff; border-radius: 6px; padding: 6px 14px; }")

    def _style_off(self):
        return ("QPushButton { background: #2a2e3a; color: #cfd6e4;"
                " border: 1px solid #3a3f4d; border-radius: 6px; padding: 6px 14px; }")

    @staticmethod
    def _fp_circle_cursor():
        """轨迹绘制光标:直径 20px 的蓝色圆圈(屏幕像素，热点居中)。"""
        pm = QPixmap(20, 20)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor("#5B8CFF"), 2))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(1, 1, 17, 17)
        p.end()
        return QCursor(pm, 10, 10)

    @staticmethod
    def _fp_brush_cursor():
        """刷子粘贴光标：蓝色刷头 + 手柄。"""
        pm = QPixmap(24, 24)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor("#5B8CFF"), 1.5))
        p.setBrush(QColor(91, 140, 255, 90))
        p.drawEllipse(2, 3, 12, 10)          # 刷头
        p.drawLine(12, 12, 19, 19)           # 手柄
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#5B8CFF"))
        p.drawRect(15, 17, 8, 6)             # 刷毛底座
        p.end()
        return QCursor(pm, 6, 6)

    def _label_icon(self, color):
        """标签颜色圆点图标(下拉菜单用)。"""
        pm = QPixmap(16, 16)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(color))
        p.drawEllipse(2, 2, 12, 12)
        p.end()
        return QIcon(pm)

    def _on_label_change_requested(self, item):
        """点击标注框上的标签 chip → 弹出所有标签下拉，选择后修改该框类别。"""
        if not self.label_colors:
            return
        menu = QMenu(self)
        # 与首页下拉框一致: 纯数字数值排序,其他按字符串
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
                # 分类数据集:点击中央类别名 -> 修改类别(移动文件)
                self._change_cls(chosen.text())
            else:
                self.scene.set_item_label(item, chosen.text())

    def _change_cls(self, new_cls):
        """分类数据集：把当前图像移动到新类别文件夹，记录改动供首页刷新缓存。"""
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
                MessageBox.warning(self, "修改类别", "移动图像文件失败：\n{}".format(old_path))
                return
        self.image_list[self.index] = new_path
        self._cls_changes.append((old_path, new_path, new_cls))
        write_log("分类修改: {} → {} ({})".format(
            old_cls, new_cls, os.path.basename(new_path)))
        self._load_current()

    def _refresh_labels(self):
        """刷新左侧标签列表（颜色块 + 名称），点击切换当前标签。"""
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
        # 按 label_sort_key 排序:纯数字按数值,其他按字符串——与首页下拉框一致
        for name, color in sorted(self.label_colors.items(),
                                  key=lambda kv: label_sort_key(kv[0])):
            row = QFrame(container)
            row.setFrameShape(QFrame.NoFrame)
            row.setStyleSheet("QFrame { background: #232834; border-radius: 6px; }")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(8, 6, 8, 6)
            rl.setSpacing(8)
            # 圆形按钮显示颜色(可点击切换当前标签)
            color_btn = QPushButton(row)
            color_btn.setFixedSize(18, 18)
            color_btn.setCursor(Qt.PointingHandCursor)
            color_btn.setStyleSheet(
                "QPushButton {{ background-color: {0}; border: 1px solid #3a3f4d;"
                " border-radius: 9px; padding: 0px; margin: 0px;"
                " min-width: 0px; max-width: 18px; min-height: 0px; max-height: 18px; }}".format(color))
            color_btn.setToolTip(name)
            color_btn.clicked.connect(lambda _=False, n=name, r=row: self._select_label(n, r))
            rl.addWidget(color_btn)
            name_lbl = QLabel(name, row)
            name_lbl.setStyleSheet("color: #e8eaf0; background: transparent;")
            rl.addWidget(name_lbl)
            rl.addStretch(1)
            row.mousePressEvent = (lambda ev, n=name, r=row: self._select_label(n, r))
            row.setContextMenuPolicy(Qt.CustomContextMenu)
            row.customContextMenuRequested.connect(
                lambda pos, n=name, r=row: self._show_label_context_menu(n, r, pos))
            layout.addWidget(row)
            self._label_buttons[name] = row
        layout.addStretch(1)

    def _show_label_context_menu(self, name, row, pos):
        """标签行右键菜单：删除标签（含其所有标注）。"""
        menu = QMenu(self)
        act_del = menu.addAction("删除标签")
        chosen = menu.exec(row.mapToGlobal(pos))
        if chosen == act_del:
            self._delete_label_from_list(name)

    def _delete_label_from_list(self, name):
        """删除标签并同步清理其标注：db / 本地 labelme json / 当前场景。

        删除前统计该标签在场景和所有可见图像 json 中的标注数；
        有标注时提示影响范围，确认后才执行（删除不可恢复）。

        性能：文件多时弹进度框；先用文本快速检查跳过不含该标签的文件
        （省去 json.load 解析），只有命中的文件才解析+过滤+写回。
        """
        needle = normalize_label(name)
        # 统计并清理所有可见图像 json 中该标签的 shapes（含当前图像）
        removed = 0
        progress = None
        if len(self.image_list) > 50:
            from app.message_box import ProgressDialog
            progress = ProgressDialog("删除标签", "正在清理标注文件…", self,
                                      maximum=len(self.image_list),
                                      cancellable=False)
        try:
            for i, img_path in enumerate(self.image_list):
                if progress is not None:
                    progress.set_progress(i)
                base, _ = os.path.splitext(img_path)
                jp = base + ".json"
                if not os.path.exists(jp):
                    continue
                try:
                    with open(jp, "r", encoding="utf-8") as f:
                        text = f.read()
                    if needle not in text:
                        continue   # 快速跳过：文本不含该标签，无需解析
                    data = json.loads(text)
                    before = len(data.get("shapes", []))
                    data["shapes"] = [s for s in data.get("shapes", [])
                                      if normalize_label(s.get("label")) != needle]
                    if len(data["shapes"]) != before:
                        removed += before - len(data["shapes"])
                        with open(jp, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                except Exception:
                    continue
        finally:
            if progress is not None:
                progress.close()
        # 当前场景中该标签的标注项（json 已清理，场景内仍需删除）
        scene_items = [it for it in self.scene.all_items()
                       if getattr(it, "label", None) == name]
        total = removed + len(scene_items)
        if total > 0:
            if not MessageBox.question(
                    self, "删除标签",
                    "标签「{}」已有 {} 处标注，删除后这些标注将被一并删除"
                    "且不可恢复。\n确定删除吗？".format(name, total),
                    default_yes=True):
                return
        else:
            if not MessageBox.question(
                    self, "删除标签",
                    "确定删除标签「{}」吗？".format(name),
                    default_yes=True):
                return
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
            bg = "#2a3f6b" if n == name else "#232834"
            r.setStyleSheet(
                "QFrame {{ background: {0}; border-radius: 6px; }}".format(bg))

    def _add_label_clicked(self):
        dlg = AddLabelDialog(self, db=self.db, project=self.project,
                             dataset=self.dataset)
        if dlg.exec() != QDialog.Accepted:
            return
        items = dlg.result_data()
        if not items:
            MessageBox.warning(self, "添加标签", "标签名称不能为空")
            return
        # 导入路径：重复标签跳过（不覆盖已有颜色/标注）；手动输入仍按原逻辑
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
        """右侧"当前图像标注"列表：每行与场景框双向联动，显示宽×高/顶点数 + 面积 px²。"""
        container = self.ui.scrollAreaWidgetContents_2
        layout = container.layout() if container.layout() else QVBoxLayout(container)
        while layout.count():
            it = layout.takeAt(0)
            w = it.widget()
            if w is not None:
                w.deleteLater()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        self._labeled_rows = {}
        self._labeled_rev = {}
        # 先按面积降序排序:最大在上,最小在下
        items_with_area = []
        for item in self.scene.all_items():
            if isinstance(item, AnnotationBoxItem):
                x1, y1, x2, y2 = item.boxes()
                area = (x2 - x1) * (y2 - y1)
            else:
                area = self._polygon_area(item.points())
            items_with_area.append((area, item))
        items_with_area.sort(key=lambda kv: kv[0], reverse=True)
        for area, item in items_with_area:
            if isinstance(item, AnnotationBoxItem):
                x1, y1, x2, y2 = item.boxes()
                kind = "矩形"
                w_ = x2 - x1
                h_ = y2 - y1
                size_text = "{} × {}".format(int(round(w_)), int(round(h_)))
                area_text = "{:,} px²".format(int(round(w_ * h_)))
            else:  # AnnotationPolygonItem
                pts = item.points()
                kind = "多边形"
                size_text = "{} 个顶点".format(len(pts))
                area = self._polygon_area(pts)
                area_text = "{:,} px²".format(int(round(area))) if area else "—"
            color = self._resolve_item_color(item)
            row = QFrame(container)
            row.setFrameShape(QFrame.NoFrame)
            row.setStyleSheet("QFrame { background: #232834; border-radius: 6px; }")
            row.setCursor(Qt.PointingHandCursor)
            vl = QVBoxLayout(row)
            vl.setContentsMargins(8, 6, 8, 6)
            vl.setSpacing(2)
            # 第一行: 圆点 + 标签名 + 类型
            top = QHBoxLayout()
            top.setSpacing(8)
            dot = QLabel(row)
            dot.setFixedSize(12, 12)
            dot.setPixmap(self._label_icon(color).pixmap(12, 12))
            dot.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            top.addWidget(dot)
            name_lbl = QLabel(item.label, row)
            name_lbl.setStyleSheet("color: #e8eaf0; background: transparent; font-weight: 600;")
            name_lbl.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            top.addWidget(name_lbl)
            kind_lbl = QLabel("({})".format(kind), row)
            kind_lbl.setStyleSheet("color: #8a92a3; background: transparent;")
            kind_lbl.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            top.addWidget(kind_lbl)
            top.addStretch(1)
            vl.addLayout(top)
            info_lbl = QLabel("{} · {}".format(size_text, area_text), row)
            info_lbl.setStyleSheet("color: #8a92a3; background: transparent; font-size: 11px;")
            info_lbl.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            vl.addWidget(info_lbl)
            layout.addWidget(row)
            self._labeled_rows[item] = row
            self._labeled_rev[row] = item
            row.mousePressEvent = self._make_labeled_row_click(item, row)
        layout.addStretch(1)
        self._sync_labeled_selection()

    def _resolve_item_color(self, item):
        """取 item 当前显示色"""
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
        """视图滚到 item 可见区域"""
        if isinstance(item, AnnotationBoxItem):
            scene_rect = item.rect().translated(item.pos()).adjusted(-20, -20, 20, 20)
        else:
            poly = item.polygon().translated(item.pos())
            scene_rect = poly.boundingRect().adjusted(-30, -30, 30, 30)
        self.view.ensureVisible(scene_rect, 60, 60)

    def _sync_labeled_selection(self, _sel=None):
        """场景选中 → 同步右侧行高亮（与左侧标签列表同款 #2a3f6b）。"""
        sel = _sel if _sel is not None else self.scene.selected_item()
        for it, row in self._labeled_rows.items():
            bg = "#2a3f6b" if it is sel else "#232834"
            row.setStyleSheet(
                "QFrame {{ background: {0}; border-radius: 6px; }}".format(bg))

    @staticmethod
    def _polygon_area(points):
        """shoelace 公式计算多边形面积（像素²），顶点数 <3 返回 0。"""
        n = len(points)
        if n < 3:
            return 0.0
        s = 0.0
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            s += x1 * y2 - x2 * y1
        return abs(s) / 2.0

    def _save_current(self):
        """
        仅在用户改动过标注（_dirty）时保存；未改动不写文件。
        保存内容包括：画/删/改标签/拖动缩放等触发的 boxes_changed；
        格式刷粘贴修改过图像像素时，一并把图像写盘。
        """
        if not self._dirty:
            return
        if not (0 <= self.index < len(self.image_list)):
            return
        image_path = self.image_list[self.index]
        # 格式刷改过图像像素 -> 覆盖写回磁盘(QPixmap.save 按扩展名决定格式)
        if getattr(self.scene, "image_modified", False):
            try:
                self.scene.image_item.pixmap().save(image_path)
            except Exception:
                pass
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
        if shapes:
            save_labelme(image_path, shapes)
        else:
            if os.path.exists(json_path):
                try:
                    os.remove(json_path)
                except OSError:
                    pass
        self._dirty = False


class _HueSatPicker(QWidget):
    """HSV 取色面板：x=色相(0-359°)、y=饱和度(1→0)，明度由外部滑块控制。"""

    def __init__(self, value=255, on_change=None):
        super().__init__()
        self.setFixedSize(200, 150)
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
    """iOS/Android 风格开关：圆角轨道 + 白色圆形滑块，点击左右滑动。"""

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
        track = QColor("#5b8cff") if self._checked else QColor("#3a3f4d")
        p.setPen(Qt.NoPen)
        p.setBrush(track)
        p.drawRoundedRect(0, 0, 36, 20, 10, 10)
        p.setBrush(QColor("#ffffff"))
        # 滑块 16px 直径, 轨道宽 36 - 留 2px 边 -> 滑动 18px
        cx = 18 if self._checked else 2
        p.drawEllipse(cx, 2, 16, 16)


class ColorPickerDialog(QDialog):
    """自定义全中文颜色选择对话框。"""

    BASIC_COLORS = [
        "#FF0000", "#00FF00", "#0000FF", "#FFFF00",
        "#00FFFF", "#FF00FF", "#000000", "#FFFFFF",
        "#808080", "#C0C0C0", "#FF8800", "#8800FF",
    ]

    def __init__(self, initial=QColor("#5B8CFF"), parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择颜色")
        self._color = QColor(initial) if initial.isValid() else QColor("#5B8CFF")

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        top = QHBoxLayout()
        self._preview = QFrame()
        self._preview.setFixedSize(60, 40)
        top.addWidget(self._preview)
        html_box = QVBoxLayout()
        html_box.addWidget(QLabel("十六进制:"))
        self._html_edit = QLineEdit()
        self._html_edit.setMaximumWidth(120)
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
        self._value_slider.setFixedHeight(150)
        self._value_slider.valueChanged.connect(self._on_value_changed)
        picker_row.addWidget(self._value_slider)
        picker_row.addStretch(1)
        layout.addLayout(picker_row)

        layout.addWidget(QLabel("基本颜色:"))
        grid = QGridLayout()
        grid.setSpacing(4)
        for i, c in enumerate(self.BASIC_COLORS):
            btn = QPushButton()
            btn.setFixedSize(28, 28)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("QPushButton { background: %s; border: 1px solid #555; border-radius: 3px; }" % c)
            btn.clicked.connect(lambda checked=False, _c=c: self._set_color(QColor(_c)))
            grid.addWidget(btn, i // 6, i % 6)
        layout.addLayout(grid)

        layout.addWidget(QLabel("自定义 RGB:"))
        rgb = QHBoxLayout()
        self._r_edit = QSpinBox()
        self._g_edit = QSpinBox()
        self._b_edit = QSpinBox()
        for s, lab in [(self._r_edit, "R:"), (self._g_edit, "G:"), (self._b_edit, "B:")]:
            s.setRange(0, 255)
            s.setFixedWidth(70)
            s.valueChanged.connect(self._on_rgb_changed)
            rgb.addWidget(QLabel(lab))
            rgb.addWidget(s)
        rgb.addStretch(1)
        layout.addLayout(rgb)

        btns = QHBoxLayout()
        btns.addStretch(1)
        cancel = QPushButton("取消")
        cancel.clicked.connect(self.reject)
        ok = QPushButton("确定")
        ok.setDefault(True)
        ok.clicked.connect(self.accept)
        btns.addWidget(cancel)
        btns.addWidget(ok)
        layout.addLayout(btns)

        self._update_widgets_from_color()

    def _update_widgets_from_color(self):
        c = self._color
        self._preview.setStyleSheet(
            "QFrame { background: %s; border: 1px solid #555; border-radius: 4px; }" % c.name())
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
    def get_color(initial=QColor("#5B8CFF"), parent=None):
        dlg = ColorPickerDialog(initial, parent)
        if dlg.exec() == QDialog.Accepted:
            return dlg.selected_color()
        return QColor()
