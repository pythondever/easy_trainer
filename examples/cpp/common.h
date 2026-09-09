// 检测/分割/分类共用的预处理与后处理（头文件形式, 三个示例直接 include）
#pragma once

#include <algorithm>
#include <cmath>
#include <fstream>
#include <string>
#include <vector>

#include <opencv2/opencv.hpp>
#include <onnxruntime_cxx_api.h>

#ifdef _WIN32
#include <windows.h>
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

// Windows 下 ORTCHAR_T 是 wchar_t, 路径要先转宽字符
inline std::basic_string<ORTCHAR_T> ortPath(const std::string& s) {
#ifdef _WIN32
    int n = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), (int)s.size(), nullptr, 0);
    std::wstring w((size_t)n, L'\0');
    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), (int)s.size(), &w[0], n);
    return w;
#else
    return s;
#endif
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
    std::ifstream f(path);
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
