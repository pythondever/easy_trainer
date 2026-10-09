# -*- coding: utf-8 -*-
"""
字符检测/识别训练执行脚本(由 UI 以子进程方式启动).
用法: main(), 由 train_worker 以 -c 导入后调用(打包后是 pyd, 不能 python -m 启动)
config 字段见 dialogs.make_train_config:
  task=ocr_det/ocr_rec, architecture=检测/识别代号, epochs, batch_size,
  lr, img_size, grad_accum, device, datasets[{split,image_paths,label_paths}]

输出(TrainWorker 解析):
  - 每 epoch: [train] EPOCH N/M
              [train] METRICS {"epochs": [...], "series": {...}, "per_class": {}}
  - 结束:     [train] RESULT {"ok", "task", "det_f1"/"cer", "model_path"}
  - 落盘:     ts_dir/checkpoint_best.pth + result.json + metrics.json

一次只跑一段: 字符检测在界面上是一项, 入队时被拆成检测段和识别段两条,
各自是独立的一条训练记录.
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

from PySide6.QtCore import QCoreApplication as QC

try:
    import numpy as np
    import torch
    from torch.utils.data import DataLoader
    import doctr.transforms as T
    from doctr.datasets import DetectionDataset, RecognitionDataset
    from doctr.models import detection, recognition
    from doctr.utils.metrics import LocalizationConfusion
except Exception as e:
    print("[train] " + QC.translate(
        "OcrTrainRunner", "缺少训练依赖: {}").format(e), flush=True)
    sys.exit(1)

from app.core import i18n
from app.core.metrics import cer
from app.train import ocr_common as occ
from app.train import ocr_data
from app.train import ocr_weights

RECO_SIZE = (32, 128)     # 识别段输入固定, 不吃界面上的 img_size


def _collate(batch):
    """图像堆成 tensor, 真值保持 list(每张图的框数不一样, 堆不动)."""
    return torch.stack([b[0] for b in batch]), [b[1] for b in batch]


def _device_of(cfg):
    d = str(cfg.get("device", "") or "")
    return "cuda" if d.startswith("cuda") and torch.cuda.is_available() else "cpu"


def _optimizer(model, name, lr):
    if name == "sgd":
        return torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9,
                               weight_decay=1e-4)
    if name == "adam":
        return torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    return torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)


def _emit(ts_dir, ep, epochs, series, extra=""):
    payload = {"epochs": list(range(1, ep + 1)), "series": series,
               "per_class": {}}
    print("[train] EPOCH {}/{}".format(ep, epochs), flush=True)
    print("[train] METRICS {}".format(json.dumps(payload, ensure_ascii=False)),
          flush=True)
    if extra:
        print("[train] " + extra, flush=True)
    with open(os.path.join(ts_dir, "metrics.json"), "w",
              encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)


def _to_boxes(arr):
    """统一成 (N, 4) 外接框: 多边形取包围盒, 预测的 (N, 5) 去掉末列得分."""
    a = np.asarray(arr, dtype=np.float32)
    if a.size == 0:
        return np.zeros((0, 4), dtype=np.float32)
    if a.ndim == 3:
        return np.stack([a[:, :, 0].min(1), a[:, :, 1].min(1),
                         a[:, :, 0].max(1), a[:, :, 1].max(1)], -1)
    a = a.reshape(-1, a.shape[-1])
    return a[:, :4]


def _f1(recall, precision):
    if not recall or not precision:
        return 0.0
    return 2 * recall * precision / (recall + precision)


def _build_det(arch):
    """优先微调官方预训练权重: 文本像素占比不到 1%, 从零训收敛不出可用框."""
    ocr_weights.ensure(arch)
    fn = getattr(detection, arch)
    for kw, tag in (({"pretrained": True}, "pretrained"),
                    ({"pretrained": False, "pretrained_backbone": True},
                     "backbone"),
                    ({"pretrained": False, "pretrained_backbone": False},
                     "scratch")):
        try:
            model = fn(**kw)
        except Exception:
            continue
        print("[train] " + QC.translate(
            "OcrTrainRunner", "检测模型 {} 权重来源: {}").format(arch, tag),
            flush=True)
        return model
    raise RuntimeError(QC.translate(
        "OcrTrainRunner", "检测模型 {} 构建失败").format(arch))


def _build_rec(arch, vocab):
    """识别段的输出层要按我们的词表重建, 只能复用骨干, 不能用官方完整权重."""
    ocr_weights.ensure(arch)
    fn = getattr(recognition, arch)
    for kw, tag in (({"pretrained": False, "pretrained_backbone": True},
                     "backbone"),
                    ({"pretrained": False, "pretrained_backbone": False},
                     "scratch")):
        try:
            model = fn(vocab=vocab, **kw)
        except Exception:
            continue
        print("[train] " + QC.translate(
            "OcrTrainRunner", "识别模型 {} 权重来源: {}").format(arch, tag),
            flush=True)
        return model
    raise RuntimeError(QC.translate(
        "OcrTrainRunner", "识别模型 {} 构建失败").format(arch))


def _train_det(cfg, ts_dir):
    size = int(cfg.get("img_size", 1024))
    code = cfg.get("architecture", "")
    arch = occ.stage_of(occ.DET_TASK, code)
    model = _build_det(arch)
    datasets = cfg.get("datasets", [])
    root = os.path.join(cfg["out_root"], str(cfg["project"]) + "_ocr", "det")
    tr_dir, tr_lab = ocr_data.write_det(
        os.path.join(root, "train"), ocr_data.collect(datasets, "train"))
    va_dir, va_lab = ocr_data.write_det(
        os.path.join(root, "val"), ocr_data.collect(datasets, "val"))
    tf = T.Resize((size, size))
    train_set = DetectionDataset(tr_dir, tr_lab, use_polygons=True,
                                 img_transforms=tf)
    val_set = DetectionDataset(va_dir, va_lab, use_polygons=True,
                               img_transforms=tf)
    return _run(cfg, ts_dir, model, arch, train_set, val_set, "F1@0.5")


def _train_rec(cfg, ts_dir):
    code = cfg.get("architecture", "")
    arch = occ.stage_of(occ.RECO_TASK, code)
    datasets = cfg.get("datasets", [])
    root = os.path.join(cfg["out_root"], str(cfg["project"]) + "_ocr", "rec")
    tr_samples = ocr_data.collect(datasets, "train")
    va_samples = ocr_data.collect(datasets, "val")
    vocab = ocr_data.build_vocab(tr_samples + va_samples)
    if not vocab:
        raise RuntimeError(QC.translate(
            "OcrTrainRunner", "标注里没有任何文字, 无法训练字符识别"))
    model = _build_rec(arch, vocab)
    tr_dir, tr_lab = ocr_data.write_rec(os.path.join(root, "train"), tr_samples)
    va_dir, va_lab = ocr_data.write_rec(os.path.join(root, "val"), va_samples)
    tf = T.Resize(RECO_SIZE)
    train_set = RecognitionDataset(tr_dir, tr_lab, img_transforms=tf)
    val_set = RecognitionDataset(va_dir, va_lab, img_transforms=tf)
    print("[train] " + QC.translate(
        "OcrTrainRunner", "词表 {} 个字符").format(len(vocab)), flush=True)
    return _run(cfg, ts_dir, model, arch, train_set, val_set, "CER")


def _run(cfg, ts_dir, model, arch, train_set, val_set, primary):
    epochs = int(cfg.get("epochs", 50))
    batch_size = int(cfg.get("batch_size", 4))
    accum = max(int(cfg.get("grad_accum", 1) or 1), 1)
    num_workers = int(cfg.get("num_workers", 0))
    early_stop = int(cfg.get("early_stop", 0) or 0)
    device = _device_of(cfg)
    is_rec = primary == "CER"
    print("[train] " + QC.translate(
        "OcrTrainRunner",
        "字符{}训练: model={} device={} epochs={} batch={} lr={}").format(
        QC.translate("OcrTrainRunner", "识别") if is_rec
        else QC.translate("OcrTrainRunner", "检测"),
        arch, device, epochs, batch_size, cfg.get("lr", 1e-4)), flush=True)
    if len(train_set) == 0:
        raise RuntimeError(QC.translate(
            "OcrTrainRunner", "训练集没有可用的文本标注"))
    if len(val_set) == 0:
        raise RuntimeError(QC.translate(
            "OcrTrainRunner", "验证集没有可用的文本标注"))
    print("[train] " + QC.translate(
        "OcrTrainRunner", "数据集: train={} val={}").format(
        len(train_set), len(val_set)), flush=True)

    pin = device == "cuda"
    loader_kw = {"batch_size": batch_size, "num_workers": num_workers,
                 "collate_fn": _collate, "pin_memory": pin}
    if num_workers > 0:
        loader_kw["persistent_workers"] = True
    train_loader = DataLoader(train_set, shuffle=True, **loader_kw)
    val_loader = DataLoader(val_set, shuffle=False, **loader_kw)

    model.to(device)
    optimizer = _optimizer(model, str(cfg.get("optimizer", "adamw")),
                           float(cfg.get("lr", 1e-4)))
    series = {"train_loss": [], "val_loss": [], primary: []}
    best = None
    no_improve = 0
    last_ep = 0
    ckpt = os.path.join(ts_dir, "checkpoint_best.pth")

    def _better(v):
        # 识别段主指标是 CER, 越小越好
        if best is None:
            return True
        return v < best if is_rec else v > best

    for ep in range(1, epochs + 1):
        last_ep = ep
        model.train()
        run_loss = 0.0
        seen = 0
        optimizer.zero_grad()
        for i, (x, tgt) in enumerate(train_loader):
            x = x.to(device, non_blocking=pin)
            loss = model(x, tgt)["loss"]
            (loss / accum).backward()
            run_loss += float(loss.item())
            seen += 1
            if (i + 1) % accum == 0 or i + 1 == len(train_loader):
                optimizer.step()
                optimizer.zero_grad()
        train_loss = run_loss / max(seen, 1)

        model.eval()
        val_loss = 0.0
        seen = 0
        refs, hyps = [], []
        metric = LocalizationConfusion(iou_thresh=0.5)
        with torch.no_grad():
            for x, tgt in val_loader:
                x = x.to(device, non_blocking=pin)
                out = model(x, tgt, return_preds=True)
                val_loss += float(out["loss"].item())
                seen += 1
                preds = out.get("preds") or []
                for t_i, p_i in zip(tgt, preds):
                    if is_rec:
                        refs.append(str(t_i))
                        hyps.append(str(p_i[0]) if p_i else "")
                    else:
                        metric.update(_to_boxes(t_i.get("words")),
                                      _to_boxes(p_i.get("words")))
        val_loss = val_loss / max(seen, 1)
        if is_rec:
            value = cer(refs, hyps)
        else:
            rec, prec, _iou = metric.summary()
            value = _f1(rec, prec)
        if value is None:
            value = 0.0
        series["train_loss"].append(round(train_loss, 4))
        series["val_loss"].append(round(val_loss, 4))
        series[primary].append(round(value, 4))
        _emit(ts_dir, ep, epochs, series,
              "epoch={} train_loss={:.4f} val_loss={:.4f} {}={:.4f}".format(
                  ep, train_loss, val_loss, primary, value))
        if _better(value):
            best = value
            no_improve = 0
            torch.save({"state_dict": model.state_dict(),
                        "architecture": arch, "vocab": getattr(model, "vocab", ""),
                        "task": cfg.get("task", "")}, ckpt)
        else:
            no_improve += 1
            if early_stop > 0 and no_improve >= early_stop:
                print("[train] " + QC.translate(
                    "OcrTrainRunner",
                    "早停触发: 连续 {} 个 epoch 无提升").format(early_stop),
                    flush=True)
                break

    result = {"ok": True, "task": cfg.get("task", ""), primary: best,
              "model_path": ckpt, "architecture": arch}
    payload = {"epochs": list(range(1, last_ep + 1)), "series": series,
               "per_class": {}}
    with open(os.path.join(ts_dir, "result.json"), "w",
              encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
    with open(os.path.join(ts_dir, "metrics.json"), "w",
              encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    print("[train] RESULT {}".format(json.dumps(result, ensure_ascii=False)),
          flush=True)


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    i18n.apply_cli(cfg.get("language", ""))
    ts_dir = cfg["timestamp_dir"]
    os.makedirs(cfg["out_root"], exist_ok=True)
    os.makedirs(ts_dir, exist_ok=True)
    shutil.copy2(cfg_path, os.path.join(ts_dir, "config.json"))
    print("[train] " + QC.translate(
        "OcrTrainRunner", "本次训练输出目录(时间戳): {}").format(ts_dir),
        flush=True)
    if str(cfg.get("task", "")) == occ.RECO_TASK:
        _train_rec(cfg, ts_dir)
    else:
        _train_det(cfg, ts_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
