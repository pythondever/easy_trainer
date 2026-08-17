# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        if not LogDialog.objectName():
            LogDialog.setObjectName(u"LogDialog")
        LogDialog.resize(903, 600)
        self.gridLayout = QGridLayout(LogDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.clr_log_btn = QPushButton(LogDialog)
        self.clr_log_btn.setObjectName(u"clr_log_btn")

        self.horizontalLayout_2.addWidget(self.clr_log_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.scrollArea = QScrollArea(LogDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 881, 547))
        self.horizontalLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.textEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setObjectName(u"textEdit")

        self.horizontalLayout.addWidget(self.textEdit)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(LogDialog)

        QMetaObject.connectSlotsByName(LogDialog)
    # setupUi

    def retranslateUi(self, LogDialog):
        LogDialog.setWindowTitle(QCoreApplication.translate("LogDialog", u"Dialog", None))
        self.clr_log_btn.setText(QCoreApplication.translate("LogDialog", u"\u6e05\u7a7a", None))
    # retranslateUi

