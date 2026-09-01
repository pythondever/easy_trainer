# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_label.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_addLabelDialog(object):
    def setupUi(self, addLabelDialog):
        if not addLabelDialog.objectName():
            addLabelDialog.setObjectName(u"addLabelDialog")
        addLabelDialog.resize(478, 300)
        self.gridLayout = QGridLayout(addLabelDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.input_label_name_txt = QLineEdit(addLabelDialog)
        self.input_label_name_txt.setObjectName(u"input_label_name_txt")

        self.horizontalLayout_5.addWidget(self.input_label_name_txt)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_5.setStretch(0, 8)
        self.horizontalLayout_5.setStretch(1, 2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.load_project_label_combo = QComboBox(addLabelDialog)
        self.load_project_label_combo.setObjectName(u"load_project_label_combo")
        self.load_project_label_combo.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_6.addWidget(self.load_project_label_combo)

        self.load_label_btn = QPushButton(addLabelDialog)
        self.load_label_btn.setObjectName(u"load_label_btn")

        self.horizontalLayout_6.addWidget(self.load_label_btn)

        self.horizontalLayout_6.setStretch(0, 8)
        self.horizontalLayout_6.setStretch(1, 2)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.color1_btn = QPushButton(addLabelDialog)
        self.color1_btn.setObjectName(u"color1_btn")

        self.horizontalLayout.addWidget(self.color1_btn)

        self.color2_btn = QPushButton(addLabelDialog)
        self.color2_btn.setObjectName(u"color2_btn")

        self.horizontalLayout.addWidget(self.color2_btn)

        self.color3_btn = QPushButton(addLabelDialog)
        self.color3_btn.setObjectName(u"color3_btn")

        self.horizontalLayout.addWidget(self.color3_btn)

        self.color4_btn = QPushButton(addLabelDialog)
        self.color4_btn.setObjectName(u"color4_btn")

        self.horizontalLayout.addWidget(self.color4_btn)

        self.color5_btn = QPushButton(addLabelDialog)
        self.color5_btn.setObjectName(u"color5_btn")

        self.horizontalLayout.addWidget(self.color5_btn)

        self.color7_btn = QPushButton(addLabelDialog)
        self.color7_btn.setObjectName(u"color7_btn")

        self.horizontalLayout.addWidget(self.color7_btn)

        self.color6_btn = QPushButton(addLabelDialog)
        self.color6_btn.setObjectName(u"color6_btn")

        self.horizontalLayout.addWidget(self.color6_btn)

        self.color10_btn = QPushButton(addLabelDialog)
        self.color10_btn.setObjectName(u"color10_btn")

        self.horizontalLayout.addWidget(self.color10_btn)

        self.color9_btn = QPushButton(addLabelDialog)
        self.color9_btn.setObjectName(u"color9_btn")

        self.horizontalLayout.addWidget(self.color9_btn)

        self.color8_btn = QPushButton(addLabelDialog)
        self.color8_btn.setObjectName(u"color8_btn")

        self.horizontalLayout.addWidget(self.color8_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.custom_color = QPushButton(addLabelDialog)
        self.custom_color.setObjectName(u"custom_color")

        self.horizontalLayout_3.addWidget(self.custom_color)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.add_label_done_btn = QPushButton(addLabelDialog)
        self.add_label_done_btn.setObjectName(u"add_label_done_btn")

        self.horizontalLayout_4.addWidget(self.add_label_done_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.retranslateUi(addLabelDialog)

        QMetaObject.connectSlotsByName(addLabelDialog)
    # setupUi

    def retranslateUi(self, addLabelDialog):
        addLabelDialog.setWindowTitle(QCoreApplication.translate("addLabelDialog", u"Dialog", None))
        self.load_label_btn.setText(QCoreApplication.translate("addLabelDialog", u"\u5bfc\u5165", None))
        self.color1_btn.setText("")
        self.color2_btn.setText("")
        self.color3_btn.setText("")
        self.color4_btn.setText("")
        self.color5_btn.setText("")
        self.color7_btn.setText("")
        self.color6_btn.setText("")
        self.color10_btn.setText("")
        self.color9_btn.setText("")
        self.color8_btn.setText("")
        self.custom_color.setText(QCoreApplication.translate("addLabelDialog", u"\u81ea\u5b9a\u4e49\u989c\u8272", None))
        self.add_label_done_btn.setText(QCoreApplication.translate("addLabelDialog", u"\u786e\u5b9a", None))
    # retranslateUi

