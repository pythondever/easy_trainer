"""
下拉弹层与控件贴合边的圆角处理.
Qt 把 QComboBox 的弹层紧贴控件底边显示, 两层各画各的圆角, 接缝处左右各留一个缺口,
看着像两张卡片叠在一起. 弹层显示时给控件打 popupOpen 标记, QSS 据此抹平贴合边的
圆角, 展开时拼成一整块, 收起后仍是完整胶囊.
Qt 只在弹层视图上发 Show/Hide, 视图并不等于弹层窗口, 但沿 parent 链能上溯到控件.
"""

from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QAbstractItemView, QComboBox


class ComboPopupFlattener(QObject):
    """装在 QApplication 上的事件过滤器, 只关心弹层视图的显示与隐藏."""

    def eventFilter(self, obj, event):
        # 基类默认实现就是 return False, 不必再透传; 透传在偶发收到非 QEvent 的实参时
        # (实测撞到过 QStandardItem) 会踩 shiboken 的实参类型校验 TypeError, 而这个
        # 异常发生在 Qt 事件分发里没人接, 直接终止进程
        if not isinstance(event, QEvent):
            return False
        t = event.type()
        if (t == QEvent.Show or t == QEvent.Hide) and isinstance(obj, QAbstractItemView):
            owner = obj.parentWidget()
            while owner is not None and not isinstance(owner, QComboBox):
                owner = owner.parentWidget()
            if owner is not None:
                owner.setProperty("popupOpen", t == QEvent.Show)
                # 动态属性不会自动触发样式重算
                owner.style().unpolish(owner)
                owner.style().polish(owner)
        return False
