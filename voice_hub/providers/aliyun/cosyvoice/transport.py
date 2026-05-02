from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Mapping

from ....errors import ConfigurationError, ProviderError
from .models import ALIYUN_COSYVOICE_CUSTOMIZATION_PATH


class AliyunCosyVoiceSDKTransport:
    """基于 DashScope SDK 的 CosyVoice 传输层。"""

    def synthesize(
        self,
        *,
        api_key: str,
        model: str,
        voice: str,
        text: str,
        format: str,
        sample_rate: int,
        volume: int,
        speech_rate: float,
        pitch_rate: float,
        seed: int,
        synthesis_type: int,
        instruction: str | None,
        language_hints: list[str] | None,
        additional_params: Mapping[str, object] | None,
        http_base_url: str,
        websocket_base_url: str,
        timeout: float,
    ) -> tuple[bytes, str | None]:
        dashscope, SpeechSynthesizer, audio_format = _load_dashscope_sdk(format, sample_rate)
        _configure_dashscope(dashscope, api_key, http_base_url, websocket_base_url)

        try:
            synthesizer = SpeechSynthesizer(
                model=model,
                voice=voice,
                format=audio_format,
                volume=volume,
                speech_rate=speech_rate,
                pitch_rate=pitch_rate,
                seed=seed,
                synthesis_type=synthesis_type,
                instruction=instruction,
                language_hints=language_hints,
                additional_params=dict(additional_params or {}),
            )
            audio = synthesizer.call(text, timeout_millis=int(timeout * 1000))
        except Exception as exc:  # DashScope SDK 抛出的异常类型不稳定，统一转换为 ProviderError。
            raise ProviderError(f"Aliyun CosyVoice synthesis failed: {exc}") from exc

        if not isinstance(audio, bytes):
            raise ProviderError("Aliyun CosyVoice synthesis returned non-bytes audio")
        return audio, _safe_call(synthesizer, "get_last_request_id")

    def create_voice(
        self,
        *,
        api_key: str,
        target_model: str,
        prefix: str,
        audio_url: str,
        language_hints: list[str] | None,
        max_prompt_audio_length: float | None,
        enable_preprocess: bool | None,
        http_base_url: str,
        websocket_base_url: str,
        timeout: float,
    ) -> tuple[str, str | None]:
        input_data: dict[str, object] = {
            "action": "create_voice",
            "target_model": target_model,
            "prefix": prefix,
            "url": audio_url,
        }
        if language_hints is not None:
            input_data["language_hints"] = list(language_hints)
        if max_prompt_audio_length is not None:
            input_data["max_prompt_audio_length"] = max_prompt_audio_length
        if enable_preprocess is not None:
            input_data["enable_preprocess"] = enable_preprocess

        response = self._customization_request(
            api_key=api_key,
            http_base_url=http_base_url,
            payload={
                "model": "voice-enrollment",
                "input": input_data,
            },
            timeout=timeout,
            error_prefix="Aliyun CosyVoice voice creation failed",
        )

        output = response.get("output")
        if not isinstance(output, Mapping):
            raise ProviderError(f"Aliyun CosyVoice voice creation missing output: {response}")
        voice_id = output.get("voice_id")
        if not isinstance(voice_id, str) or not voice_id:
            raise ProviderError("Aliyun CosyVoice voice creation returned invalid voice_id")
        request_id = response.get("request_id")
        return voice_id, request_id if isinstance(request_id, str) else None

    def query_voice(
        self,
        *,
        api_key: str,
        voice_id: str,
        http_base_url: str,
        websocket_base_url: str,
        timeout: float,
    ) -> Mapping[str, Any]:
        dashscope, VoiceEnrollmentService = _load_voice_enrollment_sdk()
        _configure_dashscope(dashscope, api_key, http_base_url, websocket_base_url)

        try:
            service = VoiceEnrollmentService(api_key=api_key, timeout=timeout)
            result = service.query_voice(voice_id=voice_id)
        except Exception as exc:
            raise ProviderError(f"Aliyun CosyVoice voice query failed: {exc}") from exc

        if not isinstance(result, Mapping):
            raise ProviderError("Aliyun CosyVoice voice query returned invalid result")
        data = dict(result)
        request_id = _safe_call(service, "get_last_request_id")
        if request_id is not None:
            data.setdefault("request_id", request_id)
        return data

    def list_voices(
        self,
        *,
        api_key: str,
        prefix: str | None,
        page_index: int,
        page_size: int,
        http_base_url: str,
        websocket_base_url: str,
        timeout: float,
    ) -> list[Mapping[str, Any]]:
        dashscope, VoiceEnrollmentService = _load_voice_enrollment_sdk()
        _configure_dashscope(dashscope, api_key, http_base_url, websocket_base_url)

        try:
            service = VoiceEnrollmentService(api_key=api_key, timeout=timeout)
            result = service.list_voices(
                prefix=prefix,
                page_index=page_index,
                page_size=page_size,
            )
        except Exception as exc:
            raise ProviderError(f"Aliyun CosyVoice voice list failed: {exc}") from exc

        if not isinstance(result, list):
            raise ProviderError("Aliyun CosyVoice voice list returned invalid result")
        return result

    def delete_voice(
        self,
        *,
        api_key: str,
        voice_id: str,
        http_base_url: str,
        websocket_base_url: str,
        timeout: float,
    ) -> str | None:
        dashscope, VoiceEnrollmentService = _load_voice_enrollment_sdk()
        _configure_dashscope(dashscope, api_key, http_base_url, websocket_base_url)

        try:
            service = VoiceEnrollmentService(api_key=api_key, timeout=timeout)
            service.delete_voice(voice_id=voice_id)
        except Exception as exc:
            raise ProviderError(f"Aliyun CosyVoice voice deletion failed: {exc}") from exc

        return _safe_call(service, "get_last_request_id")

    @staticmethod
    def _customization_request(
        *,
        api_key: str,
        http_base_url: str,
        payload: Mapping[str, object],
        timeout: float,
        error_prefix: str,
    ) -> Mapping[str, Any]:
        url = f"{http_base_url.rstrip('/')}{ALIYUN_COSYVOICE_CUSTOMIZATION_PATH}"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"{error_prefix}: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"{error_prefix}: {exc.reason}") from exc

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise ProviderError(f"{error_prefix}: invalid JSON response") from exc

        code = data.get("code")
        if code:
            raise ProviderError(f"{error_prefix}: code={code}, message={data.get('message')}")
        if not isinstance(data, Mapping):
            raise ProviderError(f"{error_prefix}: invalid response")
        return data


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


def _safe_call(obj: object, method_name: str) -> str | None:
    method = getattr(obj, method_name, None)
    if not callable(method):
        return None
    try:
        value = method()
    except Exception:
        return None
    return value if isinstance(value, str) else None
