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
// NOMINMAX: windef.h 会把 min/max 定义成宏, 吃掉后面 CNN 分支的 std::min/std::max
#ifndef NOMINMAX
#define NOMINMAX
#endif
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

// BGR 图转成 NCHW float, 方形缩放到 size（不保持宽高比, 与训练一致）
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

// dets [300,4] (cx cy w h 归一化) + labels [300, C+1] logits 转成原图像素框
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

// ---- CNN(YOLO) 分支: 预处理与输出约定都和上面那套不同, 别混用 ----

static const int PAD_COLOR = 114;   // letterbox 的补边色, 与 ultralytics 一致
static const int MASK_DIM = 32;     // 分割 head 输出的掩码系数个数

// letterbox 的几何量, 还原坐标时按它反算
struct LetterBox {
    float ratio = 1.0f;
    int left = 0, top = 0, size = 0, innerW = 0, innerH = 0;
};

// BGR 图转成 CNN 分支的模型输入: 保比例缩放到 size 后居中补灰边.
// 不像 preprocess 那样直接拉成方形, 拉伸会让框的位置系统性偏移.
inline std::vector<float> letterbox(const cv::Mat& bgr, int size, LetterBox& geo) {
    int h = bgr.rows, w = bgr.cols;
    float ratio = std::min(size / (float)h, size / (float)w);
    // nearbyint 走默认的「四舍六入五取偶」, 与 Python 的 round 一致
    int innerW = (int)std::nearbyint(w * ratio);
    int innerH = (int)std::nearbyint(h * ratio);
    // 减 0.1 再取整是照 ultralytics 的 LetterBox 抄的, 补边落半像素会让框整体偏一格
    int left = (int)std::nearbyint((size - innerW) / 2.0 - 0.1);
    int top = (int)std::nearbyint((size - innerH) / 2.0 - 0.1);

    cv::Mat inner, padded, rgb, f32;
    cv::resize(bgr, inner, cv::Size(innerW, innerH), 0, 0, cv::INTER_LINEAR);
    cv::copyMakeBorder(inner, padded, top, size - innerH - top, left,
                       size - innerW - left, cv::BORDER_CONSTANT,
                       cv::Scalar(PAD_COLOR, PAD_COLOR, PAD_COLOR));
    cv::cvtColor(padded, rgb, cv::COLOR_BGR2RGB);
    rgb.convertTo(f32, CV_32FC3, 1.0 / 255.0);

    std::vector<float> out(3 * size * size);
    for (int y = 0; y < size; ++y) {
        for (int x = 0; x < size; ++x) {
            cv::Vec3f p = f32.at<cv::Vec3f>(y, x);
            for (int c = 0; c < 3; ++c)
                out[c * size * size + y * size + x] = p[c];
        }
    }
    geo.ratio = ratio;
    geo.left = left;
    geo.top = top;
    geo.size = size;
    geo.innerW = innerW;
    geo.innerH = innerH;
    return out;
}

inline float clampf(float v, float lo, float hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

// rows x cols 的行优先布局里取 (r, c)
inline int yoloIdx(int r, int c, int cols) { return r * cols + c; }

inline float boxIoU(const std::vector<float>& a, int ai,
                    const std::vector<float>& b, int bi) {
    float ax1 = a[ai * 4], ay1 = a[ai * 4 + 1];
    float ax2 = a[ai * 4 + 2], ay2 = a[ai * 4 + 3];
    float bx1 = b[bi * 4], by1 = b[bi * 4 + 1];
    float bx2 = b[bi * 4 + 2], by2 = b[bi * 4 + 3];
    float iw = std::max(0.0f, std::min(ax2, bx2) - std::max(ax1, bx1));
    float ih = std::max(0.0f, std::min(ay2, by2) - std::max(ay1, by1));
    float inter = iw * ih;
    float areaA = (ax2 - ax1) * (ay2 - ay1);
    float areaB = (bx2 - bx1) * (by2 - by1);
    return inter / std::max(areaA + areaB - inter, 1e-9f);
}

// 单类 NMS, 返回在入参里的下标
inline std::vector<int> nmsOne(const std::vector<float>& boxes, int count,
                               const std::vector<float>& scores, float thr) {
    std::vector<int> order(count);
    for (int k = 0; k < count; ++k) order[k] = k;
    std::stable_sort(order.begin(), order.end(),
                     [&scores](int a, int b) { return scores[a] > scores[b]; });
    std::vector<int> keep;
    while (!order.empty()) {
        int i = order[0];
        keep.push_back(i);
        if (order.size() == 1) break;
        std::vector<int> next;
        for (size_t k = 1; k < order.size(); ++k)
            if (boxIoU(boxes, i, boxes, order[k]) <= thr) next.push_back(order[k]);
        order.swap(next);
    }
    return keep;
}

// 检测输出 output0 解码成原图像素框.
// rows x cols 里前 4 行是 (cx, cy, w, h) 像素值(相对 letterbox 后的输入图), 之后每行
// 一个类别分数(导出时已过 sigmoid, 不用再算); cols 是原生 anchor 点, 同一目标会命中
// 多个, 必须自己按类去重. Det.query 记的是 anchor 下标, 分割按它取掩码.
inline std::vector<Det> decodeYolo(const float* det, int rows, int cols, int ncls,
                                   const LetterBox& geo, int imgW, int imgH,
                                   float scoreThr, float iouThr) {
    (void)rows;
    std::vector<Det> res;
    std::vector<int> picked, clsId;
    std::vector<float> scores;
    for (int i = 0; i < cols; ++i) {
        int best = 0;
        float bs = det[yoloIdx(4, i, cols)];
        for (int c = 1; c < ncls; ++c) {
            float p = det[yoloIdx(4 + c, i, cols)];
            if (p > bs) {
                bs = p;
                best = c;
            }
        }
        if (bs >= scoreThr) {
            picked.push_back(i);
            clsId.push_back(best);
            scores.push_back(bs);
        }
    }
    if (picked.empty()) return res;

    // 先还原到原图坐标, 下面的 NMS 在还原后的框上算
    std::vector<float> xyxy(picked.size() * 4);
    for (size_t k = 0; k < picked.size(); ++k) {
        int i = picked[k];
        float cx = det[yoloIdx(0, i, cols)], cy = det[yoloIdx(1, i, cols)];
        float bw = det[yoloIdx(2, i, cols)], bh = det[yoloIdx(3, i, cols)];
        xyxy[k * 4 + 0] = clampf((cx - bw / 2 - geo.left) / geo.ratio, 0, (float)imgW);
        xyxy[k * 4 + 1] = clampf((cy - bh / 2 - geo.top) / geo.ratio, 0, (float)imgH);
        xyxy[k * 4 + 2] = clampf((cx + bw / 2 - geo.left) / geo.ratio, 0, (float)imgW);
        xyxy[k * 4 + 3] = clampf((cy + bh / 2 - geo.top) / geo.ratio, 0, (float)imgH);
    }

    // 按类别各做一次 NMS, 最后按下标升序回排, 与 Python/C# 示例同序
    std::vector<int> classes(clsId);
    std::sort(classes.begin(), classes.end());
    classes.erase(std::unique(classes.begin(), classes.end()), classes.end());
    std::vector<int> keep;
    for (size_t ci = 0; ci < classes.size(); ++ci) {
        std::vector<int> subset;
        for (size_t k = 0; k < clsId.size(); ++k)
            if (clsId[k] == classes[ci]) subset.push_back((int)k);
        std::vector<float> subBoxes(subset.size() * 4), subScores(subset.size());
        for (size_t k = 0; k < subset.size(); ++k) {
            for (int d = 0; d < 4; ++d)
                subBoxes[k * 4 + d] = xyxy[subset[k] * 4 + d];
            subScores[k] = scores[subset[k]];
        }
        std::vector<int> kk = nmsOne(subBoxes, (int)subset.size(), subScores, iouThr);
        for (size_t k = 0; k < kk.size(); ++k) keep.push_back(subset[kk[k]]);
    }
    std::sort(keep.begin(), keep.end());
    for (size_t k = 0; k < keep.size(); ++k) {
        int kk = keep[k];
        Det d;
        d.x1 = xyxy[kk * 4 + 0];
        d.y1 = xyxy[kk * 4 + 1];
        d.x2 = xyxy[kk * 4 + 2];
        d.y2 = xyxy[kk * 4 + 3];
        d.score = scores[kk];
        d.cls = clsId[kk];
        d.query = picked[kk];
        res.push_back(d);
    }
    return res;
}

// 分割输出的第二路: 原图尺寸的掩码(前景 255).
// 掩码由 output0 尾部 MASK_DIM 行系数与 output1 那 MASK_DIM 张低分辨率原型图线性组合
// 再补 sigmoid 得到(尾部系数没经过 sigmoid); 组合后要按 letterbox 的补边裁掉再缩回原图,
// 直接拉伸会整体位移.
inline std::vector<cv::Mat> decodeYoloMasks(
        const float* det, int cols, const float* proto, int dim, int mh, int mw,
        int ncls, const LetterBox& geo, const std::vector<Det>& dets, int imgW,
        int imgH, float maskThr) {
    std::vector<cv::Mat> masks;
    if (dets.empty()) return masks;
    int plane = mh * mw;
    for (size_t n = 0; n < dets.size(); ++n) {
        int q = dets[n].query;
        std::vector<float> combined(plane, 0.0f);
        for (int k = 0; k < dim; ++k) {
            float w = det[yoloIdx(4 + ncls + k, q, cols)];
            if (w == 0.0f) continue;
            int off = k * plane;
            for (int p = 0; p < plane; ++p) combined[p] += w * proto[off + p];
        }
        for (int p = 0; p < plane; ++p) combined[p] = sigmoid(combined[p]);

        // 变量名不能叫 small: rpcndr.h 里 small 是 char 的宏
        cv::Mat planeImg(mh, mw, CV_32F, combined.data());
        cv::Mat up, back;
        cv::resize(planeImg, up, cv::Size(geo.size, geo.size), 0, 0, cv::INTER_LINEAR);
        cv::Mat crop = up(cv::Rect(geo.left, geo.top, geo.innerW, geo.innerH));
        cv::resize(crop, back, cv::Size(imgW, imgH), 0, 0, cv::INTER_LINEAR);

        cv::Mat keep = cv::Mat::zeros(imgH, imgW, CV_8U);
        int ys = std::max((int)dets[n].y1, 0);
        int ye = std::min((int)std::ceil(dets[n].y2), imgH);
        int xs = std::max((int)dets[n].x1, 0);
        int xe = std::min((int)std::ceil(dets[n].x2), imgW);
        if (ye > ys && xe > xs) {
            // 阈值比较用 CMP_GE, 与 Python 的 >= 对齐(OpenCV 的 threshold 是严格大于)
            cv::Mat roi = back(cv::Rect(xs, ys, xe - xs, ye - ys));
            cv::Mat bin;
            cv::compare(roi, maskThr, bin, cv::CMP_GE);
            bin.copyTo(keep(cv::Rect(xs, ys, xe - xs, ye - ys)));
        }
        masks.push_back(keep);
    }
    return masks;
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

// {"类名": id} 转成按 id 下标展开的类名列表(缺号留空串, 保证 names[id] 取得到)
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
