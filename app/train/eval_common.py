# -*- coding: utf-8 -*-
"""测试脚本(eval_runner / ocr_test_runner)共用的取数小工具(子进程里跑, 不碰主进程 utils)."""

import os

from app.core.constants import IMAGE_EXTS


def list_images(img_dir):
    """返回图片文件绝对路径列表(按名称排序, 稳定复现)."""
    if not os.path.isdir(img_dir):
        return []
    names = [n for n in os.listdir(img_dir)
             if os.path.splitext(n)[1].lower() in IMAGE_EXTS]
    return [os.path.join(img_dir, n) for n in sorted(names)]


def collect_pairs(cfg):
    """
    展开成 [(图片路径, 标签目录), ...], 支持一次测多个数据集.
    标签按文件名在"该图片所属数据集的"标签目录里找, 不同数据集的同名图片
    不会串, 所以必须逐目录配对而不是共用一个 label_dir.
    兼容旧 cfg: 没有 items 时退回单条 image_path/label_path.
    """
    items = cfg.get("items") or [
        {"image_path": cfg.get("image_path", ""),
         "label_path": cfg.get("label_path", "")}]
    pairs = []
    for it in items:
        label_dir = it.get("label_path") or ""
        for img in list_images(it.get("image_path") or ""):
            pairs.append((img, label_dir))
    return pairs


def dataset_list(cfg):
    """cfg 里去重后的 [(项目, 数据集)], 报告首页要显示"测的是哪个数据集"."""
    out, seen = [], set()
    for it in cfg.get("items") or []:
        key = (str(it.get("project") or ""), str(it.get("dataset") or ""))
        if key[1] and key not in seen:
            seen.add(key)
            out.append({"project": key[0], "dataset": key[1]})
    return out
