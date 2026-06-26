# =============================================================================
# Dockerfile — Triton Inference Server 운영 이미지
# =============================================================================
# 빌드:
#   docker build -f deploy/docker/Dockerfile -t triton-server .
#
# 이 이미지는 model_repository를 마운트하여 사용
# 모델 바이너리는 이미지에 포함하지 않음 (CI가 외부에서 배치)
# =============================================================================

ARG TRITON_VERSION=24.08
FROM nvcr.io/nvidia/tritonserver:${TRITON_VERSION}-py3

# Python backend 의존성 설치
COPY requirements-model.txt /tmp/requirements-model.txt
RUN pip install --no-cache-dir -r /tmp/requirements-model.txt

# 스크립트 복사 (health check 등)
COPY scripts/health_check.sh /opt/scripts/health_check.sh
RUN chmod +x /opt/scripts/health_check.sh

# 기본 model_repository 마운트 포인트
VOLUME /models

# Prometheus metrics
EXPOSE 8000 8001 8002

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/v2/health/ready || exit 1

ENTRYPOINT ["tritonserver"]
CMD ["--model-repository=/models"]
