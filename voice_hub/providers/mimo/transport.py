from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Iterable, Mapping, Optional

from ...errors import ProviderError


class MimoHTTPTransport:
    """基于标准库的 MiMo HTTP 传输层。"""

    def post(
        self,
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
        timeout: float,
    ) -> Mapping[str, Any]:
        request = self._build_request(base_url, api_key, payload)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"MiMo API request failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"MiMo API request failed: {exc.reason}") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise ProviderError("MiMo API request returned invalid JSON") from exc

    def stream(
        self,
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
        timeout: float,
    ) -> Iterable[Mapping[str, Any]]:
        request = self._build_request(base_url, api_key, payload)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                for raw_line in response:
                    event = self._parse_sse_line(raw_line)
                    if event is not None:
                        yield event
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"MiMo API stream failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"MiMo API stream failed: {exc.reason}") from exc

    @staticmethod
    def _build_request(
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
    ) -> urllib.request.Request:
        url = f"{base_url.rstrip('/')}/chat/completions"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        return urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "api-key": api_key,
            },
        )

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
            raise ProviderError("MiMo API stream returned invalid JSON") from exc
