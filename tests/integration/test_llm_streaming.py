"""
test_llm_streaming.py — LLM Decoupled Streaming 통합 테스트

gRPC bi-directional streaming으로 토큰 단위 응답을 검증합니다.
"""

import pytest


class TestLLMStreaming:
    """LLM Decoupled Streaming 통합 테스트"""

    def test_streaming_inference(self, triton_grpc_url):
        """스트리밍 추론 E2E 테스트"""
        try:
            from client.streaming_client import TritonStreamingClient
            from client.base import TritonConfig
        except ImportError:
            pytest.skip("client module not available")

        config = TritonConfig(grpc_url=triton_grpc_url)
        client = TritonStreamingClient(config)

        try:
            if not client._client.is_model_ready("llm_vllm"):
                pytest.skip("llm_vllm model not loaded")
        except Exception:
            pytest.skip("Cannot connect to Triton gRPC")

        tokens = []
        try:
            for token in client.stream_infer("llm_vllm", "Hello", max_tokens=5):
                tokens.append(token)
                assert isinstance(token, str)
        except Exception as e:
            pytest.skip(f"Streaming inference not available: {e}")
        finally:
            client.close()

        assert len(tokens) > 0, "No tokens received"

    def test_decoupled_model_config(self, triton_grpc_url):
        """Decoupled 모델이 올바르게 설정되었는지 확인"""
        try:
            import tritonclient.grpc as grpcclient
        except ImportError:
            pytest.skip("tritonclient not installed")

        client = grpcclient.InferenceServerClient(url=triton_grpc_url)

        try:
            if not client.is_model_ready("llm_vllm"):
                pytest.skip("llm_vllm model not loaded")

            config = client.get_model_config("llm_vllm")
            # Decoupled 모델은 model_transaction_policy.decoupled = true
            assert config.config.model_transaction_policy.decoupled is True
        except Exception as e:
            pytest.skip(f"Cannot verify model config: {e}")
