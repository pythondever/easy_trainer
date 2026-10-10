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

# 只管识别段之后, 档位按识别骨干去重: nano 与 small 是同一个骨干, 合并成一档.
# 上面整张表留着只是为了认历史记录里的旧代号.
RECO_CODES = ("nano", "medium", "large")

# task 字段的取值: 下拉上是 ocr, 落到训练记录里是 ocr_rec.
# ocr_det 只为认历史记录保留, 新训练不再产生
OCR_TASKS = ("ocr", "ocr_det", "ocr_rec")
DET_TASK = "ocr_det"
RECO_TASK = "ocr_rec"

# 一次训练实际入队的段: 字符位置不再由模型找, 只训识别
TRAIN_STAGES = (RECO_TASK,)

# 识别段画布(高, 宽). 骨干在宽度上总步长 4, 时间步 T = 宽 / 4,
# 而 CTC 要求 T 不小于标注长度; 字条集最长 48 字, 768 / 4 = 192 步够用.
RECO_SIZE = (32, 768)


def model_codes():
    return list(RECO_CODES)


def split_arch(code):
    """代号转成 (检测架构, 识别架构); 认不出来时按表里第一条兜底."""
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
    """字符识别: 只训识别段, 型号是识别骨干的代号."""

    code = "ocr"
    defaults = (50, 1e-4, 768, 4)
    split_stages = TRAIN_STAGES
    # 识别段输入写死在 runner 里, 这一格填什么都不参与训练
    disabled_fields = ("img_size_line_txt",)

    def resolve_family(self, raw):
        return "ocr"

    def img_tip(self, arch):
        return QT_TRANSLATE_NOOP(
            "TrainDialog",
            "识别段输入固定 32x768(高x宽), 本项不用填")

    def arch_selectable(self, arch):
        return False

    def network_items(self, arch, tr):
        """显示名必须同时写进 itemData: 收集参数读的是 currentData."""
        return [(code, code) for code in model_codes()]

    def accepts_dataset_type(self, dataset_type):
        """不按类型挡: 字条集导入时没有类型标记, 能不能用看标签格式."""
        return True

    def dataset_problem(self, proj, name, info, task_label, tr):
        # 字条集是 .txt(一图一行字), 老 OCR 集是 .json(labelme 文本框),
        # 其余格式没有文字真值
        fmt = str(info.get("label_fmt", "") or "")
        if fmt not in (".txt", ".json"):
            return tr(NO_TEXT).format(proj, name, task_label)
        return None


SPEC = OcrSpec()

