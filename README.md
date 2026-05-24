# Teacher Segmentation Model

## 목적

이 저장소는 Face Mask Segmentation용 Teacher 모델을 학습하기 위한 레포지토리입니다.

Teacher 모델은 최종 서비스 모델이 아니며, 내부 Auto-Labeling 용도로만 사용됩니다.

최종 배포 및 상업적 사용은 별도의 Clean Dataset 기반 Student 모델만 대상으로 합니다.

### 패키지 설치는 해당 문서를 참조해주세요
[Installation.md](./Installation.md)

---

# 사용 데이터셋 관련 사항

본 저장소에서는 Roboflow Universe에 공개된 ROSA Face Mask Segmentation 데이터셋을 사용합니다.

https://universe.roboflow.com/rosa-v4waj/rosa-face-mask-segmentation

하지만 다음 문제가 존재합니다.

* 일부 원본 이미지 출처(Provenance)가 명확하지 않음
* 웹 이미지 / 개인 촬영 / 공개 이미지 등이 혼합되었을 가능성 존재
* 원본 이미지의 저작권 상태를 완전히 검증할 수 없음

따라서:

* 본 저장소는 ROSA 데이터셋 자체를 재배포하지 않음
* 원본 이미지 파일을 포함하지 않음
* annotation 원본 파일을 포함하지 않음

본 저장소는 Teacher 모델 학습 코드만 관리합니다.

---

# Teacher 모델의 역할

Teacher 모델은 다음 목적에만 사용합니다.

1. 저작권 문제가 없는 Clean 이미지에 대해 Auto Label 생성
2. 라벨링 작업 시간 단축
3. Human-in-the-loop 방식의 초기 segmentation bootstrap

Teacher 모델 출력은 최종 Ground Truth가 아닙니다.

---

# Student Dataset 생성 방식

최종 Student Dataset은 아래 방식으로 생성합니다.

1. Teacher 모델이 Clean 이미지에 대해 segmentation 생성
2. 사람이 직접 polygon 및 mask 수정
3. 수정된 annotation만 최종 dataset에 사용

즉:

* 최종 annotation은 사람의 검수 및 수정 과정을 거침
* 단순 원본 annotation 복제가 아님
* 최종 dataset은 독립적으로 구축된 Clean Dataset임

---

# Student 모델의 상업적 사용 가능 이유

최종 Student 모델은 다음 데이터만 사용하여 학습합니다.

* 직접 촬영한 이미지
* 상업적 사용 가능한 이미지
* AI 생성 이미지
* 사람이 검수한 최종 annotation

즉 최종 Student 모델에는:

* ROSA 원본 이미지 미포함
* ROSA annotation 미포함
* 불분명한 출처의 이미지 미포함

Teacher 모델은 단순 Auto-Labeling 도구 역할만 수행합니다.

최종 Student 모델은 Clean Dataset 기반으로 독립적으로 재학습됩니다.

---

# Teacher 모델 정책

Teacher 모델은 임시 Bootstrap 용도로만 사용합니다.

권장 정책:

* Teacher checkpoint 공개 금지
* Teacher dataset 재배포 금지
* Teacher annotation 재배포 금지
* Student 모델 구축 완료 후 Teacher pipeline 폐기 또는 비공개 보관

---

# 최종 원칙

공개 및 상업적 사용 대상:

* Clean Dataset
* Human-reviewed annotation
* Student 모델

비공개 유지 대상:

* Teacher dataset
* Teacher annotation
* Teacher checkpoint
