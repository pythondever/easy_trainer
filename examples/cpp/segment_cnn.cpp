// 实例分割推理示例（CNN 分支）: 比检测多一路低分辨率原型图, 掩码要自己组合出来
// 架构选 Transformer 的用 segment.cpp
// 运行: segment_cnn.exe <model.onnx> <image> [label_map.json]

#include <iostream>
#include <string>
#include <vector>

#include <onnxruntime_cxx_api.h>

#include "common.h"

static const int INPUT_SIZE = 640;
static const float SCORE_THR = 0.5f;
static const float IOU_THR = 0.45f;
static const float MASK_THR = 0.5f;

int main(int argc, char** argv) {
    initConsoleUtf8();
    std::vector<std::string> args = utf8Args(argc, argv);
    if (args.size() < 2) {
        std::cout << "用法: segment_cnn <model.onnx> <image> [label_map.json]\n";
        return 1;
    }
    std::string modelPath = args[0], imagePath = args[1];
    std::string classesPath = args.size() > 2 ? args[2] : "label_map.json";

    cv::Mat img = imreadUtf8(imagePath);
    if (img.empty()) {
        std::cout << "读图失败: " << imagePath << "\n";
        return 1;
    }

    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "segment_cnn");
    Ort::SessionOptions opt;
    opt.SetIntraOpNumThreads(4);
    Ort::Session session(env, ortPath(modelPath).c_str(), opt);

    Ort::AllocatorWithDefaultOptions alloc;
    Ort::AllocatedStringPtr inName = session.GetInputNameAllocated(0, alloc);
    Ort::AllocatedStringPtr outDet = session.GetOutputNameAllocated(0, alloc);
    Ort::AllocatedStringPtr outProto = session.GetOutputNameAllocated(1, alloc);
    std::vector<const char*> inNames{inName.get()};
    std::vector<const char*> outNames{outDet.get(), outProto.get()};

    int size = inputSize(session, INPUT_SIZE);
    LetterBox geo;
    std::vector<float> input = letterbox(img, size, geo);
    std::vector<int64_t> shape{1, 3, size, size};
    Ort::Value inTensor = makeInput(input, shape);

    auto outputs = session.Run(Ort::RunOptions{nullptr}, inNames.data(),
                               &inTensor, 1, outNames.data(), 2);
    const float* det = outputs[0].GetTensorData<float>();
    const float* proto = outputs[1].GetTensorData<float>();
    auto detShape = outputs[0].GetTensorTypeAndShapeInfo().GetShape();
    auto protoShape = outputs[1].GetTensorTypeAndShapeInfo().GetShape();
    int rows = (int)detShape[1], cols = (int)detShape[2];
    int dim = (int)protoShape[1], mh = (int)protoShape[2], mw = (int)protoShape[3];
    int ncls = rows - 4 - dim;   // 尾部 dim 行是掩码系数, 不是类别分数

    auto names = loadClasses(classesPath);
    std::vector<Det> dets = decodeYolo(det, rows, cols, ncls, geo, img.cols,
                                       img.rows, SCORE_THR, IOU_THR);
    std::vector<cv::Mat> masks = decodeYoloMasks(det, cols, proto, dim, mh, mw, ncls,
                                                 geo, dets, img.cols, img.rows, MASK_THR);

    cv::Mat overlay = img.clone();
    for (size_t k = 0; k < masks.size(); ++k)
        overlay.setTo(cv::Scalar(0, 200, 0), masks[k]);
    cv::addWeighted(overlay, 0.45, img, 0.55, 0, img);

    for (size_t k = 0; k < dets.size(); ++k) {
        std::string label = dets[k].cls < (int)names.size()
                                ? names[dets[k].cls]
                                : std::to_string(dets[k].cls);
        std::cout << label << "  " << dets[k].score << "  (" << dets[k].x1 << ","
                  << dets[k].y1 << ")-(" << dets[k].x2 << "," << dets[k].y2 << ")\n";
        cv::rectangle(img, cv::Point((int)dets[k].x1, (int)dets[k].y1),
                      cv::Point((int)dets[k].x2, (int)dets[k].y2),
                      cv::Scalar(0, 255, 0), 2);
    }
    imwriteUtf8("segment_cnn_result.jpg", img);
    return 0;
}
