#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_article.py — content/articles/{slug}.md から記事HTMLを生成する。

書き込むのは「生成記事（gym-blog/{category}/{slug}/index.html）」と
「変換画像（images/gym-blog/{slug}/*.webp）」のみ。既存HTMLは一切変更しない。

使い方:
  python3 scripts/build_article.py content/articles/foo.md        # 1本ビルド
  python3 scripts/build_article.py --rebuild-all                  # 全mdを再ビルド
  --force を付けない限り、既存の生成先 index.html は上書きしない。

禁止語（投資回収/No.1/日本一/最安）が入力mdにあれば非ゼロ終了。
cover.jpg が無い場合はプレースホルダ画像を自動生成して仮公開できる。
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.withj-inc.com"
TEMPLATE = os.path.join(ROOT, "scripts", "article_template.html")
AUTHORS = os.path.join(ROOT, "data", "authors.json")
AFFILIATE = os.path.join(ROOT, "data", "affiliate-links.json")

CATEGORIES = {
    "personal-gym": "パーソナルジム",
    "pilates": "ピラティス",
    "nutrition": "食事・栄養",
}

FORBIDDEN = ["投資回収", "No.1", "NO.1", "no.1", "日本一", "最安"]

REQUIRED_KEYS = ["title", "description", "slug", "category", "date", "author"]


def fail(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def render(tpl, **kw):
    """テンプレート中の {key} トークンのみ置換（CSS等の波括弧は無関係に温存）。"""
    for k, v in kw.items():
        tpl = tpl.replace("{" + k + "}", v)
    return tpl


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# ---------- frontmatter ----------

def parse_frontmatter(text, path):
    m = re.match(r"(?s)^---\n(.*?)\n---\n(.*)$", text)
    if not m:
        fail(f"{path}: frontmatter（--- ... ---）がありません")
    fm = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    for k in REQUIRED_KEYS:
        if not fm.get(k):
            fail(f"{path}: frontmatter に {k} がありません")
    if fm["category"] not in CATEGORIES:
        fail(f"{path}: category '{fm['category']}' は未対応です（{'/'.join(CATEGORIES)}）")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", fm["date"]):
        fail(f"{path}: date は YYYY-MM-DD 形式にしてください")
    return fm, m.group(2)


def check_forbidden(text, path):
    hits = [w for w in FORBIDDEN if w in text]
    if hits:
        fail(f"{path}: 禁止語を検出しました: {hits}")


# ---------- markdown（必要最小限のサブセット） ----------

def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md_to_html(md):
    """h2/h3・段落・ul/ol・表・引用・HTMLコメント温存。h2一覧も返す。"""
    out, h2s = [], []
    # HTMLコメントはブロックとして温存するため先にトークン化
    tokens = re.split(r"(<!--.*?-->)", md, flags=re.S)
    blocks = []
    for tok in tokens:
        if tok.startswith("<!--"):
            blocks.append(("comment", tok))
        else:
            for blk in re.split(r"\n\s*\n", tok):
                if blk.strip():
                    blocks.append(("md", blk.strip()))

    h2_idx = 0
    for kind, blk in blocks:
        if kind == "comment":
            out.append("    " + blk)
            continue
        lines = blk.splitlines()
        first = lines[0]
        if first.startswith("### "):
            out.append(f"    <h3>{inline(first[4:])}</h3>")
            rest = "\n".join(lines[1:]).strip()
            if rest:
                out.append(f"    <p>{inline(rest)}</p>")
        elif first.startswith("## "):
            h2_idx += 1
            hid = f"sec{h2_idx}"
            text = first[3:].strip()
            h2s.append((hid, text))
            out.append(f'    <h2 id="{hid}">{inline(text)}</h2>')
            rest = "\n".join(lines[1:]).strip()
            if rest:
                out.append(f"    <p>{inline(rest)}</p>")
        elif first.startswith("> "):
            quote = " ".join(l[2:] for l in lines if l.startswith("> "))
            out.append(f"    <blockquote>{inline(quote)}</blockquote>")
        elif first.startswith("- "):
            items = "".join(f"\n      <li>{inline(l[2:])}</li>" for l in lines if l.startswith("- "))
            out.append(f"    <ul>{items}\n    </ul>")
        elif re.match(r"^\d+\. ", first):
            num = re.compile(r"^\d+\. ")
            items = "".join(
                "\n      <li>" + inline(num.sub("", l)) + "</li>"
                for l in lines if num.match(l))
            out.append(f"    <ol>{items}\n    </ol>")
        elif first.startswith("|"):
            rows = [l for l in lines if l.strip().startswith("|")]
            header = [c.strip() for c in rows[0].strip("|").split("|")]
            body_rows = [r for r in rows[1:] if not re.match(r"^\|[\s:|-]+\|$", r.strip())]
            html = ["    <table>", "      <thead><tr>" +
                    "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead>",
                    "      <tbody>"]
            for r in body_rows:
                cells = [c.strip() for c in r.strip("|").split("|")]
                html.append("        <tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            html += ["      </tbody>", "    </table>"]
            out.append("\n".join(html))
        else:
            out.append(f"    <p>{inline(' '.join(l.strip() for l in lines))}</p>")
    return "\n".join(out), h2s


# ---------- 画像 ----------

def build_cover(slug, fm):
    """cover.jpg→cover.webp 変換。無ければプレースホルダを生成して仮公開可にする。"""
    from PIL import Image
    img_dir = os.path.join(ROOT, "images", "gym-blog", slug)
    os.makedirs(img_dir, exist_ok=True)
    jpg = os.path.join(img_dir, "cover.jpg")
    webp = os.path.join(img_dir, "cover.webp")
    if os.path.exists(jpg):
        im = Image.open(jpg).convert("RGB")
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)))
        im.save(webp, "WEBP", quality=82)
        print(f"  cover: {os.path.relpath(jpg, ROOT)} → cover.webp")
        return "placeholder" if False else "real"
    # プレースホルダ（記事ごとに色相を変えた文字なしグラデーション）
    w, h = 1200, 630
    import hashlib
    seed = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    base = [(18, 18, 26), (26, 18, 30)][seed % 2]
    acc = [(61, 214, 232), (224, 57, 155), (123, 77, 255), (61, 232, 160)][(seed // 2) % 4]
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        t = y / h
        for x in range(w):
            u = x / w
            k = (t * 0.75 + u * 0.25)
            px[x, y] = (
                int(base[0] + (acc[0] - base[0]) * k * 0.35),
                int(base[1] + (acc[1] - base[1]) * k * 0.35),
                int(base[2] + (acc[2] - base[2]) * k * 0.35),
            )
    im.save(webp, "WEBP", quality=82)
    print(f"  cover: cover.jpg 未着のためプレースホルダを生成 → cover.webp")
    return "placeholder"


# ---------- ビルド ----------

def build(md_path, force=False):
    text = open(md_path, encoding="utf-8").read()
    check_forbidden(text, md_path)
    fm, body_md = parse_frontmatter(text, md_path)

    slug, cat = fm["slug"], fm["category"]
    cat_name = CATEGORIES[cat]
    out_dir = os.path.join(ROOT, "gym-blog", cat, slug)
    out_file = os.path.join(out_dir, "index.html")
    if os.path.exists(out_file) and not force:
        fail(f"{os.path.relpath(out_file, ROOT)} は既に存在します。--force で上書きしてください")

    authors = json.load(open(AUTHORS, encoding="utf-8"))
    links = json.load(open(AFFILIATE, encoding="utf-8"))["links"]
    author = authors["authors"].get(fm["author"]) or fail(f"著者キー '{fm['author']}' が authors.json にありません")

    # 画像
    build_cover(slug, fm)
    cover_rel = f"../../../images/gym-blog/{slug}/cover.webp"
    og_image = f"{SITE}/images/gym-blog/{slug}/cover.webp"

    # 本文
    body_html, h2s = md_to_html(body_md)
    toc_items = "\n".join(
        f'      <li><a href="#{hid}">{esc(t)}</a></li>' for hid, t in h2s)

    # CTA（キー参照。URLが空なら出力しない）
    cta_block = ""
    cta_key = fm.get("cta", "")
    if cta_key:
        link = links.get(cta_key)
        if link is None:
            fail(f"CTAキー '{cta_key}' が affiliate-links.json にありません")
        if link.get("url"):
            cta_block = f"""
    <div class="gb-cta">
      <h3>{esc(fm.get('cta_heading', '無料カウンセリングのご案内'))}</h3>
      <p>{esc(fm.get('cta_text', ''))}<br>※無理な勧誘は一切ありません。</p>
      <a href="{esc(link['url'])}" target="_blank" rel="noopener sponsored" class="gb-cta-btn">{esc(link['label'])}</a>
    </div>"""

    # 関連リンク（固定3枠：カテゴリ一覧／NEXUS紹介／FAQ）
    related_cards = f"""        <a href="../" class="gb-related-card">
          <div class="cat">カテゴリ</div>
          <h3>{esc(cat_name)}の記事一覧</h3>
        </a>
        <a href="../../gym-comparison/nexus-personal-gym/" class="gb-related-card">
          <div class="cat">Gym Comparison</div>
          <h3>パーソナルジム「NEXUS」徹底紹介</h3>
        </a>
        <a href="../../../faq/" class="gb-related-card">
          <div class="cat">FAQ</div>
          <h3>よくある質問を見る</h3>
        </a>"""

    url = f"{SITE}/gym-blog/{cat}/{slug}/"
    jsonld_blogposting = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "headline": fm["title"],
        "description": fm["description"],
        "image": og_image,
        "datePublished": fm["date"],
        "dateModified": fm["date"],
        "inLanguage": "ja-JP",
        "articleSection": cat_name,
        "author": {
            "@type": "Person",
            "name": author["name"],
            "alternateName": author["name_en"],
            "jobTitle": author["title"],
            "url": author["url"],
            "image": f"{SITE}/{author['image']}",
            "worksFor": {"@type": "Organization", "name": author["organization"], "url": f"{SITE}/"},
        },
        "publisher": {
            "@type": "Organization",
            "name": author["organization"],
            "url": f"{SITE}/",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/images/熱狂画像.png"},
        },
    }, ensure_ascii=False, indent=2)

    jsonld_breadcrumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "パーソナルジムブログ", "item": f"{SITE}/gym-blog/"},
            {"@type": "ListItem", "position": 3, "name": cat_name, "item": f"{SITE}/gym-blog/{cat}/"},
            {"@type": "ListItem", "position": 4, "name": fm["title"], "item": url},
        ],
    }, ensure_ascii=False, indent=2)

    tpl = open(TEMPLATE, encoding="utf-8").read()
    html = render(tpl,
        title=esc(fm["title"]),
        description=esc(fm["description"]),
        url=url,
        og_image=og_image,
        date=fm["date"],
        date_dot=fm["date"].replace("-", "."),
        category_name=esc(cat_name),
        cover_src=cover_rel,
        cover_alt=esc(fm.get("cover_alt", fm["title"])),
        disclosure=esc(authors["disclosure"]),
        author_name=esc(author["name"]),
        author_name_en=esc(author["name_en"]),
        author_title=esc(author["title"]),
        author_bio=esc(author["bio"]),
        author_image=author["image"],
        supervisor=esc(fm.get("supervisor", author.get("supervisor", ""))),
        toc_items=toc_items,
        body=body_html,
        cta_block=cta_block,
        related_cards=related_cards,
        jsonld_blogposting=jsonld_blogposting,
        jsonld_breadcrumb=jsonld_breadcrumb,
    )

    os.makedirs(out_dir, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  built: {os.path.relpath(out_file, ROOT)}")
    return out_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md", nargs="?", help="content/articles/{slug}.md")
    ap.add_argument("--force", action="store_true", help="既存の生成先を上書き")
    ap.add_argument("--rebuild-all", action="store_true", help="content/articles/*.md を全部再ビルド（--force扱い）")
    args = ap.parse_args()

    if args.rebuild_all:
        for p in sorted(glob.glob(os.path.join(ROOT, "content", "articles", "*.md"))):
            print(os.path.basename(p))
            build(p, force=True)
    elif args.md:
        build(args.md, force=args.force)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
