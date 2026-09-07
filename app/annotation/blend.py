# -*- coding: utf-8 -*-
"""
粘贴融合: Lab 亮度补偿 + 边缘羽化。
"""
import numpy as np

_D65 = (0.95047, 1.0, 1.08883)
CONTRAST_MATCH = 0.25  # 对比度跟随比例: 1=完全跟背景(会把缺陷本身的明暗幅度改掉)
RING_PX = 12           # 接缝外圈宽度: 背景统计取这一圈, 而不是被覆盖的那一块
RING_STEP = 4          # 外圈统计的降采样步长(只取均值/方差, 不需要全分辨率)


def _f(t):
    return np.where(t > 0.008856, np.cbrt(t), 7.787 * t + 16.0 / 116.0)


def _f_inv(t):
    return np.where(t > 0.206893, t ** 3, (t - 16.0 / 116.0) / 7.787)


def bgr_to_lab(bgr):
    rgb = bgr[..., ::-1].astype(np.float32) / 255.0
    rgb = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / _D65[0]
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / _D65[1]
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / _D65[2]
    fx, fy, fz = _f(x), _f(y), _f(z)
    return np.stack([116.0 * fy - 16.0,
                     500.0 * (fx - fy),
                     200.0 * (fy - fz)], axis=-1)


def lab_to_bgr(lab):
    fy = (lab[..., 0] + 16.0) / 116.0
    fx = fy + lab[..., 1] / 500.0
    fz = fy - lab[..., 2] / 200.0
    x, y, z = _f_inv(fx) * _D65[0], _f_inv(fy) * _D65[1], _f_inv(fz) * _D65[2]
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    b = 0.0557 * x - 0.2040 * y + 1.0570 * z
    lin = np.clip(np.stack([r, g, b], axis=-1), 0.0, 1.0)
    srgb = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1.0 / 2.4) - 0.055)
    return np.clip(srgb[..., ::-1] * 255.0 + 0.5, 0, 255).astype(np.uint8)


def _erode(m):
    out = m.copy()
    out[1:, :] &= m[:-1, :]
    out[:-1, :] &= m[1:, :]
    out[:, 1:] &= m[:, :-1]
    out[:, :-1] &= m[:, 1:]
    return out


def _dilate(m, n):
    out = m
    for _ in range(n):
        out = ~_erode(~out)
    return out


def _inner_distance(mask, max_d):
    """到背景的近似内距离(最外圈=1, 向内+1, 封顶 max_d), 比高斯便宜且不外扩。"""
    dist = np.zeros(mask.shape, np.float32)
    cur = mask
    for _ in range(max_d):
        dist += cur
        cur = _erode(cur)
    return dist


def blend_patch(dst_bgr, src_bgra, strength=0.7, feather_px=None):
    """
    带 alpha 的 src(BGRA) 融到 dst(BGR), 返回合成 BGR。
    strength: 0=硬贴, 1=亮度完全对齐背景; feather_px 默认随 strength 取 0~6px。
    """
    alpha = src_bgra[..., 3].astype(np.float32) / 255.0
    if alpha.max() <= 0.0:
        return dst_bgr
    if feather_px is None:
        feather_px = 6.0 * min(1.0, max(0.0, strength))
    feather = int(round(feather_px))
    m = alpha > 0.5
    if feather > 0 and m.any():
        # 只在内侧渐变: 内部恒为 1, 缺陷边缘不会被背景冲淡, 也不会糊到轮廓外
        ys, xs = np.nonzero(m)
        y0 = max(0, int(ys.min()) - feather)
        y1 = min(alpha.shape[0], int(ys.max()) + feather + 1)
        x0 = max(0, int(xs.min()) - feather)
        x1 = min(alpha.shape[1], int(xs.max()) + feather + 1)
        d = _inner_distance(m[y0:y1, x0:x1], feather)
        alpha[y0:y1, x0:x1] = np.minimum(alpha[y0:y1, x0:x1],
                                         np.clip(d / feather, 0.0, 1.0))
    src_bgr = src_bgra[..., :3]
    strength = min(1.0, max(0.0, strength))
    core = alpha > 0.6
    inside = alpha > 0.0
    if strength > 0.0 and core.any():
        # 保真优先: 只补 L 不动色度, 缺陷自身纹理要原样保留
        src_lab = bgr_to_lab(src_bgr[inside])
        s = src_lab[:, 0]
        s_mean = float(s.mean())
        core_s = core[::RING_STEP, ::RING_STEP]
        ref_s = _dilate(core_s, max(1, RING_PX // RING_STEP)) & ~core_s
        if ref_s.sum() < 50:
            ref_s = core_s
        d_s = bgr_to_lab(dst_bgr[::RING_STEP, ::RING_STEP][ref_s])[:, 0]
        offset = (float(d_s.mean()) - s_mean) * strength
        # 对比度只跟一部分: 全跟会改变缺陷自身的明暗幅度
        ratio = (float(d_s.std()) / max(float(s.std()), 1e-3)) ** (
            CONTRAST_MATCH * strength)
        # 护栏: 缺陷明暗幅度最多改 30%
        ratio = min(1.3, max(0.8, ratio))
        src_lab[:, 0] = np.clip((s - s_mean) * ratio + s_mean + offset,
                                0.0, 100.0)
        src_bgr = src_bgr.copy()
        src_bgr[inside] = lab_to_bgr(src_lab)
    a = alpha[..., None]
    out = dst_bgr.astype(np.float32) * (1.0 - a) + src_bgr.astype(np.float32) * a
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)
