# -*- coding: utf-8 -*-
"""
训练指标: metrics.csv 解析, 各任务主指标的取值口径, 错误率计算
"""
import csv
import io
from collections import namedtuple

from PySide6.QtCore import QT_TRANSLATE_NOOP

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

# 任务 → 主指标. base 交给 metric_key 解析实际列(分割的 mask_ 前缀, ema 优先都在那);
# field 是训练记录里存这个值的字段名 —— 异常检测的 AUROC 落在 map50 字段上是历史包袱,
# 换字段名老记录就读不出精度了; direction 1=越大越好, -1=越小越好, 错误率类指标取
# max 不报错, 只会静默把最差的那一轮当成最好.
Primary = namedtuple("Primary", "base field label direction decimals")

PRIMARY = {
    "detect": Primary(
        "mAP@50", "map50", QT_TRANSLATE_NOOP("MetricLabel", "mAP@50"), 1, 3),
    "segment": Primary(
        "mAP@50", "map50", QT_TRANSLATE_NOOP("MetricLabel", "mask mAP50"), 1, 3),
    "classify": Primary(
        "accuracy", "accuracy", QT_TRANSLATE_NOOP("MetricLabel", "准确率"), 1, 4),
    "ad": Primary(
        "auroc", "map50", QT_TRANSLATE_NOOP("MetricLabel", "AUROC"), 1, 3),
    # 检测段的预测不带置信度, 排不出 AP, 只能给 IoU@0.5 下的 F1
    "ocr_det": Primary(
        "F1@0.5", "map50", QT_TRANSLATE_NOOP("MetricLabel", "F1@0.5"), 1, 3),
    "ocr_rec": Primary(
        "CER", "cer", QT_TRANSLATE_NOOP("MetricLabel", "CER"), -1, 4),
}


def series_from_csv(csv_path):
    """
    全量解析训练的 metrics.csv; 同一 epoch 多行时后写的值覆盖先写的.
    返回 {"epochs": [...], "ema_mAP@50": [...], ...}, 只有出现过值的列才会出现.
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
    series 里 base 指标实际用哪个键, 优先 ema; 没有返回 ''.
    分割任务看 mask_* 列(按有无 mask 系列判定, 不能按键存在性回退:
    旧分割记录没有 mask_ema 列).
    """
    is_seg = bool(series.get("mask_" + base)) or bool(series.get("mask_ema_" + base))
    pfx = "mask_" if is_seg else ""
    for k in (pfx + "ema_" + base, pfx + base):
        if series.get(k):
            return k
    return ""


def primary_for(task):
    """任务键 → 主指标定义; 未登记返回 None."""
    return PRIMARY.get(str(task or ""))


def primary_of(series, task=""):
    """
    该 series 的主指标定义: 有 task 一律用 task, 否则按 series 内容推断.

    推断只认得出 auroc/accuracy —— CER 这类错误率指标在 series 里没有特征,
    不靠 task 就会被当成 mAP@50 取不到值, 所以新任务必须登记进 PRIMARY.
    """
    p = primary_for(task)
    if p is not None:
        return p
    if "auroc" in series:
        return PRIMARY["ad"]
    if "accuracy" in series:
        return PRIMARY["classify"]
    return PRIMARY["detect"]


def best_value(series, base, direction=1):
    """该指标的全序列最优值; 无数据返回 None(序列尾部常有补齐的 None 占位).

    direction=-1 取最小: CER/WER 这类错误率越小越好.
    """
    key = metric_key(series, base)
    if not key:
        return None
    vals = [float(v) for v in (series.get(key) or []) if v is not None]
    if not vals:
        return None
    return max(vals) if direction >= 0 else min(vals)


def best_map50_from_csv(csv_path):
    """metrics.csv → 交付精度与 mAP@50-95; 读不到返回 {}."""
    series = series_from_csv(csv_path)
    out = {}
    for key, base in (("map50", "mAP@50"), ("map50_95", "mAP@50-95")):
        v = best_value(series, base)
        if v is not None:
            out[key] = round(v, 4)
    return out


def edit_distance(a, b):
    """字符级编辑距离(Levenshtein); 两行滚动数组, 内存 O(len(b))."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def cer(refs, hyps):
    """
    字符错误率(微平均): 所有框的编辑距离之和 ÷ 参考字符总数.

    微平均让长串权重更大, 口径是"这批字整体有多少读错", 与产线报数一致;
    宏平均(逐框算 CER 再取平均)会把只错一个字的短串放大成 100% 后拉平.
    参考总长为 0 时返回 None, 不返回 0 —— 0 会被当成完美.
    """
    if len(refs) != len(hyps):
        raise ValueError("CER 要求参考与预测成对: {} vs {}".format(
            len(refs), len(hyps)))
    total = sum(len(r) for r in refs)
    if not total:
        return None
    return sum(edit_distance(r, h) for r, h in zip(refs, hyps)) / float(total)
