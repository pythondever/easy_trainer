# -*- coding: utf-8 -*-
"""
AD(异常检测) 两个 runner 的公共部分: 目录收集, 正常类判定, 数据铺设.

只被 ad_train_runner / ad_test_runner 在子进程里导入. 主进程不碰 anomalib
(装不上也要能开界面), 所以这个模块和 classify_common 一样只在子进程生效.

AD 的数据来源走"按子文件夹分类"导入(导入根目录下的第一级子文件夹名=类别),
与分类任务同源: 同一份 根/{OK, 缺陷1}/图 目录, 分类拿它训多分类, AD 只把正常类
拿去建库, 其余类当测试集的异常真值.

铺到磁盘上的目录名一律用 ASCII 的 normal / c1 / c2 ..., 不直接用用户的类文件夹名.
两个原因缺一不可:
  * anomalib 的路径校验是 ^[\\x20-\\x7E]+$ (data/utils/path.py), 目录路径里
    有一个中文就 ValueError, 而"划痕""发白"正是中文用户最常用的类名;
  * 测试侧直接在用户的原始目录上跑, 两边要按同一个名字对真值, 得有个共同语言.
映射关系由 dir_to_class 带着, 评测前把目录名映回原始类名.
图片文件名不受这条限制(实测 anomalib 只校验目录路径), 所以复制时保留原名.
"""

import os
import shutil
import tempfile

from PySide6.QtCore import QCoreApplication as QC
import numpy as np
from sklearn.metrics import roc_auc_score
from app.core.constants import IMAGE_EXTS
from app.core.db import get_paths

NORMAL_NAMES = ("ok", "good", "normal", "fine", "pass",
                "良品", "正常", "正品", "正常品", "合格", "合格品",
                "无缺陷", "无瑕疵")

UNNAMED = ""

DIR_NORMAL = "normal"
DIR_ABNORMAL_PREFIX = "c"

MODEL_FILE = "ad_model.pt"

_ASCII_MIN, _ASCII_MAX = 0x20, 0x7E


DEFAULT_SEED = 42

# 热力图转异常区域多边形的参数(见 anomaly_rings)
MAP_MIN_AREA_RATIO = 0.0005   # 轮廓面积占整图比例, 低于此当噪声丢掉
MAP_POLY_EPS = 0.01           # 顶点抽稀容差, 取轮廓周长的比例
MAP_OPEN_KERNEL = 5           # 形态学开运算核, 去掉零散噪点


def seed_everything(seed=DEFAULT_SEED):
    import random

    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def is_ascii_path(path):
    """路径是否全为 ASCII 可打印字符 —— 与 anomalib 的校验规则同一口径."""
    return all(_ASCII_MIN <= ord(ch) <= _ASCII_MAX for ch in str(path))


def ascii_stage_dir(hint):
    """
    给 anomalib 用的暂存目录: 绝对路径纯 ASCII 才建得起来.
    优先用调用方给的位置(和输出放一起, 出问题好找); 输出选在"项目\\结果"
    这类中文目录下时退到系统临时目录, 再不行退到盘根 —— 宁可换个地方铺,
    也不要让用户为了跑算法去改自己的目录名.
    """
    drive = os.path.splitdrive(os.path.abspath(hint))[0]
    for cand in (hint,
                 os.path.join(tempfile.gettempdir(), "et_ad_stage"),
                 os.path.join(drive + os.sep, "et_ad_stage")):
        if not cand or not is_ascii_path(cand):
            continue
        try:
            os.makedirs(cand, exist_ok=True)
        except OSError:
            continue
        if os.access(cand, os.W_OK):
            return os.path.abspath(cand)
    raise ValueError(QC.translate(
        "AdCommon", "找不到可写的纯英文暂存目录(异常检测的底层库不支持中文路径), "
                    "请把输出路径改到纯英文目录下"))


def collect_classes(datasets, split):
    roots = []
    for ds in datasets:
        if ds.get("split") != split:
            continue
        roots.extend(get_paths(ds, "image"))
    return collect_from_roots(roots)


def collect_from_roots(roots):
    """
    {类别名: [图像路径]}, 类别取每个根目录下的第一级子文件夹名.
    图像散在根目录时归到 UNNAMED, 不再往下猜层级 —— 与导入侧
    (import_task.py 的 cls 分支) 取类别的口径一致, 免得同一批图在导入界面
    和训练时属于不同的类. 更深的层级只影响路径, 不产生新的类.
    """
    out = {}
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        for entry in sorted(os.listdir(root)):
            p = os.path.join(root, entry)
            if os.path.isdir(p):
                _add_tree(out, entry, p)
            elif entry.lower().endswith(IMAGE_EXTS):
                out.setdefault(UNNAMED, []).append(p)
    return out


def _add_tree(out, cls, sub):
    for r, _dirs, files in os.walk(sub):
        for fn in sorted(files):
            if fn.lower().endswith(IMAGE_EXTS):
                out.setdefault(cls, []).append(os.path.join(r, fn))


def _pick_normal(names, configured=""):
    """
    在类别集合里认正常类, 认不出返回 None.
    不能用空串表示"认不出": 空串是"根目录散图"这个合法类名, 一摞良品图平铺
    一个文件夹时它恰恰就是答案.
    """
    if configured:
        for c in names:
            if str(c).strip().lower() == str(configured).strip().lower():
                return c
        return None
    if len(names) == 1:
        return next(iter(names))
    for c in sorted(names):
        if c != UNNAMED and str(c).strip().lower() in NORMAL_NAMES:
            return c
    return None


def names_text(names):
    return ", ".join(QC.translate("AdCommon", "(根目录散图)") if n == UNNAMED else n
                     for n in sorted(names))


def guess_normal(names, configured=""):
    """
    在类别名集合里认正常类: 显式配置 > 常见叫法 > 只有一类就用它; 认不出返回 None.
    训练侧用不到这条(认不出直接报错, 建库集混进异常样本是致命的), 这里是
    测试侧的口径: 认不出还能退回"不评估真值".
    """
    got = _pick_normal(names, configured)
    return got if got is not None else _pick_normal(names)


def resolve_normal(train_map, val_map):
    """
    定出"哪个类别名代表正常", 返回 (正常类名, 训练侧被忽略的张数).
    常见叫法自动认 > 训练侧只有一类就用它. 认不出直接报错: 建库集里混进异常样本
    是无监督训练最致命的错误 —— 模型照样训完、指标照样出, 事后从结果里看不出来,
    所以宁可拦住, 让用户把良品类目录改成 NORMAL_NAMES 里的叫法再训.
    """
    all_names = set(train_map) | set(val_map)
    if not all_names:
        raise ValueError(QC.translate(
            "AdCommon", "数据集里没找到图像, 请先导入数据"))

    name = _pick_normal(all_names)
    if name is None:
        raise ValueError(QC.translate(
            "AdCommon", "无法从类别名判断哪个是正常品, 请把放良品图的那个文件夹改名为 "
                        "{} 之一; 现有类别: {}").format(
                            "/".join(NORMAL_NAMES), names_text(all_names)))

    if not train_map:
        raise ValueError(QC.translate("AdCommon", "训练集里没有图像"))
    if len(train_map) == 1:
        only = next(iter(train_map))
        if only not in (name, UNNAMED):
            raise ValueError(QC.translate(
                "AdCommon", "训练集里只有\"{}\"一类, 而良品类是\"{}\"; "
                            "请把良品图所在的类别文件夹挂到训练集上").format(
                                display_name(only), display_name(name)))
        ignored = 0
    elif name in train_map:
        ignored = sum(len(v) for k, v in train_map.items() if k != name)
    else:
        raise ValueError(QC.translate(
            "AdCommon", "训练集里既没有\"{}\"类、又不止一类, 无法确定拿哪批图建库; "
                        "现有类别: {}").format(name, names_text(train_map)))
    return name, ignored


def _dir_rows(class_map, normal_name):
    """
    (目录名, 原始类名) 列表: 正常类固定 normal, 异常类按类名排序编成 c1, c2...
    编号而不是音译: 用户类名长短和字符集都没法保证, 序号是唯一稳的.
    """
    rows = [(DIR_NORMAL, normal_name)]
    for i, cls in enumerate(sorted(set(class_map) - {normal_name}), 1):
        rows.append((DIR_ABNORMAL_PREFIX + str(i), cls))
    return rows


def _drop_empty_dirs(root):
    """删掉空的类别目录: 空目录会让 Folder 认为存在一个没有样本的类."""
    if not os.path.isdir(root):
        return
    for entry in os.listdir(root):
        d = os.path.join(root, entry)
        if os.path.isdir(d) and not os.listdir(d):
            os.rmdir(d)


def arrange(ad_root, datasets):
    """
    把两个 split 的图铺成 anomalib Folder 要的目录, 返回铺设结果与正常类名.
    目录固定为:
      <ad_root>/train/normal/**      建库集, 只有正常图
      <ad_root>/test/normal/**       测试集正常样本
      <ad_root>/test/c1, c2 .../**   测试集异常样本, 一个缺陷类一个目录
    每次整目录重建: 上一轮的类残留在里面会让这一轮凭空多出异常类.
    返回 (布局, 正常类名): 布局含 train / test_normal / abnormal{原类名: 张数} /
    ignored(训练侧被忽略的异常图张数) / dir_to_class(目录名 → 原始类名)
    """
    train_map = collect_classes(datasets, "train")
    val_map = collect_classes(datasets, "val")
    if UNNAMED in train_map and len(train_map) > 1:
        raise ValueError(QC.translate(
            "AdCommon", "训练集根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, "
                        "请把它们放进同一个类别文件夹"))
    name, ignored = resolve_normal(train_map, val_map)

    n_train = _rebuild(os.path.join(ad_root, "train", DIR_NORMAL),
                       train_map.get(name) if name in train_map
                       else [p for v in train_map.values() for p in v])
    n_test_normal = _rebuild(os.path.join(ad_root, "test", DIR_NORMAL),
                             val_map.get(name, []))
    dir_to_class = {}
    abnormal = {}
    for sub, cls in _dir_rows(val_map, name):
        dir_to_class[sub] = cls
        if cls == name:
            continue
        n = _rebuild(os.path.join(ad_root, "test", sub), val_map[cls])
        if n:
            abnormal[cls] = n
    _drop_empty_dirs(os.path.join(ad_root, "test"))
    return ({"train": n_train, "test_normal": n_test_normal,
             "abnormal": abnormal, "ignored": ignored,
             "dir_to_class": dir_to_class}, name)


def stage_test(ad_root, roots, normal_name=""):
    """
    把测试用的原始目录也铺一份, 返回 {dir_to_class, normal, total, origins}.
    测试侧本来可以直接在用户的原始目录上打分, 但 anomalib 不吃中文路径,
    用户的目录叫"数据\\划痕"就当场报错, 所以照样复制一份到 ASCII 目录下.
    origins 是"副本 → 原图", 结果里要显示用户原本那张图.
    """
    class_map = collect_from_roots(roots)
    if not class_map:
        raise ValueError(QC.translate("AdCommon", "没有找到任何图像, 请检查数据集"))
    if UNNAMED in class_map and len(class_map) > 1:
        raise ValueError(QC.translate(
            "AdCommon", "根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, "
                        "请把它们放进同一个类别文件夹"))
    name = guess_normal(set(class_map), normal_name)
    if name is None:
        raise ValueError(QC.translate(
            "AdCommon", "无法判断哪个类别是良品, 现有类别: {}.\n"
                        "请把良品图放在名为 {} 一类的子文件夹里, "
                        "或按训练时的方式重新导入数据集").format(
                            names_text(set(class_map)), "/".join(NORMAL_NAMES)))

    dir_to_class = {}
    origins = {}
    total = 0
    for sub, cls in _dir_rows(class_map, name):
        dir_to_class[sub] = cls
        total += _rebuild(os.path.join(ad_root, sub), class_map[cls], origins)
    _drop_empty_dirs(ad_root)
    return {"dir_to_class": dir_to_class, "normal": name,
            "total": total, "origins": origins}


def _rebuild(dst, paths, mapping=None):
    """
    清空并重建一个类别目录, 复制进 paths, 返回实际张数.
    mapping 非空时顺带记下"副本 → 原图", 明细和报告要显示用户原本那张图.
    """
    if os.path.isdir(dst):
        shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(dst, exist_ok=True)
    used = set()
    n = 0
    for src in paths:
        fn = os.path.basename(src)
        if fn in used:
            # 多个数据集合并时同名文件很常见, 加序号而不是覆盖
            base, ext = os.path.splitext(fn)
            i = 1
            while "{}_{}{}".format(base, i, ext) in used:
                i += 1
            fn = "{}_{}{}".format(base, i, ext)
        used.add(fn)
        copy = os.path.join(dst, fn)
        try:
            shutil.copy2(src, copy)
        except OSError:
            continue
        if mapping is not None:
            mapping[copy] = src
        n += 1
    return n


def abnormal_dirs(test_root):
    """
    test 铺好的异常目录名: 除正常类目录以外的所有目录, 排序后返回.
    必须逐个列全再交给 Folder: 传父目录会把正常类也当成一个异常类
    (实测 test/normal 的图被重复计入且真值标成异常).
    """
    if not os.path.isdir(test_root):
        return []
    return sorted(e for e in os.listdir(test_root)
                  if e != DIR_NORMAL and os.path.isdir(os.path.join(test_root, e)))


# ---------- AD 算法清单 ----------
AD_BACKBONE = "wide_resnet50_2"

# 安装器按 builder/pretrained-assets.txt 把骨干权重放到权重根目录的 ad/ 下
_BUNDLE_ASSET = os.path.join("ad", AD_BACKBONE + ".racm_in1k.safetensors")
_BACKBONE_BYTES = 275835296

_HF_REPO_DIR = "models--timm--wide_resnet50_2.racm_in1k"
_HF_REVISION = "30f73aceaaa1911830a9795b83ab1908dba18719"
_HF_FILENAME = "model.safetensors"


def ensure_backbone_cache():
    """
    把随安装包分发的骨干权重摆进 HuggingFace 缓存, 返回缓存里的权重路径(没有则空串).
    anomalib 建 TimmFeatureExtractor 时写死了 timm.create_model(pretrained=True),
    没有传本地文件的口子, 而 timm 只认 HF 缓存. 所以离线交付只能反过来做:
    安装器把权重要到 pretrained/ad/ 下, 这里在首次训练前按 HF 的目录约定摆好.
    缓存里已经有就什么都不做 —— 联网机器自己下过的那份不能被覆盖. 摆不进去也不报错,
    让 timm 照它原来的路子去联网, 失败信息由它给.
    """
    from huggingface_hub import constants as hf

    from app.core import model_assets

    src = ""
    for root in (model_assets.models_dir(), model_assets.default_dir()):
        # 用户改过权重目录时安装器那份还留在安装目录, 所以两个位置都找
        cand = os.path.join(root, _BUNDLE_ASSET)
        if os.path.isfile(cand) and os.path.getsize(cand) == _BACKBONE_BYTES:
            src = cand
            break

    repo = os.path.join(hf.HF_HUB_CACHE, _HF_REPO_DIR)
    dst = os.path.join(repo, "snapshots", _HF_REVISION, _HF_FILENAME)
    if os.path.isfile(dst) and os.path.getsize(dst) == _BACKBONE_BYTES:
        return dst
    if not src:
        return ""
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            os.link(src, dst)
        except OSError:
            pass
        if not os.path.isfile(dst):
            shutil.copy2(src, dst)
        os.makedirs(os.path.join(repo, "refs"), exist_ok=True)
        with open(os.path.join(repo, "refs", "main"), "w", encoding="utf-8") as f:
            f.write(_HF_REVISION)
    except OSError:
        return ""
    return dst if os.path.isfile(dst) else ""

AD_MODELS = (
    ("patchcore", "PatchCore", "Patchcore",
     {"layers": ("layer2", "layer3")}, False),
    ("cfa", "CFA", "Cfa", {}, False),
    ("stfpm", "STFPM", "Stfpm",
     {"layers": ["layer1", "layer2", "layer3"]}, True),
    ("fastflow", "FastFlow", "Fastflow", {}, True),
    ("reverse_distillation", "Reverse Distillation", "ReverseDistillation",
     {"layers": ("layer1", "layer2", "layer3")}, True),
)


def model_codes():
    return [m[0] for m in AD_MODELS]


def model_display(code):
    for m in AD_MODELS:
        if m[0] == code:
            return m[1]
    return str(code)


def _spec(code):
    for m in AD_MODELS:
        if m[0] == code:
            return m[2], dict(m[3]), m[4]
    raise ValueError(QC.translate("AdCommon",
                                  "未知的异常检测算法: {}").format(code))


def is_epoch_model(code):
    """该算法是否要吃轮次(建库型算法把轮次固定成 1)."""
    try:
        return _spec(code)[2]
    except ValueError:
        return False


def build_model(code, img_size=0, device="cpu"):
    """
    建 anomalib 模型; 返回 (模型, 类名, 可 JSON 化的构造参数).
    返回的构造参数存进模型文件, 测试时按它把模型原样重建 —— 只靠
    state_dict 恢复不了骨干结构, 而 anomalib 各算法的构造签名差异很大.
    这里顺带把骨干权重备到 HF 缓存(离线机器靠这一步, 见 ensure_backbone_cache).
    """
    import anomalib.models as M  # 只在子进程导入, 主进程不碰 anomalib

    ensure_backbone_cache()
    cls_name, kwargs, _needs = _spec(code)
    kwargs["backbone"] = AD_BACKBONE
    kwargs["visualizer"] = False
    cls = getattr(M, cls_name)
    model = cls(**_with_pre_processor(cls, kwargs, img_size))
    return model, cls_name, kwargs


def _with_pre_processor(cls, kwargs, img_size):
    """
    把图像尺寸塞进预处理器.
    anomalib 的预处理器在构造模型时就定死成 256x256(各算法都一样), 改不了
    之后. 产线图缩到 256 会把小缺陷一起抹掉, 所以这里显式重建一个.
    """
    out = dict(kwargs)
    size = int(img_size or 0)
    if size <= 0:
        return out
    try:
        out["pre_processor"] = cls.configure_pre_processor(
            image_size=(size, size))
    except Exception:
        pass
    return out


def load_model(code, cls_name, kwargs, img_size, state_dict_path):
    """
    按落盘的构造参数把模型重建并载入权重.
    重建时要先拿到骨干结构, 所以同样要骨干权重在手(见 ensure_backbone_cache).
    """
    import torch
    import anomalib.models as M

    ensure_backbone_cache()
    cls = getattr(M, cls_name)
    model = cls(**_with_pre_processor(cls, kwargs, img_size))
    ckpt = torch.load(state_dict_path, map_location="cpu", weights_only=False)
    model.load_state_dict(ckpt["state_dict"])
    return model


# ---------- 打分与评估 ----------

def predict_scores(engine, model, root, img_size=0, on_batch=None,
                   with_maps=False):
    """
    对 root 目录树逐图打分, 返回 [(图像路径, 分数, 热力图)].
    with_maps=False 时热力图为 None: 训练侧只判"这张是良品还是不良品", 没必要
    把 256×256 的图端出来; 测试侧要写异常区域, 才需要它.
    """
    from anomalib.data import PredictDataset

    size = int(img_size or 0)
    ds = PredictDataset(path=root, image_size=(size, size)) if size else \
        PredictDataset(path=root)
    out = engine.predict(model=model, dataset=ds, return_predictions=True)
    scored = []
    for batch in out or []:
        ps = getattr(batch, "pred_score", None)
        paths = getattr(batch, "image_path", None)
        if ps is None or paths is None:
            continue
        am = getattr(batch, "anomaly_map", None) if with_maps else None
        for i in range(ps.shape[0]):
            heat = None
            if am is not None:
                heat = am[i].squeeze().detach().cpu().numpy()
            scored.append((str(paths[i]), float(ps[i].flatten()[0]), heat))
        if on_batch is not None:
            on_batch(len(scored))
    return scored


def anomaly_rings(anomaly_map, score, width, height, threshold):
    """
    像素级热力图 → 原图坐标下的多边形顶点列表, 供写成 labelme json 复核.
    threshold 用图像级那个判定阈值, 但先按该图的 score/map.max 折算到像素域:
    anomalib 的图像分数是 anomaly map 的聚合(带平滑), 两者不严格相等(实测比值
    中位 1.03, 低分区波动到 1.15), 直接拿图像级阈值切会让"刚过判定线"的图切不出
    任何区域 —— 51 张测试图里有 1 张这样. 折算后两处才是同一口径.

    也不能逐图 min-max 归一化后取固定阈值: 良品图的 map 分布偏右, 归一化会把
    过半像素推到 0.5 以上, 实测切出的区域比真缺陷图还大(良品 0.115~0.868,
    缺陷 0.025~0.274), 人工复核时完全被误导.
    """
    import cv2
    import numpy as np

    if not threshold or threshold <= 0 or score <= 0:
        return []
    a = np.asarray(anomaly_map, dtype="float32").squeeze()
    if a.ndim != 2 or a.size == 0:
        return []
    thr = threshold * (float(a.max()) / score)
    mask = (a >= thr).astype(np.uint8)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                  (MAP_OPEN_KERNEL, MAP_OPEN_KERNEL)))
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sh, sw = a.shape
    sx, sy = width / sw, height / sh
    rings = []
    for c in cnts:
        if cv2.contourArea(c) * sx * sy / (width * height) < MAP_MIN_AREA_RATIO:
            continue
        # 抽稀: 原始轮廓有几百个顶点, 灌进 json 既难读也没必要
        poly = cv2.approxPolyDP(c, MAP_POLY_EPS * cv2.arcLength(c, True), True)
        if len(poly) < 3:
            continue
        rings.append([[float(p[0][0] * sx), float(p[0][1] * sy)] for p in poly])
    return rings


def pick_threshold(scores, labels):
    """
    在出现过的分数里挑 F1 最高的那个当阈值, 返回 (阈值, F1).
    与 anomalib 的 AdaptiveThreshold 同一思路. 样本只有一类时无需阈值,
    取分数中位数并返回 F1=0.
    """

    s = np.asarray(scores, dtype="float64")
    y = np.asarray(labels, dtype="int64")
    if s.size == 0:
        return 0.0, 0.0
    if y.min() == y.max():
        return float(np.median(s)), 0.0
    order = np.argsort(-s)
    s_sorted, y_sorted = s[order], y[order]
    tp = np.cumsum(y_sorted)
    fp = np.cumsum(1 - y_sorted)
    total_pos = int(y.sum())
    fn = total_pos - tp
    denom = 2 * tp + fp + fn
    f1 = np.divide(2.0 * tp, denom, out=np.zeros_like(tp, dtype="float64"),
                   where=denom > 0)
    best = int(np.argmax(f1))
    return float(s_sorted[best]), float(f1[best])


def evaluate(scored, normal_name, threshold=None):
    """
    把 [(类别名, 分数)] 按类别名推真值后算指标.
    两侧传进来的都必须是**原始类名**(不是铺到磁盘上的 normal / c1),
    调用方先用 dir_to_class 映回来; 真值口径就一句话: 类名等于
    normal_name 的是良品, 其余一律不良品.

    threshold 传空才现挑(F1 最优). 只有训练侧该现挑 —— 那是唯一手里有带真值
    验证集、要给模型定交付阈值的时刻. 测试侧必须沿用模型里存的阈值: 换一批
    数据重挑等于拿测试集调参, 精度会虚高; 同一批数据上重挑又与训练侧数字对不上.

    本批只有一类样本时挑不出阈值, 返回 single_class=True 且 accuracy=None,
    不硬凑一个分界.
    """

    labels, scores, dirs = [], [], []
    for item in scored:
        cls_dir = item[0]
        dirs.append(cls_dir)
        labels.append(0 if cls_dir == normal_name else 1)
        scores.append(float(item[1]))
    n = len(labels)
    out = {"total": n, "auroc": None, "threshold": 0.0, "accuracy": None,
           "TP": 0, "FN": 0, "FP": 0, "TN": 0, "per_class": {}}
    if n == 0:
        return out

    thr = float(threshold or 0.0)
    y = np.asarray(labels)
    if thr <= 0:
        if int(y.min()) == int(y.max()):
            out["single_class"] = True
            for cls_dir in dirs:
                st = out["per_class"].setdefault(
                    display_name(cls_dir),
                    {"total": 0, "correct": 0, "error": 0, "accuracy": None,
                     "hit": 0, "unnamed": not cls_dir})
                st["total"] += 1
            return out
        thr, f1 = pick_threshold(scores, labels)
        out["best_threshold"] = round(thr, 6)
        out["best_f1"] = round(f1, 6)
    out["threshold"] = round(thr, 6)
    pred = (np.asarray(scores) >= thr).astype("int64")
    out["TP"] = int(((pred == 1) & (y == 1)).sum())
    out["FN"] = int(((pred == 0) & (y == 1)).sum())
    out["FP"] = int(((pred == 1) & (y == 0)).sum())
    out["TN"] = int(((pred == 0) & (y == 0)).sum())
    out["accuracy"] = round((out["TP"] + out["TN"]) / n, 4)
    if 0 < int(y.sum()) < n:
        out["auroc"] = round(float(roc_auc_score(y, scores)), 6)

    per = {}
    for cls_dir, label, p in zip(dirs, labels, pred.tolist()):
        st = per.setdefault(display_name(cls_dir),
                            {"total": 0, "correct": 0, "error": 0,
                             "hit": 0, "unnamed": not cls_dir})
        st["total"] += 1
        st["correct"] += int(int(p) == int(label))
        st["error"] += int(int(p) != int(label))
        # 结果面板只报"检出了多少张"(测试侧多数没有真值), 单独记一笔
        st["hit"] += int(p)
    for st in per.values():
        st["accuracy"] = round(st["correct"] / max(st["total"], 1), 4)
    out["per_class"] = per
    return out


def display_name(cls_dir):
    """类别名 → 给人看的名字(只有"根目录散图"这个空类名要换个说法)."""
    return cls_dir or QC.translate("AdCommon", "(根目录散图)")


def truth_of_path(path, root):
    """一张图相对 root 的第一级目录名(铺设结构里的类目录名), 推不出返回空串."""
    try:
        rel = os.path.relpath(os.path.dirname(path), root)
    except ValueError:
        return ""
    if rel in (".", ""):
        return ""
    return rel.split(os.sep)[0]


