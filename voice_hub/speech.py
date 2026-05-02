from __future__ import annotations

from pathlib import Path
from typing import Iterable, Protocol


class SpeechProvider(Protocol):
    def synthesize(self, text: str, **overrides: object) -> bytes:
        ...

    def stream_synthesize(self, text: str, **overrides: object) -> Iterable[bytes]:
        ...


class Speech:
    """一次待执行的语音合成请求。"""

    def __init__(self, provider: SpeechProvider, text: str, overrides: dict[str, object]):
        if not isinstance(text, str) or not text:
            raise ValueError("text must be a non-empty string")

        self._provider = provider
        self.text = text
        self.overrides = dict(overrides)

    def bytes(self) -> bytes:
        return self._provider.synthesize(self.text, **self.overrides)

    def save(self, path: str | Path) -> str:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(self.bytes())
        return str(output_path)

    def stream(self) -> Iterable[bytes]:
        return self._provider.stream_synthesize(self.text, **self.overrides)
