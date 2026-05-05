from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from typing import Any, Iterable, Mapping

import requests

from ...errors import ProviderError
from .models import MINIMAX_FILES_UPLOAD_PATH, MINIMAX_T2A_PATH, MINIMAX_VOICE_CLONE_PATH


class MinimaxBaseAPI:
    """MiniMax HTTP API base client."""

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
            raise ProviderError(_http_error_message("MiniMax API request failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("MiniMax API request timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"MiniMax API request failed: {exc}") from exc
        return _json_mapping(response, "MiniMax API request failed")

    def stream_post(self, path: str, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        try:
            response = self.session.request(
                "POST",
                self._url(path),
                headers=self.headers,
                json=data,
                timeout=self.timeout,
                stream=True,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("MiniMax API stream failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("MiniMax API stream timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"MiniMax API stream failed: {exc}") from exc
        return _iter_sse_events(response)

    def post_file(
        self,
        path: str,
        *,
        file_path: str | Path,
        data: Mapping[str, str],
    ) -> Mapping[str, Any]:
        upload_path = Path(file_path)
        if not upload_path.exists():
            raise FileNotFoundError(str(upload_path))

        headers = dict(self.headers)
        headers.pop("Content-Type", None)
        content_type = mimetypes.guess_type(str(upload_path))[0] or "application/octet-stream"
        try:
            with upload_path.open("rb") as file_obj:
                response = self.session.request(
                    "POST",
                    self._url(path),
                    headers=headers,
                    data=dict(data),
                    files={"file": (upload_path.name, file_obj, content_type)},
                    timeout=self.timeout,
                )
                response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("MiniMax file upload failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("MiniMax file upload timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"MiniMax file upload failed: {exc}") from exc
        return _json_mapping(response, "MiniMax file upload failed")

    def get_bytes_url(self, url: str) -> bytes:
        try:
            response = self.session.request("GET", url, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("MiniMax demo audio download failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("MiniMax demo audio download timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"MiniMax demo audio download failed: {exc}") from exc
        return response.content

    def _url(self, path: str) -> str:
        if path.startswith("/"):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/{path}"


class MinimaxAPI(MinimaxBaseAPI):
    """MiniMax business API methods."""

    def t2a_v2(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MINIMAX_T2A_PATH, data=dict(data))

    def t2a_v2_stream(self, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        return self.stream_post(MINIMAX_T2A_PATH, data=dict(data))

    def upload_file(self, file_path: str | Path, purpose: str) -> Mapping[str, Any]:
        return self.post_file(
            MINIMAX_FILES_UPLOAD_PATH,
            file_path=file_path,
            data={"purpose": purpose},
        )

    def voice_clone(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MINIMAX_VOICE_CLONE_PATH, data=dict(data))

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
            raise ProviderError("MiniMax API stream timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"MiniMax API stream failed: {exc}") from exc


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
        raise ProviderError("MiniMax API stream returned invalid JSON") from exc
    if not isinstance(event, Mapping):
        raise ProviderError("MiniMax API stream returned invalid JSON")
    return event


def _json_mapping(response: requests.Response, prefix: str) -> Mapping[str, Any]:
    try:
        body = response.json()
    except ValueError as exc:
        raise ProviderError(f"{prefix}: invalid JSON response") from exc
    if not isinstance(body, Mapping):
        raise ProviderError(f"{prefix}: invalid JSON response")
    return body


def _http_error_message(prefix: str, exc: requests.exceptions.HTTPError) -> str:
    response = exc.response
    if response is None:
        return f"{prefix}: {exc}"
    return f"{prefix}: HTTP {response.status_code}: {response.text[:2000]}"
