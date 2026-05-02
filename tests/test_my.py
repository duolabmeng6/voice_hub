import os
import time
from pathlib import Path

import pytest
import voice_hub


def load_env(path: Path) -> None:
    if not path.exists():
        return

    env_values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            env_values[key] = value

    for key, value in env_values.items():
        os.environ.setdefault(key, value)


load_env(Path(__file__).resolve().parents[1] / ".env")


live_only = pytest.mark.skipif(
    os.environ.get("VOICE_HUB_RUN_LIVE_TESTS") != "1",
    reason="set VOICE_HUB_RUN_LIVE_TESTS=1 to run live provider tests",
)


def _fail_without_secret(exc: Exception) -> None:
    message = str(exc)
    for key in ("MINIMAX_KEY", "MINIMAX_KEY2", "MIMO_API_KEY", "MIMO_TOKEN_KEY"):
        secret = os.environ.get(key)
        if secret:
            message = message.replace(secret, f"<redacted {key}>")
    pytest.fail(message, pytrace=False)


@live_only
def test_mimo_voice_hub():
    tts = voice_hub.Client()
    tts.add_speaker(
        "冰糖",
        voice_hub.MimoTTS(
            api_key=os.environ["MIMO_API_KEY"],
            base_url=os.environ.get("MIMO_BASE_URL"),
            voice=voice_hub.MimoVoice.BINGTANG,
            style="自然、平稳",
        ),
        default=True,
    )

    tts.add_speaker(
        "白桦",
        voice_hub.MimoTTS(
            api_key=os.environ["MIMO_API_KEY"],
            base_url=os.environ.get("MIMO_BASE_URL"),
            voice=voice_hub.MimoVoice.BAIHUA,
            style="自然、平稳",
        ),
        default=True,
    )
    tts.add_speaker(
        "龙儿女生",
        voice_hub.MimoTTS.designed(
            api_key=os.environ["MIMO_TOKEN_KEY"],
            base_url=os.environ.get("MIMO_TOKEN_BASE_URL"),
            prompt="年轻女性，温柔、松弛、有轻微气声",
            style="自然、平稳",
        ),
        default=True,
    )
    tts.add_speaker(
        "龙儿克隆",
        voice_hub.MimoTTS.cloned(
            api_key=os.environ["MIMO_TOKEN_KEY"],
            base_url=os.environ.get("MIMO_TOKEN_BASE_URL"),
            sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
            style="自然、快速讲话",
        ),
        default=True,
    )
    try:
        tts.speaker('冰糖').speak("夜深了，城市还没有睡。").save("./tmp/out.wav")
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)
    # tts.speaker('白桦').speak("夜深了，城市还没有睡。").save("./tmp/out2.wav")
    # tts.speaker('龙儿女生').speak("夜深了，城市还没有睡。").save("./tmp/out3.wav")
    # tts.speaker('龙儿克隆').speak("夜深了，城市还没有睡。").save("./tmp/out4.wav")


@live_only
def test_mimo_obj():
    tts = voice_hub.MimoTTS(
        api_key=os.environ["MIMO_API_KEY"],
        base_url=os.environ.get("MIMO_BASE_URL"),
        voice=voice_hub.MimoVoice.BINGTANG,
        style="自然、平稳",
    )
    try:
        tts.speak("夜深了，城市还没有睡。").save("./tmp/out.wav")
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)


@live_only
def test_mimo_designed():
    tts = voice_hub.MimoTTS.designed(
        api_key=os.environ["MIMO_API_KEY"],
        base_url=os.environ.get("MIMO_BASE_URL"),
        prompt="男性,自然、平稳",
    )
    try:
        tts.speak("夜深了，城市还没有睡。").save("./tmp/out.wav")
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)


@live_only
def test_mimo_cloned():
    tts = voice_hub.MimoTTS.cloned(
        api_key=os.environ["MIMO_TOKEN_KEY"],
        base_url=os.environ.get("MIMO_TOKEN_BASE_URL"),
        sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
        style="自然、快速讲话",
    )
    try:
        tts.speak("夜深了，城市还没有睡。").save("./tmp/out.wav")
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)


@live_only
def test_minimax_obj():
    tts = voice_hub.MinimaxTTS(
        api_key=os.environ["MINIMAX_KEY"],
        voice=voice_hub.MinimaxVoice.MALE_QN_QINGSE,
        emotion="happy",
        format="mp3",
    )
    try:
        tts.speak("今天是不是很开心呀(laughs)，当然了！").save("./tmp/minimax.mp3")
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)


@live_only
def test_minimax_voice_clone_preview_only():
    tts = voice_hub.MinimaxTTS.cloned(
        api_key=os.environ["MINIMAX_KEY2"],
        sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
        voice_id=f"VoiceHubClone{int(time.time())}{os.getpid()}",
        model=voice_hub.MINIMAX_VOICE_CLONE_MODEL,
        need_noise_reduction=True,
        need_volume_normalization=True,
        language_boost="Chinese",
    )
    try:
        speech = tts.speak("今天是不是很开心呀(laughs)，当然了！")
        speech.save("./tmp/minimax-clone-preview.mp3")
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)

    assert speech.metadata["voice_id"].startswith("VoiceHubClone")
    assert speech.metadata["endpoint"] == "voice_clone"
    assert Path("./tmp/minimax-clone-preview.mp3").exists()
