# Custom Backend 확장 지점

Triton은 C++ 기반 custom backend를 지원합니다.

## 개발 절차

1. [Triton Backend API](https://github.com/triton-inference-server/backend) 참고하여 구현
2. `TRITONBACKEND_ModelInstanceExecute` 함수 구현
3. `libtriton_<backend_name>.so` 빌드
4. `/opt/tritonserver/backends/<backend_name>/` 에 배치

## 빌드

```bash
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/tritonserver ..
make install
```

## 배포

`deploy/docker/Dockerfile`에서 빌드한 .so 파일을 복사:
```dockerfile
COPY extensions/backends/my_backend/build/libtriton_my_backend.so \
     /opt/tritonserver/backends/my_backend/
```

## 참고

- [repeat_backend](https://github.com/triton-inference-server/repeat_backend) — decoupled backend 예시
- [identity_backend](https://github.com/triton-inference-server/identity_backend) — 최소 backend 예시
