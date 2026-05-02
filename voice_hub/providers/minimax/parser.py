from __future__ import annotations

import binascii
from typing import Any, Iterable, Iterator, Mapping

from ...errors import ProviderError


class MinimaxResponseParser:
    """解析 MiniMax T2A 非流式和流式响应。"""

    @staticmethod
    def decode_audio(response: Mapping[str, Any]) -> bytes:
        _raise_for_base_resp(response)
        try:
            data = response["data"]
            audio = data["audio"]
            return _decode_hex_audio(audio)
        except (KeyError, TypeError) as exc:
            summary = _summarize_response(response)
            raise ProviderError(f"MiniMax API response missing audio data: {summary}") from exc
        except (binascii.Error, ValueError) as exc:
            summary = _summarize_response(response)
            raise ProviderError(f"MiniMax API response contains invalid audio data: {summary}") from exc

    @staticmethod
    def iter_audio_chunks(events: Iterable[Mapping[str, Any]]) -> Iterator[bytes]:
        for event in events:
            _raise_for_base_resp(event)
            try:
                data = event.get("data")
                if not data:
                    continue
                audio = data.get("audio")
                if not audio:
                    continue
                yield _decode_hex_audio(audio)
            except AttributeError as exc:
                summary = _summarize_response(event)
                raise ProviderError(f"MiniMax stream chunk missing audio data: {summary}") from exc
            except (binascii.Error, ValueError) as exc:
                summary = _summarize_response(event)
                raise ProviderError(f"MiniMax stream chunk contains invalid audio data: {summary}") from exc


def _decode_hex_audio(audio: object) -> bytes:
    if not isinstance(audio, str):
        raise TypeError("audio data must be a hex string")
    return bytes.fromhex(audio)


def _raise_for_base_resp(response: Mapping[str, Any]) -> None:
    base_resp = response.get("base_resp")
    if not isinstance(base_resp, Mapping):
        return

    status_code = base_resp.get("status_code")
    if status_code in (None, 0):
        return
    status_msg = base_resp.get("status_msg", "")
    trace_id = response.get("trace_id", "")
    raise ProviderError(
        f"MiniMax API returned status_code={status_code}, "
        f"status_msg={status_msg}, trace_id={trace_id}"
    )


def _summarize_response(value: Mapping[str, Any]) -> dict[str, object]:
    """保留调试线索，同时避免把大段音频 hex 打进异常。"""
    summary: dict[str, object] = {}
    for key in ("trace_id", "base_resp", "extra_info"):
        if key in value:
            summary[key] = value[key]

    data = value.get("data")
    if isinstance(data, Mapping):
        summary["data_keys"] = sorted(str(key) for key in data.keys())
        status = data.get("status")
        if status is not None:
            summary["data_status"] = status
    return summary or {"keys": sorted(str(key) for key in value.keys())}
