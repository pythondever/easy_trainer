# -*- coding: utf-8 -*-
"""
预训练权重清单与存放目录

本地文件名一律用档位名(nano.pt / nano-seg.pt), 与官方发布名无关: 下载按 asset.url 取远端
文件, 落到本地改成这个名, 所以 URL 里仍是原始名. 字节数/MD5 仍与 rfdetr 包内 ModelWeights
注册表逐条对齐.

权重根目录下按架构分 cnn / transformer 两个子目录. rfdetr 侧靠显式传 pretrain_weights
拿绝对路径(见 train_runner._make_model), 它只认路径不认文件名, 所以两套后端的权重即使
重名也不会互相扫到.
"""

import os
import shutil

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

# YOLO26 官方权重的国内镜像. GitHub 的 release 资产(走 objects.githubusercontent.com)
# 在国内直连会超时; 这个镜像给的是同一批文件, 字节数与 SHA256 已逐条对上 HF 仓库元数据.
_YOLO_BASE = "https://hf-mirror.com/Ultralytics/YOLO26/resolve/main/"

# 档位 → 权重名里的尺寸字母, 与训练界面「型号」下拉一一对应
_YOLO_SIZES = (("nano", "n"), ("small", "s"), ("medium", "m"),
               ("large", "l"), ("x-large", "x"))

# 文件名 → (字节数, MD5); 从镜像实拉后算出
_YOLO_FILES = {
    "yolo26n.pt": (5544453, "cf3cca69f04cf639bafdeb2644bd0843"),
    "yolo26s.pt": (20422725, "372e5c34064f37eb45dd7ef5cbbe60aa"),
    "yolo26m.pt": (44255705, "70f16444e4951c78f7e6afbadc3a2ee7"),
    "yolo26l.pt": (53211173, "33dbebc96173c86168e296f1dca50993"),
    "yolo26x.pt": (118667365, "84da48ba7b49f98e1c2c85dddb895fcd"),
    "yolo26n-seg.pt": (6719965, "9f9df23eb27d6ab64512bb670cd0ae96"),
    "yolo26s-seg.pt": (23467933, "91df624caffc982a5ed76f6061c01bf1"),
    "yolo26m-seg.pt": (54750385, "df1533ff3807c54301c0f62dfb229e0b"),
    "yolo26l-seg.pt": (63700037, "36b39a2d00e4a25c22e046673d7f0e7b"),
    "yolo26x-seg.pt": (142129861, "2da1da97683497fd796f4a980520c123"),
}

# ultralytics 训练前跑 AMP 自检时固定去 WEIGHTS_DIR 找这个文件名, 找不到就联网下一份.
# 我们 cnn 目录下的 nano.pt 就是它, 所以由 ensure_amp_weight 指过去.
_AMP_FILENAME = "yolo26n.pt"

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
    """YOLO26 检测/分割各五档; 档位名与 rf-detr 前四档同名同义."""
    out = []
    for level, letter in _YOLO_SIZES:
        for task, suffix, desc in ((DETECT_CNN, "", _YOLO_DESC[level]),
                                   (SEGMENT_CNN, "-seg",
                                    _YOLO_SEG_DESC[level])):
            # 远端名(MD5 表按它索引)与本地落盘名分开: 远端带 yolo26 前缀, 本地只用档位名
            remote = "yolo26{}{}.pt".format(letter, suffix)
            nbytes, md5 = _YOLO_FILES[remote]
            out.append(ModelAsset(task, level, level + suffix + ".pt",
                                  nbytes, md5, desc, _YOLO_BASE + remote))
    return out


# desc 是界面文案: 表里存中文原文, 显示时按 "ModelAssets" context 翻(NOOP 只为让 lupdate 抽得到)
MODELS = (
    ModelAsset(DETECT, "nano", "nano.pt", 366287238,
               "fb6504cce7fbdc783f7a46991f07639f",
               QT_TRANSLATE_NOOP("ModelAssets", "速度最快, 精度够用"),
               _BASE + "nano_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "small", "small.pt", 386045550,
               "fb37061c1af7bace359c91b723a8d5c1",
               QT_TRANSLATE_NOOP("ModelAssets", "精度更好, 稍慢一些"),
               _BASE + "small_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "medium", "medium.pt", 404992918,
               "7223f764a87b863f02eb8d52bf0ce2ee",
               QT_TRANSLATE_NOOP("ModelAssets", "精度更高"),
               _BASE + "medium_coco/checkpoint_best_regular.pth"),
    ModelAsset(DETECT, "large", "large.pt", 1571684963,
               "992c8e862aa733a7bb2777e45d49f1a0",
               QT_TRANSLATE_NOOP("ModelAssets", "精度最高, 显存占用大"),
               _BASE + "rf-detr-large.pth"),
    ModelAsset(SEGMENT, "nano", "nano-seg.pt", 134545398,
               "9995497791d0ff1664a1d9ddee9cfd20",
               QT_TRANSLATE_NOOP("ModelAssets", "轻量分割"),
               _BASE + "rf-detr-seg-n-ft.pth"),
    ModelAsset(SEGMENT, "small", "small-seg.pt", 135042342,
               "0a2a3006381d0c42853907e700eadd08",
               QT_TRANSLATE_NOOP("ModelAssets", "速度与精度平衡"),
               _BASE + "rf-detr-seg-s-ft.pth"),
    ModelAsset(SEGMENT, "medium", "medium-seg.pt", 143024058,
               "a49af1562c3719227ad43d0ca53b4c7a",
               QT_TRANSLATE_NOOP("ModelAssets", "细节更完整"),
               _BASE + "rf-detr-seg-m-ft.pth"),
    ModelAsset(SEGMENT, "large", "large-seg.pt", 145055866,
               "275f7b094909544ed2841c94a677d07e",
               QT_TRANSLATE_NOOP("ModelAssets", "最精细"),
               _BASE + "rf-detr-seg-l-ft.pth"),
    # YOLO26(CNN 架构)的检测/分割五档
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
    """asset 属于哪套后端: YOLO26 那批是 CNN, 其余是 rf-detr."""
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


def rel_path(asset):
    """
    权重在根目录下的相对路径(cnn/nano.pt). 跨架构指认一个权重时用它, 不要用
    asset.filename: 本地名只到档位, nano.pt 在两套架构下都有.
    """
    return "{}/{}".format(family_of(asset), asset.filename)


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


def resolve_path(task, level, family="transformer"):
    """
    训练子进程要传给后端的权重绝对路径; 没就绪返回空串.
    子进程拿不到 db, 靠父进程传下来的 EASY_TRAINER_MODELS 定位(models_dir 无参即可).
    """
    asset = find(asset_task(task, family), level)
    if asset is None:
        return ""
    return path_of(asset) if is_ready(asset) else ""


def ensure_amp_weight(weights_dir):
    """
    ultralytics 训练前固定去 weights_dir 找 yolo26n.pt 做 AMP 自检, 缺了就联网下一份 ——
    它和我们下载的 cnn/nano.pt 是同一个文件. 同卷建硬链接(不占额外空间), 跨卷退回复制;
    没下 nano 档就返回空串, 让它照原样去下或跳过.
    """
    src = path_of(find(DETECT_CNN, "nano"))
    if not os.path.isfile(src):
        return ""
    dst = os.path.join(str(weights_dir), _AMP_FILENAME)
    if os.path.isfile(dst):
        return dst
    try:
        os.makedirs(str(weights_dir), exist_ok=True)
        os.link(src, dst)
    except OSError:
        try:
            shutil.copyfile(src, dst)
        except OSError:
            return ""
    return dst


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
