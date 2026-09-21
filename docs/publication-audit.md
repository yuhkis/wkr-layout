# 公開前監査 — 2026-09-21

初回公開候補は、確認した公開用ファイルだけを新しいGitリポジトリへコピーした独立履歴です。以前のリポジトリのGitオブジェクト・PR・tag・Release・Actions履歴を接続しません。配列と教材は作り直さず、正本JSONと生成検査で内容を確認します。

## 初回候補の監査範囲

- 全ローカルref、到達するcommit / tag / blob、author / committer、署名を検査する。初回候補は親のない署名付きcommitから始める。
- 全追跡ファイルと配布zipを、秘密情報、私的な連絡先・絶対パス・機体情報、実入力・実ログ・研究用計測の混入について検査する。テスト・教材の合成例と実データを区別する。
- `.git`、作業ログ、監査の原データを配布zipへ含めない。LFS pointerの有無も全blobから確認する。
- 新しい公開先はまずPrivateで作成する。旧リポジトリのrefをpushせず、作成後に全ref・PR ref・Release・artifact・LFS・Actionsログを再確認してから公開する。

正本と配布物の検査記録、commitとSHA256はローカルの引き継ぎへ保存します。自動走査だけを全情報の安全性の保証とせず、公開対象の文書とファイル一覧も確認します。公開直前には全refと外部成果物を再取得し、追加・変更分を含めて監査します。

## 継続的な公開前ゲート

公開URLは従来の `https://github.com/yuhkis/wkr-layout` を使用します。旧repositoryはPrivateの別名で保全し、旧checkoutのremoteを保全先へ変更した後でURLを再利用します。URLの文字列だけで新旧を区別せず、数値repository IDを照合します。旧Git履歴・PR・Releaseを新しい公開先へ移しません。

1. 新しい公開作業場で `python3 scripts/publication_guard.py install` を実行します。Git common directory内へ検査コードと基点を固定し、そのリポジトリのpre-push hookを設置します。接続先IDをまだ指定しなければ公開はできません。
2. 全refを列挙し、監査対象の新repositoryから全branch・tag・PR refを取得します。旧repositoryのrefは別の保全用Gitで確認します。`audit --report PATH --file PATH ...`で全到達履歴と配布物・PR/Release本文を検査します。報告はGit管理外に置きます。
3. 文書・コメント・fixtureの出所・commit/tagのidentityと署名・配布物を読み直します。GitHub上の全ref、PR本文・コメント、Releaseと添付、artifact、LFS、Actionsログも取得して確認します。該当物がなければ件数0を記録します。自動検査が通っただけで内容確認済みとは扱いません。
4. 利用者が対象・内容を承認した後に限り、監査報告の`fingerprint`と下記の各項目を`true`にした非公開JSONを作り、`authorize`へ渡します。`sources_and_comments`、`fixture_provenance`、`identities_and_messages`、`archive_contents`、`github_refs_prs_releases_artifacts_lfs_actions`、`user_authorized_operations`。未確認の項目を自動で埋めません。
5. push直前にhookが全対象を再検査し、指定したref・commit・接続先ID・24時間以内の承認記録と照合します。mainへの直接push、削除、別refへの付け替え、非fast-forward、tagの置換を拒否します。新しいcommit、ref、配布物や方針の変更後は再監査・再承認が必要です。
6. PR/Release本文や添付をAPIで送る直前にも`check-upload`を使います。公開後も毎回この手順を通します。CIは全到達履歴を再検査しますが、push後に走るため、公開前の検査を代替しません。

`.publication-policy.json`は公開を認めるパス、著者identity、独立履歴の基点を明記します。Gitの全履歴から削除済みのファイルも検査し、未許可パス、他の基点、個人メールやホームパス、秘密鍵/token形式、未監査LFS、symlink/submoduleを拒否します。配布zipの全エントリも走査します。エラーには検出した値を転載しません。

この仕組みは誤操作を止めるためのもので、未知の個人情報をすべて自動判定する保証ではありません。Git hookを外す操作、`--no-verify`、ブラウザやAPIへの直接投稿までは強制できません。これらの迂回は使わず、公開用素材だけを専用作業場へ置き、文章の内容確認と併用します。承認記録・元ログ・個人設定を公開Gitへ追加しません。
