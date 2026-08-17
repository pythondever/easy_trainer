# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_label.ui'
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
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.label_btn = QPushButton(Dialog)
        self.label_btn.setObjectName(u"label_btn")
        self.label_btn.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.label_btn)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.new_label_edit = QLineEdit(Dialog)
        self.new_label_edit.setObjectName(u"new_label_edit")
        self.new_label_edit.setMinimumSize(QSize(0, 40))
        self.new_label_edit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.new_label_edit)

        self.done_btn = QPushButton(Dialog)
        self.done_btn.setObjectName(u"done_btn")
        self.done_btn.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.done_btn)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u7c7b\u522b\u4fee\u6539", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u7c7b\u522b", None))
        self.label_btn.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u6279\u91cf\u4fee\u6539\u4e3a", None))
        self.done_btn.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
    # retranslateUi

