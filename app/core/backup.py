# -*- coding: utf-8 -*-
"""项目备份/恢复核心逻辑(无 Qt 依赖, 可单测).

项目级备份: lmdb 的 key 是少数几个全局单 key 存全库大 JSON 列表
(project_info_list/train_history/model_history/train_queue/paste_regions),
没有"每项目一个 key"的结构, 所以项目级备份只能做记录级过滤 + 合并:
备份时从各全局列表里捞出该项目子集, 恢复时按 id 去重合并写回,
全程不碰其他项目的记录.

恢复时若库内已有同名项目, 仅空项目可接收(用户误建的同名项目);
非空则带内容清单报错, 不写库.

恢复目标项目(target_project): 右键恢复时传当前项目名, 包内全部记录
(数据集/训练记录/模型记录/队列/粘贴模板)改归属到它, 内容进当前项目,
不按包内项目名新建; 为空时按包内项目名恢复.

备份包是 zip(.etbak): manifest.json + records.json(记录子集)
+ data/(图像与标签) + models/<训练id>/(权重等产物) + metrics/<id>.json.
"""

import json
import os
import shutil
import zipfile
from datetime import datetime

from app.core.constants import IMAGE_EXTS
from app.core.db import get_path_pairs

FORMAT_VERSION = 1
MANIFEST_NAME = "manifest.json"
RECORDS_NAME = "records.json"
DATA_DIR = "data"
MODELS_DIR = "models"
METRICS_DIR = "metrics"

# 队列里唯一"未开始"状态(见 queue_mixin.DONE_STATUS, 这里不 import mixin)
QUEUE_WAITING = "waiting"


class RestoreError(Exception):
    """恢复包不可用: 版本不兼容 / 项目名冲突 / 包损坏.

    items: 冲突时库内该项目的已有内容清单(弹窗列表用).
    """
    def __init__(self, message, items=None):
        super().__init__(message)
        self.items = list(items or [])


def _safe_members(zf, prefix):
    """包内 prefix/ 下的成员名, 拒掉越界路径(zip slip)."""
    out = []
    base = os.path.abspath(prefix)
    for name in zf.namelist():
        if not name.startswith(prefix + "/"):
            continue
        target = os.path.abspath(os.path.join(prefix, os.path.normpath(name)))
        if not (target == base or target.startswith(base + os.sep)):
            raise RestoreError("备份包含越界路径: {}".format(name))
        out.append(name)
    return out


def _item_touches_project(item, project):
    """队列项的 params.datasets 是否引用该项目(引用才随项目备份)."""
    for ds in (item.get("params") or {}).get("datasets") or []:
        if isinstance(ds, dict) and ds.get("project") == project:
            return True
    return False


def project_content(db, project):
    """该项目已有的内容清单: 判"空项目"与冲突弹窗列表共用."""
    items = []
    for i in db.get_project_info():
        if i.get("project_name") == project:
            items.append("数据集 {}({} 张)".format(
                i.get("dataset_name", ""), i.get("total", 0) or 0))
    for r in db.get_train_records():
        if r.get("project") == project:
            items.append("训练记录 {}".format(r.get("id", "")))
    for r in db.get_model_records():
        if r.get("project") == project:
            items.append("模型记录 {}".format(r.get("id", "")))
    for it in db.get_train_queue():
        if _item_touches_project(it, project):
            items.append("训练队列 {}".format(it.get("qid", "")))
    prefix = project + "/"
    for k in db.get_paste_region_templates():
        if k.startswith(prefix):
            items.append("粘贴模板 {}".format(k))
    return items


def _ensure_restorable(db, project):
    """同名项目仅空项目可恢复; 非空抛错并带上内容清单(弹窗用).

    文案点名"备份包中的项目": 恢复入口在某个项目右键打开, 但包内项目
    名可以与右键项目不同, 不说清会被误读成右键项目本身冲突。
    """
    if project not in db.get_projects():
        return
    items = project_content(db, project)
    if items:
        raise RestoreError(
            "备份包中的项目\"{}\"在库中已存在且不为空, 无法恢复。"
            "请先删除现有项目后重试。".format(
                project), items=items)


def collect_payload(db, project):
    """从 db 各全局 key 过滤出 project 的记录子集(可 JSON 序列化)."""
    infos = [i for i in db.get_project_info()
             if i.get("project_name") == project]
    trains = [r for r in db.get_train_records() if r.get("project") == project]
    models = [r for r in db.get_model_records() if r.get("project") == project]
    queue = [it for it in db.get_train_queue()
             if it.get("status") == QUEUE_WAITING
             and _item_touches_project(it, project)]
    prefix = project + "/"
    regions = {k: v for k, v in db.get_paste_region_templates().items()
               if k.startswith(prefix)}
    return {
        "project_info": infos,
        "train_history": trains,
        "model_history": models,
        "queue": queue,
        "paste_regions": regions,
    }


def build_manifest(project, payload):
    """包的索引: 版本/时间/项目名/数据集清单/记录数(恢复前给用户看摘要)."""
    datasets = [{
        "dataset_name": i.get("dataset_name", ""),
        "dataset_type": i.get("dataset_type", ""),
        "label_fmt": i.get("label_fmt", ""),
        "total": i.get("total", 0) or 0,
        "labeled": i.get("labeled", 0) or 0,
    } for i in payload["project_info"]]
    return {
        "format_version": FORMAT_VERSION,
        "app": "easy_trainer",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "project": project,
        "datasets": datasets,
        "train_records": len(payload["train_history"]),
        "queue_items": len(payload["queue"]),
    }


def _dataset_files(info):
    """(数据集名, [(源路径, 包内相对路径), ...]): 图像保留子目录结构,
    标签目录整目录带上(不挑格式, yolo txt 与原样 json 都要)."""
    ds = info.get("dataset_name", "")
    files = []
    for img_dir, lbl_dir in get_path_pairs(info):
        if img_dir and os.path.isdir(img_dir):
            for root, _dirs, names in os.walk(img_dir):
                for name in names:
                    if not name.lower().endswith(IMAGE_EXTS):
                        continue
                    src = os.path.join(root, name)
                    rel = os.path.relpath(src, img_dir)
                    files.append((src, "{}/{}/images/{}".format(
                        DATA_DIR, ds, rel.replace(os.sep, "/"))))
        if lbl_dir and os.path.isdir(lbl_dir):
            for root, _dirs, names in os.walk(lbl_dir):
                for name in names:
                    src = os.path.join(root, name)
                    rel = os.path.relpath(src, lbl_dir)
                    files.append((src, "{}/{}/labels/{}".format(
                        DATA_DIR, ds, rel.replace(os.sep, "/"))))
    return ds, files


def _count_backup_units(db, project, include_data, include_models):
    """打包总步数(进度条分母): 每条训练记录算 2 步(产物+指标),
    数据按文件数算, 记录写入算 1 步."""
    payload = collect_payload(db, project)
    total = 1 + len(payload["project_info"])
    if include_models:
        for rec in payload["train_history"]:
            total += 2
    if include_data:
        for info in payload["project_info"]:
            total += len(_dataset_files(info)[1])
    return total, payload


def write_backup(db, project, zip_path, include_data=True,
                 include_models=True, progress=None):
    """把 project 打成 zip. progress(done, total, text) 可空.
    返回 manifest dict."""
    total, payload = _count_backup_units(
        db, project, include_data, include_models)
    manifest = build_manifest(project, payload)
    done = 0

    def step(text):
        nonlocal done
        done += 1
        if progress:
            progress(done, total, text)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MANIFEST_NAME,
                    json.dumps(manifest, ensure_ascii=False, indent=2))
        zf.writestr(RECORDS_NAME,
                    json.dumps(payload, ensure_ascii=False, indent=2))
        step("写入项目记录")
        if include_models:
            metrics_dir = db.metrics_dir
            for rec in payload["train_history"]:
                rid = rec.get("id", "")
                out_dir = rec.get("output_path") or ""
                if rid and out_dir and os.path.isdir(out_dir):
                    for root, _dirs, names in os.walk(out_dir):
                        for name in names:
                            src = os.path.join(root, name)
                            rel = os.path.relpath(src, out_dir)
                            zf.write(src, "{}/{}/{}".format(
                                MODELS_DIR, rid, rel.replace(os.sep, "/")))
                step("打包训练产物 {}".format(rid))
                mfile = rec.get("metrics_file") or ""
                src = os.path.join(metrics_dir, mfile) if mfile else ""
                if mfile and os.path.isfile(src):
                    zf.write(src, "{}/{}.json".format(METRICS_DIR, rid))
                step("打包指标 {}".format(rid))
        if include_data:
            for info in payload["project_info"]:
                ds, files = _dataset_files(info)
                for src, arc in files:
                    zf.write(src, arc)
                step("打包数据集 {}".format(ds))
    return manifest


def read_backup(zip_path):
    """读包: (manifest, payload dict). 打不开/缺文件/版本过高都抛 RestoreError."""
    if not os.path.isfile(zip_path):
        raise RestoreError("文件不存在: {}".format(zip_path))
    try:
        with zipfile.ZipFile(zip_path) as zf:
            names = set(zf.namelist())
            if MANIFEST_NAME not in names or RECORDS_NAME not in names:
                raise RestoreError("不是有效的备份包(缺少 manifest/records)")
            manifest = json.loads(zf.read(MANIFEST_NAME).decode("utf-8"))
            payload = json.loads(zf.read(RECORDS_NAME).decode("utf-8"))
    except zipfile.BadZipFile:
        raise RestoreError("不是有效的备份包(文件已损坏)")
    if int(manifest.get("format_version") or 0) > FORMAT_VERSION:
        raise RestoreError("备份包版本过新(格式 {}), 请升级软件后重试".format(
            manifest.get("format_version")))
    project = manifest.get("project") or ""
    if not project:
        raise RestoreError("备份包缺少项目名")
    return manifest, payload


def check_restorable(db, zip_path, target_project=None):
    """恢复前校验: 目标项目(默认包内项目)仅空项目可恢复."""
    manifest, _payload = read_backup(zip_path)
    target = (target_project or "").strip() or manifest["project"]
    _ensure_restorable(db, target)
    return manifest


def _remap_info(info, data_root, project):
    """info 归属改写到 project, 路径重写到 data_root/<数据集名>/{images,labels}.
    保持按轮次等长配对(空串占位保留), 顺手去掉旧单值字段."""
    new = dict(info)
    new["project_name"] = project
    if not data_root:
        return new
    ds = info.get("dataset_name", "")
    imgs, lbls = [], []
    for img, lbl in get_path_pairs(info):
        imgs.append(os.path.join(data_root, ds, "images") if img else "")
        lbls.append(os.path.join(data_root, ds, "labels") if lbl else "")
    new["image_paths"] = imgs
    new["label_paths"] = lbls
    new.pop("image_path", None)
    new.pop("label_path", None)
    return new


def _remap_record(record, models_root, project):
    """训练/模型记录归属改写到 project, 产物路径重写到 models_root/<id>/."""
    new = dict(record)
    new["project"] = project
    if not models_root:
        return new
    rid = new.get("id", "")
    if new.get("output_path"):
        new["output_path"] = os.path.join(models_root, rid)
    if new.get("model_path"):
        new["model_path"] = os.path.join(
            models_root, rid, os.path.basename(new["model_path"]))
    return new


def restore_backup(db, zip_path, dest_dir, include_data=True,
                   target_project=None, progress=None):
    """恢复到 dest_dir.

    target_project 非空: 包内记录全部改归属到该项目(右键恢复, 内容进
    当前项目, 不按包内项目名新建); 为空则按包内项目名恢复. 目标项目
    仅空项目可接收, 非空抛 RestoreError(调用前可先 check_restorable).
    返回 manifest."""
    manifest, payload = read_backup(zip_path)
    project = manifest["project"]
    target = (target_project or "").strip() or project
    _ensure_restorable(db, target)
    os.makedirs(dest_dir, exist_ok=True)
    models_root = os.path.join(dest_dir, MODELS_DIR)
    data_root = os.path.join(dest_dir, DATA_DIR) if include_data else ""
    done = 0
    total = (len(payload["project_info"]) + len(payload["train_history"])
             + len(payload["model_history"]) + len(payload["queue"]) + 2)

    def step(text):
        nonlocal done
        done += 1
        if progress:
            progress(done, total, text)

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if include_data:
            members = _safe_members(zf, DATA_DIR)
            if members:
                zf.extractall(dest_dir, members)
            step("解包数据集数据")
        model_members = _safe_members(zf, MODELS_DIR)
        if model_members:
            zf.extractall(dest_dir, model_members)
        metric_members = _safe_members(zf, METRICS_DIR)
        if metric_members:
            zf.extractall(db.db_path, metric_members)
        step("解包训练产物")

    # 项目与数据集记录先落库, 再重写路径(update_dataset_import 只认已在库的条目)
    # add_project 不去重, 接收空项目时不能再 add
    if target not in db.get_projects():
        db.add_project(target)
    for info in payload["project_info"]:
        db.add_project_info(_remap_info(info, data_root, target))
        step("恢复数据集 {}".format(info.get("dataset_name", "")))

    for rec in payload["train_history"]:
        db.add_train_record(_remap_record(rec, models_root, target))
        step("恢复训练记录 {}".format(rec.get("id", "")))
    for rec in payload["model_history"]:
        db.add_model_record(_remap_record(rec, models_root, target))
        step("恢复模型记录 {}".format(rec.get("id", "")))

    # 队列: 只恢复未开始项, qid 去重, order 顺延到现有队尾
    items = db.get_train_queue()
    known = {it.get("qid") for it in items}
    order = max((int(it.get("order") or 0) for it in items), default=-1)
    for it in payload["queue"]:
        if it.get("qid") in known:
            continue
        order += 1
        new = dict(it)
        new["order"] = order
        # 数据集引用改归属到 target; 别的项目的引用原样保留
        params = dict(new.get("params") or {})
        datasets = []
        for d in params.get("datasets") or []:
            d = dict(d)
            if d.get("project") == project:
                d["project"] = target
            datasets.append(d)
        if datasets:
            params["datasets"] = datasets
            new["params"] = params
        items.append(new)
    if len(items) > len(known):
        db.save_train_queue(items)
    step("恢复训练队列")

    # 粘贴模板: key 前缀换成 target, 再按 key 合并(备份条目覆盖同名 key)
    regions = db.get_paste_region_templates()
    prefix = project + "/"
    renamed = {}
    for k, v in payload["paste_regions"].items():
        nk = target + "/" + k[len(prefix):] if k.startswith(prefix) else k
        renamed[nk] = v
    regions.update(renamed)
    if renamed:
        db.save_paste_region_templates(regions)
    step("恢复粘贴区域模板")
    return manifest
