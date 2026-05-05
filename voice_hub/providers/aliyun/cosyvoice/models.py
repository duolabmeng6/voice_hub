from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


ALIYUN_COSYVOICE_HTTP_BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"
ALIYUN_COSYVOICE_CUSTOMIZATION_PATH = "/services/audio/tts/customization"
ALIYUN_COSYVOICE_FILES_PATH = "/files"
ALIYUN_COSYVOICE_MODEL = "cosyvoice-v3-flash"
ALIYUN_COSYVOICE_CLONE_MODEL = "cosyvoice-v3.5-flash"
ALIYUN_COSYVOICE_ENROLLMENT_MODEL = "voice-enrollment"


@dataclass(frozen=True)
class AliyunCosyVoiceEnrollmentResult:
    voice_id: str
    request_id: str | None
    target_model: str
    prefix: str
    audio_url: str
    reused: bool = False
    status: str | None = None


@dataclass(frozen=True)
class AliyunCosyVoiceUploadedFile:
    file_id: str
    name: str
    size: int | None = None
    md5: str | None = None
    url: str | None = None
    request_id: str | None = None


@dataclass(frozen=True)
class AliyunCosyVoiceRequest:
    model: str
    voice: str
    text: str
    format: str = "mp3"
    sample_rate: int = 24000
    volume: int = 50
    speech_rate: float = 1.0
    pitch_rate: float = 1.0
    seed: int = 0
    synthesis_type: int = 0
    instruction: str | None = None
    language_hints: list[str] | None = None
    additional_params: Mapping[str, object] | None = None

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "model": self.model,
            "voice": self.voice,
            "text": self.text,
            "format": self.format,
            "sample_rate": self.sample_rate,
            "volume": self.volume,
            "speech_rate": self.speech_rate,
            "pitch_rate": self.pitch_rate,
            "seed": self.seed,
            "synthesis_type": self.synthesis_type,
        }
        if self.instruction is not None:
            payload["instruction"] = self.instruction
        if self.language_hints is not None:
            payload["language_hints"] = list(self.language_hints)
        if self.additional_params is not None:
            payload["additional_params"] = dict(self.additional_params)
        return payload
