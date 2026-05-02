from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from ..interfaces import TTSEngine
from ..speech import Speech


class BaseTTS(TTSEngine, ABC):
    """厂商 TTS 的最小公共接口。

    每个 provider 必须显式实现 ``speak``，避免调试时只跳到公共壳层。
    """

    @abstractmethod
    def speak(self, text: str, **overrides: object) -> Speech:
        raise NotImplementedError

    def to_file(self, text: str, path: str, **overrides: object) -> str:
        return self.speak(text, **overrides).save(path)

    def bytes(self, text: str, **overrides: object) -> bytes:
        return self.speak(text, **overrides).bytes()

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
        return self.speak(text, **overrides).stream()
