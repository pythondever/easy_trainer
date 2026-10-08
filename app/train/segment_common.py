# -*- coding: utf-8 -*-
"""分割任务的规格. 与检测同路(都走 rf-detr / CNN), 差异只在尺寸与步长."""

from app.train.task_spec import QT_TRANSLATE_NOOP, TaskSpec

# 步长按档位不同: 只有 nano 是 12, 其余三档 24
BLOCK = {"nano": 12, "small": 24, "medium": 24, "large": 24}


class SegmentSpec(TaskSpec):
    code = "segment"
    defaults = (100, 1e-4, 648, 4)

    def img_tip(self, arch):
        if arch == "cnn":
            return QT_TRANSLATE_NOOP("TrainDialog", "CNN 分割推荐尺寸: 640(需为 32 的倍数)")
        return QT_TRANSLATE_NOOP("TrainDialog", "图像分割推荐尺寸: 648(需为 {} 的倍数)")

    def img_block(self, arch, network):
        """CNN 分割不吃 rf-detr 那条 12 的倍数约束."""
        if arch == "cnn":
            return 32
        # 档位名取不到时按最松的一档算: 漏报好过误报
        return BLOCK.get(network) or min(BLOCK.values())

    def aug_supported(self):
        return True


SPEC = SegmentSpec()
