# -*- coding: utf-8 -*-
"""统一消息框 + 进度对话框（深色主题，与 app QSS 一致）。"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QDialog, QMessageBox, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QProgressBar)


_BTN_QSS = """
QPushButton {
    background-color: #2a2e38; color: #e8eaf0; border: none;
    border-radius: 6px; padding: 6px 18px; font-size: 13px;
}
QPushButton:hover { background-color: #343a48; }
"""


class MessageBox:
    """统一消息框静态封装：warning / information / question / critical。"""

    @staticmethod
    def _show(icon, title, text, parent=None, buttons=None):
        box = QMessageBox(parent)
        box.setWindowTitle(title)
        box.setText(text)
        box.setIcon(icon)
        if buttons:
            for btn, role in buttons:
                box.addButton(btn, role)
        else:
            box.addButton(QMessageBox.Ok)
        box.exec()
        return box.clickedButton()

    @staticmethod
    def warning(parent, title, text):
        MessageBox._show(QMessageBox.Warning, title, text, parent)

    @staticmethod
    def information(parent, title, text):
        MessageBox._show(QMessageBox.Information, title, text, parent)

    @staticmethod
    def critical(parent, title, text):
        MessageBox._show(QMessageBox.Critical, title, text, parent)

    @staticmethod
    def question(parent, title, text, default_yes=True):
        """返回 True=是 / False=否。"""
        box = QMessageBox(parent)
        box.setWindowTitle(title)
        box.setText(text)
        box.setIcon(QMessageBox.Question)
        yes_btn = box.addButton("是", QMessageBox.YesRole)
        no_btn = box.addButton("否", QMessageBox.NoRole)
        box.setDefaultButton(yes_btn if default_yes else no_btn)
        box.exec()
        return box.clickedButton() is yes_btn

    @staticmethod
    def choose(parent, title, text, buttons, informative=""):
        """多按钮选择框：buttons=[(文本, 角色), ...]，返回点击按钮文本；关闭返回 None。"""
        box = QMessageBox(parent)
        box.setWindowTitle(title)
        box.setText(text)
        if informative:
            box.setInformativeText(informative)
        box.setIcon(QMessageBox.Question)
        for b, role in buttons:
            box.addButton(b, role)
        box.exec()
        clicked = box.clickedButton()
        return clicked.text() if clicked is not None else None


class ProgressDialog(QDialog):
    """带进度条 + 文本 + 可选取消按钮的模态对话框（导出/批量删除长任务）。"""

    def __init__(self, title, text, parent=None, maximum=100, cancellable=True):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedWidth(430)
        self._cancelled = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        self._text_lbl = QLabel(text)
        self._text_lbl.setStyleSheet("color: #e8eaf0; font-size: 13px;")
        self._text_lbl.setWordWrap(True)
        layout.addWidget(self._text_lbl)

        self._bar = QProgressBar()
        self._bar.setRange(0, maximum)
        self._bar.setValue(0)
        self._bar.setStyleSheet(
            "QProgressBar { background: #2a2e38; border: none; border-radius: 4px;"
            " height: 10px; color: transparent; }"
            " QProgressBar::chunk { background: #5b8cff; border-radius: 4px; }")
        layout.addWidget(self._bar)

        if cancellable:
            row = QHBoxLayout()
            row.addStretch(1)
            self._cancel_btn = QPushButton("取消")
            self._cancel_btn.setStyleSheet(_BTN_QSS)
            self._cancel_btn.clicked.connect(self._on_cancel)
            row.addWidget(self._cancel_btn)
            layout.addLayout(row)
        else:
            self._cancel_btn = None

        # 立即显示并置顶避免 processEvents 时还没 show 导致用户看不到进度
        self.show()
        self.raise_()
        self.activateWindow()

    def set_progress(self, value, text=None):
        self._bar.setValue(value)
        if text is not None:
            self._text_lbl.setText(text)
        QApplication.processEvents()

    def set_text(self, text):
        self._text_lbl.setText(text)
        QApplication.processEvents()

    def is_cancelled(self):
        return self._cancelled

    def _on_cancel(self):
        self._cancelled = True
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.setText("取消中…")
