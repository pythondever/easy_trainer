# -*- coding: utf-8 -*-
"""
图像分类推理示例：输出 scores [1, C] 的 softmax 概率。
用法: python classify.py --model xxx.onnx --image test.jpg --classes classes.txt
"""

import argparse
import os

import cv2
import numpy as np
import onnxruntime as ort

from common import input_size, load_classes, preprocess

INPUT_SIZE = 224          # 分类模型固定 224（导出时若指定过别的尺寸就改这里）
TOP_K = 5


def softmax(v):
    v = v - v.max(axis=-1, keepdims=True)
    e = np.exp(v)
    return e / e.sum(axis=-1, keepdims=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--classes", default="classes.txt")
    ap.add_argument("--size", type=int, default=None)
    ap.add_argument("--topk", type=int, default=TOP_K)
    args = ap.parse_args()

    sess = ort.InferenceSession(args.model, providers=["CPUExecutionProvider"])
    img = cv2.imdecode(np.fromfile(args.image, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit("读图失败: {}".format(args.image))

    size = args.size or input_size(sess, INPUT_SIZE)

    scores = sess.run(None, {"images": preprocess(img, size)})[0][0]
    prob = softmax(scores)
    names = load_classes(args.classes if os.path.exists(args.classes) else "")

    for i in np.argsort(-prob)[:args.topk]:
        name = names[i] if i < len(names) else str(i)
        print("{:<20s} {:.4f}".format(name, float(prob[i])))


if __name__ == "__main__":
    main()
