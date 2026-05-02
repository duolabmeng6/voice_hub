from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Iterable, Mapping, Optional

from ....errors import ProviderError


class AliyunHTTPTransport:
    """基于标准库的阿里云 DashScope HTTP 传输层。"""

    def post(
        self,
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
        timeout: float,
    ) -> Mapping[str, Any]:
        request = self._build_request(base_url, api_key, payload)
        return self._open_json(request, timeout, "Aliyun TTS API request failed")

    def stream(
        self,
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
        timeout: float,
    ) -> Iterable[Mapping[str, Any]]:
        request = self._build_request(
            base_url,
            api_key,
            payload,
            extra_headers={"X-DashScope-SSE": "enable"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                for raw_line in response:
                    event = self._parse_sse_line(raw_line)
                    if event is not None:
                        yield event
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"Aliyun TTS API stream failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"Aliyun TTS API stream failed: {exc.reason}") from exc

    def download_url(self, url: str, timeout: float) -> bytes:
        request = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"Aliyun TTS audio download failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"Aliyun TTS audio download failed: {exc.reason}") from exc

    @staticmethod
    def _build_request(
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
        extra_headers: Mapping[str, str] | None = None,
    ) -> urllib.request.Request:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        if extra_headers:
            headers.update(extra_headers)
        return urllib.request.Request(
            base_url,
            data=body,
            method="POST",
            headers=headers,
        )

    @staticmethod
    def _open_json(request: urllib.request.Request, timeout: float, error_prefix: str) -> Mapping[str, Any]:
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"{error_prefix}: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"{error_prefix}: {exc.reason}") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise ProviderError(f"{error_prefix}: invalid JSON response") from exc

    @staticmethod
    def _parse_sse_line(raw_line: bytes) -> Optional[Mapping[str, Any]]:
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line or not line.startswith("data:"):
            return None

        data = line.removeprefix("data:").strip()
        if data == "[DONE]":
            return None
        try:
            return json.loads(data)
        except json.JSONDecodeError as exc:
            raise ProviderError("Aliyun TTS API stream returned invalid JSON") from exc
