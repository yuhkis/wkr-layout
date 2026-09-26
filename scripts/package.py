#!/usr/bin/env python3
"""Build the offline practice zip, and the layout zip for a layout version not yet released.

A released layout version keeps its published zip: it is never rebuilt here.
"""
import hashlib,json,subprocess,zipfile
from publication_guard import audit,inspect_asset,policy_for
from pathlib import Path
root=Path(__file__).resolve().parents[1]
subprocess.run(['python3',str(root/'scripts/generate.py'),'--check'],check=True)
layout=json.loads((root/'data/layout-v2.json').read_text())['version']
practice=(root/'practice/VERSION').read_text().strip()
if subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip():
    raise SystemExit('Commit and review public sources before packaging')
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
out=root/'build/distribution'/revision;out.mkdir(parents=True,exist_ok=True)
groups={f'wakara-practice-{practice}.zip':['LICENSE']+['practice/'+n for n in ['index.html','style.css','data.js','core.js','engine.js','app.js','README.md','VERSION']]}
RELEASED_LAYOUTS={'2.0.0-beta.1','2.0.0-beta.2'}
if layout not in RELEASED_LAYOUTS:
    groups={f'wakara-layout-{layout}.zip':['LICENSE','README.md','docs/layout-v2.md','docs/images/keymap-v2.svg','docs/compatibility.md','docs/verification.md','docs/publication-audit.md','docs/v1.md',f'docs/release-{layout}.md','practice/README.md','scripts/README.md','data/layout-v2.json','google-japanese-input/romantable.txt','azookey/custom_input_table.tsv','v2/google-japanese-input/romantable.txt','v2/azookey/custom_input_table.tsv'],**groups}
distribution_readme=f'''# わから配列 {layout}

正本は data/layout-v2.json、配列表は docs/layout-v2.md です（キー配置の図は docs/images/keymap-v2.svg）。変更点は docs/release-{layout}.md と docs/compatibility.md にあります。
v2/google-japanese-input と v2/azookey は実IME未確認の生成テーブルです。
導入時の差異と検証状況は docs/compatibility.md と docs/verification.md を参照してください。
docs/v1.md は旧版の保全です。google-japanese-input/ と azookey/ の直下にはv1.1テーブルを同梱しています。v2/ 内のテーブルと混在させないでください。

練習は別配布の wakara-practice-{practice}.zip を展開し、practice/index.html を開きます。
macOSアプリは https://github.com/yuhkis/wkr-macos で別管理します。
公開用ソース、生成スクリプトとテストは https://github.com/yuhkis/wkr-layout に置きます。
実IME未確認の点を確認してから導入してください。
'''
audit(root)
checks=[]
for name,files in groups.items():
    with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info=zipfile.ZipInfo(f,(2026,9,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            # The layout zip carries a short distribution README instead of the repository one.
            z.writestr(info,distribution_readme.encode() if f=='README.md' else (root/f).read_bytes())
    inspect_asset(out/name,policy_for(root))
    checks.append(hashlib.sha256((out/name).read_bytes()).hexdigest()+'  '+name)
manifest={'repository':'https://github.com/yuhkis/wkr-layout','revision':revision,'layoutVersion':layout,'practiceVersion':practice,'archives':checks}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
checks.append(hashlib.sha256((out/'manifest.json').read_bytes()).hexdigest()+'  manifest.json')
(out/'SHA256SUMS').write_text('\n'.join(checks)+'\n')
print('\n'.join(checks))
