# -*- coding: utf-8 -*-
"""测试结果分析对话框: 总览 + 按类别表格 + 结论提示(直白术语)."""

import datetime
import os
import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, \
    QSizePolicy, QTableWidgetItem
from app.core.label_utils import label_sort_key
from app.train.export_worker import ReportWorker
from app.widgets.message_box import MessageBox
from app.widgets.dialog_buttons import apply_icon
from ui.test_result import Ui_TestResultDialog


def _pct(v):
    return "{:.1f}%".format(v * 100)


def _ratio(a, b):
    return a / b if b else 0.0


def _rate_color(v, lower_better=False):
    """阈值与模型评估表格保持一致."""
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


def _fit_table_size(table, stretch_last=False, fit_height=False):
    """
    给表格量出贴合内容的下限宽度, 上限高度.
    QTableWidget 不把列宽算进自己的最小宽度, 窗口一窄就冒横向滚动条、
    末列被挡在视野外. 卡片区变窄时(长语言反而会更宽)就会挤到表格.
    高度正相反: 默认策略会把剩余空间全吃掉, 只有一两行时下面空出一大片.
    fit_height 只给异常检测用 —— 它的表固定一行, 而检测/分类的行数不定,
    它们靠表格吃掉剩余高度才不会把卡片撑开.
    """
    table.ensurePolished()          # 列宽要在样式表生效后量, 否则字体字号还没定
    table.resizeColumnsToContents()
    total = sum(table.columnWidth(c) for c in range(table.columnCount()))
    total += table.frameWidth() * 2 + table.verticalScrollBar().sizeHint().width()
    vh = table.verticalHeader()     # 行号列也占视野宽度
    if not vh.isHidden():
        total += max(vh.width(), vh.sizeHint().width())
    table.setMinimumWidth(total + 4)
    if fit_height:
        hh = max(table.horizontalHeader().height(),
                 table.horizontalHeader().sizeHint().height())
        rows = sum(table.rowHeight(r) for r in range(table.rowCount()))
        table.setMaximumHeight(hh + rows + table.frameWidth() * 2 + 4)
    else:
        table.setMaximumHeight(16777215)
    table.horizontalHeader().setStretchLastSection(stretch_last)


def _default_pdf_name(res):
    """默认文件名: 模型名_时间戳.pdf. 模型名做 sanitize, 避开路径分隔符与 Windows 非法字符."""
    model = (res.get("model") or "model")
    model = model.split("/")[-1].split("\\")[-1]
    model = re.sub(r'[\\/:*?"<>|\s]+', "_", model).strip("._") or "model"
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return "{}_{}.pdf".format(model, ts)


class TestResultDialog(QDialog):
    def __init__(self, res, per_class_limit=None, parent=None):
        super().__init__(parent)
        self._ui = Ui_TestResultDialog()
        self._ui.setupUi(self)
        apply_icon(self._ui.ok_btn, self.tr("确定"))
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
        """没有逐图明细(纯推理无标签 / 无错误样本)时导出按钮不可用."""
        has_detail = bool(self._res.get("detail_path"))
        self._ui.export_pdf_btn.setEnabled(has_detail)
        self._ui.sample_spin.setEnabled(has_detail)
        self._ui.sample_lbl.setEnabled(has_detail)
        if has_detail:
            tip = self.tr("把漏检/误检的图逐张画框导出成 PDF")
        elif self._res.get("task") == "ad":
            # 异常检测的逐图明细是 CSV(没有框可画), PDF 报告是给带框任务做的
            tip = self.tr("异常检测的逐图结果已写成 CSV, 不支持导出画框 PDF")
        else:
            tip = self.tr("本次测试没有逐图错误明细, 无法导出")
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
            self, self.tr("保存 PDF 报告"), default_path,
            self.tr("PDF 文件 (*.pdf)"))
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        self._ui.export_pdf_btn.setEnabled(False)
        self._ui.export_pdf_btn.setText(self.tr("正在生成..."))
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self._worker = ReportWorker(
            self._res, out_pdf=path,
            per_class_limit=self._ui.sample_spin.value(), parent=self)
        self._worker.done.connect(self._on_export_done)
        self._worker.failed.connect(self._on_export_failed)
        self._worker.start()

    def _restore_btn(self):
        QApplication.restoreOverrideCursor()
        self._ui.export_pdf_btn.setText(self.tr("导出 PDF 报告"))
        self._sync_export_btn()

    def _on_export_done(self, path):
        self._restore_btn()
        if not path:
            MessageBox.information(
                self, self.tr("无需导出"),
                self.tr("本次测试没有漏检也没有误检, 没有内容可写."))
            return
        MessageBox.information(
            self, self.tr("导出完成"),
            self.tr("PDF 报告已保存到:\n{}").format(path))

    def _on_export_failed(self, msg):
        self._restore_btn()
        MessageBox.warning(self, self.tr("导出失败"), msg)

    def closeEvent(self, event):
        # 线程还在跑时不能直接销毁, 否则 Qt 会崩
        if self._worker is not None and self._worker.isRunning():
            self._worker.quit()
            self._worker.wait(3000)
        super().closeEvent(event)

    def _fill(self, res):
        u = self._ui
        # 异常检测会把这两张卡和"每类抽取"收起来、并把几块改成不被拉伸,
        # 复用同一实例填别的任务时要放回来
        u.card_img_fn.setVisible(True)
        u.card_img_fp.setVisible(True)
        u.sample_lbl.setVisible(True)
        u.sample_spin.setVisible(True)
        for w in (u.section_img, u.conclusion_label):
            w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        if res.get("task") == "classify":
            self._fill_cls(res)
            return
        if res.get("task") == "ad":
            self._fill_ad(res)
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
        # 无标注图不进检出/未检出的分母, 数量对不上时把分母标出来
        note = self.tr("按\"张\"统计 · 检出 1 个即算检出")
        if img_gt != total:
            note += self.tr(" · 有标注 {} 张").format(img_gt)
        u.dim_img_note.setText(note)
        u.img_total_value.setText(str(total))
        u.img_ok_value.setText(str(img_ok))
        _card(u, "img_ok", self.tr("检出图像"), _ratio(img_ok, img_gt),
              self.tr("检出率 "))
        u.img_fn_value.setText(str(img_miss))
        _card(u, "img_fn", self.tr("未检出图像"),
              _ratio(img_miss, img_gt), self.tr("未检出率 "),
              lower_better=True)
        u.img_fp_value.setText(str(img_fp))
        _card(u, "img_fp", self.tr("有误检图像"),
              _ratio(img_fp, total), self.tr("误检率 "), lower_better=True)

        per_class = res.get("per_class") or {}
        gt_total = sum(d.get("gt", 0) for d in per_class.values())
        u.dim_lbl_note.setText(
            self.tr("按\"标注框\"统计 · 标注总数 {}").format(gt_total))
        u.tp_value.setText(str(tp))
        _card(u, "tp", self.tr("正确检出"), _ratio(tp, tp + fn),
              self.tr("检出率 "))
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
        # 分类一张图只判一个类别, 没有"标注框"这一层, 只保留图像维度
        u.section_lbl.setVisible(False)
        u.dim_img_note.setText(self.tr("按\"张\"统计 · 每张图判一个类别"))
        u.img_total_value.setText(str(total))
        u.img_total_lbl.setText(self.tr("测试张数"))
        u.img_total_rate.setText("")
        u.img_ok_value.setText(str(correct))
        _card(u, "img_ok", self.tr("判断正确"), _ratio(correct, total))
        u.img_fn_value.setText(str(error))
        _card(u, "img_fn", self.tr("判断错误"),
              _ratio(error, total), lower_better=True)
        u.img_fp_value.setText(_pct(acc))
        u.img_fp_lbl.setText(self.tr("精度"))
        u.img_fp_rate.setText("")
        u.img_fp_value.setStyleSheet("color:{}".format(_rate_color(acc)))
        self._fill_class_table(per_class)
        if per_class:
            worst = max(per_class.items(), key=lambda kv: kv[1].get("error", 0))
            u.conclusion_label.setText(
                self.tr("整体精度 {:.1f}%, \"{}\"类错误最多({} 张),"
                        " 是拉低精度的主要原因.").format(
                    acc * 100, worst[0], worst[1].get("error", 0)))
        else:
            u.conclusion_label.setText("")

    def _fill_ad(self, res):
        """
        异常检测: 只报检出了多少张, 不做良品/不良品的对照统计.
        测试侧的真值是从挂上来的目录现场推的, 单类批量(现场最常见)时整批都算
        良品, 准确率/漏检/误检既算不出也没人看. 交付口径就是检出张数 + 逐图明细.
        """
        u = self._ui
        total = res.get("total", 0)
        thr = float(res.get("threshold") or 0.0)
        # 判定 = 分数 >= 阈值; 模型里没存阈值就判不出, 只能报分数
        hit = int(res.get("TP", 0)) + int(res.get("FP", 0)) if thr > 0 else None
        u.section_lbl.setVisible(False)
        u.dim_img_note.setText(self.tr("按\"张\"统计 · 整图判良品/不良品"))
        u.img_total_value.setText(str(total))
        u.img_total_lbl.setText(self.tr("测试张数"))
        u.img_total_rate.setText("")
        # 没有"过杀/漏检"的对照量, 这两张卡收起来让前两张占满
        u.card_img_fn.setVisible(False)
        u.card_img_fp.setVisible(False)
        # 每类抽取只影响画框 PDF 的样本数, 而 AD 的明细是 CSV, 导出本就禁用
        u.sample_lbl.setVisible(False)
        u.sample_spin.setVisible(False)
        # 表格只有一行, 卡片与结论行都收住高度, 否则剩余空间会全灌进它们
        for w in (u.section_img, u.conclusion_label):
            w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        u.img_ok_value.setText("--" if hit is None else str(hit))
        _card(u, "img_ok", self.tr("检出异常"))
        self._fill_ad_table(res.get("per_class") or {})
        u.conclusion_label.setText(self._conclusion_ad(total, hit, thr))
        # 内容只有两卡一行, 多余高度集中留到按钮上方, 否则会被均分成几道空隙
        u.mainLayout.insertStretch(u.mainLayout.count() - 1, 1)

    def _fill_ad_table(self, per_class):
        """异常检测的类别表: 只有图数与检出数, 没有真值这一层."""
        u = self._ui
        u.result_table.setColumnCount(3)
        u.result_table.setHorizontalHeaderLabels(
            [self.tr("类别"), self.tr("总图数"), self.tr("检出异常")])
        rows = sorted(per_class.items(), key=lambda kv: label_sort_key(str(kv[0])))
        u.result_table.setRowCount(len(rows))
        for i, (cls, d) in enumerate(rows):
            # 未具名的散图不叫"(根目录散图)": 与写出的标注同名, 都叫"异常"
            name = self.tr("异常") if d.get("unnamed") else str(cls)
            vals = [name, str(d.get("total", 0)), str(d.get("hit", 0))]
            for j, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setTextAlignment(
                    Qt.AlignLeft | Qt.AlignVCenter if j == 0
                    else Qt.AlignCenter)
                u.result_table.setItem(i, j, item)
        # 3 列只有一行, 让最后一列铺满、高度贴合内容, 否则挤在左边、下面空一片
        _fit_table_size(u.result_table, stretch_last=True, fit_height=True)

    def _fill_class_table(self, per_class):
        """分类的类别表: 总图数/正确/错误/精度."""
        u = self._ui
        u.result_table.setColumnCount(5)
        u.result_table.setHorizontalHeaderLabels(
            [self.tr("类别"), self.tr("总图数"), self.tr("正确"),
             self.tr("错误"), self.tr("精度")])
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
        _fit_table_size(u.result_table)

    def _conclusion_ad(self, total, hit, thr):
        if thr <= 0:
            return self.tr(
                "模型里没有判定阈值, 只报告分数, 逐图分数见 CSV 明细.")
        return self.tr("判定阈值 {:.4f}. 本次 {} 张, 检出异常 {} 张.").format(
            thr, total, hit)

    def _fill_table(self, per_class):
        u = self._ui
        # 列数与表头在这里显式重设: 异常检测用的是 3 列版本, 同一实例切回来
        # 不能指望 .ui 里那份默认值还在
        u.result_table.setColumnCount(7)
        u.result_table.setHorizontalHeaderLabels(
            [self.tr("类别"), self.tr("标注数"), self.tr("正确检出"),
             self.tr("漏检"), self.tr("误检"), self.tr("检出率"),
             self.tr("准确率")])
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
        _fit_table_size(u.result_table)

    def _conclusion(self, per_class, tp, fp, fn, conf=None):
        if tp == 0 and fp == 0 and fn == 0:
            return ""
        if fn >= fp and fn > 0:
            worst = max(((c, d.get("fn", 0)) for c, d in per_class.items()),
                        key=lambda x: x[1])
            base = (self.tr("整体漏检偏多(漏检 {} 个, 多于误检 {} 个)."
                           "\"{}\"类漏检最多({} 个), 是检出率低的主要原因.")
                    .format(fn, fp, worst[0], worst[1]))
        elif fp > 0:
            worst = max(((c, d.get("fp", 0)) for c, d in per_class.items()),
                        key=lambda x: x[1])
            base = (self.tr("整体误检偏多(误检 {} 个, 多于漏检 {} 个)."
                           "\"{}\"类误检最多({} 个), 是准确率低的主要原因.")
                    .format(fp, fn, worst[0], worst[1]))
        else:
            return self.tr("模型表现良好: 无漏检, 无误检.")
        if conf:
            base += self.tr("另有 {} 处位置对但类别判错(报告里用紫框标出),"
                            "属分类能力不足, 需补易混淆类别的区分性样本.").format(conf)
        return base
