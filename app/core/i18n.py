# -*- coding: utf-8 -*-
"""界面语言切换.

源语言就是中文(代码里写的就是中文), 所以只有切到非中文时才需要装翻译文件,
切回中文 = 把 translator 卸掉. 翻译文件由 builder/translations.py 生成.
"""
import os

from PySide6.QtCore import QCoreApplication, QTranslator

from app.core.utils import project_root

# (代码, 下拉框里显示的名字). 名字本身不翻译: 各语言用户都看自己母语那一项,
# 认得出该选哪个. 名字用本地写法且尽量短, 下拉框前面还挂着国旗.
LANGUAGES = (
    ("zh_CN", "中文"),
    ("en_US", "English"),
    ("zh_TW", "繁體中文"),
    ("ja_JP", "日本語"),
    ("ko_KR", "한국어"),
    ("de_DE", "Deutsch"),
    ("es_ES", "Español"),
    ("fr_FR", "Français"),
    ("vi_VN", "Tiếng Việt"),
)

# 国旗图标: 自绘 SVG 而非 emoji. Windows 的 Segoe UI Emoji 不含区域指示符,
# 🇺🇸 这种会退化成 "US" 两个字母摆在界面上.
_FLAG = {
    "zh_CN": "cn",
    "en_US": "us",
    "zh_TW": "cn",      # 繁体同样挂中国国旗
    "ja_JP": "jp",
    "ko_KR": "kr",
    "de_DE": "de",
    "es_ES": "es",
    "fr_FR": "fr",
    "vi_VN": "vn",
}

DEFAULT = "zh_CN"

# 必须留引用: 只 installTranslator 而不持有, 对象被回收后界面会悄悄变回中文
_translator = None

_current = DEFAULT


def normalize(code):
    """只认 LANGUAGES 里列出的代码, 其余(含空串/None)一律落到默认语言."""
    for known, _ in LANGUAGES:
        if code == known:
            return known
    return DEFAULT


def label(code):
    """语言代码 -> 下拉框显示名."""
    for known, name in LANGUAGES:
        if known == code:
            return name
    return LANGUAGES[0][1]


def index_of(code):
    """语言代码 -> 下拉框下标(未知代码落到默认语言那一项)."""
    code = normalize(code)
    for i, (known, _) in enumerate(LANGUAGES):
        if known == code:
            return i
    return 0


def qm_path(code):
    return os.path.join(project_root(), "i18n", code + ".qm")


def flag_path(code):
    """语言代码 -> 国旗图标绝对路径(文件缺失返回空串, 调用方按无图标处理)."""
    name = _FLAG.get(normalize(code))
    path = (os.path.join(project_root(), "resources", "flags", name + ".svg")
            if name else "")
    return path if path and os.path.exists(path) else ""


def current():
    """当前生效的语言代码."""
    return _current


def apply(app, code):
    """
    装翻译并返回真正生效的语言代码.

    必须在任何界面对象(含 setupUi)之前调用才能对静态文案生效;
    已经在显示的窗口不会自己变, 调用方得自己再走一遍 retranslateUi.
    翻译文件缺失/加载失败时静默退回中文, 不让用户卡在一个空白界面上.
    """
    global _translator, _current
    if _translator is not None:
        app.removeTranslator(_translator)
        _translator = None
    code = normalize(code)
    path = qm_path(code)
    if code != DEFAULT and os.path.exists(path):
        t = QTranslator(app)
        if t.load(path):
            app.installTranslator(t)
            _translator = t
        else:
            code = DEFAULT
    _current = code
    return code


def apply_cli(code):
    """
    子进程里装翻译.

    translator 必须挂在 QCoreApplication 上, 而训练/测试子进程只跑 main(),
    没有界面也就没人建 app, 这里补一个. 装不上就静默回退中文: 日志语言不对
    不该把训练本身搞挂.
    """
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return apply(app, code)
