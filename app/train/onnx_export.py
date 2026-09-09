# -*- coding: utf-8 -*-
"""
模型导出为 ONNX。

检测/分割（RF-DETR）走 rfdetr 自带的 export，分类（resnet）走 torch.onnx.export。
两者产物统一由调用方命名，导出目录里不再出现 .pth。
"""

import os
import shutil
import tempfile


def _torch():
    import torch
    return torch


def export_detr_onnx(model_path, out_file, log=print):
    """RF-DETR 检测/分割 → ONNX。返回写好的 onnx 路径。"""
    from rfdetr import RFDETR

    model = RFDETR.from_checkpoint(model_path)
    tmp_dir = tempfile.mkdtemp(prefix="et_onnx_")
    try:
        log("[export] 正在导出 ONNX（可能需要 1~2 分钟）...")
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
    """分类模型（resnet 系列）→ ONNX。返回写好的 onnx 路径。"""
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
    log("[export] 正在导出分类模型 ONNX（输入 {}x{}）...".format(size, size))
    # 边长为动态轴: 部署侧不必强行缩放到训练尺寸
    torch.onnx.export(
        model, dummy, out_file,
        input_names=["images"], output_names=["scores"],
        opset_version=17, dynamo=False,
        dynamic_axes={"images": {0: "batch", 2: "height", 3: "width"},
                      "scores": {0: "batch"}},
    )
    return out_file


def export_onnx(model_path, task, out_file, img_size=0, log=print):
    """按任务类型分派；返回 onnx 路径。"""
    if task == "classify":
        return export_classify_onnx(model_path, out_file,
                                    img_size=img_size or 224, log=log)
    return export_detr_onnx(model_path, out_file, log=log)
