# 生成と検査

`python3 scripts/generate.py` は `data/layout-v2.json` と `practice/lessons.json`、`practice/VERSION` から配列表、v2のIMEテーブル、練習の `data.js` を生成します。`--check` は書き換えず一致を検査します。依存はPython標準ライブラリだけです。

規則のキー列・ID重複を拒否し、教材の綴りは最長一致モデルで再変換して対象かなと照合します。規則の出力と綴りに私的な実測値やログを混ぜないでください。

公開配布は `python3 scripts/package.py`。仕様と練習を別zipにし、`build/distribution/<commit>/`へSHA256とともに出力します。既存候補は別のcommitの出力先に保持します。Gitの履歴をzipへ含めず、含めるパスを固定します。公開前に `docs/verification.md` の未確認事項を見直します。

仕様zipにはv2と区別したv1.1の保全テーブルも同梱し、以前のReleaseへのアクセスを必要としません。

## v1.1の保存資料を作る

`python3 scripts/package-v1-archive.py` はcleanなcommitから、v1.1の説明・配列表・二つのIMEテーブル・LICENSEだけを固定リストでzipにします。アプリ・練習・Git履歴は収録しません。テーブルのSHA256は旧v1.1.0と照合済みの値に固定し、変更されていたら生成を止めます。

出力先は `build/distribution/v1.1.0-archive.1/<commit>/`。`manifest.json` に配列版・保存資料版・ソースcommit・収録ファイルのSHA256を記録し、zipとmanifestのハッシュを `SHA256SUMS` に書きます。同じcommitの既存ファイルと内容が違えば上書きを拒否し、同じならそのまま使います。

旧v1.1.0のタグや配列内容は変更しません。保存資料の更新時はarchive番号を上げ、公開済みの添付を置き換えません。v2・練習の配布は従来の `package.py` を使います。

## 公開操作のガード

`publication_guard.py` はPython標準ライブラリとGitを使います。GitHubの接続先照合には認証済みの`gh`が必要です。新しい公開作業場だけに `python3 scripts/publication_guard.py install` で設置します。global設定やPrivateの作業場には適用しません。

- `audit --report PATH [--file PATH ...]`: 全refの到達履歴、identity、許可パス、配布zip等を検査し、非公開の監査ファイルへfingerprintを保存します。
- `install --repository-id ID`: 確認した公開先の数値ID、履歴の基点、検査コードと方針をGit管理外へ固定し、pre-push hookを設定します。IDを省略した設置ではpushを止めたままにします。
- `authorize --report PATH --evidence PATH --operation push --ref refs/heads/codex/BRANCH [--file PATH ...]`: 同じ対象を再検査し、別途作成した内容確認・利用者承認の記録が揃った場合だけ24時間の承認記録を作ります。監査対象のファイルをすべて同じ`--file`で指定します。
- `check-upload --operation pr|release --file PATH`: 承認に含めたPR本文・Release本文・配布物が同一かを操作直前に検査します。`authorize`にも該当する`--operation`を追加します。アップロード自体は行いません。
- `python3 scripts/test_publication_guard.py`: 実データを使わず、一時Git履歴とZIPで公開拒否条件を確認します。

履歴・ref・方針・配布物が変わると承認は無効です。方針や検査コードの変更後は、差分レビュー・監査・再設置が必要です。詳細と限界は[公開前監査](../docs/publication-audit.md)を参照してください。
