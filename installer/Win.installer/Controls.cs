using System.ComponentModel;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

namespace Win.installer;

/// <summary>圆角按钮（主色实心 / 灰底 secondary 两种，带 hover/按下/禁用态）。纯 GDI+ 自绘。</summary>
public sealed class RoundedButton : Button
{
    private bool _hover;
    private bool _down;

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public bool Outline { get; set; }

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public Color Accent { get; set; } = Color.FromArgb(0x2F, 0x6F, 0xED);

    public RoundedButton()
    {
        FlatStyle = FlatStyle.Flat;
        FlatAppearance.BorderSize = 0; // ButtonBase 不允许 BorderColor=Transparent，只能靠 BorderSize=0
        // 关键：把系统主题色全部覆盖成白，避免深色主题下按钮背景透出黑/灰色
        FlatAppearance.MouseOverBackColor = Color.White;
        FlatAppearance.MouseDownBackColor = Color.White;
        FlatAppearance.CheckedBackColor = Color.White;
        BackColor = Color.White;
        UseVisualStyleBackColor = false;
        Cursor = Cursors.Hand;
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint
            | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw
            | ControlStyles.SupportsTransparentBackColor
            | ControlStyles.Opaque, true);
    }

    // 擦底交给 OnPaint 统一处理（真机系统擦底颜色不可控，曾致圆角外四角发黑）
    protected override void OnPaintBackground(PaintEventArgs e) { }

    protected override void OnMouseEnter(EventArgs e) { _hover = true; Invalidate(); base.OnMouseEnter(e); }
    protected override void OnMouseLeave(EventArgs e) { _hover = false; _down = false; Invalidate(); base.OnMouseLeave(e); }
    protected override void OnMouseDown(MouseEventArgs e) { if (e.Button == MouseButtons.Left) { _down = true; Invalidate(); } base.OnMouseDown(e); }
    protected override void OnMouseUp(MouseEventArgs e) { _down = false; Invalidate(); base.OnMouseUp(e); }

    protected override void OnPaint(PaintEventArgs e)
    {
        var g = e.Graphics;
        g.SmoothingMode = SmoothingMode.AntiAlias;
        g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

        // 先铺满父底色再画圆角：圆角外的四角由这里保证，不依赖系统擦底
        using (var bg = new SolidBrush(Parent?.BackColor ?? BackColor))
            g.FillRectangle(bg, ClientRectangle);

        // 铺满整个控件：留 0.5px 外圈会半覆盖，边缘会露出一圈像边框的残影
        var rc = new RectangleF(0f, 0f, Width, Height);

        Color fill, text;
        if (!Enabled)
        {
            fill = Color.FromArgb(0xE7, 0xE9, 0xED);
            text = Color.FromArgb(0x9C, 0xA3, 0xAE);
        }
        else if (Outline)
        {
            // 无边框灰底：白底上靠边框区分的样式在 hover 时对比度不稳，弃用
            fill = _hover ? Color.FromArgb(0xDC, 0xE3, 0xEC) : Color.FromArgb(0xEA, 0xEE, 0xF3);
            text = Accent;
        }
        else
        {
            var c = Accent;
            if (_down) c = ControlPaint.Dark(c, 0.16f);
            else if (_hover) c = ControlPaint.Dark(c, 0.08f);
            fill = c;
            text = Color.White;
        }

        using (var path = RoundedRect(rc, 6f))
        using (var b = new SolidBrush(fill))
            g.FillPath(b, path);

        TextRenderer.DrawText(g, Text, Font, Rectangle.Round(rc), text,
            TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter);
    }

    private static GraphicsPath RoundedRect(RectangleF r, float rad)
    {
        var p = new GraphicsPath();
        float d = rad * 2f;
        p.AddArc(r.X, r.Y, d, d, 180, 90);
        p.AddArc(r.Right - d, r.Y, d, d, 270, 90);
        p.AddArc(r.Right - d, r.Bottom - d, d, d, 0, 90);
        p.AddArc(r.X, r.Bottom - d, d, d, 90, 90);
        p.CloseFigure();
        return p;
    }
}

/// <summary>顶部渐变横幅：深蓝渐变 + 右侧装饰圆环，标题/副题直接画在面板上。</summary>
public sealed class HeaderPanel : Panel
{
    private static readonly Font TitleFont =
        new("Microsoft YaHei UI", 15f, FontStyle.Bold, GraphicsUnit.Point);
    private static readonly Font SubFont =
        new("Microsoft YaHei UI", 9.5f, GraphicsUnit.Point);

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public string Title { get; set; } = "";

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public string SubTitle { get; set; } = "";

    public HeaderPanel()
    {
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint
            | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw
            | ControlStyles.SupportsTransparentBackColor, true);
        BackColor = Color.Transparent;
        Height = 72;
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        var g = e.Graphics;
        g.SmoothingMode = SmoothingMode.AntiAlias;
        using (var b = new LinearGradientBrush(ClientRectangle,
            Color.FromArgb(0x14, 0x39, 0x6B), Color.FromArgb(0x2E, 0x70, 0xE0), 0f))
            g.FillRectangle(b, ClientRectangle);

        using (var pen = new Pen(Color.FromArgb(26, 255, 255, 255), 16f))
            g.DrawEllipse(pen, Width - 90, -28, 120, 120);
        using (var pen = new Pen(Color.FromArgb(16, 255, 255, 255), 10f))
            g.DrawEllipse(pen, Width - 40, 26, 70, 70);

        TextRenderer.DrawText(g, Title, TitleFont, new Point(28, 16), Color.White);
        if (SubTitle.Length > 0)
            TextRenderer.DrawText(g, SubTitle, SubFont, new Point(30, 44), Color.FromArgb(0xC9, 0xD8, 0xF4));
    }
}

/// <summary>VS Installer 风格组件卡片：左侧彩色图标块 + 标题/描述 + 右侧自定义 checkbox。
/// 整张卡可点击切换勾选；hover 浅蓝底、勾选时左侧 3px 蓝色竖条。</summary>
public sealed class ComponentCard : Panel
{
    private static readonly Color CardBg = Color.White;
    private static readonly Color CardBorder = Color.FromArgb(0xDD, 0xE0, 0xE6);
    private static readonly Color HoverBg = Color.FromArgb(0xF0, 0xF5, 0xFF);
    private static readonly Color TitleColor = Color.FromArgb(0x20, 0x24, 0x2E);
    private static readonly Color DescColor = Color.FromArgb(0x6B, 0x72, 0x80);
    private static readonly Color AccentBlue = Color.FromArgb(0x2F, 0x6F, 0xED);
    private static readonly Color CheckBoxBorder = Color.FromArgb(0xC4, 0xC9, 0xD0);
    private static readonly Color MutedBorder = Color.FromArgb(0xE7, 0xE9, 0xED);

    private static readonly Font TitleFont =
        new("Microsoft YaHei UI", 10.5f, FontStyle.Bold, GraphicsUnit.Point);
    private static readonly Font DescFont =
        new("Microsoft YaHei UI", 9f, GraphicsUnit.Point);

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public Component Model { get; }

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public bool IsChecked { get; private set; }

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public bool IsRequired { get; }

    public event Action<ComponentCard, bool>? CheckChanged;

    private bool _hover;
    private Rectangle _checkBoxRect;

    public ComponentCard(Component model, bool initialChecked, bool required)
    {
        Model = model;
        IsChecked = initialChecked;
        IsRequired = required;
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint
            | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw
            | ControlStyles.SupportsTransparentBackColor, true);
        BackColor = Color.Transparent;
        Cursor = Cursors.Hand;
        Margin = new Padding(0, 0, 14, 14);
        Size = new Size(360, 100);
    }

    public void SetCheckedSilent(bool value)
    {
        if (IsChecked == value) return;
        IsChecked = value;
        Invalidate();
    }

    protected override void OnMouseEnter(EventArgs e) { _hover = true; Invalidate(); base.OnMouseEnter(e); }
    protected override void OnMouseLeave(EventArgs e) { _hover = false; Invalidate(); base.OnMouseLeave(e); }
    protected override void OnMouseDown(MouseEventArgs e)
    {
        if (e.Button == MouseButtons.Left && !IsRequired)
        {
            IsChecked = !IsChecked;
            CheckChanged?.Invoke(this, IsChecked);
            Invalidate();
        }
        base.OnMouseDown(e);
    }

    protected override void OnResize(EventArgs e)
    {
        // 重新计算 checkbox 区域（卡片右上角）
        var box = 20;
        _checkBoxRect = new Rectangle(Width - box - 16, (Height - box) / 2, box, box);
        base.OnResize(e);
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        var g = e.Graphics;
        g.SmoothingMode = SmoothingMode.AntiAlias;
        g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

        var rc = new Rectangle(0, 0, Width - 1, Height - 1);

        // 背景：白底，hover 时浅蓝
        var bg = _hover && !IsRequired ? HoverBg : CardBg;
        var border = IsRequired ? MutedBorder : CardBorder;
        using (var path = RoundedRect(rc, 8f))
        using (var b = new SolidBrush(bg))
            g.FillPath(b, path);
        using (var pen = new Pen(border, 1f))
        using (var path = RoundedRect(rc, 8f))
            g.DrawPath(pen, path);

        // 勾选状态：左侧 3px 蓝色竖条 + 卡片轻微阴影感（用边线加重）
        if (IsChecked)
        {
            using var pen = new Pen(AccentBlue, 3f);
            g.DrawLine(pen, 4, 12, 4, Height - 12);
        }

        // 标题 + 描述
        var textX = 16;
        var textW = _checkBoxRect.Left - textX - 12;
        var titleRect = new Rectangle(textX, 20, textW, 22);
        var descRect = new Rectangle(textX, 44, textW, Height - 50);
        TextRenderer.DrawText(g, Model.Title, TitleFont, titleRect,
            IsRequired ? MutedBorder : TitleColor,
            TextFormatFlags.Left | TextFormatFlags.Top | TextFormatFlags.EndEllipsis);
        TextRenderer.DrawText(g, Model.Desc, DescFont, descRect,
            DescColor,
            TextFormatFlags.Left | TextFormatFlags.Top | TextFormatFlags.WordBreak | TextFormatFlags.EndEllipsis);

        // 右侧 checkbox
        DrawCheckBox(g, _checkBoxRect, IsChecked);
    }

    private void DrawCheckBox(Graphics g, Rectangle box, bool check)
    {
        // 底圆角矩形
        using (var path = RoundedRect(box, 4f))
        {
            if (check)
            {
                using var b = new SolidBrush(AccentBlue);
                g.FillPath(b, path);
            }
            else
            {
                using var b = new SolidBrush(Color.White);
                g.FillPath(b, path);
                using var pen = new Pen(CheckBoxBorder, 1.5f);
                g.DrawPath(pen, path);
            }
        }
        if (!check) return;

        // 白色对勾
        using var pen2 = new Pen(Color.White, 2.2f) { StartCap = LineCap.Round, EndCap = LineCap.Round };
        var p1 = new PointF(box.X + box.Width * 0.22f, box.Y + box.Height * 0.52f);
        var p2 = new PointF(box.X + box.Width * 0.44f, box.Y + box.Height * 0.72f);
        var p3 = new PointF(box.X + box.Width * 0.78f, box.Y + box.Height * 0.30f);
        g.DrawLines(pen2, new[] { p1, p2, p3 });
    }

    private static GraphicsPath RoundedRect(Rectangle r, float rad)
    {
        var p = new GraphicsPath();
        var rf = new RectangleF(r.X, r.Y, r.Width, r.Height);
        float d = rad * 2f;
        p.AddArc(rf.X, rf.Y, d, d, 180, 90);
        p.AddArc(rf.Right - d, rf.Y, d, d, 270, 90);
        p.AddArc(rf.Right - d, rf.Bottom - d, d, d, 0, 90);
        p.AddArc(rf.X, rf.Bottom - d, d, d, 90, 90);
        p.CloseFigure();
        return p;
    }
    private static GraphicsPath RoundedRect(RectangleF rf, float rad)
    {
        var p = new GraphicsPath();
        float d = rad * 2f;
        p.AddArc(rf.X, rf.Y, d, d, 180, 90);
        p.AddArc(rf.Right - d, rf.Y, d, d, 270, 90);
        p.AddArc(rf.Right - d, rf.Bottom - d, d, d, 0, 90);
        p.AddArc(rf.X, rf.Bottom - d, d, d, 90, 90);
        p.CloseFigure();
        return p;
    }
}