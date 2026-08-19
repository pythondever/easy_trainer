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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_ModelDialog(object):
    def setupUi(self, ModelDialog):
        if not ModelDialog.objectName():
            ModelDialog.setObjectName(u"ModelDialog")
        ModelDialog.resize(960, 540)
        self.verticalLayout = QVBoxLayout(ModelDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(ModelDialog)
        if (self.tableWidget.columnCount() < 14):
            self.tableWidget.setColumnCount(14)
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
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, __qtablewidgetitem13)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(14)

        self.verticalLayout.addWidget(self.tableWidget)

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
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ModelDialog", u"\u5f00\u59cb\u8bad\u7ec3\u65f6\u95f4", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ModelDialog", u"\u5b8c\u6210\u8bad\u7ec3\u65f6\u95f4", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ModelDialog", u"\u8017\u65f6", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ModelDialog", u"\u6a21\u578b\u5927\u5c0f", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ModelDialog", u"\u6a21\u578b\u7c7b\u578b", None))
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ModelDialog", u"\u6a21\u578b\u7cbe\u5ea6", None))
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("ModelDialog", u"\u56fe\u50cf\u5c3a\u5bf8", None))
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("ModelDialog", u"\u6a21\u578b\u8def\u5f84", None))
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("ModelDialog", u"\u6570\u636e\u96c6\u4fe1\u606f", None))
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("ModelDialog", u"\u5bfc\u51fa\u6a21\u578b", None))
        ___qtablewidgetitem10 = self.tableWidget.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("ModelDialog", u"\u6307\u6807", None))
        ___qtablewidgetitem11 = self.tableWidget.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("ModelDialog", u"\u5220\u9664", None))
        ___qtablewidgetitem12 = self.tableWidget.horizontalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("ModelDialog", u"\u6d4b\u8bd5", None))
        ___qtablewidgetitem13 = self.tableWidget.horizontalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("ModelDialog", u"\u8bad\u7ec3", None))
        self.pre_page_btn.setText(QCoreApplication.translate("ModelDialog", u"\u4e0a\u4e00\u9875", None))
        self.page_label.setText(QCoreApplication.translate("ModelDialog", u"1/1", None))
        self.next_page_btn.setText(QCoreApplication.translate("ModelDialog", u"\u4e0b\u4e00\u9875", None))
    # retranslateUi

