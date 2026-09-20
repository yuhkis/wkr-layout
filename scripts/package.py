#!/usr/bin/env python3
"""Build source-only layout and offline practice zips; never upload."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
subprocess.run(['python3',str(root/'scripts/generate.py'),'--check'],check=True)
layout=json.loads((root/'data/layout-v2.json').read_text())['version']
practice=(root/'practice/VERSION').read_text().strip()
if subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip():
    raise SystemExit('Commit and review public sources before packaging')
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
out=root/'build';out.mkdir(exist_ok=True)
groups={f'wakara-layout-{layout}.zip':['LICENSE','README.md','docs/layout-v2.md','docs/compatibility.md','docs/verification.md','docs/publication-audit.md','docs/v1.md','docs/release-2.0.0-beta.1.md','practice/README.md','scripts/README.md','data/layout-v2.json','google-japanese-input/romantable.txt','azookey/custom_input_table.tsv','v2/google-japanese-input/romantable.txt','v2/azookey/custom_input_table.tsv'],f'wakara-practice-{practice}.zip':['LICENSE']+['practice/'+n for n in ['index.html','style.css','data.js','core.js','app.js','README.md','VERSION']]}
distribution_readme='''# わから配列 2.0.0-beta.1

正本は data/layout-v2.json、配列表は docs/layout-v2.md です。
v2/google-japanese-input と v2/azookey は実IME未確認の生成テーブルです。
導入時の差異と検証状況は docs/compatibility.md と docs/verification.md を参照してください。
docs/v1.md は旧版の保全です。google-japanese-input/ と azookey/ の直下にはv1.1テーブルを同梱しています。v2/ 内のテーブルと混在させないでください。

練習は別配布の wakara-practice-0.1.0.zip を展開し、practice/index.html を開きます。
macOSアプリは https://github.com/yuhkis/wkr-macos で別管理します。
公開用ソース、生成スクリプトとテストは https://github.com/yuhkis/wkr-layout に置きます。
署名・公証の状態と実IME未確認の点を確認してから導入してください。
'''
checks=[]
for name,files in groups.items():
    with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info=zipfile.ZipInfo(f,(2026,9,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,distribution_readme.encode() if f=='README.md' else (root/f).read_bytes())
    checks.append(hashlib.sha256((out/name).read_bytes()).hexdigest()+'  '+name)
manifest={'repository':'https://github.com/yuhkis/wkr-layout','revision':revision,'layoutVersion':layout,'practiceVersion':practice,'archives':checks}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
checks.append(hashlib.sha256((out/'manifest.json').read_bytes()).hexdigest()+'  manifest.json')
(out/'SHA256SUMS').write_text('\n'.join(checks)+'\n')
print('\n'.join(checks))
