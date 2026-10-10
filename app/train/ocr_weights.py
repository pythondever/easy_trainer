# -*- coding: utf-8 -*-
"""
OCR 预训练权重的离线预置.
docTR 建模型时只按 default_cfgs 里的 URL 去自己的缓存找权重, 没有传本地路径的口子,
联网拿不到就会静默退化成从零训. 所以照 AD 骨干(ad_common.ensure_backbone_cache)
的路子: 安装器按 builder/pretrained-assets.txt 把权重下到权重根目录的 ocr/ 下,
训练前这里把它摆进 docTR 缓存, 之后 doctr 自己就找到了.

本地名跟其他架构一样按档位叫(nano.pt 这种), 但缓存里必须叫 doctr 下载时那个名字
(架构-哈希前 8 位), 两份名字不同, 所以每个架构记的是 (本地名, 缓存名) 一对.
"""

import hashlib
import os
import re
import shutil

from app.core import model_assets

_SUBDIR = "ocr"

# 架构对应 (本地档位名, docTR 缓存名). 缓存名与 doctr==1.0.1 的 default_cfgs 对齐,
# 升 doctr 要一起改.
# 检测段走 pretrained=True 取整模型权重; 识别段只复用骨干, 要的是骨干那一份.
# nano 与 small 的识别段是同一个网络, 所以识别骨干只有三份, 没有 small-rec.pt.
DET_FILES = {
    "db_mobilenet_v3_large": ("nano.pt", "db_mobilenet_v3_large-21748dd0.pt"),
    "linknet_resnet18": ("small.pt", "linknet_resnet18-e47a14dc.pt"),
    "db_resnet34": ("medium.pt", "db_resnet34-cb6aed9e.pt"),
    "db_resnet50": ("large.pt", "db_resnet50-79bd7d70.pt"),
}
RECO_FILES = {
    "crnn_mobilenet_v3_small": ("nano-rec.pt", "mobilenet_v3_small_r-1a8a3530.pt"),
    "crnn_mobilenet_v3_large": ("medium-rec.pt", "mobilenet_v3_large_r-74a22066.pt"),
    "crnn_vgg16_bn": ("large-rec.pt", "vgg16_bn_r-d108c19c.pt"),
}
_HASH_IN_NAME = re.compile(r"-([a-f0-9]*)\.")


def _cache_dir():
    """与 doctr.utils.data.download_from_url 的约定保持一致."""
    return os.path.join(
        os.environ.get("DOCTR_CACHE_DIR",
                        os.path.join(os.path.expanduser("~"), ".cache", "doctr")),
        "models")


def _hash_ok(path, prefix):
    """doctr 只认文件名里那段 sha256 前缀, 摆错内容的缓存会被它整份重下."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest().startswith(prefix)


def _place(local, cached):
    m = _HASH_IN_NAME.search(cached)
    if not m:
        return ""
    prefix = m.group(1)
    src = ""
    for root in (model_assets.models_dir(), model_assets.default_dir()):
        # 用户改过权重目录时安装器那份还留在安装目录, 所以两个位置都找
        cand = os.path.join(root, _SUBDIR, local)
        if os.path.isfile(cand):
            src = cand
            break
    if not src or not _hash_ok(src, prefix):
        return ""
    dst = os.path.join(_cache_dir(), cached)
    if os.path.isfile(dst) and _hash_ok(dst, prefix):
        return dst
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.isfile(dst):
            # 能走到这里说明缓存里那份内容不对(下载中断会留下半截文件).
            # 不先删掉, os.link 会因为目标已存在而失败, 后面的拷贝又被"文件在"跳过,
            # 这个坏文件被当成功返回后 doctr 会拒收并重新联网, 离线时就静默退化了
            try:
                os.remove(dst)
            except OSError:
                pass
        try:
            os.link(src, dst)
        except OSError:
            pass
        if not os.path.isfile(dst):
            shutil.copy2(src, dst)
    except OSError:
        return ""
    return dst if os.path.isfile(dst) else ""


def ensure(arch):
    """把权重根目录 ocr/ 下该架构的权重摆进 docTR 缓存, 返回缓存路径(没有则空串)."""
    pair = DET_FILES.get(arch) or RECO_FILES.get(arch)
    return _place(*pair) if pair else ""
