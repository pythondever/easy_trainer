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
    private string _lastLog = "";
    private string _srcDir = "";
    private bool _busy;
    private bool _finished;
    private readonly List<ComponentCard> _cards = new();
    private readonly Panel _scroll = new();   // 内容超出视口时出滚动条, 按钮行另挂在窗口底部
    private TableLayoutPanel _content = null!;

    // 日志所在的行: 高度由 FitScroll 现算(吃掉富余 / 让给滚动条)
    private const int LogRowIndex = 7;
    private const int LogMinHeight = 60;

    public MainForm()
    {
        SuspendLayout();
        // 手写布局全是像素值, 不打开字体自动缩放就不会跟着 DPI 走;
        // 基线 7x17 = 96dpi 下 Microsoft YaHei UI 9pt 的字体度量(设计器写出的就是这两个数)
        AutoScaleMode = AutoScaleMode.Font;
        AutoScaleDimensions = new SizeF(7F, 17F);

        Text = "安装程序";
        Font = new Font("Microsoft YaHei UI", 9f);
        BackColor = PageBg;
        ClientSize = new Size(820, 764);    // 设计尺寸
        MinimumSize = new Size(560, 420);   // 只是窗体下限: 内容装不下靠滚动条, 不再按内容定死
        StartPosition = FormStartPosition.CenterScreen;
        try { Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath) ?? Icon; } catch { }

        var header = new HeaderPanel
        {
            Dock = DockStyle.Top,
            Title = "安装向导",
            SubTitle = "检测 / 分割 / 分类 模型训练工具",
        };

        _dirBox.BorderStyle = BorderStyle.FixedSingle;
        _dirBox.Font = new Font("Microsoft YaHei UI", 9.5f);
        _dirBox.Height = 36;

        var browse = new RoundedButton
        {
            Text = "浏览...",
            Outline = true,
            Accent = Color.FromArgb(0x6B, 0x72, 0x80),
            Size = new Size(96, 36),
            Margin = new Padding(0),
        };

        _cardBox.BackColor = Color.Transparent;
        _cardBox.WrapContents = true;
        _cardBox.AutoScroll = true;
        _cardBox.Padding = new Padding(0);
        _cardBox.Margin = new Padding(0);

        _cardBox.Dock = DockStyle.Top;
        _cardBox.AutoSize = true;
        _cardBox.AutoSizeMode = AutoSizeMode.GrowAndShrink;

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
        _install.Font = new Font("Microsoft YaHei UI", 10.5f, FontStyle.Bold, GraphicsUnit.Point);
        _install.Accent = Color.FromArgb(0x2F, 0x6F, 0xED);
        _install.Margin = new Padding(0);
        _install.Click += async (_, _) =>
        {
            if (_finished) Close();
            else await InstallAsync();
        };

        _uninstall.Text = "卸载...";
        _uninstall.Size = new Size(110, 42);
        _uninstall.Outline = true;
        _uninstall.Accent = Color.FromArgb(0x6B, 0x72, 0x80);
        _uninstall.Click += (_, _) => UninstallDialog();


        var dirRow = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 2,
            RowCount = 1,
            Margin = new Padding(0),
            BackColor = PageBg,
        };
        dirRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        dirRow.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 96));
        dirRow.RowStyles.Add(new RowStyle(SizeType.Absolute, 36));
        _dirBox.Dock = DockStyle.Fill;

        _dirBox.Margin = new Padding(0, 6, 8, 6);
        browse.Dock = DockStyle.Fill;
        dirRow.Controls.Add(_dirBox, 0, 0);
        dirRow.Controls.Add(browse, 1, 0);


        var btnRow = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 3,
            RowCount = 1,
            Margin = new Padding(0, 16, 0, 0),
            BackColor = PageBg, // 同上
        };
        btnRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        btnRow.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 110));
        btnRow.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 140));
        btnRow.RowStyles.Add(new RowStyle(SizeType.Absolute, 42));
        _uninstall.Dock = DockStyle.Fill;
        _uninstall.Margin = new Padding(0, 0, 10, 0);
        _install.Dock = DockStyle.Fill;
        btnRow.Controls.Add(new Panel { BackColor = Color.Transparent, Margin = new Padding(0) }, 0, 0);
        btnRow.Controls.Add(_uninstall, 1, 0);
        btnRow.Controls.Add(_install, 2, 0);


        var content = new TableLayoutPanel
        {
            Dock = DockStyle.None,                    // 交给滚动容器, 尺寸由 FitScroll 现算
            ColumnCount = 1,
            Padding = new Padding(32, 22, 32, 0),     // 下留白归按钮条, 否则滚到底会多一块空
            BackColor = PageBg,
        };
        _content = content;
        content.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));

        content.RowCount = 9;
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 0 提示
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 1 Caption 安装目录
        content.RowStyles.Add(new RowStyle(SizeType.Absolute, 36));                              // 2 dirRow(Absolute 锁死: AutoSize 会被按钮 PreferredSize 撑到 ~100)
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 3 Caption 组件
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 4 cardContainer(高度随卡片数量自适应)
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 5 needLabel
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 6 Caption 日志
        content.RowStyles.Add(new RowStyle(SizeType.Absolute, LogMinHeight));                    // 7 logPanel(高度由 FitScroll 现算)
        content.RowStyles.Add(new RowStyle(SizeType.AutoSize));                                  // 8 _bar

        var sub = new Label
        {
            Text = "程序安装运行时和预训练权重需要连接网络; 文件放本目录则跳过下载.",
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
        // 按钮条单独挂在窗口底部: 窗口再矮也点得到, 不必先滚动
        var actionBar = new Panel
        {
            Dock = DockStyle.Bottom,
            Height = 58 + 22,
            Padding = new Padding(32, 16, 32, 22),
            BackColor = PageBg,
        };
        btnRow.Margin = new Padding(0);
        actionBar.Controls.Add(btnRow);

        _scroll.Dock = DockStyle.Fill;
        _scroll.AutoScroll = true;
        _scroll.BackColor = PageBg;
        _scroll.Resize += (_, _) => FitScroll();
        _scroll.Controls.Add(content);

        Controls.Add(_scroll);
        Controls.Add(actionBar);
        Controls.Add(header);
        ResumeLayout(performLayout: true);
        ClampToScreen();

        browse.Click += (_, _) =>
        {
            using var fbd = new FolderBrowserDialog { Description = "选择安装目录", SelectedPath = _dirBox.Text };
            if (fbd.ShowDialog(this) == DialogResult.OK)
                _dirBox.Text = fbd.SelectedPath;
        };


        _cardBox.Resize += (_, _) => RecalcCardWidths();
        this.Resize += (_, _) => RecalcCardWidths();

        _srcDir = AppContext.BaseDirectory;
        _dirBox.Text = DefaultInstallDir();

        Load += (_, _) =>
        {
            PopulateComponents();
            FitScroll();
            BeginInvoke(Refresh);
        };
    }


    // 日志行拿"视口 - 其余行高度", 地板 LogMinHeight; 装不下就整块交给滚动条.
    // 用绝对高度而不是 Percent: 窗口只有设计尺寸那么高时日志得能被压到自然高度以下(改前就是这么排的),
    // 否则会平白多出一条滚动条
    private void FitScroll()
    {
        if (_scroll.ClientSize.Width <= 0) return;
        var vp = _scroll.ClientSize;
        _content.Width = vp.Width;
        var fixedH = FixedRows();
        if (fixedH + LogMinHeight > vp.Height)
        {
            _content.Width = vp.Width - SystemInformation.VerticalScrollBarWidth;   // 让开竖条: 它压在客户区右边缘
            fixedH = FixedRows();      // 变窄后文字可能回流出更多行
        }
        var logH = Math.Max(LogMinHeight, vp.Height - fixedH);
        if ((int)_content.RowStyles[LogRowIndex].Height != logH)
            _content.RowStyles[LogRowIndex].Height = logH;
        var want = Math.Max(fixedH + logH, vp.Height);
        if (_content.Height != want) _content.Height = want;
    }

    // 除日志行以外所有行的高度之和(含内边距). 逐行取行样式 / 子控件自然高度:
    // GetRowHeights 会把表格用不完的富余摊进行里, 量出来比实际大(实测固定部分多算了 221px)
    private int FixedRows()
    {
        _content.PerformLayout();   // PreferredSize 依赖当前宽度, 宽度刚改过
        var sum = _content.Padding.Vertical;
        for (var i = 0; i < _content.RowCount; i++)
        {
            if (i == LogRowIndex) continue;
            var style = _content.RowStyles[i];
            if (style.SizeType == SizeType.Absolute)
            {
                sum += (int)style.Height;
                continue;
            }
            var child = _content.GetControlFromPosition(0, i);
            if (child != null) sum += child.PreferredSize.Height + child.Margin.Vertical;
        }
        return sum;
    }

    // 高缩放/小屏上设计尺寸会超出工作区: 夹进去, 剩下的交给滚动条
    private void ClampToScreen()
    {
        var wa = Screen.FromPoint(Cursor.Position).WorkingArea;
        var w = Math.Min(ClientSize.Width, Math.Max(320, wa.Width - 24));
        var h = Math.Min(ClientSize.Height, Math.Max(240, wa.Height - 24));
        if (w != ClientSize.Width || h != ClientSize.Height) ClientSize = new Size(w, h);
    }

    private static Label Caption(string text, int marginTop = 0)
        => new()
        {
            Text = text,
            Font = CaptionFont,
            ForeColor = CaptionColor,
            AutoSize = true,
            Margin = new Padding(0, marginTop, 0, 8),
        };

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
    }

    private void RecalcCardWidths()
    {
        if (_cardBox.Width <= 0 || _cards.Count == 0) return;
        var w = (_cardBox.ClientSize.Width - UiScale.Px(this, 14) * 2) / 2;   // 卡片的 Margin 已被自动缩放
        if (w < UiScale.Px(this, 200)) return;
        foreach (var c in _cards)
            c.Size = new Size(w, UiScale.Px(this, 100));   // 只改宽度: 高度保持设计值的等比缩放
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
            ? $"已选 {cnt} 项, 需下载 {FormatSize(total)}, 以及相关依赖约 3.3GB"
            : "请至少勾选一个组件.";
    }

    private async Task InstallAsync()
    {
        if (_busy) return;
        var root = _dirBox.Text.Trim();
        if (string.IsNullOrEmpty(root) || !Path.IsPathRooted(root))
        {
            MessageBox.Show(this, "请先填写有效的安装目录.", "installer", MessageBoxButtons.OK, MessageBoxIcon.Warning);
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
            MessageBox.Show(this, "至少选择一个组件.", "installer", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        _busy = true;
        _install.Enabled = _uninstall.Enabled = false;
        _bar.Value = 0;
        AppendLog($"安装目录: {root}");
        if (!InstallEngine.HasEmbedded("program.zip"))
            AppendLog("警告: 程序本体未内置本安装程序(发布不完整)");
        try
        {
            var progress = new Progress<InstallReport>(ReportProgress);
            await InstallEngine.InstallAsync(root, _srcDir, _mf, selected, progress);

            InstallEngine.WriteInstalled(root, _mf, selected);
            InstallEngine.CreateShortcuts(root);
            AppendLog("全部完成.");
            _bar.Value = 100;
            _finished = true;
            _install.Text = "关闭";
            MessageBox.Show(this,
                "安装完成.\n已创建桌面与开始菜单快捷方式.",
                "installer", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            AppendLog("安装失败: " + ex.Message);
            _bar.Value = 0;
            MessageBox.Show(this, "安装失败:\n" + ex.Message, "installer", MessageBoxButtons.OK, MessageBoxIcon.Error);
            _install.Text = "安装";
        }
        finally
        {
            _busy = false;
            _install.Enabled = true;
            _uninstall.Enabled = true;
        }
    }

    private async void UninstallDialog()
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
        _busy = true;
        _install.Enabled = _uninstall.Enabled = false;
        _bar.Value = 0;
        _lastLog = "";
        AppendLog($"卸载目录: {dir}");
        try
        {
            await InstallEngine.UninstallAsync(dir, new Progress<InstallReport>(ReportProgress));
            _bar.Value = 100;
            AppendLog("卸载完成.");
            MessageBox.Show(this, "已卸载.", "installer", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            _bar.Value = 0;
            AppendLog("卸载失败: " + ex.Message);
            MessageBox.Show(this, "卸载失败:" + ex.Message, "installer", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
        finally
        {
            _busy = false;
            _install.Enabled = true;
            _uninstall.Enabled = true;
        }
    }

    // 安装/卸载共用: Detail 为空表示只推进度条, 重复行不刷屏
    private void ReportProgress(InstallReport r)
    {
        _bar.Value = Math.Clamp(r.Pct, 0, 100);
        if (r.Detail.Length == 0) return;
        var line = $"[{r.Stage}] {r.Detail}";
        if (line == _lastLog) return;
        _lastLog = line;
        AppendLog(line);
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