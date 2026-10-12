using System;
using System.Collections.Generic;
using Microsoft.ML.OnnxRuntime;
using OpenCvSharp;

namespace EasyTrainerOnnx
{
    /// 目标检测（CNN 分支）: 训练时架构选 CNN 的模型用这个。
    /// 架构选 Transformer 的用 Detect.cs, 两者的预处理与输出格式都不一样。
    public static class DetectCnn
    {
        private const int InputSize = 640;
        private const float ScoreThr = 0.5f;
        private const float IouThr = 0.45f;

        public static void Run(string modelPath, string imagePath, string classesPath)
        {
            using var session = OnnxModel.Create(modelPath);
            using var img = OnnxModel.ImRead(imagePath);
            if (img.Empty()) throw new Exception("读图失败: " + imagePath);

            int size = OnnxModel.InputSize(session, InputSize);
            var input = OnnxModel.Letterbox(img, size, out var geo);
            var inputs = new List<NamedOnnxValue>
            {
                // CNN 导出的输入名是 images, 不是 Transformer 那条线的 input
                NamedOnnxValue.CreateFromTensor("images", input),
            };
            using var outputs = session.Run(inputs);
            var detTensor = outputs[0].AsTensor<float>();
            var detShape = detTensor.Dimensions.ToArray();
            int rows = (int)detShape[1], cols = (int)detShape[2];
            int ncls = rows - 4;   // 前 4 行是框, 后面全是类别分数

            var names = OnnxModel.LoadClasses(classesPath);
            foreach (var d in OnnxModel.DecodeYolo(OnnxModel.Data(detTensor), rows, cols,
                                                   ncls, geo, img.Width, img.Height,
                                                   ScoreThr, IouThr))
            {
                string label = d.ClassId < names.Count ? names[d.ClassId]
                                                       : d.ClassId.ToString();
                Console.WriteLine($"{label}  {d.Score:F3}  ({d.X1:F0},{d.Y1:F0})-({d.X2:F0},{d.Y2:F0})");
                Cv2.Rectangle(img, new Point((int)d.X1, (int)d.Y1),
                              new Point((int)d.X2, (int)d.Y2), Scalar.Green, 2);
                Cv2.PutText(img, $"{label} {d.Score:F2}", new Point((int)d.X1, (int)d.Y1 - 6),
                            HersheyFonts.HersheySimplex, 0.6, Scalar.Green, 2);
            }
            OnnxModel.ImWrite("detect_cnn_result.jpg", img);
        }
    }
}
