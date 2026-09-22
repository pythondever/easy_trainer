# -*- coding: utf-8 -*-
"""异常检测(AD)训练执行脚本(由 UI 以子进程方式启动).

用法: main(), 由 train_worker 以 -c 导入后调用(打包后是 pyd, 不能 python -m 启动)
config 字段见 dialogs.py make_train_config:
  task=ad, architecture=<算法代号>, epochs, batch_size,
  num_workers, img_size, device, out_root, project, timestamp_dir,
  datasets[{split, image_path, image_paths, label_fmt, ...}]

输出协议(TrainWorker 解析):
  - 每轮: [train] EPOCH N/M
          [train] METRICS {"epochs": [...], "series": {...}}
  - 结束: [train] RESULT {"ok", "accuracy", "auroc", "threshold",
                          "model_path", "normal_class", ...}
  - 落盘: ts_dir/ad_model.pt + result.json + metrics.json

与检测/分割/分类的差别:
  * 真值不像标注框那样存在标签目录里, 而是按"子文件夹名"现推 ——
    导入侧(import_task.py 的 cls 分支)也是这个口径.
  * 指标不用 anomalib 的 Evaluator: 它要求验证集里每张图都带 mask,
    FastFlow 这类训练期不产出 anomaly_map 的算法会在验证回路里直接抛错.
    这里改成训练只喂建库集, 训练完自己逐图打分再算指标, 顺带把逐图分数
    留给测试报告.
  * 交付精度是图像级 AUROC(阈值由验证集上的最优 F1 定), 不是 mAP@50.
"""

import json
import os
import shutil
import sys
import time
import traceback

_WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
for _p in (_WORKSPACE, os.path.join(_WORKSPACE, "app")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from PySide6.QtCore import QCoreApplication as QC

try:
    import lightning.pytorch as pl
    import torch
    from anomalib.data import Folder
    from anomalib.engine import Engine
except Exception as e:
    print("[train] " + QC.translate(
        "AdTrainRunner", "缺少训练依赖: {}").format(e), flush=True)
    sys.exit(1)

from app.core import i18n
from app.core.constants import IMAGE_EXTS
from app.train import ad_common as adc

MODEL_FILE = adc.MODEL_FILE


def _tr(text):
    return QC.translate("AdTrainRunner", text)


class _EpochProbe(pl.Callback):
    """把 anomalib 的轮次进度转成 easy_trainer 的输出协议.

    指标只取 train_loss: anomalib 的 AUROC/F1Score 由它自己的 Evaluator
    回调产出, 而 Evaluator 排在自定义回调之后, 这里读 callback_metrics
    拿不到本轮的值. 最终精度在训练结束后逐图打分另算, 更准也更有用.
    """

    def __init__(self, epochs, state):
        super().__init__()
        self.epochs = epochs
        self.state = state          # {"series": {...}, "ts_dir": ...}
        self.done = 0

    def on_train_epoch_start(self, trainer, pl_module):
        print("[train] EPOCH {}/{}".format(trainer.current_epoch + 1,
                                           self.epochs), flush=True)

    def on_train_epoch_end(self, trainer, pl_module):
        if self.epochs <= 1:
            return
        cm = getattr(trainer, "callback_metrics", None) or {}
        v = cm.get("train_loss_epoch", cm.get("train_loss"))
        if v is None:
            return
        try:
            loss = round(float(v), 6)
        except (TypeError, ValueError):
            return
        series = self.state["series"]
        series.setdefault("train_loss", []).append(loss)
        self.done += 1
        payload = {"epochs": list(range(1, self.done + 1)),
                   "series": {"train_loss": list(series["train_loss"])}}
        print("[train] METRICS {}".format(json.dumps(
            payload, ensure_ascii=False)), flush=True)
        try:
            with open(os.path.join(self.state["ts_dir"], "metrics.json"), "w",
                      encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False)
        except OSError:
            pass


def _build_engine(root, epochs, device, probe):
    """root 要传纯 ASCII 的目录(见 ascii_stage_dir)."""
    use_cuda = str(device).lower().startswith("cuda") and torch.cuda.is_available()
    try:
        import anomalib
        print("[train] " + _tr("anomalib {} / torch {}").format(
            getattr(anomalib, "__version__", "?"), torch.__version__),
            flush=True)
    except Exception:
        pass
    return Engine(
        max_epochs=epochs,
        accelerator="gpu" if use_cuda else "cpu",
        devices=1,
        default_root_dir=os.path.join(root, "lightning"),
        logger=False,
        enable_progress_bar=False,
        enable_model_summary=False,
        # barebones 是关掉 anomalib 自动注入 ModelCheckpoint 的开关:
        # 它每轮存一个 wide_resnet50_2 的 ckpt(300MB 起), 而模型由本脚本自己存;
        # 光设 enable_checkpointing=False 会与那个回调冲突直接报错
        barebones=True,
        enable_checkpointing=False,
        callbacks=[probe],
    )


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    i18n.apply_cli(cfg.get("language", ""))

    out_root = cfg["out_root"]
    ts_dir = cfg["timestamp_dir"]
    os.makedirs(out_root, exist_ok=True)
    os.makedirs(ts_dir, exist_ok=True)
    shutil.copy2(cfg_path, os.path.join(ts_dir, "config.json"))
    print("[train] " + _tr("输出路径: {}").format(out_root), flush=True)
    print("[train] " + _tr("本次训练输出目录(时间戳): {}").format(ts_dir),
          flush=True)

    code = cfg.get("architecture") or "patchcore"
    display = adc.model_display(code)
    # 建库型算法没有"训练"这一步, 轮次固定 1, 用户填多少都不影响
    epochs = int(cfg.get("epochs", 1) or 1)
    if not adc.is_epoch_model(code):
        epochs = 1
    batch_size = max(1, int(cfg.get("batch_size", 16) or 16))
    num_workers = max(0, int(cfg.get("num_workers", 4) or 0))
    img_size = int(cfg.get("img_size", 0) or 0)
    device = cfg.get("device", "cpu")
    print("[train] " + _tr(
        "异常检测: 算法={} 骨干={} 轮次={} 批次={} 图像尺寸={} device={}").format(
            display, adc.AD_BACKBONE, epochs, batch_size,
            img_size or "原尺寸", device), flush=True)

    # 1) 铺数据: 展开成 anomalib Folder 要的 train/normal + test/normal + test/c1...
    # 铺到 ASCII 暂存目录而不是输出目录: anomalib 的路径校验不放行中文, 而用户
    # 的输出路径/项目名里带中文太常见了. 用时间戳目录名避免并发训练互相覆盖
    ad_root = os.path.join(adc.ascii_stage_dir(out_root),
                           "ad_" + os.path.basename(ts_dir))
    layout, normal_name = adc.arrange(ad_root, cfg.get("datasets", []))
    dir_to_class = layout["dir_to_class"]
    print("[train] " + _tr(
        "数据准备: 建库集 {} 张({}), 测试集 正常 {} 张 / 异常 {} 张").format(
            layout["train"], normal_name, layout["test_normal"],
            sum(layout["abnormal"].values())), flush=True)
    if layout["abnormal"]:
        print("[train] " + _tr("  异常类别: {}").format(
            ", ".join("{}×{}".format(k or _tr("(散图)"), v)
                      for k, v in sorted(layout["abnormal"].items()))),
            flush=True)
    if layout["ignored"]:
        print("[train] " + _tr(
            "  注意: 建库集里另有 {} 张非正常图, 未参与建库").format(
                layout["ignored"]), flush=True)
    if layout["train"] == 0:
        raise RuntimeError(_tr("建库集里没有图像, 请检查数据集"))
    if layout["test_normal"] == 0 and not layout["abnormal"]:
        raise RuntimeError(_tr("测试集里没有图像, 请检查数据集"))

    test_root = os.path.join(ad_root, "test")
    abn_dirs = [os.path.join(test_root, d)
                for d in adc.abnormal_dirs(test_root)]
    data = Folder(
        name="ad",
        root=ad_root,
        normal_dir=os.path.join("train", adc.DIR_NORMAL),
        abnormal_dir=abn_dirs,     # 必须逐个列全, 传父目录会把正常类也当异常
        normal_test_dir=os.path.join("test", adc.DIR_NORMAL),
        extensions=IMAGE_EXTS,
        train_batch_size=batch_size,
        eval_batch_size=batch_size,
        num_workers=num_workers,
        test_split_mode="from_dir",
        val_split_mode="same_as_test",
    )
    data.setup()
    print("[train] " + _tr("数据集: 建库集 {} 张").format(
        len(data.train_data)), flush=True)

    # 2) 模型 + 训练
    t0 = time.time()
    # 铺数据之后、建库之前固定种子: 建库型算法的 coreset 是随机挑的, 不固定的话
    # 同一份数据每次重训都会得到一个不一样的记忆库(阈值跟着变)
    adc.seed_everything()
    model, cls_name, kwargs = adc.build_model(code, img_size, device)
    print("[train] " + _tr("模型构建完成({:.1f}s): {}").format(
        time.time() - t0, cls_name), flush=True)
    state = {"series": {}, "ts_dir": ts_dir}
    probe = _EpochProbe(epochs, state)
    engine = _build_engine(ad_root, epochs, device, probe)
    t1 = time.time()
    # 只喂建库集: 不建验证回路, 也就不会触发 anomalib Evaluator 的 mask 校验
    engine.fit(model=model, train_dataloaders=data.train_dataloader())
    fit_secs = time.time() - t1
    print("[train] " + _tr("建库/训练完成({:.1f}s)").format(fit_secs),
          flush=True)
    # anomalib 会在 default_root_dir 下建一层版本目录, 里面只有它自己的
    # 版本指针; 模型和指标由本脚本按 easy_trainer 的约定落盘, 不留这层
    shutil.rmtree(os.path.join(ad_root, "lightning"), ignore_errors=True)

    # 3) 逐图打分 + 自算指标
    t2 = time.time()
    scored = []
    try:
        raw = adc.predict_scores(engine, model, test_root, img_size,
                                 on_batch=lambda n: print(
                                     "[train] " + _tr("  评估中: {} 张").format(n),
                                     flush=True))
        for path, score in raw:
            # 铺出来的目录名是 normal / c1, 映回用户的原始类名再算指标
            cls = dir_to_class.get(adc.truth_of_path(path, test_root))
            if cls is not None:
                scored.append((cls, score))
    except Exception:
        print("[train] " + _tr("评估阶段失败, 只交付模型: {}").format(
            traceback.format_exc().splitlines()[-1]), flush=True)
    metrics = adc.evaluate(scored, normal_name)
    if metrics["accuracy"] is None:
        print("[train] " + _tr("评估完成({:.1f}s): {} 张").format(
            time.time() - t2, metrics["total"]), flush=True)
        print("[train] " + _tr(
            "  测试集里只有一类样本, 定不出判定阈值(没有真值反差), "
            "AUROC 和准确率都算不了; 补一些异常样本重新训练才有交付阈值"),
            flush=True)
    else:
        print("[train] " + _tr("评估完成({:.1f}s): {} 张, 准确率 {:.4f}").format(
            time.time() - t2, metrics["total"], metrics["accuracy"]), flush=True)
        if metrics["auroc"] is not None:
            print("[train] " + _tr(
                "  image AUROC = {:.4f}  阈值 = {:.6f}(本批最优 F1 处)").format(
                    metrics["auroc"], metrics["threshold"]), flush=True)
            print("[train] " + _tr("  漏检 {} 张(不良判成良品), 误检 {} 张").format(
                metrics["FN"], metrics["FP"]), flush=True)
        else:
            print("[train] " + _tr("  AUROC 无法计算"), flush=True)

    # 4) 落盘: 模型 + result.json + metrics.json
    model_path = os.path.join(ts_dir, MODEL_FILE)
    torch.save({
        "state_dict": model.state_dict(),
        "ad_model": code,
        "cls_name": cls_name,
        "kwargs": kwargs,
        "img_size": img_size,
        "normal_class": normal_name,
        "threshold": metrics["threshold"],
    }, model_path)
    print("[train] " + _tr("模型已保存: {} ({:.0f} MB)").format(
        model_path, os.path.getsize(model_path) / 1024 ** 2), flush=True)

    n_ep = max(probe.done, 1)
    pad = [None] * (n_ep - 1)
    series = dict(state["series"])
    # 精度只有一个(评估是训练之后一次算完的), 补 None 占位对齐前 n_ep-1 轮
    series["accuracy"] = pad + [metrics["accuracy"]]
    if metrics["auroc"] is not None:
        series["auroc"] = pad + [metrics["auroc"]]
    per_class = {}
    for name, st in metrics["per_class"].items():
        per_class[name] = dict(st)
        per_class[name]["accuracy"] = pad + [st["accuracy"]]
    payload = {"epochs": list(range(1, n_ep + 1)), "series": series,
               "per_class": per_class}

    result = {
        "ok": True,
        "task": "ad",
        "accuracy": metrics["accuracy"],
        "auroc": metrics["auroc"],
        "threshold": metrics["threshold"],
        "model_path": model_path,
        "normal_class": normal_name,
        "ad_model": code,
        "total": metrics["total"],
        "num_classes": len(per_class),
        "fit_seconds": round(fit_secs, 1),
    }
    with open(os.path.join(ts_dir, "result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
    with open(os.path.join(ts_dir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    # 铺出去的是一份完整副本, 数据集大时白占一倍磁盘; 交付物只有模型和指标.
    # 放在 RESULT 之后: 清理失败不该影响训练结果的交付
    print("[train] RESULT {}".format(json.dumps(result, ensure_ascii=False)),
          flush=True)
    shutil.rmtree(ad_root, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
