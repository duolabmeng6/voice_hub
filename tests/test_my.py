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



def test_mimo_builtin_voice_constants_match_docs():

    tts = voice_hub.Client()
    tts.add_speaker(
        "narrator",
        voice_hub.MimoTTS(
            api_key=os.environ["MIMO_API_KEY"],
            base_url=os.environ.get("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"),
            voice=voice_hub.MimoVoice.BINGTANG,
            style="自然、平稳",
            format="wav",
        ),
        default=True,
    )

    tts.speak("夜深了，城市还没有睡。").save("out.wav")
