#!/usr/bin/env bash
# =============================================================================
# to_tensorrt.sh — ONNX 모델을 TensorRT 엔진으로 변환
# =============================================================================
# 사용법:
#   ./scripts/convert/to_tensorrt.sh \
#       --input model.onnx \
#       --output model.plan \
#       --precision fp16 \
#       --max-batch 8
#
# 사전조건: trtexec 이 설치되어 있어야 함
#   (nvcr.io/nvidia/tritonserver 이미지 내에 포함)
# =============================================================================

set -euo pipefail

INPUT=""
OUTPUT=""
PRECISION="fp16"
MAX_BATCH=8
WORKSPACE=4096  # MB

while [[ $# -gt 0 ]]; do
    case $1 in
        --input)     INPUT="$2"; shift 2 ;;
        --output)    OUTPUT="$2"; shift 2 ;;
        --precision) PRECISION="$2"; shift 2 ;;
        --max-batch) MAX_BATCH="$2"; shift 2 ;;
        --workspace) WORKSPACE="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: $0 --input <onnx> --output <plan> [--precision fp16|fp32|int8] [--max-batch 8]"
            exit 0
            ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

if [[ -z "${INPUT}" || -z "${OUTPUT}" ]]; then
    echo "ERROR: --input and --output are required"
    exit 1
fi

if ! command -v trtexec &>/dev/null; then
    echo "ERROR: trtexec not found. Run inside Triton/TensorRT container."
    exit 1
fi

echo "[convert] ONNX → TensorRT"
echo "  Input:     ${INPUT}"
echo "  Output:    ${OUTPUT}"
echo "  Precision: ${PRECISION}"
echo "  MaxBatch:  ${MAX_BATCH}"

PRECISION_FLAG=""
case "${PRECISION}" in
    fp16)  PRECISION_FLAG="--fp16" ;;
    int8)  PRECISION_FLAG="--int8" ;;
    fp32)  PRECISION_FLAG="" ;;
    *)     echo "ERROR: Unknown precision: ${PRECISION}"; exit 1 ;;
esac

trtexec \
    --onnx="${INPUT}" \
    --saveEngine="${OUTPUT}" \
    ${PRECISION_FLAG} \
    --workspace="${WORKSPACE}" \
    --minShapes=input:1x3x224x224 \
    --optShapes=input:${MAX_BATCH}x3x224x224 \
    --maxShapes=input:${MAX_BATCH}x3x224x224 \
    --verbose

echo "[convert] Done: ${OUTPUT}"
