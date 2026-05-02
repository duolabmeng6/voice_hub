# 智谱 GLM TTS

智谱 GLM TTS 适合快速使用系统音色生成 `wav` 或 `pcm` 音频，不需要安装智谱 SDK。

## 准备

```bash
export ZHIPUAI_API_KEY="你的智谱 API Key"
```

## 最小示例

```python
import voice_hub

tts = voice_hub.GLMTTS(
    voice=voice_hub.GLMVoice.FEMALE,
    response_format="wav",
    watermark_enabled=False,
)

tts.speak("夜深了，城市还没有睡。").save("./tmp/glm.wav")
```

常用参数：

- `voice`：系统音色 ID，也可以传自定义音色 ID。
- `response_format`：`wav` 或 `pcm`。
- `speed`：语速，默认 `1.0`。
- `volume`：音量，默认 `1.0`。
- `watermark_enabled`：是否请求关闭水印。

## 放进 Client

```python
import voice_hub

client = voice_hub.Client()
client.add_speaker(
    "glm",
    voice_hub.GLMTTS(
        voice=voice_hub.GLMVoice.FEMALE,
        response_format="wav",
        watermark_enabled=False,
    ),
    default=True,
)

client.speaker("glm").speak("欢迎回来。").save("./tmp/glm-client.wav")
```

## 查看内置音色

```python
import voice_hub

print(voice_hub.GLM_SYSTEM_VOICE_IDS)
```

也可以按 ID 查看说明：

```python
spec = voice_hub.GLM_SYSTEM_VOICE_BY_ID["female"]
print(spec.name, spec.note)
```

## 水印说明

智谱服务端可能会在音频开头加入提示音。`watermark_enabled=False` 只对已经在智谱控制台开通去水印的账号生效；如果账号未开通，服务端仍可能返回带水印的音频。
