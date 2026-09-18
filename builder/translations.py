# -*- coding: utf-8 -*-
"""界面翻译: 抽条目 -> 更新 i18n/*.ts -> 编译出 .qm. 改过界面文案后跑一次:

    python builder/translations.py

译文在 .ts 里改, 本脚本只做抽取与编译; 产物 i18n/<lang>.qm 由 build.py 随发行包发布.
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(ROOT, "i18n")

# 与 app/core/i18n.py 的 LANGUAGES 对应(默认语言中文不需要文件)
TARGETS = ("en_US", "zh_TW", "ja_JP", "ko_KR", "de_DE", "es_ES", "fr_FR", "vi_VN")


def _tool(name):
    """
    找 pyside6-lupdate / pyside6-lrelease.
    先看 PATH, 再看当前解释器同级的 bin / Scripts(venv 里这两个工具
    不一定进 PATH, Windows 上还带 .exe 后缀).
    """
    exe = shutil.which(name)
    if exe:
        return exe
    bindir = os.path.dirname(sys.executable)
    for d in (bindir, os.path.join(bindir, "Scripts"), os.path.join(bindir, "bin")):
        for candidate in (name, name + ".exe"):
            path = os.path.join(d, candidate)
            if os.path.exists(path):
                return path
    raise SystemExit("找不到 {}: 装 PySide6 用 pip install pyside6".format(name))


def sources():
    """待抽取的源: 全部 .ui + app/ 下所有 .py(只认 tr()/translate() 包住的字符串)."""
    files = []
    ui_dir = os.path.join(ROOT, "ui")
    files += sorted(os.path.join(ui_dir, fn)
                    for fn in os.listdir(ui_dir) if fn.endswith(".ui"))
    app_dir = os.path.join(ROOT, "app")
    for dirpath, dirnames, filenames in os.walk(app_dir):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        files += sorted(os.path.join(dirpath, fn)
                        for fn in filenames if fn.endswith(".py"))
    return files


def main():
    os.makedirs(I18N_DIR, exist_ok=True)
    src = sources()
    lupdate = _tool("pyside6-lupdate")
    lrelease = _tool("pyside6-lrelease")
    for lang in TARGETS:
        ts = os.path.join(I18N_DIR, lang + ".ts")
        qm = os.path.join(I18N_DIR, lang + ".qm")
        print("== {} ==".format(lang))
        # -target-language 不能省: 少了它新生成的 .ts 根元素没有 language 属性,
        # 之后 lupdate 会拒绝更新该文件("does not specify any target languages"),
        # 界面文案改了也抽不进来, 这个语言就永远停在旧条目上.
        # -no-obsolete: 少了它, 文案删掉后条目会以 type="vanished" 留在 .ts 里越积越多
        # (译文要找回可查 git 历史)
        subprocess.run([lupdate] + src + ["-ts", ts, "-target-language", lang,
                                          "-no-obsolete"], check=True)
        subprocess.run([lrelease, ts, "-qm", qm], check=True)
    print("\n完成. 新抽出的条目是 type=\"unfinished\", 编译时会被跳过并回退中文.")


if __name__ == "__main__":
    main()
