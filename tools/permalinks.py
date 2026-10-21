"""
Clean, nested permalinks for the generated site.

site.py builds flat pages (box-truck-dispatch.html, blog/<slug>.html, ...). This runs last and
moves every page to a folder URL that shows where it belongs:

    /dispatch/box-truck/        /services/mc-lease/        /guides/<slug>/
    /calculators/<tool>/        /dispatch/states/<state>/  /diesel-prices/<state>/

Each page is written to <folder>/index.html, every link and absolute URL in the site
(pages, sitemaps, feed, llms.txt, urls.txt) is rewritten to the new address, and the old
.html file becomes a small redirect page (canonical + meta refresh + JS), so old links,
bookmarks and search results keep working. GitHub Pages cannot send real 301s.

Calculators live under /calculators/ because /tools/ is the build-scripts folder.
"""

import posixpath
import re
from pathlib import Path

# old file -> new folder URL; everything not listed falls back to the rules in build_map()
EXPLICIT = {
    "dispatch.html": "/dispatch/",
    "box-truck-dispatch.html": "/dispatch/box-truck/",
    "hotshot-dispatch.html": "/dispatch/hotshot/",
    "flatbed-dispatch.html": "/dispatch/flatbed-step-deck/",
    "dry-van-dispatch.html": "/dispatch/dry-van/",
    "reefer-dispatch.html": "/dispatch/reefer/",
    "power-only-dispatch.html": "/dispatch/power-only/",
    "semi-truck-dispatch.html": "/dispatch/semi-truck/",
    "owner-operator-dispatch.html": "/dispatch/owner-operators/",
    "small-fleet-dispatch.html": "/dispatch/small-fleets/",
    "dispatch-for-new-authority.html": "/dispatch/new-authority/",
    "truck-dispatch-by-state.html": "/dispatch/states/",
    "texas-truck-dispatch.html": "/dispatch/states/texas/",
    "trucking-business-services.html": "/services/",
    "mc-lease.html": "/services/mc-lease/",
    "trucking-back-office-services.html": "/services/back-office/",
    "trucking-authority-setup.html": "/services/mc-authority-setup/",
    "blog.html": "/guides/",
    "what-does-a-truck-dispatcher-do.html": "/guides/what-does-a-truck-dispatcher-do/",
    "tools.html": "/calculators/",
    "estimate.html": "/calculators/dispatch-fee-calculator/",
    "truck-fuel-cost-calculator.html": "/calculators/truck-fuel-cost-calculator/",
    "truck-dispatch-rates.html": "/rates/",
}
KEEP = {"index.html", "404.html", "head-codes.html"}
SKIP_PREFIX = ("http:", "https:", "//", "#", "mailto:", "tel:", "sms:", "data:", "javascript:")
ATTR = re.compile(r'\b(href|src|action|data-src|poster)="([^"]*)"')


def build_map(root, tool_slugs):
    m = dict(EXPLICIT)
    for slug in tool_slugs:
        m[f"{slug}.html"] = f"/calculators/{slug}/"
    for f in root.glob("*.html"):
        if f.name not in KEEP and f.name not in m and not is_stub(f):
            m[f.name] = f"/{f.stem}/"
    for f in root.glob("blog/*.html"):
        m[f"blog/{f.name}"] = f"/guides/{f.stem}/"
    for f in root.glob("truck-dispatch/*.html"):
        m[f"truck-dispatch/{f.name}"] = f"/dispatch/states/{f.stem}/"
    for f in root.glob("diesel-prices/*.html"):
        m[f"diesel-prices/{f.name}"] = f"/diesel-prices/{f.stem}/"
    return m


def is_stub(f):
    return 'http-equiv="refresh"' in f.read_text(encoding="utf-8", errors="ignore")[:600]


def map_path(abs_path, m):
    """'/box-truck-dispatch.html?x#y' -> '/dispatch/box-truck/?x#y' (unchanged if not a page we moved)."""
    q = re.search(r"[?#]", abs_path)
    path, tail = (abs_path[:q.start()], abs_path[q.start():]) if q else (abs_path, "")
    key = path.lstrip("/")
    if key == "index.html":
        return "/" + tail
    return m[key] + tail if key in m else abs_path


def rewrite_html(text, rel_dir, m, base):
    def attr(mt):
        name, v = mt.group(1), mt.group(2)
        if not v or v.startswith(SKIP_PREFIX):
            return mt.group(0)
        if not v.startswith("/"):
            q = re.search(r"[?#]", v)
            p, tail = (v[:q.start()], v[q.start():]) if q else (v, "")
            norm = posixpath.normpath(posixpath.join("/" + rel_dir, p)) if p else "/" + rel_dir
            if p.endswith("/") and not norm.endswith("/"):
                norm += "/"
            v = norm + tail
        return f'{name}="{map_path(v, m)}"'
    text = ATTR.sub(attr, text)
    return rewrite_urls(text, m, base)


def rewrite_urls(text, m, base):
    pat = re.compile(re.escape(base) + r"/([A-Za-z0-9_\-/]+\.html)")
    return pat.sub(lambda mt: base + map_path("/" + mt.group(1), m), text)


def stub(base, new):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title>'
            f'<link rel="canonical" href="{base}{new}"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={new}">'
            f'<script>location.replace("{new}"+location.search+location.hash)</script></head>'
            f'<body><p>This page has moved to <a href="{new}">{base}{new}</a>.</p></body></html>\n')


def apply(root, base, tool_slugs):
    root = Path(root)
    m = build_map(root, tool_slugs)
    moved = 0
    # pages that keep their place still need their links rewritten
    for name in ("index.html", "404.html"):
        f = root / name
        if f.exists():
            f.write_text(rewrite_html(f.read_text(encoding="utf-8"), "", m, base), encoding="utf-8", newline="\n")
    for old, new in sorted(m.items()):
        src = root / old
        if not src.exists() or is_stub(src):
            continue
        rel_dir = posixpath.dirname(old)
        html = rewrite_html(src.read_text(encoding="utf-8"), rel_dir, m, base)
        dest = root / new.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8", newline="\n")
        src.write_text(stub(base, new), encoding="utf-8", newline="\n")
        moved += 1
    for pattern in ("sitemap*.xml", "feed.xml", "llms*.txt", "urls.txt", "robots.txt"):
        for f in root.glob(pattern):
            t = f.read_text(encoding="utf-8")
            n = rewrite_urls(t, m, base).replace(base + "/index.html", base + "/")
            if n != t:
                f.write_text(n, encoding="utf-8", newline="\n")
    return moved, m
