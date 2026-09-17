# -*- coding: utf-8 -*-
"""训练状态/任务的显示名与颜色 - 全仓唯一来源.

模型管理页用中文状态键, 训练队列用英文状态键, 之前各维护一份映射,
"失败"一处是 #ff6b6b, 另一处是 #ff9aa2, 同一个状态在两个页面显示两个
颜色; 详情页的"失败原因"又单独硬编码了一次 #ff9aa2. 这里把两套键合并
到一张表, 取值一律走 status_text / status_color, 键中英文都认.

表里存的是**中文原文**, 界面语言切英文时靠 QT_TRANSLATE_NOOP 登记的
"StatusText"/"TaskText" 两个 context 翻出来. 调用方拿到的键(如
model_dialog._status 的返回值)始终是中文, 只用来比较, 不直接上屏.
"""

from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtCore import QT_TRANSLATE_NOOP

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

# 任务类型: 库里的 task 字段(detect/segment/classify) → 界面显示名
TASK_TEXT = {
    "detect": QT_TRANSLATE_NOOP("TaskText", "检测"),
    "segment": QT_TRANSLATE_NOOP("TaskText", "分割"),
    "classify": QT_TRANSLATE_NOOP("TaskText", "分类"),
}

STATUS_COLOR = {
    "waiting": "#8b93a5",
    "running": "#4f7dff",
    "done": "#7be39a",
    "failed": "#ff6b6b",
    "skipped": "#ffd166",
    "stopped": "#ffd166",
    "interrupted": "#ffd166",
    "训练中": "#4f7dff",
    "已完成": "#7be39a",
    "失败": "#ff6b6b",
    "已停止": "#ffd166",
    "失败/已停止": "#ff9f6b",
    "已跳过": "#ffd166",
    "已中断": "#ffd166",
}

DEFAULT_COLOR = "#e8eaf0"


def status_text(status):
    """状态键 → 当前语言的显示文案; 未登记的原样返回, 宁可显示原始键也不丢信息."""
    s = str(status or "")
    return QC.translate("StatusText", STATUS_TEXT.get(s, s))


def task_text(task):
    """任务键 → 当前语言的显示文案; 未登记的原样返回."""
    s = str(task or "")
    return QC.translate("TaskText", TASK_TEXT.get(s, s))


def status_color(status, default=DEFAULT_COLOR):
    """状态键 → 颜色; 中英文键都认."""
    return STATUS_COLOR.get(str(status or ""), default)
