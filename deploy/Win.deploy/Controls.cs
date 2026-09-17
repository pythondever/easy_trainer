using System.ComponentModel;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

namespace Win.deploy;

/// <summary>回溯到最近一个不透明祖先的底色.</summary>
internal static class BackDrop
{
    // 自绘圆角控件必须自己把四角填成它: 双缓冲的缓冲区是未初始化的, 跳过擦底不等于"透明", 四角会落成黑色
    internal static Color Of(Control? c)
    {
        for (var p = c; p != null; p = p.Parent)
            if (p.BackColor.A == 255) return p.BackColor;
        return SystemColors.Control;
    }

    // 四边各外扩 1px 再填: 开抗锯齿后 GDI+ 把矩形最外一行/一列的覆盖率算成 50%(角上 25%),
    // 而缓冲区初始全透明 -> 这圈半透明像素拷到屏幕上就是圆角外那几像素的"黑边". 外扩后可见像素全在矩形内部, 覆盖率回到 100%
    internal static void Fill(Control c, Graphics g, Brush brush)
    {
        var rc = c.ClientRectangle;
        g.FillRectangle(brush, rc.X - 1, rc.Y - 1, rc.Width + 2, rc.Height + 2);
    }
}

/// <summary>圆角按钮(主色实心 / 灰底 secondary 两种, 带 hover/按下/禁用态). 纯 GDI+ 自绘.</summary>
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
        FlatAppearance.BorderSize = 0; // ButtonBase 不允许 BorderColor=Transparent, 只能靠 BorderSize=0
        // 把系统主题色全部覆盖成白, 避免深色主题下按钮背景透出黑/灰色
        FlatAppearance.MouseOverBackColor = Color.White;
        FlatAppearance.MouseDownBackColor = Color.White;
        FlatAppearance.CheckedBackColor = Color.White;
        BackColor = Color.White;
        UseVisualStyleBackColor = false;
        Cursor = Cursors.Hand;
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint
            | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw
            | ControlStyles.SupportsTransparentBackColor | ControlStyles.Opaque, true);
    }

    // 擦底交给 OnPaint 统一处理(真机系统擦底颜色不可控, 曾致圆角外四角发黑)
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

        using (var bg = new SolidBrush(BackDrop.Of(Parent)))
            BackDrop.Fill(this, g, bg);

        // 铺满整个控件: 留 0.5px 外圈会半覆盖, 边缘会露出一圈像边框的残影
        var rc = new RectangleF(0f, 0f, Width, Height);

        Color fill, text;
        if (!Enabled)
        {
            fill = Color.FromArgb(0xE7, 0xE9, 0xED);
            text = Color.FromArgb(0x9C, 0xA3, 0xAE);
        }
        else if (Outline)
        {
            // 无边框灰底: 白底上靠边框区分的样式在 hover 时对比度不稳, 弃用
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

    internal static GraphicsPath RoundedRect(RectangleF r, float rad)
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

/// <summary>顶部渐变横幅: 深蓝渐变 + 右侧装饰圆环, 标题/副题直接画在面板上.</summary>
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
            BackDrop.Fill(this, g, b);

        using (var pen = new Pen(Color.FromArgb(26, 255, 255, 255), 16f))
            g.DrawEllipse(pen, Width - 90, -28, 120, 120);
        using (var pen = new Pen(Color.FromArgb(16, 255, 255, 255), 10f))
            g.DrawEllipse(pen, Width - 40, 26, 70, 70);

        TextRenderer.DrawText(g, Title, TitleFont, new Point(28, 16), Color.White);
        if (SubTitle.Length > 0)
            TextRenderer.DrawText(g, SubTitle, SubFont, new Point(30, 44), Color.FromArgb(0xC9, 0xD8, 0xF4));
    }
}

/// <summary>白底圆角容器, 用来框住环境状态这类成组信息.</summary>
public sealed class CardPanel : Panel
{
    public CardPanel()
    {
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint
            | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
        BackColor = Color.White;
        Padding = new Padding(16, 12, 16, 12);
    }

    // 擦底与圆角外的四角都交给 OnPaint: 系统擦底会刷成整块矩形, 而完全不擦又留黑角
    protected override void OnPaintBackground(PaintEventArgs e) { }

    protected override void OnPaint(PaintEventArgs e)
    {
        var g = e.Graphics;
        g.SmoothingMode = SmoothingMode.AntiAlias;

        using (var bg = new SolidBrush(BackDrop.Of(Parent)))
            BackDrop.Fill(this, g, bg);

        var rc = new RectangleF(0f, 0f, Width - 1f, Height - 1f);
        using (var path = RoundedButton.RoundedRect(rc, 8f))
        using (var b = new SolidBrush(Color.White))
            g.FillPath(b, path);
        using (var path = RoundedButton.RoundedRect(rc, 8f))
        using (var pen = new Pen(Color.FromArgb(0xDD, 0xE0, 0xE6), 1f))
            g.DrawPath(pen, path);
    }
}

/// <summary>目标格式选择卡片(单选). 整卡可点; 不可用时灰化, 点击无响应.</summary>
public sealed class SelectCard : Panel
{
    private static readonly Color CardBg = Color.White;
    private static readonly Color HoverBg = Color.FromArgb(0xF0, 0xF5, 0xFF);
    private static readonly Color DisabledBg = Color.FromArgb(0xF7, 0xF8, 0xFA);
    private static readonly Color BorderColor = Color.FromArgb(0xDD, 0xE0, 0xE6);
    private static readonly Color TitleColor = Color.FromArgb(0x20, 0x24, 0x2E);
    private static readonly Color DescColor = Color.FromArgb(0x6B, 0x72, 0x80);
    private static readonly Color MutedColor = Color.FromArgb(0xA8, 0xAE, 0xB8);
    private static readonly Color AccentBlue = Color.FromArgb(0x2F, 0x6F, 0xED);

    private static readonly Font TitleFont =
        new("Microsoft YaHei UI", 10.5f, FontStyle.Bold, GraphicsUnit.Point);
    private static readonly Font DescFont =
        new("Microsoft YaHei UI", 9f, GraphicsUnit.Point);

    private bool _hover;
    private bool _selected;

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public string Title { get; set; } = "";

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public string Description { get; set; } = "";

    [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
    public bool Selected
    {
        get => _selected;
        set { if (_selected == value) return; _selected = value; Invalidate(); }
    }

    public event Action<SelectCard>? Picked;

    public SelectCard()
    {
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint
            | ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
        BackColor = CardBg;
        Cursor = Cursors.Hand;
        Size = new Size(340, 92);
    }

    protected override void OnPaintBackground(PaintEventArgs e) { }

    protected override void OnMouseEnter(EventArgs e) { _hover = true; Invalidate(); base.OnMouseEnter(e); }
    protected override void OnMouseLeave(EventArgs e) { _hover = false; Invalidate(); base.OnMouseLeave(e); }
    protected override void OnMouseDown(MouseEventArgs e)
    {
        if (e.Button == MouseButtons.Left && Enabled) Picked?.Invoke(this);
        base.OnMouseDown(e);
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        var g = e.Graphics;
        g.SmoothingMode = SmoothingMode.AntiAlias;
        g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

        using (var back = new SolidBrush(BackDrop.Of(Parent)))
            BackDrop.Fill(this, g, back);

        var rc = new RectangleF(0f, 0f, Width - 1f, Height - 1f);
        var bg = !Enabled ? DisabledBg : _hover ? HoverBg : CardBg;
        using (var path = RoundedButton.RoundedRect(rc, 8f))
        using (var b = new SolidBrush(bg))
            g.FillPath(b, path);
        using (var path = RoundedButton.RoundedRect(rc, 8f))
        using (var pen = new Pen(_selected && Enabled ? AccentBlue : BorderColor, _selected && Enabled ? 1.4f : 1f))
            g.DrawPath(pen, path);

        if (_selected && Enabled)
        {
            using var pen = new Pen(AccentBlue, 3f);
            g.DrawLine(pen, 4, 12, 4, Height - 12);
        }

        var box = 18;
        var circle = new Rectangle(Width - box - 16, (Height - box) / 2, box, box);
        using (var path = new GraphicsPath())
        {
            path.AddEllipse(circle);
            using var b = new SolidBrush(_selected && Enabled ? AccentBlue : Color.White);
            g.FillPath(b, path);
            if (!(_selected && Enabled))
            {
                using var pen = new Pen(Enabled ? Color.FromArgb(0xC4, 0xC9, 0xD0) : MutedColor, 1.5f);
                g.DrawPath(pen, path);
            }
        }
        if (_selected && Enabled)
        {
            using var b = new SolidBrush(Color.White);
            g.FillEllipse(b, circle.X + 6, circle.Y + 6, box - 12, box - 12);
        }

        var textX = 16;
        var textW = circle.Left - textX - 12;
        TextRenderer.DrawText(g, Title, TitleFont, new Rectangle(textX, 20, textW, 22),
            Enabled ? TitleColor : MutedColor,
            TextFormatFlags.Left | TextFormatFlags.Top | TextFormatFlags.EndEllipsis);
        TextRenderer.DrawText(g, Description, DescFont, new Rectangle(textX, 44, textW, Height - 50),
            MutedColor,
            TextFormatFlags.Left | TextFormatFlags.Top | TextFormatFlags.WordBreak | TextFormatFlags.EndEllipsis);
    }
}
