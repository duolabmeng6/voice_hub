# 阿里云百炼 TTS

阿里云百炼在 `voice_hub` 里有两个常用入口：

- `AliyunTTS`：Qwen TTS，适合系统音色和指令控制。
- `AliyunCosyVoiceTTS`：CosyVoice，适合系统音色和声音复刻。

## 准备

先安装 `voice_hub`：

```bash
pip install duolabmeng6-voice-hub
```

```bash
export DASHSCOPE_API_KEY="你的 DashScope API Key"
```

Qwen TTS 走 HTTP API，不需要额外 SDK。

如果使用 CosyVoice，需要额外安装 DashScope SDK：

```bash
pip install duolabmeng6-voice-hub dashscope
```

本地开发或测试时，请把 `dashscope` 安装到当前项目使用的同一个 Python 环境：

```bash
python -m pip install -e . dashscope
```

## Qwen TTS

```python
import voice_hub

tts = voice_hub.AliyunTTS(
    voice=voice_hub.AliyunVoice.CHERRY,
    instructions="语速较快，带有明显的上扬语调，适合介绍时尚产品",
)

tts.speak("那我来给大家推荐一款T恤，这款颜色很显气质。").save("./tmp/aliyun-qwen.wav")
```

常用参数：

- `voice`：系统音色。
- `instructions`：语气、语速、情绪等自然语言控制。
- `language_type`：文本语言类型，默认 `"Chinese"`。
- `base_url`：默认北京地域；新加坡地域可用 `voice_hub.ALIYUN_INTL_BASE_URL`。

常用音色：

```python
voice_hub.AliyunVoice.CHERRY
voice_hub.AliyunVoice.ETHAN
voice_hub.AliyunVoice.SERENA
voice_hub.AliyunVoice.MIA
```

## CosyVoice 系统音色

```python
import voice_hub

tts = voice_hub.AliyunCosyVoiceTTS(
    voice=voice_hub.AliyunCosyVoice.LONGANYANG,
    instruction="你正在进行产品推广，你说话的情感是happy。",
)

tts.speak("那我来给大家推荐一款T恤，这款颜色很显气质。").save("./tmp/cosyvoice.mp3")
```

常用音色：

```python
voice_hub.AliyunCosyVoice.LONGANYANG
voice_hub.AliyunCosyVoice.LONGANHUAN
voice_hub.AliyunCosyVoice.LONGHUHU_V3
voice_hub.AliyunCosyVoice.LONGANRAN_V3
```

## CosyVoice 本地文件复刻

```python
import voice_hub

tts = voice_hub.AliyunCosyVoiceTTS.cloned(
    sample="./tmp/voice-clones/sample.wav",
    language_hints=["zh"],
)

tts.speak("这句话使用复刻音色。").save("./tmp/cosyvoice-clone.mp3")
```

复刻成功后可以查看音色信息：

```python
print(tts.voice_result.voice_id)
print(tts.voice_result.reused)
```

## CosyVoice 公网 URL 复刻

```python
import voice_hub

tts = voice_hub.AliyunCosyVoiceTTS.cloned(
    audio_url="https://example.com/reference.wav",
    language_hints=["zh"],
)

tts.speak("How is the weather today?").save("./tmp/cosyvoice-url-clone.mp3")
```

## 放进 Client

```python
import voice_hub

client = voice_hub.Client()
client.add_speaker(
    "阿里云旁白",
    voice_hub.AliyunTTS(voice=voice_hub.AliyunVoice.CHERRY),
    default=True,
)

client.speaker("阿里云旁白").speak("欢迎回来。").save("./tmp/aliyun-client.wav")
```

## 注意事项

- 北京和新加坡地域的 API Key 不通用。
- Qwen TTS 的 `instructions` 主要用于 `qwen3-tts-instruct-flash`。
- CosyVoice 系统音色和复刻音色使用的模型不同，不要混用。
- 复刻时 `voice_hub` 会优先复用已有音色，避免重复创建。
