# -*- coding: utf-8 -*-
"""
发布 deploy 模型转换工具, 产物在 deploy\\release\\ (deploy.exe + toolchain\\)

  python deploy\\build_deploy.py                全量发布(桥接源码变过会自动重编)
  python deploy\\build_deploy.py --arch sm120   换目标显卡架构
  python deploy\\build_deploy.py --no-trt       不发那 690MB 的 TensorRT 运行时
  python deploy\\build_deploy.py --probe        发布完跑一次环境自检
"""

import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.join(HERE, "Win.deploy")
CSPROJ = os.path.join(PROJ_DIR, "Win.deploy.csproj")
BRIDGE_SRC = os.path.join(HERE, "ovbridge", "ovbridge.cpp")
BRIDGE_CMD = os.path.join(HERE, "ovbridge", "build.cmd")
BRIDGE_DLL = os.path.join(PROJ_DIR, "native", "ovbridge.dll")

OV_DLLS = ("openvino.dll", "openvino_onnx_frontend.dll", "tbb12.dll")
TRT_BUILD_DLLS = ("nvinfer_10.dll", "nvinfer_plugin_10.dll", "nvonnxparser_10.dll")


def size_text(n):
    return "{:.1f}MB".format(n / 1048576.0) if n >= 1048576 else "{:.0f}KB".format(n / 1024.0)


def tree_size(path):
    total = 0
    for dirpath, _dirnames, filenames in os.walk(path):
        for fn in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, fn))
            except OSError:
                pass
    return total


def dir_has(path, names):
    return all(os.path.isfile(os.path.join(path, n)) for n in names)


def find_toolchain_root(target):
    for root in (os.path.join(target, "toolchain", "build"),
                 os.path.join(target, "toolchain", "runtime"),
                 os.path.join(target, "build"),
                 os.path.join(target, "runtime")):
        if dir_has(root, TRT_BUILD_DLLS):
            return root
    return None


def stop_running_exe():
    """正在跑的 deploy.exe 会锁住 release\\deploy.exe, 发布时直接失败"""
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq deploy.exe", "/NH"],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    except OSError:
        return
    if b"deploy.exe" not in out.lower():
        return
    print("发现正在运行的 deploy.exe, 先结束它")
    subprocess.run(["taskkill", "/F", "/IM", "deploy.exe", "/T"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def ensure_crlf(path):
    """
    批处理的行尾必须是 CRLF. LF-only 时 cmd 会从行中间开始解析(实测: 中文注释全被当命令),
    而编辑器/AI 工具默认写 LF, 所以每次调用前都查一遍
    """
    with open(path, "rb") as f:
        raw = f.read()
    if raw.count(b"\r\n") == raw.count(b"\n"):
        return
    with open(path, "wb") as f:
        f.write(raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n").replace(b"\n", b"\r\n"))
    print("{} 是 LF 行尾, 已改成 CRLF (cmd 解析 LF 批处理会出错)".format(os.path.basename(path)))


def build_bridge(sdk_dir, force):
    """
    编译桥接要用装着头文件的那份目录(与打包用的 runtime 不是同一个),
    .cmd 里已经会自己找, 所以默认不传参数
    """
    if not force:
        if not os.path.isfile(BRIDGE_DLL):
            print("桥接 dll 不存在, 尝试编译")
        else:
            dll = os.path.getmtime(BRIDGE_DLL)
            src = max(os.path.getmtime(BRIDGE_SRC), os.path.getmtime(BRIDGE_CMD))
            if dll >= src:
                print("桥接 ovbridge.dll 已是最新 (改过 ovbridge.cpp 就加 --bridge)")
                return True
            print("ovbridge.cpp 比 dll 新, 重新编译桥接")
    if not os.path.isfile(BRIDGE_CMD):
        print("找不到 {}".format(BRIDGE_CMD))
        return False
    ensure_crlf(BRIDGE_CMD)
    cmd = ["cmd", "/c", BRIDGE_CMD]
    if sdk_dir:
        cmd.append(sdk_dir)
    if subprocess.run(cmd, cwd=HERE).returncode != 0:
        print("编译桥接失败, 看 build.cmd 的输出")
        return False
    return True


def check_inputs(args, ov_dir, trt_dir):
    problems = []
    if not os.path.isfile(CSPROJ):
        problems.append("找不到工程文件: {}".format(CSPROJ))
    if shutil.which("dotnet") is None:
        problems.append("找不到 dotnet, 需要 .NET SDK 10 (https://dotnet.microsoft.com/download)"
                        " —— 注意不是 Runtime 包")

    if args.no_ov:
        print("OpenVINO 运行时: 本次不打包")
    else:
        missing = [n for n in OV_DLLS if not os.path.isfile(os.path.join(ov_dir, n))]
        if missing:
            problems.append("OpenVINO 运行时缺文件: {} (在 {} 里找)\n"
                            "    用 --ov-dir 指定, 或 --no-ov 关掉 IR 转换".format(
                                ", ".join(missing), ov_dir))
        else:
            print("OpenVINO 运行时: {} ({})".format(ov_dir, size_text(tree_size(ov_dir))))

    if args.no_trt:
        print("TensorRT 运行时: 本次不打包, release 里只有 IR 转换")
    else:
        build_root = find_toolchain_root(trt_dir)
        if build_root is None:
            problems.append("TensorRT 工具链不完整: {} 下没有 {}".format(
                trt_dir, "/".join(TRT_BUILD_DLLS)))
        else:
            arch_dir = os.path.join(trt_dir, "arch", args.arch)
            arch_dlls = [f for f in os.listdir(arch_dir)
                         if f.endswith(".dll")] if os.path.isdir(arch_dir) else []
            if not arch_dlls:
                problems.append("工具链里没有 {} 的 builder resource ({} 不存在或为空)\n"
                                "    换 --arch <架构>, 或 --no-trt 关掉 engine 转换".format(
                                    args.arch, arch_dir))
            else:
                print("TensorRT 运行时: {} ({} 个 dll + arch/{} 的 {}, {})".format(
                    build_root, len(TRT_BUILD_DLLS), args.arch,
                    ", ".join(arch_dlls), size_text(tree_size(build_root))))

    if not args.no_ov:
        if os.path.isfile(BRIDGE_DLL):
            print("桥接 dll: {} ({})".format(BRIDGE_DLL, size_text(os.path.getsize(BRIDGE_DLL))))
        else:
            problems.append("缺少 {} (跑 ovbridge\\build.cmd 生成)".format(BRIDGE_DLL))
    return problems


def clear_stale_toolchain(out_dir, arch, no_trt):
    """换架构/换开关后旧文件会留在发布目录里, 白带几百 MB 还可能被人当成有效架构"""
    tc = os.path.join(out_dir, "toolchain")
    if not os.path.isdir(tc):
        return
    if no_trt:
        shutil.rmtree(tc, ignore_errors=True)
        print("清掉上次发布的 {} (本次不带 TensorRT)".format(tc))
        return
    arch_root = os.path.join(tc, "arch")
    if not os.path.isdir(arch_root):
        return
    for name in os.listdir(arch_root):
        if name != arch:
            path = os.path.join(arch_root, name)
            size = tree_size(path)
            shutil.rmtree(path, ignore_errors=True)
            print("清掉残留架构 {} 的 resource ({})".format(name, size_text(size)))


def publish(args, ov_dir, trt_dir, out_dir):
    cmd = [shutil.which("dotnet"), "publish", CSPROJ,
           "-c", "Release", "-p:PublishProfile=win-x64",
           "--nologo", "-o", out_dir]
    if args.no_trt:
        cmd.append("-p:TrtSkip=1")
    else:
        cmd.append("-p:TrtArch={}".format(args.arch))
        cmd.append("-p:TrtToolchainDir={}".format(trt_dir))
    if args.no_ov:
        cmd.append("-p:OvSkip=1")
    else:
        cmd.append("-p:OvRuntimeDir={}".format(ov_dir))

    print()
    print("dotnet publish ...")
    ret = subprocess.run(cmd, cwd=HERE).returncode
    return ret


def report(out_dir, args):
    exe = os.path.join(out_dir, "deploy.exe")
    if not os.path.isfile(exe):
        print("发布结束但没找到 {}".format(exe))
        return 1
    print()
    print("发布完成: {}".format(out_dir))
    print("  deploy.exe            {}".format(size_text(os.path.getsize(exe))))
    tc = os.path.join(out_dir, "toolchain")
    if args.no_trt:
        print("  toolchain\\            未包含, 只有 IR 转换能用")
        return 0
    if not dir_has(os.path.join(tc, "build"), TRT_BUILD_DLLS):
        print("  toolchain\\            不完整, 缺构建用的 dll, 看上面的 dotnet 输出")
        return 1
    files = sum(len(fns) for _dp, _dn, fns in os.walk(tc))
    print("  toolchain\\            {}  {} 个文件".format(size_text(tree_size(tc)), files))
    arch_root = os.path.join(tc, "arch")
    if os.path.isdir(arch_root):
        for name in sorted(os.listdir(arch_root)):
            print("    arch\\{:<14}{}".format(
                name, size_text(tree_size(os.path.join(arch_root, name)))))
    return 0


def run_probe(out_dir):
    exe = os.path.join(out_dir, "deploy.exe")
    print()
    print("环境自检: deploy.exe --probe")
    # 接管输出再自己转印: 让它继承 stdout 的话一句都看不到(单文件是 GUI 子系统进程)
    p = subprocess.run([exe, "--probe"], cwd=out_dir,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.decode("utf-8", "replace").splitlines():
        print("  " + line)
    if p.returncode != 0:
        print("自检返回 {} (2=工具链/显卡不可用 3=缺 VC++ 运行库 4=OpenVINO 不可用)".format(p.returncode))
    return p.returncode


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description="发布 deploy 模型转换工具")
    ap.add_argument("--arch", default="sm89",
                    help="engine 用的显卡架构, 决定打包哪份 builder resource (默认 sm89)")
    ap.add_argument("--trt-dir", default="", help="TensorRT 工具链目录")
    ap.add_argument("--ov-dir", default="", help="OpenVINO 运行时目录(打三个 dll 进包)")
    ap.add_argument("--ov-sdk-dir", default="",
                    help="编译桥接用的 OpenVINO SDK 目录(含 include\\ 与 libs\\); 默认让 build.cmd 自己找")
    ap.add_argument("--out", default=os.path.join(HERE, "release"), help="输出目录")
    ap.add_argument("--no-trt", action="store_true", help="不打包 TensorRT 运行时")
    ap.add_argument("--no-ov", action="store_true", help="不打包 OpenVINO 运行时")
    ap.add_argument("--no-bridge", action="store_true", help="不检查也不重编 ovbridge.dll")
    ap.add_argument("--bridge", action="store_true", help="强制重编 ovbridge.dll")
    ap.add_argument("--probe", action="store_true", help="发布完跑一次 deploy.exe --probe")
    args = ap.parse_args()

    ov_dir = args.ov_dir or os.environ.get("OPENVINO_DIR") or r"D:\OpenVINO\runtime"
    trt_dir = args.trt_dir or os.environ.get("EASY_TRAINER_TRT") or r"D:\TensorRT\toolchain"
    out_dir = os.path.abspath(args.out)

    problems = check_inputs(args, ov_dir, trt_dir)

    if not args.no_bridge and not args.no_ov:
        if not build_bridge(args.ov_sdk_dir, args.bridge):
            problems.append("编译 ovbridge.dll 失败 (用 --no-ov 可以去掉 IR 转换后继续)")

    if problems:
        print()
        print("无法开始发布:")
        for p in problems:
            print("  - " + p)
        return 1

    stop_running_exe()
    os.makedirs(out_dir, exist_ok=True)
    clear_stale_toolchain(out_dir, args.arch, args.no_trt)

    if publish(args, ov_dir, trt_dir, out_dir) != 0:
        print("dotnet publish 失败!")
        return 1

    ret = report(out_dir, args)
    if ret == 0 and args.probe:
        run_probe(out_dir)
    return ret


if __name__ == "__main__":
    sys.exit(main())
