// 图像分类推理示例：输出 scores [1, C], 取 softmax 后的 top-k
// 运行: classify.exe <model.onnx> <image> [classes.txt]

#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

#include <onnxruntime_cxx_api.h>

#include "common.h"

static const int INPUT_SIZE = 224;
static const int TOP_K = 5;

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cout << "用法: classify <model.onnx> <image> [classes.txt]\n";
        return 1;
    }
    std::string modelPath = argv[1], imagePath = argv[2];
    std::string classesPath = argc > 3 ? argv[3] : "classes.txt";

    cv::Mat img = cv::imread(imagePath);
    if (img.empty()) {
        std::cout << "读图失败: " << imagePath << "\n";
        return 1;
    }

    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "classify");
    Ort::SessionOptions opt;
    opt.SetIntraOpNumThreads(4);
    Ort::Session session(env, modelPath.c_str(), opt);

    Ort::AllocatorWithDefaultOptions alloc;
    Ort::AllocatedStringPtr inName = session.GetInputNameAllocated(0, alloc);
    Ort::AllocatedStringPtr outName = session.GetOutputNameAllocated(0, alloc);
    std::vector<const char*> inNames{inName.get()};
    std::vector<const char*> outNames{outName.get()};

    std::vector<float> input = preprocess(img, INPUT_SIZE);
    std::vector<int64_t> shape{1, 3, INPUT_SIZE, INPUT_SIZE};
    Ort::Value inTensor = Ort::Value::CreateTensor<float>(
        shape.data(), shape.size(), input.data(), input.size());

    auto outputs = session.Run(Ort::RunOptions{nullptr}, inNames.data(),
                               &inTensor, 1, outNames.data(), 1);
    const float* logits = outputs[0].GetTensorData<float>();
    long numClasses = outputs[0].GetTensorTypeAndShapeInfo().GetShape()[1];

    std::vector<std::pair<float, int>> prob;
    float mx = *std::max_element(logits, logits + numClasses);
    float sum = 0;
    std::vector<float> p(numClasses);
    for (int i = 0; i < numClasses; ++i) {
        p[i] = std::exp(logits[i] - mx);
        sum += p[i];
    }
    for (int i = 0; i < numClasses; ++i)
        prob.push_back({p[i] / sum, i});
    std::sort(prob.begin(), prob.end(),
              [](const std::pair<float, int>& a, const std::pair<float, int>& b) {
                  return a.first > b.first;
              });

    auto names = loadClasses(classesPath);
    for (int k = 0; k < std::min<int>(TOP_K, numClasses); ++k) {
        int id = prob[k].second;
        std::string label = id < (int)names.size() ? names[id]
                                                   : std::to_string(id);
        std::cout << label << "  " << prob[k].first << "\n";
    }
    return 0;
}
