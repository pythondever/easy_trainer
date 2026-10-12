using System;
using System.Collections.Generic;
using Microsoft.ML.OnnxRuntime;
using OpenCvSharp;

namespace EasyTrainerOnnx
{
    /// 实例分割（CNN 分支）: 比检测多一路低分辨率原型图, 掩码要自己组合出来。
    /// 架构选 Transformer 的用 Segment.cs。
    public static class SegmentCnn
    {
        private const int InputSize = 640;
        private const float ScoreThr = 0.5f;
        private const float IouThr = 0.45f;
        private const float MaskThr = 0.5f;

        public static void Run(string modelPath, string imagePath, string classesPath)
        {
            using var session = OnnxModel.Create(modelPath);
            using var img = OnnxModel.ImRead(imagePath);
            if (img.Empty()) throw new Exception("读图失败: " + imagePath);

            int size = OnnxModel.InputSize(session, InputSize);
            var input = OnnxModel.Letterbox(img, size, out var geo);
            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor("images", input),
            };
            using var outputs = session.Run(inputs);
            var detTensor = outputs[0].AsTensor<float>();
            var protoTensor = outputs[1].AsTensor<float>();
            var detShape = detTensor.Dimensions.ToArray();
            var protoShape = protoTensor.Dimensions.ToArray();
            int rows = (int)detShape[1], cols = (int)detShape[2];
            int dim = (int)protoShape[1], mh = (int)protoShape[2], mw = (int)protoShape[3];
            int ncls = rows - 4 - dim;   // 尾部 dim 行是掩码系数, 不是类别分数

            var names = OnnxModel.LoadClasses(classesPath);
            var dets = OnnxModel.DecodeYolo(OnnxModel.Data(detTensor), rows, cols, ncls,
                                            geo, img.Width, img.Height, ScoreThr, IouThr);
            var masks = OnnxModel.DecodeYoloMasks(OnnxModel.Data(detTensor), cols,
                                                  OnnxModel.Data(protoTensor), dim, mh, mw,
                                                  ncls, geo, dets, img.Width, img.Height,
                                                  MaskThr);

            using var overlay = img.Clone();
            foreach (var m in masks)
            {
                overlay.SetTo(new Scalar(0, 200, 0), m);
                m.Dispose();
            }
            Cv2.AddWeighted(overlay, 0.45, img, 0.55, 0, img);

            foreach (var d in dets)
            {
                string label = d.ClassId < names.Count ? names[d.ClassId]
                                                       : d.ClassId.ToString();
                Console.WriteLine($"{label}  {d.Score:F3}  ({d.X1:F0},{d.Y1:F0})-({d.X2:F0},{d.Y2:F0})");
                Cv2.Rectangle(img, new Point((int)d.X1, (int)d.Y1),
                              new Point((int)d.X2, (int)d.Y2), Scalar.Green, 2);
            }
            OnnxModel.ImWrite("segment_cnn_result.jpg", img);
        }
    }
}
