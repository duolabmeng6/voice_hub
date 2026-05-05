from __future__ import annotations

import json
from typing import Any, Iterable, Mapping

import requests

from ....errors import ProviderError
from .models import ALIYUN_QWEN_TTS_GENERATION_PATH


class AliyunQwenTTSBaseAPI:
    """Aliyun Qwen TTS HTTP API base client."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float = 60,
        session: requests.Session | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = _normalize_base_url(base_url)
        self.timeout = timeout
        self.session = session or requests.Session()
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def post(self, path: str, data: Mapping[str, object]) -> Mapping[str, Any]:
        try:
            response = self.session.request(
                "POST",
                self._url(path),
                headers=self.headers,
                json=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("Aliyun TTS API request failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("Aliyun TTS API request timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"Aliyun TTS API request failed: {exc}") from exc
        return _json_mapping(response, "Aliyun TTS API request failed")

    def stream_post(
        self,
        path: str,
        data: Mapping[str, object],
        headers: Mapping[str, str] | None = None,
    ) -> Iterable[Mapping[str, Any]]:
        request_headers = dict(self.headers)
        if headers:
            request_headers.update(headers)
        try:
            response = self.session.request(
                "POST",
                self._url(path),
                headers=request_headers,
                json=data,
                timeout=self.timeout,
                stream=True,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("Aliyun TTS API stream failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("Aliyun TTS API stream timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"Aliyun TTS API stream failed: {exc}") from exc
        return _iter_sse_events(response)

    def get_bytes_url(self, url: str) -> bytes:
        try:
            response = self.session.request("GET", url, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("Aliyun TTS audio download failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("Aliyun TTS audio download timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"Aliyun TTS audio download failed: {exc}") from exc
        return response.content

    def _url(self, path: str) -> str:
        if path.startswith("/"):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/{path}"


class AliyunQwenTTSAPI(AliyunQwenTTSBaseAPI):
    """Aliyun Qwen TTS business API methods."""

    def generation(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(ALIYUN_QWEN_TTS_GENERATION_PATH, data=dict(data))

    def generation_stream(self, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        return self.stream_post(
            ALIYUN_QWEN_TTS_GENERATION_PATH,
            data=dict(data),
            headers={"X-DashScope-SSE": "enable"},
        )

    def download_url(self, url: str) -> bytes:
        return self.get_bytes_url(url)


def _iter_sse_events(response: requests.Response) -> Iterable[Mapping[str, Any]]:
    with response:
        try:
            for raw_line in response.iter_lines(decode_unicode=False):
                event = _parse_sse_line(raw_line)
                if event is not None:
                    yield event
        except requests.exceptions.Timeout as exc:
            raise ProviderError("Aliyun TTS API stream timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"Aliyun TTS API stream failed: {exc}") from exc


def _parse_sse_line(raw_line: bytes) -> Mapping[str, Any] | None:
    line = raw_line.decode("utf-8", errors="replace").strip()
    if not line or not line.startswith("data:"):
        return None

    data = line.removeprefix("data:").strip()
    if data == "[DONE]":
        return None
    try:
        event = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ProviderError("Aliyun TTS API stream returned invalid JSON") from exc
    if not isinstance(event, Mapping):
        raise ProviderError("Aliyun TTS API stream returned invalid JSON")
    return event


def _json_mapping(response: requests.Response, prefix: str) -> Mapping[str, Any]:
    try:
        body = response.json()
    except ValueError as exc:
        raise ProviderError(f"{prefix}: invalid JSON response") from exc
    if not isinstance(body, Mapping):
        raise ProviderError(f"{prefix}: invalid JSON response")
    return body


def _normalize_base_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith(ALIYUN_QWEN_TTS_GENERATION_PATH):
        return normalized[: -len(ALIYUN_QWEN_TTS_GENERATION_PATH)]
    return normalized


def _http_error_message(prefix: str, exc: requests.exceptions.HTTPError) -> str:
    response = exc.response
    if response is None:
        return f"{prefix}: {exc}"
    return f"{prefix}: HTTP {response.status_code}: {response.text[:2000]}"
