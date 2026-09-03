# -*- coding: utf-8 -*-
"""模型测试弹窗：在 ModelDialog 点击「测试」按钮弹出。

测试参数配置：数据/设备/模型/置信度/IoU/输出标签文件。
模型下拉只显示文件名（os.path.basename），按当前项目+数据集类型过滤。
测试结果走 TestWorker + TestResultDialog（评估模式）或自动载入首页（推理模式）。"""

import json
import os
import tempfile
import time

from PySide6.QtCore import QLocale, Qt, QEvent, QObject, QTimer
from PySide6.QtGui import (QDoubleValidator, QStandardItem,
                           QStandardItemModel, QValidator)
from PySide6.QtWidgets import QDialog, QFormLayout, QComboBox

from app.core.log import write_log
from app.widgets.dialog_buttons import apply_icon
from app.widgets.message_box import MessageBox
from app.train.dialogs import _TrainStartDialog, _available_devices
from app.train.test_result_dialog import TestResultDialog
from app.train.test_worker import TestWorker
from ui.test_dialog import Ui_TestDialog


class _RatioValidator(QDoubleValidator):
    """0~1 校验。QDoubleValidator 会把超出上限的 "1.5" 判成中间态放行，
    这里补一刀：数值已经超 1 的中间态直接拒绝。"""

    def validate(self, text, pos):
        state, text, pos = super().validate(text, pos)
        if state == QValidator.State.Intermediate:
            try:
                if float(text) > 1.0:
                    state = QValidator.State.Invalid
            except ValueError:
                pass
        return state, text, pos


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
        self._preset_dataset = dataset
        self._record = record or {}
        self._worker = None
        self._combo_filters = []
        self._model_path = str(self._record.get("model_path", "") or "")
        self._init_style()
        self._fill_model_card()
        self._fill_data_combo()
        self._fill_device_combo()
        self._fill_defaults()
        self.resize(max(self.sizeHint().width(), 520), self.sizeHint().height())
        self.ui.start_test_btn.clicked.connect(self._on_start)
        self.ui.cancel_btn.clicked.connect(self.reject)
        self._on_data_changed()

    # ---------- 样式：点击任意位置展开 + 控件对齐 ----------
    def _init_style(self):
        for name in ("test_data_combo", "test_device_combo",
                     "confidence_txt", "iou_treshold_txt"):
            w = getattr(self.ui, name, None)
            if w is not None:
                w.setFixedHeight(30)
        # 下拉的 sizeHint 按最长条目算，GPU 全名会把弹窗撑到 680+；
        # 改成按固定字符数估宽，实际列宽交给 minimumSize 决定
        for name in ("test_data_combo", "test_device_combo"):
            combo = getattr(self.ui, name, None)
            if combo is not None:
                combo.setSizeAdjustPolicy(
                    QComboBox.SizeAdjustPolicy
                    .AdjustToMinimumContentsLengthWithIcon)
                combo.setMinimumContentsLength(12)
        apply_icon(self.ui.cancel_btn, "取消")
        # 提示文字排在勾选框右侧，得显式要剩余空间：
        # 关掉 wordWrap 后 sizeHint 才是整句宽度，否则会塌成最长单词的宽度
        self.ui.out_wrap_layout.setStretch(1, 1)
        self.ui.out_note.setMinimumWidth(0)
        self.ui.out_note.setToolTip(self.ui.out_note.text())
        self._align_form_labels()
        combo = self.ui.test_device_combo
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
        for name in ("confidence_txt", "iou_treshold_txt"):
            edit = getattr(self.ui, name, None)
            if edit is not None:
                edit.setAlignment(Qt.AlignHCenter)
                self._limit_ratio(edit)

    def _limit_ratio(self, edit):
        """标签上的「（0~1）」已去掉，范围约束全靠这里。
        校验器只管逐字符输入，残留脏值在 editingFinished 里收拾。"""
        v = _RatioValidator(0.0, 1.0, 3, edit)
        v.setNotation(QDoubleValidator.Notation.StandardNotation)
        v.setLocale(QLocale(QLocale.Language.C))
        edit.setValidator(v)
        edit.editingFinished.connect(self._clamp_ratios)

    def _clamp_ratios(self):
        for name in ("confidence_txt", "iou_treshold_txt"):
            edit = getattr(self.ui, name, None)
            if edit is None or not edit.isEnabled():
                continue
            try:
                value = float(edit.text().strip())
            except ValueError:
                value = 0.5
            edit.setText("{:g}".format(min(1.0, max(0.0, value))))

    def _align_form_labels(self):
        """两个表单的 label 列同宽,字段列左边界对齐。"""
        labels = []
        for name in ("form_source", "form_param"):
            form = getattr(self.ui, name, None)
            if form is None:
                continue
            for row in range(form.rowCount()):
                item = form.itemAt(row, QFormLayout.LabelRole)
                if item is not None and item.widget() is not None:
                    labels.append(item.widget())
        if not labels:
            return
        width = max(lab.sizeHint().width() for lab in labels)
        for lab in labels:
            lab.setMinimumWidth(width)

    # ---------- 填充 ----------
    def _setup_multi_combo(self, combo):
        """配置成多选下拉(可编辑+只读+居中+点任意位置展开),与统计/训练一致。"""
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

    def _fill_data_combo(self):
        """
        跨项目所有数据集(文本"项目/数据集",可多选),入口传入的默认勾选。
        数据源与首页项目树/统计/训练一致:先 get_projects() 拿项目名,再
        get_datasets(name) 拿该项目下数据集。直接遍历 get_project_info()
        会把已删除项目残留的孤儿记录也列出来。
        """
        combo = self.ui.test_data_combo
        self._setup_multi_combo(combo)
        checked = {self._preset_dataset} if self._preset_dataset else set()
        model = QStandardItemModel(combo)
        for proj in self.app.db.get_projects():
            for ds_info in self.app.db.get_datasets(proj):
                ds = str(ds_info.get("dataset_name", "") or "")
                if not ds:
                    continue
                text = "{}/{}".format(proj, ds)
                item = QStandardItem(text)
                item.setData((proj, ds), Qt.UserRole)
                item.setTextAlignment(Qt.AlignHCenter)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                item.setCheckState(
                    Qt.Checked if text in checked else Qt.Unchecked)
                model.appendRow(item)
        combo.setModel(model)
        # 连接必须晚于 setModel, 否则绑在旧 model 上收不到勾选变化
        combo.model().itemChanged.connect(lambda *_: self._on_data_changed())
        combo.activated.connect(lambda _i: self._on_data_changed())
        self._update_data_label()

    def _checked_datasets(self):
        """勾选的数据集 [(项目, 数据集), ...]。"""
        out = []
        model = self.ui.test_data_combo.model()
        if model is None:
            return out
        for i in range(model.rowCount()):
            item = model.item(i)
            if item.checkState() == Qt.Checked:
                data = item.data(Qt.UserRole)
                if isinstance(data, tuple) and len(data) == 2:
                    out.append(data)
        return out

    def _update_data_label(self):
        """把勾选的数据集拼到编辑区(居中),未选时清空。"""
        checked = self._checked_datasets()
        texts = ["{}/{}".format(p, d) for p, d in checked]
        combo = self.ui.test_data_combo
        combo.setEditText(", ".join(texts))
        combo.setToolTip("\n".join(texts) if texts else "")
        if not texts:
            combo.setCurrentIndex(-1)

    def _fill_device_combo(self):
        combo = self.ui.test_device_combo
        combo.clear()
        for text, value in _available_devices():
            combo.addItem(text, value)
            combo.setItemData(combo.count() - 1, text, Qt.ToolTipRole)
        combo.setCurrentIndex(0)

    def _fill_model_card(self):
        """取代原来的模型下拉：一次只填一个模型，点开没得选，信息直接摆出来更清楚。"""
        u = self.ui
        rec = self._record
        task = {"detect": "检测", "segment": "分割",
                "classify": "分类"}.get(rec.get("task", ""), "—")
        u.task_badge.setText(task)
        path = self._model_path
        if not path:
            u.model_name.setText("未指定模型")
            u.model_meta.setText("请在模型列表中重新选择一行")
            return
        u.model_name.setText(os.path.basename(path))
        u.model_name.setToolTip(path)
        meta = []
        metric = rec.get("map50") or rec.get("accuracy") or ""
        if metric:
            try:
                label = "准确率" if rec.get("task") == "classify" else "mAP50"
                meta.append("{} {:.3f}".format(label, float(metric)))
            except (TypeError, ValueError):
                pass
        if rec.get("img_size"):
            meta.append("输入 {}".format(rec["img_size"]))
        if rec.get("model_size"):
            meta.append("规模 {}".format(rec["model_size"]))
        if rec.get("start_time"):
            meta.append("训练 {}".format(str(rec["start_time"])[:16]))
        u.model_meta.setText(" · ".join(meta) if meta
                             else "该记录未保存训练指标")
        if not os.path.exists(path):
            u.model_meta.setText((u.model_meta.text() + " · 文件已不存在")
                                 .lstrip(" ·"))

    def _fill_defaults(self):
        self.ui.confidence_txt.setText("0.5")
        self.ui.iou_treshold_txt.setText("0.5")
        self.ui.output_label_file_checkBox.setChecked(False)

    # ---------- 联动 ----------
    def _set_form_row_visible(self, form_name, row, visible):
        """隐藏/显示指定 QFormLayout 的某一行（label + field 一起）。"""
        form = getattr(self.ui, form_name, None)
        if form is None:
            return
        for role in (QFormLayout.LabelRole, QFormLayout.FieldRole):
            item = form.itemAt(row, role)
            if item is not None and item.widget() is not None:
                item.widget().setVisible(visible)
        # QFormLayout 不监听子控件隐藏，sizeHint 缓存不失效会把高度留成空白
        form.invalidate()
        lay = self.layout()
        if lay is not None:
            lay.invalidate()

    def _update_summary(self, checked):
        if not checked:
            self.ui.summary_text.setText("请先勾选要测试的数据集")
            return
        total = 0
        labeled_ds = 0
        cls_ds = 0
        for proj, ds_name in checked:
            info = self.app.db.get_dataset_import(proj, ds_name) or {}
            total += int(info.get("total") or 0)
            if int(info.get("labeled") or 0) > 0:
                labeled_ds += 1
            if info.get("label_fmt", "") == "cls":
                cls_ds += 1
        head = "{} 个数据集 · {} 张图".format(len(checked), total)
        if cls_ds == len(checked):
            tail = "分类数据集，统计每张图的判断正确率"
        elif labeled_ds == len(checked):
            tail = "已标注，评估模式：统计检出率 / 漏检 / 误检"
        elif labeled_ds == 0:
            tail = "未标注，推理模式：只输出预测标签"
        else:
            tail = "部分已标注，已标注与未标注的数据集不能一起测"
        self.ui.summary_text.setText("{} · {}".format(head, tail))

    def _on_data_changed(self):
        """按首个勾选的数据集决定界面模式;未选任何数据集时纯展示、不联动。"""
        self._update_data_label()
        checked = self._checked_datasets()
        self._update_summary(checked)
        if not checked:
            self._project, self._dataset = "", ""
            return
        self._project, self._dataset = checked[0]
        info = self.app.db.get_dataset_import(self._project, self._dataset) or {}
        cls_mode = info.get("label_fmt", "") == "cls"
        self._cls_mode = cls_mode
        # 分类模式只保留 数据/设备 两个下拉，隐藏整个「测试参数」分组
        for row in (0, 1, 2):
            self._set_form_row_visible("form_param", row, not cls_mode)
        self.ui.group_param_title.setVisible(not cls_mode)
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
        checked = self._checked_datasets()
        if not checked:
            MessageBox.warning(self, "测试", "请至少选择一个数据集")
            return
        cls_mode = getattr(self, "_cls_mode", False)
        if cls_mode:
            conf, iou, output_labels = 0.5, 0.5, False
        else:
            try:
                conf = float(self.ui.confidence_txt.text() or "0.5")
                iou = float(self.ui.iou_treshold_txt.text() or "0.5")
            except ValueError:
                MessageBox.warning(self, "测试", "置信度/iou阈值必须是数字")
                return
            output_labels = bool(self.ui.output_label_file_checkBox.isChecked())
        model_path = self._model_path
        if not model_path or not os.path.exists(model_path):
            MessageBox.warning(self, "测试", "模型文件不存在，请重新选择")
            return
        # 多个数据集一起测:图像目录逐个展开,标签目录与图像目录按索引配对
        items = []
        total = 0
        base_cls = None
        base_labeled = None
        for proj, ds_name in checked:
            binding = self.app.db.get_dataset_import(proj, ds_name) or {}
            image_paths = binding.get("image_paths") or (
                [binding.get("image_path")] if binding.get("image_path") else [])
            if not image_paths:
                MessageBox.warning(
                    self, "测试", "数据集 {}/{} 未导入图像".format(proj, ds_name))
                return
            label_paths = binding.get("label_paths") or (
                [binding.get("label_path")] if binding.get("label_path") else [])
            this_cls = binding.get("label_fmt", "") == "cls"
            this_labeled = int(binding.get("labeled") or 0) > 0
            if base_cls is None:
                base_cls, base_labeled = this_cls, this_labeled
            elif this_cls != base_cls:
                MessageBox.warning(
                    self, "测试",
                    "分类数据集与检测/分割数据集不能同时测试: {}/{}".format(proj, ds_name))
                return
            elif this_labeled != base_labeled:
                MessageBox.warning(
                    self, "测试",
                    "已标注与未标注的数据集不能同时测试: {}/{}".format(proj, ds_name))
                return
            for i, image_path in enumerate(image_paths):
                items.append({
                    "project": proj, "dataset": ds_name,
                    "image_path": image_path,
                    "label_path": (label_paths[i] if i < len(label_paths)
                                   else (label_paths[0] if label_paths else "")),
                })
            total += int(binding.get("total") or 0)
        has_label = bool(base_labeled)
        device = self.ui.test_device_combo.currentData() or "cuda"
        report_dir = ""
        if model_path:
            report_dir = os.path.join(
                os.path.dirname(os.path.abspath(model_path)),
                "test_" + time.strftime("%Y%m%d_%H%M%S"))
        # 配置写入临时文件,TestWorker 子进程读它
        fd, cfg_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        cfg = {
            "model_path": model_path, "items": items,
            "iou_threshold": iou, "confidence": conf,
            "has_label": has_label, "device": device,
            "total": total, "output_labels": output_labels,
            "task": "classify" if cls_mode else "",
            "report_dir": report_dir,
            "_cfg_path": cfg_path,
        }
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        write_log(
            "[test] 启动测试 worker: model={} 数据集={} 图像目录={} device={} cfg={}".format(
                model_path, ["{}/{}".format(p, d) for p, d in checked],
                [it["image_path"] for it in items], device, cfg_path))
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
        # 倒计时结束/人工点确定, 关闭模型列表窗口回首页
        md = getattr(self.app, "_model_dialog", None)
        if md is not None:
            md.accept()

    def _fill_label_stats(self, res):
        """
        把该模型训练时勾选的数据集（训练集+验证集）标注分布塞进 res。
        """
        pairs = []
        for field in ("dataset", "val_dataset"):
            for tok in (x.strip()
                        for x in str(self._record.get(field, "")).split(",")):
                if "/" in tok:
                    proj, _, name = tok.partition("/")
                    proj, name = proj.strip(), name.strip()
                    if proj and name:
                        pairs.append((proj, name))
        if not pairs:
            for ds in res.get("datasets") or []:
                proj, name = ds.get("project"), ds.get("dataset")
                if proj and name:
                    pairs.append((proj, name))
        counts, colors = {}, {}
        for proj, name in pairs:
            for k, v in (self.app.db.get_dataset_label_counts(proj, name)
                         or {}).items():
                counts[k] = counts.get(k, 0) + v
            if not colors:
                colors = self.app.db.get_dataset_labels(proj, name)
        if counts:
            res["label_stats"] = counts
        if colors:
            res["label_colors"] = colors

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
            self._fill_label_stats(res)
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