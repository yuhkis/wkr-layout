#!/usr/bin/env python3
"""Generate v2 reference, input tables and offline practice data from the canonical JSON.
Run python3 scripts/generate.py; --check detects stale generated files without writing.
"""
import argparse, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / 'data/layout-v2.json'
SPEC = json.loads(SPEC_PATH.read_text())
RULES = SPEC['rules']
VERSION = (ROOT / 'practice/VERSION').read_text().strip()

def validate():
    assert SPEC['schemaVersion'] == 1
    assert len({r['id'] for r in RULES}) == len(RULES)
    assert len({tuple(r['keys']) for r in RULES}) == len(RULES)
    assert all(r['output'] and 1 <= len(r['keys']) <= 3 for r in RULES)
    assert all(r['delivery'] in ('unicode', 'romaji') for r in RULES)
    assert all(r.get('romaji') for r in RULES if r['delivery'] == 'romaji')

BY_KEYS = {tuple(r['keys']): r for r in RULES}
PREFIXES = {tuple(r['keys'][:i]) for r in RULES for i in range(1,len(r['keys']))}

def decode(keys):
    """Layout-level maximal-prefix interpretation, including the final boundary."""
    out, pending = '', ()
    for key in keys:
        extended = pending + (key,)
        if extended not in BY_KEYS and extended not in PREFIXES:
            if pending: out += BY_KEYS[pending]['output']
            pending = ()
            extended = (key,)
        pending = extended
        if pending not in PREFIXES:
            out += BY_KEYS[pending]['output']; pending = ()
    if pending: out += BY_KEYS[pending]['output']
    return out

def encode(text, shortcuts=False):
    # Dynamic programming over kana segments. Check the entire result through
    # the same prefix model to prevent a short root swallowing the next vowel.
    candidates = [r for r in RULES if r['delivery']=='romaji' and
                  r['group']!='arrows' and (shortcuts or r['group']!='shortcuts')]
    paths = {len(text): [[]]}
    for pos in range(len(text)-1,-1,-1):
        found=[]
        for rule in candidates:
            if not text.startswith(rule['output'],pos): continue
            for tail in paths.get(pos+len(rule['output']),[]):
                keys=rule['keys']+tail
                try:
                    if decode(keys)==text[pos:]: found.append(keys)
                except KeyError: pass
        paths[pos]=sorted(found,key=lambda k:(len(k),k))[:32]
    if not paths.get(0): raise ValueError('No canonical spelling for lesson target')
    return paths[0][0]

def practice_data():
    lessons=json.loads((ROOT/'practice/lessons.json').read_text())
    assert len({x['id'] for x in lessons})==len(lessons)
    for l in lessons:
        l['exercises']=[
            {'text':t,'keys':encode(t,l['shortcuts'])} for t in l.pop('targets')]
        del l['shortcuts']
    legends=[]
    for row in ['qwertyuiop','asdfghjkl;','zxcvbnm,./']:
        legends.append([{'key':k,'label':BY_KEYS[(k,)]['output'] if (k,) in BY_KEYS else ('記号' if k=='p' else '通過')} for k in row])
    return dict(schemaVersion=1,layoutVersion=SPEC['version'],practiceVersion=VERSION,
                layoutSHA256=hashlib.sha256(SPEC_PATH.read_bytes()).hexdigest(),lessons=lessons,keyboard=legends)

SHIFT=dict(zip(['Shift+'+str(i) for i in range(1,10)],list('!"#$%&\'()')))
SHIFT.update({'Shift+-':'=','Shift+;':'+','Shift+@':'`','Shift+^':'~','Shift+,':'<','Shift+.':'>','Shift+/':'?', 'Shift+[':'{','Shift+]':'}','JIS-_':'_','JIS-Yen':'\\','Shift+JIS-Yen':'|'})
def char(key):return SHIFT.get(key,key)

def tables():
    # Mozc retains the third TSV column as pending input. Reuse each kana
    # prefix as the state marker, following the v1 adapter's convention.
    marker={p:BY_KEYS[p]['output'] if p in BY_KEYS else '■' for p in PREFIXES}
    assert len(set(marker.values()))==len(marker)
    google=[]
    for r in RULES:
        ks=tuple(r['keys'])
        reading=(marker[ks[:-1]] if len(ks)>1 else '')+char(ks[-1])
        if ks in PREFIXES: google.append((reading,'',marker[ks]))
        else: google.append((reading,r['output'],''))
    for p in PREFIXES:
        if p not in BY_KEYS:
            assert len(p)==1
            google.append((char(p[0]),'',marker[p]))
    assert len({x[0] for x in google})==len(google)
    # azooKey consumes literal sequences, with a boundary/fallback for each
    # kana-bearing prefix. Fullwidth punctuation matches its keyboard stream.
    punct={';':'；',',':'、','.':'。','/':'・'}
    def az(k):return punct.get(char(k),char(k))
    azoo=[]
    for r in RULES:
        ks=tuple(r['keys']);reading=''.join(az(k) for k in ks)
        if ks in PREFIXES:
            azoo.extend([(reading+'{composition-separator}',r['output']),
                         (reading+'{any character}',r['output']+'{any character}')])
        else: azoo.append((reading,r['output']))
    return '\n'.join('\t'.join(x).rstrip('\t') for x in google)+'\n','\n'.join('\t'.join(x) for x in azoo)+'\n'

def reference():
    lines=['# わから配列 v2 配列表', '', f"配列版 **{SPEC['version']}**。`data/layout-v2.json` から生成。",'',
           'あ段は行キー単打、または行キー + H。母音を続ける場合は H を明示します。',
           'P を2打鍵目に置く短縮形はベータで評価中です。Q は小書きの行、W J だけが3打鍵へ続きます。', '',
           '| キー | 出力 | 種別 | Apple日本語入力へ送る綴り |','| --- | --- | --- | --- |']
    for r in RULES:
        keys=' '.join(k.upper() if len(k)==1 and k.isalpha() else k for k in r['keys'])
        lines.append(f"| `{keys}` | {r['output']} | {r['group']} | {r.get('romaji','Unicode（確定文字）')} |")
    lines+=['','句読点 `,` `.` と単独の括弧は入力方式の設定に従います。',
            'ヵ・ヶの直接規則はありません。「かげつ」「かしょ」などからかな漢字変換します。',
            'WKR macOS の記号Unicode出力は未確定文字列中では抑止されます。Google / azooKey の記号は各IMEの変換対象です。',
            'Google / azooKey のv2テーブルは生成と構造を検査済みですが、各IMEでの実入力は未確認です。','']
    return '\n'.join(lines)

def outputs():
    validate();google,azoo=tables()
    data=practice_data()
    return {'docs/layout-v2.md':reference(),
            'v2/google-japanese-input/romantable.txt':google,
            'v2/azookey/custom_input_table.tsv':azoo,
            'practice/data.js':'/* Generated by scripts/generate.py. Do not edit. */\nwindow.WKR_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    stale=[]
    for name,value in outputs().items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=value: stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
    if stale: raise SystemExit('Regenerate: '+', '.join(stale))
    print(f"{len(RULES)} rules; practice {VERSION}; generated files {'checked' if args.check else 'written'}")
