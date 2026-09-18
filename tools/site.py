"""
Builds every page of dispatch.texassolutions.co from tools/content.py.

    python tools/site.py

Pages are written whole each run (no hand edits in the .html files survive),
so change words and numbers in tools/content.py, header codes in
head-codes.html, and legal text in tools/legal/*.html.
"""

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import content as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()
OG_IMAGE = f"{C.BASE}/assets/og-image.png"
LOGO = f"{C.BASE}/assets/logo/texas-solutions-logo.png"
BUSINESS_ID = f"{C.BASE}/#business"
INDEXNOW_KEY = "7c1f4e2a9b8d4c6e8f0a1b2c3d4e5f60"
esc = html.escape
S, M = C.PRICING["small"], C.PRICING["semi"]


def write(name, text):
    (ROOT / name).write_text(text, encoding="utf-8", newline="\n")


def url(path):
    return C.BASE + ("/" if path in ("", "/") else path)


def money(n):
    return f"${n:,.0f}"


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


def offers():
    out = []
    for k in ("semi", "small"):
        p = C.PRICING[k]
        out.append({
            "@type": "Offer",
            "name": f"{p['label']} OTR dispatch",
            "description": f"{p['pct'][0]}-{p['pct'][1]}% of weekly gross for OTR {', '.join(p['equipment']).lower()}. "
                           f"Typical weekly gross {money(p['gross'][0])}-{money(p['gross'][1])}. No flat rate, no setup fee.",
            "priceCurrency": "USD",
            "priceSpecification": {"@type": "UnitPriceSpecification", "name": f"{p['pct'][0]}-{p['pct'][1]}% of weekly gross",
                                   "priceCurrency": "USD", "minPrice": round(p["gross"][0] * p["pct"][0] / 100),
                                   "maxPrice": round(p["gross"][1] * p["pct"][1] / 100), "unitText": "WEEK"},
        })
    return out


def business():
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": BUSINESS_ID,
        "name": C.NAME,
        "alternateName": C.BRAND,
        "slogan": "Truck dispatch for owner-operators and small fleets",
        "description": f"Truck dispatch service for owner-operators and small fleets in the United States. Semi trucks pay "
                       f"{M['pct'][0]}-{M['pct'][1]}% of weekly gross and small trucks {S['pct'][0]}-{S['pct'][1]}%, for OTR operations, "
                       "with no flat rate and no setup fee.",
        "url": url("/"),
        "logo": LOGO,
        "image": OG_IMAGE,
        "telephone": C.PHONE_E164,
        "email": C.EMAIL,
        "priceRange": f"{M['pct'][0]}-{S['pct'][1]}% of weekly gross",
        "address": {"@type": "PostalAddress", "streetAddress": C.STREET, "addressLocality": C.CITY,
                    "addressRegion": C.REGION, "postalCode": C.POSTAL, "addressCountry": C.COUNTRY},
        "areaServed": {"@type": "Country", "name": "United States"},
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": C.PHONE_E164, "contactType": "sales", "areaServed": "US", "availableLanguage": "English"},
            {"@type": "ContactPoint", "url": f"https://wa.me/{C.WHATSAPP}", "contactType": "customer support", "name": "WhatsApp"},
        ],
        "sameAs": [C.MAIN_SITE + "/"],
        "knowsAbout": ["Truck dispatch", "Freight dispatch", "OTR dispatch", "Load boards", "Rate negotiation",
                       "Broker setup packets", "Owner-operator trucking"] + [f"{e} dispatch" for e in C.EQUIPMENT],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Truck dispatch pricing", "itemListElement": offers()},
    }


def website():
    return {"@context": "https://schema.org", "@type": "WebSite", "name": C.BRAND, "url": url("/"), "publisher": {"@id": BUSINESS_ID}}


def service(name, description, path, stype):
    return {
        "@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": stype,
        "description": description, "url": url(path), "provider": {"@id": BUSINESS_ID},
        "areaServed": {"@type": "Country", "name": "United States"},
        "audience": {"@type": "BusinessAudience", "audienceType": "Owner-operators and small trucking fleets"},
        "offers": offers(),
    }


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def crumbs_ld(trail):
    items = [("Home", "/")] + trail
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}


def speakable(path, name):
    return {"@context": "https://schema.org", "@type": "WebPage", "name": name, "url": url(path), "dateModified": TODAY,
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
    return [("Rates", "truck-dispatch-rates.html"), ("Estimate", "estimate.html"), ("About", "about.html"),
            ("FAQ", "faq.html"), ("Contact", "contact.html")]


def header(current):
    svc = "\n".join(f'          <a href="{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING)
    links = "\n".join(f'      <a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for t, h in nav_links())
    mlinks = "\n".join(f'    <a href="{h}">{t}</a>' for t, h in nav_links())
    msvc = "\n".join(f'      <a href="{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <div class="tb-left"><span class="tb-pill">OTR dispatch: semis {M['pct'][0]}-{M['pct'][1]}% &middot; small trucks {S['pct'][0]}-{S['pct'][1]}%</span><span class="tb-hide">No flat rate &middot; No setup fee</span></div>
  <div class="tb-left"><a href="tel:{C.PHONE_E164}">{C.PHONE}</a><a class="tb-hide" href="mailto:{C.EMAIL}">{C.EMAIL}</a></div>
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
    <div class="mnav-sub">
{msvc}
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
        <p>Truck dispatch service for owner-operators and small fleets across the United States. Semi trucks {M['pct'][0]}-{M['pct'][1]}% and small trucks {S['pct'][0]}-{S['pct'][1]}% of weekly gross, OTR. No flat rate.</p>
      </div>
      <div>
        <h4>Dispatch Services</h4>
{svc}
      </div>
      <div>
        <h4>Company</h4>
      <a href="truck-dispatch-rates.html">Dispatch Rates</a>
      <a href="estimate.html">Free Estimate</a>
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
<script src="js/site.js" defer></script>"""


def page(path, title, description, keywords, schemas, body, current=None, og_type="website", preload_video=False):
    codes = head_codes() or "<!-- no header codes yet: paste them into head-codes.html -->"
    lds = "\n".join(ld(s) for s in (business(), website(), *schemas))
    return f"""<!DOCTYPE html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="keywords" content="{esc(keywords)}">
<link rel="canonical" href="{url(path)}">
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
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" type="image/png" href="assets/logo/favicon.png">
<link rel="apple-touch-icon" href="assets/logo/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="css/site.css">
<link rel="alternate" type="text/plain" href="{C.BASE}/llms.txt" title="LLM summary">
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


def pricing_cards(cta=True):
    def card(k, feat):
        p = C.PRICING[k]
        lo, hi = fee_range(k)
        items = [f"For {', '.join(p['equipment'][:-1]).lower()} and {p['equipment'][-1].lower()}",
                 f"Typical weekly gross {money(p['gross'][0])} - {money(p['gross'][1])}",
                 f"About {lo} - {hi} per week on typical gross",
                 "OTR (over-the-road) operations", "No flat rate, no setup fee, no subscription",
                 "You approve every load"]
        li = "\n".join(f"      <li>{esc(i)}</li>" for i in items)
        btn = f'<a class="btn {"btn-red" if feat else "btn-dark"}" href="estimate.html?type={k}">Estimate my fee</a>' if cta else ""
        tag = '<span class="tag">Most popular</span>' if feat else ""
        return f"""<div class="price{' feat' if feat else ''} rv">
    {tag}<h3>{p['label']}</h3>
    <p class="eq">{', '.join(p['equipment'])}</p>
    <div class="amt">{p['pct'][0]}-{p['pct'][1]}%<small> of weekly gross</small></div>
    <ul>
{li}
    </ul>
    {btn}
  </div>"""
    return f"""<div class="grid g2">
  {card('semi', True)}
  {card('small', False)}
</div>
<p class="note center">{esc(C.PRICING_CONDITION)} {esc(C.PRICING_NOTE)}</p>"""


def rate_board():
    rows = "\n".join(
        f'      <tr><td>{o} &rarr; {d}</td><td><span class="eq-badge">{e}</span></td><td class="hide-sm">{mi:,} mi</td><td class="rate">{r}/mi</td></tr>'
        for o, d, e, mi, r in C.LANES)
    guide = "\n".join(
        f'    <div class="rg{" hi" if eq in ("Flatbed", "Hotshot", "Dry Van") else ""}"><b>{eq}</b><span class="v">{rate}/mi</span><small>{note}</small></div>'
        for eq, rate, note in C.RATE_GUIDE)
    return f"""<div class="grid board-grid" id="board">
  <div class="board rv">
    <div class="board-head"><b><span class="dot"></span>Sample lane board</b><span>Rough estimate &middot; <span id="boardTime">today</span></span></div>
    <div style="overflow-x:auto"><table class="board-table">
      <thead><tr><th>Lane</th><th>Equipment</th><th class="hide-sm">Miles</th><th>Rate</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table></div>
    <p class="board-foot">Illustrative sample lanes shown for demonstration. Texas Solutions does not guarantee any specific load volume, rate, revenue, or earnings.</p>
  </div>
  <div class="rv">
    <h3 style="color:#fff;margin-bottom:14px">Rough rate per mile by equipment</h3>
    <div class="rate-guide">
{guide}
    </div>
    <p style="font-size:13px;color:#8a847e;margin-top:12px">Rough estimates. Flatbed and hotshot loads often pay $5-6 a mile; dry van runs about $2-5 a mile depending on local or OTR lanes. Actual rates depend on lane, season and market.</p>
  </div>
</div>"""


def equip_cards():
    icons = "truck"
    return '<div class="grid g3">\n' + "\n".join(
        f"""  <a class="card rv" href="{p['file']}"><div class="icon">{ICONS[icons]}</div><h3>{esc(p['nav'])}</h3><p>{esc(p['description'][:150].rsplit(' ', 1)[0])}...</p><span class="more">{C.PRICING[p['kind']]['pct'][0]}-{C.PRICING[p['kind']]['pct'][1]}% &middot; Learn more &rarr;</span></a>"""
        for p in C.LANDING if not p.get("guide")) + "\n</div>"


def features():
    return '<div class="grid g3">\n' + "\n".join(
        f'  <div class="card rv"><div class="icon">{ICONS[FEATURE_ICONS[i]]}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, (t, d) in enumerate(C.FEATURES)) + "\n</div>"


def steps(dark=False):
    return '<div class="grid g4 steps">\n' + "\n".join(
        f'  <div class="step rv"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in C.STEPS) + "\n</div>"


def band(title="Ready to keep your truck loaded?", text=None):
    text = text or f"Semi trucks {M['pct'][0]}-{M['pct'][1]}%, small trucks {S['pct'][0]}-{S['pct'][1]}% of weekly gross. OTR. No flat rate, no setup fee."
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


def build_home():
    title = "Truck Dispatch Service for Owner-Operators | 5-6% Semi, 8-10% Small Truck | Texas Solutions"
    desc = (f"Truck dispatch service for owner-operators and small fleets. Semi trucks {M['pct'][0]}-{M['pct'][1]}% and box trucks & hotshots "
            f"{S['pct'][0]}-{S['pct'][1]}% of weekly gross, OTR. No flat rate, no setup fee. Flatbed & hotshot loads $5-6/mile. Free estimate.")
    qa = ("How much does truck dispatch cost at Texas Solutions?",
          f"Texas Solutions charges {M['pct'][0]}-{M['pct'][1]}% of weekly gross for OTR semi trucks (dry van, reefer, flatbed, step deck, power only) "
          f"and {S['pct'][0]}-{S['pct'][1]}% for OTR small trucks (box truck, straight truck, hotshot). There is no flat rate, no setup fee and no "
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
        <div><b>{M['pct'][0]}-{M['pct'][1]}%</b><span>Semi trucks, OTR</span></div>
        <div><b>{S['pct'][0]}-{S['pct'][1]}%</b><span>Box truck &amp; hotshot</span></div>
        <div><b>$0</b><span>Setup fee or flat rate</span></div>
      </div>
    </div>
    <aside class="hero-card" aria-label="Dispatch pricing">
      <h2>Simple percentage pricing</h2>
      <div class="row"><div><b>Semi trucks</b><br><span>Dry van, reefer, flatbed, step deck, power only &middot; gross {money(M['gross'][0])}-{money(M['gross'][1])}/wk</span></div><span class="pct">{M['pct'][0]}-{M['pct'][1]}%</span></div>
      <div class="row"><div><b>Small trucks</b><br><span>Box truck, straight truck, hotshot &middot; gross {money(S['gross'][0])}-{money(S['gross'][1])}/wk</span></div><span class="pct">{S['pct'][0]}-{S['pct'][1]}%</span></div>
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
  <div class="sec-head rv"><span class="eyebrow">Rate board</span><h2>What loads are paying</h2><p>A rough guide to rates per mile on common equipment. Flatbed and hotshot often pay $5-6 a mile. Dry van runs about $2-5 a mile depending on local or OTR.</p></div>
  {rate_board()}
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Why carriers choose us</span><h2>A dispatch team that works for the carrier</h2><p>Load boards, broker calls, rate negotiation and paperwork, handled by real dispatchers while you drive.</p></div>
  {features()}
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Dispatch services</span><h2>Truck dispatch for every trailer type</h2><p>Dedicated dispatch for dry van, reefer, flatbed, step deck, power only, hotshot, box truck and straight truck carriers nationwide.</p></div>
  {equip_cards()}
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">How it works</span><h2>Start dispatching in four steps</h2></div>
  {steps()}
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Truck dispatch FAQ</span><h2>Questions owner-operators ask</h2></div>
  {faq_html(C.FAQS[:8])}
  <p class="mt-l"><a class="btn btn-line" href="faq.html">See all FAQs</a></p>
</div></section>
{band()}"""
    schemas = [service("Truck Dispatch Service", desc, "/", "Truck dispatch"), faq_ld([qa] + C.FAQS[:8]), howto(), speakable("/", title)]
    write("index.html", page("/", title, desc, HOME_KW, schemas, body, current="index.html"))


def build_estimate():
    title = "Truck Dispatch Fee Calculator & Free Quote | Texas Solutions"
    desc = (f"Estimate your truck dispatch fee: semi trucks {M['pct'][0]}-{M['pct'][1]}% and small trucks {S['pct'][0]}-{S['pct'][1]}% of weekly gross, "
            "OTR only, no flat rate. Enter your trucks and weekly gross, see your weekly and monthly fee, and request a free quote.")
    cfg = {k: {"label": p["label"], "pct": list(p["pct"]), "gross": list(p["gross"]),
               "defaultEq": "Dry Van" if k == "semi" else "Box Truck"} for k, p in C.PRICING.items()}
    qa = ("How is the Texas Solutions dispatch fee calculated?",
          f"Multiply your truck's weekly gross by the dispatch percentage: {M['pct'][0]}-{M['pct'][1]}% for OTR semi trucks, {S['pct'][0]}-{S['pct'][1]}% "
          f"for OTR small trucks. Example: a semi grossing $9,000 a week pays about $450-$540 a week. A hotshot grossing $8,000 pays about $640-$800. "
          "There is no flat rate and no setup fee.")
    calc = f"""<div class="est rv" id="estimator" data-pricing='{json.dumps(cfg)}'>
  <div class="est-in">
    <h2 style="font-size:26px">Dispatch fee calculator</h2>
    <p style="color:var(--muted);margin-top:8px">Pick your truck type, number of trucks and weekly gross per truck.</p>
    <div class="field"><span class="flabel">Truck type</span>
      <div class="seg" role="radiogroup" aria-label="Truck type">
        <label><input type="radio" name="estType" value="semi" checked><b>Semi truck</b><span>{M['pct'][0]}-{M['pct'][1]}% &middot; dry van, reefer, flatbed, step deck, power only</span></label>
        <label><input type="radio" name="estType" value="small"><b>Small truck</b><span>{S['pct'][0]}-{S['pct'][1]}% &middot; box truck, straight truck, hotshot</span></label>
      </div>
    </div>
    <div class="field"><label for="estTrucks">Number of trucks</label>
      <div class="range-row"><input type="range" id="estTrucks" min="1" max="25" value="1"><output id="estTrucksOut" for="estTrucks">1 truck</output></div>
    </div>
    <div class="field"><label for="estGross">Weekly gross per truck</label>
      <div class="range-row"><input type="range" id="estGross" min="3000" max="15000" step="250" value="9000"><output id="estGrossOut" for="estGross">$9,000</output></div>
      <p class="hint">Typical OTR weekly gross for this truck type: <b id="estTypical">$8,000 - $10,000</b></p>
    </div>
    <span class="otr">&#9888; OTR operations only &middot; no flat rate</span>
  </div>
  <div class="est-out" aria-live="polite">
    <h3>Estimated dispatch fee</h3>
    <div class="est-big" id="estBig">$450<small> - $540 / week</small></div>
    <div class="est-lines">
      <div><span>Dispatch percentage</span><b id="estPct">5-6%</b></div>
      <div><span>Fee per truck, weekly</span><b id="estPerTruck">-</b></div>
      <div><span>Total fee, weekly</span><b id="estWeekly">-</b></div>
      <div><span>Total fee, monthly (avg)</span><b id="estMonthly">-</b></div>
      <div><span>You keep of gross, weekly</span><b id="estKeep">-</b></div>
    </div>
    <a class="btn btn-red" href="#quote">Request my free quote</a>
    <a class="btn btn-wa" href="{WA_URL}" target="_blank" rel="noopener">{ICONS['wa']}Send on WhatsApp</a>
    <small>{esc(C.PRICING_NOTE)} Gross, rates and earnings are not guaranteed.</small>
  </div>
</div>"""
    body = f"""{phero("Estimate", "Truck Dispatch Fee Calculator &amp; Free Quote", f"See what dispatch costs before you sign. Semi trucks {M['pct'][0]}-{M['pct'][1]}%, small trucks {S['pct'][0]}-{S['pct'][1]}% of weekly gross, for OTR carriers. No flat rate.", ctas=False)}
<section class="sec" style="padding-top:56px"><div class="wrap">
  {calc}
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head center rv"><span class="eyebrow">Pricing at a glance</span><h2>OTR dispatch rates</h2></div>
  {pricing_cards(cta=False)}
</div></section>
<section class="sec" id="quote"><div class="wrap two">
  <div>
    <div class="sec-head rv"><span class="eyebrow">Free quote</span><h2>Request your dispatch quote</h2><p>Send your details and a dispatcher will confirm your percentage and next steps. Written details only; no documents needed at this stage.</p></div>
    {lead_form("quoteForm", "New dispatch quote request", "Request My Free Quote", quote=True)}
  </div>
  <div class="aside">
    {answer(*qa)}
    {contact_side()}
  </div>
</div></section>
<section class="sec sec-dark"><div class="wrap">
  <div class="sec-head rv"><span class="eyebrow">Rate board</span><h2>Rough rates per mile</h2></div>
  {rate_board()}
</div></section>"""
    items = [qa] + [C.FAQS[0], C.FAQS[2], C.FAQS[3]]
    schemas = [service("Truck Dispatch Fee Estimate", desc, "/estimate.html", "Truck dispatch"),
               {"@context": "https://schema.org", "@type": "WebApplication", "name": "Truck Dispatch Fee Calculator",
                "url": url("/estimate.html"), "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
               faq_ld(items), crumbs_ld([("Estimate", "/estimate.html")]), speakable("/estimate.html", title)]
    kw = "truck dispatch calculator, dispatch fee calculator, truck dispatch quote, how much does a truck dispatcher cost, truck dispatcher percentage, dispatch fee per week, owner operator dispatch cost, " + HOME_KW
    write("estimate.html", page("/estimate.html", title, desc, kw, schemas, body, current="estimate.html"))


def build_rates():
    title = "Truck Dispatch Rates 2026: 5-6% Semi, 8-10% Box Truck & Hotshot | Texas Solutions"
    desc = ("Truck dispatch rates and rate-per-mile guide: semi trucks 5-6% of weekly gross, box trucks and hotshots 8-10%, OTR, no flat rate. "
            "Flatbed and hotshot loads often pay $5-6/mile; dry van $2-5/mile depending on local or OTR.")
    qa = ("What are truck dispatch rates in 2026?",
          f"Independent truck dispatchers usually charge a percentage of weekly gross. Texas Solutions charges {M['pct'][0]}-{M['pct'][1]}% for OTR semi trucks and "
          f"{S['pct'][0]}-{S['pct'][1]}% for OTR box trucks, straight trucks and hotshots, with no flat rate. As a rough guide to freight rates, flatbed "
          "and hotshot loads often pay $5-6 a mile and dry van about $2-5 a mile depending on local or OTR lanes.")
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
    <p>Dry van freight has the widest range, roughly $2 to $5 a mile. Short local and regional loads often pay more per mile because the load is short, while long OTR runs pay less per mile but more per load. Our published dispatch percentages apply to OTR operations.</p>
    <h2>Example: what dispatch costs on a typical week</h2>
    <ul>
      <li>Semi truck grossing {money(M['gross'][0])}-{money(M['gross'][1])}: fee about {SEMI_FEE[0]}-{SEMI_FEE[1]} a week at {M['pct'][0]}-{M['pct'][1]}%.</li>
      <li>Box truck or hotshot grossing {money(S['gross'][0])}-{money(S['gross'][1])}: fee about {SMALL_FEE[0]}-{SMALL_FEE[1]} a week at {S['pct'][0]}-{S['pct'][1]}%.</li>
      <li>No setup fee, no monthly subscription, no flat weekly charge.</li>
    </ul>
  </div>
  <div class="aside">{contact_side()}</div>
</div></section>
{band()}"""
    items = [qa, C.FAQS[0], C.FAQS[3], C.FAQS[2], C.FAQS[7]]
    schemas = [service("Truck Dispatch Rates", desc, "/truck-dispatch-rates.html", "Truck dispatch"), faq_ld(items),
               crumbs_ld([("Dispatch Rates", "/truck-dispatch-rates.html")]), speakable("/truck-dispatch-rates.html", title)]
    kw = "truck dispatch rates, dispatch rates per mile, flatbed rates per mile, hotshot rates per mile, dry van rates per mile, truck dispatcher percentage, dispatch fee, 5 percent dispatch, 10 percent dispatch, " + HOME_KW
    write("truck-dispatch-rates.html", page("/truck-dispatch-rates.html", title, desc, kw, schemas, body, current="truck-dispatch-rates.html"))


def build_contact():
    title = "Contact a Truck Dispatcher | Call or WhatsApp (838) 910-3147 | Texas Solutions"
    desc = "Talk to a Texas Solutions truck dispatcher. Call or WhatsApp (838) 910-3147, email info@texassolutions.co, or send your details. Office: 401 W Kentucky Ave, Midland, TX."
    body = f"""{phero("Contact", "Talk to a Truck Dispatcher", "Tell us about your truck, authority and lanes. The fastest way to reach us is WhatsApp.", ctas=False)}
<section class="sec" style="padding-top:56px"><div class="wrap two">
  <div>{lead_form("contactForm", "New dispatch inquiry", "Send My Details")}</div>
  <div class="aside">{contact_side()}
    {answer("Is there a fee to talk to a dispatcher?", f"No. The first call is free. Paid dispatch is {M['pct'][0]}-{M['pct'][1]}% of weekly gross for OTR semis and {S['pct'][0]}-{S['pct'][1]}% for small trucks, with no flat rate or setup fee.", "Good to know")}
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
             ("Plain pricing", f"{M['pct'][0]}-{M['pct'][1]}% of weekly gross for OTR semis, {S['pct'][0]}-{S['pct'][1]}% for small trucks. No setup charge, no flat rate, no monthly subscription."),
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
    desc = f"Answers about truck dispatch: how much a dispatcher costs ({M['pct'][0]}-{M['pct'][1]}% semi, {S['pct'][0]}-{S['pct'][1]}% small trucks), OTR vs local, contracts, paperwork and getting started."
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
    write(name, page("/" + name, title, desc, "Texas Solutions dispatch " + crumb.lower(), [crumbs_ld([(crumb, "/" + name)])], body))


def build_landing(p):
    kind = C.PRICING[p["kind"]]
    lo, hi = fee_range(p["kind"])
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
    <p>{kind['label']} on OTR pay <b>{kind['pct'][0]}-{kind['pct'][1]}% of weekly gross</b>. With typical weekly gross of {money(kind['gross'][0])}-{money(kind['gross'][1])}, the dispatch fee is about {lo}-{hi} a week. No flat rate, no setup fee and no monthly subscription. <a href="estimate.html?type={p['kind']}">Estimate your fee</a>.</p>"""
    faqs = p["faqs"] + [C.FAQS[0], C.FAQS[5]]
    others = "".join(f'<a class="chip" href="{o["file"]}">{esc(o["nav"])}</a>' for o in C.LANDING if o["file"] != p["file"])
    body = f"""{phero(p['nav'], esc(p['h1']), esc(p['lede']), extra=f'<div class="chip-row" style="justify-content:flex-start"><span class="chip" style="background:rgba(255,255,255,.08);color:#fff;border-color:rgba(255,255,255,.2)"><b style="color:#ffb3a6">{kind["pct"][0]}-{kind["pct"][1]}%</b> of weekly gross</span><span class="chip" style="background:rgba(255,255,255,.08);color:#fff;border-color:rgba(255,255,255,.2)">OTR &middot; No flat rate</span></div>')}
<section class="sec" style="padding-bottom:0"><div class="wrap">{answer(p['h1'] if p.get('guide') else f"What is {p['nav'].lower()} from Texas Solutions?", p['answer'])}</div></section>
<section class="sec"><div class="wrap two">
  <div class="prose rv">
{body_p}{sections}{what}
  </div>
  <div class="aside">
    <div class="price feat"><h3>{kind['label']}</h3><div class="amt">{kind['pct'][0]}-{kind['pct'][1]}%<small> of weekly gross</small></div><ul><li>OTR operations</li><li>No flat rate or setup fee</li><li>About {lo}-{hi}/week on typical gross</li></ul><a class="btn btn-red" href="estimate.html?type={p['kind']}">Get a Free Estimate</a></div>
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
                        "datePublished": "2026-09-01", "dateModified": TODAY, "author": {"@id": BUSINESS_ID},
                        "publisher": {"@id": BUSINESS_ID}, "mainEntityOfPage": url(path), "image": OG_IMAGE})
    write(p["file"], page(path, p["title"], p["description"], p["keywords"] + ", " + ", ".join(C.CORE_KEYWORDS[:8]), schemas, body, og_type=og))


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


def build_site_files():
    pages = [("/", "1.0", "weekly"), ("/estimate.html", "0.9", "weekly"), ("/truck-dispatch-rates.html", "0.9", "weekly")]
    pages += [("/" + p["file"], "0.8", "monthly") for p in C.LANDING]
    pages += [("/faq.html", "0.7", "monthly"), ("/about.html", "0.6", "monthly"), ("/contact.html", "0.6", "monthly"),
              ("/privacy.html", "0.2", "yearly"), ("/terms.html", "0.2", "yearly")]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><changefreq>{f}</changefreq><priority>{pr}</priority></url>" for p, pr, f in pages]
    xml.append("</urlset>")
    write("sitemap.xml", "\n".join(xml) + "\n")
    write("urls.txt", "\n".join(url(p) for p, _, _ in pages) + "\n")

    bots = ["Googlebot", "Bingbot", "Slurp", "YandexBot", "DuckDuckBot", "Applebot", "Applebot-Extended", "GPTBot", "OAI-SearchBot",
            "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended",
            "Gemini-Deep-Research", "CCBot", "Meta-ExternalAgent", "Amazonbot", "cohere-ai", "MistralAI-User"]
    robots = ["# Search engines and AI answer engines are welcome.", "User-agent: *", "Allow: /",
              "Disallow: /head-codes.html", "Disallow: /tools/", ""]
    for b in bots:
        robots += [f"User-agent: {b}", "Allow: /", "Disallow: /tools/", ""]
    robots += [f"Host: {C.BASE.replace('https://', '')}", f"Sitemap: {C.BASE}/sitemap.xml"]
    write("robots.txt", "\n".join(robots) + "\n")
    write(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)

    q = []
    for a, b in C.FAQS + [(x, y) for p in C.LANDING for x, y in p["faqs"]]:
        q += [f"Q: {a}", f"A: {b}", ""]
    llms = [
        f"# {C.BRAND}", "",
        f"> Texas Solutions is a US truck dispatch service for owner-operators and small fleets, based in {C.CITY}, Texas. "
        f"Pricing: {M['pct'][0]}-{M['pct'][1]}% of weekly gross for OTR semi trucks (dry van, reefer, flatbed, step deck, power only; typical weekly gross "
        f"{money(M['gross'][0])}-{money(M['gross'][1])}) and {S['pct'][0]}-{S['pct'][1]}% for OTR small trucks (box truck, straight truck, hotshot; typical weekly gross "
        f"{money(S['gross'][0])}-{money(S['gross'][1])}). No flat rate, no setup fee, no monthly subscription, no forced loads. "
        "Texas Solutions is not a motor carrier or freight broker and does not guarantee loads, rates or earnings.", "",
        "## Key facts",
        f"- Service: truck dispatch (load search, rate negotiation, broker setup packets, rate confirmations, lane planning)",
        f"- Semi truck dispatch fee: {M['pct'][0]}-{M['pct'][1]}% of weekly gross (OTR) - about {SEMI_FEE[0]}-{SEMI_FEE[1]} per week on typical gross",
        f"- Box truck / straight truck / hotshot dispatch fee: {S['pct'][0]}-{S['pct'][1]}% of weekly gross (OTR) - about {SMALL_FEE[0]}-{SMALL_FEE[1]} per week on typical gross",
        f"- Condition: {C.PRICING_CONDITION}",
        "- No flat rate, no setup fee, no monthly subscription, no long-term contract",
        "- Rough freight rates: flatbed and hotshot about $5-6 per mile; dry van about $2-5 per mile depending on local or OTR",
        "- Area served: United States (48 states), with a focus on Texas and the Permian Basin",
        f"- Phone: {C.PHONE} | WhatsApp: +1 838 910 3147 (https://wa.me/{C.WHATSAPP}) | Email: {C.EMAIL}",
        f"- Address: {C.STREET}, {C.CITY}, {C.REGION} {C.POSTAL}", "",
        "## Pages",
        f"- [Home]({url('/')}): truck dispatch service overview and pricing",
        f"- [Dispatch fee calculator and free quote]({url('/estimate.html')})",
        f"- [Truck dispatch rates and rate-per-mile guide]({url('/truck-dispatch-rates.html')})",
        *[f"- [{p['nav']}]({url('/' + p['file'])}): {p['answer']}" for p in C.LANDING],
        f"- [FAQ]({url('/faq.html')})", f"- [About]({url('/about.html')})", f"- [Contact]({url('/contact.html')})", "",
        "## Questions and answers", *q,
        "## Related", f"- [Texas Solutions software development, AI and QA]({C.MAIN_SITE}/)", "",
    ]
    write("llms.txt", "\n".join(llms))


def main():
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
    build_404()
    build_site_files()
    print("built", 7 + len(C.LANDING) + 1, "pages")


if __name__ == "__main__":
    main()
