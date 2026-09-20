# PySide6 的 shiboken 会给 3.10 补一个 typing.Self; typing_extensions 见 typing 里
# 有 Self 就当成 3.11 的原生对象直接采用, 于是 torch 的 Union[X, Self] 会报
# "Plain typing.Self is not valid as type argument". 必须抢在 PySide6 之前定住这两个名字.
import typing as _typing

import typing_extensions as _te

if getattr(_typing, "Self", None) is not _te.Self:
    _typing.Self = _te.Self
