# -*- coding: utf-8 -*-
"""下拉条目用到的纯文本换算: 设备名拆两行、档位选图标.

没有 Qt 依赖, 单测在 tests/test_combo_labels.py; 界面文案的拼装留给调用方,
这里只出"型号"和"12 GB"这类中性片段.
"""

import re

# device_probe 拼出来的显示名是 "<型号> (<显存> GB)", 弹层要拆成主标题与副标
_DEVICE_MEM = re.compile(
    r"^(?P<name>.+?)\s*\(\s*(?P<mem>\d+(?:\.\d+)?)\s*GB\s*\)$")

# 档位 -> 递增柱图标: 柱子数量就是档位高低
SIZE_ICONS = {"nano": "size_1", "small": "size_2", "medium": "size_3",
              "large": "size_4", "x-large": "size_5"}


def split_device_label(text):
    """
    拆设备显示名: 返回 (主标题, 显存片段).

    显存片段形如 "12 GB"(不含"显存"字样, 由调用方按界面语言拼);
    认不出格式时返回原文本与空串, 弹层就退化成单行条目.
    """
    text = str(text or "").strip()
    if not text:
        return "", ""
    match = _DEVICE_MEM.match(text)
    if match is None:
        return text, ""
    return match.group("name").strip(), "{} GB".format(match.group("mem"))


def size_icon_name(level):
    """档位对应的图标名; 异常检测算法名、OCR 型号这类非档位一律用通用图标."""
    return SIZE_ICONS.get(str(level or "").strip(), "model_generic")
