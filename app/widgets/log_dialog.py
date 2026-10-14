# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog

from app.core.log import LOG_FILE, MAX_LINES, register_log_dialog
from app.widgets.dialog_fit import fit_dialog_height
from ui.log import Ui_LogDialog


class LogDialog(QDialog):
    """
    日志查看对话框直接写入 textEdit; 段落数上限由文档自己维护.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)
        # 走 .ui 的 windowTitle(带翻译), 代码里再写一遍硬编码会把翻译覆盖掉
        self.setWindowTitle(self.tr("日志"))
        self.ui.textEdit.setReadOnly(True)
        # 段落上限必须交给文档维护: 手动逐段删的代价随段落数线性增长(一次几千段=十几秒)
        self.ui.textEdit.document().setMaximumBlockCount(MAX_LINES)
        self.ui.clr_log_btn.clicked.connect(self.clear_log)
        self._load_history()
        register_log_dialog(self)
        fit_dialog_height(self)

    def _load_history(self):
        try:
            with open(LOG_FILE, encoding="utf-8") as f:
                lines = f.read().splitlines()
            for line in lines[-MAX_LINES:]:
                self.ui.textEdit.append(line)
        except FileNotFoundError:
            pass

    def append(self, line):
        """直接写入 textEdit; 超出上限由文档自动丢最老段落."""
        self.ui.textEdit.append(line)

    def clear_log(self):
        self.ui.textEdit.clear()
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write("")
        except OSError:
            pass
