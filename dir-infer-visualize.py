import os
from pathlib import Path

import supervision as sv
from PIL import Image

# RF-DETR Segmentation 모델
from rfdetr import RFDETRSegSmall


def run_batch_inference(
    input_dir = "test_images",
    output_dir="output_results",
    checkpoint_path="output/checkpoint_best_total.pth",
    threshold=0.5,
):
    # 출력 폴더 생성
    os.makedirs(output_dir, exist_ok=True)

    # 모델 로드
    print("[INFO] Loading model...")
    model = RFDETRSegSmall()
    model = model.from_checkpoint(checkpoint_path)

    # supervision annotator
    color = sv.ColorPalette.DEFAULT

    mask_annotator = sv.MaskAnnotator(color=color)

    label_annotator = sv.LabelAnnotator(
        color=color,
        text_color=sv.Color.BLACK,
        smart_position=True
    )

    # 지원 이미지 확장자
    image_extensions = [".jpg", ".jpeg", ".png", ".webp", ".bmp"]

    image_paths = []

    for ext in image_extensions:
        image_paths.extend(Path(input_dir).glob(f"*{ext}"))
        image_paths.extend(Path(input_dir).glob(f"*{ext.upper()}"))

    print(f"[INFO] Found {len(image_paths)} images")

    # 이미지 순회
    for image_path in image_paths:
        print(f"[INFO] Processing: {image_path.name}")

        try:
            # 이미지 로드
            image = Image.open(image_path).convert("RGB")

            # 추론
            detections = model.predict(image, threshold=threshold)

            # PIL → numpy
            annotated_image = image.copy()

            # 마스크 시각화
            if detections.mask is not None and len(detections.mask) > 0:
                annotated_image = mask_annotator.annotate(
                    scene=annotated_image,
                    detections=detections
                )

            # label 생성
            labels = [
                f"facemask {conf:.2f}"
                for conf in detections.confidence
            ]

            # label 시각화
            annotated_image = label_annotator.annotate(
                annotated_image,
                detections,
                labels
            )

            # 저장 경로
            output_path = os.path.join(
                output_dir,
                f"{image_path.stem}_annotated.jpg"
            )

            # 저장
            if isinstance(annotated_image, Image.Image):
                annotated_image.save(output_path)
            else:
                Image.fromarray(annotated_image).save(output_path)

            print(f"[INFO] Saved: {output_path}")

        except Exception as e:
            print(f"[ERROR] Failed on {image_path.name}")
            print(e)

    print("[INFO] Done!")


if __name__ == "__main__":
    run_batch_inference(
        input_dir="sd_images",                 # 원본 이미지 폴더
        output_dir="output_results",           # 결과 저장 폴더
        checkpoint_path="output/checkpoint_best_total.pth",
        threshold=0.5
    )