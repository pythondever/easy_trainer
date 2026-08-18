# -*- coding: utf-8 -*-
"""训练对话框：分类(ResNet) / 检测(RF-DETR) / 分割(RF-DETR Seg)。"""

import os
import json
import traceback
import uuid
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QEvent, QObject
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import (QDialog, QLabel, QFileDialog, QSizePolicy,
                               QComboBox, QHBoxLayout, QPushButton,
                               QVBoxLayout)
from PySide6.QtGui import QStandardItem

from app.message_box import MessageBox
from app.log import write_log
from app.train.data_prep import timestamp_dir
from ui.classify import Ui_ClassifyDialog
from ui.detect import Ui_DetectDialog
from ui.segment import Ui_SegmentDialog

try:
    import torch
except ImportError:
    torch = None


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
        label.setStyleSheet("font-size: 15px;")
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
    if torch is None or not torch.cuda.is_available():
        return ["CPU"]
    return ["cuda:{}".format(i)
            for i in range(torch.cuda.device_count())] + ["CPU"]


class TrainDialogBase(QDialog):
    TITLE = "训练"

    def __init__(self, app, project, dataset):
        super().__init__(app)
        self.app = app
        self.project = project
        self.dataset = dataset
        self.ui = None
        self._int_fields = []      # [(控件, 名称, 默认值, 是否必填)]
        self._float_fields = []    # [(控件, 名称, 默认值, 是否必填)]
        self._combo_filters = []
        self._build()

    def closeEvent(self, event):
        if getattr(self.app, "is_training", None) and self.app.is_training():
            MessageBox.information(
                self, "训练进行中","训练正在后台进行中,可在首页查看进度,并通过「停止训练」按钮停止.")
        super().closeEvent(event)

    # ---------- 初始化 ----------
    def _build(self):
        self.ui = self._make_ui()
        self.ui.setupUi(self)
        self.setWindowTitle(self.TITLE)
        self.setMinimumHeight(520)
        self.ui.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.ui.gridLayout.setHorizontalSpacing(9)
        self.ui.gridLayout.setVerticalSpacing(0)
        self.ui.gridLayout.setRowStretch(0, 0)
        self.ui.gridLayout.setRowStretch(1, 0)
        self.ui.horizontalLayout_17.setContentsMargins(30, 0, 30, 0)
        self.ui.horizontalLayout_17.setSpacing(20)
        if hasattr(self.ui, "bottomActions"):
            self.ui.bottomActions.setContentsMargins(0, 8, 0, 8)
        for vl in (getattr(self.ui, "verticalLayout", None),
                   getattr(self.ui, "verticalLayout_2", None)):
            if vl is not None:
                vl.setSpacing(4)
                vl.setContentsMargins(0, 0, 0, 0)
                vl.setAlignment(Qt.AlignTop)
        self._setup_extra_ui()
        self._define_fields()
        self._fill_defaults()
        self._setup_validators()
        self._fix_heights()
        self._connect()
        self.resize(550, 530)
        self._center_start_button()

    def _center_start_button(self):
        """
        「开始训练」按钮水平居中
        """
        ba = getattr(self.ui, "bottomActions", None)
        if ba is None:
            return
        btn = None
        while ba.count():
            it = ba.takeAt(0)
            w = it.widget()
            if w is not None:
                w.hide()
                if btn is None:
                    btn = w
        if btn is not None:
            btn.show()
            ba.addStretch(1)
            ba.addWidget(btn)
            ba.addStretch(1)

    def _fix_heights(self):
        """统一控件尺寸——QSS"""
        for edit, _n, _d, _r in self._int_fields + self._float_fields:
            try:
                edit.setFixedHeight(30)
                edit.setFixedWidth(244)
                edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            except Exception:
                pass
        for combo_name in ("dataset_combo", "val_combo", "network_combo",
                           "device_combo", "img_size_comboBox",
                           "optimizer_comboBox"):
            combo = getattr(self.ui, combo_name, None)
            if combo is not None:
                combo.setFixedHeight(30)
                combo.setFixedWidth(244)
        for btn_name in ("start_train",
                         "select_output_path_btn"):
            btn = getattr(self.ui, btn_name, None)
            if btn is not None:
                btn.setFixedHeight(30)
        for lab_name in ("train_cfg_label",):
            lab = getattr(self.ui, lab_name, None)
            if lab is not None:
                lab.setFixedHeight(22)
        self._push_spacers_to_left()

    def _push_spacers_to_left(self):
        """每行重排为 [label, spacer, 控件]：label 贴左、控件贴右。"""
        candidates = ["horizontalLayout", "horizontalLayout_10",
                      "horizontalLayout_val"] + \
                     [f"horizontalLayout_{i}" for i in range(1, 25)]
        for name in candidates:
            hl = getattr(self.ui, name, None)
            if hl is None or not hasattr(hl, "count"):
                continue
            if name == "horizontalLayout_15":
                continue
            sp_idx = -1
            for i in range(hl.count()):
                it = hl.itemAt(i)
                if it is None:
                    continue
                sp = it.spacerItem()
                if sp and sp.sizePolicy().horizontalPolicy() == QSizePolicy.Expanding:
                    sp_idx = i
                    break
            if sp_idx < 0:
                continue
            label_idx = -1
            for i in range(hl.count()):
                it = hl.itemAt(i)
                if it and it.widget() and isinstance(it.widget(), QLabel):
                    label_idx = i
                    break
            target_after_label = label_idx + 1 if label_idx >= 0 else 0
            if sp_idx == target_after_label:
                continue
            sp_item = hl.takeAt(sp_idx)
            if sp_item is None:
                continue
            cur_label_idx = target_after_label
            if sp_idx < cur_label_idx:
                cur_label_idx = label_idx
            hl.insertItem(cur_label_idx, sp_item)

    def _define_fields(self):
        pass

    def _make_ui(self):
        raise NotImplementedError

    def _setup_extra_ui(self):
        vl = getattr(self.ui, "verticalLayout_2", None)
        if vl is not None:
            for i in range(vl.count()):
                lay = vl.itemAt(i).layout() if vl.itemAt(i) else None
                if lay is None:
                    continue
                lay.setSpacing(0)
                for j in range(lay.count()):
                    it = lay.itemAt(j)
                    if it is None:
                        continue

                    if it.widget() is None:
                        lay.setStretch(j, 1)
                    else:
                        lay.setStretch(j, 0)

    def _connect(self):
        self.ui.start_train.clicked.connect(self._on_start_train)
        self.ui.select_output_path_btn.clicked.connect(self._select_output_dir)

    # ---------- 填充 ----------
    def _style_combo(self, combo):
        """
        下拉框文本居中 + 点击框内任意位置打开下拉。
        """
        combo.setEditable(True)
        combo.setFocusPolicy(Qt.StrongFocus)
        le = combo.lineEdit()
        le.setReadOnly(True)
        le.setAlignment(Qt.AlignHCenter)
        le.setStyleSheet(
            "QLineEdit { background: transparent; border: none; padding: 0; }")
        f = _ClickToPopupFilter(combo)
        combo.installEventFilter(f)
        le.installEventFilter(f)
        self._combo_filters.append(f)

    def _style_all_combos(self):
        for name in ("dataset_combo", "val_combo", "network_combo",
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

    def _current_dataset_type(self):
        for ds in self.app.db.get_datasets(self.project):
            if ds["dataset_name"] == self.dataset:
                return ds.get("dataset_type", "")
        return ""

    def _fill_dataset_multi(self, combo, checked_names):
        """只列与当前数据集同类型的数据集，checked_names 内的默认勾选。"""
        model = combo.model()
        model.clear()
        dtype = self._current_dataset_type()
        for ds in self.app.db.get_datasets(self.project):
            if dtype and ds.get("dataset_type") != dtype:
                continue
            item = QStandardItem(ds["dataset_name"])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            item.setCheckState(
                Qt.Checked if ds["dataset_name"] in checked_names
                else Qt.Unchecked)
            model.appendRow(item)
        self._update_multi_label(combo)

    def _selected_checked(self, combo):
        model = combo.model()
        return [model.item(i).text() for i in range(model.rowCount())
                if model.item(i).checkState() == Qt.Checked]

    def _update_multi_label(self, combo, *_):
        checked = self._selected_checked(combo)
        combo.setEditText(", ".join(checked))
        combo.setToolTip("\n".join(checked) if checked else "")
        if not checked:
            combo.setCurrentIndex(-1)

    def _selected_datasets(self):
        """训练集（勾选的数据集）。"""
        return self._selected_checked(self.ui.dataset_combo)

    def _selected_val_datasets(self):
        """验证集（勾选的数据集）。"""
        return self._selected_checked(self.ui.val_combo)

    def _add_val_row(self):
        if getattr(self.ui, "val_combo", None) is not None:
            return
        vl = self.ui.verticalLayout
        idx = -1
        for i in range(vl.count()):
            it = vl.itemAt(i)
            if it.layout() and self._layout_has_widget(it.layout(),
                                                       self.ui.dataset_combo):
                idx = i
                break
        lab = QLabel("验证集")
        lab.setStyleSheet("color: #e8eaf0; font-size: 13px;")
        combo = QComboBox(self)
        combo.setFixedSize(244, 30)
        row = QHBoxLayout()
        row.setSpacing(4)
        row.addWidget(lab)
        row.addStretch(1)
        row.addWidget(combo)
        if idx >= 0:
            vl.insertLayout(idx + 1, row)
        else:
            vl.addLayout(row)
        self.ui.val_label = lab
        self.ui.val_combo = combo

    @staticmethod
    def _layout_has_widget(layout, widget):
        for i in range(layout.count()):
            it = layout.itemAt(i)
            if it.widget() is widget:
                return True
            if it.layout() and TrainDialogBase._layout_has_widget(it.layout(), widget):
                return True
        return False

    def _fill_defaults(self):
        self._add_val_row()
        self._style_all_combos()
        self._setup_multi_combo(self.ui.dataset_combo)
        self._setup_multi_combo(self.ui.val_combo, "请选择验证集")
        self._fill_dataset_multi(self.ui.dataset_combo, [])
        self._fill_dataset_multi(self.ui.val_combo, [])
        self.ui.dataset_label.setText("训练集")
        devs = _available_devices()
        self.ui.device_combo.addItems(devs)
        self.ui.device_combo.setCurrentIndex(0)
        self._fill_network_combo()
        for edit, _name, default, _req in self._int_fields:
            if default is not None and not edit.text():
                edit.setText(str(default))
        for edit, _name, default, _req in self._float_fields:
            if default is not None and not edit.text():
                edit.setText(str(default))
        self._setup_img_size_tip()
        workspace = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        runs = os.path.join(workspace, "runs", self.project, self.dataset)
        self.ui.output_line_txt.setText(runs)
        self._restore_last_config()
        # 有训练在进行时禁用开始训练
        if hasattr(self.app, "is_training") and self.app.is_training():
            btn = getattr(self.ui, "start_train", None)
            if btn is not None:
                btn.setEnabled(False)
                btn.setToolTip("已有训练在进行中，请先停止")

    def _restore_last_config(self):
        """回填最近一次训练的配置:匹配训练/验证集包含当前数据集的记录
        (多数据集共用一份参数),否则回退到项目最近一次训练。"""
        recs = [r for r in self.app.db.get_train_records()
                if r.get("project") == self.project and r.get("dataset")]
        if not recs:
            return
        recs.sort(key=lambda r: str(r.get("start_time", "")), reverse=True)
        cur = self.dataset
        last = None
        for r in recs:
            train_names = [x.strip() for x in str(r.get("dataset", "")).split(",") if x.strip()]
            val_names = [x.strip() for x in str(r.get("val_dataset", "")).split(",") if x.strip()]
            if cur in train_names or cur in val_names:
                last = r
                break
        if last is None:
            last = recs[0]
        train_names = [x.strip() for x in str(last.get("dataset", "")).split(",") if x.strip()]
        val_names = [x.strip() for x in str(last.get("val_dataset", "")).split(",") if x.strip()]
        if train_names:
            self._fill_dataset_multi(self.ui.dataset_combo, train_names)
        if val_names:
            self._fill_dataset_multi(self.ui.val_combo, val_names)
        self._apply_record_params(last)

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
        _set_combo("device_combo", rec.get("device"))
        _set_combo("optimizer_comboBox", rec.get("optimizer"))
        out = rec.get("output_path")
        if out and hasattr(self.ui, "output_line_txt"):
            self.ui.output_line_txt.setText(str(out))

    def _fill_network_combo(self):
        raise NotImplementedError

    def _setup_img_size_tip(self):
        """图像尺寸控件的推荐 tooltip；子类按任务类型覆盖。"""
        pass

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
        ds_names = ", ".join(self._selected_datasets())
        val_names = ", ".join(self._selected_val_datasets())
        write_log("开始训练: 任务类型={} 项目={} 训练集={} 验证集={}".format(
            self.TITLE, self.project, ds_names, val_names))
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
        """把本次训练的项目/数据集/参数记录到 db(供训练界面下次回填)。"""
        ds_names = self._selected_datasets() or [self.dataset]
        val_names = self._selected_val_datasets()
        record = {
            "id": str(uuid.uuid4()),
            "project": self.project,
            "dataset": ", ".join(ds_names),
            "val_dataset": ", ".join(val_names),
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": "",
            "duration": "",
            "model_size": self.ui.network_combo.currentText()
                if hasattr(self.ui, "network_combo") else "",
            "map50": "",
            "img_size": self._img_size(),
            "model_path": self._predict_model_path(),
            "dataset_info": "{}/{}".format(self.project, ", ".join(ds_names)),
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
            "labels": self._collect_dataset_labels(ds_names),
            "device": self.ui.device_combo.currentText()
                if hasattr(self.ui, "device_combo") else "",
        }
        self.app.db.add_train_record(record)
        return record

    def _collect_dataset_labels(self, ds_names):
        """勾选数据集的标签并集（训练启动时已知，指标界面下拉无需等验证）。"""
        labels = set()
        for name in ds_names:
            try:
                for lb in self.app.db.get_dataset_labels(self.project, name):
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
        out_root = self.ui.output_line_txt.text().strip()
        if not out_root:
            raise ValueError("请先选择输出路径")
        os.makedirs(out_root, exist_ok=True)
        ts = timestamp_dir()
        ts_dir = os.path.join(out_root, ts)
        os.makedirs(ts_dir, exist_ok=True)
        datasets = []
        for name, split in ((n, "train") for n in self._selected_datasets()):
            info = self.app.db.get_dataset_import(self.project, name)
            self._check_dataset_imported(name, info)
            datasets.append({
                "dataset_name": name, "project": self.project, "split": split,
                "image_path": info.get("image_path", ""),
                "label_path": info.get("label_path", ""),
                "fmt": info.get("label_fmt", "txt"),
            })
        for name, split in ((n, "val") for n in self._selected_val_datasets()):
            info = self.app.db.get_dataset_import(self.project, name)
            self._check_dataset_imported(name, info)
            datasets.append({
                "dataset_name": name, "project": self.project, "split": split,
                "image_path": info.get("image_path", ""),
                "label_path": info.get("label_path", ""),
                "fmt": info.get("label_fmt", "txt"),
            })
        if not any(d["split"] == "train" for d in datasets):
            raise ValueError("请至少选择一个训练集数据集")
        if not any(d["split"] == "val" for d in datasets):
            raise ValueError("请至少选择一个验证集数据集")
        config = {
            "out_root": out_root,
            "project": self.project,
            "timestamp_dir": ts_dir,
            "architecture": self.ui.network_combo.currentText()
                if hasattr(self.ui, "network_combo") else "nano",
            "device": self.ui.device_combo.currentText()
                if hasattr(self.ui, "device_combo") else "cpu",
            "epochs": self.param_int(self.ui.epochs_line_txt, 100)
                if hasattr(self.ui, "epochs_line_txt") else 100,
            "batch_size": self.param_int(self.ui.batch_size_line_txt, 8)
                if hasattr(self.ui, "batch_size_line_txt") else 8,
            "grad_accum": self.param_int(self.ui.grad_accum_line_txt, 4)
                if hasattr(self.ui, "grad_accum_line_txt") else 4,
            "num_workers": self.param_int(self.ui.batch_size_line_txt_2, 8)
                if hasattr(self.ui, "batch_size_line_txt_2") else 8,
            # 早停：>0 启用（值即 patience），<=0 禁用
            "early_stop": self.param_int(self.ui.early_stop_line_txt, 20)
                if hasattr(self.ui, "early_stop_line_txt") else 20,
            "lr": self.param_float(self.ui.lr_line_txt, 1e-4)
                if hasattr(self.ui, "lr_line_txt") else 1e-4,
            "img_size": self._img_size(),
            "datasets": datasets,
        }
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


class ClassifyDialog(TrainDialogBase):
    TITLE = "图像分类训练"

    def _make_ui(self):
        return Ui_ClassifyDialog()

    def _fill_network_combo(self):
        # 与检测/分割一致用 nano/small/medium/large, 训练时映射到 resnet 型号
        self.ui.network_combo.addItems(["nano", "small", "medium", "large"])
        self.ui.network_combo.setCurrentIndex(0)

    def _setup_extra_ui(self):
        labels = self.app.db.get_dataset_labels(self.project, self.dataset)
        if labels:
            self._num_classes = len(labels)
        else:
            self._num_classes = 10
        combo = getattr(self.ui, "img_size_comboBox", None)
        if combo is not None:
            combo.addItems(["224", "256"])
            combo.setCurrentIndex(0)
        optimizer = getattr(self.ui, "optimizer_comboBox", None)
        if optimizer is not None:
            optimizer.addItems(["adamw", "sgd"])

    def _build_train_config(self):
        config = super()._build_train_config()
        config["task"] = "classify"
        config["num_classes"] = getattr(self, "_num_classes", 10)
        # 网络 nano/small/medium/large → resnet18/34/50/101
        resnet = {
            "nano": "resnet18", "small": "resnet34",
            "medium": "resnet50", "large": "resnet101",
        }.get(config.get("architecture", "nano"), "resnet18")
        config["architecture"] = resnet
        cfg_path = config.get("_cfg_path")
        if cfg_path:
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False)
        return config

    def _define_fields(self):
        self._int_fields = [
            (self.ui.batch_size_line_txt, "批次", 4, True),
            (self.ui.epochs_line_txt, "轮次", 30, True),
            (self.ui.batch_size_line_txt_2, "线程数", 4, True),
        ]
        self._float_fields = [
            (self.ui.lr_line_txt, "学习率", 0.001, True),
        ]

    def _setup_img_size_tip(self):
        combo = getattr(self.ui, "img_size_comboBox", None)
        if combo is not None:
            combo.setToolTip("图像分类推荐尺寸：224（小图用 224，较大图可到 256）")


class DetectDialog(TrainDialogBase):
    TITLE = "目标检测训练"

    def _make_ui(self):
        return Ui_DetectDialog()

    def _fill_network_combo(self):
        self.ui.network_combo.addItems(["nano", "small", "medium", "large"])

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

    def _setup_img_size_tip(self):
        edit = getattr(self.ui, "img_size_line_txt", None)
        if edit is not None:
            edit.setToolTip("目标检测推荐图像尺寸：640（可设为 32 的倍数如 640/672）")


class SegmentDialog(TrainDialogBase):
    TITLE = "图像分割训练"

    def _make_ui(self):
        return Ui_SegmentDialog()

    def _fill_network_combo(self):
        self.ui.network_combo.addItems(["nano", "small", "medium", "large"])

    def _define_fields(self):
        self._int_fields = [
            (self.ui.batch_size_line_txt, "批次", 4, True),
            (self.ui.grad_accum_line_txt, "梯度累积", 4, True),
            (self.ui.epochs_line_txt, "轮次", 100, True),
            (self.ui.batch_size_line_txt_2, "线程数", 4, True),
            (self.ui.img_size_line_txt, "图像尺寸", 636, True),
            (self.ui.early_stop_line_txt, "早停", 20, False),
        ]
        self._float_fields = [
            (self.ui.lr_line_txt, "学习率", 1e-4, True),
        ]

    def _setup_img_size_tip(self):
        edit = getattr(self.ui, "img_size_line_txt", None)
        if edit is not None:
            edit.setToolTip("图像分割推荐尺寸：636（必须为 12 的倍数，如 636/648/660）")

    def _build_train_config(self):
        # 复用检测链路完整
        config = super()._build_train_config()
        config["task"] = "segment"
        cfg_path = config.get("_cfg_path")
        if cfg_path:
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False)
        return config
