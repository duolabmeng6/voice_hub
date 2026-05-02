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


class FakeCosyVoiceTransport:
    def __init__(self):
        self.syntheses = []
        self.created = []
        self.queries = []
        self.lists = []
        self.deleted = []
        self.uploads = []
        self.files = []

    def synthesize(self, **kwargs):
        self.syntheses.append(kwargs)
        return b"audio-bytes", "synth-request-1"

    def create_voice(self, **kwargs):
        self.created.append(kwargs)
        return "myvoice-prefix-001", "create-request-1"

    def query_voice(self, **kwargs):
        self.queries.append(kwargs)
        return {
            "voice_id": kwargs["voice_id"],
            "status": "OK",
            "request_id": "query-request-1",
        }

    def list_voices(self, **kwargs):
        self.lists.append(kwargs)
        return [{"voice_id": "myvoice-prefix-001", "status": "OK"}]

    def delete_voice(self, **kwargs):
        self.deleted.append(kwargs)
        return "delete-request-1"

    def upload_file(self, **kwargs):
        self.uploads.append(kwargs)
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

    def get_file(self, **kwargs):
        self.files.append(kwargs)
        return {
            "request_id": "file-request-1",
            "data": {
                "file_id": kwargs["file_id"],
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
    transport = FakeCosyVoiceTransport()
    tts = AliyunCosyVoiceTTS(
        api_key="key",
        voice=AliyunCosyVoice.LONGANYANG,
        instruction="用活泼自然的语气讲解产品",
        transport=transport,
    )

    speech = tts.speak("你好，欢迎来到直播间。")

    assert speech.bytes() == b"audio-bytes"
    assert speech.metadata["provider"] == "AliyunCosyVoiceTTS"
    assert speech.metadata["request_id"] == "synth-request-1"
    call = transport.syntheses[0]
    assert call["api_key"] == "key"
    assert call["model"] == ALIYUN_COSYVOICE_MODEL
    assert call["voice"] == "longanyang"
    assert call["text"] == "你好，欢迎来到直播间。"
    assert call["format"] == "mp3"
    assert call["sample_rate"] == 24000
    assert call["instruction"] == "用活泼自然的语气讲解产品"


def test_aliyun_cosyvoice_build_payload_does_not_send_request():
    transport = FakeCosyVoiceTransport()
    tts = AliyunCosyVoiceTTS(api_key="key", transport=transport)

    payload = tts.build_payload("hello", speech_rate=1.2, language_hints=["zh", "en"])

    assert transport.syntheses == []
    assert payload["model"] == ALIYUN_COSYVOICE_MODEL
    assert payload["voice"] == "longanyang"
    assert payload["text"] == "hello"
    assert payload["speech_rate"] == 1.2
    assert payload["language_hints"] == ["zh", "en"]


def test_aliyun_cosyvoice_reads_env_api_key(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "env-key")
    transport = FakeCosyVoiceTransport()
    tts = AliyunCosyVoiceTTS(transport=transport)

    tts.bytes("你好")

    assert transport.syntheses[0]["api_key"] == "env-key"


def test_aliyun_cosyvoice_rejects_unknown_override():
    tts = AliyunCosyVoiceTTS(api_key="key", transport=FakeCosyVoiceTransport())

    with pytest.raises(TypeError, match="unsupported Aliyun CosyVoice override"):
        tts.bytes("你好", speed=1.2)


def test_aliyun_cosyvoice_clone_create_query_and_tts():
    transport = FakeCosyVoiceTransport()
    clone = AliyunCosyVoiceClone(api_key="key", transport=transport)

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
    assert transport.created[0]["target_model"] == ALIYUN_COSYVOICE_CLONE_MODEL
    assert transport.created[0]["prefix"] == "myvoice"
    assert transport.created[0]["max_prompt_audio_length"] is None
    assert transport.created[0]["enable_preprocess"] is None
    assert transport.syntheses[0]["voice"] == "myvoice-prefix-001"
    assert transport.syntheses[0]["model"] == ALIYUN_COSYVOICE_CLONE_MODEL


def test_aliyun_cosyvoice_get_or_create_reuses_existing_voice():
    transport = FakeCosyVoiceTransport()
    clone = AliyunCosyVoiceClone(api_key="key", transport=transport)

    result = clone.get_or_create_voice(
        audio_url="https://example.com/sample.wav",
        prefix="myvoice",
    )

    assert result.voice_id == "myvoice-prefix-001"
    assert result.reused is True
    assert result.status == "OK"
    assert transport.lists[0]["prefix"] == "myvoice"
    assert transport.created == []


def test_aliyun_cosyvoice_get_or_create_creates_when_missing():
    class EmptyListTransport(FakeCosyVoiceTransport):
        def list_voices(self, **kwargs):
            self.lists.append(kwargs)
            return []

    transport = EmptyListTransport()
    clone = AliyunCosyVoiceClone(api_key="key", transport=transport)

    result = clone.get_or_create_voice(
        audio_url="https://example.com/sample.wav",
        language_hints=["zh"],
        max_prompt_audio_length=20.0,
        enable_preprocess=True,
    )

    assert result.voice_id == "myvoice-prefix-001"
    assert result.reused is False
    assert result.prefix == clone.default_prefix("https://example.com/sample.wav")
    assert transport.created[0]["language_hints"] == ["zh"]
    assert transport.created[0]["max_prompt_audio_length"] == 20.0
    assert transport.created[0]["enable_preprocess"] is True


def test_aliyun_cosyvoice_get_or_create_from_file_uploads_when_missing(tmp_path):
    class EmptyListTransport(FakeCosyVoiceTransport):
        def list_voices(self, **kwargs):
            self.lists.append(kwargs)
            return []

    sample = tmp_path / "sample.wav"
    sample.write_bytes(b"fake-wav")
    transport = EmptyListTransport()
    clone = AliyunCosyVoiceClone(api_key="key", transport=transport)

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
    assert transport.uploads[0]["file_path"] == sample
    assert transport.uploads[0]["purpose"] == "fine-tune"
    assert transport.files[0]["file_id"] == "file-1"
    assert transport.created[0]["audio_url"] == "https://dashscope-file.example/sample.wav"
    assert transport.created[0]["max_prompt_audio_length"] == 10.0
    assert transport.created[0]["enable_preprocess"] is False


def test_aliyun_cosyvoice_get_or_create_from_file_reuses_without_upload(tmp_path):
    sample = tmp_path / "sample.wav"
    sample.write_bytes(b"fake-wav")
    transport = FakeCosyVoiceTransport()
    clone = AliyunCosyVoiceClone(api_key="key", transport=transport)

    result = clone.get_or_create_voice_from_file(sample, prefix="myvoice")

    assert result.voice_id == "myvoice-prefix-001"
    assert result.reused is True
    assert transport.lists[0]["prefix"] == "myvoice"
    assert transport.uploads == []
    assert transport.created == []


def test_aliyun_cosyvoice_wait_until_ready_returns_ok():
    transport = FakeCosyVoiceTransport()
    clone = AliyunCosyVoiceClone(api_key="key", transport=transport)

    info = clone.wait_until_ready("voice-1", max_attempts=1, poll_interval=0)

    assert info["status"] == "OK"
    assert transport.queries[0]["voice_id"] == "voice-1"
