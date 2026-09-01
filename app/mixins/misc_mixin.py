# -*- coding: utf-8 -*-
import sys
import os
CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append(os.path.join(WORKSPACE_DIRECTORY, 'ui'))
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from app.widgets.log_dialog import LogDialog
from app.widgets.model_dialog import ModelDialog
from app.train.dialogs import TrainDialog, _ClickToPopupFilter
from ui.dataset_properties import Ui_Dialog as DatasetPropertiesUI
from app.widgets.message_box import MessageBox
from app.core.log import write_log
from PySide6.QtGui import QPixmap, QImage, QStandardItem
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMessageBox, QLabel, QGraphicsScene

try:
    from shiboken6 import isValid as _is_valid
except ImportError:
    _is_valid = lambda obj: obj is not None

try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None


class MiscMixin(object):
    @staticmethod
    def _write_log(msg):
        """记录操作日志到 logs/app.log"""
        write_log(msg)

    def _log(self, msg):
        """写日志"""
        self._write_log(msg)

    def _on_log_clicked(self):
        """显示常驻日志对话框(启动时已创建并注册，隐藏也接收日志)。"""
        dlg = getattr(self, "_log_dialog", None)
        if dlg is None:
            self._log_dialog = LogDialog(self)
            dlg = self._log_dialog
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    def _on_model_clicked(self):
        md = ModelDialog(app=self, project="", dataset="", parent=self)
        md.exec()
        md.deleteLater()

    def _on_train_clicked(self):
        dlg = TrainDialog(self)
        dlg.exec()

    def _on_dataset_properties(self):
        """工具栏「统计」按钮:全局对话框，多选数据集查看标注统计与路径。"""
        dlg = QDialog(self)
        dlg.setWindowTitle("数据集统计")
        dlg.setWindowFlags(
            dlg.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        ui = DatasetPropertiesUI()
        ui.setupUi(dlg)
        ui.image_path_line_txt.setReadOnly(True)
        ui.label_path_line_txt.setReadOnly(True)
        # 多选下拉:默认勾选当前选中的数据集(如有)
        self._setup_stats_multi_combo(ui.dataset_comboBox)
        cur = getattr(self, "_current_dataset", None)
        checked = ["{}/{}".format(*cur)] if cur else []
        self._fill_stats_dataset_multi(ui.dataset_comboBox, checked)
        ui.select_dataset_btn.clicked.connect(
            lambda: self._apply_stats_selection(ui))
        dlg.exec()

    def _setup_stats_multi_combo(self, combo):
        """把下拉框配置成多选模式(文本居中+点击任意位置展开)。"""
        combo.setEditable(True)
        combo.setFocusPolicy(Qt.StrongFocus)
        le = combo.lineEdit()
        le.setObjectName("multiComboLineEdit")
        le.setReadOnly(True)
        le.setAlignment(Qt.AlignHCenter)
        f = _ClickToPopupFilter(combo)
        # 保持引用防 GC(否则事件过滤器失效, 点击 lineEdit 不再展开)
        if not hasattr(self, "_stats_combo_filters"):
            self._stats_combo_filters = []
        self._stats_combo_filters.append(f)
        combo.installEventFilter(f)
        le.installEventFilter(f)
        combo.model().itemChanged.connect(
            lambda *_: self._update_stats_combo_text(combo))
        combo.activated.connect(lambda _i: self._update_stats_combo_text(combo))

    def _fill_stats_dataset_multi(self, combo, checked_names):
        """列出全部项目/数据集(文本"项目/数据集",data=(项目,数据集)),勾选项默认选中。"""
        model = combo.model()
        model.clear()
        for proj in self.db.get_projects():
            for ds_info in self.db.get_datasets(proj):
                ds = str(ds_info.get("dataset_name", "") or "")
                if not ds:
                    continue
                text = "{}/{}".format(proj, ds)
                item = QStandardItem(text)
                item.setData((proj, ds), Qt.UserRole)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                item.setCheckState(
                    Qt.Checked if text in checked_names else Qt.Unchecked)
                model.appendRow(item)
        self._update_stats_combo_text(combo)

    def _update_stats_combo_text(self, combo):
        """把勾选的数据集显示到下拉框编辑区(居中文本)。"""
        model = combo.model()
        checked = []
        for i in range(model.rowCount()):
            item = model.item(i)
            if item.checkState() == Qt.Checked:
                data = item.data(Qt.UserRole)
                if isinstance(data, tuple) and len(data) == 2:
                    checked.append(data)
        texts = ["{}/{}".format(p, d) for p, d in checked]
        combo.setEditText(", ".join(texts))
        combo.setToolTip("\n".join(texts) if texts else "")
        if not texts:
            combo.setCurrentIndex(-1)

    def _selected_stats_datasets(self, combo):
        """返回勾选的数据集列表 [(项目, 数据集), ...]。"""
        out = []
        model = combo.model()
        for i in range(model.rowCount()):
            item = model.item(i)
            if item.checkState() == Qt.Checked:
                data = item.data(Qt.UserRole)
                if isinstance(data, tuple) and len(data) == 2:
                    out.append(data)
        return out

    def _apply_stats_selection(self, ui):
        """点击「确定」:刷新路径框 + 合并多个数据集的标签统计画柱状图。"""
        checked = self._selected_stats_datasets(ui.dataset_comboBox)
        ui.image_path_line_txt.setText(self._format_stats_paths(checked, "image"))
        ui.label_path_line_txt.setText(self._format_stats_paths(checked, "label"))
        counts = {}
        label_colors = {}
        for proj, ds in checked:
            for k, v in (self.db.get_dataset_label_counts(proj, ds) or {}).items():
                counts[k] = counts.get(k, 0) + v
            if not label_colors:
                label_colors = self.db.get_dataset_labels(proj, ds)
        self._render_label_stats(ui.label_stats_view, "", "", counts,
                                 label_colors=label_colors)

    def _format_stats_paths(self, checked, kind):
        """
        按数据集拼接路径文本:[项目/数据集]路径1;路径2 | [项目/数据集]路径3
        同一数据集多路径只显示一次前缀,路径全跟在后面;换下一个数据集再拼前缀。
        """
        blocks = []
        for proj, ds in checked:
            binding = self.db.get_dataset_import(proj, ds) or {}
            if kind == "image":
                paths = binding.get("image_paths") or (
                    [binding.get("image_path")]
                    if binding.get("image_path") else [])
            else:
                paths = binding.get("label_paths") or (
                    [binding.get("label_path")]
                    if binding.get("label_path") else [])
            paths = [p for p in paths if p]
            if not paths:
                blocks.append("[{}/{}](未设置)".format(proj, ds))
            else:
                blocks.append("[{}/{}]{}".format(proj, ds, "; ".join(paths)))
        return " | ".join(blocks) or "(未选择数据集)"

    def _render_label_stats(self, view, project, dataset, label_counts,
                             label_colors=None):
        """标签分布柱状图(宽度随标签数量扩展,超宽用滚动条)。"""
        num_bars = max(1, len(label_counts))
        fig_width = max(4.0, num_bars * 0.3)
        fig_height = 6.0
        fig = Figure(figsize=(fig_width, fig_height), dpi=100, facecolor="#1c1e25")
        axes = fig.add_subplot(111, facecolor="#1c1e25")
        scene = QGraphicsScene()
        if not label_counts:
            axes.text(0.5, 0.5, "暂无标注", ha="center", va="center",
                      color="#8a92a3", transform=axes.transAxes, fontsize=14)
            axes.set_xticks([])
            axes.set_yticks([])
        else:
            if label_colors is None:
                label_colors = self.db.get_dataset_labels(project, dataset)
            # 按标签数量降序
            items = sorted(label_counts.items(), key=lambda kv: kv[1],
                           reverse=True)
            labels = [k for k, _ in items]
            values = [v for _, v in items]
            colors = [label_colors.get(name, "#5B8CFF") for name in labels]
            # 柱宽(数据单位)≈ n/15.5:使柱宽像素 = 图宽/20;多标签时收紧防重叠
            bar_width = max(0.05, min(0.15, num_bars / 15.5))
            x_positions = np.arange(num_bars)
            bars = axes.bar(x_positions, values, color=colors, width=bar_width,
                            edgecolor="none")
            ymax = max(values) if values else 0
            for bar, v in zip(bars, values):
                axes.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                          str(v), ha="center", va="bottom",
                          color="#e8eaf0", fontsize=10)
            axes.set_xlabel("标签", color="#c3c9d6", fontsize=11, labelpad=8)
            axes.set_ylabel("标签数量", color="#c3c9d6", fontsize=11, labelpad=8)
            axes.tick_params(axis="x", colors="#c3c9d6", labelsize=10, rotation=0)
            axes.tick_params(axis="y", colors="#c3c9d6", labelsize=10)
            axes.set_ylim(0, ymax * 1.12 if ymax else 1)
            for side in ("top", "right"):
                axes.spines[side].set_visible(False)
            for side in ("left", "bottom"):
                axes.spines[side].set_color("#3a3f4e")
            axes.yaxis.grid(True, color="#2a2e38", linestyle="--", linewidth=0.6, alpha=0.8)
            axes.set_axisbelow(True)
            axes.set_xticks(x_positions)
            axes.set_xticklabels(labels)
            axes.set_xlim(-0.5, num_bars - 0.5)
            axes.set_ylim(0, ymax * 1.12 if ymax else 1)
        canvas = FigureCanvasQTAgg(fig)
        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()
        image = QImage(canvas.buffer_rgba(), int(width), int(height),
                       QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(image)
        scene.addPixmap(pixmap)
        scene.update()
        view.setScene(scene)
        if view.sceneRect().isEmpty():
            view.setSceneRect(scene.itemsBoundingRect())

    def _refresh_dataset_stats(self, project_name, dataset_name):
        """
        一次遍历同时刷新「已标注/总数」进度与「每类框数」统计。
        """
        cache = self.dataset_cache.get(project_name, {}).get(dataset_name, {})
        recs = cache.get("all") or []
        if not recs and not cache.get("labels"):
            return
        total = len(recs)
        binding = self.db.get_dataset_import(project_name, dataset_name)
        counts = {}
        labeled = 0
        for rec in recs:
            boxes = rec.get("boxes") or []
            if boxes:
                labeled += 1
            for b in boxes:
                lbl = b[-1]
                counts[lbl] = counts.get(lbl, 0) + 1
        if not counts:
            # 无框(分类数据集): 用 labels 索引计数
            counts = {label: len(rs) for label, rs in
                      (cache.get("labels") or {}).items()}
        # 分类数据集: 每张图都有类别, 视为全部已标注
        if binding.get("label_fmt") == "cls":
            labeled = total
        if counts:
            self.db.save_dataset_label_counts(project_name, dataset_name, counts)
        self.db.update_dataset_import(
            project_name, dataset_name,
            binding.get("image_path", ""), binding.get("label_path", ""),
            binding.get("label_fmt", ""), labeled=labeled, total=total)
        self._update_dataset_row_progress(project_name, dataset_name, labeled, total)

    def _update_dataset_row_progress(self, project_name, dataset_name, labeled, total):
        """刷新项目树该数据集节点的进度文本。"""
        ds_item = self._find_dataset_item(project_name, dataset_name)
        if ds_item is None:
            return
        container = self.project_tree.itemWidget(ds_item, 0)
        if container is None:
            return
        pl = container.findChild(QLabel, "datasetRowProgress")
        if pl is not None:
            self._style_progress_chip(pl, labeled, total)
            pl.setText("{}/{}".format(labeled, total))

    def _calc_label_counts(self, project, dataset):
        """统计数据集各标签数量：内存缓存有(已载入)用实时数据并回写 db；未载入用 db 旧值。"""
        cache = self.dataset_cache.get(project, {}).get(dataset, {})
        if cache.get("all") or cache.get("labels"):
            counts = {}
            for rec in cache.get("all", []):
                for b in (rec.get("boxes") or []):
                    lbl = b[-1]
                    counts[lbl] = counts.get(lbl, 0) + 1
            if not counts:
                labels_index = cache.get("labels") or {}
                counts = {label: len(recs) for label, recs in labels_index.items()}
            if counts:
                self.db.save_dataset_label_counts(project, dataset, counts)
            return counts
        return self.db.get_dataset_label_counts(project, dataset)

    def _refresh_dataset_row_progress(self, project_name, dataset_name):
        """根据 db 当前 binding 刷新项目树该数据集节点的进度文本。"""
        ds_item = self._find_dataset_item(project_name, dataset_name)
        if ds_item is None:
            return
        container = self.project_tree.itemWidget(ds_item, 0)
        if container is None:
            return
        pl = container.findChild(QLabel, "datasetRowProgress")
        if pl is None:
            return
        binding = self.db.get_dataset_import(project_name, dataset_name)
        total = binding.get("total", 0) or 0
        labeled = binding.get("labeled", 0) or 0
        self._style_progress_chip(pl, labeled, total)
        pl.setText("{}/{}".format(labeled, total))

    @staticmethod
    def _has_label_file(image_path):
        """判断图像同路径是否存在同名 labelme json。"""
        base, _ = os.path.splitext(image_path)
        return os.path.exists(base + ".json")

    def _delete_images_core(self, project, dataset, paths, delete_local, log_msg=None):
        """
        删除图像核心逻辑(被首页多选删除 + 标注界面单张删除共用):
        - delete_local=True: 删磁盘文件(图像 + 同名 .json/.txt 标注)
        - delete_local=False: 仅 db 记录 add_deleted_image(下次加载跳过)
        - 同步更新: 缓存 index、label_counts、db total/labeled, 刷新显示与进度
        """
        norm = lambda p: os.path.normcase(os.path.normpath(p))
        norm_set = {norm(p) for p in paths}
        binding = self.db.get_dataset_import(project, dataset) or {}
        label_fmt = binding.get("label_fmt", "")
        delete_local_count = 0
        for p in paths:
            if not delete_local:
                continue        # 仅标记模式: 统一走下面的批量接口
            try:
                if os.path.exists(p):
                    os.remove(p)
                    delete_local_count += 1
            except OSError:
                pass
            for ext in self._label_exts_for_fmt(label_fmt):
                fp = os.path.splitext(p)[0] + ext
                try:
                    if os.path.exists(fp):
                        os.remove(fp)
                        delete_local_count += 1
                except OSError:
                    pass
        if not delete_local and paths:
            self.db.add_deleted_images(project, dataset, paths)
        index = self.dataset_cache.get(project, {}).get(dataset)
        if index:
            keep = []
            removed_recs = []
            for r in index["all"]:
                if norm(r.get("image_path", "")) in norm_set:
                    removed_recs.append(r)
                else:
                    keep.append(r)
            index["all"] = keep
            for lbl in list(index["labels"]):
                index["labels"][lbl] = [r for r in index["labels"][lbl]
                                        if norm(r.get("image_path", "")) not in norm_set]
                if not index["labels"][lbl]:
                    del index["labels"][lbl]
            # label_counts: 按被删图的 boxes/labels 减(关键: 之前删除后 label_counts 不会减, 导致统计界面虚高)
            if removed_recs:
                lc = dict(self.db.get_dataset_label_counts(project, dataset))
                for r in removed_recs:
                    boxes = r.get("boxes") or []
                    labels = r.get("labels") or []
                    if boxes:
                        for b in boxes:
                            lbl = b[-1] if isinstance(b, (list, tuple)) else None
                            if lbl and lbl in lc:
                                lc[lbl] = max(0, lc[lbl] - 1)
                    elif labels:
                        for lbl in labels:
                            if lbl in lc:
                                lc[lbl] = max(0, lc[lbl] - 1)
                self.db.save_dataset_label_counts(project, dataset, lc)
        self._write_log(log_msg or "删除图像: {} 张 | 方式={} | 本地删除文件={} | 项目={}, 数据集={}".format(
            len(paths), "删除本地文件" if delete_local else "仅标记不加载",
            delete_local_count, project, dataset))
        self.show_dataset_images(project, dataset)
        self._refresh_dataset_stats(project, dataset)
        self._refresh_label_filter(project, dataset)
        self._refresh_dataset_row_progress(project, dataset)

    @staticmethod
    def _label_exts_for_fmt(fmt):
        """数据集标注格式对应的文件扩展名列表(用于删除同名标注)。"""
        if fmt == ".txt":
            return [".txt"]
        if fmt == ".json":
            return [".json"]
        if fmt == "cls":
            return []
        return [".json", ".txt"]   # 未知/空格式: 两种都尝试

    def _delete_selected_images(self, items):
        """
        首页缩略图多选删除(仅"未标注"筛选下可入口):
        items 是当前页选中的缩略图项, 提取 paths 后走 _delete_paths_with_confirm。
        """
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds or not items:
            return
        paths = [it.image_path for it in items if it.image_path]
        self._delete_paths_with_confirm(paths)

    def _delete_paths_with_confirm(self, paths):
        """
        删除路径列表(首页多选/跨页全选共用):
        弹窗仅确认"从系统删除,不可恢复", 确认后真删(不走"仅标记")。
        """
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds or not paths:
            return
        proj, ds = cur_ds
        clicked = MessageBox.choose(
            self, "删除图像", "将从系统删除所选 {} 张图像？\n\n（图像与同名标注文件不可恢复）".format(len(paths)),
            [("删除", QMessageBox.YesRole),
             ("取消", QMessageBox.RejectRole)],
            informative="图像与同名标注文件将从磁盘删除，不可恢复")
        if clicked is None or clicked != "删除":
            return
        self._delete_images_core(proj, ds, paths, delete_local=True)
