from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Iterable, Mapping, Protocol

from ...errors import ConfigurationError
from ...speech import Speech
from ..base import BaseTTS
from .api import GLMAPI
from .models import GLM_BASE_URL, GLM_TTS_MODEL, GLMRequest, GLMVoice
from .payload import GLMPayloadBuilder


class GLMAPIClient(Protocol):
    def speech(self, data: Mapping[str, object]) -> bytes: ...


class GLMTTS(BaseTTS):
    """智谱 GLM 语音合成 provider。

    参数:
        api_key: 智谱 API Key；未传入时读取环境变量 ``ZHIPUAI_API_KEY``。
        voice: 系统音色 ID，默认 ``female``；也可以传入克隆后的 voice_id。
        model: GLM TTS 模型 ID，默认 ``glm-tts``。
        response_format: 输出音频格式，默认 ``wav``。
        base_url: 智谱语音合成 API 地址。
        api: 自定义 GLM API 客户端，主要用于测试、代理或替换请求实现。
        timeout: 单次请求超时时间，单位秒。
    """

    def __init__(
        self,
        api_key: str | None = None,
        voice: str = GLMVoice.FEMALE,
        model: str = GLM_TTS_MODEL,
        response_format: str = "wav",
        speed: float = 1.0,
        volume: float = 1.0,
        encode_format: str | None = None,
        watermark_enabled: bool | None = None,
        base_url: str = GLM_BASE_URL,
        api: GLMAPIClient | None = None,
        timeout: float = 60,
        sensitive_word_check: object | None = None,
        request_id: str | None = None,
        user_id: str | None = None,
        extra_body: Mapping[str, object] | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("ZHIPUAI_API_KEY", "")
        self.voice = voice
        self.model = model
        self.response_format = response_format
        self.speed = speed
        self.volume = volume
        self.encode_format = encode_format
        self.watermark_enabled = watermark_enabled
        self.base_url = base_url
        self.api = api or GLMAPI(api_key=self.api_key, base_url=self.base_url, timeout=timeout)
        self.timeout = timeout
        self.sensitive_word_check = sensitive_word_check
        self.request_id = request_id
        self.user_id = user_id
        self.extra_body = extra_body
        self._validate_config()

    def speak(self, text: str, **overrides: object) -> Speech:
        request = self.build_request(text, **overrides)
        data = request.to_payload()
        start = time.monotonic()
        audio = self.api.speech(data)
        elapsed_ms = round((time.monotonic() - start) * 1000, 3)
        return Speech(
            audio,
            text=text,
            overrides=overrides,
            metadata={
                "provider": self.__class__.__name__,
                "base_url": self.base_url,
                "model": request.model,
                "voice": request.voice,
                "response_format": request.response_format,
                "request_id": request.request_id,
                "elapsed_ms": elapsed_ms,
                "audio_bytes": len(audio),
                "payload": data,
            },
        )

    def build_payload(self, text: str, **overrides: object) -> dict[str, object]:
        """构造最终 GLM TTS 请求体，不发送网络请求。"""
        return self.build_request(text, **overrides).to_payload()

    def build_request(self, text: str, **overrides: object) -> GLMRequest:
        """构造最终 GLM TTS 请求对象，不发送网络请求。"""
        return self._payload_builder().build_request(text, overrides=overrides)

    def synthesize(self, text: str, **overrides: object) -> bytes:
        return self.speak(text, **overrides).bytes()

    def bytes(self, text: str, **overrides: object) -> bytes:
        return self.synthesize(text, **overrides)

    def to_file(self, text: str, path: str | Path, **overrides: object) -> str:
        return self.speak(text, **overrides).save(path)

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
        return self.speak(text, **overrides).stream()

    def _payload_builder(self) -> GLMPayloadBuilder:
        return GLMPayloadBuilder(
            model=self.model,
            voice=self.voice,
            response_format=self.response_format,
            speed=self.speed,
            volume=self.volume,
            encode_format=self.encode_format,
            watermark_enabled=self.watermark_enabled,
            sensitive_word_check=self.sensitive_word_check,
            request_id=self.request_id,
            user_id=self.user_id,
            extra_body=self.extra_body,
        )

    def _validate_config(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("GLM api_key is required")
        if not self.base_url or not self.base_url.strip():
            raise ConfigurationError("GLM base_url is required")
        if self.timeout <= 0:
            raise ConfigurationError("GLM timeout must be greater than 0")
        self.build_payload("config check")
