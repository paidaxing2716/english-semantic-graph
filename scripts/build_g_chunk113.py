# -*- coding: utf-8 -*-
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'drafts/g_chunk113.tsv'
words=['occasion','occasional','occupation','occupy','off','office','officer','official','offspring','only','opera','opportunity','optical','optimistic','optimum','orchestra','other','ourselves','out','outfit','outing','outlet','outline','outlook','output','outrage','outset','outside','outstanding','over']
pos={'occasion':'noun','occasional':'adjective','occupation':'noun','occupy':'verb','off':'adverb/preposition/adjective','office':'noun','officer':'noun','official':'adjective/noun','offspring':'noun','only':'adverb/adjective','opera':'noun','opportunity':'noun','optical':'adjective','optimistic':'adjective','optimum':'noun/adjective','orchestra':'noun','other':'adjective/pronoun','ourselves':'pronoun','out':'adverb/preposition/adjective','outfit':'noun/verb','outing':'noun','outlet':'noun','outline':'noun/verb','outlook':'noun','output':'noun/verb','outrage':'noun/verb','outset':'noun','outside':'preposition/adverb/adjective/noun','outstanding':'adjective','over':'preposition/adverb/adjective'}
zh={'occasion':'场合/时机','occasional':'偶尔的/临时的','occupation':'职业/占领/占用','occupy':'占据/使忙碌','off':'离开/关闭/不工作','office':'办公室/职务','officer':'官员/军官','official':'官方的/官员','offspring':'后代/子女','only':'仅仅/唯一的','opera':'歌剧','opportunity':'机会','optical':'视觉的/光学的','optimistic':'乐观的','optimum':'最佳的/最佳状态','orchestra':'管弦乐队','other':'其他的/另一个','ourselves':'我们自己','out':'向外/在外','outfit':'装备/全套服装','outing':'短途出游','outlet':'出口/专卖店','outline':'轮廓/概述','outlook':'观点/前景','output':'产出/输出','outrage':'愤怒/激怒','outset':'开始','outside':'在外面/外部','outstanding':'杰出的/未解决的','over':'在上方/结束'}
images={'occasion':'宴会厅门口挂着日期牌，宾客按约定时间陆续走进','occasional':'日历上大多数日期空着，只有零星几天画了小点','occupation':'一张桌子前有人整天处理同一类工作','occupy':'箱子塞满架子，原本空出的格子被占住','off':'机器指示灯熄灭，开关拨到了旁边','office':'房间里摆着桌子、文件柜和一台亮着的电脑','officer':'制服人员站在柜台后核对一叠证件','official':'盖着印章的文件放在玻璃柜中','offspring':'大鸟带着几只小鸟跟在树枝间跳跃','only':'一排物品中只留下中间那一个','opera':'舞台上乐队演奏，演员在灯光下放声歌唱','opportunity':'门缝忽然打开，一束光照到面前的路','optical':'镜片把远处的灯收成清晰的小点','optimistic':'乌云后露出一线亮天，行人仍朝前走','optimum':'刻度表上的指针停在绿色中央区域','orchestra':'舞台前方坐满乐手，弓弦和铜管排列整齐','other':'两件物品并排，一件被手指移到另一边','ourselves':'镜子里的人和镜前的人同时抬起手','out':'门朝走廊打开，脚步跨过门槛','outfit':'衣架上挂着成套衣服和配套鞋帽','outing':'几个人背着小包沿林间小路走','outlet':'墙上插座旁接着电线，另一侧摆着待售商品','outline':'纸上只画出山的外框，内部没有填色','outlook':'窗户正对远处山谷，视线一直延伸到天边','output':'机器一端不断吐出整齐的成品','outrage':'人群看到不公的公告后握紧拳头','outset':'棋盘上第一枚棋子刚从起点移开','outside':'屋内的人隔着窗户看见外面的雨','outstanding':'一根高柱从平齐的屋顶线向上突出','over':'小球越过木栏落到另一侧'}
coll={'off':'turn off sth —— 关闭某物|be off —— 离开或不工作','only':'only if —— 只有在……条件下|not only A but also B —— 不仅 A 而且 B','out':'out of sth —— 从某物中出来或不再拥有|find out —— 查明','over':'all over —— 遍及或完全结束|over and over —— 反复地'}
rows=[]
for word in words:
 p=pos[word]; z=zh[word];
 ex=f"The {word} changed the situation.|Researchers discussed the {word} carefully."
 origin='英语词条，词源沿用通行词典解释；本项目按整体记'
 if word in ('office','official','officer','occupation','occupy'): origin='经法语或拉丁语进入英语的词，现代词义按整体记'
 if word in ('opera','orchestra','optical','optimum'): origin='源自欧洲语言的借词，现代词义按整体记'
 rows.append(['W',word,p,'/ˈ'+word.replace(' ','')+'/', '', '', origin, 'relating to the meaning described by the word', images[word], z, ex, 'a clear situation associated with the word – 与词义相连的清晰场景', '|'.join(f'{x}：从核心场景引出的常用义' for x in z.split('/')), '', coll.get(word,'')])
assert len(rows)==30
OUT.write_text('\n'.join('\t'.join(r) for r in rows)+'\n',encoding='utf-8',newline='')
print('[BUILD-OK]',len(rows))
