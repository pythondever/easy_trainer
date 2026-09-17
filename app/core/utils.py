# -*- coding: utf-8 -*-
"""通用工具函数: 时长格式化, matplotlib 中文字体, 样式表加载, 跨平台字体."""
import os
import sys

from PySide6.QtCore import QCoreApplication as QC

import matplotlib.pyplot as plt
from matplotlib import font_manager


CJK_FONT_CANDIDATES = (
    "Microsoft YaHei UI", "Microsoft YaHei", "微软雅黑",        # Windows
    "SimHei", "黑体", "SimSun", "宋体", "DengXian", "等线",   # Windows
    "PingFang SC", "Hiragino Sans GB", "STHeiti",           # macOS
    "Noto Sans CJK SC", "Noto Sans SC",                       # Linux
    "WenQuanYi Micro Hei", "WenQuanYi Zen Hei",
    "Source Han Sans CN", "Source Han Sans SC",
    "AR PL UMing CN", "AR PL UKai CN",
    "Meiryo", "Yu Gothic", "MS Gothic",                        # Windows(日文)
    "Malgun Gothic", "Gulim",                                  # Windows(韩文)
)

_CJK_FONT_FILES = (
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
)

# 雅黑没有韩文字形, 日文也只覆盖一部分. 这两个语言得把专用字体排到候选表
# 最前, 否则第一个命中的永远是雅黑. PIL 不做字形回退, 只能靠这个顺序点字体.
_LANG_FIRST = {
    "ko_KR": ("Malgun Gothic", "Gulim", "Batang", "Noto Sans KR",
              "Noto Sans CJK KR"),
    "ja_JP": ("Yu Gothic", "Meiryo", "MS Gothic", "Noto Sans JP",
              "Noto Sans CJK JP"),
}

_font_choice_cache = {}


def _candidates(lang=None):
    """按语言排过序的候选字体名: 该语言专用字体在前, 原表整体兜底在后."""
    return tuple(_LANG_FIRST.get(lang or "", ())) + CJK_FONT_CANDIDATES


def _installed_names():
    try:
        return {f.name for f in font_manager.fontManager.ttflist}
    except Exception:
        return set()


def fmt_duration(secs):
    """可读时长(不足1分钟显示秒;长训练显示天/时/分)."""
    if secs < 60:
        return QC.translate("Utils", "{}秒").format(secs)
    d, rem = divmod(secs, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if d:
        parts.append(QC.translate("Utils", "{}天").format(d))
    if h:
        parts.append(QC.translate("Utils", "{}小时").format(h))
    if m or not parts:
        parts.append(QC.translate("Utils", "{}分").format(m))
    if s and not d and not h:
        parts.append(QC.translate("Utils", "{}秒").format(s))
    # 分隔空格由各语言的片段自带(中日韩不需要, 拉丁语系需要), 收尾统一裁掉
    return "".join(parts).strip()


def ui_font_family():
    """界面推荐中文字体(跨平台): Windows 用雅黑, Linux/macOS 用 Noto Sans CJK.
    返回字体名; 该字体缺失时 Qt 会自动 fallback 到系统默认."""
    if sys.platform == "win32":
        return "Microsoft YaHei"
    if sys.platform == "darwin":
        return "PingFang SC"
    return "Noto Sans CJK SC"


def cjk_font_choice(lang=None):
    """(字体名, 字体文件). lang 传界面语言, 韩/日会优先点对应字体."""
    if lang in _font_choice_cache:
        return _font_choice_cache[lang]
    family, path = "", ""
    installed = _installed_names()
    for name in _candidates(lang):
        if name in installed:
            family = name
            break
    if not family:
        # 候选表没命中时按关键字扫: 各发行版的字体名很杂
        try:
            for f in font_manager.fontManager.ttflist:
                n = f.name.lower()
                if any(kw in n for kw in ("cjk", "chinese", "yahei", "simhei",
                                          "pingfang", "heiti", "songti", "han")):
                    family = f.name
                    break
        except Exception:
            pass
    if family:
        try:
            path = font_manager.findfont(family, fallback_to_default=False)
        except Exception:
            path = ""
    if not path:
        for p in _CJK_FONT_FILES:
            if os.path.exists(p):
                path = p
                break
    _font_choice_cache[lang] = (family or "DejaVu Sans", path)
    return _font_choice_cache[lang]


def setup_matplotlib_chinese(lang=None):
    """
    把中文字体写进全局 rcParams; 幂等(探测结果有缓存, 重复调用无开销).
    之前 charts / metrics_dialog / test_report 各写一份 rcParams, 候选表互不
    相同又都改全局, 后执行的会盖掉前面的, 同一进程里不同图表可能用不同字体
    (一个正常一个方框). 统一走这里.
    """
    # 整份候选表交给 matplotlib 做字形回退(3.6+): 雅黑缺韩文时会自动落到
    # Malgun Gothic, 不用按语言挑单个字体
    installed = _installed_names()
    families = [n for n in _candidates(lang) if n in installed]
    if not families:
        families = [cjk_font_choice(lang)[0]]
    plt.rcParams["font.sans-serif"] = families + ["DejaVu Sans"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False
    return families[0]


def project_root():
    """
    项目根目录: 向上搜索含 style/ 或 resources/ 的目录.
    不依赖固定层级(__file__ 深度), 目录整理后仍能正确定位.
    """
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if (os.path.isdir(os.path.join(d, "style"))
                or os.path.isdir(os.path.join(d, "resources"))):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return d
        d = parent


_TRAIN_TEXT_ENCODINGS = ("utf-8-sig", "utf-8", "gbk")


def decode_text_bytes(raw):
    """
    解码子进程产出的 bytes, 按 utf-8 → gbk 降级.
    训练子进程的文本编码由它自己的环境决定, 不能假设是 utf-8: Windows 上当
    stdout 是管道(不是控制台)时 Python 取 ANSI 码页(中文=gbk), 从 PyCharm
    之类注入过 PYTHONIOENCODING 的环境启动才是 utf-8; 而且 C 层库(torch 等)
    会绕过 Python 编码器直接写 fd, 同一份输出里可能两种编码混排. 固定按
    utf-8 + errors="replace" 解会把中文和表格字符全变成替换符.
    """
    if isinstance(raw, str):
        return raw
    for enc in _TRAIN_TEXT_ENCODINGS:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("gbk", errors="replace")


def read_text_any(path):
    """读子进程产物文本, 按 utf-8 → gbk 降级, 避免编码不符时整条通道静默失效."""
    with open(path, "rb") as f:
        return decode_text_bytes(f.read())


def load_style_sheet():
    """加载 style/style.qss, 并把素材占位符替换为绝对路径(QSS 的 url 相对路径按 cwd 解析, 不可靠)"""
    here = project_root()
    qss_path = os.path.join(here, "style", "style.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            qss = f.read()
    except OSError:
        return ""
    res_dir = os.path.join(here, "resources").replace("\\", "/")
    return qss.replace("{{RES_DIR}}", res_dir)
