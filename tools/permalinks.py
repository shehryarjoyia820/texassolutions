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
# Guides renamed to shorter, year-free slugs (Oct 2026). The old address keeps working as a redirect
# page (/guides/<old>/ and /blog/<old>.html), so links, bookmarks and search results still land.
RENAMED_GUIDES = {
    "best-truck-dispatch-service-for-owner-operators-2026": "best-truck-dispatch-service",
    "what-is-a-good-rate-per-mile-trucking-2026": "what-is-a-good-rate-per-mile",
    "hotshot-trucking-rates-per-mile-fuel-and-dispatch": "hotshot-trucking-rates",
    "freight-factoring-for-owner-operators-explained": "freight-factoring-explained",
    "broker-setup-rate-confirmation-spot-vs-contract": "broker-setup-spot-vs-contract",
    "hours-of-service-rules-explained-11-14-70-hour": "hours-of-service-rules",
    "what-is-deadhead-in-trucking-how-to-reduce-it": "what-is-deadhead-in-trucking",
    "how-to-get-mc-number-authority-owner-operator": "how-to-get-an-mc-number",
    "diesel-prices-by-state-cut-fuel-cost-per-mile": "cut-fuel-cost-per-mile",
    "how-to-choose-a-truck-dispatcher-avoid-scams": "how-to-choose-a-truck-dispatcher",
    "peak-season-trucking-loads-holiday-freight": "peak-season-trucking",
    "dry-van-vs-reefer-vs-flatbed-which-trailer": "dry-van-vs-reefer-vs-flatbed",
    "cheapest-truck-dispatch-service-real-cost": "cheapest-truck-dispatch-service",
    "reefer-loads-refrigerated-dispatch-guide": "reefer-loads-guide",
    "box-truck-dispatch-find-loads-and-costs": "box-truck-loads-and-costs",
    "ifta-for-owner-operators-how-to-file": "how-to-file-ifta",
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
    for old, new in RENAMED_GUIDES.items():
        m.setdefault(f"blog/{old}.html", f"/guides/{new}/")
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
    text = pat.sub(lambda mt: base + map_path("/" + mt.group(1), m), text)
    for old, new in RENAMED_GUIDES.items():
        text = text.replace(f"/guides/{old}/", f"/guides/{new}/")
    return text


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
    # Renamed guides: both old addresses become redirect pages to the new one.
    for old, new in RENAMED_GUIDES.items():
        for f in (root / "blog" / f"{old}.html", root / "guides" / old / "index.html"):
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(stub(base, f"/guides/{new}/"), encoding="utf-8", newline="\n")
    for pattern in ("sitemap*.xml", "feed.xml", "llms*.txt", "urls.txt", "robots.txt"):
        for f in root.glob(pattern):
            t = f.read_text(encoding="utf-8")
            n = rewrite_urls(t, m, base).replace(base + "/index.html", base + "/")
            if n != t:
                f.write_text(n, encoding="utf-8", newline="\n")
    return moved, m
