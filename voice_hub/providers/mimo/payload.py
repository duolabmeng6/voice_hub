from __future__ import annotations

from typing import Mapping

from ...errors import ConfigurationError
from ...sample import VoiceSample
from .models import (
    MIMO_TTS_MODEL,
    MIMO_VOICE_CLONE_MODEL,
    MIMO_VOICE_DESIGN_MODEL,
    MimoRequest,
)


class MimoPayloadBuilder:
    """根据 provider 配置和调用覆盖项构造 MiMo 请求。"""

    def __init__(
        self,
        *,
        model: str,
        voice: str,
        style: str | None,
        format: str,
        voice_design_prompt: str | None,
        voice_sample: VoiceSample | None,
    ) -> None:
        self.model = model
        self.voice = voice
        self.style = style
        self.format = format
        self.voice_design_prompt = voice_design_prompt
        self.voice_sample = voice_sample

    def build_request(
        self,
        text: str,
        *,
        stream: bool,
        overrides: Mapping[str, object],
    ) -> MimoRequest:
        options = self.merged_options(overrides)
        messages = self.build_messages(text, options)
        audio = self.build_audio(options)
        return MimoRequest(
            model=str(options["model"]),
            messages=messages,
            audio=audio,
            stream=stream,
        )

    def merged_options(self, overrides: Mapping[str, object]) -> dict[str, object]:
        options: dict[str, object] = {
            "model": self.model,
            "voice": self.voice,
            "style": self.style,
            "speed": None,
            "format": self.format,
            "voice_design_prompt": self.voice_design_prompt,
            "voice_sample": self.voice_sample,
        }

        allowed_keys = set(options)
        unknown_keys = set(overrides) - allowed_keys
        if unknown_keys:
            unknown = ", ".join(sorted(unknown_keys))
            raise TypeError(f"unsupported MiMo override(s): {unknown}")

        options.update({key: value for key, value in overrides.items() if value is not None})
        return options

    def build_messages(
        self,
        text: str,
        options: Mapping[str, object],
    ) -> list[dict[str, str]]:
        model = str(options["model"])
        user_content = self.user_content(options)

        if model == MIMO_VOICE_DESIGN_MODEL and not user_content:
            raise ConfigurationError("voice design prompt is required")

        messages: list[dict[str, str]] = []
        if user_content or model in {MIMO_VOICE_DESIGN_MODEL, MIMO_VOICE_CLONE_MODEL}:
            messages.append({"role": "user", "content": user_content})
        messages.append({"role": "assistant", "content": text})
        return messages

    @staticmethod
    def user_content(options: Mapping[str, object]) -> str:
        prompt = options.get("voice_design_prompt")
        style = options.get("style")
        speed = options.get("speed")

        parts = [str(value).strip() for value in (prompt, style) if value]
        if speed is not None:
            parts.append(speed_instruction(speed))
        return "\n\n".join(part for part in parts if part)

    def build_audio(self, options: Mapping[str, object]) -> dict[str, str]:
        model = str(options["model"])
        audio = {"format": str(options["format"])}

        if model == MIMO_TTS_MODEL:
            audio["voice"] = str(options["voice"])
            return audio

        if model == MIMO_VOICE_DESIGN_MODEL:
            return audio

        if model == MIMO_VOICE_CLONE_MODEL:
            sample = options.get("voice_sample")
            if not isinstance(sample, VoiceSample):
                raise ConfigurationError("voice clone sample is required")
            audio["voice"] = sample.to_data_uri()
            return audio

        raise ConfigurationError(f"unsupported MiMo model: {model}")


def speed_instruction(speed: object) -> str:
    try:
        speed_value = float(speed)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"speed must be a number, got: {speed}") from exc

    if speed_value <= 0:
        raise ConfigurationError("speed must be greater than 0")
    if speed_value == 1:
        return "Use a natural default speaking speed."
    if speed_value > 1:
        return f"Speak at about {speed_value:g}x normal speed."
    return f"Speak at about {speed_value:g}x normal speed, slower than usual."
