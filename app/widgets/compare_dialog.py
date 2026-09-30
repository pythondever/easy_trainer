# -*- coding: utf-8 -*-
"""
多次训练结果对比: 同一指标的多条曲线叠在一张图上, 并列关键差异.
曲线来源与单次指标窗口同源(metrics_dialog.load_run_series), 所以这里不重复
解析 metrics.csv / metrics.json.
"""

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QDialog,
                               QHBoxLayout, QHeaderView, QLabel, QListWidget,
                               QListWidgetItem, QSizePolicy, QSpacerItem,
                               QSplitter, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)

from app.annotation.box_item import LABEL_COLORS
from app.core import theme
from app.core.metrics import metric_key
from app.core.utils import setup_matplotlib_chinese
from app.train.dialogs import AUG_ITEMS
from app.widgets.combo_utils import style_combo
from app.widgets.metrics_dialog import MetricsDialog, load_run_series
from app.widgets.status_style import task_text

# 一次最多叠几条: 再多颜色分不清, 图例也会盖住曲线
MAX_SERIES = 8
# 指标下拉的排序; 记录里实际存在的列才进下拉, 没列到的排最后
METRIC_ORDER = (
    "mAP@50", "mAP@50-95", "ema_mAP@50", "ema_mAP@50-95",
    "mask_mAP@50", "mask_mAP@50-95", "mask_ema_mAP@50", "mask_ema_mAP@50-95",
    "precision", "recall", "F1", "mAR",
    "accuracy", "auroc", "F1@0.5", "CER", "WER",
    "train_loss", "val_loss",
)
_COLUMNS = ("时间", "任务", "型号", "数据集", "轮次", "批次", "学习率")


def _muted(size=13):
    return "color: {}; font-size: {}px;".format(theme.hexof("text_3"), size)


def _direction(key):
    """越大越好还是越小越好; 错误率与 loss 越小越好."""
    if key in ("CER", "WER") or "loss" in key.lower():
        return -1
    return 1


def _best(series, key):
    vals = [v for v in (series.get(key) or []) if isinstance(v, (int, float))]
    if not vals:
        return None
    return max(vals) if _direction(key) >= 0 else min(vals)


def _fmt(v, key):
    if v is None:
        return ""
    return "{:.4f}".format(v) if key in ("CER", "WER", "accuracy") \
        else "{:.3f}".format(v)


_AUG_NAMES = {code: name for _g, code, name, _p in AUG_ITEMS}
# 图例太长会盖住曲线, 超过两项就只列前两项
AUG_LEGEND_MAX = 2


def _aug_label(value):
    """记录的增强值 → 图例短标签: 逗号串拆开列名字, 不增强给空串让图例只剩时间."""
    codes = [c.strip() for c in str(value or "").split(",")]
    names = [QC.translate("TrainDialog", _AUG_NAMES[c])
             for c in codes if c in _AUG_NAMES]
    if not names:
        return ""
    if len(names) > AUG_LEGEND_MAX:
        return "+".join(names[:AUG_LEGEND_MAX]) + "\u2026"
    return "+".join(names)


def _same_record(a, b):
    if a is None or b is None:
        return False
    aid, bid = a.get("id"), b.get("id")
    if aid and aid == bid:
        return True
    at, bt = a.get("start_time"), b.get("start_time")
    return bool(at) and at == bt


class CompareDialog(QDialog):
    """勾选若干条训练记录, 按同一指标叠图对比, 下方列出各自的超参与最好值."""

    def __init__(self, db, records, current=None, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr("对比多次训练"))
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint)
        self.resize(1060, 640)
        self.db = db
        self._db_path = getattr(db, "db_path", None)
        self._records = sorted(
            list(records), key=lambda r: str(r.get("start_time") or ""),
            reverse=True)
        self._series = [load_run_series(r, self._db_path) for r in self._records]
        self._combo_filters = []
        self._chart = None
        self._spacer = None
        self._guard = False
        self._build()
        self._fill_combo()
        self._preselect(current)
        self._refresh()

    # ---------- 装配 ----------
    def _build(self):
        body = QVBoxLayout(self)
        body.setContentsMargins(12, 12, 12, 12)
        body.setSpacing(8)

        row = QHBoxLayout()
        row.addStretch(1)
        cap = QLabel(self.tr("对比指标"))
        cap.setStyleSheet(_muted())
        row.addWidget(cap)
        self._combo = QComboBox()
        self._combo.setMinimumWidth(180)
        self._combo.currentTextChanged.connect(self._on_metric_changed)
        style_combo(self._combo, self._combo_filters, self)
        row.addWidget(self._combo)
        body.addLayout(row)

        self._split = QSplitter(Qt.Horizontal)
        self._list = self._build_list()
        self._split.addWidget(self._list)
        self._split.addWidget(self._build_right())
        self._split.setStretchFactor(0, 0)
        self._split.setStretchFactor(1, 1)
        self._split.setSizes([320, 740])
        body.addWidget(self._split, 1)

        self._hint = QLabel("")
        self._hint.setStyleSheet(_muted(12))
        body.addWidget(self._hint)

    def _build_list(self):
        lst = QListWidget()
        lst.setMinimumWidth(260)
        lst.setMaximumWidth(440)
        lst.setSelectionMode(QAbstractItemView.SingleSelection)
        lst.setToolTip(self.tr("勾选要对比的训练记录(最多 {} 条), 双击查看单次指标")
                       .format(MAX_SERIES))
        for i, rec in enumerate(self._records):
            item = QListWidgetItem(self._row_text(rec))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, i)
            lst.addItem(item)
        lst.itemChanged.connect(self._on_item_changed)
        lst.itemDoubleClicked.connect(self._open_single)
        return lst

    def _build_right(self):
        panel = QWidget()
        lay = QVBoxLayout(panel)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)
        self._right = lay
        self._table = QTableWidget(0, len(_COLUMNS) + 1, panel)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setMinimumHeight(150)
        header = self._table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        self._table.verticalHeader().setVisible(False)
        lay.addWidget(self._table, 0)
        return panel

    # ---------- 数据 ----------
    @staticmethod
    def _row_text(rec):
        t = str(rec.get("start_time") or "")
        best = rec.get("map50") or rec.get("accuracy") or ""
        bits = [t[5:] if len(t) > 5 else t,
                task_text(rec.get("task") or ""),
                str(rec.get("model_size") or "")]
        if best:
            bits.append("best={}".format(best))
        return "  ".join(b for b in bits if b)

    def _metric_keys(self):
        keys = set()
        for s in self._series:
            for k, v in s.items():
                if k == "epochs" or not isinstance(v, list):
                    continue
                if any(isinstance(x, (int, float)) for x in v):
                    keys.add(k)
        return ([k for k in METRIC_ORDER if k in keys]
                + sorted(k for k in keys if k not in METRIC_ORDER))

    def _fill_combo(self):
        keys = self._metric_keys()
        self._guard = True
        self._combo.clear()
        self._combo.addItems(keys)
        self._guard = False
        self._combo.setEnabled(bool(keys))
        self._combo.setToolTip(
            "" if keys else self.tr("这些记录都没有保存指标, 无法对比"))

    def _preselect(self, current):
        want = set()
        if current is not None:
            for i, rec in enumerate(self._records):
                if _same_record(current, rec):
                    want.add(i)
                    break
        for i in range(len(self._records)):
            if len(want) >= 3:
                break
            want.add(i)
        self._guard = True
        for i in range(self._list.count()):
            item = self._list.item(i)
            if item.data(Qt.UserRole) in want:
                item.setCheckState(Qt.Checked)
        self._guard = False

    def _checked(self):
        out = []
        for i in range(self._list.count()):
            item = self._list.item(i)
            if item.checkState() == Qt.Checked:
                out.append(item.data(Qt.UserRole))
        return out

    def _series_of(self, idx, key):
        """该记录在指定指标上的取样: 先按选中的列名取, 取不到再退回 ema 优先的列."""
        s = self._series[idx]
        vals = s.get(key)
        if vals is None:
            alt = metric_key(s, key)
            vals = s.get(alt) if alt else None
        return s, vals

    # ---------- 交互 ----------
    def _on_item_changed(self, item):
        if self._guard:
            return
        if (item.checkState() == Qt.Checked
                and len(self._checked()) > MAX_SERIES):
            self._guard = True
            item.setCheckState(Qt.Unchecked)
            self._guard = False
            self._hint.setText(self.tr("一次最多对比 {} 条记录").format(MAX_SERIES))
            return
        self._refresh()

    def _on_metric_changed(self, _text):
        if self._guard:
            return
        self._refresh()

    def _open_single(self, item):
        MetricsDialog(self._records[item.data(Qt.UserRole)], self.db, self).exec()

    # ---------- 渲染 ----------
    def _refresh(self):
        self._clear_chart()
        picked = self._checked()
        key = self._combo.currentText()
        self._fill_table(picked, key)
        self._draw_chart(picked, key)
        n = len(picked)
        self._hint.setText(
            self.tr("已选 {} 条(上限 {}), 双击左侧记录可查看单次指标")
            .format(n, MAX_SERIES) if n else
            self.tr("勾选左侧的训练记录后这里显示对比曲线"))

    def _clear_chart(self):
        if self._chart is not None:
            self._right.removeWidget(self._chart)
            self._chart.deleteLater()
            self._chart = None
        if self._spacer is not None:
            self._right.removeItem(self._spacer)
            self._spacer = None

    def _draw_chart(self, picked, key):
        if not picked or not key:
            self._chart = self._tip(self.tr("暂无可对比的指标数据"))
            self._right.insertWidget(0, self._chart)
            return
        setup_matplotlib_chinese()
        fig = Figure(figsize=(8.4, 4.2), dpi=100,
                     facecolor=theme.hexof("bg_panel"))
        axes = fig.add_subplot(111, facecolor=theme.hexof("bg_panel"))
        drawn = 0
        for n, idx in enumerate(picked[:MAX_SERIES]):
            s, vals = self._series_of(idx, key)
            epochs = s.get("epochs") or []
            if not epochs or not vals:
                continue
            pairs = [(e, v) for e, v in zip(epochs, vals)
                     if isinstance(v, (int, float))]
            if not pairs:
                continue
            xe, ve = zip(*pairs)
            axes.plot(xe, ve, color=LABEL_COLORS[n % len(LABEL_COLORS)],
                      label=self._legend(self._records[idx]), linewidth=1.5,
                      marker="o" if len(xe) <= 100 else None, markersize=4)
            drawn += 1
        if not drawn:
            self._chart = self._tip(self.tr("所选记录没有\"{}\"的数据")
                                    .format(key))
            self._right.insertWidget(0, self._chart)
            return
        axes.set_xlabel("epoch", color=theme.hexof("text_2"))
        axes.set_ylabel(key, color=theme.hexof("text_2"))
        axes.tick_params(axis="x", colors=theme.hexof("text_2"))
        axes.tick_params(axis="y", colors=theme.hexof("text_2"))
        for spine in axes.spines.values():
            spine.set_color(theme.hexof("border_strong"))
        axes.grid(True, color=theme.hexof("bg_control_2"), linestyle="--",
                  linewidth=0.5)
        axes.legend(loc="best", fontsize=8, facecolor=theme.hexof("bg_control"),
                    edgecolor=theme.hexof("border_strong"),
                    labelcolor=theme.hexof("text"))
        fig.tight_layout()
        self._chart = FigureCanvasQTAgg(fig)
        self._chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._right.insertWidget(0, self._chart)

    @staticmethod
    def _legend(rec):
        t = str(rec.get("start_time") or "")
        bits = [t[5:] if len(t) > 5 else t, _aug_label(rec.get("aug"))]
        return " · ".join(b for b in bits if b)

    def _tip(self, text):
        tip = QLabel(text)
        tip.setStyleSheet(_muted())
        tip.setAlignment(Qt.AlignCenter)
        tip.setMinimumHeight(220)
        # 空态下没给 stretch, QBoxLayout 会把多余竖向空间摊进条目间隙
        self._spacer = QSpacerItem(1, 1, QSizePolicy.Minimum,
                                   QSizePolicy.Expanding)
        self._right.addSpacerItem(self._spacer)
        return tip

    def _fill_table(self, picked, key):
        heads = list(_COLUMNS) + [key or "-"]
        self._table.setColumnCount(len(heads))
        self._table.setHorizontalHeaderLabels(heads)
        rows = picked[:MAX_SERIES]
        self._table.setRowCount(len(rows))
        for r, idx in enumerate(rows):
            rec = self._records[idx]
            s = self._series[idx]
            t = str(rec.get("start_time") or "")
            cells = [
                t[5:] if len(t) > 5 else t,
                task_text(rec.get("task") or ""),
                str(rec.get("model_size") or ""),
                str(rec.get("dataset_info") or rec.get("dataset") or ""),
                str(rec.get("epochs") or ""),
                str(rec.get("batch_size") or ""),
                str(rec.get("lr") or ""),
                _fmt(_best(s, key), key) if key else "",
            ]
            for c, text in enumerate(cells):
                self._table.setItem(r, c, QTableWidgetItem(text))
