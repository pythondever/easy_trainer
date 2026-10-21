# -*- coding: utf-8 -*-
"""标注场景-粘贴区域模板 mixin: 圈定"缺陷可以贴在哪里".

区域不是标注, 不进 labelme json(原 scene.py 节注释原话). 机械拆分,
方法体一字未改. 宿主提供 image_item/_region_points/paste_regions/
draw_mode/addItem/removeItem 等.
"""
from app.annotation.paste_regions import PasteRegionItem, regions_payload


class PasteRegionMixin:
    def set_template_mode(self, on):
        """区域模板模式: 这一模式下画出来的多边形进模板层, 不成标注."""
        on = bool(on)
        if self.template_mode == on:
            return
        self.template_mode = on
        self._cancel_polygon()      # 切模式时丢掉画到一半的中间态

    def add_paste_region(self, points):
        """记一个粘贴区域. 只存点, item 交给 _rebuild_paste_region_items 统一建."""
        if len(points) < 3:
            return None
        self._region_points.append([[float(x), float(y)] for x, y in points])
        self._rebuild_paste_region_items()
        return self.paste_regions[-1] if self.paste_regions else None

    def remove_paste_region(self, item):
        try:
            idx = self.paste_regions.index(item)
        except ValueError:
            return False
        self._region_points.pop(idx)
        self._rebuild_paste_region_items()
        return True

    def clear_paste_regions(self):
        if not self._region_points:
            return False
        self._region_points = []
        self._rebuild_paste_region_items()
        return True

    def set_paste_regions(self, points_list):
        """整体替换区域(载入模板/导出后回填都用它)."""
        self._region_points = [[[float(x), float(y)] for x, y in p]
                               for p in (points_list or []) if len(p) >= 3]
        self._rebuild_paste_region_items()

    def paste_region_payload(self):
        """区域 -> 可存盘 dict. 参考尺寸取当前图, 因为区域就是在当前图上画的."""
        size = (0, 0)
        if self.image_rect is not None:
            size = (int(self.image_rect.width()), int(self.image_rect.height()))
        return regions_payload(self.paste_regions, size)

    def paste_region_at(self, scene_pos):
        """场景坐标落在哪个区域上. 倒序遍历: 后画的压在上面."""
        for it in reversed(self.paste_regions):
            try:
                if it.shape().contains(it.mapFromScene(scene_pos)):
                    return it
            except RuntimeError:
                continue
        return None

    def refresh_paste_region_selectability(self):
        """把"能不能点选"同步给所有区域 item."""
        for it in self.paste_regions:
            try:
                it.set_selectable(not self.draw_mode)
            except RuntimeError:
                pass

    def _finish_region_drag(self):
        """松手才把新顶点写回 _region_points: 拖动中途重建 item 会把正拖的手柄换掉."""
        drag = self._region_drag
        self._region_drag = None
        if drag is None:
            return
        try:
            idx = self.paste_regions.index(drag[0])
        except ValueError:
            return
        self._region_points[idx] = drag[0].region_points()

    def _rebuild_paste_region_items(self):
        """按 _region_points 重建 item: 序号取自下标, 删一个不必手工重编号."""
        self._region_drag = None      # 旧 item 即将作废, 拖动态一并丢掉
        for it in self.paste_regions:
            # set_image 里的 clear() 已经把 item 的 C++ 对象删了, 这时只剩 Python 壳,
            # 拿它调 removeItem 会 RuntimeError(与 _dispose_item 同一处防御)
            try:
                if it.scene() is self:
                    self.removeItem(it)
            except RuntimeError:
                pass
        self.paste_regions = []
        if self.image_item is None:
            return
        for i, pts in enumerate(self._region_points, 1):
            item = PasteRegionItem(pts, i)
            self.addItem(item)
            self.paste_regions.append(item)
        self.refresh_paste_region_selectability()
