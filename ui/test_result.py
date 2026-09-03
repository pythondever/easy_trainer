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
        TestResultDialog.resize(760, 600)
        self.mainLayout = QVBoxLayout(TestResultDialog)
        self.mainLayout.setSpacing(12)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(22, 18, 22, 16)
        self.section_img = QWidget(TestResultDialog)
        self.section_img.setObjectName(u"section_img")
        self.section_img_layout = QVBoxLayout(self.section_img)
        self.section_img_layout.setSpacing(6)
        self.section_img_layout.setObjectName(u"section_img_layout")
        self.section_img_layout.setContentsMargins(0, 0, 0, 0)
        self.dim_img_row = QHBoxLayout()
        self.dim_img_row.setSpacing(8)
        self.dim_img_row.setObjectName(u"dim_img_row")
        self.dim_img_tag = QLabel(self.section_img)
        self.dim_img_tag.setObjectName(u"dim_img_tag")

        self.dim_img_row.addWidget(self.dim_img_tag)

        self.dim_img_note = QLabel(self.section_img)
        self.dim_img_note.setObjectName(u"dim_img_note")

        self.dim_img_row.addWidget(self.dim_img_note)

        self.dim_img_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.dim_img_row.addItem(self.dim_img_spacer)


        self.section_img_layout.addLayout(self.dim_img_row)

        self.metricRowImg = QHBoxLayout()
        self.metricRowImg.setSpacing(10)
        self.metricRowImg.setObjectName(u"metricRowImg")
        self.card_img_total = QFrame(self.section_img)
        self.card_img_total.setObjectName(u"card_img_total")
        self.card_img_total.setFrameShape(QFrame.NoFrame)
        self.card_img_total.setMinimumSize(QSize(0, 92))
        self.card_img_total_layout = QVBoxLayout(self.card_img_total)
        self.card_img_total_layout.setSpacing(4)
        self.card_img_total_layout.setObjectName(u"card_img_total_layout")
        self.card_img_total_layout.setContentsMargins(12, 12, 12, 12)
        self.img_total_top_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_img_total_layout.addItem(self.img_total_top_spacer)

        self.img_total_value = QLabel(self.card_img_total)
        self.img_total_value.setObjectName(u"img_total_value")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_total_value.sizePolicy().hasHeightForWidth())
        self.img_total_value.setSizePolicy(sizePolicy)
        self.img_total_value.setAlignment(Qt.AlignCenter)

        self.card_img_total_layout.addWidget(self.img_total_value)

        self.img_total_lbl = QLabel(self.card_img_total)
        self.img_total_lbl.setObjectName(u"img_total_lbl")
        sizePolicy.setHeightForWidth(self.img_total_lbl.sizePolicy().hasHeightForWidth())
        self.img_total_lbl.setSizePolicy(sizePolicy)
        self.img_total_lbl.setAlignment(Qt.AlignCenter)

        self.card_img_total_layout.addWidget(self.img_total_lbl)

        self.img_total_rate = QLabel(self.card_img_total)
        self.img_total_rate.setObjectName(u"img_total_rate")
        sizePolicy.setHeightForWidth(self.img_total_rate.sizePolicy().hasHeightForWidth())
        self.img_total_rate.setSizePolicy(sizePolicy)
        self.img_total_rate.setAlignment(Qt.AlignCenter)

        self.card_img_total_layout.addWidget(self.img_total_rate)

        self.img_total_bottom_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_img_total_layout.addItem(self.img_total_bottom_spacer)


        self.metricRowImg.addWidget(self.card_img_total)

        self.card_img_ok = QFrame(self.section_img)
        self.card_img_ok.setObjectName(u"card_img_ok")
        self.card_img_ok.setFrameShape(QFrame.NoFrame)
        self.card_img_ok.setMinimumSize(QSize(0, 92))
        self.card_img_ok_layout = QVBoxLayout(self.card_img_ok)
        self.card_img_ok_layout.setSpacing(4)
        self.card_img_ok_layout.setObjectName(u"card_img_ok_layout")
        self.card_img_ok_layout.setContentsMargins(12, 12, 12, 12)
        self.img_ok_top_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_img_ok_layout.addItem(self.img_ok_top_spacer)

        self.img_ok_value = QLabel(self.card_img_ok)
        self.img_ok_value.setObjectName(u"img_ok_value")
        sizePolicy.setHeightForWidth(self.img_ok_value.sizePolicy().hasHeightForWidth())
        self.img_ok_value.setSizePolicy(sizePolicy)
        self.img_ok_value.setAlignment(Qt.AlignCenter)

        self.card_img_ok_layout.addWidget(self.img_ok_value)

        self.img_ok_lbl = QLabel(self.card_img_ok)
        self.img_ok_lbl.setObjectName(u"img_ok_lbl")
        sizePolicy.setHeightForWidth(self.img_ok_lbl.sizePolicy().hasHeightForWidth())
        self.img_ok_lbl.setSizePolicy(sizePolicy)
        self.img_ok_lbl.setAlignment(Qt.AlignCenter)

        self.card_img_ok_layout.addWidget(self.img_ok_lbl)

        self.img_ok_rate = QLabel(self.card_img_ok)
        self.img_ok_rate.setObjectName(u"img_ok_rate")
        sizePolicy.setHeightForWidth(self.img_ok_rate.sizePolicy().hasHeightForWidth())
        self.img_ok_rate.setSizePolicy(sizePolicy)
        self.img_ok_rate.setAlignment(Qt.AlignCenter)

        self.card_img_ok_layout.addWidget(self.img_ok_rate)

        self.img_ok_bottom_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_img_ok_layout.addItem(self.img_ok_bottom_spacer)


        self.metricRowImg.addWidget(self.card_img_ok)

        self.card_img_fn = QFrame(self.section_img)
        self.card_img_fn.setObjectName(u"card_img_fn")
        self.card_img_fn.setFrameShape(QFrame.NoFrame)
        self.card_img_fn.setMinimumSize(QSize(0, 92))
        self.card_img_fn_layout = QVBoxLayout(self.card_img_fn)
        self.card_img_fn_layout.setSpacing(4)
        self.card_img_fn_layout.setObjectName(u"card_img_fn_layout")
        self.card_img_fn_layout.setContentsMargins(12, 12, 12, 12)
        self.img_fn_top_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_img_fn_layout.addItem(self.img_fn_top_spacer)

        self.img_fn_value = QLabel(self.card_img_fn)
        self.img_fn_value.setObjectName(u"img_fn_value")
        sizePolicy.setHeightForWidth(self.img_fn_value.sizePolicy().hasHeightForWidth())
        self.img_fn_value.setSizePolicy(sizePolicy)
        self.img_fn_value.setAlignment(Qt.AlignCenter)

        self.card_img_fn_layout.addWidget(self.img_fn_value)

        self.img_fn_lbl = QLabel(self.card_img_fn)
        self.img_fn_lbl.setObjectName(u"img_fn_lbl")
        sizePolicy.setHeightForWidth(self.img_fn_lbl.sizePolicy().hasHeightForWidth())
        self.img_fn_lbl.setSizePolicy(sizePolicy)
        self.img_fn_lbl.setAlignment(Qt.AlignCenter)

        self.card_img_fn_layout.addWidget(self.img_fn_lbl)

        self.img_fn_rate = QLabel(self.card_img_fn)
        self.img_fn_rate.setObjectName(u"img_fn_rate")
        sizePolicy.setHeightForWidth(self.img_fn_rate.sizePolicy().hasHeightForWidth())
        self.img_fn_rate.setSizePolicy(sizePolicy)
        self.img_fn_rate.setAlignment(Qt.AlignCenter)

        self.card_img_fn_layout.addWidget(self.img_fn_rate)

        self.img_fn_bottom_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_img_fn_layout.addItem(self.img_fn_bottom_spacer)


        self.metricRowImg.addWidget(self.card_img_fn)

        self.card_img_fp = QFrame(self.section_img)
        self.card_img_fp.setObjectName(u"card_img_fp")
        self.card_img_fp.setFrameShape(QFrame.NoFrame)
        self.card_img_fp.setMinimumSize(QSize(0, 92))
        self.card_img_fp_layout = QVBoxLayout(self.card_img_fp)
        self.card_img_fp_layout.setSpacing(4)
        self.card_img_fp_layout.setObjectName(u"card_img_fp_layout")
        self.card_img_fp_layout.setContentsMargins(12, 12, 12, 12)
        self.img_fp_top_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_img_fp_layout.addItem(self.img_fp_top_spacer)

        self.img_fp_value = QLabel(self.card_img_fp)
        self.img_fp_value.setObjectName(u"img_fp_value")
        sizePolicy.setHeightForWidth(self.img_fp_value.sizePolicy().hasHeightForWidth())
        self.img_fp_value.setSizePolicy(sizePolicy)
        self.img_fp_value.setAlignment(Qt.AlignCenter)

        self.card_img_fp_layout.addWidget(self.img_fp_value)

        self.img_fp_lbl = QLabel(self.card_img_fp)
        self.img_fp_lbl.setObjectName(u"img_fp_lbl")
        sizePolicy.setHeightForWidth(self.img_fp_lbl.sizePolicy().hasHeightForWidth())
        self.img_fp_lbl.setSizePolicy(sizePolicy)
        self.img_fp_lbl.setAlignment(Qt.AlignCenter)

        self.card_img_fp_layout.addWidget(self.img_fp_lbl)

        self.img_fp_rate = QLabel(self.card_img_fp)
        self.img_fp_rate.setObjectName(u"img_fp_rate")
        sizePolicy.setHeightForWidth(self.img_fp_rate.sizePolicy().hasHeightForWidth())
        self.img_fp_rate.setSizePolicy(sizePolicy)
        self.img_fp_rate.setAlignment(Qt.AlignCenter)

        self.card_img_fp_layout.addWidget(self.img_fp_rate)

        self.img_fp_bottom_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_img_fp_layout.addItem(self.img_fp_bottom_spacer)


        self.metricRowImg.addWidget(self.card_img_fp)

        self.metricRowImg.setStretch(0, 1)
        self.metricRowImg.setStretch(1, 1)
        self.metricRowImg.setStretch(2, 1)
        self.metricRowImg.setStretch(3, 1)

        self.section_img_layout.addLayout(self.metricRowImg)


        self.mainLayout.addWidget(self.section_img)

        self.section_lbl = QWidget(TestResultDialog)
        self.section_lbl.setObjectName(u"section_lbl")
        self.section_lbl_layout = QVBoxLayout(self.section_lbl)
        self.section_lbl_layout.setSpacing(6)
        self.section_lbl_layout.setObjectName(u"section_lbl_layout")
        self.section_lbl_layout.setContentsMargins(0, 0, 0, 0)
        self.dim_lbl_row = QHBoxLayout()
        self.dim_lbl_row.setSpacing(8)
        self.dim_lbl_row.setObjectName(u"dim_lbl_row")
        self.dim_lbl_tag = QLabel(self.section_lbl)
        self.dim_lbl_tag.setObjectName(u"dim_lbl_tag")

        self.dim_lbl_row.addWidget(self.dim_lbl_tag)

        self.dim_lbl_note = QLabel(self.section_lbl)
        self.dim_lbl_note.setObjectName(u"dim_lbl_note")

        self.dim_lbl_row.addWidget(self.dim_lbl_note)

        self.dim_lbl_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.dim_lbl_row.addItem(self.dim_lbl_spacer)


        self.section_lbl_layout.addLayout(self.dim_lbl_row)

        self.metricRowLbl = QHBoxLayout()
        self.metricRowLbl.setSpacing(10)
        self.metricRowLbl.setObjectName(u"metricRowLbl")
        self.card_tp = QFrame(self.section_lbl)
        self.card_tp.setObjectName(u"card_tp")
        self.card_tp.setFrameShape(QFrame.NoFrame)
        self.card_tp.setMinimumSize(QSize(0, 92))
        self.card_tp_layout = QVBoxLayout(self.card_tp)
        self.card_tp_layout.setSpacing(4)
        self.card_tp_layout.setObjectName(u"card_tp_layout")
        self.card_tp_layout.setContentsMargins(12, 12, 12, 12)
        self.tp_top_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_tp_layout.addItem(self.tp_top_spacer)

        self.tp_value = QLabel(self.card_tp)
        self.tp_value.setObjectName(u"tp_value")
        sizePolicy.setHeightForWidth(self.tp_value.sizePolicy().hasHeightForWidth())
        self.tp_value.setSizePolicy(sizePolicy)
        self.tp_value.setAlignment(Qt.AlignCenter)

        self.card_tp_layout.addWidget(self.tp_value)

        self.tp_lbl = QLabel(self.card_tp)
        self.tp_lbl.setObjectName(u"tp_lbl")
        sizePolicy.setHeightForWidth(self.tp_lbl.sizePolicy().hasHeightForWidth())
        self.tp_lbl.setSizePolicy(sizePolicy)
        self.tp_lbl.setAlignment(Qt.AlignCenter)

        self.card_tp_layout.addWidget(self.tp_lbl)

        self.tp_rate = QLabel(self.card_tp)
        self.tp_rate.setObjectName(u"tp_rate")
        sizePolicy.setHeightForWidth(self.tp_rate.sizePolicy().hasHeightForWidth())
        self.tp_rate.setSizePolicy(sizePolicy)
        self.tp_rate.setAlignment(Qt.AlignCenter)

        self.card_tp_layout.addWidget(self.tp_rate)

        self.tp_bottom_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_tp_layout.addItem(self.tp_bottom_spacer)


        self.metricRowLbl.addWidget(self.card_tp)

        self.card_fn = QFrame(self.section_lbl)
        self.card_fn.setObjectName(u"card_fn")
        self.card_fn.setFrameShape(QFrame.NoFrame)
        self.card_fn.setMinimumSize(QSize(0, 92))
        self.card_fn_layout = QVBoxLayout(self.card_fn)
        self.card_fn_layout.setSpacing(4)
        self.card_fn_layout.setObjectName(u"card_fn_layout")
        self.card_fn_layout.setContentsMargins(12, 12, 12, 12)
        self.fn_top_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_fn_layout.addItem(self.fn_top_spacer)

        self.fn_value = QLabel(self.card_fn)
        self.fn_value.setObjectName(u"fn_value")
        sizePolicy.setHeightForWidth(self.fn_value.sizePolicy().hasHeightForWidth())
        self.fn_value.setSizePolicy(sizePolicy)
        self.fn_value.setAlignment(Qt.AlignCenter)

        self.card_fn_layout.addWidget(self.fn_value)

        self.fn_lbl = QLabel(self.card_fn)
        self.fn_lbl.setObjectName(u"fn_lbl")
        sizePolicy.setHeightForWidth(self.fn_lbl.sizePolicy().hasHeightForWidth())
        self.fn_lbl.setSizePolicy(sizePolicy)
        self.fn_lbl.setAlignment(Qt.AlignCenter)

        self.card_fn_layout.addWidget(self.fn_lbl)

        self.fn_rate = QLabel(self.card_fn)
        self.fn_rate.setObjectName(u"fn_rate")
        sizePolicy.setHeightForWidth(self.fn_rate.sizePolicy().hasHeightForWidth())
        self.fn_rate.setSizePolicy(sizePolicy)
        self.fn_rate.setAlignment(Qt.AlignCenter)

        self.card_fn_layout.addWidget(self.fn_rate)

        self.fn_bottom_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_fn_layout.addItem(self.fn_bottom_spacer)


        self.metricRowLbl.addWidget(self.card_fn)

        self.card_fp = QFrame(self.section_lbl)
        self.card_fp.setObjectName(u"card_fp")
        self.card_fp.setFrameShape(QFrame.NoFrame)
        self.card_fp.setMinimumSize(QSize(0, 92))
        self.card_fp_layout = QVBoxLayout(self.card_fp)
        self.card_fp_layout.setSpacing(4)
        self.card_fp_layout.setObjectName(u"card_fp_layout")
        self.card_fp_layout.setContentsMargins(12, 12, 12, 12)
        self.fp_top_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_fp_layout.addItem(self.fp_top_spacer)

        self.fp_value = QLabel(self.card_fp)
        self.fp_value.setObjectName(u"fp_value")
        sizePolicy.setHeightForWidth(self.fp_value.sizePolicy().hasHeightForWidth())
        self.fp_value.setSizePolicy(sizePolicy)
        self.fp_value.setAlignment(Qt.AlignCenter)

        self.card_fp_layout.addWidget(self.fp_value)

        self.fp_lbl = QLabel(self.card_fp)
        self.fp_lbl.setObjectName(u"fp_lbl")
        sizePolicy.setHeightForWidth(self.fp_lbl.sizePolicy().hasHeightForWidth())
        self.fp_lbl.setSizePolicy(sizePolicy)
        self.fp_lbl.setAlignment(Qt.AlignCenter)

        self.card_fp_layout.addWidget(self.fp_lbl)

        self.fp_rate = QLabel(self.card_fp)
        self.fp_rate.setObjectName(u"fp_rate")
        sizePolicy.setHeightForWidth(self.fp_rate.sizePolicy().hasHeightForWidth())
        self.fp_rate.setSizePolicy(sizePolicy)
        self.fp_rate.setAlignment(Qt.AlignCenter)

        self.card_fp_layout.addWidget(self.fp_rate)

        self.fp_bottom_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_fp_layout.addItem(self.fp_bottom_spacer)


        self.metricRowLbl.addWidget(self.card_fp)

        self.card_precision = QFrame(self.section_lbl)
        self.card_precision.setObjectName(u"card_precision")
        self.card_precision.setFrameShape(QFrame.NoFrame)
        self.card_precision.setMinimumSize(QSize(0, 92))
        self.card_precision_layout = QVBoxLayout(self.card_precision)
        self.card_precision_layout.setSpacing(4)
        self.card_precision_layout.setObjectName(u"card_precision_layout")
        self.card_precision_layout.setContentsMargins(12, 12, 12, 12)
        self.precision_top_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_precision_layout.addItem(self.precision_top_spacer)

        self.precision_value = QLabel(self.card_precision)
        self.precision_value.setObjectName(u"precision_value")
        sizePolicy.setHeightForWidth(self.precision_value.sizePolicy().hasHeightForWidth())
        self.precision_value.setSizePolicy(sizePolicy)
        self.precision_value.setAlignment(Qt.AlignCenter)

        self.card_precision_layout.addWidget(self.precision_value)

        self.precision_lbl = QLabel(self.card_precision)
        self.precision_lbl.setObjectName(u"precision_lbl")
        sizePolicy.setHeightForWidth(self.precision_lbl.sizePolicy().hasHeightForWidth())
        self.precision_lbl.setSizePolicy(sizePolicy)
        self.precision_lbl.setAlignment(Qt.AlignCenter)

        self.card_precision_layout.addWidget(self.precision_lbl)

        self.precision_rate = QLabel(self.card_precision)
        self.precision_rate.setObjectName(u"precision_rate")
        sizePolicy.setHeightForWidth(self.precision_rate.sizePolicy().hasHeightForWidth())
        self.precision_rate.setSizePolicy(sizePolicy)
        self.precision_rate.setAlignment(Qt.AlignCenter)

        self.card_precision_layout.addWidget(self.precision_rate)

        self.precision_bottom_spacer = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.card_precision_layout.addItem(self.precision_bottom_spacer)


        self.metricRowLbl.addWidget(self.card_precision)

        self.metricRowLbl.setStretch(0, 1)
        self.metricRowLbl.setStretch(1, 1)
        self.metricRowLbl.setStretch(2, 1)
        self.metricRowLbl.setStretch(3, 1)

        self.section_lbl_layout.addLayout(self.metricRowLbl)


        self.mainLayout.addWidget(self.section_lbl)

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
        self.dim_img_tag.setText(QCoreApplication.translate("TestResultDialog", u"\u56fe\u50cf\u7ef4\u5ea6", None))
        self.dim_img_tag.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"dimTag", None))
        self.dim_img_note.setText(QCoreApplication.translate("TestResultDialog", u"\u6309\u300c\u5f20\u300d\u7edf\u8ba1", None))
        self.dim_img_note.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"dimNote", None))
        self.img_total_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.img_total_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.img_total_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6d4b\u8bd5\u5f20\u6570", None))
        self.img_total_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.img_total_rate.setText("")
        self.img_total_rate.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardRate", None))
        self.img_ok_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.img_ok_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.img_ok_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u5168\u5bf9\u56fe\u50cf", None))
        self.img_ok_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.img_ok_rate.setText("")
        self.img_ok_rate.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardRate", None))
        self.img_fn_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.img_fn_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.img_fn_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6709\u6f0f\u68c0\u56fe\u50cf", None))
        self.img_fn_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.img_fn_rate.setText("")
        self.img_fn_rate.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardRate", None))
        self.img_fp_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.img_fp_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.img_fp_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6709\u8bef\u68c0\u56fe\u50cf", None))
        self.img_fp_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.img_fp_rate.setText("")
        self.img_fp_rate.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardRate", None))
        self.dim_lbl_tag.setText(QCoreApplication.translate("TestResultDialog", u"\u6807\u7b7e\u7ef4\u5ea6", None))
        self.dim_lbl_tag.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"dimTag", None))
        self.dim_lbl_note.setText(QCoreApplication.translate("TestResultDialog", u"\u6309\u300c\u6807\u6ce8\u6846\u300d\u7edf\u8ba1", None))
        self.dim_lbl_note.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"dimNote", None))
        self.tp_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.tp_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.tp_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6b63\u786e\u68c0\u51fa", None))
        self.tp_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.tp_rate.setText("")
        self.tp_rate.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardRate", None))
        self.fn_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.fn_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.fn_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u6f0f\u68c0", None))
        self.fn_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.fn_rate.setText("")
        self.fn_rate.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardRate", None))
        self.fp_value.setText(QCoreApplication.translate("TestResultDialog", u"0", None))
        self.fp_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.fp_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u8bef\u68c0", None))
        self.fp_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.fp_rate.setText("")
        self.fp_rate.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardRate", None))
        self.precision_value.setText(QCoreApplication.translate("TestResultDialog", u"0%", None))
        self.precision_value.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardValue", None))
        self.precision_lbl.setText(QCoreApplication.translate("TestResultDialog", u"\u51c6\u786e\u7387", None))
        self.precision_lbl.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardLabel", None))
        self.precision_rate.setText("")
        self.precision_rate.setProperty(u"class", QCoreApplication.translate("TestResultDialog", u"cardRate", None))
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

