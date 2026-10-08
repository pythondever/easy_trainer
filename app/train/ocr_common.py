# -*- coding: utf-8 -*-
"""
OCR 架构表: 训练对话框在主进程读它, 所以这里不能 import doctr.
"""

from app.train.task_spec import (
    QT_TRANSLATE_NOOP, NO_TEXT, TaskSpec)


OCR_MODELS = (
    ("nano", "db_mobilenet_v3_large", "crnn_mobilenet_v3_small"),
    ("small", "linknet_resnet18", "crnn_mobilenet_v3_small"),
    ("medium", "db_resnet34", "crnn_mobilenet_v3_large"),
    ("large", "db_resnet50", "crnn_vgg16_bn"),
)

# task 字段的三种取值: 下拉上是 ocr, 落到训练记录里被拆成检测/识别两条
OCR_TASKS = ("ocr", "ocr_det", "ocr_rec")
DET_TASK = "ocr_det"
RECO_TASK = "ocr_rec"


def model_codes():
    return [m[0] for m in OCR_MODELS]


def split_arch(code):
    """代号 → (检测架构, 识别架构); 认不出来时按表里第一条兜底."""
    for m in OCR_MODELS:
        if m[0] == code:
            return m[1], m[2]
    return OCR_MODELS[0][1], OCR_MODELS[0][2]


def is_ocr(task):
    return str(task or "") in OCR_TASKS


def stage_of(task, code):
    """某一段训练实际要用的架构: 记录里的 task 决定取检测段还是识别段."""
    det, reco = split_arch(code)
    return reco if str(task or "") == RECO_TASK else det


class OcrSpec(TaskSpec):
    """字符检测: 一次训练拆成检测段与识别段两段排队, 型号是架构代号."""

    code = "ocr"
    defaults = (50, 1e-4, 1024, 4)
    split_stages = (DET_TASK, RECO_TASK)

    def resolve_family(self, raw):
        return "ocr"

    def img_tip(self, arch):
        return QT_TRANSLATE_NOOP(
            "TrainDialog",
            "字符检测推荐尺寸: 1024(需为 {} 的倍数); 识别段固定 32x128, 不受此项影响")

    def img_block(self, arch, network):
        return 32

    def arch_selectable(self, arch):
        return False

    def network_items(self, arch, tr):
        """显示名必须同时写进 itemData: 收集参数读的是 currentData."""
        return [(code, code) for code in model_codes()]

    def accepts_dataset_type(self, dataset_type):
        """只列打过 ocr 标记的数据集: 文本真值只在那边有."""
        return dataset_type == "ocr"

    def dataset_problem(self, proj, name, info, task_label, tr):
        if str(info.get("dataset_type", "") or "") != "ocr":
            return tr(NO_TEXT).format(proj, name, task_label)
        return None


SPEC = OcrSpec()

