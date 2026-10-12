using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
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

    /// 预处理 / 后处理, 与 Python、C++ 示例一致
    public static class OnnxModel
    {
        public static readonly float[] Mean = { 0.485f, 0.456f, 0.406f };
        public static readonly float[] Std = { 0.229f, 0.224f, 0.225f };

        /// BGR 图转成 NCHW float, 方形缩放到 size（不保持宽高比, 与训练一致）
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

        /// 模型输入尺寸是静态的, 按模型实际的 H 缩放(训练尺寸不一定是 640/224)
        public static int InputSize(InferenceSession session, int fallback)
        {
            var shape = session.InputMetadata.Values.First().Dimensions;
            return shape.Length == 4 && shape[2] > 0 ? (int)shape[2] : fallback;
        }

        /// 取张量数据(行优先一维)。Tensor<T> 没有 ToArray / Buffer, 只能按索引取
        public static float[] Data(Tensor<float> t)
        {
            var data = new float[t.Length];
            for (int i = 0; i < data.Length; i++) data[i] = t.GetValue(i);
            return data;
        }

        /// dets [300,4] (cx cy w h 归一化) + labels [300, C+1] logits 转成原图像素框。
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

        /// 类别表转成按 id 下标排列的类名列表。
        /// 认两种格式: label_map.json（{"类名": id}，导出包默认给这个）
        /// 与 classes.txt（每行 "id name" 或只有 name, 行号即类别 id, 旧包与训练目录里还有）。
        public static List<string> LoadClasses(string path)
        {
            var names = new List<string>();
            if (!File.Exists(path)) return names;
            if (path.EndsWith(".json", StringComparison.OrdinalIgnoreCase))
                return ExpandLabelMap(path);
            foreach (var line in File.ReadAllLines(path))
            {
                if (string.IsNullOrWhiteSpace(line)) continue;
                var parts = line.Trim().Split(new[] { ' ', '\t' }, 2);
                names.Add(parts.Length > 1 ? parts[1].Trim() : parts[0]);
            }
            return names;
        }

        /// {"类名": id} 转成按下标展开的类名列表(缺号留空串, 保证 names[id] 取得到)
        private static List<string> ExpandLabelMap(string path)
        {
            var items = new List<KeyValuePair<int, string>>();
            try
            {
                using (var doc = JsonDocument.Parse(
                           File.ReadAllText(path, Encoding.UTF8)))
                {
                    if (doc.RootElement.ValueKind != JsonValueKind.Object)
                        return new List<string>();
                    foreach (var prop in doc.RootElement.EnumerateObject())
                    {
                        int id;
                        if (prop.Value.ValueKind == JsonValueKind.Number &&
                            prop.Value.TryGetInt32(out id))
                            items.Add(new KeyValuePair<int, string>(id, prop.Name));
                    }
                }
            }
            catch (Exception)
            {
                return new List<string>();
            }
            int max = -1;
            foreach (var it in items) if (it.Key > max) max = it.Key;
            if (max < 0) return new List<string>();
            var names = new List<string>(max + 1);
            for (int k = 0; k <= max; ++k) names.Add("");
            foreach (var it in items) if (it.Key >= 0) names[it.Key] = it.Value;
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

        public static void ImWrite(string path, Mat img)
        {
            // 同理: 工作目录是中文时 Cv2.ImWrite 也写不出来, 自己编码后落盘
            var ext = Path.GetExtension(path);
            if (string.IsNullOrEmpty(ext)) ext = ".jpg";
            Cv2.ImEncode(ext, img, out var bytes);
            File.WriteAllBytes(path, bytes);
        }

        public static NamedOnnxValue ToInput(DenseTensor<float> tensor, string name)
            => NamedOnnxValue.CreateFromTensor(name, tensor);

        // ---- CNN(YOLO) 分支: 预处理与输出约定都和上面那套不同, 别混用 ----

        public const int PadColor = 114;   // letterbox 的补边色, 与 ultralytics 一致
        public const int MaskDim = 32;     // 分割 head 输出的掩码系数个数

        /// letterbox 的几何量, 还原坐标时按它反算
        public struct LetterBoxGeo
        {
            public float Ratio;
            public int Left, Top, Size, InnerW, InnerH;
        }

        /// BGR 图转成 CNN 分支的输入: 保比例缩放到 size 后居中补灰边。
        /// 不像上面那个 Preprocess 直接拉成方形, 拉伸会让框的位置系统性偏移。
        public static DenseTensor<float> Letterbox(Mat bgr, int size, out LetterBoxGeo geo)
        {
            int h = bgr.Rows, w = bgr.Cols;
            double ratio = Math.Min(size / (double)h, size / (double)w);
            // Math.Round 默认四舍六入五取偶, 与 Python 的 round 一致
            int innerW = (int)Math.Round(w * ratio), innerH = (int)Math.Round(h * ratio);
            // 减 0.1 再取整是照 ultralytics 的 LetterBox 抄的, 补边落半像素会让框整体偏一格
            int left = (int)Math.Round((size - innerW) / 2.0 - 0.1);
            int top = (int)Math.Round((size - innerH) / 2.0 - 0.1);

            using var inner = new Mat();
            Cv2.Resize(bgr, inner, new Size(innerW, innerH), 0, 0, InterpolationFlags.Linear);
            using var padded = new Mat();
            Cv2.CopyMakeBorder(inner, padded, top, size - innerH - top,
                               left, size - innerW - left, BorderTypes.Constant,
                               new Scalar(PadColor, PadColor, PadColor));
            using var rgb = new Mat();
            Cv2.CvtColor(padded, rgb, ColorConversionCodes.BGR2RGB);
            using var f32 = new Mat();
            rgb.ConvertTo(f32, MatType.CV_32FC3, 1.0 / 255.0);

            var data = new float[3 * size * size];
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                {
                    var p = f32.At<Vec3f>(y, x);
                    for (int c = 0; c < 3; c++)
                        data[c * size * size + y * size + x] = p[c];
                }
            }
            geo = new LetterBoxGeo
            {
                Ratio = (float)ratio, Left = left, Top = top,
                Size = size, InnerW = innerW, InnerH = innerH,
            };
            return new DenseTensor<float>(data, new[] { 1, 3, size, size });
        }

        /// rows x cols 的行优先布局里取 (r, c)
        private static int Idx(int r, int c, int cols) => r * cols + c;

        private static float Clamp(float v, float lo, float hi)
            => v < lo ? lo : (v > hi ? hi : v);

        private static float IoU(float[] a, int ai, float[] b, int bi)
        {
            float ax1 = a[ai * 4], ay1 = a[ai * 4 + 1], ax2 = a[ai * 4 + 2], ay2 = a[ai * 4 + 3];
            float bx1 = b[bi * 4], by1 = b[bi * 4 + 1], bx2 = b[bi * 4 + 2], by2 = b[bi * 4 + 3];
            float iw = Math.Max(0f, Math.Min(ax2, bx2) - Math.Max(ax1, bx1));
            float ih = Math.Max(0f, Math.Min(ay2, by2) - Math.Max(ay1, by1));
            float inter = iw * ih;
            float areaA = (ax2 - ax1) * (ay2 - ay1), areaB = (bx2 - bx1) * (by2 - by1);
            return inter / Math.Max(areaA + areaB - inter, 1e-9f);
        }

        /// 单类 NMS, 返回在入参里的下标
        private static List<int> NmsOne(float[] boxes, int count, float[] scores, float thr)
        {
            var order = Enumerable.Range(0, count)
                                  .OrderByDescending(k => scores[k]).ToArray();
            var keep = new List<int>();
            while (order.Length > 0)
            {
                int i = order[0];
                keep.Add(i);
                if (order.Length == 1) break;
                var next = new List<int>(order.Length - 1);
                for (int k = 1; k < order.Length; k++)
                    if (IoU(boxes, i, boxes, order[k]) <= thr) next.Add(order[k]);
                order = next.ToArray();
            }
            return keep;
        }

        /// 检测输出 output0 解码成原图像素框。
        /// rows x cols 里前 4 行是 (cx, cy, w, h) 像素值(相对 letterbox 后的输入图),
        /// 之后每行一个类别分数(导出时已过 sigmoid, 不用再算); cols 是原生 anchor 点,
        /// 同一目标会命中多个, 必须自己按类去重。Det.Query 记的是 anchor 下标, 分割按它取掩码。
        public static List<Det> DecodeYolo(float[] det, int rows, int cols, int ncls,
                                           LetterBoxGeo geo, int imgW, int imgH,
                                           float scoreThr, float iouThr)
        {
            var res = new List<Det>();
            var picked = new List<int>();
            var clsId = new List<int>();
            var scores = new List<float>();
            for (int i = 0; i < cols; i++)
            {
                int best = 0;
                float bs = det[Idx(4, i, cols)];
                for (int c = 1; c < ncls; c++)
                {
                    float p = det[Idx(4 + c, i, cols)];
                    if (p > bs) { bs = p; best = c; }
                }
                if (bs >= scoreThr) { picked.Add(i); clsId.Add(best); scores.Add(bs); }
            }
            if (picked.Count == 0) return res;

            var xyxy = new float[picked.Count * 4];
            for (int k = 0; k < picked.Count; k++)
            {
                int i = picked[k];
                float cx = det[Idx(0, i, cols)], cy = det[Idx(1, i, cols)];
                float bw = det[Idx(2, i, cols)], bh = det[Idx(3, i, cols)];
                xyxy[k * 4 + 0] = Clamp((cx - bw / 2 - geo.Left) / geo.Ratio, 0, imgW);
                xyxy[k * 4 + 1] = Clamp((cy - bh / 2 - geo.Top) / geo.Ratio, 0, imgH);
                xyxy[k * 4 + 2] = Clamp((cx + bw / 2 - geo.Left) / geo.Ratio, 0, imgW);
                xyxy[k * 4 + 3] = Clamp((cy + bh / 2 - geo.Top) / geo.Ratio, 0, imgH);
            }

            // 按类别各做一次 NMS, 最后按下标升序回排, 与 Python 示例同序
            var sArr = scores.ToArray();
            var keep = new List<int>();
            foreach (var c in clsId.Distinct().OrderBy(t => t).ToList())
            {
                var subset = new List<int>();
                for (int k = 0; k < clsId.Count; k++) if (clsId[k] == c) subset.Add(k);
                var subBoxes = new float[subset.Count * 4];
                var subScores = new float[subset.Count];
                for (int k = 0; k < subset.Count; k++)
                {
                    Array.Copy(xyxy, subset[k] * 4, subBoxes, k * 4, 4);
                    subScores[k] = sArr[subset[k]];
                }
                foreach (var k in NmsOne(subBoxes, subset.Count, subScores, iouThr))
                    keep.Add(subset[k]);
            }
            keep.Sort();
            foreach (var k in keep)
                res.Add(new Det
                {
                    X1 = xyxy[k * 4], Y1 = xyxy[k * 4 + 1],
                    X2 = xyxy[k * 4 + 2], Y2 = xyxy[k * 4 + 3],
                    Score = sArr[k], ClassId = clsId[k], Query = picked[k],
                });
            return res;
        }

        /// 分割的第二路输出: 原图尺寸的掩码列表(前景 255)。
        /// 掩码由 output0 尾部 MaskDim 行系数与 output1 那 MaskDim 张低分辨率原型图线性
        /// 组合再补 sigmoid 得到(尾部系数没经过 sigmoid); 组合后要按 letterbox 的补边裁掉
        /// 再缩回原图, 直接拉伸会整体位移。返回的 Mat 由调用方负责释放。
        public static List<Mat> DecodeYoloMasks(float[] det, int cols, float[] proto,
                                                int dim, int mh, int mw, int ncls,
                                                LetterBoxGeo geo, List<Det> dets, int imgW,
                                                int imgH, float maskThr)
        {
            var masks = new List<Mat>();
            if (dets.Count == 0) return masks;
            int plane = mh * mw;
            foreach (var d in dets)
            {
                var combined = new float[plane];
                for (int k = 0; k < dim; k++)
                {
                    float w = det[Idx(4 + ncls + k, d.Query, cols)];
                    if (w == 0f) continue;
                    int off = k * plane;
                    for (int p = 0; p < plane; p++) combined[p] += w * proto[off + p];
                }
                for (int p = 0; p < plane; p++) combined[p] = Sigmoid(combined[p]);

                using var small = new Mat(mh, mw, MatType.CV_32FC1, combined);
                using var up = new Mat();
                Cv2.Resize(small, up, new Size(geo.Size, geo.Size), 0, 0,
                           InterpolationFlags.Linear);
                using var crop = new Mat(up, new Rect(geo.Left, geo.Top, geo.InnerW, geo.InnerH));
                using var back = new Mat();
                Cv2.Resize(crop, back, new Size(imgW, imgH), 0, 0, InterpolationFlags.Linear);

                var keep = new Mat(imgH, imgW, MatType.CV_8UC1, Scalar.Black);
                int ys = Math.Max((int)d.Y1, 0), ye = Math.Min((int)Math.Ceiling(d.Y2), imgH);
                int xs = Math.Max((int)d.X1, 0), xe = Math.Min((int)Math.Ceiling(d.X2), imgW);
                if (ye > ys && xe > xs)
                {
                    // 阈值比较走 CmpType.GE, 与 Python 的 >= 对齐(Threshold 是严格大于)
                    using var roi = new Mat(back, new Rect(xs, ys, xe - xs, ye - ys));
                    using var thr = new Mat(roi.Size(), roi.Type(), new Scalar(maskThr));
                    using var bin = new Mat();
                    Cv2.Compare(roi, thr, bin, CmpType.GE);
                    using var dst = new Mat(keep, new Rect(xs, ys, xe - xs, ye - ys));
                    bin.CopyTo(dst);
                }
                masks.Add(keep);
            }
            return masks;
        }
    }
}
