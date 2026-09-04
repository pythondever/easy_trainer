# -*- coding: utf-8 -*-
"""弹窗确认/取消按钮：统一用 resources 图标，不再各写各的文字。

纯图标按钮一律补 tooltip，否则用户只能靠猜。
"""

import os

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap, QColor
from PySide6.QtWidgets import QPushButton

from app.core.utils import project_root

CONFIRM_ICON = "确定.png"
REJECT_ICON = "取消.png"

ICON_SIZE = 26
BTN_WIDTH = 56
BTN_HEIGHT = 36  # 与 style.qss 的 QDialog 控件统一高度一致（CONTROL_H）

CONFIRM_TEXTS = ("确定", "确认", "是", "好", "ok", "yes", "导出", "保存", "应用")
REJECT_TEXTS = ("取消", "否", "关闭", "no", "cancel", "退出")

# 深色底上的图标色
REJECT_COLOR = "#9aa3b5"
CONFIRM_COLOR = "#ffffff"  # 确认按钮一律蓝底，绿勾在上面对比度不够


def _icon_path(name):
    p = os.path.join(project_root(), "resources", name)
    return p if os.path.exists(p) else ""


def _tinted(path, color, size=ICON_SIZE):
    src = QPixmap(path)
    if src.isNull():
        return QIcon()
    out = QPixmap(src.size())
    out.fill(Qt.transparent)
    painter = QPainter(out)
    painter.drawPixmap(0, 0, src)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(out.rect(), QColor(color))
    painter.end()
    return QIcon(out)


def classify(text):
    """返回 confirm / reject / ''，最后一种表示保持原样。"""
    t = (text or "").strip().lower()
    if t in CONFIRM_TEXTS:
        return "confirm"
    if t in REJECT_TEXTS:
        return "reject"
    return ""


def apply_icon(btn, text, tooltip=None):
    """归不了类的按钮（如"覆盖"）保持文字，不动它。"""
    kind = classify(text)
    if not kind:
        return btn
    if kind == "confirm":
        path = _icon_path(CONFIRM_ICON)
        color = CONFIRM_COLOR
        btn.setProperty("class", "primary")
    else:
        path = _icon_path(REJECT_ICON)
        color = REJECT_COLOR
    if not path:
        return btn
    btn.setText("")
    btn.setIcon(_tinted(path, color))
    btn.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
    prev = btn.property("class") or ""
    btn.setProperty("class", (prev + " " if prev else "") + "iconBtn")
    btn.setFixedSize(BTN_WIDTH, BTN_HEIGHT)
    btn.setToolTip(tooltip or text)
    return btn


def confirm_button(text="确定", parent=None):
    btn = QPushButton(parent)
    btn.setObjectName("msgBtn")
    return apply_icon(btn, text)


def reject_button(text="取消", parent=None):
    btn = QPushButton(parent)
    btn.setObjectName("msgBtn")
    return apply_icon(btn, text)


def add_ok_cancel(button_row, on_accept, on_reject=None,
                  ok_text="确定", cancel_text="取消"):
    """Windows 习惯：确定在左。"""
    ok = confirm_button(ok_text)
    ok.setDefault(True)
    ok.clicked.connect(on_accept)
    button_row.addWidget(ok)
    if on_reject is not None:
        cancel = reject_button(cancel_text)
        cancel.clicked.connect(on_reject)
        button_row.addWidget(cancel)
    return ok
