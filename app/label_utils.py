# -*- coding: utf-8 -*-
import json


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


def load_json_boxes(json_path):
    """读 labelme json → boxes [(x, y, w, h, label)]（像素坐标，标签归一化）。"""
    boxes = []
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for shape in data.get("shapes", []):
            pts = shape.get("points", [])
            if len(pts) < 2:
                continue
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            label = normalize_label(shape.get("label", "unknown"))
            boxes.append((int(min(xs)), int(min(ys)),
                          int(max(xs) - min(xs)), int(max(ys) - min(ys)), label))
    except Exception:
        return []
    return boxes


def boxes_to_yolo_text(boxes, iw, ih, label_to_id):
    """boxes（像素 + label）→ yolo txt 内容（类别ID + 归一化坐标）。"""
    lines = []
    for x, y, w, h, label in boxes:
        cls_id = label_to_id.get(label, 0)
        lines.append("{} {:.6f} {:.6f} {:.6f} {:.6f}".format(
            cls_id, (x + w / 2) / iw, (y + h / 2) / ih, w / iw, h / ih))
    return "\n".join(lines)
