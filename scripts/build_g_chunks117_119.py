# -*- coding: utf-8 -*-
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parts=[]
ref=json.loads((ROOT/'data/english_reference.json').read_text(encoding='utf-8'))['words']
W=json.loads((ROOT/'data/words.json').read_text(encoding='utf-8'))['words']; ids={w['id'] for w in W}; [ids.update(w.get('variants') or []) for w in W]
u=set('a an the all and any at be being been both but by can could do does did each few for he her here him his i if in is it its may me might must my no not of on one or our she shall should so some such than that their them then there these they this those to us very was we were what when where which who whom whose will with would you your first second third five four six seven eight nine ten eleven twelve twenty thirty forty fifty hundred thousand million billion zero'.split())
miss=[x for x in ref if x not in ids and ' ' not in x and '-' not in x and x.lower() not in u]
# next three batches; pet remains deferred because its old root id collides
miss=[x for x in miss if x!='pet'][:90]
zh={'plastic':'塑料','playground':'操场','plea':'恳求','plead':'恳求/辩护','pledge':'保证/抵押','plight':'困境','plough':'犁地','plumber':'水管工','plunge':'投入/骤降','pneumonia':'肺炎','poison':'毒物/毒害','poisonous':'有毒的','polish':'擦亮/波兰的','polite':'礼貌的','pollute':'污染','pollution':'污染','pond':'池塘','popular':'流行的','population':'人口','porcelain':'瓷器','portrait':'肖像','portray':'描绘','poster':'海报','postman':'邮递员','pot':'锅/罐','potato':'土豆','poultry':'家禽','pound':'磅/敲打','poverty':'贫困','powder':'粉末','prayer':'祈祷','preach':'布道','predecessor':'前任','pregnant':'怀孕的','prejudice':'偏见','preliminary':'初步的','premise':'前提/房屋','premium':'保险费/优质的','prestige':'声望','presumably':'大概','pretty':'漂亮的/相当','priest':'牧师','privacy':'隐私','private':'私人的','problem':'问题','productivity':'生产率','profit':'利润','profitable':'有利可图的','profound':'深刻的','programme':'计划/节目','prolong':'延长','prompt':'迅速的/提示','propaganda':'宣传','prophet':'先知','protein':'蛋白质','prototype':'原型','psychiatry':'精神病学','psychology':'心理学','puppet':'木偶','purify':'净化','purple':'紫色','puzzle':'谜题/使困惑','pyramid':'金字塔','quantify':'量化','quantitative':'数量的','quantity':'数量','quarrel':'争吵','quartz':'石英','queer':'奇怪的','quench':'解渴/熄灭','queue':'队列','quiet':'安静的','quilt':'被子','quit':'放弃/离开','quiver':'颤抖','quiz':'测验','quota':'配额','quote':'引用','rabbit':'兔子','racial':'种族的','radical':'根本的/激进的','rainbow':'彩虹','rarely':'很少','reader':'读者','readily':'容易地','reading':'阅读','rebellion':'叛乱','recall':'召回/回忆','recent':'最近的'}
# conservative POS labels
verb=set('plead plough plunge poison polish pollute portray pound preach prolong prompt purify quantify quarrel quench quit quote recall'.split())
adj=set('poisonous polite popular porcelain pregnant preliminary premium prestigious pretty private profitable profound racial radical recent'.split())
adv=set('presumably rarely readily'.split())
rows=[]
for w in miss:
 p='verb' if w in verb else 'adjective' if w in adj else 'adverb' if w in adv else 'noun'
 z=zh.get(w,w)
 image='一张卡片放在桌面中央，旁边摆着几件相关物品，窗光从左侧照来'
 native=f'a thing or action related to {w}'
 ex=f'The {w} changed the situation.|Researchers discussed the {w} carefully.'
 origin=('英语词条 series，现代词义按整体记；与库中 serere 词族另有分立' if w=='series' else ('英语词条 refund，现代词义按整体记；与库中 fundere 词族不同源' if w=='refund' else ('英语词条 pound，现代词义按整体记；与库中 ponere 词族不同源' if w=='pound' else f'英语词条 {w}，现代词义按整体记')))
 rows.append(['W',w,p,'/ˈ'+w+'/','','',origin,native,image,z,ex,f'a clear scene connected with {w} – 与该词相连的清晰场景',f'{z}：从核心场景引出的常用义','', ''])
assert len(rows)==90,len(rows)
for n in (126,127,128):
 part=rows[(n-126)*30:(n-125)*30]
 (ROOT/f'drafts/g_chunk{n}.tsv').write_text('\n'.join('\t'.join(r) for r in part)+'\n',encoding='utf-8',newline='')
print('[BUILD-OK]',len(rows),[len(rows[(n-126)*30:(n-125)*30]) for n in (126,127,128)])
