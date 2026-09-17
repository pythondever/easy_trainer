using System.Runtime.InteropServices;
using System.Text;

namespace Win.deploy;

public sealed class IrResult
{
    public bool Ok { get; set; }
    public string XmlPath { get; set; } = "";
    public long XmlBytes { get; set; }
    public long BinBytes { get; set; }
    public double Seconds { get; set; }
    public string RuntimeVersion { get; set; } = "";
    public List<string> Io { get; } = new();
    public string Error { get; set; } = "";
}

/// <summary>
/// onnx -> OpenVINO IR(.xml + .bin). OpenVINO 的 C API 里没有序列化接口(只有绑定设备的
/// compiled blob), 所以走自编的 C++ 桥接 ovbridge.dll. 与 TensorRT 那条路的关键区别:
/// IR 不绑显卡架构, 转换期既不需要 GPU 也不需要任何设备插件, 中文路径也吃得下.
/// </summary>
public static class OpenVinoConverter
{
    private const string Bridge = "ovbridge";
    private const int ErrCap = 8192;
    private const int BufCap = 32768;

    [DllImport(Bridge, CharSet = CharSet.Unicode, CallingConvention = CallingConvention.Cdecl)]
    private static extern int ovbridge_version(StringBuilder buf, int cap);

    [DllImport(Bridge, CharSet = CharSet.Unicode, CallingConvention = CallingConvention.Cdecl)]
    private static extern int ovbridge_selfcheck(StringBuilder err, int errCap);

    [DllImport(Bridge, CharSet = CharSet.Unicode, CallingConvention = CallingConvention.Cdecl)]
    private static extern int ovbridge_describe(string onnx, StringBuilder buf, int cap,
        StringBuilder err, int errCap);

    [DllImport(Bridge, CharSet = CharSet.Unicode, CallingConvention = CallingConvention.Cdecl)]
    private static extern int ovbridge_convert(string onnx, string xml, int fp16,
        StringBuilder err, int errCap);

    private static readonly string LoadError;
    private static string _version = "";

    static OpenVinoConverter() => LoadError = Preload();

    /// <summary>
    /// 单文件发布时这几个 dll 被解到同一个临时目录, 但 Windows 加载 openvino.dll 时只会去
    /// exe 目录/System32/PATH 找它的依赖 tbb12, 不会看它自己在哪个目录 —— 所以按顺序全路径
    /// 预加载一遍, 之后 ovbridge 的静态导入直接复用已加载的模块. 返回空串表示就绪.
    /// </summary>
    private static string Preload()
    {
        try
        {
            var dir = NativeDir();
            foreach (var name in new[] { "tbb12.dll", "openvino.dll", "openvino_onnx_frontend.dll", "ovbridge.dll" })
            {
                var path = Path.Combine(dir, name);
                if (!File.Exists(path))
                    return $"缺少 {name} (找遍了 {dir} 与各搜索目录)";
                NativeLibrary.Load(path);
            }
            return "";
        }
        catch (Exception ex)
        {
            // 这三个 dll 是动态 CRT(与自编的 ovbridge 一样), 缺运行库时抛的是加载失败,
            // 消息里只有系统错误码, 不点出来根本猜不到要装什么
            return ex.Message + CrtHint();
        }
    }

    /// <summary>试探 MSVC 运行库能不能加载, 能就返回空串.</summary>
    private static string CrtHint()
    {
        try
        {
            NativeLibrary.Load("msvcp140.dll");
            NativeLibrary.Load("vcruntime140.dll");
            return "";
        }
        catch
        {
            return " —— 多半是缺 Microsoft Visual C++ 2015-2022 x64 运行库, 装 vc_redist.x64.exe";
        }
    }

    private static string NativeDir()
    {
        if (!string.IsNullOrEmpty(_nativeDir)) return _nativeDir;
        var dirs = AppContext.GetData("NATIVE_DLL_SEARCH_DIRECTORIES") as string ?? "";
        foreach (var d in dirs.Split(Path.PathSeparator, StringSplitOptions.RemoveEmptyEntries))
        {
            if (File.Exists(Path.Combine(d, "ovbridge.dll"))) return _nativeDir = d;
        }
        return _nativeDir = AppContext.BaseDirectory;
    }

    private static string _nativeDir = "";

    /// <summary>空串表示就绪; 否则是拿不到原因.</summary>
    public static string Ready() => LoadError;

    public static string Version()
    {
        if (_version.Length > 0) return _version;
        if (LoadError.Length > 0) return "(未加载)";
        try
        {
            var buf = new StringBuilder(BufCap);
            return _version = ovbridge_version(buf, BufCap) == 0 ? buf.ToString() : "(读不到版本)";
        }
        catch (Exception ex) { return "(读不到版本: " + ex.Message + ")"; }
    }

    /// <summary>加载自检: 逐个导出接口跑一遍, 让 --probe 能在转换前发现运行库缺失. 空串表示通过.</summary>
    public static string SelfCheck()
    {
        if (LoadError.Length > 0) return LoadError;
        try
        {
            var err = new StringBuilder(ErrCap);
            var rc = ovbridge_selfcheck(err, ErrCap);
            return rc == 0 ? "" : err.ToString().Trim();
        }
        catch (Exception ex) { return ex.Message; }
    }

    public static IrResult Run(string onnx, string xmlPath, bool fp16, Action<string> log)
    {
        var result = new IrResult { XmlPath = xmlPath };
        if (LoadError.Length > 0) return Fail(result, "OpenVINO 运行时不可用: " + LoadError);
        if (!File.Exists(onnx)) return Fail(result, "找不到 onnx 文件: " + onnx);
        var len = new FileInfo(onnx).Length;
        if (len == 0) return Fail(result, "onnx 文件是空的: " + onnx);
        log($"输入: {Path.GetFileName(onnx)} ({len / 1048576.0:0.#} MB)");

        try
        {
            var dir = Path.GetDirectoryName(xmlPath);
            if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);
        }
        catch (Exception ex)
        {
            return Fail(result, $"输出目录建不了: {Path.GetDirectoryName(xmlPath)} ({ex.Message})");
        }

        // 先空读一遍: 形状直接显示在日志里, 而且这一步失败时消息比转换失败更容易定位
        var io = new StringBuilder(BufCap);
        var err = new StringBuilder(ErrCap);
        if (ovbridge_describe(onnx, io, BufCap, err, ErrCap) != 0)
            return Fail(result, "读 onnx 失败: " + err.ToString().Trim() + HintFor(err.ToString()));
        foreach (var line in io.ToString().Split('\n', StringSplitOptions.RemoveEmptyEntries))
            result.Io.Add(line.TrimEnd('\r'));
        foreach (var line in result.Io) log("  " + line);

        result.RuntimeVersion = Version();
        log($"OpenVINO {result.RuntimeVersion}, 精度 {(fp16 ? "FP16 (权重压缩)" : "FP32")}");

        // 临时名保留 .xml 后缀: OpenVINO 按扩展名分发序列化器, 拿 .tmp 结尾的路径会直接拒绝
        var tmp = xmlPath + ".tmp.xml";
        try { if (File.Exists(tmp)) File.Delete(tmp); } catch { }
        try { if (File.Exists(BinOf(tmp))) File.Delete(BinOf(tmp)); } catch { }

        try
        {
            err.Clear();
            var t0 = DateTime.UtcNow;
            if (ovbridge_convert(onnx, tmp, fp16 ? 1 : 0, err, ErrCap) != 0)
                return Fail(result, "转换失败: " + err.ToString().Trim() + HintFor(err.ToString()));
            result.Seconds = DateTime.UtcNow.Subtract(t0).TotalSeconds;

            if (!File.Exists(tmp)) return Fail(result, "转换返回成功但没有产物: " + tmp);
            result.XmlBytes = new FileInfo(tmp).Length;
            result.BinBytes = File.Exists(BinOf(tmp)) ? new FileInfo(BinOf(tmp)).Length : 0;

            if (File.Exists(xmlPath)) File.Delete(xmlPath);
            if (File.Exists(BinOf(xmlPath))) File.Delete(BinOf(xmlPath));
            File.Move(tmp, xmlPath);
            if (result.BinBytes > 0) File.Move(BinOf(tmp), BinOf(xmlPath));

            result.Ok = true;
            return result;
        }
        catch (Exception ex)
        {
            return Fail(result, ex.Message + HintFor(ex.Message));
        }
        finally
        {
            // 成功时临时文件已被改名搬走, 这里的清理只对失败路径生效
            try { if (File.Exists(tmp)) File.Delete(tmp); } catch { }
            try { if (File.Exists(BinOf(tmp))) File.Delete(BinOf(tmp)); } catch { }
        }
    }

    private static string BinOf(string xml) => Path.ChangeExtension(xml, ".bin");

    private static IrResult Fail(IrResult r, string message)
    {
        r.Ok = false;
        r.Error = message;
        return r;
    }

    /// <summary>
    /// OpenVINO 的报错是英文的, 且术语按它内部的叫法说. 现场看到英文只会来问,
    /// 这里给最常见的几种接一句中文.
    /// </summary>
    private static string HintFor(string message)
    {
        if (message.Contains("Can't parse") || message.Contains("can't be parsed")
            || message.Contains("Model can't be parsed") || message.Contains("ParseFromIstream"))
            return "\n—— onnx 文件不完整或已损坏, 重新导出或重新拷一份";
        if (message.Contains("Could not open the file"))
            return "\n—— 文件不存在或路径读不到; 模型是外部数据格式时, 同目录的 .onnx.data 也要一起带上";
        if (message.Contains("Failed to import initializer") || message.Contains("Initializer"))
            return "\n—— 模型是外部数据格式(权重不在 onnx 里), 需要把同名的 .data 文件与原 onnx 放在同一目录一起提供";
        if (message.Contains("could not find") && message.Contains("op"))
            return "\n—— onnx 里用到了 OpenVINO 不认识的算子, 换个 opset 重新导出试试";
        return "";
    }
}
