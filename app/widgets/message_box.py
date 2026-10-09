# -*- coding: utf-8 -*-
"""统一消息框 + 进度对话框(深色主题, 自绘无边框窗口, 与 app QSS 一致)."""

import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QVBoxLayout,
                               QHBoxLayout, QLabel, QMessageBox, QPlainTextEdit,
                               QPushButton, QProgressBar, QToolTip)
from PySide6.QtWidgets import QGraphicsDropShadowEffect

from app.core import theme
from app.core.utils import project_root
from app.widgets.dialog_buttons import BTN_WIDTH, apply_icon


# 图标: (resources 文件名, 染色)
_ICONS = {
    "warning": ("msg_warning.svg", theme.hexof("icon_warning")),
    "information": ("msg_information.svg", theme.hexof("accent")),
    "critical": ("msg_critical.svg", theme.hexof("icon_critical")),
    "question": ("msg_question.svg", theme.hexof("accent")),
}
_ICON_PX = 22
_ICON_COL_W = 34          # 图标列宽固定, 保证正文左边界与标题下的对齐
TEXT_MAX_W = 420          # 正文限宽: 不限时一条长 traceback 能把窗口撑到屏幕外
DETAIL_MIN_H = 96         # 详情区按行数自适应高度, 两行也占满 180 会留一大片空
DETAIL_MAX_H = 180
DETAIL_LINE_H = 17

LIST_MAX_ITEMS = 8        # 清单块最多列几条, 再多折成"…还有 N 个", 免得弹窗高过屏幕
LIST_PAD_L = 14
LIST_PAD_R = 12
LIST_DOT_W = 6            # 条目左侧的警示色点
LIST_GAP = 10

# QMessageBox 的 Role 枚举对应 QSS 里的 class
_ROLE_MAP = {
    QMessageBox.AcceptRole: "primary",
    QMessageBox.YesRole: "primary",
    QMessageBox.DestructiveRole: "danger",
}


def _icon_pixmap(name, color):
    """加载 resources 图标并按当前主题色染色."""
    path = os.path.join(project_root(), "resources", name)
    if not os.path.exists(path):
        return QPixmap()
    src = QIcon(path).pixmap(QSize(_ICON_PX, _ICON_PX))
    if src.isNull():
        return src
    out = QPixmap(src.size())
    out.fill(Qt.transparent)
    painter = QPainter(out)
    painter.drawPixmap(0, 0, src)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(out.rect(), QColor(color))
    painter.end()
    return out


def _normalize_role(role):
    """调用方传 QMessageBox.Role 枚举或 "primary"/"danger"/"normal" 字符串都认.

    早先写成 "normal" if b[1] != "primary" else "primary", danger 与
    DestructiveRole 被一律压成 normal, 破坏性按钮和普通按钮一个颜色.
    """
    if isinstance(role, str):
        return role if role in ("primary", "danger", "normal") else "normal"
    return _ROLE_MAP.get(role, "normal")


def _split_detail(text):
    """多行或超长的错误内容才值得折叠进详情区, 单行短消息直接当正文."""
    if not text:
        return None
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2 and len(text) <= 160:
        return None
    return text


def summary_of(text):
    """长文本压成一行摘要: 详情折叠时用它当预览, 展开前也能看出个大概."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return text
    # 有 traceback 就是末行异常, 别被"训练过程中发生错误, Err:"这类引导语挡住
    for ln in lines:
        if ln.startswith("Traceback (most recent call last)"):
            return lines[-1]
    # "训练过程中发生错误, Err:" 这类引导语本身不带信息, 摘要取它后面第一行
    if len(lines) > 1 and lines[0].endswith((":", "：")):
        return lines[1]
    return lines[0]


def _copy_text(text, btn):
    """复制到剪贴板并在按钮上弹个提示, 否则用户不知道到底复制上没有."""
    QApplication.clipboard().setText(text)
    QToolTip.showText(btn.mapToGlobal(btn.rect().center()),
                      QC.translate("MessageBox", "详情已复制到剪贴板"), btn)


class _FramelessBox(QDialog):
    """自绘无边框弹窗: 圆角+阴影+自绘标题栏, 支持拖拽移动.

    内容塞 self._content(QVBoxLayout), 按钮塞 self._btn_row(QHBoxLayout, 右对齐).
    """

    # 阴影是画在窗口外圈的 graphics effect, 内容边距为 0 时会被窗口边界裁掉
    SHADOW_MARGIN = 16

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)

        margin = self.SHADOW_MARGIN
        outer = QVBoxLayout(self)
        outer.setContentsMargins(margin, margin, margin, margin)
        self._frame = QFrame(self)
        self._frame.setObjectName("msgFrame")
        self._frame.setMinimumWidth(380)
        outer.addWidget(self._frame)

        shadow = QGraphicsDropShadowEffect(self._frame)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 4)
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
        # 用 U+00D7 而不是 U+2715: 后者的字形中文字体多半没有, 会渲染成方块
        close_btn = QPushButton("×")
        close_btn.setObjectName("msgClose")
        close_btn.setFixedSize(28, 24)
        close_btn.clicked.connect(self.reject)
        title_row.addWidget(close_btn, 0, Qt.AlignTop)
        layout.addLayout(title_row)
        layout.addSpacing(10)

        # ---- 内容区(子类往 _content 里加) ----
        self._content = QVBoxLayout()
        self._content.setSpacing(0)
        layout.addLayout(self._content)
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

    # ---- 内容 ----
    def add_icon_text(self, icon_key, text):
        row = QHBoxLayout()
        row.setSpacing(12)
        name, color = _ICONS.get(icon_key, _ICONS["information"])
        pixmap = _icon_pixmap(name, color)
        icon_lbl = QLabel()
        icon_lbl.setFixedWidth(_ICON_COL_W)
        icon_lbl.setAlignment(Qt.AlignCenter)
        if pixmap.isNull():
            # 资源缺失时退化成字形, 不留空白
            icon_lbl.setText("!")
            icon_lbl.setStyleSheet(
                "color: {}; font-size: {}px; font-weight: 700;".format(color, _ICON_PX))
        else:
            icon_lbl.setPixmap(pixmap)
        row.addWidget(icon_lbl, 0, Qt.AlignVCenter)
        self._text_lbl = QLabel(text)
        self._text_lbl.setObjectName("msgText")
        self._text_lbl.setWordWrap(True)
        self._text_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._text_lbl.setMaximumWidth(TEXT_MAX_W)
        row.addWidget(self._text_lbl, 1)
        self._content.addLayout(row)
        return self._text_lbl

    def add_detail(self, text):
        """只读等宽文本区: 报错堆栈能选中能复制能滚动, 也不会把窗口撑宽."""
        edit = QPlainTextEdit()
        edit.setObjectName("msgDetail")
        edit.setPlainText(text)
        edit.setReadOnly(True)
        edit.setLineWrapMode(QPlainTextEdit.NoWrap)
        rows = max(1, len(text.splitlines()))
        height = max(DETAIL_MIN_H,
                     min(DETAIL_MAX_H, rows * DETAIL_LINE_H + 26))
        edit.setFixedSize(TEXT_MAX_W, height)
        row = QHBoxLayout()
        row.setContentsMargins(_ICON_COL_W + 12, 0, 0, 0)
        row.addWidget(edit)
        self._content.addLayout(row)
        return edit

    def add_list_block(self, title, items):
        """
        路径清单块: 标题行右侧是"复制", 下面每条一个警示色点 + 一条路径.
        点复制拿到的是换行拼接的完整清单, 不带标题与色点.
        """
        frame = QFrame()
        frame.setObjectName("msgList")
        # 宽度定死: 路径里没有空格, 不限宽时一条长路径能把弹窗撑到屏幕外
        frame.setFixedWidth(TEXT_MAX_W)
        col = QVBoxLayout(frame)
        col.setContentsMargins(LIST_PAD_L, 12, LIST_PAD_R, 12)
        col.setSpacing(0)

        head = QHBoxLayout()
        head.setSpacing(8)
        head_lbl = QLabel(title)
        head_lbl.setObjectName("msgListTitle")
        head.addWidget(head_lbl)
        head.addStretch(1)
        copy_btn = QPushButton(QC.translate("MessageBox", "复制"))
        copy_btn.setObjectName("msgListCopy")
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.clicked.connect(lambda: _copy_text("\n".join(items), copy_btn))
        head.addWidget(copy_btn)
        col.addLayout(head)

        shown = items[:LIST_MAX_ITEMS]
        for n, path in enumerate(shown):
            col.addSpacing(11 if n == 0 else 7)
            row = QHBoxLayout()
            row.setSpacing(LIST_GAP)
            dot = QLabel()
            dot.setObjectName("msgListDot")
            dot.setFixedSize(LIST_DOT_W, LIST_DOT_W)
            # 包一层竖排: 路径换行时色点跟首行走, 而不是跟着整块居中
            dot_col = QVBoxLayout()
            dot_col.setContentsMargins(0, 5, 0, 0)
            dot_col.setSpacing(0)
            dot_col.addWidget(dot)
            dot_col.addStretch(1)
            row.addLayout(dot_col)
            lbl = QLabel(path)
            lbl.setObjectName("msgListItem")
            lbl.setWordWrap(True)
            lbl.setToolTip(path)
            lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            row.addWidget(lbl, 1)
            col.addLayout(row)
        if len(shown) < len(items):
            col.addSpacing(7)
            more = QLabel(QC.translate("MessageBox", "…还有 {} 个").format(
                len(items) - len(shown)))
            more.setObjectName("msgListMore")
            col.addWidget(more)

        outer = QHBoxLayout()
        outer.setContentsMargins(_ICON_COL_W + 12, 0, 0, 0)
        outer.addWidget(frame)
        self._content.addLayout(outer)
        return frame

    # ---- 按钮 ----
    def _add_button(self, text, role="normal", default=False, accept=True):
        btn = QPushButton(text)
        btn.setObjectName("msgBtn")
        btn.setProperty("originText", text)
        # class 要在 apply_icon 之前设: 它按已有 class 决定要不要补 primary
        btn.setProperty("class", role)
        apply_icon(btn, text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumWidth(BTN_WIDTH)
        if accept:
            btn.clicked.connect(lambda: setattr(self, "_clicked", btn))
            btn.clicked.connect(self.accept)
        self._btn_row.addWidget(btn)
        if default:
            btn.setFocus()
            btn.setDefault(True)
        return btn


class MessageBox:
    """统一消息框静态封装: warning / information / question / critical."""

    @staticmethod
    def _show(icon, title, text, parent=None, buttons=None, default_idx=0, detail=None):
        """buttons=[(文本, 角色, default?)], 返回 (box, 已添加按钮列表)."""
        box = _FramelessBox(title, parent)
        box.add_icon_text(icon, text)
        edit = None
        if detail:
            box._content.addSpacing(12)
            edit = box.add_detail(detail)
        added = []
        if buttons:
            for b in buttons:
                added.append(box._add_button(
                    b[0], _normalize_role(b[1] if len(b) > 1 else "normal"),
                    len(b) > 2 and b[2]))
        elif edit is not None:
            added.append(box._add_button(
                QC.translate("MessageBox", "关闭"), "primary", True))
            copy_btn = box._add_button(
                QC.translate("MessageBox", "复制详情"), "normal", accept=False)
            copy_btn.clicked.connect(
                lambda: _copy_text(edit.toPlainText(), copy_btn))
            added.append(copy_btn)
        else:
            added.append(box._add_button(
                QC.translate("MessageBox", "确定"), "primary", True))
        if default_idx is not None and buttons and not any(
                len(b) > 2 and b[2] for b in buttons):
            added[min(default_idx, len(added) - 1)].setFocus()
        box.exec()
        return box, added

    @staticmethod
    def warning(parent, title, text):
        MessageBox._show("warning", title, text, parent)

    @staticmethod
    def missing_paths(parent, title, text, block_title, paths):
        """
        路径失效提示: 正文 + 失效路径清单 + 一个"知道了"(主色)收尾.
        图像目录被删与图像文件被删共用这一套, 标题/正文/清单标题由调用方给.
        """
        box = _FramelessBox(title, parent)
        box.add_icon_text("warning", text)
        box._content.addSpacing(14)
        box.add_list_block(block_title, paths)
        box._add_button(QC.translate("MessageBox", "知道了"), "primary", True)
        box.exec()

    @staticmethod
    def information(parent, title, text):
        MessageBox._show("information", title, text, parent)

    @staticmethod
    def critical(parent, title, text):
        """错误弹窗: 多行/超长内容(如 traceback)拆成摘要 + 可复制的详情区."""
        detail = _split_detail(text)
        if detail is not None:
            text = summary_of(text)
        MessageBox._show("critical", title, text, parent, detail=detail)

    @staticmethod
    def question(parent, title, text, default_yes=True):
        """返回 True=是 / False=否; Esc 或 × 关闭等同"否", 不按默认键算."""
        box, btns = MessageBox._show(
            "question", title, text, parent,
            [(QC.translate("MessageBox", "确定"), "primary", default_yes),
             (QC.translate("MessageBox", "取消"), "normal", not default_yes)])
        clicked = getattr(box, "_clicked", None)
        if clicked is None:                # Esc / ×关闭
            return False
        return clicked is btns[0]

    @staticmethod
    def choose(parent, title, text, buttons, informative=""):
        """多按钮选择框: buttons=[(文本, 角色), ...], 返回点击按钮文本; 关闭返回 None."""
        if informative:
            text = "{}\n\n{}".format(text, informative)
        box, btns = MessageBox._show(
            "question", title, text, parent, [(b[0], b[1]) for b in buttons])
        clicked = getattr(box, "_clicked", None)
        if clicked is None:
            return None
        for b in btns:
            if clicked is b:
                return b.property("originText") or b.text()
        return None


class ProgressDialog(_FramelessBox):
    """带进度条 + 文本 + 可选取消按钮的模态对话框(导出/批量删除长任务)."""

    def __init__(self, title, text, parent=None, maximum=100, cancellable=True):
        super().__init__(title, parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        self._cancelled = False

        self._text_lbl = QLabel(text)
        self._text_lbl.setObjectName("progressText")
        self._text_lbl.setWordWrap(True)
        self._text_lbl.setMinimumWidth(382)   # 加上左右内边距约 430 宽
        self._content.addWidget(self._text_lbl)
        self._content.addSpacing(14)

        self._bar = QProgressBar()
        self._bar.setObjectName("progressBar")
        self._bar.setRange(0, maximum)
        self._bar.setValue(0)
        self._content.addWidget(self._bar)

        self._cancel_btn = None
        if cancellable:
            self._cancel_btn = self._add_button(
                QC.translate("MessageBox", "取消"), "normal", accept=False)
            self._cancel_btn.clicked.connect(self._on_cancel)

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
        self._cancel_btn.setText(QC.translate("MessageBox", "取消中..."))
