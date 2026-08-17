# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_data.ui'
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
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(824, 496)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.export_path_txt = QLineEdit(Dialog)
        self.export_path_txt.setObjectName(u"export_path_txt")
        self.export_path_txt.setMinimumSize(QSize(300, 40))

        self.horizontalLayout_2.addWidget(self.export_path_txt)

        self.select_path_btn = QPushButton(Dialog)
        self.select_path_btn.setObjectName(u"select_path_btn")
        icon = QIcon()
        icon.addFile(u"../resources/\u6587\u4ef6\u5939.png", QSize(), QIcon.Normal, QIcon.Off)
        self.select_path_btn.setIcon(icon)
        self.select_path_btn.setIconSize(QSize(35, 35))

        self.horizontalLayout_2.addWidget(self.select_path_btn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.exp_label = QLabel(Dialog)
        self.exp_label.setObjectName(u"exp_label")

        self.horizontalLayout.addWidget(self.exp_label)

        self.exp_labelme_fmt = QRadioButton(Dialog)
        self.exp_labelme_fmt.setObjectName(u"exp_labelme_fmt")

        self.horizontalLayout.addWidget(self.exp_labelme_fmt)

        self.exp_yolo_fmt = QRadioButton(Dialog)
        self.exp_yolo_fmt.setObjectName(u"exp_yolo_fmt")

        self.horizontalLayout.addWidget(self.exp_yolo_fmt)

        self.do_export_btn = QPushButton(Dialog)
        self.do_export_btn.setObjectName(u"do_export_btn")
        self.do_export_btn.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.do_export_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.export_path_txt.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u5bfc\u51fa\u8def\u5f84", None))
        self.select_path_btn.setText("")
        self.exp_label.setText(QCoreApplication.translate("Dialog", u"\u5bfc\u51fa\u683c\u5f0f", None))
        self.exp_labelme_fmt.setText(QCoreApplication.translate("Dialog", u"labelme \u683c\u5f0f", None))
        self.exp_yolo_fmt.setText(QCoreApplication.translate("Dialog", u"yolo \u683c\u5f0f", None))
        self.do_export_btn.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u5bfc\u51fa", None))
    # retranslateUi

