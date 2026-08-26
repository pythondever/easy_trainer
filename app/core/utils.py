# -*- coding: utf-8 -*-
"""通用工具函数：时长格式化、matplotlib 中文字体、样式表加载。"""
import os

import matplotlib.pyplot as plt
from matplotlib import font_manager


_CJK_FONT_CANDIDATES = [
    "Microsoft YaHei UI", "Microsoft YaHei", "微软雅黑",   # Windows
    "SimHei", "黑体", "SimSun", "宋体",                      # Windows
    "PingFang SC", "Hiragino Sans GB", "STHeiti",            # macOS
    "Noto Sans CJK SC", "Noto Sans SC", "WenQuanYi Micro Hei",  # Linux
    "Source Han Sans CN", "Source Han Sans SC",
    "AR PL UMing CN", "AR PL UKai CN",
]


def fmt_duration(secs):
    """可读时长(不足1分钟显示秒;长训练显示天/时/分)。"""
    if secs < 60:
        return "{}秒".format(secs)
    d, rem = divmod(secs, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if d:
        parts.append("{}天".format(d))
    if h:
        parts.append("{}小时".format(h))
    if m or not parts:
        parts.append("{}分".format(m))
    if s and not d and not h:
        parts.append("{}秒".format(s))
    return "".join(parts)


def setup_matplotlib_chinese():
    try:
        available = {f.name for f in font_manager.fontManager.ttflist}
    except Exception:
        available = set()
    chosen = next((f for f in _CJK_FONT_CANDIDATES if f in available), None)
    if chosen is None:
        for f in font_manager.fontManager.ttflist:
            n = f.name.lower()
            if any(kw in n for kw in ("cjk", "chinese", "yahei", "simhei",
                                       "pingfang", "heiti", "songti", "han")):
                chosen = f.name
                break
    if chosen is None:
        chosen = "DejaVu Sans"
    plt.rcParams["font.sans-serif"] = [chosen, "DejaVu Sans"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False


def project_root():
    """项目根目录: 向上搜索含 style/ 或 resources/ 的目录。
    不依赖固定层级(__file__ 深度), 目录整理后仍能正确定位。"""
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if (os.path.isdir(os.path.join(d, "style"))
                or os.path.isdir(os.path.join(d, "resources"))):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return d
        d = parent


def load_style_sheet():
    """加载 resources/style.qss"""
    here = project_root()
    qss_path = os.path.join(here, "style", "style.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""
