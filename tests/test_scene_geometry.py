# -*- coding: utf-8 -*-
"""scene_geometry 纯函数测试: 不需要 Qt(rotate_points 的 center 用轻量替身)."""
import math

import pytest

from app.annotation.scene_geometry import (resample_track, rdp,
                                           rotate_points, simplify_track)


class Center:
    """QPointF 的轻量替身: rotate_points 只用到 .x()/.y() 协议."""

    def __init__(self, x, y):
        self._x, self._y = x, y

    def x(self):
        return self._x

    def y(self):
        return self._y


class TestResampleTrack:
    def test_点数不超上限原样返回(self):
        pts = [[0, 0], [1, 1], [2, 2]]
        assert resample_track(pts) is pts

    def test_超过上限抽稀到指定数(self):
        pts = [[i, i] for i in range(100)]
        out = resample_track(pts, max_pts=32)
        assert len(out) == 32

    def test_首尾必保(self):
        pts = [[i, i * 2] for i in range(50)]
        out = resample_track(pts, max_pts=10)
        assert out[0] == pts[0]
        assert out[-1] == pts[-1]

    def test_均匀采样落在原始点上(self):
        pts = [[i, 0] for i in range(10)]
        out = resample_track(pts, max_pts=5)
        # step = 9/4 = 2.25, 采样下标 0,2,4,7,9(round(4.5) 银行家舍入得 4)
        assert out == [pts[0], pts[2], pts[4], pts[7], pts[9]]

    def test_少于三个点不炸(self):
        assert resample_track([]) == []
        assert resample_track([[1, 2]]) == [[1, 2]]


class TestRdp:
    def test_少于三点原样拷贝(self):
        pts = [[0, 0], [3, 4]]
        out = rdp(pts, 1.0)
        assert out == pts
        assert out is not pts

    def test_共线点压成两端(self):
        pts = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
        assert rdp(pts, 0.5) == [[0, 0], [4, 0]]

    def test_尖峰偏离超阈值被保留(self):
        pts = [[0, 0], [2, 5], [4, 0]]
        out = rdp(pts, 0.5)
        assert len(out) == 3
        assert [2, 5] in out

    def test_偏离不够大可丢(self):
        pts = [[0, 0], [2, 0.1], [4, 0]]
        assert rdp(pts, 1.0) == [[0, 0], [4, 0]]

    def test_首尾重合时按到端点距离算(self):
        # p1==p2 那条分支: 所有点重合, 最大距离 0, 压成两点
        pts = [[1, 1], [1, 1], [1, 1]]
        assert rdp(pts, 0.5) == [[1, 1], [1, 1]]

    def test_大折线保形(self):
        pts = [[0, 0], [1, 10], [2, 0], [3, 10], [4, 0]]
        out = rdp(pts, 0.5)
        assert out[0] == [0, 0] and out[-1] == [4, 0]
        assert len(out) >= 3  # 两个峰都不能丢


class TestSimplifyTrack:
    def test_间隔采样按min_gap过滤(self):
        pts = [[0, 0], [1, 0], [2, 0], [10, 0], [11, 0]]
        out = simplify_track(pts, min_gap=5.0)
        # 第2/3点与上一点间距<5被滤掉; [11,0]与[10,0]间距1也被滤
        assert out == [[0, 0], [10, 0]]

    def test_少于三点不过rdp(self):
        pts = [[0, 0], [10, 0]]
        assert simplify_track(pts, min_gap=5.0) == [[0, 0], [10, 0]]

    def test_密集共线轨迹抽稀成线(self):
        pts = [[float(i), 0.0] for i in range(30)]
        out = simplify_track(pts, min_gap=5.0)
        assert len(out) == 2  # 全共线, RDP 压成两端

    def test_不改入参(self):
        pts = [[float(i), float(i % 3)] for i in range(20)]
        snapshot = [list(p) for p in pts]
        simplify_track(pts, min_gap=2.0)
        assert pts == snapshot


class TestRotatePoints:
    def test_零度原样(self):
        pts = [[1.0, 2.0], [3.0, 4.0]]
        out = rotate_points(pts, Center(0, 0), 0)
        assert out == pts

    def test_90度顺时针_y向下屏幕坐标(self):
        # (1,0) 绕原点顺时针 90° 落到 (0,1)(与 QPainter.rotate 同向);
        # cos(90°) 在浮点下是 6e-17 而非 0, 只能近似断言
        out = rotate_points([[1.0, 0.0]], Center(0, 0), 90)
        assert out[0][0] == pytest.approx(0.0, abs=1e-9)
        assert out[0][1] == pytest.approx(1.0, abs=1e-9)

    def test_180度对调(self):
        out = rotate_points([[1.0, 0.0]], Center(0, 0), 180)
        assert out[0][0] == -1.0
        assert abs(out[0][1]) < 1e-9

    def test_绕非原点center(self):
        # 中心点自身不动
        out = rotate_points([[5.0, 5.0]], Center(5, 5), 37)
        assert out[0][0] == 5.0
        assert out[0][1] == 5.0

    def test_中心右侧点顺时针转90落到下方(self):
        # center=(10,10), 点=(13,10): 顺时针 90° 应到 (10,13)
        out = rotate_points([[13.0, 10.0]], Center(10, 10), 90)
        assert abs(out[0][0] - 10.0) < 1e-9
        assert abs(out[0][1] - 13.0) < 1e-9

    def test_旋转保持到中心距离(self):
        out = rotate_points([[3.0, 4.0]], Center(0, 0), 53)
        assert math.hypot(out[0][0], out[0][1]) == 5.0

    def test_不改入参(self):
        pts = [[1.0, 2.0], [3.0, 4.0]]
        rotate_points(pts, Center(0, 0), 45)
        assert pts == [[1.0, 2.0], [3.0, 4.0]]
