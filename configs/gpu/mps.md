# CUDA Multi-Process Service (MPS) 설정 가이드

## MPS란?

CUDA MPS는 여러 프로세스가 하나의 GPU를 효율적으로 공유하게 해주는 서비스입니다.
Triton에서 여러 모델 인스턴스가 있을 때 GPU 자원 공유 효율을 높입니다.

## 활성화 절차

```bash
# 1. MPS 데몬 시작
export CUDA_VISIBLE_DEVICES=0
nvidia-cuda-mps-control -d

# 2. GPU exclusive 모드로 변경 (필수)
sudo nvidia-smi -i 0 -c EXCLUSIVE_PROCESS

# 3. Triton 서버 시작 (MPS가 자동으로 적용됨)
tritonserver --model-repository=/models ...
```

## 종료 절차

```bash
echo quit | nvidia-cuda-mps-control
sudo nvidia-smi -i 0 -c DEFAULT
```

## Docker에서의 MPS

```yaml
# docker-compose.yml
services:
  triton:
    # MPS는 호스트에서 미리 활성화해야 함
    # 또는 init 컨테이너로 MPS 데몬 시작
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Kubernetes에서의 MPS

NVIDIA GPU Operator의 MPS sharing strategy 사용:
```yaml
# nvidia.com/mps 리소스로 요청
resources:
  limits:
    nvidia.com/gpu: 1
```

## 사용 시 주의사항

- MPS는 동일 GPU를 공유하는 모든 프로세스에 적용됨
- 한 프로세스의 GPU 에러가 다른 프로세스에 영향 줄 수 있음
- production에서는 충분한 테스트 후 적용 권장
