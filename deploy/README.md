# 模型转换工具（Deploy）

把训练导出的 `.onnx` 转成 TensorRT `.engine` 或 OpenVINO IR（`.xml` + `.bin`）。
单文件 exe，**目标机不需要装 Python、TensorRT、OpenVINO**。

| 输出格式 | 产物 | 需要什么 | 实测（同一个 116 MB 的 onnx） |
|---|---|---|---|
| TensorRT engine | `<模型名>.engine` | NVIDIA 显卡 + 目标卡架构的 builder resource | 71 s，59 MB |
| OpenVINO IR | `<模型名>.xml` + `<模型名>.bin` | 不挑显卡，转换期不碰 GPU | 0.3 s，1.4 MB + 54 MB |

engine 绑显卡架构与 TensorRT 版本（只有 TensorRT 能加载）；IR 给 OpenVINO 运行时用
（Python / C++），不挑设备。默认 FP16。

## 使用

界面：双击 `deploy.exe`，选 onnx → 选格式 → 选输出目录 → 点转换。
onnx 的输入是**动态尺寸**时用「输入尺寸」那一栏填（只有 engine 需要；IR 保留动态形状，不用填）。

命令行：

```powershell
deploy.exe --probe [--toolchain <目录>]
deploy.exe --convert <model.onnx> [--ir] [--out <目录>] [--fp32] [--cross]
                             [--shapes 输入名:1x3xHxW] [--toolchain <目录>] [--log <文件>]
```

| 参数 | 说明 |
|---|---|
| `--ir` | 转 OpenVINO IR；不加就是 engine |
| `--out` | 输出目录，默认与 onnx 同目录 |
| `--fp32` | 不压 FP16（engine 是算子精度，IR 是权重压缩） |
| `--shapes` | 给动态尺寸的输入指定大小，可重复。`images:1x3x640x640`，也可三段 `images:min,opt,max` |
| `--cross` | engine 跨架构构建，能跑在 sm80 及以上（代价见下） |
| `--toolchain` | 手动指定 TensorRT 工具链目录 |
| `--log` | 把输出同时写进文件 |

返回码：`0` 成功 / `1` 转换失败 / `2` 工具链或显卡不可用 / `3` 缺 VC++ 运行库 / `4` OpenVINO 初始化自检失败。

**发给对方之前，先让他在目标机跑一次 `deploy.exe --probe`**（只读，不装任何东西），
看 `运行时自检`（两个格式都要）与 `已装架构`、`驱动`（只有 engine 要）是否满足下面的门槛。

## 交付

`python deploy\build.py` 出来的 `deploy\release\` 就是完整交付目录，整个拷过去：

```
release\
  deploy.exe                自包含单文件 (57.6 MB)，TensorRT 桥接与 OpenVINO 运行时都在里面
  toolchain\                708 MB，发布时自动装配
    build\nvinfer_10.dll
    build\nvinfer_plugin_10.dll
    build\nvonnxparser_10.dll
    arch\sm89\nvinfer_builder_resource_sm89_10.dll
    manifest.json           只用来在界面上显示版本号
```

`JYPPX.*.dll`、`jyppxtrtbridge.dll`、`openvino.dll`、`openvino_onnx_frontend.dll`、`tbb12.dll`、
`ovbridge.dll` 都已编进 exe，不用单独发，也看不到。`D:\TensorRT\toolchain\` 里的 `runtime\` 与
`trtexec.exe` 不要带（本工具在进程内构建 engine）。

另外把 `D:\OpenVINO\runtime\licensing\` 里的几个许可文件一起给对方（Apache-2.0 要求）。

### 目标机门槛

两条路都躲不掉的：

| 门槛 | 要求 | 本包现状 |
|---|---|---|
| 操作系统 | x64：Windows 11 全系 / Win10 21H2·1809·1607（仅 LTSC·企业版）/ Server 2012 R2–2025 | ✅ 常见现场都覆盖；**Win 7 / 8.1 跑不了** |
| VC++ 运行库 | Microsoft Visual C++ 2015-2022 **x64** | ⚠️ 多数机器已有，缺了两个格式都转不了 |

只有转 engine 才需要的：

| 门槛 | 要求 | 本包现状 |
|---|---|---|
| 显卡与驱动 | NVIDIA 独显，驱动 **≥ r537** | ⚠️ 需现场确认 |
| GPU 架构 | `toolchain\arch\<smXX>\` 里要有目标卡那一份 | ❌ 默认只带 **sm89** |
| 显存 | 构建期要在本机实测算子耗时，nano 级 8 GB 够用 | ✅ |

架构对照：`sm75`=RTX 20 系/T4、`sm80`=A100、`sm86`=RTX 30 系/A10、**`sm89`=RTX 40 系/L4（默认）**、
`sm90`=H100、`sm120`=RTX 50 系。

架构不匹配时程序不会崩：engine 选项整卡灰化、并指出缺哪份 resource，对方还能改转 IR。

**VC++ 运行库**这条容易漏，而且**两个格式都要**：TensorRT 那三个 dll 是静态 CRT 用不着它，但
`jyppxtrtbridge.dll`、`ovbridge.dll`、`openvino.dll`、`tbb12.dll` 都是动态 CRT，缺了直接加载失败。
把 `msvcp140 / vcruntime140` 拷到 exe 旁边或放进 PATH 都**无效**（实测），只有装 **`vc_redist.x64.exe`**
一条路。`--probe` 会直接报出来：engine 侧是 `运行时自检: 失败`（返回码 3），IR 侧是
`IR 转换: 未包含 (…缺 Microsoft Visual C++…)`。

### 换架构重新发布

```powershell
python deploy\build.py --arch sm86
```

各架构 builder resource 体积：sm75 150 / sm80 245 / sm86 230 / sm89 243 / sm90 631 / sm120 360 MB。
换卡时只替换 `arch\<smXX>\` 那一份即可，其余不用重发。

### engine 的使用限制

- 与 TensorRT 版本绑定：部署端必须用同一个 **10.14.1.48** 加载。
- 同 sm 的不同型号可以互相加载（4060 Ti 建的能在 4070/4080/4090/L4 上跑），但可能依赖
  **构建机的 SM 数量**，只能跑在 SM 数 ≥ 构建机的卡上。4060 Ti 是 34 SM，在 40 系里偏低，
  兼容面反而宽；**RTX 4060（24 SM）、笔记本 4050 有起不来的风险**。
- 输入尺寸是构建期定死的，推理时喂别的尺寸会报 shape 不匹配。
- 要多代卡通用就加 `--cross`：构建 3.3× 慢、体积 1.6×、延迟 +8%，并且发布时要带全
  sm80 / sm86 / sm89 / sm90 / sm120 / ptx 六份 resource（约 2.1 GB）。

## 构建

需要 .NET SDK 10。发布用 `deploy\build.py`，一条命令到底：

```powershell
python deploy\build.py            全量发布，产物在 deploy\release\
python deploy\build.py --probe    发布完顺带跑一次环境自检
```

| 需求 | 参数 |
|---|---|
| 换目标机架构 | `--arch sm120` |
| 换工具链来源 | `--trt-dir D:\别处\toolchain` |
| 不装配 TensorRT 运行时（只留 IR） | `--no-trt` |
| 换 OpenVINO 运行时来源 | `--ov-dir D:\别处\runtime` |
| 不打包 IR 转换 | `--no-ov` |
| 换输出目录 | `--out D:\某处` |
| 强制重编桥接 | `--bridge` |

脚本在发布前后会自己做完这些：检查 dotnet 与两个运行时目录是否齐、`ovbridge.cpp` 有改动就重编桥接、
先结束正在跑的 `deploy.exe`（否则发布产物被占用会失败）、清掉上次留下的其他架构 resource、
发布完核对 `release\` 的文件数、体积并列出最终构成。

它内部就是调下面这条命令，参数与上表一一对应：

```powershell
dotnet publish deploy\Win.deploy\Win.deploy.csproj -c Release -p:PublishProfile=win-x64
```

| 手动发布参数 | 说明 |
|---|---|
| `-p:TrtArch=sm120` | 目标机架构 |
| `-p:TrtToolchainDir=D:\别处\toolchain` | 换工具链来源 |
| `-p:TrtSkip=1` | 不装配 TensorRT 运行时 |
| `-p:OvRuntimeDir=D:\别处\runtime` | 换 OpenVINO 运行时来源 |
| `-p:OvSkip=1` | 不打包 IR 转换 |

日常编译（只出 8 个文件，与 installer 一个形态）：

```powershell
dotnet build deploy\Win.deploy\Win.deploy.csproj -c Release
```

自包含 / 单文件那几个参数只写在 `Properties\PublishProfiles\win-x64.pubxml`，别挪进 csproj。

改了 `deploy\ovbridge\ovbridge.cpp` 要重跑 `deploy\ovbridge\build.cmd` 重新生成 `native\ovbridge.dll`
（需要 VS 2022 的 C++ 生成工具，脚本会自己找 `vcvars64.bat`）。
⚠️ 这个 `.cmd` 的行尾必须是 **CRLF**：LF 行尾时 cmd.exe 会从行中间开始解析，中文注释全被当成命令
（实测），而编辑器默认存 LF。`build.py` 每次调用前会自己检查并改回来，手动跑之前留意一下。

两个本地依赖目录，都来自 `pip install openvino` 的 `site-packages\openvino\`：

| 目录 | 内容 | 用途 |
|---|---|---|
| `D:\OpenVINO\runtime` | `openvino.dll` + `openvino_onnx_frontend.dll` + `tbb12.dll` + `licensing\` | 打包进 exe（`-p:OvRuntimeDir` 的默认值） |
| `D:\OpenVINO\sdk` | `include\` + `libs\openvino.lib` | 编 `ovbridge.dll`（`build.cmd` 的默认值，12 MB） |

## 转换失败排查

### 一、程序起不来 / 探测就不通过

| 现象 | 怎么办 |
|---|---|
| 双击没反应、报缺 dll | 换 Win10 1809+ / Win11；或被杀软拦了，加白名单 |
| `--probe` 报 `未检测到 NVIDIA 显卡` | 装或升级驱动，**≥ r537** |
| `--probe` 报 `缺失文件: nvinfer_builder_resource_smXX_10.dll` | 按 `已装架构` 重新发布（见上） |
| `--probe` 报 `运行时自检: 失败`（返回码 3） | 装 `vc_redist.x64.exe` |
| `--probe` 报 `IR 转换: 未包含 (…)` | exe 里的 OpenVINO 没解压出来（被杀软拦、临时目录没写权限），或同样是缺 VC++ 运行库 |
| `--probe` 报 `IR 转换自检: 失败`（返回码 4） | OpenVINO 初始化失败，先确认上面两条都不是 |

### 二、engine：onnx 解析阶段就失败

| 报错 | 怎么办 |
|---|---|
| `输入的尺寸是动态的, 猜不出来: images 第 2/3 维` | 「输入尺寸」填 `images:1x3x640x640`，或 CLI `--shapes` |
| 同上但只有 `第 0 维` | batch 动态，程序自己按 1 处理，无需干预 |
| `这些输入都是固定尺寸(...), 指定的尺寸用不上` | 去掉该参数；要换尺寸得重新导出 onnx |
| `Failed to import initializer: xxx.weight` | 模型是外部数据格式，把同名的 `.onnx.data` 一起拷过去 |
| `onnx 文件名含中文, 而它又是外部数据格式` | 把 onnx 与 `.data` 都改成英文名 |
| `Plugin not found` | onnx 里带自定义算子（YOLO 导出常带 `trt.plugins` 的 `EfficientNMS_TRT`），导出时去掉 NMS 后处理 |
| `Failed to parse the ONNX model` | 文件损坏或没拷完整，重新导出 / 重拷 |

### 三、engine：构建阶段失败或卡住

| 现象 | 怎么办 |
|---|---|
| 时间从几十秒涨到几分钟甚至更久，日志里有 `Skipping tactic` | **显存不够**，TRT 跳过了需要大显存的策略、用剩下的硬构建。减小输入尺寸 / batch，或换大显存卡 |
| `buildSerializedNetwork returned a null TensorRT object` | 真正原因在它上面几行的 `[TensorRT]` 日志里，往上翻 |
| 输出目录报错 | 目标是只读 / 没权限 / 盘符不存在，换目录 |
| 中文路径 | 不用管：程序会自动中转，能正常转 |

### 四、IR：转换阶段失败

| 报错 | 怎么办 |
|---|---|
| `onnx 文件不完整或已损坏` | 重新导出 / 重拷 |
| `文件不存在或路径读不到` / `Failed to import initializer` | 外部数据格式要把同名的 `.onnx.data` 一起带上 |
| `用到了 OpenVINO 不认识的算子` | 换个 opset 重新导出 |

### 五、engine 转出来了，但对方拿去推理失败

| 现象 | 原因 |
|---|---|
| 加载直接失败 | 架构不符（要用 `--cross`），或 TensorRT 版本不是 10.14.1.48 |
| 在别的卡上起不来 | 构建机 SM 数量偏多，见上文「engine 的使用限制」 |
| 报 shape 不匹配 | engine 的输入尺寸是构建期定死的，喂了别的尺寸 |

## 其他

- 路径带中文也能转：engine 会自动把 onnx 复制到临时目录中转；IR 直接读。
- 单文件 exe 首次启动会把 native 库解压到 `%TEMP%`，杀软可能拦，用户也需要临时目录写权限；
  未签名的 exe 首次运行会被 SmartScreen 拦一次（"更多信息 → 仍要运行"）。
- 工具链默认按顺序找：界面手动指定的目录 > exe 同目录 > exe 同目录下的 `toolchain\`（发布时装配的那份）
  > exe 同目录下的 `native\` > 环境变量 `EASY_TRAINER_TRT`。
  本机自测时注意：以前手动选过目录会记在 `%LOCALAPPDATA%\EasyTrainer Deploy\config.json` 里，
  优先级最高，看起来像内置那份没生效；移开这个文件即可。
- 多卡机器会自动挑**算力最高**的一张定架构（0 号卡常是亮机卡），界面上会标出用了第几张。
