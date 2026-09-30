# -*- coding: utf-8 -*-
"""
项目名/数据集名/标签名的合法性校验.
项目名会同时当目录名和导出文件名用("项目_时间戳/项目_字符检测_505_medium.onnx"),
标签名会进 classes.txt / data.yaml 这类按行解析的文本. 非法字符会让落盘报错,
Windows 的保留设备名更隐晦: "CON" / "NUL" 打开不报错却没有文件产生, 上层会把
"没产出"当成功.
"""

from PySide6.QtCore import QCoreApplication as QC

# Windows 文件名禁用字符
_ILLEGAL_CHARS = '/\\:*?"<>|'
# 保留设备名: "CON.txt" 也算设备名
_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL"} | {
    "{}{}".format(prefix, i) for prefix in ("COM", "LPT") for i in range(1, 10)}
# 名字后面还要拼 "_任务_尺寸_规模.onnx", 留足 MAX_PATH 余量
MAX_NAME_LEN = 64

_CHAR_DISPLAY = {"\n": "\\n", "\t": "\\t", "\r": "\\r"}


def _check_common(name):
    if not name:
        return QC.translate("NameRules", "名称不能为空")
    if len(name) > MAX_NAME_LEN:
        return QC.translate("NameRules", "名称过长, 最多 {} 个字符").format(
            MAX_NAME_LEN)
    return ""


def _bad_chars(name, illegal):
    seen = []
    for ch in name:
        if (ch in illegal or ord(ch) < 32) and ch not in seen:
            seen.append(ch)
    return seen


def _bad_chars_message(bad):
    return QC.translate("NameRules", "名称不能包含「{}」等字符").format(
        " ".join(_CHAR_DISPLAY.get(ch, ch) for ch in bad))


def check_path_name(name):
    """项目名/数据集名: 会当文件名或目录名用. 返回不合法原因, 合法返回空串."""
    err = _check_common(name)
    if err:
        return err
    bad = _bad_chars(name, _ILLEGAL_CHARS)
    if bad:
        return _bad_chars_message(bad)
    if name.upper().split(".")[0] in _RESERVED_NAMES:
        return QC.translate("NameRules", "「{}」是系统保留名称, 请换一个").format(
            name)
    return ""


def check_label_name(name):
    """标签名: 只进文本文件, 查会让 classes.txt / data.yaml 串味的控制字符."""
    err = _check_common(name)
    if err:
        return err
    bad = _bad_chars(name, "")
    if bad:
        return _bad_chars_message(bad)
    return ""
