from __future__ import annotations

from typing import Dict, Iterable, Optional

from .errors import NoDefaultSpeakerError, SpeakerNotFoundError
from .interfaces import TTSEngine
from .speech import Speech


class Client:
    """统一 speaker 管理器。

    ``Client`` 负责维护多个命名 speaker，并把 ``speak``、``bytes``、
    ``to_file``、``stream`` 等便捷调用路由到默认 speaker。
    """

    def __init__(self) -> None:
        self._speakers: Dict[str, Speaker] = {}
        self._default_name: Optional[str] = None

    @property
    def default_name(self) -> Optional[str]:
        """当前默认 speaker 名称；尚未注册 speaker 时返回 ``None``。"""
        return self._default_name

    def add_speaker(self, name: str, engine: TTSEngine, default: bool = False) -> None:
        """注册一个命名 speaker。

        参数:
            name: speaker 名称，会自动去掉首尾空白；不能为空。
                如果名称已存在，新 ``engine`` 会覆盖旧 speaker。
            engine: 具体 TTS 引擎实例，需要实现 ``speak(text, **overrides)``
                并返回 ``Speech``，例如 ``MimoTTS``。
            default: 是否把该 speaker 设为默认。首次注册 speaker 时，即使
                ``default=False``，也会自动成为默认 speaker。

        说明:
            默认 speaker 用于 ``client.speak(...)``、``client.bytes(...)`` 等
            未显式指定名称的便捷调用；命名 speaker 可通过
            ``client.speaker(name)`` 获取。
        """
        if not name or not name.strip():
            raise ValueError("speaker name cannot be empty")

        normalized_name = name.strip()
        self._speakers[normalized_name] = Speaker(normalized_name, engine)

        if default or self._default_name is None:
            self._default_name = normalized_name

    def set_default(self, name: str) -> None:
        """把已注册的 speaker 设置为默认 speaker。"""
        self._ensure_speaker_exists(name)
        self._default_name = name

    def speaker(self, name: str) -> "Speaker":
        """按名称获取 speaker，用于调用非默认音色。"""
        self._ensure_speaker_exists(name)
        return self._speakers[name]

    def speakers(self) -> Iterable[str]:
        """返回当前已注册的 speaker 名称快照。"""
        return tuple(self._speakers.keys())

    def speak(self, text: str, **overrides: object) -> Speech:
        """使用默认 speaker 创建一次语音合成请求。"""
        return self._default_speaker().speak(text, **overrides)

    def to_file(self, text: str, path: str, **overrides: object) -> str:
        """使用默认 speaker 合成语音并保存到文件，返回输出路径字符串。"""
        return self.speak(text, **overrides).save(path)

    def bytes(self, text: str, **overrides: object) -> bytes:
        """使用默认 speaker 合成语音并返回完整音频字节。"""
        return self.speak(text, **overrides).bytes()

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
        """使用默认 speaker 以迭代器形式返回音频分片。"""
        return self.speak(text, **overrides).stream()

    def _default_speaker(self) -> "Speaker":
        if self._default_name is None:
            raise NoDefaultSpeakerError("no default speaker configured")
        return self._speakers[self._default_name]

    def _ensure_speaker_exists(self, name: str) -> None:
        if name not in self._speakers:
            raise SpeakerNotFoundError(f"speaker not found: {name}")


class Speaker:
    """绑定名称和厂商引擎的 speaker。"""

    def __init__(self, name: str, engine: TTSEngine) -> None:
        self.name = name
        self.engine = engine

    def speak(self, text: str, **overrides: object) -> Speech:
        """使用当前 speaker 创建一次语音合成请求。"""
        return self.engine.speak(text, **overrides)

    def to_file(self, text: str, path: str, **overrides: object) -> str:
        """使用当前 speaker 合成语音并保存到文件，返回输出路径字符串。"""
        return self.speak(text, **overrides).save(path)

    def bytes(self, text: str, **overrides: object) -> bytes:
        """使用当前 speaker 合成语音并返回完整音频字节。"""
        return self.speak(text, **overrides).bytes()

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
        """使用当前 speaker 以迭代器形式返回音频分片。"""
        return self.speak(text, **overrides).stream()
