# Configs 디렉토리 — 서버 레벨 설정

Triton 서버 시작 시 사용되는 CLI 인자를 환경별 + 모듈별로 분리합니다.

## 구조

```
configs/
├── base.txt          # 모든 환경 공통 (로깅, strict config 등)
├── dev.txt           # 개발: poll 모드, 짧은 폴링 주기
├── staging.txt       # 스테이징: explicit 모드
├── prod.txt          # 운영: explicit + cache + rate-limit
├── tls/              # TLS/SSL 인증서 기반 보안 통신
├── tracing/          # OpenTelemetry / Triton trace 설정
├── cache/            # Response Cache (Local / Redis)
├── gpu/              # CUDA MPS, NUMA 최적화
└── repository/       # 클라우드 모델 저장소 (S3/GCS/Azure)
```

## 사용법

`scripts/build.sh`가 환경에 맞게 설정 파일들을 합성합니다:

```bash
# 합성 순서: base.txt → {env}.txt → 선택 모듈들
./scripts/build.sh --env prod --tls --tracing otel --cache local
```

## 운영 판단 기준

| 설정 | dev | staging | prod |
|------|-----|---------|------|
| `model-control-mode` | poll (자동 감지) | explicit | explicit |
| `response-cache` | off | on (local) | on (local, redis는 별도 플러그인 검증 후) |
| `rate-limit` | off | off | on |
| `tls` | off | off | on |
| `tracing` | triton native (파일) | otel (collector) | otel (collector) |
