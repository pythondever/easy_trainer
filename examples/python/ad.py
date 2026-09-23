# -*- coding: utf-8 -*-
"""
异常检测推理示例.

和检测/分割的示例不同: AD 模型是"骨干 + 良品特征库"的组合结构, 没有 ONNX 版本,
所以这里用 anomalib 直接加载模型文件, 不依赖 onnxruntime.

用法:
    python ad.py --model 模型.pt --images D:/待测图像
    python ad.py --model 模型.pt --images D:/待测图像 --threshold 35.0
"""

import argparse
import os
import shutil
import tempfile

import torch


def load_model(model_path):
    """按模型文件里存的构造参数重建模型, 返回 (模型, 阈值, 输入尺寸)."""
    import anomalib.models as M

    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    size = int(ckpt.get("img_size") or 0)
    cls = getattr(M, ckpt["cls_name"])
    kwargs = dict(ckpt.get("kwargs") or {})
    if size:
        kwargs["pre_processor"] = cls.configure_pre_processor(image_size=(size, size))
    model = cls(**kwargs)
    model.load_state_dict(ckpt["state_dict"])
    return model, float(ckpt.get("threshold") or 0.0), size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="模型文件, 如 ad_model.pt")
    ap.add_argument("--images", required=True, help="待测图像目录")
    ap.add_argument("--threshold", type=float, default=None,
                    help="不传就用模型里存的那个(训练时在验证集上定好的)")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()

    if not os.path.isdir(args.images):
        raise SystemExit("找不到图像目录: {}".format(args.images))

    from anomalib.data import PredictDataset
    from anomalib.engine import Engine

    model, threshold, size = load_model(args.model)
    if args.threshold is not None:
        threshold = args.threshold
    print("阈值 {:.6f}   输入 {}".format(threshold, size or "原尺寸"))

    # anomalib 不收含非 ASCII 的路径(实测报 "Path contains non-printable
    # characters"), 这种目录先铺一份 ASCII 副本再推理
    work = tempfile.mkdtemp(prefix="ad_predict_")
    stage = ""
    images = args.images
    if not args.images.isascii():
        stage = os.path.join(work, "images")
        shutil.copytree(args.images, stage)
        images = stage
    try:
        engine = Engine(max_epochs=1, accelerator=args.device, devices=1,
                        logger=False, barebones=True,
                        enable_progress_bar=False, enable_model_summary=False,
                        default_root_dir=os.path.join(work, "lightning"))
        ds = PredictDataset(path=images, image_size=(size, size)) if size \
            else PredictDataset(path=images)
        out = engine.predict(model=model, dataset=ds, return_predictions=True)

        total = bad = 0
        for batch in out or []:
            for i in range(batch.pred_score.shape[0]):
                score = float(batch.pred_score[i].flatten()[0])
                hit = score >= threshold
                total += 1
                bad += 1 if hit else 0
                # 还原成调用方给的路径, 临时副本的路径对使用者没有意义
                path = str(batch.image_path[i])
                if stage and path.startswith(images + os.sep):
                    path = os.path.join(args.images, path[len(images) + 1:])
                print("{}\t{:.4f}\t{}".format(path, score, "NG" if hit else "OK"))
        print("共 {} 张, 判为异常 {} 张".format(total, bad))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
