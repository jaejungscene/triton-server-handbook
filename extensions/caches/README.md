# Custom Cache 확장 지점

Triton은 [TRITONCACHE API](https://github.com/triton-inference-server/core/blob/main/include/triton/core/tritoncache.h)를 통해 custom cache 구현을 지원합니다.

## 기본 제공 캐시

- `local` — 인메모리 캐시 (프로세스 내)
- `redis` — Redis 서버 연동

## Custom Cache 개발 절차

1. TRITONCACHE API 헤더의 인터페이스 구현
2. `libtritoncache_<name>.so` 빌드
3. `/opt/tritonserver/caches/<name>/` 에 배치
4. `--cache-config=<name>,<key>=<value>` 로 사용

## 사용 예

```bash
tritonserver \
  --cache-config=my_cache,endpoint=memcached:11211 \
  --model-repository=/models
```

## 참고

- [local_cache](https://github.com/triton-inference-server/local_cache) — 인메모리 캐시 구현
- [redis_cache](https://github.com/triton-inference-server/redis_cache) — Redis 캐시 구현
