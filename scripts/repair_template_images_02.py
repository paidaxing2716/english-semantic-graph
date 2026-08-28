import json
from pathlib import Path
p=Path('data/words.json');d=json.loads(p.read_text(encoding='utf-8'));m={
'prayer':'礼拜堂里的人低头合掌，烛火在安静的空气中轻轻摇动','preach':'讲台上的人翻开经书，台下的人抬头专心听讲','predecessor':'新任者站在旧办公桌旁，墙上还挂着上一任的照片','pregnant':'检查屏幕显示一个小小轮廓，准父母握住彼此的手','prejudice':'两扇门贴着不同标签，来人尚未了解就先被挡在一边','preliminary':'正式比赛前，运动员在空场上做最后一轮热身','premise':'地契和钥匙放在桌上，屋主指向房子的边界','premium':'两件商品并排摆放，其中一件包装更精致、价格更高','prestige':'颁奖台中央的奖杯被灯光照亮，观众起身鼓掌','presumably':'桌上的线索都指向同一个答案，人们据此作出推断','pretty':'窗台上的小花颜色柔和，旁边的人停下来微笑','priest':'穿长袍的人站在祭坛前，手里捧着一本打开的书','privacy':'窗帘拉紧后，房间里的谈话不再传到走廊','private':'一扇写着姓名的门关着，陌生人不能随意进入','problem':'桌上的齿轮卡住不转，工程师拿着工具寻找原因','productivity':'同一排机器持续运转，传送带上的成品越来越多','profit':'账本两栏之间留下余额，收入超过了支出','profitable':'田地收成装满货车，卖出后留下了可观的余额','profound':'井口向下望去看不见底，声音落下很久才传回来','programme':'墙上的时间表把活动按顺序排成一列','prolong':'道路施工把原定的终点向远处推开','prompt':'铃声一响，工作人员立刻起身处理眼前的请求','propaganda':'街角贴满统一口号的海报，行人反复看到同一套说法','prophet':'一位预言者指向远方的天空，听众安静等待将来','protein':'实验室的模型由一串折叠的分子链组成','prototype':'工作台上摆着第一个样机，工程师围着它检查细节','psychiatry':'诊室里医生和来访者面对面交谈，桌上放着记录本','psychology':'几张图卡摆在桌上，研究者记录人的选择和反应','puppet':'细线悬在舞台上方，手指一动，下面的布制身影便抬起手臂','purify':'浑水流过层层滤网，出口处变得清澈'}
wm={w['id']:w for w in d['words']};assert all(k in wm for k in m)
for k,v in m.items():wm[k]['core_image']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('[OK]',len(m))
