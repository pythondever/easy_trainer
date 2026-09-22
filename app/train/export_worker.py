# -*- coding: utf-8 -*-
"""导出任务线程: ONNX 转换耗时较长, 放线程里跑避免卡住界面."""

import os
import sys
import traceback

from PySide6.QtCore import QThread, Signal

from app.train import onnx_export

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


class OnnxExportWorker(QThread):

    stage = Signal(str)
    finished_ok = Signal(str)      # onnx 路径
    failed = Signal(str)

    def __init__(self, model_path, task, out_file, img_size=0, family="",
                 parent=None):
        super().__init__(parent)
        self._model_path = model_path
        self._task = task
        self._out_file = out_file
        self._img_size = img_size
        self._family = family

    def run(self):
        try:
            path = onnx_export.export_onnx(
                self._model_path, self._task, self._out_file,
                img_size=self._img_size, family=self._family,
                log=self.stage.emit)
            self.finished_ok.emit(path)
        except Exception as e:
            self.failed.emit("{}\n{}".format(e, traceback.format_exc()))


class ReportWorker(QThread):
    """评估报告要逐张重绘漏检/误检的原图, 6500 万像素的图单张就要 1~3 秒,
    整本的耗时是分钟级, 放 UI 线程会让窗口彻底不响应."""

    done = Signal(str)        # pdf 路径, 没内容可写时为空串
    failed = Signal(str)

    def __init__(self, res, out_pdf=None, per_class_limit=None, parent=None):
        super().__init__(parent)
        self._res = res
        self._out_pdf = out_pdf
        self._limit = per_class_limit

    def run(self):
        try:
            # matplotlib 较重, 只在真的要出报告时才导入
            from app.train.test_report import build_report
            kwargs = {}
            if self._out_pdf:
                kwargs["out_pdf"] = self._out_pdf
            if self._limit is not None:
                kwargs["per_class_limit"] = self._limit
            self.done.emit(build_report(self._res, **kwargs) or "")
        except Exception as exc:
            self.failed.emit("{}\n\n{}".format(exc, traceback.format_exc()))


def examples_dir():
    """示例目录: 源码运行时在项目根, PyInstaller 打包后在 _MEIPASS 下."""
    for base in (getattr(sys, "_MEIPASS", ""), WORKSPACE):
        if not base:
            continue
        cand = os.path.join(base, "examples")
        if os.path.isdir(cand):
            return cand
    return ""
