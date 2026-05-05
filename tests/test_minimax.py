import pytest

import voice_hub
from voice_hub.providers.minimax import (
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


class FakeMinimaxAPI:
    def __init__(self):
        self.t2a_calls = []
        self.stream_calls = []
        self.uploads = []
        self.voice_clone_calls = []
        self.downloads = []

    def t2a_v2(self, data):
        self.t2a_calls.append(dict(data))
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

    def t2a_v2_stream(self, data):
        self.stream_calls.append(dict(data))
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

    def upload_file(self, file_path, purpose):
        self.uploads.append((file_path, purpose))
        return {
            "file": {"file_id": f"file-{purpose}"},
            "base_resp": {"status_code": 0, "status_msg": "success"},
        }

    def voice_clone(self, data):
        payload = dict(data)
        self.voice_clone_calls.append(payload)
        return {
            "voice_id": payload["voice_id"],
            "demo_audio": "https://filecdn.minimax.chat/public/demo.mp3",
            "base_resp": {"status_code": 0, "status_msg": "success"},
            "trace_id": "clone-trace",
        }

    def download_url(self, url):
        self.downloads.append(url)
        return b"demo-audio-bytes"


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
    api = FakeMinimaxAPI()
    tts = MinimaxTTS(
        api_key="key",
        voice=MinimaxVoice.MALE_QN_QINGSE,
        emotion="happy",
        api=api,
    )

    speech = tts.speak("今天是不是很开心呀(laughs)，当然了！")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "MinimaxTTS"
    assert speech.metadata["trace_id"] == "trace-1"

    assert api.t2a_calls == [
        {
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
    ]

def test_minimax_build_payload_does_not_send_request():
    api = FakeMinimaxAPI()
    tts = MinimaxTTS(api_key="key", voice=MinimaxVoice.ENGLISH_GRACEFUL_LADY, api=api)

    payload = tts.build_payload("hello", speed=1.2, language_boost="English")

    assert api.t2a_calls == []
    assert payload["voice_setting"]["voice_id"] == "English_Graceful_Lady"
    assert payload["voice_setting"]["speed"] == 1.2
    assert payload["language_boost"] == "English"


def test_minimax_stream_returns_chunks():
    api = FakeMinimaxAPI()
    tts = MinimaxTTS(api_key="key", format="mp3", api=api)

    assert list(tts.stream("你好")) == [b"chunk-1", b"chunk-2"]

    payload = api.stream_calls[0]
    assert payload["stream"] is True
    assert payload["audio_setting"]["format"] == "mp3"
    assert "output_format" not in payload


def test_minimax_reads_default_api_key_from_env(monkeypatch):
    monkeypatch.setenv("MINIMAX_KEY", "env-key")
    tts = MinimaxTTS()

    assert tts.api.api_key == "env-key"


def test_minimax_rejects_unknown_override():
    tts = MinimaxTTS(api_key="key", api=FakeMinimaxAPI())

    with pytest.raises(TypeError, match="unsupported MiniMax override"):
        tts.bytes("你好", temperature=0.8)


def test_minimax_rejects_stream_wav():
    tts = MinimaxTTS(api_key="key", format="wav", api=FakeMinimaxAPI())

    with pytest.raises(voice_hub.ConfigurationError, match="stream does not support wav"):
        list(tts.stream("你好"))


def test_minimax_raises_provider_error_for_base_resp():
    class ErrorAPI(FakeMinimaxAPI):
        def t2a_v2(self, data):
            return {
                "data": None,
                "trace_id": "trace-error",
                "base_resp": {
                    "status_code": 2013,
                    "status_msg": "bad request",
                },
            }

    tts = MinimaxTTS(api_key="key", api=ErrorAPI())

    with pytest.raises(voice_hub.ProviderError, match="status_code=2013"):
        tts.bytes("你好")


def test_minimax_voice_clone_reads_key2_and_uploads(tmp_path, monkeypatch):
    monkeypatch.setenv("MINIMAX_KEY2", "clone-key")
    sample = tmp_path / "clone.wav"
    sample.write_bytes(b"fake-wav")
    api = FakeMinimaxAPI()
    client = MinimaxVoiceClone(api=api)

    file_id = client.upload_clone_audio(sample)

    assert file_id == "file-voice_clone"
    assert api.uploads == [(sample, "voice_clone")]


def test_minimax_voice_clone_from_file_builds_preview_payload(tmp_path):
    sample = tmp_path / "clone.mp3"
    sample.write_bytes(b"fake-mp3")
    prompt = tmp_path / "prompt.m4a"
    prompt.write_bytes(b"fake-m4a")
    api = FakeMinimaxAPI()
    client = MinimaxVoiceClone(api_key="clone-key", api=api)

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
    assert len(api.uploads) == 2
    assert api.uploads[0][1] == "voice_clone"
    assert api.uploads[1][1] == "prompt_audio"

    payload = api.voice_clone_calls[0]
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
    assert api.t2a_calls == []
    assert api.stream_calls == []


def test_minimax_voice_clone_payload_accepts_prompt_object():
    client = MinimaxVoiceClone(api_key="clone-key", api=FakeMinimaxAPI())

    payload = client.build_clone_payload(
        file_id=123,
        voice_id="VoiceHubClone02",
        text="hello",
        clone_prompt=MinimaxClonePrompt(prompt_audio=456, prompt_text="hello."),
    )

    assert payload["clone_prompt"] == {"prompt_audio": 456, "prompt_text": "hello."}


def test_minimax_voice_clone_rejects_invalid_voice_id():
    client = MinimaxVoiceClone(api_key="clone-key", api=FakeMinimaxAPI())

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
    api = FakeMinimaxAPI()
    tts = MinimaxTTS.cloned(
        api_key="clone-key",
        sample=voice_hub.VoiceSample(sample),
        api=api,
        language_boost="Chinese",
    )

    saved_path = tts.speak("今天是不是很开心呀(laughs)，当然了！").save(output)

    assert saved_path == str(output)
    assert output.read_bytes() == b"demo-audio-bytes"
    assert api.uploads[0][1] == "voice_clone"
    assert api.voice_clone_calls[0]["text"] == "今天是不是很开心呀(laughs)，当然了！"
    assert api.voice_clone_calls[0]["voice_id"].startswith("VoiceHubClone_")
    assert api.voice_clone_calls[0]["language_boost"] == "Chinese"
    assert api.downloads == ["https://filecdn.minimax.chat/public/demo.mp3"]
    assert api.t2a_calls == []
    assert api.stream_calls == []
