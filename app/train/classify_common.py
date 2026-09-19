# -*- coding: utf-8 -*-
"""分类 runner 的模型构造: 分类训练脚本与分类测试脚本共用一份.

主进程刻意不碰 torch(见 dialogs.collect_devices 的说明), 这里只被两个分类
runner 在子进程里导入, 不影响 GUI 启动.
"""

import torch.nn as nn
from torchvision import models


def make_resnet(arch, num_classes):
    """按架构名建 ResNet, 把 fc 换成 num_classes 类; 认不出的名字退回 resnet18."""
    variants = {
        "resnet18": models.resnet18, "resnet34": models.resnet34,
        "resnet50": models.resnet50, "resnet101": models.resnet101,
    }
    model = variants.get(arch, models.resnet18)(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model
