import base64

import pytest

import voice_hub
from voice_hub.providers.aliyun import (
    ALIYUN_INTL_BASE_URL,
    ALIYUN_QWEN_TTS_FLASH_MODEL,
    ALIYUN_QWEN_TTS_MODEL,
    ALIYUN_SYSTEM_VOICE_BY_ID,
    ALIYUN_SYSTEM_VOICE_IDS,
    ALIYUN_SYSTEM_VOICES,
    AliyunTTS,
    AliyunVoice,
)


class FakeAliyunQwenTTSAPI:
    def __init__(self):
        self.generation_calls = []
        self.stream_calls = []
        self.downloads = []

    def generation(self, data):
        self.generation_calls.append(dict(data))
        return {
            "request_id": "request-1",
            "output": {
                "audio": {
                    "url": "https://dashscope-result.example/audio.wav",
                },
                "finish_reason": "stop",
            },
            "usage": {
                "input_tokens": 16,
                "output_tokens": 32,
            },
        }

    def generation_stream(self, data):
        self.stream_calls.append(dict(data))
        return [
            {
                "output": {
                    "audio": {
                        "data": base64.b64encode(b"chunk-1").decode("utf-8")
                    }
                }
            },
            {
                "output": {
                    "audio": {
                        "data": base64.b64encode(b"chunk-2").decode("utf-8")
                    }
                }
            },
        ]

    def download_url(self, url):
        self.downloads.append(url)
        return b"audio-bytes"


def test_aliyun_system_voice_constants():
    assert AliyunVoice.CHERRY == "Cherry"
    assert AliyunVoice.ETHAN == "Ethan"
    assert AliyunVoice.ELDRIC_SAGE == "Eldric Sage"
    assert len(ALIYUN_SYSTEM_VOICES) == 49
    assert len(ALIYUN_SYSTEM_VOICE_IDS) == 49
    assert len(set(ALIYUN_SYSTEM_VOICE_IDS)) == 49
    assert ALIYUN_SYSTEM_VOICE_BY_ID["Cherry"].name == "芊悦"


def test_aliyun_non_stream_payload_and_download():
    api = FakeAliyunQwenTTSAPI()
    tts = AliyunTTS(
        api_key="key",
        voice=AliyunVoice.CHERRY,
        instructions="语速较快，带有明显的上扬语调，适合介绍时尚产品",
        api=api,
    )

    speech = tts.speak("那我来给大家推荐一款T恤")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "AliyunTTS"
    assert speech.metadata["request_id"] == "request-1"
    assert speech.metadata["audio_url"] == "https://dashscope-result.example/audio.wav"

    assert api.generation_calls == [
        {
            "model": ALIYUN_QWEN_TTS_MODEL,
            "input": {
                "text": "那我来给大家推荐一款T恤",
                "voice": "Cherry",
                "language_type": "Chinese",
                "instructions": "语速较快，带有明显的上扬语调，适合介绍时尚产品",
            },
        }
    ]
    assert api.downloads == ["https://dashscope-result.example/audio.wav"]

def test_aliyun_build_payload_matches_dashscope_shape():
    api = FakeAliyunQwenTTSAPI()
    tts = AliyunTTS(
        api_key="key",
        model=ALIYUN_QWEN_TTS_FLASH_MODEL,
        voice=AliyunVoice.CHERRY,
        api=api,
    )

    payload = tts.build_payload(
        "那我来给大家推荐一款T恤",
        language_type="Chinese",
    )

    assert api.generation_calls == []
    assert payload == {
        "model": "qwen3-tts-flash",
        "input": {
            "text": "那我来给大家推荐一款T恤",
            "voice": "Cherry",
            "language_type": "Chinese",
        },
    }


def test_aliyun_uses_env_api_key(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "env-key")
    tts = AliyunTTS()

    assert tts.api.api_key == "env-key"


def test_aliyun_stream_returns_chunks():
    api = FakeAliyunQwenTTSAPI()
    tts = AliyunTTS(api_key="key", api=api)

    assert list(tts.stream("你好")) == [b"chunk-1", b"chunk-2"]

    assert api.stream_calls == [
        {
            "model": ALIYUN_QWEN_TTS_MODEL,
            "input": {
                "text": "你好",
                "voice": "Cherry",
                "language_type": "Chinese",
            },
        }
    ]


def test_aliyun_can_use_singapore_endpoint():
    tts = AliyunTTS(
        api_key="intl-key",
        base_url=ALIYUN_INTL_BASE_URL,
    )

    assert tts.api.base_url == "https://dashscope-intl.aliyuncs.com/api/v1"

def test_aliyun_rejects_instructions_for_non_instruct_model():
    tts = AliyunTTS(
        api_key="key",
        model=ALIYUN_QWEN_TTS_FLASH_MODEL,
        api=FakeAliyunQwenTTSAPI(),
    )

    with pytest.raises(voice_hub.ConfigurationError, match="instructions require"):
        tts.build_payload("你好", instructions="语速较快")


def test_aliyun_rejects_unknown_override():
    tts = AliyunTTS(api_key="key", api=FakeAliyunQwenTTSAPI())

    with pytest.raises(TypeError, match="unsupported Aliyun override"):
        tts.bytes("你好", speed=1.2)
