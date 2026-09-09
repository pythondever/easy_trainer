# -*- coding: utf-8 -*-
"""检测/分割/分类共用的预处理与后处理。"""

import cv2
import numpy as np

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def preprocess(bgr, size):
    """OpenCV BGR 图 → 模型输入 [1,3,size,size]。方形缩放, 不保持宽高比。"""
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (size, size), interpolation=cv2.INTER_LINEAR)
    x = resized.astype(np.float32) / 255.0
    x = (x - MEAN) / STD
    return np.ascontiguousarray(np.transpose(x, (2, 0, 1))[None])


def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))


def decode_dets(dets, labels, orig_wh, score_thr=0.5):
    """
    dets/labels → [(x1, y1, x2, y2, score, class_id)]，坐标已还原到原图像素。
    300 个候选是端到端去重的结果，不需要再做 NMS。
    """
    w, h = orig_wh
    prob = sigmoid(labels[0])
    # 最后一列是「无目标」, 只在前 C 列里取类别与置信度
    scores = prob[:, :-1].max(axis=1)
    cls_ids = prob[:, :-1].argmax(axis=1)
    out = []
    for i in np.where(scores >= score_thr)[0]:
        cx, cy, bw, bh = dets[0, i]
        out.append((float((cx - bw / 2) * w), float((cy - bh / 2) * h),
                    float((cx + bw / 2) * w), float((cy + bh / 2) * h),
                    float(scores[i]), int(cls_ids[i])))
    return out


def load_classes(path):
    """classes.txt: 每行 'id name' 或只有 name, 行号即类别 id。"""
    if not path:
        return []
    names = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            names.append(parts[1] if len(parts) > 1 else parts[0])
    return names
