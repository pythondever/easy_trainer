# -*- coding: utf-8 -*-
"""
显卡探测: 子进程跑 torch 查询 + 后台线程填设备下拉.

探测必须隔一层子进程: torch 的加载在个别机器上是硬崩(非法指令/访问冲突),
Python 接不住那种崩, 留在界面进程里就是整个窗口跟着消失, 而打包后跑的
是 pythonw, 连提示都没有.
"""

import json
import os
import subprocess
import sys
import tempfile

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtCore import QT_TRANSLATE_NOOP

from app.core.log import write_log

PROBING_TEXT = QT_TRANSLATE_NOOP("TrainDialog", "正在检测显卡...")
PROBE_FAILED_TEXT = QT_TRANSLATE_NOOP(
    "TrainDialog", "本机训练库(torch)加载失败, 只能使用 CPU; 训练很可能起不来")

_DEVICES = None
_DEVICES_ERROR = ""       # torch 探测失败的原因(空 = 正常)


# 子进程侧脚本: 不依赖工程内任何代码, 结果写进 argv[1] 指定的 json.
DEVICE_PROBE_SCRIPT = """
import json, sys

out = {"ok": True, "err": "", "devices": []}
try:
    import torch
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            try:
                # 下拉宽度放不下全名, 而 ElideLeft 先吃掉的正是前缀, 反倒把型号挤没
                name = torch.cuda.get_device_name(i).removeprefix("NVIDIA ")
                total = torch.cuda.get_device_properties(i).total_memory
                text = "{} ({:.0f} GB)".format(name, total / 1024 ** 3)
            except Exception:
                text = "GPU {}".format(i)
            out["devices"].append([text, "cuda:{}".format(i)])
except BaseException as exc:
    # Windows 上 DLL 加载失败抛的是 OSError 而不是 ImportError, 所以连 BaseException 一起收
    out["ok"] = False
    out["err"] = "{}: {}".format(type(exc).__name__, exc)
out["devices"].append(["CPU", "CPU"])
with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(out, f)
"""

PROBE_TIMEOUT = 180        # 含 import torch, 机械盘老机器上要几十秒
_CREATE_NO_WINDOW = 0x08000000


def _probe_in_subprocess():
    """
    跑一次探测子进程, 返回 (设备列表, 失败原因).
    结果走临时文件而不是管道: 打包后宿主是 pythonw.exe, sys.stdout 是 None, 管道里拿不到东西.
    """
    fd, path = tempfile.mkstemp(suffix=".json", prefix="devprobe_")
    os.close(fd)
    try:
        proc = subprocess.run(
            [sys.executable, "-c", DEVICE_PROBE_SCRIPT, path],
            cwd=tempfile.gettempdir(), capture_output=True,
            creationflags=_CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            timeout=PROBE_TIMEOUT)
        try:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, ValueError):
            # 硬崩时临时文件是空的, 只有退出码能当线索
            return ([("CPU", "CPU")],
                    "探测进程异常退出(0x%08X)" % (proc.returncode & 0xFFFFFFFF))
        devices = [(str(t), str(v)) for t, v in payload.get("devices") or []]
        err = "" if payload.get("ok") else str(payload.get("err") or "探测失败")
        return devices or [("CPU", "CPU")], err
    except (OSError, subprocess.SubprocessError) as exc:
        return [("CPU", "CPU")], "探测进程起不来: {}".format(exc)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def collect_devices():
    """
    [(显示名, 设备串)]: 列表显示 GPU 型号, 实际下发的是 cuda:0 这类设备串.
    探测放子进程做, 结果缓存, 同一进程只探一次.
    """
    global _DEVICES, _DEVICES_ERROR
    if _DEVICES is None:
        _DEVICES, _DEVICES_ERROR = _probe_in_subprocess()
        if _DEVICES_ERROR:
            write_log("设备探测未通过: {}".format(_DEVICES_ERROR))
    return list(_DEVICES)


class _DeviceProbe(QThread):
    """后台探测显卡. 探测要走子进程(见 collect_devices), 同步做会把弹窗卡住."""

    ready = Signal(list)

    def run(self):
        try:
            self.ready.emit(collect_devices())
        except Exception:
            self.ready.emit([("CPU", "CPU")])


_PROBES = []                    # 运行中的探测线程, 防止被 GC


def fill_device_items(combo, devices):
    combo.clear()
    for text, value in devices:
        combo.addItem(text, value)
        combo.setItemData(combo.count() - 1, text, Qt.ToolTipRole)


def fill_device_combo_async(dialog, combo, start_button):
    """
    设备下拉先填占位值, 后台探测完回调 dialog._on_devices_ready(devices).
    就绪前禁掉下拉与开始按钮, 免得占位值 CPU 被当成用户选择跑出去.
    """
    combo.clear()
    combo.addItem(QC.translate("TrainDialog", PROBING_TEXT), "CPU")
    if _DEVICES is not None:        # 本进程已探测过, 不用再起线程
        dialog._on_devices_ready(_DEVICES)
        return
    combo.setEnabled(False)
    start_button.setEnabled(False)
    # 前一个弹窗关掉后探测可能还在跑, 搭它的车, 免得再导一次 torch
    probe = next((p for p in _PROBES if p.isRunning()), None)
    if probe is None:
        probe = _DeviceProbe()
        _PROBES.append(probe)
        probe.finished.connect(
            lambda: _PROBES.remove(probe) if probe in _PROBES else None)
        probe.start()
    probe.ready.connect(dialog._on_devices_ready)
    dialog._device_probe = probe


def detach_device_probe(dialog):
    """关窗时摘掉探测回调. 线程让它自己跑完, 关窗不该等它那 2s."""
    probe = getattr(dialog, "_device_probe", None)
    if probe is None or not probe.isRunning():
        return
    try:
        probe.ready.disconnect(dialog._on_devices_ready)
    except (RuntimeError, TypeError):
        pass
