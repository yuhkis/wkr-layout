# わから配列 / Wakara Layout (wkr)

> `w` `k` `r` と打つだけで「わから」と入力できます。配列名がそのまま配列のデモです。
>
> Type `w` `k` `r` to input "わから" — the layout name itself is a demo.

**わから配列**は、[きゅうり改](https://www.itmedia.co.jp/enterprise/articles/0704/24/news006_2.html)をベースに大幅に改良した、ローマ字入力ベースの日本語かな入力配列です。子音キー＋母音キーの2打鍵で1つのかなを入力します。

**Wakara Layout** is a Japanese kana input method based on romaji-style two-stroke key sequences, significantly improved upon [Kyuuri-Kai](https://www.itmedia.co.jp/enterprise/articles/0704/24/news006_2.html). Press a consonant key followed by a vowel key to produce a kana character.

---

## 配列図 / Layout Diagram

```
[が][わ]　[か][ら][□]　[■] や  ゆ  よ  ー　「  」
[ぱ][さ]　[な][た][は]　 あ  う  い  お  え　'  ￥
[ざ][ふぁ][だ][ま][ば]　 ん  っ  ，  ．  ・　｀
```

左手で子音（[行]）を選び、右手で母音（段）を打つ左右交互入力です。

Select a consonant row with the left hand, then type a vowel column with the right hand — alternating left-right input.

---

## 背景 / Background

QWERTYローマ字入力では右手首への負担が大きく、長時間の入力で疲労が蓄積します。わから配列は、この問題を解消するために設計しました。

Standard QWERTY romaji input places disproportionate strain on the right wrist. Wakara Layout was designed to address this problem.

---

## 狙い / Goals

- ローマ字ベースで覚えやすく、打鍵数を極力減らしたい
- できるだけ滑らかに、手首の引っ掛かりがなく入力したい
- ホームポジションから、できるだけ離れずに入力したい

---

- Easy to learn with romaji-based rules, while minimizing keystrokes
- Smooth, fluid typing without wrist strain
- Stay as close to the home position as possible

---

## オリジナリティ / What Makes It Different

ローマ字入力と比べて、**1押下で確定の「かな文字」が増えています**：

| | 1打鍵で確定する文字 |
|:---|:---|
| ローマ字入力 | あ い う え お（5文字） |
| **わから配列** | **あ い う え お や ゆ よ ん っ ー**（11文字）|

さらに、子音キー1打で行の先頭（あ段）も即時確定するため、か さ た な は ま ら わ が ざ だ ば ぱ ふぁ も実質1打鍵です。

---

Compared to standard romaji, **many more characters are produced with a single keystroke**:

In romaji, only **5 characters** (あいうえお) resolve in one keystroke. With Wakara Layout, **11 characters** resolve in one keystroke: あ い う え お や ゆ よ ん っ ー.

Additionally, each consonant key immediately produces the あ-column kana of its row, so か さ た な は ま ら わ が ざ だ ば ぱ ふぁ are also effectively single-keystroke inputs.

---

## 方法 / How It Works

### 左右交互入力を基本とする / Alternating left-right input

右手ホームポジション `H` `J` `K` `L` `;` に「あ う い お え」を割り当て、左手で子音、右手で母音を打ちます。

Vowels are mapped to the right-hand home row (`H`=あ, `J`=う, `K`=い, `L`=お, `;`=え). Left hand selects the consonant, right hand selects the vowel.

### 同じキーの連打を減らす / Reduce same-key repetition

- `N` → 「ん」に独立割り当て（1ストロークで確定）
- `M` → 「っ」に独立割り当て（1ストロークで確定）

### 子音1入力で「あ列」を入力可能にする / Single consonant produces あ-column kana

- `e` → 「か」、`e` `k` → 「き」 のように割り当て
- `e` `s` → 「かさ」、`e` `s` `k` → 「かし」 のように連続入力が可能

### 拗音は左右交互の2ストロークで入力 / Contracted sounds in two strokes

- 「た」+「や」→「ちゃ」、「た」+「ゆ」→「ちゅ」 のように割り当て

### 捨て仮名の単独入力も可能 / Small kana input

- `□` `H` → 「ぁ」、のように □（`T`キー）レイヤーで入力

### 特殊入力 / Special characters

- `E` `Y` → 「ヶ」、`W` `Y` → 「ゎ」 のように ■（`Y`キー）レイヤーで入力
- `■` `J` → 「↓」、`■` `C` → 「〇」 のように記号も入力可能
- その他、余ったキーは自由に割り当てできます

---

## 他の入力方式に対する優位点 / Advantages

### ローマ字入力に対して (thanks to [きゅうり改](https://www.itmedia.co.jp/enterprise/articles/0704/24/news006_2.html))

- 左右交互入力が基本です
- 拗音を2押下で入力可能です
- 「ん」「っ」に独立キーを割り当てています

### かな入力に対して

- ホームポジションからあまり手を動かさずに（3列のみを使用して）「かな文字」を入力できます

### 親指シフトに対して

- シフトキーを使わずに「かな文字」を入力できます

### その他の特徴

- 基本ルールは規則的で、覚える量が少なく、習得のハードルが低いです

---

## キーマップ / Keymap

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
| `F` `O` | ちょ | た行 + 拗お |
| `Q` `K` | ぎ | が行 + い段 |
| `□` `H` | ぁ | 小書きレイヤー (T→H) |
| `E` `Y` | ヶ | か行 + 特殊 (Y) |
| `W` `Y` | ゎ | わ行 + 特殊 (Y) |
| `W` `I` | ゑ | わ行 + ゆ列 |
| `F` `Y` | ちぇ | た行 + 特殊 (Y) |
| `■` `J` | ↓ | 記号レイヤー (Y→J) |
| `■` `C` | 〇 | 記号レイヤー (Y→C) |

---

## ダウンロード / Download

👉 **[最新版をダウンロード / Download Latest Release](https://github.com/yuhkis/wkr-layout/releases/latest)**

---

## インストール / Installation

### Google 日本語入力 / Google Japanese Input

1. [Releaseページ](https://github.com/yuhkis/wkr-layout/releases/latest)から `romantable.txt` をダウンロード / Download `romantable.txt` from the [Release page](https://github.com/yuhkis/wkr-layout/releases/latest)
2. Google 日本語入力の「プロパティ」を開く / Open Google Japanese Input "Properties"
3. 「一般」タブ →「ローマ字テーブル」→「編集」→「インポート」 / "General" tab → "Romaji table" → "Edit" → "Import"
4. ダウンロードした `romantable.txt` を選択 / Select the downloaded `romantable.txt`

### azooKey (macOS)

1. [Releaseページ](https://github.com/yuhkis/wkr-layout/releases/latest)から `custom_input_table.tsv` をダウンロード / Download `custom_input_table.tsv` from the [Release page](https://github.com/yuhkis/wkr-layout/releases/latest)
2. azooKeyの入力方式を「カスタム」に設定 / Set azooKey input method to "Custom"
3. 「編集」→「ファイルに書き出し」で `custom_input_table.tsv` の保存場所を確認 / "Edit" → "Export to file" to locate `custom_input_table.tsv`
4. 書き出された `custom_input_table.tsv` をダウンロードしたファイルで差し替え / Replace the exported file with the downloaded `custom_input_table.tsv`

> **⚠️ azooKeyの注意点：** Google日本語入力では子音キーを押した時点で変換候補が表示されます（例：`w` → 「わ」）が、azooKeyでは途中経過が表示されず `w` のまま表示されます。次の文字（例：`。`）を入力するか、スペースキーで変換すれば正しく「わ」に変換されますが、**文末で何も入力せずにEnterを押すと `w` のまま確定されてしまいます。** 文末ではスペースで変換するか、句読点や次の文字を入力してから確定してください。
>
> **⚠️ Note for azooKey:** Google Japanese Input shows kana conversion immediately when a consonant key is pressed (e.g., `w` → "わ"), but azooKey displays the raw consonant (e.g., `w`) without showing the intermediate kana. Typing the next character (e.g., "。") or pressing Space to convert will correctly resolve it, but **pressing Enter at the end of a sentence without additional input will commit the raw consonant as-is.** Always press Space to convert, or type punctuation or the next character before confirming at the end of a line.

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
