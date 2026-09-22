# 公開ベータの検証記録

## 2026-09-21 — 公開準備

配列 **2.0.0-beta.1**、練習 **0.1.0**。配列の正本JSONは233規則です。WKR macOS Publicはこのリポジトリの固定commitを取り込み、配列・アプリ・練習の版を別々に表示します。

| 検証 | 結果 | 範囲 |
| --- | --- | --- |
| `python3 scripts/generate.py --check` | 成功 | 正本、配列表、v2 IMEテーブル、教材が一致 |
| `python3 -m unittest discover -s tests` | 7件成功 | 全233規則、接頭辞、全127問の綴り、テーブル入力の一意性 |
| `node --test practice/core.test.cjs` | 3件成功 | 保存許可項目、未知項目・異版・破損値、上限、課題集計 |
| Chromium、file URL、ネットワークオフライン | 成功 | 全12課題・127問を完走。各課題で合成した誤キーも使用。HTTP(S)リクエスト0件 |
| 保存・再読込・削除 | 成功 | opt-in、課題別完了回数・最高正答率だけの保存、復元、削除後に保存キーが残らないこと |
| IMEイベント境界 | 成功 | 合成したcomposition中のEnterを採点せず、確定後の別Enterで採点。誤入力欄をクリア |
| 幅1150 / 390の画面 | 確認 | 課題・入力欄・保存説明が読める。狭い画面の横幅超過を修正 |
| macOS同梱WKWebView | 確認 | 同じファイルを読み、12課題・短文・版表示・保存オフ・保存/削除を画面で確認 |

「キー位置」は英字キーイベントの練習です。合成compositionイベントの検査は実IMEの互換性確認を置き換えません。

未確認: Google日本語入力・azooKeyでのインポートと実入力、実機のApple日本語入力の変換候補・確定・削除、JIS以外の記号位置、Safari / Firefoxでの全課題完走、支援技術による読み上げ操作。日常用のアプリや入力設定はこのPublic作業では切り替えていません。

仕様zipとオフライン練習zipは `scripts/package.py` でcleanなcommitから生成し、元commitをmanifestへ、各配布物のSHA256を `SHA256SUMS` へ記録します。公開前の履歴監査は [publication-audit.md](publication-audit.md) を参照してください。

## 2026-09-21 — 独立履歴での公開準備

公開用ファイルだけから始まる独立履歴を公開候補とします。正本JSON、v1 / v2のIMEテーブル、教材、練習アプリとテストの内容は、上記検証時のファイルとハッシュで一致を確認しました。v1資料のリンクを同梱テーブルへ修正し、仕様zipにもそのテーブルを含めます。新しい作業場所で生成一致、Python 7件、Node 3件の成功を再確認しました。実IMEの未確認範囲は上記のままです。

## 公開操作の回帰検査

2026-09-21、`python3 scripts/test_publication_guard.py` の15件が成功しました。合成の一時Gitで、削除済み連絡先の過去履歴、他のroot、未許可パス・identity、監査後のcommit/tag/配布物変更、別URL・repository ID、mainへの付け替え、非fast-forwardを拒否します。実際のpre-push hookが未承認のpushを拒否し、試験用の宛先へrefを送らないことも確認しました。検査は内容を読む公開前監査と併用します。

## 2026-09-21 — macOS対応版と実機確認範囲の補足

対応アプリは[WKR macOS v2 Public Beta 0.8.0-public.beta.5](https://github.com/yuhkis/wkr-macos/releases/tag/v0.8.0-public.beta.5)です。配列2.0.0-beta.1と練習帳0.1.0を使います。

Public beta.1で権限付与と短い日本語の実変換、beta.2で同梱練習の課題と配列図表示を利用者が確認しています。macOSでの確認実績がすべて未了という意味ではありません。beta.5は同じ変換処理・教材を引き継いでいますが、この配布版そのものの実機入力・停止復帰は再確認待ちです。[アプリ側の検証記録](https://github.com/yuhkis/wkr-macos/blob/main/docs/verification.md)に版ごとの範囲を記載しています。

Google日本語入力とazooKeyのテーブルは別の入力経路です。Apple日本語入力とWKRの実変換を、これらのテーブルの実IME確認として扱いません。


## 2026-09-22 — 対応アプリの表記

対応アプリは「WKR macOS v2 Public Beta」と表記します。Public Betaは一般公開の試験版を表し、正規タグ `v0.8.0-public.beta.5` と配布済みファイルは維持します。別名タグ `v0.8.0-beta.5` も同じ公開コミットを指し、以前の検証範囲は保持します。


## 2026-09-22 — 別名タグの案内を撤回

前記「対応アプリの表記」にある別名タグの案内を訂正します。`beta.5` と `public.beta.5` は公開段階の意味が異なるため、追加した `v0.8.0-beta.5` を撤回し、正規タグ `v0.8.0-public.beta.5` に統一します。

文書とReleaseの案内を修正する変更です。アプリ・配列・教材の実装や配布済みファイルは変更せず、従来の動作検証範囲と未確認事項を引き継ぎます。
