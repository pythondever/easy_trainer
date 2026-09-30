# -*- coding: utf-8 -*-
"""标注数据 IO: 图像装载与像素缓存、labelme json 读写、保存删除、模板导入导出."""

import os
import json
from PIL import Image
from PySide6.QtCore import Signal, QTimer, QThread, QMutex, QMutexLocker
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtGui import QColor, QPixmap, QImage, QImageReader
from PySide6.QtWidgets import QFileDialog


from app.annotation.scene import AnnotationScene
from app.annotation.box_item import assign_label_color, label_color
from app.core.label_utils import (OCR_JSON_FLAG, is_text_label,
                                  load_json_shapes, load_yolo_shapes,
                                  normalize_label, same_dir_json,
                                  shapes_to_boxes, shapes_to_labelme_json)
from app.widgets.message_box import MessageBox, ProgressDialog
from app.core.log import write_log

from app.annotation.annotation_canvas import _ClsLabelItem, _clip_templates


def _patch_local_points(t):
    """转为 patch 局部坐标, 原点取顶点外接框左上角(不是 png 的 0,0)."""
    pts = t.get("points") or []
    if not pts:
        return []
    minx = min(float(p[0]) for p in pts)
    miny = min(float(p[1]) for p in pts)
    return [[round(float(x) - minx, 2), round(float(y) - miny, 2)]
            for x, y in pts]


def _json_image_size(png_path):
    """读不到返回 (0, 0)."""
    try:
        with open(os.path.splitext(png_path)[0] + ".json", "r",
                  encoding="utf-8") as f:
            data = json.load(f)
        return int(data.get("imageWidth") or 0), int(data.get("imageHeight") or 0)
    except Exception:
        return 0, 0


def _fit_points_to_patch(pts, png_path, patch):
    """json 与 png 尺寸不一致时按比例换算."""
    jw, jh = _json_image_size(png_path)
    if jw > 0 and jh > 0 and (jw != patch.width() or jh != patch.height()):
        sx, sy = patch.width() / jw, patch.height() / jh
        return [[float(x) * sx, float(y) * sy] for x, y in pts]
    return [[float(x), float(y)] for x, y in pts]


def _load_labelme(json_path):
    """
    读取 labelme json → [{label, x1,y1,x2,y2} 或 {label, points, shape_type}].
    解析统一走 label_utils.load_json_shapes, 这里只转成场景要的字典形态.
    """
    return shapes_to_boxes(load_json_shapes(json_path))


def _load_import_label(image_path, label_path, fmt, label_ids=None):
    """
    从导入绑定的标签目录读取标签框(yolo txt / labelme json).
    label_path 可为 str 或 list(多路径导入: 依次查找同名标签文件).
    与 _load_labelme 返回相同格式的 boxes 列表; 无标签/目录无效返回 [].
    label_ids: {txt 数字 id 字符串: 显示名} 映射(YOLO 专用),
    有映射时优先用显示名, 无映射退回数字本身.
    用于: 导入带标注的图像进入标注界面时显示导入的标注框
    (标注系统的 labelme json 保存在图像同路径, 而导入标签在 label_path 目录).
    """
    label_dirs = [label_path] if isinstance(label_path, (str,)) else list(label_path or [])
    label_dirs = [p for p in label_dirs if p and os.path.isdir(p)]
    if not label_dirs or not fmt:
        return []
    base = os.path.splitext(os.path.basename(image_path))[0]
    ext = ".txt" if fmt == ".txt" else ".json"
    label_file = ""
    for lp in label_dirs:
        candidate = os.path.join(lp, base + ext)
        if os.path.exists(candidate):
            label_file = candidate
            break
    if not label_file:
        return []
    if fmt == ".txt":
        # 尺寸读不到就给 0, load_yolo_shapes 会直接返回空(归一化坐标还原不了)
        iw = ih = 0
        try:
            with Image.open(image_path) as im:
                iw, ih = im.size
        except Exception:
            pass
        return shapes_to_boxes(load_yolo_shapes(label_file, iw, ih, label_ids))
    return shapes_to_boxes(load_json_shapes(label_file))


def save_labelme(image_path, shapes, width=None, height=None,
                 version="5.0.1", ocr=False):
    """
    保存 labelme json 到图像同路径(*.json).
    width/height 可传入已解码的宽高, 避免每次保存重复整图解码(QImage(image_path)).
    ocr=True 时写一个顶层标志位, 见 label_utils.OCR_JSON_FLAG.
    """
    if width is not None and height is not None:
        w, h = int(width), int(height)
    else:
        try:
            img = QImage(image_path)
            w, h = img.width(), img.height()
        except Exception:
            w = h = 0
    base, _ = os.path.splitext(image_path)
    json_path = base + ".json"
    payload = {
        "version": version,
        "flags": {},
        "shapes": shapes,
        "imagePath": os.path.basename(image_path),
        "imageData": None,
        "imageHeight": h,
        "imageWidth": w,
    }
    if ocr:
        payload[OCR_JSON_FLAG] = True
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return json_path


class _PrefetchWorker(QThread):
    """
    后台解码图像到 QImage(主线程再转 QPixmap 入缓存), 避免 D 切换时同步解码大图卡顿.
    请求队列 + 停止标志; 解码保持全尺寸
    """
    decoded = Signal(str, QImage)   # (image_path, qimg) - 用路径作缓存 key, 避免删除/切页后 index 错位

    def __init__(self, image_list, parent=None):
        super().__init__(parent)
        self.image_list = list(image_list)
        self._mutex = QMutex()
        self._pending = []
        self._stop = False

    def request(self, idx):
        with QMutexLocker(self._mutex):
            if idx not in self._pending and 0 <= idx < len(self.image_list):
                self._pending.append(idx)

    def stop(self):
        with QMutexLocker(self._mutex):
            self._stop = True

    def run(self):
        while True:
            with QMutexLocker(self._mutex):
                if self._stop:
                    return
                idx = self._pending.pop(0) if self._pending else None
            if idx is None:
                QThread.msleep(30)
                continue
            path = self.image_list[idx]
            reader = QImageReader(path)
            reader.setAutoTransform(True)
            qimg = reader.read()
            if qimg is not None and not qimg.isNull():
                self.decoded.emit(path, qimg)


# 文案 context 统一写 AnnotationDialog: self.tr 取的是实例真实类名, 换一个译文就对不上
class AnnotationIOMixin:
    def _on_image_pixels_changed(self):
        """
        图像像素被改写(粘贴/填充/撤销) → 刷新缓存 + 标记落盘.
        QPixmap 是写时复制: 场景里 QPainter 画的是副本, _pix_cache 里那份原地不动,
        不换掉的话 A/D 翻走再翻回来会命中旧图(看起来"图像没改, 只剩多边形").
        """
        if not (0 <= self.index < len(self.image_list)):
            return
        item = getattr(self.scene, "image_item", None)
        if item is None:
            return
        pix = item.pixmap()
        if pix is None or pix.isNull():
            return
        self._put_pix_cache(self.image_list[self.index], pix)
        self._pix_unsaved = True
        self._dirty = True
        self._autosave_timer.start()

    def _on_boxes_changed(self):
        """
        标注内容变化(画/删/改类别/拖动缩放)→ 标记 dirty + 刷新右侧列表.
        load_boxes 加载时也会 emit boxes_changed, 但 _loading=True 期间不标记.
        """
        if not getattr(self, "_loading", False):
            self._dirty = True
            self._autosave_timer.start()
        self._labeled_refresh_timer.start()

    def _load_pixmap(self, image_path):
        """
        全尺寸加载图像(缓存命中直接返回; 未命中 QImageReader 解码后入 LRU).
        缓存 key 用 image_path(不用 self.index) - 删除图像后列表前移, index 会指向别的图,
        若按 index 缓存会把"已删图/错位图"显示出来.
        """
        pix = self._pix_cache.get(image_path)
        if pix is None:
            reader = QImageReader(image_path)
            reader.setAutoTransform(True)
            qimg = reader.read()
            if qimg is None or qimg.isNull():
                return None
            pix = QPixmap.fromImage(qimg)
            self._put_pix_cache(image_path, pix, qimg.format())
            return pix

        self._put_pix_cache(image_path, pix)
        return pix

    def _put_pix_cache(self, image_path, pix, fmt=None):
        """入缓存并刷新访问顺序(dict 末尾 = 最近使用), 超出上限按 LRU 淘汰."""
        self._pix_cache.pop(image_path, None)
        self._pix_cache[image_path] = pix
        if fmt is not None:
            self._pix_fmt_cache[image_path] = fmt
        self._trim_pix_cache()

    def _trim_pix_cache(self):
        """
        LRU 淘汰: 从 dict 首项(最久未用)开始丢弃, 同步清理 format 缓存.
        先按张数, 再按估算字节数; 字节循环保留最后一项, 保证当前图不被挤掉.
        """
        while len(self._pix_cache) > self._pix_cache_max:
            self._drop_oldest_pix()
        while (len(self._pix_cache) > 1
               and self._pix_cache_bytes() > self._pix_cache_bytes_max):
            self._drop_oldest_pix()

    def _drop_oldest_pix(self):
        k = next(iter(self._pix_cache), None)
        if k is None:
            return
        self._pix_cache.pop(k, None)
        self._pix_fmt_cache.pop(k, None)

    def _pix_cache_bytes(self):
        """按 depth 估算位图占用(灰度图用 4 字节/像素会高估, 导致过度淘汰)."""
        return sum(p.width() * p.height() * p.depth() // 8
                   for p in self._pix_cache.values())

    def _on_prefetch_decoded(self, path, qimg):
        """后台解码完成: 转 QPixmap 入缓存(按 image_path 作 key), 同步记录 format."""
        if getattr(self, "_closing", False):
            return
        if qimg.isNull():
            return
        if path in self._pix_cache:
            return
        self._put_pix_cache(path, QPixmap.fromImage(qimg), qimg.format())

    def _load_current(self):
        if not (0 <= self.index < len(self.image_list)):
            return
        self._apply_draw_mode_cursor()
        image_path = self.image_list[self.index]
        pix = self._load_pixmap(image_path)
        if pix is None or pix.isNull():
            return
        self.scene.set_image(pix)
        # 预解码相邻图(后台线程), 连续 A/D 翻页时命中缓存不卡
        for nxt in (self.index + 1, self.index - 1):
            if (0 <= nxt < len(self.image_list)
                    and self.image_list[nxt] not in self._pix_cache):
                self._prefetch_worker.request(nxt)
        if self.cls_mode:
            # 图像分类: 只读看图,无框可标注;类别 = 父文件夹名
            boxes = []
            cls = os.path.basename(os.path.dirname(image_path))
            color = self.label_colors.get(cls)
            if color is None:
                color = label_color(cls).name()
            short = min(pix.width(), pix.height())
            font_size = max(4, min(48, int(short / 4)))
            max_by_width = max(4, int(pix.width() * 0.95
                                     / max(len(str(cls)), 1) / 1.4))
            font_size = min(font_size, max_by_width)
            item = _ClsLabelItem(str(cls), str(color), font_size=font_size)
            self.scene.addItem(item)
            r = item.boundingRect()
            item.setPos(pix.width() / 2 - r.width() / 2,
                        pix.height() / 2 - r.height() / 2)
            item.setZValue(10)
        else:
            json_path = same_dir_json(image_path)
            if json_path:
                boxes = _load_labelme(json_path)
            else:
                boxes = _load_import_label(image_path, self.label_path,
                                           self.label_fmt, self.label_ids)
        self._loading = True
        try:
            self.scene.load_boxes(boxes)
        finally:
            self._loading = False
        # A/D 切图保持"显示标注"开关状态(关闭时隐藏标注轮廓)
        show = getattr(self.ui, "switchButton", None) is not None and self.ui.switchButton.isChecked()
        self.scene.set_annotations_visible(show)
        self._ensure_label_colors(boxes)
        QTimer.singleShot(0, self.view.fit_window)
        channels = {
            QImage.Format_Grayscale8: 1,
            QImage.Format_Grayscale16: 1,
            QImage.Format_RGB888: 3,
            QImage.Format_RGB32: 3,
            QImage.Format_ARGB32: 4,
            QImage.Format_RGBA8888: 4,
        }.get(self._pix_fmt_cache.get(image_path, QImage.Format_RGB32), 3)
        self.ui.image_info_label.setText(
            "{} × {} × {}    ({}/{}){}".format(
                pix.width(), pix.height(), channels,
                self.index + 1, len(self.image_list),
                QC.translate("AnnotationDialog", "    类别: {}").format(cls)
                if self.cls_mode else ""))
        self._refresh_labeled_list()
        self._dirty = False
        # 新载入的图以磁盘内容为准, 清掉上一张遗留的待写标记
        self._pix_unsaved = False

    def _switch(self, offset):
        if not self.image_list:
            return
        self._hide_params_panel()
        self._save_current(commit_pending=True)
        new_index = self.index + offset
        if not (0 <= new_index < len(self.image_list)):
            return
        self.index = new_index
        self._load_current()

    def _delete_current_image(self):
        """
        标注界面单张删除: 弹窗确认 -> 调 _delete_images_core 删文件+更新缓存/db
        -> 自动切到下一张(列表前移即指向原 next; 删最后一张则回退一张; 删光则清空场景)
        """
        if not (0 <= self.index < len(self.image_list)):
            return
        cur_path = self.image_list[self.index]
        # 先保存当前未提交的标注(避免画了框没保存就被删, 导致标注明文丢失)
        self._save_current(commit_pending=True)
        btn_delete = QC.translate("AnnotationDialog", "删除本地文件")
        btn_cancel = QC.translate("AnnotationDialog", "取消")
        clicked = MessageBox.choose(
            self, QC.translate("AnnotationDialog", "删除图像"),
            QC.translate("AnnotationDialog", "是否删除当前图像?\n\n{}").format(
                os.path.basename(cur_path)),
            [(btn_delete, "danger"), (btn_cancel, "normal")],
            informative=QC.translate("AnnotationDialog", "图像与同名标注文件将从磁盘删除, 不可恢复"))
        if clicked is None or clicked == btn_cancel:
            return
        main = getattr(self, "_main", None)
        if main is None or not hasattr(main, "_delete_images_core"):
            MessageBox.warning(self, QC.translate("AnnotationDialog", "删除图像"),
                               QC.translate("AnnotationDialog", "无法访问主窗口, 删除失败"))
            return
        main._delete_images_core(self.project, self.dataset, [cur_path],
                                 log_msg="标注界面删除图像: {} | 项目={}, 数据集={}".format(
                                     os.path.basename(cur_path),
                                     self.project, self.dataset))
        self.image_list.pop(self.index)
        self._pix_cache.pop(cur_path, None)
        self._pix_fmt_cache.pop(cur_path, None)
        if not self.image_list:
            self.index = 0
            self.scene.set_image(QPixmap())
            self._refresh_labeled_list()
            self.ui.image_info_label.setText(QC.translate("AnnotationDialog", "(无图像)"))
            return
        if self.index >= len(self.image_list):
            self.index = len(self.image_list) - 1
        self._dirty = False
        self._load_current()

    def _ensure_label_colors(self, boxes):
        """
        确保 boxes 中所有标签都在 db / label_colors 中.
        缺失的标签(如手动创建 labelme json 里的新标签)用确定性哈希色
        label_color() 入库, 保证: 同一标签在 A/D 翻页时颜色一致,
        且首页标签下拉框/下次启动都能看到
        """
        missing = {}
        used = set(self.label_colors.values())
        names = {normalize_label(b.get("label")) for b in boxes}
        text_names = {n for n in names if is_text_label(n)}
        if text_names:
            # 图里出现过文本框就把数据集标成 OCR: 首页筛选与训练集过滤都认这个标记
            self.db.set_dataset_type(self.project, self.dataset, "ocr")
        # OCR 保留标签, 混进标签表会让首页下拉和训练类别多出一类
        for lbl in sorted(names - text_names):
            if lbl and lbl not in self.label_colors:
                color = assign_label_color(lbl, used)
                missing[lbl] = color
                used.add(color)
        if not missing:
            return
        merged = dict(self.db.get_dataset_labels(self.project, self.dataset))
        merged.update(missing)
        self.db.save_dataset_labels(self.project, self.dataset, merged)
        for lbl, color in missing.items():
            self.label_colors[lbl] = color
            self.scene.label_colors[lbl] = QColor(color)
        self._refresh_labels()

    def _clip_export(self):
        """导出到目录: 一张一个 png(带 alpha) + 同名 labelme json 记多边形顶点."""
        if not _clip_templates:
            MessageBox.warning(self, QC.translate("AnnotationDialog", "导出剪切板"),
                               QC.translate("AnnotationDialog", "剪切板是空的, 没有可导出的模板"))
            return
        folder = QFileDialog.getExistingDirectory(
            self, QC.translate("AnnotationDialog", "选择导出目录"))
        if not folder:
            return
        n = 0
        try:
            for i, t in enumerate(_clip_templates):
                patch = t.get("patch")
                if patch is None or patch.isNull():
                    continue
                path = os.path.join(folder, "stamp_{:02d}.png".format(i + 1))
                if not patch.save(path, "PNG"):
                    continue
                # 顶点跟着存进同名 json: 只存 png 的话导回来就只剩一个外接矩形
                local = _patch_local_points(t)
                if len(local) >= 3:
                    data = shapes_to_labelme_json(
                        [(t.get("label") or "object", local)],
                        path, patch.width(), patch.height())
                    with open(os.path.splitext(path)[0] + ".json", "w",
                              encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                n += 1
        except Exception as e:
            write_log("导出剪切板失败: {}".format(e))
            MessageBox.warning(
                self, QC.translate("AnnotationDialog", "导出剪切板"),
                QC.translate("AnnotationDialog",
                             "导出中断: {}\n(已写出 {} 个)").format(e, n))
            return
        MessageBox.information(
            self, QC.translate("AnnotationDialog", "导出剪切板"),
            QC.translate("AnnotationDialog",
                         "已导出 {} 个模板(png + 同名 json)到:\n{}").format(n, folder))

    def _clip_import(self):
        """从目录读回 png: 有同名 json 就按顶点重裁 alpha, 没有才回落成矩形."""
        folder = QFileDialog.getExistingDirectory(
            self, QC.translate("AnnotationDialog", "选择导入目录"))
        if not folder:
            return
        try:
            names = sorted(f for f in os.listdir(folder)
                           if f.lower().endswith(".png"))
        except OSError as e:
            MessageBox.warning(self, QC.translate("AnnotationDialog", "导入剪切板"),
                               QC.translate("AnnotationDialog", "读取目录失败: {}").format(e))
            return
        if not names:
            MessageBox.warning(self, QC.translate("AnnotationDialog", "导入剪切板"),
                               QC.translate("AnnotationDialog", "这个目录里没有 png 文件"))
            return
        new_items, rect_n, bad = [], 0, []
        for name in names:
            path = os.path.join(folder, name)
            img = QImage(path)
            if img.isNull():
                bad.append(name)
                continue
            patch = img.convertToFormat(QImage.Format_ARGB32_Premultiplied)
            label, pts = "", None
            shapes = load_json_shapes(os.path.splitext(path)[0] + ".json")
            if shapes:
                label, pts, _text = shapes[0]
                pts = _fit_points_to_patch(pts, path, patch)
                # 外部 png 可能是压平过的白底, 按多边形重裁一遍才只贴出形状那块
                AnnotationScene.mask_polygon(patch, pts)
            if not pts:
                pts = [[0.0, 0.0], [float(patch.width()), 0.0],
                       [float(patch.width()), float(patch.height())],
                       [0.0, float(patch.height())]]
                rect_n += 1
            new_items.append({"points": pts, "patch": patch,
                              "w": patch.width(), "h": patch.height(),
                              "label": label or self.scene.current_label})
        if new_items:
            _clip_templates[:0] = new_items
            self._rebuild_clipboard(select=0)
        msg = QC.translate("AnnotationDialog", "已导入 {} 个模板到剪切板").format(len(new_items))
        if rect_n:
            msg += QC.translate("AnnotationDialog", "\n其中 {} 个没有同名 json, 按矩形导入").format(rect_n)
        if bad:
            msg += QC.translate("AnnotationDialog", "\n{} 个文件读不出来, 已跳过").format(len(bad))
        MessageBox.information(self, QC.translate("AnnotationDialog", "导入剪切板"), msg)

    def _dataset_image_paths(self):
        """全数据集图像路径: 优先主窗口索引(不受当前筛选视图影响), 退回当前列表."""
        cache = getattr(self._main, "dataset_cache", None) if self._main else None
        recs = {}
        if cache:
            recs = cache.get(self.project, {}).get(self.dataset, {}) or {}
        paths = [r.get("image_path", "") for r in (recs.get("all") or [])
                 if r.get("image_path")]
        return paths or list(self.image_list)

    def _count_label_in_jsons(self, needle):
        """无索引时退回统计: 扫图像同路径 json 计数该标签的 shapes."""
        paths = self._dataset_image_paths()
        progress = None
        if len(paths) > 50:
            progress = ProgressDialog(
                QC.translate("AnnotationDialog", "删除标签"),
                QC.translate("AnnotationDialog", "正在统计标注文件..."), self,
                maximum=len(paths), cancellable=False)
        try:
            total = 0
            for i, img_path in enumerate(paths):
                if progress is not None:
                    progress.set_progress(i)
                jp = same_dir_json(img_path)
                if not jp:
                    continue
                try:
                    with open(jp, "r", encoding="utf-8") as f:
                        text = f.read()
                    if needle not in text:
                        continue
                    data = json.loads(text)
                    total += sum(1 for s in data.get("shapes", [])
                                 if normalize_label(s.get("label")) == needle)
                except Exception:
                    continue
            return total
        finally:
            if progress is not None:
                progress.close()

    def _save_current(self, commit_pending=False):
        """
        仅在用户改动过标注(_dirty)时保存; 未改动不写文件.
        保存内容包括: 画/删/改标签/拖动缩放等触发的 boxes_changed;
        格式刷粘贴修改过图像像素时, 一并把图像写盘.

        commit_pending 只在用户显式要求保存时给(Ctrl+S / 切图 / 关闭 / 删图):
        浮动粘贴挨到这一刻才写进图像像素. 自动保存(150ms 定时器)不带它 ——
        否则刚粘上去就被烧进图里, 根本没机会拖到位.
        """
        if commit_pending:
            # 亮度只在用户显式保存时落地: 让自动保存(150ms)也带上的话, 拖一下就写一次盘
            self._commit_brightness()
            if self._bright_unsaved:
                self._bright_unsaved = False
                self._pix_unsaved = True
                self._dirty = True
            self.scene.commit_pastes()
        elif self.scene.has_pending_pastes():
            # 还有浮层没落地就写盘的话, json 里会有标注、图像里却没有对应图案
            return
        if not self._dirty:
            return
        if not (0 <= self.index < len(self.image_list)):
            return
        image_path = self.image_list[self.index]
        # 缓存里那份是改写前的拷贝, 必须换成刚写盘的内容, 否则翻回来看到旧图
        if self._pix_unsaved:
            item = getattr(self.scene, "image_item", None)
            item_pix = item.pixmap() if item is not None else None
            if item_pix is not None and not item_pix.isNull():
                if item_pix.save(image_path):
                    self._pix_unsaved = False
                else:
                    # 写失败保留标记, 下次再试, 避免静默丢改动
                    write_log("图像写盘失败(像素改动未保存): {}".format(image_path))
        base, _ = os.path.splitext(image_path)
        json_path = base + ".json"
        shapes = []
        for box in self.scene.boxes():
            if box.get("shape_type") == "polygon":
                shape = {
                    "label": box["label"], "points": box["points"],
                    "group_id": None, "shape_type": "polygon", "flags": {},
                }
            else:
                x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
                shape = {
                    "label": box["label"],
                    "points": [[x1, y1], [x2, y2]],
                    "group_id": None, "shape_type": "rectangle", "flags": {},
                }
            # 文字只在有内容时写, 普通检测/分割的 json 不因此多一个空字段
            if box.get("text"):
                shape["text"] = box["text"]
            shapes.append(shape)
        cur_pix = self.scene.image_item.pixmap()
        img_w = cur_pix.width() if cur_pix is not None else None
        img_h = cur_pix.height() if cur_pix is not None else None
        is_ocr = any(is_text_label(s.get("label")) for s in shapes)
        if shapes:
            save_labelme(image_path, shapes, width=img_w, height=img_h,
                         ocr=is_ocr)
        else:
            save_labelme(image_path, [], width=img_w, height=img_h,
                         ocr=is_ocr)
        self._modified_paths.add(image_path)
        self._dirty = False
