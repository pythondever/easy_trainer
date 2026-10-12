# C# 示例（Microsoft.ML.OnnxRuntime + OpenCvSharp4）

## 依赖

```bash
dotnet add package Microsoft.ML.OnnxRuntime
dotnet add package OpenCvSharp4
dotnet add package OpenCvSharp4.runtime.win
```

需要 GPU 时把 `Microsoft.ML.OnnxRuntime` 换成 `Microsoft.ML.OnnxRuntime.Gpu`，
并把 `OnnxModel.Create(modelPath)` 的 `useGpu` 传 true。

## 文件

| 文件 | 作用 |
|---|---|
| `OnnxModel.cs` | 预处理、检测后处理、读类别表、中文路径读图（两套架构各一份） |
| `Detect.cs` | 目标检测（架构选 Transformer），结果写入 `detect_result.jpg` |
| `Segment.cs` | 实例分割（架构选 Transformer），掩码叠加写入 `segment_result.jpg` |
| `DetectCnn.cs` | 目标检测（架构选 CNN），结果写入 `detect_cnn_result.jpg` |
| `SegmentCnn.cs` | 实例分割（架构选 CNN），掩码叠加写入 `segment_cnn_result.jpg` |
| `Classify.cs` | 图像分类，打印 top-5 |
| `Program.cs` | 命令行入口 |

## 运行

```bash
dotnet run -- detect      模型.onnx test.jpg ..\label_map.json
dotnet run -- segment     模型.onnx test.jpg ..\label_map.json
dotnet run -- detect_cnn  模型.onnx test.jpg ..\label_map.json
dotnet run -- segment_cnn 模型.onnx test.jpg ..\label_map.json
dotnet run -- classify    模型.onnx test.jpg ..\label_map.json
```

检测与分割按**训练时选的架构**分成两套模型，示例也跟着分：架构选 Transformer（RF-DETR）
用 `Detect.cs` / `Segment.cs`，选 CNN（YOLO）用 `DetectCnn.cs` / `SegmentCnn.cs`。
两者的预处理（方形缩放 / 保比例补边）与输出层名称都不同，**不能互换**。

分辨率与阈值在各文件顶部的 `InputSize` / `ScoreThr` 常量里改。
