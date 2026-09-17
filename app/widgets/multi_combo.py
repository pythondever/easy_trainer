"""
多选下拉: 收起态是一排可删的标签, 列表用色点区分项目.

QComboBox 撑不起这个样式 - item view 的 ::indicator 只能改尺寸和贴图, 画不出实心
圆角块, 收起态也放不进 widget(编辑区只能是 QLineEdit). 所以列表交给 delegate 自绘,
编辑区换成自绘标签的 ChipLineEdit, 两者都直接读 model 的勾选状态, 不碰文本.
"""

from PySide6.QtCore import QEvent, QObject, QPointF, QRectF, QSize, Qt, QTimer
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import (QColor, QFont, QFontMetrics, QPainter, QPainterPath,
                           QPen, QPolygonF)
from PySide6.QtWidgets import QLineEdit, QStyle, QStyledItemDelegate

ROLE_DATASET = Qt.UserRole
CHECKED_VALUE = Qt.CheckState.Checked.value


def is_checked(state):
    """勾选状态判真, 两种形态都要认.

    同一个 CheckStateRole, 存进去的方式不同, 取出来的类型就不同:
    item.setCheckState() 存 -> index.data() 给裸 int; model.setData(..., Qt.Checked)
    存 -> 给 Qt.CheckState 枚举(普通 Enum, 与 int 不相等). 两种写法都在用, 只认一种会漏.
    """
    if state is None:
        return False
    if isinstance(state, int):
        return state == CHECKED_VALUE
    return state == Qt.Checked


ROW_H = 30              # 列表行高
MIN_POPUP_W = 300       # 列表最小宽度: 窄控件上也要能完整显示"项目/数据集"
CHIP_H = 22             # 收起态标签高
CHIP_RADIUS = 5
CHIP_PAD = 6            # 标签内左右留白
CHIP_GAP = 6            # 标签间距
DOT = 6                 # 列表行首的项目色点
CHIP_DOT = 5            # 标签里的色点
MARK = 16               # 行尾勾选圈
CROSS = 7               # 标签上的删除叉
LIST_FONT_PX = 12
CHIP_FONT_PX = 11

# 项目色按在列表里出现的顺序取用, 相邻项目不会撞色; 超出色板长度后从头循环
PROJECT_COLORS = ("#4f7dff", "#9a7bff", "#33c2a0", "#e0a34d", "#e8708a", "#5aa9e6")

PROJECT_TEXT = "#7f8a9e"
SEP_TEXT = "#525a6b"
NAME_TEXT = "#c8cdd8"
NAME_TEXT_CHECKED = "#e3e7f0"
HOVER_BG = "#262a34"
PLACEHOLDER_TEXT = "#5c6270"
MARK_BORDER = "#464d5e"
MARK_BORDER_HOVER = "#5a6379"


def project_colors(model):
    """项目名 → 颜色, 只认确实出现在该模型里的项目."""
    out = {}
    for i in range(model.rowCount()):
        item = model.item(i)
        if item is None:
            continue
        data = item.data(ROLE_DATASET)
        if isinstance(data, tuple) and len(data) == 2 and data[0] not in out:
            out[data[0]] = PROJECT_COLORS[len(out) % len(PROJECT_COLORS)]
    return out


def checked_rows(model):
    """勾选的项, [(行号, 项目, 数据集, 颜色), ...], 按列表顺序."""
    colors = project_colors(model)
    out = []
    for i in range(model.rowCount()):
        item = model.item(i)
        if item is None or not is_checked(item.checkState()):
            continue
        data = item.data(ROLE_DATASET)
        if isinstance(data, tuple) and len(data) == 2:
            color = colors.get(data[0], PROJECT_COLORS[0])
            out.append((i, data[0], data[1], QColor(color)))
    return out


def toggle_row(index):
    """切一下这一行的勾选."""
    if not index.isValid():
        return
    model = index.model()
    if model is None or not (model.flags(index) & Qt.ItemIsUserCheckable):
        return
    state = index.data(Qt.CheckStateRole)
    if state is None:
        return
    want = Qt.Unchecked if is_checked(state) else Qt.Checked
    # 与各处填充代码一样走 item: model.setData 会把状态存成枚举, 之后 data() 也取回枚举
    item_of = getattr(model, "item", None)
    item = item_of(index.row(), index.column()) if callable(item_of) else None
    if item is not None:
        item.setCheckState(want)
        return
    model.setData(index, want, Qt.CheckStateRole)


class _ClickToggleFilter(QObject):
    """列表里按下就切换这一行的勾选.

    三条路都试过, 只有这条稳:
    - delegate.editorEvent: 基类实现只认点在勾选框那个小方框内, 而勾选圈画在行右端, 位置对不上;
      重写它也不行 - 松开鼠标的事件被下拉容器吞掉(它拿这个事件去关列表), 根本走不到 release.
    - view.pressed 信号: 首次展开列表的那一次按下不发这个信号, 用户要点两次才生效.
    - 按下事件: 一定会到达 viewport, 在这里切最可靠.
    """

    def __init__(self, combo):
        super().__init__(combo)
        self._combo = combo

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            view = self._combo.view()
            if view is not None:
                toggle_row(view.indexAt(event.position().toPoint()))
        return False      # 不拦, 剩下的交给容器(它要拿松开事件去关列表)


class MultiComboDelegate(QStyledItemDelegate):
    """列表行: 行首项目色点 + 项目名/数据集名 + 行尾勾选圈.

    整行自己画, 所以不做 super().paint() - 否则 QSS 里 ::item 那套会盖在下面.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._colors = {}
        self._cache_key = None

    def sizeHint(self, option, index):
        return QSize(MIN_POPUP_W, ROW_H)

    def _color_map(self, model):
        # 颜色只跟项目出现的顺序有关, 与勾选无关, 所以按 (model, 行数) 缓存就够了
        key = (id(model), model.rowCount())
        if key != self._cache_key:
            self._colors = project_colors(model)
            self._cache_key = key
        return self._colors

    def paint(self, p, option, index):
        model = index.model()
        colors = self._color_map(model)
        data = index.data(ROLE_DATASET)
        if isinstance(data, tuple) and len(data) == 2:
            project, name = data
        else:
            project, name = "", str(index.data(Qt.DisplayRole) or "")
        color = QColor(colors.get(project, PROJECT_COLORS[0]))
        checked = is_checked(index.data(Qt.CheckStateRole))
        hovered = bool(option.state & QStyle.State_MouseOver)

        rect = option.rect
        row = QRectF(rect).adjusted(2, 1, -2, -1)
        p.save()
        p.setRenderHint(QPainter.Antialiasing)
        if checked or hovered:
            path = QPainterPath()
            path.addRoundedRect(row, 5, 5)
            if checked:
                fill = QColor(color)
                fill.setAlpha(26)
                p.fillPath(path, fill)
            else:
                p.fillPath(path, QColor(HOVER_BG))

        cy = rect.center().y() + 0.5
        p.setPen(Qt.NoPen)
        p.setBrush(color)
        p.drawEllipse(QRectF(row.x() + 9, cy - DOT / 2.0, DOT, DOT))

        # 勾选圈占住右边, 先把它和两侧留白扣掉, 剩下的才是文字可用宽
        mark_cx = rect.right() - 12 - MARK / 2.0
        font = QFont(p.font())
        font.setPixelSize(LIST_FONT_PX)
        p.setFont(font)
        fm = QFontMetrics(font)
        left = row.x() + 9 + DOT + 5
        avail = mark_cx - MARK / 2.0 - 10 - left
        sep_w = fm.horizontalAdvance("/")
        # 项目名先分四成, 其余留给数据集名 - 项目名短、数据集名才是要看清的那个
        project_txt = fm.elidedText(project, Qt.ElideRight, max(28, int(avail * 0.42)))
        proj_w = fm.horizontalAdvance(project_txt)
        name_txt = fm.elidedText(
            name, Qt.ElideRight, max(28, avail - proj_w - sep_w - 6))

        p.setPen(QColor(PROJECT_TEXT))
        p.drawText(QRectF(left, rect.top(), proj_w, rect.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, project_txt)
        p.setPen(QColor(SEP_TEXT))
        p.drawText(QRectF(left + proj_w, rect.top(), sep_w, rect.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, "/")
        p.setPen(QColor(NAME_TEXT_CHECKED if checked else NAME_TEXT))
        p.drawText(QRectF(left + proj_w + sep_w + 1, rect.top(),
                          avail - proj_w - sep_w, rect.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, name_txt)

        mark = QRectF(mark_cx - MARK / 2.0, cy - MARK / 2.0, MARK, MARK)
        if checked:
            p.setPen(Qt.NoPen)
            p.setBrush(color)
            p.drawEllipse(mark)
            pen = QPen(QColor("#ffffff"), 1.8)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            p.drawPolyline(QPolygonF([
                QPointF(mark_cx - 3.4, cy),
                QPointF(mark_cx - 1.0, cy + 2.5),
                QPointF(mark_cx + 3.5, cy - 2.4)]))
        else:
            p.setPen(QPen(QColor(MARK_BORDER_HOVER if hovered else MARK_BORDER), 1.5))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(mark)
        p.restore()


class ChipLineEdit(QLineEdit):
    """收起态: 每个勾选项画成一个带删除叉的标签, 放不下就收成 +n.

    点击叉取消该项勾选, 交给 model 发 itemChanged, 调用方原有的刷新逻辑会重画.
    """

    def __init__(self, combo, placeholder):
        super().__init__(combo)
        self._combo = combo
        self._cross = []
        self.setObjectName("multiComboLineEdit")
        self.setReadOnly(True)
        self.setPlaceholderText(placeholder)
        # 标签是自己画的, 别显示出文本光标
        self.setCursor(Qt.ArrowCursor)

    def _chips(self):
        model = self._combo.model()
        return [] if model is None else checked_rows(model)

    def _draw_chip(self, p, x, cy, height, name, color, row_i):
        fm = QFontMetrics(p.font())
        text_w = fm.horizontalAdvance(name)
        width = CHIP_PAD + CHIP_DOT + 5 + text_w + 5 + CROSS + CHIP_PAD
        box = QRectF(x, cy - height / 2.0, width, height)
        path = QPainterPath()
        path.addRoundedRect(box, CHIP_RADIUS, CHIP_RADIUS)
        fill = QColor(color)
        fill.setAlpha(41)
        p.fillPath(path, fill)
        edge = QColor(color)
        edge.setAlpha(120)
        p.setPen(QPen(edge, 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

        p.setPen(Qt.NoPen)
        p.setBrush(color)
        p.drawEllipse(QRectF(x + CHIP_PAD, cy - CHIP_DOT / 2.0, CHIP_DOT, CHIP_DOT))

        p.setPen(QColor(color).lighter(155))
        text_x = x + CHIP_PAD + CHIP_DOT + 5
        p.drawText(QRectF(text_x, cy - height / 2.0, text_w, height),
                   Qt.AlignVCenter | Qt.AlignLeft, name)

        cross_cx = text_x + text_w + 5 + CROSS / 2.0
        pen = QPen(QColor(color).lighter(125), 1.5)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        half = CROSS / 2.0 - 0.8
        p.drawLine(QPointF(cross_cx - half, cy - half), QPointF(cross_cx + half, cy + half))
        p.drawLine(QPointF(cross_cx + half, cy - half), QPointF(cross_cx - half, cy + half))
        # 命中区比图形本身宽一档, 免得非要点准那两条线
        self._cross.append(
            (QRectF(cross_cx - CROSS, cy - height / 2.0, CROSS * 2, height), row_i))
        return width

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self._cross = []
        rect = self.rect()
        font = QFont(self.font())
        font.setPixelSize(CHIP_FONT_PX)
        p.setFont(font)
        rows = self._chips()
        if not rows:
            p.setPen(QColor(PLACEHOLDER_TEXT))
            p.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, self.placeholderText())
            return

        fm = QFontMetrics(font)
        height = min(CHIP_H, max(rect.height() - 2, 16))
        cy = rect.center().y() + 0.5
        x = rect.x()
        right = rect.right() + 1
        for pos, (row_i, _project, name, color) in enumerate(rows):
            text_w = fm.horizontalAdvance(name)
            width = CHIP_PAD + CHIP_DOT + 5 + text_w + 5 + CROSS + CHIP_PAD
            rest = len(rows) - pos
            if x + width > right:
                self._draw_more(p, x, rect, rest)
                break
            # 这个标签放得下, 但画完它之后若还有剩, 得给 +n 留位置
            more_w = 0
            if rest > 1:
                more_w = CHIP_GAP + fm.horizontalAdvance("+{}".format(rest - 1))
            if x + width + more_w > right:
                self._draw_more(p, x, rect, rest)
                break
            self._draw_chip(p, x, cy, height, name, color, row_i)
            x += width + CHIP_GAP

    def _draw_more(self, p, x, rect, count):
        p.setPen(QColor(PLACEHOLDER_TEXT))
        p.drawText(QRectF(x, rect.y(), 40, rect.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, "+{}".format(count))

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            super().mousePressEvent(event)
            return
        for box, row_i in self._cross:
            if box.contains(event.position()):
                model = self._combo.model()
                item = model.item(row_i) if model is not None else None
                if item is not None:
                    item.setCheckState(Qt.Unchecked)
                event.accept()
                return
        # 其余位置沿用"点框内任意位置展开"; 原来的过滤器随旧 lineEdit 一起没了
        QTimer.singleShot(0, self._combo.showPopup)
        event.accept()


def install_multi_combo(combo, placeholder=None):
    """就地改造成多选下拉, 列表样式挂在 view 上, 与 model 无关, setModel 前后调用都行."""
    combo.setProperty("multiCombo", True)
    combo.setEditable(True)
    combo.setFocusPolicy(Qt.StrongFocus)
    combo.setLineEdit(ChipLineEdit(
        combo, placeholder or QC.translate("MultiCombo", "请选择数据集")))
    view = combo.view()
    if view is not None:
        view.setItemDelegate(MultiComboDelegate(view))
        # 不打开就收不到 State_MouseOver, 行没有悬停反馈
        view.setMouseTracking(True)
        view.viewport().installEventFilter(_ClickToggleFilter(combo))
    return combo
