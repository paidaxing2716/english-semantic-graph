# -*- coding: utf-8 -*-
"""生成 chunk110；内容按列表 join，保留 15 列尾部制表符。"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'drafts/g_chunk110.tsv'
W=[]
R=[]
def r(rid,variants,origin,cc,image,edef,slug,czh,dom):
    R.append(['R',rid,variants,origin,cc,image,edef,slug,czh,dom])
def w(word,pos,ph,rid,logic,origin,native,image,zh,ex,concept,exp,coll=''):
    W.append(['W',word,pos,ph,rid,logic,origin,native,image,zh,ex,concept,exp,'',coll])

def iso(word,pos,ph,origin,native,image,zh,ex,concept,exp='',coll=''):
    w(word,pos,ph,'','',origin,native,image,zh,ex,concept,exp,coll)

r('migrare','migr','拉丁语 migrare（迁移、搬动）；in-migrare 迁入，ex-migrare 迁出','to move from one place to another / 从一处迁到另一处','一群候鸟沿海岸线飞行，旧栖地在身后，新栖地在前方','to move from one place to another','move','迁移','domain-transfer')

w('log','noun','/lɒɡ/','logos','log（logos 条理、话语）→ 把事情记成一段有条理的话','英语 log ← 希腊语 logos（话语、记录）','a written record of events or a thick piece of wood','桌边摊着一本值班簿，每次发生的事按时间添上一行','日志/记录/原木','The captain kept a daily log.|A log floated down the river.','a line set down in an ordered record – 按次序留下的一行','日志：按时间记下发生的事|原木：一段被锯下的树干，形状像一截记录的条目')
w('logic','noun','/ˈlɒdʒɪk/','logos','logic（logos 条理）→ 让每一步都接得上前一步','英语 logic ← 古法语 logique ← 希腊语 logikē（推理之学）','a way of reasoning in which each step follows the last','几块木牌首尾相接，前一块的缺口正好接住后一块','逻辑/推理','Her argument has sound logic.|There is no logic in doing it twice.','steps that hold together – 前后相扣的推理','逻辑：每一步都由前一步推出|推理：按这种相扣的次序思考')
w('logical','adjective','/ˈlɒdʒɪkl/','logos','logic（logos 条理）+ -al → 属于有条理推理的','英语 logical ← logic ← 希腊语 logos（话语、条理）','following a clear and sensible line of reasoning','一排箭头从一个小牌指向下一个，没有倒退或跳格','合乎逻辑的/合理的','That is the most logical explanation.|She made a logical decision.','ordered enough to follow – 次序清楚，跟得上','合乎逻辑的：前后关系清楚|合理的：选择能由已知情况推出')
w('magnificent','adjective','/mæɡˈnɪfɪsnt/','fac','magn（maior 大）+ fic（facere 做）+ -ent → 做得大而显眼','英语 magnificent ← 拉丁语 magnificus（做得伟大的）','extremely impressive, beautiful, or grand','大厅穹顶铺满金箔，阳光一照整面墙都在发亮','壮丽的/宏伟的/极好的','The palace has a magnificent hall.|She gave a magnificent performance.','made so grand that it commands the eye – 做得大到夺走目光','壮丽的：建筑或景象铺陈得极大|极好的：表现好到让人称赞')
iso('longitude','noun','/ˈlɒndʒɪtjuːd/','拉丁语 longitude（长度、经度）；借入英语','the angular distance east or west of a meridian','地图上从北到南画满弧线，船的位置落在其中一条上','经度','The map shows the island’s longitude.|Longitude is measured east or west.','a position measured along the globe – 沿球面标出的位置','经度：从本初子午线向东或向西量的位置')
iso('magnitude','noun','/ˈmæɡnɪtjuːd/','拉丁语 magnitudo（大小、重要性）；本项目暂不并入已有的「更大」词族','greatness in size, importance, or intensity','同一把尺子量三件物体，刻度一格格向更大处延伸','大小/重要性/震级','The magnitude of the task surprised us.|Scientists measured the earthquake’s magnitude.','the scale by which something is judged – 衡量大小强弱的尺度','大小：物体或数量的尺度|震级：地震强度的等级')
iso('malignant','adjective','/məˈlɪɡnənt/','拉丁语 malignus（恶意、有害的）← malus；与 peior（更坏）支不同源','having a harmful or destructive effect','显微镜下的细胞挤成不规则团块，边缘不断侵入旁边','恶性的/恶意的','The scan revealed a malignant tumour.|He made a malignant remark.','harm that spreads into what surrounds it – 有害力量向周围侵入','恶性的：疾病会侵入扩散|恶意的：话语带着伤人的意图')
# ---- A 档其余词：先按现有根逐项核过后补入 ----
w('master','noun','/ˈmɑːstə/','maior','magis（maior 更大）+ -ter → 更大的那一个，掌握全局的人','古英语 mægister ← 拉丁语 magister（主管、教师），与 maior（更大的）同源','a person with authority or great skill','一只手握着整串钥匙，房间里的人都等他决定','主人/大师/掌握','The master opened the locked door.|She became a master of the craft.','the one greater in rank or skill – 地位或本领更高的那一个','主人：掌管一处的人|大师：技艺高到别人来学习的人')
w('medical','adjective','/ˈmedɪkl/','medius','medi（medius 中间）+ -ical → 处理身体中间状态的','拉丁语 medicalis ← medicus（医治的），与 mederi（治疗）相关','relating to medicine or the treatment of illness','白大褂口袋里装着听诊器，医生俯身检查病人的呼吸','医学的/医疗的','She needs medical advice.|The medical team arrived quickly.','concerning the care of the body – 关于照料身体的','医学的：属于医学知识|医疗的：用于诊断或治疗')
w('medicine','noun','/ˈmedsən/','medius','medi（medius 中间）→ 在病痛与康复之间施加的处理','拉丁语 medicina（医术、药物）← medicus（医治的）','the science or practice of treating illness, or a drug','棕色药瓶立在床头，量匙里盛着一小口液体','医学/药物','The doctor prescribed new medicine.|This medicine relieved her pain.','a treatment placed between illness and recovery – 介于病痛与康复之间的处理','医学：治疗疾病的学问|药物：服下以改善病情的东西')
w('meditate','verb','/ˈmedɪteɪt/','medius','medit（medius 中间）→ 把心放在事情中间反复看','拉丁语 meditari（思量、默想），与 mederi 同源词族','think deeply and focus one’s mind for a time','人坐在安静房间中央，呼吸缓慢，桌上问题被一遍遍翻看','沉思/冥想','She meditates for ten minutes daily.|He meditated on the difficult choice.','hold the mind steadily on one point – 心稳稳停在一点上','沉思：反复思考问题|冥想：安静集中注意力')
w('meditation','noun','/ˌmedɪˈteɪʃn/','medius','meditat（medius 中间）+ -ion → 心停在中间反复观看的过程','拉丁语 meditatio（思考、默想）← meditari','the practice of focusing the mind deeply','窗边坐着一个人，眼睛闭着，窗外的声音逐渐退到远处','冥想/沉思','Meditation helped her sleep.|He found peace through meditation.','a sustained inward focus – 持续向内集中的状态','冥想：集中注意力的练习|沉思：对一个问题长时间思量')
w('memo','noun','/ˈmeməʊ/','memor','memor（memor 记得）→ 留给自己的一小张记忆纸','英语 memo 是 memorandum 的缩略，源自拉丁 memorandum（应记之事）← memor','a short written message used in an organization','办公桌角压着一张便签，几行字提醒明早要办的事','备忘录/便笺','I left a memo on your desk.|The manager sent a memo to staff.','words kept so a matter is not forgotten – 留下文字免得忘记','备忘录：组织内部传达事项的短文')
w('mine','verb/noun','/maɪn/','minus-less','min（minus 少）→ 从地下取出属于自己的那一份','古英语 min；动词 mine（开采）来自中古英语 mine ← 古法语 mine（矿坑），与拉丁 minus 近形不同源','extract minerals from the ground; a place or device containing them','黑暗坑道里灯光照着岩壁，工人把一块石头从层层土里取出','开采/矿井/我的','Workers mine coal underground.|That book is mine.','take something out from a hidden place – 从藏着的地方取出东西','开采：从地下取矿物|mine 作代词：表示属于说话人的东西')
w('mineral','noun','/ˈmɪnərəl/','minus-less','min（minus 少）→ 从大块岩石里取出的细小成分','中古英语 mineral ← 古法语 minéral ← 拉丁语 mineralis（矿物的）','a natural substance found in rocks or soil','岩石剖面露出几条不同颜色的晶脉，镐尖敲下一小块','矿物','The soil contains useful minerals.|Iron is an important mineral.','a distinct substance taken from the earth – 从土地里分出的物质','矿物：自然形成的无机物')
w('minimize','verb','/ˈmɪnɪmaɪz/','minus-less','mini（minus 少）+ -ize → 把量压到尽可能小','英语 minimize ← minimum ← 拉丁 minimus（最小的）← minor/minus','reduce something to the smallest possible amount','一团纸被反复压进小盒，空隙越来越少','使最小化/降低','We must minimize unnecessary costs.|The design minimizes heat loss.','press the amount down toward the least – 把数量压向最少','使最小化：减到可能的最低程度|降低：让损失或影响变小')
w('movie','noun','/ˈmuːvi/','mov','mov（movere 移动）→ 连续移动的画面被投到幕上','英语 movie 是 moving picture 的缩略形式；moving ← move ← 拉丁语 movere（移动）；与 paint 一族无关','a film shown in a cinema or on a screen','白幕上一格格光影快速更换，人物仿佛真的从左走到右','电影/影片','We watched a movie after dinner.|The movie tells a moving story.','moving pictures arranged into a story – 连续移动的画面组成故事','电影：在屏幕上连续播放的影像故事')

# ---- B 档 ----
iso('member','noun','/ˈmembə/','拉丁语 membrum（肢体、部分）；本项目尚未建其词族根','a person or thing belonging to a group','圆桌旁每个座位都放着一张写有名字的卡片','成员/部件/肢体','She is a member of the committee.|The leg is a key member of the machine.','one part counted within a whole – 被整体数进去的一部分','成员：属于团体的人|部件：机器中承担作用的一部分')
iso('messenger','noun','/ˈmesɪndʒə/','中古英语 messenger ← message + -er','a person who carries a message','一个人夹着信封穿过院子，把信交到另一双手里','信使/送信人','The messenger arrived before noon.|A messenger brought the news.','one who carries words from one place to another – 把话带过去的人','信使：替别人传递消息的人')
w('migrate','verb','/maɪˈɡreɪt/','migrare','mig（migrare 迁移）+ -ate → 从一处迁到另一处','拉丁语 migrare（迁移）；英语 migrate 由此借入','move from one region or habitat to another','候鸟排成一条线越过海岸，旧巢在身后越来越远','迁徙/迁移','Many birds migrate south in winter.|Workers migrate to the cities.','move camp to another place – 把栖身处搬到另一处','迁徙：动物随季节换栖息地|迁移：人群或系统换到另一地')
iso('mistress','noun','/ˈmɪstrəs/','中古英语 maistresse ← 古法语 maistresse（女主人、女教师）','a woman in a position of authority or a man’s extramarital partner','一位女士站在宅邸门口，手里握着整串钥匙','女主人/情妇','The mistress of the house greeted us.|He was accused of having a mistress.','a woman holding a household or private relationship role – 掌着一处位置的女人','女主人：管理一所房屋的女性|情妇：婚外的亲密伴侣')
iso('multitude','noun','/ˈmʌltɪtjuːd/','拉丁语 multitudo（众多）← multus（多）；与库中 plus-more 根不同根，暂按整体记','a very large number of people or things','广场上密密麻麻站满人，远处只看见一片移动的颜色','大量/众多的人','A multitude of fans filled the stadium.|A multitude of problems remained.','many counted together as one crowd – 许多被看成一片','大量：数量很多|众多的人：聚成一片的人群')
iso('loudspeaker','noun','/ˌlaʊdˈspiːkə/','英语复合词 loud + speaker','an apparatus that makes sound louder','黑色喇叭架在台边，声波一圈圈扩到最后一排','扬声器/扩音器','The announcement came through a loudspeaker.|A loudspeaker stood beside the stage.','a voice projected across a space – 把声音推到远处','扬声器：把电信号变成较大声音的装置')
iso('mankind','noun','/mænˈkaɪnd/','古英语 mann + kind，英语复合词','the human race','许多不同年龄的人围着一张地球仪，手都伸向同一片陆地','人类','The invention changed mankind.|Mankind faces a shared challenge.','all people viewed as one kind – 所有人合成的一类','人类：全体人的总称')
iso('many','noun/pronoun','/ˈmeni/','古英语 manig ← 原始日耳曼语 *managaz','a large number of people or things','一只篮子里塞满同样的小球，数也数不完','许多/很多','Many students joined the club.|How many books did you read?','a count extending well beyond a few – 数量远超过几个','许多：数量较大|many + 复数名词：询问或说明数量')
iso('mingle','verb','/ˈmɪŋɡl/','古英语 mengian ← 原始日耳曼语 *mangjaną','mix or combine with something else','两杯不同颜色的液体倒进同一只玻璃杯，边界慢慢消失','混合/交往','Oil will not mingle with water.|Guests mingled after dinner.','separate streams losing their boundaries – 分开的东西失去边界','混合：物质彼此掺在一起|交往：人群中来回交谈')
iso('missing','adjective','/ˈmɪsɪŋ/','古英语 missan（错过、失去）','not present or unable to be found','墙上的相框留着一个空钉子，原来的照片不见了','缺失的/失踪的','One page is missing from the book.|The police searched for the missing child.','an expected place left empty – 应在的位置空了','缺失的：物件或部分不在|失踪的：人找不到了')
iso('monotonous','adjective','/məˈnɒtənəs/','希腊语 monotonos（单一音调的），经拉丁语入英语','never changing in tone or pattern and therefore boring','传送带不停吐出完全相同的盒子，机器声一拍不变','单调的','The lecture became monotonous.|He spoke in a monotonous voice.','one unbroken note repeated – 一个音调反复不变','单调的：声音或活动缺少变化')
iso('more','noun/adverb','/mɔː/','古英语 māra ← 原始日耳曼语 *maizô','a greater amount or degree','同一只杯子又被添了一勺，液面继续往上升','更多/更','We need more time.|She asked for more water.','an amount added beyond what is there – 在已有基础上再加','more + noun：数量增加|more + adjective：程度增加', 'more than sth —— 多于某物')
iso('mother','noun','/ˈmʌðə/','古英语 mōdor ← 原始日耳曼语 *mōdēr','a female parent','婴儿蜷在怀里，手指紧紧抓住衣襟','母亲/母体','Her mother called yesterday.|The plant is the mother of several varieties.','the source that gives life or origin – 给予生命或源头的那一个','母亲：生育或养育孩子的女性|母体：产生其他事物的源头')
# ensure exactly 30 and write
assert len(W)==30, len(W)
for row in W:
    assert len(row)==15
    assert len(row[10].split('|'))==2
OUT.write_text('\n'.join('\t'.join(x) for x in R+W)+'\n',encoding='utf-8',newline='')
print(f'[BUILD-OK] {len(R)} R 行，{len(W)} W 行')
