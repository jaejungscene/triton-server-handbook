# Kubernetes 배포 가이드

## 구조

```
k8s/
├── base/                # 공통 리소스 (Kustomize base)
│   ├── deployment.yaml  # Triton Deployment (GPU tolerations, resource limits)
│   ├── service.yaml     # ClusterIP (gRPC 8001), NodePort (HTTP 8000)
│   ├── configmap.yaml   # Triton CLI args 주입
│   ├── pvc.yaml         # model_repository PVC
│   └── kustomization.yaml
└── overlays/
    ├── dev/             # replicas=1, resource 최소
    ├── staging/         # replicas=2
    ├── prod/            # replicas=3+, resource 최대, HPA
    ├── multi-gpu/       # 단일 노드 multi-GPU
    └── multi-node/      # 멀티 노드 + HPA + PDB
```

## 배포 명령

```bash
# Dev
kubectl apply -k deploy/k8s/overlays/dev

# Production
kubectl apply -k deploy/k8s/overlays/prod

# 상태 확인
kubectl get pods -l app=triton-server
kubectl logs -f deployment/triton-server
```

## 트레이드오프

| 결정 | 선택 | 이유 |
|------|------|------|
| Service 타입 | ClusterIP (gRPC) + NodePort (HTTP) | gRPC는 클러스터 내 통신, HTTP는 외부 디버깅 |
| PVC | ReadWriteMany | 여러 pod이 같은 모델 공유 |
| GPU 스케줄링 | tolerations + nodeSelector | GPU 노드에만 배치 |
| 스케일링 | HPA (GPU utilization) | GPU 사용률 기반 자동 스케일링 |
