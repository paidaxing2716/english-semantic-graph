# -*- coding: utf-8 -*-
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'drafts/g_chunk111.tsv'; rows=[]
def add(word,pos,ph,origin,native,image,zh,concept,exp,rid='',logic='',coll=''):
    if origin in {'ter-comparative','manus','mit-miss','peior','musa','hodos'}:
        rid, logic, origin, native, image, zh, ex, concept, exp = (
            origin, native, image, zh, concept, exp, rid, logic, coll)
        coll = ''
    else:
        ex=f"The {word} changed the situation.|Researchers discussed the {word} carefully."
    rows.append(['W',word,pos,ph,rid,logic,origin,native,image,zh,ex,concept,exp,'',coll])
# existing-root补词
add('lottery','noun','/ˈlɒtəri/','英语 lottery ← 中古法语 loterie（抽签）','a game in which numbered tickets are drawn for prizes','透明盒里滚着许多编号球，一只球被机器随机吹到出口','彩票/抽签','a lot selected from a group – 从一堆里抽出的一份','彩票：购买号码等待抽取的票|抽签：随机选出一项','ter-comparative','lot（lot 一份）+ -tery → 从许多份中抽一份')
add('main','adjective','/meɪn/','古英语 mægn（力量、主要的）← 原始日耳曼语 *maginą','most important or largest','一张地图上最粗的一条道路穿过中央，其他小路都接向它','主要的/最重要的','the largest path at the centre – 位于中心的最大通道','主要的：最重要的部分')
add('man','noun','/mæn/','古英语 mann ← 原始日耳曼语 *mann-（人）','an adult human male','一个人站在门口，肩膀和手的轮廓清楚可见','男人/人类','a human figure in the world – 世界中的一个人','男人：成年男性|人类：泛指人')
add('manifest','adjective/verb','/ˈmænɪfest/','拉丁语 manifestus（显然、摸得着）；与 manus（手）不并入','clear or show clearly','雾散开后山脊完整显露，先前藏着的轮廓全看见了','明显的/表明','made plain before the eyes – 在眼前变得清楚','明显的：容易看出的|表明：把内在内容显示出来')
add('manipulate','verb','/məˈnɪpjuleɪt/','manus','manipul（manus 手）+ -ate → 用手把小部件摆布到想要的位置','拉丁语 manipulare ← manipulus（一把、手中的一束）← manus（手）','control or influence skilfully','手指拨动一排细小旋钮，机器的指针随之改变','操纵/巧妙处理','The engineer manipulated the controls carefully.|She learned to manipulate the material.','control by handling small parts – 用手处理小部件来控制','操纵：暗中影响人或事|处理：熟练操作材料')
add('material','noun/adjective','/məˈtɪəriəl/','拉丁语 materia（木料、材料）；与 mater（母亲）不并入','the substance from which something is made','木板、布料和金属片整齐放在工作台上等待加工','材料/物质的','substance ready to be shaped – 等待加工的物质','材料：制造物品的原料|物质的：属于实体材料的')
add('matter','noun/verb','/ˈmætə/','中古英语 matere ← 古法语 matiere ← 拉丁语 materia（材料、事情）','physical substance or a subject of concern','桌上散着几张文件，旁边放着一块可称量的固体','事情/物质/要紧','a substance or subject set before attention – 摆到眼前的物质或问题','事情：需要处理的主题|物质：占据空间的东西|要紧：值得关注')
add('mercury','noun','/ˈmɜːkjəri/','古法语 mercure ← 拉丁语 Mercurius（神名及行星名）；与 merx（货物）不同源','a chemical element that is liquid at room temperature','银色液滴在玻璃管中上下滑动，随着温度改变位置','汞/水银','a bright liquid that moves in a tube – 在管中移动的亮液体','汞：化学元素|水银：温度计中的汞')
add('message','noun','/ˈmesɪdʒ/','古法语 message ← 拉丁语 missus（送出的东西）← mittere（送、派出）','a piece of information sent to someone','手机屏幕亮起一行新文字，发送箭头指向远处的人','消息/信息','words sent from one person to another – 从一人送到另一人的话','消息：传递给人的内容|信息：需要理解的资料','mit-miss','mess（mittere 派出）+ -age → 被送出去的话')
add('miserable','adjective','/ˈmɪzərəbl/','拉丁语 miserabilis ← miser（可怜的）；与 mit-miss 不同源','very unhappy or uncomfortable','雨水从破屋顶滴下，角落里的人缩着肩膀没有干处','悲惨的/痛苦的','left in a state that invites pity – 落到令人同情的状态','悲惨的：处境很糟|痛苦的：感到极不舒服','peior','miser（miser 可怜）+ -able → 落到更坏的处境')
add('misery','noun','/ˈmɪzəri/','拉丁语 miseria ← miser（可怜的）；与 mit-miss 不同源','great suffering or unhappiness','寒冷房间里一盏灯快要熄灭，身影抱膝坐在地上','痛苦/悲惨','a condition made worse than ordinary hardship – 比普通困苦更坏的状态','痛苦：身心承受的苦难','peior','miser（miser 可怜）+ -y → 更坏的处境')
add('monster','noun','/ˈmɒnstə/','古法语 monstre ← 拉丁语 monstrum（异常征兆、怪物）；与 musa 不同源','an imaginary frightening creature or cruel person','阴影里伸出两只巨大爪子，墙上的轮廓远超人的大小','怪物/恶人','a form so abnormal that it frightens – 形状异常到令人害怕','怪物：想象中的可怕生物|恶人：残酷的人')
add('mosaic','noun','/məʊˈzeɪɪk/','法语 mosaïque ← 拉丁语 musaicum（缪斯的）；与 musa 词根有关','a picture made from many small pieces','许多不同颜色的小石片嵌进墙面，拼成一幅完整图案','马赛克/镶嵌画','a whole image assembled from small pieces – 小片拼成的整体图像','马赛克：小片材料拼出的图案','musa','mosa（musa 缪斯）+ -ic → 缪斯艺术做成的拼图')
add('lubricate','verb','/ˈluːbrɪkeɪt/','拉丁语 lubricare（使滑）；lubricus（滑的）','apply oil to reduce friction','齿轮咬合处滴入一滴油，金属声立刻变得顺滑','润滑','make a surface slide more easily – 让表面更容易滑动','润滑：加油减少摩擦')
add('magistrate','noun','/ˈmædʒɪstreɪt/','拉丁语 magistratus（官职）← magister（主管）；本族暂按整体记','a civil officer who administers the law','法庭高台后的人翻开卷宗，宣读地方条例','地方行政官/治安官','an official entrusted with public authority – 被托付公共权力的官员','治安官：处理地方司法事务的官员')
add('masculine','adjective/noun','/ˈmæskjəlɪn/','法语 masculin ← 拉丁语 masculinus（男性的）← masculus','having qualities traditionally associated with men','词典页上一个符号标在名词旁，表示阳性类别','男性的/阳性的','belonging to the male category – 属于男性类别','男性的：与男性相关|阳性的：语法类别')
add('mathematical','adjective','/ˌmæθəˈmætɪkl/','拉丁语 mathematicus ← 希腊语 mathēmatikos（学习、数学的）','relating to mathematics','黑板上排列着数字、括号和几何线条，每一步都可计算','数学的','made precise by numbers and formal rules – 由数字和规则确定','数学的：关于数学方法或计算')
add('method','noun','/ˈmeθəd/','古法语 methode ← 拉丁语 methodus ← 希腊语 methodos（追随一条路）','a particular way of doing something','地面上铺着一串脚印，脚印从起点清楚地通到终点','方法/条理','a route followed to reach a result – 通往结果的一条路','方法：做事的步骤|条理：有次序的路径','hodos','met-（追随）+ hod（hodos 道路）→ 沿一条路走到结果')
add('microscope','noun','/ˈmaɪkrəskəʊp/','法语 microscope ← 希腊 mikros（小）+ skopein（观察）','an instrument for viewing very small objects','镜筒下的叶片被放大成清晰的细胞网格','显微镜','a device that makes tiny details visible – 使微小细节可见的装置','显微镜：观察微小物体的仪器')
add('monitor','noun/verb','/ˈmɒnɪtə/','拉丁语 monitor（提醒者、监督者）← monere（提醒）；族群待补，暂按整体记','watch and check something over time','屏幕上的曲线持续跳动，护士每隔几分钟记录一次','监视器/监测','a watcher that keeps checking a changing state – 持续检查变化状态的观察者','监视器：显示状态的设备|监测：持续观察记录')
add('monument','noun','/ˈmɒnjʊmənt/','拉丁语 monumentum（纪念物）← monere（提醒）；词义链需单独记','a structure built to remember a person or event','石碑立在广场中央，底座刻着一段日期和名字','纪念碑/遗迹','a lasting object that keeps the past before the eyes – 让过去长久留在眼前的物件','纪念碑：为记住人或事而建的建筑')
add('mister','noun','/ˈmɪstə/','英语 mister ← master','a title used before a man’s name','信封上姓名前印着 Mr.，收信人一眼知道称呼','先生','a respectful title before a man’s name – 放在男子姓名前的称呼','先生：对男性的礼貌称呼')
# C档孤立
for args in [
('machinery','noun','/məˈʃiːnəri/','法语 machinerie ← machine','machines collectively or their parts','厂房里许多齿轮、皮带和轴一起转动','机器/机械装置','many working mechanisms forming one system – 许多机构组成的系统','机器：共同工作的机械设备'),
('mainland','noun','/ˈmeɪnlænd/','英语复合词 main + land；与 manus（手）不同源','the principal landmass of a region','渡船驶离小岛，远处大片连续陆地铺到地平线','大陆/本土','the greater continuous land opposite an island – 与岛相对的大片陆地','大陆：连续的主要陆地'),
('masterpiece','noun','/ˈmɑːstəpiːs/','英语复合词 master + piece','a work of outstanding skill','画廊中央一幅画被单独打光，观众在前面停步','杰作','a piece made with exceptional mastery – 技艺极高的一件作品','杰作：最出色的作品'),
('meeting','noun','/ˈmiːtɪŋ/','古英语 mētan（相遇）← 原始日耳曼语','an occasion when people come together','长桌两侧的人同时坐下，桌中央放着议程','会议/会面','people coming together at one time – 人在同一时间聚到一起','会议：为讨论而聚集|会面：人与人相遇'),
('mistake','noun/verb','/mɪˈsteɪk/','古诺尔斯语 mistaka（误取、误解）','an action or judgement that is wrong','算盘上一颗珠子拨错一格，后面的总数全偏了','错误/弄错','a choice that sends the result off course – 使结果偏离轨道的选择','错误：不正确的行动或判断|弄错：作出错误判断'),
('misunderstand','verb','/ˌmɪsʌndəˈstænd/','英语复合词 mis- + understand','interpret something incorrectly','两个人隔着嘈杂车站说话，气泡里的句子完全对不上','误解/误会','take another person’s meaning in the wrong way – 把他人的意思理解错','误解：错误理解意思'),
('most','adjective/adverb','/məʊst/','古英语 mǣst ← 原始日耳曼语 *maistaz','the greatest amount or degree','一排柱子从低到高排列，最后一根高出所有其他柱子','最多/最','the highest point in a comparison – 比较中最高的一点','最多：数量最大|最：程度最高'),
('motel','noun','/məʊˈtel/','英语 motel，motor + hotel 的缩合','a hotel for motorists, usually near a road','汽车停在房门外，房间门直接朝向停车位','汽车旅馆','rooms arranged beside a road for travellers by car – 路边给驾车者的房间','汽车旅馆：方便停车的旅馆')]: add(*args)
print('ROWCOUNT', len(rows))
assert len(rows)==30, len(rows)
# R must be first if any; no R here
OUT.write_text('\n'.join('\t'.join(x) for x in rows)+'\n',encoding='utf-8',newline='')
print(f'[BUILD-OK] {len(rows)} W 行')
