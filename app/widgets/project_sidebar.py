# -*- coding: utf-8 -*-
"""首页左侧项目/数据集导航：卡片式，替代原 QTreeWidget。

行内图标/数值/选中态全部由 DatasetRowDelegate 手绘，QSS 只管卡片容器；
导入/合并标签的任务进度也走 delegate(QStyleOptionProgressBar)，不再往行里塞控件。
"""
from PySide6.QtCore import Qt, QRectF, QPointF, QSize, Signal
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout,
                               QListWidget, QListWidgetItem, QStyledItemDelegate,
                               QStyle, QSizePolicy)

ROW_H = 28
CARD_RADIUS = 10
ROW_PAD_X = 12      # 行内容距卡片左右的内边距
NUM_PAD_R = 16      # 进度数值右缘距行内边的留白
TASK_BAR_W = 116    # 行内任务进度条宽度
CHIP_PAD_X = 6      # 进度整块色底的左右内边距
BADGE_PAD_R = ROW_PAD_X + NUM_PAD_R  # 徽标与进度数值右缘对齐在同一垂线
LIST_PAD_Y = 3                      # 数据集列表上下留白(走 viewport margin)

ROLE = Qt.UserRole


def _alpha_color(hex_color, alpha):
    c = QColor(hex_color)
    c.setAlpha(alpha)
    return c


def _draw_photo_icon(p, x, y, color):
    """13x13 单色线条照片图标。"""
    p.save()
    p.setPen(QPen(color, 1.1))
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(x + 0.6, y + 1.6, 12, 9.8), 2, 2)
    p.drawPolyline([QPointF(x + 2.6, y + 9.6), QPointF(x + 5.4, y + 6.4),
                    QPointF(x + 7.6, y + 8.4), QPointF(x + 9.2, y + 6.8),
                    QPointF(x + 11.2, y + 9.2)])
    p.drawEllipse(QRectF(x + 3.1, y + 3.3, 1.8, 1.8))
    p.restore()


def _draw_chevron(p, cx, cy, expanded, color):
    """9x5 细线三角。"""
    p.save()
    p.setPen(QPen(color, 1.2))
    p.setBrush(Qt.NoBrush)
    p.setRenderHint(QPainter.Antialiasing)
    if expanded:
        pts = [QPointF(cx - 4.5, cy - 2.2), QPointF(cx, cy + 2.2), QPointF(cx + 4.5, cy - 2.2)]
    else:
        pts = [QPointF(cx - 2.2, cy - 4.5), QPointF(cx + 2.2, cy), QPointF(cx - 2.2, cy + 4.5)]
    p.drawPolyline(pts)
    p.restore()


class DatasetRowDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        return QSize(100, ROW_H)

    def paint(self, p, option, index):
        data = index.data(ROLE) or {}
        st = option.state
        selected = bool(st & QStyle.State_Selected)
        hovered = bool(st & QStyle.State_MouseOver)
        row = option.rect.adjusted(ROW_PAD_X, 1, -ROW_PAD_X, -1)

        p.save()
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(row), 6, 6)
        if selected:
            p.fillPath(path, _alpha_color("#4f7dff", 36))
        elif hovered:
            p.fillPath(path, _alpha_color("#ffffff", 13))

        total = int(data.get("total") or 0)
        labeled = int(data.get("labeled") or 0)
        task = data.get("task")

        cx = row.x() + 8
        cy = option.rect.center().y()
        if total:
            icon_c = QColor("#cfd6e4") if selected else QColor("#8b93a5")
        else:
            icon_c = QColor("#6f7789")
        _draw_photo_icon(p, cx, cy - 6.5, icon_c)

        name_font = QFont()
        name_font.setPixelSize(13)
        num_font = QFont()
        num_font.setPixelSize(11)
        p.setFont(num_font)
        fm = QFontMetrics(num_font)
        w_total = fm.horizontalAdvance(str(total))
        w_slash = fm.horizontalAdvance(" / ")
        w_lab = fm.horizontalAdvance(str(labeled))
        w_num = w_lab + w_slash + w_total

        name_font_px = 13
        p.setFont(name_font)
        nfm = QFontMetrics(name_font)
        text_x = row.x() + 28
        num_right = row.right() - NUM_PAD_R
        avail_full = num_right - (w_num + CHIP_PAD_X * 2) - text_x - 8
        # 任务进度条占住数值区, 名称让位避免被盖住
        if task is not None:
            avail = num_right - TASK_BAR_W - text_x - 10
        else:
            avail = avail_full
        name = nfm.elidedText(data.get("dataset", ""), Qt.ElideRight, max(avail, 30))
        if selected:
            name_c = QColor("#ffffff")
        elif total == 0:
            name_c = QColor("#9aa2b4")
        else:
            name_c = QColor("#c9cfdc")
        p.setPen(name_c)
        p.drawText(QRectF(text_x, row.y(), avail, row.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, name)

        if task is not None:
            bar = QRectF(num_right - TASK_BAR_W, row.y() + 7,
                         TASK_BAR_W, row.height() - 14)
            path2 = QPainterPath()
            path2.addRoundedRect(QRectF(bar), 3, 3)
            p.fillPath(path2, _alpha_color("#5b8cff", 64))
            w = bar.width() * max(0, min(int(task), 100)) / 100.0
            if w > 0.5:
                chunk = QPainterPath()
                chunk.addRoundedRect(QRectF(bar.x(), bar.y(), w, bar.height()), 3, 3)
                p.fillPath(chunk, QColor("#4f7dff"))
            p.setFont(num_font)
            p.setPen(QColor("#ffffff"))
            p.drawText(QRectF(bar), Qt.AlignCenter, "{}%".format(int(task)))
        else:
            # labeled/total 整块: 标完绿底绿字, 未标完/未标黄底黄字
            done = total > 0 and labeled >= total
            chip_hex = "#7be39a" if done else "#ffd166"
            chip_w = w_num + CHIP_PAD_X * 2
            chip = QRectF(num_right - chip_w, option.rect.center().y() - 8,
                          chip_w, 16)
            chip_path = QPainterPath()
            chip_path.addRoundedRect(chip, 4, 4)
            p.fillPath(chip_path, _alpha_color(chip_hex, 72))
            c_lab = QColor(chip_hex)
            c_dim = _alpha_color(chip_hex, 150)
            x = num_right - CHIP_PAD_X
            p.setFont(num_font)
            self._draw_right(p, x, option.rect, str(total), c_dim)
            x -= w_total
            self._draw_right(p, x, option.rect, " / ", c_dim)
            x -= w_slash
            self._draw_right(p, x, option.rect, str(labeled), c_lab)
        p.restore()

    @staticmethod
    def _draw_right(p, x, rect, text, color):
        p.setPen(color)
        p.drawText(QRectF(x - 200, rect.y(), 200, rect.height()),
                   Qt.AlignVCenter | Qt.AlignRight, text)


class DatasetListWidget(QListWidget):
    contextRequested = Signal(object, object)  # 全局坐标

    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.setObjectName("datasetList")
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setMouseTracking(True)
        self.setSpacing(0)
        self.setUniformItemSizes(True)
        self.setItemDelegate(DatasetRowDelegate(self))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._emit_context)
        self.setViewportMargins(0, LIST_PAD_Y, 0, LIST_PAD_Y)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def _emit_context(self, pos):
        self.contextRequested.emit(self.itemAt(pos), self.viewport().mapToGlobal(pos))

    def sync_height(self):
        self.setFixedHeight(self.count() * ROW_H + LIST_PAD_Y * 2)


class ProjectCardHeader(QWidget):
    clicked = Signal()
    contextRequested = Signal(object)  # 全局坐标

    def __init__(self, project, parent=None):
        QWidget.__init__(self, parent)
        self.project = project
        self.expanded = True
        self.count = 0
        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(
            lambda pos: self.contextRequested.emit(self.mapToGlobal(pos)))

    def set_expanded(self, expanded):
        self.expanded = expanded
        self.update()

    def set_count(self, n):
        self.count = n
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        cy = self.height() / 2
        hover_c = QColor("#8b93a5") if self.underMouse() else QColor("#5a6273")
        _draw_chevron(p, 20, cy, self.expanded, hover_c)
        f = QFont()
        f.setPixelSize(13)
        p.setFont(f)
        p.setPen(QColor("#e8eaf0"))
        fm = QFontMetrics(f)
        # 数据集计数徽标：宽度按文字自适应，固定 20px 放不下两位数
        fs = QFont()
        fs.setPixelSize(11)
        fms = QFontMetrics(fs)
        badge_w = max(20, fms.horizontalAdvance(str(self.count)) + 14)
        badge_x = self.width() - BADGE_PAD_R - badge_w
        name_w = badge_x - 12 - 32
        p.drawText(QRectF(32, 0, name_w, self.height()),
                   Qt.AlignVCenter | Qt.AlignLeft,
                   fm.elidedText(self.project, Qt.ElideRight, name_w))
        rect = QRectF(badge_x, cy - 8, badge_w, 16)
        path = QPainterPath()
        path.addRoundedRect(rect, 4, 4)
        p.fillPath(path, _alpha_color("#ffffff", 15))
        p.setFont(fs)
        p.setPen(QColor("#8b93a5"))
        p.drawText(rect, Qt.AlignCenter, str(self.count))


class ProjectCard(QFrame):
    expandToggled = Signal(str, bool)  # project, expanded

    def __init__(self, project, datasets, expanded=False, parent=None):
        QFrame.__init__(self, parent)
        self.setObjectName("projectCard")
        self.project = project
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        self.header = ProjectCardHeader(project, self)
        self.header.clicked.connect(self.toggle)
        v.addWidget(self.header)

        # 上下留白走 list 的 viewport margin 而不是占位 QWidget:
        # 全局 QWidget 底色(#181a20)会把占位块染成一条黑缝
        self.list = DatasetListWidget(self)
        for ds_name, labeled, total in datasets:
            item = QListWidgetItem()
            item.setData(ROLE, {"project": project, "dataset": ds_name,
                                "labeled": labeled, "total": total, "task": None})
            self.list.addItem(item)
        self.list.sync_height()
        v.addWidget(self.list)

        self.header.set_count(len(datasets))
        self.set_expanded(expanded)

    def toggle(self):
        self.set_expanded(not self.expanded)
        self.expandToggled.emit(self.project, self.expanded)

    def set_expanded(self, expanded):
        self.expanded = expanded
        self.header.set_expanded(expanded)
        self.list.setVisible(expanded)
        # setVisible 不会自动让外层滚动容器按新 sizeHint 收缩,
        # 需手动 updateGeometry 通知父布局(QScrollArea widgetResizable 依赖它)
        self.updateGeometry()


class ProjectSidebar(QWidget):
    datasetClicked = Signal(str, str)
    projectClicked = Signal(str)
    datasetContextMenu = Signal(str, str, object)
    projectContextMenu = Signal(str, object)
    expandChanged = Signal(str, bool)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName("projectSidebar")
        self.cards = {}
        # 展开态只存内存: 刷新列表不丢, 重启后全部展开
        self._expanded = {}
        v = QVBoxLayout(self)
        v.setContentsMargins(12, 4, 12, 12)
        v.setSpacing(10)
        v.addStretch(1)
        line = QFrame(self)
        line.setObjectName("sidebarStatsLine")
        line.setFixedHeight(1)
        self.stats_line = line
        self.stats_lbl = QLabel(self)
        self.stats_lbl.setObjectName("sidebarStats")
        v.addWidget(line)
        v.addWidget(self.stats_lbl)

    def rebuild(self, data):
        """data: [(project, [(dataset, labeled, total), ...]), ...]"""
        current = self.current_dataset()
        v = self.layout()
        while v.count() > 3:
            item = v.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        self.cards = {}
        self._expanded = {k: v_ for k, v_ in self._expanded.items()
                          if k in [p for p, _ in data]}
        n_ds = 0
        for project, datasets in data:
            if project in self._expanded:
                expanded = self._expanded[project]
            elif current is not None and current[0] == project:
                expanded = True   # 当前选中数据集所在项目保持展开, 否则刷新后选中看不见
            else:
                expanded = False
            card = ProjectCard(project, datasets, expanded)
            card.expandToggled.connect(self._on_expand_changed)
            card.header.clicked.connect(
                lambda p=project: self._on_header_clicked(p))
            card.header.contextRequested.connect(
                lambda gpos, proj=project: self.projectContextMenu.emit(proj, gpos))
            card.list.contextRequested.connect(self._on_row_context)
            card.list.itemClicked.connect(self._on_row_clicked)
            v.insertWidget(0, card)
            self.cards[project] = card
            n_ds += len(datasets)
        self.stats_lbl.setText("{} 个项目 · {} 个数据集".format(len(data), n_ds))
        if current is not None:
            self.select_dataset(*current)

    def _on_expand_changed(self, project, expanded):
        self._expanded[project] = expanded
        self.expandChanged.emit(project, expanded)
        # 通知滚动容器按新内容高度重算(widgetResizable 不会主动缩小 widget,
        # 漏掉这步会出现: 内容已折叠但滚动条仍在, 其它卡的宽度也不同步)
        self.adjustSize()

    def _on_row_context(self, item, global_pos):
        if item is None:
            return
        d = item.data(ROLE)
        self.datasetContextMenu.emit(d["project"], d["dataset"], global_pos)

    def _on_row_clicked(self, item):
        # 各卡片是独立列表, 需手动清掉其它卡片的高亮, 保证全局只有一个选中项
        self.clear_selection(exclude=item.listWidget())
        d = item.data(ROLE)
        self.datasetClicked.emit(d["project"], d["dataset"])

    def _on_header_clicked(self, project):
        """点卡头 = 选中项目(取消数据集选中), 由外部清空右侧图像区。"""
        self.clear_selection()
        self.projectClicked.emit(project)

    def clear_selection(self, exclude=None):
        for card in self.cards.values():
            if card.list is exclude:
                continue
            card.list.blockSignals(True)
            card.list.setCurrentItem(None)
            card.list.clearSelection()
            card.list.blockSignals(False)

    def set_expanded(self, project, expanded):
        self._expanded[project] = expanded
        card = self.cards.get(project)
        if card is not None and card.expanded != expanded:
            card.set_expanded(expanded)

    def _find(self, project, dataset):
        card = self.cards.get(project)
        if card is None:
            return None
        for i in range(card.list.count()):
            item = card.list.item(i)
            if item.data(ROLE)["dataset"] == dataset:
                return item
        return None

    def set_row_progress(self, project, dataset, labeled, total):
        item = self._find(project, dataset)
        if item is None:
            return
        d = dict(item.data(ROLE))
        d["labeled"] = labeled
        d["total"] = total
        item.setData(ROLE, d)
        self._repaint_row(item)

    def set_row_task(self, project, dataset, value):
        """value 为 0-100 显示任务进度条，None 结束任务显示。"""
        item = self._find(project, dataset)
        if item is None:
            return
        d = dict(item.data(ROLE))
        d["task"] = value
        item.setData(ROLE, d)
        self._repaint_row(item)

    def select_dataset(self, project, dataset):
        card = self.cards.get(project)
        if card is None:
            return
        item = self._find(project, dataset)
        if item is not None:
            self.clear_selection(exclude=card.list)
            card.list.blockSignals(True)
            card.list.setCurrentItem(item)
            card.list.blockSignals(False)

    def current_dataset(self):
        for card in self.cards.values():
            item = card.list.currentItem()
            if item is not None:
                d = item.data(ROLE)
                return d["project"], d["dataset"]
        return None

    def _repaint_row(self, item):
        item.listWidget().viewport().update()
