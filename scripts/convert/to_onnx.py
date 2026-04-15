#!/usr/bin/env python3
"""
to_onnx.py — PyTorch 모델을 ONNX 형식으로 변환

사용법:
    python scripts/convert/to_onnx.py \
        --model-path ./weights/model.pt \
        --output-path ./model_repository/my_model/1/model.onnx \
        --input-shape 1,3,224,224 \
        --opset 17 \
        --dynamic-axes batch_size
"""

import argparse
import sys


def convert_to_onnx(model_path, output_path, input_shape, opset, dynamic_axes):
    try:
        import torch
    except ImportError:
        print("ERROR: PyTorch is required. Install with: pip install torch", file=sys.stderr)
        sys.exit(1)

    print(f"[convert] Loading model from {model_path}")
    model = torch.load(model_path, map_location="cpu", weights_only=False)

    if isinstance(model, dict) and "model" in model:
        model = model["model"]

    model.eval()

    # Parse input shape
    shape = [int(x) for x in input_shape.split(",")]
    dummy_input = torch.randn(*shape)

    # Configure dynamic axes
    dynamic_axes_dict = None
    if dynamic_axes:
        dynamic_axes_dict = {
            "input": {0: dynamic_axes},
            "output": {0: dynamic_axes},
        }

    print(f"[convert] Exporting to ONNX (opset={opset}, shape={shape})")
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        opset_version=opset,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes=dynamic_axes_dict,
    )

    print(f"[convert] Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert PyTorch model to ONNX")
    parser.add_argument("--model-path", required=True, help="Path to PyTorch model (.pt/.pth)")
    parser.add_argument("--output-path", required=True, help="Output ONNX file path")
    parser.add_argument("--input-shape", default="1,3,224,224", help="Input shape (comma-separated)")
    parser.add_argument("--opset", type=int, default=17, help="ONNX opset version")
    parser.add_argument("--dynamic-axes", default="batch_size", help="Dynamic axis name (or empty)")
    args = parser.parse_args()

    convert_to_onnx(args.model_path, args.output_path, args.input_shape, args.opset, args.dynamic_axes)


if __name__ == "__main__":
    main()
