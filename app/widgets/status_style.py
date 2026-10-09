# -*- coding: utf-8 -*-
"""训练状态/任务的显示名与颜色 - 全仓唯一来源, 键中英文都认.

表里存的是中文原文: 上屏走 status_text / task_text 按界面语言翻, 取色走
status_color. 调用方拿到的键(如 model_dialog._status 的返回值)始终是中文,
只用来比较, 不直接上屏.
"""

from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtCore import QT_TRANSLATE_NOOP

from app.core import theme

# 表里的中文原文用 QT_TRANSLATE_NOOP 登记(运行时原样返回), 只为让 lupdate 抽得到译文.
# 注意必须写全名: 别名(如 NOOP = QT_TRANSLATE_NOOP)lupdate 认不出来, 条目不进 .ts.
STATUS_TEXT = {
    # 队列状态键
    "waiting": QT_TRANSLATE_NOOP("StatusText", "等待中"),
    "running": QT_TRANSLATE_NOOP("StatusText", "训练中"),
    "done": QT_TRANSLATE_NOOP("StatusText", "已完成"),
    "failed": QT_TRANSLATE_NOOP("StatusText", "失败"),
    "skipped": QT_TRANSLATE_NOOP("StatusText", "已跳过"),
    "stopped": QT_TRANSLATE_NOOP("StatusText", "已停止"),
    "interrupted": QT_TRANSLATE_NOOP("StatusText", "已中断"),
    # 模型记录状态
    "训练中": QT_TRANSLATE_NOOP("StatusText", "训练中"),
    "已完成": QT_TRANSLATE_NOOP("StatusText", "已完成"),
    "失败": QT_TRANSLATE_NOOP("StatusText", "失败"),
    "已停止": QT_TRANSLATE_NOOP("StatusText", "已停止"),
    "失败/已停止": QT_TRANSLATE_NOOP("StatusText", "失败/已停止"),
    "已跳过": QT_TRANSLATE_NOOP("StatusText", "已跳过"),
    "已中断": QT_TRANSLATE_NOOP("StatusText", "已中断"),
}

# 任务类型: 库里的 task 字段(detect/segment/classify)对应界面显示名
TASK_TEXT = {
    "detect": QT_TRANSLATE_NOOP("TaskText", "检测"),
    "segment": QT_TRANSLATE_NOOP("TaskText", "分割"),
    "classify": QT_TRANSLATE_NOOP("TaskText", "分类"),
    "ad": QT_TRANSLATE_NOOP("TaskText", "异常检测"),
    "ocr": QT_TRANSLATE_NOOP("TaskText", "字符检测"),
    "ocr_det": QT_TRANSLATE_NOOP("TaskText", "字符检测"),
    "ocr_rec": QT_TRANSLATE_NOOP("TaskText", "字符识别"),
}

STATUS_COLOR = {
    "waiting": theme.hexof("text_3"),
    "running": theme.hexof("accent"),
    "done": theme.hexof("st_ok"),
    "failed": theme.hexof("st_err"),
    "skipped": theme.hexof("st_warn"),
    "stopped": theme.hexof("st_warn"),
    "interrupted": theme.hexof("st_warn"),
    "训练中": theme.hexof("accent"),
    "已完成": theme.hexof("st_ok"),
    "失败": theme.hexof("st_err"),
    "已停止": theme.hexof("st_warn"),
    "失败/已停止": theme.hexof("st_err_soft"),
    "已跳过": theme.hexof("st_warn"),
    "已中断": theme.hexof("st_warn"),
}

DEFAULT_COLOR = theme.hexof("text")


def status_text(status):
    """状态键对应的当前语言显示文案; 未登记的原样返回, 宁可显示原始键也不丢信息."""
    s = str(status or "")
    return QC.translate("StatusText", STATUS_TEXT.get(s, s))


def task_text(task):
    """任务键对应的当前语言显示文案; 未登记的原样返回."""
    s = str(task or "")
    return QC.translate("TaskText", TASK_TEXT.get(s, s))


def status_color(status, default=DEFAULT_COLOR):
    """状态键对应的颜色; 中英文键都认."""
    return STATUS_COLOR.get(str(status or ""), default)
