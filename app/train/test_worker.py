# -*- coding: utf-8 -*-
"""测试工作线程：以子进程方式运行 test_runner，转发日志/进度/结果。"""

import collections
import json
import os
import queue
import re
import subprocess
import sys
import tempfile
import threading
import time

from PySide6.QtCore import QThread, Signal

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
TEST_RUNNER = os.path.join(WORKSPACE, "app", "train", "test_runner.py")
CLASSIFY_TEST_RUNNER = os.path.join(WORKSPACE, "app", "train",
                                    "classify_test_runner.py")


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
        env.pop("PYTHONPATH", None)
        env["PYTHONUNBUFFERED"] = "1"
        env["CUDA_MODULE_LOADING"] = "LAZY"
        runner = (CLASSIFY_TEST_RUNNER
                  if self._config.get("task") == "classify" else TEST_RUNNER)
        self.log.emit("[test-worker] 启动子进程: {} {} {}".format(
            python, runner, cfg_path))
        out_fd, out_path = tempfile.mkstemp(suffix=".testout")
        os.close(out_fd)
        out_file = open(out_path, "w", encoding="utf-8", errors="replace")
        try:
            self._proc = subprocess.Popen(
                [python, runner, cfg_path],
                cwd=WORKSPACE, stdout=out_file, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace", env=env)
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
                try:
                    with open(out_path, "r", encoding="utf-8",
                              errors="replace") as f:
                        f.seek(pos)
                        new = f.readlines()
                        pos = f.tell()
                except Exception:
                    new = []
                if new:
                    _consume(new)
                if self._proc.poll() is not None:
                    break
                time.sleep(0.1)
        except Exception:
            import traceback
            _trace("轮询异常:\n" + traceback.format_exc())
        try:
            with open(out_path, "r", encoding="utf-8",
                      errors="replace") as f:
                f.seek(pos)
                _consume(f.readlines())
        except Exception:
            pass
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
