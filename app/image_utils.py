# -*- coding: utf-8 -*-
"""图像工具：PIL 打开、PIL→QImage 转换、统一规格缩略图。"""
from PIL.ImageQt import ImageQt
from PySide6.QtGui import QImage

import PIL.Image as PILImage


def pil_open(path):
    return PILImage.open(path)


def pil_to_qimage(pil_img):
    """PIL RGB -> QImage(ARGB32,主线程转 QPixmap 使用)。"""
    try:
        qimg = ImageQt(pil_img).copy()
        return qimg
    except Exception:
        data = pil_img.tobytes("raw", "RGB")
        qimg = QImage(data, pil_img.width, pil_img.height,
                      pil_img.width * 3, QImage.Format_RGB888)
        return qimg.copy()


def make_uniform_thumb(pil_img, size=(200, 200), bg=(19, 21, 26), fill=False):
    """
    统一规格缩略图到 size×size。
    fill=False(默认): 等比缩放 + 居中 + 深色背景填充(首页 #13151a),
        用于整图缩略(保持原图比例，不变形).
    fill=True:不等比 resize 到 size×size（保证 QImage 严格统一规格）,
        用于 ROI 裁剪——无论原标注框大小或长宽比,
        渲染到 cell 都是严格 200×200 占满,绝对统一规格.
    """
    if fill:
        return pil_img.resize(size, PILImage.LANCZOS)
    thumb = pil_img.copy()
    thumb.thumbnail(size)
    canvas = PILImage.new("RGB", size, bg)
    off_x = (size[0] - thumb.width) // 2
    off_y = (size[1] - thumb.height) // 2
    if off_x >= 0 and off_y >= 0:
        canvas.paste(thumb, (off_x, off_y))
    return canvas
