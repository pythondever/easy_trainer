// 目标检测推理示例
// 编译见 CMakeLists.txt; 运行: detect.exe <model.onnx> <image> [classes.txt]

#include <iostream>
#include <string>
#include <vector>

#include <onnxruntime_cxx_api.h>

#include "common.h"

static const int INPUT_SIZE = 640;
static const float SCORE_THR = 0.5f;

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cout << "用法: detect <model.onnx> <image> [classes.txt]\n";
        return 1;
    }
    std::string modelPath = argv[1], imagePath = argv[2];
    std::string classesPath = argc > 3 ? argv[3] : "classes.txt";

    cv::Mat img = cv::imread(imagePath);
    if (img.empty()) {
        std::cout << "读图失败: " << imagePath << "\n";
        return 1;
    }

    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "detect");
    Ort::SessionOptions opt;
    opt.SetIntraOpNumThreads(4);
    Ort::Session session(env, ortPath(modelPath).c_str(), opt);

    Ort::AllocatorWithDefaultOptions alloc;
    Ort::AllocatedStringPtr inName = session.GetInputNameAllocated(0, alloc);
    Ort::AllocatedStringPtr outDetsName = session.GetOutputNameAllocated(0, alloc);
    Ort::AllocatedStringPtr outLabelsName = session.GetOutputNameAllocated(1, alloc);
    std::vector<const char*> inNames{inName.get()};
    std::vector<const char*> outNames{outDetsName.get(), outLabelsName.get()};

    int size = inputSize(session, INPUT_SIZE);
    std::vector<float> input = preprocess(img, size);
    std::vector<int64_t> shape{1, 3, size, size};
    Ort::Value inTensor = makeInput(input, shape);

    auto outputs = session.Run(Ort::RunOptions{nullptr}, inNames.data(),
                               &inTensor, 1, outNames.data(), 2);

    const float* dets = outputs[0].GetTensorData<float>();
    const float* labels = outputs[1].GetTensorData<float>();
    auto detShape = outputs[1].GetTensorTypeAndShapeInfo().GetShape();
    long numQueries = detShape[1];
    long numClassesPlus1 = detShape[2];

    auto names = loadClasses(classesPath);
    for (const auto& d : decodeDets(dets, labels, (int)numQueries,
                                    (int)numClassesPlus1 - 1, img.cols,
                                    img.rows, SCORE_THR)) {
        std::string label = d.cls < (int)names.size() ? names[d.cls]
                                                      : std::to_string(d.cls);
        std::cout << label << "  " << d.score << "  (" << d.x1 << "," << d.y1
                  << ")-(" << d.x2 << "," << d.y2 << ")\n";
        cv::rectangle(img, cv::Point((int)d.x1, (int)d.y1),
                      cv::Point((int)d.x2, (int)d.y2), cv::Scalar(0, 255, 0), 2);
        cv::putText(img, label + " " + std::to_string(d.score).substr(0, 4),
                    cv::Point((int)d.x1, (int)d.y1 - 6),
                    cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);
    }
    cv::imwrite("detect_result.jpg", img);
    return 0;
}
