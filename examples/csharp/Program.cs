using System;

namespace EasyTrainerOnnx
{
    internal static class Program
    {
        // 用法: EasyTrainerOnnx <detect|segment|classify> <model.onnx> <image> [classes.txt]
        private static int Main(string[] args)
        {
            if (args.Length < 3)
            {
                Console.WriteLine("用法: EasyTrainerOnnx <detect|segment|classify> <model.onnx> <image> [classes.txt]");
                return 1;
            }
            string task = args[0], model = args[1], image = args[2];
            string classes = args.Length > 3 ? args[3] : "classes.txt";
            try
            {
                switch (task)
                {
                    case "detect": Detect.Run(model, image, classes); break;
                    case "segment": Segment.Run(model, image, classes); break;
                    case "classify": Classify.Run(model, image, classes); break;
                    default:
                        Console.WriteLine("未知任务: " + task);
                        return 1;
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("推理失败: " + e.Message);
                return 1;
            }
            return 0;
        }
    }
}
