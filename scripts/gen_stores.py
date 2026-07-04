#!/usr/bin/env python3
"""NEXUS 店舗ページ ジェネレーター (data-driven).

使い方:
    python3 scripts/gen_stores.py

やること:
  1. data/stores.json を読み込む
  2. published:true かつ has_page:true の店舗ページを /shops/<slug>/ に生成
  3. /shops/ 都道府県別ハブを再生成 (Coming Soon バナー付き)
  4. sitemap.xml の店舗ページ URL を更新
  5. Search Console 申請用の URL 一覧を出力

駅情報・ランドマークが無い店舗はテンプレートが自動フォールバックする。
walk_min が null の場合「徒歩N分」表記は使わない (誤情報回避)。
"""
import json, re, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE_JSON = os.path.join(ROOT, "data", "stores.json")
SITEMAP = os.path.join(ROOT, "sitemap.xml")

PREF_ANCHOR = {"東京都":"tokyo","神奈川県":"kanagawa","埼玉県":"saitama","群馬県":"gunma",
               "栃木県":"tochigi","大阪府":"osaka","愛知県":"aichi","福岡県":"fukuoka"}
BASE = "https://www.withj-inc.com"

def esc(t):
    return (t or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def uniq(seq):
    out=[]
    for x in seq:
        if x not in out: out.append(x)
    return out

def opening_hours(hours):
    m=re.search(r'(\d{1,2}):(\d{2}).*?(\d{1,2}):(\d{2})', hours or "")
    if not m: return None
    return f"Mo-Su {int(m.group(1)):02d}:{m.group(2)}-{int(m.group(3)):02d}:{m.group(4)}"

def main_area(s):
    if s["stations"]:
        return "・".join(uniq(st["name"].replace("駅","") for st in s["stations"]))
    if s["area_keywords"]:
        return s["area_keywords"][0]
    return s["city"]

def lead_text(s):
    area=main_area(s)
    if s["stations"]:
        st0=s["stations"][0]
        stn="・".join(uniq(st["name"] for st in s["stations"]))
        lines="・".join(uniq(st["line"] for st in s["stations"]))
        if st0.get("walk_min"):
            return (f"{st0['name']}から徒歩{st0['walk_min']}分。{s['city']}の住宅街のマンションの一室にある、"
                    f"大きな看板のない隠れ家パーソナルジムです。女性会員85%、運動初心者の30〜40代女性がこっそり通っています。")
        return (f"{lines}・{stn}が最寄り。{s['city']}の住宅街のマンションの一室にある、"
                f"大きな看板のない隠れ家パーソナルジムです。女性会員85%、運動初心者の30〜40代女性がこっそり通っています。")
    return (f"{s['city']}の住宅街にひっそりと佇む、大きな看板のない隠れ家パーソナルジムです。"
            f"マンションの一室にある完全個室で、女性会員85%、運動初心者の30〜40代女性がこっそり通っています。")

def store_faq(s):
    """店舗固有 FAQ。データが無い質問は出さない。"""
    name=s["name"]; area=main_area(s); city=s["city"]; hours=s["hours"]
    kws=s["area_keywords"] or []
    area_label=("・".join(kws[:2]) if kws else area)
    q=[]
    # Q1 location
    if s["stations"]:
        stn="・".join(uniq(st["name"] for st in s["stations"]))
        lines="・".join(uniq(st["line"] for st in s["stations"]))
        q.append((f"{name}はどこにありますか？最寄り駅は？",
                  f"住所は{s['postal']} {s['address']}です。最寄りは{lines}の{stn}。{city}の住宅街のマンションの一室にある、大きな看板のない隠れ家パーソナルジムです。"))
    else:
        q.append((f"{name}はどこにありますか？",
                  f"住所は{s['postal']} {s['address']}です。{city}の住宅街のマンションの一室にある、大きな看板のない隠れ家パーソナルジムです。"))
    # Q2 walk time — only if walk_min present
    if s["stations"] and s["stations"][0].get("walk_min"):
        st0=s["stations"][0]
        q.append((f"{st0['name']}から歩いてどれくらいですか？",
                  f"{st0['name']}（{st0['line']}）から徒歩{st0['walk_min']}分です。{city}の住宅街に位置しています。"))
    # Q3 初心者
    q.append((f"{area_label}エリアで初心者向けのパーソナルジムを探しています。",
              f"{name}は、運動が初めての30〜40代女性が中心の店舗です。会員の約6割が運動経験ほぼゼロからのスタート。完全個室でトレーナーがマンツーマン指導するので、周りの目を気にせず自分のペースで始められます。"))
    # Q4 完全個室
    q.append((f"{area_label}で完全個室のパーソナルジムはありますか？",
              f"はい。{name}は{city}の住宅街のマンションの一室にある完全個室のパーソナルジムです。すっぴん・部屋着感覚で通っても他の会員に会うことがなく、人目を気にせずトレーニングに集中できます。"))
    # Q5 hours
    q.append((f"{name}の営業時間は？仕事帰りでも通えますか？",
              f"営業時間は{hours}です。朝の出勤前も、仕事帰りの夜間も通えます。手ぶら通いOKなので、バッグひとつで立ち寄れます。"))
    # Q6 booking
    q.append((f"{name}の予約はどうやって取りますか？",
              "まずはWEBから無料体験をご予約ください。体験ではカウンセリング・姿勢チェック・実際のトレーニングを行います。入会後の各セッションも予約制で、6時間前まで無料でキャンセル・変更が可能です。"))
    # Q7 women
    q.append((f"{area_label}周辺で女性が通いやすいジムを探しています。",
              f"{name}は女性会員85%。{city}の住宅街にあり、{area_label}エリアにお住まい・お勤めの女性がこっそり通っています。完全個室・手ぶらOKで、女性が通いやすい環境を整えています。"))
    # Q8 landmarks — only if present
    if s["nearby_landmarks"]:
        q.append((f"{name}の周辺には何がありますか？",
                  f"エリアには{('、'.join(s['nearby_landmarks']))}などがあります。{city}の落ち着いた住宅街に位置する、看板を控えめにした隠れ家ジムです。"))
    return q

COMMON_FAQ=[
 ("料金はいくらですか？","ライト（30分）月4回18,000円〜、ベーシック（60分）月4回34,000円〜など。1回あたり4,500円〜から始められます（すべて税込）。詳しくは料金プランをご覧ください。"),
 ("手ぶらで通えますか？","はい。ウェア・水・タオル・プロテインまで無料提供で手ぶら通いOK。仕事帰りにバッグひとつで通えます。"),
 ("キャンセルはいつまでできますか？","6時間前まで無料でキャンセル・変更が可能です。当日の急な体調不良やお子さまの発熱にも対応しやすい設計です。"),
 ("食事指導はありますか？","月額3,000円（税込）のAI食事指導があります。写真を送るだけで、無理を強いない範囲で痩せる食べ方をサポートします。"),
 ("トレーナーはどんな人ですか？","全トレーナーが3ヶ月の厳しい自社教育プログラムを修了してからデビュー。「優しく寄り添う指導」を全店共通の基準としています。"),
 ("女性会員は多いですか？","女性会員比率は85%です。30〜40代女性を中心に、運動初心者の方が多く通っています。"),
 ("体験の流れは？","無料体験は60分程度。カウンセリング → 姿勢チェック → トレーニング体験の流れです。当日入会で入会金が55,000円→15,000円（税込）に割引されます。"),
]

STORE_CSS="""
.st-wrap { max-width: 820px; margin: 0 auto; padding: 8px 6% 90px; position: relative; z-index: 1; }
.st-eyebrow { color: var(--accent1); font-weight:700; font-size:12px; letter-spacing:.18em; text-transform:uppercase; margin: 26px 0 10px; }
.st-wrap h1 { font-size: clamp(23px,5.6vw,34px); font-weight:900; line-height:1.4; margin:0 0 16px; }
.st-wrap h1 .ac { color: var(--accent1); }
.st-lead { font-size:15px; line-height:2; color: var(--ink-soft); border-left:3px solid var(--accent2); padding-left:16px; margin:0 0 8px; }
.st-wrap h2 { font-size:20px; font-weight:800; margin:44px 0 14px; }
.st-wrap p { color: var(--ink-soft); line-height:1.95; font-size:14.5px; }
.st-feature-list { list-style:none; padding:0; margin:14px 0 0; display:flex; flex-wrap:wrap; gap:8px; }
.st-feature-list li { background: var(--bg-card); border:1px solid var(--line); border-radius:999px; padding:7px 15px; font-size:13px; color:var(--ink); }
.st-feature-list li::before { content:"✓ "; color: var(--accent1); font-weight:800; }
.st-info { display:grid; gap:0; margin:16px 0 0; border:1px solid var(--line); border-radius:14px; overflow:hidden; }
.st-info .row { display:grid; grid-template-columns:96px 1fr; border-bottom:1px solid var(--line); }
.st-info .row:last-child { border-bottom:none; }
.st-info dt { background: var(--bg-soft); color: var(--ink-faint); font-size:12px; font-weight:700; padding:14px 14px; }
.st-info dd { margin:0; padding:14px 14px; font-size:14px; color: var(--ink); }
.st-map { margin-top:16px; border-radius:14px; overflow:hidden; border:1px solid var(--line); aspect-ratio:16/10; }
.st-map iframe { width:100%; height:100%; border:0; display:block; }
.st-price { display:grid; gap:10px; margin-top:14px; }
.st-price .row { display:flex; justify-content:space-between; align-items:center; gap:12px; background: var(--bg-card); border:1px solid var(--line); border-radius:12px; padding:14px 16px; }
.st-price .cn { font-weight:700; font-size:14px; } .st-price .cn span { display:block; color: var(--ink-faint); font-size:12px; font-weight:400; }
.st-price .cp { text-align:right; white-space:nowrap; } .st-price .cp b { color: var(--accent1); font-size:17px; } .st-price .cp small { display:block; color:var(--ink-faint); font-size:12px; }
.st-faq-item { border:1px solid var(--line); border-radius:12px; margin-top:10px; overflow:hidden; background: var(--bg-soft); }
.st-faq-item summary { list-style:none; cursor:pointer; display:flex; align-items:center; gap:10px; padding:16px 16px; font-weight:700; font-size:14.5px; color:var(--ink); }
.st-faq-item summary::-webkit-details-marker { display:none; }
.st-faq-item summary .q { color: var(--accent1); font-weight:900; }
.st-faq-item summary .ic { margin-left:auto; color: var(--accent1); font-weight:800; }
.st-faq-item[open] summary .ic { transform: rotate(45deg); }
.st-faq-a { padding:0 16px 18px 40px; color: var(--ink-soft); font-size:14px; line-height:1.9; }
.st-common summary { color: var(--ink-soft); }
.st-note { color: var(--ink-faint); font-size:12px; margin-top:12px; }
.st-ilink { display:inline-flex; align-items:center; gap:6px; margin-top:16px; color: var(--accent1); font-size:14px; font-weight:700; text-decoration:none; border-bottom:1px solid var(--line-accent); padding-bottom:2px; }
.st-ilink::after { content:"→"; }
.st-rev-avg { display:flex; align-items:center; flex-wrap:wrap; gap:8px; margin:6px 0 4px; }
.st-rev-avg b { font-size:22px; color:var(--ink); }
.st-rev-avg .cnt { color:var(--ink-soft); font-size:13px; }
.st-rev-avg .asof { color:var(--ink-faint); font-size:12px; }
.st-stars { color:#FBBF24; letter-spacing:1px; font-size:16px; }
.st-stars .empty { color: rgba(255,255,255,.20); }
.st-rev-src { color:var(--ink-faint); font-size:12px; margin:0 0 14px; }
.st-rev-src a { color:var(--accent1); }
.st-rev-list { display:grid; gap:12px; grid-template-columns:1fr; }
.st-rev-card { background:var(--bg-soft); border:1px solid var(--line); border-radius:14px; padding:18px 18px; }
.st-rev-card .st-rev-stars { margin-bottom:8px; }
.st-rev-card .txt { color:var(--ink); font-size:14px; line-height:1.9; margin:0 0 10px; }
.st-rev-card .who { color:var(--ink-faint); font-size:12.5px; }
.st-cta { text-align:center; margin-top:24px; background: var(--bg-card); border:1px solid var(--line); border-radius:18px; padding:30px 22px; }
.st-cta h3 { font-size:19px; font-weight:800; margin:0 0 8px; }
.st-cta p { margin:0 0 18px; }
.st-cta-btn { display:inline-flex; align-items:center; justify-content:center; background: linear-gradient(135deg,var(--accent1),var(--accent2)); color:#fff; font-weight:800; font-size:16px; padding:16px 34px; border-radius:999px; text-decoration:none; }
.st-sticky { position:fixed; left:0; right:0; bottom:0; z-index:50; background: rgba(5,5,7,.92); backdrop-filter: blur(8px); border-top:1px solid var(--line); padding:8px 14px calc(8px + env(safe-area-inset-bottom)); }
.st-sticky a { display:flex; align-items:center; justify-content:center; height:48px; max-width:480px; margin:0 auto; background: linear-gradient(135deg,var(--accent1),var(--accent2)); color:#fff; font-weight:800; font-size:15px; border-radius:999px; text-decoration:none; }
@media (max-width:768px) { .st-wrap { padding:8px 18px 96px; } .st-info .row { grid-template-columns:84px 1fr; } }
"""

def star_html(rating):
    try: full=max(0,min(5,int(round(float(rating)))))
    except (TypeError,ValueError): full=0
    s='<span class="st-stars">'+('★'*full)
    if full<5: s+='<span class="empty">'+('★'*(5-full))+'</span>'
    return s+'</span>'

def reviews_section(s):
    """Googleマップ口コミの引用セクション。
    - google フィールドが無ければ非表示（空文字）
    - rating のみ / reviews 空 → 評価+件数+リンクの簡易表示
    - 口コミ本文は原文のまま（HTMLエスケープのみ）。出典必須。Schema には出さない。
    """
    g=s.get("google")
    if not g: return ""
    place=g.get("place_url"); rating=g.get("rating"); count=g.get("review_count")
    as_of=g.get("rating_as_of"); reviews=g.get("reviews") or []
    asof_label=""
    if as_of:
        m=re.match(r'(\d{4})-(\d{1,2})', as_of)
        if m: asof_label=f"※{int(m.group(1))}年{int(m.group(2))}月時点"
    parts=['<h2>Googleマップの口コミ</h2>']
    if rating:
        avg=f'<div class="st-rev-avg">{star_html(rating)}<b>{esc(str(rating))}</b>'
        if count: avg+=f'<span class="cnt">（{esc(str(count))}件）</span>'
        if asof_label: avg+=f'<span class="asof">{asof_label}</span>'
        avg+='</div>'
        parts.append(avg)
    if place:
        parts.append(f'<p class="st-rev-src">出典：<a href="{esc(place)}" target="_blank" rel="noopener">Google マップ</a></p>')
    else:
        parts.append('<p class="st-rev-src">出典：Google マップ</p>')
    if reviews:
        cards=[]
        for r in reviews:
            txt=esc(r.get("text") or "").replace("\n","<br>")
            who=esc(r.get("author_initial") or "Googleユーザー")
            date=esc(r.get("date") or "")
            meta=who+(" ・ "+date if date else "")
            cards.append(f'<div class="st-rev-card"><div class="st-rev-stars">{star_html(r.get("rating") or 0)}</div><p class="txt">{txt}</p><div class="who">{meta}</div></div>')
        parts.append('<div class="st-rev-list">'+"\n".join(cards)+'</div>')
    if place:
        parts.append(f'<a class="st-ilink" href="{esc(place)}" target="_blank" rel="noopener">すべての口コミはGoogleマップでご覧いただけます</a>')
    return "\n".join(parts)

def gen_store_page(s):
    slug=s["slug"]; name=s["name"]; full=f"NEXUSパーソナルジム {name}"
    pref=s["prefecture"]; city=s["city"]; addr=s["address"]; postal=s["postal"]; tel=s["tel"]; hours=s["hours"]
    area=main_area(s); booking=s["booking_url"]; url=f"{BASE}/shops/{slug}/"
    map_q=urllib.parse.quote(addr); anchor=PREF_ANCHOR.get(pref,"")
    sfaq=store_faq(s)

    if s["stations"]:
        stn="・".join(uniq(st["name"] for st in s["stations"])); lines="・".join(uniq(st["line"] for st in s["stations"]))
        station_dd=f"{lines}　{stn}"
    else:
        station_dd="—"

    faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in sfaq]}
    gym={"@context":"https://schema.org","@type":"ExerciseGym","name":full,
        "image":f"{BASE}/images/nexus/gym-bright.jpg",
        "address":{"@type":"PostalAddress","postalCode":(postal or "").replace("〒",""),"addressRegion":pref,"addressLocality":city,"streetAddress":addr,"addressCountry":"JP"},
        "telephone":tel,"priceRange":"¥18,000〜/月（1回4,500円〜）","url":url,
        "parentOrganization":{"@type":"Organization","name":"NEXUS Personal Gym","description":"全国71店舗（80店舗までオープン予定）の完全個室パーソナルジム"}}
    oh=opening_hours(hours)
    if oh: gym["openingHours"]=oh
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"ホーム","item":f"{BASE}/"},
        {"@type":"ListItem","position":2,"name":"店舗一覧","item":f"{BASE}/shops/"},
        {"@type":"ListItem","position":3,"name":pref,"item":f"{BASE}/shops/#{anchor}"},
        {"@type":"ListItem","position":4,"name":name}]}

    title=f"{full}｜{area}の完全個室・隠れ家ジム | WITHJ"
    if s["stations"]:
        lines="・".join(uniq(st["line"] for st in s["stations"])); stn="・".join(uniq(st["name"] for st in s["stations"]))
        desc=f"{area}のパーソナルジムならNEXUS{name}。{lines}・{stn}が最寄り、{city}の住宅街のマンションの一室にある完全個室の隠れ家ジム。女性会員85%・手ぶらOK・1回4,500円〜。無料体験実施中。"
    else:
        desc=f"{area}のパーソナルジムならNEXUS{name}。{city}の住宅街のマンションの一室にある完全個室の隠れ家ジム。女性会員85%・手ぶらOK・1回4,500円〜。無料体験実施中。"

    feat_html="".join(f'<li>{esc(f)}</li>' for f in s["features"])
    def faq_block(items, common=False):
        cls=" st-common" if common else ""
        return "\n".join(f'  <details class="st-faq-item{cls}"><summary><span class="q">Q</span>{esc(q)}<span class="ic">+</span></summary><div class="st-faq-a">{esc(a)}</div></details>' for q,a in items)
    sfaq_html=faq_block(sfaq); cfaq_html=faq_block(COMMON_FAQ, True)

    # feature paragraph (fallback-safe)
    kw_join="・".join((s["area_keywords"] or [])[:4]) if s["area_keywords"] else city
    lm_line=(f"エリアには{('、'.join(s['nearby_landmarks']))}などがあり、" if s["nearby_landmarks"] else "")
    feat_para=(f"NEXUS{name}は、{pref}{city}の落ち着いた住宅街に佇む完全個室のパーソナルジム。大きな看板を出していないため、"
               f"{kw_join}エリアで「人目を気にせず綺麗になりたい」という30〜40代女性に選ばれています。{lm_line}"
               f"ウェア・タオル・プロテインまで無料提供の手ぶら通いOKで、忙しい毎日でもバッグひとつで続けられます。")

    p=[]
    p.append('<!DOCTYPE html>\n<html lang="ja">\n<head>')
    p.append('<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    p.append(f'<title>{esc(title)}</title>')
    p.append(f'<meta name="description" content="{esc(desc)}">')
    p.append('<meta name="robots" content="index, follow">')
    p.append(f'<link rel="canonical" href="{url}">')
    p.append('<meta property="og:type" content="business.business">')
    p.append(f'<meta property="og:title" content="{esc(full)}｜{esc(area)}の完全個室・隠れ家ジム">')
    p.append(f'<meta property="og:description" content="{esc(desc)}">')
    p.append(f'<meta property="og:url" content="{url}">')
    p.append(f'<meta property="og:image" content="{BASE}/images/nexus/gym-bright.jpg">')
    p.append('<meta property="og:site_name" content="株式会社WITHJ">\n<meta property="og:locale" content="ja_JP">\n<meta name="twitter:card" content="summary_large_image">')
    for sc in (gym,faqpage,crumb):
        p.append('<script type="application/ld+json">\n'+json.dumps(sc,ensure_ascii=False,indent=2)+'\n</script>')
    p.append('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;800;900&family=Noto+Sans+JP:wght@400;700;900&family=Bebas+Neue&display=swap" rel="stylesheet">')
    p.append('<link rel="stylesheet" href="../../gym-blog/style.css">')
    p.append('<style>'+STORE_CSS+'</style>\n</head>\n<body>')
    p.append('<header class="gb-header"><a href="../../" class="gb-logo">WITHJ<span class="accent"> / Gym Blog</span></a><nav class="gb-nav"><a href="../../">TOP</a><a href="../../gym-blog/">BLOG</a><a href="../">店舗一覧</a><a href="../../faq/">FAQ</a></nav></header>')
    p.append(f'<nav class="gb-breadcrumb" aria-label="パンくず"><ol><li><a href="../../">ホーム</a></li><li><a href="../">店舗一覧</a></li><li><a href="../#{anchor}">{pref}</a></li><li aria-current="page">{name}</li></ol></nav>')
    p.append('<main class="st-wrap">')
    p.append(f'<p class="st-eyebrow">NEXUS Personal Gym ／ {pref}{city}</p>')
    p.append(f'<h1>{esc(full)}｜<span class="ac">{esc(area)}</span>の完全個室・隠れ家ジム</h1>')
    p.append(f'<p class="st-lead">{esc(lead_text(s))}</p>')
    p.append(f'<ul class="st-feature-list">{feat_html}</ul>')
    p.append('<h2>この店舗の特徴</h2>')
    p.append(f'<p>{esc(feat_para)}</p>')
    p.append('<h2>料金プラン</h2><div class="st-price">'
     '<div class="row"><div class="cn">ライトコース<span>30分 / 月4回</span></div><div class="cp"><b>18,000円</b><small>税込 / 1回4,500円</small></div></div>'
     '<div class="row"><div class="cn">ベーシックコース<span>60分 / 月4回</span></div><div class="cp"><b>34,000円</b><small>税込 / 1回8,500円</small></div></div>'
     '<div class="row"><div class="cn">プレミアムコース<span>90分 / 月4回</span></div><div class="cp"><b>48,000円</b><small>税込 / 1回12,000円</small></div></div>'
     '<div class="row"><div class="cn">セミパーソナル<span>60分 / 月2回</span></div><div class="cp"><b>11,000円</b><small>税込 / 1回5,500円</small></div></div>'
     '</div><p class="st-note">入会金は通常55,000円、無料体験当日入会で15,000円（税込）に割引。全店舗共通の料金です。</p>')
    p.append('<h2>アクセス</h2><dl class="st-info">'
     f'<div class="row"><dt>店舗名</dt><dd>{esc(full)}</dd></div>'
     f'<div class="row"><dt>住所</dt><dd>{postal}<br>{addr}</dd></div>'
     f'<div class="row"><dt>最寄り駅</dt><dd>{station_dd}</dd></div>'
     f'<div class="row"><dt>営業時間</dt><dd>{hours}</dd></div>'
     f'<div class="row"><dt>電話番号</dt><dd>{tel}</dd></div></dl>'
     f'<div class="st-map"><iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={map_q}&z=16&output=embed" title="{esc(full)}の地図"></iframe></div>')
    revs=reviews_section(s)
    if revs: p.append(revs)
    p.append(f'<h2>{name}のよくある質問</h2>\n{sfaq_html}')
    p.append('<h2 style="font-size:17px;margin-top:36px">よくある質問（全店共通）</h2><p style="font-size:13px;color:var(--ink-faint);margin:0 0 4px">料金・制度などNEXUS全店に共通するご質問です。さらに詳しくは110問のFAQをご覧ください。</p>\n'+cfaq_html)
    p.append('<a class="st-ilink" href="../../faq/">パーソナルジムの疑問を110問FAQで解決する</a><br><a class="st-ilink" href="../../gym-blog/gym-comparison/nexus-personal-gym/">NEXUSパーソナルジムの特徴・料金をもっと見る</a>')
    p.append(f'<div class="st-cta"><h3>{esc(area)}で、こっそり綺麗になりませんか？</h3><p>まずは無料体験で、話だけ聞きに来ませんか？<br>※無理な勧誘は一切ありません</p><a class="st-cta-btn" href="{booking}" target="_blank" rel="noopener noreferrer">無料体験を予約する</a></div>')
    p.append('</main>')
    p.append(f'<div class="st-sticky"><a href="{booking}" target="_blank" rel="noopener noreferrer">まずは無料体験を予約する（勧誘なし）</a></div>')
    p.append('<footer class="gb-footer"><div class="gb-footer-logo">WITHJ</div><nav style="display:flex;gap:24px;flex-wrap:wrap;"><a href="../" style="color:var(--ink-faint);font-size:12px;">店舗一覧</a><a href="../../gym-blog/" style="color:var(--ink-faint);font-size:12px;">パーソナルジムブログ</a><a href="../../faq/" style="color:var(--ink-faint);font-size:12px;">よくある質問</a><a href="../../privacy/" style="color:var(--ink-faint);font-size:12px;">プライバシーポリシー</a></nav><div>© 2026 株式会社WITHJ All Rights Reserved.</div></footer>')
    p.append('</body>\n</html>')
    outdir=os.path.join(ROOT,"shops",slug)
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir,"index.html"),"w",encoding="utf-8").write("\n".join(p))
    return url

HUB_CSS="""
.sh-wrap { max-width: 900px; margin:0 auto; padding: 8px 6% 90px; position:relative; z-index:1; }
.sh-eyebrow { color: var(--accent1); font-weight:700; font-size:12px; letter-spacing:.18em; text-transform:uppercase; margin:26px 0 10px; }
.sh-wrap h1 { font-size: clamp(22px,5.4vw,32px); font-weight:900; line-height:1.4; margin:0 0 12px; }
.sh-wrap h1 .ac { color: var(--accent1); }
.sh-lead { color: var(--ink-soft); font-size:14.5px; line-height:1.95; max-width:760px; }
.sh-pillnav { display:flex; flex-wrap:wrap; gap:8px; margin:20px 0 8px; }
.sh-pillnav a { background: var(--bg-card); border:1px solid var(--line); border-radius:999px; padding:8px 14px; font-size:13px; font-weight:700; color:var(--ink); text-decoration:none; }
.sh-pillnav a b { color: var(--accent1); }
.sh-pref { margin-top:40px; }
.sh-pref h2 { font-size:20px; font-weight:800; padding-left:12px; border-left:4px solid var(--accent1); margin:0 0 4px; }
.sh-pref .cnt { color: var(--ink-faint); font-size:12px; margin:0 0 14px; padding-left:12px; }
.sh-store { display:block; background: var(--bg-soft); border:1px solid var(--line); border-radius:12px; padding:16px 16px; margin-top:10px; text-decoration:none; }
a.sh-store:hover { border-color: var(--line-accent); }
.sh-store .nm { font-weight:800; font-size:15px; color:var(--ink); display:flex; align-items:center; gap:8px; }
.sh-store .badge { font-size:11px; font-weight:800; color:#fff; background: linear-gradient(135deg,var(--accent1),var(--accent2)); border-radius:999px; padding:2px 9px; }
a.sh-store .arrow { margin-left:auto; color: var(--accent1); font-weight:800; }
.sh-store .meta { color: var(--ink-soft); font-size:13px; margin-top:6px; line-height:1.8; }
.sh-store .meta .tel { color: var(--ink-faint); }
.sh-ilink { display:inline-flex; gap:6px; margin-top:22px; color:var(--accent1); font-size:14px; font-weight:700; text-decoration:none; border-bottom:1px solid var(--line-accent); padding-bottom:2px; }
.sh-ilink::after { content:"→"; }
.sh-soon { position:relative; overflow:hidden; margin:22px 0 6px; padding:22px 22px; border-radius:16px; border:1px solid var(--line-accent); background:linear-gradient(135deg, rgba(0,240,255,.10), rgba(255,0,170,.10)); }
.sh-soon .tag { display:inline-flex; align-items:center; gap:8px; font-family:'Bebas Neue',sans-serif; letter-spacing:.18em; font-size:13px; color:var(--accent1); }
.sh-soon .tag::before { content:""; width:8px; height:8px; border-radius:50%; background:var(--accent2); box-shadow:0 0 0 0 rgba(255,0,170,.5); animation:shPulse 1.8s infinite; }
@keyframes shPulse { 0%{box-shadow:0 0 0 0 rgba(255,0,170,.5);} 70%{box-shadow:0 0 0 10px rgba(255,0,170,0);} 100%{box-shadow:0 0 0 0 rgba(255,0,170,0);} }
.sh-soon h2 { border:none!important; padding:0!important; margin:8px 0 4px!important; font-size:clamp(19px,5vw,26px); font-weight:900; }
.sh-soon h2 b { background:linear-gradient(90deg,var(--accent1),var(--accent2)); -webkit-background-clip:text; background-clip:text; color:transparent; }
.sh-soon p { color:var(--ink-soft); font-size:13.5px; margin:0; }
.sh-bar { margin-top:14px; height:12px; border-radius:999px; background:var(--bg-card); border:1px solid var(--line); overflow:hidden; }
.sh-bar span { display:block; height:100%; background:linear-gradient(90deg,var(--accent1),var(--accent2)); border-radius:999px; }
.sh-bar-lbl { display:flex; justify-content:space-between; margin-top:6px; font-size:12px; color:var(--ink-faint); }
.sh-bar-lbl b { color:var(--ink); }
@media (max-width:768px){ .sh-wrap { padding:8px 18px 80px; } }
"""

def gen_hub(data):
    from collections import OrderedDict
    stores=data["stores"]; total=len(stores)
    groups=OrderedDict()
    for s in stores: groups.setdefault(s["prefecture"],[]).append(s)
    def store_html(s):
        nm=f'NEXUS {s["name"]}'; meta=f'{s["postal"] or ""} {esc(s["address"])}'
        tel=f' ／ <span class="tel">TEL {s["tel"]}</span>' if s["tel"] else ""
        if s.get("has_page") and s.get("published"):
            return (f'<a class="sh-store" href="{s["slug"]}/"><div class="nm">{esc(nm)}<span class="badge">店舗ページ</span><span class="arrow">→</span></div><div class="meta">{meta}{tel}</div></a>')
        return (f'<div class="sh-store"><div class="nm">{esc(nm)}</div><div class="meta">{meta}{tel}</div></div>')
    pills="".join(f'<a href="#{PREF_ANCHOR[p]}">{p} <b>{len(v)}</b></a>' for p,v in groups.items())
    sections=[]
    for p,v in groups.items():
        sections.append(f'<section class="sh-pref" id="{PREF_ANCHOR[p]}"><h2>{p}</h2><div class="cnt">{len(v)}店舗</div>\n'+"\n".join(store_html(s) for s in v)+'\n</section>')
    pct=round(total/80*100,2)
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"ホーム","item":f"{BASE}/"},
        {"@type":"ListItem","position":2,"name":"店舗一覧"}]}
    title=f"NEXUSパーソナルジム 全国店舗一覧｜全国{total}店舗（80店舗までオープン予定） | WITHJ"
    desc=f"NEXUSパーソナルジムの全国{total}店舗（80店舗までオープン予定）一覧。東京都・神奈川県・大阪府など、住所・電話・営業時間を都道府県別に掲載。完全個室・女性会員85%の隠れ家パーソナルジム。"
    p=[]
    p.append('<!DOCTYPE html>\n<html lang="ja">\n<head>')
    p.append('<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    p.append(f'<title>{esc(title)}</title>')
    p.append(f'<meta name="description" content="{esc(desc)}">')
    p.append('<meta name="robots" content="index, follow">')
    p.append(f'<link rel="canonical" href="{BASE}/shops/">')
    p.append('<meta property="og:type" content="website">')
    p.append(f'<meta property="og:title" content="NEXUSパーソナルジム 全国店舗一覧｜全国{total}店舗（80店舗までオープン予定）">')
    p.append(f'<meta property="og:description" content="{esc(desc)}">')
    p.append(f'<meta property="og:url" content="{BASE}/shops/">')
    p.append(f'<meta property="og:image" content="{BASE}/images/nexus/gym-bright.jpg">')
    p.append('<meta property="og:site_name" content="株式会社WITHJ">\n<meta property="og:locale" content="ja_JP">')
    p.append('<script type="application/ld+json">\n'+json.dumps(crumb,ensure_ascii=False,indent=2)+'\n</script>')
    p.append('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;800;900&family=Noto+Sans+JP:wght@400;700;900&family=Bebas+Neue&display=swap" rel="stylesheet">')
    p.append('<link rel="stylesheet" href="../gym-blog/style.css">')
    p.append('<style>'+HUB_CSS+'</style>\n</head>\n<body>')
    p.append('<header class="gb-header"><a href="../" class="gb-logo">WITHJ<span class="accent"> / Gym Blog</span></a><nav class="gb-nav"><a href="../">TOP</a><a href="../gym-blog/">BLOG</a><a href="../nexus-fc/">FC</a><a href="../faq/">FAQ</a></nav></header>')
    p.append('<nav class="gb-breadcrumb" aria-label="パンくず"><ol><li><a href="../">ホーム</a></li><li aria-current="page">店舗一覧</li></ol></nav>')
    p.append('<main class="sh-wrap">')
    p.append('<p class="sh-eyebrow">NEXUS Personal Gym ／ Store List</p>')
    p.append(f'<h1>NEXUSパーソナルジム 全国店舗一覧｜<span class="ac">全国{total}店舗</span>（80店舗までオープン予定）</h1>')
    p.append(f'<p class="sh-lead">住宅街のマンションの一室にある完全個室の隠れ家パーソナルジム「NEXUS」。女性会員85%・手ぶらOK・1回4,500円〜。東京都・神奈川県を中心に全国{total}店舗を展開中です。都道府県から、お近くの店舗をお探しください。</p>')
    p.append(f'<div class="sh-pillnav">{pills}</div>')
    p.append(f'<div class="sh-soon"><span class="tag">COMING SOON</span><h2>まもなく<b>全国80店舗</b>へ。</h2><p>現在{total}店舗。80店舗のオープンに向けて、続々と新店舗を準備中です。あなたの街にも、こっそり通える隠れ家ジムが増えていきます。</p><div class="sh-bar"><span style="width:{pct}%"></span></div><div class="sh-bar-lbl"><span>{total}店舗オープン</span><b>目標 80店舗</b></div></div>')
    p.append("\n".join(sections))
    p.append('<a class="sh-ilink" href="../gym-blog/gym-comparison/nexus-personal-gym/">NEXUSパーソナルジムの特徴・料金を見る</a><br><a class="sh-ilink" href="../faq/">パーソナルジムのよくある質問（110問）</a>')
    p.append('</main>')
    p.append('<footer class="gb-footer"><div class="gb-footer-logo">WITHJ</div><nav style="display:flex;gap:24px;flex-wrap:wrap;"><a href="../gym-blog/" style="color:var(--ink-faint);font-size:12px;">パーソナルジムブログ</a><a href="../faq/" style="color:var(--ink-faint);font-size:12px;">よくある質問</a><a href="../nexus-fc/" style="color:var(--ink-faint);font-size:12px;">NEXUS FC</a><a href="../privacy/" style="color:var(--ink-faint);font-size:12px;">プライバシーポリシー</a></nav><div>© 2026 株式会社WITHJ All Rights Reserved.</div></footer>')
    p.append('</body>\n</html>')
    open(os.path.join(ROOT,"shops","index.html"),"w",encoding="utf-8").write("\n".join(p))

def update_sitemap(store_urls):
    xml=open(SITEMAP,encoding="utf-8").read()
    # remove existing store-page <url> blocks (/shops/<slug>/) but keep hub /shops/
    def keep(block):
        m=re.search(r'<loc>(.*?)</loc>', block)
        if not m: return True
        loc=m.group(1)
        return not re.match(rf'{re.escape(BASE)}/shops/[^/]+/$', loc)
    blocks=re.split(r'(?=<url>)', xml)
    kept=[b for b in blocks if keep(b)]
    xml="".join(kept)
    # insert fresh store entries right before </urlset>
    entries="".join(
        f'  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-06-16</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'
        for u in store_urls)
    xml=xml.replace('</urlset>', entries+'</urlset>')
    open(SITEMAP,"w",encoding="utf-8").write(xml)

def main():
    data=json.load(open(STORE_JSON,encoding="utf-8"))
    published=[s for s in data["stores"] if s.get("published") and s.get("has_page")]
    urls=[]
    for s in published:
        urls.append(gen_store_page(s))
    gen_hub(data)
    update_sitemap(urls)
    print(f"Generated {len(published)} published store pages:")
    for u in urls: print("  ", u)
    print("\n--- Search Console 申請用 URL 一覧 ---")
    print(f"{BASE}/shops/")
    for u in urls: print(u)

if __name__=="__main__":
    main()
