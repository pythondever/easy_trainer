# -*- coding: utf-8 -*-
"""粘贴区域模板: 圈定"缺陷可以贴在哪里", 与标注完全分开.

模板区域不是标注: 不进 labelme json, 也不受"清空标注/显示标注/画模式"影响
(scene.all_items 按类型过滤, 天然把它排除在外). 靠插入顺序压在图像之上、标注之下.
"""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (QBrush, QColor, QPainterPath,
                           QPainterPathStroker, QPen, QPolygonF)
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsPolygonItem,
                               QGraphicsRectItem, QStyle)


from app.core import theme

FILL_ALPHA = 26         # 填充透明度: 只要看出范围, 别盖住缺陷本身
BADGE_ALPHA = 235
BADGE_W, BADGE_H = 20, 16
DASH = [6, 4]
REGION_Z = 0.5
MARK_Z = 12            # 自动粘贴的标记框: 要压在标注(10)之上才看得见
HIT_PAD = 9.0          # 命中判定把轮廓加粗这么多: 细缝区域几乎没有"内部", 按填充判点不中


def _accent():
    return QColor(theme.color("accent"))


class PasteRegionItem(QGraphicsPolygonItem):
    """一个可粘贴区域: 虚线描边 + 序号角标(不填充, 免得压住底下的缺陷).

    不接鼠标: 命中与选中都走 scene.mousePressEvent, 免得抢掉画框/框选/拖顶点;
    """

    def __init__(self, points, index):
        super().__init__(QPolygonF([QPointF(float(x), float(y))
                                    for x, y in points]))
        self.index = int(index)
        # 不接鼠标(见 set_selectable): 命中与选中都走 scene.mousePressEvent,
        # 免得抢掉画框/框选/拖顶点
        # 图像 z=0, 亮度预览 z=1, 标注 z=10(box_item 里写死): 区域夹在图像与预览
        # 之间, 这样不管先加谁都不会盖住标注, 也不至于被图像挡住
        self.setZValue(REGION_Z)
        self.set_selectable(True)
        pen = QPen(_accent(), 1.6)
        pen.setStyle(Qt.DashLine)
        pen.setDashPattern(DASH)
        self.setPen(pen)
        # 不填充: 区域只是"范围提示", 铺一层蓝底会把底下的缺陷和粘贴效果压住
        self.setBrush(QBrush(Qt.NoBrush))

    def set_selectable(self, on):
        """能不能用左键点选(命中由 scene 判, 这里只管选中标记).

        画模式下必须关掉: 那时左键要留给"拉多边形".
        """
        on = bool(on)
        # 鼠标一律不接: 命中统一放在 scene.mousePressEvent 判(区域不参与标注
        # 那套逻辑), 交给 item 反而会影响"点空白处记粘贴锚点"
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, on)
        if not on and self.isSelected():
            self.setSelected(False)
        self.update()

    def shape(self):
        """命中区域用"描边加粗后的轮廓"而不是填充: 用户画歪成一条细缝时,
        多边形内部几乎为空, 只按填充判会怎么点都点不中(只能干瞪眼).
        """
        path = QPainterPath()
        path.addPolygon(self.polygon())
        path.closeSubpath()
        stroker = QPainterPathStroker()
        stroker.setWidth(HIT_PAD)
        # 必须与多边形本身求并: createStroke 只给"沿轮廓的一条环带", 不含内部,
        # 那样点区域中心反而命中不了(只剩细缝那种边上点才中)
        return stroker.createStroke(path).united(path)

    def region_points(self):
        return [[float(p.x()), float(p.y())] for p in self.polygon()]

    def boundingRect(self):
        # 角标画在多边形外接框左上角外侧, 不扩边界会被裁掉
        return super().boundingRect().adjusted(
            -BADGE_W - 4, -BADGE_H - 4, 0, 0)

    def paint(self, painter, option, widget=None):
        # 选中只把描边加粗: 默认的 QGraphicsPolygonItem 只按 pen/brush 画, 不加粗
        # 就看不出点中的是哪个区域; 不填充(填充会压住底下的缺陷)
        if option.state & QStyle.StateFlag.State_Selected:
            old_pen = self.pen()
            pen = QPen(_accent(), 2.8)
            pen.setStyle(Qt.DashLine)
            pen.setDashPattern(DASH)
            self.setPen(pen)
            super().paint(painter, option, widget)
            self.setPen(old_pen)
        else:
            super().paint(painter, option, widget)
        r = self.polygon().boundingRect()
        badge = QRectF(r.left() - BADGE_W - 2, r.top() - BADGE_H - 2,
                       BADGE_W, BADGE_H)
        painter.save()
        bg = _accent()
        bg.setAlpha(BADGE_ALPHA)
        painter.setPen(Qt.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(badge, 3, 3)
        painter.setPen(QColor(theme.color("bg_base")))
        painter.drawText(badge, Qt.AlignCenter, str(self.index))
        painter.restore()



class AutoPasteMark(QGraphicsPolygonItem):
    """一次自动粘贴留下的轮廓: 只供贴完那一下的强调动画用, 闪完就删掉.

    不接鼠标、不参与撤销(撤销统一走 Ctrl+Z); 画成多边形而不是外接矩形,
    是因为贴上去的图可能转过角度, 外接矩形会凭空大一圈.
    """

    def __init__(self, polygon, record):
        super().__init__(polygon)
        self.record = record
        self.setZValue(MARK_Z)
        # 默认什么都不画: 贴完还挂着虚线会挡住图案本身的效果,
        # 只有贴完那一下的强调动画会给它上笔. 命中不靠它(scene 里按多边形判)
        self.setPen(Qt.NoPen)
        self.setBrush(QBrush(Qt.NoBrush))
        self.setAcceptedMouseButtons(Qt.NoButton)


def regions_payload(items, image_size):
    """区域 item 列表 -> 可存盘 dict. 记下参考尺寸, 换到尺寸不同的图时才谈得上换算."""
    return {"ref_size": [int(image_size[0]), int(image_size[1])],
            "regions": [item.region_points() for item in items]}


def scaled_regions(payload, image_size):
    """可存盘 dict -> 当前图坐标的区域列表, 返回 (regions, aspect_warn).

    参考尺寸一致就原样用; 不一致按长宽比分别缩放. 长宽比本身差得多说明不是同一种
    版面, 硬套会贴错位置, 这时照样按比例缩放, 但让上层提示用户.
    """
    regions = [[[float(x), float(y)] for x, y in r]
               for r in (payload.get("regions") or []) if len(r) >= 3]
    iw, ih = float(image_size[0]), float(image_size[1])
    ref = payload.get("ref_size") or []
    try:
        rw, rh = float(ref[0]), float(ref[1])
    except (TypeError, ValueError, IndexError):
        rw = rh = 0.0
    if rw <= 0 or rh <= 0 or iw <= 0 or ih <= 0 or (rw, rh) == (iw, ih):
        return regions, False
    sx, sy = iw / rw, ih / rh
    regions = [[[x * sx, y * sy] for x, y in r] for r in regions]
    return regions, abs(sx - sy) > 0.02


def template_key(project, dataset):
    """"项目/数据集"作键: 同一相机工位的版面一致, 一套区域复用一个数据集."""
    return "{}/{}".format(project, dataset)
