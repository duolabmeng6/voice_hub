from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from typing import Any, Mapping

import requests

from ....errors import ConfigurationError, ProviderError
from .models import (
    ALIYUN_COSYVOICE_CUSTOMIZATION_PATH,
    ALIYUN_COSYVOICE_FILES_PATH,
    ALIYUN_COSYVOICE_HTTP_BASE_URL,
    ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL,
)


class AliyunCosyVoiceBaseAPI:
    """Aliyun CosyVoice API base client."""

    def __init__(
        self,
        api_key: str,
        http_base_url: str = ALIYUN_COSYVOICE_HTTP_BASE_URL,
        websocket_base_url: str = ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL,
        timeout: float = 60,
        session: requests.Session | None = None,
    ) -> None:
        self.api_key = api_key
        self.http_base_url = http_base_url.rstrip("/")
        self.websocket_base_url = websocket_base_url
        self.timeout = timeout
        self.session = session or requests.Session()
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def get(self, path: str) -> Mapping[str, Any]:
        try:
            response = self.session.request(
                "GET",
                self._url(path),
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ProviderError(_http_error_message("Aliyun file query failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("Aliyun file query timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"Aliyun file query failed: {exc}") from exc
        return _json_mapping(response, "Aliyun file query failed")

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
            raise ProviderError(_http_error_message("Aliyun CosyVoice API request failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("Aliyun CosyVoice API request timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"Aliyun CosyVoice API request failed: {exc}") from exc
        return _json_mapping(response, "Aliyun CosyVoice API request failed")

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
            raise ProviderError(_http_error_message("Aliyun file upload failed", exc)) from exc
        except requests.exceptions.Timeout as exc:
            raise ProviderError("Aliyun file upload timed out") from exc
        except requests.exceptions.RequestException as exc:
            raise ProviderError(f"Aliyun file upload failed: {exc}") from exc
        return _json_mapping(response, "Aliyun file upload failed")

    def _url(self, path: str) -> str:
        if path.startswith("/"):
            return f"{self.http_base_url}{path}"
        return f"{self.http_base_url}/{path}"


class AliyunCosyVoiceAPI(AliyunCosyVoiceBaseAPI):
    """Aliyun CosyVoice business API methods."""

    def synthesize(self, data: Mapping[str, object]) -> tuple[bytes, str | None]:
        return self._sdk_synthesize(data)

    def create_voice(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        response = self.post(ALIYUN_COSYVOICE_CUSTOMIZATION_PATH, data=dict(data))
        _raise_for_code(response, "Aliyun CosyVoice voice creation failed")
        return response

    def query_voice(self, voice_id: str) -> Mapping[str, Any]:
        return self._sdk_query_voice(voice_id)

    def list_voices(self, data: Mapping[str, object]) -> list[Mapping[str, Any]]:
        return self._sdk_list_voices(data)

    def delete_voice(self, voice_id: str) -> str | None:
        return self._sdk_delete_voice(voice_id)

    def upload_file(self, file_path: str | Path, purpose: str) -> Mapping[str, Any]:
        return self.post_file(
            ALIYUN_COSYVOICE_FILES_PATH,
            file_path=file_path,
            data={"purpose": purpose},
        )

    def get_file(self, file_id: str) -> Mapping[str, Any]:
        return self.get(f"{ALIYUN_COSYVOICE_FILES_PATH}/{file_id}")

    def _sdk_synthesize(self, data: Mapping[str, object]) -> tuple[bytes, str | None]:
        format_value = str(data.get("format", "mp3"))
        sample_rate = int(data.get("sample_rate", 24000))
        dashscope, SpeechSynthesizer, audio_format = _load_dashscope_sdk(format_value, sample_rate)
        _configure_dashscope(dashscope, self.api_key, self.http_base_url, self.websocket_base_url)

        try:
            synthesizer = SpeechSynthesizer(
                model=str(data["model"]),
                voice=str(data["voice"]),
                format=audio_format,
                volume=int(data.get("volume", 50)),
                speech_rate=float(data.get("speech_rate", 1.0)),
                pitch_rate=float(data.get("pitch_rate", 1.0)),
                seed=int(data.get("seed", 0)),
                synthesis_type=int(data.get("synthesis_type", 0)),
                instruction=_optional_str(data.get("instruction")),
                language_hints=_optional_str_list(data.get("language_hints")),
                additional_params=_optional_mapping(data.get("additional_params")) or {},
            )
            audio = synthesizer.call(str(data["text"]), timeout_millis=int(self.timeout * 1000))
        except KeyError as exc:
            raise ProviderError(f"Aliyun CosyVoice synthesis missing field: {exc}") from exc
        except Exception as exc:  # DashScope SDK 抛出的异常类型不稳定，统一转换为 ProviderError。
            raise ProviderError(f"Aliyun CosyVoice synthesis failed: {exc}") from exc

        if not isinstance(audio, bytes):
            raise ProviderError("Aliyun CosyVoice synthesis returned non-bytes audio")
        return audio, _safe_call(synthesizer, "get_last_request_id")

    def _sdk_query_voice(self, voice_id: str) -> Mapping[str, Any]:
        dashscope, VoiceEnrollmentService = _load_voice_enrollment_sdk()
        _configure_dashscope(dashscope, self.api_key, self.http_base_url, self.websocket_base_url)

        try:
            service = VoiceEnrollmentService(api_key=self.api_key, timeout=self.timeout)
            result = service.query_voice(voice_id=voice_id)
        except Exception as exc:
            raise ProviderError(f"Aliyun CosyVoice voice query failed: {exc}") from exc

        if not isinstance(result, Mapping):
            raise ProviderError("Aliyun CosyVoice voice query returned invalid result")
        payload = dict(result)
        request_id = _safe_call(service, "get_last_request_id")
        if request_id is not None:
            payload.setdefault("request_id", request_id)
        return payload

    def _sdk_list_voices(self, data: Mapping[str, object]) -> list[Mapping[str, Any]]:
        dashscope, VoiceEnrollmentService = _load_voice_enrollment_sdk()
        _configure_dashscope(dashscope, self.api_key, self.http_base_url, self.websocket_base_url)

        try:
            service = VoiceEnrollmentService(api_key=self.api_key, timeout=self.timeout)
            result = service.list_voices(
                prefix=_optional_str(data.get("prefix")),
                page_index=int(data.get("page_index", 0)),
                page_size=int(data.get("page_size", 10)),
            )
        except Exception as exc:
            raise ProviderError(f"Aliyun CosyVoice voice list failed: {exc}") from exc

        if not isinstance(result, list):
            raise ProviderError("Aliyun CosyVoice voice list returned invalid result")
        return result

    def _sdk_delete_voice(self, voice_id: str) -> str | None:
        dashscope, VoiceEnrollmentService = _load_voice_enrollment_sdk()
        _configure_dashscope(dashscope, self.api_key, self.http_base_url, self.websocket_base_url)

        try:
            service = VoiceEnrollmentService(api_key=self.api_key, timeout=self.timeout)
            service.delete_voice(voice_id=voice_id)
        except Exception as exc:
            raise ProviderError(f"Aliyun CosyVoice voice deletion failed: {exc}") from exc

        return _safe_call(service, "get_last_request_id")


def _json_mapping(response: requests.Response, prefix: str) -> Mapping[str, Any]:
    try:
        body = response.json()
    except ValueError as exc:
        raise ProviderError(f"{prefix}: invalid JSON response") from exc
    if not isinstance(body, Mapping):
        raise ProviderError(f"{prefix}: invalid response")
    return body


def _http_error_message(prefix: str, exc: requests.exceptions.HTTPError) -> str:
    response = exc.response
    if response is None:
        return f"{prefix}: {exc}"
    return f"{prefix}: HTTP {response.status_code}: {response.text[:2000]}"


def _raise_for_code(response: Mapping[str, Any], prefix: str) -> None:
    code = response.get("code")
    if code:
        raise ProviderError(f"{prefix}: code={code}, message={response.get('message')}")


def _load_dashscope_sdk(format: str, sample_rate: int):
    try:
        import dashscope
        from dashscope.audio.tts_v2 import AudioFormat, SpeechSynthesizer
    except ImportError as exc:
        raise ConfigurationError("dashscope package is required for Aliyun CosyVoice") from exc

    return dashscope, SpeechSynthesizer, _audio_format(AudioFormat, format, sample_rate)


def _load_voice_enrollment_sdk():
    try:
        import dashscope
        from dashscope.audio.tts_v2 import VoiceEnrollmentService
    except ImportError as exc:
        raise ConfigurationError("dashscope package is required for Aliyun CosyVoice voice clone") from exc

    return dashscope, VoiceEnrollmentService


def _configure_dashscope(
    dashscope,
    api_key: str,
    http_base_url: str,
    websocket_base_url: str,
) -> None:
    dashscope.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
    dashscope.base_http_api_url = http_base_url
    dashscope.base_websocket_api_url = websocket_base_url


def _audio_format(AudioFormat, format: str, sample_rate: int):
    key = f"{format.upper()}_{sample_rate}HZ_MONO_16BIT"
    if format.lower() == "mp3":
        bitrate = 128 if sample_rate in {8000, 16000} else 256
        key = f"MP3_{sample_rate}HZ_MONO_{bitrate}KBPS"
    if format.lower() == "opus":
        key = f"OGG_OPUS_{sample_rate // 1000}KHZ_MONO_32KBPS"

    try:
        return getattr(AudioFormat, key)
    except AttributeError as exc:
        raise ConfigurationError(f"unsupported CosyVoice audio format: {format}/{sample_rate}") from exc


def _optional_str(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _optional_str_list(value: object) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    raise ConfigurationError("language_hints must be a string list")


def _optional_mapping(value: object) -> Mapping[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ConfigurationError("additional_params must be a mapping")
    return value


def _safe_call(obj: object, method_name: str) -> str | None:
    method = getattr(obj, method_name, None)
    if not callable(method):
        return None
    try:
        value = method()
    except Exception:
        return None
    return value if isinstance(value, str) else None
