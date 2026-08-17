# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataset_properties.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGraphicsView, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(942, 690)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.image_path = QLabel(Dialog)
        self.image_path.setObjectName(u"image_path")

        self.horizontalLayout.addWidget(self.image_path)

        self.image_path_line_txt = QLineEdit(Dialog)
        self.image_path_line_txt.setObjectName(u"image_path_line_txt")
        self.image_path_line_txt.setMinimumSize(QSize(400, 40))

        self.horizontalLayout.addWidget(self.image_path_line_txt)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_path = QLabel(Dialog)
        self.label_path.setObjectName(u"label_path")

        self.horizontalLayout_2.addWidget(self.label_path)

        self.label_path_line_txt = QLineEdit(Dialog)
        self.label_path_line_txt.setObjectName(u"label_path_line_txt")
        self.label_path_line_txt.setMinimumSize(QSize(400, 40))

        self.horizontalLayout_2.addWidget(self.label_path_line_txt)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_stats_view = QGraphicsView(Dialog)
        self.label_stats_view.setObjectName(u"label_stats_view")

        self.horizontalLayout_4.addWidget(self.label_stats_view)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u6570\u636e\u96c6\u5c5e\u6027", None))
        self.image_path.setText(QCoreApplication.translate("Dialog", u"\u56fe\u50cf\u8def\u5f84:", None))
        self.label_path.setText(QCoreApplication.translate("Dialog", u"\u6807\u7b7e\u8def\u5f84:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u6807\u7b7e\u5206\u5e03:", None))
    # retranslateUi

