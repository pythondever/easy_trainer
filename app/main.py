import sys
import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append('../ui')
from app.log_dialog import LogDialog
from ui.app import Ui_AppUI as MainUI
from app.utils import setup_matplotlib_chinese, load_style_sheet
from db import DataBase
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtWidgets import QWidget, QApplication, QTimeEdit, QFrame


try:
    from shiboken6 import isValid as _is_valid
except ImportError:
    _is_valid = lambda obj: obj is not None

try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None

from app.mixins import (LabelMixin, ProjectMixin, ImportExportMixin,
                        DatasetViewMixin, TrainMixin, MiscMixin)


class App(QWidget, MainUI, LabelMixin, ProjectMixin, ImportExportMixin,
          DatasetViewMixin, TrainMixin, MiscMixin):
    def __init__(self):
        super().__init__()
        self.db = DataBase(os.path.join(os.path.expanduser("~"), ".easy_trainer"))
        try:
            self.db.migrate_model_records()
        except Exception:
            pass
        self.dataset_cache = {}
        self._loading_tasks = {}
        self.page_size = 50  # 每页图像记录数
        self.current_page = 0
        self.current_label = "__unlabeled__"
        self.init_widget()
        self.register_event()
        self.fill_setting()
        self._log_dialog = LogDialog(self)
        self._log("软件启动")

    def closeEvent(self, event):
        self._log("软件退出")
        if self.is_training():
            self._log("软件退出前停止训练")
            self.stop_training(confirm=False)
        # 停止还在运行的测试线程,避免 QThread destroyed while running 崩溃
        for w in list(getattr(self, "_test_workers", set())):
            try:
                w.stop()
                w.wait(3000)
            except Exception:
                pass
        super().closeEvent(event)

    def init_widget(self):
        self.setupUi(self)
        # 训练进度条/停止按钮默认隐藏(有训练任务时才显示)
        self.train_progress.hide()
        self.task_name_label.hide()
        self.stop_train_btn.hide()
        self.stop_train_btn.setStyleSheet(
            "QPushButton { background-color: #d64545; color: white;"
            " border: none; border-radius: 6px; padding: 4px 12px;"
            " font-size: 13px; }"
            "QPushButton:hover { background-color: #e05555; }")
        # 进度条文本: `30% | 0.556`
        self._latest_map50 = None
        self._apply_progress_format()
        self.time_count_label.hide()
        self.time_count_edit.hide()
        self.gpu_memory_label.show()
        self.gpu_memory_use_btn.show()
        self.time_count_edit.setReadOnly(True)
        self.time_count_edit.setButtonSymbols(QTimeEdit.NoButtons)
        self.time_count_edit.setDisplayFormat("hh:mm:ss")
        self.time_count_edit.setTime(self.time_count_edit.time().fromString("00:00:00", "hh:mm:ss"))
        self._train_start_ts = 0.0
        self._eta_remain = 0
        self._test_start_ts = 0  # 测试开始时间, 用于推算剩余时间
        self._eta_timer = QTimer(self)
        self._eta_timer.setInterval(1000)
        self._eta_timer.timeout.connect(self._eta_tick)
        self._gpu_timer = QTimer(self)
        self._gpu_timer.setInterval(2000)
        self._gpu_timer.timeout.connect(self._refresh_gpu_memory)
        self._gpu_timer.start()
        self._refresh_gpu_memory()
        self._train_worker = None
        self._training_record_id = None
        icon_path = os.path.join(WORKSPACE_DIRECTORY, "resources", "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        logo_path = os.path.join(WORKSPACE_DIRECTORY, "resources", "icon.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.appLogoLabel.setPixmap(pix)
        self.sidebarTitle.setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self._init_image_view()
        self._init_label_filter()
        self._current_dataset = None
        self._setup_header_groups()

    def _setup_header_groups(self):
        """首页顶部工具栏分组: 标签区/统计区/训练区 用竖线分隔, 主次操作视觉区分。"""
        # 主操作(训练)蓝填充 / 危险操作(删除)红色
        self.train_btn.setProperty("class", "primary")
        self.delete_label_btn.setProperty("class", "danger")

        def vline():
            line = QFrame(self)
            line.setObjectName("headerSeparator")
            line.setFrameShape(QFrame.VLine)
            line.setFrameShadow(QFrame.Plain)
            return line

        lay = self.datasetHeaderLayout
        # 插入位置(按创建顺序): 9=标签筛选 12=统计 13=训练
        lay.insertWidget(13, vline())   # 统计 | 训练
        lay.insertWidget(12, vline())   # 标签区 | 统计
        lay.insertWidget(9, vline())    # 进度区 | 标签区

    def register_event(self):
        self.add_project_btn.clicked.connect(lambda: self.add_project())
        self.pre_page_btn.clicked.connect(lambda: self.pre_page())
        self.next_page_btn.clicked.connect(lambda: self.next_page())
        self.dataset_properties_btn.clicked.connect(self._on_dataset_properties)
        self.stop_train_btn.clicked.connect(lambda checked=False: self.stop_training())
        self.rename_label_btn.clicked.connect(self._on_rename_label)
        self.delete_label_btn.clicked.connect(self._on_delete_label)
        self.train_btn.clicked.connect(self._on_train_clicked)
        self.log_btn.clicked.connect(self._on_log_clicked)
        self.model_btn.clicked.connect(self._on_model_clicked)

    def fill_setting(self):
        """启动时从 db 查询项目数据，显示到界面。"""
        self.refresh_project_list()

    def eventFilter(self, obj, event):
        """拦截 graphics_view 双击事件(双击小图进入标注)。"""
        if (obj is self.graphics_view.viewport()
                and event.type() == QEvent.MouseButtonDblClick):
            self._on_graphics_double_click(event.position().toPoint())
            return True
        return super().eventFilter(obj, event)

    def show_ui(self):
        self.showMaximized()


if __name__ == "__main__":
    setup_matplotlib_chinese()
    myapp = QApplication(sys.argv)
    myapp.setStyleSheet(load_style_sheet())
    ui = App()
    ui.show_ui()
    sys.exit(myapp.exec())
