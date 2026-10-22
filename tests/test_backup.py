# -*- coding: utf-8 -*-
"""项目备份/恢复: 记录级过滤 + 合并, 不动其他项目; 路径按轮次配对重写."""

import json
import os
import shutil
import tempfile
import zipfile

import pytest

from app.core.backup import (
    FORMAT_VERSION, MANIFEST_NAME, RestoreError, build_manifest,
    check_restorable, collect_payload, read_backup, restore_backup,
    write_backup)
from app.core.db import DataBase, get_path_pairs


@pytest.fixture
def db_dir():
    d = tempfile.mkdtemp(prefix="et_test_bak_")
    try:
        yield d
    finally:
        shutil.rmtree(d, ignore_errors=True)


def make_dataset(root, name, n_img=3, with_labels=True):
    """造一个图像(+labelme json)目录, 返回 (img_dir, lbl_dir)."""
    img_dir = os.path.join(root, name, "images")
    lbl_dir = os.path.join(root, name, "labels") if with_labels else ""
    os.makedirs(img_dir, exist_ok=True)
    if with_labels:
        os.makedirs(lbl_dir, exist_ok=True)
    for i in range(n_img):
        stem = "img{}".format(i)
        with open(os.path.join(img_dir, stem + ".png"), "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + bytes([i]) * 16)
        if with_labels:
            with open(os.path.join(lbl_dir, stem + ".json"), "w") as f:
                json.dump({"shapes": [], "imagePath": stem + ".png"}, f)
    return img_dir, lbl_dir


@pytest.fixture
def db(db_dir):
    return DataBase(db_dir)


@pytest.fixture
def data_root(db_dir):
    return os.path.join(db_dir, "userdata")


def import_dataset(db, project, ds_name, root, with_labels=True):
    img_dir, lbl_dir = make_dataset(root, ds_name, with_labels=with_labels)
    if project not in db.get_projects():
        db.add_project(project)
    db.add_dataset(project, ds_name)
    db.update_dataset_import(project, ds_name, img_dir, lbl_dir, ".json",
                             labeled=2, total=3)
    return img_dir, lbl_dir


class TestCollectPayload:
    def test_只捞本项目记录(self, db, data_root):
        import_dataset(db, "p1", "dsA", data_root)
        db.add_train_record({"id": "t1", "project": "p1", "model_path": "/m1/best.pt",
                             "output_path": "/m1", "metrics_file": ""})
        db.add_train_record({"id": "t2", "project": "p2", "model_path": "/m2/best.pt"})
        db.add_model_record({"id": "t1", "project": "p1"})
        db.save_train_queue([
            {"qid": "q1", "order": 0, "status": "waiting",
             "params": {"datasets": [{"project": "p1", "dataset_name": "dsA"}]}},
            {"qid": "q2", "order": 1, "status": "done",
             "params": {"datasets": [{"project": "p1", "dataset_name": "dsA"}]}},
            {"qid": "q3", "order": 2, "status": "waiting",
             "params": {"datasets": [{"project": "p2", "dataset_name": "dsB"}]}},
        ])
        db.save_paste_region_templates({
            "p1/dsA": {"tpl": {"ref_size": [10, 10], "regions": []}},
            "p2/dsB": {"tpl": {"ref_size": [10, 10], "regions": []}},
        })
        p = collect_payload(db, "p1")
        assert [i["dataset_name"] for i in p["project_info"]] == ["dsA"]
        assert [r["id"] for r in p["train_history"]] == ["t1"]
        assert [r["id"] for r in p["model_history"]] == ["t1"]
        assert [it["qid"] for it in p["queue"]] == ["q1"]   # done 与其他项目的不要
        assert list(p["paste_regions"]) == ["p1/dsA"]

    def test_manifest_清单(self, db, data_root):
        import_dataset(db, "p1", "dsA", data_root)
        m = build_manifest("p1", collect_payload(db, "p1"))
        assert m["format_version"] == FORMAT_VERSION
        assert m["project"] == "p1"
        assert m["datasets"] == [{"dataset_name": "dsA", "dataset_type": "",
                                  "label_fmt": ".json", "total": 3, "labeled": 2}]


class TestWriteBackup:
    def test_打包内容与往返(self, db, db_dir, data_root, tmp_path):
        img_dir, lbl_dir = import_dataset(db, "p1", "dsA", data_root)
        out_dir = os.path.join(db_dir, "train_out", "t1")
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "best.pt"), "wb") as f:
            f.write(b"weights")
        db.add_train_record({"id": "t1", "project": "p1",
                             "model_path": os.path.join(out_dir, "best.pt"),
                             "output_path": out_dir, "metrics_file": "t1.json"})
        db.save_train_metrics("t1", {"epochs": [1, 2]})
        zip_path = str(tmp_path / "b.etbak")
        m = write_backup(db, "p1", zip_path,
                         progress=lambda d, t, s: None)
        assert m["project"] == "p1" and m["train_records"] == 1
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        assert MANIFEST_NAME in names and "records.json" in names
        assert "data/dsA/images/img0.png" in names
        assert "data/dsA/labels/img0.json" in names
        assert "models/t1/best.pt" in names
        assert "metrics/t1.json" in names

    def test_不勾数据与权重(self, db, data_root, tmp_path):
        import_dataset(db, "p1", "dsA", data_root)
        zip_path = str(tmp_path / "b2.etbak")
        write_backup(db, "p1", zip_path, include_data=False,
                     include_models=False)
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        assert not [n for n in names if n.startswith("data/")]
        assert not [n for n in names if n.startswith("models/")]


class TestRestore:
    def test_同名非空项目失败并带清单(self, db, data_root, tmp_path):
        import_dataset(db, "p1", "dsA", data_root)
        db.add_train_record({"id": "t1", "project": "p1",
                             "model_path": "/m/best.pt"})
        zip_path = str(tmp_path / "b.etbak")
        write_backup(db, "p1", zip_path)
        with pytest.raises(RestoreError) as e:
            check_restorable(db, zip_path)
        assert "已存在" in str(e.value)
        # 弹窗清单: 数据集与训练记录都要列出来
        assert any("dsA" in it for it in e.value.items)
        assert any("t1" in it for it in e.value.items)

    def test_恢复写入时同名非空也失败(self, db, data_root, tmp_path):
        import_dataset(db, "p1", "dsA", data_root)
        zip_path = str(tmp_path / "b.etbak")
        write_backup(db, "p1", zip_path)
        dest = os.path.join(str(tmp_path), "r")
        with pytest.raises(RestoreError):
            restore_backup(db, zip_path, dest)
        assert not os.path.exists(dest)   # 校验不过, 不落盘

    def test_同名空项目可恢复合并(self, db, data_root, tmp_path):
        import_dataset(db, "p1", "dsA", data_root)
        zip_path = str(tmp_path / "b.etbak")
        write_backup(db, "p1", zip_path)
        db2_dir = tempfile.mkdtemp(prefix="et_test_bak5_")
        try:
            db2 = DataBase(db2_dir)
            db2.add_project("p1")   # 用户误建的同名空项目
            check_restorable(db2, zip_path)   # 不抛
            dest = os.path.join(db2_dir, "r")
            restore_backup(db2, zip_path, dest)
            assert db2.get_projects().count("p1") == 1   # add_project 不去重
            infos = [i for i in db2.get_project_info()
                     if i["project_name"] == "p1"]
            assert [i["dataset_name"] for i in infos] == ["dsA"]
            assert get_path_pairs(infos[0])[0][0] == os.path.join(
                dest, "data", "dsA", "images")
        finally:
            shutil.rmtree(db2_dir, ignore_errors=True)

    def test_坏包与版本(self, tmp_path):
        bad = tmp_path / "bad.etbak"
        bad.write_bytes(b"not a zip")
        with pytest.raises(RestoreError):
            read_backup(str(bad))
        future = tmp_path / "future.etbak"
        with zipfile.ZipFile(str(future), "w") as zf:
            zf.writestr(MANIFEST_NAME, json.dumps(
                {"format_version": FORMAT_VERSION + 1, "project": "x"}))
            zf.writestr("records.json", "{}")
        with pytest.raises(RestoreError) as e:
            read_backup(str(future))
        assert "版本" in str(e.value)

    def test_完整往返_路径重写与合并(self, db, data_root, tmp_path):
        import_dataset(db, "p1", "dsA", data_root)
        import_dataset(db, "p1", "dsB", data_root, with_labels=False)
        # 多轮导入: 第 1 轮无标签(空串占位), 第 2 轮带标签
        img2, lbl2 = make_dataset(data_root, "dsC2")
        db.add_dataset("p1", "dsC")
        db.update_dataset_import("p1", "dsC", [img2, img2], ["", lbl2], ".json",
                                 labeled=1, total=3)
        out_dir = os.path.join(data_root, "train_out")
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "best.pt"), "wb") as f:
            f.write(b"w")
        db.add_train_record({"id": "t1", "project": "p1",
                             "model_path": os.path.join(out_dir, "best.pt"),
                             "output_path": out_dir, "metrics_file": "t1.json"})
        db.save_train_metrics("t1", {"epochs": [1]})
        db.save_train_queue([{"qid": "q1", "order": 0, "status": "waiting",
                              "params": {"datasets": [{"project": "p1",
                                                       "dataset_name": "dsA"}]}}])
        db.save_paste_region_templates({"p1/dsA": {"t": {"ref_size": [1, 1],
                                                         "regions": []}}})

        zip_path = str(tmp_path / "b.etbak")
        write_backup(db, "p1", zip_path)
        shutil.rmtree(os.path.join(data_root, "p1"), ignore_errors=True)

        # 恢复到新库(模拟另一台机器)
        db2_dir = tempfile.mkdtemp(prefix="et_test_bak2_")
        try:
            db2 = DataBase(db2_dir)
            db2.add_project("other")   # 无关项目, 不能被恢复波及
            db2.add_train_record({"id": "keep", "project": "other"})
            dest = os.path.join(db2_dir, "restore")
            restore_backup(db2, zip_path, dest)

            # 项目与数据集
            assert "p1" in db2.get_projects() and "other" in db2.get_projects()
            infos = {i["dataset_name"]: i for i in db2.get_project_info()
                     if i["project_name"] == "p1"}
            assert set(infos) == {"dsA", "dsB", "dsC"}
            # 路径全部重写到恢复目录, 配对保持等长
            for name, info in infos.items():
                pairs = get_path_pairs(info)
                assert pairs and all(
                    p[0] == os.path.join(dest, "data", name, "images")
                    for p in pairs), (name, pairs)
            # 源库里同目录两轮(第 2 轮补第 1 轮标签)被 merge 成一对,
            # 恢复后仍是一对且标签槽非空
            assert get_path_pairs(infos["dsC"]) == [
                (os.path.join(dest, "data", "dsC", "images"),
                 os.path.join(dest, "data", "dsC", "labels"))]
            assert get_path_pairs(infos["dsB"])[0][1] == ""   # 无标签仍为空串
            # 数据文件真的解出来了
            assert os.path.isfile(os.path.join(
                dest, "data", "dsA", "images", "img0.png"))
            assert os.path.isfile(os.path.join(
                dest, "data", "dsC", "labels", "img0.json"))
            # 训练记录: 路径重写 + 合并(other 的 keep 不受影响)
            recs = {r["id"]: r for r in db2.get_train_records()}
            assert set(recs) == {"t1", "keep"}
            assert recs["t1"]["output_path"] == os.path.join(
                dest, "models", "t1")
            assert recs["t1"]["model_path"] == os.path.join(
                dest, "models", "t1", "best.pt")
            assert os.path.isfile(recs["t1"]["model_path"])
            assert os.path.isfile(os.path.join(
                db2.metrics_dir, "t1.json"))
            # 队列: waiting 项恢复, order 顺延
            q = db2.get_train_queue()
            assert [it["qid"] for it in q] == ["q1"] and q[0]["order"] == 0
            # 粘贴模板
            assert "p1/dsA" in db2.get_paste_region_templates()
        finally:
            shutil.rmtree(db2_dir, ignore_errors=True)

    def test_队列只恢复未开始且去重(self, db, data_root, tmp_path):
        import_dataset(db, "p1", "dsA", data_root)
        db.save_train_queue([
            {"qid": "q1", "order": 0, "status": "waiting",
             "params": {"datasets": [{"project": "p1", "dataset_name": "dsA"}]}},
            {"qid": "q2", "order": 1, "status": "running",
             "params": {"datasets": [{"project": "p1", "dataset_name": "dsA"}]}},
            {"qid": "q3", "order": 2, "status": "done",
             "params": {"datasets": [{"project": "p1", "dataset_name": "dsA"}]}},
        ])
        zip_path = str(tmp_path / "b.etbak")
        write_backup(db, "p1", zip_path)
        db2_dir = tempfile.mkdtemp(prefix="et_test_bak3_")
        try:
            db2 = DataBase(db2_dir)
            db2.save_train_queue([{"qid": "old", "order": 7, "status": "waiting",
                                   "params": {}}])
            restore_backup(db2, zip_path, os.path.join(db2_dir, "r"))
            q = db2.get_train_queue()
            assert [it["qid"] for it in q] == ["old", "q1"]
            assert q[1]["order"] == 8   # 顺延到现有队尾
        finally:
            shutil.rmtree(db2_dir, ignore_errors=True)

    def test_不勾数据时保留原路径(self, db, data_root, tmp_path):
        img_dir, lbl_dir = import_dataset(db, "p1", "dsA", data_root)
        zip_path = str(tmp_path / "b.etbak")
        write_backup(db, "p1", zip_path, include_data=False)
        db2_dir = tempfile.mkdtemp(prefix="et_test_bak4_")
        try:
            db2 = DataBase(db2_dir)
            restore_backup(db2, zip_path, os.path.join(db2_dir, "r"),
                           include_data=False)
            info = db2.get_dataset_import("p1", "dsA")
            assert info["image_paths"] == [img_dir]
            assert info["label_paths"] == [lbl_dir]
        finally:
            shutil.rmtree(db2_dir, ignore_errors=True)


class TestRestoreIntoTarget:
    """右键恢复: 内容进目标项目(记录归属改写), 不按包内项目名新建."""

    def _make_pkg(self, db, data_root, tmp_path):
        """造一个 p1 的备份包: 数据集+训练/模型记录+队列(含别的项目引用)+模板."""
        import_dataset(db, "p1", "dsA", data_root)
        out_dir = os.path.join(data_root, "train_out")
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "best.pt"), "wb") as f:
            f.write(b"w")
        db.add_train_record({"id": "t1", "project": "p1",
                             "model_path": os.path.join(out_dir, "best.pt"),
                             "output_path": out_dir, "metrics_file": "t1.json"})
        db.add_model_record({"id": "t1", "project": "p1"})
        db.save_train_queue([
            {"qid": "q1", "order": 0, "status": "waiting",
             "params": {"datasets": [
                 {"project": "p1", "dataset_name": "dsA"},
                 {"project": "other", "dataset_name": "dsX"}]}},
        ])
        db.save_paste_region_templates(
            {"p1/dsA": {"t": {"ref_size": [1, 1], "regions": []}}})
        zip_path = str(tmp_path / "b.etbak")
        write_backup(db, "p1", zip_path)
        return zip_path

    def test_恢复到空项目_记录全部改写归属(self, db, data_root, tmp_path):
        zip_path = self._make_pkg(db, data_root, tmp_path)
        db2_dir = tempfile.mkdtemp(prefix="et_test_bak6_")
        try:
            db2 = DataBase(db2_dir)
            db2.add_project("恢复1")   # 用户右键的空项目
            dest = os.path.join(db2_dir, "r")
            m = restore_backup(db2, zip_path, dest, target_project="恢复1")
            assert m["project"] == "p1"
            assert "p1" not in db2.get_projects()   # 不按包内项目名新建
            # 数据集归属改写 + 路径重写 + 数据落盘
            infos = [i for i in db2.get_project_info()
                     if i["project_name"] == "恢复1"]
            assert [i["dataset_name"] for i in infos] == ["dsA"]
            assert get_path_pairs(infos[0])[0][0] == os.path.join(
                dest, "data", "dsA", "images")
            assert os.path.isfile(os.path.join(
                dest, "data", "dsA", "images", "img0.png"))
            # 训练/模型记录归属改写 + 产物路径重写
            recs = {r["id"]: r for r in db2.get_train_records()}
            assert recs["t1"]["project"] == "恢复1"
            assert recs["t1"]["output_path"] == os.path.join(
                dest, "models", "t1")
            mrecs = {r["id"]: r for r in db2.get_model_records()}
            assert mrecs["t1"]["project"] == "恢复1"
            # 队列: 目标项目的引用改写, 别的项目的引用原样保留
            q = db2.get_train_queue()
            assert [it["qid"] for it in q] == ["q1"]
            dss = q[0]["params"]["datasets"]
            assert dss[0] == {"project": "恢复1", "dataset_name": "dsA"}
            assert dss[1] == {"project": "other", "dataset_name": "dsX"}
            # 粘贴模板 key 前缀改写
            assert "恢复1/dsA" in db2.get_paste_region_templates()
            assert "p1/dsA" not in db2.get_paste_region_templates()
        finally:
            shutil.rmtree(db2_dir, ignore_errors=True)

    def test_目标项目非空_失败带清单且不落盘(self, db, data_root, tmp_path):
        zip_path = self._make_pkg(db, data_root, tmp_path)
        db2_dir = tempfile.mkdtemp(prefix="et_test_bak7_")
        try:
            db2 = DataBase(db2_dir)
            import_dataset(db2, "恢复1", "dsOld", data_root)
            dest = os.path.join(db2_dir, "r")
            with pytest.raises(RestoreError) as e:
                check_restorable(db2, zip_path, "恢复1")
            assert any("dsOld" in it for it in e.value.items)
            with pytest.raises(RestoreError):
                restore_backup(db2, zip_path, dest, target_project="恢复1")
            assert not os.path.exists(dest)   # 校验不过, 不落盘
            infos = [i for i in db2.get_project_info()
                     if i["project_name"] == "恢复1"]
            assert [i["dataset_name"] for i in infos] == ["dsOld"]  # 原内容不动
        finally:
            shutil.rmtree(db2_dir, ignore_errors=True)

    def test_目标项目不存在则新建(self, db, data_root, tmp_path):
        # 入口只传已有项目; 直调 core 时目标不存在也按需新建(与旧语义一致)
        zip_path = self._make_pkg(db, data_root, tmp_path)
        db2_dir = tempfile.mkdtemp(prefix="et_test_bak8_")
        try:
            db2 = DataBase(db2_dir)
            restore_backup(db2, zip_path, os.path.join(db2_dir, "r"),
                           target_project="恢复1")
            assert "恢复1" in db2.get_projects()
            infos = [i for i in db2.get_project_info()
                     if i["project_name"] == "恢复1"]
            assert [i["dataset_name"] for i in infos] == ["dsA"]
        finally:
            shutil.rmtree(db2_dir, ignore_errors=True)
