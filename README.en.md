# Easy Trainer

[**中文**](README.md) | [**English**](README.en.md)

> A local image annotation and deep-learning training tool built on PySide6. Supports the full pipeline for **object detection / image segmentation / image classification**: annotation, training, testing, and model management. All data is stored in a local LMDB — the **annotate → train → evaluate** loop works fully offline.

![Home](docs/images/主页.png)

## ✨ Key Features

### 📁 Project & Dataset Management
Project tree on the left of the home page: create / add / delete / rename / import / export datasets and inspect properties; large-image preview + thumbnail grid on the right.

<p align="center">
  <img src="docs/images/添加项目.png" width="48%" />
  <img src="docs/images/添加_修改_删除_数据集.png" width="48%" />
</p>

### 📥 Data Import
Single or batch import. For detection/segmentation choose an image directory + a label directory (labelme / YOLO txt); for classification enable "import by sub-folder" (sub-folder name = class). Large datasets lazy-load thumbnails for near-instant display.

<p align="center">
  <img src="docs/images/导入数据.png" width="60%" />
</p>

### 🏷️ Label Management
- **Add labels**: type names + 10 preset colors + custom color picker; multiple labels separated by commas
- **Import labels across datasets**: one-click copy all labels from another dataset in the same project (keeps source colors)
- **Change class**: click the label chip on a box inside the annotation view
- **Batch edit / delete**: merge or delete whole classes, automatically rewriting labelme json and the first id column of YOLO txt

<p align="center">
  <img src="docs/images/添加或导入标签.png" width="48%" />
  <img src="docs/images/修改类别.png" width="48%" />
</p>

<p align="center">
  <img src="docs/images/标签批量修改.png" width="40%" />
</p>

### ✏️ Annotation
- **Rectangle**: drag to draw (label chips stay a constant pixel size while zooming)
- **Polygon**: freehand tracing + automatic point thinning on close (trace color follows the selected label)
- **Format painter**: select a template region → paint copies anywhere (pixel copy, undoable)
- **Zoom / pan**: mouse-wheel zoom, Space + drag pan, resize handles, delete, show/hide boxes
- Shortcuts: A/D for prev/next, Q / Ctrl+Z, etc.

<p align="center">
  <img src="docs/images/图像标注_矩形_多边形_格式刷.png" width="80%" />
</p>

### 🖼️ Home Browsing & Filtering by Class
Filter thumbnails by label from the dropdown; images are paginated by cell count when multiple classes exist; the top-right shows the current filtered count.

<p align="center">
  <img src="docs/images/按标注类别_分类筛选.png" width="80%" />
</p>

### 📊 Dataset Properties
Shows dataset paths and a label-distribution bar chart (descending by count; Top-N + "others" merged when there are many classes). Lists and axis are scrollable.

<p align="center">
  <img src="docs/images/数据集属性_标签分布.png" width="80%" />
</p>

### 🚀 Training
Runs in a **child process without blocking the UI**: live progress bar, ETA, GPU memory usage, manual stop (5-second countdown). Detection/segmentation use RF-DETR; classification uses ResNet (18/34/50/101). All network sizes map from a dropdown.

<p align="center">
  <img src="docs/images/训练参数设置.png" width="48%" />
  <img src="docs/images/训练进度_指标_剩余时间_显存用量.png" width="48%" />
</p>

### 📈 Metrics Review
Model management → "Metrics" opens line charts: val loss + per-class mAP / mAR / F1 / Precision / Recall.

<p align="center">
  <img src="docs/images/训练指标查看.png" width="80%" />
</p>

### 🗂️ Model Management
Training history list, filterable by project / task / model size / metric / image size; each record supports **test / metrics / export / delete**.

<p align="center">
  <img src="docs/images/模型训练记录.png" width="80%" />
</p>

### 🧪 Model Testing
Configure data / device / model / confidence / IoU thresholds and run evaluation. Detection/segmentation output per-class P/R plus a global missed/false-positive analysis; classification outputs per-class correct/incorrect stats.

<p align="center">
  <img src="docs/images/测试参数设置.png" width="48%" />
  <img src="docs/images/模型评估结果.png" width="48%" />
</p>

### 📜 Logs
Real-time training / testing / operation logs; errors pop up automatically. Logs rotate daily.

<p align="center">
  <img src="docs/images/日志.png" width="80%" />
</p>

---

## 🛠 Requirements

| Dependency | Version | Notes |
|------|------|------|
| Python | ≥ 3.10 | RF-DETR requires Python 3.10+ |
| PySide6 | ≥ 6.6 | GUI framework |
| lmdb | ≥ 1.4 | Local data store |
| Pillow | ≥ 9.0 | Image processing |
| matplotlib | ≥ 3.5 | Metric charts |
| numpy | ≥ 1.21 | Numeric computing |

**Additional dependencies for training/inference** (install in a Python 3.10+ environment):

```bash
pip install torch torchvision
pip install "rfdetr>=1.9.2"
```

## 🚀 Quick Start

```bash
# 1. Install base dependencies
pip install -r requirements.txt

# 2. Install training dependencies (Python 3.10+)
pip install torch torchvision "rfdetr>=1.9.2"

# 3. Run
python app/easy_trainer.py
```

> **Ubuntu (Linux)** — PySide6 needs a few system libraries:
> ```bash
> sudo apt install libxcb-cursor0 libxkbcommon-x11-0 libegl1 libgl1 \
>                  libdbus-1-3 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0
> sudo apt install fonts-noto-cjk   # Chinese fonts
> ```

## 📂 Directory Structure

```
easy_trainer/
├── app/                    # Application
│   ├── easy_trainer.py     # Entry point: projects/datasets, annotation, training/testing
│   ├── core/               # Data layer & common utilities
│   │   ├── db.py           # LMDB data access (YOLO label_ids, rename/merge, ...)
│   │   ├── utils.py        # matplotlib CJK font, QSS loading, project-root lookup
│   │   ├── image_utils.py  # Image loading / thumbnails / format conversion
│   │   ├── label_utils.py  # Label normalization / sorting / colors
│   │   ├── log.py          # Rotating daily logs
│   │   └── keys.py         # LMDB key constants
│   ├── tasks/              # Background tasks (import / merge)
│   │   ├── import_task.py  # Dataset scan & import (detect/segment/classify)
│   │   └── merge_task.py   # Label merging
│   ├── annotation/         # Annotation canvas scene + annotation dialog
│   │   ├── scene.py        # Annotation scene (rect/polygon/format painter)
│   │   ├── view.py         # Canvas view (zoom/pan)
│   │   ├── box_item.py     # Annotation items (boxes + label chips)
│   │   ├── annotation_dialog.py  # Annotation dialog
│   │   └── scene_items.py  # Auxiliary scene items
│   ├── widgets/            # Shared UI widgets
│   │   ├── message_box.py  # Message & progress dialogs
│   │   ├── paginator.py    # Pagination control
│   │   ├── log_dialog.py   # Log viewer dialog
│   │   ├── model_dialog.py # Model management (history, metrics, test, export)
│   │   ├── test_dialog.py  # Test parameter dialog
│   │   └── metrics_dialog.py   # Training metric charts
│   ├── mixins/             # Main-window mixins (projects/datasets/annotation/training/import-export)
│   └── train/              # Training & testing execution
│       ├── train_worker.py # Training subprocess thread (progress/metrics/result signals)
│       ├── train_runner.py # Detect/segment training script (RF-DETR)
│       ├── classify_train_runner.py  # Classification training script (ResNet + per-class accuracy)
│       ├── test_worker.py  # Test subprocess thread
│       ├── test_runner.py  # Detect/segment test script
│       ├── classify_test_runner.py   # Classification test script
│       └── dialogs.py      # Training/testing dialogs
├── ui/                     # PySide6 UI classes (generated from .ui)
├── docs/                   # Design docs + README screenshots
├── resources/              # Icons & resources
├── style/                  # QSS stylesheet
├── requirements.txt
└── README.en.md
```

## 🧭 Workflow

1. **Create a project** → add a dataset under it
2. **Import data**: right-click the dataset → Import. For detection/segmentation pick an image directory + a label directory (labelme/yolo); for classification enable "import by sub-folder"
3. **Annotate**: double-click an image in the dataset to enter the annotation view (rectangle/polygon/format painter), A/D to flip pages, labelme json is saved automatically
4. **Train**: toolbar "Train" → pick task type (detect/segment/classify) → configure parameters → start (5-second countdown, then runs in background)
5. **Test**: Model management → record "Test" → configure → run evaluation
6. **Review metrics**: Model management → "Metrics" opens the accuracy curves
7. **Export model**: Model management → record "Export" produces `project_task_size_scale.pth` + `classes.txt`

> 💡 Training image sizes: detection default **640**, segmentation default **636** (multiple of 12), classification default **224**. Recommended values appear on hover over the input.

## 💾 Data Storage

- **App data**: `~/.easy_trainer/app.mdb` (LMDB — projects/datasets bindings, labels, training history, deleted records, etc.)
- **Training output**: timestamped directories under each task's output path (`config.json` / `result.json` / `metrics.json` / `checkpoint_best.pth` / `classes.txt`)
- **Logs**: `logs/app.log` (rotated daily)

## 📝 Docs

- [Migration plan / design doc](docs/migration_plan.md)
- [User guide](docs/使用教程.pdf)
