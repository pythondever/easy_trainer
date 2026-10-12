// 目标检测推理示例（CNN 分支）: 训练时架构选 CNN 的模型用这个, 选 Transformer 的用 detect.cpp
// 编译见 CMakeLists.txt; 运行: detect_cnn.exe <model.onnx> <image> [label_map.json]

#include <iostream>
#include <string>
#include <vector>

#include <onnxruntime_cxx_api.h>

#include "common.h"

static const int INPUT_SIZE = 640;
static const float SCORE_THR = 0.5f;
static const float IOU_THR = 0.45f;

int main(int argc, char** argv) {
    initConsoleUtf8();
    std::vector<std::string> args = utf8Args(argc, argv);
    if (args.size() < 2) {
        std::cout << "用法: detect_cnn <model.onnx> <image> [label_map.json]\n";
        return 1;
    }
    std::string modelPath = args[0], imagePath = args[1];
    std::string classesPath = args.size() > 2 ? args[2] : "label_map.json";

    cv::Mat img = imreadUtf8(imagePath);
    if (img.empty()) {
        std::cout << "读图失败: " << imagePath << "\n";
        return 1;
    }

    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "detect_cnn");
    Ort::SessionOptions opt;
    opt.SetIntraOpNumThreads(4);
    Ort::Session session(env, ortPath(modelPath).c_str(), opt);

    Ort::AllocatorWithDefaultOptions alloc;
    // CNN 导出的输入名是 images, 不是 Transformer 那条线的 input
    Ort::AllocatedStringPtr inName = session.GetInputNameAllocated(0, alloc);
    Ort::AllocatedStringPtr outName = session.GetOutputNameAllocated(0, alloc);
    std::vector<const char*> inNames{inName.get()};
    std::vector<const char*> outNames{outName.get()};

    int size = inputSize(session, INPUT_SIZE);
    LetterBox geo;
    std::vector<float> input = letterbox(img, size, geo);
    std::vector<int64_t> shape{1, 3, size, size};
    Ort::Value inTensor = makeInput(input, shape);

    auto outputs = session.Run(Ort::RunOptions{nullptr}, inNames.data(),
                               &inTensor, 1, outNames.data(), 1);
    const float* det = outputs[0].GetTensorData<float>();
    auto detShape = outputs[0].GetTensorTypeAndShapeInfo().GetShape();
    int rows = (int)detShape[1], cols = (int)detShape[2];
    int ncls = rows - 4;   // 前 4 行是框, 后面全是类别分数

    auto names = loadClasses(classesPath);
    std::vector<Det> dets = decodeYolo(det, rows, cols, ncls, geo, img.cols,
                                       img.rows, SCORE_THR, IOU_THR);
    for (size_t k = 0; k < dets.size(); ++k) {
        std::string label = dets[k].cls < (int)names.size()
                                ? names[dets[k].cls]
                                : std::to_string(dets[k].cls);
        std::cout << label << "  " << dets[k].score << "  (" << dets[k].x1 << ","
                  << dets[k].y1 << ")-(" << dets[k].x2 << "," << dets[k].y2 << ")\n";
        cv::rectangle(img, cv::Point((int)dets[k].x1, (int)dets[k].y1),
                      cv::Point((int)dets[k].x2, (int)dets[k].y2),
                      cv::Scalar(0, 255, 0), 2);
        cv::putText(img, label + " " + std::to_string(dets[k].score).substr(0, 4),
                    cv::Point((int)dets[k].x1, (int)dets[k].y1 - 6),
                    cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);
    }
    imwriteUtf8("detect_cnn_result.jpg", img);
    return 0;
}
