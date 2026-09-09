# -*- coding: utf-8 -*-
"""导出任务线程：ONNX 转换耗时较长，放线程里跑避免卡住界面。"""

import os
import sys
import traceback

from PySide6.QtCore import QThread, Signal

from app.train import onnx_export

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


class OnnxExportWorker(QThread):
    """把 .pth 转成 .onnx。"""

    stage = Signal(str)
    finished_ok = Signal(str)      # onnx 路径
    failed = Signal(str)

    def __init__(self, model_path, task, out_file, img_size=0, parent=None):
        super().__init__(parent)
        self._model_path = model_path
        self._task = task
        self._out_file = out_file
        self._img_size = img_size

    def run(self):
        try:
            path = onnx_export.export_onnx(
                self._model_path, self._task, self._out_file,
                img_size=self._img_size, log=self.stage.emit)
            self.finished_ok.emit(path)
        except Exception as e:
            self.failed.emit("{}\n{}".format(e, traceback.format_exc()))


def examples_dir():
    """示例目录：源码运行时在项目根，PyInstaller 打包后在 _MEIPASS 下。"""
    for base in (getattr(sys, "_MEIPASS", ""), WORKSPACE):
        if not base:
            continue
        cand = os.path.join(base, "examples")
        if os.path.isdir(cand):
            return cand
    return ""
