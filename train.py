from rfdetr import RFDETRSegSmall

if __name__ == '__main__':
    # 1. 모델 불러오기
    model = RFDETRSegSmall() 
    
    # 2. 학습 시작 (반드시 __main__ 블록 안쪽에 위치)
    model.train(
        dataset_dir="raw_teacher_dataset", # 가지고 계신 데이터셋 폴더 경로로 변경
        epochs=10,
        batch_size=4,        # GPU VRAM에 맞춰 조절 (예: 4)
        grad_accum_steps=4   # batch_size * grad_accum_steps = 16 권장
    )