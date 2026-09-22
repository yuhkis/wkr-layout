#!/usr/bin/env python3
"""Build the current offline practice zip; keep published layout assets unchanged."""
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
audit(root)
checks=[]
for name,files in groups.items():
    with zipfile.ZipFile(out/name,'w',zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info=zipfile.ZipInfo(f,(2026,9,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,(root/f).read_bytes())
    inspect_asset(out/name,policy_for(root))
    checks.append(hashlib.sha256((out/name).read_bytes()).hexdigest()+'  '+name)
manifest={'repository':'https://github.com/yuhkis/wkr-layout','revision':revision,'layoutVersion':layout,'practiceVersion':practice,'archives':checks}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
checks.append(hashlib.sha256((out/'manifest.json').read_bytes()).hexdigest()+'  manifest.json')
(out/'SHA256SUMS').write_text('\n'.join(checks)+'\n')
print('\n'.join(checks))
