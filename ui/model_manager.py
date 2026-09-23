# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'model_manager.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ModelManagerDialog(object):
    def setupUi(self, ModelManagerDialog):
        if not ModelManagerDialog.objectName():
            ModelManagerDialog.setObjectName(u"ModelManagerDialog")
        ModelManagerDialog.resize(800, 560)
        self.root_layout = QVBoxLayout(ModelManagerDialog)
        self.root_layout.setSpacing(10)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(22, 18, 22, 16)
        self.groups_scroll = QScrollArea(ModelManagerDialog)
        self.groups_scroll.setObjectName(u"groups_scroll")
        self.groups_scroll.setFrameShape(QFrame.NoFrame)
        self.groups_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.groups_scroll.setWidgetResizable(True)
        self.groups_content = QWidget()
        self.groups_content.setObjectName(u"groups_content")
        self.groups_layout = QVBoxLayout(self.groups_content)
        self.groups_layout.setSpacing(10)
        self.groups_layout.setObjectName(u"groups_layout")
        self.groups_layout.setContentsMargins(0, 0, 0, 0)
        self.detect_title = QLabel(self.groups_content)
        self.detect_title.setObjectName(u"detect_title")
        self.detect_title.setProperty(u"class", u"modelGroupTitle")

        self.groups_layout.addWidget(self.detect_title)

        self.detect_frame = QFrame(self.groups_content)
        self.detect_frame.setObjectName(u"detect_frame")
        self.detect_frame.setProperty(u"class", u"modelGroup")
        self.detect_layout = QVBoxLayout(self.detect_frame)
        self.detect_layout.setSpacing(0)
        self.detect_layout.setObjectName(u"detect_layout")
        self.detect_layout.setContentsMargins(1, 1, 1, 1)

        self.groups_layout.addWidget(self.detect_frame)

        self.detect_cnn_title = QLabel(self.groups_content)
        self.detect_cnn_title.setObjectName(u"detect_cnn_title")
        self.detect_cnn_title.setProperty(u"class", u"modelGroupTitle")

        self.groups_layout.addWidget(self.detect_cnn_title)

        self.detect_cnn_frame = QFrame(self.groups_content)
        self.detect_cnn_frame.setObjectName(u"detect_cnn_frame")
        self.detect_cnn_frame.setProperty(u"class", u"modelGroup")
        self.detect_cnn_layout = QVBoxLayout(self.detect_cnn_frame)
        self.detect_cnn_layout.setSpacing(0)
        self.detect_cnn_layout.setObjectName(u"detect_cnn_layout")
        self.detect_cnn_layout.setContentsMargins(1, 1, 1, 1)

        self.groups_layout.addWidget(self.detect_cnn_frame)

        self.segment_title = QLabel(self.groups_content)
        self.segment_title.setObjectName(u"segment_title")
        self.segment_title.setProperty(u"class", u"modelGroupTitle")

        self.groups_layout.addWidget(self.segment_title)

        self.segment_frame = QFrame(self.groups_content)
        self.segment_frame.setObjectName(u"segment_frame")
        self.segment_frame.setProperty(u"class", u"modelGroup")
        self.segment_layout = QVBoxLayout(self.segment_frame)
        self.segment_layout.setSpacing(0)
        self.segment_layout.setObjectName(u"segment_layout")
        self.segment_layout.setContentsMargins(1, 1, 1, 1)

        self.groups_layout.addWidget(self.segment_frame)

        self.segment_cnn_title = QLabel(self.groups_content)
        self.segment_cnn_title.setObjectName(u"segment_cnn_title")
        self.segment_cnn_title.setProperty(u"class", u"modelGroupTitle")

        self.groups_layout.addWidget(self.segment_cnn_title)

        self.segment_cnn_frame = QFrame(self.groups_content)
        self.segment_cnn_frame.setObjectName(u"segment_cnn_frame")
        self.segment_cnn_frame.setProperty(u"class", u"modelGroup")
        self.segment_cnn_layout = QVBoxLayout(self.segment_cnn_frame)
        self.segment_cnn_layout.setSpacing(0)
        self.segment_cnn_layout.setObjectName(u"segment_cnn_layout")
        self.segment_cnn_layout.setContentsMargins(1, 1, 1, 1)

        self.groups_layout.addWidget(self.segment_cnn_frame)

        self.groups_spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.groups_layout.addItem(self.groups_spacer)

        self.groups_scroll.setWidget(self.groups_content)

        self.root_layout.addWidget(self.groups_scroll)

        self.foot_layout = QHBoxLayout()
        self.foot_layout.setSpacing(8)
        self.foot_layout.setObjectName(u"foot_layout")
        self.dir_title = QLabel(ModelManagerDialog)
        self.dir_title.setObjectName(u"dir_title")
        self.dir_title.setProperty(u"class", u"modelFootLabel")

        self.foot_layout.addWidget(self.dir_title)

        self.dir_label = QLabel(ModelManagerDialog)
        self.dir_label.setObjectName(u"dir_label")
        self.dir_label.setProperty(u"class", u"modelDir")

        self.foot_layout.addWidget(self.dir_label)

        self.change_dir_btn = QPushButton(ModelManagerDialog)
        self.change_dir_btn.setObjectName(u"change_dir_btn")

        self.foot_layout.addWidget(self.change_dir_btn)

        self.foot_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.foot_layout.addItem(self.foot_spacer)

        self.total_label = QLabel(ModelManagerDialog)
        self.total_label.setObjectName(u"total_label")
        self.total_label.setProperty(u"class", u"modelFootLabel")

        self.foot_layout.addWidget(self.total_label)

        self.start_btn = QPushButton(ModelManagerDialog)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setProperty(u"class", u"primary")

        self.foot_layout.addWidget(self.start_btn)

        self.close_btn = QPushButton(ModelManagerDialog)
        self.close_btn.setObjectName(u"close_btn")

        self.foot_layout.addWidget(self.close_btn)


        self.root_layout.addLayout(self.foot_layout)


        self.retranslateUi(ModelManagerDialog)

        QMetaObject.connectSlotsByName(ModelManagerDialog)
    # setupUi

    def retranslateUi(self, ModelManagerDialog):
        ModelManagerDialog.setWindowTitle(QCoreApplication.translate("ModelManagerDialog", u"\u6a21\u578b\u6743\u91cd", None))
        self.detect_title.setText(QCoreApplication.translate("ModelManagerDialog", u"\u76ee\u6807\u68c0\u6d4b \u00b7 Transformer", None))
        self.detect_cnn_title.setText(QCoreApplication.translate("ModelManagerDialog", u"\u76ee\u6807\u68c0\u6d4b \u00b7 CNN", None))
        self.segment_title.setText(QCoreApplication.translate("ModelManagerDialog", u"\u56fe\u50cf\u5206\u5272 \u00b7 Transformer", None))
        self.segment_cnn_title.setText(QCoreApplication.translate("ModelManagerDialog", u"\u56fe\u50cf\u5206\u5272 \u00b7 CNN", None))
        self.dir_title.setText(QCoreApplication.translate("ModelManagerDialog", u"\u4e0b\u8f7d\u76ee\u5f55", None))
        self.change_dir_btn.setText(QCoreApplication.translate("ModelManagerDialog", u"\u66f4\u6539", None))
        self.start_btn.setText(QCoreApplication.translate("ModelManagerDialog", u"\u5f00\u59cb\u4e0b\u8f7d", None))
        self.close_btn.setText(QCoreApplication.translate("ModelManagerDialog", u"\u5173\u95ed", None))
    # retranslateUi

