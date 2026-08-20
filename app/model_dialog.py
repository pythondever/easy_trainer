# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime
from math import ceil

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QPushButton,
                               QFileDialog, QAbstractItemView, QHeaderView,
                               QSizePolicy, QHBoxLayout, QWidget)

import traceback

from PySide6.QtCore import QTimer

from app.message_box import MessageBox
from app.metrics_dialog import MetricsDialog
from app.test_dialog import TestDialog
from app.train.dialogs import TrainDialog
from ui.model import Ui_ModelDialog


class ModelDialog(QDialog):
    """模型管理：分页表格展示 db 训练记录，支持导出模型/查看指标/删除。"""

    def __init__(self, app, project="", dataset="", parent=None):
        super().__init__(parent)
        self.ui = Ui_ModelDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("模型管理")
        self.setWindowState(Qt.WindowMaximized)
        self.app = app
        self._project = project
        self._dataset = dataset
        self._records = []
        self._page = 0
        self._page_size = 15
        # 注册到 app:测试倒计时结束后由 TestDialog 关闭本窗口回首页
        self.app._model_dialog = self
        self._setup_table()
        self.ui.pre_page_btn.clicked.connect(self._prev_page)
        self.ui.next_page_btn.clicked.connect(self._next_page)
        self._load_records()

    def showEvent(self, event):
        super().showEvent(event)
        self._calc_page_size()
        self._render_page()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        old = self._page_size
        self._calc_page_size()
        if self._page_size != old:
            self._render_page()

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

    def _setup_table(self):
        t = self.ui.tableWidget
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.setSelectionBehavior(QAbstractItemView.SelectRows)
        t.setSelectionMode(QAbstractItemView.SingleSelection)
        t.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h = t.horizontalHeader()
        for i, w in enumerate([150, 150, 150, 90, 90, 90, 90, 140, 380, 80,
                               80, 80, 80, 80]):
            h.setSectionResizeMode(i, QHeaderView.Interactive)
            t.setColumnWidth(i, w)
        h.setMinimumSectionSize(60)
        h.setStretchLastSection(False)
        t.verticalHeader().setDefaultSectionSize(40)
        t.verticalHeader().setMinimumSectionSize(40)
        for c in (9, 10, 11, 12, 13):
            t.setHorizontalHeaderItem(c, QTableWidgetItem(""))

    def _calc_page_size(self):
        """每页行数 = 视口能容纳的行数，尽量铺满窗口。"""
        t = self.ui.tableWidget
        row_h = t.verticalHeader().defaultSectionSize()
        if row_h <= 0:
            row_h = 40
        self._page_size = max(10, t.viewport().height() // row_h)

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
            recs.append(m)
            seen_train_ids.add(m.get("train_id"))
        for t in train_recs:
            if t.get("id") in seen_train_ids:
                continue
            if not self._record_match(t):
                continue
            recs.append(t)
        recs.sort(key=lambda r: r.get("start_time", ""), reverse=True)
        self._records = recs
        self._page = 0
        self._render_page()

    def _record_match(self, r):
        if self._project and r.get("project") != self._project:
            return False
        if self._dataset:
            ds_list = [x.strip() for x in str(r.get("dataset", "")).split(",")]
            val_list = [x.strip() for x in str(r.get("val_dataset", "")).split(",")]
            if self._dataset not in ds_list and self._dataset not in val_list:
                return False
        return True

    def _render_page(self):
        t = self.ui.tableWidget
        total = len(self._records)
        pages = max(1, ceil(total / self._page_size))
        self._page = min(self._page, pages - 1)
        start = self._page * self._page_size
        page_recs = self._records[start:start + self._page_size]
        rows = self._page_size
        t.clearContents()
        t.setRowCount(rows)
        for i, r in enumerate(page_recs):
            map50 = r.get("map50", "")
            if map50:
                try:
                    map50 = "{:.3f}".format(float(map50))
                except (TypeError, ValueError):
                    pass
            acc = r.get("accuracy", "")
            if acc:
                try:
                    metric_val = "{:.3f}".format(float(acc))
                except (TypeError, ValueError):
                    metric_val = str(acc)
            else:
                metric_val = map50
            task_text = {"detect": "检测", "segment": "分割",
                         "classify": "分类"}.get(r.get("task", ""), "—")
            vals = [r.get("start_time", ""), r.get("end_time", ""),
                    r.get("duration", ""), r.get("model_size", ""),
                    task_text, metric_val, r.get("img_size", ""),
                    r.get("model_path", ""), r.get("dataset_info", "")]
            for j, v in enumerate(vals):
                text = str(v)
                if j == 7:
                    text = os.path.dirname(str(v)) if v else ""
                    item = QTableWidgetItem(text)
                    item.setToolTip(str(v))
                elif j == 8:
                    full = str(v)
                    item = QTableWidgetItem(full)
                    item.setToolTip(full)
                else:
                    item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                t.setItem(i, j, item)
            btn = QPushButton("导出")
            path = r.get("model_path", "")
            btn.setEnabled(bool(path))
            btn.setFixedSize(60, 26)
            btn.clicked.connect(lambda checked=False, rec=r: self._export(rec))
            t.setCellWidget(i, 9, self._make_centered_cell(btn))
            mbtn = QPushButton("指标")
            mbtn.setFixedSize(60, 26)
            mbtn.clicked.connect(
                lambda checked=False, rec=r: self._show_metrics(rec))
            t.setCellWidget(i, 10, self._make_centered_cell(mbtn))
            dbtn = QPushButton("删除")
            dbtn.setFixedSize(60, 26)
            dbtn.clicked.connect(
                lambda checked=False, rec=r: self._delete(rec))
            t.setCellWidget(i, 11, self._make_centered_cell(dbtn))
            tbtn = QPushButton("测试")
            tbtn.setFixedSize(60, 26)
            tbtn.setEnabled(bool(r.get("model_path")))
            tbtn.clicked.connect(
                lambda checked=False, rec=r: self._test(rec))
            t.setCellWidget(i, 12, self._make_centered_cell(tbtn))
            trbtn = QPushButton("训练")
            trbtn.setFixedSize(60, 26)
            trbtn.clicked.connect(
                lambda checked=False, rec=r: self._retrain(rec))
            t.setCellWidget(i, 13, self._make_centered_cell(trbtn))
        self.ui.page_label.setText("{}/{}".format(self._page + 1, pages))
        self.ui.pre_page_btn.setEnabled(self._page > 0)
        self.ui.next_page_btn.setEnabled(self._page < pages - 1)

    def _make_centered_cell(self, widget):
        """包裹按钮到 QWidget + QHBoxLayout，让 cellWidget 居中显示。"""
        wrap = QWidget()
        wrap.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h = QHBoxLayout(wrap)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        h.addStretch(1)
        h.addWidget(widget)
        h.addStretch(1)
        h.setAlignment(Qt.AlignCenter)
        return wrap

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
            MetricsDialog(record, self).exec()
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
            self.app.db.delete_model_record(record.get("id"))
            QTimer.singleShot(0, self._load_records)
        except Exception as e:
            trace = traceback.format_exc()
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

    def _export(self, rec):
        """
        导出模型: 建时间戳文件夹, 模型命名 "项目_任务_图像尺寸_模型规模.pth",
        附带 classes.txt 供使用者对照类别。
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
                return
        d = QFileDialog.getExistingDirectory(self, "选择导出目录")
        if not d:
            return
        if not isinstance(rec, dict):
            rec = {}
        task_text = {"detect": "检测", "segment": "分割",
                     "classify": "分类"}.get(rec.get("task", ""), "模型")
        project = str(rec.get("project", "") or "项目")
        img_size = str(rec.get("img_size", "") or "")
        model_size = str(rec.get("model_size", "") or "")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            out_dir = os.path.join(d, "{}_{}".format(project, ts))
            os.makedirs(out_dir, exist_ok=True)
            ext = os.path.splitext(os.path.basename(model_path))[1] or ".pth"
            base = "_".join([p for p in (project, task_text,
                                         img_size, model_size) if p])
            dst_model = os.path.join(out_dir, base + ext)
            shutil.copy2(model_path, dst_model)
            copied = []
            model_dir = os.path.dirname(model_path)
            yaml_src = ""
            # classes.txt: 目录已有则复制; data.yaml 只读不复制(解析 names 用)
            src = os.path.join(model_dir, "classes.txt")
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(out_dir, "classes.txt"))
                copied.append("classes.txt")
            for cand in (os.path.join(model_dir, "data.yaml"),
                         os.path.join(os.path.dirname(model_dir), "data.yaml")):
                if os.path.exists(cand):
                    yaml_src = cand
                    break
            if "classes.txt" not in copied:
                generated = False
                if task_text == "分类":
                    try:
                        import torch
                        ckpt = torch.load(model_path, map_location="cpu",
                                          weights_only=False)
                        classes = ckpt.get("classes") if isinstance(ckpt, dict) else None
                        if classes:
                            with open(os.path.join(out_dir, "classes.txt"),
                                      "w", encoding="utf-8") as f:
                                for i, lb in enumerate(classes):
                                    f.write("{} {}\n".format(i, lb))
                            generated = True
                    except Exception:
                        pass
                elif yaml_src and os.path.exists(yaml_src):
                    try:
                        # 解析 data.yaml 的 names: {id: name}
                        pairs = []
                        with open(yaml_src, "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line.startswith("names:") or not line:
                                    continue
                                if ":" in line:
                                    k, _, v = line.partition(":")
                                    if k.strip().isdigit():
                                        pairs.append(
                                            (int(k.strip()), v.strip().strip('"')))
                        if pairs:
                            with open(os.path.join(out_dir, "classes.txt"),
                                      "w", encoding="utf-8") as f:
                                for _, name in sorted(pairs):
                                    f.write("{} {}\n".format(_, name))
                            generated = True
                    except Exception:
                        pass
                if generated:
                    copied.append("classes.txt(生成)")
            MessageBox.information(self, "导出模型", "导出成功")
        except OSError as e:
            MessageBox.warning(self, "导出模型", "导出失败：{}".format(e))