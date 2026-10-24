# -*- coding: utf-8 -*-
"""下拉条目的纯逻辑: 设备名拆两行、档位挑图标."""

import pytest

from app.train.combo_labels import size_icon_name, split_device_label


class TestSplitDeviceLabel:
    def test_显卡拆出显存(self):
        assert split_device_label("GeForce RTX 4070 (12 GB)") == (
            "GeForce RTX 4070", "12 GB")

    def test_两位显存(self):
        assert split_device_label("GeForce RTX 4090 (24 GB)") == (
            "GeForce RTX 4090", "24 GB")

    def test_小数显存(self):
        assert split_device_label("Tesla T4 (1.5 GB)") == ("Tesla T4", "1.5 GB")

    def test_括号内外多余空格(self):
        assert split_device_label("RTX 3090 (  24GB  )") == (
            "RTX 3090", "24 GB")

    def test_CPU没有显存副标(self):
        assert split_device_label("CPU") == ("CPU", "")

    def test_认不出的名字原样返回(self):
        assert split_device_label("GPU 0") == ("GPU 0", "")

    @pytest.mark.parametrize("value", ["", None, "   "])
    def test_空值给两个空串(self, value):
        assert split_device_label(value) == ("", "")


class TestSizeIconName:
    @pytest.mark.parametrize("level,icon", [
        ("nano", "size_1"), ("small", "size_2"), ("medium", "size_3"),
        ("large", "size_4"), ("x-large", "size_5"),
    ])
    def test_档位对应递增柱(self, level, icon):
        assert size_icon_name(level) == icon

    @pytest.mark.parametrize("level", ["patchcore", "", None, "tiny"])
    def test_非档位用通用图标(self, level):
        assert size_icon_name(level) == "model_generic"

    def test_前后空格不影响(self):
        assert size_icon_name("  nano  ") == "size_1"
