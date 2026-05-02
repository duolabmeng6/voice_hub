from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MinimaxVoiceSpec:
    """MiniMax 官方系统音色说明。"""

    index: int
    language: str
    voice_id: str
    name: str

    @property
    def note(self) -> str:
        return f"{self.language} / {self.name}"


class MinimaxVoice:
    """MiniMax 官方系统音色 ID。"""

    # 1. 中文 (普通话) / 青涩青年音色
    MALE_QN_QINGSE = 'male-qn-qingse'
    # 2. 中文 (普通话) / 精英青年音色
    MALE_QN_JINGYING = 'male-qn-jingying'
    # 3. 中文 (普通话) / 霸道青年音色
    MALE_QN_BADAO = 'male-qn-badao'
    # 4. 中文 (普通话) / 青年大学生音色
    MALE_QN_DAXUESHENG = 'male-qn-daxuesheng'
    # 5. 中文 (普通话) / 少女音色
    FEMALE_SHAONV = 'female-shaonv'
    # 6. 中文 (普通话) / 御姐音色
    FEMALE_YUJIE = 'female-yujie'
    # 7. 中文 (普通话) / 成熟女性音色
    FEMALE_CHENGSHU = 'female-chengshu'
    # 8. 中文 (普通话) / 甜美女性音色
    FEMALE_TIANMEI = 'female-tianmei'
    # 9. 中文 (普通话) / 青涩青年音色-beta
    MALE_QN_QINGSE_JINGPIN = 'male-qn-qingse-jingpin'
    # 10. 中文 (普通话) / 精英青年音色-beta
    MALE_QN_JINGYING_JINGPIN = 'male-qn-jingying-jingpin'
    # 11. 中文 (普通话) / 霸道青年音色-beta
    MALE_QN_BADAO_JINGPIN = 'male-qn-badao-jingpin'
    # 12. 中文 (普通话) / 青年大学生音色-beta
    MALE_QN_DAXUESHENG_JINGPIN = 'male-qn-daxuesheng-jingpin'
    # 13. 中文 (普通话) / 少女音色-beta
    FEMALE_SHAONV_JINGPIN = 'female-shaonv-jingpin'
    # 14. 中文 (普通话) / 御姐音色-beta
    FEMALE_YUJIE_JINGPIN = 'female-yujie-jingpin'
    # 15. 中文 (普通话) / 成熟女性音色-beta
    FEMALE_CHENGSHU_JINGPIN = 'female-chengshu-jingpin'
    # 16. 中文 (普通话) / 甜美女性音色-beta
    FEMALE_TIANMEI_JINGPIN = 'female-tianmei-jingpin'
    # 17. 中文 (普通话) / 聪明男童
    CLEVER_BOY = 'clever_boy'
    # 18. 中文 (普通话) / 可爱男童
    CUTE_BOY = 'cute_boy'
    # 19. 中文 (普通话) / 萌萌女童
    LOVELY_GIRL = 'lovely_girl'
    # 20. 中文 (普通话) / 卡通猪小琪
    CARTOON_PIG = 'cartoon_pig'
    # 21. 中文 (普通话) / 病娇弟弟
    BINGJIAO_DIDI = 'bingjiao_didi'
    # 22. 中文 (普通话) / 俊朗男友
    JUNLANG_NANYOU = 'junlang_nanyou'
    # 23. 中文 (普通话) / 纯真学弟
    CHUNZHEN_XUEDI = 'chunzhen_xuedi'
    # 24. 中文 (普通话) / 冷淡学长
    LENGDAN_XIONGZHANG = 'lengdan_xiongzhang'
    # 25. 中文 (普通话) / 霸道少爷
    BADAO_SHAOYE = 'badao_shaoye'
    # 26. 中文 (普通话) / 甜心小玲
    TIANXIN_XIAOLING = 'tianxin_xiaoling'
    # 27. 中文 (普通话) / 俏皮萌妹
    QIAOPI_MENGMEI = 'qiaopi_mengmei'
    # 28. 中文 (普通话) / 妩媚御姐
    WUMEI_YUJIE = 'wumei_yujie'
    # 29. 中文 (普通话) / 嗲嗲学妹
    DIADIA_XUEMEI = 'diadia_xuemei'
    # 30. 中文 (普通话) / 淡雅学姐
    DANYA_XUEJIE = 'danya_xuejie'
    # 31. 中文 (普通话) / 沉稳高管
    CHINESE_MANDARIN_RELIABLE_EXECUTIVE = 'Chinese (Mandarin)_Reliable_Executive'
    # 32. 中文 (普通话) / 新闻女声
    CHINESE_MANDARIN_NEWS_ANCHOR = 'Chinese (Mandarin)_News_Anchor'
    # 33. 中文 (普通话) / 傲娇御姐
    CHINESE_MANDARIN_MATURE_WOMAN = 'Chinese (Mandarin)_Mature_Woman'
    # 34. 中文 (普通话) / 不羁青年
    CHINESE_MANDARIN_UNRESTRAINED_YOUNG_MAN = 'Chinese (Mandarin)_Unrestrained_Young_Man'
    # 35. 中文 (普通话) / 嚣张小姐
    ARROGANT_MISS = 'Arrogant_Miss'
    # 36. 中文 (普通话) / 机械战甲
    ROBOT_ARMOR = 'Robot_Armor'
    # 37. 中文 (普通话) / 热心大婶
    CHINESE_MANDARIN_KIND_HEARTED_ANTIE = 'Chinese (Mandarin)_Kind-hearted_Antie'
    # 38. 中文 (普通话) / 港普空姐
    CHINESE_MANDARIN_HK_FLIGHT_ATTENDANT = 'Chinese (Mandarin)_HK_Flight_Attendant'
    # 39. 中文 (普通话) / 搞笑大爷
    CHINESE_MANDARIN_HUMOROUS_ELDER = 'Chinese (Mandarin)_Humorous_Elder'
    # 40. 中文 (普通话) / 温润男声
    CHINESE_MANDARIN_GENTLEMAN = 'Chinese (Mandarin)_Gentleman'
    # 41. 中文 (普通话) / 温暖闺蜜
    CHINESE_MANDARIN_WARM_BESTIE = 'Chinese (Mandarin)_Warm_Bestie'
    # 42. 中文 (普通话) / 播报男声
    CHINESE_MANDARIN_MALE_ANNOUNCER = 'Chinese (Mandarin)_Male_Announcer'
    # 43. 中文 (普通话) / 甜美女声
    CHINESE_MANDARIN_SWEET_LADY = 'Chinese (Mandarin)_Sweet_Lady'
    # 44. 中文 (普通话) / 南方小哥
    CHINESE_MANDARIN_SOUTHERN_YOUNG_MAN = 'Chinese (Mandarin)_Southern_Young_Man'
    # 45. 中文 (普通话) / 阅历姐姐
    CHINESE_MANDARIN_WISE_WOMEN = 'Chinese (Mandarin)_Wise_Women'
    # 46. 中文 (普通话) / 温润青年
    CHINESE_MANDARIN_GENTLE_YOUTH = 'Chinese (Mandarin)_Gentle_Youth'
    # 47. 中文 (普通话) / 温暖少女
    CHINESE_MANDARIN_WARM_GIRL = 'Chinese (Mandarin)_Warm_Girl'
    # 48. 中文 (普通话) / 花甲奶奶
    CHINESE_MANDARIN_KIND_HEARTED_ELDER = 'Chinese (Mandarin)_Kind-hearted_Elder'
    # 49. 中文 (普通话) / 憨憨萌兽
    CHINESE_MANDARIN_CUTE_SPIRIT = 'Chinese (Mandarin)_Cute_Spirit'
    # 50. 中文 (普通话) / 电台男主播
    CHINESE_MANDARIN_RADIO_HOST = 'Chinese (Mandarin)_Radio_Host'
    # 51. 中文 (普通话) / 抒情男声
    CHINESE_MANDARIN_LYRICAL_VOICE = 'Chinese (Mandarin)_Lyrical_Voice'
    # 52. 中文 (普通话) / 率真弟弟
    CHINESE_MANDARIN_STRAIGHTFORWARD_BOY = 'Chinese (Mandarin)_Straightforward_Boy'
    # 53. 中文 (普通话) / 真诚青年
    CHINESE_MANDARIN_SINCERE_ADULT = 'Chinese (Mandarin)_Sincere_Adult'
    # 54. 中文 (普通话) / 温柔学姐
    CHINESE_MANDARIN_GENTLE_SENIOR = 'Chinese (Mandarin)_Gentle_Senior'
    # 55. 中文 (普通话) / 嘴硬竹马
    CHINESE_MANDARIN_STUBBORN_FRIEND = 'Chinese (Mandarin)_Stubborn_Friend'
    # 56. 中文 (普通话) / 清脆少女
    CHINESE_MANDARIN_CRISP_GIRL = 'Chinese (Mandarin)_Crisp_Girl'
    # 57. 中文 (普通话) / 清澈邻家弟弟
    CHINESE_MANDARIN_PURE_HEARTED_BOY = 'Chinese (Mandarin)_Pure-hearted_Boy'
    # 58. 中文 (普通话) / 柔和少女
    CHINESE_MANDARIN_SOFT_GIRL = 'Chinese (Mandarin)_Soft_Girl'
    # 59. 中文 (粤语) / 专业女主持
    CANTONESE_PROFESSIONALHOST_F = 'Cantonese_ProfessionalHost（F)'
    # 60. 中文 (粤语) / 温柔女声
    CANTONESE_GENTLELADY = 'Cantonese_GentleLady'
    # 61. 中文 (粤语) / 专业男主持
    CANTONESE_PROFESSIONALHOST_M = 'Cantonese_ProfessionalHost（M)'
    # 62. 中文 (粤语) / 活泼男声
    CANTONESE_PLAYFULMAN = 'Cantonese_PlayfulMan'
    # 63. 中文 (粤语) / 可爱女孩
    CANTONESE_CUTEGIRL = 'Cantonese_CuteGirl'
    # 64. 中文 (粤语) / 善良女声
    CANTONESE_KINDWOMAN = 'Cantonese_KindWoman'
    # 65. 英文 / Santa Claus
    SANTA_CLAUS = 'Santa_Claus '
    # 66. 英文 / Grinch
    GRINCH = 'Grinch'
    # 67. 英文 / Rudolph
    RUDOLPH = 'Rudolph'
    # 68. 英文 / Arnold
    ARNOLD = 'Arnold'
    # 69. 英文 / Charming Santa
    CHARMING_SANTA = 'Charming_Santa'
    # 70. 英文 / Charming Lady
    CHARMING_LADY = 'Charming_Lady'
    # 71. 英文 / Sweet Girl
    SWEET_GIRL = 'Sweet_Girl'
    # 72. 英文 / Cute Elf
    CUTE_ELF = 'Cute_Elf'
    # 73. 英文 / Attractive Girl
    ATTRACTIVE_GIRL = 'Attractive_Girl'
    # 74. 英文 / Serene Woman
    SERENE_WOMAN = 'Serene_Woman'
    # 75. 英文 / Trustworthy Man
    ENGLISH_TRUSTWORTHY_MAN = 'English_Trustworthy_Man'
    # 76. 英文 / Graceful Lady
    ENGLISH_GRACEFUL_LADY = 'English_Graceful_Lady'
    # 77. 英文 / Aussie Bloke
    ENGLISH_AUSSIE_BLOKE = 'English_Aussie_Bloke'
    # 78. 英文 / Whispering girl
    ENGLISH_WHISPERING_GIRL = 'English_Whispering_girl'
    # 79. 英文 / Diligent Man
    ENGLISH_DILIGENT_MAN = 'English_Diligent_Man'
    # 80. 英文 / Gentle-voiced man
    ENGLISH_GENTLE_VOICED_MAN = 'English_Gentle-voiced_man'
    # 81. 日文 / Intellectual Senior
    JAPANESE_INTELLECTUALSENIOR = 'Japanese_IntellectualSenior'
    # 82. 日文 / Decisive Princess
    JAPANESE_DECISIVEPRINCESS = 'Japanese_DecisivePrincess'
    # 83. 日文 / Loyal Knight
    JAPANESE_LOYALKNIGHT = 'Japanese_LoyalKnight'
    # 84. 日文 / Dominant Man
    JAPANESE_DOMINANTMAN = 'Japanese_DominantMan'
    # 85. 日文 / Serious Commander
    JAPANESE_SERIOUSCOMMANDER = 'Japanese_SeriousCommander'
    # 86. 日文 / Cold Queen
    JAPANESE_COLDQUEEN = 'Japanese_ColdQueen'
    # 87. 日文 / Dependable Woman
    JAPANESE_DEPENDABLEWOMAN = 'Japanese_DependableWoman'
    # 88. 日文 / Gentle Butler
    JAPANESE_GENTLEBUTLER = 'Japanese_GentleButler'
    # 89. 日文 / Kind Lady
    JAPANESE_KINDLADY = 'Japanese_KindLady'
    # 90. 日文 / Calm Lady
    JAPANESE_CALMLADY = 'Japanese_CalmLady'
    # 91. 日文 / Optimistic Youth
    JAPANESE_OPTIMISTICYOUTH = 'Japanese_OptimisticYouth'
    # 92. 日文 / Generous Izakaya Owner
    JAPANESE_GENEROUSIZAKAYAOWNER = 'Japanese_GenerousIzakayaOwner'
    # 93. 日文 / Sporty Student
    JAPANESE_SPORTYSTUDENT = 'Japanese_SportyStudent'
    # 94. 日文 / Innocent Boy
    JAPANESE_INNOCENTBOY = 'Japanese_InnocentBoy'
    # 95. 日文 / Graceful Maiden
    JAPANESE_GRACEFULMAIDEN = 'Japanese_GracefulMaiden'
    # 96. 韩文 / Sweet Girl
    KOREAN_SWEETGIRL = 'Korean_SweetGirl'
    # 97. 韩文 / Cheerful Boyfriend
    KOREAN_CHEERFULBOYFRIEND = 'Korean_CheerfulBoyfriend'
    # 98. 韩文 / Enchanting Sister
    KOREAN_ENCHANTINGSISTER = 'Korean_EnchantingSister'
    # 99. 韩文 / Shy Girl
    KOREAN_SHYGIRL = 'Korean_ShyGirl'
    # 100. 韩文 / Reliable Sister
    KOREAN_RELIABLESISTER = 'Korean_ReliableSister'
    # 101. 韩文 / Strict Boss
    KOREAN_STRICTBOSS = 'Korean_StrictBoss'
    # 102. 韩文 / Sassy Girl
    KOREAN_SASSYGIRL = 'Korean_SassyGirl'
    # 103. 韩文 / Childhood Friend Girl
    KOREAN_CHILDHOODFRIENDGIRL = 'Korean_ChildhoodFriendGirl'
    # 104. 韩文 / Playboy Charmer
    KOREAN_PLAYBOYCHARMER = 'Korean_PlayboyCharmer'
    # 105. 韩文 / Elegant Princess
    KOREAN_ELEGANTPRINCESS = 'Korean_ElegantPrincess'
    # 106. 韩文 / Brave Female Warrior
    KOREAN_BRAVEFEMALEWARRIOR = 'Korean_BraveFemaleWarrior'
    # 107. 韩文 / Brave Youth
    KOREAN_BRAVEYOUTH = 'Korean_BraveYouth'
    # 108. 韩文 / Calm Lady
    KOREAN_CALMLADY = 'Korean_CalmLady'
    # 109. 韩文 / Enthusiastic Teen
    KOREAN_ENTHUSIASTICTEEN = 'Korean_EnthusiasticTeen'
    # 110. 韩文 / Soothing Lady
    KOREAN_SOOTHINGLADY = 'Korean_SoothingLady'
    # 111. 韩文 / Intellectual Senior
    KOREAN_INTELLECTUALSENIOR = 'Korean_IntellectualSenior'
    # 112. 韩文 / Lonely Warrior
    KOREAN_LONELYWARRIOR = 'Korean_LonelyWarrior'
    # 113. 韩文 / Mature Lady
    KOREAN_MATURELADY = 'Korean_MatureLady'
    # 114. 韩文 / Innocent Boy
    KOREAN_INNOCENTBOY = 'Korean_InnocentBoy'
    # 115. 韩文 / Charming Sister
    KOREAN_CHARMINGSISTER = 'Korean_CharmingSister'
    # 116. 韩文 / Athletic Student
    KOREAN_ATHLETICSTUDENT = 'Korean_AthleticStudent'
    # 117. 韩文 / Brave Adventurer
    KOREAN_BRAVEADVENTURER = 'Korean_BraveAdventurer'
    # 118. 韩文 / Calm Gentleman
    KOREAN_CALMGENTLEMAN = 'Korean_CalmGentleman'
    # 119. 韩文 / Wise Elf
    KOREAN_WISEELF = 'Korean_WiseElf'
    # 120. 韩文 / Cheerful Cool Junior
    KOREAN_CHEERFULCOOLJUNIOR = 'Korean_CheerfulCoolJunior'
    # 121. 韩文 / Decisive Queen
    KOREAN_DECISIVEQUEEN = 'Korean_DecisiveQueen'
    # 122. 韩文 / Cold Young Man
    KOREAN_COLDYOUNGMAN = 'Korean_ColdYoungMan'
    # 123. 韩文 / Mysterious Girl
    KOREAN_MYSTERIOUSGIRL = 'Korean_MysteriousGirl'
    # 124. 韩文 / Quirky Girl
    KOREAN_QUIRKYGIRL = 'Korean_QuirkyGirl'
    # 125. 韩文 / Considerate Senior
    KOREAN_CONSIDERATESENIOR = 'Korean_ConsiderateSenior'
    # 126. 韩文 / Cheerful Little Sister
    KOREAN_CHEERFULLITTLESISTER = 'Korean_CheerfulLittleSister'
    # 127. 韩文 / Dominant Man
    KOREAN_DOMINANTMAN = 'Korean_DominantMan'
    # 128. 韩文 / Airheaded Girl
    KOREAN_AIRHEADEDGIRL = 'Korean_AirheadedGirl'
    # 129. 韩文 / Reliable Youth
    KOREAN_RELIABLEYOUTH = 'Korean_ReliableYouth'
    # 130. 韩文 / Friendly Big Sister
    KOREAN_FRIENDLYBIGSISTER = 'Korean_FriendlyBigSister'
    # 131. 韩文 / Gentle Boss
    KOREAN_GENTLEBOSS = 'Korean_GentleBoss'
    # 132. 韩文 / Cold Girl
    KOREAN_COLDGIRL = 'Korean_ColdGirl'
    # 133. 韩文 / Haughty Lady
    KOREAN_HAUGHTYLADY = 'Korean_HaughtyLady'
    # 134. 韩文 / Charming Elder Sister
    KOREAN_CHARMINGELDERSISTER = 'Korean_CharmingElderSister'
    # 135. 韩文 / Intellectual Man
    KOREAN_INTELLECTUALMAN = 'Korean_IntellectualMan'
    # 136. 韩文 / Caring Woman
    KOREAN_CARINGWOMAN = 'Korean_CaringWoman'
    # 137. 韩文 / Wise Teacher
    KOREAN_WISETEACHER = 'Korean_WiseTeacher'
    # 138. 韩文 / Confident Boss
    KOREAN_CONFIDENTBOSS = 'Korean_ConfidentBoss'
    # 139. 韩文 / Athletic Girl
    KOREAN_ATHLETICGIRL = 'Korean_AthleticGirl'
    # 140. 韩文 / Possessive Man
    KOREAN_POSSESSIVEMAN = 'Korean_PossessiveMan'
    # 141. 韩文 / Gentle Woman
    KOREAN_GENTLEWOMAN = 'Korean_GentleWoman'
    # 142. 韩文 / Cocky Guy
    KOREAN_COCKYGUY = 'Korean_CockyGuy'
    # 143. 韩文 / Thoughtful Woman
    KOREAN_THOUGHTFULWOMAN = 'Korean_ThoughtfulWoman'
    # 144. 韩文 / Optimistic Youth
    KOREAN_OPTIMISTICYOUTH = 'Korean_OptimisticYouth'
    # 145. 西班牙文 / Serene Woman
    SPANISH_SERENEWOMAN = 'Spanish_SereneWoman'
    # 146. 西班牙文 / Mature Partner
    SPANISH_MATUREPARTNER = 'Spanish_MaturePartner'
    # 147. 西班牙文 / Captivating Storyteller
    SPANISH_CAPTIVATINGSTORYTELLER = 'Spanish_CaptivatingStoryteller'
    # 148. 西班牙文 / Narrator
    SPANISH_NARRATOR = 'Spanish_Narrator'
    # 149. 西班牙文 / Wise Scholar
    SPANISH_WISESCHOLAR = 'Spanish_WiseScholar'
    # 150. 西班牙文 / Kind-hearted Girl
    SPANISH_KIND_HEARTEDGIRL = 'Spanish_Kind-heartedGirl'
    # 151. 西班牙文 / Determined Manager
    SPANISH_DETERMINEDMANAGER = 'Spanish_DeterminedManager'
    # 152. 西班牙文 / Bossy Leader
    SPANISH_BOSSYLEADER = 'Spanish_BossyLeader'
    # 153. 西班牙文 / Reserved Young Man
    SPANISH_RESERVEDYOUNGMAN = 'Spanish_ReservedYoungMan'
    # 154. 西班牙文 / Confident Woman
    SPANISH_CONFIDENTWOMAN = 'Spanish_ConfidentWoman'
    # 155. 西班牙文 / Thoughtful Man
    SPANISH_THOUGHTFULMAN = 'Spanish_ThoughtfulMan'
    # 156. 西班牙文 / Strong-willed Boy
    SPANISH_STRONG_WILLEDBOY = 'Spanish_Strong-WilledBoy'
    # 157. 西班牙文 / Sophisticated Lady
    SPANISH_SOPHISTICATEDLADY = 'Spanish_SophisticatedLady'
    # 158. 西班牙文 / Rational Man
    SPANISH_RATIONALMAN = 'Spanish_RationalMan'
    # 159. 西班牙文 / Anime Character
    SPANISH_ANIMECHARACTER = 'Spanish_AnimeCharacter'
    # 160. 西班牙文 / Deep-toned Man
    SPANISH_DEEP_TONEDMAN = 'Spanish_Deep-tonedMan'
    # 161. 西班牙文 / Fussy hostess
    SPANISH_FUSSYHOSTESS = 'Spanish_Fussyhostess'
    # 162. 西班牙文 / Sincere Teen
    SPANISH_SINCERETEEN = 'Spanish_SincereTeen'
    # 163. 西班牙文 / Frank Lady
    SPANISH_FRANKLADY = 'Spanish_FrankLady'
    # 164. 西班牙文 / Comedian
    SPANISH_COMEDIAN = 'Spanish_Comedian'
    # 165. 西班牙文 / Debator
    SPANISH_DEBATOR = 'Spanish_Debator'
    # 166. 西班牙文 / Tough Boss
    SPANISH_TOUGHBOSS = 'Spanish_ToughBoss'
    # 167. 西班牙文 / Wise Lady
    SPANISH_WISELADY = 'Spanish_Wiselady'
    # 168. 西班牙文 / Steady Mentor
    SPANISH_STEADYMENTOR = 'Spanish_Steadymentor'
    # 169. 西班牙文 / Jovial Man
    SPANISH_JOVIALMAN = 'Spanish_Jovialman'
    # 170. 西班牙文 / Santa Claus
    SPANISH_SANTACLAUS = 'Spanish_SantaClaus'
    # 171. 西班牙文 / Rudolph
    SPANISH_RUDOLPH = 'Spanish_Rudolph'
    # 172. 西班牙文 / Intonate Girl
    SPANISH_INTONATEGIRL = 'Spanish_Intonategirl'
    # 173. 西班牙文 / Arnold
    SPANISH_ARNOLD = 'Spanish_Arnold'
    # 174. 西班牙文 / Ghost
    SPANISH_GHOST = 'Spanish_Ghost'
    # 175. 西班牙文 / Humorous Elder
    SPANISH_HUMOROUSELDER = 'Spanish_HumorousElder'
    # 176. 西班牙文 / Energetic Boy
    SPANISH_ENERGETICBOY = 'Spanish_EnergeticBoy'
    # 177. 西班牙文 / Whimsical Girl
    SPANISH_WHIMSICALGIRL = 'Spanish_WhimsicalGirl'
    # 178. 西班牙文 / Strict Boss
    SPANISH_STRICTBOSS = 'Spanish_StrictBoss'
    # 179. 西班牙文 / Reliable Man
    SPANISH_RELIABLEMAN = 'Spanish_ReliableMan'
    # 180. 西班牙文 / Serene Elder
    SPANISH_SERENEELDER = 'Spanish_SereneElder'
    # 181. 西班牙文 / Angry Man
    SPANISH_ANGRYMAN = 'Spanish_AngryMan'
    # 182. 西班牙文 / Assertive Queen
    SPANISH_ASSERTIVEQUEEN = 'Spanish_AssertiveQueen'
    # 183. 西班牙文 / Caring Girlfriend
    SPANISH_CARINGGIRLFRIEND = 'Spanish_CaringGirlfriend'
    # 184. 西班牙文 / Powerful Soldier
    SPANISH_POWERFULSOLDIER = 'Spanish_PowerfulSoldier'
    # 185. 西班牙文 / Passionate Warrior
    SPANISH_PASSIONATEWARRIOR = 'Spanish_PassionateWarrior'
    # 186. 西班牙文 / Chatty Girl
    SPANISH_CHATTYGIRL = 'Spanish_ChattyGirl'
    # 187. 西班牙文 / Romantic Husband
    SPANISH_ROMANTICHUSBAND = 'Spanish_RomanticHusband'
    # 188. 西班牙文 / Compelling Girl
    SPANISH_COMPELLINGGIRL = 'Spanish_CompellingGirl'
    # 189. 西班牙文 / Powerful Veteran
    SPANISH_POWERFULVETERAN = 'Spanish_PowerfulVeteran'
    # 190. 西班牙文 / Sensible Manager
    SPANISH_SENSIBLEMANAGER = 'Spanish_SensibleManager'
    # 191. 西班牙文 / Thoughtful Lady
    SPANISH_THOUGHTFULLADY = 'Spanish_ThoughtfulLady'
    # 192. 葡萄牙文 / Sentimental Lady
    PORTUGUESE_SENTIMENTALLADY = 'Portuguese_SentimentalLady'
    # 193. 葡萄牙文 / Bossy Leader
    PORTUGUESE_BOSSYLEADER = 'Portuguese_BossyLeader'
    # 194. 葡萄牙文 / Wise lady
    PORTUGUESE_WISELADY = 'Portuguese_Wiselady'
    # 195. 葡萄牙文 / Strong-willed Boy
    PORTUGUESE_STRONG_WILLEDBOY = 'Portuguese_Strong-WilledBoy'
    # 196. 葡萄牙文 / Deep-voiced Gentleman
    PORTUGUESE_DEEP_VOICEDGENTLEMAN = 'Portuguese_Deep-VoicedGentleman'
    # 197. 葡萄牙文 / Upset Girl
    PORTUGUESE_UPSETGIRL = 'Portuguese_UpsetGirl'
    # 198. 葡萄牙文 / Passionate Warrior
    PORTUGUESE_PASSIONATEWARRIOR = 'Portuguese_PassionateWarrior'
    # 199. 葡萄牙文 / Anime Character
    PORTUGUESE_ANIMECHARACTER = 'Portuguese_AnimeCharacter'
    # 200. 葡萄牙文 / Confident Woman
    PORTUGUESE_CONFIDENTWOMAN = 'Portuguese_ConfidentWoman'
    # 201. 葡萄牙文 / Angry Man
    PORTUGUESE_ANGRYMAN = 'Portuguese_AngryMan'
    # 202. 葡萄牙文 / Captivating Storyteller
    PORTUGUESE_CAPTIVATINGSTORYTELLER = 'Portuguese_CaptivatingStoryteller'
    # 203. 葡萄牙文 / Godfather
    PORTUGUESE_GODFATHER = 'Portuguese_Godfather'
    # 204. 葡萄牙文 / Reserved Young Man
    PORTUGUESE_RESERVEDYOUNGMAN = 'Portuguese_ReservedYoungMan'
    # 205. 葡萄牙文 / Smart Young Girl
    PORTUGUESE_SMARTYOUNGGIRL = 'Portuguese_SmartYoungGirl'
    # 206. 葡萄牙文 / Kind-hearted Girl
    PORTUGUESE_KIND_HEARTEDGIRL = 'Portuguese_Kind-heartedGirl'
    # 207. 葡萄牙文 / Pompous lady
    PORTUGUESE_POMPOUSLADY = 'Portuguese_Pompouslady'
    # 208. 葡萄牙文 / Grinch
    PORTUGUESE_GRINCH = 'Portuguese_Grinch'
    # 209. 葡萄牙文 / Debator
    PORTUGUESE_DEBATOR = 'Portuguese_Debator'
    # 210. 葡萄牙文 / Sweet Girl
    PORTUGUESE_SWEETGIRL = 'Portuguese_SweetGirl'
    # 211. 葡萄牙文 / Attractive Girl
    PORTUGUESE_ATTRACTIVEGIRL = 'Portuguese_AttractiveGirl'
    # 212. 葡萄牙文 / Thoughtful Man
    PORTUGUESE_THOUGHTFULMAN = 'Portuguese_ThoughtfulMan'
    # 213. 葡萄牙文 / Playful Girl
    PORTUGUESE_PLAYFULGIRL = 'Portuguese_PlayfulGirl'
    # 214. 葡萄牙文 / Gorgeous Lady
    PORTUGUESE_GORGEOUSLADY = 'Portuguese_GorgeousLady'
    # 215. 葡萄牙文 / Lovely Lady
    PORTUGUESE_LOVELYLADY = 'Portuguese_LovelyLady'
    # 216. 葡萄牙文 / Serene Woman
    PORTUGUESE_SERENEWOMAN = 'Portuguese_SereneWoman'
    # 217. 葡萄牙文 / Sad Teen
    PORTUGUESE_SADTEEN = 'Portuguese_SadTeen'
    # 218. 葡萄牙文 / Mature Partner
    PORTUGUESE_MATUREPARTNER = 'Portuguese_MaturePartner'
    # 219. 葡萄牙文 / Comedian
    PORTUGUESE_COMEDIAN = 'Portuguese_Comedian'
    # 220. 葡萄牙文 / Naughty Schoolgirl
    PORTUGUESE_NAUGHTYSCHOOLGIRL = 'Portuguese_NaughtySchoolgirl'
    # 221. 葡萄牙文 / Narrator
    PORTUGUESE_NARRATOR = 'Portuguese_Narrator'
    # 222. 葡萄牙文 / Tough Boss
    PORTUGUESE_TOUGHBOSS = 'Portuguese_ToughBoss'
    # 223. 葡萄牙文 / Fussy hostess
    PORTUGUESE_FUSSYHOSTESS = 'Portuguese_Fussyhostess'
    # 224. 葡萄牙文 / Dramatist
    PORTUGUESE_DRAMATIST = 'Portuguese_Dramatist'
    # 225. 葡萄牙文 / Steady Mentor
    PORTUGUESE_STEADYMENTOR = 'Portuguese_Steadymentor'
    # 226. 葡萄牙文 / Jovial Man
    PORTUGUESE_JOVIALMAN = 'Portuguese_Jovialman'
    # 227. 葡萄牙文 / Charming Queen
    PORTUGUESE_CHARMINGQUEEN = 'Portuguese_CharmingQueen'
    # 228. 葡萄牙文 / Santa Claus
    PORTUGUESE_SANTACLAUS = 'Portuguese_SantaClaus'
    # 229. 葡萄牙文 / Rudolph
    PORTUGUESE_RUDOLPH = 'Portuguese_Rudolph'
    # 230. 葡萄牙文 / Arnold
    PORTUGUESE_ARNOLD = 'Portuguese_Arnold'
    # 231. 葡萄牙文 / Charming Santa
    PORTUGUESE_CHARMINGSANTA = 'Portuguese_CharmingSanta'
    # 232. 葡萄牙文 / Charming Lady
    PORTUGUESE_CHARMINGLADY = 'Portuguese_CharmingLady'
    # 233. 葡萄牙文 / Ghost
    PORTUGUESE_GHOST = 'Portuguese_Ghost'
    # 234. 葡萄牙文 / Humorous Elder
    PORTUGUESE_HUMOROUSELDER = 'Portuguese_HumorousElder'
    # 235. 葡萄牙文 / Calm Leader
    PORTUGUESE_CALMLEADER = 'Portuguese_CalmLeader'
    # 236. 葡萄牙文 / Gentle Teacher
    PORTUGUESE_GENTLETEACHER = 'Portuguese_GentleTeacher'
    # 237. 葡萄牙文 / Energetic Boy
    PORTUGUESE_ENERGETICBOY = 'Portuguese_EnergeticBoy'
    # 238. 葡萄牙文 / Reliable Man
    PORTUGUESE_RELIABLEMAN = 'Portuguese_ReliableMan'
    # 239. 葡萄牙文 / Serene Elder
    PORTUGUESE_SERENEELDER = 'Portuguese_SereneElder'
    # 240. 葡萄牙文 / Grim Reaper
    PORTUGUESE_GRIMREAPER = 'Portuguese_GrimReaper'
    # 241. 葡萄牙文 / Assertive Queen
    PORTUGUESE_ASSERTIVEQUEEN = 'Portuguese_AssertiveQueen'
    # 242. 葡萄牙文 / Whimsical Girl
    PORTUGUESE_WHIMSICALGIRL = 'Portuguese_WhimsicalGirl'
    # 243. 葡萄牙文 / Stressed Lady
    PORTUGUESE_STRESSEDLADY = 'Portuguese_StressedLady'
    # 244. 葡萄牙文 / Friendly Neighbor
    PORTUGUESE_FRIENDLYNEIGHBOR = 'Portuguese_FriendlyNeighbor'
    # 245. 葡萄牙文 / Caring Girlfriend
    PORTUGUESE_CARINGGIRLFRIEND = 'Portuguese_CaringGirlfriend'
    # 246. 葡萄牙文 / Powerful Soldier
    PORTUGUESE_POWERFULSOLDIER = 'Portuguese_PowerfulSoldier'
    # 247. 葡萄牙文 / Fascinating Boy
    PORTUGUESE_FASCINATINGBOY = 'Portuguese_FascinatingBoy'
    # 248. 葡萄牙文 / Romantic Husband
    PORTUGUESE_ROMANTICHUSBAND = 'Portuguese_RomanticHusband'
    # 249. 葡萄牙文 / Strict Boss
    PORTUGUESE_STRICTBOSS = 'Portuguese_StrictBoss'
    # 250. 葡萄牙文 / Inspiring Lady
    PORTUGUESE_INSPIRINGLADY = 'Portuguese_InspiringLady'
    # 251. 葡萄牙文 / Playful Spirit
    PORTUGUESE_PLAYFULSPIRIT = 'Portuguese_PlayfulSpirit'
    # 252. 葡萄牙文 / Elegant Girl
    PORTUGUESE_ELEGANTGIRL = 'Portuguese_ElegantGirl'
    # 253. 葡萄牙文 / Compelling Girl
    PORTUGUESE_COMPELLINGGIRL = 'Portuguese_CompellingGirl'
    # 254. 葡萄牙文 / Powerful Veteran
    PORTUGUESE_POWERFULVETERAN = 'Portuguese_PowerfulVeteran'
    # 255. 葡萄牙文 / Sensible Manager
    PORTUGUESE_SENSIBLEMANAGER = 'Portuguese_SensibleManager'
    # 256. 葡萄牙文 / Thoughtful Lady
    PORTUGUESE_THOUGHTFULLADY = 'Portuguese_ThoughtfulLady'
    # 257. 葡萄牙文 / Theatrical Actor
    PORTUGUESE_THEATRICALACTOR = 'Portuguese_TheatricalActor'
    # 258. 葡萄牙文 / Fragile Boy
    PORTUGUESE_FRAGILEBOY = 'Portuguese_FragileBoy'
    # 259. 葡萄牙文 / Chatty Girl
    PORTUGUESE_CHATTYGIRL = 'Portuguese_ChattyGirl'
    # 260. 葡萄牙文 / Conscientious Instructor
    PORTUGUESE_CONSCIENTIOUSINSTRUCTOR = 'Portuguese_Conscientiousinstructor'
    # 261. 葡萄牙文 / Rational Man
    PORTUGUESE_RATIONALMAN = 'Portuguese_RationalMan'
    # 262. 葡萄牙文 / Wise Scholar
    PORTUGUESE_WISESCHOLAR = 'Portuguese_WiseScholar'
    # 263. 葡萄牙文 / Frank Lady
    PORTUGUESE_FRANKLADY = 'Portuguese_FrankLady'
    # 264. 葡萄牙文 / Determined Manager
    PORTUGUESE_DETERMINEDMANAGER = 'Portuguese_DeterminedManager'
    # 265. 法文 / Level-Headed Man
    FRENCH_MALE_SPEECH_NEW = 'French_Male_Speech_New'
    # 266. 法文 / Patient Female Presenter
    FRENCH_FEMALE_NEWS_ANCHOR = 'French_Female_News Anchor'
    # 267. 法文 / Casual Man
    FRENCH_CASUALMAN = 'French_CasualMan'
    # 268. 法文 / Movie Lead Female
    FRENCH_MOVIELEADFEMALE = 'French_MovieLeadFemale'
    # 269. 法文 / Female Anchor
    FRENCH_FEMALEANCHOR = 'French_FemaleAnchor'
    # 270. 法文 / Male Narrator
    FRENCH_MALENARRATOR = 'French_MaleNarrator'
    # 271. 印尼文 / Sweet Girl
    INDONESIAN_SWEETGIRL = 'Indonesian_SweetGirl'
    # 272. 印尼文 / Reserved Young Man
    INDONESIAN_RESERVEDYOUNGMAN = 'Indonesian_ReservedYoungMan'
    # 273. 印尼文 / Charming Girl
    INDONESIAN_CHARMINGGIRL = 'Indonesian_CharmingGirl'
    # 274. 印尼文 / Calm Woman
    INDONESIAN_CALMWOMAN = 'Indonesian_CalmWoman'
    # 275. 印尼文 / Confident Woman
    INDONESIAN_CONFIDENTWOMAN = 'Indonesian_ConfidentWoman'
    # 276. 印尼文 / Caring Man
    INDONESIAN_CARINGMAN = 'Indonesian_CaringMan'
    # 277. 印尼文 / Bossy Leader
    INDONESIAN_BOSSYLEADER = 'Indonesian_BossyLeader'
    # 278. 印尼文 / Determined Boy
    INDONESIAN_DETERMINEDBOY = 'Indonesian_DeterminedBoy'
    # 279. 印尼文 / Gentle Girl
    INDONESIAN_GENTLEGIRL = 'Indonesian_GentleGirl'
    # 280. 德文 / Friendly Man
    GERMAN_FRIENDLYMAN = 'German_FriendlyMan'
    # 281. 德文 / Sweet Lady
    GERMAN_SWEETLADY = 'German_SweetLady'
    # 282. 德文 / Playful Man
    GERMAN_PLAYFULMAN = 'German_PlayfulMan'
    # 283. 俄文 / Handsome Childhood Friend
    RUSSIAN_HANDSOMECHILDHOODFRIEND = 'Russian_HandsomeChildhoodFriend'
    # 284. 俄文 / Bright Queen
    RUSSIAN_BRIGHTHEROINE = 'Russian_BrightHeroine'
    # 285. 俄文 / Ambitious Woman
    RUSSIAN_AMBITIOUSWOMAN = 'Russian_AmbitiousWoman'
    # 286. 俄文 / Reliable Man
    RUSSIAN_RELIABLEMAN = 'Russian_ReliableMan'
    # 287. 俄文 / Crazy Girl
    RUSSIAN_CRAZYQUEEN = 'Russian_CrazyQueen'
    # 288. 俄文 / Pessimistic Girl
    RUSSIAN_PESSIMISTICGIRL = 'Russian_PessimisticGirl'
    # 289. 俄文 / Attractive Guy
    RUSSIAN_ATTRACTIVEGUY = 'Russian_AttractiveGuy'
    # 290. 俄文 / Bad-tempered Boy
    RUSSIAN_BAD_TEMPEREDBOY = 'Russian_Bad-temperedBoy'
    # 291. 意大利文 / Brave Heroine
    ITALIAN_BRAVEHEROINE = 'Italian_BraveHeroine'
    # 292. 意大利文 / Narrator
    ITALIAN_NARRATOR = 'Italian_Narrator'
    # 293. 意大利文 / Wandering Sorcerer
    ITALIAN_WANDERINGSORCERER = 'Italian_WanderingSorcerer'
    # 294. 意大利文 / Diligent Leader
    ITALIAN_DILIGENTLEADER = 'Italian_DiligentLeader'
    # 295. 阿拉伯文 / Calm Woman
    ARABIC_CALMWOMAN = 'Arabic_CalmWoman'
    # 296. 阿拉伯文 / Friendly Guy
    ARABIC_FRIENDLYGUY = 'Arabic_FriendlyGuy'
    # 297. 土耳其文 / Calm Woman
    TURKISH_CALMWOMAN = 'Turkish_CalmWoman'
    # 298. 土耳其文 / Trustworthy man
    TURKISH_TRUSTWORTHYMAN = 'Turkish_Trustworthyman'
    # 299. 乌克兰文 / Calm Woman
    UKRAINIAN_CALMWOMAN = 'Ukrainian_CalmWoman'
    # 300. 乌克兰文 / Wise Scholar
    UKRAINIAN_WISESCHOLAR = 'Ukrainian_WiseScholar'
    # 301. 荷兰文 / Kind-hearted girl
    DUTCH_KINDHEARTED_GIRL = 'Dutch_kindhearted_girl'
    # 302. 荷兰文 / Bossy leader
    DUTCH_BOSSY_LEADER = 'Dutch_bossy_leader'
    # 303. 越南文 / Kind-hearted girl
    VIETNAMESE_KINDHEARTED_GIRL = 'Vietnamese_kindhearted_girl'
    # 304. 泰文 / Serene Man
    THAI_MALE_1_SAMPLE8 = 'Thai_male_1_sample8'
    # 305. 泰文 / Friendly Man
    THAI_MALE_2_SAMPLE2 = 'Thai_male_2_sample2'
    # 306. 泰文 / Confident Woman
    THAI_FEMALE_1_SAMPLE1 = 'Thai_female_1_sample1'
    # 307. 泰文 / Energetic Woman
    THAI_FEMALE_2_SAMPLE2 = 'Thai_female_2_sample2'
    # 308. 波兰文 / Male Narrator
    POLISH_MALE_1_SAMPLE4 = 'Polish_male_1_sample4'
    # 309. 波兰文 / Male Anchor
    POLISH_MALE_2_SAMPLE3 = 'Polish_male_2_sample3'
    # 310. 波兰文 / Calm Woman
    POLISH_FEMALE_1_SAMPLE1 = 'Polish_female_1_sample1'
    # 311. 波兰文 / Casual Woman
    POLISH_FEMALE_2_SAMPLE3 = 'Polish_female_2_sample3'
    # 312. 罗马尼亚文 / Reliable Man
    ROMANIAN_MALE_1_SAMPLE2 = 'Romanian_male_1_sample2'
    # 313. 罗马尼亚文 / Energetic Youth
    ROMANIAN_MALE_2_SAMPLE1 = 'Romanian_male_2_sample1'
    # 314. 罗马尼亚文 / Optimistic Youth
    ROMANIAN_FEMALE_1_SAMPLE4 = 'Romanian_female_1_sample4'
    # 315. 罗马尼亚文 / Gentle Woman
    ROMANIAN_FEMALE_2_SAMPLE1 = 'Romanian_female_2_sample1'
    # 316. 希腊文 / Thoughtful Mentor
    GREEK_MALE_1A_V1 = 'greek_male_1a_v1'
    # 317. 希腊文 / Gentle Lady
    GREEK_FEMALE_1_SAMPLE1 = 'Greek_female_1_sample1'
    # 318. 希腊文 / Girl Next Door
    GREEK_FEMALE_2_SAMPLE3 = 'Greek_female_2_sample3'
    # 319. 捷克文 / Assured Presenter
    CZECH_MALE_1_V1 = 'czech_male_1_v1'
    # 320. 捷克文 / Steadfast Narrator
    CZECH_FEMALE_5_V7 = 'czech_female_5_v7'
    # 321. 捷克文 / Elegant Lady
    CZECH_FEMALE_2_V2 = 'czech_female_2_v2'
    # 322. 芬兰文 / Upbeat Man
    FINNISH_MALE_3_V1 = 'finnish_male_3_v1'
    # 323. 芬兰文 / Friendly Boy
    FINNISH_MALE_1_V2 = 'finnish_male_1_v2'
    # 324. 芬兰文 / Assetive Woman
    FINNISH_FEMALE_4_V1 = 'finnish_female_4_v1'
    # 325. 印地文 / Trustworthy Advisor
    HINDI_MALE_1_V2 = 'hindi_male_1_v2'
    # 326. 印地文 / Tranquil Woman
    HINDI_FEMALE_2_V1 = 'hindi_female_2_v1'
    # 327. 印地文 / News Anchor
    HINDI_FEMALE_1_V2 = 'hindi_female_1_v2'


MINIMAX_SYSTEM_VOICES = (
    MinimaxVoiceSpec(
        index=1,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.MALE_QN_QINGSE,
        name='青涩青年音色',
    ),
    MinimaxVoiceSpec(
        index=2,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.MALE_QN_JINGYING,
        name='精英青年音色',
    ),
    MinimaxVoiceSpec(
        index=3,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.MALE_QN_BADAO,
        name='霸道青年音色',
    ),
    MinimaxVoiceSpec(
        index=4,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.MALE_QN_DAXUESHENG,
        name='青年大学生音色',
    ),
    MinimaxVoiceSpec(
        index=5,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.FEMALE_SHAONV,
        name='少女音色',
    ),
    MinimaxVoiceSpec(
        index=6,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.FEMALE_YUJIE,
        name='御姐音色',
    ),
    MinimaxVoiceSpec(
        index=7,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.FEMALE_CHENGSHU,
        name='成熟女性音色',
    ),
    MinimaxVoiceSpec(
        index=8,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.FEMALE_TIANMEI,
        name='甜美女性音色',
    ),
    MinimaxVoiceSpec(
        index=9,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.MALE_QN_QINGSE_JINGPIN,
        name='青涩青年音色-beta',
    ),
    MinimaxVoiceSpec(
        index=10,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.MALE_QN_JINGYING_JINGPIN,
        name='精英青年音色-beta',
    ),
    MinimaxVoiceSpec(
        index=11,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.MALE_QN_BADAO_JINGPIN,
        name='霸道青年音色-beta',
    ),
    MinimaxVoiceSpec(
        index=12,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.MALE_QN_DAXUESHENG_JINGPIN,
        name='青年大学生音色-beta',
    ),
    MinimaxVoiceSpec(
        index=13,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.FEMALE_SHAONV_JINGPIN,
        name='少女音色-beta',
    ),
    MinimaxVoiceSpec(
        index=14,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.FEMALE_YUJIE_JINGPIN,
        name='御姐音色-beta',
    ),
    MinimaxVoiceSpec(
        index=15,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.FEMALE_CHENGSHU_JINGPIN,
        name='成熟女性音色-beta',
    ),
    MinimaxVoiceSpec(
        index=16,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.FEMALE_TIANMEI_JINGPIN,
        name='甜美女性音色-beta',
    ),
    MinimaxVoiceSpec(
        index=17,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CLEVER_BOY,
        name='聪明男童',
    ),
    MinimaxVoiceSpec(
        index=18,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CUTE_BOY,
        name='可爱男童',
    ),
    MinimaxVoiceSpec(
        index=19,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.LOVELY_GIRL,
        name='萌萌女童',
    ),
    MinimaxVoiceSpec(
        index=20,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CARTOON_PIG,
        name='卡通猪小琪',
    ),
    MinimaxVoiceSpec(
        index=21,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.BINGJIAO_DIDI,
        name='病娇弟弟',
    ),
    MinimaxVoiceSpec(
        index=22,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.JUNLANG_NANYOU,
        name='俊朗男友',
    ),
    MinimaxVoiceSpec(
        index=23,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHUNZHEN_XUEDI,
        name='纯真学弟',
    ),
    MinimaxVoiceSpec(
        index=24,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.LENGDAN_XIONGZHANG,
        name='冷淡学长',
    ),
    MinimaxVoiceSpec(
        index=25,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.BADAO_SHAOYE,
        name='霸道少爷',
    ),
    MinimaxVoiceSpec(
        index=26,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.TIANXIN_XIAOLING,
        name='甜心小玲',
    ),
    MinimaxVoiceSpec(
        index=27,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.QIAOPI_MENGMEI,
        name='俏皮萌妹',
    ),
    MinimaxVoiceSpec(
        index=28,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.WUMEI_YUJIE,
        name='妩媚御姐',
    ),
    MinimaxVoiceSpec(
        index=29,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.DIADIA_XUEMEI,
        name='嗲嗲学妹',
    ),
    MinimaxVoiceSpec(
        index=30,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.DANYA_XUEJIE,
        name='淡雅学姐',
    ),
    MinimaxVoiceSpec(
        index=31,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_RELIABLE_EXECUTIVE,
        name='沉稳高管',
    ),
    MinimaxVoiceSpec(
        index=32,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_NEWS_ANCHOR,
        name='新闻女声',
    ),
    MinimaxVoiceSpec(
        index=33,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_MATURE_WOMAN,
        name='傲娇御姐',
    ),
    MinimaxVoiceSpec(
        index=34,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_UNRESTRAINED_YOUNG_MAN,
        name='不羁青年',
    ),
    MinimaxVoiceSpec(
        index=35,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.ARROGANT_MISS,
        name='嚣张小姐',
    ),
    MinimaxVoiceSpec(
        index=36,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.ROBOT_ARMOR,
        name='机械战甲',
    ),
    MinimaxVoiceSpec(
        index=37,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_KIND_HEARTED_ANTIE,
        name='热心大婶',
    ),
    MinimaxVoiceSpec(
        index=38,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_HK_FLIGHT_ATTENDANT,
        name='港普空姐',
    ),
    MinimaxVoiceSpec(
        index=39,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_HUMOROUS_ELDER,
        name='搞笑大爷',
    ),
    MinimaxVoiceSpec(
        index=40,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_GENTLEMAN,
        name='温润男声',
    ),
    MinimaxVoiceSpec(
        index=41,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_WARM_BESTIE,
        name='温暖闺蜜',
    ),
    MinimaxVoiceSpec(
        index=42,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_MALE_ANNOUNCER,
        name='播报男声',
    ),
    MinimaxVoiceSpec(
        index=43,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_SWEET_LADY,
        name='甜美女声',
    ),
    MinimaxVoiceSpec(
        index=44,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_SOUTHERN_YOUNG_MAN,
        name='南方小哥',
    ),
    MinimaxVoiceSpec(
        index=45,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_WISE_WOMEN,
        name='阅历姐姐',
    ),
    MinimaxVoiceSpec(
        index=46,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_GENTLE_YOUTH,
        name='温润青年',
    ),
    MinimaxVoiceSpec(
        index=47,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_WARM_GIRL,
        name='温暖少女',
    ),
    MinimaxVoiceSpec(
        index=48,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_KIND_HEARTED_ELDER,
        name='花甲奶奶',
    ),
    MinimaxVoiceSpec(
        index=49,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_CUTE_SPIRIT,
        name='憨憨萌兽',
    ),
    MinimaxVoiceSpec(
        index=50,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_RADIO_HOST,
        name='电台男主播',
    ),
    MinimaxVoiceSpec(
        index=51,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_LYRICAL_VOICE,
        name='抒情男声',
    ),
    MinimaxVoiceSpec(
        index=52,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_STRAIGHTFORWARD_BOY,
        name='率真弟弟',
    ),
    MinimaxVoiceSpec(
        index=53,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_SINCERE_ADULT,
        name='真诚青年',
    ),
    MinimaxVoiceSpec(
        index=54,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_GENTLE_SENIOR,
        name='温柔学姐',
    ),
    MinimaxVoiceSpec(
        index=55,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_STUBBORN_FRIEND,
        name='嘴硬竹马',
    ),
    MinimaxVoiceSpec(
        index=56,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_CRISP_GIRL,
        name='清脆少女',
    ),
    MinimaxVoiceSpec(
        index=57,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_PURE_HEARTED_BOY,
        name='清澈邻家弟弟',
    ),
    MinimaxVoiceSpec(
        index=58,
        language='中文 (普通话)',
        voice_id=MinimaxVoice.CHINESE_MANDARIN_SOFT_GIRL,
        name='柔和少女',
    ),
    MinimaxVoiceSpec(
        index=59,
        language='中文 (粤语)',
        voice_id=MinimaxVoice.CANTONESE_PROFESSIONALHOST_F,
        name='专业女主持',
    ),
    MinimaxVoiceSpec(
        index=60,
        language='中文 (粤语)',
        voice_id=MinimaxVoice.CANTONESE_GENTLELADY,
        name='温柔女声',
    ),
    MinimaxVoiceSpec(
        index=61,
        language='中文 (粤语)',
        voice_id=MinimaxVoice.CANTONESE_PROFESSIONALHOST_M,
        name='专业男主持',
    ),
    MinimaxVoiceSpec(
        index=62,
        language='中文 (粤语)',
        voice_id=MinimaxVoice.CANTONESE_PLAYFULMAN,
        name='活泼男声',
    ),
    MinimaxVoiceSpec(
        index=63,
        language='中文 (粤语)',
        voice_id=MinimaxVoice.CANTONESE_CUTEGIRL,
        name='可爱女孩',
    ),
    MinimaxVoiceSpec(
        index=64,
        language='中文 (粤语)',
        voice_id=MinimaxVoice.CANTONESE_KINDWOMAN,
        name='善良女声',
    ),
    MinimaxVoiceSpec(
        index=65,
        language='英文',
        voice_id=MinimaxVoice.SANTA_CLAUS,
        name='Santa Claus',
    ),
    MinimaxVoiceSpec(
        index=66,
        language='英文',
        voice_id=MinimaxVoice.GRINCH,
        name='Grinch',
    ),
    MinimaxVoiceSpec(
        index=67,
        language='英文',
        voice_id=MinimaxVoice.RUDOLPH,
        name='Rudolph',
    ),
    MinimaxVoiceSpec(
        index=68,
        language='英文',
        voice_id=MinimaxVoice.ARNOLD,
        name='Arnold',
    ),
    MinimaxVoiceSpec(
        index=69,
        language='英文',
        voice_id=MinimaxVoice.CHARMING_SANTA,
        name='Charming Santa',
    ),
    MinimaxVoiceSpec(
        index=70,
        language='英文',
        voice_id=MinimaxVoice.CHARMING_LADY,
        name='Charming Lady',
    ),
    MinimaxVoiceSpec(
        index=71,
        language='英文',
        voice_id=MinimaxVoice.SWEET_GIRL,
        name='Sweet Girl',
    ),
    MinimaxVoiceSpec(
        index=72,
        language='英文',
        voice_id=MinimaxVoice.CUTE_ELF,
        name='Cute Elf',
    ),
    MinimaxVoiceSpec(
        index=73,
        language='英文',
        voice_id=MinimaxVoice.ATTRACTIVE_GIRL,
        name='Attractive Girl',
    ),
    MinimaxVoiceSpec(
        index=74,
        language='英文',
        voice_id=MinimaxVoice.SERENE_WOMAN,
        name='Serene Woman',
    ),
    MinimaxVoiceSpec(
        index=75,
        language='英文',
        voice_id=MinimaxVoice.ENGLISH_TRUSTWORTHY_MAN,
        name='Trustworthy Man',
    ),
    MinimaxVoiceSpec(
        index=76,
        language='英文',
        voice_id=MinimaxVoice.ENGLISH_GRACEFUL_LADY,
        name='Graceful Lady',
    ),
    MinimaxVoiceSpec(
        index=77,
        language='英文',
        voice_id=MinimaxVoice.ENGLISH_AUSSIE_BLOKE,
        name='Aussie Bloke',
    ),
    MinimaxVoiceSpec(
        index=78,
        language='英文',
        voice_id=MinimaxVoice.ENGLISH_WHISPERING_GIRL,
        name='Whispering girl',
    ),
    MinimaxVoiceSpec(
        index=79,
        language='英文',
        voice_id=MinimaxVoice.ENGLISH_DILIGENT_MAN,
        name='Diligent Man',
    ),
    MinimaxVoiceSpec(
        index=80,
        language='英文',
        voice_id=MinimaxVoice.ENGLISH_GENTLE_VOICED_MAN,
        name='Gentle-voiced man',
    ),
    MinimaxVoiceSpec(
        index=81,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_INTELLECTUALSENIOR,
        name='Intellectual Senior',
    ),
    MinimaxVoiceSpec(
        index=82,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_DECISIVEPRINCESS,
        name='Decisive Princess',
    ),
    MinimaxVoiceSpec(
        index=83,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_LOYALKNIGHT,
        name='Loyal Knight',
    ),
    MinimaxVoiceSpec(
        index=84,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_DOMINANTMAN,
        name='Dominant Man',
    ),
    MinimaxVoiceSpec(
        index=85,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_SERIOUSCOMMANDER,
        name='Serious Commander',
    ),
    MinimaxVoiceSpec(
        index=86,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_COLDQUEEN,
        name='Cold Queen',
    ),
    MinimaxVoiceSpec(
        index=87,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_DEPENDABLEWOMAN,
        name='Dependable Woman',
    ),
    MinimaxVoiceSpec(
        index=88,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_GENTLEBUTLER,
        name='Gentle Butler',
    ),
    MinimaxVoiceSpec(
        index=89,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_KINDLADY,
        name='Kind Lady',
    ),
    MinimaxVoiceSpec(
        index=90,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_CALMLADY,
        name='Calm Lady',
    ),
    MinimaxVoiceSpec(
        index=91,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_OPTIMISTICYOUTH,
        name='Optimistic Youth',
    ),
    MinimaxVoiceSpec(
        index=92,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_GENEROUSIZAKAYAOWNER,
        name='Generous Izakaya Owner',
    ),
    MinimaxVoiceSpec(
        index=93,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_SPORTYSTUDENT,
        name='Sporty Student',
    ),
    MinimaxVoiceSpec(
        index=94,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_INNOCENTBOY,
        name='Innocent Boy',
    ),
    MinimaxVoiceSpec(
        index=95,
        language='日文',
        voice_id=MinimaxVoice.JAPANESE_GRACEFULMAIDEN,
        name='Graceful Maiden',
    ),
    MinimaxVoiceSpec(
        index=96,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_SWEETGIRL,
        name='Sweet Girl',
    ),
    MinimaxVoiceSpec(
        index=97,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CHEERFULBOYFRIEND,
        name='Cheerful Boyfriend',
    ),
    MinimaxVoiceSpec(
        index=98,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_ENCHANTINGSISTER,
        name='Enchanting Sister',
    ),
    MinimaxVoiceSpec(
        index=99,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_SHYGIRL,
        name='Shy Girl',
    ),
    MinimaxVoiceSpec(
        index=100,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_RELIABLESISTER,
        name='Reliable Sister',
    ),
    MinimaxVoiceSpec(
        index=101,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_STRICTBOSS,
        name='Strict Boss',
    ),
    MinimaxVoiceSpec(
        index=102,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_SASSYGIRL,
        name='Sassy Girl',
    ),
    MinimaxVoiceSpec(
        index=103,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CHILDHOODFRIENDGIRL,
        name='Childhood Friend Girl',
    ),
    MinimaxVoiceSpec(
        index=104,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_PLAYBOYCHARMER,
        name='Playboy Charmer',
    ),
    MinimaxVoiceSpec(
        index=105,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_ELEGANTPRINCESS,
        name='Elegant Princess',
    ),
    MinimaxVoiceSpec(
        index=106,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_BRAVEFEMALEWARRIOR,
        name='Brave Female Warrior',
    ),
    MinimaxVoiceSpec(
        index=107,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_BRAVEYOUTH,
        name='Brave Youth',
    ),
    MinimaxVoiceSpec(
        index=108,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CALMLADY,
        name='Calm Lady',
    ),
    MinimaxVoiceSpec(
        index=109,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_ENTHUSIASTICTEEN,
        name='Enthusiastic Teen',
    ),
    MinimaxVoiceSpec(
        index=110,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_SOOTHINGLADY,
        name='Soothing Lady',
    ),
    MinimaxVoiceSpec(
        index=111,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_INTELLECTUALSENIOR,
        name='Intellectual Senior',
    ),
    MinimaxVoiceSpec(
        index=112,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_LONELYWARRIOR,
        name='Lonely Warrior',
    ),
    MinimaxVoiceSpec(
        index=113,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_MATURELADY,
        name='Mature Lady',
    ),
    MinimaxVoiceSpec(
        index=114,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_INNOCENTBOY,
        name='Innocent Boy',
    ),
    MinimaxVoiceSpec(
        index=115,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CHARMINGSISTER,
        name='Charming Sister',
    ),
    MinimaxVoiceSpec(
        index=116,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_ATHLETICSTUDENT,
        name='Athletic Student',
    ),
    MinimaxVoiceSpec(
        index=117,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_BRAVEADVENTURER,
        name='Brave Adventurer',
    ),
    MinimaxVoiceSpec(
        index=118,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CALMGENTLEMAN,
        name='Calm Gentleman',
    ),
    MinimaxVoiceSpec(
        index=119,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_WISEELF,
        name='Wise Elf',
    ),
    MinimaxVoiceSpec(
        index=120,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CHEERFULCOOLJUNIOR,
        name='Cheerful Cool Junior',
    ),
    MinimaxVoiceSpec(
        index=121,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_DECISIVEQUEEN,
        name='Decisive Queen',
    ),
    MinimaxVoiceSpec(
        index=122,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_COLDYOUNGMAN,
        name='Cold Young Man',
    ),
    MinimaxVoiceSpec(
        index=123,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_MYSTERIOUSGIRL,
        name='Mysterious Girl',
    ),
    MinimaxVoiceSpec(
        index=124,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_QUIRKYGIRL,
        name='Quirky Girl',
    ),
    MinimaxVoiceSpec(
        index=125,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CONSIDERATESENIOR,
        name='Considerate Senior',
    ),
    MinimaxVoiceSpec(
        index=126,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CHEERFULLITTLESISTER,
        name='Cheerful Little Sister',
    ),
    MinimaxVoiceSpec(
        index=127,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_DOMINANTMAN,
        name='Dominant Man',
    ),
    MinimaxVoiceSpec(
        index=128,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_AIRHEADEDGIRL,
        name='Airheaded Girl',
    ),
    MinimaxVoiceSpec(
        index=129,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_RELIABLEYOUTH,
        name='Reliable Youth',
    ),
    MinimaxVoiceSpec(
        index=130,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_FRIENDLYBIGSISTER,
        name='Friendly Big Sister',
    ),
    MinimaxVoiceSpec(
        index=131,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_GENTLEBOSS,
        name='Gentle Boss',
    ),
    MinimaxVoiceSpec(
        index=132,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_COLDGIRL,
        name='Cold Girl',
    ),
    MinimaxVoiceSpec(
        index=133,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_HAUGHTYLADY,
        name='Haughty Lady',
    ),
    MinimaxVoiceSpec(
        index=134,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CHARMINGELDERSISTER,
        name='Charming Elder Sister',
    ),
    MinimaxVoiceSpec(
        index=135,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_INTELLECTUALMAN,
        name='Intellectual Man',
    ),
    MinimaxVoiceSpec(
        index=136,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CARINGWOMAN,
        name='Caring Woman',
    ),
    MinimaxVoiceSpec(
        index=137,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_WISETEACHER,
        name='Wise Teacher',
    ),
    MinimaxVoiceSpec(
        index=138,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_CONFIDENTBOSS,
        name='Confident Boss',
    ),
    MinimaxVoiceSpec(
        index=139,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_ATHLETICGIRL,
        name='Athletic Girl',
    ),
    MinimaxVoiceSpec(
        index=140,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_POSSESSIVEMAN,
        name='Possessive Man',
    ),
    MinimaxVoiceSpec(
        index=141,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_GENTLEWOMAN,
        name='Gentle Woman',
    ),
    MinimaxVoiceSpec(
        index=142,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_COCKYGUY,
        name='Cocky Guy',
    ),
    MinimaxVoiceSpec(
        index=143,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_THOUGHTFULWOMAN,
        name='Thoughtful Woman',
    ),
    MinimaxVoiceSpec(
        index=144,
        language='韩文',
        voice_id=MinimaxVoice.KOREAN_OPTIMISTICYOUTH,
        name='Optimistic Youth',
    ),
    MinimaxVoiceSpec(
        index=145,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_SERENEWOMAN,
        name='Serene Woman',
    ),
    MinimaxVoiceSpec(
        index=146,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_MATUREPARTNER,
        name='Mature Partner',
    ),
    MinimaxVoiceSpec(
        index=147,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_CAPTIVATINGSTORYTELLER,
        name='Captivating Storyteller',
    ),
    MinimaxVoiceSpec(
        index=148,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_NARRATOR,
        name='Narrator',
    ),
    MinimaxVoiceSpec(
        index=149,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_WISESCHOLAR,
        name='Wise Scholar',
    ),
    MinimaxVoiceSpec(
        index=150,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_KIND_HEARTEDGIRL,
        name='Kind-hearted Girl',
    ),
    MinimaxVoiceSpec(
        index=151,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_DETERMINEDMANAGER,
        name='Determined Manager',
    ),
    MinimaxVoiceSpec(
        index=152,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_BOSSYLEADER,
        name='Bossy Leader',
    ),
    MinimaxVoiceSpec(
        index=153,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_RESERVEDYOUNGMAN,
        name='Reserved Young Man',
    ),
    MinimaxVoiceSpec(
        index=154,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_CONFIDENTWOMAN,
        name='Confident Woman',
    ),
    MinimaxVoiceSpec(
        index=155,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_THOUGHTFULMAN,
        name='Thoughtful Man',
    ),
    MinimaxVoiceSpec(
        index=156,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_STRONG_WILLEDBOY,
        name='Strong-willed Boy',
    ),
    MinimaxVoiceSpec(
        index=157,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_SOPHISTICATEDLADY,
        name='Sophisticated Lady',
    ),
    MinimaxVoiceSpec(
        index=158,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_RATIONALMAN,
        name='Rational Man',
    ),
    MinimaxVoiceSpec(
        index=159,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_ANIMECHARACTER,
        name='Anime Character',
    ),
    MinimaxVoiceSpec(
        index=160,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_DEEP_TONEDMAN,
        name='Deep-toned Man',
    ),
    MinimaxVoiceSpec(
        index=161,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_FUSSYHOSTESS,
        name='Fussy hostess',
    ),
    MinimaxVoiceSpec(
        index=162,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_SINCERETEEN,
        name='Sincere Teen',
    ),
    MinimaxVoiceSpec(
        index=163,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_FRANKLADY,
        name='Frank Lady',
    ),
    MinimaxVoiceSpec(
        index=164,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_COMEDIAN,
        name='Comedian',
    ),
    MinimaxVoiceSpec(
        index=165,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_DEBATOR,
        name='Debator',
    ),
    MinimaxVoiceSpec(
        index=166,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_TOUGHBOSS,
        name='Tough Boss',
    ),
    MinimaxVoiceSpec(
        index=167,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_WISELADY,
        name='Wise Lady',
    ),
    MinimaxVoiceSpec(
        index=168,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_STEADYMENTOR,
        name='Steady Mentor',
    ),
    MinimaxVoiceSpec(
        index=169,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_JOVIALMAN,
        name='Jovial Man',
    ),
    MinimaxVoiceSpec(
        index=170,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_SANTACLAUS,
        name='Santa Claus',
    ),
    MinimaxVoiceSpec(
        index=171,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_RUDOLPH,
        name='Rudolph',
    ),
    MinimaxVoiceSpec(
        index=172,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_INTONATEGIRL,
        name='Intonate Girl',
    ),
    MinimaxVoiceSpec(
        index=173,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_ARNOLD,
        name='Arnold',
    ),
    MinimaxVoiceSpec(
        index=174,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_GHOST,
        name='Ghost',
    ),
    MinimaxVoiceSpec(
        index=175,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_HUMOROUSELDER,
        name='Humorous Elder',
    ),
    MinimaxVoiceSpec(
        index=176,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_ENERGETICBOY,
        name='Energetic Boy',
    ),
    MinimaxVoiceSpec(
        index=177,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_WHIMSICALGIRL,
        name='Whimsical Girl',
    ),
    MinimaxVoiceSpec(
        index=178,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_STRICTBOSS,
        name='Strict Boss',
    ),
    MinimaxVoiceSpec(
        index=179,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_RELIABLEMAN,
        name='Reliable Man',
    ),
    MinimaxVoiceSpec(
        index=180,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_SERENEELDER,
        name='Serene Elder',
    ),
    MinimaxVoiceSpec(
        index=181,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_ANGRYMAN,
        name='Angry Man',
    ),
    MinimaxVoiceSpec(
        index=182,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_ASSERTIVEQUEEN,
        name='Assertive Queen',
    ),
    MinimaxVoiceSpec(
        index=183,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_CARINGGIRLFRIEND,
        name='Caring Girlfriend',
    ),
    MinimaxVoiceSpec(
        index=184,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_POWERFULSOLDIER,
        name='Powerful Soldier',
    ),
    MinimaxVoiceSpec(
        index=185,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_PASSIONATEWARRIOR,
        name='Passionate Warrior',
    ),
    MinimaxVoiceSpec(
        index=186,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_CHATTYGIRL,
        name='Chatty Girl',
    ),
    MinimaxVoiceSpec(
        index=187,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_ROMANTICHUSBAND,
        name='Romantic Husband',
    ),
    MinimaxVoiceSpec(
        index=188,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_COMPELLINGGIRL,
        name='Compelling Girl',
    ),
    MinimaxVoiceSpec(
        index=189,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_POWERFULVETERAN,
        name='Powerful Veteran',
    ),
    MinimaxVoiceSpec(
        index=190,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_SENSIBLEMANAGER,
        name='Sensible Manager',
    ),
    MinimaxVoiceSpec(
        index=191,
        language='西班牙文',
        voice_id=MinimaxVoice.SPANISH_THOUGHTFULLADY,
        name='Thoughtful Lady',
    ),
    MinimaxVoiceSpec(
        index=192,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_SENTIMENTALLADY,
        name='Sentimental Lady',
    ),
    MinimaxVoiceSpec(
        index=193,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_BOSSYLEADER,
        name='Bossy Leader',
    ),
    MinimaxVoiceSpec(
        index=194,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_WISELADY,
        name='Wise lady',
    ),
    MinimaxVoiceSpec(
        index=195,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_STRONG_WILLEDBOY,
        name='Strong-willed Boy',
    ),
    MinimaxVoiceSpec(
        index=196,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_DEEP_VOICEDGENTLEMAN,
        name='Deep-voiced Gentleman',
    ),
    MinimaxVoiceSpec(
        index=197,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_UPSETGIRL,
        name='Upset Girl',
    ),
    MinimaxVoiceSpec(
        index=198,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_PASSIONATEWARRIOR,
        name='Passionate Warrior',
    ),
    MinimaxVoiceSpec(
        index=199,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_ANIMECHARACTER,
        name='Anime Character',
    ),
    MinimaxVoiceSpec(
        index=200,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CONFIDENTWOMAN,
        name='Confident Woman',
    ),
    MinimaxVoiceSpec(
        index=201,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_ANGRYMAN,
        name='Angry Man',
    ),
    MinimaxVoiceSpec(
        index=202,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CAPTIVATINGSTORYTELLER,
        name='Captivating Storyteller',
    ),
    MinimaxVoiceSpec(
        index=203,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_GODFATHER,
        name='Godfather',
    ),
    MinimaxVoiceSpec(
        index=204,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_RESERVEDYOUNGMAN,
        name='Reserved Young Man',
    ),
    MinimaxVoiceSpec(
        index=205,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_SMARTYOUNGGIRL,
        name='Smart Young Girl',
    ),
    MinimaxVoiceSpec(
        index=206,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_KIND_HEARTEDGIRL,
        name='Kind-hearted Girl',
    ),
    MinimaxVoiceSpec(
        index=207,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_POMPOUSLADY,
        name='Pompous lady',
    ),
    MinimaxVoiceSpec(
        index=208,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_GRINCH,
        name='Grinch',
    ),
    MinimaxVoiceSpec(
        index=209,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_DEBATOR,
        name='Debator',
    ),
    MinimaxVoiceSpec(
        index=210,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_SWEETGIRL,
        name='Sweet Girl',
    ),
    MinimaxVoiceSpec(
        index=211,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_ATTRACTIVEGIRL,
        name='Attractive Girl',
    ),
    MinimaxVoiceSpec(
        index=212,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_THOUGHTFULMAN,
        name='Thoughtful Man',
    ),
    MinimaxVoiceSpec(
        index=213,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_PLAYFULGIRL,
        name='Playful Girl',
    ),
    MinimaxVoiceSpec(
        index=214,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_GORGEOUSLADY,
        name='Gorgeous Lady',
    ),
    MinimaxVoiceSpec(
        index=215,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_LOVELYLADY,
        name='Lovely Lady',
    ),
    MinimaxVoiceSpec(
        index=216,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_SERENEWOMAN,
        name='Serene Woman',
    ),
    MinimaxVoiceSpec(
        index=217,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_SADTEEN,
        name='Sad Teen',
    ),
    MinimaxVoiceSpec(
        index=218,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_MATUREPARTNER,
        name='Mature Partner',
    ),
    MinimaxVoiceSpec(
        index=219,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_COMEDIAN,
        name='Comedian',
    ),
    MinimaxVoiceSpec(
        index=220,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_NAUGHTYSCHOOLGIRL,
        name='Naughty Schoolgirl',
    ),
    MinimaxVoiceSpec(
        index=221,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_NARRATOR,
        name='Narrator',
    ),
    MinimaxVoiceSpec(
        index=222,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_TOUGHBOSS,
        name='Tough Boss',
    ),
    MinimaxVoiceSpec(
        index=223,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_FUSSYHOSTESS,
        name='Fussy hostess',
    ),
    MinimaxVoiceSpec(
        index=224,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_DRAMATIST,
        name='Dramatist',
    ),
    MinimaxVoiceSpec(
        index=225,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_STEADYMENTOR,
        name='Steady Mentor',
    ),
    MinimaxVoiceSpec(
        index=226,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_JOVIALMAN,
        name='Jovial Man',
    ),
    MinimaxVoiceSpec(
        index=227,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CHARMINGQUEEN,
        name='Charming Queen',
    ),
    MinimaxVoiceSpec(
        index=228,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_SANTACLAUS,
        name='Santa Claus',
    ),
    MinimaxVoiceSpec(
        index=229,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_RUDOLPH,
        name='Rudolph',
    ),
    MinimaxVoiceSpec(
        index=230,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_ARNOLD,
        name='Arnold',
    ),
    MinimaxVoiceSpec(
        index=231,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CHARMINGSANTA,
        name='Charming Santa',
    ),
    MinimaxVoiceSpec(
        index=232,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CHARMINGLADY,
        name='Charming Lady',
    ),
    MinimaxVoiceSpec(
        index=233,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_GHOST,
        name='Ghost',
    ),
    MinimaxVoiceSpec(
        index=234,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_HUMOROUSELDER,
        name='Humorous Elder',
    ),
    MinimaxVoiceSpec(
        index=235,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CALMLEADER,
        name='Calm Leader',
    ),
    MinimaxVoiceSpec(
        index=236,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_GENTLETEACHER,
        name='Gentle Teacher',
    ),
    MinimaxVoiceSpec(
        index=237,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_ENERGETICBOY,
        name='Energetic Boy',
    ),
    MinimaxVoiceSpec(
        index=238,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_RELIABLEMAN,
        name='Reliable Man',
    ),
    MinimaxVoiceSpec(
        index=239,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_SERENEELDER,
        name='Serene Elder',
    ),
    MinimaxVoiceSpec(
        index=240,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_GRIMREAPER,
        name='Grim Reaper',
    ),
    MinimaxVoiceSpec(
        index=241,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_ASSERTIVEQUEEN,
        name='Assertive Queen',
    ),
    MinimaxVoiceSpec(
        index=242,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_WHIMSICALGIRL,
        name='Whimsical Girl',
    ),
    MinimaxVoiceSpec(
        index=243,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_STRESSEDLADY,
        name='Stressed Lady',
    ),
    MinimaxVoiceSpec(
        index=244,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_FRIENDLYNEIGHBOR,
        name='Friendly Neighbor',
    ),
    MinimaxVoiceSpec(
        index=245,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CARINGGIRLFRIEND,
        name='Caring Girlfriend',
    ),
    MinimaxVoiceSpec(
        index=246,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_POWERFULSOLDIER,
        name='Powerful Soldier',
    ),
    MinimaxVoiceSpec(
        index=247,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_FASCINATINGBOY,
        name='Fascinating Boy',
    ),
    MinimaxVoiceSpec(
        index=248,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_ROMANTICHUSBAND,
        name='Romantic Husband',
    ),
    MinimaxVoiceSpec(
        index=249,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_STRICTBOSS,
        name='Strict Boss',
    ),
    MinimaxVoiceSpec(
        index=250,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_INSPIRINGLADY,
        name='Inspiring Lady',
    ),
    MinimaxVoiceSpec(
        index=251,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_PLAYFULSPIRIT,
        name='Playful Spirit',
    ),
    MinimaxVoiceSpec(
        index=252,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_ELEGANTGIRL,
        name='Elegant Girl',
    ),
    MinimaxVoiceSpec(
        index=253,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_COMPELLINGGIRL,
        name='Compelling Girl',
    ),
    MinimaxVoiceSpec(
        index=254,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_POWERFULVETERAN,
        name='Powerful Veteran',
    ),
    MinimaxVoiceSpec(
        index=255,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_SENSIBLEMANAGER,
        name='Sensible Manager',
    ),
    MinimaxVoiceSpec(
        index=256,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_THOUGHTFULLADY,
        name='Thoughtful Lady',
    ),
    MinimaxVoiceSpec(
        index=257,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_THEATRICALACTOR,
        name='Theatrical Actor',
    ),
    MinimaxVoiceSpec(
        index=258,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_FRAGILEBOY,
        name='Fragile Boy',
    ),
    MinimaxVoiceSpec(
        index=259,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CHATTYGIRL,
        name='Chatty Girl',
    ),
    MinimaxVoiceSpec(
        index=260,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_CONSCIENTIOUSINSTRUCTOR,
        name='Conscientious Instructor',
    ),
    MinimaxVoiceSpec(
        index=261,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_RATIONALMAN,
        name='Rational Man',
    ),
    MinimaxVoiceSpec(
        index=262,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_WISESCHOLAR,
        name='Wise Scholar',
    ),
    MinimaxVoiceSpec(
        index=263,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_FRANKLADY,
        name='Frank Lady',
    ),
    MinimaxVoiceSpec(
        index=264,
        language='葡萄牙文',
        voice_id=MinimaxVoice.PORTUGUESE_DETERMINEDMANAGER,
        name='Determined Manager',
    ),
    MinimaxVoiceSpec(
        index=265,
        language='法文',
        voice_id=MinimaxVoice.FRENCH_MALE_SPEECH_NEW,
        name='Level-Headed Man',
    ),
    MinimaxVoiceSpec(
        index=266,
        language='法文',
        voice_id=MinimaxVoice.FRENCH_FEMALE_NEWS_ANCHOR,
        name='Patient Female Presenter',
    ),
    MinimaxVoiceSpec(
        index=267,
        language='法文',
        voice_id=MinimaxVoice.FRENCH_CASUALMAN,
        name='Casual Man',
    ),
    MinimaxVoiceSpec(
        index=268,
        language='法文',
        voice_id=MinimaxVoice.FRENCH_MOVIELEADFEMALE,
        name='Movie Lead Female',
    ),
    MinimaxVoiceSpec(
        index=269,
        language='法文',
        voice_id=MinimaxVoice.FRENCH_FEMALEANCHOR,
        name='Female Anchor',
    ),
    MinimaxVoiceSpec(
        index=270,
        language='法文',
        voice_id=MinimaxVoice.FRENCH_MALENARRATOR,
        name='Male Narrator',
    ),
    MinimaxVoiceSpec(
        index=271,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_SWEETGIRL,
        name='Sweet Girl',
    ),
    MinimaxVoiceSpec(
        index=272,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_RESERVEDYOUNGMAN,
        name='Reserved Young Man',
    ),
    MinimaxVoiceSpec(
        index=273,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_CHARMINGGIRL,
        name='Charming Girl',
    ),
    MinimaxVoiceSpec(
        index=274,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_CALMWOMAN,
        name='Calm Woman',
    ),
    MinimaxVoiceSpec(
        index=275,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_CONFIDENTWOMAN,
        name='Confident Woman',
    ),
    MinimaxVoiceSpec(
        index=276,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_CARINGMAN,
        name='Caring Man',
    ),
    MinimaxVoiceSpec(
        index=277,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_BOSSYLEADER,
        name='Bossy Leader',
    ),
    MinimaxVoiceSpec(
        index=278,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_DETERMINEDBOY,
        name='Determined Boy',
    ),
    MinimaxVoiceSpec(
        index=279,
        language='印尼文',
        voice_id=MinimaxVoice.INDONESIAN_GENTLEGIRL,
        name='Gentle Girl',
    ),
    MinimaxVoiceSpec(
        index=280,
        language='德文',
        voice_id=MinimaxVoice.GERMAN_FRIENDLYMAN,
        name='Friendly Man',
    ),
    MinimaxVoiceSpec(
        index=281,
        language='德文',
        voice_id=MinimaxVoice.GERMAN_SWEETLADY,
        name='Sweet Lady',
    ),
    MinimaxVoiceSpec(
        index=282,
        language='德文',
        voice_id=MinimaxVoice.GERMAN_PLAYFULMAN,
        name='Playful Man',
    ),
    MinimaxVoiceSpec(
        index=283,
        language='俄文',
        voice_id=MinimaxVoice.RUSSIAN_HANDSOMECHILDHOODFRIEND,
        name='Handsome Childhood Friend',
    ),
    MinimaxVoiceSpec(
        index=284,
        language='俄文',
        voice_id=MinimaxVoice.RUSSIAN_BRIGHTHEROINE,
        name='Bright Queen',
    ),
    MinimaxVoiceSpec(
        index=285,
        language='俄文',
        voice_id=MinimaxVoice.RUSSIAN_AMBITIOUSWOMAN,
        name='Ambitious Woman',
    ),
    MinimaxVoiceSpec(
        index=286,
        language='俄文',
        voice_id=MinimaxVoice.RUSSIAN_RELIABLEMAN,
        name='Reliable Man',
    ),
    MinimaxVoiceSpec(
        index=287,
        language='俄文',
        voice_id=MinimaxVoice.RUSSIAN_CRAZYQUEEN,
        name='Crazy Girl',
    ),
    MinimaxVoiceSpec(
        index=288,
        language='俄文',
        voice_id=MinimaxVoice.RUSSIAN_PESSIMISTICGIRL,
        name='Pessimistic Girl',
    ),
    MinimaxVoiceSpec(
        index=289,
        language='俄文',
        voice_id=MinimaxVoice.RUSSIAN_ATTRACTIVEGUY,
        name='Attractive Guy',
    ),
    MinimaxVoiceSpec(
        index=290,
        language='俄文',
        voice_id=MinimaxVoice.RUSSIAN_BAD_TEMPEREDBOY,
        name='Bad-tempered Boy',
    ),
    MinimaxVoiceSpec(
        index=291,
        language='意大利文',
        voice_id=MinimaxVoice.ITALIAN_BRAVEHEROINE,
        name='Brave Heroine',
    ),
    MinimaxVoiceSpec(
        index=292,
        language='意大利文',
        voice_id=MinimaxVoice.ITALIAN_NARRATOR,
        name='Narrator',
    ),
    MinimaxVoiceSpec(
        index=293,
        language='意大利文',
        voice_id=MinimaxVoice.ITALIAN_WANDERINGSORCERER,
        name='Wandering Sorcerer',
    ),
    MinimaxVoiceSpec(
        index=294,
        language='意大利文',
        voice_id=MinimaxVoice.ITALIAN_DILIGENTLEADER,
        name='Diligent Leader',
    ),
    MinimaxVoiceSpec(
        index=295,
        language='阿拉伯文',
        voice_id=MinimaxVoice.ARABIC_CALMWOMAN,
        name='Calm Woman',
    ),
    MinimaxVoiceSpec(
        index=296,
        language='阿拉伯文',
        voice_id=MinimaxVoice.ARABIC_FRIENDLYGUY,
        name='Friendly Guy',
    ),
    MinimaxVoiceSpec(
        index=297,
        language='土耳其文',
        voice_id=MinimaxVoice.TURKISH_CALMWOMAN,
        name='Calm Woman',
    ),
    MinimaxVoiceSpec(
        index=298,
        language='土耳其文',
        voice_id=MinimaxVoice.TURKISH_TRUSTWORTHYMAN,
        name='Trustworthy man',
    ),
    MinimaxVoiceSpec(
        index=299,
        language='乌克兰文',
        voice_id=MinimaxVoice.UKRAINIAN_CALMWOMAN,
        name='Calm Woman',
    ),
    MinimaxVoiceSpec(
        index=300,
        language='乌克兰文',
        voice_id=MinimaxVoice.UKRAINIAN_WISESCHOLAR,
        name='Wise Scholar',
    ),
    MinimaxVoiceSpec(
        index=301,
        language='荷兰文',
        voice_id=MinimaxVoice.DUTCH_KINDHEARTED_GIRL,
        name='Kind-hearted girl',
    ),
    MinimaxVoiceSpec(
        index=302,
        language='荷兰文',
        voice_id=MinimaxVoice.DUTCH_BOSSY_LEADER,
        name='Bossy leader',
    ),
    MinimaxVoiceSpec(
        index=303,
        language='越南文',
        voice_id=MinimaxVoice.VIETNAMESE_KINDHEARTED_GIRL,
        name='Kind-hearted girl',
    ),
    MinimaxVoiceSpec(
        index=304,
        language='泰文',
        voice_id=MinimaxVoice.THAI_MALE_1_SAMPLE8,
        name='Serene Man',
    ),
    MinimaxVoiceSpec(
        index=305,
        language='泰文',
        voice_id=MinimaxVoice.THAI_MALE_2_SAMPLE2,
        name='Friendly Man',
    ),
    MinimaxVoiceSpec(
        index=306,
        language='泰文',
        voice_id=MinimaxVoice.THAI_FEMALE_1_SAMPLE1,
        name='Confident Woman',
    ),
    MinimaxVoiceSpec(
        index=307,
        language='泰文',
        voice_id=MinimaxVoice.THAI_FEMALE_2_SAMPLE2,
        name='Energetic Woman',
    ),
    MinimaxVoiceSpec(
        index=308,
        language='波兰文',
        voice_id=MinimaxVoice.POLISH_MALE_1_SAMPLE4,
        name='Male Narrator',
    ),
    MinimaxVoiceSpec(
        index=309,
        language='波兰文',
        voice_id=MinimaxVoice.POLISH_MALE_2_SAMPLE3,
        name='Male Anchor',
    ),
    MinimaxVoiceSpec(
        index=310,
        language='波兰文',
        voice_id=MinimaxVoice.POLISH_FEMALE_1_SAMPLE1,
        name='Calm Woman',
    ),
    MinimaxVoiceSpec(
        index=311,
        language='波兰文',
        voice_id=MinimaxVoice.POLISH_FEMALE_2_SAMPLE3,
        name='Casual Woman',
    ),
    MinimaxVoiceSpec(
        index=312,
        language='罗马尼亚文',
        voice_id=MinimaxVoice.ROMANIAN_MALE_1_SAMPLE2,
        name='Reliable Man',
    ),
    MinimaxVoiceSpec(
        index=313,
        language='罗马尼亚文',
        voice_id=MinimaxVoice.ROMANIAN_MALE_2_SAMPLE1,
        name='Energetic Youth',
    ),
    MinimaxVoiceSpec(
        index=314,
        language='罗马尼亚文',
        voice_id=MinimaxVoice.ROMANIAN_FEMALE_1_SAMPLE4,
        name='Optimistic Youth',
    ),
    MinimaxVoiceSpec(
        index=315,
        language='罗马尼亚文',
        voice_id=MinimaxVoice.ROMANIAN_FEMALE_2_SAMPLE1,
        name='Gentle Woman',
    ),
    MinimaxVoiceSpec(
        index=316,
        language='希腊文',
        voice_id=MinimaxVoice.GREEK_MALE_1A_V1,
        name='Thoughtful Mentor',
    ),
    MinimaxVoiceSpec(
        index=317,
        language='希腊文',
        voice_id=MinimaxVoice.GREEK_FEMALE_1_SAMPLE1,
        name='Gentle Lady',
    ),
    MinimaxVoiceSpec(
        index=318,
        language='希腊文',
        voice_id=MinimaxVoice.GREEK_FEMALE_2_SAMPLE3,
        name='Girl Next Door',
    ),
    MinimaxVoiceSpec(
        index=319,
        language='捷克文',
        voice_id=MinimaxVoice.CZECH_MALE_1_V1,
        name='Assured Presenter',
    ),
    MinimaxVoiceSpec(
        index=320,
        language='捷克文',
        voice_id=MinimaxVoice.CZECH_FEMALE_5_V7,
        name='Steadfast Narrator',
    ),
    MinimaxVoiceSpec(
        index=321,
        language='捷克文',
        voice_id=MinimaxVoice.CZECH_FEMALE_2_V2,
        name='Elegant Lady',
    ),
    MinimaxVoiceSpec(
        index=322,
        language='芬兰文',
        voice_id=MinimaxVoice.FINNISH_MALE_3_V1,
        name='Upbeat Man',
    ),
    MinimaxVoiceSpec(
        index=323,
        language='芬兰文',
        voice_id=MinimaxVoice.FINNISH_MALE_1_V2,
        name='Friendly Boy',
    ),
    MinimaxVoiceSpec(
        index=324,
        language='芬兰文',
        voice_id=MinimaxVoice.FINNISH_FEMALE_4_V1,
        name='Assetive Woman',
    ),
    MinimaxVoiceSpec(
        index=325,
        language='印地文',
        voice_id=MinimaxVoice.HINDI_MALE_1_V2,
        name='Trustworthy Advisor',
    ),
    MinimaxVoiceSpec(
        index=326,
        language='印地文',
        voice_id=MinimaxVoice.HINDI_FEMALE_2_V1,
        name='Tranquil Woman',
    ),
    MinimaxVoiceSpec(
        index=327,
        language='印地文',
        voice_id=MinimaxVoice.HINDI_FEMALE_1_V2,
        name='News Anchor',
    ),
)

MINIMAX_SYSTEM_VOICE_IDS = tuple(voice.voice_id for voice in MINIMAX_SYSTEM_VOICES)
MINIMAX_SYSTEM_VOICE_BY_ID = {voice.voice_id: voice for voice in MINIMAX_SYSTEM_VOICES}
MINIMAX_SYSTEM_VOICES_BY_LANGUAGE = {
    language: tuple(voice for voice in MINIMAX_SYSTEM_VOICES if voice.language == language)
    for language in sorted({voice.language for voice in MINIMAX_SYSTEM_VOICES})
}
