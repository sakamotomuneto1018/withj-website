#!/usr/bin/env python3
"""Insert favicon <link> tags into <head> of all production HTML files.

- Skips .claude/ (worktrees) and nexus-sozai/ (raw assets).
- Removes any pre-existing favicon/apple-touch-icon <link> tags, then inserts
  the canonical block right after the opening <head> tag.
"""
import os
import re

ROOT = "/Users/pass0000/Desktop/HP"

BLOCK = (
    '<link rel="icon" href="/favicon.ico" sizes="any">\n'
    '<link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48">\n'
    '<link rel="icon" href="/favicon-192x192.png" type="image/png" sizes="192x192">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
)

# Matches any existing favicon-ish <link> line (rel=icon / shortcut icon / apple-touch-icon / mask-icon)
EXISTING = re.compile(
    r'[ \t]*<link[^>]*rel=["\']?(?:shortcut icon|icon|apple-touch-icon|mask-icon)["\']?[^>]*>\s*\n?',
    re.IGNORECASE,
)
HEAD_OPEN = re.compile(r'(<head\b[^>]*>)', re.IGNORECASE)


def process(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # remove existing favicon tags
    html = EXISTING.sub("", html)

    m = HEAD_OPEN.search(html)
    if not m:
        return "NO_HEAD"

    insert_at = m.end()
    # ensure a newline after <head> then our block
    new_html = html[:insert_at] + "\n" + BLOCK + html[insert_at:].lstrip("\n")
    # collapse any leading blank line duplication
    new_html = new_html.replace(m.group(1) + "\n\n", m.group(1) + "\n")

    if new_html == html:
        return "NOCHANGE"
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    return "OK"


def main():
    counts = {}
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # prune
        dirnames[:] = [d for d in dirnames if d not in (".claude", ".git", "nexus-sozai", "node_modules")]
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.join(dirpath, fn))
    for p in sorted(files):
        r = process(p)
        counts[r] = counts.get(r, 0) + 1
    print("files:", len(files))
    print("results:", counts)


if __name__ == "__main__":
    main()
