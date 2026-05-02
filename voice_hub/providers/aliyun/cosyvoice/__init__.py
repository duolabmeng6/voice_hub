"""阿里云 CosyVoice provider public API。"""

from .clone import AliyunCosyVoiceClone
from .models import (
    ALIYUN_COSYVOICE_CLONE_MODEL,
    ALIYUN_COSYVOICE_ENROLLMENT_MODEL,
    ALIYUN_COSYVOICE_HTTP_BASE_URL,
    ALIYUN_COSYVOICE_MODEL,
    ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL,
    AliyunCosyVoiceEnrollmentResult,
    AliyunCosyVoiceRequest,
    AliyunCosyVoiceUploadedFile,
)
from .transport import AliyunCosyVoiceSDKTransport
from .tts import AliyunCosyVoiceTTS
from .voices import (
    ALIYUN_COSYVOICE_SYSTEM_VOICE_BY_ID,
    ALIYUN_COSYVOICE_SYSTEM_VOICE_IDS,
    ALIYUN_COSYVOICE_SYSTEM_VOICES,
    AliyunCosyVoice,
    AliyunCosyVoiceSpec,
)

__all__ = [
    "ALIYUN_COSYVOICE_CLONE_MODEL",
    "ALIYUN_COSYVOICE_ENROLLMENT_MODEL",
    "ALIYUN_COSYVOICE_HTTP_BASE_URL",
    "ALIYUN_COSYVOICE_MODEL",
    "ALIYUN_COSYVOICE_SYSTEM_VOICE_BY_ID",
    "ALIYUN_COSYVOICE_SYSTEM_VOICE_IDS",
    "ALIYUN_COSYVOICE_SYSTEM_VOICES",
    "ALIYUN_COSYVOICE_WEBSOCKET_BASE_URL",
    "AliyunCosyVoice",
    "AliyunCosyVoiceClone",
    "AliyunCosyVoiceEnrollmentResult",
    "AliyunCosyVoiceRequest",
    "AliyunCosyVoiceSDKTransport",
    "AliyunCosyVoiceSpec",
    "AliyunCosyVoiceTTS",
    "AliyunCosyVoiceUploadedFile",
]
