# -*- coding: utf-8 -*-
"""
OCR 数据铺设: labelme 文本标注转成 docTR 的两种数据集目录.
只在子进程被 runner 导入(主进程不装 doctr), 与 classify_common 同理.
"""

import json
import os
import shutil

import numpy as np
from PIL import Image

from app.core.constants import IMAGE_EXTS
from app.core.db import get_paths
from app.core.label_utils import (is_text_label, load_json_shapes,
                                  looks_like_labelme)
from app.train.data_prep import _unique_dst


def _image_files(img_dir):
    return [os.path.join(img_dir, fn) for fn in sorted(os.listdir(img_dir))
            if os.path.splitext(fn)[1].lower() in IMAGE_EXTS]


def _find_json(img_path, label_dirs):
    """标注 json 有两个落点: 图像同目录(标注界面产物)与导入时选的标签目录."""
    stem = os.path.splitext(os.path.basename(img_path))[0]
    cands = [os.path.join(os.path.dirname(img_path), stem + ".json")]
    cands += [os.path.join(d, stem + ".json") for d in label_dirs if d]
    for p in cands:
        if os.path.isfile(p) and looks_like_labelme(p):
            return p
    return ""


def _to_quad(points):
    """labelme 的点补成 4 点多边形: 矩形补四角, 多于 4 点退成外接框."""
    if len(points) == 4:
        return [[float(p[0]), float(p[1])] for p in points]
    xs = [float(p[0]) for p in points]
    ys = [float(p[1]) for p in points]
    x1, x2, y1, y2 = min(xs), max(xs), min(ys), max(ys)
    return [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]


def collect(datasets, split):
    """[{"image", "polygons": [[4 点]], "texts": [str]}], 只收文本标注."""
    samples = []
    for ds in datasets:
        if ds.get("split") != split:
            continue
        label_dirs = get_paths(ds, "label")
        for img_dir in get_paths(ds, "image"):
            if not img_dir or not os.path.isdir(img_dir):
                continue
            for img_path in _image_files(img_dir):
                jp = _find_json(img_path, label_dirs)
                if not jp:
                    continue
                polys, texts = [], []
                for label, pts, text in load_json_shapes(jp):
                    if not is_text_label(label) or len(pts) < 2:
                        continue
                    polys.append(_to_quad(pts))
                    texts.append(str(text or ""))
                if polys:
                    samples.append({"image": img_path, "polygons": polys,
                                    "texts": texts})
    return samples


def _reset(root):
    if os.path.isdir(root):
        shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root, exist_ok=True)


def write_det(root, samples):
    """
    铺成 DetectionDataset 要的: root/images/*.png + root/labels.json.
    docTR 的 pre_transform 会按真实图像尺寸把 polygons 除成相对坐标,
    所以这里写绝对像素, 并把 img_dimensions 一并记下.
    """
    _reset(root)
    img_dir = os.path.join(root, "images")
    os.makedirs(img_dir, exist_ok=True)
    labels = {}
    used = set()
    for s in samples:
        name = os.path.basename(s["image"])
        dst = _unique_dst(img_dir, name, used)
        shutil.copy2(s["image"], dst)
        used.add(os.path.basename(dst))
        with Image.open(dst) as im:
            w, h = im.size
        labels[os.path.basename(dst)] = {
            "img_dimensions": (h, w), "polygons": s["polygons"]}
    lab_path = os.path.join(root, "labels.json")
    with open(lab_path, "w", encoding="utf-8") as f:
        json.dump(labels, f, ensure_ascii=False)
    return img_dir, lab_path


def write_rec(root, samples):
    """
    铺成 RecognitionDataset 要的: root/crops/*.png + root/labels.json.
    按标注框裁图而不是跑检测模型: 识别段要学的是"长这样读什么",
    拿预测的框训会把检测段的误差带进来.
    """
    _reset(root)
    crop_dir = os.path.join(root, "crops")
    os.makedirs(crop_dir, exist_ok=True)
    labels = {}
    idx = 0
    for s in samples:
        stem = os.path.splitext(os.path.basename(s["image"]))[0]
        geoms = np.asarray(s["polygons"], dtype=int)
        try:
            from doctr.datasets.utils import crop_bboxes_from_image
            crops = crop_bboxes_from_image(s["image"], geoms)
        except Exception:
            crops = _crop_fallback(s["image"], geoms)
        for crop, text in zip(crops, s["texts"]):
            if not text or crop.size == 0 or min(crop.shape[:2]) < 2:
                continue
            name = "{}_{:04d}.png".format(stem, idx)
            idx += 1
            Image.fromarray(crop).save(os.path.join(crop_dir, name))
            labels[name] = text
    lab_path = os.path.join(root, "labels.json")
    with open(lab_path, "w", encoding="utf-8") as f:
        json.dump(labels, f, ensure_ascii=False)
    return crop_dir, lab_path


def _crop_fallback(img_path, geoms):
    """doctr 裁图不可用时的兜底: 按外接框裁(我们的框本来就是正的)."""
    with Image.open(img_path) as im:
        img = im.convert("RGB")
    out = []
    for g in geoms:
        xs = [float(p[0]) for p in g]
        ys = [float(p[1]) for p in g]
        box = (max(int(min(xs)), 0), max(int(min(ys)), 0),
               int(max(xs)) + 1, int(max(ys)) + 1)
        out.append(np.asarray(img.crop(box)))
    return out


def build_vocab(samples):
    """识别段词表: 直接取标注里出现过的字符, 训练是从头训, 不必对齐预训练词表."""
    chars = set()
    for s in samples:
        for t in s["texts"]:
            chars.update(str(t or ""))
    return "".join(sorted(chars))
