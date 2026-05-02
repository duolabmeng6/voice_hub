from __future__ import annotations

from dataclasses import dataclass


MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"
MIMO_TTS_MODEL = "mimo-v2.5-tts"
MIMO_VOICE_DESIGN_MODEL = "mimo-v2.5-tts-voicedesign"
MIMO_VOICE_CLONE_MODEL = "mimo-v2.5-tts-voiceclone"


@dataclass(frozen=True)
class MimoRequest:
    model: str
    messages: list[dict[str, str]]
    audio: dict[str, str]
    stream: bool = False

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "model": self.model,
            "messages": self.messages,
            "audio": self.audio,
        }
        if self.stream:
            payload["stream"] = True
        return payload
