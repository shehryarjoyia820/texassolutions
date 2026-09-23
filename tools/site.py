"""
Builds every page of dispatch.texassolutions.co from tools/content.py.

    python tools/site.py

Pages are written whole each run (no hand edits in the .html files survive),
so change words and numbers in tools/content.py, header codes in
head-codes.html, and legal text in tools/legal/*.html.
"""

import hashlib
import html
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import content as C  # noqa: E402

try:
    import covers  # noqa: E402
except Exception:  # Pillow missing: posts fall back to the default image
    covers = None

ROOT = Path(__file__).resolve().parent.parent
POSTS, STATE_PAGES = [], []
PAGE_HASH = {}
WEBSITE_ID = f"{C.BASE}/#website"
LOGO_ID = f"{C.BASE}/#logo"
TODAY = date.today().isoformat()
OG_IMAGE = f"{C.BASE}/assets/og-image.png"
LOGO = f"{C.BASE}/assets/logo/texas-solutions-logo.png"
BUSINESS_ID = f"{C.BASE}/#business"
INDEXNOW_KEY = "7c1f4e2a9b8d4c6e8f0a1b2c3d4e5f60"
esc = html.escape
S, M = C.PRICING["small"], C.PRICING["semi"]


def write(name, text):
    if name.endswith(".html"):
        PAGE_HASH[name] = hashlib.sha1(text.encode("utf-8")).hexdigest()
    (ROOT / name).write_text(text, encoding="utf-8", newline="\n")


def url(path):
    return C.BASE + ("/" if path in ("", "/") else path)


def money(n):
    return f"${n:,.0f}"


def pl(p):
    """'5%' or '8-10%' for a pricing group (or a (lo, hi) tuple)."""
    lo, hi = p["pct"] if isinstance(p, dict) else p
    return f"{lo}%" if lo == hi else f"{lo}-{hi}%"


SMALL_TXT = "box trucks and straight trucks 10%, hotshots 8%"
LANDING_PCT = {"box-truck-dispatch.html": (10, 10), "hotshot-dispatch.html": (8, 8)}


def landing_pricing(p):
    """Pricing group for a landing page, with the page's own truck percentage."""
    kind = dict(C.PRICING[p["kind"]])
    if p["file"] in LANDING_PCT:
        kind["pct"] = LANDING_PCT[p["file"]]
        kind["label"] = {"box-truck-dispatch.html": "Box trucks", "hotshot-dispatch.html": "Hotshots"}[p["file"]]
    return kind


def fee_range(kind):
    p = C.PRICING[kind]
    return money(p["gross"][0] * p["pct"][0] / 100), money(p["gross"][1] * p["pct"][1] / 100)


WA_URL = "https://wa.me/" + C.WHATSAPP + "?text=" + C.WHATSAPP_TEXT.replace(" ", "%20").replace(",", "%2C").replace("'", "%27")
SEMI_FEE, SMALL_FEE = fee_range("semi"), fee_range("small")

# ------------------------------------------------------------------ icons
ICONS = {
    "wa": '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16.04 3C8.86 3 3.03 8.82 3.03 16c0 2.3.6 4.53 1.74 6.5L3 29l6.68-1.75A12.95 12.95 0 0 0 16.04 29C23.2 29 29 23.18 29 16S23.2 3 16.04 3zm0 23.66c-2 0-3.95-.54-5.65-1.55l-.4-.24-3.97 1.04 1.06-3.86-.26-.4a10.6 10.6 0 0 1-1.63-5.65c0-5.87 4.78-10.65 10.66-10.65 5.87 0 10.63 4.78 10.63 10.65 0 5.88-4.77 10.66-10.44 10.66zm5.84-7.97c-.32-.16-1.9-.94-2.19-1.04-.3-.11-.5-.16-.72.16-.21.32-.83 1.04-1.01 1.25-.19.21-.37.24-.69.08-.32-.16-1.35-.5-2.57-1.59-.95-.85-1.59-1.9-1.78-2.22-.19-.32-.02-.49.14-.65.14-.14.32-.37.48-.56.16-.18.21-.32.32-.53.1-.21.05-.4-.03-.56-.08-.16-.72-1.73-.98-2.37-.26-.62-.52-.54-.72-.55h-.61c-.21 0-.56.08-.85.4-.29.32-1.12 1.1-1.12 2.67 0 1.57 1.15 3.1 1.31 3.3.16.22 2.26 3.45 5.47 4.84.77.33 1.36.53 1.83.67.77.25 1.47.21 2.02.13.62-.09 1.9-.78 2.17-1.53.27-.75.27-1.39.19-1.52-.08-.14-.29-.22-.61-.38z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "calc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h4"/></svg>',
    "cash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 12h.01M18 12h.01"/></svg>',
    "route": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.1V12a10 10 0 1 1-5.9-9.1"/><path d="M22 4 12 14l-3-3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
}
FEATURE_ICONS = ["cash", "route", "doc", "check", "calc", "clock"]


# ------------------------------------------------------------------ schema
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def pricing_props():
    return [
        {"@type": "PropertyValue", "name": "Semi truck dispatch fee", "value": "5% of weekly gross (OTR)"},
        {"@type": "PropertyValue", "name": "Hotshot dispatch fee", "value": "8% of weekly gross (OTR)"},
        {"@type": "PropertyValue", "name": "Box truck and straight truck dispatch fee", "value": "10% of weekly gross (OTR)"},
        {"@type": "PropertyValue", "name": "Flat rate, setup fee or subscription", "value": "None"},
    ]


def business():
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": BUSINESS_ID,
        "name": C.NAME,
        "alternateName": C.BRAND,
        "slogan": "Truck dispatch for owner-operators and small fleets",
        "description": f"Truck dispatch service for owner-operators and small fleets in the United States. Semi trucks pay "
                       f"{pl(M)} of weekly gross, hotshots 8% and box trucks 10%, for OTR operations, "
                       "with no flat rate and no setup fee.",
        "url": url("/"),
        "logo": {"@type": "ImageObject", "@id": LOGO_ID, "url": LOGO, "contentUrl": LOGO, "width": 1364, "height": 471},
        "image": [OG_IMAGE],
        "telephone": C.PHONE_E164,
        "email": C.EMAIL,
        "priceRange": "5-10% of weekly gross",
        "address": {"@type": "PostalAddress", "streetAddress": C.STREET, "addressLocality": C.CITY,
                    "addressRegion": C.REGION, "postalCode": C.POSTAL, "addressCountry": C.COUNTRY},
        "geo": {"@type": "GeoCoordinates", "latitude": 31.9973, "longitude": -102.0779},
        "areaServed": {"@type": "Country", "name": "United States"},
        "founder": {"@type": "Person", "name": "Shehryar Joyia", "jobTitle": "Owner and CEO"},
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": C.PHONE_E164, "contactType": "sales", "areaServed": "US", "availableLanguage": "English"},
            {"@type": "ContactPoint", "url": f"https://wa.me/{C.WHATSAPP}", "contactType": "customer support", "areaServed": "US", "availableLanguage": "English"},
        ],
        "sameAs": [C.MAIN_SITE + "/"],
        "knowsAbout": ["Truck dispatch", "Freight dispatch", "OTR dispatch", "Load boards", "Rate negotiation",
                       "Broker setup packets", "Owner-operator trucking"] + [f"{e} dispatch" for e in C.EQUIPMENT],
        "additionalProperty": pricing_props(),
    }


def website():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": WEBSITE_ID, "name": C.BRAND, "url": url("/"),
            "inLanguage": "en-US", "publisher": {"@id": BUSINESS_ID}}


def service(name, description, path, stype):
    return {
        "@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": stype,
        "description": description, "url": url(path), "provider": {"@id": BUSINESS_ID},
        "areaServed": {"@type": "Country", "name": "United States"},
        "audience": {"@type": "BusinessAudience", "audienceType": "Owner-operators and small trucking fleets"},
    }


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def crumbs_ld(trail):
    items = [("Home", "/")] + trail
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}


def speakable(path, name):
    return {"@context": "https://schema.org", "@type": "WebPage", "name": name, "url": url(path),
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["[data-speakable]"]}}


def howto():
    return {"@context": "https://schema.org", "@type": "HowTo", "name": "How to start truck dispatch with Texas Solutions",
            "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d} for i, (t, d) in enumerate(C.STEPS)]}


# ------------------------------------------------------------------ head codes
HEAD_CODES_MARKER = "<!-- ======= PASTE BELOW THIS LINE ======= -->"


def head_codes():
    p = ROOT / "head-codes.html"
    if not p.exists():
        return ""
    raw = p.read_text(encoding="utf-8")
    return raw.split(HEAD_CODES_MARKER, 1)[1].strip() if HEAD_CODES_MARKER in raw else ""


# ------------------------------------------------------------------ chrome
def nav_links():
    return [("Rates", "truck-dispatch-rates.html"), ("Blog", "blog.html"), ("About", "about.html"),
            ("Contact", "contact.html")]


def tools_nav_items():
    """(name, file) for every calculator, dispatch fee and fuel cost first."""
    items = [("Dispatch Fee Calculator", "estimate.html"), ("Truck Fuel Cost Calculator", "truck-fuel-cost-calculator.html")]
    items += [(t["hub_title"], t["slug"] + ".html") for t in TOOLS]
    return items


def header(current):
    svc = "\n".join(f'          <a href="{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING)
    links = "\n".join(f'      <a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for t, h in nav_links())
    mlinks = "\n".join(f'    <a href="{h}">{t}</a>' for t, h in nav_links())
    msvc = "\n".join(f'      <a href="{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING)
    tnav = tools_nav_items()
    tools_dd = "\n".join(f'          <a href="{f}">{esc(n)}</a>' for n, f in tnav)
    mtools = "\n".join(f'      <a href="{f}">{esc(n)}</a>' for n, f in tnav)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap tb-right">
  <div class="tb-left"><a href="tel:{C.PHONE_E164}">{C.PHONE}</a><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></div>
</div></div>
<header class="header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="{esc(C.BRAND)} home">
      <img src="assets/logo/texas-solutions-icon.png" alt="" width="33" height="40">
      <span>Texas Solutions<small>Truck Dispatch</small></span>
    </a>
    <nav class="nav" aria-label="Main">
      <div class="dd">
        <button type="button" aria-expanded="false">Dispatch Services &#9662;</button>
        <div class="dd-menu">
{svc}
        </div>
      </div>
      <div class="dd">
        <button type="button" aria-expanded="false">Tools &#9662;</button>
        <div class="dd-menu wide">
{tools_dd}
        </div>
      </div>
{links}
    </nav>
    <div class="nav-cta">
      <a class="btn btn-line" href="tel:{C.PHONE_E164}">{ICONS['phone']}Call</a>
      <a class="btn btn-red" href="estimate.html">Get an Estimate</a>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Mobile">
    <a href="index.html">Home</a>
{mlinks}
    <span class="mnav-label">Dispatch Services</span>
    <div class="mnav-sub">
{msvc}
    </div>
    <span class="mnav-label">Free Tools</span>
    <div class="mnav-sub">
{mtools}
    </div>
    <a class="btn btn-red" href="estimate.html">Get a Free Estimate</a>
    <a class="btn btn-wa" href="{WA_URL}" target="_blank" rel="noopener">{ICONS['wa']}WhatsApp a Dispatcher</a>
</nav>"""


def footer():
    svc = "\n".join(f'      <a href="{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING)
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="cols">
      <div class="fbrand">
        <img src="assets/logo/texas-solutions-logo.png" alt="Texas Solutions" width="127" height="44" loading="lazy">
        <p>Truck dispatch service for owner-operators and small fleets across the United States. Semi trucks {pl(M)}, hotshots 8% and box trucks 10% of weekly gross, OTR. No flat rate.</p>
      </div>
      <div>
        <h4>Dispatch Services</h4>
{svc}
      </div>
      <div>
        <h4>Company</h4>
      <a href="truck-dispatch-rates.html">Dispatch Rates</a>
      <a href="estimate.html">Free Estimate</a>
      <a href="tools.html">All Free Tools</a>
      <a href="truck-fuel-cost-calculator.html">Fuel Cost Calculator</a>
      <a href="diesel-prices/texas.html">Diesel Prices by State</a>
      <a href="blog.html">Blog</a>
      <a href="about.html">About Us</a>
      <a href="faq.html">FAQ</a>
      <a href="contact.html">Contact</a>
      <a href="privacy.html">Privacy Policy</a>
      <a href="terms.html">Terms &amp; Conditions</a>
      <a href="{C.MAIN_SITE}/" rel="noopener">Texas Solutions Software</a>
      </div>
      <div>
        <h4>Contact</h4>
      <a href="tel:{C.PHONE_E164}">{C.PHONE}</a>
      <a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp +1 838 910 3147</a>
      <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>
      <p style="margin-top:8px">{C.STREET}<br>{C.CITY}, {C.REGION} {C.POSTAL}</p>
      <p style="margin-top:8px">{C.HOURS}</p>
      </div>
    </div>
    <p class="legal">&copy; <span id="year">2026</span> Texas Solutions. All rights reserved. {C.LEGAL_FOOTER}</p>
  </div>
</footer>
<a class="wa-float" href="{WA_URL}" target="_blank" rel="noopener" aria-label="Chat with a Texas Solutions dispatcher on WhatsApp">
  <span class="wa-tip">Chat on WhatsApp<small>+1 (838) 910-3147</small></span>
  <span class="wa-btn">{ICONS['wa']}</span>
</a>
<script src="js/site.js" defer></script>
<script src="js/calc-tools.js" defer></script>"""


def graph_script(path, title, description, schemas, body, img, img_alt, page_type, published, modified):
    """One @graph per page: business, website, the page itself, image, breadcrumbs, FAQ and any extras."""
    page_url = url(path)
    wp_id = page_url + "#webpage"

    def strip(n):
        n = dict(n)
        n.pop("@context", None)
        return n

    wp = {"@type": page_type, "@id": wp_id, "url": page_url, "name": title, "description": description,
          "isPartOf": {"@id": WEBSITE_ID}, "inLanguage": "en-US",
          "primaryImageOfPage": {"@id": page_url + "#primaryimage"}}
    wp["about"] = {"@id": BUSINESS_ID}
    if published:
        wp["datePublished"] = published
    if modified:
        wp["dateModified"] = modified
    extra = []
    for s in schemas:
        n = strip(s)
        ty = n.get("@type")
        if ty == "BreadcrumbList":
            n["@id"] = page_url + "#breadcrumb"
            wp["breadcrumb"] = {"@id": n["@id"]}
            extra.append(n)
        elif ty == "WebPage" and "speakable" in n:
            if "data-speakable" in body:
                wp["speakable"] = n["speakable"]
        elif ty in ("ContactPage", "AboutPage", "CollectionPage"):
            wp["@type"] = ty
        elif ty == "FAQPage":
            n["@id"] = page_url + "#faq"
            n["isPartOf"] = {"@id": wp_id}
            extra.append(n)
        elif ty in ("BlogPosting", "Article"):
            n["@id"] = page_url + "#article"
            n["isPartOf"] = {"@id": wp_id}
            wp["mainEntity"] = {"@id": n["@id"]}
            wp.pop("about", None)
            extra.append(n)
        else:
            extra.append(n)
    image_node = {"@type": "ImageObject", "@id": page_url + "#primaryimage", "url": img, "contentUrl": img,
                  "width": 1200, "height": 630, "caption": img_alt or title, "inLanguage": "en-US"}
    graph = [strip(business()), strip(website()), wp, image_node] + extra
    return ld({"@context": "https://schema.org", "@graph": graph})


def page(path, title, description, keywords, schemas, body, current=None, og_type="website", preload_video=False,
         image=None, image_alt="", published=None, modified=None, tags=(), page_type="WebPage"):
    ov = C.SEO.get(path)
    if ov:
        title, description = ov
    img = image or OG_IMAGE
    alt = image_alt or "Texas Solutions Truck Dispatch: dispatch for owner-operators and small fleets"
    art_meta = ""
    if og_type == "article":
        art_meta = "\n".join(filter(None, [
            f'<meta property="article:published_time" content="{published}">' if published else "",
            f'<meta property="article:modified_time" content="{modified or published}">' if (modified or published) else "",
            f'<meta property="article:author" content="Texas Solutions">',
            f'<meta property="article:section" content="{esc(tags[0])}">' if tags else "",
            *[f'<meta property="article:tag" content="{esc(x)}">' for x in tags],
        ]))
    codes = head_codes() or "<!-- no header codes yet: paste them into head-codes.html -->"
    lds = graph_script(path, title, description, schemas, body, img, alt, page_type, published, modified)
    return f"""<!DOCTYPE html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="keywords" content="{esc(keywords)}">
<link rel="canonical" href="{url(path)}">
<link rel="alternate" hreflang="en-us" href="{url(path)}">
<link rel="alternate" hreflang="x-default" href="{url(path)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="bingbot" content="index, follow">
<meta name="author" content="Texas Solutions">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Midland, Texas">
<meta name="theme-color" content="#14110f">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(C.BRAND)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(alt)}">
{art_meta}
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{img}">
<meta name="twitter:image:alt" content="{esc(alt)}">
<link rel="icon" type="image/png" href="assets/logo/favicon.png">
<link rel="apple-touch-icon" href="assets/logo/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="css/site.css">
<link rel="alternate" type="text/plain" href="{C.BASE}/llms.txt" title="LLM summary">
<link rel="alternate" type="application/rss+xml" title="{esc(C.BRAND)} Blog" href="{C.BASE}/feed.xml">
<script>document.documentElement.classList.remove('no-js')</script>
{lds}
<!-- HEAD-CODES:START -->
{codes}
<!-- HEAD-CODES:END -->
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""


# ------------------------------------------------------------------ blocks
def answer(q, a, label="Quick answer"):
    return f"""<div class="answer rv" data-speakable>
  <span class="label">{label}</span>
  <h2>{esc(q)}</h2>
  <p>{esc(a)}</p>
</div>"""


def faq_html(items):
    return '<div class="faq">\n' + "\n".join(
        f'  <details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in items) + "\n</div>"


def phero(crumb_name, h1, lede, ctas=True, extra=""):
    cta = f"""<div class="ctas"><a class="btn btn-red" href="estimate.html">Get a Free Estimate</a><a class="btn btn-wa" href="{WA_URL}" target="_blank" rel="noopener">{ICONS['wa']}WhatsApp Us</a></div>""" if ctas else ""
    return f"""<section class="phero"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a> / {esc(crumb_name)}</div>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
  {cta}{extra}
</div></section>"""


PRICE_GROUPS = [
    # key, label, equipment, pct, gross, truck query, featured
    ("semi", "Semi trucks", ["Dry Van", "Reefer", "Flatbed", "Step Deck", "Power Only"], 5, (8000, 10000), "dry-van", True),
    ("hotshot", "Hotshot", ["Hotshot trucks", "Gooseneck and flatbed trailers"], 8, (7000, 9000), "hotshot", False),
    ("box", "Box trucks", ["Box Truck", "Straight Truck"], 10, (7000, 9000), "box-truck", False),
]


def pricing_cards(cta=True):
    def card(key, label, eq, pct, gross, tq, feat):
        lo, hi = money(gross[0] * pct / 100), money(gross[1] * pct / 100)
        items = [f"Typical weekly gross {money(gross[0])} - {money(gross[1])}",
                 f"About {lo} - {hi} per week on typical gross",
                 "OTR (over-the-road) operations", "No flat rate, no setup fee, no subscription",
                 "You approve every load"]
        li = "\n".join(f"      <li>{esc(i)}</li>" for i in items)
        btn = f'<a class="btn {"btn-red" if feat else "btn-dark"}" href="estimate.html?truck={tq}">Estimate my fee</a>' if cta else ""
        tag = '<span class="tag">Most popular</span>' if feat else ""
        return f"""<div class="price{' feat' if feat else ''} rv">
    {tag}<h3>{label}</h3>
    <p class="eq">{', '.join(eq)}</p>
    <div class="amt">{pct}%<small> of weekly gross</small></div>
    <ul>
{li}
    </ul>
    {btn}
  </div>"""
    cards = "\n  ".join(card(*g) for g in PRICE_GROUPS)
    return f"""<div class="grid g3 price-grid">
  {cards}
</div>
<p class="note center">{esc(C.PRICING_CONDITION)} {esc(C.PRICING_NOTE)}</p>"""


def rate_board():
    rows = "\n".join(
        f'      <tr><td>{o} &rarr; {d}</td><td><span class="eq-badge">{e}</span></td><td class="hide-sm">{mi:,} mi</td><td class="rate">{r}/mi</td></tr>'
        for o, d, e, mi, r in C.LANES)
    guide = "\n".join(
        f'    <div class="rg{" hi" if eq in ("Flatbed", "Step Deck", "Reefer") else ""}"><b>{eq}</b><span class="v">{rate}/mi</span><small>{note}</small></div>'
        for eq, rate, note in C.RATE_GUIDE)
    return f"""<div class="grid board-grid" id="board">
  <div class="board rv">
    <div class="board-head"><b><span class="dot"></span>Lane Rate Board</b><span>Rough estimate &middot; <span id="boardTime">today</span></span></div>
    <div style="overflow-x:auto"><table class="board-table">
      <thead><tr><th>Lane</th><th>Equipment</th><th class="hide-sm">Miles</th><th>Rate</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table></div>
    <p class="board-foot">Illustrative sample lanes shown for demonstration. Texas Solutions does not guarantee any specific load volume, rate, revenue, or earnings.</p>
  </div>
  <div class="rv">
    <h3 style="margin-bottom:14px">Rough rate per mile by equipment</h3>
    <div class="rate-guide">
{guide}
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:12px">Rough estimates. Flatbed and step deck loads often pay $5-7 a mile, reefer $4-6, hotshot $4-5, dry van and power only $3-5, and box trucks $1.80-3.20, depending on lane, season and local or OTR. Actual rates depend on lane, season and market.</p>
  </div>
</div>"""


def equip_cards():
    icons = "truck"
    return '<div class="grid g3">\n' + "\n".join(
        f"""  <a class="card rv" href="{p['file']}"><div class="icon">{ICONS[icons]}</div><h3>{esc(p['nav'])}</h3><p>{esc(p['description'][:150].rsplit(' ', 1)[0])}...</p><span class="more">{pl(landing_pricing(p))} &middot; Learn more &rarr;</span></a>"""
        for p in C.LANDING if not p.get("guide")) + "\n</div>"


def features():
    return '<div class="grid g3">\n' + "\n".join(
        f'  <div class="card rv"><div class="icon">{ICONS[FEATURE_ICONS[i]]}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, (t, d) in enumerate(C.FEATURES)) + "\n</div>"


def steps(dark=False):
    return '<div class="grid g4 steps">\n' + "\n".join(
        f'  <div class="step rv"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in C.STEPS) + "\n</div>"


def band(title="Ready to keep your truck loaded?", text=None):
    text = text or f"Semi trucks {pl(M)}, hotshots 8%, box trucks 10% of weekly gross. OTR. No flat rate, no setup fee."
    return f"""<section class="sec"><div class="wrap"><div class="band rv">
  <div><h2>{esc(title)}</h2><p>{esc(text)}</p></div>
  <div class="ctas"><a class="btn btn-dark" href="estimate.html">Get a Free Estimate</a><a class="btn btn-wa" href="{WA_URL}" target="_blank" rel="noopener">{ICONS['wa']}WhatsApp</a></div>
</div></div></section>"""


def equip_options(selected=""):
    return "\n".join(f'<option{" selected" if e == selected else ""}>{e}</option>' for e in C.EQUIPMENT)


def lead_form(fid, subject, button, quote=False):
    """Written fields only. No file uploads."""
    extra = '<input type="hidden" name="estimate_summary" value="">' if quote else ""
    return f"""<form class="form rv" id="{fid}" data-web3 data-subject="{esc(subject)}" novalidate>
  <div class="grid g2">
    <div><label class="fl" for="{fid}-name">Full name <i>*</i></label><input type="text" id="{fid}-name" name="name" autocomplete="name" required></div>
    <div><label class="fl" for="{fid}-phone">Phone <i>*</i></label><input type="tel" id="{fid}-phone" name="phone" autocomplete="tel" required></div>
    <div><label class="fl" for="{fid}-email">Email <i>*</i></label><input type="email" id="{fid}-email" name="email" autocomplete="email" required></div>
    <div><label class="fl" for="{fid}-company">Company name</label><input type="text" id="{fid}-company" name="company" autocomplete="organization"></div>
    <div><label class="fl" for="{fid}-mc">MC number</label><input type="text" id="{fid}-mc" name="mc_number" inputmode="numeric"></div>
    <div><label class="fl" for="{fid}-dot">DOT number</label><input type="text" id="{fid}-dot" name="dot_number" inputmode="numeric"></div>
    <div><label class="fl" for="{'qEquip' if quote else fid + '-eq'}">Equipment <i>*</i></label><select id="{'qEquip' if quote else fid + '-eq'}" name="equipment" required><option value="">Select equipment</option>{equip_options()}</select></div>
    <div><label class="fl" for="{'qTrucks' if quote else fid + '-trucks'}">Number of trucks</label><input type="number" id="{'qTrucks' if quote else fid + '-trucks'}" name="trucks" min="1" max="500" value="1"></div>
    <div class="full"><label class="fl" for="{fid}-lanes">Home base and preferred lanes</label><input type="text" id="{fid}-lanes" name="lanes" placeholder="e.g. Midland, TX. OTR to the Southeast, home every 2 weeks"></div>
    <div class="full"><label class="fl" for="{fid}-msg">Message</label><textarea id="{fid}-msg" name="message" placeholder="Tell us about your truck, authority age, and what you need from a dispatcher."></textarea></div>
    <div class="full"><label class="consent"><input type="checkbox" name="sms_consent" value="yes"><span>{C.SMS_CONSENT}</span></label></div>
  </div>
  {extra}
  <label class="hp" aria-hidden="true">Leave empty <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label>
  <button class="btn btn-red" type="submit">{esc(button)}</button>
  <p class="form-status" role="status" aria-live="polite"></p>
  <p class="fine">{esc(C.FORM_DISCLAIMER)}</p>
</form>"""


def contact_side():
    return f"""<div class="cside">
  <a class="cbox wa" href="{WA_URL}" target="_blank" rel="noopener"><span class="icon">{ICONS['wa'].replace('viewBox', 'fill="currentColor" viewBox')}</span><span><b>WhatsApp</b><span>+1 (838) 910-3147 &middot; fastest reply</span></span></a>
  <a class="cbox" href="tel:{C.PHONE_E164}"><span class="icon">{ICONS['phone']}</span><span><b>Call a dispatcher</b><span>{C.PHONE}</span></span></a>
  <a class="cbox" href="mailto:{C.EMAIL}"><span class="icon">{ICONS['mail']}</span><span><b>Email</b><span>{C.EMAIL}</span></span></a>
  <div class="cbox"><span class="icon">{ICONS['pin']}</span><span><b>Office</b><span>{C.STREET}, {C.CITY}, {C.REGION} {C.POSTAL}</span></span></div>
</div>"""


# ------------------------------------------------------------------ pages
HOME_KW = ", ".join(C.CORE_KEYWORDS)


def blog_teaser():
    if not POSTS:
        return ""
    cards = "\n".join(post_card(po) for po in POSTS[:3])
    return f"""<section class="sec"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">From the blog</span><h2>Guides for owner-operators</h2></div>
  <div class="grid g3">
{cards}
  </div>
  <p class="mt-l"><a class="btn btn-line" href="blog.html">All articles</a></p>
</div></section>"""


def build_home():
    title = "Truck Dispatch Service for Owner-Operators | 5% Semi, 8% Hotshot, 10% Box Truck | Texas Solutions"
    desc = (f"Truck dispatch service for owner-operators and small fleets. Semi trucks {pl(M)} and box trucks & hotshots "
            f"10% of weekly gross (hotshots 8%), OTR. No flat rate, no setup fee. Flatbed loads $5-7/mile. Free estimate.")
    qa = ("How much does truck dispatch cost at Texas Solutions?",
          f"Texas Solutions charges {pl(M)} of weekly gross for OTR semi trucks (dry van, reefer, flatbed, step deck, power only) "
          f"8% for OTR hotshots and 10% for OTR box trucks and straight trucks. There is no flat rate, no setup fee and no "
          f"monthly subscription. On a typical semi grossing {money(M['gross'][0])}-{money(M['gross'][1])} a week, the fee is about {SEMI_FEE[0]}-{SEMI_FEE[1]} a week.")
    hero = f"""<section class="hero">
  <video autoplay muted loop playsinline preload="metadata" aria-hidden="true"><source src="assets/video/hero-background.mp4" type="video/mp4"></video>
  <div class="wrap">
    <div>
      <span class="eyebrow"><span class="dot"></span>Truck dispatch for owner-operators &amp; small fleets</span>
      <h1>Truck Dispatch Service that keeps your <em>truck loaded.</em></h1>
      <p class="lede">We find, negotiate and book high-paying freight for owner-operators and small fleets across the USA. Dry van, reefer, flatbed, step deck, power only, hotshot and box truck. You approve every load.</p>
      <div class="ctas">
        <a class="btn btn-red" href="estimate.html">{ICONS['calc']}Get a Free Estimate</a>
        <a class="btn btn-wa" href="{WA_URL}" target="_blank" rel="noopener">{ICONS['wa']}WhatsApp a Dispatcher</a>
      </div>
      <div class="hero-stats">
        <div><b>{pl(M)}</b><span>Semi trucks, OTR</span></div>
        <div><b>8-10%</b><span>Hotshot 8%, box truck 10%</span></div>
        <div><b>$0</b><span>Setup fee or flat rate</span></div>
      </div>
    </div>
    <aside class="hero-card" aria-label="Dispatch pricing">
      <h2>Simple percentage pricing</h2>
      <div class="row"><div><b>Semi trucks</b><br><span>Dry van, reefer, flatbed, step deck, power only &middot; gross {money(M['gross'][0])}-{money(M['gross'][1])}/wk</span></div><span class="pct">{pl(M)}</span></div>
      <div class="row"><div><b>Hotshot</b><br><span>Gooseneck &amp; flatbed trailers &middot; gross $7,000-$9,000/wk</span></div><span class="pct">8%</span></div>
      <div class="row"><div><b>Box &amp; straight trucks</b><br><span>Gross $7,000-$9,000/wk</span></div><span class="pct">10%</span></div>
      <a class="btn btn-red" href="estimate.html">Calculate my dispatch fee</a>
      <small>OTR operations. Rough estimate; final percentage set in your dispatch agreement. Earnings not guaranteed.</small>
    </aside>
  </div>
</section>"""
    body = f"""{hero}
<section class="sec" style="padding-bottom:0"><div class="wrap">{answer(*qa)}</div></section>
<section class="sec" id="pricing"><div class="wrap">
  <div class="sec-head center rv"><span class="eyebrow">Truck dispatch rates</span><h2>No flat rate. Pay only a percentage of what your truck grosses.</h2><p>Transparent OTR dispatch pricing for owner-operators and small fleets. No setup fee, no monthly subscription, no long-term contract.</p></div>
  {pricing_cards()}
</div></section>
<section class="sec sec-dark"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Rate board</span><h2>What loads are paying</h2><p>A rough guide to rates per mile on common equipment. Flatbed and step deck loads often pay $5-7 a mile, reefer $4-6, hotshot $4-5, dry van and power only $3-5, and box trucks $1.80-3.20, depending on lane, season and local or OTR.</p></div>
  {rate_board()}
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Why carriers choose us</span><h2>A dispatch team that works for the carrier</h2><p>Load boards, broker calls, rate negotiation and paperwork, handled by real dispatchers while you drive.</p></div>
  {features()}
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">How it works</span><h2>Start dispatching in four steps</h2></div>
  {steps()}
</div></section>
<section class="sec sec-soft" id="contact"><div class="wrap two">
  <div>
    <div class="sec-head rv"><span class="eyebrow">Contact us</span><h2>Talk to a dispatcher</h2><p>Tell us about your truck, authority and lanes. Prefer to chat? WhatsApp is the fastest way to reach us.</p></div>
    {lead_form("homeForm", "New dispatch inquiry (home page)", "Send My Details")}
  </div>
  <div class="aside">{contact_side()}</div>
</div></section>
<section class="sec sec-dark tools-sec"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Free trucking tools</span><h2>Know your numbers before you book</h2><p>Free calculators built for owner-operators, with diesel prices for all 50 states updated every day.</p></div>
  <div class="grid g3">
    <a class="tool-card rv" href="truck-fuel-cost-calculator.html"><div class="icon">{ICONS['truck']}</div><h3>Truck fuel cost calculator</h3><p>MPG by truck type and load weight, trip fuel cost and cost per mile, with today's diesel price for your state.</p><span class="more">Calculate fuel cost &rarr;</span></a>
    <a class="tool-card rv" href="estimate.html"><div class="icon">{ICONS['calc']}</div><h3>Dispatch fee calculator</h3><p>See your weekly and monthly dispatch fee for your truck: semi 5%, hotshot 8%, box truck 10%.</p><span class="more">Estimate my fee &rarr;</span></a>
    <a class="tool-card rv" href="cost-per-mile-calculator.html"><div class="icon">{ICONS['cash']}</div><h3>Cost per mile calculator</h3><p>Your true operating cost per mile, from truck payment and insurance to fuel and driver pay.</p><span class="more">Find my CPM &rarr;</span></a>
  </div>
  <p class="mt-l center"><a class="btn btn-line" href="tools.html">See all free tools</a></p>
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Truck dispatch FAQ</span><h2>Questions owner-operators ask</h2></div>
  {faq_html(C.FAQS[:4])}
  <div class="faq faq-more" id="moreFaqs" hidden>
{chr(10).join(f'    <details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in C.FAQS[4:])}
  </div>
  <p class="mt-l"><button class="btn btn-line" type="button" data-expand="moreFaqs" data-more="See all FAQs" data-less="Show fewer FAQs" aria-expanded="false" aria-controls="moreFaqs">See all FAQs</button></p>
</div></section>
{band()}"""
    schemas = [service("Truck Dispatch Service", desc, "/", "Truck dispatch"), faq_ld([qa] + C.FAQS[:4]), howto(), speakable("/", title)]
    write("index.html", page("/", title, desc, HOME_KW, schemas, body, current="index.html"))


def build_estimate():
    title = "Truck Dispatch Fee Calculator & Free Quote | Texas Solutions"
    desc = (f"Estimate your truck dispatch fee: semi trucks {pl(M)}, hotshots 8% and box trucks 10% of weekly gross, "
            "OTR only, no flat rate. Enter your trucks and weekly gross, see your weekly and monthly fee, and request a free quote.")
    rpm = {eq: r for eq, r, _ in C.RATE_GUIDE}
    trucks_cfg = []
    for kind in ("semi", "small"):
        pr = C.PRICING[kind]
        for eq in pr["equipment"]:
            trucks_cfg.append({"id": eq.lower().replace(" ", "-"), "name": eq, "kind": kind, "label": pr["label"],
                               "pct": [C.EQ_PCT[eq], C.EQ_PCT[eq]], "gross": list(pr["gross"]),
                               "rpm": rpm.get(eq, rpm.get("Box Truck"))})
    cfg = {"trucks": trucks_cfg, "wa": C.WHATSAPP}
    qa = ("How is the Texas Solutions dispatch fee calculated?",
          f"Multiply your truck's weekly gross by the dispatch percentage: {pl(M)} for OTR semi trucks, 8% "
          f"for hotshots and 10% for box trucks. Example: a semi grossing $9,000 a week pays $450 a week. A hotshot grossing $8,000 pays $640; a box truck grossing $8,000 pays $800. "
          "There is no flat rate and no setup fee.")
    truck_btns = "\n".join(
        f'        <label><input type="radio" name="estTruck" value="{tc["id"]}"{" checked" if i == 0 else ""}>'
        f'<b>{tc["name"]}</b><span>{pl(tc)} &middot; {tc["rpm"].replace(" - ", "-").replace(".00", "")}/mi</span></label>'
        for i, tc in enumerate(trucks_cfg))
    eq_opts = "".join(f'<option value="{tc["id"]}">{tc["name"]}</option>' for tc in trucks_cfg)
    calc = f"""<div class="est rv" id="estimator" data-pricing='{json.dumps(cfg)}'>
  <div class="est-in">
    <h2 style="font-size:26px">Dispatch fee calculator</h2>
    <p style="color:var(--muted);margin-top:8px">Pick your truck, number of trucks and weekly gross per truck.</p>
    <div class="field"><span class="flabel">Your truck type</span>
      <div class="seg trucks" role="radiogroup" aria-label="Truck type">
{truck_btns}
      </div>
    </div>
    <div class="field"><label for="estTrucks">Number of trucks</label>
      <div class="range-row"><input type="range" id="estTrucks" min="1" max="25" value="1"><output id="estTrucksOut" for="estTrucks">1 truck</output></div>
    </div>
    <div class="field"><label for="estGross">Weekly gross per truck</label>
      <div class="range-row"><input type="range" id="estGross" min="3000" max="15000" step="250" value="9000"><output id="estGrossOut" for="estGross">$9,000</output></div>
      <p class="hint">Typical OTR weekly gross for a <b id="estTruckName2">Dry Van</b>: <b id="estTypical">$8,000 - $10,000</b></p>
    </div>
    <div class="field"><label for="estCustom">Your own percentage (optional)</label>
      <div class="range-row"><input type="number" id="estCustom" min="1" max="20" step="0.5" inputmode="decimal" placeholder="e.g. 5" class="pct-in"><output>%</output></div>
      <p class="hint">Type any percentage to see the dispatch fee at your rate. Leave empty to see our standard range.</p>
    </div>
    <span class="otr">&#9888; OTR trucks make more money &middot; no flat rate</span>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Price for your <span id="estTruckName">Dry Van</span></h3>
    <div class="est-big" id="estBig">$450<small>per week at 5%</small></div>
    <div class="est-lines">
      <div><span>Dispatch percentage</span><b id="estPct">5%</b></div>
      <div><span>Rough rate per mile</span><b id="estRpm">-</b></div>
      <div><span>Fee per truck, weekly</span><b id="estPerTruck">-</b></div>
      <div><span>Total fee, weekly</span><b id="estWeekly">-</b></div>
      <div><span>Total fee, monthly (avg)</span><b id="estMonthly">-</b></div>
      <div><span>You keep of gross, weekly</span><b id="estKeep">-</b></div>
    </div>
    <a class="btn btn-red" href="#quote">Get my free quote</a>
    <small>{esc(C.PRICING_NOTE)} Gross, rates and earnings are not guaranteed.</small>
  </div>
</div>"""
    quote = f"""<form class="form rv" id="waQuote" novalidate>
  <div class="grid g2">
    <div><label class="fl" for="wqName">Full name <i>*</i></label><input type="text" id="wqName" autocomplete="name" required></div>
    <div><label class="fl" for="wqPhone">Phone <i>*</i></label><input type="tel" id="wqPhone" autocomplete="tel" required></div>
    <div><label class="fl" for="wqTruck">Truck type <i>*</i></label><select id="wqTruck" required>{eq_opts}</select></div>
    <div><label class="fl" for="wqTrucks">Number of trucks</label><input type="number" id="wqTrucks" min="1" max="500" value="1"></div>
    <div><label class="fl" for="wqPct">Your desired percentage (%) <i>*</i></label><input type="number" id="wqPct" min="1" max="20" step="0.5" inputmode="decimal" placeholder="e.g. 5" required><p class="hint" id="wqPctHint" style="font-size:13px;color:var(--muted);margin-top:6px">Our rate for this truck: 5-6%</p></div>
    <div><label class="fl" for="wqGross">Weekly gross per truck ($)</label><input type="number" id="wqGross" min="0" step="100" inputmode="numeric" placeholder="e.g. 9000"></div>
    <div><label class="fl" for="wqMc">MC number</label><input type="text" id="wqMc" inputmode="numeric"></div>
    <div><label class="fl" for="wqLanes">Home base and lanes</label><input type="text" id="wqLanes" placeholder="e.g. Midland, TX. OTR Southeast"></div>
    <div class="full"><label class="fl" for="wqMsg">Message</label><textarea id="wqMsg" placeholder="Anything else we should know?"></textarea></div>
  </div>
  <button class="btn btn-wa" type="submit">{ICONS['wa']}Get Free Quote on WhatsApp</button>
  <p class="form-status" role="status" aria-live="polite"></p>
  <p class="fine">Tapping the button opens WhatsApp with your details filled in, ready to send to Texas Solutions at +1 (838) 910-3147. Nothing is sent until you press send in WhatsApp. Your requested percentage is reviewed by a dispatcher; the final percentage is discussed with each carrier.</p>
</form>"""
    body = f"""{phero("Estimate", "Truck Dispatch Fee Calculator &amp; Free Quote", f"See what dispatch costs before you sign. Semi trucks {pl(M)}, hotshots 8%, box trucks 10% of weekly gross, for OTR carriers. No flat rate.", ctas=False)}
<section class="sec" style="padding-top:56px"><div class="wrap">
  {calc}
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head center rv"><span class="eyebrow">Pricing at a glance</span><h2>OTR dispatch rates</h2></div>
  {pricing_cards(cta=False)}
</div></section>
<section class="sec" id="quote"><div class="wrap two">
  <div>
    <div class="sec-head rv"><span class="eyebrow">Free quote</span><h2>Name your percentage, get a free quote</h2><p>Tell us your truck and the dispatch percentage you want. Tap the button and your quote request opens in WhatsApp, ready to send.</p></div>
    {quote}
  </div>
  <div class="aside">
    {answer(*qa)}
    {contact_side()}
  </div>
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">FAQ</span><h2>Dispatch fee questions</h2></div>
  {faq_html([C.FAQS[0], C.FAQS[2], C.FAQS[3]])}
</div></section>
<section class="sec sec-dark"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Rate board</span><h2>Rough rates per mile</h2></div>
  {rate_board()}
</div></section>"""
    items = [qa] + [C.FAQS[0], C.FAQS[2], C.FAQS[3]]
    schemas = [service("Truck Dispatch Fee Estimate", desc, "/estimate.html", "Truck dispatch"),
               faq_ld(items), crumbs_ld([("Estimate", "/estimate.html")]), speakable("/estimate.html", title)]
    kw = "truck dispatch calculator, dispatch fee calculator, truck dispatch quote, how much does a truck dispatcher cost, truck dispatcher percentage, dispatch fee per week, owner operator dispatch cost, " + HOME_KW
    write("estimate.html", page("/estimate.html", title, desc, kw, schemas, body, current="estimate.html"))


def build_rates():
    title = "Truck Dispatch Rates 2026: 5% Semi, 8% Hotshot, 10% Box Truck | Texas Solutions"
    desc = ("Truck dispatch rates and rate-per-mile guide: semi trucks 5% of weekly gross, hotshots 8%, box trucks 10%, OTR, no flat rate. "
            "Flatbed and step deck $5-7/mile, reefer $4-6, hotshot $4-5, dry van and power only $3-5, box truck $1.80-3.20.")
    qa = ("What are truck dispatch rates in 2026?",
          f"Independent truck dispatchers usually charge a percentage of weekly gross. Texas Solutions charges {pl(M)} for OTR semi trucks and "
          f"8% for hotshots and 10% for OTR box trucks and straight trucks, with no flat rate. As a rough guide to freight rates, flatbed "
          "and step deck loads often pay $5-7 a mile, reefer $4-6, hotshot $4-5, dry van and power only $3-5, and box trucks $1.80-3.20.")
    rows = "\n".join(f"<tr><td><b>{eq}</b></td><td>{r}/mi</td><td>{n}</td></tr>" for eq, r, n in C.RATE_GUIDE)
    body = f"""{phero("Dispatch Rates", "Truck Dispatch Rates &amp; Rate-per-Mile Guide", "Clear percentage pricing for OTR carriers, plus a rough guide to what loads are paying by equipment type.")}
<section class="sec" style="padding-bottom:0"><div class="wrap">{answer(*qa)}</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head center rv"><span class="eyebrow">Dispatch fee</span><h2>Percentage of weekly gross. No flat rate.</h2></div>
  {pricing_cards()}
</div></section>
<section class="sec sec-dark"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Rate board</span><h2>Rough freight rates per mile</h2><p>Rates move with lane, season, fuel and market. These are rough estimates, not offers of freight.</p></div>
  {rate_board()}
</div></section>
<section class="sec"><div class="wrap two">
  <div class="prose">
    <h2 style="margin-top:0">Rate per mile by equipment</h2>
    <div style="overflow-x:auto;margin-top:18px"><table class="board-table" style="background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden">
      <thead><tr><th>Equipment</th><th>Rough rate</th><th>Notes</th></tr></thead>
      <tbody style="color:var(--text)">{rows.replace('<td>', '<td style="color:var(--text);border-color:var(--line)">')}</tbody>
    </table></div>
    <h2>Local vs OTR dry van rates</h2>
    <p>Dry van freight has the widest range, roughly $3 to $5 a mile. Short local and regional loads often pay more per mile because the load is short, while long OTR runs pay less per mile but more per load. Our published dispatch percentages apply to OTR operations.</p>
    <h2>Example: what dispatch costs on a typical week</h2>
    <ul>
      <li>Semi truck grossing {money(M['gross'][0])}-{money(M['gross'][1])}: fee about {SEMI_FEE[0]}-{SEMI_FEE[1]} a week at {pl(M)}.</li>
      <li>Box truck or hotshot grossing {money(S['gross'][0])}-{money(S['gross'][1])}: fee about $560-$720 a week for a hotshot at 8%, $700-$900 for a box truck at 10%.</li>
      <li>No setup fee, no monthly subscription, no flat weekly charge.</li>
    </ul>
  </div>
  <div class="aside">{contact_side()}</div>
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">FAQ</span><h2>Dispatch rate questions</h2></div>
  {faq_html([C.FAQS[0], C.FAQS[3], C.FAQS[2], C.FAQS[7]])}
</div></section>
{band()}"""
    items = [qa, C.FAQS[0], C.FAQS[3], C.FAQS[2], C.FAQS[7]]
    schemas = [service("Truck Dispatch Rates", desc, "/truck-dispatch-rates.html", "Truck dispatch"), faq_ld(items),
               crumbs_ld([("Dispatch Rates", "/truck-dispatch-rates.html")]), speakable("/truck-dispatch-rates.html", title)]
    kw = "truck dispatch rates, dispatch rates per mile, flatbed rates per mile, hotshot rates per mile, dry van rates per mile, truck dispatcher percentage, dispatch fee, 5 percent dispatch, 10 percent dispatch, " + HOME_KW
    write("truck-dispatch-rates.html", page("/truck-dispatch-rates.html", title, desc, kw, schemas, body, current="truck-dispatch-rates.html"))


def build_contact():
    title = "Contact a Truck Dispatcher | Call or WhatsApp (838) 910-3147 | Texas Solutions"
    desc = "Talk to a Texas Solutions truck dispatcher. Call or WhatsApp (838) 910-3147, email dispatch@texassolutions.co, or send your details. Office: 401 W Kentucky Ave, Midland, TX."
    body = f"""{phero("Contact", "Talk to a Truck Dispatcher", "Tell us about your truck, authority and lanes. The fastest way to reach us is WhatsApp.", ctas=False)}
<section class="sec" style="padding-top:56px"><div class="wrap two">
  <div>{lead_form("contactForm", "New dispatch inquiry", "Send My Details")}</div>
  <div class="aside">{contact_side()}
    {answer("Is there a fee to talk to a dispatcher?", f"No. The first call is free. Paid dispatch is {pl(M)} of weekly gross for OTR semis, 8% for hotshots and 10% for box trucks, with no flat rate or setup fee.", "Good to know")}
  </div>
</div></section>"""
    schemas = [{"@context": "https://schema.org", "@type": "ContactPage", "name": title, "url": url("/contact.html"), "about": {"@id": BUSINESS_ID}},
               crumbs_ld([("Contact", "/contact.html")])]
    kw = "contact truck dispatcher, truck dispatch phone number, truck dispatch WhatsApp, hire a truck dispatcher, truck dispatch Midland TX, " + HOME_KW
    write("contact.html", page("/contact.html", title, desc, kw, schemas, body, current="contact.html"))


def build_about():
    title = "About Texas Solutions | Truck Dispatch Company in Midland, Texas"
    desc = "Texas Solutions is a truck dispatch company in Midland, Texas, working for owner-operators and small fleets: load search, rate negotiation and paperwork. Not a broker. No flat rate."
    holds = [("You approve everything", "No load, lane or rate is committed without your say-so. There is no forced dispatch here."),
             ("Plain pricing", f"{pl(M)} of weekly gross for OTR semis, 8% for hotshots, 10% for box trucks. No setup charge, no flat rate, no monthly subscription."),
             ("No promises on rates", "Markets move. We commit to the search, the comparison and the negotiation, never to a number."),
             ("Your data stays here", "Applications are for our own dispatch service. We do not sell or transfer your inquiry to lead buyers.")]
    cards = "\n".join(f'  <div class="card rv"><div class="icon">{ICONS["check"]}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in holds)
    chips = "".join(f'<a class="chip" href="{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING if not p.get("guide"))
    body = f"""{phero("About", "A dispatch team, not a lead broker.", "Texas Solutions provides dispatch services directly to the carriers who sign our agreement. Your application is never sold to outside lead buyers, and the people searching your lanes are the people you speak to on the phone.")}
<section class="sec"><div class="wrap two">
  <div class="prose rv">
    <h2 style="margin-top:0">We work for the carrier</h2>
    <p>Owner-operators and small fleets run thin on time. Every hour spent calling brokers, comparing boards and chasing rate confirmations is an hour off the road. Our team takes that work on so the truck stays moving and the decisions stay yours.</p>
    <p>We do not own trucks and we are not a freight broker. We are a dispatch service based in {C.CITY}, Texas, paid a percentage of weekly gross under a signed agreement, with no setup fee, no flat rate and no long-term contract.</p>
    <h2>Equipment we dispatch</h2>
    <div class="chip-row" style="justify-content:flex-start">{chips}</div>
  </div>
  <div class="aside">{contact_side()}</div>
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">How we operate</span><h2>Four things we hold to</h2></div>
  <div class="grid g2">
{cards}
  </div>
</div></section>
{band("Tell us about your truck.", "Speak with a dispatcher about your authority, equipment and preferred lanes. No load is booked without your approval.")}"""
    schemas = [{"@context": "https://schema.org", "@type": "AboutPage", "name": title, "url": url("/about.html"), "about": {"@id": BUSINESS_ID}},
               crumbs_ld([("About", "/about.html")])]
    write("about.html", page("/about.html", title, desc, "truck dispatch company, truck dispatch company Texas, Midland truck dispatch, " + HOME_KW, schemas, body, current="about.html"))


def build_faq():
    title = "Truck Dispatch FAQ: Cost, Percentage, OTR & How It Works | Texas Solutions"
    desc = f"Answers about truck dispatch: how much a dispatcher costs ({pl(M)} semi, 8% hotshot, 10% box truck), OTR vs local, contracts, paperwork and getting started."
    extra = [(q, a) for p in C.LANDING for q, a in p["faqs"]]
    items = C.FAQS + extra
    body = f"""{phero("FAQ", "Truck Dispatch FAQ", "Straight answers on cost, contracts, loads and getting started.")}
<section class="sec"><div class="wrap">
  {faq_html(items)}
</div></section>
{band()}"""
    schemas = [faq_ld(items), crumbs_ld([("FAQ", "/faq.html")]), speakable("/faq.html", title)]
    write("faq.html", page("/faq.html", title, desc, "truck dispatch FAQ, how much does a truck dispatcher cost, truck dispatcher percentage, " + HOME_KW, schemas, body, current="faq.html"))


def build_legal(name, crumb):
    raw = (ROOT / "tools" / "legal" / name).read_text(encoding="utf-8")
    t = re.search(r"<!-- TITLE: (.*?) -->", raw).group(1)
    lede = re.search(r"<!-- LEDE: (.*?) -->", raw).group(1)
    inner = re.sub(r"<!-- (TITLE|LEDE): .*? -->\n?", "", raw)
    title = f"{html.unescape(crumb)} | {C.BRAND}"
    desc = f"{html.unescape(crumb)} for {C.BRAND} (dispatch.texassolutions.co)."
    body = f"""{phero(crumb, t.title().replace('&Amp;', '&amp;'), esc(lede), ctas=False)}
<section class="sec" style="padding-top:48px"><div class="wrap">
{inner}
</div></section>"""
    write(name, page("/" + name, title, desc, "Texas Solutions dispatch " + crumb.lower(), [crumbs_ld([(html.unescape(crumb), "/" + name)])], body))


def build_landing(p):
    kind = landing_pricing(p)
    truck_q = {"box-truck-dispatch.html": "truck=box-truck", "hotshot-dispatch.html": "truck=hotshot", "flatbed-dispatch.html": "truck=flatbed",
               "dry-van-dispatch.html": "truck=dry-van", "reefer-dispatch.html": "truck=reefer", "power-only-dispatch.html": "truck=power-only"}.get(p["file"], "type=" + p["kind"])
    lo, hi = money(kind["gross"][0] * kind["pct"][0] / 100), money(kind["gross"][1] * kind["pct"][1] / 100)
    path = "/" + p["file"]
    body_p = "\n".join(f"    <p>{esc(x)}</p>" for x in p["body"])
    sections = ""
    for h, lis in p.get("sections", []):
        sections += f"\n    <h2>{esc(h)}</h2>\n    <ul>\n" + "\n".join(f"      <li>{esc(x)}</li>" for x in lis) + "\n    </ul>"
    what = "" if p.get("guide") else f"""
    <h2>What our {esc(p['nav'].lower())} includes</h2>
    <ul>
      <li>Load search across load boards and broker networks</li>
      <li>Rate negotiation before any load reaches you</li>
      <li>Lane, deadhead and home-time planning</li>
      <li>Broker setup packets and rate confirmations</li>
      <li>You approve every load, with no forced dispatch</li>
    </ul>
    <h2>{esc(p['nav'])} pricing</h2>
    <p>{kind['label']} on OTR pay <b>{pl(kind)} of weekly gross</b>. With typical weekly gross of {money(kind['gross'][0])}-{money(kind['gross'][1])}, the dispatch fee is about {lo}-{hi} a week. No flat rate, no setup fee and no monthly subscription. <a href="estimate.html?{truck_q}">Estimate your fee</a>.</p>"""
    faqs = p["faqs"] + [C.FAQS[0], C.FAQS[5]]
    others = "".join(f'<a class="chip" href="{o["file"]}">{esc(o["nav"])}</a>' for o in C.LANDING if o["file"] != p["file"])
    body = f"""{phero(p['nav'], esc(p['h1']), esc(p['lede']), extra=f'<div class="chip-row" style="justify-content:flex-start"><span class="chip" ><b>{pl(kind)}</b> of weekly gross</span><span class="chip" >OTR &middot; No flat rate</span></div>')}
<section class="sec" style="padding-bottom:0"><div class="wrap">{answer(p['h1'] if p.get('guide') else f"What is {p['nav'].lower()} from Texas Solutions?", p['answer'])}</div></section>
<section class="sec"><div class="wrap two">
  <div class="prose rv">
{body_p}{sections}{what}
  </div>
  <div class="aside">
    <div class="price feat"><h3>{kind['label']}</h3><div class="amt">{pl(kind)}<small> of weekly gross</small></div><ul><li>OTR operations</li><li>No flat rate or setup fee</li><li>About {lo}-{hi}/week on typical gross</li></ul><a class="btn btn-red" href="estimate.html?{truck_q}">Get a Free Estimate</a></div>
    <a class="card tool-mini" href="truck-fuel-cost-calculator.html?{truck_q if truck_q.startswith('truck=') else ''}#fuelCalc"><div class="icon">{ICONS['truck']}</div><div><b>Fuel cost for this truck</b><p>MPG, fuel per mile and today's diesel price by state.</p></div></a>
    {contact_side()}
  </div>
</div></section>
<section class="sec sec-dark"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Rate board</span><h2>Rough rates per mile</h2></div>
  {rate_board()}
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">FAQ</span><h2>{esc(p['nav'])} questions</h2></div>
  {faq_html(faqs)}
  <div class="chip-row mt-l" style="justify-content:flex-start">{others}</div>
</div></section>
{band()}"""
    schemas = [service(p["h1"], p["answer"], path, p["nav"].replace("What a Truck Dispatcher Does", "Truck dispatch")),
               faq_ld(faqs), crumbs_ld([(p["nav"], path)]), speakable(path, p["title"])]
    og = "article" if p.get("guide") else "website"
    if p.get("guide"):
        schemas.append({"@context": "https://schema.org", "@type": "Article", "headline": p["h1"], "description": p["description"],
                        "datePublished": "2026-09-01", "dateModified": "2026-09-23", "author": {"@id": BUSINESS_ID},
                        "publisher": {"@id": BUSINESS_ID}, "mainEntityOfPage": url(path), "image": OG_IMAGE})
    write(p["file"], page(path, p["title"], p["description"], p["keywords"] + ", " + ", ".join(C.CORE_KEYWORDS[:8]), schemas, body, og_type=og))



def load_diesel():
    p = ROOT / "data" / "diesel-prices.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def build_fuel():
    path = "/truck-fuel-cost-calculator.html"
    diesel = load_diesel()
    regions = diesel["regions"] if diesel else {}
    week = diesel["week"] if diesel else ""
    us = regions.get("US", {}).get("price", 0)
    week_h = ""
    if week:
        d0 = date.fromisoformat(week)
        week_h = f"{d0.strftime('%B')} {d0.day}, {d0.year}"
    states_p = diesel.get("states", {}) if diesel else {}
    day = diesel.get("day") if diesel else None
    day_h = ""
    if day:
        d1 = date.fromisoformat(day)
        day_h = f"{d1.strftime('%B')} {d1.day}, {d1.year}"
    sp = lambda code: states_p.get(code) or regions.get(C.STATE_REGION[code][1], {}).get("price", 0)
    ranked = sorted(C.STATE_REGION, key=sp)
    cheap, dear = ranked[:3], ranked[-3:][::-1]
    nm = lambda code: C.STATE_REGION[code][0]
    title = "Fuel Price Calculator for Trucks & Diesel Prices Today by State (USA) | Texas Solutions"
    desc = (f"Free truck fuel price calculator with diesel prices for all 50 states, updated daily. Diesel today: Texas ${sp('TX'):.2f}, "
            f"California ${sp('CA'):.2f}, U.S. average ${us:.2f}. Calculate fuel cost for dry van, reefer, flatbed, step deck, hotshot and box trucks.")
    today_qa = ("What is the price of diesel today?",
                f"Diesel prices today ({day_h or week_h}): Texas ${sp('TX'):.3f}, California ${sp('CA'):.3f}, Florida ${sp('FL'):.3f}, "
                f"Illinois ${sp('IL'):.3f}, New York ${sp('NY'):.3f} and Georgia ${sp('GA'):.3f} per gallon. The cheapest diesel is in "
                f"{nm(cheap[0])} (${sp(cheap[0]):.3f}), {nm(cheap[1])} and {nm(cheap[2])}; the most expensive is in {nm(dear[0])} "
                f"(${sp(dear[0]):.3f}), {nm(dear[1])} and {nm(dear[2])}. The EIA U.S. weekly average is ${us:.3f}.")
    trucks = [{"id": i, "name": n, "empty": e, "k": k, "max": mx, "def": d, "idle": ig, "spd": sp} for i, n, e, k, mx, d, ig, sp in C.FUEL_TRUCKS]
    states = {k: {"name": n, "region": r} for k, (n, r) in C.STATE_REGION.items()}
    cfg = {"trucks": trucks, "states": states, "reeferGph": C.REEFER_GAL_PER_HOUR, "diesel": diesel}
    btns = "\n".join(
        f'        <label><input type="radio" name="fuelTruck" value="{tr["id"]}"{" checked" if i == 0 else ""}><b>{tr["name"]}</b>'
        f'<span>~{tr["empty"] / (1 + tr["k"] * tr["def"] / 1000):.1f} mpg loaded</span></label>'
        for i, tr in enumerate(trucks))
    st_opts = "".join(f'<option value="{k}"{" selected" if k == "TX" else ""}>{v[0]}</option>' for k, v in sorted(C.STATE_REGION.items(), key=lambda kv: kv[1][0]))
    rows = ""
    for code in sorted(C.STATE_REGION, key=nm):
        price = sp(code)
        diff = price - us
        cls = "up" if diff > 0.0005 else ("down" if diff < -0.0005 else "")
        src = "" if states_p.get(code) else " <small>EIA regional</small>"
        rows += (f'<tr id="diesel-{code.lower()}"><td><b><a href="diesel-prices/{slugify(nm(code))}.html" style="color:var(--ink)">{nm(code)}</a></b>{src}</td><td class="rate">${price:.3f}</td>'
                 f'<td class="chg {cls}">{"+" if diff >= 0 else "-"}${abs(diff):.3f}</td></tr>\n')
    truck_secs = ""
    for tid, tname, emp, k, mx, dflt, idle, spd in C.FUEL_TRUCKS:
        mpg = emp / (1 + k * dflt / 1000)
        gal = 1000 / mpg
        truck_secs += f"""  <div class="card rv" id="{tid}-fuel-calculator">
    <h3>{tname} fuel cost calculator</h3>
    <p>A {tname.lower()} averages about <b>{emp:.1f} mpg empty</b> and <b>{mpg:.1f} mpg with {dflt:,} lbs</b> of cargo. Over 1,000 miles that is about {gal:.0f} gallons, or <b>${gal * us:,.0f}</b> at the U.S. average diesel price (${gal * us / 1000:.2f} per mile).</p>
    <a class="more" href="truck-fuel-cost-calculator.html?truck={tid}#fuelCalc">Calculate {tname.lower()} fuel cost &rarr;</a>
  </div>
"""
    qa = ("How do I calculate truck fuel cost per mile?",
          f"Divide the diesel price by your truck's miles per gallon. A loaded semi averaging about 6.3 mpg with diesel at ${us:.2f} a gallon "
          f"spends about ${us / 6.3:.2f} per mile on fuel. Heavier loads lower MPG: NACFE research puts it at about 0.5-0.6% more fuel for every 1,000 lbs, roughly 0.3-0.4 mpg per 10,000 lbs on a Class 8 truck.")
    calc = f"""<div class="est rv" id="fuelCalc" data-fuel='{json.dumps(cfg).replace("'", "&#39;")}'>
  <div class="est-in">
    <h2 style="font-size:26px">Fuel cost calculator</h2>
    <p style="color:var(--muted);margin-top:8px">Choose your truck, load weight, miles and state.</p>
    <div class="field"><span class="flabel">Truck type</span>
      <div class="seg trucks" role="radiogroup" aria-label="Truck type">
{btns}
      </div>
    </div>
    <div class="field"><label for="fuelWeight">Cargo weight</label>
      <div class="range-row"><input type="range" id="fuelWeight" min="0" max="45000" step="500" value="38000"><output id="fuelWeightOut" for="fuelWeight">38,000 lbs</output></div>
      <p class="hint">Max for this truck: <b id="fuelMax">45,000 lbs</b></p>
    </div>
    <div class="grid g2" style="gap:14px;margin-top:22px">
      <div><label class="flabel" for="fuelMiles">Loaded miles</label><input class="pct-in" type="number" id="fuelMiles" min="1" step="1" value="1000" inputmode="numeric"></div>
      <div><label class="flabel" for="fuelDead">Deadhead miles</label><input class="pct-in" type="number" id="fuelDead" min="0" step="1" value="100" inputmode="numeric"></div>
      <div><label class="flabel" for="fuelState">Fuel up in (state)</label><select class="pct-in" id="fuelState">{st_opts}</select></div>
      <div><label class="flabel" for="fuelPrice">Diesel price ($/gal)</label><input class="pct-in" type="number" id="fuelPrice" min="0" step="0.001" inputmode="decimal"></div>
      <div><label class="flabel" for="fuelMpg">Your MPG (optional)</label><input class="pct-in" type="number" id="fuelMpg" min="1" max="40" step="0.1" inputmode="decimal" placeholder="auto"></div>
      <div><label class="flabel" for="fuelRate">Load rate per mile (optional)</label><input class="pct-in" type="number" id="fuelRate" min="0" step="0.01" inputmode="decimal" placeholder="e.g. 5.50"></div>
      <div><label class="flabel" for="fuelSpeed">Average highway speed (mph)</label><input class="pct-in" type="number" id="fuelSpeed" min="40" max="85" step="1" value="62" inputmode="numeric"></div>
      <div><label class="flabel" for="fuelIdle">Idle hours</label><input class="pct-in" type="number" id="fuelIdle" min="0" step="1" value="0" inputmode="numeric"></div>
      <div id="fuelReeferWrap" hidden><label class="flabel" for="fuelReefer">Reefer unit hours</label><input class="pct-in" type="number" id="fuelReefer" min="0" step="1" value="0" inputmode="numeric"></div>
    </div>
    <p class="hint" id="fuelPriceNote" style="margin-top:12px">Diesel price auto-filled from the latest EIA weekly average for your state's region. Edit it to match your pump price.</p>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Trip fuel cost</h3>
    <div class="est-big" id="fuelBig">$0<small>for 0 miles</small></div>
    <div class="est-lines">
      <div><span>Estimated MPG</span><b id="fuelMpgOut">-</b></div>
      <div><span>Total miles</span><b id="fuelTotalMi">-</b></div>
      <div><span>Diesel needed</span><b id="fuelGal">-</b></div>
      <div><span>Driving / idle / reefer</span><b id="fuelSplit">-</b></div>
      <div><span>Fuel cost per mile</span><b id="fuelCpm">-</b></div>
      <div><span>Diesel price used</span><b id="fuelPriceUsed">-</b></div>
      <div id="fuelRevRow" hidden><span>Revenue after fuel</span><b id="fuelNet">-</b></div>
      <div id="fuelShareRow" hidden><span>Fuel as % of revenue</span><b id="fuelShare">-</b></div>
    </div>
    <a class="btn btn-red" href="estimate.html">Estimate my dispatch fee</a>
    <a class="btn btn-wa" href="{WA_URL}" target="_blank" rel="noopener">{ICONS['wa']}Find better-paying loads</a>
    <small>Estimates only. Real fuel use depends on speed, terrain, weather, idling, tires and engine. Diesel prices are EIA regional weekly averages, not a specific station.</small>
  </div>
</div>"""
    faqs = [today_qa,
            ("What is the price of diesel in Texas today?", f"Diesel in Texas averages ${sp('TX'):.3f} per gallon today ({day_h or week_h}), compared with the U.S. average of ${us:.3f}."),
            ("Which state has the cheapest diesel?", f"Today the cheapest diesel is in {nm(cheap[0])} at ${sp(cheap[0]):.3f} a gallon, then {nm(cheap[1])} and {nm(cheap[2])}. The most expensive is {nm(dear[0])} at ${sp(dear[0]):.3f}."),
            qa,
            ("How many miles per gallon does a semi truck get?", "A loaded Class 8 semi typically gets about 6 to 7 miles per gallon; empty, closer to 7 to 8 mpg. Speed, terrain, weather, aerodynamics and idling all change the number."),
            ("How much diesel does a semi truck use per mile?", "Roughly 0.14 to 0.17 gallons per mile for a loaded semi averaging 6 to 7 mpg. Multiply by the diesel price to get fuel cost per mile."),
            ("How much does it cost to fuel a semi truck for 1,000 miles?", f"At about 6.3 mpg a semi burns roughly 159 gallons over 1,000 miles. At ${us:.2f} a gallon that is about ${159 * us:,.0f}. Use the calculator above for your own truck, weight and state."),
            ("How many miles per gallon does a hotshot truck get?", "A 1-ton diesel pickup pulling a gooseneck typically gets about 12 to 14 mpg empty and about 9 to 11 mpg loaded, depending on cargo weight and trailer."),
            ("How many miles per gallon does a box truck get?", "A 26-foot diesel box truck typically gets about 8 to 10 mpg, dropping toward 7 to 8 mpg near its maximum payload."),
            ("Does cargo weight affect fuel mileage?", "Yes. Heavier loads need more power, so MPG drops as weight goes up. The effect is larger on hotshots and box trucks, where cargo is a bigger share of total weight."),
            ("Why is diesel more expensive in California?", "California has stricter fuel specifications, higher state taxes and fees, and a relatively isolated refining market, so its diesel price is usually the highest in the country."),
            ("Where do the diesel prices on this page come from?", "State prices are AAA's daily state averages, refreshed every day. The U.S. average comes from the U.S. Energy Information Administration's weekly diesel survey, which is also used as a backup for any state without a daily price."),
            ("How much does it cost to fuel a dry van, reefer or step deck?", f"A loaded dry van or step deck averages about 6.0-6.3 mpg, a reefer about 6.0 mpg plus reefer unit fuel. At ${us:.2f} a gallon, that is roughly ${us / 6.3:.2f}-${us / 6.0:.2f} of diesel per mile."),
            ("How much does it cost to fuel a box truck per mile?", f"A 26 ft diesel box truck averages about 8.5-11 mpg depending on load, so fuel costs about ${us / 11:.2f}-${us / 8.5:.2f} per mile at ${us:.2f} a gallon."),
            ("How can truckers lower fuel cost per mile?", "Cut deadhead miles, slow down (fuel use rises sharply above about 62 mph), reduce idling, keep tires properly inflated, and book loads that pay enough per mile to cover fuel. A dispatcher who plans lanes can help cut empty miles.")]
    body = f"""{phero("Fuel Calculator", "Truck Fuel Cost Calculator", f"Calculate fuel cost for your truck, load weight and state, with today's diesel prices for all 50 states. Updated daily.", ctas=False)}
<section class="sec" style="padding-top:48px;padding-bottom:0"><div class="wrap">{answer(*today_qa, label="Diesel price today")}</div></section>
<section class="sec" style="padding-top:40px"><div class="wrap">
  {calc}
</div></section>
<section class="sec sec-dark" id="diesel-prices"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Fuel prices today</span><h2>Diesel prices by state today</h2><p>Average on-highway diesel price per gallon in all 50 states and Washington, DC{f", {day_h}" if day_h else ""}, compared with the U.S. average of ${us:.3f}. Updated every day.</p></div>
  <div class="board rv"><div style="overflow-x:auto"><table class="board-table diesel-table" id="dieselTable">
    <thead><tr><th>State</th><th>Diesel $/gal</th><th>vs U.S. avg</th></tr></thead>
    <tbody>
{rows}    </tbody>
  </table></div>
  <p class="board-foot">Daily state averages: <a href="https://gasprices.aaa.com/state-gas-price-averages/" rel="noopener" style="color:var(--red-600)">AAA</a>, as of <span id="dieselDay">{day_h or "-"}</span>. U.S. average and fallback regional prices: <a href="https://www.eia.gov/petroleum/gasdiesel/" rel="noopener" style="color:var(--red-600)">U.S. Energy Information Administration</a>, week of <span id="dieselWeek">{week_h}</span>.</p></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Fuel calculator by truck type</span><h2>Fuel price calculator for every truck</h2><p>Fuel cost for dry van, reefer, flatbed, step deck, power only, hotshot, box truck and straight truck, based on published fuel economy data and today's diesel prices.</p></div>
  <div class="grid g4">
{truck_secs}  </div>
</div></section>
<section class="sec sec-soft"><div class="wrap two">
  <div class="prose rv">
    <h2 style="margin-top:0">Why fuel prices matter for truckers</h2>
    <p>Fuel is the second-largest operating cost in trucking after driver pay. At ${us:.2f} a gallon, a semi averaging 6.3 mpg spends about ${us / 6.3:.2f} on diesel for every mile, loaded or empty. On a 2,500-mile week that is roughly ${2500 / 6.3 * us:,.0f}.</p>
    <p>Diesel prices can differ by more than ${sp(dear[0]) - sp(cheap[0]):.2f} a gallon between states. Fuelling in {nm(cheap[0])} instead of {nm(dear[0])} saves about ${(sp(dear[0]) - sp(cheap[0])) * 150:,.0f} on a 150-gallon fill. Planning fuel stops by state is one of the easiest ways to cut cost per mile.</p>
    <h2>How to use the fuel price calculator</h2>
    <ul>
      <li>Pick your truck type: dry van, reefer, flatbed, step deck, power only, hotshot, box truck or straight truck.</li>
      <li>Set the cargo weight; heavier loads burn more fuel.</li>
      <li>Enter loaded and deadhead miles, your average speed and any idle hours.</li>
      <li>Choose the state where you fuel up. Today's diesel price fills in automatically, or type your own pump price.</li>
      <li>Add your rate per mile to see revenue left after fuel.</li>
    </ul>
  </div>
  <div class="aside">{answer("Which state has the cheapest diesel today?", f"{nm(cheap[0])} has the cheapest diesel today at ${sp(cheap[0]):.3f} a gallon, followed by {nm(cheap[1])} (${sp(cheap[1]):.3f}) and {nm(cheap[2])} (${sp(cheap[2]):.3f}). {nm(dear[0])} is the most expensive at ${sp(dear[0]):.3f}.", "Cheapest diesel")}</div>
</div></section>
<section class="sec"><div class="wrap two">
  <div class="prose rv">
    <h2 style="margin-top:0">How the fuel calculator works</h2>
    <p>Fuel use is calculated per mile and rises with cargo weight: each 1,000 lbs adds about 0.55% fuel on a semi (NACFE), more on smaller trucks where cargo is a bigger share of total weight. The model is calibrated to published averages:</p>
    <ul>
      <li>Semi (dry van, power only): about 7.6 mpg empty, 6.3 mpg at 38,000 lbs, 6.1 mpg at 45,000 lbs. The FHWA national average for combination trucks is 6.3 mpg.</li>
      <li>Reefer, flatbed and step deck: slightly lower, for heavier trailers or open-deck drag. Reefer units add about {C.REEFER_GAL_PER_HOUR} gallons per hour.</li>
      <li>Hotshot (1-ton dually and gooseneck): about 13.5 mpg empty, 9.7 mpg at 9,000 lbs, 8 mpg near 16,000 lbs.</li>
      <li>26 ft box truck: about 11 mpg empty, 8.5 mpg fully loaded. Straight truck: about 9.5 mpg empty, 7.2 mpg loaded.</li>
      <li>Speed: figures assume 62 mph. Above that, a semi loses about 0.1 mpg per mph. Idling burns about 0.8 gallons per hour on a semi.</li>
    </ul>
    <p>If you know your real MPG from your ELD or fuel card, type it in and the calculator uses it instead.</p>
    <h2>Sources</h2>
    <ul>
{"".join(f'      <li><a href="{u}" rel="noopener">{esc(n)}</a></li>' + chr(10) for n, u in C.FUEL_SOURCES)}    </ul>
  </div>
  <div class="aside">{answer(*qa)}{contact_side()}</div>
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Fuel cost FAQ</span><h2>Diesel and fuel mileage questions</h2></div>
  {faq_html(faqs)}
</div></section>
{band("Fuel is your biggest cost. Better loads cover it.", "Our dispatchers negotiate every rate and plan lanes to cut deadhead miles, the fuel you burn without getting paid.")}"""
    schemas = [faq_ld(faqs), crumbs_ld([("Fuel Calculator", path)]), speakable(path, title),
               {"@context": "https://schema.org", "@type": "HowTo", "name": "How to calculate truck fuel cost for a trip",
                "step": [{"@type": "HowToStep", "position": 1, "name": "Pick your truck and load weight", "text": "Choose your truck type and enter the cargo weight to estimate miles per gallon."},
                         {"@type": "HowToStep", "position": 2, "name": "Add total miles", "text": "Enter loaded miles plus deadhead miles."},
                         {"@type": "HowToStep", "position": 3, "name": "Set the diesel price", "text": "Select the state where you fuel up to use today's diesel price, or type your pump price."},
                         {"@type": "HowToStep", "position": 4, "name": "Calculate", "text": "Gallons equal total miles divided by MPG; fuel cost equals gallons times the diesel price; cost per mile equals fuel cost divided by miles."}]},
               {"@context": "https://schema.org", "@type": "Dataset", "name": "Daily U.S. diesel prices by state",
                "description": "Average on-highway diesel prices (USD per gallon) for all 50 U.S. states and DC, updated daily, with the EIA weekly U.S. average.",
                "url": url(path) + "#diesel-prices", "dateModified": day or week or TODAY, "temporalCoverage": day or week or TODAY,
                "isBasedOn": ["https://gasprices.aaa.com/state-gas-price-averages/", "https://www.eia.gov/petroleum/gasdiesel/"],
                "isAccessibleForFree": True, "inLanguage": "en-US",
                "creator": {"@id": BUSINESS_ID}, "publisher": {"@id": BUSINESS_ID}, "spatialCoverage": {"@type": "Place", "name": "United States"},
                "variableMeasured": "Retail diesel price, USD per gallon"}]
    kw = ("fuel prices, fuel price calculator, fuel cost calculator, diesel prices today, diesel prices by state, diesel price per gallon, "
          "dry van fuel price calculator, step deck fuel price calculator, box truck fuel price calculator, reefer fuel cost calculator, "
          "flatbed fuel cost calculator, hotshot fuel calculator, power only fuel cost, straight truck fuel cost, fuel prices near me, "
          "cheapest diesel by state, diesel price Texas, diesel price California, trucking fuel cost per mile, trip fuel cost calculator, average diesel price, "
          "diesel prices near me, semi truck mpg, how many miles per gallon does a semi get, fuel cost per mile, truck fuel cost calculator, diesel cost calculator, fuel cost per mile calculator, semi truck fuel calculator, hotshot fuel calculator, "
          "box truck fuel cost, diesel prices by state, diesel price per gallon today, trucking fuel calculator, truck mpg calculator, " + ", ".join(C.CORE_KEYWORDS[:6]))
    write(path[1:], page(path, title, desc, kw, schemas, body, current=path[1:]))



def abs_links(shell):
    """Pages in sub-folders: make relative links root-absolute."""
    return re.sub(r'(href|src)="(?!https?:|/|#|tel:|mailto:|data:)', r'\1="/', shell)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load_posts():
    import yaml
    import markdown as md
    posts = []
    cache_file = ROOT / "assets" / "blog" / "covers.json"
    cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}
    for f in sorted((ROOT / "content" / "blog").glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if not m:
            continue
        meta = yaml.safe_load(m.group(1)) or {}
        if meta.get("draft"):
            continue

        def as_date(v, default):
            return v if isinstance(v, date) else date.fromisoformat(str(v)[:10]) if v else default

        d = as_date(meta.get("date"), date.today())
        updated = as_date(meta.get("updated"), d)
        html_body = md.markdown(m.group(2), extensions=["tables", "fenced_code", "sane_lists", "toc"])
        html_body = re.sub(r"<h1([^>]*)>", r"<h2\1>", html_body).replace("</h1>", "</h2>")
        html_body = html_body.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
        text = re.sub(r"<[^>]+>", " ", html_body)
        toc = [(hid, re.sub(r"<[^>]+>", "", h)) for hid, h in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html_body, re.S)]
        title = str(meta.get("title", f.stem))
        tags = [str(x) for x in (meta.get("tags") or [])]
        cover = meta.get("cover") or ""
        if not cover and covers is not None:
            sig = hashlib.sha1(("v3-light|" + title + "|" + "|".join(tags)).encode()).hexdigest()
            out = ROOT / "assets" / "blog" / f"{f.stem}.jpg"
            if not out.exists() or cache.get(f.stem) != sig:
                covers.make_cover(f.stem, title, tags, out)
                cache[f.stem] = sig
            cover = f"/assets/blog/{f.stem}.jpg"
        cover_abs = cover if str(cover).startswith("http") else (C.BASE + cover if cover else OG_IMAGE)
        posts.append({
            "slug": f.stem, "title": title, "seo_title": str(meta.get("seo_title") or ""), "description": str(meta.get("description", "")),
            "date": d, "updated": updated, "author": str(meta.get("author") or "Texas Solutions Dispatch Team"),
            "tags": tags, "keywords": str(meta.get("keywords") or ""),
            "cover": cover, "cover_abs": cover_abs, "cover_alt": str(meta.get("cover_alt") or title),
            "answer": str(meta.get("answer") or ""), "question": str(meta.get("question") or ""),
            "faq": [(str(x.get("q", "")), str(x.get("a", ""))) for x in (meta.get("faq") or []) if x.get("q")],
            "html": html_body, "md": m.group(2).strip(), "toc": toc, "words": len(text.split()),
        })
    if covers is not None:
        (ROOT / "assets" / "blog").mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    posts.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)
    return posts


def post_card(po, prefix=""):
    cover = (f'<img src="{esc(po["cover"])}" alt="" width="1200" height="630" loading="lazy" decoding="async" class="post-cover">'
             if po["cover"] else '<div class="post-cover post-cover-ph" aria-hidden="true"></div>')
    tags = "".join(f'<span class="tag">{esc(x)}</span>' for x in po["tags"][:2])
    return f"""  <a class="card post-card rv" href="{prefix}blog/{po['slug']}.html">
    {cover}
    <div class="post-meta">{tags}<span>{po['date'].strftime('%b')} {po['date'].day}, {po['date'].year} &middot; {max(1, round(po['words'] / 220))} min read</span></div>
    <h3>{esc(po['title'])}</h3>
    <p>{esc(po['description'][:160])}</p>
    <span class="more">Read article &rarr;</span>
  </a>"""


def post_title_tag(po):
    if po["seo_title"]:
        return po["seo_title"]
    return po["title"] + " | Texas Solutions" if len(po["title"]) + 17 <= 64 else po["title"]


def build_blog():
    posts = load_posts()
    title = "Trucking Blog: Dispatch, Rates, Fuel & Compliance Guides"
    desc = "Practical trucking guides for owner-operators: dispatch costs, rates per mile, diesel prices, fuel cost, MC authority, IFTA, HOS, deadhead and more."
    lead = posts[0] if posts else None
    rest = posts[1:]
    feature = ""
    if lead:
        feature = f"""<a class="post-feature rv" href="blog/{lead['slug']}.html">
    <img src="{esc(lead['cover'])}" alt="" width="1200" height="630" fetchpriority="high" decoding="async">
    <div><span class="tag">{esc(lead['tags'][0]) if lead['tags'] else 'Trucking'}</span><h2>{esc(lead['title'])}</h2>
    <p>{esc(lead['description'])}</p><span class="more">Read the guide &rarr;</span></div></a>"""
    cards = "\n".join(post_card(po) for po in rest) or ""
    body = f"""{phero("Blog", "Trucking Blog", "Straight answers for owner-operators on dispatch costs, rates per mile, diesel prices, compliance and fuel savings.", ctas=False)}
<section class="sec"><div class="wrap">
  {feature}
  <div class="grid g3" style="margin-top:28px">
{cards}
  </div>
</div></section>
{band("Want loads that pay after fuel?", "Our dispatchers negotiate every rate and plan lanes to cut empty miles.")}"""
    schemas = [{"@context": "https://schema.org", "@type": "Blog", "name": "Texas Solutions Trucking Blog", "url": url("/blog.html"),
                "publisher": {"@id": BUSINESS_ID}, "inLanguage": "en-US", "description": desc,
                "blogPost": [{"@type": "BlogPosting", "headline": po["title"], "url": url(f"/blog/{po['slug']}.html"),
                              "datePublished": po["date"].isoformat(), "image": po["cover_abs"],
                              "author": {"@type": "Organization", "name": po["author"]}} for po in posts]},
               {"@context": "https://schema.org", "@type": "CollectionPage"},
               crumbs_ld([("Blog", "/blog.html")])]
    kw = "trucking blog, truck dispatch blog, owner operator tips, diesel prices, fuel cost per mile, hotshot trucking, box truck loads, MC number, IFTA, hours of service, freight factoring"
    write("blog.html", page("/blog.html", title, desc, kw, schemas, body, current="blog.html",
                            image=posts[0]["cover_abs"] if posts else None, image_alt="Texas Solutions trucking blog"))

    (ROOT / "blog").mkdir(exist_ok=True)
    keep = set()
    for po in posts:
        path = f"/blog/{po['slug']}.html"
        keep.add(po["slug"] + ".html")
        mine = set(po["tags"])
        others = [x for x in posts if x["slug"] != po["slug"]]
        others.sort(key=lambda x: (-len(mine & set(x["tags"])), -x["date"].toordinal(), x["slug"]))
        rel = "\n".join(post_card(x) for x in others[:3])
        ans = answer(po.get("question") or "The short answer", po["answer"], "Quick answer") if po["answer"] else ""
        faq_block = f'<h2>Frequently asked questions</h2>\n{faq_html(po["faq"])}' if po["faq"] else ""
        hero = (f'<img src="{esc(po["cover"])}" alt="{esc(po["cover_alt"])}" width="1200" height="630" class="post-hero-img" fetchpriority="high" decoding="async">'
                if po["cover"] else "")
        toc = ""
        if len(po["toc"]) >= 4:
            toc = ('<nav class="toc" aria-label="In this article"><b>In this article</b><ol>' +
                   "".join(f'<li><a href="#{hid}">{esc(h)}</a></li>' for hid, h in po["toc"]) + "</ol></nav>")
        tags = " ".join(f'<span class="chip" >{esc(x)}</span>' for x in po["tags"])
        upd = f' &middot; Updated {po["updated"].strftime("%B")} {po["updated"].day}, {po["updated"].year}' if po["updated"] != po["date"] else ""
        meta_line = (f'<p class="lede" style="font-size:15px">By {esc(po["author"])} &middot; '
                     f'<time datetime="{po["date"].isoformat()}">{po["date"].strftime("%B")} {po["date"].day}, {po["date"].year}</time>{upd} '
                     f'&middot; {max(1, round(po["words"] / 220))} min read</p>')
        body = f"""<section class="phero"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a> / <a href="blog.html">Blog</a></div>
  <h1>{esc(po['title'])}</h1>
  {meta_line}
  <div class="chip-row" style="justify-content:flex-start">{tags}</div>
</div></section>
<section class="sec" style="padding-top:48px"><div class="wrap two">
  <article class="prose post-body">
    {hero}
    {ans}
    {toc}
    {po['html']}
    {faq_block}
    <div class="author-box"><b>About the author</b><p>{esc(po['author'])} at Texas Solutions, a truck dispatch service for owner-operators and small fleets based in {C.CITY}, Texas. We negotiate loads, plan lanes and handle broker paperwork for a percentage of weekly gross: 5% for semis, 8% for hotshots, 10% for box trucks. Rates, fees and rules change, so confirm current figures with the relevant agency or provider before you act.</p></div>
  </article>
  <div class="aside">
    <div class="card"><h3>Free trucking tools</h3><p>Work out your numbers in seconds.</p>
      <a class="btn btn-red" style="width:100%;margin-top:14px" href="truck-fuel-cost-calculator.html">Fuel cost calculator</a>
      <a class="btn btn-dark" style="width:100%;margin-top:10px" href="cost-per-mile-calculator.html">Cost per mile calculator</a>
      <a class="btn btn-line" style="width:100%;margin-top:10px" href="tools.html">All free tools</a></div>
    {contact_side()}
  </div>
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Keep reading</span><h2>More from the blog</h2></div>
  <div class="grid g3">
{rel}
  </div>
</div></section>"""
        art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": po["title"][:110], "description": po["description"],
               "image": [po["cover_abs"]], "datePublished": po["date"].isoformat(), "dateModified": po["updated"].isoformat(),
               "author": {"@type": "Organization", "name": po["author"], "url": url("/")},
               "publisher": {"@id": BUSINESS_ID}, "mainEntityOfPage": {"@id": url(path) + "#webpage"},
               "articleSection": po["tags"][0] if po["tags"] else "Trucking", "keywords": po["keywords"], "wordCount": po["words"],
               "inLanguage": "en-US", "isAccessibleForFree": True}
        schemas = [art, crumbs_ld([("Blog", "/blog.html"), (po["title"], path)]), speakable(path, po["title"])]
        if po["faq"]:
            schemas.append(faq_ld(po["faq"]))
        shell = page(path, post_title_tag(po), po["description"], po["keywords"] or "truck dispatch", schemas, body, current="blog.html",
                     og_type="article", image=po["cover_abs"], image_alt=po["cover_alt"], published=po["date"].isoformat(),
                     modified=po["updated"].isoformat(), tags=po["tags"])
        write(f"blog/{po['slug']}.html", abs_links(shell))
    for old in (ROOT / "blog").glob("*.html"):
        if old.name not in keep:
            old.unlink()
    return posts


def build_state_pages():
    diesel = load_diesel()
    if not diesel:
        return []
    regions, states_p = diesel["regions"], diesel.get("states", {})
    us = regions.get("US", {}).get("price", 0)
    day = diesel.get("day") or diesel.get("week")
    d1 = date.fromisoformat(day)
    day_h = f"{d1.strftime('%B')} {d1.day}, {d1.year}"
    sp = lambda c: states_p.get(c) or regions.get(C.STATE_REGION[c][1], {}).get("price", 0)
    ranked = sorted(C.STATE_REGION, key=sp)
    (ROOT / "diesel-prices").mkdir(exist_ok=True)
    trucks = {tid: (n, e / (1 + k * dflt / 1000), dflt) for tid, n, e, k, mx, dflt, ig, spd in C.FUEL_TRUCKS}
    out = []
    for code, (name, reg) in C.STATE_REGION.items():
        slug = slugify(name)
        path = f"/diesel-prices/{slug}.html"
        out.append((name, path))
        price = sp(code)
        rank = ranked.index(code) + 1
        diff = price - us
        neighbours = sorted([c for c, (_, r) in C.STATE_REGION.items() if r == reg and c != code], key=sp)[:6]
        nb_rows = "".join(f'<tr><td><a href="diesel-prices/{slugify(C.STATE_REGION[c][0])}.html" style="color:var(--ink)">{C.STATE_REGION[c][0]}</a></td><td class="rate">${sp(c):.3f}</td></tr>' for c in neighbours)
        ex = ""
        for tid in ("dry-van", "reefer", "flatbed", "hotshot", "box-truck"):
            n, mpg, w = trucks[tid]
            ex += f"<tr><td><b>{n}</b><small>{w:,} lbs, ~{mpg:.1f} mpg</small></td><td>${price / mpg:.2f}</td><td>${1000 / mpg * price:,.0f}</td></tr>"
        src = "AAA daily state average" if states_p.get(code) else "EIA regional weekly average"
        title = f"Diesel Prices in {name} Today (${price:.2f}/gal)"
        if len(title) <= 42:
            title += " | Fuel Calculator"
        desc = (f"{name} diesel today: ${price:.3f}/gal, ${abs(diff):.3f} {'above' if diff > 0 else 'below'} the ${us:.3f} U.S. average. "
                f"Fuel cost per mile for semi, hotshot and box trucks. Updated daily.")
        qa = (f"What is the price of diesel in {name} today?",
              f"Diesel in {name} averages ${price:.3f} per gallon today ({day_h}), ${abs(diff):.3f} {'more' if diff > 0 else 'less'} than the U.S. average of ${us:.3f}. "
              f"{name} ranks #{rank} of 51 for cheapest diesel (1 = cheapest). A loaded semi at about 6.3 mpg spends about ${price / 6.3:.2f} per mile on fuel in {name}.")
        faqs = [qa,
                (f"How much does it cost to fill a semi truck in {name}?", f"At ${price:.2f} a gallon, 150 gallons of diesel costs about ${150 * price:,.0f} and 200 gallons about ${200 * price:,.0f} in {name} today."),
                (f"Is diesel cheaper in {name} than nearby states?", (f"Among nearby states in the same region, the cheapest today is {C.STATE_REGION[neighbours[0]][0]} at ${sp(neighbours[0]):.3f} a gallon." if neighbours else f"{name} is priced on its own regional market.") + f" {name} is ${price:.3f}."),
                (f"How often are {name} diesel prices updated?", "Every day. This page refreshes each morning from daily state averages, with the EIA weekly survey as a backup.")]
        body = f"""<section class="phero"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a> / <a href="truck-fuel-cost-calculator.html">Fuel Calculator</a> / Diesel prices</div>
  <h1>Diesel Prices in {name} Today</h1>
  <p class="lede">Average diesel price in {name}: <b style="color:var(--ink)">${price:.3f} per gallon</b> on {day_h}. U.S. average ${us:.3f}. Updated daily.</p>
  <div class="ctas"><a class="btn btn-red" href="truck-fuel-cost-calculator.html?state={code}#fuelCalc">Calculate fuel cost in {name}</a><a class="btn btn-wa" href="{WA_URL}" target="_blank" rel="noopener">{ICONS['wa']}Talk to a dispatcher</a></div>
</div></section>
<section class="sec" style="padding-bottom:0"><div class="wrap">{answer(*qa, label=f"Diesel price in {name}")}</div></section>
<section class="sec"><div class="wrap">
  <div class="grid g4 stat-row">
    <div class="card"><span class="eyebrow">{name} diesel</span><div class="stat">${price:.3f}</div><p>per gallon today</p></div>
    <div class="card"><span class="eyebrow">vs U.S. average</span><div class="stat {'up' if diff > 0 else 'down'}">{'+' if diff >= 0 else '-'}${abs(diff):.3f}</div><p>U.S. average ${us:.3f}</p></div>
    <div class="card"><span class="eyebrow">Rank</span><div class="stat">#{rank}</div><p>of 51 (1 = cheapest)</p></div>
    <div class="card"><span class="eyebrow">150-gallon fill</span><div class="stat">${150 * price:,.0f}</div><p>semi truck, today</p></div>
  </div>
</div></section>
<section class="sec sec-soft"><div class="wrap two">
  <div class="prose rv">
    <h2 style="margin-top:0">Fuel cost per mile in {name}</h2>
    <p>Estimated diesel cost at today's {name} price of ${price:.3f} a gallon, using fuel economy calibrated to FHWA and NACFE data.</p>
    <div class="tbl"><table><thead><tr><th>Truck</th><th>Fuel per mile</th><th>Fuel per 1,000 miles</th></tr></thead><tbody>{ex}</tbody></table></div>
    <p>Your numbers depend on load weight, speed, terrain and idling. Enter them in the <a href="truck-fuel-cost-calculator.html?state={code}#fuelCalc">truck fuel cost calculator</a> for an exact estimate.</p>
    <h2>Frequently asked questions</h2>
    {faq_html(faqs)}
  </div>
  <div class="aside">
    <div class="board"><div class="board-head"><b>Nearby states</b><span>$/gal today</span></div>
      <table class="board-table"><tbody>{nb_rows}</tbody></table>
      <p class="board-foot">Source: {src}, {day_h}. <a href="truck-fuel-cost-calculator.html#diesel-prices" style="color:var(--red-600)">All 50 states</a></p></div>
    {contact_side()}
  </div>
</div></section>
{band(f"Running freight through {name}?", "Texas Solutions dispatches semis for 5%, hotshots for 8% and box trucks for 10% of weekly gross. We plan lanes to cut empty miles and fuel.")}"""
        schemas = [faq_ld(faqs), crumbs_ld([("Fuel Calculator", "/truck-fuel-cost-calculator.html"), (f"Diesel prices in {name}", path)]),
                   speakable(path, title),
                   {"@context": "https://schema.org", "@type": "Dataset", "name": f"Diesel prices in {name}",
                    "description": f"Daily average retail diesel price per gallon in {name}, in US dollars, updated every day.", "url": url(path),
                    "dateModified": day, "temporalCoverage": day, "spatialCoverage": {"@type": "Place", "name": f"{name}, United States"},
                    "isBasedOn": "https://gasprices.aaa.com/state-gas-price-averages/", "isAccessibleForFree": True, "inLanguage": "en-US",
                    "variableMeasured": "Retail diesel price, USD per gallon", "creator": {"@id": BUSINESS_ID}, "publisher": {"@id": BUSINESS_ID}}]
        kw = (f"diesel prices {name.lower()}, diesel price in {name.lower()} today, {name.lower()} diesel price per gallon, "
              f"cheapest diesel {name.lower()}, {name.lower()} fuel prices, truck fuel cost {name.lower()}, fuel prices near me")
        write(f"diesel-prices/{slug}.html", abs_links(page(path, title, desc, kw, schemas, body, current="truck-fuel-cost-calculator.html")))
    return out


# ==================================================================
# Free trucking tools (calculators): hub + 11 individual pages.
# Two more tools (dispatch fee, fuel cost) already exist as their own
# pages (estimate.html, truck-fuel-cost-calculator.html) and are listed
# on the hub alongside these.
# ==================================================================

TOOL_ICONS = {
    "cpm": "calc", "lp": "cash", "be": "route", "dh": "route", "dp": "cash",
    "ifta": "doc", "pd": "doc", "tl": "cash", "mb": "clock", "hos": "clock", "fc": "doc",
}


def related_tools(current):
    others = [t for t in TOOLS if t["slug"] != current]
    # A short, fixed rotation so links stay stable and relevant.
    pick = {
        "cost-per-mile-calculator": ["load-profitability-calculator", "break-even-calculator", "truck-fuel-cost-calculator"],
        "load-profitability-calculator": ["cost-per-mile-calculator", "deadhead-miles-calculator", "estimate"],
        "break-even-calculator": ["cost-per-mile-calculator", "load-profitability-calculator", "driver-pay-calculator"],
        "deadhead-miles-calculator": ["load-profitability-calculator", "cost-per-mile-calculator", "truck-fuel-cost-calculator"],
        "driver-pay-calculator": ["cost-per-mile-calculator", "break-even-calculator", "per-diem-calculator"],
        "ifta-mileage-calculator": ["truck-fuel-cost-calculator", "cost-per-mile-calculator", "deadhead-miles-calculator"],
        "per-diem-calculator": ["driver-pay-calculator", "truck-loan-calculator", "cost-per-mile-calculator"],
        "truck-loan-calculator": ["cost-per-mile-calculator", "break-even-calculator", "per-diem-calculator"],
        "maintenance-budget-calculator": ["cost-per-mile-calculator", "break-even-calculator", "truck-loan-calculator"],
        "hours-of-service-calculator": ["driver-pay-calculator", "deadhead-miles-calculator", "estimate"],
        "freight-class-calculator": ["load-profitability-calculator", "cost-per-mile-calculator", "estimate"],
    }.get(current, [t["slug"] for t in others[:3]])
    cards = []
    special = {"estimate": ("Dispatch Fee Calculator", "See your weekly dispatch fee by truck type.", "calc"),
               "truck-fuel-cost-calculator": ("Truck Fuel Cost Calculator", "MPG, fuel cost per mile and diesel prices by state.", "truck")}
    for slug in pick:
        if slug in special:
            name, desc, icon = special[slug]
            file = slug + ".html"
        else:
            t = next(x for x in TOOLS if x["slug"] == slug)
            name, desc, icon, file = t["hub_title"], t["hub_desc"], TOOL_ICONS[t["prefix"]], t["slug"] + ".html"
        cards.append(f"""  <a class="card tool-mini rv" href="{file}"><div class="icon">{ICONS[icon]}</div><div><b>{esc(name)}</b><p>{esc(desc)}</p></div></a>""")
    return "\n".join(cards)


def tool_wrap(t):
    calc = t["calc_html"]
    faqs = t["faqs"]
    body = f"""{phero("Tools", t["h1"], t["lede"], ctas=False)}
<section class="sec" style="padding-top:48px"><div class="wrap">
  {calc}
</div></section>
<section class="sec sec-soft"><div class="wrap two">
  <div class="prose rv">
    {answer("What does the " + t["hub_title"] + " do?", t["desc"])}
{t["article_html"]}
    <h2>Frequently asked questions</h2>
    {faq_html(faqs)}
  </div>
  <div class="aside">{contact_side()}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">More free tools</span><h2>Related calculators</h2></div>
  <div class="grid g3">
{related_tools(t["slug"])}
  </div>
</div></section>
{band()}"""
    path = "/" + t["slug"] + ".html"
    schemas = [
        faq_ld(faqs), crumbs_ld([("Tools", "/tools.html"), (t["hub_title"], path)]), speakable(path, t["meta_title"]),
    ]
    kw = t["keywords"] + ", free trucking calculator, owner operator tools"
    write(t["slug"] + ".html", page(path, t["meta_title"], t["desc"], kw, schemas, body, current="tools.html"))


def build_tools():
    for t in TOOLS:
        tool_wrap(t)


def build_tools_hub():
    existing = [
        ("estimate.html", "Dispatch Fee Calculator", "See your weekly dispatch fee by truck type: semi 5%, hotshot 8%, box truck 10%.", "calc"),
        ("truck-fuel-cost-calculator.html", "Truck Fuel Cost Calculator", "MPG by truck type and load weight, trip fuel cost, and diesel prices for all 50 states.", "truck"),
    ]
    cards = []
    n = 1
    for file, name, desc, icon in existing:
        cards.append(f"""  <a class="tool-num-card rv" href="{file}"><span class="tool-num">TOOL.{n:02d}</span><div class="icon">{ICONS[icon]}</div><h3>{esc(name)}</h3><p>{esc(desc)}</p><span class="more">Open tool &rarr;</span></a>""")
        n += 1
    for t in TOOLS:
        cards.append(f"""  <a class="tool-num-card rv" href="{t['slug']}.html"><span class="tool-num">TOOL.{n:02d}</span><div class="icon">{ICONS[TOOL_ICONS[t['prefix']]]}</div><h3>{esc(t['hub_title'])}</h3><p>{esc(t['hub_desc'])}</p><span class="more">Open tool &rarr;</span></a>""")
        n += 1
    title = "Free Trucking Calculators: Dispatch, Fuel, CPM, IFTA, HOS & More | Texas Solutions"
    desc = "Free calculators for owner-operators and small fleets: dispatch fee, fuel cost, cost per mile, load profitability, break-even, deadhead miles, driver pay, IFTA mileage, per diem, truck loan, maintenance budget, HOS and freight class."
    body = f"""{phero("Tools", "Free Trucking Calculators", "Work out your numbers before you book: dispatch fees, fuel cost, cost per mile, IFTA mileage, HOS hours and more. Nothing is stored, nothing is emailed.", ctas=False)}
<section class="sec"><div class="wrap">
  <div class="grid g3">
{chr(10).join(cards)}
  </div>
</div></section>
{band("Want a dispatcher who knows these numbers too?", "We negotiate every rate and plan lanes with your cost per mile in mind, not just the headline rate.")}"""
    schemas = [{"@context": "https://schema.org", "@type": "ItemList", "name": "Free trucking calculators", "url": url("/tools.html"),
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": (existing[i][1] if i < 2 else TOOLS[i - 2]["hub_title"]), "url": url("/" + (existing[i][0] if i < 2 else TOOLS[i - 2]["slug"] + ".html"))}
                                     for i in range(len(existing) + len(TOOLS))]},
               crumbs_ld([("Tools", "/tools.html")])]
    kw = "trucking calculators, owner operator calculators, free trucking tools, IFTA calculator, HOS calculator, cost per mile calculator, truck loan calculator, per diem calculator, freight class calculator"
    write("tools.html", page("/tools.html", title, desc, kw, schemas, body, current="tools.html", page_type="CollectionPage"))


TOOLS = [
    # -------------------------------------------------- Cost Per Mile
    {
        "slug": "cost-per-mile-calculator", "prefix": "cpm",
        "hub_title": "Cost Per Mile (CPM) Calculator", "hub_desc": "Your true operating cost per mile from fixed and variable costs.",
        "meta_title": "Cost Per Mile Calculator for Trucking (CPM) | Texas Solutions",
        "desc": "Free cost per mile (CPM) calculator for owner-operators: combine truck payment, insurance, permits, fuel, maintenance and driver pay into your true cost per mile.",
        "keywords": "cost per mile calculator, trucking cost per mile, CPM calculator, operating cost per mile, owner operator cost per mile",
        "h1": "Cost Per Mile (CPM) Calculator",
        "lede": "Your true cost to run one mile: fixed costs plus fuel, maintenance and driver pay. Know this before you accept a rate.",
        "calc_html": """<div class="est rv" id="cpmCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Monthly fixed costs</h2>
    <div class="grid g2" style="gap:14px;margin-top:16px">
      <div><label class="flabel" for="cpmPayment">Truck/trailer payment ($/mo)</label><input class="pct-in" type="number" id="cpmPayment" min="0" step="10" value="1800" inputmode="numeric"></div>
      <div><label class="flabel" for="cpmInsurance">Insurance ($/mo)</label><input class="pct-in" type="number" id="cpmInsurance" min="0" step="10" value="600" inputmode="numeric"></div>
      <div><label class="flabel" for="cpmPermits">Permits, licensing &amp; ELD ($/mo)</label><input class="pct-in" type="number" id="cpmPermits" min="0" step="10" value="150" inputmode="numeric"></div>
      <div><label class="flabel" for="cpmOtherFixed">Other fixed costs ($/mo)</label><input class="pct-in" type="number" id="cpmOtherFixed" min="0" step="10" value="100" inputmode="numeric"></div>
    </div>
    <h2 style="font-size:26px;margin-top:28px">Variable costs (per mile)</h2>
    <div class="grid g2" style="gap:14px;margin-top:16px">
      <div><label class="flabel" for="cpmFuel">Fuel cost ($/mi)</label><input class="pct-in" type="number" id="cpmFuel" min="0" step="0.01" value="0.65" inputmode="decimal"><p class="hint">From the <a href="truck-fuel-cost-calculator.html">fuel cost calculator</a>, or your own number.</p></div>
      <div><label class="flabel" for="cpmMaint">Maintenance &amp; tires ($/mi)</label><input class="pct-in" type="number" id="cpmMaint" min="0" step="0.01" value="0.18" inputmode="decimal"></div>
      <div><label class="flabel" for="cpmDriverPay">Driver pay ($/mi)</label><input class="pct-in" type="number" id="cpmDriverPay" min="0" step="0.01" value="0.55" inputmode="decimal"><p class="hint">0 if you are the only driver and count your own pay separately.</p></div>
      <div><label class="flabel" for="cpmMiles">Miles per month</label><input class="pct-in" type="number" id="cpmMiles" min="1" step="100" value="9000" inputmode="numeric"></div>
    </div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Your cost per mile</h3>
    <div class="est-big" id="cpmBig">$0.00<small>per mile, all-in</small></div>
    <div class="est-lines">
      <div><span>Fixed costs, monthly</span><b id="cpmFixedTotal">-</b></div>
      <div><span>Fixed cost per mile</span><b id="cpmFixedPerMi">-</b></div>
      <div><span>Variable cost per mile</span><b id="cpmVarPerMi">-</b></div>
      <div><span>Total operating cost, monthly</span><b id="cpmMonthlyTotal">-</b></div>
    </div>
    <a class="btn btn-red" href="load-profitability-calculator.html">Check a load's profit</a>
    <a class="btn btn-dark" href="break-even-calculator.html">Find my break-even rate</a>
    <small>Rough estimate. Add your own numbers for an exact figure; costs vary by truck, lane and season.</small>
  </div>
</div>""",
        "faqs": [
            ("What is cost per mile (CPM) in trucking?", "Cost per mile is your total operating cost divided by miles driven: fixed costs (truck payment, insurance, permits) divided by monthly miles, plus variable costs (fuel, maintenance, driver pay) per mile. It is the number you compare against a load's rate per mile to see if it is worth running."),
            ("What is a good cost per mile for an owner-operator?", "It depends heavily on the truck, lane and driver pay structure. Many owner-operators run somewhere between $1.50 and $2.00 all-in cost per mile. Use your own numbers in the calculator rather than a rule of thumb, since fuel, insurance and payment amounts vary widely."),
            ("Does cost per mile include driver pay?", "It should if you want your true break-even rate. If you are an owner-operator driving your own truck, either include a driver-pay line for your own labor or track it separately and make sure you are not comparing rates against a number that ignores your own time."),
        ],
        "article_html": """    <h2 style="margin-top:0">How cost per mile is calculated</h2>
    <p>Split your costs into two groups. <b>Fixed costs</b> happen whether you drive 500 miles or 15,000 miles that month: your truck payment, insurance, permits and ELD subscription. <b>Variable costs</b> scale with miles driven: fuel, maintenance, tires and driver pay.</p>
    <ul>
      <li>Fixed cost per mile = total monthly fixed costs &divide; miles driven that month</li>
      <li>Variable cost per mile = fuel + maintenance + driver pay, all per mile</li>
      <li>Cost per mile (CPM) = fixed cost per mile + variable cost per mile</li>
    </ul>
    <p>Fixed cost per mile falls as you drive more miles in a month, since the same truck payment is spread over more miles. That is why a truck sitting idle costs more per mile than a truck running hard.</p>""",
    },
    # -------------------------------------------------- Load Profitability
    {
        "slug": "load-profitability-calculator", "prefix": "lp",
        "hub_title": "Load Profitability Calculator", "hub_desc": "Weigh the rate against fuel, driver pay and other costs before you book.",
        "meta_title": "Load Profitability Calculator: Is This Load Worth Taking? | Texas Solutions",
        "desc": "Free load profitability calculator: enter the rate, miles, deadhead and your cost per mile to see net profit, margin and effective rate per mile before you book a load.",
        "keywords": "load profitability calculator, is this load worth taking, trucking profit calculator, net profit per load, effective rate per mile",
        "h1": "Load Profitability Calculator",
        "lede": "Rate, miles, deadhead and cost per mile in; net profit and margin out. Know before you book, not after you deliver.",
        "calc_html": """<div class="est rv" id="lpCalc">
  <div class="est-in">
    <h2 style="font-size:26px">This load</h2>
    <div class="grid g2" style="gap:14px;margin-top:16px">
      <div><label class="flabel" for="lpRate">Load rate / total pay ($)</label><input class="pct-in" type="number" id="lpRate" min="0" step="10" value="3000" inputmode="numeric"></div>
      <div><label class="flabel" for="lpLoaded">Loaded miles</label><input class="pct-in" type="number" id="lpLoaded" min="1" step="1" value="600" inputmode="numeric"></div>
      <div><label class="flabel" for="lpDeadhead">Deadhead miles (to pickup)</label><input class="pct-in" type="number" id="lpDeadhead" min="0" step="1" value="50" inputmode="numeric"></div>
      <div><label class="flabel" for="lpOther">Tolls, lumper, scale fees ($)</label><input class="pct-in" type="number" id="lpOther" min="0" step="5" value="0" inputmode="numeric"></div>
      <div class="full"><label class="flabel" for="lpCpm">Your cost per mile ($/mi, all-in)</label><input class="pct-in" type="number" id="lpCpm" min="0" step="0.01" value="1.85" inputmode="decimal"><p class="hint">Get this from the <a href="cost-per-mile-calculator.html">cost per mile calculator</a>.</p></div>
    </div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Net profit on this load</h3>
    <div class="est-big" id="lpBig">$0<small>net profit</small></div>
    <div class="est-lines">
      <div><span>Total miles (loaded + deadhead)</span><b id="lpTotalMi">-</b></div>
      <div><span>Total cost for this load</span><b id="lpTotalCost">-</b></div>
      <div><span>Profit margin</span><b id="lpMargin">-</b></div>
      <div><span>Rate per loaded mile</span><b id="lpRatePerLoaded">-</b></div>
      <div><span>Rate per total mile</span><b id="lpRatePerTotal">-</b></div>
    </div>
    <a class="btn btn-red" href="deadhead-miles-calculator.html">Check deadhead impact</a>
    <a class="btn btn-wa" href="__WA__" target="_blank" rel="noopener">__WA_ICON__Ask a dispatcher</a>
    <small>Rough estimate. Actual profit depends on fuel prices, detention, and costs not entered here.</small>
  </div>
</div>""",
        "faqs": [
            ("How do I know if a load is profitable?", "Add up the total cost to run the load (your cost per mile times total miles, plus tolls, lumper or scale fees) and subtract it from the rate. If the result is positive and the margin looks reasonable after accounting for time, the load is profitable; if it is thin or negative, it likely is not worth it unless it repositions you for a better load."),
            ("Should deadhead miles count against a load's profit?", "Yes. Deadhead miles cost fuel and time just like loaded miles, so they should be included in your total miles when working out true cost and effective rate per mile."),
            ("What profit margin should I target per load?", "There is no universal number; it depends on your fixed costs, how often you run, and what alternative loads are available. Compare the margin here against your other options rather than a fixed target."),
        ],
        "article_html": """    <h2 style="margin-top:0">How load profit is calculated</h2>
    <ul>
      <li>Total miles = loaded miles + deadhead miles</li>
      <li>Total cost = (cost per mile &times; total miles) + tolls, lumper and scale fees</li>
      <li>Net profit = load rate &minus; total cost</li>
      <li>Profit margin = net profit &divide; load rate &times; 100</li>
    </ul>
    <p>Two rates matter more than the headline number: <b>rate per loaded mile</b>, which is what brokers usually quote, and <b>rate per total mile</b>, which includes the deadhead it took to get there. A load that looks good per loaded mile can be mediocre once deadhead is counted.</p>""",
    },
    # -------------------------------------------------- Break-Even
    {
        "slug": "break-even-calculator", "prefix": "be",
        "hub_title": "Break-Even Calculator", "hub_desc": "How many miles a month you need to cover costs, and the rate that gets you there.",
        "meta_title": "Truck Break-Even Calculator: Miles & Rate to Cover Costs | Texas Solutions",
        "desc": "Free break-even calculator for owner-operators: enter fixed costs, variable cost per mile and your freight rate to see the miles per month you need to break even, and your profit at your planned miles.",
        "keywords": "break even calculator trucking, break even miles per month, owner operator break even rate, minimum rate per mile",
        "h1": "Break-Even Calculator",
        "lede": "The miles you need to run each month just to cover your costs, and the rate that gets you there.",
        "calc_html": """<div class="est rv" id="beCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Your costs and rate</h2>
    <div class="field"><label class="flabel" for="beFixed">Fixed costs per month ($)</label><input class="pct-in" type="number" id="beFixed" min="0" step="10" value="2650" inputmode="numeric"><p class="hint">Truck payment, insurance, permits. From the <a href="cost-per-mile-calculator.html">CPM calculator</a>.</p></div>
    <div class="field"><label class="flabel" for="beVar">Variable cost per mile ($/mi)</label><input class="pct-in" type="number" id="beVar" min="0" step="0.01" value="0.73" inputmode="decimal"><p class="hint">Fuel, maintenance and driver pay per mile.</p></div>
    <div class="field"><label class="flabel" for="beRate">Average freight rate ($/mi)</label><input class="pct-in" type="number" id="beRate" min="0" step="0.01" value="1.85" inputmode="decimal"></div>
    <div class="field"><label class="flabel" for="beMiles">Your planned miles per month</label><input class="pct-in" type="number" id="beMiles" min="0" step="100" value="9000" inputmode="numeric"></div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Break-even miles per month</h3>
    <div class="est-big" id="beBig">0<small>miles / month</small></div>
    <div class="est-lines">
      <div><span>Break-even miles per week</span><b id="beWeekly">-</b></div>
      <div><span>Profit per mile above break-even</span><b id="beMargin">-</b></div>
      <div><span>Profit at your planned miles</span><b id="bePlannedProfit">-</b></div>
    </div>
    <p class="form-status err" id="beWarn" style="display:none">At this rate, your variable cost per mile is the same or more than what you are paid per mile. You cannot break even by driving more; raise your rate or cut costs.</p>
    <a class="btn btn-red" href="load-profitability-calculator.html">Check a single load</a>
    <small>Rough estimate based on the numbers you enter.</small>
  </div>
</div>""",
        "faqs": [
            ("How many miles does an owner-operator need to break even?", "It depends on fixed costs and the gap between your freight rate and variable cost per mile. Divide fixed costs by (rate minus variable cost per mile) to get break-even miles for the month. Enter your own numbers above for your figure."),
            ("What is the minimum rate per mile to break even?", "The minimum rate equals your variable cost per mile plus fixed costs divided by the miles you plan to run. Running more miles lowers the minimum rate needed, because fixed costs are spread over more miles."),
            ("What if my variable cost is higher than my rate?", "Then every mile loses money before fixed costs are even considered, and driving more miles makes the loss bigger, not smaller. The fix is a higher rate or lower variable costs (fuel, maintenance), not more miles."),
        ],
        "article_html": """    <h2 style="margin-top:0">How break-even is calculated</h2>
    <ul>
      <li>Contribution per mile = freight rate &minus; variable cost per mile</li>
      <li>Break-even miles per month = fixed costs &divide; contribution per mile</li>
      <li>Profit at your planned miles = (contribution per mile &times; planned miles) &minus; fixed costs</li>
    </ul>
    <p>Below break-even miles, you are still losing money on fixed costs even though each mile driven brings in more than it costs. Above break-even, every extra mile is profit at your current rate.</p>""",
    },
    # -------------------------------------------------- Deadhead Miles
    {
        "slug": "deadhead-miles-calculator", "prefix": "dh",
        "hub_title": "Deadhead Miles Calculator", "hub_desc": "See how empty miles drag down your real rate per mile.",
        "meta_title": "Deadhead Miles Calculator: Effective Rate Per Mile | Texas Solutions",
        "desc": "Free deadhead miles calculator: see your deadhead percentage and effective rate per mile once empty miles are counted against a load's revenue.",
        "keywords": "deadhead miles calculator, empty miles trucking, effective rate per mile, deadhead percentage",
        "h1": "Deadhead Miles Calculator",
        "lede": "The rate a broker quotes is per loaded mile. Here is what you actually earn once deadhead is counted.",
        "calc_html": """<div class="est rv" id="dhCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Loaded vs. deadhead</h2>
    <div class="field"><label class="flabel" for="dhLoaded">Loaded miles</label><input class="pct-in" type="number" id="dhLoaded" min="1" step="1" value="550" inputmode="numeric"></div>
    <div class="field"><label class="flabel" for="dhDead">Deadhead (empty) miles</label><input class="pct-in" type="number" id="dhDead" min="0" step="1" value="80" inputmode="numeric"></div>
    <div class="field"><label class="flabel" for="dhRevenue">Load revenue ($)</label><input class="pct-in" type="number" id="dhRevenue" min="0" step="10" value="1900" inputmode="numeric"></div>
    <div class="field"><label class="flabel" for="dhCpm">Your operating cost per mile ($/mi, optional)</label><input class="pct-in" type="number" id="dhCpm" min="0" step="0.01" placeholder="e.g. 1.85" inputmode="decimal"></div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Deadhead impact</h3>
    <div class="est-big" id="dhBig">0%<small>deadhead miles</small></div>
    <div class="est-lines">
      <div><span>Total miles</span><b id="dhTotalMi">-</b></div>
      <div><span>Quoted rate (per loaded mile)</span><b id="dhQuoted">-</b></div>
      <div><span>Effective rate (all miles)</span><b id="dhEffective">-</b></div>
      <div><span>Lost to deadhead</span><b id="dhLost">-</b></div>
      <div id="dhProfitRow" style="display:none"><span>Profit after costs</span><b id="dhProfit">-</b></div>
    </div>
    <a class="btn btn-red" href="load-profitability-calculator.html">Full load profit calculator</a>
    <small>Rough estimate. Planning your next load before this one delivers is the main way to cut deadhead.</small>
  </div>
</div>""",
        "faqs": [
            ("What is a good deadhead percentage for trucking?", "Many fleets target under 10-15% deadhead, though it varies by lane and equipment type. The lower the better, since deadhead miles burn fuel and time with no revenue."),
            ("What is the difference between quoted rate and effective rate?", "The quoted rate is revenue divided by loaded miles only, which is how brokers usually post a load. The effective rate is revenue divided by total miles including deadhead, which is what you actually earn per mile driven."),
            ("How can I reduce deadhead miles?", "Plan your next load before the current one delivers, work with a dispatcher who plans lanes around your position, and avoid areas with little return freight unless the rate accounts for it."),
        ],
        "article_html": """    <h2 style="margin-top:0">How deadhead impact is calculated</h2>
    <ul>
      <li>Deadhead % = deadhead miles &divide; total miles &times; 100</li>
      <li>Quoted rate = revenue &divide; loaded miles</li>
      <li>Effective rate = revenue &divide; total miles (loaded + deadhead)</li>
      <li>Lost to deadhead = quoted rate &minus; effective rate, per mile</li>
    </ul>
    <p>A load that pays $3.00 a loaded mile can drop well below $2.50 once 80 empty miles are added in. Always compare loads on effective rate, not the quoted rate alone.</p>""",
    },
    # -------------------------------------------------- Driver Pay
    {
        "slug": "driver-pay-calculator", "prefix": "dp",
        "hub_title": "Driver Pay Calculator", "hub_desc": "Weekly, monthly and annual pay across per-mile, per-load, percentage or hourly.",
        "meta_title": "Truck Driver Pay Calculator: Per-Mile, Per-Load, % or Hourly | Texas Solutions",
        "desc": "Free truck driver pay calculator: work out weekly, monthly and annual pay for per-mile, per-load, percentage of gross, or hourly pay models.",
        "keywords": "truck driver pay calculator, per mile pay calculator, driver percentage pay calculator, trucking salary calculator",
        "h1": "Driver Pay Calculator",
        "lede": "Compare what a driving job actually pays across per-mile, per-load, percentage or hourly pay, weekly, monthly and for the year.",
        "calc_html": """<div class="est rv" id="dpCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Pay model</h2>
    <div class="seg seg-4" role="radiogroup" aria-label="Pay model">
      <label><input type="radio" name="dpModel" value="mile" checked><b>Per mile</b><span>Cents per mile</span></label>
      <label><input type="radio" name="dpModel" value="load"><b>Per load</b><span>Flat pay per load</span></label>
      <label><input type="radio" name="dpModel" value="pct"><b>Percentage</b><span>% of gross revenue</span></label>
      <label><input type="radio" name="dpModel" value="hour"><b>Hourly</b><span>Hourly rate</span></label>
    </div>
    <div class="grid g2 dp-group" data-model="mile" style="gap:14px;margin-top:20px">
      <div><label class="flabel" for="dpRateMile">Rate per mile ($)</label><input class="pct-in" type="number" id="dpRateMile" min="0" step="0.01" value="0.60" inputmode="decimal"></div>
      <div><label class="flabel" for="dpMilesWk">Miles per week</label><input class="pct-in" type="number" id="dpMilesWk" min="0" step="10" value="2400" inputmode="numeric"></div>
    </div>
    <div class="grid g2 dp-group" data-model="load" style="gap:14px;margin-top:20px;display:none">
      <div><label class="flabel" for="dpPayLoad">Pay per load ($)</label><input class="pct-in" type="number" id="dpPayLoad" min="0" step="5" value="350" inputmode="numeric"></div>
      <div><label class="flabel" for="dpLoadsWk">Loads per week</label><input class="pct-in" type="number" id="dpLoadsWk" min="0" step="1" value="4" inputmode="numeric"></div>
    </div>
    <div class="grid g2 dp-group" data-model="pct" style="gap:14px;margin-top:20px;display:none">
      <div><label class="flabel" for="dpGrossWk">Gross revenue per week ($)</label><input class="pct-in" type="number" id="dpGrossWk" min="0" step="50" value="4000" inputmode="numeric"></div>
      <div><label class="flabel" for="dpPct">Your percentage (%)</label><input class="pct-in" type="number" id="dpPct" min="0" max="100" step="0.5" value="25" inputmode="decimal"></div>
    </div>
    <div class="grid g2 dp-group" data-model="hour" style="gap:14px;margin-top:20px;display:none">
      <div><label class="flabel" for="dpHourly">Hourly rate ($)</label><input class="pct-in" type="number" id="dpHourly" min="0" step="0.5" value="22" inputmode="decimal"></div>
      <div><label class="flabel" for="dpHoursWk">Hours per week</label><input class="pct-in" type="number" id="dpHoursWk" min="0" step="1" value="55" inputmode="numeric"></div>
    </div>
    <div class="field"><label class="flabel" for="dpWeeks">Weeks worked per year</label><input class="pct-in" type="number" id="dpWeeks" min="1" max="52" step="1" value="50" inputmode="numeric"><p class="hint">52 minus time off for home, holidays or downtime.</p></div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Estimated pay</h3>
    <div class="est-big" id="dpBig">$0<small>per week</small></div>
    <div class="est-lines">
      <div><span>Monthly (average)</span><b id="dpMonthly">-</b></div>
      <div><span>Annual, at your weeks worked</span><b id="dpAnnual">-</b></div>
    </div>
    <a class="btn btn-red" href="cost-per-mile-calculator.html">See operating cost per mile</a>
    <small>Estimate only. Actual pay varies with freight availability, breakdowns and home time.</small>
  </div>
</div>""",
        "faqs": [
            ("What is the difference between per-mile and percentage pay?", "Per-mile pay is a fixed rate for every mile driven, so it does not change with freight rates. Percentage pay is a share of what the load actually earns, so it moves with the market: higher in strong freight, lower when rates soften."),
            ("How much do truck drivers make per year?", "It depends heavily on pay model, miles or loads run, and weeks worked. Use your own numbers above rather than a national average, since regional pay, equipment type and experience all change the figure."),
            ("Is percentage pay or per-mile pay better?", "Neither is universally better. Percentage pay can pay more when freight rates are strong and less when they are weak; per-mile pay is steadier. Compare both against your own typical gross revenue and miles."),
        ],
        "article_html": """    <h2 style="margin-top:0">How driver pay is calculated</h2>
    <ul>
      <li>Per mile: rate per mile &times; miles per week</li>
      <li>Per load: pay per load &times; loads per week</li>
      <li>Percentage: gross revenue per week &times; your percentage</li>
      <li>Hourly: hourly rate &times; hours per week</li>
    </ul>
    <p>Monthly pay uses a 4.33-week average month; annual pay multiplies weekly pay by the weeks you actually plan to work, not all 52, so time off is reflected in the yearly number.</p>""",
    },
    # -------------------------------------------------- IFTA
    {
        "slug": "ifta-mileage-calculator", "prefix": "ifta",
        "hub_title": "IFTA Mileage Calculator", "hub_desc": "Miles and fuel by state for your own IFTA records.",
        "meta_title": "IFTA Mileage Calculator: Miles & Fuel by State | Texas Solutions",
        "desc": "Free IFTA mileage calculator: log miles driven and fuel purchased by state, see gallons consumed per jurisdiction, and estimate net taxable gallons for your own IFTA records.",
        "keywords": "IFTA calculator, IFTA mileage calculator, IFTA fuel tax calculator, IFTA miles by state",
        "h1": "IFTA Mileage Calculator",
        "lede": "Log miles driven and fuel bought by state to see gallons consumed, net taxable gallons and a quarter's worth of totals in one place.",
        "calc_html": """<div class="est rv" id="iftaCalc" data-states='__STATES__'>
  <div class="est-in" style="max-width:none">
    <h2 style="font-size:26px">Miles and fuel by state</h2>
    <div class="field" style="max-width:280px"><label class="flabel" for="iftaMpg">Average fleet MPG</label><input class="pct-in" type="number" id="iftaMpg" min="1" step="0.1" value="6.3" inputmode="decimal"><p class="hint">From the <a href="truck-fuel-cost-calculator.html">fuel cost calculator</a>, or your own average.</p></div>
    <div style="overflow-x:auto;margin-top:18px"><table class="tbl ifta-table" id="iftaTable">
      <thead><tr><th>State</th><th>Miles driven</th><th>Gallons purchased</th><th>Tax rate paid ($/gal, optional)</th><th></th></tr></thead>
      <tbody id="iftaRows"></tbody>
      <tfoot><tr class="ifta-total"><td>Total</td><td id="iftaTotalMiles">0</td><td id="iftaTotalPurchased">0</td><td></td><td></td></tr></tfoot>
    </table></div>
    <button class="btn btn-line" type="button" id="iftaAddRow" style="margin-top:14px">+ Add a state</button>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Fleet totals</h3>
    <div class="est-big" id="iftaBig">0<small>net taxable gallons</small></div>
    <div class="est-lines">
      <div><span>Total miles</span><b id="iftaMi">-</b></div>
      <div><span>Gallons consumed (from MPG)</span><b id="iftaConsumed">-</b></div>
      <div><span>Gallons purchased</span><b id="iftaPurchased">-</b></div>
      <div><span>Estimated net tax / credit</span><b id="iftaTax">-</b></div>
    </div>
    <small>For your own mileage records only. IFTA tax rates change every quarter by jurisdiction. Enter your own current rate per state if you want a dollar estimate, or leave it blank to just see mileage and gallons. This is not a substitute for your official IFTA return.</small>
  </div>
</div>""",
        "faqs": [
            ("What is IFTA?", "The International Fuel Tax Agreement (IFTA) is how most US states and Canadian provinces share fuel tax collected from carriers that operate across state lines. Carriers file a quarterly return reporting miles driven and fuel purchased in each jurisdiction."),
            ("How is net taxable gallons calculated?", "For each state: gallons consumed = miles driven in that state divided by your fleet's average MPG. Net taxable gallons = gallons consumed minus gallons purchased in that state. A positive number means you owe tax there; a negative number is typically a credit."),
            ("Does this calculator use current IFTA tax rates?", "No. IFTA tax rates are set per jurisdiction and change every quarter, so this tool does not hardcode them. Enter your own current rate per state (from your IFTA quarterly rate matrix) if you want a dollar estimate, or use the tool for mileage and gallons only."),
            ("Does this replace my IFTA filing?", "No. This is a planning and record-keeping aid only. File your official IFTA return using your base jurisdiction's forms and current rates."),
        ],
        "article_html": """    <h2 style="margin-top:0">How this calculator works</h2>
    <p>Add a row for every state you drove in during the quarter, with the miles driven there. Gallons consumed per state is calculated from your average fleet MPG. If you also log gallons purchased in that state, the tool shows net taxable gallons: positive means you burned more fuel there than you bought, negative means you bought more than you burned.</p>
    <p>Tax rates are not built in because they are set per jurisdiction and change quarterly. If you want a dollar estimate, type in the rate you actually paid or your jurisdiction's current rate for that row.</p>""",
    },
    # -------------------------------------------------- Per Diem
    {
        "slug": "per-diem-calculator", "prefix": "pd",
        "hub_title": "Per Diem Calculator", "hub_desc": "Estimate your annual per diem deduction and tax savings.",
        "meta_title": "Truck Driver Per Diem Calculator | Texas Solutions",
        "desc": "Free per diem calculator for truck drivers: estimate your annual per diem deduction and potential tax savings based on days on the road. Not tax advice.",
        "keywords": "truck driver per diem calculator, per diem deduction trucking, owner operator per diem",
        "h1": "Per Diem Calculator",
        "lede": "A rough estimate of your annual per diem deduction and potential tax savings, based on days on the road.",
        "calc_html": """<div class="est rv" id="pdCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Your year on the road</h2>
    <div class="field"><label class="flabel" for="pdDays">Days on the road per year</label><input class="pct-in" type="number" id="pdDays" min="0" max="365" step="1" value="300" inputmode="numeric"></div>
    <div class="field"><label class="flabel" for="pdRate">Per diem rate per day ($)</label><input class="pct-in" type="number" id="pdRate" min="0" step="1" value="69" inputmode="numeric"><p class="hint">Check the current IRS special per diem rate for transportation workers before filing; this default may be out of date.</p></div>
    <div class="field"><label class="flabel" for="pdDeductPct">Deductible percentage (%)</label><input class="pct-in" type="number" id="pdDeductPct" min="0" max="100" step="1" value="80" inputmode="numeric"><p class="hint">Transportation workers subject to DOT hours of service can typically deduct a higher share of meal costs than the general rule; confirm with a tax professional.</p></div>
    <div class="field"><label class="flabel" for="pdTaxRate">Your marginal tax rate (%)</label><input class="pct-in" type="number" id="pdTaxRate" min="0" max="60" step="1" value="22" inputmode="numeric"></div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Estimated per diem</h3>
    <div class="est-big" id="pdBig">$0<small>total per diem, per year</small></div>
    <div class="est-lines">
      <div><span>Deductible amount</span><b id="pdDeductible">-</b></div>
      <div><span>Estimated tax savings</span><b id="pdSavings">-</b></div>
    </div>
    <small><b>Not tax advice.</b> Per diem rates, deductible percentages and your bracket are set by the IRS and your own situation, and can change. Confirm current figures with a tax professional before filing.</small>
  </div>
</div>""",
        "faqs": [
            ("What is per diem for truck drivers?", "Per diem is a daily allowance the IRS publishes for meals and incidental expenses while traveling for work. Drivers away from home overnight for work can generally use it to estimate a meal and incidental expense deduction instead of tracking every receipt."),
            ("How much can truck drivers deduct for per diem?", "It is generally the per diem rate times the number of days on the road, multiplied by the deductible percentage the IRS allows for transportation workers. Rates and percentages are set by the IRS and can change, so confirm the current figures before filing."),
            ("Is this per diem calculator tax advice?", "No. It gives a rough estimate only. Talk to a tax professional about your specific situation, current IRS rates, and how per diem interacts with your pay structure (company driver vs. owner-operator)."),
        ],
        "article_html": """    <h2 style="margin-top:0">How this estimate is calculated</h2>
    <ul>
      <li>Total per diem = days on the road &times; per diem rate per day</li>
      <li>Deductible amount = total per diem &times; deductible percentage</li>
      <li>Estimated tax savings = deductible amount &times; your marginal tax rate</li>
    </ul>
    <p>All three inputs (rate, deductible percentage and your tax bracket) are editable because they depend on current IRS rules and your own situation. This tool is a planning aid, not a tax filing.</p>""",
    },
    # -------------------------------------------------- Truck Loan
    {
        "slug": "truck-loan-calculator", "prefix": "tl",
        "hub_title": "Truck Loan Calculator", "hub_desc": "Monthly payment, total interest and total cost for a truck loan.",
        "meta_title": "Truck Loan Calculator: Monthly Payment & Total Interest | Texas Solutions",
        "desc": "Free truck loan calculator: enter the truck price, down payment, interest rate and term to see your monthly payment, total interest and total cost.",
        "keywords": "truck loan calculator, semi truck financing calculator, commercial truck loan payment calculator",
        "h1": "Truck Loan Calculator",
        "lede": "Monthly payment, total interest and total cost for a truck or trailer loan.",
        "calc_html": """<div class="est rv" id="tlCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Loan details</h2>
    <div class="field"><label class="flabel" for="tlPrice">Truck price ($)</label><input class="pct-in" type="number" id="tlPrice" min="0" step="1000" value="145000" inputmode="numeric"></div>
    <div class="field"><label class="flabel" for="tlDown">Down payment ($)</label><input class="pct-in" type="number" id="tlDown" min="0" step="500" value="15000" inputmode="numeric"></div>
    <div class="field"><label class="flabel" for="tlRate">Interest rate, APR (%)</label><input class="pct-in" type="number" id="tlRate" min="0" step="0.1" value="9.5" inputmode="decimal"></div>
    <div class="field"><label class="flabel" for="tlTerm">Loan term (months)</label><input class="pct-in" type="number" id="tlTerm" min="1" max="120" step="1" value="60" inputmode="numeric"></div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Monthly payment</h3>
    <div class="est-big" id="tlBig">$0<small>per month</small></div>
    <div class="est-lines">
      <div><span>Amount financed</span><b id="tlFinanced">-</b></div>
      <div><span>Total of all payments</span><b id="tlTotal">-</b></div>
      <div><span>Total interest paid</span><b id="tlInterest">-</b></div>
    </div>
    <small>Estimate only. Your actual rate and payment depend on the lender, your credit, and any fees not entered here.</small>
  </div>
</div>""",
        "faqs": [
            ("How is a truck loan payment calculated?", "Using a standard amortization formula on the amount financed (price minus down payment), the monthly interest rate (APR divided by 12), and the loan term in months. The result is the fixed monthly payment that pays off the loan by the end of the term."),
            ("How much down payment do I need for a truck loan?", "It varies by lender, credit and whether the truck is new or used. A larger down payment lowers the amount financed, which lowers both the monthly payment and total interest paid."),
            ("What interest rate should I expect on a truck loan?", "Commercial truck loan rates vary with credit, time in business, and the lender, and change with broader interest rate conditions. Get quotes from a few lenders rather than assuming a rate; use this calculator to compare offers side by side."),
        ],
        "article_html": """    <h2 style="margin-top:0">How the payment is calculated</h2>
    <p>This uses the standard loan amortization formula: <i>M = P &times; r(1+r)<sup>n</sup> &divide; ((1+r)<sup>n</sup> &minus; 1)</i>, where P is the amount financed, r is the monthly interest rate (APR &divide; 12), and n is the number of monthly payments. At 0% interest, the payment is simply the amount financed divided by the term.</p>""",
    },
    # -------------------------------------------------- Maintenance Budget
    {
        "slug": "maintenance-budget-calculator", "prefix": "mb",
        "hub_title": "Maintenance Budget Calculator", "hub_desc": "A yearly repair reserve based on your truck's age and mileage.",
        "meta_title": "Truck Maintenance Budget Calculator | Texas Solutions",
        "desc": "Free truck maintenance budget calculator: estimate a yearly and monthly repair reserve based on your truck's age and annual mileage.",
        "keywords": "truck maintenance budget calculator, trucking repair reserve, maintenance cost per mile trucking",
        "h1": "Maintenance Budget Calculator",
        "lede": "A rough yearly repair reserve based on your truck's age and how many miles you run, so a big repair does not catch you flat.",
        "calc_html": """<div class="est rv" id="mbCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Your truck</h2>
    <div class="field"><label class="flabel" for="mbAge">Truck age (years)</label><input class="pct-in" type="number" id="mbAge" min="0" max="25" step="1" value="3" inputmode="numeric"></div>
    <div class="field"><label class="flabel" for="mbMiles">Annual miles driven</label><input class="pct-in" type="number" id="mbMiles" min="0" step="1000" value="110000" inputmode="numeric"></div>
    <div class="field"><label class="flabel" for="mbCustom">Your own rate ($/mi, optional)</label><input class="pct-in" type="number" id="mbCustom" min="0" step="0.01" placeholder="overrides the age-based rate" inputmode="decimal"></div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Suggested yearly reserve</h3>
    <div class="est-big" id="mbBig">$0<small>per year</small></div>
    <div class="est-lines">
      <div><span>Rate used</span><b id="mbRate">-</b></div>
      <div><span>Monthly reserve</span><b id="mbMonthly">-</b></div>
      <div><span>Weekly reserve</span><b id="mbWeekly">-</b></div>
    </div>
    <small>Rough rule-of-thumb rates, not a quote. Actual maintenance cost depends heavily on make, model, duty cycle and how well the truck has been maintained; use your own repair history when you have it.</small>
  </div>
</div>""",
        "faqs": [
            ("How much should I budget for truck maintenance?", "As a rough rule of thumb, older trucks cost more per mile to maintain. This calculator uses editable age brackets as a starting point; once you have your own repair history, use your own cost per mile instead."),
            ("Why does maintenance cost more on an older truck?", "Wear parts, hoses, seals and major components (engine, transmission, aftertreatment) become more likely to need repair as a truck ages and accumulates miles, so the average cost per mile for upkeep tends to rise."),
            ("Should I set aside money for maintenance every month?", "Many owner-operators keep a maintenance reserve so a large repair does not become a cash-flow crisis. Setting aside a per-mile or monthly amount, even a rough estimate, is better than budgeting nothing."),
        ],
        "article_html": """    <h2 style="margin-top:0">How the reserve is estimated</h2>
    <p>This uses simple age-based rule-of-thumb rates as a starting point, editable if you have your own numbers:</p>
    <ul>
      <li>0-2 years: about $0.12 per mile</li>
      <li>3-5 years: about $0.18 per mile</li>
      <li>6-8 years: about $0.25 per mile</li>
      <li>9+ years: about $0.35 per mile</li>
    </ul>
    <p>Yearly reserve = rate per mile &times; annual miles. These are rough planning figures, not a quote or a guarantee; your own repair history is always the better number once you have a few years of it.</p>""",
    },
    # -------------------------------------------------- HOS
    {
        "slug": "hours-of-service-calculator", "prefix": "hos",
        "hub_title": "Hours of Service (HOS) Calculator", "hub_desc": "Remaining drive time under the 11-hour, 14-hour and 60/70-hour limits.",
        "meta_title": "Hours of Service (HOS) Calculator: 11, 14 & 70-Hour Limits | Texas Solutions",
        "desc": "Free HOS calculator: estimate remaining drive time under the FMCSA 11-hour driving limit, 14-hour on-duty window and 60/7 or 70/8-day cycle limits. Planning tool only, not a legal record.",
        "keywords": "HOS calculator, hours of service calculator, 14 hour rule trucking, 70 hour rule, 11 hour driving limit",
        "h1": "Hours of Service (HOS) Calculator",
        "lede": "A quick planning check against the core FMCSA drive-time limits. This is not your ELD record.",
        "calc_html": """<div class="est rv" id="hosCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Today so far</h2>
    <div class="field"><label class="flabel" for="hosDriven">Hours driven today</label><input class="pct-in" type="number" id="hosDriven" min="0" max="11" step="0.25" value="0" inputmode="decimal"></div>
    <div class="field"><label class="flabel" for="hosOnDuty">Other on-duty hours today (not driving)</label><input class="pct-in" type="number" id="hosOnDuty" min="0" max="14" step="0.25" value="0" inputmode="decimal"></div>
    <div class="field"><label class="flabel" for="hosElapsed">Hours elapsed since you started today's shift</label><input class="pct-in" type="number" id="hosElapsed" min="0" max="24" step="0.25" value="0" inputmode="decimal"><p class="hint">Clock time since coming on duty, including any breaks.</p></div>
    <div class="grid g2" style="gap:14px;margin-top:14px">
      <div><label class="flabel" for="hosCycleType">Cycle limit</label><select class="pct-in" id="hosCycleType"><option value="70">70 hours / 8 days</option><option value="60">60 hours / 7 days</option></select></div>
      <div><label class="flabel" for="hosCycleUsed">Cycle hours used (before today)</label><input class="pct-in" type="number" id="hosCycleUsed" min="0" step="0.25" value="45" inputmode="decimal"></div>
    </div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>You can drive up to</h3>
    <div class="est-big" id="hosBig">0.0<small>more hours today</small></div>
    <div class="est-lines">
      <div><span>Drive-time limit (11 hr)</span><b id="hosDriveLeft">-</b></div>
      <div><span>On-duty window (14 hr)</span><b id="hosWindowLeft">-</b></div>
      <div><span>Cycle limit</span><b id="hosCycleLeft">-</b></div>
      <div><span>Binding limit</span><b id="hosBinding">-</b></div>
    </div>
    <small><b>Planning tool only, not a legal record.</b> Does not cover every FMCSA exception (adverse conditions, short-haul, sleeper-berth splits, agricultural exemptions and more). Use your ELD as your official record and refer to 49 CFR Part 395.</small>
  </div>
</div>""",
        "faqs": [
            ("What is the 11-hour driving limit?", "Under core FMCSA rules, a property-carrying driver may drive up to 11 hours after 10 consecutive hours off duty."),
            ("What is the 14-hour rule?", "A driver may not drive after the 14th hour since coming on duty, following 10 consecutive hours off duty. The 14-hour window keeps running during on-duty time and most breaks; it is not paused, with limited exceptions such as qualifying sleeper-berth splits."),
            ("What is the 70-hour/8-day rule?", "A driver may not drive after 70 hours on duty in 8 consecutive days (or 60 hours in 7 days for carriers on that cycle). The cycle resets with 34 consecutive hours off duty."),
            ("Does this calculator replace my ELD?", "No. This is a rough planning aid for estimating remaining hours. Your electronic logging device is your official hours-of-service record. This tool does not model every FMCSA exception."),
        ],
        "article_html": """    <h2 style="margin-top:0">How remaining hours are estimated</h2>
    <ul>
      <li>Drive-time limit remaining = 11 &minus; hours driven today</li>
      <li>On-duty window remaining = 14 &minus; hours elapsed since starting today's shift</li>
      <li>Cycle limit remaining = cycle limit (60 or 70) &minus; cycle hours already used &minus; today's on-duty hours</li>
      <li>You can drive up to the smallest (binding) of the three</li>
    </ul>
    <p>This models the core rules only. It does not account for adverse driving conditions, the short-haul exemption, sleeper-berth split options, or other FMCSA exceptions in 49 CFR Part 395. Always confirm against your ELD and current regulations.</p>""",
    },
    # -------------------------------------------------- Freight Class
    {
        "slug": "freight-class-calculator", "prefix": "fc",
        "hub_title": "Freight Class Calculator", "hub_desc": "A density-based NMFC freight class estimate from dimensions and weight.",
        "meta_title": "Freight Class Calculator (NMFC Density-Based) | Texas Solutions",
        "desc": "Free freight class calculator: estimate NMFC freight class from length, width, height and weight using the standard density table. Estimate only, confirm with your carrier.",
        "keywords": "freight class calculator, NMFC freight class, freight density calculator, LTL freight class lookup",
        "h1": "Freight Class Calculator",
        "lede": "A density-based estimate of NMFC freight class from your shipment's dimensions and weight.",
        "calc_html": """<div class="est rv" id="fcCalc">
  <div class="est-in">
    <h2 style="font-size:26px">Shipment dimensions</h2>
    <div class="grid g2" style="gap:14px;margin-top:16px">
      <div><label class="flabel" for="fcL">Length (in)</label><input class="pct-in" type="number" id="fcL" min="1" step="1" value="48" inputmode="numeric"></div>
      <div><label class="flabel" for="fcW">Width (in)</label><input class="pct-in" type="number" id="fcW" min="1" step="1" value="40" inputmode="numeric"></div>
      <div><label class="flabel" for="fcH">Height (in)</label><input class="pct-in" type="number" id="fcH" min="1" step="1" value="48" inputmode="numeric"></div>
      <div><label class="flabel" for="fcWeight">Weight per unit (lbs)</label><input class="pct-in" type="number" id="fcWeight" min="1" step="1" value="500" inputmode="numeric"></div>
      <div class="full"><label class="flabel" for="fcUnits">Number of identical units</label><input class="pct-in" type="number" id="fcUnits" min="1" step="1" value="1" inputmode="numeric"></div>
    </div>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Estimated freight class</h3>
    <div style="margin-top:6px"><span class="class-badge" id="fcClass">-</span></div>
    <div class="est-lines" style="margin-top:22px">
      <div><span>Density</span><b id="fcDensity">-</b></div>
      <div><span>Total cubic feet</span><b id="fcCube">-</b></div>
      <div><span>Total weight</span><b id="fcTotalWeight">-</b></div>
    </div>
    <small><b>Estimate only.</b> Actual NMFC freight class depends on the specific commodity's NMFC item number, packaging, stowability and liability, not density alone. Confirm your class with your carrier or an official NMFC lookup before booking; getting it wrong can mean reclassification fees.</small>
  </div>
</div>""",
        "faqs": [
            ("How is freight class determined?", "Officially, freight class comes from the National Motor Freight Classification (NMFC), which assigns a specific item number to each commodity based on density, stowability, handling and liability. Density-based calculators like this one give a reasonable estimate for commodities without unusual handling or liability factors."),
            ("What is freight density and how is it calculated?", "Density is weight divided by volume, in pounds per cubic foot (PCF). Cubic feet = (length &times; width &times; height in inches) &divide; 1728. Density = total weight &divide; total cubic feet."),
            ("Why did my carrier reclassify my shipment?", "Carriers may reclassify a shipment if the class booked does not match the commodity's actual NMFC item, or if the measured density does not match what was declared. Confirming the correct class before booking avoids reclassification fees."),
        ],
        "article_html": """    <h2 style="margin-top:0">The density table used</h2>
    <div class="tbl"><table><thead><tr><th>Density (PCF)</th><th>Estimated class</th></tr></thead><tbody>
      <tr><td>50 and over</td><td>50</td></tr>
      <tr><td>35 to under 50</td><td>55</td></tr>
      <tr><td>30 to under 35</td><td>60</td></tr>
      <tr><td>22.5 to under 30</td><td>65</td></tr>
      <tr><td>15 to under 22.5</td><td>70</td></tr>
      <tr><td>12 to under 15</td><td>77.5</td></tr>
      <tr><td>10 to under 12</td><td>85</td></tr>
      <tr><td>8 to under 10</td><td>92.5</td></tr>
      <tr><td>6 to under 8</td><td>100</td></tr>
      <tr><td>4 to under 6</td><td>125</td></tr>
      <tr><td>2 to under 4</td><td>150</td></tr>
      <tr><td>1 to under 2</td><td>175</td></tr>
      <tr><td>under 1</td><td>250+</td></tr>
    </tbody></table></div>
    <p>This is the widely used general density-to-class guideline. Some commodities carry their own NMFC item number regardless of density (electronics, hazardous materials, automotive parts and more), which overrides a pure density estimate. When in doubt, ask your carrier or dispatcher.</p>""",
    },
]


# Fill placeholders that need runtime values (WA_URL/ICONS/C are defined
# earlier in site.py, by the time this module-level code runs).
for _t in TOOLS:
    if "__WA__" in _t["calc_html"]:
        _t["calc_html"] = _t["calc_html"].replace("__WA__", WA_URL).replace("__WA_ICON__", ICONS["wa"])
    if "__STATES__" in _t["calc_html"]:
        _states_json = json.dumps([n for n, _ in C.STATE_REGION.values()]).replace("'", "&#39;")
        _t["calc_html"] = _t["calc_html"].replace("__STATES__", _states_json)


def build_rss():
    """RSS 2.0 feed of blog posts, for feed readers, news aggregators and AI crawlers."""
    items = []
    for po in POSTS:
        link = url(f"/blog/{po['slug']}.html")
        pub = po["date"].strftime("%a, %d %b %Y 00:00:00 +0000")
        cat = esc(po["tags"][0]) if po["tags"] else "Trucking"
        items.append(f"""    <item>
      <title>{esc(po['title'])}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{pub}</pubDate>
      <description>{esc(po['description'])}</description>
      <category>{cat}</category>
    </item>""")
    build_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{esc(C.BRAND)} Blog</title>
    <link>{url('/blog.html')}</link>
    <atom:link href="{url('/feed.xml')}" rel="self" type="application/rss+xml" />
    <description>Truck dispatch, rates, diesel prices and fuel-saving guides for owner-operators and small fleets.</description>
    <language>en-us</language>
    <lastBuildDate>{build_date}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""
    write("feed.xml", rss)

def build_404():
    body = f"""{phero("Not found", "This page took a wrong exit.", "The page you are looking for does not exist. Try one of these instead.", ctas=False)}
<section class="sec"><div class="wrap"><div class="chip-row" style="justify-content:flex-start">
<a class="chip" href="index.html">Home</a><a class="chip" href="estimate.html">Free Estimate</a><a class="chip" href="truck-dispatch-rates.html">Dispatch Rates</a><a class="chip" href="contact.html">Contact</a>
{''.join(f'<a class="chip" href="{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING)}
</div></div></section>"""
    shell = page("/404.html", "Page Not Found | " + C.BRAND, "Page not found.", "truck dispatch", [], body)
    shell = shell.replace('content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"', 'content="noindex"')
    shell = re.sub(r'(href|src)="(?!https?:|/|#|tel:|mailto:|data:)', r'\1="/', shell)
    write("404.html", shell)


def diesel_lines():
    d = load_diesel()
    if not d:
        return []
    out = [f"## Diesel prices by state (daily, {d.get('day')}; EIA U.S. weekly average ${d['regions']['US']['price']:.3f})"]
    out += [f"- {C.STATE_REGION[c][0]}: ${v:.3f}/gal" for c, v in sorted(d.get("states", {}).items(), key=lambda kv: C.STATE_REGION[kv[0]][0])]
    out += [f"- Truck fuel cost calculator: {url('/truck-fuel-cost-calculator.html')}", ""]
    return out


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def lastmods():
    """Sitemap lastmod per page: the date only moves when that page's HTML actually changes."""
    mf = ROOT / "data" / "lastmod.json"
    old = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    new = {}
    for name, h in sorted(PAGE_HASH.items()):
        prev = old.get(name)
        new[name] = {"hash": h, "date": prev["date"] if prev and prev.get("hash") == h else TODAY}
    mf.parent.mkdir(exist_ok=True)
    mf.write_text(json.dumps(new, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return {k: v["date"] for k, v in new.items()}


def sm_urlset(entries, images=False):
    ns = 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
    if images:
        ns += ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
    out = ['<?xml version="1.0" encoding="UTF-8"?>', f"<urlset {ns}>"]
    for e in entries:
        s = f"  <url><loc>{esc(e['loc'])}</loc><lastmod>{e['lastmod']}</lastmod>"
        if e.get("image"):
            s += f"<image:image><image:loc>{esc(e['image'])}</image:loc><image:title>{esc(e['title'])}</image:title></image:image>"
        out.append(s + "</url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def llms_facts():
    return [
        f"- Service: truck dispatch (load search, rate negotiation, broker setup packets, rate confirmations, lane planning)",
        f"- Semi truck dispatch fee (dry van, reefer, flatbed, step deck, power only): {pl(M)} of weekly gross, OTR - about {SEMI_FEE[0]}-{SEMI_FEE[1]} per week on typical gross of {money(M['gross'][0])}-{money(M['gross'][1])}",
        "- Hotshot dispatch fee: 8% of weekly gross, OTR - about $560-$720 per week on typical gross of $7,000-$9,000",
        "- Box truck and straight truck dispatch fee: 10% of weekly gross, OTR - about $700-$900 per week on typical gross of $7,000-$9,000",
        "- The fee is a percentage of weekly gross (what the truck earns hauling loads that week). No flat rate, no setup fee, no monthly subscription, no long-term contract, no forced loads",
        f"- Condition: {C.PRICING_CONDITION}",
        "- Rough freight rates per mile (not guaranteed): flatbed $5-7, step deck $5-7, reefer $4-6, hotshot $4-5, dry van $3-5 (local or OTR), power only $3-5, box truck $1.80-3.20",
        "- Area served: United States (48 states), with a focus on Texas and the Permian Basin",
        "- Texas Solutions is a dispatch service. It is not a motor carrier or freight broker and does not guarantee loads, rates or earnings",
        f"- Phone: {C.PHONE} | WhatsApp: +1 838 910 3147 (https://wa.me/{C.WHATSAPP}) | Email: {C.EMAIL}",
        f"- Address: {C.STREET}, {C.CITY}, {C.REGION} {C.POSTAL}",
        "- Owner and CEO: Shehryar Joyia",
    ]


def build_site_files():
    lm = lastmods()

    def entry(path):
        f = "index.html" if path == "/" else path.lstrip("/")
        return {"loc": url(path), "lastmod": lm.get(f, TODAY)}

    core = ["/", "/estimate.html", "/truck-dispatch-rates.html", "/truck-fuel-cost-calculator.html"] + ["/" + p["file"] for p in C.LANDING] + \
           ["/faq.html", "/about.html", "/contact.html", "/privacy.html", "/terms.html"]
    tool_paths = ["/tools.html"] + ["/" + tl["slug"] + ".html" for tl in TOOLS]
    blog_entries = [entry("/blog.html")] + [dict(entry(f"/blog/{po['slug']}.html"), image=po["cover_abs"], title=po["title"]) for po in POSTS]
    groups = {
        "sitemap-pages.xml": [entry(x) for x in core],
        "sitemap-tools.xml": [entry(x) for x in tool_paths],
        "sitemap-blog.xml": blog_entries,
        "sitemap-diesel.xml": [entry(pth) for _, pth in STATE_PAGES],
    }
    for name, ents in groups.items():
        write(name, sm_urlset(ents, images=(name == "sitemap-blog.xml")))
    idx = ['<?xml version="1.0" encoding="UTF-8"?>', '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name, ents in groups.items():
        idx.append(f"  <sitemap><loc>{url('/' + name)}</loc><lastmod>{max(e['lastmod'] for e in ents)}</lastmod></sitemap>")
    idx.append("</sitemapindex>")
    write("sitemap.xml", "\n".join(idx) + "\n")
    all_locs = [e["loc"] for ents in groups.values() for e in ents]
    write("urls.txt", "\n".join(all_locs) + "\n")

    # ---------------------------------------------------------- robots.txt
    bots = ["Googlebot", "Googlebot-Image", "Bingbot", "Slurp", "YandexBot", "DuckDuckBot", "Applebot", "Applebot-Extended",
            "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "GoogleOther", "Gemini-Deep-Research", "DuckAssistBot",
            "CCBot", "Meta-ExternalAgent", "Meta-ExternalFetcher", "Amazonbot", "cohere-ai", "MistralAI-User", "YouBot"]
    block = ["Allow: /", "Disallow: /admin/", "Disallow: /content/", "Disallow: /tools/", "Disallow: /head-codes.html"]
    robots = ["# dispatch.texassolutions.co: search engines and AI answer engines are welcome.",
              f"# Plain-text summary for AI tools: {C.BASE}/llms.txt (full text: {C.BASE}/llms-full.txt)",
              f"# Blog RSS feed: {C.BASE}/feed.xml", "",
              "User-agent: *", *block, ""]
    robots += [f"User-agent: {b}" for b in bots] + block + [""]
    robots += [f"Sitemap: {C.BASE}/sitemap.xml"] + [f"Sitemap: {C.BASE}/{n}" for n in groups]
    write("robots.txt", "\n".join(robots) + "\n")
    write(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)

    # ---------------------------------------------------------- llms.txt (short) and llms-full.txt (everything)
    diesel = load_diesel()
    key_states = ["TX", "CA", "FL", "GA", "IL", "NY", "OH", "PA", "OK", "TN"]
    diesel_short = []
    if diesel:
        us_p = diesel["regions"]["US"]["price"]
        diesel_short = [f"- As of {diesel.get('day') or diesel.get('week')}: U.S. average ${us_p:.3f}/gal (EIA), "
                        + ", ".join(f"{C.STATE_REGION[c][0]} ${diesel['states'][c]:.3f}" for c in key_states if c in diesel.get("states", {})),
                        f"- Daily prices for all 50 states and DC: {url('/truck-fuel-cost-calculator.html')}#diesel-prices; one page per state at {url('/diesel-prices/texas.html')} (replace texas with the state name)"]
    summary = (f"> Texas Solutions is a US truck dispatch service for owner-operators and small fleets, based in {C.CITY}, Texas. "
               f"Dispatch fee: {pl(M)} of weekly gross for OTR semi trucks, 8% for hotshots, 10% for box trucks and straight trucks. "
               "No flat rate, no setup fee, no monthly subscription, no forced loads. Also free trucking calculators (fuel cost, cost per mile, IFTA, HOS, "
               "load profitability and more), daily diesel prices by state, and a trucking blog. Texas Solutions is not a motor carrier or freight broker "
               "and does not guarantee loads, rates or earnings.")
    llms = [f"# {C.BRAND}", "", summary, "", "## Key facts", *llms_facts(), "",
            "## Free trucking calculators",
            f"- [Tools hub]({url('/tools.html')}): all calculators in one place",
            f"- [Dispatch fee calculator and free quote]({url('/estimate.html')}): dispatch fee by truck type, plus a quote request via WhatsApp",
            f"- [Truck fuel cost calculator]({url('/truck-fuel-cost-calculator.html')}): MPG by truck type and load weight, trip fuel cost, cost per mile, daily diesel price by state",
            *[f"- [{tl['hub_title']}]({url('/' + tl['slug'] + '.html')}): {tl['desc']}" for tl in TOOLS], "",
            "## Guides (blog)",
            *[f"- [{po['title']}]({url('/blog/' + po['slug'] + '.html')}): {po['answer'] or po['description']}" for po in POSTS],
            f"- [Blog RSS feed]({url('/feed.xml')})", "",
            "## Dispatch services",
            *[f"- [{pg['nav']}]({url('/' + pg['file'])}): {pg['answer']}" for pg in C.LANDING],
            f"- [Truck dispatch rates and rate-per-mile guide]({url('/truck-dispatch-rates.html')})", "",
            "## Diesel prices", *diesel_short, "",
            "## Company",
            f"- [Home]({url('/')})", f"- [About]({url('/about.html')})", f"- [Contact]({url('/contact.html')})", f"- [FAQ]({url('/faq.html')})",
            f"- [Privacy]({url('/privacy.html')})", f"- [Terms]({url('/terms.html')})", "",
            "## Optional",
            f"- [Full text of this site for LLMs]({url('/llms-full.txt')}): guides, tool explanations, FAQs and diesel prices in one file",
            f"- [Sitemap]({url('/sitemap.xml')})",
            f"- [Texas Solutions software development, AI and QA]({C.MAIN_SITE}/)", ""]
    write("llms.txt", "\n".join(llms))

    full = [f"# {C.BRAND}: full text", "", summary, "", "## Key facts", *llms_facts(), ""]
    full += ["## Frequently asked questions"]
    seen = set()
    for q, a in C.FAQS + [(x, y) for pg in C.LANDING for x, y in pg["faqs"]]:
        if q not in seen:
            seen.add(q)
            full += [f"### {q}", a, ""]
    full += ["## Free trucking calculators", ""]
    for tl in TOOLS:
        full += [f"### {tl['hub_title']}", f"URL: {url('/' + tl['slug'] + '.html')}", tl["desc"], strip_tags(tl["article_html"]), ""]
        for q, a in tl["faqs"]:
            full += [f"Q: {q}", f"A: {a}", ""]
    full += ["## Blog posts", ""]
    for po in POSTS:
        full += [f"### {po['title']}", f"URL: {url('/blog/' + po['slug'] + '.html')}", f"Published: {po['date'].isoformat()}", "", po["md"], ""]
    if diesel:
        full += [f"## Diesel prices by state (daily, {diesel.get('day')}; EIA U.S. weekly average ${diesel['regions']['US']['price']:.3f}/gal)"]
        full += [f"- {C.STATE_REGION[c][0]}: ${v:.3f}/gal" for c, v in sorted(diesel.get("states", {}).items(), key=lambda kv: C.STATE_REGION[kv[0]][0])]
        full += [""]
    write("llms-full.txt", "\n".join(full))


def main():
    global POSTS, STATE_PAGES
    POSTS = build_blog()
    STATE_PAGES = build_state_pages()
    build_home()
    build_estimate()
    build_rates()
    build_contact()
    build_about()
    build_faq()
    build_legal("privacy.html", "Privacy Policy")
    build_legal("terms.html", "Terms & Conditions")
    for p in C.LANDING:
        build_landing(p)
    build_fuel()
    build_tools()
    build_tools_hub()
    build_rss()
    build_404()
    build_site_files()
    print("built", 19 + len(C.LANDING) + len(POSTS) + len(STATE_PAGES) + len(TOOLS), "pages, plus feed.xml")


if __name__ == "__main__":
    main()
