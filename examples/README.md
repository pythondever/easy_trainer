# 模型调用示例（ONNX Runtime）

本目录由 EasyTrainer 导出模型时自动复制到导出目录，包含 **C++ / C# / Python** 三种语言调用
ONNX 模型做 **目标检测 / 实例分割 / 图像分类** 推理的完整示例。**OCR** 导出的是两段
模型、后处理也另成一套，见下面单独一节（目前只提供 Python 版）。

## 导出产物

```
项目_时间戳/
├── 项目_任务_尺寸_规模.onnx     # 模型（检测/分割/分类同一份）
├── label_map.json               # 类名 → id 的映射（下游按名字查，见下）
├── 项目_任务_尺寸_规模_评估报告.pdf
└── examples/                    # 本目录
```

## 类别 id 会变，认名字不要认序号

`label_map.json` 里的 `id` 是**训练时按类名排序临时分配的序号**，不是类别的永久身份。
新增或删除类别后，同一个类名的 id 会跟着变：先训了 `划痕 / 压伤 / 脏污`（脏污 = 2），
后来加进 `发白 / 露铜`，排序时 `发白` 插在中间，再训练时 **脏污 就变成 3**。

下游**不要按 id 写死业务逻辑**（「2 就是脏污」这种），换一次模型就可能错位。
按类名查 `label_map.json` 才是稳的：

```json
{
  "划痕": 0,
  "压伤": 1,
  "发白": 2,
  "脏污": 3,
  "露铜": 4
}
```

```python
import json
label_map = json.load(open("label_map.json", encoding="utf-8"))
label_map["脏污"]        # → 3，始终是当前这份模型里「脏污」的 id
```

需要「id → 类名」的正查时，三套示例的类别表读取函数可以直接用
（Python `load_classes` / C++ `loadClasses` / C# `OnnxModel.LoadClasses`），
返回的就是按 id 下标排列的类名列表。

> 早先版本导出的是 `classes.txt`（每行 `id 类名`）。现在只在**训练产物目录**和
> **历史导出包**里还能见到它 —— 三套示例的类别表读取函数两种格式都认，
> 传 `classes.txt` 或 `label_map.json` 都能读。注意 `classes.txt` 有个坑：
> 类名含空格时（如 `OK 良品`）按空格切分会截断成 `OK`，json 没有这个歧义。

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

## OCR（字符检测 + 字符识别）

OCR 和其他任务不同：它导出**两份 ONNX**。检测段只出文字框，识别段只读框里的字，
两段串起来才是完整的 OCR。

```
项目_时间戳/
├── 项目_字符检测_尺寸_规模.onnx   # 检测段：概率图 → 文字框
├── 项目_字符识别_尺寸_规模.onnx   # 识别段：字条 → 文字
├── vocab.txt                     # 识别段的词表（一行字符，顺序即类别 id）
└── examples/                     # 本目录
```

**字符检测**

| 项 | 名称 | 形状 | 说明 |
|---|---|---|---|
| 输入 | `images` | `[1, 3, H, W]` | H=W=训练分辨率（默认 1024），RGB 顺序 |
| 输出 | `logits` | `[1, 1, H, W]` | **没过 sigmoid 的** logits，不是概率图 |

**字符识别**

| 项 | 名称 | 形状 | 说明 |
|---|---|---|---|
| 输入 | `images` | `[1, 3, 32, 128]` | 固定 32×128，与训练一致，不随检测尺寸走 |
| 输出 | `logits` | `[1, T, C]` | T 个时间步，C = 词表长度 + 1，**最后一列是 blank** |

后处理两段都要自己做（官方 predictor 里那套带着 numpy 与动态控制流，进不了 ONNX）：

1. **检测**：`sigmoid` → 按 0.3 二值化 → **3×3 开运算**（不做的话概率图边缘的零星
   激活会碎成一堆 1~2 像素的假框）→ 找外轮廓 → 取外接框（宽或高 < 2 像素的丢掉）
   → 框内概率均值低于 0.1 的丢掉 → 坐标按 `原图 / 输入` 的比例还原（方形缩放，
   宽高各按各的比例）
2. **识别**：按框从原图裁出字条 → 拉伸到 32×128 → `softmax` → `argmax` 取每步字符
   → **合并连续重复、去掉 blank** → 按词表映射成文字

调用见 `python/ocr.py`：

```bash
python ocr.py --det 检测.onnx --image test.jpg                    # 只做检测，画框
python ocr.py --det 检测.onnx --rec 识别.onnx --image test.jpg --save out.jpg
python ocr.py --det 检测.onnx --rec 识别.onnx --image test.jpg --json
```

`--json` 写出的 labelme 标注带 `"ocr": true` 标志位，拖回软件会被自动认成字符检测
数据集，可直接用来核对结果或补标。

> 两段是**分开训练、分开导出**的：检测段照常出评估报告（漏检/误检分析），识别段只
> 有 CER 一个结论，不生成评估报告。

## 中文路径

三种语言的示例都支持**中文的模型路径、图像路径、类别表路径，以及中文工作目录**，无需额外设置。

Windows 下代码已经绕过两个坑：OpenCV 的 `imread/imwrite` 走 ANSI 代码页（中文路径打不开，
改为「读字节 + `imdecode` / `imencode` + 字节落盘」），C++ 的 `main(argv)` 已被 CRT 转成 GBK
（改用 `GetCommandLineW` 直接取宽字符命令行）。Python 侧读图同样没用 `cv2.imread`。

## 异常检测（AD）

异常检测交付的**不是 ONNX**。AD 模型是「骨干 + 良品特征库」的组合结构，不是一条
前向网络，导不出 ONNX，所以交付的是原模型文件加几份说明：

```
项目_时间戳/
├── 项目_异常_尺寸_规模.pt      # 模型（自包含：构造参数 + 全部权重 + 判定阈值）
├── threshold.txt               # 判定阈值，一行数字
├── result.json                 # 训练时的验证集指标
├── README.txt                  # 交付说明（含离线部署的骨干权重要求）
└── examples/                   # 本目录
```

调用示例见 `python/ad.py`：

```bash
pip install anomalib==2.6.2 torch
python ad.py --model 模型.pt --images D:/待测图像
```

每张图算出一个**异常分**（特征空间的距离，不是 0~1 的概率，量级几十很正常），
`分数 >= 阈值` 判为异常。输入尺寸和阈值都从模型文件里读，不用手动传。

> 离线机器上还要备一份骨干权重 `wide_resnet50_2.racm_in1k`（约 275 MB）——
> anomalib 建模型时就要从 HuggingFace 缓存里取，缺了会直接报
> `LocalEntryNotFoundError`，哪怕权重已经在模型文件里。放法见导出目录的 `README.txt`。

## 各语言依赖

| 语言 | 依赖 | 安装 |
|---|---|---|
| Python | `onnxruntime opencv-python numpy` | `pip install onnxruntime opencv-python numpy` |
| C++ | OpenCV 4.x、ONNX Runtime 1.16+（C API） | 见 `cpp/README.md` |
| C# | `Microsoft.ML.OnnxRuntime`、`OpenCvSharp4` | `dotnet add package Microsoft.ML.OnnxRuntime OpenCvSharp4` |

> 上表的依赖连 OCR 一起覆盖（CTC 解码与开运算都只用 OpenCV + numpy）。C++ / C# 目前
> 只给了检测 / 分割 / 分类的示例，OCR 示例只有 Python 版。
