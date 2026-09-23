# -*- coding: utf-8 -*-
import os
import json
from app.core.db import get_paths
from app.annotation.annotation_dialog import AnnotationDialog
from app.widgets.paginator import Paginator
from app.core.constants import (PAGE_SIZE, THUMB_CACHE_MAX,
                                ROI_CACHE_MAX)
from app.mixins.label_mixin import UNLABELED_KEY
from app.core.label_utils import (normalize_label, label_sort_key,
                                  rec_is_labeled, same_dir_json)
from app.core.image_utils import pil_to_qimage, make_uniform_thumb
from app.annotation.scene_items import SelectablePixmapItem
from app.tasks.import_task import ImportTask
from app.widgets.message_box import MessageBox
from PySide6.QtGui import QPixmap, QPainter, QColor, QImage, QImageReader
from PySide6.QtCore import (Qt, Signal, QThread, QMutex, QMutexLocker, QTimer,
                            QRect, QSize)
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtWidgets import QMenu, QGraphicsView, QGraphicsScene


class _RoiDecodeWorker(QThread):
    """
    按类筛选的 ROI 后台解码: 避免首页 UI 线程同步 PIL 全尺寸解码卡顿.
    提交 (image_path, label, box_idx, box) 任务, 后台逐张解码+crop,
    整批完成后 emit (path, label, box_idx, qimg) 列表到主线程.
    """

    batch_done = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._jobs = []
        self._mutex = QMutex()
        self._stop = False

    def submit(self, jobs):
        with QMutexLocker(self._mutex):
            self._jobs.extend(jobs)

    def stop(self):
        with QMutexLocker(self._mutex):
            self._stop = True

    def run(self):
        while True:
            with QMutexLocker(self._mutex):
                if self._stop:
                    return
                jobs = self._jobs
                self._jobs = []
            if not jobs:
                QThread.msleep(30)
                continue
            results = []
            for path, label, box_idx, box in jobs:
                # _decode_roi 只解码标注框所在区域, 不必全图解码
                results.append((path, label, box_idx, _decode_roi(path, box)))
            self.batch_done.emit(results)


class _ThumbDecodeWorker(QThread):
    """整图缩略图后台解码: 首页/全部/未标注筛选不阻塞 UI."""

    batch_done = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._jobs = []
        self._mutex = QMutex()
        self._stop = False

    def submit(self, paths):
        with QMutexLocker(self._mutex):
            self._jobs.extend(paths)

    def stop(self):
        with QMutexLocker(self._mutex):
            self._stop = True

    def run(self):
        while True:
            with QMutexLocker(self._mutex):
                if self._stop:
                    return
                jobs = self._jobs
                self._jobs = []
            if not jobs:
                QThread.msleep(30)
                continue
            results = []
            for path in jobs:
                qimg = None
                try:
                    im = PILImage.open(path)
                    im.draft("RGB", (200, 200))
                    im = im.convert("RGB")
                    qimg = pil_to_qimage(make_uniform_thumb(im))
                except Exception:
                    pass
                results.append((path, qimg))
            self.batch_done.emit(results)


_THUMB_PLACEHOLDER = None


def _thumb_placeholder():
    """统一的缩略图占位(灰块), 后台解码完成前先垫底."""
    global _THUMB_PLACEHOLDER
    if _THUMB_PLACEHOLDER is None:
        _THUMB_PLACEHOLDER = QImage(200, 200, QImage.Format_RGB32)
        _THUMB_PLACEHOLDER.fill(QColor(56, 58, 66))
    return _THUMB_PLACEHOLDER


try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None


def _decode_roi(path, box, size=200):
    if not box or len(box) < 4:
        return None
    try:
        x, y, w, h = (int(box[0]), int(box[1]), int(box[2]), int(box[3]))
    except (TypeError, ValueError):
        return None
    if w <= 0 or h <= 0:
        return None
    x0, y0 = max(0, x), max(0, y)
    w0, h0 = w, h
    try:
        reader = QImageReader(path)
        reader.setAutoTransform(True)
        full = reader.size()
        if full.isValid():
            w0 = min(x + w, full.width()) - x0
            h0 = min(y + h, full.height()) - y0
            if w0 <= 0 or h0 <= 0:
                return None
            reader.setClipRect(QRect(x0, y0, w0, h0))
            reader.setScaledSize(QSize(size, size))
            qimg = reader.read()
            if qimg is not None and not qimg.isNull():
                return qimg
    except Exception:
        pass
    if PILImage is None:
        return None
    try:
        im = PILImage.open(path).convert("RGB")
        crop = im.crop((x0, y0, x0 + w0, y0 + h0))
        return pil_to_qimage(make_uniform_thumb(crop, fill=True))
    except Exception:
        return None


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

        def _gv_press(ev, _o=orig_press, _self=self):
            _self.graphics_view.setFocus()
            if ev.button() == Qt.LeftButton:
                # 左键点击缩略图 = 手动选择, 退出跨页全选模式
                if isinstance(_self.graphics_view.itemAt(ev.pos()), SelectablePixmapItem):
                    _self._select_all_mode = False
            elif ev.button() == Qt.RightButton:
                hit = _self.graphics_view.itemAt(ev.pos())
                if (isinstance(hit, SelectablePixmapItem)
                        and _self._unlabeled_selected()):
                    if not hit.isSelected():
                        _self.graphics_view.scene().clearSelection()
                        hit.setSelected(True)
                        # 改变了选择(单选某图), 退出跨页全选模式
                        _self._select_all_mode = False
                    ev.accept()
                    return
            _o(ev)

        self.graphics_view.mousePressEvent = _gv_press
        orig_key = self.graphics_view.keyPressEvent

        def _gv_key(ev, _o=orig_key, _self=self):
            if not _self._unlabeled_selected():
                _o(ev)
                return
            if ev.key() == Qt.Key_A and (ev.modifiers() & Qt.ControlModifier):
                scene = _self.graphics_view.scene()
                for it in scene.items():
                    if isinstance(it, SelectablePixmapItem):
                        it.setSelected(True)
                _self._select_all_mode = True
                ev.accept()
                return
            if ev.key() == Qt.Key_Escape:
                _self.graphics_view.scene().clearSelection()
                _self._select_all_mode = False
                ev.accept()
                return
            _o(ev)

        self.graphics_view.keyPressEvent = _gv_key
        orig_ctx = self.graphics_view.contextMenuEvent

        def _gv_ctx_menu(ev, _o=orig_ctx, _self=self):
            hit = _self.graphics_view.itemAt(ev.pos())
            if (isinstance(hit, SelectablePixmapItem)
                    and _self._unlabeled_selected()):
                if not hit.isSelected():
                    _self.graphics_view.scene().clearSelection()
                    hit.setSelected(True)
                selected = [i for i in _self.graphics_view.scene().selectedItems()
                            if isinstance(i, SelectablePixmapItem)]
                menu = QMenu(_self)
                if getattr(_self, "_select_all_mode", False):
                    cur_ds = _self._current_dataset
                    index = (_self.dataset_cache.get(cur_ds[0], {}).get(cur_ds[1], {})
                             if cur_ds else {})
                    unlabeled = _self._filter_records(index)
                    all_paths = [r.get("image_path", "") for r in unlabeled if r.get("image_path")]
                    act = menu.addAction(
                        QC.translate("DatasetViewMixin",
                                     "删除全部未标注图像({} 张)").format(len(all_paths)))
                    act.triggered.connect(
                        lambda: _self._delete_paths_with_confirm(all_paths))
                else:
                    act = menu.addAction(
                        QC.translate("DatasetViewMixin",
                                     "删除所选图像({} 张)").format(len(selected)))
                    act.triggered.connect(lambda: _self._delete_selected_images(selected))
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
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds:
            return
        proj, ds = cur_ds
        index = self.dataset_cache.get(proj, {}).get(ds, {})
        view_data = self._filter_records(index)
        image_list = [r.get("image_path", "") for r in view_data]
        try:
            cur = image_list.index(image_path)
        except ValueError:
            cur = 0

        binding = self.db.get_dataset_import(proj, ds)
        label_paths = get_paths(binding, "label")
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
        modified = getattr(dlg, "_modified_paths", set()) or set()
        if not changes and not deleted and not modified:
            # 会话无任何改动: 缓存/db/文件均未变化, 收尾全跳过(9w 图省一次全量重建)
            return
        # 只重读本会话真正写过 json 的图(框增删改); 整标签删除/类别修改已由
        # _apply_* 就地同步, 无框改动时无需读 json, 仅统一重建分组与 db 计数.
        self._refresh_dataset_labels(proj, ds, rescan=bool(modified),
                                     only_paths=modified or None)
        self._refresh_label_filter(proj, ds)
        self._refresh_dataset_stats(proj, ds)
        self.show_dataset_images(proj, ds)
        self._sync_label_paths_from_json(proj, ds)

    def _sync_label_paths_from_json(self, project_name, dataset_name):
        """
        标注后扫描: 哪些 image_path 目录含 labelme json, 把这些目录追加到 db label_paths.
        仅 labelme 模式(.json)有效; yolo/cls 模式不扫描.
        """
        binding = self.db.get_dataset_import(project_name, dataset_name)
        if not binding or binding.get("label_fmt", "") != ".json":
            return
        img_paths = get_paths(binding, "image")
        old_lbls = get_paths(binding, "label")
        new_lbls = list(old_lbls)
        added = False
        for ip in img_paths:
            if not ip or not os.path.isdir(ip) or ip in new_lbls:
                continue
            try:
                has_json = any(fn.lower().endswith('.json')
                                for fn in os.listdir(ip))
            except OSError:
                continue
            if has_json:
                new_lbls.append(ip)
                added = True
        if added:
            self.db.update_dataset_import(project_name, dataset_name,
                                          img_paths, new_lbls,
                                          binding.get("label_fmt", ""),
                                          labeled=None, total=None)

    def _reload_dataset(self, project, dataset):
        """清缓存重扫, 让推理写在图像同目录的 json 回流成标签."""
        # 不能用 get_dataset_import 判"没导入": 数据集存在它就返回非空 dict, 永远为真;
        # 能不能重载只看有没有真实存在的图像目录(与 show_dataset_images 同口径)
        binding = self.db.get_dataset_import(project, dataset)
        if not [p for p in get_paths(binding, "image") if p and os.path.isdir(p)]:
            self._log(QC.translate("DatasetViewMixin", "重载跳过: 数据集 {}/{} 无图像目录").format(project, dataset))
            MessageBox.warning(self, QC.translate("DatasetViewMixin", "重载"),
                               QC.translate("DatasetViewMixin",
                                            "该数据集还没有图像目录, 请先右键\"导入\""))
            return
        if (project, dataset) in self._loading_tasks:
            self._log(QC.translate("DatasetViewMixin", "重载跳过: 数据集 {}/{} 正在载入").format(project, dataset))
            return
        self._log(QC.translate("DatasetViewMixin", "重载数据集: {}/{}").format(project, dataset))
        self.project_tree.select_dataset(project, dataset)
        self._load_dataset_view(project, dataset)

    def _load_dataset_view(self, project, dataset):
        """丢缓存强制重扫并显示, 推理/标注新写的 json 靠它读入."""
        self._current_dataset = (project, dataset)
        self._set_filter_all()
        self.current_page = 0
        proj_cache = self.dataset_cache.setdefault(project, {})
        proj_cache.pop(dataset, None)
        self.project_tree.set_row_loaded(project, dataset, False)
        self._refresh_label_filter(project, dataset)
        self.show_dataset_images(project, dataset, update_stats=True)

    def _filter_records(self, data):
        """
        当前筛选命中的图像记录, 保持 index["all"] 的原始顺序.
        所有图像 → 全部; 否则是所选各项的并集(未标注按"没有有效框"判).
        分页与渲染都以它的长度为准, 所以勾选一变页数就跟着变.
        """
        all_records = data.get("all", [])
        if self.filter_all:
            return all_records
        picked = self.filter_labels
        if not picked:
            return []
        want_unlabeled = UNLABELED_KEY in picked
        wanted = {k for k in picked if k != UNLABELED_KEY}
        out = []
        for rec in all_records:
            # _lbl_set 由索引重建处收口预存, 省掉逐条新建 set 的分配;
            # 万一某条没经过重建(新建/兜底路径), 现场构造保证不漏图.
            lbls = rec.get("_lbl_set")
            if lbls is None:
                lbls = frozenset(rec.get("labels") or ())
            hit = bool(wanted & lbls)
            if not hit and want_unlabeled and not rec_is_labeled(rec):
                hit = True
            if hit:
                out.append(rec)
        return out

    def _expand_by_label_filter(self, records):
        """
        标签筛选下把记录按 box 展开成 (rec, box_idx), 一个命中框占一个格子;
        多选时各标签的格子就混在同一页里, 顺序仍是图像顺序.
        所有图像 / 只选未标注 / 分类数据集 原样返回(一图一格).
        """
        if not self._by_box_mode():
            return records
        wanted = {k for k in self.filter_labels if k != UNLABELED_KEY}
        out = []
        for rec in records:
            if rec.get("cls"):
                out.append(rec)
                continue
            boxes = rec.get("boxes") or []
            if not boxes:
                out.append(rec)
                continue
            for box_idx, box in enumerate(boxes):
                if len(box) >= 5 and box[4] in wanted:
                    out.append((rec, box_idx))
        return out

    def show_dataset_images(self, project_name, dataset_name, update_stats=False):
        """
        从内存缓存取该数据集图像显示;无缓存则尝试后台加载(多路径合并).
        update_stats=True 时重扫完成会把 labeled/total 写回 db(双击载入场景,
        推理/标注新写的标签 json 重扫后同步统计).
        """
        self._select_all_mode = False
        proj_cache = self.dataset_cache.get(project_name, {})
        data = proj_cache.get(dataset_name)
        if data:
            bpi = getattr(self, "_by_path_index", None)
            if not (bpi and bpi.get("ds") == (project_name, dataset_name)):
                # 缓存命中直接渲染时补齐 path->rec 索引(仅切换数据集时一次, 低频)
                self._by_path_index = {
                    "ds": (project_name, dataset_name),
                    "map": {r.get("image_path"): r for r in data.get("all", [])},
                }
            self._render_scene(self._filter_records(data))
            return
        binding = self.db.get_dataset_import(project_name, dataset_name)
        if binding:
            image_paths = get_paths(binding, "image")
            label_paths = get_paths(binding, "label")
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
        把导入结果构造成 项目-数据集-标签 索引:
        {"all": [全部图像记录...], "labels": {标签名: [图像记录...]}}
        一张图可出现在多个标签下(一图多缺陷).
        统一归一化 rec.labels / rec.boxes 的标签名(class_N → N),
        保证缓存索引与筛选下拉/重命名/删除使用的标签名一致.
        """
        index = {"all": [], "labels": {}}
        for rec in result:
            if rec.get("labels"):
                rec["labels"] = [normalize_label(l) for l in rec["labels"]]
            if rec.get("boxes"):
                rec["boxes"] = [tuple(b[:-1]) + (normalize_label(b[-1]),)
                                for b in rec["boxes"]]
            index["all"].append(rec)
            lbls = rec.get("labels") or ()
            rec["_lbl_set"] = frozenset(lbls)
            for label in set(lbls):
                index["labels"].setdefault(label, []).append(rec)
        return index

    def _refresh_dataset_labels(self, project_name, dataset_name, rescan=False,
                                only_paths=None):
        """
        重建缓存中的 labels 索引.
        rescan=False(导入/载入完成): 缓存 rec 刚由后台扫描生成, labels/boxes
          已是最新, 跳过逐图 json 重读, 只做归一化与索引重建(纯内存, 万级图不卡).
        rescan=True(标注后): 逐图读同路径 labelme json 获取最新标注标签
          (无 json 保留导入时的 labels), 再重建 labels 分组索引写回 dataset_cache.
          only_paths 提供时只重读这些图(标注会话真正改过的 json), 避免 9w 图
          每次关标注全量重扫; 不提供时保持全量语义.
          轻量操作: 只读 json, 不重新生成缩略图, 不扫描目录树.
        """
        proj_cache = self.dataset_cache.get(project_name, {})
        index = proj_cache.get(dataset_name)
        if not index:
            return
        if rescan:
            for rec in index.get("all", []):
                img_path = rec.get("image_path", "")
                if only_paths is not None and img_path not in only_paths:
                    continue
                json_path = same_dir_json(img_path)
                if json_path:
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
                        rec["rois_by_idx"] = {}
                        rec["_has_annotation_json"] = True
                    except Exception:
                        pass
                elif rec.get("_has_annotation_json"):
                    rec["labels"] = []
                    rec["boxes"] = None
                    rec["rois_by_idx"] = {}
                    rec["_has_annotation_json"] = False

        for rec in index.get("all", []):
            if rec.get("labels"):
                rec["labels"] = [normalize_label(l) for l in rec["labels"]]
            if rec.get("boxes"):
                rec["boxes"] = [tuple(b[:-1]) + (normalize_label(b[-1]),)
                                for b in rec["boxes"]]
        index["labels"] = {}
        for rec in index.get("all", []):
            lbls = rec.get("labels") or ()
            rec["_lbl_set"] = frozenset(lbls)
            for label in set(lbls):
                index["labels"].setdefault(label, []).append(rec)
        proj_cache[dataset_name] = index
        # 构建/刷新 path->rec 索引(一次性 O(N), 供缩略图/ROI 回调 O(1) 定位,
        # 避免每个批次全量重建 dict); 带数据集标识, 切换数据集时自动失效.
        self._by_path_index = {
            "ds": (project_name, dataset_name),
            "map": {r.get("image_path"): r for r in index.get("all", [])},
        }
        self._sync_labels_to_db(project_name, dataset_name, index["labels"])
        self._sync_db_labels_from_cache(project_name, dataset_name)

    def _clear_scene(self):
        scene = self.graphics_view.scene()
        scene.clear()

    def _reset_image_area(self):
        """
        切到非数据集状态(点项目级别 / 删除数据集)时统一清空图像区
        及所有相关 UI 状态: 分页信息, 当前页码, 标签筛选按钮与面板,
        标注统计 labelStatsLabel.
        与图像显示区(_clear_scene)一起重置,避免显示残留的旧数据集状态.
        """
        self._clear_scene()
        self._reset_page_info()
        self.current_page = 0
        self._reset_label_filter_text()
        if hasattr(self, "labelStatsLabel"):
            self.labelStatsLabel.setVisible(False)

    def _get_thumb(self, rec):
        """整图缩略图: 命中缓存直接返回, 未命中提交后台解码并先返回占位图."""
        thumb = rec.get("thumb")
        if thumb is not None:
            rec["_thumb_t"] = self._img_clock_now()
            return thumb
        img_path = rec.get("image_path", "")
        if img_path:
            if img_path not in getattr(self, "_thumb_pending", set()):
                self._ensure_thumb_worker()
                self._thumb_pending.add(img_path)
                self._thumb_worker.submit([img_path])
        return _thumb_placeholder()

    def _ensure_thumb_worker(self):
        """懒创建缩略图后台解码 worker(首页/翻页不卡顿)."""
        if getattr(self, "_thumb_worker", None) is None:
            self._thumb_worker = _ThumbDecodeWorker(self)
            self._thumb_worker.batch_done.connect(self._on_thumb_batch_done)
            self._thumb_worker.start()
            self._thumb_pending = set()
            self._thumb_refresh_timer = QTimer(self)
            self._thumb_refresh_timer.setSingleShot(True)
            self._thumb_refresh_timer.setInterval(120)
            self._thumb_refresh_timer.timeout.connect(
                lambda: self._roi_redraw())
        return self._thumb_worker

    def _on_thumb_batch_done(self, results):
        """缩略图解码完成: 回写 rec 缓存, 有变化则防抖重渲当前页.
        复用 _by_path_index 做 O(1) 定位, 不再每次全量重建 by_path dict;
        内存淘汰走 _throttled_evict 节流(翻页/切筛选仍有 _render_scene 全量兜底)."""
        if getattr(self, "_closing", False):
            return
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds:
            return
        proj, ds = cur_ds
        index = self.dataset_cache.get(proj, {}).get(ds)
        if not index:
            return
        bpi = getattr(self, "_by_path_index", None)
        by_path = bpi.get("map") if bpi and bpi.get("ds") == (proj, ds) else {}
        changed = False
        for path, qimg in results:
            if path in getattr(self, "_thumb_pending", set()):
                self._thumb_pending.discard(path)
            rec = by_path.get(path)
            if rec is not None and rec.get("thumb") is None:
                rec["thumb"] = qimg if qimg is not None else _thumb_placeholder()
                rec["_thumb_t"] = self._img_clock_now()
                changed = True
        if changed and self._current_dataset == cur_ds:
            self._thumb_refresh_timer.start()
        self._throttled_evict()

    def _ensure_roi_worker(self):
        """懒创建 ROI 后台解码 worker(首页按类筛选首屏不卡顿)."""
        if getattr(self, "_roi_worker", None) is None:
            self._roi_worker = _RoiDecodeWorker(self)
            self._roi_worker.batch_done.connect(self._on_roi_batch_done)
            self._roi_worker.start()
            self._roi_pending = set()
            self._roi_refresh_timer = QTimer(self)
            self._roi_refresh_timer.setSingleShot(True)
            self._roi_refresh_timer.setInterval(120)
            self._roi_refresh_timer.timeout.connect(
                lambda: self._roi_redraw())
        return self._roi_worker

    def _roi_for_render(self, rec, box_idx):
        """按 box 取 ROI: 缓存命中直接返回; 未命中先给灰块占位并提交后台解码
        (不显示整图缩略图, 避免"灰块→整图闪现→ROI"三段式), 解好自动重渲当前页.
        缓存按 box 自己的标签分桶, 多标签混排时各框互不串图.
        """
        boxes = rec.get("boxes") or []
        if not (0 <= box_idx < len(boxes)) or len(boxes[box_idx]) < 5:
            return _thumb_placeholder()
        label = boxes[box_idx][4]
        cache = rec.setdefault("rois_by_idx", {}).setdefault(label, {})
        if box_idx in cache:
            rec["_roi_t"] = self._img_clock_now()
            # 解码失败缓存为 None: 回退灰块占位, 不显示空白 cell
            return cache[box_idx] if cache[box_idx] is not None else _thumb_placeholder()
        key = (rec.get("image_path", ""), label, box_idx)
        if key not in getattr(self, "_roi_pending", set()):
            self._ensure_roi_worker()
            self._roi_pending.add(key)
            self._roi_worker.submit([(key[0], label, box_idx, boxes[box_idx])])
        return _thumb_placeholder()

    def _on_roi_batch_done(self, results):
        """后台 ROI 解码完成: 回写 rec 缓存(成功/失败都缓存, 防重复请求),
        有变化则防抖重渲当前页. 复用 _by_path_index O(1) 定位;
        内存淘汰走 _throttled_evict 节流(翻页/切筛选仍有 _render_scene 全量兜底)."""
        if getattr(self, "_closing", False):
            return
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds:
            return
        proj, ds = cur_ds
        index = self.dataset_cache.get(proj, {}).get(ds)
        if not index:
            return
        bpi = getattr(self, "_by_path_index", None)
        by_path = bpi.get("map") if bpi and bpi.get("ds") == (proj, ds) else {}
        changed = False
        for path, label, box_idx, qimg in results:
            key = (path, label, box_idx)
            if key in getattr(self, "_roi_pending", set()):
                self._roi_pending.discard(key)
            rec = by_path.get(path)
            if rec is not None:
                cache = rec.setdefault("rois_by_idx", {}).setdefault(label, {})
                if box_idx not in cache:
                    cache[box_idx] = qimg
                    rec["_roi_t"] = self._img_clock_now()
                    changed = True
        if changed and self._current_dataset == cur_ds:
            self._roi_refresh_timer.start()
        self._throttled_evict()

    def _throttled_evict(self):
        """节流 LRU 淘汰: 后台批次回调高频触发, 全量 O(N log N) 淘汰每 ~30 批次一次;
        翻页/切筛选走 _render_scene 的全量淘汰, 不依赖本方法."""
        self._batch_evict_count = getattr(self, "_batch_evict_count", 0) + 1
        if self._batch_evict_count >= 30:
            self._batch_evict_count = 0
            self._evict_img_cache()

    def _roi_redraw(self):
        """防抖重渲当前页(ROI 后台解码完成)."""
        cur_ds = getattr(self, "_current_dataset", None)
        if cur_ds:
            self.show_dataset_images(cur_ds[0], cur_ds[1])

    def _img_clock_now(self):
        """单调递增访问时钟(无 time 精度问题)."""
        c = getattr(self, "_img_clock", 0) + 1
        self._img_clock = c
        return c

    def _evict_img_cache(self):
        """
        QImage 图像缓存 LRU 淘汰: thumb/ROI 超过各自上限时,
        释放最久未访问且不在当前页的缓存(置 None / 清空 rois_by_idx).
        收集时只 append rec 本身, 不建 (时间, rec) 元组; 且只有真超上限才 sort
        (稳态下缓存贴着上限, 多一轮排序纯属浪费; 实测 Python 层 nsmallest
        拼不过 C 层 sort).
        淘汰后渲染时懒重建(与 label_mixin 主动失效 rec["thumb"]=None 同机制),
        保证大图集翻页/按类筛选下内存有界, 不持续增长.
        只动 QImage 缓存, 不碰 rec 元数据与 labels 索引, 分页/统计/标注不受影响.
        """
        cur = getattr(self, "_current_dataset", None)
        if not cur:
            return
        index = self.dataset_cache.get(cur[0], {}).get(cur[1])
        if not index:
            return
        t_max = getattr(self, "_thumb_cache_max", THUMB_CACHE_MAX)
        r_max = getattr(self, "_roi_cache_max", ROI_CACHE_MAX)
        records = index.get("all", [])
        # 全部装得下时必定不超限, 连遍历都免了(几千张以内的小数据集常见)
        if len(records) <= t_max and len(records) <= r_max:
            return
        protected = getattr(self, "_current_page_paths", None) or set()
        placeholder = _thumb_placeholder()
        thumbs = []
        rois = []
        for rec in records:
            if rec.get("image_path", "") in protected:
                continue
            th = rec.get("thumb")
            if th is not None and th is not placeholder:
                thumbs.append(rec)
            if rec.get("rois_by_idx"):
                rois.append(rec)
        if len(thumbs) > t_max:
            thumbs.sort(key=lambda r: r.get("_thumb_t", 0), reverse=True)
            for rec in thumbs[t_max:]:
                rec["thumb"] = None
        if len(rois) > r_max:
            rois.sort(key=lambda r: r.get("_roi_t", 0), reverse=True)
            for rec in rois[r_max:]:
                rec["rois_by_idx"] = {}

    def _render_scene(self, records):
        """
        渲染当前页图像网格. 选到真实标签时每个 cell 一个 ROI(按命中框计数),
        所有图像/未标注按整图缩略(按图像计数); 多选时两者混在同一页.
        """
        scene = self.graphics_view.scene()
        scene.clear()
        page_size = getattr(self, "page_size", PAGE_SIZE)
        view_data = self._expand_by_label_filter(records)
        total_pages = max(1, (len(view_data) + page_size - 1) // page_size)
        self.current_page = max(0, min(getattr(self, "current_page", 0),
                                       total_pages - 1))
        page_data = list(Paginator(view_data, page_size)[self.current_page])
        self._current_page_paths = set()
        for entry in page_data:
            rec = entry[0] if isinstance(entry, tuple) else entry
            if rec.get("image_path"):
                self._current_page_paths.add(rec.get("image_path", ""))
        cell_w, cell_h = 230, 230
        pad = 10
        cols = max(1, int((self.graphics_view.viewport().width() - pad) // cell_w))
        pos = 0
        for entry in page_data:
            if isinstance(entry, tuple):
                rec, box_idx = entry
                qimg = self._roi_for_render(rec, box_idx)
            else:
                rec = entry
                qimg = self._get_thumb(rec)
            if qimg is None:
                continue
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
        # 同页重复重绘(批次解码完成后回渲)不做全量淘汰: 缓存增长只来自当前页,
        # 有 _throttled_evict 兜底; 换页/换筛选才是缓存规模真会变的时机.
        paths = self._current_page_paths
        if paths != getattr(self, "_evict_page_paths", None):
            self._evict_page_paths = paths
            self._evict_img_cache()
        self._set_page_info(self._by_box_mode(), total_pages, len(view_data))

    def _set_page_info(self, by_box, total_pages, count):
        """底栏只放"第 N / M 页", 当前页数字化亮; 总数与量词进 tooltip, 免得居中那组随内容横移."""
        self._page_info_state = (by_box, total_pages, count)
        if not count:
            self._reset_page_info()
            return
        self.pageInfoLabel.setText(
            QC.translate("DatasetViewMixin", "第 {} / {} 页").format(
                '<span style="color:#e8eaf0">{}</span>'.format(self.current_page + 1),
                total_pages))
        if by_box:
            tip = QC.translate("DatasetViewMixin", "第 {}/{} 页 · 共 {} 个")
        else:
            tip = QC.translate("DatasetViewMixin", "第 {}/{} 页 · 共 {} 张")
        self.pageInfoLabel.setToolTip(tip.format(
            self.current_page + 1, total_pages, count))
        self.pre_page_btn.setEnabled(self.current_page > 0)
        self.next_page_btn.setEnabled(self.current_page < total_pages - 1)

    def _reset_page_info(self):
        """图像区清空 / 空数据集: 没有页可翻, 文案与两个按钮一起复位."""
        self._page_info_state = None
        self.pageInfoLabel.setText(QC.translate("DatasetViewMixin", "暂无数据"))
        self.pageInfoLabel.setToolTip("")
        self.pre_page_btn.setEnabled(False)
        self.next_page_btn.setEnabled(False)

    def _refresh_page_info(self):
        """换语言后重刷底栏分页文案(retranslateUi 管不到运行时拼的这行)."""
        state = getattr(self, "_page_info_state", None)
        if state:
            self._set_page_info(*state)
        else:
            self._reset_page_info()

    def _show_page(self, offset):
        """当前数据集翻页(offset: +1/-1). 分页数据与显示时一致(应用标签筛选)."""
        cur_ds = getattr(self, "_current_dataset", None)
        if not cur_ds:
            return
        data = self.dataset_cache.get(cur_ds[0], {}).get(cur_ds[1])
        if not data:
            return
        # 越界交给 _render_scene 夹到合法页, 这里不必先算一遍总页数
        self.current_page += offset
        self._render_scene(self._filter_records(data))

    def pre_page(self):
        self._show_page(-1)

    def next_page(self):
        self._show_page(1)

    def _start_import_thread(self, project_name, dataset_name,
                             image_path, label_path="", fmt="",
                             update_stats=False, excluded=None,
                             write_db=True):
        self._log(QC.translate("DatasetViewMixin", "开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}").format(
            project_name, dataset_name, image_path, label_path or QC.translate("DatasetViewMixin", "(无)"), fmt))
        key = (project_name, dataset_name)
        if update_stats:
            self._loading_tasks.pop(key, None)
        elif key in self._loading_tasks:
            return
        self.project_tree.set_row_task(project_name, dataset_name, 0)
        task = ImportTask(image_path, label_path, fmt, parent=self,
                          excluded=excluded,
                          label_ids=self.db.get_dataset_label_ids(
                              project_name, dataset_name))
        self._loading_tasks[key] = task

        def on_progress(v):
            self.project_tree.set_row_task(project_name, dataset_name, v)

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
            labeled = total if cls_mode else sum(
                1 for r in result if rec_is_labeled(r))
            if update_stats:
                new_label_path = label_path
                new_fmt = fmt
                if labeled > 0 and not cls_mode:
                    binding = self.db.get_dataset_import(
                        project_name, dataset_name)
                    old_label = get_paths(binding, "label")
                    if not old_label:
                        new_label_path = image_path
                        new_fmt = ".json"

                if write_db:
                    self.db.update_dataset_import(project_name, dataset_name,
                                                  image_path, new_label_path,
                                                  new_fmt,
                                                  labeled=labeled, total=total)
            else:
                binding = self.db.get_dataset_import(project_name, dataset_name)
                labeled = binding.get("labeled", labeled)
                total = binding.get("total", total) or total
            self.project_tree.set_row_task(project_name, dataset_name, None)
            proj_cache = self.dataset_cache.setdefault(project_name, {})
            proj_cache[dataset_name] = self._build_dataset_index(result)
            self.project_tree.set_row_loaded(project_name, dataset_name, True)
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
                QC.translate("DatasetViewMixin", "{}: {}个").format(k, v) for k, v in
                sorted(label_counts.items(), key=lambda kv: label_sort_key(kv[0])))
            self._log(QC.translate("DatasetViewMixin", "数据集导入完成: {}/{} | 图像 {} 张, 已标注 {} 张"
                      " | 标签({}类): {}").format(
                project_name, dataset_name, total, labeled,
                len(label_counts), counts_str or QC.translate("DatasetViewMixin", "(无)")))
            self._refresh_dataset_labels(project_name, dataset_name, rescan=False)
            if self._current_dataset == (project_name, dataset_name):
                self._refresh_label_filter(project_name, dataset_name)
            if getattr(self, "_current_dataset", None) == (project_name, dataset_name):
                self.show_dataset_images(project_name, dataset_name)
            # ImportTask 完成后刷新树行 chip 颜色/文本(do_import 预写阶段颜色陈旧, 此时才准确)
            self._refresh_dataset_row_progress(project_name, dataset_name)
            if self._loading_tasks.get(key) is task:
                del self._loading_tasks[key]

        task.progress_updated.connect(on_progress)
        task.finished_signal.connect(on_finished)
        task.finished_signal.connect(task.deleteLater)
        task.start()

    def _on_sidebar_dataset_clicked(self, project, dataset):
        """
        点击数据集行: 仅记录选中; 已缓存的数据集切换显示, 未缓存不触发加载.
        不强制覆盖筛选 - 由 _refresh_label_filter 按新数据集的实际 labels
        决定保留已勾项还是回退到"所有图像".
        """
        self._current_dataset = (project, dataset)
        if self.dataset_cache.get(project, {}).get(dataset):
            self._refresh_label_filter(project, dataset)
            self.show_dataset_images(project, dataset)
        else:
            self._reset_image_area()

    def _on_sidebar_dataset_double_clicked(self, project, dataset):
        """
        双击数据集行 = 载入: 首次扫描进内存并显示.
        已载入的直接忽略 - 重扫代价高(整目录重新读盘解标签), 不该被误触;
        需要重扫的只有推理回写标签那一条链(_load_dataset_view).
        """
        self._current_dataset = (project, dataset)
        if self.dataset_cache.get(project, {}).get(dataset):
            return
        if (project, dataset) in self._loading_tasks:
            return
        if not self.db.get_dataset_import(project, dataset):
            self._log(QC.translate("DatasetViewMixin", "数据集 {}/{} 未导入, 右键\"导入\"选择图像与标签目录").format(
                project, dataset))
            return
        self.show_dataset_images(project, dataset, update_stats=True)

    def _on_sidebar_project_clicked(self, project):
        self._current_dataset = None
        self._reset_image_area()
