# -*- coding: utf-8 -*-
"""首页标签筛选: 收起态按钮 + 点击弹出的平铺多选面板.

QComboBox 自带弹层是单列 item view, 画不出"圆形色块 + 名字 + 圆形勾选框"的平铺
网格; 收起态也没法按当前选择换色点. 于是两者都自绘:
  LabelFilterButton - .ui 里 promote 成它, 收起态 = 色点 + 文案 + 下箭头
  LabelFilterPanel  - Qt.Popup 浮层, "所有图像"整行 + 标签网格 + 自绘滚动条
"所有图像"与标签互斥: 选它则标签整体置灰不可点, 选了标签则它置灰不可点.
"""

from PySide6.QtCore import QPoint, QPointF, QRect, QRectF, Qt, Signal
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import (QColor, QFont, QFontMetrics, QPainter, QPainterPath,
                           QPen, QPolygonF)
from PySide6.QtWidgets import QApplication, QToolButton, QWidget

BTN_H = 32
BTN_PAD = 12
BTN_ARROW = 9
BTN_GAP = 6
BTN_MAX_W = 180

PANEL_W = 330
PAD = 10
SHADOW = 6              # 手绘投影占的边距, 弹层没有系统阴影
ROW_H = 26
COLS = 3
VISIBLE_ROWS = 3
MAX_EXPANDED_ROWS = 10  # 展开也不能顶穿屏幕, 超出仍走滚动
SCROLL_W = 13
SCROLL_GAP = 6
ALL_H = 28
SEP_GAP = 7
EXPAND_H = 22
ROW_GAP = 6
DOT = 15
CHECK = 15
LIST_FONT_PX = 12

ALL_COLOR = "#e03737"
DIM_DOT = "#5c6270"

BG = "#23262f"
BORDER = "#3a3f4e"
SEP = "#31353f"
TEXT = "#e8eaf0"
TEXT_SUB = "#8b93a5"
TEXT_DIM = "#55555e"
HOVER_BG = "#2b2f3b"
TRACK = "#1e1e26"
SLIDER = "#55555f"
SLIDER_HOVER = "#6a6a75"
CHECK_BORDER = "#464d5e"
CHECK_BORDER_HOVER = "#5a6379"
CHECK_BORDER_DIM = "#3a3a40"
ARROW_DIM = "#4a5164"


def _is_dark(color):
    """深色圆点(未标注的黑块)在深底上看不见, 需要补一圈描边."""
    return QColor(color).lightness() < 40


class LabelFilterButton(QToolButton):
    """收起态: 色点 + 文案 + 下箭头. 整块自绘, 胶囊底色与工具栏按钮同高."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self._text = QC.translate("LabelFilter", "所有图像")
        self._color = QColor(ALL_COLOR)
        self._dim = False
        self._candidates = [self._text]
        self._hover = False
        self.setFixedHeight(BTN_H)
        self._fit_width()

    def _font(self):
        f = QFont(self.font())
        f.setPixelSize(13)
        return f

    def set_state(self, text, color, dim):
        self._text = text
        self._color = QColor(color)
        self._dim = dim
        self.update()

    def set_candidates(self, texts):
        """按最宽候选文案定宽, 免得每次换选择整排工具栏跟着横移."""
        texts = [t for t in texts if t]
        self._candidates = texts or [self._text]
        self._fit_width()

    def _fit_width(self):
        fm = QFontMetrics(self._font())
        widest = max(fm.horizontalAdvance(t) for t in self._candidates)
        w = 2 * BTN_PAD + DOT + BTN_GAP + widest + BTN_GAP + BTN_ARROW
        self.setFixedWidth(min(max(w, BTN_H), BTN_MAX_W))

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, 14, 14)
        p.fillPath(path, QColor(BG))
        p.setPen(QPen(QColor("#4a5164" if self._hover else "#353a48"), 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

        cy = rect.center().y() + 0.5
        dot = QRectF(rect.x() + BTN_PAD, cy - DOT / 2.0, DOT, DOT)
        fill = QColor(self._color)
        if self._dim:
            fill.setAlpha(110)
        p.setPen(Qt.NoPen)
        p.setBrush(fill)
        p.drawEllipse(dot)
        if _is_dark(self._color):
            p.setPen(QPen(QColor(CHECK_BORDER), 1))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(dot)

        avail = (rect.width() - 2 * BTN_PAD - DOT - BTN_GAP
                 - BTN_GAP - BTN_ARROW)
        font = self._font()
        p.setFont(font)
        p.setPen(QColor(TEXT_DIM if self._dim else TEXT))
        p.drawText(QRectF(rect.x() + BTN_PAD + DOT + BTN_GAP, rect.y(),
                          avail, rect.height()),
                   Qt.AlignVCenter | Qt.AlignLeft,
                   QFontMetrics(font).elidedText(self._text, Qt.ElideRight,
                                                 max(10, int(avail))))

        ax = rect.right() - BTN_PAD - BTN_ARROW
        pen = QPen(QColor(TEXT_SUB), 1.6)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        half = BTN_ARROW / 2.0
        p.drawLine(QPointF(ax, cy - 2.2), QPointF(ax + half, cy + 2.2))
        p.drawLine(QPointF(ax + half, cy + 2.2), QPointF(ax + BTN_ARROW, cy - 2.2))


class LabelFilterPanel(QWidget):
    """点击筛选按钮弹出的平铺标签面板, 勾选互不影响(多选).

    filterChanged(all_mode, keys): all_mode 为真表示"所有图像", 此时 keys 为空.
    """

    filterChanged = Signal(bool, list)

    def __init__(self, parent=None):
        # 少了 Frameless 这一位, Windows 上透明属性不生效, 圆角外会显示成不透明黑块
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint
                         | Qt.NoDropShadowWindowHint)
        self.setObjectName("labelFilterPanel")
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._items = []            # [(名字, 颜色, key)]
        self._all = True
        self._sel = []
        self._top_row = 0
        self._expanded = False
        self._hover = None
        self._drag = None           # 滑块拖动时的抓取偏移
        self._geo = {}
        self._col_x = []
        self._col_w = []
        self._rows_total = 0
        self._rows_visible = 0
        self._rebuild_geom()

    # ---------------- 外部接口 ----------------

    def set_labels(self, items):
        """items: [(名字, 颜色, key)], 顺序即网格顺序."""
        self._items = list(items)
        valid = {key for _n, _c, key in self._items}
        self._sel = [k for k in self._sel if k in valid]
        if not self._sel and not self._all:
            self._all = True
        self._rebuild_geom()
        self.update()

    def set_state(self, all_mode, selected):
        self._all = bool(all_mode)
        self._sel = [] if self._all else list(selected)
        self.update()

    def popup_below(self, btn):
        """贴按钮下沿展开, 右边/下边放不下就往回收, 再不行翻到按钮上方."""
        self._rebuild_geom()
        gp = btn.mapToGlobal(QPoint(0, btn.height() + 4))
        scr = QApplication.screenAt(gp) or QApplication.primaryScreen()
        if scr is not None:
            avail = scr.availableGeometry()
            x = max(avail.left() + 4,
                    min(gp.x(), avail.right() - self.width() - 4))
            y = gp.y()
            if y + self.height() > avail.bottom():
                upper = gp.y() - btn.height() - 8 - self.height()
                y = (upper if upper >= avail.top()
                     else max(avail.top() + 4, avail.bottom() - self.height() - 4))
            gp = QPoint(x, y)
        self.move(gp)
        self.show()
        self.raise_()

    # ---------------- 几何 ----------------

    def _rebuild_geom(self):
        rows_total = ((len(self._items) + COLS - 1) // COLS) if self._items else 0
        limit = MAX_EXPANDED_ROWS if self._expanded else VISIBLE_ROWS
        rows_visible = min(rows_total, limit) or 1
        need_scroll = rows_total > rows_visible
        self._rows_total = rows_total
        self._rows_visible = rows_visible
        self._top_row = max(0, min(self._top_row,
                                   max(0, rows_total - rows_visible)))

        left = SHADOW + PAD
        right = SHADOW + PANEL_W - PAD
        content_w = right - left
        y = SHADOW + PAD
        geo = {"all": QRect(left, y, content_w, ALL_H)}
        y += ALL_H
        geo["sep"] = y + SEP_GAP
        y = geo["sep"] + 1 + SEP_GAP

        grid_w = content_w - (SCROLL_W + SCROLL_GAP if need_scroll else 0)
        grid_h = rows_visible * ROW_H
        geo["grid"] = QRect(left, y, grid_w, grid_h)
        if need_scroll:
            sx = right - SCROLL_W
            geo["scroll"] = QRect(sx, y, SCROLL_W, grid_h)
            geo["up"] = QRect(sx, y, SCROLL_W, SCROLL_W)
            geo["down"] = QRect(sx, y + grid_h - SCROLL_W, SCROLL_W, SCROLL_W)
            geo["track"] = QRect(sx, y + SCROLL_W,
                                 SCROLL_W, grid_h - 2 * SCROLL_W)
            geo["slider"] = self._slider_rect(geo["track"], rows_visible)
        else:
            geo["scroll"] = None
            geo["up"] = geo["down"] = geo["track"] = geo["slider"] = QRect()
        y = y + grid_h + ROW_GAP
        geo["expand"] = QRect(left, y, content_w, EXPAND_H)
        y += EXPAND_H + PAD + SHADOW

        cell = grid_w / float(COLS)
        self._col_x = [geo["grid"].x() + int(i * cell) for i in range(COLS)]
        self._col_w = [int((i + 1) * cell) - int(i * cell) for i in range(COLS)]
        self._geo = geo
        self.setFixedSize(PANEL_W + 2 * SHADOW, y)

    def _slider_rect(self, track, rows_visible):
        if track.height() <= 0 or self._rows_total <= rows_visible:
            return QRect(track.x() + 2, track.y(), track.width() - 4,
                         max(16, track.height()))
        ratio = rows_visible / float(self._rows_total)
        h = max(18, int(track.height() * ratio))
        room = track.height() - h
        span = max(1, self._rows_total - rows_visible)
        top = track.y() + int(room * (self._top_row / float(span)))
        return QRect(track.x() + 2, top, track.width() - 4, h)

    def _chip_rect(self, idx):
        row, col = divmod(idx, COLS)
        g = self._geo["grid"]
        return QRect(self._col_x[col], g.y() + (row - self._top_row) * ROW_H,
                     self._col_w[col], ROW_H)

    def _chip_at(self, pos):
        g = self._geo["grid"]
        if not g.contains(pos):
            return None
        row_in = (pos.y() - g.y()) // ROW_H
        if not (0 <= row_in < self._rows_visible):
            return None
        for col in range(COLS):
            if self._col_x[col] <= pos.x() < self._col_x[col] + self._col_w[col]:
                idx = (self._top_row + row_in) * COLS + col
                return idx if 0 <= idx < len(self._items) else None
        return None

    def _scroll_room(self):
        return max(0, self._rows_total - self._rows_visible)

    # ---------------- 交互 ----------------

    def _toggle_all(self):
        if not (self._all or not self._sel):
            return                      # 已选标签时"所有图像"置灰不可点
        self._all = not self._all
        if self._all:
            self._sel = []
        self._emit()

    def _toggle_chip(self, idx):
        if self._all:
            return                      # "所有图像"模式下标签整体置灰
        key = self._items[idx][2]
        if key in self._sel:
            self._sel.remove(key)
        else:
            self._sel.append(key)
        self._emit()

    def _emit(self):
        self.update()
        self.filterChanged.emit(self._all, list(self._sel))

    def _scroll(self, rows):
        room = self._scroll_room()
        if room <= 0:
            return
        self._top_row = max(0, min(self._top_row + rows, room))
        self._rebuild_geom()
        self.update()

    def _slide_to(self, y):
        track, slider = self._geo["track"], self._geo["slider"]
        room = self._scroll_room()
        if room <= 0 or track.height() <= slider.height():
            return
        span = track.height() - slider.height()
        rel = y - (self._drag or 0) - track.y()
        rel = max(0, min(rel, span))
        self._top_row = int(round(rel / float(span) * room))
        self._rebuild_geom()
        self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            super().mousePressEvent(event)
            return
        pos = event.position().toPoint()
        geo = self._geo
        if geo["all"].contains(pos):
            self._toggle_all()
            return
        idx = self._chip_at(pos)
        if idx is not None:
            self._toggle_chip(idx)
            return
        if geo["scroll"] is not None and geo["scroll"].contains(pos):
            if geo["up"].contains(pos):
                self._scroll(-1)
            elif geo["down"].contains(pos):
                self._scroll(1)
            elif geo["slider"].contains(pos):
                self._drag = pos.y() - geo["slider"].y()
            elif geo["track"].contains(pos):
                self._drag = geo["slider"].height() // 2
                self._slide_to(pos.y())
            return
        if geo["expand"].contains(pos):
            self._expanded = not self._expanded
            self._rebuild_geom()
            self.update()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        if self._drag is not None:
            self._slide_to(pos.y())
            return
        hover = self._hit(pos)
        if hover != self._hover:
            self._hover = hover
            self.update()

    def mouseReleaseEvent(self, event):
        self._drag = None
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        if self._geo["scroll"] is None:
            super().wheelEvent(event)
            return
        self._scroll(-1 if event.angleDelta().y() > 0 else 1)
        event.accept()

    def leaveEvent(self, event):
        self._hover = None
        self.update()
        super().leaveEvent(event)

    def _hit(self, pos):
        geo = self._geo
        if geo["all"].contains(pos):
            return ("all",)
        idx = self._chip_at(pos)
        if idx is not None:
            return ("chip", idx)
        if geo["scroll"] is not None and geo["scroll"].contains(pos):
            if geo["up"].contains(pos):
                return ("up",)
            if geo["down"].contains(pos):
                return ("down",)
            if geo["slider"].contains(pos):
                return ("slider",)
            return ("track",)
        if geo["expand"].contains(pos):
            return ("expand",)
        return None

    # ---------------- 绘制 ----------------

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for i in range(SHADOW, 0, -1):
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0, 9 * (SHADOW - i + 1)))
            p.drawRoundedRect(self.rect().adjusted(i, i, -i, -i), 9, 9)

        body = QRectF(self.rect().adjusted(SHADOW, SHADOW, -SHADOW, -SHADOW))
        path = QPainterPath()
        path.addRoundedRect(body, 8, 8)
        p.fillPath(path, QColor(BG))
        p.setPen(QPen(QColor(BORDER), 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

        font = QFont(p.font())
        font.setPixelSize(LIST_FONT_PX)
        p.setFont(font)

        geo = self._geo
        self._paint_all_row(p)
        p.setPen(QPen(QColor(SEP), 1))
        p.drawLine(QPoint(geo["all"].x(), geo["sep"]),
                   QPoint(geo["all"].right(), geo["sep"]))

        p.save()
        p.setClipRect(geo["grid"])
        for idx in range(len(self._items)):
            rect = self._chip_rect(idx)
            if rect.bottom() < geo["grid"].y() or rect.y() > geo["grid"].bottom():
                continue
            self._paint_chip(p, idx, rect)
        p.restore()

        if geo["scroll"] is not None:
            self._paint_scroll(p)
        self._paint_expand(p)

    def _paint_all_row(self, p):
        rect = self._geo["all"]
        enabled = self._all or not self._sel
        hovered = self._hover == ("all",) and enabled
        if hovered:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(HOVER_BG))
            p.drawRoundedRect(QRectF(rect).adjusted(0, 1, 0, -1), 5, 5)
        cy = rect.center().y() + 0.5
        fill = QColor(ALL_COLOR)
        if not enabled:
            fill.setAlpha(80)
        p.setPen(Qt.NoPen)
        p.setBrush(fill)
        p.drawEllipse(QRectF(rect.x() + 2, cy - DOT / 2.0, DOT, DOT))

        mark_cx = rect.right() - 2 - CHECK / 2.0
        text = QC.translate("LabelFilter", "所有图像")
        tx = rect.x() + 2 + DOT + 6
        fm = QFontMetrics(p.font())
        p.setPen(QColor(TEXT if enabled else TEXT_DIM))
        p.drawText(QRectF(tx, rect.y(),
                          mark_cx - CHECK / 2.0 - 10 - tx, rect.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, text)
        self._paint_status(p, fm, tx + fm.horizontalAdvance(text) + 8,
                           mark_cx - CHECK / 2.0 - 10)
        self._paint_mark(p, mark_cx, cy, ALL_COLOR, self._all, enabled, hovered)

    def _paint_status(self, p, fm, left, right):
        if self._all:
            text = QC.translate("LabelFilter", "显示全部图像")
        elif self._sel:
            text = QC.translate("LabelFilter", "按所选标签过滤")
        else:
            text = QC.translate("LabelFilter", "未选择标签")
        tw = fm.horizontalAdvance(text)
        if right - left < tw:
            return                      # 名字太长时让位给名字, 索性不显示状态
        p.setPen(QColor(TEXT_SUB))
        p.drawText(QRectF(left, self._geo["all"].y(), right - left,
                          self._geo["all"].height()),
                   Qt.AlignVCenter | Qt.AlignRight, text)

    def _paint_chip(self, p, idx, rect):
        name, color, key = self._items[idx]
        enabled = not self._all
        checked = key in self._sel
        hovered = enabled and self._hover == ("chip", idx)
        if hovered:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(HOVER_BG))
            p.drawRoundedRect(QRectF(rect).adjusted(0, 1, -1, -1), 5, 5)

        cy = rect.center().y() + 0.5
        dot = QRectF(rect.x() + 2, cy - DOT / 2.0, DOT, DOT)
        fill = QColor(color)
        if not enabled:
            fill.setAlpha(70)
        p.setPen(Qt.NoPen)
        p.setBrush(fill)
        p.drawEllipse(dot)
        if _is_dark(color) and enabled:
            p.setPen(QPen(QColor(CHECK_BORDER), 1))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(dot)

        mark_limit = rect.right() - 2 - CHECK   # 勾选框左边界最远只能到这儿
        tx = rect.x() + 2 + DOT + 6
        fm = QFontMetrics(p.font())
        # 名字最多占这么宽, 后面还得留得下勾选框; 钉在格子最右会让勾选框贴上
        # 下一格的色块, 所以让它跟着名字走
        avail = max(10, mark_limit - 6 - tx)
        text = fm.elidedText(name, Qt.ElideRight, int(avail))
        mark_cx = min(mark_limit, tx + fm.horizontalAdvance(text) + 6) + CHECK / 2.0
        p.setPen(QColor(TEXT_DIM if not enabled else TEXT))
        p.drawText(QRectF(tx, rect.y(), avail, rect.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, text)
        self._paint_mark(p, mark_cx, cy, color, checked, enabled, hovered)

    @staticmethod
    def _paint_mark(p, cx, cy, color, checked, enabled, hovered):
        mark = QRectF(cx - CHECK / 2.0, cy - CHECK / 2.0, CHECK, CHECK)
        if checked:
            fill = QColor(color)
            if not enabled:
                fill.setAlpha(70)
            p.setPen(Qt.NoPen)
            p.setBrush(fill)
            p.drawEllipse(mark)
            pen = QPen(QColor("#ffffff"), 1.8)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            p.drawPolyline(QPolygonF([
                QPointF(cx - 3.4, cy), QPointF(cx - 1.0, cy + 2.5),
                QPointF(cx + 3.5, cy - 2.4)]))
            return
        border = CHECK_BORDER_DIM if not enabled else (
            CHECK_BORDER_HOVER if hovered else CHECK_BORDER)
        p.setPen(QPen(QColor(border), 1.5))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(mark)

    def _paint_scroll(self, p):
        geo = self._geo
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(TRACK))
        p.drawRoundedRect(QRectF(geo["track"]), 6, 6)
        p.setBrush(QColor(SLIDER_HOVER if self._hover in (("slider",), ("track",))
                          else SLIDER))
        p.drawRoundedRect(QRectF(geo["slider"]), 4, 4)
        room = self._scroll_room()
        self._paint_arrow(p, geo["up"], True, self._top_row > 0)
        self._paint_arrow(p, geo["down"], False, self._top_row < room)

    @staticmethod
    def _paint_arrow(p, rect, up, enabled):
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(TEXT_SUB if enabled else ARROW_DIM))
        cx, cy = rect.center().x() + 0.5, rect.center().y() + 0.5
        s = 3.2
        pts = ([QPointF(cx - s, cy + s / 2), QPointF(cx, cy - s),
                QPointF(cx + s, cy + s / 2)] if up else
               [QPointF(cx - s, cy - s / 2), QPointF(cx, cy + s),
                QPointF(cx + s, cy - s / 2)])
        p.drawPolygon(QPolygonF(pts))

    def _paint_expand(self, p):
        rect = self._geo["expand"]
        hovered = self._hover == ("expand",)
        if hovered:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(HOVER_BG))
            p.drawRoundedRect(QRectF(rect).adjusted(0, 1, 0, -1), 5, 5)
        text = (QC.translate("LabelFilter", "收起") if self._expanded
                else QC.translate("LabelFilter", "展开全部"))
        p.setPen(QColor(TEXT if hovered else TEXT_SUB))
        p.drawText(QRectF(rect), Qt.AlignCenter, text)
