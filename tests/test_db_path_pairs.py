# -*- coding: utf-8 -*-
"""
导入轮次配对不变式: 第 i 个图像目录永远配第 i 个标签目录, 空串 = 该轮没导标签.

盯的是 2026-10-20 修的错位 bug: 两个列表各自去重再拼, 会让"第 1 轮只导
图像"错位成"第 1 轮的图吃第 2 轮的标签目录"; 标签按源目录尺寸算归一化坐标,
贴到别的图上全错且不报错.
"""

import shutil
import tempfile

import pytest

from app.core import db
from app.core.db import DataBase


class TestGetPathPairs:
    def test_多轮等长配对(self):
        assert db.get_path_pairs({"image_paths": ["a", "b"],
                                  "label_paths": ["x", "y"]}) == [("a", "x"), ("b", "y")]

    def test_空串占位表示该轮无标签(self):
        # 第 1 轮只导图像: 标签槽必须是空串, 不能被后面的标签目录顶上
        assert db.get_path_pairs({"image_paths": ["a", "b"],
                                  "label_paths": ["", "y"]}) == [("a", ""), ("b", "y")]

    def test_老记录长度不齐保持旧行为(self):
        # 历史上写歪的记录无从判断标签原属哪轮, 短侧补空串
        assert db.get_path_pairs({"image_paths": ["a", "b"],
                                  "label_paths": ["y"]}) == [("a", "y"), ("b", "")]

    def test_老单值记录(self):
        assert db.get_path_pairs({"image_path": "a", "label_path": "x"}) == [("a", "x")]

    def test_老单值只有图像(self):
        assert db.get_path_pairs({"image_path": "a"}) == [("a", "")]

    def test_空记录(self):
        assert db.get_path_pairs({}) == []
        assert db.get_path_pairs(None) == []


class TestMergePathPairs:
    def test_新图像目录开新槽(self):
        assert db.merge_path_pairs([], [("a", "x")]) == [("a", "x")]
        assert db.merge_path_pairs([("a", "x")], [("b", "y")]) == [("a", "x"), ("b", "y")]

    def test_已见目录补标签(self):
        assert db.merge_path_pairs([("a", "")], [("a", "x")]) == [("a", "x")]

    def test_空串不覆盖已有标签(self):
        # 重导同一图像目录但没给标签目录时, 原来那槽标签不能被清掉
        assert db.merge_path_pairs([("a", "x")], [("a", "")]) == [("a", "x")]

    def test_已见目录可换标签(self):
        assert db.merge_path_pairs([("a", "x")], [("a", "y")]) == [("a", "y")]

    def test_新目录无标签也开槽(self):
        assert db.merge_path_pairs([("a", "x")], [("b", "")]) == [("a", "x"), ("b", "")]

    def test_新侧图像为空跳过(self):
        assert db.merge_path_pairs([("a", "x")], [("", "y")]) == [("a", "x")]

    def test_多轮链式合并不错位(self):
        pairs = db.merge_path_pairs([], [("d1", "")])        # 第 1 轮只导图
        pairs = db.merge_path_pairs(pairs, [("d2", "l2")])   # 第 2 轮带标签
        pairs = db.merge_path_pairs(pairs, [("d1", "l1")])   # 补第 1 轮的标签
        assert pairs == [("d1", "l1"), ("d2", "l2")]


@pytest.fixture
def db_obj():
    """
    lmdb 在 Windows 上按 ANSI 码页解析路径, 非 ASCII 目录打不开 env
    (default_db_dir 的存在就是为这个), 所以库目录走 ASCII 临时目录,
    不用 pytest 的 tmp_path(它带着中文测试名).
    """
    db_dir = tempfile.mkdtemp(prefix="et_test_db_")
    try:
        yield DataBase(db_dir)
    finally:
        shutil.rmtree(db_dir, ignore_errors=True)


class TestUpdateDatasetImport:
    def test_单轮导入(self, db_obj):
        db_obj.update_dataset_import("P", "DS", "img", "lbl", label_fmt=".json",
                                     labeled=1, total=3)
        info = db_obj.get_dataset_import("P", "DS")
        assert info["image_paths"] == ["img"]
        assert info["label_paths"] == ["lbl"]
        assert info["image_path"] == "img"      # 单值字段保持最新, 向后兼容
        assert info["label_fmt"] == ".json"
        assert (info["labeled"], info["total"]) == (1, 3)

    def test_两轮_第二轮不顶掉第一轮的标签槽(self, db_obj):
        db_obj.update_dataset_import("P", "DS", "d1", "")        # 第 1 轮只导图
        db_obj.update_dataset_import("P", "DS", "d2", "l2")      # 第 2 轮带标签
        info = db_obj.get_dataset_import("P", "DS")
        assert info["image_paths"] == ["d1", "d2"]
        assert info["label_paths"] == ["", "l2"]
        assert db.get_path_pairs(info) == [("d1", ""), ("d2", "l2")]

    def test_重导同目录补标签(self, db_obj):
        db_obj.update_dataset_import("P", "DS", "d1", "")
        db_obj.update_dataset_import("P", "DS", "d1", "l1")
        assert db_obj.get_dataset_import("P", "DS")["label_paths"] == ["l1"]

    def test_重导同目录不给标签不清空(self, db_obj):
        db_obj.update_dataset_import("P", "DS", "d1", "l1")
        db_obj.update_dataset_import("P", "DS", "d1", "")
        assert db_obj.get_dataset_import("P", "DS")["label_paths"] == ["l1"]

    def test_一次调用传多轮按位置配对(self, db_obj):
        db_obj.update_dataset_import("P", "DS", ["d1", "d2"], ["", "l2"])
        info = db_obj.get_dataset_import("P", "DS")
        assert db.get_path_pairs(info) == [("d1", ""), ("d2", "l2")]

    def test_统计覆盖与累加(self, db_obj):
        db_obj.update_dataset_import("P", "DS", "d1", labeled=1, total=5)
        db_obj.update_dataset_import("P", "DS", "d2", labeled=2, total=7)   # 默认覆盖
        info = db_obj.get_dataset_import("P", "DS")
        assert (info["labeled"], info["total"]) == (2, 7)
        db_obj.update_dataset_import("P", "DS", "d2", labeled=3, total=4, append=True)
        info = db_obj.get_dataset_import("P", "DS")
        assert (info["labeled"], info["total"]) == (5, 11)

    def test_清空导入绑定(self, db_obj):
        db_obj.update_dataset_import("P", "DS", "d1", "l1", labeled=1, total=1)
        assert db_obj.clear_dataset_import("P", "DS") is True
        info = db_obj.get_dataset_import("P", "DS")
        assert info["image_paths"] == [] and info["label_paths"] == []

    def test_get_paths_滤空串_不能拿来配对(self, db_obj):
        # get_paths 滤掉空串占位后两个列表长度不齐, 按下标配对正是错位 bug 的入口
        db_obj.update_dataset_import("P", "DS", "d1", "")
        db_obj.update_dataset_import("P", "DS", "d2", "l2")
        info = db_obj.get_dataset_import("P", "DS")
        assert db.get_paths(info, "image") == ["d1", "d2"]
        assert db.get_paths(info, "label") == ["l2"]
        assert list(zip(db.get_paths(info, "image"),
                        db.get_paths(info, "label"))) == [("d1", "l2")]   # 错位实例
