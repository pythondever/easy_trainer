# -*- coding: utf-8 -*-
"""YOLO(ultralytics) 训练执行脚本(由 UI 以子进程方式启动).

用法与 config 字段同 train_runner, 产物也对齐同一套约定:
  <ts_dir>/metrics.csv     每 epoch 的 val 指标(列名同 rf-detr 侧, 下游零改动)
  <ts_dir>/weights/best.pt 最佳权重
  <ts_dir>/result.json     汇总, model_path 指向 best.pt
"""

import csv
import json
import os
import sys
import traceback

_WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
for _p in (_WORKSPACE, os.path.join(_WORKSPACE, "app")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from PySide6.QtCore import QCoreApplication as QC

try:
    import torch
except ImportError:
    torch = None

from app.core import i18n, model_assets
from app.core.metrics import best_map50_from_csv
from app.train.data_prep import prepare_dataset

# UI 的档位 → YOLO 权重名里那一段
_LEVELS = {"nano": "n", "small": "s", "medium": "m", "large": "l", "x-large": "x"}

# UI 的优化器名 → ultralytics 认的写法
_OPTIMIZERS = {"adamw": "AdamW", "adam": "Adam", "sgd": "SGD"}

# 转写出来的列; 顺序固定, 缺的值留空
_CSV_FIELDS = ("epoch", "time", "val/mAP_50", "val/mAP_50_95",
               "val/precision", "val/recall", "val/F1",
               "val/segm_mAP_50", "val/segm_mAP_50_95",
               "train/loss", "val/loss")

# ultralytics 列 → 内部列. (B)=box, (M)=mask; 内部沿用 rf-detr 那套名字
_BOX_MAP = (("metrics/mAP50(B)", "val/mAP_50"),
            ("metrics/mAP50-95(B)", "val/mAP_50_95"),
            ("metrics/precision(B)", "val/precision"),
            ("metrics/recall(B)", "val/recall"))
_MASK_MAP = (("metrics/mAP50(M)", "val/segm_mAP_50"),
             ("metrics/mAP50-95(M)", "val/segm_mAP_50_95"))


def _f(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _sum_loss(row, split):
    """YOLO 把损失拆成 box/cls/dfl(+seg/sem), 内部只有一列 loss, 求和."""
    total = 0.0
    hit = False
    for key, value in row.items():
        if key.startswith(split + "/") and key.endswith("_loss"):
            v = _f(value)
            if v is not None:
                total += v
                hit = True
    return round(total, 6) if hit else ""


def _f1(row):
    p, r = _f(row.get("metrics/precision(B)")), _f(row.get("metrics/recall(B)"))
    if p is None or r is None:
        return ""
    return round(2 * p * r / (p + r), 6) if (p + r) > 0 else 0.0


def _to_internal(row, task):
    """results.csv 的一行 → 内部 metrics.csv 的一行(time 原样带过, 供下游看耗时)."""
    out = {"time": row.get("time", "")}
    for src, dst in _BOX_MAP + (_MASK_MAP if task == "segment" else ()):
        v = _f(row.get(src))
        if v is not None:
            out[dst] = round(v, 6)
    out["val/F1"] = _f1(row)
    out["train/loss"] = _sum_loss(row, "train")
    out["val/loss"] = _sum_loss(row, "val")
    return out


def _read_results(path):
    """读 ultralytics 的 results.csv; 文件正被追加(末行残缺)时丢掉最后一行."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return []
    if text and not text.endswith("\n"):
        text = text[:text.rfind("\n") + 1]
    try:
        return list(csv.DictReader(text.splitlines()))
    except Exception:
        return []


def _write_metrics(rows, dst):
    """
    整体重写 metrics.csv(临时文件 + replace).

    下游 train_worker 每 5 秒全量重解析这个文件, 按 mtime 判变化; 半截文件会被
    它的"末行没有换行"检查挡掉, 这里再保证替换是原子的.
    """
    tmp = dst + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS,
                                extrasaction="ignore")
        writer.writeheader()
        for i, row in enumerate(rows):
            # results.csv 的 epoch 是 1 起, 内部 csv 是 0 起(worker 会再 +1)
            out = dict(row)
            out["epoch"] = i
            writer.writerow(out)
    os.replace(tmp, dst)


def _sync_metrics(csv_path, metrics_path, task):
    """把 ultralytics 的 results.csv 转写成内部 metrics.csv, 返回行数."""
    rows = [_to_internal(r, task) for r in _read_results(csv_path)]
    if not rows:
        return 0
    _write_metrics(rows, metrics_path)
    return len(rows)


def _device_arg(device):
    """UI 存的 cuda:0 → ultralytics 认的 0; cuda 不可用时退 cpu."""
    if not str(device).startswith("cuda"):
        return "cpu"
    if torch is None or not torch.cuda.is_available():
        return "cpu"
    parts = str(device).split(":")
    return int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0


def _pretrained_path(cfg, task):
    """训练起步用的预训练权重绝对路径; 缺文件返回空串(UI 已负责提示下载)."""
    given = cfg.get("pretrained_path")
    if given and os.path.isfile(given):
        return given
    return model_assets.resolve_path(
        task, cfg.get("architecture", "nano"),
        cfg.get("family") or "transformer")


def main():
    from ultralytics import YOLO
    from ultralytics.utils import WEIGHTS_DIR

    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    i18n.apply_cli(cfg.get("language", ""))

    out_root = cfg["out_root"]
    ts_dir = cfg["timestamp_dir"]
    os.makedirs(out_root, exist_ok=True)
    os.makedirs(ts_dir, exist_ok=True)
    print("[train] " + QC.translate("TrainRunner", "输出路径: {}").format(out_root), flush=True)
    print("[train] " + QC.translate("TrainRunner", "本次训练输出目录(时间戳): {}").format(ts_dir), flush=True)

    task = cfg.get("task", "detect")
    architecture = cfg.get("architecture", "nano")
    weights = _pretrained_path(cfg, task)
    if not weights:
        raise RuntimeError(QC.translate(
            "TrainRunner",
            "预训练权重缺失: 请先在权重管理里下载 {} 档的模型").format(
            architecture))

    model_assets.ensure_amp_weight(WEIGHTS_DIR)

    labels = prepare_dataset(out_root, project=cfg["project"],
                             datasets=cfg["datasets"], task=task)

    metrics_path = os.path.join(ts_dir, "metrics.csv")
    yolo_csv = os.path.join(ts_dir, "results.csv")

    def _flush_metrics(trainer=None):
        n = _sync_metrics(yolo_csv, metrics_path, task)
        if n and trainer is not None:
            # 收尾那轮 final_eval 也会回调, trainer.epoch 已经走到总轮数之上
            done = min(trainer.epoch + 1, trainer.epochs)
            print("[train] EPOCH {}/{}".format(done, trainer.epochs), flush=True)

    def _on_fit_epoch_end(trainer):
        _flush_metrics(trainer)

    model = YOLO(weights)
    model.add_callback("on_fit_epoch_end", _on_fit_epoch_end)
    model.add_callback("on_train_end", lambda trainer: _flush_metrics())

    epochs = int(cfg["epochs"])
    batch = int(cfg["batch_size"])
    early_stop = int(cfg.get("early_stop", 0) or 0)
    save_period = int(cfg.get("checkpoint_interval", 0) or 0)
    print("[train] " + QC.translate(
        "TrainRunner", "使用模型 {} device={} epochs={} batch={} resolution={}").format(
        architecture, cfg.get("device", "cpu"), epochs, batch,
        cfg.get("img_size", 640)), flush=True)

    model.train(
        data=os.path.join(out_root, "data.yaml"),
        epochs=epochs,
        imgsz=int(cfg.get("img_size", 640)),
        batch=batch,
        lr0=float(cfg["lr"]),
        optimizer=_OPTIMIZERS.get(str(cfg.get("optimizer", "sgd")).lower(),
                                  "auto"),
        device=_device_arg(cfg.get("device", "cpu")),
        workers=int(cfg.get("num_workers", 8)),
        # 产物落在时间戳目录下: 父目录当 project, 目录名当 name
        project=os.path.dirname(ts_dir), name=os.path.basename(ts_dir),
        exist_ok=True,
        # UI 填 0 表示不早停; YOLO 的 patience 没有"关闭"语义, 用总轮数兜底
        patience=early_stop if early_stop > 0 else epochs,
        # 梯度累积: YOLO 认的是名义批次(nbs), 折算回 UI 的累积步数语义
        nbs=max(batch * int(cfg.get("grad_accum", 4) or 1), batch),
        save_period=save_period if save_period > 0 else -1,
        seed=0,
        plots=False,
        val=True,
    )
    _flush_metrics()
    print("[train] " + QC.translate("TrainRunner", "训练完成"), flush=True)

    classes_path = os.path.join(ts_dir, "classes.txt")
    try:
        with open(classes_path, "w", encoding="utf-8") as f:
            for i, lb in enumerate(labels):
                f.write("{} {}\n".format(i, lb))
        print("[train] " + QC.translate("TrainRunner", "生成类别文件: {}").format(classes_path), flush=True)
    except Exception:
        pass

    result = {"ok": True, "metrics_csv": metrics_path}
    best = os.path.join(ts_dir, "weights", "best.pt")
    if os.path.exists(best):
        result["model_path"] = best
    if os.path.exists(metrics_path):
        try:
            result.update(best_map50_from_csv(metrics_path))
        except Exception:
            pass
    with open(os.path.join(ts_dir, "result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
    print("[train] RESULT {}".format(json.dumps(result, ensure_ascii=False)),
          flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
