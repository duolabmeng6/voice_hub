# voice_hub

[![PyPI version](https://img.shields.io/pypi/v/duolabmeng6-voice-hub.svg)](https://pypi.org/project/duolabmeng6-voice-hub/)
[![Python versions](https://img.shields.io/pypi/pyversions/duolabmeng6-voice-hub.svg)](https://pypi.org/project/duolabmeng6-voice-hub/)
[![Downloads](https://img.shields.io/pepy/dt/duolabmeng6-voice-hub.svg)](https://pepy.tech/project/duolabmeng6-voice-hub)

多厂商 TTS 的 speaker 路由器。把 MiniMax、MiMo、智谱 GLM、阿里云百炼这些服务收进一个 `Client`，像管理配音演员一样管理 AI 声音。

业务代码只关心三件事：让谁说、说什么、存到哪。系统音色、克隆音色、文本设计音色、不同厂商的 payload 和音频返回格式，都交给 `voice_hub` 处理。

```python
client.speaker("旁白").speak("欢迎回来。").save("narrator.mp3")
client.speaker("女主").speak("我已经准备好了。").save("heroine.wav")
client.speaker("广告音").speak("限时优惠，现在开始。").save("ad.mp3")
```

适合这些场景：

- 短视频、直播切片、广告素材批量生成
- 同一个项目里混用多个 TTS 厂商
- 给不同角色绑定不同声音，随时切换 speaker
- 复用克隆音色，避免业务代码到处写 provider 细节
- 先用一个厂商上线，后面平滑替换或增加新声音

核心优势：

- **角色化**：把声音注册成 `旁白`、`女主`、`广告音` 这样的业务名字。
- **多厂商统一**：MiniMax、MiMo、GLM、阿里云都走同一套调用方式。
- **少改业务代码**：换声音、换模型、换 provider，不需要到处改生成逻辑。
- **音频结果一致**：统一拿 bytes、保存文件、读取 metadata。

- PyPI: <https://pypi.org/project/duolabmeng6-voice-hub/>
- 下载统计: <https://pepy.tech/project/duolabmeng6-voice-hub>
- PyPIStats: <https://pypistats.org/packages/duolabmeng6-voice-hub>
- 仓库: <https://github.com/duolabmeng6/voice_hub>
- Issues: <https://github.com/duolabmeng6/voice_hub/issues>

## 安装

```bash
pip install duolabmeng6-voice-hub
```

Python 版本要求：`>=3.10`。

## 为什么用它

直接接 TTS 服务时，业务代码很快会被这些问题拖住：

- 每家 provider 的认证、payload、返回音频格式都不一样。
- 系统音色、克隆音色、设计音色的创建方式不一样。
- 切换声音时容易把业务逻辑和厂商参数混在一起。
- 批量生成时，需要稳定地保存音频、拿字节、记录元数据。

`voice_hub` 把这些差异压到 provider 层。业务层只和 speaker 打交道：

```python
client.add_speaker("旁白", minimax_tts, default=True)
client.add_speaker("女主", mimo_clone_tts)
client.add_speaker("广告音", aliyun_tts)

client.speak("默认 speaker 会说这句话。").save("default.mp3")
client.speaker("女主").speak("这句换女主说。").save("heroine.wav")
```

## 支持的声音来源

| Provider | 入口 | 默认环境变量 | 说明 |
| --- | --- | --- | --- |
| MiniMax | `voice_hub.MinimaxTTS` | `MINIMAX_KEY` | 同步/流式 T2A、系统音色、快速复刻试听 |
| MiMo | `voice_hub.MimoTTS` | 手动传入 `api_key` | 内置音色、文本设计音色、参考音频克隆 |
| 智谱 GLM | `voice_hub.GLMTTS` | `ZHIPUAI_API_KEY` | 系统音色和克隆后的 `voice_id` |
| 阿里云百炼 Qwen TTS | `voice_hub.AliyunTTS` | `DASHSCOPE_API_KEY` | Qwen TTS 系统音色、指令控制 |
| 阿里云百炼 CosyVoice | `voice_hub.AliyunCosyVoiceTTS` | `DASHSCOPE_API_KEY` | 系统音色、本地文件复刻、公网 URL 复刻 |
| OpenAI / Azure | `voice_hub.OpenAITTS` / `voice_hub.AzureTTS` | 按实例配置 | 占位/扩展入口 |

更完整的接入流程见：

- [阿里云百炼语音合成接入流程](https://github.com/duolabmeng6/voice_hub/blob/main/docs/aliyun-tts.md)
- [智谱 GLM TTS 接入流程](https://github.com/duolabmeng6/voice_hub/blob/main/docs/glm-tts.md)
- [MiniMax 语音合成接入流程](https://github.com/duolabmeng6/voice_hub/blob/main/docs/minimax-tts.md)
- [MiMo 语音合成接入流程](https://github.com/duolabmeng6/voice_hub/blob/main/docs/mimo-tts.md)

## 快速开始

用 MiniMax 创建一个 speaker：

```python
import os
import voice_hub

client = voice_hub.Client()

client.add_speaker(
    "旁白",
    voice_hub.MinimaxTTS(
        api_key=os.environ["MINIMAX_KEY"],
        voice=voice_hub.MinimaxVoice.MALE_QN_QINGSE,
        emotion="happy",
        format="mp3",
    ),
    default=True,
)

client.speak("夜深了，城市还没有睡。").save("./tmp/narrator.mp3")
```

再加一个 MiMo 克隆音色：

```python
client.add_speaker(
    "龙儿",
    voice_hub.MimoTTS.cloned(
        api_key=os.environ["MIMO_TOKEN_KEY"],
        base_url=os.environ["MIMO_TOKEN_BASE_URL"],
        sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
        style="自然、快速讲话",
    ),
)

client.speaker("龙儿").speak("这句话换成克隆音色来说。").save("./tmp/longer.wav")
```

需要音频字节或元数据时，拿 `Speech` 对象：

```python
speech = client.speaker("旁白").speak("你好，欢迎使用 voice_hub。")

audio_bytes = speech.bytes()
saved_path = speech.save("./tmp/output.mp3")
metadata = speech.metadata
```

也可以绕过 `Client`，直接调用单个 provider：

```python
tts = voice_hub.GLMTTS(
    voice=voice_hub.GLMVoice.FEMALE,
    response_format="wav",
    watermark_enabled=False,
)

tts.speak("夜深了，城市还没有睡。").save("./tmp/glm.wav")
```

## 多 speaker 管理

```python
import os
import voice_hub

client = voice_hub.Client()

client.add_speaker(
    "冰糖",
    voice_hub.MimoTTS(
        api_key=os.environ["MIMO_API_KEY"],
        base_url=os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"),
        voice=voice_hub.MimoVoice.BINGTANG,
        style="自然、平稳",
    ),
    default=True,
)

client.add_speaker(
    "龙儿克隆",
    voice_hub.MimoTTS.cloned(
        api_key=os.environ["MIMO_TOKEN_KEY"],
        base_url=os.environ["MIMO_TOKEN_BASE_URL"],
        sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
        style="自然、快速讲话",
    ),
)

client.add_speaker(
    "龙儿女生",
    voice_hub.MimoTTS.designed(
        api_key=os.environ["MIMO_TOKEN_KEY"],
        base_url=os.environ["MIMO_TOKEN_BASE_URL"],
        prompt="年轻女性，温柔、松弛、有轻微气声",
        style="自然、平稳",
    ),
)

client.speaker("冰糖").speak("夜深了，城市还没有睡。").save("./tmp/冰糖.wav")
client.speaker("龙儿女生").speak("夜深了，城市还没有睡。").save("./tmp/龙儿女生.wav")
client.speaker("龙儿克隆").speak("夜深了，城市还没有睡。").save("./tmp/龙儿克隆.wav")
```

## MiniMax

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

## MiMo

```python
import os
import voice_hub

api_key = os.environ["MIMO_API_KEY"]
base_url = os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")

system_tts = voice_hub.MimoTTS(
    api_key=api_key,
    base_url=base_url,
    voice=voice_hub.MimoVoice.BINGTANG,
    style="轻快",
    format="wav",
)

designed_tts = voice_hub.MimoTTS.designed(
    api_key=api_key,
    base_url=base_url,
    prompt="年轻女性，温柔、松弛、有轻微气声",
    style="自然、平稳",
)

cloned_tts = voice_hub.MimoTTS.cloned(
    api_key=api_key,
    base_url=base_url,
    sample=voice_hub.VoiceSample("voice.mp3"),
    style="自然、平稳",
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

## 智谱 GLM TTS

默认读取 `ZHIPUAI_API_KEY`，直接调用智谱 HTTP API。完整说明见 [智谱 GLM TTS 接入流程](https://github.com/duolabmeng6/voice_hub/blob/main/docs/glm-tts.md)。

```python
import voice_hub

tts = voice_hub.GLMTTS(
    voice=voice_hub.GLMVoice.FEMALE,
    response_format="wav",
    watermark_enabled=False,
)

tts.speak("夜深了，城市还没有睡。").save("./tmp/glm.wav")
```

`watermark_enabled=False` 只对已经在智谱控制台完成去水印开通的账号生效；否则服务端可能仍会返回带显式水印的音频。

当前内置官方系统音色：

```python
voice_hub.GLM_SYSTEM_VOICE_IDS
# ("female", "male", "tongtong", "chuichui", "xiaochen", "jam", "kazi", "douji", "luodo")
```

也可以使用克隆后的 `voice_id`：

```python
tts = voice_hub.GLMTTS(voice="your_voice_id", response_format="wav")
tts.speak("你好，这是使用克隆音色合成的语音。").save("./tmp/glm-clone.wav")
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

新加坡地域可把 `base_url` 改为 `voice_hub.ALIYUN_INTL_BASE_URL`。北京和新加坡 API Key 不通用。

## 阿里云百炼 CosyVoice

默认读取 `DASHSCOPE_API_KEY`，需要环境里已安装 DashScope SDK。

常用入口：

- 系统音色：直接实例化 `AliyunCosyVoiceTTS(...)`
- 本地文件复刻：`AliyunCosyVoiceTTS.cloned(sample=...)`
- 公网 URL 复刻：`AliyunCosyVoiceTTS.cloned(audio_url=...)`

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

tts.speak(
    "恭喜，已成功复刻并合成了属于自己的声音。",
).save("./tmp/cosyvoice-clone-from-file.mp3")

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

## 本地验证

普通单测不发真实网络请求：

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest \
  tests/test_client.py \
  tests/test_glm.py \
  tests/test_mimo.py \
  tests/test_minimax.py \
  tests/test_aliyun.py \
  tests/test_aliyun_cosyvoice.py \
  -q
```

真实调用测试集中在 `tests/test_my.py`，会读取本地 `.env` 并调用真实 provider：

```bash
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py -q -s
```

## 发布检查

构建并检查包：

```bash
python -m build
python -m twine check dist/*
```

发布到 PyPI 后，可以从以下地址确认版本、包文件和下载统计：

- <https://pypi.org/project/duolabmeng6-voice-hub/>
- <https://pepy.tech/project/duolabmeng6-voice-hub>
- <https://pypistats.org/packages/duolabmeng6-voice-hub>
