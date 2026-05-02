from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

from .errors import ConfigurationError


class VoiceSample:
    """克隆音色所需的本地音频样本。"""

    SUPPORTED_MIME_TYPES = {"audio/mpeg", "audio/mp3", "audio/wav", "audio/x-wav"}

    def __init__(self, path: str | Path, mime_type: str | None = None) -> None:
        self.path = Path(path)
        self.mime_type = mime_type or self._guess_mime_type(self.path)

        if self.mime_type not in self.SUPPORTED_MIME_TYPES:
            raise ConfigurationError(
                "voice clone sample must be mp3 or wav, "
                f"got MIME type: {self.mime_type}"
            )

    def to_data_uri(self) -> str:
        if not self.path.exists():
            raise FileNotFoundError(str(self.path))

        encoded = base64.b64encode(self.path.read_bytes()).decode("utf-8")
        normalized_mime_type = "audio/wav" if self.mime_type == "audio/x-wav" else self.mime_type
        return f"data:{normalized_mime_type};base64,{encoded}"

    @staticmethod
    def _guess_mime_type(path: Path) -> str:
        mime_type, _ = mimetypes.guess_type(str(path))
        if path.suffix.lower() == ".mp3":
            return "audio/mpeg"
        if path.suffix.lower() == ".wav":
            return "audio/wav"
        return mime_type or "application/octet-stream"
