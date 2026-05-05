from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


GLM_TTS_MODEL = "glm-tts"
GLM_API_ROOT_URL = "https://open.bigmodel.cn/api/paas/v4"
GLM_AUDIO_SPEECH_PATH = "/audio/speech"
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/audio/speech"


class GLMVoice:
    FEMALE = "female"
    MALE = "male"
    TONGTONG = "tongtong"
    CHUICHUI = "chuichui"
    XIAOCHEN = "xiaochen"
    JAM = "jam"
    KAZI = "kazi"
    DOUJI = "douji"
    LUODO = "luodo"


@dataclass(frozen=True)
class GLMVoiceSpec:
    voice_id: str
    name: str
    note: str


GLM_SYSTEM_VOICES = (
    GLMVoiceSpec("female", "female", "系统音色"),
    GLMVoiceSpec("male", "male", "系统音色"),
    GLMVoiceSpec("tongtong", "彤彤", "默认音色"),
    GLMVoiceSpec("chuichui", "锤锤", "系统音色"),
    GLMVoiceSpec("xiaochen", "小陈", "系统音色"),
    GLMVoiceSpec("jam", "jam", "系统音色"),
    GLMVoiceSpec("kazi", "kazi", "系统音色"),
    GLMVoiceSpec("douji", "douji", "系统音色"),
    GLMVoiceSpec("luodo", "luodo", "系统音色"),
)
GLM_SYSTEM_VOICE_IDS = tuple(voice.voice_id for voice in GLM_SYSTEM_VOICES)
GLM_SYSTEM_VOICE_BY_ID = {voice.voice_id: voice for voice in GLM_SYSTEM_VOICES}


@dataclass(frozen=True)
class GLMRequest:
    model: str
    input: str
    voice: str
    response_format: str
    speed: float
    volume: float
    encode_format: str | None = None
    watermark_enabled: bool | None = None
    sensitive_word_check: object | None = None
    request_id: str | None = None
    user_id: str | None = None
    extra_body: Mapping[str, object] | None = None

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "model": self.model,
            "input": self.input,
            "voice": self.voice,
            "response_format": self.response_format,
            "speed": self.speed,
            "volume": self.volume,
        }
        if self.encode_format is not None:
            payload["encode_format"] = self.encode_format
        if self.sensitive_word_check is not None:
            payload["sensitive_word_check"] = self.sensitive_word_check
        if self.watermark_enabled is not None:
            payload["watermark_enabled"] = self.watermark_enabled
        if self.request_id is not None:
            payload["request_id"] = self.request_id
        if self.user_id is not None:
            payload["user_id"] = self.user_id
        if self.extra_body:
            payload["extra_body"] = dict(self.extra_body)
        return payload
