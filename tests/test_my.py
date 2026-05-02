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
    # os.environ.get("VOICE_HUB_RUN_LIVE_TESTS") != "1",
    False,
    reason="set VOICE_HUB_RUN_LIVE_TESTS=1 to run live provider tests",
)


def _fail_without_secret(exc: Exception) -> None:
    message = str(exc)
    for key in (
        "DASHSCOPE_API_KEY",
        "MINIMAX_KEY",
        "MINIMAX_KEY2",
        "MIMO_API_KEY",
        "MIMO_TOKEN_KEY",
        "ZHIPUAI_API_KEY",
    ):
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

    assert speech.metadata["voice_id"].startswith("VoiceHubClone_")
    assert speech.metadata["endpoint"] == "voice_clone"
    assert Path("./tmp/minimax-clone-preview.mp3").exists()


@live_only
def test_glm_tts_system_voice():
    tts = voice_hub.GLMTTS(
        api_key=os.environ["ZHIPUAI_API_KEY"],
        voice=voice_hub.GLMVoice.FEMALE,
        response_format="wav",
        watermark_enabled=False,
        timeout=120,
    )
    output = Path("./tmp/glm_tts.wav")

    try:
        speech = tts.speak("夜深了，城市还没有睡。")
        saved = speech.save(output)
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)

    print(
        {
            "saved": saved,
            "audio_bytes": len(speech.bytes()),
            "model": speech.metadata.get("model"),
            "voice": speech.metadata.get("voice"),
            "response_format": speech.metadata.get("response_format"),
        }
    )


@live_only
def test_aliyun_qwen3_tts_instruct_flash_system_voice():
    tts = voice_hub.AliyunTTS(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        voice=voice_hub.AliyunVoice.CHERRY,
        instructions="语速较快，带有明显的上扬语调，适合介绍时尚产品",
        timeout=120,
    )
    output = Path("./tmp/aliyun_qwen3_tts.wav")

    try:
        speech = tts.speak(
            "那我来给大家推荐一款T恤，这款呢真的是超级好看，"
            "这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入。"
        )
        saved = speech.save(output)
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)

    print(
        {
            "saved": saved,
            "audio_bytes": len(speech.bytes()),
            "request_id": speech.metadata.get("request_id"),
            "model": speech.metadata.get("model"),
        }
    )


@live_only
def test_aliyun_cosyvoice_system_voice():
    tts = voice_hub.AliyunCosyVoiceTTS(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        voice=voice_hub.AliyunCosyVoice.LONGANYANG,
        model=voice_hub.ALIYUN_COSYVOICE_MODEL,
        timeout=120,
    )
    output = Path("./tmp/aliyun_cosyvoice_system.mp3")

    try:
        speech = tts.speak("那我来给大家推荐一款T恤，这款颜色很显气质。")
        saved = speech.save(output)
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)

    print(
        {
            "saved": saved,
            "audio_bytes": len(speech.bytes()),
            "request_id": speech.metadata.get("request_id"),
            "model": speech.metadata.get("model"),
            "voice": speech.metadata.get("voice"),
        }
    )


@live_only
def test_aliyun_cosyvoice_clone_voice_id_tts():
    voice_id = os.environ["ALIYUN_COSYVOICE_VOICE_ID"]
    tts = voice_hub.AliyunCosyVoiceTTS(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        voice=voice_id,
        model=voice_hub.ALIYUN_COSYVOICE_CLONE_MODEL,
        timeout=120,
    )
    output = Path("./tmp/aliyun_cosyvoice_clone.mp3")

    try:
        speech = tts.speak("How is the weather today?")
        saved = speech.save(output)
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)

    print(
        {
            "saved": saved,
            "audio_bytes": len(speech.bytes()),
            "request_id": speech.metadata.get("request_id"),
            "model": speech.metadata.get("model"),
            "voice": speech.metadata.get("voice"),
        }
    )


@live_only
def test_aliyun_cosyvoice_clone_create_and_tts():
    clone = voice_hub.AliyunCosyVoiceClone(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        target_model=voice_hub.ALIYUN_COSYVOICE_CLONE_MODEL,
        timeout=120,
    )
    output = Path("./tmp/aliyun_cosyvoice_clone_created.mp3")

    try:
        result = clone.get_or_create_voice(
            audio_url=os.environ["ALIYUN_COSYVOICE_AUDIO_URL"],
            prefix=os.environ.get("ALIYUN_COSYVOICE_PREFIX"),
            language_hints=[os.environ.get("ALIYUN_COSYVOICE_LANGUAGE", "zh")],
            max_prompt_audio_length=float(os.environ["ALIYUN_COSYVOICE_MAX_PROMPT_AUDIO_LENGTH"])
            if os.environ.get("ALIYUN_COSYVOICE_MAX_PROMPT_AUDIO_LENGTH")
            else None,
            enable_preprocess=os.environ.get("ALIYUN_COSYVOICE_ENABLE_PREPROCESS") == "1"
            if os.environ.get("ALIYUN_COSYVOICE_ENABLE_PREPROCESS") is not None
            else None,
        )
        info = clone.wait_until_ready(
            result.voice_id,
            max_attempts=int(os.environ.get("ALIYUN_COSYVOICE_MAX_ATTEMPTS", "30")),
            poll_interval=float(os.environ.get("ALIYUN_COSYVOICE_POLL_INTERVAL", "10")),
        )
        speech = clone.tts(result.voice_id).speak("How is the weather today?")
        saved = speech.save(output)
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)

    print(
        {
            "voice_id": result.voice_id,
            "create_request_id": result.request_id,
            "reused": result.reused,
            "status": info.get("status"),
            "saved": saved,
            "audio_bytes": len(speech.bytes()),
            "synth_request_id": speech.metadata.get("request_id"),
        }
    )


@live_only
def test_aliyun_cosyvoice_clone_from_file_and_tts():
    output = Path("./tmp/aliyun_cosyvoice_clone_from_file.mp3")
    sample = Path(os.environ.get("ALIYUN_COSYVOICE_SAMPLE_FILE", "./tmp/voice-clones/vc30.wav"))

    try:
        tts = voice_hub.AliyunCosyVoiceTTS.cloned(
            api_key=os.environ["DASHSCOPE_API_KEY"],
            sample=sample,
            prefix=os.environ.get("ALIYUN_COSYVOICE_PREFIX"),
            language_hints=[os.environ.get("ALIYUN_COSYVOICE_LANGUAGE", "zh")],
            max_prompt_audio_length=float(os.environ["ALIYUN_COSYVOICE_MAX_PROMPT_AUDIO_LENGTH"])
            if os.environ.get("ALIYUN_COSYVOICE_MAX_PROMPT_AUDIO_LENGTH")
            else None,
            enable_preprocess=os.environ.get("ALIYUN_COSYVOICE_ENABLE_PREPROCESS") == "1"
            if os.environ.get("ALIYUN_COSYVOICE_ENABLE_PREPROCESS") is not None
            else None,
            timeout=120,
            max_attempts=int(os.environ.get("ALIYUN_COSYVOICE_MAX_ATTEMPTS", "30")),
            poll_interval=float(os.environ.get("ALIYUN_COSYVOICE_POLL_INTERVAL", "10")),
        )
        speech = tts.speak("恭喜，已成功复刻并合成了属于自己的声音。")
        saved = speech.save(output)
    except voice_hub.VoiceHubError as exc:
        _fail_without_secret(exc)

    result = tts.voice_result
    print(
        {
            "sample": str(sample),
            "voice_id": result.voice_id if result else tts.voice,
            "reused": result.reused if result else None,
            "saved": saved,
            "audio_bytes": len(speech.bytes()),
            "synth_request_id": speech.metadata.get("request_id"),
        }
    )
