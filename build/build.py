# -*- coding: utf-8 -*-
"""
把 app/ 与 ui/ 编译成 .pyd，输出可发布的 program 根目录。

产物布局（program.zip 由 installer 解压到安装根）:
    app/  ui/           编译后的 .pyd + 保留的 __init__.py / easy_trainer.py
    style/ resources/   素材原样拷贝
    examples/           参考代码原样拷贝（导出 ONNX 时会复制给用户）

保留明文：所有 __init__.py（包结构需要）、app/easy_trainer.py（桌面快捷方式用 pythonw 直接执行它，sys.path[0] 在 app/ 下，
靠文件头 append 到项目根）。其余模块含 train_runner/test_runner 全部编译 —— worker 已改 python -m 调用。

Windows 需要 cl.exe 可用（在 VS Developer Prompt / vcvars64 里执行），否则
setuptools 找不到编译器。Linux 同理需要 gcc。
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
    sys.exit("缺少 Cython，请先安装：pip install cython")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 保留明文：包结构文件 + 入口脚本
ALWAYS_PLAIN = {"__init__.py", "easy_trainer.py"}
# 随发布拷走的数据目录
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
    dotnet publish 安装器：csproj 构建期把 program.zip 与 requirements-release.txt
    嵌进 exe，所以必须在 program.zip 就绪后执行。失败中断 —— 缺内嵌资源的
    安装器发布出去是不完整的。
    """
    dotnet = shutil.which("dotnet")
    if dotnet is None:
        sys.exit("找不到 dotnet，无法发布安装器。请先安装 .NET SDK：https://dotnet.microsoft.com/download")
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target", default=os.path.join(ROOT, "dist", "program"),
                    help="输出目录(默认 dist/program)")
    ap.add_argument("--keep-build", action="store_true",
                    help="编译后保留 build/ 与生成的 .c")
    ap.add_argument("--no-publish", action="store_true",
                    help="跳过 dotnet publish(仅编译 pyd 调试用)")
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
        build_dir=os.path.join(ROOT, "build"),
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
              "build": {"build_base": os.path.join(ROOT, "build")},
          })

    built = [p for p in glob.glob(os.path.join(ROOT, "build", "lib.*"))
             if os.path.isdir(p)]
    if not built:
        built = [p for p in glob.glob(os.path.join(ROOT, "build", "lib"))
                 if os.path.isdir(p)]
    if not built:
        listing = "\n".join(sorted(os.listdir(os.path.join(ROOT, "build")))) \
            if os.path.isdir(os.path.join(ROOT, "build")) else "(build/ 不存在)"
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

    if not args.keep_build:
        _bdir = os.path.join(ROOT, "build")
        for _name in os.listdir(_bdir):
            if _name in ("build.py", "requirements-release.txt"):
                continue
            _p = os.path.join(_bdir, _name)
            if os.path.isdir(_p):
                shutil.rmtree(_p, ignore_errors=True)
            else:
                os.remove(_p)
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

    if not args.no_publish:
        publish_installer()
        for _p in (target, zip_out):
            if os.path.isdir(_p):
                shutil.rmtree(_p, ignore_errors=True)
            elif os.path.isfile(_p):
                os.remove(_p)
        print("已清理: dist/program/ dist/program.zip")
    else:
        print("已跳过 dotnet publish(--no-publish),保留 program/ 与 program.zip 供检查")


if __name__ == "__main__":
    main()
