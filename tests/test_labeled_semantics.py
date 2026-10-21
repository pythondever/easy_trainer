# -*- coding: utf-8 -*-
"""
「已标注」判定语义测试: rec_is_labeled / label_file_has_content /
image_has_label / count_images_labeled.

用户统一定义: 仅含非空有效框的标签计入已标注; 空/损坏 json 或缺失
文件视为未标注. 这套口径同时驱动导入框和首页进度两个数字, 边角
(空 shapes 不回退旧标签/字条集/cls 模式)全部钉死.
"""
import json
import os

import pytest

from app.core.label_utils import (count_images_labeled, image_has_label,
                                  label_file_has_content, rec_is_labeled)


def _labelme(path, shapes):
    doc = {"version": "5.0.1", "shapes": shapes,
           "imagePath": os.path.basename(path), "imageWidth": 100,
           "imageHeight": 100}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f)


def _rect(label="cat"):
    return {"label": label, "points": [[10, 10], [40, 40]],
            "shape_type": "rectangle", "flags": {}}


class TestRecIsLabeled:
    def test_有框(self):
        assert rec_is_labeled({"boxes": [(1, 2, 3, 4, "", "cat")]})

    def test_无框但有标签文件(self):
        assert rec_is_labeled({"_has_label_file": True})

    def test_分类数据集按cls字段(self):
        assert rec_is_labeled({"cls": "ng"})

    def test_全空(self):
        assert not rec_is_labeled({})
        assert not rec_is_labeled({"boxes": [], "_has_label_file": False,
                                   "cls": ""})


class TestLabelFileHasContent:
    def test_文件不存在(self, tmp_path):
        assert not label_file_has_content(str(tmp_path / "nope.json"), ".json")

    def test_空json对象(self, tmp_path):
        p = tmp_path / "a.json"
        p.write_text("{}", encoding="utf-8")
        assert not label_file_has_content(str(p), ".json")

    def test_json有有效框(self, tmp_path):
        p = tmp_path / "a.json"
        _labelme(str(p), [_rect()])
        assert label_file_has_content(str(p), ".json")

    def test_json空shapes不算(self, tmp_path):
        p = tmp_path / "a.json"
        _labelme(str(p), [])
        assert not label_file_has_content(str(p), ".json")

    def test_损坏json不算(self, tmp_path):
        p = tmp_path / "a.json"
        p.write_text("{not json", encoding="utf-8")
        assert not label_file_has_content(str(p), ".json")

    def test_yolo_txt有效行(self, tmp_path):
        p = tmp_path / "a.txt"
        p.write_text("0 0.1 0.2 0.3 0.4\n", encoding="utf-8")
        assert label_file_has_content(str(p), ".txt")

    def test_txt字条行也算(self, tmp_path):
        # 字条集整行是文字, 不是 yolo 字段, 但同样算已标注
        p = tmp_path / "a.txt"
        p.write_text("SN20261020\n", encoding="utf-8")
        assert label_file_has_content(str(p), ".txt")

    def test_txt空文件不算(self, tmp_path):
        p = tmp_path / "a.txt"
        p.write_text("", encoding="utf-8")
        assert not label_file_has_content(str(p), ".txt")


class TestImageHasLabel:
    def test_同路径json有框(self, tmp_path):
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        _labelme(str(tmp_path / "a.json"), [_rect()])
        assert image_has_label(str(img), [], ".json")

    def test_同路径json空shapes_不回退导入目录(self, tmp_path):
        # 用户在界面把框删空了: 同路径 json 权威, 旧标签不能复活
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        _labelme(str(tmp_path / "a.json"), [])
        old = tmp_path / "old_labels"
        old.mkdir()
        _labelme(str(old / "a.json"), [_rect()])
        assert not image_has_label(str(img), [str(old)], ".json")

    def test_同路径是非标注json_回退标签目录(self, tmp_path):
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        (tmp_path / "a.json").write_text('{"export_list": [1, 2]}',
                                        encoding="utf-8")
        old = tmp_path / "old_labels"
        old.mkdir()
        _labelme(str(old / "a.json"), [_rect()])
        assert image_has_label(str(img), [str(old)], ".json")

    def test_标签目录同名json(self, tmp_path):
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        old = tmp_path / "old_labels"
        old.mkdir()
        _labelme(str(old / "a.json"), [_rect()])
        assert image_has_label(str(img), [str(old)], ".json")

    def test_cls模式没有标签文件(self, tmp_path):
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        assert not image_has_label(str(img), [str(tmp_path)], "cls")

    def test_cls模式同路径labelme仍权威(self, tmp_path):
        # 同路径判定在 fmt 分支之前, cls 数据集旁边的标注 json 依然算数
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        _labelme(str(tmp_path / "a.json"), [_rect()])
        assert image_has_label(str(img), [], "cls")

    def test_txt扁平排布_标签和图同目录(self, tmp_path):
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        (tmp_path / "a.txt").write_text("0 0.1 0.2 0.3 0.4\n",
                                        encoding="utf-8")
        assert image_has_label(str(img), [], ".txt")

    def test_txt标签在指定目录(self, tmp_path):
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        lab = tmp_path / "labels"
        lab.mkdir()
        (lab / "a.txt").write_text("0 0.1 0.2 0.3 0.4\n", encoding="utf-8")
        assert image_has_label(str(img), [str(lab)], ".txt")

    def test_什么都没有(self, tmp_path):
        img = tmp_path / "a.png"
        img.write_bytes(b"fake")
        assert not image_has_label(str(img), [str(tmp_path)], ".json")


class TestCountImagesLabeled:
    def _mk_img(self, d, name):
        p = d / name
        p.write_bytes(b"fake")
        return p

    def test_目录不存在返回None(self, tmp_path):
        assert count_images_labeled(str(tmp_path / "nope")) is None

    def test_基本计数(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        self._mk_img(img_dir, "a.png")
        self._mk_img(img_dir, "b.png")
        self._mk_img(img_dir, "c.png")
        _labelme(str(img_dir / "b.json"), [_rect()])
        assert count_images_labeled(str(img_dir)) == (3, 1)

    def test_非图像扩展名不计入(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        self._mk_img(img_dir, "a.png")
        (img_dir / "notes.txt").write_text("x", encoding="utf-8")
        assert count_images_labeled(str(img_dir)) == (1, 0)

    def test_label_path多目录候选(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        lab1 = tmp_path / "lab1"
        lab1.mkdir()
        lab2 = tmp_path / "lab2"
        lab2.mkdir()
        self._mk_img(img_dir, "a.png")
        self._mk_img(img_dir, "b.png")
        _labelme(str(lab2 / "b.json"), [_rect()])
        assert count_images_labeled(str(img_dir), [str(lab1), str(lab2)],
                                    ".json") == (2, 1)

    def test_label_path单字符串(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        lab = tmp_path / "lab"
        lab.mkdir()
        self._mk_img(img_dir, "a.png")
        _labelme(str(lab / "a.json"), [_rect()])
        assert count_images_labeled(str(img_dir), str(lab), ".json") == (1, 1)

    def test_cancelled提前收工(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        for n in ("a.png", "b.png", "c.png"):
            self._mk_img(img_dir, n)
        calls = []

        def cancelled():
            calls.append(1)
            return True

        assert count_images_labeled(str(img_dir), cancelled=cancelled) is None
        assert calls  # 确实被调用过
