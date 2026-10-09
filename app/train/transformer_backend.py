# -*- coding: utf-8 -*-
"""
rf-detr(Transformer) 后端的公共件: 后端判定 + 推理封装.
与 cnn_backend 对称: 那边把 ultralytics 的 Results 包成 rf-detr 的形状, 这边
rf-detr 本身就是那个形状, 所以只做加载与推理优化. rfdetr 惰性导入, 顶层不拖它.
"""

from PySide6.QtCore import QCoreApplication as QC

from app.train.cnn_backend import uses_cnn


def uses_transformer(cfg):
    """cfg 指向的模型该用 rf-detr 加载, 是 uses_cnn 的对偶, 判据共用免得两处分叉."""
    return not uses_cnn(cfg)


class DetrPredictor(object):
    """加载 rf-detr checkpoint; predict 的签名与 YoloPredictor 对齐."""

    def __init__(self, model_path, device="cuda"):
        from rfdetr import RFDETR
        try:
            import torch
        except ImportError:
            torch = None
        model = RFDETR.from_checkpoint(model_path)
        on_cuda = (str(device).startswith("cuda") and torch is not None
                   and torch.cuda.is_available())
        if on_cuda and hasattr(model, "to"):
            model.to(device)
        if hasattr(model, "inference"):
            try:
                dtype = torch.float16 if on_cuda else torch.float32
                model.inference(dtype=dtype, compile=False)
                print("[test] " + QC.translate(
                    "TestRunner", "推理已优化: {}").format(dtype), flush=True)
            except Exception:
                pass
        self._model = model

    def predict(self, img_path, threshold=0.5):
        det = self._model.predict(img_path, threshold=float(threshold))
        if isinstance(det, list):
            det = det[0]
        return det
