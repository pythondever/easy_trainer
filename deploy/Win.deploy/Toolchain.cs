using System.Text.Json;

namespace Win.deploy;

public sealed class ToolchainInfo
{
    public bool Found { get; set; }
    public string Root { get; set; } = "";
    public string Source { get; set; } = "";
    /// <summary>manifest 三层形态(manifest.json + build/ + arch/), 否则是 dll 平铺.</summary>
    public bool Layered { get; set; }
    public string Version { get; set; } = "";
    public string BuildCuda { get; set; } = "";
    public int MinDriver { get; set; }
    public List<string> InstalledArch { get; } = new();
    /// <summary>需要挂进进程 PATH 的绝对目录, 顺序即优先级.</summary>
    public List<string> SearchDirs { get; } = new();
    public List<string> Missing { get; } = new();
    public string Diagnostic { get; set; } = "";
    /// <summary>目录里是否真有工具链的踪迹(manifest 或任一 TRT dll).
    /// exe 所在目录总会被当成候选, 但它通常什么都没有.</summary>
    public bool HasTrace { get; set; }

    public bool Ready => Found && Missing.Count == 0;
    public string DisplayName => Version.Length > 0 ? $"TensorRT {Version}" + (BuildCuda.Length > 0 ? $" / cuda-{BuildCuda}" : "") : "TensorRT";

    /// <summary>同一目录可能既来自 manifest 又来自架构匹配, 只留一份.</summary>
    public void AddSearchDir(string dir)
    {
        if (dir.Length == 0) return;
        var full = dir.TrimEnd('\\');
        if (SearchDirs.Any(d => string.Equals(d.TrimEnd('\\'), full, StringComparison.OrdinalIgnoreCase))) return;
        SearchDirs.Add(dir);
    }

    /// <summary>目标机架构是否已有对应的 builder resource.</summary>
    public bool ArchReady(string sm) => InstalledArch.Contains(sm);
    public bool HasPtxFallback => InstalledArch.Contains("ptx");

    /// <summary>ampere+ 跨架构要求的架构资源: sm80 起每一代 + ptx。nvinfer 会**逐份**按名字加载,
    /// 缺哪份就在构建时报 Unable to load library(实测错误会一份份往前推, 别以为是文件坏了)。
    /// 10.14 实测确认这个集合, sm75 不需要。</summary>
    private static readonly string[] CrossArchNeed = { "sm80", "sm86", "sm89", "sm90", "sm120", "ptx" };

    /// <summary>跨架构是否可用: 上述 6 份齐备, 合计约 2.1 GB.</summary>
    public bool CrossArchReady => CrossArchNeed.All(a => InstalledArch.Contains(a));

    public IReadOnlyList<string> CrossArchMissing
        => CrossArchNeed.Where(a => !InstalledArch.Contains(a)).ToList();
}

/// <summary>
/// 工具链定位与校验. 支持两种形态:
/// ① 分层(manifest.json + build/ + arch/smXX/ + runtime/) —— 与 D:\TensorRT\toolchain 一致;
/// ② 扁平(dll 全在同一个目录) —— 现场最省事的摆法.
/// </summary>
public static class Toolchain
{
    private const string Nvinfer = "nvinfer_10.dll";
    private static readonly string[] BuildFiles = { Nvinfer, "nvinfer_plugin_10.dll", "nvonnxparser_10.dll" };

    public static IEnumerable<(string Root, string Source)> Candidates(string? userDir)
    {
        if (!string.IsNullOrWhiteSpace(userDir)) yield return (userDir, "手动指定");

        var exeDir = AppContext.BaseDirectory.TrimEnd(Path.DirectorySeparatorChar);
        yield return (exeDir, "程序目录");
        yield return (Path.Combine(exeDir, "toolchain"), "内置工具链");
        yield return (Path.Combine(exeDir, "native"), "程序目录 native");

        var env = Environment.GetEnvironmentVariable("EASY_TRAINER_TRT");
        if (!string.IsNullOrWhiteSpace(env)) yield return (env, "环境变量");
    }

    public static ToolchainInfo Resolve(GpuInfo gpu, string? userDir)
    {
        ToolchainInfo? best = null;
        foreach (var (root, source) in Candidates(userDir))
        {
            if (string.IsNullOrWhiteSpace(root) || !Directory.Exists(root)) continue;
            var tc = Inspect(root, source, gpu);
            if (tc.Ready) return tc;
            // 空目录(通常是 exe 目录)不参与报错: 否则架构不匹配时会报"缺 nvinfer_10.dll",
            // 而 dll 其实好好躺在 toolchain\build 里, 真正缺的是目标架构的 builder resource
            if (!tc.HasTrace) continue;
            if (best is null || tc.Missing.Count < best.Missing.Count) best = tc;
        }
        return best ?? new ToolchainInfo { Diagnostic = "未找到 TensorRT 运行时, 请指定工具链目录或把 dll 放到程序目录" };
    }

    private static ToolchainInfo Inspect(string root, string source, GpuInfo gpu)
    {
        var tc = new ToolchainInfo { Found = true, Root = root, Source = source };
        var manifest = Path.Combine(root, "manifest.json");
        if (File.Exists(manifest))
        {
            tc.Layered = true;
            ReadManifest(tc, manifest, gpu);
        }
        else if (File.Exists(Path.Combine(root, "build", Nvinfer)))
        {
            tc.Layered = true;
            tc.AddSearchDir(Path.Combine(root, "build"));
        }
        else
        {
            tc.AddSearchDir(root);
        }

        // 架构一律看文件在不在, 不信 manifest 里的自述: 交付时可能只带了目标机那一份
        var archRoot = Path.Combine(root, "arch");
        foreach (var f in Directory.EnumerateFiles(root, "nvinfer_builder_resource_*_10.dll"))
            AddArch(tc, Path.GetFileName(f));
        if (Directory.Exists(archRoot))
            foreach (var f in Directory.EnumerateFiles(archRoot, "nvinfer_builder_resource_*_10.dll", SearchOption.AllDirectories))
                AddArch(tc, Path.GetFileName(f));

        var missingRoot = tc.SearchDirs.Count > 0 ? tc.SearchDirs[0] : root;
        foreach (var f in BuildFiles)
            if (!File.Exists(Path.Combine(missingRoot, f)))
                tc.Missing.Add(f);

        tc.HasTrace = File.Exists(manifest) || tc.InstalledArch.Count > 0
            || BuildFiles.Any(f => File.Exists(Path.Combine(missingRoot, f)));

        var sm = gpu.Sm;
        if (sm.Length > 0 && !tc.ArchReady(sm))
        {
            if (tc.HasPtxFallback)
                tc.Diagnostic = $"缺少 {sm} 的 builder resource, 只能靠 PTX 回退(构建慢很多)";
            else
                tc.Missing.Add($"nvinfer_builder_resource_{sm}_10.dll");
        }

        // 匹配上的架构目录排最前; 其余架构目录也挂上, 多架构交付时 nvinfer 才按名字找得到对应那份
        if (Directory.Exists(archRoot))
        {
            if (sm.Length > 0) tc.AddSearchDir(Path.Combine(archRoot, sm));
            foreach (var d in Directory.EnumerateDirectories(archRoot)) tc.AddSearchDir(d);
        }
        return tc;
    }

    private static void AddArch(ToolchainInfo tc, string fileName)
    {
        var sm = SmOf(fileName);
        if (sm is not null && !tc.InstalledArch.Contains(sm)) tc.InstalledArch.Add(sm);
    }

    private static void ReadManifest(ToolchainInfo tc, string manifestPath, GpuInfo gpu)
    {
        try
        {
            using var doc = JsonDocument.Parse(File.ReadAllText(manifestPath));
            var r = doc.RootElement;
            tc.Version = Str(r, "version");
            tc.BuildCuda = Str(r, "build_cuda");
            if (r.TryGetProperty("min_driver_windows", out var md) && md.TryGetInt32(out var v)) tc.MinDriver = v;

            if (r.TryGetProperty("layouts", out var layouts)
                && layouts.TryGetProperty("build", out var build)
                && build.TryGetProperty("path_dirs", out var dirs))
            {
                var sm = gpu.Sm;
                foreach (var d in dirs.EnumerateArray())
                {
                    var rel = (d.GetString() ?? "").Replace("/", "\\");
                    if (rel.Contains("<目标机架构>"))
                    {
                        if (sm.Length == 0) continue;
                        rel = rel.Replace("<目标机架构>", sm);
                    }
                    var full = Path.Combine(tc.Root, rel);
                    if (Directory.Exists(full)) tc.AddSearchDir(full);
                }
            }
        }
        catch (Exception ex)
        {
            tc.Diagnostic = "manifest.json 解析失败: " + ex.Message;
        }

        if (tc.SearchDirs.Count == 0) tc.AddSearchDir(Path.Combine(tc.Root, "build"));
    }

    private static string? SmOf(string fileName)
    {
        // nvinfer_builder_resource_sm89_10.dll -> sm89
        var t = fileName.Replace("nvinfer_builder_resource_", "").Replace("_10.dll", "");
        return t.Length > 0 ? t : null;
    }

    private static string Str(JsonElement e, string name)
        => e.TryGetProperty(name, out var v) && v.ValueKind == JsonValueKind.String ? v.GetString() ?? "" : "";

    /// <summary>
    /// 把工具链目录挂到进程 PATH 最前面. 必须在任何 TensorRT 调用之前执行:
    /// nvinfer 是运行期按名字去找 builder resource 的(见 skill 第 7.4 节), 分层形态下架构目录不挂就 0.9s 内失败.
    /// </summary>
    public static void ApplyToProcessPath(IEnumerable<string> dirs)
    {
        var parts = (Environment.GetEnvironmentVariable("PATH") ?? "")
            .Split(';', StringSplitOptions.RemoveEmptyEntries).ToList();
        var insert = new List<string>();
        foreach (var d in dirs)
        {
            var full = Path.GetFullPath(d);
            if (!Directory.Exists(full)) continue;
            if (parts.Any(p => string.Equals(p.TrimEnd('\\'), full.TrimEnd('\\'), StringComparison.OrdinalIgnoreCase)))
                continue;
            insert.Add(full);
        }
        if (insert.Count == 0) return;
        parts.InsertRange(0, insert);
        Environment.SetEnvironmentVariable("PATH", string.Join(";", parts));
    }
}
