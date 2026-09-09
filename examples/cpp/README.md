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

模型路径、图像路径、`classes.txt` 路径以及工作目录都可以是中文，示例已做处理：

- 参数不用 `main` 的 `argv`（Windows 下已被 CRT 转成 GBK，中文必乱码），改用 `GetCommandLineW` 取 UTF-8；
- 读图走「读字节 + `imdecode`」而不是 `cv::imread`，写图走 `imencode` + 字节落盘
  （OpenCV 的窄字符 `imread/imwrite` 走 ANSI 代码页，中文路径打不开）；
- classes.txt 同样按字节流解析。

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

分辨率不用改：示例自动从模型输入 shape 读取(`INPUT_SIZE`),阈值在各自 cpp 顶部的 `SCORE_THR` 常量里改。
需要 GPU 时给 `Ort::SessionOptions` 追加 `OrtSessionOptionsAppendExecutionProvider_CUDA(opt, 0);`。
