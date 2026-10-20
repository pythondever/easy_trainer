# -*- coding: utf-8 -*-
"""
labelme json 一次读盘出三个判定: shapes / 是否标注文件 / 是否 OCR 标志.

"这张图标过没有"要同时知道 shapes 是否为空和这个 json 是不是标注文件:
图像目录里可能有别的 json(导出清单, 类别表), 它们不是标注, 不能被当成
"这张图没有目标"把有效标签清空.
"""

import json

from app.core.label_utils import (is_text_label, load_json_shapes,
                                  load_json_shapes_checked, looks_like_labelme,
                                  normalize_label)


def _write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return str(path)


def _labelme(shapes, **extra):
    data = {"version": "5.0.1", "shapes": shapes}
    data.update(extra)
    return data


class TestLoadJsonShapesChecked:
    def test_正常标注(self, tmp_path):
        p = _write_json(tmp_path / "a.json", _labelme([
            {"label": "cat", "points": [[1, 2], [3, 4]], "shape_type": "rectangle"},
            {"label": "dog", "points": [[5, 6], [7, 8]], "text": "hello"},
        ]))
        shapes, is_labelme, is_ocr = load_json_shapes_checked(p)
        assert is_labelme and not is_ocr
        assert shapes == [("cat", [[1.0, 2.0], [3.0, 4.0]], ""),
                          ("dog", [[5.0, 6.0], [7.0, 8.0]], "hello")]

    def test_顶点不足的形状跳过(self, tmp_path):
        p = _write_json(tmp_path / "a.json", _labelme([
            {"label": "x", "points": [[1, 2]]},          # 只有 1 个点, 跳过
            {"label": "y", "points": [[1, 2], [3, 4]]},
        ]))
        shapes, is_labelme, _ocr = load_json_shapes_checked(p)
        assert is_labelme and [s[0] for s in shapes] == ["y"]

    def test_class_前缀归一(self, tmp_path):
        p = _write_json(tmp_path / "a.json", _labelme(
            [{"label": "class_3", "points": [[0, 0], [1, 1]]}]))
        assert load_json_shapes_checked(p)[0][0][0] == "3"

    def test_ocr_标志(self, tmp_path):
        p = _write_json(tmp_path / "a.json", _labelme(
            [{"label": "t", "points": [[0, 0], [1, 1]]}], ocr=True))
        shapes, is_labelme, is_ocr = load_json_shapes_checked(p)
        assert is_labelme and is_ocr and len(shapes) == 1

    def test_非标注_json(self, tmp_path):
        p = _write_json(tmp_path / "a.json", {"foo": 1})
        assert load_json_shapes_checked(p) == ([], False, False)

    def test_shapes_不是列表(self, tmp_path):
        p = _write_json(tmp_path / "a.json", {"shapes": "nope"})
        assert load_json_shapes_checked(p) == ([], False, False)

    def test_损坏_json(self, tmp_path):
        p = tmp_path / "a.json"
        p.write_text("{not json", encoding="utf-8")
        assert load_json_shapes_checked(str(p)) == ([], False, False)

    def test_文件不存在(self, tmp_path):
        assert load_json_shapes_checked(str(tmp_path / "none.json")) == ([], False, False)

    def test_形状结构损坏时仍是标注文件(self, tmp_path):
        # points 不是点列: 逐项转换抛异常, 整体判为标注文件但取不到 shapes
        p = _write_json(tmp_path / "a.json",
                        _labelme([{"label": "x", "points": "oops"}]))
        assert load_json_shapes_checked(p) == ([], True, False)

    def test_空shapes是标注文件(self, tmp_path):
        # 标注过又删空的图也是标注文件, 不能被当成"不是标注"
        p = _write_json(tmp_path / "a.json", _labelme([]))
        shapes, is_labelme, _ocr = load_json_shapes_checked(p)
        assert shapes == [] and is_labelme

    def test_两个入口口径一致(self, tmp_path):
        p = _write_json(tmp_path / "a.json", _labelme(
            [{"label": "cat", "points": [[1, 2], [3, 4]]}]))
        assert load_json_shapes(p) == load_json_shapes_checked(p)[0]
        assert looks_like_labelme(p) is True


class TestNormalizeLabel:
    def test_class_前缀(self):
        assert normalize_label("class_12") == "12"

    def test_普通名字去空白(self):
        assert normalize_label(" cat ") == "cat"

    def test_class_后缀非数字不动(self):
        assert normalize_label("class_x") == "class_x"


def test_is_text_label_两种语言都认():
    assert is_text_label("文本") and is_text_label("text")
    assert not is_text_label("cat")
