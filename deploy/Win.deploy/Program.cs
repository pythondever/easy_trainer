using System.Text;

namespace Win.deploy;

static class Program
{
    [STAThread]
    static void Main(string[] args)
    {
        try { Console.OutputEncoding = Encoding.UTF8; } catch { }
        if (args.Length > 0 && args[0] == "--probe") Environment.Exit(Cli.Probe(args));
        if (args.Length > 0 && args[0] == "--convert") Environment.Exit(Cli.Convert(args));
        ApplicationConfiguration.Initialize();
        Application.Run(new MainForm());
    }
}

/// <summary>无人值守入口: 部署流水线里批量转 engine, 或 CI 里验证环境.</summary>
internal static class Cli
{
    private static string _logFile = "";
    private static readonly object Lock = new();

    private static void Say(string line)
    {
        lock (Lock)
        {
            Console.WriteLine(line);
            if (_logFile.Length > 0)
            {
                try { File.AppendAllText(_logFile, line + Environment.NewLine, Encoding.UTF8); } catch { }
            }
        }
    }

    /// <summary>多卡时标明选中的是哪张(按算力最高挑, 不是 0 号).</summary>
    private static string DevTag(GpuInfo g)
        => g.DeviceCount > 1 ? $" [第{g.DeviceIndex + 1}/{g.DeviceCount}张, 按算力最高挑]" : "";

    public static int Probe(string[] args)
    {
        Parse(args, out _, out _, out _, out _, out var toolchainDir, out _, out _, out _);
        var gpu = EnvProbe.Probe();
        Say($"显卡      : {(gpu.Available ? $"{gpu.Name} ({gpu.Sm}) x{gpu.DeviceCount}{DevTag(gpu)}" : "未检测到")}");
        Say($"显存      : {gpu.MemoryText}");
        Say($"驱动      : {gpu.DriverVersion} (支持 CUDA {gpu.DriverCudaText}, raw={gpu.DriverCuda})");
        if (gpu.Diagnostic.Length > 0) Say($"显卡诊断  : {gpu.Diagnostic}");

        var tc = Toolchain.Resolve(gpu, toolchainDir);
        Say($"工具链    : found={tc.Found} ready={tc.Ready} {tc.DisplayName} ({tc.Source})");
        Say($"已装架构  : {string.Join(",", tc.InstalledArch)}");
        Say($"搜索目录  : {string.Join(" | ", tc.SearchDirs)}");
        if (tc.Missing.Count > 0) Say($"缺失文件  : {string.Join(", ", tc.Missing)}");
        if (tc.Diagnostic.Length > 0) Say($"工具链诊断: {tc.Diagnostic}");

        // OpenVINO 这条线不碰显卡也不碰工具链: 没有 N 卡照样能转 IR, 所以它的自检要在
        // 工具链断言之前报出来, 否则一台没装 TensorRT 的机器上永远看不到这条信息
        var ov = OpenVinoConverter.Ready();
        if (ov.Length > 0)
            Say($"IR 转换   : 未包含 ({ov})");
        else
        {
            Say($"OpenVINO  : {OpenVinoConverter.Version()}");
            var ovSelf = OpenVinoConverter.SelfCheck();
            Say(ovSelf.Length == 0 ? "IR 转换自检: OK (onnx 前端就绪)" : $"IR 转换自检: 失败 - {ovSelf}");
            if (ovSelf.Length > 0) return 4;
        }
        if (!tc.Ready) return 2;

        // 文件摆对不等于跑得起来: 缺 VC++ 运行库时 4 个 dll 一个不少, 一加载就失败
        Toolchain.ApplyToProcessPath(tc.SearchDirs);
        var self = EngineConverter.SelfCheck();
        if (self.Length > 0)
        {
            Say($"运行时自检: 失败 - {self}");
            Say("  常见原因: 目标机没装 Microsoft Visual C++ 2015-2022 x64 运行库(vc_redist.x64.exe).");
            Say("  把 msvcp140/vcruntime140 拷到 exe 旁边或 PATH 里都没用, 实测依赖只从 System32 找.");
            return 3;
        }
        Say("运行时自检: OK (桥接已加载, TensorRT 版本可读)");
        return 0;
    }

    public static int Convert(string[] args)
    {
        Parse(args, out var onnx, out var outDir, out var fp16, out var cross, out var toolchainDir,
            out _, out var shapes, out var ir);
        if (onnx.Length == 0 || !File.Exists(onnx))
        {
            Say("用法: deploy --convert <model.onnx> [--ir] [--out <目录>] [--fp32] [--cross] [--shapes 输入名:1x3xHxW]");
            Say("      [--toolchain <目录>] [--log <文件>]");
            Say("      --ir = 转 OpenVINO IR(.xml + .bin), 不需要 NVIDIA 显卡与 TensorRT");
            return 1;
        }

        if (outDir.Length == 0) outDir = Path.GetDirectoryName(Path.GetFullPath(onnx)) ?? ".";
        try { Directory.CreateDirectory(outDir); }
        catch (Exception ex)
        {
            // 目录建不了在这里就得拦住: 让它冒出去是未捕获异常, 进程直接崩, 连失败原因都看不到
            Say($"输出目录不可用: {outDir} ({ex.Message})");
            return 1;
        }

        if (ir)
        {
            var name = Path.GetFileNameWithoutExtension(onnx);
            var irRes = OpenVinoConverter.Run(Path.GetFullPath(onnx), Path.Combine(outDir, name + ".xml"), fp16, Say);
            if (!irRes.Ok)
            {
                Say("失败: " + irRes.Error);
                return 1;
            }
            Say($"成功: {name}.xml {irRes.XmlBytes:N0} B + {name}.bin {irRes.BinBytes:N0} B  "
                + $"{irRes.Seconds:0.0}s  OpenVINO {irRes.RuntimeVersion}");
            return 0;
        }

        var gpu = EnvProbe.Probe();
        if (!gpu.Available)
        {
            Say("未检测到 NVIDIA 显卡, 无法构建 engine");
            return 1;
        }
        var tc = Toolchain.Resolve(gpu, toolchainDir);
        Say($"显卡 {gpu.Name} ({gpu.SmLabel}){DevTag(gpu)}, 驱动 {gpu.DriverVersion} (CUDA {gpu.DriverCudaText})");
        if (!tc.Ready)
        {
            Say("工具链不可用: " + (tc.Diagnostic.Length > 0 ? tc.Diagnostic : "缺 " + string.Join(", ", tc.Missing)));
            return 1;
        }
        Say($"工具链 {tc.DisplayName} ({tc.Source}), 搜索目录 {string.Join(" | ", tc.SearchDirs)}");
        Toolchain.ApplyToProcessPath(tc.SearchDirs);

        // 跨架构要 sm80 起每一代 + ptx 的 resource 齐备, 缺了 TRT 只会在构建期抛一句
        // "Unable to load library: ..." —— 这里提前拦掉, 并把该带哪些架构说清楚
        if (cross && !tc.CrossArchReady)
        {
            Say("跨架构(ampere+)要求工具链含 sm80 起每一代 + ptx 的 builder resource, 当前缺: "
                + string.Join(", ", tc.CrossArchMissing));
            Say("发布时用 -p:TrtArch=sm80,sm86,sm89,sm90,sm120,ptx (合计约 2.1 GB), 或去掉 --cross");
            return 1;
        }

        var req = new ConvertRequest
        {
            OnnxPath = Path.GetFullPath(onnx),
            EnginePath = Path.Combine(outDir, Path.GetFileNameWithoutExtension(onnx) + ".engine"),
            Fp16 = fp16,
            CrossArch = cross,
            Shapes = shapes,
        };
        var r = EngineConverter.Run(req, Say);
        if (!r.Ok)
        {
            Say("失败: " + r.Error);
            return 1;
        }
        foreach (var t in r.Tensors) Say("  " + t);
        Say($"成功: {r.EnginePath}  {r.EngineBytes:N0} B  构建 {r.BuildSeconds:0.0}s  TensorRT {r.RuntimeVersion}");
        return 0;
    }

    private static void Parse(string[] args, out string onnx, out string outDir,
        out bool fp16, out bool cross, out string toolchainDir, out string logFile,
        out List<string> shapes, out bool ir)
    {
        onnx = ""; outDir = ""; fp16 = true; cross = false; toolchainDir = ""; logFile = ""; ir = false;
        shapes = new List<string>();
        for (var i = 1; i < args.Length; i++)
        {
            var a = args[i];
            string Next() => i + 1 < args.Length ? args[++i] : "";
            switch (a)
            {
                case "--out": outDir = Next().Trim('"'); break;
                case "--toolchain": toolchainDir = Next().Trim('"'); break;
                case "--log": _logFile = logFile = Next().Trim('"'); break;
                case "--shapes": shapes.Add(Next().Trim('"')); break;
                case "--fp32": fp16 = false; break;
                case "--ir": ir = true; break;
                case "--cross": cross = true; break;
                default:
                    if (!a.StartsWith("--") && onnx.Length == 0) onnx = a.Trim('"');
                    break;
            }
        }
    }
}
