# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'annotation.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGraphicsView, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_annotationDialog(object):
    def setupUi(self, annotationDialog):
        if not annotationDialog.objectName():
            annotationDialog.setObjectName(u"annotationDialog")
        annotationDialog.resize(1068, 703)
        self.gridLayout = QGridLayout(annotationDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.draw_rect_btn = QPushButton(annotationDialog)
        self.draw_rect_btn.setObjectName(u"draw_rect_btn")
        icon = QIcon()
        icon.addFile(u"../resources/\u77e9\u5f62.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.draw_rect_btn.setIcon(icon)

        self.horizontalLayout.addWidget(self.draw_rect_btn)

        self.poly_btn = QPushButton(annotationDialog)
        self.poly_btn.setObjectName(u"poly_btn")
        icon1 = QIcon()
        icon1.addFile(u"../resources/\u591a\u8fb9\u5f62.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.poly_btn.setIcon(icon1)

        self.horizontalLayout.addWidget(self.poly_btn)

        self.format_painter_btn = QPushButton(annotationDialog)
        self.format_painter_btn.setObjectName(u"format_painter_btn")
        icon2 = QIcon()
        icon2.addFile(u"../resources/\u5237\u5b50.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.format_painter_btn.setIcon(icon2)

        self.horizontalLayout.addWidget(self.format_painter_btn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.image_label_show = QGraphicsView(annotationDialog)
        self.image_label_show.setObjectName(u"image_label_show")

        self.horizontalLayout_5.addWidget(self.image_label_show)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_list = QLabel(annotationDialog)
        self.label_list.setObjectName(u"label_list")

        self.horizontalLayout_3.addWidget(self.label_list)

        self.add_label = QPushButton(annotationDialog)
        self.add_label.setObjectName(u"add_label")

        self.horizontalLayout_3.addWidget(self.add_label)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_scrollArea = QScrollArea(annotationDialog)
        self.label_scrollArea.setObjectName(u"label_scrollArea")
        self.label_scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 202, 232))
        self.label_scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.label_scrollArea)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labeled_list = QLabel(annotationDialog)
        self.labeled_list.setObjectName(u"labeled_list")

        self.horizontalLayout_4.addWidget(self.labeled_list)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.label_info_scrollArea = QScrollArea(annotationDialog)
        self.label_info_scrollArea.setObjectName(u"label_info_scrollArea")
        self.label_info_scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 202, 235))
        self.label_info_scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_2.addWidget(self.label_info_scrollArea)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.image_info_label = QLabel(annotationDialog)
        self.image_info_label.setObjectName(u"image_info_label")

        self.verticalLayout_3.addWidget(self.image_info_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_3.addItem(self.horizontalSpacer_2)

        self.lineEdit = QLineEdit(annotationDialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_3.addWidget(self.lineEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)

        self.horizontalLayout_5.setStretch(0, 8)
        self.horizontalLayout_5.setStretch(1, 2)

        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.pre_page_btn = QPushButton(annotationDialog)
        self.pre_page_btn.setObjectName(u"pre_page_btn")

        self.horizontalLayout_2.addWidget(self.pre_page_btn)

        self.next_page_btn = QPushButton(annotationDialog)
        self.next_page_btn.setObjectName(u"next_page_btn")

        self.horizontalLayout_2.addWidget(self.next_page_btn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)


        self.retranslateUi(annotationDialog)

        QMetaObject.connectSlotsByName(annotationDialog)
    # setupUi

    def retranslateUi(self, annotationDialog):
        annotationDialog.setWindowTitle(QCoreApplication.translate("annotationDialog", u"Dialog", None))
        self.draw_rect_btn.setText("")
        self.poly_btn.setText("")
        self.format_painter_btn.setText(QCoreApplication.translate("annotationDialog", u"\u683c\u5f0f\u5237", None))
        self.label_list.setText(QCoreApplication.translate("annotationDialog", u"\u6807\u7b7e\u5217\u8868", None))
        self.add_label.setText(QCoreApplication.translate("annotationDialog", u"\u6dfb\u52a0", None))
        self.labeled_list.setText(QCoreApplication.translate("annotationDialog", u"\u6807\u6ce8\u4fe1\u606f", None))
        self.image_info_label.setText(QCoreApplication.translate("annotationDialog", u"\u56fe\u50cf\u4fe1\u606f", None))
        self.pre_page_btn.setText(QCoreApplication.translate("annotationDialog", u"\u4e0a\u4e00\u5f20(A)", None))
        self.next_page_btn.setText(QCoreApplication.translate("annotationDialog", u"\u4e0b\u4e00\u5f20(D)", None))
    # retranslateUi

