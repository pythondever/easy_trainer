# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'compare.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSplitter, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_CompareDialog(object):
    def setupUi(self, CompareDialog):
        if not CompareDialog.objectName():
            CompareDialog.setObjectName(u"CompareDialog")
        CompareDialog.resize(1320, 680)
        self.verticalLayout = QVBoxLayout(CompareDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.setObjectName(u"toolbarLayout")
        self.metric_caption = QLabel(CompareDialog)
        self.metric_caption.setObjectName(u"metric_caption")

        self.toolbarLayout.addWidget(self.metric_caption)

        self.metric_tabs_host = QWidget(CompareDialog)
        self.metric_tabs_host.setObjectName(u"metric_tabs_host")
        self.metricTabsLayout = QHBoxLayout(self.metric_tabs_host)
        self.metricTabsLayout.setSpacing(0)
        self.metricTabsLayout.setObjectName(u"metricTabsLayout")

        self.toolbarLayout.addWidget(self.metric_tabs_host)

        self.range_caption = QLabel(CompareDialog)
        self.range_caption.setObjectName(u"range_caption")

        self.toolbarLayout.addWidget(self.range_caption)

        self.record_range_combo = QComboBox(CompareDialog)
        self.record_range_combo.setObjectName(u"record_range_combo")
        self.record_range_combo.setMinimumWidth(120)

        self.toolbarLayout.addWidget(self.record_range_combo)

        self.toolbar_spacer_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbarLayout.addItem(self.toolbar_spacer_right)

        self.export_report_btn = QPushButton(CompareDialog)
        self.export_report_btn.setObjectName(u"export_report_btn")

        self.toolbarLayout.addWidget(self.export_report_btn)

        self.delete_selected_btn = QPushButton(CompareDialog)
        self.delete_selected_btn.setObjectName(u"delete_selected_btn")

        self.toolbarLayout.addWidget(self.delete_selected_btn)


        self.verticalLayout.addLayout(self.toolbarLayout)

        self.main_splitter = QSplitter(CompareDialog)
        self.main_splitter.setObjectName(u"main_splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.main_splitter.sizePolicy().hasHeightForWidth())
        self.main_splitter.setSizePolicy(sizePolicy)
        self.main_splitter.setOrientation(Qt.Horizontal)
        self.left_panel = QWidget(self.main_splitter)
        self.left_panel.setObjectName(u"left_panel")
        self.leftLayout = QVBoxLayout(self.left_panel)
        self.leftLayout.setSpacing(6)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.records_caption = QLabel(self.left_panel)
        self.records_caption.setObjectName(u"records_caption")

        self.leftLayout.addWidget(self.records_caption)

        self.record_list = QListWidget(self.left_panel)
        self.record_list.setObjectName(u"record_list")
        self.record_list.setMinimumSize(QSize(240, 0))
        self.record_list.setMaximumSize(QSize(340, 16777215))

        self.leftLayout.addWidget(self.record_list)

        self.selected_count_label = QLabel(self.left_panel)
        self.selected_count_label.setObjectName(u"selected_count_label")

        self.leftLayout.addWidget(self.selected_count_label)

        self.main_splitter.addWidget(self.left_panel)
        self.center_panel = QWidget(self.main_splitter)
        self.center_panel.setObjectName(u"center_panel")
        self.centerLayout = QVBoxLayout(self.center_panel)
        self.centerLayout.setObjectName(u"centerLayout")
        self.centerLayout.setContentsMargins(0, 0, 0, 0)
        self.chart_card = QFrame(self.center_panel)
        self.chart_card.setObjectName(u"chart_card")
        self.chart_card.setFrameShape(QFrame.StyledPanel)
        self.chartCardLayout = QVBoxLayout(self.chart_card)
        self.chartCardLayout.setObjectName(u"chartCardLayout")
        self.chart_title_label = QLabel(self.chart_card)
        self.chart_title_label.setObjectName(u"chart_title_label")

        self.chartCardLayout.addWidget(self.chart_title_label)

        self.chart_container = QWidget(self.chart_card)
        self.chart_container.setObjectName(u"chart_container")
        self.chartLayout = QVBoxLayout(self.chart_container)
        self.chartLayout.setObjectName(u"chartLayout")

        self.chartCardLayout.addWidget(self.chart_container)

        self.legend_label = QLabel(self.chart_card)
        self.legend_label.setObjectName(u"legend_label")
        self.legend_label.setWordWrap(True)

        self.chartCardLayout.addWidget(self.legend_label)


        self.centerLayout.addWidget(self.chart_card)

        self.table_card = QFrame(self.center_panel)
        self.table_card.setObjectName(u"table_card")
        self.table_card.setFrameShape(QFrame.StyledPanel)
        self.tableCardLayout = QVBoxLayout(self.table_card)
        self.tableCardLayout.setObjectName(u"tableCardLayout")
        self.table_title_label = QLabel(self.table_card)
        self.table_title_label.setObjectName(u"table_title_label")

        self.tableCardLayout.addWidget(self.table_title_label)

        self.summary_table = QTableWidget(self.table_card)
        self.summary_table.setObjectName(u"summary_table")

        self.tableCardLayout.addWidget(self.summary_table)


        self.centerLayout.addWidget(self.table_card)

        self.main_splitter.addWidget(self.center_panel)
        self.diff_panel = QWidget(self.main_splitter)
        self.diff_panel.setObjectName(u"diff_panel")
        self.diffPanelLayout = QVBoxLayout(self.diff_panel)
        self.diffPanelLayout.setSpacing(6)
        self.diffPanelLayout.setObjectName(u"diffPanelLayout")
        self.diffPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.diff_caption = QLabel(self.diff_panel)
        self.diff_caption.setObjectName(u"diff_caption")

        self.diffPanelLayout.addWidget(self.diff_caption)

        self.diff_scroll = QScrollArea(self.diff_panel)
        self.diff_scroll.setObjectName(u"diff_scroll")
        self.diff_scroll.setWidgetResizable(True)
        self.diff_scroll.setFrameShape(QFrame.NoFrame)
        self.diff_content = QWidget()
        self.diff_content.setObjectName(u"diff_content")
        self.diff_content.setGeometry(QRect(0, 0, 300, 540))
        self.diffLayout = QVBoxLayout(self.diff_content)
        self.diffLayout.setObjectName(u"diffLayout")
        self.diff_scroll.setWidget(self.diff_content)

        self.diffPanelLayout.addWidget(self.diff_scroll)

        self.main_splitter.addWidget(self.diff_panel)

        self.verticalLayout.addWidget(self.main_splitter)

        self.footerLayout = QHBoxLayout()
        self.footerLayout.setObjectName(u"footerLayout")
        self.status_legend_label = QLabel(CompareDialog)
        self.status_legend_label.setObjectName(u"status_legend_label")

        self.footerLayout.addWidget(self.status_legend_label)

        self.source_label = QLabel(CompareDialog)
        self.source_label.setObjectName(u"source_label")

        self.footerLayout.addWidget(self.source_label)

        self.footer_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerLayout.addItem(self.footer_spacer)

        self.hint_label = QLabel(CompareDialog)
        self.hint_label.setObjectName(u"hint_label")

        self.footerLayout.addWidget(self.hint_label)


        self.verticalLayout.addLayout(self.footerLayout)


        self.retranslateUi(CompareDialog)

        QMetaObject.connectSlotsByName(CompareDialog)
    # setupUi

    def retranslateUi(self, CompareDialog):
        CompareDialog.setWindowTitle(QCoreApplication.translate("CompareDialog", u"\u5bf9\u6bd4\u591a\u6b21\u8bad\u7ec3", None))
        self.metric_caption.setText(QCoreApplication.translate("CompareDialog", u"\u5bf9\u6bd4\u6307\u6807", None))
        self.range_caption.setText(QCoreApplication.translate("CompareDialog", u"\u8bb0\u5f55\u8303\u56f4", None))
        self.export_report_btn.setText(QCoreApplication.translate("CompareDialog", u"\u5bfc\u51fa\u5bf9\u6bd4\u62a5\u544a", None))
        self.delete_selected_btn.setText(QCoreApplication.translate("CompareDialog", u"\u5220\u9664\u9009\u4e2d", None))
        self.records_caption.setText(QCoreApplication.translate("CompareDialog", u"\u8bad\u7ec3\u8bb0\u5f55\uff08\u53ef\u52fe\u9009\uff0c\u4e0a\u9650 8 \u6761\uff09", None))
        self.selected_count_label.setText("")
        self.chart_title_label.setText("")
        self.legend_label.setText("")
        self.table_title_label.setText(QCoreApplication.translate("CompareDialog", u"\u5173\u952e\u6307\u6807\u6c47\u603b", None))
        self.diff_caption.setText(QCoreApplication.translate("CompareDialog", u"\u5dee\u5f02\u4e0e\u7ed3\u8bba", None))
        self.status_legend_label.setText("")
        self.source_label.setText("")
        self.hint_label.setText("")
    # retranslateUi

