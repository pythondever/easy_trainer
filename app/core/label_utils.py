# -*- coding: utf-8 -*-
import json
import os


def normalize_label(name):
    s = str(name).strip()
    if s.startswith("class_") and s[6:].isdigit():
        return s[6:]
    return s


def label_sort_key(name):
    s = str(name)
    try:
        return (0, int(s))
    except ValueError:
        return (1, s)


def load_json_shapes(json_path):
    """读 labelme json → [(label, points)]，points = [[x, y], ...] 像素坐标。

    保留多边形顶点而不是只取外接框：分割训练要拿顶点写 yolo-seg，
    压成框之后 mask 就没了。
    """
    shapes = []
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for shape in data.get("shapes", []):
            pts = shape.get("points") or []
            if len(pts) < 2:
                continue
            shapes.append((normalize_label(shape.get("label", "unknown")),
                           [[float(p[0]), float(p[1])] for p in pts]))
    except Exception:
        return []
    return shapes


def looks_like_labelme(json_path):
    """是否 labelme 标注文件（含 shapes 列表）。

    图像目录里可能有别的 json(导出清单、类别表等), 它们不是标注,
    不能被当成"这张图没有目标"把有效标签清空。
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False
    return isinstance(data, dict) and isinstance(data.get("shapes"), list)


def load_yolo_shapes(txt_path, iw, ih, label_ids=None):
    """读 yolo txt → [(label, points)] 像素坐标，支持 bbox(5 字段) 与 yolo-seg 多边形。

    label_ids: {数字 id 字符串: 显示名}，把 txt 里的数字 id 换成标注界面显示的名字，
    否则同一类在导入标签里叫 "0"、在标注 json 里叫 "cat"，会被当成两类。
    """
    shapes = []
    if not iw or not ih:
        return shapes
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) < 5:
                    continue
                try:
                    vals = [float(x) for x in parts[1:]]
                except ValueError:
                    continue
                raw = parts[0].strip()
                label = normalize_label(
                    label_ids.get(raw, raw) if label_ids and raw in label_ids else raw)
                if len(vals) == 4:
                    cx, cy, w, h = vals
                    x1, y1 = (cx - w / 2) * iw, (cy - h / 2) * ih
                    x2, y2 = (cx + w / 2) * iw, (cy + h / 2) * ih
                    pts = [[x1, y1], [x2, y2]]
                elif len(vals) % 2 == 0:
                    pts = [[vals[i] * iw, vals[i + 1] * ih]
                           for i in range(0, len(vals), 2)]
                else:
                    continue
                shapes.append((label, pts))
    except Exception:
        return []
    return shapes


def _rect_corners(pts):
    """两点对角 → 四角顶点。yolo-seg 至少要 3 个点，两点会被当成 bbox 解析。"""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)
    return [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]


def shapes_to_yolo_text(shapes, iw, ih, label_to_id, as_polygon=False):
    """[(label, points)] 像素坐标 → yolo txt 内容。

    as_polygon: True 全部写 yolo-seg 顶点序列（RF-DETR 会栅格化成 mask）；
    False 全部写 cx cy w h；"auto" 按 shape 自身形态来——多边形写顶点、
    矩形写 bbox，导出的标签因此能同时喂检测和分割。
    顶点少于 3 个时补成矩形四角（yolo-seg 至少要 3 个点）。
    """
    lines = []
    for label, pts in shapes:
        cls_id = label_to_id.get(label, 0)
        if as_polygon == "auto":
            as_polygon_each = len(pts) >= 3
        else:
            as_polygon_each = as_polygon
        if as_polygon_each:
            poly = pts if len(pts) >= 3 else _rect_corners(pts)
            coords = " ".join("{:.6f} {:.6f}".format(
                min(max(x / iw, 0.0), 1.0), min(max(y / ih, 0.0), 1.0))
                for x, y in poly)
            lines.append("{} {}".format(cls_id, coords))
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)
        w, h = x2 - x1, y2 - y1
        lines.append("{} {:.6f} {:.6f} {:.6f} {:.6f}".format(
            cls_id, (x1 + w / 2) / iw, (y1 + h / 2) / ih, w / iw, h / ih))
    return "\n".join(lines) + ("\n" if lines else "")


def shapes_to_labelme_json(shapes, img_path, iw, ih):
    """[(label, points)] → labelme json dict，多边形保留 polygon 形态。"""
    out = []
    for label, pts in shapes:
        out.append({
            "label": label,
            "points": [[round(float(x), 2), round(float(y), 2)] for x, y in pts],
            "group_id": None,
            "shape_type": "polygon" if len(pts) >= 3 else "rectangle",
            "flags": {},
        })
    return {"version": "5.0.1", "flags": {}, "shapes": out,
            "imagePath": os.path.basename(img_path),
            "imageWidth": iw, "imageHeight": ih}
