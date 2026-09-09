using System.Text;

namespace Win.installer;

public sealed class MainForm : Form
{
    private readonly TextBox _dirBox = new();
    private readonly CheckedListBox _compList = new();
    private readonly Label _needLabel = new();
    private readonly RichTextBox _log = new();
    private readonly ProgressBar _bar = new();
    private readonly Button _install = new();
    private readonly Button _uninstall = new();
    private Manifest _mf = new();
    private string _srcDir = "";
    private bool _busy;
    private bool _finished;

    public MainForm()
    {
        Text = "安装程序";
        Font = new Font("Microsoft YaHei UI", 9f);
        ClientSize = new Size(780, 620);
        MinimumSize = new Size(720, 560);
        StartPosition = FormStartPosition.CenterScreen;

        var top = new Label
        {
            Text = "安装程序",
            Font = new Font(Font, FontStyle.Bold),
            AutoSize = true,
        };
        var sub = new Label
        {
            Text = "程序安装运行时和预训练权重需要连接网络;文件放本目录则跳过下载.",
            ForeColor = Color.DimGray,
            AutoSize = true,
        };

        var dirLabel = new Label { Text = "安装目录：", AutoSize = true };
        _dirBox.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
        var browse = new Button { Text = "浏览…", Width = 76 };

        var compCaption = new Label { Text = "选择要安装的组件:", AutoSize = true };
        _compList.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
        _compList.Height = 168;
        _compList.CheckOnClick = true;
        _compList.ItemCheck += (_, e) =>
        {
            if (_busy || _compList.Items[e.Index] is not Component c) return;
            if (c.Required)
            {
                e.NewValue = CheckState.Checked; // 必选组件不允许取消
                return;
            }
            if (e.NewValue == CheckState.Checked && !c.LocalReady && !c.OnlineAvailable)
            {
                e.NewValue = CheckState.Unchecked; // 无来源组件（本地无同名文件且无在线 url）禁止勾选
                MessageBox.Show(this,
                    $"未找到 {c.File}。\n请先将该文件放到安装程序同目录,再勾选「{c.Title}」。\n\n不勾选也可正常安装,之后可在软件内导入权重目录。",
                    "EasyTrainer", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        };

        _needLabel.ForeColor = Color.DimGray;
        _needLabel.AutoSize = true;

        _log.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
        _log.ReadOnly = true;
        _log.BackColor = Color.FromArgb(250, 250, 250);
        _log.Font = new Font("Consolas", 9f);
        _log.Text = "";

        _bar.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
        _bar.Height = 16;

        _install.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
        _install.Text = "安装";
        _install.Width = 110;
        _install.Click += async (_, _) =>
        {
            if (_finished) Close();
            else await InstallAsync();
        };

        _uninstall.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
        _uninstall.Text = "卸载…";
        _uninstall.Width = 90;
        _uninstall.Click += (_, _) => UninstallDialog();

        var l = new TableLayoutPanel { Dock = DockStyle.Fill, Padding = new Padding(16) };
        l.ColumnCount = 3;
        l.RowCount = 9;
        l.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));
        l.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        l.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));

        var dirRow = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2 };
        dirRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        dirRow.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));
        dirRow.Controls.Add(_dirBox, 0, 0);
        dirRow.Controls.Add(browse, 1, 0);
        dirRow.Controls.Add(dirLabel, 0, 1);
        dirRow.SetColumnSpan(dirLabel, 2);

        l.Controls.Add(top, 1, 0);
        l.SetColumnSpan(top, 3);
        l.Controls.Add(sub, 1, 1);
        l.SetColumnSpan(sub, 3);
        l.Controls.Add(dirLabel, 0, 2);
        l.Controls.Add(_dirBox, 1, 2);
        l.Controls.Add(browse, 2, 2);
        l.Controls.Add(compCaption, 1, 3);
        l.SetColumnSpan(compCaption, 3);
        l.Controls.Add(_compList, 0, 4);
        l.SetColumnSpan(_compList, 3);
        l.Controls.Add(_needLabel, 1, 5);
        l.SetColumnSpan(_needLabel, 3);
        l.Controls.Add(_log, 0, 6);
        l.SetColumnSpan(_log, 3);
        l.Controls.Add(_bar, 0, 7);
        l.SetColumnSpan(_bar, 3);
        l.Controls.Add(_install, 2, 8);
        l.Controls.Add(_uninstall, 1, 8);
        for (int r = 0; r < 9; r++)
            l.RowStyles.Add(new RowStyle(r == 6 ? SizeType.Percent : SizeType.AutoSize, 100));
        _log.Height = 150;
        Controls.Add(l);

        browse.Click += (_, _) =>
        {
            using var fbd = new FolderBrowserDialog { Description = "选择安装目录", SelectedPath = _dirBox.Text };
            if (fbd.ShowDialog(this) == DialogResult.OK)
                _dirBox.Text = fbd.SelectedPath;
        };

        _srcDir = AppContext.BaseDirectory;
        _dirBox.Text = DefaultInstallDir();
        Load += (_, _) => PopulateComponents();
    }

    /// <summary>用内置组件清单填充勾选列表与合计文案。</summary>
    private void PopulateComponents()
    {
        _mf = InstallEngine.BuiltinManifest(_srcDir);

        _compList.Items.Clear();
        long total = 0;
        foreach (var c in _mf.Components)
        {
            _compList.Items.Add(c, c.Default);
            total += c.Size;
        }
        _needLabel.Text = total > 0
            ? $"需下载 {FormatSize(total)},以及相关依赖约 2.5GB"
            : "";
        AppendLog("组件清单(内置)版本: " + (_mf.Version.Length > 0 ? _mf.Version : "(未标注)"));
        foreach (var c in _mf.Components)
            AppendLog($"  [{c.Id}] {c.Title}  {(c.LocalReady ? "本目录已就绪" : c.Url.Length > 0 || c.OnlineAvailable ? "在线下载" : "无可用来源（需同目录 zip 或软件内导入）")}");
    }

    private async Task InstallAsync()
    {
        if (_busy) return;
        var root = _dirBox.Text.Trim();
        if (string.IsNullOrEmpty(root) || !Path.IsPathRooted(root))
        {
            MessageBox.Show(this, "请先填写有效的安装目录。", "installer", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        var selected = new List<string>();
        foreach (Component? c in _compList.CheckedItems)
        {
            if (c is not null && !string.IsNullOrEmpty(c.Id))
                selected.Add(c.Id);
        }
        foreach (var c in _mf.Components.Where(c => c.Required && !selected.Contains(c.Id)))
            selected.Add(c.Id); // 必选兜底
        if (selected.Count == 0)
        {
            MessageBox.Show(this, "至少选择一个组件。", "installer", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        _busy = true;
        _install.Enabled = _uninstall.Enabled = false;
        _bar.Value = 0;
        AppendLog($"安装目录: {root}");
        AppendLog(InstallEngine.HasEmbedded("program.zip")
            ? "程序本体:已内置,随安装解压"
            : "警告：程序本体未内置本安装程序(发布不完整)");
        try
        {
            var progress = new Progress<InstallReport>(r =>
            {
                _bar.Value = Math.Clamp(r.Pct, 0, 100);
                if (r.Detail.Length > 0) AppendLog($"[{r.Stage}] {r.Detail}");
            });
            await InstallEngine.InstallAsync(root, _srcDir, _mf, selected, progress);

            InstallEngine.WriteInstalled(root, _mf, selected);
            InstallEngine.CreateShortcuts(root);
            AppendLog("全部完成。");
            _bar.Value = 100;
            _finished = true;
            _install.Text = "关闭";
            MessageBox.Show(this,
                "安装完成。\n已创建桌面与开始菜单快捷方式「EasyTrainer」。",
                "installer", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            AppendLog("安装失败: " + ex.Message);
            _bar.Value = 0;
            MessageBox.Show(this, "安装失败：\n" + ex.Message, "installer", MessageBoxButtons.OK, MessageBoxIcon.Error);
            _install.Text = "安装";
        }
        finally
        {
            _busy = false;
            _install.Enabled = true;
            _uninstall.Enabled = true;
        }
    }

    private void UninstallDialog()
    {        using var fbd = new FolderBrowserDialog { Description = "选择已安装的目录(须含 installed.json)" };
        if (fbd.ShowDialog(this) != DialogResult.OK) return;
        var dir = fbd.SelectedPath;
        if (!InstallEngine.IsInstalledRoot(dir))
        {
            MessageBox.Show(this, "该目录不是安装根(缺少 installed.json).", "卸载", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }
        if (MessageBox.Show(this, $"确定删除 {dir} 及其桌面/开始菜单快捷方式?", "卸载确认",
                MessageBoxButtons.YesNo, MessageBoxIcon.Question) != DialogResult.Yes)
            return;
        try
        {
            InstallEngine.Uninstall(dir);
            MessageBox.Show(this, "已卸载。", "installer", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, "卸载失败：" + ex.Message, "installer", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    private void AppendLog(string line)
    {
        _log.AppendText(DateTime.Now.ToString("[HH:mm:ss] ") + line + Environment.NewLine);
        _log.SelectionStart = _log.TextLength;
        _log.ScrollToCaret();
    }

    private static string DefaultInstallDir()
    {
        // 优先 D 盘（数据盘），否则 LocalAppData 免 UAC
        foreach (var d in DriveInfo.GetDrives())
            if (d.IsReady && d.DriveType == DriveType.Fixed && d.Name.StartsWith("D:", StringComparison.OrdinalIgnoreCase))
                return Path.Combine(d.Name, "installer");
        return Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "installer");
    }

    private static string FormatSize(long bytes) => bytes switch
    {
        >= 1L << 30 => $"{bytes / (double)(1L << 30):0.0} GB",
        >= 1L << 20 => $"{bytes / (double)(1L << 20):0} MB",
        _ => $"{bytes / 1024.0:0} KB",
    };
}
