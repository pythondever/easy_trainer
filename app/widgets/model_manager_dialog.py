# -*- coding: utf-8 -*-
"""模型权重管理对话框: 列出所有可选权重, 现场下载并显示进度.

训练前预检(ensure_weight)也在这里: 权重缺失时给用户"去下载/仍然继续/取消"三条路,
而不是让训练子进程在后台悄悄下载、失败了只丢一堆堆栈.
"""

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import (QCheckBox, QDialog, QFileDialog, QFrame,
                               QHBoxLayout, QLabel, QProgressBar, QPushButton,
                               QVBoxLayout)

from app.core import model_assets
from app.core.log import write_log
from app.core.model_download import ModelDownloader
from app.widgets.dialog_buttons import apply_icon
from app.widgets.message_box import MessageBox
from ui.model_manager import Ui_ModelManagerDialog

ROW_H = 38
BAR_W = 158
BAR_H = 14
W_NAME = 54
W_SIZE = 62
W_DESC = 136
W_STATUS = 160
W_DIR = 220
TASK_CN = {model_assets.DETECT: "检测", model_assets.SEGMENT: "分割"}


def _set_state(widget, state):
    """切动态属性并让 QSS 重算, 否则颜色还是上一次的."""
    if widget.property("state") == state:
        return
    widget.setProperty("state", state)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def _fmt_speed(bps):
    if bps >= 1048576:
        return "{:.1f} MB/s".format(bps / 1048576.0)
    return "{:.0f} KB/s".format(bps / 1024.0)


def _fmt_eta(secs):
    secs = max(0, int(secs))
    if secs < 60:
        return "还剩 {}s".format(secs)
    return "还剩 {}m{}s".format(secs // 60, secs % 60)


class _ModelRow(QFrame):
    """一行: 勾选 / 名称 / 大小 / 描述 / 进度条(下载时才显示) / 状态."""

    def __init__(self, asset, parent=None):
        super().__init__(parent)
        self.asset = asset
        self.setObjectName("modelRow")
        self.setFixedHeight(ROW_H)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(10)

        self.check = QCheckBox()
        self.check.setProperty("class", "modelCheck")
        self.check.setCursor(Qt.PointingHandCursor)
        lay.addWidget(self.check)

        lay.addWidget(self._label(asset.level, "modelName", W_NAME, 13))
        lay.addWidget(self._label(
            model_assets.human_size(asset.nbytes), "modelSize", W_SIZE, 12))
        lay.addWidget(self._label(asset.desc, "modelDesc", W_DESC, 12))

        self.bar = QProgressBar()
        self.bar.setObjectName("modelProgress")
        self.bar.setRange(0, 1000)
        self.bar.setFixedSize(BAR_W, BAR_H)
        self.bar.setVisible(False)
        holder = QHBoxLayout()
        holder.setContentsMargins(0, 0, 0, 0)
        holder.addWidget(self.bar)
        holder.addStretch(1)
        lay.addLayout(holder, 1)

        self.status = self._label("", "modelStatus", W_STATUS, 12)
        self.status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lay.addWidget(self.status)

    def _label(self, text, cls, width, size):
        lbl = QLabel(text)
        lbl.setProperty("class", cls)
        lbl.setFixedWidth(width)
        font = lbl.font()
        font.setPixelSize(size)
        lbl.setFont(font)
        return lbl

    # ---------- 状态 ----------
    def is_checked(self):
        return self.check.isChecked()

    def set_checked(self, value):
        self.check.setChecked(bool(value))

    def mark_ready(self):
        self.bar.setVisible(False)
        self.status.setText("已就绪")
        self.status.setToolTip("")
        _set_state(self.status, "ready")

    def mark_idle(self):
        self.bar.setVisible(False)
        self.status.setText("未下载")
        self.status.setToolTip("")
        _set_state(self.status, "idle")

    def mark_verifying(self):
        self.status.setText("校验中...")
        _set_state(self.status, "busy")

    def mark_busy(self, done, total, bps):
        frac = 0.0 if not total else min(1.0, float(done) / total)
        self.bar.setVisible(True)
        self.bar.setValue(int(frac * 1000))
        if bps > 0:
            self.status.setText("{} · {}".format(
                _fmt_speed(bps), _fmt_eta((total - done) / bps)))
        else:
            self.status.setText(_fmt_speed(0))
        _set_state(self.status, "busy")

    def mark_failed(self, reason):
        self.bar.setVisible(False)
        self.status.setText("失败")
        self.status.setToolTip(reason)
        _set_state(self.status, "failed")

    def refresh(self, directory):
        if model_assets.is_ready(self.asset, directory):
            self.mark_ready()
        else:
            self.mark_idle()


class ModelManagerDialog(QDialog):
    def __init__(self, parent=None, db=None, preselect=()):
        super().__init__(parent)
        self.ui = Ui_ModelManagerDialog()
        self.ui.setupUi(self)
        self._db = db
        self._rows = []
        self._downloader = None
        self._failed = {}
        self._dir = model_assets.models_dir(db.get_models_dir() if db else "")
        self._show_dir()
        self._build_rows()
        for name in preselect:
            self._check_by_name(name)
        apply_icon(self.ui.close_btn, "关闭")
        self.ui.close_btn.clicked.connect(self.reject)
        self.ui.change_dir_btn.clicked.connect(self._on_change_dir)
        self.ui.start_btn.clicked.connect(self._on_start)
        self._refresh_total()

    # ---------- 构建 ----------
    def _build_rows(self):
        for task, layout in ((model_assets.DETECT, self.ui.detect_layout),
                             (model_assets.SEGMENT, self.ui.segment_layout)):
            assets = model_assets.for_task(task)
            for i, asset in enumerate(assets):
                row = _ModelRow(asset)
                if i == len(assets) - 1:
                    # 最后一行不画分隔线, 否则和分组框的下边框叠成粗线
                    row.setProperty("last", True)
                row.refresh(self._dir)
                # 已有的权重默认勾上: 底部"占用空间"一进来就是当前实际占用
                row.set_checked(model_assets.is_ready(asset, self._dir))
                row.check.toggled.connect(self._refresh_total)
                layout.addWidget(row)
                self._rows.append(row)

    def _check_by_name(self, filename):
        for row in self._rows:
            if row.asset.filename == filename:
                row.set_checked(True)

    def _row_of(self, filename):
        for row in self._rows:
            if row.asset.filename == filename:
                return row
        return None

    def _refresh_total(self, *_):
        total = sum(r.asset.nbytes for r in self._rows if r.is_checked())
        self.ui.total_label.setText("占用空间 {}".format(
            model_assets.human_size(total)))
        if self._downloader is None:
            self.ui.start_btn.setEnabled(True)

    # ---------- 目录 ----------
    def _show_dir(self):
        """路径定宽 + 中间省略: 不限宽会被 layout 硬裁掉尾巴, 连盘符都看不全."""
        fm = QFontMetrics(self.ui.dir_label.font())
        self.ui.dir_label.setFixedWidth(W_DIR)
        self.ui.dir_label.setText(fm.elidedText(self._dir, Qt.ElideMiddle, W_DIR))
        self.ui.dir_label.setToolTip(self._dir)

    def _on_change_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择权重目录", self._dir)
        if not d:
            return
        self._dir = model_assets.set_models_dir(d, sync_rf_home=False)
        if self._db is not None:
            self._db.set_models_dir(self._dir)
        self._show_dir()
        for row in self._rows:
            row.refresh(self._dir)
        self._refresh_total()

    def _writable(self):
        probe = os.path.join(self._dir, ".et_write_test")
        try:
            os.makedirs(self._dir, exist_ok=True)
            with open(probe, "w") as f:
                f.write("")
            os.remove(probe)
            return True
        except OSError as exc:
            write_log("权重目录不可写入 {}: {!r}".format(self._dir, exc))
            return False

    # ---------- 下载 ----------
    def _on_start(self):
        if self._downloader is not None:
            return
        todo = [r.asset for r in self._rows
                if r.is_checked() and not model_assets.is_ready(r.asset, self._dir)]
        if not todo:
            MessageBox.information(
                self, "模型权重", "勾选的模型都已就绪, 不需要下载.")
            return
        if not self._writable():
            MessageBox.warning(
                self, "模型权重",
                "当前目录不可写入, 请点\"更改\"换一个目录:\n{}".format(self._dir))
            return
        self._failed = {}
        self.ui.start_btn.setEnabled(False)
        self.ui.start_btn.setText("下载中...")
        self.ui.change_dir_btn.setEnabled(False)
        self._downloader = ModelDownloader(todo, self._dir, self)
        self._downloader.progress.connect(self._on_progress)
        self._downloader.verifying.connect(self._on_verifying)
        self._downloader.one_done.connect(self._on_one_done)
        self._downloader.one_failed.connect(self._on_one_failed)
        self._downloader.all_finished.connect(self._on_all_finished)
        self._downloader.start()

    def _on_progress(self, filename, done, total, bps):
        row = self._row_of(filename)
        if row is not None:
            row.mark_busy(done, total, bps)

    def _on_verifying(self, filename):
        row = self._row_of(filename)
        if row is not None:
            row.mark_verifying()

    def _on_one_done(self, filename):
        row = self._row_of(filename)
        if row is not None:
            row.mark_ready()

    def _on_one_failed(self, filename, reason):
        row = self._row_of(filename)
        if row is not None:
            row.mark_failed(reason)
        self._failed[filename] = reason

    def _on_all_finished(self, ok):
        self._downloader = None
        self.ui.start_btn.setText("开始下载")
        self.ui.start_btn.setEnabled(True)
        self.ui.change_dir_btn.setEnabled(True)
        self._refresh_total()
        # 目录始终记下, RF_HOME 只在真下成了才指过来: 取消或失败时该目录里还没有
        # 可用权重, 指过去会把它原本"回落 C 盘缓存"的兜底堵掉
        model_assets.set_models_dir(self._dir, sync_rf_home=ok)
        if self._failed:
            lines = ["{}: {}".format(k, v) for k, v in self._failed.items()]
            MessageBox.warning(self, "模型权重",
                               "以下权重没能下载完成:\n" + "\n".join(lines))
        elif ok:
            MessageBox.information(
                self, "模型权重", "权重已就绪, 保存在:\n{}".format(self._dir))

    def closeEvent(self, event):
        if self._downloader is not None:
            if not MessageBox.question(
                    self, "模型权重",
                    "下载还在进行, 现在关闭会中断下载(已下载部分保留, 下次可续传).\n确定关闭?"):
                event.ignore()
                return
            self._downloader.cancel()
            self._downloader.wait(3000)
            self._downloader = None
        super().closeEvent(event)


def open_model_manager(parent, db, preselect=()):
    dlg = ModelManagerDialog(parent, db, preselect)
    dlg.exec()
    return dlg


def ensure_weight(parent, db, task, level):
    """训练前预检: 返回 True 表示可以开始训练.

    缺失时弹窗说清要下多少、下到哪, 并给"去下载/仍然继续/取消"三条路:
    点"去下载"会打开权重管理且不启动训练, 避免用户以为已经开训了.
    """
    asset = model_assets.find(task, level)
    if asset is None:
        return True
    saved = db.get_models_dir() if db is not None else ""
    directory = model_assets.models_dir(saved)
    if model_assets.is_ready(asset, directory):
        model_assets.sync_rf_home(saved)
        return True
    text = "本次训练选用 {} {}模型, 需要先下载 {}.".format(
        level, TASK_CN.get(task, task), model_assets.human_size(asset.nbytes))
    informative = ("下载位置: {}\n"
                   "点\"仍然继续\"则由软件在训练时自行下载, "
                   "期间训练日志不会显示进度. 建议先在这里下载好.").format(directory)
    choice = MessageBox.choose(
        parent, "缺少模型权重", text,
        [("去下载", "primary"), ("仍然继续", "normal"), ("取消", "normal")],
        informative=informative)
    if choice == "去下载":
        open_model_manager(parent, db, preselect=(asset.filename,))
        return False
    return choice == "仍然继续"
