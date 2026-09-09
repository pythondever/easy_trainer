using System;
using System.Collections.Generic;
using Microsoft.ML.OnnxRuntime;
using OpenCvSharp;

namespace EasyTrainerOnnx
{
    public static class Segment
    {
        private const int InputSize = 640;
        private const float ScoreThr = 0.5f;
        private const float MaskThr = 0.5f;

        public static void Run(string modelPath, string imagePath, string classesPath)
        {
            using var session = OnnxModel.Create(modelPath);
            using var img = OnnxModel.ImRead(imagePath);
            if (img.Empty()) throw new Exception("读图失败: " + imagePath);

            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor("input",
                    OnnxModel.Preprocess(img, OnnxModel.InputSize(session, InputSize))),
            };
            using var outputs = session.Run(inputs);
            var dets = OnnxModel.Data(outputs[0].AsTensor<float>());
            var labelsTensor = outputs[1].AsTensor<float>();
            var labels = OnnxModel.Data(labelsTensor);
            var masksTensor = outputs[2].AsTensor<float>();
            var masks = OnnxModel.Data(masksTensor);

            var labShape = labelsTensor.Dimensions.ToArray();
            var maskShape = masksTensor.Dimensions.ToArray();
            int numQueries = (int)labShape[1], numClasses = (int)labShape[2] - 1;
            int maskH = (int)maskShape[2], maskW = (int)maskShape[3];

            var names = OnnxModel.LoadClasses(classesPath);
            var detsOut = OnnxModel.DecodeDets(dets, labels, numQueries, numClasses,
                                               img.Width, img.Height, ScoreThr);

            // 掩码按候选下标取, sigmoid 后阈值化, 再放大回原图尺寸
            using var overlay = img.Clone();
            foreach (var d in detsOut)
            {
                var mask = new float[maskH * maskW];
                Array.Copy(masks, d.Query * maskH * maskW, mask, 0, mask.Length);
                var sigData = new float[mask.Length];
                for (int i = 0; i < mask.Length; i++)
                    sigData[i] = OnnxModel.Sigmoid(mask[i]);
                using var sig = new Mat(maskH, maskW, MatType.CV_32FC1, sigData);
                using var resized = new Mat();
                Cv2.Resize(sig, resized, new Size(img.Width, img.Height), 0, 0,
                           InterpolationFlags.Linear);
                using var thr = new Mat();
                Cv2.Threshold(resized, thr, MaskThr, 255, ThresholdTypes.Binary);
                // setTo 的掩码必须是 CV_8U, Threshold 输出跟输入同类型(CV_32F)要转一次
                using var bin = new Mat();
                thr.ConvertTo(bin, MatType.CV_8UC1);
                overlay.SetTo(new Scalar(0, 200, 0), bin);
            }
            Cv2.AddWeighted(overlay, 0.45, img, 0.55, 0, img);

            foreach (var d in detsOut)
            {
                string label = d.ClassId < names.Count ? names[d.ClassId]
                                                       : d.ClassId.ToString();
                Console.WriteLine($"{label}  {d.Score:F3}  ({d.X1:F0},{d.Y1:F0})-({d.X2:F0},{d.Y2:F0})");
                Cv2.Rectangle(img, new Point((int)d.X1, (int)d.Y1),
                              new Point((int)d.X2, (int)d.Y2), Scalar.Green, 2);
            }
            OnnxModel.ImWrite("segment_result.jpg", img);
        }
    }
}
