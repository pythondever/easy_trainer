# -*- coding: utf-8 -*-
"""
训练指标读取：metrics.csv 解析
"""
import csv
import io

from app.core.utils import read_text_any


CSV_KEYS = (
    ("mAP@50-95", "val/mAP_50_95"), ("mAP@50", "val/mAP_50"),
    ("precision", "val/precision"), ("recall", "val/recall"),
    ("F1", "val/F1"), ("mAR", "val/mAR"),
    ("ema_mAP@50", "val/ema_mAP_50"), ("ema_mAP@50-95", "val/ema_mAP_50_95"),
    ("mask_mAP@50", "val/segm_mAP_50"), ("mask_mAP@50-95", "val/segm_mAP_50_95"),
    ("mask_ema_mAP@50", "val/ema_segm_mAP_50"),
    ("mask_ema_mAP@50-95", "val/ema_segm_mAP_50_95"),
    ("train_loss", "train/loss"), ("val_loss", "val/loss"),
)


def series_from_csv(csv_path):
    """
    全量解析训练的 metrics.csv; 同一 epoch 多行时后写的值覆盖先写的。
    返回 {"epochs": [...], "ema_mAP@50": [...], ...}，只有出现过值的列才会出现。
    """
    try:
        # lightning 用系统 ANSI 码页写 CSV(中文类别名下是 gbk), 不能固定按 utf-8 解
        rows = list(csv.DictReader(io.StringIO(read_text_any(csv_path))))
    except OSError:
        return {}
    by_epoch = {}
    for r in rows:
        try:
            ep = int(float(r.get("epoch", 0)))
        except (TypeError, ValueError):
            continue
        merged = by_epoch.setdefault(ep, {})
        for k, v in r.items():
            if v not in (None, ""):
                merged[k] = v
    series = {"epochs": sorted(by_epoch)}
    for key, csv_key in CSV_KEYS:
        vals = []
        for ep in series["epochs"]:
            try:
                vals.append(float(by_epoch[ep].get(csv_key)))
            except (TypeError, ValueError):
                vals.append(None)
        if any(v is not None for v in vals):
            series[key] = vals
    return series


def metric_key(series, base):
    """
    series 里 base 指标实际用哪个键，优先 ema；没有返回 ''。
    分割任务看 mask_* 列（按有无 mask 系列判定，不能按键存在性回退：
    旧分割记录没有 mask_ema 列）。
    """
    is_seg = bool(series.get("mask_" + base)) or bool(series.get("mask_ema_" + base))
    pfx = "mask_" if is_seg else ""
    for k in (pfx + "ema_" + base, pfx + base):
        if series.get(k):
            return k
    return ""


def best_value(series, base):
    """该指标的全序列最大值；无数据返回 None（序列尾部常有补齐的 None 占位）。"""
    key = metric_key(series, base)
    if not key:
        return None
    vals = [float(v) for v in (series.get(key) or []) if v is not None]
    return max(vals) if vals else None


def best_map50(series):
    """交付精度：分类看 accuracy，检测/分割看 mAP@50 全序列最大。"""
    if "accuracy" in series:
        return best_value(series, "accuracy")
    return best_value(series, "mAP@50")


def best_map50_from_csv(csv_path):
    """metrics.csv → 交付精度与 mAP@50-95；读不到返回 {}。"""
    series = series_from_csv(csv_path)
    out = {}
    for key, base in (("map50", "mAP@50"), ("map50_95", "mAP@50-95")):
        v = best_value(series, base)
        if v is not None:
            out[key] = round(v, 4)
    return out
