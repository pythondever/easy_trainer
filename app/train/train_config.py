# -*- coding: utf-8 -*-
"""
训练配置纯逻辑: 任务规格查询 / 配置组装 / 训练记录 / 训练前校验.

与 TrainDialog 解耦: 队列出队时没有对话框实例, 也走这里的函数.
这里只依赖 QtCore(翻译)与 core 层, 不碰 Qt Widgets, 可无头单测.
"""
import json
import os
import uuid
from datetime import datetime

from PySide6.QtCore import QCoreApplication as QC

from app.core import i18n
from app.core.constants import IMAGE_EXTS
from app.core.db import display_path, get_path_pairs
from app.core.log import write_log
from app.train import ad_common as adc
from app.train import classify_common, detect_common, segment_common
from app.train import ocr_common as occ
from app.train.data_prep import timestamp_dir
from app.widgets.status_style import task_text

# 与任务下拉的顺序一致
TASK_SPECS = (detect_common.SPEC, segment_common.SPEC, classify_common.SPEC,
              adc.SPEC, occ.SPEC)
_SPEC_BY_CODE = {spec.code: spec for spec in TASK_SPECS}
# 各任务用不上的控件并集: 切任务时要逐个恢复可用性, 得知道全集
DISABLEABLE_FIELDS = tuple(sorted(
    {name for spec in TASK_SPECS for name in spec.disabled_fields}))


def spec_for(task):
    """任务代号对应的任务规格. 字符检测的记录里是 ocr_det/ocr_rec 两条, 都归到 ocr."""
    if occ.is_ocr(task):
        return occ.SPEC
    return _SPEC_BY_CODE.get(str(task or ""), detect_common.SPEC)


def _td(text):
    """TrainDialog 上下文的翻译: 队列出队那条路没有对话框实例, 取不到 self.tr."""
    return QC.translate("TrainDialog", text)


def collect_dataset_labels(db, ds_pairs):
    """勾选数据集的标签并集(跨项目,训练启动时已知,指标界面下拉无需等验证)."""
    labels = set()
    for proj, name in ds_pairs:
        try:
            for lb in db.get_dataset_labels(proj, name):
                labels.add(str(lb))
        except Exception:
            pass
    return sorted(labels)


def best_ckpt_name(config):
    """训练期间先按这个填记录的 model_path, 跑完由 runner 的 RESULT 覆盖."""
    return spec_for(config.get("task", "")).checkpoint_name(
        config.get("family", ""))


def make_train_record(config, db, project_fallback=""):
    """
    按 config 组装训练记录(供训练界面回填); 不落库, 调用方在启动成功后写入.
    与 TrainDialog 解耦: 队列出队时没有对话框实例, 也走这个函数.
    """
    ds_pairs = [(d["project"], d["dataset_name"]) for d in config["datasets"]
                if d.get("split") == "train"]
    val_pairs = [(d["project"], d["dataset_name"]) for d in config["datasets"]
                 if d.get("split") == "val"]
    ds_names = ", ".join("{}/{}".format(p, d) for p, d in ds_pairs)
    val_names = ", ".join("{}/{}".format(p, d) for p, d in val_pairs)
    # dataset_info 包含训练集+验证集," / " 分隔两组;组内多个用逗号
    dataset_info = (ds_names + " / " + val_names) if val_names else ds_names
    first_proj = ds_pairs[0][0] if ds_pairs else project_fallback
    return {
        "id": str(uuid.uuid4()),
        "project": first_proj,
        "task": config.get("task", ""),
        "dataset": ds_names,
        "val_dataset": val_names,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": "",
        "duration": "",
        "model_size": config.get("model_size", ""),
        "family": config.get("family", ""),
        "map50": "",
        "img_size": config.get("img_size", ""),
        "model_path": display_path(os.path.join(
            config.get("timestamp_dir", ""), best_ckpt_name(config))),
        "dataset_info": dataset_info,
        "output_path": config.get("out_root", ""),
        "epochs": config.get("epochs", ""),
        "batch_size": config.get("batch_size", ""),
        "lr": config.get("lr", ""),
        "grad_accum": config.get("grad_accum", ""),
        "num_workers": config.get("num_workers", ""),
        "early_stop": config.get("early_stop", ""),
        "optimizer": config.get("optimizer", ""),
        "metrics_file": "",   # 指标外置为 metrics/<id>.json, 记录里只留文件名
        "metrics_epochs": 0,
        "labels": collect_dataset_labels(db, ds_pairs),
        "device": config.get("device", ""),
        "aug": config.get("aug", ""),
    }


def params_to_record(params):
    """队列项参数快照转成训练对话框 preset_record 的字段格式(用于"编辑"回填)."""
    def _names(pairs):
        return ", ".join("{}/{}".format(p[0], p[1]) for p in (pairs or []))
    return {
        "task": params.get("task", ""),
        "dataset": _names(params.get("train_ds")),
        "val_dataset": _names(params.get("val_ds")),
        "epochs": params.get("epochs", ""),
        "batch_size": params.get("batch_size", ""),
        "lr": params.get("lr", ""),
        "grad_accum": params.get("grad_accum", ""),
        "num_workers": params.get("num_workers", ""),
        "early_stop": params.get("early_stop", ""),
        "img_size": params.get("img_size", ""),
        "model_size": params.get("architecture", ""),
        "family": params.get("family", ""),
        "device": params.get("device", ""),
        "optimizer": params.get("optimizer", ""),
        "output_path": display_path(params.get("out_root", "")),
        "aug": params.get("aug", ""),
    }


def _has_label_beside(img_dir, fmt):
    """
    图像目录里有没有与图同名的标签文件.

    字条集把 .txt 跟图放一起, 自己标注出来的 json 也落在图旁边;
    读取侧本来就优先看图同目录, 校验跟上这一步, 免得"导入时还没标注"被当成错误.
    """
    exts = {".txt": (".txt",), ".json": (".json",)}.get(fmt, (".json", ".txt"))
    try:
        entries = os.listdir(img_dir)
    except OSError:
        return False
    stems = {os.path.splitext(fn)[0] for fn in entries
             if os.path.splitext(fn)[1].lower() in exts}
    if not stems:
        return False
    return any(os.path.splitext(fn)[0] in stems for fn in entries
               if os.path.splitext(fn)[1].lower() in IMAGE_EXTS)


def check_dataset_imported(name, info):
    """
    校验数据集已导入且路径有效(防止未导入/加载中的数据集直接训练).
    多路径导入后只认最后一个目录会误拦: 最新目录被移走时报"尚未导入",
    而早期导入目录的数据完好, 训不动. 这里按轮次遍历全部配对, 只要还有
    有效图像目录就放行, 失效目录写日志告警(数据准备层会跳过它们).
    分类数据集(fmt=="cls")标签即子文件夹名,无需单独 label_path 目录,
    所以跳过标签目录存在性检查. 标签目录没填/失效时, 再看图旁边有没有同名标签.
    """
    fmt = info.get("label_fmt", "")
    pairs = get_path_pairs(info)
    alive = [(img, lbl) for img, lbl in pairs if img and os.path.isdir(img)]
    if not alive:
        raise ValueError(QC.translate(
            "TrainDialog",
            "数据集\"{}\"尚未导入图像或路径无效, 请先导入该数据集再训练")
            .format(name))
    dead = [img for img, _lbl in pairs if img and not os.path.isdir(img)]
    if dead:
        write_log(QC.translate(
            "TrainDialog",
            "数据集\"{}\"有 {} 个导入目录已失效, 本次训练将跳过: {}").format(
                name, len(dead), "; ".join(dead)))
    if fmt == "cls":
        return
    # 标签目录没填/失效时再看图旁边: 导入时通常还没有标签(标注是后面的事),
    # 只要任一有效目录旁有同名标签文件就允许开始训练
    has_label = any(lbl and os.path.isdir(lbl) for _img, lbl in alive) or any(
        _has_label_beside(img, fmt) for img, _lbl in alive)
    if not has_label:
        raise ValueError(QC.translate(
            "TrainDialog",
            "数据集\"{}\"尚未导入标签或路径无效, 请先导入该数据集再训练")
            .format(name))


def _unique_ts_dir(out_root, ts):
    """时间戳只到秒: 队列里上一个任务秒退时下一个会撞名, 两个训练的输出会互相覆盖."""
    path = os.path.join(out_root, ts)
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
        return path
    i = 2
    while os.path.isdir("{}_{}".format(path, i)):
        i += 1
    path = "{}_{}".format(path, i)
    os.makedirs(path, exist_ok=True)
    return path


def make_train_config(db, params):
    """
    把参数快照落盘成子进程配置. 队列出队与开始训练共用同一条路径.
    timestamp_dir 只在这里算一次: 训练记录的 model_path 必须复用它,
    否则两次调用跨秒会指向一个不存在的目录.
    """
    task = params.get("task") or "detect"
    out_root = display_path((params.get("out_root") or "").strip())
    if not out_root:
        raise ValueError(QC.translate("TrainDialog", "请先选择输出路径"))
    os.makedirs(out_root, exist_ok=True)
    spec = spec_for(task)
    datasets = []
    for split, pairs in (("train", params.get("train_ds") or []),
                         ("val", params.get("val_ds") or [])):
        for pair in pairs:
            proj, name = pair[0], pair[1]
            info = db.get_dataset_import(proj, name)
            check_dataset_imported(name, info)
            fmt = info.get("label_fmt", "")
            # 入队后数据集可能被重新导入成别的格式, 出队时再校验一次
            # (队列可能挂着几个小时, 中间改了数据集这里才发现)
            problem = spec.dataset_problem(proj, name, info,
                                           task_text(task), _td)
            if problem:
                raise ValueError(problem)
            datasets.append({
                "dataset_name": name, "project": proj, "split": split,
                "image_path": info.get("image_path", ""),
                "label_path": info.get("label_path", ""),
                # 必须给原始列表(带空串占位): get_paths 会滤掉空串,
                # data_prep._paired_dirs 拿滤后的短列表按位置配对, 会把
                # "第 1 轮只导图像"错位成"第 1 轮的图吃第 2 轮的标签目录".
                # 其余消费者(候选目录/统计)走 get_paths 自己会滤, 不受影响
                "image_paths": list(info.get("image_paths") or []),
                "label_paths": list(info.get("label_paths") or []),
                "fmt": fmt,
                "label_ids": db.get_dataset_label_ids(proj, name),
            })
    if not any(d["split"] == "train" for d in datasets):
        raise ValueError(QC.translate("TrainDialog", "请至少选择一个训练集数据集"))
    if not any(d["split"] == "val" for d in datasets):
        raise ValueError(QC.translate("TrainDialog", "请至少选择一个验证集数据集"))
    ts_dir = _unique_ts_dir(out_root, timestamp_dir())
    architecture = spec.resolve_architecture(params.get("architecture"))
    config = {
        "task": task,
        "out_root": out_root,
        "project": datasets[0]["project"],
        "timestamp_dir": ts_dir,
        "architecture": architecture,
        "family": spec.resolve_family(params.get("family")),
        "model_size": params.get("architecture") or "nano",
        "device": params.get("device") or "",
        "epochs": params.get("epochs", 100),
        "batch_size": params.get("batch_size", 8),
        "num_workers": params.get("num_workers", 8),
        "optimizer": params.get("optimizer") or "adamw",
        # 早停: >0 启用(值即 patience), <=0 禁用
        "early_stop": params.get("early_stop", 20),
        "lr": params.get("lr", 1e-4),
        "img_size": params.get("img_size", 640),
        "aug": params.get("aug", ""),
        "datasets": datasets,
        "language": i18n.current(),
    }
    # 分类不传梯度累积(runner),检测/分割才传
    if spec.uses_grad_accum():
        config["grad_accum"] = params.get("grad_accum", 4)
    cfg_path = os.path.join(ts_dir, "train_config.json")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False)
    config["_cfg_path"] = cfg_path
    return config


def params_summary(params):
    """队列项的一行摘要文本(任务/网络/数据集)."""
    task = params.get("task", "")
    shown = task_text(task)
    # 带项目名:不同项目下常有同名数据集(如 test1/train, test2/train)
    names = ["{}/{}".format(p[0], p[1]) for p in (params.get("train_ds") or [])]
    ds = ", ".join(names) if names else QC.translate("TrainDialog", "未选数据集")
    return "{} · {} · {}".format(shown, params.get("architecture", ""), ds)
