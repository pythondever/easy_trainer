# Python 示例

依赖：

```bash
pip install onnxruntime opencv-python numpy
# 有 NVIDIA 显卡时把 onnxruntime 换成 onnxruntime-gpu，providers 改 CUDAExecutionProvider
```

| 文件 | 作用 |
|---|---|
| `common.py` | 预处理 / 检测后处理 / 读 classes.txt |
| `detect.py` | 目标检测 |
| `segment.py` | 实例分割（画框 + 掩码叠加） |
| `classify.py` | 图像分类（输出 top-k） |

```bash
python detect.py   --model 模型.onnx --image test.jpg --classes ../classes.txt --save out.jpg
python segment.py  --model 模型.onnx --image test.jpg --classes ../classes.txt --save out.jpg
python classify.py --model 模型.onnx --image test.jpg --classes ../classes.txt
```

参数：`--size` 模型输入分辨率（检测/分割默认 640，分类 224），
`--thr` 置信度阈值（默认 0.5）。
