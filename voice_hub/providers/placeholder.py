from __future__ import annotations

from typing import Iterable

from ..errors import ProviderError
from ..speech import Speech
from .base import BaseTTS


class UnsupportedTTS(BaseTTS):
    provider_name = "unsupported"

    def speak(self, text: str, **overrides: object) -> Speech:
        raise ProviderError(f"{self.provider_name} provider is not implemented yet")

    def synthesize(self, text: str, **overrides: object) -> bytes:
        raise ProviderError(f"{self.provider_name} provider is not implemented yet")

    def stream_synthesize(self, text: str, **overrides: object) -> Iterable[bytes]:
        raise ProviderError(f"{self.provider_name} provider is not implemented yet")
