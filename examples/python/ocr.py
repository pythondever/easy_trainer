# -*- coding: utf-8 -*-
"""
OCR 推理示例（字符检测 + 字符识别）。
导出的是两段模型：检测段找文字框，识别段读框里的字。只做检测就不给 --rec。

用法:
  python ocr.py --det 检测.onnx --image test.jpg
  python ocr.py --det 检测.onnx --rec 识别.onnx --image test.jpg --save out.jpg
"""

import argparse
import json
import os

import cv2
import numpy as np
import onnxruntime as ort

from common import MEAN, STD, input_size, preprocess, sigmoid

DET_SIZE = 1024        # 与训练时的检测尺寸一致
BIN_THR = 0.3          # 概率图二值化阈值
BOX_THR = 0.1          # 框得分下限
MIN_BOX = 2            # 框的最小边长（像素），与官方后处理一致
TEXT_LABEL = "文本"     # 与软件内保留的文本标签一致


def det_boxes(logits, orig_wh, bin_thr, box_thr):
    """
    检测段输出 → [(x1, y1, x2, y2, 得分)]，已还原到原图像素。
    模型吐的是没过 sigmoid 的 logits（官方 predictor 里才做），这里补上；
    形状 (1, 1, h, w)，单通道概率图。开运算是照官方后处理抄的：不加的话
    概率图边缘的零星激活会碎成一堆 1~2 像素的假框。
    """
    prob = sigmoid(logits[0, 0])
    mask = (prob >= bin_thr).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mh, mw = prob.shape[:2]
    ow, oh = orig_wh
    # 训练是方形缩放（不保持宽高比），所以宽高各按各的比例还原
    sx, sy = ow / float(mw), oh / float(mh)
    out = []
    for cnt in cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]:
        x, y, bw, bh = cv2.boundingRect(cnt)
        if bw < MIN_BOX or bh < MIN_BOX:
            continue
        score = float(prob[y:y + bh, x:x + bw].mean())
        if score < box_thr:
            continue
        out.append((x * sx, y * sy, (x + bw) * sx, (y + bh) * sy, score))
    return out


def rec_input(crop, width, height):
    """
    字条 → 识别段输入。保长宽比缩到能放进 (height, width), 右侧与下方补零。
    训练侧是 T.Resize(..., preserve_aspect_ratio=True), 这里直接拉伸会把
    16:1 的字条横向压扁好几倍。
    """
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    ih, iw = rgb.shape[:2]
    scale = min(height / float(ih), width / float(iw))
    nh = max(int(round(ih * scale)), 1)
    nw = max(int(round(iw * scale)), 1)
    resized = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_LINEAR)
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    canvas[:nh, :nw] = resized
    x = canvas.astype(np.float32) / 255.0
    x = (x - MEAN) / STD
    return np.ascontiguousarray(np.transpose(x, (2, 0, 1))[None])


def ctc_decode(logits, vocab, blank):
    """
    (T, C) logits → (文本, 置信度)。
    C = len(vocab) + 1，blank 在最后一维（不是第 0 维，常见 CTC 实现里
    blank 放首位，这里不是）。置信度取各时间步最高概率的最小值，和官方
    predictor 的口径一致。
    """
    probs = np.exp(logits - logits.max(axis=-1, keepdims=True))
    probs /= probs.sum(axis=-1, keepdims=True)
    path = probs.argmax(axis=-1)
    conf = float(probs.max(axis=-1).min()) if path.size else 0.0
    chars, prev = [], -1
    for idx in path:
        idx = int(idx)
        # 先逐帧合并重复（CTC 的 collapse），再去 blank
        if idx != prev and idx != blank:
            chars.append(vocab[idx] if idx < len(vocab) else "")
        prev = idx
    return "".join(chars), conf


def read_vocab(path):
    """
    vocab.txt 是一整串字符（无换行）。只去换行不 strip 空格 —— 词表里
    可能有空格字符。
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().replace("\r", "").replace("\n", "")
    except OSError:
        return ""


def write_json(img_path, iw, ih, rows):
    """写出 labelme 标注（带 OCR 标志位），可直接拖回软件当标注用。"""
    shapes = []
    for x1, y1, x2, y2, _score, text in rows:
        shape = {
            "label": TEXT_LABEL,
            "points": [[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y1, 2)],
                       [round(x2, 2), round(y2, 2)], [round(x1, 2), round(y2, 2)]],
            "group_id": None,
            "shape_type": "polygon",
            "flags": {},
        }
        if text:
            shape["text"] = text
        shapes.append(shape)
    doc = {"version": "5.0.1", "flags": {}, "shapes": shapes,
           "imagePath": os.path.basename(img_path), "imageData": None,
           "imageWidth": iw, "imageHeight": ih, "ocr": True}
    out = os.path.splitext(img_path)[0] + ".json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--det", required=True, help="字符检测模型 onnx")
    ap.add_argument("--rec", default="", help="字符识别模型 onnx，给了才出文字")
    ap.add_argument("--vocab", default="",
                    help="词表文件，默认取识别模型同目录的 vocab.txt")
    ap.add_argument("--image", required=True)
    ap.add_argument("--size", type=int, default=None)
    ap.add_argument("--bin-thr", type=float, default=BIN_THR)
    ap.add_argument("--box-thr", type=float, default=BOX_THR)
    ap.add_argument("--json", action="store_true",
                    help="把结果写成 labelme 标注（落在图像同目录）")
    ap.add_argument("--save", default="")
    args = ap.parse_args()

    img = cv2.imdecode(np.fromfile(args.image, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit("读图失败: {}".format(args.image))
    h, w = img.shape[:2]

    det = ort.InferenceSession(args.det, providers=["CPUExecutionProvider"])
    size = args.size or input_size(det, DET_SIZE)
    logits = det.run(None, {"images": preprocess(img, size)})[0]
    boxes = det_boxes(logits, (w, h), args.bin_thr, args.box_thr)

    rec, vocab, rec_wh = None, "", (768, 32)
    if args.rec:
        vocab = read_vocab(args.vocab or os.path.join(
            os.path.dirname(os.path.abspath(args.rec)), "vocab.txt"))
        if not vocab:
            raise SystemExit(
                "识别段要词表：用 --vocab 指定，或把 vocab.txt 放到识别模型同目录")
        rec = ort.InferenceSession(args.rec, providers=["CPUExecutionProvider"])
        shape = rec.get_inputs()[0].shape
        rec_wh = (int(shape[3]), int(shape[2]))

    rows = []
    for x1, y1, x2, y2, score in boxes:
        text = ""
        if rec is not None:
            crop = img[max(int(y1), 0):max(int(y2), 0),
                       max(int(x1), 0):max(int(x2), 0)]
            if crop.size:
                out = rec.run(None, {"images": rec_input(crop, *rec_wh)})[0]
                text, _conf = ctc_decode(out[0], vocab, len(vocab))
        rows.append((x1, y1, x2, y2, score, text))
        print("{}  {:.3f}  ({:.0f},{:.0f})-({:.0f},{:.0f})".format(
            text or "-", score, x1, y1, x2, y2))
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cap = "{} {:.2f}".format(text, score) if text else "{:.2f}".format(score)
        cv2.putText(img, cap, (int(x1), int(y1) - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if args.json:
        print("标注已写出:", write_json(args.image, w, h, rows))
    if args.save:
        cv2.imencode(".jpg", img)[1].tofile(args.save)
        print("结果已保存:", args.save)


if __name__ == "__main__":
    main()
