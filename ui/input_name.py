# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_name.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_NameInputDialog(object):
    def setupUi(self, NameInputDialog):
        if not NameInputDialog.objectName():
            NameInputDialog.setObjectName(u"NameInputDialog")
        NameInputDialog.resize(360, 170)
        self.mainLayout = QVBoxLayout(NameInputDialog)
        self.mainLayout.setSpacing(12)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 18)
        self.title_row = QHBoxLayout()
        self.title_row.setSpacing(10)
        self.title_row.setObjectName(u"title_row")
        self.title_label = QLabel(NameInputDialog)
        self.title_label.setObjectName(u"title_label")

        self.title_row.addWidget(self.title_label)

        self.title_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.title_row.addItem(self.title_spacer)


        self.mainLayout.addLayout(self.title_row)

        self.name_edit = QLineEdit(NameInputDialog)
        self.name_edit.setObjectName(u"name_edit")

        self.mainLayout.addWidget(self.name_edit)

        self.button_line = QFrame(NameInputDialog)
        self.button_line.setObjectName(u"button_line")
        self.button_line.setFrameShape(QFrame.HLine)
        self.button_line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addWidget(self.button_line)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setSpacing(8)
        self.bottom_row.setObjectName(u"bottom_row")
        self.bottom_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer)

        self.cancel_btn = QPushButton(NameInputDialog)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.bottom_row.addWidget(self.cancel_btn)

        self.ok_btn = QPushButton(NameInputDialog)
        self.ok_btn.setObjectName(u"ok_btn")
        self.ok_btn.setMinimumSize(QSize(90, 36))

        self.bottom_row.addWidget(self.ok_btn)


        self.mainLayout.addLayout(self.bottom_row)


        self.retranslateUi(NameInputDialog)

        QMetaObject.connectSlotsByName(NameInputDialog)
    # setupUi

    def retranslateUi(self, NameInputDialog):
        NameInputDialog.setWindowTitle(QCoreApplication.translate("NameInputDialog", u"\u8f93\u5165\u540d\u79f0", None))
        self.title_label.setText(QCoreApplication.translate("NameInputDialog", u"\u8f93\u5165\u540d\u79f0", None))
        self.title_label.setProperty(u"class", QCoreApplication.translate("NameInputDialog", u"dialogTitle", None))
        self.name_edit.setPlaceholderText(QCoreApplication.translate("NameInputDialog", u"\u8bf7\u8f93\u5165\u540d\u79f0", None))
        self.cancel_btn.setText(QCoreApplication.translate("NameInputDialog", u"\u53d6\u6d88", None))
        self.ok_btn.setText(QCoreApplication.translate("NameInputDialog", u"\u786e\u5b9a", None))
        self.ok_btn.setProperty(u"class", QCoreApplication.translate("NameInputDialog", u"primary", None))
    # retranslateUi

