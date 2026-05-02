# MiniMax 语音合成接入流程

本文档覆盖 `voice_hub` 当前接入的 MiniMax：

- 系统音色语音合成。
- 流式合成。
- 快速声音复刻试听。

## 环境变量

```bash
export MINIMAX_KEY="..."
export MINIMAX_KEY2="..."
```

- `MinimaxTTS` 默认读取 `MINIMAX_KEY`。
- `MinimaxVoiceClone` 默认读取 `MINIMAX_KEY2`。
- 如果直接传 `api_key`，会优先使用传入值。

## 模型

- `voice_hub.MINIMAX_T2A_MODEL`：`speech-2.8-hd`
- `voice_hub.MINIMAX_VOICE_CLONE_MODEL`：`speech-2.8-hd`
- `voice_hub.MINIMAX_BASE_URL`：`https://api.minimaxi.com/v1`

## 系统音色合成

```python
import voice_hub

tts = voice_hub.MinimaxTTS(
    voice=voice_hub.MinimaxVoice.MALE_QN_QINGSE,
    emotion="happy",
    format="mp3",
)

tts.to_file("今天是不是很开心呀，当然了！", "./tmp/minimax.mp3")
```

常用参数：

- `voice`：系统音色、复刻音色或文生音色 ID。
- `format`：`mp3`、`pcm`、`flac`，非流式也支持 `wav`。
- `speed`：语速，默认 `1`。
- `vol`：音量，默认 `1`。
- `pitch`：音调，默认 `0`。
- `emotion`：情绪参数。
- `language_boost`：语言增强，例如 `"English"`。

## 流式合成

```python
import voice_hub

tts = voice_hub.MinimaxTTS(format="mp3")

with open("./tmp/minimax-stream.mp3", "wb") as f:
    for chunk in tts.stream("你好，欢迎使用 voice_hub。"):
        f.write(chunk)
```

注意：当前 provider 对 `wav` 做了限制，流式调用不要使用 `format="wav"`。

## 快速声音复刻试听

```python
import voice_hub

tts = voice_hub.MinimaxTTS.cloned(
    sample="./tmp/voice-clones/vc30.wav",
    voice_id=voice_hub.MinimaxVoiceClone.new_voice_id("VoiceHubClone"),
)

tts.to_file(
    "你好，这是 MiniMax 快速复刻试听。",
    "./tmp/minimax-clone-preview.mp3",
)
```

底层流程：

```text
本地音频文件
  └── upload_file purpose=voice_clone
      └── /voice_clone 创建复刻试听
          └── 下载 demo_audio
              └── 保存为本地音频
```

## 音色

最新音色以 MiniMax 官方文档/控制台为准，尤其是多语言音色和新模型音色可能会更新。

官方入口：

- 系统音色列表：https://platform.minimaxi.com/docs/faq/system-voice-id
- 查询可用音色 ID API：https://platform.minimaxi.com/docs/api-reference/voice-management-get
- 同步语音合成 T2A：https://platform.minimaxi.com/docs/api-reference/speech-t2a-intro

代码里维护的是一份系统音色快照，用于常量补全和测试。查看当前内置快照：

```python
import voice_hub

for voice in voice_hub.MINIMAX_SYSTEM_VOICES:
    print(voice.index, voice.language, voice.voice_id, voice.name)
```

按语言筛选：

```python
import voice_hub

for voice in voice_hub.MINIMAX_SYSTEM_VOICES_BY_LANGUAGE["中文 (粤语)"]:
    print(voice.voice_id, voice.name)
```

按 ID 查说明：

```python
import voice_hub

spec = voice_hub.MINIMAX_SYSTEM_VOICE_BY_ID["male-qn-qingse"]
print(spec.note)
```

常用示例：

- `voice_hub.MinimaxVoice.MALE_QN_QINGSE`
- `voice_hub.MinimaxVoice.FEMALE_SHAONV`
- `voice_hub.MinimaxVoice.CHINESE_MANDARIN_NEWS_ANCHOR`
- `voice_hub.MinimaxVoice.CANTONESE_GENTLELADY`
- `voice_hub.MinimaxVoice.ENGLISH_GRACEFUL_LADY`

## 真实调用测试

```bash
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_minimax_obj -q -s
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_minimax_voice_clone_preview_only -q -s
```
