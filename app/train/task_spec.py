# -*- coding: utf-8 -*-
"""
训练任务的规格基类: 各任务自己的配置构建与界面差异点.

原先这些差异以 if task == "xxx" 的形式散在 dialogs.py 里(架构名映射, 权重
文件名, 数据集格式要求, 尺寸步长, 型号档位, 优化器, 置灰项...), 现在收进各
任务的 *_common 模块, dialogs 只按任务取一份规格来查.

分层约束: 这些 *_common 模块训练子进程也会 import(见 ad_common / ocr_common
的说明), 所以本文件不带 PySide6 / torch / numpy 依赖. 文案上的
QT_TRANSLATE_NOOP 是本文件里的同名空函数: pyside6-lupdate 是按函数名抽取的,
名字对得上就能进 .ts, 不必为了几条提示把 QtCore 拖进子进程.
"""

import os


def QT_TRANSLATE_NOOP(context, text):
    return text


# 数据集与任务对不上时的文案. 界面预检和落盘前复检走同一套, 措辞只留一份
NOT_CLS = QT_TRANSLATE_NOOP(
    "TrainDialog", "数据集\"{}/{}\"不是分类数据集(标签格式={}), 无法训练{}")
IS_CLS = QT_TRANSLATE_NOOP(
    "TrainDialog", "数据集\"{}/{}\"是分类数据集, 无法训练{}任务")
NO_TEXT = QT_TRANSLATE_NOOP(
    "TrainDialog", "数据集\"{}/{}\"没有文本标注, 无法训练{}")
UNKNOWN = QT_TRANSLATE_NOOP("TrainDialog", "未知")


class TaskSpec:
    """一个任务的差异点集合; 缺省实现对应"检测"这条 rf-detr 主线."""

    code = ""
    # (轮次, 学习率, 图像尺寸, 梯度累积)
    defaults = (100, 1e-4, 640, 4)
    # 非空表示一次训练要拆成几段排队(字符检测的检测段 + 识别段)
    split_stages = ()
    # 本任务用不上的控件: 留着可填就是骗人
    disabled_fields = ()

    # ---------- 落盘配置 ----------
    def resolve_architecture(self, raw):
        """界面上的档位名 → 写进配置的架构名."""
        return raw or "nano"

    def resolve_family(self, raw):
        return raw or "transformer"

    def uses_grad_accum(self):
        return True

    def checkpoint_name(self, family):
        """训练期间先按这个填记录的 model_path, 跑完由 runner 的 RESULT 覆盖."""
        if family == "cnn":
            return os.path.join("weights", "best.pt")
        return "checkpoint_best_ema.pth"

    def dataset_problem(self, proj, name, info, task_label, tr):
        """数据集跟本任务对不上时返回给用户看的文案, 对得上返回 None."""
        if info.get("label_fmt", "") == "cls":
            return tr(IS_CLS).format(proj, name, task_label)
        return None

    # ---------- 界面 ----------
    def img_tip(self, arch):
        return ""

    def img_note(self, arch):
        return ""

    def img_block(self, arch, network):
        """图像尺寸必须整除的步长; 无约束返回 0."""
        return 0

    def arch_selectable(self, arch):
        """网络架构下拉能不能改: 只有一条路的任务锁死."""
        return True

    def arch_forced(self):
        """锁死时的架构代号; 可改则返回 None."""
        return None

    def arch_overrides(self, arch):
        """切架构要跟着换的推荐值: CNN 显存占用比 detr 小得多, 批次能开大."""
        return {} if arch != "cnn" else {
            "lr": 0.01, "batch": 16, "optimizer": "sgd", "img_size": 640}

    def network_items(self, arch, tr):
        """型号下拉的 (显示名, itemData); data 为 None 时按显示名取值."""
        items = ["nano", "small", "medium", "large"]
        if arch == "cnn":
            items.append("x-large")
        return [(text, None) for text in items]

    def optimizer_options(self, arch):
        """(候选列表, 推荐项)."""
        return (["adamw", "sgd", "adam"], "sgd" if arch == "cnn" else "adamw")

    def disabled_tooltip(self):
        return ""

    def epochs_policy(self, network, keep_value):
        """轮次的 (可用, 要填的文本或 None, 提示)."""
        return (True, None, "")

    def aug_supported(self):
        """数据增强的代号串只有检测/分割的 runner 会展开."""
        return False

    def needs_cnn_runtime(self, arch):
        """当前架构是否要 ultralytics(CNN 那条后端)."""
        return arch == "cnn"

    def accepts_dataset_type(self, dataset_type):
        """数据集下拉里要不要列这一条: 字符检测只列打过 ocr 标记的."""
        return dataset_type != "ocr"


class NeedsClsSpec(TaskSpec):
    """只能吃分类数据集(cls, 标签即子文件夹名)的任务: 分类与异常检测同源."""

    def dataset_problem(self, proj, name, info, task_label, tr):
        fmt = info.get("label_fmt", "")
        if fmt != "cls":
            return tr(NOT_CLS).format(proj, name, fmt or tr(UNKNOWN), task_label)
        return None
