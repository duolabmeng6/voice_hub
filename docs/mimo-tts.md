# MiMo 语音合成接入流程

本文档覆盖 `voice_hub` 当前接入的小米 MiMo：

- 内置音色语音合成。
- 文本设计音色。
- 参考音频克隆音色。
- 流式合成。

## 环境变量

MiMo provider 当前要求显式传入 `api_key` 和需要的 `base_url`：

```bash
export MIMO_API_KEY="..."
export MIMO_BASE_URL="https://api.xiaomimimo.com/v1"
export MIMO_TOKEN_KEY="..."
export MIMO_TOKEN_BASE_URL="..."
```

常见用法：

- 内置音色：使用 `MIMO_API_KEY` 和默认 `MIMO_BASE_URL`。
- 文本设计/音频克隆：通常使用 token plan 的 `MIMO_TOKEN_KEY` 和 `MIMO_TOKEN_BASE_URL`。

## 模型

- `voice_hub.MIMO_TTS_MODEL`：`mimo-v2.5-tts`
- `voice_hub.MIMO_VOICE_DESIGN_MODEL`：`mimo-v2.5-tts-voicedesign`
- `voice_hub.MIMO_VOICE_CLONE_MODEL`：`mimo-v2.5-tts-voiceclone`
- `voice_hub.MIMO_BASE_URL`：`https://api.xiaomimimo.com/v1`

## 内置音色合成

```python
import os
import voice_hub

tts = voice_hub.MimoTTS(
    api_key=os.environ["MIMO_API_KEY"],
    base_url=os.environ.get("MIMO_BASE_URL", voice_hub.MIMO_BASE_URL),
    voice=voice_hub.MimoVoice.BINGTANG,
    style="自然、平稳",
)

tts.to_file("夜深了，城市还没有睡。", "./tmp/mimo.wav")
```

常用参数：

- `voice`：内置音色 ID。
- `style`：自然语言风格指令，例如语气、语速、情绪、方言。
- `format`：输出格式，默认 `wav`；流式调用默认覆盖为 `pcm16`。
- `base_url`：不同套餐或 token plan 需要显式配置。

## 文本设计音色

```python
import os
import voice_hub

tts = voice_hub.MimoTTS.designed(
    api_key=os.environ["MIMO_TOKEN_KEY"],
    base_url=os.environ["MIMO_TOKEN_BASE_URL"],
    prompt="年轻女性，温柔、松弛、有轻微气声",
    style="自然、平稳",
)

tts.to_file("夜深了，城市还没有睡。", "./tmp/mimo-designed.wav")
```

## 参考音频克隆音色

```python
import os
import voice_hub

tts = voice_hub.MimoTTS.cloned(
    api_key=os.environ["MIMO_TOKEN_KEY"],
    base_url=os.environ["MIMO_TOKEN_BASE_URL"],
    sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
    style="自然、快速讲话",
)

tts.to_file("夜深了，城市还没有睡。", "./tmp/mimo-cloned.wav")
```

内部请求会把本地音频转为 `data:audio/...;base64,...`，放进请求体的 `audio.voice`。

## 流式合成

```python
import os
import voice_hub

tts = voice_hub.MimoTTS(api_key=os.environ["MIMO_API_KEY"])

with open("./tmp/mimo-stream.pcm", "wb") as f:
    for chunk in tts.stream("你好，欢迎使用 voice_hub。"):
        f.write(chunk)
```

## 音色

最新内置音色以 MiMo 官方文档/控制台为准。

官方入口：

- MiMo 官网：https://mimo.mi.com/
- API Base URL：https://api.xiaomimimo.com/v1

当前没有找到公开稳定的 MiMo 内置音色列表文档页；如果官方控制台后续提供独立音色列表，以控制台页面为准。

代码里维护的是一份内置音色快照。查看当前内置快照：

```python
import voice_hub

for voice in voice_hub.MIMO_BUILTIN_VOICES:
    print(voice.voice_id, voice.name, voice.language, voice.gender)
```

常用示例：

- `voice_hub.MimoVoice.BINGTANG`
- `voice_hub.MimoVoice.MOLI`
- `voice_hub.MimoVoice.SUDA`
- `voice_hub.MimoVoice.BAIHUA`
- `voice_hub.MimoVoice.MIA`

## 统一 speaker 管理

```python
import os
import voice_hub

client = voice_hub.Client()
client.add_speaker(
    "冰糖",
    voice_hub.MimoTTS(
        api_key=os.environ["MIMO_API_KEY"],
        voice=voice_hub.MimoVoice.BINGTANG,
        style="自然、平稳",
    ),
    default=True,
)

client.to_file("夜深了，城市还没有睡。", "./tmp/mimo-client.wav")
```

## 真实调用测试

```bash
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_mimo_builtin_voice_constants_match_docs -q -s
```
