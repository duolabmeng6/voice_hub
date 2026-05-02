# MiniMax TTS

MiniMax 适合直接使用系统音色，也可以做快速声音复刻试听。

## 准备

```bash
export MINIMAX_KEY="你的 MiniMax API Key"
```

如果要使用快速复刻试听，也可以设置：

```bash
export MINIMAX_KEY2="你的 MiniMax Voice Clone Key"
```

## 系统音色

```python
import voice_hub

tts = voice_hub.MinimaxTTS(
    voice=voice_hub.MinimaxVoice.MALE_QN_QINGSE,
    emotion="happy",
    format="mp3",
)

tts.speak("今天是不是很开心呀，当然了！").save("./tmp/minimax.mp3")
```

常用参数：

- `voice`：音色 ID，可以用内置常量，也可以传自己的音色 ID。
- `format`：输出格式，常用 `mp3`、`wav`、`flac`。
- `speed`：语速，默认 `1`。
- `vol`：音量，默认 `1`。
- `pitch`：音调，默认 `0`。
- `emotion`：情绪，例如 `"happy"`。

## 放进 Client

```python
import voice_hub

client = voice_hub.Client()
client.add_speaker(
    "旁白",
    voice_hub.MinimaxTTS(
        voice=voice_hub.MinimaxVoice.MALE_QN_QINGSE,
        format="mp3",
    ),
    default=True,
)

client.speaker("旁白").speak("夜深了，城市还没有睡。").save("./tmp/narrator.mp3")
```

## 流式合成

```python
import voice_hub

tts = voice_hub.MinimaxTTS(format="mp3")

with open("./tmp/minimax-stream.mp3", "wb") as f:
    for chunk in tts.stream("你好，欢迎使用 voice_hub。"):
        f.write(chunk)
```

## 快速复刻试听

```python
import voice_hub

tts = voice_hub.MinimaxTTS.cloned(
    sample="./tmp/voice-clones/sample.wav",
    voice_id=voice_hub.MinimaxVoiceClone.new_voice_id("VoiceHubClone"),
)

tts.speak("你好，这是 MiniMax 快速复刻试听。").save("./tmp/minimax-clone.mp3")
```

## 查看内置音色

```python
import voice_hub

for voice in voice_hub.MINIMAX_SYSTEM_VOICES:
    print(voice.voice_id, voice.name, voice.language)
```
