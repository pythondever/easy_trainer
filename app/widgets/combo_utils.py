# -*- coding: utf-8 -*-
"""
下拉框统一装扮: 文本居中 + 点击框内任意位置展开.
"""

from PySide6.QtCore import QEvent, QObject, Qt, QTimer


class ClickToPopupFilter(QObject):
    """点击下拉框(或其 lineEdit)任意位置就展开下拉."""

    def __init__(self, combo, parent=None):
        super().__init__(parent)
        self._combo = combo

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            # 事件过滤器跑在 Qt 的禁用判定之前, 不自己挡一下的话置灰的下拉照样能点开
            if not self._combo.isEnabled():
                return True
            QTimer.singleShot(0, self._combo.showPopup)
            return True
        return False


def style_combo(combo, filters, parent=None):
    """
    文本居中 + 点击任意位置展开; 过滤器追加进调用方的 filters 保引用.
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
