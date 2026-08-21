# EasyTrainer 代码库迁移规划

> 2026-08-06 | 从 D:\code\easy2yolo（旧库）迁移到 D:\code\easy_trainer\easy_trainer（新库）
> 技术栈：PySide6 + Qt Designer（.ui 为设计器真源，pyside6-uic 生成 .py）

## 一、目标目录结构

```
easy_trainer/
├── app/                      # 业务逻辑层（不依赖 ui 生成物）
│   ├── __init__.py
│   ├── app.py                # 主窗口类 App(QWidget, Ui_AppUI) + 入口
│   ├── db.py                 # 数据层（迁移自旧 app/db.py）
│   ├── utils.py              # 通用工具：分页/主题/密钥/路径
│   ├── annotation/           # 标注逻辑
│   │   ├── editor.py         # 标注编辑器（旧 edit_label.py，自建 UI）
│   │   ├── scene.py          # 画布场景（矩形/多边形绘制）
│   │   ├── box_item.py       # 图形项（矩形+多边形+chip）
│   │   ├── view.py           # 视图（缩放/平移/右键）
│   │   └── label_io.py       # 标注文件读写（json/txt/polygon）
│   ├── train/                # 训练相关
│   │   ├── trainer.py        # 训练启动/日志（旧 trainer.py）
│   │   └── predict.py        # 预测/评估（旧 predict.py）
│   └── dialogs/              # 对话框业务（旧 widget.py 拆分）
│       ├── project_dialog.py # 新建/重命名项目
│       ├── import_dialog.py  # 数据导入
│       ├── train_config_dialog.py # 训练配置
│       ├── eval_dialog.py    # 评估结果
│       ├── dataset_dialog.py # 数据集属性
│       └── common.py         # 消息框/确认框封装
├── ui/                       # Qt Designer 真源（.ui + uic 生成 .py）
│   ├── app.ui / app.py       # 主窗口（已建骨架）
│   └── dialogs/              # 各对话框 .ui
├── resources/                # 图标/图片（顶层，已建）
├── style/                    # QSS 样式（顶层）
├── docs/                     # 文档（本规划 + 控件清单）
├── main.py                   # 启动入口（可选）
└── requirements.txt
```

## 二、旧库 → 新库 功能映射

| 旧库文件 | 行数 | 迁往 | 说明 |
| --- | --- | --- | --- |
| app/main.py | 1009 | app/app.py + dialogs | 主窗口逻辑；对话框拆 dialogs/ |
| app/widget.py | 2350 | app/dialogs/* | 按功能拆 6 个模块 |
| app/edit_label.py | 1114 | app/annotation/editor.py | 标注编辑器（自建 UI） |
| app/annotation/* | 874 | app/annotation/ | scene/box_item/view 直接搬 |
| app/trainer.py | 125 | app/train/trainer.py | 训练 |
| app/predict.py | 252 | app/train/predict.py | 预测/评估 |
| app/db.py | 364 | app/db.py | 数据层 |
| paginator+theme+keys | 128 | app/utils.py | 合并工具模块 |
| resources/* | - | resources/ | 图标直接搬 |
| style.qss | 726 | style/style.qss | 挪顶层（改加载路径） |

## 三、UI 设计清单（设计器逐个建）

| # | .ui | 用途 | 关键 objectName |
| --- | --- | --- | --- |
| 1 | ui/app.ui | 主窗口（QTabWidget） | tabWidget, add_project_btn, project_scroll_area |
| 2 | dialogs/import_data.ui | 数据导入 | 文件夹选择, 标签预览, 开始导入 |
| 3 | dialogs/train_config.ui | 训练参数 | epochs/batch/lr/类别数 |
| 4 | dialogs/dataset_properties.ui | 数据集属性 | 路径+标签分布图 |
| 5 | dialogs/evaluation.ui | 评估结果 | mAP/PR 曲线+指标表 |
| 6 | dialogs/message_dialog.ui | 通用消息 | 图标+文本 |
| 7 | dialogs/enter_name.ui | 新建/重命名 | QLineEdit |
| 8 | dialogs/confirm_dialog.ui | 确认框 | 文本+按钮 |
| 9 | dialogs/check_list.ui | 漏检/过杀列表 | 列表+详情 |

> 标注编辑器保持自建 UI（画布+工具栏+右侧面板），不进设计器

## 四、分阶段实施

### 阶段 0：基础设施
- [x] 目录结构/__init__/ui/app.ui 骨架
- [ ] style/ 挪顶层 + app.py 加载路径修正
- [ ] resources/ 图标搬入

### 阶段 1：数据层+工具（无 UI 依赖，先搬）
- [ ] db.py, utils.py
- [ ] 启动入口 + 冒烟测试（空窗启动）

### 阶段 2：主窗口逻辑
- [ ] 按控件清单设计 app.ui 全部控件
- [ ] 迁移 main.py 逻辑到 app.py
- [ ] 项目 CRUD/数据集列表/缩略图/翻页

### 阶段 3：标注链路
- [ ] editor + scene/box_item/view + label_io
- [ ] 矩形/多边形, json/txt 读写, A/D 切换, 自动保存

### 阶段 4：对话框业务
- [ ] 逐个设计 .ui + 迁移 widget.py
- [ ] 导入/训练配置/数据集属性/评估/消息确认

### 阶段 5：训练链路
- [ ] trainer.py, predict.py
- [ ] 训练启动/日志/评估结果

### 阶段 6：回归验证
- [ ] 对照检查脚本（app 引用控件 vs ui objectName）
- [ ] 全功能回归：导入→标注→训练→评估

## 五、关键约定

1. ui/*.py 永不手改：只改 .ui，pyside6-uic 重新生成
2. objectName 是契约：app 层 self.<objectName> 引用
3. 标注编辑器自建 UI，不进设计器
4. QSS 放 style/ 顶层，app 层统一加载
5. import 全用 PySide6
