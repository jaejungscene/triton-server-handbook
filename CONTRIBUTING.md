# Contributing Guide

## 모델 추가

1. `models/_templates/` 에서 적절한 템플릿을 복사합니다.
2. `models/serving/{domain}/` 아래에 배치합니다.
3. `models/serving/manifest.yaml`에 source→target 매핑을 추가합니다.
4. `config.pbtxt`를 수정합니다 (input/output shape, backend).
5. PR을 생성합니다. CI가 자동으로 config 검증을 수행합니다.

## 브랜치 전략

- `main` — 항상 배포 가능 상태
- `feature/*` — 기능 개발
- `hotfix/*` — 긴급 수정

## PR 규칙

- `models/` 하위 변경 시 ML팀 리뷰 필수 (CODEOWNERS)
- config.pbtxt 변경 시 `scripts/validate.sh` 로컬 실행 권장
- 성능에 영향을 줄 수 있는 변경은 perf test 결과 첨부

## 커밋 메시지

```
type(scope): description

feat(models): add yolox ensemble pipeline
fix(configs): correct rate limiter resource count
ci(workflows): add staging deployment step
```
