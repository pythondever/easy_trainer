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
| `OnnxModel.cs` | 预处理（方形缩放 + ImageNet 归一化）、检测后处理、读 classes.txt、中文路径读图 |
| `Detect.cs` | 目标检测，结果写入 `detect_result.jpg` |
| `Segment.cs` | 实例分割，掩码叠加写入 `segment_result.jpg` |
| `Classify.cs` | 图像分类，打印 top-5 |
| `Program.cs` | 命令行入口 |

## 运行

```bash
dotnet run -- detect   模型.onnx test.jpg ..\classes.txt
dotnet run -- segment  模型.onnx test.jpg ..\classes.txt
dotnet run -- classify 模型.onnx test.jpg ..\classes.txt
```

分辨率与阈值在各文件顶部的 `InputSize` / `ScoreThr` 常量里改。
