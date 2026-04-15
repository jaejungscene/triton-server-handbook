#!/usr/bin/env bash
# =============================================================================
# reload.sh — 무중단 모델 교체 (unload → 배치 → load)
# =============================================================================
# 사용법:
#   ./scripts/model_control/reload.sh yolox
#   ./scripts/model_control/reload.sh yolox v2         # 특정 버전
#   ./scripts/model_control/reload.sh yolox v2 http://triton:8000
#
# 이 스크립트 하나가 "Triton은 재시작 없이 모델을 교체할 수 있다"를
# 운영 절차로 만든다.
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODEL_NAME="${1:?Usage: $0 <model_name> [version] [base_url]}"
VERSION="${2:-}"
BASE_URL="${3:-http://localhost:8000}"

echo "=========================================="
echo "[reload] Model: ${MODEL_NAME}"
echo "[reload] Version: ${VERSION:-latest}"
echo "=========================================="

# Step 1: Unload
echo ""
"${SCRIPT_DIR}/unload.sh" "${MODEL_NAME}" "${BASE_URL}" || true
sleep 1

# Step 2: 새 버전 배치 (선택적)
if [[ -n "${VERSION}" ]]; then
    echo ""
    echo "[reload] Deploying version: ${VERSION}"
    # 실제 구현에서는 model_repository 내의 버전 디렉토리를 업데이트
    # 예: S3에서 다운로드, 빌드 결과물 복사 등
    echo "[reload] (Version deployment is handled by CI/CD or manual copy)"
fi

# Step 3: Load
echo ""
"${SCRIPT_DIR}/load.sh" "${MODEL_NAME}" "${BASE_URL}"

# Step 4: Health check
echo ""
echo "[reload] Verifying model status..."
sleep 2
model_status=$(curl -sf "${BASE_URL}/v2/models/${MODEL_NAME}" 2>/dev/null || echo '{"state":"UNKNOWN"}')
echo "[reload] Status: ${model_status}"

echo ""
echo "=========================================="
echo "[reload] Complete"
echo "=========================================="
