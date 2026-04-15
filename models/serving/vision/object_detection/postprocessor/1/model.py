"""Object Detection Postprocessor — NMS + Scale Recovery"""

import numpy as np
import triton_python_backend_utils as pb_utils


class TritonPythonModel:
    def initialize(self, args):
        self.conf_threshold = 0.5
        self.nms_threshold = 0.45

    def execute(self, requests):
        responses = []
        for request in requests:
            detections = pb_utils.get_input_tensor_by_name(request, "DETECTIONS").as_numpy()
            scale_factor = pb_utils.get_input_tensor_by_name(request, "SCALE_FACTOR").as_numpy()

            # Confidence filtering
            scores = detections[:, 4] * detections[:, 5]
            mask = scores > self.conf_threshold
            filtered = detections[mask]

            bboxes = filtered[:, :4] / scale_factor.repeat(2) if len(filtered) > 0 else np.zeros((0, 4), dtype=np.float32)
            final_scores = scores[mask] if len(filtered) > 0 else np.zeros(0, dtype=np.float32)
            class_ids = filtered[:, 6].astype(np.int32) if len(filtered) > 0 else np.zeros(0, dtype=np.int32)

            responses.append(pb_utils.InferenceResponse(output_tensors=[
                pb_utils.Tensor("BBOXES", bboxes.astype(np.float32)),
                pb_utils.Tensor("SCORES", final_scores.astype(np.float32)),
                pb_utils.Tensor("CLASS_IDS", class_ids),
            ]))

        return responses

    def finalize(self):
        pass
