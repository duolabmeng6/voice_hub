import pytest

import voice_hub
from voice_hub.providers.glm import (
    GLM_SYSTEM_VOICE_BY_ID,
    GLM_SYSTEM_VOICE_IDS,
    GLM_TTS_MODEL,
    GLMTTS,
    GLMVoice,
)


class FakeGLMAPI:
    def __init__(self):
        self.speech_calls = []

    def speech(self, data):
        self.speech_calls.append(dict(data))
        return b"audio-bytes"


def test_glm_non_stream_payload_and_response():
    api = FakeGLMAPI()
    tts = GLMTTS(
        api_key="key",
        voice=GLMVoice.FEMALE,
        response_format="wav",
        speed=1.2,
        volume=0.8,
        api=api,
    )

    speech = tts.speak("夜深了，城市还没有睡。")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "GLMTTS"
    assert speech.metadata["model"] == GLM_TTS_MODEL
    assert speech.metadata["voice"] == "female"
    assert speech.metadata["response_format"] == "wav"

    assert api.speech_calls == [
        {
            "model": "glm-tts",
            "input": "夜深了，城市还没有睡。",
            "voice": "female",
            "response_format": "wav",
            "speed": 1.2,
            "volume": 0.8,
        }
    ]

def test_glm_build_payload_does_not_send_request():
    api = FakeGLMAPI()
    tts = GLMTTS(api_key="key", api=api)

    payload = tts.build_payload(
        "hello",
        voice="custom-voice-id",
        request_id="request-1",
        user_id="user-1",
        watermark_enabled=True,
        extra_body={"temperature": 0.1},
    )

    assert api.speech_calls == []
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
    tts = GLMTTS()

    assert tts.api.api_key == "env-key"


def test_glm_rejects_unknown_override():
    tts = GLMTTS(api_key="key", api=FakeGLMAPI())

    with pytest.raises(TypeError, match="unsupported GLM override"):
        tts.bytes("你好", pitch=1)


def test_glm_rejects_invalid_speed():
    tts = GLMTTS(api_key="key", api=FakeGLMAPI())

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
