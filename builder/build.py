# -*- coding: utf-8 -*-
"""
程序发布
windows 输出installer.exe(dotnet实现)
windows 需要 cl.exe 否则 setuptools 找不到编译器。Linux 同理需要 gcc。
linux 输出release-linux(installer.sh + program.zip + requirements-release.txt)
"""

import argparse
import glob
import os
import platform
import shutil
import subprocess
import sys
import zipfile

from setuptools import Extension, setup

try:
    from Cython.Build import cythonize
except ImportError:
    sys.exit("缺少 Cython,请先安装：pip install cython")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(ROOT, "build")
ALWAYS_PLAIN = {"__init__.py", "easy_trainer.py"}
DATA_DIRS = ("style", "resources", "examples")


def collect_py(root_dir, base_pkg):
    """遍历包目录生成 Extension 清单"""
    exts = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in sorted(filenames):
            if not fn.endswith(".py") or fn in ALWAYS_PLAIN:
                continue
            file_path = os.path.join(dirpath, fn)
            rel = os.path.relpath(file_path, root_dir)[:-3].replace(os.sep, ".")
            module = "{}.{}".format(base_pkg, rel) if rel else base_pkg
            exts.append(Extension(module, [file_path]))
    return exts


def copy_plain(root_dir, target):
    """把保留明文的 .py 拷到目标（含 __init__.py 与 easy_trainer.py）。"""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in sorted(filenames):
            if fn not in ALWAYS_PLAIN:
                continue
            src = os.path.join(dirpath, fn)
            dst = os.path.join(target, os.path.relpath(src, ROOT))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)


def copy_data(target):
    for name in DATA_DIRS:
        src = os.path.join(ROOT, name)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(target, name), dirs_exist_ok=True)


def publish_installer():
    """
    windows 发布 installer.exe
    """
    dotnet = shutil.which("dotnet")
    if dotnet is None:
        sys.exit("找不到 dotnet,无法发布安装器. 请先安装 .NET SDK：https://dotnet.microsoft.com/download")
    proj_dir = os.path.join(ROOT, "installer", "Win.installer")
    proj = os.path.join(proj_dir, "Win.installer.csproj")
    out_dir = os.path.join(ROOT, "dist", "release")
    cmd = [dotnet, "publish", proj,
           "-c", "Release", "-r", "win-x64",
           "--self-contained", "true",
           "-p:PublishSingleFile=true",
           "-o", out_dir]
    print("发布安装器: " + " ".join(cmd))
    ret = subprocess.run(cmd, cwd=proj_dir)
    if ret.returncode != 0:
        sys.exit("dotnet publish 失败 (exit={})，请查看上方错误".format(ret.returncode))
    exe = os.path.join(out_dir, "installer.exe")
    if os.path.isfile(exe):
        print("installer.exe 就绪: {} ({:.1f}MB)".format(exe, os.path.getsize(exe) / 1048576))
    else:
        sys.exit("dotnet publish 结束但未找到 {}".format(exe))


def publish_linux(program_zip):
    """
    Linux 发布 dist/release-linux（installer.sh + program.zip + requirements + 权重清单）。
    """
    out_dir = os.path.join(ROOT, "dist", "release-linux")
    os.makedirs(out_dir, exist_ok=True)
    items = [
        (program_zip, "program.zip"),
        (os.path.join(HERE, "requirements-release.txt"), "requirements-release.txt"),
        (os.path.join(HERE, "pretrained-assets.txt"), "pretrained-assets.txt"),
        (os.path.join(ROOT, "installer", "installer.sh"), "installer.sh"),
    ]
    total = 0
    for src, name in items:
        if not os.path.isfile(src):
            sys.exit("发布 Linux 缺少文件: {}".format(src))
        shutil.copy2(src, os.path.join(out_dir, name))
        total += os.path.getsize(src)
        print("  打包:", name)
    os.chmod(os.path.join(out_dir, "installer.sh"), 0o755)
    print("Linux 发布就绪: {} ({:.1f}MB)".format(out_dir, total / 1048576))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target", default=os.path.join(ROOT, "dist", "program"),
                    help="输出目录(默认 dist/program)")
    args = ap.parse_args()

    target = os.path.abspath(args.target)
    if os.path.exists(target):
        shutil.rmtree(target)

    exts = []
    for pkg in ("app", "ui"):
        pkg_dir = os.path.join(ROOT, pkg)
        if os.path.isdir(pkg_dir):
            exts += collect_py(pkg_dir, pkg)
    if not exts:
        sys.exit("没找到要编译的 .py")

    # 拷贝明文与数据目录放在编译前做,目标目录已就绪
    os.makedirs(target, exist_ok=True)
    copy_plain(os.path.join(ROOT, "app"), target)
    copy_plain(os.path.join(ROOT, "ui"), target)
    copy_data(target)

    compile_args = [] if platform.system() == "Windows" else ["-Os"]
    cy_modules = cythonize(
        exts,
        nthreads=max(4, os.cpu_count() or 4),
        build_dir=BUILD_DIR,
        quiet=False,
        compiler_directives={
            "language_level": 3,
            "always_allow_keywords": True,
        },
    )
    sys.argv = [sys.argv[0]]
    setup(name="easy_trainer_pyd", ext_modules=cy_modules,
          script_args=["build_ext"],
          options={
              "build_ext": {"inplace": False},
              "build": {"build_base": BUILD_DIR},
          })

    built = [p for p in glob.glob(os.path.join(BUILD_DIR, "lib.*"))
             if os.path.isdir(p)]
    if not built:
        built = [p for p in glob.glob(os.path.join(BUILD_DIR, "lib"))
                 if os.path.isdir(p)]
    if not built:
        listing = "\n".join(sorted(os.listdir(BUILD_DIR))) \
            if os.path.isdir(BUILD_DIR) else "(build/ 不存在)"
        sys.exit("编译完成但找不到 build/lib* build/ 内容:\n" + listing)
    lib_root = built[0]
    for dirpath, dirnames, filenames in os.walk(lib_root):
        for fn in filenames:
            if not fn.endswith((".pyd", ".so")):
                continue
            src = os.path.join(dirpath, fn)
            dst = os.path.join(target, os.path.relpath(src, lib_root))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print("  pyd:", os.path.relpath(dst, target))

    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    print("program 根目录就绪: {}".format(target))
    zip_out = os.path.join(os.path.dirname(target), "program.zip")
    count = 0
    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for dirpath, dirnames, filenames in os.walk(target):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in sorted(filenames):
                src = os.path.join(dirpath, fn)
                arc = os.path.relpath(src, target).replace(os.sep, "/")
                zf.write(src, arc)
                count += 1
    print("program.zip 就绪: {} ({} 个文件, {:.1f}MB)".format(
        zip_out, count, os.path.getsize(zip_out) / 1048576))

    if platform.system() == "Windows":
        publish_installer()
    else:
        publish_linux(zip_out)
    for _p in (target, zip_out):
        if os.path.isdir(_p):
            shutil.rmtree(_p, ignore_errors=True)
        elif os.path.isfile(_p):
            os.remove(_p)
    print("已清理: dist/program/ dist/program.zip")


if __name__ == "__main__":
    main()
