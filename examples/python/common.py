# -*- coding: utf-8 -*-
"""检测/分割/分类共用的预处理与后处理。"""

import json

import cv2
import numpy as np

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def preprocess(bgr, size):
    """OpenCV BGR 图转成模型输入 [1,3,size,size]。方形缩放, 不保持宽高比。"""
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (size, size), interpolation=cv2.INTER_LINEAR)
    x = resized.astype(np.float32) / 255.0
    x = (x - MEAN) / STD
    return np.ascontiguousarray(np.transpose(x, (2, 0, 1))[None])


def input_size(session, fallback):
    """模型输入尺寸是静态的, 用模型实际的 H(训练尺寸不一定是 640/224)。"""
    shape = session.get_inputs()[0].shape
    return int(shape[2]) if len(shape) == 4 and isinstance(shape[2], int) else fallback


def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))


def decode_dets(dets, labels, orig_wh, score_thr=0.5):
    """
    dets/labels 转成 [(x1, y1, x2, y2, score, class_id)]，坐标已还原到原图像素。
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
    """类别表转成按 id 下标排列的类名列表。

    认两种格式: label_map.json（{"类名": id}，导出包默认给这个）
    与 classes.txt（每行 'id name' 或只有 name, 行号即类别 id, 旧包与训练目录里还有）。
    """
    if not path:
        return []
    if path.lower().endswith(".json"):
        return _load_label_map(path)
    names = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            names.append(parts[1] if len(parts) > 1 else parts[0])
    return names


def _load_label_map(path):
    """{"类名": id} 转成按下标展开的类名列表(缺号留空串, 保证 names[id] 取得到)。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return []
    if not isinstance(data, dict):
        return []
    items = []
    for name, cid in data.items():
        try:
            items.append((int(cid), str(name)))
        except (TypeError, ValueError):
            continue
    items = [(i, n) for i, n in items if i >= 0]
    if not items:
        return []
    out = [""] * (max(i for i, _ in items) + 1)
    for i, name in items:
        out[i] = name
    return out


# ---- CNN(YOLO) 分支: 预处理与输出约定都和上面那套不同, 别混用 ----

PAD_COLOR = (114, 114, 114)   # letterbox 的补边色, 与 ultralytics 一致
MASK_DIM = 32                 # 分割 head 输出的掩码系数个数


def letterbox(bgr, size, pad_color=PAD_COLOR):
    """
    BGR 图转成 CNN 分支的模型输入, 附带还原坐标要用的几何量。

    保长宽比缩放后居中补边, 不像 rf-detr 那样直接拉成方形: 拉伸会让框的
    位置系统性偏移。返回 (输入张量, 几何量字典), 字典含缩放比 ratio、补边
    left/top、输入边长 size、缩放后的 inner。
    """
    h, w = bgr.shape[:2]
    ratio = min(size / float(h), size / float(w))
    inner_w, inner_h = int(round(w * ratio)), int(round(h * ratio))
    # 减 0.1 再取整是照 ultralytics 的 LetterBox 抄的, 补边落半像素会让框整体偏一格
    left = int(round((size - inner_w) / 2.0 - 0.1))
    top = int(round((size - inner_h) / 2.0 - 0.1))
    img = cv2.resize(bgr, (inner_w, inner_h), interpolation=cv2.INTER_LINEAR)
    img = cv2.copyMakeBorder(img, top, size - inner_h - top,
                             left, size - inner_w - left,
                             cv2.BORDER_CONSTANT, value=pad_color)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    x = np.ascontiguousarray(np.transpose(rgb, (2, 0, 1))[None])
    return x, {"ratio": ratio, "left": left, "top": top, "size": size,
               "inner": (inner_w, inner_h)}


def _iou(box, boxes):
    x1 = np.maximum(box[0], boxes[:, 0])
    y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[2], boxes[:, 2])
    y2 = np.minimum(box[3], boxes[:, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    area = (box[2] - box[0]) * (box[3] - box[1])
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    return inter / np.maximum(area + areas - inter, 1e-9)


def _nms_one(boxes, scores, thr):
    """单类 NMS, 返回在入参里的下标。"""
    order = np.argsort(-scores)
    keep = []
    while order.size:
        i = order[0]
        keep.append(int(i))
        if order.size == 1:
            break
        rest = order[1:]
        order = rest[_iou(boxes[i], boxes[rest]) <= thr]
    return keep


def _pick_yolo(out, geo, orig_wh, ncls, score_thr, iou_thr):
    """
    检测输出过滤 + 类内 NMS, 返回 (原图坐标的框, 分数, 类别, 候选下标)。

    前 4 行是 (cx, cy, w, h) 像素值(相对 letterbox 后的输入图), 之后每行一个
    类别分数, 模型导出时已经过 sigmoid 不用再算。候选是原生的 anchor 点, 同一
    目标会命中多个, 必须自己去重。
    """
    det = out[0]
    boxes = det[:4].T
    prob = det[4:4 + ncls].T
    cls_ids = prob.argmax(axis=1)
    scores = prob[np.arange(len(cls_ids)), cls_ids]
    picked = np.where(scores >= score_thr)[0]
    if not picked.size:
        return (np.zeros((0, 4), np.float32), np.zeros(0, np.float32),
                np.zeros(0, np.int64), picked)
    boxes, scores, cls_ids = boxes[picked], scores[picked], cls_ids[picked]
    ow, oh = orig_wh
    cx, cy, bw, bh = boxes.T
    ratio, left, top = geo["ratio"], geo["left"], geo["top"]
    xyxy = np.stack([
        np.clip((cx - bw / 2.0 - left) / ratio, 0, ow),
        np.clip((cy - bh / 2.0 - top) / ratio, 0, oh),
        np.clip((cx + bw / 2.0 - left) / ratio, 0, ow),
        np.clip((cy + bh / 2.0 - top) / ratio, 0, oh)], axis=1)
    keep = []
    for c in np.unique(cls_ids):
        idx = np.where(cls_ids == c)[0]
        keep += [int(idx[i]) for i in _nms_one(xyxy[idx], scores[idx], iou_thr)]
    keep.sort()
    keep = np.array(keep, dtype=np.int64)
    return xyxy[keep], scores[keep], cls_ids[keep], picked[keep]


def decode_yolo(out, geo, orig_wh, ncls=None, score_thr=0.5, iou_thr=0.45):
    """
    检测输出 output0 转成 [(x1, y1, x2, y2, score, class_id)], 坐标已还原到
    原图像素。分割的 output0 也走这里, 传 ncls 把后面的掩码系数行排掉。
    """
    if ncls is None:
        ncls = out[0].shape[0] - 4
    xyxy, scores, cls_ids, _idx = _pick_yolo(out, geo, orig_wh, ncls,
                                             score_thr, iou_thr)
    return [(float(b[0]), float(b[1]), float(b[2]), float(b[3]), float(s), int(c))
            for b, s, c in zip(xyxy, scores, cls_ids)]


def decode_yolo_masks(out, proto, geo, orig_wh, ncls, score_thr=0.5,
                      iou_thr=0.45, mask_thr=0.5):
    """
    分割的两路输出转成 (检测列表, 掩码列表), 掩码是原图尺寸的 0/1 数组。

    output0 比检测多出 32 行掩码系数, 与 output1 那 32 张低分辨率原型图线性
    组合再补 sigmoid 才是掩码(与训练时的口径一致)。掩码要按 letterbox 的补边
    裁掉再缩回原图, 直接拉伸会整体位移。
    """
    det = out[0]
    xyxy, scores, cls_ids, idx = _pick_yolo(out, geo, orig_wh, ncls,
                                            score_thr, iou_thr)
    if not len(idx):
        return [], []
    dim, mh, mw = proto.shape
    coeff = det[4 + ncls:4 + ncls + dim].T[idx]
    masks = sigmoid(coeff @ proto.reshape(dim, -1)).reshape(-1, mh, mw)
    size, left, top = geo["size"], geo["left"], geo["top"]
    inner_w, inner_h = geo["inner"]
    ow, oh = orig_wh
    dets = [(float(b[0]), float(b[1]), float(b[2]), float(b[3]), float(s), int(c))
            for b, s, c in zip(xyxy, scores, cls_ids)]
    out_masks = []
    for (x1, y1, x2, y2, _s, _c), m in zip(dets, masks):
        m = cv2.resize(m, (size, size), interpolation=cv2.INTER_LINEAR)
        m = m[top:top + inner_h, left:left + inner_w]
        m = cv2.resize(m, (ow, oh), interpolation=cv2.INTER_LINEAR)
        keep = np.zeros((oh, ow), dtype=np.uint8)
        ys, ye = max(int(y1), 0), min(int(np.ceil(y2)), oh)
        xs, xe = max(int(x1), 0), min(int(np.ceil(x2)), ow)
        if ye > ys and xe > xs:
            keep[ys:ye, xs:xe] = (m[ys:ye, xs:xe] >= mask_thr).astype(np.uint8)
        out_masks.append(keep)
    return dets, out_masks
