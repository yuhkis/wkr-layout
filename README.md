# わから配列 v2 — 公開ベータ

左手で行を、右手で段を選ぶ日本語入力配列です。`W E R` + Enter で「わから」、`E K` で「き」になります。
このリポジトリが配列仕様と練習教材の正本です。**配列 2.0.0-beta.1 / 練習 0.1.0** を公開ベータとして提供します。

[仕様・練習の配布zipとSHA256SUMS](https://github.com/yuhkis/wkr-layout/releases/tag/v2.0.0-beta.1)を公式Releaseから入手できます。

## 初めて使う方へ

1. [練習アプリ](practice/index.html)をダウンロードしたフォルダのままブラウザで開きます。インストール・通信なしでキー位置を練習できます。英字入力にして「キー位置の練習」を選んでください。
2. [配列表](docs/layout-v2.md)で基本キーを確認します。練習は母音・行キーから短文へ進みます。
3. 実際の文章入力には [WKR macOS Public](https://github.com/yuhkis/wkr-macos) とApple日本語入力を使います。[実装の違い](docs/compatibility.md)も確認してください。

練習アプリは既定では成績を保存しません。「成績をこの端末に保存」を有効にした場合だけ課題別の完了回数・最高正答率を保存します。入力本文・誤入力・キー列・時刻は保存しません。[保存と削除](practice/README.md)を参照してください。

## v2 の仕様と版

- [233規則の正本JSON](data/layout-v2.json)と[生成した配列表](docs/layout-v2.md)。短縮形のP列はベータで評価中です。
- [Google日本語入力 v2テーブル](v2/google-japanese-input/romantable.txt)、[azooKey v2テーブル](v2/azookey/custom_input_table.tsv)。各IMEでの実入力は未確認です。
- [v1からの変更・既知の差](docs/compatibility.md)。v1.1資料は[保存版](docs/v1.md)、ルート直下のIMEテーブルはv1.1のままです。仕様zipにも同梱し、以前のReleaseへアクセスせず参照できます。v2と混在させないでください。
- 配列版と練習版は独立しています。WKR macOSは別リポジトリ・別バージョンです。同じ版名の内容は差し替えず、変更時は版を上げます。

## 開発

Python 3（標準ライブラリのみ）で生成・検査できます。

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
python3 -m unittest discover -s tests
node --test practice/core.test.cjs
```

使い方と構成は [scripts/README.md](scripts/README.md)、教材とブラウザ版は [practice/README.md](practice/README.md)へ。
教材を変えたら練習版、規則を変えたら配列版を更新し、WKR macOS側の同期スクリプトで固定commitから取り込みます。
[公開ベータの検証記録](docs/verification.md)と[Release文案](docs/release-2.0.0-beta.1.md)に確認範囲を残します。

MIT License — [LICENSE](LICENSE)。背景と従来版の説明は[v1資料](docs/v1.md)に残しています。

配布候補は `python3 scripts/package.py` でcleanなcommitから `build/distribution/<commit>/` へ作成します。配列・教材の版は変更せず、未公開の文書更新候補はcommitとSHA256で区別します。公開済みの配布物は置き換えません。[検証記録](docs/verification.md)と[公開前監査](docs/publication-audit.md)の未確認・保留事項を先に確認してください。

公開作業を始めるときは `python3 scripts/publication_guard.py install` で、このリポジトリだけのpush前ガードを設置します。接続先のrepository IDと監査済みの内容に対する承認が揃うまではpushを拒否します。[公開前監査](docs/publication-audit.md)に監査と承認記録の手順があります。
