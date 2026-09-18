"""
SEO and AEO build for dispatch.texassolutions.co.

Idempotent: every block it writes sits between <!-- NAME:START --> and
<!-- NAME:END --> markers and is replaced on the next run.

    python tools/build_seo.py

What it does
- Rewrites <title> and meta description, and injects canonical, robots,
  Open Graph, Twitter, font preloading, a no-JavaScript fallback and JSON-LD
  into every page.
- Adds a quick answer, an equipment hub and extra FAQs to the home page, and
  the extra FAQs to faq.html.
- Adds a "Dispatch services" column to every footer.
- Generates the equipment, audience, Texas and guide landing pages.
- Writes sitemap.xml, robots.txt, llms.txt and 404.html.
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

esc = html.escape


# ------------------------------------------------------------------ helpers
def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def write(name, text):
    (ROOT / name).write_text(text, encoding="utf-8", newline="\n")


def url(path):
    return C.BASE + ("/" if path in ("", "/") else path)


def put_block(text, name, block, anchor=None, before=True):
    """Replace a marked block, or insert it at the anchor if absent."""
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    wrapped = f"{start}\n{block}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: wrapped, text, count=1)
    if anchor is None or anchor not in text:
        raise ValueError(f"anchor for {name} not found")
    i = text.index(anchor)
    return text[:i] + wrapped + "\n" + text[i:] if before else text[: i + len(anchor)] + "\n" + wrapped + text[i + len(anchor):]


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


BUSINESS_ID = f"{C.BASE}/#business"


def business():
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": BUSINESS_ID,
        "name": C.NAME,
        "alternateName": C.BRAND,
        "description": "Truck dispatch services for owner-operators and small fleets in the United States: load search, rate negotiation, broker communication and paperwork support.",
        "url": url("/"),
        "logo": LOGO,
        "image": OG_IMAGE,
        "telephone": C.PHONE_E164,
        "email": C.EMAIL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": C.STREET,
            "addressLocality": C.CITY,
            "addressRegion": C.REGION,
            "addressCountry": C.COUNTRY,
        },
        "areaServed": {"@type": "Country", "name": "United States"},
        "knowsAbout": ["Truck dispatch", "Freight dispatch", "Load boards", "Rate negotiation",
                       "Broker setup packets", "Owner-operator trucking"] + [f"{e} dispatch" for e in C.EQUIPMENT],
    }


def service(name, description, path, service_type):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": service_type,
        "description": description,
        "url": url(path),
        "provider": {"@id": BUSINESS_ID},
        "areaServed": {"@type": "Country", "name": "United States"},
        "audience": {"@type": "BusinessAudience", "audienceType": "Owner-operators and small trucking fleets"},
    }


def faq(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items
        ],
    }


def breadcrumb(trail):
    items = [("Home", "/")] + trail
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)
        ],
    }


def speakable(path, name):
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "url": url(path),
        "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["[data-speakable]"]},
    }


def head_block(title, description, path, keywords=None, schemas=(), og_type="website"):
    lines = [
        f'<link rel="canonical" href="{url(path)}">',
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
    ]
    if keywords:
        lines.append(f'<meta name="keywords" content="{esc(keywords)}">')
    lines += [
        '<meta name="theme-color" content="#ec3013">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="{esc(C.BRAND)}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:url" content="{url(path)}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:locale" content="en_US">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(description)}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&amp;display=swap">',
        '<noscript><style>[data-reveal],[data-word]{opacity:1!important;transform:none!important;clip-path:none!important}</style></noscript>',
    ]
    lines += [ld(s) for s in (business(), *schemas)]
    return "\n".join(lines)


def set_title_desc(text, title, description):
    text = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(description)}">', text, count=1)
    return text


def apply_head(text, meta, schemas, og_type="website"):
    text = set_title_desc(text, meta["title"], meta["description"])
    block = head_block(meta["title"], meta["description"], meta["path"], meta.get("keywords"), schemas, og_type)
    return put_block(text, "SEO", block, anchor="</head>")


# --------------------------------------------------------------- fragments
def faq_items_html(items, reveal=True):
    r = " data-reveal" if reveal else ""
    return "\n".join(
        f'      <details class="faq-item"{r}>\n'
        f'        <summary class="faq-summary">{esc(q)}<span class="faq-plus">+</span></summary>\n'
        f'        <p class="faq-answer">{esc(a)}</p>\n'
        f"      </details>"
        for q, a in items
    )


def quick_answer_html(question, answer):
    return (
        '<div class="quick-answer" data-reveal>\n'
        '  <div class="quick-answer-label">Quick answer</div>\n'
        f'  <h2 class="quick-answer-q">{esc(question)}</h2>\n'
        f'  <p class="quick-answer-a" data-speakable>{esc(answer)}</p>\n'
        "</div>"
    )


def equipment_links_html():
    cells = []
    for i, page in enumerate(C.LANDING):
        if page["file"] == "what-does-a-truck-dispatcher-do.html":
            continue
        cells.append(
            f'      <a class="services-cell hub-link" href="{page["file"]}" data-reveal>\n'
            f'        <div class="services-index">{i + 1:02d}</div>\n'
            f'        <h3 style="font-size:21px;margin:14px 0 0">{esc(page["nav"])}</h3>\n'
            f'        <p class="text-muted" style="margin:10px 0 0;font-size:14px;line-height:1.6">{esc(page["lede"])}</p>\n'
            f"      </a>"
        )
    return "\n".join(cells)


FOOTER_COLUMN = "\n".join(
    [
        "    <div>",
        '      <h6 class="text-muted" style="margin:0">Dispatch services</h6>',
        '      <div class="footer-links">',
        *[f'        <a href="{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING],
        f'        <a href="{C.MAIN_SITE}/">Software, AI and QA at texassolutions.co</a>',
        "      </div>",
        "    </div>",
    ]
)

FOOTER_ANCHOR = '    <div>\n      <h6 class="text-muted" style="margin:0">Company</h6>'


def add_footer_column(text):
    return put_block(text, "FOOTER-SERVICES", FOOTER_COLUMN, anchor=FOOTER_ANCHOR)


# ------------------------------------------------------------ existing pages
def build_home():
    t = read("index.html")
    meta = C.PAGES["index.html"]
    faqs_existing = re.findall(
        r'<summary class="faq-summary">(.*?)<span class="faq-plus">\+</span></summary>\s*<p class="faq-answer">(.*?)</p>',
        t, re.S)
    faqs_existing = [(html.unescape(q.strip()), html.unescape(a.strip())) for q, a in faqs_existing]
    faqs_existing = [f for f in faqs_existing if f[0] not in dict(C.EXTRA_FAQS)]

    answer = ("Texas Solutions is a truck dispatch service for owner-operators and small fleets in the United States. "
              "Its dispatchers search for freight, negotiate rates with brokers, handle broker communication and keep "
              "paperwork organized for dry van, reefer, flatbed, step deck, power only, hotshot, box truck and straight "
              "truck carriers. The fee is percentage-based under a signed agreement, with no upfront cost, no long-term "
              "contract and no forced loads.")

    steps = [
        ("Apply", "Tell Texas Solutions about your authority, equipment, lanes, and operating goals."),
        ("Speak With Texas Solutions", "Our team reviews your needs and explains our direct dispatch service."),
        ("Complete Onboarding", "Sign the Texas Solutions dispatch agreement and provide the required carrier documents."),
        ("Start Dispatching", "We begin searching lanes for your truck and coordinate every load with you before it is booked."),
    ]
    schemas = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": C.BRAND, "url": url("/"),
         "publisher": {"@id": BUSINESS_ID}, "inLanguage": "en-US"},
        service("Truck dispatch service", meta["description"], "/", "Truck dispatch"),
        {"@context": "https://schema.org", "@type": "HowTo", "name": "How to start truck dispatch with Texas Solutions",
         "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d} for i, (n, d) in enumerate(steps)]},
        faq(faqs_existing + C.EXTRA_FAQS),
        speakable("/", "Truck dispatch services"),
    ]
    t = apply_head(t, meta, schemas)

    # Keyword-bearing H1 with the same visual design as before.
    t = t.replace(
        '<div class="hero-eyebrow" data-reveal style="color:var(--color-accent-300)">\n'
        '      <span class="live-dot" style="background:var(--color-accent-300)"></span>\n'
        '      Direct dispatch services for carriers\n'
        '    </div>\n'
        '    <h1 class="hero-title" style="color:var(--color-bg)">',
        '<h1 class="hero-eyebrow" data-reveal style="color:var(--color-accent-300);margin:0;font-weight:600">\n'
        '      <span class="live-dot" style="background:var(--color-accent-300)"></span>\n'
        '      Truck dispatch services for owner-operators and small fleets\n'
        '    </h1>\n'
        '    <p class="hero-title" style="color:var(--color-bg)">',
    )
    t = t.replace('      <span data-word>NO UPFRONT COST.</span>\n    </h1>', '      <span data-word>NO UPFRONT COST.</span>\n    </p>')

    hub = f"""<section id="dispatch-services" class="section">
  <div class="wrap">
{quick_answer_html('What is Texas Solutions truck dispatch?', answer)}
    <h6 style="color:var(--color-accent-700);margin:48px 0 0" data-reveal>Dispatch by equipment</h6>
    <h2 data-reveal style="font-size:clamp(30px,4.4vw,56px);letter-spacing:-.025em;margin:14px 0 0;max-width:22ch">TRUCK DISPATCH FOR EVERY RIG.</h2>
    <p data-reveal style="margin:20px 0 0;font-size:16px;line-height:1.65;max-width:68ch">Box truck dispatch, hotshot dispatch, dry van, reefer, flatbed, step deck and power only dispatch for owner-operators and small fleets across the United States, run from our dispatch team in Midland, Texas.</p>
    <div class="services-grid">
{equipment_links_html()}
    </div>
    <p data-reveal style="margin:28px 0 0;font-size:14px"><a href="what-does-a-truck-dispatcher-do.html">What does a truck dispatcher do? Read the guide</a></p>
  </div>
</section>"""
    t = put_block(t, "SEO-HOME", hub, anchor='<section id="services" class="section">')

    # Extra FAQs on the home page.
    faq_section = t.index('<section id="faq"')
    last = t.rindex("</details>", faq_section, t.index("</section>", faq_section)) + len("</details>")
    t = put_block(t, "SEO-FAQ", faq_items_html(C.EXTRA_FAQS), anchor=t[last:last + 1] if False else None) if "<!-- SEO-FAQ:START -->" in t \
        else t[:last] + "\n<!-- SEO-FAQ:START -->\n" + faq_items_html(C.EXTRA_FAQS) + "\n<!-- SEO-FAQ:END -->" + t[last:]

    # Below-the-fold images load lazily.
    t = re.sub(r'<img src="https://images\.unsplash\.com([^"]*)" alt="([^"]*)" style',
               r'<img src="https://images.unsplash.com\1" alt="\2" loading="lazy" decoding="async" width="1300" height="866" style', t)
    t = add_footer_column(t)
    write("index.html", t)


def build_faq_page():
    t = read("faq.html")
    meta = C.PAGES["faq.html"]
    existing = re.findall(
        r'<summary class="faq-summary">(.*?)<span class="faq-plus">\+</span></summary>\s*<p class="faq-answer">(.*?)</p>', t, re.S)
    existing = [(html.unescape(q.strip()), html.unescape(a.strip())) for q, a in existing]
    existing = [f for f in existing if f[0] not in dict(C.EXTRA_FAQS)]
    t = apply_head(t, meta, [faq(existing + C.EXTRA_FAQS), breadcrumb([("FAQ", "/faq.html")])])
    if "<!-- SEO-FAQ:START -->" in t:
        t = put_block(t, "SEO-FAQ", faq_items_html(C.EXTRA_FAQS))
    else:
        last = t.rindex("</details>") + len("</details>")
        t = t[:last] + "\n<!-- SEO-FAQ:START -->\n" + faq_items_html(C.EXTRA_FAQS) + "\n<!-- SEO-FAQ:END -->" + t[last:]
    t = add_footer_column(t)
    write("faq.html", t)


def build_simple(name, crumb):
    t = read(name)
    meta = C.PAGES[name]
    t = apply_head(t, meta, [breadcrumb([(crumb, meta["path"])])])
    t = re.sub(r'<img src="https://images\.unsplash\.com([^"]*)" alt="([^"]*)" style',
               r'<img src="https://images.unsplash.com\1" alt="\2" loading="lazy" decoding="async" width="1300" height="866" style', t)
    if name == "about.html":
        # Equipment tags become links to their dispatch pages.
        links = {"Dry Van": "dry-van-dispatch.html", "Reefer": "reefer-dispatch.html", "Flatbed": "flatbed-dispatch.html",
                 "Step Deck": "flatbed-dispatch.html", "Power Only": "power-only-dispatch.html", "Hotshot": "hotshot-dispatch.html",
                 "Box Truck": "box-truck-dispatch.html", "Straight Truck": "box-truck-dispatch.html"}
        for label, href in links.items():
            t = t.replace(f'<span class="tag tag-outline">{label}</span>', f'<a class="tag tag-outline" href="{href}">{label}</a>')
    t = add_footer_column(t)
    write(name, t)


# ---------------------------------------------------------------- new pages
def page_shell(title, description, head, body, mobile_id, current=None):
    about = read("about.html")
    header = re.search(r'<header class="site-header">.*?</header>', about, re.S).group(0)
    header = header.replace(' aria-current="page"', "").replace("aboutMobileNav", mobile_id)
    footer = re.search(r'<footer class="site-footer no-border">.*?</footer>', about, re.S).group(0)
    footer = add_footer_column(footer) if "FOOTER-SERVICES" not in footer else footer
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="css/styles.css">
<link rel="icon" type="image/png" href="assets/logo/favicon.png">
<link rel="apple-touch-icon" href="assets/logo/apple-touch-icon.png">
<!-- SEO:START -->
{head}
<!-- SEO:END -->
</head>
<body>

{header}

{body}

{footer}

<script src="js/nav.js"></script>
<script src="js/reveal.js"></script>
</body>
</html>
"""


def build_landing(p):
    path = "/" + p["file"]
    is_guide = p["file"].startswith("what-")
    crumb = [("Dispatch services", "/#dispatch-services"), (p["nav"], path)]
    schemas = [
        service(p["nav"] if not is_guide else "Truck dispatch service", p["description"], path,
                "Truck dispatch" if is_guide else p["nav"]),
        faq(p["faqs"]),
        breadcrumb(crumb),
        speakable(path, p["title"]),
    ]
    if is_guide:
        schemas.append({
            "@context": "https://schema.org", "@type": "Article", "headline": p["title"],
            "description": p["description"], "datePublished": TODAY, "dateModified": TODAY,
            "author": {"@type": "Organization", "name": C.NAME}, "publisher": {"@id": BUSINESS_ID},
            "mainEntityOfPage": url(path), "image": OG_IMAGE,
        })
    head = head_block(p["title"], p["description"], path, p["keywords"], schemas, "article" if is_guide else "website")

    intro = "\n".join(f'      <p data-reveal style="margin:0 0 16px;font-size:16px;line-height:1.7;max-width:68ch">{esc(x)}</p>' for x in p["intro"])
    handles = "\n".join(
        f'      <div class="services-cell" data-reveal>\n'
        f'        <div class="services-index">{i + 1:02d}</div>\n'
        f'        <h3 style="font-size:21px;margin:14px 0 0">{esc(h)}</h3>\n'
        f'        <p class="text-muted" style="margin:10px 0 0;font-size:14px;line-height:1.6">{esc(b)}</p>\n'
        f"      </div>"
        for i, (h, b) in enumerate(p.get("handles", []))
    )
    guide = ""
    for heading, bullets in p.get("sections", []):
        items = "\n".join(f"        <li>{esc(b)}</li>" for b in bullets)
        guide += f"""
<section class="section">
  <div class="wrap" style="max-width:1000px">
    <h2 data-reveal style="font-size:clamp(26px,3.6vw,44px);letter-spacing:-.025em;margin:0 0 20px">{esc(heading)}</h2>
    <ul class="guide-list" data-reveal>
{items}
    </ul>
  </div>
</section>"""

    related = "\n".join(
        f'      <a class="tag tag-outline" href="{o["file"]}">{esc(o["nav"])}</a>' for o in C.LANDING if o["file"] != p["file"]
    )
    handles_section = f"""
<section class="section">
  <div class="wrap">
    <h6 style="color:var(--color-accent-700);margin:0" data-reveal>What we handle</h6>
    <h2 data-reveal style="font-size:clamp(28px,4vw,48px);letter-spacing:-.025em;margin:14px 0 0;max-width:22ch">{esc(p['nav'].upper())}, DONE FOR YOU.</h2>
    <div class="services-grid">
{handles}
    </div>
  </div>
</section>""" if handles else ""

    body = f"""<section class="page-hero">
  <div class="wrap">
    <h6 style="color:var(--color-accent-700);margin:0" data-reveal>{esc(p['eyebrow'])}</h6>
    <h1 style="max-width:18ch">
      <span data-word>{esc(p['h1'][0])}</span>
      <span data-word class="accent" style="color:var(--color-accent)">{esc(p['h1'][1])}</span>
    </h1>
    <p class="page-hero-lede" data-reveal>{esc(p['lede'])}</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:28px" data-reveal>
      <a href="contact.html" class="btn btn-primary btn-cta">Talk To A Dispatcher</a>
      <a href="tel:{C.PHONE_E164}" class="btn btn-secondary btn-cta">Call {C.PHONE}</a>
    </div>
  </div>
</section>

<section class="section section-surface">
  <div class="wrap" style="max-width:1000px">
{quick_answer_html(p['answer_q'], p['answer'])}
    <div style="margin-top:36px">
{intro}
    </div>
  </div>
</section>
{handles_section}{guide}

<section class="section section-surface">
  <div class="wrap" style="max-width:1000px">
    <h6 style="color:var(--color-accent-700);margin:0" data-reveal>Common questions</h6>
    <h2 data-reveal style="font-size:clamp(28px,4vw,48px);letter-spacing:-.025em;margin:14px 0 32px">{esc(p['nav'].upper())} FAQ</h2>
    <div class="faq-list">
{faq_items_html(p['faqs'])}
    </div>
    <p class="text-muted" style="margin:24px 0 0;font-size:12px">Texas Solutions does not guarantee any specific load volume, rate, revenue or earnings. Texas Solutions is not a motor carrier or freight broker.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h6 class="text-muted" style="margin:0 0 16px">More dispatch services</h6>
    <div style="display:flex;flex-wrap:wrap;gap:8px">
{related}
    </div>
  </div>
</section>

<section class="section-accent no-border" style="padding:clamp(48px,7vw,96px) var(--section-x)">
  <div class="wrap" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:clamp(24px,4vw,64px);align-items:end">
    <h2 style="font-size:clamp(34px,6vw,84px);line-height:.94;letter-spacing:-.035em;margin:0">TELL US ABOUT YOUR TRUCK.</h2>
    <div>
      <p style="margin:0;font-size:16px;line-height:1.65">Speak with a dispatcher about your authority, equipment and preferred lanes. Nothing is charged upfront and no load is booked without your approval.</p>
      <a href="contact.html" class="btn btn-on-accent btn-cta" style="margin-top:24px">Contact Texas Solutions</a>
    </div>
  </div>
</section>"""
    mobile_id = re.sub(r"[^a-zA-Z]", "", p["file"].replace(".html", "")) + "MobileNav"
    write(p["file"], page_shell(p["title"], p["description"], head, body, mobile_id))


def build_404():
    title = "Page not found | Texas Solutions Truck Dispatch"
    desc = "That page does not exist. Find Texas Solutions truck dispatch services, the FAQ or contact a dispatcher."
    head = "\n".join([
        '<meta name="robots" content="noindex, follow">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&amp;display=swap">',
        '<noscript><style>[data-reveal],[data-word]{opacity:1!important;transform:none!important;clip-path:none!important}</style></noscript>',
    ])
    links = "\n".join(f'      <a class="tag tag-outline" href="/{p["file"]}">{esc(p["nav"])}</a>' for p in C.LANDING)
    body = f"""<section class="page-hero">
  <div class="wrap">
    <h6 style="color:var(--color-accent-700);margin:0">404</h6>
    <h1><span data-word>WRONG TURN.</span><span data-word class="accent" style="color:var(--color-accent)">LET'S REROUTE.</span></h1>
    <p class="page-hero-lede">The page you were looking for is not here. These are the places carriers usually want.</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:28px">
      <a href="/" class="btn btn-primary btn-cta">Home</a>
      <a href="/contact.html" class="btn btn-secondary btn-cta">Talk To A Dispatcher</a>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:36px">
{links}
    </div>
  </div>
</section>"""
    shell = page_shell(title, desc, head, body, "notFoundMobileNav")
    # GitHub Pages serves 404.html from any path depth, so assets need absolute URLs.
    shell = re.sub(r'(href|src)="(?!https?:|/|#|tel:|mailto:)', r'\1="/', shell)
    write("404.html", shell)


# ------------------------------------------------------------- site files
def build_site_files():
    pages = [("/", "1.0", "weekly")] + [(C.PAGES[n]["path"], "0.6", "monthly") for n in ("about.html", "contact.html", "faq.html")]
    pages += [("/" + p["file"], "0.8", "monthly") for p in C.LANDING]
    pages += [(C.PAGES[n]["path"], "0.3", "yearly") for n in ("privacy.html", "terms.html")]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio, freq in pages:
        xml.append(f"  <url><loc>{url(path)}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    xml.append("</urlset>")
    write("sitemap.xml", "\n".join(xml) + "\n")

    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "CCBot", "Meta-ExternalAgent"]
    robots = ["# Search engines and AI answer engines are welcome.", "User-agent: *", "Allow: /", ""]
    for b in bots:
        robots += [f"User-agent: {b}", "Allow: /", ""]
    robots.append(f"Sitemap: {C.BASE}/sitemap.xml")
    write("robots.txt", "\n".join(robots) + "\n")

    faq_lines = []
    for q, a in C.EXTRA_FAQS:
        faq_lines += [f"Q: {q}", f"A: {a}", ""]
    llms = [
        f"# {C.BRAND}",
        "",
        "> Texas Solutions provides truck dispatch services directly to owner-operators and small fleets in the United States: "
        "load search, rate negotiation, broker communication and paperwork support for dry van, reefer, flatbed, step deck, "
        "power only, hotshot, box truck and straight truck carriers. The fee is percentage-based under a signed dispatch "
        "agreement, with no upfront cost, no long-term contract and no forced loads. Texas Solutions is not a motor carrier "
        "or freight broker and does not guarantee loads, rates or earnings.",
        "",
        f"- Location: {C.STREET}, {C.CITY}, {C.REGION}",
        f"- Phone: {C.PHONE}",
        f"- Email: {C.EMAIL}",
        "",
        "## Dispatch services",
        *[f"- [{p['nav']}]({url('/' + p['file'])}): {p['answer']}" for p in C.LANDING],
        "",
        "## Pages",
        f"- [Home]({url('/')})",
        f"- [About]({url('/about.html')})",
        f"- [FAQ]({url('/faq.html')})",
        f"- [Contact]({url('/contact.html')})",
        "",
        "## Questions",
        *faq_lines,
        "## Related",
        f"- [Texas Solutions software development, AI and QA]({C.MAIN_SITE}/)",
        "",
    ]
    write("llms.txt", "\n".join(llms))


def patch_css():
    css = read("css/styles.css")
    # Fonts now load from <head> with preconnect instead of a blocking @import.
    css = css.replace("@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&display=swap');\n", "")
    extra = """
/* — SEO additions: quick answer, hub links, guide lists — */
.hero-title { font-family: var(--font-heading); font-weight: var(--font-heading-weight); }
.quick-answer { border-left: 4px solid var(--color-accent); background: var(--color-bg); padding: clamp(20px, 3vw, 32px); box-shadow: var(--shadow-sm); }
.section-surface .quick-answer { background: var(--color-bg); }
.quick-answer-label { font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--color-accent-700); }
.quick-answer-q { font-size: clamp(20px, 2.2vw, 26px); margin: 10px 0 0; letter-spacing: -.01em; }
.quick-answer-a { margin: 12px 0 0; font-size: 16px; line-height: 1.7; max-width: 75ch; }
a.hub-link { display: block; color: inherit; text-decoration: none; transition: background .2s ease; }
a.hub-link:hover { background: var(--color-surface); color: inherit; }
a.hub-link:hover h3 { color: var(--color-accent); }
.guide-list { margin: 0; padding-left: 20px; font-size: 16px; line-height: 1.7; max-width: 72ch; }
.guide-list li { margin-bottom: 10px; }
.guide-list li::marker { color: var(--color-accent); }
a.tag { text-decoration: none; }
"""
    # Remove any earlier copy of the block (including an old HTML-comment style), then append.
    css = re.sub(r"\n*/\* (?:<!-- )?SEO-CSS:START.*?SEO-CSS:END(?: -->)? \*/\n?", "", css, flags=re.S)
    css = css.rstrip() + "\n\n/* SEO-CSS:START */\n" + extra.strip() + "\n/* SEO-CSS:END */\n"
    write("css/styles.css", css)


def main():
    patch_css()
    for p in C.LANDING:
        build_landing(p)
    build_home()
    build_faq_page()
    build_simple("about.html", "About")
    build_simple("contact.html", "Contact")
    build_simple("privacy.html", "Privacy Policy")
    build_simple("terms.html", "Terms & Conditions")
    build_404()
    build_site_files()
    print(f"built {len(C.LANDING)} landing pages and updated 6 pages")


if __name__ == "__main__":
    main()
