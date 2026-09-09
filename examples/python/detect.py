# -*- coding: utf-8 -*-
"""目标检测推理示例。

用法: python detect.py --model xxx.onnx --image test.jpg --classes classes.txt
"""

import argparse
import os
import cv2
import numpy as np
import onnxruntime as ort
from common import decode_dets, load_classes, preprocess

INPUT_SIZE = 640          # 与训练时的图像尺寸一致
SCORE_THR = 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--classes", default="classes.txt")
    ap.add_argument("--size", type=int, default=INPUT_SIZE)
    ap.add_argument("--thr", type=float, default=SCORE_THR)
    ap.add_argument("--save", default="")
    args = ap.parse_args()

    sess = ort.InferenceSession(args.model, providers=["CPUExecutionProvider"])
    img = cv2.imdecode(np.fromfile(args.image, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit("读图失败: {}".format(args.image))
    h, w = img.shape[:2]

    x = preprocess(img, args.size)
    dets, labels = sess.run(None, {"input": x})

    names = load_classes(args.classes if os.path.exists(args.classes) else "")
    for x1, y1, x2, y2, score, cid in decode_dets(dets, labels, (w, h), args.thr):
        label = names[cid] if cid < len(names) else str(cid)
        print("{}  {:.3f}  ({:.0f},{:.0f})-({:.0f},{:.0f})".format(
            label, score, x1, y1, x2, y2))
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img, "{} {:.2f}".format(label, score), (int(x1), int(y1) - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if args.save:
        cv2.imencode(".jpg", img)[1].tofile(args.save)
        print("结果已保存:", args.save)


if __name__ == "__main__":
    main()
