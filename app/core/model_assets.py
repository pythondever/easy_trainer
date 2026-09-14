# -*- coding: utf-8 -*-
"""
预训练权重清单与存放目录
文件名/字节数/MD5 与 rfdetr 包内 ModelWeights 注册表逐条对齐: 同名文件放进 RF_HOME,
模型构造阶段直接命中, 不再走它自己的在线下载(那条路径不显示进度, 失败只抛堆栈).
"""

import os

from app.core.utils import project_root

ENV_MODELS_DIR = "EASY_TRAINER_MODELS"
_SUBDIR = "pretrained"
# rfdetr 未设 RF_HOME 时的默认缓存位置
_RFDETR_DEFAULT = os.path.join("~", ".roboflow", "models")

DETECT = "detect"
SEGMENT = "segment"


class ModelAsset(object):
    """一个权重文件: 任务 + 档位定位, 文件名/大小/MD5 用于下载与校验."""

    __slots__ = ("task", "level", "filename", "nbytes", "md5", "desc", "url")

    def __init__(self, task, level, filename, nbytes, md5, desc, url):
        self.task = task
        self.level = level
        self.filename = filename
        self.nbytes = nbytes
        self.md5 = md5
        self.desc = desc
        self.url = url


_BASE = "https://storage.googleapis.com/rfdetr/"

MODELS = (
    ModelAsset(DETECT, "nano", "rf-detr-nano.pth", 366287238,
               "fb6504cce7fbdc783f7a46991f07639f", "速度最快, 精度够用",
               _BASE + "nano_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "small", "rf-detr-small.pth", 386045550,
               "fb37061c1af7bace359c91b723a8d5c1", "精度更好, 稍慢一些",
               _BASE + "small_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "medium", "rf-detr-medium.pth", 404992918,
               "7223f764a87b863f02eb8d52bf0ce2ee", "精度更高",
               _BASE + "medium_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "large", "rf-detr-large.pth", 1571684963,
               "992c8e862aa733a7bb2777e45d49f1a0", "精度最高, 显存占用大",
               _BASE + "rf-detr-large.pth"),
    ModelAsset(SEGMENT, "nano", "rf-detr-seg-nano.pt", 134545398,
               "9995497791d0ff1664a1d9ddee9cfd20", "轻量分割",
               _BASE + "rf-detr-seg-n-ft.pth"),
    ModelAsset(SEGMENT, "small", "rf-detr-seg-small.pt", 135042342,
               "0a2a3006381d0c42853907e700eadd08", "速度与精度平衡",
               _BASE + "rf-detr-seg-s-ft.pth"),
    ModelAsset(SEGMENT, "medium", "rf-detr-seg-medium.pt", 143024058,
               "a49af1562c3719227ad43d0ca53b4c7a", "细节更完整",
               _BASE + "rf-detr-seg-m-ft.pth"),
    ModelAsset(SEGMENT, "large", "rf-detr-seg-large.pt", 145055866,
               "275f7b094909544ed2841c94a677d07e", "最精细",
               _BASE + "rf-detr-seg-l-ft.pth"),
)

_NAMES = frozenset(a.filename for a in MODELS)


def find(task, level):
    for a in MODELS:
        if a.task == task and a.level == level:
            return a
    return None


def for_task(task):
    return [a for a in MODELS if a.task == task]


def default_dir():
    """安装目录下的权重目录(新装软件的默认下载位置)."""
    return os.path.join(project_root(), _SUBDIR)


def _has_weights(path):
    if not path or not os.path.isdir(path):
        return False
    for name in _NAMES:
        if os.path.isfile(os.path.join(path, name)):
            return True
    return False


def models_dir(saved=""):
    """
    权重目录: 显式设置 > 用户上次选的 > 安装目录 > RF_HOME > rfdetr 默认缓存.
    后三个只认"确实有权重文件"的目录, 否则会把用户已有的缓存判成缺失;
    一个都没有时回落安装目录下的 pretrained 作为下载目标.
    """
    env = os.environ.get(ENV_MODELS_DIR)
    if env:
        return os.path.abspath(os.path.expanduser(env))
    if saved:
        return os.path.abspath(os.path.expanduser(saved))
    root = default_dir()
    if _has_weights(root):
        return root
    for cand in (os.environ.get("RF_HOME"), _RFDETR_DEFAULT):
        if not cand:
            continue
        full = os.path.abspath(os.path.expanduser(cand))
        if _has_weights(full):
            return full
    return root


def set_models_dir(path, sync_rf_home=True):
    """
    切换权重目录; sync_rf_home 为假时不动 RF_HOME.
    用户刚点完"更改"还没下载时不能设 RF_HOME: 目标目录可能不可写, 设了就把它原本
    "回落 C 盘缓存"的兜底堵掉, 点"仍然继续"训练会直接失败. RF_HOME 只在目录里
    确实有可用权重时才同步(sync_rf_home() / 下载完成).
    """
    full = os.path.abspath(os.path.expanduser(path))
    os.environ[ENV_MODELS_DIR] = full
    if sync_rf_home:
        os.environ["RF_HOME"] = full
    return full


def path_of(asset, directory=None):
    return os.path.join(directory or models_dir(), asset.filename)


def is_ready(asset, directory=None):
    """
    就绪 = 文件存在且字节数相符.
    不校验 MD5: 1.4GB 的文件算一次要好几秒, 每次开界面都算不划算, 而且
    rfdetr 加载时自己会校验(哈希不符只警告, 不会重下).
    """
    p = path_of(asset, directory)
    try:
        return os.path.getsize(p) == asset.nbytes
    except OSError:
        return False


def missing(task, level, saved=""):
    """训练前预检: 返回该档位缺失的权重, 就绪返回 None."""
    asset = find(task, level)
    if asset is None:
        return None
    return None if is_ready(asset, models_dir(saved)) else asset


def human_size(nbytes):
    mb = nbytes / 1048576.0
    if mb >= 1024:
        return "{:.2f} GB".format(mb / 1024)
    return "{} MB".format(int(round(mb)))


def sync_rf_home(saved=""):
    """
    把当前权重目录写进 RF_HOME.
    引导层只在目录存在时设 RF_HOME, 用户手工拷进权重或改了目录后得补一次,
    否则本次训练的子进程仍会去 C 盘缓存找. 只在权重就绪时调, 目录不可写时不至于
    把 rfdetr 原本"回落 C 盘缓存"的兜底也堵掉.
    """
    return set_models_dir(models_dir(saved))
