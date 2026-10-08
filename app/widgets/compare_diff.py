# -*- coding: utf-8 -*-
"""对比右栏: 最佳记录 / 参数差异(只列取值不同的项) / 结论.

数据由 CompareDialog 整理成 dict 列表喂进来, 这里只管排版."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.core import theme

DIFF_FIELDS = (("任务", "task"), ("模型", "model"), ("数据集", "dataset"),
               ("轮次", "epochs"), ("批次", "batch"), ("学习率", "lr"),
               ("图像尺寸", "img_size"), ("增强", "aug"))

# 没跑完的状态: 不参与最佳判定
_UNFINISHED = ("失败", "失败/已停止", "已停止", "已中断", "已跳过")

_STYLE = """
#diffCard { background-color: {{bg_control}}; border: 1px solid {{border_strong}};
            border-radius: 8px; }
#diffCardTitle { color: {{text_2}}; font-weight: 600; }
#diffCardHint { color: {{text_faint}}; font-weight: 400; }
#diffBestName { color: {{text_strong}}; font-weight: 600; }
#diffBestMeta { color: {{text_3}}; }
#diffKeyValue { color: {{text_2}}; }
#diffKeyTime { color: {{text_faint}}; }
#diffCommon { color: {{text_3}}; }
#diffConcl { color: {{text_2}}; }
"""


def _dot(color):
    return "<span style='color:{}'>●</span>".format(color)


def _esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


class DiffPanel(QWidget):
    """右栏容器: 提供一个 render(items, metric, best_idx) 与一个空态."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(theme.substitute(_STYLE)[0])
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(9)
        self._layout.addStretch(1)

    def _reset(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        self._layout.addStretch(1)

    def show_empty(self, text):
        self._reset()
        card, lay = self._card("")
        tip = QLabel(text)
        tip.setObjectName("diffConcl")
        tip.setAlignment(Qt.AlignCenter)
        tip.setWordWrap(True)
        tip.setMinimumHeight(90)
        lay.addWidget(tip)
        self._insert(card)

    def render(self, items, metric, best_idx):
        self._reset()
        self._add_best(items, metric, best_idx)
        self._add_diff(items)
        self._add_conclusion(items, metric, best_idx)

    def _insert(self, card):
        self._layout.insertWidget(self._layout.count() - 1, card)
        # 不 show 的话布局激活前它是 hidden, heightForWidth 会把它整个忽略,
        # 调用方同步量高度只会量到空布局
        card.show()

    def _card(self, title, hint=""):
        frame = QFrame(self)
        frame.setObjectName("diffCard")
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(12, 10, 12, 11)
        lay.setSpacing(6)
        if title:
            head = QHBoxLayout()
            name = QLabel(title)
            name.setObjectName("diffCardTitle")
            head.addWidget(name)
            if hint:
                tip = QLabel(hint)
                tip.setObjectName("diffCardHint")
                head.addWidget(tip)
            head.addStretch(1)
            lay.addLayout(head)
        return frame, lay

    # ---------- 最佳记录 ----------
    def _add_best(self, items, metric, best_idx):
        if best_idx is None or not (0 <= best_idx < len(items)):
            return
        it = items[best_idx]
        card, lay = self._card(self.tr("最佳记录"),
                               self.tr("按 {}").format(metric))
        name = QLabel("{} {} · {}".format(_dot(it["color"]),
                                          _esc(it["time"]),
                                          _esc(it["task"])))
        name.setObjectName("diffBestName")
        meta = QLabel("{} · {}".format(_esc(it["model"]), _esc(it["dataset"])))
        meta.setObjectName("diffBestMeta")
        meta.setWordWrap(True)
        value = QLabel(_esc(it["best_text"]))
        value.setStyleSheet("color: {}; font-size: 16px; font-weight: 700;"
                            .format(theme.hexof("st_ok")))
        for w in (name, meta, value):
            w.setWordWrap(w is not value)
            lay.addWidget(w)
        self._insert(card)

    # ---------- 参数差异 ----------
    def _add_diff(self, items):
        card, lay = self._card(self.tr("参数差异"), self.tr("仅列取值不同的项"))
        diff, same = [], []
        for name, key in DIFF_FIELDS:
            vals = [str(it.get(key) or "") for it in items]
            if len(set(vals)) > 1:
                diff.append((name, vals))
            elif vals:
                same.append("{} {}".format(name, vals[0]))
        if not diff:
            tip = QLabel(self.tr("所选记录参数完全一致"))
            tip.setObjectName("diffConcl")
            tip.setAlignment(Qt.AlignCenter)
            tip.setMinimumHeight(56)
            lay.addWidget(tip)
        for name, vals in diff:
            lay.addWidget(self._diff_row(name, vals, items))
        if same:
            common = QLabel("&nbsp;&nbsp;".join(
                "<b>{}</b> {}".format(self.tr("共同"), _esc(s)) for s in same))
            common.setObjectName("diffCommon")
            common.setWordWrap(True)
            lay.addWidget(common)
        self._insert(card)

    def _diff_row(self, name, vals, items):
        row = QWidget()
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 2, 0, 4)
        lay.setSpacing(8)
        key = QLabel(name)
        key.setObjectName("diffKeyTime")
        key.setFixedWidth(58)
        key.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        lay.addWidget(key)
        col = QVBoxLayout()
        col.setSpacing(3)
        for it, v in zip(items, vals):
            lab = QLabel("{} {} <span style='color:{}'>{}</span>".format(
                _dot(it["color"]), _esc(v), theme.hexof("text_faint"),
                _esc(it["time"])))
            lab.setObjectName("diffKeyValue")
            lab.setWordWrap(True)
            col.addWidget(lab)
        lay.addLayout(col, 1)
        return row

    # ---------- 结论 ----------
    def _add_conclusion(self, items, metric, best_idx):
        card, lay = self._card(self.tr("结论"))
        for text in self._conclusions(items, metric, best_idx):
            lab = QLabel("<span style='color:{}'>●</span>&nbsp; {}".format(
                theme.hexof("accent_soft"), text))
            lab.setObjectName("diffConcl")
            lab.setWordWrap(True)
            lay.addWidget(lab)
        self._insert(card)

    def _conclusions(self, items, metric, best_idx):
        out = []
        best = items[best_idx] if (best_idx is not None
                                   and 0 <= best_idx < len(items)) else None
        if best is not None:
            out.append("{}： <b>{} {} / {}</b>， {} {}".format(
                self.tr("最佳"), _esc(best["time"]), _esc(best["task"]),
                _esc(best["model"]), _esc(metric), _esc(best["best_text"])))
            others = [it for i, it in enumerate(items) if i != best_idx]
            alone = []
            for name, key in DIFF_FIELDS:
                bv = str(best.get(key) or "")
                if others and all(str(o.get(key) or "") != bv for o in others):
                    alone.append("{} {}".format(name, bv))
            if alone:
                out.append("{}： <b>{}</b>".format(
                    self.tr("它独有的设置"), _esc("、".join(alone[:2]))))
        with_aug = [it for it in items if it.get("aug_codes")]
        if with_aug:
            out.append("{}： <b>{}</b>".format(
                self.tr("启用增强 {}/{} 条").format(len(with_aug), len(items)),
                _esc("、".join("+".join(it["aug_codes"]) for it in with_aug))))
        else:
            out.append(self.tr("所选记录都没有启用数据增强"))
        running = [it for it in items if it.get("status") == "训练中"]
        if running:
            it = running[0]
            out.append("{} {}（{}/{}）， {}".format(
                _esc(it["model"]), self.tr("仍在训练"), it.get("prog") or 0,
                _esc(it.get("epochs") or ""),
                self.tr("曲线未收敛， 对比仅供参考")))
        bad = [it for it in items if it.get("status") in _UNFINISHED]
        if bad:
            out.append("{} {}， {}".format(
                "、".join(_esc(it["time"]) for it in bad),
                self.tr("未跑完"), self.tr("不参与最佳判定")))
        durs = [it["dur"] for it in items if it.get("dur")]
        if len(durs) > 1:
            out.append("{} {} ~ {}".format(self.tr("训练时长"),
                                           min(durs), max(durs)))
        return out
