from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol

from ....errors import ConfigurationError
from ....speech import Speech
from ...base import BaseTTS
from .api import AliyunQwenTTSAPI
from .models import ALIYUN_BASE_URL, ALIYUN_QWEN_TTS_MODEL, AliyunRequest
from .parser import AliyunResponseParser
from .payload import AliyunPayloadBuilder
from .voices import AliyunVoice


class AliyunQwenTTSAPIClient(Protocol):
    def generation(self, data: Mapping[str, object]) -> Mapping[str, Any]: ...

    def generation_stream(self, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]: ...

    def download_url(self, url: str) -> bytes: ...


class AliyunTTS(BaseTTS):
    """阿里云百炼 Qwen TTS 系统音色 provider。

    参数:
        api_key: DashScope API Key；未传入时读取环境变量 ``DASHSCOPE_API_KEY``。
        voice: 官方系统音色 ID，默认 ``Cherry``。
        model: Qwen TTS 模型 ID，默认 ``qwen3-tts-instruct-flash``。
        language_type: 文本语言类型，例如 ``Chinese``、``English`` 或 ``Auto``。
        instructions: 指令控制，仅 ``qwen3-tts-instruct-flash`` 支持。
        optimize_instructions: 是否让模型优化指令表达。
        base_url: DashScope generation endpoint；默认北京地域。
        api: 自定义阿里云 Qwen TTS API 客户端，主要用于测试、代理或替换请求实现。
        timeout: 单次 HTTP 请求和音频下载超时时间，单位秒。
    """

    def __init__(
        self,
        api_key: str | None = None,
        voice: str = AliyunVoice.CHERRY,
        model: str = ALIYUN_QWEN_TTS_MODEL,
        language_type: str = "Chinese",
        instructions: str | None = None,
        optimize_instructions: bool = False,
        base_url: str = ALIYUN_BASE_URL,
        api: AliyunQwenTTSAPIClient | None = None,
        timeout: float = 60,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("DASHSCOPE_API_KEY", "")
        self.voice = voice
        self.model = model
        self.language_type = language_type
        self.instructions = instructions
        self.optimize_instructions = optimize_instructions
        self.base_url = base_url
        self.api = api or AliyunQwenTTSAPI(api_key=self.api_key, base_url=self.base_url, timeout=timeout)
        self.timeout = timeout
        self._parser = AliyunResponseParser()
        self._validate_config()

    def speak(self, text: str, **overrides: object) -> Speech:
        """合成语音、下载返回的音频 URL，并返回音频结果。"""
        request = self.build_request(text, **overrides)
        data = request.to_payload()
        start = time.monotonic()
        response = self.api.generation(data)
        audio_url = self._parser.audio_url(response)
        audio = self.api.download_url(audio_url)
        elapsed_ms = round((time.monotonic() - start) * 1000, 3)
        return Speech(
            audio,
            text=text,
            overrides=overrides,
            metadata={
                "provider": self.__class__.__name__,
                "base_url": self.base_url,
                "model": request.model,
                "request_id": response.get("request_id"),
                "usage": response.get("usage"),
                "audio_url": audio_url,
                "elapsed_ms": elapsed_ms,
                "audio_bytes": len(audio),
                "payload": data,
            },
        )

    def build_payload(self, text: str, **overrides: object) -> dict[str, object]:
        """构造最终阿里云请求体，不发送网络请求。"""
        return self.build_request(text, **overrides).to_payload()

    def build_request(self, text: str, **overrides: object) -> AliyunRequest:
        """构造最终阿里云请求对象，不发送网络请求。"""
        return self._payload_builder().build_request(text, overrides=overrides)

    def synthesize(self, text: str, **overrides: object) -> bytes:
        """合成语音并返回字节。"""
        return self.speak(text, **overrides).bytes()

    def bytes(self, text: str, **overrides: object) -> bytes:
        """合成语音并返回完整音频字节。"""
        return self.synthesize(text, **overrides)

    def to_file(self, text: str, path: str | Path, **overrides: object) -> str:
        """合成语音并保存到文件。"""
        return self.speak(text, **overrides).save(path)

    def stream(self, text: str, **overrides: object) -> Iterable[bytes]:
        """使用 DashScope SSE 流式合成，返回 Base64 解码后的音频分片。"""
        request = self.build_request(text, **overrides)
        events = self.api.generation_stream(request.to_payload())
        return self._parser.iter_audio_chunks(events)

    def stream_synthesize(self, text: str, **overrides: object) -> Iterable[bytes]:
        return self.stream(text, **overrides)

    def _payload_builder(self) -> AliyunPayloadBuilder:
        return AliyunPayloadBuilder(
            model=self.model,
            voice=self.voice,
            language_type=self.language_type,
            instructions=self.instructions,
            optimize_instructions=self.optimize_instructions,
        )

    def _validate_config(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("Aliyun api_key is required")
        if not self.base_url or not self.base_url.strip():
            raise ConfigurationError("Aliyun base_url is required")
        if self.timeout <= 0:
            raise ConfigurationError("Aliyun timeout must be greater than 0")
        self.build_payload("config check")
