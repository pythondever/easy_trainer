# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'classify.ui'
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

class Ui_ClassifyDialog(object):
    def setupUi(self, ClassifyDialog):
        if not ClassifyDialog.objectName():
            ClassifyDialog.setObjectName(u"ClassifyDialog")
        ClassifyDialog.resize(948, 579)
        self.gridLayout = QGridLayout(ClassifyDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.train_cfg_label = QLabel(ClassifyDialog)
        self.train_cfg_label.setObjectName(u"train_cfg_label")

        self.horizontalLayout.addWidget(self.train_cfg_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.dataset_label = QLabel(ClassifyDialog)
        self.dataset_label.setObjectName(u"dataset_label")

        self.horizontalLayout_2.addWidget(self.dataset_label)

        self.dataset_combo = QComboBox(ClassifyDialog)
        self.dataset_combo.setObjectName(u"dataset_combo")

        self.horizontalLayout_2.addWidget(self.dataset_combo)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_val = QHBoxLayout()
        self.horizontalLayout_val.setObjectName(u"horizontalLayout_val")
        self.val_label = QLabel(ClassifyDialog)
        self.val_label.setObjectName(u"val_label")

        self.horizontalLayout_val.addWidget(self.val_label)

        self.val_combo = QComboBox(ClassifyDialog)
        self.val_combo.setObjectName(u"val_combo")

        self.horizontalLayout_val.addWidget(self.val_combo)

        self.horizontalSpacer_val = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_val.addItem(self.horizontalSpacer_val)


        self.verticalLayout.addLayout(self.horizontalLayout_val)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.network_label = QLabel(ClassifyDialog)
        self.network_label.setObjectName(u"network_label")

        self.horizontalLayout_3.addWidget(self.network_label)

        self.network_combo = QComboBox(ClassifyDialog)
        self.network_combo.setObjectName(u"network_combo")

        self.horizontalLayout_3.addWidget(self.network_combo)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.device_label = QLabel(ClassifyDialog)
        self.device_label.setObjectName(u"device_label")

        self.horizontalLayout_4.addWidget(self.device_label)

        self.device_combo = QComboBox(ClassifyDialog)
        self.device_combo.setObjectName(u"device_combo")

        self.horizontalLayout_4.addWidget(self.device_combo)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.img_size_label = QLabel(ClassifyDialog)
        self.img_size_label.setObjectName(u"img_size_label")

        self.horizontalLayout_19.addWidget(self.img_size_label)

        self.img_size_comboBox = QComboBox(ClassifyDialog)
        self.img_size_comboBox.setObjectName(u"img_size_comboBox")

        self.horizontalLayout_19.addWidget(self.img_size_comboBox)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_12)


        self.verticalLayout.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.optimizer_label = QLabel(ClassifyDialog)
        self.optimizer_label.setObjectName(u"optimizer_label")

        self.horizontalLayout_20.addWidget(self.optimizer_label)

        self.optimizer_comboBox = QComboBox(ClassifyDialog)
        self.optimizer_comboBox.setObjectName(u"optimizer_comboBox")

        self.horizontalLayout_20.addWidget(self.optimizer_comboBox)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_13)


        self.verticalLayout.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.batch_label = QLabel(ClassifyDialog)
        self.batch_label.setObjectName(u"batch_label")

        self.horizontalLayout_5.addWidget(self.batch_label)

        self.batch_size_line_txt = QLineEdit(ClassifyDialog)
        self.batch_size_line_txt.setObjectName(u"batch_size_line_txt")
        self.batch_size_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_5.addWidget(self.batch_size_line_txt)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.epoch_label = QLabel(ClassifyDialog)
        self.epoch_label.setObjectName(u"epoch_label")

        self.horizontalLayout_18.addWidget(self.epoch_label)

        self.epochs_line_txt = QLineEdit(ClassifyDialog)
        self.epochs_line_txt.setObjectName(u"epochs_line_txt")
        self.epochs_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_18.addWidget(self.epochs_line_txt)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.loader_num_label = QLabel(ClassifyDialog)
        self.loader_num_label.setObjectName(u"loader_num_label")

        self.horizontalLayout_9.addWidget(self.loader_num_label)

        self.batch_size_line_txt_2 = QLineEdit(ClassifyDialog)
        self.batch_size_line_txt_2.setObjectName(u"batch_size_line_txt_2")
        self.batch_size_line_txt_2.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_9.addWidget(self.batch_size_line_txt_2)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lr_label = QLabel(ClassifyDialog)
        self.lr_label.setObjectName(u"lr_label")

        self.horizontalLayout_6.addWidget(self.lr_label)

        self.lr_line_txt = QLineEdit(ClassifyDialog)
        self.lr_line_txt.setObjectName(u"lr_line_txt")
        self.lr_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_6.addWidget(self.lr_line_txt)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.output_label = QLabel(ClassifyDialog)
        self.output_label.setObjectName(u"output_label")

        self.horizontalLayout_8.addWidget(self.output_label)

        self.output_line_txt = QLineEdit(ClassifyDialog)
        self.output_line_txt.setObjectName(u"output_line_txt")
        self.output_line_txt.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_8.addWidget(self.output_line_txt)

        self.select_output_path_btn = QPushButton(ClassifyDialog)
        self.select_output_path_btn.setObjectName(u"select_output_path_btn")

        self.horizontalLayout_8.addWidget(self.select_output_path_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_17.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.horizontalLayout_17, 0, 0, 1, 1)

        self.bottomActions = QHBoxLayout()
        self.bottomActions.setObjectName(u"bottomActions")
        self.horizontalSpacer_bottomLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomActions.addItem(self.horizontalSpacer_bottomLeft)

        self.start_train = QPushButton(ClassifyDialog)
        self.start_train.setObjectName(u"start_train")

        self.bottomActions.addWidget(self.start_train)

        self.horizontalSpacer_bottomMid = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomActions.addItem(self.horizontalSpacer_bottomMid)


        self.gridLayout.addLayout(self.bottomActions, 1, 0, 1, 1)


        self.retranslateUi(ClassifyDialog)

        QMetaObject.connectSlotsByName(ClassifyDialog)
    # setupUi

    def retranslateUi(self, ClassifyDialog):
        ClassifyDialog.setWindowTitle(QCoreApplication.translate("ClassifyDialog", u"Dialog", None))
        self.train_cfg_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u8bad\u7ec3\u53c2\u6570\u914d\u7f6e", None))
        self.dataset_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u8bad\u7ec3\u96c6", None))
        self.val_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u9a8c\u8bc1\u96c6", None))
        self.network_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u7f51\u7edc", None))
        self.device_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u8bbe\u5907", None))
        self.img_size_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u56fe\u50cf\u5c3a\u5bf8", None))
        self.optimizer_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u4f18\u5316\u5668", None))
        self.batch_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u6279\u6b21", None))
        self.epoch_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u8f6e\u6b21", None))
        self.loader_num_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u7ebf\u7a0b\u6570", None))
        self.lr_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u5b66\u4e60\u7387", None))
        self.output_label.setText(QCoreApplication.translate("ClassifyDialog", u"\u8f93\u51fa\u8def\u5f84", None))
        self.output_line_txt.setText("")
        self.select_output_path_btn.setText(QCoreApplication.translate("ClassifyDialog", u"\u9009\u62e9\u8def\u5f84", None))
        self.start_train.setText(QCoreApplication.translate("ClassifyDialog", u"\u5f00\u59cb\u8bad\u7ec3", None))
    # retranslateUi

