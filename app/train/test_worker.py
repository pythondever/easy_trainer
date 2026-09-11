# -*- coding: utf-8 -*-
"""测试工作线程：以子进程方式运行 test_runner，转发日志/进度/结果。"""

import collections
import json
import os
import re
import subprocess
import sys
import tempfile
import time

from PySide6.QtCore import QThread, Signal

from app.core.utils import decode_text_bytes

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

TEST_RUNNER = "app.train.test_runner"
CLASSIFY_TEST_RUNNER = "app.train.classify_test_runner"


def _read_new_lines(path, start, final=False):
    """
    读子进程输出文件的新增行，返回 (行列表, 新偏移)。
    按字节读再逐行降级解码：子进程 stdout 的编码由它自己的环境决定（安装版从
    快捷方式启动时 Windows 上是 ANSI 码页 gbk），固定按 utf-8 解会把中文和表格
    字符全变成替换符。非 final 时只消费到最后一个换行，避免把写到一半的行当成
    完整行（那会让后续几个字节被当成新的一行）。
    """
    try:
        with open(path, "rb") as f:
            f.seek(start)
            chunk = f.read()
    except OSError:
        return [], start
    if not chunk:
        return [], start
    cut = len(chunk)
    if not final:
        nl = chunk.rfind(b"\n")
        if nl < 0:
            return [], start
        cut = nl + 1
    lines = [decode_text_bytes(part) for part in chunk[:cut].split(b"\n")]
    return lines, start + cut


class TestWorker(QThread):
    """运行一次测试（子进程），通过信号上报日志/进度/结果。"""

    log = Signal(str)
    progress = Signal(int, int)
    finished_ok = Signal(dict)           # test_runner 的 RESULT 内容
    failed = Signal(str)                 # traceback

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self._config = config
        self._proc = None
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True
        if self._proc is not None and self._proc.poll() is None:
            try:
                self._proc.terminate()
            except Exception:
                pass
            try:
                self._proc.kill()
            except Exception:
                pass

    def run(self):
        cfg_path = self._config["_cfg_path"]
        python = sys.executable
        trace_path = cfg_path + ".worker.log"

        def _trace(msg):
            try:
                with open(trace_path, "a", encoding="utf-8") as f:
                    f.write("[{}] {}\n".format(
                        time.strftime("%H:%M:%S"), msg))
            except Exception:
                pass

        _trace("run 开始")
        env = dict(os.environ)
        # PYTHONPATH 只对 Linux(venv) 生效; Windows embeddable 有 _pth 会忽略它,
        # 那边的安装根由 installer 写进 _pth
        env["PYTHONPATH"] = WORKSPACE
        env["PYTHONUNBUFFERED"] = "1"
        env["CUDA_MODULE_LOADING"] = "LAZY"
        module = (CLASSIFY_TEST_RUNNER
                  if self._config.get("task") == "classify" else TEST_RUNNER)
        # 不能用 -m: Cython 编出的 pyd 没有 code object, runpy 直接报
        # "No code object available", 只能 -c 显式导入再调 main()
        bootstrap = ("import sys; sys.path.insert(0, {!r});"
                     "from {} import main; main()").format(WORKSPACE, module)
        self.log.emit("[test-worker] 启动子进程: {} {}".format(
            python, module))
        out_fd, out_path = tempfile.mkstemp(suffix=".testout")
        os.close(out_fd)
        # 只把 fd 交给子进程, 读写都不经过这个文件对象, 编码无关
        out_file = open(out_path, "wb")
        try:
            self._proc = subprocess.Popen(
                [python, "-c", bootstrap, cfg_path],
                cwd=WORKSPACE, stdout=out_file, stderr=subprocess.STDOUT,
                env=env)
        except Exception as e:
            self.log.emit("[test-worker] 启动子进程失败: {}".format(e))
            out_file.close()
            try:
                os.remove(out_path)
            except Exception:
                pass
            self.failed.emit(f"启动测试进程失败: {e}")
            return
        _trace("子进程已启动 pid={}".format(self._proc.pid))
        self.log.emit("[test-worker] 子进程已启动 pid={}".format(self._proc.pid))
        last_lines = collections.deque(maxlen=200)
        _ansi_re = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
        _progress_re = re.compile(r"\[test\] 进度 (\d+)/(\d+)")
        pos = 0
        result_emitted = False
        _last_heartbeat = time.time()
        _bytes_read = [0]

        def _consume(new_lines):
            nonlocal result_emitted
            buf = []
            for line in new_lines:
                line = _ansi_re.sub("", line.rstrip("\r\n"))
                if not line:
                    continue
                last_lines.append(line)
                _bytes_read[0] += 1
                buf.append(line)
                m = _progress_re.search(line)
                if m:
                    self.progress.emit(int(m.group(1)), int(m.group(2)))
                if "[test] RESULT" in line:
                    try:
                        res = json.loads(line.split("RESULT ", 1)[1])
                    except Exception:
                        res = None
                    if isinstance(res, dict):
                        self.finished_ok.emit(res)
                        result_emitted = True
            if buf:
                self.log.emit("\n".join(buf))

        _trace("进入轮询循环")
        try:
            while not self._stop_flag:
                now = time.time()
                if now - _last_heartbeat >= 3:
                    _last_heartbeat = now
                    try:
                        fsz = os.path.getsize(out_path)
                    except Exception:
                        fsz = -1
                    _trace("轮询中: 文件={}B 已读{}行 子进程={}".format(
                        fsz, _bytes_read[0], self._proc.poll()))
                lines, pos = _read_new_lines(out_path, pos)
                if lines:
                    _consume(lines)
                if self._proc.poll() is not None:
                    break
                time.sleep(0.1)
        except Exception:
            import traceback
            _trace("轮询异常:\n" + traceback.format_exc())
        tail, pos = _read_new_lines(out_path, pos, final=True)
        if tail:
            _consume(tail)
        _trace("轮询结束 rc={}".format(self._proc.poll()))
        self.log.emit("[test-worker] 子进程退出 rc={}".format(
            self._proc.poll()))
        out_file.close()
        try:
            os.remove(out_path)
        except Exception:
            pass
        rc = self._proc.poll()
        if rc != 0 and not result_emitted:
            detail = "测试进程异常退出 (code={})\n\n--- 输出(尾部) ---\n{}".format(
                rc, "\n".join(last_lines))
            self.failed.emit(detail)
