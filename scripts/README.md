# 生成と検査

`python3 scripts/generate.py` は `data/layout-v2.json` と `practice/lessons.json`、`practice/VERSION` から配列表、v2のIMEテーブル、練習の `data.js` を生成します。`--check` は書き換えず一致を検査します。依存はPython標準ライブラリだけです。

規則のキー列・ID重複を拒否し、教材の綴りは最長一致モデルで再変換して対象かなと照合します。規則の出力と綴りに私的な実測値やログを混ぜないでください。

公開配布は `python3 scripts/package.py`。練習帳のzipと、まだReleaseしていない配列版の仕様zip（配列JSON・配列表・IMEテーブル・文書・その版の `docs/release-<配列版>.md`）を、`build/distribution/<commit>/`へ `manifest.json`・`SHA256SUMS` とともに出力します。既存候補は別のcommitの出力先に保持します。Gitの履歴をzipへ含めず、含めるパスを固定します。公開前に `docs/verification.md` の未確認事項を見直します。

Release済みの配列版（`package.py` の `RELEASED_LAYOUTS`。現在は2.0.0-beta.1〜2.0.0-beta.3）の仕様ZIPは再生成しません。配列版をReleaseしたら、次の変更でその版を `RELEASED_LAYOUTS` に加えます。v1.1の保全テーブルは専用の保存資料ZIPで配布します。

## v1.1の保存資料を作る

`python3 scripts/package-v1-archive.py` はcleanなcommitから、v1.1の説明・配列表・二つのIMEテーブル・LICENSEだけを固定リストでzipにします。アプリ・練習・Git履歴は収録しません。テーブルのSHA256は旧v1.1.0と照合済みの値に固定し、変更されていたら生成を止めます。

出力先は `build/distribution/v1.1.0-archive.1/<commit>/`。`manifest.json` に配列版・保存資料版・ソースcommit・収録ファイルのSHA256を記録し、zipとmanifestのハッシュを `SHA256SUMS` に書きます。同じcommitの既存ファイルと内容が違えば上書きを拒否し、同じならそのまま使います。

旧v1.1.0のタグや配列内容は変更しません。保存資料の更新時はarchive番号を上げ、公開済みの添付を置き換えません。練習帳の配布は `package.py` を使います。配列内容を変更する場合は別の版を決めてから配布処理を更新します。

## 公開操作のガード

`publication_guard.py` はPython標準ライブラリとGitを使います。GitHubの接続先照合には認証済みの`gh`が必要です。新しい公開作業場だけに `python3 scripts/publication_guard.py install` で設置します。global設定やPrivateの作業場には適用しません。

- `audit --report PATH [--file PATH ...]`: 全refの到達履歴、identity、許可パス、配布zip等を検査し、非公開の監査ファイルへfingerprintを保存します。
- `install --repository-id ID`: 確認した公開先の数値ID、履歴の基点、検査コードと方針をGit管理外へ固定し、pre-push hookを設定します。IDを省略した設置ではpushを止めたままにします。
- `authorize --report PATH --evidence PATH --operation push --ref refs/heads/codex/BRANCH [--file PATH ...]`: 同じ対象を再検査し、別途作成した内容確認・利用者承認の記録が揃った場合だけ24時間の承認記録を作ります。監査対象のファイルをすべて同じ`--file`で指定します。
- `check-upload --operation pr|release|pages --file PATH`: 承認に含めたPR本文・Release本文・配布物が同一かを操作直前に検査します。`authorize`にも該当する`--operation`を追加します。アップロード自体は行いません。
- `python3 scripts/test_publication_guard.py`: 実データを使わず、一時Git履歴とZIPで公開拒否条件を確認します。

履歴・ref・方針・配布物が変わると承認は無効です。方針や検査コードの変更後は、差分レビュー・監査・再設置が必要です。詳細と限界は[公開前監査](../docs/publication-audit.md)を参照してください。

## 個人情報を入れない継続設定

公開作業では毎回、専用Gitに `python3 scripts/publication_guard.py install --repository-id ID` で検査を設置します。pre-commitは作業ファイルではなくstage済みの全ファイルと著者情報、commit-msgは本文を検査し、許可外メール・ローカルパス・秘密情報・私的記録を含むcommitを拒否します。既存のpre-pushも維持します。未設置・検査失敗・由来不明は公開停止とし、`--no-verify`やhookの無効化で回避しません。

`check-index` で同じ検査を手動実行できます。`check-assets --file PATH` は生成したZIP・本文を検査しますが、アップロード承認にはなりません。Pagesも `authorize --operation pages` と `check-upload --operation pages --file PATH` の対象です。アプリ・サイトは固定の収録リストから作り、実データ・個人設定・監査原記録をコピーしません。検出語はログへ出しません。自動検査に加えて出所と内容を確認し、未検出を「個人情報ゼロ」の証明とは扱いません。

## 練習帳0.2.0とWebデモの配布

QWERTY体験とWKR・IME入力を選べる練習帳を用意します。教材はv2対象です。`python3 scripts/package.py` はRelease済みの配列版の仕様ZIPを作り直しません。`python3 scripts/package-site.py` はcleanなcommitを監査し、固定の9ファイルだけをbuild/site/<commit>/publicとsite.zipに出力します。`--expect-sha256 HASH` は事前に確認したサイトZIPとの一致を必須にします。

Pagesのworkflowはmainからの手動実行だけです。公開承認後にGitHub PagesをGitHub Actions方式に設定し、正確なrefと監査済みsite.zipのSHA256を指定します。pushやPRだけでサイトを公開しません。公開先は https://yuhkis.github.io/wkr-layout/ です。公開対象に作業場や私的記録を含めません。導入方法と保存の詳細はpractice/README.mdを参照してください。

`site.zip` はファイル順・時刻・権限を固定した非圧縮ZIPです。ビルド環境の圧縮ライブラリ差で承認済みSHA256が変わるのを防ぎます。配信する9ファイルにGit履歴・README・テスト・学習データ・監査記録は含めません。
