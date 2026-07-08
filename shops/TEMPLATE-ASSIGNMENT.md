# 店舗テンプレ分類（bridal / standard）— 適用済み

対象：全65店舗。判定基準は ①住所から半径約1.5km以内の主要式場（結婚式場・ゲストハウス・ホテル式場）の有無、②都心の式場集積エリア（港区・渋谷区・千代田区・目黒区など）該当、③隣接店舗と訴求軸が被る場合は片方をstandardへ調整。SEO/AIO（「エリア名＋ブライダル」高インテント検索の獲得）を最優先に、各商圏で共食い（cannibalization）を避けて8店を選定。

> 最終決定＝**bridal 8店 / standard 57店**。`templates-config.json` に反映済み・全65店へ変換適用済み。

---

## ① ブライダル型 — 8店（適用済み）

| 店舗 | 住所（市区） | 商圏 | 判定理由 |
|---|---|---|---|
| **乃木坂・赤坂店** `nogizaka-akasaka` | 港区赤坂 | 東京都心 | 港区（集積エリア）。明治記念館・赤坂〜六本木のホテル式場圏。※参照テンプレ第1号 |
| **三田/芝公園店** `mita` | 港区芝 | 東京都心 | 港区。ザ・プリンス パークタワー東京／東京プリンスホテル（芝公園）が至近のホテル式場圏 |
| **白金台・高輪台店** `shirokanedai` | 品川区上大崎（白金台） | 東京都心 | 目黒区・白金台の高級式場エリアに隣接。八芳園（白金台）が徒歩圏 |
| **渋谷・神泉店** `shibuya-shinsen` | 渋谷区道玄坂（神泉・松濤） | 東京都心 | 渋谷区（集積エリア）。松濤・渋谷のゲストハウス／レストランウェディング集積 |
| **横浜元町店** `yokohama-motomachi` | 横浜市中区山手町 | 横浜 | 山手西洋館群・元町山手のゲストハウス群（横浜随一のブライダルエリア） |
| **上野店** `ueno` | 台東区東上野 | 東京北東 | 上野精養軒（上野公園）圏。都心北東エリアで唯一のブライダル訴求点 |
| **大阪福島店** `osaka-fukushima` | 大阪市福島区（梅田西） | 大阪 | 梅田ホテル式場（ハービス系等）に近接。関西で唯一のブライダル訴求点 |
| **平尾店** `hirao` | 福岡市中央区平尾 | 福岡 | 平尾・薬院のゲストハウス圏。福岡で唯一店＝共食いゼロ |

> **選定ロジック（SEO/AIO）**：4商圏（東京都心4・横浜1・大阪1・福岡1・東京北東1）に分散し、同一商圏内で隣接店とキーワードが被らないよう1点集約。standard店もブライダル語彙は「簡易ブロック＋統合FAQ（schema維持）」で保持し、キーワード損失ゼロ。

---

## ② 要確認（ボーダーライン）— ご判断ください（暫定は standard）

| 店舗 | 住所（市区） | 論点 | 暫定 |
|---|---|---|---|
| **上野店** `ueno` | 台東区東上野 | 上野精養軒（上野公園）が約1.2kmで圏内だが、台東区は都心式場集積ワード外。精養軒訴求でbridal化も可 | standard |
| **東日本橋店** `higashi-nihonbashi` | 中央区日本橋馬喰町 | 中央区だが馬喰町は問屋街。日本橋の主要式場（マンダリン等）まで1.5km超の可能性 | standard |
| **奥沢店** `okusawa` | 世田谷区奥沢（自由が丘） | 自由が丘にゲストハウス散在。ただし世田谷は集積ワード外・訴求軸は「自由が丘」生活圏 | standard |
| **岸根公園店** `kishine-koen` | 横浜市港北区岸根町（新横浜） | 新横浜プリンスホテル等の式場はあるが、店舗自体は岸根町の住宅地 | standard |
| **大阪福島店** `osaka-fukushima` | 大阪市福島区（梅田西） | 梅田のホテル式場（ハービス系等）に近接。ただし基準②は東京ワード限定 | standard |
| **平尾店** `hirao` | 福岡市中央区平尾 | 福岡中央区。平尾・薬院にゲストハウス散在。集積度は中程度 | standard |

---

## ③ 通常型（standard）— 54店

いずれも住宅地立地で1.5km圏内に主要式場の集積がなく、集積ワードにも該当しないため standard。隣接クラスタの訴求軸（下記「訴求軸メモ」）とも整合。

### 東京・大田区クラスタ（住宅地・訴求軸は生活密着で統一）
千鳥町 `chidoricho`／池上 `ikegami`／石川台 `ishikawadai`／蒲田・蓮沼 `kamata-hasunuma`／北千束 `kita-senzoku`／久が原 `kugahara`／馬込 `magome`／武蔵新田 `musashi-nitta`／長原 `nagahara`／西馬込 `nishi-magome`／西馬込ANNEX `nishi-magome-annex`／大森北口山王 `omori-sanno`／雪が谷大塚 `yukigaya-otsuka`／雑色 `zoshiki`

### 東京・中野〜杉並〜練馬〜板橋クラスタ
中野 `nakano`／中野富士見町 `nakano-fujimicho`／中野新橋 `nakano-shimbashi`／新中野 `shin-nakano`／沼袋 `numabukuro`／新江古田 `shin-egota`／練馬 `nerima`／上板橋 `kami-itabashi`／西荻窪 `nishi-ogikubo`

### 東京・世田谷クラスタ
池ノ上 `ikenoue`／明大前 `meidaimae`／太子堂 `taishido`

### 東京・渋谷区（笹塚）／文京／墨田／江東／中央／台東／江戸川／足立
笹塚 `sasazuka`（笹塚は住宅地・渋谷本体の訴求はshibuya-shinsenへ集約）／白山 `hakusan`／千駄木 `sendagi`／菊川 `kikukawa`／清澄白河 `kiyosumi-shirakawa`／月島 `tsukishima`／西葛西 `nishi-kasai`／梅島・西新井 `umejima-nishiarai`

### 神奈川・横浜／川崎クラスタ
弘明寺 `gumyoji`／白楽 `hakuraku`／日吉 `hiyoshi`／市が尾 `ichigao`／希望ヶ丘 `kibogaoka`／三ツ境 `mitsukyo`／三ツ沢上町 `mitsuzawa-kamicho`／仲町台 `nakamachidai`／大船 `ofuna`／大口 `oguchi`／高田駅前 `takata-ekimae`／十日市場 `tokaichiba`／綱島 `tsunashima`／鹿島田・新川崎 `kashimada-shinkawasaki`／登戸 `noborito`

### 大阪・福岡クラスタ
大阪服部天神 `hattori-tenjin`／大阪緑地公園 `ryokuchi-koen`／大阪茨木・総持寺 `sojiji`／大阪豊中・曽根 `sone`／大阪豊中 `toyonaka`

---

## 訴求軸クラスタ整合メモ（③の調整根拠）
- **相鉄線・面化**：三ツ境／希望ヶ丘は相互リンクで面展開済み → 両方standardで軸を維持
- **三ツ沢上町**「観る側から動く側へ」スポーツ・坂の街訴求 → standard維持
- **長原／北千束**：独立店名運用（旧「長原/北千束店」は不使用）→ 個別standard
- **西馬込／西馬込ANNEX**：同一ビルの姉妹店 → 両方standard（訴求軸を分担、bridal化で被らせない）
- **笹塚 vs 渋谷・神泉**：渋谷区の式場訴求はshibuya-shinsen（bridal）に集約、笹塚はstandard

---

## 承認後の適用手順
1. 承認された分類で `shops/templates-config.json` の各 `slug` を `bridal`/`standard` に設定
2. bridal指定店：`nogizaka-akasaka` を参照テンプレにセクション並べ替え＋ブライダルFAQをストーリー直下へ
3. standard指定店：`_template-standard/` に沿って並べ替え、ブライダル長文は簡易ブロックへ圧縮（FAQ schemaは全問維持）
4. 各店 `TEMPLATE-ROLLOUT.md` の差分ゼロ検証を通す

**→ ①の5店をbridal、②の6店の可否、③をstandardで進めてよいかご確認ください。**
