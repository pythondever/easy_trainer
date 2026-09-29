# -*- coding: utf-8 -*-
"""
OCR 架构表: 训练对话框在主进程读它, 所以这里不能 import doctr.
"""

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
