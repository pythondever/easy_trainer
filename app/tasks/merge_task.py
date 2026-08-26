# -*- coding: utf-8 -*-
"""后台合并/删除标注类别线程。"""
import os

from PySide6.QtCore import QThread, Signal


class MergeLabelsTask(QThread):
    """
    后台合并/删除标注类别:
    合并: 把标签目录所有 txt 行首 ∈ old_ids 的行改成 new_id。
    删除(remove=True): 整行删除行首 ∈ old_ids 的行。
    使训练也按合并/删除后的类别进行。
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
