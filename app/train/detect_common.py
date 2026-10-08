# -*- coding: utf-8 -*-
"""检测任务的规格."""

from app.train.task_spec import QT_TRANSLATE_NOOP, TaskSpec


class DetectSpec(TaskSpec):
    code = "detect"
    defaults = (100, 1e-4, 640, 4)

    def img_tip(self, arch):
        return QT_TRANSLATE_NOOP(
            "TrainDialog", "目标检测推荐图像尺寸: 640(可设为 32 的倍数如 640/672)")

    def img_block(self, arch, network):
        """rf-detr 与 CNN 的检测都是 32 的倍数."""
        return 32

    def aug_supported(self):
        return True


SPEC = DetectSpec()
