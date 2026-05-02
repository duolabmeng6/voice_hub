from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class AliyunVoiceSpec:
    name: str
    voice_id: str
    note: str | None = None


class AliyunVoice:
    """阿里云 Qwen TTS 官方系统音色 ID 常量。"""

    CHERRY = "Cherry"
    SERENA = "Serena"
    ETHAN = "Ethan"
    CHELSIE = "Chelsie"
    MOMO = "Momo"
    VIVIAN = "Vivian"
    MOON = "Moon"
    MAIA = "Maia"
    KAI = "Kai"
    NOFISH = "Nofish"
    BELLA = "Bella"
    JENNIFER = "Jennifer"
    RYAN = "Ryan"
    KATERINA = "Katerina"
    AIDEN = "Aiden"
    ELDRIC_SAGE = "Eldric Sage"
    MIA = "Mia"
    MOCHI = "Mochi"
    BELLONA = "Bellona"
    VINCENT = "Vincent"
    BUNNY = "Bunny"
    NEIL = "Neil"
    ELIAS = "Elias"
    ARTHUR = "Arthur"
    NINI = "Nini"
    EBONA = "Ebona"
    SEREN = "Seren"
    PIP = "Pip"
    STELLA = "Stella"
    BODEGA = "Bodega"
    SONRISA = "Sonrisa"
    ALEK = "Alek"
    DOLCE = "Dolce"
    SOHEE = "Sohee"
    ONO_ANNA = "Ono Anna"
    LENN = "Lenn"
    EMILIEN = "Emilien"
    ANDRE = "Andre"
    RADIO_GOL = "Radio Gol"
    JADA = "Jada"
    DYLAN = "Dylan"
    LI = "Li"
    MARCUS = "Marcus"
    ROY = "Roy"
    PETER = "Peter"
    SUNNY = "Sunny"
    ERIC = "Eric"
    ROCKY = "Rocky"
    KIKI = "Kiki"


ALIYUN_SYSTEM_VOICES = (
    AliyunVoiceSpec("芊悦", AliyunVoice.CHERRY, "年轻女声，阳光自然"),
    AliyunVoiceSpec("Serena", AliyunVoice.SERENA),
    AliyunVoiceSpec("晨煦", AliyunVoice.ETHAN, "年轻男声，温暖有活力"),
    AliyunVoiceSpec("Chelsie", AliyunVoice.CHELSIE),
    AliyunVoiceSpec("Momo", AliyunVoice.MOMO),
    AliyunVoiceSpec("Vivian", AliyunVoice.VIVIAN),
    AliyunVoiceSpec("Moon", AliyunVoice.MOON),
    AliyunVoiceSpec("Maia", AliyunVoice.MAIA),
    AliyunVoiceSpec("Kai", AliyunVoice.KAI),
    AliyunVoiceSpec("不吃鱼", AliyunVoice.NOFISH),
    AliyunVoiceSpec("Bella", AliyunVoice.BELLA),
    AliyunVoiceSpec("Jennifer", AliyunVoice.JENNIFER),
    AliyunVoiceSpec("Ryan", AliyunVoice.RYAN),
    AliyunVoiceSpec("Katerina", AliyunVoice.KATERINA),
    AliyunVoiceSpec("Aiden", AliyunVoice.AIDEN),
    AliyunVoiceSpec("Eldric Sage", AliyunVoice.ELDRIC_SAGE),
    AliyunVoiceSpec("Mia", AliyunVoice.MIA),
    AliyunVoiceSpec("Mochi", AliyunVoice.MOCHI),
    AliyunVoiceSpec("Bellona", AliyunVoice.BELLONA),
    AliyunVoiceSpec("Vincent", AliyunVoice.VINCENT),
    AliyunVoiceSpec("Bunny", AliyunVoice.BUNNY),
    AliyunVoiceSpec("Neil", AliyunVoice.NEIL),
    AliyunVoiceSpec("Elias", AliyunVoice.ELIAS),
    AliyunVoiceSpec("Arthur", AliyunVoice.ARTHUR),
    AliyunVoiceSpec("Nini", AliyunVoice.NINI),
    AliyunVoiceSpec("Ebona", AliyunVoice.EBONA),
    AliyunVoiceSpec("Seren", AliyunVoice.SEREN),
    AliyunVoiceSpec("Pip", AliyunVoice.PIP),
    AliyunVoiceSpec("Stella", AliyunVoice.STELLA),
    AliyunVoiceSpec("Bodega", AliyunVoice.BODEGA),
    AliyunVoiceSpec("Sonrisa", AliyunVoice.SONRISA),
    AliyunVoiceSpec("Alek", AliyunVoice.ALEK),
    AliyunVoiceSpec("Dolce", AliyunVoice.DOLCE),
    AliyunVoiceSpec("Sohee", AliyunVoice.SOHEE),
    AliyunVoiceSpec("Ono Anna", AliyunVoice.ONO_ANNA),
    AliyunVoiceSpec("Lenn", AliyunVoice.LENN),
    AliyunVoiceSpec("Emilien", AliyunVoice.EMILIEN),
    AliyunVoiceSpec("Andre", AliyunVoice.ANDRE),
    AliyunVoiceSpec("Radio Gol", AliyunVoice.RADIO_GOL),
    AliyunVoiceSpec("Jada", AliyunVoice.JADA),
    AliyunVoiceSpec("Dylan", AliyunVoice.DYLAN),
    AliyunVoiceSpec("Li", AliyunVoice.LI),
    AliyunVoiceSpec("Marcus", AliyunVoice.MARCUS),
    AliyunVoiceSpec("Roy", AliyunVoice.ROY),
    AliyunVoiceSpec("Peter", AliyunVoice.PETER),
    AliyunVoiceSpec("Sunny", AliyunVoice.SUNNY),
    AliyunVoiceSpec("Eric", AliyunVoice.ERIC),
    AliyunVoiceSpec("Rocky", AliyunVoice.ROCKY),
    AliyunVoiceSpec("Kiki", AliyunVoice.KIKI),
)
ALIYUN_SYSTEM_VOICE_IDS = tuple(voice.voice_id for voice in ALIYUN_SYSTEM_VOICES)
ALIYUN_SYSTEM_VOICE_BY_ID = MappingProxyType(
    {voice.voice_id: voice for voice in ALIYUN_SYSTEM_VOICES}
)
