from __future__ import annotations

from typing import Mapping

from ...errors import ConfigurationError
from .models import GLMRequest


class GLMPayloadBuilder:
    """根据 provider 配置和调用覆盖项构造 GLM TTS 请求。"""

    def __init__(
        self,
        *,
        model: str,
        voice: str,
        response_format: str,
        speed: float,
        volume: float,
        encode_format: str | None,
        watermark_enabled: bool | None,
        sensitive_word_check: object | None,
        request_id: str | None,
        user_id: str | None,
        extra_body: Mapping[str, object] | None,
    ) -> None:
        self.model = model
        self.voice = voice
        self.response_format = response_format
        self.speed = speed
        self.volume = volume
        self.encode_format = encode_format
        self.watermark_enabled = watermark_enabled
        self.sensitive_word_check = sensitive_word_check
        self.request_id = request_id
        self.user_id = user_id
        self.extra_body = extra_body

    def build_request(self, text: str, *, overrides: Mapping[str, object]) -> GLMRequest:
        options = self.merged_options(overrides)
        return GLMRequest(
            model=str(options["model"]),
            input=text,
            voice=str(options["voice"]),
            response_format=_response_format(options["response_format"]),
            speed=_speed(options["speed"]),
            volume=_volume(options["volume"]),
            encode_format=_optional_str(options.get("encode_format")),
            watermark_enabled=_optional_bool(options.get("watermark_enabled")),
            sensitive_word_check=options.get("sensitive_word_check"),
            request_id=_optional_str(options.get("request_id")),
            user_id=_optional_str(options.get("user_id")),
            extra_body=_optional_mapping(options.get("extra_body")),
        )

    def merged_options(self, overrides: Mapping[str, object]) -> dict[str, object]:
        options: dict[str, object] = {
            "model": self.model,
            "voice": self.voice,
            "response_format": self.response_format,
            "speed": self.speed,
            "volume": self.volume,
            "encode_format": self.encode_format,
            "watermark_enabled": self.watermark_enabled,
            "sensitive_word_check": self.sensitive_word_check,
            "request_id": self.request_id,
            "user_id": self.user_id,
            "extra_body": self.extra_body,
        }

        unknown_keys = set(overrides) - set(options)
        if unknown_keys:
            unknown = ", ".join(sorted(unknown_keys))
            raise TypeError(f"unsupported GLM override(s): {unknown}")

        options.update({key: value for key, value in overrides.items() if value is not None})
        return options


def _float(value: object, name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"GLM {name} must be a number") from exc
    return parsed


def _speed(value: object) -> float:
    parsed = _float(value, "speed")
    if not 0.5 <= parsed <= 2:
        raise ConfigurationError("GLM speed must be between 0.5 and 2")
    return parsed


def _volume(value: object) -> float:
    parsed = _float(value, "volume")
    if parsed <= 0:
        raise ConfigurationError("GLM volume must be greater than 0")
    if parsed > 10:
        raise ConfigurationError("GLM volume must be less than or equal to 10")
    return parsed


def _response_format(value: object) -> str:
    response_format = str(value)
    if response_format not in {"wav", "pcm"}:
        raise ConfigurationError("GLM response_format must be wav or pcm")
    return response_format


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    raise ConfigurationError("GLM watermark_enabled must be a boolean")


def _optional_mapping(value: object) -> Mapping[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ConfigurationError("GLM extra_body must be a mapping")
    return value
