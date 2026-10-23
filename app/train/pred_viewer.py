# -*- coding: utf-8 -*-
"""
验证集预测明细: 读 eval_runner 写的 details.jsonl, 把每张图的预测情况画出来.

明细只记有问题的图: missing 是没匹配上的真值, spurious 是没匹配上的预测,
hits 是匹配上的那一对. 匹配是贪心一对一, 每个预测要么进 hits 要么进
spurious, 所以预测的全集就是这两项之和, 不用再跑一遍模型.

注意 hits 落盘的只有预测侧(类别/框/轮廓), 没存配对的那个真值框: IoU 已经
过阈值, 两者位置基本重合, 画预测框就够表达"这里检出了".
"""

import json
import os

import cv2
import numpy as np
import PIL.Image as PILImage

from app.core.image_utils import make_uniform_thumb
from app.train.aug_preview import _draw_texts, read_image


# 三类标注靠颜色+线型+填充三重区分: 单看线型, 缩略图和大图上都分不清漏检和误检.
#   漏检 = 亮红实线 + 淡填充: 真值客观存在, 模型没看见
#   误检 = 橙黄虚线: 模型多说出来的, 实际没有
#   检出 = 青绿虚线: 与真值匹配上的预测
# 界面底部有同色图例, 改这里要同步 dialog 的 _legend
GT_MISS = (86, 86, 230)      # BGR 亮红
PRED_FP = (0, 190, 255)      # BGR 橙黄
PRED_OK = (120, 200, 80)     # BGR 青绿

MISS = "miss"     # 有漏检
FP = "fp"         # 有误检


def load_rows(detail_path):
    """读明细, 按问题框数降序返回. 文件不在或读坏都给空表."""
    rows = []
    if not detail_path or not os.path.isfile(detail_path):
        return rows
    try:
        with open(detail_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except ValueError:
                    continue
                img = str(data.get("img") or "")
                if not img:
                    continue
                rows.append({
                    "img": img,
                    "missing": list(data.get("missing") or []),
                    "spurious": list(data.get("spurious") or []),
                    "hits": list(data.get("hits") or []),
                })
    except OSError:
        return []
    # 问题多的排前面: 打开就想先看最严重的那几张
    rows.sort(key=lambda r: len(r["missing"]) + len(r["spurious"]),
              reverse=True)
    return rows


def row_flags(row):
    """这张图有哪几类问题, 返回 MISS/FP 的集合."""
    out = set()
    if row["missing"]:
        out.add(MISS)
    if row["spurious"]:
        out.add(FP)
    return out


def select(rows, kind):
    """按状态筛图. all 是全部有问题的图."""
    if kind == "all":
        return list(rows)
    return [r for r in rows if kind in row_flags(r)]


def summary(rows):
    """检测/分割按框统计: 漏检框数、误检框数、涉及图片数."""
    miss_boxes = sum(len(r["missing"]) for r in rows)
    fp_boxes = sum(len(r["spurious"]) for r in rows)
    return {
        "miss_boxes": miss_boxes,
        "fp_boxes": fp_boxes,
        "miss_imgs": sum(1 for r in rows if r["missing"]),
        "fp_imgs": sum(1 for r in rows if r["spurious"]),
    }


def _shape_of(item, task):
    """取一个明细项的几何: 分割优先用轮廓, 检测退到外接框."""
    poly = item.get("poly")
    if task == "segment" and poly:
        rings = [np.asarray(ring, np.float32).reshape(-1, 2)
                 for ring in poly if len(ring) >= 3]
        rings = [r for r in rings if len(r)]
        if rings:
            return "poly", rings
    box = item.get("box") or [0, 0, 0, 0]
    return "box", np.asarray(box, np.float32).reshape(-1, 2)


def _anchor(pts):
    """整体左上角, 标签就放这儿. 分割可能是多个环, 得合起来取."""
    arr = np.vstack(pts) if isinstance(pts, list) else pts
    return int(arr[:, 0].min()), int(arr[:, 1].min())


def _draw_one(out, kind, pts, color, task, thickness):
    if kind == "poly":
        for ring in pts:
            poly = ring.astype(np.int32)
            overlay = out.copy()
            cv2.fillPoly(overlay, [poly], color)
            cv2.addWeighted(overlay, 0.28, out, 0.72, 0, out)
            cv2.polylines(out, [poly], True, color, thickness, cv2.LINE_AA)
        return
    x1, y1, x2, y2 = [int(round(v)) for v in
                      (pts[:, 0].min(), pts[:, 1].min(),
                       pts[:, 0].max(), pts[:, 1].max())]
    # 漏检的位置填一层淡色: 只有轮廓的话, 小缺陷在缩略图里根本看不出来
    overlay = out.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
    cv2.addWeighted(overlay, 0.30, out, 0.70, 0, out)
    cv2.rectangle(out, (x1, y1), (x2, y2), color, thickness, cv2.LINE_AA)


def render(row, task):
    """
    画一张图的预测情况, 返回 BGR 图; 图读不出来给 None.

    漏检的真值画亮红实线并填淡红, 误检的预测画橙黄虚线, 匹配上的预测画青绿
    虚线——颜色区分问题类型, 线型区分是真值还是模型说的, 填充只给漏检.
    """
    img = read_image(row["img"])
    if img is None:
        return None
    out = img.copy()
    thickness = max(1, int(round(min(out.shape[:2]) / 320.0)))
    texts = []

    for item in row["missing"]:
        kind, pts = _shape_of(item, task)
        _draw_one(out, kind, pts, GT_MISS, task, thickness)
        texts.append((str(item.get("cls") or ""),
                      *_anchor(pts), GT_MISS))

    for item in row["spurious"]:
        kind, pts = _shape_of(item, task)
        _draw_dashed(out, kind, pts, PRED_FP, task, thickness)
        texts.append((_label_of(item), *_anchor(pts), PRED_FP))

    for item in row["hits"]:
        kind, pts = _shape_of(item, task)
        _draw_dashed(out, kind, pts, PRED_OK, task, thickness)
        texts.append((_label_of(item), *_anchor(pts), PRED_OK))

    texts = [t for t in texts if t[0]]
    if texts:
        out = _draw_texts(out, texts)
    return out


def _label_of(item):
    name = str(item.get("cls") or "")
    conf = item.get("conf")
    if conf is None:
        return name
    return "{} {:.2f}".format(name, float(conf))


def thumbnail(path, size):
    """列表用小图: 只提示是哪张图, 不画框(五十来像素上画框只是噪音)."""
    try:
        pil = PILImage.open(path).convert("RGB")
        return make_uniform_thumb(pil, (size, size))
    except Exception:
        return None


def _draw_dashed(out, kind, pts, color, task, thickness):
    """虚线: cv2 没有虚线多边线, 按段自己拼."""
    if kind == "poly":
        for ring in pts:
            _dashed_poly(out, ring.astype(np.int32), color, thickness)
        return
    x1, y1, x2, y2 = [int(round(v)) for v in
                      (pts[:, 0].min(), pts[:, 1].min(),
                       pts[:, 0].max(), pts[:, 1].max())]
    for (ax, ay), (bx, by) in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)),
                               ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        _dashed_seg(out, (ax, ay), (bx, by), color, thickness)


def _dashed_seg(out, a, b, color, thickness):
    ax, ay = a
    bx, by = b
    length = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
    if length < 1:
        return
    dash = max(6.0, thickness * 4.0)
    gap = dash * 0.6
    steps = int(length // (dash + gap)) + 1
    ux, uy = (bx - ax) / length, (by - ay) / length
    for i in range(steps):
        s = i * (dash + gap)
        e = min(s + dash, length)
        if e <= s:
            break
        cv2.line(out, (int(round(ax + ux * s)), int(round(ay + uy * s))),
                 (int(round(ax + ux * e)), int(round(ay + uy * e))),
                 color, thickness, cv2.LINE_AA)


def _dashed_poly(out, poly, color, thickness):
    n = len(poly)
    for i in range(n):
        a = tuple(int(v) for v in poly[i])
        b = tuple(int(v) for v in poly[(i + 1) % n])
        _dashed_seg(out, a, b, color, thickness)
