from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Iterator, Mapping, Optional

from ..errors import ConfigurationError, ProviderError
from ..sample import VoiceSample
from .base import BaseTTS


MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"
MIMO_TTS_MODEL = "mimo-v2.5-tts"
MIMO_VOICE_DESIGN_MODEL = "mimo-v2.5-tts-voicedesign"
MIMO_VOICE_CLONE_MODEL = "mimo-v2.5-tts-voiceclone"


@dataclass(frozen=True)
class MimoVoiceSpec:
    name: str
    voice_id: str
    language: str
    gender: str | None = None


class MimoVoice:
    """MiMo 官方预置音色 ID 常量。"""

    DEFAULT = "mimo_default"
    BINGTANG = "冰糖"
    MOLI = "茉莉"
    SUDA = "苏打"
    BAIHUA = "白桦"
    MIA = "Mia"
    CHLOE = "Chloe"
    MILO = "Milo"
    DEAN = "Dean"


MIMO_BUILTIN_VOICES = (
    MimoVoiceSpec("MiMo-默认", MimoVoice.DEFAULT, "cluster-dependent"),
    MimoVoiceSpec("冰糖", MimoVoice.BINGTANG, "Chinese", "Female"),
    MimoVoiceSpec("茉莉", MimoVoice.MOLI, "Chinese", "Female"),
    MimoVoiceSpec("苏打", MimoVoice.SUDA, "Chinese", "Male"),
    MimoVoiceSpec("白桦", MimoVoice.BAIHUA, "Chinese", "Male"),
    MimoVoiceSpec("Mia", MimoVoice.MIA, "English", "Female"),
    MimoVoiceSpec("Chloe", MimoVoice.CHLOE, "English", "Female"),
    MimoVoiceSpec("Milo", MimoVoice.MILO, "English", "Male"),
    MimoVoiceSpec("Dean", MimoVoice.DEAN, "English", "Male"),
)
MIMO_BUILTIN_VOICE_IDS = tuple(voice.voice_id for voice in MIMO_BUILTIN_VOICES)
MIMO_BUILTIN_VOICE_BY_ID = MappingProxyType(
    {voice.voice_id: voice for voice in MIMO_BUILTIN_VOICES}
)


@dataclass(frozen=True)
class MimoRequest:
    model: str
    messages: list[dict[str, str]]
    audio: dict[str, str]
    stream: bool = False

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "model": self.model,
            "messages": self.messages,
            "audio": self.audio,
        }
        if self.stream:
            payload["stream"] = True
        return payload


class MimoHTTPTransport:
    """基于标准库的 MiMo HTTP 传输层。"""

    def post(
        self,
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
        timeout: float,
    ) -> Mapping[str, Any]:
        request = self._build_request(base_url, api_key, payload)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"MiMo API request failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"MiMo API request failed: {exc.reason}") from exc

        return json.loads(body)

    def stream(
        self,
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
        timeout: float,
    ) -> Iterable[Mapping[str, Any]]:
        request = self._build_request(base_url, api_key, payload)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                for raw_line in response:
                    event = self._parse_sse_line(raw_line)
                    if event is not None:
                        yield event
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ProviderError(f"MiMo API stream failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"MiMo API stream failed: {exc.reason}") from exc

    @staticmethod
    def _build_request(
        base_url: str,
        api_key: str,
        payload: Mapping[str, object],
    ) -> urllib.request.Request:
        url = f"{base_url.rstrip('/')}/chat/completions"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        return urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "api-key": api_key,
            },
        )

    @staticmethod
    def _parse_sse_line(raw_line: bytes) -> Optional[Mapping[str, Any]]:
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line or not line.startswith("data:"):
            return None

        data = line.removeprefix("data:").strip()
        if data == "[DONE]":
            return None
        return json.loads(data)


class MimoTTS(BaseTTS):
    """小米 MiMo-V2.5-TTS 系列 provider。"""

    def __init__(
        self,
        api_key: str,
        voice: str = "mimo_default",
        style: str | None = None,
        format: str = "wav",
        model: str = MIMO_TTS_MODEL,
        base_url: str = MIMO_BASE_URL,
        transport: MimoHTTPTransport | None = None,
        timeout: float = 60,
        voice_design_prompt: str | None = None,
        voice_sample: VoiceSample | str | None = None,
    ) -> None:
        self.api_key = api_key
        self.voice = voice
        self.style = style
        self.format = format
        self.model = model
        self.base_url = base_url
        self.transport = transport or MimoHTTPTransport()
        self.timeout = timeout
        self.voice_design_prompt = voice_design_prompt
        self.voice_sample = self._normalize_sample(voice_sample)
        self._validate_config()

    @classmethod
    def designed(
        cls,
        api_key: str,
        prompt: str = "",
        style: str | None = None,
        format: str = "wav",
        **kwargs: object,
    ) -> "MimoTTS":
        return cls(
            api_key=api_key,
            style=style,
            format=format,
            model=MIMO_VOICE_DESIGN_MODEL,
            voice_design_prompt=prompt,
            **kwargs,
        )

    @classmethod
    def cloned(
        cls,
        api_key: str,
        sample: VoiceSample | str | None = None,
        style: str | None = None,
        format: str = "wav",
        **kwargs: object,
    ) -> "MimoTTS":
        return cls(
            api_key=api_key,
            style=style,
            format=format,
            model=MIMO_VOICE_CLONE_MODEL,
            voice_sample=sample,
            **kwargs,
        )

    def synthesize(self, text: str, **overrides: object) -> bytes:
        request = self._build_request(text, stream=False, overrides=overrides)
        response = self.transport.post(
            self.base_url,
            self.api_key,
            request.to_payload(),
            self.timeout,
        )
        return self._decode_message_audio(response)

    def stream_synthesize(self, text: str, **overrides: object) -> Iterable[bytes]:
        stream_overrides = dict(overrides)
        stream_overrides.setdefault("format", "pcm16")

        request = self._build_request(text, stream=True, overrides=stream_overrides)
        events = self.transport.stream(
            self.base_url,
            self.api_key,
            request.to_payload(),
            self.timeout,
        )
        return self._iter_audio_chunks(events)

    def _build_request(
        self,
        text: str,
        stream: bool,
        overrides: Mapping[str, object],
    ) -> MimoRequest:
        options = self._merged_options(overrides)
        messages = self._build_messages(text, options)
        audio = self._build_audio(options)
        return MimoRequest(
            model=str(options["model"]),
            messages=messages,
            audio=audio,
            stream=stream,
        )

    def _merged_options(self, overrides: Mapping[str, object]) -> dict[str, object]:
        options: dict[str, object] = {
            "model": self.model,
            "voice": self.voice,
            "style": self.style,
            "speed": None,
            "format": self.format,
            "voice_design_prompt": self.voice_design_prompt,
            "voice_sample": self.voice_sample,
        }

        allowed_keys = set(options)
        unknown_keys = set(overrides) - allowed_keys
        if unknown_keys:
            unknown = ", ".join(sorted(unknown_keys))
            raise TypeError(f"unsupported MiMo override(s): {unknown}")

        options.update({key: value for key, value in overrides.items() if value is not None})
        return options

    def _build_messages(self, text: str, options: Mapping[str, object]) -> list[dict[str, str]]:
        model = str(options["model"])
        user_content = self._user_content(options)

        if model == MIMO_VOICE_DESIGN_MODEL and not user_content:
            raise ConfigurationError("voice design prompt is required")

        messages: list[dict[str, str]] = []
        if user_content or model in {MIMO_VOICE_DESIGN_MODEL, MIMO_VOICE_CLONE_MODEL}:
            messages.append({"role": "user", "content": user_content})
        messages.append({"role": "assistant", "content": text})
        return messages

    @staticmethod
    def _user_content(options: Mapping[str, object]) -> str:
        prompt = options.get("voice_design_prompt")
        style = options.get("style")
        speed = options.get("speed")

        parts = [str(value).strip() for value in (prompt, style) if value]
        if speed is not None:
            parts.append(_speed_instruction(speed))
        return "\n\n".join(part for part in parts if part)

    def _build_audio(self, options: Mapping[str, object]) -> dict[str, str]:
        model = str(options["model"])
        audio = {"format": str(options["format"])}

        if model == MIMO_TTS_MODEL:
            audio["voice"] = str(options["voice"])
            return audio

        if model == MIMO_VOICE_DESIGN_MODEL:
            return audio

        if model == MIMO_VOICE_CLONE_MODEL:
            sample = options.get("voice_sample")
            if not isinstance(sample, VoiceSample):
                raise ConfigurationError("voice clone sample is required")
            audio["voice"] = sample.to_data_uri()
            return audio

        raise ConfigurationError(f"unsupported MiMo model: {model}")

    @staticmethod
    def _decode_message_audio(response: Mapping[str, Any]) -> bytes:
        try:
            audio_data = response["choices"][0]["message"]["audio"]["data"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"MiMo API response missing audio data: {response}") from exc
        return base64.b64decode(audio_data)

    @staticmethod
    def _iter_audio_chunks(events: Iterable[Mapping[str, Any]]) -> Iterator[bytes]:
        for event in events:
            try:
                choices = event.get("choices", [])
                if not choices:
                    continue
                audio = choices[0].get("delta", {}).get("audio")
                if not audio:
                    continue
                yield base64.b64decode(audio["data"])
            except (KeyError, TypeError) as exc:
                raise ProviderError(f"MiMo stream chunk missing audio data: {event}") from exc

    @staticmethod
    def _normalize_sample(sample: VoiceSample | str | None) -> VoiceSample | None:
        if sample is None or isinstance(sample, VoiceSample):
            return sample
        return VoiceSample(sample)

    def _validate_config(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("MiMo api_key is required")
        if not self.base_url or not self.base_url.strip():
            raise ConfigurationError("MiMo base_url is required")
        if self.model == MIMO_VOICE_DESIGN_MODEL and not self.voice_design_prompt:
            raise ConfigurationError("voice design prompt is required")
        if self.model == MIMO_VOICE_CLONE_MODEL and not self.voice_sample:
            raise ConfigurationError("voice clone sample is required")


def _speed_instruction(speed: object) -> str:
    try:
        speed_value = float(speed)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"speed must be a number, got: {speed}") from exc

    if speed_value <= 0:
        raise ConfigurationError("speed must be greater than 0")
    if speed_value == 1:
        return "Use a natural default speaking speed."
    if speed_value > 1:
        return f"Speak at about {speed_value:g}x normal speed."
    return f"Speak at about {speed_value:g}x normal speed, slower than usual."
