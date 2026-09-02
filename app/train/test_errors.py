# -*- coding: utf-8 -*-
"""错误样本归类的共用逻辑，测试进程与报告模块都从这里取。

单独开一个模块是因为 test_runner 跑在子进程里，不该为了算个 IoU 把
matplotlib 拖进来；而报告又要跟测试用同一套判定，否则界面上的数和
PDF 上的数会打架。
"""

# 漏检框与误检框 IoU 超过这个值就认定是同一个目标，合并显示成类别认错。
# 没匹配上却重合度这么高，只可能是类别被判错了。
CONFUSE_IOU = 0.5


def box_iou(a, b):
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    if inter <= 0:
        return 0.0
    ua = (max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
          + max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1]) - inter)
    return inter / ua if ua > 0 else 0.0


def pair_confusions(missing, spurious, iou_th=CONFUSE_IOU):
    """
    把重合的「漏检 GT + 误检预测」配成类别认错，剩余的照旧。
    missing / spurious 的元素统一是 {"cls": ..., "box": [x1,y1,x2,y2]}。
    返回 (pairs, 剩余 missing, 剩余 spurious)，pairs 元素为
    {"gt": ..., "pred": ..., "iou": ...}。
    只在展示层合并，不回改 TP/FP/FN：指标该怎么算还怎么算，这里只是让人
    看出这是分类问题（找得到但认错）而不是定位问题。
    同类别的不合并——那说明是框重复或位置差太多，不是认错。
    """
    cands = []
    for i, m in enumerate(missing):
        mb = m.get("box") or []
        if len(mb) != 4:
            continue
        for j, s in enumerate(spurious):
            sb = s.get("box") or []
            if len(sb) != 4:
                continue
            if str(m.get("cls", "")) == str(s.get("cls", "")):
                continue
            iou = box_iou(mb, sb)
            if iou >= iou_th:
                cands.append((-iou, i, j))
    cands.sort()
    pairs, used_m, used_s = [], set(), set()
    for neg_iou, i, j in cands:
        if i in used_m or j in used_s:
            continue
        used_m.add(i)
        used_s.add(j)
        pairs.append({"gt": missing[i], "pred": spurious[j], "iou": -neg_iou})
    return (pairs,
            [m for i, m in enumerate(missing) if i not in used_m],
            [s for j, s in enumerate(spurious) if j not in used_s])
