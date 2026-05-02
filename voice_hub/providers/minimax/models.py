from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .voices import MinimaxVoice

MINIMAX_BASE_URL = "https://api.minimaxi.com/v1"
MINIMAX_T2A_MODEL = "speech-2.8-hd"


@dataclass(frozen=True)
class MinimaxRequest:
    model: str
    text: str
    stream: bool
    voice_setting: Mapping[str, object]
    audio_setting: Mapping[str, object]
    pronunciation_dict: Mapping[str, object] | None = None
    timbre_weights: list[Mapping[str, object]] | None = None
    language_boost: str | None = None
    voice_modify: Mapping[str, object] | None = None
    subtitle_enable: bool = False
    output_format: str = "hex"
    aigc_watermark: bool = False
    stream_options: Mapping[str, object] | None = None

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "model": self.model,
            "text": self.text,
            "stream": self.stream,
            "voice_setting": dict(self.voice_setting),
            "audio_setting": dict(self.audio_setting),
            "subtitle_enable": self.subtitle_enable,
        }

        if not self.stream:
            payload["output_format"] = self.output_format
            payload["aigc_watermark"] = self.aigc_watermark
        if self.stream_options is not None:
            payload["stream_options"] = dict(self.stream_options)
        if self.pronunciation_dict is not None:
            payload["pronunciation_dict"] = dict(self.pronunciation_dict)
        if self.timbre_weights is not None:
            payload["timbre_weights"] = [dict(item) for item in self.timbre_weights]
        if self.language_boost is not None:
            payload["language_boost"] = self.language_boost
        if self.voice_modify is not None:
            payload["voice_modify"] = dict(self.voice_modify)

        return payload
