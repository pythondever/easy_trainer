<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="en_US">
<context>
    <name>AdCommon</name>
    <message>
        <location filename="../app/train/ad_common.py" line="102"/>
        <source>找不到可写的纯英文暂存目录(异常检测的底层库不支持中文路径), 请把输出路径改到纯英文目录下</source>
        <translation>No writable ASCII-only temp directory found (the anomaly detection library does not support non-ASCII paths); change the output path to an ASCII-only directory</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="164"/>
        <location filename="../app/train/ad_common.py" line="689"/>
        <source>(根目录散图)</source>
        <translation>(loose images in root)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="187"/>
        <source>数据集里没找到图像, 请先导入数据</source>
        <translation>No images found in the dataset; import data first</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="192"/>
        <source>无法从类别名判断哪个是正常品, 请把放良品图的那个文件夹改名为 {} 之一; 现有类别: {}</source>
        <translation>Cannot tell which class holds good parts from the class names; rename the folder of good images to one of {}; existing classes: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="198"/>
        <source>训练集里没有图像</source>
        <translation>The train set has no images</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="205"/>
        <source>训练集里只有&quot;{}&quot;一类, 而良品类是&quot;{}&quot;; 请把良品图所在的类别文件夹挂到训练集上</source>
        <translation>The train set has only class &quot;{}&quot; while the good class is &quot;{}&quot;; attach the folder holding good images to the train set</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="215"/>
        <source>训练集里既没有&quot;{}&quot;类、又不止一类, 无法确定拿哪批图建库; 现有类别: {}</source>
        <translation>The train set has no class &quot;{}&quot; and more than one class, so it is unclear which images to use for the memory bank; existing classes: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="257"/>
        <source>训练集根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>The train root has both loose images and subfolders, so the class of the loose images is unclear; put them into one class folder</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="291"/>
        <source>没有找到任何图像, 请检查数据集</source>
        <translation>No images found; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="293"/>
        <source>根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>The root has both loose images and subfolders, so the class of the loose images is unclear; put them into one class folder</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="298"/>
        <source>无法判断哪个类别是良品, 现有类别: {}.
请把良品图放在名为 {} 一类的子文件夹里, 或按训练时的方式重新导入数据集</source>
        <translation>Cannot tell which class is good; existing classes: {}.
Put the good images in a subfolder named one of {}, or re-import the dataset the same way as for training</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="452"/>
        <source>未知的异常检测算法: {}</source>
        <translation>Unknown anomaly detection algorithm: {}</translation>
    </message>
</context>
<context>
    <name>AdTestRunner</name>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="46"/>
        <source>缺少测试依赖: {}</source>
        <translation>Missing test dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="263"/>
        <source>图像</source>
        <translation>Image</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="264"/>
        <source>类别</source>
        <translation>Class</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="265"/>
        <source>真值</source>
        <translation>Ground truth</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="266"/>
        <source>判定</source>
        <translation>Verdict</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="267"/>
        <source>分数</source>
        <translation>Score</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="268"/>
        <source>阈值</source>
        <translation>Threshold</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="269"/>
        <source>是否正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="284"/>
        <source>是</source>
        <translation>Yes</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="285"/>
        <source>否</source>
        <translation>No</translation>
    </message>
</context>
<context>
    <name>AdTrainRunner</name>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="48"/>
        <source>缺少训练依赖: {}</source>
        <translation>Missing training dependency: {}</translation>
    </message>
</context>
<context>
    <name>AddLabelDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="458"/>
        <source>添加标签</source>
        <translation>Add Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="472"/>
        <source>编辑标签</source>
        <translation>Edit Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="504"/>
        <source>标签名称, 多个用逗号分隔</source>
        <translation>Label names, separate multiple with commas</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="506"/>
        <source>导入</source>
        <translation>Import</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="513"/>
        <source>选择数据集...</source>
        <translation>Select dataset...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="536"/>
        <location filename="../app/annotation/annotation_dialog.py" line="541"/>
        <source>导入标签</source>
        <translation>Import Labels</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="537"/>
        <source>请先选择一个数据集</source>
        <translation>Select a dataset first</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="542"/>
        <source>数据集&quot;{}&quot;还没有标签</source>
        <translation>Dataset &quot;{}&quot; has no labels yet</translation>
    </message>
</context>
<context>
    <name>AnnotationDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="295"/>
        <source>复制</source>
        <translation>Copy</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="297"/>
        <source>填充</source>
        <translation>Fill</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="307"/>
        <source>粘贴</source>
        <translation>Paste</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="689"/>
        <source>标注 - {} / {}</source>
        <translation>Annotation - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="707"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1934"/>
        <source>矩形</source>
        <translation>Rectangle</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="708"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1940"/>
        <source>多边形</source>
        <translation>Polygon</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="717"/>
        <source>标签列表</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="718"/>
        <source>标注信息</source>
        <translation>Annotations</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="719"/>
        <source>上一张</source>
        <translation>Prev</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="720"/>
        <source>下一张</source>
        <translation>Next</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="755"/>
        <source>只在选中的多边形框内生效; A/D 切图或 Ctrl+S 才写盘</source>
        <translation>Applies only inside the selected polygon; written to disk on A/D image switch or Ctrl+S</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="793"/>
        <source>显示标注</source>
        <translation>Show labels</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="880"/>
        <source>先在画布上点选一个多边形</source>
        <translation>Select a polygon on the canvas first</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="883"/>
        <source>亮度调节只对多边形有效</source>
        <translation>Brightness adjustment only works on polygons</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1159"/>
        <source>    类别: {}</source>
        <translation>    Class: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1186"/>
        <source>删除本地文件</source>
        <translation>Delete local files</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1187"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1189"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1199"/>
        <source>删除图像</source>
        <translation>Delete Image</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1190"/>
        <source>是否删除当前图像?

{}</source>
        <translation>Delete the current image?

{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1194"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>The image and its label file will be deleted from disk. This cannot be undone</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1200"/>
        <source>无法访问主窗口, 删除失败</source>
        <translation>Cannot reach the main window; delete failed</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1214"/>
        <source>(无图像)</source>
        <translation>(no image)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1278"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1885"/>
        <source>添加标签</source>
        <translation>Add Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1279"/>
        <source>请先添加标签(点击&quot;+&quot;)</source>
        <translation>Add a label first (click &quot;+&quot;)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1391"/>
        <source>剪切板  {}/{}</source>
        <translation>Clipboard  {}/{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1416"/>
        <source>第 {} 个模板  {}x{}
左键选中用于粘贴, 右键 删除/导入/导出/清空</source>
        <translation>Template {}  {}x{}
Left click to select for pasting; right click to delete / import / export / clear</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1448"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1697"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1451"/>
        <source>导入</source>
        <translation>Import</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1452"/>
        <source>导出</source>
        <translation>Export</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1454"/>
        <source>清空</source>
        <translation>Clear</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1482"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1509"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1513"/>
        <source>导出剪切板</source>
        <translation>Export Clipboard</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1483"/>
        <source>剪切板是空的, 没有可导出的模板</source>
        <translation>The clipboard is empty; nothing to export</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1485"/>
        <source>选择导出目录</source>
        <translation>Select Export Directory</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1510"/>
        <source>导出中断: {}
(已写出 {} 个)</source>
        <translation>Export interrupted: {}
({} written)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1514"/>
        <source>已导出 {} 个模板(png + 同名 json)到:
{}</source>
        <translation>Exported {} template(s) (png + same-name json) to:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1518"/>
        <source>选择导入目录</source>
        <translation>Select Import Directory</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1525"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1529"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1563"/>
        <source>导入剪切板</source>
        <translation>Import Clipboard</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1526"/>
        <source>读取目录失败: {}</source>
        <translation>Failed to read the directory: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1530"/>
        <source>这个目录里没有 png 文件</source>
        <translation>No png files in this directory</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1558"/>
        <source>已导入 {} 个模板到剪切板</source>
        <translation>Imported {} template(s) into the clipboard</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1560"/>
        <source>
其中 {} 个没有同名 json, 按矩形导入</source>
        <translation>
{} of them have no same-name json and were imported as rectangles</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1562"/>
        <source>
{} 个文件读不出来, 已跳过</source>
        <translation>
{} file(s) could not be read and were skipped</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1638"/>
        <source>修改类别</source>
        <translation>Change Class</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1639"/>
        <source>移动图像文件失败:
{}</source>
        <translation>Failed to move the image file:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1696"/>
        <source>编辑</source>
        <translation>Edit</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1755"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1814"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1821"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1830"/>
        <source>删除标签</source>
        <translation>Delete Label</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1755"/>
        <source>正在统计标注文件...</source>
        <translation>Counting label files...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1815"/>
        <source>标签&quot;{}&quot;已有 {} 处标注, 删除后这些标注将被一并删除且不可恢复.
确定删除吗?</source>
        <translation>Label &quot;{}&quot; has {} annotation(s). Deleting it removes them all and cannot be undone.
Delete anyway?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1822"/>
        <source>确定删除标签&quot;{}&quot;吗?</source>
        <translation>Delete label &quot;{}&quot;?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1830"/>
        <source>正在清理标注文件...</source>
        <translation>Cleaning up label files...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1886"/>
        <source>标签名称不能为空</source>
        <translation>Label name cannot be empty</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1941"/>
        <source>{} 个顶点</source>
        <translation>{} vertices</translation>
    </message>
</context>
<context>
    <name>App</name>
    <message>
        <location filename="../app/main_window.py" line="43"/>
        <source>软件启动</source>
        <translation>App started</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="46"/>
        <source>软件退出</source>
        <translation>App exited</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="48"/>
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
        <source>编辑</source>
        <translation>Edit</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="406"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="413"/>
        <source>统计</source>
        <translation>Stats</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="420"/>
        <source>训练</source>
        <translation>Train</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="427"/>
        <source>模型</source>
        <translation>Models</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="434"/>
        <location filename="../app/mixins/queue_mixin.py" line="334"/>
        <source>队列</source>
        <translation>Queue</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="441"/>
        <source>日志</source>
        <translation>Log</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="460"/>
        <source>界面语言</source>
        <translation>Interface language</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="551"/>
        <source>上一页</source>
        <translation>Prev</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="580"/>
        <source>下一页</source>
        <translation>Next</translation>
    </message>
</context>
<context>
    <name>Charts</name>
    <message>
        <location filename="../app/widgets/charts.py" line="11"/>
        <source>暂无标注</source>
        <translation>No annotations</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="12"/>
        <source>标签</source>
        <translation>Label</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="13"/>
        <source>标签数量</source>
        <translation>Label count</translation>
    </message>
</context>
<context>
    <name>ClassifyTestRunner</name>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="33"/>
        <source>缺少测试依赖: {}</source>
        <translation>Missing test dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="85"/>
        <source>加载分类模型: {}</source>
        <translation>Loading classification model: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="110"/>
        <source>测试图片 {} 张</source>
        <translation>{} test images</translation>
    </message>
</context>
<context>
    <name>ClassifyTrainRunner</name>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="40"/>
        <source>缺少训练依赖: {}</source>
        <translation>Missing training dependency: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="132"/>
        <source>输出路径: {}</source>
        <translation>Output path: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="133"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Run output directory (timestamp): {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="149"/>
        <source>分类训练: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</source>
        <translation>Classification training: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="158"/>
        <source>数据准备: train={} 张, val={} 张</source>
        <translation>Data prep: train={} images, val={} images</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="160"/>
        <source>训练集无图像, 请检查数据集</source>
        <translation>Train set has no images; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="162"/>
        <source>验证集无图像, 请检查数据集</source>
        <translation>Val set has no images; check the dataset</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="187"/>
        <source>未从数据集中解析到任何类别(子文件夹),无法训练图像分类</source>
        <translation>No classes (subfolders) parsed from the dataset; cannot train image classification</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="197"/>
        <source>数据集: train={} val={} 类别({})={}</source>
        <translation>Dataset: train={} val={} classes({})={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="284"/>
        <source>早停触发: 连续 {} 个 epoch 精度无提升</source>
        <translation>Early stop triggered: no accuracy gain for {} epochs in a row</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="289"/>
        <source>训练完成 best_acc={:.4f}</source>
        <translation>Training complete best_acc={:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="297"/>
        <source>生成类别文件: {}</source>
        <translation>Writing class file: {}</translation>
    </message>
</context>
<context>
    <name>ColorPickerDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="2250"/>
        <source>选择颜色</source>
        <translation>Pick Color</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="2262"/>
        <source>十六进制:</source>
        <translation>Hex:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="2283"/>
        <source>基本颜色:</source>
        <translation>Basic colors:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="2295"/>
        <source>自定义 RGB:</source>
        <translation>Custom RGB:</translation>
    </message>
</context>
<context>
    <name>DataBase</name>
    <message>
        <location filename="../app/core/db.py" line="479"/>
        <source>已删除图像记录解析失败, 跳过迁移以免覆盖丢失 ({}): {}</source>
        <translation>Failed to parse the deleted-image record; skipping migration to avoid overwriting data ({}): {}</translation>
    </message>
</context>
<context>
    <name>DataPrep</name>
    <message>
        <location filename="../app/train/data_prep.py" line="189"/>
        <source>解析到类别 {} 个: {}</source>
        <translation>Parsed {} classes: {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="209"/>
        <source>复制数据集 {}: 图像 {} 张, 标签 {} 个 → {}</source>
        <translation>Copy dataset {}: {} images, {} labels → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="296"/>
        <source>合并 {} 数据集 → {} ({} 个文件)</source>
        <translation>Merge {} dataset → {} ({} files)</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="313"/>
        <source>生成 data.yaml → {}</source>
        <translation>Write data.yaml → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="326"/>
        <source>未从数据集中解析到任何标签类别, 请检查标签文件</source>
        <translation>No label classes parsed from the dataset; check the label files</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="333"/>
        <source>数据准备完成: {} 个类别, 输出目录 {}</source>
        <translation>Data prep done: {} classes, output directory {}</translation>
    </message>
</context>
<context>
    <name>DatasetViewMixin</name>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="246"/>
        <source>删除全部未标注图像({} 张)</source>
        <translation>Delete all unlabeled images ({} images)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="252"/>
        <source>删除所选图像({} 张)</source>
        <translation>Delete selected images ({} images)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="349"/>
        <source>重载跳过: 数据集 {}/{} 无图像目录</source>
        <translation>Reload skipped: dataset {}/{} has no image directory</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="350"/>
        <source>重载</source>
        <translation>Reload</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="351"/>
        <source>该数据集还没有图像目录, 请先右键&quot;导入&quot;</source>
        <translation>This dataset has no image directory yet; right-click &quot;Import&quot; first</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="355"/>
        <source>重载跳过: 数据集 {}/{} 正在载入</source>
        <translation>Reload skipped: dataset {}/{} is loading</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="357"/>
        <source>重载数据集: {}/{}</source>
        <translation>Reload dataset: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="802"/>
        <source>第 {} / {} 页</source>
        <translation>Page {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="806"/>
        <source>第 {}/{} 页 · 共 {} 个</source>
        <translation>Page {}/{} · {} items</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="808"/>
        <source>第 {}/{} 页 · 共 {} 张</source>
        <translation>Page {}/{} · {} images</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="817"/>
        <source>暂无数据</source>
        <translation>No data</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="854"/>
        <source>开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}</source>
        <translation>Import start: {}/{} | image path={} | label path={} | format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="855"/>
        <location filename="../app/mixins/dataset_view_mixin.py" line="925"/>
        <source>(无)</source>
        <translation>(none)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="920"/>
        <source>{}: {}个</source>
        <translation>{}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="922"/>
        <source>数据集导入完成: {}/{} | 图像 {} 张, 已标注 {} 张 | 标签({}类): {}</source>
        <translation>Dataset import done: {}/{} | {} images, {} labeled | labels ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="966"/>
        <source>数据集 {}/{} 未导入, 右键&quot;导入&quot;选择图像与标签目录</source>
        <translation>Dataset {}/{} not imported; right-click &quot;Import&quot; to choose the image and label folders</translation>
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
        <location filename="../ui/edit_label.ui" line="14"/>
        <source>类别修改</source>
        <translation>Edit Class</translation>
    </message>
    <message>
        <location filename="../ui/edit_label.ui" line="22"/>
        <source>类别</source>
        <translation>Class</translation>
    </message>
    <message>
        <location filename="../ui/edit_label.ui" line="42"/>
        <source>批量修改为</source>
        <translation>Rename all to</translation>
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
        <location filename="../app/annotation/annotation_dialog.py" line="501"/>
        <location filename="../app/mixins/import_export_mixin.py" line="277"/>
        <location filename="../app/mixins/label_mixin.py" line="196"/>
        <location filename="../app/mixins/misc_mixin.py" line="122"/>
        <location filename="../app/widgets/dialog_buttons.py" line="104"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../app/widgets/dialog_buttons.py" line="110"/>
        <source>取消</source>
        <translation>Cancel</translation>
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
        <location filename="../ui/import_data.ui" line="113"/>
        <source>标签格式:</source>
        <translation>Label format:</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="126"/>
        <source>Yolo txt</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="139"/>
        <source>Labelme json</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="149"/>
        <source>按子文件夹分类导入</source>
        <translation>Import as classification (subfolders)</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="179"/>
        <source>提示信息</source>
        <translation>Info</translation>
    </message>
</context>
<context>
    <name>ImportExportMixin</name>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="58"/>
        <source>导入数据 - {} / {}</source>
        <translation>Import Data - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="65"/>
        <location filename="../app/mixins/import_export_mixin.py" line="165"/>
        <source>请选择图像文件夹</source>
        <translation>Choose an image folder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="141"/>
        <source>请选择分类根目录(子文件夹名=类别)</source>
        <translation>Choose the classification root folder (subfolder name = class)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="154"/>
        <source>(根目录)</source>
        <translation>(root folder)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="156"/>
        <source>所选文件夹下无分类子文件夹或图像</source>
        <translation>No class subfolders or images in the selected folder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="158"/>
        <source>{}: {}张</source>
        <translation>{}: {} images</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="160"/>
        <source>检测到 {} 类: {}</source>
        <translation>Detected {} classes: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="79"/>
        <source>所选文件夹无图像</source>
        <translation>No images in the selected folder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="82"/>
        <source>共 {} 张图像, 已标注 {} 张</source>
        <translation>{} images, {} labeled</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="98"/>
        <source>(检测到 {} 张 {} 标签, 请切换上方格式为&quot;{}&quot;)</source>
        <translation>({} {} label(s) detected; switch the format above to &quot;{}&quot;)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="102"/>
        <source>共 {} 张图像, 已标注 0 张 {}</source>
        <translation>{} images, 0 labeled {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="104"/>
        <source>共 {} 张图像(标签目录无匹配文件)</source>
        <translation>{} images (no matching files in the label folder)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="171"/>
        <source>选择文件夹</source>
        <translation>Select Folder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="211"/>
        <source>分类根目录(子文件夹名=类别)</source>
        <translation>Classification root (subfolder name = class)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="211"/>
        <source>图像路径</source>
        <translation>Image path</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="233"/>
        <location filename="../app/mixins/import_export_mixin.py" line="236"/>
        <source>导入数据</source>
        <translation>Import Data</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="233"/>
        <source>请先选择有效的图像文件夹</source>
        <translation>Choose a valid image folder first</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="236"/>
        <source>标签路径无效</source>
        <translation>Invalid label path</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="297"/>
        <location filename="../app/mixins/import_export_mixin.py" line="302"/>
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
        <location filename="../app/mixins/import_export_mixin.py" line="297"/>
        <source>请先在左侧选中要导出的数据集</source>
        <translation>Select the dataset to export on the left first</translation>
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
        <location filename="../app/tasks/import_task.py" line="113"/>
        <source>导入跳过 {}: {}</source>
        <translation>Import skipped {}: {}</translation>
    </message>
</context>
<context>
    <name>LabelMixin</name>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="553"/>
        <location filename="../app/mixins/label_mixin.py" line="39"/>
        <location filename="../app/mixins/label_mixin.py" line="55"/>
        <location filename="../app/mixins/label_mixin.py" line="124"/>
        <source>未标注</source>
        <translation>Unlabeled</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="181"/>
        <location filename="../app/mixins/label_mixin.py" line="186"/>
        <location filename="../app/mixins/label_mixin.py" line="203"/>
        <source>重命名</source>
        <translation>Rename</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="181"/>
        <location filename="../app/mixins/label_mixin.py" line="434"/>
        <source>请先在左侧选中一个数据集</source>
        <translation>Select a dataset on the left first</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="187"/>
        <source>请先在筛选下拉框中选择要重命名的标签</source>
        <translation>Select the label to rename in the filter dropdown first</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="190"/>
        <source>类别修改</source>
        <translation>Edit Class</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="203"/>
        <source>标签名称不能为空</source>
        <translation>Label name cannot be empty</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="212"/>
        <source>合并标签</source>
        <translation>Merge Labels</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="213"/>
        <source>标签&quot;{}&quot;已存在.
确定把&quot;{}&quot;的所有标注合并到&quot;{}&quot;吗?
此操作会改写数据集源标签文件, 且不可恢复.</source>
        <translation>Label &quot;{}&quot; already exists.
Merge all annotations of &quot;{}&quot; into &quot;{}&quot;?
This rewrites the dataset&apos;s source label files and cannot be undone.</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="268"/>
        <source>合并标签: {} → {} ({}/{}) | 启动后台文件合并, 完成后输出统计</source>
        <translation>Merge labels: {} → {} ({}/{}) | background file merge started; stats printed when done</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="274"/>
        <source>重命名标签: {} → {} ({}/{})</source>
        <translation>Rename label: {} → {} ({}/{})</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="346"/>
        <source>{}: {}个</source>
        <translation>{}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="349"/>
        <source>删除标签完成: {} | 修改 {} 个标签文件 | 删除后标签统计({}类): {}</source>
        <translation>Delete label done: {} | {} label files changed | label stats after delete ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="352"/>
        <location filename="../app/mixins/label_mixin.py" line="357"/>
        <location filename="../app/mixins/label_mixin.py" line="362"/>
        <source>(无)</source>
        <translation>(none)</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="354"/>
        <source>合并标签: {} → {} | 修改 {} 个标签文件 | 合并后标签统计({}类): {}</source>
        <translation>Merge labels: {} → {} | {} label files changed | label stats after merge ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="359"/>
        <source>合并标签: {} → {} | 无标签文件被修改 | 合并后标签统计({}类): {}</source>
        <translation>Merge labels: {} → {} | no label files changed | label stats after merge ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="400"/>
        <source>重命名标签</source>
        <translation>Rename Labels</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="400"/>
        <source>正在更新标注文件...</source>
        <translation>Updating label files...</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="434"/>
        <location filename="../app/mixins/label_mixin.py" line="439"/>
        <location filename="../app/mixins/label_mixin.py" line="443"/>
        <location filename="../app/mixins/label_mixin.py" line="544"/>
        <source>删除标签</source>
        <translation>Delete Label</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="440"/>
        <source>请先在筛选下拉框中选择要删除的标签</source>
        <translation>Select the label to delete in the filter dropdown first</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="444"/>
        <source>确定删除标签&quot;{}&quot;吗?
该标签的所有标注将被删除, 且不可恢复.</source>
        <translation>Delete label &quot;{}&quot;?
All its annotations will be removed and cannot be undone.</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="477"/>
        <source>删除标签: {} ({}/{})</source>
        <translation>Delete label: {} ({}/{})</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="544"/>
        <source>正在清理标注文件...</source>
        <translation>Cleaning up label files...</translation>
    </message>
</context>
<context>
    <name>LogDialog</name>
    <message>
        <location filename="../ui/log.ui" line="14"/>
        <source>Dialog</source>
        <translation>Add Label</translation>
    </message>
    <message>
        <location filename="../ui/log.ui" line="37"/>
        <source>清空</source>
        <translation>Clear</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="79"/>
        <location filename="../app/widgets/log_dialog.py" line="20"/>
        <source>日志</source>
        <translation>Log</translation>
    </message>
</context>
<context>
    <name>MessageBox</name>
    <message>
        <location filename="../app/widgets/message_box.py" line="146"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="170"/>
        <source>是</source>
        <translation>Yes</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="171"/>
        <source>否</source>
        <translation>No</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="226"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="258"/>
        <source>取消中...</source>
        <translation>Cancelling...</translation>
    </message>
</context>
<context>
    <name>MetricsDialog</name>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="33"/>
        <source>训练指标</source>
        <translation>Training Metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="61"/>
        <source>标签筛选</source>
        <translation>Label filter</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="65"/>
        <source>全部指标</source>
        <translation>All metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="66"/>
        <source>全部标签-P</source>
        <translation>All labels - P</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="67"/>
        <source>全部标签-R</source>
        <translation>All labels - R</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="80"/>
        <source>(暂无标签数据,需完成首次 epoch 验证后才会出现)</source>
        <translation>(No label data yet; shown after the first epoch validation)</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="105"/>
        <source>暂无该标签的指标数据(训练完成后可查看)</source>
        <translation>No metric data for this label yet (available after training completes)</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="148"/>
        <source>loss 值</source>
        <translation>Loss</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="149"/>
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
        <location filename="../app/mixins/misc_mixin.py" line="114"/>
        <source>数据集统计</source>
        <translation>Dataset Statistics</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="123"/>
        <source>应用所选数据集</source>
        <translation>Apply selected datasets</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="214"/>
        <source>[{}/{}](未设置)</source>
        <translation>[{}/{}](not set)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="217"/>
        <source>(未选择数据集)</source>
        <translation>(no dataset selected)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="342"/>
        <source>删除图像: {} 张 | 方式={} | 本地删除文件={} | 项目={}, 数据集={}</source>
        <translation>Delete images: {} | mode={} | delete local files={} | project={}, dataset={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="343"/>
        <source>删除本地文件</source>
        <translation>Delete local files</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="343"/>
        <source>仅标记不加载</source>
        <translation>Mark only, do not load</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="381"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="382"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="384"/>
        <source>删除图像</source>
        <translation>Delete Images</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="385"/>
        <source>将从系统删除所选 {} 张图像?

(图像与同名标注文件不可恢复)</source>
        <translation>Delete the selected {} image(s) from the system?

(Images and their label files cannot be recovered)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="390"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>Images and their label files will be deleted from disk. This cannot be undone</translation>
    </message>
</context>
<context>
    <name>ModelAssets</name>
    <message>
        <location filename="../app/core/model_assets.py" line="79"/>
        <location filename="../app/core/model_assets.py" line="113"/>
        <source>速度最快, 精度够用</source>
        <translation>Fastest, accuracy is sufficient</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="80"/>
        <location filename="../app/core/model_assets.py" line="117"/>
        <source>精度更好, 稍慢一些</source>
        <translation>Better accuracy, slightly slower</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="81"/>
        <location filename="../app/core/model_assets.py" line="121"/>
        <source>精度更高</source>
        <translation>Higher accuracy</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="82"/>
        <location filename="../app/core/model_assets.py" line="125"/>
        <source>精度最高, 显存占用大</source>
        <translation>Highest accuracy, but uses more VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="83"/>
        <source>精度极致, 显存占用很大</source>
        <translation>Ultimate accuracy, uses much more VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="86"/>
        <location filename="../app/core/model_assets.py" line="129"/>
        <source>轻量分割</source>
        <translation>Lightweight segmentation</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="87"/>
        <location filename="../app/core/model_assets.py" line="133"/>
        <source>速度与精度平衡</source>
        <translation>Balanced speed and accuracy</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="88"/>
        <location filename="../app/core/model_assets.py" line="137"/>
        <source>细节更完整</source>
        <translation>More complete details</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="89"/>
        <location filename="../app/core/model_assets.py" line="141"/>
        <source>最精细</source>
        <translation>Most refined</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="90"/>
        <source>最精细, 显存占用很大</source>
        <translation>Most refined, uses much more VRAM</translation>
    </message>
</context>
<context>
    <name>ModelDialog</name>
    <message>
        <location filename="../ui/model.ui" line="14"/>
        <location filename="../app/widgets/model_dialog.py" line="146"/>
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
        <location filename="../app/widgets/model_dialog.py" line="565"/>
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
        <location filename="../app/widgets/model_dialog.py" line="569"/>
        <source>精度</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="150"/>
        <location filename="../app/widgets/model_dialog.py" line="580"/>
        <source>训练时间</source>
        <translation>Trained at</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="155"/>
        <location filename="../app/widgets/model_dialog.py" line="582"/>
        <source>耗时</source>
        <translation>Duration</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="160"/>
        <location filename="../app/widgets/model_dialog.py" line="572"/>
        <source>图像尺寸</source>
        <translation>Image Size</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="165"/>
        <source>操作</source>
        <translation>Actions</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="182"/>
        <source>模型详情</source>
        <translation>Model details</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="189"/>
        <location filename="../app/widgets/model_dialog.py" line="549"/>
        <source>选中一行查看详情</source>
        <translation>Select a row to see details</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="215"/>
        <source>查看完整指标</source>
        <translation>View full metrics</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="222"/>
        <source>测试此模型</source>
        <translation>Test this model</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="229"/>
        <source>按此配置重训</source>
        <translation>Retrain with this config</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="236"/>
        <source>打开模型目录</source>
        <translation>Open model directory</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="276"/>
        <source>上一页</source>
        <translation>Prev</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="283"/>
        <source>1/1</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="290"/>
        <source>下一页</source>
        <translation>Next</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="389"/>
        <source>共 {} 条</source>
        <translation>{} records</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="440"/>
        <source> 等 {} 类</source>
        <translation> and {} more classes</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="464"/>
        <source>测试</source>
        <translation>Test</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="469"/>
        <source>导出</source>
        <translation>Export</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="474"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="562"/>
        <source>{} × {} 累积</source>
        <translation>{} × {} accumulated</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="563"/>
        <source>状态</source>
        <translation>Status</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="570"/>
        <source>训练集</source>
        <translation>Train Set</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="571"/>
        <source>验证集</source>
        <translation>Val Set</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="573"/>
        <source>轮数 / 早停</source>
        <translation>Epochs / Early stop</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="575"/>
        <source>批大小</source>
        <translation>Batch size</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="576"/>
        <source>学习率</source>
        <translation>Learning rate</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="577"/>
        <source>优化器</source>
        <translation>Optimizer</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="578"/>
        <source>设备</source>
        <translation>Device</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="579"/>
        <source>标签</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="583"/>
        <source>模型路径</source>
        <translation>Model path</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="602"/>
        <source>失败原因</source>
        <translation>Failure reason</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="620"/>
        <source>暂无曲线</source>
        <translation>No curve</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="644"/>
        <source>{}  最佳 {:.3f}</source>
        <translation>{}  best {:.3f}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="652"/>
        <location filename="../app/widgets/model_dialog.py" line="663"/>
        <source>打开目录</source>
        <translation>Open directory</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="653"/>
        <source>模型目录不存在:
{}</source>
        <translation>Model directory does not exist:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="681"/>
        <source>[model_dialog] 打开指标失败: {}
{}</source>
        <translation>[model_dialog] Failed to open metrics: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="683"/>
        <source>查看指标失败</source>
        <translation>Failed to open metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="690"/>
        <source>删除模型记录</source>
        <translation>Delete Model Record</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="691"/>
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
        <location filename="../app/widgets/model_dialog.py" line="695"/>
        <source>删除模型记录: 项目={} 数据集={} 任务={} 开始时间={}</source>
        <translation>Delete model record: project={} dataset={} task={} start time={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="709"/>
        <source>删除模型记录失败: {} | {}</source>
        <translation>Failed to delete model record: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="710"/>
        <source>[model_dialog] 删除失败: {}
{}</source>
        <translation>[model_dialog] Delete failed: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="719"/>
        <source>[model_dialog] 打开训练失败: {}
{}</source>
        <translation>[model_dialog] Failed to open training: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="720"/>
        <source>打开训练失败</source>
        <translation>Failed to open training</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="745"/>
        <source>[model_dialog] 打开测试失败: {}
{}</source>
        <translation>[model_dialog] Failed to open testing: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="747"/>
        <source>打开测试失败</source>
        <translation>Failed to open testing</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="764"/>
        <location filename="../app/widgets/model_dialog.py" line="782"/>
        <location filename="../app/widgets/model_dialog.py" line="798"/>
        <location filename="../app/widgets/model_dialog.py" line="1032"/>
        <location filename="../app/widgets/model_dialog.py" line="1042"/>
        <source>导出模型</source>
        <translation>Export Model</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="765"/>
        <source>模型文件不存在:
{}</source>
        <translation>Model file does not exist:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="766"/>
        <source>导出模型失败: 模型文件不存在 {}</source>
        <translation>Export model failed: model file not found {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="768"/>
        <source>选择导出目录</source>
        <translation>Select Export Directory</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="783"/>
        <source>创建目录失败: {}</source>
        <translation>Failed to create directory: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="784"/>
        <source>导出模型失败: 创建目录失败 {} | {}</source>
        <translation>Export model failed: cannot create directory {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="794"/>
        <source>开始导出模型: 项目={} 任务={} 架构={} 尺寸={} | {}</source>
        <translation>Export model start: project={} task={} arch={} size={} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="795"/>
        <location filename="../app/widgets/model_dialog.py" line="899"/>
        <source>未知</source>
        <translation>Unknown</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="799"/>
        <source>正在导出 ONNX...</source>
        <translation>Exporting ONNX...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="818"/>
        <source>ONNX 导出完成: {} ({:.1f} MB)</source>
        <translation>ONNX export done: {} ({:.1f} MB)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="876"/>
        <source>生成 classes.txt 失败: {}</source>
        <translation>Failed to write classes.txt: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="877"/>
        <source>[export] 生成 classes.txt 失败: {}</source>
        <translation>[export] Failed to write classes.txt: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="883"/>
        <source>导出模型报告跳过: 分类任务不出评估报告</source>
        <translation>Model report export skipped: classification tasks have no evaluation report</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="884"/>
        <source>分类任务不生成评估报告</source>
        <translation>Classification tasks do not produce an evaluation report</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="888"/>
        <source>导出模型报告跳过: 未找到验证集</source>
        <translation>Model report export skipped: no val set found</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="889"/>
        <source>未找到验证集, 已跳过评估报告</source>
        <translation>No validation set found; evaluation report skipped</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="891"/>
        <location filename="../app/widgets/model_dialog.py" line="965"/>
        <source>正在生成模型报告...</source>
        <translation>Generating model report...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="895"/>
        <source>正在生成模型报告 {}/{}</source>
        <translation>Generating model report {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="898"/>
        <source>导出模型评估失败: {}</source>
        <translation>Model export evaluation failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="901"/>
        <source>评估失败, 已跳过报告: {}</source>
        <translation>Evaluation failed; report skipped: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="984"/>
        <source>导出模型报告跳过: 验证集没有标注</source>
        <translation>Model report export skipped: the val set has no labels</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="985"/>
        <source>验证集没有标注, 已跳过评估报告</source>
        <translation>The val set has no labels; the evaluation report was skipped.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="991"/>
        <source>[export] 生成评估报告失败:
{}</source>
        <translation>[export] Failed to generate the evaluation report:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="988"/>
        <source>生成评估报告失败: {}</source>
        <translation>Failed to generate the evaluation report: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="980"/>
        <source>导出模型报告完成: {}</source>
        <translation>Model report export done: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="992"/>
        <source>评估完成, 但报告生成失败</source>
        <translation>Evaluation finished, but the report could not be generated</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1026"/>
        <source>导出模型完成: {} | 包含: {}</source>
        <translation>Model export done: {} | contains: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1028"/>
        <source>已导出到:
{}

包含: {}</source>
        <translation>Exported to:
{}

Contains: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="990"/>
        <location filename="../app/widgets/model_dialog.py" line="1039"/>
        <source>未知错误</source>
        <translation>Unknown error</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1043"/>
        <source>模型导出失败, 详情见日志</source>
        <translation>Model export failed, see the log for details</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1038"/>
        <source>导出模型失败: {}</source>
        <translation>Export model failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1040"/>
        <source>[export] ONNX 导出失败: {}</source>
        <translation>[export] ONNX export failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1057"/>
        <source>复制导出示例失败: {}</source>
        <translation>Failed to copy the export sample: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1058"/>
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
        <location filename="../app/widgets/model_manager_dialog.py" line="287"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="291"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="340"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="347"/>
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
        <location filename="../app/widgets/model_manager_dialog.py" line="330"/>
        <source>开始下载</source>
        <translation>Start Download</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="275"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="171"/>
        <source>关闭</source>
        <translation>Close</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="52"/>
        <source>还剩 {}s</source>
        <translation>{}s left</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="53"/>
        <source>还剩 {}m{}s</source>
        <translation>{}m{}s left</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="237"/>
        <source>占用空间 {}</source>
        <translation>Uses {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="255"/>
        <source>选择权重目录</source>
        <translation>Select Weights Directory</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="276"/>
        <source>权重目录不可写入 {}: {!r}</source>
        <translation>Weights directory is not writable {}: {!r}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="287"/>
        <source>勾选的模型都已就绪, 不需要下载.</source>
        <translation>All selected models are ready; nothing to download.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="292"/>
        <source>当前目录不可写入, 请点&quot;更改&quot;换一个目录:
{}</source>
        <translation>The current directory is not writable. Click &quot;Change&quot; to pick another:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="297"/>
        <source>下载中...</source>
        <translation>Downloading...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="341"/>
        <source>以下权重没能下载完成:
</source>
        <translation>These weights could not be downloaded:
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="348"/>
        <source>下载还在进行, 现在关闭会中断下载(已下载部分保留, 下次可续传).
确定关闭?</source>
        <translation>A download is still running. Closing now interrupts it (the parts already downloaded are kept and will resume next time).
Close anyway?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="380"/>
        <source>去下载</source>
        <translation>Download</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="389"/>
        <source>该架构的权重必须先下载好才能开始训练.</source>
        <translation>Weights for this architecture must be downloaded before training can start.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="383"/>
        <source>本次训练选用 {} {}模型, 需要先下载 {}.</source>
        <translation>This training uses the {} {} model and needs {} downloaded first.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="382"/>
        <source>缺少模型权重</source>
        <translation>Missing Model Weights</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="381"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
</context>
<context>
    <name>MultiCombo</name>
    <message>
        <location filename="../app/widgets/multi_combo.py" line="349"/>
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
    <name>OnnxExport</name>
    <message>
        <location filename="../app/train/onnx_export.py" line="105"/>
        <source>异常检测模型暂不支持导出 ONNX(它是骨干加记忆库的组合结构), 请直接用模型文件在软件里测试</source>
        <translation>ONNX export is not supported for anomaly detection models (they combine a backbone with a memory bank); test them in the software directly with the model file</translation>
    </message>
</context>
<context>
    <name>ProjectMixin</name>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="18"/>
        <source>输入名称</source>
        <translation>Enter Name</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="19"/>
        <source>项目名称</source>
        <translation>Project name</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="22"/>
        <location filename="../app/mixins/project_mixin.py" line="26"/>
        <source>创建项目</source>
        <translation>Create Project</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="26"/>
        <location filename="../app/mixins/project_mixin.py" line="38"/>
        <source>项目名称已存在!</source>
        <translation>A project with this name already exists!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="29"/>
        <source>创建项目: {}</source>
        <translation>Create project: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="34"/>
        <location filename="../app/mixins/project_mixin.py" line="38"/>
        <location filename="../app/mixins/project_mixin.py" line="91"/>
        <source>修改名称</source>
        <translation>Rename</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <source>重命名项目: {} → {}</source>
        <translation>Rename project: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="46"/>
        <location filename="../app/mixins/project_mixin.py" line="92"/>
        <source>删除项目</source>
        <translation>Delete Project</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="47"/>
        <source>确定删除项目&quot;{}&quot;吗?
</source>
        <translation>Delete project &quot;{}&quot;?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="48"/>
        <source>删除项目: {}</source>
        <translation>Delete project: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="88"/>
        <location filename="../app/mixins/project_mixin.py" line="132"/>
        <location filename="../app/mixins/project_mixin.py" line="140"/>
        <source>添加数据集</source>
        <translation>Add Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="90"/>
        <source>导出项目</source>
        <translation>Export Project</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="107"/>
        <source>导入</source>
        <translation>Import</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="108"/>
        <source>导出</source>
        <translation>Export</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="109"/>
        <source>重载</source>
        <translation>Reload</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="110"/>
        <source>移动</source>
        <translation>Move</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="111"/>
        <source>修改</source>
        <translation>Rename</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="112"/>
        <source>删除</source>
        <translation>Delete</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="133"/>
        <source>数据集名称</source>
        <translation>Dataset name</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="140"/>
        <location filename="../app/mixins/project_mixin.py" line="151"/>
        <source>该项目下已存在同名数据集!</source>
        <translation>A dataset with this name already exists in this project!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="142"/>
        <source>创建数据集: {}/{}</source>
        <translation>Create dataset: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="147"/>
        <location filename="../app/mixins/project_mixin.py" line="151"/>
        <source>修改数据集</source>
        <translation>Rename Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="153"/>
        <source>重命名数据集: {} → {}</source>
        <translation>Rename dataset: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="158"/>
        <source>删除数据集</source>
        <translation>Delete Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="159"/>
        <source>确定删除数据集&quot;{}&quot;吗?
</source>
        <translation>Delete dataset &quot;{}&quot;?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="163"/>
        <source>删除数据集: {}/{}</source>
        <translation>Delete dataset: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="182"/>
        <location filename="../app/mixins/project_mixin.py" line="195"/>
        <location filename="../app/mixins/project_mixin.py" line="212"/>
        <source>移动数据集</source>
        <translation>Move Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="183"/>
        <source>是否将&quot;{}&quot;的数据从
{} / {} 移动到 {} / {}?
移动后源数据集将清空.</source>
        <translation>Move the data of &quot;{}&quot; from
{} / {} to {} / {}?
The source dataset will be emptied.</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="192"/>
        <source>移动失败</source>
        <translation>Move Failed</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="196"/>
        <source>已从 {} / {} 移动到 {} / {}</source>
        <translation>Moved from {} / {} to {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="213"/>
        <source>没有可移动到的目标数据集(本项目之外无数据集)</source>
        <translation>No target dataset available (there are no datasets outside this project)</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="217"/>
        <source>选择目标数据集</source>
        <translation>Select Target Dataset</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="221"/>
        <source>选择要将数据移动到的目标数据集:</source>
        <translation>Select the target dataset to move the data into:</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="305"/>
        <source>{}: {}个</source>
        <translation>{}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="307"/>
        <source>数据集移动: {}/{} → {}/{} | 移动图像 {} 张 | 目标标签统计({}类): {}</source>
        <translation>Dataset move: {}/{} → {}/{} | {} images moved | target label stats ({} classes): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="310"/>
        <source>(无)</source>
        <translation>(none)</translation>
    </message>
</context>
<context>
    <name>ProjectSidebar</name>
    <message>
        <location filename="../app/widgets/project_sidebar.py" line="400"/>
        <source>{} 个项目 · {} 个数据集</source>
        <translation>Projects {} · Datasets {}</translation>
    </message>
</context>
<context>
    <name>QueueMixin</name>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="92"/>
        <source>训练队列已启动</source>
        <translation>Training queue started</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="100"/>
        <source>[队列] 已停止</source>
        <translation>[队列] Stopped</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="188"/>
        <source>[队列] 所有任务已执行完毕</source>
        <translation>[队列] All tasks finished</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="196"/>
        <source>[队列] 跳过任务 {}: {}</source>
        <translation>[队列] Skipping task {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="197"/>
        <source>队列任务启动失败 {}: {}</source>
        <translation>Failed to start queue task {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="217"/>
        <source>[队列] 缺少权重 {}, 该项训练会失败</source>
        <translation>[队列] Missing weights {}; this training will fail</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="220"/>
        <source>[队列] 缺少权重 {}, 该项训练时会自行下载</source>
        <translation>[队列] Missing weights {}; this item will download them during training</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="230"/>
        <source>已有训练在进行中</source>
        <translation>A training job is already running</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="235"/>
        <source>[队列] 开始队列第 {}/{} 项: {}</source>
        <translation>[队列] Starting queue item {}/{}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="239"/>
        <source>队列启动任务: {} record={}</source>
        <translation>Queue starting task: {} record={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="277"/>
        <source>训练未完成, 详见日志</source>
        <translation>Training did not finish; see the log</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="304"/>
        <source>[队列] 显存等待超时, 仍继续启动下一个任务</source>
        <translation>[队列] VRAM wait timed out; starting the next task anyway</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="333"/>
        <source>队列 {}</source>
        <translation>Queue {}</translation>
    </message>
</context>
<context>
    <name>StatusText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="16"/>
        <source>等待中</source>
        <translation>Waiting</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="17"/>
        <location filename="../app/widgets/status_style.py" line="24"/>
        <source>训练中</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="18"/>
        <location filename="../app/widgets/status_style.py" line="25"/>
        <source>已完成</source>
        <translation>Finished</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="19"/>
        <location filename="../app/widgets/status_style.py" line="26"/>
        <source>失败</source>
        <translation>Failed</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="20"/>
        <location filename="../app/widgets/status_style.py" line="29"/>
        <source>已跳过</source>
        <translation>Skipped</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="21"/>
        <location filename="../app/widgets/status_style.py" line="27"/>
        <source>已停止</source>
        <translation>Stopped</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="22"/>
        <location filename="../app/widgets/status_style.py" line="30"/>
        <source>已中断</source>
        <translation>Interrupted</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="28"/>
        <source>失败/已停止</source>
        <translation>Failed/Stopped</translation>
    </message>
</context>
<context>
    <name>TaskText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="35"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="36"/>
        <source>分割</source>
        <translation>Segmentation</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="37"/>
        <source>分类</source>
        <translation>Classification</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="38"/>
        <source>异常检测</source>
        <translation>Anomaly Detection</translation>
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
        <location filename="../ui/test_dialog.ui" line="77"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="93"/>
        <source>best.pth</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="105"/>
        <source>mAP50 0.912 · 输入 640 · 规模 n · 训练 2026-09-01 14:22</source>
        <translation>mAP50 0.912 · Input 640 · Scale n · Trained 2026-09-01 14:22</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="126"/>
        <source>数据与设备</source>
        <translation>Data &amp; Device</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="168"/>
        <source>数据</source>
        <translation>Data</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="191"/>
        <source>设备</source>
        <translation>Device</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="221"/>
        <source>测试参数</source>
        <translation>Test Parameters</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="263"/>
        <source>置信度</source>
        <translation>Confidence</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="304"/>
        <source>低于该分数的预测直接丢弃</source>
        <translation>Predictions scoring below this value are discarded</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="320"/>
        <source>IoU 阈值</source>
        <translation>IoU threshold</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="361"/>
        <source>与标注框重合度达标才算正确检出</source>
        <translation>Overlap with the ground-truth box must reach this value to count as a correct detection</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="377"/>
        <source>输出标签文件</source>
        <translation>Write label files</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="409"/>
        <source>会在图像路径下输出标签文件, 可重载数据集查看检出效果</source>
        <translation>Writes label files next to the images; reload the dataset to review the detections</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="461"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="471"/>
        <source>请选择数据集</source>
        <translation>Select datasets</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="515"/>
        <location filename="../app/widgets/test_dialog.py" line="92"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="522"/>
        <source>开始测试</source>
        <translation>Start Test</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="220"/>
        <source>未指定模型</source>
        <translation>No model selected</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="221"/>
        <source>请在模型列表中重新选择一行</source>
        <translation>Select a row in the model list again</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="229"/>
        <source>准确率</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="236"/>
        <source>输入 {}</source>
        <translation>Input {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="238"/>
        <source>规模 {}</source>
        <translation>Scale {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="240"/>
        <source>训练 {}</source>
        <translation>Trained {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="242"/>
        <source>该记录未保存训练指标</source>
        <translation>This record has no saved training metrics</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="245"/>
        <source> · 文件已不存在</source>
        <translation> · file no longer exists</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="271"/>
        <source>请先勾选要测试的数据集</source>
        <translation>Select the datasets to test first</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="283"/>
        <source>{} 个数据集 · {} 张图</source>
        <translation>{} datasets · {} images</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="285"/>
        <source>分类数据集, 统计每张图的判断正确率</source>
        <translation>Classification dataset; measures per-image accuracy</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="287"/>
        <source>已标注, 评估模式: 统计检出率 / 漏检 / 误检</source>
        <translation>Labeled: evaluation mode, measures recall / misses / false positives</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="289"/>
        <source>未标注, 推理模式: 只输出预测标签</source>
        <translation>Unlabeled: inference mode, only writes predicted labels</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="291"/>
        <source>部分已标注, 已标注与未标注的数据集不能一起测</source>
        <translation>Partially labeled; labeled and unlabeled datasets cannot be tested together</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="318"/>
        <source>为判定为不良品的图写 &lt;同名&gt;.json 到图像目录, 多边形标出异常区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Writes &lt;same-name&gt;.json next to the image for parts judged defective, with polygons marking the anomaly regions; the annotation tool can open them directly; any manual annotation already there is overwritten</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="322"/>
        <source>把异常区域写成 labelme json, 便于重载复核</source>
        <translation>Writes the anomaly regions as labelme json for easy reload and review</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="328"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Write &lt;same-name&gt;.json next to each image so the annotation tool can open it directly; existing manual labels there are overwritten</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="345"/>
        <location filename="../app/widgets/test_dialog.py" line="349"/>
        <location filename="../app/widgets/test_dialog.py" line="365"/>
        <location filename="../app/widgets/test_dialog.py" line="371"/>
        <location filename="../app/widgets/test_dialog.py" line="384"/>
        <location filename="../app/widgets/test_dialog.py" line="394"/>
        <location filename="../app/widgets/test_dialog.py" line="400"/>
        <source>测试</source>
        <translation>Test</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="345"/>
        <source>已有测试在进行中</source>
        <translation>A test is already running</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="349"/>
        <source>请至少选择一个数据集</source>
        <translation>Select at least one dataset</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="366"/>
        <source>置信度/iou阈值必须是数字</source>
        <translation>Confidence / IoU threshold must be a number</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="372"/>
        <source>模型文件不存在, 请重新选择</source>
        <translation>The model file does not exist; please select it again</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="385"/>
        <source>数据集 {}/{} 未导入图像</source>
        <translation>Dataset {}/{} has no images imported</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="395"/>
        <source>分类数据集与检测/分割数据集不能同时测试: {}/{}</source>
        <translation>Classification and detection/segmentation datasets cannot be tested together: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="401"/>
        <source>已标注与未标注的数据集不能同时测试: {}/{}</source>
        <translation>Labeled and unlabeled datasets cannot be tested together: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="436"/>
        <source>[test] 启动测试 worker: model={} 数据集={} 图像目录={} device={} cfg={}</source>
        <translation>[test] Starting test worker: model={} dataset={} image dir={} device={} cfg={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="441"/>
        <source>测试准备中...</source>
        <translation>Preparing test...</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="458"/>
        <location filename="../app/widgets/test_dialog.py" line="459"/>
        <source>测试即将开始</source>
        <translation>Test is about to start</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="505"/>
        <source>测试中 {}/{}</source>
        <translation>Testing {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="517"/>
        <source>[test-dialog] 测试完成, ok={}</source>
        <translation>[test-dialog] Test finished, ok={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="525"/>
        <source>测试结果</source>
        <translation>Test Results</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="526"/>
        <source>测试未正常完成</source>
        <translation>The test did not finish normally</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="536"/>
        <source>[test-dialog] 测试失败: {}</source>
        <translation>[test-dialog] Test failed: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="543"/>
        <source>测试失败</source>
        <translation>Test Failed</translation>
    </message>
</context>
<context>
    <name>TestReport</name>
    <message>
        <location filename="../app/train/test_report.py" line="178"/>
        <source>漏 {}</source>
        <translation>Missed {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="180"/>
        <source>误 {}</source>
        <translation>False pos. {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="182"/>
        <source>认错 {}</source>
        <translation>Wrong class {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="193"/>
        <source>(图片无法打开)</source>
        <translation>(image cannot be opened)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="279"/>
        <source>类别认错: {} → {}</source>
        <translation>Wrong class: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="307"/>
        <source>本次验证集没有漏检, 也没有误检.</source>
        <translation>No missed or false detections on this val set.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="310"/>
        <source>明细抽样: 共 {} 张有问题(漏检 {} / 误检 {}), 本报告抽取 {} 张 - 每个类别每种错误最多 {} 张, 按错误数从多到少取</source>
        <translation>Detail sampling: {} problematic images in total (missed {} / false positive {}); this report takes {} - at most {} per error type per class, ordered by error count</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="315"/>
        <source>明细: 共 {} 张有问题(漏检 {} / 误检 {}), 已全部列出</source>
        <translation>Details: {} problematic images in total (missed {} / false positive {}), all listed</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="342"/>
        <source>漏检 GT: 有标注但模型没检出</source>
        <translation>Missed GT: labeled but not detected by the model</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="344"/>
        <source>误检预测: 模型检出但标注里没有</source>
        <translation>False positive: detected by the model but not in the labels</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="346"/>
        <source>正确检出(仅作位置参照)</source>
        <translation>Correct detections (for position reference only)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="348"/>
        <source>类别认错: 位置对但判错类别(GT → 预测)</source>
        <translation>Wrong class: correct position but wrong class (GT → prediction)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="351"/>
        <source>虚线轮廓: 分割 mask / 标注多边形(判定按外接框 IoU)</source>
        <translation>Dashed outline: segmentation mask / annotation polygon (matched by bounding-box IoU)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="449"/>
        <location filename="../app/train/test_report.py" line="1048"/>
        <source>模型评估报告</source>
        <translation>Model Evaluation Report</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="453"/>
        <source>当前训练模型</source>
        <translation>Current training model</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="457"/>
        <location filename="../app/train/test_report.py" line="463"/>
        <source>(未记录)</source>
        <translation>(not recorded)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="462"/>
        <source>数据集 </source>
        <translation>Dataset </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="465"/>
        <source>置信度 {}</source>
        <translation>Confidence {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="485"/>
        <source>测试张数</source>
        <translation>Images tested</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="486"/>
        <location filename="../app/train/test_report.py" line="488"/>
        <source>{} 张</source>
        <translation>{} images</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="487"/>
        <source>有问题的图片</source>
        <translation>Problematic images</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="490"/>
        <source>检出率 (Recall)</source>
        <translation>Recall</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="492"/>
        <source>准确率 (Precision)</source>
        <translation>Accuracy (Precision)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="494"/>
        <source>正确检出</source>
        <translation>Correct detections</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="495"/>
        <source>{} 个</source>
        <translation>{}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="496"/>
        <source>漏检 (该抓没抓)</source>
        <translation>Missed (should have caught it)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="497"/>
        <location filename="../app/train/test_report.py" line="500"/>
        <location filename="../app/train/test_report.py" line="505"/>
        <source>{} 个 / {} 张图</source>
        <translation>{} / {} images</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="499"/>
        <source>误检 (过杀)</source>
        <translation>False pos. (overkill)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="504"/>
        <source>类别认错 (位置对, 类别错)</source>
        <translation>Wrong class (right position, wrong class)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="507"/>
        <source>指标</source>
        <translation>Metric</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="508"/>
        <source>值</source>
        <translation>Value</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="527"/>
        <source>按类别</source>
        <translation>By class</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="530"/>
        <source>类别</source>
        <translation>Class</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="531"/>
        <source>标注</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="532"/>
        <source>正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="533"/>
        <source>漏检</source>
        <translation>Missed</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="534"/>
        <source>误检</source>
        <translation>False pos.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="535"/>
        <source>检出率</source>
        <translation>Recall</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="536"/>
        <source>准确率</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="563"/>
        <source>... 另有 {} 类未列出</source>
        <translation>... {} more classes not listed</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="585"/>
        <source>错误样本明细(仅列漏检 / 误检图片, 正确检出不列出)</source>
        <translation>Error sample details (only missed / false-positive images; correct detections are not listed)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="624"/>
        <source>本轮检出率 {:.0f}%, 准确率 {:.0f}%.</source>
        <translation>This run: recall {:.0f}%, accuracy {:.0f}%.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="627"/>
        <source>没有逐类别统计, 无法定位到具体标签,请先确认标签文件能正常读到.</source>
        <translation>No per-class stats, so the specific labels cannot be located. Check first that the label files can be read.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="651"/>
        <source>漏检分布在</source>
        <translation>Misses are spread across</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="652"/>
        <source>漏检集中在</source>
        <translation>Misses are concentrated in</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="655"/>
        <source>(共 {} 个), 优先补这几类的姿态, 光照样本,并复核标注是否有遗漏.</source>
        <translation>({} in total); add pose and lighting samples for these classes first, and double-check the labels for omissions.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="661"/>
        <source>误检分布在</source>
        <translation>False positives are spread across</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="662"/>
        <source>误检以</source>
        <translation>False positives are mainly</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="663"/>
        <source>({} 个),属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({}), i.e. overkill; add defect-free negative samples and clean up label noise.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="665"/>
        <source>({} 个)为主,属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({} of them), i.e. overkill; add defect-free negative samples and clean up label noise.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="674"/>
        <source>暂无</source>
        <translation>None</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="678"/>
        <source>此外 {} 处位置对但类别判错</source>
        <translation>In addition, {} boxes are correctly located but assigned the wrong class</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="680"/>
        <source>(报告紫框), 属分类能力不足而非定位问题,需补易混淆类别之间的区分性样本.</source>
        <translation>(purple boxes in the report); this is weak classification rather than a localization problem, so add discriminative samples between easily confused classes.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="685"/>
        <source>其中</source>
        <translation>Among them</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="687"/>
        <source>仅 {} 个标注, 样本不足是主要瓶颈, 建议补到 200 个以上.</source>
        <translation>Only {} labels; insufficient samples are the main bottleneck - aim for 200 or more.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="692"/>
        <source>各类样本量差距大(最多 {} / 最少 {}),训练时建议做类别均衡采样.</source>
        <translation>Sample counts vary widely across classes (max {} / min {}); use class-balanced sampling when training.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="697"/>
        <source>把本报告中的漏检, 误检图加入训练集复训,再用同参数复测对比.</source>
        <translation>Add the missed and false-positive images from this report to the train set, retrain, then re-test with the same parameters and compare.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="701"/>
        <source>本轮无漏检, 无误检, 建议用更严的阈值或更难的样本再压一轮, 确认稳定性.</source>
        <translation>No misses and no false positives this run; test again with a stricter threshold or harder samples to confirm stability.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="897"/>
        <source>改进建议</source>
        <translation>Suggestions for Improvement</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="902"/>
        <source>基于本次测试的指标与按类别表现</source>
        <translation>Based on this test&apos;s metrics and per-class performance</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="904"/>
        <source>(模型: {})</source>
        <translation>(model: {})</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="906"/>
        <source>, 建议如下:</source>
        <translation>, suggestions:</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="924"/>
        <source>标红的标签是需要重点关注的类别.</source>
        <translation>Labels in red are the classes that need the most attention.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="929"/>
        <location filename="../app/train/test_report.py" line="955"/>
        <source>第 {} 页</source>
        <translation>Page {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1019"/>
        <source>{}(抽取 {} / 共 {} 张)</source>
        <translation>{}(sampled {} / {} total)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1022"/>
        <source>{}(共 {} 张)</source>
        <translation>{}({} total)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1024"/>
        <source>漏检样本: 有标注但模型没检出</source>
        <translation>Missed samples: labeled but not detected by the model</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1027"/>
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
        <location filename="../ui/test_result.ui" line="58"/>
        <source>图像维度</source>
        <translation>By Image</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="68"/>
        <source>按「张」统计</source>
        <translation>Counted by image</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="125"/>
        <location filename="../ui/test_result.ui" line="181"/>
        <location filename="../ui/test_result.ui" line="237"/>
        <location filename="../ui/test_result.ui" line="293"/>
        <location filename="../ui/test_result.ui" line="417"/>
        <location filename="../ui/test_result.ui" line="473"/>
        <location filename="../ui/test_result.ui" line="529"/>
        <source>0</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="138"/>
        <location filename="../app/train/test_result_dialog.py" line="220"/>
        <location filename="../app/train/test_result_dialog.py" line="252"/>
        <source>测试张数</source>
        <translation>Images tested</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="194"/>
        <source>全对图像</source>
        <translation>All-correct images</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="250"/>
        <source>有漏检图像</source>
        <translation>Images with misses</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="306"/>
        <location filename="../app/train/test_result_dialog.py" line="189"/>
        <source>有误检图像</source>
        <translation>Images with false positives</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="350"/>
        <source>标签维度</source>
        <translation>By Label</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="360"/>
        <source>按「标注框」统计</source>
        <translation>Counted by box</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="430"/>
        <location filename="../ui/test_result.ui" line="639"/>
        <location filename="../app/train/test_result_dialog.py" line="197"/>
        <source>正确检出</source>
        <translation>Correct detections</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="486"/>
        <location filename="../ui/test_result.ui" line="644"/>
        <source>漏检</source>
        <translation>Missed</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="542"/>
        <location filename="../ui/test_result.ui" line="649"/>
        <source>误检</source>
        <translation>False pos.</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="585"/>
        <source>0%</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="598"/>
        <location filename="../ui/test_result.ui" line="659"/>
        <source>准确率</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="629"/>
        <location filename="../app/train/test_result_dialog.py" line="275"/>
        <source>类别</source>
        <translation>Class</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="634"/>
        <source>标注数</source>
        <translation>Boxes</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="654"/>
        <source>检出率</source>
        <translation>Recall</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="679"/>
        <source>每类抽取</source>
        <translation>Per class</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="686"/>
        <source>每个类别的每种错误（漏检 / 误检）最多列出几张图。
报告体积约 120 KB 一张，样本多时调小可以显著减小 PDF；选「全部」则每张有问题的图都列。</source>
        <translation>Maximum images listed per error type (missed / false positive) for each class.
The report is about 120 KB per image; lowering this shrinks the PDF noticeably when there are many samples. Choosing &quot;All&quot; lists every problematic image.</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="690"/>
        <source> 张</source>
        <translation> images</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="693"/>
        <source>全部</source>
        <translation>All</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="722"/>
        <location filename="../app/train/test_result_dialog.py" line="133"/>
        <source>导出 PDF 报告</source>
        <translation>Export PDF Report</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="729"/>
        <location filename="../app/train/test_result_dialog.py" line="79"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="98"/>
        <source>把漏检/误检的图逐张画框导出成 PDF</source>
        <translation>Export a PDF with boxes drawn on every missed / false-positive image</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="101"/>
        <source>异常检测的逐图结果已写成 CSV, 不支持导出画框 PDF</source>
        <translation>Per-image anomaly detection results were written to CSV; boxed PDF export is not supported</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="103"/>
        <source>本次测试没有逐图错误明细, 无法导出</source>
        <translation>This test has no per-image error details; cannot export</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="115"/>
        <source>保存 PDF 报告</source>
        <translation>Save PDF Report</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="116"/>
        <source>PDF 文件 (*.pdf)</source>
        <translation>PDF files (*.pdf)</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="122"/>
        <source>正在生成...</source>
        <translation>Generating...</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="140"/>
        <source>无需导出</source>
        <translation>Nothing to Export</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="141"/>
        <source>本次测试没有漏检也没有误检, 没有内容可写.</source>
        <translation>This test has neither misses nor false positives; nothing to write.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="144"/>
        <source>导出完成</source>
        <translation>Export Complete</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="145"/>
        <source>PDF 报告已保存到:
{}</source>
        <translation>PDF report saved to:
{}</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="149"/>
        <source>导出失败</source>
        <translation>Export Failed</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="176"/>
        <source>按&quot;张&quot;统计 · 检出 1 个即算检出</source>
        <translation>By image · one detected box counts as detected</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="178"/>
        <source> · 有标注 {} 张</source>
        <translation> · {} images with labels</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="182"/>
        <source>检出图像</source>
        <translation>Detected images</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="183"/>
        <location filename="../app/train/test_result_dialog.py" line="198"/>
        <source>检出率 </source>
        <translation>Recall </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="185"/>
        <source>未检出图像</source>
        <translation>Undetected images</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="186"/>
        <source>未检出率 </source>
        <translation>Miss rate </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="190"/>
        <source>误检率 </source>
        <translation>False positive rate </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="195"/>
        <source>按&quot;标注框&quot;统计 · 标注总数 {}</source>
        <translation>By box · {} boxes total</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="218"/>
        <source>按&quot;张&quot;统计 · 每张图判一个类别</source>
        <translation>By image · one class judged per image</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="223"/>
        <location filename="../app/train/test_result_dialog.py" line="255"/>
        <source>判断正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="225"/>
        <location filename="../app/train/test_result_dialog.py" line="257"/>
        <source>判断错误</source>
        <translation>Wrong</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="228"/>
        <location filename="../app/train/test_result_dialog.py" line="276"/>
        <source>精度</source>
        <translation>Accuracy</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="250"/>
        <source>按&quot;张&quot;统计 · 整图判良品/不良品</source>
        <translation>Counted per image · each image judged good or defective</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="275"/>
        <source>总图数</source>
        <translation>Total images</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="275"/>
        <source>正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="276"/>
        <source>错误</source>
        <translation>Wrong</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="235"/>
        <source>整体精度 {:.1f}%, &quot;{}&quot;类错误最多({} 张), 是拉低精度的主要原因.</source>
        <translation>Overall accuracy {:.1f}%. Class &quot;{}&quot; has the most errors ({} images) and is the main reason for the lower accuracy.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="295"/>
        <source>(根目录散图)</source>
        <translation>(loose images in root)</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="298"/>
        <source>本批只有一类样本({}), 定不出判定阈值, 只报告分数; 补一些异常样本重新训练才有可交付的阈值.</source>
        <translation>This batch has only one class ({}), so no decision threshold can be derived; scores are reported only. Add anomalous samples and retrain to get a deliverable threshold.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="300"/>
        <source>良品类别: {}, 判定阈值 {:.4f}.</source>
        <translation>Good class: {}, decision threshold {:.4f}.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="305"/>
        <source> 无漏检, 无误检.</source>
        <translation> No misses, no false positives.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="309"/>
        <source> 漏检 {} 张(不良判成良品), 误检 {} 张(良品判成不良品); &quot;{}&quot;类错误最多({} 张).</source>
        <translation> {} missed (defective judged good), {} false positives (good judged defective); class &quot;{}&quot; has the most errors ({}).</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="341"/>
        <source>整体漏检偏多(漏检 {} 个, 多于误检 {} 个).&quot;{}&quot;类漏检最多({} 个), 是检出率低的主要原因.</source>
        <translation>Misses dominate overall ({} missed vs {} false positives). Class &quot;{}&quot; has the most misses ({}) and is the main reason for the low recall.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="347"/>
        <source>整体误检偏多(误检 {} 个, 多于漏检 {} 个).&quot;{}&quot;类误检最多({} 个), 是准确率低的主要原因.</source>
        <translation>False positives dominate overall ({} vs {} missed). Class &quot;{}&quot; has the most false positives ({}) and is the main reason for the low precision.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="351"/>
        <source>模型表现良好: 无漏检, 无误检.</source>
        <translation>The model performs well: no misses and no false positives.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="353"/>
        <source>另有 {} 处位置对但类别判错(报告里用紫框标出),属分类能力不足, 需补易混淆类别的区分性样本.</source>
        <translation>{} more boxes are correctly located but assigned the wrong class (marked with purple boxes in the report). This points to weak classification ability; add more discriminative samples for easily confused classes.</translation>
    </message>
</context>
<context>
    <name>TestRunner</name>
    <message>
        <location filename="../app/train/test_runner.py" line="282"/>
        <source>覆盖已有标注 {}</source>
        <translation>Overwrite existing labels {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="312"/>
        <source>明细初始化失败: {}</source>
        <translation>Failed to initialize details: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="321"/>
        <source>明细目录创建失败: {}</source>
        <translation>Failed to create the details directory: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="349"/>
        <source>明细写入失败: {}</source>
        <translation>Failed to write details: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="431"/>
        <source>当前安装缺少所需组件, 无法执行测试</source>
        <translation>This installation is missing required components; cannot run the test</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="433"/>
        <source>加载模型: {}</source>
        <translation>Loading model: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="449"/>
        <source>推理已优化: {}</source>
        <translation>Inference optimized: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="465"/>
        <source>测试图片 {} 张</source>
        <translation>{} test images</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="515"/>
        <source>预测失败 {}: {}</source>
        <translation>Prediction failed {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="529"/>
        <source>输出标注失败 {}: {}</source>
        <translation>Failed to write labels {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="584"/>
        <source>WARN 标签目录存在但所有 {} 张图都没读到 GT,请确认标签是 .txt (YOLO) 或 .json (labelme)</source>
        <translation>WARN Label directory exists but no GT was read for any of the {} images; make sure the labels are .txt (YOLO) or .json (labelme)</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="589"/>
        <source>WARN {} 张图缺标签文件</source>
        <translation>WARN {} images have no label file</translation>
    </message>
</context>
<context>
    <name>TestWorker</name>
    <message>
        <location filename="../app/train/test_worker.py" line="80"/>
        <source>run 开始</source>
        <translation>run start</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="93"/>
        <source>启动子进程: {} {}</source>
        <translation>Start subprocess: {} {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="105"/>
        <source>启动子进程失败: {}</source>
        <translation>Failed to start subprocess: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="112"/>
        <source>启动测试进程失败: {}</source>
        <translation>Failed to start the test process: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="114"/>
        <location filename="../app/train/test_worker.py" line="116"/>
        <source>子进程已启动 pid={}</source>
        <translation>Subprocess started pid={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="148"/>
        <source>进入轮询循环</source>
        <translation>Entering poll loop</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="158"/>
        <source>轮询中: 文件={}B 已读{}行 子进程={}</source>
        <translation>Polling: file={}B {} lines read subprocess={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="168"/>
        <source>轮询异常:
</source>
        <translation>Poll error:
</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="176"/>
        <source>轮询结束 rc={}</source>
        <translation>Poll loop finished rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="178"/>
        <source>子进程退出 rc={}</source>
        <translation>Subprocess exited rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="188"/>
        <source>测试未能完成, 详情见日志</source>
        <translation>The test could not be completed, see the log for details</translation>
    </message>
</context>
<context>
    <name>TrainDialog</name>
    <message>
        <location filename="../ui/train.ui" line="14"/>
        <location filename="../ui/train.ui" line="40"/>
        <location filename="../app/train/dialogs.py" line="470"/>
        <source>训练</source>
        <translation>Train</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="50"/>
        <location filename="../ui/train.ui" line="144"/>
        <source>检测</source>
        <translation>Detection</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="93"/>
        <source>模型与数据</source>
        <translation>Model &amp; Data</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="133"/>
        <source>任务类型</source>
        <translation>Task</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="149"/>
        <source>分割</source>
        <translation>Segmentation</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="154"/>
        <source>分类</source>
        <translation>Classification</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="159"/>
        <source>异常检测</source>
        <translation>Anomaly Detection</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="167"/>
        <source>型号</source>
        <translation>Model</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="180"/>
        <location filename="../app/train/dialogs.py" line="665"/>
        <source>训练集</source>
        <translation>Train Set</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="200"/>
        <source>验证集</source>
        <translation>Val Set</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="220"/>
        <source>设备</source>
        <translation>Device</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="233"/>
        <source>架构</source>
        <translation>Architecture</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="266"/>
        <source>训练超参</source>
        <translation>Hyperparameters</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="306"/>
        <location filename="../app/train/dialogs.py" line="546"/>
        <source>轮次</source>
        <translation>Epochs</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="319"/>
        <source>优化器</source>
        <translation>Optimizer</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="332"/>
        <location filename="../app/train/dialogs.py" line="549"/>
        <source>早停</source>
        <translation>Early Stop</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="369"/>
        <source>连续无提升则提前结束，0 为关闭</source>
        <translation>Stop early when no improvement; 0 disables</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="385"/>
        <location filename="../app/train/dialogs.py" line="552"/>
        <source>学习率</source>
        <translation>Learning rate</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="422"/>
        <source>初始学习率，训练中自动衰减</source>
        <translation>Initial LR, decayed while training</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="438"/>
        <location filename="../app/train/dialogs.py" line="544"/>
        <source>批次</source>
        <translation>Batch</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="451"/>
        <location filename="../app/train/dialogs.py" line="548"/>
        <source>图像尺寸</source>
        <translation>Image Size</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="482"/>
        <location filename="../app/train/dialogs.py" line="430"/>
        <location filename="../app/train/dialogs.py" line="434"/>
        <source>32 的倍数</source>
        <translation>multiple of 32</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="498"/>
        <location filename="../app/train/dialogs.py" line="545"/>
        <source>梯度累积</source>
        <translation>Grad Accum</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="535"/>
        <source>显存不足时调大，等效批次 × N</source>
        <translation>Raise when VRAM is tight; effective batch × N</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="551"/>
        <location filename="../app/train/dialogs.py" line="547"/>
        <source>线程数</source>
        <translation>Threads</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="584"/>
        <source>输出</source>
        <translation>Output</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="627"/>
        <source>输出路径</source>
        <translation>Output Path</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="642"/>
        <source>留空则自动按时间生成目录</source>
        <translation>Leave empty to auto-name a timestamped folder</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="655"/>
        <source>选择路径</source>
        <translation>Browse</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="700"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="716"/>
        <location filename="../app/train/dialogs.py" line="631"/>
        <source>请选择训练集与验证集</source>
        <translation>Select a train set and a val set</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="760"/>
        <location filename="../app/train/dialogs.py" line="559"/>
        <source>取消</source>
        <translation>Cancel</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="773"/>
        <location filename="../app/train/dialogs.py" line="1114"/>
        <location filename="../app/train/dialogs.py" line="1123"/>
        <location filename="../app/train/dialogs.py" line="1131"/>
        <location filename="../app/train/dialogs.py" line="1150"/>
        <source>加入队列</source>
        <translation>Add to Queue</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="786"/>
        <location filename="../app/train/dialogs.py" line="1062"/>
        <location filename="../app/train/dialogs.py" line="1072"/>
        <location filename="../app/train/dialogs.py" line="1095"/>
        <source>开始训练</source>
        <translation>Start Training</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="34"/>
        <source>正在检测显卡...</source>
        <translation>Detecting GPUs...</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="146"/>
        <source>数据集&quot;{}&quot;尚未导入图像或路径无效, 请先导入该数据集再训练</source>
        <translation>Dataset &quot;{}&quot; has no images imported or its path is invalid. Import it before training.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="153"/>
        <source>数据集&quot;{}&quot;尚未导入标签或路径无效, 请先导入该数据集再训练</source>
        <translation>Dataset &quot;{}&quot; has no labels imported or its path is invalid. Import it before training.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="182"/>
        <location filename="../app/train/dialogs.py" line="1124"/>
        <source>请先选择输出路径</source>
        <translation>Select an output path first</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="195"/>
        <source>数据集&quot;{}/{}&quot;不是分类数据集(标签格式={}), 无法训练图像分类</source>
        <translation>Dataset &quot;{}/{}&quot; is not a classification dataset (label format={}); cannot train image classification</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="198"/>
        <location filename="../app/train/dialogs.py" line="203"/>
        <location filename="../app/train/dialogs.py" line="1031"/>
        <source>未知</source>
        <translation>Unknown</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="200"/>
        <source>数据集&quot;{}/{}&quot;不是分类数据集(标签格式={}), 无法训练异常检测</source>
        <translation>Dataset &quot;{}/{}&quot; is not a classification dataset (label format={}); cannot train anomaly detection</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="205"/>
        <source>数据集&quot;{}/{}&quot;是分类数据集, 无法训练{}任务</source>
        <translation>Dataset &quot;{}/{}&quot; is a classification dataset; cannot train a {} task</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="219"/>
        <source>请至少选择一个训练集数据集</source>
        <translation>Select at least one train-set dataset</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="221"/>
        <source>请至少选择一个验证集数据集</source>
        <translation>Select at least one val-set dataset</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="270"/>
        <source>未选数据集</source>
        <translation>no dataset selected</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="416"/>
        <source>目标检测推荐图像尺寸: 640(可设为 32 的倍数如 640/672)</source>
        <translation>Recommended image size for detection: 640 (set it to a multiple of 32, e.g. 640/672)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="418"/>
        <source>图像分割推荐尺寸: 636(必须为 12 的倍数, 如 636/648/660)</source>
        <translation>Recommended size for segmentation: 636 (must be a multiple of 12, e.g. 636/648/660)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="420"/>
        <source>CNN 分割推荐尺寸: 640(需为 32 的倍数)</source>
        <translation>Recommended size for CNN segmentation: 640 (must be a multiple of 32)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="422"/>
        <source>图像分类推荐尺寸: 224(小图用 224, 较大图可到 256)</source>
        <translation>Recommended size for classification: 224 (224 for small images, up to 256 for larger ones)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="424"/>
        <source>异常检测推荐尺寸: 256; 缺陷很小时调到 512 更稳, 显存和耗时随之上升</source>
        <translation>Recommended size for anomaly detection: 256; for tiny defects 512 is more reliable, at the cost of VRAM and time</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="431"/>
        <source>12 的倍数</source>
        <translation>multiple of 12</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="432"/>
        <source>建议 224</source>
        <translation>224 suggested</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="435"/>
        <source>建议 256</source>
        <translation>256 recommended</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="641"/>
        <source>训练集 {} 个 · 验证集 {} 个 · 共 {} 张图</source>
        <translation>{} train · {} val · {} images total</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="644"/>
        <source>未选择验证集</source>
        <translation>no val set selected</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="646"/>
        <source>已标注, 可直接训练</source>
        <translation>labeled, ready to train</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="648"/>
        <source>有 {} 个数据集尚未标注</source>
        <translation>{} dataset(s) are not fully labeled</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="662"/>
        <source>请选择验证集</source>
        <translation>Select val datasets</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="744"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>A training job is already running; stop it first</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="835"/>
        <source>异常检测算法自带学习率与优化器, 不需要设置</source>
        <translation>Anomaly detection algorithms bring their own learning rate and optimizer; nothing to set here</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="862"/>
        <source>建库型算法只提取特征建立记忆库, 没有训练轮次</source>
        <translation>Memory-bank algorithms only extract features to build the memory bank; there are no training epochs</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="971"/>
        <source>仅建库</source>
        <translation>Build only</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1001"/>
        <source>请至少选择一个数据集</source>
        <translation>Select at least one dataset</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1005"/>
        <location filename="../app/train/dialogs.py" line="1015"/>
        <source>&quot;{}&quot;不能为空</source>
        <translation>&quot;{}&quot; cannot be empty</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1010"/>
        <source>&quot;{}&quot;必须是整数(当前: {})</source>
        <translation>&quot;{}&quot; must be an integer (currently: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1020"/>
        <source>&quot;{}&quot;必须是数字(当前: {})</source>
        <translation>&quot;{}&quot; must be a number (currently: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1030"/>
        <source>数据集&quot;{}/{}&quot;不是按分类导入的数据集(标签格式={}),无法训练{}</source>
        <translation>Dataset &quot;{}/{}&quot; was not imported as a classification dataset (label format={}); cannot train {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1035"/>
        <source>数据集&quot;{}/{}&quot;是分类数据集,无法训练{}任务</source>
        <translation>Dataset &quot;{}/{}&quot; is a classification dataset; cannot train a {} task</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1042"/>
        <source>选择输出目录</source>
        <translation>Select Output Directory</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1056"/>
        <source>当前安装缺少 CNN 架构所需的组件, 无法训练.
请重新安装软件后再试</source>
        <translation>This installation is missing the components required by the CNN architecture, so training cannot start.
Please reinstall the software and try again</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1063"/>
        <source>当前已有训练在进行中, 请先停止!</source>
        <translation>A training job is already running; stop it first!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1067"/>
        <source>参数校验未通过: {}</source>
        <translation>Parameter validation failed: {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1068"/>
        <location filename="../app/train/dialogs.py" line="1110"/>
        <source>参数校验</source>
        <translation>Parameter Validation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1085"/>
        <source>训练启动失败: {}
{}</source>
        <translation>Training failed to start: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1088"/>
        <source>训练启动失败</source>
        <translation>Training Failed to Start</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1096"/>
        <source>已有训练在进行中, 请先停止!</source>
        <translation>A training job is already running; stop it first!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1098"/>
        <source>开始训练: 任务类型={} 训练集={} 验证集={}</source>
        <translation>Training start: task={} train set={} val set={}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1136"/>
        <source>队列</source>
        <translation>Queue</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1137"/>
        <source>已更新该队列任务的参数</source>
        <translation>Queue task parameters updated</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1143"/>
        <source>加入队列失败</source>
        <translation>Failed to Add to Queue</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1146"/>
        <source>加入训练队列: {} | {}</source>
        <translation>Add to training queue: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1151"/>
        <source>已加入队列(第 {} 个), 可在首页&quot;队列&quot;中查看或启动.</source>
        <translation>Added to the queue (position {}). Review or start it from &quot;Queue&quot; on the home page.</translation>
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
        <location filename="../app/mixins/train_mixin.py" line="148"/>
        <source>进度 | 当前最好 AUROC</source>
        <translation>Progress | Best AUROC so far</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="150"/>
        <source>进度 | 当前最好准确率</source>
        <translation>Progress | best accuracy so far</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="152"/>
        <source>进度 | 当前最好 mAP@50</source>
        <translation>Progress | best mAP@50 so far</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="190"/>
        <source>训练失败(队列模式, 已跳过弹窗): {}</source>
        <translation>Training failed (queue mode, dialog skipped): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="192"/>
        <source>训练失败</source>
        <translation>Training Failed</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="193"/>
        <source>训练过程中发生错误, Err:

{}</source>
        <translation>An error occurred during training, Err:

{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="216"/>
        <source>更新训练指标: record={} 已完成epoch={} map50={} acc={} 类别数={}</source>
        <translation>Update training metrics: record={} epochs done={} map50={} acc={} classes={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="279"/>
        <source>已保存模型记录: {} | {}</source>
        <translation>Model record saved: {} | {}</translation>
    </message>
</context>
<context>
    <name>TrainQueueDialog</name>
    <message>
        <location filename="../ui/train_queue.ui" line="14"/>
        <location filename="../ui/train_queue.ui" line="40"/>
        <location filename="../app/widgets/queue_dialog.py" line="32"/>
        <source>训练队列</source>
        <translation>Training Queue</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="50"/>
        <location filename="../app/widgets/queue_dialog.py" line="121"/>
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
        <location filename="../app/widgets/queue_dialog.py" line="253"/>
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
        <location filename="../app/widgets/queue_dialog.py" line="142"/>
        <source>开始队列</source>
        <translation>Start Queue</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="21"/>
        <source>队列为空, 可在训练界面点&quot;加入队列&quot;添加任务</source>
        <translation>The queue is empty. Click &quot;Add to Queue&quot; in the training dialog to add tasks.</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="111"/>
        <source>运行中</source>
        <translation>Running</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="111"/>
        <source>队列正在串行执行</source>
        <translation>The queue runs tasks one after another</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>待启动</source>
        <translation>Pending</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="114"/>
        <source>有 {} 个任务等待启动</source>
        <translation>{} task(s) waiting to start</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="116"/>
        <source>训练中</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="116"/>
        <source>当前有训练在进行(非队列启动)</source>
        <translation>A training job is running (not started by the queue)</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>已结束</source>
        <translation>Finished</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="119"/>
        <source>没有待执行的任务, 点&quot;重新开始队列&quot;可重跑</source>
        <translation>No pending tasks; click &quot;Restart Queue&quot; to run them again</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="125"/>
        <source>共 {} 个: 等待 {} · 完成 {} · 失败 {}</source>
        <translation>{} total: {} waiting · {} done · {} failed</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="128"/>
        <source>正在训练&quot;{}&quot; · {}</source>
        <translation>Training &quot;{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="131"/>
        <source>下一个: &quot;{}&quot; · {}</source>
        <translation>Next: &quot;{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="144"/>
        <location filename="../app/widgets/queue_dialog.py" line="181"/>
        <source>重新开始队列</source>
        <translation>Restart Queue</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="166"/>
        <location filename="../app/widgets/queue_dialog.py" line="188"/>
        <source>队列</source>
        <translation>Queue</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="167"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>A training job is already running; stop it first</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="176"/>
        <source>{} 个{}</source>
        <translation>{} {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="182"/>
        <source>队列中没有等待中的任务.

待重跑: {}

是否重新入队并开始训练?</source>
        <translation>There are no waiting tasks in the queue.

To re-run: {}

Re-enqueue them and start training?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="189"/>
        <source>队列启动失败, 请查看日志</source>
        <translation>Failed to start the queue; check the log</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="205"/>
        <location filename="../app/widgets/queue_dialog.py" line="209"/>
        <source>移除任务</source>
        <translation>Remove Task</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="206"/>
        <source>训练中的任务不能移除, 请先停止</source>
        <translation>A running task cannot be removed; stop it first</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="210"/>
        <source>确定从队列中移除&quot;{}&quot;吗?</source>
        <translation>Remove &quot;{}&quot; from the queue?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="217"/>
        <source>清理</source>
        <translation>Clear</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="218"/>
        <source>没有已结束的任务</source>
        <translation>No finished tasks</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="220"/>
        <source>[队列] 已清理 {} 个已结束任务</source>
        <translation>[队列] Cleared {} finished task(s)</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="227"/>
        <source>编辑任务</source>
        <translation>Edit Task</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="228"/>
        <source>训练中的任务不能编辑, 请先停止</source>
        <translation>A running task cannot be edited; stop it first</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="244"/>
        <source>重新入队</source>
        <translation>Re-enqueue</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="246"/>
        <location filename="../app/widgets/queue_dialog.py" line="267"/>
        <source>打开输出目录</source>
        <translation>Open Output Directory</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="248"/>
        <source>在模型界面查看</source>
        <translation>View in Model Manager</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="268"/>
        <source>目录不存在: {}</source>
        <translation>Directory does not exist: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="269"/>
        <source>未设置</source>
        <translation>Not set</translation>
    </message>
</context>
<context>
    <name>TrainRunner</name>
    <message>
        <location filename="../app/train/train_runner.py" line="78"/>
        <location filename="../app/train/yolo_train_runner.py" line="171"/>
        <source>输出路径: {}</source>
        <translation>Output path: {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="79"/>
        <location filename="../app/train/yolo_train_runner.py" line="172"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Run output directory (timestamp): {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="81"/>
        <source>训练配置文件已保存 → {}</source>
        <translation>Training config saved → {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="103"/>
        <source>分割模型 resolution 已自动取整: {} → {} (block={})</source>
        <translation>Segmentation model resolution rounded automatically: {} → {} (block={})</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="105"/>
        <location filename="../app/train/yolo_train_runner.py" line="209"/>
        <source>使用模型 {} device={} epochs={} batch={} resolution={}</source>
        <translation>Using model {} device={} epochs={} batch={} resolution={}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="174"/>
        <location filename="../app/train/yolo_train_runner.py" line="237"/>
        <source>训练完成</source>
        <translation>Training complete</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="183"/>
        <location filename="../app/train/yolo_train_runner.py" line="244"/>
        <source>生成类别文件: {}</source>
        <translation>Writing class file: {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="90"/>
        <location filename="../app/train/yolo_train_runner.py" line="178"/>
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
        <location filename="../app/core/utils.py" line="57"/>
        <location filename="../app/core/utils.py" line="69"/>
        <source>{}秒</source>
        <translation>{}s</translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="63"/>
        <source>{}天</source>
        <translation>{}d </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="65"/>
        <source>{}小时</source>
        <translation>{}h </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="67"/>
        <source>{}分</source>
        <translation>{}m </translation>
    </message>
</context>
<context>
    <name>_ModelRow</name>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="113"/>
        <source>已就绪</source>
        <translation>Ready</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="119"/>
        <source>未下载</source>
        <translation>Not downloaded</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="124"/>
        <source>校验中...</source>
        <translation>Verifying...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="140"/>
        <source>失败</source>
        <translation>Failed</translation>
    </message>
</context>
<context>
    <name>_TrainStartDialog</name>
    <message>
        <location filename="../app/train/dialogs.py" line="280"/>
        <source>训练即将开始</source>
        <translation>Training is about to start</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="290"/>
        <location filename="../app/train/dialogs.py" line="303"/>
        <source>确认({})</source>
        <translation>OK ({})</translation>
    </message>
</context>
<context>
    <name>addLabelDialog</name>
    <message>
        <location filename="../ui/add_label.ui" line="14"/>
        <source>Dialog</source>
        <translation>Add Label</translation>
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
        <translation>Add Label</translation>
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
        <location filename="../ui/annotation.ui" line="90"/>
        <source>标签列表</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="113"/>
        <source>添加标签</source>
        <translation>Add Label</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="116"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="160"/>
        <source>标注信息</source>
        <translation>Annotations</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="203"/>
        <source>图像信息</source>
        <translation>Image Info</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="230"/>
        <source>剪切板</source>
        <translation>Clipboard</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="295"/>
        <source>上一张(A)</source>
        <translation>Prev (A)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="302"/>
        <source>下一张(D)</source>
        <translation>Next (D)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="352"/>
        <source>标注参数</source>
        <translation>Annotation Params</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="364"/>
        <source>角度范围</source>
        <translation>Angle Range</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="378"/>
        <source>~</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="412"/>
        <source>融合强度</source>
        <translation>Blend Strength</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="446"/>
        <source>亮度调节</source>
        <translation>Brightness</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="480"/>
        <source>填充颜色</source>
        <translation>Fill Color</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="487"/>
        <source>点击打开取色器, 选任意颜色</source>
        <translation>Click to open the color picker</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="500"/>
        <source>支持 #RRGGBB / #RGB / 255,255,255 / black / 白 等写法, 也可以点左边色块打开取色器</source>
        <translation>Accepts #RRGGBB / #RGB / 255,255,255 / black / white — or click the swatch on the left to pick a color</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="503"/>
        <source>#RRGGBB</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="510"/>
        <source>自定义颜色</source>
        <translation>Custom Color</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="537"/>
        <source>常用色</source>
        <translation>Presets</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="568"/>
        <source>恢复默认</source>
        <translation>Reset</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="588"/>
        <source>完成</source>
        <translation>Done</translation>
    </message>
</context>
</TS>
