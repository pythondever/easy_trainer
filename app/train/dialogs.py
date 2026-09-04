# -*- coding: utf-8 -*-
"""训练对话框(统一):任务类型下拉 检测/分割/分类,数据集跨项目选择。"""

import os
import json
import traceback
import uuid
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QEvent, QObject
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import (QDialog, QLabel, QFileDialog, QComboBox,
                               QPushButton, QVBoxLayout)
from PySide6.QtGui import QStandardItem

from app.widgets.dialog_buttons import apply_icon
from app.widgets.message_box import MessageBox
from app.core.log import write_log
from app.train.data_prep import timestamp_dir
from ui.train import Ui_TrainDialog

try:
    import torch
except ImportError:
    torch = None

# 弹窗输入类控件统一高度，与 style.qss 的 QDialog 规则（36）保持一致
CONTROL_H = 36


class _TrainStartDialog(QDialog):
    """训练/测试启动提示：确认按钮带倒计时，5s 后自动确认；手动点击立即确认并停止计时。"""

    def __init__(self, seconds=5, parent=None, title="训练即将开始",
                 message="训练即将开始"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self._left = seconds
        self.setMinimumWidth(280)
        layout = QVBoxLayout(self)
        label = QLabel(message)
        label.setObjectName("dialogConfirmPrompt")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self._btn = QPushButton("确认({})".format(seconds))
        self._btn.clicked.connect(self._confirm)
        layout.addWidget(self._btn)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)

    def _tick(self):
        self._left -= 1
        if self._left <= 0:
            self._timer.stop()
            self.accept()
        else:
            self._btn.setText("确认({})".format(self._left))

    def _confirm(self):
        self._timer.stop()
        self.accept()

    def closeEvent(self, event):
        self._timer.stop()
        super().closeEvent(event)


class _ClickToPopupFilter(QObject):
    """事件过滤器：点击下拉框（或其 lineEdit）任意位置 → 展开下拉。"""

    def __init__(self, combo, parent=None):
        super().__init__(parent)
        self._combo = combo

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            QTimer.singleShot(0, self._combo.showPopup)
            return True
        return False


def _available_devices():
    """[(显示名, 设备串)]：列表显示 GPU 型号，实际下发的是 cuda:0 这类设备串。"""
    if torch is None or not torch.cuda.is_available():
        return [("CPU", "CPU")]
    out = []
    for i in range(torch.cuda.device_count()):
        try:
            name = torch.cuda.get_device_name(i)
            total = torch.cuda.get_device_properties(i).total_memory
            text = "{} ({:.0f} GB)".format(name, total / 1024 ** 3)
        except Exception:
            text = "GPU {}".format(i)
        out.append((text, "cuda:{}".format(i)))
    out.append(("CPU", "CPU"))
    return out


class TrainDialog(QDialog):
    """统一训练对话框：任务类型(检测/分割/分类) + 跨项目数据集选择。"""

    TASK_TEXT = {"检测": "detect", "分割": "segment", "分类": "classify"}
    # 各任务默认参数:epochs / lr / img_size / grad_accum(分类禁用)
    TASK_DEFAULTS = {
        "detect": (100, 1e-4, 640, 4),
        "segment": (100, 1e-4, 636, 4),
        "classify": (30, 0.001, 224, 4),
    }
    TASK_TIPS = {
        "detect": "目标检测推荐图像尺寸：640（可设为 32 的倍数如 640/672）",
        "segment": "图像分割推荐尺寸：636（必须为 12 的倍数，如 636/648/660）",
        "classify": "图像分类推荐尺寸：224（小图用 224，较大图可到 256）",
    }
    # 输入框右侧的倍数约束，写不下整句 tooltip 就靠这几个字
    IMG_NOTE = {"detect": "32 的倍数", "segment": "12 的倍数",
                "classify": "建议 224"}

    def __init__(self, app, project="", dataset="", preset_record=None):
        """project/dataset 可为空(独立入口);preset_record 传入时按记录回填(模型界面训练按钮)。"""
        super().__init__(app)
        self.app = app
        self.project = project
        self.dataset = dataset
        self.ui = None
        self._int_fields = []      # [(控件, 名称, 默认值, 是否必填)]
        self._float_fields = []    # [(控件, 名称, 默认值, 是否必填)]
        self._combo_filters = []
        self._preset_record = preset_record
        self._last_epochs_default = None
        self._last_lr_default = None
        self._last_img_default = None
        self._build()

    def closeEvent(self, event):
        super().closeEvent(event)

    # ---------- 初始化 ----------
    def _build(self):
        self.ui = Ui_TrainDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("训练")
        self._define_fields()
        self._setup_validators()
        self._fill_defaults()
        self._fix_heights()
        self._connect()
        self.resize(740, max(560, self.sizeHint().height()))

    def _task(self):
        """当前任务类型文本:detect/segment/classify。"""
        return self.TASK_TEXT.get(self.ui.task_combo.currentText(), "detect")

    def _task_text(self):
        return self.ui.task_combo.currentText()

    def _fix_heights(self):
        """统一控件高度（宽度交给网格拉伸），数值输入框文字居中。"""
        for edit, _n, _d, _r in self._int_fields + self._float_fields:
            try:
                edit.setFixedHeight(CONTROL_H)
                edit.setAlignment(Qt.AlignHCenter)
            except Exception:
                pass
        out_edit = getattr(self.ui, "output_line_txt", None)
        if out_edit is not None:
            out_edit.setFixedHeight(CONTROL_H)
            out_edit.setAlignment(Qt.AlignHCenter)
            # 只读:路径只能通过"选择路径"按钮填入;悬停显示完整路径
            out_edit.setReadOnly(True)
            out_edit.setToolTip(out_edit.text())
            out_edit.textChanged.connect(
                lambda t: out_edit.setToolTip(t))
        for combo_name in ("task_combo", "dataset_combo", "val_combo", "network_combo",
                           "device_combo", "img_size_comboBox",
                           "optimizer_comboBox"):
            combo = getattr(self.ui, combo_name, None)
            if combo is not None:
                combo.setFixedHeight(CONTROL_H)
        # 下拉的 sizeHint 按最长条目算，GPU 全名会把整列撑宽，改成按固定字符数估宽
        for name in ("dataset_combo", "val_combo", "device_combo"):
            combo = getattr(self.ui, name, None)
            if combo is not None:
                combo.setSizeAdjustPolicy(
                    QComboBox.SizeAdjustPolicy
                    .AdjustToMinimumContentsLengthWithIcon)
                combo.setMinimumContentsLength(12)
        self._align_grid_labels()

    def _align_grid_labels(self):
        """网格的左右两组标签列各自同宽，否则两侧输入框左边界对不齐。"""
        for grid_name in ("grid_data", "grid_hyper"):
            grid = getattr(self.ui, grid_name, None)
            if grid is None:
                continue
            for col in (0, 2):
                labels = []
                for row in range(grid.rowCount()):
                    item = grid.itemAtPosition(row, col)
                    w = item.widget() if item is not None else None
                    if isinstance(w, QLabel):
                        labels.append(w)
                if not labels:
                    continue
                width = max(lbl.sizeHint().width() for lbl in labels)
                for lbl in labels:
                    lbl.setMinimumWidth(width)

    def _define_fields(self):
        self._int_fields = [
            (self.ui.batch_size_line_txt, "批次", 4, True),
            (self.ui.grad_accum_line_txt, "梯度累积", 4, True),
            (self.ui.epochs_line_txt, "轮次", 100, True),
            (self.ui.batch_size_line_txt_2, "线程数", 4, True),
            (self.ui.img_size_line_txt, "图像尺寸", 640, True),
            (self.ui.early_stop_line_txt, "早停", 20, False),
        ]
        self._float_fields = [
            (self.ui.lr_line_txt, "学习率", 1e-4, True),
        ]

    def _connect(self):
        self.ui.start_train.clicked.connect(self._on_start_train)
        self.ui.select_output_path_btn.clicked.connect(self._select_output_dir)
        apply_icon(self.ui.cancel_btn, "取消")
        self.ui.cancel_btn.clicked.connect(self.reject)

    # ---------- 填充 ----------
    def _style_combo(self, combo):
        """
        下拉框文本居中 + 点击框内任意位置打开下拉。
        """
        combo.setEditable(True)
        combo.setFocusPolicy(Qt.StrongFocus)
        le = combo.lineEdit()
        le.setObjectName("multiComboLineEdit")
        le.setReadOnly(True)
        le.setAlignment(Qt.AlignHCenter)
        f = _ClickToPopupFilter(combo)
        combo.installEventFilter(f)
        le.installEventFilter(f)
        self._combo_filters.append(f)

    def _style_all_combos(self):
        for name in ("task_combo", "dataset_combo", "val_combo", "network_combo",
                     "device_combo", "img_size_comboBox", "optimizer_comboBox"):
            combo = getattr(self.ui, name, None)
            if combo is not None:
                self._style_combo(combo)

    def _setup_multi_combo(self, combo, placeholder="请选择数据集"):
        """
        多选下拉
        """
        combo.model().itemChanged.connect(lambda *_: self._update_multi_label(combo))
        combo.activated.connect(lambda _i: self._update_multi_label(combo))
        return combo

    def _fill_dataset_multi(self, combo, checked_names):
        """
        跨项目列出所有数据集(文本"项目/数据集",data=(项目,数据集)),checked_names 内默认勾选。
        数据源与首页项目树一致:先 get_projects() 拿项目名,再 get_datasets(name)
        拿该项目下数据集——不会列出已删除项目残留的孤儿数据集记录。
        """
        model = combo.model()
        model.clear()
        for proj in self.app.db.get_projects():
            for ds_info in self.app.db.get_datasets(proj):
                ds = str(ds_info.get("dataset_name", "") or "")
                if not ds:
                    continue
                text = "{}/{}".format(proj, ds)
                item = QStandardItem(text)
                item.setData((proj, ds), Qt.UserRole)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                item.setCheckState(
                    Qt.Checked if text in checked_names else Qt.Unchecked)
                model.appendRow(item)
        self._update_multi_label(combo)

    def _selected_checked(self, combo):
        model = combo.model()
        out = []
        for i in range(model.rowCount()):
            item = model.item(i)
            if item.checkState() == Qt.Checked:
                data = item.data(Qt.UserRole)
                if isinstance(data, tuple) and len(data) == 2:
                    out.append(data)
                else:
                    out.append((self.project, item.text()))
        return out

    def _update_multi_label(self, combo, *_):
        checked = self._selected_checked(combo)
        texts = []
        for c in checked:
            if isinstance(c, tuple):
                texts.append("{}/{}".format(c[0], c[1]))
            else:
                texts.append(str(c))
        combo.setEditText(", ".join(texts))
        combo.setToolTip("\n".join(texts) if texts else "")
        if not texts:
            combo.setCurrentIndex(-1)
        self._update_summary()

    def _update_summary(self):
        """底部概要条：勾了几个训练集/验证集、总共多少张图、能不能直接开训。"""
        train = self._selected_datasets()
        val = self._selected_val_datasets()
        if not train:
            self.ui.summary_text.setText("请选择训练集与验证集")
            return
        total = 0
        labeled = 0
        for proj, name in train + val:
            info = self.app.db.get_dataset_import(proj, name) or {}
            total += int(info.get("total") or 0)
            if int(info.get("labeled") or 0) > 0:
                labeled += 1
        picked = len(train) + len(val)
        text = "训练集 {} 个 · 验证集 {} 个 · 共 {} 张图".format(
            len(train), len(val), total)
        if not val:
            tail = "未选择验证集"
        elif labeled == picked:
            tail = "已标注，可直接训练"
        else:
            tail = "有 {} 个数据集尚未标注".format(picked - labeled)
        self.ui.summary_text.setText("{} · {}".format(text, tail))

    def _selected_datasets(self):
        """训练集（勾选的数据集）。"""
        return self._selected_checked(self.ui.dataset_combo)

    def _selected_val_datasets(self):
        """验证集（勾选的数据集）。"""
        return self._selected_checked(self.ui.val_combo)

    def _fill_defaults(self):
        self._style_all_combos()
        self._setup_multi_combo(self.ui.dataset_combo)
        self._setup_multi_combo(self.ui.val_combo, "请选择验证集")
        self._fill_dataset_multi(self.ui.dataset_combo, [])
        self._fill_dataset_multi(self.ui.val_combo, [])
        self.ui.dataset_label.setText("训练集")
        self._fill_device_combo()
        self._center_combo_items(self.ui.task_combo)
        self._fill_network_combo()
        self._fill_optimizer()
        self.ui.task_combo.setCurrentIndex(0)  # 默认检测
        self.ui.task_combo.currentIndexChanged.connect(self._on_task_changed)
        # 预设记录(模型界面训练按钮)时完整回填;首页进入填任务推荐参数
        if self._preset_record is not None:
            self._restore_record(self._preset_record)
        else:
            for edit, _name, default, _req in self._int_fields:
                if default is not None and not edit.text():
                    edit.setText(str(default))
            for edit, _name, default, _req in self._float_fields:
                if default is not None and not edit.text():
                    edit.setText(str(default))
            self._apply_task_ui()
        # 输出路径:默认留空(不填 runs 占位),只有模型界面回填才有值
        self.ui.task_badge.setText(self._task_text())
        self._setup_img_size_tip()
        self._update_summary()
        # 有训练在进行时禁用开始训练
        if hasattr(self.app, "is_training") and self.app.is_training():
            btn = getattr(self.ui, "start_train", None)
            if btn is not None:
                btn.setEnabled(False)
                btn.setToolTip("已有训练在进行中，请先停止")

    def _set_device(self, value):
        """设备下拉显示的是 GPU 型号，回填得按 itemData 里的 cuda:0 找；
        历史记录存的是小写 cpu，下拉数据是大写 CPU，按忽略大小写兜底。"""
        if not value:
            return
        combo = self.ui.device_combo
        idx = combo.findData(str(value))
        if idx < 0:
            for i in range(combo.count()):
                data = combo.itemData(i)
                if data and str(data).lower() == str(value).lower():
                    idx = i
                    break
        if idx >= 0:
            combo.setCurrentIndex(idx)

    def _device(self):
        data = self.ui.device_combo.currentData()
        if data:
            return str(data)
        return self.ui.device_combo.currentText() or "cpu"

    def _fill_device_combo(self):
        combo = self.ui.device_combo
        combo.clear()
        for text, value in _available_devices():
            combo.addItem(text, value)
            combo.setItemData(combo.count() - 1, text, Qt.ToolTipRole)
        combo.setCurrentIndex(0)
        self._center_combo_items(combo)

    def _fill_optimizer(self):
        """优化器下拉:检测/分割(detr 推荐 adamw) vs 分类(resnet 推荐 sgd)。"""
        combo = self.ui.optimizer_comboBox
        combo.clear()
        if self._task() == "classify":
            combo.addItems(["adamw", "sgd"])
            recommended = "sgd"
        else:
            combo.addItems(["adamw", "sgd", "adam"])
            recommended = "adamw"
        idx = combo.findText(recommended)
        if idx >= 0:
            combo.setCurrentIndex(idx)
        self._center_combo_items(combo)

    @staticmethod
    def _center_combo_items(combo):
        """下拉列表项文字居中(单选下拉:任务类型/网络/设备/优化器)。"""
        model = combo.model()
        for i in range(model.rowCount()):
            it = model.item(i)
            if it is not None:
                it.setTextAlignment(Qt.AlignHCenter)

    def _on_task_changed(self):
        self.ui.task_badge.setText(self._task_text())
        self._fill_optimizer()
        self._apply_task_ui()
        self._setup_img_size_tip()

    def _apply_task_ui(self):
        """任务类型切换:按任务推荐填充参数、grad_accum 可用性、网络项。

        首页进入是空表单,用户选择任务类型后由这里给出推荐值;
        模型界面回填(preset_record)时 _apply_record_params 会在其后覆盖为记录值。
        """
        task = self._task()
        epochs, lr, img, _ = self.TASK_DEFAULTS.get(task, (100, 1e-4, 640, 4))
        self.ui.grad_accum_line_txt.setEnabled(task != "classify")
        self.ui.epochs_line_txt.setText(str(epochs))
        self.ui.lr_line_txt.setText(str(lr))
        self.ui.img_size_line_txt.setText(str(img))
        # 通用参数推荐值(批次/线程数/早停)
        if not self.ui.batch_size_line_txt.text().strip():
            self.ui.batch_size_line_txt.setText("4")
        if not self.ui.batch_size_line_txt_2.text().strip():
            self.ui.batch_size_line_txt_2.setText("4")
        if not self.ui.early_stop_line_txt.text().strip():
            self.ui.early_stop_line_txt.setText("20")
        if not self.ui.grad_accum_line_txt.text().strip():
            self.ui.grad_accum_line_txt.setText("4")
        self._last_epochs_default = epochs
        self._last_lr_default = lr
        self._last_img_default = img
        self._fill_network_combo()

    def _restore_record(self, rec):
        """按指定训练记录回填全部字段(模型界面训练按钮)。"""
        task = str(rec.get("task", "") or "")
        if task in self.TASK_TEXT.values():
            for k, v in self.TASK_TEXT.items():
                if v == task:
                    idx = self.ui.task_combo.findText(k)
                    if idx >= 0:
                        self.ui.task_combo.setCurrentIndex(idx)
                    break
        self._apply_task_ui()
        train_names = [x.strip() for x in str(rec.get("dataset", "")).split(",") if x.strip()]
        val_names = [x.strip() for x in str(rec.get("val_dataset", "")).split(",") if x.strip()]
        if train_names:
            self._fill_dataset_multi(self.ui.dataset_combo, train_names)
        if val_names:
            self._fill_dataset_multi(self.ui.val_combo, val_names)
        self._apply_record_params(rec)

    def _apply_record_params(self, rec):
        """把训练记录参数回填到界面(控件按存在性防护)。"""

        def _set_int(name, val):
            edit = getattr(self.ui, name, None)
            if edit is not None and val not in (None, ""):
                try:
                    edit.setText(str(int(val)))
                except (TypeError, ValueError):
                    pass

        def _set_float(name, val):
            edit = getattr(self.ui, name, None)
            if edit is not None and val not in (None, ""):
                try:
                    edit.setText(str(float(val)))
                except (TypeError, ValueError):
                    pass

        def _set_combo(name, val):
            combo = getattr(self.ui, name, None)
            if combo is not None and val not in (None, ""):
                idx = combo.findText(str(val))
                if idx >= 0:
                    combo.setCurrentIndex(idx)

        _set_int("epochs_line_txt", rec.get("epochs"))
        _set_int("batch_size_line_txt", rec.get("batch_size"))
        _set_float("lr_line_txt", rec.get("lr"))
        _set_int("grad_accum_line_txt", rec.get("grad_accum"))
        _set_int("batch_size_line_txt_2", rec.get("num_workers"))
        _set_int("early_stop_line_txt", rec.get("early_stop"))
        img = rec.get("img_size")
        if img not in (None, ""):
            edit = getattr(self.ui, "img_size_line_txt", None)
            combo = getattr(self.ui, "img_size_comboBox", None)
            if edit is not None:
                try:
                    edit.setText(str(int(img)))
                except (TypeError, ValueError):
                    pass
            elif combo is not None:
                idx = combo.findText(str(img))
                if idx >= 0:
                    combo.setCurrentIndex(idx)
        _set_combo("network_combo", rec.get("model_size"))
        self._set_device(rec.get("device"))
        _set_combo("optimizer_comboBox", rec.get("optimizer"))
        out = rec.get("output_path")
        if out and hasattr(self.ui, "output_line_txt"):
            self.ui.output_line_txt.setText(str(out))

    def _fill_network_combo(self):
        combo = self.ui.network_combo
        combo.clear()
        combo.addItems(["nano", "small", "medium", "large"])
        self._center_combo_items(combo)
        if self._task() == "classify":
            combo.setCurrentIndex(0)

    def _setup_img_size_tip(self):
        self.ui.img_size_line_txt.setToolTip(self.TASK_TIPS.get(self._task(), ""))
        self.ui.img_note.setText(self.IMG_NOTE.get(self._task(), ""))

    # ---------- 校验 ----------
    def _setup_validators(self):
        for edit, _name, _default, _req in self._int_fields:
            edit.setValidator(QIntValidator(0, 999999, self))
        for edit, _name, _default, _req in self._float_fields:
            edit.setValidator(QDoubleValidator(0.0, 1.0, 8, self))

    def _validate(self):
        if not self._selected_datasets():
            return False, "请至少选择一个数据集"
        for edit, name, _default, required in self._int_fields:
            txt = edit.text().strip()
            if not txt and required:
                return False, "「{}」不能为空".format(name)
            if txt:
                try:
                    int(txt)
                except ValueError:
                    return False, "「{}」必须是整数（当前: {}）".format(name, txt)
        for edit, name, _default, required in self._float_fields:
            txt = edit.text().strip()
            if not txt and required:
                return False, "「{}」不能为空".format(name)
            if txt:
                try:
                    float(txt)
                except ValueError:
                    return False, "「{}」必须是数字（当前: {}）".format(name, txt)
        # 任务类型与数据集格式匹配校验(按导入时的 label_fmt 判断:cls=分类,其余=检测/分割)
        task = self._task()
        task_text = self._task_text()
        for proj, name in self._selected_datasets() + self._selected_val_datasets():
            fmt = self.app.db.get_dataset_import(proj, name).get("label_fmt", "")
            if task != "classify" and fmt == "cls":
                return False, "数据集「{}/{}」是分类数据集,无法训练{}任务".format(
                    proj, name, task_text)
            if task == "classify" and fmt != "cls":
                return False, "数据集「{}/{}」不是分类数据集(标签格式={}),无法训练图像分类".format(
                    proj, name, fmt or "未知")
        return True, ""

    # ---------- 交互 ----------
    def _select_output_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录", self.ui.output_line_txt.text())
        if d:
            self.ui.output_line_txt.setText(d)

    def _on_start_train(self):
        if self.app.is_training():
            MessageBox.warning(
                self, "开始训练","当前已有训练在进行中，请先停止!")
            return
        ok, msg = self._validate()
        if not ok:
            MessageBox.warning(self, "参数校验", msg)
            return
        ds_pairs = self._selected_datasets()
        val_pairs = self._selected_val_datasets()
        ds_names = ", ".join("{}/{}".format(p, d) for p, d in ds_pairs)
        val_names = ", ".join("{}/{}".format(p, d) for p, d in val_pairs)
        write_log("开始训练: 任务类型={} 训练集={} 验证集={}".format(
            self._task_text(), ds_names, val_names))
        record = self._save_train_record()
        # 全局启动(进度条/停止按钮在首页)
        try:
            config = self._build_train_config()
            if not self.app.start_training(config, record["id"]):
                MessageBox.warning(self, "开始训练", "已有训练在进行中，请先停止!")
                return
        except Exception as exc:
            MessageBox.critical(self, "训练启动失败", "{}\n\n{}".format(
                exc, traceback.format_exc()))
            return
        # 启动成功:立即关闭训练窗口 + 弹倒计时提示(5s 自动确认/点击立即确认)
        self.accept()
        _TrainStartDialog(parent=self).exec()

    def _save_train_record(self):
        """把本次训练的任务/数据集/参数记录到 db(供训练界面回填)。"""
        ds_pairs = self._selected_datasets()
        val_pairs = self._selected_val_datasets()
        ds_names = ", ".join("{}/{}".format(p, d) for p, d in ds_pairs)
        val_names = ", ".join("{}/{}".format(p, d) for p, d in val_pairs)
        # dataset_info 包含训练集+验证集," / " 分隔两组;组内多个用逗号
        dataset_info = (ds_names + " / " + val_names) if val_names else ds_names
        first_proj = ds_pairs[0][0] if ds_pairs else self.project
        record = {
            "id": str(uuid.uuid4()),
            "project": first_proj,
            "task": self._task(),
            "dataset": ds_names,
            "val_dataset": val_names,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": "",
            "duration": "",
            "model_size": self.ui.network_combo.currentText()
                if hasattr(self.ui, "network_combo") else "",
            "map50": "",
            "img_size": self._img_size(),
            "model_path": self._predict_model_path(),
            "dataset_info": dataset_info,
            "output_path": self.ui.output_line_txt.text().strip(),
            "epochs": self.param_int(self.ui.epochs_line_txt, 100)
                if hasattr(self.ui, "epochs_line_txt") else "",
            "batch_size": self.param_int(self.ui.batch_size_line_txt, 8)
                if hasattr(self.ui, "batch_size_line_txt") else "",
            "lr": self.param_float(self.ui.lr_line_txt, 1e-4)
                if hasattr(self.ui, "lr_line_txt") else "",
            "grad_accum": self.param_int(self.ui.grad_accum_line_txt, 4)
                if hasattr(self.ui, "grad_accum_line_txt") else "",
            "num_workers": self.param_int(self.ui.batch_size_line_txt_2, 4)
                if hasattr(self.ui, "batch_size_line_txt_2") else "",
            "early_stop": self.param_int(self.ui.early_stop_line_txt, 20)
                if hasattr(self.ui, "early_stop_line_txt") else "",
            "optimizer": self.ui.optimizer_comboBox.currentText()
                if hasattr(self.ui, "optimizer_comboBox") else "",
            "metrics": {},   # 训练中实时更新：{"epochs": [...], "series": {名称: [...]}}
            "labels": self._collect_dataset_labels(ds_pairs),
            "device": self._device(),
        }
        self.app.db.add_train_record(record)
        return record

    def _collect_dataset_labels(self, ds_pairs):
        """勾选数据集的标签并集(跨项目,训练启动时已知,指标界面下拉无需等验证)。"""
        labels = set()
        for proj, name in ds_pairs:
            try:
                for lb in self.app.db.get_dataset_labels(proj, name):
                    labels.add(str(lb))
            except Exception:
                pass
        return sorted(labels)

    def _predict_model_path(self):
        """启动训练后 checkpoint_best_regular.pth 的路径（rfdetr 最佳常规模型，训练中即存在）。"""
        out_root = self.ui.output_line_txt.text().strip()
        if not out_root:
            return ""
        return os.path.join(out_root, timestamp_dir(), "checkpoint_best_regular.pth")

    def _build_train_config(self):
        """组装子进程训练配置并写入 config.json。"""
        task = self._task()
        out_root = self.ui.output_line_txt.text().strip()
        if not out_root:
            raise ValueError("请先选择输出路径")
        os.makedirs(out_root, exist_ok=True)
        ts = timestamp_dir()
        ts_dir = os.path.join(out_root, ts)
        os.makedirs(ts_dir, exist_ok=True)
        datasets = []
        for proj, name in self._selected_datasets():
            info = self.app.db.get_dataset_import(proj, name)
            self._check_dataset_imported(name, info)
            datasets.append({
                "dataset_name": name, "project": proj, "split": "train",
                "image_path": info.get("image_path", ""),
                "label_path": info.get("label_path", ""),
                "fmt": info.get("label_fmt", "txt"),
            })
        for proj, name in self._selected_val_datasets():
            info = self.app.db.get_dataset_import(proj, name)
            self._check_dataset_imported(name, info)
            datasets.append({
                "dataset_name": name, "project": proj, "split": "val",
                "image_path": info.get("image_path", ""),
                "label_path": info.get("label_path", ""),
                "fmt": info.get("label_fmt", "txt"),
            })
        if not any(d["split"] == "train" for d in datasets):
            raise ValueError("请至少选择一个训练集数据集")
        if not any(d["split"] == "val" for d in datasets):
            raise ValueError("请至少选择一个验证集数据集")
        architecture = self.ui.network_combo.currentText() or "nano"
        if task == "classify":
            # nano/small/medium/large → resnet18/34/50/101
            architecture = {
                "nano": "resnet18", "small": "resnet34",
                "medium": "resnet50", "large": "resnet101",
            }.get(architecture, "resnet18")
        config = {
            "task": task,
            "out_root": out_root,
            "project": datasets[0]["project"],
            "timestamp_dir": ts_dir,
            "architecture": architecture,
            "device": self._device(),
            "epochs": self.param_int(self.ui.epochs_line_txt, 100),
            "batch_size": self.param_int(self.ui.batch_size_line_txt, 8),
            "num_workers": self.param_int(self.ui.batch_size_line_txt_2, 8),
            "optimizer": self.ui.optimizer_comboBox.currentText() or "adamw",
            # 早停：>0 启用（值即 patience），<=0 禁用
            "early_stop": self.param_int(self.ui.early_stop_line_txt, 20),
            "lr": self.param_float(self.ui.lr_line_txt, 1e-4),
            "img_size": self._img_size(),
            "datasets": datasets,
        }
        # 分类不传梯度累积(runner 不消费该字段),检测/分割才传
        if task != "classify":
            config["grad_accum"] = self.param_int(self.ui.grad_accum_line_txt, 4)
        cfg_path = os.path.join(ts_dir, "train_config.json")
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False)
        config["_cfg_path"] = cfg_path
        return config

    def _check_dataset_imported(self, name, info):
        """
        校验数据集已导入且路径有效（防止未导入/加载中的数据集直接训练）。
        分类数据集（fmt=="cls"）标签即子文件夹名,无需单独 label_path 目录，
        所以跳过标签目录存在性检查。
        """
        img = info.get("image_path", "")
        lab = info.get("label_path", "")
        fmt = info.get("label_fmt", "")
        if not img or not os.path.isdir(img):
            raise ValueError(
                "数据集「{}」尚未导入图像或路径无效，请先导入该数据集再训练".format(name))
        if fmt == "cls":
            return
        if not lab or not os.path.isdir(lab):
            raise ValueError(
                "数据集「{}」尚未导入标签或路径无效，请先导入该数据集再训练".format(name))

    def _img_size(self):
        edit = getattr(self.ui, "img_size_line_txt", None)
        if edit is not None:
            return self.param_int(edit, 640)
        combo = getattr(self.ui, "img_size_comboBox", None)
        return self.param_int(combo, 224) if combo is not None else 640

    def _log(self, line):
        write_log(line)

    # ---------- 参数读取 ----------
    def param_int(self, edit, default):
        try:
            return int(edit.text().strip())
        except (ValueError, AttributeError):
            return default

    def param_float(self, edit, default):
        try:
            return float(edit.text().strip())
        except (ValueError, AttributeError):
            return default

    def param(self, combo):
        return combo.currentText().strip()
