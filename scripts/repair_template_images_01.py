import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; p=ROOT/'data/words.json'
images={
'plastic':'透明模具里倒入热浆，冷却后变成轻而硬的彩色物件','playground':'孩子们在秋千、滑梯和沙坑之间跑来跑去，鞋印铺满地面','plea':'一个人双手合十站在门前，抬头等待对方答应','plead':'律师站在法庭中央，向法官陈述理由并请求改变决定','pledge':'两个人在桌边交换写好名字的纸，随后郑重握手','plight':'漏雨的屋檐下只剩一张椅子，行李和积水挤在脚边','plough':'铁犁切开田土，身后的泥垄一道道翻向两侧','plumber':'工具箱摊在水槽下，扳手正拧紧一段漏水的管道','plunge':'跳水者从高台直落水面，四周的空气迅速被甩在身后','pneumonia':'病房里的人呼吸急促，胸前贴着监测电极','poison':'瓶口贴着骷髅标志，几滴液体落进隔离的玻璃杯','poisonous':'鲜艳的浆果挂在灌木上，旁边立着警示牌','polish':'布团反复擦过铜盘，暗淡表面逐渐映出灯光','polite':'客人站在门边侧身让路，先等年长者走进房间','pollute':'黑烟从烟囱飘向河面，水边的鱼群开始躲开','pollution':'河岸漂着塑料瓶，灰色泡沫聚在排水口','pond':'树林低处围着一圈静水，荷叶贴着水面展开','popular':'广场入口排起长队，大家都朝同一个摊位走去','population':'地图上的小点密密麻麻聚在沿海城市周围','porcelain':'薄白杯子放在软布上，边缘透着细细的光','portrait':'画布上的脸部轮廓和眼神被一笔笔固定下来','portray':'演员站在布景前，用姿态重现画中人物的神情','poster':'墙上贴着一张大幅彩纸，日期和醒目的图案吸引路人','postman':'邮差背着帆布袋沿街走，把信件逐户投入信箱','pot':'炉火上的陶罐咕嘟作响，蒸汽从盖边一缕缕冒出','potato':'刚挖出的块茎沾满泥土，堆在木筐里等待清洗','poultry':'院子里的鸡鸭围着食槽啄食，羽毛在阳光下移动','pound':'铁锤连续落下，木桩一点点陷进坚实的地面','poverty':'狭小房间里只有一张旧床，窗缝透进冷风','powder':'研钵中的固体被杵头磨成细白颗粒','prayer':'教堂长椅上的人低头合掌，烛火在指缝间摇动','preach':'讲台上的人翻开经书，台下的人安静听着','predecessor':'接任者站在旧办公桌旁，墙上还挂着上一任的照片','pregnant':'检查室屏幕显示胎儿轮廓，准父母握住彼此的手','preliminary':'正式比赛前，运动员在空场上做最后一轮热身','premise':'门口的地契和钥匙放在桌上，屋主指向房间边界','premium':'两件商品并排摆放，其中一件包装更精致、价格也更高','prestige':'颁奖台中央的奖杯被灯光照亮，观众起身鼓掌'}
d=json.loads(p.read_text(encoding='utf-8')); wm={w['id']:w for w in d['words']}
missing=[]
for wid,img in images.items():
 if wid not in wm: missing.append(wid)
 else: wm[wid]['core_image']=img
if missing: raise SystemExit('missing: '+','.join(missing))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('[OK]',len(images))
