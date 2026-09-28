using System.Diagnostics;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Win.deploy;

public sealed class MainForm : Form
{
    /// <summary>「输入尺寸」那一行的三种形态: 手写框 / 只读形状 / 动态维数字框.</summary>
    private enum ShapeMode { Manual, ReadOnly, Boxes }

    /// <summary>
    /// 动态维的数字框怎么拼回 shape: Template 是已经定好的完整形状(固定维取模型值,
    /// batch 维按 1, 其余动态维先给默认值), Boxes 只覆盖用户能改的那几维.
    /// </summary>
    private sealed class DynPlan
    {
        public string Name = "";
        public int[] Template = Array.Empty<int>();
        public readonly List<(int Dim, NumericUpDown Box)> Boxes = new();
    }

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
    private readonly Label _shapeInfo = new();
    private readonly FlowLayoutPanel _shapeDyn = new();
    private readonly List<DynPlan> _dynPlans = new();
    private List<InputShapeInfo> _probed = new();
    private string _probedOnnx = "";
    private bool _probing;
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
        content.Controls.Add(BuildShapeRow(), 0, 7);
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
        if (onBrowse is null) return row;   // 没有浏览回调就不放按钮

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

    /// <summary>「输入尺寸」那一行: 手写框 / 只读形状 / 动态维数字框 三种形态共用一格.</summary>
    private Control BuildShapeRow()
    {
        var row = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            ColumnCount = 2,
            RowCount = 1,
            Margin = new Padding(0),
            BackColor = PageBg,
        };
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 68));
        row.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        row.RowStyles.Add(new RowStyle(SizeType.Absolute, 34));

        row.Controls.Add(new Label
        {
            Text = "输入尺寸",
            ForeColor = MutedColor,
            Dock = DockStyle.Fill,
            TextAlign = ContentAlignment.MiddleLeft,
            Margin = new Padding(0, 0, 0, 0),
        }, 0, 0);

        _shapeBox.BorderStyle = BorderStyle.FixedSingle;
        _shapeBox.Font = new Font("Microsoft YaHei UI", 9.5f);
        _shapeBox.Dock = DockStyle.Fill;
        _shapeBox.Margin = new Padding(0, 6, 8, 6);
        _shapeBox.PlaceholderText = "模型的输入是动态尺寸时才填, 如 images:1x3x640x640";

        _shapeInfo.AutoSize = false;
        _shapeInfo.Dock = DockStyle.Fill;
        _shapeInfo.AutoEllipsis = true;
        _shapeInfo.TextAlign = ContentAlignment.MiddleLeft;
        _shapeInfo.Margin = new Padding(0, 0, 8, 0);

        _shapeDyn.Dock = DockStyle.Fill;
        _shapeDyn.Margin = new Padding(0);
        _shapeDyn.WrapContents = false;   // 行高固定, 换行会被裁掉; 铺不下时改走手写框(见 ApplyProbed)
        _shapeDyn.AutoScroll = false;

        var host = new Panel { Dock = DockStyle.Fill, Margin = new Padding(0), BackColor = PageBg };
        host.Controls.Add(_shapeBox);
        host.Controls.Add(_shapeInfo);
        host.Controls.Add(_shapeDyn);
        row.Controls.Add(host, 1, 0);
        return row;
    }

    private void SetShapeMode(ShapeMode mode)
    {
        _shapeBox.Visible = mode == ShapeMode.Manual;
        _shapeInfo.Visible = mode == ShapeMode.ReadOnly;
        _shapeDyn.Visible = mode == ShapeMode.Boxes;
    }

    /// <summary>按"当前目标格式 + 探测结果"决定这一行长什么样.</summary>
    private void RefreshShapeRow()
    {
        if (_format != "engine")
        {
            _shapeInfo.ForeColor = MutedColor;
            _shapeInfo.Text = "OpenVINO IR 保留动态形状, 转换时不需定尺寸(运行时 reshape 即可), 这一行对 IR 不生效";
            SetShapeMode(ShapeMode.ReadOnly);
            return;
        }
        if (_probed.Count > 0 && _probedOnnx == _onnxBox.Text.Trim())
        {
            ApplyProbed();
            return;
        }
        SetShapeMode(ShapeMode.Manual);   // 还没读到形状: 留着输入框, 用户手填仍然算数
    }

    private void ApplyProbed()
    {
        _shapeDyn.Controls.Clear();
        _dynPlans.Clear();      // 切到别的形态时靠这里清掉, 否则 CollectShapes 会拿旧框的值

        var need = _probed.Where(x => x.NeedsValue).ToList();
        if (need.Count == 0)
        {
            _shapeInfo.ForeColor = MutedColor;
            _shapeInfo.Text = string.Join("   ", _probed.Select(x => x.Name + "  " + x.Text
                + (x.DynamicAt.Length > 0 ? "  (batch 维动态, 按 1 处理)" : "")))
                + "  — 输入是固定尺寸, 无需指定";
            SetShapeMode(ShapeMode.ReadOnly);
            return;
        }
        // 数字框铺不下"多个输入 + 长维度"这类情形(行高固定, 超宽会被裁):
        // 退回手写框, 但把输入名与固定维都填好, 用户只可能改数字
        if (need.Count > 1 || need[0].Dims.Length > 4)
        {
            _shapeBox.Text = string.Join("; ", need.Select(x => x.Name + ":" + PrefillDims(x)));
            SetShapeMode(ShapeMode.Manual);
            return;
        }

        var inp = need[0];
        var plan = new DynPlan { Name = inp.Name, Template = new int[inp.Dims.Length] };
        for (var k = 0; k < inp.Dims.Length; k++)
            plan.Template[k] = inp.Dims[k] > 0 ? inp.Dims[k] : (k == 0 ? 1 : 640);

        _shapeDyn.Controls.Add(DimLabel(inp.Name + " :"));
        for (var k = 0; k < inp.Dims.Length; k++)
        {
            if (k > 0) _shapeDyn.Controls.Add(DimLabel("x"));
            if (inp.Dims[k] > 0)
            {
                _shapeDyn.Controls.Add(DimLabel(inp.Dims[k].ToString()));
                continue;
            }
            // batch 维动态时构建期本来就按 1 处理, 不开放给用户改(改大吃显存)
            if (k == 0)
            {
                _shapeDyn.Controls.Add(DimLabel("1"));
                continue;
            }
            var box = new NumericUpDown
            {
                Minimum = 1,
                Maximum = 8192,
                Value = 640,
                Width = 64,
                Font = new Font("Microsoft YaHei UI", 9.5f),
                Margin = new Padding(0, 4, 6, 0),
            };
            _shapeDyn.Controls.Add(box);
            plan.Boxes.Add((k, box));
        }
        _dynPlans.Add(plan);
        SetShapeMode(ShapeMode.Boxes);
    }

    private static Label DimLabel(string text)
        => new()
        {
            Text = text,
            ForeColor = MutedColor,
            AutoSize = true,
            Margin = new Padding(0, 8, 6, 0),
        };

    /// <summary>退回手写框时的预填值: batch 维按 1, 其余动态维先按 640; 输入名与固定维都从模型里来.</summary>
    private static string PrefillDims(InputShapeInfo x)
        => string.Join("x", x.Dims.Select((d, k) => d > 0 ? d.ToString() : k == 0 ? "1" : "640"));

    /// <summary>把手写框或数字框里的值收成 engine 要的 Shapes; 没有需要用户给的维时返回空.</summary>
    private string[] CollectShapes()
    {
        if (_dynPlans.Count > 0 && _shapeDyn.Visible)
        {
            return _dynPlans.Select(p =>
            {
                var dims = (int[])p.Template.Clone();
                foreach (var (dim, box) in p.Boxes) dims[dim] = (int)box.Value;
                return p.Name + ":" + string.Join("x", dims);
            }).ToArray();
        }
        // 分号分隔多个输入: ParseShapes 的逗号是 min/opt/max 的分隔, 两个输入必须给两个元素
        return _shapeBox.Text.Split(';', StringSplitOptions.RemoveEmptyEntries)
            .Select(s => s.Trim())
            .Where(s => s.Length > 0)
            .ToArray();
    }

    /// <summary>读 onnx 的输入形状. 读不出来不算错: 手写框仍是有效入口, 只记一行日志.</summary>
    private async Task ProbeOnnxAsync(string onnx)
    {
        if (_probing || _busy) return;
        if (onnx.Length == 0 || !File.Exists(onnx)) return;
        if (_probedOnnx == onnx) return;                 // 同一个文件不重复探
        if (!(_gpu.Available && _tc.Ready)) return;      // 没有 TensorRT 就只能手写
        _probing = true;
        try
        {
            var r = await Task.Run(() => EngineConverter.ProbeInputs(onnx, AppendLog));
            if (!r.Ok)
            {
                AppendLog("读不出输入形状(不影响手工填写): " + r.Error);
                return;
            }
            _probed = r.Inputs;
            _probedOnnx = onnx;
            AppendLog("输入形状: " + string.Join(", ", r.Inputs.Select(x => x.Name + " [" + x.Text + "]"))
                + (_probed.Any(x => x.NeedsValue) ? " — 有动态维, 请在「输入尺寸」里填" : " — 尺寸固定, 无需指定"));
            RefreshShapeRow();
        }
        catch (Exception ex)
        {
            AppendLog("读输入形状出错(不影响手工填写): " + ex.Message);
        }
        finally
        {
            _probing = false;
        }
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
    }

    private bool IrUsable => OpenVinoConverter.Ready().Length == 0;

    /// <summary>IR 保留动态形状, 尺寸留到运行时 reshape 就行, 转换期不需要定死.</summary>
    private void SyncShapeBox(bool engineSelected)
    {
        _shapeBox.Enabled = _shapeDyn.Enabled = engineSelected;
        _tips.SetToolTip(_shapeBox, "onnx 的输入是动态尺寸时才要填: 输入名:1x3x640x640; "
            + "多个输入用分号隔开; 也可以给三段 输入名:min,opt,max. 模型输入是固定尺寸时填了不生效.");
        _tips.SetToolTip(_shapeInfo, "从 onnx 里读到的输入形状");
        _tips.SetToolTip(_shapeDyn, "方框是动态维的取值(填部署时实际要用的输入尺寸), 灰字维是模型里固定的; batch 维按 1 构建");
        RefreshShapeRow();
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
            _ = ProbeOnnxAsync(_onnxBox.Text.Trim());
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
        _ = ProbeOnnxAsync(_onnxBox.Text.Trim());
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
        // 手改过路径(没走选文件那条路)时在这里补探一次: 不探就不知道该不该让用户填尺寸
        if (_format == "engine") await ProbeOnnxAsync(onnx);
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
                    Shapes = CollectShapes(),
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
