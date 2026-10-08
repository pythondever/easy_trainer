# -*- coding: utf-8 -*-
"""界面设计令牌: 颜色与尺寸的唯一来源.

style.qss 里写 {{token}}, 加载时由 utils.load_style_sheet 替换;
Python 侧手绘控件用 color() / hexof() / alpha() 取同一份取值.
新增样式一律引用这里的名字, 不要再写死十六进制 —— 同一层级的近似色各自写死,
想整体调深一档就得改十几处, 永远改不全.
"""

import re

from PySide6.QtGui import QColor

# ---------------- 颜色 ----------------
# 表面: 由深到浅
PALETTE = {
    "bg_sunken": "#0f1117",        # 凹陷槽: 进度条 / 时间框
    "bg_base": "#15181e",          # 窗口底 / 输入框底 / 列表表格底
    "bg_panel": "#1e212a",         # 面板: 对话框 / 分组框 / 侧栏 / 菜单
    "bg_raised": "#252933",        # 抬升面: 顶栏 / 表头 / 交替行 / 分组块
    "bg_control": "#2b303d",       # 控件面: 按钮 / 项目卡片 / 选中行
    "bg_control_2": "#323846",     # 次级控件面: 弹窗按钮 / 弹窗输入框
    "hover_chip": "#2b2f3b",       # 勾选条目悬停底: 比控件面再暗一档
    "bg_hover": "#3b4252",         # 悬停
    "bg_pressed": "#171921",       # 按下(控件面系, 比常态暗)
    "bg_pressed_2": "#3f4657",     # 按下(次级控件面系, 比常态亮)
    "bg_deep": "#0e1015",          # 标注对话框子主题底色 / 图像画布底色
    "bg_deep_2": "#1e222b",        # 标注子主题内的输入类控件

    # 描边
    "border_subtle": "#383e4c",    # 结构分隔: 面板边框 / 网格线 / 分割条
    "border": "#3f4554",           # 控件描边(按钮与输入框同一支)
    "border_strong": "#4a5164",    # 结构描边: 卡片与面板分隔 / 弹层边框 / 滚动条滑块
    "border_hover": "#5c6480",     # 描边悬停

    # 文字
    "text_strong": "#ffffff",
    "text": "#e8eaf0",             # 正文
    "text_2": "#c3c9d6",           # 次要
    "text_dim": "#9aa2b4",         # 更弱的正文(空数据集行名 / 拒绝图标)
    "text_3": "#949cae",           # 弱化: 说明 / 表头 / 元信息
    "text_faint": "#757d90",       # 极弱: 分组小标题 / 禁用菜单项
    "text_disabled": "#5c6270",    # 置灰控件文字

    # 主色
    "accent": "#4f7dff",
    "accent_hover": "#638cff",
    "accent_pressed": "#3f6ceb",
    "accent_dim": "#304067",       # 选中态底色 / 勾选态底色
    "accent_text": "#8fb0ff",      # 主色底上的浅色文字
    "accent_soft": "#7ba2ff",      # 进度条渐变末端

    # 危险
    "danger_bg": "#3a2329",
    "danger_bg_hover": "#4d2a32",
    "danger_bg_pressed": "#2e1b20",
    "danger_border": "#6e3a42",
    "danger_border_hover": "#a04a55",
    "danger_text": "#ff9aa2",
    "danger_solid": "#d64545",
    "danger_solid_hover": "#e05555",

    # 成功(行内正向操作: 测试 / 导出)
    "ok_bg": "#1d3327",
    "ok_bg_hover": "#25402f",
    "ok_bg_pressed": "#172a20",
    "ok_border": "#37694a",
    "ok_border_hover": "#4f8f64",
    "ok_text": "#8fe1a8",

    # 状态
    "st_ok": "#7be39a",
    "st_warn": "#ffd166",
    "st_err": "#ff6b6b",
    "st_err_soft": "#ff9f6b",
    "st_info": "#33c2da",
    "icon_warning": "#f5b84b",
    "icon_critical": "#f2645a",
}

# ---------------- 控件盒模型 ----------------
# QSS 的尺寸按内容盒算: 总高 = 内容高 + 上下 padding + 上下边框
PAD_BTN = (6, 14)             # 按钮内边距 (上下, 左右)
PAD_FIELD = (6, 10)           # 输入框 / 下拉内边距
H_CTRL = 18                   # 主窗口控件内容高 -> 18 + 12 + 2 = 32
H_CTRL_DIALOG = 22            # 弹窗控件内容高 -> 22 + 12 + 2 = 36

# 弹窗按钮实测高度, 供 Python 侧 setMinimumHeight 用(与 QSS 的 h_ctrl_dialog 同源)
BTN_HEIGHT = H_CTRL_DIALOG + 12 + 2

# ---------------- 字号 ----------------
FONT = {
    "font_xs": 10,        # 行内迷你进度条
    "font_sm": 11,        # 徽标 / 分组小标题
    "font_md": 12,        # 表格 / 说明
    "font_base": 13,      # 正文(全局默认)
    "font_lg": 14,        # 选项卡 / 弹窗标题
    "font_xl": 15,        # 对话框标题 / 分组标题
    "font_2xl": 17,       # 应用标题
    "font_3xl": 22,       # 结果大数字
}

# ---------------- 圆角 ----------------
RADIUS = {
    "r_sm": 4,            # 指示器 / 行内色块
    "r_md": 6,            # 按钮 / 输入框
    "r_lg": 8,            # 分组框 / 表格
    "r_xl": 10,           # 项目卡片 / 参数浮层
    "r_2xl": 12,          # 消息框
}

# ---------------- 界面倍率 ----------------
# 用户可选的字号档位. 默认 1.0 = 原样, 不动它时观感逐像素不变.
# 字号必须和盒模型一起缩: 只放大字号, 按钮仍按旧尺寸描边会立刻显挤.
FONT_SCALE = 1.0


def px(value):
    """Python 侧写死的像素尺寸(字号)走这里, 才能跟界面倍率一起变."""
    return max(1, int(round(value * FONT_SCALE)))


def set_font_scale(scale):
    """换倍率并重算令牌; 之后要重新 load_style_sheet() + setStyleSheet 才生效."""
    global FONT_SCALE
    FONT_SCALE = float(scale) if scale else 1.0
    _rebuild_tokens()


TOKENS = {}


def _rebuild_tokens():
    TOKENS.clear()
    TOKENS.update(PALETTE)
    TOKENS.update({k: "{}px".format(px(v)) for k, v in FONT.items()})
    TOKENS.update({k: "{}px".format(px(v)) for k, v in RADIUS.items()})
    TOKENS.update({
        "h_ctrl": "{}px".format(px(H_CTRL)),
        "h_ctrl_dialog": "{}px".format(px(H_CTRL_DIALOG)),
        "pad_btn": "{}px {}px".format(px(PAD_BTN[0]), px(PAD_BTN[1])),
        "pad_field": "{}px {}px".format(px(PAD_FIELD[0]), px(PAD_FIELD[1])),
        # rgba() 里要的是裸三元组, 不能带 #
        "accent_rgb": "79,125,255",
    })


_rebuild_tokens()

_PLACEHOLDER = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")


def hexof(name):
    return PALETTE[name]


def color(name):
    return QColor(PALETTE[name])


def alpha(name, value):
    c = QColor(PALETTE[name])
    c.setAlpha(value)
    return c


def substitute(text, extra=None):
    """把 {{token}} 换成取值, 返回 (替换后的文本, 未定义的令牌名列表)."""
    table = TOKENS if extra is None else dict(TOKENS, **extra)
    missing = set()

    def _rep(m):
        name = m.group(1)
        if name in table:
            return str(table[name])
        missing.add(name)
        return m.group(0)

    return _PLACEHOLDER.sub(_rep, text), sorted(missing)
