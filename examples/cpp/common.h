// 检测/分割/分类共用的预处理与后处理（头文件形式, 三个示例直接 include）
#pragma once

#include <algorithm>
#include <cctype>
#include <cmath>
#include <cstdio>
#include <fstream>
#include <sstream>
#include <string>
#include <utility>
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

// ---- label_map.json 的极简解析 ----
// 导出格式固定是 {"类名": 数字, ...} 这种平铺对象, 不为此引入 JSON 库.
inline bool endsWithNoCase(const std::string& s, const std::string& suf) {
    if (s.size() < suf.size()) return false;
    size_t off = s.size() - suf.size();
    for (size_t k = 0; k < suf.size(); ++k)
        if (tolower((unsigned char)s[off + k]) != tolower((unsigned char)suf[k]))
            return false;
    return true;
}

inline void appendUtf8(std::string& out, unsigned int cp) {
    if (cp < 0x80) {
        out.push_back((char)cp);
    } else if (cp < 0x800) {
        out.push_back((char)(0xC0 | (cp >> 6)));
        out.push_back((char)(0x80 | (cp & 0x3F)));
    } else if (cp < 0x10000) {
        out.push_back((char)(0xE0 | (cp >> 12)));
        out.push_back((char)(0x80 | ((cp >> 6) & 0x3F)));
        out.push_back((char)(0x80 | (cp & 0x3F)));
    } else {
        out.push_back((char)(0xF0 | (cp >> 18)));
        out.push_back((char)(0x80 | ((cp >> 12) & 0x3F)));
        out.push_back((char)(0x80 | ((cp >> 6) & 0x3F)));
        out.push_back((char)(0x80 | (cp & 0x3F)));
    }
}

inline unsigned int hexDigit(char c) {
    if (c >= '0' && c <= '9') return (unsigned int)(c - '0');
    if (c >= 'a' && c <= 'f') return (unsigned int)(c - 'a' + 10);
    if (c >= 'A' && c <= 'F') return (unsigned int)(c - 'A' + 10);
    return 0;
}

// 从 text 的 i 处(开引号已消费)读一个 JSON 字符串, i 落到收尾引号之后
inline std::string readJsonString(const std::string& t, size_t& i, bool& ok) {
    std::string out;
    while (i < t.size() && t[i] != '"') {
        if (t[i] != '\\') {
            out.push_back(t[i++]);
            continue;
        }
        if (i + 1 >= t.size()) break;
        char e = t[++i];
        switch (e) {
            case 'n': out.push_back('\n'); break;
            case 't': out.push_back('\t'); break;
            case 'r': out.push_back('\r'); break;
            case 'b': out.push_back('\b'); break;
            case 'f': out.push_back('\f'); break;
            case 'u': {
                if (i + 4 >= t.size()) { ok = false; return out; }
                unsigned int cp = 0;
                for (int k = 1; k <= 4; ++k) cp = (cp << 4) | hexDigit(t[i + k]);
                i += 4;
                // 代理对: 高半区后面紧跟 \uDC00-\uDFFF 时合成一个码点
                if (cp >= 0xD800 && cp <= 0xDBFF && i + 6 < t.size() &&
                    t[i + 1] == '\\' && t[i + 2] == 'u') {
                    unsigned int lo = 0;
                    for (int k = 3; k <= 6; ++k)
                        lo = (lo << 4) | hexDigit(t[i + k]);
                    if (lo >= 0xDC00 && lo <= 0xDFFF) {
                        cp = 0x10000 + ((cp - 0xD800) << 10) + (lo - 0xDC00);
                        i += 6;
                    }
                }
                appendUtf8(out, cp);
                break;
            }
            default: out.push_back(e); break;   // \" \\ \/ 等原样
        }
        ++i;
    }
    if (i >= t.size()) { ok = false; return out; }
    ++i;                                        // 跳过收尾引号
    ok = true;
    return out;
}

// {"类名": id} → 按 id 下标展开的类名列表(缺号留空串, 保证 names[id] 取得到)
inline std::vector<std::string> parseLabelMapJson(const std::string& t) {
    std::vector<std::pair<int, std::string> > items;
    size_t i = t.find('{');
    if (i == std::string::npos) return std::vector<std::string>();
    ++i;
    while (i < t.size()) {
        while (i < t.size() &&
               (isspace((unsigned char)t[i]) || t[i] == ',')) ++i;
        if (i >= t.size() || t[i] == '}') break;
        if (t[i] != '"') break;                 // 不是平铺对象就不猜了
        ++i;
        bool ok = false;
        std::string name = readJsonString(t, i, ok);
        if (!ok) break;
        while (i < t.size() && isspace((unsigned char)t[i])) ++i;
        if (i >= t.size() || t[i] != ':') break;
        ++i;
        while (i < t.size() && isspace((unsigned char)t[i])) ++i;
        bool neg = false;
        if (i < t.size() && (t[i] == '-' || t[i] == '+')) {
            neg = (t[i] == '-');
            ++i;
        }
        if (i >= t.size() || !isdigit((unsigned char)t[i])) break;
        int id = 0;
        while (i < t.size() && isdigit((unsigned char)t[i]))
            id = id * 10 + (t[i++] - '0');
        items.push_back(std::make_pair(neg ? -id : id, name));
    }
    int mx = -1;
    for (size_t k = 0; k < items.size(); ++k)
        if (items[k].first > mx) mx = items[k].first;
    if (mx < 0) return std::vector<std::string>();
    std::vector<std::string> out((size_t)mx + 1);
    for (size_t k = 0; k < items.size(); ++k)
        if (items[k].first >= 0) out[(size_t)items[k].first] = items[k].second;
    return out;
}

// 类别表: label_map.json({"类名": id}) 或 classes.txt(每行 "id name" 或只有 name, 行号即类别 id)
inline std::vector<std::string> loadClasses(const std::string& path) {
    // 走字节流解析, 中文路径和内容(UTF-8)都能正常读
    std::vector<char> buf = readFileBytes(path);
    if (buf.empty()) return std::vector<std::string>();
    std::string text(buf.begin(), buf.end());
    if (endsWithNoCase(path, ".json")) return parseLabelMapJson(text);
    std::vector<std::string> names;
    std::istringstream f(text);
    std::string line;
    while (std::getline(f, line)) {
        // Windows 上手改过的 txt 可能是 CRLF, 不留 \r 在类名末尾
        if (!line.empty() && line[line.size() - 1] == '\r')
            line.erase(line.size() - 1);
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
