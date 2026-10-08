# -*- coding: utf-8 -*-
"""多次训练结果对比: 三栏(记录 / 曲线+汇总表 / 差异与结论).

界面由 ui/compare.py 编译生成(Ui_CompareDialog), 这里 setupUi 填充数据.
曲线来源与单次指标窗口同源(metrics_dialog.load_run_series), 不重复
解析 metrics.csv / metrics.json; 绘制走自绘 CompareChart, 不用 matplotlib.
"""

import csv
import datetime as _dt
import os

from PySide6.QtCore import QEvent, QRect, QSize, Qt, QTimer
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog,
                               QFileDialog, QHeaderView, QListWidgetItem,
                               QMessageBox, QStyle, QStyledItemDelegate,
                               QTableWidgetItem)

from app.core import theme
from app.core.metrics import metric_key, primary_for
from app.train.dialogs import AUG_ITEMS
from app.widgets.combo_utils import style_combo
from app.widgets.compare_chart import CompareChart, series_color
from app.widgets.compare_diff import DiffPanel
from app.widgets.metrics_dialog import MetricsDialog, load_run_series
from app.widgets.metric_tabs import MetricTabs
from app.widgets.status_style import status_color, task_text
from ui.compare import Ui_CompareDialog

# 一次最多叠几条: 再多颜色分不清, 图例也会盖住曲线
MAX_SERIES = 8
# 指标 tab 的排序; 记录里实际存在的列才进候选, 没列到的排最后
METRIC_ORDER = (
    "mAP@50", "mAP@50-95", "ema_mAP@50", "ema_mAP@50-95",
    "mask_mAP@50", "mask_mAP@50-95", "mask_ema_mAP@50", "mask_ema_mAP@50-95",
    "precision", "recall", "F1", "mAR",
    "accuracy", "auroc", "F1@0.5", "CER", "WER",
    "train_loss", "val_loss",
)
# 汇总表固定列: 与设计稿一致, 不随当前对比指标变化
_COLUMNS = ("时间", "任务 / 模型", "数据集", "轮次", "批次", "学习率",
            "mAP@50", "precision", "recall", "F1@0.5", "训练时长", "增强")
# 汇总表里跟着当前指标标背景的列(表头列名 → 列号)
_CUR_COLUMN = {"mAP@50": 6, "precision": 7, "recall": 8, "F1@0.5": 9}

# 记录范围下拉: (界面文案, 判断键)
RANGE_ITEMS = (("全部记录", "all"), ("今天", "today"), ("昨天", "yesterday"),
               ("近7天", "7d"), ("近30天", "30d"))

# 任务键 → 卡片类型标签(文本, 底色, 前景色); ocr 系列本质是检测/识别, 标签沿用设计稿
TASK_TAG = {
    "detect": ("DETECT", "#12354f", "#6fc2ff"),
    "ocr": ("DETECT", "#12354f", "#6fc2ff"),
    "ocr_det": ("DETECT", "#12354f", "#6fc2ff"),
    "segment": ("SEG", "#3a2a10", "#f5b84c"),
    "classify": ("CLS", "#123a2d", "#52d6a8"),
    "ocr_rec": ("OCR", "#123a2d", "#52d6a8"),
    "ad": ("AD", "#1f2a3d", "#7c879c"),
}

# 主指标短名: 卡片右侧"F1 0.278"这类, 长名(如 mAP@50)放不下
_PRIMARY_SHORT = {"mAP@50": "mAP", "mask mAP50": "mAP", "准确率": "ACC",
                  "AUROC": "AUROC", "F1@0.5": "F1", "CER": "CER"}

# 非完成状态在卡片上的文案; 键是库里存的中文状态
_STATUS_LABEL = {"失败": "已失败", "失败/已停止": "已失败", "已停止": "已停止",
                 "已中断": "已中断", "已跳过": "已跳过"}

# QListWidgetItem 自定义角色: 卡片 delegate 自绘取数据用
ROLE_IDX = Qt.UserRole
ROLE_STATUS = Qt.UserRole + 1
ROLE_TIME = Qt.UserRole + 2
ROLE_TASK = Qt.UserRole + 3
ROLE_TAG = Qt.UserRole + 4
ROLE_MODEL = Qt.UserRole + 5
ROLE_BEST = Qt.UserRole + 6
ROLE_BAD = Qt.UserRole + 7

_AUG_NAMES = {code: name for _g, code, name, _p in AUG_ITEMS}
# 右栏差异里的增强太长会挤成几行, 超过两项就只列前两项
AUG_DIFF_MAX = 2


def _muted(size=13):
    return "color: {}; font-size: {}px;".format(theme.hexof("text_3"), size)


def _esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def _direction(key):
    """越大越好还是越小越好; 错误率与 loss 越小越好."""
    if key in ("CER", "WER") or "loss" in key.lower():
        return -1
    return 1


def _fmt(v, key):
    if v is None:
        return ""
    return "{:.4f}".format(v) if key in ("CER", "WER", "accuracy") \
        else "{:.3f}".format(v)


def _fmt_dur(secs):
    """秒数 → hh:mm:ss; 没有时长字段给空串."""
    try:
        secs = int(secs or 0)
    except (TypeError, ValueError):
        return ""
    if secs <= 0:
        return ""
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return "{:02d}:{:02d}:{:02d}".format(h, m, s)


def _time_short(t):
    t = str(t or "")
    return t[5:] if len(t) > 5 else t


def _aug_label(value):
    """增强值 → 中文名, 不增强给空串."""
    codes = [c.strip() for c in str(value or "").split(",")]
    names = [QC.translate("TrainDialog", _AUG_NAMES[c])
             for c in codes if c in _AUG_NAMES]
    if not names:
        return ""
    if len(names) > AUG_DIFF_MAX:
        return "+".join(names[:AUG_DIFF_MAX]) + "\u2026"
    return "+".join(names)


def _aug_codes(value):
    """增强值 → 英文代码列表, 表格列直接展示."""
    return [c.strip() for c in str(value or "").split(",") if c.strip()]


def _same_record(a, b):
    if a is None or b is None:
        return False
    aid, bid = a.get("id"), b.get("id")
    if aid and aid == bid:
        return True
    at, bt = a.get("start_time"), b.get("start_time")
    return bool(at) and at == bt


class _RecordDelegate(QStyledItemDelegate):
    """左侧训练记录卡片: 整卡自绘, 默认行样式会压扁卡片观感."""

    CARD = QSize(0, 76)

    def sizeHint(self, option, index):
        return self.CARD

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        r = option.rect.adjusted(2, 2, -2, -2)
        checked = index.data(Qt.CheckStateRole) == Qt.Checked
        bg = "#1c2433" if checked else "#1a2130"
        border = "#2b6ee8" if checked else "#28334a"
        if option.state & QStyle.State_MouseOver:
            bg = "#1e2838"
        painter.setPen(QPen(QColor(border), 1))
        painter.setBrush(QColor(bg))
        painter.drawRoundedRect(r, 8, 8)

        # 复选框: 勾选蓝底白勾, 未勾灰边框
        cb = QRect(r.left() + 10, r.top() + 10, 13, 13)
        if checked:
            painter.setBrush(QColor("#2b6ee8"))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(cb, 3, 3)
            painter.setPen(QPen(QColor("#ffffff"), 1.6))
            painter.drawLine(cb.left() + 3, cb.center().y(),
                             cb.left() + 6, cb.bottom() - 3)
            painter.drawLine(cb.left() + 6, cb.bottom() - 3,
                             cb.right() - 2, cb.top() + 3)
        else:
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor("#4a5670"), 1))
            painter.drawRoundedRect(cb, 3, 3)

        # 状态点
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(status_color(index.data(ROLE_STATUS))))
        painter.drawEllipse(QRect(r.left() + 30, r.top() + 12, 8, 8))

        # 第一行: 时间
        f_small = QFont(option.font)
        f_small.setPointSizeF(8.5)
        painter.setFont(f_small)
        painter.setPen(QColor("#77829a"))
        painter.drawText(QRect(r.left() + 43, r.top() + 4, r.width() - 60, 24),
                         Qt.AlignVCenter | Qt.AlignLeft,
                         str(index.data(ROLE_TIME) or ""))

        # 第二行: 任务名 + 类型标签
        f_name = QFont(option.font)
        f_name.setPointSizeF(10)
        f_name.setBold(True)
        painter.setFont(f_name)
        name = str(index.data(ROLE_TASK) or "")
        name_w = painter.fontMetrics().horizontalAdvance(name)
        name_rect = QRect(r.left() + 10, r.top() + 30, r.width() - 20, 24)
        painter.setPen(QColor("#e8edf6"))
        painter.drawText(name_rect, Qt.AlignVCenter | Qt.AlignLeft, name)
        tag_text, tag_bg, tag_fg = TASK_TAG.get(
            str(index.data(ROLE_TAG) or ""), ("", "#1f2a3d", "#7c879c"))
        if tag_text:
            tag_rect = QRect(name_rect.left() + name_w + 6, r.top() + 33,
                             painter.fontMetrics().horizontalAdvance(tag_text) + 14, 18)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(tag_bg))
            painter.drawRoundedRect(tag_rect, 4, 4)
            f_tag = QFont(f_name)
            f_tag.setPointSizeF(8)
            painter.setFont(f_tag)
            painter.setPen(QColor(tag_fg))
            painter.drawText(tag_rect, Qt.AlignCenter, tag_text)

        # 第三行: 模型名(左) + 主指标(右)
        f_meta = QFont(option.font)
        f_meta.setPointSizeF(8.5)
        painter.setFont(f_meta)
        painter.setPen(QColor("#77829a"))
        meta_rect = QRect(r.left() + 10, r.top() + 52, r.width() - 20, 20)
        painter.drawText(meta_rect, Qt.AlignVCenter | Qt.AlignLeft,
                         str(index.data(ROLE_MODEL) or ""))
        best = str(index.data(ROLE_BEST) or "")
        if best:
            f_best = QFont(option.font)
            f_best.setPointSizeF(9.5)
            f_best.setBold(True)
            painter.setFont(f_best)
            painter.setPen(QColor("#ff8aa0" if index.data(ROLE_BAD)
                                  else "#3ddc84"))
            painter.drawText(meta_rect, Qt.AlignVCenter | Qt.AlignRight, best)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        # 单击整卡切换勾选; 双击返回 False, 交给 QListWidget 发 itemDoubleClicked
        if (event.type() == QEvent.MouseButtonRelease
                and event.button() == Qt.LeftButton):
            state = (Qt.Unchecked if model.data(index, Qt.CheckStateRole) == Qt.Checked
                     else Qt.Checked)
            model.setData(index, state, Qt.CheckStateRole)
            return True
        return False


class CompareDialog(QDialog):
    """勾选若干条训练记录, 按同一指标叠图对比, 右侧列出差异与结论."""

    def __init__(self, db, records, current=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_CompareDialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint)
        self.db = db
        self._db_path = getattr(db, "db_path", None)
        self._records = sorted(
            list(records), key=lambda r: str(r.get("start_time") or ""),
            reverse=True)
        self._series = [load_run_series(r, self._db_path) for r in self._records]
        self._visible = list(range(len(self._records)))
        self._combo_filters = []
        self._metric = ""
        self._guard = False

        self.ui.metric_caption.setStyleSheet(_muted())
        self.ui.range_caption.setStyleSheet(_muted())
        self.ui.records_caption.setStyleSheet(_muted(12))
        self.ui.diff_caption.setStyleSheet(_muted(12))
        self.ui.chart_title_label.setStyleSheet(_muted(13))
        self.ui.table_title_label.setStyleSheet(_muted(13))
        self.ui.legend_label.setStyleSheet(_muted(11))
        self.ui.hint_label.setStyleSheet(_muted(12))
        self.ui.source_label.setStyleSheet(_muted(12))
        self.ui.status_legend_label.setStyleSheet(_muted(12))
        self.ui.selected_count_label.setStyleSheet(_muted(11))
        self.ui.selected_count_label.setAlignment(Qt.AlignCenter)

        # 底部固定文案: 状态色标 + 数据来源
        self.ui.source_label.setText(
            self.tr("数据来源：LMDB train_history + metrics.csv / metrics json"))
        self.ui.status_legend_label.setText(self._legend_html())

        self._tabs = MetricTabs(self.ui.metric_tabs_host)
        self.ui.metricTabsLayout.addWidget(self._tabs)
        self._tabs.metricChanged.connect(self._on_metric_changed)

        style_combo(self.ui.record_range_combo, self._combo_filters, self)
        self.ui.record_range_combo.currentIndexChanged.connect(
            self._on_range_changed)
        self._fill_range_combo()

        self._chart = CompareChart(self.ui.chart_container)
        self.ui.chartLayout.addWidget(self._chart)

        self._diff = DiffPanel(self.ui.diff_content)
        self.ui.diffLayout.addWidget(self._diff)
        # QScrollArea 的 widgetResizable 不认 heightForWidth, wrap 内容会被压扁
        self.ui.diff_scroll.viewport().installEventFilter(self)
        # 滚动条常驻: 出现/消失会让 viewport 宽度抖动, 高度跟着反复重算
        self.ui.diff_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.ui.record_list.setItemDelegate(_RecordDelegate(self.ui.record_list))
        self.ui.record_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.record_list.setToolTip(
            self.tr("勾选要对比的训练记录(最多 {} 条), 双击查看单次指标")
            .format(MAX_SERIES))
        self.ui.record_list.itemChanged.connect(self._on_item_changed)
        self.ui.record_list.itemDoubleClicked.connect(self._open_single)

        self.ui.summary_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.summary_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.summary_table.setMinimumHeight(150)
        header = self.ui.summary_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        self.ui.summary_table.verticalHeader().setVisible(False)

        self.ui.export_report_btn.clicked.connect(self._export_report)
        self.ui.delete_selected_btn.clicked.connect(self._delete_selected)

        # 三栏: 左右固定, 中间吃剩余空间
        self.ui.main_splitter.setStretchFactor(0, 0)
        self.ui.main_splitter.setStretchFactor(1, 1)
        self.ui.main_splitter.setStretchFactor(2, 0)
        self.ui.main_splitter.setSizes([280, 700, 320])

        self._populate_list()
        self._preselect(current)
        self._refresh()

    def showEvent(self, event):
        super().showEvent(event)
        # 窗口默认 1320 宽, 但防被内容(如指标 tab)撑出屏幕外
        scr = self.screen() or QApplication.primaryScreen()
        if scr is not None:
            avail = scr.availableGeometry()
            self.resize(min(self.width(), avail.width() - 16),
                        min(self.height(), avail.height() - 16))

    # ---------- 数据 ----------
    @staticmethod
    def _legend_html():
        dots = [("已完成", status_color("已完成")),
                ("训练中", status_color("训练中")),
                ("失败", status_color("失败")),
                ("已停止", status_color("已停止"))]
        parts = ["状态色标："]
        for name, color in dots:
            parts.append("<span style='color:{}'>●</span> {}".format(color, name))
        return "&nbsp;&nbsp;".join(parts)

    def _metric_keys(self, picked=None):
        """候选指标取全部记录(切换勾选时 tab 不跳动), 可用指标只算勾选的."""
        idxs = range(len(self._records)) if picked is None else picked
        keys = set()
        for i in idxs:
            for k, v in self._series[i].items():
                if k == "epochs" or not isinstance(v, list):
                    continue
                if any(isinstance(x, (int, float)) for x in v):
                    keys.add(k)
        return ([k for k in METRIC_ORDER if k in keys]
                + sorted(k for k in keys if k not in METRIC_ORDER))

    def _fill_range_combo(self):
        self._guard = True
        self.ui.record_range_combo.clear()
        for text, key in RANGE_ITEMS:
            self.ui.record_range_combo.addItem(text)
            self.ui.record_range_combo.setItemData(
                self.ui.record_range_combo.count() - 1, key)
        self._guard = False

    def _apply_range(self):
        """按当前范围筛出可见记录(原索引); 时间取 start_time 前 10 位日期比较."""
        key = self.ui.record_range_combo.currentData() or "all"
        if key == "all":
            self._visible = list(range(len(self._records)))
            return
        today = _dt.date.today()
        if key == "today":
            lo = today.isoformat()
        elif key == "yesterday":
            lo = (today - _dt.timedelta(days=1)).isoformat()
        elif key == "7d":
            lo = (today - _dt.timedelta(days=6)).isoformat()
        elif key == "30d":
            lo = (today - _dt.timedelta(days=29)).isoformat()
        else:
            lo = ""
        self._visible = []
        for i, rec in enumerate(self._records):
            day = str(rec.get("start_time") or "")[:10]
            if day and day >= lo:
                self._visible.append(i)

    def _best_of(self, idx, key):
        """该记录在指定指标上的最优值; 取不到指标列就按 ema 优先回退."""
        _, vals = self._series_of(idx, key)
        vals = [v for v in (vals or []) if isinstance(v, (int, float))]
        if not vals:
            return None
        return max(vals) if _direction(key) >= 0 else min(vals)

    def _best_text(self, idx):
        """卡片主指标: 训练中/失败/停止显示状态, 完成显示'短名 数值'."""
        rec = self._records[idx]
        st = str(rec.get("status") or "")
        if st == "训练中":
            done = len(self._series[idx].get("epochs") or [])
            total = rec.get("epochs") or ""
            return ("进行中 {}/{}".format(done, total) if total
                    else "进行中"), False
        if st in _STATUS_LABEL:
            return _STATUS_LABEL[st], True
        p = primary_for(rec.get("task") or "")
        if p is None:
            return "", False
        v = self._best_of(idx, p.base)
        if v is None:
            return "", False
        text = "{} {:.{}f}".format(_PRIMARY_SHORT.get(p.label, p.label),
                                   v, p.decimals)
        return text, False

    def _populate_list(self):
        """按当前可见集合重建列表; 保留仍在范围内的勾选."""
        keep = set(self._checked())
        self.ui.record_list.clear()
        for i in self._visible:
            item = QListWidgetItem()
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if i in keep else Qt.Unchecked)
            item.setData(ROLE_IDX, i)
            rec = self._records[i]
            item.setData(ROLE_STATUS, str(rec.get("status") or ""))
            item.setData(ROLE_TIME, _time_short(rec.get("start_time")))
            item.setData(ROLE_TASK, task_text(rec.get("task") or ""))
            item.setData(ROLE_TAG, str(rec.get("task") or ""))
            item.setData(ROLE_MODEL, str(rec.get("model_size") or ""))
            best, bad = self._best_text(i)
            item.setData(ROLE_BEST, best)
            item.setData(ROLE_BAD, bad)
            self.ui.record_list.addItem(item)

    def _preselect(self, current):
        want = set()
        if current is not None:
            for i in self._visible:
                if _same_record(current, self._records[i]):
                    want.add(i)
                    break
        for i in self._visible:
            if len(want) >= 3:
                break
            want.add(i)
        self._guard = True
        for i in range(self.ui.record_list.count()):
            item = self.ui.record_list.item(i)
            if item.data(ROLE_IDX) in want:
                item.setCheckState(Qt.Checked)
        self._guard = False

    def _checked(self):
        out = []
        for i in range(self.ui.record_list.count()):
            item = self.ui.record_list.item(i)
            if item.checkState() == Qt.Checked:
                out.append(item.data(ROLE_IDX))
        return out

    def _series_of(self, idx, key):
        """该记录在指定指标上的取样: 先按选中的列名取, 取不到再退回 ema 优先的列."""
        s = self._series[idx]
        vals = s.get(key)
        if vals is None:
            alt = metric_key(s, key)
            vals = s.get(alt) if alt else None
        return s, vals

    def _pairs(self, idx, key):
        """该记录的 (epoch, 值) 有效点; 没有 epoch 列就按序号补."""
        s, vals = self._series_of(idx, key)
        epochs = s.get("epochs") or []
        if not epochs or not vals:
            return []
        out = [(e, v) for e, v in zip(epochs, vals)
               if isinstance(v, (int, float))]
        return out

    # ---------- 交互 ----------
    def _on_item_changed(self, item):
        if self._guard:
            return
        if (item.checkState() == Qt.Checked
                and len(self._checked()) > MAX_SERIES):
            self._guard = True
            item.setCheckState(Qt.Unchecked)
            self._guard = False
            self.ui.hint_label.setText(
                self.tr("一次最多对比 {} 条记录").format(MAX_SERIES))
            return
        self._refresh()

    def _on_metric_changed(self, key):
        self._metric = key
        self._refresh()

    def _on_range_changed(self, _index):
        if self._guard:
            return
        self._apply_range()
        self._populate_list()
        self._refresh()

    def _open_single(self, item):
        MetricsDialog(self._records[item.data(ROLE_IDX)], self.db, self).exec()

    # ---------- 渲染 ----------
    def _refresh(self):
        picked = self._checked()
        all_keys = self._metric_keys()
        usable = set(self._metric_keys(picked))
        self._tabs.set_metrics(all_keys, usable, self._metric)
        metric = self._tabs.current()
        self._metric = metric

        self.ui.chart_title_label.setText(
            self.tr("{} 训练曲线（按 epoch）").format(metric) if metric else "")
        self._fill_table(picked, metric)
        self._draw_chart(picked, metric)
        self._render_diff(picked, metric)

        n = len(picked)
        self.ui.selected_count_label.setText(
            self.tr("已选 {} 条（上限 {}）").format(n, MAX_SERIES))
        self.ui.hint_label.setText(
            self.tr("已选 {} 条(上限 {}), 双击左侧记录可查看单次指标")
            .format(n, MAX_SERIES) if n else
            self.tr("勾选左侧的训练记录后这里显示对比曲线"))

    def _draw_chart(self, picked, key):
        items = []
        legend = []
        for n, idx in enumerate(picked[:MAX_SERIES]):
            pairs = self._pairs(idx, key) if key else []
            if not pairs:
                continue
            rec = self._records[idx]
            color = series_color(n)
            items.append(("{} · {} · {}".format(
                _time_short(rec.get("start_time")),
                task_text(rec.get("task") or ""),
                str(rec.get("model_size") or "")),
                color, [p[0] for p in pairs], [p[1] for p in pairs]))
            aug = _aug_label(rec.get("aug"))
            legend.append("<span style='color:{}'>●</span> {} · {} · {}{}"
                          .format(color,
                                  _esc(_time_short(rec.get("start_time"))),
                                  _esc(task_text(rec.get("task") or "")),
                                  _esc(rec.get("model_size") or ""),
                                  "" if not aug else " · " + _esc(aug)))
        self.ui.legend_label.setText("&nbsp;&nbsp;".join(legend))
        if not picked:
            self._chart.set_empty(
                self.tr("勾选左侧的训练记录后这里显示对比曲线"))
            return
        if not items:
            self._chart.set_empty(
                self.tr("所选记录没有\"{}\"的数据").format(key))
            return
        self._chart.set_series(items, key, _direction(key) < 0,
                               lambda v: _fmt(v, key))

    def _row_cells(self, idx):
        rec = self._records[idx]
        return [
            _time_short(rec.get("start_time")),
            "{} / {}".format(task_text(rec.get("task") or ""),
                             str(rec.get("model_size") or "")),
            str(rec.get("dataset_info") or rec.get("dataset") or ""),
            str(rec.get("epochs") or ""),
            str(rec.get("batch_size") or ""),
            str(rec.get("lr") or ""),
            _fmt(self._best_of(idx, "mAP@50"), "mAP@50"),
            _fmt(self._best_of(idx, "precision"), "precision"),
            _fmt(self._best_of(idx, "recall"), "recall"),
            _fmt(self._best_of(idx, "F1@0.5"), "F1@0.5"),
            _fmt_dur(rec.get("duration_secs")) or "—",
            ", ".join(_aug_codes(rec.get("aug"))) or "—",
        ]

    def _fill_table(self, picked, metric):
        # 高亮列: mAP@50 与 F1@0.5, 与设计稿表格一致
        hl_cols = {6, 9}
        cur_col = _CUR_COLUMN.get(metric)
        labels = [c + " ●" if i == cur_col else c
                  for i, c in enumerate(_COLUMNS)]
        self.ui.summary_table.setColumnCount(len(_COLUMNS))
        self.ui.summary_table.setHorizontalHeaderLabels(labels)
        if cur_col is not None:
            self.ui.summary_table.horizontalHeaderItem(cur_col).setForeground(
                QColor(theme.hexof("accent_soft")))
        rows = picked[:MAX_SERIES]
        self.ui.summary_table.setRowCount(len(rows))
        cur_bg = QColor(theme.hexof("accent_dim"))
        for r, idx in enumerate(rows):
            for c, text in enumerate(self._row_cells(idx)):
                item = QTableWidgetItem(text)
                if c == cur_col:
                    item.setBackground(cur_bg)
                if c in hl_cols and text and text != "—":
                    item.setForeground(QColor("#3ddc84"))
                    f = item.font()
                    f.setBold(True)
                    item.setFont(f)
                self.ui.summary_table.setItem(r, c, item)

    def _diff_items(self, picked, metric):
        items = []
        for n, idx in enumerate(picked[:MAX_SERIES]):
            rec = self._records[idx]
            best = self._best_of(idx, metric) if metric else None
            items.append({
                "color": series_color(n),
                "time": _time_short(rec.get("start_time")),
                "task": task_text(rec.get("task") or ""),
                "model": str(rec.get("model_size") or ""),
                "dataset": str(rec.get("dataset_info") or rec.get("dataset") or ""),
                "epochs": str(rec.get("epochs") or ""),
                "batch": str(rec.get("batch_size") or ""),
                "lr": str(rec.get("lr") or ""),
                "img_size": str(rec.get("img_size") or ""),
                "aug": _aug_label(rec.get("aug")) or self.tr("无"),
                "aug_codes": _aug_codes(rec.get("aug")),
                "status": str(rec.get("status") or ""),
                "prog": len(self._series[idx].get("epochs") or []),
                "dur": _fmt_dur(rec.get("duration_secs")),
                "best": best,
                "best_text": _fmt(best, metric) if best is not None else "—",
            })
        return items

    def _render_diff(self, picked, metric):
        if len(picked) < 2:
            self._diff.show_empty(
                self.tr("至少勾选 2 条记录<br>才能比较差异"))
            return
        items = self._diff_items(picked, metric)
        # 最佳只在有该指标数据的记录里比, 方向跟着指标走
        scored = [(i, it) for i, it in enumerate(items)
                  if it.get("best") is not None]
        if scored:
            d = _direction(metric)
            best_idx = max(scored, key=lambda t: t[1]["best"] * d)[0]
        else:
            best_idx = None
        self._diff.render(items, metric, best_idx)
        # 内容高度变了 viewport 不一定 resize, 主动补; 再排一次延迟兜底,
        # 布局激活后宽度若有微调, 高度按最终宽度再算一遍
        self._fit_diff_height()
        QTimer.singleShot(0, self._fit_diff_height)

    def eventFilter(self, obj, event):
        if obj is self.ui.diff_scroll.viewport() \
                and event.type() == QEvent.Resize:
            QTimer.singleShot(0, self._fit_diff_height)
        return super().eventFilter(obj, event)

    def _fit_diff_height(self):
        h = self.ui.diff_content.heightForWidth(self.ui.diff_content.width())
        if h > 0:
            self.ui.diff_content.setMinimumHeight(h)

    # ---------- 工具栏动作 ----------
    def _export_report(self):
        """当前图存 PNG, 汇总表存同名 CSV(同目录)."""
        picked = self._checked()
        if not picked or not self._chart.has_series():
            QMessageBox.information(self, self.tr("导出对比报告"),
                                    self.tr("当前没有可导出的对比图表"))
            return
        path, _ = QFileDialog.getSaveFileName(
            self, self.tr("导出对比报告"), "compare_report.png",
            self.tr("PNG 图片 (*.png)"))
        if not path:
            return
        try:
            if not self._chart.grab().save(path):
                raise OSError("save failed")
            csv_path = os.path.splitext(path)[0] + ".csv"
            # utf-8-sig: Excel 直接打开中文表头不乱码
            with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(list(_COLUMNS))
                for idx in picked[:MAX_SERIES]:
                    w.writerow(self._row_cells(idx))
            self.ui.hint_label.setText(
                self.tr("已导出: {}\n{}").format(path, csv_path))
        except Exception as e:
            QMessageBox.warning(self, self.tr("导出对比报告"),
                                self.tr("导出失败: {}").format(e))

    def _delete_selected(self):
        """删除勾选的训练记录(db 会级联清理指标文件), 之后重建列表."""
        picked = self._checked()
        if not picked:
            QMessageBox.information(self, self.tr("删除选中"),
                                    self.tr("请先勾选要删除的训练记录"))
            return
        if not QMessageBox.question(
                self, self.tr("删除选中"),
                self.tr("确定删除选中的 {} 条训练记录? 对应指标文件会一并删除.")
                .format(len(picked))):
            return
        ids = {self._records[i].get("id") for i in picked}
        for rid in ids:
            self.db.delete_train_record(rid)
        self._records = [r for r in self._records if r.get("id") not in ids]
        self._series = [load_run_series(r, self._db_path)
                        for r in self._records]
        self._apply_range()
        self._populate_list()
        self._refresh()
