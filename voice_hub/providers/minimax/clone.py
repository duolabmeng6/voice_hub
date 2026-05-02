from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Mapping

from ...errors import ConfigurationError, ProviderError
from ...speech import Speech
from .models import (
    MINIMAX_BASE_URL,
    MINIMAX_VOICE_CLONE_MODEL,
    MinimaxClonePrompt,
    MinimaxVoiceCloneResult,
)
from .parser import _raise_for_base_resp
from .transport import MinimaxHTTPTransport


class MinimaxVoiceClone:
    """MiniMax 音色快速复刻客户端，仅调用上传和复刻试听接口。"""

    SUPPORTED_SUFFIXES = {".mp3", ".m4a", ".wav"}
    MAX_AUDIO_BYTES = 20 * 1024 * 1024
    _VOICE_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{6,254}[A-Za-z0-9]$")

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = MINIMAX_BASE_URL,
        transport: MinimaxHTTPTransport | None = None,
        timeout: float = 120,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("MINIMAX_KEY2", "")
        self.base_url = base_url
        self.transport = transport or MinimaxHTTPTransport()
        self.timeout = timeout
        self._validate_config()

    def upload_clone_audio(self, path: str | Path) -> str | int:
        """上传 10 秒到 5 分钟的复刻音频，返回 file_id。"""
        self._validate_audio_file(path)
        response = self.transport.upload_file(
            self.base_url,
            self.api_key,
            path,
            "voice_clone",
            self.timeout,
        )
        _raise_for_base_resp(response)
        return self._extract_file_id(response)

    def upload_prompt_audio(self, path: str | Path) -> str | int:
        """上传小于 8 秒的示例音频，返回 file_id。"""
        self._validate_audio_file(path)
        response = self.transport.upload_file(
            self.base_url,
            self.api_key,
            path,
            "prompt_audio",
            self.timeout,
        )
        _raise_for_base_resp(response)
        return self._extract_file_id(response)

    def clone(
        self,
        file_id: str | int,
        voice_id: str,
        text: str,
        *,
        model: str = MINIMAX_VOICE_CLONE_MODEL,
        clone_prompt: MinimaxClonePrompt | Mapping[str, object] | None = None,
        need_noise_reduction: bool = False,
        need_volume_normalization: bool = False,
        language_boost: str | None = None,
        aigc_watermark: bool = False,
        continuous_sound: bool = False,
    ) -> MinimaxVoiceCloneResult:
        """基于已上传 file_id 创建克隆音色，并返回试听音频链接。"""
        payload = self.build_clone_payload(
            file_id=file_id,
            voice_id=voice_id,
            text=text,
            model=model,
            clone_prompt=clone_prompt,
            need_noise_reduction=need_noise_reduction,
            need_volume_normalization=need_volume_normalization,
            language_boost=language_boost,
            aigc_watermark=aigc_watermark,
            continuous_sound=continuous_sound,
        )
        start = time.monotonic()
        response = self.transport.voice_clone(
            self.base_url,
            self.api_key,
            payload,
            self.timeout,
        )
        _raise_for_base_resp(response)
        elapsed_ms = round((time.monotonic() - start) * 1000, 3)
        raw_response = dict(response)
        raw_response["elapsed_ms"] = elapsed_ms
        return MinimaxVoiceCloneResult(
            voice_id=voice_id,
            file_id=file_id,
            demo_audio_url=self._extract_demo_audio_url(response),
            raw_response=raw_response,
        )

    def speak(
        self,
        text: str,
        *,
        path: str | Path,
        voice_id: str,
        prompt_path: str | Path | None = None,
        prompt_text: str | None = None,
        **clone_options: object,
    ) -> Speech:
        """使用快速复刻试听接口生成音频，兼容 ``tts.speak(...).save(...)``。"""
        result = self.clone_from_file(
            path,
            voice_id,
            text,
            prompt_path=prompt_path,
            prompt_text=prompt_text,
            **clone_options,
        )
        if not result.demo_audio_url:
            raise ProviderError("MiniMax voice clone response missing demo audio url")

        audio = self.transport.download_url(result.demo_audio_url, self.timeout)
        return Speech(
            audio,
            text=text,
            overrides=clone_options,
            metadata={
                "provider": self.__class__.__name__,
                "base_url": self.base_url,
                "model": clone_options.get("model", MINIMAX_VOICE_CLONE_MODEL),
                "voice_id": result.voice_id,
                "file_id": result.file_id,
                "demo_audio_url": result.demo_audio_url,
                "raw_response": result.raw_response,
                "audio_bytes": len(audio),
                "endpoint": "voice_clone",
            },
        )

    def clone_from_file(
        self,
        path: str | Path,
        voice_id: str,
        text: str,
        *,
        prompt_path: str | Path | None = None,
        prompt_text: str | None = None,
        **clone_options: object,
    ) -> MinimaxVoiceCloneResult:
        """上传复刻音频，可选上传示例音频，然后创建音色复刻试听。"""
        file_id = self.upload_clone_audio(path)
        if prompt_path is not None:
            if not prompt_text:
                raise ConfigurationError("MiniMax prompt_text is required when prompt_path is provided")
            prompt_file_id = self.upload_prompt_audio(prompt_path)
            clone_options["clone_prompt"] = MinimaxClonePrompt(
                prompt_audio=prompt_file_id,
                prompt_text=prompt_text,
            )
        return self.clone(file_id=file_id, voice_id=voice_id, text=text, **clone_options)

    def build_clone_payload(
        self,
        *,
        file_id: str | int,
        voice_id: str,
        text: str,
        model: str = MINIMAX_VOICE_CLONE_MODEL,
        clone_prompt: MinimaxClonePrompt | Mapping[str, object] | None = None,
        need_noise_reduction: bool = False,
        need_volume_normalization: bool = False,
        language_boost: str | None = None,
        aigc_watermark: bool = False,
        continuous_sound: bool = False,
    ) -> dict[str, object]:
        self._validate_voice_id(voice_id)
        if not str(file_id).strip():
            raise ConfigurationError("MiniMax file_id is required")
        if not text or not text.strip():
            raise ConfigurationError("MiniMax voice clone preview text is required")
        if len(text) > 1000:
            raise ConfigurationError("MiniMax voice clone preview text must be <= 1000 characters")
        if not model or not model.strip():
            raise ConfigurationError("MiniMax voice clone model is required")

        payload: dict[str, object] = {
            "file_id": file_id,
            "voice_id": voice_id,
            "text": text,
            "model": model,
            "need_noise_reduction": need_noise_reduction,
            "need_volume_normalization": need_volume_normalization,
        }
        if clone_prompt is not None:
            payload["clone_prompt"] = (
                clone_prompt.to_payload()
                if isinstance(clone_prompt, MinimaxClonePrompt)
                else dict(clone_prompt)
            )
        if language_boost is not None:
            payload["language_boost"] = language_boost
        if aigc_watermark:
            payload["aigc_watermark"] = aigc_watermark
        if continuous_sound:
            payload["continuous_sound"] = continuous_sound
        return payload

    def _validate_config(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("MiniMax voice clone api_key is required")
        if not self.base_url or not self.base_url.strip():
            raise ConfigurationError("MiniMax base_url is required")
        if self.timeout <= 0:
            raise ConfigurationError("MiniMax timeout must be greater than 0")

    def _validate_audio_file(self, path: str | Path) -> None:
        file_path = Path(path)
        if file_path.suffix.lower() not in self.SUPPORTED_SUFFIXES:
            raise ConfigurationError("MiniMax voice clone audio must be mp3, m4a, or wav")
        if file_path.exists() and file_path.stat().st_size > self.MAX_AUDIO_BYTES:
            raise ConfigurationError("MiniMax voice clone audio must be <= 20 MB")

    def _validate_voice_id(self, voice_id: str) -> None:
        if not self._VOICE_ID_PATTERN.fullmatch(voice_id):
            raise ConfigurationError(
                "MiniMax voice_id must be 8-256 chars, start with a letter, "
                "and end with a letter or digit"
            )

    @staticmethod
    def _extract_file_id(response: Mapping[str, object]) -> str | int:
        try:
            file_obj = response["file"]
            if isinstance(file_obj, Mapping):
                file_id = file_obj["file_id"]
            else:
                raise TypeError("file must be a mapping")
        except (KeyError, TypeError) as exc:
            raise ProviderError(f"MiniMax upload response missing file_id: {response}") from exc
        return file_id  # type: ignore[return-value]

    @staticmethod
    def _extract_demo_audio_url(response: Mapping[str, object]) -> str | None:
        for key in ("demo_audio", "demo_audio_url", "preview_audio", "audio_file"):
            value = response.get(key)
            if isinstance(value, str) and value:
                return value

        data = response.get("data")
        if isinstance(data, Mapping):
            for key in ("demo_audio", "demo_audio_url", "preview_audio", "audio_file"):
                value = data.get(key)
                if isinstance(value, str) and value:
                    return value
        return None
