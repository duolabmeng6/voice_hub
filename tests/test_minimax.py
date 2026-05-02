import pytest

import voice_hub
from voice_hub.providers.minimax import (
    MINIMAX_BASE_URL,
    MINIMAX_SYSTEM_VOICE_BY_ID,
    MINIMAX_SYSTEM_VOICE_IDS,
    MINIMAX_SYSTEM_VOICES,
    MINIMAX_SYSTEM_VOICES_BY_LANGUAGE,
    MINIMAX_T2A_MODEL,
    MINIMAX_VOICE_CLONE_MODEL,
    MinimaxClonePrompt,
    MinimaxTTS,
    MinimaxVoice,
    MinimaxVoiceClone,
)


class FakeTransport:
    def __init__(self):
        self.posts = []
        self.streams = []

    def post(self, base_url, api_key, payload, timeout):
        self.posts.append((base_url, api_key, payload, timeout))
        return {
            "data": {
                "audio": b"audio-bytes".hex(),
                "status": 2,
            },
            "extra_info": {
                "audio_length": 100,
                "audio_sample_rate": 32000,
                "audio_format": "mp3",
            },
            "trace_id": "trace-1",
            "base_resp": {
                "status_code": 0,
                "status_msg": "success",
            },
        }

    def stream(self, base_url, api_key, payload, timeout):
        self.streams.append((base_url, api_key, payload, timeout))
        return [
            {
                "data": {
                    "audio": b"chunk-1".hex(),
                    "status": 1,
                },
                "base_resp": {
                    "status_code": 0,
                    "status_msg": "",
                },
            },
            {
                "data": {
                    "audio": b"chunk-2".hex(),
                    "status": 2,
                },
                "trace_id": "trace-2",
                "base_resp": {
                    "status_code": 0,
                    "status_msg": "success",
                },
            },
        ]


class FakeVoiceCloneTransport:
    def __init__(self):
        self.uploads = []
        self.clones = []
        self.posts = []
        self.streams = []

    def upload_file(self, base_url, api_key, file_path, purpose, timeout):
        self.uploads.append((base_url, api_key, file_path, purpose, timeout))
        return {
            "file": {"file_id": f"file-{purpose}"},
            "base_resp": {"status_code": 0, "status_msg": "success"},
        }

    def voice_clone(self, base_url, api_key, payload, timeout):
        self.clones.append((base_url, api_key, payload, timeout))
        return {
            "voice_id": payload["voice_id"],
            "demo_audio": "https://filecdn.minimax.chat/public/demo.mp3",
            "base_resp": {"status_code": 0, "status_msg": "success"},
            "trace_id": "clone-trace",
        }

    def download_url(self, url, timeout):
        return b"demo-audio-bytes"

    def post(self, base_url, api_key, payload, timeout):
        self.posts.append((base_url, api_key, payload, timeout))
        raise AssertionError("voice clone must not call t2a post")

    def stream(self, base_url, api_key, payload, timeout):
        self.streams.append((base_url, api_key, payload, timeout))
        raise AssertionError("voice clone must not call t2a stream")


def test_minimax_builtin_voice_constants():
    assert MinimaxVoice.MALE_QN_QINGSE == "male-qn-qingse"
    assert MinimaxVoice.CHINESE_MANDARIN_LYRICAL_VOICE == "Chinese (Mandarin)_Lyrical_Voice"
    assert MinimaxVoice.ENGLISH_GRACEFUL_LADY == "English_Graceful_Lady"
    assert MinimaxVoice.HINDI_FEMALE_1_V2 == "hindi_female_1_v2"


def test_minimax_system_voice_specs_match_docs():
    assert len(MINIMAX_SYSTEM_VOICES) == 327
    assert len(MINIMAX_SYSTEM_VOICE_IDS) == 327
    assert len(set(MINIMAX_SYSTEM_VOICE_IDS)) == 327

    first = MINIMAX_SYSTEM_VOICES[0]
    assert first.index == 1
    assert first.language == "中文 (普通话)"
    assert first.voice_id == "male-qn-qingse"
    assert first.name == "青涩青年音色"
    assert first.note == "中文 (普通话) / 青涩青年音色"

    last = MINIMAX_SYSTEM_VOICES[-1]
    assert last.index == 327
    assert last.language == "印地文"
    assert last.voice_id == "hindi_female_1_v2"
    assert last.name == "News Anchor"

    assert MINIMAX_SYSTEM_VOICE_BY_ID["English_Graceful_Lady"].name == "Graceful Lady"
    assert len(MINIMAX_SYSTEM_VOICES_BY_LANGUAGE["中文 (普通话)"]) == 58
    assert len(MINIMAX_SYSTEM_VOICES_BY_LANGUAGE["中文 (粤语)"]) == 6
    assert MINIMAX_SYSTEM_VOICE_IDS == tuple(voice.voice_id for voice in MINIMAX_SYSTEM_VOICES)


def test_minimax_non_stream_payload_and_response():
    transport = FakeTransport()
    tts = MinimaxTTS(
        api_key="key",
        voice=MinimaxVoice.MALE_QN_QINGSE,
        emotion="happy",
        transport=transport,
    )

    speech = tts.speak("今天是不是很开心呀(laughs)，当然了！")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "MinimaxTTS"
    assert speech.metadata["trace_id"] == "trace-1"

    base_url, api_key, payload, timeout = transport.posts[0]
    assert base_url == MINIMAX_BASE_URL
    assert api_key == "key"
    assert timeout == 60
    assert payload == {
        "model": MINIMAX_T2A_MODEL,
        "text": "今天是不是很开心呀(laughs)，当然了！",
        "stream": False,
        "voice_setting": {
            "voice_id": "male-qn-qingse",
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0,
            "emotion": "happy",
            "text_normalization": False,
            "latex_read": False,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
            "force_cbr": False,
        },
        "subtitle_enable": False,
        "output_format": "hex",
        "aigc_watermark": False,
    }


def test_minimax_build_payload_does_not_send_request():
    transport = FakeTransport()
    tts = MinimaxTTS(api_key="key", voice=MinimaxVoice.ENGLISH_GRACEFUL_LADY, transport=transport)

    payload = tts.build_payload("hello", speed=1.2, language_boost="English")

    assert transport.posts == []
    assert payload["voice_setting"]["voice_id"] == "English_Graceful_Lady"
    assert payload["voice_setting"]["speed"] == 1.2
    assert payload["language_boost"] == "English"


def test_minimax_stream_returns_chunks():
    transport = FakeTransport()
    tts = MinimaxTTS(api_key="key", format="mp3", transport=transport)

    assert list(tts.stream("你好")) == [b"chunk-1", b"chunk-2"]

    payload = transport.streams[0][2]
    assert payload["stream"] is True
    assert payload["audio_setting"]["format"] == "mp3"
    assert "output_format" not in payload


def test_minimax_reads_default_api_key_from_env(monkeypatch):
    monkeypatch.setenv("MINIMAX_KEY", "env-key")
    transport = FakeTransport()
    tts = MinimaxTTS(transport=transport)

    tts.bytes("你好")

    assert transport.posts[0][1] == "env-key"


def test_minimax_rejects_unknown_override():
    tts = MinimaxTTS(api_key="key", transport=FakeTransport())

    with pytest.raises(TypeError, match="unsupported MiniMax override"):
        tts.bytes("你好", temperature=0.8)


def test_minimax_rejects_stream_wav():
    tts = MinimaxTTS(api_key="key", format="wav", transport=FakeTransport())

    with pytest.raises(voice_hub.ConfigurationError, match="stream does not support wav"):
        list(tts.stream("你好"))


def test_minimax_raises_provider_error_for_base_resp():
    class ErrorTransport(FakeTransport):
        def post(self, base_url, api_key, payload, timeout):
            return {
                "data": None,
                "trace_id": "trace-error",
                "base_resp": {
                    "status_code": 2013,
                    "status_msg": "bad request",
                },
            }

    tts = MinimaxTTS(api_key="key", transport=ErrorTransport())

    with pytest.raises(voice_hub.ProviderError, match="status_code=2013"):
        tts.bytes("你好")


def test_minimax_voice_clone_reads_key2_and_uploads(tmp_path, monkeypatch):
    monkeypatch.setenv("MINIMAX_KEY2", "clone-key")
    sample = tmp_path / "clone.wav"
    sample.write_bytes(b"fake-wav")
    transport = FakeVoiceCloneTransport()
    client = MinimaxVoiceClone(transport=transport)

    file_id = client.upload_clone_audio(sample)

    assert file_id == "file-voice_clone"
    assert transport.uploads == [
        (MINIMAX_BASE_URL, "clone-key", sample, "voice_clone", 120),
    ]


def test_minimax_voice_clone_from_file_builds_preview_payload(tmp_path):
    sample = tmp_path / "clone.mp3"
    sample.write_bytes(b"fake-mp3")
    prompt = tmp_path / "prompt.m4a"
    prompt.write_bytes(b"fake-m4a")
    transport = FakeVoiceCloneTransport()
    client = MinimaxVoiceClone(api_key="clone-key", transport=transport)

    result = client.clone_from_file(
        sample,
        "VoiceHubClone01",
        "大兄弟，听您口音不是本地人吧。",
        prompt_path=prompt,
        prompt_text="后来认为啊，是有人抓这鸡。",
        need_noise_reduction=True,
        language_boost="Chinese",
    )

    assert result.voice_id == "VoiceHubClone01"
    assert result.file_id == "file-voice_clone"
    assert result.demo_audio_url == "https://filecdn.minimax.chat/public/demo.mp3"
    assert len(transport.uploads) == 2
    assert transport.uploads[0][3] == "voice_clone"
    assert transport.uploads[1][3] == "prompt_audio"

    payload = transport.clones[0][2]
    assert payload == {
        "file_id": "file-voice_clone",
        "voice_id": "VoiceHubClone01",
        "text": "大兄弟，听您口音不是本地人吧。",
        "model": MINIMAX_VOICE_CLONE_MODEL,
        "need_noise_reduction": True,
        "need_volume_normalization": False,
        "clone_prompt": {
            "prompt_audio": "file-prompt_audio",
            "prompt_text": "后来认为啊，是有人抓这鸡。",
        },
        "language_boost": "Chinese",
    }
    assert transport.posts == []
    assert transport.streams == []


def test_minimax_voice_clone_payload_accepts_prompt_object():
    client = MinimaxVoiceClone(api_key="clone-key", transport=FakeVoiceCloneTransport())

    payload = client.build_clone_payload(
        file_id=123,
        voice_id="VoiceHubClone02",
        text="hello",
        clone_prompt=MinimaxClonePrompt(prompt_audio=456, prompt_text="hello."),
    )

    assert payload["clone_prompt"] == {"prompt_audio": 456, "prompt_text": "hello."}


def test_minimax_voice_clone_rejects_invalid_voice_id():
    client = MinimaxVoiceClone(api_key="clone-key", transport=FakeVoiceCloneTransport())

    with pytest.raises(voice_hub.ConfigurationError, match="voice_id"):
        client.build_clone_payload(file_id=1, voice_id="bad_", text="hello")


def test_minimax_voice_clone_generates_unique_voice_id():
    first = MinimaxVoiceClone.new_voice_id()
    second = MinimaxVoiceClone.new_voice_id()

    assert first != second
    assert first.startswith("VoiceHubClone_")
    assert MinimaxVoiceClone._VOICE_ID_PATTERN.fullmatch(first)


def test_minimax_cloned_tts_speak_save_uses_voice_clone_preview(tmp_path):
    sample = tmp_path / "clone.wav"
    sample.write_bytes(b"fake-wav")
    output = tmp_path / "minimax.mp3"
    transport = FakeVoiceCloneTransport()
    tts = MinimaxTTS.cloned(
        api_key="clone-key",
        sample=voice_hub.VoiceSample(sample),
        transport=transport,
        language_boost="Chinese",
    )

    saved_path = tts.speak("今天是不是很开心呀(laughs)，当然了！").save(output)

    assert saved_path == str(output)
    assert output.read_bytes() == b"demo-audio-bytes"
    assert transport.uploads[0][3] == "voice_clone"
    assert transport.clones[0][2]["text"] == "今天是不是很开心呀(laughs)，当然了！"
    assert transport.clones[0][2]["voice_id"].startswith("VoiceHubClone_")
    assert transport.clones[0][2]["language_boost"] == "Chinese"
    assert transport.posts == []
    assert transport.streams == []
