# -*- coding: utf-8 -*-
"""
预训练权重下载器(带进度).
不复用 rfdetr 内置的下载: 它用 tqdm 按 \r 刷新同一行, 而读取侧是逐行读进程输出,
整段下载期间日志是空的; 失败时也只往外抛原始异常. 这里按块下载, 进度直接发信号.

用标准库 urllib 而不是 requests: requests 会多付 150ms 导入时间, 而这个模块在软件
启动时就被导入, 只为一个下载功能不划算.
"""

import hashlib
import os
import time
import urllib.request

from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import QCoreApplication as QC

from app.core import model_assets
from app.core.log import write_log

CHUNK = 1 << 20
_TIMEOUT = 30
_REPORT_INTERVAL = 0.1
_HASH_CHUNK = 1 << 22


class ModelDownloader(QThread):
    """
    串行下载多个权重, 支持取消与断点续传.
    每个文件先落到 <名字>.part, 校验通过才改名成正式文件, 避免半截文件被当成可用权重.
    """

    progress = Signal(str, int, int, float)   # 文件名, 已完成字节, 总字节, 字节/秒
    verifying = Signal(str)                   # 文件名(正在校验)
    one_done = Signal(str)
    one_failed = Signal(str, str)             # 文件名, 业务语言原因
    all_finished = Signal(bool)               # 是否全部成功

    def __init__(self, assets, dest, parent=None):
        super().__init__(parent)
        self._assets = list(assets)
        # 权重根目录: 每个文件实际落在它按架构分出的子目录里
        self._dest = dest
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    # ---------- 主流程 ----------
    def run(self):
        ok = True
        for asset in self._assets:
            if self._cancelled:
                ok = False
                break
            if not self._fetch(asset):
                ok = False
                if self._cancelled:
                    break
        self.all_finished.emit(ok)

    def _fetch(self, asset):
        final = model_assets.path_of(asset, self._dest)
        part = final + ".part"
        try:
            os.makedirs(os.path.dirname(final), exist_ok=True)
        except OSError as exc:
            return self._fail(asset, QC.translate(
                "ModelDownloader",
                "权重目录不可写入, 请点\"更改\"换一个目录"), exc)

        if _size_of(final) == asset.nbytes:
            self.one_done.emit(asset.filename)
            return True
        if os.path.exists(final):
            # 大小不符说明是半截或已损坏的旧文件, 留着会被当成就绪
            write_log(QC.translate(
                "ModelDownloader",
                "权重文件大小不符, 丢弃重下: {}").format(final))
            _remove(final)

        done = _size_of(part)
        if done > asset.nbytes:
            _remove(part)
            done = 0
        headers = {"Range": "bytes={}-".format(done)} if done else {}
        write_log(QC.translate(
            "ModelDownloader",
            "开始下载权重 {} ({}, 已下载 {})").format(
            asset.filename, asset.desc, done))
        try:
            resp, start = self._open(asset, headers, done)
        except Exception as exc:
            write_log(QC.translate(
                "ModelDownloader",
                "下载权重失败 {}: {}").format(asset.filename, exc))
            return self._fail(asset, QC.translate(
                "ModelDownloader",
                "无法连接下载服务器, 请检查网络后重试"), exc)
        try:
            with resp:
                if not self._write(resp, part, asset, start):
                    return False
        except Exception as exc:
            return self._fail(asset, QC.translate(
                "ModelDownloader",
                "下载中断, 已保留进度, 可再次点击续传"), exc)

        if _size_of(part) != asset.nbytes:
            return self._fail(asset, QC.translate(
                "ModelDownloader",
                "下载不完整, 已保留进度, 可再次点击续传"), None)

        self.verifying.emit(asset.filename)
        got = _md5_of(part)
        if got != asset.md5:
            write_log(QC.translate(
                "ModelDownloader",
                "权重校验不通过 {}: 期望 {} 实际 {}").format(
                asset.filename, asset.md5, got))
            _remove(part)
            return self._fail(asset, QC.translate(
                "ModelDownloader",
                "文件校验未通过, 损坏文件已删除, 请重试"), None)
        try:
            os.replace(part, final)
        except OSError as exc:
            return self._fail(asset, QC.translate(
                "ModelDownloader",
                "写入权重目录失败, 请检查磁盘空间"), exc)
        write_log(QC.translate("ModelDownloader", "权重就绪: {}").format(final))
        self.one_done.emit(asset.filename)
        return True

    def _open(self, asset, headers, done):
        """发起请求, 返回 (响应对象, 起始字节)."""
        req = urllib.request.Request(asset.url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=_TIMEOUT)
        status = getattr(resp, "status", 200)
        if done and status != 206:
            # 服务端不支持续传: 从头下载, 否则拼出来的文件是坏的
            done = 0
        return resp, done

    def _write(self, resp, part, asset, start):
        mode = "ab" if start else "wb"
        done = start
        last = last_bytes = time.time()
        with open(part, mode) as f:
            while True:
                if self._cancelled:
                    write_log(QC.translate(
                        "ModelDownloader",
                        "下载已取消, 已下载部分保留以便续传: {}").format(
                        asset.filename))
                    return False
                block = resp.read(CHUNK)
                if not block:
                    break
                f.write(block)
                done += len(block)
                now = time.time()
                if now - last >= _REPORT_INTERVAL:
                    self.progress.emit(asset.filename, done, asset.nbytes,
                                       (done - last_bytes) / (now - last))
                    last, last_bytes = now, done
        self.progress.emit(asset.filename, done, asset.nbytes, 0.0)
        return True

    def _fail(self, asset, reason, exc):
        if exc is not None:
            write_log(QC.translate(
                "ModelDownloader",
                "权重下载异常 {}: {!r}").format(asset.filename, exc))
        self.one_failed.emit(asset.filename, reason)
        return False


def _size_of(path):
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def _remove(path):
    try:
        os.remove(path)
    except OSError:
        pass


def _md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(_HASH_CHUNK), b""):
            h.update(block)
    return h.hexdigest()
