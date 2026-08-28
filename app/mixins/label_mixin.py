# -*- coding: utf-8 -*-
import sys
import os
import json

CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append(os.path.join(WORKSPACE_DIRECTORY, 'ui'))
from ui.edit_label import Ui_Dialog as EditLabelUI
from app.core.label_utils import (normalize_label, label_sort_key)
from app.widgets.message_box import MessageBox, ProgressDialog
from app.tasks.merge_task import MergeLabelsTask
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QProgressBar, QComboBox

try:
    from shiboken6 import isValid as _is_valid
except ImportError:
    _is_valid = lambda obj: obj is not None

try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None


class LabelMixin(object):
    def _init_label_filter(self):
        """
        绑定首页设计器已有的标签筛选下拉框（label_comboBox）。
        第一项固定"未标注"。
        """
        self.label_filter_combo = self.label_comboBox
        self.label_filter_combo.clear()
        self.label_filter_combo.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.label_filter_combo.setMinimumContentsLength(12)
        self.label_filter_combo.addItem("未标注", "__unlabeled__")
        self.label_filter_combo.currentIndexChanged.connect(self._on_label_filter_changed)

    def _on_label_filter_changed(self, idx):
        """标签下拉框变更:重新渲染场景(按标签筛选)。"""
        self.current_label = self.label_filter_combo.itemData(idx) or "__unlabeled__"
        self.current_page = 0   # 切换筛选后从第一页开始
        cur_ds = getattr(self, "_current_dataset", None)
        if cur_ds:
            proj, ds = cur_ds
            self.show_dataset_images(proj, ds)

    def _refresh_label_filter(self, project_name, dataset_name):
        """
        切换数据集时刷新首页标签下拉框选项(从 db 读取该数据集标签)。
        "未标注"固定排最后; 数据集全标注时默认选中第一个标签, 否则默认"未标注"。
        """
        if not hasattr(self, "label_filter_combo"):
            return
        self.label_filter_combo.blockSignals(True)
        try:
            self.label_filter_combo.clear()
            labels = {normalize_label(k): v for k, v in
                      self.db.get_dataset_labels(project_name, dataset_name).items()}
            if labels != self.db.get_dataset_labels(project_name, dataset_name):
                self.db.save_dataset_labels(project_name, dataset_name, labels)
            # 标签按排序放前面,"未标注"固定排最后
            for name, color in sorted(labels.items(),
                                      key=lambda kv: label_sort_key(kv[0])):
                self.label_filter_combo.addItem(name, name)
                idx = self.label_filter_combo.count() - 1
                pix = QPixmap(14, 14)
                pix.fill(QColor(color))
                self.label_filter_combo.setItemIcon(idx, QIcon(pix))
            self.label_filter_combo.addItem("未标注", "__unlabeled__")
            if (self.current_label
                    and self.current_label != "__unlabeled__"
                    and self.current_label in labels):
                for i in range(self.label_filter_combo.count()):
                    if self.label_filter_combo.itemData(i) == self.current_label:
                        self.label_filter_combo.setCurrentIndex(i)
                        break
                else:
                    self._set_label_filter_default(project_name, dataset_name, labels)
            else:
                self._set_label_filter_default(project_name, dataset_name, labels)
        finally:
            self.label_filter_combo.blockSignals(False)

    def _set_label_filter_default(self, project_name, dataset_name, labels):
        """数据集全标注 → 默认选第一个标签; 否则默认"未标注"(在下拉最后)。"""
        binding = self.db.get_dataset_import(project_name, dataset_name)
        total = binding.get("total", 0) or 0
        labeled = binding.get("labeled", 0) or 0
        if total > 0 and labeled >= total and labels:
            first = sorted(labels.keys(), key=label_sort_key)[0]
            self.current_label = first
            for i in range(self.label_filter_combo.count()):
                if self.label_filter_combo.itemData(i) == first:
                    self.label_filter_combo.setCurrentIndex(i)
                    break
        else:
            self.current_label = "__unlabeled__"
            self.label_filter_combo.setCurrentIndex(
                self.label_filter_combo.count() - 1)

    def _rebuild_index_labels(self, project_name, dataset_name):
        """按 rec.labels 重建 dataset_cache 的 labels 分组索引。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        index["labels"] = {}
        for rec in index.get("all", []):
            for lbl in (rec.get("labels") or []):
                index["labels"].setdefault(lbl, []).append(rec)

    def _on_rename_label(self):
        """
        首页「编辑」按钮: 重命名当前筛选下拉选中的标签。
        弹 ui/edit_label.py 对话框(类别 + 批量修改为 + 确定)。
        """
        if not self._current_dataset:
            MessageBox.warning(self, "重命名", "请先在左侧选中一个数据集")
            return
        old = self.current_label
        if old == "__unlabeled__" or not old:
            MessageBox.warning(self, "重命名", "请先在筛选下拉框中选择要重命名的标签")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("类别修改")
        ui = EditLabelUI()
        ui.setupUi(dlg)
        ui.label_btn.setText(old)
        ui.new_label_edit.setText(old)
        ui.new_label_edit.selectAll()
        ui.done_btn.clicked.connect(dlg.accept)
        dlg.exec()
        new_name = ui.new_label_edit.text().strip()
        if dlg.result() != QDialog.Accepted:
            return
        if not new_name:
            MessageBox.warning(self, "重命名", "标签名称不能为空")
            return
        if new_name == old:
            return
        proj, ds = self._current_dataset
        # 合并模式(新名已存在)会改写源标签文件,不可逆,需明确确认
        exists = self.db.get_dataset_labels(proj, ds)
        if new_name in exists:
            if not MessageBox.question(
                    self, "合并标签",
                    "标签「{}」已存在。\n"
                    "确定把「{}」的所有标注合并到「{}」吗？\n"
                    "此操作会改写数据集源标签文件，且不可恢复。".format(
                        new_name, old, new_name),
                    default_yes=False):
                return
        self._apply_rename_label(proj, ds, old, new_name)

    def _apply_rename_label(self, project_name, dataset_name, old_name, new_name):
        """
        重命名标签: 内存索引 / 本地 json / db 同步改, 支持合并（新名已存在）。
        合并模式(新名已存在)除了 UI 显示层合并, 还做文件层合并:
        后台线程把标签目录所有 txt 行首 == 旧 id 的行改成新 id,
        使训练也按合并后的类别进行(带项目树进度条)。
        """
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if index:
            for rec in index.get("all", []):
                labels = rec.get("labels") or []
                if old_name in labels:
                    seen = []
                    for lbl in labels:
                        nl = new_name if lbl == old_name else lbl
                        if nl not in seen:
                            seen.append(nl)
                    rec["labels"] = seen
                boxes = rec.get("boxes")
                if boxes:
                    rec["boxes"] = [tuple(b[:-1]) + (new_name,)
                                    if b[-1] == old_name else b for b in boxes]
                rec["rois"] = {}
            self._rebuild_index_labels(project_name, dataset_name)
        self._rename_label_in_files(project_name, dataset_name, old_name, new_name)
        labels = self.db.get_dataset_labels(project_name, dataset_name)
        merge_mode = new_name in labels  # 新名已存在合并类别
        color = labels.pop(old_name, None)
        if color is not None and new_name not in labels:
            labels[new_name] = color
        self.db.save_dataset_labels(project_name, dataset_name, labels)
        # 同步 class_id 映射:值==旧名的项改新名(YOLO 数字 id 的显示名)
        ids = self.db.get_dataset_label_ids(project_name, dataset_name)
        if ids:
            changed = {k: (new_name if v == old_name else v)
                       for k, v in ids.items()}
            if changed != ids:
                self.db.save_dataset_label_ids(
                    project_name, dataset_name, changed)
        if merge_mode:
            self.current_label = new_name
            self._log("合并标签: {} → {} ({}/{}) | 启动后台文件合并, 完成后输出统计".format(
                old_name, new_name, project_name, dataset_name))
            self._merge_label_files(project_name, dataset_name,
                                    old_name, new_name)
            return  # 文件合并是异步的,完成后回调里刷新
        self.current_label = new_name
        self._log("重命名标签: {} → {} ({}/{})".format(
            old_name, new_name, project_name, dataset_name))
        self._refresh_label_filter(project_name, dataset_name)
        self.show_dataset_images(project_name, dataset_name)

    def _merge_label_files(self, project_name, dataset_name, old_name, new_name):
        """合并模式的文件层: 后台改 txt(行首旧 id → 新 id), 项目树行内进度条。"""
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        label_fmt = binding.get("label_fmt", "") or ""
        label_paths = binding.get("label_paths") or (
            [binding.get("label_path")]
            if binding.get("label_path") else [])
        ids = self.db.get_dataset_label_ids(project_name, dataset_name)
        old_ids = [k for k, v in ids.items() if v == old_name]
        new_ids = [k for k, v in ids.items() if v == new_name]
        if label_fmt != ".txt" or not old_ids or not new_ids:
            # 非 txt 或映射不足: 仅显示层合并(标注界面读 json 名已改),直接刷新
            self._after_merge_refresh(project_name, dataset_name,
                                      old_name, new_name, 0)
            return
        task = MergeLabelsTask(label_paths, old_ids, new_ids[0], parent=self)
        ds_item = self._find_dataset_item(project_name, dataset_name)
        progress = None
        progress_lbl = None
        if ds_item is not None:
            container = self.project_tree.itemWidget(ds_item, 0)
            if container is not None:
                progress_lbl = container.findChild(QLabel, "datasetRowProgress")
                if progress_lbl is not None:
                    progress_lbl.setVisible(False)
                progress = QProgressBar(container)
                progress.setObjectName("miniProgressBar")
                progress.setRange(0, 100)
                progress.setValue(0)
                progress.setFixedSize(140, 14)
                progress.setTextVisible(True)
                container.layout().addWidget(progress)
                container.layout().setAlignment(progress, Qt.AlignVCenter)

        def on_progress(v):
            if progress is not None:
                progress.setValue(v)

        def on_done(changed):
            if progress is not None:
                progress.deleteLater()
            if progress_lbl is not None:
                progress_lbl.setVisible(True)
                # 实时重算已标注/总数(cache boxes 已是合并后,与缩略图一致)
                index = self.dataset_cache.get(
                    project_name, {}).get(dataset_name) or {}
                total = len(index.get("all", []))
                labeled = sum(1 for r in index.get("all", [])
                              if r.get("boxes"))
                progress_lbl.setText("{}/{}".format(labeled, total))
            self._after_merge_refresh(project_name, dataset_name,
                                      old_name, new_name, changed)

        task.progress_updated.connect(on_progress)
        task.finished_signal.connect(on_done)
        task.start()
        self._merge_tasks = getattr(self, "_merge_tasks", None)
        if self._merge_tasks is None:
            self._merge_tasks = set()
        self._merge_tasks.add(task)

    def _after_merge_refresh(self, project_name, dataset_name,
                             old_name, new_name, changed, op="merge"):
        """合并/删除完成: 清理 id 映射旧项 + 重算统计 + 刷新缓存/筛选/分页。"""
        # 文件合并后旧 id 已不存在, 从映射移除
        ids = self.db.get_dataset_label_ids(project_name, dataset_name)
        old_ids = {k for k, v in ids.items() if v == old_name}
        if old_ids:
            self.db.save_dataset_label_ids(
                project_name, dataset_name,
                {k: v for k, v in ids.items() if k not in old_ids})
        # 统计重算(cache boxes 已是新名)
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        label_counts = {}
        for rec in (index or {}).get("all", []):
            for b in (rec.get("boxes") or []):
                lbl = b[-1]
                label_counts[lbl] = label_counts.get(lbl, 0) + 1
        if not label_counts:
            for rec in (index or {}).get("all", []):
                for lbl in (rec.get("labels") or []):
                    label_counts[lbl] = label_counts.get(lbl, 0) + 1
        self.db.save_dataset_label_counts(project_name, dataset_name,
                                          label_counts)
        # 清理 db labels dict 中 cache
        self._sync_db_labels_from_cache(project_name, dataset_name)
        counts_str = ", ".join(
            "{}: {}个".format(k, v) for k, v in
            sorted(label_counts.items(), key=lambda kv: label_sort_key(kv[0])))
        if op == "delete":
            self._log("删除标签完成: {} | 修改 {} 个标签文件 | "
                      "删除后标签统计({}类): {}".format(
                old_name, changed, len(label_counts),
                counts_str or "(无)"))
        elif changed:
            self._log("合并标签: {} → {} | 修改 {} 个标签文件 | "
                      "合并后标签统计({}类): {}".format(
                old_name, new_name, changed,
                len(label_counts), counts_str or "(无)"))
        else:
            self._log("合并标签: {} → {} | 无标签文件被修改 | "
                      "合并后标签统计({}类): {}".format(
                old_name, new_name,
                len(label_counts), counts_str or "(无)"))
        self._refresh_label_filter(project_name, dataset_name)
        self.show_dataset_images(project_name, dataset_name)

    def _sync_db_labels_from_cache(self, project_name, dataset_name):
        """
        合并/删除/重命名后清理 db labels dict: 移除 cache 里不再出现的 key,
        新出现的 key 保持缺失(保留旧颜色), 防止下拉残留死标签导致筛选显示异常。
        """
        index = self.dataset_cache.get(project_name, {}).get(dataset_name) or {}
        used = set()
        for rec in index.get("all", []):
            for b in (rec.get("boxes") or []):
                used.add(b[-1])
        current = self.db.get_dataset_labels(project_name, dataset_name)
        if not current:
            return
        cleaned = {k: v for k, v in current.items() if k in used}
        if cleaned != current:
            self.db.save_dataset_labels(project_name, dataset_name, cleaned)

    def _rename_label_in_files(self, project_name, dataset_name, old_name, new_name):
        """本地 labelme json：把 shape.label == old_name 改成 new_name。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        for rec in index.get("all", []):
            img_path = rec.get("image_path", "")
            base, _ = os.path.splitext(img_path)
            json_path = base + ".json"
            if not os.path.exists(json_path):
                continue
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                changed = False
                for shape in data.get("shapes", []):
                    if normalize_label(shape.get("label")) == old_name:
                        shape["label"] = new_name
                        changed = True
                if changed:
                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception:
                continue

    def _on_delete_label(self):
        """首页「删除」按钮：删除当前筛选下拉选中的标签(含确认弹窗)。"""
        if not self._current_dataset:
            MessageBox.warning(self, "删除标签", "请先在左侧选中一个数据集")
            return
        old = self.current_label
        if old == "__unlabeled__" or not old:
            MessageBox.warning(self, "删除标签", "请先在筛选下拉框中选择要删除的标签")
            return
        if not MessageBox.question(
                self, "删除标签", "确定删除标签「{}」吗？\n该标签的所有标注将被删除，且不可恢复。".format(old),
                default_yes=True):
            return
        proj, ds = self._current_dataset
        self._apply_delete_label(proj, ds, old)

    def _apply_delete_label(self, project_name, dataset_name, label_name):
        """删除标签: 内存索引 / 本地 json / db / YOLO txt 同步移除。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if index:
            for rec in index.get("all", []):
                if label_name in (rec.get("labels") or []):
                    rec["labels"] = [l for l in rec["labels"] if l != label_name]
                if rec.get("boxes"):
                    rec["boxes"] = [b for b in rec["boxes"] if b[-1] != label_name]
                rec["rois"] = {}
            self._rebuild_index_labels(project_name, dataset_name)
        self._delete_label_in_files(project_name, dataset_name, label_name)
        self.db.remove_dataset_label(project_name, dataset_name, label_name)
        # 同步移除 class_id 映射中指向该标签的项
        ids = self.db.get_dataset_label_ids(project_name, dataset_name)
        old_ids = [k for k, v in ids.items() if v == label_name]
        if old_ids:
            self.db.save_dataset_label_ids(
                project_name, dataset_name,
                {k: v for k, v in ids.items() if k not in set(old_ids)})
        if self.current_label == label_name:
            self.current_label = "__unlabeled__"
        self._log("删除标签: {} ({}/{})".format(
            label_name, project_name, dataset_name))
        # YOLO txt 文件层删除: 后台删行首==旧 id 的行(否则重新导入标签复活)
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        label_fmt = binding.get("label_fmt", "") or ""
        label_paths = binding.get("label_paths") or (
            [binding.get("label_path")]
            if binding.get("label_path") else [])
        if label_fmt == ".txt" and old_ids and label_paths:
            self._remove_label_files(project_name, dataset_name,
                                     label_name, old_ids)
            return  # 文件删除是异步的,完成后回调里刷新
        self._after_merge_refresh(project_name, dataset_name,
                                  label_name, "", 0, op="delete")

    def _remove_label_files(self, project_name, dataset_name,
                            label_name, old_ids):
        """删除模式的 YOLO txt 文件层: 后台删行(项目树行内进度条)。"""
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        label_paths = binding.get("label_paths") or (
            [binding.get("label_path")]
            if binding.get("label_path") else [])
        task = MergeLabelsTask(label_paths, old_ids, "", parent=self,
                               remove=True)
        ds_item = self._find_dataset_item(project_name, dataset_name)
        progress = None
        progress_lbl = None
        if ds_item is not None:
            container = self.project_tree.itemWidget(ds_item, 0)
            if container is not None:
                progress_lbl = container.findChild(QLabel, "datasetRowProgress")
                if progress_lbl is not None:
                    progress_lbl.setVisible(False)
                progress = QProgressBar(container)
                progress.setObjectName("miniProgressBar")
                progress.setRange(0, 100)
                progress.setValue(0)
                progress.setFixedSize(140, 14)
                progress.setTextVisible(True)
                container.layout().addWidget(progress)
                container.layout().setAlignment(progress, Qt.AlignVCenter)

        def on_progress(v):
            if progress is not None:
                progress.setValue(v)

        def on_done(changed):
            if progress is not None:
                progress.deleteLater()
            if progress_lbl is not None:
                progress_lbl.setVisible(True)
                # 实时重算已标注/总数(cache boxes 已过滤被删的,与缩略图一致)
                index = self.dataset_cache.get(
                    project_name, {}).get(dataset_name) or {}
                total = len(index.get("all", []))
                labeled = sum(1 for r in index.get("all", [])
                              if r.get("boxes"))
                progress_lbl.setText("{}/{}".format(labeled, total))
            self._after_merge_refresh(project_name, dataset_name,
                                      label_name, "", changed, op="delete")

        task.progress_updated.connect(on_progress)
        task.finished_signal.connect(on_done)
        task.start()
        self._merge_tasks = getattr(self, "_merge_tasks", None)
        if self._merge_tasks is None:
            self._merge_tasks = set()
        self._merge_tasks.add(task)

    def _delete_label_in_files(self, project_name, dataset_name, label_name):
        """
        本地 labelme json: 删除 shape.label == label_name 的所有 shapes。
        文件较多时弹进度框；先用文本快速检查跳过不含该标签的文件
        （省去 json.load 解析），仅命中文件才解析+过滤+写回。
        """
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        recs = index.get("all", [])
        progress = None
        if len(recs) > 50:
            progress = ProgressDialog("删除标签", "正在清理标注文件…", self,
                                      maximum=len(recs), cancellable=False)
        try:
            for i, rec in enumerate(recs):
                if progress is not None:
                    progress.set_progress(i)
                img_path = rec.get("image_path", "")
                base, _ = os.path.splitext(img_path)
                json_path = base + ".json"
                if not os.path.exists(json_path):
                    continue
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        text = f.read()
                    if label_name not in text:
                        continue  # 快速跳过：文本不含该标签，无需解析
                    data = json.loads(text)
                    before = len(data.get("shapes", []))
                    data["shapes"] = [s for s in data.get("shapes", [])
                                      if normalize_label(s.get("label")) != label_name]
                    if len(data["shapes"]) != before:
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                except Exception:
                    continue
        finally:
            if progress is not None:
                progress.close()

    def _apply_deleted_labels(self, project_name, dataset_name, label_names):
        """
        清理缓存中的 labels/boxes/rois、重建分组。
        """
        if not label_names:
            return
        for lb in label_names:
            self._delete_label_in_files(project_name, dataset_name, lb)
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        for rec in index.get("all", []):
            rec_labels = rec.get("labels") or []
            new_labels = [l for l in rec_labels if l not in label_names]
            if len(new_labels) != len(rec_labels):
                rec["labels"] = new_labels
            if rec.get("boxes"):
                rec["boxes"] = [b for b in rec["boxes"]
                                if b[-1] not in label_names]
            rec["rois"] = {}
        self._rebuild_index_labels(project_name, dataset_name)

    def _apply_cls_changes(self, project_name, dataset_name, changes):
        """分类数据集修改了类别：同步缓存中的 image_path/cls/labels，重建标签分组。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if not index:
            return
        recs = index.get("all", [])
        for old_p, new_p, new_cls in changes:
            for rec in recs:
                if rec.get("image_path") == old_p:
                    rec["image_path"] = new_p
                    rec["cls"] = new_cls
                    rec["labels"] = [new_cls]
                    rec["thumb"] = None  # 旧缩略图失效,渲染时懒重新生成
                    rec["rois"] = {}
                    break
        index["labels"] = {}
        for rec in recs:
            for lbl in set(rec.get("labels") or []):
                index["labels"].setdefault(lbl, []).append(rec)
