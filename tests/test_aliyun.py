import base64

import pytest

import voice_hub
from voice_hub.providers.aliyun import (
    ALIYUN_BASE_URL,
    ALIYUN_INTL_BASE_URL,
    ALIYUN_QWEN_TTS_FLASH_MODEL,
    ALIYUN_QWEN_TTS_MODEL,
    ALIYUN_SYSTEM_VOICE_BY_ID,
    ALIYUN_SYSTEM_VOICE_IDS,
    ALIYUN_SYSTEM_VOICES,
    AliyunTTS,
    AliyunVoice,
)


class FakeTransport:
    def __init__(self):
        self.posts = []
        self.streams = []
        self.downloads = []

    def post(self, base_url, api_key, payload, timeout):
        self.posts.append((base_url, api_key, payload, timeout))
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

    def stream(self, base_url, api_key, payload, timeout):
        self.streams.append((base_url, api_key, payload, timeout))
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

    def download_url(self, url, timeout):
        self.downloads.append((url, timeout))
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
    transport = FakeTransport()
    tts = AliyunTTS(
        api_key="key",
        voice=AliyunVoice.CHERRY,
        instructions="语速较快，带有明显的上扬语调，适合介绍时尚产品",
        transport=transport,
    )

    speech = tts.speak("那我来给大家推荐一款T恤")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "AliyunTTS"
    assert speech.metadata["request_id"] == "request-1"
    assert speech.metadata["audio_url"] == "https://dashscope-result.example/audio.wav"

    base_url, api_key, payload, timeout = transport.posts[0]
    assert base_url == ALIYUN_BASE_URL
    assert api_key == "key"
    assert timeout == 60
    assert payload == {
        "model": ALIYUN_QWEN_TTS_MODEL,
        "input": {
            "text": "那我来给大家推荐一款T恤",
            "voice": "Cherry",
            "language_type": "Chinese",
            "instructions": "语速较快，带有明显的上扬语调，适合介绍时尚产品",
        },
    }
    assert transport.downloads == [("https://dashscope-result.example/audio.wav", 60)]


def test_aliyun_build_payload_matches_dashscope_shape():
    transport = FakeTransport()
    tts = AliyunTTS(
        api_key="key",
        model=ALIYUN_QWEN_TTS_FLASH_MODEL,
        voice=AliyunVoice.CHERRY,
        transport=transport,
    )

    payload = tts.build_payload(
        "那我来给大家推荐一款T恤",
        language_type="Chinese",
    )

    assert transport.posts == []
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
    transport = FakeTransport()
    tts = AliyunTTS(transport=transport)

    tts.bytes("你好")

    assert transport.posts[0][1] == "env-key"


def test_aliyun_stream_returns_chunks():
    transport = FakeTransport()
    tts = AliyunTTS(api_key="key", transport=transport)

    assert list(tts.stream("你好")) == [b"chunk-1", b"chunk-2"]

    payload = transport.streams[0][2]
    assert payload == {
        "model": ALIYUN_QWEN_TTS_MODEL,
        "input": {
            "text": "你好",
            "voice": "Cherry",
            "language_type": "Chinese",
        },
    }


def test_aliyun_rejects_instructions_for_non_instruct_model():
    tts = AliyunTTS(
        api_key="key",
        model=ALIYUN_QWEN_TTS_FLASH_MODEL,
        transport=FakeTransport(),
    )

    with pytest.raises(voice_hub.ConfigurationError, match="instructions require"):
        tts.build_payload("你好", instructions="语速较快")


def test_aliyun_rejects_unknown_override():
    tts = AliyunTTS(api_key="key", transport=FakeTransport())

    with pytest.raises(TypeError, match="unsupported Aliyun override"):
        tts.bytes("你好", speed=1.2)


def test_aliyun_can_use_singapore_endpoint():
    transport = FakeTransport()
    tts = AliyunTTS(
        api_key="intl-key",
        base_url=ALIYUN_INTL_BASE_URL,
        transport=transport,
    )

    tts.bytes("hello")

    assert transport.posts[0][0] == ALIYUN_INTL_BASE_URL
