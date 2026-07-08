# 店舗ページ 2テンプレート展開手順

店舗ページを **ブライダル型（bridal）** と **通常型（standard）** の2テンプレートで統一運用するための手順書。

## 成果物

| ファイル | 役割 |
|---|---|
| `shops/nogizaka-akasaka/index.html` | ブライダル型・完成第1号（本番） |
| `shops/_template-standard/index.html` | 通常型・雛形（noindex／`{{TOKEN}}`置換式） |
| `shops/templates-config.json` | 店舗ごとの型指定（bridal / standard） |
| `shops/TEMPLATE-ROLLOUT.md` | 本手順書 |

## テンプレートの指定方法（型の切り替え）

`shops/templates-config.json` の `stores` に `"slug": "bridal" | "standard"` を書く。
展開作業はこの値を参照して、その店舗にどちらのセクション順を適用するか決める。
HTML側は `<main class="st-wrap" data-template="bridal|standard">` にマーカーが入っており、
現在どちらの型かはページを開かずとも `data-template` 属性で判別できる。

```jsonc
{
  "stores": {
    "nogizaka-akasaka": "bridal",   // ブライダル訴求が強い店舗
    "chidoricho": "standard",       // 通常店舗
    ...
  }
}
```

現状 `nogizaka-akasaka` のみ bridal。ブライダル素材・訴求のある店舗を選んで bridal に切り替える。

## セクション順（型の違い）

**ブライダル型（A）**
1. ヒーロー（H1＋バッジ＋CTA・ブライダル前面）
2. ブライダルストーリー（5ステップカード＋モデルケース＋ブライダルFAQ3問アコーディオン）
3. CTA①
4. 料金プラン（4プランカード／ベーシック=人気No.1）
5. CTA②
6. お客様の声（★帯＋口コミ3件＋Googleマップ）
7. この店舗の特徴（写真2枚横並び）
8. アクセス
9. FAQ（店舗＋全店 統合アコーディオン）
10. 最終CTA ＋ 追従フッターCTA

**通常型（B）**
1. ヒーロー（エリア訴求H1＋バッジ＋CTA）
2. この店舗の特徴（写真2枚横並び）
3. 料金プラン（4プランカード）
4. CTA①
5. お客様の声（集約版）
6. ブライダル簡易ブロック（2〜3文＋ブライダル専用ページへのリンクのみ）
7. アクセス
8. FAQ（統合アコーディオン）
9. 最終CTA ＋ 追従フッターCTA

## 絶対に維持するもの（型変換で触らない）

- `<script type="application/ld+json">` … LocalBusiness/ExerciseGym・FAQPage・BreadcrumbList・ImageObject の**内容**
  （例外＝今回の事実修正のみ：`openingHours` を `08:00-23:00` に統一）
- `<title>` / `meta description` / OGP / `canonical`
- H1のキーワード、画像の `alt`
- 店舗固有の事実（住所・最寄り駅・電話・料金・店舗紹介文）
- 内部リンク（bridalページ・110問FAQ・店舗一覧・比較ページ・Googleマップ・`nexus-gym.com/adp` の予約CTA URL）
- FAQの**本文と設問**（表示順の並べ替え・アコーディオン化はOK、本文の削除はNG）

## 事実修正（全店共通・最優先）

- 営業時間の表記を **8:00〜23:00** に統一
  - 本文（アクセス欄・店舗FAQ・統計バーの「8-23時」）
  - LocalBusiness schema の `openingHours` → `"Mo-Su 08:00-23:00"`
- 競合ジムの実名表記があれば **「R社」形式**（頭文字＋社）に置換
  - チェック用: `grep -rn 'ライザップ\|RIZAP\|24/7\|チョコザップ\|エニタイム\|ANYTIME' shops/*/index.html`
- ※ nogizaka-akasaka は上記いずれも対応済み（競合実名は元から無し）

## 展開の進め方（推奨）

各店舗ページは**既存HTMLに全情報（schema・facts・FAQ・alt）が揃っている**ため、
「新規生成」ではなく「既存を維持したままセクションを並べ替える」変換で行う。

### 手順（1店舗あたり）

1. `templates-config.json` でその店舗の型を確認。
2. **事実修正を先に適用**：`7:00〜23:00`→`8:00〜23:00`、`07:00-23:00`→`08:00-23:00`、統計バー `7-23`→`8-23`。競合実名→R社。
3. セクションを対象テンプレの順に並べ替え：
   - `standard`：`_template-standard/index.html` の順序・クラスに合わせる。ブライダル関連の長文ストーリーは「ブライダル簡易ブロック（2〜3文＋リンク）」へ圧縮（**ブライダルFAQ3問はschema・統合FAQ側で維持**）。
   - `bridal`：nogizaka-akasaka を参照。ストーリー直下にブライダルFAQ3問アコーディオンを置き、統合FAQ側の重複表示は外す（schemaは全問維持）。
4. CTAを4カ所（ヒーロー・型別①・②または簡易後・最終）＋追従フッターに統一。予約URLは各店の既存adp URLを流用（**変更禁止**）。
5. 検証（下記チェック）を通す。

### 変換前後の必須チェック（差分ゼロ確認）

```bash
f=shops/<slug>/index.html
grep -c 'application/ld+json' "$f"          # JSON-LDブロック数：変換前後で不変
grep -o '<title>[^<]*</title>' "$f"          # title不変
grep -c '7:00〜23:00\|07:00-23:00\|7-23' "$f" # → 0（営業時間修正済み）
grep -o 'openingHours[^,]*' "$f"             # → 08:00-23:00
grep -o 'data-template="[a-z]*"' "$f"        # 指定した型と一致
grep -c 'nexus-gym.com/adp' "$f"             # 予約CTA本数（ヒーロー+①+②/簡易+最終+追従）
grep -o 'href="\.\./\.\./[a-z/-]*"' "$f" | sort | uniq -c  # 内部リンク：変換前後で不変
```

FAQ設問数（schema `Question` 数）とページ内 `st-faq-item` 数が変換前後で保たれていることも確認。

### 表示確認（390px）

ローカルサーバ＋ヘッドレスChromeでフルページ撮影 → 各セクションが指定順で並び、文字の壁が無いことを確認。

```bash
python3 -m http.server 8791 &   # HP直下で
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --hide-scrollbars --force-device-scale-factor=1 --window-size=390,9000 \
  --screenshot=/tmp/check.png "http://127.0.0.1:8791/shops/<slug>/"
```

## 公開

`feedback_publish_and_index` の方針どおり、公開（git push→Vercel）とSearch Consoleインデックス登録は
ユーザーが「公開」を指示したときに**セット**で実施する（skill: publish-and-index）。
`_template-standard/` は noindex 雛形のため、サイトマップに含めない／実店舗に流用時は `robots` を `index, follow` に戻す。
