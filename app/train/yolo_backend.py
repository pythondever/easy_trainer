# -*- coding: utf-8 -*-
"""YOLO(ultralytics) 后端的公共件: 后端判定 + 设备参数转换 + 推理结果适配.

测试流程(test_runner)与导出(onnx_export)吃的都是 rf-detr 的形状 —— predict
返回 .xyxy / .confidence / .class_id / .mask / .data['class_name']. 这里把
YOLO 的 Results 包成同样的形状, 下游那两个后端就能共用同一套代码.
"""

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import numpy as np
except ImportError:
    np = None


def uses_cnn(cfg):
    """
    cfg 指向的模型该用 ultralytics 还是 rf-detr 来加载.

    以训练记录里写的 family 为准; 没有 family 才退回看后缀(ultralytics 权重的
    后缀是 .pt, rf-detr 训练产物是 .pth). 后缀只兜"路径是手工拼的"那种情况 ——
    rf-detr 的分割*预训练*权重也叫 .pt, 所以凡是有 family 的地方必须传进来.
    """
    family = str(cfg.get("family") or "")
    if family:
        return family == "cnn"
    return str(cfg.get("model_path", "")).lower().endswith(".pt")


def device_arg(device):
    """UI 存的 cuda:0 → ultralytics 认的 0; 非 cuda 或不可用时退 cpu."""
    if not str(device).startswith("cuda"):
        return "cpu"
    try:
        import torch
    except ImportError:
        return "cpu"
    if not torch.cuda.is_available():
        return "cpu"
    parts = str(device).split(":")
    return int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0


def _polys_to_masks(polys, width, height):
    """
    多边形顶点 → 原图尺寸的二值 mask, 喂给 test_runner 的 _mask_to_rings.

    不用 Results.masks.data: 那是 letterbox 之后推理尺寸上的 mask, 直接当原图用
    会整体偏缩. masks.xy 已经还原到原图坐标, 按它填回来最省事也最准.
    """
    if cv2 is None or np is None:
        return None
    out = []
    for poly in polys:
        canvas = np.zeros((height, width), np.uint8)
        pts = np.asarray(poly, dtype=np.float32).reshape(-1, 1, 2)
        if len(pts) >= 3:
            cv2.fillPoly(canvas, [np.round(pts).astype(np.int32)], 255)
        out.append(canvas)
    return out


class YoloDetections(object):
    """一次 YOLO 预测的结果, 字段名与用法对齐 rf-detr 的 predict 返回值."""

    __slots__ = ("xyxy", "confidence", "class_id", "mask", "data")

    def __init__(self, xyxy, confidence, class_id, mask, data):
        self.xyxy = xyxy
        self.confidence = confidence
        self.class_id = class_id
        self.mask = mask
        self.data = data


def to_detections(result):
    """ultralytics 单个 Results → YoloDetections."""
    boxes = getattr(result, "boxes", None)
    xyxy, confs, cids = [], [], []
    if boxes is not None and len(boxes):
        xyxy = [[float(v) for v in box] for box in boxes.xyxy]
        confs = [float(c) for c in boxes.conf]
        cids = [int(c) for c in boxes.cls]

    masks = None
    raw = getattr(result, "masks", None)
    if raw is not None and len(raw):
        shape = getattr(result, "orig_shape", None)
        if shape:
            masks = _polys_to_masks(list(raw.xy), int(shape[1]), int(shape[0]))

    names = getattr(result, "names", None) or {}
    cnames = []
    if cids and isinstance(names, dict):
        cnames = [str(names.get(c, c)) for c in cids]
    return YoloDetections(xyxy, confs, cids, masks, {"class_name": cnames})


class YoloPredictor(object):
    """加载 .pt; predict 的签名与 rf-detr 对齐(图片路径 + threshold)."""

    def __init__(self, model_path, device="cuda"):
        from ultralytics import YOLO
        self._model = YOLO(model_path)
        self._device = device_arg(device)

    def predict(self, img_path, threshold=0.5):
        results = self._model.predict(img_path, conf=float(threshold),
                                      device=self._device, verbose=False)
        result = results[0] if isinstance(results, (list, tuple)) else results
        return to_detections(result)
