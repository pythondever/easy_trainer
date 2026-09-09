# -*- coding: utf-8 -*-
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from math import ceil

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPixmap, QPen
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QPushButton, QLabel,
                               QFileDialog, QAbstractItemView, QHeaderView,
                               QSizePolicy, QHBoxLayout, QVBoxLayout, QWidget, QProgressBar)

import traceback

from PySide6.QtCore import QTimer

from app.core.db import load_train_metrics
from app.core.log import write_log
from app.widgets.message_box import MessageBox, ProgressDialog
from app.widgets.metrics_dialog import MetricsDialog
from app.widgets.test_dialog import TestDialog
from app.train.dialogs import TrainDialog
from app.train.test_worker import TestWorker
from app.train.export_worker import OnnxExportWorker, examples_dir
from ui.model import Ui_ModelDialog

TASK_TEXT = {"detect": "检测", "segment": "分割", "classify": "分类"}
COL_TASK, COL_DATA, COL_METRIC, COL_TIME, COL_DUR, COL_IMG, COL_OPS = range(7)
METRIC_GOOD, METRIC_MID, METRIC_BAD = "#7be39a", "#ffd166", "#ff6b6b"

# 操作列按钮配色: 测试/导出绿, 删除红。行内样式会盖掉全局, 故 disabled 态要自己补
_OPS_BTN = "QPushButton{font-size:12px;padding:2px 4px;background-color:%s;" \
           "border:1px solid %s;color:%s;}" \
           "QPushButton:hover{background-color:%s;border-color:%s;}" \
           "QPushButton:pressed{background-color:%s;}" \
           "QPushButton:disabled{background-color:#1c1e25;border-color:#2a2d37;" \
           "color:#5c6270;}"
OPS_BTN_QSS = {
    "opsGo": _OPS_BTN % ("#2b6b4a", "#3d8c62", "#d6f5e4",
                         "#357f58", "#4ba376", "#245c40"),
    "opsDel": _OPS_BTN % ("#7a3336", "#a3454b", "#ffd9d9",
                          "#8f3d41", "#bd5359", "#6a2c2f"),
}
CURVE_BG, CURVE_LINE = QColor("#181a20"), QColor("#4f7dff")


def _metric_value(rec):
    """精度统一取成 float: 检测/分割用 map50, 分类用 accuracy。"""
    for key in ("map50", "accuracy"):
        v = rec.get(key)
        if v in (None, ""):
            continue
        try:
            return float(v)
        except (TypeError, ValueError):
            continue
    return None


def _status(rec):
    st = str(rec.get("status") or "").strip()
    if not st:
        return "训练中" if not rec.get("model_path") else "已完成"
    if st in ("失败", "已停止", "失败/已停止"):
        return st      # "失败/已停止" 是旧记录, 区分不出停止还是报错
    if "失败" in st or "停止" in st:
        return "失败/已停止"
    if "训练" in st or "运行" in st:
        return "训练中"
    return "已完成"


STATUS_COLOR = {
    "失败": "#ff6b6b",
    "已停止": "#ffd166",
    "失败/已停止": "#ff9f6b",   # 旧记录: 无法判定
    "训练中": "#6bb8ff",
}


# 训练 metrics.csv 列名 -> 指标文件 series 键名, 与 train_worker._write_row 保持一致
_CSV_KEYS = (
    ("mAP@50-95", "val/mAP_50_95"), ("mAP@50", "val/mAP_50"),
    ("precision", "val/precision"), ("recall", "val/recall"),
    ("F1", "val/F1"), ("mAR", "val/mAR"),
    ("ema_mAP@50", "val/ema_mAP_50"), ("ema_mAP@50-95", "val/ema_mAP_50_95"),
    ("mask_mAP@50", "val/segm_mAP_50"), ("mask_mAP@50-95", "val/segm_mAP_50_95"),
    ("mask_ema_mAP@50", "val/ema_segm_mAP_50"),
    ("mask_ema_mAP@50-95", "val/ema_segm_mAP_50_95"),
    ("train_loss", "train/loss"), ("val_loss", "val/loss"),
)


def _series_from_csv(csv_path):
    """全量解析训练的 metrics.csv; 同一 epoch 多行时后写的值覆盖先写的。"""
    try:
        with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
            rows = list(csv.DictReader(f))
    except OSError:
        return {}
    by_epoch = {}
    for r in rows:
        try:
            ep = int(float(r.get("epoch", 0)))
        except (TypeError, ValueError):
            continue
        merged = by_epoch.setdefault(ep, {})
        for k, v in r.items():
            if v not in (None, ""):
                merged[k] = v
    series = {"epochs": sorted(by_epoch)}
    for key, csv_key in _CSV_KEYS:
        vals = []
        for ep in series["epochs"]:
            try:
                vals.append(float(by_epoch[ep].get(csv_key)))
            except (TypeError, ValueError):
                vals.append(None)
        if any(v is not None for v in vals):
            series[key] = vals
    return series


def _load_series(rec, db_path):
    """显示用曲线数据: 优先训练目录的 metrics.csv(rf-detr 真源);
    指标 json 只是训练中的节流快照, 可能缺列或缺尾轮。分类无 csv, 走 json。"""
    model_path = rec.get("model_path") or ""
    csv_path = os.path.join(os.path.dirname(model_path), "metrics.csv") if model_path else ""
    if csv_path and os.path.isfile(csv_path):
        s = _series_from_csv(csv_path)
        if s.get("epochs"):
            return s
    try:
        return (load_train_metrics(rec, db_path) or {}).get("series") or {}
    except Exception:
        return {}


def _curve_series(series):
    """曲线数据与精度列同源: 优先 ema 列(交付模型按 ema 选 best checkpoint)。"""
    if "accuracy" in series:
        key = "accuracy"
    else:
        is_seg = bool(series.get("mask_mAP@50") or series.get("mask_ema_mAP@50"))
        key = next((k for k in (("mask_ema_mAP@50", "mask_mAP@50") if is_seg
                                else ("ema_mAP@50", "mAP@50"))
                    if series.get(k)), "")
    ys = [v for v in (series.get(key) or []) if isinstance(v, (int, float))]
    return key, ys


def _duration_seconds(text):
    def pick(pattern):
        m = re.search(pattern, str(text or ""))
        return int(m.group(1)) if m else 0

    return (pick(r"(\d+)\s*(?:小时|h)") * 3600
            + pick(r"(\d+)\s*(?:分|min)") * 60
            + pick(r"(\d+)\s*(?:秒|s)"))


def _esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


class ModelDialog(QDialog):
    """模型管理：筛选 + 排序的分页表格，选中行在右侧显示详情与精度曲线。"""

    def __init__(self, app, project="", dataset="", parent=None):
        super().__init__(parent)
        self.ui = Ui_ModelDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("模型管理")
        self.setWindowState(Qt.WindowMaximized)
        self.app = app
        self._project = project
        self._dataset = dataset
        self._all_records = []
        self._records = []
        self._page_recs = []
        self._page = 0
        self._page_size = 15
        self._sort_col = COL_TIME
        self._sort_desc = True
        self._current = None
        self._exp = None          # 导出任务上下文
        self._exp_dlg = None
        self._onnx_worker = None
        self._eval_worker = None
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(150)
        self._resize_timer.timeout.connect(self._render_page)
        # 注册到 app:测试倒计时结束后由 TestDialog 关闭本窗口回首页
        self.app._model_dialog = self
        self._setup_table()
        self._setup_filters()
        self.ui.pre_page_btn.clicked.connect(self._prev_page)
        self.ui.next_page_btn.clicked.connect(self._next_page)
        self._load_records()

    def showEvent(self, event):
        super().showEvent(event)
        self._calc_page_size()
        self._render_page()
        # 首次渲染时详情面板还没布局完, 曲线宽度拿不到, 这里按实际宽度补画一次
        if self._current is not None:
            self._draw_curve(self._current)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        old = self._page_size
        self._calc_page_size()
        if self._page_size != old:
            self._resize_timer.start()

    def done(self, result):
        """关闭前清理 cellWidget：避免 PySide6 对话框 GC 时按钮 lambda 循环引用导致 0xC0000005。"""
        try:
            t = self.ui.tableWidget
            for r in range(t.rowCount()):
                for c in range(t.columnCount()):
                    w = t.cellWidget(r, c)
                    if w is not None:
                        t.removeCellWidget(r, c)
                        w.deleteLater()
        except Exception:
            pass
        super().done(result)

    # ---------- 表格与筛选控件 ----------

    def _setup_table(self):
        t = self.ui.tableWidget
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.setSelectionBehavior(QAbstractItemView.SelectRows)
        t.setSelectionMode(QAbstractItemView.SingleSelection)
        t.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h = t.horizontalHeader()
        widths = {
            COL_TASK: (QHeaderView.ResizeToContents, 60),
            COL_DATA: (QHeaderView.Stretch, 0),
            COL_METRIC: (QHeaderView.Fixed, 110),
            COL_TIME: (QHeaderView.ResizeToContents, 130),
            COL_DUR: (QHeaderView.ResizeToContents, 90),
            COL_IMG: (QHeaderView.ResizeToContents, 80),
            COL_OPS: (QHeaderView.Fixed, 150),
        }
        for i, (mode, w) in widths.items():
            h.setSectionResizeMode(i, mode)
            if w:
                t.setColumnWidth(i, w)
        h.setMinimumSectionSize(60)
        h.setStretchLastSection(False)
        h.setSortIndicatorShown(True)
        h.setSortIndicator(self._sort_col, Qt.DescendingOrder)
        h.sectionClicked.connect(self._on_header_clicked)
        t.verticalHeader().setDefaultSectionSize(46)
        t.verticalHeader().setMinimumSectionSize(40)
        t.itemSelectionChanged.connect(self._on_selection_changed)

    def _setup_filters(self):
        u = self.ui
        u.search_edit.textChanged.connect(self._apply_filters)
        u.task_combo.currentTextChanged.connect(self._apply_filters)
        u.status_combo.currentTextChanged.connect(self._apply_filters)
        u.best_only_check.stateChanged.connect(self._apply_filters)
        u.detail_metrics_btn.clicked.connect(
            lambda: self._current and self._show_metrics(self._current))
        u.detail_test_btn.clicked.connect(
            lambda: self._current and self._test(self._current))
        u.detail_retrain_btn.clicked.connect(
            lambda: self._current and self._retrain(self._current))
        u.detail_open_dir_btn.clicked.connect(self._open_model_dir)
        self._show_detail(None)

    def _on_header_clicked(self, col):
        if col == COL_OPS:
            return
        if col == self._sort_col:
            self._sort_desc = not self._sort_desc
        else:
            self._sort_col = col
            self._sort_desc = True
        self.ui.tableWidget.horizontalHeader().setSortIndicator(
            col, Qt.DescendingOrder if self._sort_desc else Qt.AscendingOrder)
        self._apply_filters()

    def _calc_page_size(self):
        """每页行数 = 视口能容纳的行数，尽量铺满窗口。"""
        t = self.ui.tableWidget
        row_h = t.verticalHeader().defaultSectionSize()
        if row_h <= 0:
            row_h = 40
        self._page_size = max(10, t.viewport().height() // row_h)

    # ---------- 数据 ----------

    def _load_records(self):
        """
        合并显示:已完成的优先从 model_history 取(完整字段),
        未完成/训练中/无模型输出的用 train_history 补充(实时更新 metrics)。
        """
        train_recs = self.app.db.get_train_records()
        model_recs = self.app.db.get_model_records()
        seen_train_ids = set()
        recs = []
        for m in model_recs:
            if not self._record_match(m):
                continue
            self._refresh_metric_from_file(m)
            recs.append(m)
            seen_train_ids.add(m.get("train_id"))
        for t in train_recs:
            if t.get("id") in seen_train_ids:
                continue
            self._refresh_metric_from_file(t)
            if not self._record_match(t):
                continue
            recs.append(t)
        self._all_records = recs
        self._apply_filters()

    # 库里的 map50/accuracy 可能是训练中途的快照(result.json 也不带 map50),
    # 显示一律以训练目录的 csv(或指标 json)全程最佳为准
    def _refresh_metric_from_file(self, rec):
        if not (rec.get("metrics_file") or rec.get("model_path")):
            return
        series = _load_series(rec, getattr(self.app.db, "db_path", None))
        key, ys = _curve_series(series)
        if ys:
            rec["map50" if key != "accuracy" else "accuracy"] = "{:.3f}".format(max(ys))

    def _record_match(self, r):
        if self._project and r.get("project") != self._project:
            return False
        if self._dataset:
            ds_list = [x.strip() for x in str(r.get("dataset", "")).split(",")]
            val_list = [x.strip() for x in str(r.get("val_dataset", "")).split(",")]
            if self._dataset not in ds_list and self._dataset not in val_list:
                return False
        return True

    def _apply_filters(self):
        kw = self.ui.search_edit.text().strip().lower()
        task = self.ui.task_combo.currentText()
        status = self.ui.status_combo.currentText()
        recs = []
        for r in self._all_records:
            if task != "全部任务" and TASK_TEXT.get(r.get("task", ""), "—") != task:
                continue
            if status != "全部状态":
                st = _status(r)
                # 旧记录的"失败/已停止"判定不了, 两种筛选都让它命中
                if st != status and not (st == "失败/已停止"
                                         and status in ("失败", "已停止")):
                    continue
            if kw:
                labels = r.get("labels") or []
                if not isinstance(labels, (list, tuple)):
                    labels = [labels]
                hay = " ".join([str(r.get(k, "")) for k in
                                ("project", "dataset", "val_dataset",
                                 "dataset_info")] + [str(x) for x in labels])
                if kw not in hay.lower():
                    continue
            recs.append(r)
        if self.ui.best_only_check.isChecked():
            best = {}
            for r in recs:
                m = _metric_value(r)
                if m is None:
                    continue
                key = r.get("dataset") or r.get("dataset_info") or ""
                cur = best.get(key)
                if cur is None or m > _metric_value(cur):
                    best[key] = r
            recs = list(best.values())
        self._records = self._sort_records(recs)
        self._page = 0
        self.ui.count_label.setText("共 {} 条".format(len(self._records)))
        self._render_page()

    def _sort_records(self, recs):
        # 无精度的(训练中/失败)无论升降序都沉到最后, 否则按精度升序时它们霸占榜首
        if self._sort_col == COL_METRIC:
            has = [r for r in recs if _metric_value(r) is not None]
            none = [r for r in recs if _metric_value(r) is None]
            has.sort(key=_metric_value, reverse=self._sort_desc)
            return has + none

        def key(r):
            if self._sort_col == COL_TIME:
                v = str(r.get("start_time", ""))
            elif self._sort_col == COL_DUR:
                v = _duration_seconds(r.get("duration"))
            elif self._sort_col == COL_IMG:
                try:
                    v = int(r.get("img_size") or 0)
                except (TypeError, ValueError):
                    v = 0
            elif self._sort_col == COL_DATA:
                v = str(r.get("dataset_info") or r.get("dataset") or "")
            else:
                v = TASK_TEXT.get(r.get("task", ""), "—")
            return v

        return sorted(recs, key=key, reverse=self._sort_desc)

    # ---------- 渲染 ----------

    def _render_page(self):
        t = self.ui.tableWidget
        total = len(self._records)
        pages = max(1, ceil(total / self._page_size))
        self._page = min(self._page, pages - 1)
        start = self._page * self._page_size
        page_recs = self._records[start:start + self._page_size]
        self._page_recs = page_recs
        t.clearContents()
        t.setRowCount(self._page_size)
        for i, r in enumerate(page_recs):
            st = _status(r)
            m = _metric_value(r)
            labels = r.get("labels") or []
            if not isinstance(labels, (list, tuple)):
                labels = [labels]
            label_text = " · ".join(str(x) for x in labels[:6])
            if len(labels) > 6:
                label_text += " 等 {} 类".format(len(labels))
            data_text = str(r.get("dataset_info") or r.get("dataset") or "")
            if label_text:
                data_text += "\n{}".format(label_text)
            vals = [TASK_TEXT.get(r.get("task", ""), "—"), data_text,
                    "", r.get("start_time", ""), r.get("duration", ""),
                    r.get("img_size", "")]
            for j, v in enumerate(vals):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(
                    Qt.AlignCenter if j != COL_DATA else Qt.AlignLeft | Qt.AlignVCenter)
                item.setToolTip(str(v))
                t.setItem(i, j, item)
            if m is None:
                item = QTableWidgetItem(st)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor(STATUS_COLOR.get(st, "#ffd166")))
                err = str(r.get("error") or "").strip()
                item.setToolTip(err or st)
                t.setItem(i, COL_METRIC, item)
            else:
                t.setCellWidget(i, COL_METRIC, self._make_metric_cell(
                    m, st if st != "已完成" else None, r.get("error")))
            btns = []
            tbtn = QPushButton("测试")
            tbtn.setObjectName("opsGo")
            tbtn.setEnabled(bool(r.get("model_path")))
            tbtn.clicked.connect(lambda checked=False, rec=r: self._test(rec))
            btns.append(tbtn)
            ebtn = QPushButton("导出")
            ebtn.setObjectName("opsGo")
            ebtn.setEnabled(bool(r.get("model_path")))
            ebtn.clicked.connect(lambda checked=False, rec=r: self._export(rec))
            btns.append(ebtn)
            dbtn = QPushButton("删除")
            dbtn.setObjectName("opsDel")
            dbtn.clicked.connect(lambda checked=False, rec=r: self._delete(rec))
            btns.append(dbtn)
            t.setCellWidget(i, COL_OPS, self._make_ops_cell(btns))
        self.ui.page_label.setText("{}/{}".format(self._page + 1, pages))
        self.ui.pre_page_btn.setEnabled(self._page > 0)
        self.ui.next_page_btn.setEnabled(self._page < pages - 1)
        if page_recs:
            t.selectRow(0)
        else:
            self._show_detail(None)

    # 全局 qss 的 QWidget 背景会把单元格容器刷成黑色, 用 id 选择器只对容器本身透明
    @staticmethod
    def _transparent_wrap(wrap):
        wrap.setObjectName("cellWrap")
        wrap.setStyleSheet("#cellWrap{background:transparent;}")
        return wrap

    def _make_metric_cell(self, value, status=None, error=None):
        color = METRIC_GOOD if value >= 0.8 else (
            METRIC_MID if value >= 0.5 else METRIC_BAD)
        wrap = QWidget()
        v = QVBoxLayout(wrap)
        v.setContentsMargins(2, 2, 2, 2)
        v.setSpacing(2)
        lbl = QLabel("{:.3f}".format(value))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size:12px;color:%s;" % color)
        if status:
            s = QLabel(status)
            s.setAlignment(Qt.AlignCenter)
            s.setStyleSheet("font-size:10px;color:%s;"
                            % STATUS_COLOR.get(status, METRIC_MID))
            v.addWidget(s)
            if error:
                wrap.setToolTip(error)
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(int(round(value * 100)))
        bar.setTextVisible(False)
        bar.setFixedHeight(5)
        bar.setStyleSheet(
            "QProgressBar{border:none;background:#2c303c;border-radius:2px;}"
            "QProgressBar::chunk{background:%s;border-radius:2px;}" % color)
        v.addWidget(lbl)
        v.addWidget(bar)
        return self._transparent_wrap(wrap)

    def _make_ops_cell(self, buttons):
        wrap = QWidget()
        h = QHBoxLayout(wrap)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(4)
        h.addStretch(1)
        for b in buttons:
            b.setMinimumSize(44, 26)
            b.setMaximumWidth(50)
            b.setStyleSheet(OPS_BTN_QSS[b.objectName()])
            h.addWidget(b)
        h.addStretch(1)
        return self._transparent_wrap(wrap)

    def _on_selection_changed(self):
        row = self.ui.tableWidget.currentRow()
        rec = self._page_recs[row] if 0 <= row < len(self._page_recs) else None
        self._show_detail(rec)

    # ---------- 详情面板 ----------

    def _show_detail(self, rec):
        self._current = rec
        u = self.ui
        if rec is None:
            u.detail_info.setText("选中一行查看详情")
            u.detail_curve.setPixmap(QPixmap())
            u.detail_curve.setText("")
            for b in (u.detail_metrics_btn, u.detail_test_btn,
                      u.detail_retrain_btn, u.detail_open_dir_btn):
                b.setEnabled(False)
            return
        m = _metric_value(rec)
        labels = rec.get("labels") or []
        if not isinstance(labels, (list, tuple)):
            labels = [labels]
        batch = rec.get("batch_size", "")
        if batch and str(rec.get("grad_accum", "")) not in ("", "1"):
            batch = "{} × {} 累积".format(batch, rec.get("grad_accum"))
        rows = [
            ("任务", "{} · {}".format(TASK_TEXT.get(rec.get("task", ""), "—"),
                                     rec.get("model_size", "—"))),
            ("状态", _status(rec)),
            ("精度", "{:.3f}".format(m) if m is not None else "—"),
            ("训练集", rec.get("dataset", "—")),
            ("验证集", rec.get("val_dataset", "—")),
            ("图像尺寸", rec.get("img_size", "—")),
            ("轮数 / 早停", "{} / {}".format(rec.get("epochs", "—"),
                                            rec.get("early_stop", "—"))),
            ("批大小", batch or "—"),
            ("学习率", rec.get("lr", "—")),
            ("优化器", rec.get("optimizer", "—")),
            ("设备", rec.get("device", "—")),
            ("标签", " · ".join(str(x) for x in labels) or "—"),
            ("训练时间", "{} ~ {}".format(rec.get("start_time", "—"),
                                         rec.get("end_time", "—"))),
            ("耗时", rec.get("duration", "—")),
            ("模型路径", rec.get("model_path", "—")),
        ]
        html = ""
        for k, v in rows:
            val = _esc(v)
            if k == "状态":
                val = "<span style='color:{}'>{}</span>".format(
                    STATUS_COLOR.get(v, "#e8eaf0"), val)
            html += ("<tr><td style='color:#8b8b8b;padding-right:6px;"
                     "white-space:nowrap'>{}</td><td>{}</td></tr>".format(
                         _esc(k), val))
        err = str(rec.get("error") or "").strip()
        if err:
            html += ("<tr><td style='color:#8b8b8b;padding-right:6px;"
                     "vertical-align:top;white-space:nowrap'>失败原因</td>"
                     "<td><pre style='margin:0;white-space:pre-wrap;"
                     "font-family:inherit;color:#ff9aa2'>{}</pre></td></tr>"
                     .format(_esc(err[:800])))
        u.detail_info.setText(
            "<table style='font-size:12px;line-height:150%'>{}</table>".format(html))
        self._draw_curve(rec)
        has_model = bool(rec.get("model_path"))
        u.detail_metrics_btn.setEnabled(True)
        u.detail_test_btn.setEnabled(has_model)
        u.detail_retrain_btn.setEnabled(True)
        u.detail_open_dir_btn.setEnabled(has_model)

    def _draw_curve(self, rec):
        label = self.ui.detail_curve
        label.setText("")
        series = _load_series(rec, getattr(self.app.db, "db_path", None))
        key, ys = _curve_series(series)
        if not ys:
            label.setPixmap(QPixmap())
            label.setText("暂无曲线")
            return
        w = max(120, label.width() - 4)
        h = 104
        pix = QPixmap(w, h)
        pix.fill(CURVE_BG)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor("#3a3f4b"), 1))
        p.drawRect(0, 0, w - 1, h - 1)
        lo, hi = min(ys), max(ys)
        span = max(hi - lo, 1e-6)
        pad = 8
        n = len(ys)
        pts = []
        for i, v in enumerate(ys):
            x = pad + (w - 2 * pad) * (i / max(1, n - 1))
            y = h - pad - (h - 2 * pad) * ((v - lo) / span)
            pts.append((x, y))
        p.setPen(QPen(CURVE_LINE, 2))
        for i in range(1, len(pts)):
            p.drawLine(int(pts[i - 1][0]), int(pts[i - 1][1]),
                       int(pts[i][0]), int(pts[i][1]))
        p.setPen(QColor("#8b8b8b"))
        p.drawText(6, 14, "{}  最佳 {:.3f}".format(key, hi))
        p.end()
        label.setPixmap(pix)

    def _open_model_dir(self):
        path = (self._current or {}).get("model_path", "")
        d = os.path.dirname(path) if path else ""
        if not d or not os.path.isdir(d):
            MessageBox.warning(self, "打开目录", "模型目录不存在：\n{}".format(d))
            return
        try:
            if sys.platform.startswith("win"):
                os.startfile(d)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", d])
            else:
                subprocess.Popen(["xdg-open", d])
        except Exception as e:
            MessageBox.warning(self, "打开目录", str(e))

    # ---------- 操作 ----------

    def _prev_page(self):
        if self._page > 0:
            self._page -= 1
            self._render_page()

    def _next_page(self):
        if (self._page + 1) * self._page_size < len(self._records):
            self._page += 1
            self._render_page()

    def _show_metrics(self, record):
        try:
            MetricsDialog(record, self.app.db, self).exec()
        except Exception as e:
            print("[model_dialog] 打开指标失败: {}\n{}".format(
                e, traceback.format_exc()), flush=True)
            MessageBox.warning(self, "查看指标失败", str(e))

    def _delete(self, record):
        ds = record.get("dataset", "")
        st = record.get("start_time", "")
        try:
            if not MessageBox.question(
                    self, "删除模型记录",
                    "确定删除该条模型记录？\n项目={}\n数据集={}\n开始时间={}\n".format(
                        record.get("project", ""), ds, st)):
                return
            write_log("删除模型记录: 项目={} 数据集={} 任务={} 开始时间={}".format(
                record.get("project", ""), ds,
                TASK_TEXT.get(record.get("task", ""), record.get("task", "")), st))
            self.app.db.delete_model_record(record.get("id"))
            # 模型列表同时展示训练记录: 联动删除对应训练记录(train_id)
            tid = record.get("train_id")
            if tid:
                self.app.db.delete_train_record(tid)
            else:
                # train_history 来源记录(无 train_id 字段), 直接删训练记录
                self.app.db.delete_train_record(record.get("id"))
            QTimer.singleShot(0, self._load_records)
        except Exception as e:
            trace = traceback.format_exc()
            write_log("删除模型记录失败: {} | {}".format(record.get("project", ""), e))
            print("[model_dialog] 删除失败: {}\n{}".format(e, trace), flush=True)

    def _retrain(self, record):
        """按该记录回填参数打开训练界面(任务类型/数据集/参数)。"""
        try:
            dlg = TrainDialog(self.app, preset_record=record)
            dlg.exec()
        except Exception as e:
            trace = traceback.format_exc()
            print("[model_dialog] 打开训练失败: {}\n{}".format(e, trace), flush=True)
            MessageBox.warning(self, "打开训练失败", str(e))

    def _test(self, record):
        """
        点击测试 → 弹 TestDialog，默认选中当前行的模型。
        模型界面是独立入口(显示全部项目),传 record 自己的 project/dataset
        才能让 TestDialog 正确填充数据/模型下拉。
        """
        try:
            first_pair = ""
            ds_field = record.get("dataset", "") or ""
            for tok in (x.strip() for x in ds_field.split(",") if x.strip()):
                if "/" in tok:
                    first_pair = tok
                    break
            dlg = TestDialog(
                self.app, record,
                project=record.get("project", "") or "",
                dataset=first_pair,
                parent=self.app,
            )
            self.app._test_dlg = dlg
            dlg.exec()
        except Exception as e:
            trace = traceback.format_exc()
            print("[model_dialog] 打开测试失败: {}\n{}".format(
                e, trace), flush=True)
            MessageBox.warning(self, "打开测试失败", str(e))

    # ---------------- 导出 ----------------
    def _export(self, rec):
        """
        导出模型到时间戳文件夹: onnx + classes.txt + 验证集评估报告 PDF + 调用示例。
        """
        model_path = rec.get("model_path", "") if isinstance(rec, dict) else rec
        if not model_path or not os.path.exists(model_path):
            model_dir = os.path.dirname(model_path) if model_path else ""
            for cand in ("checkpoint_best.pth", "checkpoint_best_ema.pth",
                         "checkpoint_best_regular.pth"):
                p = os.path.join(model_dir, cand)
                if os.path.exists(p):
                    model_path = p
                    break
        if not model_path or not os.path.exists(model_path):
            MessageBox.warning(self, "导出模型", "模型文件不存在：\n{}".format(model_path))
            write_log("导出模型失败: 模型文件不存在 {}".format(model_path))
            return
        d = QFileDialog.getExistingDirectory(self, "选择导出目录")
        if not d:
            return
        if not isinstance(rec, dict):
            rec = {}
        task = rec.get("task", "")
        project = str(rec.get("project", "") or "项目")
        img_size = str(rec.get("img_size", "") or "")
        model_size = str(rec.get("model_size", "") or "")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = os.path.join(d, "{}_{}".format(project, ts))
        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError as e:
            MessageBox.warning(self, "导出模型", "创建目录失败：{}".format(e))
            write_log("导出模型失败: 创建目录失败 {} | {}".format(out_dir, e))
            return
        base = "_".join([p for p in (project, TASK_TEXT.get(task, "模型"),
                                     img_size, model_size) if p])
        self._exp = {
            "rec": rec, "task": task, "out_dir": out_dir, "base": base,
            "model_path": model_path, "model_dir": os.path.dirname(model_path),
            "onnx": os.path.join(out_dir, base + ".onnx"),
            "copied": [], "report": "", "note": "",
        }
        write_log("开始导出模型: 项目={} 任务={} 架构={} 尺寸={} | {}".format(
            project, TASK_TEXT.get(task, task) or "未知", model_size, img_size,
            model_path))
        # maximum=0 → 忙碌进度条(不确定时长); 统一深色样式见 message_box.ProgressDialog
        self._exp_dlg = ProgressDialog("导出模型", "正在导出 ONNX…", self,
                                       maximum=0, cancellable=False)
        try:
            size = int(rec.get("img_size") or 0)
        except (TypeError, ValueError):
            size = 0
        self._onnx_worker = OnnxExportWorker(model_path, task,
                                             self._exp["onnx"], size, parent=self)
        self._onnx_worker.stage.connect(
            lambda msg: self._exp_dlg.set_text(
                str(msg).replace("[export] ", "")))
        self._onnx_worker.finished_ok.connect(self._export_after_onnx)
        self._onnx_worker.failed.connect(self._export_failed)
        self._onnx_worker.start()

    def _export_after_onnx(self, onnx_path):
        self._exp["copied"].append(os.path.basename(onnx_path))
        size_mb = os.path.getsize(onnx_path) / 1048576.0 if os.path.exists(onnx_path) else 0
        write_log("ONNX 导出完成: {} ({:.1f} MB)".format(
            os.path.basename(onnx_path), size_mb))
        self._write_export_classes()
        self._export_start_eval()

    def _write_export_classes(self):
        """classes.txt: 模型目录已有则复制, 否则从 data.yaml(检测/分割)或 ckpt(分类)生成。"""
        out_dir = self._exp["out_dir"]
        model_dir = self._exp["model_dir"]
        model_path = self._exp["model_path"]
        task = self._exp["task"]
        src = os.path.join(model_dir, "classes.txt")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(out_dir, "classes.txt"))
            self._exp["copied"].append("classes.txt")
            return
        yaml_src = ""
        for cand in (os.path.join(model_dir, "data.yaml"),
                     os.path.join(os.path.dirname(model_dir), "data.yaml")):
            if os.path.exists(cand):
                yaml_src = cand
                break
        try:
            if task == "classify":
                import torch
                ckpt = torch.load(model_path, map_location="cpu",
                                  weights_only=False)
                classes = ckpt.get("classes") if isinstance(ckpt, dict) else None
                if not classes:
                    return
                pairs = list(enumerate(classes))
            elif yaml_src:
                pairs = []
                with open(yaml_src, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("names:") or not line:
                            continue
                        if ":" in line:
                            k, _, v = line.partition(":")
                            if k.strip().isdigit():
                                pairs.append((int(k.strip()), v.strip().strip('"')))
            else:
                return
            if not pairs:
                return
            with open(os.path.join(out_dir, "classes.txt"), "w",
                      encoding="utf-8") as f:
                for i, name in sorted(pairs):
                    f.write("{} {}\n".format(i, name))
            self._exp["copied"].append("classes.txt")
        except Exception as e:
            write_log("生成 classes.txt 失败: {}".format(e))
            print("[export] 生成 classes.txt 失败: {}".format(e), flush=True)

    def _export_start_eval(self):
        """用验证集跑一次评估, 结果交给 build_report 出 PDF。"""
        if self._exp["task"] == "classify":
            # test_report 是检测/分割的漏检误检报告, 分类任务不适用
            write_log("导出模型报告跳过: 分类任务不出评估报告")
            self._export_finish("分类任务不生成评估报告")
            return
        cfg = self._build_eval_cfg()
        if not cfg:
            write_log("导出模型报告跳过: 未找到验证集")
            self._export_finish("未找到验证集，已跳过评估报告")
            return
        self._exp_dlg.set_text("正在生成模型报告…")
        self._eval_worker = TestWorker(cfg, parent=self)
        self._eval_worker.progress.connect(
            lambda done, total: self._exp_dlg.set_text(
                "正在生成模型报告 {}/{}".format(done, total)))
        self._eval_worker.finished_ok.connect(self._export_on_eval_done)
        self._eval_worker.failed.connect(
            lambda msg: (write_log("导出模型评估失败: {}".format(
                             (msg or "").strip().splitlines()[0] if msg else "未知")),
                         self._export_finish(
                             "评估失败，已跳过报告：{}".format((msg or "").splitlines()[0]))))
        self._eval_worker.start()

    def _build_eval_cfg(self):
        """按记录的 val_dataset 组装测试配置(与测试界面同一套 runner)。"""
        rec = self._exp["rec"]
        db = getattr(self.app, "db", None)
        if db is None:
            return None
        pairs = []
        for field in ("val_dataset", "dataset"):
            pairs = []
            for tok in str(rec.get(field, "") or "").split(","):
                tok = tok.strip()
                if "/" in tok:
                    proj, _, name = tok.partition("/")
                    if proj.strip() and name.strip():
                        pairs.append((proj.strip(), name.strip()))
            if pairs:
                break
        if not pairs:
            return None
        items, total = [], 0
        has_label, cls_mode = False, False
        for i, (proj, ds_name) in enumerate(pairs):
            binding = db.get_dataset_import(proj, ds_name) or {}
            image_paths = binding.get("image_paths") or (
                [binding["image_path"]] if binding.get("image_path") else [])
            if not image_paths:
                continue
            label_paths = binding.get("label_paths") or (
                [binding["label_path"]] if binding.get("label_path") else [])
            if i == 0:
                has_label = int(binding.get("labeled") or 0) > 0
                cls_mode = binding.get("label_fmt", "") == "cls"
            items.append({"project": proj, "dataset": ds_name,
                          "image_path": image_paths[0],
                          "label_path": label_paths[0] if label_paths else ""})
            total += int(binding.get("total") or 0)
        if not items:
            return None
        report_dir = tempfile.mkdtemp(prefix="et_eval_")
        fd, cfg_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        cfg = {
            "model_path": self._exp["model_path"], "items": items,
            "iou_threshold": 0.5, "confidence": 0.5,
            "has_label": has_label, "device": rec.get("device") or "cuda",
            "total": total, "output_labels": False,
            "task": "classify" if cls_mode else "",
            "report_dir": report_dir, "_cfg_path": cfg_path,
        }
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        return cfg

    def _export_on_eval_done(self, res):
        pdf = ""
        try:
            # matplotlib 较重, 只在真的要出报告时才导入
            from app.train.test_report import build_report
            self._inject_label_stats(res)
            pdf = build_report(
                res, out_pdf=os.path.join(
                    self._exp["out_dir"],
                    self._exp["base"] + "_评估报告.pdf"))
        except Exception:
            trace = traceback.format_exc()
            print("[export] 生成评估报告失败:\n{}".format(trace), flush=True)
            write_log("生成评估报告失败: {}".format(trace.strip().splitlines()[-1]))
        if pdf:
            self._exp["report"] = os.path.basename(pdf)
            self._exp["copied"].append(os.path.basename(pdf))
            write_log("导出模型报告完成: {}".format(os.path.basename(pdf)))
        self._export_finish("" if pdf else "评估完成，但报告生成失败")

    def _inject_label_stats(self, res):
        """把验证集的标注分布塞进 res, PDF 首页才有类别分布图。"""
        db = getattr(self.app, "db", None)
        if db is None:
            return
        pairs = []
        for field in ("val_dataset", "dataset"):
            for tok in (x.strip() for x in
                        str(self._exp["rec"].get(field, "") or "").split(",")):
                if "/" in tok:
                    proj, _, name = tok.partition("/")
                    if proj.strip() and name.strip():
                        pairs.append((proj.strip(), name.strip()))
            if pairs:
                break
        counts, colors = {}, {}
        for proj, name in pairs:
            for k, v in (db.get_dataset_label_counts(proj, name) or {}).items():
                counts[k] = counts.get(k, 0) + v
            if not colors:
                colors = dict(db.get_dataset_labels(proj, name) or {})
        if counts:
            res["label_stats"] = counts
        if colors:
            res["label_colors"] = colors

    def _export_finish(self, note=""):
        self._copy_examples()
        if self._exp_dlg is not None:
            self._exp_dlg.close()
            self._exp_dlg = None
        files = "、".join(self._exp["copied"]) or "（空）"
        write_log("导出模型完成: {} | 包含：{}".format(
            self._exp["out_dir"], files))
        msg = "已导出到：\n{}\n\n包含：{}".format(self._exp["out_dir"], files)
        if note:
            msg += "\n\n{}".format(note)
        MessageBox.information(self, "导出模型", msg)

    def _export_failed(self, msg):
        if self._exp_dlg is not None:
            self._exp_dlg.close()
            self._exp_dlg = None
        head = (msg or "").strip().splitlines()
        tip = head[0] if head else "未知错误"
        write_log("导出模型失败: {}".format(msg or "未知错误"))
        print("[export] ONNX 导出失败: {}".format(msg), flush=True)
        MessageBox.warning(
            self, "导出模型",
            "ONNX 导出失败：{}\n\n若提示缺少 onnx / onnxsim，请先安装：\n"
            "pip install onnx onnxsim".format(tip))

    def _copy_examples(self):
        src = examples_dir()
        if not src:
            return
        dst = os.path.join(self._exp["out_dir"], "examples")
        try:
            if os.path.exists(dst):
                shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst,
                            ignore=shutil.ignore_patterns("__pycache__"))
            self._exp["copied"].append("examples/")
        except OSError as e:
            write_log("复制导出示例失败: {}".format(e))
            print("[export] 复制示例失败: {}".format(e), flush=True)
