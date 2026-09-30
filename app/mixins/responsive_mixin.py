# -*- coding: utf-8 -*-
"""顶栏装不下时把尾部的入口按钮收进「…」菜单."""
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtCore import QT_TRANSLATE_NOOP
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QApplication, QMenu, QPushButton

from app.core import theme
from app.core.utils import load_style_sheet

# 可收起的入口: 都是"打开某个对话框"; 不含主操作(训练)、自救入口(语言)与标签筛选
OVERFLOW_BTNS = ("dataset_properties_btn", "model_btn", "queue_btn", "log_btn")


class ResponsiveMixin(object):
    def init_header_overflow(self):
        btn = QPushButton("…", self)
        btn.setObjectName("headerMoreBtn")
        btn.setToolTip(QC.translate("ResponsiveMixin", "更多"))
        menu = QMenu(btn)
        self._header_overflow_actions = []
        for name in OVERFLOW_BTNS:
            src = getattr(self, name)
            act = menu.addAction(src.text())
            act.triggered.connect(src.click)
            self._header_overflow_actions.append(act)
        menu.addSeparator()
        self._append_font_scale_menu(menu)
        # 按钮文案随语言和队列条数变, 建菜单时抄一遍就再也跟不上 —— 改成弹出前现取
        menu.aboutToShow.connect(self._sync_header_more_menu)
        btn.setMenu(menu)
        self.datasetHeaderLayout.addWidget(btn)
        self._header_more_btn = btn
        self._header_more_menu = menu
        self._header_collapsed = False
        self.datasetHeader.installEventFilter(self)

    def _retranslate_header_overflow(self):
        self._header_more_btn.setToolTip(QC.translate("ResponsiveMixin", "更多"))
        if self._font_scale_menu is not None:
            self._font_scale_menu.setTitle(
                QC.translate("ResponsiveMixin", "界面字号"))
            for act, label, _scale in self._font_scale_actions:
                act.setText(QC.translate("ResponsiveMixin", label))
        self._sync_font_scale_menu()
        self._sync_header_more_menu()
        self._fit_header()

    def _append_font_scale_menu(self, menu):
        """界面倍率: QSS 的字号是绝对值, 系统"文本大小"递不进来, 只能应用内自己给档位."""
        sub = menu.addMenu(QC.translate("ResponsiveMixin", "界面字号"))
        group = QActionGroup(sub)
        group.setExclusive(True)
        self._font_scale_menu = sub
        self._font_scale_actions = []
        # 档位名是变量, 不是 translate() 的字面量参数, 得包一层 lupdate 才扫得到
        for label, scale in ((QT_TRANSLATE_NOOP("ResponsiveMixin", "标准"), 1.0),
                             (QT_TRANSLATE_NOOP("ResponsiveMixin", "大"), 1.15),
                             (QT_TRANSLATE_NOOP("ResponsiveMixin", "超大"), 1.35)):
            act = sub.addAction(QC.translate("ResponsiveMixin", label))
            act.setCheckable(True)
            act.triggered.connect(
                lambda _checked=False, s=scale: self._set_font_scale(s))
            group.addAction(act)
            self._font_scale_actions.append((act, label, scale))
        self._sync_font_scale_menu()

    def _sync_font_scale_menu(self):
        for act, _label, scale in self._font_scale_actions:
            act.setChecked(abs(theme.FONT_SCALE - scale) < 0.01)

    def _set_font_scale(self, scale):
        theme.set_font_scale(scale)
        self.db.set_font_scale(scale)
        QApplication.instance().setStyleSheet(load_style_sheet()[0])
        # 侧栏的字号是建列表项时写上去的, 不重建跟不上新倍率
        self.refresh_project_list()
        self._sync_font_scale_menu()
        self._fit_header()

    def _sync_header_more_menu(self):
        for name, act in zip(OVERFLOW_BTNS, self._header_overflow_actions):
            src = getattr(self, name)
            act.setText(src.text())
            act.setEnabled(src.isEnabled())

    def _fit_header(self):
        """顶栏装不下就收起那 4 个入口按钮.

        宽度按各控件自己的 sizeHint 求和(与可见性无关): 若按当前可见项算, 收起后需求
        变小、下一拍又该放开, 会来回抖.
        """
        if getattr(self, "_header_more_btn", None) is None:
            return
        lay = self.datasetHeaderLayout
        need = 0
        count = 0
        for i in range(lay.count()):
            item = lay.itemAt(i)
            wid = item.widget()
            if wid is None:
                need += item.sizeHint().width()      # 弹簧也要占它那份
                count += 1
                continue
            # 业务上隐藏的(训练进度条/停止按钮)不占位置; 我们收起来的那 4 个仍要计入
            if wid.isHidden() and wid.objectName() not in OVERFLOW_BTNS:
                continue
            need += wid.sizeHint().width()
            count += 1
        margins = lay.contentsMargins()
        need += lay.spacing() * max(0, count - 1) + margins.left() + margins.right()
        collapsed = need > self.datasetHeader.width()
        if collapsed == self._header_collapsed:
            return
        self._header_collapsed = collapsed
        for name in OVERFLOW_BTNS:
            getattr(self, name).setVisible(not collapsed)
