# -*- coding: utf-8 -*-
import sys
import os
CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append('../ui')
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from app.log_dialog import LogDialog
from app.model_dialog import ModelDialog
from app.train.dialogs import TrainDialog
from ui.dataset_properties import Ui_Dialog as DatasetPropertiesUI
from app.message_box import MessageBox
from app.log import write_log
from PySide6.QtGui import QPixmap, QImage
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
        """工具栏「属性」按钮:弹数据集属性对话框(路径 + 标签分布柱状图)。"""
        if not self._current_dataset:
            MessageBox.warning(self, "属性", "请先在左侧选中一个数据集")
            return
        project, dataset = self._current_dataset
        dlg = QDialog(self)
        dlg.setWindowTitle("数据集属性 - {} / {}".format(project, dataset))
        dlg.setWindowFlags(
            dlg.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        ui = DatasetPropertiesUI()
        ui.setupUi(dlg)
        info = self.db.get_dataset_import(project, dataset) or {}
        image_paths = info.get("image_paths") or []
        label_paths = info.get("label_paths") or []
        ui.image_path_line_txt.setText("; ".join(image_paths) or "(未设置)")
        ui.label_path_line_txt.setText("; ".join(label_paths) or "(未设置)")
        ui.image_path_line_txt.setReadOnly(True)
        ui.label_path_line_txt.setReadOnly(True)
        cache = self.dataset_cache.get(project, {}).get(dataset, {})
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
        else:
            counts = self.db.get_dataset_label_counts(project, dataset)
        self._render_label_stats(ui.label_stats_view, project, dataset, counts)
        dlg.exec()

    def _render_label_stats(self, view, project, dataset, label_counts):
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

    def _refresh_annotation_progress(self, project_name, dataset_name):
        """标注完成后重新统计该数据集已标注数量并写 db、刷新树节点。"""
        proj_cache = self.dataset_cache.get(project_name, {})
        index = proj_cache.get(dataset_name)
        if not index:
            return
        total = len(index["all"])
        labeled = 0
        for rec in index["all"]:
            if rec.get("boxes") or self._has_label_file(rec.get("image_path", "")):
                labeled += 1
        binding = self.db.get_dataset_import(project_name, dataset_name)
        self.db.update_dataset_import(
            project_name, dataset_name,
            binding.get("image_path", ""), binding.get("label_path", ""),
            binding.get("label_fmt", ""), labeled=labeled, total=total)
        ds_item = self._find_dataset_item(project_name, dataset_name)
        if ds_item is not None:
            container = self.project_tree.itemWidget(ds_item, 0)
            if container is not None:
                pl = container.findChild(QLabel, "datasetRowProgress")
                if pl is not None:
                    pl.setText("{}/{}".format(labeled, total))

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
        pl.setText("{}/{}".format(labeled, total))

    @staticmethod
    def _has_label_file(image_path):
        """判断图像同路径是否存在同名 labelme json。"""
        base, _ = os.path.splitext(image_path)
        return os.path.exists(base + ".json")

    def _delete_selected_images(self, items):
        """
        删除所选图像：可选删除本地文件 / 仅标记不加载(db 记录,下次加载跳过)。
        同时从内存缓存移除并刷新显示区与总数。
        """
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds or not items:
            return
        proj, ds = cur_ds
        paths = [it.image_path for it in items if it.image_path]
        if not paths:
            return
        clicked = MessageBox.choose(
            self, "删除图像", "是否删除所选 {} 张图像？".format(len(paths)),
            [("删除本地文件", QMessageBox.YesRole),
             ("仅标记不加载", QMessageBox.NoRole),
             ("取消", QMessageBox.RejectRole)],
            informative="删除本地文件：图像文件将从磁盘删除，不可恢复\n"
                        "仅标记不加载：保留文件，但下次加载数据集时自动跳过")
        if clicked is None or clicked == "取消":
            return
        delete_local = (clicked == "删除本地文件")
        norm = lambda p: os.path.normcase(os.path.normpath(p))
        norm_set = {norm(p) for p in paths}
        deleted_local = 0
        for p in paths:
            if delete_local:
                for fp in (p, os.path.splitext(p)[0] + ".json"):
                    try:
                        if os.path.exists(fp):
                            os.remove(fp)
                            deleted_local += 1
                    except OSError:
                        pass
            else:
                self.db.add_deleted_image(proj, ds, p)
        # 从内存缓存移除图像及其标注
        index = self.dataset_cache.get(proj, {}).get(ds)
        if index:
            index["all"] = [r for r in index["all"]
                            if norm(r.get("image_path", "")) not in norm_set]
            for lbl in list(index["labels"]):
                index["labels"][lbl] = [r for r in index["labels"][lbl]
                                        if norm(r.get("image_path", "")) not in norm_set]
                if not index["labels"][lbl]:
                    del index["labels"][lbl]

        # 日志
        self._write_log("删除图像: {} 张 | 方式={} | 本地删除文件={} | 项目={}, 数据集={}".format(
            len(paths), "删除本地文件" if delete_local else "仅标记不加载",
            deleted_local, proj, ds))

        # 刷新显示区(总数/分页同步更新) + 标注进度
        self.show_dataset_images(proj, ds)
        self._refresh_annotation_progress(proj, ds)
