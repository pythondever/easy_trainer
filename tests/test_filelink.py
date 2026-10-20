# -*- coding: utf-8 -*-
"""
clone_file: 同卷硬链接优先, 跨卷退回复制; 目标已存在先删再建.

先删再建防的是"就地覆盖顺着同一个数据块改到源图": dst 若是上一轮铺数据留下
的硬链接, 直接写内容会改到 inode 背后的那份源图.
"""

import os

from app.core.filelink import clone_file


class TestCloneFile:
    def test_同卷硬链接(self, tmp_path):
        src = tmp_path / "src.jpg"
        src.write_bytes(b"pixels")
        dst = tmp_path / "dst.jpg"
        clone_file(str(src), str(dst))
        assert dst.read_bytes() == b"pixels"
        assert os.path.samefile(str(src), str(dst))

    def test_目标已存在时先删_不动旧源(self, tmp_path):
        src1 = tmp_path / "src1.jpg"
        src1.write_bytes(b"one")
        dst = tmp_path / "dst.jpg"
        clone_file(str(src1), str(dst))          # dst 现在是 src1 的硬链接
        src2 = tmp_path / "src2.jpg"
        src2.write_bytes(b"two")
        clone_file(str(src2), str(dst))
        assert dst.read_bytes() == b"two"
        assert src1.read_bytes() == b"one"       # 旧源没被顺着数据块改掉

    def test_跨卷退化复制(self, tmp_path, monkeypatch):
        src = tmp_path / "src.jpg"
        src.write_bytes(b"pixels")
        dst = tmp_path / "dst.jpg"

        def _no_link(_a, _b):
            raise OSError("cross-device link")

        monkeypatch.setattr(os, "link", _no_link)
        clone_file(str(src), str(dst))
        assert dst.read_bytes() == b"pixels"
        assert not os.path.samefile(str(src), str(dst))
