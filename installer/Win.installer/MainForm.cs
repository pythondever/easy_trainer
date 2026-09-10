using System.Drawing;
using System.Windows.Forms;

namespace Win.installer;

public sealed class MainForm : Form
{
    private static readonly Color PageBg = Color.FromArgb(0xF4, 0xF6, 0xFA);
    private static readonly Color CaptionColor = Color.FromArgb(0x33, 0x3B, 0x4A);
    private static readonly Color MutedColor = Color.FromArgb(0x6B, 0x72, 0x80);
    private static readonly Font CaptionFont = new("Microsoft YaHei UI", 9.75f, FontStyle.Bold, GraphicsUnit.Point);

    private readonly TextBox _dirBox = new();
    private readonly FlowLayoutPanel _cardBox = new();
    private readonly Label _needLabel = new();
    private readonly RichTextBox _log = new();
    private readonly ProgressBar _bar = new();
    private readonly RoundedButton _install = new();
    private readonly RoundedButton _uninstall = new();
    private Manifest _mf = new();
    private string _srcDir = "";
    private bool _busy;
    private bool _finished;
    private readonly List<ComponentCard> _cards = new();

    public MainForm()
    {
        Text = "EasyTrainer 安装程序";
        Font = new Font("Microsoft YaHei UI", 9f);
        BackColor = PageBg;
        ClientSize = new Size(820, 720);
        MinimumSize = new Size(760, 640);
        StartPosition = FormStartPosition.CenterScreen;
        try { Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath) ?? Icon; } catch { }

        var header = new HeaderPanel
        {
            Dock = DockStyle.Top,
            Title = "EasyTrainer",
            SubTitle = "检测 / 分割 / 分类 模型训练工具 · 安装向导",
        };

        // ── 控件初始化 ────────────────────────────────────────────────
        _dirBox.BorderStyle = BorderStyle.FixedSingle;
        _dirBox.Font = new Font("Microsoft YaHei UI", 9.5f);
        _dirBox.Height = 36;

        var browse = new RoundedButton
        {
            Text = "浏览…",
            Outline = true,
            Accent = Color.FromArgb(0x33, 0x3B, 0x4A),
            Size = new Size(96, 36),
            MinimumSize = new Size(96, 36),
        };

        _cardBox.BackColor = Color.Transparent;
        _cardBox.WrapContents = true;
        _cardBox.AutoScroll = true;
        _cardBox.Padding = new Padding(0);
        _cardBox.Margin = new Padding(0);

        _needLabel.ForeColor = MutedColor;
        _needLabel.AutoSize = true;
        _needLabel.Font = new Font(Font, FontStyle.Regular);

        _log.ReadOnly = true;
        _log.BackColor = Color.White;
        _log.BorderStyle = BorderStyle.None;
        _log.Font = new Font("Consolas", 9f);
        _log.ForeColor = Color.FromArgb(0x1F, 0x24, 0x30);
        _log.Dock = DockStyle.Fill;
        var logPanel = new Panel
        {
            Dock = DockStyle.Fill,
            BackColor = Color.White,
            Padding = new Padding(12, 8, 12, 8),
            BorderStyle = BorderStyle.FixedSingle,
        };
        logPanel.Controls.Add(_log);

        _bar.Dock = DockStyle.Top;
        _bar.Height = 14;

        _install.Text = "安装";
        _install.Size = new Size(140, 42);
        _install.MinimumSize = new Size(140, 42);
        _install.Font = new Font("Microsoft YaHei UI", 10.5f, FontStyle.Bold, GraphicsUnit.Point);
        _install.Accent = Color.FromArgb(0x2F, 0x6F, 0xED);
        _install.Click += async (_, _) =>
        {
            if (_finished) Close();
            else await InstallAsync();
        };

        _uninstall.Text = "卸载…";
        _uninstall.Size = new Size(110, 42);
        _uninstall.MinimumSize = new Size(110, 42);
        _uninstall.Outline = true;
        _uninstall.Accent = Color.FromArgb(0x6B, 0x72, 0x80);
        _uninstall.Click += (_, _) => UninstallDialog();

        // ── 目录行（嵌套 TableLayoutPanel：Percent 100 + Absolute 100） ──
        var dirRow = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 2,
            RowCount = 1,
            Margin = new Padding(0),
        };
        dirRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        dirRow.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 96));
        dirRow.RowStyles.Add(new RowStyle(SizeType.Absolute, 36));
        _dirBox.Dock = DockStyle.Fill;
        _dirBox.Margin = new Padding(0, 0, 8, 0);
        browse.Dock = DockStyle.Fill;
        dirRow.Controls.Add(_dirBox, 0, 0);
        dirRow.Controls.Add(browse, 1, 0);

        // ── 按钮行 ───────────────────────────────────────────────────
        var btnRow = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 3,
            RowCount = 1,
            Margin = new Padding(0, 16, 0, 0),
        };
        btnRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        btnRow.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 110));
        btnRow.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 140));
        btnRow.RowStyles.Add(new RowStyle(SizeType.Absolute, 42));
        _uninstall.Dock = DockStyle.Fill;
        _uninstall.Margin = new Padding(0, 0, 10, 0);
        _install.Dock = DockStyle.Fill;
        btnRow.Controls.Add(new Panel { BackColor = Color.Transparent }, 0, 0);
        btnRow.Controls.Add(_uninstall, 1, 0);
        btnRow.Controls.Add(_install, 2, 0);

        // ── 主内容 TableLayoutPanel（列 Percent 100 + 行混排） ─────────
        var content = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 1,
            Padding = new Padding(32, 22, 32, 22),
            BackColor = PageBg,
        };
        content.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        // 行样式：前几个 AutoSize，中间卡片 Absolute 高度，日志 Percent 100
        content.RowCount = 10;
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 0 提示
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 1 Caption 安装目录
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 2 dirRow
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 3 Caption 组件
        content.RowStyles.Add(new RowStyle(SizeType.Absolute, 224));                             // 4 cardContainer
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 5 needLabel
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 6 Caption 日志
        content.RowStyles.Add(new RowStyle(SizeType.Percent, 100));                              // 7 logPanel
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 8 _bar
        content.RowStyles.Add(new RowStyle(SizeType.Absolute, 42));                              // 9 btnRow

        var sub = new Label
        {
            Text = "程序安装运行时和预训练权重需要连接网络;文件放本目录则跳过下载.",
            ForeColor = MutedColor,
            AutoSize = true,
            Font = new Font("Microsoft YaHei UI", 9f),
            Margin = new Padding(0, 0, 0, 14),
        };
        content.Controls.Add(sub, 0, 0);
        content.Controls.Add(Caption("安装目录"), 0, 1);
        content.Controls.Add(dirRow, 0, 2);
        content.Controls.Add(Caption("选择要安装的组件"), 0, 3);
        _cardBox.Dock = DockStyle.Fill;
        content.Controls.Add(_cardBox, 0, 4);
        content.Controls.Add(_needLabel, 0, 5);
        content.Controls.Add(Caption("安装日志"), 0, 6);
        content.Controls.Add(logPanel, 0, 7);
        _bar.Margin = new Padding(0, 10, 0, 0);
        content.Controls.Add(_bar, 0, 8);
        content.Controls.Add(btnRow, 0, 9);

        Controls.Add(content);
        Controls.Add(header);

        browse.Click += (_, _) =>
        {
            using var fbd = new FolderBrowserDialog { Description = "选择安装目录", SelectedPath = _dirBox.Text };
            if (fbd.ShowDialog(this) == DialogResult.OK)
                _dirBox.Text = fbd.SelectedPath;
        };

        // 卡片容器尺寸变化时重排卡片宽度为两列
        _cardBox.Resize += (_, _) => RecalcCardWidths();
        this.Resize += (_, _) => RecalcCardWidths();

        _srcDir = AppContext.BaseDirectory;
        _dirBox.Text = DefaultInstallDir();
        Load += (_, _) => PopulateComponents();
    }

    /// <summary>分组标题 Label（可选上边距）。</summary>
    private static Label Caption(string text, int marginTop = 0)
        => new()
        {
            Text = text,
            Font = CaptionFont,
            ForeColor = CaptionColor,
            AutoSize = true,
            Margin = new Padding(0, marginTop, 0, 8),
        };

    /// <summary>用内置组件清单填充卡片容器与合计文案。</summary>
    private void PopulateComponents()
    {
        _mf = InstallEngine.BuiltinManifest(_srcDir);

        _cardBox.Controls.Clear();
        _cards.Clear();
        long total = 0;
        foreach (var c in _mf.Components)
        {
            var card = new ComponentCard(c, c.Default, c.Required);
            card.CheckChanged += (_, _) => UpdateNeedLabel();
            _cards.Add(card);
            _cardBox.Controls.Add(card);
            if (c.Default || c.Required) total += c.Size;
        }
        RecalcCardWidths();
        UpdateNeedLabel();

        AppendLog("组件清单(内置)版本: " + (_mf.Version.Length > 0 ? _mf.Version : "(未标注)"));
        foreach (var c in _mf.Components)
            AppendLog($"  [{c.Id}] {c.Title}  {(c.LocalReady ? "本目录已就绪" : c.Url.Length > 0 || c.OnlineAvailable ? "在线下载" : "无可用来源（需同目录 zip 或软件内导入）")}");
    }

    /// <summary>让卡片始终保持两列（VS Installer 网格）。</summary>
    private void RecalcCardWidths()
    {
        if (_cardBox.Width <= 0 || _cards.Count == 0) return;
        // 容器内可用宽（减 padding/margin），单列 = 一半再减间距
        var gap = 14;
        var w = (_cardBox.ClientSize.Width - gap) / 2;
        if (w < 200) return;
        foreach (var c in _cards)
            c.Size = new Size(w, 92);
    }

    private void UpdateNeedLabel()
    {
        long total = 0;
        int cnt = 0;
        foreach (var card in _cards)
        {
            if (card.IsChecked)
            {
                cnt++;
                total += card.Model.Size;
            }
        }
        _needLabel.Text = cnt > 0
            ? $"已选 {cnt} 项,需下载 {FormatSize(total)},以及相关依赖约 2.5GB"
            : "请至少勾选一个组件。";
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
        foreach (var card in _cards)
        {
            if (!card.IsChecked) continue;
            if (!string.IsNullOrEmpty(card.Model.Id))
                selected.Add(card.Model.Id);
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
            : "警告:程序本体未内置本安装程序(发布不完整)");
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
    {
        using var fbd = new FolderBrowserDialog { Description = "选择已安装的目录(须含 installed.json)" };
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