
# compile and get the apk

```bash
mkdir -p bin
```

```bash
docker-compose -f docker-compose.build.yml up --build
```

adb logcat | grep kivyopencvcamera
