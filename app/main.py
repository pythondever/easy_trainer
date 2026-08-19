import sys
import os
import json
import shutil
import subprocess
import time
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append('../ui')
import matplotlib.pyplot as plt
import numpy as np
import uuid
from datetime import datetime
from matplotlib import font_manager
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtGui import QFontMetrics
from PIL.ImageQt import ImageQt
from app.annotation.box_item import label_color
from app.annotation_dialog import AnnotationDialog
from app.log_dialog import LogDialog
from app.model_dialog import ModelDialog
from app.train.dialogs import TrainDialog
from app.train.train_worker import TrainWorker
from paginator import Paginator
from ui.app import Ui_AppUI as MainUI
from ui.enter_name import Ui_Dialog as EnterNameUI
from ui.add_dataset import Ui_AddDatasets
from ui.import_data import Ui_ImportData
from ui.dataset_properties import Ui_Dialog as DatasetPropertiesUI
from ui.edit_label import Ui_Dialog as EditLabelUI
from ui.export_data import Ui_Dialog as ExportDataUI
from app.label_utils import (normalize_label, label_sort_key,
                             load_json_boxes, boxes_to_yolo_text)
from app.message_box import MessageBox, ProgressDialog
from app.log import write_log


from db import DataBase
from PySide6.QtGui import QIcon, QPixmap, QFont, QImage, QPainter, QColor, QPen
from PySide6.QtCore import Qt, QSize, QThread, Signal, QTimer, QEvent, QTime
from PySide6.QtWidgets import QWidget, QApplication, QDialog, QMenu, QMessageBox, \
    QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QTreeWidget, QTreeWidgetItem, \
    QFileDialog, QProgressBar, QGraphicsView, QGraphicsScene, QHeaderView, QAbstractItemView, \
    QComboBox, QPushButton, QTimeEdit, \
    QGraphicsPixmapItem, QGraphicsItem

try:
    from shiboken6 import isValid as _is_valid
except ImportError:
    _is_valid = lambda obj: obj is not None

try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None


_CJK_FONT_CANDIDATES = [
    "Microsoft YaHei UI", "Microsoft YaHei", "微软雅黑",   # Windows
    "SimHei", "黑体", "SimSun", "宋体",                      # Windows
    "PingFang SC", "Hiragino Sans GB", "STHeiti",            # macOS
    "Noto Sans CJK SC", "Noto Sans SC", "WenQuanYi Micro Hei",  # Linux
    "Source Han Sans CN", "Source Han Sans SC",
    "AR PL UMing CN", "AR PL UKai CN",
]


def _fmt_duration(secs):
    """可读时长(不足1分钟显示秒;长训练显示天/时/分)。"""
    if secs < 60:
        return "{}秒".format(secs)
    d, rem = divmod(secs, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if d:
        parts.append("{}天".format(d))
    if h:
        parts.append("{}小时".format(h))
    if m or not parts:
        parts.append("{}分".format(m))
    if s and not d and not h:
        parts.append("{}秒".format(s))
    return "".join(parts)


def setup_matplotlib_chinese():
    try:
        available = {f.name for f in font_manager.fontManager.ttflist}
    except Exception:
        available = set()
    chosen = next((f for f in _CJK_FONT_CANDIDATES if f in available), None)
    if chosen is None:
        for f in font_manager.fontManager.ttflist:
            n = f.name.lower()
            if any(kw in n for kw in ("cjk", "chinese", "yahei", "simhei",
                                       "pingfang", "heiti", "songti", "han")):
                chosen = f.name
                break
    if chosen is None:
        chosen = "DejaVu Sans"
    plt.rcParams["font.sans-serif"] = [chosen, "DejaVu Sans"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False


def load_style_sheet():
    """加载 resources/style.qss"""
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    qss_path = os.path.join(here, "style", "style.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _load_yolo_boxes(txt_path, img_path):
    """读 yolo txt boxes(归一化坐标转像素,标签归一化)。"""
    boxes = []
    try:
        with PILImage.open(img_path) as im:
            iw, ih = im.size
    except Exception:
        return []
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) < 5:
                    continue
                try:
                    cx, cy, w, h = map(float, parts[1:5])
                except ValueError:
                    continue
                label = normalize_label(parts[0].strip())
                boxes.append((max(0, int((cx - w / 2) * iw)), max(0, int((cy - h / 2) * ih)),
                              max(1, int(w * iw)), max(1, int(h * ih)), label))
    except Exception:
        return []
    return boxes


def _boxes_to_labelme_json(boxes, img_path, iw, ih):
    """boxes(像素 + label) -> labelme json dict。"""
    shapes = []
    for x, y, w, h, label in boxes:
        shapes.append({"label": label, "points": [[x, y], [x + w, y + h]],
                       "group_id": None, "shape_type": "rectangle", "flags": {}})
    return {"version": "5.0.1", "flags": {}, "shapes": shapes,
            "imagePath": os.path.basename(img_path),
            "imageWidth": iw, "imageHeight": ih}


class _ImportTask(QThread):
    """
    后台导入线程: 扫描图像目录,可选读取标签(yolo txt / labelme json),
    生成整图缩略图(默认大图模式);ROI 裁剪小图在筛选时懒生成(见 _get_rois)。
    结果以 list 通过 finished_signal 返回:
    [{"image_path", "label_path", "boxes": [(x,y,w,h,label)]或None, "labels": [...],
      "thumb": QImage或None, "rois": {label: [QImage]}}]
    """
    progress_updated = Signal(int)
    finished_signal = Signal(list)

    IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

    def __init__(self, image_path, label_path="", fmt="", parent=None, excluded=None):
        super().__init__(parent)
        self.image_paths = [image_path] if isinstance(image_path, (str,)) else list(image_path or [])
        self.label_paths = [label_path] if isinstance(label_path, (str,)) else list(label_path or [])
        self.image_paths = [p for p in self.image_paths if p]
        self.label_paths = [p for p in self.label_paths if p]
        self.fmt = fmt  # '' 无标签 / '.txt' / '.json'
        self.excluded = set(excluded or [])
        self._cancel = False

    @staticmethod
    def _norm(path):
        return os.path.normcase(os.path.normpath(path))

    def run(self):
        cls_mode = self.fmt == "cls"   # 按子文件夹分类导入: 子文件夹名=类别
        images = []
        for base_dir in self.image_paths:
            if self._cancel:
                break
            if not base_dir or not os.path.isdir(base_dir):
                continue
            for root, _, files in os.walk(base_dir):
                if self._cancel:
                    break
                for fn in sorted(files):
                    if fn.lower().endswith(self.IMAGE_EXTS):
                        p = os.path.join(root, fn)
                        if self._norm(p) in self.excluded:
                            continue
                        if cls_mode:
                            # 类别 = 根目录下第一级子文件夹名; 图像直接在根目录则用根目录名
                            rel = os.path.relpath(root, base_dir)
                            cls = (rel.split(os.sep)[0]
                                   if rel and rel != "."
                                   else os.path.basename(base_dir))
                            images.append((p, cls))
                        else:
                            images.append((p, None))
        total = len(images)
        result = []
        for i, (img_path, cls) in enumerate(images):
            if self._cancel:
                break
            try:
                if cls_mode:
                    result.append({
                        "image_path": img_path,
                        "label_path": "",
                        "cls": cls,
                        "labels": [cls] if cls else [],
                        "boxes": None,
                        "thumb": None,
                        "rois": {},
                    })
                else:
                    boxes, labels = self._read_boxes(img_path)
                    thumb = None
                    result.append({
                        "image_path": img_path,
                        "label_path": self._label_of(img_path),
                        "boxes": boxes if boxes else None,   # [(x, y, w, h, label)] 或 None
                        "labels": labels,
                        "thumb": thumb,
                        "rois": {},
                    })
            except Exception:
                pass  #
            if total > 0:
                self.progress_updated.emit(int((i + 1) / total * 100))
        self.finished_signal.emit(result)

    def _label_of(self, img_path):
        """在多个标签目录中找同名的标签文件(txt/json)，返回存在的第一个; 无则空。"""
        if not self.label_paths or not self.fmt:
            return ""
        base = os.path.splitext(os.path.basename(img_path))[0]
        ext = ".txt" if self.fmt == ".txt" else ".json"
        for lp in self.label_paths:
            if not lp or not os.path.isdir(lp):
                continue
            candidate = os.path.join(lp, base + ext)
            if os.path.exists(candidate):
                return candidate
        return ""

    def _read_boxes(self, img_path):
        """
        读取标签，返回 (boxes, labels):
        boxes = 像素坐标 [(x, y, w, h, label)]; labels = 对应类别列表
        无标签返回(None, [])。
        优先读图像同路径 labelme json，与标注界面 _load_current
        一致；没有才回退 label_paths 的导入标签(txt/json)。否则重启后首页
        缩略图会显示标注界面修改前的旧标签。
        """
        same_path_json = os.path.splitext(img_path)[0] + ".json"
        if os.path.exists(same_path_json):
            label_file = same_path_json
            fmt = ".json"
        elif self.label_paths and self.fmt:
            label_file = self._label_of(img_path)
            fmt = self.fmt
        else:
            return None, []
        if not os.path.exists(label_file):
            return None, []
        try:
            with PIL_ImageOpen(img_path) as im:
                iw, ih = im.size
        except Exception:
            return None, []
        boxes = []
        labels = []
        if fmt == ".txt":
            with open(label_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) < 5:
                        continue
                    try:
                        vals = [float(x) for x in parts[1:]]
                    except ValueError:
                        continue
                    if len(vals) == 4:
                        cx, cy, w, h = vals
                        x = int((cx - w / 2) * iw)
                        y = int((cy - h / 2) * ih)
                        bw = int(w * iw)
                        bh = int(h * ih)
                    else:
                        xs = vals[0::2]
                        ys = vals[1::2]
                        if not xs or not ys:
                            continue
                        x = int(min(xs) * iw)
                        y = int(min(ys) * ih)
                        bw = int((max(xs) - min(xs)) * iw)
                        bh = int((max(ys) - min(ys)) * ih)
                    lbl = normalize_label(parts[0].strip())
                    boxes.append((max(0, x), max(0, y), max(1, bw), max(1, bh), lbl))
                    labels.append(lbl)
        else:
            with open(label_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for shape in data.get("shapes", []):
                pts = shape.get("points", [])
                if len(pts) < 2:
                    continue
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                x, y = int(min(xs)), int(min(ys))
                w, h = int(max(xs) - min(xs)), int(max(ys) - min(ys))
                lbl = normalize_label(shape.get("label", "unknown"))
                boxes.append((max(0, x), max(0, y), max(1, w), max(1, h), lbl))
                labels.append(lbl)
        return boxes, labels


def PIL_ImageOpen(path):
    return PILImage.open(path)


def _pil_to_qimage(pil_img):
    """PIL RGB -> QImage(ARGB32,主线程转 QPixmap 使用)。"""
    try:
        qimg = ImageQt(pil_img).copy()
        return qimg
    except Exception:
        data = pil_img.tobytes("raw", "RGB")
        qimg = QImage(data, pil_img.width, pil_img.height, pil_img.width * 3, QImage.Format_RGB888)
        return qimg.copy()


def _make_uniform_thumb(pil_img, size=(200, 200), bg=(19, 21, 26), fill=False):
    """
    统一规格缩略图到 size×size。
    fill=False(默认): 等比缩放 + 居中 + 深色背景填充(首页 #13151a),
        用于整图缩略(保持原图比例，不变形).
    fill=True:不等比 resize 到 size×size（保证 QImage 严格统一规格）,
        用于 ROI 裁剪——无论原标注框大小或长宽比,
        渲染到 cell 都是严格 200×200 占满,绝对统一规格.
    """
    if fill:
        return pil_img.resize(size, PILImage.LANCZOS)
    thumb = pil_img.copy()
    thumb.thumbnail(size)
    canvas = PILImage.new("RGB", size, bg)
    off_x = (size[0] - thumb.width) // 2
    off_y = (size[1] - thumb.height) // 2
    if off_x >= 0 and off_y >= 0:
        canvas.paste(thumb, (off_x, off_y))
    return canvas


class SelectablePixmapItem(QGraphicsPixmapItem):
    """首页图像列表项:点击高亮边框、可选中(单选/Ctrl多选/Ctrl+A全选)。"""

    def __init__(self, pixmap, image_path):
        super().__init__(pixmap)
        self.image_path = image_path
        self.setData(0, image_path)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self._sel_pen = QPen(QColor("#5B8CFF"), 3)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setPen(self._sel_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect().adjusted(2, 2, -2, -2))


class App(QWidget, MainUI):
    def __init__(self):
        super().__init__()
        self.db = DataBase(os.path.join(os.path.expanduser("~"), ".easy_trainer"))
        try:
            self.db.migrate_model_records()
        except Exception:
            pass
        self.dataset_cache = {}
        self._loading_tasks = {}
        # 分页状态
        self.page_size = 50   # 每页图像记录数
        self.current_page = 0
        self.current_label = "__unlabeled__"
        self.init_widget()
        self.register_event()
        self.fill_setting()
        self._log_dialog = LogDialog(self)
        self._log("软件启动")

    def closeEvent(self, event):
        self._log("软件退出")
        if self.is_training():
            self._log("软件退出前停止训练")
            self.stop_training(confirm=False)
        # 停止还在运行的测试线程,避免 QThread destroyed while running 崩溃
        for w in list(getattr(self, "_test_workers", set())):
            try:
                w.stop()
                w.wait(3000)
            except Exception:
                pass
        super().closeEvent(event)

    def init_widget(self):
        self.setupUi(self)
        # 训练进度条/停止按钮默认隐藏(有训练任务时才显示)
        self.train_progress.hide()
        self.task_name_label.hide()
        self.stop_train_btn.hide()
        self.stop_train_btn.setStyleSheet(
            "QPushButton { background-color: #d64545; color: white;"
            " border: none; border-radius: 6px; padding: 4px 12px;"
            " font-size: 13px; }"
            "QPushButton:hover { background-color: #e05555; }")
        # 进度条文本: `30% | 0.556`
        self._latest_map50 = None
        self._apply_progress_format()
        self.time_count_label.hide()
        self.time_count_edit.hide()
        self.gpu_memory_label.show()
        self.gpu_memory_use_btn.show()
        self.time_count_edit.setReadOnly(True)
        self.time_count_edit.setButtonSymbols(QTimeEdit.NoButtons)
        self.time_count_edit.setDisplayFormat("hh:mm:ss")
        self.time_count_edit.setTime(self.time_count_edit.time().fromString("00:00:00", "hh:mm:ss"))
        self._train_start_ts = 0.0
        self._eta_remain = 0
        self._test_start_ts = 0    # 测试开始时间, 用于推算剩余时间
        self._eta_timer = QTimer(self)
        self._eta_timer.setInterval(1000)
        self._eta_timer.timeout.connect(self._eta_tick)
        self._gpu_timer = QTimer(self)
        self._gpu_timer.setInterval(2000)
        self._gpu_timer.timeout.connect(self._refresh_gpu_memory)
        self._gpu_timer.start()
        self._refresh_gpu_memory()
        self._train_worker = None
        self._training_record_id = None
        icon_path = os.path.join(WORKSPACE_DIRECTORY, "resources", "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        logo_path = os.path.join(WORKSPACE_DIRECTORY, "resources", "icon.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.appLogoLabel.setPixmap(pix)
        self.sidebarTitle.setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self._init_image_view()
        self._init_label_filter()
        self._current_dataset = None

    def _init_image_view(self):
        """在 thumbnailsLayout 内创建 QGraphicsView 显示区"""
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setObjectName("imageGraphicsView")
        self.graphics_view.setScene(QGraphicsScene(self.graphics_view))
        self.graphics_view.setRenderHint(QPainter.Antialiasing)
        self.graphics_view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.graphics_view.setBackgroundBrush(QColor("#13151a"))
        self.graphics_view.setDragMode(QGraphicsView.NoDrag)
        self.graphics_view.setCursor(Qt.ArrowCursor)
        self.graphics_view.setMouseTracking(True)
        self.graphics_view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.graphics_view.viewport().installEventFilter(self)
        self.graphics_view.viewport().setMouseTracking(True)
        layout = self.thumbnailsLayout
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        layout.addWidget(self.graphics_view)
        self.graphics_view.setFocusPolicy(Qt.StrongFocus)
        orig_press = self.graphics_view.mousePressEvent

        def _gv_press(ev, _o=orig_press):
            self.graphics_view.setFocus()
            _o(ev)
        self.graphics_view.mousePressEvent = _gv_press
        orig_key = self.graphics_view.keyPressEvent

        def _gv_key(ev, _o=orig_key, _self=self):
            if _self.current_label:
                _o(ev)
                return
            if ev.key() == Qt.Key_A and (ev.modifiers() & Qt.ControlModifier):
                scene = _self.graphics_view.scene()
                for it in scene.items():
                    if isinstance(it, SelectablePixmapItem):
                        it.setSelected(True)
                ev.accept()
                return
            if ev.key() == Qt.Key_Escape:
                _self.graphics_view.scene().clearSelection()
                ev.accept()
                return
            _o(ev)
        self.graphics_view.keyPressEvent = _gv_key
        orig_ctx = self.graphics_view.contextMenuEvent

        def _gv_ctx_menu(ev, _o=orig_ctx):
            hit = self.graphics_view.itemAt(ev.pos())
            if isinstance(hit, SelectablePixmapItem) and not self.current_label:
                if not hit.isSelected():
                    self.graphics_view.scene().clearSelection()
                    hit.setSelected(True)
                selected = [i for i in self.graphics_view.scene().selectedItems()
                            if isinstance(i, SelectablePixmapItem)]
                menu = QMenu(self)
                act = menu.addAction("删除所选图像（{} 张）".format(len(selected)))
                act.triggered.connect(lambda: self._delete_selected_images(selected))
                menu.exec(ev.globalPos())
                ev.accept()
                return
            _o(ev)
        self.graphics_view.contextMenuEvent = _gv_ctx_menu

    def _on_graphics_double_click(self, pos):
        """双击图像显示区:定位到点击的图像记录,进入标注."""
        item = self.graphics_view.itemAt(pos)
        if item is None:
            return
        image_path = item.data(0)
        if not image_path or not os.path.exists(image_path):
            return
        self._open_annotation(image_path)

    def _open_annotation(self, image_path):
        """打开标注对话框"""
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds:
            return
        proj, ds = cur_ds
        index = self.dataset_cache.get(proj, {}).get(ds, {})
        view_data = self._view_data_by_label(index)
        image_list = [r.get("image_path", "") for r in view_data]
        try:
            cur = image_list.index(image_path)
        except ValueError:
            cur = 0

        binding = self.db.get_dataset_import(proj, ds)
        label_paths = binding.get("label_paths") or (
            [binding.get("label_path")] if binding.get("label_path") else [])
        cls_mode = binding.get("label_fmt", "") == "cls"
        dlg = AnnotationDialog(image_list, cur, self.db, proj, ds,
                               label_path=label_paths,
                               label_fmt=binding.get("label_fmt", ""),
                               cls_mode=cls_mode,
                               parent=self)
        dlg.exec()
        changes = getattr(dlg, "_cls_changes", [])
        if changes:
            self._apply_cls_changes(proj, ds, changes)
        deleted = getattr(dlg, "_deleted_labels", [])
        if deleted:
            self._apply_deleted_labels(proj, ds, deleted)
        self._refresh_dataset_labels(proj, ds)
        self._refresh_label_filter(proj, ds)
        self._refresh_annotation_progress(proj, ds)
        if self.current_label:
            self.show_dataset_images(proj, ds)

    def _apply_deleted_labels(self, project_name, dataset_name, label_names):
        """
        清理缓存中的 labels/boxes/rois、重建分组。
        """
        if not label_names:
            return
        for lb in label_names:
            self._delete_label_in_files(project_name, dataset_name, lb)
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        for rec in index.get("all", []):
            rec_labels = rec.get("labels") or []
            new_labels = [l for l in rec_labels if l not in label_names]
            if len(new_labels) != len(rec_labels):
                rec["labels"] = new_labels
            if rec.get("boxes"):
                rec["boxes"] = [b for b in rec["boxes"]
                                if b[-1] not in label_names]
            rec["rois"] = {}
        self._rebuild_index_labels(project_name, dataset_name)

    def _apply_cls_changes(self, project_name, dataset_name, changes):
        """分类数据集修改了类别：同步缓存中的 image_path/cls/labels，重建标签分组。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        recs = index.get("all", [])
        for old_p, new_p, new_cls in changes:
            for rec in recs:
                if rec.get("image_path") == old_p:
                    rec["image_path"] = new_p
                    rec["cls"] = new_cls
                    rec["labels"] = [new_cls]
                    rec["thumb"] = None   # 旧缩略图失效,渲染时懒重新生成
                    rec["rois"] = {}
                    break
        index["labels"] = {}
        for rec in recs:
            for lbl in set(rec.get("labels") or []):
                index["labels"].setdefault(lbl, []).append(rec)

    def _init_label_filter(self):
        """
        绑定首页设计器已有的标签筛选下拉框（label_comboBox）。
        第一项固定"未标注"。
        """
        self.label_filter_combo = self.label_comboBox
        self.label_filter_combo.clear()
        self.label_filter_combo.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.label_filter_combo.setMinimumContentsLength(12)
        self.label_filter_combo.addItem("未标注", "__unlabeled__")
        self.label_filter_combo.currentIndexChanged.connect(self._on_label_filter_changed)

    def _on_label_filter_changed(self, idx):
        """标签下拉框变更:重新渲染场景(按标签筛选)。"""
        self.current_label = self.label_filter_combo.itemData(idx) or "__unlabeled__"
        cur_ds = getattr(self, "_current_dataset", None)
        if cur_ds:
            proj, ds = cur_ds
            self.show_dataset_images(proj, ds)

    def _refresh_label_filter(self, project_name, dataset_name):
        """
        切换数据集时刷新首页标签下拉框选项(从 db 读取该数据集标签)。
        "未标注"固定排最后; 数据集全标注时默认选中第一个标签, 否则默认"未标注"。
        """
        if not hasattr(self, "label_filter_combo"):
            return
        self.label_filter_combo.blockSignals(True)
        try:
            self.label_filter_combo.clear()
            labels = {normalize_label(k): v for k, v in
                      self.db.get_dataset_labels(project_name, dataset_name).items()}
            if labels != self.db.get_dataset_labels(project_name, dataset_name):
                self.db.save_dataset_labels(project_name, dataset_name, labels)
            # 标签按排序放前面,"未标注"固定排最后
            for name, color in sorted(labels.items(),
                                      key=lambda kv: label_sort_key(kv[0])):
                self.label_filter_combo.addItem(name, name)
                idx = self.label_filter_combo.count() - 1
                pix = QPixmap(14, 14)
                pix.fill(QColor(color))
                self.label_filter_combo.setItemIcon(idx, QIcon(pix))
            self.label_filter_combo.addItem("未标注", "__unlabeled__")
            if (self.current_label
                    and self.current_label != "__unlabeled__"
                    and self.current_label in labels):
                for i in range(self.label_filter_combo.count()):
                    if self.label_filter_combo.itemData(i) == self.current_label:
                        self.label_filter_combo.setCurrentIndex(i)
                        break
                else:
                    self._set_label_filter_default(project_name, dataset_name, labels)
            else:
                self._set_label_filter_default(project_name, dataset_name, labels)
        finally:
            self.label_filter_combo.blockSignals(False)

    def _set_label_filter_default(self, project_name, dataset_name, labels):
        """数据集全标注 → 默认选第一个标签; 否则默认"未标注"(在下拉最后)。"""
        binding = self.db.get_dataset_import(project_name, dataset_name)
        total = binding.get("total", 0) or 0
        labeled = binding.get("labeled", 0) or 0
        if total > 0 and labeled >= total and labels:
            first = sorted(labels.keys(), key=label_sort_key)[0]
            self.current_label = first
            for i in range(self.label_filter_combo.count()):
                if self.label_filter_combo.itemData(i) == first:
                    self.label_filter_combo.setCurrentIndex(i)
                    break
        else:
            self.current_label = "__unlabeled__"
            self.label_filter_combo.setCurrentIndex(
                self.label_filter_combo.count() - 1)

    def _rebuild_index_labels(self, project_name, dataset_name):
        """按 rec.labels 重建 dataset_cache 的 labels 分组索引。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        index["labels"] = {}
        for rec in index.get("all", []):
            for lbl in (rec.get("labels") or []):
                index["labels"].setdefault(lbl, []).append(rec)

    def _on_rename_label(self):
        """首页「编辑」按钮: 重命名当前筛选下拉选中的标签。
        弹 ui/edit_label.py 对话框(类别 + 批量修改为 + 确定)。"""
        if not self._current_dataset:
            MessageBox.warning(self, "重命名", "请先在左侧选中一个数据集")
            return
        old = self.current_label
        if old == "__unlabeled__" or not old:
            MessageBox.warning(self, "重命名", "请先在筛选下拉框中选择要重命名的标签")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("类别修改")
        ui = EditLabelUI()
        ui.setupUi(dlg)
        ui.label_btn.setText(old)
        ui.new_label_edit.setText(old)
        ui.new_label_edit.selectAll()
        ui.done_btn.clicked.connect(dlg.accept)
        dlg.exec()
        new_name = ui.new_label_edit.text().strip()
        if dlg.result() != QDialog.Accepted:
            return
        if not new_name:
            MessageBox.warning(self, "重命名", "标签名称不能为空")
            return
        if new_name == old:
            return
        proj, ds = self._current_dataset
        self._apply_rename_label(proj, ds, old, new_name)

    def _apply_rename_label(self, project_name, dataset_name, old_name, new_name):
        """重命名标签: 内存索引 / 本地 json / db 同步改, 支持合并（新名已存在）。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if index:
            for rec in index.get("all", []):
                labels = rec.get("labels") or []
                if old_name in labels:
                    seen = []
                    for lbl in labels:
                        nl = new_name if lbl == old_name else lbl
                        if nl not in seen:
                            seen.append(nl)
                    rec["labels"] = seen
                boxes = rec.get("boxes")
                if boxes:
                    rec["boxes"] = [tuple(b[:-1]) + (new_name,)
                                    if b[-1] == old_name else b for b in boxes]
                rec["rois"] = {}
            self._rebuild_index_labels(project_name, dataset_name)
        self._rename_label_in_files(project_name, dataset_name, old_name, new_name)
        labels = self.db.get_dataset_labels(project_name, dataset_name)
        color = labels.pop(old_name, None)
        if color is not None and new_name not in labels:
            labels[new_name] = color
        self.db.save_dataset_labels(project_name, dataset_name, labels)
        self._log("重命名标签: {} → {} ({}/{})".format(
            old_name, new_name, project_name, dataset_name))
        self.current_label = new_name
        self._refresh_label_filter(project_name, dataset_name)
        self.show_dataset_images(project_name, dataset_name)

    def _rename_label_in_files(self, project_name, dataset_name, old_name, new_name):
        """本地 labelme json：把 shape.label == old_name 改成 new_name。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        for rec in index.get("all", []):
            img_path = rec.get("image_path", "")
            base, _ = os.path.splitext(img_path)
            json_path = base + ".json"
            if not os.path.exists(json_path):
                continue
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                changed = False
                for shape in data.get("shapes", []):
                    if normalize_label(shape.get("label")) == old_name:
                        shape["label"] = new_name
                        changed = True
                if changed:
                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception:
                continue

    def _on_delete_label(self):
        """首页「删除」按钮：删除当前筛选下拉选中的标签(含确认弹窗)。"""
        if not self._current_dataset:
            MessageBox.warning(self, "删除标签", "请先在左侧选中一个数据集")
            return
        old = self.current_label
        if old == "__unlabeled__" or not old:
            MessageBox.warning(self, "删除标签", "请先在筛选下拉框中选择要删除的标签")
            return
        if not MessageBox.question(
                self, "删除标签", "确定删除标签「{}」吗？\n该标签的所有标注将被删除，且不可恢复。".format(old),
                default_yes=True):
            return
        proj, ds = self._current_dataset
        self._apply_delete_label(proj, ds, old)

    def _apply_delete_label(self, project_name, dataset_name, label_name):
        """删除标签: 内存索引 / 本地 json / db 同步移除。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if index:
            for rec in index.get("all", []):
                if label_name in (rec.get("labels") or []):
                    rec["labels"] = [l for l in rec["labels"] if l != label_name]
                if rec.get("boxes"):
                    rec["boxes"] = [b for b in rec["boxes"] if b[-1] != label_name]
                rec["rois"] = {}
            self._rebuild_index_labels(project_name, dataset_name)
        self._delete_label_in_files(project_name, dataset_name, label_name)
        self.db.remove_dataset_label(project_name, dataset_name, label_name)
        self._log("删除标签: {} ({}/{})".format(
            label_name, project_name, dataset_name))
        if self.current_label == label_name:
            self.current_label = "__unlabeled__"
            self._reset_image_area()
            self._refresh_label_filter(project_name, dataset_name)
        else:
            self._refresh_label_filter(project_name, dataset_name)
            self.show_dataset_images(project_name, dataset_name)

    def _delete_label_in_files(self, project_name, dataset_name, label_name):
        """
        本地 labelme json: 删除 shape.label == label_name 的所有 shapes。
        文件较多时弹进度框；先用文本快速检查跳过不含该标签的文件
        （省去 json.load 解析），仅命中文件才解析+过滤+写回。
        """
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        recs = index.get("all", [])
        progress = None
        if len(recs) > 50:
            progress = ProgressDialog("删除标签", "正在清理标注文件…", self,
                                      maximum=len(recs), cancellable=False)
        try:
            for i, rec in enumerate(recs):
                if progress is not None:
                    progress.set_progress(i)
                img_path = rec.get("image_path", "")
                base, _ = os.path.splitext(img_path)
                json_path = base + ".json"
                if not os.path.exists(json_path):
                    continue
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        text = f.read()
                    if label_name not in text:
                        continue   # 快速跳过：文本不含该标签，无需解析
                    data = json.loads(text)
                    before = len(data.get("shapes", []))
                    data["shapes"] = [s for s in data.get("shapes", [])
                                      if normalize_label(s.get("label")) != label_name]
                    if len(data["shapes"]) != before:
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                except Exception:
                    continue
        finally:
            if progress is not None:
                progress.close()

    def _show_enter_name(self, preset=""):
        """弹出项目名称输入框。返回(name, ok);ok=False 表示用户取消。"""
        dlg = QDialog(self)
        dlg.setWindowTitle("项目名称")
        ui = EnterNameUI()
        ui.setupUi(dlg)
        if preset:
            ui.project_name_txt.setText(preset)
            ui.project_name_txt.selectAll()
        ui.enter_name_lbl.setVisible(False)
        ui.done_enter_name_btn.clicked.connect(dlg.accept)
        dlg.exec()
        name = ui.project_name_txt.text().strip()
        return name, dlg.result() == QDialog.Accepted

    def add_project(self):
        name, ok = self._show_enter_name()
        if not ok or not name:
            return
        if name in self.db.get_projects():
            MessageBox.warning(self, "创建项目", "项目名称已存在！")
            return
        self.db.add_project(name)
        self._log("创建项目: {}".format(name))
        self.refresh_project_list()

    def _rename_project(self, old_name):
        new_name, ok = self._show_enter_name(preset=old_name)
        if not ok or not new_name or new_name == old_name:
            return
        if new_name in self.db.get_projects():
            MessageBox.warning(self, "修改名称", "项目名称已存在！")
            return
        self.db.rename_project(old_name, new_name)
        self.refresh_project_list()

    def _delete_project(self, name):
        if MessageBox.question(self, "删除项目", "确定删除项目「{}」吗?\n".format(name),
                               default_yes=True):
            self.db.delete_project(name)
            self.db.delete_project_info(name)
            self.db.delete_project_records(name)
            self.dataset_cache.pop(name, None)
            cur_ds = getattr(self, "_current_dataset", None)
            if cur_ds and cur_ds[0] == name:
                self._current_dataset = None
                self.current_page = 0
                self._clear_scene()
                self.pageInfoLabel.setText("0 / 0")
            self.refresh_project_list()

    def _init_project_tree(self):
        self.project_tree = QTreeWidget()
        self.project_tree.setObjectName("projectTree")
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setRootIsDecorated(False)
        self.project_tree.setIndentation(20)
        self.project_tree.setIconSize(QSize(16, 16))
        self.project_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self._on_project_tree_menu)
        self.project_tree.itemExpanded.connect(self._on_project_expand_changed)
        self.project_tree.itemCollapsed.connect(self._on_project_expand_changed)
        self.project_tree.itemClicked.connect(self._on_project_tree_clicked)
        self.project_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.project_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.project_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.project_scroll_area.setWidget(self.project_tree)
        self.project_scroll_area.setWidgetResizable(True)

    @staticmethod
    def _on_project_expand_changed(item):
        """项目节点展开/折叠时切换文本前的 ▶/▼ 标记。"""
        kind = item.data(0, Qt.UserRole)
        if not kind or kind[0] != "project":
            return
        prefix = "▼" if item.isExpanded() else "▶"
        item.setText(0, "{}{}".format(prefix, kind[1]))

    def refresh_project_list(self):
        if not hasattr(self, "project_tree"):
            self._init_project_tree()
        self.project_tree.clear()
        project_icon = self._tree_icon("项目.png")
        dataset_icon = self._tree_icon("图像.png")
        proj_font = QFont()
        proj_font.setBold(True)
        proj_font.setPointSize(12)
        for name in self.db.get_projects():
            proj_item = QTreeWidgetItem(["▶" + name])
            proj_item.setData(0, Qt.UserRole, ("project", name))
            proj_item.setFont(0, proj_font)
            if not project_icon.isNull():
                proj_item.setIcon(0, project_icon)
            for ds in self.db.get_datasets(name):
                ds_item = QTreeWidgetItem([""])
                ds_item.setData(0, Qt.UserRole, ("dataset", name, ds["dataset_name"]))
                proj_item.addChild(ds_item)
                self._set_dataset_widget(ds_item, name, ds["dataset_name"])
            self.project_tree.addTopLevelItem(proj_item)

    def _tree_icon(self, name):
        """加载 resources/ 下图标, 缺失则返回空 QIcon。"""
        path = os.path.join(WORKSPACE_DIRECTORY, "resources", name)
        if os.path.exists(path):
            return QIcon(path)
        return QIcon()

    def _set_dataset_widget(self, ds_item, project_name, dataset_name):
        """
        把数据集节点替换为整体行内容器: [图标 + 名称 + 拉伸 + 标注进度]，
        """
        container = QWidget(self)
        container.setObjectName("datasetRowContainer")
        container.setStyleSheet("background: transparent;")
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h = QHBoxLayout(container)
        h.setContentsMargins(6, 0, 8, 0)
        h.setSpacing(8)
        h.setAlignment(Qt.AlignVCenter)
        name_lbl = QLabel(container)
        name_lbl.setObjectName("datasetRowName")
        name_lbl.setTextFormat(Qt.RichText)
        icon_path_uri = "file:///" + os.path.join(
            WORKSPACE_DIRECTORY, "resources", "图像.png").replace("\\", "/")
        name_lbl.setText(
            '<img src="{0}" width="14" height="14" '
            'style="vertical-align: middle;"/>&nbsp;{1}'.format(
                icon_path_uri, dataset_name))
        name_lbl.setStyleSheet("color: #ffffff; background: transparent;")
        h.addWidget(name_lbl)
        h.addStretch(1)
        progress_lbl = QLabel(container)
        progress_lbl.setObjectName("datasetRowProgress")
        progress_lbl.setStyleSheet(
            "color: #b8c0d0; background: transparent;"
            " padding-right: 4px; font-size: 12px;")
        h.addWidget(progress_lbl)
        binding = self.db.get_dataset_import(project_name, dataset_name)
        total = binding.get("total", 0)
        labeled = binding.get("labeled", 0)
        progress_lbl.setText("{}/{}".format(labeled, total))
        self.project_tree.setItemWidget(ds_item, 0, container)
        return container, progress_lbl

    def _on_project_tree_menu(self, pos):
        """
        项目树右键菜单:
        项目节点 -> 添加数据集 / 修改名称 / 删除项目
        数据集节点 -> 修改 / 删除
        """
        item = self.project_tree.itemAt(pos)
        if item is None:
            return
        kind = item.data(0, Qt.UserRole)
        menu = QMenu(self)
        if kind[0] == "project":
            act_add_ds = menu.addAction("添加数据集")
            menu.addSeparator()
            act_rename = menu.addAction("修改名称")
            act_del = menu.addAction("删除项目")
            act = menu.exec(self.project_tree.mapToGlobal(pos))
            if act is None:
                return
            if act == act_add_ds:
                self._add_dataset(kind[1])
            elif act == act_rename:
                self._rename_project(kind[1])
            elif act == act_del:
                self._delete_project(kind[1])
        elif kind[0] == "dataset":
            act_load = menu.addAction("载入")
            act_move = menu.addAction("移动")
            act_rename = menu.addAction("修改")
            act_del = menu.addAction("删除")
            act = menu.exec(self.project_tree.mapToGlobal(pos))
            if act is None:
                return
            if act == act_load:
                self._load_dataset_view(kind[1], kind[2])
            elif act == act_move:
                self._on_dataset_move(kind[1], kind[2])
            elif act == act_rename:
                self._rename_dataset(kind[1], kind[2])
            elif act == act_del:
                self._delete_dataset(kind[1], kind[2])

    def _show_add_dataset(self, preset_name="", title="添加数据集"):
        """
        弹出数据集对话框(ui/add_dataset.py 设计器生成)。
        数据集不再区分类型,隐藏类型下拉;返回(name, ok)。
        """
        dlg = QDialog(self)
        ui = Ui_AddDatasets()
        ui.setupUi(dlg)
        dlg.setWindowTitle(title)
        if preset_name:
            ui.lineEdit.setText(preset_name)
            ui.lineEdit.selectAll()
        # 类型已废弃:隐藏类型下拉
        combo = getattr(ui, "comboBox", None)
        if combo is not None:
            combo.setVisible(False)
        ui.done_btn.clicked.connect(dlg.accept)
        dlg.setFixedHeight(dlg.sizeHint().height())
        dlg.exec()
        name = ui.lineEdit.text().strip()
        return name, dlg.result() == QDialog.Accepted

    def _add_dataset(self, project_name):
        name, ok = self._show_add_dataset()
        if not ok or not name:
            return
        if not self.db.add_dataset(project_name, name):
            MessageBox.warning(self, "添加数据集", "该项目下已存在同名数据集！")
            return
        self._log("创建数据集: {}/{}".format(project_name, name))
        self.refresh_project_list()

    def _rename_dataset(self, project_name, old_name):
        name, ok = self._show_add_dataset(preset_name=old_name, title="修改数据集")
        if not ok or not name or name == old_name:
            return
        if not self.db.rename_dataset(project_name, old_name, name):
            MessageBox.warning(self, "修改数据集", "该项目下已存在同名数据集！")
            return
        self._log("重命名数据集: {} → {}".format(project_name, old_name, name))
        self.refresh_project_list()

    def _delete_dataset(self, project_name, ds_name):
        if MessageBox.question(
                self, "删除数据集",
                "确定删除数据集「{}」吗?\n".format(ds_name),
                default_yes=True):
            self.db.delete_dataset(project_name, ds_name)
            # 训练/模型记录可能被多个数据集共用,只移除该数据集,无引用才删记录
            self.db.remove_dataset_from_records(project_name, ds_name)
            self._log("删除数据集: {}/{}".format(project_name, ds_name))
            proj_cache = self.dataset_cache.get(project_name, {})
            proj_cache.pop(ds_name, None)
            if getattr(self, "_current_dataset", None) == (project_name, ds_name):
                self._current_dataset = None
                self.current_page = 0
                self._clear_scene()
                self.pageInfoLabel.setText("0 / 0")
            self.refresh_project_list()

    # ---------------- 数据集移动（A → B，跨项目） ----------------
    def _on_dataset_move(self, project_name, ds_name):
        """右键「移动」: 选择目标数据集 → 确认 → 移动数据。"""
        # 1. 选择目标数据集(本项目之外的其他项目数据集)
        target = self._select_move_target(project_name, ds_name)
        if target is None:
            return
        dst_proj, dst_ds = target
        # 2. 确认
        if not MessageBox.question(
                self, "移动数据集",
                "是否将「{}」的数据从\n{} / {} 移动到 {} / {}？\n"
                "移动后源数据集将清空。".format(
                    ds_name, project_name, ds_name, dst_proj, dst_ds),
                default_yes=True):
            return
        # 3. 执行
        try:
            self._move_dataset_data(project_name, ds_name, dst_proj, dst_ds)
        except Exception as e:
            MessageBox.critical(self, "移动失败", str(e))
            return
        MessageBox.information(
            self, "移动数据集",
            "已从 {} / {} 移动到 {} / {}".format(
                project_name, ds_name, dst_proj, dst_ds))

    def _select_move_target(self, src_project, src_ds):
        """
        弹目标数据集选择对话框(同项目/跨项目，排除源数据集自身)。
        返回(项目, 数据集)或 None。
        """
        candidates = []  # (项目, 数据集) —— 排除源数据集自身, 同项目内其他数据集也可选
        for proj in self.db.get_projects():
            for ds in self.db.get_datasets(proj):
                if proj == src_project and ds["dataset_name"] == src_ds:
                    continue
                candidates.append((proj, ds["dataset_name"]))
        if not candidates:
            MessageBox.warning(self, "移动数据集", "没有可移动到的目标数据集（本项目之外无数据集）")
            return None
        dlg = QDialog(self)
        dlg.setObjectName("MoveTargetDialog")
        dlg.setWindowTitle("选择目标数据集")
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)
        tip = QLabel("选择要将数据移动到的目标数据集：")
        layout.addWidget(tip)
        combo = QComboBox(dlg)
        for proj, ds in candidates:
            combo.addItem("{} / {}".format(proj, ds), (proj, ds))
        layout.addWidget(combo)
        btns = QHBoxLayout()
        btns.addStretch(1)
        ok_btn = QPushButton("确定", dlg)
        ok_btn.clicked.connect(dlg.accept)
        cancel_btn = QPushButton("取消", dlg)
        cancel_btn.clicked.connect(dlg.reject)
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)
        if dlg.exec() != QDialog.Accepted:
            return None
        return combo.currentData()

    def _move_dataset_data(self, src_proj, src_ds, dst_proj, dst_ds):
        """
        核心:源数据集数据合并到目标数据集,源清空.
        覆盖:缓存索引(按图像去重)、db 导入绑定路径列表、标签类别、
        标注/总数统计、已删除图像记录。
        """
        # ---- 1. 缓存合并(image_path 归一化去重; 源中已存在于目标的跳过)----
        src_index = self.dataset_cache.get(src_proj, {}).get(src_ds) or {}
        dst_index = self.dataset_cache.get(dst_proj, {}).get(dst_ds) or {}
        src_recs = list(src_index.get("all", []))
        dst_recs = list(dst_index.get("all", []))
        norm = lambda p: os.path.normcase(os.path.normpath(p or ""))
        seen = {norm(r.get("image_path")) for r in dst_recs}
        moved = [r for r in src_recs
                 if norm(r.get("image_path")) not in seen]
        dst_recs = dst_recs + moved
        dst_index["all"] = dst_recs
        # 重建目标 labels 分组索引
        if self.dataset_cache.get(dst_proj, {}).get(dst_ds) is not None:
            self._rebuild_index_labels(dst_proj, dst_ds)
        # 源缓存清空
        if src_index:
            src_index["all"] = []
            src_index["labels"] = {}

        # ---- 2. db：目标合并导入绑定 + 重算统计 ----
        src_binding = self.db.get_dataset_import(src_proj, src_ds) or {}
        dst_binding = self.db.get_dataset_import(dst_proj, dst_ds) or {}
        dst_img = list(dst_binding.get("image_paths") or [])
        src_img = list(src_binding.get("image_paths") or [])
        dst_lbl = list(dst_binding.get("label_paths") or [])
        src_lbl = list(src_binding.get("label_paths") or [])
        img_paths = dst_img + [p for p in src_img if p not in dst_img]
        lbl_paths = dst_lbl + [p for p in src_lbl if p not in dst_lbl]
        total_new = len(dst_recs)
        labeled_new = sum(
            1 for r in dst_recs
            if r.get("boxes") or self._has_label_file(r.get("image_path", "")))
        self.db.update_dataset_import(
            dst_proj, dst_ds, img_paths, lbl_paths,
            dst_binding.get("label_fmt", ""),
            labeled=labeled_new, total=total_new)

        # ---- 3. db：目标标签合并(颜色冲突保留目标)----
        dst_labels = self.db.get_dataset_labels(dst_proj, dst_ds)
        for lbl, color in self.db.get_dataset_labels(src_proj, src_ds).items():
            if lbl not in dst_labels:
                dst_labels[lbl] = color
        self.db.save_dataset_labels(dst_proj, dst_ds, dst_labels)

        # ---- 4. db：源清空(导入绑定 + 标签)----
        self.db.clear_dataset_import(src_proj, src_ds)
        self.db.save_dataset_labels(src_proj, src_ds, {})

        # ---- 5. 已删除图像记录迁移 ----
        self.db.move_deleted_images(src_proj, src_ds, dst_proj, dst_ds)

        # ---- 6. 日志: 目标标签统计(按框数)----
        label_counts = {}
        for r in dst_recs:
            for b in (r.get("boxes") or []):
                lbl = b[-1]
                label_counts[lbl] = label_counts.get(lbl, 0) + 1
        counts_str = ", ".join(
            "{}: {}个".format(k, v) for k, v in
            sorted(label_counts.items(), key=lambda kv: label_sort_key(kv[0])))
        self._log("数据集移动: {}/{} → {}/{} | 移动图像 {} 张"
                  " | 目标标签统计({}类): {}".format(
                      src_proj, src_ds, dst_proj, dst_ds, len(moved),
                      len(label_counts), counts_str or "(无)"))

        # ---- 7. 刷新: 树 / 显示区 / 标签筛选 ----
        self.refresh_project_list()
        if getattr(self, "_current_dataset", None) == (src_proj, src_ds):
            # 源数据集已清空: 完整重置图像区/分页/筛选下拉/标注统计
            self._current_dataset = None
            self._reset_image_area()
        elif getattr(self, "_current_dataset", None) == (dst_proj, dst_ds):
            self.show_dataset_images(dst_proj, dst_ds)
            self._refresh_label_filter(dst_proj, dst_ds)

    @staticmethod
    def _scan_import_info(image_path, label_path="", fmt=""):
        """
        扫描导入信息：图像总数 + 已标注数。
        - total = 图像目录下图像数（jpg/jpeg/png/bmp/webp，含子目录）
        - labeled = label_path 里有同名标签文件（按 fmt 后缀）的图像数
        - 无 label_path 或目录不存在时 labeled=0
        返回 (total, labeled)；目录不存在返回 None。
        """
        if not image_path or not os.path.isdir(image_path):
            return None
        IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        total = 0
        names = set()
        for root, _, files in os.walk(image_path):
            for fn in files:
                if fn.lower().endswith(IMAGE_EXTS):
                    total += 1
                    names.add(os.path.splitext(fn)[0])
        labeled = 0
        if label_path and os.path.isdir(label_path) and fmt:
            ext = ".txt" if fmt == ".txt" else ".json"
            try:
                label_names = {os.path.splitext(fn)[0]
                               for fn in os.listdir(label_path)
                               if fn.lower().endswith(ext)}
            except OSError:
                label_names = set()
            labeled = len(names & label_names)
        return total, labeled

    @staticmethod
    def _count_labeled_in_dir(image_path, label_path, ext):
        """
        统计图像目录与标签目录同名的标签文件数(ext: '.txt' / '.json')。
        用于格式选错时的探测: 当前格式匹配 0 张, 检查另一种格式是否
        存在同名标签文件,给用户切换格式的提示.
        """
        try:
            label_names = {os.path.splitext(fn)[0]
                           for fn in os.listdir(label_path)
                           if fn.lower().endswith(ext)}
        except OSError:
            return 0
        if not label_names:
            return 0
        IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        image_names = set()
        for root, _, files in os.walk(image_path):
            for fn in files:
                if fn.lower().endswith(IMAGE_EXTS):
                    image_names.add(os.path.splitext(fn)[0])
        return len(image_names & label_names)

    def _import_dataset(self, project_name, dataset_name):
        """
        数据集右键「导入」: 弹导入对话框(图像路径 + 标签路径可选 + 格式)。
        实时显示: 共 N 张图像，已标注 M 张。
        """
        dlg = QDialog(self)
        dlg.setWindowTitle("导入数据 - {} / {}".format(project_name, dataset_name))
        ui = Ui_ImportData()
        ui.setupUi(dlg)
        ui.horizontalLayout_3.setSpacing(16)
        _fm = QFontMetrics(ui.yolo_fmt.font())
        for rb in (ui.yolo_fmt, ui.labelme_fmt):
            rb.setMinimumWidth(_fm.horizontalAdvance(rb.text()) + 28)  # indicator+spacing
        ui.tips_lbl.setText("请选择图像文件夹")
        ui.progress_bar.setVisible(False)
        ui.done_import_btn.setEnabled(False)
        ui.image_path_txt.setEnabled(False)
        ui.label_path_txt.setEnabled(False)

        def update_tips():
            """实时统计图像目录 + 已标注数 → 更新 tips_lbl 显示。"""
            img_path = ui.image_path_txt.text().strip()
            lbl_path = ui.label_path_txt.text().strip()
            # 分类导入:按子文件夹统计各类别图像数
            if ui.cls_fmt.isChecked():
                if not img_path or not os.path.isdir(img_path):
                    ui.tips_lbl.setText("请选择分类根目录（子文件夹名=类别）")
                    return
                classes = {}
                IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
                for entry in os.listdir(img_path):
                    sub = os.path.join(img_path, entry)
                    if os.path.isdir(sub):
                        n = sum(1 for _, _, fs in os.walk(sub)
                                for fn in fs if fn.lower().endswith(IMAGE_EXTS))
                        if n:
                            classes[entry] = n
                root_n = sum(1 for fn in os.listdir(img_path)
                             if fn.lower().endswith(IMAGE_EXTS))
                if root_n:
                    classes["(根目录)"] = root_n
                if not classes:
                    ui.tips_lbl.setText("所选文件夹下无分类子文件夹或图像")
                else:
                    desc = ", ".join("{}: {}张".format(k, v)
                                     for k, v in sorted(classes.items()))
                    ui.tips_lbl.setText("检测到 {} 类：{}".format(
                        len(classes), desc))
                return
            fmt = ".txt" if ui.yolo_fmt.isChecked() else ".json"
            if not img_path or not os.path.isdir(img_path):
                ui.tips_lbl.setText("请选择图像文件夹")
                return
            total, labeled = self._scan_import_info(img_path, lbl_path, fmt)
            if total == 0:
                ui.tips_lbl.setText("所选文件夹无图像")
            elif labeled > 0:
                ui.tips_lbl.setText("共 {} 张图像，已标注 {} 张".format(total, labeled))
            else:
                alt_tip = ""
                if lbl_path and os.path.isdir(lbl_path):
                    alt_ext = ".txt" if fmt == ".json" else ".json"
                    alt_fmt_name = "Yolo txt" if alt_ext == ".txt" else "Labelme json"
                    try:
                        alt_names = {os.path.splitext(fn)[0]
                                     for fn in os.listdir(lbl_path)
                                     if fn.lower().endswith(alt_ext)}
                    except OSError:
                        alt_names = set()
                    if alt_names:
                        alt_labeled = self._count_labeled_in_dir(
                            img_path, lbl_path, alt_ext)
                        if alt_labeled > 0:
                            alt_tip = "（检测到 {} 张 {} 标签，请切换上方格式为「{}」）".format(
                                alt_labeled, alt_ext, alt_fmt_name)
                if alt_tip:
                    ui.tips_lbl.setText("共 {} 张图像，已标注 0 张 {}".format(total, alt_tip))
                else:
                    ui.tips_lbl.setText("共 {} 张图像（标签目录无匹配文件）".format(total))

        def choose_folder(operator_name):
            folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
            if not folder:
                return
            if operator_name == "图像":
                ui.image_path_txt.setEnabled(True)
                ui.image_path_txt.setText(folder)
            else:
                ui.label_path_txt.setEnabled(True)
                ui.label_path_txt.setText(folder)
            ui.done_import_btn.setEnabled(bool(ui.image_path_txt.text().strip()))
            update_tips()

        ui.choose_image_dir_btn.clicked.connect(lambda: choose_folder("图像"))
        ui.choose_label_dir_btn.clicked.connect(lambda: choose_folder("标签"))
        ui.yolo_fmt.toggled.connect(update_tips)
        ui.labelme_fmt.toggled.connect(update_tips)

        def set_cls_mode(on):
            """切换「按子文件夹分类导入」:分类模式只需根目录,标签路径/格式不可用。"""
            ui.label_path_txt.setEnabled(not on)
            ui.choose_label_dir_btn.setEnabled(not on)
            for rb in (ui.yolo_fmt, ui.labelme_fmt):
                rb.setEnabled(not on)
            ui.image_path_txt.setPlaceholderText(
                "分类根目录（子文件夹名=类别）" if on else "图像路径")
            if on:
                ui.label_path_txt.clear()
            ui.done_import_btn.setEnabled(bool(ui.image_path_txt.text().strip()))
            update_tips()

        ui.cls_fmt.toggled.connect(set_cls_mode)

        def do_import():
            IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
            cls_mode = ui.cls_fmt.isChecked()
            image_path = ui.image_path_txt.text().strip()
            label_path = "" if cls_mode else ui.label_path_txt.text().strip()
            fmt = "cls" if cls_mode else (
                ".txt" if ui.yolo_fmt.isChecked() else ".json")
            if not image_path or not os.path.isdir(image_path):
                MessageBox.warning(dlg, "导入数据", "请先选择有效的图像文件夹")
                return
            if label_path and not os.path.isdir(label_path):
                MessageBox.warning(dlg, "导入数据", "标签路径无效")
                return
            dlg.accept()
            if cls_mode:
                _total = 0
                for _r, _, _fs in os.walk(image_path):
                    for _fn in _fs:
                        if _fn.lower().endswith(IMAGE_EXTS):
                            _total += 1
                _labeled = _total
            else:
                _scanned = self._scan_import_info(image_path, label_path, fmt)
                _total = _scanned[0] if _scanned else 0
                _labeled = _scanned[1] if _scanned else 0
            self.db.update_dataset_import(project_name, dataset_name,
                                          image_path, label_path, fmt,
                                          labeled=_labeled, total=_total)
            self._refresh_dataset_row_progress(project_name, dataset_name)
            self._start_import_thread(project_name, dataset_name,
                                      image_path, label_path, fmt,
                                      update_stats=True)

        ui.done_import_btn.clicked.connect(do_import)
        dlg.exec()

    def _on_toolbar_import(self):
        """工具栏「导入」按钮: 为当前选中的数据集触发导入流程。"""
        if not self._current_dataset:
            MessageBox.warning(self, "导入", "请先在左侧选中一个数据集")
            return
        project, dataset = self._current_dataset
        self._import_dataset(project, dataset)

    def _on_export_clicked(self):
        """
        工具栏「导出」按钮:弹导出对话框（路径 + 格式）,
        选中项目 -> 导出项目下全部数据集；选中数据集 → 导出该数据集。
        目录结构：数据集 <保存路径>/<数据集名>/images|labels;
        项目 <保存路径>/<项目名>/<数据集名>/images|labels。
        标签按所选格式转换导出(labelme json / yolo txt)。
        """
        item = self.project_tree.currentItem()
        if item is None:
            MessageBox.warning(self, "导出", "请先在左侧选中要导出的项目或数据集")
            return
        kind = item.data(0, Qt.UserRole)
        if not kind:
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("导出")
        ui = ExportDataUI()
        ui.setupUi(dlg)
        ui.export_path_txt.setReadOnly(True)
        ui.exp_labelme_fmt.setChecked(True)    # 默认 labelme 格式
        ui.select_path_btn.clicked.connect(
            lambda: self._pick_export_path(dlg, ui))
        ui.do_export_btn.clicked.connect(dlg.accept)
        if dlg.exec() != QDialog.Accepted:
            return
        save_dir = ui.export_path_txt.text().strip()
        if not save_dir:
            MessageBox.warning(self, "导出", "请先选择导出保存位置")
            return
        fmt = "yolo" if ui.exp_yolo_fmt.isChecked() else "labelme"
        try:
            if kind[0] == "project":
                project_name = kind[1]
                root = os.path.join(save_dir, project_name)
                ds_list = [(project_name, d["dataset_name"])
                           for d in self.db.get_datasets(project_name)]
                src = "; ".join(self._export_source(project_name, ds)
                                for _, ds in ds_list)
                self._log("开始导出: 项目={} | 源路径={} | 保存路径={} | 格式={}".format(
                    project_name, src, root, fmt))
                recs_map = {ds: self._collect_export_recs(project_name, ds)
                            for _, ds in ds_list}
                total = sum(len(v) for v in recs_map.values())
                dlg2 = ProgressDialog("导出", "正在导出项目…", self, maximum=max(1, total))
                try:
                    done = 0
                    for proj, ds in ds_list:
                        done += self._export_dataset(
                            proj, ds, root, fmt=fmt, progress=dlg2,
                            base_done=done, total=total)
                finally:
                    dlg2.close()
                MessageBox.information(
                    self, "导出",
                    "项目「{}」导出完成，共复制 {} 张图像\n位置：{}".format(
                        project_name, total, root))
                self._log("导出项目完成: {} | {} 张图像 | 标签({}) | 格式={} | → {}".format(
                    project_name, total,
                    self._export_labels(project_name, ds_list), fmt, root))
            else:
                project_name, dataset_name = kind[1], kind[2]
                src = self._export_source(project_name, dataset_name)
                self._log("开始导出: 数据集={}/{} | 源路径={} | 保存路径={} | 格式={}".format(
                    project_name, dataset_name, src, save_dir, fmt))
                recs = self._collect_export_recs(project_name, dataset_name)
                dlg2 = ProgressDialog("导出", "正在导出数据集…", self,
                                      maximum=max(1, len(recs)))
                try:
                    total = self._export_dataset(
                        project_name, dataset_name, save_dir, fmt=fmt,
                        progress=dlg2, total=len(recs))
                finally:
                    dlg2.close()
                MessageBox.information(
                    self, "导出",
                    "数据集「{}」导出完成，共复制 {} 张图像\n位置：{}".format(
                        dataset_name, total,
                        os.path.join(save_dir, dataset_name)))
                self._log("导出数据集完成: {}/{} | {} 张图像 | 标签({}) | 格式={} | → {}".format(
                    project_name, dataset_name, total,
                    self._export_labels(project_name, [(project_name, dataset_name)]),
                    fmt, os.path.join(save_dir, dataset_name)))
        except Exception as e:
            MessageBox.critical(self, "导出失败", str(e))

    def _pick_export_path(self, dlg, ui):
        path = QFileDialog.getExistingDirectory(dlg, "选择导出保存位置")
        if path:
            ui.export_path_txt.setText(path)

    def _collect_export_recs(self, project_name, dataset_name):
        """返回该数据集待导出的图像记录列表（缓存优先，无缓存 os.walk 扫描）。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if index:
            return list(index.get("all", []))
        recs = []
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        image_paths = binding.get("image_paths") or (
            [binding.get("image_path")] if binding.get("image_path") else [])
        IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        for img_root in image_paths:
            if not img_root or not os.path.isdir(img_root):
                continue
            for root, _, files in os.walk(img_root):
                for fn in files:
                    if fn.lower().endswith(IMAGE_EXTS):
                        recs.append({"image_path": os.path.join(root, fn)})
        return recs

    def _export_source(self, project_name, dataset_name):
        """数据集导入源路径摘要（图像目录 + 标签目录），供导出日志用。"""
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        img = binding.get("image_paths") or (
            [binding.get("image_path")] if binding.get("image_path") else [])
        lbl = binding.get("label_paths") or (
            [binding.get("label_path")] if binding.get("label_path") else [])
        return "{} => 标签:{}".format(";".join(img or ["(无)"]),
                                     ";".join(lbl or ["(无)"]))

    def _export_labels(self, project_name, ds_list):
        """数据集标签列表摘要（label_sort_key 排序），供导出日志用。"""
        all_labels = set()
        for proj, ds in ds_list:
            all_labels.update(self.db.get_dataset_labels(proj, ds))
        return ", ".join(sorted(all_labels, key=label_sort_key)) or "(无标签)"

    def _export_dataset(self, project_name, dataset_name, base_dir,
                        fmt="labelme", progress=None, base_done=0, total=None):
        """
        导出单个数据集到 base_dir/<数据集名>/images|labels。
        图像直接复制:标签按 fmt 转换导出;
        - labelme:同路径 json优先复制,否则从源标签转成 json
        - yolo:从标注 boxes 转成 yolo txt(类别ID 按 db 标签排序映射)
        progress：ProgressDialog（set_progress + is_cancelled）；中断返回已复制数。
        """
        ds_dir = os.path.join(base_dir, dataset_name)
        img_dir = os.path.join(ds_dir, "images")
        lbl_dir = os.path.join(ds_dir, "labels")
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(lbl_dir, exist_ok=True)
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        # yolo 类别 ID 映射:db 标签按 label_sort_key 排序后的序号
        labels = self.db.get_dataset_labels(project_name, dataset_name)
        label_to_id = {name: i for i, name in
                       enumerate(sorted(labels, key=label_sort_key))}

        recs = self._collect_export_recs(project_name, dataset_name)
        copied = 0
        for i, rec in enumerate(recs):
            src = rec.get("image_path", "")
            if not src or not os.path.exists(src):
                continue
            if progress is not None:
                if progress.is_cancelled():
                    return copied
                progress.set_progress(
                    base_done + i,
                    "正在导出: {}".format(os.path.basename(src)))
            dst = os.path.join(img_dir, os.path.basename(src))
            if os.path.abspath(src) != os.path.abspath(dst):
                shutil.copy2(src, dst)
            copied += 1
            self._export_label_file(src, fmt, label_to_id, binding, lbl_dir)
        return copied

    def _export_label_file(self, img_src, fmt, label_to_id, binding, lbl_dir):
        """按目标格式把一张图的标注写入 lbl_dir(同名文件)."""
        stem = os.path.splitext(os.path.basename(img_src))[0]
        base_wo_ext, _ = os.path.splitext(img_src)
        # labelme: 同路径 json 标注直接复制(保持标注界面的原始 json)
        if fmt == "labelme":
            same_json = base_wo_ext + ".json"
            if os.path.exists(same_json):
                shutil.copy2(same_json, os.path.join(lbl_dir, stem + ".json"))
                return
        boxes = self._read_export_boxes(img_src, binding)
        if not boxes:
            return
        try:
            with PILImage.open(img_src) as im:
                iw, ih = im.size
        except Exception:
            return
        target = os.path.join(lbl_dir,
                              stem + (".json" if fmt == "labelme" else ".txt"))
        if fmt == "labelme":
            data = _boxes_to_labelme_json(boxes, img_src, iw, ih)
            with open(target, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            text = boxes_to_yolo_text(boxes, iw, ih, label_to_id)
            if text:
                with open(target, "w", encoding="utf-8") as f:
                    f.write(text + "\n")

    def _read_export_boxes(self, img_src, binding):
        """
        读取一张图的标注 boxes(像素坐标 + label).
        优先同路径 labelme json(标注产物),否则 label_paths 同名标签.
        """
        base_wo_ext, _ = os.path.splitext(img_src)
        same_json = base_wo_ext + ".json"
        if os.path.exists(same_json):
            return load_json_boxes(same_json)
        label_fmt = binding.get("label_fmt", "")
        if not label_fmt:
            return []
        ext = ".txt" if label_fmt == ".txt" else ".json"
        stem = os.path.splitext(os.path.basename(img_src))[0]
        for lp in (binding.get("label_paths") or
                   ([binding.get("label_path")] if binding.get("label_path") else [])):
            if not lp or not os.path.isdir(lp):
                continue
            cand = os.path.join(lp, stem + ext)
            if not os.path.exists(cand):
                continue
            if ext == ".json":
                return load_json_boxes(cand)
            return _load_yolo_boxes(cand, img_src)
        return []

    def _on_train_clicked(self):
        # 独立入口:无需先选中数据集,任务类型在训练界面选择
        dlg = TrainDialog(self)
        dlg.exec()

    def _on_dataset_properties(self):
        """工具栏「属性」按钮:弹数据集属性对话框(路径 + 标签分布柱状图)。"""
        if not self._current_dataset:
            MessageBox.warning(self, "属性", "请先在左侧选中一个数据集")
            return
        project, dataset = self._current_dataset
        dlg = QDialog(self)
        dlg.setWindowTitle("数据集属性 - {} / {}".format(project, dataset))
        # 支持最小化/最大化(默认 dialog 只有关闭按钮)
        dlg.setWindowFlags(
            dlg.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        ui = DatasetPropertiesUI()
        ui.setupUi(dlg)
        info = self.db.get_dataset_import(project, dataset) or {}
        image_paths = info.get("image_paths") or []
        label_paths = info.get("label_paths") or []
        ui.image_path_line_txt.setText("; ".join(image_paths) or "(未设置)")
        ui.label_path_line_txt.setText("; ".join(label_paths) or "(未设置)")
        ui.image_path_line_txt.setReadOnly(True)
        ui.label_path_line_txt.setReadOnly(True)
        cache = self.dataset_cache.get(project, {}).get(dataset, {})
        counts = {}
        for rec in cache.get("all", []):
            for b in (rec.get("boxes") or []):
                lbl = b[-1]
                counts[lbl] = counts.get(lbl, 0) + 1
        if not counts:
            labels_index = cache.get("labels") or {}
            counts = {label: len(recs) for label, recs in labels_index.items()}
        if counts:
            self.db.save_dataset_label_counts(project, dataset, counts)
        else:
            counts = self.db.get_dataset_label_counts(project, dataset)
        self._render_label_stats(ui.label_stats_view, project, dataset, counts)
        dlg.exec()

    def _render_label_stats(self, view, project, dataset, label_counts):
        """标签分布柱状图(宽度随标签数量扩展,超宽用滚动条)。"""
        num_bars = max(1, len(label_counts))
        fig_width = max(4.0, num_bars * 0.3)
        fig_height = 6.0
        fig = Figure(figsize=(fig_width, fig_height), dpi=100, facecolor="#1c1e25")
        axes = fig.add_subplot(111, facecolor="#1c1e25")
        scene = QGraphicsScene()
        if not label_counts:
            axes.text(0.5, 0.5, "暂无标注", ha="center", va="center",
                      color="#8a92a3", transform=axes.transAxes, fontsize=14)
            axes.set_xticks([])
            axes.set_yticks([])
        else:
            label_colors = self.db.get_dataset_labels(project, dataset)
            # 按标签数量降序(教程:自动按数量降序)
            items = sorted(label_counts.items(), key=lambda kv: kv[1],
                           reverse=True)
            labels = [k for k, _ in items]
            values = [v for _, v in items]
            colors = [label_colors.get(name, "#5B8CFF") for name in labels]
            # 柱宽(数据单位)≈ n/15.5:使柱宽像素 = 图宽/20;多标签时收紧防重叠
            bar_width = max(0.05, min(0.15, num_bars / 15.5))
            x_positions = np.arange(num_bars)
            bars = axes.bar(x_positions, values, color=colors, width=bar_width,
                            edgecolor="none")
            ymax = max(values) if values else 0
            for bar, v in zip(bars, values):
                axes.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                          str(v), ha="center", va="bottom",
                          color="#e8eaf0", fontsize=10)
            axes.set_xlabel("标签", color="#c3c9d6", fontsize=11, labelpad=8)
            axes.set_ylabel("标签数量", color="#c3c9d6", fontsize=11, labelpad=8)
            axes.tick_params(axis="x", colors="#c3c9d6", labelsize=10, rotation=0)
            axes.tick_params(axis="y", colors="#c3c9d6", labelsize=10)
            axes.set_ylim(0, ymax * 1.12 if ymax else 1)
            for side in ("top", "right"):
                axes.spines[side].set_visible(False)
            for side in ("left", "bottom"):
                axes.spines[side].set_color("#3a3f4e")
            axes.yaxis.grid(True, color="#2a2e38", linestyle="--", linewidth=0.6, alpha=0.8)
            axes.set_axisbelow(True)
            axes.set_xticks(x_positions)
            axes.set_xticklabels(labels)
            axes.set_xlim(-0.5, num_bars - 0.5)
            axes.set_ylim(0, ymax * 1.12 if ymax else 1)
        canvas = FigureCanvasQTAgg(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()
        image = QImage(canvas.buffer_rgba(), int(width), int(height),
                       QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(image)
        scene.addPixmap(pixmap)
        scene.update()
        view.setScene(scene)
        if view.sceneRect().isEmpty():
            view.setSceneRect(scene.itemsBoundingRect())

    def _start_import_thread(self, project_name, dataset_name,
                             image_path, label_path="", fmt="",
                             update_stats=False, excluded=None):
        """
        启动后台导入线程
        """
        self._log("开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}".format(
            project_name, dataset_name, image_path, label_path or "(无)", fmt))
        key = (project_name, dataset_name)
        if update_stats:
            self._loading_tasks.pop(key, None)
        elif key in self._loading_tasks:
            return
        ds_item = self._find_dataset_item(project_name, dataset_name)
        progress = None
        progress_lbl = None
        # container = None
        if ds_item is not None:
            container = self.project_tree.itemWidget(ds_item, 0)
            if container is not None:
                progress_lbl = container.findChild(QLabel, "datasetRowProgress")
                if progress_lbl is not None:
                    progress_lbl.setVisible(False)
                progress = QProgressBar(container)
                progress.setRange(0, 100)
                progress.setValue(0)
                progress.setFixedSize(140, 14)
                progress.setTextVisible(True)
                progress.setStyleSheet(
                    "QProgressBar { background-color: rgba(91,140,255,0.25);"
                    " border: none; border-radius: 3px;"
                    " color: #ffffff; font-size: 10px; }"
                    " QProgressBar::chunk { background-color: #5b8cff;"
                    " border-radius: 3px; }")
                h = container.layout()
                h.addWidget(progress)
                h.setAlignment(progress, Qt.AlignVCenter)
        task = _ImportTask(image_path, label_path, fmt, parent=self, excluded=excluded)
        self._loading_tasks[key] = task

        def on_progress(v):
            if progress is not None:
                progress.setValue(v)

        def on_finished(result):
            cls_mode = fmt == "cls"
            total = len(result)
            # 分类模式:每张图都有类别,视为全部已标注
            labeled = total if cls_mode else sum(
                1 for r in result if r.get("boxes"))
            if update_stats:
                new_label_path = label_path
                new_fmt = fmt
                if labeled > 0 and not cls_mode:
                    binding = self.db.get_dataset_import(
                        project_name, dataset_name)
                    old_label = binding.get("label_paths") or (
                        [binding.get("label_path")]
                        if binding.get("label_path") else [])
                    if not old_label:
                        new_label_path = image_path
                        new_fmt = ".json"
                self.db.update_dataset_import(project_name, dataset_name,
                                              image_path, new_label_path,
                                              new_fmt,
                                              labeled=labeled, total=total)
            else:
                binding = self.db.get_dataset_import(project_name, dataset_name)
                labeled = binding.get("labeled", labeled)
                total = binding.get("total", total) or total
            if progress is not None:
                progress.deleteLater()
            if progress_lbl is not None:
                progress_lbl.setVisible(True)
                progress_lbl.setText("{}/{}".format(labeled, total))
            proj_cache = self.dataset_cache.setdefault(project_name, {})
            proj_cache[dataset_name] = self._build_dataset_index(result)
            # 检测/分割按框,分类按类别;持久化供属性页无缓存时展示
            label_counts = {}
            for rec in result:
                for b in (rec.get("boxes") or []):
                    lbl = b[-1]
                    label_counts[lbl] = label_counts.get(lbl, 0) + 1
            if not label_counts:
                for rec in result:
                    for lbl in (rec.get("labels") or []):
                        label_counts[lbl] = label_counts.get(lbl, 0) + 1
            self.db.save_dataset_label_counts(project_name, dataset_name, label_counts)
            counts_str = ", ".join(
                "{}: {}个".format(k, v) for k, v in
                sorted(label_counts.items(), key=lambda kv: label_sort_key(kv[0])))
            self._log("数据集导入完成: {}/{} | 图像 {} 张，已标注 {} 张"
                      " | 标签({}类): {}".format(
                          project_name, dataset_name, total, labeled,
                          len(label_counts), counts_str or "(无)"))
            self._refresh_dataset_labels(project_name, dataset_name)
            index = proj_cache[dataset_name]
            current_labels = self.db.get_dataset_labels(project_name, dataset_name)
            cleaned = {normalize_label(k): v for k, v in current_labels.items()}
            if cleaned != current_labels:
                self.db.save_dataset_labels(project_name, dataset_name, cleaned)
                current_labels = cleaned
            for lbl in index.get("labels", {}):
                if lbl not in current_labels:
                    self.db.add_dataset_label(project_name, dataset_name,
                                              lbl, label_color(lbl).name())
                    current_labels[lbl] = label_color(lbl).name()
            if self._current_dataset == (project_name, dataset_name):
                self._refresh_label_filter(project_name, dataset_name)
            if getattr(self, "_current_dataset", None) == (project_name, dataset_name):
                self.show_dataset_images(project_name, dataset_name)
            if self._loading_tasks.get(key) is task:
                del self._loading_tasks[key]

        task.progress_updated.connect(on_progress)
        task.finished_signal.connect(on_finished)
        task.finished_signal.connect(task.deleteLater)
        task.start()

    def _find_dataset_item(self, project_name, dataset_name):
        """在项目树中定位数据集节点(展开状态下)。"""
        if not hasattr(self, "project_tree"):
            return None
        for i in range(self.project_tree.topLevelItemCount()):
            proj_item = self.project_tree.topLevelItem(i)
            if proj_item.data(0, Qt.UserRole) == ("project", project_name):
                for j in range(proj_item.childCount()):
                    child = proj_item.child(j)
                    if child.data(0, Qt.UserRole) == ("dataset", project_name, dataset_name):
                        return child
        return None

    def _on_project_tree_clicked(self, item, column):
        """点击：仅记录选中；已缓存的数据集切换显示，未缓存不触发加载。"""
        kind = item.data(0, Qt.UserRole)
        if not kind:
            return
        if kind[0] == "dataset":
            project, dataset = kind[1], kind[2]
            self._current_dataset = (project, dataset)
            if self.dataset_cache.get(project, {}).get(dataset):
                self.current_label = "__unlabeled__"
                self._refresh_label_filter(project, dataset)
                self.show_dataset_images(project, dataset)
            else:
                self._reset_image_area()
        elif kind[0] == "project":
            self._current_dataset = None
            self._reset_image_area()

    def _load_dataset_view(self, project, dataset):
        """
        右键「载入」: 强制重扫并显示数据集图像。
        丢弃旧缓存强制重扫,否则推理/标注界面新写的 labelme json 不会被读入。
        """
        self._current_dataset = (project, dataset)
        self.current_label = "__unlabeled__"
        proj_cache = self.dataset_cache.setdefault(project, {})
        proj_cache.pop(dataset, None)
        self._refresh_label_filter(project, dataset)
        self.show_dataset_images(project, dataset, update_stats=True)

    def _view_data_by_label(self, data):
        """
        按当前筛选 current_label 取 view_data(未标注 / 具体标签 / 全部)。
        用于分页和渲染:分页按筛选后 view_data 计算(不再是全量)。
        """
        cur = self.current_label
        all_records = data.get("all", [])
        if cur == "__unlabeled__":
            return [r for r in all_records if not r.get("labels")]
        if cur and cur in data.get("labels", {}):
            return data["labels"][cur]
        return all_records

    def _expand_by_label(self, data):
        """按标签把图像列表按 box 展开为 (rec, box_idx);未标注/全部/分类原样返回。"""
        cur = self.current_label
        if not cur or cur == "__unlabeled__":
            return data
        expanded = []
        for rec in data:
            if rec.get("cls"):
                expanded.append(rec)
                continue
            matched = False
            for box_idx, box in enumerate(rec.get("boxes") or []):
                if len(box) >= 5 and box[4] == cur:
                    expanded.append((rec, box_idx))
                    matched = True
            if not matched and not (rec.get("boxes") or []):
                expanded.append(rec)
        return expanded

    def show_dataset_images(self, project_name, dataset_name, update_stats=False):
        """
        从内存缓存取该数据集图像显示;无缓存则尝试后台加载（多路径合并）。
        update_stats=True 时重扫完成会把 labeled/total 写回 db(右键「载入」场景,
        推理/标注新写的标签 json 重扫后同步统计)。
        """
        proj_cache = self.dataset_cache.get(project_name, {})
        data = proj_cache.get(dataset_name)
        if data:
            self.current_page = 0
            self._render_scene(self._view_data_by_label(data))
            return
        binding = self.db.get_dataset_import(project_name, dataset_name)
        if binding:
            image_paths = binding.get("image_paths") or (
                [binding.get("image_path")] if binding.get("image_path") else [])
            label_paths = binding.get("label_paths") or (
                [binding.get("label_path")] if binding.get("label_path") else [])
            valid_images = [p for p in image_paths if p and os.path.isdir(p)]
            if valid_images:
                excluded = self.db.get_deleted_images(project_name, dataset_name)
                self._start_import_thread(project_name, dataset_name,
                                          valid_images, label_paths,
                                          binding.get("label_fmt", ""),
                                          update_stats=update_stats,
                                          excluded=excluded)
                return
        self._clear_scene()

    @staticmethod
    def _build_dataset_index(result):
        """
        把导入结果构造成 项目-数据集-标签 索引：
        {"all": [全部图像记录...], "labels": {标签名: [图像记录...]}}
        一张图可出现在多个标签下（一图多缺陷）。
        统一归一化 rec.labels / rec.boxes 的标签名（class_N → N），
        保证缓存索引与筛选下拉/重命名/删除使用的标签名一致。
        """
        index = {"all": [], "labels": {}}
        for rec in result:
            if rec.get("labels"):
                rec["labels"] = [normalize_label(l) for l in rec["labels"]]
            if rec.get("boxes"):
                rec["boxes"] = [tuple(b[:-1]) + (normalize_label(b[-1]),)
                                for b in rec["boxes"]]
            rec["rois"] = {}
            index["all"].append(rec)
            for label in set(rec.get("labels") or []):
                index["labels"].setdefault(label, []).append(rec)
        return index

    def _refresh_dataset_labels(self, project_name, dataset_name):
        """
        标注完成后重建缓存中的 labels 索引：
        对每张图读同路径 labelme json 获取最新标注标签(无 json 保留导入时的 labels),
        然后重建 labels 分组索引写回 dataset_cache。
        轻量操作：只读 json,不重新生成缩略图,不扫描磁盘。
        """
        proj_cache = self.dataset_cache.get(project_name, {})
        index = proj_cache.get(dataset_name)
        if not index:
            return
        for rec in index.get("all", []):
            img_path = rec.get("image_path", "")
            base, _ = os.path.splitext(img_path)
            json_path = base + ".json"
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    labels = []
                    boxes = []
                    for shape in data.get("shapes", []):
                        lbl = normalize_label(shape.get("label", ""))
                        if not lbl:
                            continue
                        labels.append(lbl)
                        pts = shape.get("points", [])
                        if len(pts) >= 2:
                            xs = [p[0] for p in pts]
                            ys = [p[1] for p in pts]
                            x, y = int(min(xs)), int(min(ys))
                            w, h = int(max(xs) - min(xs)), int(max(ys) - min(ys))
                            boxes.append((max(0, x), max(0, y), max(1, w), max(1, h), lbl))
                    rec["labels"] = labels
                    rec["boxes"] = boxes if boxes else None
                    rec["rois"] = {}
                    rec["_has_annotation_json"] = True
                except Exception:
                    pass
            elif rec.get("_has_annotation_json"):
                rec["labels"] = []
                rec["boxes"] = None
                rec["rois"] = {}
                rec["_has_annotation_json"] = False

        for rec in index.get("all", []):
            if rec.get("labels"):
                rec["labels"] = [normalize_label(l) for l in rec["labels"]]
            if rec.get("boxes"):
                rec["boxes"] = [tuple(b[:-1]) + (normalize_label(b[-1]),)
                                for b in rec["boxes"]]
        index["labels"] = {}
        for rec in index.get("all", []):
            for label in set(rec.get("labels") or []):
                index["labels"].setdefault(label, []).append(rec)
        proj_cache[dataset_name] = index

    def _clear_scene(self):
        scene = self.graphics_view.scene()
        scene.clear()

    def _reset_image_area(self):
        """
        切到非数据集状态(点项目级别 / 删除数据集)时统一清空图像区
        及所有相关 UI 状态: 分页信息, 当前页码, 标签筛选下拉框、
        标注统计 labelStatsLabel。
        与图像显示区(_clear_scene)一起重置,避免显示残留的旧数据集状态。
        """
        self._clear_scene()
        self.pageInfoLabel.setText("0 / 0")
        self.current_page = 0
        if hasattr(self, "label_filter_combo"):
            self.label_filter_combo.blockSignals(True)
            self.label_filter_combo.clear()
            self.label_filter_combo.addItem("未标注", "__unlabeled__")
            self.label_filter_combo.setCurrentIndex(0)
            self.label_filter_combo.blockSignals(False)
        self.current_label = "__unlabeled__"
        if hasattr(self, "labelStatsLabel"):
            self.labelStatsLabel.setVisible(False)

    def _get_thumb(self, rec):
        """
        懒生成整图缩略图并缓存到 rec["thumb"]（渲染当前页时调用）。
        载入不再全量生成缩略图(大数据集全量解码很慢)，改为渲染到某页时才现场解码该页图像
        翻页/切回/再次筛选命中缓存不重复解码:解码失败也缓存 None。
        """
        if rec.get("thumb") is not None:
            return rec["thumb"]
        qimg = None
        img_path = rec.get("image_path", "")
        if img_path and PILImage is not None:
            try:
                im = PILImage.open(img_path)
                im.draft("RGB", (200, 200))
                im = im.convert("RGB")
                qimg = _pil_to_qimage(_make_uniform_thumb(im))
            except Exception:
                qimg = None
        rec["thumb"] = qimg
        return qimg

    def _get_rois(self, rec, label):
        """懒生成某标签的 ROI 裁剪小图并缓存到 rec["rois"][label]。"""
        rois = rec.setdefault("rois", {})
        if label in rois:
            return rois[label]
        result = []
        boxes = rec.get("boxes") or []
        img_path = rec.get("image_path", "")
        if boxes and img_path and PILImage is not None:
            try:
                im = PILImage.open(img_path).convert("RGB")
                for box in boxes:
                    if len(box) >= 5 and box[4] == label:
                        x, y, w, h = box[0], box[1], box[2], box[3]
                        crop = im.crop((x, y, x + w, y + h))
                        qimg = _pil_to_qimage(_make_uniform_thumb(crop, fill=True))
                        if qimg is not None:
                            result.append(qimg)
            except Exception:
                pass
        rois[label] = result
        return result

    def _get_roi_at(self, rec, label, box_idx):
        """取第 box_idx 个匹配 box 的 ROI 缩略图并缓存(区别于 _get_rois 只裁一个,省内存)。"""
        cache = rec.setdefault("rois_by_idx", {}).setdefault(label, {})
        if box_idx in cache:
            return cache[box_idx]
        qimg = None
        boxes = rec.get("boxes") or []
        img_path = rec.get("image_path", "")
        if 0 <= box_idx < len(boxes) and img_path and PILImage is not None:
            box = boxes[box_idx]
            if len(box) >= 5 and box[4] == label:
                try:
                    im = PILImage.open(img_path).convert("RGB")
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    crop = im.crop((x, y, x + w, y + h))
                    qimg = _pil_to_qimage(_make_uniform_thumb(crop, fill=True))
                except Exception:
                    qimg = None
        cache[box_idx] = qimg
        return qimg

    def _render_scene(self, data):
        """渲染当前页图像网格。按具体标签筛选时每个 cell 一个 ROI(box 计数),
        未标注/全部按整图缩略(图像计数)。"""
        scene = self.graphics_view.scene()
        scene.clear()
        page_size = getattr(self, "page_size", 50)
        cur_label = getattr(self, "current_label", None)
        view_data = self._expand_by_label(data)
        total_pages = max(1, (len(view_data) + page_size - 1) // page_size)
        self.current_page = max(0, min(getattr(self, "current_page", 0), total_pages - 1))
        page_data = list(Paginator(view_data, page_size)[self.current_page])
        cell_w, cell_h = 230, 230
        pad = 10
        cols = max(1, int((self.graphics_view.viewport().width() - pad) // cell_w))
        pos = 0
        for entry in page_data:
            if isinstance(entry, tuple):
                rec, box_idx = entry
                single_box = True
            else:
                rec, box_idx = entry, None
                single_box = False
            if (cur_label and cur_label != "__unlabeled__"
                    and not rec.get("cls")):
                if single_box:
                    qimg = self._get_roi_at(rec, cur_label, box_idx)
                else:
                    qimg = self._get_thumb(rec)
                qimgs = [qimg] if qimg is not None else []
            else:
                qimg = self._get_thumb(rec)
                qimgs = [qimg] if qimg is not None else []
            for qimg in qimgs:
                pix = QPixmap.fromImage(qimg)
                if pix.isNull():
                    continue
                item = SelectablePixmapItem(pix, rec.get("image_path", ""))
                scene.addItem(item)
                row = pos // cols
                col = pos % cols
                x = col * (cell_w + pad) + pad
                y = row * (cell_h + pad) + pad
                item.setPos(x + (cell_w - pix.width()) // 2, y + (cell_h - pix.height()) // 2)
                item.setToolTip(rec.get("image_path", ""))
                item.setData(0, rec.get("image_path", ""))  # 双击定位用
                pos += 1
        scene.setSceneRect(scene.itemsBoundingRect().adjusted(-10, -10, 20, 20))
        if cur_label and cur_label != "__unlabeled__":
            self.pageInfoLabel.setText("第 {}/{} 页 · 共 {} 个".format(
                self.current_page + 1, total_pages, len(view_data)))
        else:
            self.pageInfoLabel.setText("第 {}/{} 页 · 共 {} 张".format(
                self.current_page + 1, total_pages, len(view_data)))
        self.pre_page_btn.setEnabled(self.current_page > 0)
        self.next_page_btn.setEnabled(self.current_page < total_pages - 1)

    def _show_page(self, offset):
        """当前数据集翻页(offset: +1/-1)。分页数据与显示时一致（应用标签筛选）。"""
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds:
            return
        proj, ds = cur_ds
        data = self.dataset_cache.get(proj, {}).get(ds)
        if not data:
            return
        view_data = self._expand_by_label(self._view_data_by_label(data))
        total_pages = max(1, (len(view_data) + self.page_size - 1) // self.page_size)
        self.current_page = max(0, min(self.current_page + offset, total_pages - 1))
        self._render_scene(self._view_data_by_label(data))

    def pre_page(self):
        self._show_page(-1)

    def next_page(self):
        self._show_page(1)

    def register_event(self):
        self.add_project_btn.clicked.connect(lambda: self.add_project())
        self.pre_page_btn.clicked.connect(lambda: self.pre_page())
        self.next_page_btn.clicked.connect(lambda: self.next_page())
        self.import_dataset_btn.clicked.connect(self._on_toolbar_import)
        self.dataset_properties_btn.clicked.connect(self._on_dataset_properties)
        self.export_dataset_btn.clicked.connect(self._on_export_clicked)
        self.stop_train_btn.clicked.connect(
            lambda checked=False: self.stop_training())
        self.rename_label_btn.clicked.connect(self._on_rename_label)
        self.delete_label_btn.clicked.connect(self._on_delete_label)
        self.train_btn.clicked.connect(self._on_train_clicked)
        self.log_btn.clicked.connect(self._on_log_clicked)
        self.model_btn.clicked.connect(self._on_model_clicked)

    def fill_setting(self):
        """启动时从 db 查询项目数据，显示到界面。"""
        self.refresh_project_list()

    def eventFilter(self, obj, event):
        """拦截 graphics_view 双击事件(双击小图进入标注)。"""
        if (obj is self.graphics_view.viewport()
                and event.type() == QEvent.MouseButtonDblClick):
            self._on_graphics_double_click(event.position().toPoint())
            return True
        return super().eventFilter(obj, event)

    def _refresh_annotation_progress(self, project_name, dataset_name):
        """标注完成后重新统计该数据集已标注数量并写 db、刷新树节点。"""
        proj_cache = self.dataset_cache.get(project_name, {})
        index = proj_cache.get(dataset_name)
        if not index:
            return
        total = len(index["all"])
        labeled = 0
        for rec in index["all"]:
            if rec.get("boxes") or self._has_label_file(rec.get("image_path", "")):
                labeled += 1
        binding = self.db.get_dataset_import(project_name, dataset_name)
        self.db.update_dataset_import(
            project_name, dataset_name,
            binding.get("image_path", ""), binding.get("label_path", ""),
            binding.get("label_fmt", ""), labeled=labeled, total=total)
        ds_item = self._find_dataset_item(project_name, dataset_name)
        if ds_item is not None:
            container = self.project_tree.itemWidget(ds_item, 0)
            if container is not None:
                pl = container.findChild(QLabel, "datasetRowProgress")
                if pl is not None:
                    pl.setText("{}/{}".format(labeled, total))

    def _refresh_dataset_row_progress(self, project_name, dataset_name):
        """根据 db 当前 binding 刷新项目树该数据集节点的进度文本。"""
        ds_item = self._find_dataset_item(project_name, dataset_name)
        if ds_item is None:
            return
        container = self.project_tree.itemWidget(ds_item, 0)
        if container is None:
            return
        pl = container.findChild(QLabel, "datasetRowProgress")
        if pl is None:
            return
        binding = self.db.get_dataset_import(project_name, dataset_name)
        total = binding.get("total", 0) or 0
        labeled = binding.get("labeled", 0) or 0
        pl.setText("{}/{}".format(labeled, total))

    @staticmethod
    def _has_label_file(image_path):
        """判断图像同路径是否存在同名 labelme json。"""
        base, _ = os.path.splitext(image_path)
        return os.path.exists(base + ".json")

    def _delete_selected_images(self, items):
        """
        删除所选图像：可选删除本地文件 / 仅标记不加载(db 记录,下次加载跳过)。
        同时从内存缓存移除并刷新显示区与总数。
        """
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds or not items:
            return
        proj, ds = cur_ds
        paths = [it.image_path for it in items if it.image_path]
        if not paths:
            return
        clicked = MessageBox.choose(
            self, "删除图像", "是否删除所选 {} 张图像？".format(len(paths)),
            [("删除本地文件", QMessageBox.YesRole),
             ("仅标记不加载", QMessageBox.NoRole),
             ("取消", QMessageBox.RejectRole)],
            informative="删除本地文件：图像文件将从磁盘删除，不可恢复\n"
                        "仅标记不加载：保留文件，但下次加载数据集时自动跳过")
        if clicked is None or clicked == "取消":
            return
        delete_local = (clicked == "删除本地文件")
        norm = lambda p: os.path.normcase(os.path.normpath(p))
        norm_set = {norm(p) for p in paths}
        deleted_local = 0
        for p in paths:
            if delete_local:
                for fp in (p, os.path.splitext(p)[0] + ".json"):
                    try:
                        if os.path.exists(fp):
                            os.remove(fp)
                            deleted_local += 1
                    except OSError:
                        pass
            else:
                self.db.add_deleted_image(proj, ds, p)
        # 从内存缓存移除图像及其标注
        index = self.dataset_cache.get(proj, {}).get(ds)
        if index:
            index["all"] = [r for r in index["all"]
                            if norm(r.get("image_path", "")) not in norm_set]
            for lbl in list(index["labels"]):
                index["labels"][lbl] = [r for r in index["labels"][lbl]
                                        if norm(r.get("image_path", "")) not in norm_set]
                if not index["labels"][lbl]:
                    del index["labels"][lbl]

        # 日志
        self._write_log("删除图像: {} 张 | 方式={} | 本地删除文件={} | 项目={}, 数据集={}".format(
            len(paths), "删除本地文件" if delete_local else "仅标记不加载",
            deleted_local, proj, ds))

        # 刷新显示区(总数/分页同步更新) + 标注进度
        self.show_dataset_images(proj, ds)
        self._refresh_annotation_progress(proj, ds)

    @staticmethod
    def _write_log(msg):
        """记录操作日志到 logs/app.log"""
        write_log(msg)

    def _log(self, msg):
        """写日志"""
        self._write_log(msg)

    def _on_log_clicked(self):
        """显示常驻日志对话框(启动时已创建并注册，隐藏也接收日志)。"""
        dlg = getattr(self, "_log_dialog", None)
        if dlg is None:
            self._log_dialog = LogDialog(self)
            dlg = self._log_dialog
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    def _on_model_clicked(self):
        # 独立入口:显示全部训练/模型记录(不做项目/数据集筛选)
        md = ModelDialog(app=self, project="", dataset="", parent=self)
        md.exec()
        md.deleteLater()

    # ---------------- 训练进度条(首页标题栏)----------------
    def _show_train_task(self, task_name, value=0):
        """训练开始时显示: 任务名 + 进度条 + 剩余时间 + 显存"""
        self.task_name_label.setText(task_name)
        self.train_progress.setValue(max(0, min(100, int(value))))
        self.task_name_label.show()
        self.train_progress.show()
        self.time_count_label.show()
        self.time_count_edit.show()
        self.gpu_memory_label.show()
        self.gpu_memory_use_btn.show()
        if not self._gpu_timer.isActive():
            self._refresh_gpu_memory()
            self._gpu_timer.start()
        if not self._eta_timer.isActive():
            self._eta_timer.start()

    def _set_train_progress(self, value):
        """更新训练进度(0-100)。"""
        self.train_progress.setValue(max(0, min(100, int(value))))

    def _apply_progress_format(self):
        """进度条文本:`30% | 0.556` 进度 | 精度 """
        m = self._latest_map50
        tail = "{:.3f}".format(m) if m is not None else "--"
        self.train_progress.setFormat("%p% | " + tail)

    def _hide_train_task(self):
        """训练结束/无训练任务时隐藏。"""
        self.task_name_label.hide()
        self.train_progress.hide()
        self.stop_train_btn.hide()
        self.time_count_label.hide()
        self.time_count_edit.hide()
        self._eta_timer.stop()
        self._eta_remain = 0
        self._eta_total_epochs = 0

    def _update_eta(self, epoch, total):
        """progress到达时按已用时长外推剩余秒数(epoch 从 1 起,首 epoch 内无数据跳过)。"""
        if not total or epoch <= 0 or not self._train_start_ts:
            return
        elapsed = time.time() - self._train_start_ts
        if elapsed <= 0:
            return
        avg = elapsed / epoch          # 每 epoch 平均耗时
        self._eta_remain = max(0, int(avg * (total - epoch)))
        self._show_eta()

    def _update_test_eta(self, done, total):
        """测试进度推进时按已用时长外推剩余秒数（首次调用记录开始时间）。"""
        if not total:
            return
        if not self._test_start_ts:
            self._test_start_ts = time.time()
        if done <= 0:
            return
        elapsed = time.time() - self._test_start_ts
        if elapsed <= 0:
            return
        avg = elapsed / done           # 每张图平均耗时
        self._eta_remain = max(0, int(avg * (total - done)))
        self._show_eta()

    def _eta_tick(self):
        """每秒递减剩余秒数,实现持续倒计时(训练推进时由 _update_eta 重估校准)。"""
        if self._eta_remain > 0:
            self._eta_remain -= 1
        self._show_eta()

    def _show_eta(self):
        h, remain = divmod(self._eta_remain, 3600)
        m, s = divmod(remain, 60)
        self.time_count_edit.setTime(QTime(h, m, s))

    def _refresh_gpu_memory(self):
        """2s定时:查询显存使用率,>55% 显示红色"""
        usage = None
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.used,memory.total",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=3)
            used, total = [x.strip() for x in out.stdout.strip().split(",")]
            usage = int(used) * 100.0 / int(total) if int(total) else 0.0
        except Exception:
            pass
        if usage is None:
            self.gpu_memory_use_btn.setText("N/A")
            self.gpu_memory_use_btn.setStyleSheet(self._gpu_btn_style(False))
            return
        self.gpu_memory_use_btn.setText("{:.0f}%".format(usage))
        self.gpu_memory_use_btn.setStyleSheet(
            self._gpu_btn_style(usage > 55))

    @staticmethod
    def _gpu_btn_style(high):
        """显存按钮配色:超 55% 深红发黑"""
        color = "#7a1515" if high else "#2e9e5b"
        hover = "#8f1c1c" if high else "#37b06a"
        return (
            "QPushButton {{ background-color: {}; color: white;"
            " border: none; border-radius: 6px; padding: 4px 12px;"
            " font-size: 12px; font-weight: 600; }}"
            "QPushButton:hover {{ background-color: {}; }}").format(color, hover)

    # ---------------- 全局训练管理(唯一训练实例 + 首页停止按钮)----------------
    def is_training(self):
        return (self._train_worker is not None
                and self._train_worker.isRunning())

    def start_training(self, config, record_id):
        if self.is_training():
            return False
        self._training_record_id = record_id
        self._train_worker = TrainWorker(config, self)
        self._train_worker.progress.connect(self._on_train_progress)
        self._train_worker.metrics.connect(self._on_train_metrics)
        self._train_worker.finished_ok.connect(self._on_train_done)
        self._train_worker.failed.connect(self._on_train_failed)
        self._train_worker.log.connect(self._on_train_log)
        self._show_train_task("{} 训练中 0/{}".format(
            config["project"], config["epochs"]), 0)
        self._train_start_ts = time.time()
        self._eta_total_epochs = int(config.get("epochs", 0))
        self._latest_map50 = None
        self._apply_progress_format()
        if self._eta_total_epochs > 0:
            self._eta_remain = self._eta_total_epochs * 300
            self._show_eta()
        self.stop_train_btn.show()
        self._train_worker.start()
        return True

    def stop_training(self, confirm=True):
        if confirm and not MessageBox.question(self, "停止训练", "确定要停止当前训练吗？"):
            return
        w = self._train_worker
        if w is not None:
            w.stop()
            w.wait(3000)
            self._train_worker = None
            self._log("手动停止训练: {}".format(self._training_record_id))
        self._hide_train_task()
        rid = self._training_record_id
        self._training_record_id = None
        if rid:
            self.on_train_finished(rid, None)

    def _on_train_progress(self, epoch, total):
        # 停止/结束后兜底：子进程被 kill 残留 stdout 的 EPOCH 行可能在
        # _hide_train_task 之后才进事件队列；此时 worker 已为 None，忽略。
        if self._train_worker is None or self._training_record_id is None:
            return
        project = self._train_worker._config.get("project", "") if self._train_worker else ""
        self._show_train_task("{} 训练中 {}/{}".format(project, epoch, total),
                              epoch * 100.0 / total if total else 0)
        self._update_eta(epoch, total)

    def _on_train_metrics(self, metrics):
        try:
            write_log("_on_train_metrics 收到: rid={} epochs={} per_class_keys={}".format(
                (self._training_record_id or "")[:8], metrics.get("epochs"),
                list(metrics.get("per_class", {}).keys())))
        except Exception:
            pass
        # 同步最新指标到进度条文本(分类->精度, 检测/分割→mAP@50)
        s = metrics.get("series", {})
        if s.get("accuracy"):
            self._latest_map50 = float(s["accuracy"][-1])
            self._apply_progress_format()
        elif s.get("mAP@50"):
            self._latest_map50 = float(s["mAP@50"][-1])
            self._apply_progress_format()
        if self._training_record_id:
            self.update_train_metrics(self._training_record_id, metrics)

    def _on_train_done(self, result):
        rid = self._training_record_id
        self._hide_train_task()
        self._train_worker = None
        if rid:
            self.on_train_finished(rid, result)

            def _clear():
                if self._training_record_id == rid:
                    self._training_record_id = None
            QTimer.singleShot(0, _clear)
        else:
            self._training_record_id = None

    def _on_train_failed(self, detail):
        rid = self._training_record_id
        self._hide_train_task()
        self._training_record_id = None
        self._train_worker = None
        if rid:
            self.on_train_finished(rid, None)
        for line in detail.splitlines():
            self._log("[train] " + line)
        MessageBox.critical(self, "训练失败", "训练过程中发生错误，Err：\n\n{}".format(detail))

    def _on_train_log(self, line):
        self._log("[train] " + line)

    def on_train_progress(self, project, datasets, epoch, total):
        self._show_train_task("{} / {} 训练中 {}/{}".format(
            project, datasets, epoch, total),
            epoch * 100.0 / total if total else 0)

    def update_train_metrics(self, record_id, metrics):
        for r in self.db.get_train_records():
            if r.get("id") == record_id:
                r["metrics"] = metrics
                s = metrics.get("series", {})
                if s.get("mAP@50"):
                    r["map50"] = "{:.3f}".format(float(s["mAP@50"][-1]))
                if s.get("accuracy"):
                    r["accuracy"] = "{:.4f}".format(float(s["accuracy"][-1]))
                self.db.update_train_record(r)
                write_log("更新训练指标: record={} epochs={} mAP@50={} map50={} acc={} per_class={}".format(
                    record_id[:8], metrics.get("epochs"),
                    s.get("mAP@50"), r.get("map50"), r.get("accuracy"),
                    list(metrics.get("per_class", {}).keys())))
                return

    def on_train_finished(self, record_id, result):
        self._hide_train_task()
        recs = self.db.get_train_records()
        for r in recs:
            if r.get("id") == record_id:
                r["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    t0 = datetime.strptime(r.get("start_time", ""), "%Y-%m-%d %H:%M:%S")
                    t1 = datetime.strptime(r["end_time"], "%Y-%m-%d %H:%M:%S")
                    secs = int((t1 - t0).total_seconds())
                    r["duration"] = _fmt_duration(int((t1 - t0).total_seconds()))
                except Exception:
                    pass
                if result:
                    if result.get("map50"):
                        r["map50"] = "{:.3f}".format(float(result["map50"]))
                    if result.get("accuracy"):
                        r["accuracy"] = "{:.4f}".format(float(result["accuracy"]))
                    if result.get("model_path"):
                        r["model_path"] = result["model_path"]
                else:
                    r["status"] = "失败/已停止"
                self.db.update_train_record(r)
                if result and result.get("model_path"):
                    self._save_model_record(r)
                break

    def _save_model_record(self, train_record):
        """把训练记录副本写入 model_history(独立 id,幂等,删除不影响训练参数)。"""
        rid = train_record.get("id")
        for m in self.db.get_model_records():
            if m.get("train_id") == rid:
                return
        rec = dict(train_record)
        rec["id"] = str(uuid.uuid4())
        rec["train_id"] = rid
        self.db.add_model_record(rec)
        write_log("已保存模型记录: {} | {}".format(
            rec.get("model_path", ""), rec.get("dataset_info", "")))

    def show_ui(self):
        self.showMaximized()


if __name__ == "__main__":
    setup_matplotlib_chinese()
    myapp = QApplication(sys.argv)
    myapp.setStyleSheet(load_style_sheet())
    ui = App()
    ui.show_ui()
    sys.exit(myapp.exec())
