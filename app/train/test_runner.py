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

from app.train.test_errors import pair_confusions

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    import torch
except ImportError:
    torch = None

try:
    from rfdetr import RFDETR   # from_checkpoint 自动推断检测/分割模型类
except ImportError:
    RFDETR = None

try:
    from app.core.label_utils import normalize_label as _normalize_label
except Exception:
    def _normalize_label(name):
        return str(name).strip()

_IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp")
_MAX_POLY_PTS = 60


def _list_images(img_dir):
    """返回图片文件绝对路径列表（按名称排序，稳定复现）。"""
    if not os.path.isdir(img_dir):
        return []
    names = [n for n in os.listdir(img_dir)
             if n.lower().endswith(_IMG_EXTS)]
    return [os.path.join(img_dir, n) for n in sorted(names)]


def _collect_pairs(cfg):
    """
    展开成 [(图片路径, 标签目录), ...]，支持一次测多个数据集。
    标签按文件名在"该图片所属数据集的"标签目录里找，不同数据集的同名图片
    不会串，所以必须逐目录配对而不是共用一个 label_dir。
    兼容旧 cfg：没有 items 时退回单条 image_path/label_path。
    """
    items = cfg.get("items") or [
        {"image_path": cfg.get("image_path", ""),
         "label_path": cfg.get("label_path", "")}]
    pairs = []
    for it in items:
        label_dir = it.get("label_path") or ""
        for img in _list_images(it.get("image_path") or ""):
            pairs.append((img, label_dir))
    return pairs


def _decimate(pts, max_pts):
    if len(pts) <= max_pts:
        return pts
    step = len(pts) / float(max_pts)
    return [pts[int(i * step)] for i in range(max_pts)]


def _mask_to_rings(mask, max_rings=6):
    """
    分割 mask → 轮廓环列表 [[[x,y],...], ...]（原图像素坐标），失败返回 None。
    一个实例被遮挡时 mask 会断成好几块，只留最大的那块画出来会比框小一大圈，
    看着像模型只分割出了一部分；所以按面积保留主要连通块，太小的碎片丢掉。
    """
    if cv2 is None or np is None or mask is None:
        return None
    try:
        m = np.asarray(mask)
        if m.ndim > 2:
            m = m.squeeze()
        if m.size == 0:
            return None
        m = (m > 0.5).astype(np.uint8) * 255 if m.dtype != np.uint8 else m
        found = cv2.findContours(m, cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
        contours = found[0] if len(found) == 2 else found[1]
        if not contours:
            return None
        cnts = sorted(contours, key=cv2.contourArea, reverse=True)
        top = cv2.contourArea(cnts[0])
        if top <= 0:
            return None
        kept = []
        for cnt in cnts[:max_rings]:
            # 面积不到最大的 3% 就是噪声碎片，画出来只会糊
            if cv2.contourArea(cnt) < top * 0.03:
                break
            peri = cv2.arcLength(cnt, True)
            if peri <= 0:
                continue
            approx = cv2.approxPolyDP(cnt, 0.002 * peri, True)
            if len(approx) < 3:
                continue
            kept.append([[float(p[0][0]), float(p[0][1])] for p in approx])
        if not kept:
            return None
        # 总点数按环数分摊，避免多连通目标把明细撑大好几倍
        budget = max(8, _MAX_POLY_PTS // len(kept))
        return [_decimate(ring, budget) for ring in kept]
    except Exception:
        return None


def _read_yolo_label(txt_path, img_w, img_h):
    """
    YOLO txt → [(cls, 像素[x1,y1,x2,y2], poly)] 列表。
    兼容两种格式：检测 `cls cx cy w h`（5 个数，中心点+宽高），poly 为 None；
    分割 `cls x1 y1 x2 y2 ...`（偶数个坐标且 >=6）→ 外接框 + 多边形顶点。
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
            poly = None
            if len(vals) == 4:
                # YOLO 检测：cx cy w h（归一化）
                cx, cy, w, h = vals
                x1 = (cx - w / 2) * img_w
                y1 = (cy - h / 2) * img_h
                x2 = (cx + w / 2) * img_w
                y2 = (cy + h / 2) * img_h
            elif len(vals) >= 6 and len(vals) % 2 == 0:
                # YOLO 分割：多边形顶点(归一化)
                xs = [vals[i] * img_w for i in range(0, len(vals), 2)]
                ys = [vals[i] * img_h for i in range(1, len(vals), 2)]
                x1, x2 = min(xs), max(xs)
                y1, y2 = min(ys), max(ys)
                poly = [_decimate([[round(x, 1), round(y, 1)]
                                   for x, y in zip(xs, ys)], _MAX_POLY_PTS)]
            else:
                continue
            boxes.append((p[0].strip(), [x1, y1, x2, y2], poly))
    return boxes


def _read_labelme_label(js_path):
    """
    labelme json → [(cls, box, poly)]，poly 是像素坐标顶点或 None。
    自己解析而不是复用 load_json_boxes：后者只给外接框，拿不到 polygon 顶点，
    而两次读文件再按序号对齐的做法在数据有脏 shape 时会错位。
    """
    out = []
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return out
    for shape in data.get("shapes") or []:
        pts = shape.get("points") or []
        if len(pts) < 2:
            continue
        try:
            xs = [float(p[0]) for p in pts]
            ys = [float(p[1]) for p in pts]
        except (TypeError, ValueError, IndexError):
            continue
        # labelme 的 rectangle 也存成 2 个点，>=3 个点的才是多边形
        poly = None
        if len(pts) >= 3:
            poly = [_decimate([[round(x, 1), round(y, 1)]
                               for x, y in zip(xs, ys)], _MAX_POLY_PTS)]
        out.append((_normalize_label(shape.get("label", "unknown")),
                    [min(xs), min(ys), max(xs), max(ys)], poly))
    return out


def _read_label_label(label_dir, img_path):
    """
    按图片同名找标签，优先 .txt (YOLO) 其次 .json (labelme)。
    返回 (gts, from_yolo)：gts 为 [(cls, 像素[x1,y1,x2,y2], poly)]，poly 是
    分割轮廓（环的列表，检测标注为 None），from_yolo 表示 cls 是类别 id 而不是名字。
    两种格式都覆盖，否则纯 labelme 的验证集会读到 0 个 GT，所有预测都被判成
    误检，看着像模型崩了其实是读不到标注。
    """
    base = os.path.splitext(os.path.basename(img_path))[0]
    with Image.open(img_path) as im:
        iw, ih = im.size
    txt = os.path.join(label_dir, base + ".txt")
    if os.path.exists(txt):
        return _read_yolo_label(txt, iw, ih), True
    js = os.path.join(label_dir, base + ".json")
    if os.path.exists(js):
        return _read_labelme_label(js), False
    return [], False


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


def _ring_area(ring):
    """算多边形面积（绝对值），用来在多连通 mask 里挑最大的那块。"""
    s = 0.0
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def _largest_ring(poly):
    if not poly:
        return None
    try:
        return max(poly, key=_ring_area)
    except (TypeError, ValueError, IndexError):
        return None


def _write_labelme_json(img_path, items):
    """
    写 labelme JSON 到图片同目录，同名 .json 覆盖。
    items: [([x1,y1,x2,y2], cls, poly)]，poly 非空时写 polygon，否则 rectangle。
    分割模型导成矩形会把 mask 轮廓丢掉，回到标注工具里只剩个框没法用。
    labelme 一个 shape 只能带一个多边形，多连通的 mask 取面积最大的那块。
    """
    with Image.open(img_path) as im:
        iw, ih = im.size
    shapes = []
    for b, cn, poly in items:
        ring = _largest_ring(poly)
        if ring and len(ring) >= 3:
            points = [[round(float(x), 2), round(float(y), 2)]
                      for x, y in ring]
            shape_type = "polygon"
        else:
            points = [[round(float(b[0]), 2), round(float(b[1]), 2)],
                      [round(float(b[2]), 2), round(float(b[3]), 2)]]
            shape_type = "rectangle"
        shapes.append({
            "label": cn or "object",
            "points": points,
            "group_id": None,
            "shape_type": shape_type,
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


def _open_detail(cfg):
    out_dir = cfg.get("report_dir") or ""
    if not out_dir:
        return None
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "details.jsonl")
        # 往同一目录重跑时先清空：写入是逐图追加的，留着旧数据明细会翻倍。
        # 删失败(例如被 hook 拦截到回收站)时降级 truncate，
        # truncate 也失败才放弃，否则 append 模式会把新旧数据拼在一起
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                try:
                    with open(path, "w", encoding="utf-8"):
                        pass
                except OSError as exc:
                    print("[test] 明细初始化失败: {}".format(exc), flush=True)
                    return None
        return path
    except OSError as exc:
        print("[test] 明细目录创建失败: {}".format(exc), flush=True)
        return None


def _detail_item(cls, box, poly, conf=None):
    d = {"cls": str(cls), "box": [round(v, 1) for v in box]}
    # 没有轮廓就不写这个字段
    if poly:
        d["poly"] = [[[round(float(x), 1), round(float(y), 1)]
                      for x, y in ring] for ring in poly]
    if conf is not None:
        d["conf"] = round(float(conf), 4)
    return d


def _write_detail(path, img_path, missing, spurious, hits):
    """只写有漏检或误检的图，正确检出的图不落盘。"""
    row = {
        "img": img_path,
        "missing": [_detail_item(c, b, p) for c, b, p in missing],
        "spurious": [_detail_item(c, b, p, cf) for c, b, cf, p in spurious],
        "hits": [_detail_item(c, b, p) for c, b, _, p in hits],
    }
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError as exc:
        print("[test] 明细写入失败: {}".format(exc), flush=True)


def _dataset_list(cfg):
    """cfg 里去重后的 [(项目, 数据集)]，报告首页要显示「测的是哪个数据集」。"""
    out, seen = [], set()
    for it in cfg.get("items") or []:
        key = (str(it.get("project") or ""), str(it.get("dataset") or ""))
        if key[1] and key not in seen:
            seen.add(key)
            out.append({"project": key[0], "dataset": key[1]})
    return out


def _decide_use_cls(gts_are_ids, preds_are_ids):
    """
    能不能按类别匹配：GT 与预测的类别体系必须一致。
    YOLO 标注只存类别 id（"0"/"1"），预测的 cls 来自 class_name（「溢锡」），
    对不上就没法比，只能退回不看类别。两侧都是名字时才比——这样模型把 A 类认成
    B 类才会被记成一次 FP + 一次 FN，而不是当正确检出藏起来。
    体系由来源直接给出，不去猜「类别名是不是数字」：类别名本身可能就是数字
    （产品型号之类），猜会把它们全误判成 id。也不敢用「两侧有没有交集」判，
    因为模型认错类别时交集同样为空，恰好放过最该抓出来的错误。
    """
    return not gts_are_ids and not preds_are_ids


def _match(preds, gts, iou_th, per_class, use_cls=None):
    """
    贪心匹配：每个 GT 只吃一个 IoU 最大的预测框，IoU≥阈值即算检出。
    """
    if use_cls is None:
        use_cls = False
    tp = fp = 0
    gt_matched = [False] * len(gts)
    hit_idx = []
    spurious = []
    for pi, (p_cls, p, p_conf, p_poly) in enumerate(preds):
        _tally(per_class, "det", p_cls)
        best_iou, best_gi = 0.0, -1
        for gi, (g_cls, g, _g_poly) in enumerate(gts):
            if gt_matched[gi]:
                continue
            if use_cls and g_cls != p_cls:
                continue
            iou = _iou(p, g)
            if iou > best_iou:
                best_iou, best_gi = iou, gi
        if best_iou >= iou_th and best_gi >= 0:
            tp += 1
            gt_matched[best_gi] = True
            hit_idx.append(pi)
            _tally(per_class, "tp", gts[best_gi][0])
        else:
            fp += 1
            _tally(per_class, "fp", p_cls)
            spurious.append((p_cls, p, p_conf, p_poly))
    fn = 0
    missing = []
    for gi, g_item in enumerate(gts):
        _tally(per_class, "gt", g_item[0])
        if not gt_matched[gi]:
            fn += 1
            _tally(per_class, "fn", g_item[0])
            missing.append(g_item)
    hits = [preds[i] for i in hit_idx]
    return tp, fp, fn, missing, spurious, hits


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

    pairs = _collect_pairs(cfg)
    print("[test] 测试图片 {} 张".format(len(pairs)), flush=True)
    conf_th = float(cfg.get("confidence", 0.5))
    iou_th = float(cfg.get("iou_threshold", 0.5))
    has_label = bool(cfg.get("has_label"))

    tp = fp = fn = 0
    _miss = 0                 # 有标签目录却找不到 .txt/.json 的图片数
    conf_total = conf_imgs = 0   # 位置对但类别判错: 总处数 / 涉及图片数
    # 图像维度: 有标注图 / 检出图 / 未检出图 / 有误检图
    img_gt = img_ok = img_miss = img_fp = 0
    per_class = {}           # {cls: {gt,tp,fp,fn,det}}
    use_cls = None
    output_labels = bool(cfg.get("output_labels"))
    detail_path = _open_detail(cfg) if has_label else None
    for i, (img_path, label_dir) in enumerate(pairs):
        try:
            det = model.predict(img_path, threshold=conf_th)
            if isinstance(det, list):
                det = det[0]
            xyxy = getattr(det, "xyxy", None)
            confs = getattr(det, "confidence", None)
            masks = getattr(det, "mask", None)   # 分割模型才有
            preds = []          # [(cls, box, conf, poly)]
            class_names = []    # 与 preds 对应的类别名
            preds_are_ids = False
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
                        preds_are_ids = True
                    else:
                        cn = "object"
                    cf = (float(confs[k]) if confs is not None
                          and k < len(confs) else 1.0)
                    poly = _mask_to_rings(masks[k]) if masks is not None \
                        and k < len(masks) else None
                    class_names.append(cn)
                    preds.append((cn, box, cf, poly))
        except Exception as exc:
            print("[test] 预测失败 {}: {}".format(
                os.path.basename(img_path), exc), flush=True)
            traceback.print_exc()
            preds = []
            class_names = []
            preds_are_ids = False
        if output_labels and preds:
            try:
                _write_labelme_json(
                    img_path,
                    [(b, class_names[i] if i < len(class_names) else "", p)
                     for i, (_, b, _, p) in enumerate(preds)])
            except Exception as exc:
                print("[test] 输出标注失败 {}: {}".format(
                    os.path.basename(img_path), exc), flush=True)
        if has_label:
            with Image.open(img_path) as im:
                iw, ih = im.size
            gts, gts_are_ids = _read_label_label(label_dir, img_path)
            if not gts:
                _miss += 1
            if use_cls is None and gts and preds:
                use_cls = _decide_use_cls(gts_are_ids, preds_are_ids)
            t, f_p, f_n, missing, spurious, hits = _match(
                preds, gts, iou_th, per_class, use_cls)
            tp += t
            fp += f_p
            fn += f_n
            # 图级口径: 一张图只要检出 1 个就算「已检出」，不要求把标注全检出
            if gts:
                img_gt += 1
                if t:
                    img_ok += 1
                else:
                    img_miss += 1
            if f_p:
                img_fp += 1
            if missing and spurious:
                n_conf = len(pair_confusions(
                    [_detail_item(c, b, p) for c, b, p in missing],
                    [_detail_item(c, b, p, cf) for c, b, cf, p in spurious],
                    iou_th)[0])
                if n_conf:
                    conf_total += n_conf
                    conf_imgs += 1
            if detail_path and (missing or spurious):
                _write_detail(detail_path, img_path, missing, spurious, hits)
        if (i + 1) % 10 == 0 or i + 1 == len(pairs):
            print("[test] 进度 {}/{}".format(i + 1, len(pairs)), flush=True)

    result = {"ok": True, "total": len(pairs),
              "model": os.path.basename(cfg.get("model_path", "") or ""),
              "conf": conf_th, "iou": iou_th,
              "datasets": _dataset_list(cfg)}
    if detail_path and os.path.exists(detail_path):
        result["detail_path"] = detail_path
        result["report_dir"] = os.path.dirname(detail_path)
    if has_label:
        p = tp / (tp + fp) if (tp + fp) else 0.0
        r = tp / (tp + fn) if (tp + fn) else 0.0
        result.update({"P": p, "R": r, "TP": tp, "FP": fp, "FN": fn,
                       "per_class": per_class, "gt_missing": _miss,
                       "conf_total": conf_total, "conf_imgs": conf_imgs,
                       "img_gt": img_gt,
                       "img_ok": img_ok, "img_miss": img_miss,
                       "img_fp": img_fp})
        if _miss and _miss == len(pairs):
            print("[test] WARN 标签目录存在但所有 {} 张图都没读到 GT,"
                  "请确认标签是 .txt (YOLO) 或 .json (labelme)".format(
                      len(pairs)), flush=True)
        elif _miss:
            print("[test] WARN {} 张图缺标签文件".format(_miss),
                  flush=True)
        print("[test] P={:.4f} R={:.4f} TP={} FP={} FN={}".format(
            p, r, tp, fp, fn), flush=True)
    print("[test] RESULT " + json.dumps(result, ensure_ascii=False),
          flush=True)


if __name__ == "__main__":
    main()
