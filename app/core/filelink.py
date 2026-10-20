# -*- coding: utf-8 -*-
"""
数据铺设时的文件搬运: 同卷走硬链接, 跨卷退回复制.
图像是只读素材, 铺出来的副本只是给训练框架一个统一目录, 没必要把整份像素
再写一遍. 抽成公共模块是因为数据准备、分类、异常检测、OCR 四条链路都要铺
数据, 各自写一遍同一段 try/except 迟早会长歪.
"""

import os
import shutil


def clone_file(src, dst):
    """
    把 src 搬到 dst: 同卷硬链接优先, 失败退回复制(保留元数据).
    目标已存在时先删掉再建: 它可能是上一轮铺数据留下的硬链接, 就地覆盖会
    顺着同一个数据块改到那份源图.
    """
    if os.path.exists(dst):
        try:
            os.remove(dst)
        except OSError:
            pass
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)
