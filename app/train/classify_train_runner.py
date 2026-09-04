# -*- coding: utf-8 -*-
"""图像分类训练执行脚本（由 UI 以子进程方式启动）。

用法: python -m app.train.classify_train_runner <config.json>
config 字段见 dialogs.py ClassifyDialog._build_train_config：
  task=classify, architecture=resnet18/34/50/101, num_classes, epochs,
  batch_size, lr, img_size, device, datasets[{split,image_path,label_fmt}]

输出协议（TrainWorker 解析）:
  - 每 epoch: [train] EPOCH N/M
              [train] METRICS {"epochs": [...], "series": {...}, "per_class": {...}}
              [train] epoch=.. train_loss=.. val_loss=.. acc=..
  - 结束:     [train] RESULT {"ok", "accuracy", "model_path", ...}
  - 落盘:     ts_dir/checkpoint_best.pth + result.json + metrics.json
per_class 结构: {类别名: {"total": n, "correct": c, "accuracy": [每epoch累积...]}}
"""

import json
import os
import shutil
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
    from torch.utils.data import DataLoader, Dataset
    from torchvision import transforms, models
    from PIL import Image
except Exception as e:
    print("[train] 缺少训练依赖: {}".format(e), flush=True)
    sys.exit(1)

_IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def _scan_classes(root):
    """扫描根目录下的类别子文件夹名（排序）。"""
    out = []
    if os.path.isdir(root):
        for entry in sorted(os.listdir(root)):
            if os.path.isdir(os.path.join(root, entry)):
                out.append(entry)
    return out


class _ImageFolderSimple(Dataset):
    """「根目录/类别子文件夹/图像」结构的分类数据集。"""

    def __init__(self, root, transform=None, class_to_idx=None):
        self.samples = []
        self.classes = []
        for entry in sorted(os.listdir(root)):
            sub = os.path.join(root, entry)
            if not os.path.isdir(sub):
                continue
            if entry not in self.classes:
                self.classes.append(entry)
            # class_to_idx 提供时用统一全局索引(train/val 类别顺序一致)
            ci = (class_to_idx[entry] if class_to_idx is not None
                  else self.classes.index(entry))
            for fn in sorted(os.listdir(sub)):
                if fn.lower().endswith(_IMG_EXTS):
                    self.samples.append((os.path.join(sub, fn), ci))
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, ci = self.samples[idx]
        im = Image.open(path).convert("RGB")
        if self.transform is not None:
            im = self.transform(im)
        return im, ci


def _make_model(arch, num_classes):
    variants = {
        "resnet18": models.resnet18, "resnet34": models.resnet34,
        "resnet50": models.resnet50, "resnet101": models.resnet101,
    }
    model = variants.get(arch, models.resnet18)(weights=None)
    in_f = model.fc.in_features
    model.fc = nn.Linear(in_f, num_classes)
    return model


def _collect_images(datasets, split, dest):
    """
    把某个 split 的所有分类数据集图像复制到 dest/{类别}/。
    每次训练前清空 dest 重建
    """
    if os.path.isdir(dest):
        shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(dest, exist_ok=True)
    n_total = 0
    for ds in datasets:
        if ds.get("split") != split:
            continue
        img_root = ds.get("image_path", "")
        if not img_root or not os.path.isdir(img_root):
            continue
        for entry in sorted(os.listdir(img_root)):
            sub = os.path.join(img_root, entry)
            if not os.path.isdir(sub):
                continue
            d = os.path.join(dest, entry)
            os.makedirs(d, exist_ok=True)
            for fn in sorted(os.listdir(sub)):
                if not fn.lower().endswith(_IMG_EXTS):
                    continue
                src = os.path.join(sub, fn)
                dst = os.path.join(d, fn)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    n_total += 1
    # 删除空类别目录
    if os.path.isdir(dest):
        for entry in os.listdir(dest):
            p = os.path.join(dest, entry)
            if os.path.isdir(p) and not os.listdir(p):
                try:
                    os.rmdir(p)
                except OSError:
                    pass
    return n_total


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    out_root = cfg["out_root"]
    project = cfg["project"]
    ts_dir = cfg["timestamp_dir"]
    os.makedirs(out_root, exist_ok=True)
    os.makedirs(ts_dir, exist_ok=True)
    shutil.copy2(cfg_path, os.path.join(ts_dir, "config.json"))
    print("[train] 输出路径: {}".format(out_root), flush=True)
    print("[train] 本次训练输出目录(时间戳): {}".format(ts_dir), flush=True)

    epochs = int(cfg.get("epochs", 30))
    batch_size = int(cfg.get("batch_size", 32))
    lr = float(cfg.get("lr", 0.001))
    img_size = int(cfg.get("img_size", 224))
    num_classes = int(cfg.get("num_classes", 10))
    arch = cfg.get("architecture", "resnet18")
    num_workers = int(cfg.get("num_workers", 4))
    optimizer_name = cfg.get("optimizer", "adamw")
    early_stop = int(cfg.get("early_stop", 0))   # >0 启用(patience),<=0 禁用
    device = cfg.get("device", "cpu")
    if device.startswith("cuda") and torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print("[train] 分类训练: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}".format(
        arch, num_classes, device, epochs, batch_size, lr, img_size, optimizer_name), flush=True)

    # 1) 数据准备：按 split 复制到 out_root/{project}_cls/{train,val}/{类别}/
    cls_root = os.path.join(out_root, project + "_cls")
    train_root = os.path.join(cls_root, "train")
    val_root = os.path.join(cls_root, "val")
    n_train = _collect_images(cfg.get("datasets", []), "train", train_root)
    n_val = _collect_images(cfg.get("datasets", []), "val", val_root)
    print("[train] 数据准备: train={} 张, val={} 张".format(n_train, n_val), flush=True)
    if n_train == 0:
        raise RuntimeError("训练集无图像，请检查数据集")
    if n_val == 0:
        raise RuntimeError("验证集无图像，请检查数据集")

    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    train_tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    train_ds = _ImageFolderSimple(train_root, train_tf)
    val_ds = _ImageFolderSimple(val_root, val_tf)
    # 类别数以实际数据为准(训练集 + 验证集并集),并统一为全局索引,
    # 保证验证时 y 的类索引与模型输出维度一致(train/val 顺序必须一致).
    classes = sorted(set(train_ds.classes) | set(val_ds.classes))
    class_to_idx = {c: i for i, c in enumerate(classes)}
    if class_to_idx != {c: i for i, c in enumerate(train_ds.classes)}:
        train_ds = _ImageFolderSimple(train_root, train_tf, class_to_idx)
        val_ds = _ImageFolderSimple(val_root, val_tf, class_to_idx)
    if not classes:
        raise RuntimeError("未从数据集中解析到任何类别(子文件夹),无法训练图像分类")
    real_classes = len(classes)
    _pin = getattr(device, "type", str(device)) == "cuda"
    _persistent = num_workers > 0
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                              num_workers=num_workers, drop_last=True,
                              pin_memory=_pin, persistent_workers=_persistent)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                            num_workers=num_workers,
                            pin_memory=_pin, persistent_workers=_persistent)
    print("[train] 数据集: train={} val={} 类别({})={}".format(
        len(train_ds), len(val_ds), len(classes),
        ", ".join(classes) if len(classes) <= 12 else "{}...".format(
            ", ".join(classes[:12]))), flush=True)

    # 2) 模型
    model = _make_model(arch, real_classes)
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    if optimizer_name == "sgd":
        optimizer = torch.optim.SGD(model.parameters(), lr=lr,
                                    momentum=0.9, weight_decay=1e-4)
    else:
        optimizer = torch.optim.AdamW(model.parameters(), lr=lr,
                                      weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

    best_acc = 0.0
    no_improve = 0
    last_ep = 0
    series = {"accuracy": [], "train_loss": [], "val_loss": []}
    per_class = {}   # {类别名: {"total": n, "correct": c, "accuracy": [每epoch...]}}
    for ep in range(1, epochs + 1):
        last_ep = ep
        model.train()
        run_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            run_loss += loss.item() * x.size(0)
        train_loss = run_loss / max(len(train_ds), 1)
        model.eval()
        val_loss = 0.0
        correct = 0
        per_ep = {ci: [0, 0] for ci in range(len(classes))}   # 类索引: [correct, total]
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                out = model(x)
                loss = criterion(out, y)
                val_loss += loss.item() * x.size(0)
                preds = out.argmax(1)
                correct += (preds == y).sum().item()
                for i in range(y.size(0)):
                    yi = int(y[i].item())
                    st = per_ep.get(yi)
                    if st is not None:
                        st[1] += 1
                        if int(preds[i].item()) == yi:
                            st[0] += 1
        val_loss = val_loss / max(len(val_ds), 1)
        acc = correct / max(len(val_ds), 1)
        # 每类精度(total/correct 为当前 epoch 统计,accuracy 按 epoch 累积)
        for ci, cname in enumerate(classes):
            st = per_ep.get(ci, [0, 0])
            pc = per_class.setdefault(
                cname, {"total": 0, "correct": 0, "accuracy": []})
            pc["total"] = st[1]
            pc["correct"] = st[0]
            pc["accuracy"].append(round(st[0] / max(st[1], 1), 4))
        series["accuracy"].append(round(acc, 4))
        series["train_loss"].append(round(train_loss, 4))
        series["val_loss"].append(round(val_loss, 4))
        metrics_payload = {"epochs": list(range(1, ep + 1)),
                           "series": series, "per_class": per_class}
        print("[train] EPOCH {}/{}".format(ep, epochs), flush=True)
        print("[train] METRICS {}".format(json.dumps(
            metrics_payload, ensure_ascii=False)), flush=True)
        print("[train] epoch={} train_loss={:.4f} val_loss={:.4f} acc={:.4f}".format(
            ep, train_loss, val_loss, acc), flush=True)
        # 每 epoch 落盘 metrics.json(TrainWorker 轮询读)
        with open(os.path.join(ts_dir, "metrics.json"), "w",
                  encoding="utf-8") as f:
            json.dump(metrics_payload, f, ensure_ascii=False)
        if acc > best_acc:
            best_acc = acc
            no_improve = 0
            torch.save({"state_dict": model.state_dict(), "classes": classes,
                        "architecture": arch},
                       os.path.join(ts_dir, "checkpoint_best.pth"))
        else:
            no_improve += 1
            if early_stop > 0 and no_improve >= early_stop:
                print("[train] 早停触发: 连续 {} 个 epoch 精度无提升".format(early_stop),
                      flush=True)
                break
        scheduler.step()

    print("[train] 训练完成 best_acc={:.4f}".format(best_acc), flush=True)

    # 模型目录生成 classes.txt: 每行 "id 类别名"(交付他人使用时显式对照)
    classes_path = os.path.join(ts_dir, "classes.txt")
    try:
        with open(classes_path, "w", encoding="utf-8") as f:
            for i, lb in enumerate(classes):
                f.write("{} {}\n".format(i, lb))
        print("[train] 生成类别文件: {}".format(classes_path), flush=True)
    except Exception:
        pass

    # 3) 结果汇总
    result = {
        "ok": True,
        "accuracy": round(best_acc, 4),
        "model_path": os.path.join(ts_dir, "checkpoint_best.pth"),
        "num_classes": len(classes),
    }
    metrics_payload = {"epochs": list(range(1, last_ep + 1)),
                       "series": series, "per_class": per_class}
    with open(os.path.join(ts_dir, "result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
    with open(os.path.join(ts_dir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, ensure_ascii=False)
    print("[train] RESULT {}".format(json.dumps(result, ensure_ascii=False)),
          flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
