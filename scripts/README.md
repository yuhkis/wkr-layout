# 生成と検査

`python3 scripts/generate.py` は `data/layout-v2.json` と `practice/lessons.json`、`practice/VERSION` から配列表、v2のIMEテーブル、練習の `data.js` を生成します。`--check` は書き換えず一致を検査します。依存はPython標準ライブラリだけです。

規則のキー列・ID重複を拒否し、教材の綴りは最長一致モデルで再変換して対象かなと照合します。規則の出力と綴りに私的な実測値やログを混ぜないでください。

公開配布は `python3 scripts/package.py`。仕様と練習を別zipにし、SHA256を出力します。Gitの履歴をzipへ含めず、含めるパスを固定します。公開前に `docs/verification.md` の未確認事項を見直します。

仕様zipにはv2と区別したv1.1の保全テーブルも同梱し、以前のReleaseへのアクセスを必要としません。
