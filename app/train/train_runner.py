# -*- coding: utf-8 -*-
"""
检测/分割训练的入口: 按网络架构转发到 rf-detr 或 CNN 的实现.

train_worker 以 -c 方式导入本模块再调 main(), config 路径走 argv[1]; 两个实现
自己会再读一次同一个文件, 这里只管挑一个交出去.

导入放在函数里是刻意的: 两个实现分别拖着 rfdetr + pytorch_lightning 与
ultralytics, 子进程只该加载自己那套框架.
"""

import json
import sys

from app.train.transformer_backend import uses_transformer


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if uses_transformer(cfg):
        from app.train.transformer_train_runner import main as run
    else:
        from app.train.cnn_train_runner import main as run
    run()


if __name__ == "__main__":
    main()
