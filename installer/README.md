# EasyTrainer 安装器

仿 VS Installer 的组件化分发：C# 写的 `installer.exe` **内置程序本体**
（`program.zip` 以资源形式嵌入 exe），勾选 **运行时** 后联网下载官方
Python 安装器并**现场 pip 安装依赖**（走国内镜像，无需自制 2GB 环境包）；
Python 代码（app/、ui/）由 Cython 编成 .pyd，安装完成直接建桌面/开始菜单
快捷方式指向 `runtime\python310\pythonw.exe app\easy_trainer.py`，无需中间启动器。

## 分发形态

给客户的只有一个文件：`installer.exe`。

```
installer.exe   双击打开 → 勾选 → 联网下载安装
```

| 组件 | 来源 | 方式 |
|---|---|---|
| 程序本体 program | 构建期 csproj 嵌入 exe | 直接解压，**不联网** |
| 运行时 | 官方 python 3.10 embeddable zip（国内镜像） | 下载 → 解压即用（绿色，不写注册表） |
| torch 等依赖 | PyPI 国内镜像（清华）+ torch 专用源 | pip 现场安装（约 2.5GB 下载） |
| 预训练权重 | 官方源（storage.googleapis.com，rfdetr 分发通道） | 下载 5 个 .pth/.pt 到 `pretrained\`（约 880MB） |

Python、pip 依赖是国内可直连的公开地址，**无需自建服务器/OSS**：
- Python：`https://mirrors.huaweicloud.com/python/3.10.11/python-3.10.11-embed-amd64.zip`
- pip 引导：**已内嵌**在 exe 里（`builder\get-pip.py`），不再依赖 bootstrap.pypa.io
- pip 依赖：`https://pypi.tuna.tsinghua.edu.cn/simple`
- torch/torchvision：**上海交大 pytorch 镜像** `https://mirror.sjtu.edu.cn/pytorch-wheels/cu121/`，
  失败自动换官方 `https://download.pytorch.org/whl/cu121`

> **为什么必须额外指定 torch 源**：Windows 上 PyPI 的 `torch` 是 **CPU-only**（wheel 仅 203MB，
> 12 个 `nvidia-*` 依赖全带 `platform_system == "Linux"` 条件，Windows 一条都不装）。要拿到
> CUDA 版必须装 `torch==2.5.1+cu121`，而带 local version 的 wheel 只存在于 pytorch 自己的源里，
> 所以 requirements 锁定 `+cu121` 并用 `--extra-index-url` 叠源。装完后请确认：
> `runtime\python310\python.exe -c "import torch;print(torch.cuda.is_available())"` 应为 True。

Python 走 **embeddable 绿色包**（不装 MSI、不写注册表、不需要卸载）：解压到
`runtime\python310` 后改写 `python310._pth`（开 `import site`，把 `Lib\site-packages`
与安装根 `..\..` 加进 sys.path），pip 装的所有包就在这个目录里，卸载即删除目录。老版本 MSI 装的
运行时会在安装时自动识别（`python310._pth` 缺失）并整套换成绿色包。

**磁盘要求**：装"运行时"需要约 **10GB**（torch cu121 下载 2.4GB + 落地约 9GB），
仅装"程序本体"只要几百 MB。安装器会在开始前按所选组件估算并校验，空间不足直接报错、
不会装一半才发现。

**注意**：预训练权重没有国内镜像（rfdetr 官方仅发布在 Google 存储；HuggingFace 上只有
transformers 格式的 safetensors，rfdetr 包不认），大陆网络下不动时改用离线兜底（见下），
或在软件内"导入权重目录"。

**离线兜底**：把 `python-3.10.11-embed-amd64.zip`（或可选 `pretrained.zip`）放安装器同目录，
安装器检测到同名文件即跳过下载、直接使用。

## 权重清单（唯一数据源）

`builder\pretrained-assets.txt`：`文件名 \t URL \t SHA256`，**C# 安装器、installer.sh、
builder\build.py 三端共用**，改这一处即可换源或添加国内镜像（同一文件名写多行 = 多个候选源，
安装器按顺序尝试）。Python 运行时本身的下载信息仍写死在 `InstallerCore.cs` 常量里。

## 构建步骤（Windows）

1. **一键构建**（需要 cl.exe：开始菜单 → VS 2022 → Developer PowerShell；
   以及 .NET SDK 10）。`builder\build.py` 依次完成：Cython 全量编译 pyd →
   组装 `dist\program` → 打 `dist\program.zip` → 自动 `dotnet publish` 安装器
   （csproj 构建期把 `program.zip` 与 `builder\requirements-release.txt` 嵌进 exe）：

   ```powershell
   cd D:\code\easy_trainer
   pip install cython
   python builder\build.py -t dist\program
   ```

   产物：`dist\release\installer.exe`（发布成功后自动清理 `dist\program\`、
   `dist\program.zip` 与 `build\` 中间产物）。构建只做编译与发布，不碰网络下载——
   权重与 Python 运行时的获取全部交给安装器。

2. **requirements-release.txt**（内嵌，pip 现场安装用）已随仓库维护在
   `builder\requirements-release.txt`——版本锁定自 rf-detr 开发环境；注意国内 PyPI
   镜像对 PySide6 只同步到 6.9.1。

3. **分发**：在线版只发 `dist\release\installer.exe`——勾选运行时从
   华为云下载 Python、从清华源 pip 装依赖，中途网络中断会自动重试（下载 3 次、
   pip 失败则换备用源整体重试一次）。
   权重默认在线拉（官方源在大陆常不可达）；若已自行备好，把 `pretrained.zip`
   与 `installer.exe` 放同目录，安装器会优先用本地 zip 完全不走网络。
   离线/U盘版还可加 `python-3.10.11-embed-amd64.zip`（运行时离线包，
   同目录自动跳过下载）。

## 安装后的目录

```
安装根\
  app\ ui\                  全部 .pyd（__init__.py、easy_trainer.py 明文）
  style\ resources\ examples\
  pretrained\               预训练权重（可选；存在时程序启动自动识别）
  runtime\python310\        完整 Python 3.10（自带 pip，依赖装在 Lib\site-packages）
  installed.json            卸载/升级的依据
```

启动链：桌面/开始菜单快捷方式 → `runtime\python310\pythonw.exe "安装根\app\easy_trainer.py"`。
`PYTHONPATH` 由 easy_trainer.py 文件头自行 append 安装根；`RF_HOME` 在
`安装根\pretrained` 存在时由程序启动早期 setdefault（用户显式设过环境变量则不覆盖）。
训练/测试子进程走 `pythonw.exe -c "…from app.train.*_runner import main; main()"`。
**不能用 `-m`**：打包后 runner 是 pyd，runpy 取不到 code object，会直接报
`No code object available`。安装根由 `-c` 里的 `sys.path.insert` 兜底，另在
`python310._pth` 里也写了 `..\..`（覆盖 DataLoader 派生的孙进程——它们同样是
embeddable 解释器，同样忽略 `PYTHONPATH`）。

## 静默安装（无人值守/CI 验证）

```powershell
installer.exe --install D:\EasyTrainer runtime
# 组件取 runtime / pretrained 逗号组合；安装包须与 exe 同目录（或在线下载）
```

日志写 `安装根\install.log`（pip 详细输出在 `runtime\python310\pip-install.log`），
返回码 0=成功。

## 注意事项

- **pyd 版本锁死**：Python 3.10 cp310 ABI；升级解释器必须重编 pyd。
- **改程序代码要重发安装器**：program.zip 构建期嵌入；程序更新 = 重跑
  `build.py` + `dotnet publish`，重新分发 exe。
- pip 现场安装无断点续传，中途断网重跑安装器即可（已装部分 pip 会跳过/缓存）。
- torch 装完约占 4.3GB + 权重可选 882MB，安装前确认目标盘空间。
- 中文安装路径可用（cv2/PyTorch 均按 UTF-8 处理）；安装器 per-user 安装免 UAC，
  不写系统注册表（Python 本体按用户级安装到安装目录内）。
- 卸载：运行 `installer.exe` → 「卸载…」选择安装根即可。

## Linux 发布

`build.py` 的编译段与组包段跨平台（Cython 产物后缀随系统：Windows → `.pyd`，
Linux → `.so`），因此**在 Linux 机器上跑同一脚本**即可产出 Linux 程序包；
`build.py` 末尾按平台分派发布器：

| 平台 | 发布动作 | 产物目录 |
|---|---|---|
| Windows | `dotnet publish`（现状，program.zip 内嵌 exe） | `dist/release/installer.exe` |
| Linux | 组四件套：`installer.sh` + `program.zip` + `requirements-release.txt` + `pretrained-assets.txt` | `dist/release-linux/` |

```bash
# Linux 构建机（需 gcc + python3.10-dev + cython + setuptools）
python3 builder/build.py -t dist/program
```

**Linux 端客户机安装**（把 `dist/release-linux/` 的文件拷过去后）：

```bash
./installer.sh            # 默认装到 ~/EasyTrainer
./installer.sh -d /opt/easy_trainer -p   # 换目录 + 安装预训练权重(~880MB)
TORCH_INDEX=https://download.pytorch.org/whl/cu121 ./installer.sh   # torch 换源
```

脚本与 Windows 安装器职责对应：校验 python3.10 → 建 venv → 解压 program.zip →
pip 清华源装依赖 → （可选）权重 → 生成桌面启动项 `.desktop`；日志/`installed.json`
同样落在安装根。权重清单与 Windows 端共用 `builder/pretrained-assets.txt`（installer.sh
内置同名表仅作无该文件时的兜底）。

**Linux 特有注意**：
- `.so` 按 cp310 编译，要求客户机 python 恰为 **3.10.x**（Ubuntu 22.04+ 自带）；
  系统为其它版本时用 `PY=/path/to/python3.10 ./installer.sh` 指定。
- requirements 锁的是 `torch==2.5.1+cu121`（与 Windows 一致），该版本只存在于 pytorch 源，
  脚本用 `--extra-index-url` 叠源，默认走上海交大等国内镜像可由 `TORCH_INDEX` 覆盖。
- 预训练权重无国内镜像，大陆网络下不动时同目录放 `pretrained.zip` 走离线。
