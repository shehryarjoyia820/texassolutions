# texassolutions


## SEO and AEO

`tools/build_seo.py` owns the search and answer-engine layer. Edit `tools/content.py`, then run:

```bash
python tools/build_seo.py
```

It is safe to run repeatedly. It rewrites titles and descriptions, injects canonical, Open Graph and
JSON-LD (LocalBusiness, Service, FAQPage, HowTo, BreadcrumbList, speakable) into every page,
regenerates the equipment, Texas and guide landing pages, and writes `sitemap.xml`, `robots.txt`,
`llms.txt` and `404.html`. The SMS consent text, privacy policy and terms are never touched.

`tools/og-image.mjs` rebuilds `assets/og-image.png` (needs the `sharp` package).

## Header codes and ads.txt

- **Header codes** (Search Console, Bing, Google Analytics, Tag Manager, AdSense, Meta Pixel, Clarity,
  any other snippet): paste into `head-codes.html` below the "PASTE BELOW THIS LINE" marker, run
  `python tools/build_seo.py`, commit and push. The codes are copied into the `<head>` of every page.
- **ads.txt**: edit `ads.txt` in the repository root. AdSense reads the root domain's file, which lives
  in the texassolutions_main repo (`src/config/head-codes.ts`).
