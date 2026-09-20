# Release文案 — わから配列 2.0.0-beta.1

初めてv2を使う方のための公開ベータです。配列の正本JSON、233規則の配列表、Google日本語入力とazooKeyのv2用テーブルをまとめました。Pの特殊列は評価中のため、今後のベータで変更する場合があります。

同時に用意する「わから v2 練習帳 0.1.0」は、母音から短文へ進む12課題を備え、ブラウザでオフライン利用できます。保存は明示的に有効化した課題別成績だけです。WKR macOS Publicには同じ教材を同梱します。

添付予定: `wakara-layout-2.0.0-beta.1.zip`、`wakara-practice-0.1.0.zip`、`SHA256SUMS`。練習版は独立して管理し、将来の教材更新時に配列版を流用しません。

Google日本語入力・azooKeyの実IME確認とmacOS実機入力確認は未完了です。[検証記録](verification.md)を参照してください。v1.1の利用者は[v2の対応と違い](compatibility.md)を確認し、旧テーブルの控えを取ってから切り替えてください。

公開前: 全ref監査、配布物のハッシュ照合、WKR macOS側の固定commitと版表示、利用者の公開承認を確認します。


公開操作案: 新しいリポジトリにこの候補の独立履歴を公開する。以前のリポジトリのPR・tag・Release・履歴は移さない。tag `v2.0.0-beta.1` のprereleaseに仕様zip・練習zip・`manifest.json`・`SHA256SUMS`を添付する。練習版は `practice/VERSION` で独立管理し、教材単独の次回更新に配列tagを再利用しない。公開先の作成・push・tag・Releaseは利用者の最終承認後に行う。
