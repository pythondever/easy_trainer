# -*- coding: utf-8 -*-
import sys
import os
import json
import shutil
CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append('../ui')
from PySide6.QtGui import QFontMetrics
from ui.import_data import Ui_ImportData
from ui.export_data import Ui_Dialog as ExportDataUI
from app.label_utils import (label_sort_key,
                             load_json_boxes, boxes_to_yolo_text,
                             load_yolo_boxes, boxes_to_labelme_json)
from app.message_box import MessageBox, ProgressDialog
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QDialog, QFileDialog, QButtonGroup

try:
    from shiboken6 import isValid as _is_valid
except ImportError:
    _is_valid = lambda obj: obj is not None

try:
    import PIL.Image as PILImage
except ImportError:
    PILImage = None


class ImportExportMixin(object):
    @staticmethod
    def _scan_import_info(image_path, label_path="", fmt=""):
        """
        扫描导入信息：图像总数 + 已标注数。
        - total = 图像目录下图像数（jpg/jpeg/png/bmp/webp，含子目录）
        - labeled = label_path 里有同名标签文件（按 fmt 后缀）的图像数
        - 无 label_path 或目录不存在时 labeled=0
        返回 (total, labeled)；目录不存在返回 None。
        """
        if not image_path or not os.path.isdir(image_path):
            return None
        IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        total = 0
        names = set()
        for root, _, files in os.walk(image_path):
            for fn in files:
                if fn.lower().endswith(IMAGE_EXTS):
                    total += 1
                    names.add(os.path.splitext(fn)[0])
        labeled = 0
        if label_path and os.path.isdir(label_path) and fmt:
            ext = ".txt" if fmt == ".txt" else ".json"
            try:
                label_names = {os.path.splitext(fn)[0]
                               for fn in os.listdir(label_path)
                               if fn.lower().endswith(ext)}
            except OSError:
                label_names = set()
            labeled = len(names & label_names)
        return total, labeled

    @staticmethod
    def _count_labeled_in_dir(image_path, label_path, ext):
        """
        统计图像目录与标签目录同名的标签文件数(ext: '.txt' / '.json')。
        用于格式选错时的探测: 当前格式匹配 0 张, 检查另一种格式是否
        存在同名标签文件,给用户切换格式的提示.
        """
        try:
            label_names = {os.path.splitext(fn)[0]
                           for fn in os.listdir(label_path)
                           if fn.lower().endswith(ext)}
        except OSError:
            return 0
        if not label_names:
            return 0
        IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        image_names = set()
        for root, _, files in os.walk(image_path):
            for fn in files:
                if fn.lower().endswith(IMAGE_EXTS):
                    image_names.add(os.path.splitext(fn)[0])
        return len(image_names & label_names)

    def _import_dataset(self, project_name, dataset_name):
        """
        数据集右键「导入」: 弹导入对话框(图像路径 + 标签路径可选 + 格式)。
        实时显示: 共 N 张图像，已标注 M 张。
        """
        dlg = QDialog(self)
        dlg.setWindowTitle("导入数据 - {} / {}".format(project_name, dataset_name))
        ui = Ui_ImportData()
        ui.setupUi(dlg)
        ui.horizontalLayout_3.setSpacing(16)
        _fm = QFontMetrics(ui.yolo_fmt.font())
        for rb in (ui.yolo_fmt, ui.labelme_fmt):
            rb.setMinimumWidth(_fm.horizontalAdvance(rb.text()) + 28)  # indicator+spacing
        ui.tips_lbl.setText("请选择图像文件夹")
        # progress_bar 已从 .ui 移除(导入进度走首页进度条)
        ui.done_import_btn.setEnabled(False)
        ui.image_path_txt.setEnabled(False)
        ui.label_path_txt.setEnabled(False)

        def update_tips():
            """实时统计图像目录 + 已标注数 → 更新 tips_lbl 显示。"""
            img_path = ui.image_path_txt.text().strip()
            lbl_path = ui.label_path_txt.text().strip()
            # 分类导入:按子文件夹统计各类别图像数
            if ui.cls_fmt.isChecked():
                if not img_path or not os.path.isdir(img_path):
                    ui.tips_lbl.setText("请选择分类根目录（子文件夹名=类别）")
                    return
                classes = {}
                IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
                for entry in os.listdir(img_path):
                    sub = os.path.join(img_path, entry)
                    if os.path.isdir(sub):
                        n = sum(1 for _, _, fs in os.walk(sub)
                                for fn in fs if fn.lower().endswith(IMAGE_EXTS))
                        if n:
                            classes[entry] = n
                root_n = sum(1 for fn in os.listdir(img_path)
                             if fn.lower().endswith(IMAGE_EXTS))
                if root_n:
                    classes["(根目录)"] = root_n
                if not classes:
                    ui.tips_lbl.setText("所选文件夹下无分类子文件夹或图像")
                else:
                    desc = ", ".join("{}: {}张".format(k, v)
                                     for k, v in sorted(classes.items()))
                    ui.tips_lbl.setText("检测到 {} 类：{}".format(
                        len(classes), desc))
                return
            fmt = ".txt" if ui.yolo_fmt.isChecked() else ".json"
            if not img_path or not os.path.isdir(img_path):
                ui.tips_lbl.setText("请选择图像文件夹")
                return
            total, labeled = self._scan_import_info(img_path, lbl_path, fmt)
            if total == 0:
                ui.tips_lbl.setText("所选文件夹无图像")
            elif labeled > 0:
                ui.tips_lbl.setText("共 {} 张图像，已标注 {} 张".format(total, labeled))
            else:
                alt_tip = ""
                if lbl_path and os.path.isdir(lbl_path):
                    alt_ext = ".txt" if fmt == ".json" else ".json"
                    alt_fmt_name = "Yolo txt" if alt_ext == ".txt" else "Labelme json"
                    try:
                        alt_names = {os.path.splitext(fn)[0]
                                     for fn in os.listdir(lbl_path)
                                     if fn.lower().endswith(alt_ext)}
                    except OSError:
                        alt_names = set()
                    if alt_names:
                        alt_labeled = self._count_labeled_in_dir(
                            img_path, lbl_path, alt_ext)
                        if alt_labeled > 0:
                            alt_tip = "（检测到 {} 张 {} 标签，请切换上方格式为「{}」）".format(
                                alt_labeled, alt_ext, alt_fmt_name)
                if alt_tip:
                    ui.tips_lbl.setText("共 {} 张图像，已标注 0 张 {}".format(total, alt_tip))
                else:
                    ui.tips_lbl.setText("共 {} 张图像（标签目录无匹配文件）".format(total))

        def choose_folder(operator_name):
            folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
            if not folder:
                return
            if operator_name == "图像":
                ui.image_path_txt.setEnabled(True)
                ui.image_path_txt.setText(folder)
            else:
                ui.label_path_txt.setEnabled(True)
                ui.label_path_txt.setText(folder)
            ui.done_import_btn.setEnabled(bool(ui.image_path_txt.text().strip()))
            update_tips()

        ui.choose_image_dir_btn.clicked.connect(lambda: choose_folder("图像"))
        ui.choose_label_dir_btn.clicked.connect(lambda: choose_folder("标签"))
        for btn_name in ("choose_image_dir_btn", "choose_label_dir_btn"):
            btn = getattr(ui, btn_name, None)
            if btn is not None:
                btn.setFixedHeight(40)
                btn.setStyleSheet(
                    "QPushButton{padding:0px;border:1px solid #353a48;border-radius:6px;}")
                btn.setIconSize(QSize(28, 28))
        ui.yolo_fmt.toggled.connect(update_tips)
        ui.labelme_fmt.toggled.connect(update_tips)

        def set_cls_mode(on):
            """
            切换「按子文件夹分类导入」:分类模式只需根目录,标签路径不可用。
            """
            ui.label_path_txt.setEnabled(not on)
            ui.choose_label_dir_btn.setEnabled(not on)
            ui.image_path_txt.setPlaceholderText(
                "分类根目录（子文件夹名=类别）" if on else "图像路径")
            if on:
                ui.label_path_txt.clear()
            ui.done_import_btn.setEnabled(bool(ui.image_path_txt.text().strip()))
            update_tips()

        ui.cls_fmt.toggled.connect(set_cls_mode)
        fmt_group = QButtonGroup(dlg)
        fmt_group.setExclusive(True)
        fmt_group.addButton(ui.yolo_fmt)
        fmt_group.addButton(ui.labelme_fmt)
        fmt_group.addButton(ui.cls_fmt)
        ui.cls_fmt.setAutoExclusive(False)

        def do_import():
            IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
            cls_mode = ui.cls_fmt.isChecked()
            image_path = ui.image_path_txt.text().strip()
            label_path = "" if cls_mode else ui.label_path_txt.text().strip()
            fmt = "cls" if cls_mode else (
                ".txt" if ui.yolo_fmt.isChecked() else ".json")
            if not image_path or not os.path.isdir(image_path):
                MessageBox.warning(dlg, "导入数据", "请先选择有效的图像文件夹")
                return
            if label_path and not os.path.isdir(label_path):
                MessageBox.warning(dlg, "导入数据", "标签路径无效")
                return
            dlg.accept()
            if cls_mode:
                _total = 0
                for _r, _, _fs in os.walk(image_path):
                    for _fn in _fs:
                        if _fn.lower().endswith(IMAGE_EXTS):
                            _total += 1
                _labeled = _total
            else:
                _scanned = self._scan_import_info(image_path, label_path, fmt)
                _total = _scanned[0] if _scanned else 0
                _labeled = _scanned[1] if _scanned else 0
            self.db.update_dataset_import(project_name, dataset_name,
                                          image_path, label_path, fmt,
                                          labeled=_labeled, total=_total)
            self._refresh_dataset_row_progress(project_name, dataset_name)
            self._start_import_thread(project_name, dataset_name,
                                      image_path, label_path, fmt,
                                      update_stats=True)

        ui.done_import_btn.clicked.connect(do_import)
        dlg.exec()

    def _on_toolbar_import(self):
        """工具栏「导入」按钮: 为当前选中的数据集触发导入流程。"""
        if not self._current_dataset:
            MessageBox.warning(self, "导入", "请先在左侧选中一个数据集")
            return
        project, dataset = self._current_dataset
        self._import_dataset(project, dataset)

    def _on_export_clicked(self):
        """
        工具栏「导出」按钮:弹导出对话框（路径 + 格式）,
        选中项目 -> 导出项目下全部数据集；选中数据集 → 导出该数据集。
        目录结构：数据集 <保存路径>/<数据集名>/images|labels;
        项目 <保存路径>/<项目名>/<数据集名>/images|labels。
        标签按所选格式转换导出(labelme json / yolo txt)。
        """
        item = self.project_tree.currentItem()
        if item is None:
            MessageBox.warning(self, "导出", "请先在左侧选中要导出的项目或数据集")
            return
        kind = item.data(0, Qt.UserRole)
        if not kind:
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("导出")
        ui = ExportDataUI()
        ui.setupUi(dlg)
        ui.export_path_txt.setReadOnly(True)
        ui.exp_labelme_fmt.setChecked(True)  # 默认 labelme 格式
        for btn_name in ("select_path_btn", "do_export_btn"):
            btn = getattr(ui, btn_name, None)
            if btn is not None:
                btn.setFixedHeight(40)
                btn.setFixedWidth(60)
                btn.setStyleSheet(
                    "QPushButton{padding:0px;border:1px solid #353a48;"
                    "border-radius:6px;}")
                if btn_name == "select_path_btn":
                    btn.setIconSize(QSize(28, 28))
        ui.select_path_btn.clicked.connect(
            lambda: self._pick_export_path(dlg, ui))
        ui.do_export_btn.clicked.connect(dlg.accept)
        if dlg.exec() != QDialog.Accepted:
            return
        save_dir = ui.export_path_txt.text().strip()
        if not save_dir:
            MessageBox.warning(self, "导出", "请先选择导出保存位置")
            return
        fmt = "yolo" if ui.exp_yolo_fmt.isChecked() else "labelme"
        try:
            if kind[0] == "project":
                project_name = kind[1]
                root = os.path.join(save_dir, project_name)
                ds_list = [(project_name, d["dataset_name"])
                           for d in self.db.get_datasets(project_name)]
                src = "; ".join(self._export_source(project_name, ds)
                                for _, ds in ds_list)
                self._log("开始导出: 项目={} | 源路径={} | 保存路径={} | 格式={}".format(
                    project_name, src, root, fmt))
                recs_map = {ds: self._collect_export_recs(project_name, ds)
                            for _, ds in ds_list}
                total = sum(len(v) for v in recs_map.values())
                dlg2 = ProgressDialog("导出", "正在导出项目…", self, maximum=max(1, total))
                try:
                    done = 0
                    for proj, ds in ds_list:
                        done += self._export_dataset(
                            proj, ds, root, fmt=fmt, progress=dlg2,
                            base_done=done, total=total)
                finally:
                    dlg2.close()
                MessageBox.information(
                    self, "导出",
                    "项目「{}」导出完成，共复制 {} 张图像\n位置：{}".format(
                        project_name, total, root))
                self._log("导出项目完成: {} | {} 张图像 | 标签({}) | 格式={} | → {}".format(
                    project_name, total,
                    self._export_labels(project_name, ds_list), fmt, root))
            else:
                project_name, dataset_name = kind[1], kind[2]
                src = self._export_source(project_name, dataset_name)
                self._log("开始导出: 数据集={}/{} | 源路径={} | 保存路径={} | 格式={}".format(
                    project_name, dataset_name, src, save_dir, fmt))
                recs = self._collect_export_recs(project_name, dataset_name)
                dlg2 = ProgressDialog("导出", "正在导出数据集…", self,
                                      maximum=max(1, len(recs)))
                try:
                    total = self._export_dataset(
                        project_name, dataset_name, save_dir, fmt=fmt,
                        progress=dlg2, total=len(recs))
                finally:
                    dlg2.close()
                MessageBox.information(
                    self, "导出",
                    "数据集「{}」导出完成，共复制 {} 张图像\n位置：{}".format(
                        dataset_name, total,
                        os.path.join(save_dir, dataset_name)))
                self._log("导出数据集完成: {}/{} | {} 张图像 | 标签({}) | 格式={} | → {}".format(
                    project_name, dataset_name, total,
                    self._export_labels(project_name, [(project_name, dataset_name)]),
                    fmt, os.path.join(save_dir, dataset_name)))
        except Exception as e:
            MessageBox.critical(self, "导出失败", str(e))

    def _pick_export_path(self, dlg, ui):
        path = QFileDialog.getExistingDirectory(dlg, "选择导出保存位置")
        if path:
            ui.export_path_txt.setText(path)

    def _collect_export_recs(self, project_name, dataset_name):
        """返回该数据集待导出的图像记录列表（缓存优先，无缓存 os.walk 扫描）。"""
        index = self.dataset_cache.get(project_name, {}).get(dataset_name)
        if index:
            return list(index.get("all", []))
        recs = []
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        image_paths = binding.get("image_paths") or (
            [binding.get("image_path")] if binding.get("image_path") else [])
        IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        for img_root in image_paths:
            if not img_root or not os.path.isdir(img_root):
                continue
            for root, _, files in os.walk(img_root):
                for fn in files:
                    if fn.lower().endswith(IMAGE_EXTS):
                        recs.append({"image_path": os.path.join(root, fn)})
        return recs

    def _export_source(self, project_name, dataset_name):
        """数据集导入源路径摘要（图像目录 + 标签目录），供导出日志用。"""
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        img = binding.get("image_paths") or (
            [binding.get("image_path")] if binding.get("image_path") else [])
        lbl = binding.get("label_paths") or (
            [binding.get("label_path")] if binding.get("label_path") else [])
        return "{} => 标签:{}".format(";".join(img or ["(无)"]),
                                      ";".join(lbl or ["(无)"]))

    def _export_labels(self, project_name, ds_list):
        """数据集标签列表摘要（label_sort_key 排序），供导出日志用。"""
        all_labels = set()
        for proj, ds in ds_list:
            all_labels.update(self.db.get_dataset_labels(proj, ds))
        return ", ".join(sorted(all_labels, key=label_sort_key)) or "(无标签)"

    def _export_dataset(self, project_name, dataset_name, base_dir,
                        fmt="labelme", progress=None, base_done=0, total=None):
        """
        导出单个数据集到 base_dir/<数据集名>/images|labels。
        图像直接复制:标签按 fmt 转换导出;
        - labelme:同路径 json优先复制,否则从源标签转成 json
        - yolo:从标注 boxes 转成 yolo txt(类别ID 按 db 标签排序映射)
        progress：ProgressDialog（set_progress + is_cancelled）；中断返回已复制数。
        """
        ds_dir = os.path.join(base_dir, dataset_name)
        img_dir = os.path.join(ds_dir, "images")
        lbl_dir = os.path.join(ds_dir, "labels")
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(lbl_dir, exist_ok=True)
        binding = self.db.get_dataset_import(project_name, dataset_name) or {}
        # yolo 类别 ID 映射:db 标签按 label_sort_key 排序后的序号
        labels = self.db.get_dataset_labels(project_name, dataset_name)
        label_to_id = {name: i for i, name in
                       enumerate(sorted(labels, key=label_sort_key))}

        recs = self._collect_export_recs(project_name, dataset_name)
        copied = 0
        for i, rec in enumerate(recs):
            src = rec.get("image_path", "")
            if not src or not os.path.exists(src):
                continue
            if progress is not None:
                if progress.is_cancelled():
                    return copied
                progress.set_progress(
                    base_done + i,
                    "正在导出: {}".format(os.path.basename(src)))
            dst = os.path.join(img_dir, os.path.basename(src))
            if os.path.abspath(src) != os.path.abspath(dst):
                shutil.copy2(src, dst)
            copied += 1
            self._export_label_file(src, fmt, label_to_id, binding, lbl_dir)
        return copied

    def _export_label_file(self, img_src, fmt, label_to_id, binding, lbl_dir):
        """按目标格式把一张图的标注写入 lbl_dir(同名文件)."""
        stem = os.path.splitext(os.path.basename(img_src))[0]
        base_wo_ext, _ = os.path.splitext(img_src)
        # labelme: 同路径 json 标注直接复制(保持标注界面的原始 json)
        if fmt == "labelme":
            same_json = base_wo_ext + ".json"
            if os.path.exists(same_json):
                shutil.copy2(same_json, os.path.join(lbl_dir, stem + ".json"))
                return
        boxes = self._read_export_boxes(img_src, binding)
        if not boxes:
            return
        try:
            with PILImage.open(img_src) as im:
                iw, ih = im.size
        except Exception:
            return
        target = os.path.join(lbl_dir, stem + (".json" if fmt == "labelme" else ".txt"))
        if fmt == "labelme":
            data = boxes_to_labelme_json(boxes, img_src, iw, ih)
            with open(target, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            text = boxes_to_yolo_text(boxes, iw, ih, label_to_id)
            if text:
                with open(target, "w", encoding="utf-8") as f:
                    f.write(text + "\n")

    def _read_export_boxes(self, img_src, binding):
        """
        读取一张图的标注 boxes(像素坐标 + label).
        优先同路径 labelme json(标注产物),否则 label_paths 同名标签.
        """
        base_wo_ext, _ = os.path.splitext(img_src)
        same_json = base_wo_ext + ".json"
        if os.path.exists(same_json):
            return load_json_boxes(same_json)
        label_fmt = binding.get("label_fmt", "")
        if not label_fmt:
            return []
        ext = ".txt" if label_fmt == ".txt" else ".json"
        stem = os.path.splitext(os.path.basename(img_src))[0]
        for lp in (binding.get("label_paths") or
                   ([binding.get("label_path")] if binding.get("label_path") else [])):
            if not lp or not os.path.isdir(lp):
                continue
            cand = os.path.join(lp, stem + ext)
            if not os.path.exists(cand):
                continue
            if ext == ".json":
                return load_json_boxes(cand)
            return load_yolo_boxes(cand, img_src)
        return []
