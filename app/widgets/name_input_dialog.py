from PySide6.QtWidgets import QDialog

from ui.input_name import Ui_NameInputDialog


class NameInputDialog(QDialog):
    """通用「输入名称」弹窗：项目/数据集的新建与改名共用一套样式。"""

    def __init__(self, parent=None, title="输入名称", preset="", placeholder="请输入名称"):
        super().__init__(parent)
        self.ui = Ui_NameInputDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.title_label.setText(title)
        self.ui.name_edit.setPlaceholderText(placeholder)
        if preset:
            self.ui.name_edit.setText(preset)
            self.ui.name_edit.selectAll()
        self.ui.cancel_btn.clicked.connect(self.reject)
        self.ui.ok_btn.clicked.connect(self.accept)
        # 回车直接确认,与主界面操作习惯一致
        self.ui.name_edit.returnPressed.connect(self.accept)
        self.ui.name_edit.setFocus()

    @staticmethod
    def get_name(parent=None, title="输入名称", preset="", placeholder="请输入名称"):
        """弹出并返回 (name, ok);ok=False 表示用户取消。"""
        dlg = NameInputDialog(parent, title, preset, placeholder)
        dlg.exec()
        return dlg.ui.name_edit.text().strip(), dlg.result() == QDialog.Accepted
