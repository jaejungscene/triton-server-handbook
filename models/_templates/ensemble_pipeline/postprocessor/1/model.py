"""
Ensemble Pipeline — Postprocessor (Python Backend)

추론 결과 후처리: softmax, argmax, label 매핑 등
"""

import numpy as np
import triton_python_backend_utils as pb_utils


class TritonPythonModel:
    def initialize(self, args):
        # 필요 시 label 매핑 파일 로드
        # self.labels = json.load(open("labels.json"))
        pass

    def execute(self, requests):
        responses = []
        for request in requests:
            raw_output = pb_utils.get_input_tensor_by_name(request, "RAW_OUTPUT")
            result = raw_output.as_numpy()

            # 후처리 로직 구현
            # 예: softmax → argmax
            # exp_result = np.exp(result - np.max(result, axis=-1, keepdims=True))
            # probabilities = exp_result / np.sum(exp_result, axis=-1, keepdims=True)

            output_tensor = pb_utils.Tensor("FINAL_OUTPUT", result.astype(np.float32))
            responses.append(pb_utils.InferenceResponse(output_tensors=[output_tensor]))

        return responses

    def finalize(self):
        pass
