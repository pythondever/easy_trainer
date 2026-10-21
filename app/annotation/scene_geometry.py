# -*- coding: utf-8 -*-
"""
标注场景的纯几何计算: 无 Qt 依赖, 可直接单测(见 tests/test_scene_geometry.py).

两个语义不同的抽稀, 按用途分开命名:
- resample_track:  均匀采样抽稀(首尾必保), 供格式刷轨迹抠图用
- simplify_track:  间隔采样 + Douglas-Peucker, 供手绘多边形成图用
"""
import math


def resample_track(pts, max_pts=32):
    """轨迹点抽稀为均匀采样的多边形顶点(首尾必保), 避免顶点过多."""
    if len(pts) <= max_pts:
        return pts
    step = (len(pts) - 1) / (max_pts - 1)
    out = [pts[0]]
    i = 1
    while i < max_pts - 1:
        out.append(pts[int(round(i * step))])
        i += 1
    out.append(pts[-1])
    return out


def rdp(points, epsilon):
    """Douglas-Peucker 抽稀: 保形且顶点数合理."""
    if len(points) < 3:
        return list(points)
    p1, p2 = points[0], points[-1]
    x1, y1 = p1; x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dmax, idx = 0.0, 0
    for i in range(1, len(points) - 1):
        px, py = points[i]
        if abs(dx) < 1e-9 and abs(dy) < 1e-9:
            d = ((px-x1)**2 + (py-y1)**2) ** 0.5
        else:
            d = abs(dy*px - dx*py + x2*y1 - y2*x1) / (dx*dx + dy*dy) ** 0.5
        if d > dmax:
            dmax, idx = d, i
    if dmax > epsilon:
        left = rdp(points[:idx+1], epsilon)
        right = rdp(points[idx:], epsilon)
        return left[:-1] + right
    return [p1, p2]


def simplify_track(points, min_gap=5.0, max_angle=150.0):
    """轨迹抽稀: 间隔采样 + RDP 保形, 返回多边形顶点."""
    pts = []
    for p in points:
        if pts and (p[0]-pts[-1][0])**2 + (p[1]-pts[-1][1])**2 < min_gap**2:
            continue
        pts.append(p)
    if len(pts) < 3:
        return pts
    return rdp(pts, 0.8)


def rotate_points(pts, center, angle):
    """
    多边形点绕 center 旋转 angle 度. Qt 屏幕坐标 y 向下:
    正角度=视觉顺时针, 负角度=视觉逆时针(与 QPainter.rotate 方向一致).
    center 只需提供 .x()/.y()(QPointF 或同名轻量对象均可).
    """
    rad = math.radians(angle)
    c, s = math.cos(rad), math.sin(rad)
    cx, cy = center.x(), center.y()
    out = []
    for x, y in pts:
        dx, dy = x - cx, y - cy
        out.append([cx + dx * c - dy * s, cy + dx * s + dy * c])
    return out
