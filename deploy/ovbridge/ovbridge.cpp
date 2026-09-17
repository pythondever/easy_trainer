// OpenVINO 转换桥接: onnx -> IR(.xml + .bin).
//
// deploy 是 C# 程序, 而 OpenVINO 的 C API(openvino_c.dll)里没有序列化接口
// (只有导出的 compiled blob, 那是绑定设备的, 不能当交付格式), 所以自己封一层 C++.
// 导出的是 C 接口, 参数一律宽字符, 中文路径不用额外转换.

#include <openvino/frontend/manager.hpp>
#include <openvino/openvino.hpp>

#include <windows.h>

#include <filesystem>
#include <string>

namespace
{

void SetErr(wchar_t* err, int cap, const std::wstring& msg)
{
    if (err == nullptr || cap <= 0) return;
    wcsncpy_s(err, static_cast<size_t>(cap), msg.c_str(), _TRUNCATE);
}

// 失败路径之外也要清: 调用方复用同一个 buffer, 不清就会把上一次的报错当成这次的
void Clear(wchar_t* buf, int cap)
{
    if (buf != nullptr && cap > 0) buf[0] = L'\0';
}

// OpenVINO 抛的是窄字符异常(内部消息是 UTF-8), 界面要显示中文得转一次
std::wstring Widen(const std::string& s)
{
    if (s.empty()) return {};
    const int n = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, nullptr, 0);
    if (n <= 1) return {};
    std::wstring out(static_cast<size_t>(n - 1), L'\0');
    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, out.data(), n);
    return out;
}

std::string ShapeText(const ov::PartialShape& ps)
{
    return ps.is_dynamic() ? "dynamic:" + ps.to_string() : ps.to_string();
}

}  // namespace

extern "C"
{

__declspec(dllexport) int ovbridge_version(wchar_t* buf, int cap)
{
    Clear(buf, cap);
    try
    {
        auto v = ov::get_openvino_version();
        std::string s = v.description ? v.description : "";
        if (v.buildNumber != nullptr && *v.buildNumber != '\0')
        {
            s += " (";
            s += v.buildNumber;
            s += ")";
        }
        SetErr(buf, cap, Widen(s));
        return 0;
    }
    catch (...)
    {
        SetErr(buf, cap, L"读取版本失败");
        return 1;
    }
}

// 只读不写: 拿模型的输入输出形状, 让界面在转换前就能显示出来.
__declspec(dllexport) int ovbridge_describe(const wchar_t* onnx, wchar_t* buf, int cap, wchar_t* err, int err_cap)
{
    Clear(buf, cap);
    Clear(err, err_cap);
    try
    {
        ov::Core core;
        auto model = core.read_model(std::filesystem::path(onnx));
        std::string s;
        for (const auto& in : model->inputs())
            s += "in " + in.get_any_name() + " " + ShapeText(in.get_partial_shape()) + "\n";
        for (const auto& out : model->outputs())
            s += "out " + out.get_any_name() + " " + ShapeText(out.get_partial_shape()) + "\n";
        SetErr(buf, cap, Widen(s));
        return 0;
    }
    catch (const std::exception& e) { SetErr(err, err_cap, Widen(e.what())); return 1; }
    catch (...) { SetErr(err, err_cap, L"未知异常"); return 2; }
}

__declspec(dllexport) int ovbridge_convert(const wchar_t* onnx, const wchar_t* xml, int fp16,
                                          wchar_t* err, int err_cap)
{
    Clear(err, err_cap);
    try
    {
        ov::Core core;
        auto model = core.read_model(std::filesystem::path(onnx));
        // save_model 走的是 OVC 的默认流程(必要的图变换 + 权重压 fp16);
        // 换成 ov::serialize 会原样落盘, 权重不减半, 现场就白多一倍体积
        ov::save_model(model, std::filesystem::path(xml), fp16 != 0);
        return 0;
    }
    catch (const std::exception& e) { SetErr(err, err_cap, Widen(e.what())); return 1; }
    catch (...) { SetErr(err, err_cap, L"未知异常 (非 std::exception)"); return 2; }
}

// 加载自检: 让 --probe 能在转换前就跑一遍 Core 构造与 onnx 前端加载,
// 缺 dll / 版本不匹配当场报出来, 不用等用户选好文件才失败.
__declspec(dllexport) int ovbridge_selfcheck(wchar_t* err, int err_cap)
{
    Clear(err, err_cap);
    try
    {
        ov::Core core;
        auto v = ov::get_openvino_version();
        ov::frontend::FrontEndManager fem;
        auto fe = fem.load_by_framework("onnx");   // 只加载不解析, 确认 onnx 前端在位
        std::string s = "OpenVINO ";
        s += (v.description ? v.description : "?");
        s += fe ? " | onnx 前端就绪" : " | onnx 前端缺失";
        SetErr(err, err_cap, Widen(s));
        return fe ? 0 : 1;
    }
    catch (const std::exception& e) { SetErr(err, err_cap, Widen(e.what())); return 1; }
    catch (...) { SetErr(err, err_cap, L"未知异常"); return 2; }
}

}  // extern "C"
