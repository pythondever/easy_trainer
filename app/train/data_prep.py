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

from app.label_utils import (normalize_label, load_json_boxes,
                             boxes_to_yolo_text)


def timestamp_dir():
    return datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


def _img_size(path):
    try:
        with Image.open(path) as im:
            return im.size
    except Exception:
        return (0, 0)


def _copy_dataset_labels(src_label_path, fmt, dst_labels, label_to_id, img_dir):
    """复制单个标签到 yolo txt 目录（labelme json 先转 txt）。返回出现过的标签。"""
    if not src_label_path or not os.path.isdir(src_label_path):
        return set()
    labels_found = set()
    for fn in os.listdir(src_label_path):
        if fmt == "json" and fn.lower().endswith(".json"):
            boxes = load_json_boxes(os.path.join(src_label_path, fn))
            if not boxes:
                continue
            for b in boxes:
                labels_found.add(b[4])
            iw, ih = 0, 0
            if img_dir:
                for ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
                    p = os.path.join(img_dir, os.path.splitext(fn)[0] + ext)
                    if os.path.exists(p):
                        iw, ih = _img_size(p)
                        break
            if iw and ih:
                txt = boxes_to_yolo_text(boxes, iw, ih, label_to_id)
                base = os.path.splitext(fn)[0] + ".txt"
                with open(os.path.join(dst_labels, base), "w", encoding="utf-8") as f:
                    f.write(txt)
        elif fmt == "txt" and fn.lower().endswith(".txt"):
            # txt 标签：class ID 重映射到 0..N-1(原始数据集可能非零基，如 1~14)
            src = os.path.join(src_label_path, fn)
            try:
                lines = []
                with open(src, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.split()
                        if len(parts) >= 5:
                            new_cid = label_to_id.get(parts[0], parts[0])
                            lines.append(" ".join([str(new_cid)] + parts[1:]))
                if lines:
                    with open(os.path.join(dst_labels, fn), "w",
                              encoding="utf-8") as f:
                        f.write("\n".join(lines) + "\n")
            except Exception:
                pass
    return labels_found


def _collect_labels(datasets, label_to_id):
    """扫描所有数据集标签收集完整类别集合（txt 直接读行，json 读 label）。"""
    labels = []
    for info in datasets:
        label_path = info.get("label_path")
        fmt = str(info.get("fmt", "txt")).lstrip(".")
        if not label_path or not os.path.isdir(label_path):
            continue
        for fn in sorted(os.listdir(label_path)):
            if fmt == "json" and fn.lower().endswith(".json"):
                for b in load_json_boxes(os.path.join(label_path, fn)):
                    if b[4] not in labels:
                        labels.append(b[4])
            elif fmt == "txt" and fn.lower().endswith(".txt"):
                try:
                    with open(os.path.join(label_path, fn), "r", encoding="utf-8") as f:
                        for line in f:
                            p = line.split()
                            if len(p) >= 1:
                                lb = normalize_label(p[0])
                                if lb not in labels:
                                    labels.append(lb)
                except Exception:
                    continue
    return labels


def _copy_images(src_img_path, dst_images):
    """复制图像（扁平目录）。返回图像文件名集合。"""
    copied = set()
    if not src_img_path or not os.path.isdir(src_img_path):
        return copied
    for fn in os.listdir(src_img_path):
        if fn.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff")):
            shutil.copy2(os.path.join(src_img_path, fn), os.path.join(dst_images, fn))
            copied.add(fn)
    return copied


def _sort_labels(labels):
    """类别排序：数字标签按数值升序，非数字按字符串（保证 txt ID 重映射稳定）。"""
    def key(x):
        return (0, int(x)) if str(x).isdigit() else (1, str(x))
    return sorted(set(labels), key=key)


def copy_datasets(out_root, project, datasets):
    """把勾选数据集复制到 <out_root>/<项目>/<数据集>/images|labels（json→txt）。"""
    labels = _sort_labels(_collect_labels(datasets, {}))
    label_to_id = {lb: i for i, lb in enumerate(labels)}
    print("[train] 解析到类别 {} 个: {}".format(len(labels), labels), flush=True)
    for info in datasets:
        ds_name = info["dataset_name"]
        dst = os.path.join(out_root, project, ds_name)
        dst_images = os.path.join(dst, "images")
        dst_labels = os.path.join(dst, "labels")
        os.makedirs(dst_images, exist_ok=True)
        os.makedirs(dst_labels, exist_ok=True)
        imgs = _copy_images(info.get("image_path"), dst_images)
        _copy_dataset_labels(
            info.get("label_path"), str(info.get("fmt", "txt")).lstrip("."),
            dst_labels, label_to_id, info.get("image_path"))
        n_lab = len([f for f in os.listdir(dst_labels)
                     if f.lower().endswith(".txt")])
        print("[train] 复制数据集 {}: 图像 {} 张, 标签 {} 个 → {}".format(
            ds_name, len(imgs), n_lab, dst), flush=True)
        # 图像同路径的 labelme json(标注系统生成) -> txt 覆盖
        if info.get("image_path") and os.path.isdir(info["image_path"]):
            for fn in os.listdir(info["image_path"]):
                if fn.lower().endswith(".json"):
                    jp = os.path.join(info["image_path"], fn)
                    boxes = load_json_boxes(jp)
                    if not boxes:
                        continue
                    iw, ih = _img_size(os.path.join(info["image_path"],
                                                    os.path.splitext(fn)[0] + ".jpg"))
                    if iw and ih:
                        txt = boxes_to_yolo_text(boxes, iw, ih, label_to_id)
                        base = os.path.splitext(fn)[0] + ".txt"
                        with open(os.path.join(dst_labels, base), "w",
                                  encoding="utf-8") as f:
                            f.write(txt)
    return labels, label_to_id


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


def _unique_dst(d, fn):
    """目标已存在同名文件时加序号(多数据集合并防覆盖，图像/txt 名保持一致)。"""
    dst = os.path.join(d, fn)
    if not os.path.exists(dst):
        return dst
    base, ext = os.path.splitext(fn)
    i = 1
    while os.path.exists(os.path.join(d, "{}_{}{}".format(base, i, ext))):
        i += 1
    return os.path.join(d, "{}_{}{}".format(base, i, ext))


def merge_split(out_root, datasets):
    """把勾选数据集副本合并进 <out_root>/train 或 val(同名自动加序号，不覆盖)。"""
    for info in datasets:
        src = os.path.join(out_root, info.get("project", ""), info["dataset_name"])
        merged = 0
        for sub in ("images", "labels"):
            s = os.path.join(src, sub)
            d = os.path.join(out_root, info["split"], sub)
            os.makedirs(d, exist_ok=True)
            if not os.path.isdir(s):
                continue
            for fn in os.listdir(s):
                shutil.copy2(os.path.join(s, fn), _unique_dst(d, fn))
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
