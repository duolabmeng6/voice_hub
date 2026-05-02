from __future__ import annotations

from typing import Iterable

from ..interfaces import TTSEngine
from ..speech import Speech


class BaseTTS(TTSEngine):
    """厂商 TTS 的最小公共接口。"""

    def speak(self, text: str, **overrides: object) -> Speech:
        return Speech(self, text, overrides)

    def to_file(self, text: str, path: str, **overrides: object) -> str:
        return self.speak(text, **overrides).save(path)

    def bytes(self, text: str, **overrides: object) -> bytes:
        return self.speak(text, **overrides).bytes()

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
        return self.speak(text, **overrides).stream()
