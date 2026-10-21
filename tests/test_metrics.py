# -*- coding: utf-8 -*-
"""
metrics 测试: metrics.csv 解析(用户约定统一入口)、主指标口径、
好坏分折算、编辑距离/CER.
"""
import pytest

from app.core import metrics as M


def _csv(tmp_path, rows, encoding="utf-8"):
    """rows: [{"epoch": "1", "val/mAP_50": "0.5", ...}, ...] 写成 csv."""
    p = tmp_path / "metrics.csv"
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    lines = [",".join(keys)]
    for r in rows:
        lines.append(",".join(str(r.get(k, "")) for k in keys))
    p.write_bytes(("\n".join(lines) + "\n").encode(encoding))
    return str(p)


class TestSeriesFromCsv:
    def test_正常解析(self, tmp_path):
        p = _csv(tmp_path, [
            {"epoch": "1", "val/mAP_50": "0.5", "val/mAP_50_95": "0.3",
             "train/loss": "1.2"},
            {"epoch": "2", "val/mAP_50": "0.7", "val/mAP_50_95": "0.4",
             "train/loss": "0.8"},
        ])
        s = M.series_from_csv(p)
        assert s["epochs"] == [1, 2]
        assert s["mAP@50"] == [0.5, 0.7]
        assert s["mAP@50-95"] == [0.3, 0.4]
        assert s["train_loss"] == [1.2, 0.8]

    def test_没出现过的列不进series(self, tmp_path):
        p = _csv(tmp_path, [{"epoch": "1", "val/mAP_50": "0.5"}])
        s = M.series_from_csv(p)
        assert "recall" not in s

    def test_同epoch多行后者覆盖(self, tmp_path):
        p = _csv(tmp_path, [
            {"epoch": "1", "val/mAP_50": "0.5"},
            {"epoch": "1", "val/mAP_50": "0.9"},
            {"epoch": "2", "val/mAP_50": "0.6"},
        ])
        s = M.series_from_csv(p)
        assert s["epochs"] == [1, 2]
        assert s["mAP@50"] == [0.9, 0.6]

    def test_epoch列坏行跳过(self, tmp_path):
        p = _csv(tmp_path, [
            {"epoch": "abc", "val/mAP_50": "0.5"},
            {"epoch": "1", "val/mAP_50": "0.6"},
        ])
        s = M.series_from_csv(p)
        assert s["epochs"] == [1]
        assert s["mAP@50"] == [0.6]

    def test_缺值补None占位(self, tmp_path):
        p = _csv(tmp_path, [
            {"epoch": "1", "val/mAP_50": "0.5", "val/recall": "0.6"},
            {"epoch": "2", "val/mAP_50": "0.7"},
        ])
        s = M.series_from_csv(p)
        assert s["recall"] == [0.6, None]

    def test_文件不存在返回空(self, tmp_path):
        assert M.series_from_csv(str(tmp_path / "nope.csv")) == {}

    def test_gbk编码的子进程产物能读(self, tmp_path):
        # lightning 在管道下按 ANSI 码页写 csv, 中文列值不能按 utf-8 解;
        # "狗" 的 gbk 字节不是合法 utf-8, 固定 utf-8 解会把整份 csv 读废
        p = _csv(tmp_path, [
            {"epoch": "1", "val/mAP_50": "0.5", "类别": "狗"},
            {"epoch": "2", "val/mAP_50": "0.7", "类别": "狗"},
        ], encoding="gbk")
        s = M.series_from_csv(p)
        assert s["mAP@50"] == [0.5, 0.7]


class TestMetricKey:
    def test_ema优先(self):
        assert M.metric_key({"mAP@50": [1], "ema_mAP@50": [1]},
                            "mAP@50") == "ema_mAP@50"

    def test_无ema取原列(self):
        assert M.metric_key({"mAP@50": [1]}, "mAP@50") == "mAP@50"

    def test_分割按mask系列判定(self):
        s = {"mask_mAP@50": [0.5], "mask_ema_mAP@50": [0.6]}
        assert M.metric_key(s, "mAP@50") == "mask_ema_mAP@50"

    def test_旧分割无mask_ema(self):
        assert M.metric_key({"mask_mAP@50": [0.5]}, "mAP@50") == "mask_mAP@50"

    def test_非分割不误触mask前缀(self):
        # 有 mask 列就按分割口径走, 即使同时存在普通列
        s = {"mAP@50": [0.4], "mask_mAP@50": [0.5]}
        assert M.metric_key(s, "mAP@50") == "mask_mAP@50"

    def test_没有返回空串(self):
        assert M.metric_key({}, "mAP@50") == ""


class TestPrimaryOf:
    def test_task优先于内容推断(self):
        p = M.primary_of({"auroc": [0.9]}, "detect")
        assert p.field == "map50"

    def test_无task按auroc推断(self):
        assert M.primary_of({"auroc": [0.9]}).label == "AUROC"

    def test_按accuracy推断(self):
        assert M.primary_of({"accuracy": [0.9]}).label == "准确率"

    def test_都不像按检测兜底(self):
        assert M.primary_of({}).base == "mAP@50"

    def test_未登记任务返回None(self):
        assert M.primary_for("nope") is None

    def test_ocr_rec是错误率方向(self):
        p = M.primary_for("ocr_rec")
        assert p.direction == -1


class TestBestValue:
    def test_取最大(self):
        assert M.best_value({"mAP@50": [0.1, 0.5, 0.3]}, "mAP@50") == 0.5

    def test_错误率取最小(self):
        assert M.best_value({"CER": [1.2, 0.8, 1.5]}, "CER", -1) == 0.8

    def test_无数据返回None(self):
        assert M.best_value({}, "mAP@50") is None

    def test_全None占位返回None(self):
        assert M.best_value({"mAP@50": [None, None]}, "mAP@50") is None

    def test_尾部None占位忽略(self):
        assert M.best_value({"mAP@50": [0.3, None, 0.6]}, "mAP@50") == 0.6


class TestScoreOf:
    def test_越大越好原样(self):
        assert M.score_of("detect", 0.85) == 0.85

    def test_错误率取1减x(self):
        assert M.score_of("ocr_rec", 0.2) == pytest.approx(0.8)

    def test_欠训练CER截断到0(self):
        assert M.score_of("ocr_rec", 1.5) == 0.0

    def test_负值截断到0(self):
        assert M.score_of("detect", -0.5) == 0.0

    def test_None透传(self):
        assert M.score_of("detect", None) is None


class TestBestMap50FromCsv:
    def test_取交付精度(self, tmp_path):
        p = _csv(tmp_path, [
            {"epoch": "1", "val/mAP_50": "0.51234", "val/mAP_50_95": "0.31234"},
            {"epoch": "2", "val/mAP_50": "0.61234", "val/mAP_50_95": "0.41234"},
        ])
        assert M.best_map50_from_csv(p) == {"map50": 0.6123,
                                            "map50_95": 0.4123}

    def test_读不到返回空(self, tmp_path):
        assert M.best_map50_from_csv(str(tmp_path / "nope.csv")) == {}


class TestEditDistance:
    @pytest.mark.parametrize("a,b,expect", [
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("", "abc", 3),
        ("abc", "", 3),
        ("", "", 0),
        ("abc", "abc", 0),
    ])
    def test_经典用例(self, a, b, expect):
        assert M.edit_distance(a, b) == expect


class TestCer:
    def test_微平均(self):
        # 总参考长 6, 编辑距离 0+2, 长串权重更大
        assert M.cer(["ab", "abcd"], ["ab", "ab"]) == pytest.approx(2 / 6)

    def test_长度不配对抛错(self):
        with pytest.raises(ValueError):
            M.cer(["ab"], ["a", "b"])

    def test_参考全空返回None(self):
        assert M.cer(["", ""], ["a", "b"]) is None

    def test_全对返回0(self):
        assert M.cer(["ab"], ["ab"]) == 0.0


class TestEditOps:
    def test_替换加插入(self):
        # kitten→sitting: k→s, e→i 两次替换 + 插入 g
        assert M.edit_ops("kitten", "sitting") == (2, 0, 1)

    def test_纯删除(self):
        assert M.edit_ops("abc", "ac") == (0, 1, 0)

    def test_纯插入(self):
        assert M.edit_ops("ac", "abc") == (0, 0, 1)

    def test_相同(self):
        assert M.edit_ops("abc", "abc") == (0, 0, 0)

    def test_空串(self):
        assert M.edit_ops("", "abc") == (0, 0, 3)
        assert M.edit_ops("abc", "") == (0, 3, 0)


class TestCerDetail:
    def test_分解合计一致(self):
        refs = ["kitten", "flaw", "abc"]
        hyps = ["sitting", "lawn", "abc"]
        d = M.cer_detail(refs, hyps)
        assert d["sub"] + d["dele"] + d["ins"] == \
            sum(M.edit_distance(r, h) for r, h in zip(refs, hyps))
        assert d["correct"] == d["chars"] - d["sub"] - d["dele"]
        assert d["chars"] == 13  # 6+4+3

    def test_长度不配对抛错(self):
        with pytest.raises(ValueError):
            M.cer_detail(["ab"], ["a", "b"])
