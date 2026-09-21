# wkr-layout の作業方針

配列の正本は `data/layout-v2.json`。配列表・IMEアダプター・教材のキー列は `scripts/generate.py` で生成します。v1の原本は保持します。

個人パス、機体名、実ログ、誤入力、キー履歴、研究用計測は追跡しません。練習保存は明示的有効化と課題別の集計だけです。外部通信やトラッカーを追加しません。

配列版と練習版を分け、既存版の内容を差し替えません。生成一致検査・単体検査・ブラウザ操作を行い、実IME未確認を明記します。公開前には全ref・履歴・PR ref・Release・artifact・LFS・Actionsログを監査します。push・PR・Release・公開範囲変更は明示承認後に行います。

## 公開操作の必須経路

公開用の専用Gitでpublication_guardを設置し、全履歴・成果物の監査と内容確認、利用者の操作承認を揃える。監査報告だけで承認済みとしない。pre-pushを無効化・迂回しない。PR本文、Release本文・添付はcheck-uploadを通した正確なファイルだけを送る。方針・ガード・ref・成果物の変更後は再確認する。旧URLを再利用するときは、先に既知の旧checkoutのremoteを保全先へ変更し、新repository IDを固定する。詳細はdocs/publication-audit.md。
