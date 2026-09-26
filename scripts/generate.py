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
        # ん has two keys since 2.0.0-beta.3; lessons show U, the one added for it.
        paths[pos]=sorted(found,key=lambda k:(len(k),k.count('n'),k))[:32]
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
        legends.append([{'key':k,'label':BY_KEYS[(k,)]['output'] if (k,) in BY_KEYS else '通過'} for k in row])
    return dict(schemaVersion=1,layoutVersion=SPEC['version'],practiceVersion=VERSION,
                layoutSHA256=hashlib.sha256(SPEC_PATH.read_bytes()).hexdigest(),lessons=lessons,keyboard=legends,
                rules=[dict(keys=r['keys'],output=r['output']) for r in RULES])

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
    # A prefix with no output of its own (Q Q, the symbol layer) is reached
    # from the state of the keys before it, like any other rule.
    for p in PREFIXES:
        if p not in BY_KEYS:
            google.append(((marker[p[:-1]] if len(p)>1 else '')+char(p[-1]),'',marker[p]))
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

# The at-a-glance map: the three letter rows of a JIS keyboard, each key named
# by what it does alone. Read off the rules, so it cannot drift from them.
KEY_ROWS=['qwertyuiop','asdfghjkl;','zxcvbnm,./']
FINGERS=['小指','薬指','中指','人差し指','人差し指','人差し指','人差し指','中指','薬指','小指']
COLUMNS=[('h','あ段'),('k','い段'),('j','う段'),(';','え段'),('l','お段'),('p','ゃ'),('o','ゅ'),('i','ょ')]
def cap(k):return k.upper() if k.isalpha() else k
def row_keys():
    # Keys with a kana of their own that other rules continue from, in keyboard order.
    return [k for k in ''.join(KEY_ROWS) if (k,) in BY_KEYS and (k,) in PREFIXES]
def key_role(k):
    single=BY_KEYS.get((k,))
    if k in row_keys():return single['output']+'行'
    if single:return single['output']
    return {',':'、','.':'。'}.get(k,'')
def keymap_table():
    lines=['| | '+' | '.join(FINGERS)+' |','| --- |'+' --- |'*10]
    for name,row in zip(['上段','中段','下段'],KEY_ROWS):
        lines.append(f'| {name} | '+' | '.join(f'`{cap(k)}` {key_role(k)}' for k in row)+' |')
    return lines
def grid_table():
    lines=['| 行キー | 単打 | '+' | '.join(f'`{cap(c)}` {n}' for c,n in COLUMNS)+' |','| --- | --- |'+' --- |'*len(COLUMNS)]
    # In the order of the kana table, so a reader finds a kana by its row.
    order=['か','さ','た','な','は','ま','ら','わ','が','ざ','だ','ば','ぱ','ふぁ','ゔ','ぁ']
    rows=sorted([(k,) for k in row_keys()]+[('w','j')],key=lambda r:order.index(BY_KEYS[r]['output']))
    for r in rows:
        cells=[BY_KEYS[r+(c,)]['output'] if r+(c,) in BY_KEYS else '' for c,_ in COLUMNS]
        lines.append(f"| `{' '.join(cap(k) for k in r)}` | {BY_KEYS[r]['output']} | "+' | '.join(cells)+' |')
    return lines
def keymap_svg():
    # Plain shapes and text, no external resources. Kinds are coloured apart:
    # rows for the left hand, columns for the right, keys that give one kana alone.
    u,gap,pad=64,6,20;offsets=[0,0.25,0.75]
    fill={'row':'#dbeafe','column':'#fde68a','single':'#e9d5ff','small':'#bbf7d0','pass':'#f3f4f6'}
    columns={c for c,_ in COLUMNS}
    def kind(k):
        if k=='q':return 'small'
        if k in row_keys():return 'row'
        if k in columns:return 'column'
        if (k,) in BY_KEYS:return 'single'
        return 'pass'
    sub={c:n for c,n in COLUMNS};sub.update({'q':'Q Q 記号','u':'','n':'','m':'','y':'','/':'Shift で ・'})
    top=34;width=int(pad*2+u*10.75);height=top+pad*2+u*3+178
    esc=lambda t:t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="Hiragino Sans, Hiragino Kaku Gothic ProN, Noto Sans JP, Yu Gothic, Meiryo, sans-serif">',
         f'<title>わから配列 {esc(SPEC["version"])} のキー配置</title>',
         f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
         f'<text x="{pad}" y="{pad+14}" font-size="18" font-weight="700" fill="#111827">わから配列 {esc(SPEC["version"])}（JISキーボードの文字キー）</text>']
    for r,row in enumerate(KEY_ROWS):
        for i,k in enumerate(row):
            x=pad+(i+offsets[r])*u;y=top+pad+r*u;w=u-gap
            out.append(f'<rect x="{x:.0f}" y="{y}" width="{w}" height="{w}" rx="8" fill="{fill[kind(k)]}" stroke="#6b7280"/>')
            out.append(f'<text x="{x+7:.0f}" y="{y+16}" font-size="13" fill="#374151">{esc(cap(k))}</text>')
            role=key_role(k);size=22 if len(role)<=2 else 16
            out.append(f'<text x="{x+w/2:.0f}" y="{y+40}" font-size="{size}" font-weight="700" text-anchor="middle" fill="#111827">{esc(role)}</text>')
            if sub.get(k):out.append(f'<text x="{x+w/2:.0f}" y="{y+w-6}" font-size="10" text-anchor="middle" fill="#4b5563">{esc(sub[k])}</text>')
    y=top+pad+u*3+22
    legend=[('row','左手の行キー。単打でその行のあ段（E＝か）'),('column','右手の段キー。単打で あいうえお・や ゆ よ、行キーの後で段を選ぶ（E K＝き、E P＝きゃ）'),
            ('single','単打だけのキー（ん・っ・ー・？）。行キーの後でも行のあ段を確定してから続く（E U＝かん）'),('small','小書きの行（Q＝ぁ、Q P＝ゃ、Q W＝ゎ）。Q Q の後で記号・矢印（Q Q L＝→）'),
            ('pass','入力方式の句読点の設定のまま通す（、 。）')]
    for i,(k,text) in enumerate(legend):
        out.append(f'<rect x="{pad}" y="{y+i*28-14}" width="18" height="18" rx="4" fill="{fill[k]}" stroke="#6b7280"/>')
        out.append(f'<text x="{pad+28}" y="{y+i*28}" font-size="14" fill="#111827">{esc(text)}</text>')
    out.append('</svg>')
    return '\n'.join(out)+'\n'

def reference():
    lines=['# わから配列 v2 配列表', '', f"配列版 **{SPEC['version']}**。`data/layout-v2.json` から生成。",'',
           f"![わから配列 {SPEC['version']} のキー配置](images/keymap-v2.svg)",'',
           '## ひと目で','',
           '左手の行キーで行（子音）を、右手の段キーで段（母音）を選びます。行キー単打はあ段で、`W E R` は「わから」、`E K` は「き」です。',
           '各キーが単打で出すものを、JISキーボードの位置で示します。','']+keymap_table()+['',
           '- `U` と `N` はどちらも ん、`M` は っ、`Y` は ー、`/` は ？、Shift+`/` は ・ です。`,` `.` は入力方式の句読点設定のまま通します。',
           '- 行キーの後に段キー（`H` `K` `J` `;` `L` `P` `O` `I`）以外を打つと、行のあ段を確定してからそのキーの文字になります（`E U` かん、`E Y` かー）。',
           '  あ段のかなの直後に段キーのかなを続けるときは `H` を明示します（かい＝`E H K`、かや＝`E H P`）。',
           '- 記号・矢印は `Q` `Q` の後に1打です（`Q Q L` →、`Q Q H` ←、`Q Q A` ※）。全件は下の一覧にあります。','',
           '## 行と段の組み合わせ','',
           '行キー（`W J` は ゔ の行で、3打鍵目で段を選ぶ）の後に段キーを打ちます。表は五十音の順です。','']+grid_table()+['',
           '## 全規則','',
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
            'docs/images/keymap-v2.svg':keymap_svg(),
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
