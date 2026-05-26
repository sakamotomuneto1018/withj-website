#!/usr/bin/env python3
"""
NEXUS店舗数 一括更新スクリプト
================================
使い方:
  python3 update-store-count.py

店舗数が変わったら以下の変数だけ書き換えて実行してください。
全ページの表記が自動的に統一されます。
"""

import os, sys

# ============================================================
# ★ ここだけ変更する ★
# ============================================================
STORE_NOW  = "約60店舗"          # 現在稼働中の店舗数
STORE_PLAN = "70店舗まで拡大予定" # 将来見込み（契約済み含む）
# ============================================================

STORE_FULL = f"{STORE_NOW}（{STORE_PLAN}）"
BASE = os.path.dirname(os.path.abspath(__file__))

AUTHOR_BIO_SHORT  = f"NEXUSパーソナルジム{STORE_FULL}のFC加盟開発を主導。30〜40代女性のジム継続パターンを現場で観察してきた経験から、パーソナルジムの「本当の選び方」を発信。"
AUTHOR_BIO_LONG_A = f"NEXUSパーソナルジム{STORE_FULL}のFC加盟開発を主導。何百人もの「続いた人」「続かなかった人」を現場で観察してきた経験から、30〜40代女性のジム継続パターンを発信しています。"
AUTHOR_BIO_LONG_B = f"NEXUSパーソナルジム{STORE_FULL}のFC加盟開発を主導。何百人もの「続いた人」「続かなかった人」を現場で観察してきた経験から、30〜40代女性のジム継続パターンを発信中。"

# 修正ルール: { ファイルパス: [(旧文字列, 新文字列), ...] }
# 注意: このリストは STORE_NOW/STORE_PLAN の値に関わらず常に最新になります。
# 旧パターンは「直前に実行されたときの値」を表すので、値を変えたら旧側も更新してください。

def make_rules(old_now, old_plan):
    """old_now/old_plan = 直前のスクリプト実行時の値"""
    old_full = f"{old_now}（{old_plan}）"
    old_bio_short  = f"NEXUSパーソナルジム{old_full}のFC加盟開発を主導。30〜40代女性のジム継続パターンを現場で観察してきた経験から、パーソナルジムの「本当の選び方」を発信。"
    old_bio_long_a = f"NEXUSパーソナルジム{old_full}のFC加盟開発を主導。何百人もの「続いた人」「続かなかった人」を現場で観察してきた経験から、30〜40代女性のジム継続パターンを発信しています。"
    old_bio_long_b = f"NEXUSパーソナルジム{old_full}のFC加盟開発を主導。何百人もの「続いた人」「続かなかった人」を現場で観察してきた経験から、30〜40代女性のジム継続パターンを発信中。"

    return {
        f"{BASE}/faq/index.html": [
            (old_bio_long_a, AUTHOR_BIO_LONG_A),
            (f"全国{old_full}で相互利用が可能。", f"全国{STORE_FULL}で相互利用が可能。"),
            (f"NEXUS Personal Gym {old_full}で実際によく聞かれた質問から100問を厳選。第1弾は25問。",
             f"NEXUS Personal Gym {STORE_FULL}で実際によく聞かれた質問から100問を厳選。第1弾は25問。"),
            (f"全国<strong>{old_full}で相互利用が可能</strong>。",
             f"全国<strong>{STORE_FULL}で相互利用が可能</strong>。"),
        ],
        f"{BASE}/gym-blog/keep-going/5-reasons-not-continuing/index.html": [
            (f"NEXUSパーソナルジム{old_full}を見てきた経験から、",
             f"NEXUSパーソナルジム{STORE_FULL}を見てきた経験から、"),
            (old_bio_long_b, AUTHOR_BIO_LONG_B),
            (old_bio_long_a, AUTHOR_BIO_LONG_A),
            (f"NEXUSパーソナルジム{old_full}のFC開拓を主導してきた立場で、",
             f"NEXUSパーソナルジム{STORE_FULL}のFC開拓を主導してきた立場で、"),
        ],
        f"{BASE}/gym-blog/diet-bodymake/30s-40s-diet-routine/index.html": [
            (old_bio_short, AUTHOR_BIO_SHORT),
            (old_bio_short.replace("発信。", "発信しています。"),
             AUTHOR_BIO_SHORT.replace("発信。", "発信しています。")),
            (f"NEXUSパーソナルジム{old_full}のFC加盟開発を主導してきました。",
             f"NEXUSパーソナルジム{STORE_FULL}のFC加盟開発を主導してきました。"),
        ],
        f"{BASE}/gym-blog/postpartum-mom/postpartum-diet-when-to-start/index.html": [
            (old_bio_short, AUTHOR_BIO_SHORT),
            (old_bio_short.replace("発信。", "発信しています。"),
             AUTHOR_BIO_SHORT.replace("発信。", "発信しています。")),
            (f"<strong>{old_full}</strong>のパーソナルジム運営に関わってきた私は、",
             f"<strong>{STORE_FULL}</strong>のパーソナルジム運営に関わってきた私は、"),
            (f"{old_full}の現場で見えてきた「成功パターン」",
             f"{STORE_FULL}の現場で見えてきた「成功パターン」"),
            (f"私たちが運営に関わる{old_full}のパーソナルジムで、",
             f"私たちが運営に関わる{STORE_FULL}のパーソナルジムで、"),
            (f"全国{old_full}で展開。", f"全国{STORE_FULL}で展開。"),
        ],
        f"{BASE}/nexus-members/index.html": [
            (f"全国{old_full}展開中。", f"全国{STORE_FULL}展開中。"),
            (f">{old_full}<", f">{STORE_FULL}<"),
        ],
        f"{BASE}/index.html": [
            (f"NEXUSパーソナルジム{old_full}の現場から、",
             f"NEXUSパーソナルジム{STORE_FULL}の現場から、"),
        ],
    }


def run(old_now, old_plan):
    rules = make_rules(old_now, old_plan)
    total = 0
    for filepath, replacements in rules.items():
        if not os.path.exists(filepath):
            print(f"  [skip] {filepath} not found")
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content
        for old, new in replacements:
            n = content.count(old)
            if n:
                content = content.replace(old, new)
                total += n
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fname = "/".join(filepath.replace(BASE + "/", "").split("/")[-2:])
            print(f"  ✓ {fname}")
    print(f"\n合計 {total} 箇所更新")
    print(f"表記: {STORE_FULL}")


if __name__ == "__main__":
    # ★ 次回変更時: 下の old_now/old_plan を「現在の値」に変えてから
    #   上の STORE_NOW/STORE_PLAN を「新しい値」に変えて実行する
    OLD_NOW  = "約60店舗"
    OLD_PLAN = "70店舗まで拡大予定"
    print(f"更新: {OLD_NOW}（{OLD_PLAN}） → {STORE_FULL}")
    run(OLD_NOW, OLD_PLAN)
