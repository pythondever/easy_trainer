# -*- coding: utf-8 -*-
"""RF-DETR 训练执行脚本（由 UI 以子进程方式启动）。

用法: python -m app.train.train_runner <config.json>
config 字段见 dialogs.py _build_train_config。
"""

import json
import math
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
except ImportError:
    torch = None

from pytorch_lightning.callbacks import Callback
import rfdetr.training as T
from rfdetr.training.callbacks import coco_eval as _ce
from rfdetr import (RFDETRNano, RFDETRSmall, RFDETRMedium, RFDETRLarge,
                    RFDETRSegNano, RFDETRSegSmall, RFDETRSegMedium,
                    RFDETRSegLarge)

from app.train.data_prep import (copy_datasets, merge_split,
                                 write_data_yaml, clean_split)


def _make_model(architecture, task="detect"):
    if task == "segment":
        variants = {
            "nano": RFDETRSegNano, "small": RFDETRSegSmall,
            "medium": RFDETRSegMedium, "large": RFDETRSegLarge,
        }
    else:
        variants = {
            "nano": RFDETRNano, "small": RFDETRSmall,
            "medium": RFDETRMedium, "large": RFDETRLarge,
        }
    cls = variants.get(architecture, variants["nano"])
    return cls()


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    out_root = cfg["out_root"]
    project = cfg["project"]
    ts_dir = cfg["timestamp_dir"]
    os.makedirs(out_root, exist_ok=True)
    os.makedirs(ts_dir, exist_ok=True)
    print("[train] 输出路径: {}".format(out_root), flush=True)
    print("[train] 本次训练输出目录(时间戳): {}".format(ts_dir), flush=True)
    shutil.copy2(cfg_path, os.path.join(ts_dir, "config.json"))
    print("[train] 训练配置文件已保存 → {}".format(
        os.path.join(ts_dir, "config.json")), flush=True)

    datasets = cfg["datasets"]
    labels, _ = copy_datasets(out_root, project, datasets)
    if not labels:
        raise RuntimeError("未从数据集中解析到任何标签类别，请检查标签文件")
    clean_split(out_root)
    merge_split(out_root, [d for d in datasets if d["split"] == "train"])
    merge_split(out_root, [d for d in datasets if d["split"] == "val"])
    write_data_yaml(out_root, labels)
    shutil.rmtree(os.path.join(out_root, project), ignore_errors=True)
    print("[train] 数据准备完成: {} 个类别, 输出目录 {}".format(
        len(labels), out_root), flush=True)

    # 2) 训练:
    task = cfg.get("task", "detect")
    model = _make_model(cfg.get("architecture", "nano"), task)
    device = cfg.get("device", "cpu")
    if device.startswith("cuda"):
        device = "cuda" if (torch is not None and torch.cuda.is_available()) else "cpu"
    resolution = int(cfg.get("img_size", 640))
    if task == "segment":
        block = model.model_config.patch_size * model.model_config.num_windows
        if resolution % block != 0:
            resolution = resolution // block * block
            print("[train] 分割模型 resolution 已自动取整: {} → {} (block={})".format(
                cfg.get("img_size", 640), resolution, block), flush=True)
    print("[train] 使用模型 {} device={} epochs={} batch={} resolution={}".format(
        cfg.get("architecture", "nano"), device, cfg["epochs"],
        cfg["batch_size"], resolution), flush=True)

    def _patch_training_hooks():
        class _FlushCsv(Callback):
            def on_train_epoch_end(self, trainer, pl_module):
                for lg in trainer.loggers:
                    if lg.__class__.__name__ == "CSVLogger":
                        try:
                            lg.save()
                        except Exception:
                            pass

        _orig_build_rows = _ce.COCOEvalCallback._build_per_class_rows

        def _patched_build_rows(self, metrics, pfx, split, pl_module,
                                ar_by_cid, f1_by_cid, metric_prefix=""):
            rows = _orig_build_rows(self, metrics, pfx, split, pl_module,
                                    ar_by_cid, f1_by_cid, metric_prefix)
            if not self._log_per_class_metrics:
                return rows
            base = "{}/{}".format(split, metric_prefix)
            for row in rows:
                name = row["name"]
                for key, col in (("ar", "AR"), ("f1", "F1"),
                                 ("precision", "Precision"), ("recall", "Recall")):
                    v = row.get(key)
                    if v is None:
                        continue
                    try:
                        if math.isnan(float(v)):
                            continue
                    except (TypeError, ValueError):
                        pass
                    pl_module.log("{}{}/{}".format(base, col, name), v)
            return rows

        _ce.COCOEvalCallback._build_per_class_rows = _patched_build_rows

        _orig = T.build_trainer

        def _patched(config, model_config, **kwargs):
            trainer = _orig(config, model_config, **kwargs)
            trainer.callbacks.extend([_FlushCsv()])
            return trainer

        T.build_trainer = _patched

    _patch_training_hooks()
    model.train(
        dataset_dir=out_root,
        dataset_file="yolo",
        output_dir=ts_dir,
        epochs=cfg["epochs"],
        batch_size=cfg["batch_size"],
        grad_accum_steps=cfg.get("grad_accum", 4),
        num_workers=cfg.get("num_workers", 8),
        lr=cfg["lr"],
        optimizer=cfg.get("optimizer", "adamw"),
        device=device,
        resolution=resolution,
        use_ema=cfg.get("use_ema", True),
        checkpoint_interval=cfg.get("checkpoint_interval", 10),
        # 早停：UI 填 0 禁用，>0 启用且值为 patience
        early_stopping=cfg.get("early_stop", 0) > 0,
        early_stopping_patience=max(cfg.get("early_stop", 0), 1),
        log_per_class_metrics=True,
    )
    print("[train] 训练完成", flush=True)

    # 3) 结果汇总: best ckpt + metrics.csv 末行指标
    # 在模型目录生成 classes.txt: 每行 "id 类别名"(交付他人使用时显式对照)
    classes_path = os.path.join(ts_dir, "classes.txt")
    try:
        with open(classes_path, "w", encoding="utf-8") as f:
            for i, lb in enumerate(labels):
                f.write("{} {}\n".format(i, lb))
        print("[train] 生成类别文件: {}".format(classes_path), flush=True)
    except Exception:
        pass
    result = {"ok": True, "metrics_csv": os.path.join(ts_dir, "metrics.csv")}
    best = os.path.join(ts_dir, "checkpoint_best_ema.pth")
    if not os.path.exists(best):
        best = os.path.join(ts_dir, "checkpoint_best_regular.pth")
    if os.path.exists(best):
        result["model_path"] = best
    csv_path = result["metrics_csv"]
    if os.path.exists(csv_path):
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                lines = [l for l in f.read().splitlines() if l.strip()]
            if len(lines) > 1:
                header = lines[0].split(",")
                row = lines[-1].split(",")
                d = dict(zip(header, row))
                for k in ("map50", "map50_95", "map", "map50-95"):
                    if k in d:
                        try:
                            result["map50"] = round(float(d[k]), 3)
                        except ValueError:
                            pass
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
