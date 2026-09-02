# -*- coding: utf-8 -*-
"""
测试结果 PDF 报告：逐图定位漏检/误检样本，数据源是 details.jsonl。
页面顺序：汇总首页（模型 + 标注分布 + 指标 + 按类别）→ 缩略图 → 改进建议。
"""

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")          # 无显示设备的子进程里也要能出图

from matplotlib import font_manager
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Rectangle
from PIL import Image, ImageDraw, ImageFont

from app.train.test_errors import CONFUSE_IOU, pair_confusions

# 漏检=红(该抓没抓, 最危险) 误检=橙(过杀) 正确检出=绿(仅作位置参照)
# 类别认错=紫(位置对但判错类别, 是分类问题不是定位问题)
C_MISSING = "#e03131"
C_SPURIOUS = "#f08c00"
C_HIT = "#2f9e44"
C_CONFUSE = "#7048e8"

_A4_W_PT, _A4_H_PT = 595, 842      # A4 pt (1pt=1/72 英寸, 矢量 PDF 用)
_A4_W_IN, _A4_H_IN = 8.27, 11.69   # matplotlib figsize 用英寸
_GRID_COLS, _GRID_ROWS = 2, 3

# 首页/建议页都是 PIL 位图，统一这个 dpi 才能和 A4 英寸对上
_DPI = 150
_PAGE_W = int(round(_A4_W_IN * _DPI))
_PAGE_H = int(round(_A4_H_IN * _DPI))
_MARGIN = int(round(0.42 * _DPI))
_CONTENT_W = _PAGE_W - 2 * _MARGIN
_CHART_H = 240                     # 标注分布柱状图占位高度

PER_CLASS_LIMIT = 10

_CJK_FONTS = ("Microsoft YaHei", "SimHei", "DengXian", "Noto Sans CJK SC",
              "WenQuanYi Zen Hei", "Source Han Sans CN", "DejaVu Sans")
_WIN_FONTS = (r"C:\Windows\Fonts\msyh.ttc",
              r"C:\Windows\Fonts\simhei.ttf",
              r"C:\Windows\Fonts\simsun.ttc")


def _setup_font():
    avail = {f.name for f in font_manager.fontManager.ttflist}
    for name in _CJK_FONTS:
        if name in avail:
            plt.rcParams["font.sans-serif"] = [name]
            break
    plt.rcParams["axes.unicode_minus"] = False


def _pil_font(size):
    for p in _WIN_FONTS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    avail = {f.name for f in font_manager.fontManager.ttflist}
    for name in _CJK_FONTS:
        if name in avail:
            fpath = font_manager.findfont(name, fallback_to_default=False)
            try:
                return ImageFont.truetype(fpath, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _pick_image_font():
    avail = {f.name for f in font_manager.fontManager.ttflist}
    for name in _CJK_FONTS:
        if name in avail:
            try:
                fpath = font_manager.findfont(name, fallback_to_default=False)
                return fpath
            except Exception:
                continue
    for p in _WIN_FONTS:
        if os.path.exists(p):
            return p
    return None


def load_details(detail_path):
    rows = []
    if not detail_path or not os.path.exists(detail_path):
        return rows
    with open(detail_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except ValueError:
                continue
    return rows


def _thumb_arr(img_path, thumb_w):
    try:
        with Image.open(img_path) as im:
            im = im.convert("RGB")
            iw, ih = im.size
            scale = thumb_w / float(iw) if iw else 1.0
            th = max(1, int(round(ih * scale)))
            im = im.resize((thumb_w, th), Image.LANCZOS)
            return np.array(im), im.size[1], im.size[0], scale
    except Exception:
        return None, 0, 0, 1.0


def _err_counts(row, kind):
    out = {}
    for b in row.get(kind) or []:
        c = str(b.get("cls", ""))
        out[c] = out.get(c, 0) + 1
    return out


def _pair_confusions(row, iou_th=CONFUSE_IOU):
    return pair_confusions(row.get("missing") or [],
                           row.get("spurious") or [], iou_th)


def _sample_rows(rows, limit, confuse_iou=CONFUSE_IOU, conf_stat=None):
    """
    按「类别 × 错误类型」抽样，每格最多 limit 张。
    排序键是 (该类错误数降序, 明细原始次序)，保证先看错得最狠的图，
    且同一份明细重复导出得到的必然是同一批图，方便前后对比。
    同时有漏检和误检的图归到漏检段（误检框照样画，不丢信息）。
    conf_stat 由测试进程给出时直接用，省掉再遍历一遍明细
    """
    miss_total = sum(1 for r in rows if r.get("missing"))
    spur_total = sum(1 for r in rows if r.get("spurious"))
    if conf_stat is None:
        conf_stat = {"total": 0, "imgs": 0}
        for r in rows:
            n = len(_pair_confusions(r, confuse_iou)[0])
            if n:
                conf_stat["imgs"] += 1
                conf_stat["total"] += n
    conf_total = int(conf_stat.get("total", 0))
    conf_imgs = int(conf_stat.get("imgs", 0))
    if not limit or limit <= 0:
        miss = [r for r in rows if r.get("missing")]
        spur = [r for r in rows if r.get("spurious") and not r.get("missing")]
        stat = {"total": len(rows), "miss_total": miss_total,
                "spur_total": spur_total, "limit": 0,
                "conf_total": conf_total, "conf_imgs": conf_imgs,
                "shown": len(miss) + len(spur)}
        return miss, spur, stat

    taken = set()

    def pick(kind):
        buckets = {}
        for idx, r in enumerate(rows):
            for cls, n in _err_counts(r, kind).items():
                buckets.setdefault(cls, []).append((-n, idx))
        out = []
        for cls in sorted(buckets):
            got = 0
            for _, idx in sorted(buckets[cls]):
                if idx in taken:
                    continue
                taken.add(idx)
                out.append(rows[idx])
                got += 1
                if got >= limit:
                    break
        return out

    miss = pick("missing")
    spur = pick("spurious")

    def order(rs, kind):
        return sorted(rs, key=lambda r: (-len(r.get(kind) or []),
                                         os.path.basename(r.get("img", ""))))

    miss, spur = order(miss, "missing"), order(spur, "spurious")
    stat = {"total": len(rows), "miss_total": miss_total,
            "spur_total": spur_total, "limit": limit,
            "conf_total": conf_total, "conf_imgs": conf_imgs,
            "shown": len(miss) + len(spur)}
    return miss, spur, stat


def _any_poly(rows):
    """明细里带不带分割轮廓，决定首页图例要不要加那条说明。"""
    for r in rows:
        for kind in ("missing", "spurious", "hits"):
            for b in r.get(kind) or []:
                if b.get("poly"):
                    return True
    return False


def _err_foot(n_miss, n_spur, n_conf=0):
    parts = []
    if n_miss:
        parts.append("漏 {}".format(n_miss))
    if n_spur:
        parts.append("误 {}".format(n_spur))
    if n_conf:
        parts.append("认错 {}".format(n_conf))
    return "  ·  ".join(parts) or "—"


def _cell(ax, row, thumb_w, confuse_iou=CONFUSE_IOU):
    arr, h, w, sc = _thumb_arr(row["img"], thumb_w)
    base = os.path.basename(row.get("img", ""))
    pairs, miss_boxes, spur_boxes = _pair_confusions(row, confuse_iou)
    n_miss, n_spur, n_conf = len(miss_boxes), len(spur_boxes), len(pairs)

    if arr is None:
        ax.text(0.5, 0.5, "（图片无法打开）", ha="center", va="center",
                transform=ax.transAxes, color="#888888")
        ax.set_title(base + "  ·  " + _err_foot(n_miss, n_spur, n_conf),
                     fontsize=8)
        ax.set_xticks([]); ax.set_yticks([])
        return

    ax.imshow(arr, aspect="auto")
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.set_xticks([]); ax.set_yticks([])

    fig = ax.figure
    # 数据单位 → 屏幕像素，用来估算标签宽度：小框上贴长标签会糊成一片
    pos = ax.get_position()
    px_per_unit = (pos.width * fig.get_size_inches()[0] * fig.dpi / w
                   if w else 1.0)
    char_px = 6.0 / 72.0 * fig.dpi     # fontsize=6 的单个全角字符宽

    def _label_x(x1, txt):
        tw_u = len(txt) * char_px / px_per_unit
        return x1 if x1 + tw_u <= w else max(0.0, w - tw_u)

    def _outline(b, color):
        """
        分割轮廓：细虚线画在框内侧，框负责标位置和归属，轮廓看贴合度。
        poly 是环的列表——目标被遮挡时 mask 会断成几块，每块都得画出来，
        只画最大的那块看着像模型只分割出了一部分。
        """
        rings = b.get("poly")
        if not rings:
            return
        for pts in rings:
            if not pts or len(pts) < 3:
                continue
            try:
                arr = np.asarray(pts, dtype=float) * sc
            except (TypeError, ValueError):
                continue
            if arr.ndim != 2 or arr.shape[1] != 2:
                continue
            ax.add_patch(MplPolygon(arr, closed=True, fill=False,
                                    edgecolor=color, linewidth=1.1,
                                    linestyle=":", zorder=2.5))

    def _draw(boxes, color, lw, style, label):
        for b in boxes:
            xy = b.get("box") or []
            if len(xy) != 4:
                continue
            x1, y1 = xy[0] * sc, xy[1] * sc
            bw, bh = (xy[2] - xy[0]) * sc, (xy[3] - xy[1]) * sc
            if bw <= 0 or bh <= 0:
                continue
            ax.add_patch(Rectangle(
                (x1, y1), bw, bh, fill=False, edgecolor=color,
                linewidth=lw, linestyle=style, zorder=3))
            _outline(b, color)
            if label:
                cn = b.get("cls", "")
                conf = b.get("conf")
                if conf is not None:
                    txt = "{} {:.2f}".format(cn, conf)
                else:
                    txt = str(cn)
                ax.text(_label_x(x1, txt), max(y1, 0) + 9, txt, fontsize=6,
                        color="white",
                        bbox={"facecolor": color, "edgecolor": "none",
                              "pad": 1.2}, zorder=4)

    _draw(row.get("hits") or [], C_HIT, 1.0, "-", False)
    _draw(miss_boxes, C_MISSING, 2.2, "-", True)
    _draw(spur_boxes, C_SPURIOUS, 2.2, "--", True)
    # 认错的两个框位置基本重合,只画 GT 框, 标签里写明 GT → 预测
    for p in pairs:
        mb = p["gt"].get("box") or []
        if len(mb) != 4:
            continue
        x1, y1 = mb[0] * sc, mb[1] * sc
        bw, bh = (mb[2] - mb[0]) * sc, (mb[3] - mb[1]) * sc
        if bw <= 0 or bh <= 0:
            continue
        ax.add_patch(Rectangle((x1, y1), bw, bh, fill=False,
                               edgecolor=C_CONFUSE, linewidth=2.6, zorder=5))
        _outline(p["gt"], C_CONFUSE)
        full = "类别认错：{} → {}".format(p["gt"].get("cls", ""),
                                       p["pred"].get("cls", ""))
        # 框比标签还窄时退化成短文案,靠紫色和图例区分
        if len(full) * char_px > bw * px_per_unit:
            full = "{} → {}".format(p["gt"].get("cls", ""),
                                    p["pred"].get("cls", ""))
        ax.text(_label_x(x1, full), max(y1, 0) + 9, full, fontsize=6,
                color="white",
                bbox={"facecolor": C_CONFUSE, "edgecolor": "none", "pad": 1.2},
                zorder=6)

    foot = _err_foot(n_miss, n_spur, n_conf)
    color = C_MISSING if n_miss else (C_CONFUSE if n_conf else C_SPURIOUS)
    ax.set_title(base + "   " + foot, fontsize=8,
                 color=color, loc="left")


# ----------------------- 首页: 位图 PIL 自渲染 -------------------------

def _sample_note(stat):
    if not stat:
        return "", "#888888"
    total = stat.get("total", 0)
    shown = stat.get("shown", 0)
    mt, st = stat.get("miss_total", 0), stat.get("spur_total", 0)
    limit = stat.get("limit", 0)
    if limit and shown < total:
        return ("明细抽样：共 {} 张有问题（漏检 {} / 误检 {}），本报告抽取 {} 张"
                "——每个类别每种错误最多 {} 张，按错误数从多到少取"
                .format(total, mt, st, shown, limit)), "#8a5a00"
    return ("明细：共 {} 张有问题（漏检 {} / 误检 {}），已全部列出"
            .format(total, mt, st)), "#888888"


def _short(text, n):
    text = str(text)
    return text if len(text) <= n else text[:n - 1] + "…"


def _render_label_chart_png(counts, colors, out_png, width_px, height_px):
    """
    各类别标注数量柱状图，样式对齐统计界面（共用 app/charts 实现）。
    白底：报告是打印/归档用的，深色底那一套在纸上糊成一团。
    """
    if not counts:
        return False
    from app.widgets.charts import render_label_chart
    fig = render_label_chart(
        counts, label_colors=colors, dark=False,
        figsize=(width_px / float(_DPI), height_px / float(_DPI)))
    # 留出 x 轴标签旋转空间，防底部文字被裁
    fig.subplots_adjust(left=0.085, right=0.985, top=0.9, bottom=0.34)
    fig.savefig(out_png, dpi=_DPI, facecolor="white")
    plt.close(fig)
    return True


def _legend_items(stat):
    items = [(C_MISSING, "solid", "漏检 GT：有标注但模型没检出"),
             (C_SPURIOUS, "dash", "误检预测：模型检出但标注里没有"),
             (C_HIT, "solid", "正确检出（仅作位置参照）")]
    if stat and stat.get("conf_total"):
        items.insert(2, (C_CONFUSE, "solid",
                         "类别认错：位置对但判错类别（GT → 预测）"))
    if stat and stat.get("has_poly"):
        items.append((C_MISSING, "dot",
                      "虚线轮廓：分割 mask / 标注多边形（判定按外接框 IoU）"))
    return items


def _render_summary_png(summary, out_png, stat, chart_png=None):
    """
    stat 里的张数一律是全量，抽样情况单独用一行说明，
    免得总览表看起来像只测了抽出来的这几张。
    """
    dpi = _DPI
    W, H = _PAGE_W, _PAGE_H
    M = _MARGIN
    content_w = _CONTENT_W
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    fpath = _pick_image_font()

    def font(sz):
        return ImageFont.truetype(fpath, sz) if fpath else ImageFont.load_default()

    f_title = font(34)
    f_meta = font(14)
    f_sec = font(19)
    f_h = font(15)
    f_b = font(14)
    f_lbl = font(13)

    def tw(txt, f):
        bb = d.textbbox((0, 0), txt, font=f)
        return bb[2] - bb[0]

    def put(x0, y0, w, h, txt, f, fill="black", align="center"):
        bb = d.textbbox((0, 0), txt, font=f)
        ty = y0 + (h - (bb[3] - bb[1])) / 2.0 - bb[1]
        if align == "center":
            tx = x0 + (w - (bb[2] - bb[0])) / 2.0 - bb[0]
        else:
            tx = x0 + 8
        d.text((tx, ty), txt, fill=fill, font=f)

    def clip(txt, f, maxw):
        if tw(txt, f) <= maxw:
            return txt
        s = txt
        while len(s) > 1 and tw(s + "…", f) > maxw:
            s = s[:-1]
        return s + "…"

    def table(y0, head, data, weights, rh):
        """返回表格底边 y。列宽按权重分摊 content_w，不写死宽度才能不出血。"""
        total_w = float(sum(weights))
        cols = [content_w * w / total_w for w in weights]
        xs = []
        x = M
        for c in cols:
            xs.append(x)
            x += c

        def frame(yy, fill=None):
            d.rectangle([M, yy, M + content_w, yy + rh],
                        fill=fill, outline="#bbbbbb")

        frame(y0, "#eef1f5")
        for j, h in enumerate(head):
            put(xs[j], y0, cols[j], rh, h, f_h)
        for i, row in enumerate(data):
            yy = y0 + (i + 1) * rh
            frame(yy)
            for j, v in enumerate(row):
                put(xs[j], yy, cols[j], rh, clip(str(v), f_lbl, cols[j] - 12),
                    f_lbl, "#333333" if j == 0 else "black",
                    "left" if j == 0 else "center")
        return y0 + (len(data) + 1) * rh

    y = int(0.34 * dpi)
    d.text((M, y), "模型评估报告", fill="black", font=f_title)
    y += int(0.46 * dpi)

    d.text((M, y), "当前训练模型", fill="black", font=f_sec)
    y += int(0.30 * dpi)
    d.text((M, y), clip(str(summary.get("model") or "(未记录)"), f_b,
                        content_w), fill="#1f1f1f", font=f_b)
    y += int(0.26 * dpi)
    ds_txt = "、".join("{}/{}".format(x.get("project", ""), x.get("dataset", ""))
                      for x in (summary.get("datasets") or []))
    sub = ["数据集 " + (ds_txt or "(未记录)")]
    if summary.get("conf") is not None:
        sub.append("置信度 {}".format(summary["conf"]))
    if summary.get("iou") is not None:
        sub.append("IoU {}".format(summary["iou"]))
    d.text((M, y), clip("  ·  ".join(sub), f_meta, content_w),
           fill="#666666", font=f_meta)
    y += int(0.32 * dpi)

    if chart_png and os.path.exists(chart_png):
        with Image.open(chart_png) as chart:
            chart = chart.convert("RGB")
            img.paste(chart, (M, y))
            y += chart.size[1]
        y += int(0.20 * dpi)

    total = summary.get("total", 0)
    tp, fp, fn = summary.get("TP", 0), summary.get("FP", 0), summary.get("FN", 0)
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rows = [
        ["测试张数", "{} 张".format(total)],
        ["有问题的图片", "{} 张".format(stat.get("total", 0) if stat else 0)],
        ["检出率 (Recall)", "{:.1f}%".format(rec * 100)],
        ["准确率 (Precision)", "{:.1f}%".format(prec * 100)],
        ["正确检出", "{} 个".format(tp)],
        ["漏检 (该抓没抓)", "{} 个 / {} 张图".format(
            fn, stat.get("miss_total", 0) if stat else 0)],
        ["误检 (过杀)", "{} 个 / {} 张图".format(
            fp, stat.get("spur_total", 0) if stat else 0)],
    ]
    if stat and stat.get("conf_total"):
        rows.append(["类别认错 (位置对、类别错)",
                     "{} 个 / {} 张图".format(stat["conf_total"],
                                            stat.get("conf_imgs", 0))])
    y = table(y, ["指标", "值"], rows, [1.5, 1.0], int(0.33 * dpi))
    y += int(0.30 * dpi)

    note, note_color = _sample_note(stat)
    if note:
        d.text((M, y), note, fill=note_color, font=f_meta)
        y += int(0.34 * dpi)

    per_class = summary.get("per_class") or {}
    if per_class:
        d.text((M, y), "按类别", fill="black", font=f_sec)
        y += int(0.34 * dpi)
        head = ["类别", "标注", "正确", "漏检", "误检", "检出率", "准确率"]
        weights = [1.4, 0.6, 0.6, 0.6, 0.6, 0.9, 0.9]
        rh2 = int(0.32 * dpi)
        # 图例两列排布，条数会随认错/轮廓两条增减，行数得跟着算才不会出血
        legend_rows = (len(_legend_items(stat)) + 1) // 2
        legend_h = legend_rows * int(0.36 * dpi) + int(0.34 * dpi)
        room = H - int(0.46 * dpi) - legend_h - int(0.34 * dpi) - y
        max_rows = max(1, int(room // rh2) - 1)

        def stats(kv):
            cls, dd = kv
            tpv = dd.get("tp", 0)
            fnv = dd.get("fn", 0)
            fpv = dd.get("fp", 0)
            return (tpv, fnv, fpv,
                    "{:.1f}%".format(tpv / (tpv + fnv) * 100
                                     if (tpv + fnv) else 0),
                    "{:.1f}%".format(tpv / (tpv + fpv) * 100
                                     if (tpv + fpv) else 0))

        cs = sorted(per_class.items(),
                    key=lambda kv: (-(kv[1].get("fn", 0) + kv[1].get("fp", 0)),
                                    str(kv[0])))
        shown, hidden = cs[:max_rows], cs[max_rows:]
        data = []
        for cls, dd in shown:
            tpv, fnv, fpv, rs, ps = stats((cls, dd))
            data.append([str(cls), dd.get("gt", 0), tpv, fnv, fpv, rs, ps])
        if hidden:
            data.append(["… 另有 {} 类未列出".format(len(hidden)),
                         "", "", "", "", "", ""])
        y = table(y, head, data, weights, rh2)
        y += int(0.40 * dpi)

    legend = _legend_items(stat)
    sw_w, sw_h = int(0.55 * dpi), int(0.18 * dpi)
    col_w = content_w / 2.0
    for i, (color, style, label) in enumerate(legend):
        cx = M + (i % 2) * col_w
        cy = y + (i // 2) * int(0.36 * dpi)
        box = [cx, cy, cx + sw_w, cy + sw_h]
        if style == "dash":
            _dash_rect(d, box, color, 3)
        elif style == "dot":
            _dash_rect(d, box, color, 2, dash=3, gap=4)
        else:
            d.rectangle(box, outline=color, width=3)
        d.text((cx + sw_w + 12, cy + 2),
               clip(label, f_meta, col_w - sw_w - 16),
               fill="black", font=f_meta)
    y += ((len(legend) + 1) // 2) * int(0.36 * dpi)

    d.text((M, y), "错误样本明细（仅列漏检 / 误检图片，正确检出不列出）",
           fill="#888888", font=f_meta)

    img.save(out_png, "PNG", dpi=(dpi, dpi))


def _dash_rect(d, box, color, width=3, dash=9, gap=6):
    """PIL 没有虚线矩形，手动分段画，线型对齐缩略图页的 '--'。"""
    x0, y0, x1, y1 = box
    x = x0
    while x < x1:
        xe = min(x + dash, x1)
        d.line([(x, y0), (xe, y0)], fill=color, width=width)
        d.line([(x, y1), (xe, y1)], fill=color, width=width)
        x += dash + gap
    y = y0
    while y < y1:
        ye = min(y + dash, y1)
        d.line([(x0, y), (x0, ye)], fill=color, width=width)
        d.line([(x1, y), (x1, ye)], fill=color, width=width)
        y += dash + gap


def _advice_items(res, stat=None):
    """
    改进建议
    """
    pc = {str(k): (v or {}) for k, v in (res.get("per_class") or {}).items()}
    tp, fp, fn = res.get("TP", 0), res.get("FP", 0), res.get("FN", 0)
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    parts = [[("本轮检出率 {:.0f}%、准确率 {:.0f}%。".format(
        rec * 100, prec * 100), False)]]
    if not pc:
        parts.append([("没有逐类别统计，无法定位到具体标签，"
                       "请先确认标签文件能正常读到。", False)])
        return [s for p in parts for s in p]

    gts = {c: int(d.get("gt", 0)) for c, d in pc.items()}
    avg = sum(gts.values()) / float(len(gts)) if gts else 0.0
    hot_fn = sorted(((c, int(d.get("fn", 0))) for c, d in pc.items()
                     if d.get("fn", 0)), key=lambda x: -x[1])[:2]
    hot_fp = sorted(((c, int(d.get("fp", 0))) for c, d in pc.items()
                     if d.get("fp", 0)), key=lambda x: -x[1])[:2]

    def names(pairs):
        out = []
        for i, (c, _) in enumerate(pairs):
            if i:
                out.append(("、", False))
            out.append(("「{}」".format(c), True))
        return out

    all_fn = len(hot_fn) >= len(gts) and len(gts) > 1
    all_fp = len(hot_fp) >= len(gts) and len(gts) > 1
    if hot_fn:
        parts.append([("漏检" + ("分布在" if all_fn else "集中在"), False)] +
                     names(hot_fn) +
                     [("（共 {} 个），优先补这几类的姿态、光照样本，"
                       "并复核标注是否有遗漏。".format(
                           sum(v for _, v in hot_fn)), False)])
    if hot_fp:
        parts.append([("误检" + ("分布在" if all_fp else "以"), False)] +
                     names(hot_fp) +
                     [("（{} 个）{}属过杀，建议补无缺陷负样本、"
                       "清理标注噪声。".format(sum(v for _, v in hot_fp),
                                            "，" if all_fp else "为主，"),
                       False)])
    n_conf = int((stat or {}).get("conf_total", 0))
    if n_conf:
        parts.append([("此外 {} 处".format(n_conf), False),
                      ("位置对但类别判错", False),
                      ("（报告紫框），属分类能力不足而非定位问题，"
                       "需补易混淆类别之间的区分性样本。", False)])
    worst_cls, worst_gt = min(gts.items(), key=lambda kv: kv[1])
    if (hot_fn or hot_fp) and worst_gt < max(100, avg * 0.4):
        parts.append([("其中", False), ("「{}」".format(worst_cls), True),
                      ("仅 {} 个标注，样本不足是主要瓶颈，建议补到 "
                       "200 个以上。".format(worst_gt), False)])
    if len(gts) > 1 and max(gts.values()) > 5 * max(1, min(gts.values())):
        parts.append([("各类样本量差距大（最多 {} / 最少 {}），"
                       "训练时建议做类别均衡采样。".format(
                           max(gts.values()), min(gts.values())), False)])
    if hot_fn or hot_fp:
        parts.append([("把本报告中的漏检、误检图加入训练集复训，"
                       "再用同参数复测对比。", False)])
    else:
        parts.append([("本轮无漏检、无误检，建议用更严的阈值或更难的样本"
                       "再压一轮，确认稳定性。", False)])

    out, used = [], 0
    for seg in parts:
        n = sum(len(t) for t, _ in seg) + 1      # +1 是段间换行, 也算 1 字
        if out and used + n > 200:
            break
        out.extend(seg)
        out.append(("\n", False))
        used += n
    if out and out[-1][0] == "\n":
        out.pop()
    return out


def _char_w(d, ch, font):
    try:
        return d.textlength(ch, font=font)
    except AttributeError:
        return d.textbbox((0, 0), ch, font=font)[2]


def _render_advice_png(items, out_png, page_no, model=""):
    dpi = _DPI
    img = Image.new("RGB", (_PAGE_W, _PAGE_H), "white")
    d = ImageDraw.Draw(img)
    fpath = _pick_image_font()

    def font(sz):
        return ImageFont.truetype(fpath, sz) if fpath else \
            ImageFont.load_default()

    f_title = font(34)
    f_lead = font(18)
    f_body = font(28)
    f_meta = font(14)
    M, content_w = _MARGIN, _CONTENT_W

    y = int(0.55 * dpi)
    d.text((M, y), "改进建议", fill="black", font=f_title)
    y += int(0.52 * dpi)
    d.line([(M, y), (M + content_w, y)], fill="#d8d8d8", width=2)
    y += int(0.34 * dpi)
    lead = "基于本次测试的指标与按类别表现"
    if model:
        lead += "（模型：{}）".format(_short(model, 28))
    d.text((M, y), lead + "，建议如下：", fill="#666666", font=f_lead)
    y += int(0.40 * dpi)

    line_h = int(0.34 * dpi)
    x0 = M
    x, yy = x0, y
    for text, is_label in items:
        for ch in text:
            if ch == "\n":
                x, yy = x0, yy + line_h + int(0.10 * dpi)
                continue
            w = _char_w(d, ch, f_body)
            if x + w > x0 + content_w:
                x, yy = x0, yy + line_h
            d.text((x, yy), ch, font=f_body,
                   fill=C_MISSING if is_label else "#202020")
            x += w
    y = yy + line_h

    foot_y = _PAGE_H - int(0.62 * dpi)
    d.line([(M, foot_y - int(0.18 * dpi)),
            (M + content_w, foot_y - int(0.18 * dpi))],
           fill="#e4e4e4", width=1)
    d.text((M, foot_y), "标红的标签是需要重点关注的类别。",
           fill="#888888", font=f_meta)
    page_txt = "第 {} 页".format(page_no)
    d.text((M + content_w - d.textbbox((0, 0), page_txt, font=f_meta)[2],
            foot_y), page_txt, fill="#777777", font=f_meta)

    img.save(out_png, "PNG", dpi=(dpi, dpi))


def _embed_image_page(pdf, png_path):
    arr = np.array(Image.open(png_path).convert("RGB"))
    H, W = arr.shape[:2]
    fig = plt.figure(figsize=(_A4_W_IN, _A4_H_IN))
    gs = fig.add_gridspec(1, 1, left=0, right=1, bottom=0, top=1)
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(arr)
    ax.set_xlim(0, W); ax.set_ylim(H, 0)
    ax.set_xticks([]); ax.set_yticks([])
    pdf.savefig(fig, dpi=200)
    plt.close(fig)


def _page_gallery(pdf, rows, title, thumb_w, page_no,
                  confuse_iou=CONFUSE_IOU):
    fig = plt.figure(figsize=(_A4_W_IN, _A4_H_IN))
    fig.text(0.04, 0.955, title, fontsize=14, fontweight="bold")
    fig.text(0.96, 0.955, "第 {} 页".format(page_no),
             fontsize=9, ha="right", color="#777777")
    gs = fig.add_gridspec(_GRID_ROWS, _GRID_COLS,
                          left=0.04, right=0.96, top=0.92, bottom=0.04,
                          hspace=0.32, wspace=0.10)
    for i, row in enumerate(rows[:_GRID_COLS * _GRID_ROWS]):
        r, c = i // _GRID_COLS, i % _GRID_COLS
        ax = fig.add_subplot(gs[r, c])
        _cell(ax, row, thumb_w, confuse_iou)
    pdf.savefig(fig)
    plt.close(fig)


def build_report(res, out_pdf=None, thumb_w=480, summary_png=None,
                 per_class_limit=PER_CLASS_LIMIT):
    """
    生成 PDF。res 需含 detail_path；返回 pdf 路径，无明细时返回空串。
    per_class_limit 每个「类别 × 错误类型」最多列几张，0/None 表示全列。
    抽样只发生在出报告这一步，details.jsonl 里仍是全量，后续做难例挖掘不丢数据。
    标注分布优先用 res["label_stats"]（统计界面那一套，带标签颜色），
    取不到就退回 per_class 的 gt，反正都是这次真正测到的标注数。
    """
    detail_path = res.get("detail_path") or ""
    rows = load_details(detail_path)
    if not rows:
        return ""

    if out_pdf is None:
        out_dir = res.get("report_dir") or os.path.dirname(detail_path)
        out_pdf = os.path.join(out_dir, "report.pdf")
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
    out_dir = os.path.dirname(out_pdf)
    if summary_png is None:
        summary_png = os.path.join(out_dir, "summary.png")
    advice_png = os.path.join(out_dir, "advice.png")
    chart_png = os.path.join(out_dir, "label_chart.png")

    _setup_font()
    try:
        confuse_iou = float(res.get("iou") or CONFUSE_IOU)
    except (TypeError, ValueError):
        confuse_iou = CONFUSE_IOU
    conf_stat = None
    if res.get("conf_total") is not None:
        conf_stat = {"total": res["conf_total"],
                     "imgs": res.get("conf_imgs") or 0}
    miss_rows, spur_rows, stat = _sample_rows(rows, per_class_limit,
                                              confuse_iou, conf_stat)
    stat["has_poly"] = _any_poly(rows)

    counts = res.get("label_stats")
    if not counts:
        counts = {str(c): int((d or {}).get("gt", 0))
                  for c, d in (res.get("per_class") or {}).items()
                  if int((d or {}).get("gt", 0)) > 0}
    if not _render_label_chart_png(counts, res.get("label_colors"),
                                   chart_png, _CONTENT_W, _CHART_H):
        chart_png = None
    _render_summary_png(res, summary_png, stat, chart_png)

    def title_of(kind, shown, total):
        if shown < total:
            return "{}（抽取 {} / 共 {} 张）".format(kind, shown, total)
        return "{}（共 {} 张）".format(kind, total)

    miss_title = title_of("漏检样本：有标注但模型没检出",
                          len(miss_rows), stat["miss_total"])
    spur_title = title_of("误检样本：模型检出但标注里没有",
                          len(spur_rows), stat["spur_total"])

    with PdfPages(out_pdf) as pdf:
        _embed_image_page(pdf, summary_png)
        page = 1
        for start in range(0, len(miss_rows), _GRID_COLS * _GRID_ROWS):
            _page_gallery(pdf, miss_rows[start:start + _GRID_COLS * _GRID_ROWS],
                          miss_title, thumb_w, page, confuse_iou)
            page += 1
        for start in range(0, len(spur_rows), _GRID_COLS * _GRID_ROWS):
            _page_gallery(pdf, spur_rows[start:start + _GRID_COLS * _GRID_ROWS],
                          spur_title, thumb_w, page, confuse_iou)
            page += 1
        _render_advice_png(_advice_items(res, stat), advice_png, page,
                           str(res.get("model") or ""))
        _embed_image_page(pdf, advice_png)
        d = pdf.infodict()
        d["Title"] = "模型评估报告"
    return out_pdf
