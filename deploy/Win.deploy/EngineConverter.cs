using JYPPX.TensorRtSharp;
using JYPPX.TensorRtSharp.Shared.Interop;

namespace Win.deploy;

public sealed class ConvertRequest
{
    public string OnnxPath { get; set; } = "";
    public string EnginePath { get; set; } = "";
    public bool Fp16 { get; set; } = true;
    /// <summary>跨架构(ampere+): engine 可跑在 sm80 及以上, 代价是构建更慢/体积更大.</summary>
    public bool CrossArch { get; set; }
    /// <summary>
    /// 动态输入的尺寸, 形如 "images:1x3x640x640"; 也可给 min,opt,max 三段
    /// "images:1x3x320x320,1x3x640x640,1x3x1280x1280". 不填时只有 batch 维动态能自动处理.
    /// </summary>
    public IReadOnlyList<string> Shapes { get; set; } = Array.Empty<string>();
}

public sealed class ConvertResult
{
    public bool Ok { get; set; }
    public string EnginePath { get; set; } = "";
    public long EngineBytes { get; set; }
    public double BuildSeconds { get; set; }
    public string RuntimeVersion { get; set; } = "";
    public List<string> Tensors { get; } = new();
    public string Error { get; set; } = "";
}

/// <summary>
/// onnx -> engine. 走 JYPPX 的 C ABI 桥接在进程内建 engine, 不用 trtexec
/// (trtexec 是 developer tool, 许可上不能随产品分发, 见 skill 第 7.3 节).
/// </summary>
public static class EngineConverter
{
    private static readonly TensorRtApiLine Line = TensorRtApiLine.TensorRt10;

    /// <summary>
    /// 只做运行时加载自检: 桥接能不能起来、TensorRT 版本读不读得到.
    /// 文件摆对不等于跑得起来 —— 目标机缺 VC++ 运行库时 dll 一个不少, 一加载就失败;
    /// 让 --probe 提前发现, 免得"探测一切正常, 一转换就报错". 空串表示通过.
    /// </summary>
    public static string SelfCheck()
    {
        try
        {
            using var logger = new TensorRtLogger(Line, new TensorRtLogHandler((_, _) => { }),
                TensorRtLogSeverity.Error);
            var dep = TensorRtEnvironmentProbe.ProbeNativeDependencies(Line);
            if (dep is null || !dep.BridgeInitialized)
                return "TensorRT 桥接加载失败: " + (dep?.BridgeDiagnostic ?? "未知原因");
            if (!TensorRtEnvironmentProbe.TryGetGlobalRuntimeVersion(Line, out var ver, out var diag) || ver is null)
                return "读不到 TensorRT 版本号: " + diag;
            return "";
        }
        catch (Exception ex)
        {
            return ex.Message;
        }
    }

    public static ConvertResult Run(ConvertRequest req, Action<string> log)
    {
        var result = new ConvertResult { EnginePath = req.EnginePath };
        var onnx = req.OnnxPath;
        if (!File.Exists(onnx))
            return Fail(result, "找不到 onnx 文件: " + onnx);
        var len = new FileInfo(onnx).Length;
        if (len == 0)
            return Fail(result, "onnx 文件是空的: " + onnx);
        log($"输入: {Path.GetFileName(onnx)} ({len / 1048576.0:0.#} MB)");
        // 体积判不了真假: 外部数据格式的 .onnx 只存结构, 权重在同目录的 .onnx.data 里,
        // 874 字节的主文件是合法的(实测); 只看首字节, 不像也交给 parser 下结论
        var head = FirstByteOf(onnx);
        if (head != 0x08)
            log($"(注意: 文件首字节是 0x{head:X2}, 而 ONNX 模型通常是 0x08, 仍尝试解析)");

        var emitted = 0;
        var suppressed = 0;
        void Effuse(TensorRtLogSeverity sev, string msg)
        {
            // 回调跑在 native 线程, 抛异常会被桥接记成 CallbackFailure, 再往后日志全丢
            try
            {
                var text = msg.Trim();
                if (text.Length == 0) return;
                if (sev is TensorRtLogSeverity.Error or TensorRtLogSeverity.InternalError)
                {
                    log($"[TensorRT] {text}");
                    return;
                }
                if (Interlocked.Increment(ref emitted) <= 200) log($"[TensorRT] {text}");
                else Interlocked.Increment(ref suppressed);
            }
            catch { }
        }

        try
        {
            var dir = Path.GetDirectoryName(req.EnginePath);
            if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);
        }
        catch (Exception ex)
        {
            return Fail(result, $"输出目录建不了: {Path.GetDirectoryName(req.EnginePath)} ({ex.Message})");
        }

        // nvonnxparser 与 engine 落盘都只认窄字符路径: 路径里带中文会在"文件明明在"的情况下报
        // "Input file cannot be found". 这种时候原生 IO 挪进纯 ASCII 的中转目录, 搬运交给自己做
        var stage = AsciiStageDir(onnx, req.EnginePath, log);
        string? box = null;
        var parsePath = onnx;
        var tmp = req.EnginePath + ".tmp";
        if (stage is not null)
        {
            var origName = Path.GetFileName(onnx);
            var side = ExternalDataFiles(onnx).ToList();
            // 外部数据格式靠相对路径找权重, 文件名动不得; 而 TensorRT 只认窄字符名 ——
            // 两个要求撞上时只能让用户先改名, 硬来会报"找不到权重", 比直接说清楚更难查
            if (!IsAscii(origName) && side.Count > 0)
                return Fail(result, $"onnx 文件名含中文, 而它又是外部数据格式(权重在同目录的 .data 里): "
                                    + "TensorRT 只认窄字符文件名, 改名会让它找不到权重. "
                                    + "请把 onnx 与 .data 都改成英文名后再转");
            box = Path.Combine(stage, Guid.NewGuid().ToString("N"));
            try
            {
                Directory.CreateDirectory(box);
                parsePath = Path.Combine(box, IsAscii(origName)
                    ? origName
                    : Guid.NewGuid().ToString("N") + ".onnx");
                tmp = Path.Combine(box, "out.engine");
                File.Copy(onnx, parsePath, overwrite: true);
                foreach (var f in side)
                    File.Copy(f, Path.Combine(box, Path.GetFileName(f)), overwrite: true);
            }
            catch (Exception ex)
            {
                return Fail(result, "中转文件复制失败: " + ex.Message);
            }
        }
        // 先写临时名再改名: 构建中途失败会在目标路径留下 0 字节残骸, 下次拿它 load 会报
        // "Failed to read header from the stream", 看着像 dll 装错了 (见 skill 第 2.3 节)
        try { if (File.Exists(tmp)) File.Delete(tmp); } catch { }

        try
        {
            using var logger = new TensorRtLogger(Line, new TensorRtLogHandler(Effuse), TensorRtLogSeverity.Info);

            var dep = TensorRtEnvironmentProbe.ProbeNativeDependencies(Line);
            if (dep is null || !dep.BridgeInitialized)
                return Fail(result, "TensorRT 桥接初始化失败: " + (dep?.BridgeDiagnostic ?? "未知原因"));
            if (TensorRtEnvironmentProbe.TryGetGlobalRuntimeVersion(Line, out var ver, out var diag) && ver is not null)
            {
                result.RuntimeVersion = $"{ver.Major}.{ver.Minor}.{ver.Patch}.{ver.Build}";
                log($"TensorRT {result.RuntimeVersion} (inferLib={ver.InferLibVersion}, onnxParser={ver.OnnxParserVersion})");
            }
            else
            {
                log("读不到 TensorRT 版本号: " + diag);
            }

            using var builder = new TensorRtBuilder(logger);
            using var network = builder.CreateNetwork();
            using var config = builder.CreateBuilderConfig();

            var fp16 = req.Fp16;
            if (fp16 && !builder.PlatformHasFastFp16)
            {
                log("该显卡不支持快速 FP16, 自动改用 FP32");
                fp16 = false;
            }
            if (fp16) config.SetFlag(TensorRtBuilderFlag.Fp16, true);
            log($"精度: {(fp16 ? "FP16" : "FP32")}, 平台支持 FP16={builder.PlatformHasFastFp16}");

            if (req.CrossArch)
            {
                config.SetHardwareCompatibilityLevel(TensorRtHardwareCompatibilityLevel.AmperePlus);
                log("跨架构模式: engine 可在 sm80 及以上运行 (构建更慢, 体积更大)");
            }

            using var parser = new TensorRtOnnxParser(logger, network);
            try { parser.SetBuilderConfig(config); }
            catch (Exception) { /* TRT 11 才有的接口, 10.x 上抛 NotSupported, 无碍 */ }

            var t0 = DateTime.UtcNow;
            if (!parser.ParseFromFile(parsePath))
            {
                var summary = string.Join("; ", parser.GetErrors().Select(e => e.ToString()));
                if (summary.Length == 0) summary = parser.GetErrorSummary();
                return Fail(result, "解析 onnx 失败: " + summary + HintFor(summary));
            }
            log($"解析完成 {DateTime.UtcNow.Subtract(t0).TotalSeconds:0.0}s, 开始构建 engine...");

            var shapeError = SetupInputProfiles(builder, network, config, req.Shapes, log);
            if (shapeError is not null) return Fail(result, shapeError);

            var t1 = DateTime.UtcNow;
            using var serialized = builder.BuildSerializedNetwork(network, config);
            result.BuildSeconds = DateTime.UtcNow.Subtract(t1).TotalSeconds;
            log($"构建完成 {result.BuildSeconds:0.0}s, 序列化 {serialized.SizeInBytes / 1048576.0:0.#} MB, 校验中...");

            serialized.SaveToFile(tmp);

            // 产物必须能被反序列化才算成功: 只看构建返回值会被半截 engine 骗过去
            using (var runtime = new TensorRtRuntime(logger))
            using (var engine = runtime.DeserializeFromFile(tmp))
            {
                if (engine is null) return Fail(result, "engine 反序列化失败");
                for (var i = 0; i < engine.IOTensorCount; i++)
                {
                    var info = engine.GetIOTensorInfo(i);
                    if (info is null) continue;
                    var shape = string.Join("x", info.Shape?.Values ?? Array.Empty<int>());
                    var kind = info.IOMode == TensorRtIOMode.Input ? "输入" : "输出";
                    result.Tensors.Add($"{kind} {info.Name} [{shape}] {info.DataType}");
                }
                log($"engine 校验通过: {engine.LayerCount} 层, 显存占用 {engine.DeviceMemorySizeInBytes / 1048576.0:0.#} MB");
            }

            result.EngineBytes = new FileInfo(tmp).Length;
            if (File.Exists(req.EnginePath)) File.Delete(req.EnginePath);
            File.Move(tmp, req.EnginePath);
            result.Ok = true;
            if (suppressed > 0) log($"(另有 {suppressed} 条 TensorRT 日志省略)");
            return result;
        }
        catch (Exception ex)
        {
            return Fail(result, ex.Message + HintFor(ex.Message));
        }
        finally
        {
            // 成功时 tmp 已经被改名搬走, 这里的清理只对失败/提前 return 生效
            if (box is not null) { try { Directory.Delete(box, true); } catch { } }
            try { if (File.Exists(tmp)) File.Delete(tmp); } catch { }
        }
    }

    /// <summary>
    /// 动态输入必须显式挂 optimization profile: 实测缺它时构建期直接抛
    /// "Network has dynamic or shape inputs, but no optimization profile has been defined",
    /// 而桥接把这句原因吞掉, 只留 "buildSerializedNetwork returned a null TensorRT object".
    /// batch 维动态取 1 是明确的; 空间维动态猜不出来, 让用户给尺寸而不是替他猜.
    /// 返回非 null 即失败原因.
    /// </summary>
    private static string? SetupInputProfiles(TensorRtBuilder builder, TensorRtNetworkDefinition network,
        TensorRtBuilderConfig config, IReadOnlyList<string> overrides, Action<string> log)
    {
        var dynamicInputs = new List<(string Name, int[] Dims, int[] At)>();
        var allInputs = new List<(string Name, int[] Dims)>();
        for (var i = 0; i < network.InputCount; i++)
        {
            var t = network.GetInput(i);
            var dims = t?.Shape?.Values;
            if (dims is null || dims.Length == 0) continue;
            var at = Enumerable.Range(0, dims.Length).Where(k => dims[k] < 0).ToArray();
            allInputs.Add((t!.Name, dims.ToArray()));
            if (at.Length > 0) dynamicInputs.Add((t!.Name, dims.ToArray(), at));
        }

        var given = ParseShapes(overrides, out var bad);
        if (bad.Length > 0) return bad;

        if (dynamicInputs.Count == 0)
        {
            // 静默忽略会让用户以为 engine 是按他给的尺寸建的
            if (given.Count > 0)
                return "这些输入都是固定尺寸(" + string.Join("; ", allInputs.Select(x => $"{x.Name} {ShapeText(x.Dims)}"))
                       + "), 指定的尺寸用不上; 要改尺寸请按目标尺寸重新导出 onnx";
            return null;
        }

        var unguessable = new List<string>();
        var notes = new List<string>();
        var profile = builder.CreateOptimizationProfile();   // 归 builder 所有, 不能自己 Dispose
        foreach (var (name, dims, at) in dynamicInputs)
        {
            int[] min, opt, max;
            if (given.TryGetValue(name, out var segs))
            {
                if (segs[0].Length != dims.Length)
                    return $"输入 {name} 是 {dims.Length} 维, 指定的是 {segs[0].Length} 维 ({ShapeText(segs[0])})";
                for (var k = 0; k < dims.Length; k++)
                    if (dims[k] > 0 && segs[0][k] != dims[k])
                        return $"输入 {name} 第 {k} 维固定为 {dims[k]}, 指定的 {segs[0][k]} 对不上";
                if (segs.Length == 3) (min, opt, max) = (segs[0], segs[1], segs[2]);
                else (min, opt, max) = (segs[0], segs[0], segs[0]);
                notes.Add($"{name} {ShapeText(opt)}"
                          + (segs.Length == 3 ? $" (min {ShapeText(min)} / max {ShapeText(max)})" : ""));
            }
            else if (at.Length == 1 && at[0] == 0)
            {
                // 只有 batch 维动态: engine 按单张图构建, 没什么可选的
                var d = (int[])dims.Clone();
                d[0] = 1;
                (min, opt, max) = (d, (int[])d.Clone(), (int[])d.Clone());
                notes.Add($"{name} {ShapeText(d)} (batch 维动态, 按 1 处理)");
            }
            else
            {
                unguessable.Add($"{name} 第 {string.Join("/", at)} 维");
                continue;
            }
            // 必须是 SetShape(=TRT 的 setDimensions): 同名的 SetShapeValues 是给 shape tensor
            // 输入设值的, 用它 profile 里不会落下任何维度, 构建期报
            // "Dynamic input tensor xxx is missing dimensions in profile 0"
            profile.SetShape(name, new TensorRtDims(min), new TensorRtDims(opt), new TensorRtDims(max));
        }

        if (unguessable.Count > 0)
            return "输入的尺寸是动态的, 猜不出来: " + string.Join("; ", unguessable)
                   + " —— 用 --shapes <输入名>:<1x3xHxW> 指定, 或按固定尺寸重新导出 onnx";
        if (!profile.IsValid) return "optimization profile 无效, 指定的尺寸超出模型可接受范围";
        if (config.AddOptimizationProfile(profile) < 0) return "无法把 optimization profile 挂到 builder config";
        foreach (var n in notes) log("动态输入按 " + n + " 构建");
        return null;
    }

    /// <summary>"images:1x3x640x640" 或 "images:min,opt,max" 三段 -> 输入名到尺寸段的映射.</summary>
    private static Dictionary<string, int[][]> ParseShapes(IReadOnlyList<string> items, out string error)
    {
        error = "";
        var map = new Dictionary<string, int[][]>(StringComparer.Ordinal);
        foreach (var raw in items)
        {
            var text = raw.Trim();
            if (text.Length == 0) continue;
            var colon = text.IndexOf(':');
            if (colon <= 0)
            {
                error = $"尺寸要写成 <输入名>:<尺寸>, 例如 images:1x3x640x640, 收到 \"{text}\"";
                return map;
            }
            var name = text[..colon].Trim();
            var segs = new List<int[]>();
            foreach (var part in text[(colon + 1)..].Split(',', StringSplitOptions.RemoveEmptyEntries))
            {
                var items2 = part.Trim().Split('x', 'X');
                var dims = new int[items2.Length];
                for (var i = 0; i < items2.Length; i++)
                    if (!int.TryParse(items2[i], out dims[i]) || dims[i] <= 0)
                    {
                        error = $"尺寸 \"{part}\" 里每一维都要是正整数, 用 x 分隔";
                        return map;
                    }
                segs.Add(dims);
            }
            if (segs.Count is not (1 or 3))
            {
                error = $"输入 {name} 的尺寸要么 1 段(固定), 要么 3 段(min,opt,max), 收到 {segs.Count} 段";
                return map;
            }
            map[name] = segs.ToArray();
        }
        return map;
    }

    private static string ShapeText(IEnumerable<int> dims) => string.Join("x", dims);

    /// <summary>返回纯 ASCII 的中转目录; 路径本来就干净时返回 null, 不白搬一趟.</summary>
    private static string? AsciiStageDir(string onnx, string enginePath, Action<string> log)
    {
        if (IsAscii(Path.GetFullPath(onnx)) && IsAscii(Path.GetFullPath(enginePath))) return null;
        foreach (var d in new[] { Path.GetTempPath(), Path.GetDirectoryName(enginePath) ?? "", AppContext.BaseDirectory })
        {
            if (d.Length == 0) continue;
            var full = Path.GetFullPath(d);
            if (!IsAscii(full)) continue;
            log("路径含非 ASCII 字符, TensorRT 的文件读写改在临时目录进行: " + full);
            return Path.Combine(full, "easy_trainer_deploy");
        }
        log("路径含非 ASCII 字符, 又找不到纯 ASCII 的临时目录, TensorRT 可能报找不到文件");
        return null;
    }

    private static bool IsAscii(string s) => s.All(ch => ch < 128);

    private static byte FirstByteOf(string path)
    {
        try
        {
            using var fs = File.OpenRead(path);
            return (byte)fs.ReadByte();
        }
        catch { return 0; }
    }

    /// <summary>
    /// 外部数据格式(权重与结构分离)的权重文件: 常见命名是 model.onnx.data 或 model.data.
    /// 中转时得跟着搬, 否则 parser 报的是找不到权重而不是路径问题.
    /// </summary>
    private static IEnumerable<string> ExternalDataFiles(string onnx)
    {
        var dir = Path.GetDirectoryName(onnx) ?? "";
        foreach (var name in new[]
                 {
                     Path.GetFileName(onnx) + ".data",
                     Path.GetFileNameWithoutExtension(onnx) + ".data",
                 })
        {
            var p = Path.Combine(dir, name);
            if (File.Exists(p)) yield return p;
        }
    }

    private static ConvertResult Fail(ConvertResult r, string message)
    {
        r.Ok = false;
        r.Error = message;
        return r;
    }

    /// <summary>
    /// TensorRT 的报错全是英文, 而且只说症状不说怎么调. 这里把最常见的几种
    /// 接一句能直接照做的中文提示 (现场对方看到英文只会来问).
    /// </summary>
    private static string HintFor(string message)
    {
        if (message.Contains("Failed to import initializer"))
            return "\n—— 模型是外部数据格式(权重不在 onnx 里), 需要把同名的 .onnx.data 与原 onnx 放在同一目录一起提供";
        if (message.Contains("Plugin not found"))
            return "\n—— onnx 里用到了自定义算子/插件(如 YOLO 导出的 trt.plugins EfficientNMS), 这类模型要用导出时那套插件的 TensorRT 环境构建; 本工具只带官方 dll, 不含插件, 建议导出时去掉 NMS 后处理";
        if (message.Contains("Failed to parse the ONNX model"))
            return "\n—— onnx 文件不完整或已损坏, 重新导出/重新拷一份试试";
        if (message.Contains("null TensorRT object"))
            return "\n—— 具体原因见上方 [TensorRT] 日志, 常见: 显存不够(换小一点的输入尺寸或换个显卡)、算子不支持、onnx 导出环境与 TensorRT 版本不匹配";
        if (message.Contains("could not find any CUDA device") || message.Contains("CUDA initialization"))
            return "\n—— 驱动异常或显卡被独占, 先重启机器/更新驱动";
        return "";
    }
}
