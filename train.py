from rfdetr import RFDETRSegSmall

if __name__ == '__main__':
    model = RFDETRSegSmall() 
    
    # 추천: VRAM 16GB 기준 가장 빠른 설정
    model.train(
        dataset_dir="raw_teacher_dataset",
        epochs=100,            # 100 에포크로 변경
        batch_size=8,         # 최대한 늘림 (VRAM 에러 시 8로 감소)
        grad_accum_steps=2,    # batch * grad_accum = 16 유지 (8로 낮추면 2로 변경)
        num_workers=6          # 데이터 로딩 병목 현상 제거 (에러 시 4로 감소)
    )