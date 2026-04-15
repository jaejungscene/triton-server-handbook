"""Object Detection Preprocessor — 이미지 전처리 (letterbox + normalize)"""

import numpy as np
import triton_python_backend_utils as pb_utils


class TritonPythonModel:
    def initialize(self, args):
        self.input_size = (640, 640)

    def execute(self, requests):
        responses = []
        for request in requests:
            raw_image = pb_utils.get_input_tensor_by_name(request, "RAW_IMAGE").as_numpy()
            img = raw_image.astype(np.float32) / 255.0

            # Letterbox resize (placeholder — 실무에서는 cv2 사용)
            h, w = img.shape[1:3] if img.ndim == 4 else img.shape[:2]
            scale = min(self.input_size[0] / h, self.input_size[1] / w)
            scale_factor = np.array([scale, scale], dtype=np.float32)

            # HWC → CHW
            if img.ndim == 4:
                img = np.transpose(img, (0, 3, 1, 2))
            else:
                img = np.transpose(img, (2, 0, 1))

            preprocessed = pb_utils.Tensor("PREPROCESSED_IMAGE", img.astype(np.float32))
            scale_out = pb_utils.Tensor("SCALE_FACTOR", scale_factor)
            responses.append(pb_utils.InferenceResponse(output_tensors=[preprocessed, scale_out]))

        return responses

    def finalize(self):
        pass
