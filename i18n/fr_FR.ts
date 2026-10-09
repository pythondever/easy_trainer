<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="fr_FR">
<context>
    <name>AdCommon</name>
    <message>
        <location filename="../app/train/ad_common.py" line="92"/>
        <source>找不到可写的纯英文暂存目录(异常检测的底层库不支持中文路径), 请把输出路径改到纯英文目录下</source>
        <translation>Aucun dossier temporaire inscriptible en ASCII pur trouvé (la bibliothèque de détection d&apos;anomalies ne prend pas en charge les chemins non ASCII) ; changez le chemin de sortie vers un dossier en ASCII pur</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="153"/>
        <location filename="../app/train/ad_common.py" line="655"/>
        <source>(根目录散图)</source>
        <translation>(images éparses à la racine)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="176"/>
        <source>数据集里没找到图像, 请先导入数据</source>
        <translation>Aucune image trouvée dans le jeu de données ; importez d&apos;abord des données</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="181"/>
        <source>无法从类别名判断哪个是正常品, 请把放良品图的那个文件夹改名为 {} 之一; 现有类别: {}</source>
        <translation>Impossible de déterminer la classe des pièces conformes d&apos;après les noms de classes ; renommez le dossier des images conformes en l&apos;un de {} ; classes existantes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="187"/>
        <source>训练集里没有图像</source>
        <translation>Aucune image dans le jeu d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="191"/>
        <source>训练集里只有&quot;{}&quot;一类, 而良品类是&quot;{}&quot;; 请把良品图所在的类别文件夹挂到训练集上</source>
        <translation>Le jeu d&apos;entraînement ne contient que la classe « {} » alors que la classe conforme est « {} » ; rattachez le dossier des images conformes au jeu d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="199"/>
        <source>训练集里既没有&quot;{}&quot;类、又不止一类, 无法确定拿哪批图建库; 现有类别: {}</source>
        <translation>Le jeu d&apos;entraînement n&apos;a pas la classe « {} » et compte plus d&apos;une classe ; impossible de savoir quelles images utiliser pour la banque de mémoire ; classes existantes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="240"/>
        <source>训练集根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>La racine du jeu d&apos;entraînement contient à la fois des images éparses et des sous-dossiers ; impossible de déterminer la classe des images éparses ; placez-les dans un même dossier de classe</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="274"/>
        <source>没有找到任何图像, 请检查数据集</source>
        <translation>Aucune image trouvée ; vérifiez le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="276"/>
        <source>根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>La racine contient à la fois des images éparses et des sous-dossiers ; impossible de déterminer la classe des images éparses ; placez-les dans un même dossier de classe</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="281"/>
        <source>无法判断哪个类别是良品, 现有类别: {}.
请把良品图放在名为 {} 一类的子文件夹里, 或按训练时的方式重新导入数据集</source>
        <translation>Impossible de déterminer quelle classe est conforme ; classes existantes : {}.
Placez les images conformes dans un sous-dossier nommé l&apos;un de {}, ou réimportez le jeu de données comme lors de l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="422"/>
        <source>未知的异常检测算法: {}</source>
        <translation>Algorithme de détection d&apos;anomalies inconnu : {}</translation>
    </message>
</context>
<context>
    <name>AdPackage</name>
    <message>
        <location filename="../app/train/ad_package.py" line="88"/>
        <source>正在复制模型文件...</source>
        <translation>Copie du fichier de modèle...</translation>
    </message>
</context>
<context>
    <name>AdTestRunner</name>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="47"/>
        <source>缺少测试依赖: {}</source>
        <translation>Dépendances de test manquantes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="77"/>
        <source>加载异常检测模型: {}</source>
        <translation>Chargement du modèle de détection d&apos;anomalies : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="86"/>
        <source>算法={} 图像尺寸={} 阈值={:.6f}</source>
        <translation>Algorithme={} taille d&apos;image={} seuil={:.6f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="88"/>
        <source>原尺寸</source>
        <translation>taille d&apos;origine</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="96"/>
        <source>没有可用的图像目录, 请检查数据集</source>
        <translation>Aucun dossier d&apos;images utilisable ; vérifiez le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="107"/>
        <source>测试图片 {} 张, 良品类别: {}</source>
        <translation>{} images de test, classe des bonnes pièces : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="144"/>
        <source>没有取到任何图像, 请检查数据集</source>
        <translation>Aucune image récupérée ; vérifiez le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="151"/>
        <source>沿用训练时定下的阈值 {:.6f}</source>
        <translation>Utilisation du seuil fixé lors de l&apos;entraînement {:.6f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="155"/>
        <source>模型里没有阈值, 本批又只有一类样本, 定不出判定阈值, 只报告分数</source>
        <translation>Le modèle n&apos;a pas de seuil et ce lot ne contient qu&apos;une seule classe ; aucun seuil de décision ne peut être déterminé, seuls les scores sont reportés</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="159"/>
        <source>模型里没有阈值, 已按本批数据现挑 {:.6f}(精度会偏乐观)</source>
        <translation>Le modèle n&apos;a pas de seuil ; {:.6f} a été choisi sur ce lot (la précision sera optimiste)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="189"/>
        <source>完成: {} 张, 没有判定阈值, 只报告分数</source>
        <translation>Terminé : {} images, aucun seuil de décision, seuls les scores sont reportés</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="195"/>
        <source>完成: {} 张, 检出异常 {} 张</source>
        <translation>Terminé : {} images, {} anomalies détectées</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="199"/>
        <source>完成: {} 张, 准确率 {:.4f}, 漏检 {} 张, 误检 {} 张</source>
        <translation>Terminé : {} images, précision {:.4f}, {} manquées, {} faux positifs</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="204"/>
        <source>  image AUROC = {:.4f}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="220"/>
        <source>模型里没有判定阈值, 不输出异常区域</source>
        <translation>Le modèle n&apos;a pas de seuil de décision ; aucune zone d&apos;anomalie écrite</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="223"/>
        <source>异常</source>
        <translation>Anomalie</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="233"/>
        <source>提取异常区域失败 {}: {}</source>
        <translation>Échec de l&apos;extraction de la zone d&apos;anomalie {} : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="250"/>
        <source>输出异常区域失败 {}: {}</source>
        <translation>Échec de l&apos;écriture de la zone d&apos;anomalie {} : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="254"/>
        <source>已为 {} 张不良品图写出异常区域标注(图像同目录)</source>
        <translation>Zones d&apos;anomalie écrites pour {} images défectueuses (à côté des images)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="258"/>
        <source>另有 {} 张判为不良品, 但热力图没超过判定线, 未写标注</source>
        <translation>{} autres images jugées défectueuses, mais leur carte de chaleur n&apos;a pas dépassé la ligne de décision ; aucune annotation écrite</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="277"/>
        <source>图像</source>
        <translation>Image</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="278"/>
        <source>类别</source>
        <translation>Classe</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="279"/>
        <source>真值</source>
        <translation>Vérité terrain</translation>
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
        <translation>Seuil</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="283"/>
        <source>是否正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="298"/>
        <source>是</source>
        <translation>Oui</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="299"/>
        <source>否</source>
        <translation>Non</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="301"/>
        <source>逐图明细: {}</source>
        <translation>Détail par image : {}</translation>
    </message>
</context>
<context>
    <name>AdTrainRunner</name>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="49"/>
        <source>缺少训练依赖: {}</source>
        <translation>Dépendances d&apos;entraînement manquantes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="137"/>
        <source>anomalib {} / torch {}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="170"/>
        <source>输出路径: {}</source>
        <translation>Chemin de sortie : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="172"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Dossier de sortie de cet entraînement (horodatage) : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="186"/>
        <source>异常检测: 算法={} 骨干={} 轮次={} 批次={} 图像尺寸={} device={}</source>
        <translation>Détection d&apos;anomalies : algorithme={} backbone={} époques={} batch={} taille d&apos;image={} device={}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="198"/>
        <source>数据准备: 建库集 {} 张({}), 测试集 正常 {} 张 / 异常 {} 张</source>
        <translation>Données prêtes : banque de mémoire {} images ({}), jeu de test {} bonnes / {} anormales</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="203"/>
        <source>  异常类别: {}</source>
        <translation>  classes anormales : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="204"/>
        <source>(散图)</source>
        <translation>(images isolées)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="209"/>
        <source>  注意: 建库集里另有 {} 张非正常图, 未参与建库</source>
        <translation>  note : la banque de mémoire contient {} images anormales non utilisées</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="213"/>
        <source>建库集里没有图像, 请检查数据集</source>
        <translation>La banque de mémoire ne contient aucune image ; vérifiez le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="215"/>
        <source>测试集里没有图像, 请检查数据集</source>
        <translation>Le jeu de test ne contient aucune image ; vérifiez le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="234"/>
        <source>数据集: 建库集 {} 张</source>
        <translation>Jeu de données : banque de mémoire {} images</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="243"/>
        <source>模型构建完成({:.1f}s): {}</source>
        <translation>Modèle construit en {:.1f}s : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="261"/>
        <source>建库/训练完成({:.1f}s)</source>
        <translation>Banque/entraînement terminé ({:.1f}s)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="274"/>
        <source>  评估中: {} 张</source>
        <translation>  évaluation en cours : {} images</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="283"/>
        <source>评估阶段失败, 只交付模型: {}</source>
        <translation>Échec de l&apos;évaluation ; seul le modèle est livré : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="288"/>
        <source>评估完成({:.1f}s): {} 张</source>
        <translation>Évaluation terminée ({:.1f}s) : {} images</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="291"/>
        <source>  测试集里只有一类样本, 定不出判定阈值(没有真值反差), AUROC 和准确率都算不了; 补一些异常样本重新训练才有交付阈值</source>
        <translation>  le jeu de test ne contient qu&apos;une seule classe ; aucun seuil de décision ne peut être déterminé (pas de contraste dans la vérité terrain) et ni l&apos;AUROC ni la précision ne peuvent être calculés ; réentraînez avec des échantillons anormaux pour obtenir un seuil livrable</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="296"/>
        <source>评估完成({:.1f}s): {} 张, 准确率 {:.4f}</source>
        <translation>Évaluation terminée ({:.1f}s) : {} images, précision {:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="300"/>
        <source>  image AUROC = {:.4f}  阈值 = {:.6f}(本批最优 F1 处)</source>
        <translation>  image AUROC = {:.4f}  seuil = {:.6f} (meilleur F1 sur ce lot)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="303"/>
        <source>  漏检 {} 张(不良判成良品), 误检 {} 张</source>
        <translation>  {} manquées (défectueuse jugée bonne), {} faux positifs</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="307"/>
        <source>  AUROC 无法计算</source>
        <translation>  AUROC ne peut pas être calculé</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="321"/>
        <source>模型已保存: {} ({:.0f} MB)</source>
        <translation>Modèle enregistré : {} ({:.0f} Mo)</translation>
    </message>
</context>
<context>
    <name>AddLabelDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="168"/>
        <source>添加标签</source>
        <translation>Ajouter une étiquette</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="185"/>
        <source>编辑标签</source>
        <translation>Modifier l&apos;étiquette</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="187"/>
        <source>标签名称</source>
        <translation>Nom de l&apos;étiquette</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="222"/>
        <source>标签名称, 多个用逗号分隔</source>
        <translation>Noms des étiquettes, séparés par des virgules</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="224"/>
        <source>导入</source>
        <translation>Importer</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="231"/>
        <source>选择数据集...</source>
        <translation>Sélectionner un jeu de données...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="254"/>
        <location filename="../app/annotation/annotation_dialog.py" line="259"/>
        <source>导入标签</source>
        <translation>Importer les étiquettes</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="255"/>
        <source>请先选择一个数据集</source>
        <translation>Sélectionnez d&apos;abord un jeu de données</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="260"/>
        <source>数据集&quot;{}&quot;还没有标签</source>
        <translation>Le jeu de données « {} » n&apos;a pas encore d&apos;étiquette</translation>
    </message>
</context>
<context>
    <name>AnnotationDialog</name>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="208"/>
        <source>复制</source>
        <translation>Copier</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="210"/>
        <source>填充</source>
        <translation>Remplir</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="220"/>
        <source>粘贴</source>
        <translation>Coller</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="374"/>
        <source>标注 - {} / {}</source>
        <translation>Annotation - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="392"/>
        <location filename="../app/annotation/annotation_dialog.py" line="874"/>
        <source>矩形</source>
        <translation>Rectangle</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="393"/>
        <location filename="../app/annotation/annotation_dialog.py" line="880"/>
        <source>多边形</source>
        <translation>Polygone</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="402"/>
        <source>标签列表</source>
        <translation>Étiquettes</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="403"/>
        <source>标注信息</source>
        <translation>Annotations</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="407"/>
        <source>上一张</source>
        <translation>Précédent</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="408"/>
        <source>下一张</source>
        <translation>Suivant</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="443"/>
        <source>只在选中的多边形框内生效; A/D 切图或 Ctrl+S 才写盘</source>
        <translation>S&apos;applique uniquement dans le polygone sélectionné ; écriture sur disque au changement d&apos;image (A/D) ou via Ctrl+S</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="481"/>
        <source>显示标注</source>
        <translation>Afficher les annotations</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="487"/>
        <source>文本标注</source>
        <translation>Annotation de texte</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="713"/>
        <source>编辑标签</source>
        <translation>Modifier l&apos;étiquette</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1032"/>
        <source>转换</source>
        <translation>Convertir</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1033"/>
        <source>设置像素精度, 在像素面积后显示物理面积</source>
        <translation>Définir l&apos;échelle de pixel pour afficher l&apos;aire physique après l&apos;aire en pixels</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1037"/>
        <source>当前像素精度 {}, 点击修改</source>
        <translation>Échelle de pixel actuelle {}, cliquer pour modifier</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="563"/>
        <source>先在画布上点选一个多边形</source>
        <translation>Sélectionnez d&apos;abord un polygone sur le canevas</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="566"/>
        <source>亮度调节只对多边形有效</source>
        <translation>Le réglage de luminosité ne s&apos;applique qu&apos;aux polygones</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="326"/>
        <source>    类别: {}</source>
        <translation>    Classe : {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="354"/>
        <source>删除本地文件</source>
        <translation>Supprimer le fichier local</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="355"/>
        <source>取消</source>
        <translation>Annuler</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="357"/>
        <location filename="../app/annotation/annotation_io.py" line="366"/>
        <source>删除图像</source>
        <translation>Supprimer l&apos;image</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="358"/>
        <source>是否删除当前图像?

{}</source>
        <translation>Supprimer l&apos;image actuelle ?

{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="361"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>L&apos;image et son fichier d&apos;annotation seront supprimés du disque. Action irréversible</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="367"/>
        <source>无法访问主窗口, 删除失败</source>
        <translation>Fenêtre principale inaccessible, échec de la suppression</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="380"/>
        <source>(无图像)</source>
        <translation>(aucune image)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="696"/>
        <location filename="../app/annotation/annotation_dialog.py" line="820"/>
        <location filename="../app/annotation/annotation_dialog.py" line="826"/>
        <source>添加标签</source>
        <translation>Ajouter une étiquette</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="697"/>
        <source>请先添加标签(点击&quot;+&quot;)</source>
        <translation>Ajoutez d&apos;abord une étiquette (cliquez sur « + »)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="733"/>
        <source>标注文字</source>
        <translation>Texte de l&apos;annotation</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="734"/>
        <source>请输入框内的文字</source>
        <translation>Saisissez le texte de la zone</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="846"/>
        <source>剪切板  {}/{}</source>
        <translation>Presse-papiers  {}/{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="871"/>
        <source>第 {} 个模板  {}x{}
左键选中用于粘贴, 右键 删除/导入/导出/清空</source>
        <translation>Modèle {}  {}x{}
Clic gauche pour sélectionner en vue du collage ; clic droit pour supprimer / importer / exporter / vider</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="903"/>
        <location filename="../app/annotation/annotation_dialog.py" line="685"/>
        <source>删除</source>
        <translation>Supprimer</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="906"/>
        <source>导入</source>
        <translation>Importer</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="907"/>
        <source>导出</source>
        <translation>Exporter</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="909"/>
        <source>清空</source>
        <translation>Vider</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="420"/>
        <location filename="../app/annotation/annotation_io.py" line="449"/>
        <location filename="../app/annotation/annotation_io.py" line="454"/>
        <source>导出剪切板</source>
        <translation>Exporter le presse-papiers</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="421"/>
        <source>剪切板是空的, 没有可导出的模板</source>
        <translation>Le presse-papiers est vide, aucun modèle à exporter</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="424"/>
        <source>选择导出目录</source>
        <translation>Sélectionner le dossier d&apos;export</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="450"/>
        <source>导出中断: {}
(已写出 {} 个)</source>
        <translation>Export interrompu : {}
({} écrit(s))</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="455"/>
        <source>已导出 {} 个模板(png + 同名 json)到:
{}</source>
        <translation>{} modèle(s) exporté(s) (png + json du même nom) vers :
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="461"/>
        <source>选择导入目录</source>
        <translation>Sélectionner le dossier d&apos;import</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="468"/>
        <location filename="../app/annotation/annotation_io.py" line="472"/>
        <location filename="../app/annotation/annotation_io.py" line="506"/>
        <source>导入剪切板</source>
        <translation>Importer le presse-papiers</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="469"/>
        <source>读取目录失败: {}</source>
        <translation>Échec de la lecture du dossier : {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="473"/>
        <source>这个目录里没有 png 文件</source>
        <translation>Aucun fichier png dans ce dossier</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="501"/>
        <source>已导入 {} 个模板到剪切板</source>
        <translation>{} modèle(s) importé(s) dans le presse-papiers</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="503"/>
        <source>
其中 {} 个没有同名 json, 按矩形导入</source>
        <translation>
Dont {} sans json du même nom, importés comme rectangles</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="505"/>
        <source>
{} 个文件读不出来, 已跳过</source>
        <translation>
{} fichier(s) illisible(s), ignoré(s)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="622"/>
        <source>修改类别</source>
        <translation>Modifier la classe</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="623"/>
        <source>移动图像文件失败:
{}</source>
        <translation>Échec du déplacement du fichier image :
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="684"/>
        <source>编辑</source>
        <translation>Modifier</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="780"/>
        <location filename="../app/annotation/annotation_dialog.py" line="787"/>
        <location filename="../app/annotation/annotation_io.py" line="524"/>
        <source>删除标签</source>
        <translation>Supprimer l&apos;étiquette</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="525"/>
        <source>正在统计标注文件...</source>
        <translation>Comptage des fichiers d&apos;annotation...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="781"/>
        <source>标签&quot;{}&quot;已有 {} 处标注, 删除后这些标注将被一并删除且不可恢复.
确定删除吗?</source>
        <translation>L&apos;étiquette « {} » compte {} annotation(s). Elles seront toutes supprimées et ne pourront pas être récupérées.
Confirmer la suppression ?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="788"/>
        <source>确定删除标签&quot;{}&quot;吗?</source>
        <translation>Supprimer l&apos;étiquette « {} » ?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="714"/>
        <location filename="../app/annotation/annotation_dialog.py" line="821"/>
        <source>标签名称不能为空</source>
        <translation>Le nom de l&apos;étiquette ne peut pas être vide</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="881"/>
        <source>{} 个顶点</source>
        <translation>{} sommets</translation>
    </message>
</context>
<context>
    <name>App</name>
    <message>
        <location filename="../app/main_window.py" line="55"/>
        <source>软件启动</source>
        <translation>Démarrage du logiciel</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="58"/>
        <source>软件退出</source>
        <translation>Fermeture du logiciel</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="60"/>
        <source>软件退出前停止训练</source>
        <translation>Arrêt de l&apos;entraînement avant fermeture du logiciel</translation>
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
        <translation>Projets</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="193"/>
        <source>添加项目</source>
        <translation>Ajouter un projet</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="196"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="335"/>
        <source>项目训练中</source>
        <translation>Entraînement en cours</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="365"/>
        <source>停止训练</source>
        <translation>Arrêter l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="372"/>
        <source>剩余时间:</source>
        <translation>Temps restant :</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="382"/>
        <source>显存:</source>
        <translation>VRAM :</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="389"/>
        <source>20%</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="399"/>
        <source>统计</source>
        <translation>Statistiques</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="406"/>
        <source>训练</source>
        <translation>Entraîner</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="413"/>
        <source>模型</source>
        <translation>Modèles</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="420"/>
        <location filename="../app/mixins/queue_mixin.py" line="368"/>
        <source>队列</source>
        <translation>File d&apos;attente</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="427"/>
        <source>日志</source>
        <translation>Journal</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="446"/>
        <source>界面语言</source>
        <translation>Langue de l&apos;interface</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="537"/>
        <source>上一页</source>
        <translation>Précédent</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="566"/>
        <source>下一页</source>
        <translation>Suivant</translation>
    </message>
</context>
<context>
    <name>Charts</name>
    <message>
        <location filename="../app/widgets/charts.py" line="12"/>
        <source>暂无标注</source>
        <translation>Aucune annotation</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="13"/>
        <source>标签</source>
        <translation>Étiquette</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="14"/>
        <source>标签数量</source>
        <translation>Nombre d&apos;étiquettes</translation>
    </message>
</context>
<context>
    <name>ClassifyTestRunner</name>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="33"/>
        <source>缺少测试依赖: {}</source>
        <translation>Dépendances de test manquantes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="85"/>
        <source>加载分类模型: {}</source>
        <translation>Chargement du modèle de classification : {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="110"/>
        <source>测试图片 {} 张</source>
        <translation>{} images de test</translation>
    </message>
</context>
<context>
    <name>ClassifyTrainRunner</name>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="40"/>
        <source>缺少训练依赖: {}</source>
        <translation>Dépendances d&apos;entraînement manquantes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="132"/>
        <source>输出路径: {}</source>
        <translation>Chemin de sortie : {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="133"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Dossier de sortie de cet entraînement (horodatage) : {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="149"/>
        <source>分类训练: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</source>
        <translation>Entraînement de classification : model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="158"/>
        <source>数据准备: train={} 张, val={} 张</source>
        <translation>Préparation des données : train={} images, val={} images</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="160"/>
        <source>训练集无图像, 请检查数据集</source>
        <translation>Aucune image dans le jeu d&apos;entraînement, vérifiez le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="162"/>
        <source>验证集无图像, 请检查数据集</source>
        <translation>Aucune image dans le jeu de validation, vérifiez le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="187"/>
        <source>未从数据集中解析到任何类别(子文件夹),无法训练图像分类</source>
        <translation>Aucune classe extraite du jeu de données (sous-dossiers), impossible d&apos;entraîner la classification d&apos;images</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="197"/>
        <source>数据集: train={} val={} 类别({})={}</source>
        <translation>Jeu de données : train={} val={} classes({})={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="284"/>
        <source>早停触发: 连续 {} 个 epoch 精度无提升</source>
        <translation>Arrêt anticipé déclenché : précision sans amélioration pendant {} époques consécutives</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="289"/>
        <source>训练完成 best_acc={:.4f}</source>
        <translation>Entraînement terminé best_acc={:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="297"/>
        <source>生成类别文件: {}</source>
        <translation>Génération du fichier de classes : {}</translation>
    </message>
</context>
<context>
    <name>CollapsibleText</name>
    <message>
        <location filename="../app/widgets/collapsible_text.py" line="57"/>
        <source>点击展开 / 收起完整内容</source>
        <translation>Cliquer pour déplier / replier</translation>
    </message>
</context>
<context>
    <name>ColorPickerDialog</name>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="395"/>
        <source>选择颜色</source>
        <translation>Choisir une couleur</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="407"/>
        <source>十六进制:</source>
        <translation>Hexadécimal :</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="428"/>
        <source>基本颜色:</source>
        <translation>Couleurs de base :</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="440"/>
        <source>自定义 RGB:</source>
        <translation>RGB personnalisé :</translation>
    </message>
</context>
<context>
    <name>CompareDialog</name>
    <message>
        <location filename="../ui/compare.ui" line="14"/>
        <source>对比多次训练</source>
        <translation>Comparer les entraînements</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="22"/>
        <source>对比指标</source>
        <translation>Comparer la métrique</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="38"/>
        <source>记录范围</source>
        <translation>Plage d&apos;enregistrements</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="65"/>
        <location filename="../app/widgets/compare_dialog.py" line="695"/>
        <location filename="../app/widgets/compare_dialog.py" line="699"/>
        <location filename="../app/widgets/compare_dialog.py" line="716"/>
        <source>导出对比报告</source>
        <translation>Exporter le rapport comparatif</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="72"/>
        <location filename="../app/widgets/compare_dialog.py" line="723"/>
        <location filename="../app/widgets/compare_dialog.py" line="727"/>
        <source>删除选中</source>
        <translation>Supprimer la sélection</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="97"/>
        <source>训练记录（可勾选，上限 8 条）</source>
        <translation>Entraînements (cochables, 8 max)</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="168"/>
        <source>关键指标汇总</source>
        <translation>Résumé des métriques clés</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="188"/>
        <source>差异与结论</source>
        <translation>Différences et conclusion</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="320"/>
        <source>勾选要对比的训练记录(最多 {} 条), 双击查看单次指标</source>
        <translation>Cochez les entraînements à comparer (max. {}); double-cliquez pour voir les métriques d&apos;un seul</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="295"/>
        <source>数据来源：LMDB train_history + metrics.csv / metrics json</source>
        <translation>Source des données : LMDB train_history + metrics.csv / metrics json</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="516"/>
        <source>一次最多对比 {} 条记录</source>
        <translation>On peut comparer au plus {} enregistrements à la fois</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="544"/>
        <source>{} 训练曲线（按 epoch）</source>
        <translation>Courbe d&apos;entraînement {} (par époque)</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="551"/>
        <source>已选 {} 条（上限 {}）</source>
        <translation>{} sélectionnés (max {})</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="553"/>
        <source>已选 {} 条(上限 {}), 双击左侧记录可查看单次指标</source>
        <translation>{} sélectionnés (limite {}); double-cliquez sur un enregistrement à gauche pour voir ses métriques</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="555"/>
        <location filename="../app/widgets/compare_dialog.py" line="581"/>
        <source>勾选左侧的训练记录后这里显示对比曲线</source>
        <translation>Cochez des enregistrements à gauche pour afficher ici leurs courbes comparées</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="649"/>
        <source>无</source>
        <translation>Aucun</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="662"/>
        <source>至少勾选 2 条记录&lt;br&gt;才能比较差异</source>
        <translation>Cochez au moins 2 enregistrements&lt;br&gt;pour comparer les différences</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="696"/>
        <source>当前没有可导出的对比图表</source>
        <translation>Aucun graphique comparable à exporter</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="700"/>
        <source>PNG 图片 (*.png)</source>
        <translation>Image PNG (*.png)</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="714"/>
        <source>已导出: {}
{}</source>
        <translation>Exporté : {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="717"/>
        <source>导出失败: {}</source>
        <translation>Échec de l&apos;export : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="724"/>
        <source>请先勾选要删除的训练记录</source>
        <translation>Cochez d&apos;abord les enregistrements à supprimer</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="728"/>
        <source>确定删除选中的 {} 条训练记录? 对应指标文件会一并删除.</source>
        <translation>Supprimer les {} enregistrements d&apos;entraînement sélectionnés ? Leurs fichiers de métriques seront aussi supprimés.</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="585"/>
        <source>所选记录没有&quot;{}&quot;的数据</source>
        <translation>Les enregistrements sélectionnés n&apos;ont pas de données &quot;{}&quot;</translation>
    </message>
</context>
<context>
    <name>DataPrep</name>
    <message>
        <location filename="../app/train/data_prep.py" line="189"/>
        <source>解析到类别 {} 个: {}</source>
        <translation>{} classes extraites : {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="209"/>
        <source>复制数据集 {}: 图像 {} 张, 标签 {} 个 → {}</source>
        <translation>Copie du jeu de données {} : {} images, {} étiquettes → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="296"/>
        <source>合并 {} 数据集 → {} ({} 个文件)</source>
        <translation>Fusion de {} jeux de données → {} ({} fichiers)</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="313"/>
        <source>生成 data.yaml → {}</source>
        <translation>Génération de data.yaml → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="326"/>
        <source>未从数据集中解析到任何标签类别, 请检查标签文件</source>
        <translation>Aucune classe d&apos;étiquette extraite du jeu de données ; vérifiez les fichiers d&apos;étiquettes</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="333"/>
        <source>数据准备完成: {} 个类别, 输出目录 {}</source>
        <translation>Préparation des données terminée : {} classes, dossier de sortie {}</translation>
    </message>
</context>
<context>
    <name>DatasetViewMixin</name>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="261"/>
        <source>删除全部未标注图像({} 张)</source>
        <translation>Supprimer toutes les images non étiquetées ({} images)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="267"/>
        <source>删除所选图像({} 张)</source>
        <translation>Supprimer les images sélectionnées ({} images)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="381"/>
        <source>重载跳过: 数据集 {}/{} 无图像目录</source>
        <translation>Rechargement ignoré : le jeu de données {}/{} n&apos;a pas de dossier d&apos;images</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="382"/>
        <source>重载</source>
        <translation>Recharger</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="383"/>
        <source>该数据集还没有图像目录, 请先右键&quot;导入&quot;</source>
        <translation>Ce jeu de données n&apos;a pas encore de dossier d&apos;images ; faites d&apos;abord un clic droit sur « Importer »</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="387"/>
        <source>重载跳过: 数据集 {}/{} 正在载入</source>
        <translation>Rechargement ignoré : le jeu de données {}/{} est en cours de chargement</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="389"/>
        <source>重载数据集: {}/{}</source>
        <translation>Rechargement du jeu de données : {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="598"/>
        <source>数据集 {}/{} 含 OCR 文本标注, 已标为字符检测数据集</source>
        <translation>Le jeu de données {}/{} contient des annotations de texte OCR, marqué comme jeu de détection de texte</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="880"/>
        <source>第 {} / {} 页</source>
        <translation>Page {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="884"/>
        <source>第 {}/{} 页 · 共 {} 个</source>
        <translation>Page {}/{} · {} éléments</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="886"/>
        <source>第 {}/{} 页 · 共 {} 张</source>
        <translation>Page {}/{} · {} images</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="899"/>
        <source>未选择标签</source>
        <translation>Aucune étiquette sélectionnée</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="901"/>
        <source>暂无数据</source>
        <translation>Aucune donnée</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="938"/>
        <source>开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}</source>
        <translation>Début de l&apos;import : {}/{} | Chemin des images={} | Chemin des étiquettes={} | Format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="939"/>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1008"/>
        <source>(无)</source>
        <translation>(aucun)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1003"/>
        <source>{}: {}个</source>
        <translation>{} : {} boîtes</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1005"/>
        <source>数据集导入完成: {}/{} | 图像 {} 张, 已标注 {} 张 | 标签({}类): {}</source>
        <translation>Import du jeu de données terminé : {}/{} | {} images, {} étiquetées | Étiquettes ({} classes) : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1050"/>
        <source>数据集 {}/{} 未导入, 右键&quot;导入&quot;选择图像与标签目录</source>
        <translation>Jeu de données {}/{} non importé ; clic droit sur « Importer » pour choisir les dossiers d&apos;images et d&apos;étiquettes</translation>
    </message>
</context>
<context>
    <name>Dialog</name>
    <message>
        <location filename="../ui/dataset_properties.ui" line="14"/>
        <source>数据集属性</source>
        <translation>Propriétés du jeu de données</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="30"/>
        <source>选择数据:</source>
        <translation>Sélectionner le jeu de données :</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="53"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="77"/>
        <source>图像路径:</source>
        <translation>Chemin des images :</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="98"/>
        <source>标签路径:</source>
        <translation>Chemin des étiquettes :</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="119"/>
        <source>标签分布:</source>
        <translation>Répartition des étiquettes :</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="14"/>
        <source>导出</source>
        <translation>Exporter</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="36"/>
        <source>请选择导出路径</source>
        <translation>Sélectionnez un chemin d&apos;export</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="90"/>
        <source>导出格式</source>
        <translation>Format d&apos;export</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="106"/>
        <source>labelme 格式</source>
        <translation>format labelme</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="119"/>
        <source>yolo 格式</source>
        <translation>format yolo</translation>
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
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../app/widgets/dialog_buttons.py" line="116"/>
        <source>取消</source>
        <translation>Annuler</translation>
    </message>
</context>
<context>
    <name>DiffPanel</name>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="107"/>
        <source>最佳记录</source>
        <translation>Meilleur enregistrement</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="108"/>
        <source>按 {}</source>
        <translation>selon {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="126"/>
        <source>参数差异</source>
        <translation>Différences de paramètres</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="126"/>
        <source>仅列取值不同的项</source>
        <translation>Seules les valeurs différentes</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="135"/>
        <source>所选记录参数完全一致</source>
        <translation>Les enregistrements sélectionnés ont des paramètres identiques</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="144"/>
        <source>共同</source>
        <translation>Commun</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="174"/>
        <source>结论</source>
        <translation>Conclusion</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="189"/>
        <source>最佳</source>
        <translation>Meilleur</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="199"/>
        <source>它独有的设置</source>
        <translation>propre à celui-ci</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="203"/>
        <source>启用增强 {}/{} 条</source>
        <translation>Augmentation activée sur {}/{} :</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="206"/>
        <source>所选记录都没有启用数据增强</source>
        <translation>Aucun enregistrement n&apos;a activé l&apos;augmentation de données</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="211"/>
        <source>仍在训练</source>
        <translation>entraînement en cours</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="213"/>
        <source>曲线未收敛， 对比仅供参考</source>
        <translation>courbe non convergée， à titre indicatif</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="218"/>
        <source>未跑完</source>
        <translation>non terminé</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="218"/>
        <source>不参与最佳判定</source>
        <translation>exclu du meilleur</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="221"/>
        <source>训练时长</source>
        <translation>Durée d&apos;entraînement</translation>
    </message>
</context>
<context>
    <name>ImportData</name>
    <message>
        <location filename="../ui/import_data.ui" line="14"/>
        <source>导入数据</source>
        <translation>Importer des données</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="33"/>
        <source>图像路径</source>
        <translation>Chemin des images</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="73"/>
        <source>标签路径</source>
        <translation>Chemin des étiquettes</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="107"/>
        <source>标签格式:</source>
        <translation>Format des étiquettes :</translation>
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
        <translation>Importer comme classification (sous-dossiers)</translation>
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
        <translation>Importer des données - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="66"/>
        <location filename="../app/mixins/import_export_mixin.py" line="166"/>
        <source>请选择图像文件夹</source>
        <translation>Choisissez un dossier d&apos;images</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="142"/>
        <source>请选择分类根目录(子文件夹名=类别)</source>
        <translation>Choisissez le dossier racine de classification (nom du sous-dossier = classe)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="155"/>
        <source>(根目录)</source>
        <translation>(dossier racine)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="157"/>
        <source>所选文件夹下无分类子文件夹或图像</source>
        <translation>Aucun sous-dossier de classe ni image dans le dossier sélectionné</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="159"/>
        <source>{}: {}张</source>
        <translation>{} : {} images</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="161"/>
        <source>检测到 {} 类: {}</source>
        <translation>{} classes détectées : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="80"/>
        <source>所选文件夹无图像</source>
        <translation>Aucune image dans le dossier sélectionné</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="83"/>
        <source>共 {} 张图像, 已标注 {} 张</source>
        <translation>{} images, dont {} étiquetées</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="99"/>
        <source>(检测到 {} 张 {} 标签, 请切换上方格式为&quot;{}&quot;)</source>
        <translation>({} étiquette(s) {} détectée(s) ; changez le format ci-dessus en « {} »)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="103"/>
        <source>共 {} 张图像, 已标注 0 张 {}</source>
        <translation>{} images, 0 étiquetée {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="105"/>
        <source>共 {} 张图像(标签目录无匹配文件)</source>
        <translation>{} images (aucun fichier correspondant dans le dossier d&apos;étiquettes)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="172"/>
        <source>选择文件夹</source>
        <translation>Sélectionner un dossier</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="212"/>
        <source>分类根目录(子文件夹名=类别)</source>
        <translation>Dossier racine de classification (nom du sous-dossier = classe)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="212"/>
        <source>图像路径</source>
        <translation>Chemin des images</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="234"/>
        <location filename="../app/mixins/import_export_mixin.py" line="237"/>
        <source>导入数据</source>
        <translation>Importer des données</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="234"/>
        <source>请先选择有效的图像文件夹</source>
        <translation>Choisissez d&apos;abord un dossier d&apos;images valide</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="237"/>
        <source>标签路径无效</source>
        <translation>Chemin des étiquettes invalide</translation>
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
        <translation>Exporter</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="298"/>
        <source>请先在左侧选中要导出的数据集</source>
        <translation>Sélectionnez d&apos;abord à gauche le jeu de données à exporter</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="311"/>
        <source>打开</source>
        <translation>Ouvrir</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="322"/>
        <source>请先选择导出保存位置</source>
        <translation>Choisissez d&apos;abord où enregistrer l&apos;export</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="333"/>
        <source>开始导出: 项目={} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>Début de l&apos;export : projet={} | chemin source={} | chemin d&apos;enregistrement={} | format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="339"/>
        <source>正在导出项目...</source>
        <translation>Exportation du projet...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="350"/>
        <source>项目&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>Projet « {} » exporté : {} images copiées
Emplacement : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="352"/>
        <source>导出项目完成: {} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>Export du projet terminé : {} | {} images | étiquettes ({}) | format={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="358"/>
        <source>开始导出: 数据集={}/{} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>Début de l&apos;export : jeu de données={}/{} | chemin source={} | chemin d&apos;enregistrement={} | format={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="362"/>
        <source>正在导出数据集...</source>
        <translation>Exportation du jeu de données...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="372"/>
        <source>数据集&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>Jeu de données « {} » exporté : {} images copiées
Emplacement : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="375"/>
        <source>导出数据集完成: {}/{} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>Export du jeu de données terminé : {}/{} | {} images | étiquettes ({}) | format={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="380"/>
        <source>导出失败: 项目={} 数据集={} | {}</source>
        <translation>Échec de l&apos;export : projet={} jeu de données={} | {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="381"/>
        <source>(整个项目)</source>
        <translation>(projet entier)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="382"/>
        <source>导出失败</source>
        <translation>Échec de l&apos;export</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="385"/>
        <source>选择导出保存位置</source>
        <translation>Sélectionner la destination de l&apos;export</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="411"/>
        <source>{} =&gt; 标签:{}</source>
        <translation>{} =&gt; étiquettes : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="412"/>
        <location filename="../app/mixins/import_export_mixin.py" line="413"/>
        <source>(无)</source>
        <translation>(aucun)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="420"/>
        <source>(无标签)</source>
        <translation>(aucune étiquette)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="463"/>
        <source>正在导出: {}</source>
        <translation>Exportation : {}</translation>
    </message>
</context>
<context>
    <name>ImportTask</name>
    <message>
        <location filename="../app/tasks/import_task.py" line="109"/>
        <source>导入跳过 {}: {}</source>
        <translation>Import ignoré {} : {}</translation>
    </message>
</context>
<context>
    <name>LabelFilter</name>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="60"/>
        <location filename="../app/widgets/label_filter_popup.py" line="451"/>
        <source>全选</source>
        <translation>Tout sélectionner</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="464"/>
        <source>显示全部图像</source>
        <translation>Sans filtre</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="466"/>
        <source>按所选标签过滤</source>
        <translation>Filtre par étiquette</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="468"/>
        <source>未选择标签</source>
        <translation>Aucun choix</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="533"/>
        <source>收起</source>
        <translation>Réduire</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="534"/>
        <source>展开全部</source>
        <translation>Tout afficher</translation>
    </message>
</context>
<context>
    <name>LabelMixin</name>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="88"/>
        <source>已选 {} 个</source>
        <translation>{} sélectionnées</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="89"/>
        <source>全选</source>
        <translation>Tout sélectionner</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="91"/>
        <location filename="../app/mixins/label_mixin.py" line="108"/>
        <source>未选择标签</source>
        <translation>Aucun choix</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="100"/>
        <location filename="../app/mixins/label_mixin.py" line="175"/>
        <source>未标注</source>
        <translation>Non étiqueté</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="208"/>
        <source>重命名</source>
        <translation>Renommer</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="214"/>
        <source>合并标签</source>
        <translation>Fusionner les étiquettes</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="215"/>
        <source>标签&quot;{}&quot;已存在.
确定把&quot;{}&quot;的所有标注合并到&quot;{}&quot;吗?
此操作会改写数据集源标签文件, 且不可恢复.</source>
        <translation>L&apos;étiquette « {} » existe déjà.
Fusionner toutes les annotations de « {} » dans « {} » ?
Cette opération réécrit les fichiers d&apos;étiquettes source du jeu de données et est irréversible.</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="270"/>
        <source>合并标签: {} → {} ({}/{}) | 启动后台文件合并, 完成后输出统计</source>
        <translation>Fusion des étiquettes : {} → {} ({}/{}) | fusion des fichiers lancée en arrière-plan, statistiques affichées à la fin</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="273"/>
        <source>重命名标签: {} → {} ({}/{})</source>
        <translation>Renommage de l&apos;étiquette : {} → {} ({}/{})</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="349"/>
        <source>{}: {}个</source>
        <translation>{} : {} boîtes</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="352"/>
        <source>删除标签完成: {} | 修改 {} 个标签文件 | 删除后标签统计({}类): {}</source>
        <translation>Suppression d&apos;étiquette terminée : {} | {} fichiers d&apos;étiquettes modifiés | statistiques après suppression ({} classes) : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="355"/>
        <location filename="../app/mixins/label_mixin.py" line="360"/>
        <location filename="../app/mixins/label_mixin.py" line="365"/>
        <source>(无)</source>
        <translation>(aucun)</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="357"/>
        <source>合并标签: {} → {} | 修改 {} 个标签文件 | 合并后标签统计({}类): {}</source>
        <translation>Fusion des étiquettes : {} → {} | {} fichiers d&apos;étiquettes modifiés | statistiques après fusion ({} classes) : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="362"/>
        <source>合并标签: {} → {} | 无标签文件被修改 | 合并后标签统计({}类): {}</source>
        <translation>Fusion des étiquettes : {} → {} | aucun fichier d&apos;étiquettes modifié | statistiques après fusion ({} classes) : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="456"/>
        <source>删除标签: {} ({}/{})</source>
        <translation>Supprimer l&apos;étiquette : {} ({}/{})</translation>
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
        <translation>Vider</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="79"/>
        <location filename="../app/widgets/log_dialog.py" line="21"/>
        <source>日志</source>
        <translation>Journal</translation>
    </message>
</context>
<context>
    <name>MessageBox</name>
    <message>
        <location filename="../app/widgets/message_box.py" line="274"/>
        <location filename="../app/widgets/message_box.py" line="302"/>
        <source>确定</source>
        <translation>OK</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="98"/>
        <source>详情已复制到剪贴板</source>
        <translation>Détails copiés dans le presse-papiers</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="267"/>
        <source>关闭</source>
        <translation>Fermer</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="269"/>
        <source>复制详情</source>
        <translation>Copier les détails</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="303"/>
        <location filename="../app/widgets/message_box.py" line="350"/>
        <source>取消</source>
        <translation>Annuler</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="374"/>
        <source>取消中...</source>
        <translation>Annulation...</translation>
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
        <translation>Précision</translation>
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
        <location filename="../app/widgets/metric_tabs.py" line="90"/>
        <source>所选记录都没有 {} 的数据</source>
        <translation>Aucun des enregistrements sélectionnés n&apos;a de données {}</translation>
    </message>
</context>
<context>
    <name>MetricsDialog</name>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="55"/>
        <source>训练指标</source>
        <translation>Métriques d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="84"/>
        <source>标签筛选</source>
        <translation>Filtre d&apos;étiquettes</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="88"/>
        <source>全部指标</source>
        <translation>Toutes les métriques</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="89"/>
        <source>全部标签-P</source>
        <translation>Toutes les étiquettes - P</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="90"/>
        <source>全部标签-R</source>
        <translation>Toutes les étiquettes - R</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="126"/>
        <source>暂无该标签的指标数据(训练完成后可查看)</source>
        <translation>Aucune donnée de métrique pour cette étiquette (disponible une fois l&apos;entraînement terminé)</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="174"/>
        <source>loss 值</source>
        <translation>Valeur de perte</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="175"/>
        <source>指标值 (mAP/P/R)</source>
        <translation>Métrique (mAP/P/R)</translation>
    </message>
</context>
<context>
    <name>MiscMixin</name>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="54"/>
        <source>界面语言: {}</source>
        <translation>Langue de l&apos;interface : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="115"/>
        <source>数据集统计</source>
        <translation>Statistiques du jeu de données</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="124"/>
        <source>应用所选数据集</source>
        <translation>Appliquer les jeux de données sélectionnés</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="215"/>
        <source>[{}/{}](未设置)</source>
        <translation>[{}/{}](non défini)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="218"/>
        <source>(未选择数据集)</source>
        <translation>(aucun jeu de données sélectionné)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="338"/>
        <source>删除图像: {} 张 | 本地删除文件={} | 项目={}, 数据集={}</source>
        <translation>Suppression d&apos;images : {} | suppression des fichiers locaux={} | projet={}, jeu de données={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="376"/>
        <source>删除</source>
        <translation>Supprimer</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="377"/>
        <source>取消</source>
        <translation>Annuler</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="379"/>
        <source>删除图像</source>
        <translation>Supprimer les images</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="380"/>
        <source>将从系统删除所选 {} 张图像?

(图像与同名标注文件不可恢复)</source>
        <translation>Supprimer du système les {} image(s) sélectionnée(s) ?

(les images et leurs fichiers d&apos;annotation ne pourront pas être récupérés)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="384"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>Les images et leurs fichiers d&apos;annotation seront supprimés du disque. Action irréversible</translation>
    </message>
</context>
<context>
    <name>ModelAssets</name>
    <message>
        <location filename="../app/core/model_assets.py" line="88"/>
        <location filename="../app/core/model_assets.py" line="122"/>
        <source>速度最快, 精度够用</source>
        <translation>Le plus rapide, précision suffisante</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="89"/>
        <location filename="../app/core/model_assets.py" line="126"/>
        <source>精度更好, 稍慢一些</source>
        <translation>Meilleure précision, un peu plus lent</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="90"/>
        <location filename="../app/core/model_assets.py" line="130"/>
        <source>精度更高</source>
        <translation>Précision supérieure</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="91"/>
        <source>精度最高, 显存占用大</source>
        <translation>Précision maximale, mais consomme plus de VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="92"/>
        <source>精度极致, 显存占用很大</source>
        <translation>Précision extrême, mais consomme beaucoup plus de VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="95"/>
        <location filename="../app/core/model_assets.py" line="141"/>
        <source>轻量分割</source>
        <translation>Segmentation légère</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="96"/>
        <location filename="../app/core/model_assets.py" line="145"/>
        <source>速度与精度平衡</source>
        <translation>Équilibre entre vitesse et précision</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="97"/>
        <location filename="../app/core/model_assets.py" line="149"/>
        <source>细节更完整</source>
        <translation>Détails plus complets</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="98"/>
        <location filename="../app/core/model_assets.py" line="153"/>
        <source>最精细</source>
        <translation>Le plus fin</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="99"/>
        <source>最精细, 显存占用很大</source>
        <translation>Le plus fin, mais consomme beaucoup plus de VRAM</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="137"/>
        <source>结构与 medium 相同</source>
        <translation>Même architecture que medium</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="295"/>
        <source>文件不存在: {}</source>
        <translation>Fichier introuvable : {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="298"/>
        <source>只支持 {} 格式</source>
        <translation>Seul le format {} est pris en charge</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="303"/>
        <source>读不到文件大小: {}</source>
        <translation>Taille du fichier illisible : {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="305"/>
        <source>文件只有 {}, 不像完整的权重</source>
        <translation>Le fichier ne fait que {}, il ne semble pas s&apos;agir d&apos;un poids complet</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="316"/>
        <source>这看着是 Transformer 权重, 当前档位是 CNN(YOLO)</source>
        <translation>Cela ressemble à un poids Transformer, mais l&apos;emplacement choisi est CNN (YOLO)</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="320"/>
        <source>这看着是 CNN(YOLO) 权重, 当前档位是 Transformer</source>
        <translation>Cela ressemble à un poids CNN (YOLO), mais l&apos;emplacement choisi est Transformer</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="340"/>
        <source>权重目录不可写: {}</source>
        <translation>Dossier des poids non accessible en écriture : {}</translation>
    </message>
</context>
<context>
    <name>ModelDialog</name>
    <message>
        <location filename="../ui/model.ui" line="14"/>
        <location filename="../app/widgets/model_dialog.py" line="190"/>
        <source>模型管理</source>
        <translation>Gestionnaire de modèles</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="28"/>
        <source>搜索项目 / 数据集 / 标签</source>
        <translation>Rechercher un projet / jeu de données / étiquette</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="39"/>
        <source>全部任务</source>
        <translation>Toutes les tâches</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="44"/>
        <source>检测</source>
        <translation>Détection</translation>
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
        <translation>Tous les états</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="71"/>
        <source>已完成</source>
        <translation>Terminé</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="76"/>
        <source>训练中</source>
        <translation>Entraînement</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="81"/>
        <source>失败</source>
        <translation>Échec</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="86"/>
        <source>已停止</source>
        <translation>Arrêté</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="94"/>
        <source>仅看每个数据集最佳</source>
        <translation>Meilleur par jeu de données uniquement</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="114"/>
        <source>共 0 条</source>
        <translation>0 enregistrement</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="135"/>
        <location filename="../app/widgets/model_dialog.py" line="629"/>
        <source>任务</source>
        <translation>Tâche</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="140"/>
        <source>数据集 / 标签</source>
        <translation>Jeu de données / Étiquettes</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="145"/>
        <location filename="../app/widgets/model_dialog.py" line="633"/>
        <source>精度</source>
        <translation>Précision</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="150"/>
        <location filename="../app/widgets/model_dialog.py" line="644"/>
        <source>训练时间</source>
        <translation>Date d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="155"/>
        <location filename="../app/widgets/model_dialog.py" line="646"/>
        <source>耗时</source>
        <translation>Durée</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="160"/>
        <location filename="../app/widgets/model_dialog.py" line="636"/>
        <source>图像尺寸</source>
        <translation>Taille d&apos;image</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="165"/>
        <source>操作</source>
        <translation>Actions</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="184"/>
        <source>模型详情</source>
        <translation>Détails du modèle</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="191"/>
        <location filename="../app/widgets/model_dialog.py" line="612"/>
        <source>选中一行查看详情</source>
        <translation>Sélectionnez une ligne pour voir les détails</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="220"/>
        <source>查看完整指标</source>
        <translation>Voir toutes les métriques</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="227"/>
        <location filename="../app/widgets/model_dialog.py" line="756"/>
        <source>对比多次训练</source>
        <translation>Comparer les entraînements</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="234"/>
        <source>按此配置重训</source>
        <translation>Réentraîner avec cette configuration</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="241"/>
        <source>打开模型目录</source>
        <translation>Ouvrir le dossier du modèle</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="281"/>
        <source>上一页</source>
        <translation>Précédent</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="288"/>
        <source>1/1</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="295"/>
        <source>下一页</source>
        <translation>Suivant</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="436"/>
        <source>共 {} 条</source>
        <translation>{} enregistrements</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="487"/>
        <source> 等 {} 类</source>
        <translation> et {} autres classes</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="502"/>
        <source>测试</source>
        <translation>Tester</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="507"/>
        <source>导出</source>
        <translation>Exporter</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="512"/>
        <source>删除</source>
        <translation>Supprimer</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="626"/>
        <source>{} × {} 累积</source>
        <translation>{} × {} cumulés</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="627"/>
        <source>状态</source>
        <translation>État</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="634"/>
        <source>训练集</source>
        <translation>Jeu d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="635"/>
        <source>验证集</source>
        <translation>Jeu de validation</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="637"/>
        <source>轮数 / 早停</source>
        <translation>Époques / Arrêt anticipé</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="639"/>
        <source>批大小</source>
        <translation>Taille de lot</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="640"/>
        <source>学习率</source>
        <translation>Taux d&apos;apprentissage</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="641"/>
        <source>优化器</source>
        <translation>Optimiseur</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="642"/>
        <source>设备</source>
        <translation>Appareil</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="643"/>
        <source>标签</source>
        <translation>Étiquettes</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="647"/>
        <source>模型路径</source>
        <translation>Chemin du modèle</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="663"/>
        <source>失败原因</source>
        <translation>Cause de l&apos;échec</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="679"/>
        <source>暂无曲线</source>
        <translation>Aucune courbe</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="703"/>
        <source>{}  最佳 {:.3f}</source>
        <translation>{}  meilleur {:.3f}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="711"/>
        <location filename="../app/widgets/model_dialog.py" line="722"/>
        <source>打开目录</source>
        <translation>Ouvrir le dossier</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="712"/>
        <source>模型目录不存在:
{}</source>
        <translation>Le dossier du modèle n&apos;existe pas :
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="740"/>
        <source>[model_dialog] 打开指标失败: {}
{}</source>
        <translation>[model_dialog] Échec de l&apos;ouverture des métriques : {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="742"/>
        <source>查看指标失败</source>
        <translation>Échec de l&apos;ouverture des métriques</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="757"/>
        <source>当前没有可对比的训练记录</source>
        <translation>Aucun entraînement à comparer</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="764"/>
        <source>[model_dialog] 打开对比失败: {}
{}</source>
        <translation>[model_dialog] Échec de l&apos;ouverture de la comparaison: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="766"/>
        <source>打开对比失败</source>
        <translation>Échec de l&apos;ouverture de la comparaison</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="773"/>
        <source>删除模型记录</source>
        <translation>Supprimer l&apos;enregistrement du modèle</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="774"/>
        <source>确定删除该条模型记录?
项目={}
数据集={}
开始时间={}
</source>
        <translation>Supprimer cet enregistrement de modèle ?
Projet={}
Jeu de données={}
Heure de début={}
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="778"/>
        <source>删除模型记录: 项目={} 数据集={} 任务={} 开始时间={}</source>
        <translation>Suppression de l&apos;enregistrement de modèle : projet={} jeu de données={} tâche={} heure de début={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="792"/>
        <source>删除模型记录失败: {} | {}</source>
        <translation>Échec de la suppression de l&apos;enregistrement de modèle : {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="793"/>
        <source>[model_dialog] 删除失败: {}
{}</source>
        <translation>[model_dialog] Échec de la suppression : {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="802"/>
        <source>[model_dialog] 打开训练失败: {}
{}</source>
        <translation>[model_dialog] Échec de l&apos;ouverture de l&apos;entraînement : {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="803"/>
        <source>打开训练失败</source>
        <translation>Échec de l&apos;ouverture de l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="828"/>
        <source>[model_dialog] 打开测试失败: {}
{}</source>
        <translation>[model_dialog] Échec de l&apos;ouverture du test : {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="830"/>
        <source>打开测试失败</source>
        <translation>Échec de l&apos;ouverture du test</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="848"/>
        <location filename="../app/widgets/model_dialog.py" line="866"/>
        <location filename="../app/widgets/model_dialog.py" line="882"/>
        <location filename="../app/widgets/model_dialog.py" line="1173"/>
        <location filename="../app/widgets/model_dialog.py" line="1183"/>
        <source>导出模型</source>
        <translation>Exporter le modèle</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="849"/>
        <source>模型文件不存在:
{}</source>
        <translation>Le fichier du modèle n&apos;existe pas :
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="850"/>
        <source>导出模型失败: 模型文件不存在 {}</source>
        <translation>Échec de l&apos;export du modèle : fichier du modèle introuvable {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="852"/>
        <source>选择导出目录</source>
        <translation>Sélectionner le dossier d&apos;export</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="867"/>
        <source>创建目录失败: {}</source>
        <translation>Échec de la création du dossier : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="868"/>
        <source>导出模型失败: 创建目录失败 {} | {}</source>
        <translation>Échec de l&apos;export du modèle : échec de la création du dossier {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="878"/>
        <source>开始导出模型: 项目={} 任务={} 架构={} 尺寸={} | {}</source>
        <translation>Début de l&apos;export du modèle : projet={} tâche={} architecture={} taille={} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="879"/>
        <location filename="../app/widgets/model_dialog.py" line="1033"/>
        <source>未知</source>
        <translation>Inconnu</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="883"/>
        <source>正在导出 ONNX...</source>
        <translation>Exportation ONNX...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="904"/>
        <source>正在导出模型包...</source>
        <translation>Exportation du paquet de modèle...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="915"/>
        <source>导出模型包完成: 包含 {}</source>
        <translation>Export du paquet de modèle terminé : contient : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="922"/>
        <source>ONNX 导出完成: {} ({:.1f} MB)</source>
        <translation>Export ONNX terminé : {} ({:.1f} Mo)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="979"/>
        <source>读取词表失败: {}</source>
        <translation>Échec de lecture du vocabulaire : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="990"/>
        <source>生成 vocab.txt 失败: {}</source>
        <translation>Échec de génération de vocab.txt : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1006"/>
        <source>生成 label_map.json 失败: {}</source>
        <translation>Échec de la génération de label_map.json : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1012"/>
        <source>导出模型报告跳过: 分类任务不出评估报告</source>
        <translation>Export du rapport du modèle ignoré : les tâches de classification ne génèrent pas de rapport d&apos;évaluation</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1013"/>
        <source>分类任务不生成评估报告</source>
        <translation>Les tâches de classification ne génèrent pas de rapport d&apos;évaluation</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1017"/>
        <source>导出模型报告跳过: 字符识别不出评估报告</source>
        <translation>Export du rapport de modèle ignoré : la reconnaissance de texte ne produit pas de rapport d&apos;évaluation</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1018"/>
        <source>字符识别不生成评估报告</source>
        <translation>La reconnaissance de texte ne produit pas de rapport d&apos;évaluation</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1022"/>
        <source>导出模型报告跳过: 未找到验证集</source>
        <translation>Export du rapport du modèle ignoré : aucun jeu de validation trouvé</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1023"/>
        <source>未找到验证集, 已跳过评估报告</source>
        <translation>Aucun jeu de validation trouvé, rapport d&apos;évaluation ignoré</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1025"/>
        <location filename="../app/widgets/model_dialog.py" line="1106"/>
        <source>正在生成模型报告...</source>
        <translation>Génération du rapport du modèle...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1029"/>
        <source>正在生成模型报告 {}/{}</source>
        <translation>Génération du rapport du modèle {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1032"/>
        <source>导出模型评估失败: {}</source>
        <translation>Échec de l&apos;évaluation du modèle à l&apos;export : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1035"/>
        <source>评估失败, 已跳过报告: {}</source>
        <translation>Échec de l&apos;évaluation, rapport ignoré : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1125"/>
        <source>导出模型报告跳过: 验证集没有标注</source>
        <translation>Export du rapport du modèle ignoré : le jeu de validation n&apos;a pas d&apos;annotations</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1126"/>
        <source>验证集没有标注, 已跳过评估报告</source>
        <translation>Jeu de validation sans annotations, rapport d&apos;évaluation ignoré</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1132"/>
        <source>[export] 生成评估报告失败:
{}</source>
        <translation>[export] Échec de la génération du rapport d&apos;évaluation :
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1129"/>
        <source>生成评估报告失败: {}</source>
        <translation>Échec de la génération du rapport d&apos;évaluation : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="964"/>
        <source>读取类别表失败: {}</source>
        <translation>Échec de la lecture de la liste des classes : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="965"/>
        <source>[export] 读取类别表失败: {}</source>
        <translation>[export] Échec de la lecture de la liste des classes : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1121"/>
        <source>导出模型报告完成: {}</source>
        <translation>Export du rapport du modèle terminé : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1133"/>
        <source>评估完成, 但报告生成失败</source>
        <translation>Évaluation terminée, mais la génération du rapport a échoué</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1167"/>
        <source>导出模型完成: {} | 包含: {}</source>
        <translation>Export du modèle terminé : {} | contient : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1169"/>
        <source>已导出到:
{}

包含: {}</source>
        <translation>Exporté vers :
{}

Contient : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1131"/>
        <location filename="../app/widgets/model_dialog.py" line="1180"/>
        <source>未知错误</source>
        <translation>Erreur inconnue</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1184"/>
        <source>模型导出失败, 详情见日志</source>
        <translation>Échec de l&apos;exportation du modèle, voir le journal</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1179"/>
        <source>导出模型失败: {}</source>
        <translation>Échec de l&apos;export du modèle : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1181"/>
        <source>[export] ONNX 导出失败: {}</source>
        <translation>[export] Échec de l&apos;export ONNX : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1198"/>
        <source>复制导出示例失败: {}</source>
        <translation>Échec de la copie de l&apos;exemple d&apos;export : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1199"/>
        <source>[export] 复制示例失败: {}</source>
        <translation>[export] Échec de la copie de l&apos;exemple : {}</translation>
    </message>
</context>
<context>
    <name>ModelDownloader</name>
    <message>
        <location filename="../app/core/model_download.py" line="92"/>
        <source>权重目录不可写入, 请点&quot;更改&quot;换一个目录</source>
        <translation>Le dossier des poids n&apos;est pas accessible en écriture ; cliquez sur « Modifier » pour en choisir un autre</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="101"/>
        <source>权重文件大小不符, 丢弃重下: {}</source>
        <translation>Taille du fichier de poids incorrecte, fichier abandonné et re-téléchargé : {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="111"/>
        <source>开始下载权重 {} ({}, 已下载 {})</source>
        <translation>Début du téléchargement des poids {} ({}, déjà téléchargé {})</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="118"/>
        <source>下载权重失败 {}: {}</source>
        <translation>Échec du téléchargement des poids {} : {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="121"/>
        <source>无法连接下载服务器, 请检查网络后重试</source>
        <translation>Impossible de se connecter au serveur de téléchargement, vérifiez le réseau puis réessayez</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="129"/>
        <source>下载中断, 已保留进度, 可再次点击续传</source>
        <translation>Téléchargement interrompu, progression conservée ; cliquez à nouveau pour reprendre</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="134"/>
        <source>下载不完整, 已保留进度, 可再次点击续传</source>
        <translation>Téléchargement incomplet, progression conservée ; cliquez à nouveau pour reprendre</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="141"/>
        <source>权重校验不通过 {}: 期望 {} 实际 {}</source>
        <translation>Vérification des poids échouée {} : attendu {} obtenu {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="146"/>
        <source>文件校验未通过, 损坏文件已删除, 请重试</source>
        <translation>Vérification du fichier échouée, fichier corrompu supprimé, veuillez réessayer</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="152"/>
        <source>写入权重目录失败, 请检查磁盘空间</source>
        <translation>Échec de l&apos;écriture dans le dossier des poids, vérifiez l&apos;espace disque</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="155"/>
        <source>权重就绪: {}</source>
        <translation>Poids prêts : {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="176"/>
        <source>下载已取消, 已下载部分保留以便续传: {}</source>
        <translation>Téléchargement annulé, la partie déjà téléchargée est conservée pour la reprise : {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="196"/>
        <source>权重下载异常 {}: {!r}</source>
        <translation>Erreur de téléchargement des poids {} : {!r}</translation>
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
        <translation>Poids du modèle</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="63"/>
        <source>目标检测 · Transformer</source>
        <translation>Détection d&apos;objets · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="97"/>
        <source>目标检测 · CNN</source>
        <translation>Détection d&apos;objets · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="131"/>
        <source>图像分割 · Transformer</source>
        <translation>Segmentation d&apos;images · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="165"/>
        <source>图像分割 · CNN</source>
        <translation>Segmentation d&apos;images · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="221"/>
        <source>下载目录</source>
        <translation>Dossier de téléchargement</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="238"/>
        <source>更改</source>
        <translation>Modifier</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="265"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="293"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="498"/>
        <source>开始下载</source>
        <translation>Démarrer le téléchargement</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="275"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="280"/>
        <source>关闭</source>
        <translation>Fermer</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="58"/>
        <source>还剩 {}s</source>
        <translation>{} s restantes</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="59"/>
        <source>还剩 {}m{}s</source>
        <translation>{} min {} s restantes</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="387"/>
        <source>选择权重目录</source>
        <translation>Sélectionner le dossier des poids</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="405"/>
        <source>选择预训练权重</source>
        <translation>Sélectionner les poids pré-entraînés</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="406"/>
        <source>权重文件 (*.pt *.pth *.ckpt)</source>
        <translation>Fichiers de poids (*.pt *.pth *.ckpt)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="416"/>
        <source>仍要用这个文件吗?</source>
        <translation>Utiliser ce fichier quand même ?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="444"/>
        <source>权重目录不可写入 {}: {!r}</source>
        <translation>Dossier des poids non accessible en écriture {} : {!r}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="455"/>
        <source>勾选的模型都已就绪, 不需要下载.</source>
        <translation>Tous les modèles cochés sont prêts, aucun téléchargement nécessaire.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="460"/>
        <source>当前目录不可写入, 请点&quot;更改&quot;换一个目录:
{}</source>
        <translation>Le dossier actuel n&apos;est pas accessible en écriture. Cliquez sur « Modifier » pour en choisir un autre :
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="293"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="465"/>
        <source>下载中...</source>
        <translation>Téléchargement...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="511"/>
        <source>以下权重没能下载完成:
</source>
        <translation>Ces poids n&apos;ont pas pu être téléchargés :
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="518"/>
        <source>下载还在进行, 现在关闭会中断下载(已下载部分保留, 下次可续传).
确定关闭?</source>
        <translation>Un téléchargement est toujours en cours. Fermer maintenant l&apos;interrompra (les parties déjà téléchargées sont conservées et la reprise se fera au prochain lancement).
Fermer quand même ?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="550"/>
        <source>去下载</source>
        <translation>Télécharger</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="559"/>
        <source>该架构的权重必须先下载好才能开始训练, 也可以在权重管理里指定本地的权重文件.</source>
        <translation>Les poids de cette architecture doivent être téléchargés avant de lancer l&apos;entraînement. Vous pouvez aussi indiquer un fichier de poids local dans Poids du modèle.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="553"/>
        <source>本次训练选用 {} {}模型, 需要先下载 {}.</source>
        <translation>Cet entraînement utilise le modèle {} {} et nécessite de télécharger {} au préalable.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="552"/>
        <source>缺少模型权重</source>
        <translation>Poids du modèle manquants</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="365"/>
        <source>待下载 {}</source>
        <translation>À télécharger : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="367"/>
        <source>无需下载</source>
        <translation>Aucun téléchargement nécessaire</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="369"/>
        <source>本地 {} 项</source>
        <translation>Locaux : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="551"/>
        <source>取消</source>
        <translation>Annuler</translation>
    </message>
</context>
<context>
    <name>MultiCombo</name>
    <message>
        <location filename="../app/widgets/multi_combo.py" line="350"/>
        <source>请选择数据集</source>
        <translation>Sélectionner les jeux de données</translation>
    </message>
</context>
<context>
    <name>NameInputDialog</name>
    <message>
        <location filename="../ui/input_name.ui" line="14"/>
        <location filename="../ui/input_name.ui" line="40"/>
        <location filename="../app/widgets/name_input_dialog.py" line="13"/>
        <source>输入名称</source>
        <translation>Saisir un nom</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="65"/>
        <location filename="../app/widgets/name_input_dialog.py" line="14"/>
        <source>请输入名称</source>
        <translation>Saisissez un nom</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="100"/>
        <source>取消</source>
        <translation>Annuler</translation>
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
        <translation>Le nom ne peut pas être vide</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="27"/>
        <source>名称过长, 最多 {} 个字符</source>
        <translation>Le nom est trop long, {} caractères au maximum</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="41"/>
        <source>名称不能包含「{}」等字符</source>
        <translation>Le nom ne peut pas contenir de caractères tels que {}</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="54"/>
        <source>「{}」是系统保留名称, 请换一个</source>
        <translation>« {} » est un nom réservé, veuillez en choisir un autre</translation>
    </message>
</context>
<context>
    <name>OcrTestRunner</name>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="46"/>
        <source>缺少测试依赖: {}</source>
        <translation>Dépendances de test manquantes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="187"/>
        <source>识别失败: {}</source>
        <translation>Échec de la reconnaissance : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="274"/>
        <source>明细写入失败: {}</source>
        <translation>Échec de l&apos;écriture des détails : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="282"/>
        <source>未知的字符检测架构: {}</source>
        <translation>Architecture de détection de texte inconnue : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="296"/>
        <source>已加载配对识别模型: {}</source>
        <translation>Modèle de reconnaissance associé chargé : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="300"/>
        <source>识别模型不可用, 输出的标注只有框没有文字</source>
        <translation>Modèle de reconnaissance indisponible ; les annotations produites n&apos;ont que des zones, sans texte</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="306"/>
        <location filename="../app/train/ocr_test_runner.py" line="425"/>
        <source>没有可用的图像, 请检查数据集</source>
        <translation>Aucune image utilisable ; vérifiez le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="307"/>
        <source>加载字符检测模型: {}</source>
        <translation>Chargement du modèle de détection de texte : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="309"/>
        <location filename="../app/train/ocr_test_runner.py" line="429"/>
        <source>测试图片 {} 张</source>
        <translation>{} images de test</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="342"/>
        <source>预测失败 {}: {}</source>
        <translation>Échec de la prédiction {} : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="372"/>
        <source>输出标注失败 {}: {}</source>
        <translation>Échec de l&apos;écriture des annotations {} : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="400"/>
        <source>已写出 {} 张图的文本标注(图像同目录)</source>
        <translation>Annotations de texte écrites pour {} images (à côté de l&apos;image)</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="411"/>
        <source>未知的字符识别架构: {}</source>
        <translation>Architecture de reconnaissance de texte inconnue : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="415"/>
        <source>该模型没有词表, 无法识别</source>
        <translation>Ce modèle n&apos;a pas de vocabulaire ; reconnaissance impossible</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="426"/>
        <source>加载字符识别模型: {} 词表 {} 个字符</source>
        <translation>Chargement du modèle de reconnaissance de texte : {} vocabulaire de {} caractères</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="457"/>
        <source>识别失败 {}: {}</source>
        <translation>Échec de la reconnaissance {} : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="464"/>
        <source>没有取到任何字条: 该数据集没有文本标注, 识别段只能拿标注框裁图来测</source>
        <translation>Aucun extrait de texte obtenu : ce jeu de données n&apos;a pas d&apos;annotations de texte, l&apos;étape de reconnaissance ne peut être testée qu&apos;en découpant les zones annotées</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="470"/>
        <source>WARN {} 张图没有文本标注, 已跳过</source>
        <translation>WARN {} images sans annotation de texte, ignorées</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="473"/>
        <source>字条 {} 条, CER={:.4f}, 全对 {} 条</source>
        <translation>{} extraits de texte, CER={:.4f}, {} entièrement corrects</translation>
    </message>
</context>
<context>
    <name>OcrTrainRunner</name>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="42"/>
        <source>缺少训练依赖: {}</source>
        <translation>Dépendances d&apos;entraînement manquantes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="118"/>
        <source>检测模型 {} 权重来源: {}</source>
        <translation>Modèle de détection {} : poids issus de {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="122"/>
        <source>检测模型 {} 构建失败</source>
        <translation>Échec de construction du modèle de détection {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="138"/>
        <source>识别模型 {} 权重来源: {}</source>
        <translation>Modèle de reconnaissance {} : poids issus de {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="142"/>
        <source>识别模型 {} 构建失败</source>
        <translation>Échec de construction du modèle de reconnaissance {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="174"/>
        <source>标注里没有任何文字, 无法训练字符识别</source>
        <translation>Aucun texte dans les annotations ; impossible d&apos;entraîner la reconnaissance de texte</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="182"/>
        <source>词表 {} 个字符</source>
        <translation>Vocabulaire : {} caractères</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="195"/>
        <source>字符{}训练: model={} device={} epochs={} batch={} lr={}</source>
        <translation>Entraînement {} : model={} device={} epochs={} batch={} lr={}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="198"/>
        <source>识别</source>
        <translation>reconnaissance</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="199"/>
        <source>检测</source>
        <translation>Détection</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="202"/>
        <source>训练集没有可用的文本标注</source>
        <translation>Aucune annotation de texte utilisable dans le jeu d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="205"/>
        <source>验证集没有可用的文本标注</source>
        <translation>Aucune annotation de texte utilisable dans le jeu de validation</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="207"/>
        <source>数据集: train={} val={}</source>
        <translation>Jeu de données : train={} val={}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="293"/>
        <source>早停触发: 连续 {} 个 epoch 无提升</source>
        <translation>Arrêt anticipé déclenché : aucune amélioration sur {} epoch consécutifs</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="322"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Répertoire de sortie de cet entraînement (horodatage) : {}</translation>
    </message>
</context>
<context>
    <name>OnnxExport</name>
    <message>
        <location filename="../app/train/onnx_export.py" line="112"/>
        <source>该识别模型没有词表, 无法导出</source>
        <translation>Ce modèle de reconnaissance n&apos;a pas de vocabulaire ; export impossible</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="121"/>
        <source>未知的字符模型架构: {}</source>
        <translation>Architecture de modèle de texte inconnue : {}</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="133"/>
        <source>识别</source>
        <translation>reconnaissance</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="134"/>
        <source>检测</source>
        <translation>Détection</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="152"/>
        <source>异常检测不导出 ONNX, 请用模型管理的「导出」生成模型包</source>
        <translation>La détection d&apos;anomalies n&apos;exporte pas en ONNX. Utilisez « Exporter » dans la gestion des modèles pour créer le paquet</translation>
    </message>
</context>
<context>
    <name>ProjectMixin</name>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="32"/>
        <source>输入名称</source>
        <translation>Saisir un nom</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="33"/>
        <source>项目名称</source>
        <translation>Nom du projet</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="37"/>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <source>创建项目</source>
        <translation>Créer un projet</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <location filename="../app/mixins/project_mixin.py" line="53"/>
        <source>项目名称已存在!</source>
        <translation>Ce nom de projet existe déjà !</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="44"/>
        <source>创建项目: {}</source>
        <translation>Création du projet : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="49"/>
        <location filename="../app/mixins/project_mixin.py" line="53"/>
        <location filename="../app/mixins/project_mixin.py" line="106"/>
        <source>修改名称</source>
        <translation>Renommer</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="56"/>
        <source>重命名项目: {} → {}</source>
        <translation>Renommage du projet : {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="61"/>
        <location filename="../app/mixins/project_mixin.py" line="107"/>
        <source>删除项目</source>
        <translation>Supprimer le projet</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="62"/>
        <source>确定删除项目&quot;{}&quot;吗?
</source>
        <translation>Supprimer le projet « {} » ?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="63"/>
        <source>删除项目: {}</source>
        <translation>Suppression du projet : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="103"/>
        <location filename="../app/mixins/project_mixin.py" line="147"/>
        <location filename="../app/mixins/project_mixin.py" line="156"/>
        <source>添加数据集</source>
        <translation>Ajouter un jeu de données</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="105"/>
        <source>导出项目</source>
        <translation>Exporter le projet</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="122"/>
        <source>导入</source>
        <translation>Importer</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="123"/>
        <source>导出</source>
        <translation>Exporter</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="124"/>
        <source>重载</source>
        <translation>Recharger</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="125"/>
        <source>移动</source>
        <translation>Déplacer</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="126"/>
        <source>修改</source>
        <translation>Renommer</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="127"/>
        <source>删除</source>
        <translation>Supprimer</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="148"/>
        <source>数据集名称</source>
        <translation>Nom du jeu de données</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="156"/>
        <location filename="../app/mixins/project_mixin.py" line="167"/>
        <source>该项目下已存在同名数据集!</source>
        <translation>Un jeu de données portant ce nom existe déjà dans ce projet !</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="158"/>
        <source>创建数据集: {}/{}</source>
        <translation>Création du jeu de données : {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="163"/>
        <location filename="../app/mixins/project_mixin.py" line="167"/>
        <source>修改数据集</source>
        <translation>Renommer le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="169"/>
        <source>重命名数据集: {} → {}</source>
        <translation>Renommage du jeu de données : {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="174"/>
        <source>删除数据集</source>
        <translation>Supprimer le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="175"/>
        <source>确定删除数据集&quot;{}&quot;吗?
</source>
        <translation>Supprimer le jeu de données « {} » ?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="179"/>
        <source>删除数据集: {}/{}</source>
        <translation>Suppression du jeu de données : {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="198"/>
        <location filename="../app/mixins/project_mixin.py" line="211"/>
        <location filename="../app/mixins/project_mixin.py" line="228"/>
        <source>移动数据集</source>
        <translation>Déplacer le jeu de données</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="199"/>
        <source>是否将&quot;{}&quot;的数据从
{} / {} 移动到 {} / {}?
移动后源数据集将清空.</source>
        <translation>Déplacer les données de « {} » de
{} / {} vers {} / {} ?
Le jeu de données source sera vidé.</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="208"/>
        <source>移动失败</source>
        <translation>Échec du déplacement</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="212"/>
        <source>已从 {} / {} 移动到 {} / {}</source>
        <translation>Déplacé de {} / {} vers {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="229"/>
        <source>没有可移动到的目标数据集(本项目之外无数据集)</source>
        <translation>Aucun jeu de données cible disponible (aucun jeu de données hors de ce projet)</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="233"/>
        <source>选择目标数据集</source>
        <translation>Sélectionner le jeu de données cible</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="237"/>
        <source>选择要将数据移动到的目标数据集:</source>
        <translation>Sélectionnez le jeu de données cible vers lequel déplacer les données :</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="318"/>
        <source>{}: {}个</source>
        <translation>{} : {} boîtes</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="320"/>
        <source>数据集移动: {}/{} → {}/{} | 移动图像 {} 张 | 目标标签统计({}类): {}</source>
        <translation>Déplacement du jeu de données : {}/{} → {}/{} | {} images déplacées | statistiques des étiquettes de destination ({} classes) : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="323"/>
        <source>(无)</source>
        <translation>(aucun)</translation>
    </message>
</context>
<context>
    <name>ProjectSidebar</name>
    <message>
        <location filename="../app/widgets/project_sidebar.py" line="424"/>
        <source>{} 个项目 · {} 个数据集</source>
        <translation>{} projets · {} jeux de données</translation>
    </message>
</context>
<context>
    <name>QueueMixin</name>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="97"/>
        <source>训练队列已启动</source>
        <translation>File d&apos;attente d&apos;entraînement démarrée</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="107"/>
        <source>[队列] 已停止</source>
        <translation>[队列] Arrêté</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="195"/>
        <source>[队列] 所有任务已执行完毕</source>
        <translation>[队列] Toutes les tâches sont terminées</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="203"/>
        <source>[队列] 跳过任务 {}: {}</source>
        <translation>[队列] Tâche ignorée {} : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="204"/>
        <source>队列任务启动失败 {}: {}</source>
        <translation>Échec du démarrage de la tâche de la file d&apos;attente {} : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="224"/>
        <source>[队列] 缺少权重 {}, 该项训练会失败</source>
        <translation>[队列] Poids manquants {} ; cet entraînement échouera</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="227"/>
        <source>[队列] 缺少权重 {}, 该项训练时会自行下载</source>
        <translation>[队列] Poids manquants {} ; ils seront téléchargés pendant l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="240"/>
        <source>已有训练在进行中</source>
        <translation>Un entraînement est déjà en cours</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="245"/>
        <source>[队列] 开始队列第 {}/{} 项: {}</source>
        <translation>[队列] Démarrage de l&apos;élément {}/{} de la file d&apos;attente : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="249"/>
        <source>队列启动任务: {} record={}</source>
        <translation>File d&apos;attente, lancement de la tâche : {} record={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="287"/>
        <source>训练未完成, 详见日志</source>
        <translation>Entraînement non terminé, voir le journal</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="321"/>
        <source>[队列] 显存等待超时, 仍继续启动下一个任务</source>
        <translation>[队列] Délai d&apos;attente de la VRAM dépassé, lancement de la tâche suivante malgré tout</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="367"/>
        <source>队列 {}</source>
        <translation>File d&apos;attente {}</translation>
    </message>
</context>
<context>
    <name>ResponsiveMixin</name>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="19"/>
        <location filename="../app/mixins/responsive_mixin.py" line="40"/>
        <source>更多</source>
        <translation>Plus</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="43"/>
        <location filename="../app/mixins/responsive_mixin.py" line="52"/>
        <source>界面字号</source>
        <translation>Taille de police de l&apos;interface</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="58"/>
        <source>标准</source>
        <translation>Standard</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="59"/>
        <source>大</source>
        <translation>Grande</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="60"/>
        <source>超大</source>
        <translation>Très grande</translation>
    </message>
</context>
<context>
    <name>StatusText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="18"/>
        <source>等待中</source>
        <translation>En attente</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="19"/>
        <location filename="../app/widgets/status_style.py" line="26"/>
        <source>训练中</source>
        <translation>Entraînement</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="20"/>
        <location filename="../app/widgets/status_style.py" line="27"/>
        <source>已完成</source>
        <translation>Terminé</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="21"/>
        <location filename="../app/widgets/status_style.py" line="28"/>
        <source>失败</source>
        <translation>Échec</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="22"/>
        <location filename="../app/widgets/status_style.py" line="31"/>
        <source>已跳过</source>
        <translation>Ignoré</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="23"/>
        <location filename="../app/widgets/status_style.py" line="29"/>
        <source>已停止</source>
        <translation>Arrêté</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="24"/>
        <location filename="../app/widgets/status_style.py" line="32"/>
        <source>已中断</source>
        <translation>Interrompu</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="30"/>
        <source>失败/已停止</source>
        <translation>Échec/Arrêté</translation>
    </message>
</context>
<context>
    <name>TaskText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="37"/>
        <source>检测</source>
        <translation>Détection</translation>
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
        <translation>Détection d&apos;anomalies</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="41"/>
        <location filename="../app/widgets/status_style.py" line="42"/>
        <source>字符检测</source>
        <translation>Détection de texte</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="43"/>
        <source>字符识别</source>
        <translation>Reconnaissance de texte</translation>
    </message>
</context>
<context>
    <name>TestDialog</name>
    <message>
        <location filename="../ui/test_dialog.ui" line="14"/>
        <location filename="../ui/test_dialog.ui" line="41"/>
        <source>模型测试</source>
        <translation>Test du modèle</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="102"/>
        <source>检测</source>
        <translation>Détection</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="118"/>
        <source>best.pth</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="130"/>
        <source>mAP50 0.912 · 输入 640 · 规模 n · 训练 2026-09-01 14:22</source>
        <translation>mAP50 0.912 · Entrée 640 · Échelle n · Entraîné le 2026-09-01 14:22</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="151"/>
        <source>数据与设备</source>
        <translation>Données et appareil</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="193"/>
        <source>数据</source>
        <translation>Données</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="216"/>
        <source>设备</source>
        <translation>Appareil</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="246"/>
        <source>测试参数</source>
        <translation>Paramètres de test</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="288"/>
        <source>置信度</source>
        <translation>Confiance</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="329"/>
        <source>低于该分数的预测直接丢弃</source>
        <translation>Les prédictions sous ce score sont écartées</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="345"/>
        <source>IoU 阈值</source>
        <translation>Seuil IoU</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="386"/>
        <source>与标注框重合度达标才算正确检出</source>
        <translation>Le recouvrement avec la boîte de référence doit atteindre cette valeur pour compter comme une détection correcte</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="402"/>
        <source>输出标签文件</source>
        <translation>Écrire les fichiers d&apos;étiquettes</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="434"/>
        <source>写在图像目录下, 可重载数据集查看检出效果</source>
        <translation>Écrit dans le dossier d&apos;images ; rechargez le jeu de données pour vérifier les résultats</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="486"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="496"/>
        <source>请选择数据集</source>
        <translation>Sélectionner les jeux de données</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="544"/>
        <location filename="../app/widgets/test_dialog.py" line="109"/>
        <source>取消</source>
        <translation>Annuler</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="551"/>
        <source>开始测试</source>
        <translation>Démarrer le test</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="237"/>
        <source>未指定模型</source>
        <translation>Aucun modèle spécifié</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="238"/>
        <source>请在模型列表中重新选择一行</source>
        <translation>Sélectionnez à nouveau une ligne dans la liste des modèles</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="254"/>
        <source>输入 {}</source>
        <translation>Entrée {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="256"/>
        <source>规模 {}</source>
        <translation>Échelle {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="258"/>
        <source>训练 {}</source>
        <translation>Entraîné le {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="260"/>
        <source>该记录未保存训练指标</source>
        <translation>Cet enregistrement n&apos;a pas de métriques d&apos;entraînement enregistrées</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="263"/>
        <source> · 文件已不存在</source>
        <translation> · le fichier n&apos;existe plus</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="289"/>
        <source>请先勾选要测试的数据集</source>
        <translation>Cochez d&apos;abord les jeux de données à tester</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="301"/>
        <source>{} 个数据集 · {} 张图</source>
        <translation>{} jeux de données · {} images</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="303"/>
        <source>分类数据集, 统计每张图的判断正确率</source>
        <translation>Jeu de données de classification ; mesure la précision de jugement par image</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="305"/>
        <source>已标注, 评估模式: 统计检出率 / 漏检 / 误检</source>
        <translation>Étiqueté, mode évaluation : taux de détection / oublis / fausses détections</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="307"/>
        <source>未标注, 推理模式: 只输出预测标签</source>
        <translation>Non étiqueté, mode inférence : seules les étiquettes prédites sont écrites</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="309"/>
        <source>部分已标注, 已标注与未标注的数据集不能一起测</source>
        <translation>Partiellement étiqueté ; les jeux de données étiquetés et non étiquetés ne peuvent pas être testés ensemble</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="336"/>
        <source>为判定为不良品的图写 &lt;同名&gt;.json 到图像目录, 多边形标出异常区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Pour les images jugées défectueuses, écrit &lt;même nom&gt;.json dans le dossier des images, avec des polygones délimitant les zones d&apos;anomalie ; l&apos;outil d&apos;annotation peut l&apos;ouvrir directement ; toute annotation manuelle déjà présente sera écrasée</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="340"/>
        <source>把异常区域写成 labelme json, 便于重载复核</source>
        <translation>Écrit les zones d&apos;anomalie au format json labelme, pour faciliter le rechargement et la vérification</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="353"/>
        <source>字符识别只报告字条识别率, 不输出标注文件</source>
        <translation>La reconnaissance de texte ne rapporte que la précision sur les extraits de texte ; aucun fichier d&apos;annotation n&apos;est produit</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="359"/>
        <location filename="../app/widgets/test_dialog.py" line="365"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 框出文本区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Écrit &lt;même-nom&gt;.json dans le dossier des images pour chaque image, en encadrant les zones de texte ; ouvrable directement dans l&apos;outil d&apos;annotation ; les annotations manuelles existantes seront écrasées</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="368"/>
        <source>把检测到的文本框写成 labelme json, 便于重载复核</source>
        <translation>Écrire les zones de texte détectées en labelme json pour vérification après rechargement</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="371"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>Écrit un &lt;même nom&gt;.json dans le dossier des images, ouvrable directement par l&apos;outil d&apos;annotation ; les annotations manuelles déjà présentes seront écrasées</translation>
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
        <translation>Test</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="388"/>
        <source>已有测试在进行中</source>
        <translation>Un test est déjà en cours</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="392"/>
        <source>请至少选择一个数据集</source>
        <translation>Sélectionnez au moins un jeu de données</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="407"/>
        <source>置信度/iou阈值必须是数字</source>
        <translation>Le seuil de confiance / IoU doit être un nombre</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="413"/>
        <source>模型文件不存在, 请重新选择</source>
        <translation>Le fichier du modèle n&apos;existe pas, veuillez le sélectionner à nouveau</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="426"/>
        <source>数据集 {}/{} 未导入图像</source>
        <translation>Le jeu de données {}/{} n&apos;a aucune image importée</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="436"/>
        <source>分类数据集与检测/分割数据集不能同时测试: {}/{}</source>
        <translation>Un jeu de données de classification et un jeu de détection/segmentation ne peuvent pas être testés ensemble : {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="442"/>
        <source>已标注与未标注的数据集不能同时测试: {}/{}</source>
        <translation>Les jeux de données étiquetés et non étiquetés ne peuvent pas être testés ensemble : {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="457"/>
        <source>字符识别要拿标注框裁字条才能测, 请选择已标注的数据集</source>
        <translation>La reconnaissance de texte a besoin des zones annotées pour découper les extraits de texte ; veuillez choisir un jeu de données annoté</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="482"/>
        <source>[test] 启动测试 worker: model={} 数据集={} 图像目录={} device={} cfg={}</source>
        <translation>[test] Lancement du worker de test : model={} jeu de données={} dossier d&apos;images={} device={} cfg={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="487"/>
        <source>测试准备中...</source>
        <translation>Préparation du test...</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="504"/>
        <location filename="../app/widgets/test_dialog.py" line="505"/>
        <source>测试即将开始</source>
        <translation>Le test va bientôt démarrer</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="551"/>
        <source>测试中 {}/{}</source>
        <translation>Test en cours {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="571"/>
        <source>[test-dialog] 测试完成, ok={}</source>
        <translation>[test-dialog] Test terminé, ok={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="579"/>
        <location filename="../app/widgets/test_dialog.py" line="589"/>
        <source>测试结果</source>
        <translation>Résultats du test</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="580"/>
        <source>测试未正常完成</source>
        <translation>Le test ne s&apos;est pas terminé correctement</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="590"/>
        <source>字条 {} 条 · CER {:.4f} · 全对 {} 条</source>
        <translation>{} extraits de texte · CER {:.4f} · {} entièrement corrects</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="597"/>
        <source>[test-dialog] 测试失败: {}</source>
        <translation>[test-dialog] Échec du test : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="604"/>
        <source>测试失败</source>
        <translation>Échec du test</translation>
    </message>
</context>
<context>
    <name>TestReport</name>
    <message>
        <location filename="../app/train/test_report.py" line="179"/>
        <source>漏 {}</source>
        <translation>Oublis {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="181"/>
        <source>误 {}</source>
        <translation>Fausses dét. {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="183"/>
        <source>认错 {}</source>
        <translation>Classe err. {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="194"/>
        <source>(图片无法打开)</source>
        <translation>(image illisible)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="280"/>
        <source>类别认错: {} → {}</source>
        <translation>Classe erronée : {} → {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="308"/>
        <source>本次验证集没有漏检, 也没有误检.</source>
        <translation>Aucun oubli ni fausse détection sur ce jeu de validation.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="311"/>
        <source>明细抽样: 共 {} 张有问题(漏检 {} / 误检 {}), 本报告抽取 {} 张 - 每个类别每种错误最多 {} 张, 按错误数从多到少取</source>
        <translation>Détail échantillonné : {} images problématiques au total ({} oublis / {} fausses détections), ce rapport en retient {} - au maximum {} par classe et par type d&apos;erreur, prises par nombre d&apos;erreurs décroissant</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="316"/>
        <source>明细: 共 {} 张有问题(漏检 {} / 误检 {}), 已全部列出</source>
        <translation>Détail : {} images problématiques au total ({} oublis / {} fausses détections), toutes listées</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="343"/>
        <source>漏检 GT: 有标注但模型没检出</source>
        <translation>Oubli GT : annoté mais non détecté par le modèle</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="345"/>
        <source>误检预测: 模型检出但标注里没有</source>
        <translation>Fausse détection : détectée par le modèle mais absente des annotations</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="347"/>
        <source>正确检出(仅作位置参照)</source>
        <translation>Détection correcte (référence de position uniquement)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="349"/>
        <source>类别认错: 位置对但判错类别(GT → 预测)</source>
        <translation>Classe erronée : position correcte mais classe fausse (GT → prédiction)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="352"/>
        <source>虚线轮廓: 分割 mask / 标注多边形(判定按外接框 IoU)</source>
        <translation>Contour en pointillés : masque de segmentation / polygone d&apos;annotation (jugé sur l&apos;IoU de la boîte englobante)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="450"/>
        <location filename="../app/train/test_report.py" line="1049"/>
        <source>模型评估报告</source>
        <translation>Rapport d&apos;évaluation du modèle</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="454"/>
        <source>当前训练模型</source>
        <translation>Modèle entraîné actuel</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="458"/>
        <location filename="../app/train/test_report.py" line="464"/>
        <source>(未记录)</source>
        <translation>(non enregistré)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="463"/>
        <source>数据集 </source>
        <translation>Jeu de données </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="466"/>
        <source>置信度 {}</source>
        <translation>Confiance {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="486"/>
        <source>测试张数</source>
        <translation>Images testées</translation>
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
        <translation>Images problématiques</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="491"/>
        <source>检出率 (Recall)</source>
        <translation>Taux de détection (Recall)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="493"/>
        <source>准确率 (Precision)</source>
        <translation>Précision (Precision)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="495"/>
        <source>正确检出</source>
        <translation>Détections correctes</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="496"/>
        <source>{} 个</source>
        <translation>{} boîtes</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="497"/>
        <source>漏检 (该抓没抓)</source>
        <translation>Oublis (non détectés)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="498"/>
        <location filename="../app/train/test_report.py" line="501"/>
        <location filename="../app/train/test_report.py" line="506"/>
        <source>{} 个 / {} 张图</source>
        <translation>{} boîtes / {} images</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="500"/>
        <source>误检 (过杀)</source>
        <translation>Fausses détections (surdétection)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="505"/>
        <source>类别认错 (位置对, 类别错)</source>
        <translation>Classe erronée (position correcte, classe fausse)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="508"/>
        <source>指标</source>
        <translation>Métrique</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="509"/>
        <source>值</source>
        <translation>Valeur</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="528"/>
        <source>按类别</source>
        <translation>Par classe</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="531"/>
        <source>类别</source>
        <translation>Classe</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="532"/>
        <source>标注</source>
        <translation>Annotations</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="533"/>
        <source>正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="534"/>
        <source>漏检</source>
        <translation>Oublis</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="535"/>
        <source>误检</source>
        <translation>Fausses détections</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="536"/>
        <source>检出率</source>
        <translation>Taux de détection</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="537"/>
        <source>准确率</source>
        <translation>Précision</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="564"/>
        <source>... 另有 {} 类未列出</source>
        <translation>... et {} classes non listées</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="586"/>
        <source>错误样本明细(仅列漏检 / 误检图片, 正确检出不列出)</source>
        <translation>Détail des échantillons erronés (seules les images en oubli / fausse détection sont listées, les détections correctes ne le sont pas)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="625"/>
        <source>本轮检出率 {:.0f}%, 准确率 {:.0f}%.</source>
        <translation>Taux de détection {:.0f} %, précision {:.0f} %.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="628"/>
        <source>没有逐类别统计, 无法定位到具体标签,请先确认标签文件能正常读到.</source>
        <translation>Aucune statistique par classe, impossible de cibler une étiquette précise ; vérifiez d&apos;abord que les fichiers d&apos;étiquettes sont lisibles.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="652"/>
        <source>漏检分布在</source>
        <translation>Les oublis se répartissent sur </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="653"/>
        <source>漏检集中在</source>
        <translation>Les oublis se concentrent sur </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="656"/>
        <source>(共 {} 个), 优先补这几类的姿态, 光照样本,并复核标注是否有遗漏.</source>
        <translation>(soit {} au total) ; ajoutez en priorité des échantillons de ces classes en variant la pose et l&apos;éclairage, et vérifiez que les annotations sont complètes.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="662"/>
        <source>误检分布在</source>
        <translation>Les fausses détections se répartissent sur </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="663"/>
        <source>误检以</source>
        <translation>Fausses détections principalement sur </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="664"/>
        <source>({} 个),属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({} boîtes), surdétection ; ajoutez des échantillons négatifs sans défaut et nettoyez le bruit d&apos;annotation.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="666"/>
        <source>({} 个)为主,属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({} boîtes) en majorité, surdétection ; ajoutez des échantillons négatifs sans défaut et nettoyez le bruit d&apos;annotation.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="675"/>
        <source>暂无</source>
        <translation>Aucune</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="679"/>
        <source>此外 {} 处位置对但类别判错</source>
        <translation>En outre, {} boîtes sont bien positionnées mais de classe erronée </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="681"/>
        <source>(报告紫框), 属分类能力不足而非定位问题,需补易混淆类别之间的区分性样本.</source>
        <translation>(cadre violet dans le rapport) ; cela relève d&apos;une capacité de classification insuffisante et non d&apos;un problème de localisation ; ajoutez des échantillons discriminants entre les classes faciles à confondre.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="686"/>
        <source>其中</source>
        <translation>Dont la classe </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="688"/>
        <source>仅 {} 个标注, 样本不足是主要瓶颈, 建议补到 200 个以上.</source>
        <translation> ne compte que {} annotations ; le manque d&apos;échantillons est le principal goulot d&apos;étranglement, visez plus de 200.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="693"/>
        <source>各类样本量差距大(最多 {} / 最少 {}),训练时建议做类别均衡采样.</source>
        <translation>Écart important de nombre d&apos;échantillons entre les classes (max {} / min {}) ; à l&apos;entraînement, faites un échantillonnage équilibré par classe.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="698"/>
        <source>把本报告中的漏检, 误检图加入训练集复训,再用同参数复测对比.</source>
        <translation>Ajoutez les images en oubli et en fausse détection de ce rapport au jeu d&apos;entraînement, réentraînez, puis retestez avec les mêmes paramètres pour comparer.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="702"/>
        <source>本轮无漏检, 无误检, 建议用更严的阈值或更难的样本再压一轮, 确认稳定性.</source>
        <translation>Aucun oubli ni fausse détection sur ce test ; utilisez un seuil plus strict ou des échantillons plus difficiles pour une nouvelle passe et confirmer la stabilité.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="898"/>
        <source>改进建议</source>
        <translation>Suggestions d&apos;amélioration</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="903"/>
        <source>基于本次测试的指标与按类别表现</source>
        <translation>D&apos;après les métriques de ce test et les performances par classe</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="905"/>
        <source>(模型: {})</source>
        <translation>(modèle : {})</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="907"/>
        <source>, 建议如下:</source>
        <translation>, voici les suggestions :</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="925"/>
        <source>标红的标签是需要重点关注的类别.</source>
        <translation>Les étiquettes en rouge sont les classes à surveiller en priorité.</translation>
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
        <translation>{}(extrait {} / {} images)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1023"/>
        <source>{}(共 {} 张)</source>
        <translation>{}({} images)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1025"/>
        <source>漏检样本: 有标注但模型没检出</source>
        <translation>Échantillons en oubli : annotés mais non détectés par le modèle</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1028"/>
        <source>误检样本: 模型检出但标注里没有</source>
        <translation>Échantillons en fausse détection : détectés par le modèle mais absents des annotations</translation>
    </message>
</context>
<context>
    <name>TestResultDialog</name>
    <message>
        <location filename="../ui/test_result.ui" line="14"/>
        <source>测试结果分析</source>
        <translation>Analyse des résultats du test</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="83"/>
        <source>图像维度</source>
        <translation>Par image</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="93"/>
        <source>按「张」统计</source>
        <translation>Statistique par image</translation>
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
        <translation>Images testées</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="219"/>
        <source>全对图像</source>
        <translation>Images entièrement correctes</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="275"/>
        <source>有漏检图像</source>
        <translation>Images avec oublis</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="331"/>
        <location filename="../app/train/test_result_dialog.py" line="251"/>
        <source>有误检图像</source>
        <translation>Images avec fausses détections</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="375"/>
        <source>标签维度</source>
        <translation>Par étiquette</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="385"/>
        <source>按「标注框」统计</source>
        <translation>Statistique par boîte d&apos;annotation</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="455"/>
        <location filename="../ui/test_result.ui" line="664"/>
        <location filename="../app/train/test_result_dialog.py" line="259"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>正确检出</source>
        <translation>Détections correctes</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="511"/>
        <location filename="../ui/test_result.ui" line="669"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>漏检</source>
        <translation>Oublis</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="567"/>
        <location filename="../ui/test_result.ui" line="674"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>误检</source>
        <translation>Fausses détections</translation>
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
        <translation>Précision</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="654"/>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>类别</source>
        <translation>Classe</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="659"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>标注数</source>
        <translation>Nb d&apos;annotations</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="679"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>检出率</source>
        <translation>Taux de détection</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="708"/>
        <source>每类抽取</source>
        <translation>Par classe</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="715"/>
        <source>每个类别的每种错误（漏检 / 误检）最多列出几张图。
报告体积约 120 KB 一张，样本多时调小可以显著减小 PDF；选「全部」则每张有问题的图都列。</source>
        <translation>Nombre maximal d&apos;images listées par type d&apos;erreur (oublis / fausses détections) pour chaque classe.
Le rapport pèse environ 120 Ko par image ; réduire cette valeur diminue nettement le PDF quand les échantillons sont nombreux. En choisissant « Tout », toutes les images problématiques sont listées.</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="719"/>
        <source> 张</source>
        <translation> images</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="722"/>
        <source>全部</source>
        <translation>Tout</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="751"/>
        <location filename="../app/train/test_result_dialog.py" line="187"/>
        <source>导出 PDF 报告</source>
        <translation>Exporter le rapport PDF</translation>
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
        <translation>Exporter en PDF chaque image en oubli / fausse détection, avec les boîtes dessinées</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="155"/>
        <source>异常检测的逐图结果已写成 CSV, 不支持导出画框 PDF</source>
        <translation>Les résultats image par image de la détection d&apos;anomalies ont été écrits en CSV ; l&apos;export PDF avec cadres n&apos;est pas pris en charge</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="157"/>
        <source>本次测试没有逐图错误明细, 无法导出</source>
        <translation>Ce test n&apos;a pas de détail d&apos;erreur par image, export impossible</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="169"/>
        <source>保存 PDF 报告</source>
        <translation>Enregistrer le rapport PDF</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="170"/>
        <source>PDF 文件 (*.pdf)</source>
        <translation>Fichiers PDF (*.pdf)</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="176"/>
        <source>正在生成...</source>
        <translation>Génération...</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="194"/>
        <source>无需导出</source>
        <translation>Aucun export nécessaire</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="195"/>
        <source>本次测试没有漏检也没有误检, 没有内容可写.</source>
        <translation>Ce test ne comporte ni oubli ni fausse détection, il n&apos;y a rien à écrire.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="198"/>
        <source>导出完成</source>
        <translation>Export terminé</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="199"/>
        <source>PDF 报告已保存到:
{}</source>
        <translation>Rapport PDF enregistré dans :
{}</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="203"/>
        <source>导出失败</source>
        <translation>Échec de l&apos;export</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="238"/>
        <source>按&quot;张&quot;统计 · 检出 1 个即算检出</source>
        <translation>Statistique par image · une boîte détectée suffit à compter l&apos;image comme détectée</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="240"/>
        <source> · 有标注 {} 张</source>
        <translation> · {} images avec annotation</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="244"/>
        <source>检出图像</source>
        <translation>Images détectées</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="245"/>
        <location filename="../app/train/test_result_dialog.py" line="260"/>
        <source>检出率 </source>
        <translation>Taux de détection </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="247"/>
        <source>未检出图像</source>
        <translation>Images non détectées</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="248"/>
        <source>未检出率 </source>
        <translation>Taux d&apos;oublis </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="252"/>
        <source>误检率 </source>
        <translation>Taux de fausses détections </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="257"/>
        <source>按&quot;标注框&quot;统计 · 标注总数 {}</source>
        <translation>Statistique par boîte d&apos;annotation · {} annotations au total</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="280"/>
        <source>按&quot;张&quot;统计 · 每张图判一个类别</source>
        <translation>Statistique par image · une seule classe jugée par image</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="285"/>
        <source>判断正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="287"/>
        <source>判断错误</source>
        <translation>Incorrect</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="290"/>
        <location filename="../app/train/test_result_dialog.py" line="362"/>
        <source>精度</source>
        <translation>Précision</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="315"/>
        <source>按&quot;张&quot;统计 · 整图判良品/不良品</source>
        <translation>Comptage par image · chaque image jugée conforme ou défectueuse</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="329"/>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <source>检出异常</source>
        <translation>Anomalies détectées</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <source>总图数</source>
        <translation>Nombre total d&apos;images</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="345"/>
        <source>异常</source>
        <translation>Anomalie</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <source>正确</source>
        <translation>Correct</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="362"/>
        <source>错误</source>
        <translation>Incorrect</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="383"/>
        <source>模型里没有判定阈值, 只报告分数, 逐图分数见 CSV 明细.</source>
        <translation>Le modèle n&apos;a pas de seuil de décision ; seuls les scores sont reportés. Scores par image dans le détail CSV.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="384"/>
        <source>判定阈值 {:.4f}. 本次 {} 张, 检出异常 {} 张.</source>
        <translation>Seuil de décision {:.4f}. {} images testées, {} anomalies détectées.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="297"/>
        <source>整体精度 {:.1f}%, &quot;{}&quot;类错误最多({} 张), 是拉低精度的主要原因.</source>
        <translation>Précision globale {:.1f} %, la classe « {} » concentre le plus d&apos;erreurs ({} images) et est la principale cause de la baisse de précision.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="422"/>
        <source>整体漏检偏多(漏检 {} 个, 多于误检 {} 个).&quot;{}&quot;类漏检最多({} 个), 是检出率低的主要原因.</source>
        <translation>Les oublis dominent ({} oublis contre {} fausses détections). La classe « {} » concentre le plus d&apos;oublis ({}) et est la principale cause du faible taux de détection.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="428"/>
        <source>整体误检偏多(误检 {} 个, 多于漏检 {} 个).&quot;{}&quot;类误检最多({} 个), 是准确率低的主要原因.</source>
        <translation>Les fausses détections dominent ({} contre {} oublis). La classe « {} » concentre le plus de fausses détections ({}) et est la principale cause de la faible précision.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="432"/>
        <source>模型表现良好: 无漏检, 无误检.</source>
        <translation>Le modèle se comporte bien : aucun oubli, aucune fausse détection.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="434"/>
        <source>另有 {} 处位置对但类别判错(报告里用紫框标出),属分类能力不足, 需补易混淆类别的区分性样本.</source>
        <translation>{} autres boîtes sont bien positionnées mais de classe erronée (marquées en violet dans le rapport) ; cela révèle une capacité de classification insuffisante et nécessite d&apos;ajouter des échantillons discriminants pour les classes faciles à confondre.</translation>
    </message>
</context>
<context>
    <name>TestRunner</name>
    <message>
        <location filename="../app/train/test_runner.py" line="278"/>
        <source>覆盖已有标注 {}</source>
        <translation>Écrasement des annotations existantes {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="308"/>
        <source>明细初始化失败: {}</source>
        <translation>Échec de l&apos;initialisation des détails : {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="317"/>
        <source>明细目录创建失败: {}</source>
        <translation>Échec de la création du dossier de détails : {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="345"/>
        <source>明细写入失败: {}</source>
        <translation>Échec de l&apos;écriture des détails : {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="427"/>
        <source>当前安装缺少所需组件, 无法执行测试</source>
        <translation>Cette installation ne contient pas les composants requis, test impossible</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="429"/>
        <source>加载模型: {}</source>
        <translation>Chargement du modèle : {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_backend.py" line="36"/>
        <source>推理已优化: {}</source>
        <translation>Inférence optimisée : {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="446"/>
        <source>测试图片 {} 张</source>
        <translation>{} images de test</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="496"/>
        <source>预测失败 {}: {}</source>
        <translation>Échec de la prédiction {} : {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="510"/>
        <source>输出标注失败 {}: {}</source>
        <translation>Échec de l&apos;écriture des annotations {} : {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="565"/>
        <source>WARN 标签目录存在但所有 {} 张图都没读到 GT,请确认标签是 .txt (YOLO) 或 .json (labelme)</source>
        <translation>WARN Le dossier d&apos;étiquettes existe mais aucune GT n&apos;a pu être lue pour les {} images ; vérifiez que les étiquettes sont au format .txt (YOLO) ou .json (labelme)</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="570"/>
        <source>WARN {} 张图缺标签文件</source>
        <translation>WARN {} images sans fichier d&apos;étiquettes</translation>
    </message>
</context>
<context>
    <name>TestWorker</name>
    <message>
        <location filename="../app/train/test_worker.py" line="83"/>
        <source>run 开始</source>
        <translation>run démarré</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="97"/>
        <source>启动子进程: {} {}</source>
        <translation>Lancement du sous-processus : {} {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="109"/>
        <source>启动子进程失败: {}</source>
        <translation>Échec du lancement du sous-processus : {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="116"/>
        <source>启动测试进程失败: {}</source>
        <translation>Échec du lancement du processus de test : {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="118"/>
        <location filename="../app/train/test_worker.py" line="120"/>
        <source>子进程已启动 pid={}</source>
        <translation>Sous-processus lancé pid={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="152"/>
        <source>进入轮询循环</source>
        <translation>Entrée dans la boucle de scrutation</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="162"/>
        <source>轮询中: 文件={}B 已读{}行 子进程={}</source>
        <translation>Scrutation : fichier={}B lignes lues={} sous-processus={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="172"/>
        <source>轮询异常:
</source>
        <translation>Erreur de scrutation :
</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="180"/>
        <source>轮询结束 rc={}</source>
        <translation>Scrutation terminée rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="182"/>
        <source>子进程退出 rc={}</source>
        <translation>Sous-processus terminé rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="192"/>
        <source>测试未能完成, 详情见日志</source>
        <translation>Le test n&apos;a pas pu être terminé, voir le journal</translation>
    </message>
</context>
<context>
    <name>TrainDialog</name>
    <message>
        <location filename="../ui/train.ui" line="14"/>
        <location filename="../ui/train.ui" line="40"/>
        <location filename="../app/train/dialogs.py" line="493"/>
        <source>训练</source>
        <translation>Entraîner</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="50"/>
        <location filename="../ui/train.ui" line="169"/>
        <source>检测</source>
        <translation>Détection</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="118"/>
        <source>模型与数据</source>
        <translation>Modèle et données</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="158"/>
        <source>任务类型</source>
        <translation>Type de tâche</translation>
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
        <translation>Détection d&apos;anomalies</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="189"/>
        <source>字符检测</source>
        <translation>Détection de texte</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="197"/>
        <source>型号</source>
        <translation>Modèle</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="210"/>
        <location filename="../app/train/dialogs.py" line="715"/>
        <source>训练集</source>
        <translation>Jeu d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="230"/>
        <source>验证集</source>
        <translation>Jeu de validation</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="250"/>
        <source>设备</source>
        <translation>Appareil</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="263"/>
        <source>架构</source>
        <translation>Architecture</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="296"/>
        <source>训练超参</source>
        <translation>Hyperparamètres</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="336"/>
        <location filename="../app/train/dialogs.py" line="589"/>
        <source>轮次</source>
        <translation>Époques</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="349"/>
        <source>优化器</source>
        <translation>Optimiseur</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="362"/>
        <location filename="../app/train/dialogs.py" line="592"/>
        <source>早停</source>
        <translation>Arrêt anticipé</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="399"/>
        <source>连续无提升则提前结束，0 为关闭</source>
        <translation>Arrêt anticipé en l&apos;absence d&apos;amélioration ; 0 désactive</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="415"/>
        <location filename="../app/train/dialogs.py" line="595"/>
        <source>学习率</source>
        <translation>Taux d&apos;apprentissage</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="452"/>
        <source>初始学习率，训练中自动衰减</source>
        <translation>Taux d&apos;apprentissage initial, réduit automatiquement pendant l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="468"/>
        <location filename="../app/train/dialogs.py" line="587"/>
        <source>批次</source>
        <translation>Lot</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="481"/>
        <location filename="../app/train/dialogs.py" line="591"/>
        <source>图像尺寸</source>
        <translation>Taille d&apos;image</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="512"/>
        <source>32 的倍数</source>
        <translation>multiple de 32</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="528"/>
        <location filename="../app/train/dialogs.py" line="588"/>
        <source>梯度累积</source>
        <translation>Accumulation de gradient</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="565"/>
        <source>显存不足时调大，等效批次 × N</source>
        <translation>Augmenter en cas de VRAM insuffisante ; lot effectif × N</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="581"/>
        <location filename="../app/train/dialogs.py" line="590"/>
        <source>线程数</source>
        <translation>Threads</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="642"/>
        <source>数据增强</source>
        <translation>Augmentation de données</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="723"/>
        <source>输出</source>
        <translation>Sortie</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="766"/>
        <source>输出路径</source>
        <translation>Chemin de sortie</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="781"/>
        <source>留空则自动按时间生成目录</source>
        <translation>Laisser vide pour générer automatiquement un dossier horodaté</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="794"/>
        <source>选择路径</source>
        <translation>Parcourir</translation>
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
        <translation>Sélectionnez un jeu d&apos;entraînement et un jeu de validation</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="903"/>
        <location filename="../app/train/dialogs.py" line="604"/>
        <source>取消</source>
        <translation>Annuler</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="916"/>
        <location filename="../app/train/dialogs.py" line="1343"/>
        <location filename="../app/train/dialogs.py" line="1352"/>
        <location filename="../app/train/dialogs.py" line="1363"/>
        <location filename="../app/train/dialogs.py" line="1382"/>
        <location filename="../app/train/dialogs.py" line="1395"/>
        <source>加入队列</source>
        <translation>Ajouter à la file d&apos;attente</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="929"/>
        <location filename="../app/train/dialogs.py" line="1274"/>
        <location filename="../app/train/dialogs.py" line="1284"/>
        <location filename="../app/train/dialogs.py" line="1310"/>
        <source>开始训练</source>
        <translation>Démarrer l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="40"/>
        <source>正在检测显卡...</source>
        <translation>Détection des GPU...</translation>
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
        <translation>Le jeu de données « {} » n&apos;a pas d&apos;images importées ou son chemin est invalide. Importez-le avant l&apos;entraînement.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="233"/>
        <source>数据集&quot;{}&quot;尚未导入标签或路径无效, 请先导入该数据集再训练</source>
        <translation>Le jeu de données « {} » n&apos;a pas d&apos;étiquettes importées ou son chemin est invalide. Importez-le avant l&apos;entraînement.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="262"/>
        <location filename="../app/train/dialogs.py" line="1353"/>
        <source>请先选择输出路径</source>
        <translation>Sélectionnez d&apos;abord un chemin de sortie</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="23"/>
        <source>数据集&quot;{}/{}&quot;不是分类数据集(标签格式={}), 无法训练{}</source>
        <translation>Le jeu de données « {}/{} » n&apos;est pas un jeu de classification (format des étiquettes={}) ; impossible d&apos;entraîner {}</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="29"/>
        <source>未知</source>
        <translation>Inconnu</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="25"/>
        <source>数据集&quot;{}/{}&quot;是分类数据集, 无法训练{}任务</source>
        <translation>Le jeu de données « {}/{} » est un jeu de classification ; impossible d&apos;entraîner une tâche de {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="289"/>
        <source>请至少选择一个训练集数据集</source>
        <translation>Sélectionnez au moins un jeu de données d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="291"/>
        <source>请至少选择一个验证集数据集</source>
        <translation>Sélectionnez au moins un jeu de données de validation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="331"/>
        <source>未选数据集</source>
        <translation>aucun jeu de données sélectionné</translation>
    </message>
    <message>
        <location filename="../app/train/detect_common.py" line="12"/>
        <source>目标检测推荐图像尺寸: 640(可设为 32 的倍数如 640/672)</source>
        <translation>Taille d&apos;image recommandée pour la détection : 640 (utilisez un multiple de 32, par ex. 640/672)</translation>
    </message>
    <message>
        <location filename="../app/train/segment_common.py" line="16"/>
        <source>CNN 分割推荐尺寸: 640(需为 32 的倍数)</source>
        <translation>Taille recommandée pour la segmentation CNN : 640 (doit être un multiple de 32)</translation>
    </message>
    <message>
        <location filename="../app/train/classify_common.py" line="27"/>
        <source>图像分类推荐尺寸: 224(小图用 224, 较大图可到 256)</source>
        <translation>Taille recommandée pour la classification d&apos;images : 224 (224 pour les petites images, jusqu&apos;à 256 pour les plus grandes)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="695"/>
        <source>异常检测推荐尺寸: 256; 缺陷很小时调到 512 更稳, 显存和耗时随之上升</source>
        <translation>Taille recommandée pour la détection d&apos;anomalies : 256 ; pour de très petits défauts, 512 est plus fiable, au prix de la VRAM et du temps</translation>
    </message>
    <message>
        <location filename="../app/train/segment_common.py" line="17"/>
        <source>图像分割推荐尺寸: 648(需为 {} 的倍数)</source>
        <translation>Taille recommandée pour la segmentation d&apos;images : 648 (doit être un multiple de {})</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="27"/>
        <source>数据集&quot;{}/{}&quot;没有文本标注, 无法训练{}</source>
        <translation>Le jeu de données &quot;{}/{}&quot; n&apos;a pas d&apos;annotations de texte ; impossible d&apos;entraîner {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_common.py" line="56"/>
        <source>字符检测推荐尺寸: 1024(需为 {} 的倍数); 识别段固定 32x128, 不受此项影响</source>
        <translation>Taille recommandée pour la détection de texte : 1024 (doit être un multiple de {}) ; l&apos;étape de reconnaissance est fixée à 32x128 et n&apos;est pas concernée</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="466"/>
        <source>{} 的倍数</source>
        <translation>multiple de {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_common.py" line="31"/>
        <source>建议 224</source>
        <translation>224 conseillé</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="700"/>
        <source>建议 256</source>
        <translation>256 recommandé</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="691"/>
        <source>训练集 {} 个 · 验证集 {} 个 · 共 {} 张图</source>
        <translation>{} jeux d&apos;entraînement · {} jeux de validation · {} images au total</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="694"/>
        <source>未选择验证集</source>
        <translation>aucun jeu de validation sélectionné</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="696"/>
        <source>已标注, 可直接训练</source>
        <translation>étiqueté, prêt à entraîner</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="698"/>
        <source>有 {} 个数据集尚未标注</source>
        <translation>{} jeu(x) de données pas encore étiqueté(s)</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="712"/>
        <source>请选择验证集</source>
        <translation>Sélectionner les jeux de validation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="797"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>Un entraînement est déjà en cours, arrêtez-le d&apos;abord</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="76"/>
        <source>几何变换</source>
        <translation>Géométrique</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="77"/>
        <source>标注框会跟着一起变换</source>
        <translation>Les boîtes suivent la transformation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="78"/>
        <source>像素变换</source>
        <translation>Pixels</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="79"/>
        <source>只改画面，标注框不动</source>
        <translation>Image seule, boîtes inchangées</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="82"/>
        <source>水平翻转</source>
        <translation>Miroir horizontal</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="84"/>
        <source>垂直翻转</source>
        <translation>Miroir vertical</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="86"/>
        <source>旋转</source>
        <translation>Rotation</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="87"/>
        <source>±15°</source>
        <translation>±15°</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="88"/>
        <source>仿射</source>
        <translation>Affine</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="90"/>
        <source>马赛克</source>
        <translation>Mosaïque</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="91"/>
        <source>4 图拼接</source>
        <translation>4 images</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="92"/>
        <source>亮度/对比度</source>
        <translation>Luminosité/contraste</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="93"/>
        <source>±0.1</source>
        <translation>±0.1</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="94"/>
        <source>颜色抖动</source>
        <translation>Variation de couleur</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="95"/>
        <source>饱和/色相</source>
        <translation>saturation/teinte</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="96"/>
        <source>高斯模糊</source>
        <translation>Flou gaussien</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="97"/>
        <source>核 3</source>
        <translation>noyau 3</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="98"/>
        <source>高斯噪声</source>
        <translation>Bruit gaussien</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="99"/>
        <source>σ 0.05</source>
        <translation>σ 0.05</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="101"/>
        <source>已启用 {} 项</source>
        <translation>{} activés</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="102"/>
        <source>该任务不支持配置数据增强</source>
        <translation>Cette tâche ne permet pas de configurer l&apos;augmentation de données</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="104"/>
        <source>当前网络架构不支持该增强</source>
        <translation>L&apos;architecture réseau actuelle ne prend pas en charge cette augmentation</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="722"/>
        <source>异常检测算法自带学习率与优化器, 不需要设置</source>
        <translation>Les algorithmes de détection d&apos;anomalies intègrent leur propre taux d&apos;apprentissage et optimiseur ; rien à configurer</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="728"/>
        <source>建库型算法只提取特征建立记忆库, 没有训练轮次</source>
        <translation>Les algorithmes à banque de mémoire extraient seulement des caractéristiques pour construire la banque de mémoire ; il n&apos;y a pas d&apos;époques d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="669"/>
        <source>仅建库</source>
        <translation>Construction seule</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1210"/>
        <source>请至少选择一个数据集</source>
        <translation>Sélectionnez au moins un jeu de données</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1214"/>
        <location filename="../app/train/dialogs.py" line="1224"/>
        <source>&quot;{}&quot;不能为空</source>
        <translation>« {} » ne peut pas être vide</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1219"/>
        <source>&quot;{}&quot;必须是整数(当前: {})</source>
        <translation>« {} » doit être un entier (actuel : {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1229"/>
        <source>&quot;{}&quot;必须是数字(当前: {})</source>
        <translation>« {} » doit être un nombre (actuel : {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1238"/>
        <source>图像尺寸需为 {} 的倍数(当前 {}), 可改为 {}</source>
        <translation>La taille d&apos;image doit être un multiple de {} (actuelle {}) ; essayez {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1254"/>
        <source>选择输出目录</source>
        <translation>Sélectionner le dossier de sortie</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1268"/>
        <source>当前安装缺少 CNN 架构所需的组件, 无法训练.
请重新安装软件后再试</source>
        <translation>Cette installation ne contient pas les composants requis par l&apos;architecture CNN, entraînement impossible.
Veuillez réinstaller le logiciel</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1275"/>
        <source>当前已有训练在进行中, 请先停止!</source>
        <translation>Un entraînement est déjà en cours, arrêtez-le d&apos;abord !</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1279"/>
        <source>参数校验未通过: {}</source>
        <translation>Validation des paramètres échouée : {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1280"/>
        <location filename="../app/train/dialogs.py" line="1339"/>
        <source>参数校验</source>
        <translation>Validation des paramètres</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1300"/>
        <source>训练启动失败: {}
{}</source>
        <translation>Échec du démarrage de l&apos;entraînement : {}
{}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1303"/>
        <source>训练启动失败</source>
        <translation>Échec du démarrage de l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1311"/>
        <source>已有训练在进行中, 请先停止!</source>
        <translation>Un entraînement est déjà en cours, arrêtez-le d&apos;abord !</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1313"/>
        <source>开始训练: 任务类型={} 训练集={} 验证集={}</source>
        <translation>Début de l&apos;entraînement : type de tâche={} jeu d&apos;entraînement={} jeu de validation={}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1329"/>
        <source>开始训练: 字符检测分两段入队 | {} | {}</source>
        <translation>Démarrage de l&apos;entraînement : détection de texte mise en file en deux étapes | {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1368"/>
        <source>队列</source>
        <translation>File d&apos;attente</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1369"/>
        <source>已更新该队列任务的参数</source>
        <translation>Paramètres de la tâche de la file d&apos;attente mis à jour</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1375"/>
        <source>加入队列失败</source>
        <translation>Échec de l&apos;ajout à la file d&apos;attente</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1378"/>
        <source>加入训练队列: {} | {}</source>
        <translation>Ajout à la file d&apos;attente d&apos;entraînement : {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1383"/>
        <source>已加入队列(第 {} 个), 可在首页&quot;队列&quot;中查看或启动.</source>
        <translation>Ajouté à la file d&apos;attente (position {}) ; consultez-le ou lancez-le depuis « File d&apos;attente » sur la page d&apos;accueil.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1396"/>
        <source>字符检测已拆成检测段与识别段, 分别排在第 {} 和第 {} 个</source>
        <translation>Détection de texte divisée en étape de détection et étape de reconnaissance, respectivement aux rangs {} et {}</translation>
    </message>
</context>
<context>
    <name>TrainMixin</name>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="47"/>
        <source>{} 训练中 0/{}</source>
        <translation>{} entraînement 0/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="86"/>
        <source>[train] 训练线程已结束但未返回结果, 按失败收尾</source>
        <translation>[train] Le thread d&apos;entraînement s&apos;est terminé sans renvoyer de résultat, traité comme un échec</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="97"/>
        <source>仅停止当前</source>
        <translation>Arrêter uniquement l&apos;actuel</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="98"/>
        <source>停止队列</source>
        <translation>Arrêter la file d&apos;attente</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <location filename="../app/mixins/train_mixin.py" line="121"/>
        <source>停止训练</source>
        <translation>Arrêter l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <source>当前正在跑训练队列, 要停止到什么范围?</source>
        <translation>Une file d&apos;attente d&apos;entraînement est en cours. Jusqu&apos;où faut-il arrêter ?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="102"/>
        <location filename="../app/mixins/train_mixin.py" line="103"/>
        <source>取消</source>
        <translation>Annuler</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <source>确定要停止当前训练吗?</source>
        <translation>Arrêter l&apos;entraînement en cours ?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="117"/>
        <source>手动停止训练: {}</source>
        <translation>Arrêt manuel de l&apos;entraînement : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="119"/>
        <source>[train] 训练进程 10 秒内未退出, 可能有子进程残留占用显存</source>
        <translation>[train] Le processus d&apos;entraînement ne s&apos;est pas arrêté en 10 secondes ; des sous-processus occupent peut-être encore la VRAM</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="122"/>
        <source>训练进程未能完全退出, 可能仍有子进程占用显存.
建议稍等片刻再启动下一个任务.</source>
        <translation>Le processus d&apos;entraînement ne s&apos;est pas complètement terminé ; des processus enfants occupent peut-être encore la VRAM.
Attendez un instant avant de lancer la tâche suivante.</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="134"/>
        <source>{} 训练中 {}/{}</source>
        <translation>{} entraînement {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="147"/>
        <source>进度 | 当前最好 {}</source>
        <translation>Progression | meilleur score : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="211"/>
        <source>更新训练指标: record={} 已完成epoch={} {}={} 类别数={}</source>
        <translation>Mise à jour des métriques d&apos;entraînement : record={} epoch terminés={} {}={} nombre de classes={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="310"/>
        <source>等待显存释放 · 下一项:{}</source>
        <translation>Attente libération VRAM · suivant : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="187"/>
        <source>训练失败(队列模式, 已跳过弹窗): {}</source>
        <translation>Échec de l&apos;entraînement (mode file d&apos;attente, boîte de dialogue ignorée) : {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="189"/>
        <source>训练失败</source>
        <translation>Échec de l&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="190"/>
        <source>训练过程中发生错误, Err:

{}</source>
        <translation>Une erreur est survenue pendant l&apos;entraînement, Err :

{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="283"/>
        <source>已保存模型记录: {} | {}</source>
        <translation>Enregistrement de modèle sauvegardé : {} | {}</translation>
    </message>
</context>
<context>
    <name>TrainQueueDialog</name>
    <message>
        <location filename="../ui/train_queue.ui" line="14"/>
        <location filename="../ui/train_queue.ui" line="40"/>
        <location filename="../app/widgets/queue_dialog.py" line="33"/>
        <source>训练队列</source>
        <translation>File d&apos;attente d&apos;entraînement</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="50"/>
        <location filename="../app/widgets/queue_dialog.py" line="123"/>
        <source>空闲</source>
        <translation>Inactif</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="93"/>
        <source>#</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="98"/>
        <source>名称</source>
        <translation>Nom</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="103"/>
        <source>任务</source>
        <translation>Tâche</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="108"/>
        <source>数据集</source>
        <translation>Jeu de données</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="113"/>
        <source>型号</source>
        <translation>Modèle</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="118"/>
        <source>轮次</source>
        <translation>Époques</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="123"/>
        <source>状态</source>
        <translation>État</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="152"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="168"/>
        <source>队列为空，可在训练界面点「加入队列」添加任务</source>
        <translation>La file d&apos;attente est vide ; cliquez sur « Ajouter à la file d&apos;attente » dans la fenêtre d&apos;entraînement pour ajouter des tâches.</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="199"/>
        <source>上移</source>
        <translation>Monter</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="209"/>
        <source>下移</source>
        <translation>Descendre</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="219"/>
        <location filename="../app/widgets/queue_dialog.py" line="255"/>
        <source>移除</source>
        <translation>Retirer</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="229"/>
        <source>清理已结束</source>
        <translation>Vider les tâches terminées</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="252"/>
        <source>编辑</source>
        <translation>Modifier</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="259"/>
        <source>关闭</source>
        <translation>Fermer</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="272"/>
        <location filename="../app/widgets/queue_dialog.py" line="144"/>
        <source>开始队列</source>
        <translation>Démarrer la file d&apos;attente</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="22"/>
        <source>队列为空, 可在训练界面点&quot;加入队列&quot;添加任务</source>
        <translation>La file d&apos;attente est vide ; cliquez sur « Ajouter à la file d&apos;attente » dans la fenêtre d&apos;entraînement pour ajouter des tâches.</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>运行中</source>
        <translation>En cours</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>队列正在串行执行</source>
        <translation>La file d&apos;attente exécute les tâches les unes après les autres</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="115"/>
        <source>待启动</source>
        <translation>En attente de démarrage</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="116"/>
        <source>有 {} 个任务等待启动</source>
        <translation>{} tâche(s) en attente de démarrage</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>训练中</source>
        <translation>Entraînement</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>当前有训练在进行(非队列启动)</source>
        <translation>Un entraînement est en cours (non lancé par la file d&apos;attente)</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="120"/>
        <source>已结束</source>
        <translation>Terminé</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="121"/>
        <source>没有待执行的任务, 点&quot;重新开始队列&quot;可重跑</source>
        <translation>Aucune tâche en attente ; cliquez sur « Redémarrer la file d&apos;attente » pour les relancer</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="127"/>
        <source>共 {} 个: 等待 {} · 完成 {} · 失败 {}</source>
        <translation>{} au total : {} en attente · {} terminées · {} échouées</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="130"/>
        <source>正在训练&quot;{}&quot; · {}</source>
        <translation>Entraînement de « {} » · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="133"/>
        <source>下一个: &quot;{}&quot; · {}</source>
        <translation>Suivant : « {} » · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="146"/>
        <location filename="../app/widgets/queue_dialog.py" line="183"/>
        <source>重新开始队列</source>
        <translation>Redémarrer la file d&apos;attente</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="168"/>
        <location filename="../app/widgets/queue_dialog.py" line="190"/>
        <source>队列</source>
        <translation>File d&apos;attente</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="169"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>Un entraînement est déjà en cours, arrêtez-le d&apos;abord</translation>
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
        <translation>Aucune tâche en attente dans la file d&apos;attente.

À relancer : {}

Les remettre en file et démarrer l&apos;entraînement ?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="191"/>
        <source>队列启动失败, 请查看日志</source>
        <translation>Échec du démarrage de la file d&apos;attente, consultez le journal</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="207"/>
        <location filename="../app/widgets/queue_dialog.py" line="211"/>
        <source>移除任务</source>
        <translation>Retirer la tâche</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="208"/>
        <source>训练中的任务不能移除, 请先停止</source>
        <translation>Une tâche en cours ne peut pas être retirée, arrêtez-la d&apos;abord</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="212"/>
        <source>确定从队列中移除&quot;{}&quot;吗?</source>
        <translation>Retirer « {} » de la file d&apos;attente ?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="219"/>
        <source>清理</source>
        <translation>Vider</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="220"/>
        <source>没有已结束的任务</source>
        <translation>Aucune tâche terminée</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="222"/>
        <source>[队列] 已清理 {} 个已结束任务</source>
        <translation>[队列] {} tâches terminées supprimées</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="229"/>
        <source>编辑任务</source>
        <translation>Modifier la tâche</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="230"/>
        <source>训练中的任务不能编辑, 请先停止</source>
        <translation>Une tâche en cours ne peut pas être modifiée, arrêtez-la d&apos;abord</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="246"/>
        <source>重新入队</source>
        <translation>Remettre en file</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="248"/>
        <location filename="../app/widgets/queue_dialog.py" line="269"/>
        <source>打开输出目录</source>
        <translation>Ouvrir le dossier de sortie</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="250"/>
        <source>在模型界面查看</source>
        <translation>Voir dans le gestionnaire de modèles</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="270"/>
        <source>目录不存在: {}</source>
        <translation>Le dossier n&apos;existe pas : {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="271"/>
        <source>未设置</source>
        <translation>Non défini</translation>
    </message>
</context>
<context>
    <name>TrainRunner</name>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="114"/>
        <source>数据增强需要 kornia 或 albumentations, 当前环境两者都没有.
请把训练参数里的&quot;数据增强&quot;全部取消勾选, 或补装组件后重试</source>
        <translation>L&apos;augmentation de données nécessite kornia ou albumentations, aucun des deux n&apos;est installé.
Décochez tout dans « Augmentation de données » des paramètres d&apos;entraînement, ou installez-en un puis réessayez</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="203"/>
        <location filename="../app/train/transformer_train_runner.py" line="131"/>
        <source>输出路径: {}</source>
        <translation>Chemin de sortie : {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="204"/>
        <location filename="../app/train/transformer_train_runner.py" line="132"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>Dossier de sortie de cet entraînement (horodatage) : {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="134"/>
        <source>训练配置文件已保存 → {}</source>
        <translation>Fichier de configuration d&apos;entraînement enregistré → {}</translation>
    </message>
    <message>
        <location filename="../app/train/transformer_train_runner.py" line="156"/>
        <source>分割模型 resolution 已自动取整: {} → {} (block={})</source>
        <translation>Résolution du modèle de segmentation arrondie automatiquement : {} → {} (block={})</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="241"/>
        <location filename="../app/train/transformer_train_runner.py" line="158"/>
        <source>使用模型 {} device={} epochs={} batch={} resolution={}</source>
        <translation>Modèle utilisé {} device={} epochs={} batch={} resolution={}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="253"/>
        <location filename="../app/train/transformer_train_runner.py" line="169"/>
        <source>数据增强: {}</source>
        <translation>Augmentation de données: {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="256"/>
        <location filename="../app/train/transformer_train_runner.py" line="172"/>
        <source>数据增强: 未启用</source>
        <translation>Augmentation : aucune</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="282"/>
        <location filename="../app/train/transformer_train_runner.py" line="240"/>
        <source>训练完成</source>
        <translation>Entraînement terminé</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="289"/>
        <location filename="../app/train/transformer_train_runner.py" line="249"/>
        <source>生成类别文件: {}</source>
        <translation>Génération du fichier de classes : {}</translation>
    </message>
    <message>
        <location filename="../app/train/cnn_train_runner.py" line="210"/>
        <location filename="../app/train/transformer_train_runner.py" line="143"/>
        <source>预训练权重缺失: 请先在权重管理里下载 {} 档的模型</source>
        <translation>Poids pré-entraînés manquants : téléchargez d&apos;abord le modèle de niveau {} dans Poids du modèle</translation>
    </message>
</context>
<context>
    <name>TrainWorker</name>
    <message>
        <location filename="../app/train/train_worker.py" line="483"/>
        <source>训练监控异常, 已终止.

{}</source>
        <translation>Erreur du moniteur d&apos;entraînement, processus terminé.

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="492"/>
        <source>训练结果文件读取失败: {}

{}</source>
        <translation>Échec de la lecture du fichier de résultats d&apos;entraînement : {}

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="497"/>
        <source>训练进程异常退出 (code={})

--- 子进程输出(尾部) ---
{}</source>
        <translation>Le processus d&apos;entraînement s&apos;est terminé anormalement (code={})

--- sortie du sous-processus (fin) ---
{}</translation>
    </message>
</context>
<context>
    <name>Utils</name>
    <message>
        <location filename="../app/core/utils.py" line="59"/>
        <location filename="../app/core/utils.py" line="71"/>
        <source>{}秒</source>
        <translation>{} s</translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="65"/>
        <source>{}天</source>
        <translation>{} j </translation>
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
        <translation>Dissocier le poids local</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="177"/>
        <source>已就绪</source>
        <translation>Prêt</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="184"/>
        <source>未下载</source>
        <translation>Non téléchargé</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="193"/>
        <source>更换</source>
        <translation>Modifier</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="201"/>
        <source>本地权重</source>
        <translation>Poids local</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="210"/>
        <source>重选</source>
        <translation>Choisir à nouveau</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="211"/>
        <source>(路径未记录)</source>
        <translation>(chemin non enregistré)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="213"/>
        <source>本地失效</source>
        <translation>Poids local manquant</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="215"/>
        <source>登记的本地权重文件已不在这个位置:
{}</source>
        <translation>Le fichier de poids local enregistré n&apos;est plus à cet emplacement :
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="220"/>
        <source>校验中...</source>
        <translation>Vérification...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="239"/>
        <source>失败</source>
        <translation>Échec</translation>
    </message>
</context>
<context>
    <name>_PixelScaleDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="108"/>
        <source>像素精度</source>
        <translation>Échelle de pixel</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="114"/>
        <source>1 像素代表的实际长度</source>
        <translation>Longueur réelle représentée par 1 pixel</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="147"/>
        <source>请输入大于 0 的数字</source>
        <translation>Saisissez un nombre supérieur à 0</translation>
    </message>
</context>
<context>
    <name>_TrainStartDialog</name>
    <message>
        <location filename="../app/train/dialogs.py" line="341"/>
        <source>训练即将开始</source>
        <translation>L&apos;entraînement va bientôt démarrer</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="351"/>
        <location filename="../app/train/dialogs.py" line="364"/>
        <source>确认({})</source>
        <translation>Valider ({})</translation>
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
        <translation>Importer</translation>
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
        <translation>Polygone</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="46"/>
        <source>删除图像</source>
        <translation>Supprimer l&apos;image</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="70"/>
        <source>设置</source>
        <translation>Paramètres</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="90"/>
        <source>标签列表</source>
        <translation>Étiquettes</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="113"/>
        <source>添加标签</source>
        <translation>Ajouter une étiquette</translation>
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
        <location filename="../ui/annotation.ui" line="180"/>
        <source>转换</source>
        <translation>Convertir</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="210"/>
        <source>图像信息</source>
        <translation>Infos image</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="237"/>
        <source>剪切板</source>
        <translation>Presse-papiers</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="302"/>
        <source>上一张(A)</source>
        <translation>Précédent (A)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="309"/>
        <source>下一张(D)</source>
        <translation>Suivant (D)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="359"/>
        <source>标注参数</source>
        <translation>Paramètres d&apos;annotation</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="371"/>
        <source>角度范围</source>
        <translation>Plage d&apos;angles</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="385"/>
        <source>~</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="419"/>
        <source>融合强度</source>
        <translation>Intensité de fusion</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="453"/>
        <source>亮度调节</source>
        <translation>Luminosité</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="487"/>
        <source>填充颜色</source>
        <translation>Couleur de remplissage</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="494"/>
        <source>点击打开取色器, 选任意颜色</source>
        <translation>Cliquez pour ouvrir le sélecteur de couleur</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="507"/>
        <source>支持 #RRGGBB / #RGB / 255,255,255 / black / 白 等写法, 也可以点左边色块打开取色器</source>
        <translation>Accepte les formats #RRGGBB / #RGB / 255,255,255 / black / white, etc. ; vous pouvez aussi cliquer sur le carré de couleur à gauche pour ouvrir le sélecteur</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="510"/>
        <source>#RRGGBB</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="517"/>
        <source>自定义颜色</source>
        <translation>Couleur personnalisée</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="544"/>
        <source>常用色</source>
        <translation>Couleurs prédéfinies</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="575"/>
        <source>恢复默认</source>
        <translation>Rétablir les valeurs par défaut</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="595"/>
        <source>完成</source>
        <translation>Terminer</translation>
    </message>
</context>
</TS>
