"""
Ensemble Pipeline — Preprocessor (Python Backend)

이미지 전처리: 리사이즈 → 정규화 → CHW 변환
"""

import numpy as np
import triton_python_backend_utils as pb_utils


class TritonPythonModel:
    def initialize(self, args):
        self.target_size = (224, 224)
        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def execute(self, requests):
        responses = []
        for request in requests:
            raw_input = pb_utils.get_input_tensor_by_name(request, "RAW_INPUT")
            img = raw_input.as_numpy()

            # Resize (간단 구현 — 실무에서는 cv2/PIL 사용)
            # img = cv2.resize(img, self.target_size)

            # Normalize
            img = img.astype(np.float32) / 255.0
            img = (img - self.mean) / self.std

            # HWC → CHW
            img = np.transpose(img, (0, 3, 1, 2)) if img.ndim == 4 else np.transpose(img, (2, 0, 1))

            output_tensor = pb_utils.Tensor("PREPROCESSED", img.astype(np.float32))
            responses.append(pb_utils.InferenceResponse(output_tensors=[output_tensor]))

        return responses

    def finalize(self):
        pass
