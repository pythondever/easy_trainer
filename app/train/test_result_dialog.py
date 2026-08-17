# -*- coding: utf-8 -*-
"""测试结果分析对话框：总览 + 按类别表格 + 结论提示（直白术语）。"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QTableWidgetItem

from ui.test_result import Ui_TestResultDialog


def _pct(v):
    return "{:.1f}%".format(v * 100)


class TestResultDialog(QDialog):
    """评估结果弹窗"""

    def __init__(self, res, parent=None):
        super().__init__(parent)
        self._ui = Ui_TestResultDialog()
        self._ui.setupUi(self)
        self._ui.ok_btn.clicked.connect(self.accept)
        self._fill(res)

    def _fill(self, res):
        u = self._ui
        if res.get("task") == "classify":
            self._fill_cls(res)
            return
        u.total_value.setText(str(res.get("total", 0)))
        u.recall_value.setText(_pct(res.get("R", 0.0)))
        u.precision_value.setText(_pct(res.get("P", 0.0)))
        u.tp_value.setText(str(res.get("TP", 0)))
        u.fn_value.setText(str(res.get("FN", 0)))
        u.fp_value.setText(str(res.get("FP", 0)))
        per_class = res.get("per_class") or {}
        self._fill_table(per_class)
        u.conclusion_label.setText(
            self._conclusion(per_class, res.get("TP", 0),
                             res.get("FP", 0), res.get("FN", 0)))

    def _fill_cls(self, res):
        """分类评估：图像维度——总精度 + 每类正确/错误/精度(复用同一对话框控件)。"""
        u = self._ui
        total = res.get("total", 0)
        per_class = res.get("per_class") or {}
        correct = sum(d.get("correct", 0) for d in per_class.values())
        error = sum(d.get("error", 0) for d in per_class.values())
        acc = res.get("accuracy", 0.0)
        u.total_value.setText(str(total))
        u.recall_lbl.setText("精度:")
        u.recall_value.setText(_pct(acc))
        u.precision_lbl.setText("正确数:")
        u.precision_value.setText(str(correct))
        u.tp_lbl.setText("正确分类:")
        u.tp_value.setText(str(correct))
        u.fn_lbl.setText("错误分类:")
        u.fn_value.setText(str(error))
        u.fp_lbl.hide()
        u.fp_value.hide()
        # 表格改为图像维度 5 列
        u.result_table.setColumnCount(5)
        u.result_table.setHorizontalHeaderLabels(
            ["类别", "总图数", "正确", "错误", "精度"])
        rows = sorted(per_class.items())
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
        rows = sorted(per_class.items())
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

    def _conclusion(self, per_class, tp, fp, fn):
        """生成一句直白结论:漏检为主还是误检为主 + 拖累最大的类别。"""
        if tp == 0 and fp == 0 and fn == 0:
            return ""
        if fn >= fp and fn > 0:
            worst = max(((c, d.get("fn", 0)) for c, d in per_class.items()),
                        key=lambda x: x[1])
            return ("整体漏检偏多（漏检 {} 个，多于误检 {} 个）。"
                    "「{}」类漏检最多（{} 个），是检出率低的主要原因。"
                    .format(fn, fp, worst[0], worst[1]))
        if fp > 0:
            worst = max(((c, d.get("fp", 0)) for c, d in per_class.items()),
                        key=lambda x: x[1])
            return ("整体误检偏多（误检 {} 个，多于漏检 {} 个）。"
                    "「{}」类误检最多（{} 个），是准确率低的主要原因。"
                    .format(fp, fn, worst[0], worst[1]))
        return "模型表现良好：无漏检、无误检。"
