# -*- coding: utf-8 -*-
"""实例分割推理示例（CNN 分支）：在检测基础上多取一路原型图。

架构选 CNN 导出的模型用这个，选 Transformer 的用 segment.py。
CNN 走 ultralytics YOLO：输出是 output0（框 + 类别 + 掩码系数）与
output1（低分辨率原型图），掩码要自己组合出来。

用法: python segment_cnn.py --model xxx.onnx --image test.jpg --classes label_map.json
"""

import argparse
import os

import cv2
import numpy as np
import onnxruntime as ort

from common import MASK_DIM, decode_yolo_masks, input_size, letterbox, load_classes

INPUT_SIZE = 640
SCORE_THR = 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--classes", default="label_map.json")
    ap.add_argument("--size", type=int, default=None)
    ap.add_argument("--thr", type=float, default=SCORE_THR)
    ap.add_argument("--save", default="")
    args = ap.parse_args()

    sess = ort.InferenceSession(args.model, providers=["CPUExecutionProvider"])
    img = cv2.imdecode(np.fromfile(args.image, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit("读图失败: {}".format(args.image))
    h, w = img.shape[:2]

    size = args.size or input_size(sess, INPUT_SIZE)

    x, geo = letterbox(img, size)
    outs = sess.run(None, {"images": x})
    # output0 比检测多 32 行掩码系数, 类别数要减掉它们
    ncls = outs[0].shape[1] - 4 - MASK_DIM
    dets, masks = decode_yolo_masks(outs[0], outs[1][0], geo, (w, h), ncls, args.thr)

    names = load_classes(args.classes if os.path.exists(args.classes) else "")
    overlay = img.copy()
    for x1, y1, x2, y2, score, cid in dets:
        label = names[cid] if cid < len(names) else str(cid)
        print("{}  {:.3f}  ({:.0f},{:.0f})-({:.0f},{:.0f})".format(
            label, score, x1, y1, x2, y2))

    for m in masks:
        overlay[m > 0] = (0, 200, 0)
    cv2.addWeighted(overlay, 0.45, img, 0.55, 0, img)
    for x1, y1, x2, y2, score, cid in dets:
        label = names[cid] if cid < len(names) else str(cid)
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img, "{} {:.2f}".format(label, score), (int(x1), int(y1) - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if args.save:
        cv2.imencode(".jpg", img)[1].tofile(args.save)
        print("结果已保存:", args.save)


if __name__ == "__main__":
    main()
