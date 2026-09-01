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


class _ImageListDS(torch.utils.data.Dataset):
    """
    测试图像列表数据集。
    解码失败的样本返回 (index, None), 由 _collate 过滤掉——保证单张坏图
    不会中断整批推理(语义等价于原来 try/except 后 pred="?")。
    """

    def __init__(self, paths, tf):
        self.paths = paths
        self.tf = tf

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, i):
        try:
            with Image.open(self.paths[i]) as im:
                return i, self.tf(im.convert("RGB"))
        except Exception:
            return i, None


def _collate(batch):
    """过滤解码失败样本; 全部失败时返回 (None, None)。"""
    keep = [(i, x) for i, x in batch if x is not None]
    if not keep:
        return None, None
    idxs = torch.tensor([i for i, _ in keep], dtype=torch.long)
    xs = torch.stack([x for _, x in keep])
    return idxs, xs


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
    fc_out = int(ckpt["state_dict"]["fc.weight"].shape[0])
    model = _make_model(arch, fc_out)
    model.load_state_dict(ckpt["state_dict"])
    model.to(device).eval()
    img_size = int(cfg.get("img_size", 224))
    tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])
    # 收集图像(含子文件夹);items 支持一次测多个数据集
    items = cfg.get("items") or [{"image_path": image_path}]
    images = []
    for it in items:
        for root, _, files in os.walk(it.get("image_path") or ""):
            for fn in sorted(files):
                if fn.lower().endswith(_IMG_EXTS):
                    images.append(os.path.join(root, fn))
    print("[test] 测试图片 {} 张".format(len(images)), flush=True)
    total = 0
    correct = 0
    per_class = {}
    from torch.utils.data import DataLoader
    batch_size = max(1, int(cfg.get("batch_size", 32) or 32))
    num_workers = max(0, min(int(cfg.get("num_workers", 4) or 0),
                             (os.cpu_count() or 1)))
    loader = DataLoader(_ImageListDS(images, tf), batch_size=batch_size,
                        shuffle=False, num_workers=num_workers,
                        collate_fn=_collate,
                        pin_memory=getattr(device, "type", str(device)) == "cuda")

    preds = ["?"] * len(images)     # 解码失败的保持 "?", 与原逻辑一致
    done = 0
    for idxs, xs in loader:
        if xs is None:
            continue
        with torch.no_grad():
            out = model(xs.to(device))
        top = out.argmax(1).tolist()
        for j, i in enumerate(idxs.tolist()):
            k = int(top[j])
            if 0 <= k < len(classes):
                preds[i] = classes[k]
        done += len(idxs)
        print("[test] 进度 {}/{}".format(done, len(images)), flush=True)

    for p, pred in zip(images, preds):
        true_cls = os.path.basename(os.path.dirname(p)) or "(无类别)"
        pc = per_class.setdefault(true_cls, {"total": 0, "correct": 0, "error": 0})
        pc["total"] += 1
        if pred == true_cls:
            correct += 1
            pc["correct"] += 1
        else:
            pc["error"] += 1
        total += 1
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
