# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'train_queue.ui'
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
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_TrainQueueDialog(object):
    def setupUi(self, TrainQueueDialog):
        if not TrainQueueDialog.objectName():
            TrainQueueDialog.setObjectName(u"TrainQueueDialog")
        TrainQueueDialog.resize(900, 600)
        self.mainLayout = QVBoxLayout(TrainQueueDialog)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 18)
        self.title_row = QHBoxLayout()
        self.title_row.setSpacing(10)
        self.title_row.setObjectName(u"title_row")
        self.title_label = QLabel(TrainQueueDialog)
        self.title_label.setObjectName(u"title_label")

        self.title_row.addWidget(self.title_label)

        self.queue_badge = QLabel(TrainQueueDialog)
        self.queue_badge.setObjectName(u"queue_badge")

        self.title_row.addWidget(self.queue_badge)

        self.title_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.title_row.addItem(self.title_spacer)


        self.mainLayout.addLayout(self.title_row)

        self.queue_table = QTableWidget(TrainQueueDialog)
        if (self.queue_table.columnCount() < 7):
            self.queue_table.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.queue_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.queue_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.queue_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.queue_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.queue_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.queue_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.queue_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        if (self.queue_table.rowCount() < 1):
            self.queue_table.setRowCount(1)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.queue_table.setVerticalHeaderItem(0, __qtablewidgetitem7)
        self.queue_table.setObjectName(u"queue_table")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queue_table.sizePolicy().hasHeightForWidth())
        self.queue_table.setSizePolicy(sizePolicy)
        self.queue_table.horizontalHeader().setVisible(True)
        self.queue_table.verticalHeader().setVisible(False)

        self.mainLayout.addWidget(self.queue_table)

        self.summary_bar = QFrame(TrainQueueDialog)
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

        self.button_line = QFrame(TrainQueueDialog)
        self.button_line.setObjectName(u"button_line")
        self.button_line.setFrameShape(QFrame.HLine)
        self.button_line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addWidget(self.button_line)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setSpacing(8)
        self.bottom_row.setObjectName(u"bottom_row")
        self.move_up_btn = QPushButton(TrainQueueDialog)
        self.move_up_btn.setObjectName(u"move_up_btn")

        self.bottom_row.addWidget(self.move_up_btn)

        self.move_down_btn = QPushButton(TrainQueueDialog)
        self.move_down_btn.setObjectName(u"move_down_btn")

        self.bottom_row.addWidget(self.move_down_btn)

        self.remove_btn = QPushButton(TrainQueueDialog)
        self.remove_btn.setObjectName(u"remove_btn")

        self.bottom_row.addWidget(self.remove_btn)

        self.clear_done_btn = QPushButton(TrainQueueDialog)
        self.clear_done_btn.setObjectName(u"clear_done_btn")

        self.bottom_row.addWidget(self.clear_done_btn)

        self.bottom_spacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottom_row.addItem(self.bottom_spacer_left)

        self.edit_btn = QPushButton(TrainQueueDialog)
        self.edit_btn.setObjectName(u"edit_btn")

        self.bottom_row.addWidget(self.edit_btn)

        self.close_btn = QPushButton(TrainQueueDialog)
        self.close_btn.setObjectName(u"close_btn")

        self.bottom_row.addWidget(self.close_btn)

        self.start_btn = QPushButton(TrainQueueDialog)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setMinimumSize(QSize(120, 38))

        self.bottom_row.addWidget(self.start_btn)


        self.mainLayout.addLayout(self.bottom_row)


        self.retranslateUi(TrainQueueDialog)

        QMetaObject.connectSlotsByName(TrainQueueDialog)
    # setupUi

    def retranslateUi(self, TrainQueueDialog):
        TrainQueueDialog.setWindowTitle(QCoreApplication.translate("TrainQueueDialog", u"\u8bad\u7ec3\u961f\u5217", None))
        self.title_label.setText(QCoreApplication.translate("TrainQueueDialog", u"\u8bad\u7ec3\u961f\u5217", None))
        self.title_label.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"dialogTitle", None))
        self.queue_badge.setText(QCoreApplication.translate("TrainQueueDialog", u"\u7a7a\u95f2", None))
        self.queue_badge.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"taskBadge", None))
        ___qtablewidgetitem = self.queue_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("TrainQueueDialog", u"#", None))
        ___qtablewidgetitem1 = self.queue_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("TrainQueueDialog", u"\u540d\u79f0", None))
        ___qtablewidgetitem2 = self.queue_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("TrainQueueDialog", u"\u4efb\u52a1", None))
        ___qtablewidgetitem3 = self.queue_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("TrainQueueDialog", u"\u6570\u636e\u96c6", None))
        ___qtablewidgetitem4 = self.queue_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("TrainQueueDialog", u"\u7f51\u7edc", None))
        ___qtablewidgetitem5 = self.queue_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("TrainQueueDialog", u"\u8f6e\u6b21", None))
        ___qtablewidgetitem6 = self.queue_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("TrainQueueDialog", u"\u72b6\u6001", None))
        self.summary_icon.setText(QCoreApplication.translate("TrainQueueDialog", u"i", None))
        self.summary_icon.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"summaryIcon", None))
        self.summary_text.setText(QCoreApplication.translate("TrainQueueDialog", u"\u961f\u5217\u4e3a\u7a7a\uff0c\u53ef\u5728\u8bad\u7ec3\u754c\u9762\u70b9\u300c\u52a0\u5165\u961f\u5217\u300d\u6dfb\u52a0\u4efb\u52a1", None))
        self.summary_text.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"summaryText", None))
        self.move_up_btn.setText(QCoreApplication.translate("TrainQueueDialog", u"\u4e0a\u79fb", None))
        self.move_up_btn.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"ghost", None))
        self.move_down_btn.setText(QCoreApplication.translate("TrainQueueDialog", u"\u4e0b\u79fb", None))
        self.move_down_btn.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"ghost", None))
        self.remove_btn.setText(QCoreApplication.translate("TrainQueueDialog", u"\u79fb\u9664", None))
        self.remove_btn.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"ghost", None))
        self.clear_done_btn.setText(QCoreApplication.translate("TrainQueueDialog", u"\u6e05\u7406\u5df2\u5b8c\u6210", None))
        self.clear_done_btn.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"ghost", None))
        self.edit_btn.setText(QCoreApplication.translate("TrainQueueDialog", u"\u7f16\u8f91", None))
        self.close_btn.setText(QCoreApplication.translate("TrainQueueDialog", u"\u5173\u95ed", None))
        self.start_btn.setText(QCoreApplication.translate("TrainQueueDialog", u"\u5f00\u59cb\u961f\u5217", None))
        self.start_btn.setProperty(u"class", QCoreApplication.translate("TrainQueueDialog", u"primary", None))
    # retranslateUi

