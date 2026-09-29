# -*- coding: utf-8 -*-
"""
弹窗确认/取消按钮: 统一用 resources 图标
"""

import os
from functools import lru_cache

from PySide6.QtCore import QSize, Qt
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import QIcon, QPainter, QPixmap, QColor
from PySide6.QtWidgets import QPushButton

from app.core import theme
from app.core.utils import project_root

CONFIRM_ICON = "确定.png"
REJECT_ICON = "取消.png"

ICON_SIZE = 16
BTN_WIDTH = 84
BTN_HEIGHT = theme.BTN_HEIGHT   # 与 style.qss 的 h_ctrl_dialog 同源

# 调用方传进来的文案可能已经是英文了(界面语言切换后), 两套都要认
CONFIRM_TEXTS = ("确定", "确认", "是", "好", "ok", "yes", "导出", "保存", "应用",
                 "ok", "confirm", "yes", "save", "apply", "export")
REJECT_TEXTS = ("取消", "否", "关闭", "no", "cancel", "退出",
                "no", "cancel", "close", "dismiss")

# 深色底上的图标色
REJECT_COLOR = theme.hexof("text_dim")
CONFIRM_COLOR = theme.hexof("text_strong")


@lru_cache(maxsize=64)
def _icon_path(name):
    p = os.path.join(project_root(), "resources", name)
    return p if os.path.exists(p) else ""


def resource_icon(name):
    """
    绝对路径取 resources 图标
    """
    path = _icon_path(name)
    return QIcon(path) if path else QIcon()


@lru_cache(maxsize=128)
def _tinted(path, color):
    """
    按颜色染色的图标.
    """
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
    """返回 confirm / reject / '', 最后一种表示保持原样."""
    t = (text or "").strip().lower()
    if t in CONFIRM_TEXTS:
        return "confirm"
    if t in REJECT_TEXTS:
        return "reject"
    return ""


def apply_icon(btn, text, tooltip=None):
    """归不了类的按钮(如"覆盖")保持纯文字, 不动它.

    图标放左侧、文字保留: 早先版本用图标顶掉文字, 弹窗里只剩 ✓ / ✕,
    和右上角的关闭 ✕ 撞脸又没法看出是"确定"还是"取消".
    """
    kind = classify(text)
    if not kind:
        return btn
    if kind == "confirm":
        path = _icon_path(CONFIRM_ICON)
        color = CONFIRM_COLOR
    else:
        path = _icon_path(REJECT_ICON)
        color = REJECT_COLOR
    if not path:
        return btn
    btn.setText(text)
    btn.setIcon(_tinted(path, color))
    btn.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
    if kind == "confirm":
        roles = (btn.property("class") or "").split()
        # danger 是调用方指定的破坏性语义, 不能被"确定"文案顶成主色
        if not {"primary", "danger"} & set(roles):
            btn.setProperty("class", " ".join(roles + ["primary"]))
    if tooltip:
        btn.setToolTip(tooltip)
    return btn


def confirm_button(text=None, parent=None):
    btn = QPushButton(parent)
    btn.setObjectName("msgBtn")
    return apply_icon(btn, text or QC.translate("DialogButtons", "确定"))


def reject_button(text=None, parent=None):
    btn = QPushButton(parent)
    btn.setObjectName("msgBtn")
    return apply_icon(btn, text or QC.translate("DialogButtons", "取消"))


def add_ok_cancel(button_row, on_accept, on_reject=None,
                  ok_text=None, cancel_text=None):
    """Windows 习惯: 确定在左."""
    ok = confirm_button(ok_text)
    ok.setDefault(True)
    ok.clicked.connect(on_accept)
    button_row.addWidget(ok)
    if on_reject is not None:
        cancel = reject_button(cancel_text)
        cancel.clicked.connect(on_reject)
        button_row.addWidget(cancel)
    return ok
