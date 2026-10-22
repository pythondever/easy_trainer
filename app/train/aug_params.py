# -*- coding: utf-8 -*-
"""
勾选代号 → 训练后端增强参数的唯一映射.

界面只存代号串(hflip,brightness...), 两个 runner 各自按自己的后端展开成字典.
预览要在 GUI 进程里拿到同一份参数, 而 cnn_train_runner 顶层带 ultralytics、
transformer_train_runner 顶层带 rfdetr, 都不能从界面 import, 所以参数表单独
放这里, 谁也不依赖谁.
"""

# ultralytics 的增强默认值全是开着的(马赛克 1.0、hsv_s 0.7、fliplr 0.5...), 所以先把
# 这批全置 0, 再按勾选覆盖: 界面上"不勾选"才等于真的不增强
YOLO_AUG_OFF = {
    "mosaic": 0.0, "mixup": 0.0, "cutmix": 0.0, "copy_paste": 0.0,
    "perspective": 0.0, "bgr": 0.0,
    "hsv_h": 0.0, "hsv_s": 0.0, "hsv_v": 0.0,
    "degrees": 0.0, "translate": 0.0, "scale": 0.0, "shear": 0.0,
    "flipud": 0.0, "fliplr": 0.0,
}

# 勾选代号对应 ultralytics 超参. 模糊/噪声没有原生参数(ultralytics 自己那两项是靠
# albumentations 实现的), 界面在 CNN 下把这两项置灰; 亮度也只有 hsv_v 一项可对应
YOLO_AUG_PARAMS = {
    "hflip": {"fliplr": 0.5},
    "vflip": {"flipud": 0.5},
    "rotate": {"degrees": 15.0},
    "affine": {"scale": 0.2, "translate": 0.1, "shear": 5.0},
    "mosaic": {"mosaic": 1.0},
    "brightness": {"hsv_v": 0.1},
    "colorjitter": {"hsv_h": 0.1, "hsv_s": 0.2},
}

# 勾选代号对应 rfdetr 的 aug_config 片段. GUI 进程不导入 rfdetr, 免得为了几个
# 字面量让启动多等一两秒
AUG_TRANSFORMS = {
    "hflip": {"HorizontalFlip": {"p": 0.5}},
    "vflip": {"VerticalFlip": {"p": 0.5}},
    "rotate": {"Rotate": {"limit": 15, "p": 0.5}},
    "affine": {"Affine": {"scale": (0.8, 1.2), "translate_percent": (-0.1, 0.1),
                          "rotate": (-15, 15), "shear": (-5, 5), "p": 0.5}},
    "brightness": {"RandomBrightnessContrast": {"brightness_limit": 0.1,
                                                "contrast_limit": 0.1, "p": 0.3}},
    "colorjitter": {"ColorJitter": {"brightness": 0.2, "contrast": 0.2,
                                    "saturation": 0.2, "hue": 0.1, "p": 0.5}},
    "blur": {"GaussianBlur": {"blur_limit": 3, "p": 0.3}},
    "noise": {"GaussNoise": {"std_range": (0.01, 0.05), "p": 0.3}},
}

# 改造前的记录存的是单档预设代号, 展开成勾选组合才能对上
AUG_LEGACY_CODES = {
    "off": (),
    "default": ("hflip",),
    "conservative": ("hflip", "brightness"),
    "industrial": ("hflip", "brightness", "blur", "noise"),
    "aggressive": ("hflip", "vflip", "rotate", "affine", "colorjitter"),
}

# 各代号吃得下的后端: 没列到的两项通吃. 马赛克只有 ultralytics 有,
# 模糊/噪声 ultralytics 没有原生参数, 在 CNN 下置灰
AUG_BOTH = ("transformer", "cnn")
AUG_FAMILIES = {
    "mosaic": ("cnn",),
    "blur": ("transformer",),
    "noise": ("transformer",),
}

# 整块隐藏而不是置灰的项: 留着会让 CNN 那一列凭空少一格
AUG_HIDE_WHEN_UNSUPPORTED = ("mosaic",)


def aug_codes(value):
    """记录里的增强值展开成代号元组: 新值是逗号串, 旧值是单档预设代号."""
    text = str(value or "").strip().lower()
    if not text:
        return ()
    return AUG_LEGACY_CODES.get(text, tuple(text.split(",")))


def resolve_yolo_aug(value):
    """勾选代号串转成 ultralytics 增强超参; 空值/没勾/代号全不认识都给全 0."""
    out = dict(YOLO_AUG_OFF)
    for code in aug_codes(value):
        frag = YOLO_AUG_PARAMS.get(str(code).strip())
        if frag:
            out.update(frag)
    return out


def resolve_aug_config(value):
    """勾选代号串转成 aug_config 字典. 空值/没勾/代号全不认识都给 {} (空字典即不增强)."""
    out = {}
    for code in aug_codes(value):
        frag = AUG_TRANSFORMS.get(str(code).strip())
        if frag:
            out.update(frag)
    return out
