import os
import shutil
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from tqdm import tqdm

from rfdetr import RFDETRSegSmall


def build_unet_dataset(
    input_dir="sd_images",
    output_dir="unet_dataset",
    checkpoint_path="output/checkpoint_best_total.pth",
    threshold=0.5,
):
    """
    RF-DETR Segmentation 결과를 이용하여
    U-Net 학습용 Binary Mask Dataset 생성

    output_dir/
        images/
        masks/
    """

    images_dir = Path(output_dir) / "images"
    masks_dir = Path(output_dir) / "masks"

    images_dir.mkdir(parents=True, exist_ok=True)
    masks_dir.mkdir(parents=True, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[INFO] Device: {device}")
    print("[INFO] Loading model...")

    model = RFDETRSegSmall.from_checkpoint(
        checkpoint_path
    )

    try:
        model.model.to(device)
    except Exception:
        pass

    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
    }

    image_paths = [
        p for p in Path(input_dir).iterdir()
        if p.suffix.lower() in image_extensions
    ]

    image_paths = sorted(
        image_paths,
        key=lambda x: x.name
    )

    print(f"[INFO] Found {len(image_paths)} images")

    success_count = 0
    empty_count = 0

    for image_path in tqdm(image_paths):

        try:
            image = Image.open(image_path).convert("RGB")
            image_np = np.array(image)

            with torch.inference_mode():

                detections = model.predict(
                    image_np,
                    threshold=threshold
                )

            height, width = image_np.shape[:2]

            # -----------------------
            # Binary Mask 생성
            # -----------------------

            if (
                detections.mask is not None
                and len(detections.mask) > 0
            ):

                combined_mask = np.any(
                    detections.mask,
                    axis=0
                )

                mask_img = (
                    combined_mask.astype(np.uint8)
                    * 255
                )

                success_count += 1

            else:
                # 검출 실패 시 빈 마스크 생성
                mask_img = np.zeros(
                    (height, width),
                    dtype=np.uint8
                )

                empty_count += 1

            # -----------------------
            # 원본 이미지 저장
            # -----------------------

            image_output_path = (
                images_dir /
                image_path.name
            )

            shutil.copy2(
                image_path,
                image_output_path
            )

            # -----------------------
            # Binary Mask 저장
            # -----------------------

            mask_output_path = (
                masks_dir /
                f"{image_path.stem}.png"
            )

            Image.fromarray(mask_img).save(
                mask_output_path
            )

        except Exception as e:

            print(
                f"[ERROR] {image_path.name}"
            )
            print(e)

    print()
    print("[INFO] Finished")
    print(f"[INFO] Valid Masks : {success_count}")
    print(f"[INFO] Empty Masks : {empty_count}")


if __name__ == "__main__":

    build_unet_dataset(
        input_dir="sd_images",
        output_dir="unet_dataset",
        checkpoint_path="output/checkpoint_best_total.pth",
        threshold=0.5,
    )