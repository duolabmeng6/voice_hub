# voice_hub

统一 TTS speaker 管理器。

```bash
pip install duolabmeng6-voice-hub
```

## 快速开始

```python
import os
import voice_hub

tts = voice_hub.Client()

tts.add_speaker(
    "冰糖",
    voice_hub.MimoTTS(
        api_key=os.environ["MIMO_API_KEY"],
        base_url=os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"),
        voice=voice_hub.MimoVoice.BINGTANG,
        style="自然、平稳",
    ),
    default=True,
)

tts.add_speaker(
    "龙儿克隆",
    voice_hub.MimoTTS.cloned(
        api_key=os.environ["MIMO_TOKEN_KEY"],
        base_url=os.environ["MIMO_TOKEN_BASE_URL"],
        sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
        style="自然、快速讲话",
    ),
)

tts.add_speaker(
    "龙儿女生",
    voice_hub.MimoTTS.designed(
        api_key=os.environ["MIMO_TOKEN_KEY"],
        base_url=os.environ["MIMO_TOKEN_BASE_URL"],
        prompt="年轻女性，温柔、松弛、有轻微气声",
        style="自然、平稳",
    ),
)

tts.speaker("冰糖").speak("夜深了，城市还没有睡。").save("./tmp/冰糖.wav")
tts.speaker("龙儿女生").speak("夜深了，城市还没有睡。").save("./tmp/龙儿女生.wav")
tts.speaker("龙儿克隆").speak("夜深了，城市还没有睡。").save("./tmp/龙儿克隆.wav")
```

## MiniMax 音色

同步 HTTP 语音合成：

```python
import os
import voice_hub

tts = voice_hub.MinimaxTTS(
    api_key=os.environ["MINIMAX_KEY"],
    voice=voice_hub.MinimaxVoice.MALE_QN_QINGSE,
    model=voice_hub.MINIMAX_T2A_MODEL,
    emotion="happy",
    format="mp3",
)

tts.speak("今天是不是很开心呀(laughs)，当然了！").save("./tmp/minimax.mp3")
```

查看官方系统音色备注：

```python
voice_hub.MINIMAX_SYSTEM_VOICE_BY_ID["male-qn-qingse"].note
# "中文 (普通话) / 青涩青年音色"

voice_hub.MINIMAX_SYSTEM_VOICES_BY_LANGUAGE["中文 (粤语)"]
# 返回全部粤语系统音色说明
```

也可以交给统一 speaker 管理：

```python
client = voice_hub.Client()
client.add_speaker("minimax", voice_hub.MinimaxTTS(), default=True)
client.to_file("夜深了，城市还没有睡。", "./tmp/minimax.mp3")
```

## MiMo 音色

内置音色：

```python
voice_hub.MimoTTS(
    api_key=os.environ["MIMO_API_KEY"],
    base_url=os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"),
    voice=voice_hub.MimoVoice.BINGTANG,
    style="轻快",
)
```

文字设计音色：

```python
voice_hub.MimoTTS.designed(
    api_key=os.environ["MIMO_TOKEN_KEY"],
    base_url=os.environ["MIMO_TOKEN_BASE_URL"],
    prompt="年轻女性，温柔、松弛、有轻微气声",
    style="自然、平稳",
)
```

参考音频克隆音色：

```python
voice_hub.MimoTTS.cloned(
    api_key=os.environ["MIMO_TOKEN_KEY"],
    base_url=os.environ["MIMO_TOKEN_BASE_URL"],
    sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
    style="自然、快速讲话",
)
```

## 常用配置

- `api_key`：小米 MiMo API Key
- `base_url`：默认用 `https://api.xiaomimimo.com/v1`；token-plan 地址用 `MIMO_TOKEN_BASE_URL`
- `voice`：内置音色，只用于 `voice_hub.MimoTTS(...)`
- `prompt`：文字设计音色，只用于 `voice_hub.MimoTTS.designed(...)`
- `sample`：本地 mp3/wav 参考音频，只用于 `voice_hub.MimoTTS.cloned(...)`
- `style`：语气、语速、情绪、方言等自然语言控制
- `MINIMAX_KEY`：MiniMax API Key，`MinimaxTTS()` 未显式传入 `api_key` 时默认读取
- `MINIMAX_SYSTEM_VOICES`：MiniMax 官方系统音色列表，包含 Voice ID、语言、名称和备注

## 预置音色

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

## 单次覆盖

```python
tts.speaker("冰糖").speak("这句话临时加快语速。", speed=1.2).save("./tmp/冰糖-快速.wav")
tts.speaker("冰糖").speak("这句话临时换个声音。", voice="茉莉").save("./tmp/茉莉.wav")
tts.speaker("minimax").speak("这句话临时加快语速。", speed=1.2).save("./tmp/minimax-fast.mp3")
```
