"""
SEO / structured-data audit for the generated site. Run after building:

    python tools/audit.py

Checks every generated .html page for: title and meta description length,
one H1, canonical URL, Open Graph image, JSON-LD validity (required fields per
type, absolute URLs, duplicate @id, FAQ answers visible on the page, speakable
selectors that exist), internal links, and sitemap coverage. Exits 1 on errors.
"""

import glob
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
BASE = "https://dispatch.texassolutions.co"

errors, warnings = [], []


def err(f, msg):
    errors.append(f"{f}: {msg}")


def warn(f, msg):
    warnings.append(f"{f}: {msg}")


def visible_text(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<template.*?</template>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).lower()


REQUIRED = {
    "Organization": ["name"], "LocalBusiness": ["name", "address", "telephone"], "ProfessionalService": ["name"],
    "WebSite": ["name", "url"], "WebPage": ["name", "url"], "CollectionPage": ["name", "url"], "AboutPage": ["name", "url"],
    "ContactPage": ["name", "url"], "FAQPage": ["mainEntity"], "BreadcrumbList": ["itemListElement"],
    "BlogPosting": ["headline", "image", "datePublished", "author", "publisher", "mainEntityOfPage"],
    "Article": ["headline", "image", "datePublished", "author", "publisher"],
    "Blog": ["name", "url"], "Service": ["name", "provider"], "HowTo": ["name", "step"], "Dataset": ["name", "description"],
    "ItemList": ["itemListElement"], "ImageObject": ["url"],
}


def flatten(data):
    """Yield every node in a JSON-LD document, following @graph."""
    if isinstance(data, list):
        for d in data:
            yield from flatten(d)
    elif isinstance(data, dict):
        if "@graph" in data:
            yield from flatten(data["@graph"])
        else:
            yield data


def types_of(n):
    t = n.get("@type")
    return t if isinstance(t, list) else [t]


def check_urls(f, node, path=""):
    for k, v in node.items():
        if k in ("url", "item", "@id", "mainEntityOfPage", "sameAs", "logo", "image", "contentUrl") and isinstance(v, str):
            if v.startswith("/") or (not v.startswith("http") and not v.startswith("#")):
                err(f, f"non-absolute URL in {k}: {v[:60]}")
        elif isinstance(v, dict):
            check_urls(f, v, path + k + ".")


pages = [p.replace(os.sep, "/") for p in glob.glob("*.html") + glob.glob("blog/*.html") + glob.glob("diesel-prices/*.html") if p != "head-codes.html"]
titles = {}
for f in sorted(pages):
    t = Path(f).read_text(encoding="utf-8")
    vt = visible_text(t)
    title = html.unescape(re.search(r"<title>(.*?)</title>", t, re.S).group(1)).strip()
    dm = re.search(r'<meta name="description" content="([^"]*)"', t)
    desc = html.unescape(dm.group(1)) if dm else ""
    if f != "404.html":
        if len(title) > 65:
            warn(f, f"title {len(title)} chars (aim <= 65): {title}")
        if len(desc) > 160:
            warn(f, f"description {len(desc)} chars (aim <= 160)")
        if len(desc) < 70:
            warn(f, f"description only {len(desc)} chars")
        titles.setdefault(title, []).append(f)
    if t.count("<h1") != 1:
        err(f, f"{t.count('<h1')} h1 tags")
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    if not canon and f != "404.html":
        err(f, "missing canonical")
    if f != "404.html" and not re.search(r'<meta property="og:image" content="https://', t):
        err(f, "missing absolute og:image")

    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    ids, all_nodes = {}, []
    for b in blocks:
        try:
            data = json.loads(b)
        except Exception as e:
            err(f, f"invalid JSON-LD: {e}")
            continue
        for n in flatten(data):
            all_nodes.append(n)
            if "@id" in n:
                ids.setdefault(n["@id"], []).append(n)
    for i, ns in ids.items():
        if len(ns) > 1 and len({json.dumps(x, sort_keys=True) for x in ns}) > 1:
            err(f, f"duplicate @id with different content: {i}")
    graph_ids = set(ids)
    for n in all_nodes:
        for ty in types_of(n):
            for req in REQUIRED.get(ty, []):
                if req not in n:
                    err(f, f"{ty} missing required '{req}'")
        check_urls(f, n)
        for ty in types_of(n):
            if ty == "Offer" or "offers" in n:
                err(f, "Offer present (percentage pricing is not a valid Offer price)")
            if ty in ("WebApplication", "SoftwareApplication"):
                err(f, f"{ty} needs aggregateRating/review (Search Console error); not used")
            if ty == "FAQPage":
                for q in n.get("mainEntity", []):
                    qn = html.unescape(q.get("name", "")).lower().strip()
                    if qn and qn not in vt:
                        err(f, f"FAQ question not visible on page: {qn[:70]}")
                    if not q.get("acceptedAnswer", {}).get("text"):
                        err(f, "FAQ answer missing text")
            if ty in ("BlogPosting", "Article") and len(n.get("headline", "")) > 110:
                warn(f, "headline over 110 chars")
            if ty == "Dataset" and len(n.get("description", "")) < 50:
                err(f, "Dataset description under 50 chars")
        sp = n.get("speakable")
        if sp:
            for sel in sp.get("cssSelector", []):
                if sel == "[data-speakable]" and "data-speakable" not in re.sub(r"<script.*?</script>", "", t, flags=re.S):
                    err(f, "speakable selector matches nothing")
        for ref_key in ("provider", "publisher", "isPartOf", "breadcrumb", "about", "author"):
            ref = n.get(ref_key)
            if isinstance(ref, dict) and set(ref) == {"@id"} and ref["@id"] not in graph_ids:
                err(f, f"{ref_key} references missing @id {ref['@id']}")
    if f != "404.html" and not any("BreadcrumbList" in types_of(n) for n in all_nodes) and f not in ("index.html", "head-codes.html"):
        warn(f, "no BreadcrumbList")

    for h in set(re.findall(r'href="/?([A-Za-z0-9_\-/]+\.html)(?:[?#"])', t)):
        if not os.path.exists(h):
            err(f, f"broken internal link: {h}")

for title, fs in titles.items():
    if len(fs) > 1:
        warn(",".join(fs[:3]), f"duplicate title: {title}")

# sitemaps
sm_files = ["sitemap.xml"] + sorted(glob.glob("sitemap-*.xml"))
locs = set()
for s in sm_files:
    if not os.path.exists(s):
        continue
    x = Path(s).read_text(encoding="utf-8")
    try:
        import xml.dom.minidom as md
        md.parseString(x.encode("utf-8"))
    except Exception as e:
        err(s, f"invalid XML: {e}")
    locs |= set(re.findall(r"<loc>([^<]+)</loc>", x))
for f in pages:
    if f in ("404.html",):
        continue
    u = BASE + "/" + ("" if f == "index.html" else f)
    if u not in locs:
        err("sitemap", f"{u} not in any sitemap")
for f in ("robots.txt", "llms.txt", "ads.txt", "feed.xml"):
    if not os.path.exists(f):
        err(f, "missing")

print(f"{len(pages)} pages audited")
for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
