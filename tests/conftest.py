"""
conftest.py — pytest 공통 fixture

Triton 서버 URL, 공용 클라이언트 인스턴스 등을 제공합니다.
"""

import os

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--triton-url",
        action="store",
        default=os.getenv("TRITON_HTTP_URL", "http://localhost:8000"),
        help="Triton HTTP endpoint URL",
    )
    parser.addoption(
        "--triton-grpc-url",
        action="store",
        default=os.getenv("TRITON_GRPC_URL", "localhost:8001"),
        help="Triton gRPC endpoint URL",
    )


@pytest.fixture(scope="session")
def triton_url(request):
    return request.config.getoption("--triton-url")


@pytest.fixture(scope="session")
def triton_grpc_url(request):
    return request.config.getoption("--triton-grpc-url")


@pytest.fixture(scope="session")
def project_root():
    """프로젝트 루트 디렉토리 경로"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
