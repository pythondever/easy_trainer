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

from app.train.cnn_backend import uses_cnn


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


def export_ocr_onnx(model_path, out_file, img_size=0, log=print):
    """
    字符检测/识别 → ONNX. 返回写好的 onnx 路径.
    docTR 的模型在 exportable=True 下只吐 logits(检测是概率图, 识别是字符
    序列), 后处理留给部署侧 —— 官方 predictor 里那套二值化/CTC 解码带着
    numpy 与动态控制流, 进不了 onnx. 输入尺寸取训练时的 img_size: 骨干是
    全卷积, 换尺寸能跑但部署侧得自己 resize, 动态轴反而容易在 LinkNet 的
    插值上翻车.
    """
    torch = _torch()
    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    arch = str(ckpt.get("architecture") or "")
    is_rec = str(ckpt.get("task") or "") == "ocr_rec"
    if is_rec:
        from doctr.models import recognition as _lib
        vocab = str(ckpt.get("vocab") or "")
        if not vocab:
            raise ValueError(QC.translate(
                "OnnxExport", "该识别模型没有词表, 无法导出"))
        fn = getattr(_lib, arch, None)
        kwargs = {"vocab": vocab}
    else:
        from doctr.models import detection as _lib
        fn = getattr(_lib, arch, None)
        kwargs = {}
    if fn is None:
        raise ValueError(QC.translate(
            "OnnxExport", "未知的字符模型架构: {}").format(arch))
    # 权重全在 ckpt 里: 默认参数会去下骨干的 ImageNet 权重
    model = fn(pretrained=False, pretrained_backbone=False, exportable=True,
               **kwargs)
    model.load_state_dict(ckpt["state_dict"])
    model.eval()
    channels, height, width = tuple(model.cfg["input_shape"])
    if not is_rec and img_size:
        height = width = int(img_size)
    dummy = torch.zeros(1, channels, height, width)
    log("[export] 正在导出字符{}模型 ONNX(输入 {}x{})...".format(
        QC.translate("OnnxExport", "识别") if is_rec
        else QC.translate("OnnxExport", "检测"), height, width))
    torch.onnx.export(
        model, dummy, out_file,
        input_names=["images"], output_names=["logits"],
        opset_version=17, dynamo=False,
        dynamic_axes={"images": {0: "batch"}, "logits": {0: "batch"}},
    )
    return out_file


def export_onnx(model_path, task, out_file, img_size=0, family="", log=print):
    """按任务与网络架构分派; 返回 onnx 路径."""
    if task == "classify":
        return export_classify_onnx(model_path, out_file,
                                    img_size=img_size or 224, log=log)
    if task == "ad":
        # 异常检测的模型文件是一整个 anomalib 模型(骨干 + 记忆库/归一化流),
        # 不是一条前向网络; 交付走 model_dialog 的专用导出包, 到不了这里
        raise ValueError(QC.translate(
            "OnnxExport",
            "异常检测不导出 ONNX, 请用模型管理的「导出」生成模型包"))
    if task in ("ocr", "ocr_det", "ocr_rec"):
        return export_ocr_onnx(model_path, out_file, img_size=img_size,
                               log=log)
    if uses_cnn({"family": family, "model_path": model_path}):
        return export_yolo_onnx(model_path, out_file, img_size=img_size,
                                log=log)
    return export_detr_onnx(model_path, out_file, log=log)
