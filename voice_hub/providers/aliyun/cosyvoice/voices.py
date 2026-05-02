from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from .models import ALIYUN_COSYVOICE_MODEL


@dataclass(frozen=True)
class AliyunCosyVoiceSpec:
    name: str
    voice_id: str
    model: str
    language: str
    note: str | None = None
    supports_ssml: bool = True
    supports_instruction: bool = False
    supports_timestamp: bool = True


class AliyunCosyVoice:
    """阿里云 cosyvoice-v3-flash 官方系统音色 ID 常量。"""

    LONGANYANG = "longanyang"
    LONGANHUAN = "longanhuan"
    LONGHUHU_V3 = "longhuhu_v3"
    LONGPAOPAO_V3 = "longpaopao_v3"
    LONGJIELIDOU_V3 = "longjielidou_v3"
    LONGXIAN_V3 = "longxian_v3"
    LONGLING_V3 = "longling_v3"
    LONGSHANSHAN_V3 = "longshanshan_v3"
    LONGNIUNIU_V3 = "longniuniu_v3"
    LONGJIAXIN_V3 = "longjiaxin_v3"
    LONGJIAYI_V3 = "longjiayi_v3"
    LONGANYUE_V3 = "longanyue_v3"
    LONGLAOTIE_V3 = "longlaotie_v3"
    LONGSHANGE_V3 = "longshange_v3"
    LONGANMIN_V3 = "longanmin_v3"
    LOONGKYONG_V3 = "loongkyong_v3"
    LOONGRIKO_V3 = "loongriko_v3"
    LOONGTOMOKA_V3 = "loongtomoka_v3"
    LOONGABBY_V3 = "loongabby_v3"
    LOONGANDY_V3 = "loongandy_v3"
    LOONGANNIE_V3 = "loongannie_v3"
    LOONGAVA_V3 = "loongava_v3"
    LOONGBETH_V3 = "loongbeth_v3"
    LOONGBETTY_V3 = "loongbetty_v3"
    LOONGCALLY_V3 = "loongcally_v3"
    LOONGCINDY_V3 = "loongcindy_v3"
    LOONGDAVID_V3 = "loongdavid_v3"
    LOONGDONNA_V3 = "loongdonna_v3"
    LOONGEMILY_V3 = "loongemily_v3"
    LOONGERIC_V3 = "loongeric_v3"
    LOONGLUNA_V3 = "loongluna_v3"
    LOONGLUCA_V3 = "loongluca_v3"
    LOONGTOMOYA_V3 = "loongtomoya_v3"
    LOONGYUUNA_V3 = "loongyuuna_v3"
    LOONGYUUMA_V3 = "loongyuuma_v3"
    LOONGJIHUN_V3 = "loongjihun_v3"
    LOONGINDAH_V3 = "loongindah_v3"
    LONGFEI_V3 = "longfei_v3"
    LONGYINGXIAO_V3 = "longyingxiao_v3"
    LONGYINGXUN_V3 = "longyingxun_v3"
    LONGYINGJING_V3 = "longyingjing_v3"
    LONGYINGLING_V3 = "longyingling_v3"
    LONGYINGTAO_V3 = "longyingtao_v3"
    LONGXIAOCHUN_V3 = "longxiaochun_v3"
    LONGXIAOXIA_V3 = "longxiaoxia_v3"
    LONGYUMI_V3 = "longyumi_v3"
    LONGANYUN_V3 = "longanyun_v3"
    LONGANWEN_V3 = "longanwen_v3"
    LONGANLI_V3 = "longanli_v3"
    LONGANLANG_V3 = "longanlang_v3"
    LONGYINGMU_V3 = "longyingmu_v3"
    LONGANTAI_V3 = "longantai_v3"
    LONGHUA_V3 = "longhua_v3"
    LONGCHENG_V3 = "longcheng_v3"
    LONGZE_V3 = "longze_v3"
    LONGZHE_V3 = "longzhe_v3"
    LONGYAN_V3 = "longyan_v3"
    LONGXING_V3 = "longxing_v3"
    LONGTIAN_V3 = "longtian_v3"
    LONGWAN_V3 = "longwan_v3"
    LONGQIANG_V3 = "longqiang_v3"
    LONGFEIFEI_V3 = "longfeifei_v3"
    LONGHAO_V3 = "longhao_v3"
    LONGANROU_V3 = "longanrou_v3"
    LONGHAN_V3 = "longhan_v3"
    LONGANZHI_V3 = "longanzhi_v3"
    LONGANLING_V3 = "longanling_v3"
    LONGANYA_V3 = "longanya_v3"
    LONGANQIN_V3 = "longanqin_v3"
    LONGMIAO_V3 = "longmiao_v3"
    LONGSANSHU_V3 = "longsanshu_v3"
    LONGYUAN_V3 = "longyuan_v3"
    LONGYUE_V3 = "longyue_v3"
    LONGXIU_V3 = "longxiu_v3"
    LONGNAN_V3 = "longnan_v3"
    LONGWANJUN_V3 = "longwanjun_v3"
    LONGYICHEN_V3 = "longyichen_v3"
    LONGLAOBO_V3 = "longlaobo_v3"
    LONGLAOYI_V3 = "longlaoyi_v3"
    LONGJIQI_V3 = "longjiqi_v3"
    LONGHOUGE_V3 = "longhouge_v3"
    LONGDAIYU_V3 = "longdaiyu_v3"
    LONGANRAN_V3 = "longanran_v3"
    LONGANXUAN_V3 = "longanxuan_v3"
    LONGSHUO_V3 = "longshuo_v3"
    LONGSHU_V3 = "longshu_v3"
    LOONGBELLA_V3 = "loongbella_v3"


def _v3(
    name: str,
    voice_id: str,
    language: str,
    note: str,
    *,
    supports_ssml: bool = True,
    supports_instruction: bool = False,
    supports_timestamp: bool = True,
) -> AliyunCosyVoiceSpec:
    return AliyunCosyVoiceSpec(
        name=name,
        voice_id=voice_id,
        model=ALIYUN_COSYVOICE_MODEL,
        language=language,
        note=note,
        supports_ssml=supports_ssml,
        supports_instruction=supports_instruction,
        supports_timestamp=supports_timestamp,
    )


ALIYUN_COSYVOICE_SYSTEM_VOICES = (
    _v3("龙安洋", AliyunCosyVoice.LONGANYANG, "中文（普通话）、英文", "阳光大男孩", supports_instruction=True),
    _v3("龙安欢", AliyunCosyVoice.LONGANHUAN, "中文（普通话）、英文", "欢脱元气女", supports_instruction=True),
    _v3("龙呼呼", AliyunCosyVoice.LONGHUHU_V3, "中文（普通话）、英文", "天真烂漫女童", supports_instruction=True),
    _v3("龙泡泡", AliyunCosyVoice.LONGPAOPAO_V3, "中文（普通话）、英文", "飞天泡泡音"),
    _v3("龙杰力豆", AliyunCosyVoice.LONGJIELIDOU_V3, "中文（普通话）、英文", "阳光顽皮男"),
    _v3("龙仙", AliyunCosyVoice.LONGXIAN_V3, "中文（普通话）、英文", "豪放可爱女"),
    _v3("龙铃", AliyunCosyVoice.LONGLING_V3, "中文（普通话）、英文", "稚气呆板女"),
    _v3("龙闪闪", AliyunCosyVoice.LONGSHANSHAN_V3, "中文（普通话）、英文", "戏剧化童声"),
    _v3("龙牛牛", AliyunCosyVoice.LONGNIUNIU_V3, "中文（普通话）、英文", "阳光男童声"),
    _v3("龙嘉欣", AliyunCosyVoice.LONGJIAXIN_V3, "中文（粤语）、英文", "优雅粤语女"),
    _v3("龙嘉怡", AliyunCosyVoice.LONGJIAYI_V3, "中文（粤语）、英文", "知性粤语女"),
    _v3("龙安粤", AliyunCosyVoice.LONGANYUE_V3, "中文（粤语）、英文", "欢脱粤语男"),
    _v3("龙老铁", AliyunCosyVoice.LONGLAOTIE_V3, "中文（东北话）、英文", "东北直率男"),
    _v3("龙陕哥", AliyunCosyVoice.LONGSHANGE_V3, "中文（陕西话）、英文", "原味陕北男"),
    _v3("龙安闽", AliyunCosyVoice.LONGANMIN_V3, "中文（闽南话）、英文", "清纯萝莉女"),
    _v3("loongkyong", AliyunCosyVoice.LOONGKYONG_V3, "韩语", "韩语女", supports_ssml=False, supports_timestamp=False),
    _v3("Riko", AliyunCosyVoice.LOONGRIKO_V3, "日语", "二次元霓虹女", supports_ssml=False, supports_timestamp=False),
    _v3("loongtomoka", AliyunCosyVoice.LOONGTOMOKA_V3, "日语", "日语女", supports_ssml=False, supports_timestamp=False),
    _v3("loongabby", AliyunCosyVoice.LOONGABBY_V3, "美式英语", "美式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongandy", AliyunCosyVoice.LOONGANDY_V3, "美式英语", "美式英文男", supports_ssml=False, supports_timestamp=False),
    _v3("loongannie", AliyunCosyVoice.LOONGANNIE_V3, "美式英语", "美式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongava", AliyunCosyVoice.LOONGAVA_V3, "美式英语", "美式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongbeth", AliyunCosyVoice.LOONGBETH_V3, "美式英语", "美式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongbetty", AliyunCosyVoice.LOONGBETTY_V3, "美式英语", "美式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongcally", AliyunCosyVoice.LOONGCALLY_V3, "美式英语", "美式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongcindy", AliyunCosyVoice.LOONGCINDY_V3, "美式英语", "美式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongdavid", AliyunCosyVoice.LOONGDAVID_V3, "美式英语", "美式英文男", supports_ssml=False, supports_timestamp=False),
    _v3("loongdonna", AliyunCosyVoice.LOONGDONNA_V3, "美式英语", "美式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongemily", AliyunCosyVoice.LOONGEMILY_V3, "英式英语", "英式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongeric", AliyunCosyVoice.LOONGERIC_V3, "英式英语", "英式英文男", supports_ssml=False, supports_timestamp=False),
    _v3("loongluna", AliyunCosyVoice.LOONGLUNA_V3, "英式英语", "英式英文女", supports_ssml=False, supports_timestamp=False),
    _v3("loongluca", AliyunCosyVoice.LOONGLUCA_V3, "英式英语", "英式英文男", supports_ssml=False, supports_timestamp=False),
    _v3("loongtomoya", AliyunCosyVoice.LOONGTOMOYA_V3, "日语", "日语男", supports_ssml=False, supports_timestamp=False),
    _v3("Yuuna", AliyunCosyVoice.LOONGYUUNA_V3, "日语", "日语女", supports_ssml=False, supports_timestamp=False),
    _v3("Yuuma", AliyunCosyVoice.LOONGYUUMA_V3, "日语", "日语男", supports_ssml=False, supports_timestamp=False),
    _v3("Jihun", AliyunCosyVoice.LOONGJIHUN_V3, "韩语", "韩语男", supports_ssml=False, supports_timestamp=False),
    _v3("loongindah", AliyunCosyVoice.LOONGINDAH_V3, "印尼语", "印尼女", supports_ssml=False, supports_timestamp=False),
    _v3("龙飞", AliyunCosyVoice.LONGFEI_V3, "中文（普通话）、英文", "热血磁性男"),
    _v3("龙应笑", AliyunCosyVoice.LONGYINGXIAO_V3, "中文（普通话）、英文", "清甜推销女"),
    _v3("龙应询", AliyunCosyVoice.LONGYINGXUN_V3, "中文（普通话）、英文", "年轻青涩男"),
    _v3("龙应静", AliyunCosyVoice.LONGYINGJING_V3, "中文（普通话）、英文", "低调冷静女"),
    _v3("龙应聆", AliyunCosyVoice.LONGYINGLING_V3, "中文（普通话）、英文", "温和共情女"),
    _v3("龙应桃", AliyunCosyVoice.LONGYINGTAO_V3, "中文（普通话）、英文", "温柔淡定女"),
    _v3("龙小淳", AliyunCosyVoice.LONGXIAOCHUN_V3, "中文（普通话）、英文", "知性积极女"),
    _v3("龙小夏", AliyunCosyVoice.LONGXIAOXIA_V3, "中文（普通话）、英文", "沉稳权威女"),
    _v3("YUMI", AliyunCosyVoice.LONGYUMI_V3, "中文（普通话）、英文", "正经青年女"),
    _v3("龙安昀", AliyunCosyVoice.LONGANYUN_V3, "中文（普通话）、英文", "居家暖男"),
    _v3("龙安温", AliyunCosyVoice.LONGANWEN_V3, "中文（普通话）、英文", "优雅知性女"),
    _v3("龙安莉", AliyunCosyVoice.LONGANLI_V3, "中文（普通话）、英文", "利落从容女"),
    _v3("龙安朗", AliyunCosyVoice.LONGANLANG_V3, "中文（普通话）、英文", "清爽利落男"),
    _v3("龙应沐", AliyunCosyVoice.LONGYINGMU_V3, "中文（普通话）、英文", "优雅知性女"),
    _v3("龙安台", AliyunCosyVoice.LONGANTAI_V3, "中文（普通话）、英文", "嗲甜台湾女"),
    _v3("龙华", AliyunCosyVoice.LONGHUA_V3, "中文（普通话）、英文", "元气甜美女"),
    _v3("龙橙", AliyunCosyVoice.LONGCHENG_V3, "中文（普通话）、英文", "智慧青年男"),
    _v3("龙泽", AliyunCosyVoice.LONGZE_V3, "中文（普通话）、英文", "温暖元气男"),
    _v3("龙哲", AliyunCosyVoice.LONGZHE_V3, "中文（普通话）、英文", "呆板大暖男"),
    _v3("龙颜", AliyunCosyVoice.LONGYAN_V3, "中文（普通话）、英文", "温暖春风女"),
    _v3("龙星", AliyunCosyVoice.LONGXING_V3, "中文（普通话）、英文", "温婉邻家女"),
    _v3("龙天", AliyunCosyVoice.LONGTIAN_V3, "中文（普通话）、英文", "磁性理智男"),
    _v3("龙婉", AliyunCosyVoice.LONGWAN_V3, "中文（普通话）、英文", "细腻柔声女"),
    _v3("龙嫱", AliyunCosyVoice.LONGQIANG_V3, "中文（普通话）、英文", "浪漫风情女"),
    _v3("龙菲菲", AliyunCosyVoice.LONGFEIFEI_V3, "中文（普通话）、英文", "甜美娇气女"),
    _v3("龙浩", AliyunCosyVoice.LONGHAO_V3, "中文（普通话）、英文", "多情忧郁男"),
    _v3("龙安柔", AliyunCosyVoice.LONGANROU_V3, "中文（普通话）、英文", "温柔闺蜜女"),
    _v3("龙寒", AliyunCosyVoice.LONGHAN_V3, "中文（普通话）、英文", "温暖痴情男"),
    _v3("龙安智", AliyunCosyVoice.LONGANZHI_V3, "中文（普通话）、英文", "睿智轻熟男"),
    _v3("龙安灵", AliyunCosyVoice.LONGANLING_V3, "中文（普通话）、英文", "思维灵动女"),
    _v3("龙安雅", AliyunCosyVoice.LONGANYA_V3, "中文（普通话）、英文", "高雅气质女"),
    _v3("龙安亲", AliyunCosyVoice.LONGANQIN_V3, "中文（普通话）、英文", "亲和活泼女"),
    _v3("龙妙", AliyunCosyVoice.LONGMIAO_V3, "中文（普通话）、英文", "抑扬顿挫女"),
    _v3("龙三叔", AliyunCosyVoice.LONGSANSHU_V3, "中文（普通话）、英文", "沉稳质感男"),
    _v3("龙媛", AliyunCosyVoice.LONGYUAN_V3, "中文（普通话）、英文", "温暖治愈女"),
    _v3("龙悦", AliyunCosyVoice.LONGYUE_V3, "中文（普通话）、英文", "温暖磁性女"),
    _v3("龙修", AliyunCosyVoice.LONGXIU_V3, "中文（普通话）、英文", "博才说书男"),
    _v3("龙楠", AliyunCosyVoice.LONGNAN_V3, "中文（普通话）、英文", "睿智青年男"),
    _v3("龙婉君", AliyunCosyVoice.LONGWANJUN_V3, "中文（普通话）、英文", "细腻柔声女"),
    _v3("龙逸尘", AliyunCosyVoice.LONGYICHEN_V3, "中文（普通话）、英文", "洒脱活力男"),
    _v3("龙老伯", AliyunCosyVoice.LONGLAOBO_V3, "中文（普通话）、英文", "沧桑岁月爷"),
    _v3("龙老姨", AliyunCosyVoice.LONGLAOYI_V3, "中文（普通话）、英文", "烟火从容阿姨"),
    _v3("龙机器", AliyunCosyVoice.LONGJIQI_V3, "中文（普通话）、英文", "呆萌机器人"),
    _v3("龙猴哥", AliyunCosyVoice.LONGHOUGE_V3, "中文（普通话）、英文", "经典猴哥"),
    _v3("龙黛玉", AliyunCosyVoice.LONGDAIYU_V3, "中文（普通话）、英文", "娇率才女音"),
    _v3("龙安燃", AliyunCosyVoice.LONGANRAN_V3, "中文（普通话）、英文", "活泼质感女"),
    _v3("龙安宣", AliyunCosyVoice.LONGANXUAN_V3, "中文（普通话）、英文", "经典直播女"),
    _v3("龙硕", AliyunCosyVoice.LONGSHUO_V3, "中文（普通话）、英文", "博才干练男"),
    _v3("龙书", AliyunCosyVoice.LONGSHU_V3, "中文（普通话）、英文", "沉稳青年男"),
    _v3("Bella3.0", AliyunCosyVoice.LOONGBELLA_V3, "中文（普通话）、英文", "精准干练女"),
)
ALIYUN_COSYVOICE_SYSTEM_VOICE_IDS = tuple(voice.voice_id for voice in ALIYUN_COSYVOICE_SYSTEM_VOICES)
ALIYUN_COSYVOICE_SYSTEM_VOICE_BY_ID = MappingProxyType(
    {voice.voice_id: voice for voice in ALIYUN_COSYVOICE_SYSTEM_VOICES}
)
