<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="de_DE">
<context>
    <name>AdCommon</name>
    <message>
        <location filename="../app/train/ad_common.py" line="102"/>
        <source>找不到可写的纯英文暂存目录(异常检测的底层库不支持中文路径), 请把输出路径改到纯英文目录下</source>
        <translation>Kein beschreibbares temporäres Verzeichnis mit reiner ASCII-Benennung gefunden (die Bibliothek der Anomalieerkennung unterstützt keine Nicht-ASCII-Pfade); bitte den Ausgabepfad auf ein reines ASCII-Verzeichnis ändern</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="164"/>
        <location filename="../app/train/ad_common.py" line="689"/>
        <source>(根目录散图)</source>
        <translation>(lose Bilder im Wurzelordner)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="187"/>
        <source>数据集里没找到图像, 请先导入数据</source>
        <translation>Im Datensatz wurden keine Bilder gefunden, bitte zuerst Daten importieren</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="192"/>
        <source>无法从类别名判断哪个是正常品, 请把放良品图的那个文件夹改名为 {} 之一; 现有类别: {}</source>
        <translation>Aus den Klassennamen lässt sich nicht erkennen, welche Klasse die Gutteile enthält; den Ordner mit den Gutbildern in einen der Namen {} umbenennen; vorhandene Klassen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="198"/>
        <source>训练集里没有图像</source>
        <translation>Das Trainingsset enthält keine Bilder</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="205"/>
        <source>训练集里只有&quot;{}&quot;一类, 而良品类是&quot;{}&quot;; 请把良品图所在的类别文件夹挂到训练集上</source>
        <translation>Das Trainingsset enthält nur die Klasse „{}“, die Gutklasse ist jedoch „{}“; den Klassenordner mit den Gutbildern an das Trainingsset anhängen</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="215"/>
        <source>训练集里既没有&quot;{}&quot;类、又不止一类, 无法确定拿哪批图建库; 现有类别: {}</source>
        <translation>Im Trainingsset fehlt die Klasse „{}“ und es gibt mehr als eine Klasse, daher ist unklar, welche Bilder für die Speicherbank verwendet werden sollen; vorhandene Klassen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="257"/>
        <source>训练集根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>Im Wurzelordner des Trainingssets liegen sowohl lose Bilder als auch Unterordner, daher ist die Klasse der losen Bilder unklar; bitte alle in einen gemeinsamen Klassenordner legen</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="291"/>
        <source>没有找到任何图像, 请检查数据集</source>
        <translation>Keine Bilder gefunden, bitte den Datensatz prüfen</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="293"/>
        <source>根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>Im Wurzelordner liegen sowohl lose Bilder als auch Unterordner, daher ist die Klasse der losen Bilder unklar; bitte alle in einen gemeinsamen Klassenordner legen</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="298"/>
        <source>无法判断哪个类别是良品, 现有类别: {}.
请把良品图放在名为 {} 一类的子文件夹里, 或按训练时的方式重新导入数据集</source>
        <translation>Es lässt sich nicht feststellen, welche Klasse die Gutteile enthält; vorhandene Klassen: {}.
Bitte die Gutbilder in einen Unterordner mit einem der Namen {} legen oder den Datensatz wie beim Training erneut importieren</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="452"/>
        <source>未知的异常检测算法: {}</source>
        <translation>Unbekannter Anomalieerkennungs-Algorithmus: {}</translation>
    </message>
</context>
<context>
    <name>AdTestRunner</name>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="46"/>
        <source>缺少测试依赖: {}</source>
        <translation>Test-Abhängigkeiten fehlen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="263"/>
        <source>图像</source>
        <translation>Bild</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="264"/>
        <source>类别</source>
        <translation>Klasse</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="265"/>
        <source>真值</source>
        <translation>Ground Truth</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="266"/>
        <source>判定</source>
        <translation>Urteil</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="267"/>
        <source>分数</source>
        <translation>Wert</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="268"/>
        <source>阈值</source>
        <translation>Schwelle</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="269"/>
        <source>是否正确</source>
        <translation>Korrekt</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="284"/>
        <source>是</source>
        <translation>Ja</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="285"/>
        <source>否</source>
        <translation>Nein</translation>
    </message>
</context>
<context>
    <name>AdTrainRunner</name>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="48"/>
        <source>缺少训练依赖: {}</source>
        <translation>Trainings-Abhängigkeiten fehlen: {}</translation>
    </message>
</context>
<context>
    <name>AddLabelDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="458"/>
        <source>添加标签</source>
        <translation>Label hinzufügen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="472"/>
        <source>编辑标签</source>
        <translation>Label bearbeiten</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="504"/>
        <source>标签名称, 多个用逗号分隔</source>
        <translation>Labelnamen, mehrere durch Komma trennen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="506"/>
        <source>导入</source>
        <translation>Importieren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="513"/>
        <source>选择数据集...</source>
        <translation>Datensatz wählen...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="536"/>
        <location filename="../app/annotation/annotation_dialog.py" line="541"/>
        <source>导入标签</source>
        <translation>Labels importieren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="537"/>
        <source>请先选择一个数据集</source>
        <translation>Zuerst einen Datensatz auswählen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="542"/>
        <source>数据集&quot;{}&quot;还没有标签</source>
        <translation>Datensatz „{}&quot; hat noch keine Labels</translation>
    </message>
</context>
<context>
    <name>AnnotationDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="295"/>
        <source>复制</source>
        <translation>Kopieren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="297"/>
        <source>填充</source>
        <translation>Füllen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="307"/>
        <source>粘贴</source>
        <translation>Einfügen</translation>
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
        <translation>Rechteck</translation>
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
        <translation>Label-Liste</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="718"/>
        <source>标注信息</source>
        <translation>Annotationen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="719"/>
        <source>上一张</source>
        <translation>Zurück</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="720"/>
        <source>下一张</source>
        <translation>Weiter</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="755"/>
        <source>只在选中的多边形框内生效; A/D 切图或 Ctrl+S 才写盘</source>
        <translation>Wirkt nur im ausgewählten Polygon; gespeichert wird erst bei A/D-Bildwechsel oder Ctrl+S</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="793"/>
        <source>显示标注</source>
        <translation>Annotationen anzeigen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="880"/>
        <source>先在画布上点选一个多边形</source>
        <translation>Zuerst ein Polygon auf der Zeichenfläche auswählen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="883"/>
        <source>亮度调节只对多边形有效</source>
        <translation>Helligkeitsanpassung wirkt nur auf Polygone</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1159"/>
        <source>    类别: {}</source>
        <translation>    Klasse: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1186"/>
        <source>删除本地文件</source>
        <translation>Lokale Datei löschen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1187"/>
        <source>取消</source>
        <translation>Abbrechen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1189"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1199"/>
        <source>删除图像</source>
        <translation>Bild löschen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1190"/>
        <source>是否删除当前图像?

{}</source>
        <translation>Aktuelles Bild löschen?

{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1194"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>Bild und gleichnamige Labeldatei werden von der Festplatte gelöscht. Nicht wiederherstellbar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1200"/>
        <source>无法访问主窗口, 删除失败</source>
        <translation>Kein Zugriff auf das Hauptfenster; Löschen fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1214"/>
        <source>(无图像)</source>
        <translation>(kein Bild)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1278"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1885"/>
        <source>添加标签</source>
        <translation>Label hinzufügen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1279"/>
        <source>请先添加标签(点击&quot;+&quot;)</source>
        <translation>Zuerst ein Label hinzufügen (auf „+&quot; klicken)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1391"/>
        <source>剪切板  {}/{}</source>
        <translation>Zwischenablage  {}/{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1416"/>
        <source>第 {} 个模板  {}x{}
左键选中用于粘贴, 右键 删除/导入/导出/清空</source>
        <translation>Vorlage {}  {}x{}
Linksklick zum Auswählen fürs Einfügen; Rechtsklick: Löschen / Importieren / Exportieren / Leeren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1448"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1697"/>
        <source>删除</source>
        <translation>Löschen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1451"/>
        <source>导入</source>
        <translation>Importieren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1452"/>
        <source>导出</source>
        <translation>Exportieren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1454"/>
        <source>清空</source>
        <translation>Leeren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1482"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1509"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1513"/>
        <source>导出剪切板</source>
        <translation>Zwischenablage exportieren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1483"/>
        <source>剪切板是空的, 没有可导出的模板</source>
        <translation>Die Zwischenablage ist leer; keine Vorlagen zum Exportieren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1485"/>
        <source>选择导出目录</source>
        <translation>Exportordner wählen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1510"/>
        <source>导出中断: {}
(已写出 {} 个)</source>
        <translation>Export abgebrochen: {}
({} geschrieben)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1514"/>
        <source>已导出 {} 个模板(png + 同名 json)到:
{}</source>
        <translation>{} Vorlage(n) exportiert (png + gleichnamige json) nach:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1518"/>
        <source>选择导入目录</source>
        <translation>Importordner wählen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1525"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1529"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1563"/>
        <source>导入剪切板</source>
        <translation>Zwischenablage importieren</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1526"/>
        <source>读取目录失败: {}</source>
        <translation>Ordner konnte nicht gelesen werden: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1530"/>
        <source>这个目录里没有 png 文件</source>
        <translation>In diesem Ordner gibt es keine png-Dateien</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1558"/>
        <source>已导入 {} 个模板到剪切板</source>
        <translation>{} Vorlage(n) in die Zwischenablage importiert</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1560"/>
        <source>
其中 {} 个没有同名 json, 按矩形导入</source>
        <translation>
Davon {} ohne gleichnamige json, als Rechteck importiert</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1562"/>
        <source>
{} 个文件读不出来, 已跳过</source>
        <translation>
{} Datei(en) nicht lesbar, übersprungen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1638"/>
        <source>修改类别</source>
        <translation>Klasse ändern</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1639"/>
        <source>移动图像文件失败:
{}</source>
        <translation>Bilddatei konnte nicht verschoben werden:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1696"/>
        <source>编辑</source>
        <translation>Bearbeiten</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1755"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1814"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1821"/>
        <location filename="../app/annotation/annotation_dialog.py" line="1830"/>
        <source>删除标签</source>
        <translation>Label löschen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1755"/>
        <source>正在统计标注文件...</source>
        <translation>Labeldateien werden gezählt...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1815"/>
        <source>标签&quot;{}&quot;已有 {} 处标注, 删除后这些标注将被一并删除且不可恢复.
确定删除吗?</source>
        <translation>Label „{}&quot; hat {} Annotation(en). Beim Löschen werden sie mit entfernt und können nicht wiederhergestellt werden.
Trotzdem löschen?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1822"/>
        <source>确定删除标签&quot;{}&quot;吗?</source>
        <translation>Label „{}&quot; löschen?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1830"/>
        <source>正在清理标注文件...</source>
        <translation>Labeldateien werden bereinigt...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1886"/>
        <source>标签名称不能为空</source>
        <translation>Labelname darf nicht leer sein</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1941"/>
        <source>{} 个顶点</source>
        <translation>{} Eckpunkte</translation>
    </message>
</context>
<context>
    <name>App</name>
    <message>
        <location filename="../app/main_window.py" line="43"/>
        <source>软件启动</source>
        <translation>Software startet</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="46"/>
        <source>软件退出</source>
        <translation>Software beendet</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="48"/>
        <source>软件退出前停止训练</source>
        <translation>Training vor dem Beenden stoppen</translation>
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
        <translation>Projekte</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="193"/>
        <source>添加项目</source>
        <translation>Projekt hinzufügen</translation>
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
        <translation>Training stoppen</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="372"/>
        <source>剩余时间:</source>
        <translation>Restzeit:</translation>
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
        <translation>Bearbeiten</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="406"/>
        <source>删除</source>
        <translation>Löschen</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="413"/>
        <source>统计</source>
        <translation>Statistik</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="420"/>
        <source>训练</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="427"/>
        <source>模型</source>
        <translation>Modelle</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="434"/>
        <location filename="../app/mixins/queue_mixin.py" line="334"/>
        <source>队列</source>
        <translation>Warteschlange</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="441"/>
        <source>日志</source>
        <translation>Protokoll</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="460"/>
        <source>界面语言</source>
        <translation>Oberflächensprache</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="551"/>
        <source>上一页</source>
        <translation>Zurück</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="580"/>
        <source>下一页</source>
        <translation>Weiter</translation>
    </message>
</context>
<context>
    <name>Charts</name>
    <message>
        <location filename="../app/widgets/charts.py" line="11"/>
        <source>暂无标注</source>
        <translation>Keine Annotationen</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="12"/>
        <source>标签</source>
        <translation>Label</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="13"/>
        <source>标签数量</source>
        <translation>Labelanzahl</translation>
    </message>
</context>
<context>
    <name>ClassifyTestRunner</name>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="33"/>
        <source>缺少测试依赖: {}</source>
        <translation>Test-Abhängigkeiten fehlen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="85"/>
        <source>加载分类模型: {}</source>
        <translation>Klassifizierungsmodell laden: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="110"/>
        <source>测试图片 {} 张</source>
        <translation>{} Testbilder</translation>
    </message>
</context>
<context>
    <name>ClassifyTrainRunner</name>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="40"/>
        <source>缺少训练依赖: {}</source>
        <translation>Trainings-Abhängigkeiten fehlen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="132"/>
        <source>输出路径: {}</source>
        <translation>Ausgabepfad: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="133"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Ausgabeverzeichnis dieses Trainings (Zeitstempel): {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="149"/>
        <source>分类训练: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</source>
        <translation>Klassifizierungstraining: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="158"/>
        <source>数据准备: train={} 张, val={} 张</source>
        <translation>Datenvorbereitung: train={} Bilder, val={} Bilder</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="160"/>
        <source>训练集无图像, 请检查数据集</source>
        <translation>Trainingsset ohne Bilder, bitte Datensatz prüfen</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="162"/>
        <source>验证集无图像, 请检查数据集</source>
        <translation>Validierungsset ohne Bilder, bitte Datensatz prüfen</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="187"/>
        <source>未从数据集中解析到任何类别(子文件夹),无法训练图像分类</source>
        <translation>Keine Klassen (Unterordner) im Datensatz gefunden, Bildklassifizierung nicht möglich</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="197"/>
        <source>数据集: train={} val={} 类别({})={}</source>
        <translation>Datensatz: train={} val={} Klassen({})={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="284"/>
        <source>早停触发: 连续 {} 个 epoch 精度无提升</source>
        <translation>Early Stopping ausgelöst: {} Epochen in Folge ohne Genauigkeitsverbesserung</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="289"/>
        <source>训练完成 best_acc={:.4f}</source>
        <translation>Training abgeschlossen best_acc={:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="297"/>
        <source>生成类别文件: {}</source>
        <translation>Klassendatei erzeugen: {}</translation>
    </message>
</context>
<context>
    <name>ColorPickerDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="2250"/>
        <source>选择颜色</source>
        <translation>Farbe wählen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="2262"/>
        <source>十六进制:</source>
        <translation>Hex:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="2283"/>
        <source>基本颜色:</source>
        <translation>Grundfarben:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="2295"/>
        <source>自定义 RGB:</source>
        <translation>Eigenes RGB:</translation>
    </message>
</context>
<context>
    <name>DataBase</name>
    <message>
        <location filename="../app/core/db.py" line="479"/>
        <source>已删除图像记录解析失败, 跳过迁移以免覆盖丢失 ({}): {}</source>
        <translation>Analyse gelöschter Bildeinträge fehlgeschlagen, Migration übersprungen, um Datenverlust zu vermeiden ({}): {}</translation>
    </message>
</context>
<context>
    <name>DataPrep</name>
    <message>
        <location filename="../app/train/data_prep.py" line="189"/>
        <source>解析到类别 {} 个: {}</source>
        <translation>{} Klassen erkannt: {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="209"/>
        <source>复制数据集 {}: 图像 {} 张, 标签 {} 个 → {}</source>
        <translation>Datensatz kopieren {}: {} Bilder, {} Labels → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="296"/>
        <source>合并 {} 数据集 → {} ({} 个文件)</source>
        <translation>{} Datensätze zusammenführen → {} ({} Dateien)</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="313"/>
        <source>生成 data.yaml → {}</source>
        <translation>data.yaml erzeugen → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="326"/>
        <source>未从数据集中解析到任何标签类别, 请检查标签文件</source>
        <translation>Keine Label-Klassen aus dem Datensatz gelesen, bitte Label-Dateien prüfen</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="333"/>
        <source>数据准备完成: {} 个类别, 输出目录 {}</source>
        <translation>Datenvorbereitung abgeschlossen: {} Klassen, Ausgabeverzeichnis {}</translation>
    </message>
</context>
<context>
    <name>DatasetViewMixin</name>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="246"/>
        <source>删除全部未标注图像({} 张)</source>
        <translation>Alle nicht annotierten Bilder löschen ({} Bilder)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="252"/>
        <source>删除所选图像({} 张)</source>
        <translation>Ausgewählte Bilder löschen ({} Bilder)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="349"/>
        <source>重载跳过: 数据集 {}/{} 无图像目录</source>
        <translation>Neuladen übersprungen: Datensatz {}/{} ohne Bildordner</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="350"/>
        <source>重载</source>
        <translation>Neu laden</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="351"/>
        <source>该数据集还没有图像目录, 请先右键&quot;导入&quot;</source>
        <translation>Dieser Datensatz hat noch keinen Bildordner; zuerst per Rechtsklick „Importieren&quot;</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="355"/>
        <source>重载跳过: 数据集 {}/{} 正在载入</source>
        <translation>Neuladen übersprungen: Datensatz {}/{} wird geladen</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="357"/>
        <source>重载数据集: {}/{}</source>
        <translation>Datensatz neu laden: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="802"/>
        <source>第 {} / {} 页</source>
        <translation>Seite {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="806"/>
        <source>第 {}/{} 页 · 共 {} 个</source>
        <translation>Seite {}/{} · {} Einträge</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="808"/>
        <source>第 {}/{} 页 · 共 {} 张</source>
        <translation>Seite {}/{} · {} Bilder</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="817"/>
        <source>暂无数据</source>
        <translation>Keine Daten</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="854"/>
        <source>开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}</source>
        <translation>Import starten: {}/{} | Bildpfad={} | Labelpfad={} | Format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="855"/>
        <location filename="../app/mixins/dataset_view_mixin.py" line="925"/>
        <source>(无)</source>
        <translation>(keine)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="920"/>
        <source>{}: {}个</source>
        <translation>{}: {} Stück</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="922"/>
        <source>数据集导入完成: {}/{} | 图像 {} 张, 已标注 {} 张 | 标签({}类): {}</source>
        <translation>Datensatzimport abgeschlossen: {}/{} | {} Bilder, {} annotiert | Labels ({} Klassen): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="966"/>
        <source>数据集 {}/{} 未导入, 右键&quot;导入&quot;选择图像与标签目录</source>
        <translation>Datensatz {}/{} nicht importiert, per Rechtsklick „Importieren&quot; Bild- und Labelordner wählen</translation>
    </message>
</context>
<context>
    <name>Dialog</name>
    <message>
        <location filename="../ui/dataset_properties.ui" line="14"/>
        <source>数据集属性</source>
        <translation>Datensatz-Eigenschaften</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="30"/>
        <source>选择数据:</source>
        <translation>Datensatz wählen:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="53"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="77"/>
        <source>图像路径:</source>
        <translation>Bildpfad:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="98"/>
        <source>标签路径:</source>
        <translation>Labelpfad:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="119"/>
        <source>标签分布:</source>
        <translation>Labelverteilung:</translation>
    </message>
    <message>
        <location filename="../ui/edit_label.ui" line="14"/>
        <source>类别修改</source>
        <translation>Klasse ändern</translation>
    </message>
    <message>
        <location filename="../ui/edit_label.ui" line="22"/>
        <source>类别</source>
        <translation>Klasse</translation>
    </message>
    <message>
        <location filename="../ui/edit_label.ui" line="42"/>
        <source>批量修改为</source>
        <translation>Alle umbenennen in</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="14"/>
        <source>导出</source>
        <translation>Exportieren</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="36"/>
        <source>请选择导出路径</source>
        <translation>Exportpfad wählen</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="90"/>
        <source>导出格式</source>
        <translation>Exportformat</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="106"/>
        <source>labelme 格式</source>
        <translation>labelme-Format</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="119"/>
        <source>yolo 格式</source>
        <translation>yolo-Format</translation>
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
        <translation>Abbrechen</translation>
    </message>
</context>
<context>
    <name>ImportData</name>
    <message>
        <location filename="../ui/import_data.ui" line="14"/>
        <source>导入数据</source>
        <translation>Daten importieren</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="33"/>
        <source>图像路径</source>
        <translation>Bildpfad</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="73"/>
        <source>标签路径</source>
        <translation>Labelpfad</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="113"/>
        <source>标签格式:</source>
        <translation>Labelformat:</translation>
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
        <translation>Als Klassifizierung importieren (Unterordner)</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="179"/>
        <source>提示信息</source>
        <translation>Hinweis</translation>
    </message>
</context>
<context>
    <name>ImportExportMixin</name>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="58"/>
        <source>导入数据 - {} / {}</source>
        <translation>Daten importieren - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="65"/>
        <location filename="../app/mixins/import_export_mixin.py" line="165"/>
        <source>请选择图像文件夹</source>
        <translation>Bildordner wählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="141"/>
        <source>请选择分类根目录(子文件夹名=类别)</source>
        <translation>Klassifizierungs-Wurzelordner wählen (Unterordnername = Klasse)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="154"/>
        <source>(根目录)</source>
        <translation>(Wurzelordner)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="156"/>
        <source>所选文件夹下无分类子文件夹或图像</source>
        <translation>Keine Klassen-Unterordner oder Bilder im gewählten Ordner</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="158"/>
        <source>{}: {}张</source>
        <translation>{}: {} Bilder</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="160"/>
        <source>检测到 {} 类: {}</source>
        <translation>{} Klassen erkannt: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="79"/>
        <source>所选文件夹无图像</source>
        <translation>Keine Bilder im gewählten Ordner</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="82"/>
        <source>共 {} 张图像, 已标注 {} 张</source>
        <translation>{} Bilder, {} annotiert</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="98"/>
        <source>(检测到 {} 张 {} 标签, 请切换上方格式为&quot;{}&quot;)</source>
        <translation>({} {} Labels erkannt; oben das Format auf „{}&quot; umstellen)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="102"/>
        <source>共 {} 张图像, 已标注 0 张 {}</source>
        <translation>{} Bilder, 0 annotiert {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="104"/>
        <source>共 {} 张图像(标签目录无匹配文件)</source>
        <translation>{} Bilder (keine passenden Dateien im Labelordner)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="171"/>
        <source>选择文件夹</source>
        <translation>Ordner wählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="211"/>
        <source>分类根目录(子文件夹名=类别)</source>
        <translation>Klassifizierungs-Wurzel (Unterordnername = Klasse)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="211"/>
        <source>图像路径</source>
        <translation>Bildpfad</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="233"/>
        <location filename="../app/mixins/import_export_mixin.py" line="236"/>
        <source>导入数据</source>
        <translation>Daten importieren</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="233"/>
        <source>请先选择有效的图像文件夹</source>
        <translation>Zuerst einen gültigen Bildordner wählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="236"/>
        <source>标签路径无效</source>
        <translation>Labelpfad ungültig</translation>
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
        <translation>Exportieren</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="297"/>
        <source>请先在左侧选中要导出的数据集</source>
        <translation>Zuerst links den zu exportierenden Datensatz auswählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="322"/>
        <source>请先选择导出保存位置</source>
        <translation>Zuerst den Speicherort für den Export wählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="333"/>
        <source>开始导出: 项目={} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>Export starten: Projekt={} | Quellpfad={} | Speicherpfad={} | Format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="339"/>
        <source>正在导出项目...</source>
        <translation>Projekt wird exportiert...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="350"/>
        <source>项目&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>Projekt „{}&quot; exportiert: {} Bilder kopiert
Ort: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="352"/>
        <source>导出项目完成: {} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>Projektexport abgeschlossen: {} | {} Bilder | Labels({}) | Format={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="358"/>
        <source>开始导出: 数据集={}/{} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>Export starten: Datensatz={}/{} | Quellpfad={} | Speicherpfad={} | Format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="362"/>
        <source>正在导出数据集...</source>
        <translation>Datensatz wird exportiert...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="372"/>
        <source>数据集&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>Datensatz „{}&quot; exportiert: {} Bilder kopiert
Ort: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="375"/>
        <source>导出数据集完成: {}/{} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>Datensatzexport abgeschlossen: {}/{} | {} Bilder | Labels({}) | Format={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="380"/>
        <source>导出失败: 项目={} 数据集={} | {}</source>
        <translation>Export fehlgeschlagen: Projekt={} Datensatz={} | {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="381"/>
        <source>(整个项目)</source>
        <translation>(gesamtes Projekt)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="382"/>
        <source>导出失败</source>
        <translation>Export fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="385"/>
        <source>选择导出保存位置</source>
        <translation>Ziel für Export wählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="411"/>
        <source>{} =&gt; 标签:{}</source>
        <translation>{} =&gt; Labels:{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="412"/>
        <location filename="../app/mixins/import_export_mixin.py" line="413"/>
        <source>(无)</source>
        <translation>(keine)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="420"/>
        <source>(无标签)</source>
        <translation>(keine Labels)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="463"/>
        <source>正在导出: {}</source>
        <translation>Export läuft: {}</translation>
    </message>
</context>
<context>
    <name>ImportTask</name>
    <message>
        <location filename="../app/tasks/import_task.py" line="113"/>
        <source>导入跳过 {}: {}</source>
        <translation>Import übersprungen {}: {}</translation>
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
        <translation>Nicht annotiert</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="181"/>
        <location filename="../app/mixins/label_mixin.py" line="186"/>
        <location filename="../app/mixins/label_mixin.py" line="203"/>
        <source>重命名</source>
        <translation>Umbenennen</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="181"/>
        <location filename="../app/mixins/label_mixin.py" line="434"/>
        <source>请先在左侧选中一个数据集</source>
        <translation>Zuerst links einen Datensatz auswählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="187"/>
        <source>请先在筛选下拉框中选择要重命名的标签</source>
        <translation>Zuerst im Filter-Dropdown das umzubenennende Label wählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="190"/>
        <source>类别修改</source>
        <translation>Klasse ändern</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="203"/>
        <source>标签名称不能为空</source>
        <translation>Labelname darf nicht leer sein</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="212"/>
        <source>合并标签</source>
        <translation>Labels zusammenführen</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="213"/>
        <source>标签&quot;{}&quot;已存在.
确定把&quot;{}&quot;的所有标注合并到&quot;{}&quot;吗?
此操作会改写数据集源标签文件, 且不可恢复.</source>
        <translation>Label „{}&quot; existiert bereits.
Alle Annotationen von „{}&quot; in „{}&quot; zusammenführen?
Dies überschreibt die Quell-Labeldateien des Datensatzes und kann nicht rückgängig gemacht werden.</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="268"/>
        <source>合并标签: {} → {} ({}/{}) | 启动后台文件合并, 完成后输出统计</source>
        <translation>Labels zusammenführen: {} → {} ({}/{}) | Hintergrund-Zusammenführung gestartet, Statistik folgt nach Abschluss</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="274"/>
        <source>重命名标签: {} → {} ({}/{})</source>
        <translation>Label umbenennen: {} → {} ({}/{})</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="346"/>
        <source>{}: {}个</source>
        <translation>{}: {} Stück</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="349"/>
        <source>删除标签完成: {} | 修改 {} 个标签文件 | 删除后标签统计({}类): {}</source>
        <translation>Label löschen abgeschlossen: {} | {} Labeldateien geändert | Labelstatistik nach dem Löschen ({} Klassen): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="352"/>
        <location filename="../app/mixins/label_mixin.py" line="357"/>
        <location filename="../app/mixins/label_mixin.py" line="362"/>
        <source>(无)</source>
        <translation>(keine)</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="354"/>
        <source>合并标签: {} → {} | 修改 {} 个标签文件 | 合并后标签统计({}类): {}</source>
        <translation>Labels zusammenführen: {} → {} | {} Labeldateien geändert | Labelstatistik nach dem Zusammenführen ({} Klassen): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="359"/>
        <source>合并标签: {} → {} | 无标签文件被修改 | 合并后标签统计({}类): {}</source>
        <translation>Labels zusammenführen: {} → {} | keine Labeldatei geändert | Labelstatistik nach dem Zusammenführen ({} Klassen): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="400"/>
        <source>重命名标签</source>
        <translation>Labels umbenennen</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="400"/>
        <source>正在更新标注文件...</source>
        <translation>Labeldateien werden aktualisiert...</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="434"/>
        <location filename="../app/mixins/label_mixin.py" line="439"/>
        <location filename="../app/mixins/label_mixin.py" line="443"/>
        <location filename="../app/mixins/label_mixin.py" line="544"/>
        <source>删除标签</source>
        <translation>Label löschen</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="440"/>
        <source>请先在筛选下拉框中选择要删除的标签</source>
        <translation>Zuerst im Filter-Dropdown das zu löschende Label wählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="444"/>
        <source>确定删除标签&quot;{}&quot;吗?
该标签的所有标注将被删除, 且不可恢复.</source>
        <translation>Label „{}&quot; löschen?
Alle seine Annotationen werden gelöscht und können nicht wiederhergestellt werden.</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="477"/>
        <source>删除标签: {} ({}/{})</source>
        <translation>Label löschen: {} ({}/{})</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="544"/>
        <source>正在清理标注文件...</source>
        <translation>Labeldateien werden bereinigt...</translation>
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
        <translation>Leeren</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="79"/>
        <location filename="../app/widgets/log_dialog.py" line="20"/>
        <source>日志</source>
        <translation>Protokoll</translation>
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
        <translation>Ja</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="171"/>
        <source>否</source>
        <translation>Nein</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="226"/>
        <source>取消</source>
        <translation>Abbrechen</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="258"/>
        <source>取消中...</source>
        <translation>Wird abgebrochen...</translation>
    </message>
</context>
<context>
    <name>MetricsDialog</name>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="33"/>
        <source>训练指标</source>
        <translation>Trainingsmetriken</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="61"/>
        <source>标签筛选</source>
        <translation>Labelfilter</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="65"/>
        <source>全部指标</source>
        <translation>Alle Metriken</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="66"/>
        <source>全部标签-P</source>
        <translation>Alle Labels - P</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="67"/>
        <source>全部标签-R</source>
        <translation>Alle Labels - R</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="80"/>
        <source>(暂无标签数据,需完成首次 epoch 验证后才会出现)</source>
        <translation>(Noch keine Labeldaten; erscheinen erst nach der ersten Epochen-Validierung)</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="105"/>
        <source>暂无该标签的指标数据(训练完成后可查看)</source>
        <translation>Noch keine Metrikdaten für dieses Label (nach Abschluss des Trainings verfügbar)</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="148"/>
        <source>loss 值</source>
        <translation>Loss</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="149"/>
        <source>指标值 (mAP/P/R)</source>
        <translation>Metrik (mAP/P/R)</translation>
    </message>
</context>
<context>
    <name>MiscMixin</name>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="54"/>
        <source>界面语言: {}</source>
        <translation>Oberflächensprache: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="114"/>
        <source>数据集统计</source>
        <translation>Datensatz-Statistik</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="123"/>
        <source>应用所选数据集</source>
        <translation>Ausgewählte Datensätze übernehmen</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="214"/>
        <source>[{}/{}](未设置)</source>
        <translation>[{}/{}](nicht gesetzt)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="217"/>
        <source>(未选择数据集)</source>
        <translation>(kein Datensatz gewählt)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="342"/>
        <source>删除图像: {} 张 | 方式={} | 本地删除文件={} | 项目={}, 数据集={}</source>
        <translation>Bilder löschen: {} | Modus={} | lokale Datei gelöscht={} | Projekt={}, Datensatz={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="343"/>
        <source>删除本地文件</source>
        <translation>Lokale Datei löschen</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="343"/>
        <source>仅标记不加载</source>
        <translation>Nur markieren, nicht laden</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="381"/>
        <source>删除</source>
        <translation>Löschen</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="382"/>
        <source>取消</source>
        <translation>Abbrechen</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="384"/>
        <source>删除图像</source>
        <translation>Bilder löschen</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="385"/>
        <source>将从系统删除所选 {} 张图像?

(图像与同名标注文件不可恢复)</source>
        <translation>Die ausgewählten {} Bilder endgültig löschen?

(Bilder und gleichnamige Labeldateien können nicht wiederhergestellt werden)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="390"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>Bilder und gleichnamige Labeldateien werden von der Festplatte gelöscht. Nicht wiederherstellbar</translation>
    </message>
</context>
<context>
    <name>ModelAssets</name>
    <message>
        <location filename="../app/core/model_assets.py" line="79"/>
        <location filename="../app/core/model_assets.py" line="113"/>
        <source>速度最快, 精度够用</source>
        <translation>Am schnellsten, Genauigkeit ausreichend</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="80"/>
        <location filename="../app/core/model_assets.py" line="117"/>
        <source>精度更好, 稍慢一些</source>
        <translation>Bessere Genauigkeit, etwas langsamer</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="81"/>
        <location filename="../app/core/model_assets.py" line="121"/>
        <source>精度更高</source>
        <translation>Höhere Genauigkeit</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="82"/>
        <location filename="../app/core/model_assets.py" line="125"/>
        <source>精度最高, 显存占用大</source>
        <translation>Höchste Genauigkeit, hoher VRAM-Bedarf</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="83"/>
        <source>精度极致, 显存占用很大</source>
        <translation>Höchste Präzision, sehr hoher VRAM-Bedarf</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="86"/>
        <location filename="../app/core/model_assets.py" line="129"/>
        <source>轻量分割</source>
        <translation>Leichtgewichtige Segmentierung</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="87"/>
        <location filename="../app/core/model_assets.py" line="133"/>
        <source>速度与精度平衡</source>
        <translation>Ausgewogen zwischen Tempo und Genauigkeit</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="88"/>
        <location filename="../app/core/model_assets.py" line="137"/>
        <source>细节更完整</source>
        <translation>Vollständigere Details</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="89"/>
        <location filename="../app/core/model_assets.py" line="141"/>
        <source>最精细</source>
        <translation>Am feinsten</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="90"/>
        <source>最精细, 显存占用很大</source>
        <translation>Am feinsten, sehr hoher VRAM-Bedarf</translation>
    </message>
</context>
<context>
    <name>ModelDialog</name>
    <message>
        <location filename="../ui/model.ui" line="14"/>
        <location filename="../app/widgets/model_dialog.py" line="146"/>
        <source>模型管理</source>
        <translation>Modellverwaltung</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="28"/>
        <source>搜索项目 / 数据集 / 标签</source>
        <translation>Projekt / Datensatz / Label suchen</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="39"/>
        <source>全部任务</source>
        <translation>Alle Aufgaben</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="44"/>
        <source>检测</source>
        <translation>Erkennung</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="49"/>
        <source>分割</source>
        <translation>Segmentierung</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="54"/>
        <source>分类</source>
        <translation>Klassifizierung</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="66"/>
        <source>全部状态</source>
        <translation>Alle Status</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="71"/>
        <source>已完成</source>
        <translation>Abgeschlossen</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="76"/>
        <source>训练中</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="81"/>
        <source>失败</source>
        <translation>Fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="86"/>
        <source>已停止</source>
        <translation>Gestoppt</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="94"/>
        <source>仅看每个数据集最佳</source>
        <translation>Nur beste je Datensatz</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="114"/>
        <source>共 0 条</source>
        <translation>0 Einträge</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="135"/>
        <location filename="../app/widgets/model_dialog.py" line="565"/>
        <source>任务</source>
        <translation>Aufgabe</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="140"/>
        <source>数据集 / 标签</source>
        <translation>Datensatz / Labels</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="145"/>
        <location filename="../app/widgets/model_dialog.py" line="569"/>
        <source>精度</source>
        <translation>Genauigkeit</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="150"/>
        <location filename="../app/widgets/model_dialog.py" line="580"/>
        <source>训练时间</source>
        <translation>Trainiert am</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="155"/>
        <location filename="../app/widgets/model_dialog.py" line="582"/>
        <source>耗时</source>
        <translation>Dauer</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="160"/>
        <location filename="../app/widgets/model_dialog.py" line="572"/>
        <source>图像尺寸</source>
        <translation>Bildgröße</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="165"/>
        <source>操作</source>
        <translation>Aktionen</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="182"/>
        <source>模型详情</source>
        <translation>Modelldetails</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="189"/>
        <location filename="../app/widgets/model_dialog.py" line="549"/>
        <source>选中一行查看详情</source>
        <translation>Eine Zeile auswählen für Details</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="215"/>
        <source>查看完整指标</source>
        <translation>Alle Metriken anzeigen</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="222"/>
        <source>测试此模型</source>
        <translation>Dieses Modell testen</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="229"/>
        <source>按此配置重训</source>
        <translation>Mit dieser Konfiguration neu trainieren</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="236"/>
        <source>打开模型目录</source>
        <translation>Modellordner öffnen</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="276"/>
        <source>上一页</source>
        <translation>Zurück</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="283"/>
        <source>1/1</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="290"/>
        <source>下一页</source>
        <translation>Weiter</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="389"/>
        <source>共 {} 条</source>
        <translation>{} Einträge</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="440"/>
        <source> 等 {} 类</source>
        <translation> und {} weitere Klassen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="464"/>
        <source>测试</source>
        <translation>Testen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="469"/>
        <source>导出</source>
        <translation>Exportieren</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="474"/>
        <source>删除</source>
        <translation>Löschen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="562"/>
        <source>{} × {} 累积</source>
        <translation>{} × {} akkumuliert</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="563"/>
        <source>状态</source>
        <translation>Status</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="570"/>
        <source>训练集</source>
        <translation>Trainingsset</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="571"/>
        <source>验证集</source>
        <translation>Validierungsset</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="573"/>
        <source>轮数 / 早停</source>
        <translation>Epochen / Early Stop</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="575"/>
        <source>批大小</source>
        <translation>Batch-Größe</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="576"/>
        <source>学习率</source>
        <translation>Lernrate</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="577"/>
        <source>优化器</source>
        <translation>Optimierer</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="578"/>
        <source>设备</source>
        <translation>Gerät</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="579"/>
        <source>标签</source>
        <translation>Labels</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="583"/>
        <source>模型路径</source>
        <translation>Modellpfad</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="602"/>
        <source>失败原因</source>
        <translation>Fehlerursache</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="620"/>
        <source>暂无曲线</source>
        <translation>Keine Kurve</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="644"/>
        <source>{}  最佳 {:.3f}</source>
        <translation>{}  bestes {:.3f}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="652"/>
        <location filename="../app/widgets/model_dialog.py" line="663"/>
        <source>打开目录</source>
        <translation>Ordner öffnen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="653"/>
        <source>模型目录不存在:
{}</source>
        <translation>Modellordner existiert nicht:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="681"/>
        <source>[model_dialog] 打开指标失败: {}
{}</source>
        <translation>[model_dialog] Metriken öffnen fehlgeschlagen: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="683"/>
        <source>查看指标失败</source>
        <translation>Metriken konnten nicht geöffnet werden</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="690"/>
        <source>删除模型记录</source>
        <translation>Modelleintrag löschen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="691"/>
        <source>确定删除该条模型记录?
项目={}
数据集={}
开始时间={}
</source>
        <translation>Diesen Modelleintrag löschen?
Projekt={}
Datensatz={}
Startzeit={}
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="695"/>
        <source>删除模型记录: 项目={} 数据集={} 任务={} 开始时间={}</source>
        <translation>Modelleintrag löschen: Projekt={} Datensatz={} Aufgabe={} Startzeit={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="709"/>
        <source>删除模型记录失败: {} | {}</source>
        <translation>Modelleintrag löschen fehlgeschlagen: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="710"/>
        <source>[model_dialog] 删除失败: {}
{}</source>
        <translation>[model_dialog] Löschen fehlgeschlagen: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="719"/>
        <source>[model_dialog] 打开训练失败: {}
{}</source>
        <translation>[model_dialog] Training öffnen fehlgeschlagen: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="720"/>
        <source>打开训练失败</source>
        <translation>Training konnte nicht geöffnet werden</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="745"/>
        <source>[model_dialog] 打开测试失败: {}
{}</source>
        <translation>[model_dialog] Test öffnen fehlgeschlagen: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="747"/>
        <source>打开测试失败</source>
        <translation>Test konnte nicht geöffnet werden</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="764"/>
        <location filename="../app/widgets/model_dialog.py" line="782"/>
        <location filename="../app/widgets/model_dialog.py" line="798"/>
        <location filename="../app/widgets/model_dialog.py" line="1032"/>
        <location filename="../app/widgets/model_dialog.py" line="1042"/>
        <source>导出模型</source>
        <translation>Modell exportieren</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="765"/>
        <source>模型文件不存在:
{}</source>
        <translation>Modelldatei existiert nicht:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="766"/>
        <source>导出模型失败: 模型文件不存在 {}</source>
        <translation>Modellexport fehlgeschlagen: Modelldatei existiert nicht {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="768"/>
        <source>选择导出目录</source>
        <translation>Exportordner wählen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="783"/>
        <source>创建目录失败: {}</source>
        <translation>Ordner konnte nicht erstellt werden: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="784"/>
        <source>导出模型失败: 创建目录失败 {} | {}</source>
        <translation>Modellexport fehlgeschlagen: Ordner erstellen fehlgeschlagen {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="794"/>
        <source>开始导出模型: 项目={} 任务={} 架构={} 尺寸={} | {}</source>
        <translation>Modellexport starten: Projekt={} Aufgabe={} Architektur={} Größe={} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="795"/>
        <location filename="../app/widgets/model_dialog.py" line="899"/>
        <source>未知</source>
        <translation>unbekannt</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="799"/>
        <source>正在导出 ONNX...</source>
        <translation>ONNX wird exportiert...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="818"/>
        <source>ONNX 导出完成: {} ({:.1f} MB)</source>
        <translation>ONNX-Export abgeschlossen: {} ({:.1f} MB)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="876"/>
        <source>生成 classes.txt 失败: {}</source>
        <translation>classes.txt erzeugen fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="877"/>
        <source>[export] 生成 classes.txt 失败: {}</source>
        <translation>[export] classes.txt erzeugen fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="883"/>
        <source>导出模型报告跳过: 分类任务不出评估报告</source>
        <translation>Modellberichtsexport übersprungen: Klassifizierungsaufgaben erzeugen keinen Auswertungsbericht</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="884"/>
        <source>分类任务不生成评估报告</source>
        <translation>Klassifizierungsaufgaben erzeugen keinen Auswertungsbericht</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="888"/>
        <source>导出模型报告跳过: 未找到验证集</source>
        <translation>Modellberichtsexport übersprungen: kein Validierungsset gefunden</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="889"/>
        <source>未找到验证集, 已跳过评估报告</source>
        <translation>Kein Validierungsset gefunden; Auswertungsbericht übersprungen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="891"/>
        <location filename="../app/widgets/model_dialog.py" line="965"/>
        <source>正在生成模型报告...</source>
        <translation>Modellbericht wird erstellt...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="895"/>
        <source>正在生成模型报告 {}/{}</source>
        <translation>Modellbericht wird erstellt {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="898"/>
        <source>导出模型评估失败: {}</source>
        <translation>Export der Modellauswertung fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="901"/>
        <source>评估失败, 已跳过报告: {}</source>
        <translation>Auswertung fehlgeschlagen; Bericht übersprungen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="984"/>
        <source>导出模型报告跳过: 验证集没有标注</source>
        <translation>Modellberichtsexport übersprungen: Validierungsset ohne Annotation</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="985"/>
        <source>验证集没有标注, 已跳过评估报告</source>
        <translation>Validierungsset ohne Annotation, Bewertungsbericht übersprungen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="991"/>
        <source>[export] 生成评估报告失败:
{}</source>
        <translation>[export] Auswertungsbericht erzeugen fehlgeschlagen:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="988"/>
        <source>生成评估报告失败: {}</source>
        <translation>Auswertungsbericht erzeugen fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="980"/>
        <source>导出模型报告完成: {}</source>
        <translation>Modellberichtsexport abgeschlossen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="992"/>
        <source>评估完成, 但报告生成失败</source>
        <translation>Auswertung abgeschlossen, aber der Bericht konnte nicht erstellt werden</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1026"/>
        <source>导出模型完成: {} | 包含: {}</source>
        <translation>Modelexport abgeschlossen: {} | Enthält: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1028"/>
        <source>已导出到:
{}

包含: {}</source>
        <translation>Exportiert nach:
{}

Enthält: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="990"/>
        <location filename="../app/widgets/model_dialog.py" line="1039"/>
        <source>未知错误</source>
        <translation>Unbekannter Fehler</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1043"/>
        <source>模型导出失败, 详情见日志</source>
        <translation>Modell-Export fehlgeschlagen, Details siehe Protokoll</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1038"/>
        <source>导出模型失败: {}</source>
        <translation>Modelexport fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1040"/>
        <source>[export] ONNX 导出失败: {}</source>
        <translation>[export] ONNX-Export fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1057"/>
        <source>复制导出示例失败: {}</source>
        <translation>Exportbeispiel kopieren fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1058"/>
        <source>[export] 复制示例失败: {}</source>
        <translation>[export] Beispiel kopieren fehlgeschlagen: {}</translation>
    </message>
</context>
<context>
    <name>ModelDownloader</name>
    <message>
        <location filename="../app/core/model_download.py" line="92"/>
        <source>权重目录不可写入, 请点&quot;更改&quot;换一个目录</source>
        <translation>Gewichtsordner nicht beschreibbar, bitte auf „Ändern&quot; klicken und einen anderen Ordner wählen</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="101"/>
        <source>权重文件大小不符, 丢弃重下: {}</source>
        <translation>Gewichtsdatei hat falsche Größe, verworfen und erneut laden: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="111"/>
        <source>开始下载权重 {} ({}, 已下载 {})</source>
        <translation>Gewichtsdownload startet: {} ({}, bereits geladen {})</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="118"/>
        <source>下载权重失败 {}: {}</source>
        <translation>Gewichte herunterladen fehlgeschlagen {}: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="121"/>
        <source>无法连接下载服务器, 请检查网络后重试</source>
        <translation>Keine Verbindung zum Downloadserver, bitte Netzwerk prüfen und erneut versuchen</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="129"/>
        <source>下载中断, 已保留进度, 可再次点击续传</source>
        <translation>Download unterbrochen, Fortschritt beibehalten, erneut klicken zum Fortsetzen</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="134"/>
        <source>下载不完整, 已保留进度, 可再次点击续传</source>
        <translation>Download unvollständig, Fortschritt beibehalten, erneut klicken zum Fortsetzen</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="141"/>
        <source>权重校验不通过 {}: 期望 {} 实际 {}</source>
        <translation>Gewichtsprüfung fehlgeschlagen {}: erwartet {} tatsächlich {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="146"/>
        <source>文件校验未通过, 损坏文件已删除, 请重试</source>
        <translation>Dateiprüfung fehlgeschlagen, beschädigte Datei gelöscht, bitte erneut versuchen</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="152"/>
        <source>写入权重目录失败, 请检查磁盘空间</source>
        <translation>Schreiben in den Gewichtsordner fehlgeschlagen, bitte Speicherplatz prüfen</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="155"/>
        <source>权重就绪: {}</source>
        <translation>Gewichte bereit: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="176"/>
        <source>下载已取消, 已下载部分保留以便续传: {}</source>
        <translation>Download abgebrochen, geladener Teil zum Fortsetzen beibehalten: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="196"/>
        <source>权重下载异常 {}: {!r}</source>
        <translation>Fehler beim Gewichtsdownload {}: {!r}</translation>
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
        <translation>Modellgewichte</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="63"/>
        <source>目标检测 · Transformer</source>
        <translation>Objekterkennung · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="97"/>
        <source>目标检测 · CNN</source>
        <translation>Objekterkennung · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="131"/>
        <source>图像分割 · Transformer</source>
        <translation>Bildsegmentierung · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="165"/>
        <source>图像分割 · CNN</source>
        <translation>Bildsegmentierung · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="221"/>
        <source>下载目录</source>
        <translation>Downloadordner</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="238"/>
        <source>更改</source>
        <translation>Ändern</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="265"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="330"/>
        <source>开始下载</source>
        <translation>Download starten</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="275"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="171"/>
        <source>关闭</source>
        <translation>Schließen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="52"/>
        <source>还剩 {}s</source>
        <translation>Noch {}s</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="53"/>
        <source>还剩 {}m{}s</source>
        <translation>Noch {}m{}s</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="237"/>
        <source>占用空间 {}</source>
        <translation>Belegt {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="255"/>
        <source>选择权重目录</source>
        <translation>Gewichtsordner wählen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="276"/>
        <source>权重目录不可写入 {}: {!r}</source>
        <translation>Gewichtsordner nicht beschreibbar {}: {!r}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="287"/>
        <source>勾选的模型都已就绪, 不需要下载.</source>
        <translation>Alle ausgewählten Modelle sind bereit; kein Download nötig.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="292"/>
        <source>当前目录不可写入, 请点&quot;更改&quot;换一个目录:
{}</source>
        <translation>Der aktuelle Ordner ist nicht beschreibbar. Auf „Ändern&quot; klicken und einen anderen wählen:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="297"/>
        <source>下载中...</source>
        <translation>Wird heruntergeladen...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="341"/>
        <source>以下权重没能下载完成:
</source>
        <translation>Diese Gewichte konnten nicht vollständig geladen werden:
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="348"/>
        <source>下载还在进行, 现在关闭会中断下载(已下载部分保留, 下次可续传).
确定关闭?</source>
        <translation>Ein Download läuft noch. Beim Schließen wird er unterbrochen (bereits Geladenes bleibt erhalten und wird beim nächsten Mal fortgesetzt).
Trotzdem schließen?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="380"/>
        <source>去下载</source>
        <translation>Herunterladen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="389"/>
        <source>该架构的权重必须先下载好才能开始训练.</source>
        <translation>Die Gewichte dieser Architektur müssen zuerst heruntergeladen werden, erst dann kann das Training starten.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="383"/>
        <source>本次训练选用 {} {}模型, 需要先下载 {}.</source>
        <translation>Dieses Training nutzt das Modell {} {} und benötigt zuerst {}.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="382"/>
        <source>缺少模型权重</source>
        <translation>Modellgewichte fehlen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="381"/>
        <source>取消</source>
        <translation>Abbrechen</translation>
    </message>
</context>
<context>
    <name>MultiCombo</name>
    <message>
        <location filename="../app/widgets/multi_combo.py" line="349"/>
        <source>请选择数据集</source>
        <translation>Datensätze wählen</translation>
    </message>
</context>
<context>
    <name>NameInputDialog</name>
    <message>
        <location filename="../ui/input_name.ui" line="14"/>
        <location filename="../ui/input_name.ui" line="40"/>
        <location filename="../app/widgets/name_input_dialog.py" line="13"/>
        <source>输入名称</source>
        <translation>Name eingeben</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="65"/>
        <location filename="../app/widgets/name_input_dialog.py" line="14"/>
        <source>请输入名称</source>
        <translation>Namen eingeben</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="100"/>
        <source>取消</source>
        <translation>Abbrechen</translation>
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
        <translation>Der ONNX-Export wird für Anomalieerkennungsmodelle nicht unterstützt (sie kombinieren ein Backbone mit einer Speicherbank); bitte das Modell mit der Modelldatei direkt in der Software testen</translation>
    </message>
</context>
<context>
    <name>ProjectMixin</name>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="18"/>
        <source>输入名称</source>
        <translation>Name eingeben</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="19"/>
        <source>项目名称</source>
        <translation>Projektname</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="22"/>
        <location filename="../app/mixins/project_mixin.py" line="26"/>
        <source>创建项目</source>
        <translation>Projekt erstellen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="26"/>
        <location filename="../app/mixins/project_mixin.py" line="38"/>
        <source>项目名称已存在!</source>
        <translation>Ein Projekt mit diesem Namen existiert bereits!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="29"/>
        <source>创建项目: {}</source>
        <translation>Projekt erstellen: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="34"/>
        <location filename="../app/mixins/project_mixin.py" line="38"/>
        <location filename="../app/mixins/project_mixin.py" line="91"/>
        <source>修改名称</source>
        <translation>Umbenennen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <source>重命名项目: {} → {}</source>
        <translation>Projekt umbenennen: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="46"/>
        <location filename="../app/mixins/project_mixin.py" line="92"/>
        <source>删除项目</source>
        <translation>Projekt löschen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="47"/>
        <source>确定删除项目&quot;{}&quot;吗?
</source>
        <translation>Projekt „{}&quot; löschen?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="48"/>
        <source>删除项目: {}</source>
        <translation>Projekt löschen: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="88"/>
        <location filename="../app/mixins/project_mixin.py" line="132"/>
        <location filename="../app/mixins/project_mixin.py" line="140"/>
        <source>添加数据集</source>
        <translation>Datensatz hinzufügen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="90"/>
        <source>导出项目</source>
        <translation>Projekt exportieren</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="107"/>
        <source>导入</source>
        <translation>Importieren</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="108"/>
        <source>导出</source>
        <translation>Exportieren</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="109"/>
        <source>重载</source>
        <translation>Neu laden</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="110"/>
        <source>移动</source>
        <translation>Verschieben</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="111"/>
        <source>修改</source>
        <translation>Umbenennen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="112"/>
        <source>删除</source>
        <translation>Löschen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="133"/>
        <source>数据集名称</source>
        <translation>Datensatzname</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="140"/>
        <location filename="../app/mixins/project_mixin.py" line="151"/>
        <source>该项目下已存在同名数据集!</source>
        <translation>In diesem Projekt existiert bereits ein Datensatz mit diesem Namen!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="142"/>
        <source>创建数据集: {}/{}</source>
        <translation>Datensatz erstellen: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="147"/>
        <location filename="../app/mixins/project_mixin.py" line="151"/>
        <source>修改数据集</source>
        <translation>Datensatz umbenennen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="153"/>
        <source>重命名数据集: {} → {}</source>
        <translation>Datensatz umbenennen: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="158"/>
        <source>删除数据集</source>
        <translation>Datensatz löschen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="159"/>
        <source>确定删除数据集&quot;{}&quot;吗?
</source>
        <translation>Datensatz „{}&quot; löschen?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="163"/>
        <source>删除数据集: {}/{}</source>
        <translation>Datensatz löschen: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="182"/>
        <location filename="../app/mixins/project_mixin.py" line="195"/>
        <location filename="../app/mixins/project_mixin.py" line="212"/>
        <source>移动数据集</source>
        <translation>Datensatz verschieben</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="183"/>
        <source>是否将&quot;{}&quot;的数据从
{} / {} 移动到 {} / {}?
移动后源数据集将清空.</source>
        <translation>Die Daten von „{}&quot; von
{} / {} nach {} / {} verschieben?
Der Quell-Datensatz wird danach geleert.</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="192"/>
        <source>移动失败</source>
        <translation>Verschieben fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="196"/>
        <source>已从 {} / {} 移动到 {} / {}</source>
        <translation>Von {} / {} nach {} / {} verschoben</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="213"/>
        <source>没有可移动到的目标数据集(本项目之外无数据集)</source>
        <translation>Kein Ziel-Datensatz verfügbar (außerhalb dieses Projekts gibt es keine Datensätze)</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="217"/>
        <source>选择目标数据集</source>
        <translation>Ziel-Datensatz wählen</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="221"/>
        <source>选择要将数据移动到的目标数据集:</source>
        <translation>Ziel-Datensatz wählen, in den die Daten verschoben werden:</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="305"/>
        <source>{}: {}个</source>
        <translation>{}: {} Stück</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="307"/>
        <source>数据集移动: {}/{} → {}/{} | 移动图像 {} 张 | 目标标签统计({}类): {}</source>
        <translation>Datensatz verschieben: {}/{} → {}/{} | {} Bilder verschoben | Labelstatistik im Ziel ({} Klassen): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="310"/>
        <source>(无)</source>
        <translation>(keine)</translation>
    </message>
</context>
<context>
    <name>ProjectSidebar</name>
    <message>
        <location filename="../app/widgets/project_sidebar.py" line="400"/>
        <source>{} 个项目 · {} 个数据集</source>
        <translation>Projekte {} · Datensätze {}</translation>
    </message>
</context>
<context>
    <name>QueueMixin</name>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="92"/>
        <source>训练队列已启动</source>
        <translation>Trainings-Warteschlange gestartet</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="100"/>
        <source>[队列] 已停止</source>
        <translation>[队列] Gestoppt</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="188"/>
        <source>[队列] 所有任务已执行完毕</source>
        <translation>[队列] Alle Aufgaben wurden abgearbeitet</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="196"/>
        <source>[队列] 跳过任务 {}: {}</source>
        <translation>[队列] Aufgabe übersprungen {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="197"/>
        <source>队列任务启动失败 {}: {}</source>
        <translation>Warteschlangen-Aufgabe konnte nicht gestartet werden {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="217"/>
        <source>[队列] 缺少权重 {}, 该项训练会失败</source>
        <translation>[队列] Gewichte fehlen {}, dieses Training wird fehlschlagen</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="220"/>
        <source>[队列] 缺少权重 {}, 该项训练时会自行下载</source>
        <translation>[队列] Gewichte fehlen {}, werden beim Training dieser Aufgabe automatisch geladen</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="230"/>
        <source>已有训练在进行中</source>
        <translation>Ein Training läuft bereits</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="235"/>
        <source>[队列] 开始队列第 {}/{} 项: {}</source>
        <translation>[队列] Warteschlangen-Eintrag {}/{} startet: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="239"/>
        <source>队列启动任务: {} record={}</source>
        <translation>Warteschlange startet Aufgabe: {} record={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="277"/>
        <source>训练未完成, 详见日志</source>
        <translation>Training nicht abgeschlossen; siehe Protokoll</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="304"/>
        <source>[队列] 显存等待超时, 仍继续启动下一个任务</source>
        <translation>[队列] Zeitüberschreitung beim Warten auf VRAM, die nächste Aufgabe wird trotzdem gestartet</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="333"/>
        <source>队列 {}</source>
        <translation>Warteschlange {}</translation>
    </message>
</context>
<context>
    <name>StatusText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="16"/>
        <source>等待中</source>
        <translation>Wartet</translation>
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
        <translation>Abgeschlossen</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="19"/>
        <location filename="../app/widgets/status_style.py" line="26"/>
        <source>失败</source>
        <translation>Fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="20"/>
        <location filename="../app/widgets/status_style.py" line="29"/>
        <source>已跳过</source>
        <translation>Übersprungen</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="21"/>
        <location filename="../app/widgets/status_style.py" line="27"/>
        <source>已停止</source>
        <translation>Gestoppt</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="22"/>
        <location filename="../app/widgets/status_style.py" line="30"/>
        <source>已中断</source>
        <translation>Abgebrochen</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="28"/>
        <source>失败/已停止</source>
        <translation>Fehlgeschlagen/Gestoppt</translation>
    </message>
</context>
<context>
    <name>TaskText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="35"/>
        <source>检测</source>
        <translation>Erkennung</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="36"/>
        <source>分割</source>
        <translation>Segmentierung</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="37"/>
        <source>分类</source>
        <translation>Klassifizierung</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="38"/>
        <source>异常检测</source>
        <translation>Anomalieerkennung</translation>
    </message>
</context>
<context>
    <name>TestDialog</name>
    <message>
        <location filename="../ui/test_dialog.ui" line="14"/>
        <location filename="../ui/test_dialog.ui" line="41"/>
        <source>模型测试</source>
        <translation>Modelltest</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="77"/>
        <source>检测</source>
        <translation>Erkennung</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="93"/>
        <source>best.pth</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="105"/>
        <source>mAP50 0.912 · 输入 640 · 规模 n · 训练 2026-09-01 14:22</source>
        <translation>mAP50 0.912 · Eingabe 640 · Skala n · Training 2026-09-01 14:22</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="126"/>
        <source>数据与设备</source>
        <translation>Daten &amp; Gerät</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="168"/>
        <source>数据</source>
        <translation>Daten</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="191"/>
        <source>设备</source>
        <translation>Gerät</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="221"/>
        <source>测试参数</source>
        <translation>Testparameter</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="263"/>
        <source>置信度</source>
        <translation>Konfidenz</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="304"/>
        <source>低于该分数的预测直接丢弃</source>
        <translation>Vorhersagen unterhalb dieses Werts werden verworfen</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="320"/>
        <source>IoU 阈值</source>
        <translation>IoU-Schwelle</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="361"/>
        <source>与标注框重合度达标才算正确检出</source>
        <translation>Die Überlappung mit dem Labelrahmen muss diesen Wert erreichen, um als korrekt erkannt zu gelten</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="377"/>
        <source>输出标签文件</source>
        <translation>Labeldateien schreiben</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="409"/>
        <source>会在图像路径下输出标签文件, 可重载数据集查看检出效果</source>
        <translation>Schreibt Labeldateien neben den Bildern; Datensatz neu laden, um die Erkennungsergebnisse zu prüfen</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="461"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="471"/>
        <source>请选择数据集</source>
        <translation>Datensätze wählen</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="515"/>
        <location filename="../app/widgets/test_dialog.py" line="92"/>
        <source>取消</source>
        <translation>Abbrechen</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="522"/>
        <source>开始测试</source>
        <translation>Test starten</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="220"/>
        <source>未指定模型</source>
        <translation>Kein Modell angegeben</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="221"/>
        <source>请在模型列表中重新选择一行</source>
        <translation>In der Modellliste erneut eine Zeile auswählen</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="229"/>
        <source>准确率</source>
        <translation>Genauigkeit</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="236"/>
        <source>输入 {}</source>
        <translation>Eingabe {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="238"/>
        <source>规模 {}</source>
        <translation>Skala {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="240"/>
        <source>训练 {}</source>
        <translation>Training {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="242"/>
        <source>该记录未保存训练指标</source>
        <translation>Für diesen Eintrag wurden keine Trainingsmetriken gespeichert</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="245"/>
        <source> · 文件已不存在</source>
        <translation> · Datei existiert nicht mehr</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="271"/>
        <source>请先勾选要测试的数据集</source>
        <translation>Zuerst die zu testenden Datensätze anhaken</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="283"/>
        <source>{} 个数据集 · {} 张图</source>
        <translation>{} Datensätze · {} Bilder</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="285"/>
        <source>分类数据集, 统计每张图的判断正确率</source>
        <translation>Klassifizierungs-Datensatz; misst die Trefferquote pro Bild</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="287"/>
        <source>已标注, 评估模式: 统计检出率 / 漏检 / 误检</source>
        <translation>Annotiert, Auswertungsmodus: Trefferquote / Übersehenes / Fehlalarme</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="289"/>
        <source>未标注, 推理模式: 只输出预测标签</source>
        <translation>Nicht annotiert, Inferenzmodus: gibt nur vorhergesagte Labels aus</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="291"/>
        <source>部分已标注, 已标注与未标注的数据集不能一起测</source>
        <translation>Teilweise annotiert; annotierte und nicht annotierte Datensätze können nicht zusammen getestet werden</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="318"/>
        <source>为判定为不良品的图写 &lt;同名&gt;.json 到图像目录, 多边形标出异常区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Schreibt für als Schlechtteil bewertete Bilder &lt;gleichnamig&gt;.json neben das Bild, Polygone markieren die Anomaliebereiche, das Annotationstool kann sie direkt öffnen; vorhandene manuelle Annotationen dort werden überschrieben</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="322"/>
        <source>把异常区域写成 labelme json, 便于重载复核</source>
        <translation>Schreibt die Anomaliebereiche als labelme json, um sie zum Prüfen neu laden zu können</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="328"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Schreibt &lt;gleicher Name&gt;.json neben jedes Bild, sodass das Annotationstool sie direkt öffnen kann; vorhandene manuelle Labels dort werden überschrieben</translation>
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
        <translation>Testen</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="345"/>
        <source>已有测试在进行中</source>
        <translation>Ein Test läuft bereits</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="349"/>
        <source>请至少选择一个数据集</source>
        <translation>Mindestens einen Datensatz auswählen</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="366"/>
        <source>置信度/iou阈值必须是数字</source>
        <translation>Konfidenz/IoU-Schwelle muss eine Zahl sein</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="372"/>
        <source>模型文件不存在, 请重新选择</source>
        <translation>Die Modelldatei existiert nicht; bitte erneut auswählen</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="385"/>
        <source>数据集 {}/{} 未导入图像</source>
        <translation>Datensatz {}/{} hat keine Bilder importiert</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="395"/>
        <source>分类数据集与检测/分割数据集不能同时测试: {}/{}</source>
        <translation>Klassifizierungs- und Erkennungs-/Segmentierungs-Datensätze können nicht zusammen getestet werden: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="401"/>
        <source>已标注与未标注的数据集不能同时测试: {}/{}</source>
        <translation>Annotierte und nicht annotierte Datensätze können nicht zusammen getestet werden: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="436"/>
        <source>[test] 启动测试 worker: model={} 数据集={} 图像目录={} device={} cfg={}</source>
        <translation>[test] Test-Worker starten: model={} Datensatz={} Bildordner={} device={} cfg={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="441"/>
        <source>测试准备中...</source>
        <translation>Test wird vorbereitet...</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="458"/>
        <location filename="../app/widgets/test_dialog.py" line="459"/>
        <source>测试即将开始</source>
        <translation>Test startet gleich</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="505"/>
        <source>测试中 {}/{}</source>
        <translation>Test läuft {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="517"/>
        <source>[test-dialog] 测试完成, ok={}</source>
        <translation>[test-dialog] Test abgeschlossen, ok={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="525"/>
        <source>测试结果</source>
        <translation>Testergebnisse</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="526"/>
        <source>测试未正常完成</source>
        <translation>Der Test wurde nicht regulär abgeschlossen</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="536"/>
        <source>[test-dialog] 测试失败: {}</source>
        <translation>[test-dialog] Test fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="543"/>
        <source>测试失败</source>
        <translation>Test fehlgeschlagen</translation>
    </message>
</context>
<context>
    <name>TestReport</name>
    <message>
        <location filename="../app/train/test_report.py" line="178"/>
        <source>漏 {}</source>
        <translation>Übersehen {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="180"/>
        <source>误 {}</source>
        <translation>Fehlalarm {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="182"/>
        <source>认错 {}</source>
        <translation>Falsch erkannt {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="193"/>
        <source>(图片无法打开)</source>
        <translation>(Bild lässt sich nicht öffnen)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="279"/>
        <source>类别认错: {} → {}</source>
        <translation>Klasse falsch: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="307"/>
        <source>本次验证集没有漏检, 也没有误检.</source>
        <translation>In diesem Validierungsset gibt es weder übersehene noch falsch erkannte Objekte.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="310"/>
        <source>明细抽样: 共 {} 张有问题(漏检 {} / 误检 {}), 本报告抽取 {} 张 - 每个类别每种错误最多 {} 张, 按错误数从多到少取</source>
        <translation>Detailstichprobe: {} Bilder mit Problemen (Übersehen {} / Fehlalarm {}), dieser Bericht wählt {} Bilder aus - je Klasse und Fehlertyp höchstens {} Bilder, sortiert nach Fehlerzahl absteigend</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="315"/>
        <source>明细: 共 {} 张有问题(漏检 {} / 误检 {}), 已全部列出</source>
        <translation>Details: {} Bilder mit Problemen (Übersehen {} / Fehlalarm {}), alle aufgelistet</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="342"/>
        <source>漏检 GT: 有标注但模型没检出</source>
        <translation>Übersehen GT: annotiert, aber vom Modell nicht erkannt</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="344"/>
        <source>误检预测: 模型检出但标注里没有</source>
        <translation>Fehlalarm-Vorhersage: vom Modell erkannt, aber nicht annotiert</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="346"/>
        <source>正确检出(仅作位置参照)</source>
        <translation>Korrekt erkannt (nur als Positionsreferenz)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="348"/>
        <source>类别认错: 位置对但判错类别(GT → 预测)</source>
        <translation>Klasse falsch: Position korrekt, Klasse falsch (GT → Vorhersage)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="351"/>
        <source>虚线轮廓: 分割 mask / 标注多边形(判定按外接框 IoU)</source>
        <translation>Gestrichelte Kontur: Segmentierungs-Maske / Annotationspolygon (Bewertung nach IoU des umschließenden Rahmens)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="449"/>
        <location filename="../app/train/test_report.py" line="1048"/>
        <source>模型评估报告</source>
        <translation>Modell-Auswertungsbericht</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="453"/>
        <source>当前训练模型</source>
        <translation>Aktuelles Trainingsmodell</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="457"/>
        <location filename="../app/train/test_report.py" line="463"/>
        <source>(未记录)</source>
        <translation>(nicht erfasst)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="462"/>
        <source>数据集 </source>
        <translation>Datensatz </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="465"/>
        <source>置信度 {}</source>
        <translation>Konfidenz {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="485"/>
        <source>测试张数</source>
        <translation>Getestete Bilder</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="486"/>
        <location filename="../app/train/test_report.py" line="488"/>
        <source>{} 张</source>
        <translation>{} Bilder</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="487"/>
        <source>有问题的图片</source>
        <translation>Bilder mit Problemen</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="490"/>
        <source>检出率 (Recall)</source>
        <translation>Trefferquote (Recall)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="492"/>
        <source>准确率 (Precision)</source>
        <translation>Genauigkeit (Precision)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="494"/>
        <source>正确检出</source>
        <translation>Korrekt</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="495"/>
        <source>{} 个</source>
        <translation>{} Stück</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="496"/>
        <source>漏检 (该抓没抓)</source>
        <translation>Übersehen (nicht erkannt)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="497"/>
        <location filename="../app/train/test_report.py" line="500"/>
        <location filename="../app/train/test_report.py" line="505"/>
        <source>{} 个 / {} 张图</source>
        <translation>{} Stück / {} Bilder</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="499"/>
        <source>误检 (过杀)</source>
        <translation>Fehlalarm (Übererkennung)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="504"/>
        <source>类别认错 (位置对, 类别错)</source>
        <translation>Klasse falsch (Position korrekt, Klasse falsch)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="507"/>
        <source>指标</source>
        <translation>Metrik</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="508"/>
        <source>值</source>
        <translation>Wert</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="527"/>
        <source>按类别</source>
        <translation>Nach Klasse</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="530"/>
        <source>类别</source>
        <translation>Klasse</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="531"/>
        <source>标注</source>
        <translation>Annotation</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="532"/>
        <source>正确</source>
        <translation>Richtig</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="533"/>
        <source>漏检</source>
        <translation>Übersehen</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="534"/>
        <source>误检</source>
        <translation>Fehlalarm</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="535"/>
        <source>检出率</source>
        <translation>Trefferquote</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="536"/>
        <source>准确率</source>
        <translation>Genauigkeit</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="563"/>
        <source>... 另有 {} 类未列出</source>
        <translation>... {} weitere Klassen nicht aufgelistet</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="585"/>
        <source>错误样本明细(仅列漏检 / 误检图片, 正确检出不列出)</source>
        <translation>Fehlerstichproben-Details (nur Bilder mit Übersehenem / Fehlalarm, korrekte Treffer nicht aufgelistet)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="624"/>
        <source>本轮检出率 {:.0f}%, 准确率 {:.0f}%.</source>
        <translation>Trefferquote dieser Runde {:.0f}%, Genauigkeit {:.0f}%.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="627"/>
        <source>没有逐类别统计, 无法定位到具体标签,请先确认标签文件能正常读到.</source>
        <translation>Keine Statistik je Klasse, konkrete Labels lassen sich nicht bestimmen; bitte zuerst prüfen, ob die Labeldateien lesbar sind.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="651"/>
        <source>漏检分布在</source>
        <translation>Übersehenes verteilt auf</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="652"/>
        <source>漏检集中在</source>
        <translation>Übersehenes konzentriert sich auf</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="655"/>
        <source>(共 {} 个), 优先补这几类的姿态, 光照样本,并复核标注是否有遗漏.</source>
        <translation>(insgesamt {}), vorrangig Pose- und Beleuchtungsbeispiele für diese Klassen ergänzen und die Annotationen auf Lücken prüfen.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="661"/>
        <source>误检分布在</source>
        <translation>Fehlalarme verteilt auf</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="662"/>
        <source>误检以</source>
        <translation>Fehlalarme überwiegend in</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="663"/>
        <source>({} 个),属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({} Stück), Übererkennung, bitte fehlerfreie Negativbeispiele ergänzen und Annotationsrauschen bereinigen.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="665"/>
        <source>({} 个)为主,属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({} Stück) als Hauptanteil, Übererkennung, bitte fehlerfreie Negativbeispiele ergänzen und Annotationsrauschen bereinigen.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="674"/>
        <source>暂无</source>
        <translation>Keine</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="678"/>
        <source>此外 {} 处位置对但类别判错</source>
        <translation>Zusätzlich {} Stellen mit korrekter Position, aber falscher Klasse</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="680"/>
        <source>(报告紫框), 属分类能力不足而非定位问题,需补易混淆类别之间的区分性样本.</source>
        <translation>(im Bericht violett markiert), das liegt an zu schwacher Klassifizierung und nicht an der Lokalisierung, daher mehr unterscheidbare Beispiele zwischen leicht verwechselbaren Klassen ergänzen.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="685"/>
        <source>其中</source>
        <translation>Davon</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="687"/>
        <source>仅 {} 个标注, 样本不足是主要瓶颈, 建议补到 200 个以上.</source>
        <translation>Nur {} Annotationen, zu wenige Beispiele sind der Hauptengpass, bitte auf über 200 aufstocken.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="692"/>
        <source>各类样本量差距大(最多 {} / 最少 {}),训练时建议做类别均衡采样.</source>
        <translation>Große Unterschiede bei der Beispielzahl je Klasse (max. {} / min. {}), beim Training klassenausgeglichenes Sampling verwenden.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="697"/>
        <source>把本报告中的漏检, 误检图加入训练集复训,再用同参数复测对比.</source>
        <translation>Die übersehenen und falschen Bilder aus diesem Bericht ins Trainingsset aufnehmen, erneut trainieren und mit denselben Parametern erneut testen und vergleichen.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="701"/>
        <source>本轮无漏检, 无误检, 建议用更严的阈值或更难的样本再压一轮, 确认稳定性.</source>
        <translation>Diese Runde ohne Übersehenes und ohne Fehlalarme, bitte mit strengerer Schwelle oder schwierigeren Beispielen erneut prüfen, um die Stabilität zu bestätigen.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="897"/>
        <source>改进建议</source>
        <translation>Verbesserungsvorschläge</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="902"/>
        <source>基于本次测试的指标与按类别表现</source>
        <translation>Basierend auf den Metriken dieses Tests und der Leistung je Klasse</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="904"/>
        <source>(模型: {})</source>
        <translation>(Modell: {})</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="906"/>
        <source>, 建议如下:</source>
        <translation>, Empfehlungen:</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="924"/>
        <source>标红的标签是需要重点关注的类别.</source>
        <translation>Rot markierte Labels sind die Klassen, die besondere Aufmerksamkeit brauchen.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="929"/>
        <location filename="../app/train/test_report.py" line="955"/>
        <source>第 {} 页</source>
        <translation>Seite {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1019"/>
        <source>{}(抽取 {} / 共 {} 张)</source>
        <translation>{}(ausgewählt {} / von {} Bildern)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1022"/>
        <source>{}(共 {} 张)</source>
        <translation>{}(insgesamt {} Bilder)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1024"/>
        <source>漏检样本: 有标注但模型没检出</source>
        <translation>Übersehene Beispiele: annotiert, aber vom Modell nicht erkannt</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1027"/>
        <source>误检样本: 模型检出但标注里没有</source>
        <translation>Fehlalarm-Beispiele: vom Modell erkannt, aber nicht annotiert</translation>
    </message>
</context>
<context>
    <name>TestResultDialog</name>
    <message>
        <location filename="../ui/test_result.ui" line="14"/>
        <source>测试结果分析</source>
        <translation>Testergebnis-Analyse</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="58"/>
        <source>图像维度</source>
        <translation>Nach Bild</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="68"/>
        <source>按「张」统计</source>
        <translation>Zählung nach Bildern</translation>
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
        <translation>Getestete Bilder</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="194"/>
        <source>全对图像</source>
        <translation>Bilder ohne Fehler</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="250"/>
        <source>有漏检图像</source>
        <translation>Bilder mit Übersehenem</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="306"/>
        <location filename="../app/train/test_result_dialog.py" line="189"/>
        <source>有误检图像</source>
        <translation>Bilder mit Fehlalarm</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="350"/>
        <source>标签维度</source>
        <translation>Nach Label</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="360"/>
        <source>按「标注框」统计</source>
        <translation>Zählung nach Rahmen</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="430"/>
        <location filename="../ui/test_result.ui" line="639"/>
        <location filename="../app/train/test_result_dialog.py" line="197"/>
        <source>正确检出</source>
        <translation>Korrekt</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="486"/>
        <location filename="../ui/test_result.ui" line="644"/>
        <source>漏检</source>
        <translation>Übersehen</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="542"/>
        <location filename="../ui/test_result.ui" line="649"/>
        <source>误检</source>
        <translation>Fehlalarm</translation>
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
        <translation>Genauigkeit</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="629"/>
        <location filename="../app/train/test_result_dialog.py" line="275"/>
        <source>类别</source>
        <translation>Klasse</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="634"/>
        <source>标注数</source>
        <translation>Rahmen</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="654"/>
        <source>检出率</source>
        <translation>Trefferquote</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="679"/>
        <source>每类抽取</source>
        <translation>Pro Klasse</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="686"/>
        <source>每个类别的每种错误（漏检 / 误检）最多列出几张图。
报告体积约 120 KB 一张，样本多时调小可以显著减小 PDF；选「全部」则每张有问题的图都列。</source>
        <translation>Maximale Anzahl gelisteter Bilder je Fehlertyp (Übersehen / Fehlalarm) und Klasse.
Der Bericht umfasst ca. 120 KB pro Bild; bei vielen Stichproben verkleinert ein niedrigerer Wert die PDF deutlich. Bei „Alle&quot; wird jedes problematische Bild gelistet.</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="690"/>
        <source> 张</source>
        <translation> Bilder</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="693"/>
        <source>全部</source>
        <translation>Alle</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="722"/>
        <location filename="../app/train/test_result_dialog.py" line="133"/>
        <source>导出 PDF 报告</source>
        <translation>PDF-Bericht exportieren</translation>
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
        <translation>Alle Bilder mit Übersehenem oder Fehlalarm mit Rahmen in ein PDF exportieren</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="101"/>
        <source>异常检测的逐图结果已写成 CSV, 不支持导出画框 PDF</source>
        <translation>Die Ergebnisse der Anomalieerkennung pro Bild wurden als CSV geschrieben; der Export als PDF mit Rahmen wird nicht unterstützt</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="103"/>
        <source>本次测试没有逐图错误明细, 无法导出</source>
        <translation>Dieser Test enthält keine Fehlerdetails pro Bild; Export nicht möglich</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="115"/>
        <source>保存 PDF 报告</source>
        <translation>PDF-Bericht speichern</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="116"/>
        <source>PDF 文件 (*.pdf)</source>
        <translation>PDF-Dateien (*.pdf)</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="122"/>
        <source>正在生成...</source>
        <translation>Wird erstellt...</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="140"/>
        <source>无需导出</source>
        <translation>Nichts zu exportieren</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="141"/>
        <source>本次测试没有漏检也没有误检, 没有内容可写.</source>
        <translation>Dieser Test hat weder Übersehenes noch Fehlalarme; nichts zu schreiben.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="144"/>
        <source>导出完成</source>
        <translation>Export abgeschlossen</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="145"/>
        <source>PDF 报告已保存到:
{}</source>
        <translation>PDF-Bericht gespeichert unter:
{}</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="149"/>
        <source>导出失败</source>
        <translation>Export fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="176"/>
        <source>按&quot;张&quot;统计 · 检出 1 个即算检出</source>
        <translation>Nach Bild · ein erkannter Rahmen zählt als erkannt</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="178"/>
        <source> · 有标注 {} 张</source>
        <translation> · {} Bilder mit Labels</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="182"/>
        <source>检出图像</source>
        <translation>Erkannte Bilder</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="183"/>
        <location filename="../app/train/test_result_dialog.py" line="198"/>
        <source>检出率 </source>
        <translation>Trefferquote </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="185"/>
        <source>未检出图像</source>
        <translation>Nicht erkannte Bilder</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="186"/>
        <source>未检出率 </source>
        <translation>Übersehensquote </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="190"/>
        <source>误检率 </source>
        <translation>Fehlalarmquote </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="195"/>
        <source>按&quot;标注框&quot;统计 · 标注总数 {}</source>
        <translation>Nach Rahmen · {} Rahmen insgesamt</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="218"/>
        <source>按&quot;张&quot;统计 · 每张图判一个类别</source>
        <translation>Nach Bild · eine Klasse pro Bild</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="223"/>
        <location filename="../app/train/test_result_dialog.py" line="255"/>
        <source>判断正确</source>
        <translation>Richtig</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="225"/>
        <location filename="../app/train/test_result_dialog.py" line="257"/>
        <source>判断错误</source>
        <translation>Falsch</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="228"/>
        <location filename="../app/train/test_result_dialog.py" line="276"/>
        <source>精度</source>
        <translation>Genauigkeit</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="250"/>
        <source>按&quot;张&quot;统计 · 整图判良品/不良品</source>
        <translation>Zählung pro Bild · ganzes Bild als Gutteil/Schlechtteil bewertet</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="275"/>
        <source>总图数</source>
        <translation>Bilder gesamt</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="275"/>
        <source>正确</source>
        <translation>Richtig</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="276"/>
        <source>错误</source>
        <translation>Falsch</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="235"/>
        <source>整体精度 {:.1f}%, &quot;{}&quot;类错误最多({} 张), 是拉低精度的主要原因.</source>
        <translation>Gesamtgenauigkeit {:.1f}%. Klasse „{}&quot; hat die meisten Fehler ({} Bilder) und ist die Hauptursache für die niedrigere Genauigkeit.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="295"/>
        <source>(根目录散图)</source>
        <translation>(lose Bilder im Wurzelordner)</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="298"/>
        <source>本批只有一类样本({}), 定不出判定阈值, 只报告分数; 补一些异常样本重新训练才有可交付的阈值.</source>
        <translation>Dieser Stapel enthält nur eine Klasse ({}), daher lässt sich keine Entscheidungsschwelle ableiten; es werden nur Werte ausgegeben. Erst mit zusätzlichen anomalen Beispielen und erneutem Training gibt es eine belastbare Schwelle.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="300"/>
        <source>良品类别: {}, 判定阈值 {:.4f}.</source>
        <translation>Gutklasse: {}, Entscheidungsschwelle {:.4f}.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="305"/>
        <source> 无漏检, 无误检.</source>
        <translation> Kein Übersehenes, keine Fehlalarme.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="309"/>
        <source> 漏检 {} 张(不良判成良品), 误检 {} 张(良品判成不良品); &quot;{}&quot;类错误最多({} 张).</source>
        <translation> {} übersehen (Schlechtteil als Gutteil bewertet), {} Fehlalarme (Gutteil als Schlechtteil bewertet); Klasse „{}“ hat die meisten Fehler ({}).</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="341"/>
        <source>整体漏检偏多(漏检 {} 个, 多于误检 {} 个).&quot;{}&quot;类漏检最多({} 个), 是检出率低的主要原因.</source>
        <translation>Insgesamt überwiegt Übersehenes ({} übersehen gegenüber {} Fehlalarmen). Klasse „{}&quot; hat die meisten übersehenen Objekte ({}) und ist die Hauptursache für die niedrige Trefferquote.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="347"/>
        <source>整体误检偏多(误检 {} 个, 多于漏检 {} 个).&quot;{}&quot;类误检最多({} 个), 是准确率低的主要原因.</source>
        <translation>Insgesamt überwiegen Fehlalarme ({} Fehlalarme gegenüber {} übersehenen). Klasse „{}&quot; hat die meisten Fehlalarme ({}) und ist die Hauptursache für die niedrige Genauigkeit.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="351"/>
        <source>模型表现良好: 无漏检, 无误检.</source>
        <translation>Das Modell ist gut: kein Übersehenes und keine Fehlalarme.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="353"/>
        <source>另有 {} 处位置对但类别判错(报告里用紫框标出),属分类能力不足, 需补易混淆类别的区分性样本.</source>
        <translation>Weitere {} Rahmen sind korrekt positioniert, aber falsch klassifiziert (im Bericht violett markiert). Das deutet auf zu schwache Klassifizierung hin; mehr unterscheidbare Beispiele für leicht verwechselbare Klassen ergänzen.</translation>
    </message>
</context>
<context>
    <name>TestRunner</name>
    <message>
        <location filename="../app/train/test_runner.py" line="282"/>
        <source>覆盖已有标注 {}</source>
        <translation>Vorhandene Annotationen überschreiben {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="312"/>
        <source>明细初始化失败: {}</source>
        <translation>Detailinitialisierung fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="321"/>
        <source>明细目录创建失败: {}</source>
        <translation>Detailordner erstellen fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="349"/>
        <source>明细写入失败: {}</source>
        <translation>Details schreiben fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="431"/>
        <source>当前安装缺少所需组件, 无法执行测试</source>
        <translation>In dieser Installation fehlen erforderliche Komponenten, Test nicht möglich</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="433"/>
        <source>加载模型: {}</source>
        <translation>Modell laden: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="449"/>
        <source>推理已优化: {}</source>
        <translation>Inferenz optimiert: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="465"/>
        <source>测试图片 {} 张</source>
        <translation>{} Testbilder</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="515"/>
        <source>预测失败 {}: {}</source>
        <translation>Vorhersage fehlgeschlagen {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="529"/>
        <source>输出标注失败 {}: {}</source>
        <translation>Annotationen ausgeben fehlgeschlagen {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="584"/>
        <source>WARN 标签目录存在但所有 {} 张图都没读到 GT,请确认标签是 .txt (YOLO) 或 .json (labelme)</source>
        <translation>WARN Labelordner vorhanden, aber für alle {} Bilder wurde kein GT gelesen, bitte prüfen, ob die Labels .txt (YOLO) oder .json (labelme) sind</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="589"/>
        <source>WARN {} 张图缺标签文件</source>
        <translation>WARN {} Bilder ohne Labeldatei</translation>
    </message>
</context>
<context>
    <name>TestWorker</name>
    <message>
        <location filename="../app/train/test_worker.py" line="80"/>
        <source>run 开始</source>
        <translation>run gestartet</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="93"/>
        <source>启动子进程: {} {}</source>
        <translation>Unterprozess starten: {} {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="105"/>
        <source>启动子进程失败: {}</source>
        <translation>Unterprozess starten fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="112"/>
        <source>启动测试进程失败: {}</source>
        <translation>Testprozess konnte nicht gestartet werden: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="114"/>
        <location filename="../app/train/test_worker.py" line="116"/>
        <source>子进程已启动 pid={}</source>
        <translation>Unterprozess gestartet pid={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="148"/>
        <source>进入轮询循环</source>
        <translation>Polling-Schleife gestartet</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="158"/>
        <source>轮询中: 文件={}B 已读{}行 子进程={}</source>
        <translation>Polling: Datei={}B, {} Zeilen gelesen, Unterprozess={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="168"/>
        <source>轮询异常:
</source>
        <translation>Polling-Ausnahme: 
</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="176"/>
        <source>轮询结束 rc={}</source>
        <translation>Polling beendet rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="178"/>
        <source>子进程退出 rc={}</source>
        <translation>Unterprozess beendet rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="188"/>
        <source>测试未能完成, 详情见日志</source>
        <translation>Test konnte nicht abgeschlossen werden, Details siehe Protokoll</translation>
    </message>
</context>
<context>
    <name>TrainDialog</name>
    <message>
        <location filename="../ui/train.ui" line="14"/>
        <location filename="../ui/train.ui" line="40"/>
        <location filename="../app/train/dialogs.py" line="470"/>
        <source>训练</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="50"/>
        <location filename="../ui/train.ui" line="144"/>
        <source>检测</source>
        <translation>Erkennung</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="93"/>
        <source>模型与数据</source>
        <translation>Modell &amp; Daten</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="133"/>
        <source>任务类型</source>
        <translation>Aufgabentyp</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="149"/>
        <source>分割</source>
        <translation>Segmentierung</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="154"/>
        <source>分类</source>
        <translation>Klassifizierung</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="159"/>
        <source>异常检测</source>
        <translation>Anomalieerkennung</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="167"/>
        <source>型号</source>
        <translation>Modell</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="180"/>
        <location filename="../app/train/dialogs.py" line="665"/>
        <source>训练集</source>
        <translation>Trainingsset</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="200"/>
        <source>验证集</source>
        <translation>Validierungsset</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="220"/>
        <source>设备</source>
        <translation>Gerät</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="233"/>
        <source>架构</source>
        <translation>Architektur</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="266"/>
        <source>训练超参</source>
        <translation>Hyperparameter</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="306"/>
        <location filename="../app/train/dialogs.py" line="546"/>
        <source>轮次</source>
        <translation>Epochen</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="319"/>
        <source>优化器</source>
        <translation>Optimierer</translation>
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
        <translation>Beendet früher, wenn keine Verbesserung mehr eintritt; 0 deaktiviert</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="385"/>
        <location filename="../app/train/dialogs.py" line="552"/>
        <source>学习率</source>
        <translation>Lernrate</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="422"/>
        <source>初始学习率，训练中自动衰减</source>
        <translation>Anfängliche Lernrate, wird beim Training automatisch reduziert</translation>
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
        <translation>Bildgröße</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="482"/>
        <location filename="../app/train/dialogs.py" line="430"/>
        <location filename="../app/train/dialogs.py" line="434"/>
        <source>32 的倍数</source>
        <translation>Vielfaches von 32</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="498"/>
        <location filename="../app/train/dialogs.py" line="545"/>
        <source>梯度累积</source>
        <translation>Grad-Akkum.</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="535"/>
        <source>显存不足时调大，等效批次 × N</source>
        <translation>Bei VRAM-Mangel erhöhen; effektive Batch × N</translation>
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
        <translation>Ausgabe</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="627"/>
        <source>输出路径</source>
        <translation>Ausgabepfad</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="642"/>
        <source>留空则自动按时间生成目录</source>
        <translation>Leer lassen für automatischen Ordner mit Zeitstempel</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="655"/>
        <source>选择路径</source>
        <translation>Durchsuchen</translation>
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
        <translation>Trainings- und Validierungsset wählen</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="760"/>
        <location filename="../app/train/dialogs.py" line="559"/>
        <source>取消</source>
        <translation>Abbrechen</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="773"/>
        <location filename="../app/train/dialogs.py" line="1114"/>
        <location filename="../app/train/dialogs.py" line="1123"/>
        <location filename="../app/train/dialogs.py" line="1131"/>
        <location filename="../app/train/dialogs.py" line="1150"/>
        <source>加入队列</source>
        <translation>Zur Warteschlange</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="786"/>
        <location filename="../app/train/dialogs.py" line="1062"/>
        <location filename="../app/train/dialogs.py" line="1072"/>
        <location filename="../app/train/dialogs.py" line="1095"/>
        <source>开始训练</source>
        <translation>Training starten</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="34"/>
        <source>正在检测显卡...</source>
        <translation>GPUs werden erkannt...</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="146"/>
        <source>数据集&quot;{}&quot;尚未导入图像或路径无效, 请先导入该数据集再训练</source>
        <translation>Datensatz „{}&quot; hat keine importierten Bilder oder der Pfad ist ungültig. Zuerst importieren, dann trainieren</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="153"/>
        <source>数据集&quot;{}&quot;尚未导入标签或路径无效, 请先导入该数据集再训练</source>
        <translation>Datensatz „{}&quot; hat keine importierten Labels oder der Pfad ist ungültig. Zuerst importieren, dann trainieren</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="182"/>
        <location filename="../app/train/dialogs.py" line="1124"/>
        <source>请先选择输出路径</source>
        <translation>Zuerst einen Ausgabepfad wählen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="195"/>
        <source>数据集&quot;{}/{}&quot;不是分类数据集(标签格式={}), 无法训练图像分类</source>
        <translation>Datensatz „{}/{}&quot; ist kein Klassifizierungs-Datensatz (Labelformat={}); Bildklassifizierung nicht möglich</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="198"/>
        <location filename="../app/train/dialogs.py" line="203"/>
        <location filename="../app/train/dialogs.py" line="1031"/>
        <source>未知</source>
        <translation>unbekannt</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="200"/>
        <source>数据集&quot;{}/{}&quot;不是分类数据集(标签格式={}), 无法训练异常检测</source>
        <translation>Datensatz „{}/{}“ ist kein Klassifizierungsdatensatz (Labelformat={}), Anomalieerkennung kann nicht trainiert werden</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="205"/>
        <source>数据集&quot;{}/{}&quot;是分类数据集, 无法训练{}任务</source>
        <translation>Datensatz „{}/{}&quot; ist ein Klassifizierungs-Datensatz; {} kann nicht trainiert werden</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="219"/>
        <source>请至少选择一个训练集数据集</source>
        <translation>Mindestens einen Trainings-Datensatz wählen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="221"/>
        <source>请至少选择一个验证集数据集</source>
        <translation>Mindestens einen Validierungs-Datensatz wählen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="270"/>
        <source>未选数据集</source>
        <translation>kein Datensatz gewählt</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="416"/>
        <source>目标检测推荐图像尺寸: 640(可设为 32 的倍数如 640/672)</source>
        <translation>Empfohlene Bildgröße für Erkennung: 640 (Vielfaches von 32, z. B. 640/672)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="418"/>
        <source>图像分割推荐尺寸: 636(必须为 12 的倍数, 如 636/648/660)</source>
        <translation>Empfohlene Größe für Segmentierung: 636 (muss ein Vielfaches von 12 sein, z. B. 636/648/660)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="420"/>
        <source>CNN 分割推荐尺寸: 640(需为 32 的倍数)</source>
        <translation>Empfohlene Größe für CNN-Segmentierung: 640 (muss ein Vielfaches von 32 sein)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="422"/>
        <source>图像分类推荐尺寸: 224(小图用 224, 较大图可到 256)</source>
        <translation>Empfohlene Größe für Klassifizierung: 224 (224 für kleine Bilder, bis 256 bei größeren)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="424"/>
        <source>异常检测推荐尺寸: 256; 缺陷很小时调到 512 更稳, 显存和耗时随之上升</source>
        <translation>Empfohlene Größe für Anomalieerkennung: 256; bei sehr kleinen Defekten ist 512 stabiler, VRAM-Bedarf und Laufzeit steigen dann</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="431"/>
        <source>12 的倍数</source>
        <translation>Vielfaches von 12</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="432"/>
        <source>建议 224</source>
        <translation>224 empfohlen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="435"/>
        <source>建议 256</source>
        <translation>256 empfohlen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="641"/>
        <source>训练集 {} 个 · 验证集 {} 个 · 共 {} 张图</source>
        <translation>Trainingssets {} · Validierungssets {} · {} Bilder gesamt</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="644"/>
        <source>未选择验证集</source>
        <translation>kein Validierungsset gewählt</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="646"/>
        <source>已标注, 可直接训练</source>
        <translation>annotiert, direkt trainierbar</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="648"/>
        <source>有 {} 个数据集尚未标注</source>
        <translation>{} Datensatz/Datensätze noch nicht annotiert</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="662"/>
        <source>请选择验证集</source>
        <translation>Validierungs-Datensätze wählen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="744"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>Ein Training läuft bereits; zuerst stoppen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="835"/>
        <source>异常检测算法自带学习率与优化器, 不需要设置</source>
        <translation>Anomalieerkennungs-Algorithmen bringen Lernrate und Optimierer mit; hier ist nichts einzustellen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="862"/>
        <source>建库型算法只提取特征建立记忆库, 没有训练轮次</source>
        <translation>Speicherbank-basierte Algorithmen extrahieren nur Merkmale und bauen die Speicherbank auf; Trainingsepochen gibt es nicht</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="971"/>
        <source>仅建库</source>
        <translation>Nur Speicherbank</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1001"/>
        <source>请至少选择一个数据集</source>
        <translation>Mindestens einen Datensatz auswählen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1005"/>
        <location filename="../app/train/dialogs.py" line="1015"/>
        <source>&quot;{}&quot;不能为空</source>
        <translation>„{}&quot; darf nicht leer sein</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1010"/>
        <source>&quot;{}&quot;必须是整数(当前: {})</source>
        <translation>„{}&quot; muss eine ganze Zahl sein (aktuell: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1020"/>
        <source>&quot;{}&quot;必须是数字(当前: {})</source>
        <translation>„{}&quot; muss eine Zahl sein (aktuell: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1030"/>
        <source>数据集&quot;{}/{}&quot;不是按分类导入的数据集(标签格式={}),无法训练{}</source>
        <translation>Datensatz „{}/{}“ wurde nicht als Klassifizierungsdatensatz importiert (Labelformat={}), {} kann nicht trainiert werden</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1035"/>
        <source>数据集&quot;{}/{}&quot;是分类数据集,无法训练{}任务</source>
        <translation>Datensatz „{}/{}&quot; ist ein Klassifizierungs-Datensatz; {} kann nicht trainiert werden</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1042"/>
        <source>选择输出目录</source>
        <translation>Ausgabeordner wählen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1056"/>
        <source>当前安装缺少 CNN 架构所需的组件, 无法训练.
请重新安装软件后再试</source>
        <translation>In dieser Installation fehlen die für die CNN-Architektur erforderlichen Komponenten, Training nicht möglich.
Bitte installieren Sie die Software erneut</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1063"/>
        <source>当前已有训练在进行中, 请先停止!</source>
        <translation>Ein Training läuft bereits; zuerst stoppen!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1067"/>
        <source>参数校验未通过: {}</source>
        <translation>Parametervalidierung fehlgeschlagen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1068"/>
        <location filename="../app/train/dialogs.py" line="1110"/>
        <source>参数校验</source>
        <translation>Parametervalidierung</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1085"/>
        <source>训练启动失败: {}
{}</source>
        <translation>Training starten fehlgeschlagen: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1088"/>
        <source>训练启动失败</source>
        <translation>Training konnte nicht starten</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1096"/>
        <source>已有训练在进行中, 请先停止!</source>
        <translation>Ein Training läuft bereits; zuerst stoppen!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1098"/>
        <source>开始训练: 任务类型={} 训练集={} 验证集={}</source>
        <translation>Training starten: Aufgabentyp={} Trainingsset={} Validierungsset={}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1136"/>
        <source>队列</source>
        <translation>Warteschlange</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1137"/>
        <source>已更新该队列任务的参数</source>
        <translation>Parameter der Warteschlangen-Aufgabe aktualisiert</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1143"/>
        <source>加入队列失败</source>
        <translation>Hinzufügen zur Warteschlange fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1146"/>
        <source>加入训练队列: {} | {}</source>
        <translation>Zur Trainings-Warteschlange hinzufügen: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1151"/>
        <source>已加入队列(第 {} 个), 可在首页&quot;队列&quot;中查看或启动.</source>
        <translation>Zur Warteschlange hinzugefügt (Position {}). Auf der Startseite unter „Warteschlange&quot; prüfen oder starten.</translation>
    </message>
</context>
<context>
    <name>TrainMixin</name>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="47"/>
        <source>{} 训练中 0/{}</source>
        <translation>{} Training 0/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="86"/>
        <source>[train] 训练线程已结束但未返回结果, 按失败收尾</source>
        <translation>[train] Trainingsthread beendet, aber ohne Ergebnis, wird als Fehler gewertet</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="97"/>
        <source>仅停止当前</source>
        <translation>Nur aktuelles stoppen</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="98"/>
        <source>停止队列</source>
        <translation>Warteschlange stoppen</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <location filename="../app/mixins/train_mixin.py" line="121"/>
        <source>停止训练</source>
        <translation>Training stoppen</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <source>当前正在跑训练队列, 要停止到什么范围?</source>
        <translation>Eine Trainings-Warteschlange läuft. Wie weit soll gestoppt werden?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="102"/>
        <location filename="../app/mixins/train_mixin.py" line="103"/>
        <source>取消</source>
        <translation>Abbrechen</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <source>确定要停止当前训练吗?</source>
        <translation>Aktuelles Training stoppen?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="117"/>
        <source>手动停止训练: {}</source>
        <translation>Training manuell gestoppt: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="119"/>
        <source>[train] 训练进程 10 秒内未退出, 可能有子进程残留占用显存</source>
        <translation>[train] Trainingsprozess nach 10 Sekunden nicht beendet, möglicherweise belegen Unterprozesse noch VRAM</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="122"/>
        <source>训练进程未能完全退出, 可能仍有子进程占用显存.
建议稍等片刻再启动下一个任务.</source>
        <translation>Der Trainingsprozess wurde nicht vollständig beendet; Unterprozesse belegen möglicherweise noch VRAM.
Vor dem nächsten Task besser kurz warten.</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="134"/>
        <source>{} 训练中 {}/{}</source>
        <translation>{} Training {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="148"/>
        <source>进度 | 当前最好 AUROC</source>
        <translation>Fortschritt | Bester AUROC bisher</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="150"/>
        <source>进度 | 当前最好准确率</source>
        <translation>Fortschritt | beste Genauigkeit bisher</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="152"/>
        <source>进度 | 当前最好 mAP@50</source>
        <translation>Fortschritt | bester mAP@50 bisher</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="190"/>
        <source>训练失败(队列模式, 已跳过弹窗): {}</source>
        <translation>Training fehlgeschlagen (Warteschlangenmodus, Dialog übersprungen): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="192"/>
        <source>训练失败</source>
        <translation>Training fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="193"/>
        <source>训练过程中发生错误, Err:

{}</source>
        <translation>Während des Trainings ist ein Fehler aufgetreten, Err:

{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="216"/>
        <source>更新训练指标: record={} 已完成epoch={} map50={} acc={} 类别数={}</source>
        <translation>Trainingsmetriken aktualisieren: record={} abgeschlossene epoch={} map50={} acc={} Klassenanzahl={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="279"/>
        <source>已保存模型记录: {} | {}</source>
        <translation>Modelleintrag gespeichert: {} | {}</translation>
    </message>
</context>
<context>
    <name>TrainQueueDialog</name>
    <message>
        <location filename="../ui/train_queue.ui" line="14"/>
        <location filename="../ui/train_queue.ui" line="40"/>
        <location filename="../app/widgets/queue_dialog.py" line="32"/>
        <source>训练队列</source>
        <translation>Trainings-Warteschlange</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="50"/>
        <location filename="../app/widgets/queue_dialog.py" line="121"/>
        <source>空闲</source>
        <translation>Leerlauf</translation>
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
        <translation>Aufgabe</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="108"/>
        <source>数据集</source>
        <translation>Datensatz</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="113"/>
        <source>型号</source>
        <translation>Modell</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="118"/>
        <source>轮次</source>
        <translation>Epochen</translation>
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
        <translation>Die Warteschlange ist leer. Im Trainingsdialog auf „Zur Warteschlange&quot; klicken, um Aufgaben hinzuzufügen</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="199"/>
        <source>上移</source>
        <translation>Nach oben</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="209"/>
        <source>下移</source>
        <translation>Nach unten</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="219"/>
        <location filename="../app/widgets/queue_dialog.py" line="253"/>
        <source>移除</source>
        <translation>Entfernen</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="229"/>
        <source>清理已结束</source>
        <translation>Beendete löschen</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="252"/>
        <source>编辑</source>
        <translation>Bearbeiten</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="259"/>
        <source>关闭</source>
        <translation>Schließen</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="272"/>
        <location filename="../app/widgets/queue_dialog.py" line="142"/>
        <source>开始队列</source>
        <translation>Warteschlange starten</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="21"/>
        <source>队列为空, 可在训练界面点&quot;加入队列&quot;添加任务</source>
        <translation>Die Warteschlange ist leer. Im Trainingsdialog auf „Zur Warteschlange&quot; klicken, um Aufgaben hinzuzufügen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="111"/>
        <source>运行中</source>
        <translation>Läuft</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="111"/>
        <source>队列正在串行执行</source>
        <translation>Die Warteschlange führt die Aufgaben nacheinander aus</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>待启动</source>
        <translation>Wartet auf Start</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="114"/>
        <source>有 {} 个任务等待启动</source>
        <translation>{} Aufgabe(n) warten auf den Start</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="116"/>
        <source>训练中</source>
        <translation>Training</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="116"/>
        <source>当前有训练在进行(非队列启动)</source>
        <translation>Ein Training läuft (nicht aus der Warteschlange gestartet)</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>已结束</source>
        <translation>Beendet</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="119"/>
        <source>没有待执行的任务, 点&quot;重新开始队列&quot;可重跑</source>
        <translation>Keine offenen Aufgaben; über „Warteschlange neu starten&quot; erneut ausführen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="125"/>
        <source>共 {} 个: 等待 {} · 完成 {} · 失败 {}</source>
        <translation>{} gesamt: {} wartend · {} fertig · {} fehlgeschlagen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="128"/>
        <source>正在训练&quot;{}&quot; · {}</source>
        <translation>Training „{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="131"/>
        <source>下一个: &quot;{}&quot; · {}</source>
        <translation>Nächste: „{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="144"/>
        <location filename="../app/widgets/queue_dialog.py" line="181"/>
        <source>重新开始队列</source>
        <translation>Warteschlange neu starten</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="166"/>
        <location filename="../app/widgets/queue_dialog.py" line="188"/>
        <source>队列</source>
        <translation>Warteschlange</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="167"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>Ein Training läuft bereits; zuerst stoppen</translation>
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
        <translation>Es gibt keine wartenden Aufgaben in der Warteschlange.

Erneut ausführen: {}

Erneut einreihen und Training starten?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="189"/>
        <source>队列启动失败, 请查看日志</source>
        <translation>Warteschlange konnte nicht gestartet werden; siehe Protokoll</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="205"/>
        <location filename="../app/widgets/queue_dialog.py" line="209"/>
        <source>移除任务</source>
        <translation>Aufgabe entfernen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="206"/>
        <source>训练中的任务不能移除, 请先停止</source>
        <translation>Eine laufende Aufgabe kann nicht entfernt werden; zuerst stoppen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="210"/>
        <source>确定从队列中移除&quot;{}&quot;吗?</source>
        <translation>„{}&quot; aus der Warteschlange entfernen?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="217"/>
        <source>清理</source>
        <translation>Löschen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="218"/>
        <source>没有已结束的任务</source>
        <translation>Keine beendeten Aufgaben</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="220"/>
        <source>[队列] 已清理 {} 个已结束任务</source>
        <translation>[队列] {} beendete Aufgaben entfernt</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="227"/>
        <source>编辑任务</source>
        <translation>Aufgabe bearbeiten</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="228"/>
        <source>训练中的任务不能编辑, 请先停止</source>
        <translation>Eine laufende Aufgabe kann nicht bearbeitet werden; zuerst stoppen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="244"/>
        <source>重新入队</source>
        <translation>Erneut einreihen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="246"/>
        <location filename="../app/widgets/queue_dialog.py" line="267"/>
        <source>打开输出目录</source>
        <translation>Ausgabeordner öffnen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="248"/>
        <source>在模型界面查看</source>
        <translation>In der Modellverwaltung ansehen</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="268"/>
        <source>目录不存在: {}</source>
        <translation>Ordner existiert nicht: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="269"/>
        <source>未设置</source>
        <translation>Nicht gesetzt</translation>
    </message>
</context>
<context>
    <name>TrainRunner</name>
    <message>
        <location filename="../app/train/train_runner.py" line="78"/>
        <location filename="../app/train/yolo_train_runner.py" line="171"/>
        <source>输出路径: {}</source>
        <translation>Ausgabepfad: {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="79"/>
        <location filename="../app/train/yolo_train_runner.py" line="172"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Ausgabeverzeichnis dieses Trainings (Zeitstempel): {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="81"/>
        <source>训练配置文件已保存 → {}</source>
        <translation>Trainingskonfiguration gespeichert → {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="103"/>
        <source>分割模型 resolution 已自动取整: {} → {} (block={})</source>
        <translation>Segmentierungsmodell resolution automatisch gerundet: {} → {} (block={})</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="105"/>
        <location filename="../app/train/yolo_train_runner.py" line="209"/>
        <source>使用模型 {} device={} epochs={} batch={} resolution={}</source>
        <translation>Modell verwendet {} device={} epochs={} batch={} resolution={}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="174"/>
        <location filename="../app/train/yolo_train_runner.py" line="237"/>
        <source>训练完成</source>
        <translation>Training abgeschlossen</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="183"/>
        <location filename="../app/train/yolo_train_runner.py" line="244"/>
        <source>生成类别文件: {}</source>
        <translation>Klassendatei erzeugen: {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="90"/>
        <location filename="../app/train/yolo_train_runner.py" line="178"/>
        <source>预训练权重缺失: 请先在权重管理里下载 {} 档的模型</source>
        <translation>Vorabgewichte fehlen: Bitte zuerst im Gewichts-Manager das Modell der Stufe {} herunterladen</translation>
    </message>
</context>
<context>
    <name>TrainWorker</name>
    <message>
        <location filename="../app/train/train_worker.py" line="481"/>
        <source>训练监控异常, 已终止.

{}</source>
        <translation>Trainingsüberwachung fehlerhaft; abgebrochen.

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="490"/>
        <source>训练结果文件读取失败: {}

{}</source>
        <translation>Trainingsergebnisdatei konnte nicht gelesen werden: {}

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="495"/>
        <source>训练进程异常退出 (code={})

--- 子进程输出(尾部) ---
{}</source>
        <translation>Trainingsprozess wurde unerwartet beendet (code={})

--- Unterprozess-Ausgabe (Ende) ---
{}</translation>
    </message>
</context>
<context>
    <name>Utils</name>
    <message>
        <location filename="../app/core/utils.py" line="57"/>
        <location filename="../app/core/utils.py" line="69"/>
        <source>{}秒</source>
        <translation>{} Sek </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="63"/>
        <source>{}天</source>
        <translation>{} T </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="65"/>
        <source>{}小时</source>
        <translation>{} Std </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="67"/>
        <source>{}分</source>
        <translation>{} Min </translation>
    </message>
</context>
<context>
    <name>_ModelRow</name>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="113"/>
        <source>已就绪</source>
        <translation>Bereit</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="119"/>
        <source>未下载</source>
        <translation>Nicht geladen</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="124"/>
        <source>校验中...</source>
        <translation>Wird geprüft...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="140"/>
        <source>失败</source>
        <translation>Fehlgeschlagen</translation>
    </message>
</context>
<context>
    <name>_TrainStartDialog</name>
    <message>
        <location filename="../app/train/dialogs.py" line="280"/>
        <source>训练即将开始</source>
        <translation>Training startet gleich</translation>
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
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/add_label.ui" line="49"/>
        <source>导入</source>
        <translation>Importieren</translation>
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
        <translation>Rechteck</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="35"/>
        <source>多边形</source>
        <translation>Polygon</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="46"/>
        <source>删除图像</source>
        <translation>Bild löschen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="70"/>
        <source>设置</source>
        <translation>Einstellungen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="90"/>
        <source>标签列表</source>
        <translation>Label-Liste</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="113"/>
        <source>添加标签</source>
        <translation>Label hinzufügen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="116"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="160"/>
        <source>标注信息</source>
        <translation>Annotationen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="203"/>
        <source>图像信息</source>
        <translation>Bildinfo</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="230"/>
        <source>剪切板</source>
        <translation>Zwischenablage</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="295"/>
        <source>上一张(A)</source>
        <translation>Zurück (A)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="302"/>
        <source>下一张(D)</source>
        <translation>Weiter (D)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="352"/>
        <source>标注参数</source>
        <translation>Annotationsparameter</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="364"/>
        <source>角度范围</source>
        <translation>Winkelbereich</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="378"/>
        <source>~</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="412"/>
        <source>融合强度</source>
        <translation>Mischstärke</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="446"/>
        <source>亮度调节</source>
        <translation>Helligkeit</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="480"/>
        <source>填充颜色</source>
        <translation>Füllfarbe</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="487"/>
        <source>点击打开取色器, 选任意颜色</source>
        <translation>Klicken, um den Farbwähler zu öffnen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="500"/>
        <source>支持 #RRGGBB / #RGB / 255,255,255 / black / 白 等写法, 也可以点左边色块打开取色器</source>
        <translation>Unterstützt #RRGGBB / #RGB / 255,255,255 / black / weiß — oder links auf das Farbfeld klicken, um den Farbwähler zu öffnen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="503"/>
        <source>#RRGGBB</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="510"/>
        <source>自定义颜色</source>
        <translation>Eigene Farbe</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="537"/>
        <source>常用色</source>
        <translation>Vorgaben</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="568"/>
        <source>恢复默认</source>
        <translation>Zurücksetzen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="588"/>
        <source>完成</source>
        <translation>Fertig</translation>
    </message>
</context>
</TS>
