from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Mapping

from ...errors import ProviderError
from .models import GLMRequest


class GLMHTTPTransport:
    """基于标准库 HTTP 的 GLM TTS 传输层。"""

    def synthesize(
        self,
        *,
        api_key: str,
        base_url: str,
        request: GLMRequest,
        timeout: float,
    ) -> bytes:
        http_request = _build_request(base_url, api_key, request.to_payload())
        try:
            with urllib.request.urlopen(http_request, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"GLM TTS request failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"GLM TTS request failed: {exc.reason}") from exc


def _build_request(
    base_url: str,
    api_key: str,
    payload: Mapping[str, object],
) -> urllib.request.Request:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return urllib.request.Request(
        base_url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )


GLMSDKTransport = GLMHTTPTransport
