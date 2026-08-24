# -*- coding: utf-8 -*-
import sys
import os

CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append('../ui')
from ui.enter_name import Ui_Dialog as EnterNameUI
from ui.add_dataset import Ui_AddDatasets
from app.label_utils import label_sort_key
from app.message_box import MessageBox
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QDialog, QMenu, \
    QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QTreeWidget, QTreeWidgetItem, \
    QHeaderView, QAbstractItemView, QComboBox, QPushButton

try:
    from shiboken6 import isValid as _is_valid
except ImportError:
    _is_valid = lambda obj: obj is not None

try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None


class ProjectMixin(object):
    def _show_enter_name(self, preset=""):
        """弹出项目名称输入框。返回(name, ok);ok=False 表示用户取消。"""
        dlg = QDialog(self)
        dlg.setWindowTitle("项目名称")
        ui = EnterNameUI()
        ui.setupUi(dlg)
        if preset:
            ui.project_name_txt.setText(preset)
            ui.project_name_txt.selectAll()
        ui.enter_name_lbl.setVisible(False)
        ui.done_enter_name_btn.clicked.connect(dlg.accept)
        dlg.exec()
        name = ui.project_name_txt.text().strip()
        return name, dlg.result() == QDialog.Accepted

    def add_project(self):
        name, ok = self._show_enter_name()
        if not ok or not name:
            return
        if name in self.db.get_projects():
            MessageBox.warning(self, "创建项目", "项目名称已存在！")
            return
        self.db.add_project(name)
        self._log("创建项目: {}".format(name))
        self.refresh_project_list()

    def _rename_project(self, old_name):
        new_name, ok = self._show_enter_name(preset=old_name)
        if not ok or not new_name or new_name == old_name:
            return
        if new_name in self.db.get_projects():
            MessageBox.warning(self, "修改名称", "项目名称已存在！")
            return
        self.db.rename_project(old_name, new_name)
        self.refresh_project_list()

    def _delete_project(self, name):
        if MessageBox.question(self, "删除项目", "确定删除项目「{}」吗?\n".format(name),
                               default_yes=True):
            self.db.delete_project(name)
            self.db.delete_project_info(name)
            self.db.delete_project_records(name)
            self.dataset_cache.pop(name, None)
            cur_ds = getattr(self, "_current_dataset", None)
            if cur_ds and cur_ds[0] == name:
                self._current_dataset = None
                self.current_page = 0
                self._clear_scene()
                self.pageInfoLabel.setText("0 / 0")
            self.refresh_project_list()

    def _init_project_tree(self):
        self.project_tree = QTreeWidget()
        self.project_tree.setObjectName("projectTree")
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setRootIsDecorated(False)
        self.project_tree.setIndentation(20)
        self.project_tree.setIconSize(QSize(16, 16))
        self.project_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_tree.customContextMenuRequested.connect(self._on_project_tree_menu)
        self.project_tree.itemExpanded.connect(self._on_project_expand_changed)
        self.project_tree.itemCollapsed.connect(self._on_project_expand_changed)
        self.project_tree.itemClicked.connect(self._on_project_tree_clicked)
        self.project_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.project_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.project_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.project_scroll_area.setWidget(self.project_tree)
        self.project_scroll_area.setWidgetResizable(True)

    @staticmethod
    def _on_project_expand_changed(item):
        """项目节点展开/折叠时切换文本前的 ▶/▼ 标记。"""
        kind = item.data(0, Qt.UserRole)
        if not kind or kind[0] != "project":
            return
        prefix = "▼" if item.isExpanded() else "▶"
        item.setText(0, "{}{}".format(prefix, kind[1]))

    def refresh_project_list(self):
        if not hasattr(self, "project_tree"):
            self._init_project_tree()
        self.project_tree.clear()
        project_icon = self._tree_icon("项目.png")
        # dataset_icon = self._tree_icon("图像.png")
        proj_font = QFont()
        proj_font.setBold(True)
        proj_font.setPointSize(12)
        for name in self.db.get_projects():
            proj_item = QTreeWidgetItem(["▶" + name])
            proj_item.setData(0, Qt.UserRole, ("project", name))
            proj_item.setFont(0, proj_font)
            if not project_icon.isNull():
                proj_item.setIcon(0, project_icon)
            for ds in self.db.get_datasets(name):
                ds_item = QTreeWidgetItem([""])
                ds_item.setData(0, Qt.UserRole, ("dataset", name, ds["dataset_name"]))
                proj_item.addChild(ds_item)
                self._set_dataset_widget(ds_item, name, ds["dataset_name"])
            self.project_tree.addTopLevelItem(proj_item)

    def _tree_icon(self, name):
        """加载 resources/ 下图标, 缺失则返回空 QIcon。"""
        path = os.path.join(WORKSPACE_DIRECTORY, "resources", name)
        if os.path.exists(path):
            return QIcon(path)
        return QIcon()

    def _set_dataset_widget(self, ds_item, project_name, dataset_name):
        """
        把数据集节点替换为整体行内容器: [图标 + 名称 + 拉伸 + 标注进度]，
        """
        container = QWidget(self)
        container.setObjectName("datasetRowContainer")
        # 事件穿透到 QTreeWidget, 让 ::item:hover / :selected 整行高亮生效
        container.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h = QHBoxLayout(container)
        h.setContentsMargins(6, 0, 8, 0)
        h.setSpacing(8)
        h.setAlignment(Qt.AlignVCenter)
        name_lbl = QLabel(container)
        name_lbl.setObjectName("datasetRowName")
        name_lbl.setTextFormat(Qt.RichText)
        icon_path_uri = "file:///" + os.path.join(
            WORKSPACE_DIRECTORY, "resources", "图像.png").replace("\\", "/")
        name_lbl.setText(
            '<img src="{0}" width="14" height="14" '
            'style="vertical-align: middle;"/>&nbsp;{1}'.format(
                icon_path_uri, dataset_name))
        h.addWidget(name_lbl)
        h.addStretch(1)
        progress_lbl = QLabel(container)
        progress_lbl.setObjectName("datasetRowProgress")
        h.addWidget(progress_lbl)
        binding = self.db.get_dataset_import(project_name, dataset_name)
        total = binding.get("total", 0)
        labeled = binding.get("labeled", 0)
        self._style_progress_chip(progress_lbl, labeled, total)
        progress_lbl.setText("{}/{}".format(labeled, total))
        self.project_tree.setItemWidget(ds_item, 0, container)
        return container, progress_lbl

    @staticmethod
    def _style_progress_chip(lbl, labeled, total):
        """标注进度 chip: 全部标完绿色, 未完成主题蓝, 无数据中性。"""
        if total > 0 and labeled >= total:
            chip = ("background-color: #1f6b45; color: #d9f2e3;"
                    " border-radius: 8px; padding: 2px 10px; font-size: 11px;")
        elif total > 0:
            chip = ("background-color: #2c3a5e; color: #c3d0f0;"
                    " border-radius: 8px; padding: 2px 10px; font-size: 11px;")
        else:
            chip = ("color: #6c7385; background: transparent;"
                    " padding-right: 4px; font-size: 12px;")
        lbl.setStyleSheet(chip)

    def _on_project_tree_menu(self, pos):
        """
        项目树右键菜单:
        项目节点 -> 添加数据集 / 修改名称 / 删除项目
        数据集节点 -> 修改 / 删除
        """
        item = self.project_tree.itemAt(pos)
        if item is None:
            return
        kind = item.data(0, Qt.UserRole)
        menu = QMenu(self)
        if kind[0] == "project":
            act_add_ds = menu.addAction("添加数据集")
            menu.addSeparator()
            act_rename = menu.addAction("修改名称")
            act_del = menu.addAction("删除项目")
            act = menu.exec(self.project_tree.mapToGlobal(pos))
            if act is None:
                return
            if act == act_add_ds:
                self._add_dataset(kind[1])
            elif act == act_rename:
                self._rename_project(kind[1])
            elif act == act_del:
                self._delete_project(kind[1])
        elif kind[0] == "dataset":
            act_load = menu.addAction("载入")
            act_import = menu.addAction("导入")
            act_export = menu.addAction("导出")
            act_move = menu.addAction("移动")
            act_rename = menu.addAction("修改")
            act_del = menu.addAction("删除")
            act = menu.exec(self.project_tree.mapToGlobal(pos))
            if act is None:
                return
            if act == act_load:
                self._load_dataset_view(kind[1], kind[2])
            elif act == act_import:
                self._import_dataset(kind[1], kind[2])
            elif act == act_export:
                self.project_tree.setCurrentItem(item)
                self._on_export_clicked()
            elif act == act_move:
                self._on_dataset_move(kind[1], kind[2])
            elif act == act_rename:
                self._rename_dataset(kind[1], kind[2])
            elif act == act_del:
                self._delete_dataset(kind[1], kind[2])

    def _show_add_dataset(self, preset_name="", title="添加数据集"):
        """
        弹出数据集对话框(ui/add_dataset.py 设计器生成)。
        数据集不再区分类型,隐藏类型下拉;返回(name, ok)。
        """
        dlg = QDialog(self)
        ui = Ui_AddDatasets()
        ui.setupUi(dlg)
        dlg.setWindowTitle(title)
        if preset_name:
            ui.lineEdit.setText(preset_name)
            ui.lineEdit.selectAll()
        # 类型已废弃:隐藏类型下拉
        combo = getattr(ui, "comboBox", None)
        if combo is not None:
            combo.setVisible(False)
        ui.done_btn.clicked.connect(dlg.accept)
        dlg.setFixedHeight(dlg.sizeHint().height())
        dlg.exec()
        name = ui.lineEdit.text().strip()
        return name, dlg.result() == QDialog.Accepted

    def _add_dataset(self, project_name):
        name, ok = self._show_add_dataset()
        if not ok or not name:
            return
        if not self.db.add_dataset(project_name, name):
            MessageBox.warning(self, "添加数据集", "该项目下已存在同名数据集！")
            return
        self._log("创建数据集: {}/{}".format(project_name, name))
        self.refresh_project_list()

    def _rename_dataset(self, project_name, old_name):
        name, ok = self._show_add_dataset(preset_name=old_name, title="修改数据集")
        if not ok or not name or name == old_name:
            return
        if not self.db.rename_dataset(project_name, old_name, name):
            MessageBox.warning(self, "修改数据集", "该项目下已存在同名数据集！")
            return
        self._log("重命名数据集: {} → {}".format(project_name, old_name, name))
        self.refresh_project_list()

    def _delete_dataset(self, project_name, ds_name):
        if MessageBox.question(
                self, "删除数据集",
                "确定删除数据集「{}」吗?\n".format(ds_name),
                default_yes=True):
            self.db.delete_dataset(project_name, ds_name)
            # 训练/模型记录可能被多个数据集共用,只移除该数据集,无引用才删记录
            self.db.remove_dataset_from_records(project_name, ds_name)
            self._log("删除数据集: {}/{}".format(project_name, ds_name))
            proj_cache = self.dataset_cache.get(project_name, {})
            proj_cache.pop(ds_name, None)
            if getattr(self, "_current_dataset", None) == (project_name, ds_name):
                self._current_dataset = None
                self.current_page = 0
                self._clear_scene()
                self.pageInfoLabel.setText("0 / 0")
            self.refresh_project_list()

    def _on_dataset_move(self, project_name, ds_name):
        """右键「移动」: 选择目标数据集 → 确认 → 移动数据。"""
        # 1. 选择目标数据集(本项目之外的其他项目数据集)
        target = self._select_move_target(project_name, ds_name)
        if target is None:
            return
        dst_proj, dst_ds = target
        # 2. 确认
        if not MessageBox.question(
                self, "移动数据集",
                "是否将「{}」的数据从\n{} / {} 移动到 {} / {}？\n"
                "移动后源数据集将清空。".format(
                    ds_name, project_name, ds_name, dst_proj, dst_ds),
                default_yes=True):
            return
        # 3. 执行
        try:
            self._move_dataset_data(project_name, ds_name, dst_proj, dst_ds)
        except Exception as e:
            MessageBox.critical(self, "移动失败", str(e))
            return
        MessageBox.information(
            self, "移动数据集",
            "已从 {} / {} 移动到 {} / {}".format(
                project_name, ds_name, dst_proj, dst_ds))

    def _select_move_target(self, src_project, src_ds):
        """
        弹目标数据集选择对话框(同项目/跨项目，排除源数据集自身)。
        返回(项目, 数据集)或 None。
        """
        candidates = []  # (项目, 数据集) —— 排除源数据集自身, 同项目内其他数据集也可选
        for proj in self.db.get_projects():
            for ds in self.db.get_datasets(proj):
                if proj == src_project and ds["dataset_name"] == src_ds:
                    continue
                candidates.append((proj, ds["dataset_name"]))
        if not candidates:
            MessageBox.warning(self, "移动数据集", "没有可移动到的目标数据集（本项目之外无数据集）")
            return None
        dlg = QDialog(self)
        dlg.setObjectName("MoveTargetDialog")
        dlg.setWindowTitle("选择目标数据集")
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)
        tip = QLabel("选择要将数据移动到的目标数据集：")
        layout.addWidget(tip)
        combo = QComboBox(dlg)
        for proj, ds in candidates:
            combo.addItem("{} / {}".format(proj, ds), (proj, ds))
        layout.addWidget(combo)
        btns = QHBoxLayout()
        btns.addStretch(1)
        ok_btn = QPushButton("确定", dlg)
        ok_btn.clicked.connect(dlg.accept)
        cancel_btn = QPushButton("取消", dlg)
        cancel_btn.clicked.connect(dlg.reject)
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)
        if dlg.exec() != QDialog.Accepted:
            return None
        return combo.currentData()

    def _move_dataset_data(self, src_proj, src_ds, dst_proj, dst_ds):
        """
        核心:源数据集数据合并到目标数据集,源清空.
        覆盖:缓存索引(按图像去重)、db 导入绑定路径列表、标签类别、
        标注/总数统计、已删除图像记录。
        """
        # ---- 1. 缓存合并(image_path 归一化去重; 源中已存在于目标的跳过)----
        src_index = self.dataset_cache.get(src_proj, {}).get(src_ds) or {}
        dst_index = self.dataset_cache.get(dst_proj, {}).get(dst_ds) or {}
        src_recs = list(src_index.get("all", []))
        dst_recs = list(dst_index.get("all", []))
        norm = lambda p: os.path.normcase(os.path.normpath(p or ""))
        seen = {norm(r.get("image_path")) for r in dst_recs}
        moved = [r for r in src_recs
                 if norm(r.get("image_path")) not in seen]
        dst_recs = dst_recs + moved
        dst_index["all"] = dst_recs
        # 重建目标 labels 分组索引
        if self.dataset_cache.get(dst_proj, {}).get(dst_ds) is not None:
            self._rebuild_index_labels(dst_proj, dst_ds)
        # 源缓存清空
        if src_index:
            src_index["all"] = []
            src_index["labels"] = {}

        # ---- 2. db：目标合并导入绑定 + 重算统计 ----
        src_binding = self.db.get_dataset_import(src_proj, src_ds) or {}
        dst_binding = self.db.get_dataset_import(dst_proj, dst_ds) or {}
        dst_img = list(dst_binding.get("image_paths") or [])
        src_img = list(src_binding.get("image_paths") or [])
        dst_lbl = list(dst_binding.get("label_paths") or [])
        src_lbl = list(src_binding.get("label_paths") or [])
        img_paths = dst_img + [p for p in src_img if p not in dst_img]
        lbl_paths = dst_lbl + [p for p in src_lbl if p not in dst_lbl]
        total_new = len(dst_recs)
        labeled_new = sum(
            1 for r in dst_recs
            if r.get("boxes") or self._has_label_file(r.get("image_path", "")))
        self.db.update_dataset_import(
            dst_proj, dst_ds, img_paths, lbl_paths,
            dst_binding.get("label_fmt", ""),
            labeled=labeled_new, total=total_new)

        # ---- 3. db：目标标签合并(颜色冲突保留目标)----
        dst_labels = self.db.get_dataset_labels(dst_proj, dst_ds)
        for lbl, color in self.db.get_dataset_labels(src_proj, src_ds).items():
            if lbl not in dst_labels:
                dst_labels[lbl] = color
        self.db.save_dataset_labels(dst_proj, dst_ds, dst_labels)

        # ---- 4. db：源清空(导入绑定 + 标签)----
        self.db.clear_dataset_import(src_proj, src_ds)
        self.db.save_dataset_labels(src_proj, src_ds, {})
        # class_id 映射合并进目标(目标优先),源清空
        src_ids = self.db.get_dataset_label_ids(src_proj, src_ds)
        dst_ids = self.db.get_dataset_label_ids(dst_proj, dst_ds)
        if src_ids or dst_ids:
            merged = dict(src_ids)
            merged.update(dst_ids)  # 目标优先
            self.db.save_dataset_label_ids(dst_proj, dst_ds, merged)
            self.db.save_dataset_label_ids(src_proj, src_ds, {})

        # ---- 5. 已删除图像记录迁移 ----
        self.db.move_deleted_images(src_proj, src_ds, dst_proj, dst_ds)

        # ---- 6. 日志: 目标标签统计(按框数)----
        label_counts = {}
        for r in dst_recs:
            for b in (r.get("boxes") or []):
                lbl = b[-1]
                label_counts[lbl] = label_counts.get(lbl, 0) + 1
        counts_str = ", ".join(
            "{}: {}个".format(k, v) for k, v in
            sorted(label_counts.items(), key=lambda kv: label_sort_key(kv[0])))
        self._log("数据集移动: {}/{} → {}/{} | 移动图像 {} 张"
                  " | 目标标签统计({}类): {}".format(
            src_proj, src_ds, dst_proj, dst_ds, len(moved),
            len(label_counts), counts_str or "(无)"))

        # ---- 7. 刷新: 树 / 显示区 / 标签筛选 ----
        self.refresh_project_list()
        if getattr(self, "_current_dataset", None) == (src_proj, src_ds):
            # 源数据集已清空: 完整重置图像区/分页/筛选下拉/标注统计
            self._current_dataset = None
            self._reset_image_area()
        elif getattr(self, "_current_dataset", None) == (dst_proj, dst_ds):
            self.show_dataset_images(dst_proj, dst_ds)
            self._refresh_label_filter(dst_proj, dst_ds)
