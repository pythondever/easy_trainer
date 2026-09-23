# -*- coding: utf-8 -*-
"""模型权重管理对话框: 列出所有可选权重, 现场下载并显示进度.

训练前预检(ensure_weight)也在这里: 权重缺失时给用户"去下载/取消"两条路,
而不是让训练子进程在后台悄悄下载、失败了只丢一堆堆栈.
"""

import os

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import (QCheckBox, QDialog, QFileDialog, QFrame,
                               QHBoxLayout, QLabel, QMenu, QProgressBar,
                               QPushButton)

from app.core import model_assets
from app.core.log import write_log
from app.core.model_download import ModelDownloader
from app.widgets.dialog_buttons import apply_icon
from app.widgets.message_box import MessageBox
from app.widgets.status_style import task_text
from ui.model_manager import Ui_ModelManagerDialog

ROW_H = 38
BAR_W = 144
BAR_H = 14
W_NAME = 54
W_SIZE = 62
# 描述列原 136: '精度极致, 显存占用很大' 实测 137px. 进度条让 8px 给状态列,
# 否则下载中 '1.2 MB/s · 还剩 12m30s' 这种长 ETA 会贴边被裁
W_DESC = 140
W_STATUS = 158
W_DIR = 220
BTN_W = 72


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
        return QC.translate("ModelManagerDialog", "还剩 {}s").format(secs)
    return QC.translate("ModelManagerDialog", "还剩 {}m{}s").format(
        secs // 60, secs % 60)


class _ModelRow(QFrame):
    """一行: 勾选 / 名称 / 大小 / 描述 / 进度条或本地路径 / 状态 / 本地按钮."""

    pick_requested = Signal(object)
    unbind_requested = Signal(object)

    def __init__(self, asset, parent=None):
        super().__init__(parent)
        self.asset = asset
        self.local_src = ""
        self.local_broken = False
        self.setObjectName("modelRow")
        self.setFixedHeight(ROW_H)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(10)

        self.check = QCheckBox()
        self.check.setProperty("class", "modelCheck")
        self.check.setCursor(Qt.PointingHandCursor)
        lay.addWidget(self.check)

        self.size_label = self._label(
            model_assets.human_size(asset.nbytes), "modelSize", W_SIZE)
        lay.addWidget(self._label(asset.level, "modelName", W_NAME))
        lay.addWidget(self.size_label)
        lay.addWidget(self._label(
            QC.translate("ModelAssets", asset.desc), "modelDesc", W_DESC))

        self.bar = QProgressBar()
        self.bar.setObjectName("modelProgress")
        self.bar.setRange(0, 1000)
        self.bar.setFixedSize(BAR_W, BAR_H)
        self.bar.setVisible(False)
        # 本地权重在进度条的位置显示源文件路径, 两者等宽互斥. 这格必须定宽:
        # 让它自适应就得占住全部弹性, 一隐藏空间回流给勾选框, 整行列位全右移
        self.path_label = QLabel()
        self.path_label.setProperty("class", "modelLocalPath")
        self.path_label.setFixedWidth(BAR_W)
        self.path_label.setVisible(False)
        lay.addWidget(self.bar)
        lay.addWidget(self.path_label)
        lay.addStretch(1)

        self.status = self._label("", "modelStatus", W_STATUS)
        self.status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lay.addWidget(self.status)

        self.local_btn = QPushButton(self.tr("本地"))
        self.local_btn.setProperty("class", "modelLocal")
        self.local_btn.setFixedWidth(BTN_W)
        self.local_btn.setCursor(Qt.PointingHandCursor)
        self.local_btn.clicked.connect(
            lambda: self.pick_requested.emit(self))
        lay.addWidget(self.local_btn)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_menu)

    def _label(self, text, cls, width):
        lbl = QLabel(text)
        lbl.setProperty("class", cls)
        lbl.setFixedWidth(width)
        return lbl

    # ---------- 本地权重 ----------
    def _on_menu(self, pos):
        if not (self.local_src or self.local_broken):
            return
        menu = QMenu(self)
        act = menu.addAction(self.tr("取消本地绑定"))
        if menu.exec(self.mapToGlobal(pos)) == act:
            self.unbind_requested.emit(self)

    def _show_path(self, text):
        fm = QFontMetrics(self.path_label.font())
        self.path_label.setToolTip(text)
        self.path_label.setText(
            fm.elidedText(text, Qt.ElideMiddle, BAR_W))
        self.path_label.setVisible(True)

    # ---------- 状态 ----------
    def is_checked(self):
        return self.check.isChecked()

    def set_checked(self, value):
        self.check.setChecked(bool(value))

    def _clear_local(self):
        self.local_src = ""
        self.local_broken = False
        self.path_label.setVisible(False)
        self.path_label.setText("")
        self.size_label.setText(model_assets.human_size(self.asset.nbytes))
        self.local_btn.setText(self.tr("本地"))
        self.local_btn.setVisible(True)

    def mark_ready(self):
        self.bar.setVisible(False)
        self._clear_local()
        self.status.setText(self.tr("已就绪"))
        self.status.setToolTip("")
        _set_state(self.status, "ready")

    def mark_idle(self):
        self.bar.setVisible(False)
        self._clear_local()
        self.status.setText(self.tr("未下载"))
        self.status.setToolTip("")
        _set_state(self.status, "idle")

    def mark_local(self, src):
        self.bar.setVisible(False)
        self.local_src = src
        self.local_broken = False
        self.local_btn.setVisible(True)
        self.local_btn.setText(self.tr("更换"))
        self._show_path(src)
        try:
            size = os.path.getsize(src)
        except OSError:
            size = 0
        self.size_label.setText(
            model_assets.human_size(size) if size else "—")
        self.status.setText(self.tr("本地权重"))
        self.status.setToolTip(src)
        _set_state(self.status, "local")

    def mark_local_broken(self, src):
        self.bar.setVisible(False)
        self.local_src = ""
        self.local_broken = True
        self.local_btn.setVisible(True)
        self.local_btn.setText(self.tr("重选"))
        self._show_path(src or self.tr("(路径未记录)"))
        self.size_label.setText("—")
        self.status.setText(self.tr("本地失效"))
        self.status.setToolTip(
            self.tr("登记的本地权重文件已不在这个位置:\n{}").format(src))
        _set_state(self.status, "broken")

    def mark_verifying(self):
        self.local_btn.setVisible(False)
        self.status.setText(self.tr("校验中..."))
        _set_state(self.status, "busy")

    def mark_busy(self, done, total, bps):
        frac = 0.0 if not total else min(1.0, float(done) / total)
        self.path_label.setVisible(False)
        self.local_btn.setVisible(False)
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
        self.local_btn.setVisible(True)
        self.status.setText(self.tr("失败"))
        self.status.setToolTip(reason)
        _set_state(self.status, "failed")

    def refresh(self, directory):
        # 本地绑定优先于官方文件: resolve_path 也是先给本地那份
        item = model_assets.local_entry(self.asset, directory)
        src = (item or {}).get("src") or ""
        if item and src and os.path.isfile(src):
            self.mark_local(src)
        elif item:
            self.mark_local_broken(src)
        elif model_assets.is_downloaded(self.asset, directory):
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
        # 权重标识(根目录下相对路径) → 行. 本地文件名只到档位, nano.pt 在 cnn 和
        # transformer 下各有一份, 拿文件名当键会让进度画到另一个架构的行上
        self._rows_by_key = {}
        self._downloader = None
        self._failed = {}
        self._focus_row = None
        self._dir = model_assets.models_dir(db.get_models_dir() if db else "")
        self._show_dir()
        self._build_rows()
        for key in preselect:
            self._check_key(key)
            if self._focus_row is None:
                self._focus_row = self._row_of(key)
        for row in self._rows:
            row.pick_requested.connect(self._on_pick_local)
            row.unbind_requested.connect(self._on_unbind_local)
        apply_icon(self.ui.close_btn, self.tr("关闭"))
        self.ui.close_btn.clicked.connect(self.reject)
        self.ui.change_dir_btn.clicked.connect(self._on_change_dir)
        self.ui.start_btn.clicked.connect(self._on_start)
        self._refresh_total()
        self._fit_height()
        self._fit_start_btn()

    def _fit_start_btn(self):
        """按当前语言最长的那条按钮文案定宽: QSS 的 min-width 装不下德/法语的译文."""
        btn = self.ui.start_btn
        cur = btn.text()
        widest = 0
        for text in (self.tr("开始下载"), self.tr("下载中...")):
            btn.setText(text)
            widest = max(widest, btn.sizeHint().width())
        btn.setText(cur)
        btn.setFixedWidth(max(btn.minimumSizeHint().width(), widest))

    def _fit_height(self):
        """十八行权重全展开约 900px, 小屏上会顶出去: 按内容高度开窗, 上限留给屏幕."""
        scr = self.screen()
        avail = scr.availableGeometry().height() if scr else 900
        margin = self.ui.root_layout.contentsMargins()
        want = (self.ui.groups_content.sizeHint().height()
                + self.ui.foot_layout.sizeHint().height()
                + margin.top() + margin.bottom()
                + self.ui.root_layout.spacing())
        self.resize(self.width(), min(want, max(360, avail - 90)))

    def showEvent(self, event):
        super().showEvent(event)
        if self._focus_row is not None:
            # "去下载"带过来的那一行在滚动区下方, 不滚过去看着像没勾上.
            # 开窗这一拍滚动条量程还没算出来, 得推到事件循环下一拍
            QTimer.singleShot(0, self._scroll_to_focus)

    def _scroll_to_focus(self):
        row, self._focus_row = self._focus_row, None
        if row is not None:
            self.ui.groups_scroll.ensureWidgetVisible(row)

    # ---------- 构建 ----------
    def _build_rows(self):
        # 顺序必须与 .ui 里标题+分组框的排布一致, 否则行会挂到别的标题下面
        for task, layout in ((model_assets.DETECT, self.ui.detect_layout),
                             (model_assets.DETECT_CNN,
                              self.ui.detect_cnn_layout),
                             (model_assets.SEGMENT, self.ui.segment_layout),
                             (model_assets.SEGMENT_CNN,
                              self.ui.segment_cnn_layout)):
            assets = model_assets.for_task(task)
            for i, asset in enumerate(assets):
                row = _ModelRow(asset)
                self._rows_by_key[model_assets.rel_path(asset)] = row
                if i == len(assets) - 1:
                    # 最后一行不画分隔线, 否则和分组框的下边框叠成粗线
                    row.setProperty("last", True)
                row.refresh(self._dir)
                # 已有的权重(含本地绑定)默认勾上: 底部计数一进来就是当前实况
                row.set_checked(model_assets.is_ready(asset, self._dir))
                row.check.toggled.connect(self._refresh_total)
                layout.addWidget(row)
                self._rows.append(row)
            # addWidget 只把内层布局标脏, 装滚动区的外层缓存里这个框还是空的高.
            # 不补这一下, _fit_height 量到的内容高度会少掉整个分组
            layout.parentWidget().updateGeometry()

    def _check_key(self, key):
        row = self._row_of(key)
        if row is not None:
            row.set_checked(True)

    def _row_of(self, key):
        return self._rows_by_key.get(key)

    def _refresh_total(self, *_):
        pending = 0
        n_local = 0
        for r in self._rows:
            if r.local_src or r.local_broken:
                n_local += 1
            elif r.is_checked() and not model_assets.is_downloaded(
                    r.asset, self._dir):
                pending += r.asset.nbytes
        text = (self.tr("待下载 {}").format(
            model_assets.human_size(pending)) if pending
            else self.tr("无需下载"))
        if n_local:
            text += " · " + self.tr("本地 {} 项").format(n_local)
        self.ui.total_label.setText(text)
        if self._downloader is None:
            self.ui.start_btn.setEnabled(True)

    # ---------- 目录 ----------
    def _show_dir(self):
        """路径定宽 + 中间省略: 不限宽会被 layout 硬裁掉尾巴, 连盘符都看不全."""
        fm = QFontMetrics(self.ui.dir_label.font())
        self.ui.dir_label.setFixedWidth(W_DIR)
        self.ui.dir_label.setText(fm.elidedText(self._dir, Qt.ElideMiddle, W_DIR))
        # 标签只放得下根目录, 实际文件在架构子目录里: tooltip 补上, 免得照着去找扑空
        self.ui.dir_label.setToolTip("{}\ntransformer  {}\ncnn  {}".format(
            self._dir,
            model_assets.dir_for(model_assets.TRANSFORMER, self._dir),
            model_assets.dir_for(model_assets.CNN, self._dir)))

    def _on_change_dir(self):
        d = QFileDialog.getExistingDirectory(self, self.tr("选择权重目录"),
                                             self._dir)
        if not d:
            return
        self._dir = model_assets.set_models_dir(d, sync_rf_home=False)
        if self._db is not None:
            self._db.set_models_dir(self._dir)
        self._show_dir()
        for row in self._rows:
            row.refresh(self._dir)
        self._refresh_total()

    def _on_pick_local(self, row):
        start = ""
        item = model_assets.local_entry(row.asset, self._dir)
        if item:
            start = os.path.dirname(item.get("src") or "")
        path, _ = QFileDialog.getOpenFileName(
            self, self.tr("选择预训练权重"), start,
            self.tr("权重文件 (*.pt *.pth *.ckpt)"))
        if not path:
            return
        reason = model_assets.check_local_file(path)
        if reason:
            MessageBox.warning(self, self.tr("模型权重"), reason)
            return
        hint = model_assets.mismatch_hint(row.asset, path)
        if hint and not MessageBox.question(
                self, self.tr("模型权重"),
                "{}\n\n{}".format(hint, self.tr("仍要用这个文件吗?"))):
            return
        ok, reason = model_assets.bind_local(row.asset, path, self._dir)
        if not ok:
            MessageBox.warning(self, self.tr("模型权重"), reason)
            return
        # 目录里现在有可用权重了, 立刻把 RF_HOME 指过来: 不然界面显示就绪,
        # 训练子进程还按上次记的位置找
        model_assets.set_models_dir(self._dir, sync_rf_home=True)
        if self._db is not None:
            self._db.set_models_dir(self._dir)
        row.refresh(self._dir)
        self._refresh_total()

    def _on_unbind_local(self, row):
        if model_assets.unbind_local(row.asset, self._dir):
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
            write_log(QC.translate("ModelManagerDialog", "权重目录不可写入 {}: {!r}").format(self._dir, exc))
            return False

    # ---------- 下载 ----------
    def _on_start(self):
        if self._downloader is not None:
            return
        todo = [r.asset for r in self._rows
                if r.is_checked() and not model_assets.is_ready(r.asset, self._dir)]
        if not todo:
            MessageBox.information(
                self, self.tr("模型权重"), self.tr("勾选的模型都已就绪, 不需要下载."))
            return
        if not self._writable():
            MessageBox.warning(
                self, self.tr("模型权重"),
                self.tr("当前目录不可写入, 请点\"更改\"换一个目录:\n{}")
                .format(self._dir))
            return
        self._failed = {}
        self.ui.start_btn.setEnabled(False)
        self.ui.start_btn.setText(self.tr("下载中..."))
        self.ui.change_dir_btn.setEnabled(False)
        self._downloader = ModelDownloader(todo, self._dir, self)
        self._downloader.progress.connect(self._on_progress)
        self._downloader.verifying.connect(self._on_verifying)
        self._downloader.one_done.connect(self._on_one_done)
        self._downloader.one_failed.connect(self._on_one_failed)
        self._downloader.all_finished.connect(self._on_all_finished)
        self._downloader.start()

    def _on_progress(self, key, done, total, bps):
        row = self._row_of(key)
        if row is not None:
            row.mark_busy(done, total, bps)

    def _on_verifying(self, key):
        row = self._row_of(key)
        if row is not None:
            row.mark_verifying()

    def _on_one_done(self, key):
        row = self._row_of(key)
        if row is not None:
            row.mark_ready()

    def _on_one_failed(self, key, reason):
        row = self._row_of(key)
        if row is not None:
            row.mark_failed(reason)
        self._failed[key] = reason

    def _on_all_finished(self, ok):
        self._downloader = None
        self.ui.start_btn.setText(self.tr("开始下载"))
        self.ui.start_btn.setEnabled(True)
        self.ui.change_dir_btn.setEnabled(True)
        self._refresh_total()
        # 目录始终记下, RF_HOME 只在真下成了才指过来: 取消或失败时该目录里还没有
        # 可用权重, 指过去会把它原本"回落 C 盘缓存"的兜底堵掉
        model_assets.set_models_dir(
            self._dir,
            sync_rf_home=ok or any(r.local_src for r in self._rows))
        if self._failed:
            # 同一原因在多个文件上重复时只报一次; 是哪几个文件看列表里标红的行
            reasons = list(dict.fromkeys(self._failed.values()))
            MessageBox.warning(self, self.tr("模型权重"),
                               self.tr("以下权重没能下载完成:\n")
                               + "\n".join(reasons))

    def closeEvent(self, event):
        if self._downloader is not None:
            if not MessageBox.question(
                    self, self.tr("模型权重"),
                    self.tr("下载还在进行, 现在关闭会中断下载"
                            "(已下载部分保留, 下次可续传).\n确定关闭?")):
                event.ignore()
                return
            self._downloader.cancel()
            self._downloader.wait(3000)
            self._downloader = None
        super().closeEvent(event)


def open_model_manager(parent, db, preselect=()):
    """preselect 收权重标识(model_assets.rel_path), 不是文件名."""
    dlg = ModelManagerDialog(parent, db, preselect)
    dlg.exec()
    return dlg


def ensure_weight(parent, db, task, level, family="transformer"):
    """训练前预检: 返回 True 表示可以开始训练, 缺权重一律不放行.

    缺失时弹窗说清要下多少, 并给"去下载/取消"两条路:
    点"去下载"会打开权重管理且不启动训练, 避免用户以为已经开训了.
    """
    asset = model_assets.find(model_assets.asset_task(task, family), level)
    if asset is None:
        return True
    saved = db.get_models_dir() if db is not None else ""
    directory = model_assets.models_dir(saved)
    if model_assets.is_ready(asset, directory):
        model_assets.sync_rf_home(saved)
        return True
    # 模块级函数没有 self.tr; 文案也要按字面量传给 translate, 否则抽不出译文
    btn_down = QC.translate("ModelManagerDialog", "去下载")
    btn_cancel = QC.translate("ModelManagerDialog", "取消")
    title = QC.translate("ModelManagerDialog", "缺少模型权重")
    text = QC.translate(
        "ModelManagerDialog", "本次训练选用 {} {}模型, 需要先下载 {}.").format(
        level, task_text(task), model_assets.human_size(asset.nbytes))
    choice = MessageBox.choose(
        parent, title, text,
        [(btn_down, "primary"), (btn_cancel, "normal")],
        informative=QC.translate(
            "ModelManagerDialog",
        "该架构的权重必须先下载好才能开始训练, 也可以在权重管理里指定本地的权重文件."))
    if choice == btn_down:
        open_model_manager(parent, db,
                           preselect=(model_assets.rel_path(asset),))
    return False
