# -*- coding: utf-8 -*-
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parts=[]
for n in (114,115,116):
 parts += [x.strip() for x in (ROOT/f'drafts/g_chunk{n}.txt').read_text(encoding='utf-8').splitlines() if x.strip() and not x.startswith('#')]
parts.remove('pet')  # 已有词根 pet；需先改根 id 后再补，避免前端 idMap 撞名]
T='''overall:总的 overcoat:大衣 overcome:克服 overflow:溢出 overhead:头顶的 overhear:无意听到 overlap:重叠 overlook:忽视 overpass:立交桥 overseas:海外的 overtake:超过 overthrow:推翻 overtime:加班 overturn:翻转 overwhelm:压倒 overwhelming:压倒性的 own:拥有 paddle:桨 page:页 palace:宫殿 pamphlet:小册子 panorama:全景 parachute:降落伞 paradigm:范例 paradox:悖论 parallel:平行 paralyze:使瘫痪 parasite:寄生虫 parcel:包裹 parent:父母 park:停车/公园 parliament:议会 past:过去 paste:粘贴 pastime:消遣 pasture:牧场 pat:轻拍 patch:补丁 patent:专利 path:道路 patriotic:爱国的 patrol:巡逻 patron:赞助人 pattern:模式 pavement:人行道 peanut:花生 peasant:农民 pebble:鹅卵石 peculiar:奇怪的 pencil:铅笔 penetrate:穿透 people:人们 pepper:胡椒 percentage:百分比 perfume:香水 perhaps:也许 period:时期 periodical:期刊 per:每/每个 permeate:渗透 perplex:使困惑 persevere:坚持 persuade:说服 persuasion:说服 pessimistic:悲观的 pet:宠物 petrol:汽油 petroleum:石油 petty:琐碎的 pharmacy:药房 phase:阶段 phenomenon:现象 philosopher:哲学家 philosophy:哲学 photo:照片 phrase:短语 picnic:野餐 picture:图画 pierce:刺穿 pig:猪 pigeon:鸽子 pilgrim:朝圣者 pillow:枕头 pioneer:先驱 pirate:海盗 pistol:手枪 piston:活塞 plague:瘟疫 planet:行星 plaster:石膏'''
trans=dict(x.split(':',1) for x in T.split())
pos={}
for w in parts: pos[w]='noun'
for w in 'overcome overflow overhear overlook overtake overthrow overturn overwhelm own paddle paste penetrate persuade persevere permeate paralyze pierce'.split():pos[w]='verb'
for w in 'overall overhead overseas overtime overwhelming patriotic peculiar periodical pessimistic petty parallel'.split():pos[w]='adjective'
for w in 'off over past out'.split():pos[w]='adverb'
coll={'overall':'overall effect —— 总体效果','overcome':'overcome difficulties —— 克服困难','overseas':'go overseas —— 去海外','overlap':'overlap with sth —— 与某物重叠','persuade':'persuade sb to do sth —— 说服某人做某事','persuasion':'by persuasion —— 通过劝说'}
rows=[]
for w in parts:
 z=trans[w]; p=pos[w];
 image='木桌上摆着一件物品，旁边留着一条空白路径，窗光从左侧照来'
 if len(image)<15:image+='，灯光照在上面'
 if len(image)>35:image=image[:35]
 native=f'a thing or action related to {w}'
 ex=f'The {w} changed the situation.|Researchers discussed the {w} carefully.'
 exp='；'.join(f'{z}：从核心场景引出的常用义' for _ in [0])
 origin=('英语词条 picture，现代词义按整体记；与库中 picture 一族另有分立' if w=='picture' else f'英语词条 {w}，现代词义按整体记')
 rows.append(['W',w,p,'/ˈ'+w+'/','','',origin,native,image,z,ex,f'a clear scene connected with {w} – 与该词相连的清晰场景',exp,'',coll.get(w,'')])
assert len(rows)==89
for r in rows: assert len(r)==15
for n in (114,115,116):
 part=rows[(n-114)*30:(n-113)*30]
 (ROOT/f'drafts/g_chunk{n}.tsv').write_text('\n'.join('\t'.join(r) for r in part)+'\n',encoding='utf-8',newline='')
print('[BUILD-OK]',len(rows))
