// 实例分割推理示例：在检测基础上多取一个 masks 输出
// 运行: segment.exe <model.onnx> <image> [classes.txt]

#include <iostream>
#include <string>
#include <vector>

#include <onnxruntime_cxx_api.h>

#include "common.h"

static const int INPUT_SIZE = 640;
static const float SCORE_THR = 0.5f;
static const float MASK_THR = 0.5f;

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cout << "用法: segment <model.onnx> <image> [classes.txt]\n";
        return 1;
    }
    std::string modelPath = argv[1], imagePath = argv[2];
    std::string classesPath = argc > 3 ? argv[3] : "classes.txt";

    cv::Mat img = cv::imread(imagePath);
    if (img.empty()) {
        std::cout << "读图失败: " << imagePath << "\n";
        return 1;
    }

    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "segment");
    Ort::SessionOptions opt;
    opt.SetIntraOpNumThreads(4);
    Ort::Session session(env, ortPath(modelPath).c_str(), opt);

    Ort::AllocatorWithDefaultOptions alloc;
    Ort::AllocatedStringPtr inName = session.GetInputNameAllocated(0, alloc);
    Ort::AllocatedStringPtr outDets = session.GetOutputNameAllocated(0, alloc);
    Ort::AllocatedStringPtr outLabels = session.GetOutputNameAllocated(1, alloc);
    Ort::AllocatedStringPtr outMasks = session.GetOutputNameAllocated(2, alloc);
    std::vector<const char*> inNames{inName.get()};
    std::vector<const char*> outNames{outDets.get(), outLabels.get(), outMasks.get()};

    int size = inputSize(session, INPUT_SIZE);
    std::vector<float> input = preprocess(img, size);
    std::vector<int64_t> shape{1, 3, size, size};
    Ort::Value inTensor = makeInput(input, shape);

    auto outputs = session.Run(Ort::RunOptions{nullptr}, inNames.data(),
                               &inTensor, 1, outNames.data(), 3);
    const float* dets = outputs[0].GetTensorData<float>();
    const float* labels = outputs[1].GetTensorData<float>();
    const float* masks = outputs[2].GetTensorData<float>();

    auto labShape = outputs[1].GetTensorTypeAndShapeInfo().GetShape();
    auto maskShape = outputs[2].GetTensorTypeAndShapeInfo().GetShape();
    int numQueries = (int)labShape[1];
    int numClasses = (int)labShape[2] - 1;
    int maskH = (int)maskShape[2], maskW = (int)maskShape[3];

    auto names = loadClasses(classesPath);
    auto detsOut = decodeDets(dets, labels, numQueries, numClasses, img.cols,
                              img.rows, SCORE_THR);

    // 掩码按候选下标与原图对齐: 先 sigmoid + 阈值, 再放大回原图尺寸
    cv::Mat overlay = img.clone();
    for (const auto& d : detsOut) {
        int q = d.query;
        cv::Mat m(maskH, maskW, CV_32F, (void*)(masks + q * maskH * maskW));
        cv::Mat negExp, onePlus, prob, resized, bin;
        cv::exp(-m, negExp);
        cv::add(negExp, cv::Scalar::all(1.0), onePlus);
        cv::divide(1.0, onePlus, prob);
        cv::resize(prob, resized, cv::Size(img.cols, img.rows), 0, 0,
                   cv::INTER_LINEAR);
        bin = resized > MASK_THR;   // 比较结果是 CV_8U, 可直接当 setTo 的掩码
        overlay.setTo(cv::Scalar(0, 200, 0), bin);
    }
    cv::addWeighted(overlay, 0.45, img, 0.55, 0, img);

    for (const auto& d : detsOut) {
        std::string label = d.cls < (int)names.size() ? names[d.cls]
                                                      : std::to_string(d.cls);
        std::cout << label << "  " << d.score << "  (" << d.x1 << "," << d.y1
                  << ")-(" << d.x2 << "," << d.y2 << ")\n";
        cv::rectangle(img, cv::Point((int)d.x1, (int)d.y1),
                      cv::Point((int)d.x2, (int)d.y2), cv::Scalar(0, 255, 0), 2);
    }
    cv::imwrite("segment_result.jpg", img);
    return 0;
}
