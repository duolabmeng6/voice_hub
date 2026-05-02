import voice_hub


class FakeEngine:
    def __init__(self, marker):
        self.marker = marker

    def speak(self, text, **overrides):
        suffix = overrides.get("suffix", "")
        audio = f"{self.marker}:{text}{suffix}".encode("utf-8")
        return voice_hub.Speech(audio, text=text, overrides=overrides)


def test_client_routes_default_speaker():
    tts = voice_hub.Client()
    tts.add_speaker("narrator", FakeEngine("a"), default=True)

    assert tts.bytes("你好", suffix="!") == "a:你好!".encode("utf-8")


def test_client_routes_named_speaker():
    tts = voice_hub.Client()
    tts.add_speaker("a", FakeEngine("a"), default=True)
    tts.add_speaker("b", FakeEngine("b"))

    assert tts.speaker("b").bytes("你好") == "b:你好".encode("utf-8")
