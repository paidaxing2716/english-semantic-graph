#!/usr/bin/env python3
"""把审计发现的模板画面切成可人工重写的批次，不修改词条。"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
T='一张卡片放在桌面中央，旁边摆着几件相关物品，窗光从左侧照来'
W=json.loads((ROOT/'data/words.json').read_text(encoding='utf-8'))['words']
xs=[w['id'] for w in W if w.get('core_image')==T]
for i in range(0,len(xs),30):
 p=ROOT/'audit'/f'template_image_{i//30+1:02}.txt';p.parent.mkdir(exist_ok=True)
 p.write_text('\n'.join(xs[i:i+30])+'\n',encoding='utf-8')
print(f'[OK] {len(xs)} 个模板画面，切成 {(len(xs)+29)//30} 批，每批最多 30')
