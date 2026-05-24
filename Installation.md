# 의존성 패키지 설치법

## Python 버전 고정

RF-DETR 계열은 현재 Python 3.11 추천.

```bash
uv python install 3.11
uv venv --python 3.11
```

활성화:

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows PowerShell

```bash
.venv\Scripts\activate
```

## PyTorch 설치

```bash
# CUDA 12.6 전용 PyTorch 다운로드로 변경 (안정성 최상)
uv add torch torchvision --index https://download.pytorch.org/whl/cu126

# RF-DETR 설치
uv add "rfdetr[train,loggers]" --index-strategy unsafe-best-match
```

### 추가 추천 패키지

```bash
uv add opencv-python pycocotools supervision matplotlib tqdm
```