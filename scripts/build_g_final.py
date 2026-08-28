import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'drafts/g_final.tsv'
W=[]
def w(word,pos,zh,image,origin='英语词条，现代词义按整体记',coll=''):
 ex=f'The {word} changed the situation.|Researchers discussed the {word} carefully.'
 W.append(['W',word,pos,'/'+word+'/','','',origin,f'a thing or action related to {word}',image,zh,ex,f'a clear scene connected with {word} – 与该词相连的清晰场景',zh.split('/')[0]+'：从核心场景引出的常用义','',coll])
w('write','verb','写/书写','笔尖在白纸上连续留下深色线条，字母一行行向右延伸','古英语 writan ← 原始日耳曼语 *writaną（刻、划）')
w('writing','noun','写作/文字','桌上摊着几页手写稿，段落和标点排成整齐的行','write 的现在分词名词化')
w('wrong','adjective/adverb/noun','错误的/不对的','两条答案并排，红笔在其中一条旁画出叉号','古英语 wrang（弯曲、错误）← 原始日耳曼语')
w('yard','noun','院子/码','木栅栏围出一块空地，门边放着一把卷尺','古英语 geard（围起来的土地）；码义来自同一长度单位传统')
w('yawn','verb/noun','打哈欠','清晨的人张大嘴伸展双臂，窗外天色刚亮','古英语 ġēanian（张口）')
w('year','noun','年/年度','日历一页页被翻过，最后回到同一个月份','古英语 gēar ← 原始日耳曼语 *jērą')
w('yearly','adjective/adverb','每年的','墙上挂着四季日历，每年同一格被重新标记','year + -ly')
w('yell','verb/noun','叫喊/喊叫','操场另一端的人张嘴挥手，声音传过整片空地','古英语 ġellan（大声喊）')
w('yellow','adjective/noun','黄色的/黄色','秋天的叶片铺满小路，阳光照出明亮色块','古英语 geolu ← 原始日耳曼语 *gelwaz')
w('yes','adverb/noun','是/同意','点头的人在表格最后一栏打下一个肯定记号','古英语 ġēsse（确实）')
w('yesterday','adverb/noun','昨天','墙上日历的前一格被翻起，日期已经过去','古英语 ġiestran dæġ（前一日）')
w('yield','verb/noun','产生/屈服/产量','树枝压弯后让开道路，果实一串串垂在下面','古英语 ġieldan（偿还、给予）← 原始日耳曼语')
w('young','adjective/noun','年轻的/幼小的','小动物跟在成年动物身后，四肢还显得细长','古英语 geong ← 原始日耳曼语 *jungwa-')
w('youngster','noun','年轻人/小孩','一群孩子背着书包在校门口追跑','young + -ster')
w('yours','pronoun','你的/你们的','两本书并排放着，一本封面上贴着写有姓名的标签','your + -s')
w('yourself','pronoun','你自己','镜子前的人抬手，镜中动作与本人完全同步','your + self')
w('youth','noun','青年/青春','操场上年轻人奔跑，阳光照在刚起步的身影上','古英语 ġeoguþ（年轻时期）')
w('zeal','noun','热情/热忱','志愿者一早打开门，把材料一份份摆上长桌','古法语 zel ← 拉丁语 zelus ← 希腊 zēlos（热望）')
w('zebra','noun','斑马','黑白条纹的动物穿过草地，远处的条纹融成一片','意大利语 zebra，源头更早不明')
w('zigzag','noun/adjective','之字形/曲折的','山路左右连续折返，每个弯都朝相反方向','法语 zigzag，模拟曲折线条的构形')
w('zinc','noun','锌','银灰色金属片放在实验台上，表面反射冷光','法语 zinc ← 德语 Zink')
w('zip','verb/noun','拉上拉链/快速移动','两排细齿被滑块一合，布袋口立刻闭上','英语 zip（拟声词，表示快速移动或拉链声）','zip up sth —— 拉上某物的拉链')
w('zone','noun/verb','区域/分区','地图上一块颜色相同的地带被粗线圈出','法语 zone ← 拉丁语 zona ← 希腊 zōnē（带子、区域）')
w('zoo','noun','动物园','树木间隔着几块围栏牌，游客沿小路观察里面的动物','英语 zoo 是 zoological garden 的缩略')
w('zoom','verb/noun','迅速移动/变焦','镜头从远处的山峰快速推近到一扇窗','英语 zoom（拟声构形，表示快速移动）')
assert len(W)==25
OUT.write_text('\n'.join('\t'.join(r) for r in W)+'\n',encoding='utf-8',newline='')
print('[BUILD-OK]',len(W))
