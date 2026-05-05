from __future__ import annotations

from typing import Mapping

import requests

from ...errors import ProviderError
from .models import GLM_AUDIO_SPEECH_PATH


class GLMBaseAPI:
    """GLM HTTP API base client."""

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

    def post_bytes(self, path: str, data: Mapping[str, object]) -> bytes:
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
            raise ProviderError(_http_error_message("GLM TTS request failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("GLM TTS request timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"GLM TTS request failed: {exc}") from exc
        return response.content

    def _url(self, path: str) -> str:
        if path.startswith("/"):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/{path}"


class GLMAPI(GLMBaseAPI):
    """GLM business API methods."""

    def speech(self, data: Mapping[str, object]) -> bytes:
        return self.post_bytes(GLM_AUDIO_SPEECH_PATH, data=dict(data))


def _normalize_base_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith(GLM_AUDIO_SPEECH_PATH):
        return normalized[: -len(GLM_AUDIO_SPEECH_PATH)]
    return normalized


def _http_error_message(prefix: str, exc: requests.exceptions.HTTPError) -> str:
    response = exc.response
    if response is None:
        return f"{prefix}: {exc}"
    return f"{prefix}: HTTP {response.status_code}: {response.text[:2000]}"
