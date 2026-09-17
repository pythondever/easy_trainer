# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'annotation.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGraphicsView,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_annotationDialog(object):
    def setupUi(self, annotationDialog):
        if not annotationDialog.objectName():
            annotationDialog.setObjectName(u"annotationDialog")
        annotationDialog.resize(1068, 703)
        self.paramsPanel = QFrame(annotationDialog)
        self.paramsPanel.setObjectName(u"paramsPanel")
        self.paramsPanel.setGeometry(QRect(640, 90, 360, 244))
        self.verticalLayout_params = QVBoxLayout(self.paramsPanel)
        self.verticalLayout_params.setSpacing(10)
        self.verticalLayout_params.setObjectName(u"verticalLayout_params")
        self.verticalLayout_params.setContentsMargins(14, 14, 14, 14)
        self.params_title = QLabel(self.paramsPanel)
        self.params_title.setObjectName(u"params_title")

        self.verticalLayout_params.addWidget(self.params_title)

        self.params_row_angle = QHBoxLayout()
        self.params_row_angle.setObjectName(u"params_row_angle")
        self.params_angle_label = QLabel(self.paramsPanel)
        self.params_angle_label.setObjectName(u"params_angle_label")
        self.params_angle_label.setMinimumSize(QSize(64, 0))

        self.params_row_angle.addWidget(self.params_angle_label)

        self.min_ange_lineEdit = QLineEdit(self.paramsPanel)
        self.min_ange_lineEdit.setObjectName(u"min_ange_lineEdit")
        self.min_ange_lineEdit.setMinimumSize(QSize(62, 0))

        self.params_row_angle.addWidget(self.min_ange_lineEdit)

        self.label = QLabel(self.paramsPanel)
        self.label.setObjectName(u"label")

        self.params_row_angle.addWidget(self.label)

        self.max_ange_lineEdit = QLineEdit(self.paramsPanel)
        self.max_ange_lineEdit.setObjectName(u"max_ange_lineEdit")
        self.max_ange_lineEdit.setMinimumSize(QSize(62, 0))

        self.params_row_angle.addWidget(self.max_ange_lineEdit)

        self.params_spacer_angle = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.params_row_angle.addItem(self.params_spacer_angle)


        self.verticalLayout_params.addLayout(self.params_row_angle)

        self.params_row_blend = QHBoxLayout()
        self.params_row_blend.setObjectName(u"params_row_blend")
        self.blend_strength_label = QLabel(self.paramsPanel)
        self.blend_strength_label.setObjectName(u"blend_strength_label")
        self.blend_strength_label.setMinimumSize(QSize(64, 0))

        self.params_row_blend.addWidget(self.blend_strength_label)

        self.blend_slider = QSlider(self.paramsPanel)
        self.blend_slider.setObjectName(u"blend_slider")
        self.blend_slider.setMinimumSize(QSize(120, 0))
        self.blend_slider.setOrientation(Qt.Horizontal)

        self.params_row_blend.addWidget(self.blend_slider)

        self.blend_strength_lineEdit = QLineEdit(self.paramsPanel)
        self.blend_strength_lineEdit.setObjectName(u"blend_strength_lineEdit")
        self.blend_strength_lineEdit.setMinimumSize(QSize(58, 0))
        self.blend_strength_lineEdit.setMaximumSize(QSize(58, 16777215))

        self.params_row_blend.addWidget(self.blend_strength_lineEdit)


        self.verticalLayout_params.addLayout(self.params_row_blend)

        self.params_row_brightness = QHBoxLayout()
        self.params_row_brightness.setObjectName(u"params_row_brightness")
        self.brightness_label = QLabel(self.paramsPanel)
        self.brightness_label.setObjectName(u"brightness_label")
        self.brightness_label.setMinimumSize(QSize(64, 0))

        self.params_row_brightness.addWidget(self.brightness_label)

        self.brightness_slider = QSlider(self.paramsPanel)
        self.brightness_slider.setObjectName(u"brightness_slider")
        self.brightness_slider.setMinimumSize(QSize(120, 0))
        self.brightness_slider.setOrientation(Qt.Horizontal)

        self.params_row_brightness.addWidget(self.brightness_slider)

        self.brightness_lineEdit = QLineEdit(self.paramsPanel)
        self.brightness_lineEdit.setObjectName(u"brightness_lineEdit")
        self.brightness_lineEdit.setMinimumSize(QSize(58, 0))
        self.brightness_lineEdit.setMaximumSize(QSize(58, 16777215))

        self.params_row_brightness.addWidget(self.brightness_lineEdit)


        self.verticalLayout_params.addLayout(self.params_row_brightness)

        self.params_row_fill = QHBoxLayout()
        self.params_row_fill.setObjectName(u"params_row_fill")
        self.params_fill_label = QLabel(self.paramsPanel)
        self.params_fill_label.setObjectName(u"params_fill_label")
        self.params_fill_label.setMinimumSize(QSize(64, 0))

        self.params_row_fill.addWidget(self.params_fill_label)

        self.fill_color_btn = QPushButton(self.paramsPanel)
        self.fill_color_btn.setObjectName(u"fill_color_btn")
        self.fill_color_btn.setMinimumSize(QSize(28, 28))
        self.fill_color_btn.setMaximumSize(QSize(28, 28))

        self.params_row_fill.addWidget(self.fill_color_btn)

        self.fill_color_lineEdit = QLineEdit(self.paramsPanel)
        self.fill_color_lineEdit.setObjectName(u"fill_color_lineEdit")

        self.params_row_fill.addWidget(self.fill_color_lineEdit)

        self.custom_color_btn = QPushButton(self.paramsPanel)
        self.custom_color_btn.setObjectName(u"custom_color_btn")

        self.params_row_fill.addWidget(self.custom_color_btn)

        self.params_spacer_fill = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.params_row_fill.addItem(self.params_spacer_fill)


        self.verticalLayout_params.addLayout(self.params_row_fill)

        self.params_row_presets = QHBoxLayout()
        self.params_row_presets.setObjectName(u"params_row_presets")
        self.params_presets_label = QLabel(self.paramsPanel)
        self.params_presets_label.setObjectName(u"params_presets_label")
        self.params_presets_label.setMinimumSize(QSize(64, 0))

        self.params_row_presets.addWidget(self.params_presets_label)

        self.params_presets_box = QHBoxLayout()
        self.params_presets_box.setSpacing(5)
        self.params_presets_box.setObjectName(u"params_presets_box")

        self.params_row_presets.addLayout(self.params_presets_box)


        self.verticalLayout_params.addLayout(self.params_row_presets)

        self.params_sep = QFrame(self.paramsPanel)
        self.params_sep.setObjectName(u"params_sep")
        self.params_sep.setMinimumSize(QSize(0, 1))
        self.params_sep.setMaximumSize(QSize(16777215, 1))
        self.params_sep.setFrameShape(QFrame.HLine)

        self.verticalLayout_params.addWidget(self.params_sep)

        self.params_row_btn = QHBoxLayout()
        self.params_row_btn.setObjectName(u"params_row_btn")
        self.reset_params_btn = QPushButton(self.paramsPanel)
        self.reset_params_btn.setObjectName(u"reset_params_btn")

        self.params_row_btn.addWidget(self.reset_params_btn)

        self.params_spacer_btn = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.params_row_btn.addItem(self.params_spacer_btn)

        self.close_params_btn = QPushButton(self.paramsPanel)
        self.close_params_btn.setObjectName(u"close_params_btn")

        self.params_row_btn.addWidget(self.close_params_btn)


        self.verticalLayout_params.addLayout(self.params_row_btn)

        self.gridLayout = QGridLayout(annotationDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.draw_rect_btn = QPushButton(annotationDialog)
        self.draw_rect_btn.setObjectName(u"draw_rect_btn")
        icon = QIcon()
        icon.addFile(u"../resources/\u77e9\u5f62.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.draw_rect_btn.setIcon(icon)

        self.horizontalLayout.addWidget(self.draw_rect_btn)

        self.poly_btn = QPushButton(annotationDialog)
        self.poly_btn.setObjectName(u"poly_btn")
        icon1 = QIcon()
        icon1.addFile(u"../resources/\u591a\u8fb9\u5f62.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.poly_btn.setIcon(icon1)

        self.horizontalLayout.addWidget(self.poly_btn)

        self.delete_image_btn = QPushButton(annotationDialog)
        self.delete_image_btn.setObjectName(u"delete_image_btn")
        icon2 = QIcon()
        icon2.addFile(u"../resources/\u5220\u9664.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.delete_image_btn.setIcon(icon2)

        self.horizontalLayout.addWidget(self.delete_image_btn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.settings_btn = QPushButton(annotationDialog)
        self.settings_btn.setObjectName(u"settings_btn")

        self.horizontalLayout.addWidget(self.settings_btn)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.image_label_show = QGraphicsView(annotationDialog)
        self.image_label_show.setObjectName(u"image_label_show")

        self.horizontalLayout_5.addWidget(self.image_label_show)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_list = QLabel(annotationDialog)
        self.label_list.setObjectName(u"label_list")

        self.horizontalLayout_3.addWidget(self.label_list)

        self.horizontalSpacer_label = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_label)

        self.add_label = QPushButton(annotationDialog)
        self.add_label.setObjectName(u"add_label")
        self.add_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.add_label.setMinimumSize(QSize(24, 24))
        self.add_label.setMaximumSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.add_label)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_scrollArea = QScrollArea(annotationDialog)
        self.label_scrollArea.setObjectName(u"label_scrollArea")
        self.label_scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 202, 232))
        self.label_scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.label_scrollArea)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labeled_list = QLabel(annotationDialog)
        self.labeled_list.setObjectName(u"labeled_list")

        self.horizontalLayout_4.addWidget(self.labeled_list)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.label_info_scrollArea = QScrollArea(annotationDialog)
        self.label_info_scrollArea.setObjectName(u"label_info_scrollArea")
        self.label_info_scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 202, 235))
        self.label_info_scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_2.addWidget(self.label_info_scrollArea)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.image_info_label = QLabel(annotationDialog)
        self.image_info_label.setObjectName(u"image_info_label")

        self.verticalLayout_3.addWidget(self.image_info_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_3.addItem(self.horizontalSpacer_2)

        self.lineEdit = QLineEdit(annotationDialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_3.addWidget(self.lineEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_clip = QVBoxLayout()
        self.verticalLayout_clip.setObjectName(u"verticalLayout_clip")
        self.clipboard_label = QLabel(annotationDialog)
        self.clipboard_label.setObjectName(u"clipboard_label")

        self.verticalLayout_clip.addWidget(self.clipboard_label)

        self.clipboard_scroll = QScrollArea(annotationDialog)
        self.clipboard_scroll.setObjectName(u"clipboard_scroll")
        self.clipboard_scroll.setWidgetResizable(True)
        self.clipboard_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.clipboard_container = QWidget()
        self.clipboard_container.setObjectName(u"clipboard_container")
        self.clipboard_container.setGeometry(QRect(0, 0, 200, 120))
        self.clipboard_layout = QVBoxLayout(self.clipboard_container)
        self.clipboard_layout.setSpacing(6)
        self.clipboard_layout.setObjectName(u"clipboard_layout")
        self.clipboard_layout.setContentsMargins(0, 0, 0, 0)
        self.clipboard_scroll.setWidget(self.clipboard_container)

        self.verticalLayout_clip.addWidget(self.clipboard_scroll)


        self.verticalLayout_4.addLayout(self.verticalLayout_clip)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)

        self.horizontalLayout_5.setStretch(0, 8)
        self.horizontalLayout_5.setStretch(1, 2)

        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.pre_page_btn = QPushButton(annotationDialog)
        self.pre_page_btn.setObjectName(u"pre_page_btn")

        self.horizontalLayout_2.addWidget(self.pre_page_btn)

        self.next_page_btn = QPushButton(annotationDialog)
        self.next_page_btn.setObjectName(u"next_page_btn")

        self.horizontalLayout_2.addWidget(self.next_page_btn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)


        self.retranslateUi(annotationDialog)

        QMetaObject.connectSlotsByName(annotationDialog)
    # setupUi

    def retranslateUi(self, annotationDialog):
        annotationDialog.setWindowTitle(QCoreApplication.translate("annotationDialog", u"Dialog", None))
        self.params_title.setText(QCoreApplication.translate("annotationDialog", u"\u6807\u6ce8\u53c2\u6570", None))
        self.params_angle_label.setText(QCoreApplication.translate("annotationDialog", u"\u89d2\u5ea6\u8303\u56f4", None))
        self.label.setText(QCoreApplication.translate("annotationDialog", u"~", None))
        self.blend_strength_label.setText(QCoreApplication.translate("annotationDialog", u"\u878d\u5408\u5f3a\u5ea6", None))
        self.brightness_label.setText(QCoreApplication.translate("annotationDialog", u"\u4eae\u5ea6\u8c03\u8282", None))
        self.params_fill_label.setText(QCoreApplication.translate("annotationDialog", u"\u586b\u5145\u989c\u8272", None))
#if QT_CONFIG(tooltip)
        self.fill_color_btn.setToolTip(QCoreApplication.translate("annotationDialog", u"\u70b9\u51fb\u6253\u5f00\u53d6\u8272\u5668, \u9009\u4efb\u610f\u989c\u8272", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.fill_color_lineEdit.setToolTip(QCoreApplication.translate("annotationDialog", u"\u652f\u6301 #RRGGBB / #RGB / 255,255,255 / black / \u767d \u7b49\u5199\u6cd5, \u4e5f\u53ef\u4ee5\u70b9\u5de6\u8fb9\u8272\u5757\u6253\u5f00\u53d6\u8272\u5668", None))
#endif // QT_CONFIG(tooltip)
        self.fill_color_lineEdit.setPlaceholderText(QCoreApplication.translate("annotationDialog", u"#RRGGBB", None))
#if QT_CONFIG(tooltip)
        self.custom_color_btn.setToolTip(QCoreApplication.translate("annotationDialog", u"\u81ea\u5b9a\u4e49\u989c\u8272", None))
#endif // QT_CONFIG(tooltip)
        self.params_presets_label.setText(QCoreApplication.translate("annotationDialog", u"\u5e38\u7528\u8272", None))
        self.reset_params_btn.setText(QCoreApplication.translate("annotationDialog", u"\u6062\u590d\u9ed8\u8ba4", None))
        self.close_params_btn.setText(QCoreApplication.translate("annotationDialog", u"\u5b8c\u6210", None))
        self.draw_rect_btn.setText(QCoreApplication.translate("annotationDialog", u"\u77e9\u5f62", None))
        self.poly_btn.setText(QCoreApplication.translate("annotationDialog", u"\u591a\u8fb9\u5f62", None))
        self.delete_image_btn.setText(QCoreApplication.translate("annotationDialog", u"\u5220\u9664\u56fe\u50cf", None))
        self.settings_btn.setText(QCoreApplication.translate("annotationDialog", u"\u8bbe\u7f6e", None))
        self.label_list.setText(QCoreApplication.translate("annotationDialog", u"\u6807\u7b7e\u5217\u8868", None))
#if QT_CONFIG(tooltip)
        self.add_label.setToolTip(QCoreApplication.translate("annotationDialog", u"\u6dfb\u52a0\u6807\u7b7e", None))
#endif // QT_CONFIG(tooltip)
        self.add_label.setText(QCoreApplication.translate("annotationDialog", u"+", None))
        self.labeled_list.setText(QCoreApplication.translate("annotationDialog", u"\u6807\u6ce8\u4fe1\u606f", None))
        self.image_info_label.setText(QCoreApplication.translate("annotationDialog", u"\u56fe\u50cf\u4fe1\u606f", None))
        self.clipboard_label.setText(QCoreApplication.translate("annotationDialog", u"\u526a\u5207\u677f", None))
        self.pre_page_btn.setText(QCoreApplication.translate("annotationDialog", u"\u4e0a\u4e00\u5f20(A)", None))
        self.next_page_btn.setText(QCoreApplication.translate("annotationDialog", u"\u4e0b\u4e00\u5f20(D)", None))
    # retranslateUi

