# -*- coding: utf-8 -*-
"""
字符检测/识别测试执行脚本(由 UI 以子进程方式启动).
用法: main(), 由 test_worker 以 -c 导入后调用(打包后是 pyd, 不能 python -m 启动)
config 字段(与 test_dialog 组装的一致):
  model_path    训练产出的 checkpoint_best.pth
  task          ocr_det / ocr_rec
  items         [{image_path, label_path, project, dataset}]
  iou_threshold / confidence / has_label / output_labels / report_dir

检测段: 每张图预测文本框, 有标注时按 IoU 匹配算 P/R/TP/FP/FN; 勾选"输出标签
文件"时把框写成 labelme json(类别为保留标签)到图像同目录, 首页重载即可看到.
识别段: 没有框就无从裁字条, 只能拿标注框裁图跑识别算 CER, 所以无标注数据集
直接报错而不是给出 0.
"""

import json
import os
import sys
import traceback

_WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
for _p in (_WORKSPACE, os.path.join(_WORKSPACE, "app")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from PIL import Image
from PySide6.QtCore import QCoreApplication as QC

from app.core import i18n
from app.core.constants import IMAGE_EXTS
from app.core.label_utils import (is_text_label, load_json_shapes,
                                  shapes_to_labelme_json, text_label)
from app.core.metrics import cer

try:
    import numpy as np
    import torch
    from doctr.models import detection, recognition
    from doctr.models.detection.zoo import detection_predictor
    from doctr.models.recognition.zoo import recognition_predictor
    from app.train import ocr_common as occ
    from app.train import ocr_data
except Exception as e:
    print("[test] " + QC.translate(
        "OcrTestRunner", "缺少测试依赖: {}").format(e), flush=True)
    sys.exit(1)

DET_ARCH = "db_mobilenet_v3_large"
REC_ARCH = "crnn_mobilenet_v3_small"


def _list_images(img_dir):
    if not os.path.isdir(img_dir):
        return []
    names = [n for n in os.listdir(img_dir)
             if os.path.splitext(n)[1].lower() in IMAGE_EXTS]
    return [os.path.join(img_dir, n) for n in sorted(names)]


def _collect_pairs(cfg):
    items = cfg.get("items") or [
        {"image_path": cfg.get("image_path", ""),
         "label_path": cfg.get("label_path", "")}]
    pairs = []
    for it in items:
        label_dir = it.get("label_path") or ""
        for img in _list_images(it.get("image_path") or ""):
            pairs.append((img, label_dir))
    return pairs


def _dataset_list(cfg):
    out, seen = [], set()
    for it in cfg.get("items") or []:
        key = (str(it.get("project") or ""), str(it.get("dataset") or ""))
        if key[1] and key not in seen:
            seen.add(key)
            out.append({"project": key[0], "dataset": key[1]})
    return out


def _iou(a, b):
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    if inter <= 0:
        return 0.0
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return inter / (area_a + area_b - inter)


def _match(preds, gts, iou_th):
    """贪心匹配: 每个 GT 只吃一个 IoU 最大的预测框."""
    tp = fp = 0
    taken = [False] * len(gts)
    missing, spurious, hits = [], [], []
    for box, conf in preds:
        best_iou, best_gi = 0.0, -1
        for gi, g in enumerate(gts):
            if taken[gi]:
                continue
            iou = _iou(box, g)
            if iou > best_iou:
                best_iou, best_gi = iou, gi
        if best_iou >= iou_th and best_gi >= 0:
            tp += 1
            taken[best_gi] = True
            hits.append((box, conf))
        else:
            fp += 1
            spurious.append((box, conf))
    for gi, g in enumerate(gts):
        if not taken[gi]:
            missing.append(g)
    return tp, fp, len(missing), missing, spurious, hits


def _device_of(cfg):
    d = str(cfg.get("device", "") or "")
    return "cuda" if d.startswith("cuda") and torch.cuda.is_available() else "cpu"


def _locate_rec(model_path, det_arch):
    """
    在同一次训练的输出目录里找同档位的识别模型: 检测段只出框, 字要靠识别段读.
    按目录名倒序取最新的那个: 检测/识别是两条记录, 重训过识别段时该用新的.
    """
    parent = os.path.dirname(os.path.dirname(os.path.abspath(model_path)))
    if not os.path.isdir(parent):
        return ""
    want = ""
    for code in occ.model_codes():
        det, reco = occ.split_arch(code)
        if det == det_arch:
            want = reco
            break
    if not want:
        return ""
    for name in sorted(os.listdir(parent), reverse=True):
        res_path = os.path.join(parent, name, "result.json")
        if not os.path.isfile(res_path):
            continue
        try:
            with open(res_path, "r", encoding="utf-8") as f:
                res = json.load(f)
        except (OSError, ValueError):
            continue
        if str(res.get("task")) != occ.RECO_TASK:
            continue
        if str(res.get("architecture")) != want:
            continue
        ck = os.path.join(parent, name, "checkpoint_best.pth")
        if os.path.isfile(ck):
            return ck
    return ""


def _rec_predictor(ckpt, model, device):
    """按训练时的画布装识别器: 画布记在 ckpt 里, 推理必须与训练同一几何."""
    size = ckpt.get("reco_size")
    if isinstance(size, (list, tuple)) and len(size) == 2:
        model.cfg["input_shape"] = (3, int(size[0]), int(size[1]))
    model.eval().to(device)
    pred = recognition_predictor(arch=model, pretrained=False)
    # 训练喂的是整条字条, 推理再按 ar>8 切块就与训练分布对不上了
    pred.split_wide_crops = False
    return pred


def _build_rec_predictor(path, device):
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    arch = str(ckpt.get("architecture") or REC_ARCH)
    vocab = str(ckpt.get("vocab") or "")
    fn = getattr(recognition, arch, None)
    if fn is None or not vocab:
        return None
    model = fn(vocab=vocab, pretrained=False, pretrained_backbone=False)
    model.load_state_dict(ckpt["state_dict"])
    return _rec_predictor(ckpt, model, device)


def _read_texts(rec, crops):
    """识别一批字条得到 [str]; 空条返回空串, 保持与框一一对应."""
    out = [""] * len(crops)
    if rec is None:
        return out
    keep = [i for i, c in enumerate(crops)
            if c.size and min(c.shape[:2]) >= 2]
    if not keep:
        return out
    try:
        for i, res in zip(keep, rec([crops[i] for i in keep])):
            out[i] = str(res[0]) if res else ""
    except Exception as exc:
        print("[test] " + QC.translate(
            "OcrTestRunner", "识别失败: {}").format(exc), flush=True)
    return out


def _quad_arrays(page, boxes):
    return [page[max(int(b[1]), 0):max(int(b[3]), 0),
                 max(int(b[0]), 0):max(int(b[2]), 0)] for b in boxes]


def _write_json(img_path, iw, ih, boxes, texts):
    shapes = []
    for i, b in enumerate(boxes):
        x1, y1, x2, y2 = b
        pts = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        shapes.append((text_label(), pts, texts[i] if i < len(texts) else ""))
    # 标志位是重载时把数据集认成 OCR 的唯一依据: 这些 json 没经过标注工具,
    # 走不到 annotation_io 那条置位路径
    data = shapes_to_labelme_json(shapes, img_path, iw, ih, ocr=True)
    data["imageData"] = None
    out = os.path.splitext(img_path)[0] + ".json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out


def _gt_boxes(json_path):
    """labelme 里的文本框转成 [[x1,y1,x2,y2]], 只取保留标签这一类."""
    boxes = []
    for label, pts, _text in load_json_shapes(json_path):
        if not is_text_label(label):
            continue
        xs = [float(p[0]) for p in pts]
        ys = [float(p[1]) for p in pts]
        boxes.append([min(xs), min(ys), max(xs), max(ys)])
    return boxes


def _crop_boxes(json_path):
    out = []
    for label, pts, text in load_json_shapes(json_path):
        if not is_text_label(label) or not str(text or ""):
            continue
        xs = [float(p[0]) for p in pts]
        ys = [float(p[1]) for p in pts]
        out.append(([min(xs), min(ys), max(xs), max(ys)], str(text)))
    return out


def _open_detail(cfg):
    out_dir = cfg.get("report_dir") or ""
    if not out_dir:
        return None
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "details.jsonl")
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                with open(path, "w", encoding="utf-8"):
                    pass
        open(path, "a", encoding="utf-8").close()
        return path
    except OSError:
        return None


def _write_detail(path, img_path, missing, spurious, hits):
    """照 test_runner 的口径: 只写有漏检或误检的图, 全对的图不落盘."""
    def item(box, conf=None):
        d = {"cls": text_label(),
             "box": [round(float(v), 1) for v in box]}
        if conf is not None:
            d["conf"] = round(float(conf), 4)
        return d

    row = {
        "img": img_path,
        "missing": [item(b) for b in missing],
        "spurious": [item(b, c) for b, c in spurious],
        "hits": [item(b, c) for b, c in hits],
    }
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError as exc:
        print("[test] " + QC.translate(
            "OcrTestRunner", "明细写入失败: {}").format(exc), flush=True)


def _run_det(cfg, ckpt):
    arch = str(ckpt.get("architecture") or DET_ARCH)
    fn = getattr(detection, arch, None)
    if fn is None:
        raise RuntimeError(QC.translate(
            "OcrTestRunner", "未知的字符检测架构: {}").format(arch))
    # 权重全部来自 ckpt, 构造时禁止联网: 默认参数会去下骨干的 ImageNet 权重
    model = fn(pretrained=False, pretrained_backbone=False)
    model.load_state_dict(ckpt["state_dict"])
    device = _device_of(cfg)
    model.eval().to(device)
    predictor = detection_predictor(arch=model, pretrained=False)

    rec_path = _locate_rec(cfg["model_path"], arch)
    rec = None
    if rec_path:
        rec = _build_rec_predictor(rec_path, device)
        if rec is not None:
            print("[test] " + QC.translate(
                "OcrTestRunner", "已加载配对识别模型: {}").format(
                os.path.basename(os.path.dirname(rec_path))), flush=True)
        else:
            print("[test] " + QC.translate(
                "OcrTestRunner", "识别模型不可用, 输出的标注只有框没有文字"),
                flush=True)

    pairs = _collect_pairs(cfg)
    if not pairs:
        raise RuntimeError(QC.translate("OcrTestRunner", "没有可用的图像, 请检查数据集"))
    print("[test] " + QC.translate(
        "OcrTestRunner", "加载字符检测模型: {}").format(arch), flush=True)
    print("[test] " + QC.translate(
        "OcrTestRunner", "测试图片 {} 张").format(len(pairs)), flush=True)
    conf_th = float(cfg.get("confidence", 0.5))
    iou_th = float(cfg.get("iou_threshold", 0.5))
    has_label = bool(cfg.get("has_label"))
    write_labels = bool(cfg.get("output_labels"))
    detail_path = _open_detail(cfg) if has_label else None

    tp = fp = fn_ = 0
    gt_total = gt_missing = 0
    img_gt = img_ok = img_miss = img_fp = 0
    written = 0
    for i, (img_path, label_dir) in enumerate(pairs):
        page = None
        preds, texts = [], []
        try:
            with Image.open(img_path) as im:
                page = np.asarray(im.convert("RGB"))
                ih, iw = page.shape[:2]
            out = predictor([page]) or []
            words = out[0].get("words") if out else None
            if words is not None and len(words):
                arr = np.asarray(words, dtype=np.float32)
                for row in arr:
                    conf = float(row[4]) if arr.shape[1] >= 5 else 1.0
                    if conf < conf_th:
                        continue
                    preds.append(([float(row[0]) * iw, float(row[1]) * ih,
                                   float(row[2]) * iw, float(row[3]) * ih],
                                  conf))
            texts = _read_texts(rec, _quad_arrays(
                page, [b for b, _c in preds])) if preds else []
        except Exception as exc:
            print("[test] " + QC.translate(
                "OcrTestRunner", "预测失败 {}: {}").format(
                    os.path.basename(img_path), exc), flush=True)
        if has_label:
            # 必须先读真值再写标注: 标注与图像同目录时, 先写就把真值冲掉了,
            # 拿刚写出的预测框当真值比对会得到 P=R=1 的假象
            jp = ocr_data._find_json(img_path, [label_dir])
            if not jp:
                gt_missing += 1
            gts = _gt_boxes(jp) if jp else []
            gt_total += len(gts)
            t, f_p, f_n, missing, spurious, hits = _match(preds, gts, iou_th)
            tp += t
            fp += f_p
            fn_ += f_n
            if gts:
                img_gt += 1
                if t:
                    img_ok += 1
                else:
                    img_miss += 1
            if f_p:
                img_fp += 1
            if detail_path and (missing or spurious):
                _write_detail(detail_path, img_path, missing, spurious, hits)
        if write_labels and preds:
            try:
                _write_json(img_path, iw, ih, [b for b, _c in preds], texts)
                written += 1
            except OSError as exc:
                print("[test] " + QC.translate(
                    "OcrTestRunner", "输出标注失败 {}: {}").format(
                        os.path.basename(img_path), exc), flush=True)
        if (i + 1) % 10 == 0 or i + 1 == len(pairs):
            print("[test] PROGRESS {}/{}".format(i + 1, len(pairs)),
                  flush=True)

    result = {"ok": True, "task": occ.DET_TASK, "total": len(pairs),
              "model": os.path.basename(cfg.get("model_path", "") or ""),
              "conf": conf_th, "iou": iou_th,
              "datasets": _dataset_list(cfg)}
    if detail_path and os.path.exists(detail_path):
        result["detail_path"] = detail_path
        result["report_dir"] = os.path.dirname(detail_path)
    if has_label:
        p = tp / (tp + fp) if (tp + fp) else 0.0
        r = tp / (tp + fn_) if (tp + fn_) else 0.0
        result.update({"P": p, "R": r, "TP": tp, "FP": fp, "FN": fn_,
                       "per_class": {text_label(): {"gt": gt_total, "tp": tp,
                                                  "fp": fp, "fn": fn_,
                                                  "det": tp + fp}},
                       "gt_missing": gt_missing,
                       "img_gt": img_gt, "img_ok": img_ok,
                       "img_miss": img_miss, "img_fp": img_fp})
        print("[test] P={:.4f} R={:.4f} TP={} FP={} FN={}".format(
            p, r, tp, fp, fn_), flush=True)
    if write_labels:
        result["ocr_json"] = written
        print("[test] " + QC.translate(
            "OcrTestRunner", "已写出 {} 张图的文本标注(图像同目录)").format(
            written), flush=True)
    print("[test] RESULT " + json.dumps(result, ensure_ascii=False),
          flush=True)


def _run_rec(cfg, ckpt):
    arch = str(ckpt.get("architecture") or REC_ARCH)
    fn = getattr(recognition, arch, None)
    if fn is None:
        raise RuntimeError(QC.translate(
            "OcrTestRunner", "未知的字符识别架构: {}").format(arch))
    vocab = str(ckpt.get("vocab") or "")
    if not vocab:
        raise RuntimeError(QC.translate(
            "OcrTestRunner", "该模型没有词表, 无法识别"))
    model = fn(vocab=vocab, pretrained=False, pretrained_backbone=False)
    model.load_state_dict(ckpt["state_dict"])
    device = _device_of(cfg)
    predictor = _rec_predictor(ckpt, model, device)

    pairs = _collect_pairs(cfg)
    if not pairs:
        raise RuntimeError(QC.translate("OcrTestRunner", "没有可用的图像, 请检查数据集"))
    print("[test] " + QC.translate(
        "OcrTestRunner", "加载字符识别模型: {} 词表 {} 个字符").format(
        arch, len(vocab)), flush=True)
    print("[test] " + QC.translate(
        "OcrTestRunner", "测试图片 {} 张").format(len(pairs)), flush=True)
    refs, hyps = [], []
    no_label = 0
    for i, (img_path, label_dir) in enumerate(pairs):
        jp = ocr_data._find_json(img_path, [label_dir])
        if not jp:
            no_label += 1
            continue
        try:
            with Image.open(img_path) as im:
                page = np.asarray(im.convert("RGB"))
            ih, iw = page.shape[:2]
            boxes, texts = [], []
            for box, text in _crop_boxes(jp):
                box = [max(0.0, box[0]), max(0.0, box[1]),
                       min(float(iw), box[2]), min(float(ih), box[3])]
                if box[2] - box[0] < 2 or box[3] - box[1] < 2:
                    continue
                boxes.append(box)
                texts.append(text)
            if not boxes:
                continue
            crops = _quad_arrays(page, boxes)
            for text, hyp in zip(texts, _read_texts(predictor, crops)):
                refs.append(text)
                hyps.append(hyp)
        except Exception as exc:
            print("[test] " + QC.translate(
                "OcrTestRunner", "识别失败 {}: {}").format(
                    os.path.basename(img_path), exc), flush=True)
        if (i + 1) % 10 == 0 or i + 1 == len(pairs):
            print("[test] PROGRESS {}/{}".format(i + 1, len(pairs)),
                  flush=True)
    if not refs:
        raise RuntimeError(QC.translate(
            "OcrTestRunner",
            "没有取到任何字条: 该数据集没有文本标注, 识别段只能拿标注框裁图来测"))
    value = cer(refs, hyps)
    exact = sum(1 for a, b in zip(refs, hyps) if a == b)
    if no_label:
        print("[test] " + QC.translate(
            "OcrTestRunner", "WARN {} 张图没有文本标注, 已跳过").format(no_label),
            flush=True)
    print("[test] " + QC.translate(
        "OcrTestRunner", "字条 {} 条, CER={:.4f}, 全对 {} 条").format(
        len(refs), value, exact), flush=True)
    result = {"ok": True, "task": occ.RECO_TASK, "total": len(refs),
              "cer": value, "exact": exact, "no_label": no_label,
              "model": os.path.basename(cfg.get("model_path", "") or ""),
              "datasets": _dataset_list(cfg)}
    print("[test] RESULT " + json.dumps(result, ensure_ascii=False),
          flush=True)


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    i18n.apply_cli(cfg.get("language", ""))
    ckpt = torch.load(cfg["model_path"], map_location="cpu",
                      weights_only=False)
    task = str(cfg.get("task") or "")
    # cfg 里没带 task 时信 ckpt 自己记的那一个: 检测/识别是两条记录,
    # 走错分支会在识别模型上跑检测后处理
    if task not in (occ.DET_TASK, occ.RECO_TASK):
        task = str(ckpt.get("task") or occ.DET_TASK)
    if task == occ.RECO_TASK:
        _run_rec(cfg, ckpt)
    else:
        _run_det(cfg, ckpt)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
