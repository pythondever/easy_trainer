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
    QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_TestDialog(object):
    def setupUi(self, TestDialog):
        if not TestDialog.objectName():
            TestDialog.setObjectName(u"TestDialog")
        TestDialog.resize(460, 420)
        TestDialog.setMinimumSize(QSize(460, 420))
        self.mainLayout = QVBoxLayout(TestDialog)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 20)
        self.title_label = QLabel(TestDialog)
        self.title_label.setObjectName(u"title_label")

        self.mainLayout.addWidget(self.title_label)

        self.group_source_title = QLabel(TestDialog)
        self.group_source_title.setObjectName(u"group_source_title")

        self.mainLayout.addWidget(self.group_source_title)

        self.form_source = QFormLayout()
        self.form_source.setObjectName(u"form_source")
        self.form_source.setHorizontalSpacing(14)
        self.form_source.setVerticalSpacing(12)
        self.form_source.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.test_data_label = QLabel(TestDialog)
        self.test_data_label.setObjectName(u"test_data_label")

        self.form_source.setWidget(0, QFormLayout.ItemRole.LabelRole, self.test_data_label)

        self.test_data_combo = QComboBox(TestDialog)
        self.test_data_combo.setObjectName(u"test_data_combo")
        self.test_data_combo.setMinimumSize(QSize(280, 0))

        self.form_source.setWidget(0, QFormLayout.ItemRole.FieldRole, self.test_data_combo)

        self.test_device_label = QLabel(TestDialog)
        self.test_device_label.setObjectName(u"test_device_label")

        self.form_source.setWidget(1, QFormLayout.ItemRole.LabelRole, self.test_device_label)

        self.test_device_combo = QComboBox(TestDialog)
        self.test_device_combo.setObjectName(u"test_device_combo")
        self.test_device_combo.setMinimumSize(QSize(280, 0))

        self.form_source.setWidget(1, QFormLayout.ItemRole.FieldRole, self.test_device_combo)

        self.model_label = QLabel(TestDialog)
        self.model_label.setObjectName(u"model_label")

        self.form_source.setWidget(2, QFormLayout.ItemRole.LabelRole, self.model_label)

        self.model_combo = QComboBox(TestDialog)
        self.model_combo.setObjectName(u"model_combo")
        self.model_combo.setMinimumSize(QSize(280, 0))

        self.form_source.setWidget(2, QFormLayout.ItemRole.FieldRole, self.model_combo)


        self.mainLayout.addLayout(self.form_source)

        self.group_param_label = QLabel(TestDialog)
        self.group_param_label.setObjectName(u"group_param_label")

        self.mainLayout.addWidget(self.group_param_label)

        self.form_param = QFormLayout()
        self.form_param.setObjectName(u"form_param")
        self.form_param.setHorizontalSpacing(14)
        self.form_param.setVerticalSpacing(12)
        self.form_param.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.confidence_label = QLabel(TestDialog)
        self.confidence_label.setObjectName(u"confidence_label")

        self.form_param.setWidget(0, QFormLayout.ItemRole.LabelRole, self.confidence_label)

        self.confidence_txt = QLineEdit(TestDialog)
        self.confidence_txt.setObjectName(u"confidence_txt")
        self.confidence_txt.setMinimumSize(QSize(280, 0))

        self.form_param.setWidget(0, QFormLayout.ItemRole.FieldRole, self.confidence_txt)

        self.iou_treshold_label = QLabel(TestDialog)
        self.iou_treshold_label.setObjectName(u"iou_treshold_label")

        self.form_param.setWidget(1, QFormLayout.ItemRole.LabelRole, self.iou_treshold_label)

        self.iou_treshold_txt = QLineEdit(TestDialog)
        self.iou_treshold_txt.setObjectName(u"iou_treshold_txt")
        self.iou_treshold_txt.setMinimumSize(QSize(280, 0))

        self.form_param.setWidget(1, QFormLayout.ItemRole.FieldRole, self.iou_treshold_txt)

        self.output_label_label = QLabel(TestDialog)
        self.output_label_label.setObjectName(u"output_label_label")

        self.form_param.setWidget(2, QFormLayout.ItemRole.LabelRole, self.output_label_label)

        self.output_label_file_checkBox = QCheckBox(TestDialog)
        self.output_label_file_checkBox.setObjectName(u"output_label_file_checkBox")

        self.form_param.setWidget(2, QFormLayout.ItemRole.FieldRole, self.output_label_file_checkBox)


        self.mainLayout.addLayout(self.form_param)

        self.bottomSpacerTop = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacerTop)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setObjectName(u"bottom_row")
        self.bottom_spacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer_left)

        self.start_test_btn = QPushButton(TestDialog)
        self.start_test_btn.setObjectName(u"start_test_btn")
        self.start_test_btn.setMinimumSize(QSize(140, 38))

        self.bottom_row.addWidget(self.start_test_btn)

        self.bottom_spacer_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer_right)


        self.mainLayout.addLayout(self.bottom_row)


        self.retranslateUi(TestDialog)

        QMetaObject.connectSlotsByName(TestDialog)
    # setupUi

    def retranslateUi(self, TestDialog):
        TestDialog.setWindowTitle(QCoreApplication.translate("TestDialog", u"\u6a21\u578b\u6d4b\u8bd5", None))
        self.title_label.setText(QCoreApplication.translate("TestDialog", u"\u6d4b\u8bd5\u53c2\u6570\u914d\u7f6e", None))
        self.title_label.setProperty(u"objectName", QCoreApplication.translate("TestDialog", u"dialogTitle", None))
        self.group_source_title.setText(QCoreApplication.translate("TestDialog", u"\u6570\u636e\u4e0e\u6a21\u578b", None))
        self.group_source_title.setProperty(u"objectName", QCoreApplication.translate("TestDialog", u"dialogSectionTitle", None))
        self.test_data_label.setText(QCoreApplication.translate("TestDialog", u"\u6570\u636e", None))
        self.test_device_label.setText(QCoreApplication.translate("TestDialog", u"\u8bbe\u5907", None))
        self.model_label.setText(QCoreApplication.translate("TestDialog", u"\u6a21\u578b", None))
        self.group_param_label.setText(QCoreApplication.translate("TestDialog", u"\u6d4b\u8bd5\u53c2\u6570", None))
        self.group_param_label.setProperty(u"objectName", QCoreApplication.translate("TestDialog", u"dialogSectionTitle", None))
        self.confidence_label.setText(QCoreApplication.translate("TestDialog", u"\u7f6e\u4fe1\u5ea6\uff080~1\uff09", None))
        self.iou_treshold_label.setText(QCoreApplication.translate("TestDialog", u"IoU \u9608\u503c\uff080~1\uff09", None))
        self.output_label_label.setText(QCoreApplication.translate("TestDialog", u"\u8f93\u51fa\u6807\u7b7e\u6587\u4ef6", None))
        self.start_test_btn.setText(QCoreApplication.translate("TestDialog", u"\u5f00\u59cb\u6d4b\u8bd5", None))
    # retranslateUi

