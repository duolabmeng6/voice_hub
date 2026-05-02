class VoiceHubError(Exception):
    """voice_hub 基础异常。"""


class ConfigurationError(VoiceHubError):
    """配置缺失或非法。"""


class SpeakerNotFoundError(VoiceHubError):
    """speaker 不存在。"""


class NoDefaultSpeakerError(VoiceHubError):
    """未配置默认 speaker。"""


class ProviderError(VoiceHubError):
    """厂商接口调用失败。"""
