# voice_hub

统一 TTS speaker 管理器。

```bash
pip install voice_hub
```

```python
import voice_hub as vh
import os

tts = vh.Client()
tts.add_speaker(
    "narrator",
    vh.MimoTTS(
        api_key=os.environ["MIMO_API_KEY"],
        base_url=os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"),
        voice=vh.MimoVoice.BINGTANG,
        style="自然、平稳",
        format="wav",
    ),
    default=True,
)

tts.speak("夜深了，城市还没有睡。").save("out.wav")
```

## MiMo 音色

```python
api_key = os.environ["MIMO_API_KEY"]
base_url = os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")

# 内置音色
vh.MimoTTS(
    api_key=api_key,
    base_url=base_url,
    voice=vh.MimoVoice.BINGTANG,
    style="轻快",
    format="wav",
)

# 设计音色
vh.MimoTTS.designed(
    api_key=api_key,
    base_url=base_url,
    prompt="年轻女性，温柔、松弛、有轻微气声",
    style="自然、平稳",
)

# 克隆音色
vh.MimoTTS.cloned(
    api_key=api_key,
    base_url=base_url,
    sample=vh.VoiceSample("voice.mp3"),
    style="自然、平稳",
)
```

如果使用 token-plan 地址，由调用方显式传入对应变量：

```python
tts = vh.MimoTTS(
    api_key=os.environ["MIMO_TOKEN_KEY"],
    base_url=os.environ["MIMO_TOKEN_BASE_URL"],
    voice=vh.MimoVoice.BINGTANG,
)
```

预置音色常量：

```python
vh.MimoVoice.DEFAULT   # "mimo_default"
vh.MimoVoice.BINGTANG  # "冰糖"
vh.MimoVoice.MOLI      # "茉莉"
vh.MimoVoice.SUDA      # "苏打"
vh.MimoVoice.BAIHUA    # "白桦"
vh.MimoVoice.MIA       # "Mia"
vh.MimoVoice.CHLOE     # "Chloe"
vh.MimoVoice.MILO      # "Milo"
vh.MimoVoice.DEAN      # "Dean"
```

`speak()` 的临时覆盖参数会合并到单次请求：

```python
tts.speak("这句话临时加快语速。", speed=1.2).save("fast.wav")
tts.speak("这句话临时换个声音。", voice="茉莉").save("moli.wav")
```
