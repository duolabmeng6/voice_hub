from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class MimoVoiceSpec:
    name: str
    voice_id: str
    language: str
    gender: str | None = None


class MimoVoice:
    """MiMo 官方预置音色 ID 常量。"""

    DEFAULT = "mimo_default"
    BINGTANG = "冰糖"
    MOLI = "茉莉"
    SUDA = "苏打"
    BAIHUA = "白桦"
    MIA = "Mia"
    CHLOE = "Chloe"
    MILO = "Milo"
    DEAN = "Dean"


MIMO_BUILTIN_VOICES = (
    MimoVoiceSpec("MiMo-默认", MimoVoice.DEFAULT, "cluster-dependent"),
    MimoVoiceSpec("冰糖", MimoVoice.BINGTANG, "Chinese", "Female"),
    MimoVoiceSpec("茉莉", MimoVoice.MOLI, "Chinese", "Female"),
    MimoVoiceSpec("苏打", MimoVoice.SUDA, "Chinese", "Male"),
    MimoVoiceSpec("白桦", MimoVoice.BAIHUA, "Chinese", "Male"),
    MimoVoiceSpec("Mia", MimoVoice.MIA, "English", "Female"),
    MimoVoiceSpec("Chloe", MimoVoice.CHLOE, "English", "Female"),
    MimoVoiceSpec("Milo", MimoVoice.MILO, "English", "Male"),
    MimoVoiceSpec("Dean", MimoVoice.DEAN, "English", "Male"),
)
MIMO_BUILTIN_VOICE_IDS = tuple(voice.voice_id for voice in MIMO_BUILTIN_VOICES)
MIMO_BUILTIN_VOICE_BY_ID = MappingProxyType(
    {voice.voice_id: voice for voice in MIMO_BUILTIN_VOICES}
)
