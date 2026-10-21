# -*- coding: utf-8 -*-
"""QImage(ARGB32 系) 转 HxWx4 BGRA 视图(小端内存序), 不拷贝.

img 必须在结果使用期间存活, 否则段错误.
贴图融合与多边形亮度两簇共用, 故独立成模块(拆自 scene.py).
"""
import numpy as np


def bgra_view(img):
    w, h = img.width(), img.height()
    arr = np.frombuffer(img.bits(), dtype=np.uint8)
    return arr.reshape(h, img.bytesPerLine())[:, :w * 4].reshape(h, w, 4)
