# MiMo TTS

MiMo 支持内置音色、文本设计音色和参考音频克隆音色。

## 准备

```bash
export MIMO_API_KEY="你的 MiMo API Key"
export MIMO_BASE_URL="https://api.xiaomimimo.com/v1"
```

如果你使用 token plan，再设置：

```bash
export MIMO_TOKEN_KEY="你的 token plan key"
export MIMO_TOKEN_BASE_URL="你的 token plan base url"
```

## 内置音色

```python
import os
import voice_hub

tts = voice_hub.MimoTTS(
    api_key=os.environ["MIMO_API_KEY"],
    base_url=os.environ.get("MIMO_BASE_URL", voice_hub.MIMO_BASE_URL),
    voice=voice_hub.MimoVoice.BINGTANG,
    style="自然、平稳",
)

tts.speak("夜深了，城市还没有睡。").save("./tmp/mimo.wav")
```

常用内置音色：

```python
voice_hub.MimoVoice.BINGTANG  # 冰糖
voice_hub.MimoVoice.MOLI      # 茉莉
voice_hub.MimoVoice.SUDA      # 苏打
voice_hub.MimoVoice.BAIHUA    # 白桦
voice_hub.MimoVoice.MIA       # Mia
```

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

tts.speak("夜深了，城市还没有睡。").save("./tmp/mimo-designed.wav")
```

## 参考音频克隆

```python
import os
import voice_hub

tts = voice_hub.MimoTTS.cloned(
    api_key=os.environ["MIMO_TOKEN_KEY"],
    base_url=os.environ["MIMO_TOKEN_BASE_URL"],
    sample=voice_hub.VoiceSample("./tmp/voice-clones/sample.wav"),
    style="自然、快速讲话",
)

tts.speak("这句话使用克隆音色。").save("./tmp/mimo-cloned.wav")
```

## 放进 Client

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

client.speaker("冰糖").speak("欢迎回来。").save("./tmp/bingtang.wav")
```

## 流式合成

```python
import os
import voice_hub

tts = voice_hub.MimoTTS(api_key=os.environ["MIMO_API_KEY"])

with open("./tmp/mimo-stream.pcm", "wb") as f:
    for chunk in tts.stream("你好，欢迎使用 voice_hub。"):
        f.write(chunk)
```
