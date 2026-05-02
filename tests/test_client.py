import voice_hub as vh


class FakeEngine:
    def __init__(self, marker):
        self.marker = marker

    def speak(self, text, **overrides):
        return vh.Speech(FakeProvider(self.marker), text, overrides)


class FakeProvider:
    def __init__(self, marker):
        self.marker = marker

    def synthesize(self, text, **overrides):
        suffix = overrides.get("suffix", "")
        return f"{self.marker}:{text}{suffix}".encode("utf-8")

    def stream_synthesize(self, text, **overrides):
        yield self.synthesize(text, **overrides)


def test_client_routes_default_speaker():
    tts = vh.Client()
    tts.add_speaker("narrator", FakeEngine("a"), default=True)

    assert tts.bytes("你好", suffix="!") == "a:你好!".encode("utf-8")


def test_client_routes_named_speaker():
    tts = vh.Client()
    tts.add_speaker("a", FakeEngine("a"), default=True)
    tts.add_speaker("b", FakeEngine("b"))

    assert tts.speaker("b").bytes("你好") == "b:你好".encode("utf-8")
