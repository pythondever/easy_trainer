# -*- coding: utf-8 -*-
"""
异常检测模型的导出包.

AD 模型是"骨干 + 良品特征库"的组合结构, 不是一条前向网络, 导不出 ONNX. 交付的是
训练时那个 ad_model.pt, 外加几份旁挂文件: 阈值单独成文本(不装软件也能一眼看到判定线),
训练时的验证集指标留档, README 写清新机器上怎么把它跑起来.

模型文件本身是自包含的 —— 构造参数、全部权重、判定阈值都在里面, 外部按 kwargs
重建即可, 实测分数与软件里逐位一致.
"""

import os
import shutil

from PySide6.QtCore import QCoreApplication as QC

MODEL_SUFFIX = ".pt"
THRESHOLD_FILE = "threshold.txt"
RESULT_FILE = "result.json"
README_FILE = "README.txt"

# 面向拿到文件夹就要跑起来的人, 中文纯文本 —— 交付物不是界面, 不进 i18n
_README = """异常检测模型
==============

由 EasyTrainer 导出。算法 {model}，输入尺寸 {size}，良品类别 {normal}。

本目录内容
----------
- {model_name}：模型文件（自包含：构造参数 + 全部权重 + 判定阈值）
- threshold.txt：判定阈值，一行数字
- result.json：训练时的验证集指标
- examples/：各语言调用示例

判定规则
--------
每张图算出一个异常分（特征空间的距离，不是 0~1 的概率），分数 >= 阈值判为异常。
阈值是训练时在验证集上按最优 F1 定的，换一批数据重挑等于拿测试集调参，所以直接
沿用本目录里的值。

怎么用
------
1. 准备 Python 环境：

       pip install anomalib==2.6.2 torch

2. 离线机器还要备一份骨干权重 wide_resnet50_2.racm_in1k（约 275 MB）。anomalib 建
   模型时就要从 HuggingFace 缓存里取，缺了会直接报 LocalEntryNotFoundError——
   哪怕权重已经在模型文件里。按 HF 的目录约定放好即可：

       ~/.cache/huggingface/hub/models--timm--wide_resnet50_2.racm_in1k/
           snapshots/<revision>/model.safetensors

   联网的机器不用管，timm 会自己下载。

3. 跑推理：

       python examples/python/ad.py --model {model_name} --images D:/待测图像

   输入尺寸与判定阈值都会从模型文件里读出来，不用手动传。
"""


def _read_info(model_path):
    """读出要写进说明与 threshold.txt 的几项; 只要标量, 不碰权重."""
    import torch

    # 优先安全加载; 万一有张量类型不在白名单再退回完整加载(文件是本机训练产出的)
    try:
        ckpt = torch.load(model_path, map_location="cpu", weights_only=True)
    except Exception:
        ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    return {
        "model": str(ckpt.get("ad_model", "")),
        "size": int(ckpt.get("img_size") or 0),
        "normal": str(ckpt.get("normal_class", "")),
        "threshold": float(ckpt.get("threshold") or 0.0),
    }


def build(model_path, out_dir, base, log=print):
    """产出导出包, 返回写进去的文件名列表."""
    info = _read_info(model_path)

    copied = []
    model_name = base + MODEL_SUFFIX
    log(QC.translate("AdPackage", "正在复制模型文件..."))
    shutil.copy2(model_path, os.path.join(out_dir, model_name))
    copied.append(model_name)

    with open(os.path.join(out_dir, THRESHOLD_FILE), "w", encoding="utf-8") as f:
        f.write("{:.6f}\n".format(info["threshold"]))
    copied.append(THRESHOLD_FILE)

    # 训练时那次验证集评估的结论, 有就带上 —— 交付方要讲精度只能拿它
    src = os.path.join(os.path.dirname(model_path), RESULT_FILE)
    if os.path.isfile(src):
        shutil.copy2(src, os.path.join(out_dir, RESULT_FILE))
        copied.append(RESULT_FILE)

    with open(os.path.join(out_dir, README_FILE), "w", encoding="utf-8") as f:
        f.write(_README.format(
            model=info["model"], normal=info["normal"] or "-",
            size=info["size"] or "原尺寸", model_name=model_name))
    copied.append(README_FILE)
    return copied
