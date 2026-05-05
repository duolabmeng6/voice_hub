"""阿里云百炼 Qwen TTS provider public API。"""

from .api import AliyunQwenTTSAPI, AliyunQwenTTSBaseAPI
from .models import (
    ALIYUN_API_ROOT_URL,
    ALIYUN_BASE_URL,
    ALIYUN_INTL_BASE_URL,
    ALIYUN_INTL_API_ROOT_URL,
    ALIYUN_QWEN_TTS_GENERATION_PATH,
    ALIYUN_QWEN_TTS_FLASH_MODEL,
    ALIYUN_QWEN_TTS_MODEL,
    AliyunRequest,
)
from .tts import AliyunTTS
from .voices import (
    ALIYUN_SYSTEM_VOICE_BY_ID,
    ALIYUN_SYSTEM_VOICE_IDS,
    ALIYUN_SYSTEM_VOICES,
    AliyunVoice,
    AliyunVoiceSpec,
)

__all__ = [
    "ALIYUN_API_ROOT_URL",
    "ALIYUN_BASE_URL",
    "ALIYUN_INTL_BASE_URL",
    "ALIYUN_INTL_API_ROOT_URL",
    "ALIYUN_QWEN_TTS_GENERATION_PATH",
    "ALIYUN_QWEN_TTS_FLASH_MODEL",
    "ALIYUN_QWEN_TTS_MODEL",
    "ALIYUN_SYSTEM_VOICE_BY_ID",
    "ALIYUN_SYSTEM_VOICE_IDS",
    "ALIYUN_SYSTEM_VOICES",
    "AliyunQwenTTSAPI",
    "AliyunQwenTTSBaseAPI",
    "AliyunRequest",
    "AliyunTTS",
    "AliyunVoice",
    "AliyunVoiceSpec",
]
