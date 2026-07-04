# NEXUS 店舗ページ 追加・運用ガイド

店舗ページはすべて **`data/stores.json` を単一の情報源（Single Source of Truth）** として、
テンプレート（`scripts/gen_stores.py`）から自動生成されます。
80店舗目以降も **JSON に1エントリ足すだけ** でページを増やせます。

---

## 新店舗を追加する手順

### 1. `data/stores.json` にエントリを追加

`stores` 配列に、以下の形式で1件追加します。

```json
{
  "slug": "shinjuku",                     // URL に使うローマ字（半角英数とハイフン）。重複禁止
  "name": "新宿店",                        // 表示名（「NEXUS」は付けない）
  "prefecture": "東京都",
  "city": "新宿区",
  "postal": "〒160-0000",
  "address": "東京都新宿区…",              // 実住所（必須）
  "stations": [                            // 分かる場合のみ。不明なら null
    {"name": "新宿駅", "line": "JR山手線", "walk_min": null}
  ],
  "area_keywords": ["新宿", "西新宿", "新宿三丁目", "新宿区"],  // 周辺エリア名3〜5個。不明なら null
  "tel": "050-0000-0000",                  // 必須
  "hours": "8:00〜23:00",                   // 必須
  "features": ["完全個室", "手ぶら通いOK", "女性会員85%", "運動初心者歓迎", "AI食事指導"],
  "nearby_landmarks": null,                // 確実なランドマークがあれば配列で。無ければ null
  "booking_url": "https://www.nexus-gym.com/adp/?cid=c01ktyakbz3fk61hg56s6zwrryn&p=pidbwutz6pb9",
  "has_page": true,                        // ページを生成するなら true
  "priority": 2,
  "published": false                       // ← 公開する準備ができたら true にする（下記参照）
}
```

#### データ入力の鉄則（重要）
- **推測で書かない。** 最寄り駅・路線・徒歩分数・ランドマークは、確実に分かるものだけ記載する。
- `walk_min` が不明なときは **null のまま**。テンプレートが「◯◯駅が最寄り」という
  徒歩分数なしの文面に自動フォールバックする（「徒歩◯分」「駅近」等の曖昧表現は出さない）。
- 駅情報が全く無いときは `stations: null`。テンプレートは「◯◯（市区）の住宅街にひっそりと」に切り替わる。
- データが無い FAQ（徒歩分数の質問・ランドマークの質問）は **自動的に出力されない**（質問数は店舗により6〜8問で変動）。

### 2. 生成コマンドを実行

```bash
python3 scripts/gen_stores.py
```

これだけで以下がまとめて更新されます：
- `published: true` かつ `has_page: true` の店舗ページを `/shops/<slug>/` に生成
- `/shops/` 都道府県別ハブを再生成（Coming Soon バナー・店舗数・進捗バーも自動反映）
- `sitemap.xml` の店舗ページ URL を更新
- Search Console 申請用の URL 一覧を標準出力に表示

### 3. 確認してデプロイ

- スマホ表示の崩れがないか確認
- `git add -A && git commit && git push`（= Vercel 本番反映）

---

## 段階的な公開（スパム判定の回避）

Google の「誘導ページ（doorway pages）量産」判定を避けるため、**一気に全店公開しない**。
`published` フラグで公開タイミングを制御する。

- 第1週：主要10店舗ほどを `published: true` にして生成・公開
- 第2〜3週：20〜30店舗ずつ `published: true` に切り替えて再生成・公開

`published: false` の店舗はページが生成されず（ハブでも住所テキストのみ表示）、
公開対象になったら `true` に変えて再実行するだけ。

### 品質ゲート（公開の条件）
`published: true` にする前に、最低限：
- 住所・電話・営業時間がすべて揃っている
- 本文の固有情報（住所・駅・エリア名など）比率が十分（30%以上目安）

揃っていない店舗は `published: false` のままにしておく。

---

## ファイル構成

| パス | 役割 |
|---|---|
| `data/stores.json` | 全店舗の情報（Single Source of Truth） |
| `scripts/gen_stores.py` | ページ・ハブ・sitemap のジェネレーター |
| `shops/index.html` | 都道府県別ハブ（自動生成物・直接編集しない） |
| `shops/<slug>/index.html` | 各店舗ページ（自動生成物・直接編集しない） |

> `shops/` 配下の HTML は生成物です。文面を直したい場合は
> `scripts/gen_stores.py`（テンプレート）または `data/stores.json`（データ）を編集して再生成してください。
