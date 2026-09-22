# wkr-layout の作業方針

配列の正本は `data/layout-v2.json`。配列表・IMEアダプター・教材のキー列は `scripts/generate.py` で生成します。v1の原本は保持します。

個人パス、機体名、実ログ、誤入力、キー履歴、研究用計測は追跡しません。練習保存は明示的有効化と課題別の集計だけです。外部通信やトラッカーを追加しません。

配列版と練習版を分け、既存版の内容を差し替えません。生成一致検査・単体検査・ブラウザ操作を行い、実IME未確認を明記します。公開前には全ref・履歴・PR ref・Release・artifact・LFS・Actionsログを監査します。push・PR・Release・公開範囲変更は明示承認後に行います。

## 公開操作の必須経路

公開用の専用Gitでpublication_guardを設置し、全履歴・成果物の監査と内容確認、利用者の操作承認を揃える。監査報告だけで承認済みとしない。pre-pushを無効化・迂回しない。PR本文、Release本文・添付はcheck-uploadを通した正確なファイルだけを送る。方針・ガード・ref・成果物の変更後は再確認する。旧URLを再利用するときは、先に既知の旧checkoutのremoteを保全先へ変更し、新repository IDを固定する。詳細はdocs/publication-audit.md。

## 個人情報を入れない継続設定

公開作業では毎回、専用Gitに `python3 scripts/publication_guard.py install --repository-id ID` で検査を設置します。pre-commitは作業ファイルではなくstage済みの全ファイルと著者情報、commit-msgは本文を検査し、許可外メール・ローカルパス・秘密情報・私的記録を含むcommitを拒否します。既存のpre-pushも維持します。未設置・検査失敗・由来不明は公開停止とし、`--no-verify`やhookの無効化で回避しません。

`check-index` で同じ検査を手動実行できます。`check-assets --file PATH` は生成したZIP・本文を検査しますが、アップロード承認にはなりません。Pagesも `authorize --operation pages` と `check-upload --operation pages --file PATH` の対象です。アプリ・サイトは固定の収録リストから作り、実データ・個人設定・監査原記録をコピーしません。検出語はログへ出しません。自動検査に加えて出所と内容を確認し、未検出を「個人情報ゼロ」の証明とは扱いません。
