# -*- coding: utf-8 -*-
"""训练权重文件的回找: 记录里存的路径失效时, 按同目录的候选名兜底.

记录刚建时填的是该任务权重的预期名, 训练被停止或失败时走不到 runner 的
RESULT 覆盖, 名字可能与实际落盘的对不上; 导出与测试都要先过这里.
"""

import os

# 各任务训练产物的权重文件名, 顺序即优先级
CKPT_CANDIDATES = ("checkpoint_best.pth", "checkpoint_best_ema.pth",
                   "checkpoint_best_regular.pth",
                   os.path.join("weights", "best.pt"))


def resolve_ckpt(path):
    """返回可用的权重路径: 给的路径不在时在同目录按候选名找, 都不在则原样返回."""
    if path and os.path.exists(path):
        return path
    model_dir = os.path.dirname(path) if path else ""
    if not model_dir or not os.path.isdir(model_dir):
        return path
    for cand in CKPT_CANDIDATES:
        p = os.path.join(model_dir, cand)
        if os.path.exists(p):
            return p
    return path
