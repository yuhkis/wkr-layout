# わから配列 v1.1.0 — 保存資料

v1系を後から参照できるよう、配列1.1.0の説明・配列表・Google日本語入力とazooKeyのテーブルを保存用の配布物にまとめました。v1.0からv1.1への変更履歴も収録しています。

配列の版は **1.1.0**、保存資料の版とタグは **v1.1.0-archive.1** です。旧版のタグを差し替えず、保存資料として作成したことを区別しています。両IMEテーブルは旧v1.1.0とbyte単位で同一で、SHA256をmanifestに記録しています。

## 入手するファイル

- `wakara-layout-1.1.0-archive.1.zip`: 説明、配列表、v1.1のIMEテーブル、ライセンス。
- `manifest.json`: 保存用配布物のソースcommit、版、各ファイルのSHA256。
- `SHA256SUMS`: zipとmanifestの検査用ハッシュ。

v1.1の資料だけを取得する場合は上記zipを使用してください。GitHubが自動生成する「Source code」は、v2の資料も含むリポジトリ全体です。

## 記録の範囲

[v1資料](v1.md)のかな・記号の役割と、[Google日本語入力用](../google-japanese-input/romantable.txt)・[azooKey用](../azookey/custom_input_table.tsv)のテーブルを保存しています。実際の入力ログや利用者の端末設定は収録しません。

この保存版にはmacOSアプリや練習アプリを含みません。現行の[WKR macOS Public](https://github.com/yuhkis/wkr-macos)と練習帳はv2用です。新しく使う場合は[v2の公開ベータ](https://github.com/yuhkis/wkr-layout/releases/tag/v2.0.0-beta.1)を参照してください。

Google日本語入力・azooKeyでの実IME確認は未了です。資料にあるmacOSの確認は当時の記録であり、この保存版での再検証を意味しません。静的なファイル照合・保存用zipの検査と、実機動作の確認を区別します。

対応するmacOS実装は[WKR macOS 0.7.0 保存ソース](https://github.com/yuhkis/wkr-macos/releases/tag/v0.7.0-archive.1)です。保存版のタグは`v0.7.0-archive.1`で、現在のv2用Publicアプリとは別です。
