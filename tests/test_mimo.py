import base64

import pytest
import requests

import voice_hub
from voice_hub.errors import ConfigurationError, ProviderError
from voice_hub.providers.mimo import (
    MIMO_BUILTIN_VOICE_BY_ID,
    MIMO_BUILTIN_VOICE_IDS,
    MIMO_BUILTIN_VOICES,
    MIMO_CHAT_COMPLETIONS_PATH,
    MIMO_TTS_MODEL,
    MIMO_VOICE_CLONE_MODEL,
    MIMO_VOICE_DESIGN_MODEL,
    MimoAPI,
    MimoBaseAPI,
    MimoTTS,
    MimoVoice,
)


class FakeMimoAPI:
    def __init__(self):
        self.tts_calls = []
        self.voice_design_calls = []
        self.voice_clone_calls = []
        self.stream_calls = []

    def tts(self, data):
        self.tts_calls.append(dict(data))
        return _audio_response(b"audio-bytes")

    def voice_design(self, data):
        self.voice_design_calls.append(dict(data))
        return _audio_response(b"audio-bytes")

    def voice_clone(self, data):
        self.voice_clone_calls.append(dict(data))
        return _audio_response(b"audio-bytes")

    def tts_stream(self, data):
        self.stream_calls.append(dict(data))
        return [
            _stream_audio_response(b"chunk-1"),
            _stream_audio_response(b"chunk-2"),
        ]


def _audio_response(audio: bytes):
    return {
        "choices": [
            {
                "message": {
                    "audio": {
                        "data": base64.b64encode(audio).decode("utf-8")
                    }
                }
            }
        ]
    }


def _stream_audio_response(audio: bytes):
    return {
        "choices": [
            {
                "delta": {
                    "audio": {
                        "data": base64.b64encode(audio).decode("utf-8")
                    }
                }
            }
        ]
    }


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
    api = FakeMimoAPI()
    tts = MimoTTS(
        api_key="key",
        voice=MimoVoice.BINGTANG,
        style="自然、平稳",
        format="wav",
        api=api,
    )

    assert tts.bytes("夜深了") == b"audio-bytes"

    payload = api.tts_calls[0]
    assert payload["model"] == MIMO_TTS_MODEL
    assert payload["messages"] == [
        {"role": "user", "content": "自然、平稳"},
        {"role": "assistant", "content": "夜深了"},
    ]
    assert payload["audio"] == {"format": "wav", "voice": "冰糖"}
    assert api.voice_design_calls == []
    assert api.voice_clone_calls == []


def test_mimo_speak_is_explicit_provider_entrypoint():
    api = FakeMimoAPI()
    tts = MimoTTS(api_key="key", voice=MimoVoice.MOLI, api=api)

    speech = tts.speak("你好")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "MimoTTS"
    assert speech.metadata["payload"]["audio"] == {"format": "wav", "voice": "茉莉"}


def test_mimo_build_payload_does_not_send_request():
    api = FakeMimoAPI()
    tts = MimoTTS(api_key="key", voice=MimoVoice.BINGTANG, api=api)

    payload = tts.build_payload("你好", voice=MimoVoice.MOLI)

    assert api.tts_calls == []
    assert api.voice_design_calls == []
    assert api.voice_clone_calls == []
    assert api.stream_calls == []
    assert payload["audio"] == {"format": "wav", "voice": "茉莉"}
    assert payload["messages"] == [{"role": "assistant", "content": "你好"}]


def test_mimo_voice_design_payload():
    api = FakeMimoAPI()
    tts = MimoTTS.designed(
        api_key="key",
        prompt="年轻女性，温柔、松弛",
        style="自然、平稳",
        api=api,
    )

    tts.bytes("你好")

    payload = api.voice_design_calls[0]
    assert payload["model"] == MIMO_VOICE_DESIGN_MODEL
    assert payload["messages"] == [
        {"role": "user", "content": "年轻女性，温柔、松弛\n\n自然、平稳"},
        {"role": "assistant", "content": "你好"},
    ]
    assert payload["audio"] == {"format": "wav"}
    assert api.tts_calls == []
    assert api.voice_clone_calls == []


def test_mimo_voice_clone_payload(tmp_path):
    sample_path = tmp_path / "voice.mp3"
    sample_path.write_bytes(b"sample")
    api = FakeMimoAPI()
    tts = MimoTTS.cloned(
        api_key="key",
        sample=voice_hub.VoiceSample(sample_path),
        style="轻快",
        api=api,
    )

    tts.bytes("你好")

    payload = api.voice_clone_calls[0]
    assert payload["model"] == MIMO_VOICE_CLONE_MODEL
    assert payload["messages"] == [
        {"role": "user", "content": "轻快"},
        {"role": "assistant", "content": "你好"},
    ]
    assert payload["audio"]["format"] == "wav"
    assert payload["audio"]["voice"].startswith("data:audio/mpeg;base64,")
    assert api.tts_calls == []
    assert api.voice_design_calls == []


def test_mimo_voice_clone_metadata_redacts_sample(tmp_path):
    sample_path = tmp_path / "voice.mp3"
    sample_path.write_bytes(b"sample")
    api = FakeMimoAPI()
    tts = MimoTTS.cloned(
        api_key="key",
        sample=voice_hub.VoiceSample(sample_path),
        api=api,
    )

    speech = tts.speak("你好")

    assert speech.metadata["payload"]["audio"] == {
        "format": "wav",
        "voice": "<redacted voice sample data URI>",
    }


def test_mimo_stream_defaults_to_pcm16():
    api = FakeMimoAPI()
    tts = MimoTTS(api_key="key", api=api)

    assert list(tts.stream("你好")) == [b"chunk-1", b"chunk-2"]

    payload = api.stream_calls[0]
    assert payload["stream"] is True
    assert payload["audio"]["format"] == "pcm16"


def test_mimo_uses_explicit_base_url_and_api_key():
    tts = MimoTTS(
        api_key="api-key",
        base_url="https://example.test/v1",
    )

    assert tts.api.base_url == "https://example.test/v1"
    assert tts.api.api_key == "api-key"


def test_mimo_token_endpoint_is_explicit_configuration():
    tts = MimoTTS(
        api_key="token-key",
        base_url="https://token-plan-cn.xiaomimimo.com/v1",
    )

    assert tts.api.base_url == "https://token-plan-cn.xiaomimimo.com/v1"
    assert tts.api.api_key == "token-key"


def test_mimo_speed_override_becomes_style_instruction():
    api = FakeMimoAPI()
    tts = MimoTTS(api_key="key", style="轻快", api=api)

    tts.bytes("你好", speed=1.2)

    payload = api.tts_calls[0]
    assert payload["messages"] == [
        {
            "role": "user",
            "content": "轻快\n\nSpeak at about 1.2x normal speed.",
        },
        {"role": "assistant", "content": "你好"},
    ]


def test_mimo_rejects_unknown_override():
    tts = MimoTTS(api_key="key", api=FakeMimoAPI())

    with pytest.raises(TypeError, match="unsupported MiMo override"):
        tts.bytes("你好", temperature=0.8)


def test_mimo_rejects_empty_base_url_before_api_setup():
    with pytest.raises(ConfigurationError, match="MiMo base_url is required"):
        MimoTTS(api_key="key", base_url="")


def test_mimo_api_methods_use_chat_completions_endpoint(monkeypatch):
    calls = []

    def fake_post(self, path, data):
        calls.append((path, dict(data)))
        return _audio_response(b"audio-bytes")

    monkeypatch.setattr(MimoBaseAPI, "post", fake_post)
    api = MimoAPI(api_key="key", base_url="https://example.test/v1")

    api.tts({"model": MIMO_TTS_MODEL})
    api.voice_design({"model": MIMO_VOICE_DESIGN_MODEL})
    api.voice_clone({"model": MIMO_VOICE_CLONE_MODEL})

    assert calls == [
        (MIMO_CHAT_COMPLETIONS_PATH, {"model": MIMO_TTS_MODEL}),
        (MIMO_CHAT_COMPLETIONS_PATH, {"model": MIMO_VOICE_DESIGN_MODEL}),
        (MIMO_CHAT_COMPLETIONS_PATH, {"model": MIMO_VOICE_CLONE_MODEL}),
    ]


def test_mimo_api_converts_http_error():
    response = FakeResponse({"error": "bad request"}, status_code=400, text="bad request")
    response.error = requests.exceptions.HTTPError(response=response)
    api = MimoAPI(api_key="key", base_url="https://example.test/v1", session=FakeSession(response))

    with pytest.raises(ProviderError, match="MiMo API request failed: HTTP 400: bad request"):
        api.tts({"model": "m"})


def test_mimo_api_converts_timeout():
    api = MimoAPI(
        api_key="key",
        base_url="https://example.test/v1",
        session=ErrorSession(requests.exceptions.Timeout()),
    )

    with pytest.raises(ProviderError, match="MiMo API request timed out"):
        api.tts({"model": "m"})


def test_mimo_api_converts_invalid_json():
    api = MimoAPI(
        api_key="key",
        base_url="https://example.test/v1",
        session=FakeSession(FakeResponse(json_error=ValueError("bad json"))),
    )

    with pytest.raises(ProviderError, match="MiMo API request returned invalid JSON"):
        api.tts({"model": "m"})


class FakeResponse:
    def __init__(
        self,
        body=None,
        *,
        status_code=200,
        text="",
        json_error=None,
        lines=None,
    ):
        self.body = body
        self.status_code = status_code
        self.text = text
        self.json_error = json_error
        self.lines = lines or []
        self.error = None
        self.closed = False

    def raise_for_status(self):
        if self.error is not None:
            raise self.error

    def json(self):
        if self.json_error is not None:
            raise self.json_error
        return self.body

    def iter_lines(self, decode_unicode=False):
        return iter(self.lines)

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


class FakeSession:
    def __init__(self, response):
        self.response = response

    def request(self, *args, **kwargs):
        return self.response


class ErrorSession:
    def __init__(self, error):
        self.error = error

    def request(self, *args, **kwargs):
        raise self.error
