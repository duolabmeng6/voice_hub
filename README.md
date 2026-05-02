# voice_hub

统一 TTS speaker 管理器。

```bash
pip install duolabmeng6-voice-hub
```

```python
import os
import voice_hub

tts = voice_hub.Client()
tts.add_speaker(
    "narrator",
    voice_hub.MimoTTS(
        api_key=os.environ["MIMO_API_KEY"],
        base_url=os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"),
        voice=voice_hub.MimoVoice.BINGTANG,
        style="自然、平稳",
        format="wav",
    ),
    default=True,
)

tts.speak("夜深了，城市还没有睡。").save("out.wav")
```

## MiMo 音色

MiMo-V2.5-TTS 有三种用法：

- `voice_hub.MimoTTS(...)`：使用官方内置音色，配置 `voice`
- `voice_hub.MimoTTS.designed(...)`：用文字描述生成新音色，配置 `prompt`
- `voice_hub.MimoTTS.cloned(...)`：用本地 mp3/wav 参考音频克隆音色，配置 `sample`

参数速查：

- `api_key`：小米 MiMo 控制台 API Key，对应请求头 `api-key`
- `base_url`：API 地址，默认 `https://api.xiaomimimo.com/v1`
- `voice`：内置音色 ID，只对 `mimo-v2.5-tts` 生效
- `style`：自然语言风格指令，控制语速、情绪、角色、方言等
- `format`：输出格式；非流式常用 `wav`，流式会默认用 `pcm16`
- `model`：底层模型 ID，通常不需要手动传，优先用便捷构造方法
- `voice_design_prompt`：文本设计音色描述，等价于 `designed(prompt=...)`
- `voice_sample`：克隆音色参考音频，等价于 `cloned(sample=...)`
- `timeout`：HTTP 请求超时时间，单位秒
- `transport`：自定义传输层，主要用于测试或代理

```python
api_key = os.environ["MIMO_API_KEY"]
base_url = os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")

# 内置音色
voice_hub.MimoTTS(
    api_key=api_key,
    base_url=base_url,
    voice=voice_hub.MimoVoice.BINGTANG,
    style="轻快",
    format="wav",
)

# 设计音色
voice_hub.MimoTTS.designed(
    api_key=api_key,
    base_url=base_url,
    prompt="年轻女性，温柔、松弛、有轻微气声",
    style="自然、平稳",
)

# 克隆音色
voice_hub.MimoTTS.cloned(
    api_key=api_key,
    base_url=base_url,
    sample=voice_hub.VoiceSample("voice.mp3"),
    style="自然、平稳",
)
```

如果使用 token-plan 地址，由调用方显式传入对应变量：

```python
tts = voice_hub.MimoTTS(
    api_key=os.environ["MIMO_TOKEN_KEY"],
    base_url=os.environ["MIMO_TOKEN_BASE_URL"],
    voice=voice_hub.MimoVoice.BINGTANG,
)
```

预置音色常量：

```python
voice_hub.MimoVoice.DEFAULT   # "mimo_default"
voice_hub.MimoVoice.BINGTANG  # "冰糖"
voice_hub.MimoVoice.MOLI      # "茉莉"
voice_hub.MimoVoice.SUDA      # "苏打"
voice_hub.MimoVoice.BAIHUA    # "白桦"
voice_hub.MimoVoice.MIA       # "Mia"
voice_hub.MimoVoice.CHLOE     # "Chloe"
voice_hub.MimoVoice.MILO      # "Milo"
voice_hub.MimoVoice.DEAN      # "Dean"
```

`speak()` 的临时覆盖参数会合并到单次请求：

```python
tts.speak("这句话临时加快语速。", speed=1.2).save("fast.wav")
tts.speak("这句话临时换个声音。", voice="茉莉").save("moli.wav")
```
