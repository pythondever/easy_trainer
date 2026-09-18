# -*- coding: utf-8 -*-
"""
预训练权重清单与存放目录
文件名/字节数/MD5 与 rfdetr 包内 ModelWeights 注册表逐条对齐: 同名文件放进 RF_HOME,
模型构造阶段直接命中, 不再走它自己的在线下载(那条路径不显示进度, 失败只抛堆栈).

权重根目录下按架构分 cnn / transformer 两个子目录. rfdetr 只认 RF_HOME 指向的单个
目录, 两套后端的权重混放会让它扫到不属于自己的文件.
"""

import os

from PySide6.QtCore import QT_TRANSLATE_NOOP

from app.core.utils import project_root

ENV_MODELS_DIR = "EASY_TRAINER_MODELS"
_SUBDIR = "pretrained"

CNN = "cnn"
TRANSFORMER = "transformer"

DETECT = "detect"
SEGMENT = "segment"
# CNN(YOLO) 的权重按任务另起两组, 这样 find/for_task 不必扩成三维签名
DETECT_CNN = "detect_cnn"
SEGMENT_CNN = "segment_cnn"


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

# YOLO11 官方权重的国内镜像. GitHub 的 release 资产(走 objects.githubusercontent.com)
# 在国内直连会超时, 这个镜像给的是同一批文件: 与 gh-proxy 转发官方源下到的
# 逐条比对过文件名/字节数/MD5, 完全一致.
_YOLO_BASE = "https://hf-mirror.com/Ultralytics/YOLO11/resolve/main/"

# 档位 → 权重名里的尺寸字母, 与训练界面「型号」下拉一一对应
_YOLO_SIZES = (("nano", "n"), ("small", "s"), ("medium", "m"),
               ("large", "l"), ("x-large", "x"))

# 文件名 → (字节数, MD5); 从镜像实拉后算出
_YOLO_FILES = {
    "yolo11n.pt": (5613764, "261474e91b15f5ef14a63c21ce6c0cbb"),
    "yolo11s.pt": (19313732, "9637097d5fbdc1002d25d2d3d9f7c435"),
    "yolo11m.pt": (40684120, "2c2bcbb54c3829b20d31a32524ee0f03"),
    "yolo11l.pt": (51387343, "92001a3126d6ebf548c1762038698214"),
    "yolo11x.pt": (114636239, "2f89622f77147e631f1e075e9fc6b795"),
    "yolo11n-seg.pt": (6182636, "edfa69d9468b2703b185f550e8f26251"),
    "yolo11s-seg.pt": (20669228, "0a0febcb560f334cb78ae8922382bf74"),
    "yolo11m-seg.pt": (45400152, "8cc5706386c334b11551d9cd779e304c"),
    "yolo11l-seg.pt": (56096965, "ca3de7ae1af6e4854c5d8d5eda796e3c"),
    "yolo11x-seg.pt": (125090821, "4c73cb4ac70d1dd4b104b18fedd862e7"),
}

# 前四档的描述与 rf-detr 用同一批文案(同 context 同文本, 共用已有译文)
_YOLO_DESC = {
    "nano": QT_TRANSLATE_NOOP("ModelAssets", "速度最快, 精度够用"),
    "small": QT_TRANSLATE_NOOP("ModelAssets", "精度更好, 稍慢一些"),
    "medium": QT_TRANSLATE_NOOP("ModelAssets", "精度更高"),
    "large": QT_TRANSLATE_NOOP("ModelAssets", "精度最高, 显存占用大"),
    "x-large": QT_TRANSLATE_NOOP("ModelAssets", "精度极致, 显存占用很大"),
}
_YOLO_SEG_DESC = {
    "nano": QT_TRANSLATE_NOOP("ModelAssets", "轻量分割"),
    "small": QT_TRANSLATE_NOOP("ModelAssets", "速度与精度平衡"),
    "medium": QT_TRANSLATE_NOOP("ModelAssets", "细节更完整"),
    "large": QT_TRANSLATE_NOOP("ModelAssets", "最精细"),
    "x-large": QT_TRANSLATE_NOOP("ModelAssets", "最精细, 显存占用很大"),
}


def _yolo_assets():
    """YOLO11 检测/分割各五档; 档位名与 rf-detr 前四档同名同义."""
    out = []
    for level, letter in _YOLO_SIZES:
        for task, suffix, desc in ((DETECT_CNN, "", _YOLO_DESC[level]),
                                   (SEGMENT_CNN, "-seg",
                                    _YOLO_SEG_DESC[level])):
            name = "yolo11{}{}.pt".format(letter, suffix)
            nbytes, md5 = _YOLO_FILES[name]
            out.append(ModelAsset(task, level, name, nbytes, md5, desc,
                                  _YOLO_BASE + name))
    return out


# desc 是界面文案: 表里存中文原文, 显示时按 "ModelAssets" context 翻(NOOP 只为让 lupdate 抽得到)
MODELS = (
    ModelAsset(DETECT, "nano", "rf-detr-nano.pth", 366287238,
               "fb6504cce7fbdc783f7a46991f07639f",
               QT_TRANSLATE_NOOP("ModelAssets", "速度最快, 精度够用"),
               _BASE + "nano_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "small", "rf-detr-small.pth", 386045550,
               "fb37061c1af7bace359c91b723a8d5c1",
               QT_TRANSLATE_NOOP("ModelAssets", "精度更好, 稍慢一些"),
               _BASE + "small_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "medium", "rf-detr-medium.pth", 404992918,
               "7223f764a87b863f02eb8d52bf0ce2ee",
               QT_TRANSLATE_NOOP("ModelAssets", "精度更高"),
               _BASE + "medium_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "large", "rf-detr-large.pth", 1571684963,
               "992c8e862aa733a7bb2777e45d49f1a0",
               QT_TRANSLATE_NOOP("ModelAssets", "精度最高, 显存占用大"),
               _BASE + "rf-detr-large.pth"),
    ModelAsset(SEGMENT, "nano", "rf-detr-seg-nano.pt", 134545398,
               "9995497791d0ff1664a1d9ddee9cfd20",
               QT_TRANSLATE_NOOP("ModelAssets", "轻量分割"),
               _BASE + "rf-detr-seg-n-ft.pth"),
    ModelAsset(SEGMENT, "small", "rf-detr-seg-small.pt", 135042342,
               "0a2a3006381d0c42853907e700eadd08",
               QT_TRANSLATE_NOOP("ModelAssets", "速度与精度平衡"),
               _BASE + "rf-detr-seg-s-ft.pth"),
    ModelAsset(SEGMENT, "medium", "rf-detr-seg-medium.pt", 143024058,
               "a49af1562c3719227ad43d0ca53b4c7a",
               QT_TRANSLATE_NOOP("ModelAssets", "细节更完整"),
               _BASE + "rf-detr-seg-m-ft.pth"),
    ModelAsset(SEGMENT, "large", "rf-detr-seg-large.pt", 145055866,
               "275f7b094909544ed2841c94a677d07e",
               QT_TRANSLATE_NOOP("ModelAssets", "最精细"),
               _BASE + "rf-detr-seg-l-ft.pth"),
    # YOLO11(CNN 架构)的检测/分割五档
    *_yolo_assets(),
)


def find(task, level):
    for a in MODELS:
        if a.task == task and a.level == level:
            return a
    return None


def for_task(task):
    return [a for a in MODELS if a.task == task]


def default_dir():
    """安装目录下的权重根目录(新装软件的默认下载位置)."""
    return os.path.join(project_root(), _SUBDIR)


def family_of(asset):
    """asset 属于哪套后端: YOLO11 那批是 CNN, 其余是 rf-detr."""
    return CNN if asset.task in (DETECT_CNN, SEGMENT_CNN) else TRANSFORMER


def dir_for(family, root=""):
    """某套后端的权重目录 = 根目录下的架构子目录."""
    return os.path.join(root or models_dir(), family)


def models_dir(saved=""):
    """
    权重根目录: 显式设置 > 用户上次选的 > 安装目录下的 pretrained.
    只返回根, 具体文件落在哪个子目录由 path_of 按架构决定.
    """
    env = os.environ.get(ENV_MODELS_DIR)
    if env:
        return os.path.abspath(os.path.expanduser(env))
    if saved:
        return os.path.abspath(os.path.expanduser(saved))
    return default_dir()


def set_models_dir(path, sync_rf_home=True):
    """
    切换权重根目录; sync_rf_home 为假时不动 RF_HOME.
    用户刚点完"更改"还没下载时不能设 RF_HOME: 目标目录可能不可写, 设了 rfdetr 就会
    一直在那儿找. RF_HOME 只在目录里确实有可用权重时才同步
    (sync_rf_home() / 下载完成).

    RF_HOME 指向 <根>/transformer: rfdetr 只认一个目录, 而它的权重都在那一支.
    """
    full = os.path.abspath(os.path.expanduser(path))
    os.environ[ENV_MODELS_DIR] = full
    if sync_rf_home:
        os.environ["RF_HOME"] = dir_for(TRANSFORMER, full)
    return full


def path_of(asset, directory=None):
    """directory 传的是根目录; 文件按架构落在子目录下."""
    return os.path.join(dir_for(family_of(asset), directory), asset.filename)


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


def asset_task(task, family="transformer"):
    """(任务, 架构) → 权重清单里的任务键: CNN 的检测/分割各占一组."""
    if family != "cnn":
        return task
    if task == DETECT:
        return DETECT_CNN
    if task == SEGMENT:
        return SEGMENT_CNN
    return task


def missing(task, level, saved="", family="transformer"):
    """训练前预检: 返回该档位缺失的权重, 就绪返回 None."""
    asset = find(asset_task(task, family), level)
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
    把当前权重根目录下的 transformer 子目录写进 RF_HOME.
    引导层设过一次, 但用户手工拷进权重或改了目录后得补一次, 否则本次训练的子进程
    仍会去它记着的旧位置找. 只在权重就绪时调.
    """
    return set_models_dir(models_dir(saved))
