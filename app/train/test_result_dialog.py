# -*- coding: utf-8 -*-
"""测试结果分析对话框：总览 + 按类别表格 + 结论提示（直白术语）。"""

import datetime
import os
import re
import traceback

from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, \
    QTableWidgetItem
from app.core.label_utils import label_sort_key
from app.widgets.message_box import MessageBox
from app.widgets.dialog_buttons import apply_icon
from ui.test_result import Ui_TestResultDialog


def _pct(v):
    return "{:.1f}%".format(v * 100)


def _ratio(a, b):
    return a / b if b else 0.0


def _rate_color(v, lower_better=False):
    """阈值与模型评估表格保持一致。"""
    score = 1.0 - v if lower_better else v
    if score >= 0.85:
        return "#7be39a"
    return "#e8eaf0" if score >= 0.6 else "#ffb46b"


def _rate_span(v, lower_better=False):
    return '<span style="color:{}">{}</span>'.format(
        _rate_color(v, lower_better), _pct(v))


def _card(u, name, text, rate=None, rate_prefix="", lower_better=False):
    getattr(u, name + "_lbl").setText(text)
    rate_lbl = getattr(u, name + "_rate")
    if rate is None:
        rate_lbl.setText("")
    else:
        rate_lbl.setText("{}{}".format(rate_prefix,
                                       _rate_span(rate, lower_better)))


def _default_pdf_name(res):
    """默认文件名：模型名_时间戳.pdf。模型名做 sanitize，避开路径分隔符与 Windows 非法字符。"""
    model = (res.get("model") or "model")
    model = model.split("/")[-1].split("\\")[-1]
    model = re.sub(r'[\\/:*?"<>|\s]+', "_", model).strip("._") or "model"
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return "{}_{}.pdf".format(model, ts)


class _PdfExportWorker(QThread):
    """原图可能 6500 万像素，重绘缩略图单张就要 1~3 秒，必须离开 UI 线程。"""

    done = Signal(str)
    failed = Signal(str)

    def __init__(self, res, per_class_limit=None, out_pdf=None, parent=None):
        super().__init__(parent)
        self._res = res
        self._limit = per_class_limit
        self._out_pdf = out_pdf

    def run(self):
        try:
            from app.train.test_report import build_report
            kwargs = {"out_pdf": self._out_pdf} if self._out_pdf else {}
            if self._limit is None:
                self.done.emit(build_report(self._res, **kwargs) or "")
            else:
                self.done.emit(
                    build_report(self._res, per_class_limit=self._limit,
                                 **kwargs) or "")
        except Exception as exc:
            self.failed.emit("{}\n\n{}".format(exc, traceback.format_exc()))


class TestResultDialog(QDialog):
    def __init__(self, res, per_class_limit=None, parent=None):
        super().__init__(parent)
        self._ui = Ui_TestResultDialog()
        self._ui.setupUi(self)
        apply_icon(self._ui.ok_btn, "确定")
        self._ui.ok_btn.clicked.connect(self.accept)
        self._ui.export_pdf_btn.clicked.connect(self._on_export)
        self._res = res
        self._worker = None
        if per_class_limit is not None:
            self._ui.sample_spin.setValue(per_class_limit)
        self._fill(res)
        self._sync_export_btn()

    # ---------------- 导出 PDF ----------------

    def _sync_export_btn(self):
        """没有逐图明细(纯推理无标签 / 无错误样本)时导出按钮不可用。"""
        has_detail = bool(self._res.get("detail_path"))
        self._ui.export_pdf_btn.setEnabled(has_detail)
        self._ui.sample_spin.setEnabled(has_detail)
        self._ui.sample_lbl.setEnabled(has_detail)
        tip = ("把漏检/误检的图逐张画框导出成 PDF" if has_detail
               else "本次测试没有逐图错误明细，无法导出")
        self._ui.export_pdf_btn.setToolTip(tip)

    def _on_export(self):
        if self._worker is not None and self._worker.isRunning():
            return
        default_dir = self._res.get("report_dir") or os.path.dirname(
            self._res.get("detail_path") or "") or os.getcwd()
        if not os.path.isdir(default_dir):
            default_dir = os.getcwd()
        default_path = os.path.join(default_dir, _default_pdf_name(self._res))
        path, _ = QFileDialog.getSaveFileName(
            self, "保存 PDF 报告", default_path, "PDF 文件 (*.pdf)")
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        self._ui.export_pdf_btn.setEnabled(False)
        self._ui.export_pdf_btn.setText("正在生成…")
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self._worker = _PdfExportWorker(
            self._res, self._ui.sample_spin.value(), path, self)
        self._worker.done.connect(self._on_export_done)
        self._worker.failed.connect(self._on_export_failed)
        self._worker.start()

    def _restore_btn(self):
        QApplication.restoreOverrideCursor()
        self._ui.export_pdf_btn.setText("导出 PDF 报告")
        self._sync_export_btn()

    def _on_export_done(self, path):
        self._restore_btn()
        if not path:
            MessageBox.information(
                self, "无需导出",
                "本次测试没有漏检也没有误检，没有内容可写。")
            return
        MessageBox.information(
            self, "导出完成", "PDF 报告已保存到：\n{}".format(path))

    def _on_export_failed(self, msg):
        self._restore_btn()
        MessageBox.warning(self, "导出失败", msg)

    def closeEvent(self, event):
        # 线程还在跑时不能直接销毁，否则 Qt 会崩
        if self._worker is not None and self._worker.isRunning():
            self._worker.quit()
            self._worker.wait(3000)
        super().closeEvent(event)

    def _fill(self, res):
        u = self._ui
        if res.get("task") == "classify":
            self._fill_cls(res)
            return
        total = res.get("total", 0) or 0
        tp = res.get("TP", 0)
        fn = res.get("FN", 0)
        fp = res.get("FP", 0)
        p = res.get("P", 0.0)
        img_gt = res.get("img_gt", 0)
        img_ok = res.get("img_ok", 0)
        img_miss = res.get("img_miss", 0)
        img_fp = res.get("img_fp", 0)
        # 无标注图不进检出/未检出的分母，数量对不上时把分母标出来
        note = "按「张」统计 · 检出 1 个即算检出"
        if img_gt != total:
            note += " · 有标注 {} 张".format(img_gt)
        u.dim_img_note.setText(note)
        u.img_total_value.setText(str(total))
        u.img_ok_value.setText(str(img_ok))
        _card(u, "img_ok", "检出图像", _ratio(img_ok, img_gt), "检出率 ")
        u.img_fn_value.setText(str(img_miss))
        _card(u, "img_fn", "未检出图像",
              _ratio(img_miss, img_gt), "未检出率 ", lower_better=True)
        u.img_fp_value.setText(str(img_fp))
        _card(u, "img_fp", "有误检图像",
              _ratio(img_fp, total), "误检率 ", lower_better=True)

        per_class = res.get("per_class") or {}
        gt_total = sum(d.get("gt", 0) for d in per_class.values())
        u.dim_lbl_note.setText("按「标注框」统计 · 标注总数 {}".format(gt_total))
        u.tp_value.setText(str(tp))
        _card(u, "tp", "正确检出", _ratio(tp, tp + fn), "检出率 ")
        u.fn_value.setText(str(fn))
        u.fp_value.setText(str(fp))
        u.precision_value.setText(_pct(p))
        u.precision_value.setStyleSheet("color:{}".format(_rate_color(p)))
        self._fill_table(per_class)
        u.conclusion_label.setText(
            self._conclusion(per_class, res.get("TP", 0),
                             res.get("FP", 0), res.get("FN", 0),
                             res.get("conf_total")))

    def _fill_cls(self, res):
        u = self._ui
        total = res.get("total", 0)
        per_class = res.get("per_class") or {}
        correct = sum(d.get("correct", 0) for d in per_class.values())
        error = sum(d.get("error", 0) for d in per_class.values())
        acc = res.get("accuracy", 0.0)
        # 分类一张图只判一个类别，没有「标注框」这一层，只保留图像维度
        u.section_lbl.setVisible(False)
        u.dim_img_note.setText("按「张」统计 · 每张图判一个类别")
        u.img_total_value.setText(str(total))
        u.img_total_lbl.setText("测试张数")
        u.img_total_rate.setText("")
        u.img_ok_value.setText(str(correct))
        _card(u, "img_ok", "判断正确", _ratio(correct, total))
        u.img_fn_value.setText(str(error))
        _card(u, "img_fn", "判断错误",
              _ratio(error, total), lower_better=True)
        u.img_fp_value.setText(_pct(acc))
        u.img_fp_lbl.setText("精度")
        u.img_fp_rate.setText("")
        u.img_fp_value.setStyleSheet("color:{}".format(_rate_color(acc)))
        u.result_table.setColumnCount(5)
        u.result_table.setHorizontalHeaderLabels(
            ["类别", "总图数", "正确", "错误", "精度"])
        # 类别名按自然排序(纯数字按数值,非数字按字典序),与首页标签下拉一致
        rows = sorted(per_class.items(), key=lambda kv: label_sort_key(str(kv[0])))
        u.result_table.setRowCount(len(rows))
        for i, (cls, d) in enumerate(rows):
            t = d.get("total", 0)
            c = d.get("correct", 0)
            e = d.get("error", 0)
            pa = c / t if t else 0.0
            vals = [str(cls), str(t), str(c), str(e), _pct(pa)]
            for j, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setTextAlignment(
                    Qt.AlignLeft | Qt.AlignVCenter if j == 0
                    else Qt.AlignCenter)
                u.result_table.setItem(i, j, item)
        u.result_table.resizeColumnsToContents()
        if per_class:
            worst = max(per_class.items(), key=lambda kv: kv[1].get("error", 0))
            u.conclusion_label.setText(
                "整体精度 {:.1f}%，「{}」类错误最多（{} 张），是拉低精度的主要原因。".format(
                    acc * 100, worst[0], worst[1].get("error", 0)))
        else:
            u.conclusion_label.setText("")

    def _fill_table(self, per_class):
        u = self._ui
        rows = sorted(per_class.items(), key=lambda kv: label_sort_key(str(kv[0])))
        u.result_table.setRowCount(len(rows))
        for i, (cls, d) in enumerate(rows):
            gt = d.get("gt", 0)
            tp = d.get("tp", 0)
            fn = d.get("fn", 0)
            fp = d.get("fp", 0)
            rec = tp / (tp + fn) if (tp + fn) else 0.0
            prec = tp / (tp + fp) if (tp + fp) else 0.0
            vals = [str(cls), str(gt), str(tp), str(fn), str(fp),
                    _pct(rec), _pct(prec)]
            for j, v in enumerate(vals):
                item = QTableWidgetItem(v)
                if j == 0:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                u.result_table.setItem(i, j, item)
        u.result_table.resizeColumnsToContents()

    def _conclusion(self, per_class, tp, fp, fn, conf=None):
        if tp == 0 and fp == 0 and fn == 0:
            return ""
        if fn >= fp and fn > 0:
            worst = max(((c, d.get("fn", 0)) for c, d in per_class.items()),
                        key=lambda x: x[1])
            base = ("整体漏检偏多（漏检 {} 个，多于误检 {} 个）。"
                    "「{}」类漏检最多（{} 个），是检出率低的主要原因。"
                    .format(fn, fp, worst[0], worst[1]))
        elif fp > 0:
            worst = max(((c, d.get("fp", 0)) for c, d in per_class.items()),
                        key=lambda x: x[1])
            base = ("整体误检偏多（误检 {} 个，多于漏检 {} 个）。"
                    "「{}」类误检最多（{} 个），是准确率低的主要原因。"
                    .format(fp, fn, worst[0], worst[1]))
        else:
            return "模型表现良好：无漏检、无误检。"
        if conf:
            base += ("另有 {} 处位置对但类别判错（报告里用紫框标出），"
                     "属分类能力不足，需补易混淆类别的区分性样本。".format(conf))
        return base
