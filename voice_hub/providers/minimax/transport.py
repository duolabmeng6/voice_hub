from __future__ import annotations

import json
import mimetypes
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional

from ...errors import ProviderError


class MinimaxHTTPTransport:
    """基于标准库的 MiniMax T2A HTTP 传输层。"""

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
            raise ProviderError(f"MiniMax API request failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"MiniMax API request failed: {exc.reason}") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise ProviderError("MiniMax API request returned invalid JSON") from exc

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
            raise ProviderError(f"MiniMax API stream failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"MiniMax API stream failed: {exc.reason}") from exc

    def upload_file(
        self,
        base_url: str,
        api_key: str,
        file_path: str | Path,
        purpose: str,
        timeout: float,
    ) -> Mapping[str, Any]:
        path = Path(file_path)
        boundary = f"----voice-hub-minimax-{uuid.uuid4().hex}"
        body = _encode_multipart_form(
            boundary,
            fields={"purpose": purpose},
            file_field="file",
            file_path=path,
        )
        request = urllib.request.Request(
            f"{base_url.rstrip('/')}/files/upload",
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        return self._open_json(request, timeout, "MiniMax file upload failed")

    def voice_clone(
        self,
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
        timeout: float,
    ) -> Mapping[str, Any]:
        request = self._build_json_request(
            f"{base_url.rstrip('/')}/voice_clone",
            api_key,
            payload,
        )
        return self._open_json(request, timeout, "MiniMax voice clone failed")

    def download_url(self, url: str, timeout: float) -> bytes:
        request = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"MiniMax demo audio download failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"MiniMax demo audio download failed: {exc.reason}") from exc

    @staticmethod
    def _build_request(
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
    ) -> urllib.request.Request:
        url = f"{base_url.rstrip('/')}/t2a_v2"
        return MinimaxHTTPTransport._build_json_request(url, api_key, payload)

    @staticmethod
    def _build_json_request(
        url: str,
        api_key: str,
        payload: Mapping[str, object],
    ) -> urllib.request.Request:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        return urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
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
            raise ProviderError("MiniMax API stream returned invalid JSON") from exc


def _encode_multipart_form(
    boundary: str,
    fields: Mapping[str, str],
    file_field: str,
    file_path: Path,
) -> bytes:
    if not file_path.exists():
        raise FileNotFoundError(str(file_path))

    lines: list[bytes] = []
    for name, value in fields.items():
        lines.extend(
            [
                f"--{boundary}".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"'.encode("utf-8"),
                b"",
                value.encode("utf-8"),
            ]
        )

    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    lines.extend(
        [
            f"--{boundary}".encode("utf-8"),
            (
                f'Content-Disposition: form-data; name="{file_field}"; '
                f'filename="{file_path.name}"'
            ).encode("utf-8"),
            f"Content-Type: {content_type}".encode("utf-8"),
            b"",
            file_path.read_bytes(),
            f"--{boundary}--".encode("utf-8"),
            b"",
        ]
    )
    return b"\r\n".join(lines)
