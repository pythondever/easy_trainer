# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'model.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QDialog, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_ModelDialog(object):
    def setupUi(self, ModelDialog):
        if not ModelDialog.objectName():
            ModelDialog.setObjectName(u"ModelDialog")
        ModelDialog.resize(1200, 700)
        self.verticalLayout = QVBoxLayout(ModelDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.filterLayout = QHBoxLayout()
        self.filterLayout.setObjectName(u"filterLayout")
        self.search_edit = QLineEdit(ModelDialog)
        self.search_edit.setObjectName(u"search_edit")
        self.search_edit.setMinimumSize(QSize(200, 0))

        self.filterLayout.addWidget(self.search_edit)

        self.task_combo = QComboBox(ModelDialog)
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.setObjectName(u"task_combo")
        self.task_combo.setMinimumWidth(96)

        self.filterLayout.addWidget(self.task_combo)

        self.status_combo = QComboBox(ModelDialog)
        self.status_combo.addItem("")
        self.status_combo.addItem("")
        self.status_combo.addItem("")
        self.status_combo.addItem("")
        self.status_combo.addItem("")
        self.status_combo.setObjectName(u"status_combo")
        self.status_combo.setMinimumWidth(96)

        self.filterLayout.addWidget(self.status_combo)

        self.best_only_check = QCheckBox(ModelDialog)
        self.best_only_check.setObjectName(u"best_only_check")

        self.filterLayout.addWidget(self.best_only_check)

        self.filterSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filterLayout.addItem(self.filterSpacer)

        self.count_label = QLabel(ModelDialog)
        self.count_label.setObjectName(u"count_label")

        self.filterLayout.addWidget(self.count_label)


        self.verticalLayout.addLayout(self.filterLayout)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setObjectName(u"contentLayout")
        self.tableWidget = QTableWidget(ModelDialog)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(7)

        self.contentLayout.addWidget(self.tableWidget)

        self.detail_panel = QWidget(ModelDialog)
        self.detail_panel.setObjectName(u"detail_panel")
        self.detail_panel.setMinimumWidth(250)
        self.detail_panel.setMaximumWidth(280)
        self.detail_layout = QVBoxLayout(self.detail_panel)
        self.detail_layout.setObjectName(u"detail_layout")
        self.detail_title = QLabel(self.detail_panel)
        self.detail_title.setObjectName(u"detail_title")

        self.detail_layout.addWidget(self.detail_title)

        self.detail_info = QLabel(self.detail_panel)
        self.detail_info.setObjectName(u"detail_info")
        self.detail_info.setWordWrap(True)
        self.detail_info.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.detail_layout.addWidget(self.detail_info)

        self.detail_curve = QLabel(self.detail_panel)
        self.detail_curve.setObjectName(u"detail_curve")
        self.detail_curve.setMinimumSize(QSize(0, 110))
        self.detail_curve.setAlignment(Qt.AlignCenter)

        self.detail_layout.addWidget(self.detail_curve)

        self.detail_metrics_btn = QPushButton(self.detail_panel)
        self.detail_metrics_btn.setObjectName(u"detail_metrics_btn")

        self.detail_layout.addWidget(self.detail_metrics_btn)

        self.detail_test_btn = QPushButton(self.detail_panel)
        self.detail_test_btn.setObjectName(u"detail_test_btn")

        self.detail_layout.addWidget(self.detail_test_btn)

        self.detail_retrain_btn = QPushButton(self.detail_panel)
        self.detail_retrain_btn.setObjectName(u"detail_retrain_btn")

        self.detail_layout.addWidget(self.detail_retrain_btn)

        self.detail_open_dir_btn = QPushButton(self.detail_panel)
        self.detail_open_dir_btn.setObjectName(u"detail_open_dir_btn")

        self.detail_layout.addWidget(self.detail_open_dir_btn)

        self.detailSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.detail_layout.addItem(self.detailSpacer)


        self.contentLayout.addWidget(self.detail_panel)


        self.verticalLayout.addLayout(self.contentLayout)

        self.pagerLayout = QHBoxLayout()
        self.pagerLayout.setObjectName(u"pagerLayout")
        self.horizontalSpacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pagerLayout.addItem(self.horizontalSpacer_left)

        self.pre_page_btn = QPushButton(ModelDialog)
        self.pre_page_btn.setObjectName(u"pre_page_btn")

        self.pagerLayout.addWidget(self.pre_page_btn)

        self.page_label = QLabel(ModelDialog)
        self.page_label.setObjectName(u"page_label")

        self.pagerLayout.addWidget(self.page_label)

        self.next_page_btn = QPushButton(ModelDialog)
        self.next_page_btn.setObjectName(u"next_page_btn")

        self.pagerLayout.addWidget(self.next_page_btn)

        self.horizontalSpacer_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pagerLayout.addItem(self.horizontalSpacer_right)


        self.verticalLayout.addLayout(self.pagerLayout)


        self.retranslateUi(ModelDialog)

        QMetaObject.connectSlotsByName(ModelDialog)
    # setupUi

    def retranslateUi(self, ModelDialog):
        ModelDialog.setWindowTitle(QCoreApplication.translate("ModelDialog", u"\u6a21\u578b\u7ba1\u7406", None))
        self.search_edit.setPlaceholderText(QCoreApplication.translate("ModelDialog", u"\u641c\u7d22\u9879\u76ee / \u6570\u636e\u96c6 / \u6807\u7b7e", None))
        self.task_combo.setItemText(0, QCoreApplication.translate("ModelDialog", u"\u5168\u90e8\u4efb\u52a1", None))
        self.task_combo.setItemText(1, QCoreApplication.translate("ModelDialog", u"\u68c0\u6d4b", None))
        self.task_combo.setItemText(2, QCoreApplication.translate("ModelDialog", u"\u5206\u5272", None))
        self.task_combo.setItemText(3, QCoreApplication.translate("ModelDialog", u"\u5206\u7c7b", None))

        self.status_combo.setItemText(0, QCoreApplication.translate("ModelDialog", u"\u5168\u90e8\u72b6\u6001", None))
        self.status_combo.setItemText(1, QCoreApplication.translate("ModelDialog", u"\u5df2\u5b8c\u6210", None))
        self.status_combo.setItemText(2, QCoreApplication.translate("ModelDialog", u"\u8bad\u7ec3\u4e2d", None))
        self.status_combo.setItemText(3, QCoreApplication.translate("ModelDialog", u"\u5931\u8d25", None))
        self.status_combo.setItemText(4, QCoreApplication.translate("ModelDialog", u"\u5df2\u505c\u6b62", None))

        self.best_only_check.setText(QCoreApplication.translate("ModelDialog", u"\u4ec5\u770b\u6bcf\u4e2a\u6570\u636e\u96c6\u6700\u4f73", None))
        self.count_label.setText(QCoreApplication.translate("ModelDialog", u"\u5171 0 \u6761", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ModelDialog", u"\u4efb\u52a1", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ModelDialog", u"\u6570\u636e\u96c6 / \u6807\u7b7e", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ModelDialog", u"\u7cbe\u5ea6", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ModelDialog", u"\u8bad\u7ec3\u65f6\u95f4", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ModelDialog", u"\u8017\u65f6", None))
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ModelDialog", u"\u56fe\u50cf\u5c3a\u5bf8", None))
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("ModelDialog", u"\u64cd\u4f5c", None))
        self.detail_title.setText(QCoreApplication.translate("ModelDialog", u"\u6a21\u578b\u8be6\u60c5", None))
        self.detail_info.setText(QCoreApplication.translate("ModelDialog", u"\u9009\u4e2d\u4e00\u884c\u67e5\u770b\u8be6\u60c5", None))
        self.detail_metrics_btn.setText(QCoreApplication.translate("ModelDialog", u"\u67e5\u770b\u5b8c\u6574\u6307\u6807", None))
        self.detail_test_btn.setText(QCoreApplication.translate("ModelDialog", u"\u6d4b\u8bd5\u6b64\u6a21\u578b", None))
        self.detail_retrain_btn.setText(QCoreApplication.translate("ModelDialog", u"\u6309\u6b64\u914d\u7f6e\u91cd\u8bad", None))
        self.detail_open_dir_btn.setText(QCoreApplication.translate("ModelDialog", u"\u6253\u5f00\u6a21\u578b\u76ee\u5f55", None))
        self.pre_page_btn.setText(QCoreApplication.translate("ModelDialog", u"\u4e0a\u4e00\u9875", None))
        self.page_label.setText(QCoreApplication.translate("ModelDialog", u"1/1", None))
        self.next_page_btn.setText(QCoreApplication.translate("ModelDialog", u"\u4e0b\u4e00\u9875", None))
    # retranslateUi

