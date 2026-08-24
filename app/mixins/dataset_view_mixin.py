# -*- coding: utf-8 -*-
import sys
import os
import json
CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append('../ui')
from app.annotation.box_item import label_color
from app.annotation_dialog import AnnotationDialog
from paginator import Paginator
from app.label_utils import (normalize_label, label_sort_key)
from app.image_utils import pil_to_qimage, make_uniform_thumb
from app.scene_items import SelectablePixmapItem
from app.import_task import ImportTask
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu, QLabel, QProgressBar, QGraphicsView, QGraphicsScene

try:
    from shiboken6 import isValid as _is_valid
except ImportError:
    _is_valid = lambda obj: obj is not None

try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None


class DatasetViewMixin(object):
    def _init_image_view(self):
        """在 thumbnailsLayout 内创建 QGraphicsView 显示区"""
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setObjectName("imageGraphicsView")
        self.graphics_view.setScene(QGraphicsScene(self.graphics_view))
        self.graphics_view.setRenderHint(QPainter.Antialiasing)
        self.graphics_view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.graphics_view.setBackgroundBrush(QColor("#13151a"))
        self.graphics_view.setDragMode(QGraphicsView.NoDrag)
        self.graphics_view.setCursor(Qt.ArrowCursor)
        self.graphics_view.setMouseTracking(True)
        self.graphics_view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.graphics_view.viewport().installEventFilter(self)
        self.graphics_view.viewport().setMouseTracking(True)
        layout = self.thumbnailsLayout
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        layout.addWidget(self.graphics_view)
        self.graphics_view.setFocusPolicy(Qt.StrongFocus)
        orig_press = self.graphics_view.mousePressEvent

        def _gv_press(ev, _o=orig_press):
            self.graphics_view.setFocus()
            _o(ev)

        self.graphics_view.mousePressEvent = _gv_press
        orig_key = self.graphics_view.keyPressEvent

        def _gv_key(ev, _o=orig_key, _self=self):
            if _self.current_label:
                _o(ev)
                return
            if ev.key() == Qt.Key_A and (ev.modifiers() & Qt.ControlModifier):
                scene = _self.graphics_view.scene()
                for it in scene.items():
                    if isinstance(it, SelectablePixmapItem):
                        it.setSelected(True)
                ev.accept()
                return
            if ev.key() == Qt.Key_Escape:
                _self.graphics_view.scene().clearSelection()
                ev.accept()
                return
            _o(ev)

        self.graphics_view.keyPressEvent = _gv_key
        orig_ctx = self.graphics_view.contextMenuEvent

        def _gv_ctx_menu(ev, _o=orig_ctx):
            hit = self.graphics_view.itemAt(ev.pos())
            if isinstance(hit, SelectablePixmapItem) and not self.current_label:
                if not hit.isSelected():
                    self.graphics_view.scene().clearSelection()
                    hit.setSelected(True)
                selected = [i for i in self.graphics_view.scene().selectedItems()
                            if isinstance(i, SelectablePixmapItem)]
                menu = QMenu(self)
                act = menu.addAction("删除所选图像（{} 张）".format(len(selected)))
                act.triggered.connect(lambda: self._delete_selected_images(selected))
                menu.exec(ev.globalPos())
                ev.accept()
                return
            _o(ev)

        self.graphics_view.contextMenuEvent = _gv_ctx_menu

    def _on_graphics_double_click(self, pos):
        """双击图像显示区:定位到点击的图像记录,进入标注."""
        item = self.graphics_view.itemAt(pos)
        if item is None:
            return
        image_path = item.data(0)
        if not image_path or not os.path.exists(image_path):
            return
        self._open_annotation(image_path)

    def _open_annotation(self, image_path):
        """打开标注对话框"""
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds:
            return
        proj, ds = cur_ds
        index = self.dataset_cache.get(proj, {}).get(ds, {})
        view_data = self._view_data_by_label(index)
        image_list = [r.get("image_path", "") for r in view_data]
        try:
            cur = image_list.index(image_path)
        except ValueError:
            cur = 0

        binding = self.db.get_dataset_import(proj, ds)
        label_paths = binding.get("label_paths") or (
            [binding.get("label_path")] if binding.get("label_path") else [])
        cls_mode = binding.get("label_fmt", "") == "cls"
        dlg = AnnotationDialog(image_list, cur, self.db, proj, ds,
                               label_path=label_paths,
                               label_fmt=binding.get("label_fmt", ""),
                               cls_mode=cls_mode,
                               parent=self)
        dlg.exec()
        changes = getattr(dlg, "_cls_changes", [])
        if changes:
            self._apply_cls_changes(proj, ds, changes)
        deleted = getattr(dlg, "_deleted_labels", [])
        if deleted:
            self._apply_deleted_labels(proj, ds, deleted)
        self._refresh_dataset_labels(proj, ds)
        self._refresh_label_filter(proj, ds)
        self._refresh_annotation_progress(proj, ds)
        self._calc_label_counts(proj, ds)
        if self.current_label:
            self.show_dataset_images(proj, ds)

    def _load_dataset_view(self, project, dataset):
        """
        右键「载入」: 强制重扫并显示数据集图像。
        丢弃旧缓存强制重扫,否则推理/标注界面新写的 labelme json 不会被读入。
        """
        self._current_dataset = (project, dataset)
        self.current_label = "__unlabeled__"
        proj_cache = self.dataset_cache.setdefault(project, {})
        proj_cache.pop(dataset, None)
        self._refresh_label_filter(project, dataset)
        self.show_dataset_images(project, dataset, update_stats=True)

    def _view_data_by_label(self, data):
        """
        按当前筛选 current_label 取 view_data(未标注 / 具体标签 / 全部)。
        用于分页和渲染:分页按筛选后 view_data 计算(不再是全量)。
        """
        cur = self.current_label
        all_records = data.get("all", [])
        if not cur:
            return all_records
        if cur == "__unlabeled__":
            return [r for r in all_records if not r.get("labels")]
        if cur in data.get("labels", {}):
            return data["labels"][cur]
        return []

    def _expand_by_label(self, data):
        """按标签把图像列表按 box 展开为 (rec, box_idx);未标注/全部/分类原样返回。"""
        cur = self.current_label
        if not cur or cur == "__unlabeled__":
            return data
        expanded = []
        for rec in data:
            if rec.get("cls"):
                expanded.append(rec)
                continue
            matched = False
            for box_idx, box in enumerate(rec.get("boxes") or []):
                if len(box) >= 5 and box[4] == cur:
                    expanded.append((rec, box_idx))
                    matched = True
            if not matched and not (rec.get("boxes") or []):
                expanded.append(rec)
        return expanded

    def show_dataset_images(self, project_name, dataset_name, update_stats=False):
        """
        从内存缓存取该数据集图像显示;无缓存则尝试后台加载（多路径合并）。
        update_stats=True 时重扫完成会把 labeled/total 写回 db(右键「载入」场景,
        推理/标注新写的标签 json 重扫后同步统计)。
        """
        proj_cache = self.dataset_cache.get(project_name, {})
        data = proj_cache.get(dataset_name)
        if data:
            self.current_page = 0
            self._render_scene(self._view_data_by_label(data))
            return
        binding = self.db.get_dataset_import(project_name, dataset_name)
        if binding:
            image_paths = binding.get("image_paths") or (
                [binding.get("image_path")] if binding.get("image_path") else [])
            label_paths = binding.get("label_paths") or (
                [binding.get("label_path")] if binding.get("label_path") else [])
            valid_images = [p for p in image_paths if p and os.path.isdir(p)]
            if valid_images:
                excluded = self.db.get_deleted_images(project_name, dataset_name)
                self._start_import_thread(project_name, dataset_name,
                                          valid_images, label_paths,
                                          binding.get("label_fmt", ""),
                                          update_stats=update_stats,
                                          excluded=excluded)
                return
        self._clear_scene()

    @staticmethod
    def _build_dataset_index(result):
        """
        把导入结果构造成 项目-数据集-标签 索引：
        {"all": [全部图像记录...], "labels": {标签名: [图像记录...]}}
        一张图可出现在多个标签下（一图多缺陷）。
        统一归一化 rec.labels / rec.boxes 的标签名（class_N → N），
        保证缓存索引与筛选下拉/重命名/删除使用的标签名一致。
        """
        index = {"all": [], "labels": {}}
        for rec in result:
            if rec.get("labels"):
                rec["labels"] = [normalize_label(l) for l in rec["labels"]]
            if rec.get("boxes"):
                rec["boxes"] = [tuple(b[:-1]) + (normalize_label(b[-1]),)
                                for b in rec["boxes"]]
            rec["rois"] = {}
            index["all"].append(rec)
            for label in set(rec.get("labels") or []):
                index["labels"].setdefault(label, []).append(rec)
        return index

    def _refresh_dataset_labels(self, project_name, dataset_name):
        """
        标注完成后重建缓存中的 labels 索引：
        对每张图读同路径 labelme json 获取最新标注标签(无 json 保留导入时的 labels),
        然后重建 labels 分组索引写回 dataset_cache。
        轻量操作：只读 json,不重新生成缩略图,不扫描磁盘。
        """
        proj_cache = self.dataset_cache.get(project_name, {})
        index = proj_cache.get(dataset_name)
        if not index:
            return
        for rec in index.get("all", []):
            img_path = rec.get("image_path", "")
            base, _ = os.path.splitext(img_path)
            json_path = base + ".json"
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    labels = []
                    boxes = []
                    for shape in data.get("shapes", []):
                        lbl = normalize_label(shape.get("label", ""))
                        if not lbl:
                            continue
                        labels.append(lbl)
                        pts = shape.get("points", [])
                        if len(pts) >= 2:
                            xs = [p[0] for p in pts]
                            ys = [p[1] for p in pts]
                            x, y = int(min(xs)), int(min(ys))
                            w, h = int(max(xs) - min(xs)), int(max(ys) - min(ys))
                            boxes.append((max(0, x), max(0, y), max(1, w), max(1, h), lbl))
                    rec["labels"] = labels
                    rec["boxes"] = boxes if boxes else None
                    rec["rois"] = {}
                    rec["_has_annotation_json"] = True
                except Exception:
                    pass
            elif rec.get("_has_annotation_json"):
                rec["labels"] = []
                rec["boxes"] = None
                rec["rois"] = {}
                rec["_has_annotation_json"] = False

        for rec in index.get("all", []):
            if rec.get("labels"):
                rec["labels"] = [normalize_label(l) for l in rec["labels"]]
            if rec.get("boxes"):
                rec["boxes"] = [tuple(b[:-1]) + (normalize_label(b[-1]),)
                                for b in rec["boxes"]]
        index["labels"] = {}
        for rec in index.get("all", []):
            for label in set(rec.get("labels") or []):
                index["labels"].setdefault(label, []).append(rec)
        proj_cache[dataset_name] = index

    def _clear_scene(self):
        scene = self.graphics_view.scene()
        scene.clear()

    def _reset_image_area(self):
        """
        切到非数据集状态(点项目级别 / 删除数据集)时统一清空图像区
        及所有相关 UI 状态: 分页信息, 当前页码, 标签筛选下拉框、
        标注统计 labelStatsLabel。
        与图像显示区(_clear_scene)一起重置,避免显示残留的旧数据集状态。
        """
        self._clear_scene()
        self.pageInfoLabel.setText("0 / 0")
        self.current_page = 0
        if hasattr(self, "label_filter_combo"):
            self.label_filter_combo.blockSignals(True)
            self.label_filter_combo.clear()
            self.label_filter_combo.addItem("未标注", "__unlabeled__")
            self.label_filter_combo.setCurrentIndex(0)
            self.label_filter_combo.blockSignals(False)
        self.current_label = "__unlabeled__"
        if hasattr(self, "labelStatsLabel"):
            self.labelStatsLabel.setVisible(False)

    def _get_thumb(self, rec):
        """
        懒生成整图缩略图并缓存到 rec["thumb"]（渲染当前页时调用）。
        载入不再全量生成缩略图(大数据集全量解码很慢)，改为渲染到某页时才现场解码该页图像
        翻页/切回/再次筛选命中缓存不重复解码:解码失败也缓存 None。
        """
        if rec.get("thumb") is not None:
            return rec["thumb"]
        qimg = None
        img_path = rec.get("image_path", "")
        if img_path and PILImage is not None:
            try:
                im = PILImage.open(img_path)
                im.draft("RGB", (200, 200))
                im = im.convert("RGB")
                qimg = pil_to_qimage(make_uniform_thumb(im))
            except Exception:
                qimg = None
        rec["thumb"] = qimg
        return qimg

    def _get_rois(self, rec, label):
        """懒生成某标签的 ROI 裁剪小图并缓存到 rec["rois"][label]。"""
        rois = rec.setdefault("rois", {})
        if label in rois:
            return rois[label]
        result = []
        boxes = rec.get("boxes") or []
        img_path = rec.get("image_path", "")
        if boxes and img_path and PILImage is not None:
            try:
                im = PILImage.open(img_path).convert("RGB")
                for box in boxes:
                    if len(box) >= 5 and box[4] == label:
                        x, y, w, h = box[0], box[1], box[2], box[3]
                        crop = im.crop((x, y, x + w, y + h))
                        qimg = pil_to_qimage(make_uniform_thumb(crop, fill=True))
                        if qimg is not None:
                            result.append(qimg)
            except Exception:
                pass
        rois[label] = result
        return result

    def _get_roi_at(self, rec, label, box_idx):
        """取第 box_idx 个匹配 box 的 ROI 缩略图并缓存(区别于 _get_rois 只裁一个,省内存)。"""
        cache = rec.setdefault("rois_by_idx", {}).setdefault(label, {})
        if box_idx in cache:
            return cache[box_idx]
        qimg = None
        boxes = rec.get("boxes") or []
        img_path = rec.get("image_path", "")
        if 0 <= box_idx < len(boxes) and img_path and PILImage is not None:
            box = boxes[box_idx]
            if len(box) >= 5 and box[4] == label:
                try:
                    im = PILImage.open(img_path).convert("RGB")
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    crop = im.crop((x, y, x + w, y + h))
                    qimg = pil_to_qimage(make_uniform_thumb(crop, fill=True))
                except Exception:
                    qimg = None
        cache[box_idx] = qimg
        return qimg

    def _render_scene(self, data):
        """渲染当前页图像网格。按具体标签筛选时每个 cell 一个 ROI(box 计数),
        未标注/全部按整图缩略(图像计数)。"""
        scene = self.graphics_view.scene()
        scene.clear()
        page_size = getattr(self, "page_size", 50)
        cur_label = getattr(self, "current_label", None)
        view_data = self._expand_by_label(data)
        total_pages = max(1, (len(view_data) + page_size - 1) // page_size)
        self.current_page = max(0, min(getattr(self, "current_page", 0), total_pages - 1))
        page_data = list(Paginator(view_data, page_size)[self.current_page])
        cell_w, cell_h = 230, 230
        pad = 10
        cols = max(1, int((self.graphics_view.viewport().width() - pad) // cell_w))
        pos = 0
        for entry in page_data:
            if isinstance(entry, tuple):
                rec, box_idx = entry
                single_box = True
            else:
                rec, box_idx = entry, None
                single_box = False
            if (cur_label and cur_label != "__unlabeled__"
                    and not rec.get("cls")):
                if single_box:
                    qimg = self._get_roi_at(rec, cur_label, box_idx)
                else:
                    qimg = self._get_thumb(rec)
                qimgs = [qimg] if qimg is not None else []
            else:
                qimg = self._get_thumb(rec)
                qimgs = [qimg] if qimg is not None else []
            for qimg in qimgs:
                pix = QPixmap.fromImage(qimg)
                if pix.isNull():
                    continue
                item = SelectablePixmapItem(pix, rec.get("image_path", ""),
                                            labels=rec.get("labels") or [])
                scene.addItem(item)
                row = pos // cols
                col = pos % cols
                x = col * (cell_w + pad) + pad
                y = row * (cell_h + pad) + pad
                card_w = pix.width() + 2 * 4
                card_h = pix.height() + 2 * 4 + 22
                item.setPos(x + (cell_w - card_w) // 2, y + (cell_h - card_h) // 2)
                item.setToolTip(rec.get("image_path", ""))
                item.setData(0, rec.get("image_path", ""))  # 双击定位用
                pos += 1
        scene.setSceneRect(scene.itemsBoundingRect().adjusted(-10, -10, 20, 20))
        if cur_label and cur_label != "__unlabeled__":
            self.pageInfoLabel.setText("第 {}/{} 页 · 共 {} 个".format(
                self.current_page + 1, total_pages, len(view_data)))
        else:
            self.pageInfoLabel.setText("第 {}/{} 页 · 共 {} 张".format(
                self.current_page + 1, total_pages, len(view_data)))
        self.pre_page_btn.setEnabled(self.current_page > 0)
        self.next_page_btn.setEnabled(self.current_page < total_pages - 1)

    def _show_page(self, offset):
        """当前数据集翻页(offset: +1/-1)。分页数据与显示时一致（应用标签筛选）。"""
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds:
            return
        proj, ds = cur_ds
        data = self.dataset_cache.get(proj, {}).get(ds)
        if not data:
            return
        view_data = self._expand_by_label(self._view_data_by_label(data))
        total_pages = max(1, (len(view_data) + self.page_size - 1) // self.page_size)
        self.current_page = max(0, min(self.current_page + offset, total_pages - 1))
        self._render_scene(self._view_data_by_label(data))

    def pre_page(self):
        self._show_page(-1)

    def next_page(self):
        self._show_page(1)

    def _start_import_thread(self, project_name, dataset_name,
                             image_path, label_path="", fmt="",
                             update_stats=False, excluded=None):
        """
        启动后台导入线程
        """
        self._log("开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}".format(
            project_name, dataset_name, image_path, label_path or "(无)", fmt))
        key = (project_name, dataset_name)
        if update_stats:
            self._loading_tasks.pop(key, None)
        elif key in self._loading_tasks:
            return
        ds_item = self._find_dataset_item(project_name, dataset_name)
        progress = None
        progress_lbl = None
        # container = None
        if ds_item is not None:
            container = self.project_tree.itemWidget(ds_item, 0)
            if container is not None:
                progress_lbl = container.findChild(QLabel, "datasetRowProgress")
                if progress_lbl is not None:
                    progress_lbl.setVisible(False)
                progress = QProgressBar(container)
                progress.setRange(0, 100)
                progress.setValue(0)
                progress.setFixedSize(140, 14)
                progress.setTextVisible(True)
                progress.setStyleSheet(
                    "QProgressBar { background-color: rgba(91,140,255,0.25);"
                    " border: none; border-radius: 3px;"
                    " color: #ffffff; font-size: 10px; }"
                    " QProgressBar::chunk { background-color: #5b8cff;"
                    " border-radius: 3px; }")
                h = container.layout()
                h.addWidget(progress)
                h.setAlignment(progress, Qt.AlignVCenter)
        task = ImportTask(image_path, label_path, fmt, parent=self,
                          excluded=excluded,
                          label_ids=self.db.get_dataset_label_ids(
                              project_name, dataset_name))
        self._loading_tasks[key] = task

        def on_progress(v):
            if progress is not None:
                progress.setValue(v)

        def on_finished(result):
            cls_mode = fmt == "cls"
            total = len(result)
            # YOLO txt: 把扫描到的 id→显示名映射持久化,重命名跨重启生效
            if fmt == ".txt" and getattr(task, "_seen_ids", None):
                seen = task._seen_ids
                merged = dict(self.db.get_dataset_label_ids(
                    project_name, dataset_name))
                merged.update(seen)  # 以本次扫描为准
                self.db.save_dataset_label_ids(
                    project_name, dataset_name, merged)
            # 分类模式:每张图都有类别,视为全部已标注
            labeled = total if cls_mode else sum(
                1 for r in result if r.get("boxes"))
            if update_stats:
                new_label_path = label_path
                new_fmt = fmt
                if labeled > 0 and not cls_mode:
                    binding = self.db.get_dataset_import(
                        project_name, dataset_name)
                    old_label = binding.get("label_paths") or (
                        [binding.get("label_path")]
                        if binding.get("label_path") else [])
                    if not old_label:
                        new_label_path = image_path
                        new_fmt = ".json"
                self.db.update_dataset_import(project_name, dataset_name,
                                              image_path, new_label_path,
                                              new_fmt,
                                              labeled=labeled, total=total)
            else:
                binding = self.db.get_dataset_import(project_name, dataset_name)
                labeled = binding.get("labeled", labeled)
                total = binding.get("total", total) or total
            if progress is not None:
                progress.deleteLater()
            if progress_lbl is not None:
                progress_lbl.setVisible(True)
                progress_lbl.setText("{}/{}".format(labeled, total))
            proj_cache = self.dataset_cache.setdefault(project_name, {})
            proj_cache[dataset_name] = self._build_dataset_index(result)
            # 检测/分割按框,分类按类别;持久化供属性页无缓存时展示
            label_counts = {}
            for rec in result:
                for b in (rec.get("boxes") or []):
                    lbl = b[-1]
                    label_counts[lbl] = label_counts.get(lbl, 0) + 1
            if not label_counts:
                for rec in result:
                    for lbl in (rec.get("labels") or []):
                        label_counts[lbl] = label_counts.get(lbl, 0) + 1
            self.db.save_dataset_label_counts(project_name, dataset_name, label_counts)
            counts_str = ", ".join(
                "{}: {}个".format(k, v) for k, v in
                sorted(label_counts.items(), key=lambda kv: label_sort_key(kv[0])))
            self._log("数据集导入完成: {}/{} | 图像 {} 张，已标注 {} 张"
                      " | 标签({}类): {}".format(
                project_name, dataset_name, total, labeled,
                len(label_counts), counts_str or "(无)"))
            self._refresh_dataset_labels(project_name, dataset_name)
            index = proj_cache[dataset_name]
            current_labels = self.db.get_dataset_labels(project_name, dataset_name)
            cleaned = {normalize_label(k): v for k, v in current_labels.items()}
            if cleaned != current_labels:
                self.db.save_dataset_labels(project_name, dataset_name, cleaned)
                current_labels = cleaned
            for lbl in index.get("labels", {}):
                if lbl not in current_labels:
                    self.db.add_dataset_label(project_name, dataset_name,
                                              lbl, label_color(lbl).name())
                    current_labels[lbl] = label_color(lbl).name()
            if self._current_dataset == (project_name, dataset_name):
                self._refresh_label_filter(project_name, dataset_name)
            if getattr(self, "_current_dataset", None) == (project_name, dataset_name):
                self.show_dataset_images(project_name, dataset_name)
            if self._loading_tasks.get(key) is task:
                del self._loading_tasks[key]

        task.progress_updated.connect(on_progress)
        task.finished_signal.connect(on_finished)
        task.finished_signal.connect(task.deleteLater)
        task.start()

    def _find_dataset_item(self, project_name, dataset_name):
        """在项目树中定位数据集节点(展开状态下)。"""
        if not hasattr(self, "project_tree"):
            return None
        for i in range(self.project_tree.topLevelItemCount()):
            proj_item = self.project_tree.topLevelItem(i)
            if proj_item.data(0, Qt.UserRole) == ("project", project_name):
                for j in range(proj_item.childCount()):
                    child = proj_item.child(j)
                    if child.data(0, Qt.UserRole) == ("dataset", project_name, dataset_name):
                        return child
        return None

    def _on_project_tree_clicked(self, item, column):
        """点击：仅记录选中；已缓存的数据集切换显示，未缓存不触发加载。"""
        kind = item.data(0, Qt.UserRole)
        if not kind:
            return
        if kind[0] == "dataset":
            project, dataset = kind[1], kind[2]
            self._current_dataset = (project, dataset)
            if self.dataset_cache.get(project, {}).get(dataset):
                self.current_label = "__unlabeled__"
                self._refresh_label_filter(project, dataset)
                self.show_dataset_images(project, dataset)
            else:
                self._reset_image_area()
        elif kind[0] == "project":
            self._current_dataset = None
            self._reset_image_area()
