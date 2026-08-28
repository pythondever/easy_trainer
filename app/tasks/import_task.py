# -*- coding: utf-8 -*-
"""后台导入线程：扫描图像目录，可选读取标签(yolo txt / labelme json)。"""
import os
import json

from PySide6.QtCore import QThread, Signal

from app.core.image_utils import pil_open
from app.core.label_utils import normalize_label


class ImportTask(QThread):
    """
    后台导入线程: 扫描图像目录,可选读取标签(yolo txt / labelme json),
    生成整图缩略图(默认大图模式);ROI 裁剪小图在筛选时懒生成。
    结果以 list 通过 finished_signal 返回:
    [{"image_path", "label_path", "boxes": [(x,y,w,h,label)]或None, "labels": [...],
      "thumb": QImage或None, "rois": {label: [QImage]}}]
    """
    progress_updated = Signal(int)
    finished_signal = Signal(list)

    IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

    def __init__(self, image_path, label_path="", fmt="", parent=None,
                 excluded=None, label_ids=None):
        super().__init__(parent)
        self.image_paths = [image_path] if isinstance(image_path, (str,)) else list(image_path or [])
        self.label_paths = [label_path] if isinstance(label_path, (str,)) else list(label_path or [])
        self.image_paths = [p for p in self.image_paths if p]
        self.label_paths = [p for p in self.label_paths if p]
        self.fmt = fmt  # '' 无标签 / '.txt' / '.json'
        self.excluded = set(excluded or [])
        self._cancel = False
        self._id_names = dict(label_ids or {})
        self._seen_ids = {}

    @staticmethod
    def _norm(path):
        return os.path.normcase(os.path.normpath(path))

    def run(self):
        cls_mode = self.fmt == "cls"   # 按子文件夹分类导入: 子文件夹名=类别
        images = []
        for base_dir in self.image_paths:
            if self._cancel:
                break
            if not base_dir or not os.path.isdir(base_dir):
                continue
            for root, _, files in os.walk(base_dir):
                if self._cancel:
                    break
                for fn in sorted(files):
                    if fn.lower().endswith(self.IMAGE_EXTS):
                        p = os.path.join(root, fn)
                        if self._norm(p) in self.excluded:
                            continue
                        if cls_mode:
                            # 类别 = 根目录下第一级子文件夹名; 图像直接在根目录则用根目录名
                            rel = os.path.relpath(root, base_dir)
                            cls = (rel.split(os.sep)[0]
                                   if rel and rel != "."
                                   else os.path.basename(base_dir))
                            images.append((p, cls))
                        else:
                            images.append((p, None))
        total = len(images)
        result = []
        last_pct = -1
        for i, (img_path, cls) in enumerate(images):
            if self._cancel:
                break
            try:
                if cls_mode:
                    result.append({
                        "image_path": img_path,
                        "label_path": "",
                        "cls": cls,
                        "labels": [cls] if cls else [],
                        "boxes": None,
                        "thumb": None,
                        "rois": {},
                    })
                else:
                    # 标注解析失败(损坏/空 json 等)不能丢弃整张图:
                    # 保留 rec(boxes=None → 归为未标注), 保证 total 计数正确
                    try:
                        boxes, labels = self._read_boxes(img_path)
                    except Exception:
                        boxes, labels = None, []
                    thumb = None
                    result.append({
                        "image_path": img_path,
                        "label_path": self._label_of(img_path),
                        "boxes": boxes if boxes else None,   # [(x, y, w, h, label)] 或 None
                        "labels": labels,
                        "thumb": thumb,
                        "rois": {},
                    })
            except Exception:
                pass
            if total > 0:
                pct = int((i + 1) / total * 100)
                if pct != last_pct:
                    last_pct = pct
                    self.progress_updated.emit(pct)
        self.finished_signal.emit(result)

    def _label_of(self, img_path):
        """在多个标签目录中找同名的标签文件(txt/json)，返回存在的第一个; 无则空。"""
        if not self.label_paths or not self.fmt:
            return ""
        base = os.path.splitext(os.path.basename(img_path))[0]
        ext = ".txt" if self.fmt == ".txt" else ".json"
        for lp in self.label_paths:
            if not lp or not os.path.isdir(lp):
                continue
            candidate = os.path.join(lp, base + ext)
            if os.path.exists(candidate):
                return candidate
        return ""

    def _read_boxes(self, img_path):
        """
        读取标签，返回 (boxes, labels):
        boxes = 像素坐标 [(x, y, w, h, label)]; labels = 对应类别列表
        无标签返回(None, [])。
        优先读图像同路径 labelme json，与标注界面 _load_current
        一致；没有才回退 label_paths 的导入标签(txt/json)。否则重启后首页
        缩略图会显示标注界面修改前的旧标签。
        """
        same_path_json = os.path.splitext(img_path)[0] + ".json"
        if os.path.exists(same_path_json):
            label_file = same_path_json
            fmt = ".json"
        elif self.label_paths and self.fmt:
            label_file = self._label_of(img_path)
            fmt = self.fmt
        else:
            return None, []
        if not os.path.exists(label_file):
            return None, []
        try:
            with pil_open(img_path) as im:
                iw, ih = im.size
        except Exception:
            return None, []
        boxes = []
        labels = []
        if fmt == ".txt":
            with open(label_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) < 5:
                        continue
                    try:
                        vals = [float(x) for x in parts[1:]]
                    except ValueError:
                        continue
                    if len(vals) == 4:
                        cx, cy, w, h = vals
                        x = int((cx - w / 2) * iw)
                        y = int((cy - h / 2) * ih)
                        bw = int(w * iw)
                        bh = int(h * ih)
                    else:
                        xs = vals[0::2]
                        ys = vals[1::2]
                        if not xs or not ys:
                            continue
                        x = int(min(xs) * iw)
                        y = int(min(ys) * ih)
                        bw = int((max(xs) - min(xs)) * iw)
                        bh = int((max(ys) - min(ys)) * ih)
                    lbl = normalize_label(parts[0].strip())
                    # 映射数字 id
                    if parts[0].strip() in self._id_names:
                        lbl = normalize_label(self._id_names[parts[0].strip()])
                    self._seen_ids[parts[0].strip()] = lbl
                    boxes.append((max(0, x), max(0, y), max(1, bw), max(1, bh), lbl))
                    labels.append(lbl)
        else:
            with open(label_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for shape in data.get("shapes", []):
                pts = shape.get("points", [])
                if len(pts) < 2:
                    continue
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                x, y = int(min(xs)), int(min(ys))
                w, h = int(max(xs) - min(xs)), int(max(ys) - min(ys))
                lbl = normalize_label(shape.get("label", "unknown"))
                boxes.append((max(0, x), max(0, y), max(1, w), max(1, h), lbl))
                labels.append(lbl)
        return boxes, labels
