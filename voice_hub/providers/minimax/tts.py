from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol

from ...errors import ConfigurationError
from ...sample import VoiceSample
from ...speech import Speech
from ..base import BaseTTS
from .api import MinimaxAPI
from .clone import MinimaxVoiceClone
from .models import (
    MINIMAX_BASE_URL,
    MINIMAX_T2A_MODEL,
    MinimaxRequest,
    MinimaxVoice,
)
from .parser import MinimaxResponseParser
from .payload import MinimaxPayloadBuilder


class MinimaxAPIClient(Protocol):
    def t2a_v2(self, data: Mapping[str, object]) -> Mapping[str, Any]: ...

    def t2a_v2_stream(self, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]: ...


class MinimaxTTS(BaseTTS):
    """MiniMax 同步 T2A HTTP provider。

    参数:
        api_key: MiniMax API Key；未传入时读取环境变量 ``MINIMAX_KEY``。
        voice: 系统音色、复刻音色或文生音色 ID。
        model: MiniMax T2A 模型 ID，默认 ``speech-2.8-hd``。
        format: 输出音频格式，支持 ``mp3``、``pcm``、``flac``，非流式也支持 ``wav``。
        base_url: MiniMax API 根地址，默认 ``https://api.minimaxi.com/v1``。
        api: 自定义 MiniMax API 客户端，主要用于测试、代理或替换请求实现。
        timeout: 单次 HTTP 请求超时时间，单位秒。
    """

    def __init__(
        self,
        api_key: str | None = None,
        voice: str = MinimaxVoice.MALE_QN_QINGSE,
        model: str = MINIMAX_T2A_MODEL,
        format: str = "mp3",
        base_url: str = MINIMAX_BASE_URL,
        api: MinimaxAPIClient | None = None,
        timeout: float = 60,
        speed: float = 1,
        vol: float = 1,
        pitch: int = 0,
        emotion: str | None = None,
        text_normalization: bool = False,
        latex_read: bool = False,
        sample_rate: int = 32000,
        bitrate: int = 128000,
        channel: int = 1,
        force_cbr: bool = False,
        pronunciation_dict: Mapping[str, object] | None = None,
        timbre_weights: list[Mapping[str, object]] | None = None,
        language_boost: str | None = None,
        voice_modify: Mapping[str, object] | None = None,
        subtitle_enable: bool = False,
        output_format: str = "hex",
        aigc_watermark: bool = False,
        stream_options: Mapping[str, object] | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("MINIMAX_KEY", "")
        self.voice = voice
        self.model = model
        self.format = format
        self.base_url = base_url
        self.api = api or MinimaxAPI(api_key=self.api_key, base_url=self.base_url, timeout=timeout)
        self.timeout = timeout
        self.speed = speed
        self.vol = vol
        self.pitch = pitch
        self.emotion = emotion
        self.text_normalization = text_normalization
        self.latex_read = latex_read
        self.sample_rate = sample_rate
        self.bitrate = bitrate
        self.channel = channel
        self.force_cbr = force_cbr
        self.pronunciation_dict = pronunciation_dict
        self.timbre_weights = timbre_weights
        self.language_boost = language_boost
        self.voice_modify = voice_modify
        self.subtitle_enable = subtitle_enable
        self.output_format = output_format
        self.aigc_watermark = aigc_watermark
        self.stream_options = stream_options
        self._parser = MinimaxResponseParser()
        self._validate_config()

    def speak(self, text: str, **overrides: object) -> Speech:
        """合成语音并返回音频结果。"""
        request = self.build_request(text, stream=False, **overrides)
        data = request.to_payload()
        start = time.monotonic()
        response = self.api.t2a_v2(data)
        audio = self._parser.decode_audio(response)
        elapsed_ms = round((time.monotonic() - start) * 1000, 3)
        return Speech(
            audio,
            text=text,
            overrides=overrides,
            metadata={
                "provider": self.__class__.__name__,
                "base_url": self.base_url,
                "model": request.model,
                "trace_id": response.get("trace_id"),
                "extra_info": response.get("extra_info"),
                "elapsed_ms": elapsed_ms,
                "audio_bytes": len(audio),
                "payload": data,
            },
        )

    @classmethod
    def cloned(
        cls,
        api_key: str | None = None,
        sample: VoiceSample | str | Path | None = None,
        voice_id: str | None = None,
        **kwargs: object,
    ) -> MinimaxVoiceClone:
        """创建 MiniMax 快速复刻试听 provider，不调用正式 T2A 合成接口。"""
        return MinimaxVoiceClone(
            api_key=api_key,
            sample=sample,
            voice_id=voice_id,
            **kwargs,
        )

    def build_payload(self, text: str, stream: bool = False, **overrides: object) -> dict[str, object]:
        """构造最终 MiniMax 请求体，不发送网络请求。"""
        return self.build_request(text, stream=stream, **overrides).to_payload()

    def build_request(self, text: str, stream: bool = False, **overrides: object) -> MinimaxRequest:
        """构造最终 MiniMax 请求对象，不发送网络请求。"""
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
        request = self.build_request(text, stream=True, **overrides)
        events = self.api.t2a_v2_stream(request.to_payload())
        return self._parser.iter_audio_chunks(events)

    def _payload_builder(self) -> MinimaxPayloadBuilder:
        return MinimaxPayloadBuilder(
            model=self.model,
            voice=self.voice,
            speed=self.speed,
            vol=self.vol,
            pitch=self.pitch,
            emotion=self.emotion,
            text_normalization=self.text_normalization,
            latex_read=self.latex_read,
            sample_rate=self.sample_rate,
            bitrate=self.bitrate,
            format=self.format,
            channel=self.channel,
            force_cbr=self.force_cbr,
            pronunciation_dict=self.pronunciation_dict,
            timbre_weights=self.timbre_weights,
            language_boost=self.language_boost,
            voice_modify=self.voice_modify,
            subtitle_enable=self.subtitle_enable,
            output_format=self.output_format,
            aigc_watermark=self.aigc_watermark,
            stream_options=self.stream_options,
        )

    def _validate_config(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("MiniMax api_key is required")
        if not self.base_url or not self.base_url.strip():
            raise ConfigurationError("MiniMax base_url is required")
        if self.timeout <= 0:
            raise ConfigurationError("MiniMax timeout must be greater than 0")
        self.build_payload("config check")
