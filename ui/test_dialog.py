# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_TestDialog(object):
    def setupUi(self, TestDialog):
        if not TestDialog.objectName():
            TestDialog.setObjectName(u"TestDialog")
        TestDialog.resize(520, 440)
        self.verticalLayout = QVBoxLayout(TestDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_label = QLabel(TestDialog)
        self.title_label.setObjectName(u"title_label")

        self.verticalLayout.addWidget(self.title_label)

        self.data_row = QHBoxLayout()
        self.data_row.setObjectName(u"data_row")
        self.test_data_label = QLabel(TestDialog)
        self.test_data_label.setObjectName(u"test_data_label")

        self.data_row.addWidget(self.test_data_label)

        self.test_data_combo = QComboBox(TestDialog)
        self.test_data_combo.setObjectName(u"test_data_combo")

        self.data_row.addWidget(self.test_data_combo)


        self.verticalLayout.addLayout(self.data_row)

        self.device_row = QHBoxLayout()
        self.device_row.setObjectName(u"device_row")
        self.test_device_label = QLabel(TestDialog)
        self.test_device_label.setObjectName(u"test_device_label")

        self.device_row.addWidget(self.test_device_label)

        self.test_device_combo = QComboBox(TestDialog)
        self.test_device_combo.setObjectName(u"test_device_combo")

        self.device_row.addWidget(self.test_device_combo)


        self.verticalLayout.addLayout(self.device_row)

        self.model_row = QHBoxLayout()
        self.model_row.setObjectName(u"model_row")
        self.model_label = QLabel(TestDialog)
        self.model_label.setObjectName(u"model_label")

        self.model_row.addWidget(self.model_label)

        self.model_combo = QComboBox(TestDialog)
        self.model_combo.setObjectName(u"model_combo")

        self.model_row.addWidget(self.model_combo)


        self.verticalLayout.addLayout(self.model_row)

        self.confidence_row = QHBoxLayout()
        self.confidence_row.setObjectName(u"confidence_row")
        self.confidence_label = QLabel(TestDialog)
        self.confidence_label.setObjectName(u"confidence_label")

        self.confidence_row.addWidget(self.confidence_label)

        self.confidence_txt = QLineEdit(TestDialog)
        self.confidence_txt.setObjectName(u"confidence_txt")

        self.confidence_row.addWidget(self.confidence_txt)


        self.verticalLayout.addLayout(self.confidence_row)

        self.iou_row = QHBoxLayout()
        self.iou_row.setObjectName(u"iou_row")
        self.iou_treshold_label = QLabel(TestDialog)
        self.iou_treshold_label.setObjectName(u"iou_treshold_label")

        self.iou_row.addWidget(self.iou_treshold_label)

        self.iou_treshold_txt = QLineEdit(TestDialog)
        self.iou_treshold_txt.setObjectName(u"iou_treshold_txt")

        self.iou_row.addWidget(self.iou_treshold_txt)


        self.verticalLayout.addLayout(self.iou_row)

        self.output_row = QHBoxLayout()
        self.output_row.setObjectName(u"output_row")
        self.output_label_file_checkBox = QCheckBox(TestDialog)
        self.output_label_file_checkBox.setObjectName(u"output_label_file_checkBox")

        self.output_row.addWidget(self.output_label_file_checkBox)

        self.output_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.output_row.addItem(self.output_spacer)


        self.verticalLayout.addLayout(self.output_row)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setObjectName(u"bottom_row")
        self.bottom_spacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer_left)

        self.start_test_btn = QPushButton(TestDialog)
        self.start_test_btn.setObjectName(u"start_test_btn")
        self.start_test_btn.setMinimumSize(QSize(120, 36))

        self.bottom_row.addWidget(self.start_test_btn)

        self.bottom_spacer_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer_right)


        self.verticalLayout.addLayout(self.bottom_row)


        self.retranslateUi(TestDialog)

        QMetaObject.connectSlotsByName(TestDialog)
    # setupUi

    def retranslateUi(self, TestDialog):
        TestDialog.setWindowTitle(QCoreApplication.translate("TestDialog", u"\u6a21\u578b\u6d4b\u8bd5", None))
        self.title_label.setText(QCoreApplication.translate("TestDialog", u"\u6d4b\u8bd5\u53c2\u6570\u914d\u7f6e", None))
        self.title_label.setStyleSheet(QCoreApplication.translate("TestDialog", u"color: #e8eaf0; font-size: 16px; font-weight: bold;", None))
        self.test_data_label.setText(QCoreApplication.translate("TestDialog", u"\u6570\u636e:", None))
        self.test_device_label.setText(QCoreApplication.translate("TestDialog", u"\u8bbe\u5907:", None))
        self.model_label.setText(QCoreApplication.translate("TestDialog", u"\u6a21\u578b:", None))
        self.confidence_label.setText(QCoreApplication.translate("TestDialog", u"\u7f6e\u4fe1\u5ea6:", None))
        self.iou_treshold_label.setText(QCoreApplication.translate("TestDialog", u"iou\u9608\u503c:", None))
        self.output_label_file_checkBox.setText(QCoreApplication.translate("TestDialog", u"\u8f93\u51fa\u6807\u7b7e\u6587\u4ef6", None))
        self.start_test_btn.setText(QCoreApplication.translate("TestDialog", u"\u5f00\u59cb\u6d4b\u8bd5", None))
    # retranslateUi

