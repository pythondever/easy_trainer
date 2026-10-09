# -*- coding: utf-8 -*-
"""
公用常量.
"""

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
# 缩略图分页大小
PAGE_SIZE = 50
# 缩略图/ROI 缓存张数上限(单个数据集内, 换页时按此淘汰)
THUMB_CACHE_MAX = 2000
ROI_CACHE_MAX = 2000
# QImage 缓存全局字节上限(切换数据集时跨数据集回收, 超了就整集清最旧的).
# 单个数据集满配额约 640MB, 这个额度够装两个满配额数据集, 也就是在
# A/B 之间横跳不会重解; 第三个数据集进来时才把最久没用的那个整集释放.
IMG_CACHE_BYTES_MAX = 1536 * 1024 * 1024
