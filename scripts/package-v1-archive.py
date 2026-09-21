#!/usr/bin/env python3
"""Package the unchanged v1.1 tables as historical reference; never upload."""
import hashlib
import io
import json
import subprocess
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
archive_version = '1.1.0-archive.1'
table_hashes = {
    'google-japanese-input/romantable.txt': '6053ce3ec46fa39b46f4cee12f48fe38d452bfad2ead6a36d671a2afbd2b1fc5',
    'azookey/custom_input_table.tsv': 'aeb3cb13699435d192298981e714a5f8b83dca52bc76f6e5400fa1c0c22f7442',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

if subprocess.check_output(['git', 'status', '--porcelain'], cwd=root).strip():
    raise SystemExit('Commit and review sources before packaging')
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
for name, expected in table_hashes.items():
    if sha((root / name).read_bytes()) != expected:
        raise SystemExit('Historical v1.1 table changed; refusing to package it under the same version')

readme = '''# わから配列 v1.1.0 — 保存資料

配列の版は1.1.0、保存資料の版は1.1.0-archive.1です。
説明・配列表・変更履歴は [docs/v1.md](docs/v1.md) を参照してください。
Google日本語入力用は google-japanese-input/romantable.txt、
azooKey用は azookey/custom_input_table.tsv です。旧v1.1.0と同一のテーブルです。
収録範囲・確認状況は [Release情報](docs/release-1.1.0-archive.1.md) に記載しています。

このzipにアプリ・練習は含みません。現在のWKR macOS Publicはv2用です。
v2の導入は https://github.com/yuhkis/wkr-layout を参照してください。
'''
files = {name: (root / name).read_bytes() for name in
         ['LICENSE', 'docs/v1.md', 'docs/release-1.1.0-archive.1.md', *table_hashes]}
files['README.md'] = readme.encode()
buffer = io.BytesIO()
with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name, data in sorted(files.items()):
        entry = zipfile.ZipInfo(name, (2026, 9, 21, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = 0o100644 << 16
        archive.writestr(entry, data)
filename = 'wakara-layout-' + archive_version + '.zip'
payload = {filename: buffer.getvalue()}
manifest = {'repository': 'https://github.com/yuhkis/wkr-layout', 'revision': revision,
            'layoutVersion': '1.1.0', 'archiveVersion': archive_version,
            'archive': filename, 'sha256': sha(payload[filename]),
            'files': {name: sha(data) for name, data in sorted(files.items())},
            'unchangedV11Tables': table_hashes}
payload['manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
checks = '\n'.join(sha(data) + '  ' + name for name, data in payload.items()) + '\n'
payload['SHA256SUMS'] = checks.encode()
out = root / 'build/distribution' / ('v' + archive_version) / revision
for name, data in payload.items():
    path = out / name
    if path.exists() and path.read_bytes() != data:
        raise SystemExit('Existing archive differs; refusing to overwrite it')
out.mkdir(parents=True, exist_ok=True)
for name, data in payload.items():
    path = out / name
    if not path.exists():
        path.write_bytes(data)
print(checks, end='')
