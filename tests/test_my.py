import os
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
    tts.speaker('冰糖').speak("夜深了，城市还没有睡。").save("./tmp/out.wav")
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
    tts.speak("夜深了，城市还没有睡。").save("./tmp/out.wav")


@live_only
def test_mimo_designed():
    tts = voice_hub.MimoTTS.designed(
        api_key=os.environ["MIMO_API_KEY"],
        base_url=os.environ.get("MIMO_BASE_URL"),
        prompt="男性,自然、平稳",
    )
    tts.speak("夜深了，城市还没有睡。").save("./tmp/out.wav")


@live_only
def test_mimo_cloned():
    tts = voice_hub.MimoTTS.cloned(
        api_key=os.environ["MIMO_TOKEN_KEY"],
        base_url=os.environ.get("MIMO_TOKEN_BASE_URL"),
        sample=voice_hub.VoiceSample("./tmp/voice-clones/vc30.wav"),
        style="自然、快速讲话",
    )
    tts.speak("夜深了，城市还没有睡。").save("./tmp/out.wav")


@live_only
def test_minimax_obj():
    tts = voice_hub.MinimaxTTS(
        api_key=os.environ["MINIMAX_KEY"],
        voice=voice_hub.MinimaxVoice.MALE_QN_QINGSE,
        emotion="happy",
        format="mp3",
    )
    tts.speak("今天是不是很开心呀(laughs)，当然了！").save("./tmp/minimax.mp3")
