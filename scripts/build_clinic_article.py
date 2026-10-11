#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_clinic_article.py — content/clinic/{slug}.md から /clinic/{slug}/index.html を生成する。

/gym-blog/ の build_article.py と同じ仕組み（md→HTML、禁止語チェック、cover.jpg→webp変換、
:::cta / :::compare 共通部品）。書き込むのは生成記事と変換画像のみ。

使い方:
  python3 scripts/build_clinic_article.py content/clinic/foo.md     # 1本ビルド
  python3 scripts/build_clinic_article.py --rebuild-all             # 全mdを再ビルド
  --force を付けない限り、既存の生成先 index.html は上書きしない。

frontmatter（gym-blogと同形式）:
  title / description / slug / category / date / author は必須。
  category は medical-diet / glp1 / aga / pill / ed のいずれか。
  noindex: true でそのページを noindex にできる（サンプル記事用）。
  cta: affiliate-links.json のキー。cta_heading / cta_text / cover_alt / related も同様。

掲載ルール（運用時の注意・テンプレに組み込み済みの項目以外）:
  - 他社の料金・コース・店舗数は公式サイトの公開情報のみ。「○年○月時点・公式サイトより」を必ず記載
  - 優劣の断定・体験談風の他社下げは書かない。事実を並べて読者に判断させる
  - 他社ロゴ・画像は使わない（社名はテキストのみ）。商標ワード狙いのページは作らない
  - 効果の断定・ビフォーアフター写真は使わない
"""
import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_article import (  # noqa: E402
    SITE, AUTHORS, AFFILIATE, FORBIDDEN, REQUIRED_KEYS,
    fail, render, esc, md_to_html, check_forbidden,
    extract_parts, inject_parts,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "scripts", "clinic_template.html")

CATEGORIES = {
    "medical-diet": "医療ダイエット",
    "glp1": "GLP-1",
    "aga": "AGA",
    "pill": "ピル",
    "ed": "ED",
}


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


def build_cover(slug):
    """images/clinic/{slug}/cover.jpg→cover.webp。無ければグラデーションプレースホルダ。"""
    from PIL import Image
    img_dir = os.path.join(ROOT, "images", "clinic", slug)
    os.makedirs(img_dir, exist_ok=True)
    jpg = os.path.join(img_dir, "cover.jpg")
    webp = os.path.join(img_dir, "cover.webp")
    if os.path.exists(jpg):
        im = Image.open(jpg).convert("RGB")
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)))
        im.save(webp, "WEBP", quality=82)
        print(f"  cover: {os.path.relpath(jpg, ROOT)} → cover.webp")
        return "real"
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


def build(md_path, force=False):
    text = open(md_path, encoding="utf-8").read()
    check_forbidden(text, md_path)
    fm, body_md = parse_frontmatter(text, md_path)

    slug, cat = fm["slug"], fm["category"]
    cat_name = CATEGORIES[cat]
    out_dir = os.path.join(ROOT, "clinic", slug)
    out_file = os.path.join(out_dir, "index.html")
    if os.path.exists(out_file) and not force:
        fail(f"{os.path.relpath(out_file, ROOT)} は既に存在します。--force で上書きしてください")

    authors = json.load(open(AUTHORS, encoding="utf-8"))
    links = json.load(open(AFFILIATE, encoding="utf-8"))["links"]
    author = authors["authors"].get(fm["author"]) or fail(f"著者キー '{fm['author']}' が authors.json にありません")

    # 画像
    build_cover(slug)
    cover_rel = f"../../images/clinic/{slug}/cover.webp"
    og_image = f"{SITE}/images/clinic/{slug}/cover.webp"

    # 本文（:::cta / :::compare 部品を先に退避）
    body_md, parts = extract_parts(body_md)
    body_html, h2s = md_to_html(body_md)
    body_html = inject_parts(body_html, parts)
    # 最初のH2直後に「この記事を書いた人」1行を挿入
    byline = (f'<p class="gb-byline" style="font-size:12.5px;color:var(--ink-faint,#888892);'
              f'margin:-10px 0 24px;">この記事を書いた人：'
              f'<a href="../../gym-blog/author/{fm["author"]}/" style="color:var(--accent1,#00f0ff);">'
              f'{esc(author["name"])}</a>（NEXUS加盟店オーナー・オンライン診療利用者）</p>')
    idx = body_html.find("</h2>")
    if idx != -1:
        p = idx + len("</h2>")
        body_html = body_html[:p] + "\n" + byline + body_html[p:]
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
      <h3>{esc(fm.get('cta_heading', '公式サイトのご案内'))}</h3>
      <p>{esc(fm.get('cta_text', ''))}</p>
      <a href="{esc(link['url'])}" target="_blank" rel="noopener sponsored" class="gb-cta-btn">{esc(link['label'])}</a>
    </div>"""

    url = f"{SITE}/clinic/{slug}/"
    jsonld_article = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
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
            "url": f"{SITE}/gym-blog/author/{fm['author']}/",
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
            {"@type": "ListItem", "position": 2, "name": "オンライン診療・医療ダイエット", "item": f"{SITE}/clinic/"},
            {"@type": "ListItem", "position": 3, "name": fm["title"], "item": url},
        ],
    }, ensure_ascii=False, indent=2)

    tpl = open(TEMPLATE, encoding="utf-8").read()
    html = render(tpl,
        title=esc(fm["title"]),
        description=esc(fm["description"]),
        url=url,
        og_image=og_image,
        robots="noindex, nofollow" if fm.get("noindex") == "true" else "index, follow",
        date=fm["date"],
        date_dot=fm["date"].replace("-", "."),
        category_name=esc(cat_name),
        cover_src=cover_rel,
        cover_alt=esc(fm.get("cover_alt", fm["title"])),
        author_key=fm["author"],
        author_name=esc(author["name"]),
        author_name_en=esc(author["name_en"]),
        author_title=esc(author["title"]),
        author_bio=esc(author.get("bio_clinic", author["bio"])),
        author_image=author["image"],
        toc_items=toc_items,
        body=body_html,
        cta_block=cta_block,
        jsonld_article=jsonld_article,
        jsonld_breadcrumb=jsonld_breadcrumb,
    )

    os.makedirs(out_dir, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  built: {os.path.relpath(out_file, ROOT)}")
    return out_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md", nargs="?", help="content/clinic/{slug}.md")
    ap.add_argument("--force", action="store_true", help="既存の生成先を上書き")
    ap.add_argument("--rebuild-all", action="store_true", help="content/clinic/*.md を全部再ビルド（--force扱い）")
    args = ap.parse_args()

    if args.rebuild_all:
        for p in sorted(glob.glob(os.path.join(ROOT, "content", "clinic", "*.md"))):
            print(os.path.basename(p))
            build(p, force=True)
    elif args.md:
        build(args.md, force=args.force)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
