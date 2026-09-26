# わから配列 v2 配列表

配列版 **2.0.0-beta.3**。`data/layout-v2.json` から生成。

![わから配列 2.0.0-beta.3 のキー配置](images/keymap-v2.svg)

## ひと目で

左手の行キーで行（子音）を、右手の段キーで段（母音）を選びます。行キー単打はあ段で、`W E R` は「わから」、`E K` は「き」です。
各キーが単打で出すものを、JISキーボードの位置で示します。

| | 小指 | 薬指 | 中指 | 人差し指 | 人差し指 | 人差し指 | 人差し指 | 中指 | 薬指 | 小指 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 上段 | `Q` ぁ行 | `W` わ行 | `E` か行 | `R` ら行 | `T` ぱ行 | `Y` ー | `U` ん | `I` よ | `O` ゆ | `P` や |
| 中段 | `A` が行 | `S` さ行 | `D` な行 | `F` た行 | `G` は行 | `H` あ | `J` う | `K` い | `L` お | `;` え |
| 下段 | `Z` ざ行 | `X` ふぁ行 | `C` だ行 | `V` ま行 | `B` ば行 | `N` ん | `M` っ | `,` 、 | `.` 。 | `/` ？ |

- `U` と `N` はどちらも ん、`M` は っ、`Y` は ー、`/` は ？、Shift+`/` は ・ です。`,` `.` は入力方式の句読点設定のまま通します。
- 行キーの後に段キー（`H` `K` `J` `;` `L` `P` `O` `I`）以外を打つと、行のあ段を確定してからそのキーの文字になります（`E U` かん、`E Y` かー）。
  あ段のかなの直後に段キーのかなを続けるときは `H` を明示します（かい＝`E H K`、かや＝`E H P`）。
- 記号・矢印は `Q` `Q` の後に1打です（`Q Q L` →、`Q Q H` ←、`Q Q A` ※）。全件は下の一覧にあります。

## 行と段の組み合わせ

行キー（`W J` は ゔ の行で、3打鍵目で段を選ぶ）の後に段キーを打ちます。表は五十音の順です。

| 行キー | 単打 | `H` あ段 | `K` い段 | `J` う段 | `;` え段 | `L` お段 | `P` ゃ | `O` ゅ | `I` ょ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `E` | か | か | き | く | け | こ | きゃ | きゅ | きょ |
| `S` | さ | さ | し | す | せ | そ | しゃ | しゅ | しょ |
| `F` | た | た | ち | つ | て | と | ちゃ | ちゅ | ちょ |
| `D` | な | な | に | ぬ | ね | の | にゃ | にゅ | にょ |
| `G` | は | は | ひ | ふ | へ | ほ | ひゃ | ひゅ | ひょ |
| `V` | ま | ま | み | む | め | も | みゃ | みゅ | みょ |
| `R` | ら | ら | り | る | れ | ろ | りゃ | りゅ | りょ |
| `W` | わ | わ | うぃ | ゔ | うぇ | を | ゐ | ゑ | うぉ |
| `A` | が | が | ぎ | ぐ | げ | ご | ぎゃ | ぎゅ | ぎょ |
| `Z` | ざ | ざ | じ | ず | ぜ | ぞ | じゃ | じゅ | じょ |
| `C` | だ | だ | ぢ | づ | で | ど | でぃ | でゅ | どぅ |
| `B` | ば | ば | び | ぶ | べ | ぼ | びゃ | びゅ | びょ |
| `T` | ぱ | ぱ | ぴ | ぷ | ぺ | ぽ | ぴゃ | ぴゅ | ぴょ |
| `X` | ふぁ | ふぁ | ふぃ | ふゅ | ふぇ | ふぉ | てぃ | てゅ | とぅ |
| `W J` | ゔ | ゔぁ | ゔぃ | ゔ | ゔぇ | ゔぉ | ゔゃ | ゔゅ | ゔょ |
| `Q` | ぁ | ぁ | ぃ | ぅ | ぇ | ぉ | ゃ | ゅ | ょ |

## 全規則

| キー | 出力 | 種別 | Apple日本語入力へ送る綴り |
| --- | --- | --- | --- |
| `E` | か | kana | ka |
| `E H` | か | kana | ka |
| `E K` | き | kana | ki |
| `E J` | く | kana | ku |
| `E ;` | け | kana | ke |
| `E L` | こ | kana | ko |
| `E P` | きゃ | kana | kya |
| `E O` | きゅ | kana | kyu |
| `E I` | きょ | kana | kyo |
| `S` | さ | kana | sa |
| `S H` | さ | kana | sa |
| `S K` | し | kana | shi |
| `S J` | す | kana | su |
| `S ;` | せ | kana | se |
| `S L` | そ | kana | so |
| `S P` | しゃ | kana | sha |
| `S O` | しゅ | kana | shu |
| `S I` | しょ | kana | sho |
| `F` | た | kana | ta |
| `F H` | た | kana | ta |
| `F K` | ち | kana | ti |
| `F J` | つ | kana | tu |
| `F ;` | て | kana | te |
| `F L` | と | kana | to |
| `F P` | ちゃ | kana | tya |
| `F O` | ちゅ | kana | tyu |
| `F I` | ちょ | kana | tyo |
| `D` | な | kana | na |
| `D H` | な | kana | na |
| `D K` | に | kana | ni |
| `D J` | ぬ | kana | nu |
| `D ;` | ね | kana | ne |
| `D L` | の | kana | no |
| `D P` | にゃ | kana | nya |
| `D O` | にゅ | kana | nyu |
| `D I` | にょ | kana | nyo |
| `G` | は | kana | ha |
| `G H` | は | kana | ha |
| `G K` | ひ | kana | hi |
| `G J` | ふ | kana | hu |
| `G ;` | へ | kana | he |
| `G L` | ほ | kana | ho |
| `G P` | ひゃ | kana | hya |
| `G O` | ひゅ | kana | hyu |
| `G I` | ひょ | kana | hyo |
| `V` | ま | kana | ma |
| `V H` | ま | kana | ma |
| `V K` | み | kana | mi |
| `V J` | む | kana | mu |
| `V ;` | め | kana | me |
| `V L` | も | kana | mo |
| `V P` | みゃ | kana | mya |
| `V O` | みゅ | kana | myu |
| `V I` | みょ | kana | myo |
| `R` | ら | kana | ra |
| `R H` | ら | kana | ra |
| `R K` | り | kana | ri |
| `R J` | る | kana | ru |
| `R ;` | れ | kana | re |
| `R L` | ろ | kana | ro |
| `R P` | りゃ | kana | rya |
| `R O` | りゅ | kana | ryu |
| `R I` | りょ | kana | ryo |
| `W` | わ | kana | wa |
| `W H` | わ | kana | wa |
| `W K` | うぃ | kana | wi |
| `W J` | ゔ | kana | vu |
| `W ;` | うぇ | kana | we |
| `W L` | を | kana | wo |
| `W P` | ゐ | kana | wyi |
| `W O` | ゑ | kana | wye |
| `W I` | うぉ | kana | who |
| `A` | が | kana | ga |
| `A H` | が | kana | ga |
| `A K` | ぎ | kana | gi |
| `A J` | ぐ | kana | gu |
| `A ;` | げ | kana | ge |
| `A L` | ご | kana | go |
| `A P` | ぎゃ | kana | gya |
| `A O` | ぎゅ | kana | gyu |
| `A I` | ぎょ | kana | gyo |
| `Z` | ざ | kana | za |
| `Z H` | ざ | kana | za |
| `Z K` | じ | kana | zi |
| `Z J` | ず | kana | zu |
| `Z ;` | ぜ | kana | ze |
| `Z L` | ぞ | kana | zo |
| `Z P` | じゃ | kana | zya |
| `Z O` | じゅ | kana | zyu |
| `Z I` | じょ | kana | zyo |
| `C` | だ | kana | da |
| `C H` | だ | kana | da |
| `C K` | ぢ | kana | di |
| `C J` | づ | kana | du |
| `C ;` | で | kana | de |
| `C L` | ど | kana | do |
| `C P` | でぃ | kana | deli |
| `C O` | でゅ | kana | delyu |
| `C I` | どぅ | kana | dolu |
| `B` | ば | kana | ba |
| `B H` | ば | kana | ba |
| `B K` | び | kana | bi |
| `B J` | ぶ | kana | bu |
| `B ;` | べ | kana | be |
| `B L` | ぼ | kana | bo |
| `B P` | びゃ | kana | bya |
| `B O` | びゅ | kana | byu |
| `B I` | びょ | kana | byo |
| `T` | ぱ | kana | pa |
| `T H` | ぱ | kana | pa |
| `T K` | ぴ | kana | pi |
| `T J` | ぷ | kana | pu |
| `T ;` | ぺ | kana | pe |
| `T L` | ぽ | kana | po |
| `T P` | ぴゃ | kana | pya |
| `T O` | ぴゅ | kana | pyu |
| `T I` | ぴょ | kana | pyo |
| `X` | ふぁ | kana | fa |
| `X H` | ふぁ | kana | fa |
| `X K` | ふぃ | kana | fi |
| `X J` | ふゅ | kana | fyu |
| `X ;` | ふぇ | kana | fe |
| `X L` | ふぉ | kana | fo |
| `X P` | てぃ | kana | teli |
| `X O` | てゅ | kana | telyu |
| `X I` | とぅ | kana | tolu |
| `H` | あ | kana | a |
| `K` | い | kana | i |
| `J` | う | kana | u |
| `;` | え | kana | e |
| `L` | お | kana | o |
| `P` | や | kana | ya |
| `O` | ゆ | kana | yu |
| `I` | よ | kana | yo |
| `N` | ん | kana | nn |
| `U` | ん | kana | nn |
| `M` | っ | kana | ltu |
| `Y` | ー | kana | - |
| `/` | ？ | kana | ? |
| `Shift+/` | ・ | kana | / |
| `Q H` | ぁ | kana | la |
| `Q K` | ぃ | kana | li |
| `Q J` | ぅ | kana | lu |
| `Q ;` | ぇ | kana | le |
| `Q L` | ぉ | kana | lo |
| `Q P` | ゃ | kana | lya |
| `Q O` | ゅ | kana | lyu |
| `Q I` | ょ | kana | lyo |
| `Q` | ぁ | kana | la |
| `Q W` | ゎ | kana | lwa |
| `Q ,` | ， | kana | Unicode（確定文字） |
| `Q .` | ． | kana | Unicode（確定文字） |
| `Q /` | ／ | kana | Unicode（確定文字） |
| `W J H` | ゔぁ | kana | va |
| `W J K` | ゔぃ | kana | vi |
| `W J J` | ゔ | kana | vu |
| `W J ;` | ゔぇ | kana | ve |
| `W J L` | ゔぉ | kana | vo |
| `W J P` | ゔゃ | kana | vya |
| `W J O` | ゔゅ | kana | vyu |
| `W J I` | ゔょ | kana | vyo |
| `Q Q H` | ← | arrows | zh |
| `Q Q J` | ↓ | arrows | zj |
| `Q Q K` | ↑ | arrows | zk |
| `Q Q L` | → | arrows | zl |
| `Q Q 1` | ○ | symbols | Unicode（確定文字） |
| `Q Q Shift+1` | ● | symbols | Unicode（確定文字） |
| `Q Q 2` | ▽ | symbols | Unicode（確定文字） |
| `Q Q Shift+2` | ▼ | symbols | Unicode（確定文字） |
| `Q Q 3` | △ | symbols | Unicode（確定文字） |
| `Q Q Shift+3` | ▲ | symbols | Unicode（確定文字） |
| `Q Q 4` | □ | symbols | Unicode（確定文字） |
| `Q Q Shift+4` | ■ | symbols | Unicode（確定文字） |
| `Q Q 5` | ◇ | symbols | Unicode（確定文字） |
| `Q Q Shift+5` | ◆ | symbols | Unicode（確定文字） |
| `Q Q 6` | ☆ | symbols | Unicode（確定文字） |
| `Q Q Shift+6` | ★ | symbols | Unicode（確定文字） |
| `Q Q 7` | ◎ | symbols | Unicode（確定文字） |
| `Q Q Shift+7` | ￡ | symbols | Unicode（確定文字） |
| `Q Q 8` | ￠ | symbols | Unicode（確定文字） |
| `Q Q Shift+8` | 【 | symbols | Unicode（確定文字） |
| `Q Q 9` | ♂ | symbols | Unicode（確定文字） |
| `Q Q Shift+9` | 】 | symbols | Unicode（確定文字） |
| `Q Q 0` | ♀ | symbols | Unicode（確定文字） |
| `Q Q JIS-_` | ∴ | symbols | Unicode（確定文字） |
| `Q Q Shift+-` | ≒ | symbols | Unicode（確定文字） |
| `Q Q Shift+;` | ± | symbols | Unicode（確定文字） |
| `Q Q JIS-Yen` | ＼ | symbols | Unicode（確定文字） |
| `Q Q Shift+JIS-Yen` | ∥ | symbols | Unicode（確定文字） |
| `Q Q Shift+@` | ´ | symbols | Unicode（確定文字） |
| `Q Q Shift+^` | ¨ | symbols | Unicode（確定文字） |
| `Q Q Q` | ゛ | symbols | Unicode（確定文字） |
| `Q Q P` | ～ | symbols | Unicode（確定文字） |
| `Q Q :` | ゜ | symbols | Unicode（確定文字） |
| `Q Q N` | ′ | symbols | Unicode（確定文字） |
| `Q Q M` | ″ | symbols | Unicode（確定文字） |
| `Q Q ;` | ； | symbols | Unicode（確定文字） |
| `Q Q ,` | ， | symbols | Unicode（確定文字） |
| `Q Q Shift+,` | ≦ | symbols | Unicode（確定文字） |
| `Q Q .` | ． | symbols | Unicode（確定文字） |
| `Q Q Shift+.` | ≧ | symbols | Unicode（確定文字） |
| `Q Q /` | ／ | symbols | Unicode（確定文字） |
| `Q Q E` | 々 | symbols | Unicode（確定文字） |
| `Q Q T` | 〆 | symbols | Unicode（確定文字） |
| `Q Q S` | ヽ | symbols | Unicode（確定文字） |
| `Q Q D` | ゝ | symbols | Unicode（確定文字） |
| `Q Q F` | 〃 | symbols | Unicode（確定文字） |
| `Q Q G` | ‐ | symbols | Unicode（確定文字） |
| `Q Q C` | 〇 | symbols | Unicode（確定文字） |
| `Q Q X` | × | symbols | Unicode（確定文字） |
| `Q Q A` | ※ | symbols | Unicode（確定文字） |
| `Q Q B` | ° | symbols | Unicode（確定文字） |
| `Q Q W` | w | symbols | Unicode（確定文字） |
| `Q Q Y` | 〒 | symbols | Unicode（確定文字） |
| `Q Q [` | ［ | symbols | Unicode（確定文字） |
| `Q Q ]` | ］ | symbols | Unicode（確定文字） |
| `Q Q Shift+[` | 《 | symbols | Unicode（確定文字） |
| `Q Q Shift+]` | 》 | symbols | Unicode（確定文字） |
| `Q Q I` | 【 | symbols | Unicode（確定文字） |
| `Q Q O` | 】 | symbols | Unicode（確定文字） |

句読点 `,` `.` と単独の括弧は入力方式の設定に従います。
ヵ・ヶの直接規則はありません。「かげつ」「かしょ」などからかな漢字変換します。
WKR macOS の記号Unicode出力は未確定文字列中では抑止されます。Google / azooKey の記号は各IMEの変換対象です。
Google / azooKey のv2テーブルは生成と構造を検査済みですが、各IMEでの実入力は未確認です。
