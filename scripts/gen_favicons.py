#!/usr/bin/env python3
"""Generate WITHJ favicon set (design 1: cyan W on dark rounded square)."""
from PIL import Image, ImageDraw

BG = (18, 16, 28, 255)      # near-black with slight purple
CYAN = (61, 214, 230, 255)  # bright cyan W

SS = 8  # supersample factor


def draw_icon(size, rounded=True):
    """Render icon at `size` px using supersampling for crisp anti-aliasing."""
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background
    if rounded:
        radius = int(S * 0.225)
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=radius, fill=BG)
    else:
        d.rectangle([0, 0, S - 1, S - 1], fill=BG)

    # Bold geometric "W" as a thick polyline (5 vertices, 4 strokes)
    def P(x, y):
        return (x / 100 * S, y / 100 * S)

    pts = [P(17, 30), P(35, 72), P(50, 47), P(65, 72), P(83, 30)]
    w = int(S * 0.135)  # stroke width
    d.line(pts, fill=CYAN, width=w, joint="curve")
    # round the stroke ends & vertices
    r = w // 2
    for (x, y) in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=CYAN)

    return img.resize((size, size), Image.LANCZOS)


def main():
    out = "/Users/pass0000/Desktop/HP"
    # PNG favicons (rounded, transparent corners)
    for s in (48, 96, 144, 192):
        draw_icon(s, rounded=True).save(f"{out}/favicon-{s}x{s}.png")
    # apple-touch-icon: full opaque square (iOS applies its own mask), 180px std
    draw_icon(180, rounded=False).save(f"{out}/apple-touch-icon.png")
    # .ico multi-size
    ico = draw_icon(64, rounded=True)
    ico.save(f"{out}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("generated favicons")


if __name__ == "__main__":
    main()
