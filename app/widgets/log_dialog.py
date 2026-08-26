# -*- coding: utf-8 -*-
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QDialog

from app.core.log import LOG_FILE, MAX_LINES, register_log_dialog
from ui.log import Ui_LogDialog


class LogDialog(QDialog):
    """
    日志查看对话框直接写入 textEdit。
    超过 MAX_LINES(1000)条自动删除最老的再追加最新的。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("日志")
        self.ui.textEdit.setReadOnly(True)
        self.ui.clr_log_btn.clicked.connect(self.clear_log)
        self._load_history()
        register_log_dialog(self)

    def _load_history(self):
        try:
            with open(LOG_FILE, encoding="utf-8") as f:
                lines = f.read().splitlines()
            for line in lines[-MAX_LINES:]:
                self.ui.textEdit.append(line)
            self._trim()
        except FileNotFoundError:
            pass

    def append(self, line):
        """直接写入 textEdit；超 1000 行删除最老。"""
        edit = self.ui.textEdit
        edit.append(line)
        self._trim()

    def _trim(self):
        """超过 MAX_LINES 行删除最老的。"""
        edit = self.ui.textEdit
        while edit.document().blockCount() > MAX_LINES:
            c = edit.textCursor()
            c.movePosition(QTextCursor.Start)
            c.select(QTextCursor.LineUnderCursor)
            c.removeSelectedText()
            c.deleteChar()   # 删除行尾换行

    def clear_log(self):
        self.ui.textEdit.clear()
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write("")
        except OSError:
            pass
