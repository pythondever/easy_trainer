# -*- coding: utf-8 -*-


def fit_dialog_height(dlg):
    """按屏幕可用高度收窗; 内容自身最小高超过可用高时压不动, 那种对话框得先加滚动区."""
    scr = dlg.screen()
    if scr is None:
        return
    floor = dlg.minimumSizeHint().height()
    avail = scr.availableGeometry().height() - 90   # 标题栏 + 留白
    if max(dlg.height(), floor) > avail:
        dlg.resize(dlg.width(), max(floor, avail))
