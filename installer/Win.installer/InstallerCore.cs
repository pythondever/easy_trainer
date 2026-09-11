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
    [JsonIgnore] public bool OnlineAvailable { get; set; }
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

public static class InstallEngine
{
    private static readonly HttpClient Http = new() { Timeout = Timeout.InfiniteTimeSpan };
    // 固定安装顺序：运行时先落地(含 pip 依赖),程序其次,预训练最后
    private static readonly string[] Order = { "runtime", "program", "pretrained" };
    // runtime 阶段含 pip 下载约 2.5GB(torch 为主),进度权重按此估算而非安装器体积
    private const long RuntimeWeight = 2_600L * 1024 * 1024;
    private const string PipIndex = "https://pypi.tuna.tsinghua.edu.cn/simple";
    private const string PythonFile = "python-3.10.11-embed-amd64.zip";
    private const string PythonUrl =
        "https://mirrors.huaweicloud.com/python/3.10.11/python-3.10.11-embed-amd64.zip";
    private const string PythonSha256 =
        "608619F8619075629C9C69F361352A0DA6ED7E62F83A0E19C63E0EA32EB7629D";
    private const string PipBootstrapUrl = "https://bootstrap.pypa.io/get-pip.py";
    private static readonly string[] TorchIndexUrls =
    {
        "https://mirror.sjtu.edu.cn/pytorch-wheels/cu121/",   // 上海交大
        "https://download.pytorch.org/whl/cu121",             // 官方兜底
    };
    private const long RuntimeInstalledBytes = 9L * 1024 * 1024 * 1024;
    private const int DownloadAttempts = 3;
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
                    Desc = "运行时 + 深度学习 等依赖",
                    File = PythonFile, Url = PythonUrl, Sha256 = PythonSha256,
                    Size = 8_629_277, Required = true, Default = true,
                    OnlineAvailable = true,
                },
                new()
                {
                    Id = "pretrained", Title = "预训练权重",
                    Desc = "检测/分割初始权重(同目录有 pretrained.zip 则离线优先)",
                    File = "pretrained.zip", Required = false,
                    Size = 922_746_880, Default = false, OnlineAvailable = true,
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

    public static async Task InstallAsync(string root, string srcDir, Manifest mf,
        IReadOnlyCollection<string> selectedIds, IProgress<InstallReport> report)
    {
        Directory.CreateDirectory(root);
        var sel = selectedIds.ToHashSet();
        if (HasEmbedded("program.zip"))
            sel.Add("program");
        var todo = Order.Where(sel.Contains).ToList();
        long totalBytes = todo.Sum(id => WeightOf(mf, id));
        if (totalBytes <= 0) totalBytes = todo.Count;
        var needBytes = todo.Sum(id => Math.Max(ResolveComponent(mf, id).Size, 0))
                      + (todo.Contains("runtime") ? RuntimeInstalledBytes : 0);
        var freeBytes = FreeBytesOf(root);
        if (freeBytes >= 0 && freeBytes < needBytes)
            throw new InvalidOperationException(
                $"磁盘空间不足:本次安装需要约 {Gb(needBytes)},安装盘当前可用 {Gb(freeBytes)}。" +
                Environment.NewLine + "请更换空间充足的目录,或清理磁盘后重试。");

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
                    report.Report(new InstallReport { Stage = comp.Title, Detail = "正在安装…", Pct = stageBase + (int)(45 * w / totalBytes) });
                    await Task.Run(() => ExtractEmbeddedZip("program.zip", dest,
                        s => report.Report(new InstallReport { Stage = comp.Title, Pct = stageBase + 45 + (int)(50 * w / totalBytes) })));
                    report.Report(new InstallReport { Stage = comp.Title, Detail = "完成", Pct = stageBase + (int)(100 * w / totalBytes) });
                    break;
                default:
                    await InstallZipComponentAsync(srcDir, comp, root, report, stageBase, w, totalBytes);
                    break;
            }
        }
    }

    private static long WeightOf(Manifest mf, string id)
        => id == "runtime" ? RuntimeWeight : Math.Max(ResolveComponent(mf, id).Size, 1);
    private static async Task InstallRuntimeAsync(string srcDir, Component comp, string root,
        IProgress<InstallReport> report, int stageBase, long w, long totalBytes)
    {
        var zip = await EnsureFileAsync(srcDir, comp, report, stageBase, w);
        if (zip is null)
            throw new InvalidOperationException("运行包缺失: " + comp.Title);
        if (!string.IsNullOrEmpty(comp.Sha256))
        {
            report.Report(new InstallReport { Stage = comp.Title, Detail = "校验文件完整性…", Pct = stageBase + (int)(8 * w / totalBytes) });
            var got = await Task.Run(() => Sha256Of(zip));
            if (!got.Equals(comp.Sha256, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("SHA256 校验失败: " + comp.File);
        }

        var pyDir = Path.Combine(root, "runtime", "python310");
        var python = Path.Combine(pyDir, "python.exe");
        if (!File.Exists(Path.Combine(pyDir, "python310._pth")) && Directory.Exists(pyDir))
            Directory.Delete(pyDir, recursive: true);
        Directory.CreateDirectory(pyDir);
        report.Report(new InstallReport { Stage = comp.Title, Detail = "正在安装…", Pct = stageBase + (int)(10 * w / totalBytes) });
        await Task.Run(() =>
        {
            using var za = ZipFile.OpenRead(zip);
            ExtractZipArchive(za, pyDir, _ => { });
        });
        if (!File.Exists(python))
            throw new InvalidOperationException("解压后未找到运行时: " + python);

        // ..\.. 是安装根: embeddable python 有 _pth 时会忽略 PYTHONPATH 与 cwd,
        // 不加这行训练/测试子进程(含 DataLoader 派生子进程)都 import 不到 app 包
        var pthContent = string.Join(Environment.NewLine,
            "python310.zip", ".", @"Lib\site-packages", @"..\..", "", "import site");
        await File.WriteAllTextAsync(Path.Combine(pyDir, "python310._pth"), pthContent);

        if (!await EnsurePipAsync(python, comp.Title, report, stageBase, w, totalBytes))
            throw new InvalidOperationException("Python 环境缺少 pip，且自动安装失败。");

        await InstallRequirementsAsync(python, comp.Title, report, stageBase, w, totalBytes,
            Path.Combine(pyDir, "pip-install.log"));
        report.Report(new InstallReport { Stage = comp.Title, Detail = "完成", Pct = stageBase + (int)(100 * w / totalBytes) });
    }

    private static async Task InstallRequirementsAsync(string python, string stage,
        IProgress<InstallReport> report, int stageBase, long w, long totalBytes, string logPath)
    {
        var reqPath = Path.Combine(Path.GetTempPath(), "installer", "requirements.txt");
        using (var rs = OpenEmbedded("requirements.txt"))
        {
            if (rs is null)
                throw new InvalidOperationException("安装程序内置缺少 requirements.txt(发布不完整)");
            Directory.CreateDirectory(Path.GetDirectoryName(reqPath)!);
            using var rfs = File.Create(reqPath);
            await rfs.WriteAsync(Encoding.UTF8.GetPreamble());
            await rs.CopyToAsync(rfs);
        }

        const string pipMsg = "正在下载安装所需组件,请勿断网…";
        report.Report(new InstallReport { Stage = stage, Detail = pipMsg, Pct = stageBase + (int)(12 * w / totalBytes) });

        string? lastErr = null;
        foreach (var torchIdx in TorchIndexUrls)
        {
            var args = $"-m pip install --disable-pip-version-check --timeout 60 --retries 10 "
                     + $"-r \"{reqPath}\" -i {PipIndex} --extra-index-url {torchIdx}";
            var (ok, err) = await RunPipAsync(python, args, stage, pipMsg, logPath, report, stageBase, w, totalBytes);
            if (ok) return;
            lastErr = err;
        }
        throw new InvalidOperationException("pip 安装依赖失败：" + lastErr);
    }

    private static async Task<(bool Ok, string? Error)> RunPipAsync(string python, string args, string stage, string pipMsg,
        string logPath, IProgress<InstallReport> report, int stageBase, long w, long totalBytes)
    {
        var sb = new StringBuilder();
        var psi = new ProcessStartInfo
        {
            FileName = python,
            Arguments = args,
            UseShellExecute = false,
            CreateNoWindow = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
        };
        using var p = Process.Start(psi);
        if (p is null)
            return (false, "无法启动 pip");
        p.OutputDataReceived += (_, e) => { if (e.Data is not null) sb.AppendLine(e.Data); };
        p.ErrorDataReceived += (_, e) => { if (e.Data is not null) sb.AppendLine(e.Data); };
        p.BeginOutputReadLine();
        p.BeginErrorReadLine();
        var tick = 12;
        while (!p.HasExited)
        {
            await Task.Delay(3000);
            if (tick < 85)
            {
                tick += 1;
                report.Report(new InstallReport { Stage = stage, Detail = pipMsg, Pct = stageBase + (int)(tick * w / totalBytes) });
            }
        }
        await p.WaitForExitAsync();
        try { await File.WriteAllTextAsync(logPath, sb.ToString(), Encoding.UTF8); } catch { }
        if (p.ExitCode == 0)
            return (true, null);
        return (false, $"退出码 {p.ExitCode}，日志: {logPath}");
    }

    private static async Task<bool> EnsurePipAsync(string python, string stage,
        IProgress<InstallReport> report, int stageBase, long w, long totalBytes)
    {
        if (await RunOk(python, "-m pip --version")) return true;

        report.Report(new InstallReport { Stage = stage, Detail = "正在安装 pip…", Pct = stageBase + (int)(11 * w / totalBytes) });
        var script = Path.Combine(Path.GetTempPath(), "installer", "get-pip.py");
        Directory.CreateDirectory(Path.GetDirectoryName(script)!);
        bool ready;
        await using (var res = OpenEmbedded("get-pip.py"))
        {
            if (res is not null)
            {
                await using var fs = File.Create(script);
                await res.CopyToAsync(fs);
                ready = true;
            }
            else
            {
                ready = await TryDownloadAsync(PipBootstrapUrl, script);
            }
        }
        if (!ready)
            throw new InvalidOperationException("获取 pip 安装脚本失败：网络不可达,且本安装程序未内置该脚本.");
        return await RunOk(python, $"\"{script}\" --no-warn-script-location -i {PipIndex}");
    }
    private static async Task<bool> TryDownloadAsync(string url, string path)
    {
        for (var attempt = 1; attempt <= DownloadAttempts; attempt++)
        {
            try
            {
                await using (var s = await Http.GetStreamAsync(url))
                await using (var fs = File.Create(path))
                    await s.CopyToAsync(fs);
                return true;
            }
            catch (Exception) when (attempt < DownloadAttempts)
            {
                await Task.Delay(3000 * attempt);
            }
            catch
            {
                return false;
            }
        }
        return false;
    }


    private static long FreeBytesOf(string path)
    {
        try
        {
            var full = Path.GetFullPath(path);
            if (full.StartsWith(@"\\")) return -1;
            foreach (var d in DriveInfo.GetDrives())
                if (d.IsReady && full.StartsWith(d.Name, StringComparison.OrdinalIgnoreCase))
                    return d.AvailableFreeSpace;
        }
        catch { }
        return -1;
    }

    private static string Gb(long bytes) => (bytes / 1073741824.0).ToString("0.0") + " GB";

    private static async Task<bool> RunOk(string file, string args)
    {
        try
        {
            using var p = Process.Start(new ProcessStartInfo
            {
                FileName = file,
                Arguments = args,
                UseShellExecute = false,
                CreateNoWindow = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
            });
            if (p is null) return false;
            await p.WaitForExitAsync();
            return p.ExitCode == 0;
        }
        catch { return false; }
    }


    private static List<(string File, string Url, string Sha256)> LoadAssets()
    {
        using var s = OpenEmbedded("pretrained-assets.txt")
            ?? throw new InvalidOperationException("安装程序内置缺少 pretrained-assets.txt(发布不完整)");
        using var r = new StreamReader(s);
        var list = new List<(string, string, string)>();
        while (r.ReadLine() is { } line)
        {
            if (line.Length == 0 || line[0] == '#') continue;
            var f = line.Split('\t');
            if (f.Length < 3) continue;
            list.Add((f[0].Trim(), f[1].Trim(), f[2].Trim()));
        }
        if (list.Count == 0)
            throw new InvalidOperationException("pretrained-assets.txt 里没有可用的权重条目（发布不完整）");
        return list;
    }


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

        var groups = LoadAssets().GroupBy(a => a.File, StringComparer.OrdinalIgnoreCase).ToList();
        var n = groups.Count;
        var failed = new List<string>();
        for (var i = 0; i < n; i++)
        {
            var grp = groups[i];
            var file = grp.Key;
            var target = Path.Combine(dest, file);
            var segPct = 100.0 / n * w / totalBytes;
            var segBase = stageBase + (int)(segPct * i);
            var no = $"第 {i + 1}/{n} 个文件";
            if (File.Exists(target))
            {
                var local = Sha256Of(target);
                if (grp.Any(a => local.Equals(a.Sha256, StringComparison.OrdinalIgnoreCase)))
                {
                    report.Report(new InstallReport { Stage = comp.Title, Detail = no + "已就绪,跳过", Pct = (int)(segBase + segPct) });
                    continue;
                }
            }
            report.Report(new InstallReport { Stage = comp.Title, Detail = "正在下载" + no + "…", Pct = segBase });
            Exception? firstErr = null;
            var step = -1;
            foreach (var (_, url, sha) in grp)
            {
                try
                {
                    await DownloadFileAsync(url, target, sha, (got, total) =>
                    {

                        var pct = Math.Min(100, (int)(100 * got / Math.Max(total, 1)));
                        var seg = pct / 5;
                        var bar = segBase + (int)(segPct * 0.9 * pct / 100);
                        if (seg == step)
                            report.Report(new InstallReport { Stage = comp.Title, Pct = bar });
                        else
                        {
                            step = seg;
                            report.Report(new InstallReport { Stage = comp.Title, Detail = no + " " + pct + "%", Pct = bar });
                        }
                    });
                    firstErr = null;
                    break;
                }
                catch (Exception ex)
                {
                    firstErr ??= ex;
                    step = -1;   // 换源重下,进度条从头再走
                }
            }
            if (firstErr is null)
                report.Report(new InstallReport { Stage = comp.Title, Detail = no + "下载完成", Pct = (int)(segBase + segPct) });
            else
                failed.Add(no + "（" + firstErr.Message + "）");
        }
        if (failed.Count > 0)
            report.Report(new InstallReport { Stage = comp.Title,
                Detail = "部分文件下载失败：" + string.Join(";", failed) + "重新运行本安装器可续传,或在软件内导入权重目录",
                Pct = stageBase + (int)(100 * w / totalBytes) });
        else
            report.Report(new InstallReport { Stage = comp.Title, Detail = "完成", Pct = stageBase + (int)(100 * w / totalBytes) });
    }

    private static async Task DownloadFileAsync(string url, string target, string expectedSha256,
        Action<long, long>? onProgress = null)
    {
        Exception? last = null;
        for (var attempt = 1; attempt <= DownloadAttempts; attempt++)
        {
            try
            {
                await DownloadOnceAsync(url, target, expectedSha256, onProgress);
                return;
            }
            catch (Exception ex) when (attempt < DownloadAttempts)
            {

                last = ex;
                await Task.Delay(3000 * attempt);
            }
        }
        throw last ?? new IOException("下载失败: " + url);
    }


    private static async Task DownloadOnceAsync(string url, string target, string expectedSha256,
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
            throw new InvalidDataException("SHA256 校验失败(官方源文件可能已更新,或下载被篡改)");
        }
        if (File.Exists(target)) File.Delete(target);
        File.Move(part, target);
    }


    private static async Task InstallZipComponentAsync(string srcDir, Component comp, string root,
        IProgress<InstallReport> report, int stageBase, long w, long totalBytes)
    {
        var zip = await EnsureFileAsync(srcDir, comp, report, stageBase, w);
        if (zip is null)
        {

            report.Report(new InstallReport { Stage = comp.Title,
                Detail = "跳过:该组件非必需,不影响使用,之后可在软件内导入权重目录",
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
        await Task.Run(() => ExtractAll(zip, dest,
            s => report.Report(new InstallReport { Stage = comp.Title, Pct = stageBase + 45 + (int)(50 * w / totalBytes) })));
        report.Report(new InstallReport { Stage = comp.Title, Detail = "完成", Pct = stageBase + (int)(100 * w / totalBytes) });
    }


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


    private static Stream? OpenEmbedded(string name)
    {
        var asm = Assembly.GetExecutingAssembly();
        var full = asm.GetManifestResourceNames()
            .FirstOrDefault(n => n.EndsWith(name, StringComparison.OrdinalIgnoreCase));
        return full is null ? null : asm.GetManifestResourceStream(full);
    }

    public static bool HasEmbedded(string name) => OpenEmbedded(name) is not null;


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

        report.Report(new InstallReport { Stage = comp.Title, Detail = "正在下载…", Pct = stageBase + (int)(30 * weightTotal / 100) });

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
            var step = -1;
            while ((n = await stream.ReadAsync(buf)) > 0)
            {
                await fs.WriteAsync(buf.AsMemory(0, n));
                got += n;
                var pct = Math.Min(100, (int)(100 * got / Math.Max(total, 1)));
                var bar = stageBase + (int)((30L + 40L * pct / 100) * weightTotal / 100);
                if (pct / 5 == step)
                {
                    report.Report(new InstallReport { Stage = comp.Title, Pct = bar });
                    continue;
                }
                step = pct / 5;
                report.Report(new InstallReport { Stage = comp.Title, Detail = $"正在下载… {pct}%", Pct = bar });
            }
        }
        if (File.Exists(target)) File.Delete(target);
        File.Move(part, target);
        return target;
    }


    private static int ExtractAll(string zip, string destDir, Action<string> progress)
    {
        using var za = ZipFile.OpenRead(zip);
        return ExtractZipArchive(za, destDir, progress);
    }


    private static int ExtractEmbeddedZip(string name, string destDir, Action<string> progress)
    {
        using var s = OpenEmbedded(name) ??
            throw new InvalidOperationException("程序内置资源缺失: " + name);
        using var za = new ZipArchive(s);
        return ExtractZipArchive(za, destDir, progress);
    }


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
                progress?.Invoke($"已解压 {count} 项…");
        }
        return count;
    }


    public static void CreateShortcuts(string root)
    {
        var pyDir = Path.Combine(root, "runtime", "python310");
        var pythonw = Path.Combine(pyDir, "pythonw.exe");
        if (!File.Exists(pythonw))
            pythonw = Path.Combine(pyDir, "python.exe");
        if (!File.Exists(pythonw))
            return; // 没装 runtime(如只装了 program 的调试场景)就不建快捷方式
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


    private static string FriendlyName(string name) => name switch
    {
        "runtime" => "运行时",
        "pretrained" => "预训练权重",
        "app" => "程序本体",
        "program" => "程序本体",
        "installed.json" => "安装信息",
        "unins000.exe" => "卸载程序",
        _ => name,
    };


    public static async Task UninstallAsync(string root, IProgress<InstallReport> report)
    {
        const string stage = "卸载";
        report.Report(new InstallReport { Stage = stage, Detail = "正在移除快捷方式…", Pct = 5 });
        await Task.Run(RemoveShortcuts);
        report.Report(new InstallReport { Stage = stage, Detail = "快捷方式已移除", Pct = 10 });

        if (!Directory.Exists(root))
        {
            report.Report(new InstallReport { Stage = stage, Detail = "安装目录已不存在", Pct = 100 });
            return;
        }

        var entries = await Task.Run(() => Directory.EnumerateFileSystemEntries(root)
            .Select(Path.GetFileName).Where(n => n is not null).ToList());
        var failed = new List<string>();
        for (var i = 0; i < entries.Count; i++)
        {
            var name = entries[i]!;
            report.Report(new InstallReport
            {
                Stage = stage,
                Detail = "正在删除 " + FriendlyName(name) + "…",
                Pct = 10 + (int)(85.0 * i / entries.Count),
            });
            if (!await Task.Run(() => TryDelete(Path.Combine(root, name))))
                failed.Add(FriendlyName(name));
        }
        TryDelete(root);

        if (failed.Count > 0)
            report.Report(new InstallReport
            {
                Stage = stage,
                Detail = "部分内容未能删除(可能被占用):" + string.Join("、", failed) + ",可关闭相关程序后手动删除",
                Pct = 100,
            });
        else
            report.Report(new InstallReport { Stage = stage, Detail = "完成", Pct = 100 });
    }

    private static void RemoveShortcuts()
    {
        var desktop = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory), "EasyTrainer.lnk");
        var startDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Programs), "EasyTrainer");
        var startMenu = Path.Combine(startDir, "EasyTrainer.lnk");
        foreach (var f in new[] { desktop, startMenu })
        {
            try { if (File.Exists(f)) File.Delete(f); } catch { }
        }
        try { if (Directory.Exists(startDir) && !Directory.EnumerateFileSystemEntries(startDir).Any()) Directory.Delete(startDir); } catch { }
    }


    private static bool TryDelete(string path)
    {
        try
        {
            Delete(path);
            return true;
        }
        catch { }
        try
        {
            ClearReadOnly(path);
            Delete(path);
            return true;
        }
        catch { return false; }
    }

    private static void Delete(string path)
    {
        if (Directory.Exists(path)) Directory.Delete(path, true);
        else if (File.Exists(path)) File.Delete(path);
    }

    private static void ClearReadOnly(string path)
    {
        if (File.Exists(path))
        {
            var fi = new FileInfo(path);
            if (fi.IsReadOnly) fi.IsReadOnly = false;
            return;
        }
        if (!Directory.Exists(path)) return;
        foreach (var f in Directory.EnumerateFiles(path, "*", SearchOption.AllDirectories))
        {
            try
            {
                var fi = new FileInfo(f);
                if (fi.IsReadOnly) fi.IsReadOnly = false;
            }
            catch { }
        }
    }

    private static string Sha256Of(string path)
    {
        using var fs = File.OpenRead(path);
        using var sha = SHA256.Create();
        return Convert.ToHexString(sha.ComputeHash(fs));
    }
}
