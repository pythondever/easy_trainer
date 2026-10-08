<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ko_KR">
<context>
    <name>AdCommon</name>
    <message>
        <location filename="../app/train/ad_common.py" line="92"/>
        <source>找不到可写的纯英文暂存目录(异常检测的底层库不支持中文路径), 请把输出路径改到纯英文目录下</source>
        <translation>쓸 수 있는 영문(ASCII) 임시 디렉터리를 찾지 못했습니다(이상 검출 하위 라이브러리가 비ASCII 경로를 지원하지 않습니다). 출력 경로를 영문 디렉터리로 변경하세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="153"/>
        <location filename="../app/train/ad_common.py" line="655"/>
        <source>(根目录散图)</source>
        <translation>(루트 디렉터리 낱개 이미지)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="176"/>
        <source>数据集里没找到图像, 请先导入数据</source>
        <translation>데이터셋에서 이미지를 찾지 못했습니다. 먼저 데이터를 가져오세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="181"/>
        <source>无法从类别名判断哪个是正常品, 请把放良品图的那个文件夹改名为 {} 之一; 现有类别: {}</source>
        <translation>클래스 이름만으로는 어느 것이 양품인지 판단할 수 없습니다. 양품 이미지가 들어 있는 폴더 이름을 {} 중 하나로 변경하세요. 현재 클래스: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="187"/>
        <source>训练集里没有图像</source>
        <translation>학습 세트에 이미지가 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="191"/>
        <source>训练集里只有&quot;{}&quot;一类, 而良品类是&quot;{}&quot;; 请把良品图所在的类别文件夹挂到训练集上</source>
        <translation>학습 세트에 &quot;{}&quot; 클래스 하나만 있는데 양품 클래스는 &quot;{}&quot;입니다. 양품 이미지가 있는 클래스 폴더를 학습 세트에 연결하세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="199"/>
        <source>训练集里既没有&quot;{}&quot;类、又不止一类, 无法确定拿哪批图建库; 现有类别: {}</source>
        <translation>학습 세트에 &quot;{}&quot; 클래스가 없고 클래스가 둘 이상이라 어떤 이미지로 메모리 뱅크를 구축할지 결정할 수 없습니다. 현재 클래스: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="240"/>
        <source>训练集根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>학습 세트 루트 디렉터리에 낱개 이미지와 하위 폴더가 함께 있어 낱개 이미지가 어느 클래스인지 결정할 수 없습니다. 하나의 클래스 폴더에 넣어 주세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="274"/>
        <source>没有找到任何图像, 请检查数据集</source>
        <translation>이미지를 찾지 못했습니다. 데이터셋을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="276"/>
        <source>根目录下既有散图又有子文件夹, 无法确定散图属于哪一类, 请把它们放进同一个类别文件夹</source>
        <translation>루트 디렉터리에 낱개 이미지와 하위 폴더가 함께 있어 낱개 이미지가 어느 클래스인지 결정할 수 없습니다. 하나의 클래스 폴더에 넣어 주세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="281"/>
        <source>无法判断哪个类别是良品, 现有类别: {}.
请把良品图放在名为 {} 一类的子文件夹里, 或按训练时的方式重新导入数据集</source>
        <translation>어느 클래스가 양품인지 판단할 수 없습니다. 현재 클래스: {}.
양품 이미지를 {} 중 하나의 이름을 가진 하위 폴더에 넣거나, 학습할 때와 같은 방식으로 데이터셋을 다시 가져오세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="422"/>
        <source>未知的异常检测算法: {}</source>
        <translation>알 수 없는 이상 검출 알고리즘: {}</translation>
    </message>
</context>
<context>
    <name>AdPackage</name>
    <message>
        <location filename="../app/train/ad_package.py" line="88"/>
        <source>正在复制模型文件...</source>
        <translation>모델 파일 복사 중...</translation>
    </message>
</context>
<context>
    <name>AdTestRunner</name>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="47"/>
        <source>缺少测试依赖: {}</source>
        <translation>테스트 의존성이 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="77"/>
        <source>加载异常检测模型: {}</source>
        <translation>이상 검출 모델 불러오기: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="86"/>
        <source>算法={} 图像尺寸={} 阈值={:.6f}</source>
        <translation>알고리즘={} 이미지 크기={} 임계값={:.6f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="88"/>
        <source>原尺寸</source>
        <translation>원본 크기</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="96"/>
        <source>没有可用的图像目录, 请检查数据集</source>
        <translation>사용할 수 있는 이미지 디렉터리가 없습니다. 데이터셋을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="107"/>
        <source>测试图片 {} 张, 良品类别: {}</source>
        <translation>테스트 이미지 {}장, 정상 클래스: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="144"/>
        <source>没有取到任何图像, 请检查数据集</source>
        <translation>이미지를 하나도 읽지 못했습니다. 데이터셋을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="151"/>
        <source>沿用训练时定下的阈值 {:.6f}</source>
        <translation>학습 시 정한 임계값을 그대로 사용합니다: {:.6f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="155"/>
        <source>模型里没有阈值, 本批又只有一类样本, 定不出判定阈值, 只报告分数</source>
        <translation>모델에 임계값이 없고 이번 배치에 클래스가 하나뿐이라 판정 임계값을 정할 수 없습니다. 점수만 보고합니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="159"/>
        <source>模型里没有阈值, 已按本批数据现挑 {:.6f}(精度会偏乐观)</source>
        <translation>모델에 임계값이 없어 이번 배치 데이터에서 임의로 선정했습니다: {:.6f}(정확도가 낙관적입니다)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="189"/>
        <source>完成: {} 张, 没有判定阈值, 只报告分数</source>
        <translation>완료: {}장, 판정 임계값 없음, 점수만 보고</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="195"/>
        <source>完成: {} 张, 检出异常 {} 张</source>
        <translation>완료: {}장, 이상 {}장 검출</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="199"/>
        <source>完成: {} 张, 准确率 {:.4f}, 漏检 {} 张, 误检 {} 张</source>
        <translation>완료: {}장, 정확도 {:.4f}, 미검출 {}장, 오검출 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="204"/>
        <source>  image AUROC = {:.4f}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="220"/>
        <source>模型里没有判定阈值, 不输出异常区域</source>
        <translation>모델에 판정 임계값이 없어 이상 영역을 출력하지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="223"/>
        <source>异常</source>
        <translation>이상</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="233"/>
        <source>提取异常区域失败 {}: {}</source>
        <translation>이상 영역 추출 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="250"/>
        <source>输出异常区域失败 {}: {}</source>
        <translation>이상 영역 출력 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="254"/>
        <source>已为 {} 张不良品图写出异常区域标注(图像同目录)</source>
        <translation>이상 이미지 {}장에 이상 영역 어노테이션을 작성했습니다(이미지와 같은 디렉터리)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="258"/>
        <source>另有 {} 张判为不良品, 但热力图没超过判定线, 未写标注</source>
        <translation>그 외 {}장은 이상으로 판정되었지만 히트맵이 판정 임계값을 넘지 않아 어노테이션을 작성하지 않았습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="277"/>
        <source>图像</source>
        <translation>이미지</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="278"/>
        <source>类别</source>
        <translation>클래스</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="279"/>
        <source>真值</source>
        <translation>정답</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="280"/>
        <source>判定</source>
        <translation>판정</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="281"/>
        <source>分数</source>
        <translation>점수</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="282"/>
        <source>阈值</source>
        <translation>임계값</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="283"/>
        <source>是否正确</source>
        <translation>정답 여부</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="298"/>
        <source>是</source>
        <translation>예</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="299"/>
        <source>否</source>
        <translation>아니요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_test_runner.py" line="301"/>
        <source>逐图明细: {}</source>
        <translation>이미지별 상세: {}</translation>
    </message>
</context>
<context>
    <name>AdTrainRunner</name>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="49"/>
        <source>缺少训练依赖: {}</source>
        <translation>학습 의존성이 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="137"/>
        <source>anomalib {} / torch {}</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="170"/>
        <source>输出路径: {}</source>
        <translation>출력 경로: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="172"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>이번 학습 출력 디렉터리(타임스탬프): {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="186"/>
        <source>异常检测: 算法={} 骨干={} 轮次={} 批次={} 图像尺寸={} device={}</source>
        <translation>이상 검출: 알고리즘={} 백본={} 에포크={} 배치={} 이미지 크기={} device={}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="198"/>
        <source>数据准备: 建库集 {} 张({}), 测试集 正常 {} 张 / 异常 {} 张</source>
        <translation>데이터 준비: 메모리 뱅크 {}장({}), 테스트 세트 정상 {}장 / 이상 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="203"/>
        <source>  异常类别: {}</source>
        <translation>  이상 클래스: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="204"/>
        <source>(散图)</source>
        <translation>(낱개 이미지)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="209"/>
        <source>  注意: 建库集里另有 {} 张非正常图, 未参与建库</source>
        <translation>  주의: 메모리 뱅크에 정상이 아닌 이미지가 {}장 더 있으나 구축에 사용하지 않았습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="213"/>
        <source>建库集里没有图像, 请检查数据集</source>
        <translation>메모리 뱅크에 이미지가 없습니다. 데이터셋을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="215"/>
        <source>测试集里没有图像, 请检查数据集</source>
        <translation>테스트 세트에 이미지가 없습니다. 데이터셋을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="234"/>
        <source>数据集: 建库集 {} 张</source>
        <translation>데이터셋: 메모리 뱅크 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="243"/>
        <source>模型构建完成({:.1f}s): {}</source>
        <translation>모델 구성 완료({:.1f}s): {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="261"/>
        <source>建库/训练完成({:.1f}s)</source>
        <translation>메모리 뱅크 구축/학습 완료({:.1f}s)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="274"/>
        <source>  评估中: {} 张</source>
        <translation>  평가 중: {}장</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="283"/>
        <source>评估阶段失败, 只交付模型: {}</source>
        <translation>평가 단계 실패, 모델만 전달합니다: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="288"/>
        <source>评估完成({:.1f}s): {} 张</source>
        <translation>평가 완료({:.1f}s): {}장</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="291"/>
        <source>  测试集里只有一类样本, 定不出判定阈值(没有真值反差), AUROC 和准确率都算不了; 补一些异常样本重新训练才有交付阈值</source>
        <translation>  테스트 세트에 클래스가 하나뿐이라 판정 임계값을 정할 수 없고(정답 대비가 없음), AUROC와 정확도도 계산할 수 없습니다. 이상 샘플을 보충해 다시 학습해야 전달할 판정 임계값이 생깁니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="296"/>
        <source>评估完成({:.1f}s): {} 张, 准确率 {:.4f}</source>
        <translation>평가 완료({:.1f}s): {}장, 정확도 {:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="300"/>
        <source>  image AUROC = {:.4f}  阈值 = {:.6f}(本批最优 F1 处)</source>
        <translation>  image AUROC = {:.4f}  임계값 = {:.6f}(이번 배치 최적 F1 지점)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="303"/>
        <source>  漏检 {} 张(不良判成良品), 误检 {} 张</source>
        <translation>  미검출 {}장(이상을 정상으로 판정), 오검출 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="307"/>
        <source>  AUROC 无法计算</source>
        <translation>  AUROC를 계산할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_train_runner.py" line="321"/>
        <source>模型已保存: {} ({:.0f} MB)</source>
        <translation>모델 저장됨: {} ({:.0f} MB)</translation>
    </message>
</context>
<context>
    <name>AddLabelDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="168"/>
        <source>添加标签</source>
        <translation>라벨 추가</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="185"/>
        <source>编辑标签</source>
        <translation>라벨 편집</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="187"/>
        <source>标签名称</source>
        <translation>라벨 이름</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="222"/>
        <source>标签名称, 多个用逗号分隔</source>
        <translation>라벨 이름, 여러 개는 쉼표로 구분</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="224"/>
        <source>导入</source>
        <translation>가져오기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="231"/>
        <source>选择数据集...</source>
        <translation>데이터셋 선택...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="254"/>
        <location filename="../app/annotation/annotation_dialog.py" line="259"/>
        <source>导入标签</source>
        <translation>라벨 가져오기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="255"/>
        <source>请先选择一个数据集</source>
        <translation>먼저 데이터셋을 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="260"/>
        <source>数据集&quot;{}&quot;还没有标签</source>
        <translation>데이터셋 &quot;{}&quot;에 아직 라벨이 없습니다</translation>
    </message>
</context>
<context>
    <name>AnnotationDialog</name>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="208"/>
        <source>复制</source>
        <translation>복사</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="210"/>
        <source>填充</source>
        <translation>채우기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="220"/>
        <source>粘贴</source>
        <translation>붙여넣기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="374"/>
        <source>标注 - {} / {}</source>
        <translation>어노테이션 - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="392"/>
        <location filename="../app/annotation/annotation_dialog.py" line="874"/>
        <source>矩形</source>
        <translation>사각형</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="393"/>
        <location filename="../app/annotation/annotation_dialog.py" line="880"/>
        <source>多边形</source>
        <translation>다각형</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="402"/>
        <source>标签列表</source>
        <translation>라벨 목록</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="403"/>
        <source>标注信息</source>
        <translation>어노테이션 정보</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="407"/>
        <source>上一张</source>
        <translation>이전</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="408"/>
        <source>下一张</source>
        <translation>다음</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="443"/>
        <source>只在选中的多边形框内生效; A/D 切图或 Ctrl+S 才写盘</source>
        <translation>선택한 다각형 안에서만 적용됩니다. A/D로 이미지를 전환하거나 Ctrl+S를 눌러야 디스크에 저장됩니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="481"/>
        <source>显示标注</source>
        <translation>어노테이션 표시</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="487"/>
        <source>文本标注</source>
        <translation>텍스트 어노테이션</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="713"/>
        <source>编辑标签</source>
        <translation>라벨 편집</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1032"/>
        <source>转换</source>
        <translation>변환</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1033"/>
        <source>设置像素精度, 在像素面积后显示物理面积</source>
        <translation>픽셀 정밀도를 설정하면 픽셀 면적 뒤에 물리 면적이 표시됩니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="1037"/>
        <source>当前像素精度 {}, 点击修改</source>
        <translation>현재 픽셀 정밀도 {}, 클릭하여 수정</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="563"/>
        <source>先在画布上点选一个多边形</source>
        <translation>먼저 캔버스에서 다각형을 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="566"/>
        <source>亮度调节只对多边形有效</source>
        <translation>밝기 조절은 다각형에만 적용됩니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="326"/>
        <source>    类别: {}</source>
        <translation>    클래스: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="354"/>
        <source>删除本地文件</source>
        <translation>로컬 파일 삭제</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="355"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="357"/>
        <location filename="../app/annotation/annotation_io.py" line="366"/>
        <source>删除图像</source>
        <translation>이미지 삭제</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="358"/>
        <source>是否删除当前图像?

{}</source>
        <translation>현재 이미지를 삭제하시겠습니까?

{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="361"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>이미지와 같은 이름의 라벨 파일이 디스크에서 삭제되며 복구할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="367"/>
        <source>无法访问主窗口, 删除失败</source>
        <translation>메인 창에 접근할 수 없어 삭제에 실패했습니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="380"/>
        <source>(无图像)</source>
        <translation>(이미지 없음)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="696"/>
        <location filename="../app/annotation/annotation_dialog.py" line="820"/>
        <location filename="../app/annotation/annotation_dialog.py" line="826"/>
        <source>添加标签</source>
        <translation>라벨 추가</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="697"/>
        <source>请先添加标签(点击&quot;+&quot;)</source>
        <translation>먼저 라벨을 추가하세요(&quot;+&quot; 클릭)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="733"/>
        <source>标注文字</source>
        <translation>어노테이션 텍스트</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="734"/>
        <source>请输入框内的文字</source>
        <translation>상자 안의 텍스트를 입력하세요</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="846"/>
        <source>剪切板  {}/{}</source>
        <translation>클립보드  {}/{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="871"/>
        <source>第 {} 个模板  {}x{}
左键选中用于粘贴, 右键 删除/导入/导出/清空</source>
        <translation>{}번째 템플릿  {}x{}
왼쪽 클릭으로 붙여넣기 대상을 선택하고, 오른쪽 클릭으로 삭제/가져오기/내보내기/비우기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="903"/>
        <location filename="../app/annotation/annotation_dialog.py" line="685"/>
        <source>删除</source>
        <translation>삭제</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="906"/>
        <source>导入</source>
        <translation>가져오기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="907"/>
        <source>导出</source>
        <translation>내보내기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="909"/>
        <source>清空</source>
        <translation>비우기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="420"/>
        <location filename="../app/annotation/annotation_io.py" line="449"/>
        <location filename="../app/annotation/annotation_io.py" line="454"/>
        <source>导出剪切板</source>
        <translation>클립보드 내보내기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="421"/>
        <source>剪切板是空的, 没有可导出的模板</source>
        <translation>클립보드가 비어 있어 내보낼 템플릿이 없습니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="424"/>
        <source>选择导出目录</source>
        <translation>내보내기 디렉터리 선택</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="450"/>
        <source>导出中断: {}
(已写出 {} 个)</source>
        <translation>내보내기 중단: {}
({}개 작성됨)</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="455"/>
        <source>已导出 {} 个模板(png + 同名 json)到:
{}</source>
        <translation>템플릿 {}개(png + 같은 이름 json)를 다음 위치로 내보냈습니다:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="461"/>
        <source>选择导入目录</source>
        <translation>가져오기 디렉터리 선택</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="468"/>
        <location filename="../app/annotation/annotation_io.py" line="472"/>
        <location filename="../app/annotation/annotation_io.py" line="506"/>
        <source>导入剪切板</source>
        <translation>클립보드 가져오기</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="469"/>
        <source>读取目录失败: {}</source>
        <translation>디렉터리를 읽지 못했습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="473"/>
        <source>这个目录里没有 png 文件</source>
        <translation>이 디렉터리에 png 파일이 없습니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="501"/>
        <source>已导入 {} 个模板到剪切板</source>
        <translation>템플릿 {}개를 클립보드로 가져왔습니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="503"/>
        <source>
其中 {} 个没有同名 json, 按矩形导入</source>
        <translation>
그중 {}개는 같은 이름의 json이 없어 사각형으로 가져왔습니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="505"/>
        <source>
{} 个文件读不出来, 已跳过</source>
        <translation>
{}개 파일을 읽지 못해 건너뛰었습니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="622"/>
        <source>修改类别</source>
        <translation>클래스 수정</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="623"/>
        <source>移动图像文件失败:
{}</source>
        <translation>이미지 파일 이동 실패:
{}</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="684"/>
        <source>编辑</source>
        <translation>편집</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="780"/>
        <location filename="../app/annotation/annotation_dialog.py" line="787"/>
        <location filename="../app/annotation/annotation_io.py" line="524"/>
        <source>删除标签</source>
        <translation>라벨 삭제</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_io.py" line="525"/>
        <source>正在统计标注文件...</source>
        <translation>라벨 파일 집계 중...</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="781"/>
        <source>标签&quot;{}&quot;已有 {} 处标注, 删除后这些标注将被一并删除且不可恢复.
确定删除吗?</source>
        <translation>라벨 &quot;{}&quot;에 어노테이션 {}개가 있습니다. 삭제하면 해당 어노테이션도 함께 삭제되며 복구할 수 없습니다.
삭제하시겠습니까?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="788"/>
        <source>确定删除标签&quot;{}&quot;吗?</source>
        <translation>라벨 &quot;{}&quot;을(를) 삭제하시겠습니까?</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="714"/>
        <location filename="../app/annotation/annotation_dialog.py" line="821"/>
        <source>标签名称不能为空</source>
        <translation>라벨 이름은 비워둘 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="881"/>
        <source>{} 个顶点</source>
        <translation>꼭짓점 {}개</translation>
    </message>
</context>
<context>
    <name>App</name>
    <message>
        <location filename="../app/main_window.py" line="55"/>
        <source>软件启动</source>
        <translation>소프트웨어 시작</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="58"/>
        <source>软件退出</source>
        <translation>소프트웨어 종료</translation>
    </message>
    <message>
        <location filename="../app/main_window.py" line="60"/>
        <source>软件退出前停止训练</source>
        <translation>소프트웨어 종료 전 학습 중지</translation>
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
        <translation>프로젝트</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="193"/>
        <source>添加项目</source>
        <translation>프로젝트 추가</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="196"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="335"/>
        <source>项目训练中</source>
        <translation>학습 중</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="365"/>
        <source>停止训练</source>
        <translation>학습 중지</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="372"/>
        <source>剩余时间:</source>
        <translation>남은 시간:</translation>
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
        <translation>통계</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="406"/>
        <source>训练</source>
        <translation>학습</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="413"/>
        <source>模型</source>
        <translation>모델</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="420"/>
        <location filename="../app/mixins/queue_mixin.py" line="368"/>
        <source>队列</source>
        <translation>대기열</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="427"/>
        <source>日志</source>
        <translation>로그</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="446"/>
        <source>界面语言</source>
        <translation>인터페이스 언어</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="537"/>
        <source>上一页</source>
        <translation>이전</translation>
    </message>
    <message>
        <location filename="../ui/app.ui" line="566"/>
        <source>下一页</source>
        <translation>다음</translation>
    </message>
</context>
<context>
    <name>Charts</name>
    <message>
        <location filename="../app/widgets/charts.py" line="12"/>
        <source>暂无标注</source>
        <translation>어노테이션 없음</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="13"/>
        <source>标签</source>
        <translation>라벨</translation>
    </message>
    <message>
        <location filename="../app/widgets/charts.py" line="14"/>
        <source>标签数量</source>
        <translation>라벨 수</translation>
    </message>
</context>
<context>
    <name>ClassifyTestRunner</name>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="33"/>
        <source>缺少测试依赖: {}</source>
        <translation>테스트 의존성이 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="85"/>
        <source>加载分类模型: {}</source>
        <translation>분류 모델 불러오기: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_test_runner.py" line="110"/>
        <source>测试图片 {} 张</source>
        <translation>테스트 이미지 {}장</translation>
    </message>
</context>
<context>
    <name>ClassifyTrainRunner</name>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="40"/>
        <source>缺少训练依赖: {}</source>
        <translation>학습 의존성이 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="132"/>
        <source>输出路径: {}</source>
        <translation>출력 경로: {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="133"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>이번 학습 출력 디렉터리(타임스탬프): {}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="149"/>
        <source>分类训练: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</source>
        <translation>분류 학습: model={} classes={} device={} epochs={} batch={} lr={} img={} optimizer={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="158"/>
        <source>数据准备: train={} 张, val={} 张</source>
        <translation>데이터 준비: train={}장, val={}장</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="160"/>
        <source>训练集无图像, 请检查数据集</source>
        <translation>학습 세트에 이미지가 없습니다. 데이터셋을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="162"/>
        <source>验证集无图像, 请检查数据集</source>
        <translation>검증 세트에 이미지가 없습니다. 데이터셋을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="187"/>
        <source>未从数据集中解析到任何类别(子文件夹),无法训练图像分类</source>
        <translation>데이터셋에서 클래스(하위 폴더)를 분석하지 못해 이미지 분류를 학습할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="197"/>
        <source>数据集: train={} val={} 类别({})={}</source>
        <translation>데이터셋: train={} val={} 클래스({})={}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="284"/>
        <source>早停触发: 连续 {} 个 epoch 精度无提升</source>
        <translation>조기 중단 발동: {} epoch 연속 정확도 향상 없음</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="289"/>
        <source>训练完成 best_acc={:.4f}</source>
        <translation>학습 완료 best_acc={:.4f}</translation>
    </message>
    <message>
        <location filename="../app/train/classify_train_runner.py" line="297"/>
        <source>生成类别文件: {}</source>
        <translation>클래스 파일 생성: {}</translation>
    </message>
</context>
<context>
    <name>CollapsibleText</name>
    <message>
        <location filename="../app/widgets/collapsible_text.py" line="57"/>
        <source>点击展开 / 收起完整内容</source>
        <translation>클릭하여 펼치기 / 접기</translation>
    </message>
</context>
<context>
    <name>ColorPickerDialog</name>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="395"/>
        <source>选择颜色</source>
        <translation>색상 선택</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="407"/>
        <source>十六进制:</source>
        <translation>16진수:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="428"/>
        <source>基本颜色:</source>
        <translation>기본 색상:</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_canvas.py" line="440"/>
        <source>自定义 RGB:</source>
        <translation>사용자 지정 RGB:</translation>
    </message>
</context>
<context>
    <name>CompareDialog</name>
    <message>
        <location filename="../ui/compare.ui" line="14"/>
        <source>对比多次训练</source>
        <translation>여러 학습 비교</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="22"/>
        <source>对比指标</source>
        <translation>비교 지표</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="38"/>
        <source>记录范围</source>
        <translation>기록 범위</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="65"/>
        <location filename="../app/widgets/compare_dialog.py" line="695"/>
        <location filename="../app/widgets/compare_dialog.py" line="699"/>
        <location filename="../app/widgets/compare_dialog.py" line="716"/>
        <source>导出对比报告</source>
        <translation>비교 보고서 내보내기</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="72"/>
        <location filename="../app/widgets/compare_dialog.py" line="723"/>
        <location filename="../app/widgets/compare_dialog.py" line="727"/>
        <source>删除选中</source>
        <translation>선택 항목 삭제</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="97"/>
        <source>训练记录（可勾选，上限 8 条）</source>
        <translation>학습 기록(선택 가능, 최대 8개)</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="168"/>
        <source>关键指标汇总</source>
        <translation>주요 지표 요약</translation>
    </message>
    <message>
        <location filename="../ui/compare.ui" line="188"/>
        <source>差异与结论</source>
        <translation>차이와 결론</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="320"/>
        <source>勾选要对比的训练记录(最多 {} 条), 双击查看单次指标</source>
        <translation>비교할 학습 기록을 선택하세요(최대 {} 개), 더블클릭하면 단일 지표를 봅니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="295"/>
        <source>数据来源：LMDB train_history + metrics.csv / metrics json</source>
        <translation>데이터 출처: LMDB train_history + metrics.csv / metrics json</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="516"/>
        <source>一次最多对比 {} 条记录</source>
        <translation>한 번에 최대 {} 개까지 비교할 수 있습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="544"/>
        <source>{} 训练曲线（按 epoch）</source>
        <translation>{} 학습 곡선(epoch별)</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="551"/>
        <source>已选 {} 条（上限 {}）</source>
        <translation>{}개 선택(최대 {})</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="553"/>
        <source>已选 {} 条(上限 {}), 双击左侧记录可查看单次指标</source>
        <translation>{} 개 선택됨(상한 {}), 왼쪽 기록을 더블클릭하면 단일 지표를 봅니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="555"/>
        <location filename="../app/widgets/compare_dialog.py" line="581"/>
        <source>勾选左侧的训练记录后这里显示对比曲线</source>
        <translation>왼쪽에서 학습 기록을 선택하면 여기에 비교 곡선이 표시됩니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="649"/>
        <source>无</source>
        <translation>없음</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="662"/>
        <source>至少勾选 2 条记录&lt;br&gt;才能比较差异</source>
        <translation>차이를 비교하려면&lt;br&gt;2개 이상 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="696"/>
        <source>当前没有可导出的对比图表</source>
        <translation>내보낼 비교 차트가 없습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="700"/>
        <source>PNG 图片 (*.png)</source>
        <translation>PNG 이미지 (*.png)</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="714"/>
        <source>已导出: {}
{}</source>
        <translation>내보냄: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="717"/>
        <source>导出失败: {}</source>
        <translation>내보내기 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="724"/>
        <source>请先勾选要删除的训练记录</source>
        <translation>삭제할 학습 기록을 먼저 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="728"/>
        <source>确定删除选中的 {} 条训练记录? 对应指标文件会一并删除.</source>
        <translation>선택한 {}개의 학습 기록을 삭제할까요? 해당 지표 파일도 함께 삭제됩니다.</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_dialog.py" line="585"/>
        <source>所选记录没有&quot;{}&quot;的数据</source>
        <translation>선택한 기록에 &quot;{}&quot; 데이터가 없습니다</translation>
    </message>
</context>
<context>
    <name>DataPrep</name>
    <message>
        <location filename="../app/train/data_prep.py" line="189"/>
        <source>解析到类别 {} 个: {}</source>
        <translation>클래스 {}개 분석: {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="209"/>
        <source>复制数据集 {}: 图像 {} 张, 标签 {} 个 → {}</source>
        <translation>데이터셋 {} 복사: 이미지 {}장, 라벨 {}개 → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="296"/>
        <source>合并 {} 数据集 → {} ({} 个文件)</source>
        <translation>{} 데이터셋 병합 → {} ({}개 파일)</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="313"/>
        <source>生成 data.yaml → {}</source>
        <translation>data.yaml 생성 → {}</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="326"/>
        <source>未从数据集中解析到任何标签类别, 请检查标签文件</source>
        <translation>데이터셋에서 라벨 클래스를 분석하지 못했습니다. 라벨 파일을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/data_prep.py" line="333"/>
        <source>数据准备完成: {} 个类别, 输出目录 {}</source>
        <translation>데이터 준비 완료: {}개 클래스, 출력 디렉터리 {}</translation>
    </message>
</context>
<context>
    <name>DatasetViewMixin</name>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="261"/>
        <source>删除全部未标注图像({} 张)</source>
        <translation>미라벨 이미지 모두 삭제({}장)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="267"/>
        <source>删除所选图像({} 张)</source>
        <translation>선택한 이미지 삭제({}장)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="381"/>
        <source>重载跳过: 数据集 {}/{} 无图像目录</source>
        <translation>다시 불러오기 건너뜀: 데이터셋 {}/{}에 이미지 디렉터리가 없습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="382"/>
        <source>重载</source>
        <translation>다시 불러오기</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="383"/>
        <source>该数据集还没有图像目录, 请先右键&quot;导入&quot;</source>
        <translation>이 데이터셋에는 아직 이미지 디렉터리가 없습니다. 먼저 마우스 오른쪽 버튼으로 &quot;가져오기&quot;를 실행하세요</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="387"/>
        <source>重载跳过: 数据集 {}/{} 正在载入</source>
        <translation>다시 불러오기 건너뜀: 데이터셋 {}/{} 불러오는 중</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="389"/>
        <source>重载数据集: {}/{}</source>
        <translation>데이터셋 다시 불러오기: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="598"/>
        <source>数据集 {}/{} 含 OCR 文本标注, 已标为字符检测数据集</source>
        <translation>데이터셋 {}/{}에 OCR 텍스트 어노테이션이 있어 텍스트 검출 데이터셋으로 표시했습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="880"/>
        <source>第 {} / {} 页</source>
        <translation>{} / {} 페이지</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="884"/>
        <source>第 {}/{} 页 · 共 {} 个</source>
        <translation>{}/{} 페이지 · 총 {}개</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="886"/>
        <source>第 {}/{} 页 · 共 {} 张</source>
        <translation>{}/{} 페이지 · 총 {}장</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="899"/>
        <source>未选择标签</source>
        <translation>선택된 라벨 없음</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="901"/>
        <source>暂无数据</source>
        <translation>데이터 없음</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="938"/>
        <source>开始导入: {}/{} | 图像路径={} | 标签路径={} | 格式={}</source>
        <translation>가져오기 시작: {}/{} | 이미지 경로={} | 라벨 경로={} | 형식={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="939"/>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1008"/>
        <source>(无)</source>
        <translation>(없음)</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1003"/>
        <source>{}: {}个</source>
        <translation>{}: {}개</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1005"/>
        <source>数据集导入完成: {}/{} | 图像 {} 张, 已标注 {} 张 | 标签({}类): {}</source>
        <translation>데이터셋 가져오기 완료: {}/{} | 이미지 {}장, 라벨링 {}장 | 라벨({}개 클래스): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/dataset_view_mixin.py" line="1050"/>
        <source>数据集 {}/{} 未导入, 右键&quot;导入&quot;选择图像与标签目录</source>
        <translation>데이터셋 {}/{}은(는) 가져오지 않았습니다. 마우스 오른쪽 버튼의 &quot;가져오기&quot;로 이미지와 라벨 디렉터리를 선택하세요</translation>
    </message>
</context>
<context>
    <name>Dialog</name>
    <message>
        <location filename="../ui/dataset_properties.ui" line="14"/>
        <source>数据集属性</source>
        <translation>데이터셋 속성</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="30"/>
        <source>选择数据:</source>
        <translation>데이터 선택:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="53"/>
        <source>确定</source>
        <translation>확인</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="77"/>
        <source>图像路径:</source>
        <translation>이미지 경로:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="98"/>
        <source>标签路径:</source>
        <translation>라벨 경로:</translation>
    </message>
    <message>
        <location filename="../ui/dataset_properties.ui" line="119"/>
        <source>标签分布:</source>
        <translation>라벨 분포:</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="14"/>
        <source>导出</source>
        <translation>내보내기</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="36"/>
        <source>请选择导出路径</source>
        <translation>내보낼 경로를 선택하세요</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="90"/>
        <source>导出格式</source>
        <translation>내보내기 형식</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="106"/>
        <source>labelme 格式</source>
        <translation>labelme 형식</translation>
    </message>
    <message>
        <location filename="../ui/export_data.ui" line="119"/>
        <source>yolo 格式</source>
        <translation>yolo 형식</translation>
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
        <translation>확인</translation>
    </message>
    <message>
        <location filename="../app/widgets/dialog_buttons.py" line="116"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
</context>
<context>
    <name>DiffPanel</name>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="107"/>
        <source>最佳记录</source>
        <translation>최고 기록</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="108"/>
        <source>按 {}</source>
        <translation>{} 기준</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="126"/>
        <source>参数差异</source>
        <translation>파라미터 차이</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="126"/>
        <source>仅列取值不同的项</source>
        <translation>값이 다른 항목만 표시</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="135"/>
        <source>所选记录参数完全一致</source>
        <translation>선택한 기록의 파라미터가 완전히 같습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="144"/>
        <source>共同</source>
        <translation>공통</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="174"/>
        <source>结论</source>
        <translation>결론</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="189"/>
        <source>最佳</source>
        <translation>최고</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="199"/>
        <source>它独有的设置</source>
        <translation>이 기록만의 설정</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="203"/>
        <source>启用增强 {}/{} 条</source>
        <translation>증강 활성화 {}/{}개</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="206"/>
        <source>所选记录都没有启用数据增强</source>
        <translation>선택한 기록은 모두 데이터 증강을 사용하지 않았습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="211"/>
        <source>仍在训练</source>
        <translation>학습 중</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="213"/>
        <source>曲线未收敛， 对比仅供参考</source>
        <translation>곡선이 수렴하지 않음， 참고용</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="218"/>
        <source>未跑完</source>
        <translation>미완료</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="218"/>
        <source>不参与最佳判定</source>
        <translation>최고 판정 제외</translation>
    </message>
    <message>
        <location filename="../app/widgets/compare_diff.py" line="221"/>
        <source>训练时长</source>
        <translation>학습 시간</translation>
    </message>
</context>
<context>
    <name>ImportData</name>
    <message>
        <location filename="../ui/import_data.ui" line="14"/>
        <source>导入数据</source>
        <translation>데이터 가져오기</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="33"/>
        <source>图像路径</source>
        <translation>이미지 경로</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="73"/>
        <source>标签路径</source>
        <translation>라벨 경로</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="107"/>
        <source>标签格式:</source>
        <translation>라벨 형식:</translation>
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
        <translation>하위 폴더 기준 분류로 가져오기</translation>
    </message>
    <message>
        <location filename="../ui/import_data.ui" line="155"/>
        <source>提示信息</source>
        <translation>정보</translation>
    </message>
</context>
<context>
    <name>ImportExportMixin</name>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="59"/>
        <source>导入数据 - {} / {}</source>
        <translation>데이터 가져오기 - {} / {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="66"/>
        <location filename="../app/mixins/import_export_mixin.py" line="166"/>
        <source>请选择图像文件夹</source>
        <translation>이미지 폴더를 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="142"/>
        <source>请选择分类根目录(子文件夹名=类别)</source>
        <translation>분류 루트 디렉터리를 선택하세요(하위 폴더 이름 = 클래스)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="155"/>
        <source>(根目录)</source>
        <translation>(루트 디렉터리)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="157"/>
        <source>所选文件夹下无分类子文件夹或图像</source>
        <translation>선택한 폴더에 분류 하위 폴더나 이미지가 없습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="159"/>
        <source>{}: {}张</source>
        <translation>{}: {}장</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="161"/>
        <source>检测到 {} 类: {}</source>
        <translation>{}개 클래스 감지: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="80"/>
        <source>所选文件夹无图像</source>
        <translation>선택한 폴더에 이미지가 없습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="83"/>
        <source>共 {} 张图像, 已标注 {} 张</source>
        <translation>이미지 {}장, 라벨링 {}장</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="99"/>
        <source>(检测到 {} 张 {} 标签, 请切换上方格式为&quot;{}&quot;)</source>
        <translation>({}개의 {} 라벨이 감지되었습니다. 위 형식을 &quot;{}&quot;으로 전환하세요)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="103"/>
        <source>共 {} 张图像, 已标注 0 张 {}</source>
        <translation>이미지 {}장, 라벨링 0장 {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="105"/>
        <source>共 {} 张图像(标签目录无匹配文件)</source>
        <translation>이미지 {}장(라벨 디렉터리에 일치하는 파일 없음)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="172"/>
        <source>选择文件夹</source>
        <translation>폴더 선택</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="212"/>
        <source>分类根目录(子文件夹名=类别)</source>
        <translation>분류 루트 디렉터리(하위 폴더 이름 = 클래스)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="212"/>
        <source>图像路径</source>
        <translation>이미지 경로</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="234"/>
        <location filename="../app/mixins/import_export_mixin.py" line="237"/>
        <source>导入数据</source>
        <translation>데이터 가져오기</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="234"/>
        <source>请先选择有效的图像文件夹</source>
        <translation>먼저 유효한 이미지 폴더를 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="237"/>
        <source>标签路径无效</source>
        <translation>라벨 경로가 유효하지 않습니다</translation>
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
        <translation>내보내기</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="298"/>
        <source>请先在左侧选中要导出的数据集</source>
        <translation>먼저 왼쪽에서 내보낼 데이터셋을 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="311"/>
        <source>打开</source>
        <translation>열기</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="322"/>
        <source>请先选择导出保存位置</source>
        <translation>먼저 내보낼 저장 위치를 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="333"/>
        <source>开始导出: 项目={} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>내보내기 시작: 프로젝트={} | 원본 경로={} | 저장 경로={} | 형식={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="339"/>
        <source>正在导出项目...</source>
        <translation>프로젝트 내보내는 중...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="350"/>
        <source>项目&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>프로젝트 &quot;{}&quot; 내보내기 완료, 이미지 {}장 복사됨
위치: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="352"/>
        <source>导出项目完成: {} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>프로젝트 내보내기 완료: {} | 이미지 {}장 | 라벨({}) | 형식={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="358"/>
        <source>开始导出: 数据集={}/{} | 源路径={} | 保存路径={} | 格式={}</source>
        <translation>내보내기 시작: 데이터셋={}/{} | 원본 경로={} | 저장 경로={} | 형식={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="362"/>
        <source>正在导出数据集...</source>
        <translation>데이터셋 내보내는 중...</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="372"/>
        <source>数据集&quot;{}&quot;导出完成, 共复制 {} 张图像
位置: {}</source>
        <translation>데이터셋 &quot;{}&quot; 내보내기 완료, 이미지 {}장 복사됨
위치: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="375"/>
        <source>导出数据集完成: {}/{} | {} 张图像 | 标签({}) | 格式={} | → {}</source>
        <translation>데이터셋 내보내기 완료: {}/{} | 이미지 {}장 | 라벨({}) | 형식={} | → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="380"/>
        <source>导出失败: 项目={} 数据集={} | {}</source>
        <translation>내보내기 실패: 프로젝트={} 데이터셋={} | {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="381"/>
        <source>(整个项目)</source>
        <translation>(프로젝트 전체)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="382"/>
        <source>导出失败</source>
        <translation>내보내기 실패</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="385"/>
        <source>选择导出保存位置</source>
        <translation>내보낼 저장 위치 선택</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="411"/>
        <source>{} =&gt; 标签:{}</source>
        <translation>{} =&gt; 라벨:{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="412"/>
        <location filename="../app/mixins/import_export_mixin.py" line="413"/>
        <source>(无)</source>
        <translation>(없음)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="420"/>
        <source>(无标签)</source>
        <translation>(라벨 없음)</translation>
    </message>
    <message>
        <location filename="../app/mixins/import_export_mixin.py" line="463"/>
        <source>正在导出: {}</source>
        <translation>내보내는 중: {}</translation>
    </message>
</context>
<context>
    <name>ImportTask</name>
    <message>
        <location filename="../app/tasks/import_task.py" line="109"/>
        <source>导入跳过 {}: {}</source>
        <translation>가져오기 건너뜀 {}: {}</translation>
    </message>
</context>
<context>
    <name>LabelFilter</name>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="60"/>
        <location filename="../app/widgets/label_filter_popup.py" line="451"/>
        <source>全选</source>
        <translation>전체 선택</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="464"/>
        <source>显示全部图像</source>
        <translation>모든 이미지 표시 중</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="466"/>
        <source>按所选标签过滤</source>
        <translation>선택한 라벨로 필터링 중</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="468"/>
        <source>未选择标签</source>
        <translation>라벨 미선택</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="533"/>
        <source>收起</source>
        <translation>접기</translation>
    </message>
    <message>
        <location filename="../app/widgets/label_filter_popup.py" line="534"/>
        <source>展开全部</source>
        <translation>모두 펼치기</translation>
    </message>
</context>
<context>
    <name>LabelMixin</name>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="88"/>
        <source>已选 {} 个</source>
        <translation>{}개 선택됨</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="89"/>
        <source>全选</source>
        <translation>전체 선택</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="91"/>
        <location filename="../app/mixins/label_mixin.py" line="108"/>
        <source>未选择标签</source>
        <translation>라벨 미선택</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="100"/>
        <location filename="../app/mixins/label_mixin.py" line="175"/>
        <source>未标注</source>
        <translation>미라벨</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="208"/>
        <source>重命名</source>
        <translation>이름 바꾸기</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="214"/>
        <source>合并标签</source>
        <translation>라벨 병합</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="215"/>
        <source>标签&quot;{}&quot;已存在.
确定把&quot;{}&quot;的所有标注合并到&quot;{}&quot;吗?
此操作会改写数据集源标签文件, 且不可恢复.</source>
        <translation>라벨 &quot;{}&quot;이(가) 이미 존재합니다.
&quot;{}&quot;의 모든 어노테이션을 &quot;{}&quot;에 병합하시겠습니까?
이 작업은 데이터셋 원본 라벨 파일을 다시 쓰며 복구할 수 없습니다.</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="270"/>
        <source>合并标签: {} → {} ({}/{}) | 启动后台文件合并, 完成后输出统计</source>
        <translation>라벨 병합: {} → {} ({}/{}) | 백그라운드에서 파일 병합을 시작했습니다. 완료 후 통계를 출력합니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="273"/>
        <source>重命名标签: {} → {} ({}/{})</source>
        <translation>라벨 이름 바꾸기: {} → {} ({}/{})</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="349"/>
        <source>{}: {}个</source>
        <translation>{}: {}개</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="352"/>
        <source>删除标签完成: {} | 修改 {} 个标签文件 | 删除后标签统计({}类): {}</source>
        <translation>라벨 삭제 완료: {} | 라벨 파일 {}개 수정 | 삭제 후 라벨 통계({}개 클래스): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="355"/>
        <location filename="../app/mixins/label_mixin.py" line="360"/>
        <location filename="../app/mixins/label_mixin.py" line="365"/>
        <source>(无)</source>
        <translation>(없음)</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="357"/>
        <source>合并标签: {} → {} | 修改 {} 个标签文件 | 合并后标签统计({}类): {}</source>
        <translation>라벨 병합: {} → {} | 라벨 파일 {}개 수정 | 병합 후 라벨 통계({}개 클래스): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="362"/>
        <source>合并标签: {} → {} | 无标签文件被修改 | 合并后标签统计({}类): {}</source>
        <translation>라벨 병합: {} → {} | 수정된 라벨 파일 없음 | 병합 후 라벨 통계({}개 클래스): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/label_mixin.py" line="456"/>
        <source>删除标签: {} ({}/{})</source>
        <translation>라벨 삭제: {} ({}/{})</translation>
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
        <translation>비우기</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="79"/>
        <location filename="../app/widgets/log_dialog.py" line="21"/>
        <source>日志</source>
        <translation>로그</translation>
    </message>
</context>
<context>
    <name>MessageBox</name>
    <message>
        <location filename="../app/widgets/message_box.py" line="274"/>
        <location filename="../app/widgets/message_box.py" line="302"/>
        <source>确定</source>
        <translation>확인</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="98"/>
        <source>详情已复制到剪贴板</source>
        <translation>세부 정보를 클립보드에 복사했습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="267"/>
        <source>关闭</source>
        <translation>닫기</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="269"/>
        <source>复制详情</source>
        <translation>세부 정보 복사</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="303"/>
        <location filename="../app/widgets/message_box.py" line="350"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
    <message>
        <location filename="../app/widgets/message_box.py" line="374"/>
        <source>取消中...</source>
        <translation>취소 중...</translation>
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
        <translation>정확도</translation>
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
        <translation>선택한 기록에 {} 데이터가 없습니다</translation>
    </message>
</context>
<context>
    <name>MetricsDialog</name>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="55"/>
        <source>训练指标</source>
        <translation>학습 지표</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="84"/>
        <source>标签筛选</source>
        <translation>라벨 필터</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="88"/>
        <source>全部指标</source>
        <translation>전체 지표</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="89"/>
        <source>全部标签-P</source>
        <translation>전체 라벨-P</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="90"/>
        <source>全部标签-R</source>
        <translation>전체 라벨-R</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="126"/>
        <source>暂无该标签的指标数据(训练完成后可查看)</source>
        <translation>이 라벨의 지표 데이터가 아직 없습니다(학습 완료 후 확인 가능)</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="174"/>
        <source>loss 值</source>
        <translation>loss 값</translation>
    </message>
    <message>
        <location filename="../app/widgets/metrics_dialog.py" line="175"/>
        <source>指标值 (mAP/P/R)</source>
        <translation>지표 값 (mAP/P/R)</translation>
    </message>
</context>
<context>
    <name>MiscMixin</name>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="54"/>
        <source>界面语言: {}</source>
        <translation>인터페이스 언어: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="115"/>
        <source>数据集统计</source>
        <translation>데이터셋 통계</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="124"/>
        <source>应用所选数据集</source>
        <translation>선택한 데이터셋 적용</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="215"/>
        <source>[{}/{}](未设置)</source>
        <translation>[{}/{}](미설정)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="218"/>
        <source>(未选择数据集)</source>
        <translation>(선택된 데이터셋 없음)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="338"/>
        <source>删除图像: {} 张 | 本地删除文件={} | 项目={}, 数据集={}</source>
        <translation>이미지 삭제: {}장 | 로컬 파일 삭제={} | 프로젝트={}, 데이터셋={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="376"/>
        <source>删除</source>
        <translation>삭제</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="377"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="379"/>
        <source>删除图像</source>
        <translation>이미지 삭제</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="380"/>
        <source>将从系统删除所选 {} 张图像?

(图像与同名标注文件不可恢复)</source>
        <translation>선택한 {}장의 이미지를 시스템에서 삭제하시겠습니까?

(이미지와 같은 이름의 라벨 파일은 복구할 수 없습니다)</translation>
    </message>
    <message>
        <location filename="../app/mixins/misc_mixin.py" line="384"/>
        <source>图像与同名标注文件将从磁盘删除, 不可恢复</source>
        <translation>이미지와 같은 이름의 라벨 파일이 디스크에서 삭제되며 복구할 수 없습니다</translation>
    </message>
</context>
<context>
    <name>ModelAssets</name>
    <message>
        <location filename="../app/core/model_assets.py" line="88"/>
        <location filename="../app/core/model_assets.py" line="122"/>
        <source>速度最快, 精度够用</source>
        <translation>가장 빠르고 정확도는 충분함</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="89"/>
        <location filename="../app/core/model_assets.py" line="126"/>
        <source>精度更好, 稍慢一些</source>
        <translation>정확도가 더 좋고 약간 느림</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="90"/>
        <location filename="../app/core/model_assets.py" line="130"/>
        <source>精度更高</source>
        <translation>정확도가 더 높음</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="91"/>
        <source>精度最高, 显存占用大</source>
        <translation>정확도가 가장 높지만 VRAM 사용량이 큼</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="92"/>
        <source>精度极致, 显存占用很大</source>
        <translation>정확도가 최고 수준, VRAM 사용량이 매우 큼</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="95"/>
        <location filename="../app/core/model_assets.py" line="141"/>
        <source>轻量分割</source>
        <translation>경량 세그멘테이션</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="96"/>
        <location filename="../app/core/model_assets.py" line="145"/>
        <source>速度与精度平衡</source>
        <translation>속도와 정확도의 균형</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="97"/>
        <location filename="../app/core/model_assets.py" line="149"/>
        <source>细节更完整</source>
        <translation>디테일이 더 완전함</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="98"/>
        <location filename="../app/core/model_assets.py" line="153"/>
        <source>最精细</source>
        <translation>가장 정밀함</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="99"/>
        <source>最精细, 显存占用很大</source>
        <translation>가장 정밀함, VRAM 사용량이 매우 큼</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="137"/>
        <source>结构与 medium 相同</source>
        <translation>medium와 동일한 구조</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="295"/>
        <source>文件不存在: {}</source>
        <translation>파일이 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="298"/>
        <source>只支持 {} 格式</source>
        <translation>{} 형식만 지원합니다</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="303"/>
        <source>读不到文件大小: {}</source>
        <translation>파일 크기를 읽을 수 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="305"/>
        <source>文件只有 {}, 不像完整的权重</source>
        <translation>파일이 {}뿐이라 완전한 가중치 파일로 보이지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="316"/>
        <source>这看着是 Transformer 权重, 当前档位是 CNN(YOLO)</source>
        <translation>Transformer 가중치로 보이지만 현재 선택은 CNN(YOLO)입니다</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="320"/>
        <source>这看着是 CNN(YOLO) 权重, 当前档位是 Transformer</source>
        <translation>CNN(YOLO) 가중치로 보이지만 현재 선택은 Transformer입니다</translation>
    </message>
    <message>
        <location filename="../app/core/model_assets.py" line="340"/>
        <source>权重目录不可写: {}</source>
        <translation>가중치 디렉터리에 쓸 수 없습니다: {}</translation>
    </message>
</context>
<context>
    <name>ModelDialog</name>
    <message>
        <location filename="../ui/model.ui" line="14"/>
        <location filename="../app/widgets/model_dialog.py" line="190"/>
        <source>模型管理</source>
        <translation>모델 관리</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="28"/>
        <source>搜索项目 / 数据集 / 标签</source>
        <translation>프로젝트 / 데이터셋 / 라벨 검색</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="39"/>
        <source>全部任务</source>
        <translation>전체 작업</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="44"/>
        <source>检测</source>
        <translation>객체 검출</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="49"/>
        <source>分割</source>
        <translation>세그멘테이션</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="54"/>
        <source>分类</source>
        <translation>분류</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="66"/>
        <source>全部状态</source>
        <translation>전체 상태</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="71"/>
        <source>已完成</source>
        <translation>완료</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="76"/>
        <source>训练中</source>
        <translation>학습 중</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="81"/>
        <source>失败</source>
        <translation>실패</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="86"/>
        <source>已停止</source>
        <translation>중지됨</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="94"/>
        <source>仅看每个数据集最佳</source>
        <translation>데이터셋별 최고 성능만 보기</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="114"/>
        <source>共 0 条</source>
        <translation>총 0건</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="135"/>
        <location filename="../app/widgets/model_dialog.py" line="629"/>
        <source>任务</source>
        <translation>작업</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="140"/>
        <source>数据集 / 标签</source>
        <translation>데이터셋 / 라벨</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="145"/>
        <location filename="../app/widgets/model_dialog.py" line="633"/>
        <source>精度</source>
        <translation>정확도</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="150"/>
        <location filename="../app/widgets/model_dialog.py" line="644"/>
        <source>训练时间</source>
        <translation>학습 시각</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="155"/>
        <location filename="../app/widgets/model_dialog.py" line="646"/>
        <source>耗时</source>
        <translation>소요 시간</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="160"/>
        <location filename="../app/widgets/model_dialog.py" line="636"/>
        <source>图像尺寸</source>
        <translation>이미지 크기</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="165"/>
        <source>操作</source>
        <translation>작업</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="184"/>
        <source>模型详情</source>
        <translation>모델 상세</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="191"/>
        <location filename="../app/widgets/model_dialog.py" line="612"/>
        <source>选中一行查看详情</source>
        <translation>행을 선택하면 상세 정보를 볼 수 있습니다</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="220"/>
        <source>查看完整指标</source>
        <translation>전체 지표 보기</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="227"/>
        <location filename="../app/widgets/model_dialog.py" line="756"/>
        <source>对比多次训练</source>
        <translation>여러 학습 비교</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="234"/>
        <source>按此配置重训</source>
        <translation>이 구성으로 재학습</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="241"/>
        <source>打开模型目录</source>
        <translation>모델 디렉터리 열기</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="281"/>
        <source>上一页</source>
        <translation>이전</translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="288"/>
        <source>1/1</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/model.ui" line="295"/>
        <source>下一页</source>
        <translation>다음</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="436"/>
        <source>共 {} 条</source>
        <translation>총 {}건</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="487"/>
        <source> 等 {} 类</source>
        <translation> 외 {}개 클래스</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="502"/>
        <source>测试</source>
        <translation>테스트</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="507"/>
        <source>导出</source>
        <translation>내보내기</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="512"/>
        <source>删除</source>
        <translation>삭제</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="626"/>
        <source>{} × {} 累积</source>
        <translation>{} × {} 누적</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="627"/>
        <source>状态</source>
        <translation>상태</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="634"/>
        <source>训练集</source>
        <translation>학습 세트</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="635"/>
        <source>验证集</source>
        <translation>검증 세트</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="637"/>
        <source>轮数 / 早停</source>
        <translation>에포크 / 조기 중단</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="639"/>
        <source>批大小</source>
        <translation>배치 크기</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="640"/>
        <source>学习率</source>
        <translation>학습률</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="641"/>
        <source>优化器</source>
        <translation>옵티마이저</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="642"/>
        <source>设备</source>
        <translation>장치</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="643"/>
        <source>标签</source>
        <translation>라벨</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="647"/>
        <source>模型路径</source>
        <translation>모델 경로</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="663"/>
        <source>失败原因</source>
        <translation>실패 원인</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="679"/>
        <source>暂无曲线</source>
        <translation>곡선 없음</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="703"/>
        <source>{}  最佳 {:.3f}</source>
        <translation>{}  최고 {:.3f}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="711"/>
        <location filename="../app/widgets/model_dialog.py" line="722"/>
        <source>打开目录</source>
        <translation>디렉터리 열기</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="712"/>
        <source>模型目录不存在:
{}</source>
        <translation>모델 디렉터리가 없습니다:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="740"/>
        <source>[model_dialog] 打开指标失败: {}
{}</source>
        <translation>[model_dialog] 지표 열기 실패: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="742"/>
        <source>查看指标失败</source>
        <translation>지표를 열지 못했습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="757"/>
        <source>当前没有可对比的训练记录</source>
        <translation>비교할 학습 기록이 없습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="764"/>
        <source>[model_dialog] 打开对比失败: {}
{}</source>
        <translation>[model_dialog] 비교 열기 실패: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="766"/>
        <source>打开对比失败</source>
        <translation>비교 열기 실패</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="773"/>
        <source>删除模型记录</source>
        <translation>모델 기록 삭제</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="774"/>
        <source>确定删除该条模型记录?
项目={}
数据集={}
开始时间={}
</source>
        <translation>이 모델 기록을 삭제하시겠습니까?
프로젝트={}
데이터셋={}
시작 시간={}
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="778"/>
        <source>删除模型记录: 项目={} 数据集={} 任务={} 开始时间={}</source>
        <translation>모델 기록 삭제: 프로젝트={} 데이터셋={} 작업={} 시작 시간={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="792"/>
        <source>删除模型记录失败: {} | {}</source>
        <translation>모델 기록 삭제 실패: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="793"/>
        <source>[model_dialog] 删除失败: {}
{}</source>
        <translation>[model_dialog] 삭제 실패: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="802"/>
        <source>[model_dialog] 打开训练失败: {}
{}</source>
        <translation>[model_dialog] 학습 열기 실패: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="803"/>
        <source>打开训练失败</source>
        <translation>학습 열기 실패</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="828"/>
        <source>[model_dialog] 打开测试失败: {}
{}</source>
        <translation>[model_dialog] 테스트 열기 실패: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="830"/>
        <source>打开测试失败</source>
        <translation>테스트 열기 실패</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="848"/>
        <location filename="../app/widgets/model_dialog.py" line="866"/>
        <location filename="../app/widgets/model_dialog.py" line="882"/>
        <location filename="../app/widgets/model_dialog.py" line="1173"/>
        <location filename="../app/widgets/model_dialog.py" line="1183"/>
        <source>导出模型</source>
        <translation>모델 내보내기</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="849"/>
        <source>模型文件不存在:
{}</source>
        <translation>모델 파일이 없습니다:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="850"/>
        <source>导出模型失败: 模型文件不存在 {}</source>
        <translation>모델 내보내기 실패: 모델 파일이 없습니다 {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="852"/>
        <source>选择导出目录</source>
        <translation>내보내기 디렉터리 선택</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="867"/>
        <source>创建目录失败: {}</source>
        <translation>디렉터리 생성 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="868"/>
        <source>导出模型失败: 创建目录失败 {} | {}</source>
        <translation>모델 내보내기 실패: 디렉터리 생성 실패 {} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="878"/>
        <source>开始导出模型: 项目={} 任务={} 架构={} 尺寸={} | {}</source>
        <translation>모델 내보내기 시작: 프로젝트={} 작업={} 아키텍처={} 크기={} | {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="879"/>
        <location filename="../app/widgets/model_dialog.py" line="1033"/>
        <source>未知</source>
        <translation>알 수 없음</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="883"/>
        <source>正在导出 ONNX...</source>
        <translation>ONNX 내보내는 중...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="904"/>
        <source>正在导出模型包...</source>
        <translation>모델 패키지 내보내는 중...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="915"/>
        <source>导出模型包完成: 包含 {}</source>
        <translation>모델 패키지 내보내기 완료: 포함: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="922"/>
        <source>ONNX 导出完成: {} ({:.1f} MB)</source>
        <translation>ONNX 내보내기 완료: {} ({:.1f} MB)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="979"/>
        <source>读取词表失败: {}</source>
        <translation>어휘를 읽지 못했습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="990"/>
        <source>生成 vocab.txt 失败: {}</source>
        <translation>vocab.txt 생성 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1006"/>
        <source>生成 label_map.json 失败: {}</source>
        <translation>label_map.json 생성 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1012"/>
        <source>导出模型报告跳过: 分类任务不出评估报告</source>
        <translation>모델 보고서 내보내기 건너뜀: 분류 작업은 평가 보고서를 생성하지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1013"/>
        <source>分类任务不生成评估报告</source>
        <translation>분류 작업은 평가 보고서를 생성하지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1017"/>
        <source>导出模型报告跳过: 字符识别不出评估报告</source>
        <translation>모델 보고서 내보내기 건너뜀: 텍스트 인식은 평가 보고서를 만들지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1018"/>
        <source>字符识别不生成评估报告</source>
        <translation>텍스트 인식은 평가 보고서를 생성하지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1022"/>
        <source>导出模型报告跳过: 未找到验证集</source>
        <translation>모델 보고서 내보내기 건너뜀: 검증 세트를 찾지 못했습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1023"/>
        <source>未找到验证集, 已跳过评估报告</source>
        <translation>검증 세트를 찾지 못해 평가 보고서를 건너뛰었습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1025"/>
        <location filename="../app/widgets/model_dialog.py" line="1106"/>
        <source>正在生成模型报告...</source>
        <translation>모델 보고서 생성 중...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1029"/>
        <source>正在生成模型报告 {}/{}</source>
        <translation>모델 보고서 생성 중 {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1032"/>
        <source>导出模型评估失败: {}</source>
        <translation>모델 내보내기 평가 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1035"/>
        <source>评估失败, 已跳过报告: {}</source>
        <translation>평가 실패, 보고서 건너뜀: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1125"/>
        <source>导出模型报告跳过: 验证集没有标注</source>
        <translation>모델 보고서 내보내기 건너뜀: 검증 세트에 어노테이션이 없습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1126"/>
        <source>验证集没有标注, 已跳过评估报告</source>
        <translation>검증 세트에 어노테이션이 없어 평가 보고서를 건너뛰었습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1132"/>
        <source>[export] 生成评估报告失败:
{}</source>
        <translation>[export] 평가 보고서 생성 실패:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1129"/>
        <source>生成评估报告失败: {}</source>
        <translation>평가 보고서 생성 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="964"/>
        <source>读取类别表失败: {}</source>
        <translation>클래스 목록 읽기 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="965"/>
        <source>[export] 读取类别表失败: {}</source>
        <translation>[export] 클래스 목록 읽기 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1121"/>
        <source>导出模型报告完成: {}</source>
        <translation>모델 보고서 내보내기 완료: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1133"/>
        <source>评估完成, 但报告生成失败</source>
        <translation>평가는 완료되었지만 보고서 생성에 실패했습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1167"/>
        <source>导出模型完成: {} | 包含: {}</source>
        <translation>모델 내보내기 완료: {} | 포함: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1169"/>
        <source>已导出到:
{}

包含: {}</source>
        <translation>다음 위치로 내보냈습니다:
{}

포함: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1131"/>
        <location filename="../app/widgets/model_dialog.py" line="1180"/>
        <source>未知错误</source>
        <translation>알 수 없는 오류</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1184"/>
        <source>模型导出失败, 详情见日志</source>
        <translation>모델 내보내기에 실패했습니다. 자세한 내용은 로그를 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1179"/>
        <source>导出模型失败: {}</source>
        <translation>모델 내보내기 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1181"/>
        <source>[export] ONNX 导出失败: {}</source>
        <translation>[export] ONNX 내보내기 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1198"/>
        <source>复制导出示例失败: {}</source>
        <translation>내보내기 예제 복사 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_dialog.py" line="1199"/>
        <source>[export] 复制示例失败: {}</source>
        <translation>[export] 예제 복사 실패: {}</translation>
    </message>
</context>
<context>
    <name>ModelDownloader</name>
    <message>
        <location filename="../app/core/model_download.py" line="92"/>
        <source>权重目录不可写入, 请点&quot;更改&quot;换一个目录</source>
        <translation>가중치 디렉터리에 쓸 수 없습니다. &quot;변경&quot;을 눌러 다른 디렉터리를 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="101"/>
        <source>权重文件大小不符, 丢弃重下: {}</source>
        <translation>가중치 파일 크기가 일치하지 않아 삭제 후 다시 다운로드합니다: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="111"/>
        <source>开始下载权重 {} ({}, 已下载 {})</source>
        <translation>가중치 {} 다운로드 시작 ({}, 다운로드됨 {})</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="118"/>
        <source>下载权重失败 {}: {}</source>
        <translation>가중치 다운로드 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="121"/>
        <source>无法连接下载服务器, 请检查网络后重试</source>
        <translation>다운로드 서버에 연결할 수 없습니다. 네트워크를 확인한 후 다시 시도하세요</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="129"/>
        <source>下载中断, 已保留进度, 可再次点击续传</source>
        <translation>다운로드 중단됨, 진행 상황은 보존되었습니다. 다시 클릭하면 이어받을 수 있습니다</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="134"/>
        <source>下载不完整, 已保留进度, 可再次点击续传</source>
        <translation>다운로드가 불완전합니다. 진행 상황은 보존되었습니다. 다시 클릭하면 이어받을 수 있습니다</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="141"/>
        <source>权重校验不通过 {}: 期望 {} 实际 {}</source>
        <translation>가중치 검증 실패 {}: 예상 {} 실제 {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="146"/>
        <source>文件校验未通过, 损坏文件已删除, 请重试</source>
        <translation>파일 검증에 실패했습니다. 손상된 파일은 삭제되었습니다. 다시 시도하세요</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="152"/>
        <source>写入权重目录失败, 请检查磁盘空间</source>
        <translation>가중치 디렉터리 쓰기 실패, 디스크 공간을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="155"/>
        <source>权重就绪: {}</source>
        <translation>가중치 준비됨: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="176"/>
        <source>下载已取消, 已下载部分保留以便续传: {}</source>
        <translation>다운로드가 취소되었습니다. 내려받은 부분은 이어받을 수 있도록 보존됩니다: {}</translation>
    </message>
    <message>
        <location filename="../app/core/model_download.py" line="196"/>
        <source>权重下载异常 {}: {!r}</source>
        <translation>가중치 다운로드 예외 {}: {!r}</translation>
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
        <translation>모델 가중치</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="63"/>
        <source>目标检测 · Transformer</source>
        <translation>객체 검출 · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="97"/>
        <source>目标检测 · CNN</source>
        <translation>객체 검출 · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="131"/>
        <source>图像分割 · Transformer</source>
        <translation>이미지 세그멘테이션 · Transformer</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="165"/>
        <source>图像分割 · CNN</source>
        <translation>이미지 세그멘테이션 · CNN</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="221"/>
        <source>下载目录</source>
        <translation>다운로드 디렉터리</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="238"/>
        <source>更改</source>
        <translation>변경</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="265"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="293"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="498"/>
        <source>开始下载</source>
        <translation>다운로드 시작</translation>
    </message>
    <message>
        <location filename="../ui/model_manager.ui" line="275"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="280"/>
        <source>关闭</source>
        <translation>닫기</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="58"/>
        <source>还剩 {}s</source>
        <translation>{}s 남음</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="59"/>
        <source>还剩 {}m{}s</source>
        <translation>{}m{}s 남음</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="387"/>
        <source>选择权重目录</source>
        <translation>가중치 디렉터리 선택</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="405"/>
        <source>选择预训练权重</source>
        <translation>사전 학습된 가중치 선택</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="406"/>
        <source>权重文件 (*.pt *.pth *.ckpt)</source>
        <translation>가중치 파일 (*.pt *.pth *.ckpt)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="416"/>
        <source>仍要用这个文件吗?</source>
        <translation>그래도 이 파일을 사용하시겠습니까?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="444"/>
        <source>权重目录不可写入 {}: {!r}</source>
        <translation>가중치 디렉터리에 쓸 수 없습니다 {}: {!r}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="455"/>
        <source>勾选的模型都已就绪, 不需要下载.</source>
        <translation>선택한 모델이 모두 준비되어 다운로드가 필요하지 않습니다.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="460"/>
        <source>当前目录不可写入, 请点&quot;更改&quot;换一个目录:
{}</source>
        <translation>현재 디렉터리에 쓸 수 없습니다. &quot;변경&quot;을 눌러 다른 디렉터리를 선택하세요:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="293"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="465"/>
        <source>下载中...</source>
        <translation>다운로드 중...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="511"/>
        <source>以下权重没能下载完成:
</source>
        <translation>다음 가중치는 다운로드를 완료하지 못했습니다:
</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="518"/>
        <source>下载还在进行, 现在关闭会中断下载(已下载部分保留, 下次可续传).
确定关闭?</source>
        <translation>다운로드가 진행 중입니다. 지금 닫으면 중단됩니다(내려받은 부분은 보존되며 다음에 이어받기 가능).
닫으시겠습니까?</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="550"/>
        <source>去下载</source>
        <translation>다운로드</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="559"/>
        <source>该架构的权重必须先下载好才能开始训练, 也可以在权重管理里指定本地的权重文件.</source>
        <translation>이 아키텍처의 가중치는 먼저 다운로드해야 학습을 시작할 수 있습니다. 모델 가중치에서 로컬 가중치 파일을 지정할 수도 있습니다.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="553"/>
        <source>本次训练选用 {} {}模型, 需要先下载 {}.</source>
        <translation>이번 학습은 {} {} 모델을 사용하며, {}을(를) 먼저 다운로드해야 합니다.</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="552"/>
        <source>缺少模型权重</source>
        <translation>모델 가중치 없음</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="365"/>
        <source>待下载 {}</source>
        <translation>다운로드 필요: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="367"/>
        <source>无需下载</source>
        <translation>다운로드 불필요</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="369"/>
        <source>本地 {} 项</source>
        <translation>로컬: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="551"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
</context>
<context>
    <name>MultiCombo</name>
    <message>
        <location filename="../app/widgets/multi_combo.py" line="350"/>
        <source>请选择数据集</source>
        <translation>데이터셋 선택</translation>
    </message>
</context>
<context>
    <name>NameInputDialog</name>
    <message>
        <location filename="../ui/input_name.ui" line="14"/>
        <location filename="../ui/input_name.ui" line="40"/>
        <location filename="../app/widgets/name_input_dialog.py" line="13"/>
        <source>输入名称</source>
        <translation>이름 입력</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="65"/>
        <location filename="../app/widgets/name_input_dialog.py" line="14"/>
        <source>请输入名称</source>
        <translation>이름을 입력하세요</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="100"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
    <message>
        <location filename="../ui/input_name.ui" line="113"/>
        <source>确定</source>
        <translation>확인</translation>
    </message>
</context>
<context>
    <name>NameRules</name>
    <message>
        <location filename="../app/core/name_rules.py" line="25"/>
        <source>名称不能为空</source>
        <translation>이름을 입력하세요</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="27"/>
        <source>名称过长, 最多 {} 个字符</source>
        <translation>이름이 너무 깁니다(최대 {}자)</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="41"/>
        <source>名称不能包含「{}」等字符</source>
        <translation>이름에「{}」등의 문자는 사용할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/core/name_rules.py" line="54"/>
        <source>「{}」是系统保留名称, 请换一个</source>
        <translation>&quot;{}&quot;은(는) 예약된 이름입니다. 다른 이름을 사용하세요</translation>
    </message>
</context>
<context>
    <name>OcrTestRunner</name>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="46"/>
        <source>缺少测试依赖: {}</source>
        <translation>테스트 의존성이 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="187"/>
        <source>识别失败: {}</source>
        <translation>인식 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="274"/>
        <source>明细写入失败: {}</source>
        <translation>상세 쓰기 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="282"/>
        <source>未知的字符检测架构: {}</source>
        <translation>알 수 없는 텍스트 검출 아키텍처: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="296"/>
        <source>已加载配对识别模型: {}</source>
        <translation>페어링된 인식 모델을 불러왔습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="300"/>
        <source>识别模型不可用, 输出的标注只有框没有文字</source>
        <translation>인식 모델을 사용할 수 없습니다. 작성된 어노테이션에는 텍스트 없이 상자만 있습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="306"/>
        <location filename="../app/train/ocr_test_runner.py" line="425"/>
        <source>没有可用的图像, 请检查数据集</source>
        <translation>사용할 수 있는 이미지가 없습니다. 데이터셋을 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="307"/>
        <source>加载字符检测模型: {}</source>
        <translation>텍스트 검출 모델 불러오기: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="309"/>
        <location filename="../app/train/ocr_test_runner.py" line="429"/>
        <source>测试图片 {} 张</source>
        <translation>테스트 이미지 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="342"/>
        <source>预测失败 {}: {}</source>
        <translation>예측 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="372"/>
        <source>输出标注失败 {}: {}</source>
        <translation>어노테이션 출력 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="400"/>
        <source>已写出 {} 张图的文本标注(图像同目录)</source>
        <translation>{}개 이미지의 텍스트 어노테이션을 작성했습니다(이미지와 같은 디렉터리)</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="411"/>
        <source>未知的字符识别架构: {}</source>
        <translation>알 수 없는 텍스트 인식 아키텍처: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="415"/>
        <source>该模型没有词表, 无法识别</source>
        <translation>이 모델에는 어휘가 없어 인식할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="426"/>
        <source>加载字符识别模型: {} 词表 {} 个字符</source>
        <translation>텍스트 인식 모델 불러오기: {} 어휘 {}자</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="457"/>
        <source>识别失败 {}: {}</source>
        <translation>인식 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="464"/>
        <source>没有取到任何字条: 该数据集没有文本标注, 识别段只能拿标注框裁图来测</source>
        <translation>가져온 잘라낸 텍스트가 없습니다: 이 데이터셋에는 텍스트 어노테이션이 없어, 인식 단계는 어노테이션 상자로 잘라낸 이미지로만 테스트할 수 있습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="470"/>
        <source>WARN {} 张图没有文本标注, 已跳过</source>
        <translation>WARN {}개 이미지에 텍스트 어노테이션이 없어 건너뛰었습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_test_runner.py" line="473"/>
        <source>字条 {} 条, CER={:.4f}, 全对 {} 条</source>
        <translation>잘라낸 텍스트 {}개, CER={:.4f}, 전부 정확 {}개</translation>
    </message>
</context>
<context>
    <name>OcrTrainRunner</name>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="42"/>
        <source>缺少训练依赖: {}</source>
        <translation>학습 의존성이 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="118"/>
        <source>检测模型 {} 权重来源: {}</source>
        <translation>검출 모델 {} 가중치 출처: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="122"/>
        <source>检测模型 {} 构建失败</source>
        <translation>검출 모델 {} 구성 실패</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="138"/>
        <source>识别模型 {} 权重来源: {}</source>
        <translation>인식 모델 {} 가중치 출처: {}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="142"/>
        <source>识别模型 {} 构建失败</source>
        <translation>인식 모델 {} 구성 실패</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="174"/>
        <source>标注里没有任何文字, 无法训练字符识别</source>
        <translation>어노테이션에 텍스트가 없어 텍스트 인식을 학습할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="182"/>
        <source>词表 {} 个字符</source>
        <translation>어휘 {}자</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="195"/>
        <source>字符{}训练: model={} device={} epochs={} batch={} lr={}</source>
        <translation>텍스트 {} 학습: model={} device={} epochs={} batch={} lr={}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="198"/>
        <source>识别</source>
        <translation>인식</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="199"/>
        <source>检测</source>
        <translation>객체 검출</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="202"/>
        <source>训练集没有可用的文本标注</source>
        <translation>학습 세트에 사용할 수 있는 텍스트 어노테이션이 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="205"/>
        <source>验证集没有可用的文本标注</source>
        <translation>검증 세트에 사용할 수 있는 텍스트 어노테이션이 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="207"/>
        <source>数据集: train={} val={}</source>
        <translation>데이터셋: train={} val={}</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="293"/>
        <source>早停触发: 连续 {} 个 epoch 无提升</source>
        <translation>조기 종료 발동: {} epoch 연속 향상 없음</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_train_runner.py" line="322"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>이번 학습 출력 디렉터리(타임스탬프): {}</translation>
    </message>
</context>
<context>
    <name>OnnxExport</name>
    <message>
        <location filename="../app/train/onnx_export.py" line="112"/>
        <source>该识别模型没有词表, 无法导出</source>
        <translation>이 인식 모델에는 어휘가 없어 내보낼 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="121"/>
        <source>未知的字符模型架构: {}</source>
        <translation>알 수 없는 텍스트 모델 아키텍처: {}</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="133"/>
        <source>识别</source>
        <translation>인식</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="134"/>
        <source>检测</source>
        <translation>객체 검출</translation>
    </message>
    <message>
        <location filename="../app/train/onnx_export.py" line="152"/>
        <source>异常检测不导出 ONNX, 请用模型管理的「导出」生成模型包</source>
        <translation>이상 검출은 ONNX를 내보내지 않습니다. 모델 관리의 「내보내기」로 모델 패키지를 생성하세요</translation>
    </message>
</context>
<context>
    <name>ProjectMixin</name>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="32"/>
        <source>输入名称</source>
        <translation>이름 입력</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="33"/>
        <source>项目名称</source>
        <translation>프로젝트 이름</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="37"/>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <source>创建项目</source>
        <translation>프로젝트 생성</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="41"/>
        <location filename="../app/mixins/project_mixin.py" line="53"/>
        <source>项目名称已存在!</source>
        <translation>같은 이름의 프로젝트가 이미 있습니다!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="44"/>
        <source>创建项目: {}</source>
        <translation>프로젝트 생성: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="49"/>
        <location filename="../app/mixins/project_mixin.py" line="53"/>
        <location filename="../app/mixins/project_mixin.py" line="106"/>
        <source>修改名称</source>
        <translation>이름 변경</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="56"/>
        <source>重命名项目: {} → {}</source>
        <translation>프로젝트 이름 바꾸기: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="61"/>
        <location filename="../app/mixins/project_mixin.py" line="107"/>
        <source>删除项目</source>
        <translation>프로젝트 삭제</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="62"/>
        <source>确定删除项目&quot;{}&quot;吗?
</source>
        <translation>프로젝트 &quot;{}&quot;을(를) 삭제하시겠습니까?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="63"/>
        <source>删除项目: {}</source>
        <translation>프로젝트 삭제: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="103"/>
        <location filename="../app/mixins/project_mixin.py" line="147"/>
        <location filename="../app/mixins/project_mixin.py" line="156"/>
        <source>添加数据集</source>
        <translation>데이터셋 추가</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="105"/>
        <source>导出项目</source>
        <translation>프로젝트 내보내기</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="122"/>
        <source>导入</source>
        <translation>가져오기</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="123"/>
        <source>导出</source>
        <translation>내보내기</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="124"/>
        <source>重载</source>
        <translation>다시 불러오기</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="125"/>
        <source>移动</source>
        <translation>이동</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="126"/>
        <source>修改</source>
        <translation>이름 변경</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="127"/>
        <source>删除</source>
        <translation>삭제</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="148"/>
        <source>数据集名称</source>
        <translation>데이터셋 이름</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="156"/>
        <location filename="../app/mixins/project_mixin.py" line="167"/>
        <source>该项目下已存在同名数据集!</source>
        <translation>이 프로젝트에 같은 이름의 데이터셋이 이미 있습니다!</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="158"/>
        <source>创建数据集: {}/{}</source>
        <translation>데이터셋 생성: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="163"/>
        <location filename="../app/mixins/project_mixin.py" line="167"/>
        <source>修改数据集</source>
        <translation>데이터셋 이름 변경</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="169"/>
        <source>重命名数据集: {} → {}</source>
        <translation>데이터셋 이름 바꾸기: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="174"/>
        <source>删除数据集</source>
        <translation>데이터셋 삭제</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="175"/>
        <source>确定删除数据集&quot;{}&quot;吗?
</source>
        <translation>데이터셋 &quot;{}&quot;을(를) 삭제하시겠습니까?
</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="179"/>
        <source>删除数据集: {}/{}</source>
        <translation>데이터셋 삭제: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="198"/>
        <location filename="../app/mixins/project_mixin.py" line="211"/>
        <location filename="../app/mixins/project_mixin.py" line="228"/>
        <source>移动数据集</source>
        <translation>데이터셋 이동</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="199"/>
        <source>是否将&quot;{}&quot;的数据从
{} / {} 移动到 {} / {}?
移动后源数据集将清空.</source>
        <translation>&quot;{}&quot;의 데이터를
{} / {}에서 {} / {}로 이동하시겠습니까?
이동 후 원본 데이터셋은 비워집니다.</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="208"/>
        <source>移动失败</source>
        <translation>이동 실패</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="212"/>
        <source>已从 {} / {} 移动到 {} / {}</source>
        <translation>{} / {}에서 {} / {}로 이동했습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="229"/>
        <source>没有可移动到的目标数据集(本项目之外无数据集)</source>
        <translation>이동할 대상 데이터셋이 없습니다(이 프로젝트 외에 데이터셋이 없음)</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="233"/>
        <source>选择目标数据集</source>
        <translation>대상 데이터셋 선택</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="237"/>
        <source>选择要将数据移动到的目标数据集:</source>
        <translation>데이터를 이동할 대상 데이터셋을 선택하세요:</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="318"/>
        <source>{}: {}个</source>
        <translation>{}: {}개</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="320"/>
        <source>数据集移动: {}/{} → {}/{} | 移动图像 {} 张 | 目标标签统计({}类): {}</source>
        <translation>데이터셋 이동: {}/{} → {}/{} | 이미지 {}장 이동 | 대상 라벨 통계({}개 클래스): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/project_mixin.py" line="323"/>
        <source>(无)</source>
        <translation>(없음)</translation>
    </message>
</context>
<context>
    <name>ProjectSidebar</name>
    <message>
        <location filename="../app/widgets/project_sidebar.py" line="424"/>
        <source>{} 个项目 · {} 个数据集</source>
        <translation>프로젝트 {}개 · 데이터셋 {}개</translation>
    </message>
</context>
<context>
    <name>QueueMixin</name>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="97"/>
        <source>训练队列已启动</source>
        <translation>학습 대기열이 시작되었습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="107"/>
        <source>[队列] 已停止</source>
        <translation>[队列] 중지했습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="195"/>
        <source>[队列] 所有任务已执行完毕</source>
        <translation>[队列] 모든 작업이 실행 완료되었습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="203"/>
        <source>[队列] 跳过任务 {}: {}</source>
        <translation>[队列] 작업 건너뜀 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="204"/>
        <source>队列任务启动失败 {}: {}</source>
        <translation>대기열 작업 시작 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="224"/>
        <source>[队列] 缺少权重 {}, 该项训练会失败</source>
        <translation>[队列] 가중치 {}가 없습니다. 해당 학습은 실패합니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="227"/>
        <source>[队列] 缺少权重 {}, 该项训练时会自行下载</source>
        <translation>[队列] 가중치 {}가 없습니다. 해당 항목은 학습 시 자동으로 다운로드합니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="240"/>
        <source>已有训练在进行中</source>
        <translation>이미 학습이 진행 중입니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="245"/>
        <source>[队列] 开始队列第 {}/{} 项: {}</source>
        <translation>[队列] 대기열 {}/{}번째 시작: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="249"/>
        <source>队列启动任务: {} record={}</source>
        <translation>대기열 작업 시작: {} record={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="287"/>
        <source>训练未完成, 详见日志</source>
        <translation>학습이 완료되지 않았습니다. 로그를 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="321"/>
        <source>[队列] 显存等待超时, 仍继续启动下一个任务</source>
        <translation>[队列] VRAM 대기가 시간 초과되었지만 다음 작업 시작을 계속합니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/queue_mixin.py" line="367"/>
        <source>队列 {}</source>
        <translation>대기열 {}</translation>
    </message>
</context>
<context>
    <name>ResponsiveMixin</name>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="19"/>
        <location filename="../app/mixins/responsive_mixin.py" line="40"/>
        <source>更多</source>
        <translation>더 보기</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="43"/>
        <location filename="../app/mixins/responsive_mixin.py" line="52"/>
        <source>界面字号</source>
        <translation>화면 글꼴 크기</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="58"/>
        <source>标准</source>
        <translation>표준</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="59"/>
        <source>大</source>
        <translation>크게</translation>
    </message>
    <message>
        <location filename="../app/mixins/responsive_mixin.py" line="60"/>
        <source>超大</source>
        <translation>아주 크게</translation>
    </message>
</context>
<context>
    <name>StatusText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="18"/>
        <source>等待中</source>
        <translation>대기 중</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="19"/>
        <location filename="../app/widgets/status_style.py" line="26"/>
        <source>训练中</source>
        <translation>학습 중</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="20"/>
        <location filename="../app/widgets/status_style.py" line="27"/>
        <source>已完成</source>
        <translation>완료</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="21"/>
        <location filename="../app/widgets/status_style.py" line="28"/>
        <source>失败</source>
        <translation>실패</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="22"/>
        <location filename="../app/widgets/status_style.py" line="31"/>
        <source>已跳过</source>
        <translation>건너뜀</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="23"/>
        <location filename="../app/widgets/status_style.py" line="29"/>
        <source>已停止</source>
        <translation>중지됨</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="24"/>
        <location filename="../app/widgets/status_style.py" line="32"/>
        <source>已中断</source>
        <translation>중단됨</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="30"/>
        <source>失败/已停止</source>
        <translation>실패/중지됨</translation>
    </message>
</context>
<context>
    <name>TaskText</name>
    <message>
        <location filename="../app/widgets/status_style.py" line="37"/>
        <source>检测</source>
        <translation>객체 검출</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="38"/>
        <source>分割</source>
        <translation>세그멘테이션</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="39"/>
        <source>分类</source>
        <translation>분류</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="40"/>
        <source>异常检测</source>
        <translation>이상 검출</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="41"/>
        <location filename="../app/widgets/status_style.py" line="42"/>
        <source>字符检测</source>
        <translation>텍스트 검출</translation>
    </message>
    <message>
        <location filename="../app/widgets/status_style.py" line="43"/>
        <source>字符识别</source>
        <translation>텍스트 인식</translation>
    </message>
</context>
<context>
    <name>TestDialog</name>
    <message>
        <location filename="../ui/test_dialog.ui" line="14"/>
        <location filename="../ui/test_dialog.ui" line="41"/>
        <source>模型测试</source>
        <translation>모델 테스트</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="102"/>
        <source>检测</source>
        <translation>객체 검출</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="118"/>
        <source>best.pth</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="130"/>
        <source>mAP50 0.912 · 输入 640 · 规模 n · 训练 2026-09-01 14:22</source>
        <translation>mAP50 0.912 · 입력 640 · 스케일 n · 학습 2026-09-01 14:22</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="151"/>
        <source>数据与设备</source>
        <translation>데이터 및 장치</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="193"/>
        <source>数据</source>
        <translation>데이터</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="216"/>
        <source>设备</source>
        <translation>장치</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="246"/>
        <source>测试参数</source>
        <translation>테스트 파라미터</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="288"/>
        <source>置信度</source>
        <translation>신뢰도</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="329"/>
        <source>低于该分数的预测直接丢弃</source>
        <translation>이 점수보다 낮은 예측은 버립니다</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="345"/>
        <source>IoU 阈值</source>
        <translation>IoU 임계값</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="386"/>
        <source>与标注框重合度达标才算正确检出</source>
        <translation>정답 박스와의 겹침이 이 값 이상이어야 정확한 검출로 인정됩니다</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="402"/>
        <source>输出标签文件</source>
        <translation>라벨 파일 출력</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="434"/>
        <source>写在图像目录下, 可重载数据集查看检出效果</source>
        <translation>이미지 디렉터리에 작성되며, 데이터셋을 다시 불러와 검출 결과를 확인할 수 있습니다</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="486"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="496"/>
        <source>请选择数据集</source>
        <translation>데이터셋 선택</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="544"/>
        <location filename="../app/widgets/test_dialog.py" line="109"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
    <message>
        <location filename="../ui/test_dialog.ui" line="551"/>
        <source>开始测试</source>
        <translation>테스트 시작</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="237"/>
        <source>未指定模型</source>
        <translation>모델이 지정되지 않았습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="238"/>
        <source>请在模型列表中重新选择一行</source>
        <translation>모델 목록에서 행을 다시 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="254"/>
        <source>输入 {}</source>
        <translation>입력 {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="256"/>
        <source>规模 {}</source>
        <translation>스케일 {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="258"/>
        <source>训练 {}</source>
        <translation>학습 {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="260"/>
        <source>该记录未保存训练指标</source>
        <translation>이 기록에는 저장된 학습 지표가 없습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="263"/>
        <source> · 文件已不存在</source>
        <translation> · 파일이 더 이상 존재하지 않음</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="289"/>
        <source>请先勾选要测试的数据集</source>
        <translation>먼저 테스트할 데이터셋을 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="301"/>
        <source>{} 个数据集 · {} 张图</source>
        <translation>데이터셋 {}개 · 이미지 {}장</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="303"/>
        <source>分类数据集, 统计每张图的判断正确率</source>
        <translation>분류 데이터셋, 이미지별 판정 정확도를 집계합니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="305"/>
        <source>已标注, 评估模式: 统计检出率 / 漏检 / 误检</source>
        <translation>라벨 있음, 평가 모드: 재현율 / 미검출 / 오검출 집계</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="307"/>
        <source>未标注, 推理模式: 只输出预测标签</source>
        <translation>미라벨, 추론 모드: 예측 라벨만 출력</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="309"/>
        <source>部分已标注, 已标注与未标注的数据集不能一起测</source>
        <translation>일부만 라벨링됨. 라벨 있는 데이터셋과 미라벨 데이터셋은 함께 테스트할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="336"/>
        <source>为判定为不良品的图写 &lt;同名&gt;.json 到图像目录, 多边形标出异常区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>불량품으로 판정된 이미지에 대해 &lt;같은 이름&gt;.json을 이미지 디렉터리에 작성하고, 다각형으로 이상 영역을 표시하며, 어노테이션 도구에서 바로 열 수 있습니다. 해당 위치의 기존 수동 라벨은 덮어써집니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="340"/>
        <source>把异常区域写成 labelme json, 便于重载复核</source>
        <translation>이상 영역을 labelme json으로 작성해 다시 불러와 검토하기 쉽게 합니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="353"/>
        <source>字符识别只报告字条识别率, 不输出标注文件</source>
        <translation>텍스트 인식은 잘라낸 텍스트 인식률만 보고하며, 어노테이션 파일은 출력하지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="359"/>
        <location filename="../app/widgets/test_dialog.py" line="365"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 框出文本区域, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>각 이미지마다 &lt;동일한 이름&gt;.json을 이미지 디렉터리에 작성하여 텍스트 영역을 상자로 표시합니다. 어노테이션 도구에서 바로 열 수 있으며, 해당 위치의 기존 수동 어노테이션은 덮어씌워집니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="368"/>
        <source>把检测到的文本框写成 labelme json, 便于重载复核</source>
        <translation>검출된 텍스트 상자를 labelme json으로 작성하여, 다시 불러온 후 검토하기 쉽게 합니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="371"/>
        <source>为每张图写 &lt;同名&gt;.json 到图像目录, 标注工具可直接打开;该处已有人工标注会被覆盖</source>
        <translation>이미지마다 &lt;같은 이름&gt;.json을 이미지 디렉터리에 작성해 어노테이션 도구에서 바로 열 수 있습니다. 해당 위치의 기존 수동 라벨은 덮어써집니다</translation>
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
        <translation>테스트</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="388"/>
        <source>已有测试在进行中</source>
        <translation>이미 테스트가 진행 중입니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="392"/>
        <source>请至少选择一个数据集</source>
        <translation>데이터셋을 하나 이상 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="407"/>
        <source>置信度/iou阈值必须是数字</source>
        <translation>신뢰도/IoU 임계값은 숫자여야 합니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="413"/>
        <source>模型文件不存在, 请重新选择</source>
        <translation>모델 파일이 없습니다. 다시 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="426"/>
        <source>数据集 {}/{} 未导入图像</source>
        <translation>데이터셋 {}/{}에 이미지가 가져와지지 않았습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="436"/>
        <source>分类数据集与检测/分割数据集不能同时测试: {}/{}</source>
        <translation>분류 데이터셋과 검출/세그멘테이션 데이터셋은 함께 테스트할 수 없습니다: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="442"/>
        <source>已标注与未标注的数据集不能同时测试: {}/{}</source>
        <translation>라벨 있는 데이터셋과 미라벨 데이터셋은 함께 테스트할 수 없습니다: {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="457"/>
        <source>字符识别要拿标注框裁字条才能测, 请选择已标注的数据集</source>
        <translation>텍스트 인식은 어노테이션 상자로 잘라낸 텍스트를 만들어야 테스트할 수 있으므로, 어노테이션이 완료된 데이터셋을 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="482"/>
        <source>[test] 启动测试 worker: model={} 数据集={} 图像目录={} device={} cfg={}</source>
        <translation>[test] 테스트 worker 시작: model={} 데이터셋={} 이미지 디렉터리={} device={} cfg={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="487"/>
        <source>测试准备中...</source>
        <translation>테스트 준비 중...</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="504"/>
        <location filename="../app/widgets/test_dialog.py" line="505"/>
        <source>测试即将开始</source>
        <translation>테스트가 곧 시작됩니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="551"/>
        <source>测试中 {}/{}</source>
        <translation>테스트 중 {}/{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="571"/>
        <source>[test-dialog] 测试完成, ok={}</source>
        <translation>[test-dialog] 테스트 완료, ok={}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="579"/>
        <location filename="../app/widgets/test_dialog.py" line="589"/>
        <source>测试结果</source>
        <translation>테스트 결과</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="580"/>
        <source>测试未正常完成</source>
        <translation>테스트가 정상적으로 완료되지 않았습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="590"/>
        <source>字条 {} 条 · CER {:.4f} · 全对 {} 条</source>
        <translation>잘라낸 텍스트 {}개 · CER {:.4f} · 전부 정확 {}개</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="597"/>
        <source>[test-dialog] 测试失败: {}</source>
        <translation>[test-dialog] 테스트 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/test_dialog.py" line="604"/>
        <source>测试失败</source>
        <translation>테스트 실패</translation>
    </message>
</context>
<context>
    <name>TestReport</name>
    <message>
        <location filename="../app/train/test_report.py" line="179"/>
        <source>漏 {}</source>
        <translation>미검출 {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="181"/>
        <source>误 {}</source>
        <translation>오검출 {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="183"/>
        <source>认错 {}</source>
        <translation>오분류 {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="194"/>
        <source>(图片无法打开)</source>
        <translation>(이미지를 열 수 없음)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="280"/>
        <source>类别认错: {} → {}</source>
        <translation>클래스 오분류: {} → {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="308"/>
        <source>本次验证集没有漏检, 也没有误检.</source>
        <translation>이번 검증 세트에는 미검출도 오검출도 없습니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="311"/>
        <source>明细抽样: 共 {} 张有问题(漏检 {} / 误检 {}), 本报告抽取 {} 张 - 每个类别每种错误最多 {} 张, 按错误数从多到少取</source>
        <translation>상세 샘플링: 문제가 있는 이미지 총 {}장(미검출 {} / 오검출 {}), 이 보고서는 {}장을 추출 - 각 클래스별 각 오류 유형 최대 {}장, 오류 수가 많은 순서로 선택</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="316"/>
        <source>明细: 共 {} 张有问题(漏检 {} / 误检 {}), 已全部列出</source>
        <translation>상세: 문제가 있는 이미지 총 {}장(미검출 {} / 오검출 {}), 모두 나열했습니다</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="343"/>
        <source>漏检 GT: 有标注但模型没检出</source>
        <translation>미검출 GT: 어노테이션은 있지만 모델이 검출하지 못한 것</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="345"/>
        <source>误检预测: 模型检出但标注里没有</source>
        <translation>오검출 예측: 모델이 검출했지만 어노테이션에 없는 것</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="347"/>
        <source>正确检出(仅作位置参照)</source>
        <translation>정상 검출(위치 참조용)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="349"/>
        <source>类别认错: 位置对但判错类别(GT → 预测)</source>
        <translation>클래스 오분류: 위치는 맞지만 클래스가 틀림(GT → 예측)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="352"/>
        <source>虚线轮廓: 分割 mask / 标注多边形(判定按外接框 IoU)</source>
        <translation>점선 윤곽: 세그멘테이션 mask / 어노테이션 다각형(판정은 외접 사각형 IoU 기준)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="450"/>
        <location filename="../app/train/test_report.py" line="1049"/>
        <source>模型评估报告</source>
        <translation>모델 평가 보고서</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="454"/>
        <source>当前训练模型</source>
        <translation>현재 학습 모델</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="458"/>
        <location filename="../app/train/test_report.py" line="464"/>
        <source>(未记录)</source>
        <translation>(기록 없음)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="463"/>
        <source>数据集 </source>
        <translation>데이터셋 </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="466"/>
        <source>置信度 {}</source>
        <translation>신뢰도 {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="486"/>
        <source>测试张数</source>
        <translation>테스트 이미지 수</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="487"/>
        <location filename="../app/train/test_report.py" line="489"/>
        <source>{} 张</source>
        <translation>{}장</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="488"/>
        <source>有问题的图片</source>
        <translation>문제가 있는 이미지</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="491"/>
        <source>检出率 (Recall)</source>
        <translation>재현율 (Recall)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="493"/>
        <source>准确率 (Precision)</source>
        <translation>정확도 (Precision)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="495"/>
        <source>正确检出</source>
        <translation>정상 검출</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="496"/>
        <source>{} 个</source>
        <translation>{}개</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="497"/>
        <source>漏检 (该抓没抓)</source>
        <translation>미검출 (검출해야 할 것을 놓침)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="498"/>
        <location filename="../app/train/test_report.py" line="501"/>
        <location filename="../app/train/test_report.py" line="506"/>
        <source>{} 个 / {} 张图</source>
        <translation>{}개 / 이미지 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="500"/>
        <source>误检 (过杀)</source>
        <translation>오검출 (과검출)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="505"/>
        <source>类别认错 (位置对, 类别错)</source>
        <translation>클래스 오분류 (위치는 맞지만 클래스가 틀림)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="508"/>
        <source>指标</source>
        <translation>지표</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="509"/>
        <source>值</source>
        <translation>값</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="528"/>
        <source>按类别</source>
        <translation>클래스별</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="531"/>
        <source>类别</source>
        <translation>클래스</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="532"/>
        <source>标注</source>
        <translation>어노테이션</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="533"/>
        <source>正确</source>
        <translation>정답</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="534"/>
        <source>漏检</source>
        <translation>미검출</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="535"/>
        <source>误检</source>
        <translation>오검출</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="536"/>
        <source>检出率</source>
        <translation>재현율</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="537"/>
        <source>准确率</source>
        <translation>정확도</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="564"/>
        <source>... 另有 {} 类未列出</source>
        <translation>... 그 외 {}개 클래스는 나열되지 않음</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="586"/>
        <source>错误样本明细(仅列漏检 / 误检图片, 正确检出不列出)</source>
        <translation>오류 샘플 상세(미검출 / 오검출 이미지만 나열, 정상 검출은 나열하지 않음)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="625"/>
        <source>本轮检出率 {:.0f}%, 准确率 {:.0f}%.</source>
        <translation>이번 재현율 {:.0f}%, 정확도 {:.0f}%.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="628"/>
        <source>没有逐类别统计, 无法定位到具体标签,请先确认标签文件能正常读到.</source>
        <translation>클래스별 통계가 없어 구체적인 라벨을 특정할 수 없습니다. 먼저 라벨 파일을 정상적으로 읽을 수 있는지 확인하세요.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="652"/>
        <source>漏检分布在</source>
        <translation>미검출은 다음 클래스에 분포합니다: </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="653"/>
        <source>漏检集中在</source>
        <translation>미검출은 다음 클래스에 집중됩니다: </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="656"/>
        <source>(共 {} 个), 优先补这几类的姿态, 光照样本,并复核标注是否有遗漏.</source>
        <translation>({}개). 해당 클래스의 자세·조명 샘플을 우선 보완하고, 어노테이션 누락 여부를 확인하세요.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="662"/>
        <source>误检分布在</source>
        <translation>오검출은 다음 클래스에 분포합니다: </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="663"/>
        <source>误检以</source>
        <translation>오검출은 </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="664"/>
        <source>({} 个),属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({}개), 과검출에 해당합니다. 무결함 부정 샘플을 보완하고 어노테이션 노이즈를 정리하는 것이 좋습니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="666"/>
        <source>({} 个)为主,属过杀, 建议补无缺陷负样本,清理标注噪声.</source>
        <translation>({}개)가 중심입니다. 과검출에 해당합니다. 무결함 부정 샘플을 보완하고 어노테이션 노이즈를 정리하는 것이 좋습니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="675"/>
        <source>暂无</source>
        <translation>없음</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="679"/>
        <source>此外 {} 处位置对但类别判错</source>
        <translation>그 외 {}곳은 위치는 맞지만 클래스 판정이 틀렸습니다</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="681"/>
        <source>(报告紫框), 属分类能力不足而非定位问题,需补易混淆类别之间的区分性样本.</source>
        <translation>(보고서의 보라색 박스). 위치 문제가 아니라 분류 능력 부족에 해당하므로, 혼동하기 쉬운 클래스 간 구분 샘플을 보완해야 합니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="686"/>
        <source>其中</source>
        <translation>이 중 </translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="688"/>
        <source>仅 {} 个标注, 样本不足是主要瓶颈, 建议补到 200 个以上.</source>
        <translation>라벨이 {}개뿐이며 샘플 부족이 주요 병목입니다. 200개 이상으로 보완하는 것이 좋습니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="693"/>
        <source>各类样本量差距大(最多 {} / 最少 {}),训练时建议做类别均衡采样.</source>
        <translation>클래스별 샘플 수 차이가 큽니다(최대 {} / 최소 {}). 학습 시 클래스 균형 샘플링을 권장합니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="698"/>
        <source>把本报告中的漏检, 误检图加入训练集复训,再用同参数复测对比.</source>
        <translation>이 보고서의 미검출·오검출 이미지를 학습 세트에 추가해 재학습한 뒤, 동일한 파라미터로 다시 테스트해 비교하세요.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="702"/>
        <source>本轮无漏检, 无误检, 建议用更严的阈值或更难的样本再压一轮, 确认稳定性.</source>
        <translation>이번에는 미검출과 오검출이 없습니다. 더 엄격한 임계값이나 더 어려운 샘플로 한 번 더 검증해 안정성을 확인하는 것이 좋습니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="898"/>
        <source>改进建议</source>
        <translation>개선 제안</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="903"/>
        <source>基于本次测试的指标与按类别表现</source>
        <translation>이번 테스트의 지표와 클래스별 성능 기준</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="905"/>
        <source>(模型: {})</source>
        <translation>(모델: {})</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="907"/>
        <source>, 建议如下:</source>
        <translation>, 권장 사항은 다음과 같습니다:</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="925"/>
        <source>标红的标签是需要重点关注的类别.</source>
        <translation>빨간색으로 표시된 라벨은 중점 관리가 필요한 클래스입니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="930"/>
        <location filename="../app/train/test_report.py" line="956"/>
        <source>第 {} 页</source>
        <translation>{} 페이지</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1020"/>
        <source>{}(抽取 {} / 共 {} 张)</source>
        <translation>{}(추출 {} / 총 {}장)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1023"/>
        <source>{}(共 {} 张)</source>
        <translation>{}(총 {}장)</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1025"/>
        <source>漏检样本: 有标注但模型没检出</source>
        <translation>미검출 샘플: 어노테이션은 있지만 모델이 검출하지 못한 것</translation>
    </message>
    <message>
        <location filename="../app/train/test_report.py" line="1028"/>
        <source>误检样本: 模型检出但标注里没有</source>
        <translation>오검출 샘플: 모델이 검출했지만 어노테이션에 없는 것</translation>
    </message>
</context>
<context>
    <name>TestResultDialog</name>
    <message>
        <location filename="../ui/test_result.ui" line="14"/>
        <source>测试结果分析</source>
        <translation>테스트 결과 분석</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="83"/>
        <source>图像维度</source>
        <translation>이미지 기준</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="93"/>
        <source>按「张」统计</source>
        <translation>「장」 단위 집계</translation>
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
        <translation>테스트 이미지 수</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="219"/>
        <source>全对图像</source>
        <translation>모두 정확한 이미지</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="275"/>
        <source>有漏检图像</source>
        <translation>미검출 이미지</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="331"/>
        <location filename="../app/train/test_result_dialog.py" line="251"/>
        <source>有误检图像</source>
        <translation>오검출 이미지</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="375"/>
        <source>标签维度</source>
        <translation>라벨 기준</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="385"/>
        <source>按「标注框」统计</source>
        <translation>「박스」 단위 집계</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="455"/>
        <location filename="../ui/test_result.ui" line="664"/>
        <location filename="../app/train/test_result_dialog.py" line="259"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>正确检出</source>
        <translation>정상 검출</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="511"/>
        <location filename="../ui/test_result.ui" line="669"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>漏检</source>
        <translation>미검출</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="567"/>
        <location filename="../ui/test_result.ui" line="674"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>误检</source>
        <translation>오검출</translation>
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
        <translation>정확도</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="654"/>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>类别</source>
        <translation>클래스</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="659"/>
        <location filename="../app/train/test_result_dialog.py" line="393"/>
        <source>标注数</source>
        <translation>어노테이션 수</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="679"/>
        <location filename="../app/train/test_result_dialog.py" line="394"/>
        <source>检出率</source>
        <translation>재현율</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="708"/>
        <source>每类抽取</source>
        <translation>클래스별 추출</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="715"/>
        <source>每个类别的每种错误（漏检 / 误检）最多列出几张图。
报告体积约 120 KB 一张，样本多时调小可以显著减小 PDF；选「全部」则每张有问题的图都列。</source>
        <translation>클래스마다 각 오류 유형(미검출 / 오검출)에 대해 최대로 나열할 이미지 수입니다.
보고서는 이미지 한 장당 약 120 KB이며, 샘플이 많을 때 이 값을 낮추면 PDF가 크게 줄어듭니다. 「전체」를 선택하면 문제가 있는 이미지를 모두 나열합니다.</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="719"/>
        <source> 张</source>
        <translation> 장</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="722"/>
        <source>全部</source>
        <translation>전체</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="751"/>
        <location filename="../app/train/test_result_dialog.py" line="187"/>
        <source>导出 PDF 报告</source>
        <translation>PDF 보고서 내보내기</translation>
    </message>
    <message>
        <location filename="../ui/test_result.ui" line="758"/>
        <location filename="../app/train/test_result_dialog.py" line="92"/>
        <source>确定</source>
        <translation>확인</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="152"/>
        <source>把漏检/误检的图逐张画框导出成 PDF</source>
        <translation>미검출/오검출 이미지에 박스를 그려 PDF로 내보냅니다</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="155"/>
        <source>异常检测的逐图结果已写成 CSV, 不支持导出画框 PDF</source>
        <translation>이상 검출의 이미지별 결과를 CSV로 작성했습니다. 박스를 그린 PDF 내보내기는 지원하지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="157"/>
        <source>本次测试没有逐图错误明细, 无法导出</source>
        <translation>이번 테스트에는 이미지별 오류 상세가 없어 내보낼 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="169"/>
        <source>保存 PDF 报告</source>
        <translation>PDF 보고서 저장</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="170"/>
        <source>PDF 文件 (*.pdf)</source>
        <translation>PDF 파일 (*.pdf)</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="176"/>
        <source>正在生成...</source>
        <translation>생성 중...</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="194"/>
        <source>无需导出</source>
        <translation>내보낼 내용 없음</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="195"/>
        <source>本次测试没有漏检也没有误检, 没有内容可写.</source>
        <translation>이번 테스트에는 미검출도 오검출도 없어 작성할 내용이 없습니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="198"/>
        <source>导出完成</source>
        <translation>내보내기 완료</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="199"/>
        <source>PDF 报告已保存到:
{}</source>
        <translation>PDF 보고서를 저장했습니다:
{}</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="203"/>
        <source>导出失败</source>
        <translation>내보내기 실패</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="238"/>
        <source>按&quot;张&quot;统计 · 检出 1 个即算检出</source>
        <translation>&quot;장&quot; 단위 집계 · 1개만 검출되어도 검출로 인정</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="240"/>
        <source> · 有标注 {} 张</source>
        <translation> · 라벨 있는 이미지 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="244"/>
        <source>检出图像</source>
        <translation>검출 이미지</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="245"/>
        <location filename="../app/train/test_result_dialog.py" line="260"/>
        <source>检出率 </source>
        <translation>재현율 </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="247"/>
        <source>未检出图像</source>
        <translation>미검출 이미지</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="248"/>
        <source>未检出率 </source>
        <translation>미검출률 </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="252"/>
        <source>误检率 </source>
        <translation>오검출률 </translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="257"/>
        <source>按&quot;标注框&quot;统计 · 标注总数 {}</source>
        <translation>&quot;박스&quot; 단위 집계 · 총 어노테이션 {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="280"/>
        <source>按&quot;张&quot;统计 · 每张图判一个类别</source>
        <translation>&quot;장&quot; 단위 집계 · 이미지마다 클래스 하나 판정</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="285"/>
        <source>判断正确</source>
        <translation>정확 판정</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="287"/>
        <source>判断错误</source>
        <translation>오판정</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="290"/>
        <location filename="../app/train/test_result_dialog.py" line="362"/>
        <source>精度</source>
        <translation>정확도</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="315"/>
        <source>按&quot;张&quot;统计 · 整图判良品/不良品</source>
        <translation>&quot;장&quot; 단위 집계 · 이미지 전체를 양품/불량품으로 판정</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="329"/>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <source>检出异常</source>
        <translation>검출된 이상</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="340"/>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <source>总图数</source>
        <translation>전체 이미지 수</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="345"/>
        <source>异常</source>
        <translation>이상</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="361"/>
        <source>正确</source>
        <translation>정답</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="362"/>
        <source>错误</source>
        <translation>오류</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="383"/>
        <source>模型里没有判定阈值, 只报告分数, 逐图分数见 CSV 明细.</source>
        <translation>모델에 판정 임계값이 없어 점수만 보고합니다. 이미지별 점수는 CSV 상세를 참조하세요.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="384"/>
        <source>判定阈值 {:.4f}. 本次 {} 张, 检出异常 {} 张.</source>
        <translation>판정 임계값 {:.4f}. 이번 {}장, 이상 {}장 검출.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="297"/>
        <source>整体精度 {:.1f}%, &quot;{}&quot;类错误最多({} 张), 是拉低精度的主要原因.</source>
        <translation>전체 정확도 {:.1f}%, &quot;{}&quot; 클래스의 오류가 가장 많아({}장) 정확도를 낮추는 주된 원인입니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="422"/>
        <source>整体漏检偏多(漏检 {} 个, 多于误检 {} 个).&quot;{}&quot;类漏检最多({} 个), 是检出率低的主要原因.</source>
        <translation>전체적으로 미검출이 많습니다(미검출 {}개 &gt; 오검출 {}개). &quot;{}&quot; 클래스의 미검출이 가장 많아({}개) 재현율이 낮은 주된 원인입니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="428"/>
        <source>整体误检偏多(误检 {} 个, 多于漏检 {} 个).&quot;{}&quot;类误检最多({} 个), 是准确率低的主要原因.</source>
        <translation>전체적으로 오검출이 많습니다(오검출 {}개 &gt; 미검출 {}개). &quot;{}&quot; 클래스의 오검출이 가장 많아({}개) 정밀도가 낮은 주된 원인입니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="432"/>
        <source>模型表现良好: 无漏检, 无误检.</source>
        <translation>모델 성능이 양호합니다: 미검출과 오검출이 없습니다.</translation>
    </message>
    <message>
        <location filename="../app/train/test_result_dialog.py" line="434"/>
        <source>另有 {} 处位置对但类别判错(报告里用紫框标出),属分类能力不足, 需补易混淆类别的区分性样本.</source>
        <translation>위치가 맞지만 클래스를 잘못 판정한 박스가 {}개 더 있습니다(보고서에 보라색 박스로 표시). 분류 능력 부족에 해당하므로 혼동하기 쉬운 클래스의 구분 샘플을 보강해야 합니다.</translation>
    </message>
</context>
<context>
    <name>TestRunner</name>
    <message>
        <location filename="../app/train/test_runner.py" line="282"/>
        <source>覆盖已有标注 {}</source>
        <translation>기존 어노테이션 덮어쓰기 {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="312"/>
        <source>明细初始化失败: {}</source>
        <translation>상세 초기화 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="321"/>
        <source>明细目录创建失败: {}</source>
        <translation>상세 디렉터리 생성 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="349"/>
        <source>明细写入失败: {}</source>
        <translation>상세 쓰기 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="431"/>
        <source>当前安装缺少所需组件, 无法执行测试</source>
        <translation>현재 설치에 필요한 구성 요소가 없어 테스트를 실행할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="433"/>
        <source>加载模型: {}</source>
        <translation>모델 불러오기: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="449"/>
        <source>推理已优化: {}</source>
        <translation>추론 최적화됨: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="465"/>
        <source>测试图片 {} 张</source>
        <translation>테스트 이미지 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="515"/>
        <source>预测失败 {}: {}</source>
        <translation>예측 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="529"/>
        <source>输出标注失败 {}: {}</source>
        <translation>어노테이션 출력 실패 {}: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="584"/>
        <source>WARN 标签目录存在但所有 {} 张图都没读到 GT,请确认标签是 .txt (YOLO) 或 .json (labelme)</source>
        <translation>WARN 라벨 디렉터리는 존재하지만 {}장 이미지 모두에서 GT를 읽지 못했습니다. 라벨이 .txt (YOLO) 또는 .json (labelme)인지 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/train/test_runner.py" line="589"/>
        <source>WARN {} 张图缺标签文件</source>
        <translation>WARN {}장 이미지에 라벨 파일이 없습니다</translation>
    </message>
</context>
<context>
    <name>TestWorker</name>
    <message>
        <location filename="../app/train/test_worker.py" line="83"/>
        <source>run 开始</source>
        <translation>run 시작</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="97"/>
        <source>启动子进程: {} {}</source>
        <translation>하위 프로세스 시작: {} {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="109"/>
        <source>启动子进程失败: {}</source>
        <translation>하위 프로세스 시작 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="116"/>
        <source>启动测试进程失败: {}</source>
        <translation>테스트 프로세스 시작 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="118"/>
        <location filename="../app/train/test_worker.py" line="120"/>
        <source>子进程已启动 pid={}</source>
        <translation>하위 프로세스 시작됨 pid={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="152"/>
        <source>进入轮询循环</source>
        <translation>폴링 루프 진입</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="162"/>
        <source>轮询中: 文件={}B 已读{}行 子进程={}</source>
        <translation>폴링 중: 파일={}B 읽음 {}행 하위 프로세스={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="172"/>
        <source>轮询异常:
</source>
        <translation>폴링 예외:
</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="180"/>
        <source>轮询结束 rc={}</source>
        <translation>폴링 종료 rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="182"/>
        <source>子进程退出 rc={}</source>
        <translation>하위 프로세스 종료 rc={}</translation>
    </message>
    <message>
        <location filename="../app/train/test_worker.py" line="192"/>
        <source>测试未能完成, 详情见日志</source>
        <translation>테스트를 완료하지 못했습니다. 자세한 내용은 로그를 확인하세요</translation>
    </message>
</context>
<context>
    <name>TrainDialog</name>
    <message>
        <location filename="../ui/train.ui" line="14"/>
        <location filename="../ui/train.ui" line="40"/>
        <location filename="../app/train/dialogs.py" line="493"/>
        <source>训练</source>
        <translation>학습</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="50"/>
        <location filename="../ui/train.ui" line="169"/>
        <source>检测</source>
        <translation>객체 검출</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="118"/>
        <source>模型与数据</source>
        <translation>모델 및 데이터</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="158"/>
        <source>任务类型</source>
        <translation>작업 유형</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="174"/>
        <source>分割</source>
        <translation>세그멘테이션</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="179"/>
        <source>分类</source>
        <translation>분류</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="184"/>
        <source>异常检测</source>
        <translation>이상 검출</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="189"/>
        <source>字符检测</source>
        <translation>텍스트 검출</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="197"/>
        <source>型号</source>
        <translation>모델</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="210"/>
        <location filename="../app/train/dialogs.py" line="715"/>
        <source>训练集</source>
        <translation>학습 세트</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="230"/>
        <source>验证集</source>
        <translation>검증 세트</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="250"/>
        <source>设备</source>
        <translation>장치</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="263"/>
        <source>架构</source>
        <translation>아키텍처</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="296"/>
        <source>训练超参</source>
        <translation>학습 하이퍼파라미터</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="336"/>
        <location filename="../app/train/dialogs.py" line="589"/>
        <source>轮次</source>
        <translation>에포크</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="349"/>
        <source>优化器</source>
        <translation>옵티마이저</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="362"/>
        <location filename="../app/train/dialogs.py" line="592"/>
        <source>早停</source>
        <translation>조기 중단</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="399"/>
        <source>连续无提升则提前结束，0 为关闭</source>
        <translation>연속으로 개선이 없으면 조기 종료하며, 0은 사용 안 함</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="415"/>
        <location filename="../app/train/dialogs.py" line="595"/>
        <source>学习率</source>
        <translation>학습률</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="452"/>
        <source>初始学习率，训练中自动衰减</source>
        <translation>초기 학습률, 학습 중 자동 감소</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="468"/>
        <location filename="../app/train/dialogs.py" line="587"/>
        <source>批次</source>
        <translation>배치</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="481"/>
        <location filename="../app/train/dialogs.py" line="591"/>
        <source>图像尺寸</source>
        <translation>이미지 크기</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="512"/>
        <source>32 的倍数</source>
        <translation>32의 배수</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="528"/>
        <location filename="../app/train/dialogs.py" line="588"/>
        <source>梯度累积</source>
        <translation>그래디언트 누적</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="565"/>
        <source>显存不足时调大，等效批次 × N</source>
        <translation>VRAM이 부족할 때 늘리며, 실질 배치 × N</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="581"/>
        <location filename="../app/train/dialogs.py" line="590"/>
        <source>线程数</source>
        <translation>스레드 수</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="642"/>
        <source>数据增强</source>
        <translation>데이터 증강</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="723"/>
        <source>输出</source>
        <translation>출력</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="766"/>
        <source>输出路径</source>
        <translation>출력 경로</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="781"/>
        <source>留空则自动按时间生成目录</source>
        <translation>비워두면 시간 기준으로 디렉터리가 자동 생성됩니다</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="794"/>
        <source>选择路径</source>
        <translation>찾아보기</translation>
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
        <translation>학습 세트와 검증 세트를 선택하세요</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="903"/>
        <location filename="../app/train/dialogs.py" line="604"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="916"/>
        <location filename="../app/train/dialogs.py" line="1343"/>
        <location filename="../app/train/dialogs.py" line="1352"/>
        <location filename="../app/train/dialogs.py" line="1363"/>
        <location filename="../app/train/dialogs.py" line="1382"/>
        <location filename="../app/train/dialogs.py" line="1395"/>
        <source>加入队列</source>
        <translation>대기열에 추가</translation>
    </message>
    <message>
        <location filename="../ui/train.ui" line="929"/>
        <location filename="../app/train/dialogs.py" line="1274"/>
        <location filename="../app/train/dialogs.py" line="1284"/>
        <location filename="../app/train/dialogs.py" line="1310"/>
        <source>开始训练</source>
        <translation>학습 시작</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="40"/>
        <source>正在检测显卡...</source>
        <translation>GPU 감지 중...</translation>
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
        <translation>데이터셋 &quot;{}&quot;에 이미지가 없거나 경로가 유효하지 않습니다. 해당 데이터셋을 먼저 가져온 후 학습하세요</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="233"/>
        <source>数据集&quot;{}&quot;尚未导入标签或路径无效, 请先导入该数据集再训练</source>
        <translation>데이터셋 &quot;{}&quot;에 라벨이 없거나 경로가 유효하지 않습니다. 해당 데이터셋을 먼저 가져온 후 학습하세요</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="262"/>
        <location filename="../app/train/dialogs.py" line="1353"/>
        <source>请先选择输出路径</source>
        <translation>먼저 출력 경로를 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="22"/>
        <source>数据集&quot;{}/{}&quot;不是分类数据集(标签格式={}), 无法训练{}</source>
        <translation>데이터셋 &quot;{}/{}&quot;은(는) 분류 데이터셋이 아니므로(라벨 형식={}) {} 학습을 진행할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="28"/>
        <source>未知</source>
        <translation>알 수 없음</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="24"/>
        <source>数据集&quot;{}/{}&quot;是分类数据集, 无法训练{}任务</source>
        <translation>데이터셋 &quot;{}/{}&quot;은(는) 분류 데이터셋이므로 {} 작업을 학습할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="289"/>
        <source>请至少选择一个训练集数据集</source>
        <translation>학습 세트 데이터셋을 하나 이상 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="291"/>
        <source>请至少选择一个验证集数据集</source>
        <translation>검증 세트 데이터셋을 하나 이상 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="331"/>
        <source>未选数据集</source>
        <translation>선택된 데이터셋 없음</translation>
    </message>
    <message>
        <location filename="../app/train/detect_common.py" line="12"/>
        <source>目标检测推荐图像尺寸: 640(可设为 32 的倍数如 640/672)</source>
        <translation>객체 검출 권장 이미지 크기: 640(32의 배수로 설정 가능, 예: 640/672)</translation>
    </message>
    <message>
        <location filename="../app/train/segment_common.py" line="16"/>
        <source>CNN 分割推荐尺寸: 640(需为 32 的倍数)</source>
        <translation>CNN 세그멘테이션 권장 크기: 640(32의 배수여야 합니다)</translation>
    </message>
    <message>
        <location filename="../app/train/classify_common.py" line="27"/>
        <source>图像分类推荐尺寸: 224(小图用 224, 较大图可到 256)</source>
        <translation>이미지 분류 권장 크기: 224(작은 이미지는 224, 큰 이미지는 256까지)</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="695"/>
        <source>异常检测推荐尺寸: 256; 缺陷很小时调到 512 更稳, 显存和耗时随之上升</source>
        <translation>이상 검출 권장 크기: 256. 결함이 아주 작을 때는 512로 올리면 더 안정적이지만 VRAM과 소요 시간이 늘어납니다</translation>
    </message>
    <message>
        <location filename="../app/train/segment_common.py" line="17"/>
        <source>图像分割推荐尺寸: 648(需为 {} 的倍数)</source>
        <translation>이미지 세그멘테이션 권장 크기: 648({}의 배수여야 합니다)</translation>
    </message>
    <message>
        <location filename="../app/train/task_spec.py" line="26"/>
        <source>数据集&quot;{}/{}&quot;没有文本标注, 无法训练{}</source>
        <translation>데이터셋 &quot;{}/{}&quot;에 텍스트 어노테이션이 없어 {} 학습 불가</translation>
    </message>
    <message>
        <location filename="../app/train/ocr_common.py" line="56"/>
        <source>字符检测推荐尺寸: 1024(需为 {} 的倍数); 识别段固定 32x128, 不受此项影响</source>
        <translation>텍스트 검출 권장 크기: 1024({}의 배수여야 함); 인식 단계는 32x128로 고정되어 이 항목의 영향을 받지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="466"/>
        <source>{} 的倍数</source>
        <translation>{}의 배수</translation>
    </message>
    <message>
        <location filename="../app/train/classify_common.py" line="31"/>
        <source>建议 224</source>
        <translation>224 권장</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="700"/>
        <source>建议 256</source>
        <translation>256 권장</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="691"/>
        <source>训练集 {} 个 · 验证集 {} 个 · 共 {} 张图</source>
        <translation>학습 세트 {}개 · 검증 세트 {}개 · 총 {}장</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="694"/>
        <source>未选择验证集</source>
        <translation>검증 세트 미선택</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="696"/>
        <source>已标注, 可直接训练</source>
        <translation>라벨링 완료, 바로 학습 가능</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="698"/>
        <source>有 {} 个数据集尚未标注</source>
        <translation>라벨링되지 않은 데이터셋이 {}개 있습니다</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="712"/>
        <source>请选择验证集</source>
        <translation>검증 세트 선택</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="797"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>이미 학습이 진행 중입니다. 먼저 중지하세요</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="76"/>
        <source>几何变换</source>
        <translation>기하 변환</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="77"/>
        <source>标注框会跟着一起变换</source>
        <translation>바운딩 박스도 함께 변환</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="78"/>
        <source>像素变换</source>
        <translation>픽셀 변환</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="79"/>
        <source>只改画面，标注框不动</source>
        <translation>이미지만 변경, 바운딩 박스 그대로</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="82"/>
        <source>水平翻转</source>
        <translation>좌우 반전</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="84"/>
        <source>垂直翻转</source>
        <translation>상하 반전</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="86"/>
        <source>旋转</source>
        <translation>회전</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="87"/>
        <source>±15°</source>
        <translation>±15°</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="88"/>
        <source>仿射</source>
        <translation>아핀</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="90"/>
        <source>马赛克</source>
        <translation>모자이크</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="91"/>
        <source>4 图拼接</source>
        <translation>4장 결합</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="92"/>
        <source>亮度/对比度</source>
        <translation>밝기/대비</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="93"/>
        <source>±0.1</source>
        <translation>±0.1</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="94"/>
        <source>颜色抖动</source>
        <translation>색상 지터</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="95"/>
        <source>饱和/色相</source>
        <translation>채도/색조</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="96"/>
        <source>高斯模糊</source>
        <translation>가우시안 블러</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="97"/>
        <source>核 3</source>
        <translation>커널 3</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="98"/>
        <source>高斯噪声</source>
        <translation>가우시안 노이즈</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="99"/>
        <source>σ 0.05</source>
        <translation>σ 0.05</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="101"/>
        <source>已启用 {} 项</source>
        <translation>{} 개 활성화</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="102"/>
        <source>该任务不支持配置数据增强</source>
        <translation>이 작업은 데이터 증강 설정을 지원하지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="104"/>
        <source>当前网络架构不支持该增强</source>
        <translation>현재 네트워크 아키텍처에서는 이 증강을 지원하지 않습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="722"/>
        <source>异常检测算法自带学习率与优化器, 不需要设置</source>
        <translation>이상 검출 알고리즘은 학습률과 옵티마이저를 자체적으로 사용하므로 설정할 필요가 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="728"/>
        <source>建库型算法只提取特征建立记忆库, 没有训练轮次</source>
        <translation>뱅크 구축형 알고리즘은 특징만 추출해 메모리 뱅크를 구축하며 학습 에포크가 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/ad_common.py" line="669"/>
        <source>仅建库</source>
        <translation>뱅크 구축만</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1210"/>
        <source>请至少选择一个数据集</source>
        <translation>데이터셋을 하나 이상 선택하세요</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1214"/>
        <location filename="../app/train/dialogs.py" line="1224"/>
        <source>&quot;{}&quot;不能为空</source>
        <translation>&quot;{}&quot;은(는) 비워둘 수 없습니다</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1219"/>
        <source>&quot;{}&quot;必须是整数(当前: {})</source>
        <translation>&quot;{}&quot;은(는) 정수여야 합니다(현재: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1229"/>
        <source>&quot;{}&quot;必须是数字(当前: {})</source>
        <translation>&quot;{}&quot;은(는) 숫자여야 합니다(현재: {})</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1238"/>
        <source>图像尺寸需为 {} 的倍数(当前 {}), 可改为 {}</source>
        <translation>이미지 크기는 {}의 배수여야 합니다(현재 {}). {}로 변경할 수 있습니다</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1254"/>
        <source>选择输出目录</source>
        <translation>출력 디렉터리 선택</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1268"/>
        <source>当前安装缺少 CNN 架构所需的组件, 无法训练.
请重新安装软件后再试</source>
        <translation>현재 설치에 CNN 아키텍처에 필요한 구성 요소가 없어 학습을 시작할 수 없습니다.
소프트웨어를 다시 설치한 후 시도해 주세요</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1275"/>
        <source>当前已有训练在进行中, 请先停止!</source>
        <translation>현재 학습이 진행 중입니다. 먼저 중지하세요!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1279"/>
        <source>参数校验未通过: {}</source>
        <translation>파라미터 검증 실패: {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1280"/>
        <location filename="../app/train/dialogs.py" line="1339"/>
        <source>参数校验</source>
        <translation>파라미터 검증</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1300"/>
        <source>训练启动失败: {}
{}</source>
        <translation>학습 시작 실패: {}
{}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1303"/>
        <source>训练启动失败</source>
        <translation>학습 시작 실패</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1311"/>
        <source>已有训练在进行中, 请先停止!</source>
        <translation>이미 학습이 진행 중입니다. 먼저 중지하세요!</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1313"/>
        <source>开始训练: 任务类型={} 训练集={} 验证集={}</source>
        <translation>학습 시작: 작업 유형={} 학습 세트={} 검증 세트={}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1329"/>
        <source>开始训练: 字符检测分两段入队 | {} | {}</source>
        <translation>학습 시작: 텍스트 검출이 두 단계로 나뉘어 대기열에 추가됨 | {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1368"/>
        <source>队列</source>
        <translation>대기열</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1369"/>
        <source>已更新该队列任务的参数</source>
        <translation>대기열 작업의 파라미터를 업데이트했습니다</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1375"/>
        <source>加入队列失败</source>
        <translation>대기열 추가 실패</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1378"/>
        <source>加入训练队列: {} | {}</source>
        <translation>학습 대기열에 추가: {} | {}</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1383"/>
        <source>已加入队列(第 {} 个), 可在首页&quot;队列&quot;中查看或启动.</source>
        <translation>대기열에 추가되었습니다({}번째). 홈 화면의 &quot;대기열&quot;에서 확인하거나 시작할 수 있습니다.</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="1396"/>
        <source>字符检测已拆成检测段与识别段, 分别排在第 {} 和第 {} 个</source>
        <translation>텍스트 검출이 검출 단계와 인식 단계로 나뉘어 각각 {}번째와 {}번째에 배치되었습니다</translation>
    </message>
</context>
<context>
    <name>TrainMixin</name>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="47"/>
        <source>{} 训练中 0/{}</source>
        <translation>{} 학습 중 0/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="86"/>
        <source>[train] 训练线程已结束但未返回结果, 按失败收尾</source>
        <translation>[train] 학습 스레드가 종료되었지만 결과가 반환되지 않아 실패로 처리합니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="97"/>
        <source>仅停止当前</source>
        <translation>현재 작업만 중지</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="98"/>
        <source>停止队列</source>
        <translation>대기열 중지</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <location filename="../app/mixins/train_mixin.py" line="121"/>
        <source>停止训练</source>
        <translation>학습 중지</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="100"/>
        <source>当前正在跑训练队列, 要停止到什么范围?</source>
        <translation>현재 학습 대기열이 실행 중입니다. 어디까지 중지할까요?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="102"/>
        <location filename="../app/mixins/train_mixin.py" line="103"/>
        <source>取消</source>
        <translation>취소</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="109"/>
        <source>确定要停止当前训练吗?</source>
        <translation>현재 학습을 중지하시겠습니까?</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="117"/>
        <source>手动停止训练: {}</source>
        <translation>수동으로 학습 중지: {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="119"/>
        <source>[train] 训练进程 10 秒内未退出, 可能有子进程残留占用显存</source>
        <translation>[train] 학습 프로세스가 10초 내에 종료되지 않았습니다. 하위 프로세스가 남아 VRAM을 점유하고 있을 수 있습니다</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="122"/>
        <source>训练进程未能完全退出, 可能仍有子进程占用显存.
建议稍等片刻再启动下一个任务.</source>
        <translation>학습 프로세스가 완전히 종료되지 않았습니다. 하위 프로세스가 아직 VRAM을 점유하고 있을 수 있습니다.
잠시 기다린 후 다음 작업을 시작하는 것을 권장합니다.</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="134"/>
        <source>{} 训练中 {}/{}</source>
        <translation>{} 학습 중 {}/{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="147"/>
        <source>进度 | 当前最好 {}</source>
        <translation>진행률 | 현재 최고 {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="211"/>
        <source>更新训练指标: record={} 已完成epoch={} {}={} 类别数={}</source>
        <translation>학습 지표 업데이트: record={} 완료 epoch={} {}={} 클래스 수={}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="310"/>
        <source>等待显存释放 · 下一项:{}</source>
        <translation>VRAM 해제 대기 · 다음:{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="187"/>
        <source>训练失败(队列模式, 已跳过弹窗): {}</source>
        <translation>학습 실패(대기열 모드, 팝업 건너뜀): {}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="189"/>
        <source>训练失败</source>
        <translation>학습 실패</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="190"/>
        <source>训练过程中发生错误, Err:

{}</source>
        <translation>학습 중 오류가 발생했습니다, Err:

{}</translation>
    </message>
    <message>
        <location filename="../app/mixins/train_mixin.py" line="283"/>
        <source>已保存模型记录: {} | {}</source>
        <translation>모델 기록 저장됨: {} | {}</translation>
    </message>
</context>
<context>
    <name>TrainQueueDialog</name>
    <message>
        <location filename="../ui/train_queue.ui" line="14"/>
        <location filename="../ui/train_queue.ui" line="40"/>
        <location filename="../app/widgets/queue_dialog.py" line="33"/>
        <source>训练队列</source>
        <translation>학습 대기열</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="50"/>
        <location filename="../app/widgets/queue_dialog.py" line="123"/>
        <source>空闲</source>
        <translation>유휴</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="93"/>
        <source>#</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="98"/>
        <source>名称</source>
        <translation>이름</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="103"/>
        <source>任务</source>
        <translation>작업</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="108"/>
        <source>数据集</source>
        <translation>데이터셋</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="113"/>
        <source>型号</source>
        <translation>모델</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="118"/>
        <source>轮次</source>
        <translation>에포크</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="123"/>
        <source>状态</source>
        <translation>상태</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="152"/>
        <source>i</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="168"/>
        <source>队列为空，可在训练界面点「加入队列」添加任务</source>
        <translation>대기열이 비어 있습니다. 학습 화면에서 「대기열에 추가」를 눌러 작업을 추가할 수 있습니다</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="199"/>
        <source>上移</source>
        <translation>위로</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="209"/>
        <source>下移</source>
        <translation>아래로</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="219"/>
        <location filename="../app/widgets/queue_dialog.py" line="255"/>
        <source>移除</source>
        <translation>제거</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="229"/>
        <source>清理已结束</source>
        <translation>종료된 항목 정리</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="252"/>
        <source>编辑</source>
        <translation>편집</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="259"/>
        <source>关闭</source>
        <translation>닫기</translation>
    </message>
    <message>
        <location filename="../ui/train_queue.ui" line="272"/>
        <location filename="../app/widgets/queue_dialog.py" line="144"/>
        <source>开始队列</source>
        <translation>대기열 시작</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="22"/>
        <source>队列为空, 可在训练界面点&quot;加入队列&quot;添加任务</source>
        <translation>대기열이 비어 있습니다. 학습 화면에서 &quot;대기열에 추가&quot;를 눌러 작업을 추가할 수 있습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>运行中</source>
        <translation>실행 중</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="113"/>
        <source>队列正在串行执行</source>
        <translation>대기열이 순차적으로 실행 중입니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="115"/>
        <source>待启动</source>
        <translation>시작 대기</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="116"/>
        <source>有 {} 个任务等待启动</source>
        <translation>시작을 기다리는 작업이 {}개 있습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>训练中</source>
        <translation>학습 중</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="118"/>
        <source>当前有训练在进行(非队列启动)</source>
        <translation>현재 학습이 진행 중입니다(대기열로 시작되지 않음)</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="120"/>
        <source>已结束</source>
        <translation>종료됨</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="121"/>
        <source>没有待执行的任务, 点&quot;重新开始队列&quot;可重跑</source>
        <translation>실행할 작업이 없습니다. &quot;대기열 다시 시작&quot;을 누르면 다시 실행할 수 있습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="127"/>
        <source>共 {} 个: 等待 {} · 完成 {} · 失败 {}</source>
        <translation>총 {}개: 대기 {} · 완료 {} · 실패 {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="130"/>
        <source>正在训练&quot;{}&quot; · {}</source>
        <translation>&quot;{}&quot; 학습 중 · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="133"/>
        <source>下一个: &quot;{}&quot; · {}</source>
        <translation>다음: &quot;{}&quot; · {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="146"/>
        <location filename="../app/widgets/queue_dialog.py" line="183"/>
        <source>重新开始队列</source>
        <translation>대기열 다시 시작</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="168"/>
        <location filename="../app/widgets/queue_dialog.py" line="190"/>
        <source>队列</source>
        <translation>대기열</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="169"/>
        <source>已有训练在进行中, 请先停止</source>
        <translation>이미 학습이 진행 중입니다. 먼저 중지하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="178"/>
        <source>{} 个{}</source>
        <translation>{}개 {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="184"/>
        <source>队列中没有等待中的任务.

待重跑: {}

是否重新入队并开始训练?</source>
        <translation>대기열에 대기 중인 작업이 없습니다.

다시 실행: {}

다시 대기열에 넣고 학습을 시작하시겠습니까?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="191"/>
        <source>队列启动失败, 请查看日志</source>
        <translation>대기열 시작 실패, 로그를 확인하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="207"/>
        <location filename="../app/widgets/queue_dialog.py" line="211"/>
        <source>移除任务</source>
        <translation>작업 제거</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="208"/>
        <source>训练中的任务不能移除, 请先停止</source>
        <translation>학습 중인 작업은 제거할 수 없습니다. 먼저 중지하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="212"/>
        <source>确定从队列中移除&quot;{}&quot;吗?</source>
        <translation>대기열에서 &quot;{}&quot;을(를) 제거하시겠습니까?</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="219"/>
        <source>清理</source>
        <translation>정리</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="220"/>
        <source>没有已结束的任务</source>
        <translation>종료된 작업이 없습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="222"/>
        <source>[队列] 已清理 {} 个已结束任务</source>
        <translation>[队列] 종료된 작업 {}개를 정리했습니다</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="229"/>
        <source>编辑任务</source>
        <translation>작업 편집</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="230"/>
        <source>训练中的任务不能编辑, 请先停止</source>
        <translation>학습 중인 작업은 편집할 수 없습니다. 먼저 중지하세요</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="246"/>
        <source>重新入队</source>
        <translation>대기열에 다시 추가</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="248"/>
        <location filename="../app/widgets/queue_dialog.py" line="269"/>
        <source>打开输出目录</source>
        <translation>출력 디렉터리 열기</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="250"/>
        <source>在模型界面查看</source>
        <translation>모델 화면에서 보기</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="270"/>
        <source>目录不存在: {}</source>
        <translation>디렉터리가 없습니다: {}</translation>
    </message>
    <message>
        <location filename="../app/widgets/queue_dialog.py" line="271"/>
        <source>未设置</source>
        <translation>미설정</translation>
    </message>
</context>
<context>
    <name>TrainRunner</name>
    <message>
        <location filename="../app/train/train_runner.py" line="114"/>
        <source>数据增强需要 kornia 或 albumentations, 当前环境两者都没有.
请把训练参数里的&quot;数据增强&quot;全部取消勾选, 或补装组件后重试</source>
        <translation>데이터 증강에는 kornia 또는 albumentations가 필요하지만 둘 다 설치되어 있지 않습니다.
학습 설정의 &quot;데이터 증강&quot;을 모두 해제하거나 하나를 설치한 뒤 다시 시도하세요</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="131"/>
        <location filename="../app/train/yolo_train_runner.py" line="217"/>
        <source>输出路径: {}</source>
        <translation>출력 경로: {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="132"/>
        <location filename="../app/train/yolo_train_runner.py" line="218"/>
        <source>本次训练输出目录(时间戳): {}</source>
        <translation>이번 학습 출력 디렉터리(타임스탬프): {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="134"/>
        <source>训练配置文件已保存 → {}</source>
        <translation>학습 설정 파일 저장됨 → {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="156"/>
        <source>分割模型 resolution 已自动取整: {} → {} (block={})</source>
        <translation>세그멘테이션 모델 resolution 자동 정수화: {} → {} (block={})</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="158"/>
        <location filename="../app/train/yolo_train_runner.py" line="255"/>
        <source>使用模型 {} device={} epochs={} batch={} resolution={}</source>
        <translation>사용 모델 {} device={} epochs={} batch={} resolution={}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="169"/>
        <location filename="../app/train/yolo_train_runner.py" line="267"/>
        <source>数据增强: {}</source>
        <translation>데이터 증강: {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="172"/>
        <location filename="../app/train/yolo_train_runner.py" line="270"/>
        <source>数据增强: 未启用</source>
        <translation>데이터 증강: 사용 안 함</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="240"/>
        <location filename="../app/train/yolo_train_runner.py" line="296"/>
        <source>训练完成</source>
        <translation>학습 완료</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="249"/>
        <location filename="../app/train/yolo_train_runner.py" line="303"/>
        <source>生成类别文件: {}</source>
        <translation>클래스 파일 생성: {}</translation>
    </message>
    <message>
        <location filename="../app/train/train_runner.py" line="143"/>
        <location filename="../app/train/yolo_train_runner.py" line="224"/>
        <source>预训练权重缺失: 请先在权重管理里下载 {} 档的模型</source>
        <translation>사전 학습 가중치 누락: 먼저 가중치 관리에서 {} 등급 모델을 다운로드하세요</translation>
    </message>
</context>
<context>
    <name>TrainWorker</name>
    <message>
        <location filename="../app/train/train_worker.py" line="486"/>
        <source>训练监控异常, 已终止.

{}</source>
        <translation>학습 모니터링 오류로 종료되었습니다.

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="495"/>
        <source>训练结果文件读取失败: {}

{}</source>
        <translation>학습 결과 파일 읽기 실패: {}

{}</translation>
    </message>
    <message>
        <location filename="../app/train/train_worker.py" line="500"/>
        <source>训练进程异常退出 (code={})

--- 子进程输出(尾部) ---
{}</source>
        <translation>학습 프로세스가 비정상 종료되었습니다 (code={})

--- 하위 프로세스 출력(끝부분) ---
{}</translation>
    </message>
</context>
<context>
    <name>Utils</name>
    <message>
        <location filename="../app/core/utils.py" line="59"/>
        <location filename="../app/core/utils.py" line="71"/>
        <source>{}秒</source>
        <translation>{}초 </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="65"/>
        <source>{}天</source>
        <translation>{}일 </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="67"/>
        <source>{}小时</source>
        <translation>{}시간 </translation>
    </message>
    <message>
        <location filename="../app/core/utils.py" line="69"/>
        <source>{}分</source>
        <translation>{}분 </translation>
    </message>
</context>
<context>
    <name>_ModelRow</name>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="119"/>
        <location filename="../app/widgets/model_manager_dialog.py" line="171"/>
        <source>本地</source>
        <translation>로컬</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="142"/>
        <source>取消本地绑定</source>
        <translation>로컬 연결 해제</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="177"/>
        <source>已就绪</source>
        <translation>준비됨</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="184"/>
        <source>未下载</source>
        <translation>다운로드되지 않음</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="193"/>
        <source>更换</source>
        <translation>변경</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="201"/>
        <source>本地权重</source>
        <translation>로컬 가중치</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="210"/>
        <source>重选</source>
        <translation>다시 선택</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="211"/>
        <source>(路径未记录)</source>
        <translation>(경로 미기록)</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="213"/>
        <source>本地失效</source>
        <translation>로컬 가중치 없음</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="215"/>
        <source>登记的本地权重文件已不在这个位置:
{}</source>
        <translation>등록된 로컬 가중치 파일이 더 이상 이 위치에 없습니다:
{}</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="220"/>
        <source>校验中...</source>
        <translation>검증 중...</translation>
    </message>
    <message>
        <location filename="../app/widgets/model_manager_dialog.py" line="239"/>
        <source>失败</source>
        <translation>실패</translation>
    </message>
</context>
<context>
    <name>_PixelScaleDialog</name>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="108"/>
        <source>像素精度</source>
        <translation>픽셀 정밀도</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="114"/>
        <source>1 像素代表的实际长度</source>
        <translation>1 픽셀이 나타내는 실제 길이</translation>
    </message>
    <message>
        <location filename="../app/annotation/annotation_dialog.py" line="147"/>
        <source>请输入大于 0 的数字</source>
        <translation>0보다 큰 숫자를 입력하세요</translation>
    </message>
</context>
<context>
    <name>_TrainStartDialog</name>
    <message>
        <location filename="../app/train/dialogs.py" line="341"/>
        <source>训练即将开始</source>
        <translation>학습이 곧 시작됩니다</translation>
    </message>
    <message>
        <location filename="../app/train/dialogs.py" line="351"/>
        <location filename="../app/train/dialogs.py" line="364"/>
        <source>确认({})</source>
        <translation>확인({})</translation>
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
        <translation>가져오기</translation>
    </message>
    <message>
        <location filename="../ui/add_label.ui" line="284"/>
        <source>确定</source>
        <translation>확인</translation>
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
        <translation>사각형</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="35"/>
        <source>多边形</source>
        <translation>다각형</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="46"/>
        <source>删除图像</source>
        <translation>이미지 삭제</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="70"/>
        <source>设置</source>
        <translation>설정</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="90"/>
        <source>标签列表</source>
        <translation>라벨 목록</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="113"/>
        <source>添加标签</source>
        <translation>라벨 추가</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="116"/>
        <source>+</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="160"/>
        <source>标注信息</source>
        <translation>어노테이션 정보</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="180"/>
        <source>转换</source>
        <translation>변환</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="210"/>
        <source>图像信息</source>
        <translation>이미지 정보</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="237"/>
        <source>剪切板</source>
        <translation>클립보드</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="302"/>
        <source>上一张(A)</source>
        <translation>이전(A)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="309"/>
        <source>下一张(D)</source>
        <translation>다음(D)</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="359"/>
        <source>标注参数</source>
        <translation>어노테이션 파라미터</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="371"/>
        <source>角度范围</source>
        <translation>각도 범위</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="385"/>
        <source>~</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="419"/>
        <source>融合强度</source>
        <translation>블렌드 강도</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="453"/>
        <source>亮度调节</source>
        <translation>밝기</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="487"/>
        <source>填充颜色</source>
        <translation>채우기 색상</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="494"/>
        <source>点击打开取色器, 选任意颜色</source>
        <translation>클릭하면 색상 선택기가 열립니다. 아무 색이나 고르세요</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="507"/>
        <source>支持 #RRGGBB / #RGB / 255,255,255 / black / 白 等写法, 也可以点左边色块打开取色器</source>
        <translation>#RRGGBB / #RGB / 255,255,255 / black / 흰색 등의 표기를 지원하며, 왼쪽 색상 칸을 클릭해 색상 선택기를 열 수도 있습니다</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="510"/>
        <source>#RRGGBB</source>
        <translation type="unfinished"></translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="517"/>
        <source>自定义颜色</source>
        <translation>사용자 지정 색상</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="544"/>
        <source>常用色</source>
        <translation>자주 쓰는 색</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="575"/>
        <source>恢复默认</source>
        <translation>기본값 복원</translation>
    </message>
    <message>
        <location filename="../ui/annotation.ui" line="595"/>
        <source>完成</source>
        <translation>완료</translation>
    </message>
</context>
</TS>
