from __future__ import annotations

import time
from pathlib import Path
from typing import Iterable, Mapping

from ...errors import ConfigurationError
from ...sample import VoiceSample
from ...speech import Speech
from ..base import BaseTTS
from .models import (
    MIMO_BASE_URL,
    MIMO_TTS_MODEL,
    MIMO_VOICE_CLONE_MODEL,
    MIMO_VOICE_DESIGN_MODEL,
    MimoRequest,
)
from .parser import MimoResponseParser
from .payload import MimoPayloadBuilder
from .transport import MimoHTTPTransport


class MimoTTS(BaseTTS):
    """小米 MiMo-V2.5-TTS 系列 provider。

    参数:
        api_key: 小米 MiMo 控制台获取的 API Key，请求时会作为 ``api-key`` 请求头发送。
        voice: 内置音色 ID，仅 ``mimo-v2.5-tts`` 使用。
        style: 自然语言风格指令，会放入 ``role=user`` 消息。
        format: 输出音频格式。流式调用默认覆盖为 ``pcm16``。
        model: MiMo TTS 模型 ID。
        base_url: MiMo OpenAI-compatible API 地址。
        transport: 自定义 HTTP 传输层，主要用于测试、代理或替换标准库请求实现。
        timeout: 单次 HTTP 请求超时时间，单位秒。
        voice_design_prompt: 文本设计音色描述，仅文本设计音色模型必填。
        voice_sample: 克隆音色参考音频，仅克隆音色模型必填。
    """

    def __init__(
        self,
        api_key: str,
        voice: str = "mimo_default",
        style: str | None = None,
        format: str = "wav",
        model: str = MIMO_TTS_MODEL,
        base_url: str = MIMO_BASE_URL,
        transport: MimoHTTPTransport | None = None,
        timeout: float = 60,
        voice_design_prompt: str | None = None,
        voice_sample: VoiceSample | str | None = None,
    ) -> None:
        self.api_key = api_key
        self.voice = voice
        self.style = style
        self.format = format
        self.model = model
        self.base_url = base_url
        self.transport = transport or MimoHTTPTransport()
        self.timeout = timeout
        self.voice_design_prompt = voice_design_prompt
        self.voice_sample = self._normalize_sample(voice_sample)
        self._parser = MimoResponseParser()
        self._validate_config()

    def speak(self, text: str, **overrides: object) -> Speech:
        """合成语音并返回音频结果。"""
        request = self.build_request(text, stream=False, **overrides)
        start = time.monotonic()
        response = self.transport.post(
            self.base_url,
            self.api_key,
            request.to_payload(),
            self.timeout,
        )
        audio = self._parser.decode_message_audio(response)
        elapsed_ms = round((time.monotonic() - start) * 1000, 3)
        return Speech(
            audio,
            text=text,
            overrides=overrides,
            metadata={
                "provider": self.__class__.__name__,
                "base_url": self.base_url,
                "model": request.model,
                "elapsed_ms": elapsed_ms,
                "audio_bytes": len(audio),
                "payload": _redact_payload(request.to_payload()),
            },
        )

    @classmethod
    def designed(
        cls,
        api_key: str,
        prompt: str = "",
        style: str | None = None,
        format: str = "wav",
        **kwargs: object,
    ) -> "MimoTTS":
        """创建文本设计音色 provider。"""
        return cls(
            api_key=api_key,
            style=style,
            format=format,
            model=MIMO_VOICE_DESIGN_MODEL,
            voice_design_prompt=prompt,
            **kwargs,
        )

    @classmethod
    def cloned(
        cls,
        api_key: str,
        sample: VoiceSample | str | None = None,
        style: str | None = None,
        format: str = "wav",
        **kwargs: object,
    ) -> "MimoTTS":
        """创建克隆音色 provider。"""
        return cls(
            api_key=api_key,
            style=style,
            format=format,
            model=MIMO_VOICE_CLONE_MODEL,
            voice_sample=sample,
            **kwargs,
        )

    def build_payload(self, text: str, stream: bool = False, **overrides: object) -> dict[str, object]:
        """构造最终 MiMo 请求体，不发送网络请求。"""
        return self.build_request(text, stream=stream, **overrides).to_payload()

    def build_request(self, text: str, stream: bool = False, **overrides: object) -> MimoRequest:
        """构造最终 MiMo 请求对象，不发送网络请求。"""
        return self._payload_builder().build_request(
            text,
            stream=stream,
            overrides=overrides,
        )

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
        """流式合成语音并返回音频分片。"""
        return self.stream_synthesize(text, **overrides)

    def stream_synthesize(self, text: str, **overrides: object) -> Iterable[bytes]:
        stream_overrides = dict(overrides)
        stream_overrides.setdefault("format", "pcm16")

        request = self.build_request(text, stream=True, **stream_overrides)
        events = self.transport.stream(
            self.base_url,
            self.api_key,
            request.to_payload(),
            self.timeout,
        )
        return self._parser.iter_audio_chunks(events)

    @staticmethod
    def _normalize_sample(sample: VoiceSample | str | None) -> VoiceSample | None:
        if sample is None or isinstance(sample, VoiceSample):
            return sample
        return VoiceSample(sample)

    def _payload_builder(self) -> MimoPayloadBuilder:
        return MimoPayloadBuilder(
            model=self.model,
            voice=self.voice,
            style=self.style,
            format=self.format,
            voice_design_prompt=self.voice_design_prompt,
            voice_sample=self.voice_sample,
        )

    def _validate_config(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("MiMo api_key is required")
        if not self.base_url or not self.base_url.strip():
            raise ConfigurationError("MiMo base_url is required")
        if self.timeout <= 0:
            raise ConfigurationError("MiMo timeout must be greater than 0")
        if self.model == MIMO_VOICE_DESIGN_MODEL and not self.voice_design_prompt:
            raise ConfigurationError("voice design prompt is required")
        if self.model == MIMO_VOICE_CLONE_MODEL and not self.voice_sample:
            raise ConfigurationError("voice clone sample is required")


def _redact_payload(payload: Mapping[str, object]) -> dict[str, object]:
    sanitized = dict(payload)
    audio = sanitized.get("audio")
    if isinstance(audio, Mapping):
        sanitized_audio = dict(audio)
        voice = sanitized_audio.get("voice")
        if isinstance(voice, str) and voice.startswith("data:"):
            sanitized_audio["voice"] = "<redacted voice sample data URI>"
        sanitized["audio"] = sanitized_audio
    return sanitized
