import base64

import pytest

import voice_hub
from voice_hub.providers.mimo import (
    MIMO_BUILTIN_VOICE_BY_ID,
    MIMO_BUILTIN_VOICE_IDS,
    MIMO_BUILTIN_VOICES,
    MIMO_TTS_MODEL,
    MIMO_VOICE_CLONE_MODEL,
    MIMO_VOICE_DESIGN_MODEL,
    MimoTTS,
    MimoVoice,
)


class FakeTransport:
    def __init__(self):
        self.posts = []
        self.streams = []

    def post(self, base_url, api_key, payload, timeout):
        self.posts.append((base_url, api_key, payload, timeout))
        return {
            "choices": [
                {
                    "message": {
                        "audio": {
                            "data": base64.b64encode(b"audio-bytes").decode("utf-8")
                        }
                    }
                }
            ]
        }

    def stream(self, base_url, api_key, payload, timeout):
        self.streams.append((base_url, api_key, payload, timeout))
        return [
            {
                "choices": [
                    {
                        "delta": {
                            "audio": {
                                "data": base64.b64encode(b"chunk-1").decode("utf-8")
                            }
                        }
                    }
                ]
            },
            {
                "choices": [
                    {
                        "delta": {
                            "audio": {
                                "data": base64.b64encode(b"chunk-2").decode("utf-8")
                            }
                        }
                    }
                ]
            },
        ]


def test_mimo_builtin_voice_constants_match_docs():
    assert MimoVoice.DEFAULT == "mimo_default"
    assert MimoVoice.BINGTANG == "冰糖"
    assert MimoVoice.MOLI == "茉莉"
    assert MimoVoice.SUDA == "苏打"
    assert MimoVoice.BAIHUA == "白桦"
    assert MimoVoice.MIA == "Mia"
    assert MimoVoice.CHLOE == "Chloe"
    assert MimoVoice.MILO == "Milo"
    assert MimoVoice.DEAN == "Dean"
    assert MIMO_BUILTIN_VOICE_IDS == (
        "mimo_default",
        "冰糖",
        "茉莉",
        "苏打",
        "白桦",
        "Mia",
        "Chloe",
        "Milo",
        "Dean",
    )
    assert len(MIMO_BUILTIN_VOICES) == 9
    assert MIMO_BUILTIN_VOICE_BY_ID["冰糖"].gender == "Female"


def test_mimo_builtin_voice_payload():
    transport = FakeTransport()
    tts = MimoTTS(
        api_key="key",
        voice=MimoVoice.BINGTANG,
        style="自然、平稳",
        format="wav",
        transport=transport,
    )

    assert tts.bytes("夜深了") == b"audio-bytes"

    payload = transport.posts[0][2]
    assert payload["model"] == MIMO_TTS_MODEL
    assert payload["messages"] == [
        {"role": "user", "content": "自然、平稳"},
        {"role": "assistant", "content": "夜深了"},
    ]
    assert payload["audio"] == {"format": "wav", "voice": "冰糖"}


def test_mimo_speak_is_explicit_provider_entrypoint():
    transport = FakeTransport()
    tts = MimoTTS(api_key="key", voice=MimoVoice.MOLI, transport=transport)

    speech = tts.speak("你好")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "MimoTTS"
    assert speech.metadata["payload"]["audio"] == {"format": "wav", "voice": "茉莉"}


def test_mimo_build_payload_does_not_send_request():
    transport = FakeTransport()
    tts = MimoTTS(api_key="key", voice=MimoVoice.BINGTANG, transport=transport)

    payload = tts.build_payload("你好", voice=MimoVoice.MOLI)

    assert transport.posts == []
    assert payload["audio"] == {"format": "wav", "voice": "茉莉"}
    assert payload["messages"] == [{"role": "assistant", "content": "你好"}]


def test_mimo_voice_design_payload():
    transport = FakeTransport()
    tts = MimoTTS.designed(
        api_key="key",
        prompt="年轻女性，温柔、松弛",
        style="自然、平稳",
        transport=transport,
    )

    tts.bytes("你好")

    payload = transport.posts[0][2]
    assert payload["model"] == MIMO_VOICE_DESIGN_MODEL
    assert payload["messages"] == [
        {"role": "user", "content": "年轻女性，温柔、松弛\n\n自然、平稳"},
        {"role": "assistant", "content": "你好"},
    ]
    assert payload["audio"] == {"format": "wav"}


def test_mimo_voice_clone_payload(tmp_path):
    sample_path = tmp_path / "voice.mp3"
    sample_path.write_bytes(b"sample")
    transport = FakeTransport()
    tts = MimoTTS.cloned(
        api_key="key",
        sample=voice_hub.VoiceSample(sample_path),
        style="轻快",
        transport=transport,
    )

    tts.bytes("你好")

    payload = transport.posts[0][2]
    assert payload["model"] == MIMO_VOICE_CLONE_MODEL
    assert payload["messages"] == [
        {"role": "user", "content": "轻快"},
        {"role": "assistant", "content": "你好"},
    ]
    assert payload["audio"]["format"] == "wav"
    assert payload["audio"]["voice"].startswith("data:audio/mpeg;base64,")


def test_mimo_stream_defaults_to_pcm16():
    transport = FakeTransport()
    tts = MimoTTS(api_key="key", transport=transport)

    assert list(tts.stream("你好")) == [b"chunk-1", b"chunk-2"]

    payload = transport.streams[0][2]
    assert payload["stream"] is True
    assert payload["audio"]["format"] == "pcm16"


def test_mimo_uses_explicit_base_url_and_api_key():
    transport = FakeTransport()
    tts = MimoTTS(
        api_key="api-key",
        base_url="https://example.test/v1",
        transport=transport,
    )

    tts.bytes("你好")

    base_url, api_key, _, _ = transport.posts[0]
    assert base_url == "https://example.test/v1"
    assert api_key == "api-key"


def test_mimo_token_endpoint_is_explicit_configuration():
    transport = FakeTransport()
    tts = MimoTTS(
        api_key="token-key",
        base_url="https://token-plan-cn.xiaomimimo.com/v1",
        transport=transport,
    )

    tts.bytes("你好")

    base_url, api_key, _, _ = transport.posts[0]
    assert base_url == "https://token-plan-cn.xiaomimimo.com/v1"
    assert api_key == "token-key"


def test_mimo_speed_override_becomes_style_instruction():
    transport = FakeTransport()
    tts = MimoTTS(api_key="key", style="轻快", transport=transport)

    tts.bytes("你好", speed=1.2)

    payload = transport.posts[0][2]
    assert payload["messages"] == [
        {
            "role": "user",
            "content": "轻快\n\nSpeak at about 1.2x normal speed.",
        },
        {"role": "assistant", "content": "你好"},
    ]


def test_mimo_rejects_unknown_override():
    tts = MimoTTS(api_key="key", transport=FakeTransport())

    with pytest.raises(TypeError, match="unsupported MiMo override"):
        tts.bytes("你好", temperature=0.8)
