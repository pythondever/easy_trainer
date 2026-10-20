# -*- coding: utf-8 -*-
"""
训练前校验: 多路径导入后不能只认最后一个目录.

误拦场景: 最新导入的目录被移走时报"尚未导入", 而早期导入目录的数据完好,
训不动. 校验按轮次遍历全部配对, 只要还有效图像目录就放行, 失效目录写日志
告警(数据准备层本就跳过它们).
"""

import pytest

from app.train import dialogs


@pytest.fixture
def check(monkeypatch):
    """接管 write_log: 校验里的目录失效告警收进列表, 不落盘."""
    logs = []
    monkeypatch.setattr(dialogs, "write_log", logs.append)
    return dialogs.check_dataset_imported, logs


def _mk_img(path, stem="img1"):
    img = path / (stem + ".jpg")
    img.write_bytes(b"")
    return img


class TestCheckDatasetImported:
    def test_全部目录失效才拦(self, check, tmp_path):
        f, _logs = check
        dead = str(tmp_path / "gone")
        with pytest.raises(ValueError, match="尚未导入图像"):
            f("DS", {"label_fmt": ".json", "image_paths": [dead], "label_paths": [""]})

    def test_空记录拦(self, check):
        f, _logs = check
        with pytest.raises(ValueError, match="尚未导入图像"):
            f("DS", {})

    def test_最新目录失效旧目录完好_放行并告警(self, check, tmp_path):
        f, logs = check
        old = tmp_path / "old"
        old.mkdir()
        lbl = tmp_path / "lbl"
        lbl.mkdir()
        f("DS", {"label_fmt": ".json",
                 "image_paths": [str(old), str(tmp_path / "gone")],
                 "label_paths": [str(lbl), ""]})
        assert any("gone" in m and "失效" in m for m in logs)

    def test_最新目录失效_图旁有标签也放行(self, check, tmp_path):
        f, _logs = check
        d = tmp_path / "d"
        d.mkdir()
        _mk_img(d)
        (d / "img1.json").write_text("{}", encoding="utf-8")
        f("DS", {"label_fmt": ".json",
                 "image_paths": [str(d), str(tmp_path / "gone")],
                 "label_paths": ["", ""]})

    def test_一个目录都没有标签才拦(self, check, tmp_path):
        f, _logs = check
        d = tmp_path / "d"
        d.mkdir()
        _mk_img(d)
        with pytest.raises(ValueError, match="尚未导入标签"):
            f("DS", {"label_fmt": ".json",
                     "image_paths": [str(d)], "label_paths": [""]})

    def test_cls_模式有图即放行(self, check, tmp_path):
        f, _logs = check
        d = tmp_path / "d"
        d.mkdir()
        _mk_img(d)
        f("DS", {"label_fmt": "cls", "image_paths": [str(d)], "label_paths": [""]})

    def test_txt_字条集看图旁同名_txt(self, check, tmp_path):
        f, _logs = check
        d = tmp_path / "d"
        d.mkdir()
        _mk_img(d)
        (d / "img1.txt").write_text("0 0.5 0.5 0.1 0.1", encoding="utf-8")
        f("DS", {"label_fmt": ".txt", "image_paths": [str(d)], "label_paths": [""]})

    def test_老单值记录(self, check, tmp_path):
        f, _logs = check
        d = tmp_path / "d"
        d.mkdir()
        lbl = tmp_path / "lbl"
        lbl.mkdir()
        f("DS", {"label_fmt": ".json", "image_path": str(d), "label_path": str(lbl)})
