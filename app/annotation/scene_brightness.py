# -*- coding: utf-8 -*-
"""
标注场景-多边形亮度 mixin: 拖动只画预览层, 松手一次落盘.
"""
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem

from app.annotation.box_item import AnnotationPolygonItem
from app.annotation.image_buf import bgra_view

# 亮度基准按多边形各存一份(几万像素级的 ROI 要几十 MB), 只留最近调过的这几个
_BRIGHT_CACHE_MAX = 2


class BrightnessMixin:
    def fill_polygon(self, item, value):
        """把多边形区域内像素填成 value 颜色, value 可为 (r,g,b) 或单通道灰度, 入同一撤销栈供 Ctrl+Z 恢复."""
        # 亮度还没落盘的话先写进去, 下面取到的 pix 才是最终要填的像素
        self.drop_brightness()
        pix = self.image_item.pixmap() if self.image_item is not None else None
        poly = item.polygon() if item is not None else None
        if pix is None or poly is None or poly.isEmpty():
            return False
        if isinstance(value, (tuple, list)):
            r, g, b = (min(255, max(0, int(c))) for c in value)
        else:
            r = g = b = min(255, max(0, int(value)))
        box = poly.boundingRect()
        ox = max(0, int(box.x()))
        oy = max(0, int(box.y()))
        bw = min(int(box.right()) + 1, pix.width()) - ox
        bh = min(int(box.bottom()) + 1, pix.height()) - oy
        if bw <= 0 or bh <= 0:
            return False
        before = pix.copy(ox, oy, bw, bh)
        if before.isNull():
            return False
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addPolygon(poly)
        p.fillPath(path, QColor(r, g, b))
        p.end()
        self.image_item.setPixmap(pix)
        self.image_modified = True
        self.image_pixels_changed.emit()
        self._fp_undo_stack.append(
            {"before": before, "ox": ox, "oy": oy, "item": None})
        return True

    def _polygon_coverage(self, poly, ox, oy, w, h):
        """多边形内部 255, 边缘按抗锯齿取中间值, 外部 0; 亮度按它插值, 边界才不出硬边."""
        mask = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
        mask.fill(Qt.transparent)
        p = QPainter(mask)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(255, 255, 255))
        p.translate(-ox, -oy)
        p.drawPolygon(poly)
        p.end()
        # mask 是局部的, 必须 copy: 直接留视图会在 QImage 销毁后悬空
        return bgra_view(mask)[..., 3].copy()

    def set_polygon_brightness(self, item, value, commit=False):
        """
        0.5=原样, 1=两倍, 0=全黑; 只改多边形框内像素, 拖动过程不叠加.
        commit=False 只把结果画到预览层, 图像像素不动: 写一次图像就要整幅写时复制,
        拖动中每格都写的话光拷贝就把主线程占满, 所以留到松手时一次落地.
        """
        if not isinstance(item, AnnotationPolygonItem) or self.image_item is None \
                or self.image_rect is None:
            return False
        poly = item.mapToScene(item.polygon())
        if poly.count() < 3:
            return False
        box = poly.boundingRect()
        ox = max(0, int(box.left()))
        oy = max(0, int(box.top()))
        bw = min(int(box.right()) + 1, int(self.image_rect.width())) - ox
        bh = min(int(box.bottom()) + 1, int(self.image_rect.height())) - oy
        if bw <= 0 or bh <= 0:
            return False
        # 基准按多边形各存一份: 调完 A 去调 B 再回来调 A, 不会在已调亮的像素上再叠一层
        e = self._bright_cache.get(item)
        if (e is None or e["ox"] != ox or e["oy"] != oy
                or e["w"] != bw or e["h"] != bh):
            e = self._make_bright_base(item, poly, ox, oy, bw, bh)
            if e is None:
                return False
            self._bright_cache[item] = e
            while len(self._bright_cache) > _BRIGHT_CACHE_MAX:
                victim = next((k for k, v in self._bright_cache.items()
                               if not v["dirty"]), None)
                if victim is None:
                    break
                self._bright_cache.pop(victim)
        if e["value"] != value or e["layer"] is None:
            e["value"] = value
            self._render_bright(e, value)
            e["dirty"] = True
        if commit:
            self.commit_brightness()
        else:
            self._show_bright_preview(e)
        return True

    def _make_bright_base(self, item, poly, ox, oy, bw, bh):
        """
        固化亮度基准: 区域原像素 + 覆盖度.
        覆盖度铺成 3 通道是为了让重算走连续内存: 拿 (h,w,1) 广播乘同一批像素要慢
        一倍. 基准不随滑块变, 这笔内存和这一次彩色转换只付一次.
        """
        before = self.image_item.pixmap().copy(ox, oy, bw, bh)
        if before.isNull():
            return None
        base_q = before.toImage().convertToFormat(QImage.Format_ARGB32)
        covf = self._polygon_coverage(poly, ox, oy, bw, bh).astype(np.float32) / 255.0
        layer = QImage(bw, bh, QImage.Format_ARGB32)
        # 一次调节只入一条撤销: 每次拖动都从这份基准重算, 拖十下 Ctrl+Z 也是一步回原样
        self._fp_undo_stack.append(
            {"before": before, "ox": ox, "oy": oy, "item": None})
        return {"item": item, "ox": ox, "oy": oy, "w": bw, "h": bh,
                "base": bgra_view(base_q)[..., :3].astype(np.float32),
                "cov3": np.repeat(covf[..., None], 3, axis=2),
                "layer": layer, "lv": bgra_view(layer),
                "value": None, "dirty": False}

    def _render_bright(self, e, value):
        """按 value 重算 ROI: 与原来的 base*(1 + t*cov) 同一个运算顺序, 只是不再每格重取基准."""
        buf = self._bright_scratch(e["w"], e["h"])
        np.multiply(e["cov3"], value / 0.5 - 1.0, out=buf)
        np.add(buf, 1.0, out=buf)
        np.multiply(e["base"], buf, out=buf)
        np.clip(buf, 0, 255, out=buf)
        # 值已夹到 0~255, 这里只剩取整; 直接写进预览层的缓冲, 不额外拷一份
        np.copyto(e["lv"][..., :3], buf, casting="unsafe")
        e["lv"][..., 3] = 255

    def _bright_scratch(self, w, h):
        """乘加用的临时缓冲: 按 ROI 尺寸留一份, 相邻几格反复调时不必反复分配."""
        buf = self._bright_buf
        if buf is None or buf.shape[0] != h or buf.shape[1] != w:
            buf = np.empty((h, w, 3), np.float32)
            self._bright_buf = buf
        return buf

    def commit_brightness(self):
        """
        把预览层里的亮度结果写进图像像素, 返回是否有改动.
        待落盘的区域共用一份像素引用: 整批只触发一次整图写时复制.
        """
        if self.image_item is None:
            return False
        dirty = [e for e in self._bright_cache.values() if e["dirty"]]
        self._hide_bright_preview()
        if not dirty:
            return False
        pix = self.image_item.pixmap()
        for e in dirty:
            p = QPainter(pix)
            p.drawImage(e["ox"], e["oy"], e["layer"])
            p.end()
            e["dirty"] = False
        self.image_item.setPixmap(pix)
        self.image_modified = True
        return True

    def _ensure_bright_overlay(self):
        """亮度预览层: 夹在图像与标注框之间, 只显示还没落盘的调亮结果."""
        it = self._bright_overlay
        if it is not None:
            return it
        it = QGraphicsPixmapItem()
        it.setZValue(1)
        it.setAcceptedMouseButtons(Qt.NoButton)
        self.addItem(it)
        self._bright_overlay = it
        return it

    def _show_bright_preview(self, e):
        if e["layer"] is None:
            return
        it = self._ensure_bright_overlay()
        it.setPixmap(QPixmap.fromImage(e["layer"]))
        it.setPos(e["ox"], e["oy"])
        it.setVisible(True)

    def _hide_bright_preview(self):
        it = self._bright_overlay
        if it is None:
            return
        try:
            it.setVisible(False)
        except RuntimeError:
            # 场景清空时 C++ 对象已被销毁, 引用在这里顺手作废
            self._bright_overlay = None

    def has_pending_brightness(self):
        return any(e["dirty"] for e in self._bright_cache.values())

    def brightness_of(self, item):
        """该多边形当前的亮度值(没调过就是 0.5), 切回同一个框时把滑块摆回原位."""
        e = self._bright_cache.get(item)
        return e["value"] if e is not None and e["value"] is not None else 0.5

    def drop_brightness(self, commit=True):
        """
        换图或像素被别的操作改写时调: 基准作废, 下次按当下像素重取一份.
        默认先把没落盘的亮度写进像素, 否则拖了半天再点一下粘贴, 这次调节就白做了.
        """
        if commit:
            self.commit_brightness()
        self._bright_cache.clear()
        self._hide_bright_preview()
