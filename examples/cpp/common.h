// 检测/分割/分类共用的预处理与后处理（头文件形式, 三个示例直接 include）
#pragma once

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

#include <opencv2/opencv.hpp>
#include <onnxruntime_cxx_api.h>

#ifdef _WIN32
#include <windows.h>
#include <shellapi.h>
#pragma comment(lib, "shell32.lib")
#endif

struct Det {
    float x1 = 0, y1 = 0, x2 = 0, y2 = 0;
    float score = 0;
    int cls = 0;
    int query = 0;   // 候选下标, 分割要按它取对应掩码
};

static const float MEAN[3] = {0.485f, 0.456f, 0.406f};
static const float STD[3] = {0.229f, 0.224f, 0.225f};

// BGR 图 → NCHW float, 方形缩放到 size（不保持宽高比, 与训练一致）
inline std::vector<float> preprocess(const cv::Mat& bgr, int size) {
    cv::Mat rgb, resized, f32;
    cv::cvtColor(bgr, rgb, cv::COLOR_BGR2RGB);
    cv::resize(rgb, resized, cv::Size(size, size), 0, 0, cv::INTER_LINEAR);
    resized.convertTo(f32, CV_32FC3, 1.0 / 255.0);

    // 逐像素写 NCHW: 不能用 split + 表达式赋值回写, Mat 赋值是浅拷贝,
    // 表达式会另开内存, 原 buffer 拿不到归一化结果
    std::vector<float> out(3 * size * size);
    for (int y = 0; y < size; ++y) {
        for (int x = 0; x < size; ++x) {
            cv::Vec3f p = f32.at<cv::Vec3f>(y, x);
            for (int c = 0; c < 3; ++c)
                out[c * size * size + y * size + x] = (p[c] - MEAN[c]) / STD[c];
        }
    }
    return out;
}

inline float sigmoid(float v) { return 1.0f / (1.0f + std::exp(-v)); }

// dets [300,4] (cx cy w h 归一化) + labels [300, C+1] logits → 原图像素框
// 最后一列是「无目标」, 只在前 C 列取类别; 300 个候选已端到端去重, 不需要 NMS
inline std::vector<Det> decodeDets(const float* dets, const float* labels,
                                   int numQueries, int numClasses,
                                   int imgW, int imgH, float thr) {
    std::vector<Det> res;
    for (int i = 0; i < numQueries; ++i) {
        const float* logits = labels + i * (numClasses + 1);
        int cls = 0;
        float best = sigmoid(logits[0]);
        for (int c = 1; c < numClasses; ++c) {
            float p = sigmoid(logits[c]);
            if (p > best) { best = p; cls = c; }
        }
        if (best < thr) continue;

        float cx = dets[i * 4 + 0], cy = dets[i * 4 + 1];
        float w = dets[i * 4 + 2], h = dets[i * 4 + 3];
        Det d;
        d.x1 = (cx - w / 2) * imgW;
        d.y1 = (cy - h / 2) * imgH;
        d.x2 = (cx + w / 2) * imgW;
        d.y2 = (cy + h / 2) * imgH;
        d.score = best;
        d.cls = cls;
        d.query = i;
        res.push_back(d);
    }
    return res;
}

// 以下路径/IO 一律以 UTF-8 字符串为准, 需要系统 API 时再转宽字符。
#ifdef _WIN32
inline std::wstring toWide(const std::string& utf8) {
    int n = MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), (int)utf8.size(), nullptr, 0);
    std::wstring w((size_t)(n > 0 ? n : 0), L'\0');
    if (n > 0) MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), (int)utf8.size(), &w[0], n);
    return w;
}

inline std::string toUtf8(const std::wstring& w) {
    int n = WideCharToMultiByte(CP_UTF8, 0, w.c_str(), (int)w.size(), nullptr, 0, nullptr, nullptr);
    std::string s((size_t)(n > 0 ? n : 0), '\0');
    if (n > 0) WideCharToMultiByte(CP_UTF8, 0, w.c_str(), (int)w.size(), &s[0], n, nullptr, nullptr);
    return s;
}
#endif

// Windows 下 ORTCHAR_T 是 wchar_t, 路径要先转宽字符
inline std::basic_string<ORTCHAR_T> ortPath(const std::string& s) {
#ifdef _WIN32
    return toWide(s);
#else
    return s;
#endif
}

// 命令行参数统一取 UTF-8。不能直接用 main 的 argv: Windows 下 CRT 已把它转成
// ANSI 代码页(GBK), 从 PowerShell/cmd 传中文路径会先一步变成乱码。
inline std::vector<std::string> utf8Args(int argc, char** argv) {
    std::vector<std::string> out;
#ifdef _WIN32
    (void)argv;
    int n = 0;
    LPWSTR* wargv = CommandLineToArgvW(GetCommandLineW(), &n);
    if (wargv) {
        for (int i = 1; i < n; ++i) out.push_back(toUtf8(wargv[i]));
        LocalFree(wargv);
    }
#else
    (void)argc;
    for (int i = 1; i < argc; ++i) out.push_back(argv[i]);
#endif
    return out;
}

// 让 printf/std::cout 的 UTF-8 中文在 Windows 控制台正常显示(否则输出乱码)
inline void initConsoleUtf8() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif
}

// 按 UTF-8 路径读整个文件(Windows 走宽字符 ifstream, 绕开 ANSI 代码页)
inline std::vector<char> readFileBytes(const std::string& utf8) {
    std::vector<char> data;
#ifdef _WIN32
    std::ifstream f(toWide(utf8), std::ios::binary);
#else
    std::ifstream f(utf8, std::ios::binary);
#endif
    if (!f) return data;
    f.seekg(0, std::ios::end);
    data.resize((size_t)f.tellg());
    f.seekg(0, std::ios::beg);
    if (!data.empty()) f.read(data.data(), (std::streamsize)data.size());
    return data;
}

// 读图: 先取字节再 imdecode, 等价于 OpenCV 官方推荐的中文路径解法
inline cv::Mat imreadUtf8(const std::string& utf8) {
    std::vector<char> buf = readFileBytes(utf8);
    if (buf.empty()) return cv::Mat();
    return cv::imdecode(buf, cv::IMREAD_COLOR);
}

inline bool writeFileBytes(const std::string& utf8, const std::vector<uchar>& data) {
    if (data.empty()) return false;
#ifdef _WIN32
    std::ofstream f(toWide(utf8), std::ios::binary);
#else
    std::ofstream f(utf8, std::ios::binary);
#endif
    if (!f) return false;
    f.write((const char*)data.data(), (std::streamsize)data.size());
    return true;
}

// 写图同理: 工作目录是中文时 cv::imwrite 一样会失败
inline bool imwriteUtf8(const std::string& utf8, const cv::Mat& img) {
    std::string ext = ".jpg";
    size_t dot = utf8.rfind('.');
    if (dot != std::string::npos) ext = utf8.substr(dot);
    std::vector<uchar> buf;
    if (!cv::imencode(ext, img, buf)) return false;
    return writeFileBytes(utf8, buf);
}

// 模型输入尺寸是静态的, 必须按模型实际的 H 缩放(训练尺寸不一定是 640/224)
inline int inputSize(Ort::Session& s, int fallback) {
    auto shape = s.GetInputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape();
    if (shape.size() == 4 && shape[2] > 0) return (int)shape[2];
    return fallback;
}

// 1.23 起 CreateTensor 必须带 MemoryInfo, 没有四参数的简便重载了
inline Ort::Value makeInput(std::vector<float>& data,
                            const std::vector<int64_t>& shape) {
    Ort::MemoryInfo info =
        Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    return Ort::Value::CreateTensor<float>(info, data.data(), data.size(),
                                           shape.data(), shape.size());
}

// classes.txt: 每行 "id name" 或只有 name, 行号即类别 id
inline std::vector<std::string> loadClasses(const std::string& path) {
    std::vector<std::string> names;
    // 走字节流解析, 中文路径和内容(UTF-8)都能正常读
    std::vector<char> buf = readFileBytes(path);
    std::istringstream f(std::string(buf.begin(), buf.end()));
    std::string line;
    while (std::getline(f, line)) {
        if (line.empty()) continue;
        auto pos = line.find_first_of(" \t");
        if (pos == std::string::npos)
            names.push_back(line);
        else {
            std::string name = line.substr(pos);
            size_t b = name.find_first_not_of(" \t");
            names.push_back(b == std::string::npos ? "" : name.substr(b));
        }
    }
    return names;
}
