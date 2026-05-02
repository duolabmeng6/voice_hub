from __future__ import annotations

from typing import Mapping

from ....errors import ConfigurationError
from .models import ALIYUN_QWEN_TTS_MODEL, AliyunRequest


class AliyunPayloadBuilder:
    """根据 provider 配置和调用覆盖项构造阿里云 Qwen TTS 请求。"""

    def __init__(
        self,
        *,
        model: str,
        voice: str,
        language_type: str,
        instructions: str | None,
        optimize_instructions: bool,
    ) -> None:
        self.model = model
        self.voice = voice
        self.language_type = language_type
        self.instructions = instructions
        self.optimize_instructions = optimize_instructions

    def build_request(
        self,
        text: str,
        *,
        overrides: Mapping[str, object],
    ) -> AliyunRequest:
        options = self.merged_options(overrides)
        input_data: dict[str, object] = {
            "text": text,
            "voice": str(options["voice"]),
            "language_type": str(options["language_type"]),
        }
        self.apply_instructions(input_data, options)
        return AliyunRequest(
            model=str(options["model"]),
            input=input_data,
        )

    def merged_options(self, overrides: Mapping[str, object]) -> dict[str, object]:
        options: dict[str, object] = {
            "model": self.model,
            "voice": self.voice,
            "language_type": self.language_type,
            "instructions": self.instructions,
            "optimize_instructions": self.optimize_instructions,
        }

        allowed_keys = set(options)
        unknown_keys = set(overrides) - allowed_keys
        if unknown_keys:
            unknown = ", ".join(sorted(unknown_keys))
            raise TypeError(f"unsupported Aliyun override(s): {unknown}")

        options.update({key: value for key, value in overrides.items() if value is not None})
        return options

    @staticmethod
    def apply_instructions(
        input_data: dict[str, object],
        options: Mapping[str, object],
    ) -> None:
        model = str(options["model"])
        instructions = options.get("instructions")
        optimize_instructions = bool(options.get("optimize_instructions"))

        if instructions:
            if "instruct" not in model:
                raise ConfigurationError("instructions require qwen3-tts-instruct-flash model")
            input_data["instructions"] = str(instructions)
            if optimize_instructions:
                input_data["optimize_instructions"] = True
        elif optimize_instructions and model != ALIYUN_QWEN_TTS_MODEL:
            raise ConfigurationError("optimize_instructions requires qwen3-tts-instruct-flash model")
        elif optimize_instructions:
            input_data["optimize_instructions"] = True
