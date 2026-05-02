"""统一 TTS 入口。"""

from .client import Client, Speaker
from .errors import (
    ConfigurationError,
    NoDefaultSpeakerError,
    ProviderError,
    SpeakerNotFoundError,
    VoiceHubError,
)
from .providers import (
    MIMO_BUILTIN_VOICE_BY_ID,
    MIMO_BUILTIN_VOICE_IDS,
    MIMO_BUILTIN_VOICES,
    AzureTTS,
    MimoTTS,
    MimoVoice,
    MimoVoiceSpec,
    OpenAITTS,
)
from .sample import VoiceSample
from .speech import Speech

__all__ = [
    "AzureTTS",
    "Client",
    "ConfigurationError",
    "MIMO_BUILTIN_VOICE_BY_ID",
    "MIMO_BUILTIN_VOICE_IDS",
    "MIMO_BUILTIN_VOICES",
    "MimoTTS",
    "MimoVoice",
    "MimoVoiceSpec",
    "NoDefaultSpeakerError",
    "OpenAITTS",
    "ProviderError",
    "Speaker",
    "SpeakerNotFoundError",
    "Speech",
    "VoiceHubError",
    "VoiceSample",
]
