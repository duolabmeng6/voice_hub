from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Iterable, Mapping

from ....errors import ConfigurationError
from ....speech import Speech
from ...base import BaseTTS
from .models import (
    ALIYUN_COSYVOICE_CLONE_MODEL,
    ALIYUN_COSYVOICE_HTTP_BASE_URL,
    ALIYUN_COSYVOICE_MODEL,
    ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL,
    AliyunCosyVoiceEnrollmentResult,
    AliyunCosyVoiceRequest,
)
from .transport import AliyunCosyVoiceSDKTransport
from .voices import AliyunCosyVoice


class AliyunCosyVoiceTTS(BaseTTS):
    """阿里云 CosyVoice 系统音色或已创建克隆音色 provider。"""

    def __init__(
        self,
        api_key: str | None = None,
        voice: str = AliyunCosyVoice.LONGANYANG,
        model: str = ALIYUN_COSYVOICE_MODEL,
        format: str = "mp3",
        sample_rate: int = 24000,
        volume: int = 50,
        speech_rate: float = 1.0,
        pitch_rate: float = 1.0,
        seed: int = 0,
        synthesis_type: int = 0,
        instruction: str | None = None,
        language_hints: list[str] | None = None,
        additional_params: Mapping[str, object] | None = None,
        http_base_url: str = ALIYUN_COSYVOICE_HTTP_BASE_URL,
        websocket_base_url: str = ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL,
        transport: AliyunCosyVoiceSDKTransport | None = None,
        timeout: float = 60,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("DASHSCOPE_API_KEY", "")
        self.voice = voice
        self.model = model
        self.format = format
        self.sample_rate = sample_rate
        self.volume = volume
        self.speech_rate = speech_rate
        self.pitch_rate = pitch_rate
        self.seed = seed
        self.synthesis_type = synthesis_type
        self.instruction = instruction
        self.language_hints = language_hints
        self.additional_params = additional_params
        self.http_base_url = http_base_url
        self.websocket_base_url = websocket_base_url
        self.transport = transport or AliyunCosyVoiceSDKTransport()
        self.timeout = timeout
        self.voice_result: AliyunCosyVoiceEnrollmentResult | None = None
        self._validate_config()

    def speak(self, text: str, **overrides: object) -> Speech:
        request = self.build_request(text, **overrides)
        start = time.monotonic()
        audio, request_id = self.transport.synthesize(
            api_key=self.api_key,
            model=request.model,
            voice=request.voice,
            text=request.text,
            format=request.format,
            sample_rate=request.sample_rate,
            volume=request.volume,
            speech_rate=request.speech_rate,
            pitch_rate=request.pitch_rate,
            seed=request.seed,
            synthesis_type=request.synthesis_type,
            instruction=request.instruction,
            language_hints=request.language_hints,
            additional_params=request.additional_params,
            http_base_url=self.http_base_url,
            websocket_base_url=self.websocket_base_url,
            timeout=self.timeout,
        )
        elapsed_ms = round((time.monotonic() - start) * 1000, 3)
        return Speech(
            audio,
            text=text,
            overrides=overrides,
            metadata={
                "provider": self.__class__.__name__,
                "model": request.model,
                "voice": request.voice,
                "request_id": request_id,
                "elapsed_ms": elapsed_ms,
                "audio_bytes": len(audio),
                "payload": request.to_payload(),
                "voice_result": self.voice_result,
            },
        )

    @classmethod
    def cloned(
        cls,
        api_key: str | None = None,
        sample: str | Path | None = None,
        audio_url: str | None = None,
        prefix: str | None = None,
        language_hints: list[str] | None = None,
        max_prompt_audio_length: float | None = None,
        enable_preprocess: bool | None = None,
        model: str = ALIYUN_COSYVOICE_CLONE_MODEL,
        wait: bool = True,
        max_attempts: int = 30,
        poll_interval: float = 10,
        format: str = "mp3",
        sample_rate: int = 24000,
        http_base_url: str = ALIYUN_COSYVOICE_HTTP_BASE_URL,
        websocket_base_url: str = ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL,
        transport: AliyunCosyVoiceSDKTransport | None = None,
        timeout: float = 120,
        **kwargs: object,
    ) -> "AliyunCosyVoiceTTS":
        """创建复刻音色 TTS provider，自动复用已有音色。"""
        from .clone import AliyunCosyVoiceClone

        if sample is None and audio_url is None:
            raise ConfigurationError("sample or audio_url is required for CosyVoice clone")
        if sample is not None and audio_url is not None:
            raise ConfigurationError("sample and audio_url cannot be used together")

        clone = AliyunCosyVoiceClone(
            api_key=api_key,
            target_model=model,
            http_base_url=http_base_url,
            websocket_base_url=websocket_base_url,
            transport=transport,
            timeout=timeout,
        )
        if sample is not None:
            result = clone.get_or_create_voice_from_file(
                sample,
                prefix=prefix,
                language_hints=language_hints,
                max_prompt_audio_length=max_prompt_audio_length,
                enable_preprocess=enable_preprocess,
            )
        else:
            result = clone.get_or_create_voice(
                audio_url=str(audio_url),
                prefix=prefix,
                language_hints=language_hints,
                max_prompt_audio_length=max_prompt_audio_length,
                enable_preprocess=enable_preprocess,
            )
        return clone.tts_from_voice(
            result,
            wait=wait,
            max_attempts=max_attempts,
            poll_interval=poll_interval,
            format=format,
            sample_rate=sample_rate,
            **kwargs,
        )

    def build_payload(self, text: str, **overrides: object) -> dict[str, object]:
        return self.build_request(text, **overrides).to_payload()

    def build_request(self, text: str, **overrides: object) -> AliyunCosyVoiceRequest:
        options = self._merged_options(overrides)
        return AliyunCosyVoiceRequest(
            model=str(options["model"]),
            voice=str(options["voice"]),
            text=text,
            format=str(options["format"]),
            sample_rate=int(options["sample_rate"]),
            volume=int(options["volume"]),
            speech_rate=float(options["speech_rate"]),
            pitch_rate=float(options["pitch_rate"]),
            seed=int(options["seed"]),
            synthesis_type=int(options["synthesis_type"]),
            instruction=_optional_str(options.get("instruction")),
            language_hints=_optional_str_list(options.get("language_hints")),
            additional_params=_optional_mapping(options.get("additional_params")),
        )

    def synthesize(self, text: str, **overrides: object) -> bytes:
        return self.speak(text, **overrides).bytes()

    def bytes(self, text: str, **overrides: object) -> bytes:
        return self.synthesize(text, **overrides)

    def to_file(self, text: str, path: str | Path, **overrides: object) -> str:
        return self.speak(text, **overrides).save(path)

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
        return self.speak(text, **overrides).stream()

    def _merged_options(self, overrides: Mapping[str, object]) -> dict[str, object]:
        options: dict[str, object] = {
            "model": self.model,
            "voice": self.voice,
            "format": self.format,
            "sample_rate": self.sample_rate,
            "volume": self.volume,
            "speech_rate": self.speech_rate,
            "pitch_rate": self.pitch_rate,
            "seed": self.seed,
            "synthesis_type": self.synthesis_type,
            "instruction": self.instruction,
            "language_hints": self.language_hints,
            "additional_params": self.additional_params,
        }
        unknown_keys = set(overrides) - set(options)
        if unknown_keys:
            unknown = ", ".join(sorted(unknown_keys))
            raise TypeError(f"unsupported Aliyun CosyVoice override(s): {unknown}")
        options.update({key: value for key, value in overrides.items() if value is not None})
        return options

    def _validate_config(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("Aliyun CosyVoice api_key is required")
        if not self.http_base_url or not self.http_base_url.strip():
            raise ConfigurationError("Aliyun CosyVoice http_base_url is required")
        if not self.websocket_base_url or not self.websocket_base_url.strip():
            raise ConfigurationError("Aliyun CosyVoice websocket_base_url is required")
        if self.timeout <= 0:
            raise ConfigurationError("Aliyun CosyVoice timeout must be greater than 0")
        self.build_payload("config check")


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)


def _optional_str_list(value: object) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    raise ConfigurationError("language_hints must be a string list")


def _optional_mapping(value: object) -> Mapping[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ConfigurationError("additional_params must be a mapping")
    return value
