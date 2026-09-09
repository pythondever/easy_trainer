using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using OpenCvSharp;

namespace EasyTrainerOnnx
{
    public struct Det
    {
        public float X1, Y1, X2, Y2, Score;
        public int ClassId;
        public int Query;   // 候选下标, 分割按它取对应掩码
    }

    /// 预处理 / 后处理, 与 Python、C++ 示例完全一致
    public static class OnnxModel
    {
        public static readonly float[] Mean = { 0.485f, 0.456f, 0.406f };
        public static readonly float[] Std = { 0.229f, 0.224f, 0.225f };

        /// BGR 图 → NCHW float, 方形缩放到 size（不保持宽高比, 与训练一致）
        public static DenseTensor<float> Preprocess(Mat bgr, int size)
        {
            using var rgb = new Mat();
            Cv2.CvtColor(bgr, rgb, ColorConversionCodes.BGR2RGB);
            using var resized = new Mat();
            Cv2.Resize(rgb, resized, new Size(size, size), 0, 0, InterpolationFlags.Linear);
            using var f32 = new Mat();
            resized.ConvertTo(f32, MatType.CV_32FC3, 1.0 / 255.0);

            var data = new float[3 * size * size];
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    var p = f32.At<Vec3f>(y, x);
                    for (int c = 0; c < 3; c++)
                        data[c * size * size + y * size + x] = (p[c] - Mean[c]) / Std[c];
                }
            }
            return new DenseTensor<float>(data, new[] { 1, 3, size, size });
        }

        public static float Sigmoid(float v) => 1f / (1f + (float)Math.Exp(-v));

        /// dets [300,4] (cx cy w h 归一化) + labels [300, C+1] logits → 原图像素框。
        /// 最后一列是「无目标」, 只在前 C 列取类别; 300 个候选已端到端去重, 不需要 NMS。
        public static List<Det> DecodeDets(float[] dets, float[] labels, int numQueries,
                                           int numClasses, int imgW, int imgH, float thr)
        {
            var res = new List<Det>();
            for (int i = 0; i < numQueries; i++)
            {
                int cls = 0;
                float best = Sigmoid(labels[i * (numClasses + 1)]);
                for (int c = 1; c < numClasses; c++)
                {
                    float p = Sigmoid(labels[i * (numClasses + 1) + c]);
                    if (p > best) { best = p; cls = c; }
                }
                if (best < thr) continue;

                float cx = dets[i * 4], cy = dets[i * 4 + 1];
                float w = dets[i * 4 + 2], h = dets[i * 4 + 3];
                res.Add(new Det
                {
                    X1 = (cx - w / 2) * imgW,
                    Y1 = (cy - h / 2) * imgH,
                    X2 = (cx + w / 2) * imgW,
                    Y2 = (cy + h / 2) * imgH,
                    Score = best,
                    ClassId = cls,
                    Query = i,
                });
            }
            return res;
        }

        /// classes.txt: 每行 "id name" 或只有 name, 行号即类别 id
        public static List<string> LoadClasses(string path)
        {
            var names = new List<string>();
            if (!File.Exists(path)) return names;
            foreach (var line in File.ReadAllLines(path))
            {
                if (string.IsNullOrWhiteSpace(line)) continue;
                var parts = line.Trim().Split(new[] { ' ', '\t' }, 2);
                names.Add(parts.Length > 1 ? parts[1].Trim() : parts[0]);
            }
            return names;
        }

        public static InferenceSession Create(string modelPath, bool useGpu = false)
        {
            var opt = new SessionOptions();
            if (useGpu) opt.AppendExecutionProvider_CUDA(0);
            return new InferenceSession(modelPath, opt);
        }

        public static Mat ImRead(string path)
        {
            // OpenCvSharp 直接 ImRead 对中文路径会失败, 走 MemoryStream
            var bytes = File.ReadAllBytes(path);
            return Cv2.ImDecode(bytes, ImreadModes.Color);
        }

        public static NamedOnnxValue ToInput(DenseTensor<float> tensor, string name)
            => NamedOnnxValue.CreateFromTensor(name, tensor);
    }
}
