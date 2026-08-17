# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_data.ui'
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
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ImportData(object):
    def setupUi(self, ImportData):
        if not ImportData.objectName():
            ImportData.setObjectName(u"ImportData")
        ImportData.resize(796, 437)
        self.gridLayout = QGridLayout(ImportData)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.image_path_txt = QLineEdit(ImportData)
        self.image_path_txt.setObjectName(u"image_path_txt")
        self.image_path_txt.setMinimumSize(QSize(300, 40))

        self.horizontalLayout.addWidget(self.image_path_txt)

        self.choose_image_dir_btn = QPushButton(ImportData)
        self.choose_image_dir_btn.setObjectName(u"choose_image_dir_btn")
        self.choose_image_dir_btn.setMinimumSize(QSize(60, 40))
        icon = QIcon()
        icon.addFile(u"../resources/\u6253\u5f00.png", QSize(), QIcon.Normal, QIcon.Off)
        self.choose_image_dir_btn.setIcon(icon)
        self.choose_image_dir_btn.setIconSize(QSize(45, 40))

        self.horizontalLayout.addWidget(self.choose_image_dir_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_path_txt = QLineEdit(ImportData)
        self.label_path_txt.setObjectName(u"label_path_txt")
        self.label_path_txt.setMinimumSize(QSize(300, 40))

        self.horizontalLayout_2.addWidget(self.label_path_txt)

        self.choose_label_dir_btn = QPushButton(ImportData)
        self.choose_label_dir_btn.setObjectName(u"choose_label_dir_btn")
        self.choose_label_dir_btn.setMinimumSize(QSize(60, 40))
        self.choose_label_dir_btn.setIcon(icon)
        self.choose_label_dir_btn.setIconSize(QSize(45, 40))

        self.horizontalLayout_2.addWidget(self.choose_label_dir_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_fmt = QLabel(ImportData)
        self.label_fmt.setObjectName(u"label_fmt")
        font = QFont()
        font.setFamilies([u"Microsoft YaHei"])
        font.setPointSize(12)
        self.label_fmt.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_fmt)

        self.yolo_fmt = QRadioButton(ImportData)
        self.yolo_fmt.setObjectName(u"yolo_fmt")
        self.yolo_fmt.setFont(font)

        self.horizontalLayout_3.addWidget(self.yolo_fmt)

        self.labelme_fmt = QRadioButton(ImportData)
        self.labelme_fmt.setObjectName(u"labelme_fmt")
        self.labelme_fmt.setFont(font)
        self.labelme_fmt.setChecked(True)

        self.horizontalLayout_3.addWidget(self.labelme_fmt)

        self.cls_fmt = QRadioButton(ImportData)
        self.cls_fmt.setObjectName(u"cls_fmt")

        self.horizontalLayout_3.addWidget(self.cls_fmt)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tips_lbl = QLabel(ImportData)
        self.tips_lbl.setObjectName(u"tips_lbl")
        self.tips_lbl.setFont(font)

        self.horizontalLayout_4.addWidget(self.tips_lbl)

        self.progress_bar = QProgressBar(ImportData)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(24)

        self.horizontalLayout_4.addWidget(self.progress_bar)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.done_import_btn = QPushButton(ImportData)
        self.done_import_btn.setObjectName(u"done_import_btn")
        self.done_import_btn.setMinimumSize(QSize(100, 50))
        icon1 = QIcon()
        icon1.addFile(u"../resources/\u786e\u5b9a.png", QSize(), QIcon.Normal, QIcon.Off)
        self.done_import_btn.setIcon(icon1)
        self.done_import_btn.setIconSize(QSize(40, 25))

        self.horizontalLayout_5.addWidget(self.done_import_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.retranslateUi(ImportData)

        QMetaObject.connectSlotsByName(ImportData)
    # setupUi

    def retranslateUi(self, ImportData):
        ImportData.setWindowTitle(QCoreApplication.translate("ImportData", u"\u5bfc\u5165\u6570\u636e", None))
        self.image_path_txt.setPlaceholderText(QCoreApplication.translate("ImportData", u"\u56fe\u50cf\u8def\u5f84", None))
        self.choose_image_dir_btn.setText("")
        self.label_path_txt.setPlaceholderText(QCoreApplication.translate("ImportData", u"\u6807\u7b7e\u8def\u5f84", None))
        self.choose_label_dir_btn.setText("")
        self.label_fmt.setText(QCoreApplication.translate("ImportData", u"\u6807\u7b7e\u683c\u5f0f:", None))
        self.yolo_fmt.setText(QCoreApplication.translate("ImportData", u"Yolo txt", None))
        self.labelme_fmt.setText(QCoreApplication.translate("ImportData", u"Labelme json", None))
        self.cls_fmt.setText(QCoreApplication.translate("ImportData", u"\u6309\u5b50\u6587\u4ef6\u5939\u5206\u7c7b\u5bfc\u5165", None))
        self.tips_lbl.setText(QCoreApplication.translate("ImportData", u"\u63d0\u793a\u4fe1\u606f", None))
        self.done_import_btn.setText("")
    # retranslateUi

