import json
from pathlib import Path
p=Path('data/words.json');d=json.loads(p.read_text(encoding='utf-8'));wm={w['id']:w for w in d['words']}
m={
'purple':'一块深色布料铺在白墙旁，色彩对比格外明显','puzzle':'桌上散着形状各异的拼片，缺口还没有完全补齐','pyramid':'沙漠中央堆着层层缩小的石阶，顶端指向天空','quantify':'实验员把液体逐份倒入有刻度的量筒','quantitative':'报告中的数字排成表格，每一项都对应明确数量','quantity':'几个箱子并排码放，标签标出各自装了多少','quarrel':'两个人隔着桌子指向对方，声音越来越高','quartz':'透明晶体躺在岩石裂缝里，切面反射出细碎亮光','queer':'展柜里一件形状出人意料的物品让参观者停步','quench':'火苗碰到水流后立刻缩小，最后只剩一缕白烟','queue':'售票窗前的人沿栏杆排成一条弯曲的长线','quiet':'图书馆里的人翻页很轻，窗外的雨声清楚可闻','quilt':'许多不同颜色的布块缝在一起，铺成厚实的被面','quit':'桌边的人放下工具，转身走出正在进行的工作','quiver':'弓弦轻轻颤动，箭尖也跟着细微摇摆','quiz':'教室里每个人面前放着一张小卷，正在逐题作答','quota':'公告板上画着一个空格，达到规定数额后才能填满','quote':'书页上有一段文字被引号圈出，旁边标着来源','rabbit':'草地边一双长耳朵从灌木后探出，随后跳过小路','racial':'地图上的不同群体用不同颜色标注，研究者比较其分布','radical':'树根从土层深处向四周伸展，牢牢抓住地面','rainbow':'雨后的天空横跨着七色弧线，尽头落在远处山后','rarely':'日历上大多数日期空白，只有极少几天画着标记','reader':'有人坐在窗边翻页，手指沿着纸上的行字移动','readily':'柜台上的材料已分门别类，伸手便能取到所需那份','reading':'台灯照着摊开的书页，读者逐行停下来理解','rebellion':'广场上人群举起不同旗帜，队伍拒绝听从旧命令','recall':'仓库管理员逐件核对清单，把已发出的箱子叫回','recent':'日历最靠近今天的一格被圈出，墨迹还很新','recipe':'厨房台面上摆着原料和步骤清单，厨师按顺序准备'}
assert set(m)<=set(wm),set(m)-set(wm)
for k,v in m.items():wm[k]['core_image']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('[OK]',len(m))
