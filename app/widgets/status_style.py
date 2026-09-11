# -*- coding: utf-8 -*-
"""训练状态的中文名与颜色 —— 全仓唯一来源。

模型管理页用中文状态键、训练队列用英文状态键，之前各维护一份映射，
"失败"一处是 #ff6b6b、另一处是 #ff9aa2，同一个状态在两个页面显示两个
颜色；详情页的"失败原因"又单独硬编码了一次 #ff9aa2。这里把两套键合并
到一张表，取值一律走 status_text / status_color，键中英文都认。
"""

STATUS_TEXT = {
    # 队列状态键（英文，queue_mixin 产出的记录）
    "waiting": "等待中",
    "running": "训练中",
    "done": "已完成",
    "failed": "失败",
    "skipped": "已跳过",
    "stopped": "已停止",
    "interrupted": "已中断",
    # 模型记录状态键（中文，model_dialog._status 归一出）
    "训练中": "训练中",
    "已完成": "已完成",
    "失败": "失败",
    "已停止": "已停止",
    "失败/已停止": "失败/已停止",
    "已跳过": "已跳过",
    "已中断": "已中断",
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
    "失败/已停止": "#ff9f6b",   # 旧记录: 区分不出是停止还是报错
    "已跳过": "#ffd166",
    "已中断": "#ffd166",
}

DEFAULT_COLOR = "#e8eaf0"


def status_text(status):
    """状态键 → 中文文案；未登记的原样返回，宁可显示原始键也不丢信息。"""
    s = str(status or "")
    return STATUS_TEXT.get(s, s)


def status_color(status, default=DEFAULT_COLOR):
    """状态键 → 颜色；中英文键都认。"""
    return STATUS_COLOR.get(str(status or ""), default)
