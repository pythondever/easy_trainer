# -*- coding: utf-8 -*-
"""异常检测(AD)测试执行脚本(由 UI 以子进程方式启动).

用法: main(), 由 test_worker 以 -c 导入后调用(打包后是 pyd, 不能 python -m 启动)
config: model_path(ad_model.pt), items[{image_path,...}], device, task="ad"
输出:
  - [test] PROGRESS N/M
  - [test] RESULT {"ok", "task":"ad", "total", "accuracy", "auroc",
                   "threshold", "normal_class", "per_class"}

真值按"子文件夹名"现推(与导入侧一致): 哪个类是良品由算法认, 认不出就报错 ——
把良品当不良品、或反过来, 都会让评估数字彻底反过来, 宁可拦住.

用户的原始目录不能直接喂给 anomalib: 它的路径校验只放行 ASCII, 目录叫"划痕"
就当场 ValueError. 所以这里把选中的目录铺一份到 ASCII 暂存区再打分, 目录名
经 dir_to_class 映回原始类名, 指标和明细里出现的仍是用户认得的名字.
"""

import csv
import json
import os
import shutil
import sys
import tempfile
import traceback

_WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
for _p in (_WORKSPACE, os.path.join(_WORKSPACE, "app")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from PySide6.QtCore import QCoreApplication as QC

from app.core import i18n

try:
    import torch
    from anomalib.engine import Engine
    from app.train import ad_common as adc
except Exception as e:
    print("[test] " + QC.translate(
        "AdTestRunner", "缺少测试依赖: {}").format(e), flush=True)
    sys.exit(1)


def _tr(text):
    return QC.translate("AdTestRunner", text)


def _collect_roots(items):
    """把 items 里出现过的图像根目录去重(同一份数据可能被勾了多次)."""
    roots = []
    for it in items:
        root = it.get("image_path") or ""
        if root and os.path.isdir(root) and root not in roots:
            roots.append(root)
    return roots


def main():
    cfg_path = sys.argv[1]
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    i18n.apply_cli(cfg.get("language", ""))

    model_path = cfg.get("model_path", "")
    device = cfg.get("device", "cpu")
    if str(device).lower().startswith("cuda") and torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    use_cuda = device == "cuda"
    print("[test] " + _tr("加载异常检测模型: {}").format(
        os.path.basename(model_path)), flush=True)
    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    code = ckpt.get("ad_model", "patchcore")
    cls_name = ckpt.get("cls_name", "")
    kwargs = ckpt.get("kwargs", {})
    img_size = int(ckpt.get("img_size", 0) or 0)
    normal_ckpt = ckpt.get("normal_class", "")
    threshold = float(ckpt.get("threshold", 0.0) or 0.0)
    print("[test] " + _tr("算法={} 图像尺寸={} 阈值={:.6f}").format(
        adc.model_display(code), img_size or _tr("原尺寸"), threshold),
        flush=True)

    model = adc.load_model(code, cls_name, kwargs, img_size, model_path)

    roots = _collect_roots(cfg.get("items") or [])
    if not roots:
        raise RuntimeError(_tr("没有可用的图像目录, 请检查数据集"))

    stage_root = os.path.join(
        adc.ascii_stage_dir(cfg.get("report_dir") or tempfile.gettempdir()),
        "ad_pred_" + str(os.getpid()))
    try:
        # 铺一份 ASCII 副本, 顺带定出哪个类是良品(认不出会在这里报错)
        staged = adc.stage_test(stage_root, roots, normal_ckpt)
        dir_to_class = staged["dir_to_class"]
        normal = staged["normal"]
        origins = staged["origins"]
        print("[test] " + _tr("测试图片 {} 张, 良品类别: {}").format(
            staged["total"], adc.display_name(normal)), flush=True)

        engine = Engine(
            max_epochs=1,
            accelerator="gpu" if use_cuda else "cpu",
            devices=1,
            default_root_dir=os.path.join(stage_root, "lightning"),
            logger=False,
            enable_progress_bar=False,
            enable_model_summary=False,
            # 见 ad_train_runner: barebones 才挡得住 anomalib 自动注入的 ModelCheckpoint
            barebones=True,
            enable_checkpointing=False,
        )

        scored = []                   # [(原始类名, 分数, 原图路径)]
        raw = adc.predict_scores(
            engine, model, stage_root, img_size,
            on_batch=lambda n: print(
                "[test] PROGRESS {}/{}".format(n, staged["total"]), flush=True))
        for path, score in raw:
            cls = dir_to_class.get(adc.truth_of_path(path, stage_root))
            if cls is None:
                continue
            # 明细里要写用户原本的那张图, 不是暂存副本
            scored.append((cls, score, origins.get(path, path)))
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)

    if not scored:
        raise RuntimeError(_tr("没有取到任何图像, 请检查数据集"))
    print("[test] PROGRESS {}/{}".format(len(scored), len(scored)), flush=True)

    # 阈值沿用模型里训练时定好的那个: 换一批数据重挑等于拿测试集调参
    metrics = adc.evaluate([(s[0], s[1]) for s in scored], normal,
                           threshold=threshold)
    if metrics["threshold"] > 0:
        print("[test] " + _tr("沿用训练时定下的阈值 {:.6f}").format(
            metrics["threshold"]), flush=True)
    elif metrics.get("single_class"):
        print("[test] " + _tr(
            "模型里没有阈值, 本批又只有一类样本, 定不出判定阈值, 只报告分数"),
            flush=True)
    else:
        print("[test] " + _tr(
            "模型里没有阈值, 已按本批数据现挑 {:.6f}(精度会偏乐观)").format(
                metrics["threshold"]), flush=True)

    result = {
        "ok": True,
        "task": "ad",
        "total": metrics["total"],
        "accuracy": metrics["accuracy"],
        "auroc": metrics["auroc"],
        "threshold": metrics["threshold"],
        "normal_class": normal,
        # 漏检 = 不良判成良品, 误检 = 良品判成不良品; 结果面板要分开报
        "TP": metrics["TP"], "FN": metrics["FN"],
        "FP": metrics["FP"], "TN": metrics["TN"],
        "per_class": metrics["per_class"],
        "model": os.path.basename(model_path),
        "ad_model": code,
        "report_dir": cfg.get("report_dir", ""),
    }
    if metrics.get("single_class"):
        result["single_class"] = True
    detail = _write_detail(cfg, scored, metrics, normal)
    if detail:
        # 逐图明细单独放一个键: detail_path 是检测任务的"带框明细",
        # 报告模块按它画框, AD 没有框, 塞进去会让导出做成一份空报告
        result["ad_detail_path"] = detail
    if metrics["accuracy"] is None:
        print("[test] " + _tr("完成: {} 张, 没有判定阈值, 只报告分数").format(
            metrics["total"]), flush=True)
    else:
        print("[test] " + _tr(
            "完成: {} 张, 准确率 {:.4f}, 漏检 {} 张, 误检 {} 张").format(
                metrics["total"], metrics["accuracy"], metrics["FN"],
                metrics["FP"]), flush=True)
    if metrics["auroc"] is not None:
        print("[test] " + _tr("  image AUROC = {:.4f}").format(
            metrics["auroc"]), flush=True)
    print("[test] RESULT {}".format(json.dumps(result, ensure_ascii=False)),
          flush=True)


def _write_detail(cfg, scored, metrics, normal):
    """逐图结果写成 CSV(交付/复查用), 返回路径; 写不了返回空串."""
    out_dir = cfg.get("report_dir") or ""
    if not out_dir:
        return ""
    threshold = metrics["threshold"]
    # 没有阈值时不给判定, 免得把"全部判 NG"当成结论交付出去
    has_thr = threshold > 0
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "ad_detail.csv")
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            wr = csv.writer(f)
            wr.writerow([QC.translate("AdTestRunner", "图像"),
                         QC.translate("AdTestRunner", "类别"),
                         QC.translate("AdTestRunner", "真值"),
                         QC.translate("AdTestRunner", "判定"),
                         QC.translate("AdTestRunner", "分数"),
                         QC.translate("AdTestRunner", "阈值"),
                         QC.translate("AdTestRunner", "是否正确")])
            for cls, score, img in scored:
                label = 0 if cls == normal else 1
                if not has_thr:
                    wr.writerow([img, adc.display_name(cls),
                                 "NG" if label else "OK", "",
                                 "{:.6f}".format(score), "", ""])
                    continue
                pred = 1 if score >= threshold else 0
                wr.writerow([
                    img, adc.display_name(cls),
                    "NG" if label else "OK",
                    "NG" if pred else "OK",
                    "{:.6f}".format(score),
                    "{:.6f}".format(threshold),
                    QC.translate("AdTestRunner", "是") if pred == label
                    else QC.translate("AdTestRunner", "否"),
                ])
        print("[test] " + _tr("逐图明细: {}").format(path), flush=True)
        return path
    except OSError:
        return ""


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
