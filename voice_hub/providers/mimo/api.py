from __future__ import annotations

import json
from typing import Any, Iterable, Mapping

import requests

from ...errors import ProviderError
from .models import MIMO_CHAT_COMPLETIONS_PATH


class MimoBaseAPI:
    """MiMo HTTP API base client."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float = 60,
        session: requests.Session | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.headers = {
            "Content-Type": "application/json",
            "api-key": api_key,
        }

    def post(self, path: str, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self._request("POST", path, data=data)

    def stream_post(self, path: str, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        return self._stream_request("POST", path, data=data)

    def _request(
        self,
        method: str,
        path: str,
        data: Mapping[str, object] | None = None,
    ) -> Mapping[str, Any]:
        try:
            response = self.session.request(
                method,
                self._url(path),
                headers=self.headers,
                json=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("MiMo API request failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("MiMo API request timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"MiMo API request failed: {exc}") from exc

        try:
            body = response.json()
        except ValueError as exc:
            raise ProviderError("MiMo API request returned invalid JSON") from exc
        if not isinstance(body, Mapping):
            raise ProviderError("MiMo API request returned invalid JSON")
        return body

    def _stream_request(
        self,
        method: str,
        path: str,
        data: Mapping[str, object] | None = None,
    ) -> Iterable[Mapping[str, Any]]:
        try:
            response = self.session.request(
                method,
                self._url(path),
                headers=self.headers,
                json=data,
                timeout=self.timeout,
                stream=True,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("MiMo API stream failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("MiMo API stream timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"MiMo API stream failed: {exc}") from exc

        return _iter_sse_events(response)

    def _url(self, path: str) -> str:
        if path.startswith("/"):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/{path}"


class MimoAPI(MimoBaseAPI):
    """MiMo business API methods."""

    def tts(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MIMO_CHAT_COMPLETIONS_PATH, data=dict(data))

    def tts_stream(self, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        return self.stream_post(MIMO_CHAT_COMPLETIONS_PATH, data=dict(data))

    def voice_design(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MIMO_CHAT_COMPLETIONS_PATH, data=dict(data))

    def voice_clone(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MIMO_CHAT_COMPLETIONS_PATH, data=dict(data))


def _iter_sse_events(response: requests.Response) -> Iterable[Mapping[str, Any]]:
    with response:
        try:
            for raw_line in response.iter_lines(decode_unicode=False):
                event = _parse_sse_line(raw_line)
                if event is not None:
                    yield event
        except requests.exceptions.Timeout as exc:
            raise ProviderError("MiMo API stream timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"MiMo API stream failed: {exc}") from exc


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
        raise ProviderError("MiMo API stream returned invalid JSON") from exc
    if not isinstance(event, Mapping):
        raise ProviderError("MiMo API stream returned invalid JSON")
    return event


def _http_error_message(prefix: str, exc: requests.exceptions.HTTPError) -> str:
    response = exc.response
    if response is None:
        return f"{prefix}: {exc}"

    detail = response.text[:2000]
    return f"{prefix}: HTTP {response.status_code}: {detail}"
