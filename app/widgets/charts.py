# -*- coding: utf-8 -*-
"""标签分布柱状图的共用渲染实现, 统计界面与测试报告 PDF 都用它."""
import numpy as np
from matplotlib.figure import Figure
from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtCore import QT_TRANSLATE_NOOP

from app.core import theme
from app.core.utils import setup_matplotlib_chinese

# 图表里的文案: 存中文原文, 显示时按界面语言翻. NOOP 只为让 lupdate 抽得到译文
TEXT_NO_LABEL = QT_TRANSLATE_NOOP("Charts", "暂无标注")
TEXT_LABEL = QT_TRANSLATE_NOOP("Charts", "标签")
TEXT_LABEL_COUNT = QT_TRANSLATE_NOOP("Charts", "标签数量")
# 合并尾部长尾类别时的条目名
TEXT_REST = QT_TRANSLATE_NOOP("Charts", "其余 {} 类")
# 渲染 dpi: 2 倍超采样. 统计界面把图缩回 0.5 显示(见 misc_mixin), 
# 滚轮放大 2 倍以内文字都是 1:1 的清晰像素; PDF 侧 savefig 显式
# 传 dpi, 不受这个常量影响
_RENDER_DPI = 200


def _tr(text):
    return QC.translate("Charts", text)


def _short(text, n):
    text = str(text)
    return text if len(text) <= n else text[:n - 1] + "..."


def render_label_chart(label_counts, label_colors=None, dark=True,
                       figsize=None, empty_text=None, top_n=0):
    """返回已画好的 Figure. label_counts: {标签: 数量}.

    横向条形图: 类别名完整显示在左侧纵轴, 数量标在条末. 竖柱在类别多
    且数量差几十倍时小类会贴成一条线, 横向至少保住每类有数字可读.
    top_n > 0 且类别数超过时只画前 top_n 个, 其余合并成一条
    "其余 N 类": 80 类全画会把每类行高压到几个像素, 类别名全叠在一起.
    """
    setup_matplotlib_chinese()
    num_bars = max(1, len(label_counts))
    if figsize is None:
        figsize = (6.0, max(2.6, num_bars * 0.32 + 1.2))
    if dark:
        fig = Figure(figsize=figsize, dpi=_RENDER_DPI,
                     facecolor=theme.hexof("bg_panel"))
        axes = fig.add_subplot(111, facecolor=theme.hexof("bg_panel"))
    else:
        fig = Figure(figsize=figsize, dpi=_RENDER_DPI, facecolor="white")
        axes = fig.add_subplot(111, facecolor="white")
    if not label_counts:
        axes.text(0.5, 0.5, _tr(empty_text or TEXT_NO_LABEL), ha="center",
                  va="center", color=theme.hexof("text_3"), transform=axes.transAxes,
                  fontsize=14)
        axes.set_xticks([])
        axes.set_yticks([])
        return fig

    # 按标签数量降序; barh 的 y 从小到大的向上排, 反转轴让最大值在顶部
    items = sorted(label_counts.items(), key=lambda kv: kv[1], reverse=True)
    rest_n = 0
    rest_sum = 0
    if top_n and len(items) > top_n:
        tail = items[top_n:]
        items = items[:top_n]
        rest_n = len(tail)
        rest_sum = sum(int(v) for _, v in tail)
    # (纵轴显示名, 数值, 颜色, 是否"其余"合并条)
    rows = [(_short(name, 20), int(v),
             (label_colors or {}).get(name, theme.hexof("accent")), False)
            for name, v in items]
    if rest_n:
        rows.append((_tr(TEXT_REST).format(rest_n), rest_sum,
                     theme.hexof("text_3"), True))
    num_bars = len(rows)
    y_positions = np.arange(num_bars)
    axes.barh(y_positions, [r[1] for r in rows], color=[r[2] for r in rows],
              height=0.72, edgecolor="none")
    if dark:
        txt_color = theme.hexof("text")
        tick_color = theme.hexof("text_2")
        label_color = theme.hexof("text_2")
        grid_color = theme.hexof("bg_control_2")
        spine_color = theme.hexof("border_strong")
    else:
        txt_color = "#333333"
        tick_color = "#666666"
        label_color = "#555555"
        grid_color = "#e0e0e0"
        spine_color = "#c0c0c0"
    # 类别多时缩字号: 纵轴标签与条末数值同号, 行内对齐
    fs = 11 if num_bars <= 6 else (9 if num_bars <= 10 else
                                   (7.5 if num_bars <= 16 else 6.5))
    xmax = max(r[1] for r in rows) if rows else 0
    for i, (_, v, _, is_rest) in enumerate(rows):
        axes.text(v + xmax * 0.015, y_positions[i], str(v), ha="left",
                  va="center",
                  color=tick_color if is_rest else txt_color, fontsize=fs)
    axes.set_yticks(y_positions)
    axes.set_yticklabels([r[0] for r in rows], fontsize=fs, color=tick_color)
    axes.invert_yaxis()
    axes.set_xlabel(_tr(TEXT_LABEL_COUNT), color=label_color, fontsize=11,
                    labelpad=8)
    axes.set_ylabel(_tr(TEXT_LABEL), color=label_color, fontsize=11,
                    labelpad=8)
    axes.tick_params(axis="x", colors=tick_color, labelsize=10)
    axes.tick_params(axis="y", length=0)
    axes.set_xlim(0, xmax * 1.15 if xmax else 1)
    for side in ("top", "right"):
        axes.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        axes.spines[side].set_color(spine_color)
    axes.xaxis.grid(True, color=grid_color, linestyle="--", linewidth=0.6,
                    alpha=0.8)
    axes.set_axisbelow(True)
    # 纵轴类别名占左边距, 不设会被 fig 默认边距切掉(PDF 侧会自行覆盖)
    fig.subplots_adjust(left=0.16)
    return fig
