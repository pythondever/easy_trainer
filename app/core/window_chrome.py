# -*- coding: utf-8 -*-
"""模态对话框的外观统一: 压暗底窗与深色系统标题栏.

QDialog 弹出来时和背后内容同深, 层次只能靠猜; Windows 的原生标题栏又是浅色,
和深色界面割裂. 这两件事与对话框里装什么无关, 所以收在应用级事件过滤器里统一
处理, 各处对话框不用各自改.
"""

import ctypes
import sys

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QDialog, QWidget

DIM_ALPHA = 108       # 底窗压暗程度: 0 不动 / 255 全黑
# DWMWA_USE_IMMERSIVE_DARK_MODE 的编号, 20H1 之前是 19, 之后是 20
_DWM_DARK = (20, 19)


def apply_dark_title_bar(widget):
    """把 Windows 的原生标题栏切成深色, 非 win32 或调用失败就静默跳过."""
    if sys.platform != "win32":
        return
    try:
        hwnd = int(widget.winId())
        flag = ctypes.c_int(1)
        for attr in _DWM_DARK:
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, attr, ctypes.byref(flag), ctypes.sizeof(flag)) == 0:
                return
    except Exception:
        # 老系统没有 dwmapi, 或控件还没建出原生窗口, 都不值得让界面起不来
        pass


class _Dim(QWidget):
    """盖在底窗上的半透明层: 只负责压暗, 鼠标事件穿透给底下自己处理."""

    def __init__(self, host):
        super().__init__(host)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setGeometry(host.rect())
        self.show()
        self.raise_()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, DIM_ALPHA))


class DialogChrome(QObject):
    """应用级事件过滤器: 模态对话框出现时压暗它的宿主窗口.

    按引用计数而不是标志位: 同一个宿主窗口上可能叠两层模态框(训练弹窗里再弹一个
    消息框), 谁先关都得留住另一层.
    """

    def __init__(self, app):
        super().__init__(app)
        self._dims = {}        # 宿主窗口 -> [遮罩, 引用计数]
        self._dimmed = set()   # 加过遮罩的对话框, 取消时靠它配对

    def eventFilter(self, obj, event):
        # PySide6 6.9.1 偶尔把 QStandardItem 当 event 投过来, 直接 event.type() 是空指针解引用
        if not isinstance(event, QEvent):
            return False
        kind = event.type()
        if isinstance(obj, QDialog):
            if kind == QEvent.Show:
                self._on_show(obj)
            elif kind in (QEvent.Hide, QEvent.Close):
                self._on_hide(obj)
        elif kind == QEvent.Resize:
            entry = self._dims.get(obj)
            if entry is not None:
                entry[0].setGeometry(obj.rect())
        elif kind == QEvent.Show and isinstance(obj, QWidget) and obj.isWindow():
            apply_dark_title_bar(obj)
        return False

    @staticmethod
    def _host_of(dialog):
        """对话框盖住的顶层窗口, 没有父窗口(独立弹窗)就返回 None."""
        parent = dialog.parentWidget()
        return None if parent is None else parent.window()

    def _on_show(self, dialog):
        apply_dark_title_bar(dialog)
        # exec() 在此之前就把模态设好了, 所以这时问 isModal() 是准的
        if not dialog.isModal():
            return
        host = self._host_of(dialog)
        if host is None or host is dialog:
            return
        self._dimmed.add(dialog)
        entry = self._dims.get(host)
        if entry is None:
            self._dims[host] = [_Dim(host), 1]
        else:
            entry[1] += 1

    def _on_hide(self, dialog):
        # 这里不能再问 isModal(): exec() 收尾已把模态还原, 遮罩会漏在屏幕上
        if dialog not in self._dimmed:
            return
        self._dimmed.discard(dialog)
        host = self._host_of(dialog)
        entry = self._dims.get(host)
        if entry is None:
            return
        entry[1] -= 1
        if entry[1] <= 0:
            self._dims.pop(host)
            entry[0].hide()
            entry[0].deleteLater()
