# -*- coding: utf-8 -*-
"""主页图像区空态提示: 无数据时在画布中央显示图标与引导文案.

空态时 scene 清空后什么都不画, 图像区是一片死黑(bg_deep), 仅有的提示缩在
底栏分页行, 用户看不出下一步该做什么. 按三种空态(未选数据集 / 数据集无图 /
筛选无结果)分别给主文案与指路文案, 画法沿用标签统计空态(居中 + 弱化文字);
挂成 viewport 子控件并穿透鼠标, 不影响图区的点选与框选.
"""
import random

from PySide6.QtCore import QEvent, QRectF, Qt
from PySide6.QtGui import QColor, QFontMetrics, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget

from app.core import theme
from PySide6.QtCore import QCoreApplication as QC

# 每种空态一组文案: (主引导, 使用技巧). 进入空态时随机取一条,
# 让停留在此的界面也能顺手了解软件用法; 新增技巧往对应列表里加即可.
HINTS = {
    "no_dataset": [
        ("在左侧选择项目与数据集", "双击侧边栏的数据集即可载入图像"),
        ("在左侧选择项目与数据集", "右键项目可新建数据集"),
        ("还没有选中数据集", "右键数据集可导入图像与标签"),
        ("还没有选中数据集", "导入支持 Labelme json、YOLO txt 与分类文件夹"),
        ("从左侧选一个数据集开始", "双击缩略图可打开标注窗口"),
        ("从左侧选一个数据集开始", "悬停缩略图可查看图像完整路径"),
        ("在左侧选择项目与数据集", "顶栏可进入统计、训练、模型与队列"),
        ("在左侧选择项目与数据集", "顶栏右侧可切换中文与英文界面"),
    ],
    "no_image": [
        ("该数据集还没有图像", "右键数据集选择导入图像"),
        ("该数据集还没有图像", "导入支持 Labelme json、YOLO txt 与分类文件夹"),
        ("该数据集还没有图像", "分类导入时子文件夹名就是类别名"),
        ("这个数据集是空的", "右键数据集选择导入图像"),
        ("这个数据集是空的", "图像与标签可分开放, 导入时各选一个目录"),
        ("该数据集还没有图像", "导入完成后双击缩略图即可开始标注"),
    ],
    "no_filter": [
        ("当前筛选下没有图像", "在标签面板勾选类别, 或点「全选」"),
        ("当前筛选下没有图像", "选中标签后, 每个标注框单独占一个格子"),
        ("当前筛选下没有图像", "未标注的图像可勾「未标注」单独查看"),
        ("换一个标签试试", "在顶栏标签下拉里勾选要看的类别"),
        ("当前筛选下没有图像", "取消所有勾选会清空图区, 至少勾一项"),
        ("换一个标签试试", "标签按类别聚合, 一图多类会同时出现在各类下"),
    ],
}
ICONS = {"no_dataset": "tree", "no_image": "image", "no_filter": "filter"}

# 每种状态上次抽中的下标: 连续进入同一空态时不重复上一条
_LAST_PICK = {}

ICON = 28        # 图标边长
GAP_ICON = 12    # 图标与主文案的间距
MAIN_H = 22      # 主文案行高
GAP_SUB = 2      # 主副文案间距
SUB_H = 18       # 副文案行高


def hint_texts(key):
    """(主文案, 副文案): 从该状态的文案池随机取一条, 避开上次那条."""
    pool = HINTS.get(key) or HINTS["no_dataset"]
    idx = _LAST_PICK.get(key, -1)
    if len(pool) > 1:
        while idx == _LAST_PICK.get(key, -1):
            idx = random.randrange(len(pool))
    else:
        idx = 0
    _LAST_PICK[key] = idx
    main, sub = pool[idx]
    return QC.translate("EmptyHint", main), QC.translate("EmptyHint", sub)


class EmptyHintOverlay(QWidget):
    """空态浮层: 图标 + 主文案 + 副文案, 整体居于画布中央."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_text = ""
        self._sub_text = ""
        self._icon = "tree"
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(Qt.NoFocus)
        if parent is not None:
            parent.installEventFilter(self)
            self.resize(parent.size())
        self.hide()

    def set_hint(self, key):
        main, sub = hint_texts(key)
        self._main_text = main
        self._sub_text = sub
        self._icon = ICONS.get(key, "tree")
        self.setVisible(True)
        self.raise_()
        self.update()

    def clear_hint(self):
        self._main_text = ""
        self.hide()

    def eventFilter(self, obj, event):
        # 浮层铺满 viewport: 父控件一变大小就跟着撑开(否则文案会留在旧位置)
        if obj is self.parent() and event.type() == QEvent.Resize:
            self.resize(obj.size())
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        if not self._main_text:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        block = ICON + GAP_ICON + MAIN_H
        if self._sub_text:
            block += GAP_SUB + SUB_H
        top = max(0, (h - block) // 2)
        faint = QColor(theme.hexof("text_faint"))
        p.setPen(QPen(faint, 1))
        self._paint_icon(p, w // 2 - ICON // 2, top)
        y = top + ICON + GAP_ICON
        f = p.font()
        f.setPixelSize(13)
        p.setFont(f)
        fm = QFontMetrics(f)
        # 窗口缩到很窄时截断而不是溢出画布
        main_shown = fm.elidedText(self._main_text, Qt.ElideRight, w - 40)
        p.setPen(QColor(theme.hexof("text_2")))
        p.drawText(QRectF(0, y, w, MAIN_H), Qt.AlignCenter, main_shown)
        if self._sub_text:
            y += MAIN_H + GAP_SUB
            f.setPixelSize(11)
            p.setFont(f)
            fm = QFontMetrics(f)
            sub_shown = fm.elidedText(self._sub_text, Qt.ElideRight, w - 40)
            p.setPen(QColor(theme.hexof("text_3")))
            p.drawText(QRectF(0, y, w, SUB_H), Qt.AlignCenter, sub_shown)

    def _paint_icon(self, p, x, y):
        """三种线性小图标: 列表(未选) / 图片占位(无图) / 筛选(无结果)."""
        s = ICON
        p.setBrush(Qt.NoBrush)
        if self._icon == "filter":
            p.drawLine(x + 2, y + 7, x + s - 2, y + 7)
            p.drawLine(x + 6, y + 13, x + s - 6, y + 13)
            p.drawLine(x + 10, y + 19, x + s - 10, y + 19)
        elif self._icon == "image":
            p.drawRoundedRect(QRectF(x + 0.5, y + 0.5, s - 1, s - 1), 4, 4)
            p.setBrush(QColor(theme.hexof("text_faint")))
            p.drawEllipse(QRectF(x + s * 0.32 - 2, y + s * 0.32 - 2, 4, 4))
            p.setBrush(Qt.NoBrush)
            path = QPainterPath()
            path.moveTo(x + 3, y + s - 4)
            path.lineTo(x + s * 0.38, y + s * 0.50)
            path.lineTo(x + s * 0.56, y + s * 0.68)
            path.lineTo(x + s * 0.70, y + s * 0.54)
            path.lineTo(x + s - 3, y + s - 4)
            p.drawPath(path)
        else:
            p.drawRoundedRect(QRectF(x + 1.5, y + 1.5, s - 3, s - 3), 3, 3)
            p.drawLine(x + 6, y + 5, x + 6, y + s - 5)
            p.drawLine(x + 11, y + 9, x + s - 6, y + 9)
            p.drawLine(x + 11, y + 15, x + s - 6, y + 15)
            p.drawLine(x + 11, y + 21, x + s - 9, y + 21)
