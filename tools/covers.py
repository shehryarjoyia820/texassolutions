"""
Featured-image generator for blog posts (1200x630 JPEG, brand styled).

    python tools/covers.py            # (re)build every post's cover
    from covers import make_cover     # used by site.py for posts without one

Each cover has a category glyph (truck, fuel drop, route, document, gauge),
a brand accent glow chosen from the post's tags, the Texas Solutions mark, the
category tag and the title. Output goes to assets/blog/<slug>.jpg.
"""

import hashlib
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "tools" / "fonts" / "Archivo-Variable.ttf"
ICON = ROOT / "assets" / "logo" / "texas-solutions-icon.png"
W, H = 1200, 630
INK = (20, 17, 15)
RED = (236, 48, 19)
ACCENTS = [(236, 48, 19), (255, 122, 26), (214, 40, 72), (240, 170, 30)]


def font(size, weight=800):
    try:
        f = ImageFont.truetype(str(FONT), size)
        f.set_variation_by_axes([weight, 100])
        return f
    except Exception:
        for name in ("arialbd.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf"):
            try:
                return ImageFont.truetype(name, size)
            except Exception:
                continue
        return ImageFont.load_default()


def glyph_for(tags, title):
    s = (" ".join(tags) + " " + title).lower()
    if any(k in s for k in ("fuel", "diesel", "mpg", "ifta")):
        return "drop"
    if any(k in s for k in ("rate", "cost", "pay", "profit", "factoring", "price", "fee", "money")):
        return "gauge"
    if any(k in s for k in ("mc ", "authority", "packet", "document", "hours of service", "rules", "compliance", "broker", "vs")):
        return "doc"
    if any(k in s for k in ("load board", "deadhead", "lane", "route", "detention")):
        return "route"
    return "truck"


def draw_glyph(d, kind, cx, cy, s, fill, cut=(0, 0, 0, 0)):
    if kind == "truck":
        d.rounded_rectangle([cx - 5 * s, cy - 3 * s, cx + 1.5 * s, cy + 2 * s], 10, fill=fill)
        d.polygon([(cx + 2 * s, cy - 1.6 * s), (cx + 4.2 * s, cy - 1.6 * s), (cx + 5.6 * s, cy + 0.2 * s), (cx + 5.6 * s, cy + 2 * s), (cx + 2 * s, cy + 2 * s)], fill=fill)
        for x in (cx - 3 * s, cx + 3.6 * s):
            d.ellipse([x - 0.9 * s, cy + 1.2 * s, x + 0.9 * s, cy + 3.1 * s], fill=fill)
    elif kind == "drop":
        d.ellipse([cx - 2.7 * s, cy - 0.2 * s, cx + 2.7 * s, cy + 5.2 * s], fill=fill)
        d.polygon([(cx, cy - 4.6 * s), (cx - 2.6 * s, cy + 1.6 * s), (cx + 2.6 * s, cy + 1.6 * s)], fill=fill)
    elif kind == "gauge":
        d.pieslice([cx - 5 * s, cy - 4 * s, cx + 5 * s, cy + 6 * s], 180, 360, fill=fill)
        d.pieslice([cx - 3.4 * s, cy - 2.4 * s, cx + 3.4 * s, cy + 4.4 * s], 180, 360, fill=cut)
        d.line([(cx, cy + 1 * s), (cx + 3 * s, cy - 2.2 * s)], fill=fill, width=int(0.5 * s))
        d.ellipse([cx - 0.6 * s, cy + 0.4 * s, cx + 0.6 * s, cy + 1.6 * s], fill=fill)
    elif kind == "doc":
        d.rounded_rectangle([cx - 3.4 * s, cy - 4.6 * s, cx + 3.4 * s, cy + 4.6 * s], 14, fill=fill)
        for i in range(4):
            d.rounded_rectangle([cx - 2.2 * s, cy - 2.8 * s + i * 1.6 * s, cx + (2.2 - (0.9 if i == 3 else 0)) * s, cy - 2.2 * s + i * 1.6 * s], 5, fill=cut)
    else:  # route
        d.line([(cx - 5 * s, cy + 3.4 * s), (cx - 2 * s, cy + 0.4 * s), (cx + 1.6 * s, cy + 2.6 * s), (cx + 5 * s, cy - 2.6 * s)], fill=fill, width=int(0.9 * s), joint="curve")
        d.ellipse([cx - 6 * s, cy + 2.4 * s, cx - 4 * s, cy + 4.4 * s], fill=fill)
        d.ellipse([cx + 4 * s, cy - 3.6 * s, cx + 6 * s, cy - 1.6 * s], fill=fill)


def wrap(draw, text, fnt, max_w, max_lines=4):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .,:;") + "..."
    return lines


def make_cover(slug, title, tags=(), out=None):
    seed = int(hashlib.sha1(slug.encode()).hexdigest(), 16)
    accent = ACCENTS[seed % len(ACCENTS)]
    kind = glyph_for(tags, title)
    # background: vertical gradient + accent glow
    img = Image.new("RGB", (W, H), INK)
    px = img.load()
    for y in range(H):
        t = y / H
        c = (int(20 + 14 * t), int(17 + 11 * t), int(15 + 9 * t))
        for x in range(W):
            px[x, y] = c
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gx, gy = (W - 130 - (seed % 120), 40 + (seed // 7) % 90)
    gd.ellipse([gx - 420, gy - 340, gx + 420, gy + 340], fill=tuple(int(c * 0.55) for c in accent))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = ImageChops.add(img, glow)

    d = ImageDraw.Draw(img, "RGBA")
    for i in range(-2, 9):  # road lines
        x0 = i * 190
        d.line([(x0, H), (x0 + 330, 0)], fill=(255, 255, 255, 12), width=2)

    # large glyph
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_glyph(ImageDraw.Draw(layer), kind, W - 250, H // 2 + 10, 42, accent + (255,))
    layer.putalpha(layer.split()[3].point(lambda v: int(v * 0.38)))
    img.paste(layer, (0, 0), layer)
    d.ellipse([W - 420, H // 2 - 170, W - 80, H // 2 + 190], outline=accent + (60,), width=3)

    # brand mark
    try:
        mark = Image.open(ICON).convert("RGBA")
        mh = 54
        mark = mark.resize((int(mark.width * mh / mark.height), mh))
        white = Image.new("RGBA", mark.size, (255, 255, 255, 255))
        white.putalpha(mark.split()[3])
        img.paste(white, (64, 54), white)
        d.text((64 + white.width + 16, 52), "TEXAS SOLUTIONS", font=font(22, 800), fill=(255, 255, 255, 255))
        d.text((64 + white.width + 16, 80), "TRUCK DISPATCH", font=font(18, 700), fill=accent + (255,))
    except Exception:
        d.text((64, 60), "TEXAS SOLUTIONS", font=font(24, 800), fill=(255, 255, 255, 255))

    # tag pill
    label = (tags[0] if tags else "Trucking").upper()
    tf = font(22, 800)
    tw = d.textlength(label, font=tf)
    d.rounded_rectangle([64, 170, 64 + tw + 40, 214], 22, fill=accent + (255,))
    d.text((84, 178), label, font=tf, fill=(255, 255, 255, 255))

    # title
    size = 64
    max_w = 700
    while True:
        tfnt = font(size, 800)
        lines = wrap(d, title, tfnt, max_w, 4)
        if len(lines) <= 3 or size <= 46:
            break
        size -= 4
    y = 244
    for ln in lines:
        d.text((64, y), ln, font=tfnt, fill=(255, 255, 255, 255))
        y += int(size * 1.14)

    # footer
    d.rectangle([0, H - 12, W, H], fill=accent + (255,))
    d.text((64, H - 62), "dispatch.texassolutions.co", font=font(24, 700), fill=(200, 194, 188, 255))

    out = Path(out) if out else ROOT / "assets" / "blog" / f"{slug}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return out


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    import re
    import yaml
    for f in sorted((ROOT / "content" / "blog").glob("*.md")):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", f.read_text(encoding="utf-8"), re.S)
        meta = yaml.safe_load(m.group(1)) if m else {}
        p = make_cover(f.stem, str(meta.get("title", f.stem)), meta.get("tags") or [])
        print("cover", p.name, p.stat().st_size // 1024, "KB")
