# -*- coding: utf-8 -*-
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'drafts/g_chunk112.tsv'; rows=[]
def add(word,pos,ph,origin,native,image,zh,concept,exp,rid='',logic='',coll=''):
 ex=f"The {word} changed the situation.|Researchers discussed the {word} carefully."
 if word in {'notice','number'}:
  rid = {'notice':'gnoscere','number':'numerus'}[word]
  logic = {'notice':'not（noscere 知道）+ -ice → 被意识捕捉到','number':'numer（numerus 数）→ 用来计数和识别的标记'}[word]
 rows.append(['W',word,pos,ph,rid,logic,origin,native,image,zh,ex,concept,exp,'',coll])
def iso(*a): add(*a)
def root(*a): add(*a[0:8],a[8],a[9],a[10])
add('mind','noun/verb','/maɪnd/','古英语 gemynd（记忆、心智）← 原始日耳曼语 *ga-mundiz；与 mens（心）不同源','the part of a person that thinks and remembers','一盏灯照着书页，人的注意力停在其中一行','头脑/心思/介意','the inner place where thoughts are held – 收纳念头的内在处所','头脑：思考与记忆的能力|介意：把某事放在心上')
add('municipal','adjective','/mjuːˈnɪsɪpl/','拉丁语 municipalis（市政的）← municipium（自治市）；与 mun（公共服务）词族分立','relating to a town or its local government','市政厅门前挂着城市徽章，工作人员处理本地事务','市政的/地方政府的','belonging to a self-governing town – 属于自治城镇的','市政的：与城市地方政府有关')
add('muscle','noun','/ˈmʌsl/','古法语 muscle ← 拉丁语 musculus（小老鼠、小肌肉）← mus（老鼠）；词源链不传可学联系','a body tissue that produces movement','手臂弯曲时皮肤下的线条隆起又放松','肌肉','tissue that tightens to move the body – 收紧以带动身体的组织','肌肉：收缩产生动作的身体组织')
add('muscular','adjective','/ˈmʌskjələ/','拉丁语 muscularis（肌肉的）← musculus；与 musa（缪斯）不同源','having well-developed muscles','运动员抬起重物，肩背轮廓在衣服下清楚凸起','肌肉发达的/强壮的','built with visibly strong muscle – 肌肉轮廓明显强健','肌肉发达的：肌肉很强|强壮的：体格有力')
add('mushroom','noun','/ˈmʌʃruːm/','古法语 mousseron；英语 mushroom，词源更早不明','a fungus with a rounded cap and stem','潮湿树根旁一夜冒出几顶圆伞，颜色深浅各不相同','蘑菇','a rounded growth rising from the ground – 从地面长出的圆顶物','蘑菇：有菌盖和菌柄的真菌')
add('mutter','verb/noun','/ˈmʌtə/','中古英语 muteren（低声说）；拟声起源','speak in a low voice that is difficult to hear','嘴唇动着但旁边的人听不清','咕哝/喃喃自语','words released too softly for clear hearing – 声音太低而听不清的话','咕哝：低声不清楚地说')
add('mysterious','adjective','/mɪˈstɪəriəs/','古法语 misterie ← 拉丁 mysterium ← 希腊 mystērion（秘密仪式）','difficult to understand or explain','雾中的房门半掩，门后只有一线看不清的灯光','神秘的/难以解释的','kept beyond ordinary understanding – 藏在通常理解之外','神秘的：难以解释或看透')
add('mystery','noun','/ˈmɪstəri/','古法语 mystere ← 拉丁 mysterium ← 希腊 mystērion（秘密仪式）','something difficult to explain or understand','桌上只有一把钥匙和一张没有署名的纸条','谜/神秘事物','a matter whose answer remains hidden – 答案仍藏着的事情','谜：尚未解开的疑问|神秘事物：难以理解的事情')
add('narrative','noun/adjective','/ˈnærətɪv/','拉丁语 narrativus ← narrare（讲述）','a spoken or written account of connected events','一串卡片按时间排开，每张接着下一张讲完一段经历','叙述/故事','events connected and told in sequence – 按次序连起来讲的事件','叙述：对事件的连贯讲述|故事：讲出的事件线')
add('neglect','verb/noun','/nɪˈɡlekt/','拉丁语 neglegere（不理会、疏忽）← nec + legere；与库中 legere 一族的「拾取、挑选」另有分立','fail to give proper care or attention','花盆放在窗角，土已干裂，叶子垂下却没人浇水','忽视/疏忽','leaving a duty unattended – 把应照料的事搁在一边','忽视：不注意应处理的事|疏忽：没有尽到照料义务')
add('negligible','adjective','/ˈneɡlɪdʒəbl/','拉丁语 negligi（不理会）← neglegere；与 legere（拾取）这一支不同源','so small or unimportant that it can be ignored','天平两边放着物体，新增的那粒尘土几乎不改变指针','微不足道的/可忽略的','too slight to affect the result – 轻到不影响结果','微不足道的：数量或影响极小')
add('negotiate','verb','/nɪˈɡəʊʃieɪt/','拉丁语 negotiari（做生意、处理事务）← negotium（事务）','try to reach an agreement by discussion','长桌两边的人交换文件，最后把笔同时放在一份协议上','谈判/协商','work through terms until both sides can agree – 逐条处理条件达成一致','谈判：通过讨论达成协议|协商：共同处理条件')
add('newspaper','noun','/ˈnjuːzˌpeɪpə/','英语复合词 news + paper','a printed publication containing current events','早餐桌上摊开一张大纸，标题和照片排成多栏','报纸','printed pages carrying recent public information – 印着近期公共消息的纸页','报纸：定期刊登新闻的出版物')
add('next','adjective/adverb','/nekst/','古英语 niehst（最近的）← 原始日耳曼语 *nēhwistaz','following immediately in time or order','队伍里一个人紧挨着前一个，轮到他时向前一步','下一个/紧接着','the one immediately following – 紧跟在后面的那一个','下一个：顺序紧接的一项|紧接着：时间或位置相邻')
add('nor','conjunction','/nɔː/','古英语 nor（ne + or）','used to introduce a further negative statement','两盏灯都熄着，门口的牌子写着两个选择都不成立','也不/也没有','a second negative joined to the first – 接在第一个否定后面的第二个否定','nor + 助动词 + 主语 —— 前句否定后补充另一项也不成立')
add('notwithstanding','preposition/conjunction','/ˌnɒtwɪðˈstændɪŋ/','英语 not + withstanding（站在对面）；现代复合结构','in spite of something','大雨打在伞面上，行人仍沿原路往前走','尽管/虽然','a fact present but not stopping what follows – 情况存在却没拦住后事','notwithstanding sth —— 尽管某事|notwithstanding that 从句 —— 虽然某事')
add('northeast','noun/adjective','/ˌnɔːθˈiːst/','英语复合词 north + east','the direction midway between north and east','指南针的指针停在北和东之间的斜角','东北/东北的','the diagonal direction between north and east – 北与东之间的斜向','东北：方向或地区')
add('northwest','noun/adjective','/ˌnɔːθˈwest/','英语复合词 north + west','the direction midway between north and west','指南针的指针停在北和西之间的斜角','西北/西北的','the diagonal direction between north and west – 北与西之间的斜向','西北：方向或地区')
add('nothing','pronoun','/ˈnʌθɪŋ/','古英语 nān þing（没有东西）','not anything; no single thing','打开的盒子里空空的，连一张纸片也没有','什么也没有/无','an empty set with no item in it – 集合里没有任何一项','什么也没有：不存在任何东西')
add('notice','noun/verb','/ˈnəʊtɪs/','古法语 notice ← 拉丁语 notitia（知道、认识）← noscere；与 gnoscere 根的现有成员同源，直接补挂','become aware of something through seeing or hearing','窗边的人抬头，立刻看到玻璃上的一道新裂纹','注意/通知','a detail brought into awareness – 被意识捕捉到的细节','注意：察觉某事|通知：让别人知道的消息')
add('noticeable','adjective','/ˈnəʊtɪsəbl/','英语 noticeable ← notice ← 拉丁 notitia（知道）','easy to see or recognize','白墙上的一块深色污迹远远就能看见','明显的/显著的','clear enough to attract attention – 清楚到会吸引注意','明显的：容易被察觉|显著的：差异较大')
add('now','adverb/noun','/naʊ/','古英语 nū ← 原始日耳曼语 *nu','at the present time','钟面上的秒针正指着最上方，正在发生的事没有过去','现在/目前','the point of time being lived – 正在经历的这一刻','现在：此刻|目前：当前阶段')
add('nuclear','adjective','/ˈnjuːkliə/','拉丁语 nuclearis（核心的）← nucleus（小核）；与 nucleus 词族暂未建根','relating to the nucleus of an atom or cell','剖开的圆形结构中央有一个密实的小点，周围层层环绕','核的/原子能的','belonging to a dense central core – 属于致密中心的','核的：关于原子或细胞中心|原子能的：利用原子核能量')
add('numb','adjective/verb','/nʌm/','古英语 numen（取走感觉）← 原始日耳曼语 *nemaną','unable to feel normally','手在雪水里泡久后，指尖被轻轻捏也没有反应','麻木的/使麻木','feeling temporarily taken away – 感觉暂时被拿走','麻木的：感觉减弱|使麻木：使失去感觉')
add('number','noun/verb','/ˈnʌmbə/','拉丁 numerus（数、数量）；与库中 numerus 根同源，当前直接按现有根补挂','a word or symbol expressing a quantity','黑板上排列着一串符号，每个符号对应一组物体','数字/数量/编号','a mark used to count or identify – 用来计数或识别的标记','数字：表示数量的符号|数量：可计数的多少|编号：识别顺序')
add('nutrition','noun','/njuːˈtrɪʃn/','拉丁语 nutritio（滋养）← nutrire（喂养、滋养）','the process of obtaining food needed for health','餐盘里的食物经过消化示意图，箭头指向身体各处','营养/营养学','food taken in and used to sustain life – 摄入并维持生命的食物','营养：维持健康所需的养分|营养学：研究养分的学科','nutrire','nutr（nutrire 滋养）+ -ition → 被身体吸收的滋养')
add('obscure','adjective/verb','/əbˈskjʊə/','拉丁语 obscurus（黑暗、隐蔽）；族群不足，暂按整体记','not well known or difficult to understand','厚雾遮住山谷，远处的路只剩看不清的轮廓','模糊的/鲜为人知的/使模糊','hidden from clear view – 藏在清楚视线之外','模糊的：不清楚|鲜为人知的：很少被人知道|使模糊：遮住清晰轮廓')
add('observation','noun','/ˌɒbzəˈveɪʃn/','拉丁语 observatio ← observare（观察、留意）','the act of watching carefully or a comment based on it','研究员透过玻璃逐项记录实验装置的变化','观察/观察结果','careful watching turned into a record – 仔细观看后留下的记录','观察：认真察看|观察结果：从察看得到的结论')
add('observe','verb','/əbˈzɜːv/','拉丁语 observare（注意、观察）← ob- + servare；本项目暂不建 servare 根','watch carefully and notice what happens','望远镜对准远处鸟巢，记录者一动不动地记下每次动作','观察/遵守','keep watch and mark what is seen – 守着并记下所见','观察：仔细看|遵守：按要求照做')
add('obstacle','noun','/ˈɒbstəkl/','古法语 obstacle ← 拉丁 obstaculum（挡住之物）← obstare（站在前面）','something that blocks progress or movement','小路中央横着倒木，行人只能停下寻找绕行处','障碍/阻碍','something standing across the path – 横在路上的东西','障碍：挡住前进的事物|阻碍：使进展变慢')
assert len(rows)==30,len(rows)
OUT.write_text('\n'.join('\t'.join(x) for x in rows)+'\n',encoding='utf-8',newline='')
print('[BUILD-OK]',len(rows))
