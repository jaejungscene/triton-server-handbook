#!/usr/bin/env bash
# =============================================================================
# health_check.sh — Triton 서버 및 모델 상태 확인
# =============================================================================
# 사용법:
#   ./scripts/health_check.sh                      # localhost:8000
#   ./scripts/health_check.sh http://triton:8000   # 커스텀 URL
# =============================================================================

set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"

echo "[health] Checking Triton server at ${BASE_URL}"
echo "=========================================="

# Server liveness
echo -n "Server Live:  "
if curl -sf "${BASE_URL}/v2/health/live" > /dev/null 2>&1; then
    echo "OK"
else
    echo "FAIL"
    echo "[health] Server is not running"
    exit 1
fi

# Server readiness
echo -n "Server Ready: "
if curl -sf "${BASE_URL}/v2/health/ready" > /dev/null 2>&1; then
    echo "OK"
else
    echo "FAIL (server is live but not ready)"
    exit 1
fi

echo "=========================================="

# Model status
echo "[health] Loaded Models:"
models_response=$(curl -sf "${BASE_URL}/v2/models" 2>/dev/null || echo '{"models":[]}')

if command -v python3 &>/dev/null; then
    echo "${models_response}" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    models = data.get('models', [])
    if not models:
        print('  (no models loaded)')
    for m in models:
        name = m.get('name', 'unknown')
        version = m.get('version', '-')
        state = m.get('state', 'unknown')
        print(f'  {name} (v{version}): {state}')
except Exception as e:
    print(f'  Error parsing response: {e}')
"
else
    echo "  ${models_response}"
fi

echo "=========================================="
echo "[health] Check complete"
