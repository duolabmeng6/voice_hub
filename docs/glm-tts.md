# 智谱 GLM TTS 接入流程

本文档覆盖 `voice_hub` 当前接入的智谱 GLM 文本转语音：

- 系统音色语音合成。
- 直接 HTTP 调用 `/paas/v4/audio/speech`。
- 水印参数和真实调用测试。

## 环境变量

```bash
export ZHIPUAI_API_KEY="..."
```

- `GLMTTS` 默认读取 `ZHIPUAI_API_KEY`。
- 如果直接传 `api_key`，会优先使用传入值。
- 不需要安装智谱 SDK。

## 模型和接口

- `voice_hub.GLM_TTS_MODEL`：`glm-tts`
- `voice_hub.GLM_BASE_URL`：`https://open.bigmodel.cn/api/paas/v4/audio/speech`

底层请求等价于：

```bash
curl -X POST "https://open.bigmodel.cn/api/paas/v4/audio/speech" \
  -H "Authorization: Bearer $ZHIPUAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "glm-tts",
        "input": "你好呀，欢迎来到智谱开放平台",
        "voice": "female",
        "speed": 1.0,
        "volume": 1.0,
        "response_format": "wav"
      }' \
  --output speech.wav
```

## 系统音色合成

```python
import voice_hub

tts = voice_hub.GLMTTS(
    voice=voice_hub.GLMVoice.FEMALE,
    response_format="wav",
    watermark_enabled=False,
)

tts.to_file("夜深了，城市还没有睡。", "./tmp/glm.wav")
```

常用参数：

- `voice`：系统音色 ID，或已创建的自定义音色 ID。
- `response_format`：`wav` 或 `pcm`。
- `speed`：语速，范围 `0.5` 到 `2`，默认 `1.0`。
- `volume`：音量，范围 `0` 到 `10`，默认 `1.0`。
- `watermark_enabled`：是否开启水印；默认由智谱服务端决定。
- `base_url`：智谱语音合成 API 地址，通常不需要改。

## 音色

最新音色以智谱官方文档/控制台为准。

官方入口：

- GLM-TTS 指南：https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-tts
- 文本转语音 API：https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%9C%AC%E8%BD%AC%E8%AF%AD%E9%9F%B3

代码里维护的是一份系统音色 ID 快照。查看当前内置快照：

```python
import voice_hub

print(voice_hub.GLM_SYSTEM_VOICE_IDS)
```

当前包含：

- `female`
- `male`
- `tongtong`
- `chuichui`
- `xiaochen`
- `jam`
- `kazi`
- `douji`
- `luodo`

也可以按 ID 查说明：

```python
import voice_hub

spec = voice_hub.GLM_SYSTEM_VOICE_BY_ID["tongtong"]
print(spec.name, spec.note)
```

## 水印说明

智谱接口可能会在音频开头加入“滴滴滴”提示音，这是服务端显式水印，不是 `voice_hub` 解码错误。

可以在请求中设置：

```python
tts = voice_hub.GLMTTS(watermark_enabled=False)
```

但 `watermark_enabled=False` 只对已经在智谱控制台完成去水印开通的账号生效；否则服务端可能仍会返回带显式水印的音频。

## 统一 speaker 管理

```python
import voice_hub

client = voice_hub.Client()
client.add_speaker(
    "glm",
    voice_hub.GLMTTS(
        voice=voice_hub.GLMVoice.FEMALE,
        watermark_enabled=False,
    ),
    default=True,
)

client.to_file("夜深了，城市还没有睡。", "./tmp/glm-client.wav")
```

## 真实调用测试

```bash
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_glm_tts_system_voice -q -s
```

当前测试输出示例：

```text
tmp/glm_tts.wav
```
