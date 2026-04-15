# Scripts 디렉토리 — 운영 자동화 스크립트

## 스크립트 목록

| 스크립트 | 시나리오 | 실행 시점 |
|----------|----------|-----------|
| `build.sh` | manifest.yaml 기반으로 models/serving/ → model_repository/ 동기화 | CI/CD, 로컬 개발 |
| `validate.sh` | 모든 config.pbtxt 유효성 검사 | PR 시, 배포 전 |
| `health_check.sh` | 서버 및 모델별 상태 확인 | 배포 후, 모니터링 |
| `convert/to_onnx.py` | PyTorch → ONNX 변환 | 모델 업데이트 시 |
| `convert/to_tensorrt.sh` | ONNX → TensorRT 변환 | CI/CD |
| `convert/to_torchscript.py` | PyTorch → TorchScript 변환 | 모델 업데이트 시 |
| `convert/to_fil.py` | sklearn/XGBoost → FIL 변환 | 모델 업데이트 시 |
| `model_control/load.sh` | 런타임 모델 로드 | 무중단 배포 |
| `model_control/unload.sh` | 런타임 모델 언로드 | 무중단 교체 |
| `model_control/reload.sh` | unload → 배치 → load 시퀀스 | 무중단 교체 |
