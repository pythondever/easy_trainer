using System.Runtime.InteropServices;
using System.Text;

namespace Win.deploy;

public sealed class GpuInfo
{
    /// <summary>CUDA 驱动可用且至少有一块卡.</summary>
    public bool Available { get; set; }
    public int DeviceCount { get; set; }
    /// <summary>选中的卡序号. 多卡时按算力最高挑, 不一定是 0.</summary>
    public int DeviceIndex { get; set; }
    public string Name { get; set; } = "";
    public int CcMajor { get; set; }
    public int CcMinor { get; set; }
    public long MemoryBytes { get; set; }
    /// <summary>NVML 报的驱动号, 形如 576.88; NVML 不可用时为空.</summary>
    public string DriverVersion { get; set; } = "";
    /// <summary>cuDriverGetVersion 的原始值, 12090 表示驱动支持到 CUDA 12.9.</summary>
    public int DriverCuda { get; set; }
    public string Diagnostic { get; set; } = "";

    /// <summary>TensorRT 的文件/目录名用 sm89 这种无下划线写法.</summary>
    public string Sm => CcMajor > 0 ? $"sm{CcMajor}{CcMinor}" : "";
    /// <summary>给人看的写法.</summary>
    public string SmLabel => CcMajor > 0 ? $"sm_{CcMajor}{CcMinor}" : "";
    public string DriverCudaText => DriverCuda >= 1000 ? $"{DriverCuda / 1000}.{DriverCuda % 1000 / 10:0}" : "";
    public string MemoryText => MemoryBytes > 0 ? $"{MemoryBytes / 1073741824.0:0.#} GB" : "";
}

/// <summary>
/// 显卡探测走 CUDA Driver API 而不是调用 nvidia-smi: 后者要起进程(约 1s)且客户机不一定在 PATH 里,
/// 而 nvcuda.dll 是驱动自带的系统组件, 直接 LoadLibrary 更可靠.
/// 驱动号另走 NVML(可选) —— CUDA 只报"支持到哪个 CUDA 版本", 界面上显示具体驱动号更直观.
/// </summary>
public static class EnvProbe
{
    private const int CudaSuccess = 0;
    private const int AttrCcMajor = 75;
    private const int AttrCcMinor = 76;

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int CuInit(uint flags);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int CuDeviceGetCount(out int count);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int CuDeviceGetName(byte[] name, int len, int dev);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int CuDeviceGetAttribute(out int value, int attrib, int dev);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int CuDriverGetVersion(out int version);
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int CuDeviceTotalMem(ref ulong bytes, int dev);

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int NvmlInit();
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)] private delegate int NvmlSystemGetDriverVersion(byte[] version, uint length);

    public static GpuInfo Probe()
    {
        var g = new GpuInfo();
        IntPtr h;
        try
        {
            if (!NativeLibrary.TryLoad("nvcuda.dll", out h))
            {
                g.Diagnostic = "未找到 nvcuda.dll, 未安装 NVIDIA 驱动";
                g.DriverVersion = NvmlDriverVersion();
                return g;
            }
        }
        catch (Exception ex)
        {
            g.Diagnostic = "加载 nvcuda.dll 失败: " + ex.Message;
            return g;
        }

        try
        {
            var init = Bind<CuInit>(h, "cuInit");
            var rc = init(0);
            if (rc != CudaSuccess)
            {
                g.Diagnostic = $"cuInit 失败 (CUresult={rc}), 驱动异常";
                return g;
            }

            var getCount = Bind<CuDeviceGetCount>(h, "cuDeviceGetCount");
            if (getCount(out var n) != CudaSuccess || n <= 0)
            {
                g.Diagnostic = "未检测到 CUDA 设备";
                return g;
            }
            g.Available = true;
            g.DeviceCount = n;

            var getAttr = Bind<CuDeviceGetAttribute>(h, "cuDeviceGetAttribute");

            // 0 号卡常是亮机卡(核显/老卡), 按它定架构会取错 builder resource;
            // 遍历所有卡挑算力最高的一张, 后续查询都用它
            var pick = 0;
            var pickScore = -1;
            for (var i = 0; i < n; i++)
            {
                var score = 0;
                if (getAttr(out var mj, AttrCcMajor, i) == CudaSuccess
                    && getAttr(out var mn, AttrCcMinor, i) == CudaSuccess)
                    score = mj * 100 + mn;
                if (score > pickScore) { pickScore = score; pick = i; }
            }
            g.DeviceIndex = pick;

            var getName = Bind<CuDeviceGetName>(h, "cuDeviceGetName");
            var buf = new byte[256];
            if (getName(buf, buf.Length, pick) == CudaSuccess)
                g.Name = Encoding.ASCII.GetString(buf).TrimEnd('\0');

            if (getAttr(out var maj, AttrCcMajor, pick) == CudaSuccess) g.CcMajor = maj;
            if (getAttr(out var min, AttrCcMinor, pick) == CudaSuccess) g.CcMinor = min;

            try
            {
                var getMem = Bind<CuDeviceTotalMem>(h, "cuDeviceTotalMem_v2");
                ulong mem = 0;
                if (getMem(ref mem, pick) == CudaSuccess) g.MemoryBytes = (long)mem;
            }
            catch (EntryPointNotFoundException) { }

            var getVer = Bind<CuDriverGetVersion>(h, "cuDriverGetVersion");
            if (getVer(out var v) == CudaSuccess) g.DriverCuda = v;
        }
        catch (EntryPointNotFoundException ex)
        {
            g.Diagnostic = "nvcuda.dll 缺少预期导出: " + ex.Message;
        }
        catch (Exception ex)
        {
            g.Diagnostic = "探测显卡时出错: " + ex.Message;
        }

        g.DriverVersion = NvmlDriverVersion();
        NativeLibrary.Free(h);
        return g;
    }

    private static T Bind<T>(IntPtr lib, string name) where T : Delegate
        => Marshal.GetDelegateForFunctionPointer<T>(NativeLibrary.GetExport(lib, name));

    /// <summary>NVML 取驱动版本; 加载不到不算错误, 只影响界面显示.</summary>
    private static string NvmlDriverVersion()
    {
        foreach (var candidate in NvmlCandidates())
        {
            try
            {
                if (!NativeLibrary.TryLoad(candidate, out var h)) continue;
                try
                {
                    var init = Bind<NvmlInit>(h, "nvmlInit_v2");
                    if (init() != 0) continue;
                    var get = Bind<NvmlSystemGetDriverVersion>(h, "nvmlSystemGetDriverVersion");
                    var buf = new byte[96];
                    if (get(buf, (uint)buf.Length) == 0)
                    {
                        var s = Encoding.ASCII.GetString(buf).TrimEnd('\0');
                        if (s.Length > 0) return s;
                    }
                }
                finally { NativeLibrary.Free(h); }
            }
            catch { }
        }
        return "";
    }

    private static IEnumerable<string> NvmlCandidates()
    {
        var sys = Environment.GetFolderPath(Environment.SpecialFolder.System);
        yield return Path.Combine(sys, "nvml.dll");
        var pf = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles);
        yield return Path.Combine(pf, "NVIDIA Corporation", "NVSMI", "nvml.dll");
        yield return "nvml.dll";
    }
}
