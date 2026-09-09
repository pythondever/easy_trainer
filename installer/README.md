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
| 运行时 | 官方 python 3.10 安装器（国内镜像） | 下载 → 静默安装 |
| torch 等依赖 | PyPI 国内镜像（清华） | pip 现场安装（约 2.5GB） |
| 预训练权重 | 官方源（storage.googleapis.com，rfdetr 分发通道） | 下载 5 个 .pth/.pt 到 `pretrained\`（约 880MB） |

Python、pip 依赖是国内可直连的公开地址，**无需自建服务器/OSS**：
- Python：`https://mirrors.huaweicloud.com/python/3.10.11/python-3.10.11-amd64.exe`
- pip 依赖：`https://pypi.tuna.tsinghua.edu.cn/simple`

**注意**：预训练权重没有国内镜像（rfdetr 官方仅发布在 Google 存储），大陆网络
下不动时改用离线兜底（见下），或在软件内"导入权重目录"。

**离线兜底**：把 `python-3.10.11-amd64.exe`（或可选 `pretrained.zip`）放安装器同目录，
安装器检测到同名文件即跳过下载、直接使用。组件下载信息（地址/SHA256）写死在
`InstallerCore.cs` 常量里，没有外部 manifest.json。

## 构建步骤（Windows）

1. **一键构建**（需要 cl.exe：开始菜单 → VS 2022 → Developer PowerShell；
   以及 .NET SDK 10）。`build.py` 依次完成：Cython 全量编译 pyd →
   组装 `dist\program` → 打 `dist\program.zip` → 自动 `dotnet publish` 安装器
   （csproj 构建期把 `program.zip` 与 `build\requirements-release.txt` 嵌进 exe）：

   ```powershell
   cd D:\code\easy_trainer
   pip install cython
   python build\build.py -t dist\program        # 完整发布
   python build\build.py -t dist\program --no-publish   # 只编 pyd，跳过安装器
   ```

   产物：`dist\release\installer.exe`（发布成功后自动清理 `dist\program\` 与
   `dist\program.zip` 中间产物；`--no-publish` 时保留供检查）。

2. **requirements-release.txt**（内嵌，pip 现场安装用）已随仓库维护在
   `build\requirements-release.txt`——版本锁定自 rf-detr 开发环境；注意国内 PyPI
   镜像对 PySide6 只同步到 6.9.1。

3. **分发**：在线版只发 `dist\release\installer.exe`——勾选运行时从
   华为云下载 Python、从清华源 pip 装依赖；勾选预训练权重则从官方源下载 5 个权重
   （约 880MB，大陆网络受限时可能失败，见上文注意）。离线/U盘版把以下文件放同一目录：
   `python-3.10.11-amd64.exe`（运行时离线包，与安装器同目录自动跳过下载）、
   `pretrained.zip`（可选，预训练权重，把 `~\.roboflow\models` 目录内容压成 zip 即可）。

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
训练/测试子进程走 `pythonw.exe -m app.train.*_runner`（worker 已按模块名调用，
cwd=安装根，因此 pyd 化后不受影响）。

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
