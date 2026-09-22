#!/usr/bin/env python3
"""Stage only the reviewed static site files; no deployment or automatic upload."""
import argparse, hashlib, io, json, re, subprocess, zipfile
from pathlib import Path
from publication_guard import audit, inspect_asset, policy_for
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--expect-sha256');a=p.parse_args()
if a.expect_sha256 is not None and not re.fullmatch('[0-9a-f]{64}', a.expect_sha256):
    raise SystemExit('An exact lowercase SHA256 is required')
subprocess.run(['python3',str(root/'scripts/generate.py'),'--check'],check=True)
audit(root)
revision=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
names=['index.html','style.css','data.js','core.js','engine.js','app.js','VERSION']
files={n:(root/'practice'/n).read_bytes() for n in names}
files['LICENSE']=(root/'LICENSE').read_bytes();files['.nojekyll']=b''
buffer=io.BytesIO()
with zipfile.ZipFile(buffer,'w',zipfile.ZIP_STORED) as z:
    for name,value in sorted(files.items()):
        info=zipfile.ZipInfo(name,(2026,9,22,0,0,0));info.compress_type=zipfile.ZIP_STORED;info.external_attr=0o100644<<16
        z.writestr(info,value)
blob=buffer.getvalue();digest=hashlib.sha256(blob).hexdigest()
if a.expect_sha256 is not None and a.expect_sha256 != digest:raise SystemExit('Site differs from the approved artifact')
out=root/'build/site'/revision;out.mkdir(parents=True,exist_ok=True)
def put(path,data):
    if path.exists() and path.read_bytes()!=data:raise SystemExit('Refusing to replace a different candidate')
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
put(out/'site.zip',blob);inspect_asset(out/'site.zip',policy_for(root))
site=out/'public'
if site.is_symlink() or site.exists() and any(p.is_symlink() for p in site.rglob('*')):
    raise SystemExit('Symbolic links are not site assets')
if site.exists() and {str(p.relative_to(site)) for p in site.rglob('*') if p.is_file()}-set(files):
    raise SystemExit('Unexpected file in the site output directory')
for name,value in files.items():put(site/name,value)
manifest={'revision':revision,'practiceVersion':(root/'practice/VERSION').read_text().strip(),
          'sha256':digest,'files':{n:hashlib.sha256(v).hexdigest() for n,v in files.items()}}
put(out/'manifest.json',(json.dumps(manifest,indent=2)+'\n').encode())
print(json.dumps({'revision':revision,'sha256':digest,'files':len(files)}))
