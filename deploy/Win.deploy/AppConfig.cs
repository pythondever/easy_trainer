using System.Text.Json;

namespace Win.deploy;

/// <summary>用户设置, 落在 %LOCALAPPDATA%\EasyTrainer Deploy\config.json.</summary>
public sealed class AppConfig
{
    public string ToolchainDir { get; set; } = "";
    public string LastOnnxDir { get; set; } = "";
    public string OutputDir { get; set; } = "";
    public bool Fp16 { get; set; } = true;
    public bool CrossArch { get; set; }

    private static string Dir =>
        Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "EasyTrainer Deploy");

    private static string FilePath => Path.Combine(Dir, "config.json");

    public static AppConfig Load()
    {
        try
        {
            if (File.Exists(FilePath))
                return JsonSerializer.Deserialize<AppConfig>(File.ReadAllText(FilePath)) ?? new AppConfig();
        }
        catch { }
        return new AppConfig();
    }

    public void Save()
    {
        try
        {
            Directory.CreateDirectory(Dir);
            File.WriteAllText(FilePath, JsonSerializer.Serialize(this, new JsonSerializerOptions { WriteIndented = true }));
        }
        catch { }
    }
}
