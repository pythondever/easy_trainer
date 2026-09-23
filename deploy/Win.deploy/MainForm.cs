using System.Diagnostics;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Win.deploy;

public sealed class MainForm : Form
{
    private static readonly Color PageBg = Color.FromArgb(0xF4, 0xF6, 0xFA);
    private static readonly Color CaptionColor = Color.FromArgb(0x33, 0x3B, 0x4A);
    private static readonly Color MutedColor = Color.FromArgb(0x6B, 0x72, 0x80);
    private static readonly Color OkColor = Color.FromArgb(0x1B, 0x8A, 0x4B);
    private static readonly Color WarnColor = Color.FromArgb(0xB5, 0x66, 0x00);
    private static readonly Color ErrColor = Color.FromArgb(0xC0, 0x36, 0x36);
    private static readonly Font CaptionFont =
        new("Microsoft YaHei UI", 9.75f, FontStyle.Bold, GraphicsUnit.Point);

    private readonly AppConfig _cfg = AppConfig.Load();
    private GpuInfo _gpu = new();
    private ToolchainInfo _tc = new();
    private bool _busy;
    private string _format = "engine";
    private bool _formatPickedByUser;
    private readonly Panel _scroll = new();   // 内容超出视口时出滚动条, 按钮行另挂在窗口底部
    private TableLayoutPanel _content = null!;

    // 日志所在的行: 高度由 FitScroll 现算(吃掉富余 / 让给滚动条)
    private const int LogRowIndex = 10;
    private const int LogMinHeight = 60;

    private readonly TextBox _onnxBox = new();
    private readonly TextBox _outBox = new();
    private readonly TextBox _shapeBox = new();
    private readonly RichTextBox _log = new();
    private readonly ProgressBar _bar = new();
    private readonly RoundedButton _run = new();
    private readonly RoundedButton _openOut = new();
    private readonly RoundedButton _redetect = new();
    private readonly RoundedButton _pickToolchain = new();
    private readonly RoundedButton _fp16Btn = new();
    private readonly RoundedButton _fp32Btn = new();
    private readonly CheckBox _crossArch = new();
    private readonly ToolTip _tips = new();
    private readonly SelectCard _cardEngine = new();
    private readonly SelectCard _cardOpenVino = new();
    private readonly Label _valGpu = new();
    private readonly Label _valDriver = new();
    private readonly Label _valToolchain = new();
    private readonly Label _valOv = new();
    private readonly FlowLayoutPanel _cardRow = new();

    public MainForm()
    {
        SuspendLayout();
        // 手写布局全是像素值, 不打开字体自动缩放就不会跟着 DPI 走;
        // 基线 7x17 = 96dpi 下 Microsoft YaHei UI 9pt 的字体度量(设计器写出的就是这两个数)
        AutoScaleMode = AutoScaleMode.Font;
        AutoScaleDimensions = new SizeF(7F, 17F);

        Text = "模型转换";
        Font = new Font("Microsoft YaHei UI", 9f);
        BackColor = PageBg;
        ClientSize = new Size(880, 802);    // 设计尺寸
        MinimumSize = new Size(560, 420);   // 只是窗体下限: 内容装不下靠滚动条, 不再按内容定死
        StartPosition = FormStartPosition.CenterScreen;
        try { Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath) ?? Icon; } catch { }

        var header = new HeaderPanel
        {
            Dock = DockStyle.Top,
            Title = "模型转换",
            SubTitle = "把训练导出的 onnx 转成 TensorRT engine 或 OpenVINO IR",
        };

        var content = new TableLayoutPanel
        {
            Dock = DockStyle.None,                    // 交给滚动容器, 尺寸由 FitScroll 现算
            ColumnCount = 1,
            Padding = new Padding(32, 18, 32, 0),     // 下留白归按钮条, 否则滚到底会多一块空
            BackColor = PageBg,
        };
        _content = content;
        content.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        content.RowCount = 12;
        for (var i = 0; i < 12; i++) content.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        content.RowStyles[0] = new RowStyle(SizeType.Absolute, 40);   // 环境标题行(锁死, 免得被按钮撑高)
        content.RowStyles[5] = new RowStyle(SizeType.Absolute, 34);   // 输入 onnx
        content.RowStyles[6] = new RowStyle(SizeType.Absolute, 34);   // 输出目录
        content.RowStyles[7] = new RowStyle(SizeType.Absolute, 34);   // 输入尺寸
        content.RowStyles[10] = new RowStyle(SizeType.Absolute, LogMinHeight);  // 日志(高度由 FitScroll 现算)

        content.Controls.Add(BuildEnvHeader(), 0, 0);
        content.Controls.Add(BuildEnvCard(), 0, 1);
        content.Controls.Add(Caption("目标格式"), 0, 2);
        content.Controls.Add(BuildCardRow(), 0, 3);
        content.Controls.Add(Caption("文件"), 0, 4);
        content.Controls.Add(BuildFileRow(_onnxBox, "onnx 模型", "选择训练导出的 .onnx", PickOnnx), 0, 5);
        content.Controls.Add(BuildFileRow(_outBox, "输出目录", "留空则与模型同目录", PickOutDir), 0, 6);
        content.Controls.Add(BuildFileRow(_shapeBox, "输入尺寸", "模型的输入是动态尺寸时才填, 如 images:1x3x640x640", null), 0, 7);
        content.Controls.Add(BuildOptionsRow(), 0, 8);
        content.Controls.Add(Caption("日志"), 0, 9);
        content.Controls.Add(BuildLogPanel(), 0, 10);
        _bar.Dock = DockStyle.Top;
        _bar.Height = 14;
        _bar.Margin = new Padding(0, 10, 0, 0);
        content.Controls.Add(_bar, 0, 11);

        // 按钮条单独挂在窗口底部: 窗口再矮也点得到, 不必先滚动
        var actionBar = new Panel
        {
            Dock = DockStyle.Bottom,
            Height = 56 + 18,
            Padding = new Padding(32, 14, 32, 18),
            BackColor = PageBg,
        };
        var btnRow = BuildButtonRow();
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

        _onnxBox.Text = _cfg.LastOnnxDir;
        _outBox.Text = _cfg.OutputDir;
        SetFp16(_cfg.Fp16, persist: false);
        _crossArch.Checked = _cfg.CrossArch;
        SyncShapeBox(true);

        Load += async (_, _) => await DetectAsync();
        FormClosing += (_, _) =>
        {
            _cfg.LastOnnxDir = _onnxBox.Text.Trim();
            _cfg.OutputDir = _outBox.Text.Trim();
            _cfg.CrossArch = _crossArch.Checked;
            _cfg.Save();
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

    private static Label Caption(string text)
        => new()
        {
            Text = text,
            Font = CaptionFont,
            ForeColor = CaptionColor,
            AutoSize = true,
            Margin = new Padding(0, 6, 0, 8),
        };

    private TableLayoutPanel BuildEnvHeader()
    {
        var row = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 3,
            RowCount = 1,
            Margin = new Padding(0),
            BackColor = PageBg,
        };
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 148));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 96));

        var cap = Caption("运行环境");
        cap.AutoSize = false;
        cap.Dock = DockStyle.Fill;
        cap.TextAlign = ContentAlignment.MiddleLeft;
        cap.Margin = new Padding(0, 0, 0, 4);

        _pickToolchain.Text = "选择工具链目录";
        _pickToolchain.Outline = true;
        _pickToolchain.Accent = MutedColor;
        _pickToolchain.Font = new Font("Microsoft YaHei UI", 9f);
        _pickToolchain.Dock = DockStyle.Fill;
        _pickToolchain.Margin = new Padding(0, 4, 8, 4);
        _pickToolchain.Click += (_, _) => PickToolchainDir();

        _redetect.Text = "重新检测";
        _redetect.Outline = true;
        _redetect.Accent = MutedColor;
        _redetect.Font = new Font("Microsoft YaHei UI", 9f);
        _redetect.Dock = DockStyle.Fill;
        _redetect.Margin = new Padding(0, 4, 0, 4);
        _redetect.Click += async (_, _) => await DetectAsync();

        row.Controls.Add(cap, 0, 0);
        row.Controls.Add(_pickToolchain, 1, 0);
        row.Controls.Add(_redetect, 2, 0);
        return row;
    }

    private CardPanel BuildEnvCard()
    {
        var card = new CardPanel
        {
            Dock = DockStyle.Fill,
            AutoSize = true,
            AutoSizeMode = AutoSizeMode.GrowAndShrink,
            Margin = new Padding(0, 0, 0, 12),
        };
        var grid = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            AutoSize = true,
            AutoSizeMode = AutoSizeMode.GrowAndShrink,
            ColumnCount = 2,
            RowCount = 4,
            BackColor = Color.White,
            Margin = new Padding(0),
        };
        grid.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 68));
        grid.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        for (var i = 0; i < 4; i++) grid.RowStyles.Add(new RowStyle(SizeType.AutoSize));

        AddEnvRow(grid, 0, "显卡", _valGpu);
        AddEnvRow(grid, 1, "驱动", _valDriver);
        AddEnvRow(grid, 2, "工具链", _valToolchain);
        AddEnvRow(grid, 3, "OpenVINO", _valOv);
        card.Controls.Add(grid);
        return card;
    }

    private static void AddEnvRow(TableLayoutPanel grid, int row, string key, Label val)
    {
        grid.Controls.Add(new Label
        {
            Text = key,
            ForeColor = MutedColor,
            AutoSize = true,
            BackColor = Color.White,
            Margin = new Padding(0, 3, 0, 3),
        }, 0, row);
        val.AutoSize = true;
        val.BackColor = Color.White;
        val.Margin = new Padding(0, 3, 0, 3);
        val.Text = "检测中...";
        grid.Controls.Add(val, 1, row);
    }

    private FlowLayoutPanel BuildCardRow()
    {
        _cardEngine.Title = "TensorRT engine";
        _cardEngine.Description = "显卡直接加载, 推理最快. 需要 NVIDIA 显卡与 TensorRT 运行时文件.";
        _cardEngine.Picked += _ => SelectFormat("engine", byUser: true);

        _cardOpenVino.Title = "OpenVINO IR";
        _cardOpenVino.Description = "转成 .xml + .bin 交给 OpenVINO 运行时(Python / C++). 不挑显卡, 也不用装 TensorRT.";
        _cardOpenVino.Picked += _ => SelectFormat("ir", byUser: true);

        _cardRow.Dock = DockStyle.Fill;
        _cardRow.AutoSize = true;
        _cardRow.AutoSizeMode = AutoSizeMode.GrowAndShrink;
        _cardRow.WrapContents = false;
        _cardRow.BackColor = PageBg;
        _cardRow.Margin = new Padding(0, 0, 0, 6);
        _cardRow.Controls.Add(_cardEngine);
        _cardRow.Controls.Add(_cardOpenVino);
        _cardRow.Resize += (_, _) => RecalcCardWidths();
        return _cardRow;
    }

    private void RecalcCardWidths()
    {
        if (_cardRow.Width <= 0) return;
        var w = (_cardRow.ClientSize.Width - UiScale.Px(this, 14)) / 2;   // 卡片的 Margin 已被自动缩放
        if (w < UiScale.Px(this, 220)) return;
        var h = UiScale.Px(this, 92);   // 只改宽度: 高度保持设计值的等比缩放
        _cardEngine.Size = new Size(w, h);
        _cardOpenVino.Size = new Size(w, h);
    }

    private Control BuildFileRow(TextBox box, string label, string placeholder, Action? onBrowse)
    {
        var row = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 3,
            RowCount = 1,
            Margin = new Padding(0),
            BackColor = PageBg,
        };
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 68));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, onBrowse is null ? 0 : 92));
        row.RowStyles.Add(new RowStyle(SizeType.Absolute, 34));

        var tag = new Label
        {
            Text = label,
            ForeColor = MutedColor,
            Dock = DockStyle.Fill,
            TextAlign = ContentAlignment.MiddleLeft,
            Margin = new Padding(0, 0, 0, 0),
        };
        row.Controls.Add(tag, 0, 0);

        box.BorderStyle = BorderStyle.FixedSingle;
        box.Font = new Font("Microsoft YaHei UI", 9.5f);
        box.Dock = DockStyle.Fill;
        // 单行 TextBox 高度固定, margin 要按按钮高度反推, 否则两者差一截不齐平
        box.Margin = new Padding(0, 6, 8, 6);
        box.PlaceholderText = placeholder;

        row.Controls.Add(box, 1, 0);
        if (onBrowse is null) return row;   // 纯输入行(输入尺寸), 不给浏览按钮

        var browse = new RoundedButton
        {
            Text = "浏览...",
            Outline = true,
            Accent = MutedColor,
            Font = new Font("Microsoft YaHei UI", 9f),
            Dock = DockStyle.Fill,
            Margin = new Padding(0, 6, 0, 6),
        };
        browse.Click += (_, _) => onBrowse();

        row.Controls.Add(browse, 2, 0);
        return row;
    }

    private Control BuildOptionsRow()
    {
        _fp16Btn.Text = "FP16";
        _fp32Btn.Text = "FP32";
        foreach (var b in new[] { _fp16Btn, _fp32Btn })
        {
            b.Font = new Font("Microsoft YaHei UI", 9f);
            b.Size = new Size(72, 30);
            b.Margin = new Padding(0, 4, 8, 4);
        }
        _fp16Btn.Click += (_, _) => SetFp16(true, persist: true);
        _fp32Btn.Click += (_, _) => SetFp16(false, persist: true);

        _crossArch.Text = "跨架构 (ampere+, 适配 sm80 及以上显卡)";
        _crossArch.AutoSize = true;
        _crossArch.ForeColor = MutedColor;
        _crossArch.Margin = new Padding(20, 9, 0, 4);

        var row = new FlowLayoutPanel
        {
            Dock = DockStyle.Fill,
            AutoSize = true,
            AutoSizeMode = AutoSizeMode.GrowAndShrink,
            WrapContents = false,
            BackColor = PageBg,
            Margin = new Padding(0, 2, 0, 2),
        };
        var tag = new Label
        {
            Text = "精度",
            ForeColor = MutedColor,
            AutoSize = true,
            Margin = new Padding(0, 11, 12, 4),
        };
        row.Controls.Add(tag);
        row.Controls.Add(_fp16Btn);
        row.Controls.Add(_fp32Btn);
        row.Controls.Add(_crossArch);
        return row;
    }

    private Control BuildLogPanel()
    {
        _log.ReadOnly = true;
        _log.BackColor = Color.White;
        _log.BorderStyle = BorderStyle.None;
        _log.Font = new Font("Consolas", 9f);
        _log.ForeColor = Color.FromArgb(0x1F, 0x24, 0x30);
        _log.Dock = DockStyle.Fill;
        _log.WordWrap = false;
        var panel = new Panel
        {
            Dock = DockStyle.Fill,
            BackColor = Color.White,
            Padding = new Padding(12, 8, 12, 8),
            BorderStyle = BorderStyle.FixedSingle,
            Margin = new Padding(0),
        };
        panel.Controls.Add(_log);
        return panel;
    }

    private Control BuildButtonRow()
    {
        _openOut.Text = "打开输出目录";
        _openOut.Outline = true;
        _openOut.Accent = MutedColor;
        _openOut.Size = new Size(140, 42);
        _openOut.Margin = new Padding(0);
        _openOut.Click += (_, _) => OpenOutputDir();

        _run.Text = "开始转换";
        _run.Size = new Size(150, 42);
        _run.Font = new Font("Microsoft YaHei UI", 10.5f, FontStyle.Bold, GraphicsUnit.Point);
        _run.Accent = Color.FromArgb(0x2F, 0x6F, 0xED);
        _run.Margin = new Padding(12, 0, 0, 0);
        _run.Click += async (_, _) => await RunAsync();

        var row = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 3,
            RowCount = 1,
            Margin = new Padding(0, 14, 0, 0),
            BackColor = PageBg,
        };
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 140));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 162));
        row.RowStyles.Add(new RowStyle(SizeType.Absolute, 42));
        _openOut.Dock = DockStyle.Fill;
        _run.Dock = DockStyle.Fill;
        row.Controls.Add(_openOut, 0, 0);
        row.Controls.Add(new Panel { BackColor = Color.Transparent, Margin = new Padding(0) }, 1, 0);
        row.Controls.Add(_run, 2, 0);
        return row;
    }

    private void SetFp16(bool on, bool persist)
    {
        _fp16Btn.Outline = !on;
        _fp32Btn.Outline = on;
        _fp16Btn.Invalidate();
        _fp32Btn.Invalidate();
        if (persist) _cfg.Fp16 = on;
    }

    private bool Fp16 => !_fp16Btn.Outline;

    private void SelectFormat(string format, bool byUser)
    {
        if (byUser) _formatPickedByUser = true;
        var engineUsable = _gpu.Available && _tc.Ready;
        if (format == "engine" && !engineUsable)
        {
            if (byUser) AppendLog("engine 需要 NVIDIA 显卡与 TensorRT 运行时, 当前条件不满足");
            format = "ir";
        }
        if (format == "ir" && !IrUsable)
        {
            if (byUser) AppendLog("OpenVINO 运行时不可用: " + OpenVinoConverter.Ready());
            format = "engine";
        }
        _format = format;
        _cardEngine.Selected = format == "engine";
        _cardOpenVino.Selected = format == "ir";
        // FP16/FP32 两条路都有意义: engine 是算子精度, IR 是权重压缩
        _fp16Btn.Enabled = _fp32Btn.Enabled = true;
        SyncCrossArch(format == "engine");
        SyncShapeBox(format == "engine");
        _run.Text = format == "engine" ? "开始转换" : "转成 OpenVINO IR";
    }

    private bool IrUsable => OpenVinoConverter.Ready().Length == 0;

    /// <summary>IR 保留动态形状, 尺寸留到运行时 reshape 就行, 转换期不需要定死.</summary>
    private void SyncShapeBox(bool enabled)
    {
        _shapeBox.Enabled = enabled;
        _tips.SetToolTip(_shapeBox, enabled
            ? "onnx 的输入是动态尺寸时才要填: 输入名:1x3x640x640, 多个输入各写一条分开; "
              + "也可以给三段 输入名:min,opt,max. 模型输入是固定尺寸时填了不生效."
            : "OpenVINO IR 保留动态形状, 转换时不需定尺寸(运行时 reshape 即可), 这一行对 IR 不生效");
    }

    /// <summary>跨架构要 sm80 起每一代 + ptx 的 builder resource 齐备(约 2.1 GB), 缺了只好禁掉.</summary>
    private void SyncCrossArch(bool engineSelected)
    {
        var ok = engineSelected && _tc.CrossArchReady;
        _crossArch.Enabled = ok;
        if (!ok && _crossArch.Checked)
        {
            _crossArch.Checked = false;
            _cfg.CrossArch = false;
        }
        _tips.SetToolTip(_crossArch, ok
            ? "engine 可在 sm80 及以上运行, 但构建更慢、体积更大"
            : "不可用: 跨架构要 sm80 起每一代 + ptx 的 builder resource 齐备(约 2.1 GB), 当前缺 "
              + string.Join(", ", _tc.CrossArchMissing)
              + "。确有需要时用 -p:TrtArch=sm80,sm86,sm89,sm90,sm120,ptx 重新发布。");
    }

    private async Task DetectAsync()
    {
        if (_busy) return;
        _redetect.Enabled = _pickToolchain.Enabled = false;
        _valGpu.Text = _valDriver.Text = _valToolchain.Text = "检测中...";
        _valGpu.ForeColor = _valDriver.ForeColor = _valToolchain.ForeColor = MutedColor;
        try
        {
            var (gpu, tc) = await Task.Run(() =>
            {
                var g = EnvProbe.Probe();
                var t = Toolchain.Resolve(g, _cfg.ToolchainDir);
                return (g, t);
            });
            _gpu = gpu;
            _tc = tc;
            if (_tc.Ready) Toolchain.ApplyToProcessPath(_tc.SearchDirs);
            ShowEnv();
            FitScroll();
            var devPick = gpu.DeviceCount > 1 ? $", 选中第{gpu.DeviceIndex + 1}/{gpu.DeviceCount}张(算力最高)" : "";
            AppendLog(gpu.Available
                ? $"显卡 {gpu.Name} ({gpu.Sm}) x{gpu.DeviceCount}{devPick}, 驱动 {gpu.DriverVersion} (支持 CUDA {gpu.DriverCudaText})"
                : "未检测到可用的 NVIDIA 显卡");
            AppendLog(_tc.Ready
                ? $"工具链 {_tc.DisplayName} ({_tc.Source}), 架构 {string.Join(",", _tc.InstalledArch)}"
                : "工具链不可用: " + _tc.Diagnostic);
            // 用户没主动选过就默认 engine; 环境不支持时 SelectFormat 内部会落回 onnx
            SelectFormat(_formatPickedByUser ? _format : "engine", byUser: false);
        }
        finally
        {
            _redetect.Enabled = _pickToolchain.Enabled = true;
            _cardEngine.Enabled = _gpu.Available && _tc.Ready;
            _cardOpenVino.Enabled = IrUsable;
            _cardEngine.Invalidate();
            _cardOpenVino.Invalidate();
        }
    }

    private void ShowEnv()
    {
        if (_gpu.Available)
        {
            var mem = _gpu.MemoryText.Length > 0 ? " " + _gpu.MemoryText : "";
            var multi = _gpu.DeviceCount > 1 ? $" ×{_gpu.DeviceCount} 用第{_gpu.DeviceIndex + 1}张" : "";
            _valGpu.Text = $"{_gpu.Name}{mem} ({_gpu.SmLabel}){multi}";
            _valGpu.ForeColor = Color.FromArgb(0x20, 0x24, 0x2E);
        }
        else
        {
            _valGpu.Text = string.IsNullOrEmpty(_gpu.Diagnostic) ? "未检测到 NVIDIA 显卡" : _gpu.Diagnostic;
            _valGpu.ForeColor = WarnColor;
        }

        if (_gpu.DriverCuda > 0)
        {
            var ver = _gpu.DriverVersion.Length > 0 ? _gpu.DriverVersion + " " : "";
            _valDriver.Text = $"{ver}(支持 CUDA {_gpu.DriverCudaText})";
            _valDriver.ForeColor = Color.FromArgb(0x20, 0x24, 0x2E);
        }
        else
        {
            _valDriver.Text = _gpu.DriverVersion.Length > 0 ? _gpu.DriverVersion : "--";
            _valDriver.ForeColor = MutedColor;
        }

        if (_tc.Ready)
        {
            var arch = _gpu.Sm.Length > 0 ? $" · {_gpu.Sm} 就绪" : "";
            _valToolchain.Text = $"{_tc.DisplayName} · {_tc.Source}{arch}";
            _valToolchain.ForeColor = _tc.Diagnostic.Length > 0 ? WarnColor : OkColor;
            if (_tc.Diagnostic.Length > 0)
                _valToolchain.Text += " · " + _tc.Diagnostic;
            else if (_tc.MinDriver > 0 && _gpu.DriverVersion.Length > 0 && !DriverEnough(_gpu.DriverVersion, _tc.MinDriver))
                _valToolchain.Text += $" · 驱动低于 r{_tc.MinDriver}, 可能起不来";
        }
        else
        {
            _valToolchain.Text = _tc.Diagnostic.Length > 0
                ? _tc.Diagnostic
                : "缺少文件: " + string.Join(", ", _tc.Missing.Take(3));
            _valToolchain.ForeColor = ErrColor;
        }

        var ovMissing = OpenVinoConverter.Ready();
        _valOv.Text = ovMissing.Length > 0 ? "未包含 (" + ovMissing + ")" : OpenVinoConverter.Version();
        _valOv.ForeColor = ovMissing.Length > 0 ? WarnColor : OkColor;
    }

    private static bool DriverEnough(string driverVersion, int minMajor)
    {
        var head = driverVersion.Split('.')[0];
        return int.TryParse(head, out var v) && v >= minMajor;
    }

    private void PickOnnx()
    {
        using var dlg = new OpenFileDialog
        {
            Title = "选择 onnx 模型",
            Filter = "onnx 模型 (*.onnx)|*.onnx|所有文件 (*.*)|*.*",
        };
        var dir = Path.GetDirectoryName(_onnxBox.Text.Trim());
        if (!string.IsNullOrEmpty(dir) && Directory.Exists(dir)) dlg.InitialDirectory = dir;
        if (dlg.ShowDialog(this) != DialogResult.OK) return;
        _onnxBox.Text = dlg.FileName;
        if (_outBox.Text.Trim().Length == 0)
            _outBox.Text = Path.GetDirectoryName(dlg.FileName) ?? "";
        SelectFormat(_format, byUser: false);
    }

    private void PickOutDir()
    {
        using var dlg = new FolderBrowserDialog { Description = "选择输出目录", SelectedPath = _outBox.Text.Trim() };
        if (dlg.ShowDialog(this) == DialogResult.OK)
            _outBox.Text = dlg.SelectedPath;
    }

    private void PickToolchainDir()
    {
        using var dlg = new FolderBrowserDialog
        {
            Description = "选择 TensorRT 工具链目录 (含 nvinfer_10.dll, 或含 build/ 与 arch/)",
            SelectedPath = _cfg.ToolchainDir,
        };
        if (dlg.ShowDialog(this) != DialogResult.OK) return;
        _cfg.ToolchainDir = dlg.SelectedPath;
        _cfg.Save();
        _ = DetectAsync();
    }

    private void OpenOutputDir()
    {
        var dir = OutputDirFor(_onnxBox.Text.Trim());
        if (dir.Length == 0 || !Directory.Exists(dir))
        {
            MessageBox.Show(this, "输出目录还不存在.", "模型转换", MessageBoxButtons.OK, MessageBoxIcon.Information);
            return;
        }
        Process.Start(new ProcessStartInfo { FileName = "explorer.exe", Arguments = "\"" + dir + "\"", UseShellExecute = true });
    }

    private string OutputDirFor(string onnx)
    {
        var dir = _outBox.Text.Trim();
        if (dir.Length > 0) return dir;
        return onnx.Length > 0 ? Path.GetDirectoryName(onnx) ?? "" : "";
    }

    private async Task RunAsync()
    {
        if (_busy) return;
        var onnx = _onnxBox.Text.Trim();
        if (!File.Exists(onnx))
        {
            MessageBox.Show(this, "请先选择存在的 onnx 模型.", "模型转换", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }
        var outDir = OutputDirFor(onnx);
        if (outDir.Length == 0)
        {
            MessageBox.Show(this, "请先选择输出目录.", "模型转换", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }
        if (_format == "engine" && (!_gpu.Available || !_tc.Ready))
        {
            MessageBox.Show(this, "当前环境无法转换 engine, 请改用 OpenVINO IR, 或先补齐显卡与工具链.",
                "模型转换", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }
        if (_format == "ir" && !IrUsable)
        {
            MessageBox.Show(this, "OpenVINO 运行时不可用: " + OpenVinoConverter.Ready(),
                "模型转换", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        _busy = true;
        _run.Enabled = _redetect.Enabled = _pickToolchain.Enabled = false;
        _bar.Style = ProgressBarStyle.Marquee;
        _cfg.Save();
        try
        {
            if (_format == "ir")
            {
                var name = Path.GetFileNameWithoutExtension(onnx);
                var ir = await Task.Run(() => OpenVinoConverter.Run(onnx, Path.Combine(outDir, name + ".xml"), Fp16, AppendLog));
                if (!ir.Ok) throw new InvalidOperationException(ir.Error);
                AppendLog($"完成: {name}.xml ({ir.XmlBytes / 1024.0:0.#} KB) + {name}.bin ({ir.BinBytes / 1048576.0:0.#} MB), "
                          + $"耗时 {ir.Seconds:0.0}s");
                MessageBox.Show(this,
                    $"转换完成.\n\n{name}.xml + {name}.bin\n"
                    + $"{ir.BinBytes / 1048576.0:0.#} MB, 耗时 {ir.Seconds:0.0} 秒\n"
                    + "两个文件放在一起交给 Python / C++ 的 OpenVINO 运行时即可.",
                    "模型转换", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                var name = Path.GetFileNameWithoutExtension(onnx);
                var req = new ConvertRequest
                {
                    OnnxPath = onnx,
                    EnginePath = Path.Combine(outDir, name + ".engine"),
                    Fp16 = Fp16,
                    CrossArch = _crossArch.Checked,
                    Shapes = _shapeBox.Text.Trim().Length == 0
                        ? Array.Empty<string>()
                        : new[] { _shapeBox.Text.Trim() },
                };
                Directory.CreateDirectory(outDir);
                var result = await Task.Run(() => EngineConverter.Run(req, AppendLog));
                if (!result.Ok) throw new InvalidOperationException(result.Error);
                foreach (var t in result.Tensors) AppendLog("  " + t);
                AppendLog($"完成: {Path.GetFileName(result.EnginePath)} ({result.EngineBytes / 1048576.0:0.#} MB), 构建 {result.BuildSeconds:0.0}s");
                MessageBox.Show(this,
                    $"转换完成.\n\n{Path.GetFileName(result.EnginePath)}\n{result.EngineBytes / 1048576.0:0.#} MB, 耗时 {result.BuildSeconds:0.0} 秒",
                    "模型转换", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            _bar.Style = ProgressBarStyle.Continuous;
            _bar.Value = 100;
        }
        catch (Exception ex)
        {
            _bar.Style = ProgressBarStyle.Continuous;
            _bar.Value = 0;
            AppendLog("失败: " + ex.Message);
            MessageBox.Show(this, "转换失败:\n" + ex.Message, "模型转换", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
        finally
        {
            _busy = false;
            _run.Enabled = _redetect.Enabled = _pickToolchain.Enabled = true;
        }
    }

    /// <summary>转换在后台线程跑, 日志回调必须切回 UI 线程.</summary>
    private void AppendLog(string line)
    {
        if (IsDisposed) return;
        if (InvokeRequired)
        {
            try { BeginInvoke(new Action<string>(AppendLog), line); } catch { }
            return;
        }
        _log.AppendText(DateTime.Now.ToString("[HH:mm:ss] ") + line + Environment.NewLine);
        _log.SelectionStart = _log.TextLength;
        _log.ScrollToCaret();
    }
}
