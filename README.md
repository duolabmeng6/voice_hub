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

## 完整接入教程

- [阿里云百炼语音合成接入流程](docs/aliyun-tts.md)
- [MiniMax 语音合成接入流程](docs/minimax-tts.md)
- [MiMo 语音合成接入流程](docs/mimo-tts.md)

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

## 阿里云百炼 Qwen TTS

系统音色合成，默认读取 `DASHSCOPE_API_KEY`：

```python
import voice_hub

tts = voice_hub.AliyunTTS(
    voice=voice_hub.AliyunVoice.CHERRY,
    instructions="语速较快，带有明显的上扬语调，适合介绍时尚产品",
)

tts.speak("那我来给大家推荐一款T恤，这款呢真的是超级好看。").save("./tmp/aliyun.wav")
```

默认模型是 `qwen3-tts-instruct-flash`。如需使用普通 Flash 模型：

```python
voice_hub.AliyunTTS(model=voice_hub.ALIYUN_QWEN_TTS_FLASH_MODEL)
```

新加坡地域可把 `base_url` 改为 `voice_hub.ALIYUN_INTL_BASE_URL`，注意北京和新加坡 API Key 不通用。

代码目录：

```text
voice_hub/providers/aliyun/qwen_tts
```

## 阿里云百炼 CosyVoice

默认读取 `DASHSCOPE_API_KEY`，需要环境里已安装 DashScope SDK。

这里把最常用的入口放在 `AliyunCosyVoiceTTS` 上：

- 系统音色：直接实例化 `AliyunCosyVoiceTTS(...)`
- 本地文件复刻：`AliyunCosyVoiceTTS.cloned(sample=...)`
- 公网 URL 复刻：`AliyunCosyVoiceTTS.cloned(audio_url=...)`

注意模型和音色必须匹配。当前系统音色使用 `cosyvoice-v3-flash`，复刻音色默认使用 `cosyvoice-v3.5-flash`。例如 `longanyang` 可以配 `cosyvoice-v3-flash`，不能配 `cosyvoice-v3.5-flash`。

系统音色合成：

```python
import voice_hub

tts = voice_hub.AliyunCosyVoiceTTS(
    voice=voice_hub.AliyunCosyVoice.LONGANYANG,
)

tts.speak("那我来给大家推荐一款T恤，这款颜色很显气质。").save("./tmp/cosyvoice.mp3")
```

本地文件复刻音色：

```python
tts = voice_hub.AliyunCosyVoiceTTS.cloned(
    sample="./tmp/voice-clones/vc30.wav",
    language_hints=["zh"],
)

tts.to_file(
    "恭喜，已成功复刻并合成了属于自己的声音。",
    "./tmp/cosyvoice-clone-from-file.mp3",
)

print(tts.voice_result.voice_id)
print(tts.voice_result.reused)
```

公网 URL 复刻音色：

```python
tts = voice_hub.AliyunCosyVoiceTTS.cloned(
    audio_url="https://example.com/reference.wav",
    language_hints=["zh"],
    max_prompt_audio_length=20.0,
    enable_preprocess=False,
)

tts.speak("How is the weather today?").save("./tmp/cosyvoice-clone.mp3")
```

复刻时默认会先复用已有音色，避免每次调用都创建新音色：

- `sample=...`：使用 `target_model + 文件内容` 的 MD5 派生 10 位以内前缀。
- `audio_url=...`：使用 `target_model + audio_url` 的 MD5 派生 10 位以内前缀。
- 创建前会先按前缀 `list_voices`，已有 `OK` 或 `DEPLOYING` 音色时直接复用。
- 也可以显式传入 `prefix`，例如 `prefix="myvoice"`。

本地文件模式会自动走百炼文件管理服务：

```text
本地音频文件
  └── 上传到 /api/v1/files
      └── 查询文件详情拿临时 OSS URL
          └── 调用 CosyVoice create_voice
              └── 使用 voice_id 合成语音
```

需要管理音色生命周期时，再使用底层管理器：

```python
clone = voice_hub.AliyunCosyVoiceClone(
    target_model=voice_hub.ALIYUN_COSYVOICE_CLONE_MODEL,
)

result = clone.get_or_create_voice_from_file("./tmp/voice-clones/vc30.wav")
clone.wait_until_ready(result.voice_id)
clone.tts(result.voice_id).speak("你好").save("./tmp/cosyvoice-clone.mp3")
```

常用复刻参数：

- `language_hints=["zh"]`：样本音频语种提示。
- `max_prompt_audio_length=20.0`：用于复刻的样本最大时长，适用于 v3/v3.5 相关模型。
- `enable_preprocess=False`：是否开启降噪、音频增强、音量规整等预处理。

手动真实测试在 `tests/test_my.py`，默认跳过。需要真实调用时：

```bash
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_aliyun_cosyvoice_system_voice -q -s
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py::test_aliyun_cosyvoice_clone_from_file_and_tts -q -s
```

当前测试输出示例：

```text
tmp/aliyun_cosyvoice_system.mp3
tmp/aliyun_cosyvoice_clone_from_file.mp3
```

代码目录：

```text
voice_hub/providers/aliyun/cosyvoice
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
- `DASHSCOPE_API_KEY`：阿里云百炼 API Key，`AliyunTTS` 和 `AliyunCosyVoiceTTS` 未显式传入 `api_key` 时默认读取
- `ALIYUN_COSYVOICE_MODEL`：CosyVoice 系统音色默认模型，当前为 `cosyvoice-v3-flash`
- `ALIYUN_COSYVOICE_CLONE_MODEL`：CosyVoice 复刻音色默认模型，当前为 `cosyvoice-v3.5-flash`

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
