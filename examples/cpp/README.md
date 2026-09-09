# C++ 示例（ONNX Runtime C++ API + OpenCV）

## 依赖

| 库 | 版本 | 获取 |
|---|---|---|
| OpenCV | 4.x | vcpkg: `vcpkg install opencv` |
| ONNX Runtime | 1.16+ | https://github.com/microsoft/onnxruntime/releases 下载 `onnxruntime-win-x64-*.zip` |

## 编译

```bash
cmake -S . -B build -DONNXRUNTIME_DIR=D:/libs/onnxruntime-win-x64-1.18.0 -DCMAKE_PREFIX_PATH=D:/libs/opencv/build
cmake --build build --config Release
```

运行时把 `onnxruntime.dll`、`onnxruntime_providers_shared.dll` 放到 exe 同目录。

## 文件

| 文件 | 作用 |
|---|---|
| `common.h` | 预处理（方形缩放 + ImageNet 归一化）、检测后处理、读 classes.txt |
| `detect.cpp` | 目标检测，结果画到 `detect_result.jpg` |
| `segment.cpp` | 实例分割，掩码叠加到 `segment_result.jpg` |
| `classify.cpp` | 图像分类，打印 top-5 |

## 调用方式

```bash
detect.exe   模型.onnx test.jpg ..\classes.txt
segment.exe  模型.onnx test.jpg ..\classes.txt
classify.exe 模型.onnx test.jpg ..\classes.txt
```

分辨率与阈值在各自 cpp 顶部的 `INPUT_SIZE` / `SCORE_THR` 常量里改。
需要 GPU 时给 `Ort::SessionOptions` 追加 `OrtSessionOptionsAppendExecutionProvider_CUDA(opt, 0);`。
