# -*- coding: utf-8 -*-
"""测试执行脚本（由 UI 以子进程方式启动）。

用法: python -m app.train.test_runner <config.json>
config 字段（dialogs.py _on_start_test 组装）：
  model_path   训练输出的 best total checkpoint（.pth）
  image_path   测试数据集图片目录
  label_path   标注目录（可选；为空即推理模式）
  iou_threshold IoU 阈值（评估模式用）
  confidence   置信度阈值（predict 过滤低置信框）
  has_label    是否有标注
"""

import json
import logging
import os
import sys
import traceback
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)
logging.getLogger("rf-detr").setLevel(logging.ERROR)

_WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
for _p in (_WORKSPACE, os.path.join(_WORKSPACE, "app")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from PIL import Image

try:
    import torch
except ImportError:
    torch = None

try:
    from rfdetr import RFDETR   # from_checkpoint 自动推断检测/分割模型类
except ImportError:
    RFDETR = None

_IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp")


def _list_images(img_dir):
    """返回图片文件绝对路径列表（按名称排序，稳定复现）。"""
    if not os.path.isdir(img_dir):
        return []
    names = [n for n in os.listdir(img_dir)
             if n.lower().endswith(_IMG_EXTS)]
    return [os.path.join(img_dir, n) for n in sorted(names)]


def _read_yolo_label(txt_path, img_w, img_h):
    """YOLO txt → [(cls, 像素[x1,y1,x2,y2])] 列表。

    兼容两种格式：检测 `cls cx cy w h`（5 个数，中心点+宽高）；
    分割 `cls x1 y1 x2 y2 ...`（>=7 个数，多边形顶点）→ 取外接框。
    cls 为标注类别（str）。
    """
    boxes = []
    if not os.path.exists(txt_path):
        return boxes
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            p = line.split()
            if len(p) < 5:
                continue
            try:
                vals = [float(x) for x in p[1:]]
            except ValueError:
                continue
            if len(vals) == 4:
                # YOLO 检测：cx cy w h（归一化）
                cx, cy, w, h = vals
                x1 = (cx - w / 2) * img_w
                y1 = (cy - h / 2) * img_h
                x2 = (cx + w / 2) * img_w
                y2 = (cy + h / 2) * img_h
            else:
                # YOLO 分割：多边形顶点（偶数个坐标）→ 外接框
                xs = vals[0::2]
                ys = vals[1::2]
                if not xs or not ys:
                    continue
                x1, x2 = min(xs) * img_w, max(xs) * img_w
                y1, y2 = min(ys) * img_h, max(ys) * img_h
            boxes.append((p[0].strip(), [x1, y1, x2, y2]))
    return boxes


def _iou(a, b):
    """两个 [x1,y1,x2,y2] 框的 IoU。"""
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return inter / (area_a + area_b - inter)


def _write_labelme_json(img_path, boxes, class_names):
    """写 labelme JSON（rectangle）到图片同目录，同名 .json 覆盖。

    boxes: [[x1,y1,x2,y2],...]，class_names 与 boxes 一一对应（无类别名时兜底 object）。
    """
    with Image.open(img_path) as im:
        iw, ih = im.size
    shapes = []
    for i, b in enumerate(boxes):
        cn = class_names[i] if i < len(class_names) and class_names[i] else "object"
        shapes.append({
            "label": cn,
            "points": [[b[0], b[1]], [b[2], b[3]]],
            "group_id": None,
            "shape_type": "rectangle",
            "flags": {},
        })
    data = {
        "version": "5.5.0",
        "flags": {},
        "shapes": shapes,
        "imagePath": os.path.basename(img_path),
        "imageData": None,
        "imageHeight": ih,
        "imageWidth": iw,
    }
    out = os.path.splitext(img_path)[0] + ".json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _tally(pc, key, cls):
    """按类别累加统计：pc[cls] = {gt, tp, fp, fn, det}。"""
    d = pc.setdefault(str(cls), {"gt": 0, "tp": 0, "fp": 0, "fn": 0, "det": 0})
    d[key] += 1


def _match(preds, gts, iou_th, per_class):
    """
    预测框与标注框匹配（不看类别）：IoU≥阈值即算检出。
    贪心：每个 GT 只匹配一个 IoU 最大的预测框；预测框无匹配则 FP，GT 无匹配则 FN。
    preds/gts 为 [(cls, [x1,y1,x2,y2])]；per_class 按类别累加（dict 原地修改）。
    统计口径：TP 归 GT 类别（检出了哪个类的目标），FP 归预测类别，FN 归 GT 类别。
    返回 (tp, fp, fn)。
    """
    tp = fp = 0
    gt_matched = [False] * len(gts)
    for p_cls, p in preds:
        _tally(per_class, "det", p_cls)
        best_iou, best_gi = 0.0, -1
        for gi, (g_cls, g) in enumerate(gts):
            if gt_matched[gi]:
                continue
            iou = _iou(p, g)
            if iou > best_iou:
                best_iou, best_gi = iou, gi
        if best_iou >= iou_th and best_gi >= 0:
            tp += 1
            gt_matched[best_gi] = True
            _tally(per_class, "tp", gts[best_gi][0])
        else:
            fp += 1
            _tally(per_class, "fp", p_cls)
    fn = 0
    for gi, (g_cls, g) in enumerate(gts):
        _tally(per_class, "gt", g_cls)
        if not gt_matched[gi]:
            fn += 1
            _tally(per_class, "fn", g_cls)
    return tp, fp, fn


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if RFDETR is None:
        raise RuntimeError("rfdetr 未安装，无法执行测试")
    print("[test] 加载模型: {}".format(os.path.basename(cfg["model_path"])),
          flush=True)
    model = RFDETR.from_checkpoint(cfg["model_path"])
    device = cfg.get("device", "cuda")
    if device.startswith("cuda") and hasattr(model, "to") \
            and torch is not None and torch.cuda.is_available():
        model.to(device)
    if hasattr(model, "inference"):
        try:
            dtype = torch.float16 if device.startswith("cuda") \
                and torch is not None and torch.cuda.is_available() \
                else torch.float32
            model.inference(dtype=dtype, compile=False)
            print("[test] 推理已优化: {}".format(dtype), flush=True)
        except Exception:
            pass

    imgs = _list_images(cfg["image_path"])
    print("[test] 测试图片 {} 张".format(len(imgs)), flush=True)
    conf_th = float(cfg.get("confidence", 0.5))
    iou_th = float(cfg.get("iou_threshold", 0.5))
    has_label = bool(cfg.get("has_label"))
    label_dir = cfg.get("label_path") or ""

    tp = fp = fn = 0
    per_class = {}           # {cls: {gt,tp,fp,fn,det}}
    output_labels = bool(cfg.get("output_labels"))
    for i, img_path in enumerate(imgs):
        try:
            det = model.predict(img_path, threshold=conf_th)
            if isinstance(det, list):
                det = det[0]
            xyxy = getattr(det, "xyxy", None)
            preds = []          # [(cls, box)]
            class_names = []    # 与 preds 对应的类别名
            if xyxy is not None:
                data = getattr(det, "data", {}) or {}
                cnames_raw = data.get("class_name")
                cnames = list(cnames_raw) if cnames_raw is not None else []
                cids = getattr(det, "class_id", None)
                for k, x in enumerate(xyxy):
                    box = [float(x[0]), float(x[1]),
                           float(x[2]), float(x[3])]
                    if k < len(cnames) and cnames[k]:
                        cn = str(cnames[k])
                    elif cids is not None and k < len(cids):
                        cn = str(int(cids[k]))
                    else:
                        cn = "object"
                    class_names.append(cn)
                    preds.append((cn, box))
        except Exception as exc:
            print("[test] 预测失败 {}: {}".format(
                os.path.basename(img_path), exc), flush=True)
            traceback.print_exc()
            preds = []
            class_names = []
        if output_labels and preds:
            try:
                _write_labelme_json(
                    img_path, [b for _, b in preds], class_names)
            except Exception as exc:
                print("[test] 输出标注失败 {}: {}".format(
                    os.path.basename(img_path), exc), flush=True)
        if has_label:
            with Image.open(img_path) as im:
                iw, ih = im.size
            txt = os.path.join(label_dir,
                               os.path.splitext(os.path.basename(img_path))[0]
                               + ".txt")
            gts = _read_yolo_label(txt, iw, ih)
            t, f_p, f_n = _match(preds, gts, iou_th, per_class)
            tp += t
            fp += f_p
            fn += f_n
        if (i + 1) % 10 == 0 or i + 1 == len(imgs):
            print("[test] 进度 {}/{}".format(i + 1, len(imgs)), flush=True)

    result = {"ok": True, "total": len(imgs)}
    if has_label:
        p = tp / (tp + fp) if (tp + fp) else 0.0
        r = tp / (tp + fn) if (tp + fn) else 0.0
        result.update({"P": p, "R": r, "TP": tp, "FP": fp, "FN": fn,
                       "per_class": per_class})
        print("[test] P={:.4f} R={:.4f} TP={} FP={} FN={}".format(
            p, r, tp, fp, fn), flush=True)
    print("[test] RESULT " + json.dumps(result, ensure_ascii=False),
          flush=True)


if __name__ == "__main__":
    main()
