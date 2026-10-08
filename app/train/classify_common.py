# -*- coding: utf-8 -*-
"""分类任务的规格.

只被 dialogs 在主进程读, 所以这里不能 import torch —— 分类的模型构造在
classify_model.py, 那份才是子进程用的.
"""

from app.train.task_spec import QT_TRANSLATE_NOOP, NeedsClsSpec

# 档位 → resnet 深度; 分类固定 from scratch 训练那一档
ARCHS = {"nano": "resnet18", "small": "resnet34",
         "medium": "resnet50", "large": "resnet101"}


class ClassifySpec(NeedsClsSpec):
    code = "classify"
    defaults = (30, 0.001, 224, 4)

    def resolve_architecture(self, raw):
        return ARCHS.get(raw or "", "resnet18")

    def checkpoint_name(self, family):
        """分类的产物名不随架构变, 所以按任务判, 不看 family."""
        return "checkpoint_best.pth"

    def img_tip(self, arch):
        return QT_TRANSLATE_NOOP(
            "TrainDialog", "图像分类推荐尺寸: 224(小图用 224, 较大图可到 256)")

    def img_note(self, arch):
        return QT_TRANSLATE_NOOP("TrainDialog", "建议 224")

    def arch_selectable(self, arch):
        return False

    def arch_forced(self):
        return "cnn"

    def arch_overrides(self, arch):
        """分类只有 resnet 一条路, 不吃 CNN 那套(它不走 ultralytics)."""
        return {}

    def network_items(self, arch, tr):
        return [(text, None) for text in ARCHS]

    def optimizer_options(self, arch):
        return (["adamw", "sgd"], "sgd")

    def needs_cnn_runtime(self, arch):
        return False


SPEC = ClassifySpec()
