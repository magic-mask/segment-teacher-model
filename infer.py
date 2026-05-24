import supervision as sv
from PIL import Image
# 범용 Model 대신 학습 시 사용한 구체적인 클래스를 임포트합니다.
from rfdetr import RFDETRSegSmall 

if __name__ == '__main__':
    # 1. 테스트할 단일 이미지 로드
    image = Image.open("test/mask_dataset_0.png") # 테스트할 이미지 파일명으로 변경하세요

    # 2. 커스텀 학습된 가중치 불러오기
    # output 폴더 내부에 생성된 가장 최신 가중치 파일 경로를 입력하세요.
    # PyTorch Lightning은 보통 .ckpt 확장자로 저장합니다 (예: output/checkpoints/best.ckpt)
    checkpoint_path = "output/checkpoint_best_total.pth" # 실제 폴더에 있는 파일명으로 수정 필수!
    
    model = RFDETRSegSmall()
    # 체크포인트를 로드하여 덮어씌웁니다 (rfdetr/pytorch_lightning 표준 방식)
    model = model.from_checkpoint(checkpoint_path)
    #model.eval() # 추론 모드로 전환

    # 3. 추론 실행
    detections = model.predict(image, threshold=0.5)

    # 4. 시각화 (커스텀 클래스 지정)
    color = sv.ColorPalette.DEFAULT
    box_annotator = sv.BoxAnnotator(color=color)
    label_annotator = sv.LabelAnnotator(
        color=color, 
        text_color=sv.Color.BLACK, 
        smart_position=True
    )

    # 마스크 어노테이터 (주의사항 참조)
    mask_annotator = sv.MaskAnnotator(color=color)

    # 데이터셋에 facemask 하나뿐이므로 하드코딩합니다.
    labels = [f"facemask {conf:.2f}" for conf in detections.confidence]

    annotated_image = image.copy()
    
    # 예측 결과에 마스크 데이터가 존재할 때만 마스크를 그립니다.
    if detections.mask is not None:
        annotated_image = mask_annotator.annotate(annotated_image, detections)
        
    annotated_image = box_annotator.annotate(annotated_image, detections)
    annotated_image = label_annotator.annotate(annotated_image, detections, labels)

    # 결과 이미지 출력
    annotated_image.show()