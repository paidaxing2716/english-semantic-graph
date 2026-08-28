#!/usr/bin/env python3
"""修复 audit_all.py 发现的确定性例句问题。"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
SECOND={
'figurative':'The phrase is figurative, not literal.',
'disfigure':'The accident disfigured the old statue.',
'configuration':'Change the configuration before restarting.',
'compress':'The tool can compress large images quickly.',
'formal':'He wore formal clothes to the ceremony.',
'inform':'We will inform you of the final decision.',
'transform':'Rain transformed the dry valley into a lake.',
'reform':'The bill aims to reform the tax system.',
'attract':'Bright flowers attract bees in spring.',
'distract':'Loud music can distract tired drivers.',
'tractor':'The tractor pulled the trailer uphill.',
'oppose':'Local groups oppose the proposed highway.',
'mission':'The spacecraft completed its mission safely.',
'inspect':'Please inspect the equipment before use.',
'prospect':'The job offers good prospects for promotion.',
'spectator':'Every spectator received a printed ticket.',
'expect':'We expect the package tomorrow morning.',
'describe':'Words cannot describe the beautiful view.',
'prescribe':'The doctor prescribed rest and plenty of water.',
'manuscript':'Her manuscript was accepted by the publisher.',
'educate':'Good schools educate students for independent life.',
'reduce':'Turning off lights can reduce energy use.',
'import':'The country imports coffee from several regions.',
'export':'The company exports machines across Asia.',
'transport':'Buses transport workers to the factory.',
'portable':'This portable charger fits in my pocket.',
'select':'The committee selected three finalists.',
'state':'Please state your reasons clearly.',
}
def main():
    wp=DATA/'words.json'; ep=DATA/'examples.json'
    words=json.loads(wp.read_text(encoding='utf-8')); examples=json.loads(ep.read_text(encoding='utf-8'))
    wm={w['id']:w for w in words['words']}; by={}
    for e in examples['examples']: by.setdefault(e['word_id'],[]).append(e)
    changed=[]
    for wid, sentence in SECOND.items():
        w=wm[wid]
        if len(w.get('examples') or []) >= 2: continue
        w.setdefault('examples',[]).append(sentence)
        # examples.json mirrors words.examples; use next available stable suffix
        n=len(by.get(wid,[]))+1
        examples['examples'].append({'id':f'ex-{wid}-{n}','word_id':wid,'text':sentence,'source':'审计修复'})
        changed.append(wid)
    # Missing terminal punctuation is a deterministic formatting defect.
    punct=[]
    for w in words['words']:
        for i,s in enumerate(w.get('examples') or []):
            if s and s[-1] not in '.!?。！？':
                w['examples'][i]=s+'.'; punct.append((w['id'],i))
        for e in by.get(w['id'],[]):
            if e.get('text') and e['text'][-1] not in '.!?。！？': e['text']+='.'
    wp.write_text(json.dumps(words,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    ep.write_text(json.dumps(examples,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'补充 {len(changed)} 个第二例句，修正 {len(punct)} 条句末标点')
if __name__=='__main__': main()
