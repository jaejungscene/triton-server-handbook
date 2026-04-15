#!/usr/bin/env python3
"""
to_fil.py — sklearn/XGBoost/LightGBM 모델을 FIL 백엔드 형식으로 변환

사용법:
    python scripts/convert/to_fil.py \
        --model-path ./weights/xgb_model.pkl \
        --output-path ./model_repository/anomaly_detector/1/xgboost.json \
        --format xgboost_json
"""

import argparse
import sys


def convert_to_fil(model_path, output_path, fmt):
    print(f"[convert] Loading from {model_path}")

    if fmt == "xgboost_json":
        try:
            import xgboost as xgb
        except ImportError:
            print("ERROR: xgboost required", file=sys.stderr)
            sys.exit(1)
        model = xgb.Booster()
        model.load_model(model_path)
        model.save_model(output_path)

    elif fmt == "lightgbm":
        try:
            import lightgbm as lgb
        except ImportError:
            print("ERROR: lightgbm required", file=sys.stderr)
            sys.exit(1)
        model = lgb.Booster(model_file=model_path)
        model.save_model(output_path)

    elif fmt == "treelite":
        try:
            import pickle
            import treelite
        except ImportError:
            print("ERROR: treelite required", file=sys.stderr)
            sys.exit(1)
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        tl_model = treelite.sklearn.import_model(model)
        tl_model.serialize(output_path)

    else:
        print(f"ERROR: Unknown format: {fmt}", file=sys.stderr)
        sys.exit(1)

    print(f"[convert] Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--format", choices=["xgboost_json", "lightgbm", "treelite"], default="xgboost_json")
    args = parser.parse_args()
    convert_to_fil(args.model_path, args.output_path, args.format)


if __name__ == "__main__":
    main()
