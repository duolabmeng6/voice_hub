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


pytestmark = pytest.mark.skipif(
    os.environ.get("VOICE_HUB_RUN_LIVE_TESTS") != "1",
    reason="需要真实 MiMo 凭据和网络，默认跳过手工联网测试",
)


def test_mimo_builtin_voice_constants_match_docs():

    tts = voice_hub.Client()
    tts.add_speaker(
        "冰糖",
        voice_hub.MimoTTS(
            api_key=os.environ["MIMO_API_KEY"],
            base_url=os.environ.get("MIMO_BASE_URL"),
            voice=voice_hub.MimoVoice.BINGTANG,
            style="自然、平稳",
            format="wav",
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
            format="wav",
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
            format="wav",
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
            format="wav",
        ),
        default=True,
    )
    # tts.speaker('冰糖').speak("夜深了，城市还没有睡。").save("./tmp/out.wav")
    # tts.speaker('白桦').speak("夜深了，城市还没有睡。").save("./tmp/out2.wav")
    # tts.speaker('龙儿女生').speak("夜深了，城市还没有睡。").save("./tmp/out3.wav")
    tts.speaker('龙儿克隆').speak("夜深了，城市还没有睡。").save("./tmp/out4.wav")
