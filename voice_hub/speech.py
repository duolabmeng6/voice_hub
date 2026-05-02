from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping


class Speech:
    """一次已经完成的语音合成结果。"""

    def __init__(
        self,
        audio: bytes,
        *,
        text: str,
        overrides: Mapping[str, object] | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> None:
        if not isinstance(audio, bytes):
            raise TypeError("audio must be bytes")

        self._audio = audio
        self.text = text
        self.overrides = dict(overrides or {})
        self.metadata = dict(metadata or {})

    def bytes(self) -> bytes:
        return self._audio

    def save(self, path: str | Path) -> str:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(self.bytes())
        return str(output_path)

    def stream(self) -> Iterable[bytes]:
        yield self._audio
