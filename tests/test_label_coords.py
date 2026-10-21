# -*- coding: utf-8 -*-
"""
坐标换算测试: shapes_to_yolo_text(写) 与 load_yolo_shapes(读) 双向.
这两个函数是训练数据的最后一道关: 写错或读错都不报错, 只是把脏坐标
静默喂给模型, 所以往返一致性和每一处口径(补角/钳位/字段数)都钉死.
"""
import os

import pytest

from app.core.label_utils import (
    _rect_corners, load_yolo_shapes, points_bbox, shapes_to_boxes,
    shapes_to_detections, shapes_to_xywh, shapes_to_yolo_text)


def _pts_close(actual, expect):
    """逐点近似比较: pytest.approx 不支持嵌套列表."""
    assert len(actual) == len(expect)
    for a, e in zip(actual, expect):
        assert a == pytest.approx(e)


def _write_yolo(tmp_path, text):
    p = tmp_path / "labels.txt"
    p.write_text(text, encoding="utf-8")
    return str(p)


class TestShapesToYoloText:
    """labelme 形态 → yolo txt 行."""

    def test_bbox模式_矩形(self):
        txt = shapes_to_yolo_text(
            [("cat", [[10, 20], [110, 70]], "")], 200, 100, {"cat": 0})
        # cx=(10+50)/200=0.3, cy=(20+25)/100=0.45, w=100/200, h=50/100
        assert txt == "0 0.300000 0.450000 0.500000 0.500000\n"

    def test_bbox模式_多点取外接框(self):
        txt = shapes_to_yolo_text(
            [("cat", [[10, 10], [50, 5], [90, 80]], "")], 200, 100, {"cat": 0})
        # 外接框 x 10..90, y 5..80
        assert txt == "0 0.250000 0.425000 0.400000 0.750000\n"

    def test_bbox模式_越界不钳位(self):
        # 钉住现状: 只有 polygon 分支钳位到 [0,1], bbox 分支原样写出
        # (yolo 检测框允许越界, 由训练侧自行裁剪); 两处口径不一致是已知点
        txt = shapes_to_yolo_text(
            [("cat", [[-20, -10], [260, 150]], "")], 200, 100, {"cat": 0})
        assert txt == "0 0.600000 0.700000 1.400000 1.600000\n"

    def test_bbox模式_未知类别落0(self):
        txt = shapes_to_yolo_text(
            [("unknown_cls", [[0, 0], [10, 10]], "")], 100, 100, {"cat": 0})
        assert txt.startswith("0 ")

    def test_polygon模式_多边形原样归一化(self):
        txt = shapes_to_yolo_text(
            [("cat", [[10, 10], [50, 10], [50, 50]], "")],
            200, 100, {"cat": 0}, as_polygon=True)
        assert txt == "0 0.050000 0.100000 0.250000 0.100000 0.250000 0.500000\n"

    def test_polygon模式_矩形补四角(self):
        # yolo-seg 至少 3 个点, 两点矩形必须补成四角
        txt = shapes_to_yolo_text(
            [("cat", [[10, 10], [50, 50]], "")],
            200, 100, {"cat": 0}, as_polygon=True)
        parts = txt.split()
        assert len(parts) == 9  # cls + 4 个点
        assert parts[0] == "0"

    def test_auto模式_按形态分流(self):
        shapes = [("cat", [[10, 10], [50, 50]], ""),      # 矩形 → bbox
                  ("dog", [[10, 10], [50, 10], [50, 50]], "")]  # 多边形 → 顶点
        txt = shapes_to_yolo_text(shapes, 200, 100,
                                  {"cat": 0, "dog": 1}, as_polygon="auto")
        lines = txt.splitlines()
        assert len(lines) == 2
        assert len(lines[0].split()) == 5
        assert len(lines[1].split()) == 7

    def test_文字内容不写进txt(self):
        txt = shapes_to_yolo_text(
            [("__text__", [[10, 10], [50, 50]], "ABC123")], 200, 100, {})
        assert "ABC123" not in txt
        assert len(txt.split()) == 5

    def test_空shapes返回空串(self):
        assert shapes_to_yolo_text([], 200, 100, {}) == ""


class TestLoadYoloShapes:
    """yolo txt → labelme 形态."""

    def test_bbox行还原像素矩形(self, tmp_path):
        p = _write_yolo(tmp_path, "0 0.300000 0.450000 0.500000 0.500000\n")
        shapes = load_yolo_shapes(p, 200, 100)
        assert len(shapes) == 1
        label, pts, text = shapes[0]
        assert label == "0"
        assert text == ""
        _pts_close(pts, [[10, 20], [110, 70]])

    def test_多边形行还原顶点(self, tmp_path):
        p = _write_yolo(tmp_path, "0 0.050000 0.100000 0.250000 0.100000 0.250000 0.500000\n")
        shapes = load_yolo_shapes(p, 200, 100)
        assert len(shapes) == 1
        _pts_close(shapes[0][1], [[10, 10], [50, 10], [50, 50]])

    def test_字段异常行丢弃_不硬凑(self, tmp_path):
        # 6 字段(带置信度): vals 长度 5 为奇数, 只能丢
        p = _write_yolo(tmp_path,
                        "0 0.1 0.2 0.3 0.4 0.5\n"      # 5+1 字段
                        "0 0.1 0.2\n"                  # 不足 5 字段
                        "1 0.1 0.2 0.3 0.4\n")         # 正常行保留
        shapes = load_yolo_shapes(p, 100, 100)
        assert len(shapes) == 1
        assert shapes[0][0] == "1"

    def test_非数字行丢弃(self, tmp_path):
        p = _write_yolo(tmp_path, "0 a b c d\n1 0.1 0.2 0.3 0.4\n")
        shapes = load_yolo_shapes(p, 100, 100)
        assert len(shapes) == 1
        assert shapes[0][0] == "1"

    def test_尺寸为0返回空(self, tmp_path):
        p = _write_yolo(tmp_path, "0 0.1 0.2 0.3 0.4\n")
        assert load_yolo_shapes(p, 0, 0) == []

    def test_文件不存在返回空(self, tmp_path):
        assert load_yolo_shapes(str(tmp_path / "nope.txt"), 100, 100) == []

    def test_label_ids映射显示名并记录seen(self, tmp_path):
        p = _write_yolo(tmp_path, "0 0.1 0.2 0.3 0.4\n")
        seen = {}
        shapes = load_yolo_shapes(p, 100, 100, {"0": "cat"}, seen)
        assert shapes[0][0] == "cat"
        assert seen == {"0": "cat"}

    def test_空文件返回空(self, tmp_path):
        p = _write_yolo(tmp_path, "")
        assert load_yolo_shapes(p, 100, 100) == []


class TestRoundTrip:
    """写→读往返: 导出的 txt 必须能读回同一份坐标."""

    def test_bbox往返(self, tmp_path):
        shapes = [("cat", [[10, 20], [110, 70]], "")]
        txt = shapes_to_yolo_text(shapes, 200, 100, {"cat": 0})
        p = _write_yolo(tmp_path, txt)
        back = load_yolo_shapes(p, 200, 100, {"0": "cat"})
        assert len(back) == 1
        assert back[0][0] == "cat"
        _pts_close(back[0][1], [[10, 20], [110, 70]])

    def test_polygon往返(self, tmp_path):
        shapes = [("cat", [[10, 10], [50, 10], [50, 50]], "")]
        txt = shapes_to_yolo_text(shapes, 200, 100, {"cat": 0},
                                  as_polygon="auto")
        p = _write_yolo(tmp_path, txt)
        back = load_yolo_shapes(p, 200, 100, {"0": "cat"})
        _pts_close(back[0][1], [[10, 10], [50, 10], [50, 50]])

    def test_多点按bbox写_读回外接框一致(self, tmp_path):
        shapes = [("cat", [[10, 10], [50, 5], [90, 80]], "")]
        txt = shapes_to_yolo_text(shapes, 200, 100, {"cat": 0})
        p = _write_yolo(tmp_path, txt)
        back = load_yolo_shapes(p, 200, 100, {"0": "cat"})
        _pts_close(back[0][1], [[10, 5], [90, 80]])


class TestDerivedStructures:
    """points_bbox / shapes_to_xywh / detections / boxes / _rect_corners."""

    def test_points_bbox(self):
        assert points_bbox([[3, 9], [1, 2], [7, 4]]) == (1, 2, 7, 9)

    def test_rect_corners_对角顺序无关(self):
        assert _rect_corners([[90, 80], [10, 10]]) == \
            [[10, 10], [90, 10], [90, 80], [10, 80]]

    def test_shapes_to_xywh_基本换算(self):
        out = shapes_to_xywh([("cat", [[10, 20], [110, 70]], "T")])
        assert out == [(10, 20, 100, 50, "T", "cat")]
        # 类别一律取 box[-1], text 排在它前面
        assert out[0][-1] == "cat"
        assert out[0][-2] == "T"

    def test_shapes_to_xywh_退化框最小1像素(self):
        out = shapes_to_xywh([("cat", [[5, 5], [5, 5]], "")])
        assert out == [(5, 5, 1, 1, "", "cat")]

    def test_shapes_to_xywh_负坐标钳到0(self):
        out = shapes_to_xywh([("cat", [[-10, -20], [30, 40]], "")])
        assert out == [(0, 0, 40, 60, "", "cat")]

    def test_shapes_to_xywh_单点跳过(self):
        assert shapes_to_xywh([("cat", [[5, 5]], "")]) == []

    def test_shapes_to_detections_多边形保留顶点(self):
        out = shapes_to_detections(
            [("cat", [[1, 2], [3, 4], [5, 6]], "T"),
             ("dog", [[1, 2], [3, 4]], "")])
        assert out[0] == ("cat", [1, 2, 5, 6], [[1, 2], [3, 4], [5, 6]])
        assert out[1] == ("dog", [1, 2, 3, 4], None)

    def test_shapes_to_boxes_多边形与矩形(self):
        out = shapes_to_boxes(
            [("cat", [[1, 2], [3, 4], [5, 6]], ""),
             ("dog", [[1, 2], [3, 4]], "")])
        assert out[0]["shape_type"] == "polygon"
        assert out[0]["points"] == [[1, 2], [3, 4], [5, 6]]
        # 矩形分支不带 shape_type 键, 靠 x1/y1/x2/y2 存在性区分
        assert "shape_type" not in out[1]
        assert (out[1]["x1"], out[1]["y1"]) == (1, 2)
        assert (out[1]["x2"], out[1]["y2"]) == (3, 4)
