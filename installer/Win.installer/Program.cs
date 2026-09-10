using System.Text;

namespace Win.installer;

static class Program
{
    [STAThread]
    static void Main(string[] args)
    {
        ApplicationConfiguration.Initialize();
        if (args.Length >= 3 && args[0] == "--install")
            Environment.Exit(SilentInstall(args));
        Application.Run(new MainForm());
    }


    static int SilentInstall(string[] args)
    {
        var root = args[1];
        var comps = args[2].Split(',', StringSplitOptions.RemoveEmptyEntries)
            .Select(s => s.Trim()).Where(s => s.Length > 0).ToList();
        var srcDir = AppContext.BaseDirectory;
        var logPath = Path.Combine(root, "install.log");
        void Log(string s)
        {
            try { File.AppendAllText(logPath, $"[{DateTime.Now:HH:mm:ss}] {s}\n", Encoding.UTF8); } catch { }
        }
        try
        {
            Directory.CreateDirectory(root);
            var mf = InstallEngine.BuiltinManifest(srcDir);
            Log($"组件清单（内置）版本: {mf.Version};组件: {string.Join(",", comps)}");
            Log("程序本体内置: " + InstallEngine.HasEmbedded("program.zip"));
            var progress = new Progress<InstallReport>(r => Log($"[{r.Stage}] {r.Detail}"));
            InstallEngine.InstallAsync(root, srcDir, mf, comps, progress).GetAwaiter().GetResult();
            InstallEngine.WriteInstalled(root, mf, comps);
            Log("完成");
            return 0;
        }
        catch (Exception ex)
        {
            Log("失败: " + ex);
            return 1;
        }
    }
}
