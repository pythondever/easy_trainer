# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_dataset.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_AddDatasets(object):
    def setupUi(self, AddDatasets):
        if not AddDatasets.objectName():
            AddDatasets.setObjectName(u"AddDatasets")
        AddDatasets.resize(400, 300)
        self.gridLayout = QGridLayout(AddDatasets)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(AddDatasets)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.comboBox = QComboBox(AddDatasets)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.done_btn = QPushButton(AddDatasets)
        self.done_btn.setObjectName(u"done_btn")
        icon = QIcon()
        icon.addFile(u"../resources/\u786e\u5b9a.png", QSize(), QIcon.Normal, QIcon.Off)
        self.done_btn.setIcon(icon)

        self.horizontalLayout.addWidget(self.done_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.retranslateUi(AddDatasets)

        QMetaObject.connectSlotsByName(AddDatasets)
    # setupUi

    def retranslateUi(self, AddDatasets):
        AddDatasets.setWindowTitle(QCoreApplication.translate("AddDatasets", u"Dialog", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("AddDatasets", u"\u6570\u636e\u96c6\u540d\u79f0", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("AddDatasets", u"\u76ee\u6807\u68c0\u6d4b", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("AddDatasets", u"\u56fe\u50cf\u5206\u7c7b", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("AddDatasets", u"\u56fe\u50cf\u5206\u5272", None))

        self.done_btn.setText("")
    # retranslateUi

