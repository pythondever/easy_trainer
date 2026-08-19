# -*- coding: utf-8 -*-
"""模型测试弹窗：在 ModelDialog 点击「测试」按钮弹出。

测试参数配置：数据/设备/模型/置信度/IoU/输出标签文件。
模型下拉只显示文件名（os.path.basename），按当前项目+数据集类型过滤。
测试结果走 TestWorker + TestResultDialog（评估模式）或自动载入首页（推理模式）。"""

import json
import os
import tempfile

from PySide6.QtCore import Qt, QEvent, QObject, QTimer
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog

from app.log import write_log
from app.message_box import MessageBox
from app.train.dialogs import _TrainStartDialog
from app.train.test_result_dialog import TestResultDialog
from app.train.test_worker import TestWorker
from ui.test_dialog import Ui_TestDialog


def _available_devices():
    try:
        import torch
    except ImportError:
        torch = None
    if torch is None or not torch.cuda.is_available():
        return ["CPU"]
    return ["cuda:{}".format(i) for i in range(torch.cuda.device_count())] + ["CPU"]


class _ClickToPopupFilter(QObject):
    def __init__(self, combo, parent=None):
        super().__init__(parent)
        self._combo = combo

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            QTimer.singleShot(0, self._combo.showPopup)
            return True
        return False


class TestDialog(QDialog):
    def __init__(self, app, record, project="", dataset="", parent=None):
        super().__init__(parent)
        self.ui = Ui_TestDialog()
        self.ui.setupUi(self)
        self.app = app
        self._project = project
        self._dataset = dataset
        self._record = record or {}
        self._worker = None
        self._combo_filters = []
        self._init_style()
        self._fill_data_combo()
        self._fill_device_combo()
        self._fill_model_combo()
        self._fill_defaults()
        self.ui.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ui.verticalLayout.setSpacing(0)
        self.ui.title_label.setAlignment(Qt.AlignTop)
        self.ui.title_label.setFixedHeight(20)
        self.ui.verticalLayout.setSpacing(5)
        self.resize(self.width(), self.sizeHint().height())
        self.ui.test_data_combo.currentIndexChanged.connect(self._on_data_changed)
        self.ui.start_test_btn.clicked.connect(self._on_start)
        self._on_data_changed(self.ui.test_data_combo.currentIndex())

    # ---------- 样式：点击任意位置展开 + 控件对齐 ----------
    def _init_style(self):
        for name in ("test_data_combo", "test_device_combo", "model_combo",
                     "confidence_txt", "iou_treshold_txt"):
            w = getattr(self.ui, name, None)
            if w is None:
                continue
            w.setFixedWidth(244)
            w.setFixedHeight(30)
        for layout_name in ("data_row", "device_row", "model_row",
                            "confidence_row", "iou_row", "output_row"):
            lay = getattr(self.ui, layout_name, None)
            if lay is None:
                continue
            has_stretch = any(lay.itemAt(i) and lay.itemAt(i).spacerItem()
                              for i in range(lay.count()))
            if not has_stretch:
                lay.insertStretch(1, 1)
        for name in ("test_data_combo", "test_device_combo", "model_combo"):
            combo = getattr(self.ui, name, None)
            if combo is None:
                continue
            combo.setEditable(True)
            combo.setFocusPolicy(Qt.StrongFocus)
            le = combo.lineEdit()
            le.setReadOnly(True)
            le.setAlignment(Qt.AlignHCenter)
            le.setStyleSheet(
                "QLineEdit { background: transparent; border: none; padding: 0; }")
            f = _ClickToPopupFilter(combo)
            combo.installEventFilter(f)
            combo.lineEdit().installEventFilter(f)
            self._combo_filters.append(f)
        # 文本框文字居中（与下拉框保持一致的视觉风格）
        for name in ("confidence_txt", "iou_treshold_txt"):
            edit = getattr(self.ui, name, None)
            if edit is not None:
                edit.setAlignment(Qt.AlignHCenter)

    # ---------- 填充 ----------
    def _fill_data_combo(self):
        """跨项目所有数据集(文本"项目/数据集",项居中)。"""
        combo = self.ui.test_data_combo
        model = QStandardItemModel(combo)
        for info in self.app.db.get_project_info():
            proj = str(info.get("project_name", "") or "")
            ds = str(info.get("dataset_name", "") or "")
            if not proj or not ds:
                continue
            item = QStandardItem("{}/{}".format(proj, ds))
            item.setData((proj, ds), Qt.UserRole)
            item.setTextAlignment(Qt.AlignHCenter)
            model.appendRow(item)
        combo.setModel(model)
        # 默认选中传入的 dataset(完整"项目/数据集"格式)
        for i in range(model.rowCount()):
            if model.item(i).text() == self._dataset:
                combo.setCurrentIndex(i)
                break

    def _fill_device_combo(self):
        combo = self.ui.test_device_combo
        combo.clear()
        for d in _available_devices():
            combo.addItem(d)
        combo.setCurrentIndex(0)

    def _fill_model_combo(self):
        """只显示当前行 record 的模型(从 record["model_path"] 取文件名),不查 db。"""
        combo = self.ui.model_combo
        combo.clear()
        path = self._record.get("model_path", "") or ""
        if not path or not os.path.exists(path):
            return
        combo.addItem(os.path.basename(path), path)
        combo.setCurrentIndex(0)
        # 鼠标悬停可见完整路径
        for i in range(combo.count()):
            combo.setItemData(i, combo.itemData(i) or "", Qt.ToolTipRole)
        if combo.count():
            combo.setToolTip(combo.currentData() or "")
            combo.currentIndexChanged.connect(
                lambda _i: combo.setToolTip(combo.currentData() or ""))

    def _fill_defaults(self):
        self.ui.confidence_txt.setText("0.5")
        self.ui.iou_treshold_txt.setText("0.5")
        self.ui.output_label_file_checkBox.setChecked(False)

    def _current_dataset(self):
        d = self.ui.test_data_combo.currentData()
        return d

    # ---------- 联动 ----------
    def _set_row_visible(self, row_name, visible):
        """隐藏/显示某行布局内的所有控件（布局本身无 setVisible）。"""
        lay = getattr(self.ui, row_name, None)
        if lay is None:
            return
        for i in range(lay.count()):
            it = lay.itemAt(i)
            w = it.widget()
            if w is not None:
                w.setVisible(visible)

    def _on_data_changed(self, _idx):
        d = self._current_dataset()
        if not d:
            return
        self._project, self._dataset = d
        self._fill_model_combo()
        info = self.app.db.get_dataset_import(self._project, self._dataset) or {}
        cls_mode = info.get("label_fmt", "") == "cls"
        self._cls_mode = cls_mode
        # 分类模式：隐藏 iou 阈值行 + 输出标签文件行（分类无框、无需输出标注）
        self._set_row_visible("iou_row", not cls_mode)
        self._set_row_visible("output_row", not cls_mode)
        labeled = int(info.get("labeled") or 0)
        has_label = labeled > 0
        self.ui.iou_treshold_txt.setEnabled(has_label)
        if not has_label:
            # 推理模式：强制输出标注文件
            self.ui.output_label_file_checkBox.setChecked(True)
            self.ui.output_label_file_checkBox.setEnabled(False)
        else:
            self.ui.output_label_file_checkBox.setEnabled(True)
            self.ui.output_label_file_checkBox.setChecked(False)

    # ---------- 开始测试 ----------
    def _on_start(self):
        if self._worker is not None and self._worker.isRunning():
            MessageBox.warning(self, "测试", "已有测试在进行中")
            return
        ds = self._current_dataset()
        if not ds:
            return
        proj, ds_name = ds
        cls_mode = getattr(self, "_cls_mode", False)
        if cls_mode:
            # 分类模式：无置信度/IoU 概念，用默认值；不输出标注文件
            conf, iou, output_labels = 0.5, 0.5, False
        else:
            try:
                conf = float(self.ui.confidence_txt.text() or "0.5")
                iou = float(self.ui.iou_treshold_txt.text() or "0.5")
            except ValueError:
                MessageBox.warning(self, "测试", "置信度/iou阈值必须是数字")
                return
            output_labels = bool(self.ui.output_label_file_checkBox.isChecked())
        model_path = self.ui.model_combo.currentData()
        if not model_path:
            MessageBox.warning(self, "测试", "请选择模型")
            return
        binding = self.app.db.get_dataset_import(proj, ds_name) or {}
        image_paths = binding.get("image_paths") or (
            [binding.get("image_path")] if binding.get("image_path") else [])
        label_paths = binding.get("label_paths") or (
            [binding.get("label_path")] if binding.get("label_path") else [])
        image_path = image_paths[0] if image_paths else ""
        label_path = label_paths[0] if label_paths else ""
        if not image_path:
            MessageBox.warning(self, "测试", "当前数据集未导入图像")
            return
        has_label = int(binding.get("labeled") or 0) > 0
        device = self.ui.test_device_combo.currentText() or "cuda"
        total = int(binding.get("total") or 0)
        # 配置写入临时文件,TestWorker 子进程读它
        fd, cfg_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        cfg = {
            "model_path": model_path, "image_path": image_path,
            "label_path": label_path, "iou_threshold": iou,
            "confidence": conf, "has_label": has_label, "device": device,
            "total": total, "output_labels": output_labels,
            "task": "classify" if cls_mode else "",
            "_cfg_path": cfg_path,
        }
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        write_log("[test] 启动测试 worker: model={} images={} label={} device={} cfg={}".format(
            model_path, image_path, label_path, device, cfg_path))
        # 进度条交给首页
        if hasattr(self.app, "_show_train_task"):
            self.app._show_train_task("测试准备中...", 0)
        self._worker = TestWorker(cfg, parent=self.app)
        workers = getattr(self.app, "_test_workers", None)
        if workers is None:
            workers = set()
            self.app._test_workers = workers
        workers.add(self._worker)
        self._worker.log.connect(self._on_log)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished_ok.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)
        self._worker.finished.connect(
            lambda: workers.discard(self._worker))
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.start()
        self.ui.start_test_btn.setEnabled(False)
        self.accept()
        _TrainStartDialog(parent=self.app, title="测试即将开始",
                          message="测试即将开始").exec()

    def _on_log(self, line):
        write_log("[test] " + line)

    def _on_progress(self, done, total):
        # 推算剩余时间(按已用时长外推),首页进度条旁的 "剩余时间" 会每秒倒计时
        if hasattr(self.app, "_update_test_eta"):
            self.app._update_test_eta(done, total)
        if hasattr(self.app, "_show_train_task"):
            pct = done * 100.0 / total if total else 0
            self.app._show_train_task(
                "测试中 {}/{}".format(done, total), pct)

    def _on_finished(self, res):
        write_log("[test-dialog] 测试完成, ok={}".format(res.get("ok")))
        if hasattr(self.app, "_hide_train_task"):
            self.app._hide_train_task()
        if hasattr(self.app, "_test_start_ts"):
            self.app._test_start_ts = 0
        self.ui.start_test_btn.setEnabled(True)
        self._worker = None
        if not res.get("ok"):
            MessageBox.warning(self, "测试结果", "测试未正常完成")
            return
        if "P" in res or res.get("task") == "classify":
            TestResultDialog(res, parent=self.app).exec()
        else:
            self.app._load_dataset_view(self._project, self._dataset)

    def _on_failed(self, detail):
        write_log("[test-dialog] 测试失败: {}".format(detail[:300]))
        if hasattr(self.app, "_hide_train_task"):
            self.app._hide_train_task()
        if hasattr(self.app, "_test_start_ts"):
            self.app._test_start_ts = 0
        self.ui.start_test_btn.setEnabled(True)
        self._worker = None
        MessageBox.critical(self, "测试失败", detail)