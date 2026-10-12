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

## 中文路径

模型路径、图像路径、类别表路径以及工作目录都可以是中文，示例已做处理：

- 参数不用 `main` 的 `argv`（Windows 下已被 CRT 转成 GBK，中文必乱码），改用 `GetCommandLineW` 取 UTF-8；
- 读图走「读字节 + `imdecode`」而不是 `cv::imread`，写图走 `imencode` + 字节落盘
  （OpenCV 的窄字符 `imread/imwrite` 走 ANSI 代码页，中文路径打不开）；
- 类别表（label_map.json / classes.txt）同样按字节流解析。

## 文件

| 文件 | 作用 |
|---|---|
| `common.h` | 预处理、检测后处理、读类别表（两套架构各一份） |
| `detect.cpp` | 目标检测（架构选 Transformer），结果画到 `detect_result.jpg` |
| `segment.cpp` | 实例分割（架构选 Transformer），掩码叠加到 `segment_result.jpg` |
| `detect_cnn.cpp` | 目标检测（架构选 CNN），结果画到 `detect_cnn_result.jpg` |
| `segment_cnn.cpp` | 实例分割（架构选 CNN），掩码叠加到 `segment_cnn_result.jpg` |
| `classify.cpp` | 图像分类，打印 top-5 |

## 调用方式

```bash
detect.exe    模型.onnx test.jpg ..\label_map.json
segment.exe   模型.onnx test.jpg ..\label_map.json
detect_cnn.exe  模型.onnx test.jpg ..\label_map.json
segment_cnn.exe 模型.onnx test.jpg ..\label_map.json
classify.exe  模型.onnx test.jpg ..\label_map.json
```

检测与分割按**训练时选的架构**分成两套模型，示例也跟着分：架构选 Transformer（RF-DETR）
用 `detect.cpp` / `segment.cpp`，选 CNN（YOLO）用 `detect_cnn.cpp` / `segment_cnn.cpp`。
两者的预处理（方形缩放 / 保比例补边）与输出层名称都不同，**不能互换**。

分辨率不用改：示例自动从模型输入 shape 读取(`INPUT_SIZE`),阈值在各自 cpp 顶部的 `SCORE_THR` 常量里改。
需要 GPU 时给 `Ort::SessionOptions` 追加 `OrtSessionOptionsAppendExecutionProvider_CUDA(opt, 0);`。
