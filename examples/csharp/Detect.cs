using System;
using System.Collections.Generic;
using Microsoft.ML.OnnxRuntime;
using OpenCvSharp;

namespace EasyTrainerOnnx
{
    public static class Detect
    {
        private const int InputSize = 640;
        private const float ScoreThr = 0.5f;

        public static void Run(string modelPath, string imagePath, string classesPath)
        {
            using var session = OnnxModel.Create(modelPath);
            using var img = OnnxModel.ImRead(imagePath);
            if (img.Empty()) throw new Exception("读图失败: " + imagePath);

            var input = OnnxModel.Preprocess(img, OnnxModel.InputSize(session, InputSize));
            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor("input", input),
            };
            using var outputs = session.Run(inputs);
            var dets = OnnxModel.Data(outputs[0].AsTensor<float>());
            var labelsTensor = outputs[1].AsTensor<float>();
            var labels = OnnxModel.Data(labelsTensor);
            var shape = labelsTensor.Dimensions.ToArray();
            int numQueries = (int)shape[1], numClasses = (int)shape[2] - 1;

            var names = OnnxModel.LoadClasses(classesPath);
            foreach (var d in OnnxModel.DecodeDets(dets, labels, numQueries, numClasses,
                                                   img.Width, img.Height, ScoreThr))
            {
                string label = d.ClassId < names.Count ? names[d.ClassId]
                                                       : d.ClassId.ToString();
                Console.WriteLine($"{label}  {d.Score:F3}  ({d.X1:F0},{d.Y1:F0})-({d.X2:F0},{d.Y2:F0})");
                Cv2.Rectangle(img, new Point((int)d.X1, (int)d.Y1),
                              new Point((int)d.X2, (int)d.Y2), Scalar.Green, 2);
                Cv2.PutText(img, $"{label} {d.Score:F2}", new Point((int)d.X1, (int)d.Y1 - 6),
                            HersheyFonts.HersheySimplex, 0.6, Scalar.Green, 2);
            }
            OnnxModel.ImWrite("detect_result.jpg", img);
        }
    }
}
