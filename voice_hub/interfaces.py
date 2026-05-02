from __future__ import annotations

from typing import Protocol

from .speech import Speech


class TTSEngine(Protocol):
    def speak(self, text: str, **overrides: object) -> Speech:
        ...
