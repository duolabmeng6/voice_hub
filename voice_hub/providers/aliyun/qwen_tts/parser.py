from __future__ import annotations

import base64
import binascii
from typing import Any, Iterable, Iterator, Mapping

from ....errors import ProviderError


class AliyunResponseParser:
    """解析阿里云 Qwen TTS 非流式和 SSE 响应。"""

    @staticmethod
    def audio_url(response: Mapping[str, Any]) -> str:
        _raise_for_error(response)
        try:
            url = response["output"]["audio"]["url"]
        except (KeyError, TypeError) as exc:
            summary = _summarize_response(response)
            raise ProviderError(f"Aliyun TTS response missing audio url: {summary}") from exc
        if not isinstance(url, str) or not url:
            summary = _summarize_response(response)
            raise ProviderError(f"Aliyun TTS response contains invalid audio url: {summary}")
        return url

    @staticmethod
    def iter_audio_chunks(events: Iterable[Mapping[str, Any]]) -> Iterator[bytes]:
        for event in events:
            _raise_for_error(event)
            try:
                audio = event.get("output", {}).get("audio", {})
                audio_data = audio.get("data")
            except AttributeError as exc:
                summary = _summarize_response(event)
                raise ProviderError(f"Aliyun TTS stream chunk missing audio data: {summary}") from exc

            if audio_data is None:
                continue
            try:
                yield _decode_audio_data(audio_data)
            except (binascii.Error, ValueError) as exc:
                summary = _summarize_response(event)
                raise ProviderError(f"Aliyun TTS stream chunk contains invalid audio data: {summary}") from exc


def _decode_audio_data(audio_data: object) -> bytes:
    if not isinstance(audio_data, str):
        raise TypeError("audio data must be a base64 string")
    return base64.b64decode(audio_data, validate=True)


def _raise_for_error(response: Mapping[str, Any]) -> None:
    code = response.get("code")
    message = response.get("message")
    if code:
        raise ProviderError(f"Aliyun TTS API error: code={code}, message={message}")


def _summarize_response(value: Mapping[str, Any]) -> dict[str, object]:
    """保留调试线索，同时避免把大段音频 base64 打进异常。"""
    summary: dict[str, object] = {}
    for key in ("request_id", "code", "message", "usage"):
        if key in value:
            summary[key] = value[key]

    output = value.get("output")
    if isinstance(output, Mapping):
        summary["output_keys"] = sorted(str(key) for key in output.keys())
        audio = output.get("audio")
        if isinstance(audio, Mapping):
            summary["audio_keys"] = sorted(str(key) for key in audio.keys())
        finish_reason = output.get("finish_reason")
        if finish_reason is not None:
            summary["finish_reason"] = finish_reason

    return summary or {"keys": sorted(str(key) for key in value.keys())}
