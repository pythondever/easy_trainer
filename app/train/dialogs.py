# -*- coding: utf-8 -*-
"""训练对话框(统一):任务类型下拉 检测/分割/分类,数据集跨项目选择."""

import os
import json
import traceback
import uuid
from datetime import datetime
from importlib.util import find_spec

from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtCore import QT_TRANSLATE_NOOP
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import (QDialog, QLabel, QFileDialog, QComboBox,
                               QPushButton, QVBoxLayout)
from PySide6.QtGui import QStandardItem

from app.widgets.combo_utils import style_combo
from app.widgets.dialog_buttons import apply_icon
from app.widgets.message_box import MessageBox
from app.widgets.multi_combo import install_multi_combo
from app.widgets.status_style import task_text
from app.widgets.model_manager_dialog import ensure_weight
from app.core import i18n
from app.core.db import get_paths
from app.core.log import write_log
from app.train.data_prep import timestamp_dir
from ui.train import Ui_TrainDialog

CONTROL_H = 36
# 探测设备期间下拉里的占位文本: 常量存原文, 用的时候走 QC.translate
PROBING_TEXT = QT_TRANSLATE_NOOP("TrainDialog", "正在检测显卡...")


def collect_dataset_labels(db, ds_pairs):
    """勾选数据集的标签并集(跨项目,训练启动时已知,指标界面下拉无需等验证)."""
    labels = set()
    for proj, name in ds_pairs:
        try:
            for lb in db.get_dataset_labels(proj, name):
                labels.add(str(lb))
        except Exception:
            pass
    return sorted(labels)


# 各任务 best 权重的文件名: rf-detr 用 ema track, 分类 runner 只有单一 best
BEST_CKPT = {"classify": "checkpoint_best.pth"}
BEST_CKPT_DEFAULT = "checkpoint_best_ema.pth"
BEST_CKPT_CNN = os.path.join("weights", "best.pt")


def best_ckpt_name(config):
    """训练期间先按这个填记录的 model_path, 跑完由 runner 的 RESULT 覆盖.

    分类也带 family="cnn", 但它的产物名不随架构变, 所以先按任务判.
    """
    task = config.get("task", "")
    if task == "classify":
        return BEST_CKPT["classify"]
    if config.get("family") == "cnn":
        return BEST_CKPT_CNN
    return BEST_CKPT_DEFAULT


def make_train_record(config, db, project_fallback=""):
    """按 config 组装训练记录(供训练界面回填); 不落库, 调用方在启动成功后写入.

    与 TrainDialog 解耦: 队列出队时没有对话框实例, 也走这个函数.
    """
    ds_pairs = [(d["project"], d["dataset_name"]) for d in config["datasets"]
                if d.get("split") == "train"]
    val_pairs = [(d["project"], d["dataset_name"]) for d in config["datasets"]
                 if d.get("split") == "val"]
    ds_names = ", ".join("{}/{}".format(p, d) for p, d in ds_pairs)
    val_names = ", ".join("{}/{}".format(p, d) for p, d in val_pairs)
    # dataset_info 包含训练集+验证集," / " 分隔两组;组内多个用逗号
    dataset_info = (ds_names + " / " + val_names) if val_names else ds_names
    first_proj = ds_pairs[0][0] if ds_pairs else project_fallback
    return {
        "id": str(uuid.uuid4()),
        "project": first_proj,
        "task": config.get("task", ""),
        "dataset": ds_names,
        "val_dataset": val_names,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": "",
        "duration": "",
        "model_size": config.get("model_size", ""),
        "family": config.get("family", ""),
        "map50": "",
        "img_size": config.get("img_size", ""),
        "model_path": os.path.join(
            config.get("timestamp_dir", ""), best_ckpt_name(config)),
        "dataset_info": dataset_info,
        "output_path": config.get("out_root", ""),
        "epochs": config.get("epochs", ""),
        "batch_size": config.get("batch_size", ""),
        "lr": config.get("lr", ""),
        "grad_accum": config.get("grad_accum", ""),
        "num_workers": config.get("num_workers", ""),
        "early_stop": config.get("early_stop", ""),
        "optimizer": config.get("optimizer", ""),
        "metrics_file": "",   # 指标外置为 metrics/<id>.json, 记录里只留文件名
        "metrics_epochs": 0,
        "labels": collect_dataset_labels(db, ds_pairs),
        "device": config.get("device", ""),
    }


def params_to_record(params):
    """队列项参数快照 → 训练对话框 preset_record 的字段格式(用于"编辑"回填)."""
    def _names(pairs):
        return ", ".join("{}/{}".format(p[0], p[1]) for p in (pairs or []))
    return {
        "task": params.get("task", ""),
        "dataset": _names(params.get("train_ds")),
        "val_dataset": _names(params.get("val_ds")),
        "epochs": params.get("epochs", ""),
        "batch_size": params.get("batch_size", ""),
        "lr": params.get("lr", ""),
        "grad_accum": params.get("grad_accum", ""),
        "num_workers": params.get("num_workers", ""),
        "early_stop": params.get("early_stop", ""),
        "img_size": params.get("img_size", ""),
        "model_size": params.get("architecture", ""),
        "family": params.get("family", ""),
        "device": params.get("device", ""),
        "optimizer": params.get("optimizer", ""),
        "output_path": params.get("out_root", ""),
    }


def check_dataset_imported(name, info):
    """
    校验数据集已导入且路径有效(防止未导入/加载中的数据集直接训练).
    分类数据集(fmt=="cls")标签即子文件夹名,无需单独 label_path 目录,
    所以跳过标签目录存在性检查.
    """
    img = info.get("image_path", "")
    lab = info.get("label_path", "")
    fmt = info.get("label_fmt", "")
    if not img or not os.path.isdir(img):
        raise ValueError(QC.translate(
            "TrainDialog",
            "数据集\"{}\"尚未导入图像或路径无效, 请先导入该数据集再训练")
            .format(name))
    if fmt == "cls":
        return
    if not lab or not os.path.isdir(lab):
        raise ValueError(QC.translate(
            "TrainDialog",
            "数据集\"{}\"尚未导入标签或路径无效, 请先导入该数据集再训练")
            .format(name))


def _unique_ts_dir(out_root, ts):
    """时间戳只到秒: 队列里上一个任务秒退时下一个会撞名, 两个训练的输出会互相覆盖."""
    path = os.path.join(out_root, ts)
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
        return path
    i = 2
    while os.path.isdir("{}_{}".format(path, i)):
        i += 1
    path = "{}_{}".format(path, i)
    os.makedirs(path, exist_ok=True)
    return path


def make_train_config(db, params):
    """把参数快照落盘成子进程配置. 队列出队与开始训练共用同一条路径.

    timestamp_dir 只在这里算一次: 训练记录的 model_path 必须复用它,
    否则两次调用跨秒会指向一个不存在的目录.
    """
    task = params.get("task") or "detect"
    out_root = (params.get("out_root") or "").strip()
    if not out_root:
        raise ValueError(QC.translate("TrainDialog", "请先选择输出路径"))
    os.makedirs(out_root, exist_ok=True)
    datasets = []
    for split, pairs in (("train", params.get("train_ds") or []),
                         ("val", params.get("val_ds") or [])):
        for pair in pairs:
            proj, name = pair[0], pair[1]
            info = db.get_dataset_import(proj, name)
            check_dataset_imported(name, info)
            fmt = info.get("label_fmt", "")
            # 入队后数据集可能被重新导入成别的格式, 出队时再校验一次
            # (队列可能挂着几个小时, 中间改了数据集这里才发现)
            if task == "classify" and fmt != "cls":
                raise ValueError(QC.translate(
                    "TrainDialog",
                    "数据集\"{}/{}\"不是分类数据集(标签格式={}), 无法训练图像分类")
                    .format(proj, name, fmt or QC.translate("TrainDialog", "未知")))
            if task != "classify" and fmt == "cls":
                raise ValueError(QC.translate(
                    "TrainDialog",
                    "数据集\"{}/{}\"是分类数据集, 无法训练{}任务")
                    .format(proj, name, task_text(task)))
            datasets.append({
                "dataset_name": name, "project": proj, "split": split,
                "image_path": info.get("image_path", ""),
                "label_path": info.get("label_path", ""),
                "image_paths": get_paths(info, "image"),
                "label_paths": get_paths(info, "label"),
                "fmt": fmt,
                "label_ids": db.get_dataset_label_ids(proj, name),
            })
    if not any(d["split"] == "train" for d in datasets):
        raise ValueError(QC.translate("TrainDialog", "请至少选择一个训练集数据集"))
    if not any(d["split"] == "val" for d in datasets):
        raise ValueError(QC.translate("TrainDialog", "请至少选择一个验证集数据集"))
    ts_dir = _unique_ts_dir(out_root, timestamp_dir())
    architecture = params.get("architecture") or "nano"
    if task == "classify":
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
        "family": params.get("family") or "transformer",
        "model_size": params.get("architecture") or "nano",
        "device": params.get("device") or "",
        "epochs": params.get("epochs", 100),
        "batch_size": params.get("batch_size", 8),
        "num_workers": params.get("num_workers", 8),
        "optimizer": params.get("optimizer") or "adamw",
        # 早停: >0 启用(值即 patience), <=0 禁用
        "early_stop": params.get("early_stop", 20),
        "lr": params.get("lr", 1e-4),
        "img_size": params.get("img_size", 640),
        "datasets": datasets,
        # 子进程按它装翻译, 少了这行日志只会出中文
        "language": i18n.current(),
    }
    # 分类不传梯度累积(runner 不消费该字段),检测/分割才传
    if task != "classify":
        config["grad_accum"] = params.get("grad_accum", 4)
    cfg_path = os.path.join(ts_dir, "train_config.json")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False)
    config["_cfg_path"] = cfg_path
    return config


def params_summary(params):
    """队列项的一行摘要文本(任务/网络/数据集)."""
    task = params.get("task", "")
    shown = task_text(task)
    # 带项目名:不同项目下常有同名数据集(如 test1/train, test2/train)
    names = ["{}/{}".format(p[0], p[1]) for p in (params.get("train_ds") or [])]
    ds = ", ".join(names) if names else QC.translate("TrainDialog", "未选数据集")
    return "{} · {} · {}".format(shown, params.get("architecture", ""), ds)


class _TrainStartDialog(QDialog):
    """训练/测试启动提示: 确认按钮带倒计时, 5s 后自动确认; 手动点击立即确认并停止计时."""

    def __init__(self, seconds=5, parent=None, title=None, message=None):
        super().__init__(parent)
        # 默认参数在 installTranslator 之前求值, 中文默认值要延后到这里取
        title = title or self.tr("训练即将开始")
        message = message or title
        self.setWindowTitle(title)
        self._left = seconds
        self.setMinimumWidth(280)
        layout = QVBoxLayout(self)
        label = QLabel(message)
        label.setObjectName("dialogConfirmPrompt")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self._btn = QPushButton(self.tr("确认({})").format(seconds))
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
            self._btn.setText(self.tr("确认({})").format(self._left))

    def _confirm(self):
        self._timer.stop()
        self.accept()

    def closeEvent(self, event):
        self._timer.stop()
        super().closeEvent(event)


_DEVICES = None


def collect_devices():
    """
    [(显示名, 设备串)]: 列表显示 GPU 型号, 实际下发的是 cuda:0 这类设备串.
    torch 延迟到这里导入: 本模块被 queue_mixin 在启动时引入, 带着 torch 会让
    GUI 启动多花约 2s(耗时全在 import 本身). 结果缓存, 同一进程只探测一次.
    """
    global _DEVICES
    if _DEVICES is None:
        try:
            import torch
        except ImportError:
            torch = None
        if torch is None or not torch.cuda.is_available():
            _DEVICES = [("CPU", "CPU")]
        else:
            _DEVICES = []
            for i in range(torch.cuda.device_count()):
                try:
                    name = torch.cuda.get_device_name(i)
                    # 下拉宽度放不下全名, 而 ElideLeft 先吃掉的正是前缀, 反倒把型号挤没
                    name = name.removeprefix("NVIDIA ")
                    total = torch.cuda.get_device_properties(i).total_memory
                    text = "{} ({:.0f} GB)".format(name, total / 1024 ** 3)
                except Exception:
                    text = "GPU {}".format(i)
                _DEVICES.append((text, "cuda:{}".format(i)))
            _DEVICES.append(("CPU", "CPU"))
    return list(_DEVICES)


class _DeviceProbe(QThread):
    """后台探测显卡. 同步探测要等 import torch(约 2s), 弹窗会晚 2s 才出现."""

    ready = Signal(list)

    def run(self):
        try:
            self.ready.emit(collect_devices())
        except Exception:
            self.ready.emit([("CPU", "CPU")])


_PROBES = []                    # 运行中的探测线程, 防止被 GC


def fill_device_items(combo, devices):
    combo.clear()
    for text, value in devices:
        combo.addItem(text, value)
        combo.setItemData(combo.count() - 1, text, Qt.ToolTipRole)


def fill_device_combo_async(dialog, combo, start_button):
    """设备下拉先填占位值, 后台探测完回调 dialog._on_devices_ready(devices).

    就绪前禁掉下拉与开始按钮, 免得占位值 CPU 被当成用户选择跑出去.
    """
    combo.clear()
    combo.addItem(QC.translate("TrainDialog", PROBING_TEXT), "CPU")
    if _DEVICES is not None:        # 本进程已探测过, 不用再起线程
        dialog._on_devices_ready(_DEVICES)
        return
    combo.setEnabled(False)
    start_button.setEnabled(False)
    # 前一个弹窗关掉后探测可能还在跑, 搭它的车, 免得再导一次 torch
    probe = next((p for p in _PROBES if p.isRunning()), None)
    if probe is None:
        probe = _DeviceProbe()
        _PROBES.append(probe)
        probe.finished.connect(
            lambda: _PROBES.remove(probe) if probe in _PROBES else None)
        probe.start()
    probe.ready.connect(dialog._on_devices_ready)
    dialog._device_probe = probe


def detach_device_probe(dialog):
    """关窗时摘掉探测回调. 线程让它自己跑完, 关窗不该等它那 2s."""
    probe = getattr(dialog, "_device_probe", None)
    if probe is None or not probe.isRunning():
        return
    try:
        probe.ready.disconnect(dialog._on_devices_ready)
    except (RuntimeError, TypeError):
        pass


class TrainDialog(QDialog):
    """统一训练对话框: 任务类型(检测/分割/分类) + 跨项目数据集选择."""

    # 各任务默认参数:epochs / lr / img_size / grad_accum(分类禁用)
    TASK_DEFAULTS = {
        "detect": (100, 1e-4, 640, 4),
        "segment": (100, 1e-4, 636, 4),
        "classify": (30, 0.001, 224, 4),
    }
    TASK_TIPS = {
        "detect": QT_TRANSLATE_NOOP(
            "TrainDialog", "目标检测推荐图像尺寸: 640(可设为 32 的倍数如 640/672)"),
        "segment": QT_TRANSLATE_NOOP(
            "TrainDialog", "图像分割推荐尺寸: 636(必须为 12 的倍数, 如 636/648/660)"),
        "cnn_segment": QT_TRANSLATE_NOOP(
            "TrainDialog", "CNN 分割推荐尺寸: 640(需为 32 的倍数)"),
        "classify": QT_TRANSLATE_NOOP(
            "TrainDialog", "图像分类推荐尺寸: 224(小图用 224, 较大图可到 256)"),
    }
    # 输入框右侧的倍数约束, 写不下整句 tooltip 就靠这几个字
    IMG_NOTE = {
        "detect": QT_TRANSLATE_NOOP("TrainDialog", "32 的倍数"),
        "segment": QT_TRANSLATE_NOOP("TrainDialog", "12 的倍数"),
        "classify": QT_TRANSLATE_NOOP("TrainDialog", "建议 224"),
        # 636 那个 12 的倍数来自 rf-detr 的 patch_size*num_windows, CNN 没有这约束
        "cnn_segment": QT_TRANSLATE_NOOP("TrainDialog", "32 的倍数"),
    }
    # 切架构时要跟着换的推荐值; 没列的沿用任务默认(分类只有 resnet, 不参与)
    ARCH_DEFAULTS = {
        "transformer": {},
        "cnn": {"lr": 0.01, "batch": 16, "optimizer": "sgd", "img_size": 640},
    }

    def __init__(self, app, project="", dataset="", preset_record=None):
        """project/dataset 可为空(独立入口);preset_record 传入时按记录回填(模型界面训练按钮)."""
        super().__init__(app)
        self.app = app
        self.project = project
        self.dataset = dataset
        self.ui = None
        self._int_fields = []      # [(控件, 名称, 默认值, 是否必填)]
        self._float_fields = []    # [(控件, 名称, 默认值, 是否必填)]
        self._combo_filters = []
        self._preset_record = preset_record
        self.queue_edit_qid = None   # 队列面板"编辑"时回填用: 保存即更新该队列项
        self._pending_device = None   # 设备列表探测期间没回填上的设备串
        self._build()

    def closeEvent(self, event):
        detach_device_probe(self)
        super().closeEvent(event)

    # ---------- 初始化 ----------
    def _build(self):
        self.ui = Ui_TrainDialog()
        self.ui.setupUi(self)
        self._tag_task_combo()
        self.setWindowTitle(self.tr("训练"))
        self._define_fields()
        self._setup_validators()
        self._fill_defaults()
        self._fix_heights()
        self._connect()
        self.resize(740, max(560, self.sizeHint().height()))

    def _tag_task_combo(self):
        """任务下拉挂 itemData. 按文本找的话, 界面切英文后 _task() 会全部落空."""
        for i, code in enumerate(("detect", "segment", "classify")):
            self.ui.task_combo.setItemData(i, code)

    def _task(self):
        return self.ui.task_combo.currentData() or "detect"

    def _task_text(self):
        return self.ui.task_combo.currentText()

    def _fix_heights(self):
        """统一控件高度(宽度交给网格拉伸), 数值输入框文字居中."""
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
                           "arch_combo", "device_combo", "img_size_comboBox",
                           "optimizer_comboBox"):
            combo = getattr(self.ui, combo_name, None)
            if combo is not None:
                combo.setFixedHeight(CONTROL_H)
        # 下拉的 sizeHint 按最长条目算, GPU 全名会把整列撑宽, 改成按固定字符数估宽
        for name in ("dataset_combo", "val_combo", "device_combo"):
            combo = getattr(self.ui, name, None)
            if combo is not None:
                combo.setSizeAdjustPolicy(
                    QComboBox.SizeAdjustPolicy
                    .AdjustToMinimumContentsLengthWithIcon)
                combo.setMinimumContentsLength(12)
        self._align_grid_labels()

    def _align_grid_labels(self):
        """网格的左右两组标签列各自同宽, 否则两侧输入框左边界对不齐."""
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
        # name 会拼进校验提示(""批次"不能为空"), 所以跟着界面语言走
        self._int_fields = [
            (self.ui.batch_size_line_txt, self.tr("批次"), 4, True),
            (self.ui.grad_accum_line_txt, self.tr("梯度累积"), 4, True),
            (self.ui.epochs_line_txt, self.tr("轮次"), 100, True),
            (self.ui.batch_size_line_txt_2, self.tr("线程数"), 4, True),
            (self.ui.img_size_line_txt, self.tr("图像尺寸"), 640, True),
            (self.ui.early_stop_line_txt, self.tr("早停"), 20, False),
        ]
        self._float_fields = [
            (self.ui.lr_line_txt, self.tr("学习率"), 1e-4, True),
        ]

    def _connect(self):
        self.ui.start_train.clicked.connect(self._on_start_train)
        self.ui.add_queue_btn.clicked.connect(self._on_add_to_queue)
        self.ui.select_output_path_btn.clicked.connect(self._select_output_dir)
        apply_icon(self.ui.cancel_btn, self.tr("取消"))
        self.ui.cancel_btn.clicked.connect(self.reject)

    # ---------- 填充 ----------
    def _style_all_combos(self):
        # 多选下拉的编辑区自己画标签(见 _setup_multi_combo), 不套这里的居中和点击展开
        for name in ("task_combo", "network_combo", "device_combo", "arch_combo",
                     "img_size_comboBox", "optimizer_comboBox"):
            combo = getattr(self.ui, name, None)
            if combo is not None:
                style_combo(combo, self._combo_filters)

    def _setup_multi_combo(self, combo, placeholder=None):
        install_multi_combo(combo, placeholder)
        combo.model().itemChanged.connect(lambda *_: self._update_multi_label(combo))
        combo.activated.connect(lambda _i: self._update_multi_label(combo))
        return combo

    def _fill_dataset_multi(self, combo, checked_names):
        """
        跨项目列出所有数据集(文本"项目/数据集",data=(项目,数据集)),checked_names 内默认勾选.
        数据源与首页项目树一致:先 get_projects() 拿项目名,再 get_datasets(name)
        拿该项目下数据集 - 不会列出已删除项目残留的孤儿数据集记录.
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
        """底部概要条: 勾了几个训练集/验证集, 总共多少张图, 能不能直接开训."""
        train = self._selected_datasets()
        val = self._selected_val_datasets()
        if not train:
            self.ui.summary_text.setText(self.tr("请选择训练集与验证集"))
            return
        total = 0
        labeled = 0
        for proj, name in train + val:
            info = self.app.db.get_dataset_import(proj, name) or {}
            total += int(info.get("total") or 0)
            if int(info.get("labeled") or 0) > 0:
                labeled += 1
        picked = len(train) + len(val)
        text = self.tr("训练集 {} 个 · 验证集 {} 个 · 共 {} 张图").format(
            len(train), len(val), total)
        if not val:
            tail = self.tr("未选择验证集")
        elif labeled == picked:
            tail = self.tr("已标注, 可直接训练")
        else:
            tail = self.tr("有 {} 个数据集尚未标注").format(picked - labeled)
        self.ui.summary_text.setText("{} · {}".format(text, tail))

    def _selected_datasets(self):
        """训练集(勾选的数据集)."""
        return self._selected_checked(self.ui.dataset_combo)

    def _selected_val_datasets(self):
        """验证集(勾选的数据集)."""
        return self._selected_checked(self.ui.val_combo)

    def _fill_defaults(self):
        self._style_all_combos()
        self._setup_multi_combo(self.ui.dataset_combo)
        self._setup_multi_combo(self.ui.val_combo, self.tr("请选择验证集"))
        self._fill_dataset_multi(self.ui.dataset_combo, [])
        self._fill_dataset_multi(self.ui.val_combo, [])
        self.ui.dataset_label.setText(self.tr("训练集"))
        self._fill_device_combo()
        self._center_combo_items(self.ui.task_combo)
        self._fill_arch_combo()
        self._fill_network_combo()
        self._fill_optimizer()
        self.ui.task_combo.setCurrentIndex(0)  # 默认检测
        self.ui.task_combo.currentIndexChanged.connect(self._on_task_changed)
        self.ui.arch_combo.currentIndexChanged.connect(self._on_arch_changed)
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
        # 还没探测完设备, 或已有训练在跑, 都先别让点开始
        self._sync_start_enabled()

    def _set_device(self, value):
        """设备下拉显示的是 GPU 型号, 回填得按 itemData 里的 cuda:0 找;
        历史记录存的是小写 cpu, 下拉数据是大写 CPU, 按忽略大小写兜底."""
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
        else:
            # 设备列表还在后台探测, 等就绪后再回填一次
            self._pending_device = str(value)

    def _device(self):
        data = self.ui.device_combo.currentData()
        if data:
            return str(data)
        return self.ui.device_combo.currentText() or "cpu"

    def _fill_device_combo(self):
        fill_device_combo_async(self, self.ui.device_combo, self.ui.start_train)

    def _on_devices_ready(self, devices):
        """后台探测完成: 填列表, 解禁, 把探测期间没铺上的设备回填上."""
        combo = self.ui.device_combo
        fill_device_items(combo, devices)
        combo.setEnabled(True)
        combo.setCurrentIndex(0)
        self._center_combo_items(combo)
        self._sync_start_enabled()
        if self._pending_device:
            pending, self._pending_device = self._pending_device, None
            self._set_device(pending)

    def _sync_start_enabled(self):
        """设备列表就绪且没有训练在跑, 才允许点开始."""
        btn = getattr(self.ui, "start_train", None)
        if btn is None:
            return
        busy = hasattr(self.app, "is_training") and self.app.is_training()
        ready = _DEVICES is not None
        btn.setEnabled(ready and not busy)
        if not ready:
            btn.setToolTip(QC.translate("TrainDialog", PROBING_TEXT))
        else:
            btn.setToolTip(self.tr("已有训练在进行中, 请先停止") if busy else "")

    def _fill_optimizer(self):
        """优化器下拉: 分类(resnet)与 CNN(YOLO) 推荐 sgd, 检测/分割的 detr 推荐 adamw."""
        combo = self.ui.optimizer_comboBox
        combo.clear()
        if self._task() == "classify":
            combo.addItems(["adamw", "sgd"])
            recommended = "sgd"
        elif self._arch() == "cnn":
            combo.addItems(["adamw", "sgd", "adam"])
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
        """下拉列表项文字居中(单选下拉:任务类型/网络/设备/优化器)."""
        model = combo.model()
        for i in range(model.rowCount()):
            it = model.item(i)
            if it is not None:
                it.setTextAlignment(Qt.AlignHCenter)

    def _on_task_changed(self):
        self.ui.task_badge.setText(self._task_text())
        self._apply_task_ui()

    def _fill_arch_combo(self):
        """架构下拉: 值放 itemData, 和任务下拉一样不吃界面语言的亏."""
        combo = self.ui.arch_combo
        combo.clear()
        for text, code in (("Transformer", "transformer"), ("CNN", "cnn")):
            combo.addItem(text, code)
        combo.setCurrentIndex(0)
        self._center_combo_items(combo)

    def _arch(self):
        return self.ui.arch_combo.currentData() or "transformer"

    def _on_arch_changed(self):
        self._apply_task_ui()

    def _apply_task_ui(self):
        """任务类型/架构切换: 按两者推荐填充参数, grad_accum 可用性, 型号项.

        首页进入是空表单,用户选择任务类型后由这里给出推荐值;
        模型界面回填(preset_record)时 _apply_record_params 会在其后覆盖为记录值.
        """
        task = self._task()
        epochs, lr, img, _ = self.TASK_DEFAULTS.get(task, (100, 1e-4, 640, 4))
        self._sync_arch_combo(task)
        over = {} if task == "classify" else self.ARCH_DEFAULTS.get(self._arch(), {})
        self.ui.grad_accum_line_txt.setEnabled(task != "classify")
        self.ui.epochs_line_txt.setText(str(epochs))
        self.ui.lr_line_txt.setText(str(over.get("lr", lr)))
        self.ui.img_size_line_txt.setText(str(over.get("img_size", img)))
        # 批次跟着架构走(CNN 显存占用比 detr 小得多), 所以是覆盖而不是"空才填"
        self.ui.batch_size_line_txt.setText(str(over.get("batch", 4)))
        if not self.ui.batch_size_line_txt_2.text().strip():
            self.ui.batch_size_line_txt_2.setText("4")
        if not self.ui.early_stop_line_txt.text().strip():
            self.ui.early_stop_line_txt.setText("20")
        if not self.ui.grad_accum_line_txt.text().strip():
            self.ui.grad_accum_line_txt.setText("4")
        self._fill_optimizer()
        self._fill_network_combo()
        self._setup_img_size_tip()

    def _sync_arch_combo(self, task):
        """分类只有 resnet(CNN) 一条路, 架构锁死; 锁的时候别触发联动, 否则覆盖回填值."""
        combo = self.ui.arch_combo
        combo.setEnabled(task != "classify")
        if task == "classify":
            idx = combo.findData("cnn")
            if idx >= 0:
                combo.blockSignals(True)
                combo.setCurrentIndex(idx)
                combo.blockSignals(False)

    def _restore_record(self, rec):
        """按指定训练记录回填全部字段(模型界面训练按钮)."""
        task = str(rec.get("task", "") or "")
        if task:
            idx = self.ui.task_combo.findData(task)
            if idx >= 0:
                self.ui.task_combo.setCurrentIndex(idx)
        # 老记录没有 family, 当年只有 rf-detr 一条路, 一律当 transformer
        arch = self.ui.arch_combo
        idx = arch.findData(str(rec.get("family") or "transformer"))
        arch.blockSignals(True)
        arch.setCurrentIndex(idx if idx >= 0 else 0)
        arch.blockSignals(False)
        self._apply_task_ui()
        train_names = [x.strip() for x in str(rec.get("dataset", "")).split(",") if x.strip()]
        val_names = [x.strip() for x in str(rec.get("val_dataset", "")).split(",") if x.strip()]
        if train_names:
            self._fill_dataset_multi(self.ui.dataset_combo, train_names)
        if val_names:
            self._fill_dataset_multi(self.ui.val_combo, val_names)
        self._apply_record_params(rec)

    def _apply_record_params(self, rec):
        """把训练记录参数回填到界面(控件按存在性防护)."""

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
        """型号档位: CNN 多一档 x-large(YOLO11 五档), 前四档两边同名同义."""
        combo = self.ui.network_combo
        combo.clear()
        if self._task() != "classify" and self._arch() == "cnn":
            combo.addItems(["nano", "small", "medium", "large", "x-large"])
        else:
            combo.addItems(["nano", "small", "medium", "large"])
        self._center_combo_items(combo)
        if self._task() == "classify":
            # 分类只有 resnet, 档位即 resnet18/34/50/101, 固定从头训练的那档
            combo.setCurrentIndex(0)

    def _setup_img_size_tip(self):
        key = self._img_key()
        self.ui.img_size_line_txt.setToolTip(self.tr(self.TASK_TIPS.get(key, "")))
        self.ui.img_note.setText(self.tr(self.IMG_NOTE.get(key, "")))

    def _img_key(self):
        """CNN 分割不吃 rf-detr 的 12 的倍数约束, 提示语单独一套."""
        if self._task() == "segment" and self._arch() == "cnn":
            return "cnn_segment"
        return self._task()

    # ---------- 校验 ----------
    def _setup_validators(self):
        for edit, _name, _default, _req in self._int_fields:
            edit.setValidator(QIntValidator(0, 999999, self))
        for edit, _name, _default, _req in self._float_fields:
            edit.setValidator(QDoubleValidator(0.0, 1.0, 8, self))

    def _validate(self):
        if not self._selected_datasets():
            return False, self.tr("请至少选择一个数据集")
        for edit, name, _default, required in self._int_fields:
            txt = edit.text().strip()
            if not txt and required:
                return False, self.tr("\"{}\"不能为空").format(name)
            if txt:
                try:
                    int(txt)
                except ValueError:
                    return False, self.tr("\"{}\"必须是整数(当前: {})").format(
                        name, txt)
        for edit, name, _default, required in self._float_fields:
            txt = edit.text().strip()
            if not txt and required:
                return False, self.tr("\"{}\"不能为空").format(name)
            if txt:
                try:
                    float(txt)
                except ValueError:
                    return False, self.tr("\"{}\"必须是数字(当前: {})").format(
                        name, txt)
        # 任务类型与数据集格式匹配校验(按导入时的 label_fmt 判断:cls=分类,其余=检测/分割)
        task = self._task()
        task_text = self._task_text()
        for proj, name in self._selected_datasets() + self._selected_val_datasets():
            fmt = self.app.db.get_dataset_import(proj, name).get("label_fmt", "")
            if task != "classify" and fmt == "cls":
                return False, self.tr(
                    "数据集\"{}/{}\"是分类数据集,无法训练{}任务").format(
                    proj, name, task_text)
            if task == "classify" and fmt != "cls":
                return False, self.tr(
                    "数据集\"{}/{}\"不是分类数据集(标签格式={}),"
                    "无法训练图像分类").format(proj, name, fmt or self.tr("未知"))
        return True, ""

    # ---------- 交互 ----------
    def _select_output_dir(self):
        d = QFileDialog.getExistingDirectory(
            self, self.tr("选择输出目录"), self.ui.output_line_txt.text())
        if d:
            self.ui.output_line_txt.setText(d)

    def _family_ready(self):
        """CNN 走 ultralytics 后端, 没装就别放行 —— 否则要等子进程起来才报 ImportError.

        用 find_spec 而不是 import: 后者在 GUI 线程里要花一两秒.
        """
        if self._task() == "classify" or self._arch() != "cnn":
            return True, ""
        if find_spec("ultralytics") is None:
            # 不点库名: 这条是给终端用户看的, 正常装好的包不该走到这里
            return False, self.tr(
                "当前安装缺少 CNN 架构所需的组件, 无法训练.\n请重新安装软件后再试")
        return True, ""

    def _on_start_train(self):
        if self.app.is_training():
            MessageBox.warning(
                self, self.tr("开始训练"),
                self.tr("当前已有训练在进行中, 请先停止!"))
            return
        ok, msg = self._validate()
        if not ok:
            write_log(QC.translate("TrainDialog", "参数校验未通过: {}").format(msg))
            MessageBox.warning(self, self.tr("参数校验"), msg)
            return
        ok, msg = self._family_ready()
        if not ok:
            MessageBox.warning(self, self.tr("开始训练"), msg)
            return
        # 权重缺失时拦下来: 子进程自己下是静默的, 日志里看不到进度
        if not ensure_weight(self, self.app.db, self._task(),
                             self.ui.network_combo.currentText() or "nano",
                             self._arch()):
            return
        params = self.collect_train_params()
        try:
            config = make_train_config(self.app.db, params)
        except Exception as exc:
            # 落盘失败时不写训练记录,避免模型界面留下没有结果的空行
            tb = traceback.format_exc()
            write_log(QC.translate(
                "TrainDialog",
                "训练启动失败: {}\n{}").format(exc, tb))
            MessageBox.critical(self, self.tr("训练启动失败"),
                                 "{}\n\n{}".format(exc, tb))
            return
        record = make_train_record(config, self.app.db, self.project)
        self.app.db.add_train_record(record)
        if not self.app.start_training(config, record["id"]):
            self.app.db.delete_train_record(record["id"])
            MessageBox.warning(self, self.tr("开始训练"),
                               self.tr("已有训练在进行中, 请先停止!"))
            return
        write_log(QC.translate(
            "TrainDialog",
            "开始训练: 任务类型={} 训练集={} 验证集={}").format(
            self._task_text(), record["dataset"], record["val_dataset"]))
        # 启动成功:立即关闭训练窗口 + 弹倒计时提示(5s 自动确认/点击立即确认)
        self.accept()
        _TrainStartDialog(parent=self).exec()

    def _on_add_to_queue(self):
        """把当前参数快照存入队列(不建目录, 不启动训练)."""
        ok, msg = self._validate()
        if not ok:
            MessageBox.warning(self, self.tr("参数校验"), msg)
            return
        ok, msg = self._family_ready()
        if not ok:
            MessageBox.warning(self, self.tr("加入队列"), msg)
            return
        # 入队时就查权重: 队列多半无人守着, 缺权重到出队时才发现在半夜
        if not ensure_weight(self, self.app.db, self._task(),
                             self.ui.network_combo.currentText() or "nano",
                             self._arch()):
            return
        params = self.collect_train_params()
        if not params["out_root"]:
            MessageBox.warning(self, self.tr("加入队列"),
                               self.tr("请先选择输出路径"))
            return
        for proj, name in params["train_ds"] + params["val_ds"]:
            info = self.app.db.get_dataset_import(proj, name)
            try:
                check_dataset_imported(name, info)
            except ValueError as exc:
                MessageBox.warning(self, self.tr("加入队列"), str(exc))
                return
        if self.queue_edit_qid:
            # 队列面板的"编辑": 保存即覆盖原队列项, 不新增
            if self.app.queue_update_params(self.queue_edit_qid, params):
                MessageBox.information(self, self.tr("队列"),
                                       self.tr("已更新该队列任务的参数"))
                self.accept()
            return
        try:
            item = self.app.enqueue_train(params)
        except Exception as exc:
            MessageBox.critical(self, self.tr("加入队列失败"),
                                 "{}".format(exc))
            return
        write_log(QC.translate(
            "TrainDialog",
            "加入训练队列: {} | {}").format(item["name"], item["qid"]))
        MessageBox.information(
            self, self.tr("加入队列"),
            self.tr("已加入队列(第 {} 个), 可在首页\"队列\"中查看或启动.")
            .format(item["order"] + 1))
        self.accept()

    def collect_train_params(self):
        """纯收集: 只读 UI 与 db, 不建目录, 不落盘(入队与开始训练共用)."""
        return {
            "task": self._task(),
            "architecture": self.ui.network_combo.currentText() or "nano",
            "family": self._arch(),
            "device": self._device(),
            "epochs": self.param_int(self.ui.epochs_line_txt, 100),
            "batch_size": self.param_int(self.ui.batch_size_line_txt, 8),
            "num_workers": self.param_int(self.ui.batch_size_line_txt_2, 8),
            "optimizer": self.ui.optimizer_comboBox.currentText() or "adamw",
            "lr": self.param_float(self.ui.lr_line_txt, 1e-4),
            "img_size": self._img_size(),
            "early_stop": self.param_int(self.ui.early_stop_line_txt, 20),
            "grad_accum": self.param_int(self.ui.grad_accum_line_txt, 4),
            "out_root": self.ui.output_line_txt.text().strip(),
            "train_ds": [list(x) for x in self._selected_datasets()],
            "val_ds": [list(x) for x in self._selected_val_datasets()],
        }

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
