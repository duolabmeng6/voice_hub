from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


ALIYUN_BASE_URL = (
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/"
    "multimodal-generation/generation"
)
ALIYUN_INTL_BASE_URL = (
    "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/"
    "multimodal-generation/generation"
)
ALIYUN_API_ROOT_URL = "https://dashscope.aliyuncs.com/api/v1"
ALIYUN_INTL_API_ROOT_URL = "https://dashscope-intl.aliyuncs.com/api/v1"
ALIYUN_QWEN_TTS_GENERATION_PATH = "/services/aigc/multimodal-generation/generation"
ALIYUN_QWEN_TTS_MODEL = "qwen3-tts-instruct-flash"
ALIYUN_QWEN_TTS_FLASH_MODEL = "qwen3-tts-flash"


@dataclass(frozen=True)
class AliyunRequest:
    model: str
    input: Mapping[str, object]
    parameters: Mapping[str, object] | None = None

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "model": self.model,
            "input": dict(self.input),
        }
        if self.parameters:
            payload["parameters"] = dict(self.parameters)
        return payload
