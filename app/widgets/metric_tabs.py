# -*- coding: utf-8 -*-
"""
指标分段按钮: 一排 pill, 当前项高亮; 所选记录都没有的指标置灰不可点.
指标多时整排的最小宽度会把窗口撑到屏幕外, 所以按钮排在内部横向
QScrollArea 里: 控件自身最小宽度小, 滚轮映射为横向滚动, 真的放不下时
滚动条才出现; 行高按需补足, 免得滚动条压住按钮.
"""

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtWidgets import (QButtonGroup, QFrame, QHBoxLayout,
                               QScrollArea, QSizePolicy, QToolButton,
                               QWidget)

_SCROLL_STEP = 48


class MetricTabs(QWidget):
    """指标切换; keys 是全部候选, available 是当前勾选记录真正有的."""

    metricChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("metricTabsBox")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumWidth(240)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setFocusPolicy(Qt.NoFocus)
        self._inner = QWidget()
        self._inner.setObjectName("metricTabsInner")
        self._layout = QHBoxLayout(self._inner)
        self._layout.setContentsMargins(3, 3, 3, 3)
        self._layout.setSpacing(2)
        # 末尾垫一根弹簧: 没有它, 宽度富余时布局会把按钮拉长填满整行
        self._layout.addStretch(1)
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
            # 而 deleteLater 要等事件循环才回收, 切指标时新旧两层文字会叠在同一处
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
            # 插在尾部弹簧之前, 否则新按钮会排到弹簧后面
            self._layout.insertWidget(self._layout.count() - 1, btn)
            self._buttons.append(btn)
            if key == current:
                # 回填当前项不能回调出去: 调用方正处在自己的刷新里
                btn.blockSignals(True)
                btn.setChecked(True)
                btn.blockSignals(False)
        self._current = current
        self._sync_height()

    def current(self):
        for key, btn in zip(self._keys, self._buttons):
            if btn.isChecked():
                return key
        return self._current if self._keys else ""

    def _sync_height(self):
        """行高跟着按钮走; 要出横向滚动条时再补上它那点高度, 免得压住按钮."""
        self._layout.activate()
        bar = self._scroll.horizontalScrollBar()
        reserve = bar.sizeHint().height() if bar.maximum() > 0 else 0
        h = self._inner.sizeHint().height() + reserve
        if h != self._scroll.height():
            self._scroll.setFixedHeight(h)

    def eventFilter(self, obj, event):
        # PySide6 6.9.1 偶尔把 QStandardItem 当 event 投过来, 直接 event.type() 是空指针解引用
        if not isinstance(event, QEvent):
            return False
        if obj is self._scroll.viewport():
            if event.type() == QEvent.Wheel:
                bar = self._scroll.horizontalScrollBar()
                delta = event.angleDelta().y() or event.angleDelta().x()
                if bar.maximum() > 0 and delta:
                    bar.setValue(bar.value() - (_SCROLL_STEP if delta > 0
                                                else -_SCROLL_STEP))
                    return True
            elif event.type() == QEvent.Resize:
                # 滚动条出不出现、多高, 这轮布局算完才知道
                QTimer.singleShot(0, self._sync_height)
        return super().eventFilter(obj, event)

    def _on_clicked(self):
        btn = self.sender()
        for key, b in zip(self._keys, self._buttons):
            if b is btn:
                self._current = key
                self.metricChanged.emit(key)
                return
