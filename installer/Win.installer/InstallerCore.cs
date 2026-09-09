using System.Diagnostics;
using System.IO.Compression;
using System.Net.Http;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Win.installer;

public sealed class Component
{
    public string Id { get; set; } = "";
    public string Title { get; set; } = "";
    public string Desc { get; set; } = "";
    public string File { get; set; } = "";
    public long Size { get; set; }
    public string Sha256 { get; set; } = "";
    public string Url { get; set; } = "";
    public bool Required { get; set; }
    public bool Default { get; set; }

    [JsonIgnore] public bool LocalReady { get; set; }
    [JsonIgnore] public long LocalSize { get; set; }
    [JsonIgnore] public bool OnlineAvailable { get; set; }   // 有在线下载源；无源且本地无文件时 UI 禁止勾选

    // CheckedListBox 渲染时调用 ToString()，没重写就会打印类全名
    public override string ToString() => Title;
}

public sealed class Manifest
{
    public string App { get; set; } = "EasyTrainer";
    public string Version { get; set; } = "";
    public List<Component> Components { get; set; } = new();
}

public sealed class InstallReport
{
    public string Stage { get; init; } = "";
    public string Detail { get; init; } = "";
    public int Pct { get; init; }
}

/// <summary>组件 → 安装目录下的目标位置（program 内嵌解压到根，pretrained 到独立目录）。</summary>
public static class Layout
{
    public static string DestDir(string root, string compId) => compId switch
    {
        "runtime" => Path.Combine(root, "runtime", "python310"),
        "env" => Path.Combine(root, "site-packages"),
        "pretrained" => Path.Combine(root, "pretrained"),
        "program" => root,
        _ => root,
    };
}

/// <summary>下载 + SHA256 校验 + Python 静默安装 + pip 装依赖 + 内嵌解压 + 快捷方式 + 卸载。</summary>
public static class InstallEngine
{
    private static readonly HttpClient Http = new() { Timeout = Timeout.InfiniteTimeSpan };
    // 固定安装顺序：运行时先落地（含 pip 依赖），程序其次，预训练最后
    private static readonly string[] Order = { "runtime", "program", "pretrained" };
    // runtime 阶段含 pip 下载约 2.5GB（torch 为主），进度权重按此估算而非安装器体积
    private const long RuntimeWeight = 2_600L * 1024 * 1024;
    private const string PipIndex = "https://pypi.tuna.tsinghua.edu.cn/simple";
    // Python 运行时下载信息写死（唯一在线源：华为云镜像）。换版本/换源改这里。
    private const string PythonFile = "python-3.10.11-amd64.exe";
    private const string PythonUrl =
        "https://mirrors.huaweicloud.com/python/3.10.11/python-3.10.11-amd64.exe";
    private const string PythonSha256 =
        "D8DEDE5005564B408BA50317108B765ED9C3C510342A598F9FD42681CBE0648B";

    // 预训练权重：rfdetr 按文件名在 RF_HOME(=pretrained/) 根目录精确查找（不分子目录），
    // 文件名必须与 rfdetr 1.9.x 注册名一致。官方 .pth/.pt 仅存 GCS，无国内镜像；
    // 大陆网络若下不动，可改走同目录 pretrained.zip 离线分发。
    private static readonly (string File, string Url, string Sha256)[] PretrainedAssets =
    {
        ("rf-detr-nano.pth",
         "https://storage.googleapis.com/rfdetr/nano_coco/checkpoint_best_regular.pth",
         "D8D6B9EE57D4D0ED2B1F305163624712A0532CB7BCE0C747317984FC5457440D"),
        ("rf-detr-seg-nano.pt",
         "https://storage.googleapis.com/rfdetr/rf-detr-seg-n-ft.pth",
         "A44613A4ECD6B5BA61A62002C600B0B6CB7A9DA2936A45317EC4B62C635FB99B"),
        ("rf-detr-seg-small.pt",
         "https://storage.googleapis.com/rfdetr/rf-detr-seg-s-ft.pth",
         "6DE3DA31B2572CAC214A1C76CCE4A92A13966D56390AC2B3A3DE9A8DC2B2BCA3"),
        ("rf-detr-seg-medium.pt",
         "https://storage.googleapis.com/rfdetr/rf-detr-seg-m-ft.pth",
         "3AD325094735F431AEE9962A8D204D68EB5BFC393D53E7E836E70998FEF5EA58"),
        ("rf-detr-seg-large.pt",
         "https://storage.googleapis.com/rfdetr/rf-detr-seg-l-ft.pth",
         "CA7B7C630BA22496067CC4F034C4E70C8E47FD7ADCEA04C3A49AA8C1755CBE6B"),
    };

    /// <summary>内置组件清单（下载信息写死在代码里，不再依赖外部 manifest.json）。
    /// srcDir 用于探测"离线就绪"：同目录有同名文件则跳过下载直接用。</summary>
    public static Manifest BuiltinManifest(string srcDir)
    {
        var mf = new Manifest
        {
            App = "EasyTrainer",
            Version = "1.0.0",
            Components = new List<Component>
            {
                new()
                {
                    Id = "runtime", Title = "运行时",
                    Desc = "Python 3.10 + torch 等依赖（pip 现场安装）",
                    File = PythonFile, Url = PythonUrl, Sha256 = PythonSha256,
                    Size = 29_037_240, Required = true, Default = true,
                    OnlineAvailable = true,
                },
                new()
                {
                    Id = "pretrained", Title = "预训练权重",
                    Desc = "检测/分割初始权重（在线下载官方源约 880MB；同目录有 pretrained.zip 则离线优先）",
                    File = "pretrained.zip", Required = false,
                    Default = false, OnlineAvailable = true,
                },
            },
        };
        foreach (var c in mf.Components)
        {
            var local = Path.Combine(srcDir, c.File);
            c.LocalReady = File.Exists(local);
            c.LocalSize = c.LocalReady ? new FileInfo(local).Length : 0;
        }
        return mf;
    }

    /// <summary>按固定顺序安装勾选的组件。report.Pct 为全局 0-100。</summary>
    public static async Task InstallAsync(string root, string srcDir, Manifest mf,
        IReadOnlyCollection<string> selectedIds, IProgress<InstallReport> report)
    {
        Directory.CreateDirectory(root);
        var sel = selectedIds.ToHashSet();
        // 程序本体内嵌在安装器里 → 固定必装
        if (HasEmbedded("program.zip"))
            sel.Add("program");
        var todo = Order.Where(sel.Contains).ToList();
        long totalBytes = todo.Sum(id => WeightOf(mf, id));
        if (totalBytes <= 0) totalBytes = todo.Count;

        long doneBytes = 0;
        for (var i = 0; i < todo.Count; i++)
        {
            var id = todo[i];
            var comp = ResolveComponent(mf, id);
            var w = WeightOf(mf, id);
            var stageBase = (int)(100 * doneBytes / totalBytes);
            doneBytes += w;

            switch (id)
            {
                case "runtime":
                    await InstallRuntimeAsync(srcDir, comp, root, report, stageBase, w, totalBytes);
                    break;
                case "pretrained":
                    await InstallPretrainedAsync(srcDir, comp, root, report, stageBase, w, totalBytes);
                    break;
                case "program" when HasEmbedded("program.zip"):
                    var dest = Layout.DestDir(root, id);
                    report.Report(new InstallReport { Stage = comp.Title, Detail = "解压程序本体…", Pct = stageBase + (int)(45 * w / totalBytes) });
                    var entries = await Task.Run(() => ExtractEmbeddedZip("program.zip", dest,
                        s => report.Report(new InstallReport { Stage = comp.Title, Detail = s, Pct = stageBase + 45 + (int)(50 * w / totalBytes) })));
                    report.Report(new InstallReport { Stage = comp.Title, Detail = $"完成（{entries} 个文件）", Pct = stageBase + (int)(100 * w / totalBytes) });
                    break;
                default:
                    await InstallZipComponentAsync(srcDir, comp, root, report, stageBase, w, totalBytes);
                    break;
            }
        }
    }

    private static long WeightOf(Manifest mf, string id)
        => id == "runtime" ? RuntimeWeight : Math.Max(ResolveComponent(mf, id).Size, 1);

    /// <summary>runtime 组件：下载 python 安装器 → 静默装到 runtime\python310 → pip 装依赖。</summary>
    private static async Task InstallRuntimeAsync(string srcDir, Component comp, string root,
        IProgress<InstallReport> report, int stageBase, long w, long totalBytes)
    {
        // 1) 下载 python 安装器（同目录离线包优先，否则 url）
        var exe = await EnsureFileAsync(srcDir, comp, report, stageBase, w);
        if (exe is null)
            throw new InvalidOperationException("Python 安装包缺失: " + comp.Title);
        if (!string.IsNullOrEmpty(comp.Sha256))
        {
            report.Report(new InstallReport { Stage = comp.Title, Detail = "校验文件完整性…", Pct = stageBase + (int)(8 * w / totalBytes) });
            var got = await Task.Run(() => Sha256Of(exe));
            if (!got.Equals(comp.Sha256, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("SHA256 校验失败: " + comp.File);
        }

        // 2) per-user 静默安装（免 UAC）；已装过则跳过（幂等，重跑安装器只补 pip）
        var pyDir = Path.Combine(root, "runtime", "python310");
        var python = Path.Combine(pyDir, "python.exe");
        if (!File.Exists(python))
        {
            if (Directory.Exists(pyDir))
                Directory.Delete(pyDir, recursive: true);
            Directory.CreateDirectory(pyDir);
            report.Report(new InstallReport { Stage = comp.Title, Detail = "正在安装运行时…", Pct = stageBase + (int)(10 * w / totalBytes) });
            var logFile = Path.Combine(pyDir, "python-install.log");
            var psi = new ProcessStartInfo
            {
                FileName = exe,
                UseShellExecute = false,
                CreateNoWindow = true,   // MSI bootstrapper 默认会闪个 cmd 窗口
                Arguments = $"/quiet InstallAllUsers=0 TargetDir=\"{pyDir}\" " +
                            "Include_launcher=0 Include_test=0 Include_doc=0 Include_tcltk=0 " +
                            $"AssociateFiles=0 Shortcuts=0 PrependPath=0 Include_pip=1 /log \"{logFile}\"",
            };
            using (var p = Process.Start(psi))
            {
                if (p is null)
                    throw new InvalidOperationException("无法启动 Python 安装器");
                await p.WaitForExitAsync();
                if (p.ExitCode != 0 && p.ExitCode != 3010)
                    throw new InvalidOperationException($"Python 安装失败（退出码 {p.ExitCode}，日志: {logFile}）");
            }
            if (!File.Exists(python))
                throw new InvalidOperationException("Python 安装成功但找不到 python.exe: " + python);
        }

        // 3) pip 安装依赖（内嵌 requirements.txt，清华镜像）
        var reqPath = Path.Combine(Path.GetTempPath(), "installer", "requirements.txt");
        using (var rs = OpenEmbedded("requirements.txt"))
        {
            if (rs is null)
                throw new InvalidOperationException("安装程序内置缺少 requirements.txt（发布不完整）");
            Directory.CreateDirectory(Path.GetDirectoryName(reqPath)!);
            using var rfs = File.Create(reqPath);
            await rs.CopyToAsync(rfs);
        }

        report.Report(new InstallReport { Stage = comp.Title, Detail = "正在下载安装 Python 依赖（torch 约 2.4GB，视网速 5~30 分钟）…", Pct = stageBase + (int)(12 * w / totalBytes) });
        var logPath = Path.Combine(pyDir, "pip-install.log");
        var sb = new StringBuilder();
        var pip = new ProcessStartInfo
        {
            FileName = python,
            UseShellExecute = false,
            CreateNoWindow = true,   // 不弹黑色控制台窗口（pip 约 30 分钟，让人看到会以为卡住）
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            Arguments = $"-m pip install --disable-pip-version-check -r \"{reqPath}\" -i {PipIndex}",
        };
        using (var p2 = Process.Start(pip))
        {
            if (p2 is null)
                throw new InvalidOperationException("无法启动 pip");
            p2.OutputDataReceived += (_, e) => { if (e.Data is not null) sb.AppendLine(e.Data); };
            p2.ErrorDataReceived += (_, e) => { if (e.Data is not null) sb.AppendLine(e.Data); };
            p2.BeginOutputReadLine();
            p2.BeginErrorReadLine();
            // pip 下载进度不产生整行输出，UI 用心跳推进
            var tick = 12;
            while (!p2.HasExited)
            {
                await Task.Delay(3000);
                if (tick < 85)
                {
                    tick += 1;
                    report.Report(new InstallReport { Stage = comp.Title, Detail = "正在下载安装 Python 依赖…（保持网络连接，请耐心等待）", Pct = stageBase + (int)(tick * w / totalBytes) });
                }
            }
            await p2.WaitForExitAsync();
            if (p2.ExitCode != 0)
            {
                try { File.WriteAllText(logPath, sb.ToString(), Encoding.UTF8); } catch { }
                throw new InvalidOperationException($"pip 安装依赖失败（退出码 {p2.ExitCode}），日志: {logPath}");
            }
        }
        try { File.WriteAllText(logPath, sb.ToString(), Encoding.UTF8); } catch { }
        report.Report(new InstallReport { Stage = comp.Title, Detail = "完成（Python + 依赖已就绪）", Pct = stageBase + (int)(100 * w / totalBytes) });
    }

    /// <summary>pretrained 组件：同目录 pretrained.zip 存在则走通用 zip 解压（离线分发）；
    /// 否则逐个在线下载 5 个权重到 pretrained/（官方 GCS，独立断点续传 + SHA256）。
    /// 单个文件失败只记警告不中断——可选组件，训练时 rfdetr 也能自行补下缺失权重。</summary>
    private static async Task InstallPretrainedAsync(string srcDir, Component comp, string root,
        IProgress<InstallReport> report, int stageBase, long w, long totalBytes)
    {
        if (File.Exists(Path.Combine(srcDir, comp.File)))
        {
            await InstallZipComponentAsync(srcDir, comp, root, report, stageBase, w, totalBytes);
            return;
        }

        var dest = Layout.DestDir(root, comp.Id);
        Directory.CreateDirectory(dest);
        var n = PretrainedAssets.Length;
        var failed = new List<string>();
        for (var i = 0; i < n; i++)
        {
            var (file, url, sha) = PretrainedAssets[i];
            var target = Path.Combine(dest, file);
            var segPct = 100.0 / n * w / totalBytes;
            var segBase = stageBase + (int)(segPct * i);
            try
            {
                if (File.Exists(target) && Sha256Of(target).Equals(sha, StringComparison.OrdinalIgnoreCase))
                {
                    report.Report(new InstallReport { Stage = comp.Title, Detail = file + " 已就绪，跳过", Pct = (int)(segBase + segPct) });
                    continue;
                }
                report.Report(new InstallReport { Stage = comp.Title, Detail = "正在下载 " + file + "…", Pct = segBase });
                await DownloadFileAsync(url, target, sha,
                    (got, total) => report.Report(new InstallReport { Stage = comp.Title,
                        Detail = file + "… " + got / 1_048_576 + "MB", Pct = segBase + (int)(segPct * 0.9 * got / Math.Max(total, 1)) }));
                report.Report(new InstallReport { Stage = comp.Title, Detail = file + " 完成", Pct = (int)(segBase + segPct) });
            }
            catch (Exception ex)
            {
                failed.Add(file + "（" + ex.Message + "）");
            }
        }
        if (failed.Count > 0)
            report.Report(new InstallReport { Stage = comp.Title,
                Detail = "完成，但部分文件下载失败：" + string.Join("；", failed) + "。重跑安装器可续传，或在软件内导入权重目录",
                Pct = stageBase + (int)(100 * w / totalBytes) });
        else
            report.Report(new InstallReport { Stage = comp.Title, Detail = "完成（" + n + " 个权重）", Pct = stageBase + (int)(100 * w / totalBytes) });
    }

    /// <summary>下载到目标文件：.part 断点续传 → SHA256 校验 → 改名就位。校验失败删 .part（避免续传死循环）并抛错。</summary>
    private static async Task DownloadFileAsync(string url, string target, string expectedSha256,
        Action<long, long>? onProgress = null)
    {
        var part = target + ".part";
        var existing = File.Exists(part) ? new FileInfo(part).Length : 0;
        using var req = new HttpRequestMessage(HttpMethod.Get, url);
        if (existing > 0)
            req.Headers.Range = new System.Net.Http.Headers.RangeHeaderValue(existing, null);
        using var resp = await Http.SendAsync(req, HttpCompletionOption.ResponseHeadersRead);
        resp.EnsureSuccessStatusCode();
        var total = (resp.Content.Headers.ContentLength ?? 0) + existing;
        await using (var fs = new FileStream(part, existing > 0 ? FileMode.Append : FileMode.Create, FileAccess.Write))
        {
            await using var stream = await resp.Content.ReadAsStreamAsync();
            var buf = new byte[1 << 20];
            long got = existing;
            int nRead;
            while ((nRead = await stream.ReadAsync(buf)) > 0)
            {
                await fs.WriteAsync(buf.AsMemory(0, nRead));
                got += nRead;
                onProgress?.Invoke(got, total);
            }
        }
        if (!Sha256Of(part).Equals(expectedSha256, StringComparison.OrdinalIgnoreCase))
        {
            try { File.Delete(part); } catch { }
            throw new InvalidDataException("SHA256 校验失败（官方源文件可能已更新，或下载被篡改）");
        }
        if (File.Exists(target)) File.Delete(target);
        File.Move(part, target);
    }

    /// <summary>通用 zip 组件（如离线 pretrained）：下载 → 校验 → 解压。</summary>
    private static async Task InstallZipComponentAsync(string srcDir, Component comp, string root,
        IProgress<InstallReport> report, int stageBase, long w, long totalBytes)
    {
        var zip = await EnsureFileAsync(srcDir, comp, report, stageBase, w);
        if (zip is null)
        {
            // 可选 zip 组件本地缺文件 → 跳过而非抛错：它不该让整个安装失败
            report.Report(new InstallReport { Stage = comp.Title,
                Detail = "跳过：未找到 " + comp.File + "（可选，不影响使用，之后可在软件内导入权重目录）",
                Pct = stageBase + (int)(100 * w / totalBytes) });
            return;
        }

        if (!string.IsNullOrEmpty(comp.Sha256))
        {
            report.Report(new InstallReport { Stage = comp.Title, Detail = "校验文件完整性…", Pct = stageBase + (int)(40 * w / totalBytes) });
            var got = await Task.Run(() => Sha256Of(zip));
            if (!got.Equals(comp.Sha256, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("SHA256 校验失败: " + comp.File);
        }

        var dest = Layout.DestDir(root, comp.Id);
        report.Report(new InstallReport { Stage = comp.Title, Detail = "解压中…", Pct = stageBase + (int)(45 * w / totalBytes) });
        var entries = await Task.Run(() => ExtractAll(zip, dest,
            s => report.Report(new InstallReport { Stage = comp.Title, Detail = s, Pct = stageBase + 45 + (int)(50 * w / totalBytes) })));
        report.Report(new InstallReport { Stage = comp.Title, Detail = $"完成（{entries} 个文件）", Pct = stageBase + (int)(100 * w / totalBytes) });
    }

    /// <summary>按 id 取组件；内置清单无 program 条目时用内嵌资源长度构造占位。</summary>
    private static Component ResolveComponent(Manifest mf, string id)
    {
        var c = mf.Components.FirstOrDefault(x => x.Id == id);
        if (c is not null)
            return c;
        if (id == "program")
        {
            using var s = OpenEmbedded("program.zip");
            return new Component
            {
                Id = "program", Title = "程序本体", Desc = "内置",
                File = "program.zip", Size = s?.Length ?? 0,
                LocalReady = s is not null, Required = true,
            };
        }
        throw new InvalidOperationException("清单缺少组件: " + id);
    }

    /// <summary>按资源名取内嵌资源流（csproj LogicalName 嵌入，名可能是短名或全限定名）。</summary>
    private static Stream? OpenEmbedded(string name)
    {
        var asm = Assembly.GetExecutingAssembly();
        var full = asm.GetManifestResourceNames()
            .FirstOrDefault(n => n.EndsWith(name, StringComparison.OrdinalIgnoreCase));
        return full is null ? null : asm.GetManifestResourceStream(full);
    }

    public static bool HasEmbedded(string name) => OpenEmbedded(name) is not null;

    /// <summary>本地文件不在安装器同目录时，按组件 url 下载到 %TEMP% 缓存（断点续传）。</summary>
    private static async Task<string?> EnsureFileAsync(string srcDir, Component comp,
        IProgress<InstallReport> report, int stageBase, long weightTotal)
    {
        var local = Path.Combine(srcDir, comp.File);
        if (File.Exists(local))
            return local;

        if (string.IsNullOrEmpty(comp.Url))
            return null;

        var cacheDir = Path.Combine(Path.GetTempPath(), "installer");
        Directory.CreateDirectory(cacheDir);
        var target = Path.Combine(cacheDir, comp.File);
        var part = target + ".part";

        report.Report(new InstallReport { Stage = comp.Title, Detail = "下载中…", Pct = stageBase + (int)(30 * weightTotal / 100) });

        var existing = File.Exists(part) ? new FileInfo(part).Length : 0;
        using var req = new HttpRequestMessage(HttpMethod.Get, comp.Url);
        if (existing > 0)
            req.Headers.Range = new System.Net.Http.Headers.RangeHeaderValue(existing, null);
        using var resp = await Http.SendAsync(req, HttpCompletionOption.ResponseHeadersRead);
        resp.EnsureSuccessStatusCode();
        var total = (resp.Content.Headers.ContentLength ?? 0) + existing;

        await using (var fs = new FileStream(part, existing > 0 ? FileMode.Append : FileMode.Create, FileAccess.Write))
        {
            await using var stream = await resp.Content.ReadAsStreamAsync();
            var buf = new byte[1 << 20];
            long got = existing;
            int n;
            while ((n = await stream.ReadAsync(buf)) > 0)
            {
                await fs.WriteAsync(buf.AsMemory(0, n));
                got += n;
                report.Report(new InstallReport { Stage = comp.Title, Detail = $"下载中… {got / 1_048_576}MB", Pct = stageBase + (int)(30 * weightTotal / 100) });
            }
        }
        if (File.Exists(target)) File.Delete(target);
        File.Move(part, target);
        return target;
    }

    /// <summary>逐条解压本地 zip（覆盖旧文件），返回解压条目数。</summary>
    private static int ExtractAll(string zip, string destDir, Action<string> progress)
    {
        using var za = ZipFile.OpenRead(zip);
        return ExtractZipArchive(za, destDir, progress);
    }

    /// <summary>解压程序集内嵌的 zip（program.zip），同上语义。</summary>
    private static int ExtractEmbeddedZip(string name, string destDir, Action<string> progress)
    {
        using var s = OpenEmbedded(name) ??
            throw new InvalidOperationException("程序内置资源缺失: " + name);
        using var za = new ZipArchive(s);
        return ExtractZipArchive(za, destDir, progress);
    }

    /// <summary>逐条解压（覆盖旧文件），防 zip slip。</summary>
    private static int ExtractZipArchive(ZipArchive za, string destDir, Action<string> progress)
    {
        Directory.CreateDirectory(destDir);
        var fullDest = Path.GetFullPath(destDir);
        var count = 0;
        foreach (var e in za.Entries)
        {
            if (e.FullName.EndsWith("/") || string.IsNullOrEmpty(e.Name))
                continue;
            var target = Path.GetFullPath(Path.Combine(destDir, e.FullName));
            if (!target.StartsWith(fullDest, StringComparison.OrdinalIgnoreCase))
                continue; // zip slip 防护
            Directory.CreateDirectory(Path.GetDirectoryName(target)!);
            e.ExtractToFile(target, overwrite: true);
            if (++count % 500 == 0)
                progress($"已解压 {count} 项…");
        }
        return count;
    }

    /// <summary>桌面 + 开始菜单各建一个 EasyTrainer 快捷方式，直接指向 pythonw 跑入口脚本
    /// （无需中间 launcher；PYTHONPATH 由 easy_trainer.py 文件头自行 append，
    /// RF_HOME 由其在 pretrained 存在时 setdefault）。</summary>
    public static void CreateShortcuts(string root)
    {
        var pyDir = Path.Combine(root, "runtime", "python310");
        var pythonw = Path.Combine(pyDir, "pythonw.exe");
        if (!File.Exists(pythonw))
            pythonw = Path.Combine(pyDir, "python.exe");
        if (!File.Exists(pythonw))
            return; // 没装 runtime（如只装了 program 的调试场景）就不建快捷方式
        var script = Path.Combine(root, "app", "easy_trainer.py");
        var icon = Path.Combine(root, "resources", "favicon.ico");
        var iconLoc = File.Exists(icon) ? $"{icon},0" : "";
        var desktop = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
        var startMenu = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Programs), "EasyTrainer");
        Directory.CreateDirectory(startMenu);

        MakeLnk(Path.Combine(desktop, "EasyTrainer.lnk"), pythonw, root, script, iconLoc);
        MakeLnk(Path.Combine(startMenu, "EasyTrainer.lnk"), pythonw, root, script, iconLoc);
    }

    private static void MakeLnk(string lnkPath, string target, string workDir, string script, string iconLoc)
    {
        try
        {
            var shell = Activator.CreateInstance(Type.GetTypeFromProgID("WScript.Shell")!)!;
            dynamic lnk = shell.GetType().InvokeMember("CreateShortcut",
                System.Reflection.BindingFlags.InvokeMethod, null, shell, new object?[] { lnkPath })!;
            lnk.TargetPath = target;
            lnk.Arguments = "\"" + script + "\"";
            lnk.WorkingDirectory = workDir;
            lnk.Description = "EasyTrainer 标注/训练工具";
            if (iconLoc.Length > 0) lnk.IconLocation = iconLoc;
            lnk.Save();
        }
        catch
        {
            // 快捷方式创建失败不阻断安装
        }
    }

    public static void WriteInstalled(string root, Manifest mf, IReadOnlyCollection<string> ids)
    {
        var info = new
        {
            mf.App,
            mf.Version,
            installedAt = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
            components = Order.Where(ids.Contains).ToArray(),
        };
        File.WriteAllText(Path.Combine(root, "installed.json"),
            JsonSerializer.Serialize(info, new JsonSerializerOptions { WriteIndented = true }));
    }

    public static bool IsInstalledRoot(string root)
        => File.Exists(Path.Combine(root, "installed.json"));

    /// <summary>删除安装目录与两个快捷方式（先确认目录确实是安装根）。</summary>
    public static void Uninstall(string root)
    {
        var desktop = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory), "EasyTrainer.lnk");
        var startMenu = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Programs), "EasyTrainer", "EasyTrainer.lnk");
        foreach (var f in new[] { desktop, startMenu })
        {
            try { if (File.Exists(f)) File.Delete(f); } catch { }
        }
        var startDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Programs), "EasyTrainer");
        try { if (Directory.Exists(startDir) && !Directory.EnumerateFileSystemEntries(startDir).Any()) Directory.Delete(startDir); } catch { }
        try { if (Directory.Exists(root)) Directory.Delete(root, recursive: true); } catch { }
    }

    private static string Sha256Of(string path)
    {
        using var fs = File.OpenRead(path);
        using var sha = SHA256.Create();
        return Convert.ToHexString(sha.ComputeHash(fs));
    }
}
