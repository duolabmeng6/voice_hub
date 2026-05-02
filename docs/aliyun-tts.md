# 阿里云百炼语音合成接入流程

本文档覆盖 `voice_hub` 当前接入的阿里云百炼 TTS：

- Qwen TTS：系统音色，支持 `qwen3-tts-instruct-flash` 指令控制。
- CosyVoice：系统音色、声音复刻、本地文件上传后复刻。

## 环境变量

```bash
export DASHSCOPE_API_KEY="sk-..."
```

如果不传 `api_key`，`AliyunTTS`、`AliyunCosyVoiceTTS` 和 `AliyunCosyVoiceClone` 都会默认读取 `DASHSCOPE_API_KEY`。

北京和新加坡地域的 API Key 不通用。当前默认使用北京地域。

## Qwen TTS

### 模型

- `voice_hub.ALIYUN_QWEN_TTS_MODEL`：`qwen3-tts-instruct-flash`
- `voice_hub.ALIYUN_QWEN_TTS_FLASH_MODEL`：`qwen3-tts-flash`

`instructions` 只适用于 `qwen3-tts-instruct-flash`。普通 `qwen3-tts-flash` 不要传 `instructions`。

### Endpoint

- 北京：`voice_hub.ALIYUN_BASE_URL`
- 新加坡：`voice_hub.ALIYUN_INTL_BASE_URL`

### 最小系统音色合成

```python
import voice_hub

tts = voice_hub.AliyunTTS(
    voice=voice_hub.AliyunVoice.CHERRY,
    instructions="语速较快，带有明显的上扬语调，适合介绍时尚产品",
)

tts.to_file(
    "那我来给大家推荐一款T恤，这款颜色很显气质。",
    "./tmp/aliyun-qwen.mp3",
)
```

### Qwen 系统音色

最新音色以阿里云百炼官方文档/控制台为准：

- Qwen TTS API 文档：https://bailian.console.aliyun.com/cn-beijing?tab=api#/api/?type=model&url=2881635
- Qwen TTS 模型文档：https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2879134

代码里维护的是一份方便调用的系统音色快照。查看当前内置快照：

```python
import voice_hub

for voice in voice_hub.ALIYUN_SYSTEM_VOICES:
    print(voice.voice_id, voice.name, voice.note)
```

常用示例：

- `voice_hub.AliyunVoice.CHERRY`
- `voice_hub.AliyunVoice.ETHAN`
- `voice_hub.AliyunVoice.SERENA`
- `voice_hub.AliyunVoice.MIA`

## CosyVoice

### 模型

- `voice_hub.ALIYUN_COSYVOICE_MODEL`：`cosyvoice-v3-flash`，用于系统音色。
- `voice_hub.ALIYUN_COSYVOICE_CLONE_MODEL`：`cosyvoice-v3.5-flash`，用于声音复刻。
- `voice_hub.ALIYUN_COSYVOICE_ENROLLMENT_MODEL`：`voice-enrollment`，用于创建、查询、删除复刻音色。

系统音色和复刻音色的模型不要混用。例如 `longanyang` 能用于 `cosyvoice-v3-flash`，不能用于 `cosyvoice-v3.5-flash`。

### 系统音色合成

```python
import voice_hub

tts = voice_hub.AliyunCosyVoiceTTS(
    voice=voice_hub.AliyunCosyVoice.LONGANYANG,
    instruction="你正在进行产品推广，你说话的情感是happy。",
)

tts.to_file(
    "那我来给大家推荐一款T恤，这款颜色很显气质。",
    "./tmp/aliyun-cosyvoice-system.mp3",
)
```

### 本地文件复刻

推荐使用易用入口 `AliyunCosyVoiceTTS.cloned(sample=...)`：

```python
import voice_hub

tts = voice_hub.AliyunCosyVoiceTTS.cloned(
    sample="./tmp/voice-clones/vc30.wav",
    language_hints=["zh"],
    max_prompt_audio_length=20.0,
    enable_preprocess=False,
)

tts.to_file(
    "恭喜，已成功复刻并合成了属于自己的声音。",
    "./tmp/aliyun-cosyvoice-clone-from-file.mp3",
)

print(tts.voice_result.voice_id)
print(tts.voice_result.reused)
```

内部流程：

```text
本地音频文件
  └── 上传到百炼文件管理服务 /api/v1/files
      └── 查询文件详情，拿到临时 OSS URL
          └── create_voice 创建 CosyVoice 音色
              └── voice_id 用作后续合成的 voice 参数
```

### 公网 URL 复刻

如果样本音频已经有公网可访问 URL：

```python
import voice_hub

tts = voice_hub.AliyunCosyVoiceTTS.cloned(
    audio_url="https://example.com/reference.wav",
    language_hints=["zh"],
)

tts.to_file("你好，欢迎使用我的复刻音色。", "./tmp/aliyun-cosyvoice-clone.mp3")
```

### 底层音色管理

需要显式管理音色时使用 `AliyunCosyVoiceClone`：

```python
import voice_hub

clone = voice_hub.AliyunCosyVoiceClone()

result = clone.get_or_create_voice_from_file(
    "./tmp/voice-clones/vc30.wav",
    language_hints=["zh"],
)

clone.wait_until_ready(result.voice_id)
clone.tts(result.voice_id).to_file("你好", "./tmp/clone.mp3")

voices = clone.list_voices(prefix=result.prefix)
info = clone.query_voice(result.voice_id)
```

### 复用策略

- `sample=...` 默认使用 `target_model + 文件内容` 的 MD5 派生前缀。
- `audio_url=...` 默认使用 `target_model + audio_url` 的 MD5 派生前缀。
- 创建前先按前缀 `list_voices`。
- 已有 `OK` 或 `DEPLOYING` 音色时直接复用。
- 没有可复用音色时才创建，避免频繁创建占用音色配额。
- 也可以显式传入 `prefix="myvoice"`。

### CosyVoice 系统音色

最新音色以阿里云官方音色列表为准：

- CosyVoice 音色列表：https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list
- CosyVoice 语音合成文档：https://help.aliyun.com/zh/model-studio/text-to-speech#992f46b0f4ha2
- CosyVoice 声音复刻/设计文档：https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api

代码里维护的是 `cosyvoice-v3-flash` 系统音色快照。查看当前内置快照：

```python
import voice_hub

for voice in voice_hub.ALIYUN_COSYVOICE_SYSTEM_VOICES:
    print(voice.voice_id, voice.name, voice.language, voice.note)
```

常用示例：

- `voice_hub.AliyunCosyVoice.LONGANYANG`
- `voice_hub.AliyunCosyVoice.LONGANHUAN`
- `voice_hub.AliyunCosyVoice.LONGHUHU_V3`
- `voice_hub.AliyunCosyVoice.LONGANRAN_V3`

## 真实调用测试

```bash
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_aliyun_qwen3_tts_instruct_flash_system_voice -q -s
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_aliyun_cosyvoice_system_voice -q -s
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_aliyun_cosyvoice_clone_from_file_and_tts -q -s
```

常见输出：

```text
tmp/aliyun_qwen3_tts.wav
tmp/aliyun_cosyvoice_system.mp3
tmp/aliyun_cosyvoice_clone_from_file.mp3
```
