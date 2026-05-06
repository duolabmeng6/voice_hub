# voice_hub 教程

这些教程只讲怎么用。

先安装：

```bash
pip install duolabmeng6-voice-hub
```

基础安装适用于 MiniMax、MiMo、智谱 GLM 和阿里云百炼 Qwen TTS。

如果使用阿里云百炼 CosyVoice，需要额外安装 DashScope SDK：

```bash
pip install duolabmeng6-voice-hub dashscope
```

本地开发或测试时，请把额外依赖安装到当前项目使用的同一个 Python 环境：

```bash
python -m pip install -e . dashscope
```

推荐写法是先 `speak()`，再 `save()`：

```python
speech = tts.speak("你好，欢迎使用 voice_hub。")
speech.save("./tmp/output.mp3")
```

如果同一个项目里有多个声音，用 `Client` 管理：

```python
import voice_hub

client = voice_hub.Client()
client.add_speaker("旁白", voice_hub.MinimaxTTS(), default=True)

client.speaker("旁白").speak("欢迎回来。").save("./tmp/narrator.mp3")
```

## 教程目录

- [MiniMax](minimax-tts.md)
- [MiMo](mimo-tts.md)
- [智谱 GLM](glm-tts.md)
- [阿里云百炼](aliyun-tts.md)
