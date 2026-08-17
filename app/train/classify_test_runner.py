# -*- coding: utf-8 -*-
"""图像分类测试执行脚本（由 UI 以子进程方式启动）。

用法: python -m app.train.classify_test_runner <config.json>
config: model_path(分类 checkpoint), image_path, has_label, device, total, task=classify
输出:
  - [test] 进度 N/M
  - [test] RESULT {"ok", "total", "accuracy",
                   "per_class": {类别: {total, correct, error}}, "task": "classify"}
"""

import json
import os
import sys
import traceback

_WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
for _p in (_WORKSPACE, os.path.join(_WORKSPACE, "app")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    import torch
    import torch.nn as nn
    from torchvision import transforms, models
    from PIL import Image
except Exception as e:
    print("[test] 缺少测试依赖: {}".format(e), flush=True)
    sys.exit(1)

_IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def _make_model(arch, num_classes):
    variants = {
        "resnet18": models.resnet18, "resnet34": models.resnet34,
        "resnet50": models.resnet50, "resnet101": models.resnet101,
    }
    model = variants.get(arch, models.resnet18)(weights=None)
    in_f = model.fc.in_features
    model.fc = nn.Linear(in_f, num_classes)
    return model


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    model_path = cfg.get("model_path", "")
    image_path = cfg.get("image_path", "")
    device = cfg.get("device", "cpu")
    if device.startswith("cuda") and torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print("[test] 加载分类模型: {}".format(os.path.basename(model_path)),
          flush=True)
    ckpt = torch.load(model_path, map_location="cpu")
    classes = list(ckpt.get("classes") or [])
    arch = ckpt.get("architecture", "resnet18")
    model = _make_model(arch, max(len(classes), 1))
    model.load_state_dict(ckpt["state_dict"])
    model.to(device).eval()
    img_size = int(cfg.get("img_size", 224))
    tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])
    # 收集图像(含子文件夹)
    images = []
    for root, _, files in os.walk(image_path or ""):
        for fn in sorted(files):
            if fn.lower().endswith(_IMG_EXTS):
                images.append(os.path.join(root, fn))
    print("[test] 测试图片 {} 张".format(len(images)), flush=True)
    total = 0
    correct = 0
    per_class = {}
    for i, p in enumerate(images):
        try:
            im = Image.open(p).convert("RGB")
            x = tf(im).unsqueeze(0).to(device)
            with torch.no_grad():
                out = model(x)
            pred = classes[out.argmax(1).item()] if classes else "?"
        except Exception:
            pred = "?"
        true_cls = os.path.basename(os.path.dirname(p)) or "(无类别)"
        pc = per_class.setdefault(true_cls, {"total": 0, "correct": 0, "error": 0})
        pc["total"] += 1
        if pred == true_cls:
            correct += 1
            pc["correct"] += 1
        else:
            pc["error"] += 1
        total += 1
        if (i + 1) % 10 == 0 or i + 1 == len(images):
            print("[test] 进度 {}/{}".format(i + 1, len(images)), flush=True)
    acc = correct / total if total else 0.0
    result = {
        "ok": True, "total": total, "accuracy": round(acc, 4),
        "per_class": per_class, "task": "classify",
    }
    print("[test] RESULT {}".format(json.dumps(result, ensure_ascii=False)),
          flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
