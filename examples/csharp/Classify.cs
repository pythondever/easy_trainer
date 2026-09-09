using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.ML.OnnxRuntime;

namespace EasyTrainerOnnx
{
    public static class Classify
    {
        private const int InputSize = 224;
        private const int TopK = 5;

        public static void Run(string modelPath, string imagePath, string classesPath)
        {
            using var session = OnnxModel.Create(modelPath);
            using var img = OnnxModel.ImRead(imagePath);
            if (img.Empty()) throw new Exception("读图失败: " + imagePath);

            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor("images",
                    OnnxModel.Preprocess(img, OnnxModel.InputSize(session, InputSize))),
            };
            using var outputs = session.Run(inputs);
            var logits = OnnxModel.Data(outputs[0].AsTensor<float>());

            var max = logits.Max();
            var prob = logits.Select(v => (float)Math.Exp(v - max)).ToArray();
            var sum = prob.Sum();
            var ranked = prob.Select((p, i) => (Score: p / sum, Id: i))
                             .OrderByDescending(x => x.Score)
                             .Take(TopK);

            var names = OnnxModel.LoadClasses(classesPath);
            foreach (var r in ranked)
            {
                string label = r.Id < names.Count ? names[r.Id] : r.Id.ToString();
                Console.WriteLine($"{label,-20} {r.Score:F4}");
            }
        }
    }
}
