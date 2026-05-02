from __future__ import annotations

import base64
import binascii
from typing import Any, Iterable, Iterator, Mapping

from ...errors import ProviderError


class MimoResponseParser:
    """解析 MiMo 非流式和流式响应。"""

    @staticmethod
    def decode_message_audio(response: Mapping[str, Any]) -> bytes:
        try:
            audio_data = response["choices"][0]["message"]["audio"]["data"]
            return _decode_audio_data(audio_data)
        except (KeyError, IndexError, TypeError) as exc:
            summary = _summarize_response(response)
            raise ProviderError(f"MiMo API response missing audio data: {summary}") from exc
        except (binascii.Error, ValueError) as exc:
            summary = _summarize_response(response)
            raise ProviderError(f"MiMo API response contains invalid audio data: {summary}") from exc

    @staticmethod
    def iter_audio_chunks(events: Iterable[Mapping[str, Any]]) -> Iterator[bytes]:
        for event in events:
            try:
                choices = event.get("choices", [])
                if not choices:
                    continue
                audio = choices[0].get("delta", {}).get("audio")
                if not audio:
                    continue
                yield _decode_audio_data(audio["data"])
            except (KeyError, TypeError) as exc:
                summary = _summarize_response(event)
                raise ProviderError(f"MiMo stream chunk missing audio data: {summary}") from exc
            except (binascii.Error, ValueError) as exc:
                summary = _summarize_response(event)
                raise ProviderError(f"MiMo stream chunk contains invalid audio data: {summary}") from exc


def _decode_audio_data(audio_data: object) -> bytes:
    if not isinstance(audio_data, str):
        raise TypeError("audio data must be a base64 string")
    return base64.b64decode(audio_data, validate=True)


def _summarize_response(value: Mapping[str, Any]) -> dict[str, object]:
    """保留调试线索，同时避免把大段音频 base64 打进异常。"""
    summary: dict[str, object] = {}
    for key in ("id", "object", "created", "model", "error"):
        if key in value:
            summary[key] = value[key]

    choices = value.get("choices")
    if isinstance(choices, list):
        summary["choices_count"] = len(choices)
        if choices:
            first = choices[0]
            if isinstance(first, Mapping):
                summary["first_choice_keys"] = sorted(str(key) for key in first.keys())
    return summary or {"keys": sorted(str(key) for key in value.keys())}
