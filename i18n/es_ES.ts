<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="es_ES">
<context>
    <name>AdCommon</name>
    <message>
        <location filename="../app/train/ad_common.py" line="92"/>
        <source>找不到可写的纯英文暂存目录(异常检测的底层库不支持中文路径), 请把输出路径改到纯英文目录下</source>
        <translation>No se encontró ningún directorio temporal de solo ASCII con permisos de escritura (la librería de detección de anomalías no admite rutas no ASCII); cambie la ruta de salida a un directorio de solo ASCII</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="153"/>
        <location filename="../app/train/ad_common.py" line="655"/>
        <source>(根目录散图)</source>
        <translation>(imágenes sueltas en la raíz)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="176"/>
        <source>数据集里没找到图像, 请先导入数据</source>
        <translation>No se encontraron imágenes en el conjunto de datos; importe primero los datos</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="181"/>
        <source>无法从类别名判断哪个是正常品, 请把放良品图的那个文件夹改名为 {} 之一; 现有类别: {}</source>
        <translation>No se puede determinar cuál es la clase buena a partir de los nombres de clase; cambie el nombre de la carpeta de imágenes buenas a uno de {}; clases actuales: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="187"/>
        <source>训练集里没有图像</source>
        <translation>El conjunto de entrenamiento no tiene imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="191"/>
        <source>训练集里只有&quot;{}&quot;一类, 而良品类是&quot;{}&quot;; 请把良品图所在的类别文件夹挂到训练集上</source>
        <translation>El conjunto de entrenamiento solo tiene la clase &quot;{}&quot;, pero la clase buena es &quot;{}&quot;; asigne al conjunto de entrenamiento la carpeta de clase que contiene las imágenes buenas</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="199"/>
        <source>训练集里既没有&quot;{}&quot;类、又不止一类, 无法确定拿哪批图建库; 现有类别: {}</source>
        <translation>El conjunto de entrenamiento no tiene la clase &quot;{}&quot; y tiene más de una clase, así que no está claro qué imágenes usar para crear el banco de memoria; clases actuales: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="240"/>
        <source>训练集根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>La raíz del conjunto de entrenamiento tiene imágenes sueltas y subcarpetas; no se puede determinar a qué clase pertenecen las imágenes sueltas; colóquelas en una misma carpeta de clase</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="274"/>
        <source>没有找到任何图像, 请检查数据集</source>
        <translation>No se encontró ninguna imagen; revise el conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="276"/>
        <source>根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>La raíz tiene imágenes sueltas y subcarpetas; no se puede determinar a qué clase pertenecen las imágenes sueltas; colóquelas en una misma carpeta de clase</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="281"/>
        <source>无法判断哪个类别是良品, 现有类别: {}.
请把良品图放在名为 {} 一类的子文件夹里, 或按训练时的方式重新导入数据集</source>
        <translation>No se puede determinar qué clase es la buena; clases actuales: {}.
Coloque las imágenes buenas en una subcarpeta llamada como una de {} o vuelva a importar el conjunto de datos igual que en el entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="422"/>
        <source>未知的异常检测算法: {}</source>
        <translation>Algoritmo de detección de anomalías desconocido: {}</translation>
    </message>
</context>
<context>
    <name>AdPackage</name>
    <message>
        <location filename="../app/train/ad_package.py" line="88"/>
        <source>正在复制模型文件...</source>
        <translation>Copiando archivo de modelo...</translation>
    </message>
</context>
<context>
    <name>AdTestRunner</name>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="47"/>
        <source>缺少测试依赖: {}</source>
        <translation>Faltan dependencias de prueba: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="77"/>
        <source>加载异常检测模型: {}</source>
        <translation>Cargando el modelo de detección de anomalías: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="86"/>
        <source>算法={} 图像尺寸={} 阈值={:.6f}</source>
        <translation>Algoritmo={} tamaño de imagen={} umbral={:.6f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="88"/>
        <source>原尺寸</source>
        <translation>tamaño original</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="96"/>
        <source>没有可用的图像目录, 请检查数据集</source>
        <translation>No hay ningún directorio de imágenes utilizable; revise el conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="107"/>
        <source>测试图片 {} 张, 良品类别: {}</source>
        <translation>Probando {} imágenes, clase correcta: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="144"/>
        <source>没有取到任何图像, 请检查数据集</source>
        <translation>No se leyó ninguna imagen; revise el conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="151"/>
        <source>沿用训练时定下的阈值 {:.6f}</source>
        <translation>Se usa el umbral fijado durante el entrenamiento {:.6f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="155"/>
        <source>模型里没有阈值, 本批又只有一类样本, 定不出判定阈值, 只报告分数</source>
        <translation>El modelo no tiene umbral y este lote solo tiene una clase, así que no se puede derivar el umbral de decisión; solo se informan las puntuaciones</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="159"/>
        <source>模型里没有阈值, 已按本批数据现挑 {:.6f}(精度会偏乐观)</source>
        <translation>El modelo no tiene umbral; se eligió {:.6f} con este lote (la exactitud será optimista)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="189"/>
        <source>完成: {} 张, 没有判定阈值, 只报告分数</source>
        <translation>Listo: {} imágenes, sin umbral de decisión, solo se informan las puntuaciones</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="195"/>
        <source>完成: {} 张, 检出异常 {} 张</source>
        <translation>Listo: {} imágenes, {} anomalías detectadas</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="199"/>
        <source>完成: {} 张, 准确率 {:.4f}, 漏检 {} 张, 误检 {} 张</source>
        <translation>Listo: {} imágenes, exactitud {:.4f}, {} omitidos, {} falsos positivos</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="204"/>
        <source>  image AUROC = {:.4f}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="220"/>
        <source>模型里没有判定阈值, 不输出异常区域</source>
        <translation>El modelo no tiene umbral de decisión; no se escriben regiones anómalas</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="223"/>
        <source>异常</source>
        <translation>Anomalía</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="233"/>
        <source>提取异常区域失败 {}: {}</source>
        <translation>Error al extraer la región anómala {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="250"/>
        <source>输出异常区域失败 {}: {}</source>
        <translation>Error al escribir la región anómala {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="254"/>
        <source>已为 {} 张不良品图写出异常区域标注(图像同目录)</source>
        <translation>Se escribieron etiquetas de región anómala para {} imágenes defectuosas (junto a las imágenes)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="258"/>
        <source>另有 {} 张判为不良品, 但热力图没超过判定线, 未写标注</source>
        <translation>Otras {} imágenes se juzgaron defectuosas, pero su mapa de calor no superó la línea de decisión; no se escribieron etiquetas</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="277"/>
        <source>图像</source>
        <translation>Imagen</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="278"/>
        <source>类别</source>
        <translation>Clase</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="279"/>
        <source>真值</source>
        <translation>Valor real</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="280"/>
        <source>判定</source>
        <translation>Veredicto</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="281"/>
        <source>分数</source>
        <translation>Puntuación</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="282"/>
        <source>阈值</source>
        <translation>Umbral</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="283"/>
        <source>是否正确</source>
        <translation>¿Correcto?</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="298"/>
        <source>是</source>
        <translation>Sí</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="299"/>
        <source>否</source>
        <translation>No</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="301"/>
        <source>逐图明细: {}</source>
        <translation>Detalle por imagen: {}</translation>
    </message>
</context>
<context>
    <name>AdTrainRunner</name>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="49"/>
        <source>缺少训练依赖: {}</source>
        <translation>Faltan dependencias de entrenamiento: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="137"/>
        <source>anomalib {} / torch {}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="170"/>
        <source>输出路径: {}</source>
        <translation>Ruta de salida: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="172"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Directorio de salida de este entrenamiento (marca de tiempo): {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="186"/>
        <source>异常检测: 算法={} 骨干={} 轮次={} 批次={} 图像尺寸={} device={}</source>
        <translation>Detección de anomalías: algoritmo={} backbone={} épocas={} lote={} tamaño de imagen={} device={}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="198"/>
        <source>数据准备: 建库集 {} 张({}), 测试集 正常 {} 张 / 异常 {} 张</source>
        <translation>Datos listos: conjunto de banco {} imágenes ({}), conjunto de prueba {} correctas / {} anómalas</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="203"/>
        <source>  异常类别: {}</source>
        <translation>  clases anómalas: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="204"/>
        <source>(散图)</source>
        <translation>(imágenes sueltas)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="209"/>
        <source>  注意: 建库集里另有 {} 张非正常图, 未参与建库</source>
        <translation>  nota: el conjunto de banco tiene {} imágenes anómalas que no se usaron</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="213"/>
        <source>建库集里没有图像, 请检查数据集</source>
        <translation>El conjunto de banco no tiene imágenes; revise el conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="215"/>
        <source>测试集里没有图像, 请检查数据集</source>
        <translation>El conjunto de prueba no tiene imágenes; revise el conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="234"/>
        <source>数据集: 建库集 {} 张</source>
        <translation>Conjunto de datos: conjunto de banco {} imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="243"/>
        <source>模型构建完成({:.1f}s): {}</source>
        <translation>Modelo construido en {:.1f}s: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="261"/>
        <source>建库/训练完成({:.1f}s)</source>
        <translation>Banco/entrenamiento completados en {:.1f}s</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="274"/>
        <source>  评估中: {} 张</source>
        <translation>  evaluando: {} imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="283"/>
        <source>评估阶段失败, 只交付模型: {}</source>
        <translation>Error en la evaluación; solo se entrega el modelo: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="288"/>
        <source>评估完成({:.1f}s): {} 张</source>
        <translation>Evaluación completada en {:.1f}s: {} imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="291"/>
        <source>  测试集里只有一类样本, 定不出判定阈值(没有真值反差), AUROC 和准确率都算不了; 补一些异常样本重新训练才有交付阈值</source>
        <translation>  el conjunto de prueba solo tiene una clase, así que no se puede derivar el umbral de decisión (no hay contraste en la verdad de referencia) y no se pueden calcular ni AUROC ni exactitud; reentrene añadiendo muestras anómalas para obtener un umbral entregable</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="296"/>
        <source>评估完成({:.1f}s): {} 张, 准确率 {:.4f}</source>
        <translation>Evaluación completada en {:.1f}s: {} imágenes, exactitud {:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="300"/>
        <source>  image AUROC = {:.4f}  阈值 = {:.6f}(本批最优 F1 处)</source>
        <translation>  image AUROC = {:.4f}  umbral = {:.6f} (mejor F1 de este lote)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="303"/>
        <source>  漏检 {} 张(不良判成良品), 误检 {} 张</source>
        <translation>  {} omitidos (defectuosa juzgada correcta), {} falsos positivos</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="307"/>
        <source>  AUROC 无法计算</source>
        <translation>  no se puede calcular AUROC</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="321"/>
        <source>模型已保存: {} ({:.0f} MB)</source>
        <translation>Modelo guardado: {} ({:.0f} MB)</translation>
    </message>
</context>
<context>
    <name>AddLabelDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="168"/>
        <source>添加标签</source>
        <translation>Añadir etiqueta</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="185"/>
        <source>编辑标签</source>
        <translation>Editar etiqueta</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="187"/>
        <source>标签名称</source>
        <translation>Nombre de etiqueta</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="222"/>
        <source>标签名称, 多个用逗号分隔</source>
        <translation>Nombres de etiquetas, separar varios con comas</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="224"/>
        <source>导入</source>
        <translation>Importar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="231"/>
        <source>选择数据集...</source>
        <translation>Seleccionar conjunto de datos...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="254"/>
        <location filename="../app/annotation/annotation_dialog.py" line="259"/>
        <source>导入标签</source>
        <translation>Importar etiquetas</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="255"/>
        <source>请先选择一个数据集</source>
        <translation>Seleccione un conjunto de datos primero</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="260"/>
        <source>数据集&quot;{}&quot;还没有标签</source>
        <translation>El conjunto de datos &quot;{}&quot; aún no tiene etiquetas</translation>
    </message>
</context>
<context>
    <name>AnnotationDialog</name>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="208"/>
        <source>复制</source>
        <translation>Copiar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="210"/>
        <source>填充</source>
        <translation>Rellenar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="220"/>
        <source>粘贴</source>
        <translation>Pegar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="374"/>
        <source>标注 - {} / {}</source>
        <translation>Anotación - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="392"/>
        <location filename="../app/annotation/annotation_dialog.py" line="874"/>
        <source>矩形</source>
        <translation>Rectángulo</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="393"/>
        <location filename="../app/annotation/annotation_dialog.py" line="880"/>
        <source>多边形</source>
        <translation>Polígono</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="402"/>
        <source>标签列表</source>
        <translation>Etiquetas</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="403"/>
        <source>标注信息</source>
        <translation>Anotaciones</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="407"/>
        <source>上一张</source>
        <translation>Anterior</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="408"/>
        <source>下一张</source>
        <translation>Siguiente</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="443"/>
        <source>只在选中的多边形框内生效; A/D 切图或 Ctrl+S 才写盘</source>
        <translation>Solo se aplica dentro del polígono seleccionado; se guarda al cambiar de imagen con A/D o con Ctrl+S</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="481"/>
        <source>显示标注</source>
        <translation>Mostrar etiquetas</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="487"/>
        <source>文本标注</source>
        <translation>Anotación de texto</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="713"/>
        <source>编辑标签</source>
        <translation>Editar etiqueta</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1032"/>
        <source>转换</source>
        <translation>Convertir</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1033"/>
        <source>设置像素精度, 在像素面积后显示物理面积</source>
        <translation>Definir la escala de píxel para mostrar el área física tras el área en píxeles</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1037"/>
        <source>当前像素精度 {}, 点击修改</source>
        <translation>Escala de píxel actual {}, clic para cambiar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="563"/>
        <source>先在画布上点选一个多边形</source>
        <translation>Seleccione primero un polígono en el lienzo</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="566"/>
        <source>亮度调节只对多边形有效</source>
        <translation>El ajuste de brillo solo funciona en polígonos</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="326"/>
        <source>    类别: {}</source>
        <translation>    Clase: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="354"/>
        <source>删除本地文件</source>
        <translation>Eliminar archivo local</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="355"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="357"/>
        <location filename="../app/annotation/annotation_io.py" line="366"/>
        <source>删除图像</source>
        <translation>Eliminar imagen</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="358"/>
        <source>是否删除当前图像?

{}</source>
        <translation>¿Eliminar la imagen actual?

{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="361"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>La imagen y su archivo de etiquetas se eliminarán del disco. Esta acción no se puede deshacer</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="367"/>
        <source>无法访问主窗口, 删除失败</source>
        <translation>No se puede acceder a la ventana principal; error al eliminar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="380"/>
        <source>(无图像)</source>
        <translation>(sin imagen)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="696"/>
        <location filename="../app/annotation/annotation_dialog.py" line="820"/>
        <location filename="../app/annotation/annotation_dialog.py" line="826"/>
        <source>添加标签</source>
        <translation>Añadir etiqueta</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="697"/>
        <source>请先添加标签(点击&quot;+&quot;)</source>
        <translation>Añada una etiqueta primero (haga clic en &quot;+&quot;)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="733"/>
        <source>标注文字</source>
        <translation>Etiqueta de texto</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="734"/>
        <source>请输入框内的文字</source>
        <translation>Introduzca el texto dentro del cuadro</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="833"/>
        <source>剪切板  {}/{}</source>
        <translation>Portapapeles  {}/{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="858"/>
        <source>第 {} 个模板  {}x{}
左键选中用于粘贴, 右键 删除/导入/导出/清空</source>
        <translation>Plantilla {}  {}x{}
Clic izquierdo para seleccionar y pegar; clic derecho para eliminar / importar / exportar / vaciar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="890"/>
        <location filename="../app/annotation/annotation_dialog.py" line="685"/>
        <source>删除</source>
        <translation>Eliminar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="893"/>
        <source>导入</source>
        <translation>Importar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="894"/>
        <source>导出</source>
        <translation>Exportar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="896"/>
        <source>清空</source>
        <translation>Vaciar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="420"/>
        <location filename="../app/annotation/annotation_io.py" line="449"/>
        <location filename="../app/annotation/annotation_io.py" line="454"/>
        <source>导出剪切板</source>
        <translation>Exportar portapapeles</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="421"/>
        <source>剪切板是空的, 没有可导出的模板</source>
        <translation>El portapapeles está vacío; no hay plantillas que exportar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="424"/>
        <source>选择导出目录</source>
        <translation>Seleccionar directorio de exportación</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="450"/>
        <source>导出中断: {}
(已写出 {} 个)</source>
        <translation>Exportación interrumpida: {}
({} escritas)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="455"/>
        <source>已导出 {} 个模板(png + 同名 json)到:
{}</source>
        <translation>Se exportaron {} plantilla(s) (png + json con el mismo nombre) a:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="461"/>
        <source>选择导入目录</source>
        <translation>Seleccionar directorio de importación</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="468"/>
        <location filename="../app/annotation/annotation_io.py" line="472"/>
        <location filename="../app/annotation/annotation_io.py" line="506"/>
        <source>导入剪切板</source>
        <translation>Importar portapapeles</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="469"/>
        <source>读取目录失败: {}</source>
        <translation>Error al leer el directorio: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="473"/>
        <source>这个目录里没有 png 文件</source>
        <translation>No hay archivos png en este directorio</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="501"/>
        <source>已导入 {} 个模板到剪切板</source>
        <translation>Se importaron {} plantillas al portapapeles</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="503"/>
        <source>
其中 {} 个没有同名 json, 按矩形导入</source>
        <translation>
{} de ellas no tienen un json con el mismo nombre y se importaron como rectángulos</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="505"/>
        <source>
{} 个文件读不出来, 已跳过</source>
        <translation>
No se pudieron leer {} archivo(s); se omitieron</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="622"/>
        <source>修改类别</source>
        <translation>Cambiar clase</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="623"/>
        <source>移动图像文件失败:
{}</source>
        <translation>Error al mover el archivo de imagen:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="684"/>
        <source>编辑</source>
        <translation>Editar</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="780"/>
        <location filename="../app/annotation/annotation_dialog.py" line="787"/>
        <location filename="../app/annotation/annotation_io.py" line="524"/>
        <source>删除标签</source>
        <translation>Eliminar etiqueta</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="525"/>
        <source>正在统计标注文件...</source>
        <translation>Contando archivos de etiquetas...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="781"/>
        <source>标签&quot;{}&quot;已有 {} 处标注, 删除后这些标注将被一并删除且不可恢复.
确定删除吗?</source>
        <translation>La etiqueta &quot;{}&quot; tiene {} anotación(es). Si la elimina, todas se borrarán y no se podrá deshacer.
¿Eliminar de todos modos?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="788"/>
        <source>确定删除标签&quot;{}&quot;吗?</source>
        <translation>¿Eliminar la etiqueta &quot;{}&quot;?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="714"/>
        <location filename="../app/annotation/annotation_dialog.py" line="821"/>
        <source>标签名称不能为空</source>
        <translation>El nombre de la etiqueta no puede estar vacío</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="881"/>
        <source>{} 个顶点</source>
        <translation>{} vértices</translation>
    </message>
</context>
<context>
    <name>App</name>
    <message>
        <location filename="../app/main_window.py" line="55"/>
        <source>软件启动</source>
        <translation>Inicio del programa</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="58"/>
        <source>软件退出</source>
        <translation>Cierre del programa</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="60"/>
        <source>软件退出前停止训练</source>
        <translation>Detener el entrenamiento antes de salir</translation>
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
        <translation>Proyectos</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="193"/>
        <source>添加项目</source>
        <translation>Añadir proyecto</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="196"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="335"/>
        <source>项目训练中</source>
        <translation>Entrenando</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="365"/>
        <source>停止训练</source>
        <translation>Detener entrenamiento</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="372"/>
        <source>剩余时间:</source>
        <translation>Tiempo restante:</translation>
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
        <translation>Estadísticas</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="406"/>
        <source>训练</source>
        <translation>Entrenar</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="413"/>
        <source>模型</source>
        <translation>Modelos</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="420"/>
        <location filename="../app/mixins/queue_mixin.py" line="368"/>
        <source>队列</source>
        <translation>Cola</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="427"/>
        <source>日志</source>
        <translation>Registro</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="446"/>
        <source>界面语言</source>
        <translation>Idioma de la interfaz</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="537"/>
        <source>上一页</source>
        <translation>Anterior</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="566"/>
        <source>下一页</source>
        <translation>Siguiente</translation>
    </message>
</context>
<context>
    <name>Charts</name>
    <message>
        <location filename="../app/widgets/charts.py" line="12"/>
        <source>暂无标注</source>
        <translation>Sin anotaciones</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="13"/>
        <source>标签</source>
        <translation>Etiqueta</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="14"/>
        <source>标签数量</source>
        <translation>Número de etiquetas</translation>
    </message>
</context>
<context>
    <name>ClassifyTestRunner</name>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="34"/>
        <source>缺少测试依赖: {}</source>
        <translation>Faltan dependencias de prueba: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="86"/>
        <source>加载分类模型: {}</source>
        <translation>Cargando modelo de clasificación: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="112"/>
        <source>测试图片 {} 张</source>
        <translation>{} imágenes de prueba</translation>
    </message>
</context>
<context>
    <name>ClassifyTrainRunner</name>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="41"/>
        <source>缺少训练依赖: {}</source>
        <translation>Faltan dependencias de entrenamiento: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="133"/>
        <source>输出路径: {}</source>
        <translation>Ruta de salida: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="134"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Directorio de salida de este entrenamiento (marca de tiempo): {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="150"/>
        <source>分类训练: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</source>
        <translation>Entrenamiento de clasificación: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="159"/>
        <source>数据准备: train={} 张, val={} 张</source>
        <translation>Preparación de datos: train={} imágenes, val={} imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="161"/>
        <source>训练集无图像, 请检查数据集</source>
        <translation>El conjunto de entrenamiento no tiene imágenes; revise el conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="163"/>
        <source>验证集无图像, 请检查数据集</source>
        <translation>El conjunto de validación no tiene imágenes; revise el conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="188"/>
        <source>未从数据集中解析到任何类别(子文件夹),无法训练图像分类</source>
        <translation>No se detectó ninguna clase (subcarpeta) en el conjunto de datos; no se puede entrenar clasificación de imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="198"/>
        <source>数据集: train={} val={} 类别({})={}</source>
        <translation>Conjunto de datos: train={} val={} clases({})={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="285"/>
        <source>早停触发: 连续 {} 个 epoch 精度无提升</source>
        <translation>Parada temprana activada: {} épocas seguidas sin mejora de precisión</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="290"/>
        <source>训练完成 best_acc={:.4f}</source>
        <translation>Entrenamiento completado best_acc={:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="298"/>
        <source>生成类别文件: {}</source>
        <translation>Generando archivo de clases: {}</translation>
    </message>
</context>
<context>
    <name>CollapsibleText</name>
    <message>
        <location filename="../app/widgets/collapsible_text.py" line="47"/>
        <source>点击展开 / 收起完整内容</source>
        <translation>Clic para expandir / contraer</translation>
    </message>
</context>
<context>
    <name>ColorPickerDialog</name>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="395"/>
        <source>选择颜色</source>
        <translation>Elegir color</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="407"/>
        <source>十六进制:</source>
        <translation>Hex:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="428"/>
        <source>基本颜色:</source>
        <translation>Colores básicos:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="440"/>
        <source>自定义 RGB:</source>
        <translation>RGB personalizado:</translation>
    </message>
</context>
<context>
    <name>CompareDialog</name>
    <message>
        <location filename="../ui/compare.ui" line="14"/>
        <source>对比多次训练</source>
        <translation>Comparar entrenamientos</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="22"/>
        <source>对比指标</source>
        <translation>Comparar métrica</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="38"/>
        <source>记录范围</source>
        <translation>Rango de registros</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="65"/>
        <location filename="../app/widgets/compare_dialog.py" line="680"/>
        <location filename="../app/widgets/compare_dialog.py" line="684"/>
        <location filename="../app/widgets/compare_dialog.py" line="701"/>
        <source>导出对比报告</source>
        <translation>Exportar informe comparativo</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="72"/>
        <location filename="../app/widgets/compare_dialog.py" line="708"/>
        <location filename="../app/widgets/compare_dialog.py" line="712"/>
        <source>删除选中</source>
        <translation>Eliminar selección</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="97"/>
        <source>训练记录（可勾选，上限 8 条）</source>
        <translation>Registros de entrenamiento (seleccionables, máx. 8)</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="168"/>
        <source>关键指标汇总</source>
        <translation>Resumen de métricas clave</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="188"/>
        <source>差异与结论</source>
        <translation>Diferencias y conclusión</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="305"/>
        <source>勾选要对比的训练记录(最多 {} 条), 双击查看单次指标</source>
        <translation>Marca los entrenamientos a comparar (máx. {}); doble clic para ver las métricas de uno</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="280"/>
        <source>数据来源：LMDB train_history + metrics.csv / metrics json</source>
        <translation>Fuente de datos: LMDB train_history + metrics.csv / metrics json</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="501"/>
        <source>一次最多对比 {} 条记录</source>
        <translation>Se pueden comparar como máximo {} registros a la vez</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="529"/>
        <source>{} 训练曲线（按 epoch）</source>
        <translation>Curva de entrenamiento de {} (por época)</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="536"/>
        <source>已选 {} 条（上限 {}）</source>
        <translation>{} seleccionados (máx. {})</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="538"/>
        <source>已选 {} 条(上限 {}), 双击左侧记录可查看单次指标</source>
        <translation>{} seleccionados (límite {}); doble clic en un registro de la izquierda para ver sus métricas</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="540"/>
        <location filename="../app/widgets/compare_dialog.py" line="566"/>
        <source>勾选左侧的训练记录后这里显示对比曲线</source>
        <translation>Marca registros de la izquierda para mostrar aquí sus curvas comparadas</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="634"/>
        <source>无</source>
        <translation>Ninguno</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="647"/>
        <source>至少勾选 2 条记录&lt;br&gt;才能比较差异</source>
        <translation>Selecciona al menos 2 registros&lt;br&gt;para comparar diferencias</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="681"/>
        <source>当前没有可导出的对比图表</source>
        <translation>No hay gráficos comparativos para exportar</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="685"/>
        <source>PNG 图片 (*.png)</source>
        <translation>Imagen PNG (*.png)</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="699"/>
        <source>已导出: {}
{}</source>
        <translation>Exportado: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="702"/>
        <source>导出失败: {}</source>
        <translation>Error al exportar: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="709"/>
        <source>请先勾选要删除的训练记录</source>
        <translation>Selecciona primero los registros a eliminar</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="713"/>
        <source>确定删除选中的 {} 条训练记录? 对应指标文件会一并删除.</source>
        <translation>¿Eliminar los {} registros de entrenamiento seleccionados? Sus archivos de métricas también se eliminarán.</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="570"/>
        <source>所选记录没有&quot;{}&quot;的数据</source>
        <translation>Los registros seleccionados no tienen datos de &quot;{}&quot;</translation>
    </message>
</context>
<context>
    <name>DataPrep</name>
    <message>
        <location filename="../app/train/data_prep.py" line="189"/>
        <source>解析到类别 {} 个: {}</source>
        <translation>{} clases detectadas: {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="209"/>
        <source>复制数据集 {}: 图像 {} 张, 标签 {} 个 → {}</source>
        <translation>Copiando conjunto de datos {}: {} imágenes, {} etiquetas → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="296"/>
        <source>合并 {} 数据集 → {} ({} 个文件)</source>
        <translation>Fusionando {} conjuntos de datos → {} ({} archivos)</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="313"/>
        <source>生成 data.yaml → {}</source>
        <translation>Generando data.yaml → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="326"/>
        <source>未从数据集中解析到任何标签类别, 请检查标签文件</source>
        <translation>No se han detectado clases de etiqueta en el conjunto de datos; revisa los archivos de etiquetas</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="333"/>
        <source>数据准备完成: {} 个类别, 输出目录 {}</source>
        <translation>Preparación de datos completada: {} clases, directorio de salida {}</translation>
    </message>
</context>
<context>
    <name>DatasetViewMixin</name>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="266"/>
        <source>删除全部未标注图像({} 张)</source>
        <translation>Eliminar todas las imágenes sin etiquetar ({} imágenes)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="272"/>
        <source>删除所选图像({} 张)</source>
        <translation>Eliminar las imágenes seleccionadas ({} imágenes)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="386"/>
        <source>重载跳过: 数据集 {}/{} 无图像目录</source>
        <translation>Recarga omitida: el conjunto de datos {}/{} no tiene directorio de imágenes</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="387"/>
        <source>重载</source>
        <translation>Recargar</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="388"/>
        <source>该数据集还没有图像目录, 请先右键&quot;导入&quot;</source>
        <translation>Este conjunto de datos aún no tiene directorio de imágenes; haga clic derecho en &quot;Importar&quot; primero</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="392"/>
        <source>重载跳过: 数据集 {}/{} 正在载入</source>
        <translation>Recarga omitida: el conjunto de datos {}/{} se está cargando</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="394"/>
        <source>重载数据集: {}/{}</source>
        <translation>Recargando conjunto de datos: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="609"/>
        <source>数据集 {}/{} 含 OCR 文本标注, 已标为字符检测数据集</source>
        <translation>El conjunto {}/{} contiene anotaciones de texto OCR, marcado como conjunto de detección de texto</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="950"/>
        <source>第 {} / {} 页</source>
        <translation>Página {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="954"/>
        <source>第 {}/{} 页 · 共 {} 个</source>
        <translation>Página {}/{} · {} en total</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="956"/>
        <source>第 {}/{} 页 · 共 {} 张</source>
        <translation>Página {}/{} · {} imágenes</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="969"/>
        <source>未选择标签</source>
        <translation>Ninguna etiqueta seleccionada</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="971"/>
        <source>暂无数据</source>
        <translation>Sin datos</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1008"/>
        <source>开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}</source>
        <translation>Iniciando importación: {}/{} | ruta de imágenes={} | ruta de etiquetas={} | formato={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1009"/>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1078"/>
        <source>(无)</source>
        <translation>(ninguno)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1073"/>
        <source>{}: {}个</source>
        <translation>{}: {} unidades</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1075"/>
        <source>数据集导入完成: {}/{} | 图像 {} 张, 已标注 {} 张 | 标签({}类): {}</source>
        <translation>Importación del conjunto de datos completada: {}/{} | {} imágenes, {} etiquetadas | etiquetas ({} clases): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1120"/>
        <source>数据集 {}/{} 未导入, 右键&quot;导入&quot;选择图像与标签目录</source>
        <translation>Conjunto de datos {}/{} sin importar; haga clic derecho en &quot;Importar&quot; y seleccione las carpetas de imágenes y etiquetas</translation>
    </message>
</context>
<context>
    <name>Dialog</name>
    <message>
        <location filename="../ui/dataset_properties.ui" line="14"/>
        <source>数据集属性</source>
        <translation>Propiedades del conjunto de datos</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="30"/>
        <source>选择数据:</source>
        <translation>Seleccionar conjunto de datos:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="53"/>
        <source>确定</source>
        <translation>Aceptar</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="77"/>
        <source>图像路径:</source>
        <translation>Ruta de imágenes:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="98"/>
        <source>标签路径:</source>
        <translation>Ruta de etiquetas:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="119"/>
        <source>标签分布:</source>
        <translation>Distribución de etiquetas:</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="14"/>
        <source>导出</source>
        <translation>Exportar</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="36"/>
        <source>请选择导出路径</source>
        <translation>Seleccione una ruta de exportación</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="90"/>
        <source>导出格式</source>
        <translation>Formato de exportación</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="106"/>
        <source>labelme 格式</source>
        <translation>formato labelme</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="119"/>
        <source>yolo 格式</source>
        <translation>formato yolo</translation>
    </message>
</context>
<context>
    <name>DialogButtons</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="219"/>
        <location filename="../app/mixins/import_export_mixin.py" line="278"/>
        <location filename="../app/mixins/misc_mixin.py" line="123"/>
        <location filename="../app/widgets/dialog_buttons.py" line="110"/>
        <source>确定</source>
        <translation>Aceptar</translation>
    </message>
    <message>
        <location filename="../app/widgets/dialog_buttons.py" line="116"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
</context>
<context>
    <name>DiffPanel</name>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="93"/>
        <source>最佳记录</source>
        <translation>Mejor registro</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="94"/>
        <source>按 {}</source>
        <translation>según {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="112"/>
        <source>参数差异</source>
        <translation>Diferencias de parámetros</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="112"/>
        <source>仅列取值不同的项</source>
        <translation>Solo valores distintos</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="121"/>
        <source>所选记录参数完全一致</source>
        <translation>Los registros seleccionados tienen parámetros idénticos</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="130"/>
        <source>共同</source>
        <translation>Común</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="160"/>
        <source>结论</source>
        <translation>Conclusión</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="175"/>
        <source>最佳</source>
        <translation>Mejor</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="185"/>
        <source>它独有的设置</source>
        <translation>exclusivo de este</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="189"/>
        <source>启用增强 {}/{} 条</source>
        <translation>Aumento activado en {}/{}:</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="192"/>
        <source>所选记录都没有启用数据增强</source>
        <translation>Ninguno de los registros activó aumento de datos</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="197"/>
        <source>仍在训练</source>
        <translation>aún entrenando</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="199"/>
        <source>曲线未收敛， 对比仅供参考</source>
        <translation>curva sin converger， solo referencia</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="204"/>
        <source>未跑完</source>
        <translation>sin terminar</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="204"/>
        <source>不参与最佳判定</source>
        <translation>excluido del mejor</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="207"/>
        <source>训练时长</source>
        <translation>Duración del entrenamiento</translation>
    </message>
</context>
<context>
    <name>ImportData</name>
    <message>
        <location filename="../ui/import_data.ui" line="14"/>
        <source>导入数据</source>
        <translation>Importar datos</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="33"/>
        <source>图像路径</source>
        <translation>Ruta de imágenes</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="73"/>
        <source>标签路径</source>
        <translation>Ruta de etiquetas</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="107"/>
        <source>标签格式:</source>
        <translation>Formato de etiquetas:</translation>
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
        <translation>Importar como clasificación (subcarpetas)</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="155"/>
        <source>提示信息</source>
        <translation>Información</translation>
    </message>
</context>
<context>
    <name>ImportExportMixin</name>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="59"/>
        <source>导入数据 - {} / {}</source>
        <translation>Importar datos - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="66"/>
        <location filename="../app/mixins/import_export_mixin.py" line="166"/>
        <source>请选择图像文件夹</source>
        <translation>Seleccione una carpeta de imágenes</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="142"/>
        <source>请选择分类根目录(子文件夹名=类别)</source>
        <translation>Seleccione la carpeta raíz de clasificación (nombre de subcarpeta = clase)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="155"/>
        <source>(根目录)</source>
        <translation>(carpeta raíz)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="157"/>
        <source>所选文件夹下无分类子文件夹或图像</source>
        <translation>La carpeta seleccionada no contiene subcarpetas de clase ni imágenes</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="159"/>
        <source>{}: {}张</source>
        <translation>{}: {} imágenes</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="161"/>
        <source>检测到 {} 类: {}</source>
        <translation>Detectadas {} clases: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="80"/>
        <source>所选文件夹无图像</source>
        <translation>No hay imágenes en la carpeta seleccionada</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="83"/>
        <source>共 {} 张图像, 已标注 {} 张</source>
        <translation>{} imágenes, {} etiquetadas</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="99"/>
        <source>(检测到 {} 张 {} 标签, 请切换上方格式为&quot;{}&quot;)</source>
        <translation>(Se detectaron {} etiquetas {}; cambie el formato de arriba a &quot;{}&quot;)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="103"/>
        <source>共 {} 张图像, 已标注 0 张 {}</source>
        <translation>{} imágenes, 0 etiquetadas {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="105"/>
        <source>共 {} 张图像(标签目录无匹配文件)</source>
        <translation>{} imágenes (no hay archivos coincidentes en la carpeta de etiquetas)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="172"/>
        <source>选择文件夹</source>
        <translation>Seleccionar carpeta</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="212"/>
        <source>分类根目录(子文件夹名=类别)</source>
        <translation>Raíz de clasificación (nombre de subcarpeta = clase)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="212"/>
        <source>图像路径</source>
        <translation>Ruta de imágenes</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="234"/>
        <location filename="../app/mixins/import_export_mixin.py" line="237"/>
        <source>导入数据</source>
        <translation>Importar datos</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="234"/>
        <source>请先选择有效的图像文件夹</source>
        <translation>Seleccione primero una carpeta de imágenes válida</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="237"/>
        <source>标签路径无效</source>
        <translation>Ruta de etiquetas no válida</translation>
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
        <translation>Exportar</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="298"/>
        <source>请先在左侧选中要导出的数据集</source>
        <translation>Seleccione primero a la izquierda el conjunto de datos que desea exportar</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="311"/>
        <source>打开</source>
        <translation>Abrir</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="322"/>
        <source>请先选择导出保存位置</source>
        <translation>Seleccione primero dónde guardar la exportación</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="333"/>
        <source>开始导出: 项目={} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>Iniciando exportación: proyecto={} | ruta de origen={} | ruta de destino={} | formato={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="339"/>
        <source>正在导出项目...</source>
        <translation>Exportando proyecto...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="350"/>
        <source>项目&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>Proyecto &quot;{}&quot; exportado: {} imágenes copiadas
Ubicación: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="352"/>
        <source>导出项目完成: {} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>Exportación del proyecto completada: {} | {} imágenes | etiquetas({}) | formato={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="358"/>
        <source>开始导出: 数据集={}/{} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>Iniciando exportación: conjunto de datos={}/{} | ruta de origen={} | ruta de destino={} | formato={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="362"/>
        <source>正在导出数据集...</source>
        <translation>Exportando conjunto de datos...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="372"/>
        <source>数据集&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>Conjunto de datos &quot;{}&quot; exportado: {} imágenes copiadas
Ubicación: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="375"/>
        <source>导出数据集完成: {}/{} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>Exportación del conjunto de datos completada: {}/{} | {} imágenes | etiquetas({}) | formato={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="380"/>
        <source>导出失败: 项目={} 数据集={} | {}</source>
        <translation>Error de exportación: proyecto={} conjunto de datos={} | {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="381"/>
        <source>(整个项目)</source>
        <translation>(proyecto completo)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="382"/>
        <source>导出失败</source>
        <translation>Error de exportación</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="385"/>
        <source>选择导出保存位置</source>
        <translation>Seleccionar destino de exportación</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="411"/>
        <source>{} =&gt; 标签:{}</source>
        <translation>{} =&gt; etiquetas:{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="412"/>
        <location filename="../app/mixins/import_export_mixin.py" line="413"/>
        <source>(无)</source>
        <translation>(ninguno)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="420"/>
        <source>(无标签)</source>
        <translation>(sin etiquetas)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="463"/>
        <source>正在导出: {}</source>
        <translation>Exportando: {}</translation>
    </message>
</context>
<context>
    <name>ImportTask</name>
    <message>
        <location filename="../app/tasks/import_task.py" line="109"/>
        <source>导入跳过 {}: {}</source>
        <translation>Importación omitida {}: {}</translation>
    </message>
</context>
<context>
    <name>LabelFilter</name>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="60"/>
        <location filename="../app/widgets/label_filter_popup.py" line="451"/>
        <source>全选</source>
        <translation>Seleccionar todo</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="464"/>
        <source>显示全部图像</source>
        <translation>Sin filtro</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="466"/>
        <source>按所选标签过滤</source>
        <translation>Filtro por etiqueta</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="468"/>
        <source>未选择标签</source>
        <translation>Sin selección</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="533"/>
        <source>收起</source>
        <translation>Contraer</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="534"/>
        <source>展开全部</source>
        <translation>Mostrar todo</translation>
    </message>
</context>
<context>
    <name>LabelMixin</name>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="88"/>
        <source>已选 {} 个</source>
        <translation>{} seleccionadas</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="89"/>
        <source>全选</source>
        <translation>Seleccionar todo</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="91"/>
        <location filename="../app/mixins/label_mixin.py" line="108"/>
        <source>未选择标签</source>
        <translation>Sin selección</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="100"/>
        <location filename="../app/mixins/label_mixin.py" line="175"/>
        <source>未标注</source>
        <translation>Sin etiquetar</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="208"/>
        <source>重命名</source>
        <translation>Renombrar</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="214"/>
        <source>合并标签</source>
        <translation>Fusionar etiquetas</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="215"/>
        <source>标签&quot;{}&quot;已存在.
确定把&quot;{}&quot;的所有标注合并到&quot;{}&quot;吗?
此操作会改写数据集源标签文件, 且不可恢复.</source>
        <translation>La etiqueta &quot;{}&quot; ya existe.
¿Fusionar todas las anotaciones de &quot;{}&quot; en &quot;{}&quot;?
Esta operación reescribe los archivos de etiquetas originales del conjunto de datos y no se puede deshacer.</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="270"/>
        <source>合并标签: {} → {} ({}/{}) | 启动后台文件合并, 完成后输出统计</source>
        <translation>Fusionando etiquetas: {} → {} ({}/{}) | fusión en segundo plano iniciada; las estadísticas se muestran al terminar</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="273"/>
        <source>重命名标签: {} → {} ({}/{})</source>
        <translation>Renombrando etiqueta: {} → {} ({}/{})</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="349"/>
        <source>{}: {}个</source>
        <translation>{}: {} unidades</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="352"/>
        <source>删除标签完成: {} | 修改 {} 个标签文件 | 删除后标签统计({}类): {}</source>
        <translation>Eliminación de etiqueta completada: {} | {} archivos de etiquetas modificados | estadísticas de etiquetas tras eliminar ({} clases): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="355"/>
        <location filename="../app/mixins/label_mixin.py" line="360"/>
        <location filename="../app/mixins/label_mixin.py" line="365"/>
        <source>(无)</source>
        <translation>(ninguno)</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="357"/>
        <source>合并标签: {} → {} | 修改 {} 个标签文件 | 合并后标签统计({}类): {}</source>
        <translation>Fusionando etiquetas: {} → {} | {} archivos de etiquetas modificados | estadísticas de etiquetas tras la fusión ({} clases): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="362"/>
        <source>合并标签: {} → {} | 无标签文件被修改 | 合并后标签统计({}类): {}</source>
        <translation>Fusionando etiquetas: {} → {} | ningún archivo de etiquetas modificado | estadísticas de etiquetas tras la fusión ({} clases): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="456"/>
        <source>删除标签: {} ({}/{})</source>
        <translation>Eliminar etiqueta: {} ({}/{})</translation>
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
        <translation>Vaciar</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="79"/>
        <location filename="../app/widgets/log_dialog.py" line="21"/>
        <source>日志</source>
        <translation>Registro</translation>
    </message>
</context>
<context>
    <name>MessageBox</name>
    <message>
        <location filename="../app/widgets/message_box.py" line="274"/>
        <location filename="../app/widgets/message_box.py" line="302"/>
        <source>确定</source>
        <translation>Aceptar</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="98"/>
        <source>详情已复制到剪贴板</source>
        <translation>Detalles copiados al portapapeles</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="267"/>
        <source>关闭</source>
        <translation>Cerrar</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="269"/>
        <source>复制详情</source>
        <translation>Copiar detalles</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="303"/>
        <location filename="../app/widgets/message_box.py" line="350"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="374"/>
        <source>取消中...</source>
        <translation>Cancelando...</translation>
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
        <translation>Exactitud</translation>
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
        <translation>Ninguno de los registros seleccionados tiene datos de {}</translation>
    </message>
</context>
<context>
    <name>MetricsDialog</name>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="50"/>
        <source>训练指标</source>
        <translation>Métricas de entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="79"/>
        <source>标签筛选</source>
        <translation>Filtro de etiquetas</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="83"/>
        <source>全部指标</source>
        <translation>Todas las métricas</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="84"/>
        <source>全部标签-P</source>
        <translation>Todas las etiquetas - P</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="85"/>
        <source>全部标签-R</source>
        <translation>Todas las etiquetas - R</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="121"/>
        <source>暂无该标签的指标数据(训练完成后可查看)</source>
        <translation>Aún no hay datos de métricas para esta etiqueta (disponibles al terminar el entrenamiento)</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="169"/>
        <source>loss 值</source>
        <translation>Valor de loss</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="170"/>
        <source>指标值 (mAP/P/R)</source>
        <translation>Métrica (mAP/P/R)</translation>
    </message>
</context>
<context>
    <name>MiscMixin</name>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="54"/>
        <source>界面语言: {}</source>
        <translation>Idioma de la interfaz: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="115"/>
        <source>数据集统计</source>
        <translation>Estadísticas del conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="124"/>
        <source>应用所选数据集</source>
        <translation>Aplicar los conjuntos de datos seleccionados</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="215"/>
        <source>[{}/{}](未设置)</source>
        <translation>[{}/{}](sin configurar)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="218"/>
        <source>(未选择数据集)</source>
        <translation>(ningún conjunto de datos seleccionado)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="338"/>
        <source>删除图像: {} 张 | 本地删除文件={} | 项目={}, 数据集={}</source>
        <translation>Eliminar imágenes: {} | archivo local eliminado={} | proyecto={}, conjunto de datos={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="376"/>
        <source>删除</source>
        <translation>Eliminar</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="377"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="379"/>
        <source>删除图像</source>
        <translation>Eliminar imágenes</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="380"/>
        <source>将从系统删除所选 {} 张图像?

(图像与同名标注文件不可恢复)</source>
        <translation>¿Eliminar del sistema las {} imágenes seleccionadas?

(Las imágenes y sus archivos de etiquetas no se podrán recuperar)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="384"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>Las imágenes y sus archivos de etiquetas se eliminarán del disco. Esta acción no se puede deshacer</translation>
    </message>
</context>
<context>
    <name>ModelAssets</name>
    <message>
        <location filename="../app/core/model_assets.py" line="87"/>
        <location filename="../app/core/model_assets.py" line="121"/>
        <source>速度最快, 精度够用</source>
        <translation>El más rápido, precisión suficiente</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="88"/>
        <location filename="../app/core/model_assets.py" line="125"/>
        <source>精度更好, 稍慢一些</source>
        <translation>Mejor precisión, algo más lento</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="89"/>
        <location filename="../app/core/model_assets.py" line="129"/>
        <source>精度更高</source>
        <translation>Precisión más alta</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="90"/>
        <source>精度最高, 显存占用大</source>
        <translation>La precisión más alta, pero usa más VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="91"/>
        <source>精度极致, 显存占用很大</source>
        <translation>La precisión más extrema, pero usa mucho más VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="94"/>
        <location filename="../app/core/model_assets.py" line="140"/>
        <source>轻量分割</source>
        <translation>Segmentación ligera</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="95"/>
        <location filename="../app/core/model_assets.py" line="144"/>
        <source>速度与精度平衡</source>
        <translation>Equilibrio entre velocidad y precisión</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="96"/>
        <location filename="../app/core/model_assets.py" line="148"/>
        <source>细节更完整</source>
        <translation>Detalles más completos</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="97"/>
        <location filename="../app/core/model_assets.py" line="152"/>
        <source>最精细</source>
        <translation>El más detallado</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="98"/>
        <source>最精细, 显存占用很大</source>
        <translation>El más detallado, pero usa mucho más VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="136"/>
        <source>结构与 medium 相同</source>
        <translation>Misma arquitectura que medium</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="294"/>
        <source>文件不存在: {}</source>
        <translation>El archivo no existe: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="297"/>
        <source>只支持 {} 格式</source>
        <translation>Solo se admite el formato {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="302"/>
        <source>读不到文件大小: {}</source>
        <translation>No se puede leer el tamaño del archivo: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="304"/>
        <source>文件只有 {}, 不像完整的权重</source>
        <translation>El archivo solo ocupa {}, no parece un peso completo</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="315"/>
        <source>这看着是 Transformer 权重, 当前档位是 CNN(YOLO)</source>
        <translation>Parece un peso de Transformer, pero la opción actual es CNN (YOLO)</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="319"/>
        <source>这看着是 CNN(YOLO) 权重, 当前档位是 Transformer</source>
        <translation>Parece un peso de CNN (YOLO), pero la opción actual es Transformer</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="339"/>
        <source>权重目录不可写: {}</source>
        <translation>No se puede escribir en el directorio de pesos: {}</translation>
    </message>
</context>
<context>
    <name>ModelDialog</name>
    <message>
        <location filename="../ui/model.ui" line="14"/>
        <location filename="../app/widgets/model_dialog.py" line="169"/>
        <source>模型管理</source>
        <translation>Gestión de modelos</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="28"/>
        <source>搜索项目 / 数据集 / 标签</source>
        <translation>Buscar proyecto / conjunto de datos / etiqueta</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="39"/>
        <source>全部任务</source>
        <translation>Todas las tareas</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="44"/>
        <source>检测</source>
        <translation>Detección</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="49"/>
        <source>分割</source>
        <translation>Segmentación</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="54"/>
        <source>分类</source>
        <translation>Clasificación</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="66"/>
        <source>全部状态</source>
        <translation>Todos los estados</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="71"/>
        <source>已完成</source>
        <translation>Finalizado</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="76"/>
        <source>训练中</source>
        <translation>En entrenamiento</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="81"/>
        <source>失败</source>
        <translation>Fallido</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="86"/>
        <source>已停止</source>
        <translation>Detenido</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="94"/>
        <source>仅看每个数据集最佳</source>
        <translation>Solo el mejor de cada conjunto de datos</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="114"/>
        <source>共 0 条</source>
        <translation>0 registros</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="135"/>
        <location filename="../app/widgets/model_dialog.py" line="606"/>
        <source>任务</source>
        <translation>Tarea</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="140"/>
        <source>数据集 / 标签</source>
        <translation>Conjunto de datos / Etiquetas</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="145"/>
        <location filename="../app/widgets/model_dialog.py" line="610"/>
        <source>精度</source>
        <translation>Precisión</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="150"/>
        <location filename="../app/widgets/model_dialog.py" line="621"/>
        <source>训练时间</source>
        <translation>Fecha de entrenamiento</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="155"/>
        <location filename="../app/widgets/model_dialog.py" line="623"/>
        <source>耗时</source>
        <translation>Duración</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="160"/>
        <location filename="../app/widgets/model_dialog.py" line="613"/>
        <source>图像尺寸</source>
        <translation>Tamaño de imagen</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="165"/>
        <source>操作</source>
        <translation>Acciones</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="184"/>
        <source>模型详情</source>
        <translation>Detalles del modelo</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="191"/>
        <location filename="../app/widgets/model_dialog.py" line="589"/>
        <source>选中一行查看详情</source>
        <translation>Seleccione una fila para ver los detalles</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="220"/>
        <source>查看完整指标</source>
        <translation>Ver métricas completas</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="227"/>
        <location filename="../app/widgets/model_dialog.py" line="733"/>
        <source>对比多次训练</source>
        <translation>Comparar entrenamientos</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="234"/>
        <source>按此配置重训</source>
        <translation>Reentrenar con esta configuración</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="241"/>
        <source>打开模型目录</source>
        <translation>Abrir directorio del modelo</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="281"/>
        <source>上一页</source>
        <translation>Anterior</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="288"/>
        <source>1/1</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="295"/>
        <source>下一页</source>
        <translation>Siguiente</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="415"/>
        <source>共 {} 条</source>
        <translation>{} registros</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="466"/>
        <source> 等 {} 类</source>
        <translation> y {} clases más</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="481"/>
        <source>测试</source>
        <translation>Probar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="486"/>
        <source>导出</source>
        <translation>Exportar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="491"/>
        <source>删除</source>
        <translation>Eliminar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="603"/>
        <source>{} × {} 累积</source>
        <translation>{} × {} acumulado</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="604"/>
        <source>状态</source>
        <translation>Estado</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="611"/>
        <source>训练集</source>
        <translation>Conjunto de entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="612"/>
        <source>验证集</source>
        <translation>Conjunto de validación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="614"/>
        <source>轮数 / 早停</source>
        <translation>Épocas / Parada temprana</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="616"/>
        <source>批大小</source>
        <translation>Tamaño de lote</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="617"/>
        <source>学习率</source>
        <translation>Tasa de aprendizaje</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="618"/>
        <source>优化器</source>
        <translation>Optimizador</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="619"/>
        <source>设备</source>
        <translation>Dispositivo</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="620"/>
        <source>标签</source>
        <translation>Etiquetas</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="624"/>
        <source>模型路径</source>
        <translation>Ruta del modelo</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="640"/>
        <source>失败原因</source>
        <translation>Motivo del fallo</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="656"/>
        <source>暂无曲线</source>
        <translation>Sin curva</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="680"/>
        <source>{}  最佳 {:.3f}</source>
        <translation>{}  mejor {:.3f}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="688"/>
        <location filename="../app/widgets/model_dialog.py" line="699"/>
        <source>打开目录</source>
        <translation>Abrir directorio</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="689"/>
        <source>模型目录不存在:
{}</source>
        <translation>El directorio del modelo no existe:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="717"/>
        <source>[model_dialog] 打开指标失败: {}
{}</source>
        <translation>[model_dialog] Error al abrir las métricas: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="719"/>
        <source>查看指标失败</source>
        <translation>Error al abrir las métricas</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="734"/>
        <source>当前没有可对比的训练记录</source>
        <translation>No hay entrenamientos que comparar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="741"/>
        <source>[model_dialog] 打开对比失败: {}
{}</source>
        <translation>[model_dialog] No se pudo abrir la comparación: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="743"/>
        <source>打开对比失败</source>
        <translation>No se pudo abrir la comparación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="750"/>
        <source>删除模型记录</source>
        <translation>Eliminar registro del modelo</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="751"/>
        <source>确定删除该条模型记录?
项目={}
数据集={}
开始时间={}
</source>
        <translation>¿Eliminar este registro de modelo?
Proyecto={}
Conjunto de datos={}
Hora de inicio={}
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="755"/>
        <source>删除模型记录: 项目={} 数据集={} 任务={} 开始时间={}</source>
        <translation>Eliminar registro de modelo: proyecto={} conjunto de datos={} tarea={} hora de inicio={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="769"/>
        <source>删除模型记录失败: {} | {}</source>
        <translation>Error al eliminar el registro del modelo: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="770"/>
        <source>[model_dialog] 删除失败: {}
{}</source>
        <translation>[model_dialog] Error al eliminar: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="779"/>
        <source>[model_dialog] 打开训练失败: {}
{}</source>
        <translation>[model_dialog] Error al abrir el entrenamiento: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="780"/>
        <source>打开训练失败</source>
        <translation>Error al abrir el entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="805"/>
        <source>[model_dialog] 打开测试失败: {}
{}</source>
        <translation>[model_dialog] Error al abrir la prueba: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="807"/>
        <source>打开测试失败</source>
        <translation>Error al abrir la prueba</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="825"/>
        <location filename="../app/widgets/model_dialog.py" line="843"/>
        <location filename="../app/widgets/model_dialog.py" line="859"/>
        <location filename="../app/widgets/model_dialog.py" line="1151"/>
        <location filename="../app/widgets/model_dialog.py" line="1161"/>
        <source>导出模型</source>
        <translation>Exportar modelo</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="826"/>
        <source>模型文件不存在:
{}</source>
        <translation>El archivo del modelo no existe:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="827"/>
        <source>导出模型失败: 模型文件不存在 {}</source>
        <translation>Error al exportar el modelo: el archivo del modelo no existe {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="829"/>
        <source>选择导出目录</source>
        <translation>Seleccionar directorio de exportación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="844"/>
        <source>创建目录失败: {}</source>
        <translation>Error al crear el directorio: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="845"/>
        <source>导出模型失败: 创建目录失败 {} | {}</source>
        <translation>Error al exportar el modelo: no se pudo crear el directorio {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="855"/>
        <source>开始导出模型: 项目={} 任务={} 架构={} 尺寸={} | {}</source>
        <translation>Iniciando exportación del modelo: proyecto={} tarea={} arquitectura={} tamaño={} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="856"/>
        <location filename="../app/widgets/model_dialog.py" line="1010"/>
        <source>未知</source>
        <translation>desconocido</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="860"/>
        <source>正在导出 ONNX...</source>
        <translation>Exportando ONNX...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="881"/>
        <source>正在导出模型包...</source>
        <translation>Exportando paquete de modelo...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="892"/>
        <source>导出模型包完成: 包含 {}</source>
        <translation>Paquete de modelo exportado, contiene: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="899"/>
        <source>ONNX 导出完成: {} ({:.1f} MB)</source>
        <translation>Exportación ONNX completada: {} ({:.1f} MB)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="956"/>
        <source>读取词表失败: {}</source>
        <translation>Error al leer el vocabulario: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="967"/>
        <source>生成 vocab.txt 失败: {}</source>
        <translation>Error al generar vocab.txt: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="983"/>
        <source>生成 label_map.json 失败: {}</source>
        <translation>Error al generar label_map.json: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="989"/>
        <source>导出模型报告跳过: 分类任务不出评估报告</source>
        <translation>Exportación del informe del modelo omitida: las tareas de clasificación no generan informe de evaluación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="990"/>
        <source>分类任务不生成评估报告</source>
        <translation>Las tareas de clasificación no generan informe de evaluación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="994"/>
        <source>导出模型报告跳过: 字符识别不出评估报告</source>
        <translation>Informe del modelo omitido: el reconocimiento de texto no genera informe de evaluación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="995"/>
        <source>字符识别不生成评估报告</source>
        <translation>El reconocimiento de texto no genera informe de evaluación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="999"/>
        <source>导出模型报告跳过: 未找到验证集</source>
        <translation>Exportación del informe del modelo omitida: no se encontró conjunto de validación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1000"/>
        <source>未找到验证集, 已跳过评估报告</source>
        <translation>No se encontró conjunto de validación; informe de evaluación omitido</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1002"/>
        <location filename="../app/widgets/model_dialog.py" line="1084"/>
        <source>正在生成模型报告...</source>
        <translation>Generando informe del modelo...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1006"/>
        <source>正在生成模型报告 {}/{}</source>
        <translation>Generando informe del modelo {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1009"/>
        <source>导出模型评估失败: {}</source>
        <translation>Error al exportar la evaluación del modelo: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1012"/>
        <source>评估失败, 已跳过报告: {}</source>
        <translation>Evaluación fallida; informe omitido: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1103"/>
        <source>导出模型报告跳过: 验证集没有标注</source>
        <translation>Exportación del informe del modelo omitida: el conjunto de validación no tiene anotaciones</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1104"/>
        <source>验证集没有标注, 已跳过评估报告</source>
        <translation>El conjunto de validación no tiene anotaciones; se omitió el informe de evaluación</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1110"/>
        <source>[export] 生成评估报告失败:
{}</source>
        <translation>[export] Error al generar el informe de evaluación:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1107"/>
        <source>生成评估报告失败: {}</source>
        <translation>Error al generar el informe de evaluación: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="941"/>
        <source>读取类别表失败: {}</source>
        <translation>Error al leer la lista de clases: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="942"/>
        <source>[export] 读取类别表失败: {}</source>
        <translation>[export] Error al leer la lista de clases: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1099"/>
        <source>导出模型报告完成: {}</source>
        <translation>Exportación del informe del modelo completada: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1111"/>
        <source>评估完成, 但报告生成失败</source>
        <translation>La evaluación terminó, pero no se pudo generar el informe</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1145"/>
        <source>导出模型完成: {} | 包含: {}</source>
        <translation>Exportación del modelo completada: {} | contiene: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1147"/>
        <source>已导出到:
{}

包含: {}</source>
        <translation>Exportado a:
{}

Contiene: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1109"/>
        <location filename="../app/widgets/model_dialog.py" line="1158"/>
        <source>未知错误</source>
        <translation>Error desconocido</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1162"/>
        <source>模型导出失败, 详情见日志</source>
        <translation>Error al exportar el modelo, consulte el registro para más detalles</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1157"/>
        <source>导出模型失败: {}</source>
        <translation>Error al exportar el modelo: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1159"/>
        <source>[export] ONNX 导出失败: {}</source>
        <translation>[export] Error de exportación ONNX: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1176"/>
        <source>复制导出示例失败: {}</source>
        <translation>Error al copiar el ejemplo de exportación: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1177"/>
        <source>[export] 复制示例失败: {}</source>
        <translation>[export] Error al copiar el ejemplo: {}</translation>
    </message>
</context>
<context>
    <name>ModelDownloader</name>
    <message>
        <location filename="../app/core/model_download.py" line="92"/>
        <source>权重目录不可写入, 请点&quot;更改&quot;换一个目录</source>
        <translation>No se puede escribir en el directorio de pesos; haga clic en &quot;Cambiar&quot; para elegir otro directorio</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="101"/>
        <source>权重文件大小不符, 丢弃重下: {}</source>
        <translation>El tamaño del archivo de pesos no coincide; se descarta y se vuelve a descargar: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="111"/>
        <source>开始下载权重 {} ({}, 已下载 {})</source>
        <translation>Iniciando descarga de pesos {} ({}, ya descargado {})</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="118"/>
        <source>下载权重失败 {}: {}</source>
        <translation>Error al descargar los pesos {}: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="121"/>
        <source>无法连接下载服务器, 请检查网络后重试</source>
        <translation>No se puede conectar con el servidor de descargas; revise la red e inténtelo de nuevo</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="129"/>
        <source>下载中断, 已保留进度, 可再次点击续传</source>
        <translation>Descarga interrumpida; se conservó el progreso, haga clic de nuevo para continuar</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="134"/>
        <source>下载不完整, 已保留进度, 可再次点击续传</source>
        <translation>Descarga incompleta; se conservó el progreso, haga clic de nuevo para continuar</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="141"/>
        <source>权重校验不通过 {}: 期望 {} 实际 {}</source>
        <translation>Verificación de pesos fallida {}: esperado {} real {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="146"/>
        <source>文件校验未通过, 损坏文件已删除, 请重试</source>
        <translation>Verificación del archivo fallida; el archivo dañado se eliminó, inténtelo de nuevo</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="152"/>
        <source>写入权重目录失败, 请检查磁盘空间</source>
        <translation>Error al escribir en el directorio de pesos; compruebe el espacio en disco</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="155"/>
        <source>权重就绪: {}</source>
        <translation>Pesos listos: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="176"/>
        <source>下载已取消, 已下载部分保留以便续传: {}</source>
        <translation>Descarga cancelada; la parte descargada se conserva para continuar: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="196"/>
        <source>权重下载异常 {}: {!r}</source>
        <translation>Error en la descarga de pesos {}: {!r}</translation>
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
        <translation>Pesos del modelo</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="63"/>
        <source>目标检测 · Transformer</source>
        <translation>Detección de objetos · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="97"/>
        <source>目标检测 · CNN</source>
        <translation>Detección de objetos · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="131"/>
        <source>图像分割 · Transformer</source>
        <translation>Segmentación de imágenes · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="165"/>
        <source>图像分割 · CNN</source>
        <translation>Segmentación de imágenes · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="221"/>
        <source>下载目录</source>
        <translation>Carpeta de descargas</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="238"/>
        <source>更改</source>
        <translation>Cambiar</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="265"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="293"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="498"/>
        <source>开始下载</source>
        <translation>Iniciar descarga</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="275"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="280"/>
        <source>关闭</source>
        <translation>Cerrar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="58"/>
        <source>还剩 {}s</source>
        <translation>Quedan {}s</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="59"/>
        <source>还剩 {}m{}s</source>
        <translation>Quedan {}m{}s</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="387"/>
        <source>选择权重目录</source>
        <translation>Seleccionar directorio de pesos</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="405"/>
        <source>选择预训练权重</source>
        <translation>Seleccionar pesos preentrenados</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="406"/>
        <source>权重文件 (*.pt *.pth *.ckpt)</source>
        <translation>Archivos de pesos (*.pt *.pth *.ckpt)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="416"/>
        <source>仍要用这个文件吗?</source>
        <translation>¿Usar este archivo de todos modos?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="444"/>
        <source>权重目录不可写入 {}: {!r}</source>
        <translation>No se puede escribir en el directorio de pesos {}: {!r}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="455"/>
        <source>勾选的模型都已就绪, 不需要下载.</source>
        <translation>Todos los modelos marcados están listos; no hay nada que descargar.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="460"/>
        <source>当前目录不可写入, 请点&quot;更改&quot;换一个目录:
{}</source>
        <translation>El directorio actual no permite escritura; haga clic en &quot;Cambiar&quot; para elegir otro:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="293"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="465"/>
        <source>下载中...</source>
        <translation>Descargando...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="511"/>
        <source>以下权重没能下载完成:
</source>
        <translation>Estos pesos no se pudieron descargar:
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="518"/>
        <source>下载还在进行, 现在关闭会中断下载(已下载部分保留, 下次可续传).
确定关闭?</source>
        <translation>Hay una descarga en curso. Si cierra ahora, se interrumpirá (la parte descargada se conserva y se reanudará la próxima vez).
¿Cerrar de todos modos?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="550"/>
        <source>去下载</source>
        <translation>Descargar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="559"/>
        <source>该架构的权重必须先下载好才能开始训练, 也可以在权重管理里指定本地的权重文件.</source>
        <translation>Los pesos de esta arquitectura deben descargarse antes de iniciar el entrenamiento. También puede indicar un archivo de pesos local en Pesos del modelo.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="553"/>
        <source>本次训练选用 {} {}模型, 需要先下载 {}.</source>
        <translation>Este entrenamiento usa el modelo {} {} y requiere descargar {} primero.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="552"/>
        <source>缺少模型权重</source>
        <translation>Faltan pesos del modelo</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="365"/>
        <source>待下载 {}</source>
        <translation>Pendiente: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="367"/>
        <source>无需下载</source>
        <translation>No hay nada que descargar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="369"/>
        <source>本地 {} 项</source>
        <translation>Locales: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="551"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
</context>
<context>
    <name>MultiCombo</name>
    <message>
        <location filename="../app/widgets/multi_combo.py" line="350"/>
        <source>请选择数据集</source>
        <translation>Seleccione conjuntos de datos</translation>
    </message>
</context>
<context>
    <name>NameInputDialog</name>
    <message>
        <location filename="../ui/input_name.ui" line="14"/>
        <location filename="../ui/input_name.ui" line="40"/>
        <location filename="../app/widgets/name_input_dialog.py" line="13"/>
        <source>输入名称</source>
        <translation>Introducir nombre</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="65"/>
        <location filename="../app/widgets/name_input_dialog.py" line="14"/>
        <source>请输入名称</source>
        <translation>Introduzca un nombre</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="100"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="113"/>
        <source>确定</source>
        <translation>Aceptar</translation>
    </message>
</context>
<context>
    <name>NameRules</name>
    <message>
        <location filename="../app/core/name_rules.py" line="25"/>
        <source>名称不能为空</source>
        <translation>El nombre no puede estar vacío</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="27"/>
        <source>名称过长, 最多 {} 个字符</source>
        <translation>El nombre es demasiado largo, como máximo {} caracteres</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="41"/>
        <source>名称不能包含「{}」等字符</source>
        <translation>El nombre no puede contener caracteres como {}</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="54"/>
        <source>「{}」是系统保留名称, 请换一个</source>
        <translation>&quot;{}&quot; es un nombre reservado, elija otro</translation>
    </message>
</context>
<context>
    <name>OcrTestRunner</name>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="46"/>
        <source>缺少测试依赖: {}</source>
        <translation>Faltan dependencias de prueba: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="187"/>
        <source>识别失败: {}</source>
        <translation>Error de reconocimiento: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="274"/>
        <source>明细写入失败: {}</source>
        <translation>Error al escribir los detalles: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="282"/>
        <source>未知的字符检测架构: {}</source>
        <translation>Arquitectura de detección de texto desconocida: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="296"/>
        <source>已加载配对识别模型: {}</source>
        <translation>Modelo de reconocimiento emparejado cargado: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="300"/>
        <source>识别模型不可用, 输出的标注只有框没有文字</source>
        <translation>Modelo de reconocimiento no disponible; las anotaciones escritas tienen cuadros pero no texto</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="306"/>
        <location filename="../app/train/ocr_test_runner.py" line="425"/>
        <source>没有可用的图像, 请检查数据集</source>
        <translation>No hay imágenes utilizables; compruebe el conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="307"/>
        <source>加载字符检测模型: {}</source>
        <translation>Cargando modelo de detección de texto: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="309"/>
        <location filename="../app/train/ocr_test_runner.py" line="429"/>
        <source>测试图片 {} 张</source>
        <translation>{} imágenes de prueba</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="342"/>
        <source>预测失败 {}: {}</source>
        <translation>Error de predicción {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="372"/>
        <source>输出标注失败 {}: {}</source>
        <translation>Error al escribir las anotaciones {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="400"/>
        <source>已写出 {} 张图的文本标注(图像同目录)</source>
        <translation>Se escribieron anotaciones de texto de {} imágenes (en el mismo directorio que cada imagen)</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="411"/>
        <source>未知的字符识别架构: {}</source>
        <translation>Arquitectura de reconocimiento de texto desconocida: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="415"/>
        <source>该模型没有词表, 无法识别</source>
        <translation>Este modelo no tiene vocabulario; no se puede reconocer</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="426"/>
        <source>加载字符识别模型: {} 词表 {} 个字符</source>
        <translation>Cargando modelo de reconocimiento de texto: {} vocabulario {} caracteres</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="457"/>
        <source>识别失败 {}: {}</source>
        <translation>Reconocimiento fallido {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="464"/>
        <source>没有取到任何字条: 该数据集没有文本标注, 识别段只能拿标注框裁图来测</source>
        <translation>No se obtuvieron recortes de texto: este conjunto de datos no tiene anotaciones de texto y la etapa de reconocimiento solo puede probarse recortando con los cuadros anotados</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="470"/>
        <source>WARN {} 张图没有文本标注, 已跳过</source>
        <translation>WARN {} imágenes no tienen anotaciones de texto, se omitieron</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="473"/>
        <source>字条 {} 条, CER={:.4f}, 全对 {} 条</source>
        <translation>{} recortes de texto, CER={:.4f}, {} completamente correctos</translation>
    </message>
</context>
<context>
    <name>OcrTrainRunner</name>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="42"/>
        <source>缺少训练依赖: {}</source>
        <translation>Faltan dependencias de entrenamiento: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="118"/>
        <source>检测模型 {} 权重来源: {}</source>
        <translation>Modelo de detección {}, pesos procedentes de: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="122"/>
        <source>检测模型 {} 构建失败</source>
        <translation>Error al construir el modelo de detección {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="138"/>
        <source>识别模型 {} 权重来源: {}</source>
        <translation>Modelo de reconocimiento {}, pesos procedentes de: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="142"/>
        <source>识别模型 {} 构建失败</source>
        <translation>Error al construir el modelo de reconocimiento {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="174"/>
        <source>标注里没有任何文字, 无法训练字符识别</source>
        <translation>No hay texto en las anotaciones; no se puede entrenar el reconocimiento de texto</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="182"/>
        <source>词表 {} 个字符</source>
        <translation>Vocabulario: {} caracteres</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="195"/>
        <source>字符{}训练: model={} device={} epochs={} batch={} lr={}</source>
        <translation>Entrenamiento de texto {}: model={} device={} epochs={} batch={} lr={}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="198"/>
        <source>识别</source>
        <translation>reconocimiento</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="199"/>
        <source>检测</source>
        <translation>Detección</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="202"/>
        <source>训练集没有可用的文本标注</source>
        <translation>No hay anotaciones de texto utilizables en el conjunto de entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="205"/>
        <source>验证集没有可用的文本标注</source>
        <translation>No hay anotaciones de texto utilizables en el conjunto de validación</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="207"/>
        <source>数据集: train={} val={}</source>
        <translation>Conjunto de datos: train={} val={}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="293"/>
        <source>早停触发: 连续 {} 个 epoch 无提升</source>
        <translation>Parada anticipada activada: sin mejora durante {} epoch consecutivos</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="322"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Directorio de salida de esta ejecución (marca de tiempo): {}</translation>
    </message>
</context>
<context>
    <name>OnnxExport</name>
    <message>
        <location filename="../app/train/onnx_export.py" line="112"/>
        <source>该识别模型没有词表, 无法导出</source>
        <translation>Este modelo de reconocimiento no tiene vocabulario; no se puede exportar</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="121"/>
        <source>未知的字符模型架构: {}</source>
        <translation>Arquitectura de modelo de texto desconocida: {}</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="133"/>
        <source>识别</source>
        <translation>reconocimiento</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="134"/>
        <source>检测</source>
        <translation>Detección</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="152"/>
        <source>异常检测不导出 ONNX, 请用模型管理的「导出」生成模型包</source>
        <translation>La detección de anomalías no exporta ONNX. Use «Exportar» en la gestión de modelos para crear el paquete</translation>
    </message>
</context>
<context>
    <name>ProjectMixin</name>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="32"/>
        <source>输入名称</source>
        <translation>Introducir nombre</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="33"/>
        <source>项目名称</source>
        <translation>Nombre del proyecto</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="37"/>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <source>创建项目</source>
        <translation>Crear proyecto</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <location filename="../app/mixins/project_mixin.py" line="53"/>
        <source>项目名称已存在!</source>
        <translation>¡Ya existe un proyecto con este nombre!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="44"/>
        <source>创建项目: {}</source>
        <translation>Creando proyecto: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="49"/>
        <location filename="../app/mixins/project_mixin.py" line="53"/>
        <location filename="../app/mixins/project_mixin.py" line="106"/>
        <source>修改名称</source>
        <translation>Renombrar</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="56"/>
        <source>重命名项目: {} → {}</source>
        <translation>Renombrando proyecto: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="61"/>
        <location filename="../app/mixins/project_mixin.py" line="107"/>
        <source>删除项目</source>
        <translation>Eliminar proyecto</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="62"/>
        <source>确定删除项目&quot;{}&quot;吗?
</source>
        <translation>¿Eliminar el proyecto &quot;{}&quot;?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="63"/>
        <source>删除项目: {}</source>
        <translation>Eliminando proyecto: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="103"/>
        <location filename="../app/mixins/project_mixin.py" line="147"/>
        <location filename="../app/mixins/project_mixin.py" line="156"/>
        <source>添加数据集</source>
        <translation>Añadir conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="105"/>
        <source>导出项目</source>
        <translation>Exportar proyecto</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="122"/>
        <source>导入</source>
        <translation>Importar</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="123"/>
        <source>导出</source>
        <translation>Exportar</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="124"/>
        <source>重载</source>
        <translation>Recargar</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="125"/>
        <source>移动</source>
        <translation>Mover</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="126"/>
        <source>修改</source>
        <translation>Renombrar</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="127"/>
        <source>删除</source>
        <translation>Eliminar</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="148"/>
        <source>数据集名称</source>
        <translation>Nombre del conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="156"/>
        <location filename="../app/mixins/project_mixin.py" line="167"/>
        <source>该项目下已存在同名数据集!</source>
        <translation>¡Ya existe un conjunto de datos con este nombre en este proyecto!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="158"/>
        <source>创建数据集: {}/{}</source>
        <translation>Creando conjunto de datos: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="163"/>
        <location filename="../app/mixins/project_mixin.py" line="167"/>
        <source>修改数据集</source>
        <translation>Renombrar conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="169"/>
        <source>重命名数据集: {} → {}</source>
        <translation>Renombrando conjunto de datos: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="174"/>
        <source>删除数据集</source>
        <translation>Eliminar conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="175"/>
        <source>确定删除数据集&quot;{}&quot;吗?
</source>
        <translation>¿Eliminar el conjunto de datos &quot;{}&quot;?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="179"/>
        <source>删除数据集: {}/{}</source>
        <translation>Eliminando conjunto de datos: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="198"/>
        <location filename="../app/mixins/project_mixin.py" line="211"/>
        <location filename="../app/mixins/project_mixin.py" line="228"/>
        <source>移动数据集</source>
        <translation>Mover conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="199"/>
        <source>是否将&quot;{}&quot;的数据从
{} / {} 移动到 {} / {}?
移动后源数据集将清空.</source>
        <translation>¿Mover los datos de &quot;{}&quot; de
{} / {} a {} / {}?
El conjunto de datos de origen quedará vacío.</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="208"/>
        <source>移动失败</source>
        <translation>Error al mover</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="212"/>
        <source>已从 {} / {} 移动到 {} / {}</source>
        <translation>Se movió de {} / {} a {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="229"/>
        <source>没有可移动到的目标数据集(本项目之外无数据集)</source>
        <translation>No hay conjunto de datos de destino disponible (no hay conjuntos de datos fuera de este proyecto)</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="233"/>
        <source>选择目标数据集</source>
        <translation>Seleccionar conjunto de datos de destino</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="237"/>
        <source>选择要将数据移动到的目标数据集:</source>
        <translation>Seleccione el conjunto de datos de destino al que mover los datos:</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="318"/>
        <source>{}: {}个</source>
        <translation>{}: {} unidades</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="320"/>
        <source>数据集移动: {}/{} → {}/{} | 移动图像 {} 张 | 目标标签统计({}类): {}</source>
        <translation>Movimiento del conjunto de datos: {}/{} → {}/{} | {} imágenes movidas | estadísticas de etiquetas del destino ({} clases): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="323"/>
        <source>(无)</source>
        <translation>(ninguno)</translation>
    </message>
</context>
<context>
    <name>ProjectSidebar</name>
    <message>
        <location filename="../app/widgets/project_sidebar.py" line="424"/>
        <source>{} 个项目 · {} 个数据集</source>
        <translation>{} proyectos · {} conjuntos de datos</translation>
    </message>
</context>
<context>
    <name>QueueMixin</name>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="97"/>
        <source>训练队列已启动</source>
        <translation>Cola de entrenamiento iniciada</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="107"/>
        <source>[队列] 已停止</source>
        <translation>[队列] Detenida</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="195"/>
        <source>[队列] 所有任务已执行完毕</source>
        <translation>[队列] Todas las tareas se han completado</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="203"/>
        <source>[队列] 跳过任务 {}: {}</source>
        <translation>[队列] Tarea omitida {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="204"/>
        <source>队列任务启动失败 {}: {}</source>
        <translation>Error al iniciar la tarea de la cola {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="224"/>
        <source>[队列] 缺少权重 {}, 该项训练会失败</source>
        <translation>[队列] Faltan pesos {}, ese entrenamiento fallará</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="227"/>
        <source>[队列] 缺少权重 {}, 该项训练时会自行下载</source>
        <translation>[队列] Faltan pesos {}, se descargarán automáticamente al entrenar esa tarea</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="240"/>
        <source>已有训练在进行中</source>
        <translation>Ya hay un entrenamiento en curso</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="245"/>
        <source>[队列] 开始队列第 {}/{} 项: {}</source>
        <translation>[队列] Iniciando el elemento {}/{} de la cola: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="249"/>
        <source>队列启动任务: {} record={}</source>
        <translation>La cola inicia la tarea: {} record={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="287"/>
        <source>训练未完成, 详见日志</source>
        <translation>El entrenamiento no terminó; consulte el registro</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="321"/>
        <source>[队列] 显存等待超时, 仍继续启动下一个任务</source>
        <translation>[队列] Se agotó el tiempo de espera de VRAM; se inicia igualmente la siguiente tarea</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="367"/>
        <source>队列 {}</source>
        <translation>Cola {}</translation>
    </message>
</context>
<context>
    <name>ResponsiveMixin</name>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="19"/>
        <location filename="../app/mixins/responsive_mixin.py" line="40"/>
        <source>更多</source>
        <translation>Más</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="43"/>
        <location filename="../app/mixins/responsive_mixin.py" line="52"/>
        <source>界面字号</source>
        <translation>Tamaño de fuente de la interfaz</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="58"/>
        <source>标准</source>
        <translation>Estándar</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="59"/>
        <source>大</source>
        <translation>Grande</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="60"/>
        <source>超大</source>
        <translation>Muy grande</translation>
    </message>
</context>
<context>
    <name>StatusText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="18"/>
        <source>等待中</source>
        <translation>En espera</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="19"/>
        <location filename="../app/widgets/status_style.py" line="26"/>
        <source>训练中</source>
        <translation>En entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="20"/>
        <location filename="../app/widgets/status_style.py" line="27"/>
        <source>已完成</source>
        <translation>Finalizado</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="21"/>
        <location filename="../app/widgets/status_style.py" line="28"/>
        <source>失败</source>
        <translation>Fallido</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="22"/>
        <location filename="../app/widgets/status_style.py" line="31"/>
        <source>已跳过</source>
        <translation>Omitido</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="23"/>
        <location filename="../app/widgets/status_style.py" line="29"/>
        <source>已停止</source>
        <translation>Detenido</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="24"/>
        <location filename="../app/widgets/status_style.py" line="32"/>
        <source>已中断</source>
        <translation>Interrumpido</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="30"/>
        <source>失败/已停止</source>
        <translation>Fallido/Detenido</translation>
    </message>
</context>
<context>
    <name>TaskText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="37"/>
        <source>检测</source>
        <translation>Detección</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="38"/>
        <source>分割</source>
        <translation>Segmentación</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="39"/>
        <source>分类</source>
        <translation>Clasificación</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="40"/>
        <source>异常检测</source>
        <translation>Detección de anomalías</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="41"/>
        <location filename="../app/widgets/status_style.py" line="42"/>
        <source>字符检测</source>
        <translation>Detección de texto</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="43"/>
        <source>字符识别</source>
        <translation>Reconocimiento de texto</translation>
    </message>
</context>
<context>
    <name>TestDialog</name>
    <message>
        <location filename="../ui/test_dialog.ui" line="14"/>
        <location filename="../ui/test_dialog.ui" line="41"/>
        <source>模型测试</source>
        <translation>Prueba de modelo</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="102"/>
        <source>检测</source>
        <translation>Detección</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="118"/>
        <source>best.pth</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="130"/>
        <source>mAP50 0.912 · 输入 640 · 规模 n · 训练 2026-09-01 14:22</source>
        <translation>mAP50 0.912 · Entrada 640 · Escala n · Entrenado 2026-09-01 14:22</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="151"/>
        <source>数据与设备</source>
        <translation>Datos y dispositivo</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="193"/>
        <source>数据</source>
        <translation>Datos</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="216"/>
        <source>设备</source>
        <translation>Dispositivo</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="246"/>
        <source>测试参数</source>
        <translation>Parámetros de prueba</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="288"/>
        <source>置信度</source>
        <translation>Confianza</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="329"/>
        <source>低于该分数的预测直接丢弃</source>
        <translation>Las predicciones con una puntuación inferior a este valor se descartan</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="345"/>
        <source>IoU 阈值</source>
        <translation>Umbral IoU</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="386"/>
        <source>与标注框重合度达标才算正确检出</source>
        <translation>La superposición con la caja anotada debe alcanzar este valor para contar como detección correcta</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="402"/>
        <source>输出标签文件</source>
        <translation>Escribir archivos de etiquetas</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="434"/>
        <source>写在图像目录下, 可重载数据集查看检出效果</source>
        <translation>Se escribe en el directorio de imágenes; recargue el conjunto de datos para revisar los resultados</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="486"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="496"/>
        <source>请选择数据集</source>
        <translation>Seleccione conjuntos de datos</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="544"/>
        <location filename="../app/widgets/test_dialog.py" line="109"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="551"/>
        <source>开始测试</source>
        <translation>Iniciar prueba</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="237"/>
        <source>未指定模型</source>
        <translation>Ningún modelo especificado</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="238"/>
        <source>请在模型列表中重新选择一行</source>
        <translation>Vuelva a seleccionar una fila en la lista de modelos</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="254"/>
        <source>输入 {}</source>
        <translation>Entrada {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="256"/>
        <source>规模 {}</source>
        <translation>Escala {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="258"/>
        <source>训练 {}</source>
        <translation>Entrenado {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="260"/>
        <source>该记录未保存训练指标</source>
        <translation>Este registro no tiene métricas de entrenamiento guardadas</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="263"/>
        <source> · 文件已不存在</source>
        <translation> · el archivo ya no existe</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="289"/>
        <source>请先勾选要测试的数据集</source>
        <translation>Marque primero los conjuntos de datos que desea probar</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="301"/>
        <source>{} 个数据集 · {} 张图</source>
        <translation>{} conjuntos de datos · {} imágenes</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="303"/>
        <source>分类数据集, 统计每张图的判断正确率</source>
        <translation>Conjunto de datos de clasificación; se mide la exactitud por imagen</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="305"/>
        <source>已标注, 评估模式: 统计检出率 / 漏检 / 误检</source>
        <translation>Etiquetado, modo evaluación: mide la tasa de detección / omisiones / falsos positivos</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="307"/>
        <source>未标注, 推理模式: 只输出预测标签</source>
        <translation>Sin etiquetar, modo inferencia: solo genera las etiquetas predichas</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="309"/>
        <source>部分已标注, 已标注与未标注的数据集不能一起测</source>
        <translation>Parcialmente etiquetado; los conjuntos de datos etiquetados y sin etiquetar no se pueden probar juntos</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="336"/>
        <source>为判定为不良品的图写 &lt;同名&gt;.json 到图像目录, 多边形标出异常区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Escribe &lt;mismo nombre&gt;.json junto a las imágenes juzgadas como defectuosas; los polígonos marcan las regiones anómalas y la herramienta de anotación puede abrirlos directamente; si ya hay una anotación manual, se sobrescribe</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="340"/>
        <source>把异常区域写成 labelme json, 便于重载复核</source>
        <translation>Escribe las regiones anómalas como json de labelme para recargarlas y revisarlas fácilmente</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="353"/>
        <source>字符识别只报告字条识别率, 不输出标注文件</source>
        <translation>El reconocimiento de texto solo informa la tasa de acierto de los recortes de texto; no se escriben archivos de anotación</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="359"/>
        <location filename="../app/widgets/test_dialog.py" line="365"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 框出文本区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Escribe &lt;mismo-nombre&gt;.json en el directorio de cada imagen, enmarcando las regiones de texto; se puede abrir directamente en la herramienta de anotación; las anotaciones manuales existentes se sobrescribirán</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="368"/>
        <source>把检测到的文本框写成 labelme json, 便于重载复核</source>
        <translation>Escribe los cuadros de texto detectados en labelme json para revisarlos después de recargar</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="371"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Escribe &lt;mismo nombre&gt;.json junto a cada imagen para que la herramienta de anotación pueda abrirlo directamente; las anotaciones manuales existentes se sobrescribirán</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="388"/>
        <location filename="../app/widgets/test_dialog.py" line="392"/>
        <location filename="../app/widgets/test_dialog.py" line="406"/>
        <location filename="../app/widgets/test_dialog.py" line="412"/>
        <location filename="../app/widgets/test_dialog.py" line="425"/>
        <location filename="../app/widgets/test_dialog.py" line="435"/>
        <location filename="../app/widgets/test_dialog.py" line="441"/>
        <location filename="../app/widgets/test_dialog.py" line="456"/>
        <source>测试</source>
        <translation>Probar</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="388"/>
        <source>已有测试在进行中</source>
        <translation>Ya hay una prueba en curso</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="392"/>
        <source>请至少选择一个数据集</source>
        <translation>Seleccione al menos un conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="407"/>
        <source>置信度/iou阈值必须是数字</source>
        <translation>La confianza / el umbral IoU deben ser un número</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="413"/>
        <source>模型文件不存在, 请重新选择</source>
        <translation>El archivo del modelo no existe; selecciónelo de nuevo</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="426"/>
        <source>数据集 {}/{} 未导入图像</source>
        <translation>El conjunto de datos {}/{} no tiene imágenes importadas</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="436"/>
        <source>分类数据集与检测/分割数据集不能同时测试: {}/{}</source>
        <translation>Los conjuntos de datos de clasificación y de detección/segmentación no se pueden probar juntos: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="442"/>
        <source>已标注与未标注的数据集不能同时测试: {}/{}</source>
        <translation>Los conjuntos de datos etiquetados y sin etiquetar no se pueden probar juntos: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="457"/>
        <source>字符识别要拿标注框裁字条才能测, 请选择已标注的数据集</source>
        <translation>El reconocimiento de texto necesita cuadros anotados para recortar el texto; seleccione un conjunto de datos ya anotado</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="483"/>
        <source>[test] 启动测试 worker: model={} 数据集={} 图像目录={} device={} cfg={}</source>
        <translation>[test] Iniciando worker de prueba: model={} conjunto de datos={} directorio de imágenes={} device={} cfg={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="488"/>
        <source>测试准备中...</source>
        <translation>Preparando la prueba...</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="505"/>
        <location filename="../app/widgets/test_dialog.py" line="506"/>
        <source>测试即将开始</source>
        <translation>La prueba está a punto de comenzar</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="552"/>
        <source>测试中 {}/{}</source>
        <translation>Probando {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="572"/>
        <source>[test-dialog] 测试完成, ok={}</source>
        <translation>[test-dialog] Prueba completada, ok={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="580"/>
        <location filename="../app/widgets/test_dialog.py" line="590"/>
        <source>测试结果</source>
        <translation>Resultados de la prueba</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="581"/>
        <source>测试未正常完成</source>
        <translation>La prueba no finalizó correctamente</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="591"/>
        <source>字条 {} 条 · CER {:.4f} · 全对 {} 条</source>
        <translation>{} recortes de texto · CER {:.4f} · {} completamente correctos</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="598"/>
        <source>[test-dialog] 测试失败: {}</source>
        <translation>[test-dialog] Prueba fallida: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="605"/>
        <source>测试失败</source>
        <translation>Prueba fallida</translation>
    </message>
</context>
<context>
    <name>TestReport</name>
    <message>
        <location filename="../app/train/test_report.py" line="179"/>
        <source>漏 {}</source>
        <translation>Omitidos {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="181"/>
        <source>误 {}</source>
        <translation>Falsos pos. {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="183"/>
        <source>认错 {}</source>
        <translation>Clase errónea {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="194"/>
        <source>(图片无法打开)</source>
        <translation>(no se puede abrir la imagen)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="280"/>
        <source>类别认错: {} → {}</source>
        <translation>Clase errónea: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="308"/>
        <source>本次验证集没有漏检, 也没有误检.</source>
        <translation>En este conjunto de validación no hay omisiones ni falsos positivos.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="311"/>
        <source>明细抽样: 共 {} 张有问题(漏检 {} / 误检 {}), 本报告抽取 {} 张 - 每个类别每种错误最多 {} 张, 按错误数从多到少取</source>
        <translation>Muestreo de detalles: {} imágenes con problemas (omisiones {} / falsos positivos {}); este informe incluye {} imágenes - como máximo {} por clase y tipo de error, ordenadas de más a menos errores</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="316"/>
        <source>明细: 共 {} 张有问题(漏检 {} / 误检 {}), 已全部列出</source>
        <translation>Detalles: {} imágenes con problemas (omisiones {} / falsos positivos {}), todas listadas</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="343"/>
        <source>漏检 GT: 有标注但模型没检出</source>
        <translation>Omisión GT: hay anotación pero el modelo no la detectó</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="345"/>
        <source>误检预测: 模型检出但标注里没有</source>
        <translation>Falso positivo predicho: el modelo lo detectó pero no está en las anotaciones</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="347"/>
        <source>正确检出(仅作位置参照)</source>
        <translation>Detección correcta (solo como referencia de posición)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="349"/>
        <source>类别认错: 位置对但判错类别(GT → 预测)</source>
        <translation>Clase errónea: posición correcta pero clase incorrecta (GT → predicción)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="352"/>
        <source>虚线轮廓: 分割 mask / 标注多边形(判定按外接框 IoU)</source>
        <translation>Contorno discontinuo: máscara de segmentación / polígono de anotación (se evalúa por IoU de la caja envolvente)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="450"/>
        <location filename="../app/train/test_report.py" line="1049"/>
        <source>模型评估报告</source>
        <translation>Informe de evaluación del modelo</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="454"/>
        <source>当前训练模型</source>
        <translation>Modelo entrenado actual</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="458"/>
        <location filename="../app/train/test_report.py" line="464"/>
        <source>(未记录)</source>
        <translation>(sin registro)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="463"/>
        <source>数据集 </source>
        <translation>Conjunto de datos </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="466"/>
        <source>置信度 {}</source>
        <translation>Confianza {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="486"/>
        <source>测试张数</source>
        <translation>Imágenes probadas</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="487"/>
        <location filename="../app/train/test_report.py" line="489"/>
        <source>{} 张</source>
        <translation>{} imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="488"/>
        <source>有问题的图片</source>
        <translation>Imágenes con problemas</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="491"/>
        <source>检出率 (Recall)</source>
        <translation>Tasa de detección (Recall)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="493"/>
        <source>准确率 (Precision)</source>
        <translation>Exactitud (Precision)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="495"/>
        <source>正确检出</source>
        <translation>Correctos</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="496"/>
        <source>{} 个</source>
        <translation>{} unidades</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="497"/>
        <source>漏检 (该抓没抓)</source>
        <translation>Omisiones (no detectados)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="498"/>
        <location filename="../app/train/test_report.py" line="501"/>
        <location filename="../app/train/test_report.py" line="506"/>
        <source>{} 个 / {} 张图</source>
        <translation>{} unidades / {} imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="500"/>
        <source>误检 (过杀)</source>
        <translation>Falsos positivos (detección excesiva)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="505"/>
        <source>类别认错 (位置对, 类别错)</source>
        <translation>Clase errónea (posición correcta, clase incorrecta)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="508"/>
        <source>指标</source>
        <translation>Métrica</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="509"/>
        <source>值</source>
        <translation>Valor</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="528"/>
        <source>按类别</source>
        <translation>Por clase</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="531"/>
        <source>类别</source>
        <translation>Clase</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="532"/>
        <source>标注</source>
        <translation>Anotación</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="533"/>
        <source>正确</source>
        <translation>Correctas</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="534"/>
        <source>漏检</source>
        <translation>Omitidos</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="535"/>
        <source>误检</source>
        <translation>Falsos pos.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="536"/>
        <source>检出率</source>
        <translation>Tasa de detección</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="537"/>
        <source>准确率</source>
        <translation>Exactitud</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="564"/>
        <source>... 另有 {} 类未列出</source>
        <translation>... {} clases más no listadas</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="586"/>
        <source>错误样本明细(仅列漏检 / 误检图片, 正确检出不列出)</source>
        <translation>Detalle de muestras con error (solo imágenes con omisiones / falsos positivos; las detecciones correctas no se listan)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="625"/>
        <source>本轮检出率 {:.0f}%, 准确率 {:.0f}%.</source>
        <translation>Tasa de detección de esta ronda {:.0f}%, exactitud {:.0f}%.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="628"/>
        <source>没有逐类别统计, 无法定位到具体标签,请先确认标签文件能正常读到.</source>
        <translation>No hay estadísticas por clase y no se puede localizar la etiqueta concreta; compruebe primero que los archivos de etiquetas se lean correctamente.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="652"/>
        <source>漏检分布在</source>
        <translation>Las omisiones se distribuyen en</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="653"/>
        <source>漏检集中在</source>
        <translation>Las omisiones se concentran en</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="656"/>
        <source>(共 {} 个), 优先补这几类的姿态, 光照样本,并复核标注是否有遗漏.</source>
        <translation>(en total {}), añada primero muestras de postura e iluminación de estas clases y revise si faltan anotaciones.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="662"/>
        <source>误检分布在</source>
        <translation>Los falsos positivos se distribuyen en</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="663"/>
        <source>误检以</source>
        <translation>Los falsos positivos se concentran en</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="664"/>
        <source>({} 个),属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({} unidades), detección excesiva; añada muestras negativas sin defectos y limpie el ruido en las anotaciones.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="666"/>
        <source>({} 个)为主,属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({} unidades) como principal, detección excesiva; añada muestras negativas sin defectos y limpie el ruido en las anotaciones.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="675"/>
        <source>暂无</source>
        <translation>Ninguna</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="679"/>
        <source>此外 {} 处位置对但类别判错</source>
        <translation>Además, {} casos con posición correcta pero clase incorrecta</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="681"/>
        <source>(报告紫框), 属分类能力不足而非定位问题,需补易混淆类别之间的区分性样本.</source>
        <translation>(marcados en morado en el informe); se debe a una capacidad de clasificación insuficiente y no a un problema de localización, así que añada muestras más discriminativas entre las clases que se confunden con facilidad.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="686"/>
        <source>其中</source>
        <translation>De ellos</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="688"/>
        <source>仅 {} 个标注, 样本不足是主要瓶颈, 建议补到 200 个以上.</source>
        <translation>Solo {} anotaciones; la falta de muestras es el principal cuello de botella, añada hasta superar las 200.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="693"/>
        <source>各类样本量差距大(最多 {} / 最少 {}),训练时建议做类别均衡采样.</source>
        <translation>Gran diferencia de muestras entre clases (máx. {} / mín. {}); al entrenar, se recomienda un muestreo equilibrado por clase.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="698"/>
        <source>把本报告中的漏检, 误检图加入训练集复训,再用同参数复测对比.</source>
        <translation>Añada al conjunto de entrenamiento las imágenes con omisiones y falsos positivos de este informe, vuelva a entrenar y repita la prueba con los mismos parámetros para comparar.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="702"/>
        <source>本轮无漏检, 无误检, 建议用更严的阈值或更难的样本再压一轮, 确认稳定性.</source>
        <translation>En esta ronda no hubo omisiones ni falsos positivos; repita la prueba con un umbral más estricto o muestras más difíciles para confirmar la estabilidad.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="898"/>
        <source>改进建议</source>
        <translation>Sugerencias de mejora</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="903"/>
        <source>基于本次测试的指标与按类别表现</source>
        <translation>Según las métricas de esta prueba y el rendimiento por clase</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="905"/>
        <source>(模型: {})</source>
        <translation>(modelo: {})</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="907"/>
        <source>, 建议如下:</source>
        <translation>, se recomienda lo siguiente:</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="925"/>
        <source>标红的标签是需要重点关注的类别.</source>
        <translation>Las etiquetas marcadas en rojo son las clases que requieren especial atención.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="930"/>
        <location filename="../app/train/test_report.py" line="956"/>
        <source>第 {} 页</source>
        <translation>Página {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1020"/>
        <source>{}(抽取 {} / 共 {} 张)</source>
        <translation>{}(seleccionadas {} / de {} imágenes)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1023"/>
        <source>{}(共 {} 张)</source>
        <translation>{}({} imágenes en total)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1025"/>
        <source>漏检样本: 有标注但模型没检出</source>
        <translation>Muestras omitidas: hay anotación pero el modelo no la detectó</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1028"/>
        <source>误检样本: 模型检出但标注里没有</source>
        <translation>Muestras con falso positivo: el modelo lo detectó pero no está en las anotaciones</translation>
    </message>
</context>
<context>
    <name>TestResultDialog</name>
    <message>
        <location filename="../ui/test_result.ui" line="14"/>
        <source>测试结果分析</source>
        <translation>Análisis de resultados de la prueba</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="83"/>
        <source>图像维度</source>
        <translation>Por imagen</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="93"/>
        <source>按「张」统计</source>
        <translation>Recuento por imagen</translation>
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
        <translation>Imágenes probadas</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="219"/>
        <source>全对图像</source>
        <translation>Imágenes totalmente correctas</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="275"/>
        <source>有漏检图像</source>
        <translation>Imágenes con omisiones</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="331"/>
        <location filename="../app/train/test_result_dialog.py" line="251"/>
        <source>有误检图像</source>
        <translation>Imágenes con falsos positivos</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="375"/>
        <source>标签维度</source>
        <translation>Por etiqueta</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="385"/>
        <source>按「标注框」统计</source>
        <translation>Recuento por caja</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="455"/>
        <location filename="../ui/test_result.ui" line="664"/>
        <location filename="../app/train/test_result_dialog.py" line="259"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>正确检出</source>
        <translation>Correctos</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="511"/>
        <location filename="../ui/test_result.ui" line="669"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>漏检</source>
        <translation>Omitidos</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="567"/>
        <location filename="../ui/test_result.ui" line="674"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>误检</source>
        <translation>Falsos pos.</translation>
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
        <translation>Exactitud</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="654"/>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>类别</source>
        <translation>Clase</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="659"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>标注数</source>
        <translation>Cajas</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="679"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>检出率</source>
        <translation>Tasa de detección</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="708"/>
        <source>每类抽取</source>
        <translation>Por clase</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="715"/>
        <source>每个类别的每种错误（漏检 / 误检）最多列出几张图。
报告体积约 120 KB 一张，样本多时调小可以显著减小 PDF；选「全部」则每张有问题的图都列。</source>
        <translation>Número máximo de imágenes listadas por cada tipo de error (omisión / falso positivo) de cada clase.
El informe ocupa unos 120 KB por imagen; con muchas muestras, reducirlo disminuye notablemente el PDF. Si elige &quot;Todo&quot;, se listan todas las imágenes con problemas.</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="719"/>
        <source> 张</source>
        <translation> imágenes</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="722"/>
        <source>全部</source>
        <translation>Todo</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="751"/>
        <location filename="../app/train/test_result_dialog.py" line="187"/>
        <source>导出 PDF 报告</source>
        <translation>Exportar informe PDF</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="758"/>
        <location filename="../app/train/test_result_dialog.py" line="92"/>
        <source>确定</source>
        <translation>Aceptar</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="152"/>
        <source>把漏检/误检的图逐张画框导出成 PDF</source>
        <translation>Exporta a PDF las imágenes con omisiones/falsos positivos con las cajas dibujadas una a una</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="155"/>
        <source>异常检测的逐图结果已写成 CSV, 不支持导出画框 PDF</source>
        <translation>Los resultados por imagen de la detección de anomalías se escribieron en CSV; no se admite exportar el PDF con recuadros</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="157"/>
        <source>本次测试没有逐图错误明细, 无法导出</source>
        <translation>Esta prueba no tiene detalle de errores por imagen; no se puede exportar</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="169"/>
        <source>保存 PDF 报告</source>
        <translation>Guardar informe PDF</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="170"/>
        <source>PDF 文件 (*.pdf)</source>
        <translation>Archivos PDF (*.pdf)</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="176"/>
        <source>正在生成...</source>
        <translation>Generando...</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="194"/>
        <source>无需导出</source>
        <translation>Nada que exportar</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="195"/>
        <source>本次测试没有漏检也没有误检, 没有内容可写.</source>
        <translation>Esta prueba no tiene omisiones ni falsos positivos; no hay contenido que escribir.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="198"/>
        <source>导出完成</source>
        <translation>Exportación completada</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="199"/>
        <source>PDF 报告已保存到:
{}</source>
        <translation>Informe PDF guardado en:
{}</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="203"/>
        <source>导出失败</source>
        <translation>Error de exportación</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="238"/>
        <source>按&quot;张&quot;统计 · 检出 1 个即算检出</source>
        <translation>Recuento por imagen · basta con detectar 1 para contar como detectado</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="240"/>
        <source> · 有标注 {} 张</source>
        <translation> · {} imágenes con etiquetas</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="244"/>
        <source>检出图像</source>
        <translation>Imágenes detectadas</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="245"/>
        <location filename="../app/train/test_result_dialog.py" line="260"/>
        <source>检出率 </source>
        <translation>Tasa de detección </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="247"/>
        <source>未检出图像</source>
        <translation>Imágenes no detectadas</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="248"/>
        <source>未检出率 </source>
        <translation>Tasa de omisión </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="252"/>
        <source>误检率 </source>
        <translation>Tasa de falsos positivos </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="257"/>
        <source>按&quot;标注框&quot;统计 · 标注总数 {}</source>
        <translation>Recuento por caja · {} cajas en total</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="280"/>
        <source>按&quot;张&quot;统计 · 每张图判一个类别</source>
        <translation>Recuento por imagen · se asigna una clase a cada imagen</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="285"/>
        <source>判断正确</source>
        <translation>Correcto</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="287"/>
        <source>判断错误</source>
        <translation>Incorrecto</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="290"/>
        <location filename="../app/train/test_result_dialog.py" line="362"/>
        <source>精度</source>
        <translation>Precisión</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="315"/>
        <source>按&quot;张&quot;统计 · 整图判良品/不良品</source>
        <translation>Recuento por imagen · cada imagen se juzga como buena o defectuosa</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="329"/>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <source>检出异常</source>
        <translation>Anomalías detectadas</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <source>总图数</source>
        <translation>Total de imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="345"/>
        <source>异常</source>
        <translation>Anomalía</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <source>正确</source>
        <translation>Correctas</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="362"/>
        <source>错误</source>
        <translation>Incorrectas</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="383"/>
        <source>模型里没有判定阈值, 只报告分数, 逐图分数见 CSV 明细.</source>
        <translation>El modelo no tiene umbral de decisión; solo se informan las puntuaciones. Consulte el CSV para las puntuaciones por imagen.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="384"/>
        <source>判定阈值 {:.4f}. 本次 {} 张, 检出异常 {} 张.</source>
        <translation>Umbral de decisión {:.4f}. Probadas {} imágenes, {} anomalías detectadas.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="297"/>
        <source>整体精度 {:.1f}%, &quot;{}&quot;类错误最多({} 张), 是拉低精度的主要原因.</source>
        <translation>Exactitud global {:.1f}%. La clase &quot;{}&quot; concentra la mayoría de los errores ({} imágenes) y es la causa principal de la baja exactitud.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="422"/>
        <source>整体漏检偏多(漏检 {} 个, 多于误检 {} 个).&quot;{}&quot;类漏检最多({} 个), 是检出率低的主要原因.</source>
        <translation>Las omisiones predominan en general ({} omitidos frente a {} falsos positivos). La clase &quot;{}&quot; concentra la mayoría de las omisiones ({}) y es la causa principal de la baja tasa de detección.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="428"/>
        <source>整体误检偏多(误检 {} 个, 多于漏检 {} 个).&quot;{}&quot;类误检最多({} 个), 是准确率低的主要原因.</source>
        <translation>Los falsos positivos predominan en general ({} frente a {} omitidos). La clase &quot;{}&quot; concentra la mayoría de los falsos positivos ({}) y es la causa principal de la baja precisión.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="432"/>
        <source>模型表现良好: 无漏检, 无误检.</source>
        <translation>El modelo funciona bien: sin omisiones ni falsos positivos.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="434"/>
        <source>另有 {} 处位置对但类别判错(报告里用紫框标出),属分类能力不足, 需补易混淆类别的区分性样本.</source>
        <translation>Otras {} cajas están bien situadas pero con la clase incorrecta (marcadas con cajas moradas en el informe); esto indica una capacidad de clasificación insuficiente y requiere añadir muestras más discriminativas para las clases que se confunden con facilidad.</translation>
    </message>
</context>
<context>
    <name>TestRunner</name>
    <message>
        <location filename="../app/train/test_runner.py" line="278"/>
        <source>覆盖已有标注 {}</source>
        <translation>Sobrescribir las anotaciones existentes {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="308"/>
        <source>明细初始化失败: {}</source>
        <translation>Error al inicializar el detalle: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="317"/>
        <source>明细目录创建失败: {}</source>
        <translation>Error al crear el directorio de detalles: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="345"/>
        <source>明细写入失败: {}</source>
        <translation>Error al escribir los detalles: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="427"/>
        <source>当前安装缺少所需组件, 无法执行测试</source>
        <translation>Esta instalación no incluye los componentes necesarios; no se puede ejecutar la prueba</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="429"/>
        <source>加载模型: {}</source>
        <translation>Cargando modelo: {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_backend.py" line="36"/>
        <source>推理已优化: {}</source>
        <translation>Inferencia optimizada: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="446"/>
        <source>测试图片 {} 张</source>
        <translation>{} imágenes de prueba</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="496"/>
        <source>预测失败 {}: {}</source>
        <translation>Error de predicción {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="510"/>
        <source>输出标注失败 {}: {}</source>
        <translation>Error al escribir las anotaciones {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="565"/>
        <source>WARN 标签目录存在但所有 {} 张图都没读到 GT,请确认标签是 .txt (YOLO) 或 .json (labelme)</source>
        <translation>WARN El directorio de etiquetas existe, pero no se leyó GT para ninguna de las {} imágenes; compruebe que las etiquetas sean .txt (YOLO) o .json (labelme)</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="570"/>
        <source>WARN {} 张图缺标签文件</source>
        <translation>WARN {} imágenes sin archivo de etiquetas</translation>
    </message>
</context>
<context>
    <name>TestWorker</name>
    <message>
        <location filename="../app/train/test_worker.py" line="83"/>
        <source>run 开始</source>
        <translation>run iniciado</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="97"/>
        <source>启动子进程: {} {}</source>
        <translation>Iniciando subproceso: {} {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="109"/>
        <source>启动子进程失败: {}</source>
        <translation>Error al iniciar el subproceso: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="116"/>
        <source>启动测试进程失败: {}</source>
        <translation>Error al iniciar el proceso de prueba: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="118"/>
        <location filename="../app/train/test_worker.py" line="120"/>
        <source>子进程已启动 pid={}</source>
        <translation>Subproceso iniciado pid={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="152"/>
        <source>进入轮询循环</source>
        <translation>Entrando en el bucle de sondeo</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="162"/>
        <source>轮询中: 文件={}B 已读{}行 子进程={}</source>
        <translation>Sondeando: archivo={}B, {} líneas leídas, subproceso={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="172"/>
        <source>轮询异常:
</source>
        <translation>Excepción en el sondeo: 
</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="180"/>
        <source>轮询结束 rc={}</source>
        <translation>Sondeo finalizado rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="182"/>
        <source>子进程退出 rc={}</source>
        <translation>Subproceso finalizado rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="192"/>
        <source>测试未能完成, 详情见日志</source>
        <translation>No se pudo completar la prueba, consulte el registro para más detalles</translation>
    </message>
</context>
<context>
    <name>TrainDialog</name>
    <message>
        <location filename="../ui/train.ui" line="14"/>
        <location filename="../ui/train.ui" line="40"/>
        <location filename="../app/train/dialogs.py" line="493"/>
        <source>训练</source>
        <translation>Entrenar</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="50"/>
        <location filename="../ui/train.ui" line="169"/>
        <source>检测</source>
        <translation>Detección</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="118"/>
        <source>模型与数据</source>
        <translation>Modelo y datos</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="158"/>
        <source>任务类型</source>
        <translation>Tipo de tarea</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="174"/>
        <source>分割</source>
        <translation>Segmentación</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="179"/>
        <source>分类</source>
        <translation>Clasificación</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="184"/>
        <source>异常检测</source>
        <translation>Detección de anomalías</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="189"/>
        <source>字符检测</source>
        <translation>Detección de texto</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="197"/>
        <source>型号</source>
        <translation>Modelo</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="210"/>
        <location filename="../app/train/dialogs.py" line="715"/>
        <source>训练集</source>
        <translation>Conjunto de entrenamiento</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="230"/>
        <source>验证集</source>
        <translation>Conjunto de validación</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="250"/>
        <source>设备</source>
        <translation>Dispositivo</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="263"/>
        <source>架构</source>
        <translation>Arquitectura</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="296"/>
        <source>训练超参</source>
        <translation>Hiperparámetros</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="336"/>
        <location filename="../app/train/dialogs.py" line="589"/>
        <source>轮次</source>
        <translation>Épocas</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="349"/>
        <source>优化器</source>
        <translation>Optimizador</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="362"/>
        <location filename="../app/train/dialogs.py" line="592"/>
        <source>早停</source>
        <translation>Parada temprana</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="399"/>
        <source>连续无提升则提前结束，0 为关闭</source>
        <translation>Finaliza antes si no hay mejoras; 0 lo desactiva</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="415"/>
        <location filename="../app/train/dialogs.py" line="595"/>
        <source>学习率</source>
        <translation>Tasa de aprendizaje</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="452"/>
        <source>初始学习率，训练中自动衰减</source>
        <translation>Tasa de aprendizaje inicial, se reduce automáticamente durante el entrenamiento</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="468"/>
        <location filename="../app/train/dialogs.py" line="587"/>
        <source>批次</source>
        <translation>Lote</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="481"/>
        <location filename="../app/train/dialogs.py" line="591"/>
        <source>图像尺寸</source>
        <translation>Tamaño de imagen</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="512"/>
        <source>32 的倍数</source>
        <translation>múltiplo de 32</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="528"/>
        <location filename="../app/train/dialogs.py" line="588"/>
        <source>梯度累积</source>
        <translation>Acum. gradiente</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="565"/>
        <source>显存不足时调大，等效批次 × N</source>
        <translation>Auméntelo si falta VRAM; lote efectivo × N</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="581"/>
        <location filename="../app/train/dialogs.py" line="590"/>
        <source>线程数</source>
        <translation>Número de hilos</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="642"/>
        <source>数据增强</source>
        <translation>Aumento de datos</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="723"/>
        <source>输出</source>
        <translation>Salida</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="766"/>
        <source>输出路径</source>
        <translation>Ruta de salida</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="781"/>
        <source>留空则自动按时间生成目录</source>
        <translation>Si se deja vacío, se crea una carpeta con la fecha automáticamente</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="794"/>
        <source>选择路径</source>
        <translation>Examinar</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="839"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="855"/>
        <location filename="../app/train/dialogs.py" line="681"/>
        <source>请选择训练集与验证集</source>
        <translation>Seleccione un conjunto de entrenamiento y uno de validación</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="903"/>
        <location filename="../app/train/dialogs.py" line="604"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="916"/>
        <location filename="../app/train/dialogs.py" line="1343"/>
        <location filename="../app/train/dialogs.py" line="1352"/>
        <location filename="../app/train/dialogs.py" line="1363"/>
        <location filename="../app/train/dialogs.py" line="1382"/>
        <location filename="../app/train/dialogs.py" line="1395"/>
        <source>加入队列</source>
        <translation>Añadir a la cola</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="929"/>
        <location filename="../app/train/dialogs.py" line="1274"/>
        <location filename="../app/train/dialogs.py" line="1284"/>
        <location filename="../app/train/dialogs.py" line="1310"/>
        <source>开始训练</source>
        <translation>Iniciar entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="40"/>
        <source>正在检测显卡...</source>
        <translation>Detectando GPU...</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="83"/>
        <location filename="../app/train/dialogs.py" line="85"/>
        <source>0.5</source>
        <translation>0.5</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="89"/>
        <source>±20%</source>
        <translation>±20%</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="226"/>
        <source>数据集&quot;{}&quot;尚未导入图像或路径无效, 请先导入该数据集再训练</source>
        <translation>El conjunto de datos &quot;{}&quot; no tiene imágenes importadas o su ruta no es válida. Importe ese conjunto de datos antes de entrenar.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="233"/>
        <source>数据集&quot;{}&quot;尚未导入标签或路径无效, 请先导入该数据集再训练</source>
        <translation>El conjunto de datos &quot;{}&quot; no tiene etiquetas importadas o su ruta no es válida. Importe ese conjunto de datos antes de entrenar.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="262"/>
        <location filename="../app/train/dialogs.py" line="1353"/>
        <source>请先选择输出路径</source>
        <translation>Seleccione primero una ruta de salida</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="23"/>
        <source>数据集&quot;{}/{}&quot;不是分类数据集(标签格式={}), 无法训练{}</source>
        <translation>El conjunto de datos &quot;{}/{}&quot; no es un conjunto de datos de clasificación (formato de etiquetas={}); no se puede entrenar {}</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="29"/>
        <source>未知</source>
        <translation>desconocido</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="25"/>
        <source>数据集&quot;{}/{}&quot;是分类数据集, 无法训练{}任务</source>
        <translation>El conjunto de datos &quot;{}/{}&quot; es un conjunto de datos de clasificación; no se puede entrenar una tarea de {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="289"/>
        <source>请至少选择一个训练集数据集</source>
        <translation>Seleccione al menos un conjunto de datos para entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="291"/>
        <source>请至少选择一个验证集数据集</source>
        <translation>Seleccione al menos un conjunto de datos para validación</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="331"/>
        <source>未选数据集</source>
        <translation>sin conjunto de datos seleccionado</translation>
    </message>
    <message>
        <location filename="../app/train/detect_common.py" line="12"/>
        <source>目标检测推荐图像尺寸: 640(可设为 32 的倍数如 640/672)</source>
        <translation>Tamaño de imagen recomendado para detección: 640 (puede ser múltiplo de 32, p. ej. 640/672)</translation>
    </message>
    <message>
        <location filename="../app/train/segment_common.py" line="16"/>
        <source>CNN 分割推荐尺寸: 640(需为 32 的倍数)</source>
        <translation>Tamaño recomendado para segmentación CNN: 640 (debe ser múltiplo de 32)</translation>
    </message>
    <message>
        <location filename="../app/train/classify_common.py" line="27"/>
        <source>图像分类推荐尺寸: 224(小图用 224, 较大图可到 256)</source>
        <translation>Tamaño recomendado para clasificación: 224 (224 para imágenes pequeñas y hasta 256 para las más grandes)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="695"/>
        <source>异常检测推荐尺寸: 256; 缺陷很小时调到 512 更稳, 显存和耗时随之上升</source>
        <translation>Tamaño recomendado para detección de anomalías: 256; con defectos muy pequeños, 512 es más fiable, a costa de más VRAM y tiempo</translation>
    </message>
    <message>
        <location filename="../app/train/segment_common.py" line="17"/>
        <source>图像分割推荐尺寸: 648(需为 {} 的倍数)</source>
        <translation>Tamaño recomendado para segmentación: 648 (debe ser múltiplo de {})</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="27"/>
        <source>数据集&quot;{}/{}&quot;没有文本标注, 无法训练{}</source>
        <translation>El conjunto de datos &quot;{}/{}&quot; no tiene anotaciones de texto; no se puede entrenar {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_common.py" line="56"/>
        <source>字符检测推荐尺寸: 1024(需为 {} 的倍数); 识别段固定 32x128, 不受此项影响</source>
        <translation>Tamaño recomendado para la detección de texto: 1024 (debe ser múltiplo de {}); la etapa de reconocimiento es fija en 32x128 y no se ve afectada por este ajuste</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="466"/>
        <source>{} 的倍数</source>
        <translation>múltiplo de {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_common.py" line="31"/>
        <source>建议 224</source>
        <translation>224 recomendado</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="700"/>
        <source>建议 256</source>
        <translation>256 recomendado</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="691"/>
        <source>训练集 {} 个 · 验证集 {} 个 · 共 {} 张图</source>
        <translation>{} conjuntos de entrenamiento · {} de validación · {} imágenes en total</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="694"/>
        <source>未选择验证集</source>
        <translation>sin conjunto de validación seleccionado</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="696"/>
        <source>已标注, 可直接训练</source>
        <translation>etiquetado, listo para entrenar</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="698"/>
        <source>有 {} 个数据集尚未标注</source>
        <translation>{} conjuntos de datos sin etiquetar por completo</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="712"/>
        <source>请选择验证集</source>
        <translation>Seleccione conjuntos de validación</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="797"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>Ya hay un entrenamiento en curso; deténgalo primero</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="76"/>
        <source>几何变换</source>
        <translation>Geométrico</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="77"/>
        <source>标注框会跟着一起变换</source>
        <translation>Las cajas se transforman también</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="78"/>
        <source>像素变换</source>
        <translation>Píxel</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="79"/>
        <source>只改画面，标注框不动</source>
        <translation>Solo la imagen, cajas intactas</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="82"/>
        <source>水平翻转</source>
        <translation>Volteo horizontal</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="84"/>
        <source>垂直翻转</source>
        <translation>Volteo vertical</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="86"/>
        <source>旋转</source>
        <translation>Rotación</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="87"/>
        <source>±15°</source>
        <translation>±15°</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="88"/>
        <source>仿射</source>
        <translation>Afín</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="90"/>
        <source>马赛克</source>
        <translation>Mosaico</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="91"/>
        <source>4 图拼接</source>
        <translation>4 imágenes</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="92"/>
        <source>亮度/对比度</source>
        <translation>Brillo/contraste</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="93"/>
        <source>±0.1</source>
        <translation>±0.1</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="94"/>
        <source>颜色抖动</source>
        <translation>Variación de color</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="95"/>
        <source>饱和/色相</source>
        <translation>saturación/matiz</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="96"/>
        <source>高斯模糊</source>
        <translation>Desenfoque gaussiano</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="97"/>
        <source>核 3</source>
        <translation>kernel 3</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="98"/>
        <source>高斯噪声</source>
        <translation>Ruido gaussiano</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="99"/>
        <source>σ 0.05</source>
        <translation>σ 0.05</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="101"/>
        <source>已启用 {} 项</source>
        <translation>{} activos</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="102"/>
        <source>该任务不支持配置数据增强</source>
        <translation>Esta tarea no admite configurar el aumento de datos</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="104"/>
        <source>当前网络架构不支持该增强</source>
        <translation>La arquitectura de red actual no admite este aumento</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="722"/>
        <source>异常检测算法自带学习率与优化器, 不需要设置</source>
        <translation>Los algoritmos de detección de anomalías ya incluyen tasa de aprendizaje y optimizador; no hay nada que configurar</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="728"/>
        <source>建库型算法只提取特征建立记忆库, 没有训练轮次</source>
        <translation>Los algoritmos de tipo banco de memoria solo extraen características para crear el banco de memoria; no hay épocas de entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="669"/>
        <source>仅建库</source>
        <translation>Solo crear</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1210"/>
        <source>请至少选择一个数据集</source>
        <translation>Seleccione al menos un conjunto de datos</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1214"/>
        <location filename="../app/train/dialogs.py" line="1224"/>
        <source>&quot;{}&quot;不能为空</source>
        <translation>&quot;{}&quot; no puede estar vacío</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1219"/>
        <source>&quot;{}&quot;必须是整数(当前: {})</source>
        <translation>&quot;{}&quot; debe ser un número entero (actual: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1229"/>
        <source>&quot;{}&quot;必须是数字(当前: {})</source>
        <translation>&quot;{}&quot; debe ser un número (actual: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1238"/>
        <source>图像尺寸需为 {} 的倍数(当前 {}), 可改为 {}</source>
        <translation>El tamaño de imagen debe ser múltiplo de {} (actual {}); puede usar {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1254"/>
        <source>选择输出目录</source>
        <translation>Seleccionar directorio de salida</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1268"/>
        <source>当前安装缺少 CNN 架构所需的组件, 无法训练.
请重新安装软件后再试</source>
        <translation>Esta instalación no incluye los componentes necesarios para la arquitectura CNN; no se puede entrenar.
Vuelva a instalar el software e inténtelo de nuevo</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1275"/>
        <source>当前已有训练在进行中, 请先停止!</source>
        <translation>¡Ya hay un entrenamiento en curso; deténgalo primero!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1279"/>
        <source>参数校验未通过: {}</source>
        <translation>Validación de parámetros fallida: {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1280"/>
        <location filename="../app/train/dialogs.py" line="1339"/>
        <source>参数校验</source>
        <translation>Validación de parámetros</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1300"/>
        <source>训练启动失败: {}
{}</source>
        <translation>Error al iniciar el entrenamiento: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1303"/>
        <source>训练启动失败</source>
        <translation>Error al iniciar el entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1311"/>
        <source>已有训练在进行中, 请先停止!</source>
        <translation>¡Ya hay un entrenamiento en curso; deténgalo primero!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1313"/>
        <source>开始训练: 任务类型={} 训练集={} 验证集={}</source>
        <translation>Iniciando entrenamiento: tipo de tarea={} entrenamiento={} validación={}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1329"/>
        <source>开始训练: 字符检测分两段入队 | {} | {}</source>
        <translation>Iniciar entrenamiento: la detección de texto se encola en dos etapas | {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1368"/>
        <source>队列</source>
        <translation>Cola</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1369"/>
        <source>已更新该队列任务的参数</source>
        <translation>Se actualizaron los parámetros de la tarea en cola</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1375"/>
        <source>加入队列失败</source>
        <translation>Error al añadir a la cola</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1378"/>
        <source>加入训练队列: {} | {}</source>
        <translation>Añadir a la cola de entrenamiento: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1383"/>
        <source>已加入队列(第 {} 个), 可在首页&quot;队列&quot;中查看或启动.</source>
        <translation>Añadido a la cola (posición {}). Puede verlo o iniciarlo en &quot;Cola&quot; de la página principal.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1396"/>
        <source>字符检测已拆成检测段与识别段, 分别排在第 {} 和第 {} 个</source>
        <translation>La detección de texto se ha dividido en la etapa de detección y la etapa de reconocimiento, encoladas en las posiciones #{} y #{}</translation>
    </message>
</context>
<context>
    <name>TrainMixin</name>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="47"/>
        <source>{} 训练中 0/{}</source>
        <translation>{} entrenando 0/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="86"/>
        <source>[train] 训练线程已结束但未返回结果, 按失败收尾</source>
        <translation>[train] El hilo de entrenamiento terminó pero no devolvió resultado; se cierra como error</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="97"/>
        <source>仅停止当前</source>
        <translation>Detener solo el actual</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="98"/>
        <source>停止队列</source>
        <translation>Detener la cola</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <location filename="../app/mixins/train_mixin.py" line="121"/>
        <source>停止训练</source>
        <translation>Detener entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <source>当前正在跑训练队列, 要停止到什么范围?</source>
        <translation>La cola de entrenamiento está en ejecución. ¿Hasta qué punto desea detenerla?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="102"/>
        <location filename="../app/mixins/train_mixin.py" line="103"/>
        <source>取消</source>
        <translation>Cancelar</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <source>确定要停止当前训练吗?</source>
        <translation>¿Detener el entrenamiento actual?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="117"/>
        <source>手动停止训练: {}</source>
        <translation>Entrenamiento detenido manualmente: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="119"/>
        <source>[train] 训练进程 10 秒内未退出, 可能有子进程残留占用显存</source>
        <translation>[train] El proceso de entrenamiento no terminó en 10 segundos; puede que queden subprocesos ocupando VRAM</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="122"/>
        <source>训练进程未能完全退出, 可能仍有子进程占用显存.
建议稍等片刻再启动下一个任务.</source>
        <translation>El proceso de entrenamiento no se cerró del todo; puede que aún haya procesos secundarios ocupando VRAM.
Se recomienda esperar un momento antes de iniciar la siguiente tarea.</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="134"/>
        <source>{} 训练中 {}/{}</source>
        <translation>{} entrenando {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="147"/>
        <source>进度 | 当前最好 {}</source>
        <translation>Progreso | {} (mejor hasta ahora)</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="211"/>
        <source>更新训练指标: record={} 已完成epoch={} {}={} 类别数={}</source>
        <translation>Actualizando métricas de entrenamiento: record={} epoch completadas={} {}={} número de clases={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="310"/>
        <source>等待显存释放 · 下一项:{}</source>
        <translation>Esperando liberar VRAM · siguiente:{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="187"/>
        <source>训练失败(队列模式, 已跳过弹窗): {}</source>
        <translation>Entrenamiento fallido (modo cola, diálogo omitido): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="189"/>
        <source>训练失败</source>
        <translation>Entrenamiento fallido</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="190"/>
        <source>训练过程中发生错误, Err:

{}</source>
        <translation>Se produjo un error durante el entrenamiento, Err:

{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="283"/>
        <source>已保存模型记录: {} | {}</source>
        <translation>Registro de modelo guardado: {} | {}</translation>
    </message>
</context>
<context>
    <name>TrainQueueDialog</name>
    <message>
        <location filename="../ui/train_queue.ui" line="14"/>
        <location filename="../ui/train_queue.ui" line="40"/>
        <location filename="../app/widgets/queue_dialog.py" line="33"/>
        <source>训练队列</source>
        <translation>Cola de entrenamiento</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="50"/>
        <location filename="../app/widgets/queue_dialog.py" line="123"/>
        <source>空闲</source>
        <translation>Inactivo</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="93"/>
        <source>#</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="98"/>
        <source>名称</source>
        <translation>Nombre</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="103"/>
        <source>任务</source>
        <translation>Tarea</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="108"/>
        <source>数据集</source>
        <translation>Conjunto de datos</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="113"/>
        <source>型号</source>
        <translation>Modelo</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="118"/>
        <source>轮次</source>
        <translation>Épocas</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="123"/>
        <source>状态</source>
        <translation>Estado</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="152"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="168"/>
        <source>队列为空，可在训练界面点「加入队列」添加任务</source>
        <translation>La cola está vacía; puede añadir tareas con &quot;Añadir a la cola&quot; en la pantalla de entrenamiento</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="199"/>
        <source>上移</source>
        <translation>Subir</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="209"/>
        <source>下移</source>
        <translation>Bajar</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="219"/>
        <location filename="../app/widgets/queue_dialog.py" line="255"/>
        <source>移除</source>
        <translation>Quitar</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="229"/>
        <source>清理已结束</source>
        <translation>Limpiar finalizadas</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="252"/>
        <source>编辑</source>
        <translation>Editar</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="259"/>
        <source>关闭</source>
        <translation>Cerrar</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="272"/>
        <location filename="../app/widgets/queue_dialog.py" line="144"/>
        <source>开始队列</source>
        <translation>Iniciar cola</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="22"/>
        <source>队列为空, 可在训练界面点&quot;加入队列&quot;添加任务</source>
        <translation>La cola está vacía; puede añadir tareas con &quot;Añadir a la cola&quot; en la pantalla de entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>运行中</source>
        <translation>En ejecución</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>队列正在串行执行</source>
        <translation>La cola se ejecuta de forma secuencial</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="115"/>
        <source>待启动</source>
        <translation>Pendiente de inicio</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="116"/>
        <source>有 {} 个任务等待启动</source>
        <translation>{} tareas esperando para iniciarse</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>训练中</source>
        <translation>En entrenamiento</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>当前有训练在进行(非队列启动)</source>
        <translation>Hay un entrenamiento en curso (no iniciado por la cola)</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="120"/>
        <source>已结束</source>
        <translation>Finalizado</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="121"/>
        <source>没有待执行的任务, 点&quot;重新开始队列&quot;可重跑</source>
        <translation>No hay tareas pendientes; haga clic en &quot;Reiniciar cola&quot; para volver a ejecutarlas</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="127"/>
        <source>共 {} 个: 等待 {} · 完成 {} · 失败 {}</source>
        <translation>{} en total: {} en espera · {} completadas · {} fallidas</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="130"/>
        <source>正在训练&quot;{}&quot; · {}</source>
        <translation>Entrenando &quot;{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="133"/>
        <source>下一个: &quot;{}&quot; · {}</source>
        <translation>Siguiente: &quot;{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="146"/>
        <location filename="../app/widgets/queue_dialog.py" line="183"/>
        <source>重新开始队列</source>
        <translation>Reiniciar cola</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="168"/>
        <location filename="../app/widgets/queue_dialog.py" line="190"/>
        <source>队列</source>
        <translation>Cola</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="169"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>Ya hay un entrenamiento en curso; deténgalo primero</translation>
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
        <translation>No hay tareas en espera en la cola.

Para volver a ejecutar: {}

¿Volver a encolarlas e iniciar el entrenamiento?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="191"/>
        <source>队列启动失败, 请查看日志</source>
        <translation>Error al iniciar la cola; consulte el registro</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="207"/>
        <location filename="../app/widgets/queue_dialog.py" line="211"/>
        <source>移除任务</source>
        <translation>Quitar tarea</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="208"/>
        <source>训练中的任务不能移除, 请先停止</source>
        <translation>No se puede quitar una tarea en entrenamiento; deténgala primero</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="212"/>
        <source>确定从队列中移除&quot;{}&quot;吗?</source>
        <translation>¿Quitar &quot;{}&quot; de la cola?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="219"/>
        <source>清理</source>
        <translation>Limpiar</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="220"/>
        <source>没有已结束的任务</source>
        <translation>No hay tareas finalizadas</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="222"/>
        <source>[队列] 已清理 {} 个已结束任务</source>
        <translation>[队列] Se eliminaron {} tareas finalizadas</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="229"/>
        <source>编辑任务</source>
        <translation>Editar tarea</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="230"/>
        <source>训练中的任务不能编辑, 请先停止</source>
        <translation>No se puede editar una tarea en entrenamiento; deténgala primero</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="246"/>
        <source>重新入队</source>
        <translation>Volver a encolar</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="248"/>
        <location filename="../app/widgets/queue_dialog.py" line="269"/>
        <source>打开输出目录</source>
        <translation>Abrir directorio de salida</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="250"/>
        <source>在模型界面查看</source>
        <translation>Ver en la gestión de modelos</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="270"/>
        <source>目录不存在: {}</source>
        <translation>El directorio no existe: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="271"/>
        <source>未设置</source>
        <translation>Sin configurar</translation>
    </message>
</context>
<context>
    <name>TrainRunner</name>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="114"/>
        <source>数据增强需要 kornia 或 albumentations, 当前环境两者都没有.
请把训练参数里的&quot;数据增强&quot;全部取消勾选, 或补装组件后重试</source>
        <translation>El aumento de datos necesita kornia o albumentations, y no hay ninguno instalado.
Desmarca todo en &quot;Aumento de datos&quot; en los ajustes de entrenamiento, o instala uno y reintenta</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="202"/>
        <location filename="../app/train/transformer_train_runner.py" line="131"/>
        <source>输出路径: {}</source>
        <translation>Ruta de salida: {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="203"/>
        <location filename="../app/train/transformer_train_runner.py" line="132"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Directorio de salida de este entrenamiento (marca de tiempo): {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="134"/>
        <source>训练配置文件已保存 → {}</source>
        <translation>Configuración de entrenamiento guardada → {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="156"/>
        <source>分割模型 resolution 已自动取整: {} → {} (block={})</source>
        <translation>resolution del modelo de segmentación redondeado automáticamente: {} → {} (block={})</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="240"/>
        <location filename="../app/train/transformer_train_runner.py" line="158"/>
        <source>使用模型 {} device={} epochs={} batch={} resolution={}</source>
        <translation>Usando el modelo {} device={} epochs={} batch={} resolution={}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="252"/>
        <location filename="../app/train/transformer_train_runner.py" line="169"/>
        <source>数据增强: {}</source>
        <translation>Aumento de datos: {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="255"/>
        <location filename="../app/train/transformer_train_runner.py" line="172"/>
        <source>数据增强: 未启用</source>
        <translation>Aumento: desactivado</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="281"/>
        <location filename="../app/train/transformer_train_runner.py" line="240"/>
        <source>训练完成</source>
        <translation>Entrenamiento completado</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="288"/>
        <location filename="../app/train/transformer_train_runner.py" line="249"/>
        <source>生成类别文件: {}</source>
        <translation>Generando archivo de clases: {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="209"/>
        <location filename="../app/train/transformer_train_runner.py" line="143"/>
        <source>预训练权重缺失: 请先在权重管理里下载 {} 档的模型</source>
        <translation>Faltan los pesos preentrenados: descarga primero el modelo de nivel {} en Pesos del modelo</translation>
    </message>
</context>
<context>
    <name>TrainWorker</name>
    <message>
        <location filename="../app/train/train_worker.py" line="481"/>
        <source>训练监控异常, 已终止.

{}</source>
        <translation>Error en el monitor de entrenamiento; se ha terminado.

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="490"/>
        <source>训练结果文件读取失败: {}

{}</source>
        <translation>Error al leer el archivo de resultados del entrenamiento: {}

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="495"/>
        <source>训练进程异常退出 (code={})

--- 子进程输出(尾部) ---
{}</source>
        <translation>El proceso de entrenamiento terminó de forma anómala (code={})

--- salida del subproceso (final) ---
{}</translation>
    </message>
</context>
<context>
    <name>Utils</name>
    <message>
        <location filename="../app/core/utils.py" line="59"/>
        <location filename="../app/core/utils.py" line="71"/>
        <source>{}秒</source>
        <translation>{} s </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="65"/>
        <source>{}天</source>
        <translation>{} d </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="67"/>
        <source>{}小时</source>
        <translation>{} h </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="69"/>
        <source>{}分</source>
        <translation>{} min </translation>
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
        <translation>Desvincular peso local</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="177"/>
        <source>已就绪</source>
        <translation>Listo</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="184"/>
        <source>未下载</source>
        <translation>Sin descargar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="193"/>
        <source>更换</source>
        <translation>Cambiar</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="201"/>
        <source>本地权重</source>
        <translation>Peso local</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="210"/>
        <source>重选</source>
        <translation>Volver a elegir</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="211"/>
        <source>(路径未记录)</source>
        <translation>(ruta no registrada)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="213"/>
        <source>本地失效</source>
        <translation>Peso local no encontrado</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="215"/>
        <source>登记的本地权重文件已不在这个位置:
{}</source>
        <translation>El archivo de pesos local registrado ya no está en esta ubicación:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="220"/>
        <source>校验中...</source>
        <translation>Verificando...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="239"/>
        <source>失败</source>
        <translation>Fallido</translation>
    </message>
</context>
<context>
    <name>_PixelScaleDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="108"/>
        <source>像素精度</source>
        <translation>Escala de píxel</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="114"/>
        <source>1 像素代表的实际长度</source>
        <translation>Longitud real que representa 1 píxel</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="147"/>
        <source>请输入大于 0 的数字</source>
        <translation>Introduzca un número mayor que 0</translation>
    </message>
</context>
<context>
    <name>_TrainStartDialog</name>
    <message>
        <location filename="../app/train/dialogs.py" line="341"/>
        <source>训练即将开始</source>
        <translation>El entrenamiento está a punto de comenzar</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="351"/>
        <location filename="../app/train/dialogs.py" line="364"/>
        <source>确认({})</source>
        <translation>Aceptar ({})</translation>
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
        <translation>Importar</translation>
    </message>
    <message>
        <location filename="../ui/add_label.ui" line="284"/>
        <source>确定</source>
        <translation>Aceptar</translation>
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
        <translation>Rectángulo</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="35"/>
        <source>多边形</source>
        <translation>Polígono</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="46"/>
        <source>删除图像</source>
        <translation>Eliminar imagen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="70"/>
        <source>设置</source>
        <translation>Ajustes</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="90"/>
        <source>标签列表</source>
        <translation>Etiquetas</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="113"/>
        <source>添加标签</source>
        <translation>Añadir etiqueta</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="116"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="160"/>
        <source>标注信息</source>
        <translation>Anotaciones</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="180"/>
        <source>转换</source>
        <translation>Convertir</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="210"/>
        <source>图像信息</source>
        <translation>Información de la imagen</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="237"/>
        <source>剪切板</source>
        <translation>Portapapeles</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="302"/>
        <source>上一张(A)</source>
        <translation>Anterior (A)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="309"/>
        <source>下一张(D)</source>
        <translation>Siguiente (D)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="359"/>
        <source>标注参数</source>
        <translation>Parámetros de anotación</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="371"/>
        <source>角度范围</source>
        <translation>Rango de ángulo</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="385"/>
        <source>~</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="419"/>
        <source>融合强度</source>
        <translation>Intensidad de mezcla</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="453"/>
        <source>亮度调节</source>
        <translation>Brillo</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="487"/>
        <source>填充颜色</source>
        <translation>Color de relleno</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="494"/>
        <source>点击打开取色器, 选任意颜色</source>
        <translation>Haga clic para abrir el selector de color y elegir cualquiera</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="507"/>
        <source>支持 #RRGGBB / #RGB / 255,255,255 / black / 白 等写法, 也可以点左边色块打开取色器</source>
        <translation>Admite formatos como #RRGGBB / #RGB / 255,255,255 / black / blanco; también puede hacer clic en la muestra de la izquierda para abrir el selector de color</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="510"/>
        <source>#RRGGBB</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="517"/>
        <source>自定义颜色</source>
        <translation>Color personalizado</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="544"/>
        <source>常用色</source>
        <translation>Colores frecuentes</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="575"/>
        <source>恢复默认</source>
        <translation>Restablecer</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="595"/>
        <source>完成</source>
        <translation>Hecho</translation>
    </message>
</context>
</TS>
