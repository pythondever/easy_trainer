# -*- coding: utf-8 -*-
"""
data_prep 测试: 目录配对读取、类别收集、图旁 json 权威覆盖、
copy_datasets / merge_split / prepare_dataset 装配链路.

这一层错了同样是静默脏数据(坐标按错图的尺寸换算/同名互相覆盖),
所以每个环节都落盘验证, 不只验证返回值.
"""
import json
import os

import pytest
from PIL import Image

from app.core.db import get_path_pairs, get_paths
from app.train import data_prep as dp


def _mk_img(path, size=(100, 50), color=(255, 0, 0)):
    Image.new("RGB", size, color).save(str(path))


def _labelme(path, shapes, iw=100, ih=50):
    doc = {"version": "5.0.1", "shapes": shapes, "imagePath": "x.png",
           "imageWidth": iw, "imageHeight": ih}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f)


def _rect(label, x1, y1, x2, y2):
    return {"label": label, "points": [[x1, y1], [x2, y2]],
            "shape_type": "rectangle", "flags": {}}


def _poly(label, pts):
    return {"label": label, "points": pts, "shape_type": "polygon",
            "flags": {}}


class TestPairing:
    def test_paired_dirs_按轮次配对(self, tmp_path):
        a, b = str(tmp_path / "a"), str(tmp_path / "b")
        info = {"image_paths": [a, b], "label_paths": [a + "_lab", ""]}
        assert dp._paired_dirs(info) == [(a, a + "_lab"), (b, "")]

    def test_paired_dirs_老单值记录(self, tmp_path):
        a = str(tmp_path / "a")
        info = {"image_path": a, "label_path": a + "_lab"}
        assert dp._paired_dirs(info) == [(a, a + "_lab")]

    def test_label_img_dirs_配对优先其余兜底(self):
        assert dp._label_img_dirs("a", ["a", "b", "c"]) == ["a", "b", "c"]
        assert dp._label_img_dirs("", ["b", "c"]) == ["b", "c"]


class TestSortLabels:
    def test_数字标签按数值升序(self):
        assert dp._sort_labels(["10", "2", "cat", "1"]) == ["1", "2", "10", "cat"]


class TestUniqueDst:
    def test_无used_按磁盘探测(self, tmp_path):
        (tmp_path / "a.png").write_bytes(b"x")
        r1 = dp._unique_dst(str(tmp_path), "a.png")
        assert os.path.basename(r1) == "a_1.png"
        # 调用方真的落盘后, 下一次才继续往上加
        open(r1, "wb").close()
        r2 = dp._unique_dst(str(tmp_path), "a.png")
        assert os.path.basename(r2) == "a_2.png"

    def test_used集合是权威_跨数据集累加(self, tmp_path):
        (tmp_path / "a.png").write_bytes(b"x")  # 磁盘有也不算数
        used = set()
        assert os.path.basename(
            dp._unique_dst(str(tmp_path), "a.png", used)) == "a.png"
        assert os.path.basename(
            dp._unique_dst(str(tmp_path), "a.png", used)) == "a_1.png"
        assert os.path.basename(
            dp._unique_dst(str(tmp_path), "a.png", used)) == "a_2.png"

    def test_used已占用时不看磁盘(self, tmp_path):
        used = {"a.png", "a_1.png"}
        assert os.path.basename(
            dp._unique_dst(str(tmp_path), "a.png", used)) == "a_2.png"


class TestCollectLabels:
    def test_标签目录与图旁json都扫(self, tmp_path):
        img_dir = tmp_path / "imgs"
        lab_dir = tmp_path / "labs"
        img_dir.mkdir()
        lab_dir.mkdir()
        _mk_img(img_dir / "b.png")
        _labelme(str(img_dir / "b.json"), [_rect("dog", 20, 20, 60, 40)])
        _labelme(str(lab_dir / "a.json"), [_rect("cat", 10, 10, 40, 40)])
        labels = dp._collect_labels([{
            "fmt": "json", "image_paths": [str(img_dir)],
            "label_paths": [str(lab_dir)]}])
        assert labels == ["cat", "dog"]

    def test_txt按label_ids换显示名(self, tmp_path):
        lab_dir = tmp_path / "labs"
        lab_dir.mkdir()
        (lab_dir / "a.txt").write_text("0 0.1 0.2 0.3 0.4\n",
                                       encoding="utf-8")
        labels = dp._collect_labels([{
            "fmt": "txt", "image_paths": [str(tmp_path / "no")],
            "label_paths": [str(lab_dir)], "label_ids": {"0": "cat"}}])
        assert labels == ["cat"]

    def test_目录不存在与非标注json不炸(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        (img_dir / "notes.json").write_text('{"list": [1]}',
                                            encoding="utf-8")
        labels = dp._collect_labels([{
            "fmt": "json", "image_paths": [str(img_dir)],
            "label_paths": [str(tmp_path / "gone")]}])
        assert labels == []


class TestOverrideBySameDirJson:
    def test_覆盖导入结果_空shapes也写(self, tmp_path):
        img_dir = tmp_path / "imgs"
        dst = tmp_path / "dst"
        img_dir.mkdir()
        dst.mkdir()
        _mk_img(img_dir / "a.png")
        _mk_img(img_dir / "b.png")
        _mk_img(img_dir / "c.png")
        _labelme(str(img_dir / "a.json"), [_rect("cat", 10, 10, 40, 40)])
        _labelme(str(img_dir / "b.json"), [])  # 用户在界面删空了
        (dst / "a.txt").write_text("GARBAGE", encoding="utf-8")
        dp._override_by_same_dir_json(str(img_dir), str(dst), {"cat": 0},
                                      False)
        # 权威来源覆盖导入目录的旧结果
        assert (dst / "a.txt").read_text(encoding="utf-8") == \
            "0 0.250000 0.500000 0.300000 0.600000\n"
        # 空 shapes 也要写: 否则删掉的框会在训练里复活
        assert (dst / "b.txt").exists()
        assert (dst / "b.txt").read_text(encoding="utf-8") == ""
        # 没有同路径 json 的图不生成空 txt
        assert not (dst / "c.txt").exists()

    def test_尺寸查不到跳过(self, tmp_path):
        img_dir = tmp_path / "imgs"
        dst = tmp_path / "dst"
        img_dir.mkdir()
        dst.mkdir()
        _labelme(str(img_dir / "d.json"), [_rect("cat", 1, 1, 2, 2)])
        dp._override_by_same_dir_json(str(img_dir), str(dst), {"cat": 0},
                                      False)
        assert not (dst / "d.txt").exists()


class TestCopyDatasets:
    def _one_ds(self, tmp_path):
        img_dir = tmp_path / "imgs"
        lab_dir = tmp_path / "labs"
        img_dir.mkdir()
        lab_dir.mkdir()
        _mk_img(img_dir / "a.png")
        _mk_img(img_dir / "b.png")
        _labelme(str(lab_dir / "a.json"), [_rect("cat", 10, 10, 40, 40)])
        _labelme(str(img_dir / "b.json"), [_rect("dog", 20, 20, 60, 40)])
        return img_dir, lab_dir, {
            "dataset_name": "ds", "fmt": "json", "split": "train",
            "image_paths": [str(img_dir)], "label_paths": [str(lab_dir)]}

    def test_端到端_图像与坐标换算(self, tmp_path):
        img_dir, lab_dir, info = self._one_ds(tmp_path)
        out = str(tmp_path / "out")
        labels, l2i = dp.copy_datasets(out, "proj", [info])
        assert labels == ["cat", "dog"]
        assert l2i == {"cat": 0, "dog": 1}
        dst = tmp_path / "out" / "proj" / "ds"
        assert sorted(os.listdir(dst / "images")) == ["a.png", "b.png"]
        # 导入目录标签按图像尺寸换算
        assert (dst / "labels" / "a.txt").read_text(encoding="utf-8") == \
            "0 0.250000 0.500000 0.300000 0.600000\n"
        # 图旁 json 覆盖导入目录结果
        assert (dst / "labels" / "b.txt").read_text(encoding="utf-8") == \
            "1 0.400000 0.600000 0.400000 0.400000\n"

    def test_segment写多边形顶点(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        _mk_img(img_dir / "a.png")
        _labelme(str(img_dir / "a.json"),
                 [_poly("cat", [[10, 10], [50, 10], [50, 50]])])
        info = {"dataset_name": "ds", "fmt": "json", "split": "train",
                "image_paths": [str(img_dir)], "label_paths": []}
        labels, l2i = dp.copy_datasets(str(tmp_path / "out"), "proj", [info],
                                       task="segment")
        txt = (tmp_path / "out" / "proj" / "ds" / "labels" /
               "a.txt").read_text(encoding="utf-8")
        assert len(txt.split()) == 7  # cls + 3 个顶点
        assert labels == ["cat"]


class TestMergeSplit:
    def test_同名加序号_图文保持一致(self, tmp_path):
        # merge_split 从 <out_root>/<项目>/<数据集> 取副本, 与
        # prepare_dataset 的落地布局一致; 源码必须放在 out_root 底下
        out = str(tmp_path / "out")
        for name, color, txt in (("ds1", (255, 0, 0), "x"),
                                 ("ds2", (0, 255, 0), "y")):
            src = tmp_path / "out" / "proj" / name
            (src / "images").mkdir(parents=True)
            (src / "labels").mkdir(parents=True)
            _mk_img(src / "images" / "a.png", color=color)
            (src / "labels" / "a.txt").write_text(txt, encoding="utf-8")
        datasets = [{"project": "proj", "dataset_name": n, "split": "train"}
                    for n in ("ds1", "ds2")]
        dp.merge_split(out, datasets)
        imgs = tmp_path / "out" / "train" / "images"
        labs = tmp_path / "out" / "train" / "labels"
        assert sorted(os.listdir(imgs)) == ["a.png", "a_1.png"]
        assert sorted(os.listdir(labs)) == ["a.txt", "a_1.txt"]
        # 图像和标签必须同步改名, 不能一个加序号一个不加
        assert (labs / "a_1.txt").read_text(encoding="utf-8") == "y"
        with Image.open(str(imgs / "a_1.png")) as im:
            assert im.getpixel((0, 0)) == (0, 255, 0)

    def test_源目录不存在不炸(self, tmp_path):
        dp.merge_split(str(tmp_path / "out"),
                       [{"project": "p", "dataset_name": "gone",
                         "split": "train"}])


class TestCleanSplit:
    def test_清空旧文件保留目录(self, tmp_path):
        out = tmp_path / "out"
        for split in ("train", "val"):
            for sub in ("images", "labels"):
                d = out / split / sub
                d.mkdir(parents=True)
                (d / "old.png").write_bytes(b"x")
        dp.clean_split(str(out))
        for split in ("train", "val"):
            for sub in ("images", "labels"):
                d = out / split / sub
                assert d.is_dir()
                assert os.listdir(d) == []


class TestWriteDataYaml:
    def test_内容(self, tmp_path):
        dp.write_data_yaml(str(tmp_path), ["cat", "dog"])
        assert (tmp_path / "data.yaml").read_text(encoding="utf-8") == \
            "train: train\nval: val\n\nnames:\n  0: cat\n  1: dog\n"


class TestDialogsHandoff:
    """
    dialogs.make_train_config → data_prep 的接缝回归(③ 的收尾):
    info 里的 image_paths/label_paths 必须是原始列表(带空串占位),
    否则 _paired_dirs 按位置配对会把第 1 轮的图配到第 2 轮的标签目录.
    """

    def test_滤空串的短列表会错位(self):
        # 钉住 bug 入口: dialogs 曾经把 get_paths 滤后的短列表递给
        # data_prep, "第 1 轮只导图像 + 第 2 轮带标签"就配成了这样
        binding = {"image_paths": ["d1", "d2"], "label_paths": ["", "lb"]}
        bad = {"image_paths": get_paths(binding, "image"),
               "label_paths": get_paths(binding, "label")}
        assert dp._paired_dirs(bad) == [("d1", "lb"), ("d2", "")]

    def test_原始列表配对正确(self):
        binding = {"image_paths": ["d1", "d2"], "label_paths": ["", "lb"]}
        info = {"image_paths": list(binding["image_paths"]),
                "label_paths": list(binding["label_paths"])}
        assert dp._paired_dirs(info) == [("d1", ""), ("d2", "lb")]


class TestPrepareDataset:
    def test_全链路_合并后删副本不影响train(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        _mk_img(img_dir / "a.png")
        _mk_img(img_dir / "b.png")
        _labelme(str(img_dir / "a.json"), [_rect("cat", 10, 10, 40, 40)])
        _labelme(str(img_dir / "b.json"), [_rect("dog", 20, 20, 60, 40)])
        info = {"dataset_name": "ds", "project": "proj", "fmt": "json",
                "split": "train",
                "image_paths": [str(img_dir)], "label_paths": []}
        out = str(tmp_path / "out")
        labels = dp.prepare_dataset(out, "proj", [info])
        assert labels == ["cat", "dog"]
        # 副本目录已删
        assert not (tmp_path / "out" / "proj").exists()
        # 两级之间走硬链接, 删副本后 train 里的文件仍然完好
        train_imgs = tmp_path / "out" / "train" / "images"
        assert sorted(os.listdir(train_imgs)) == ["a.png", "b.png"]
        with Image.open(str(train_imgs / "a.png")) as im:
            assert im.size == (100, 50)
        assert (tmp_path / "out" / "train" / "labels" /
                "a.txt").read_text(encoding="utf-8") != ""
        assert (tmp_path / "out" / "data.yaml").exists()

    def test_没有类别抛错(self, tmp_path):
        img_dir = tmp_path / "imgs"
        img_dir.mkdir()
        _mk_img(img_dir / "a.png")  # 没有任何标签
        info = {"dataset_name": "ds", "fmt": "json", "split": "train",
                "image_paths": [str(img_dir)], "label_paths": []}
        with pytest.raises(RuntimeError):
            dp.prepare_dataset(str(tmp_path / "out"), "proj", [info])
