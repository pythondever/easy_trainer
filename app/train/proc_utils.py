# -*- coding: utf-8 -*-
"""子进程收尾, 启动表达式与 worker 公共底座: 训练/测试共用一份, 避免逻辑分叉."""

import os

from PySide6.QtCore import QThread

try:
    import psutil
except ImportError:
    psutil = None

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def runner_bootstrap(module):
    """
    子进程启动用的 -c 表达式.
    不能用 -m: Cython 编出的 pyd/.so 没有 code object, runpy 会直接报
    "No code object available", 只能 -c 显式导入再调 main(). 而 import app
    又依赖安装根在 sys.path 上 - Windows embeddable 有 ._pth 时会忽略
    PYTHONPATH 与 cwd, 所以这里显式插进去.
    """
    return ("import sys; sys.path.insert(0, {!r});"
            "from {} import main; main()").format(WORKSPACE, module)


def kill_process_tree(proc):
    """
    终止子进程及其孙进程(proc 已退出则直接返回).
    只 kill 直接子进程不够: rf-detr 的 dataloader(num_workers>0) 会 fork
    孙进程, 主进程被杀后它们变孤儿继续占显存, 下一个训练会直接 OOM.
    调用方必须在子进程还活着的时候调它 - 父进程退出后就没法按 pid 找回
    已被 reparent 的孙进程了.
    """
    if proc is None or proc.poll() is not None:
        return
    if psutil is not None:
        try:
            parent = psutil.Process(proc.pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.kill()
                except Exception:
                    pass
            try:
                parent.kill()
            except Exception:
                pass
            psutil.wait_procs(children + [parent], timeout=5)
            return
        except Exception:
            pass
    try:
        proc.terminate()
    except Exception:
        pass
    try:
        proc.kill()
    except Exception:
        pass


class SubprocessWorker(QThread):
    """
    跑子进程的 worker 的公共部分: 配置快照, 进程句柄, 停止标志.
    信号留给各自的子类声明 - 训练要报指标, 测试不报.
    """

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self._config = config
        self._proc = None
        self._stop_flag = False

    def stop(self):
        """请求停止: 置标志并终止子进程及其孙进程."""
        self._stop_flag = True
        self._kill_proc()

    def _kill_proc(self):
        """终止子进程及其孙进程; 不动 _stop_flag(监控循环收尾也要用)."""
        kill_process_tree(self._proc)
