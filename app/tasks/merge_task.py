# -*- coding: utf-8 -*-
"""后台改写标注文件的线程: 合并/删除类别(txt) / 重命名/删除标签(json)."""
import json
import os

from PySide6.QtCore import QThread, Signal

from app.core.label_utils import normalize_label


class MergeLabelsTask(QThread):
    """
    后台合并/删除标注类别:
    合并: 把标签目录所有 txt 行首 ∈ old_ids 的行改成 new_id.
    删除(remove=True): 整行删除行首 ∈ old_ids 的行.
    使训练也按合并/删除后的类别进行.
    """

    progress_updated = Signal(int)
    finished_signal = Signal(int)      # 实际修改的文件数

    def __init__(self, label_paths, old_ids, new_id, parent=None, remove=False):
        super().__init__(parent)
        self.label_paths = [p for p in (label_paths or []) if p]
        self.old_ids = set(old_ids or [])
        self.new_id = str(new_id)
        self.remove = remove
        self._cancel = False

    def cancel(self):
        """请求停止: 置取消标志, run 循环内检查后退出."""
        self._cancel = True

    def run(self):
        changed_files = 0
        files = []
        for lp in self.label_paths:
            if not lp or not os.path.isdir(lp):
                continue
            for fn in sorted(os.listdir(lp)):
                if fn.lower().endswith(".txt"):
                    files.append(os.path.join(lp, fn))
        total = max(1, len(files))
        for i, path in enumerate(files):
            if self._cancel:
                break
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                out = []
                changed = False
                for line in lines:
                    parts = line.split()
                    if parts and parts[0] in self.old_ids:
                        if self.remove:
                            changed = True
                            continue          # 整行删除
                        parts[0] = self.new_id
                        out.append(" ".join(parts))
                        changed = True
                    else:
                        out.append(line)
                if changed:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write("\n".join(out) + "\n")
                    changed_files += 1
            except Exception:
                continue
            self.progress_updated.emit(int((i + 1) * 100 / total))
        self.finished_signal.emit(changed_files)


class LabelJsonTask(QThread):
    """
    后台改写 labelme json 的 shape 标签:
    old_name 非空按重命名改(new_name), 否则把 names 里的标签整条删掉.
    先拿原文做子串预筛, 不含目标标签的图不付 json 解析的代价.
    """

    progress_updated = Signal(int)
    finished_signal = Signal(int)      # 实际改写的文件数

    def __init__(self, image_paths, parent=None, old_name=None, new_name=None,
                 names=None):
        super().__init__(parent)
        self.image_paths = [p for p in (image_paths or []) if p]
        self.old_name = old_name or ""
        self.new_name = new_name or ""
        self.names = {n for n in (names or []) if n}
        self._cancel = False

    def cancel(self):
        """请求停止: 置取消标志, run 循环内检查后退出."""
        self._cancel = True

    def _rewrite_one(self, img_path, probes):
        """改写单张图对应的 json, 返回是否真的写盘."""
        json_path = os.path.splitext(img_path)[0] + ".json"
        if not os.path.exists(json_path):
            return False
        with open(json_path, "r", encoding="utf-8") as f:
            text = f.read()
        if not any(p in text for p in probes):
            return False
        data = json.loads(text)
        shapes = data.get("shapes", [])
        if self.old_name:
            hit = False
            for shape in shapes:
                if normalize_label(shape.get("label")) == self.old_name:
                    shape["label"] = self.new_name
                    hit = True
        else:
            kept = [s for s in shapes
                    if normalize_label(s.get("label")) not in self.names]
            data["shapes"] = kept
            hit = len(kept) != len(shapes)
        if not hit:
            return False
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True

    def run(self):
        changed_files = 0
        probes = [self.old_name] if self.old_name else sorted(self.names)
        total = max(1, len(self.image_paths))
        for i, img_path in enumerate(self.image_paths):
            if self._cancel:
                break
            try:
                if self._rewrite_one(img_path, probes):
                    changed_files += 1
            except Exception:
                pass
            self.progress_updated.emit(int((i + 1) * 100 / total))
        self.finished_signal.emit(changed_files)
