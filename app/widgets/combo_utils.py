# -*- coding: utf-8 -*-
"""下拉框统一装扮: 文本居中 + 点击框内任意位置展开.

训练对话框, 测试对话框, 指标对话框原先各有一份实现, 改一处漏一处的风险
比代码量本身更要紧.
"""

from PySide6.QtCore import QEvent, QObject, Qt, QTimer


class ClickToPopupFilter(QObject):
    """点击下拉框(或其 lineEdit)任意位置 → 展开下拉."""

    def __init__(self, combo, parent=None):
        super().__init__(parent)
        self._combo = combo

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            QTimer.singleShot(0, self._combo.showPopup)
            return True
        return False


def style_combo(combo, filters, parent=None):
    """文本居中 + 点击任意位置展开; 过滤器追加进调用方的 filters 保引用.

    parent 传对话框自身的场合: 对话框设了 WA_DeleteOnClose 时过滤器必须
    随之销毁, 否则延时弹出的 singleShot 会打到已删除的 combo 上.
    """
    combo.setEditable(True)
    combo.setFocusPolicy(Qt.StrongFocus)
    le = combo.lineEdit()
    le.setObjectName("multiComboLineEdit")
    le.setReadOnly(True)
    le.setAlignment(Qt.AlignHCenter)
    f = ClickToPopupFilter(combo, parent)
    combo.installEventFilter(f)
    le.installEventFilter(f)
    filters.append(f)
    return combo
