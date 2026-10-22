# -*- coding: utf-8 -*-
"""
训练对话框-数据增强 mixin: 勾选项现场搭建 / 可用性分级 / 计数徽标.

eventFilter 故意留在 TrainDialog(它还管 img_size 输入框的 Resize),
标题行点击切换由 _toggle_aug 承担. 宿主提供 ui/aug_body 等控件与 _spec()/_arch()/
_fit_content() 能力.
"""
from PySide6.QtCore import Qt, QT_TRANSLATE_NOOP
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout

from app.widgets.check_chip import CheckChip
from app.widgets.message_box import MessageBox
from app.core import theme
from app.train.aug_params import (AUG_BOTH, AUG_FAMILIES,
                                  AUG_HIDE_WHEN_UNSUPPORTED, aug_codes)
from app.train.aug_preview_dialog import AugPreviewDialog


AUG_GROUPS = (
    ("geo", QT_TRANSLATE_NOOP("TrainDialog", "几何变换"),
     QT_TRANSLATE_NOOP("TrainDialog", "标注框会跟着一起变换")),
    ("pix", QT_TRANSLATE_NOOP("TrainDialog", "像素变换"),
     QT_TRANSLATE_NOOP("TrainDialog", "只改画面，标注框不动")),
)
AUG_ITEMS = (
    ("geo", "hflip", QT_TRANSLATE_NOOP("TrainDialog", "水平翻转"),
     QT_TRANSLATE_NOOP("TrainDialog", "0.5")),
    ("geo", "vflip", QT_TRANSLATE_NOOP("TrainDialog", "垂直翻转"),
     QT_TRANSLATE_NOOP("TrainDialog", "0.5")),
    ("geo", "rotate", QT_TRANSLATE_NOOP("TrainDialog", "旋转"),
     QT_TRANSLATE_NOOP("TrainDialog", "±15°")),
    ("geo", "affine", QT_TRANSLATE_NOOP("TrainDialog", "仿射"),
     QT_TRANSLATE_NOOP("TrainDialog", "±20%")),
    ("geo", "mosaic", QT_TRANSLATE_NOOP("TrainDialog", "马赛克"),
     QT_TRANSLATE_NOOP("TrainDialog", "4 图拼接")),
    ("pix", "brightness", QT_TRANSLATE_NOOP("TrainDialog", "亮度/对比度"),
     QT_TRANSLATE_NOOP("TrainDialog", "±0.1")),
    ("pix", "colorjitter", QT_TRANSLATE_NOOP("TrainDialog", "颜色抖动"),
     QT_TRANSLATE_NOOP("TrainDialog", "饱和/色相")),
    ("pix", "blur", QT_TRANSLATE_NOOP("TrainDialog", "高斯模糊"),
     QT_TRANSLATE_NOOP("TrainDialog", "核 3")),
    ("pix", "noise", QT_TRANSLATE_NOOP("TrainDialog", "高斯噪声"),
     QT_TRANSLATE_NOOP("TrainDialog", "σ 0.05")),
)
AUG_COUNT_FMT = QT_TRANSLATE_NOOP("TrainDialog", "已启用 {} 项")
AUG_UNAVAILABLE = QT_TRANSLATE_NOOP(
    "TrainDialog", "该任务不支持配置数据增强")
AUG_ITEM_UNAVAILABLE = QT_TRANSLATE_NOOP(
    "TrainDialog", "当前网络架构不支持该增强")


AUG_TINT = {"geo": "accent", "pix": "st_info"}


def parse_aug_codes(value):
    """记录里的增强值转成勾选代号集合: 新值是逗号串, 旧值是单档预设代号."""
    known = {code for _g, code, _n, _p in AUG_ITEMS}
    return {c for c in (x.strip() for x in aug_codes(value)) if c in known}


class AugMixin:
    def _build_aug_items(self):
        """按 AUG_ITEMS 现场搭勾选项: 文案全部走 tr(), 换语言不用重排 XML."""
        body = getattr(self.ui, "aug_body", None)
        if body is None:
            return
        lay = body.layout()
        while lay.count():
            item = lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
        self._aug_checks = {}

        for gid, gname, gtip in AUG_GROUPS:
            head = QWidget(body)
            head.setObjectName("aug_group_head")
            hl = QHBoxLayout(head)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setSpacing(8)
            title = QLabel(self.tr(gname), head)
            title.setProperty("class", "augGroupTitle")
            tip = QLabel(self.tr(gtip), head)
            tip.setProperty("class", "augGroupTip")
            hl.addWidget(title)
            hl.addWidget(tip)
            hl.addStretch(1)
            lay.addWidget(head)

            grid = QGridLayout()
            grid.setHorizontalSpacing(7)
            grid.setVerticalSpacing(7)
            lay.addLayout(grid)
            row = 0
            col = 0
            for g, code, name, param in AUG_ITEMS:
                if g != gid:
                    continue
                chk = CheckChip(body, check=theme.color(AUG_TINT[gid]))
                chk.setText("{}({})".format(self.tr(name),
                                            self.tr(param)))
                chk.toggled.connect(self._on_aug_toggled)
                # 不撑满格子: 拉满的话悬停底色会横铺大半行
                grid.addWidget(chk, row, col, Qt.AlignLeft | Qt.AlignVCenter)
                self._aug_checks[code] = chk
                col += 1
                if col >= 2:
                    col = 0
                    row += 1

        self._set_aug_enabled()
        self._refresh_aug_badge()

    def _aug_backend(self):
        """增强交给哪套后端: Transformer 是 rf-detr(kornia), CNN 是 YOLO(ultralytics)."""
        return "cnn" if self._arch() == "cnn" else "transformer"

    def _aug_available(self):
        """分类(resnet)/异常检测(anomalib)/OCR(docTR) 的训练 runner 都不读增强代号."""
        return self._spec().aug_supported()

    def _aug_item_ok(self, code):
        return self._aug_backend() in AUG_FAMILIES.get(code, AUG_BOTH)

    def _checked_aug_codes(self):
        """只留当前后端吃得下的代号, 存进记录的和实际生效的才是同一份."""
        return [c for c, chk in self._aug_checks.items()
                if chk.isChecked() and self._aug_item_ok(c)]

    def _aug_value(self):
        """勾选代号串(逗号分隔); 整块不可用时按"不增强"记录."""
        if not self._aug_available():
            return ""
        return ",".join(self._checked_aug_codes())

    def _set_aug_checks(self, value):
        """回填勾选: 新记录是逗号串, 改造前的老记录是单档预设代号, 两种都认."""
        codes = parse_aug_codes(value)
        for code, chk in self._aug_checks.items():
            chk.blockSignals(True)
            chk.setChecked(code in codes)
            chk.blockSignals(False)
        self._refresh_aug_badge()

    def _set_aug_enabled(self):
        """
        整块不可用(任务不吃)就全灰; 整块可用时再按后端逐项分.
        不可用只改可用性和可见性, 勾选留着, 切回原来那套还是原样.
        """
        body = getattr(self.ui, "aug_body", None)
        if body is None:
            return
        ok = self._aug_available()
        tip = "" if ok else self.tr(AUG_UNAVAILABLE)
        # 折叠态下 body 是隐藏的, 提示得同时挂在标题行上
        for name in ("aug_body", "section_aug_wrap", "aug_toggle_btn",
                     "group_aug_title", "aug_count_label", "aug_preview_btn"):
            w = getattr(self.ui, name, None)
            if w is not None:
                w.setEnabled(ok)
                w.setToolTip(tip)
        for code, chk in self._aug_checks.items():
            usable = ok and self._aug_item_ok(code)
            chk.setVisible(code not in AUG_HIDE_WHEN_UNSUPPORTED
                           or self._aug_item_ok(code))
            chk.setEnabled(usable)
            chk.setToolTip("" if usable else self.tr(AUG_ITEM_UNAVAILABLE))
        self._refresh_aug_badge()
        # 马赛克卡片会随架构显示/隐藏, 内容高度跟着变
        self._fit_content()

    def _toggle_aug(self, expand):
        """折叠只改可见性, 勾选状态留着."""
        body = getattr(self.ui, "aug_body", None)
        btn = getattr(self.ui, "aug_toggle_btn", None)
        if body is None or btn is None:
            return
        body.setVisible(bool(expand))
        btn.setArrowType(Qt.DownArrow if expand else Qt.RightArrow)
        self._fit_content()

    def _on_aug_toggled(self):
        # 勾选态由 CheckChip 自绘, 这里只管计数
        self._refresh_aug_badge()

    def _refresh_aug_badge(self):
        label = getattr(self.ui, "aug_count_label", None)
        if label is None:
            return
        count = len(self._checked_aug_codes())
        label.setText(self.tr(AUG_COUNT_FMT).format(count))
        label.setProperty("on", "true" if count else "false")
        self._repolish(label)

    def _open_aug_preview(self):
        """
        增强预览: 勾选项/架构/图像尺寸都取界面当前值, 与开训时下发的同一份.
        不勾任何项也允许打开 — 空参数正好让人确认"不勾就是不增强".
        """
        ds = list(self._selected_datasets())
        if not ds:
            MessageBox.information(self, self.tr("数据增强预览"),
                                   self.tr("请先在训练集里选择数据集"))
            return
        dlg = AugPreviewDialog(self, self.app.db, ds,
                               self._checked_aug_codes(), self._aug_backend(),
                               self._task(), self._img_size())
        dlg.exec()

    @staticmethod
    def _repolish(widget):
        """动态属性改完要让样式重算, 否则得等下一次重绘才变."""
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()
