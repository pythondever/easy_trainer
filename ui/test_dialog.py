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
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_TestDialog(object):
    def setupUi(self, TestDialog):
        if not TestDialog.objectName():
            TestDialog.setObjectName(u"TestDialog")
        TestDialog.resize(520, 560)
        TestDialog.setMinimumSize(QSize(500, 0))
        self.mainLayout = QVBoxLayout(TestDialog)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 18)
        self.title_label = QLabel(TestDialog)
        self.title_label.setObjectName(u"title_label")

        self.mainLayout.addWidget(self.title_label)

        self.model_card = QFrame(TestDialog)
        self.model_card.setObjectName(u"model_card")
        self.model_card.setFrameShape(QFrame.NoFrame)
        self.model_card_layout = QVBoxLayout(self.model_card)
        self.model_card_layout.setSpacing(5)
        self.model_card_layout.setObjectName(u"model_card_layout")
        self.model_card_layout.setContentsMargins(14, 12, 14, 12)
        self.model_card_top = QHBoxLayout()
        self.model_card_top.setSpacing(8)
        self.model_card_top.setObjectName(u"model_card_top")
        self.task_badge = QLabel(self.model_card)
        self.task_badge.setObjectName(u"task_badge")

        self.model_card_top.addWidget(self.task_badge)

        self.model_name = QLabel(self.model_card)
        self.model_name.setObjectName(u"model_name")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.model_name.sizePolicy().hasHeightForWidth())
        self.model_name.setSizePolicy(sizePolicy)

        self.model_card_top.addWidget(self.model_name)


        self.model_card_layout.addLayout(self.model_card_top)

        self.model_meta = QLabel(self.model_card)
        self.model_meta.setObjectName(u"model_meta")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.model_meta.sizePolicy().hasHeightForWidth())
        self.model_meta.setSizePolicy(sizePolicy1)
        self.model_meta.setWordWrap(True)

        self.model_card_layout.addWidget(self.model_meta)


        self.mainLayout.addWidget(self.model_card)

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
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.test_data_combo.sizePolicy().hasHeightForWidth())
        self.test_data_combo.setSizePolicy(sizePolicy2)
        self.test_data_combo.setMinimumSize(QSize(300, 0))

        self.form_source.setWidget(0, QFormLayout.ItemRole.FieldRole, self.test_data_combo)

        self.test_device_label = QLabel(TestDialog)
        self.test_device_label.setObjectName(u"test_device_label")

        self.form_source.setWidget(1, QFormLayout.ItemRole.LabelRole, self.test_device_label)

        self.test_device_combo = QComboBox(TestDialog)
        self.test_device_combo.setObjectName(u"test_device_combo")
        sizePolicy2.setHeightForWidth(self.test_device_combo.sizePolicy().hasHeightForWidth())
        self.test_device_combo.setSizePolicy(sizePolicy2)
        self.test_device_combo.setMinimumSize(QSize(300, 0))

        self.form_source.setWidget(1, QFormLayout.ItemRole.FieldRole, self.test_device_combo)


        self.mainLayout.addLayout(self.form_source)

        self.group_param_title = QLabel(TestDialog)
        self.group_param_title.setObjectName(u"group_param_title")

        self.mainLayout.addWidget(self.group_param_title)

        self.form_param = QFormLayout()
        self.form_param.setObjectName(u"form_param")
        self.form_param.setHorizontalSpacing(14)
        self.form_param.setVerticalSpacing(10)
        self.form_param.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.confidence_label = QLabel(TestDialog)
        self.confidence_label.setObjectName(u"confidence_label")

        self.form_param.setWidget(0, QFormLayout.ItemRole.LabelRole, self.confidence_label)

        self.conf_wrap = QWidget(TestDialog)
        self.conf_wrap.setObjectName(u"conf_wrap")
        self.conf_wrap_layout = QVBoxLayout(self.conf_wrap)
        self.conf_wrap_layout.setSpacing(4)
        self.conf_wrap_layout.setObjectName(u"conf_wrap_layout")
        self.conf_wrap_layout.setContentsMargins(0, 0, 0, 0)
        self.confidence_txt = QLineEdit(self.conf_wrap)
        self.confidence_txt.setObjectName(u"confidence_txt")
        sizePolicy2.setHeightForWidth(self.confidence_txt.sizePolicy().hasHeightForWidth())
        self.confidence_txt.setSizePolicy(sizePolicy2)
        self.confidence_txt.setMinimumSize(QSize(300, 0))

        self.conf_wrap_layout.addWidget(self.confidence_txt)

        self.conf_note = QLabel(self.conf_wrap)
        self.conf_note.setObjectName(u"conf_note")
        sizePolicy1.setHeightForWidth(self.conf_note.sizePolicy().hasHeightForWidth())
        self.conf_note.setSizePolicy(sizePolicy1)
        self.conf_note.setWordWrap(True)

        self.conf_wrap_layout.addWidget(self.conf_note)


        self.form_param.setWidget(0, QFormLayout.ItemRole.FieldRole, self.conf_wrap)

        self.iou_treshold_label = QLabel(TestDialog)
        self.iou_treshold_label.setObjectName(u"iou_treshold_label")

        self.form_param.setWidget(1, QFormLayout.ItemRole.LabelRole, self.iou_treshold_label)

        self.iou_wrap = QWidget(TestDialog)
        self.iou_wrap.setObjectName(u"iou_wrap")
        self.iou_wrap_layout = QVBoxLayout(self.iou_wrap)
        self.iou_wrap_layout.setSpacing(4)
        self.iou_wrap_layout.setObjectName(u"iou_wrap_layout")
        self.iou_wrap_layout.setContentsMargins(0, 0, 0, 0)
        self.iou_treshold_txt = QLineEdit(self.iou_wrap)
        self.iou_treshold_txt.setObjectName(u"iou_treshold_txt")
        sizePolicy2.setHeightForWidth(self.iou_treshold_txt.sizePolicy().hasHeightForWidth())
        self.iou_treshold_txt.setSizePolicy(sizePolicy2)
        self.iou_treshold_txt.setMinimumSize(QSize(300, 0))

        self.iou_wrap_layout.addWidget(self.iou_treshold_txt)

        self.iou_note = QLabel(self.iou_wrap)
        self.iou_note.setObjectName(u"iou_note")
        sizePolicy1.setHeightForWidth(self.iou_note.sizePolicy().hasHeightForWidth())
        self.iou_note.setSizePolicy(sizePolicy1)
        self.iou_note.setWordWrap(True)

        self.iou_wrap_layout.addWidget(self.iou_note)


        self.form_param.setWidget(1, QFormLayout.ItemRole.FieldRole, self.iou_wrap)

        self.output_label_label = QLabel(TestDialog)
        self.output_label_label.setObjectName(u"output_label_label")

        self.form_param.setWidget(2, QFormLayout.ItemRole.LabelRole, self.output_label_label)

        self.out_wrap = QWidget(TestDialog)
        self.out_wrap.setObjectName(u"out_wrap")
        self.out_wrap_layout = QHBoxLayout(self.out_wrap)
        self.out_wrap_layout.setSpacing(10)
        self.out_wrap_layout.setObjectName(u"out_wrap_layout")
        self.out_wrap_layout.setContentsMargins(0, 0, 0, 0)
        self.output_label_file_checkBox = QCheckBox(self.out_wrap)
        self.output_label_file_checkBox.setObjectName(u"output_label_file_checkBox")

        self.out_wrap_layout.addWidget(self.output_label_file_checkBox)

        self.out_note = QLabel(self.out_wrap)
        self.out_note.setObjectName(u"out_note")
        sizePolicy.setHeightForWidth(self.out_note.sizePolicy().hasHeightForWidth())
        self.out_note.setSizePolicy(sizePolicy)
        self.out_note.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.out_wrap_layout.addWidget(self.out_note)


        self.form_param.setWidget(2, QFormLayout.ItemRole.FieldRole, self.out_wrap)


        self.mainLayout.addLayout(self.form_param)

        self.bottomSpacerTop = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacerTop)

        self.summary_bar = QFrame(TestDialog)
        self.summary_bar.setObjectName(u"summary_bar")
        self.summary_bar.setFrameShape(QFrame.NoFrame)
        self.summary_bar_layout = QHBoxLayout(self.summary_bar)
        self.summary_bar_layout.setSpacing(8)
        self.summary_bar_layout.setObjectName(u"summary_bar_layout")
        self.summary_bar_layout.setContentsMargins(12, 10, 12, 10)
        self.summary_icon = QLabel(self.summary_bar)
        self.summary_icon.setObjectName(u"summary_icon")

        self.summary_bar_layout.addWidget(self.summary_icon)

        self.summary_text = QLabel(self.summary_bar)
        self.summary_text.setObjectName(u"summary_text")
        sizePolicy.setHeightForWidth(self.summary_text.sizePolicy().hasHeightForWidth())
        self.summary_text.setSizePolicy(sizePolicy)
        self.summary_text.setWordWrap(True)
        self.summary_text.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.summary_bar_layout.addWidget(self.summary_text)


        self.mainLayout.addWidget(self.summary_bar)

        self.button_line = QFrame(TestDialog)
        self.button_line.setObjectName(u"button_line")
        self.button_line.setFrameShape(QFrame.HLine)
        self.button_line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addWidget(self.button_line)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setSpacing(10)
        self.bottom_row.setObjectName(u"bottom_row")
        self.bottom_spacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer_left)

        self.cancel_btn = QPushButton(TestDialog)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.bottom_row.addWidget(self.cancel_btn)

        self.start_test_btn = QPushButton(TestDialog)
        self.start_test_btn.setObjectName(u"start_test_btn")
        self.start_test_btn.setMinimumSize(QSize(140, 38))

        self.bottom_row.addWidget(self.start_test_btn)


        self.mainLayout.addLayout(self.bottom_row)


        self.retranslateUi(TestDialog)

        QMetaObject.connectSlotsByName(TestDialog)
    # setupUi

    def retranslateUi(self, TestDialog):
        TestDialog.setWindowTitle(QCoreApplication.translate("TestDialog", u"\u6a21\u578b\u6d4b\u8bd5", None))
        self.title_label.setText(QCoreApplication.translate("TestDialog", u"\u6a21\u578b\u6d4b\u8bd5", None))
        self.title_label.setProperty(u"class", QCoreApplication.translate("TestDialog", u"dialogTitle", None))
        self.task_badge.setText(QCoreApplication.translate("TestDialog", u"\u68c0\u6d4b", None))
        self.task_badge.setProperty(u"class", QCoreApplication.translate("TestDialog", u"taskBadge", None))
        self.model_name.setText(QCoreApplication.translate("TestDialog", u"best.pth", None))
        self.model_name.setProperty(u"class", QCoreApplication.translate("TestDialog", u"modelName", None))
        self.model_meta.setText(QCoreApplication.translate("TestDialog", u"mAP50 0.912 \u00b7 \u8f93\u5165 640 \u00b7 \u89c4\u6a21 n \u00b7 \u8bad\u7ec3 2026-09-01 14:22", None))
        self.model_meta.setProperty(u"class", QCoreApplication.translate("TestDialog", u"modelMeta", None))
        self.group_source_title.setText(QCoreApplication.translate("TestDialog", u"\u6570\u636e\u4e0e\u8bbe\u5907", None))
        self.group_source_title.setProperty(u"class", QCoreApplication.translate("TestDialog", u"dialogSectionTitle", None))
        self.test_data_label.setText(QCoreApplication.translate("TestDialog", u"\u6570\u636e", None))
        self.test_device_label.setText(QCoreApplication.translate("TestDialog", u"\u8bbe\u5907", None))
        self.group_param_title.setText(QCoreApplication.translate("TestDialog", u"\u6d4b\u8bd5\u53c2\u6570", None))
        self.group_param_title.setProperty(u"class", QCoreApplication.translate("TestDialog", u"dialogSectionTitle", None))
        self.confidence_label.setText(QCoreApplication.translate("TestDialog", u"\u7f6e\u4fe1\u5ea6", None))
        self.conf_note.setText(QCoreApplication.translate("TestDialog", u"\u4f4e\u4e8e\u8be5\u5206\u6570\u7684\u9884\u6d4b\u76f4\u63a5\u4e22\u5f03", None))
        self.conf_note.setProperty(u"class", QCoreApplication.translate("TestDialog", u"fieldNote", None))
        self.iou_treshold_label.setText(QCoreApplication.translate("TestDialog", u"IoU \u9608\u503c", None))
        self.iou_note.setText(QCoreApplication.translate("TestDialog", u"\u4e0e\u6807\u6ce8\u6846\u91cd\u5408\u5ea6\u8fbe\u6807\u624d\u7b97\u6b63\u786e\u68c0\u51fa", None))
        self.iou_note.setProperty(u"class", QCoreApplication.translate("TestDialog", u"fieldNote", None))
        self.output_label_label.setText(QCoreApplication.translate("TestDialog", u"\u8f93\u51fa\u6807\u7b7e\u6587\u4ef6", None))
        self.output_label_file_checkBox.setText("")
        self.out_note.setText(QCoreApplication.translate("TestDialog", u"\u628a\u9884\u6d4b\u6846\u5199\u6210 labelme json\uff0c\u4fbf\u4e8e\u4eba\u5de5\u590d\u6838", None))
        self.out_note.setProperty(u"class", QCoreApplication.translate("TestDialog", u"fieldNote", None))
        self.summary_icon.setText(QCoreApplication.translate("TestDialog", u"i", None))
        self.summary_icon.setProperty(u"class", QCoreApplication.translate("TestDialog", u"summaryIcon", None))
        self.summary_text.setText(QCoreApplication.translate("TestDialog", u"\u8bf7\u9009\u62e9\u6570\u636e\u96c6", None))
        self.summary_text.setProperty(u"class", QCoreApplication.translate("TestDialog", u"summaryText", None))
        self.cancel_btn.setText(QCoreApplication.translate("TestDialog", u"\u53d6\u6d88", None))
        self.start_test_btn.setText(QCoreApplication.translate("TestDialog", u"\u5f00\u59cb\u6d4b\u8bd5", None))
    # retranslateUi

