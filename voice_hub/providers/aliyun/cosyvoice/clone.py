from __future__ import annotations

import hashlib
import os
import time
from pathlib import Path
from typing import Mapping

from ....errors import ConfigurationError, ProviderError
from .models import (
    ALIYUN_COSYVOICE_CLONE_MODEL,
    ALIYUN_COSYVOICE_HTTP_BASE_URL,
    ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL,
    AliyunCosyVoiceEnrollmentResult,
    AliyunCosyVoiceUploadedFile,
)
from .transport import AliyunCosyVoiceSDKTransport
from .tts import AliyunCosyVoiceTTS


class AliyunCosyVoiceClone:
    """阿里云 CosyVoice 复刻音色管理器。"""

    def __init__(
        self,
        api_key: str | None = None,
        target_model: str = ALIYUN_COSYVOICE_CLONE_MODEL,
        http_base_url: str = ALIYUN_COSYVOICE_HTTP_BASE_URL,
        websocket_base_url: str = ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL,
        transport: AliyunCosyVoiceSDKTransport | None = None,
        timeout: float = 120,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("DASHSCOPE_API_KEY", "")
        self.target_model = target_model
        self.http_base_url = http_base_url
        self.websocket_base_url = websocket_base_url
        self.transport = transport or AliyunCosyVoiceSDKTransport()
        self.timeout = timeout
        self._validate_config()

    def create_voice(
        self,
        *,
        audio_url: str,
        prefix: str | None = None,
        language_hints: list[str] | None = None,
        max_prompt_audio_length: float | None = None,
        enable_preprocess: bool | None = None,
    ) -> AliyunCosyVoiceEnrollmentResult:
        final_prefix = prefix or self.default_prefix(audio_url)
        voice_id, request_id = self.transport.create_voice(
            api_key=self.api_key,
            target_model=self.target_model,
            prefix=final_prefix,
            audio_url=audio_url,
            language_hints=language_hints,
            max_prompt_audio_length=max_prompt_audio_length,
            enable_preprocess=enable_preprocess,
            http_base_url=self.http_base_url,
            websocket_base_url=self.websocket_base_url,
            timeout=self.timeout,
        )
        return AliyunCosyVoiceEnrollmentResult(
            voice_id=voice_id,
            request_id=request_id,
            target_model=self.target_model,
            prefix=final_prefix,
            audio_url=audio_url,
            reused=False,
        )

    def get_or_create_voice(
        self,
        *,
        audio_url: str,
        prefix: str | None = None,
        language_hints: list[str] | None = None,
        max_prompt_audio_length: float | None = None,
        enable_preprocess: bool | None = None,
        reusable_statuses: tuple[str, ...] = ("OK", "DEPLOYING"),
    ) -> AliyunCosyVoiceEnrollmentResult:
        """优先复用已有音色，避免频繁 create_voice 消耗音色配额。"""
        final_prefix = prefix or self.default_prefix(audio_url)
        existing = self.find_reusable_voice(
            prefix=final_prefix,
            audio_url=audio_url,
            reusable_statuses=reusable_statuses,
        )
        if existing is not None:
            voice_id = str(existing["voice_id"])
            return AliyunCosyVoiceEnrollmentResult(
                voice_id=voice_id,
                request_id=_optional_str(existing.get("request_id")),
                target_model=_optional_str(existing.get("target_model")) or self.target_model,
                prefix=final_prefix,
                audio_url=audio_url,
                reused=True,
                status=_optional_str(existing.get("status")),
            )
        return self.create_voice(
            audio_url=audio_url,
            prefix=final_prefix,
            language_hints=language_hints,
            max_prompt_audio_length=max_prompt_audio_length,
            enable_preprocess=enable_preprocess,
        )

    def get_or_create_voice_from_file(
        self,
        file_path: str | Path,
        *,
        prefix: str | None = None,
        language_hints: list[str] | None = None,
        max_prompt_audio_length: float | None = None,
        enable_preprocess: bool | None = None,
        purpose: str = "fine-tune",
        reusable_statuses: tuple[str, ...] = ("OK", "DEPLOYING"),
    ) -> AliyunCosyVoiceEnrollmentResult:
        path = Path(file_path)
        final_prefix = prefix or self.default_prefix_for_file(path)
        existing = self.find_reusable_voice(
            prefix=final_prefix,
            reusable_statuses=reusable_statuses,
        )
        if existing is not None:
            voice_id = str(existing["voice_id"])
            return AliyunCosyVoiceEnrollmentResult(
                voice_id=voice_id,
                request_id=_optional_str(existing.get("request_id")),
                target_model=_optional_str(existing.get("target_model")) or self.target_model,
                prefix=final_prefix,
                audio_url=_optional_str(existing.get("resource_link")) or "",
                reused=True,
                status=_optional_str(existing.get("status")),
            )

        uploaded = self.upload_file(path, purpose=purpose)
        if not uploaded.url:
            raise ProviderError(f"Aliyun uploaded file missing url: {uploaded}")
        return self.create_voice(
            audio_url=uploaded.url,
            prefix=final_prefix,
            language_hints=language_hints,
            max_prompt_audio_length=max_prompt_audio_length,
            enable_preprocess=enable_preprocess,
        )

    def upload_file(
        self,
        file_path: str | Path,
        *,
        purpose: str = "fine-tune",
    ) -> AliyunCosyVoiceUploadedFile:
        response = self.transport.upload_file(
            api_key=self.api_key,
            file_path=file_path,
            purpose=purpose,
            http_base_url=self.http_base_url,
            timeout=self.timeout,
        )
        request_id = _optional_str(response.get("request_id"))
        uploaded = _first_uploaded_file(response)
        file_id = uploaded.get("file_id")
        name = uploaded.get("name")
        if not isinstance(file_id, str) or not isinstance(name, str):
            raise ProviderError(f"Aliyun file upload returned invalid response: {response}")

        file_info = self.transport.get_file(
            api_key=self.api_key,
            file_id=file_id,
            http_base_url=self.http_base_url,
            timeout=self.timeout,
        )
        data = file_info.get("data")
        if not isinstance(data, Mapping):
            raise ProviderError(f"Aliyun file query returned invalid response: {file_info}")
        return AliyunCosyVoiceUploadedFile(
            file_id=file_id,
            name=name,
            size=_optional_int(data.get("size")),
            md5=_optional_str(data.get("md5")),
            url=_optional_str(data.get("url")),
            request_id=request_id or _optional_str(file_info.get("request_id")),
        )

    def find_reusable_voice(
        self,
        *,
        prefix: str,
        audio_url: str | None = None,
        reusable_statuses: tuple[str, ...] = ("OK", "DEPLOYING"),
    ) -> Mapping[str, object] | None:
        for voice in self.list_voices(prefix=prefix, page_size=1000):
            voice_id = voice.get("voice_id")
            status = voice.get("status")
            if not isinstance(voice_id, str) or status not in reusable_statuses:
                continue
            target_model = voice.get("target_model")
            if isinstance(target_model, str) and target_model != self.target_model:
                continue
            resource_link = voice.get("resource_link")
            if audio_url and isinstance(resource_link, str) and resource_link != audio_url:
                continue
            return voice
        return None

    def default_prefix(self, audio_url: str) -> str:
        digest = hashlib.md5(f"{self.target_model}:{audio_url}".encode("utf-8")).hexdigest()
        return f"vh{digest[:8]}"

    def default_prefix_for_file(self, file_path: str | Path) -> str:
        path = Path(file_path)
        digest = hashlib.md5()
        digest.update(self.target_model.encode("utf-8"))
        digest.update(b":")
        digest.update(path.read_bytes())
        return f"vh{digest.hexdigest()[:8]}"

    def query_voice(self, voice_id: str) -> Mapping[str, object]:
        return self.transport.query_voice(
            api_key=self.api_key,
            voice_id=voice_id,
            http_base_url=self.http_base_url,
            websocket_base_url=self.websocket_base_url,
            timeout=self.timeout,
        )

    def list_voices(
        self,
        *,
        prefix: str | None = None,
        page_index: int = 0,
        page_size: int = 10,
    ) -> list[Mapping[str, object]]:
        return self.transport.list_voices(
            api_key=self.api_key,
            prefix=prefix,
            page_index=page_index,
            page_size=page_size,
            http_base_url=self.http_base_url,
            websocket_base_url=self.websocket_base_url,
            timeout=self.timeout,
        )

    def delete_voice(self, voice_id: str) -> str | None:
        return self.transport.delete_voice(
            api_key=self.api_key,
            voice_id=voice_id,
            http_base_url=self.http_base_url,
            websocket_base_url=self.websocket_base_url,
            timeout=self.timeout,
        )

    def wait_until_ready(
        self,
        voice_id: str,
        *,
        max_attempts: int = 30,
        poll_interval: float = 10,
    ) -> Mapping[str, object]:
        for _ in range(max_attempts):
            info = self.query_voice(voice_id)
            status = info.get("status")
            if status == "OK":
                return info
            if status == "UNDEPLOYED":
                raise ProviderError(f"Aliyun CosyVoice voice processing failed: {info}")
            time.sleep(poll_interval)
        raise ProviderError("Aliyun CosyVoice voice polling timed out")

    def tts(self, voice_id: str, **kwargs: object) -> AliyunCosyVoiceTTS:
        return AliyunCosyVoiceTTS(
            api_key=self.api_key,
            voice=voice_id,
            model=self.target_model,
            http_base_url=self.http_base_url,
            websocket_base_url=self.websocket_base_url,
            transport=self.transport,
            timeout=self.timeout,
            **kwargs,
        )

    def tts_from_voice(
        self,
        result: AliyunCosyVoiceEnrollmentResult,
        *,
        wait: bool = True,
        max_attempts: int = 30,
        poll_interval: float = 10,
        **kwargs: object,
    ) -> AliyunCosyVoiceTTS:
        if wait:
            self.wait_until_ready(
                result.voice_id,
                max_attempts=max_attempts,
                poll_interval=poll_interval,
            )
        tts = self.tts(result.voice_id, **kwargs)
        tts.voice_result = result
        return tts

    def _validate_config(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("Aliyun CosyVoice api_key is required")
        if not self.target_model or not self.target_model.strip():
            raise ConfigurationError("Aliyun CosyVoice target_model is required")
        if self.timeout <= 0:
            raise ConfigurationError("Aliyun CosyVoice timeout must be greater than 0")


def _optional_str(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _optional_int(value: object) -> int | None:
    return value if isinstance(value, int) else None


def _first_uploaded_file(response: Mapping[str, object]) -> Mapping[str, object]:
    data = response.get("data")
    if not isinstance(data, Mapping):
        raise ProviderError(f"Aliyun file upload missing data: {response}")
    uploaded_files = data.get("uploaded_files")
    if not isinstance(uploaded_files, list) or not uploaded_files:
        raise ProviderError(f"Aliyun file upload returned no uploaded files: {response}")
    first = uploaded_files[0]
    if not isinstance(first, Mapping):
        raise ProviderError(f"Aliyun file upload returned invalid file item: {response}")
    return first
