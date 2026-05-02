# voice_hub 接入教程

这里放完整的语音合成接入流程。README 只保留快速示例，具体模型、音色、环境变量、克隆流程和真实测试命令都写在这里。

## 教程目录

- [阿里云百炼语音合成接入流程](aliyun-tts.md)
- [MiniMax 语音合成接入流程](minimax-tts.md)
- [MiMo 语音合成接入流程](mimo-tts.md)

## 统一使用方式

所有 provider 都返回 `Speech` 对象，常用方法一致：

```python
speech = tts.speak("你好")
audio_bytes = speech.bytes()
speech.save("./tmp/output.mp3")
```

也可以使用统一 speaker 管理器：

```python
import voice_hub

client = voice_hub.Client()
client.add_speaker("main", voice_hub.MinimaxTTS(), default=True)
client.to_file("你好，欢迎使用 voice_hub。", "./tmp/main.mp3")
```

## 本地验证

普通单测不发真实网络请求：

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```

真实调用测试默认跳过，需要显式开启：

```bash
VOICE_HUB_RUN_LIVE_TESTS=1 python -m pytest tests/test_my.py -q -s
```

