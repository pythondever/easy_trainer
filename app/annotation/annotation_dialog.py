# -*- coding: utf-8 -*-
"""
标注对话框: 主类骨架 + 左右两侧列表(标签列表 / 标注信息).
画布与绘制交互见 annotation_canvas, 数据读写见 annotation_io.
- 矩形/多边形标注(颜色 = 标签颜色, 支持中文标签)
- 左侧标签列表(点击切换当前标签), 添加标签弹窗(10 默认色 + 自定义色 + 跨数据集导入)
- A/D 切换上一张/下一张, 切换/关闭时保存 labelme json(图像同路径)
"""
import os
import re
import shutil
from functools import lru_cache
from PySide6.QtCore import Qt, QTimer, QSize, QEvent, QRegularExpression
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import (QColor, QPixmap, QKeySequence, QShortcut,
                           QPainter, QIcon, QCursor, QIntValidator,
                           QDoubleValidator, QRegularExpressionValidator)
from PySide6.QtWidgets import (QDialog, QWidget, QApplication, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QFrame, QMenu)

from ui.annotation import Ui_annotationDialog as AnnotationUI
from ui.add_label import Ui_addLabelDialog as AddLabelUI

from app.annotation.annotation_canvas import (ANGLE_RANGE_DEFAULT,
                                              AnnotationCanvasMixin,
                                              BLEND_STRENGTH_DEFAULT,
                                              BRIGHTNESS_DEFAULT,
                                              ColorPickerDialog,
                                              FILL_COLOR_DEFAULT,
                                              FILL_COLOR_PRESETS,
                                              SwitchButton, _fill_dot_qss,
                                              _resource_path,
                                              _upgrade_graphics_view)
from app.annotation.annotation_io import AnnotationIOMixin, _PrefetchWorker
from app.core import name_rules, theme
from app.annotation.box_item import (AnnotationBoxItem, LABEL_COLORS,
                                     assign_label_color, label_color)
from app.core.label_utils import (label_sort_key, normalize_label,
                                  text_label)
from app.widgets.dialog_buttons import (add_ok_cancel, apply_icon,
                                        _icon_path, _tinted)
from app.widgets.message_box import MessageBox
from app.core.log import write_log


# 左右两个列表行的高亮底色(左侧标签列表 / 右侧标注列表同款)
ROW_BG_SELECTED = "#2a3f6b"
ROW_BG_NORMAL = theme.hexof("bg_control")
_ROW_QSS = "QFrame {{ background: {0}; border-radius: 6px; }}"

# 像素精度(mm/像素)
_PX_SCALE = None


def _fmt_area_mm2(v):
    """小数位随量级走: 0.05mm/px 下一块杂质可能只有零点几 mm²."""
    if v >= 1000:
        return "{:,}".format(int(round(v)))
    if v >= 100:
        txt = "{:.1f}".format(v)
    elif v >= 1:
        txt = "{:.2f}".format(v)
    else:
        txt = "{:.3f}".format(v)
    return txt.rstrip("0").rstrip(".") if "." in txt else txt


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


class _PixelScaleDialog(QDialog):
    """像素精度输入: 1 像素 = ? mm(mm/px)."""

    def __init__(self, current=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("像素精度"))
        self._value = 1.0 if current is None else float(current)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.addWidget(QLabel(self.tr("1 像素代表的实际长度")))
        row = QHBoxLayout()
        row.setSpacing(8)
        self._edit = QLineEdit()
        self._edit.setFixedWidth(120)
        self._edit.setAlignment(Qt.AlignCenter)
        self._edit.setValidator(QDoubleValidator(0.0, 1e6, 6, self))
        self._edit.setText("{:g}".format(self._value))
        row.addWidget(self._edit)
        row.addWidget(QLabel("mm / px"))
        row.addStretch(1)
        layout.addLayout(row)
        self._hint = QLabel("")
        self._hint.setStyleSheet("color: #e5677a; font-size: 12px;")
        layout.addWidget(self._hint)
        btns = QHBoxLayout()
        btns.addStretch(1)
        add_ok_cancel(btns, self._try_accept, self.reject)
        layout.addLayout(btns)

        self._edit.textChanged.connect(lambda _="": self._hint.setText(""))

    def showEvent(self, event):
        super().showEvent(event)
        self._edit.setFocus()
        self._edit.selectAll()

    def _try_accept(self):
        try:
            v = float(self._edit.text().strip())
        except ValueError:
            v = 0.0
        if v <= 0:
            self._hint.setText(self.tr("请输入大于 0 的数字"))
            return
        self._value = v
        self.accept()

    def value(self):
        return self._value


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
        self._edit_mode = False       # 编辑已有标签: 整段名称当一项, 不按逗号拆
        self._setup()
        if preset_name:
            self.ui.input_label_name_txt.setText(preset_name)
        if preset_color:
            self._select_color(preset_color)
        if edit_mode:
            # 编辑已有标签: 名称与颜色都可改; 跨数据集导入与编辑无关, 一并锁掉.
            # 名称里的逗号会撑坏 data.yaml 的类别列表, 置校验器直接禁掉输入
            self._edit_mode = True
            self.setWindowTitle(self.tr("编辑标签"))
            self.ui.input_label_name_txt.setPlaceholderText(
                self.tr("标签名称"))
            self.ui.input_label_name_txt.setValidator(
                QRegularExpressionValidator(QRegularExpression("[^,，]*"), self))
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
            "QPushButton {{ background-color: {ctl}; border: 2px solid {bd};{0} }}"
            "QPushButton:hover {{ border-color: {ac}; }}".format(
                CIRCLE_CSS, ctl=theme.hexof("bg_control_2"),
                bd=theme.hexof("border_strong"), ac=theme.hexof("accent")))
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
        color = ColorPickerDialog.get_color(QColor(self._selected_color or theme.hexof("accent")), self)
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
        if self._edit_mode:
            # 编辑单个已有标签: 整段就是名称(输入框已禁逗号), 不做批量拆分
            return [(text, self._selected_color
                     or assign_label_color(text, set()))]
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


class AnnotationDialog(QDialog, AnnotationCanvasMixin, AnnotationIOMixin):
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
        # "文本标注"开关(OCR): 打开后免建标签直接拉框, 类别是保留标签
        self.text_mode = False
        self._label_before_text_mode = ""
        self._cls_changes = []
        self._label_files_touched = False   # 本会话改过标签文件(删除/改名)
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
        u.px_scale_btn.setCursor(Qt.PointingHandCursor)
        u.px_scale_btn.clicked.connect(self._edit_px_scale)
        self._sync_px_scale_btn()
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
        u.text_switch = SwitchButton(self)
        u.text_switch.setObjectName("textSwitchButton")
        u.text_switch.setChecked(False)
        u.text_switch.toggled.connect(self._toggle_text_mode)
        u.text_switch_label = QLabel(self.tr("文本标注"), self)
        u.text_switch_label.setObjectName("text_switch_label")
        # 参数收进"设置"弹层后, 工具条右侧只剩两个开关和设置按钮
        idx = u.horizontalLayout.indexOf(u.settings_btn)
        u.horizontalLayout.insertWidget(idx, u.switchButton)
        u.horizontalLayout.insertWidget(idx + 1, u.show_boxes_label)
        u.horizontalLayout.insertSpacing(idx + 2, 10)
        u.horizontalLayout.insertWidget(idx + 3, u.text_switch)
        u.horizontalLayout.insertWidget(idx + 4, u.text_switch_label)
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
        self.scene.box_edit_requested.connect(self._on_box_edit_requested)
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

    def eventFilter(self, obj, event):
        # 弹层不在布局里, 收不到"点了别处"的信号, 只能全局盯鼠标按下.
        # 按坐标判落点而不是看 obj: QLabel 不吃鼠标事件, 会一路冒泡到 dialog 再进来
        # Qt 偶发把非 QEvent 的对象当 event 投过来, 透传给 super() 会踩 shiboken
        # 的实参校验抛 TypeError, 这个异常在事件分发里没人接, 直接掀掉进程
        if not isinstance(event, QEvent):
            return False
        if (event.type() == QEvent.Type.MouseButtonPress
                and not self.ui.paramsPanel.isHidden()
                and isinstance(obj, QWidget) and obj.window() is self
                and not self._hit_params_area(event.globalPosition().toPoint())):
            self._hide_params_panel()
        return False

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("A"), self, activated=lambda: self._switch(-1))
        QShortcut(QKeySequence("D"), self, activated=lambda: self._switch(1))
        QShortcut(QKeySequence("Delete"), self, activated=self.scene.delete_selected)
        QShortcut(QKeySequence("Ctrl+S"), self,
                  activated=lambda: self._save_current(commit_pending=True))
        QShortcut(QKeySequence("Ctrl+Z"), self, activated=self._undo_fp_paste)
        QShortcut(QKeySequence(Qt.Key_Escape), self, activated=self._cancel_draw_mode)

    def closeEvent(self, event):
        self._save_current(commit_pending=True)
        self._closing = True
        QApplication.instance().removeEventFilter(self)
        if getattr(self, "_prefetch_worker", None) is not None:
            self._prefetch_worker.stop()
            self._prefetch_worker.wait(2000)
        QApplication.restoreOverrideCursor()
        super().closeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        # QDialog 首次显示后置最大化(exec 前设置不生效)
        if not getattr(self, "_maximized_once", False):
            self._maximized_once = True
            self.setWindowState(Qt.WindowMaximized)

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
        if self.text_mode:
            # 文本标注的类别是保留标签, 与数据集有没有自建标签无关
            self.scene.current_label = text_label()
        if not self.label_colors:
            self.scene.current_label = "" if not self.text_mode else text_label()
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
                "QPushButton {{ background-color: {0}; border: 1px solid {bd};"
                " border-radius: 9px; padding: 0px; margin: 0px;"
                " min-width: 0px; max-width: 18px; min-height: 0px; max-height: 18px; }}".format(
                    color, bd=theme.hexof("border_strong")))
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
                "QPushButton:hover { background: " + theme.hexof("bg_hover") + "; }")
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
        """编辑标签: 名称与颜色一起改, 改名由主窗口链路同步改写标签文件."""
        dlg = AddLabelDialog(self, preset_name=name,
                             preset_color=self.label_colors.get(name, ""),
                             db=self.db, project=self.project,
                             dataset=self.dataset, edit_mode=True)
        if dlg.exec() != QDialog.Accepted:
            return
        items = dlg.result_data()
        if not items:
            MessageBox.warning(self, self.tr("编辑标签"),
                               self.tr("标签名称不能为空"))
            return
        new_name, new_color = items[0]
        if new_name != name:
            if not self._main.rename_label(self.project, self.dataset, name,
                                           new_name, parent=self):
                return
            self._rename_label_in_scene(name, new_name)
            name = new_name
            self._label_files_touched = True
            self._refresh_labels()
        if new_color and new_color != self.label_colors.get(name):
            self.db.add_dataset_label(self.project, self.dataset, name, new_color)
            self.label_colors[name] = new_color
            self.scene.label_colors[name] = QColor(new_color)
            # 框颜色是 paint 时动态查 scene.label_colors, 重绘即可生效(A/D 翻页同源)
            self.scene.update()
            self._refresh_labels()
            write_log("修改标签颜色: {} → {} ({}/{})".format(
                name, new_color, self.project, self.dataset))
        self._refresh_labeled_list()

    def _rename_label_in_scene(self, old_name, new_name):
        """场景内该标签的框改挂新名; 名称是 paint 时读的, 重绘即可生效."""
        for item in self.scene.all_items():
            if getattr(item, "label", None) == old_name:
                item.label = new_name
        self.scene.label_colors.pop(old_name, None)
        if self.scene.current_label == old_name:
            self.scene.current_label = new_name
        self.scene.update()

    def _delete_label_from_list(self, name):
        """
        删除标签并同步清理其标注: 标签文件 / db / 缓存索引 / 当前场景.
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
        # 文件层交给主窗口那条链路(后台上线): 图像同路径 json 与导入的 YOLO
        # txt 一并改写, 同时清缓存索引 / db / class_id 映射, 改完自己刷新首页视图
        self._label_files_touched = True
        self._main._apply_delete_label(self.project, self.dataset, name)
        for item in scene_items:
            self.scene.delete_item(item)
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
        for _name, _color in items:
            err = name_rules.check_label_name(_name)
            if err:
                MessageBox.warning(self, self.tr("添加标签"), err)
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
                area_text = self._area_text((x2 - x1) * (y2 - y1))
            else:  # AnnotationPolygonItem
                pts = item.points()
                kind = self.tr("多边形")
                size_text = self.tr("{} 个顶点").format(len(pts))
                area_text = self._area_text(area) if area else "-"
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

    def _area_text(self, px_area):
        """像素面积; 设过像素精度就在后面补一段物理面积."""
        txt = "{:,} px²".format(int(round(px_area)))
        if _PX_SCALE:
            txt += " · {} mm²".format(_fmt_area_mm2(px_area * _PX_SCALE ** 2))
        return txt

    def _sync_px_scale_btn(self):
        btn = self.ui.px_scale_btn
        icon = _resource_path("编辑.png")
        if icon:
            btn.setIcon(_tinted(icon, "#b8c0d0"))
            btn.setIconSize(QSize(13, 13))
        if _PX_SCALE is None:
            btn.setText(self.tr("转换"))
            btn.setToolTip(self.tr("设置像素精度, 在像素面积后显示物理面积"))
        else:
            txt = "{:g} mm/px".format(_PX_SCALE)
            btn.setText(txt)
            btn.setToolTip(self.tr("当前像素精度 {}, 点击修改").format(txt))
        btn.setProperty("pxScaleSet", "true" if _PX_SCALE is not None else "false")
        btn.style().unpolish(btn)
        btn.style().polish(btn)

    def _edit_px_scale(self):
        global _PX_SCALE
        dlg = _PixelScaleDialog(_PX_SCALE, self)
        if dlg.exec() != QDialog.Accepted:
            return
        _PX_SCALE = dlg.value()
        self._sync_px_scale_btn()
        self._refresh_labeled_list()



