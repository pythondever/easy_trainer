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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_TestResultDialog(object):
    def setupUi(self, TestResultDialog):
        if not TestResultDialog.objectName():
            TestResultDialog.setObjectName(u"TestResultDialog")
        TestResultDialog.resize(680, 480)
        self.verticalLayout = QVBoxLayout(TestResultDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.overview_row1 = QHBoxLayout()
        self.overview_row1.setObjectName(u"overview_row1")
        self.total_lbl = QLabel(TestResultDialog)
        self.total_lbl.setObjectName(u"total_lbl")

        self.overview_row1.addWidget(self.total_lbl)

        self.total_value = QLabel(TestResultDialog)
        self.total_value.setObjectName(u"total_value")

        self.overview_row1.addWidget(self.total_value)

        self.spacer_row1_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overview_row1.addItem(self.spacer_row1_1)

        self.recall_lbl = QLabel(TestResultDialog)
        self.recall_lbl.setObjectName(u"recall_lbl")

        self.overview_row1.addWidget(self.recall_lbl)

        self.recall_value = QLabel(TestResultDialog)
        self.recall_value.setObjectName(u"recall_value")

        self.overview_row1.addWidget(self.recall_value)

        self.spacer_row1_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overview_row1.addItem(self.spacer_row1_2)

        self.precision_lbl = QLabel(TestResultDialog)
        self.precision_lbl.setObjectName(u"precision_lbl")

        self.overview_row1.addWidget(self.precision_lbl)

        self.precision_value = QLabel(TestResultDialog)
        self.precision_value.setObjectName(u"precision_value")

        self.overview_row1.addWidget(self.precision_value)


        self.verticalLayout.addLayout(self.overview_row1)

        self.overview_row2 = QHBoxLayout()
        self.overview_row2.setObjectName(u"overview_row2")
        self.tp_lbl = QLabel(TestResultDialog)
        self.tp_lbl.setObjectName(u"tp_lbl")

        self.overview_row2.addWidget(self.tp_lbl)

        self.tp_value = QLabel(TestResultDialog)
        self.tp_value.setObjectName(u"tp_value")

        self.overview_row2.addWidget(self.tp_value)

        self.spacer_row2_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overview_row2.addItem(self.spacer_row2_1)

        self.fn_lbl = QLabel(TestResultDialog)
        self.fn_lbl.setObjectName(u"fn_lbl")

        self.overview_row2.addWidget(self.fn_lbl)

        self.fn_value = QLabel(TestResultDialog)
        self.fn_value.setObjectName(u"fn_value")

        self.overview_row2.addWidget(self.fn_value)

        self.spacer_row2_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.overview_row2.addItem(self.spacer_row2_2)

        self.fp_lbl = QLabel(TestResultDialog)
        self.fp_lbl.setObjectName(u"fp_lbl")

        self.overview_row2.addWidget(self.fp_lbl)

        self.fp_value = QLabel(TestResultDialog)
        self.fp_value.setObjectName(u"fp_value")

        self.overview_row2.addWidget(self.fp_value)


        self.verticalLayout.addLayout(self.overview_row2)

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

        self.verticalLayout.addWidget(self.result_table)

        self.conclusion_label = QLabel(TestResultDialog)
        self.conclusion_label.setObjectName(u"conclusion_label")
        self.conclusion_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.conclusion_label)

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

        self.reveal_btn = QPushButton(TestResultDialog)
        self.reveal_btn.setObjectName(u"reveal_btn")

        self.btn_row.addWidget(self.reveal_btn)

        self.ok_btn = QPushButton(TestResultDialog)
        self.ok_btn.setObjectName(u"ok_btn")

        self.btn_row.addWidget(self.ok_btn)


        self.verticalLayout.addLayout(self.btn_row)


        self.retranslateUi(TestResultDialog)

        QMetaObject.connectSlotsByName(TestResultDialog)
    # setupUi

    def retranslateUi(self, TestResultDialog):
        TestResultDialog.setWindowTitle(QCoreApplication.translate("TestResultDialog", u"\u6d4b\u8bd5\u7ed3\u679c\u5206\u6790", None))
        self.total_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6d4b\u8bd5\u5f20\u6570:", None))
        self.total_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.recall_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u68c0\u51fa\u7387:", None))
        self.recall_value.setText(QCoreApplication.translate("TestResultDialog", u"0%", None))
        self.precision_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u51c6\u786e\u7387:", None))
        self.precision_value.setText(QCoreApplication.translate("TestResultDialog", u"0%", None))
        self.tp_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6b63\u786e\u68c0\u51fa:", None))
        self.tp_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.fn_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6f0f\u68c0:", None))
        self.fn_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.fp_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u8bef\u68c0:", None))
        self.fp_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
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
        self.reveal_btn.setText(QCoreApplication.translate("TestResultDialog", u"\u6253\u5f00\u6240\u5728\u6587\u4ef6\u5939", None))
        self.ok_btn.setText(QCoreApplication.translate("TestResultDialog", u"\u786e\u5b9a", None))
    # retranslateUi

