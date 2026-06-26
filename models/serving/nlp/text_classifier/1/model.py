"""Small deterministic text classifier for smoke tests and examples."""

import numpy as np
import triton_python_backend_utils as pb_utils


class TritonPythonModel:
    def initialize(self, args):
        self.positive_keywords = {"good", "great", "love", "fast", "stable", "좋다", "빠르다"}
        self.negative_keywords = {"bad", "slow", "fail", "error", "unstable", "나쁘다", "느리다"}

    def execute(self, requests):
        responses = []
        for request in requests:
            input_tensor = pb_utils.get_input_tensor_by_name(request, "INPUT_TEXT")
            texts = input_tensor.as_numpy().reshape(-1)

            labels = []
            confidences = []
            for raw in texts:
                text = raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
                lowered = text.lower()

                positive = any(keyword in lowered for keyword in self.positive_keywords)
                negative = any(keyword in lowered for keyword in self.negative_keywords)

                if positive and not negative:
                    labels.append("positive")
                    confidences.append(0.91)
                elif negative and not positive:
                    labels.append("negative")
                    confidences.append(0.89)
                else:
                    labels.append("neutral")
                    confidences.append(0.62)

            label_tensor = pb_utils.Tensor(
                "LABEL",
                np.array(labels, dtype=object).reshape(-1, 1),
            )
            confidence_tensor = pb_utils.Tensor(
                "CONFIDENCE",
                np.array(confidences, dtype=np.float32).reshape(-1, 1),
            )
            responses.append(
                pb_utils.InferenceResponse(output_tensors=[label_tensor, confidence_tensor])
            )

        return responses

    def finalize(self):
        pass
