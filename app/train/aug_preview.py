# -*- coding: utf-8 -*-
"""
数据增强预览的渲染核心: 取一张训练集里的图, 按勾选参数当场做一遍增强.

一致性靠 aug_params 那份参数表(训练端同一个来源), 渲染本身用 cv2 重写一遍:
GUI 进程不能为了看一眼预览去 import ultralytics / rfdetr / albumentations.
代数上与原库会有微小差异(插值核、随机分布), 预览只求"看得出这一项在做什么".
"""

import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from app.core.constants import IMAGE_EXTS
from app.core.db import get_path_pairs
from app.core.label_utils import (load_json_shapes, load_yolo_shapes,
                                  same_dir_json)

# 图像外的补边色, 与 ultralytics 的 letterbox 默认值一致
PAD = (114, 114, 114)
PAD_VAL = 114

_PALETTE = ((255, 107, 107), (90, 122, 224), (123, 227, 154), (255, 209, 102),
            (51, 194, 218), (214, 83, 126), (255, 159, 107), (147, 174, 240))

_FONT_FILES = (
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
)


def _font(size):
    for path in _FONT_FILES:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                break
    return ImageFont.load_default()


def read_image(path):
    """cv2.imread 在中文路径下静默返回 None, 走 fromfile 一条路."""
    try:
        buf = np.fromfile(path, dtype=np.uint8)
        return cv2.imdecode(buf, cv2.IMREAD_COLOR)
    except Exception:
        return None


def dataset_images(info):
    """
    数据集里可用的 (图像路径, 标签目录, 标签格式, 类别映射).
    配对口径与 data_prep 一致: 只认图像目录还活着的那些轮次.
    """
    fmt = str(info.get("label_fmt", "") or "").lstrip(".")
    if not fmt or fmt == "cls":
        return []
    label_ids = info.get("label_ids") or {}
    out = []
    for img_dir, label_dir in get_path_pairs(info):
        if not img_dir or not os.path.isdir(img_dir):
            continue
        try:
            names = os.listdir(img_dir)
        except OSError:
            continue
        for fn in names:
            if fn.lower().endswith(IMAGE_EXTS):
                out.append((os.path.join(img_dir, fn), label_dir, fmt, label_ids))
    out.sort()
    return out


def load_shapes(img_path, width, height, label_dir, fmt, label_ids):
    """标注来源与 data_prep 一致: 图旁边的 json(标注产物)优先, 其次导入的标签目录."""
    same = same_dir_json(img_path)
    if same:
        return load_json_shapes(same)
    if not label_dir or not os.path.isdir(label_dir):
        return []
    stem = os.path.splitext(os.path.basename(img_path))[0]
    if fmt == "txt":
        path = os.path.join(label_dir, stem + ".txt")
        return (load_yolo_shapes(path, width, height, label_ids)
                if os.path.isfile(path) else [])
    path = os.path.join(label_dir, stem + ".json")
    return load_json_shapes(path) if os.path.isfile(path) else []


def load_sample(entry):
    """读一张图及其标注. 图读不出来返回 None."""
    img_path, label_dir, fmt, label_ids = entry
    img = read_image(img_path)
    if img is None:
        return None
    h, w = img.shape[:2]
    return {"image": img, "shapes": load_shapes(img_path, w, h, label_dir,
                                                fmt, label_ids),
            "name": os.path.basename(img_path), "path": img_path}


def has_label(entry):
    """这张图有没有标注. 没标注的图上增强看不出几何项的效果, 抽图时排到后面."""
    img_path, label_dir, fmt, _ids = entry
    if same_dir_json(img_path):
        return True
    if not label_dir:
        return False
    stem = os.path.splitext(os.path.basename(img_path))[0]
    ext = ".txt" if fmt == "txt" else ".json"
    return os.path.isfile(os.path.join(label_dir, stem + ext))


def _map_shapes(shapes, matrix):
    """按 3x3 矩阵变换顶点. 框跟着图走靠的就是这一步."""
    out = []
    for label, pts, text in shapes:
        arr = np.asarray(pts, np.float64).reshape(-1, 2)
        if not len(arr):
            continue
        homo = np.hstack([arr, np.ones((len(arr), 1))])
        moved = (matrix @ homo.T).T[:, :2]
        out.append((label, [[float(x), float(y)] for x, y in moved], text))
    return out


def letterbox(img, shapes, size):
    """等比缩放 + 居中补边到 size 见方, 标注同步换算."""
    h, w = img.shape[:2]
    r = min(size / float(w or 1), size / float(h or 1))
    nw, nh = max(1, int(round(w * r))), max(1, int(round(h * r)))
    interp = cv2.INTER_AREA if r < 1 else cv2.INTER_LINEAR
    canvas = np.full((size, size, 3), PAD_VAL, np.uint8)
    dx, dy = (size - nw) // 2, (size - nh) // 2
    canvas[dy:dy + nh, dx:dx + nw] = cv2.resize(img, (nw, nh),
                                                interpolation=interp)
    matrix = np.array([[r, 0, dx], [0, r, dy], [0, 0, 1]], np.float64)
    return canvas, _map_shapes(shapes, matrix)


def _geom_matrix(width, height, angle, scale, shear, tx, ty):
    """绕图心的旋转/缩放/剪切/平移合成一个矩阵(3x3)."""
    cx, cy = width / 2.0, height / 2.0
    cos, sin = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    rot = np.array([[cos, sin], [-sin, cos]], np.float64) * scale
    sh = np.array([[1.0, math.tan(math.radians(shear))], [0.0, 1.0]])
    a = rot @ sh
    center = np.array([cx, cy])
    move = center - a @ center + np.array([tx, ty])
    m = np.eye(3)
    m[:2, :2] = a
    m[:2, 2] = move
    return m


def _flip_matrix(width, height, horizontal):
    m = np.eye(3)
    if horizontal:
        m[0, 0], m[0, 2] = -1.0, width - 1.0
    else:
        m[1, 1], m[1, 2] = -1.0, height - 1.0
    return m


def _warp(img, matrix):
    h, w = img.shape[:2]
    return cv2.warpAffine(img, matrix[:2], (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT,
                          borderValue=PAD)


def _ops(params, backend):
    """两套后端的参数字典折成同一组操作与强度."""
    p = params or {}
    ops = {"mosaic": 0.0, "hflip": 0.0, "vflip": 0.0, "rotate": None,
           "affine": None, "hsv": None, "bri": None, "blur": None,
           "noise": None}
    if backend == "cnn":
        if p.get("fliplr"):
            ops["hflip"] = float(p["fliplr"])
        if p.get("flipud"):
            ops["vflip"] = float(p["flipud"])
        if p.get("degrees"):
            ops["rotate"] = (float(p["degrees"]), 1.0)
        if p.get("scale") or p.get("translate") or p.get("shear"):
            sc = float(p.get("scale") or 0.0)
            ops["affine"] = (1.0 - sc, 1.0 + sc, float(p.get("translate") or 0.0),
                             float(p.get("shear") or 0.0), 1.0)
        if p.get("hsv_h") or p.get("hsv_s") or p.get("hsv_v"):
            ops["hsv"] = (float(p.get("hsv_h") or 0.0),
                          float(p.get("hsv_s") or 0.0),
                          float(p.get("hsv_v") or 0.0), 1.0)
        if p.get("mosaic"):
            ops["mosaic"] = float(p["mosaic"])
        return ops

    def frag(name):
        return p.get(name) or {}

    fl = frag("HorizontalFlip")
    if fl:
        ops["hflip"] = float(fl.get("p", 1.0))
    fl = frag("VerticalFlip")
    if fl:
        ops["vflip"] = float(fl.get("p", 1.0))
    rot = frag("Rotate")
    if rot:
        ops["rotate"] = (float(rot.get("limit", 0.0)), float(rot.get("p", 1.0)))
    aff = frag("Affine")
    if aff:
        lo, hi = aff.get("scale", (1.0, 1.0))
        trans = aff.get("translate_percent", (0.0, 0.0))
        shear = aff.get("shear", (0.0, 0.0))
        ops["affine"] = (float(lo), float(hi),
                         max(abs(float(trans[0])), abs(float(trans[1]))),
                         max(abs(float(shear[0])), abs(float(shear[1]))),
                         float(aff.get("p", 1.0)))
        # Affine 自带一段旋转, 与 Rotate 是两次独立抽样, 这里折进 rotate 的幅度
        extra = aff.get("rotate", (0.0, 0.0))
        if ops["rotate"] is None and any(extra):
            ops["rotate"] = (max(abs(float(extra[0])), abs(float(extra[1]))),
                             float(aff.get("p", 1.0)))
    bri = frag("RandomBrightnessContrast")
    if bri:
        ops["bri"] = (float(bri.get("brightness_limit", 0.0)),
                      float(bri.get("contrast_limit", 0.0)),
                      float(bri.get("p", 1.0)))
    jit = frag("ColorJitter")
    if jit:
        ops["hsv"] = (float(jit.get("hue", 0.0)), float(jit.get("saturation", 0.0)),
                      float(jit.get("brightness", 0.0)), float(jit.get("p", 1.0)))
    blur = frag("GaussianBlur")
    if blur:
        ops["blur"] = (int(blur.get("blur_limit", 3)) | 1, float(blur.get("p", 1.0)))
    noise = frag("GaussNoise")
    if noise:
        lo, hi = noise.get("std_range", (0.0, 0.0))
        ops["noise"] = (float(lo), float(hi), float(noise.get("p", 1.0)))
    return ops


def _apply_color(img, ops, rng):
    out = img.astype(np.float32)
    if ops["bri"] is not None:
        b_lim, c_lim, p = ops["bri"]
        if rng.random() < p:
            alpha = 1.0 + rng.uniform(-c_lim, c_lim)
            beta = rng.uniform(-b_lim, b_lim) * 255.0
            out = out * alpha + beta
    if ops["hsv"] is not None:
        dh, ds, dv, p = ops["hsv"]
        if rng.random() < p:
            hsv = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8),
                               cv2.COLOR_BGR2HSV).astype(np.float32)
            if dh:
                hsv[..., 0] = (hsv[..., 0] + rng.uniform(-dh, dh) * 180.0) % 180.0
            if ds:
                hsv[..., 1] = hsv[..., 1] * (1.0 + rng.uniform(-ds, ds))
            if dv:
                hsv[..., 2] = hsv[..., 2] * (1.0 + rng.uniform(-dv, dv))
            hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
            hsv[..., 2] = np.clip(hsv[..., 2], 0, 255)
            out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    return np.clip(out, 0, 255).astype(np.uint8)


def _apply_pixel(img, ops, rng):
    out = _apply_color(img, ops, rng)
    if ops["blur"] is not None:
        k, p = ops["blur"]
        if rng.random() < p:
            out = cv2.GaussianBlur(out, (max(1, k), max(1, k)), 0)
    if ops["noise"] is not None:
        lo, hi, p = ops["noise"]
        if rng.random() < p:
            sigma = rng.uniform(lo, hi) * 255.0
            grain = np.random.normal(0.0, sigma, out.shape)
            out = np.clip(out.astype(np.float32) + grain, 0, 255).astype(np.uint8)
    return out


def _fill_cell(img, shapes, size):
    """缩放到覆盖整格再居中裁切: 四格都填满, 才看得出这是拼接出来的训练样本."""
    h, w = img.shape[:2]
    r = max(size / float(w or 1), size / float(h or 1))
    nw, nh = max(size, int(round(w * r))), max(size, int(round(h * r)))
    interp = cv2.INTER_AREA if r < 1 else cv2.INTER_LINEAR
    resized = cv2.resize(img, (nw, nh), interpolation=interp)
    x0, y0 = (nw - size) // 2, (nh - size) // 2
    matrix = np.array([[r, 0, -x0], [0, r, -y0], [0, 0, 1]], np.float64)
    return resized[y0:y0 + size, x0:x0 + size], _map_shapes(shapes, matrix)


def _compose_mosaic(items, size):
    """
    四图 2x2 拼接, 各格标注跟着自己那格换算.
    items 要原始图(不是 letterbox 过的), 否则每格会把自己那份补边再裁一遍, 拼出来中间横一条灰.
    """
    half = size // 2
    canvas = np.full((size, size, 3), PAD_VAL, np.uint8)
    merged = []
    slots = ((0, 0), (half, 0), (0, half), (half, half))
    pool = list(items)
    while len(pool) < 4:
        pool.append(pool[0])
    for (ox, oy), (im, sh) in zip(slots, pool[:4]):
        cell, moved = _fill_cell(im, sh, half)
        canvas[oy:oy + half, ox:ox + half] = cell
        merged += [(lb, [[x + ox, y + oy] for x, y in pts], tx)
                   for lb, pts, tx in moved]
    return canvas, merged


def augment(img, shapes, params, backend, rng, others=None, source=None):
    """
    按参数做一遍增强. others/source 是未 letterbox 的原图: 勾了马赛克就用它们拼图,
    其余项叠在拼好的图上. 返回 (图像, 标注), 标注与图像同一坐标系.
    """
    ops = _ops(params, backend)
    height, width = img.shape[:2]
    out, boxes = img, shapes
    if others and ops["mosaic"] and rng.random() < ops["mosaic"]:
        first = source if source is not None else (img, shapes)
        out, boxes = _compose_mosaic([first] + list(others), height)
        height, width = out.shape[:2]

    matrix = np.eye(3)
    if ops["hflip"] and rng.random() < ops["hflip"]:
        matrix = _flip_matrix(width, height, True) @ matrix
    if ops["vflip"] and rng.random() < ops["vflip"]:
        matrix = _flip_matrix(width, height, False) @ matrix
    angle = shear = tx = ty = 0.0
    scale = 1.0
    if ops["rotate"] is not None:
        limit, p = ops["rotate"]
        if rng.random() < p:
            angle = rng.uniform(-limit, limit)
    if ops["affine"] is not None:
        lo, hi, trans, shearmax, p = ops["affine"]
        if rng.random() < p:
            scale = rng.uniform(lo, hi)
            shear = rng.uniform(-shearmax, shearmax) if shearmax else 0.0
            tx = rng.uniform(-trans, trans) * width
            ty = rng.uniform(-trans, trans) * height
    if angle or scale != 1.0 or shear or tx or ty:
        matrix = _geom_matrix(width, height, angle, scale, shear, tx, ty) @ matrix
    if not np.allclose(matrix, np.eye(3)):
        out = _warp(out, matrix)
        boxes = _map_shapes(boxes, matrix)

    out = _apply_pixel(out, ops, rng)
    return out, boxes


def draw(img, shapes, task, show_labels=True):
    """把标注画上去: 分割画多边形填充+轮廓, 检测(或三点以下)画外接框."""
    out = img.copy()
    texts = []
    for label, pts, _text in shapes:
        arr = np.asarray(pts, np.float32).reshape(-1, 2)
        if not len(arr):
            continue
        color = label_color(label)
        if task == "segment" and len(arr) >= 3:
            poly = arr.astype(np.int32)
            overlay = out.copy()
            cv2.fillPoly(overlay, [poly], color)
            cv2.addWeighted(overlay, 0.30, out, 0.70, 0, out)
            cv2.polylines(out, [poly], True, color, 2, cv2.LINE_AA)
            x, y = int(arr[:, 0].min()), int(arr[:, 1].min())
        else:
            x, y = int(arr[:, 0].min()), int(arr[:, 1].min())
            x2, y2 = int(arr[:, 0].max()), int(arr[:, 1].max())
            cv2.rectangle(out, (x, y), (x2, y2), color, 2, cv2.LINE_AA)
        if show_labels:
            texts.append((str(label), x, y, color))
    if texts:
        out = _draw_texts(out, texts)
    return out


def _draw_texts(img, texts):
    """标签文字走 PIL: cv2.putText 画不了中文."""
    h, w = img.shape[:2]
    size = max(11, int(round(min(h, w) / 26.0)))
    font = _font(size)
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil)
    for text, x, y, color in texts:
        try:
            box = draw.textbbox((0, 0), text, font=font)
            tw, th = box[2] - box[0], box[3] - box[1]
        except Exception:
            tw, th = 6 * len(text), size
        top = max(0, y - th - 6)
        draw.rectangle([x, top, x + tw + 6, top + th + 6],
                       fill=(color[2], color[1], color[0]))
        draw.text((x + 3, top + 1), text,
                  fill=(20, 20, 20) if _bright(color) else (245, 245, 245),
                  font=font)
    return cv2.cvtColor(np.asarray(pil), cv2.COLOR_RGB2BGR)


def _bright(color):
    r, g, b = color
    return (0.299 * r + 0.587 * g + 0.114 * b) > 150


def label_color(label):
    return _PALETTE[sum(ord(c) for c in str(label)) % len(_PALETTE)]


def _num(value):
    text = ("%.2f" % float(value)).rstrip("0").rstrip(".")
    return text or "0"


def param_rows(params, backend):
    """参数栏的展示行 [(界面名, 下发值)], 只列真正生效的项."""
    rows = []
    p = params or {}
    if backend == "cnn":
        for key, name in (("fliplr", "水平翻转"), ("flipud", "垂直翻转"),
                          ("degrees", "旋转"), ("scale", "缩放"),
                          ("translate", "平移"), ("shear", "剪切"),
                          ("mosaic", "马赛克"), ("hsv_v", "亮度"),
                          ("hsv_h", "色相"), ("hsv_s", "饱和度")):
            if p.get(key):
                rows.append((name, "{} {}".format(key, _num(p[key]))))
        return rows
    for key, name in (("HorizontalFlip", "水平翻转"), ("VerticalFlip", "垂直翻转"),
                      ("Rotate", "旋转"), ("Affine", "仿射"),
                      ("RandomBrightnessContrast", "亮度/对比度"),
                      ("ColorJitter", "颜色抖动"), ("GaussianBlur", "高斯模糊"),
                      ("GaussNoise", "高斯噪声")):
        frag = p.get(key)
        if frag:
            rows.append((name, _frag_text(key, frag)))
    return rows


# 参数栏窄, 长键名压短: 右侧要放得下 "bri .2 con .2 sat .2 hue .1 p .5"
_SHORT_KEY = {"brightness": "bri", "contrast": "con", "saturation": "sat",
              "brightness_limit": "bri", "contrast_limit": "con",
              "translate_percent": "trans", "blur_limit": "k"}


def _frag_text(key, frag):
    if key == "Affine":
        lo, hi = frag.get("scale", (1.0, 1.0))
        return "scale {}~{} p {}".format(_num(lo), _num(hi),
                                         _num(frag.get("p", 1.0)))
    if key == "GaussNoise":
        lo, hi = frag.get("std_range", (0.0, 0.0))
        return "std {}~{} p {}".format(_num(lo), _num(hi),
                                       _num(frag.get("p", 1.0)))
    if key == "GaussianBlur":
        return "k {} p {}".format(frag.get("blur_limit", 3),
                                  _num(frag.get("p", 1.0)))
    if key == "Rotate":
        return "±{} p {}".format(_num(frag.get("limit", 0)),
                                 _num(frag.get("p", 1.0)))
    body = []
    for k, v in frag.items():
        name = _SHORT_KEY.get(k, k)
        if isinstance(v, (int, float)):
            body.append("{} {}".format(name, _num(v)))
        elif isinstance(v, (tuple, list)) and len(v) == 2:
            body.append("{} {}~{}".format(name, _num(v[0]), _num(v[1])))
    return " ".join(body)
