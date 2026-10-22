# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'backup_restore.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(640, 470)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mode_layout = QHBoxLayout()
        self.mode_layout.setSpacing(12)
        self.mode_layout.setObjectName(u"mode_layout")
        self.bk_mode_backup = QRadioButton(Dialog)
        self.bk_mode_backup.setObjectName(u"bk_mode_backup")
        self.bk_mode_backup.setMinimumSize(QSize(0, 36))
        self.bk_mode_backup.setChecked(True)

        self.mode_layout.addWidget(self.bk_mode_backup)

        self.bk_mode_restore = QRadioButton(Dialog)
        self.bk_mode_restore.setObjectName(u"bk_mode_restore")
        self.bk_mode_restore.setMinimumSize(QSize(0, 36))

        self.mode_layout.addWidget(self.bk_mode_restore)

        self.mode_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.mode_layout.addItem(self.mode_spacer)


        self.verticalLayout_2.addLayout(self.mode_layout)

        self.bk_stack = QStackedWidget(Dialog)
        self.bk_stack.setObjectName(u"bk_stack")
        self.bk_page_backup = QWidget()
        self.bk_page_backup.setObjectName(u"bk_page_backup")
        self.backup_layout = QVBoxLayout(self.bk_page_backup)
        self.backup_layout.setSpacing(8)
        self.backup_layout.setObjectName(u"backup_layout")
        self.bk_content_label = QLabel(self.bk_page_backup)
        self.bk_content_label.setObjectName(u"bk_content_label")

        self.backup_layout.addWidget(self.bk_content_label)

        self.bk_inc_data = QCheckBox(self.bk_page_backup)
        self.bk_inc_data.setObjectName(u"bk_inc_data")
        self.bk_inc_data.setMinimumSize(QSize(0, 32))
        self.bk_inc_data.setChecked(True)

        self.backup_layout.addWidget(self.bk_inc_data)

        self.bk_inc_models = QCheckBox(self.bk_page_backup)
        self.bk_inc_models.setObjectName(u"bk_inc_models")
        self.bk_inc_models.setMinimumSize(QSize(0, 32))
        self.bk_inc_models.setChecked(True)

        self.backup_layout.addWidget(self.bk_inc_models)

        self.bk_inc_queue = QCheckBox(self.bk_page_backup)
        self.bk_inc_queue.setObjectName(u"bk_inc_queue")
        self.bk_inc_queue.setMinimumSize(QSize(0, 32))
        self.bk_inc_queue.setChecked(True)

        self.backup_layout.addWidget(self.bk_inc_queue)

        self.save_row = QHBoxLayout()
        self.save_row.setObjectName(u"save_row")
        self.bk_save_path = QLineEdit(self.bk_page_backup)
        self.bk_save_path.setObjectName(u"bk_save_path")
        self.bk_save_path.setMinimumSize(QSize(300, 40))
        self.bk_save_path.setReadOnly(True)

        self.save_row.addWidget(self.bk_save_path)

        self.bk_browse_btn = QPushButton(self.bk_page_backup)
        self.bk_browse_btn.setObjectName(u"bk_browse_btn")
        self.bk_browse_btn.setMinimumSize(QSize(72, 40))

        self.save_row.addWidget(self.bk_browse_btn)


        self.backup_layout.addLayout(self.save_row)

        self.backup_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.backup_layout.addItem(self.backup_spacer)

        self.bk_stack.addWidget(self.bk_page_backup)
        self.bk_page_restore = QWidget()
        self.bk_page_restore.setObjectName(u"bk_page_restore")
        self.restore_layout = QVBoxLayout(self.bk_page_restore)
        self.restore_layout.setSpacing(8)
        self.restore_layout.setObjectName(u"restore_layout")
        self.pkg_row = QHBoxLayout()
        self.pkg_row.setObjectName(u"pkg_row")
        self.bk_pkg_path = QLineEdit(self.bk_page_restore)
        self.bk_pkg_path.setObjectName(u"bk_pkg_path")
        self.bk_pkg_path.setMinimumSize(QSize(300, 40))
        self.bk_pkg_path.setReadOnly(True)

        self.pkg_row.addWidget(self.bk_pkg_path)

        self.bk_pkg_btn = QPushButton(self.bk_page_restore)
        self.bk_pkg_btn.setObjectName(u"bk_pkg_btn")
        self.bk_pkg_btn.setMinimumSize(QSize(72, 40))

        self.pkg_row.addWidget(self.bk_pkg_btn)


        self.restore_layout.addLayout(self.pkg_row)

        self.bk_summary = QLabel(self.bk_page_restore)
        self.bk_summary.setObjectName(u"bk_summary")
        self.bk_summary.setMinimumSize(QSize(0, 120))
        self.bk_summary.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bk_summary.setWordWrap(True)

        self.restore_layout.addWidget(self.bk_summary)

        self.restore_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.restore_layout.addItem(self.restore_spacer)

        self.bk_stack.addWidget(self.bk_page_restore)

        self.verticalLayout_2.addWidget(self.bk_stack)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setObjectName(u"bottom_row")
        self.bottom_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer)

        self.bk_cancel_btn = QPushButton(Dialog)
        self.bk_cancel_btn.setObjectName(u"bk_cancel_btn")
        self.bk_cancel_btn.setMinimumSize(QSize(80, 40))

        self.bottom_row.addWidget(self.bk_cancel_btn)

        self.bk_ok_btn = QPushButton(Dialog)
        self.bk_ok_btn.setObjectName(u"bk_ok_btn")
        self.bk_ok_btn.setMinimumSize(QSize(80, 40))

        self.bottom_row.addWidget(self.bk_ok_btn)


        self.verticalLayout_2.addLayout(self.bottom_row)


        self.retranslateUi(Dialog)

        self.bk_stack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u9879\u76ee\u5907\u4efd/\u6062\u590d", None))
        self.bk_mode_backup.setText(QCoreApplication.translate("Dialog", u"\u5907\u4efd\u9879\u76ee", None))
        self.bk_mode_restore.setText(QCoreApplication.translate("Dialog", u"\u6062\u590d\u9879\u76ee", None))
        self.bk_content_label.setText(QCoreApplication.translate("Dialog", u"\u5907\u4efd\u5185\u5bb9", None))
        self.bk_inc_data.setText(QCoreApplication.translate("Dialog", u"\u6570\u636e\u96c6\u6570\u636e(\u56fe\u50cf\u4e0e\u6807\u6ce8, \u4f53\u79ef\u6700\u5927)", None))
        self.bk_inc_models.setText(QCoreApplication.translate("Dialog", u"\u6a21\u578b\u6743\u91cd\u4e0e\u8bad\u7ec3\u4ea7\u7269", None))
        self.bk_inc_queue.setText(QCoreApplication.translate("Dialog", u"\u672a\u5f00\u59cb\u7684\u8bad\u7ec3\u961f\u5217", None))
        self.bk_save_path.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u5907\u4efd\u4fdd\u5b58\u4f4d\u7f6e", None))
        self.bk_browse_btn.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8", None))
        self.bk_pkg_path.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u5907\u4efd\u5305(.etbak)", None))
        self.bk_pkg_btn.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8", None))
        self.bk_summary.setText(QCoreApplication.translate("Dialog", u"\u9009\u62e9\u5907\u4efd\u5305\u540e\u663e\u793a\u6458\u8981", None))
        self.bk_cancel_btn.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
        self.bk_ok_btn.setText("")
    # retranslateUi

