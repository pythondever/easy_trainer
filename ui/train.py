# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'train.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_TrainDialog(object):
    def setupUi(self, TrainDialog):
        if not TrainDialog.objectName():
            TrainDialog.setObjectName(u"TrainDialog")
        TrainDialog.resize(740, 600)
        self.mainLayout = QVBoxLayout(TrainDialog)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 18)
        self.title_row = QHBoxLayout()
        self.title_row.setSpacing(10)
        self.title_row.setObjectName(u"title_row")
        self.title_label = QLabel(TrainDialog)
        self.title_label.setObjectName(u"title_label")

        self.title_row.addWidget(self.title_label)

        self.task_badge = QLabel(TrainDialog)
        self.task_badge.setObjectName(u"task_badge")

        self.title_row.addWidget(self.task_badge)

        self.title_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.title_row.addItem(self.title_spacer)


        self.mainLayout.addLayout(self.title_row)

        self.section_data_wrap = QWidget(TrainDialog)
        self.section_data_wrap.setObjectName(u"section_data_wrap")
        self.section_data_layout = QHBoxLayout(self.section_data_wrap)
        self.section_data_layout.setSpacing(10)
        self.section_data_layout.setObjectName(u"section_data_layout")
        self.section_data_layout.setContentsMargins(0, 0, 0, 0)
        self.group_data_title = QLabel(self.section_data_wrap)
        self.group_data_title.setObjectName(u"group_data_title")

        self.section_data_layout.addWidget(self.group_data_title)

        self.group_data_line = QFrame(self.section_data_wrap)
        self.group_data_line.setObjectName(u"group_data_line")
        self.group_data_line.setFrameShape(QFrame.HLine)
        self.group_data_line.setFrameShadow(QFrame.Sunken)

        self.section_data_layout.addWidget(self.group_data_line)


        self.mainLayout.addWidget(self.section_data_wrap)

        self.grid_data = QGridLayout()
        self.grid_data.setObjectName(u"grid_data")
        self.grid_data.setHorizontalSpacing(12)
        self.grid_data.setVerticalSpacing(12)
        self.task_label = QLabel(TrainDialog)
        self.task_label.setObjectName(u"task_label")
        self.task_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_data.addWidget(self.task_label, 0, 0, 1, 1)

        self.task_combo = QComboBox(TrainDialog)
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.setObjectName(u"task_combo")

        self.grid_data.addWidget(self.task_combo, 0, 1, 1, 1)

        self.network_label = QLabel(TrainDialog)
        self.network_label.setObjectName(u"network_label")
        self.network_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_data.addWidget(self.network_label, 0, 2, 1, 1)

        self.network_combo = QComboBox(TrainDialog)
        self.network_combo.setObjectName(u"network_combo")

        self.grid_data.addWidget(self.network_combo, 0, 3, 1, 1)

        self.dataset_label = QLabel(TrainDialog)
        self.dataset_label.setObjectName(u"dataset_label")
        self.dataset_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_data.addWidget(self.dataset_label, 1, 0, 1, 1)

        self.dataset_combo = QComboBox(TrainDialog)
        self.dataset_combo.setObjectName(u"dataset_combo")

        self.grid_data.addWidget(self.dataset_combo, 1, 1, 1, 1)

        self.val_label = QLabel(TrainDialog)
        self.val_label.setObjectName(u"val_label")
        self.val_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_data.addWidget(self.val_label, 1, 2, 1, 1)

        self.val_combo = QComboBox(TrainDialog)
        self.val_combo.setObjectName(u"val_combo")

        self.grid_data.addWidget(self.val_combo, 1, 3, 1, 1)

        self.device_label = QLabel(TrainDialog)
        self.device_label.setObjectName(u"device_label")
        self.device_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_data.addWidget(self.device_label, 2, 0, 1, 1)

        self.device_combo = QComboBox(TrainDialog)
        self.device_combo.setObjectName(u"device_combo")

        self.grid_data.addWidget(self.device_combo, 2, 1, 1, 3)


        self.mainLayout.addLayout(self.grid_data)

        self.section_hyper_wrap = QWidget(TrainDialog)
        self.section_hyper_wrap.setObjectName(u"section_hyper_wrap")
        self.section_hyper_layout = QHBoxLayout(self.section_hyper_wrap)
        self.section_hyper_layout.setSpacing(10)
        self.section_hyper_layout.setObjectName(u"section_hyper_layout")
        self.section_hyper_layout.setContentsMargins(0, 0, 0, 0)
        self.group_hyper_title = QLabel(self.section_hyper_wrap)
        self.group_hyper_title.setObjectName(u"group_hyper_title")

        self.section_hyper_layout.addWidget(self.group_hyper_title)

        self.group_hyper_line = QFrame(self.section_hyper_wrap)
        self.group_hyper_line.setObjectName(u"group_hyper_line")
        self.group_hyper_line.setFrameShape(QFrame.HLine)
        self.group_hyper_line.setFrameShadow(QFrame.Sunken)

        self.section_hyper_layout.addWidget(self.group_hyper_line)


        self.mainLayout.addWidget(self.section_hyper_wrap)

        self.grid_hyper = QGridLayout()
        self.grid_hyper.setObjectName(u"grid_hyper")
        self.grid_hyper.setHorizontalSpacing(12)
        self.grid_hyper.setVerticalSpacing(12)
        self.epoch_label = QLabel(TrainDialog)
        self.epoch_label.setObjectName(u"epoch_label")
        self.epoch_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_hyper.addWidget(self.epoch_label, 0, 0, 1, 1)

        self.epochs_line_txt = QLineEdit(TrainDialog)
        self.epochs_line_txt.setObjectName(u"epochs_line_txt")

        self.grid_hyper.addWidget(self.epochs_line_txt, 0, 1, 1, 1)

        self.optimizer_label = QLabel(TrainDialog)
        self.optimizer_label.setObjectName(u"optimizer_label")
        self.optimizer_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_hyper.addWidget(self.optimizer_label, 0, 2, 1, 1)

        self.optimizer_comboBox = QComboBox(TrainDialog)
        self.optimizer_comboBox.setObjectName(u"optimizer_comboBox")

        self.grid_hyper.addWidget(self.optimizer_comboBox, 0, 3, 1, 1)

        self.early_stop_label = QLabel(TrainDialog)
        self.early_stop_label.setObjectName(u"early_stop_label")
        self.early_stop_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_hyper.addWidget(self.early_stop_label, 1, 0, 1, 1)

        self.early_wrap = QWidget(TrainDialog)
        self.early_wrap.setObjectName(u"early_wrap")
        self.early_wrap_layout = QVBoxLayout(self.early_wrap)
        self.early_wrap_layout.setSpacing(4)
        self.early_wrap_layout.setObjectName(u"early_wrap_layout")
        self.early_wrap_layout.setContentsMargins(0, 0, 0, 0)
        self.early_stop_line_txt = QLineEdit(self.early_wrap)
        self.early_stop_line_txt.setObjectName(u"early_stop_line_txt")

        self.early_wrap_layout.addWidget(self.early_stop_line_txt)

        self.early_note = QLabel(self.early_wrap)
        self.early_note.setObjectName(u"early_note")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.early_note.sizePolicy().hasHeightForWidth())
        self.early_note.setSizePolicy(sizePolicy)
        self.early_note.setWordWrap(True)

        self.early_wrap_layout.addWidget(self.early_note)


        self.grid_hyper.addWidget(self.early_wrap, 1, 1, 1, 1)

        self.lr_label = QLabel(TrainDialog)
        self.lr_label.setObjectName(u"lr_label")
        self.lr_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_hyper.addWidget(self.lr_label, 1, 2, 1, 1)

        self.lr_wrap = QWidget(TrainDialog)
        self.lr_wrap.setObjectName(u"lr_wrap")
        self.lr_wrap_layout = QVBoxLayout(self.lr_wrap)
        self.lr_wrap_layout.setSpacing(4)
        self.lr_wrap_layout.setObjectName(u"lr_wrap_layout")
        self.lr_wrap_layout.setContentsMargins(0, 0, 0, 0)
        self.lr_line_txt = QLineEdit(self.lr_wrap)
        self.lr_line_txt.setObjectName(u"lr_line_txt")

        self.lr_wrap_layout.addWidget(self.lr_line_txt)

        self.lr_note = QLabel(self.lr_wrap)
        self.lr_note.setObjectName(u"lr_note")
        sizePolicy.setHeightForWidth(self.lr_note.sizePolicy().hasHeightForWidth())
        self.lr_note.setSizePolicy(sizePolicy)
        self.lr_note.setWordWrap(True)

        self.lr_wrap_layout.addWidget(self.lr_note)


        self.grid_hyper.addWidget(self.lr_wrap, 1, 3, 1, 1)

        self.batch_label = QLabel(TrainDialog)
        self.batch_label.setObjectName(u"batch_label")
        self.batch_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_hyper.addWidget(self.batch_label, 2, 0, 1, 1)

        self.batch_size_line_txt = QLineEdit(TrainDialog)
        self.batch_size_line_txt.setObjectName(u"batch_size_line_txt")

        self.grid_hyper.addWidget(self.batch_size_line_txt, 2, 1, 1, 1)

        self.img_size_label = QLabel(TrainDialog)
        self.img_size_label.setObjectName(u"img_size_label")
        self.img_size_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_hyper.addWidget(self.img_size_label, 2, 2, 1, 1)

        self.img_wrap = QWidget(TrainDialog)
        self.img_wrap.setObjectName(u"img_wrap")
        self.img_wrap_layout = QHBoxLayout(self.img_wrap)
        self.img_wrap_layout.setSpacing(8)
        self.img_wrap_layout.setObjectName(u"img_wrap_layout")
        self.img_wrap_layout.setContentsMargins(0, 0, 0, 0)
        self.img_size_line_txt = QLineEdit(self.img_wrap)
        self.img_size_line_txt.setObjectName(u"img_size_line_txt")

        self.img_wrap_layout.addWidget(self.img_size_line_txt)

        self.img_note = QLabel(self.img_wrap)
        self.img_note.setObjectName(u"img_note")
        self.img_note.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.img_wrap_layout.addWidget(self.img_note)


        self.grid_hyper.addWidget(self.img_wrap, 2, 3, 1, 1)

        self.grad_accum_label = QLabel(TrainDialog)
        self.grad_accum_label.setObjectName(u"grad_accum_label")
        self.grad_accum_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_hyper.addWidget(self.grad_accum_label, 3, 0, 1, 1)

        self.grad_wrap = QWidget(TrainDialog)
        self.grad_wrap.setObjectName(u"grad_wrap")
        self.grad_wrap_layout = QVBoxLayout(self.grad_wrap)
        self.grad_wrap_layout.setSpacing(4)
        self.grad_wrap_layout.setObjectName(u"grad_wrap_layout")
        self.grad_wrap_layout.setContentsMargins(0, 0, 0, 0)
        self.grad_accum_line_txt = QLineEdit(self.grad_wrap)
        self.grad_accum_line_txt.setObjectName(u"grad_accum_line_txt")

        self.grad_wrap_layout.addWidget(self.grad_accum_line_txt)

        self.grad_note = QLabel(self.grad_wrap)
        self.grad_note.setObjectName(u"grad_note")
        sizePolicy.setHeightForWidth(self.grad_note.sizePolicy().hasHeightForWidth())
        self.grad_note.setSizePolicy(sizePolicy)
        self.grad_note.setWordWrap(True)

        self.grad_wrap_layout.addWidget(self.grad_note)


        self.grid_hyper.addWidget(self.grad_wrap, 3, 1, 1, 1)

        self.loader_num_label = QLabel(TrainDialog)
        self.loader_num_label.setObjectName(u"loader_num_label")
        self.loader_num_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.grid_hyper.addWidget(self.loader_num_label, 3, 2, 1, 1)

        self.batch_size_line_txt_2 = QLineEdit(TrainDialog)
        self.batch_size_line_txt_2.setObjectName(u"batch_size_line_txt_2")

        self.grid_hyper.addWidget(self.batch_size_line_txt_2, 3, 3, 1, 1)


        self.mainLayout.addLayout(self.grid_hyper)

        self.section_out_wrap = QWidget(TrainDialog)
        self.section_out_wrap.setObjectName(u"section_out_wrap")
        self.section_out_layout = QHBoxLayout(self.section_out_wrap)
        self.section_out_layout.setSpacing(10)
        self.section_out_layout.setObjectName(u"section_out_layout")
        self.section_out_layout.setContentsMargins(0, 0, 0, 0)
        self.group_out_title = QLabel(self.section_out_wrap)
        self.group_out_title.setObjectName(u"group_out_title")

        self.section_out_layout.addWidget(self.group_out_title)

        self.group_out_line = QFrame(self.section_out_wrap)
        self.group_out_line.setObjectName(u"group_out_line")
        self.group_out_line.setFrameShape(QFrame.HLine)
        self.group_out_line.setFrameShadow(QFrame.Sunken)

        self.section_out_layout.addWidget(self.group_out_line)


        self.mainLayout.addWidget(self.section_out_wrap)

        self.form_out = QFormLayout()
        self.form_out.setObjectName(u"form_out")
        self.form_out.setHorizontalSpacing(12)
        self.form_out.setVerticalSpacing(12)
        self.form_out.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.output_label = QLabel(TrainDialog)
        self.output_label.setObjectName(u"output_label")

        self.form_out.setWidget(0, QFormLayout.ItemRole.LabelRole, self.output_label)

        self.out_row = QHBoxLayout()
        self.out_row.setSpacing(8)
        self.out_row.setObjectName(u"out_row")
        self.output_line_txt = QLineEdit(TrainDialog)
        self.output_line_txt.setObjectName(u"output_line_txt")

        self.out_row.addWidget(self.output_line_txt)

        self.select_output_path_btn = QPushButton(TrainDialog)
        self.select_output_path_btn.setObjectName(u"select_output_path_btn")
        self.select_output_path_btn.setMinimumSize(QSize(90, 30))

        self.out_row.addWidget(self.select_output_path_btn)


        self.form_out.setLayout(0, QFormLayout.ItemRole.FieldRole, self.out_row)


        self.mainLayout.addLayout(self.form_out)

        self.bottom_spacer_top = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottom_spacer_top)

        self.summary_bar = QFrame(TrainDialog)
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.summary_text.sizePolicy().hasHeightForWidth())
        self.summary_text.setSizePolicy(sizePolicy1)
        self.summary_text.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.summary_bar_layout.addWidget(self.summary_text)


        self.mainLayout.addWidget(self.summary_bar)

        self.button_line = QFrame(TrainDialog)
        self.button_line.setObjectName(u"button_line")
        self.button_line.setFrameShape(QFrame.HLine)
        self.button_line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addWidget(self.button_line)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setSpacing(10)
        self.bottom_row.setObjectName(u"bottom_row")
        self.bottom_spacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer_left)

        self.cancel_btn = QPushButton(TrainDialog)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.bottom_row.addWidget(self.cancel_btn)

        self.start_train = QPushButton(TrainDialog)
        self.start_train.setObjectName(u"start_train")
        self.start_train.setMinimumSize(QSize(120, 38))

        self.bottom_row.addWidget(self.start_train)


        self.mainLayout.addLayout(self.bottom_row)


        self.retranslateUi(TrainDialog)

        QMetaObject.connectSlotsByName(TrainDialog)
    # setupUi

    def retranslateUi(self, TrainDialog):
        TrainDialog.setWindowTitle(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3", None))
        self.title_label.setText(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3", None))
        self.title_label.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"dialogTitle", None))
        self.task_badge.setText(QCoreApplication.translate("TrainDialog", u"\u68c0\u6d4b", None))
        self.task_badge.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"taskBadge", None))
        self.group_data_title.setText(QCoreApplication.translate("TrainDialog", u"\u6a21\u578b\u4e0e\u6570\u636e", None))
        self.group_data_title.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"dialogSectionTitle", None))
        self.group_data_line.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"dialogSectionLine", None))
        self.task_label.setText(QCoreApplication.translate("TrainDialog", u"\u4efb\u52a1\u7c7b\u578b", None))
        self.task_combo.setItemText(0, QCoreApplication.translate("TrainDialog", u"\u68c0\u6d4b", None))
        self.task_combo.setItemText(1, QCoreApplication.translate("TrainDialog", u"\u5206\u5272", None))
        self.task_combo.setItemText(2, QCoreApplication.translate("TrainDialog", u"\u5206\u7c7b", None))

        self.network_label.setText(QCoreApplication.translate("TrainDialog", u"\u7f51\u7edc", None))
        self.dataset_label.setText(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3\u96c6", None))
        self.val_label.setText(QCoreApplication.translate("TrainDialog", u"\u9a8c\u8bc1\u96c6", None))
        self.device_label.setText(QCoreApplication.translate("TrainDialog", u"\u8bbe\u5907", None))
        self.group_hyper_title.setText(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3\u8d85\u53c2", None))
        self.group_hyper_title.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"dialogSectionTitle", None))
        self.group_hyper_line.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"dialogSectionLine", None))
        self.epoch_label.setText(QCoreApplication.translate("TrainDialog", u"\u8f6e\u6b21", None))
        self.optimizer_label.setText(QCoreApplication.translate("TrainDialog", u"\u4f18\u5316\u5668", None))
        self.early_stop_label.setText(QCoreApplication.translate("TrainDialog", u"\u65e9\u505c", None))
        self.early_note.setText(QCoreApplication.translate("TrainDialog", u"\u8fde\u7eed\u65e0\u63d0\u5347\u5219\u63d0\u524d\u7ed3\u675f\uff0c0 \u4e3a\u5173\u95ed", None))
        self.early_note.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"fieldNote", None))
        self.lr_label.setText(QCoreApplication.translate("TrainDialog", u"\u5b66\u4e60\u7387", None))
        self.lr_note.setText(QCoreApplication.translate("TrainDialog", u"\u521d\u59cb\u5b66\u4e60\u7387\uff0c\u8bad\u7ec3\u4e2d\u81ea\u52a8\u8870\u51cf", None))
        self.lr_note.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"fieldNote", None))
        self.batch_label.setText(QCoreApplication.translate("TrainDialog", u"\u6279\u6b21", None))
        self.img_size_label.setText(QCoreApplication.translate("TrainDialog", u"\u56fe\u50cf\u5c3a\u5bf8", None))
        self.img_note.setText(QCoreApplication.translate("TrainDialog", u"32 \u7684\u500d\u6570", None))
        self.img_note.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"fieldNote", None))
        self.grad_accum_label.setText(QCoreApplication.translate("TrainDialog", u"\u68af\u5ea6\u7d2f\u79ef", None))
        self.grad_note.setText(QCoreApplication.translate("TrainDialog", u"\u663e\u5b58\u4e0d\u8db3\u65f6\u8c03\u5927\uff0c\u7b49\u6548\u6279\u6b21 \u00d7 N", None))
        self.grad_note.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"fieldNote", None))
        self.loader_num_label.setText(QCoreApplication.translate("TrainDialog", u"\u7ebf\u7a0b\u6570", None))
        self.group_out_title.setText(QCoreApplication.translate("TrainDialog", u"\u8f93\u51fa", None))
        self.group_out_title.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"dialogSectionTitle", None))
        self.group_out_line.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"dialogSectionLine", None))
        self.output_label.setText(QCoreApplication.translate("TrainDialog", u"\u8f93\u51fa\u8def\u5f84", None))
        self.output_line_txt.setText("")
        self.output_line_txt.setPlaceholderText(QCoreApplication.translate("TrainDialog", u"\u7559\u7a7a\u5219\u81ea\u52a8\u6309\u65f6\u95f4\u751f\u6210\u76ee\u5f55", None))
        self.select_output_path_btn.setText(QCoreApplication.translate("TrainDialog", u"\u9009\u62e9\u8def\u5f84", None))
        self.summary_icon.setText(QCoreApplication.translate("TrainDialog", u"i", None))
        self.summary_icon.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"summaryIcon", None))
        self.summary_text.setText(QCoreApplication.translate("TrainDialog", u"\u8bf7\u9009\u62e9\u8bad\u7ec3\u96c6\u4e0e\u9a8c\u8bc1\u96c6", None))
        self.summary_text.setProperty(u"class", QCoreApplication.translate("TrainDialog", u"summaryText", None))
        self.cancel_btn.setText(QCoreApplication.translate("TrainDialog", u"\u53d6\u6d88", None))
        self.start_train.setText(QCoreApplication.translate("TrainDialog", u"\u5f00\u59cb\u8bad\u7ec3", None))
    # retranslateUi

