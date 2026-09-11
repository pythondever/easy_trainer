# -*- coding: utf-8 -*-
"""
训练数据准备：复制图像/标签到输出路径、labelme json→yolo txt、生成 data.yaml。
目录结构（输出路径根）:
  data.yaml                      # yolo 配置（train/val 指向合并目录，names 类别）
  <项目>/<数据集>/images|labels    # 原始副本（需求：项目/数据集 结构）
  train/images|labels            # 训练集合并（RF-DETR 单路径 train）
  val/images|labels              # 验证集合并
  <时间戳>/                       # 本次训练输出（模型、metrics.csv）
"""

import os
import shutil
from datetime import datetime
from PIL import Image
from app.core.constants import IMAGE_EXTS
from app.core.db import get_paths
from app.core.label_utils import (normalize_label, load_json_shapes,
                                  load_yolo_shapes, looks_like_labelme,
                                  shapes_to_yolo_text)


def timestamp_dir():
    return datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


_img_size_cache = {}


def _img_size_of_stem(img_dir, stem):
    """按文件名主干在多种扩展名中找图并取尺寸, 找不到返回 (0, 0)。"""
    if not img_dir:
        return 0, 0
    for ext in IMAGE_EXTS:
        p = os.path.join(img_dir, stem + ext)
        if os.path.exists(p):
            return _img_size(p)
    return 0, 0


def _img_size(path):
    """
    图像尺寸(带进程内缓存)。
    labelme json → yolo txt 需要对每张图取尺寸, 而同一张图在「标签目录转换」
    和「图像同路径 json 转换」两处都会被查询, 缓存可省掉重复的文件打开。
    """
    cached = _img_size_cache.get(path)
    if cached is not None:
        return cached
    try:
        with Image.open(path) as im:
            size = im.size
    except Exception:
        size = (0, 0)
    _img_size_cache[path] = size
    return size


def _map_class_id(raw, label_ids):
    """txt 里的数字 id → 显示名(与标注 json 里的类别名对齐)，无映射则原样。"""
    raw = str(raw).strip()
    if label_ids and raw in label_ids:
        return normalize_label(label_ids[raw])
    return normalize_label(raw)


def _write_yolo_txt(dst_labels, base, shapes, iw, ih, label_to_id, as_polygon):
    """shapes → dst_labels/base。空 shapes 写空文件(用于覆盖来源里的旧标注)。"""
    if not shapes:
        return
    txt = shapes_to_yolo_text(shapes, iw, ih, label_to_id, as_polygon)
    with open(os.path.join(dst_labels, base), "w", encoding="utf-8") as f:
        f.write(txt)


def _copy_dataset_labels(src_label_path, fmt, dst_labels, label_to_id, img_dirs,
                         as_polygon=False, label_ids=None):
    """
    复制单个导入标签目录到 yolo txt 目录（labelme json / yolo txt 都转 txt）。
    img_dirs 是候选图像目录（配对目录排第一）。标签要按图像尺寸做坐标换算，
    尺寸查不到就整条跳过，所以目录配错不会写错数据，只会静默丢标签；
    "先只导图像、后导图像+标签"这类历史记录里配不成对的情况靠多候选兜住。
    """
    if not src_label_path or not os.path.isdir(src_label_path):
        return
    for fn in os.listdir(src_label_path):
        stem, ext = os.path.splitext(fn)
        if not ((fmt == "json" and ext.lower() == ".json")
                or (fmt == "txt" and ext.lower() == ".txt")):
            continue
        iw = ih = 0
        for d in img_dirs:
            iw, ih = _img_size_of_stem(d, stem)
            if iw and ih:
                break
        if not (iw and ih):
            continue
        if fmt == "json":
            shapes = load_json_shapes(os.path.join(src_label_path, fn))
        else:
            shapes = load_yolo_shapes(os.path.join(src_label_path, fn),
                                      iw, ih, label_ids)
        _write_yolo_txt(dst_labels, stem + ".txt", shapes, iw, ih,
                        label_to_id, as_polygon)


def _paired_dirs(info):
    """
    多路径导入的图像/标签目录配对 [(图像目录, 标签目录), ...]。
    每次导入往 image_paths / label_paths 各追加一项，按下标成对。
    只读 image_path / label_path 单值的话，多次导入后训练只吃得到最后
    一次导入的那个目录，之前的全被静默丢掉。
    """
    imgs = get_paths(info, "image")
    lbls = get_paths(info, "label")
    n = max(len(imgs), len(lbls))
    return [(imgs[i] if i < len(imgs) else "",
             lbls[i] if i < len(lbls) else "") for i in range(n)]


def _label_img_dirs(img_dir, all_img_dirs):
    """标签转换时的候选图像目录: 配对目录优先, 其余目录兜底。"""
    return ([img_dir] if img_dir else []) + [d for d in all_img_dirs
                                             if d and d != img_dir]


def _collect_labels(datasets):
    """收集类别集合：导入标签目录 + 图像同路径 json(标注产物) 都要扫。

    只扫导入目录的话，标注界面新增的类别名进不了 label_to_id，
    会被 shapes_to_yolo_text 的 get(label, 0) 静默写成类别 0。
    txt 的类别按 label_ids 换成显示名，避免和 json 里的同一个类被当成两类。
    """
    labels = []
    seen = set()
    for info in datasets:
        fmt = str(info.get("fmt", "txt")).lstrip(".")
        label_ids = info.get("label_ids") or {}

        def _add(lb):
            if lb and lb not in seen:
                seen.add(lb)
                labels.append(lb)

        for img_dir, label_path in _paired_dirs(info):
            if label_path and os.path.isdir(label_path):
                for fn in sorted(os.listdir(label_path)):
                    stem, ext = os.path.splitext(fn)
                    if fmt == "json" and ext.lower() == ".json":
                        for lb, _ in load_json_shapes(
                                os.path.join(label_path, fn)):
                            _add(lb)
                    elif fmt == "txt" and ext.lower() == ".txt":
                        try:
                            with open(os.path.join(label_path, fn), "r",
                                      encoding="utf-8") as f:
                                for line in f:
                                    p = line.split()
                                    if len(p) >= 5:
                                        _add(_map_class_id(p[0], label_ids))
                        except Exception:
                            continue
            if img_dir and os.path.isdir(img_dir):
                for fn in sorted(os.listdir(img_dir)):
                    if not fn.lower().endswith(".json"):
                        continue
                    jp = os.path.join(img_dir, fn)
                    if not looks_like_labelme(jp):
                        continue
                    for lb, _ in load_json_shapes(jp):
                        _add(lb)
    return labels


def _copy_images(src_img_path, dst_images):
    """复制图像（扁平目录）。返回图像文件名集合。"""
    copied = set()
    if not src_img_path or not os.path.isdir(src_img_path):
        return copied
    for fn in os.listdir(src_img_path):
        if fn.lower().endswith(IMAGE_EXTS):
            shutil.copy2(os.path.join(src_img_path, fn), os.path.join(dst_images, fn))
            copied.add(fn)
    return copied


def _sort_labels(labels):
    """类别排序：数字标签按数值升序，非数字按字符串（保证 txt ID 重映射稳定）。"""
    def key(x):
        return (0, int(x)) if str(x).isdigit() else (1, str(x))
    return sorted(set(labels), key=key)


def copy_datasets(out_root, project, datasets, task="detect"):
    """
    把勾选数据集复制到 <out_root>/<项目>/<数据集>/images|labels（json/txt→yolo txt）。
    task=segment 时写 yolo-seg 多边形顶点，检测写 cx cy w h。
    每张图的标签来源以图像同路径 json 为准（存在即覆盖，空的也算：表示这张图没有目标）。
    """
    as_polygon = task == "segment"
    labels = _sort_labels(_collect_labels(datasets))
    label_to_id = {lb: i for i, lb in enumerate(labels)}
    print("[train] 解析到类别 {} 个: {}".format(len(labels), labels), flush=True)
    for info in datasets:
        ds_name = info["dataset_name"]
        dst = os.path.join(out_root, project, ds_name)
        dst_images = os.path.join(dst, "images")
        dst_labels = os.path.join(dst, "labels")
        os.makedirs(dst_images, exist_ok=True)
        os.makedirs(dst_labels, exist_ok=True)
        fmt = str(info.get("fmt", "txt")).lstrip(".")
        imgs = set()
        all_img_dirs = get_paths(info, "image")
        for img_dir, label_dir in _paired_dirs(info):
            imgs |= _copy_images(img_dir, dst_images)
            _copy_dataset_labels(label_dir, fmt, dst_labels, label_to_id,
                                 _label_img_dirs(img_dir, all_img_dirs),
                                 as_polygon, info.get("label_ids"))
            _override_by_same_dir_json(img_dir, dst_labels, label_to_id,
                                       as_polygon)
        n_lab = len([f for f in os.listdir(dst_labels)
                     if f.lower().endswith(".txt")])
        print("[train] 复制数据集 {}: 图像 {} 张, 标签 {} 个 → {}".format(
            ds_name, len(imgs), n_lab, dst), flush=True)
    return labels, label_to_id


def _override_by_same_dir_json(img_dir, dst_labels, label_to_id, as_polygon):
    """图像同路径的 labelme json(标注界面产物)是权威来源, 覆盖导入标签目录的结果。"""
    if not img_dir or not os.path.isdir(img_dir):
        return
    for fn in sorted(os.listdir(img_dir)):
        if not fn.lower().endswith(".json"):
            continue
        stem = os.path.splitext(fn)[0]
        iw, ih = _img_size_of_stem(img_dir, stem)
        if not (iw and ih):
            continue
        jp = os.path.join(img_dir, fn)
        if not looks_like_labelme(jp):
            continue
        shapes = load_json_shapes(jp)
        txt = shapes_to_yolo_text(shapes, iw, ih, label_to_id, as_polygon)
        # 空 shapes 也要写(清空), 否则界面删掉的框会在训练里复活
        with open(os.path.join(dst_labels, stem + ".txt"), "w",
                  encoding="utf-8") as f:
            f.write(txt)


def clean_split(out_root):
    """清空 train/val 合并目录(防止上一轮遗留旧标签，如未重映射的 ID)。"""
    for split in ("train", "val"):
        for sub in ("images", "labels"):
            d = os.path.join(out_root, split, sub)
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                p = os.path.join(d, fn)
                if os.path.isfile(p):
                    os.remove(p)


def _unique_dst(d, fn, used=None):
    """
    目标已存在同名文件时加序号(多数据集合并防覆盖，图像/txt 名保持一致)。
    used 为该目录已占用的文件名集合(可选)。原实现每次都从 i=1 重新用
    os.path.exists 逐个探测, 重名文件多时是 O(K²) 次系统调用; 传入 used
    后改为集合判断, 同一目录内跨数据集连续累加。
    """
    if used is None:
        dst = os.path.join(d, fn)
        if not os.path.exists(dst):
            return dst
        base, ext = os.path.splitext(fn)
        i = 1
        while os.path.exists(os.path.join(d, "{}_{}{}".format(base, i, ext))):
            i += 1
        return os.path.join(d, "{}_{}{}".format(base, i, ext))
    if fn not in used:
        used.add(fn)
        return os.path.join(d, fn)
    base, ext = os.path.splitext(fn)
    i = 1
    while "{}_{}{}".format(base, i, ext) in used:
        i += 1
    new = "{}_{}{}".format(base, i, ext)
    used.add(new)
    return os.path.join(d, new)


def merge_split(out_root, datasets):
    """把勾选数据集副本合并进 <out_root>/train 或 val(同名自动加序号，不覆盖)。"""
    used_names = {}          # (split, sub) → 该目录已占用的文件名集合
    for info in datasets:
        src = os.path.join(out_root, info.get("project", ""), info["dataset_name"])
        merged = 0
        for sub in ("images", "labels"):
            s = os.path.join(src, sub)
            d = os.path.join(out_root, info["split"], sub)
            os.makedirs(d, exist_ok=True)
            if not os.path.isdir(s):
                continue
            key = (info["split"], sub)
            if key not in used_names:
                used_names[key] = set(os.listdir(d))
            used = used_names[key]
            for fn in os.listdir(s):
                shutil.copy2(os.path.join(s, fn), _unique_dst(d, fn, used))
                merged += 1
        print("[train] 合并 {} 数据集 → {} ({} 个文件)".format(
            info["dataset_name"], info["split"], merged), flush=True)


def write_data_yaml(out_root, labels):
    """生成 <out_root>/data.yaml（train/val 合并目录 + names）。"""
    lines = ["path: .", "train: train", "val: val", "", "names:"]
    for i, lb in enumerate(labels):
        lines.append("  {}: {}".format(i, lb))
    with open(os.path.join(out_root, "data.yaml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("[train] 生成 data.yaml → {}".format(
        os.path.join(out_root, "data.yaml")), flush=True)
