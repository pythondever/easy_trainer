# -*- coding: utf-8 -*-
"""指标分段按钮: 一排 pill, 当前项高亮; 所选记录都没有的指标置灰不可点.

指标多时整排的最小宽度会把窗口撑到屏幕外, 所以按钮排在内部横向
QScrollArea 里: 控件自身最小宽度小, 滚轮映射为横向滚动; 滚动条常隐
(AlwaysOff) 避免出现/消失引发的宽度抖动.
"""

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (QButtonGroup, QFrame, QHBoxLayout,
                               QScrollArea, QSizePolicy, QToolButton,
                               QWidget)

from app.core import theme

_STYLE = """
#metricTabsBox { background-color: {{bg_control}};
                 border: 1px solid {{border}}; border-radius: 7px; }
#metricTabsBox QScrollArea, #metricTabsBox QWidget#metricTabsInner {
    background: transparent; border: none; }
#metricTabsBox QToolButton { background: transparent; border: none;
    border-radius: 5px; padding: 5px 12px; color: {{text_3}}; }
#metricTabsBox QToolButton:hover:!disabled { background-color: {{bg_hover}};
    color: {{text}}; }
#metricTabsBox QToolButton:checked { background-color: {{accent}};
    color: {{text_strong}}; }
#metricTabsBox QToolButton:disabled { color: {{text_disabled}}; }
"""

_SCROLL_STEP = 48


class MetricTabs(QWidget):
    """指标切换; keys 是全部候选, available 是当前勾选记录真正有的."""

    metricChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("metricTabsBox")
        self.setStyleSheet(theme.substitute(_STYLE)[0])
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumWidth(240)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setFocusPolicy(Qt.NoFocus)
        self._inner = QWidget()
        self._inner.setObjectName("metricTabsInner")
        self._layout = QHBoxLayout(self._inner)
        self._layout.setContentsMargins(3, 3, 3, 3)
        self._layout.setSpacing(2)
        self._scroll.setWidget(self._inner)
        outer.addWidget(self._scroll)
        self._scroll.viewport().installEventFilter(self)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._buttons = []
        self._keys = []
        self._available = set()
        self._current = ""

    def set_metrics(self, keys, available=(), current=""):
        """重建按钮; current 不在 keys 里就退回第一个可用的."""
        self._keys = list(keys)
        self._available = set(available)
        for btn in self._buttons:
            self._layout.removeWidget(btn)
            # 只 removeWidget 不动父级的话, 旧按钮会带着原 geometry 继续画,
            # 而 deleteLater 要等事件循环才回收 —— 切指标时新旧两层文字会叠在同一处
            btn.setParent(None)
            btn.deleteLater()
        self._buttons = []
        if current not in self._keys:
            current = next((k for k in self._keys if k in self._available),
                           self._keys[0] if self._keys else "")
        for key in self._keys:
            btn = QToolButton(self._inner)
            btn.setText(key)
            btn.setCheckable(True)
            usable = key in self._available
            btn.setEnabled(usable)
            btn.setToolTip("" if usable else
                           self.tr("所选记录都没有 {} 的数据").format(key))
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            btn.clicked.connect(self._on_clicked)
            self._group.addButton(btn)
            self._layout.addWidget(btn)
            self._buttons.append(btn)
            if key == current:
                # 回填当前项不能回调出去: 调用方正处在自己的刷新里
                btn.blockSignals(True)
                btn.setChecked(True)
                btn.blockSignals(False)
        self._current = current
        # 行高跟着按钮走, 滚动区纵向不留空
        self._scroll.setFixedHeight(self._inner.sizeHint().height())

    def current(self):
        for key, btn in zip(self._keys, self._buttons):
            if btn.isChecked():
                return key
        return self._current if self._keys else ""

    def eventFilter(self, obj, event):
        if obj is self._scroll.viewport() and event.type() == QEvent.Wheel:
            bar = self._scroll.horizontalScrollBar()
            delta = event.angleDelta().y() or event.angleDelta().x()
            if bar.maximum() > 0 and delta:
                bar.setValue(bar.value() - (_SCROLL_STEP if delta > 0
                                            else -_SCROLL_STEP))
                return True
        return super().eventFilter(obj, event)

    def _on_clicked(self):
        btn = self.sender()
        for key, b in zip(self._keys, self._buttons):
            if b is btn:
                self._current = key
                self.metricChanged.emit(key)
                return
