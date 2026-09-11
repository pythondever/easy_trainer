# Easy Trainer

[**中文**](README.md) | [**English**](README.en.md)

> 基于 PySide6 的本地图像标注与深度学习训练工具，支持**目标检测 / 图像分割 / 图像分类**三类任务的标注、训练、测试与模型管理全流程。数据存储于本地 LMDB，无需联网即可完成 **标注 → 训练 → 评估** 闭环。

![主页](docs/images/主页.png)

## ✨ 核心特性

### 📁 项目与数据集管理
首页左侧项目树，支持多项目 / 多数据集的创建、添加、删除、修改、导入、导出、属性查看；右侧大图浏览 + 缩略图网格。

<p align="center">
  <img src="docs/images/添加项目.png" width="48%" />
  <img src="docs/images/添加_修改_删除_数据集.png" width="48%" />
</p>

### 📥 数据导入
支持单图或批量导入，检测/分割选图像目录 + 标签目录（labelme / YOLO txt），分类勾选"按子文件夹分类导入"（子文件夹名即类别）。大数据集懒加载缩略图，秒级呈现。

<p align="center">
  <img src="docs/images/导入数据.png" width="60%" />
</p>

### 🏷️ 标签管理
- **添加标签**：手动输入 + 10 种预设色 + 自定义颜色拾色器，多个标签用逗号分隔
- **跨数据集导入**：一键把同项目下其他数据集的标签全部导入（沿用源颜色）
- **修改类别**：标注界面直接点击框的标签 chip 切换类别
- **批量修改 / 删除**：合并 / 整类删除，自动改 json + 标签 txt 行首 id

<p align="center">
  <img src="docs/images/添加或导入标签.png" width="48%" />
  <img src="docs/images/修改类别.png" width="48%" />
</p>

<p align="center">
  <img src="docs/images/标签批量修改.png" width="40%" />
</p>

### ✏️ 图像标注
- **矩形**：拖拽绘制（chip 标签随缩放恒定大小）
- **多边形**：轨迹描边 + 自动抽稀闭合（轨迹颜色跟随所选标签）
- **格式刷**：圈选模板 → 任意位置刷子粘贴（像素复制，可撤销）
- **缩放 / 平移**：滚轮缩放、Space + 拖拽平移、缩放手柄、删除、显示标注开关
- A/D 翻页、Q/Ctrl+Z 等快捷键

<p align="center">
  <img src="docs/images/图像标注_矩形_多边形_格式刷.png" width="80%" />
</p>

### 🖼️ 首页浏览与按类筛选
标签下拉框按类别筛选缩略图，多类时图按数量分页（"共 N 个"按 cell 数），右上角统计当前筛选数量。

<p align="center">
  <img src="docs/images/按标注类别_分类筛选.png" width="80%" />
</p>

### 📊 数据集属性
查看数据集路径、标签分布柱状图（按数量降序，类多时 Top-N + 其他合并），列表与横轴支持滚动。

<p align="center">
  <img src="docs/images/数据集属性_标签分布.png" width="80%" />
</p>

### 🚀 训练
**子进程执行不阻塞 UI**，实时进度条、剩余时间、显存占用，支持手动停止（5 秒倒计时）。检测/分割走 RF-DETR，分类走 ResNet（18/34/50/101），所有网络尺寸下拉映射。支持**训练队列**：多组配置排队串行执行，可暂停 / 继续 / 停止，中断或失败后可一键重新入队。

<p align="center">
  <img src="docs/images/训练参数设置.png" width="48%" />
  <img src="docs/images/训练进度_指标_剩余时间_显存用量.png" width="48%" />
</p>

### 📈 训练指标回看
模型管理 → "指标" 打开折线图：val loss + 每类 mAP / mAR / F1 / Precision / Recall 全指标折线。

<p align="center">
  <img src="docs/images/训练指标查看.png" width="80%" />
</p>

### 🗂️ 模型管理
训练历史列表，按项目/任务/模型规模/精度/图像尺寸筛选，每条记录支持 **测试 / 指标 / 导出 / 删除**。

<p align="center">
  <img src="docs/images/模型训练记录.png" width="80%" />
</p>

### 🧪 模型测试
配置数据 / 设备 / 模型 / 置信度 / IoU 阈值，运行评估。检测/分割输出每类 P/R + 整体漏检误检分析；分类输出每类正确/错误统计。

<p align="center">
  <img src="docs/images/测试参数设置.png" width="48%" />
  <img src="docs/images/模型评估结果.png" width="48%" />
</p>

### 📜 日志
训练 / 测试 / 操作日志实时输出，异常自动弹窗。日志按天归档。

<p align="center">
  <img src="docs/images/日志.png" width="80%" />
</p>

---

## 🛠 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | ≥ 3.10 | RF-DETR 要求 Python 3.10+ |
| PySide6 | ≥ 6.6 | GUI 框架 |
| lmdb | ≥ 1.4 | 本地数据存储 |
| Pillow | ≥ 9.0 | 图像处理 |
| matplotlib | ≥ 3.5 | 指标曲线绘制 |
| numpy | ≥ 1.21 | 数值计算 |
| opencv-python-headless | ≥ 4.8 | 图像读取与尺寸处理 |

**训练 / 推理额外依赖**（需在 Python 3.10+ 环境安装）：

```bash
pip install torch torchvision
pip install "rfdetr>=1.9.2"
```

**模型导出 ONNX 额外依赖**（仅使用「模型管理 → 导出」时需要）：

```bash
pip install onnx onnxsim onnxruntime
```

## 🚀 快速开始

```bash
# 1. 安装基础依赖
pip install -r requirements.txt

# 2. 安装训练依赖（Python 3.10+）
pip install torch torchvision "rfdetr>=1.9.2"

# 3. 安装导出依赖（可选，需要导出 ONNX 时）
pip install onnx onnxsim onnxruntime

# 4. 启动
python app/easy_trainer.py
```

> 💡 不想配环境、或要发给同事/客户：见下一节的安装包（一个 exe 装完即用）。

**Ubuntu（Linux）源码运行**需补几个系统库：

```bash
sudo apt install libxcb-cursor0 libxkbcommon-x11-0 libegl1 libgl1 \
                 libdbus-1-3 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0
sudo apt install fonts-noto-cjk   # 中文字体
```

## 📦 打包与安装

源码运行适合开发；要交付"装了就能用"的包，走 `builder/` + `installer/`。

### 构建安装包

| 平台 | 命令 | 产物 |
|---|---|---|
| Windows | `python builder\build.py -t dist\program` | `dist\release\installer.exe` |
| Linux | `python3 builder/build.py -t dist/program` | `dist/release-linux/`（`installer.sh` + `program.zip` + 依赖清单 + 权重清单） |

`build.py` 依次完成：Cython 把 `app/`、`ui/` 全量编译成 `.pyd`（Linux 为 `.so`）→ 组 `dist/program`（`__init__.py`、`easy_trainer.py` 与 `style/`、`resources/`、`examples/` 保留明文）→ 打 `program.zip` → 调用平台发布器 → 清理中间产物。Windows 端需要 `cl.exe`（VS 2022 的 Developer PowerShell）与 .NET SDK 10；Linux 端需要 `gcc` 与 `python3.10-dev`。

编译只做本地打包，**不碰网络**：Python 运行时与预训练权重都由安装器在客户机按需获取。`.pyd` / `.so` 锁死 cp310 ABI，**换 Python 版本必须重编重发**；程序代码有改动也要重跑一次 `build.py`（`program.zip` 是构建期嵌进 exe 的）。

### 客户机安装

- **Windows**：只需一个 `installer.exe`，双击勾选组件；也支持静默安装
  ```powershell
  installer.exe --install D:\EasyTrainer runtime     # 组件: runtime / program / pretrained 逗号组合
  ```
- **Linux**：`./installer.sh [-d 安装目录] [-p]`（`-p` 一并安装预训练权重，约 880MB）

| 组件 | 来源 | 方式 |
|---|---|---|
| 程序本体 | 构建期嵌入 installer.exe | 解压，不联网 |
| 运行时 | 华为云官方 Python 3.10 embeddable 包 | 解压即用（绿色，不写注册表） |
| 依赖（torch 等） | 清华 PyPI + torch 专用源 | pip 现场安装（约 2.5GB 下载） |
| 预训练权重 | rfdetr 官方源（storage.googleapis.com） | 下载到 `pretrained\`（约 880MB） |

安装前按所选组件估算并校验磁盘空间（装运行时约需 10GB）；下载失败自动重试，pip 失败换源重试。**离线兜底**：把 `python-3.10.11-embed-amd64.zip` / `pretrained.zip` 放到安装器同目录即自动优先使用，完全不走网络。

> Windows 上 PyPI 的 `torch` 是 CPU-only，要 GPU 必须装 `torch==2.5.1+cu121`（只在 pytorch 源有）——requirements 已锁好并用 `--extra-index-url` 叠源，无需手工处理。

安装后的目录、启动链、Linux 特有注意事项等细节见 [installer/README.md](installer/README.md)。

## 📂 目录结构

```
easy_trainer/
├── app/                    # 主程序
│   ├── easy_trainer.py     # 启动引导（设好 sys.path/RF_HOME 后转交 main_window，发布时保留明文）
│   ├── main_window.py      # 主窗口：项目/数据集管理、标注渲染、训练/测试入口
│   ├── core/               # 数据访问层与通用工具
│   │   ├── db.py           # LMDB 数据访问层（YOLO label_ids、重命名合并等）
│   │   ├── utils.py        # 通用工具（中文字体、QSS 加载、项目根定位、文本解码）
│   │   ├── constants.py    # 全局常量（图像扩展名、分页大小、缓存上限）
│   │   ├── metrics.py      # 指标读取（metrics.csv 解析、最优 mAP 取值）
│   │   ├── image_utils.py  # 图像加载/缩略图/格式转换
│   │   ├── label_utils.py  # 标签归一化/排序/颜色，labelme 与 YOLO 互转
│   │   ├── log.py          # 滚动日志（按天归档）
│   │   └── keys.py         # LMDB 键名常量
│   ├── tasks/              # 后台任务（导入/合并）
│   │   ├── import_task.py  # 数据集扫描导入（检测/分割/分类）
│   │   └── merge_task.py   # 标签合并
│   ├── annotation/         # 标注画布与标注弹窗
│   │   ├── scene.py        # 标注场景（拖拽绘制、命中判定、撤销栈）
│   │   ├── box_item.py     # 标注图形项（矩形框 / 多边形 + 标签 chip）
│   │   ├── annotation_dialog.py  # 标注弹窗（画布缩放平移、画框/多边形/格式刷/改类/取色）
│   │   ├── blend.py        # 格式刷粘贴融合（Lab 亮度补偿 + 边缘羽化）
│   │   └── scene_items.py  # 场景辅助图形项
│   ├── widgets/            # 通用 UI 组件
│   │   ├── message_box.py  # 统一消息框/进度对话框
│   │   ├── dialog_buttons.py     # 弹窗按钮与图标统一样式
│   │   ├── name_input_dialog.py  # 命名输入弹窗
│   │   ├── paginator.py    # 分页控件
│   │   ├── project_sidebar.py    # 首页项目/数据集侧栏（卡片式树）
│   │   ├── charts.py       # 自绘图表（标签分布柱状图）
│   │   ├── status_style.py # 任务状态文案与配色
│   │   ├── queue_dialog.py # 训练队列弹窗
│   │   ├── log_dialog.py   # 日志查看弹窗
│   │   ├── model_dialog.py # 模型管理（历史记录、精度、测试、导出）
│   │   ├── test_dialog.py  # 测试参数弹窗
│   │   └── metrics_dialog.py   # 训练指标折线图
│   ├── mixins/             # 主窗口功能扩展（项目/数据集/标注/训练/队列/导入导出）
│   └── train/              # 训练与测试执行
│       ├── train_worker.py # 训练子进程线程（进度/指标/结果信号转发）
│       ├── train_runner.py # 检测/分割训练脚本（RF-DETR）
│       ├── classify_train_runner.py  # 分类训练脚本（ResNet + 每类精度）
│       ├── data_prep.py    # 训练数据准备（转 yolo 格式、类别收集）
│       ├── test_worker.py  # 测试子进程线程
│       ├── test_runner.py  # 检测/分割测试脚本
│       ├── classify_test_runner.py   # 分类测试脚本
│       ├── test_errors.py  # 漏检/误检分析
│       ├── test_report.py  # 评估报告 PDF 生成
│       ├── test_result_dialog.py  # 评估结果弹窗
│       ├── onnx_export.py  # ONNX 导出（检测/分割走 rfdetr，分类走 torch.onnx）
│       ├── export_worker.py  # 导出后台线程
│       └── dialogs.py      # 训练/测试弹窗
├── examples/               # ONNX 调用示例（导出时一并复制到导出目录）
│   ├── cpp/                # C++（ONNX Runtime + OpenCV）
│   ├── csharp/             # C#（Microsoft.ML.OnnxRuntime + OpenCvSharp4）
│   └── python/             # Python（onnxruntime + opencv）
├── builder/                # 打包发布（Windows / Linux 通用）
│   ├── build.py            # 一键发布：Cython 编译 → 组 program.zip → 调平台发布器
│   ├── requirements-release.txt  # 发布环境锁定依赖（嵌进安装器，客户机 pip 现场安装）
│   ├── pretrained-assets.txt     # 预训练权重清单（三端共用的唯一数据源）
│   └── get-pip.py          # pip 引导脚本（嵌进 installer.exe）
├── installer/              # 安装器
│   ├── Win.installer/      # C# 自绘安装器（dotnet publish → installer.exe）
│   ├── installer.sh        # Linux 安装脚本（venv + 解压 + pip + 桌面启动项）
│   └── README.md           # 安装器与发布流程细节
├── ui/                     # PySide6 UI 类（.py 由 .ui 编译生成）
├── docs/                   # 设计文档 + README 截图
├── resources/              # 图标等资源
├── style/                  # QSS 样式表
├── requirements.txt
├── README.md               # 中文说明（本文件）
└── README.en.md            # English README
```

## 🧭 使用流程

1. **新建项目** → 在项目下添加数据集
2. **导入数据**：右键数据集 → 导入。检测/分割选图像目录 + 标签目录（labelme/yolo），分类勾选"按子文件夹分类导入"
3. **标注**：双击数据集图像进入标注界面（矩形/多边形/格式刷），A/D 翻页，自动保存 labelme json
4. **训练**：工具栏"训练" → 选任务类型（检测/分割/分类）→ 配置参数 → 开始训练（5 秒倒计时后进入后台执行）
5. **测试**：模型管理 → 某条记录"测试" → 配置 → 运行评估
6. **回看指标**：模型管理 → "指标" 打开精度曲线
7. **导出模型**：模型管理 → 某条记录"导出"，生成 `项目_任务_尺寸_规模.pth` + `classes.txt`

> 💡 训练图像尺寸：检测默认 **640**、分割默认 **636**（12 的倍数）、分类默认 **224**。输入框悬停可见推荐值。

## 💾 数据存储

- **应用数据**：`~/.easy_trainer/app.mdb`（LMDB，保存项目/数据集绑定、标签、训练历史、删除记录等）
- **训练输出**：各任务 `输出路径` 下的时间戳目录（`config.json` / `result.json` / `metrics.json` / `checkpoint_best.pth` / `classes.txt`）
- **运行日志**：`logs/app.log`（滚动按天归档）

## 📝 文档

- [迁移计划 / 设计文档](docs/migration_plan.md)
- [使用教程](docs/使用教程.pdf)
- [安装器与发布流程](installer/README.md)
