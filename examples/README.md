# 模型调用示例（ONNX Runtime）

本目录由 EasyTrainer 导出模型时自动复制到导出目录，包含 **C++ / C# / Python** 三种语言调用
ONNX 模型做 **目标检测 / 实例分割 / 图像分类** 推理的完整示例。

## 导出产物

```
项目_时间戳/
├── 项目_任务_尺寸_规模.onnx     # 模型（检测/分割/分类同一份）
├── classes.txt                  # 类别清单，行号即类别 id
├── 项目_任务_尺寸_规模_评估报告.pdf
└── examples/                    # 本目录
```

## 模型输入输出约定

**检测 / 分割（RF-DETR 导出）**

| 项 | 名称 | 形状 | 说明 |
|---|---|---|---|
| 输入 | `input` | `[1, 3, H, W]` | H=W=训练分辨率（检测默认 640），RGB 顺序 |
| 输出 | `dets` | `[1, N, 4]` | N 个候选框（检测 300 / 分割 100），`(cx, cy, w, h)`，**归一化到 0~1** |
| 输出 | `labels` | `[1, N, C+1]` | 分类 logits，最后一列是「无目标」，**用 sigmoid 不是 softmax** |
| 输出（仅分割） | `masks` | `[1, N, Mh, Mw]` | 掩码 logits（`Mh=Mw=H/4`），sigmoid 后 >0.5 视为前景，再放大回原图 |

> 候选数 N 随模型规模变化，示例代码都从输出 shape 动态读取，不要写死。
> 输入尺寸同理：导出时固定为训练分辨率，示例自动从模型读取，不用手动指定。

**分类**

| 项 | 名称 | 形状 | 说明 |
|---|---|---|---|
| 输入 | `images` | `[1, 3, 224, 224]` | RGB |
| 输出 | `scores` | `[1, C]` | 各类别 logits，**用 softmax** |

### 预处理

1. 图像直接**方形缩放**到模型分辨率（不保持宽高比，与训练时一致）
2. `像素值 / 255`
3. 减 `mean = (0.485, 0.456, 0.406)`，除 `std = (0.229, 0.224, 0.225)`
4. 通道顺序 `HWC → CHW`，前面补 batch 维

### 后处理

1. `score = sigmoid(labels[i])`，只取**前 C 列**（丢掉最后一列「无目标」）
2. `类别 id = argmax(前 C 列)`，`置信度 = 该列 sigmoid 值`
3. 过滤 `置信度 < threshold` 的候选（建议 0.5）
4. `(cx, cy, w, h) → (x1, y1, x2, y2)`，乘原图宽高还原到像素坐标

> 300 个候选已经是端到端去重结果，**不需要再做 NMS**。

## 各语言依赖

| 语言 | 依赖 | 安装 |
|---|---|---|
| Python | `onnxruntime opencv-python numpy` | `pip install onnxruntime opencv-python numpy` |
| C++ | OpenCV 4.x、ONNX Runtime 1.16+（C API） | 见 `cpp/README.md` |
| C# | `Microsoft.ML.OnnxRuntime`、`OpenCvSharp4` | `dotnet add package Microsoft.ML.OnnxRuntime OpenCvSharp4` |
