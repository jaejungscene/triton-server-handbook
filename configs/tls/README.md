# TLS/SSL 설정 가이드

## 인증서 생성 (개발/테스트용 self-signed)

```bash
# CA 생성
openssl genrsa -out ca.key 4096
openssl req -new -x509 -days 365 -key ca.key -out ca.crt \
  -subj "/CN=triton-ca"

# 서버 인증서 생성
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr \
  -subj "/CN=triton-server"
openssl x509 -req -days 365 -in server.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
```

## 파일 구성

```
configs/tls/
├── README.md           # 이 파일
├── grpc_tls.txt        # gRPC TLS 서버 인자
└── http_tls.txt        # HTTP TLS 서버 인자
```

## 인증서 배포

- 운영 환경: Kubernetes Secret으로 마운트
  ```yaml
  volumes:
    - name: tls-certs
      secret:
        secretName: triton-tls
  ```
- 개발 환경: `deploy/docker/certs/` 디렉토리에 배치 (gitignore 대상)

## 갱신 절차

1. 새 인증서 생성
2. Secret 업데이트: `kubectl create secret tls triton-tls --cert=server.crt --key=server.key --dry-run=client -o yaml | kubectl apply -f -`
3. Triton pod 재시작: `kubectl rollout restart deployment triton-server`
