import pytest

import voice_hub
from voice_hub.providers.aliyun import (
    ALIYUN_COSYVOICE_CLONE_MODEL,
    ALIYUN_COSYVOICE_MODEL,
    ALIYUN_COSYVOICE_SYSTEM_VOICE_BY_ID,
    ALIYUN_COSYVOICE_SYSTEM_VOICE_IDS,
    ALIYUN_COSYVOICE_SYSTEM_VOICES,
    AliyunCosyVoice,
    AliyunCosyVoiceClone,
    AliyunCosyVoiceTTS,
)


class FakeAliyunCosyVoiceAPI:
    def __init__(self):
        self.syntheses = []
        self.created = []
        self.queries = []
        self.lists = []
        self.deleted = []
        self.uploads = []
        self.files = []

    def synthesize(self, data):
        self.syntheses.append(dict(data))
        return b"audio-bytes", "synth-request-1"

    def create_voice(self, data):
        self.created.append(dict(data))
        return {
            "output": {"voice_id": "myvoice-prefix-001"},
            "request_id": "create-request-1",
        }

    def query_voice(self, voice_id):
        self.queries.append(voice_id)
        return {
            "voice_id": voice_id,
            "status": "OK",
            "request_id": "query-request-1",
        }

    def list_voices(self, data):
        self.lists.append(dict(data))
        return [{"voice_id": "myvoice-prefix-001", "status": "OK"}]

    def delete_voice(self, voice_id):
        self.deleted.append(voice_id)
        return "delete-request-1"

    def upload_file(self, file_path, purpose):
        self.uploads.append((file_path, purpose))
        return {
            "request_id": "upload-request-1",
            "data": {
                "uploaded_files": [
                    {
                        "name": "sample.wav",
                        "file_id": "file-1",
                    }
                ],
                "failed_uploads": [],
            },
        }

    def get_file(self, file_id):
        self.files.append(file_id)
        return {
            "request_id": "file-request-1",
            "data": {
                "file_id": file_id,
                "name": "sample.wav",
                "size": 123,
                "md5": "abc",
                "url": "https://dashscope-file.example/sample.wav",
            },
        }


def test_aliyun_cosyvoice_system_voice_constants():
    assert AliyunCosyVoice.LONGANYANG == "longanyang"
    assert AliyunCosyVoice.LONGANHUAN == "longanhuan"
    assert AliyunCosyVoice.LONGANRAN_V3 == "longanran_v3"
    assert len(ALIYUN_COSYVOICE_SYSTEM_VOICES) == 87
    assert AliyunCosyVoice.LONGANYANG in ALIYUN_COSYVOICE_SYSTEM_VOICE_IDS
    assert AliyunCosyVoice.LONGANRAN_V3 in ALIYUN_COSYVOICE_SYSTEM_VOICE_IDS
    assert len(set(ALIYUN_COSYVOICE_SYSTEM_VOICE_IDS)) == 87
    assert ALIYUN_COSYVOICE_SYSTEM_VOICE_BY_ID["longanyang"].supports_instruction is True
    assert ALIYUN_COSYVOICE_SYSTEM_VOICE_BY_ID["longanran_v3"].note == "活泼质感女"


def test_aliyun_cosyvoice_system_tts_synthesizes_bytes():
    api = FakeAliyunCosyVoiceAPI()
    tts = AliyunCosyVoiceTTS(
        api_key="key",
        voice=AliyunCosyVoice.LONGANYANG,
        instruction="用活泼自然的语气讲解产品",
        api=api,
    )

    speech = tts.speak("你好，欢迎来到直播间。")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "AliyunCosyVoiceTTS"
    assert speech.metadata["request_id"] == "synth-request-1"
    call = api.syntheses[0]
    assert call["model"] == ALIYUN_COSYVOICE_MODEL
    assert call["voice"] == "longanyang"
    assert call["text"] == "你好，欢迎来到直播间。"
    assert call["format"] == "mp3"
    assert call["sample_rate"] == 24000
    assert call["instruction"] == "用活泼自然的语气讲解产品"


def test_aliyun_cosyvoice_build_payload_does_not_send_request():
    api = FakeAliyunCosyVoiceAPI()
    tts = AliyunCosyVoiceTTS(api_key="key", api=api)

    payload = tts.build_payload("hello", speech_rate=1.2, language_hints=["zh", "en"])

    assert api.syntheses == []
    assert payload["model"] == ALIYUN_COSYVOICE_MODEL
    assert payload["voice"] == "longanyang"
    assert payload["text"] == "hello"
    assert payload["speech_rate"] == 1.2
    assert payload["language_hints"] == ["zh", "en"]


def test_aliyun_cosyvoice_reads_env_api_key(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "env-key")
    tts = AliyunCosyVoiceTTS()

    assert tts.api.api_key == "env-key"


def test_aliyun_cosyvoice_rejects_unknown_override():
    tts = AliyunCosyVoiceTTS(api_key="key", api=FakeAliyunCosyVoiceAPI())

    with pytest.raises(TypeError, match="unsupported Aliyun CosyVoice override"):
        tts.bytes("你好", speed=1.2)


def test_aliyun_cosyvoice_clone_create_query_and_tts():
    api = FakeAliyunCosyVoiceAPI()
    clone = AliyunCosyVoiceClone(api_key="key", api=api)

    result = clone.create_voice(
        audio_url="https://example.com/sample.wav",
        prefix="myvoice",
        language_hints=["en"],
    )
    info = clone.query_voice(result.voice_id)
    voices = clone.list_voices(prefix="myvoice")
    request_id = clone.delete_voice(result.voice_id)
    tts = clone.tts(result.voice_id)
    speech = tts.speak("How is the weather today?")

    assert result.voice_id == "myvoice-prefix-001"
    assert result.request_id == "create-request-1"
    assert result.target_model == ALIYUN_COSYVOICE_CLONE_MODEL
    assert info["status"] == "OK"
    assert voices == [{"voice_id": "myvoice-prefix-001", "status": "OK"}]
    assert request_id == "delete-request-1"
    assert speech.bytes() == b"audio-bytes"
    assert api.created[0]["model"] == "voice-enrollment"
    assert api.created[0]["input"]["action"] == "create_voice"
    assert api.created[0]["input"]["target_model"] == ALIYUN_COSYVOICE_CLONE_MODEL
    assert api.created[0]["input"]["prefix"] == "myvoice"
    assert "max_prompt_audio_length" not in api.created[0]["input"]
    assert "enable_preprocess" not in api.created[0]["input"]
    assert api.syntheses[0]["voice"] == "myvoice-prefix-001"
    assert api.syntheses[0]["model"] == ALIYUN_COSYVOICE_CLONE_MODEL


def test_aliyun_cosyvoice_get_or_create_reuses_existing_voice():
    api = FakeAliyunCosyVoiceAPI()
    clone = AliyunCosyVoiceClone(api_key="key", api=api)

    result = clone.get_or_create_voice(
        audio_url="https://example.com/sample.wav",
        prefix="myvoice",
    )

    assert result.voice_id == "myvoice-prefix-001"
    assert result.reused is True
    assert result.status == "OK"
    assert api.lists[0]["prefix"] == "myvoice"
    assert api.created == []


def test_aliyun_cosyvoice_get_or_create_creates_when_missing():
    class EmptyListAPI(FakeAliyunCosyVoiceAPI):
        def list_voices(self, data):
            self.lists.append(dict(data))
            return []

    api = EmptyListAPI()
    clone = AliyunCosyVoiceClone(api_key="key", api=api)

    result = clone.get_or_create_voice(
        audio_url="https://example.com/sample.wav",
        language_hints=["zh"],
        max_prompt_audio_length=20.0,
        enable_preprocess=True,
    )

    assert result.voice_id == "myvoice-prefix-001"
    assert result.reused is False
    assert result.prefix == clone.default_prefix("https://example.com/sample.wav")
    assert api.created[0]["input"]["language_hints"] == ["zh"]
    assert api.created[0]["input"]["max_prompt_audio_length"] == 20.0
    assert api.created[0]["input"]["enable_preprocess"] is True


def test_aliyun_cosyvoice_get_or_create_from_file_uploads_when_missing(tmp_path):
    class EmptyListAPI(FakeAliyunCosyVoiceAPI):
        def list_voices(self, data):
            self.lists.append(dict(data))
            return []

    sample = tmp_path / "sample.wav"
    sample.write_bytes(b"fake-wav")
    api = EmptyListAPI()
    clone = AliyunCosyVoiceClone(api_key="key", api=api)

    result = clone.get_or_create_voice_from_file(
        sample,
        language_hints=["zh"],
        max_prompt_audio_length=10.0,
        enable_preprocess=False,
    )

    assert result.voice_id == "myvoice-prefix-001"
    assert result.reused is False
    assert result.audio_url == "https://dashscope-file.example/sample.wav"
    assert result.prefix == clone.default_prefix_for_file(sample)
    assert api.uploads[0] == (sample, "fine-tune")
    assert api.files[0] == "file-1"
    assert api.created[0]["input"]["url"] == "https://dashscope-file.example/sample.wav"
    assert api.created[0]["input"]["max_prompt_audio_length"] == 10.0
    assert api.created[0]["input"]["enable_preprocess"] is False


def test_aliyun_cosyvoice_get_or_create_from_file_reuses_without_upload(tmp_path):
    sample = tmp_path / "sample.wav"
    sample.write_bytes(b"fake-wav")
    api = FakeAliyunCosyVoiceAPI()
    clone = AliyunCosyVoiceClone(api_key="key", api=api)

    result = clone.get_or_create_voice_from_file(sample, prefix="myvoice")

    assert result.voice_id == "myvoice-prefix-001"
    assert result.reused is True
    assert api.lists[0]["prefix"] == "myvoice"
    assert api.uploads == []
    assert api.created == []


def test_aliyun_cosyvoice_tts_cloned_from_file_is_easy_entrypoint(tmp_path):
    class EmptyListAPI(FakeAliyunCosyVoiceAPI):
        def list_voices(self, data):
            self.lists.append(dict(data))
            return []

    sample = tmp_path / "sample.wav"
    sample.write_bytes(b"fake-wav")
    api = EmptyListAPI()

    tts = AliyunCosyVoiceTTS.cloned(
        api_key="key",
        sample=sample,
        language_hints=["zh"],
        api=api,
        wait=True,
        poll_interval=0,
    )
    speech = tts.speak("你好")

    assert tts.voice == "myvoice-prefix-001"
    assert tts.model == ALIYUN_COSYVOICE_CLONE_MODEL
    assert tts.voice_result is not None
    assert tts.voice_result.reused is False
    assert speech.bytes() == b"audio-bytes"
    assert api.uploads[0] == (sample, "fine-tune")
    assert api.queries[0] == "myvoice-prefix-001"
    assert api.syntheses[0]["voice"] == "myvoice-prefix-001"


def test_aliyun_cosyvoice_tts_cloned_from_url_reuses_existing_voice():
    api = FakeAliyunCosyVoiceAPI()

    tts = AliyunCosyVoiceTTS.cloned(
        api_key="key",
        audio_url="https://example.com/sample.wav",
        prefix="myvoice",
        api=api,
        wait=False,
    )

    assert tts.voice == "myvoice-prefix-001"
    assert tts.voice_result is not None
    assert tts.voice_result.reused is True
    assert api.created == []


def test_aliyun_cosyvoice_wait_until_ready_returns_ok():
    api = FakeAliyunCosyVoiceAPI()
    clone = AliyunCosyVoiceClone(api_key="key", api=api)

    info = clone.wait_until_ready("voice-1", max_attempts=1, poll_interval=0)

    assert info["status"] == "OK"
    assert api.queries[0] == "voice-1"
