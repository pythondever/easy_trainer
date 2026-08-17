# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'enter_name.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        icon = QIcon()
        icon.addFile(u"../resources/favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.enter_name_lbl = QLabel(Dialog)
        self.enter_name_lbl.setObjectName(u"enter_name_lbl")

        self.gridLayout.addWidget(self.enter_name_lbl, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.project_name_txt = QLineEdit(Dialog)
        self.project_name_txt.setObjectName(u"project_name_txt")
        self.project_name_txt.setMinimumSize(QSize(200, 40))

        self.horizontalLayout.addWidget(self.project_name_txt)

        self.done_enter_name_btn = QPushButton(Dialog)
        self.done_enter_name_btn.setObjectName(u"done_enter_name_btn")
        self.done_enter_name_btn.setMinimumSize(QSize(60, 40))
        icon1 = QIcon()
        icon1.addFile(u"../resources/\u786e\u5b9a.png", QSize(), QIcon.Normal, QIcon.Off)
        self.done_enter_name_btn.setIcon(icon1)
        self.done_enter_name_btn.setIconSize(QSize(40, 25))

        self.horizontalLayout.addWidget(self.done_enter_name_btn)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u9879\u76ee\u540d\u79f0", None))
        self.enter_name_lbl.setText(QCoreApplication.translate("Dialog", u"\u540d\u79f0\u5df2\u5b58\u5728\uff01", None))
        self.project_name_txt.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u9879\u76ee\u540d\u79f0", None))
        self.done_enter_name_btn.setText("")
    # retranslateUi

