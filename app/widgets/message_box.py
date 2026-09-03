# -*- coding: utf-8 -*-
"""统一消息框 + 进度对话框（深色主题，自绘无边框窗口，与 app QSS 一致）。"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QProgressBar)
from PySide6.QtWidgets import QGraphicsDropShadowEffect

from app.widgets.dialog_buttons import apply_icon


# 图标: (符号, 颜色)
_ICONS = {
    "warning": ("⚠", "#f5b84b"),
    "information": ("ⓘ", "#4f7dff"),
    "critical": ("✕", "#f2645a"),
    "question": ("?", "#4f7dff"),
}


class _FramelessBox(QDialog):
    """自绘无边框弹窗: 圆角+阴影+自绘标题栏, 支持拖拽移动。"""

    def __init__(self, title, icon_key, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setMinimumWidth(380)

        # 外层透明容器(放圆角+阴影)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self._frame = QFrame(self)
        self._frame.setObjectName("msgFrame")
        outer.addWidget(self._frame)

        # 阴影
        shadow = QGraphicsDropShadowEffect(self._frame)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 4)
        from PySide6.QtGui import QColor
        shadow.setColor(QColor(0, 0, 0, 140))
        self._frame.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self._frame)
        layout.setContentsMargins(24, 14, 24, 20)
        layout.setSpacing(0)

        # ---- 标题栏: 标题 + 关闭按钮 ----
        title_row = QHBoxLayout()
        self._title_lbl = QLabel(title)
        self._title_lbl.setObjectName("msgTitle")
        title_row.addWidget(self._title_lbl)
        title_row.addStretch(1)
        close_btn = QPushButton("✕")
        close_btn.setObjectName("msgClose")
        close_btn.setFixedSize(28, 24)
        close_btn.clicked.connect(self.reject)
        title_row.addWidget(close_btn, 0, Qt.AlignTop)
        layout.addLayout(title_row)
        layout.addSpacing(10)

        # ---- 内容区: 图标 + 文本 ----
        body = QHBoxLayout()
        body.setSpacing(16)
        sym, color = _ICONS.get(icon_key, ("ⓘ", "#4f7dff"))
        self._icon_lbl = QLabel(sym)
        self._icon_lbl.setStyleSheet(
            "color: {}; font-size: 30px; font-weight: 700;".format(color))
        self._icon_lbl.setFixedWidth(44)
        self._icon_lbl.setAlignment(Qt.AlignCenter)
        body.addWidget(self._icon_lbl, 0, Qt.AlignVCenter)
        self._text_lbl = QLabel("")
        self._text_lbl.setObjectName("msgText")
        self._text_lbl.setWordWrap(True)
        self._text_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        body.addWidget(self._text_lbl, 1)
        layout.addLayout(body)
        layout.addSpacing(18)

        # ---- 按钮区 ----
        self._btn_row = QHBoxLayout()
        self._btn_row.addStretch(1)
        self._btn_row.setSpacing(8)
        layout.addLayout(self._btn_row)

        # 拖拽移动
        self._drag_pos = None

    # ---- 拖拽 ----
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)

    # ---- 按钮 ----
    def _add_button(self, text, role, default=False):
        btn = QPushButton(text)
        btn.setObjectName("msgBtn")
        btn.setProperty("originText", text)
        if role == "primary":
            btn.setProperty("class", "primary")
        apply_icon(btn, text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: setattr(self, "_clicked", btn))
        btn.clicked.connect(self.accept)
        self._btn_row.addWidget(btn)
        if default:
            btn.setFocus()
            btn.setDefault(True)
        return btn


class MessageBox:
    """统一消息框静态封装：warning / information / question / critical。"""

    @staticmethod
    def _show(icon, title, text, parent=None, buttons=None, default_idx=0):
        """buttons=[(文本, 角色, default?)], 返回点击的按钮对象。"""
        box = _FramelessBox(title, icon, parent)
        box._text_lbl.setText(text)
        added = []
        if buttons:
            for b in buttons:
                text_b, role_b = b[0], b[1]
                default = len(b) > 2 and b[2]
                added.append(box._add_button(text_b, role_b, default))
        else:
            added.append(box._add_button("确定", "primary", True))
        if default_idx is not None and buttons and not any(
                len(b) > 2 and b[2] for b in buttons):
            added[min(default_idx, len(added) - 1)].setFocus()
        box.exec()
        return box, added

    @staticmethod
    def warning(parent, title, text):
        MessageBox._show("warning", title, text, parent)

    @staticmethod
    def information(parent, title, text):
        MessageBox._show("information", title, text, parent)

    @staticmethod
    def critical(parent, title, text):
        MessageBox._show("critical", title, text, parent)

    @staticmethod
    def question(parent, title, text, default_yes=True):
        """返回 True=是 / False=否；Esc 或 ✕ 关闭等同「否」，不按默认键算。"""
        box, btns = MessageBox._show(
            "question", title, text, parent,
            [("是", "primary", default_yes), ("否", "normal", not default_yes)])
        clicked = getattr(box, "_clicked", None)
        if clicked is None:                # Esc / ✕关闭
            return False
        return clicked is btns[0]

    @staticmethod
    def choose(parent, title, text, buttons, informative=""):
        """多按钮选择框：buttons=[(文本, 角色), ...]，返回点击按钮文本；关闭返回 None。"""
        if informative:
            text = "{}\n\n{}".format(text, informative)
        box, btns = MessageBox._show(
            "question", title, text, parent,
            [(b[0], "normal" if b[1] != "primary" else "primary") for b in buttons])
        clicked = getattr(box, "_clicked", None)
        if clicked is None:
            return None
        for b in btns:
            if clicked is b:
                return b.property("originText") or b.text()
        return None


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
        self._text_lbl.setObjectName("progressText")
        self._text_lbl.setWordWrap(True)
        layout.addWidget(self._text_lbl)

        self._bar = QProgressBar()
        self._bar.setObjectName("progressBar")
        self._bar.setRange(0, maximum)
        self._bar.setValue(0)
        layout.addWidget(self._bar)

        if cancellable:
            row = QHBoxLayout()
            row.addStretch(1)
            self._cancel_btn = QPushButton("取消")
            self._cancel_btn.setObjectName("msgBtn")
            apply_icon(self._cancel_btn, "取消")
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
