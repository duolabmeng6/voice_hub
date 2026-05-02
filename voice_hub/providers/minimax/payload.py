from __future__ import annotations

from typing import Mapping

from ...errors import ConfigurationError
from .models import MINIMAX_T2A_MODEL, MinimaxRequest


class MinimaxPayloadBuilder:
    """根据 provider 配置和调用覆盖项构造 MiniMax T2A 请求。"""

    def __init__(
        self,
        *,
        model: str,
        voice: str,
        speed: float,
        vol: float,
        pitch: int,
        emotion: str | None,
        text_normalization: bool,
        latex_read: bool,
        sample_rate: int,
        bitrate: int,
        format: str,
        channel: int,
        force_cbr: bool,
        pronunciation_dict: Mapping[str, object] | None,
        timbre_weights: list[Mapping[str, object]] | None,
        language_boost: str | None,
        voice_modify: Mapping[str, object] | None,
        subtitle_enable: bool,
        output_format: str,
        aigc_watermark: bool,
        stream_options: Mapping[str, object] | None,
    ) -> None:
        self.options: dict[str, object] = {
            "model": model,
            "voice": voice,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
            "emotion": emotion,
            "text_normalization": text_normalization,
            "latex_read": latex_read,
            "sample_rate": sample_rate,
            "bitrate": bitrate,
            "format": format,
            "channel": channel,
            "force_cbr": force_cbr,
            "pronunciation_dict": pronunciation_dict,
            "timbre_weights": timbre_weights,
            "language_boost": language_boost,
            "voice_modify": voice_modify,
            "subtitle_enable": subtitle_enable,
            "output_format": output_format,
            "aigc_watermark": aigc_watermark,
            "stream_options": stream_options,
        }

    def build_request(
        self,
        text: str,
        *,
        stream: bool,
        overrides: Mapping[str, object],
    ) -> MinimaxRequest:
        if not text:
            raise ConfigurationError("MiniMax text is required")

        options = self.merged_options(overrides)
        voice_setting = self.build_voice_setting(options)
        audio_setting = self.build_audio_setting(options, stream=stream)
        output_format = str(options["output_format"])
        if output_format != "hex":
            raise ConfigurationError("MiniMax output_format=url is not supported by byte-returning Speech")
        return MinimaxRequest(
            model=str(options["model"]),
            text=text,
            stream=stream,
            voice_setting=voice_setting,
            audio_setting=audio_setting,
            pronunciation_dict=_mapping_or_none(options["pronunciation_dict"], "pronunciation_dict"),
            timbre_weights=_timbre_weights_or_none(options["timbre_weights"]),
            language_boost=_str_or_none(options["language_boost"]),
            voice_modify=_mapping_or_none(options["voice_modify"], "voice_modify"),
            subtitle_enable=bool(options["subtitle_enable"]),
            output_format=output_format,
            aigc_watermark=bool(options["aigc_watermark"]),
            stream_options=_mapping_or_none(options["stream_options"], "stream_options"),
        )

    def merged_options(self, overrides: Mapping[str, object]) -> dict[str, object]:
        allowed_keys = set(self.options)
        unknown_keys = set(overrides) - allowed_keys
        if unknown_keys:
            unknown = ", ".join(sorted(unknown_keys))
            raise TypeError(f"unsupported MiniMax override(s): {unknown}")

        options = dict(self.options)
        options.update({key: value for key, value in overrides.items() if value is not None})
        return options

    @staticmethod
    def build_voice_setting(options: Mapping[str, object]) -> dict[str, object]:
        voice_setting: dict[str, object] = {
            "voice_id": str(options["voice"]),
            "speed": _float_in_range(options["speed"], "speed", minimum=0.5, maximum=2),
            "vol": _float_in_range(options["vol"], "vol", minimum=0, maximum=10, exclusive_minimum=True),
            "pitch": _int_in_range(options["pitch"], "pitch", minimum=-12, maximum=12),
            "text_normalization": bool(options["text_normalization"]),
            "latex_read": bool(options["latex_read"]),
        }
        if options["emotion"] is not None:
            voice_setting["emotion"] = str(options["emotion"])
        return voice_setting

    @staticmethod
    def build_audio_setting(options: Mapping[str, object], *, stream: bool) -> dict[str, object]:
        audio_format = str(options["format"])
        allowed_formats = {"mp3", "pcm", "flac", "wav"}
        if audio_format not in allowed_formats:
            allowed_text = ", ".join(sorted(allowed_formats))
            raise ConfigurationError(f"format must be one of: {allowed_text}")
        if stream and audio_format == "wav":
            raise ConfigurationError("MiniMax stream does not support wav format")

        return {
            "sample_rate": _int_in_set(
                options["sample_rate"],
                "sample_rate",
                {8000, 16000, 22050, 24000, 32000, 44100},
            ),
            "bitrate": _int_in_set(
                options["bitrate"],
                "bitrate",
                {32000, 64000, 128000, 256000},
            ),
            "format": audio_format,
            "channel": _int_in_set(options["channel"], "channel", {1, 2}),
            "force_cbr": bool(options["force_cbr"]),
        }


def _float_in_range(
    value: object,
    name: str,
    *,
    minimum: float,
    maximum: float,
    exclusive_minimum: bool = False,
) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{name} must be a number, got: {value}") from exc

    if exclusive_minimum and number <= minimum:
        raise ConfigurationError(f"{name} must be greater than {minimum:g}")
    if not exclusive_minimum and number < minimum:
        raise ConfigurationError(f"{name} must be at least {minimum:g}")
    if number > maximum:
        raise ConfigurationError(f"{name} must be at most {maximum:g}")
    return number


def _int_in_range(value: object, name: str, *, minimum: int, maximum: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{name} must be an integer, got: {value}") from exc

    if number < minimum or number > maximum:
        raise ConfigurationError(f"{name} must be between {minimum} and {maximum}")
    return number


def _int_in_set(value: object, name: str, allowed: set[int]) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{name} must be an integer, got: {value}") from exc

    if number not in allowed:
        allowed_text = ", ".join(str(item) for item in sorted(allowed))
        raise ConfigurationError(f"{name} must be one of: {allowed_text}")
    return number


def _mapping_or_none(value: object, name: str) -> Mapping[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ConfigurationError(f"{name} must be a mapping")
    return value


def _timbre_weights_or_none(value: object) -> list[Mapping[str, object]] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ConfigurationError("timbre_weights must be a list")
    for item in value:
        if not isinstance(item, Mapping):
            raise ConfigurationError("timbre_weights entries must be mappings")
    return value


def _str_or_none(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
