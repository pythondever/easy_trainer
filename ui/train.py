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
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_TrainDialog(object):
    def setupUi(self, TrainDialog):
        if not TrainDialog.objectName():
            TrainDialog.setObjectName(u"TrainDialog")
        TrainDialog.resize(740, 560)
        self.mainLayout = QVBoxLayout(TrainDialog)
        self.mainLayout.setSpacing(12)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(28, 20, 28, 20)
        self.rowBasic = QHBoxLayout()
        self.rowBasic.setSpacing(28)
        self.rowBasic.setObjectName(u"rowBasic")
        self.formBasic = QFormLayout()
        self.formBasic.setObjectName(u"formBasic")
        self.formBasic.setHorizontalSpacing(12)
        self.formBasic.setVerticalSpacing(12)
        self.task_label = QLabel(TrainDialog)
        self.task_label.setObjectName(u"task_label")

        self.formBasic.setWidget(0, QFormLayout.ItemRole.LabelRole, self.task_label)

        self.task_combo = QComboBox(TrainDialog)
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.setObjectName(u"task_combo")

        self.formBasic.setWidget(0, QFormLayout.ItemRole.FieldRole, self.task_combo)

        self.dataset_label = QLabel(TrainDialog)
        self.dataset_label.setObjectName(u"dataset_label")

        self.formBasic.setWidget(1, QFormLayout.ItemRole.LabelRole, self.dataset_label)

        self.dataset_combo = QComboBox(TrainDialog)
        self.dataset_combo.setObjectName(u"dataset_combo")

        self.formBasic.setWidget(1, QFormLayout.ItemRole.FieldRole, self.dataset_combo)


        self.rowBasic.addLayout(self.formBasic)

        self.formModel = QFormLayout()
        self.formModel.setObjectName(u"formModel")
        self.formModel.setHorizontalSpacing(12)
        self.formModel.setVerticalSpacing(12)
        self.network_label = QLabel(TrainDialog)
        self.network_label.setObjectName(u"network_label")

        self.formModel.setWidget(0, QFormLayout.ItemRole.LabelRole, self.network_label)

        self.network_combo = QComboBox(TrainDialog)
        self.network_combo.setObjectName(u"network_combo")

        self.formModel.setWidget(0, QFormLayout.ItemRole.FieldRole, self.network_combo)

        self.device_label = QLabel(TrainDialog)
        self.device_label.setObjectName(u"device_label")

        self.formModel.setWidget(1, QFormLayout.ItemRole.LabelRole, self.device_label)

        self.device_combo = QComboBox(TrainDialog)
        self.device_combo.setObjectName(u"device_combo")

        self.formModel.setWidget(1, QFormLayout.ItemRole.FieldRole, self.device_combo)


        self.rowBasic.addLayout(self.formModel)

        self.rowBasic.setStretch(0, 1)
        self.rowBasic.setStretch(1, 1)

        self.mainLayout.addLayout(self.rowBasic)

        self.rowHyper = QHBoxLayout()
        self.rowHyper.setSpacing(28)
        self.rowHyper.setObjectName(u"rowHyper")
        self.formHyper1 = QFormLayout()
        self.formHyper1.setObjectName(u"formHyper1")
        self.formHyper1.setHorizontalSpacing(12)
        self.formHyper1.setVerticalSpacing(12)
        self.optimizer_label = QLabel(TrainDialog)
        self.optimizer_label.setObjectName(u"optimizer_label")

        self.formHyper1.setWidget(0, QFormLayout.ItemRole.LabelRole, self.optimizer_label)

        self.optimizer_comboBox = QComboBox(TrainDialog)
        self.optimizer_comboBox.setObjectName(u"optimizer_comboBox")

        self.formHyper1.setWidget(0, QFormLayout.ItemRole.FieldRole, self.optimizer_comboBox)

        self.img_size_label = QLabel(TrainDialog)
        self.img_size_label.setObjectName(u"img_size_label")

        self.formHyper1.setWidget(1, QFormLayout.ItemRole.LabelRole, self.img_size_label)

        self.img_size_line_txt = QLineEdit(TrainDialog)
        self.img_size_line_txt.setObjectName(u"img_size_line_txt")

        self.formHyper1.setWidget(1, QFormLayout.ItemRole.FieldRole, self.img_size_line_txt)

        self.early_stop_label = QLabel(TrainDialog)
        self.early_stop_label.setObjectName(u"early_stop_label")

        self.formHyper1.setWidget(2, QFormLayout.ItemRole.LabelRole, self.early_stop_label)

        self.early_stop_line_txt = QLineEdit(TrainDialog)
        self.early_stop_line_txt.setObjectName(u"early_stop_line_txt")

        self.formHyper1.setWidget(2, QFormLayout.ItemRole.FieldRole, self.early_stop_line_txt)

        self.batch_label = QLabel(TrainDialog)
        self.batch_label.setObjectName(u"batch_label")

        self.formHyper1.setWidget(3, QFormLayout.ItemRole.LabelRole, self.batch_label)

        self.batch_size_line_txt = QLineEdit(TrainDialog)
        self.batch_size_line_txt.setObjectName(u"batch_size_line_txt")

        self.formHyper1.setWidget(3, QFormLayout.ItemRole.FieldRole, self.batch_size_line_txt)


        self.rowHyper.addLayout(self.formHyper1)

        self.formHyper2 = QFormLayout()
        self.formHyper2.setObjectName(u"formHyper2")
        self.formHyper2.setHorizontalSpacing(12)
        self.formHyper2.setVerticalSpacing(12)
        self.grad_accum_label = QLabel(TrainDialog)
        self.grad_accum_label.setObjectName(u"grad_accum_label")

        self.formHyper2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.grad_accum_label)

        self.grad_accum_line_txt = QLineEdit(TrainDialog)
        self.grad_accum_line_txt.setObjectName(u"grad_accum_line_txt")

        self.formHyper2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.grad_accum_line_txt)

        self.epoch_label = QLabel(TrainDialog)
        self.epoch_label.setObjectName(u"epoch_label")

        self.formHyper2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.epoch_label)

        self.epochs_line_txt = QLineEdit(TrainDialog)
        self.epochs_line_txt.setObjectName(u"epochs_line_txt")

        self.formHyper2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.epochs_line_txt)

        self.loader_num_label = QLabel(TrainDialog)
        self.loader_num_label.setObjectName(u"loader_num_label")

        self.formHyper2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.loader_num_label)

        self.batch_size_line_txt_2 = QLineEdit(TrainDialog)
        self.batch_size_line_txt_2.setObjectName(u"batch_size_line_txt_2")

        self.formHyper2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.batch_size_line_txt_2)

        self.lr_label = QLabel(TrainDialog)
        self.lr_label.setObjectName(u"lr_label")

        self.formHyper2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lr_label)

        self.lr_line_txt = QLineEdit(TrainDialog)
        self.lr_line_txt.setObjectName(u"lr_line_txt")

        self.formHyper2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lr_line_txt)


        self.rowHyper.addLayout(self.formHyper2)

        self.rowHyper.setStretch(0, 1)
        self.rowHyper.setStretch(1, 1)

        self.mainLayout.addLayout(self.rowHyper)

        self.formOut = QFormLayout()
        self.formOut.setObjectName(u"formOut")
        self.formOut.setHorizontalSpacing(12)
        self.formOut.setVerticalSpacing(12)
        self.output_label = QLabel(TrainDialog)
        self.output_label.setObjectName(u"output_label")

        self.formOut.setWidget(0, QFormLayout.ItemRole.LabelRole, self.output_label)

        self.outRow = QHBoxLayout()
        self.outRow.setSpacing(8)
        self.outRow.setObjectName(u"outRow")
        self.output_line_txt = QLineEdit(TrainDialog)
        self.output_line_txt.setObjectName(u"output_line_txt")

        self.outRow.addWidget(self.output_line_txt)

        self.select_output_path_btn = QPushButton(TrainDialog)
        self.select_output_path_btn.setObjectName(u"select_output_path_btn")
        self.select_output_path_btn.setMinimumSize(QSize(90, 30))

        self.outRow.addWidget(self.select_output_path_btn)


        self.formOut.setLayout(0, QFormLayout.ItemRole.FieldRole, self.outRow)


        self.mainLayout.addLayout(self.formOut)

        self.bottomActions = QHBoxLayout()
        self.bottomActions.setObjectName(u"bottomActions")
        self.bottomSpacerLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomActions.addItem(self.bottomSpacerLeft)

        self.start_train = QPushButton(TrainDialog)
        self.start_train.setObjectName(u"start_train")
        self.start_train.setMinimumSize(QSize(120, 40))

        self.bottomActions.addWidget(self.start_train)

        self.bottomSpacerRight = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomActions.addItem(self.bottomSpacerRight)


        self.mainLayout.addLayout(self.bottomActions)


        self.retranslateUi(TrainDialog)

        QMetaObject.connectSlotsByName(TrainDialog)
    # setupUi

    def retranslateUi(self, TrainDialog):
        TrainDialog.setWindowTitle(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3", None))
        self.task_label.setText(QCoreApplication.translate("TrainDialog", u"\u4efb\u52a1\u7c7b\u578b", None))
        self.task_combo.setItemText(0, QCoreApplication.translate("TrainDialog", u"\u68c0\u6d4b", None))
        self.task_combo.setItemText(1, QCoreApplication.translate("TrainDialog", u"\u5206\u5272", None))
        self.task_combo.setItemText(2, QCoreApplication.translate("TrainDialog", u"\u5206\u7c7b", None))

        self.dataset_label.setText(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3\u96c6", None))
        self.network_label.setText(QCoreApplication.translate("TrainDialog", u"\u7f51\u7edc", None))
        self.device_label.setText(QCoreApplication.translate("TrainDialog", u"\u8bbe\u5907", None))
        self.optimizer_label.setText(QCoreApplication.translate("TrainDialog", u"\u4f18\u5316\u5668", None))
        self.img_size_label.setText(QCoreApplication.translate("TrainDialog", u"\u56fe\u50cf\u5c3a\u5bf8", None))
        self.early_stop_label.setText(QCoreApplication.translate("TrainDialog", u"\u65e9\u505c", None))
        self.batch_label.setText(QCoreApplication.translate("TrainDialog", u"\u6279\u6b21", None))
        self.grad_accum_label.setText(QCoreApplication.translate("TrainDialog", u"\u68af\u5ea6\u7d2f\u79ef", None))
        self.epoch_label.setText(QCoreApplication.translate("TrainDialog", u"\u8f6e\u6b21", None))
        self.loader_num_label.setText(QCoreApplication.translate("TrainDialog", u"\u7ebf\u7a0b\u6570", None))
        self.lr_label.setText(QCoreApplication.translate("TrainDialog", u"\u5b66\u4e60\u7387", None))
        self.output_label.setText(QCoreApplication.translate("TrainDialog", u"\u8f93\u51fa\u8def\u5f84", None))
        self.output_line_txt.setText("")
        self.select_output_path_btn.setText(QCoreApplication.translate("TrainDialog", u"\u9009\u62e9\u8def\u5f84", None))
        self.start_train.setText(QCoreApplication.translate("TrainDialog", u"\u5f00\u59cb\u8bad\u7ec3", None))
    # retranslateUi

