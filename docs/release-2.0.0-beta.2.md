# Release情報 — わから配列 2.0.0-beta.2 / 練習帳 0.2.1

2.0.0-beta.1で入れ替えていた ん・っ を、v1と同じ **ん＝N、っ＝M** に戻した公開ベータです。ほかの規則は2.0.0-beta.1と同じです（Pの後の `N`＝′・`M`＝″ などの記号選択、`Y`・`/`・Shift+/、I/O、特殊列、3打鍵の規則はそのまま）。Pの特殊列は評価中のため、今後のベータで変更する場合があります。

配列の正本JSON、233規則の配列表、Google日本語入力とazooKeyのv2用テーブルをまとめました。練習帳0.2.1は、教材の打鍵をこの変更に合わせたものです。「v1 からの移行」の課題から ん・っ を外しました。成績の保存先は配列版ごとに分かれるため、2.0.0-beta.1で保存した成績は引き継がれません。[ブラウザデモ](https://yuhkis.github.io/wkr-layout/)も同じ練習帳0.2.1です。

添付: `wakara-layout-2.0.0-beta.2.zip`、`wakara-practice-0.2.1.zip`、`manifest.json`、`SHA256SUMS`。練習帳ZIPは展開して `practice/index.html` を開くと、オフラインで動きます。

**macOSの対応アプリは、まだ2.0.0-beta.2に対応していません。** 公開済みの [WKR macOS v2 Public Beta 0.8.0-public.beta.5](https://github.com/yuhkis/wkr-macos/releases/tag/v0.8.0-public.beta.5) は配列2.0.0-beta.1（ん＝M、っ＝N）と練習帳0.1.0のままです。WKR macOSで使う場合は、2.0.0-beta.2に対応した版の公開を待つか、2.0.0-beta.1の配列で使ってください。

Google日本語入力・azooKeyのv2テーブルのインポートと実入力、実機WKR・Apple日本語入力と練習帳の組み合わせは未確認です。[検証記録](verification.md)を参照してください。v1.1の利用者は[v2の対応と違い](compatibility.md)を確認し、旧テーブルの控えを取ってから切り替えてください。
