import json
from pathlib import Path
p=Path('data/words.json');d=json.loads(p.read_text(encoding='utf-8'));m={
'recipient':'包裹上的收件人姓名写在正面，快递员把它递到对方手中','reciprocal':'两个人轮流把球传给对方，每次动作都得到回应','recognition':'领奖台上的人听到名字后走上前，观众认出并鼓掌','recognize':'街角的人抬头看清来者，马上认出那张熟悉的脸','recollect':'散落的照片一张张拼回，旧日场景逐渐在脑中恢复','recreation':'公园里的人放下工作，在草地和球场上轻松活动','recruit':'新成员站进队伍，教练给他发放制服和编号','rectangle':'纸张四条边首尾相接，四个角都是直角','redundant':'仓库里堆着两台完全相同的备用机器，其中一台长期不用','reflect':'阳光照到平静水面，岸边的树影清楚地映回来','reflection':'镜面里的人影与站在面前的人同时抬手','refrain':'歌手唱到熟悉的一句时停住，手指示意乐队暂不继续','refuge':'风暴来临时，动物钻进岩洞深处躲避风雨','refugee':'人群背着行李离开受灾的家，沿安全路线向远处走','refund':'售票处把钱退回顾客手中，原来的票被收回','refute':'两份证据摆在桌面上，其中一份直接推翻了前面的说法','regret':'夜里的人盯着已经寄出的信，手指反复摩挲空信封','rehearsal':'演员在空舞台上反复走位，灯光和台词逐项核对','reinforce':'桥梁下方加装粗钢梁，承重结构变得更牢','reluctant':'门口的人握着把手迟迟不进，脚尖仍朝向外面','remain':'搬空的房间里只剩一把椅子和墙上的钟','remainder':'一堆物品分走几份后，旁边留下没有取走的部分','remains':'古老建筑倒塌后，石墙残段仍留在草地上','remark':'会议中有人举手，说出一句引起大家注意的话','remarkable':'平静的队列中一个人完成了异常出色的动作，所有人转头观看','remedy':'破损的管道找到合适零件，水流恢复正常','remember':'抽屉里的旧照片让人想起多年前的那一天','remind':'手机在约定时间响起，提示主人别忘记一件事','remnant':'布料剪裁后，桌角留下几块窄窄的余料','render':'电脑把模型转换成带光影的完整画面'}
wm={w['id']:w for w in d['words']};assert len(m)==30 and set(m)<=set(wm)
for k,v in m.items():wm[k]['core_image']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('[OK]',len(m))
