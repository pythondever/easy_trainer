# -*- coding: utf-8 -*-
"""
模型导出为 ONNX.

按任务与网络架构分派: 分类(resnet)走 torch.onnx.export, 检测/分割里 rf-detr 与
YOLO 各走自家 export. 后两家会把 onnx 写到权重文件旁边, 这里统一 move 到调用方
给的 out_file, 导出目录里就只剩调用方命名的文件.
"""

import os
import shutil
import tempfile

from PySide6.QtCore import QCoreApplication as QC

from app.train.yolo_backend import uses_cnn


def _torch():
    import torch
    return torch


def export_detr_onnx(model_path, out_file, log=print):
    """RF-DETR 检测/分割 → ONNX. 返回写好的 onnx 路径."""
    from rfdetr import RFDETR

    model = RFDETR.from_checkpoint(model_path)
    tmp_dir = tempfile.mkdtemp(prefix="et_onnx_")
    try:
        log("[export] 正在导出 ONNX(可能需要 1~2 分钟)...")
        produced = model.export(output_dir=tmp_dir, format="onnx")
        src = str(produced) if produced else ""
        if not src or not os.path.exists(src):
            # 不同版本返回值可能为空, 退回按文件名挑; .sim.onnx 是简化后的最终产物
            cands = [f for f in os.listdir(tmp_dir) if f.endswith(".onnx")]
            if not cands:
                raise RuntimeError("ONNX 导出未生成文件")
            cands.sort(key=lambda n: (not n.endswith(".sim.onnx"), n))
            src = os.path.join(tmp_dir, cands[0])
        shutil.move(src, out_file)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    return out_file


def export_classify_onnx(model_path, out_file, img_size=224, log=print):
    """分类模型(resnet 系列)→ ONNX. 返回写好的 onnx 路径."""
    torch = _torch()
    import torch.nn as nn
    from torchvision import models

    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    arch = ckpt.get("architecture", "resnet18")
    fc_out = int(ckpt["state_dict"]["fc.weight"].shape[0])
    variants = {
        "resnet18": models.resnet18, "resnet34": models.resnet34,
        "resnet50": models.resnet50, "resnet101": models.resnet101,
    }
    model = variants.get(arch, models.resnet18)(weights=None)
    model.fc = nn.Linear(model.fc.in_features, fc_out)
    model.load_state_dict(ckpt["state_dict"])
    model.eval()

    size = int(img_size or 224)
    dummy = torch.zeros(1, 3, size, size)
    log("[export] 正在导出分类模型 ONNX(输入 {}x{})...".format(size, size))
    # 边长为动态轴: 部署侧不必强行缩放到训练尺寸
    torch.onnx.export(
        model, dummy, out_file,
        input_names=["images"], output_names=["scores"],
        opset_version=17, dynamo=False,
        dynamic_axes={"images": {0: "batch", 2: "height", 3: "width"},
                      "scores": {0: "batch"}},
    )
    return out_file


def export_yolo_onnx(model_path, out_file, img_size=0, log=print):
    """YOLO(ultralytics) 检测/分割 → ONNX. 返回写好的 onnx 路径."""
    from ultralytics import YOLO

    model = YOLO(model_path)
    log("[export] 正在导出 ONNX(可能需要 1~2 分钟)...")
    produced = model.export(format="onnx", imgsz=int(img_size or 640),
                            simplify=True)
    src = str(produced or "")
    if not src or not os.path.exists(src):
        raise RuntimeError("ONNX 导出未生成文件")
    # export 把 onnx 写在 .pt 旁边(可能就在训练输出目录里), 不挪走会留个副本
    if os.path.abspath(src) != os.path.abspath(out_file):
        shutil.move(src, out_file)
    return out_file


def export_onnx(model_path, task, out_file, img_size=0, family="", log=print):
    """按任务与网络架构分派; 返回 onnx 路径."""
    if task == "classify":
        return export_classify_onnx(model_path, out_file,
                                    img_size=img_size or 224, log=log)
    if task == "ad":
        # 异常检测的模型文件是一整个 anomalib 模型(骨干 + 记忆库/归一化流),
        # 不是一条前向网络, 也没有"一张图一个分数"的现成导出入口; 硬导会得到
        # 一个语义不明的图, 不如直接说清楚
        raise ValueError(QC.translate(
            "OnnxExport",
            "异常检测模型暂不支持导出 ONNX(它是骨干加记忆库的组合结构), "
            "请直接用模型文件在软件里测试"))
    if uses_cnn({"family": family, "model_path": model_path}):
        return export_yolo_onnx(model_path, out_file, img_size=img_size,
                                log=log)
    return export_detr_onnx(model_path, out_file, log=log)
