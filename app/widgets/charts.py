# -*- coding: utf-8 -*-
"""
标签分布柱状图的共用渲染实现。
统计界面与测试报告 PDF
"""
import numpy as np
from matplotlib import font_manager, rcParams
from matplotlib.figure import Figure

_FONT_CANDIDATES = (
    "Microsoft YaHei", "SimHei", "SimSun", "PingFang SC",
    "Noto Sans CJK SC", "WenQuanYi Micro Hei", "Source Han Sans SC",
)
_installed = {f.name for f in font_manager.fontManager.ttflist}
for _f in _FONT_CANDIDATES:
    if _f in _installed:
        rcParams["font.sans-serif"] = [_f] + list(rcParams.get("font.sans-serif", []))
        rcParams["axes.unicode_minus"] = False
        break


def _short(text, n):
    text = str(text)
    return text if len(text) <= n else text[:n - 1] + "…"


def render_label_chart(label_counts, label_colors=None, dark=True,
                       figsize=None):
    """返回已画好的 Figure。label_counts: {标签: 数量}。"""
    num_bars = max(1, len(label_counts))
    if figsize is None:
        figsize = (max(4.0, num_bars * 0.3), 6.0)
    if dark:
        fig = Figure(figsize=figsize, dpi=100, facecolor="#1c1e25")
        axes = fig.add_subplot(111, facecolor="#1c1e25")
    else:
        fig = Figure(figsize=figsize, dpi=100, facecolor="white")
        axes = fig.add_subplot(111, facecolor="white")
    if not label_counts:
        axes.text(0.5, 0.5, "暂无标注", ha="center", va="center",
                  color="#8a92a3", transform=axes.transAxes, fontsize=14)
        axes.set_xticks([])
        axes.set_yticks([])
        return fig

    # 按标签数量降序
    items = sorted(label_counts.items(), key=lambda kv: kv[1], reverse=True)
    labels = [str(k) for k, _ in items]
    values = [int(v) for _, v in items]
    colors = [(label_colors or {}).get(name, "#5B8CFF") for name in labels]
    # 柱宽(数据单位)≈ n/15.5:使柱宽像素 = 图宽/20;多标签时收紧防重叠
    bar_width = max(0.05, min(0.15, num_bars / 15.5))
    x_positions = np.arange(num_bars)
    axes.bar(x_positions, values, color=colors, width=bar_width,
             edgecolor="none")
    ymax = max(values) if values else 0
    # 类别多时先缩字号再倾斜不丢标签
    fs = 11 if num_bars <= 6 else (9 if num_bars <= 10 else
                                   (7.5 if num_bars <= 16 else 6.5))
    rot = 0 if num_bars <= 10 else 20
    if dark:
        txt_color = "#e8eaf0"
        tick_color = "#c3c9d6"
        label_color = "#c3c9d6"
        grid_color = "#2a2e38"
        spine_color = "#3a3f4e"
    else:
        txt_color = "#333333"
        tick_color = "#666666"
        label_color = "#555555"
        grid_color = "#e0e0e0"
        spine_color = "#c0c0c0"
    for i, v in enumerate(values):
        axes.text(x_positions[i], v, str(v), ha="center", va="bottom",
                  color=txt_color, fontsize=fs)
    axes.set_xlabel("标签", color=label_color, fontsize=11, labelpad=8)
    axes.set_ylabel("标签数量", color=label_color, fontsize=11, labelpad=8)
    axes.tick_params(axis="x", colors=tick_color, labelsize=fs, rotation=rot)
    axes.tick_params(axis="y", colors=tick_color, labelsize=10)
    axes.set_ylim(0, ymax * 1.12 if ymax else 1)
    for side in ("top", "right"):
        axes.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        axes.spines[side].set_color(spine_color)
    axes.yaxis.grid(True, color=grid_color, linestyle="--", linewidth=0.6,
                    alpha=0.8)
    axes.set_axisbelow(True)
    axes.set_xticks(x_positions)
    axes.set_xticklabels([_short(k, 8) for k in labels])
    axes.set_xlim(-0.5, num_bars - 0.5)
    axes.set_ylim(0, ymax * 1.12 if ymax else 1)
    return fig
