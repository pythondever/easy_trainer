# Python 示例

依赖：

```bash
pip install onnxruntime opencv-python numpy
# 有 NVIDIA 显卡时把 onnxruntime 换成 onnxruntime-gpu，providers 改 CUDAExecutionProvider
```

异常检测示例（`ad.py`）不走 ONNX，依赖换一条：

```bash
pip install anomalib==2.6.2 torch
```

| 文件 | 作用 |
|---|---|
| `common.py` | 预处理 / 检测后处理 / 读类别表（label_map.json / classes.txt）|
| `detect.py` | 目标检测 |
| `segment.py` | 实例分割（画框 + 掩码叠加） |
| `classify.py` | 图像分类（输出 top-k） |
| `ocr.py` | OCR（字符检测 + 字符识别，两段模型） |
| `ad.py` | 异常检测（anomalib 直接加载模型文件，不走 ONNX） |

```bash
python detect.py   --model 模型.onnx --image test.jpg --classes ../label_map.json --save out.jpg
python segment.py  --model 模型.onnx --image test.jpg --classes ../label_map.json --save out.jpg
python classify.py --model 模型.onnx --image test.jpg --classes ../label_map.json
python ocr.py      --det 检测.onnx   --rec 识别.onnx --image test.jpg --save out.jpg
python ad.py       --model 模型.pt   --images D:/待测图像
```

参数：`--size` 模型输入分辨率（检测/分割默认 640，分类 224），
`--thr` 置信度阈值（默认 0.5）。

OCR 的检测段与识别段是两份模型，只做检测时不给 `--rec` 就行。识别段要读词表
（默认取识别模型同目录的 `vocab.txt`，可用 `--vocab` 指定）。加 `--json` 会把
结果写成 labelme 标注（带 OCR 标志位），可以直接拖回软件当标注用。
