#!/usr/bin/env python3
"""
to_torchscript.py — PyTorch 모델을 TorchScript로 변환

사용법:
    python scripts/convert/to_torchscript.py \
        --model-path ./weights/model.pt \
        --output-path ./model_repository/my_model/1/model.pt \
        --method trace \
        --input-shape 1,3,224,224
"""

import argparse
import sys


def convert_to_torchscript(model_path, output_path, method, input_shape):
    try:
        import torch
    except ImportError:
        print("ERROR: PyTorch required", file=sys.stderr)
        sys.exit(1)

    print(f"[convert] Loading from {model_path}")
    model = torch.load(model_path, map_location="cpu", weights_only=False)
    if isinstance(model, dict) and "model" in model:
        model = model["model"]
    model.eval()

    shape = [int(x) for x in input_shape.split(",")]

    if method == "trace":
        dummy = torch.randn(*shape)
        scripted = torch.jit.trace(model, dummy)
    elif method == "script":
        scripted = torch.jit.script(model)
    else:
        print(f"ERROR: Unknown method: {method}", file=sys.stderr)
        sys.exit(1)

    scripted.save(output_path)
    print(f"[convert] Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--method", choices=["trace", "script"], default="trace")
    parser.add_argument("--input-shape", default="1,3,224,224")
    args = parser.parse_args()
    convert_to_torchscript(args.model_path, args.output_path, args.method, args.input_shape)


if __name__ == "__main__":
    main()
