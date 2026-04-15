# Custom Operations 확장 지점

TensorRT 모델에서 사용하는 custom plugin, ONNX custom op 등을 관리합니다.

## TensorRT Custom Plugin

1. `IPluginV2DynamicExt` 인터페이스 구현
2. `.so` 빌드 후 모델과 함께 배포
3. `config.pbtxt`에서 `default_model_filename`으로 plugin 포함된 엔진 지정

## ONNX Custom Op

1. ONNX Runtime의 Custom Op API로 구현
2. 모델 config에서 `optimization.custom_ops` 설정

## 배포 경로

```
/opt/tritonserver/lib/         # TensorRT plugins
/opt/tritonserver/backends/    # ONNX custom ops
```

## Docker에서의 배치

```dockerfile
COPY extensions/custom_ops/build/*.so /opt/tritonserver/lib/
ENV LD_PRELOAD=/opt/tritonserver/lib/libmy_plugin.so
```
