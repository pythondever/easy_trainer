<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="en_US">
<context>
    <name>AdCommon</name>
    <message>
        <location filename="../app/train/ad_common.py" line="92"/>
        <source>找不到可写的纯英文暂存目录(异常检测的底层库不支持中文路径), 请把输出路径改到纯英文目录下</source>
        <translation>No writable ASCII-only temp directory found (the anomaly detection library does not support non-ASCII paths); change the output path to an ASCII-only directory</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="153"/>
        <location filename="../app/train/ad_common.py" line="659"/>
        <source>(根目录散图)</source>
        <translation>(loose images in root)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="176"/>
        <source>数据集里没找到图像, 请先导入数据</source>
        <translation>No images found in the dataset; import data first</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="181"/>
        <source>无法从类别名判断哪个是正常品, 请把放良品图的那个文件夹改名为 {} 之一; 现有类别: {}</source>
        <translation>Cannot tell which class holds good parts from the class names; rename the folder of good images to one of {}; existing classes: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="187"/>
        <source>训练集里没有图像</source>
        <translation>The train set has no images</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="191"/>
        <source>训练集里只有&quot;{}&quot;一类, 而良品类是&quot;{}&quot;; 请把良品图所在的类别文件夹挂到训练集上</source>
        <translation>The train set has only class &quot;{}&quot; while the good class is &quot;{}&quot;; attach the folder holding good images to the train set</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="199"/>
        <source>训练集里既没有&quot;{}&quot;类、又不止一类, 无法确定拿哪批图建库; 现有类别: {}</source>
        <translation>The train set has no class &quot;{}&quot; and more than one class, so it is unclear which images to use for the memory bank; existing classes: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="240"/>
        <source>训练集根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>The train root has both loose images and subfolders, so the class of the loose images is unclear; put them into one class folder</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="274"/>
        <source>没有找到任何图像, 请检查数据集</source>
        <translation>No images found; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="276"/>
        <source>根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>The root has both loose images and subfolders, so the class of the loose images is unclear; put them into one class folder</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="281"/>
        <source>无法判断哪个类别是良品, 现有类别: {}.
请把良品图放在名为 {} 一类的子文件夹里, 或按训练时的方式重新导入数据集</source>
        <translation>Cannot tell which class is good; existing classes: {}.
Put the good images in a subfolder named one of {}, or re-import the dataset the same way as for training</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="422"/>
        <source>未知的异常检测算法: {}</source>
        <translation>Unknown anomaly detection algorithm: {}</translation>
    </message>
</context>
<context>
    <name>AdPackage</name>
    <message>
        <location filename="../app/train/ad_package.py" line="88"/>
        <source>正在复制模型文件...</source>
        <translation>Copying model file...</translation>
    </message>
</context>
<context>
    <name>AdTestRunner</name>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="47"/>
        <source>缺少测试依赖: {}</source>
        <translation>Missing test dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="77"/>
        <source>加载异常检测模型: {}</source>
        <translation>Loading anomaly detection model: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="86"/>
        <source>算法={} 图像尺寸={} 阈值={:.6f}</source>
        <translation>Algorithm={} image size={} threshold={:.6f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="88"/>
        <source>原尺寸</source>
        <translation>original size</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="96"/>
        <source>没有可用的图像目录, 请检查数据集</source>
        <translation>No usable image directory; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="107"/>
        <source>测试图片 {} 张, 良品类别: {}</source>
        <translation>Testing {} images, good class: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="144"/>
        <source>没有取到任何图像, 请检查数据集</source>
        <translation>No images were read; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="151"/>
        <source>沿用训练时定下的阈值 {:.6f}</source>
        <translation>Using the threshold fixed during training {:.6f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="155"/>
        <source>模型里没有阈值, 本批又只有一类样本, 定不出判定阈值, 只报告分数</source>
        <translation>The model has no threshold and this batch has only one class, so no decision threshold can be derived; reporting scores only</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="159"/>
        <source>模型里没有阈值, 已按本批数据现挑 {:.6f}(精度会偏乐观)</source>
        <translation>The model has no threshold; {:.6f} was picked from this batch (accuracy will be optimistic)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="189"/>
        <source>完成: {} 张, 没有判定阈值, 只报告分数</source>
        <translation>Done: {} images, no decision threshold, scores only</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="195"/>
        <source>完成: {} 张, 检出异常 {} 张</source>
        <translation>Done: {} images, {} detected as anomalous</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="199"/>
        <source>完成: {} 张, 准确率 {:.4f}, 漏检 {} 张, 误检 {} 张</source>
        <translation>Done: {} images, accuracy {:.4f}, {} missed, {} false positives</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="204"/>
        <source>  image AUROC = {:.4f}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="220"/>
        <source>模型里没有判定阈值, 不输出异常区域</source>
        <translation>The model has no decision threshold; no anomaly regions written</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="223"/>
        <source>异常</source>
        <translation>Anomaly</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="233"/>
        <source>提取异常区域失败 {}: {}</source>
        <translation>Failed to extract the anomaly region {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="250"/>
        <source>输出异常区域失败 {}: {}</source>
        <translation>Failed to write the anomaly region {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="254"/>
        <source>已为 {} 张不良品图写出异常区域标注(图像同目录)</source>
        <translation>Wrote anomaly region labels for {} defective images (next to the images)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="258"/>
        <source>另有 {} 张判为不良品, 但热力图没超过判定线, 未写标注</source>
        <translation>{} more images were judged defective but their heatmaps stayed below the decision line; no labels written</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="277"/>
        <source>图像</source>
        <translation>Image</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="278"/>
        <source>类别</source>
        <translation>Class</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="279"/>
        <source>真值</source>
        <translation>Ground truth</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="280"/>
        <source>判定</source>
        <translation>Verdict</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="281"/>
        <source>分数</source>
        <translation>Score</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="282"/>
        <source>阈值</source>
        <translation>Threshold</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="283"/>
        <source>是否正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="298"/>
        <source>是</source>
        <translation>Yes</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="299"/>
        <source>否</source>
        <translation>No</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="301"/>
        <source>逐图明细: {}</source>
        <translation>Per-image details: {}</translation>
    </message>
</context>
<context>
    <name>AdTrainRunner</name>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="49"/>
        <source>缺少训练依赖: {}</source>
        <translation>Missing training dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="137"/>
        <source>anomalib {} / torch {}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="170"/>
        <source>输出路径: {}</source>
        <translation>Output path: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="172"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Training output directory (timestamp): {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="186"/>
        <source>异常检测: 算法={} 骨干={} 轮次={} 批次={} 图像尺寸={} device={}</source>
        <translation>Anomaly detection: algorithm={} backbone={} epochs={} batch={} image size={} device={}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="198"/>
        <source>数据准备: 建库集 {} 张({}), 测试集 正常 {} 张 / 异常 {} 张</source>
        <translation>Data ready: bank set {} images ({}), test set {} good / {} abnormal</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="203"/>
        <source>  异常类别: {}</source>
        <translation>    abnormal classes: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="204"/>
        <source>(散图)</source>
        <translation>(loose images)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="209"/>
        <source>  注意: 建库集里另有 {} 张非正常图, 未参与建库</source>
        <translation>    note: the bank set has {} abnormal images that were not used</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="213"/>
        <source>建库集里没有图像, 请检查数据集</source>
        <translation>The bank set has no images; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="215"/>
        <source>测试集里没有图像, 请检查数据集</source>
        <translation>The test set has no images; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="234"/>
        <source>数据集: 建库集 {} 张</source>
        <translation>Dataset: bank set {} images</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="243"/>
        <source>模型构建完成({:.1f}s): {}</source>
        <translation>Model built in {:.1f}s: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="261"/>
        <source>建库/训练完成({:.1f}s)</source>
        <translation>Bank/training finished in {:.1f}s</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="274"/>
        <source>  评估中: {} 张</source>
        <translation>    evaluating: {} images</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="283"/>
        <source>评估阶段失败, 只交付模型: {}</source>
        <translation>Evaluation failed; delivering the model only: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="288"/>
        <source>评估完成({:.1f}s): {} 张</source>
        <translation>Evaluation finished in {:.1f}s: {} images</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="291"/>
        <source>  测试集里只有一类样本, 定不出判定阈值(没有真值反差), AUROC 和准确率都算不了; 补一些异常样本重新训练才有交付阈值</source>
        <translation>    the test set has only one class, so no decision threshold can be derived (no contrast in ground truth) and neither AUROC nor accuracy can be computed; retrain with some abnormal samples to get a deliverable threshold</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="296"/>
        <source>评估完成({:.1f}s): {} 张, 准确率 {:.4f}</source>
        <translation>Evaluation finished in {:.1f}s: {} images, accuracy {:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="300"/>
        <source>  image AUROC = {:.4f}  阈值 = {:.6f}(本批最优 F1 处)</source>
        <translation>    image AUROC = {:.4f}  threshold = {:.6f} (best F1 on this batch)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="303"/>
        <source>  漏检 {} 张(不良判成良品), 误检 {} 张</source>
        <translation>    {} missed (defective judged good), {} false positives</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="307"/>
        <source>  AUROC 无法计算</source>
        <translation>    AUROC cannot be computed</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="321"/>
        <source>模型已保存: {} ({:.0f} MB)</source>
        <translation>Model saved: {} ({:.0f} MB)</translation>
    </message>
</context>
<context>
    <name>AddLabelDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="169"/>
        <source>添加标签</source>
        <translation>Add Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="186"/>
        <source>编辑标签</source>
        <translation>Edit Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="188"/>
        <source>标签名称</source>
        <translation>Label name</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="223"/>
        <source>标签名称, 多个用逗号分隔</source>
        <translation>Label names, separate multiple with commas</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="225"/>
        <source>导入</source>
        <translation>Import</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="232"/>
        <source>选择数据集...</source>
        <translation>Select dataset...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="255"/>
        <location filename="../app/annotation/annotation_dialog.py" line="260"/>
        <source>导入标签</source>
        <translation>Import Labels</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="256"/>
        <source>请先选择一个数据集</source>
        <translation>Select a dataset first</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="261"/>
        <source>数据集&quot;{}&quot;还没有标签</source>
        <translation>Dataset &quot;{}&quot; has no labels yet</translation>
    </message>
</context>
<context>
    <name>AnnotationDialog</name>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="207"/>
        <source>复制</source>
        <translation>Copy</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="209"/>
        <source>填充</source>
        <translation>Fill</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="219"/>
        <source>粘贴</source>
        <translation>Paste</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="375"/>
        <source>标注 - {} / {}</source>
        <translation>Annotation - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="393"/>
        <location filename="../app/annotation/annotation_dialog.py" line="981"/>
        <source>矩形</source>
        <translation>Rectangle</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="394"/>
        <location filename="../app/annotation/annotation_dialog.py" line="987"/>
        <source>多边形</source>
        <translation>Polygon</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="403"/>
        <source>标签列表</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="404"/>
        <source>标注信息</source>
        <translation>Annotations</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="408"/>
        <source>上一张</source>
        <translation>Prev</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="409"/>
        <source>下一张</source>
        <translation>Next</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="444"/>
        <source>只在选中的多边形框内生效; A/D 切图或 Ctrl+S 才写盘</source>
        <translation>Applies only inside the selected polygon; written to disk on A/D image switch or Ctrl+S</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="482"/>
        <source>显示标注</source>
        <translation>Show labels</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="488"/>
        <source>文本标注</source>
        <translation>Text Annotation</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="642"/>
        <source>保存失败</source>
        <translation>Save failed</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="643"/>
        <source>写文字标签失败:
{}</source>
        <translation>Failed to write the text label:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="658"/>
        <source>已标注 {} · 未标注 {}</source>
        <translation>Labeled {} · Unlabeled {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="820"/>
        <source>编辑标签</source>
        <translation>Edit Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1139"/>
        <source>转换</source>
        <translation>Convert</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1140"/>
        <source>设置像素精度, 在像素面积后显示物理面积</source>
        <translation>Set the pixel scale to show physical area after the pixel area</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1144"/>
        <source>当前像素精度 {}, 点击修改</source>
        <translation>Current pixel scale {}, click to change</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="582"/>
        <source>先在画布上点选一个多边形</source>
        <translation>Select a polygon on the canvas first</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="585"/>
        <source>亮度调节只对多边形有效</source>
        <translation>Brightness adjustment only works on polygons</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="378"/>
        <source>    类别: {}</source>
        <translation>    Class: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="408"/>
        <source>删除本地文件</source>
        <translation>Delete local files</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="409"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="411"/>
        <location filename="../app/annotation/annotation_io.py" line="420"/>
        <source>删除图像</source>
        <translation>Delete Image</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="412"/>
        <source>是否删除当前图像?

{}</source>
        <translation>Delete the current image?

{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="415"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>The image and its label file will be deleted from disk. This cannot be undone</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="421"/>
        <source>无法访问主窗口, 删除失败</source>
        <translation>Cannot reach the main window; delete failed</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="434"/>
        <source>(无图像)</source>
        <translation>(no image)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="718"/>
        <location filename="../app/annotation/annotation_dialog.py" line="927"/>
        <location filename="../app/annotation/annotation_dialog.py" line="933"/>
        <source>添加标签</source>
        <translation>Add Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="719"/>
        <source>请先添加标签(点击&quot;+&quot;)</source>
        <translation>Add a label first (click &quot;+&quot;)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="820"/>
        <source>剪切板  {}/{}</source>
        <translation>Clipboard  {}/{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="845"/>
        <source>第 {} 个模板  {}x{}
左键选中用于粘贴, 右键 删除/导入/导出/清空</source>
        <translation>Template {}  {}x{}
Left click to select for pasting; right click to delete / import / export / clear</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="877"/>
        <location filename="../app/annotation/annotation_dialog.py" line="792"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="880"/>
        <source>导入</source>
        <translation>Import</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="881"/>
        <source>导出</source>
        <translation>Export</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="883"/>
        <source>清空</source>
        <translation>Clear</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="474"/>
        <location filename="../app/annotation/annotation_io.py" line="503"/>
        <location filename="../app/annotation/annotation_io.py" line="508"/>
        <source>导出剪切板</source>
        <translation>Export Clipboard</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="475"/>
        <source>剪切板是空的, 没有可导出的模板</source>
        <translation>The clipboard is empty; nothing to export</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="478"/>
        <source>选择导出目录</source>
        <translation>Select Export Directory</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="504"/>
        <source>导出中断: {}
(已写出 {} 个)</source>
        <translation>Export interrupted: {}
({} written)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="509"/>
        <source>已导出 {} 个模板(png + 同名 json)到:
{}</source>
        <translation>Exported {} template(s) (png + same-name json) to:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="515"/>
        <source>选择导入目录</source>
        <translation>Select Import Directory</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="522"/>
        <location filename="../app/annotation/annotation_io.py" line="526"/>
        <location filename="../app/annotation/annotation_io.py" line="560"/>
        <source>导入剪切板</source>
        <translation>Import Clipboard</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="523"/>
        <source>读取目录失败: {}</source>
        <translation>Failed to read the directory: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="527"/>
        <source>这个目录里没有 png 文件</source>
        <translation>No png files in this directory</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="555"/>
        <source>已导入 {} 个模板到剪切板</source>
        <translation>Imported {} template(s) into the clipboard</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="557"/>
        <source>
其中 {} 个没有同名 json, 按矩形导入</source>
        <translation>
{} of them have no same-name json and were imported as rectangles</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="559"/>
        <source>
{} 个文件读不出来, 已跳过</source>
        <translation>
{} file(s) could not be read and were skipped</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="732"/>
        <source>修改类别</source>
        <translation>Change Class</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="733"/>
        <source>移动图像文件失败:
{}</source>
        <translation>Failed to move the image file:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="791"/>
        <source>编辑</source>
        <translation>Edit</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="887"/>
        <location filename="../app/annotation/annotation_dialog.py" line="894"/>
        <location filename="../app/annotation/annotation_io.py" line="578"/>
        <source>删除标签</source>
        <translation>Delete Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="579"/>
        <source>正在统计标注文件...</source>
        <translation>Counting label files...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="888"/>
        <source>标签&quot;{}&quot;已有 {} 处标注, 删除后这些标注将被一并删除且不可恢复.
确定删除吗?</source>
        <translation>Label &quot;{}&quot; has {} annotation(s). Deleting it removes them all and cannot be undone.
Delete anyway?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="895"/>
        <source>确定删除标签&quot;{}&quot;吗?</source>
        <translation>Delete label &quot;{}&quot;?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="821"/>
        <location filename="../app/annotation/annotation_dialog.py" line="928"/>
        <source>标签名称不能为空</source>
        <translation>Label name cannot be empty</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="988"/>
        <source>{} 个顶点</source>
        <translation>{} vertices</translation>
    </message>
</context>
<context>
    <name>App</name>
    <message>
        <location filename="../app/main_window.py" line="57"/>
        <source>软件启动</source>
        <translation>App started</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="60"/>
        <source>软件退出</source>
        <translation>App exited</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="62"/>
        <source>软件退出前停止训练</source>
        <translation>Stopping training before exit</translation>
    </message>
</context>
<context>
    <name>AppUI</name>
    <message>
        <location filename="../ui/app.ui" line="14"/>
        <location filename="../ui/app.ui" line="87"/>
        <source>EasyTrainer</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="114"/>
        <location filename="../ui/app.ui" line="170"/>
        <source>项目</source>
        <translation>Projects</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="193"/>
        <source>添加项目</source>
        <translation>Add Project</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="196"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="335"/>
        <source>项目训练中</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="365"/>
        <source>停止训练</source>
        <translation>Stop Training</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="372"/>
        <source>剩余时间:</source>
        <translation>Time Left:</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="382"/>
        <source>显存:</source>
        <translation>VRAM:</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="389"/>
        <source>20%</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="399"/>
        <source>统计</source>
        <translation>Stats</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="406"/>
        <source>训练</source>
        <translation>Train</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="413"/>
        <source>模型</source>
        <translation>Models</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="420"/>
        <location filename="../app/mixins/queue_mixin.py" line="368"/>
        <source>队列</source>
        <translation>Queue</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="427"/>
        <source>日志</source>
        <translation>Log</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="446"/>
        <source>界面语言</source>
        <translation>Interface language</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="537"/>
        <source>上一页</source>
        <translation>Prev</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="566"/>
        <source>下一页</source>
        <translation>Next</translation>
    </message>
</context>
<context>
    <name>Charts</name>
    <message>
        <location filename="../app/widgets/charts.py" line="12"/>
        <source>暂无标注</source>
        <translation>No annotations</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="13"/>
        <source>标签</source>
        <translation>Label</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="14"/>
        <source>标签数量</source>
        <translation>Label count</translation>
    </message>
</context>
<context>
    <name>ClassifyTestRunner</name>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="34"/>
        <source>缺少测试依赖: {}</source>
        <translation>Missing test dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="86"/>
        <source>加载分类模型: {}</source>
        <translation>Loading classification model: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="112"/>
        <source>测试图片 {} 张</source>
        <translation>{} test images</translation>
    </message>
</context>
<context>
    <name>ClassifyTrainRunner</name>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="41"/>
        <source>缺少训练依赖: {}</source>
        <translation>Missing training dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="133"/>
        <source>输出路径: {}</source>
        <translation>Output path: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="134"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Run output directory (timestamp): {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="150"/>
        <source>分类训练: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</source>
        <translation>Classification training: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="159"/>
        <source>数据准备: train={} 张, val={} 张</source>
        <translation>Data prep: train={} images, val={} images</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="161"/>
        <source>训练集无图像, 请检查数据集</source>
        <translation>Train set has no images; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="163"/>
        <source>验证集无图像, 请检查数据集</source>
        <translation>Val set has no images; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="188"/>
        <source>未从数据集中解析到任何类别(子文件夹),无法训练图像分类</source>
        <translation>No classes (subfolders) parsed from the dataset; cannot train image classification</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="198"/>
        <source>数据集: train={} val={} 类别({})={}</source>
        <translation>Dataset: train={} val={} classes({})={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="290"/>
        <source>早停触发: 连续 {} 个 epoch 精度无提升</source>
        <translation>Early stop triggered: no accuracy gain for {} epochs in a row</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="295"/>
        <source>训练完成 best_acc={:.4f}</source>
        <translation>Training complete best_acc={:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="303"/>
        <source>生成类别文件: {}</source>
        <translation>Writing class file: {}</translation>
    </message>
</context>
<context>
    <name>CollapsibleText</name>
    <message>
        <location filename="../app/widgets/collapsible_text.py" line="47"/>
        <source>点击展开 / 收起完整内容</source>
        <translation>Click to expand / collapse</translation>
    </message>
</context>
<context>
    <name>ColorPickerDialog</name>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="396"/>
        <source>选择颜色</source>
        <translation>Pick Color</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="408"/>
        <source>十六进制:</source>
        <translation>Hex:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="429"/>
        <source>基本颜色:</source>
        <translation>Basic colors:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="441"/>
        <source>自定义 RGB:</source>
        <translation>Custom RGB:</translation>
    </message>
</context>
<context>
    <name>CompareDialog</name>
    <message>
        <location filename="../ui/compare.ui" line="14"/>
        <source>对比多次训练</source>
        <translation>Compare Runs</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="22"/>
        <source>对比指标</source>
        <translation>Compare Metric</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="38"/>
        <source>记录范围</source>
        <translation>Record range</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="65"/>
        <location filename="../app/widgets/compare_dialog.py" line="680"/>
        <location filename="../app/widgets/compare_dialog.py" line="684"/>
        <location filename="../app/widgets/compare_dialog.py" line="701"/>
        <source>导出对比报告</source>
        <translation>Export comparison report</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="72"/>
        <location filename="../app/widgets/compare_dialog.py" line="708"/>
        <location filename="../app/widgets/compare_dialog.py" line="712"/>
        <source>删除选中</source>
        <translation>Delete selected</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="97"/>
        <source>训练记录（可勾选，上限 8 条）</source>
        <translation>Training records (checkable, up to 8)</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="168"/>
        <source>关键指标汇总</source>
        <translation>Key metrics summary</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="188"/>
        <source>差异与结论</source>
        <translation>Differences and conclusion</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="305"/>
        <source>勾选要对比的训练记录(最多 {} 条), 双击查看单次指标</source>
        <translation>Tick the training runs to compare (up to {}); double-click to view one run&apos;s metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="280"/>
        <source>数据来源：LMDB train_history + metrics.csv / metrics json</source>
        <translation>Data source: LMDB train_history + metrics.csv / metrics json</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="501"/>
        <source>一次最多对比 {} 条记录</source>
        <translation>At most {} runs can be compared at once</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="529"/>
        <source>{} 训练曲线（按 epoch）</source>
        <translation>{} training curve (by epoch)</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="536"/>
        <source>已选 {} 条（上限 {}）</source>
        <translation>{} selected (max {})</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="538"/>
        <source>已选 {} 条(上限 {}), 双击左侧记录可查看单次指标</source>
        <translation>{} selected (limit {}); double-click a run on the left to view its metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="540"/>
        <location filename="../app/widgets/compare_dialog.py" line="566"/>
        <source>勾选左侧的训练记录后这里显示对比曲线</source>
        <translation>Tick runs on the left to show their comparison curves here</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="634"/>
        <source>无</source>
        <translation>None</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="647"/>
        <source>至少勾选 2 条记录&lt;br&gt;才能比较差异</source>
        <translation>Select at least 2 records&lt;br&gt;to compare differences</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="681"/>
        <source>当前没有可导出的对比图表</source>
        <translation>No comparison chart to export</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="685"/>
        <source>PNG 图片 (*.png)</source>
        <translation>PNG image (*.png)</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="699"/>
        <source>已导出: {}
{}</source>
        <translation>Exported: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="702"/>
        <source>导出失败: {}</source>
        <translation>Export failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="709"/>
        <source>请先勾选要删除的训练记录</source>
        <translation>Select records to delete first</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="713"/>
        <source>确定删除选中的 {} 条训练记录? 对应指标文件会一并删除.</source>
        <translation>Delete the {} selected training records? Their metric files will be removed too.</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="570"/>
        <source>所选记录没有&quot;{}&quot;的数据</source>
        <translation>The selected runs have no &quot;{}&quot; data</translation>
    </message>
</context>
<context>
    <name>DataPrep</name>
    <message>
        <location filename="../app/train/data_prep.py" line="207"/>
        <source>解析到类别 {} 个: {}</source>
        <translation>Parsed {} classes: {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="227"/>
        <source>复制数据集 {}: 图像 {} 张, 标签 {} 个 → {}</source>
        <translation>Copy dataset {}: {} images, {} labels → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="314"/>
        <source>合并 {} 数据集 → {} ({} 个文件)</source>
        <translation>Merge {} dataset → {} ({} files)</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="331"/>
        <source>生成 data.yaml → {}</source>
        <translation>Write data.yaml → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="345"/>
        <source>未从数据集中解析到任何标签类别, 请检查标签文件</source>
        <translation>No label classes parsed from the dataset; check the label files</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="352"/>
        <source>数据准备完成: {} 个类别, 输出目录 {}</source>
        <translation>Data prep done: {} classes, output directory {}</translation>
    </message>
</context>
<context>
    <name>DatasetViewMixin</name>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="282"/>
        <source>删除全部未标注图像({} 张)</source>
        <translation>Delete all unlabeled images ({} images)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="288"/>
        <source>删除所选图像({} 张)</source>
        <translation>Delete selected images ({} images)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="313"/>
        <source>图像文件不存在, 无法打开标注: {}</source>
        <translation>Image file missing; the annotation cannot be opened: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="317"/>
        <source>图像文件不存在</source>
        <translation>Image file missing</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="318"/>
        <source>该图像已不在磁盘上, 无法打开标注. 文件可能被移动、改名或删除了.</source>
        <translation>This image is no longer on disk; the annotation cannot be opened. The file may have been moved, renamed or deleted.</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="321"/>
        <source>失效文件</source>
        <translation>Missing file</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="418"/>
        <source>重载跳过: 数据集 {}/{} 无图像目录</source>
        <translation>Reload skipped: dataset {}/{} has no image directory</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="419"/>
        <source>重载</source>
        <translation>Reload</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="420"/>
        <source>该数据集还没有图像目录, 请先右键&quot;导入&quot;</source>
        <translation>This dataset has no image directory yet; right-click &quot;Import&quot; first</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="424"/>
        <source>重载跳过: 数据集 {}/{} 正在载入</source>
        <translation>Reload skipped: dataset {}/{} is loading</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="426"/>
        <source>重载数据集: {}/{}</source>
        <translation>Reload dataset: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="659"/>
        <source>数据集 {}/{} 含 OCR 文本标注, 已标为字符检测数据集</source>
        <translation>Dataset {}/{} contains OCR text annotations, marked as a text detection dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1099"/>
        <source>第 {} / {} 页</source>
        <translation>Page {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1103"/>
        <source>第 {}/{} 页 · 共 {} 个</source>
        <translation>Page {}/{} · {} items</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1105"/>
        <source>第 {}/{} 页 · 共 {} 张</source>
        <translation>Page {}/{} · {} images</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1118"/>
        <source>未选择标签</source>
        <translation>No labels selected</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1120"/>
        <source>暂无数据</source>
        <translation>No data</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1161"/>
        <source>开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}</source>
        <translation>Import start: {}/{} | image path={} | label path={} | format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1162"/>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1234"/>
        <source>(无)</source>
        <translation>(none)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1229"/>
        <source>{}: {}个</source>
        <translation>{}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1231"/>
        <source>数据集导入完成: {}/{} | 图像 {} 张, 已标注 {} 张 | 标签({}类): {}</source>
        <translation>Dataset import done: {}/{} | {} images, {} labeled | labels ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1277"/>
        <source>数据集 {}/{} 未导入, 右键&quot;导入&quot;选择图像与标签目录</source>
        <translation>Dataset {}/{} not imported; right-click &quot;Import&quot; to choose the image and label folders</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1288"/>
        <source>数据集 {}/{} 有 {} 个图像目录不存在, 已跳过</source>
        <translation>Dataset {}/{} has {} missing image directories; skipped</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1302"/>
        <source>数据集 {}/{} 的图像目录不存在, 无法载入</source>
        <translation>Image directory of dataset {}/{} is missing; cannot load</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1306"/>
        <source>图像目录不存在</source>
        <translation>Image directory missing</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1307"/>
        <source>数据集「{}」的图像目录已不在磁盘上, 无法载入图像. 目录可能被移动、改名或删除了.</source>
        <translation>The image directory of dataset &quot;{}&quot; is no longer on disk; images cannot be loaded. The directory may have been moved, renamed or deleted.</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1310"/>
        <source>失效目录 · {} 个</source>
        <translation>{} missing directories</translation>
    </message>
</context>
<context>
    <name>Dialog</name>
    <message>
        <location filename="../ui/dataset_properties.ui" line="14"/>
        <source>数据集属性</source>
        <translation>Dataset Properties</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="30"/>
        <source>选择数据:</source>
        <translation>Select dataset:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="53"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="77"/>
        <source>图像路径:</source>
        <translation>Image path:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="98"/>
        <source>标签路径:</source>
        <translation>Label path:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="119"/>
        <source>标签分布:</source>
        <translation>Label distribution:</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="14"/>
        <source>导出</source>
        <translation>Export</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="36"/>
        <source>请选择导出路径</source>
        <translation>Select an export path</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="90"/>
        <source>导出格式</source>
        <translation>Export format</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="106"/>
        <source>labelme 格式</source>
        <translation>labelme format</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="119"/>
        <source>yolo 格式</source>
        <translation>yolo format</translation>
    </message>
</context>
<context>
    <name>DialogButtons</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="220"/>
        <location filename="../app/mixins/import_export_mixin.py" line="278"/>
        <location filename="../app/mixins/misc_mixin.py" line="123"/>
        <location filename="../app/widgets/dialog_buttons.py" line="110"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../app/widgets/dialog_buttons.py" line="116"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
</context>
<context>
    <name>DiffPanel</name>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="93"/>
        <source>最佳记录</source>
        <translation>Best record</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="94"/>
        <source>按 {}</source>
        <translation>by {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="112"/>
        <source>参数差异</source>
        <translation>Parameter differences</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="112"/>
        <source>仅列取值不同的项</source>
        <translation>Only differing values</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="121"/>
        <source>所选记录参数完全一致</source>
        <translation>Selected records share identical parameters</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="130"/>
        <source>共同</source>
        <translation>Common</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="160"/>
        <source>结论</source>
        <translation>Conclusion</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="175"/>
        <source>最佳</source>
        <translation>Best</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="185"/>
        <source>它独有的设置</source>
        <translation>unique to it</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="189"/>
        <source>启用增强 {}/{} 条</source>
        <translation>Augmentation enabled on {}/{}:</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="192"/>
        <source>所选记录都没有启用数据增强</source>
        <translation>No record enabled data augmentation</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="197"/>
        <source>仍在训练</source>
        <translation>still training</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="199"/>
        <source>曲线未收敛， 对比仅供参考</source>
        <translation>curve not converged, for reference only</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="204"/>
        <source>未跑完</source>
        <translation>unfinished</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="204"/>
        <source>不参与最佳判定</source>
        <translation>excluded from best pick</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="207"/>
        <source>训练时长</source>
        <translation>Training duration</translation>
    </message>
</context>
<context>
    <name>ImportData</name>
    <message>
        <location filename="../ui/import_data.ui" line="14"/>
        <source>导入数据</source>
        <translation>Import Data</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="33"/>
        <source>图像路径</source>
        <translation>Image path</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="73"/>
        <source>标签路径</source>
        <translation>Label path</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="107"/>
        <source>标签格式:</source>
        <translation>Label format:</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="114"/>
        <source>Yolo txt</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="121"/>
        <source>Labelme json</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="131"/>
        <source>按子文件夹分类导入</source>
        <translation>Import as classification (subfolders)</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="155"/>
        <source>提示信息</source>
        <translation>Info</translation>
    </message>
</context>
<context>
    <name>ImportExportMixin</name>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="59"/>
        <source>导入数据 - {} / {}</source>
        <translation>Import Data - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="66"/>
        <location filename="../app/mixins/import_export_mixin.py" line="166"/>
        <source>请选择图像文件夹</source>
        <translation>Choose an image folder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="142"/>
        <source>请选择分类根目录(子文件夹名=类别)</source>
        <translation>Choose the classification root folder (subfolder name = class)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="155"/>
        <source>(根目录)</source>
        <translation>(root folder)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="157"/>
        <source>所选文件夹下无分类子文件夹或图像</source>
        <translation>No class subfolders or images in the selected folder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="159"/>
        <source>{}: {}张</source>
        <translation>{}: {} images</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="161"/>
        <source>检测到 {} 类: {}</source>
        <translation>Detected {} classes: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="80"/>
        <source>所选文件夹无图像</source>
        <translation>No images in the selected folder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="83"/>
        <source>共 {} 张图像, 已标注 {} 张</source>
        <translation>{} images, {} labeled</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="99"/>
        <source>(检测到 {} 张 {} 标签, 请切换上方格式为&quot;{}&quot;)</source>
        <translation>({} {} label(s) detected; switch the format above to &quot;{}&quot;)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="103"/>
        <source>共 {} 张图像, 已标注 0 张 {}</source>
        <translation>{} images, 0 labeled {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="105"/>
        <source>共 {} 张图像(标签目录无匹配文件)</source>
        <translation>{} images (no matching files in the label folder)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="172"/>
        <source>选择文件夹</source>
        <translation>Select Folder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="212"/>
        <source>分类根目录(子文件夹名=类别)</source>
        <translation>Classification root (subfolder name = class)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="212"/>
        <source>图像路径</source>
        <translation>Image path</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="234"/>
        <location filename="../app/mixins/import_export_mixin.py" line="237"/>
        <source>导入数据</source>
        <translation>Import Data</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="234"/>
        <source>请先选择有效的图像文件夹</source>
        <translation>Choose a valid image folder first</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="237"/>
        <source>标签路径无效</source>
        <translation>Invalid label path</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="298"/>
        <location filename="../app/mixins/import_export_mixin.py" line="303"/>
        <location filename="../app/mixins/import_export_mixin.py" line="314"/>
        <location filename="../app/mixins/import_export_mixin.py" line="322"/>
        <location filename="../app/mixins/import_export_mixin.py" line="339"/>
        <location filename="../app/mixins/import_export_mixin.py" line="349"/>
        <location filename="../app/mixins/import_export_mixin.py" line="362"/>
        <location filename="../app/mixins/import_export_mixin.py" line="371"/>
        <source>导出</source>
        <translation>Export</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="298"/>
        <source>请先在左侧选中要导出的数据集</source>
        <translation>Select the dataset to export on the left first</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="311"/>
        <source>打开</source>
        <translation>Open</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="322"/>
        <source>请先选择导出保存位置</source>
        <translation>Choose where to save the export first</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="333"/>
        <source>开始导出: 项目={} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>Export start: project={} | source path={} | save path={} | format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="339"/>
        <source>正在导出项目...</source>
        <translation>Exporting project...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="350"/>
        <source>项目&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>Project &quot;{}&quot; exported: {} images copied
Location: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="352"/>
        <source>导出项目完成: {} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>Project export done: {} | {} images | labels ({}) | format={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="358"/>
        <source>开始导出: 数据集={}/{} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>Export start: dataset={}/{} | source path={} | save path={} | format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="362"/>
        <source>正在导出数据集...</source>
        <translation>Exporting dataset...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="372"/>
        <source>数据集&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>Dataset &quot;{}&quot; exported: {} images copied
Location: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="375"/>
        <source>导出数据集完成: {}/{} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>Dataset export done: {}/{} | {} images | labels ({}) | format={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="380"/>
        <source>导出失败: 项目={} 数据集={} | {}</source>
        <translation>Export failed: project={} dataset={} | {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="381"/>
        <source>(整个项目)</source>
        <translation>(whole project)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="382"/>
        <source>导出失败</source>
        <translation>Export Failed</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="385"/>
        <source>选择导出保存位置</source>
        <translation>Select Export Destination</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="411"/>
        <source>{} =&gt; 标签:{}</source>
        <translation>{} =&gt; labels:{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="412"/>
        <location filename="../app/mixins/import_export_mixin.py" line="413"/>
        <source>(无)</source>
        <translation>(none)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="420"/>
        <source>(无标签)</source>
        <translation>(no labels)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="463"/>
        <source>正在导出: {}</source>
        <translation>Exporting: {}</translation>
    </message>
</context>
<context>
    <name>ImportTask</name>
    <message>
        <location filename="../app/tasks/import_task.py" line="109"/>
        <source>导入跳过 {}: {}</source>
        <translation>Import skipped {}: {}</translation>
    </message>
</context>
<context>
    <name>LabelFilter</name>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="60"/>
        <location filename="../app/widgets/label_filter_popup.py" line="451"/>
        <source>全选</source>
        <translation>Select all</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="464"/>
        <source>显示全部图像</source>
        <translation>Showing all images</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="466"/>
        <source>按所选标签过滤</source>
        <translation>Filtered by selected labels</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="468"/>
        <source>未选择标签</source>
        <translation>No labels selected</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="533"/>
        <source>收起</source>
        <translation>Collapse</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="534"/>
        <source>展开全部</source>
        <translation>Show all</translation>
    </message>
</context>
<context>
    <name>LabelMixin</name>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="88"/>
        <source>已选 {} 个</source>
        <translation>{} selected</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="89"/>
        <source>全选</source>
        <translation>Select all</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="91"/>
        <location filename="../app/mixins/label_mixin.py" line="108"/>
        <source>未选择标签</source>
        <translation>No labels selected</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="100"/>
        <location filename="../app/mixins/label_mixin.py" line="175"/>
        <source>未标注</source>
        <translation>Unlabeled</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="213"/>
        <source>重命名</source>
        <translation>Rename</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="219"/>
        <source>合并标签</source>
        <translation>Merge Labels</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="220"/>
        <source>标签&quot;{}&quot;已存在.
确定把&quot;{}&quot;的所有标注合并到&quot;{}&quot;吗?
此操作会改写数据集源标签文件, 且不可恢复.</source>
        <translation>Label &quot;{}&quot; already exists.
Merge all annotations of &quot;{}&quot; into &quot;{}&quot;?
This rewrites the dataset&apos;s source label files and cannot be undone.</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="275"/>
        <source>合并标签: {} → {} ({}/{}) | 启动后台文件合并, 完成后输出统计</source>
        <translation>Merge labels: {} → {} ({}/{}) | background file merge started; stats printed when done</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="278"/>
        <source>重命名标签: {} → {} ({}/{})</source>
        <translation>Rename label: {} → {} ({}/{})</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="354"/>
        <source>{}: {}个</source>
        <translation>{}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="357"/>
        <source>删除标签完成: {} | 修改 {} 个标签文件 | 删除后标签统计({}类): {}</source>
        <translation>Delete label done: {} | {} label files changed | label stats after delete ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="360"/>
        <location filename="../app/mixins/label_mixin.py" line="365"/>
        <location filename="../app/mixins/label_mixin.py" line="370"/>
        <source>(无)</source>
        <translation>(none)</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="362"/>
        <source>合并标签: {} → {} | 修改 {} 个标签文件 | 合并后标签统计({}类): {}</source>
        <translation>Merge labels: {} → {} | {} label files changed | label stats after merge ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="367"/>
        <source>合并标签: {} → {} | 无标签文件被修改 | 合并后标签统计({}类): {}</source>
        <translation>Merge labels: {} → {} | no label files changed | label stats after merge ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="461"/>
        <source>删除标签: {} ({}/{})</source>
        <translation>Delete label: {} ({}/{})</translation>
    </message>
</context>
<context>
    <name>LogDialog</name>
    <message>
        <location filename="../ui/log.ui" line="14"/>
        <source>Dialog</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/log.ui" line="37"/>
        <source>清空</source>
        <translation>Clear</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="79"/>
        <location filename="../app/widgets/log_dialog.py" line="21"/>
        <source>日志</source>
        <translation>Log</translation>
    </message>
</context>
<context>
    <name>MessageBox</name>
    <message>
        <location filename="../app/widgets/message_box.py" line="343"/>
        <location filename="../app/widgets/message_box.py" line="384"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="105"/>
        <source>详情已复制到剪贴板</source>
        <translation>Details copied to clipboard</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="253"/>
        <source>复制</source>
        <translation>Copy</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="284"/>
        <source>…还有 {} 个</source>
        <translation>…and {} more</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="335"/>
        <source>关闭</source>
        <translation>Close</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="337"/>
        <source>复制详情</source>
        <translation>Copy details</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="364"/>
        <source>知道了</source>
        <translation>Got it</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="385"/>
        <location filename="../app/widgets/message_box.py" line="432"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="456"/>
        <source>取消中...</source>
        <translation>Cancelling...</translation>
    </message>
</context>
<context>
    <name>MetricLabel</name>
    <message>
        <location filename="../app/core/metrics.py" line="33"/>
        <source>mAP@50</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/core/metrics.py" line="35"/>
        <source>mask mAP50</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/core/metrics.py" line="37"/>
        <source>准确率</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../app/core/metrics.py" line="39"/>
        <source>AUROC</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/core/metrics.py" line="42"/>
        <source>F1@0.5</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/core/metrics.py" line="44"/>
        <source>CER</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>MetricTabs</name>
    <message>
        <location filename="../app/widgets/metric_tabs.py" line="73"/>
        <source>所选记录都没有 {} 的数据</source>
        <translation>None of the selected records have {} data</translation>
    </message>
</context>
<context>
    <name>MetricsDialog</name>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="50"/>
        <source>训练指标</source>
        <translation>Training Metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="79"/>
        <source>标签筛选</source>
        <translation>Label filter</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="83"/>
        <source>全部指标</source>
        <translation>All metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="84"/>
        <source>全部标签-P</source>
        <translation>All labels - P</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="85"/>
        <source>全部标签-R</source>
        <translation>All labels - R</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="121"/>
        <source>暂无该标签的指标数据(训练完成后可查看)</source>
        <translation>No metric data for this label yet (available after training completes)</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="169"/>
        <source>loss 值</source>
        <translation>Loss</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="170"/>
        <source>指标值 (mAP/P/R)</source>
        <translation>Metric (mAP/P/R)</translation>
    </message>
</context>
<context>
    <name>MiscMixin</name>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="54"/>
        <source>界面语言: {}</source>
        <translation>Interface language: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="115"/>
        <source>数据集统计</source>
        <translation>Dataset Statistics</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="124"/>
        <source>应用所选数据集</source>
        <translation>Apply selected datasets</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="215"/>
        <source>[{}/{}](未设置)</source>
        <translation>[{}/{}](not set)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="218"/>
        <source>(未选择数据集)</source>
        <translation>(no dataset selected)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="338"/>
        <source>删除图像: {} 张 | 本地删除文件={} | 项目={}, 数据集={}</source>
        <translation>Delete images: {} | delete local files={} | project={}, dataset={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="376"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="377"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="379"/>
        <source>删除图像</source>
        <translation>Delete Images</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="380"/>
        <source>将从系统删除所选 {} 张图像?

(图像与同名标注文件不可恢复)</source>
        <translation>Delete the selected {} image(s) from the system?

(Images and their label files cannot be recovered)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="384"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>Images and their label files will be deleted from disk. This cannot be undone</translation>
    </message>
</context>
<context>
    <name>ModelAssets</name>
    <message>
        <location filename="../app/core/model_assets.py" line="87"/>
        <location filename="../app/core/model_assets.py" line="121"/>
        <source>速度最快, 精度够用</source>
        <translation>Fastest, accuracy is sufficient</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="88"/>
        <location filename="../app/core/model_assets.py" line="125"/>
        <source>精度更好, 稍慢一些</source>
        <translation>Better accuracy, slightly slower</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="89"/>
        <location filename="../app/core/model_assets.py" line="129"/>
        <source>精度更高</source>
        <translation>Higher accuracy</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="90"/>
        <source>精度最高, 显存占用大</source>
        <translation>Highest accuracy, but uses more VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="91"/>
        <source>精度极致, 显存占用很大</source>
        <translation>Ultimate accuracy, uses much more VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="94"/>
        <location filename="../app/core/model_assets.py" line="140"/>
        <source>轻量分割</source>
        <translation>Lightweight segmentation</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="95"/>
        <location filename="../app/core/model_assets.py" line="144"/>
        <source>速度与精度平衡</source>
        <translation>Balanced speed and accuracy</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="96"/>
        <location filename="../app/core/model_assets.py" line="148"/>
        <source>细节更完整</source>
        <translation>More complete details</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="97"/>
        <location filename="../app/core/model_assets.py" line="152"/>
        <source>最精细</source>
        <translation>Most refined</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="98"/>
        <source>最精细, 显存占用很大</source>
        <translation>Most refined, uses much more VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="136"/>
        <source>结构与 medium 相同</source>
        <translation>Same architecture as medium</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="294"/>
        <source>文件不存在: {}</source>
        <translation>File not found: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="297"/>
        <source>只支持 {} 格式</source>
        <translation>Only {} files are supported</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="302"/>
        <source>读不到文件大小: {}</source>
        <translation>Cannot read file size: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="304"/>
        <source>文件只有 {}, 不像完整的权重</source>
        <translation>The file is only {}, too small to be a complete weight file</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="315"/>
        <source>这看着是 Transformer 权重, 当前档位是 CNN(YOLO)</source>
        <translation>This looks like a Transformer weight, but the selected slot is CNN (YOLO)</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="319"/>
        <source>这看着是 CNN(YOLO) 权重, 当前档位是 Transformer</source>
        <translation>This looks like a CNN (YOLO) weight, but the selected slot is Transformer</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="339"/>
        <source>权重目录不可写: {}</source>
        <translation>Weights directory is not writable: {}</translation>
    </message>
</context>
<context>
    <name>ModelDialog</name>
    <message>
        <location filename="../ui/model.ui" line="14"/>
        <location filename="../app/widgets/model_dialog.py" line="169"/>
        <source>模型管理</source>
        <translation>Model Manager</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="28"/>
        <source>搜索项目 / 数据集 / 标签</source>
        <translation>Search project / dataset / label</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="39"/>
        <source>全部任务</source>
        <translation>All tasks</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="44"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="49"/>
        <source>分割</source>
        <translation>Segmentation</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="54"/>
        <source>分类</source>
        <translation>Classification</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="66"/>
        <source>全部状态</source>
        <translation>All statuses</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="71"/>
        <source>已完成</source>
        <translation>Finished</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="76"/>
        <source>训练中</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="81"/>
        <source>失败</source>
        <translation>Failed</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="86"/>
        <source>已停止</source>
        <translation>Stopped</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="94"/>
        <source>仅看每个数据集最佳</source>
        <translation>Best per dataset only</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="114"/>
        <source>共 0 条</source>
        <translation>0 records</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="135"/>
        <location filename="../app/widgets/model_dialog.py" line="606"/>
        <source>任务</source>
        <translation>Task</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="140"/>
        <source>数据集 / 标签</source>
        <translation>Dataset / Labels</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="145"/>
        <location filename="../app/widgets/model_dialog.py" line="610"/>
        <source>精度</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="150"/>
        <location filename="../app/widgets/model_dialog.py" line="621"/>
        <source>训练时间</source>
        <translation>Trained at</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="155"/>
        <location filename="../app/widgets/model_dialog.py" line="623"/>
        <source>耗时</source>
        <translation>Duration</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="160"/>
        <location filename="../app/widgets/model_dialog.py" line="613"/>
        <source>图像尺寸</source>
        <translation>Image Size</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="165"/>
        <source>操作</source>
        <translation>Actions</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="184"/>
        <source>模型详情</source>
        <translation>Model details</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="191"/>
        <location filename="../app/widgets/model_dialog.py" line="589"/>
        <source>选中一行查看详情</source>
        <translation>Select a row to see details</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="220"/>
        <source>查看完整指标</source>
        <translation>View full metrics</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="227"/>
        <location filename="../app/widgets/model_dialog.py" line="733"/>
        <source>对比多次训练</source>
        <translation>Compare Runs</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="234"/>
        <source>按此配置重训</source>
        <translation>Retrain with this config</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="241"/>
        <source>打开模型目录</source>
        <translation>Open model directory</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="281"/>
        <source>上一页</source>
        <translation>Prev</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="288"/>
        <source>1/1</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="295"/>
        <source>下一页</source>
        <translation>Next</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="415"/>
        <source>共 {} 条</source>
        <translation>{} records</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="466"/>
        <source> 等 {} 类</source>
        <translation> and {} more classes</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="481"/>
        <source>测试</source>
        <translation>Test</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="486"/>
        <source>导出</source>
        <translation>Export</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="491"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="603"/>
        <source>{} × {} 累积</source>
        <translation>{} × {} accumulated</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="604"/>
        <source>状态</source>
        <translation>Status</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="611"/>
        <source>训练集</source>
        <translation>Train Set</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="612"/>
        <source>验证集</source>
        <translation>Val Set</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="614"/>
        <source>轮数 / 早停</source>
        <translation>Epochs / Early stop</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="616"/>
        <source>批大小</source>
        <translation>Batch size</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="617"/>
        <source>学习率</source>
        <translation>Learning rate</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="618"/>
        <source>优化器</source>
        <translation>Optimizer</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="619"/>
        <source>设备</source>
        <translation>Device</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="620"/>
        <source>标签</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="624"/>
        <source>模型路径</source>
        <translation>Model path</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="640"/>
        <source>失败原因</source>
        <translation>Failure reason</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="656"/>
        <source>暂无曲线</source>
        <translation>No curve</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="680"/>
        <source>{}  最佳 {:.3f}</source>
        <translation>{}  best {:.3f}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="688"/>
        <location filename="../app/widgets/model_dialog.py" line="699"/>
        <source>打开目录</source>
        <translation>Open directory</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="689"/>
        <source>模型目录不存在:
{}</source>
        <translation>Model directory does not exist:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="717"/>
        <source>[model_dialog] 打开指标失败: {}
{}</source>
        <translation>[model_dialog] Failed to open metrics: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="719"/>
        <source>查看指标失败</source>
        <translation>Failed to open metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="734"/>
        <source>当前没有可对比的训练记录</source>
        <translation>No training runs available to compare</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="741"/>
        <source>[model_dialog] 打开对比失败: {}
{}</source>
        <translation>[model_dialog] Failed to open comparison: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="743"/>
        <source>打开对比失败</source>
        <translation>Failed to open comparison</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="750"/>
        <source>删除模型记录</source>
        <translation>Delete Model Record</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="751"/>
        <source>确定删除该条模型记录?
项目={}
数据集={}
开始时间={}
</source>
        <translation>Delete this model record?
Project={}
Dataset={}
Start time={}
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="755"/>
        <source>删除模型记录: 项目={} 数据集={} 任务={} 开始时间={}</source>
        <translation>Delete model record: project={} dataset={} task={} start time={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="769"/>
        <source>删除模型记录失败: {} | {}</source>
        <translation>Failed to delete model record: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="770"/>
        <source>[model_dialog] 删除失败: {}
{}</source>
        <translation>[model_dialog] Delete failed: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="779"/>
        <source>[model_dialog] 打开训练失败: {}
{}</source>
        <translation>[model_dialog] Failed to open training: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="780"/>
        <source>打开训练失败</source>
        <translation>Failed to open training</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="805"/>
        <source>[model_dialog] 打开测试失败: {}
{}</source>
        <translation>[model_dialog] Failed to open testing: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="807"/>
        <source>打开测试失败</source>
        <translation>Failed to open testing</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="825"/>
        <location filename="../app/widgets/model_dialog.py" line="843"/>
        <location filename="../app/widgets/model_dialog.py" line="859"/>
        <location filename="../app/widgets/model_dialog.py" line="1151"/>
        <location filename="../app/widgets/model_dialog.py" line="1161"/>
        <source>导出模型</source>
        <translation>Export Model</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="826"/>
        <source>模型文件不存在:
{}</source>
        <translation>Model file does not exist:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="827"/>
        <source>导出模型失败: 模型文件不存在 {}</source>
        <translation>Export model failed: model file not found {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="829"/>
        <source>选择导出目录</source>
        <translation>Select Export Directory</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="844"/>
        <source>创建目录失败: {}</source>
        <translation>Failed to create directory: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="845"/>
        <source>导出模型失败: 创建目录失败 {} | {}</source>
        <translation>Export model failed: cannot create directory {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="855"/>
        <source>开始导出模型: 项目={} 任务={} 架构={} 尺寸={} | {}</source>
        <translation>Export model start: project={} task={} arch={} size={} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="856"/>
        <location filename="../app/widgets/model_dialog.py" line="1010"/>
        <source>未知</source>
        <translation>Unknown</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="860"/>
        <source>正在导出 ONNX...</source>
        <translation>Exporting ONNX...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="881"/>
        <source>正在导出模型包...</source>
        <translation>Exporting model package...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="892"/>
        <source>导出模型包完成: 包含 {}</source>
        <translation>Model package exported, contains: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="899"/>
        <source>ONNX 导出完成: {} ({:.1f} MB)</source>
        <translation>ONNX export done: {} ({:.1f} MB)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="956"/>
        <source>读取词表失败: {}</source>
        <translation>Failed to read vocabulary: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="967"/>
        <source>生成 vocab.txt 失败: {}</source>
        <translation>Failed to generate vocab.txt: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="983"/>
        <source>生成 label_map.json 失败: {}</source>
        <translation>Failed to write label_map.json: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="989"/>
        <source>导出模型报告跳过: 分类任务不出评估报告</source>
        <translation>Model report export skipped: classification tasks have no evaluation report</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="990"/>
        <source>分类任务不生成评估报告</source>
        <translation>Classification tasks do not produce an evaluation report</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="994"/>
        <source>导出模型报告跳过: 字符识别不出评估报告</source>
        <translation>Model report skipped: text recognition produces no evaluation report</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="995"/>
        <source>字符识别不生成评估报告</source>
        <translation>Text recognition does not produce an evaluation report</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="999"/>
        <source>导出模型报告跳过: 未找到验证集</source>
        <translation>Model report export skipped: no val set found</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1000"/>
        <source>未找到验证集, 已跳过评估报告</source>
        <translation>No validation set found; evaluation report skipped</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1002"/>
        <location filename="../app/widgets/model_dialog.py" line="1084"/>
        <source>正在生成模型报告...</source>
        <translation>Generating model report...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1006"/>
        <source>正在生成模型报告 {}/{}</source>
        <translation>Generating model report {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1009"/>
        <source>导出模型评估失败: {}</source>
        <translation>Model export evaluation failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1012"/>
        <source>评估失败, 已跳过报告: {}</source>
        <translation>Evaluation failed; report skipped: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1103"/>
        <source>导出模型报告跳过: 验证集没有标注</source>
        <translation>Model report export skipped: the val set has no labels</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1104"/>
        <source>验证集没有标注, 已跳过评估报告</source>
        <translation>The val set has no labels; the evaluation report was skipped.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1110"/>
        <source>[export] 生成评估报告失败:
{}</source>
        <translation>[export] Failed to generate the evaluation report:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1107"/>
        <source>生成评估报告失败: {}</source>
        <translation>Failed to generate the evaluation report: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="941"/>
        <source>读取类别表失败: {}</source>
        <translation>Failed to read class list: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="942"/>
        <source>[export] 读取类别表失败: {}</source>
        <translation>[export] Failed to read class list: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1099"/>
        <source>导出模型报告完成: {}</source>
        <translation>Model report export done: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1111"/>
        <source>评估完成, 但报告生成失败</source>
        <translation>Evaluation finished, but the report could not be generated</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1145"/>
        <source>导出模型完成: {} | 包含: {}</source>
        <translation>Model export done: {} | contains: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1147"/>
        <source>已导出到:
{}

包含: {}</source>
        <translation>Exported to:
{}

Contains: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1109"/>
        <location filename="../app/widgets/model_dialog.py" line="1158"/>
        <source>未知错误</source>
        <translation>Unknown error</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1162"/>
        <source>模型导出失败, 详情见日志</source>
        <translation>Model export failed, see the log for details</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1157"/>
        <source>导出模型失败: {}</source>
        <translation>Export model failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1159"/>
        <source>[export] ONNX 导出失败: {}</source>
        <translation>[export] ONNX export failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1176"/>
        <source>复制导出示例失败: {}</source>
        <translation>Failed to copy the export sample: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1177"/>
        <source>[export] 复制示例失败: {}</source>
        <translation>[export] Failed to copy the sample: {}</translation>
    </message>
</context>
<context>
    <name>ModelDownloader</name>
    <message>
        <location filename="../app/core/model_download.py" line="92"/>
        <source>权重目录不可写入, 请点&quot;更改&quot;换一个目录</source>
        <translation>Weights directory is not writable; click &quot;Change&quot; to pick another one</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="101"/>
        <source>权重文件大小不符, 丢弃重下: {}</source>
        <translation>Weight file size mismatch; discarding and re-downloading: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="111"/>
        <source>开始下载权重 {} ({}, 已下载 {})</source>
        <translation>Start downloading weights {} ({}, {} downloaded)</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="118"/>
        <source>下载权重失败 {}: {}</source>
        <translation>Failed to download weights {}: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="121"/>
        <source>无法连接下载服务器, 请检查网络后重试</source>
        <translation>Cannot reach the download server; check your network and retry</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="129"/>
        <source>下载中断, 已保留进度, 可再次点击续传</source>
        <translation>Download interrupted; progress kept, click again to resume</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="134"/>
        <source>下载不完整, 已保留进度, 可再次点击续传</source>
        <translation>Download incomplete; progress kept, click again to resume</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="141"/>
        <source>权重校验不通过 {}: 期望 {} 实际 {}</source>
        <translation>Weight verification failed {}: expected {} got {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="146"/>
        <source>文件校验未通过, 损坏文件已删除, 请重试</source>
        <translation>File verification failed; the corrupted file was deleted, please retry</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="152"/>
        <source>写入权重目录失败, 请检查磁盘空间</source>
        <translation>Failed to write to the weights directory; check disk space</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="155"/>
        <source>权重就绪: {}</source>
        <translation>Weights ready: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="176"/>
        <source>下载已取消, 已下载部分保留以便续传: {}</source>
        <translation>Download cancelled; the downloaded part is kept for resuming: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="196"/>
        <source>权重下载异常 {}: {!r}</source>
        <translation>Weights download error {}: {!r}</translation>
    </message>
</context>
<context>
    <name>ModelManagerDialog</name>
    <message>
        <location filename="../ui/model_manager.ui" line="14"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="411"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="415"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="420"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="455"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="459"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="510"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="517"/>
        <source>模型权重</source>
        <translation>Model Weights</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="63"/>
        <source>目标检测 · Transformer</source>
        <translation>Object Detection · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="97"/>
        <source>目标检测 · CNN</source>
        <translation>Object Detection · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="131"/>
        <source>图像分割 · Transformer</source>
        <translation>Image Segmentation · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="165"/>
        <source>图像分割 · CNN</source>
        <translation>Image Segmentation · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="221"/>
        <source>下载目录</source>
        <translation>Download folder</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="238"/>
        <source>更改</source>
        <translation>Change</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="265"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="293"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="498"/>
        <source>开始下载</source>
        <translation>Start Download</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="275"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="280"/>
        <source>关闭</source>
        <translation>Close</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="58"/>
        <source>还剩 {}s</source>
        <translation>{}s left</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="59"/>
        <source>还剩 {}m{}s</source>
        <translation>{}m{}s left</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="387"/>
        <source>选择权重目录</source>
        <translation>Select Weights Directory</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="405"/>
        <source>选择预训练权重</source>
        <translation>Select Pretrained Weights</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="406"/>
        <source>权重文件 (*.pt *.pth *.ckpt)</source>
        <translation>Weight files (*.pt *.pth *.ckpt)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="416"/>
        <source>仍要用这个文件吗?</source>
        <translation>Use this file anyway?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="444"/>
        <source>权重目录不可写入 {}: {!r}</source>
        <translation>Weights directory is not writable {}: {!r}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="455"/>
        <source>勾选的模型都已就绪, 不需要下载.</source>
        <translation>All selected models are ready; nothing to download.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="460"/>
        <source>当前目录不可写入, 请点&quot;更改&quot;换一个目录:
{}</source>
        <translation>The current directory is not writable. Click &quot;Change&quot; to pick another:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="293"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="465"/>
        <source>下载中...</source>
        <translation>Downloading...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="511"/>
        <source>以下权重没能下载完成:
</source>
        <translation>These weights could not be downloaded:
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="518"/>
        <source>下载还在进行, 现在关闭会中断下载(已下载部分保留, 下次可续传).
确定关闭?</source>
        <translation>A download is still running. Closing now interrupts it (the parts already downloaded are kept and will resume next time).
Close anyway?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="550"/>
        <source>去下载</source>
        <translation>Download</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="559"/>
        <source>该架构的权重必须先下载好才能开始训练, 也可以在权重管理里指定本地的权重文件.</source>
        <translation>Weights for this architecture must be downloaded before training starts. You can also select a local weight file in Model Weights.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="553"/>
        <source>本次训练选用 {} {}模型, 需要先下载 {}.</source>
        <translation>This training uses the {} {} model and needs {} downloaded first.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="552"/>
        <source>缺少模型权重</source>
        <translation>Missing Model Weights</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="365"/>
        <source>待下载 {}</source>
        <translation>To download: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="367"/>
        <source>无需下载</source>
        <translation>Nothing to download</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="369"/>
        <source>本地 {} 项</source>
        <translation>Local: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="551"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
</context>
<context>
    <name>MultiCombo</name>
    <message>
        <location filename="../app/widgets/multi_combo.py" line="350"/>
        <source>请选择数据集</source>
        <translation>Select datasets</translation>
    </message>
</context>
<context>
    <name>NameInputDialog</name>
    <message>
        <location filename="../ui/input_name.ui" line="14"/>
        <location filename="../ui/input_name.ui" line="40"/>
        <location filename="../app/widgets/name_input_dialog.py" line="13"/>
        <source>输入名称</source>
        <translation>Enter Name</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="65"/>
        <location filename="../app/widgets/name_input_dialog.py" line="14"/>
        <source>请输入名称</source>
        <translation>Enter a name</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="100"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="113"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
</context>
<context>
    <name>NameRules</name>
    <message>
        <location filename="../app/core/name_rules.py" line="25"/>
        <source>名称不能为空</source>
        <translation>Name cannot be empty</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="27"/>
        <source>名称过长, 最多 {} 个字符</source>
        <translation>Name is too long, at most {} characters</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="41"/>
        <source>名称不能包含「{}」等字符</source>
        <translation>Name cannot contain characters such as {}</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="54"/>
        <source>「{}」是系统保留名称, 请换一个</source>
        <translation>&quot;{}&quot; is a reserved name, please use another one</translation>
    </message>
</context>
<context>
    <name>OcrTestRunner</name>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="46"/>
        <source>缺少测试依赖: {}</source>
        <translation>Missing test dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="198"/>
        <source>识别失败: {}</source>
        <translation>Recognition failed: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="285"/>
        <source>明细写入失败: {}</source>
        <translation>Failed to write details: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="293"/>
        <source>未知的字符检测架构: {}</source>
        <translation>Unknown text detection architecture: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="307"/>
        <source>已加载配对识别模型: {}</source>
        <translation>Paired recognition model loaded: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="311"/>
        <source>识别模型不可用, 输出的标注只有框没有文字</source>
        <translation>Recognition model unavailable; written annotations have boxes but no text</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="317"/>
        <location filename="../app/train/ocr_test_runner.py" line="435"/>
        <source>没有可用的图像, 请检查数据集</source>
        <translation>No usable images; please check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="318"/>
        <source>加载字符检测模型: {}</source>
        <translation>Loading text detection model: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="320"/>
        <location filename="../app/train/ocr_test_runner.py" line="439"/>
        <source>测试图片 {} 张</source>
        <translation>{} test images</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="353"/>
        <source>预测失败 {}: {}</source>
        <translation>Prediction failed {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="383"/>
        <source>输出标注失败 {}: {}</source>
        <translation>Failed to write labels {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="411"/>
        <source>已写出 {} 张图的文本标注(图像同目录)</source>
        <translation>Wrote text annotations for {} images (next to each image)</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="422"/>
        <source>未知的字符识别架构: {}</source>
        <translation>Unknown text recognition architecture: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="426"/>
        <source>该模型没有词表, 无法识别</source>
        <translation>This model has no vocabulary; cannot recognize</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="436"/>
        <source>加载字符识别模型: {} 词表 {} 个字符</source>
        <translation>Loading text recognition model: {} vocabulary {} characters</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="467"/>
        <source>识别失败 {}: {}</source>
        <translation>Recognition failed {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="474"/>
        <source>没有取到任何字条: 该数据集没有文本标注, 识别段只能拿标注框裁图来测</source>
        <translation>No text crops obtained: this dataset has no text annotations, and the recognition stage can only be tested by cropping with annotated boxes</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="480"/>
        <source>WARN {} 张图没有文本标注, 已跳过</source>
        <translation>WARN {} images have no text annotations, skipped</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="483"/>
        <source>字条 {} 条, CER={:.4f}, 全对 {} 条</source>
        <translation>{} crops, CER={:.4f}, {} fully correct</translation>
    </message>
</context>
<context>
    <name>OcrTrainRunner</name>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="43"/>
        <source>缺少训练依赖: {}</source>
        <translation>Missing training dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="116"/>
        <source>检测模型 {} 权重来源: {}</source>
        <translation>Detection model {} weights from: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="120"/>
        <source>检测模型 {} 构建失败</source>
        <translation>Failed to build detection model {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="136"/>
        <source>识别模型 {} 权重来源: {}</source>
        <translation>Recognition model {} weights from: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="140"/>
        <source>识别模型 {} 构建失败</source>
        <translation>Failed to build recognition model {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="172"/>
        <source>标注里没有任何文字, 无法训练字符识别</source>
        <translation>No text in the annotations; cannot train text recognition</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="180"/>
        <source>标注最长 {} 字, 超过识别段能输出的 {} 步, 请加大输入宽度</source>
        <translation>Longest label has {} chars, more than the {} steps the recognition stage can output; widen the input width</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="200"/>
        <source>词表 {} 个字符</source>
        <translation>Vocabulary: {} characters</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="213"/>
        <source>字符{}训练: model={} device={} epochs={} batch={} lr={}</source>
        <translation>Text {} training: model={} device={} epochs={} batch={} lr={}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="216"/>
        <source>识别</source>
        <translation>recognition</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="217"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="220"/>
        <source>训练集没有可用的文本标注</source>
        <translation>No usable text annotations in the training set</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="223"/>
        <source>验证集没有可用的文本标注</source>
        <translation>No usable text annotations in the validation set</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="225"/>
        <source>数据集: train={} val={}</source>
        <translation>Dataset: train={} val={}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="312"/>
        <source>早停触发: 连续 {} 个 epoch 无提升</source>
        <translation>Early stopping: no improvement for {} consecutive epochs</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="341"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Output directory of this run (timestamp): {}</translation>
    </message>
</context>
<context>
    <name>OnnxExport</name>
    <message>
        <location filename="../app/train/onnx_export.py" line="112"/>
        <source>该识别模型没有词表, 无法导出</source>
        <translation>This recognition model has no vocabulary; cannot export</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="121"/>
        <source>未知的字符模型架构: {}</source>
        <translation>Unknown text model architecture: {}</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="138"/>
        <source>识别</source>
        <translation>recognition</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="139"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="157"/>
        <source>异常检测不导出 ONNX, 请用模型管理的「导出」生成模型包</source>
        <translation>Anomaly detection does not export ONNX. Use Export in model management to build a model package</translation>
    </message>
</context>
<context>
    <name>ProjectMixin</name>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="32"/>
        <source>输入名称</source>
        <translation>Enter Name</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="33"/>
        <source>项目名称</source>
        <translation>Project name</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="37"/>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <source>创建项目</source>
        <translation>Create Project</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <location filename="../app/mixins/project_mixin.py" line="53"/>
        <source>项目名称已存在!</source>
        <translation>A project with this name already exists!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="44"/>
        <source>创建项目: {}</source>
        <translation>Create project: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="49"/>
        <location filename="../app/mixins/project_mixin.py" line="53"/>
        <location filename="../app/mixins/project_mixin.py" line="107"/>
        <source>修改名称</source>
        <translation>Rename</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="56"/>
        <source>重命名项目: {} → {}</source>
        <translation>Rename project: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="61"/>
        <location filename="../app/mixins/project_mixin.py" line="108"/>
        <source>删除项目</source>
        <translation>Delete Project</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="62"/>
        <source>确定删除项目&quot;{}&quot;吗?
</source>
        <translation>Delete project &quot;{}&quot;?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="63"/>
        <source>删除项目: {}</source>
        <translation>Delete project: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="104"/>
        <location filename="../app/mixins/project_mixin.py" line="148"/>
        <location filename="../app/mixins/project_mixin.py" line="157"/>
        <source>添加数据集</source>
        <translation>Add Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="106"/>
        <source>导出项目</source>
        <translation>Export Project</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="123"/>
        <source>导入</source>
        <translation>Import</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="124"/>
        <source>导出</source>
        <translation>Export</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="125"/>
        <source>重载</source>
        <translation>Reload</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="126"/>
        <source>移动</source>
        <translation>Move</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="127"/>
        <source>修改</source>
        <translation>Rename</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="128"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="149"/>
        <source>数据集名称</source>
        <translation>Dataset name</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="157"/>
        <location filename="../app/mixins/project_mixin.py" line="168"/>
        <source>该项目下已存在同名数据集!</source>
        <translation>A dataset with this name already exists in this project!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="159"/>
        <source>创建数据集: {}/{}</source>
        <translation>Create dataset: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="164"/>
        <location filename="../app/mixins/project_mixin.py" line="168"/>
        <source>修改数据集</source>
        <translation>Rename Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="170"/>
        <source>重命名数据集: {} → {}</source>
        <translation>Rename dataset: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="175"/>
        <source>删除数据集</source>
        <translation>Delete Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="176"/>
        <source>确定删除数据集&quot;{}&quot;吗?
</source>
        <translation>Delete dataset &quot;{}&quot;?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="180"/>
        <source>删除数据集: {}/{}</source>
        <translation>Delete dataset: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="200"/>
        <location filename="../app/mixins/project_mixin.py" line="213"/>
        <location filename="../app/mixins/project_mixin.py" line="230"/>
        <source>移动数据集</source>
        <translation>Move Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="201"/>
        <source>是否将&quot;{}&quot;的数据从
{} / {} 移动到 {} / {}?
移动后源数据集将清空.</source>
        <translation>Move the data of &quot;{}&quot; from
{} / {} to {} / {}?
The source dataset will be emptied.</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="210"/>
        <source>移动失败</source>
        <translation>Move Failed</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="214"/>
        <source>已从 {} / {} 移动到 {} / {}</source>
        <translation>Moved from {} / {} to {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="231"/>
        <source>没有可移动到的目标数据集(本项目之外无数据集)</source>
        <translation>No target dataset available (there are no datasets outside this project)</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="235"/>
        <source>选择目标数据集</source>
        <translation>Select Target Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="239"/>
        <source>选择要将数据移动到的目标数据集:</source>
        <translation>Select the target dataset to move the data into:</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="324"/>
        <source>{}: {}个</source>
        <translation>{}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="326"/>
        <source>数据集移动: {}/{} → {}/{} | 移动图像 {} 张 | 目标标签统计({}类): {}</source>
        <translation>Dataset move: {}/{} → {}/{} | {} images moved | target label stats ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="329"/>
        <source>(无)</source>
        <translation>(none)</translation>
    </message>
</context>
<context>
    <name>ProjectSidebar</name>
    <message>
        <location filename="../app/widgets/project_sidebar.py" line="424"/>
        <source>{} 个项目 · {} 个数据集</source>
        <translation>Projects {} · Datasets {}</translation>
    </message>
</context>
<context>
    <name>QueueMixin</name>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="97"/>
        <source>训练队列已启动</source>
        <translation>Training queue started</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="107"/>
        <source>[队列] 已停止</source>
        <translation>[队列] Stopped</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="195"/>
        <source>[队列] 所有任务已执行完毕</source>
        <translation>[队列] All tasks finished</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="203"/>
        <source>[队列] 跳过任务 {}: {}</source>
        <translation>[队列] Skipping task {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="204"/>
        <source>队列任务启动失败 {}: {}</source>
        <translation>Failed to start queue task {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="224"/>
        <source>[队列] 缺少权重 {}, 该项训练会失败</source>
        <translation>[队列] Missing weights {}; this training will fail</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="227"/>
        <source>[队列] 缺少权重 {}, 该项训练时会自行下载</source>
        <translation>[队列] Missing weights {}; this item will download them during training</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="240"/>
        <source>已有训练在进行中</source>
        <translation>A training job is already running</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="245"/>
        <source>[队列] 开始队列第 {}/{} 项: {}</source>
        <translation>[队列] Starting queue item {}/{}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="249"/>
        <source>队列启动任务: {} record={}</source>
        <translation>Queue starting task: {} record={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="287"/>
        <source>训练未完成, 详见日志</source>
        <translation>Training did not finish; see the log</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="321"/>
        <source>[队列] 显存等待超时, 仍继续启动下一个任务</source>
        <translation>[队列] VRAM wait timed out; starting the next task anyway</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="367"/>
        <source>队列 {}</source>
        <translation>Queue {}</translation>
    </message>
</context>
<context>
    <name>ResponsiveMixin</name>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="19"/>
        <location filename="../app/mixins/responsive_mixin.py" line="40"/>
        <source>更多</source>
        <translation>More</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="43"/>
        <location filename="../app/mixins/responsive_mixin.py" line="52"/>
        <source>界面字号</source>
        <translation>Interface font size</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="58"/>
        <source>标准</source>
        <translation>Standard</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="59"/>
        <source>大</source>
        <translation>Large</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="60"/>
        <source>超大</source>
        <translation>Extra large</translation>
    </message>
</context>
<context>
    <name>StatusText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="18"/>
        <source>等待中</source>
        <translation>Waiting</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="19"/>
        <location filename="../app/widgets/status_style.py" line="26"/>
        <source>训练中</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="20"/>
        <location filename="../app/widgets/status_style.py" line="27"/>
        <source>已完成</source>
        <translation>Finished</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="21"/>
        <location filename="../app/widgets/status_style.py" line="28"/>
        <source>失败</source>
        <translation>Failed</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="22"/>
        <location filename="../app/widgets/status_style.py" line="31"/>
        <source>已跳过</source>
        <translation>Skipped</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="23"/>
        <location filename="../app/widgets/status_style.py" line="29"/>
        <source>已停止</source>
        <translation>Stopped</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="24"/>
        <location filename="../app/widgets/status_style.py" line="32"/>
        <source>已中断</source>
        <translation>Interrupted</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="30"/>
        <source>失败/已停止</source>
        <translation>Failed/Stopped</translation>
    </message>
</context>
<context>
    <name>TaskText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="37"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="38"/>
        <source>分割</source>
        <translation>Segmentation</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="39"/>
        <source>分类</source>
        <translation>Classification</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="40"/>
        <source>异常检测</source>
        <translation>Anomaly Detection</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="41"/>
        <location filename="../app/widgets/status_style.py" line="42"/>
        <source>字符检测</source>
        <translation>Text Detection</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="43"/>
        <source>字符识别</source>
        <translation>Text Recognition</translation>
    </message>
</context>
<context>
    <name>TestDialog</name>
    <message>
        <location filename="../ui/test_dialog.ui" line="14"/>
        <location filename="../ui/test_dialog.ui" line="41"/>
        <source>模型测试</source>
        <translation>Model Testing</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="102"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="118"/>
        <source>best.pth</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="130"/>
        <source>mAP50 0.912 · 输入 640 · 规模 n · 训练 2026-09-01 14:22</source>
        <translation>mAP50 0.912 · Input 640 · Scale n · Trained 2026-09-01 14:22</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="151"/>
        <source>数据与设备</source>
        <translation>Data &amp; Device</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="193"/>
        <source>数据</source>
        <translation>Data</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="216"/>
        <source>设备</source>
        <translation>Device</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="246"/>
        <source>测试参数</source>
        <translation>Test Parameters</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="288"/>
        <source>置信度</source>
        <translation>Confidence</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="329"/>
        <source>低于该分数的预测直接丢弃</source>
        <translation>Predictions scoring below this value are discarded</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="345"/>
        <source>IoU 阈值</source>
        <translation>IoU threshold</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="386"/>
        <source>与标注框重合度达标才算正确检出</source>
        <translation>Overlap with the ground-truth box must reach this value to count as a correct detection</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="402"/>
        <source>输出标签文件</source>
        <translation>Write label files</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="434"/>
        <source>写在图像目录下, 可重载数据集查看检出效果</source>
        <translation>Written to the image directory; reload the dataset to review the results</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="486"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="496"/>
        <source>请选择数据集</source>
        <translation>Select datasets</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="544"/>
        <location filename="../app/widgets/test_dialog.py" line="116"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="551"/>
        <source>开始测试</source>
        <translation>Start Test</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="244"/>
        <source>未指定模型</source>
        <translation>No model selected</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="245"/>
        <source>请在模型列表中重新选择一行</source>
        <translation>Select a row in the model list again</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="261"/>
        <source>输入 {}</source>
        <translation>Input {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="263"/>
        <source>规模 {}</source>
        <translation>Scale {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="265"/>
        <source>训练 {}</source>
        <translation>Trained {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="267"/>
        <source>该记录未保存训练指标</source>
        <translation>This record has no saved training metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="270"/>
        <source> · 文件已不存在</source>
        <translation> · file no longer exists</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="296"/>
        <source>请先勾选要测试的数据集</source>
        <translation>Select the datasets to test first</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="308"/>
        <source>{} 个数据集 · {} 张图</source>
        <translation>{} datasets · {} images</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="310"/>
        <source>分类数据集, 统计每张图的判断正确率</source>
        <translation>Classification dataset; measures per-image accuracy</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="312"/>
        <source>已标注, 评估模式: 统计检出率 / 漏检 / 误检</source>
        <translation>Labeled: evaluation mode, measures recall / misses / false positives</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="314"/>
        <source>未标注, 推理模式: 只输出预测标签</source>
        <translation>Unlabeled: inference mode, only writes predicted labels</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="316"/>
        <source>部分已标注, 已标注与未标注的数据集不能一起测</source>
        <translation>Partially labeled; labeled and unlabeled datasets cannot be tested together</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="343"/>
        <source>为判定为不良品的图写 &lt;同名&gt;.json 到图像目录, 多边形标出异常区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Writes &lt;same-name&gt;.json next to the image for parts judged defective, with polygons marking the anomaly regions; the annotation tool can open them directly; any manual annotation already there is overwritten</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="347"/>
        <source>把异常区域写成 labelme json, 便于重载复核</source>
        <translation>Writes the anomaly regions as labelme json for easy reload and review</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="360"/>
        <source>字符识别只报告字条识别率, 不输出标注文件</source>
        <translation>Text recognition only reports crop accuracy; no annotation files are written</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="366"/>
        <location filename="../app/widgets/test_dialog.py" line="372"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 框出文本区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Writes &lt;same-name&gt;.json next to each image, boxing the text regions; can be opened directly in the annotation tool; existing manual annotations there will be overwritten</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="375"/>
        <source>把检测到的文本框写成 labelme json, 便于重载复核</source>
        <translation>Write detected text boxes to labelme json for review after reload</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="378"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Write &lt;same-name&gt;.json next to each image so the annotation tool can open it directly; existing manual labels there are overwritten</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="395"/>
        <location filename="../app/widgets/test_dialog.py" line="399"/>
        <location filename="../app/widgets/test_dialog.py" line="413"/>
        <location filename="../app/widgets/test_dialog.py" line="419"/>
        <location filename="../app/widgets/test_dialog.py" line="432"/>
        <location filename="../app/widgets/test_dialog.py" line="442"/>
        <location filename="../app/widgets/test_dialog.py" line="448"/>
        <location filename="../app/widgets/test_dialog.py" line="463"/>
        <location filename="../app/widgets/test_dialog.py" line="468"/>
        <source>测试</source>
        <translation>Test</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="395"/>
        <source>已有测试在进行中</source>
        <translation>A test is already running</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="399"/>
        <source>请至少选择一个数据集</source>
        <translation>Select at least one dataset</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="414"/>
        <source>置信度/iou阈值必须是数字</source>
        <translation>Confidence / IoU threshold must be a number</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="420"/>
        <source>模型文件不存在, 请重新选择</source>
        <translation>The model file does not exist; please select it again</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="433"/>
        <source>数据集 {}/{} 未导入图像</source>
        <translation>Dataset {}/{} has no images imported</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="443"/>
        <source>分类数据集与检测/分割数据集不能同时测试: {}/{}</source>
        <translation>Classification and detection/segmentation datasets cannot be tested together: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="449"/>
        <source>已标注与未标注的数据集不能同时测试: {}/{}</source>
        <translation>Labeled and unlabeled datasets cannot be tested together: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="464"/>
        <source>字符识别要拿标注框裁字条才能测, 请选择已标注的数据集</source>
        <translation>Text recognition needs annotated boxes to crop text; please select a labeled dataset</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="469"/>
        <source>图像尺寸过大,文字识别需要裁剪出文字区域的图像再做推理</source>
        <translation>The image is too large. Text recognition needs images cropped to the text area before it can run inference</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="495"/>
        <source>[test] 启动测试 worker: model={} 数据集={} 图像目录={} device={} cfg={}</source>
        <translation>[test] Starting test worker: model={} dataset={} image dir={} device={} cfg={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="500"/>
        <source>测试准备中...</source>
        <translation>Preparing test...</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="517"/>
        <location filename="../app/widgets/test_dialog.py" line="518"/>
        <source>测试即将开始</source>
        <translation>Test is about to start</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="564"/>
        <source>测试中 {}/{}</source>
        <translation>Testing {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="612"/>
        <source>[test-dialog] 测试完成, ok={}</source>
        <translation>[test-dialog] Test finished, ok={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="620"/>
        <location filename="../app/widgets/test_dialog.py" line="630"/>
        <source>测试结果</source>
        <translation>Test Results</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="621"/>
        <source>测试未正常完成</source>
        <translation>The test did not finish normally</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="631"/>
        <source>字条 {} 条 · CER {:.4f} · 全对 {} 条</source>
        <translation>{} crops · CER {:.4f} · {} fully correct</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="638"/>
        <source>[test-dialog] 测试失败: {}</source>
        <translation>[test-dialog] Test failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="645"/>
        <source>测试失败</source>
        <translation>Test Failed</translation>
    </message>
</context>
<context>
    <name>TestReport</name>
    <message>
        <location filename="../app/train/test_report.py" line="179"/>
        <source>漏 {}</source>
        <translation>Missed {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="181"/>
        <source>误 {}</source>
        <translation>False pos. {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="183"/>
        <source>认错 {}</source>
        <translation>Wrong class {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="194"/>
        <source>(图片无法打开)</source>
        <translation>(image cannot be opened)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="280"/>
        <source>类别认错: {} → {}</source>
        <translation>Wrong class: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="308"/>
        <source>本次验证集没有漏检, 也没有误检.</source>
        <translation>No missed or false detections on this val set.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="311"/>
        <source>明细抽样: 共 {} 张有问题(漏检 {} / 误检 {}), 本报告抽取 {} 张 - 每个类别每种错误最多 {} 张, 按错误数从多到少取</source>
        <translation>Detail sampling: {} problematic images in total (missed {} / false positive {}); this report takes {} - at most {} per error type per class, ordered by error count</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="316"/>
        <source>明细: 共 {} 张有问题(漏检 {} / 误检 {}), 已全部列出</source>
        <translation>Details: {} problematic images in total (missed {} / false positive {}), all listed</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="343"/>
        <source>漏检 GT: 有标注但模型没检出</source>
        <translation>Missed GT: labeled but not detected by the model</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="345"/>
        <source>误检预测: 模型检出但标注里没有</source>
        <translation>False positive: detected by the model but not in the labels</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="347"/>
        <source>正确检出(仅作位置参照)</source>
        <translation>Correct detections (for position reference only)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="349"/>
        <source>类别认错: 位置对但判错类别(GT → 预测)</source>
        <translation>Wrong class: correct position but wrong class (GT → prediction)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="352"/>
        <source>虚线轮廓: 分割 mask / 标注多边形(判定按外接框 IoU)</source>
        <translation>Dashed outline: segmentation mask / annotation polygon (matched by bounding-box IoU)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="450"/>
        <location filename="../app/train/test_report.py" line="1049"/>
        <source>模型评估报告</source>
        <translation>Model Evaluation Report</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="454"/>
        <source>当前训练模型</source>
        <translation>Current training model</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="458"/>
        <location filename="../app/train/test_report.py" line="464"/>
        <source>(未记录)</source>
        <translation>(not recorded)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="463"/>
        <source>数据集 </source>
        <translation>Dataset </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="466"/>
        <source>置信度 {}</source>
        <translation>Confidence {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="486"/>
        <source>测试张数</source>
        <translation>Images tested</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="487"/>
        <location filename="../app/train/test_report.py" line="489"/>
        <source>{} 张</source>
        <translation>{} images</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="488"/>
        <source>有问题的图片</source>
        <translation>Problematic images</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="491"/>
        <source>检出率 (Recall)</source>
        <translation>Recall</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="493"/>
        <source>准确率 (Precision)</source>
        <translation>Accuracy (Precision)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="495"/>
        <source>正确检出</source>
        <translation>Correct detections</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="496"/>
        <source>{} 个</source>
        <translation>{}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="497"/>
        <source>漏检 (该抓没抓)</source>
        <translation>Missed (should have caught it)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="498"/>
        <location filename="../app/train/test_report.py" line="501"/>
        <location filename="../app/train/test_report.py" line="506"/>
        <source>{} 个 / {} 张图</source>
        <translation>{} / {} images</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="500"/>
        <source>误检 (过杀)</source>
        <translation>False pos. (overkill)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="505"/>
        <source>类别认错 (位置对, 类别错)</source>
        <translation>Wrong class (right position, wrong class)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="508"/>
        <source>指标</source>
        <translation>Metric</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="509"/>
        <source>值</source>
        <translation>Value</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="528"/>
        <source>按类别</source>
        <translation>By class</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="531"/>
        <source>类别</source>
        <translation>Class</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="532"/>
        <source>标注</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="533"/>
        <source>正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="534"/>
        <source>漏检</source>
        <translation>Missed</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="535"/>
        <source>误检</source>
        <translation>False pos.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="536"/>
        <source>检出率</source>
        <translation>Recall</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="537"/>
        <source>准确率</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="564"/>
        <source>... 另有 {} 类未列出</source>
        <translation>... {} more classes not listed</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="586"/>
        <source>错误样本明细(仅列漏检 / 误检图片, 正确检出不列出)</source>
        <translation>Error sample details (only missed / false-positive images; correct detections are not listed)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="625"/>
        <source>本轮检出率 {:.0f}%, 准确率 {:.0f}%.</source>
        <translation>This run: recall {:.0f}%, accuracy {:.0f}%.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="628"/>
        <source>没有逐类别统计, 无法定位到具体标签,请先确认标签文件能正常读到.</source>
        <translation>No per-class stats, so the specific labels cannot be located. Check first that the label files can be read.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="652"/>
        <source>漏检分布在</source>
        <translation>Misses are spread across</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="653"/>
        <source>漏检集中在</source>
        <translation>Misses are concentrated in</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="656"/>
        <source>(共 {} 个), 优先补这几类的姿态, 光照样本,并复核标注是否有遗漏.</source>
        <translation>({} in total); add pose and lighting samples for these classes first, and double-check the labels for omissions.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="662"/>
        <source>误检分布在</source>
        <translation>False positives are spread across</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="663"/>
        <source>误检以</source>
        <translation>False positives are mainly</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="664"/>
        <source>({} 个),属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({}), i.e. overkill; add defect-free negative samples and clean up label noise.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="666"/>
        <source>({} 个)为主,属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({} of them), i.e. overkill; add defect-free negative samples and clean up label noise.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="675"/>
        <source>暂无</source>
        <translation>None</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="679"/>
        <source>此外 {} 处位置对但类别判错</source>
        <translation>In addition, {} boxes are correctly located but assigned the wrong class</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="681"/>
        <source>(报告紫框), 属分类能力不足而非定位问题,需补易混淆类别之间的区分性样本.</source>
        <translation>(purple boxes in the report); this is weak classification rather than a localization problem, so add discriminative samples between easily confused classes.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="686"/>
        <source>其中</source>
        <translation>Among them</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="688"/>
        <source>仅 {} 个标注, 样本不足是主要瓶颈, 建议补到 200 个以上.</source>
        <translation>Only {} labels; insufficient samples are the main bottleneck - aim for 200 or more.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="693"/>
        <source>各类样本量差距大(最多 {} / 最少 {}),训练时建议做类别均衡采样.</source>
        <translation>Sample counts vary widely across classes (max {} / min {}); use class-balanced sampling when training.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="698"/>
        <source>把本报告中的漏检, 误检图加入训练集复训,再用同参数复测对比.</source>
        <translation>Add the missed and false-positive images from this report to the train set, retrain, then re-test with the same parameters and compare.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="702"/>
        <source>本轮无漏检, 无误检, 建议用更严的阈值或更难的样本再压一轮, 确认稳定性.</source>
        <translation>No misses and no false positives this run; test again with a stricter threshold or harder samples to confirm stability.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="898"/>
        <source>改进建议</source>
        <translation>Suggestions for Improvement</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="903"/>
        <source>基于本次测试的指标与按类别表现</source>
        <translation>Based on this test&apos;s metrics and per-class performance</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="905"/>
        <source>(模型: {})</source>
        <translation>(model: {})</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="907"/>
        <source>, 建议如下:</source>
        <translation>, suggestions:</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="925"/>
        <source>标红的标签是需要重点关注的类别.</source>
        <translation>Labels in red are the classes that need the most attention.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="930"/>
        <location filename="../app/train/test_report.py" line="956"/>
        <source>第 {} 页</source>
        <translation>Page {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1020"/>
        <source>{}(抽取 {} / 共 {} 张)</source>
        <translation>{}(sampled {} / {} total)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1023"/>
        <source>{}(共 {} 张)</source>
        <translation>{}({} total)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1025"/>
        <source>漏检样本: 有标注但模型没检出</source>
        <translation>Missed samples: labeled but not detected by the model</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1028"/>
        <source>误检样本: 模型检出但标注里没有</source>
        <translation>False-positive samples: detected by the model but not in the labels</translation>
    </message>
</context>
<context>
    <name>TestResultDialog</name>
    <message>
        <location filename="../ui/test_result.ui" line="14"/>
        <source>测试结果分析</source>
        <translation>Test Result Analysis</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="83"/>
        <source>图像维度</source>
        <translation>By Image</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="93"/>
        <source>按「张」统计</source>
        <translation>Counted by image</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="150"/>
        <location filename="../ui/test_result.ui" line="206"/>
        <location filename="../ui/test_result.ui" line="262"/>
        <location filename="../ui/test_result.ui" line="318"/>
        <location filename="../ui/test_result.ui" line="442"/>
        <location filename="../ui/test_result.ui" line="498"/>
        <location filename="../ui/test_result.ui" line="554"/>
        <source>0</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="163"/>
        <location filename="../app/train/test_result_dialog.py" line="282"/>
        <location filename="../app/train/test_result_dialog.py" line="317"/>
        <source>测试张数</source>
        <translation>Images tested</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="219"/>
        <source>全对图像</source>
        <translation>All-correct images</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="275"/>
        <source>有漏检图像</source>
        <translation>Images with misses</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="331"/>
        <location filename="../app/train/test_result_dialog.py" line="251"/>
        <source>有误检图像</source>
        <translation>Images with false positives</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="375"/>
        <source>标签维度</source>
        <translation>By Label</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="385"/>
        <source>按「标注框」统计</source>
        <translation>Counted by box</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="455"/>
        <location filename="../ui/test_result.ui" line="664"/>
        <location filename="../app/train/test_result_dialog.py" line="259"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>正确检出</source>
        <translation>Correct detections</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="511"/>
        <location filename="../ui/test_result.ui" line="669"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>漏检</source>
        <translation>Missed</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="567"/>
        <location filename="../ui/test_result.ui" line="674"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>误检</source>
        <translation>False pos.</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="610"/>
        <source>0%</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="623"/>
        <location filename="../ui/test_result.ui" line="684"/>
        <location filename="../app/train/test_result_dialog.py" line="395"/>
        <source>准确率</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="654"/>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>类别</source>
        <translation>Class</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="659"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>标注数</source>
        <translation>Boxes</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="679"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>检出率</source>
        <translation>Recall</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="708"/>
        <source>每类抽取</source>
        <translation>Per class</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="715"/>
        <source>每个类别的每种错误（漏检 / 误检）最多列出几张图。
报告体积约 120 KB 一张，样本多时调小可以显著减小 PDF；选「全部」则每张有问题的图都列。</source>
        <translation>Maximum images listed per error type (missed / false positive) for each class.
The report is about 120 KB per image; lowering this shrinks the PDF noticeably when there are many samples. Choosing &quot;All&quot; lists every problematic image.</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="719"/>
        <source> 张</source>
        <translation> images</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="722"/>
        <source>全部</source>
        <translation>All</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="751"/>
        <location filename="../app/train/test_result_dialog.py" line="187"/>
        <source>导出 PDF 报告</source>
        <translation>Export PDF Report</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="758"/>
        <location filename="../app/train/test_result_dialog.py" line="92"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="152"/>
        <source>把漏检/误检的图逐张画框导出成 PDF</source>
        <translation>Export a PDF with boxes drawn on every missed / false-positive image</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="155"/>
        <source>异常检测的逐图结果已写成 CSV, 不支持导出画框 PDF</source>
        <translation>Per-image anomaly detection results were written to CSV; boxed PDF export is not supported</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="157"/>
        <source>本次测试没有逐图错误明细, 无法导出</source>
        <translation>This test has no per-image error details; cannot export</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="169"/>
        <source>保存 PDF 报告</source>
        <translation>Save PDF Report</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="170"/>
        <source>PDF 文件 (*.pdf)</source>
        <translation>PDF files (*.pdf)</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="176"/>
        <source>正在生成...</source>
        <translation>Generating...</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="194"/>
        <source>无需导出</source>
        <translation>Nothing to Export</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="195"/>
        <source>本次测试没有漏检也没有误检, 没有内容可写.</source>
        <translation>This test has neither misses nor false positives; nothing to write.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="198"/>
        <source>导出完成</source>
        <translation>Export Complete</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="199"/>
        <source>PDF 报告已保存到:
{}</source>
        <translation>PDF report saved to:
{}</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="203"/>
        <source>导出失败</source>
        <translation>Export Failed</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="238"/>
        <source>按&quot;张&quot;统计 · 检出 1 个即算检出</source>
        <translation>By image · one detected box counts as detected</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="240"/>
        <source> · 有标注 {} 张</source>
        <translation> · {} images with labels</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="244"/>
        <source>检出图像</source>
        <translation>Detected images</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="245"/>
        <location filename="../app/train/test_result_dialog.py" line="260"/>
        <source>检出率 </source>
        <translation>Recall </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="247"/>
        <source>未检出图像</source>
        <translation>Undetected images</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="248"/>
        <source>未检出率 </source>
        <translation>Miss rate </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="252"/>
        <source>误检率 </source>
        <translation>False positive rate </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="257"/>
        <source>按&quot;标注框&quot;统计 · 标注总数 {}</source>
        <translation>By box · {} boxes total</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="280"/>
        <source>按&quot;张&quot;统计 · 每张图判一个类别</source>
        <translation>By image · one class judged per image</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="285"/>
        <source>判断正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="287"/>
        <source>判断错误</source>
        <translation>Wrong</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="290"/>
        <location filename="../app/train/test_result_dialog.py" line="362"/>
        <source>精度</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="315"/>
        <source>按&quot;张&quot;统计 · 整图判良品/不良品</source>
        <translation>Counted per image · each image judged good or defective</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="329"/>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <source>检出异常</source>
        <translation>Detected anomalies</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <source>总图数</source>
        <translation>Total images</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="345"/>
        <source>异常</source>
        <translation>Anomaly</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <source>正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="362"/>
        <source>错误</source>
        <translation>Wrong</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="383"/>
        <source>模型里没有判定阈值, 只报告分数, 逐图分数见 CSV 明细.</source>
        <translation>The model has no decision threshold; only scores are reported. See the CSV for per-image scores.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="384"/>
        <source>判定阈值 {:.4f}. 本次 {} 张, 检出异常 {} 张.</source>
        <translation>Decision threshold {:.4f}. Tested {} images, {} detected as anomalous.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="297"/>
        <source>整体精度 {:.1f}%, &quot;{}&quot;类错误最多({} 张), 是拉低精度的主要原因.</source>
        <translation>Overall accuracy {:.1f}%. Class &quot;{}&quot; has the most errors ({} images) and is the main reason for the lower accuracy.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="422"/>
        <source>整体漏检偏多(漏检 {} 个, 多于误检 {} 个).&quot;{}&quot;类漏检最多({} 个), 是检出率低的主要原因.</source>
        <translation>Misses dominate overall ({} missed vs {} false positives). Class &quot;{}&quot; has the most misses ({}) and is the main reason for the low recall.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="428"/>
        <source>整体误检偏多(误检 {} 个, 多于漏检 {} 个).&quot;{}&quot;类误检最多({} 个), 是准确率低的主要原因.</source>
        <translation>False positives dominate overall ({} vs {} missed). Class &quot;{}&quot; has the most false positives ({}) and is the main reason for the low precision.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="432"/>
        <source>模型表现良好: 无漏检, 无误检.</source>
        <translation>The model performs well: no misses and no false positives.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="434"/>
        <source>另有 {} 处位置对但类别判错(报告里用紫框标出),属分类能力不足, 需补易混淆类别的区分性样本.</source>
        <translation>{} more boxes are correctly located but assigned the wrong class (marked with purple boxes in the report). This points to weak classification ability; add more discriminative samples for easily confused classes.</translation>
    </message>
</context>
<context>
    <name>TestRunner</name>
    <message>
        <location filename="../app/train/test_runner.py" line="278"/>
        <source>覆盖已有标注 {}</source>
        <translation>Overwrite existing labels {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="308"/>
        <source>明细初始化失败: {}</source>
        <translation>Failed to initialize details: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="317"/>
        <source>明细目录创建失败: {}</source>
        <translation>Failed to create the details directory: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="345"/>
        <source>明细写入失败: {}</source>
        <translation>Failed to write details: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="427"/>
        <source>当前安装缺少所需组件, 无法执行测试</source>
        <translation>This installation is missing required components; cannot run the test</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="429"/>
        <source>加载模型: {}</source>
        <translation>Loading model: {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_backend.py" line="36"/>
        <source>推理已优化: {}</source>
        <translation>Inference optimized: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="446"/>
        <source>测试图片 {} 张</source>
        <translation>{} test images</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="496"/>
        <source>预测失败 {}: {}</source>
        <translation>Prediction failed {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="510"/>
        <source>输出标注失败 {}: {}</source>
        <translation>Failed to write labels {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="565"/>
        <source>WARN 标签目录存在但所有 {} 张图都没读到 GT,请确认标签是 .txt (YOLO) 或 .json (labelme)</source>
        <translation>WARN Label directory exists but no GT was read for any of the {} images; make sure the labels are .txt (YOLO) or .json (labelme)</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="570"/>
        <source>WARN {} 张图缺标签文件</source>
        <translation>WARN {} images have no label file</translation>
    </message>
</context>
<context>
    <name>TestWorker</name>
    <message>
        <location filename="../app/train/test_worker.py" line="83"/>
        <source>run 开始</source>
        <translation>run start</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="97"/>
        <source>启动子进程: {} {}</source>
        <translation>Start subprocess: {} {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="109"/>
        <source>启动子进程失败: {}</source>
        <translation>Failed to start subprocess: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="116"/>
        <source>启动测试进程失败: {}</source>
        <translation>Failed to start the test process: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="118"/>
        <location filename="../app/train/test_worker.py" line="120"/>
        <source>子进程已启动 pid={}</source>
        <translation>Subprocess started pid={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="152"/>
        <source>进入轮询循环</source>
        <translation>Entering poll loop</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="162"/>
        <source>轮询中: 文件={}B 已读{}行 子进程={}</source>
        <translation>Polling: file={}B {} lines read subprocess={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="172"/>
        <source>轮询异常:
</source>
        <translation>Poll error:
</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="180"/>
        <source>轮询结束 rc={}</source>
        <translation>Poll loop finished rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="182"/>
        <source>子进程退出 rc={}</source>
        <translation>Subprocess exited rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="192"/>
        <source>测试未能完成, 详情见日志</source>
        <translation>The test could not be completed, see the log for details</translation>
    </message>
</context>
<context>
    <name>TrainDialog</name>
    <message>
        <location filename="../ui/train.ui" line="14"/>
        <location filename="../ui/train.ui" line="40"/>
        <location filename="../app/train/dialogs.py" line="517"/>
        <source>训练</source>
        <translation>Train</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="50"/>
        <location filename="../ui/train.ui" line="169"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="118"/>
        <source>模型与数据</source>
        <translation>Model &amp; Data</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="158"/>
        <source>任务类型</source>
        <translation>Task</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="174"/>
        <source>分割</source>
        <translation>Segmentation</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="179"/>
        <source>分类</source>
        <translation>Classification</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="184"/>
        <source>异常检测</source>
        <translation>Anomaly Detection</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="189"/>
        <source>字符检测</source>
        <translation>Text Detection</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="197"/>
        <source>型号</source>
        <translation>Model</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="210"/>
        <location filename="../app/train/dialogs.py" line="739"/>
        <source>训练集</source>
        <translation>Train Set</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="230"/>
        <source>验证集</source>
        <translation>Val Set</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="250"/>
        <source>设备</source>
        <translation>Device</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="263"/>
        <source>架构</source>
        <translation>Architecture</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="296"/>
        <source>训练超参</source>
        <translation>Hyperparameters</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="336"/>
        <location filename="../app/train/dialogs.py" line="613"/>
        <source>轮次</source>
        <translation>Epochs</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="349"/>
        <source>优化器</source>
        <translation>Optimizer</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="362"/>
        <location filename="../app/train/dialogs.py" line="616"/>
        <source>早停</source>
        <translation>Early Stop</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="399"/>
        <source>连续无提升则提前结束，0 为关闭</source>
        <translation>Stop early when no improvement; 0 disables</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="415"/>
        <location filename="../app/train/dialogs.py" line="619"/>
        <source>学习率</source>
        <translation>Learning rate</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="452"/>
        <source>初始学习率，训练中自动衰减</source>
        <translation>Initial LR, decayed while training</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="468"/>
        <location filename="../app/train/dialogs.py" line="611"/>
        <source>批次</source>
        <translation>Batch</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="481"/>
        <location filename="../app/train/dialogs.py" line="615"/>
        <source>图像尺寸</source>
        <translation>Image Size</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="512"/>
        <source>32 的倍数</source>
        <translation>multiple of 32</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="528"/>
        <location filename="../app/train/dialogs.py" line="612"/>
        <source>梯度累积</source>
        <translation>Grad Accum</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="565"/>
        <source>显存不足时调大，等效批次 × N</source>
        <translation>Raise when VRAM is tight; effective batch × N</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="581"/>
        <location filename="../app/train/dialogs.py" line="614"/>
        <source>线程数</source>
        <translation>Threads</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="642"/>
        <source>数据增强</source>
        <translation>Data Augmentation</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="723"/>
        <source>输出</source>
        <translation>Output</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="766"/>
        <source>输出路径</source>
        <translation>Output Path</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="781"/>
        <source>留空则自动按时间生成目录</source>
        <translation>Leave empty to auto-name a timestamped folder</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="794"/>
        <source>选择路径</source>
        <translation>Browse</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="839"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="855"/>
        <location filename="../app/train/dialogs.py" line="705"/>
        <source>请选择训练集与验证集</source>
        <translation>Select a train set and a val set</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="903"/>
        <location filename="../app/train/dialogs.py" line="628"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="916"/>
        <location filename="../app/train/dialogs.py" line="1364"/>
        <location filename="../app/train/dialogs.py" line="1373"/>
        <location filename="../app/train/dialogs.py" line="1384"/>
        <location filename="../app/train/dialogs.py" line="1403"/>
        <location filename="../app/train/dialogs.py" line="1414"/>
        <source>加入队列</source>
        <translation>Add to Queue</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="929"/>
        <location filename="../app/train/dialogs.py" line="1298"/>
        <location filename="../app/train/dialogs.py" line="1308"/>
        <location filename="../app/train/dialogs.py" line="1334"/>
        <source>开始训练</source>
        <translation>Start Training</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="41"/>
        <source>正在检测显卡...</source>
        <translation>Detecting GPUs...</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="84"/>
        <location filename="../app/train/dialogs.py" line="86"/>
        <source>0.5</source>
        <translation>0.5</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="90"/>
        <source>±20%</source>
        <translation>±20%</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="247"/>
        <source>数据集&quot;{}&quot;尚未导入图像或路径无效, 请先导入该数据集再训练</source>
        <translation>Dataset &quot;{}&quot; has no images imported or its path is invalid. Import it before training.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="257"/>
        <source>数据集&quot;{}&quot;尚未导入标签或路径无效, 请先导入该数据集再训练</source>
        <translation>Dataset &quot;{}&quot; has no labels imported or its path is invalid. Import it before training.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="286"/>
        <location filename="../app/train/dialogs.py" line="1374"/>
        <source>请先选择输出路径</source>
        <translation>Select an output path first</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="23"/>
        <source>数据集&quot;{}/{}&quot;不是分类数据集(标签格式={}), 无法训练{}</source>
        <translation>Dataset &quot;{}/{}&quot; is not a classification dataset (label format={}); cannot train {}</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="29"/>
        <source>未知</source>
        <translation>Unknown</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="25"/>
        <source>数据集&quot;{}/{}&quot;是分类数据集, 无法训练{}任务</source>
        <translation>Dataset &quot;{}/{}&quot; is a classification dataset; cannot train a {} task</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="313"/>
        <source>请至少选择一个训练集数据集</source>
        <translation>Select at least one train-set dataset</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="315"/>
        <source>请至少选择一个验证集数据集</source>
        <translation>Select at least one val-set dataset</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="355"/>
        <source>未选数据集</source>
        <translation>no dataset selected</translation>
    </message>
    <message>
        <location filename="../app/train/detect_common.py" line="12"/>
        <source>目标检测推荐图像尺寸: 640(可设为 32 的倍数如 640/672)</source>
        <translation>Recommended image size for detection: 640 (set it to a multiple of 32, e.g. 640/672)</translation>
    </message>
    <message>
        <location filename="../app/train/segment_common.py" line="16"/>
        <source>CNN 分割推荐尺寸: 640(需为 32 的倍数)</source>
        <translation>Recommended size for CNN segmentation: 640 (must be a multiple of 32)</translation>
    </message>
    <message>
        <location filename="../app/train/classify_common.py" line="27"/>
        <source>图像分类推荐尺寸: 224(小图用 224, 较大图可到 256)</source>
        <translation>Recommended size for classification: 224 (224 for small images, up to 256 for larger ones)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="699"/>
        <source>异常检测推荐尺寸: 256; 缺陷很小时调到 512 更稳, 显存和耗时随之上升</source>
        <translation>Recommended size for anomaly detection: 256; for tiny defects 512 is more reliable, at the cost of VRAM and time</translation>
    </message>
    <message>
        <location filename="../app/train/segment_common.py" line="17"/>
        <source>图像分割推荐尺寸: 648(需为 {} 的倍数)</source>
        <translation>Recommended size for segmentation: 648 (must be a multiple of {})</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="27"/>
        <source>数据集&quot;{}/{}&quot;没有文本标注, 无法训练{}</source>
        <translation>Dataset &quot;{}/{}&quot; has no text annotations; cannot train {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="490"/>
        <source>{} 的倍数</source>
        <translation>multiple of {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_common.py" line="31"/>
        <source>建议 224</source>
        <translation>224 suggested</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="704"/>
        <source>建议 256</source>
        <translation>256 recommended</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="715"/>
        <source>训练集 {} 个 · 验证集 {} 个 · 共 {} 张图</source>
        <translation>{} train · {} val · {} images total</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="718"/>
        <source>未选择验证集</source>
        <translation>no val set selected</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="720"/>
        <source>已标注, 可直接训练</source>
        <translation>labeled, ready to train</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="722"/>
        <source>有 {} 个数据集尚未标注</source>
        <translation>{} dataset(s) are not fully labeled</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="736"/>
        <source>请选择验证集</source>
        <translation>Select val datasets</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="821"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>A training job is already running; stop it first</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="77"/>
        <source>几何变换</source>
        <translation>Geometric</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="78"/>
        <source>标注框会跟着一起变换</source>
        <translation>Boxes transform with it</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="79"/>
        <source>像素变换</source>
        <translation>Pixel</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="80"/>
        <source>只改画面，标注框不动</source>
        <translation>Image only, boxes stay</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="83"/>
        <source>水平翻转</source>
        <translation>Horizontal flip</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="85"/>
        <source>垂直翻转</source>
        <translation>Vertical flip</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="87"/>
        <source>旋转</source>
        <translation>Rotation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="88"/>
        <source>±15°</source>
        <translation>±15°</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="89"/>
        <source>仿射</source>
        <translation>Affine</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="91"/>
        <source>马赛克</source>
        <translation>Mosaic</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="92"/>
        <source>4 图拼接</source>
        <translation>4 images</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="93"/>
        <source>亮度/对比度</source>
        <translation>Brightness/contrast</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="94"/>
        <source>±0.1</source>
        <translation>±0.1</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="95"/>
        <source>颜色抖动</source>
        <translation>Color jitter</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="96"/>
        <source>饱和/色相</source>
        <translation>saturation/hue</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="97"/>
        <source>高斯模糊</source>
        <translation>Gaussian blur</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="98"/>
        <source>核 3</source>
        <translation>kernel 3</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="99"/>
        <source>高斯噪声</source>
        <translation>Gaussian noise</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="100"/>
        <source>σ 0.05</source>
        <translation>σ 0.05</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="102"/>
        <source>已启用 {} 项</source>
        <translation>{} enabled</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="103"/>
        <source>该任务不支持配置数据增强</source>
        <translation>This task does not support configurable data augmentation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="105"/>
        <source>当前网络架构不支持该增强</source>
        <translation>The current network architecture does not support this augmentation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1351"/>
        <source>开始训练: 字符识别 | {}</source>
        <translation>Start training: text recognition | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1415"/>
        <source>字符识别已加入队列, 排在第 {} 个</source>
        <translation>Text recognition added to the queue, number {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="726"/>
        <source>异常检测算法自带学习率与优化器, 不需要设置</source>
        <translation>Anomaly detection algorithms bring their own learning rate and optimizer; nothing to set here</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="732"/>
        <source>建库型算法只提取特征建立记忆库, 没有训练轮次</source>
        <translation>Memory-bank algorithms only extract features to build the memory bank; there are no training epochs</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="673"/>
        <source>仅建库</source>
        <translation>Build only</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1234"/>
        <source>请至少选择一个数据集</source>
        <translation>Select at least one dataset</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1238"/>
        <location filename="../app/train/dialogs.py" line="1248"/>
        <source>&quot;{}&quot;不能为空</source>
        <translation>&quot;{}&quot; cannot be empty</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1243"/>
        <source>&quot;{}&quot;必须是整数(当前: {})</source>
        <translation>&quot;{}&quot; must be an integer (currently: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1253"/>
        <source>&quot;{}&quot;必须是数字(当前: {})</source>
        <translation>&quot;{}&quot; must be a number (currently: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1262"/>
        <source>图像尺寸需为 {} 的倍数(当前 {}), 可改为 {}</source>
        <translation>Image size must be a multiple of {} (currently {}); try {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1278"/>
        <source>选择输出目录</source>
        <translation>Select Output Directory</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1292"/>
        <source>当前安装缺少 CNN 架构所需的组件, 无法训练.
请重新安装软件后再试</source>
        <translation>This installation is missing the components required by the CNN architecture, so training cannot start.
Please reinstall the software and try again</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1299"/>
        <source>当前已有训练在进行中, 请先停止!</source>
        <translation>A training job is already running; stop it first!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1303"/>
        <source>参数校验未通过: {}</source>
        <translation>Parameter validation failed: {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1304"/>
        <location filename="../app/train/dialogs.py" line="1360"/>
        <source>参数校验</source>
        <translation>Parameter Validation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1324"/>
        <source>训练启动失败: {}
{}</source>
        <translation>Training failed to start: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1327"/>
        <source>训练启动失败</source>
        <translation>Training Failed to Start</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1335"/>
        <source>已有训练在进行中, 请先停止!</source>
        <translation>A training job is already running; stop it first!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1337"/>
        <source>开始训练: 任务类型={} 训练集={} 验证集={}</source>
        <translation>Training start: task={} train set={} val set={}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1389"/>
        <source>队列</source>
        <translation>Queue</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1390"/>
        <source>已更新该队列任务的参数</source>
        <translation>Queue task parameters updated</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1396"/>
        <source>加入队列失败</source>
        <translation>Failed to Add to Queue</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1399"/>
        <source>加入训练队列: {} | {}</source>
        <translation>Add to training queue: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1404"/>
        <source>已加入队列(第 {} 个), 可在首页&quot;队列&quot;中查看或启动.</source>
        <translation>Added to the queue (position {}). Review or start it from &quot;Queue&quot; on the home page.</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_common.py" line="70"/>
        <source>识别段输入固定 32x768(高x宽), 本项不用填</source>
        <translation>The recognition stage takes a fixed 32x768 input (height x width); this field is not used</translation>
    </message>
</context>
<context>
    <name>TrainMixin</name>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="47"/>
        <source>{} 训练中 0/{}</source>
        <translation>{} training 0/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="86"/>
        <source>[train] 训练线程已结束但未返回结果, 按失败收尾</source>
        <translation>[train] Training thread ended without returning a result; treating as failure</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="97"/>
        <source>仅停止当前</source>
        <translation>Stop Current Only</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="98"/>
        <source>停止队列</source>
        <translation>Stop Queue</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <location filename="../app/mixins/train_mixin.py" line="121"/>
        <source>停止训练</source>
        <translation>Stop Training</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <source>当前正在跑训练队列, 要停止到什么范围?</source>
        <translation>A training queue is running. How much should be stopped?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="102"/>
        <location filename="../app/mixins/train_mixin.py" line="103"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <source>确定要停止当前训练吗?</source>
        <translation>Stop the current training?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="117"/>
        <source>手动停止训练: {}</source>
        <translation>Training stopped manually: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="119"/>
        <source>[train] 训练进程 10 秒内未退出, 可能有子进程残留占用显存</source>
        <translation>[train] Training process did not exit within 10 s; child processes may still hold VRAM</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="122"/>
        <source>训练进程未能完全退出, 可能仍有子进程占用显存.
建议稍等片刻再启动下一个任务.</source>
        <translation>The training process did not exit completely; child processes may still hold VRAM.
Wait a moment before starting the next task.</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="134"/>
        <source>{} 训练中 {}/{}</source>
        <translation>{} training {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="147"/>
        <source>进度 | 当前最好 {}</source>
        <translation>Progress | {} (best so far)</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="211"/>
        <source>更新训练指标: record={} 已完成epoch={} {}={} 类别数={}</source>
        <translation>Update training metrics: record={} epochs done={} {}={} classes={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="310"/>
        <source>等待显存释放 · 下一项:{}</source>
        <translation>Waiting for VRAM release · next:{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="187"/>
        <source>训练失败(队列模式, 已跳过弹窗): {}</source>
        <translation>Training failed (queue mode, dialog skipped): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="189"/>
        <source>训练失败</source>
        <translation>Training Failed</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="190"/>
        <source>训练过程中发生错误, Err:

{}</source>
        <translation>An error occurred during training, Err:

{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="283"/>
        <source>已保存模型记录: {} | {}</source>
        <translation>Model record saved: {} | {}</translation>
    </message>
</context>
<context>
    <name>TrainQueueDialog</name>
    <message>
        <location filename="../ui/train_queue.ui" line="14"/>
        <location filename="../ui/train_queue.ui" line="40"/>
        <location filename="../app/widgets/queue_dialog.py" line="33"/>
        <source>训练队列</source>
        <translation>Training Queue</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="50"/>
        <location filename="../app/widgets/queue_dialog.py" line="123"/>
        <source>空闲</source>
        <translation>Idle</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="93"/>
        <source>#</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="98"/>
        <source>名称</source>
        <translation>Name</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="103"/>
        <source>任务</source>
        <translation>Task</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="108"/>
        <source>数据集</source>
        <translation>Dataset</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="113"/>
        <source>型号</source>
        <translation>Model</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="118"/>
        <source>轮次</source>
        <translation>Epochs</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="123"/>
        <source>状态</source>
        <translation>Status</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="152"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="168"/>
        <source>队列为空，可在训练界面点「加入队列」添加任务</source>
        <translation>The queue is empty. Click &quot;Add to Queue&quot; in the training dialog to add tasks.</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="199"/>
        <source>上移</source>
        <translation>Move Up</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="209"/>
        <source>下移</source>
        <translation>Move Down</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="219"/>
        <location filename="../app/widgets/queue_dialog.py" line="255"/>
        <source>移除</source>
        <translation>Remove</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="229"/>
        <source>清理已结束</source>
        <translation>Clear Finished</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="252"/>
        <source>编辑</source>
        <translation>Edit</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="259"/>
        <source>关闭</source>
        <translation>Close</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="272"/>
        <location filename="../app/widgets/queue_dialog.py" line="144"/>
        <source>开始队列</source>
        <translation>Start Queue</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="22"/>
        <source>队列为空, 可在训练界面点&quot;加入队列&quot;添加任务</source>
        <translation>The queue is empty. Click &quot;Add to Queue&quot; in the training dialog to add tasks.</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>运行中</source>
        <translation>Running</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>队列正在串行执行</source>
        <translation>The queue runs tasks one after another</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="115"/>
        <source>待启动</source>
        <translation>Pending</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="116"/>
        <source>有 {} 个任务等待启动</source>
        <translation>{} task(s) waiting to start</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>训练中</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>当前有训练在进行(非队列启动)</source>
        <translation>A training job is running (not started by the queue)</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="120"/>
        <source>已结束</source>
        <translation>Finished</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="121"/>
        <source>没有待执行的任务, 点&quot;重新开始队列&quot;可重跑</source>
        <translation>No pending tasks; click &quot;Restart Queue&quot; to run them again</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="127"/>
        <source>共 {} 个: 等待 {} · 完成 {} · 失败 {}</source>
        <translation>{} total: {} waiting · {} done · {} failed</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="130"/>
        <source>正在训练&quot;{}&quot; · {}</source>
        <translation>Training &quot;{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="133"/>
        <source>下一个: &quot;{}&quot; · {}</source>
        <translation>Next: &quot;{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="146"/>
        <location filename="../app/widgets/queue_dialog.py" line="183"/>
        <source>重新开始队列</source>
        <translation>Restart Queue</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="168"/>
        <location filename="../app/widgets/queue_dialog.py" line="190"/>
        <source>队列</source>
        <translation>Queue</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="169"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>A training job is already running; stop it first</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="178"/>
        <source>{} 个{}</source>
        <translation>{} {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="184"/>
        <source>队列中没有等待中的任务.

待重跑: {}

是否重新入队并开始训练?</source>
        <translation>There are no waiting tasks in the queue.

To re-run: {}

Re-enqueue them and start training?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="191"/>
        <source>队列启动失败, 请查看日志</source>
        <translation>Failed to start the queue; check the log</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="207"/>
        <location filename="../app/widgets/queue_dialog.py" line="211"/>
        <source>移除任务</source>
        <translation>Remove Task</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="208"/>
        <source>训练中的任务不能移除, 请先停止</source>
        <translation>A running task cannot be removed; stop it first</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="212"/>
        <source>确定从队列中移除&quot;{}&quot;吗?</source>
        <translation>Remove &quot;{}&quot; from the queue?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="219"/>
        <source>清理</source>
        <translation>Clear</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="220"/>
        <source>没有已结束的任务</source>
        <translation>No finished tasks</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="222"/>
        <source>[队列] 已清理 {} 个已结束任务</source>
        <translation>[队列] Cleared {} finished task(s)</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="229"/>
        <source>编辑任务</source>
        <translation>Edit Task</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="230"/>
        <source>训练中的任务不能编辑, 请先停止</source>
        <translation>A running task cannot be edited; stop it first</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="246"/>
        <source>重新入队</source>
        <translation>Re-enqueue</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="248"/>
        <location filename="../app/widgets/queue_dialog.py" line="269"/>
        <source>打开输出目录</source>
        <translation>Open Output Directory</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="250"/>
        <source>在模型界面查看</source>
        <translation>View in Model Manager</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="270"/>
        <source>目录不存在: {}</source>
        <translation>Directory does not exist: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="271"/>
        <source>未设置</source>
        <translation>Not set</translation>
    </message>
</context>
<context>
    <name>TrainRunner</name>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="114"/>
        <source>数据增强需要 kornia 或 albumentations, 当前环境两者都没有.
请把训练参数里的&quot;数据增强&quot;全部取消勾选, 或补装组件后重试</source>
        <translation>Data augmentation needs kornia or albumentations, but neither is installed.
Uncheck every item under &quot;Data augmentation&quot; in the training settings, or install one and retry</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="202"/>
        <location filename="../app/train/transformer_train_runner.py" line="131"/>
        <source>输出路径: {}</source>
        <translation>Output path: {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="203"/>
        <location filename="../app/train/transformer_train_runner.py" line="132"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Run output directory (timestamp): {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="134"/>
        <source>训练配置文件已保存 → {}</source>
        <translation>Training config saved → {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="156"/>
        <source>分割模型 resolution 已自动取整: {} → {} (block={})</source>
        <translation>Segmentation model resolution rounded automatically: {} → {} (block={})</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="240"/>
        <location filename="../app/train/transformer_train_runner.py" line="158"/>
        <source>使用模型 {} device={} epochs={} batch={} resolution={}</source>
        <translation>Using model {} device={} epochs={} batch={} resolution={}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="252"/>
        <location filename="../app/train/transformer_train_runner.py" line="169"/>
        <source>数据增强: {}</source>
        <translation>Data augmentation: {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="255"/>
        <location filename="../app/train/transformer_train_runner.py" line="172"/>
        <source>数据增强: 未启用</source>
        <translation>Augmentation: none</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="281"/>
        <location filename="../app/train/transformer_train_runner.py" line="240"/>
        <source>训练完成</source>
        <translation>Training complete</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="288"/>
        <location filename="../app/train/transformer_train_runner.py" line="249"/>
        <source>生成类别文件: {}</source>
        <translation>Writing class file: {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="209"/>
        <location filename="../app/train/transformer_train_runner.py" line="143"/>
        <source>预训练权重缺失: 请先在权重管理里下载 {} 档的模型</source>
        <translation>Pretrained weights missing: download the {} tier model from Model Weights first</translation>
    </message>
</context>
<context>
    <name>TrainWorker</name>
    <message>
        <location filename="../app/train/train_worker.py" line="481"/>
        <source>训练监控异常, 已终止.

{}</source>
        <translation>Training monitor error; terminated.

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="490"/>
        <source>训练结果文件读取失败: {}

{}</source>
        <translation>Failed to read the training result file: {}

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="495"/>
        <source>训练进程异常退出 (code={})

--- 子进程输出(尾部) ---
{}</source>
        <translation>The training process exited abnormally (code={})

--- subprocess output (tail) ---
{}</translation>
    </message>
</context>
<context>
    <name>Utils</name>
    <message>
        <location filename="../app/core/utils.py" line="59"/>
        <location filename="../app/core/utils.py" line="71"/>
        <source>{}秒</source>
        <translation>{}s</translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="65"/>
        <source>{}天</source>
        <translation>{}d </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="67"/>
        <source>{}小时</source>
        <translation>{}h </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="69"/>
        <source>{}分</source>
        <translation>{}m </translation>
    </message>
</context>
<context>
    <name>_ModelRow</name>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="119"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="171"/>
        <source>本地</source>
        <translation>Local</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="142"/>
        <source>取消本地绑定</source>
        <translation>Unbind Local Weight</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="177"/>
        <source>已就绪</source>
        <translation>Ready</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="184"/>
        <source>未下载</source>
        <translation>Not downloaded</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="193"/>
        <source>更换</source>
        <translation>Change</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="201"/>
        <source>本地权重</source>
        <translation>Local weight</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="210"/>
        <source>重选</source>
        <translation>Reselect</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="211"/>
        <source>(路径未记录)</source>
        <translation>(path not recorded)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="213"/>
        <source>本地失效</source>
        <translation>Local weight missing</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="215"/>
        <source>登记的本地权重文件已不在这个位置:
{}</source>
        <translation>The registered local weight file is no longer at this location:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="220"/>
        <source>校验中...</source>
        <translation>Verifying...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="239"/>
        <source>失败</source>
        <translation>Failed</translation>
    </message>
</context>
<context>
    <name>_PixelScaleDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="109"/>
        <source>像素精度</source>
        <translation>Pixel scale</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="115"/>
        <source>1 像素代表的实际长度</source>
        <translation>Real length that 1 pixel represents</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="148"/>
        <source>请输入大于 0 的数字</source>
        <translation>Enter a number greater than 0</translation>
    </message>
</context>
<context>
    <name>_TrainStartDialog</name>
    <message>
        <location filename="../app/train/dialogs.py" line="365"/>
        <source>训练即将开始</source>
        <translation>Training is about to start</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="375"/>
        <location filename="../app/train/dialogs.py" line="388"/>
        <source>确认({})</source>
        <translation>OK ({})</translation>
    </message>
</context>
<context>
    <name>addLabelDialog</name>
    <message>
        <location filename="../ui/add_label.ui" line="14"/>
        <source>Dialog</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/add_label.ui" line="49"/>
        <source>导入</source>
        <translation>Import</translation>
    </message>
    <message>
        <location filename="../ui/add_label.ui" line="284"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
</context>
<context>
    <name>annotationDialog</name>
    <message>
        <location filename="../ui/annotation.ui" line="14"/>
        <source>Dialog</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="24"/>
        <source>矩形</source>
        <translation>Rectangle</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="35"/>
        <source>多边形</source>
        <translation>Polygon</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="46"/>
        <source>删除图像</source>
        <translation>Delete Image</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="70"/>
        <source>设置</source>
        <translation>Settings</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="86"/>
        <source>输入本图文字</source>
        <translation>Enter the text in this image</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="101"/>
        <source>标签列表</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="124"/>
        <source>添加标签</source>
        <translation>Add Label</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="127"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="171"/>
        <source>标注信息</source>
        <translation>Annotations</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="191"/>
        <source>转换</source>
        <translation>Convert</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="221"/>
        <source>图像信息</source>
        <translation>Image Info</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="248"/>
        <source>剪切板</source>
        <translation>Clipboard</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="313"/>
        <source>上一张(A)</source>
        <translation>Prev (A)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="320"/>
        <source>下一张(D)</source>
        <translation>Next (D)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="370"/>
        <source>标注参数</source>
        <translation>Annotation Params</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="382"/>
        <source>角度范围</source>
        <translation>Angle Range</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="396"/>
        <source>~</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="430"/>
        <source>融合强度</source>
        <translation>Blend Strength</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="464"/>
        <source>亮度调节</source>
        <translation>Brightness</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="498"/>
        <source>填充颜色</source>
        <translation>Fill Color</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="505"/>
        <source>点击打开取色器, 选任意颜色</source>
        <translation>Click to open the color picker</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="518"/>
        <source>支持 #RRGGBB / #RGB / 255,255,255 / black / 白 等写法, 也可以点左边色块打开取色器</source>
        <translation>Accepts #RRGGBB / #RGB / 255,255,255 / black / white — or click the swatch on the left to pick a color</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="521"/>
        <source>#RRGGBB</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="528"/>
        <source>自定义颜色</source>
        <translation>Custom Color</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="555"/>
        <source>常用色</source>
        <translation>Presets</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="586"/>
        <source>恢复默认</source>
        <translation>Reset</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="606"/>
        <source>完成</source>
        <translation>Done</translation>
    </message>
</context>
</TS>
