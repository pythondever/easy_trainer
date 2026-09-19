# -*- coding: utf-8 -*-
"""导入对话框的实时统计线程: 数图像张数与其中已标注的张数.

判定"已标注"要逐个解析标签文件, 上万张图同步跑会把对话框冻住一两秒,
所以只把这段数字扫描丢进后台.
"""
from PySide6.QtCore import QThread, Signal

from app.core.label_utils import count_images_labeled


class ImportScanTask(QThread):
    """扫描完发 (total, labeled); 被取消或目录失效则什么都不发."""

    scanned_signal = Signal(int, int)

    def __init__(self, image_path, label_path="", fmt="", parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.label_path = label_path
        self.fmt = fmt
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        result = count_images_labeled(self.image_path, self.label_path, self.fmt,
                                      cancelled=lambda: self._cancel)
        if result is not None and not self._cancel:
            self.scanned_signal.emit(result[0], result[1])
