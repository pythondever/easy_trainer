# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_result.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_TestResultDialog(object):
    def setupUi(self, TestResultDialog):
        if not TestResultDialog.objectName():
            TestResultDialog.setObjectName(u"TestResultDialog")
        TestResultDialog.resize(760, 520)
        self.mainLayout = QVBoxLayout(TestResultDialog)
        self.mainLayout.setSpacing(12)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(22, 18, 22, 16)
        self.metricRow1 = QHBoxLayout()
        self.metricRow1.setSpacing(10)
        self.metricRow1.setObjectName(u"metricRow1")
        self.card_total = QFrame(TestResultDialog)
        self.card_total.setObjectName(u"card_total")
        self.card_total.setFrameShape(QFrame.NoFrame)
        self.card_total.setMinimumSize(QSize(0, 74))
        self.card_total_layout = QVBoxLayout(self.card_total)
        self.card_total_layout.setSpacing(4)
        self.card_total_layout.setObjectName(u"card_total_layout")
        self.card_total_layout.setContentsMargins(16, 12, 16, 12)
        self.total_value = QLabel(self.card_total)
        self.total_value.setObjectName(u"total_value")
        self.total_value.setAlignment(Qt.AlignCenter)

        self.card_total_layout.addWidget(self.total_value)

        self.total_lbl = QLabel(self.card_total)
        self.total_lbl.setObjectName(u"total_lbl")
        self.total_lbl.setAlignment(Qt.AlignCenter)

        self.card_total_layout.addWidget(self.total_lbl)


        self.metricRow1.addWidget(self.card_total)

        self.card_recall = QFrame(TestResultDialog)
        self.card_recall.setObjectName(u"card_recall")
        self.card_recall.setFrameShape(QFrame.NoFrame)
        self.card_recall.setMinimumSize(QSize(0, 74))
        self.card_recall_layout = QVBoxLayout(self.card_recall)
        self.card_recall_layout.setSpacing(4)
        self.card_recall_layout.setObjectName(u"card_recall_layout")
        self.card_recall_layout.setContentsMargins(16, 12, 16, 12)
        self.recall_value = QLabel(self.card_recall)
        self.recall_value.setObjectName(u"recall_value")
        self.recall_value.setAlignment(Qt.AlignCenter)

        self.card_recall_layout.addWidget(self.recall_value)

        self.recall_lbl = QLabel(self.card_recall)
        self.recall_lbl.setObjectName(u"recall_lbl")
        self.recall_lbl.setAlignment(Qt.AlignCenter)

        self.card_recall_layout.addWidget(self.recall_lbl)


        self.metricRow1.addWidget(self.card_recall)

        self.card_precision = QFrame(TestResultDialog)
        self.card_precision.setObjectName(u"card_precision")
        self.card_precision.setFrameShape(QFrame.NoFrame)
        self.card_precision.setMinimumSize(QSize(0, 74))
        self.card_precision_layout = QVBoxLayout(self.card_precision)
        self.card_precision_layout.setSpacing(4)
        self.card_precision_layout.setObjectName(u"card_precision_layout")
        self.card_precision_layout.setContentsMargins(16, 12, 16, 12)
        self.precision_value = QLabel(self.card_precision)
        self.precision_value.setObjectName(u"precision_value")
        self.precision_value.setAlignment(Qt.AlignCenter)

        self.card_precision_layout.addWidget(self.precision_value)

        self.precision_lbl = QLabel(self.card_precision)
        self.precision_lbl.setObjectName(u"precision_lbl")
        self.precision_lbl.setAlignment(Qt.AlignCenter)

        self.card_precision_layout.addWidget(self.precision_lbl)


        self.metricRow1.addWidget(self.card_precision)

        self.metricRow1.setStretch(0, 1)
        self.metricRow1.setStretch(1, 1)
        self.metricRow1.setStretch(2, 1)

        self.mainLayout.addLayout(self.metricRow1)

        self.metricRow2 = QHBoxLayout()
        self.metricRow2.setSpacing(10)
        self.metricRow2.setObjectName(u"metricRow2")
        self.card_tp = QFrame(TestResultDialog)
        self.card_tp.setObjectName(u"card_tp")
        self.card_tp.setFrameShape(QFrame.NoFrame)
        self.card_tp.setMinimumSize(QSize(0, 74))
        self.card_tp_layout = QVBoxLayout(self.card_tp)
        self.card_tp_layout.setSpacing(4)
        self.card_tp_layout.setObjectName(u"card_tp_layout")
        self.card_tp_layout.setContentsMargins(16, 12, 16, 12)
        self.tp_value = QLabel(self.card_tp)
        self.tp_value.setObjectName(u"tp_value")
        self.tp_value.setAlignment(Qt.AlignCenter)

        self.card_tp_layout.addWidget(self.tp_value)

        self.tp_lbl = QLabel(self.card_tp)
        self.tp_lbl.setObjectName(u"tp_lbl")
        self.tp_lbl.setAlignment(Qt.AlignCenter)

        self.card_tp_layout.addWidget(self.tp_lbl)


        self.metricRow2.addWidget(self.card_tp)

        self.card_fn = QFrame(TestResultDialog)
        self.card_fn.setObjectName(u"card_fn")
        self.card_fn.setFrameShape(QFrame.NoFrame)
        self.card_fn.setMinimumSize(QSize(0, 74))
        self.card_fn_layout = QVBoxLayout(self.card_fn)
        self.card_fn_layout.setSpacing(4)
        self.card_fn_layout.setObjectName(u"card_fn_layout")
        self.card_fn_layout.setContentsMargins(16, 12, 16, 12)
        self.fn_value = QLabel(self.card_fn)
        self.fn_value.setObjectName(u"fn_value")
        self.fn_value.setAlignment(Qt.AlignCenter)

        self.card_fn_layout.addWidget(self.fn_value)

        self.fn_lbl = QLabel(self.card_fn)
        self.fn_lbl.setObjectName(u"fn_lbl")
        self.fn_lbl.setAlignment(Qt.AlignCenter)

        self.card_fn_layout.addWidget(self.fn_lbl)


        self.metricRow2.addWidget(self.card_fn)

        self.card_fp = QFrame(TestResultDialog)
        self.card_fp.setObjectName(u"card_fp")
        self.card_fp.setFrameShape(QFrame.NoFrame)
        self.card_fp.setMinimumSize(QSize(0, 74))
        self.card_fp_layout = QVBoxLayout(self.card_fp)
        self.card_fp_layout.setSpacing(4)
        self.card_fp_layout.setObjectName(u"card_fp_layout")
        self.card_fp_layout.setContentsMargins(16, 12, 16, 12)
        self.fp_value = QLabel(self.card_fp)
        self.fp_value.setObjectName(u"fp_value")
        self.fp_value.setAlignment(Qt.AlignCenter)

        self.card_fp_layout.addWidget(self.fp_value)

        self.fp_lbl = QLabel(self.card_fp)
        self.fp_lbl.setObjectName(u"fp_lbl")
        self.fp_lbl.setAlignment(Qt.AlignCenter)

        self.card_fp_layout.addWidget(self.fp_lbl)


        self.metricRow2.addWidget(self.card_fp)

        self.metricRow2.setStretch(0, 1)
        self.metricRow2.setStretch(1, 1)
        self.metricRow2.setStretch(2, 1)

        self.mainLayout.addLayout(self.metricRow2)

        self.result_table = QTableWidget(TestResultDialog)
        if (self.result_table.columnCount() < 7):
            self.result_table.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.result_table.setObjectName(u"result_table")
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.result_table.setAlternatingRowColors(True)

        self.mainLayout.addWidget(self.result_table)

        self.conclusion_label = QLabel(TestResultDialog)
        self.conclusion_label.setObjectName(u"conclusion_label")
        self.conclusion_label.setWordWrap(True)

        self.mainLayout.addWidget(self.conclusion_label)

        self.btn_row = QHBoxLayout()
        self.btn_row.setObjectName(u"btn_row")
        self.sample_lbl = QLabel(TestResultDialog)
        self.sample_lbl.setObjectName(u"sample_lbl")

        self.btn_row.addWidget(self.sample_lbl)

        self.sample_spin = QSpinBox(TestResultDialog)
        self.sample_spin.setObjectName(u"sample_spin")
        self.sample_spin.setMinimum(0)
        self.sample_spin.setMaximum(999)
        self.sample_spin.setValue(10)

        self.btn_row.addWidget(self.sample_spin)

        self.btn_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.btn_row.addItem(self.btn_spacer)

        self.export_pdf_btn = QPushButton(TestResultDialog)
        self.export_pdf_btn.setObjectName(u"export_pdf_btn")

        self.btn_row.addWidget(self.export_pdf_btn)

        self.ok_btn = QPushButton(TestResultDialog)
        self.ok_btn.setObjectName(u"ok_btn")

        self.btn_row.addWidget(self.ok_btn)


        self.mainLayout.addLayout(self.btn_row)


        self.retranslateUi(TestResultDialog)

        QMetaObject.connectSlotsByName(TestResultDialog)
    # setupUi

    def retranslateUi(self, TestResultDialog):
        TestResultDialog.setWindowTitle(QCoreApplication.translate("TestResultDialog", u"\u6d4b\u8bd5\u7ed3\u679c\u5206\u6790", None))
        self.total_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.total_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.total_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6d4b\u8bd5\u5f20\u6570", None))
        self.total_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.recall_value.setText(QCoreApplication.translate("TestResultDialog", u"0%", None))
        self.recall_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.recall_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u68c0\u51fa\u7387", None))
        self.recall_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.precision_value.setText(QCoreApplication.translate("TestResultDialog", u"0%", None))
        self.precision_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.precision_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u51c6\u786e\u7387", None))
        self.precision_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.tp_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.tp_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.tp_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6b63\u786e\u68c0\u51fa", None))
        self.tp_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.fn_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.fn_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.fn_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6f0f\u68c0", None))
        self.fn_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.fp_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.fp_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.fp_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u8bef\u68c0", None))
        self.fp_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        ___qtablewidgetitem = self.result_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("TestResultDialog", u"\u7c7b\u522b", None))
        ___qtablewidgetitem1 = self.result_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("TestResultDialog", u"\u6807\u6ce8\u6570", None))
        ___qtablewidgetitem2 = self.result_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("TestResultDialog", u"\u6b63\u786e\u68c0\u51fa", None))
        ___qtablewidgetitem3 = self.result_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("TestResultDialog", u"\u6f0f\u68c0", None))
        ___qtablewidgetitem4 = self.result_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("TestResultDialog", u"\u8bef\u68c0", None))
        ___qtablewidgetitem5 = self.result_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("TestResultDialog", u"\u68c0\u51fa\u7387", None))
        ___qtablewidgetitem6 = self.result_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("TestResultDialog", u"\u51c6\u786e\u7387", None))
        self.conclusion_label.setText("")
        self.sample_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6bcf\u7c7b\u62bd\u53d6", None))
#if QT_CONFIG(tooltip)
        self.sample_spin.setToolTip(QCoreApplication.translate("TestResultDialog", u"\u6bcf\u4e2a\u7c7b\u522b\u7684\u6bcf\u79cd\u9519\u8bef\uff08\u6f0f\u68c0 / \u8bef\u68c0\uff09\u6700\u591a\u5217\u51fa\u51e0\u5f20\u56fe\u3002\n"
"\u62a5\u544a\u4f53\u79ef\u7ea6 120 KB \u4e00\u5f20\uff0c\u6837\u672c\u591a\u65f6\u8c03\u5c0f\u53ef\u4ee5\u663e\u8457\u51cf\u5c0f PDF\uff1b\u9009\u300c\u5168\u90e8\u300d\u5219\u6bcf\u5f20\u6709\u95ee\u9898\u7684\u56fe\u90fd\u5217\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.sample_spin.setSuffix(QCoreApplication.translate("TestResultDialog", u" \u5f20", None))
        self.sample_spin.setSpecialValueText(QCoreApplication.translate("TestResultDialog", u"\u5168\u90e8", None))
        self.export_pdf_btn.setText(QCoreApplication.translate("TestResultDialog", u"\u5bfc\u51fa PDF \u62a5\u544a", None))
        self.ok_btn.setText(QCoreApplication.translate("TestResultDialog", u"\u786e\u5b9a", None))
    # retranslateUi

