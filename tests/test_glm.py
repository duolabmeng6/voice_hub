import pytest

import voice_hub
from voice_hub.providers.glm import (
    GLM_BASE_URL,
    GLM_SYSTEM_VOICE_BY_ID,
    GLM_SYSTEM_VOICE_IDS,
    GLM_TTS_MODEL,
    GLMTTS,
    GLMVoice,
)


class FakeTransport:
    def __init__(self):
        self.syntheses = []

    def synthesize(self, *, api_key, base_url, request, timeout):
        self.syntheses.append((api_key, base_url, request, timeout))
        return b"audio-bytes"


def test_glm_non_stream_payload_and_response():
    transport = FakeTransport()
    tts = GLMTTS(
        api_key="key",
        voice=GLMVoice.FEMALE,
        response_format="wav",
        speed=1.2,
        volume=0.8,
        transport=transport,
    )

    speech = tts.speak("夜深了，城市还没有睡。")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "GLMTTS"
    assert speech.metadata["model"] == GLM_TTS_MODEL
    assert speech.metadata["voice"] == "female"
    assert speech.metadata["response_format"] == "wav"

    api_key, base_url, request, timeout = transport.syntheses[0]
    assert api_key == "key"
    assert base_url == GLM_BASE_URL
    assert timeout == 60
    assert request.to_payload() == {
        "model": "glm-tts",
        "input": "夜深了，城市还没有睡。",
        "voice": "female",
        "response_format": "wav",
        "speed": 1.2,
        "volume": 0.8,
    }


def test_glm_build_payload_does_not_send_request():
    transport = FakeTransport()
    tts = GLMTTS(api_key="key", transport=transport)

    payload = tts.build_payload(
        "hello",
        voice="custom-voice-id",
        request_id="request-1",
        user_id="user-1",
        watermark_enabled=True,
        extra_body={"temperature": 0.1},
    )

    assert transport.syntheses == []
    assert payload == {
        "model": "glm-tts",
        "input": "hello",
        "voice": "custom-voice-id",
        "response_format": "wav",
        "speed": 1.0,
        "volume": 1.0,
        "watermark_enabled": True,
        "request_id": "request-1",
        "user_id": "user-1",
        "extra_body": {"temperature": 0.1},
    }


def test_glm_reads_default_api_key_from_env(monkeypatch):
    monkeypatch.setenv("ZHIPUAI_API_KEY", "env-key")
    transport = FakeTransport()
    tts = GLMTTS(transport=transport)

    tts.bytes("你好")

    assert transport.syntheses[0][0] == "env-key"


def test_glm_rejects_unknown_override():
    tts = GLMTTS(api_key="key", transport=FakeTransport())

    with pytest.raises(TypeError, match="unsupported GLM override"):
        tts.bytes("你好", pitch=1)


def test_glm_rejects_invalid_speed():
    tts = GLMTTS(api_key="key", transport=FakeTransport())

    with pytest.raises(voice_hub.ConfigurationError, match="speed must be between 0.5 and 2"):
        tts.build_payload("你好", speed=0)


def test_glm_exports_from_top_level():
    assert voice_hub.GLMTTS is GLMTTS
    assert voice_hub.GLMVoice.FEMALE == "female"
    assert voice_hub.GLM_SYSTEM_VOICE_IDS == GLM_SYSTEM_VOICE_IDS


def test_glm_system_voice_constants_match_docs():
    assert GLM_SYSTEM_VOICE_IDS == (
        "female",
        "male",
        "tongtong",
        "chuichui",
        "xiaochen",
        "jam",
        "kazi",
        "douji",
        "luodo",
    )
    assert GLM_SYSTEM_VOICE_BY_ID["female"].name == "female"
    assert GLM_SYSTEM_VOICE_BY_ID["tongtong"].name == "彤彤"
    assert GLM_SYSTEM_VOICE_BY_ID["tongtong"].note == "默认音色"
