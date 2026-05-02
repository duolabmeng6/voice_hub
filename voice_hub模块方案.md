# voicehub 模块方案

## 1. 设计目标

voicehub 设计成 **统一 speaker 管理器**，不是统一 provider 调用器。

核心规则：

```text
配置阶段：关心厂商、音色、风格、格式
调用阶段：只关心文本和输出位置
```

主路径：

```python
tts.speak("夜深了，城市还没有睡。").save("out.wav")
tts.speaker("xiaoxiao").speak("你好").save("xiaoxiao.wav")
```


## 2. 公开 API

```python
import voice_hub

voice_hub.Client

voice_hub.MimoTTS
voice_hub.AzureTTS
voice_hub.OpenAITTS

voice_hub.VoiceSample
```

### Client

```python
tts = voice_hub.Client()

tts.add_speaker(name, engine, default=False)
tts.set_default(name)
tts.speaker(name)

tts.speak(text, **overrides)
tts.to_file(text, path, **overrides)
tts.bytes(text, **overrides)
tts.stream(text, **overrides)
```

### Speaker

```python
tts.speaker(name).speak(text, **overrides)
tts.speaker(name).to_file(text, path, **overrides)
tts.speaker(name).bytes(text, **overrides)
tts.speaker(name).stream(text, **overrides)
```

### Speech

```python
speech = tts.speak("你好")

speech.save(path)
speech.bytes()
speech.stream()
```


## 3. 推荐用法

```python
import voice_hub

tts = voice_hub.Client()

tts.add_speaker(
    "narrator",
    voice_hub.MimoTTS(
        api_key="",
        voice="冰糖",
        style="自然、平稳",
        format="wav",
    ),
    default=True,
)

tts.speak("夜深了，城市还没有睡。").save("out.wav")
```

多 speaker：

```python
tts.add_speaker(
    "bingtang",
    voice_hub.MimoTTS(
        api_key="",
        voice="冰糖",
        style="轻快、兴奋、语速稍快",
        format="wav",
    ),
    default=True,
)

tts.add_speaker(
    "xiaoxiao",
    voice_hub.AzureTTS(
        api_key="",
        region="eastasia",
        voice="zh-CN-XiaoxiaoNeural",
        format="wav",
    ),
)

tts.speak("这是默认 speaker。").save("default.wav")
tts.speaker("xiaoxiao").speak("这是 Azure 晓晓的声音。").save("xiaoxiao.wav")
```


## 4. MiMo 音色 API

### 普通音色

```python
voice_hub.MimoTTS(
    api_key="",
    voice="冰糖",
    style="自然、平稳",
    format="wav",
)
```

### 设计音色

```python
voice_hub.MimoTTS.designed(
    api_key="",
    prompt="年轻女性，温柔、松弛、有轻微气声",
    style="自然、平稳",
    format="wav",
)
```

### 克隆音色

```python
voice_hub.MimoTTS.cloned(
    api_key="",
    sample="voice.mp3",
    style="自然、平稳",
    format="wav",
)
```

可选样本对象：

```python
sample = voice_hub.VoiceSample("voice.mp3")

voice_hub.MimoTTS.cloned(
    api_key="",
    sample=sample,
)
```


## 5. 输出方式

链式写法：

```python
audio = tts.speak("这是一段测试语音。").bytes()
tts.speak("这是一段测试语音。").save("out.wav")

for chunk in tts.speak("这是一段流式语音。").stream():
    handle(chunk)
```

快捷写法：

```python
audio = tts.bytes("这是一段测试语音。")
tts.to_file("这是一段测试语音。", "out.wav")

for chunk in tts.stream("这是一段流式语音。"):
    handle(chunk)
```

指定 speaker：

```python
audio = tts.speaker("xiaoxiao").bytes("你好")
tts.speaker("xiaoxiao").to_file("你好", "xiaoxiao.wav")
```


## 6. 临时覆盖参数

长期配置放 speaker 初始化。

短期变化放 `speak()` overrides：

```python
tts.speak("这句话临时加快语速。", speed=1.2).save("fast.wav")
tts.speak("这句话临时换个声音。", voice="另一个音色").save("temp.wav")
```

文档主推初始化配置，不主推频繁 overrides。


## 7. 厂商独立使用

统一入口之外，厂商模块必须能独立使用。

```python
from voicehub.providers.mimo import MimoTTS

mimo = MimoTTS(
    api_key="",
    voice="冰糖",
    style="自然、平稳",
    format="wav",
)

audio = mimo.speak("你好。").bytes()
mimo.speak("你好。").save("out.wav")
```


## 8. 命名定稿

```text
统一入口：Client
注册声音配置：add_speaker
默认声音配置：set_default
选择声音配置：speaker(name)
说话动作：speak(text)
生成结果对象：Speech
保存结果：speech.save(path)
返回音频 bytes：speech.bytes()
返回流式 chunk：speech.stream()

MiMo 引擎：MimoTTS
Azure 引擎：AzureTTS
OpenAI 引擎：OpenAITTS
MiMo 设计音色：MimoTTS.designed(...)
MiMo 克隆音色：MimoTTS.cloned(...)
```


## 9. 模块结构

```text
voicehub/
├── __init__.py
├── client.py
├── speaker.py
├── speech.py
├── errors.py
├── types.py
├── providers/
│   ├── __init__.py
│   ├── base.py
│   ├── mimo/
│   │   ├── __init__.py
│   │   ├── provider.py
│   │   ├── client.py
│   │   ├── mapper.py
│   │   └── errors.py
│   ├── azure/
│   │   ├── __init__.py
│   │   ├── provider.py
│   │   ├── client.py
│   │   ├── mapper.py
│   │   └── errors.py
│   └── openai/
│       ├── __init__.py
│       ├── provider.py
│       ├── client.py
│       ├── mapper.py
│       └── errors.py
└── tests/
    ├── test_client.py
    ├── test_speaker.py
    ├── test_speech.py
    └── providers/
        └── test_mimo.py
```

结构原则：

```text
一个厂商一个目录
每个厂商独立测试
后续可拆成插件包
```


## 10. 核心类设计

### Client

```python
class Client:
    def __init__(self, default: str | None = None):
        self._default = default
        self._speakers = {}

    def add_speaker(self, name: str, engine, default: bool = False):
        self._speakers[name] = Speaker(name=name, engine=engine)

        if default or self._default is None:
            self._default = name

        return self

    def set_default(self, name: str):
        self._get_speaker(name)
        self._default = name
        return self

    def speaker(self, name: str):
        return self._get_speaker(name)

    def speak(self, text: str, **overrides):
        return self._get_speaker(self._default).speak(text, **overrides)

    def to_file(self, text: str, path: str, **overrides):
        return self.speak(text, **overrides).save(path)

    def bytes(self, text: str, **overrides) -> bytes:
        return self.speak(text, **overrides).bytes()

    def stream(self, text: str, **overrides):
        return self.speak(text, **overrides).stream()

    def _get_speaker(self, name: str | None):
        if not name:
            raise ConfigError("default speaker is required")

        if name not in self._speakers:
            raise ConfigError(f"speaker not found: {name}")

        return self._speakers[name]
```

### Speaker

```python
class Speaker:
    def __init__(self, name: str, engine):
        self.name = name
        self.engine = engine

    def speak(self, text: str, **overrides):
        return Speech(engine=self.engine, text=text, overrides=overrides)

    def to_file(self, text: str, path: str, **overrides):
        return self.speak(text, **overrides).save(path)

    def bytes(self, text: str, **overrides) -> bytes:
        return self.speak(text, **overrides).bytes()

    def stream(self, text: str, **overrides):
        return self.speak(text, **overrides).stream()
```

### Speech

```python
from pathlib import Path


class Speech:
    def __init__(self, engine, text: str, overrides: dict | None = None):
        self.engine = engine
        self.text = text
        self.overrides = overrides or {}

    def bytes(self) -> bytes:
        return self.engine.synthesize(self.text, **self.overrides)

    def save(self, path: str | Path):
        data = self.bytes()
        path = Path(path)
        path.write_bytes(data)
        return path

    def stream(self):
        return self.engine.stream(self.text, **self.overrides)
```

`save()` 只写服务商返回的音频 bytes，不做默认转码。

### TTSEngine

```python
from typing import Iterator, Protocol


class TTSEngine(Protocol):
    def synthesize(self, text: str, **overrides) -> bytes:
        ...

    def stream(self, text: str, **overrides) -> Iterator[bytes]:
        ...
```


## 11. MiMo 内部设计

### 配置对象

```python
@dataclass
class MimoVoiceConfig:
    mode: Literal["builtin", "designed", "cloned"]
    voice: str | None = None
    prompt: str | None = None
    sample: str | Path | VoiceSample | None = None
```

`MimoVoiceConfig` 为内部对象，不作为用户必须理解的公开主模型。

### 模型选择

```python
if config.mode == "designed":
    model = "mimo-v2.5-tts-voicedesign"
elif config.mode == "cloned":
    model = "mimo-v2.5-tts-voiceclone"
else:
    model = "mimo-v2.5-tts"
```

### Payload 映射

普通音色：

```python
{
    "model": "mimo-v2.5-tts",
    "messages": [
        {"role": "user", "content": style},
        {"role": "assistant", "content": text},
    ],
    "audio": {
        "format": format,
        "voice": voice,
    },
}
```

设计音色：

```python
{
    "model": "mimo-v2.5-tts-voicedesign",
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": text},
    ],
    "audio": {
        "format": format,
    },
}
```

克隆音色：

```python
{
    "model": "mimo-v2.5-tts-voiceclone",
    "messages": [
        {"role": "user", "content": style},
        {"role": "assistant", "content": text},
    ],
    "audio": {
        "format": format,
        "voice": "data:audio/mpeg;base64,...",
    },
}
```

克隆音频转 `data:audio/...;base64,...` 的逻辑放在 `mapper.py`。


## 12. 异常设计

```python
class VoiceHubError(Exception):
    pass


class ConfigError(VoiceHubError):
    pass


class ProviderError(VoiceHubError):
    pass


class UnsupportedError(VoiceHubError):
    pass
```


## 13. 第一阶段 MVP

实现：

```text
Client
Speaker
Speech

MimoTTS
MimoTTS(...)
MimoTTS.designed(...)
MimoTTS.cloned(...)

add_speaker
set_default
speaker
speak
to_file
bytes
stream

MiMo 非流式合成
MiMo payload mapper
MiMo 单元测试
```

暂不做：

```text
AzureTTS
OpenAITTS
插件自动加载
能力系统 Capability
音频转码
复杂配置文件
异步接口
批量合成
```


## 14. 后续阶段

第二阶段：

```text
AzureTTS
OpenAITTS
VolcengineTTS
AliyunTTS
更多输出格式
更完整 stream
错误码标准化
文档示例
```

第三阶段：

```text
插件系统
voicehub.load_plugins()
voicehub.create(...)
音频转码 export()
异步 async_speak()
批量 batch()
本地缓存
音色列表 list_voices()
```
