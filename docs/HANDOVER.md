# dispatch.texassolutions.co: audit and handover (October 2026)

This is the audit of the live site against the "USA Trucking Traffic & Lead
Generation" developer proposal, followed by what was changed, how it works and
how to run it. Existing tools and URLs were kept and upgraded. Nothing was
rebuilt from scratch, and no public URL changed.

Status labels describe the site **before** this work:
**Available** · **Needs Improvement** · **Missing** · **Requires Verification**.
The "Now" column says what was done.

## 1. Audit

### Positioning and access
| Requirement | Status | Evidence | Now |
|---|---|---|---|
| Nationwide positioning: "Truck Dispatch Services & Free Trucking Tools for USA Owner-Operators" | Needs Improvement | H1 "Truck Dispatch Service that keeps your truck loaded"; tools only in the nav and lower on the page | Eyebrow uses the positioning line, H1 "USA Truck Dispatch Service...", tool links in the hero, meta description mentions free tools |
| Dispatch services and free tools reachable from every page | Available | Header "Dispatch Services" and "Tools" menus, footer links | Kept; 4 more tool cards on the home page |

### Findings in the proposal
| Finding | Status | Evidence | Now |
|---|---|---|---|
| 13 calculators exist | Available | Verified: estimate, fuel + 11 hub tools | Upgraded in place; 15 tools now |
| Load profit lacks dispatch/factoring inputs | Needs Improvement (confirmed) | Inputs were rate, loaded, deadhead, tolls, CPM only | Rebuilt on the same URL (section 4) |
| Box-truck page shows mixed-equipment rate board | Needs Improvement (confirmed) | Same 10 semi/hotshot lanes on every page | Each service page shows only its own equipment; 5 box-truck example lanes added |
| Rate boards labelled "today" while illustrative | Needs Improvement (confirmed) | Header showed a live clock and rows flashed in rotation | Clock and flashing removed; "Example lanes · illustrative examples, not live rates" |
| Fuel calculator and Texas page showed different dates | Requires Verification → pipeline healthy | Daily commits 21 Sep-2 Oct; both live pages showed 2 Oct when checked. Real problems found: calculator note said "EIA weekly average" when AAA daily was used, footnote called all prices "EIA regional weekly", browser refresh updated the week but not the day, nothing marked stale data | Shared fuel-data service (section 6) |
| Blog already covers the six themes | Available | Posts exist for all six | Improved in place (section 7) |

### Keyword-to-page plan
| Page | Primary candidate keyword | Status | Now |
|---|---|---|---|
| Home | truck dispatch service | Available | Positioning improved |
| owner-operator-dispatch.html | owner operator dispatch service | Available | Tool links in sidebar |
| box-truck-dispatch.html | box truck dispatch service | Needs Improvement | Box-truck-only examples, tool links |
| hotshot-dispatch.html | hotshot dispatch service | Available | Hotshot-only examples, tool links |
| dry-van-dispatch.html | dry van dispatch service | Available | Dry-van-only examples |
| reefer-dispatch.html | reefer dispatch service | Available | Reefer rate guide only (too few example lanes for a board) |
| flatbed-dispatch.html | flatbed dispatch service | Available | Kept combined with step deck: no evidence that a split is justified |
| power-only-dispatch.html | power only dispatch service | Available | Power-only rate guide only |
| truck-fuel-cost-calculator.html | truck fuel cost calculator | Available | Priority tool upgraded |
| cost-per-mile-calculator.html | trucking cost per mile calculator | Available | Priority tool upgraded |
| load-profitability-calculator.html | load profitability calculator | Needs Improvement | Priority tool rebuilt + compare two loads |
| deadhead-miles-calculator.html | deadhead miles calculator | Available | Validation, example, toolbar |
| estimate.html | dispatch fee calculator | Available | Toolbar, analytics |
| diesel-prices/[state].html | diesel prices in [state] | Needs Improvement | Same record drives title, summary, tables, calculator default |
| fuel-surcharge-calculator.html | fuel surcharge calculator | Missing | **New** |
| detention-pay-calculator.html | detention pay calculator | Missing | **New** |
| Search volume and difficulty | n/a | Requires Verification | Not invented. Validate with USA-filtered Search Console and Keyword Planner before reprioritising |
| Equipment-specific fuel pages | n/a | Available | Sections per truck on the fuel page plus `?truck=` links (canonical to the main page). No thin new pages created |

### All calculators
| Requirement | Status | Now |
|---|---|---|
| No signup | Available | Kept |
| Mobile-friendly inputs and readable results | Available | Kept; mobile contact bar no longer covers results |
| Formulas, units, assumptions shown | Needs Improvement (fuel page had no formula list, units implicit) | Formula lists with units on every tool |
| Validate empty, negative, zero-denominator | **Missing**: empty inputs became 0 and `Math.max(1, ...)` hid zero miles | Shared validation; the offending field is highlighted with a plain message |
| "Enter your details" instead of a $0 result | Needs Improvement (fuel page rendered "$0 for 0 miles") | Every result shows "Enter your details" until inputs are valid |
| Reset, print, optional local saving | **Missing** | Reset / Print / Save on this device / Share tool on every calculator |
| Worked example | **Missing** | On all 15 tools, matching the values each tool opens with |
| FAQs | Available | Kept, extended on upgraded tools |
| Link to next calculator and a service | Available / Needs Improvement | Related calculators kept; dispatcher prompt with service link added |
| Dispatcher prompt below the result | Needs Improvement | Added on every tool page |
| Saved scenarios / URL parameters must not create indexed duplicates | Available | Every page has a self-canonical; saving uses browser storage only; share links add only UTM tags |

### Priority tools
| Tool | Requirement | Status | Now |
|---|---|---|---|
| Fuel | Editable MPG, loaded/deadhead miles, idle and reefer fuel, manual price | Available | Kept; manual price labelled "your price" |
| Fuel | Diesel/gasoline where relevant | **Missing** | Fuel-type selector for hotshot, box and straight trucks; gasoline state averages added to the data |
| Fuel | Source/date labels | Needs Improvement | Source, date and stale status shown next to the price and in the result |
| CPM | Separate fixed and variable costs | Available | Kept |
| CPM | Owner-driver labor explicit | Needs Improvement (one "driver pay" field) | Hired driver pay (variable) and own pay (monthly) separate; CPM shown before and after own pay |
| CPM | Total miles vs loaded miles | **Missing** | Both inputs; cost per loaded mile and deadhead share shown |
| Load profit | Dispatch and factoring fees with fee basis | **Missing** | Dispatch % and factoring %, per-fee choice of whether other pay is included |
| Load profit | Double-counting protection | **Missing** | "Only costs not already in your CPM" + "my CPM already includes the fees" switch |
| Load profit | Return/repositioning miles, effective RPM, profit, target rate | Partly Available | Return miles, break-even and target linehaul added; result labelled "estimated profit based on entered costs" |

### New tools
| Tool | Status | Now |
|---|---|---|
| Fuel surcharge | Missing | Three contract methods (per-mile, step in ¢/mile, step in % of linehaul), rounding and below-base options. Never presented as one universal formula |
| Detention pay | Missing | Appointment, arrival and release (overnight OK), free time, rate, increment and rounding, optional cap, late/early-arrival notes, documentation note |
| Compare two loads | Missing | On the load profit page: save Load A, compare profit, miles, driving time, profit per mile and per hour. No claims about reloads |

### Fuel data reliability
| Requirement | Status | Now |
|---|---|---|
| One shared fuel-data service | Needs Improvement (one file, but each page re-implemented the lookup) | `tools/fuel_data.py`, mirrored in `js/site.js` (`TS.fuelResolve`) |
| Record fields: geography, fuel, price, source, observation date, fetch time, level, status | **Missing** (only file-level day and week) | Every record carries them; status is computed against today's date |
| Permitted feeds | Requires Verification | EIA is public domain. AAA's state averages are read from its public page; review AAA's terms periodically and consider a licensed feed (e.g. OPIS) for daily state data |
| Weekly EIA never shown as a daily state value | Needs Improvement | Fallback rows say "EIA weekly regional" and name the region |
| On failure keep the last value with its real date and a stale label | Needs Improvement (kept the value but still said "today") | Per-record dates kept; "today" wording only when fresh, "latest" plus a stale badge otherwise |
| Manual price entry | Available | Kept |
| Never invent a value | Available | Kept; with no data the calculator asks for a pump price |
| Title, summary, tables and calculator defaults from one record | Needs Improvement | Done |

### Search
| Requirement | Status | Evidence |
|---|---|---|
| Important pages return 200 and are indexable | Available | 96 of 96 sitemap URLs returned 200 on 3 Oct; robots allow; meta robots index |
| Title, description, canonical, one H1 | Available | `tools/audit.py`: 0 errors on 99 pages; every page has exactly one H1 |
| Content in rendered HTML | Available | Static HTML; calculators add results only |
| Robots and sitemap | Available | New pages are added to `sitemap-tools.xml` automatically |
| Crawlable links | Available | Plain `<a href>` |
| Structured data matches visible content | Available | Audit checks that FAQ questions are visible; no Offer/WebApplication markup |
| Permanent redirects for changed URLs | Available | No URL changed |
| **HTTP to HTTPS** | **Requires Verification** | `http://dispatch.texassolutions.co/` returned 200 with no redirect. Turn on "Enforce HTTPS" in GitHub → repo Settings → Pages |
| Social previews | Needs Improvement (one image for every page) | Per-tool 1200x630 images in `assets/og/` |
| Doorway / scaled content | Available | One location page (Texas). The 51 state diesel pages each carry distinct daily data; no city pages added |

### Conversion
| Requirement | Status | Now |
|---|---|---|
| Call, Text, WhatsApp, Request Callback easy on mobile | Needs Improvement (Call button hidden under 1040px, no Text, no Callback) | Fixed bottom bar on phones: Call · Text · WhatsApp · Callback; floating WhatsApp button hidden there so nothing overlaps |
| Short first form (name, phone or email, equipment, home state, trucks, MC status, contact method) | Needs Improvement (10 fields incl. MC/DOT numbers, company, lanes) | Exactly those 7 plus an optional note; phone **or** email required |
| Documents after the first conversation | Available | Stated next to the form and in "Next steps" |
| Verified reviews, dispatcher intros, permission-based case studies | **Missing** | **Needs owner input.** Not written: nothing may be invented |
| Store inquiries reliably | **Requires Verification** | Web3Forms emails each lead; there is no database or CRM. Needs a decision (section 4) |
| Prevent duplicate submissions | **Missing** | In-flight lock + same person/form blocked for 30 minutes in the session |
| Surface delivery failures to staff | **Missing** | Visitor sees a call/WhatsApp fallback with their details; `lead_form_error` event in GA4. Real staff alerting needs a backend |
| Keep SMS consent wording and version with the lead | **Missing** | `sms_consent`, `sms_consent_text` and `sms_consent_version` sent with every lead |
| Tools directory privacy wording | Needs Improvement ("Nothing is stored") | Now separates device-only saving, analytics counts and emailed forms |
| Callback request | **Missing** | Callback form on contact.html#callback |

### Analytics
| Requirement | Status | Now |
|---|---|---|
| GA4 | Available (G-ZKMGJ4L8NG) | Events added (section 5). Local/staging hosts no longer send data |
| Search Console | Requires Verification | Verification tag is present; confirm the owner's access |
| Event table | **Missing** | All 8 events implemented, plus `share` and `lead_form_error` |
| No names, phones, emails, MC/DOT in events | n/a | Enforced in `TS.track` callers; checked in QA |
| Completed-call attribution | Requires decision | Phone taps are not calls. Needs a call-tracking provider if wanted |
| CRM lead stages new → contacted → qualified → onboarding → signed/lost | **Missing** | Needs a CRM choice |
| Baseline before targets | Requires Verification | Collect about 4 weeks of data after launch first |

### Distribution
| Requirement | Status | Now |
|---|---|---|
| Shareable tool links | Missing | "Share tool" on every calculator: `?utm_source=share&utm_medium=tool_link&utm_campaign=<tool>` |
| Social-preview images | Needs Improvement | Done for all tools |
| Consistent UTM attribution | Missing | First touch per session is stored and sent with each lead (`attribution_*` fields) and added to events |
| Videos, community posts, partnerships, Search Ads | n/a | Marketing tasks, outside the build |

## 2. URL inventory

98 public URLs, all in `urls.txt` and the sitemaps. Two are new: `/fuel-surcharge-calculator.html` and `/detention-pay-calculator.html`. Every page was built and audited locally (0 errors). All pre-existing URLs returned 200 on the live site on 3 Oct 2026. After deploying, re-run the live check (section 7).

## 3. Data sources (`data/fuel-prices.json`)

| Fuel | Level | Source | Cadence | Used for |
|---|---|---|---|---|
| Diesel, gasoline (regular) | State (50 + DC) | AAA state averages, gasprices.aaa.com | Daily | Default price per state |
| Diesel, gasoline | U.S. + 10 regions | U.S. EIA weekly retail prices (public domain) | Weekly (Monday) | U.S. average; regional fallback only when a state has no daily value |

- `tools/fuel_prices.py` fetches (Action `fuel-prices.yml`, 11:15 and 17:15 UTC) and commits only on change.
- Each record has `price`, `observed` (source date) and `fetched` (when it was taken). A failed or partial fetch keeps the old records with their old dates.
- Status: daily data is **fresh** for up to 2 days after its observation date, weekly data for 9 days; after that it is **stale**. No value at all means **unavailable** (the calculator asks for a pump price). Change `MAX_AGE` in `tools/fuel_data.py`.
- Pages say "today" only when data is fresh, otherwise "latest" with a stale badge.

## 4. Decisions needed from the owner

1. **Lead storage and staff alerts.** Web3Forms only emails. Options: keep email-only, add Web3Forms' paid webhook into a Google Sheet or CRM, or reuse the main site's Vercel `/api/submit` endpoint with a database.
2. **CRM** for the stages new → contacted → qualified → onboarding → signed/lost.
3. **Call tracking**, if completed calls must be attributed to sources.
4. **Trust content.** Real reviews (with permission), dispatcher introductions, case studies with dated evidence that separates gross from profit.
5. **Privacy policy, section 1.** Legal text is kept verbatim, so this wasn't changed. Suggested replacement:
   > We collect the information you give us when you send an inquiry, request a callback or contact us: your name, phone number and/or email address, equipment type, home state, number of trucks, MC authority status, preferred contact method, any message you add and, if you agree to texts, the SMS consent wording and version you agreed to. We record which page and campaign brought you to the site. We use Google Analytics to count page visits and calculator use; it does not receive what you type into calculators or forms. If you choose "Save on this device" in a calculator, your inputs are stored only in your browser's local storage.
6. **GitHub Pages "Enforce HTTPS"** (see Search).
7. **GA4 admin.** Register custom dimensions `tool_name`, `equipment`, `link_location`, `form_id`, `method`, `error_type`. Mark `lead_form_submit` and `callback_request` as key events.

## 5. Analytics events

| Event | Fires when | Parameters |
|---|---|---|
| `tool_start` | First real input in a calculator (once per page view) | `tool_name` |
| `tool_calculate` | A valid result has settled for 1.5 s after typing stops; once per distinct set of inputs | `tool_name`, `equipment` (fuel, dispatch fee) |
| `tool_export` | Print, Save on this device, or "Save as Load A" | `tool_name`, `method` (`print`, `save_device`, `compare_save`) |
| `share` | Share tool link shared or copied | `method`, `content_type=tool`, `item_id` |
| `click_call` | `tel:` link tapped (a tap, not a confirmed call) | `link_location`, `tool_name` when inside a tool |
| `click_text` | `sms:` link tapped | `link_location` |
| `click_whatsapp` | `wa.me` link tapped, or the WhatsApp quote button | `link_location`, `equipment` on the quote |
| `lead_form_submit` | Web3Forms confirms an inquiry was accepted | `form_id`, `equipment`, `trucks`, `mc_status`, `contact_method`, `sms_consent` |
| `callback_request` | Web3Forms confirms a callback request | `form_id`, `sms_consent` |
| `lead_form_error` | A submission failed (network or rejected) | `form_id`, `error_type` |

Every event also carries `page_path` and, when the session arrived with UTM tags, `campaign_source`, `campaign_medium` and `campaign_campaign`. Events never include name, phone, email, MC or DOT numbers. On any host other than `*.texassolutions.co`, GA4 is disabled and events are logged to the console (`TS.events`) for QA.

## 6. Calculator formulas

Each formula is also printed on its tool page with units.

- **Load profit:** `profit = L + O - d*(L + O_d) - f*(L + O_f) - M*C - A`, where L = linehaul, O = other pay, O_d/O_f = other pay if that fee applies to it, M = loaded + deadhead + return miles, C = cost per mile, A = extra trip expenses. When both fees apply to all revenue R this is `R*(1-d-f) - M*C - A`. Required linehaul for profit P: `(M*C + A + P - O + d*O_d + f*O_f) / (1-d-f)`; break-even uses P = 0. "My CPM already includes the fees" sets d = f = 0.
- **Cost per mile:** fixed per mile = monthly fixed / total miles; operating CPM = fixed per mile + fuel + maintenance + hired driver pay; all-in = operating + own pay / total miles; per loaded mile = all-in × total / loaded.
- **Fuel cost:** mpg = empty mpg / (1 + k × cargo lbs / 1000) minus a speed penalty above 62 mph (or the user's MPG); gallons = miles / mpg + idle h × idle gph + reefer h × 0.8; cost = gallons × price.
- **Fuel surcharge:** per-mile method `(current - base) / MPG`; step methods `steps = (current - base) / step` (completed or rounded up), then `steps × cents` or `linehaul × steps × %`; total = per mile × miles; below base = 0 unless credit is chosen.
- **Detention:** clock start = arrival, or the appointment if arrival was earlier; eligible = release - start - free time (minimum 0); billable = eligible in increments (completed, rounded up or nearest), capped; pay = billable hours × rate.
- Break-even, deadhead, driver pay, IFTA, per diem, truck loan, maintenance, HOS and freight class are unchanged apart from validation.

## 7. QA results (3 October 2026, local build)

- Every calculator's opening result matches its published worked example: estimate $450; fuel $1,011 (175.0 gal × $5.777 TX); CPM $1.50/$1.10/$1.70; load profit $1,173, required $1,995, break-even $1,125; break-even 2,366 mi; deadhead 12.7%/$3.02; driver pay $1,440; per diem $20,700; loan $2,730.24; maintenance $19,800; HOS 11.0; freight class 92.5; fuel surcharge $0.20/mi in all three methods; detention $150.
- Edge cases: empty, negative and zero inputs, fees of 100% or more, loaded miles above total, down payment above price, release before arrival, % method without a linehaul. Each shows "Enter your details" plus a specific message. Load profit with $300 other pay and dispatch excluded from it gives fees $120 / $81 and a required linehaul of $1,678, matching a hand calculation.
- Fuel data: missing state → labelled EIA regional fallback; 13-day-old value → stale; no value → "enter your pump price". Python and browser labels are identical.
- Forms (network stubbed, so nothing was sent): phone-or-email rule, success event once, duplicate blocked, failure shows the fallback and logs `lead_form_error`, consent text and version included.
- Analytics: `tool_start` once, `tool_calculate` once per settled distinct calculation, no personal data in any payload.
- Mobile (375 px): no horizontal scroll; bottom contact bar shown; floating WhatsApp button hidden.
- `python tools/audit.py`: 99 pages, 0 errors, 0 warnings.

**After deploying (production smoke check):**

```bash
while read u; do c=$(curl -s -o /dev/null -w "%{http_code}" "$u"); [ "$c" != 200 ] && echo "$c $u"; done < urls.txt
```

Then send one real test inquiry from the contact page, confirm it arrives in the dispatch inbox, and check GA4 → Reports → Realtime for `lead_form_submit`.

## 8. Operating instructions

- **Edit words or numbers:** `tools/content.py` (rates, FAQs, form options, example lanes, SEO titles) or `tools/site.py` (page layouts, tool definitions, worked examples in `EXAMPLES`). Then run `python tools/site.py` and `python tools/audit.py`, commit and push to `Main`. GitHub Pages deploys in about a minute.
- **Changing a tool's example values:** recompute its entry in `EXAMPLES` so the text still matches the calculator.
- **SMS consent wording:** if `SMS_CONSENT` changes, bump `SMS_CONSENT_VERSION` in `tools/content.py`.
- **Fuel prices:** automatic. To force a refresh, run the "Update diesel prices (daily)" Action manually or run `python tools/fuel_prices.py && python tools/site.py`.
- **Local preview:** `python -m http.server 8765` in the repo, then open http://localhost:8765. Analytics stay off locally.
- **Build needs:** `pip install markdown pyyaml pillow`.

## 9. Keyword map (added 3 October 2026)

Keywords came from the owner's list and are not volume-checked. Validate them in Search Console and Keyword Planner. Only true statements are used: 24/7, remote team, new MC from day one, first load free, back office, and the 8 equipment types. Other equipment (car hauler, cargo/sprinter van, tanker, hazmat, lowboy/RGN, conestoga, dump, oversize) is deliberately **not** targeted.

| Keyword group | Page(s) |
|---|---|
| Core service (truck/trucking dispatch services, truck dispatcher, dispatching company, USA, hire/for hire, independent, professional, 24/7, affordable, reliable, remote) | Home (title, hero, "Trucking dispatch services for every kind of carrier" section, FAQs) |
| Customer type (owner operators, small fleets, small trucking companies, one truck, fleet owners, lease operators) | owner-operator-dispatch.html |
| New authority / new MC / new trucking company / brokers that work with new authority | dispatch-for-new-authority.html (new); blog how-to-start-a-trucking-company |
| Equipment (dry van, reefer, flatbed, step deck, hotshot / hot shot dispatcher, non-CDL hotshot, box truck dispatcher, 26 ft, non-CDL box truck, power only, semi truck) | Each equipment page (titles, body, FAQs); home section |
| Pricing (cost, how much dispatchers charge, fees, percentage, flat rate, cheap/low fee, 5 percent, pricing, no contract, no upfront fee, free trial, pay per load) | truck-dispatch-rates.html (title, three new sections, pricing FAQs); blog how-much-does-a-truck-dispatcher-cost |
| Load and revenue problems (find loads, high paying loads, without load board, direct shipper, dedicated/consistent lanes, no loads, load booking) | blog how-to-find-loads-for-your-truck |
| Negotiation, rate per mile, deadhead | blog how-to-negotiate-freight-rates; blog what-is-deadhead |
| Back office (paperwork, packets, invoicing, billing, factoring + dispatch, IFTA filing, compliance, DOT, MC setup, detention and lumper, ELD support, carrier setup) | trucking-back-office-services.html (new) |
| Comparison (worth it, need a dispatcher, self-dispatch vs, vs load board, DAT vs dispatcher) | blog is-a-truck-dispatcher-worth-it; blog truck-dispatcher-vs-freight-broker |
| Trust (how to choose, scams, legit, questions to ask, reviews, agreement/contract) | blog how-to-choose-a-truck-dispatcher-avoid-scams |
| Informational (what is truck dispatching, how it works, how dispatchers find loads, what percentage) | what-does-a-truck-dispatcher-do.html (new sections); blog broker-setup-rate-confirmation-spot-vs-contract |
| Owner-operator earnings, cost per mile, rate per mile | blog how-much-do-owner-operators-make; existing CPM and rate posts |
| Location (near me, every state, hubs, equipment + state) | truck-dispatch-by-state.html + 49 pages in /truck-dispatch/ + texas-truck-dispatch.html. Each page has its own hubs, highways, freight, ports, lanes and live diesel price from tools/states.py |
| AI assistant questions | FAQ answers on faq.html, home, rates, new authority, back office and equipment pages, plus llms.txt facts |

**Not covered, on purpose:** "freight market trends 2026" (no verified data), and "dispatch service reviews" as a claim (we have no reviews; the scams post explains how to check reviews instead).

**Negative keywords for Google Ads (never used on the site):** truck dispatcher jobs, truck dispatcher training, truck dispatcher course, how to become a truck dispatcher, truck dispatcher salary, dispatcher certification, dispatch software, TMS, free load board, 911, police dispatch, emergency dispatch.

**Review `tools/states.py`** when editing state pages. Less certain items: NE I-76/I-680, NV I-11, secondary hubs Seward, Kent, Dalton and Garden City, and the inland-port names for WV, KS and SC.
