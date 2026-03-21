# わから配列 / Wakara Layout (wkr)

> `w` `k` `r` と打つだけで「わから」と入力できます。配列名がそのまま配列のデモです。
>
> Type `w` `k` `r` to input "わから" — the layout name itself is a demo.

**わから配列**は、ローマ字入力ベースの日本語かな入力配列です。子音キー＋母音キーの2打鍵で1つのかなを入力します。

**Wakara Layout** is a Japanese kana input method based on romaji-style two-stroke key sequences. Press a consonant key followed by a vowel key to produce a kana character.

---

## 特徴 / What Makes It Different

通常のローマ字入力では、1打鍵で確定するかな文字は **「あいうえお」の5文字** だけです。

わから配列では、**1打鍵で確定するかな文字が大幅に増えます**：

| | 1打鍵で確定する文字 |
|:---|:---|
| ローマ字入力 | あ い う え お（5文字） |
| **わから配列** | **あ い う え お や ゆ よ ん っ ー**（11文字）|

さらに、子音キー1打で行の先頭（あ段）も即時確定するため、か さ た な は ま ら わ が ざ だ ば ぱ ふぁ も実質1打鍵です。

---

In standard romaji input, only **5 characters** (あいうえお) are produced with a single keystroke.

With Wakara Layout, **11 characters** can be produced with a single keystroke: あ い う え お や ゆ よ ん っ ー.

Additionally, each consonant key immediately produces the あ-column kana of its row, so か さ た な は ま ら わ が ざ だ ば ぱ ふぁ are also effectively single-keystroke inputs.

---

## 設計思想 / Design Philosophy

- **2打鍵で1かな**: 子音ねー（行選択）→ 母音キー（段選択）の組み合わせで入力
- **ホームポジション重視**: 母音キーを右手ホームポジション（`H`=あ, `K`=い, `J`=う, `;`=え, `L`=お）に配置
- **拗音も2打鍵**: `U`=や行, `I`=ゆ行, `O`=よ行で拗音を直接入力
- **頻出操作を最適化**: `N`=ん, `M`=っ, `P`=ー を単打で入力可能
- **特殊文字レイヤー**: `Y`（■）キーで記号レイヤー、`T`（□）キーで小書きかなレイヤーにアクセス

---

- **Two keystrokes per kana**: Consonant key (row) → Vowel key (column)
- **Home-row vowels**: Vowels mapped to the right-hand home row (`H`=a, `K`=i, `J`=u, `;`=e, `L`=o)
- **Contracted sounds in two strokes**: `U`=ya, `I`=yu, `O`=yo for direct yōon input
- **Optimized frequent characters**: `N`=ん, `M`=っ, `P`=ー available as single keystrokes
- **Symbol layers**: `Y` (■) for symbol layer, `T` (□) for small kana layer

---

## キーマッㅗ / Keymap

### 子音キー（行選択） / Consonant Keys (Row Selection)

| キー / Key | 行 / Row |
|:---:|:---|
| `E` | か行 (Ka) |
| `S` | さ行 (Sa) |
| `F` | た行 (Ta) |
| `D` | な行 (Na) |
| `G` | は行 (Ha) |
| `V` | ま行 (Ma) |
| `R` | ら行 (Ra) |
| `W` | わ行 (Wa) |
| `Q` | が行 (Ga) |
| `Z` | ざ行 (Za) |
| `C` | だ行 (Da) |
| `B` | ば行 (Ba) |
| `A` | ぱ行 (Pa) |
| `X` | ふぁ行 (Fa) / 外来語 |

### 母音キー（段選択） / Vowel Keys (Column Selection)

| キー / Key | 段 / Column |
|:---:|:---|
| `H` | あ段 (-a) |
| `K` | い段 (-i) |
| `J` | う段 (-u) |
| `;` | え段 (-e) |
| `L` | お段 (-o) |
| `U` | 拗あ (-ya) |
| `I` | 拗う (-yu) |
| `O` | 拗お (-yo) |

### 単打キー / Single Keys

| キー / Key | 出力 / Output |
|:---:|:---|
| `H` | あ |
| `K` | い |
| `J` | う |
| `;` | え |
| `L` | お |
| `U` | や |
| `I` | ゆ |
| `O` | よ |
| `N` | ん |
| `M` | っ |
| `P` | ー |

### 入力例 / Input Examples

| 入力 / Input | 出力 / Output | 説明 / Description |
|:---:|:---:|:---|
| `E` `H` | か | か行 + あ段 |
| `S` `K` | し | さ行 + い段 |
| `F` `J` | つ | た行 + う段 |
| `D` `;` | ね | な行 + え段 |
| `G` `L` | ほ | は行 + お段 |
| `S` `U` | しゃ | さ行 + 拗あ |
| `F` `O` | ちょ | た行 + 招お |
| `Q` `K` | ぎ | が行 + い段 |
| `□` `H` | ぁ | 小書きレイヤー (T→あ段) |
| `E` `Y` | ヶ | か行 + 特殊 (Y) |
| `W` `Y` | ゎ | わ行 + 特殊 (Y) |
| `W` `I` | ゑ | わ行 + ゆ列 |
| `F` `Y` | ちぇ | た行 + 特殊 (Y) |
| `■` `J` | ↓ | 記号レイヤー (Y→J) |
| `■` `C` | 〇 | 記号レイヤー (Y→C) |

---

## インストール / Installation

### Google 日本語入力 / Google Japanese Input

1. Google 日本語入力の「プロパティ」を開く / Open Google Japanese Input "Properties"
2. 「一般」タブ →「ローマ字テーブル」→「編集」→「インポート」 / "General" tab → "Romaji table" → "Edit" → "Import"
3. `google-japanese-input/romantable.txt` を選択 / Select `google-japanese-input/romantable.txt`

### azooKey (macOS)

1. azooKeyの入力方式を「カスタム」に設定 / Set azooKey input method to "Custom"
2. 「編集」→「ファイルに書き出し」で `custom_input_table.tsv` の保存場所を確認 / "Edit" → "Export to file" to locate `custom_input_table.tsv`
3. 書き出された `custom_input_table.tsv` を本リポジトリの `azookey/custom_input_table.tsv` の内容で差し替え / Replace the exported `custom_input_table.tsv` with `azookey/custom_input_table.tsv` from this repository

---

## ファイル構成 / File Structure

```
wkr-layout/
├── README.md
├── LICENSE
├── google-japanese-input/
│   └── romantable.txt      # Google 日本語入力用ローマ字テーブル
└── azookey/
    └── custom_input_table.tsv  # azooKey用カスタムタブ定義
```

---

## ライセンス / License

MIT License — 詳細は [LICENSE](./LICENSE) を参照 / See [LICENSE](./LICENSE) for details.
