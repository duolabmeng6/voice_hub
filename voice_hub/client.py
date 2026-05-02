from __future__ import annotations

from typing import Dict, Iterable, Optional, Protocol

from .errors import NoDefaultSpeakerError, SpeakerNotFoundError
from .speech import Speech


class TTSEngine(Protocol):
    def speak(self, text: str, **overrides: object) -> Speech:
        ...


class Client:
    """统一 speaker 管理器。"""

    def __init__(self) -> None:
        self._speakers: Dict[str, Speaker] = {}
        self._default_name: Optional[str] = None

    @property
    def default_name(self) -> Optional[str]:
        return self._default_name

    def add_speaker(self, name: str, engine: TTSEngine, default: bool = False) -> None:
        if not name or not name.strip():
            raise ValueError("speaker name cannot be empty")

        normalized_name = name.strip()
        self._speakers[normalized_name] = Speaker(normalized_name, engine)

        if default or self._default_name is None:
            self._default_name = normalized_name

    def set_default(self, name: str) -> None:
        self._ensure_speaker_exists(name)
        self._default_name = name

    def speaker(self, name: str) -> "Speaker":
        self._ensure_speaker_exists(name)
        return self._speakers[name]

    def speakers(self) -> Iterable[str]:
        return tuple(self._speakers.keys())

    def speak(self, text: str, **overrides: object) -> Speech:
        return self._default_speaker().speak(text, **overrides)

    def to_file(self, text: str, path: str, **overrides: object) -> str:
        return self.speak(text, **overrides).save(path)

    def bytes(self, text: str, **overrides: object) -> bytes:
        return self.speak(text, **overrides).bytes()

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
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
        return self.engine.speak(text, **overrides)

    def to_file(self, text: str, path: str, **overrides: object) -> str:
        return self.speak(text, **overrides).save(path)

    def bytes(self, text: str, **overrides: object) -> bytes:
        return self.speak(text, **overrides).bytes()

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
        return self.speak(text, **overrides).stream()
