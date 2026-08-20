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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_TrainDialog(object):
    def setupUi(self, TrainDialog):
        if not TrainDialog.objectName():
            TrainDialog.setObjectName(u"TrainDialog")
        TrainDialog.resize(1014, 700)
        self.gridLayout = QGridLayout(TrainDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.train_cfg_label = QLabel(TrainDialog)
        self.train_cfg_label.setObjectName(u"train_cfg_label")

        self.horizontalLayout.addWidget(self.train_cfg_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_task = QHBoxLayout()
        self.horizontalLayout_task.setObjectName(u"horizontalLayout_task")
        self.task_label = QLabel(TrainDialog)
        self.task_label.setObjectName(u"task_label")

        self.horizontalLayout_task.addWidget(self.task_label)

        self.task_combo = QComboBox(TrainDialog)
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.addItem("")
        self.task_combo.setObjectName(u"task_combo")

        self.horizontalLayout_task.addWidget(self.task_combo)

        self.horizontalSpacer_task = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_task.addItem(self.horizontalSpacer_task)


        self.verticalLayout.addLayout(self.horizontalLayout_task)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.dataset_label = QLabel(TrainDialog)
        self.dataset_label.setObjectName(u"dataset_label")

        self.horizontalLayout_2.addWidget(self.dataset_label)

        self.dataset_combo = QComboBox(TrainDialog)
        self.dataset_combo.setObjectName(u"dataset_combo")

        self.horizontalLayout_2.addWidget(self.dataset_combo)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_val = QHBoxLayout()
        self.horizontalLayout_val.setObjectName(u"horizontalLayout_val")
        self.val_label = QLabel(TrainDialog)
        self.val_label.setObjectName(u"val_label")

        self.horizontalLayout_val.addWidget(self.val_label)

        self.val_combo = QComboBox(TrainDialog)
        self.val_combo.setObjectName(u"val_combo")

        self.horizontalLayout_val.addWidget(self.val_combo)

        self.horizontalSpacer_val = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_val.addItem(self.horizontalSpacer_val)


        self.verticalLayout.addLayout(self.horizontalLayout_val)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.network_label = QLabel(TrainDialog)
        self.network_label.setObjectName(u"network_label")

        self.horizontalLayout_3.addWidget(self.network_label)

        self.network_combo = QComboBox(TrainDialog)
        self.network_combo.setObjectName(u"network_combo")

        self.horizontalLayout_3.addWidget(self.network_combo)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.device_label = QLabel(TrainDialog)
        self.device_label.setObjectName(u"device_label")

        self.horizontalLayout_4.addWidget(self.device_label)

        self.device_combo = QComboBox(TrainDialog)
        self.device_combo.setObjectName(u"device_combo")

        self.horizontalLayout_4.addWidget(self.device_combo)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_optimizer = QHBoxLayout()
        self.horizontalLayout_optimizer.setObjectName(u"horizontalLayout_optimizer")
        self.optimizer_label = QLabel(TrainDialog)
        self.optimizer_label.setObjectName(u"optimizer_label")

        self.horizontalLayout_optimizer.addWidget(self.optimizer_label)

        self.optimizer_comboBox = QComboBox(TrainDialog)
        self.optimizer_comboBox.setObjectName(u"optimizer_comboBox")

        self.horizontalLayout_optimizer.addWidget(self.optimizer_comboBox)

        self.horizontalSpacer_optimizer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_optimizer.addItem(self.horizontalSpacer_optimizer)


        self.verticalLayout.addLayout(self.horizontalLayout_optimizer)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.img_size_label = QLabel(TrainDialog)
        self.img_size_label.setObjectName(u"img_size_label")

        self.horizontalLayout_19.addWidget(self.img_size_label)

        self.img_size_line_txt = QLineEdit(TrainDialog)
        self.img_size_line_txt.setObjectName(u"img_size_line_txt")
        self.img_size_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_19.addWidget(self.img_size_line_txt)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_12)


        self.verticalLayout.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.early_stop_label = QLabel(TrainDialog)
        self.early_stop_label.setObjectName(u"early_stop_label")

        self.horizontalLayout_23.addWidget(self.early_stop_label)

        self.early_stop_line_txt = QLineEdit(TrainDialog)
        self.early_stop_line_txt.setObjectName(u"early_stop_line_txt")
        self.early_stop_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_23.addWidget(self.early_stop_line_txt)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_16)


        self.verticalLayout.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.batch_label = QLabel(TrainDialog)
        self.batch_label.setObjectName(u"batch_label")

        self.horizontalLayout_5.addWidget(self.batch_label)

        self.batch_size_line_txt = QLineEdit(TrainDialog)
        self.batch_size_line_txt.setObjectName(u"batch_size_line_txt")
        self.batch_size_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_5.addWidget(self.batch_size_line_txt)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.grad_accum_label = QLabel(TrainDialog)
        self.grad_accum_label.setObjectName(u"grad_accum_label")

        self.horizontalLayout_20.addWidget(self.grad_accum_label)

        self.grad_accum_line_txt = QLineEdit(TrainDialog)
        self.grad_accum_line_txt.setObjectName(u"grad_accum_line_txt")
        self.grad_accum_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_20.addWidget(self.grad_accum_line_txt)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_13)


        self.verticalLayout.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.epoch_label = QLabel(TrainDialog)
        self.epoch_label.setObjectName(u"epoch_label")

        self.horizontalLayout_18.addWidget(self.epoch_label)

        self.epochs_line_txt = QLineEdit(TrainDialog)
        self.epochs_line_txt.setObjectName(u"epochs_line_txt")
        self.epochs_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_18.addWidget(self.epochs_line_txt)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.loader_num_label = QLabel(TrainDialog)
        self.loader_num_label.setObjectName(u"loader_num_label")

        self.horizontalLayout_9.addWidget(self.loader_num_label)

        self.batch_size_line_txt_2 = QLineEdit(TrainDialog)
        self.batch_size_line_txt_2.setObjectName(u"batch_size_line_txt_2")
        self.batch_size_line_txt_2.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_9.addWidget(self.batch_size_line_txt_2)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lr_label = QLabel(TrainDialog)
        self.lr_label.setObjectName(u"lr_label")

        self.horizontalLayout_6.addWidget(self.lr_label)

        self.lr_line_txt = QLineEdit(TrainDialog)
        self.lr_line_txt.setObjectName(u"lr_line_txt")
        self.lr_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_6.addWidget(self.lr_line_txt)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.output_label = QLabel(TrainDialog)
        self.output_label.setObjectName(u"output_label")

        self.horizontalLayout_8.addWidget(self.output_label)

        self.output_line_txt = QLineEdit(TrainDialog)
        self.output_line_txt.setObjectName(u"output_line_txt")
        self.output_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_8.addWidget(self.output_line_txt)

        self.select_output_path_btn = QPushButton(TrainDialog)
        self.select_output_path_btn.setObjectName(u"select_output_path_btn")
        self.select_output_path_btn.setMinimumSize(QSize(60, 30))

        self.horizontalLayout_8.addWidget(self.select_output_path_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_17.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.horizontalLayout_17, 0, 0, 1, 1)

        self.bottomActions = QHBoxLayout()
        self.bottomActions.setObjectName(u"bottomActions")
        self.horizontalSpacer_bottomLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomActions.addItem(self.horizontalSpacer_bottomLeft)

        self.start_train = QPushButton(TrainDialog)
        self.start_train.setObjectName(u"start_train")

        self.bottomActions.addWidget(self.start_train)

        self.horizontalSpacer_bottomMid = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomActions.addItem(self.horizontalSpacer_bottomMid)

        self.horizontalSpacer_bottomRight = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomActions.addItem(self.horizontalSpacer_bottomRight)


        self.gridLayout.addLayout(self.bottomActions, 1, 0, 1, 1)


        self.retranslateUi(TrainDialog)

        QMetaObject.connectSlotsByName(TrainDialog)
    # setupUi

    def retranslateUi(self, TrainDialog):
        TrainDialog.setWindowTitle(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3", None))
        self.train_cfg_label.setText(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3\u53c2\u6570\u914d\u7f6e", None))
        self.task_label.setText(QCoreApplication.translate("TrainDialog", u"\u4efb\u52a1\u7c7b\u578b", None))
        self.task_combo.setItemText(0, QCoreApplication.translate("TrainDialog", u"\u68c0\u6d4b", None))
        self.task_combo.setItemText(1, QCoreApplication.translate("TrainDialog", u"\u5206\u5272", None))
        self.task_combo.setItemText(2, QCoreApplication.translate("TrainDialog", u"\u5206\u7c7b", None))

        self.dataset_label.setText(QCoreApplication.translate("TrainDialog", u"\u8bad\u7ec3\u96c6", None))
        self.val_label.setText(QCoreApplication.translate("TrainDialog", u"\u9a8c\u8bc1\u96c6", None))
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

