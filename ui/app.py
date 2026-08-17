# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTabWidget,
    QTimeEdit, QVBoxLayout, QWidget)

class Ui_AppUI(object):
    def setupUi(self, AppUI):
        if not AppUI.objectName():
            AppUI.setObjectName(u"AppUI")
        AppUI.resize(1269, 780)
        self.rootLayout = QVBoxLayout(AppUI)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.headerBar = QFrame(AppUI)
        self.headerBar.setObjectName(u"headerBar")
        self.headerBar.setMinimumSize(QSize(0, 56))
        self.headerBar.setMaximumSize(QSize(16777215, 56))
        self.headerLayout = QHBoxLayout(self.headerBar)
        self.headerLayout.setSpacing(12)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(20, 0, 20, 0)
        self.appLogoLabel = QLabel(self.headerBar)
        self.appLogoLabel.setObjectName(u"appLogoLabel")
        self.appLogoLabel.setMinimumSize(QSize(28, 28))
        self.appLogoLabel.setMaximumSize(QSize(28, 28))
        self.appLogoLabel.setScaledContents(True)

        self.headerLayout.addWidget(self.appLogoLabel)

        self.appTitle = QLabel(self.headerBar)
        self.appTitle.setObjectName(u"appTitle")

        self.headerLayout.addWidget(self.appTitle)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)


        self.rootLayout.addWidget(self.headerBar)

        self.tabWidget = QTabWidget(AppUI)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_project = QWidget()
        self.tab_project.setObjectName(u"tab_project")
        self.projectTabLayout = QHBoxLayout(self.tab_project)
        self.projectTabLayout.setSpacing(0)
        self.projectTabLayout.setObjectName(u"projectTabLayout")
        self.projectTabLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebarPanel = QFrame(self.tab_project)
        self.sidebarPanel.setObjectName(u"sidebarPanel")
        self.sidebarPanel.setMinimumSize(QSize(280, 0))
        self.sidebarPanel.setMaximumSize(QSize(280, 16777215))
        self.sidebarLayout = QVBoxLayout(self.sidebarPanel)
        self.sidebarLayout.setSpacing(10)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(14, 16, 14, 14)
        self.sidebarTitle = QLabel(self.sidebarPanel)
        self.sidebarTitle.setObjectName(u"sidebarTitle")

        self.sidebarLayout.addWidget(self.sidebarTitle)

        self.add_project_btn = QPushButton(self.sidebarPanel)
        self.add_project_btn.setObjectName(u"add_project_btn")
        self.add_project_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.sidebarLayout.addWidget(self.add_project_btn)

        self.project_scroll_area = QScrollArea(self.sidebarPanel)
        self.project_scroll_area.setObjectName(u"project_scroll_area")
        self.project_scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 250, 606))
        self.project_list_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.project_list_layout.setSpacing(6)
        self.project_list_layout.setObjectName(u"project_list_layout")
        self.project_list_layout.setContentsMargins(0, 0, 0, 0)
        self.projectListSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.project_list_layout.addItem(self.projectListSpacer)

        self.project_scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.sidebarLayout.addWidget(self.project_scroll_area)


        self.projectTabLayout.addWidget(self.sidebarPanel)

        self.mainContent = QFrame(self.tab_project)
        self.mainContent.setObjectName(u"mainContent")
        self.mainContentLayout = QVBoxLayout(self.mainContent)
        self.mainContentLayout.setSpacing(12)
        self.mainContentLayout.setObjectName(u"mainContentLayout")
        self.mainContentLayout.setContentsMargins(20, 16, 20, 0)
        self.datasetHeader = QFrame(self.mainContent)
        self.datasetHeader.setObjectName(u"datasetHeader")
        self.datasetHeader.setMinimumSize(QSize(0, 40))
        self.datasetHeader.setMaximumSize(QSize(16777215, 40))
        self.datasetHeaderLayout = QHBoxLayout(self.datasetHeader)
        self.datasetHeaderLayout.setSpacing(8)
        self.datasetHeaderLayout.setObjectName(u"datasetHeaderLayout")
        self.datasetHeaderLayout.setContentsMargins(0, 0, 0, 0)
        self.datasetTitleLabel = QLabel(self.datasetHeader)
        self.datasetTitleLabel.setObjectName(u"datasetTitleLabel")

        self.datasetHeaderLayout.addWidget(self.datasetTitleLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.datasetHeaderLayout.addItem(self.horizontalSpacer_2)

        self.task_name_label = QLabel(self.datasetHeader)
        self.task_name_label.setObjectName(u"task_name_label")

        self.datasetHeaderLayout.addWidget(self.task_name_label)

        self.labelStatsLabel = QLabel(self.datasetHeader)
        self.labelStatsLabel.setObjectName(u"labelStatsLabel")
        self.labelStatsLabel.setVisible(False)

        self.datasetHeaderLayout.addWidget(self.labelStatsLabel)

        self.train_progress = QProgressBar(self.datasetHeader)
        self.train_progress.setObjectName(u"train_progress")
        self.train_progress.setValue(24)

        self.datasetHeaderLayout.addWidget(self.train_progress)

        self.stop_train_btn = QPushButton(self.datasetHeader)
        self.stop_train_btn.setObjectName(u"stop_train_btn")
        self.stop_train_btn.setEnabled(True)
        self.stop_train_btn.setVisible(False)

        self.datasetHeaderLayout.addWidget(self.stop_train_btn)

        self.time_count_label = QLabel(self.datasetHeader)
        self.time_count_label.setObjectName(u"time_count_label")

        self.datasetHeaderLayout.addWidget(self.time_count_label)

        self.time_count_edit = QTimeEdit(self.datasetHeader)
        self.time_count_edit.setObjectName(u"time_count_edit")

        self.datasetHeaderLayout.addWidget(self.time_count_edit)

        self.gpu_memory_label = QLabel(self.datasetHeader)
        self.gpu_memory_label.setObjectName(u"gpu_memory_label")

        self.datasetHeaderLayout.addWidget(self.gpu_memory_label)

        self.gpu_memory_use_btn = QPushButton(self.datasetHeader)
        self.gpu_memory_use_btn.setObjectName(u"gpu_memory_use_btn")

        self.datasetHeaderLayout.addWidget(self.gpu_memory_use_btn)

        self.label_comboBox = QComboBox(self.datasetHeader)
        self.label_comboBox.setObjectName(u"label_comboBox")

        self.datasetHeaderLayout.addWidget(self.label_comboBox)

        self.rename_label_btn = QPushButton(self.datasetHeader)
        self.rename_label_btn.setObjectName(u"rename_label_btn")

        self.datasetHeaderLayout.addWidget(self.rename_label_btn)

        self.delete_label_btn = QPushButton(self.datasetHeader)
        self.delete_label_btn.setObjectName(u"delete_label_btn")

        self.datasetHeaderLayout.addWidget(self.delete_label_btn)

        self.import_dataset_btn = QPushButton(self.datasetHeader)
        self.import_dataset_btn.setObjectName(u"import_dataset_btn")

        self.datasetHeaderLayout.addWidget(self.import_dataset_btn)

        self.export_dataset_btn = QPushButton(self.datasetHeader)
        self.export_dataset_btn.setObjectName(u"export_dataset_btn")

        self.datasetHeaderLayout.addWidget(self.export_dataset_btn)

        self.dataset_properties_btn = QPushButton(self.datasetHeader)
        self.dataset_properties_btn.setObjectName(u"dataset_properties_btn")

        self.datasetHeaderLayout.addWidget(self.dataset_properties_btn)

        self.train_btn = QPushButton(self.datasetHeader)
        self.train_btn.setObjectName(u"train_btn")

        self.datasetHeaderLayout.addWidget(self.train_btn)

        self.model_btn = QPushButton(self.datasetHeader)
        self.model_btn.setObjectName(u"model_btn")

        self.datasetHeaderLayout.addWidget(self.model_btn)

        self.log_btn = QPushButton(self.datasetHeader)
        self.log_btn.setObjectName(u"log_btn")

        self.datasetHeaderLayout.addWidget(self.log_btn)


        self.mainContentLayout.addWidget(self.datasetHeader)

        self.thumbnailsLayout = QVBoxLayout()
        self.thumbnailsLayout.setObjectName(u"thumbnailsLayout")
        self.thumbnailsLayout.setContentsMargins(0, 0, 0, 0)
        self.thumbnailsSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.thumbnailsLayout.addItem(self.thumbnailsSpacer)


        self.mainContentLayout.addLayout(self.thumbnailsLayout)

        self.bottomBar = QFrame(self.mainContent)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 48))
        self.bottomBar.setMaximumSize(QSize(16777215, 48))
        self.bottomBarLayout = QHBoxLayout(self.bottomBar)
        self.bottomBarLayout.setObjectName(u"bottomBarLayout")
        self.bottomBarLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomBarLeftSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomBarLayout.addItem(self.bottomBarLeftSpacer)

        self.pageInfoLabel = QLabel(self.bottomBar)
        self.pageInfoLabel.setObjectName(u"pageInfoLabel")

        self.bottomBarLayout.addWidget(self.pageInfoLabel)

        self.pre_page_btn = QPushButton(self.bottomBar)
        self.pre_page_btn.setObjectName(u"pre_page_btn")

        self.bottomBarLayout.addWidget(self.pre_page_btn)

        self.next_page_btn = QPushButton(self.bottomBar)
        self.next_page_btn.setObjectName(u"next_page_btn")

        self.bottomBarLayout.addWidget(self.next_page_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomBarLayout.addItem(self.horizontalSpacer)


        self.mainContentLayout.addWidget(self.bottomBar)


        self.projectTabLayout.addWidget(self.mainContent)

        self.tabWidget.addTab(self.tab_project, "")

        self.rootLayout.addWidget(self.tabWidget)


        self.retranslateUi(AppUI)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AppUI)
    # setupUi

    def retranslateUi(self, AppUI):
        AppUI.setWindowTitle(QCoreApplication.translate("AppUI", u"EasyTrainer", None))
        self.appLogoLabel.setText("")
        self.appTitle.setText(QCoreApplication.translate("AppUI", u"EasyTrainer", None))
        self.sidebarTitle.setText(QCoreApplication.translate("AppUI", u"\u9879\u76ee", None))
        self.add_project_btn.setText(QCoreApplication.translate("AppUI", u"+ \u6dfb\u52a0\u9879\u76ee", None))
        self.datasetTitleLabel.setText("")
        self.task_name_label.setText(QCoreApplication.translate("AppUI", u"\u9879\u76ee\u8bad\u7ec3\u4e2d", None))
        self.labelStatsLabel.setText("")
        self.stop_train_btn.setText(QCoreApplication.translate("AppUI", u"\u505c\u6b62\u8bad\u7ec3", None))
        self.time_count_label.setText(QCoreApplication.translate("AppUI", u"\u5269\u4f59\u65f6\u95f4:", None))
        self.gpu_memory_label.setText(QCoreApplication.translate("AppUI", u"\u663e\u5b58:", None))
        self.gpu_memory_use_btn.setText(QCoreApplication.translate("AppUI", u"20%", None))
        self.rename_label_btn.setText(QCoreApplication.translate("AppUI", u"\u7f16\u8f91", None))
        self.delete_label_btn.setText(QCoreApplication.translate("AppUI", u"\u5220\u9664", None))
        self.import_dataset_btn.setText(QCoreApplication.translate("AppUI", u"\u5bfc\u5165", None))
        self.export_dataset_btn.setText(QCoreApplication.translate("AppUI", u"\u5bfc\u51fa", None))
        self.dataset_properties_btn.setText(QCoreApplication.translate("AppUI", u"\u5c5e\u6027", None))
        self.train_btn.setText(QCoreApplication.translate("AppUI", u"\u8bad\u7ec3", None))
        self.model_btn.setText(QCoreApplication.translate("AppUI", u"\u6a21\u578b", None))
        self.log_btn.setText(QCoreApplication.translate("AppUI", u"\u65e5\u5fd7", None))
        self.pageInfoLabel.setText(QCoreApplication.translate("AppUI", u"0 / 0", None))
        self.pre_page_btn.setText(QCoreApplication.translate("AppUI", u"\u4e0a\u4e00\u9875", None))
        self.next_page_btn.setText(QCoreApplication.translate("AppUI", u"\u4e0b\u4e00\u9875", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_project), QCoreApplication.translate("AppUI", u"\u9879\u76ee", None))
    # retranslateUi

