# -*- coding: utf-8 -*-
"""
html文档转pdf
"""

import os
import shutil
import subprocess
import sys

# Windows 常见安装路径
EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
# macOS 常见安装路径
MAC_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
# Linux/macOS 的 PATH 命令
PATH_COMMANDS = ["google-chrome", "google-chrome-stable", "chromium",
                 "chromium-browser", "microsoft-edge", "microsoft-edge-stable"]


def find_browser():
    for p in EDGE_CANDIDATES + MAC_CANDIDATES:
        if os.path.exists(p):
            return p
    for name in PATH_COMMANDS:
        p = shutil.which(name)
        if p:
            return p
    return ""


def main(in_html, out_pdf):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_arg = in_html
    if os.path.isabs(src_arg) or os.sep in src_arg or "/" in src_arg:
        src_path = src_arg
    else:
        src_path = os.path.join(base_dir, src_arg)
    dst_path = out_pdf
    if not os.path.exists(src_path):
        print("输入文件不存在: {}".format(src_path))
        sys.exit(1)
    src_path = os.path.abspath(src_path)
    dst_path = os.path.abspath(dst_path)
    browser = find_browser()
    if not browser:
        print("未找到 Edge/Chrome, 请安装 Microsoft Edge 或 Chrome 后重试")
        sys.exit(1)

    url = "file:///" + src_path.replace("\\", "/")
    cmd = [browser,
           "--headless", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer",
           "--print-to-pdf-no-header",
           '--print-to-pdf={}'.format(dst_path),
           url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
    except subprocess.TimeoutExpired:
        print("生成超时(120s)")
        sys.exit(1)
    if os.path.exists(dst_path):
        print("已生成: {}".format(dst_path))
    else:
        print("生成失败:\n{}".format((r.stdout or r.stderr)[-2000:]))
        sys.exit(1)


if __name__ == "__main__":
    _base = os.path.dirname(os.path.abspath(__file__))
    in_html = os.path.join(_base, "使用教程.html")
    out_pdf = os.path.join(_base, "使用教程.pdf")
    main(in_html, out_pdf)
