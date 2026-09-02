# -*- coding: utf-8 -*-
"""训练指标折线图对话框：从训练记录的 metrics 字段绘制。"""

import re

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import Qt, QEvent, QObject, QTimer
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QComboBox)


def _muted_style(size=13):
    """辅助说明文字: 中性灰 + 指定字号。"""
    return "color: #8b93a5; font-size: {}px;".format(size)


def _setup_matplotlib_chinese():
    """设置中文字体（与 app.easy_trainer 同逻辑，避免循环导入）。"""
    try:
        available = {f.name for f in font_manager.fontManager.ttflist}
    except Exception:
        available = set()
    candidates = ["Microsoft YaHei UI", "Microsoft YaHei", "SimHei",
                  "SimSun", "PingFang SC", "Noto Sans CJK SC", "Noto Sans SC"]
    chosen = next((f for f in candidates if f in available), None)
    if chosen is None:
        for f in font_manager.fontManager.ttflist:
            n = f.name.lower()
            if any(kw in n for kw in ("cjk", "chinese", "yahei", "simhei",
                                      "pingfang", "heiti", "songti", "han")):
                chosen = f.name
                break
    plt.rcParams["font.sans-serif"] = [chosen or "DejaVu Sans", "DejaVu Sans"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False


class _ClickToPopupFilter(QObject):
    """点击下拉框任意位置展开(与训练界面行为一致)。"""

    def __init__(self, combo, parent=None):
        super().__init__(parent)
        self._combo = combo

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.MouseButtonPress
                and event.button() == Qt.LeftButton):
            QTimer.singleShot(0, self._combo.showPopup)
            return True
        return False


class MetricsDialog(QDialog):
    """
    展示一次训练的指标曲线。
    metrics 结构: {"epochs": [...], "series": {名称: [...]},
                   "per_class": {标签名: {AP50-95/AR/F1/Precision/Recall: [...]}}}
    下拉默认"全部指标"(overall series),选标签后显示该标签的 per-class 曲线。
    """

    def __init__(self, record, parent=None):
        super().__init__(parent)
        # 关闭即销毁: 临时对象 .exec() 无引用持有, 不加此属性会导致
        # C++ 对象(含 Figure)随 parent 常驻泄漏
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("训练指标")
        # 支持最小化/最大化(默认 dialog 只有关闭按钮)
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint)
        self.resize(760, 520)
        self._record = record
        metrics = record.get("metrics") or {}
        self._epochs = metrics.get("epochs") or []
        self._series = metrics.get("series") or {}
        self._per_class = metrics.get("per_class") or {}
        self._labels = list(record.get("labels") or [])
        for lb in self._per_class:
            if lb not in self._labels:
                self._labels.append(str(lb))
        # 数字自然排序(1,2,10 而非 1,10,2)
        self._labels.sort(key=lambda s: [
            int(x) if x.isdigit() else x
            for x in re.split(r"(\d+)", str(s))])
        self._body = QVBoxLayout(self)
        self._body.setContentsMargins(12, 12, 12, 12)
        self._combo_filters = []
        self._build_toolbar()
        self._chart = None
        self._rebuild_chart()

    def _build_toolbar(self):
        row = QHBoxLayout()
        row.addStretch(1)
        lbl = QLabel("标签筛选")
        lbl.setStyleSheet(_muted_style())
        row.addWidget(lbl)
        self._combo = QComboBox()
        self._combo.addItem("全部指标")
        cls_mode = "accuracy" in self._series
        if not cls_mode:
            self._combo.addItem("全部标签-P")
            self._combo.addItem("全部标签-R")
        for name in self._labels:
            self._combo.addItem(str(name))
        self._style_combo(self._combo)
        self._combo.currentTextChanged.connect(lambda _: self._rebuild_chart())
        row.addWidget(self._combo)
        # 无 per_class
        if not self._per_class and not self._labels:
            self._hint = QLabel("(暂无标签数据,需完成首次 epoch 验证后才会出现)")
            self._hint.setStyleSheet(_muted_style(12))
            row.addWidget(self._hint)
        self._body.addLayout(row)

    def _style_combo(self, combo):
        """与训练界面下拉一致：文本居中 + 点击任意位置展开下拉。"""
        combo.setEditable(True)
        combo.setFocusPolicy(Qt.StrongFocus)
        le = combo.lineEdit()
        le.setObjectName("multiComboLineEdit")
        le.setReadOnly(True)
        le.setAlignment(Qt.AlignHCenter)
        # parent=self: dialog 设了 WA_DeleteOnClose, 过滤器必须随之销毁,
        # 否则延时弹出的 singleShot 会打到已删除的 combo 上。
        f = _ClickToPopupFilter(combo, self)
        combo.installEventFilter(f)
        combo.lineEdit().installEventFilter(f)
        self._combo_filters.append(f)   # 保引用
        return combo

    def _rebuild_chart(self):
        if self._chart is not None:
            self._body.removeWidget(self._chart)
            self._chart.deleteLater()
            self._chart = None
        sel = self._combo.currentText()
        if sel == "全部指标":
            epochs, series = self._epochs, self._series
        elif sel == "全部标签-P":
            epochs = self._epochs
            series = {lb: pc.get("Precision", []) for lb, pc in self._per_class.items()}
        elif sel == "全部标签-R":
            epochs = self._epochs
            series = {lb: pc.get("Recall", []) for lb, pc in self._per_class.items()}
        else:
            pc = self._per_class.get(sel) or {}
            epochs, series = self._epochs, pc
        series = {k: v for k, v in series.items()
                  if isinstance(v, list) and v}
        if not epochs or not series:
            tip = QLabel("暂无该标签的指标数据（训练完成后可查看）")
            tip.setStyleSheet(_muted_style())
            tip.setAlignment(Qt.AlignCenter)
            self._chart = tip
            self._body.addWidget(tip)
            return
        self._chart = self._build_chart(epochs, series)
        self._body.addWidget(self._chart)

    def _build_chart(self, epochs, series):

        loss_items = {k: v for k, v in series.items() if "loss" in k.lower()}
        score_items = {k: v for k, v in series.items() if "loss" not in k.lower()}
        groups = [g for g in (loss_items, score_items) if g]
        _setup_matplotlib_chinese()
        fig = Figure(figsize=(8, 3.6 * len(groups)), dpi=100,
                     facecolor="#1c1e25")
        for idx, g in enumerate(groups):
            axes = fig.add_subplot(len(groups), 1, idx + 1,
                                   facecolor="#1c1e25")
            for name, values in g.items():
                n = min(len(epochs), len(values))
                # 缺值在 worker 侧补了 None 占位以保持与 epochs 对齐,
                # 绘图前必须过滤, 否则 min/max 与 format 会拿到 None 崩溃。
                pairs = [(e, v) for e, v in zip(epochs[:n], values[:n])
                         if v is not None]
                if not pairs:
                    continue
                xe, ve = zip(*pairs)
                if len(xe) == 1:
                    axes.plot(xe, ve, "o", markersize=10,
                              label=name)
                    axes.annotate("{:.4f}".format(ve[0]),
                                  xy=(xe[0], ve[0]),
                                  xytext=(8, 0), textcoords="offset points",
                                  color="#e8eaf0", fontsize=10,
                                  va="center")
                else:
                    # 点多时去掉逐点 marker(50类×300epoch=1.5万对象拖慢重绘), 仅画线
                    axes.plot(xe, ve, label=name, linewidth=1.5,
                              marker="o" if len(xe) <= 100 else None,
                              markersize=4)
            axes.set_xlabel("epoch", color="#c3c9d6")
            group_label = "loss 值" if g is loss_items else "指标值 (mAP/P/R)"
            axes.set_ylabel(group_label, color="#c3c9d6")
            axes.tick_params(axis="x", colors="#c3c9d6")
            axes.tick_params(axis="y", colors="#c3c9d6")
            for spine in axes.spines.values():
                spine.set_color("#3a3f4e")
            axes.grid(True, color="#2a2e38", linestyle="--", linewidth=0.5)
            axes.legend(loc="lower right", facecolor="#23262f", edgecolor="#3a3f4e",
                        labelcolor="#e8eaf0")
            if epochs:
                all_vals = [v for vs in g.values() for v in vs
                            if v is not None]
                if all_vals:
                    lo, hi = min(all_vals), max(all_vals)
                    pad = max((hi - lo) * 0.15, max(0.001, hi * 0.15))
                    axes.set_ylim(lo - pad, hi + pad)
            if epochs:
                # 刻度钉死全部 epoch 会在 300 点时建 300 个 Text 对象, 每次
                # 重绘全量重建; 限制最多 10 档均匀刻度, 交互读值以线为准。
                # 向上取整: 保证 step 均匀覆盖到最后一个 epoch, 否则
                # 双重截断(::step 后再 [:10])会让 x 轴右半段没有刻度。
                step = max(1, (len(epochs) + 9) // 10)
                axes.set_xticks(epochs[::step])
        fig.tight_layout()
        return FigureCanvasQTAgg(fig)
