"""
All words and numbers for dispatch.texassolutions.co.
Edit here, then run:  python tools/site.py

Pricing (OTR only, no flat rate, % of weekly gross):
  Semi trucks (dry van, reefer, flatbed, step deck, power only): 5%,
      typical weekly gross $8,000-$10,000
  Box truck and straight truck: 8%; hotshot: 7%;
      typical weekly gross $7,000-$9,000
"""

BASE = "https://dispatch.texassolutions.co"
MAIN_SITE = "https://texassolutions.co"
NAME = "Texas Solutions"
BRAND = "Texas Solutions Truck Dispatch"
PHONE = "(838) 910-3147"
PHONE_E164 = "+18389103147"
WHATSAPP = "18389103147"
WHATSAPP_TEXT = "Hi Texas Solutions, I'd like to know more about your truck dispatch service."
EMAIL = "dispatch@texassolutions.co"
STREET = "401 W Kentucky Ave"
CITY = "Midland"
REGION = "TX"
POSTAL = "79701"
COUNTRY = "US"
HOURS = "Dispatchers available 24/7 by call, text or WhatsApp"

# Web3Forms delivers form submissions by email (existing account).
WEB3FORMS_KEY = "acb4c65c-c969-44a9-8bee-31407b1b23d6"

# -------------------------------------------------------------- pricing
PRICING = {
    "small": {
        "label": "Small trucks",
        "equipment": ["Box Truck", "Straight Truck", "Hotshot"],
        "pct": (7, 8),  # hotshot 7%, box and straight truck 8% (see EQ_PCT)
        "gross": (7000, 9000),
    },
    "semi": {
        "label": "Semi trucks",
        "equipment": ["Dry Van", "Reefer", "Flatbed", "Step Deck", "Power Only"],
        "pct": (5, 5),
        "gross": (8000, 10000),
    },
    # MC lease (lease-on to a partner carrier's authority). Not part of the dispatch fee calculator.
    "lease": {
        "label": "MC lease",
        "equipment": ["Lease-on"],
        "pct": (18, 20),
        "gross": (8000, 10000),
    },
}
# Dispatch percentage for each truck type.
EQ_PCT = {"Dry Van": 5, "Reefer": 5, "Flatbed": 5, "Step Deck": 5, "Power Only": 5,
          "Box Truck": 8, "Straight Truck": 8, "Hotshot": 7}
PRICING_CONDITION = "Rates apply to OTR (over-the-road) operations. Local and regional work is quoted separately."
COVERAGE = "Nationwide truck dispatch for owner-operators and small fleets across the USA."
OFFICE_VS_COVERAGE = "Office: 401 W Kentucky Ave, Midland, TX 79701. Service coverage: nationwide across the USA, with remote dispatchers across US time zones."
AK_HI_NOTE = "Carriers based in Alaska or Hawaii can contact us about their mainland USA operations."
AGREEMENT_NOTE = "No long-term contract. A signed dispatch agreement sets your percentage and the notice period before we book loads."
FIRST_LOAD_NOTE = "Your first load is dispatched with no dispatch fee. After that, the percentage in your signed dispatch agreement applies."
GROSS_NOTE = "Weekly gross is the revenue a truck books before fuel, insurance, maintenance and other costs. It is not profit."
PRICING_NOTE = "Rough estimate only. Your percentage is confirmed in your signed dispatch agreement. First load dispatched free. No flat rate, no setup fee, no monthly subscription, no long-term contract."

# Planning ranges per mile by equipment, from our dispatch desk (October 2026).
# They are not a market index, available loads or quotes, and are labelled so wherever shown.
RATE_GUIDE_NOTE = ("Planning ranges our dispatchers use, October 2026. Not a market index, available loads or rate quotes; "
                   "real rates depend on lane, distance, season, freight type and local or OTR work.")
RATE_GUIDE = [
    ("Flatbed", "$5.00 - $7.00", "Open-deck OTR freight"),
    ("Step Deck", "$5.00 - $7.00", "Taller open-deck freight"),
    ("Reefer", "$4.00 - $6.00", "Temperature-controlled"),
    ("Hotshot", "$4.00 - $5.00", "Expedited and partial loads"),
    ("Dry Van", "$3.00 - $5.00", "Depends on local or OTR lanes"),
    ("Power Only", "$3.00 - $5.00", "Drop-and-hook trailers"),
    ("Box Truck", "$1.80 - $3.20", "Small-truck freight"),
]

# Example lanes for the rate board. These are illustrative examples of how
# loads are quoted, not live or current market rates, and are labelled so on
# every page. Each service page shows only its own equipment's examples.
LANES = [
    # Illustrative lanes across regions. Not available loads or current rate quotes.
    ("Los Angeles, CA", "Phoenix, AZ", "Dry Van", 372, "$3.40"),
    ("Chicago, IL", "Atlanta, GA", "Dry Van", 716, "$3.20"),
    ("Philadelphia, PA", "Atlanta, GA", "Dry Van", 781, "$3.10"),
    ("Ontario, CA", "Dallas, TX", "Reefer", 1388, "$4.10"),
    ("Jacksonville, FL", "Atlanta, GA", "Reefer", 346, "$4.50"),
    ("Columbus, OH", "Nashville, TN", "Reefer", 380, "$4.30"),
    ("Pittsburgh, PA", "Chicago, IL", "Flatbed", 461, "$5.40"),
    ("Ontario, CA", "Las Vegas, NV", "Flatbed", 230, "$5.90"),
    ("Dallas, TX", "Oklahoma City, OK", "Step Deck", 206, "$5.80"),
    ("Savannah, GA", "Nashville, TN", "Power Only", 492, "$3.30"),
    ("Chicago, IL", "Indianapolis, IN", "Power Only", 182, "$3.60"),
    ("Allentown, PA", "Columbus, OH", "Power Only", 421, "$3.20"),
    ("Cleveland, OH", "Pittsburgh, PA", "Hotshot", 134, "$4.60"),
    ("Houston, TX", "Baton Rouge, LA", "Hotshot", 271, "$4.70"),
    ("Fresno, CA", "Reno, NV", "Hotshot", 265, "$4.40"),
    ("Atlanta, GA", "Charlotte, NC", "Box Truck", 245, "$2.80"),
    ("Joliet, IL", "Columbus, OH", "Box Truck", 333, "$2.70"),
    ("Miami, FL", "Orlando, FL", "Box Truck", 235, "$2.40"),
    ("Dallas, TX", "Houston, TX", "Box Truck", 239, "$2.90"),
]
# Equipment shown in the rate board on each service page (others show every lane).
BOARD_EQUIPMENT = {
    "box-truck-dispatch.html": ["Box Truck"],
    "hotshot-dispatch.html": ["Hotshot"],
    "flatbed-dispatch.html": ["Flatbed", "Step Deck"],
    "dry-van-dispatch.html": ["Dry Van"],
    "reefer-dispatch.html": ["Reefer"],
    "power-only-dispatch.html": ["Power Only"],
}

EQUIPMENT = ["Dry Van", "Reefer", "Flatbed", "Step Deck", "Power Only", "Hotshot", "Box Truck", "Straight Truck"]

# Kept verbatim from the live site (SMS registration wording).
SMS_CONSENT = (
    'I agree to receive conversational and service-related SMS messages from Texas Solutions, a brand operated by '
    'LeadFlow Marketing Inc. at the phone number provided, including responses to my inquiry and dispatch-related '
    'communications. Message frequency varies. Message and data rates may apply. Reply STOP to opt out and HELP for '
    'help. SMS consent is optional and is not a condition of receiving dispatch services. See our '
    '<a href="privacy.html">Privacy Policy</a> and <a href="terms.html">Terms &amp; Conditions</a>.'
)
# Stored with every lead that ticks the box, so the exact wording agreed to is on record.
# Change SMS_CONSENT_VERSION whenever the wording above changes.
SMS_CONSENT_VERSION = "sms-consent-v1 (wording live since September 2026)"

# Short first-contact form (documents are collected after the first call).
MC_STATUS = ["Active MC authority", "New authority (under 6 months)", "Applying for authority", "No authority yet / leased on"]
CONTACT_METHODS = ["Phone call", "Text message", "WhatsApp", "Email"]
CALLBACK_TIMES = ["Any time", "Morning", "Afternoon", "Evening"]  # the carrier's preference, not our hours

FORM_DISCLAIMER = (
    "Submitting this form requests contact from Texas Solutions regarding Texas Solutions's own dispatch services. "
    "Texas Solutions does not sell or transfer mobile opt-in information or SMS consent to third parties for "
    "marketing or promotional purposes."
)
LEGAL_FOOTER = (
    "Texas Solutions provides dispatch services directly to its carrier clients. Texas Solutions is not a motor "
    "carrier or freight broker. Freight availability, rates, and earnings are not guaranteed."
)

# -------------------------------------------------------------- keywords
CORE_KEYWORDS = [
    "truck dispatch service", "truck dispatching company", "truck dispatcher", "truck dispatch services near me",
    "owner operator dispatch service", "dispatch service for owner operators", "independent truck dispatcher",
    "freight dispatch services", "best truck dispatch company", "OTR truck dispatch", "semi truck dispatch",
    "box truck dispatch", "hotshot dispatch", "flatbed dispatch", "dry van dispatch", "reefer dispatch",
    "power only dispatch", "step deck dispatch", "truck dispatch services USA", "dispatch service for small fleets",
    "how much does a truck dispatcher cost", "truck dispatch fee", "5% truck dispatch",
    "truck dispatch services", "trucking dispatch services", "truck dispatch company USA", "dispatch services for truckers",
    "hire a truck dispatcher", "truck dispatcher for hire", "24/7 truck dispatch service", "remote truck dispatcher",
    "dispatch for new authority", "semi truck dispatch services",
    "truck dispatching", "dispatch services for trucks", "trucking dispatch company", "truck dispatch company",
    "dispatcher for truckers", "truck dispatch service near me", "dispatcher for owner operators",
    "find a dispatcher for my truck", "need a dispatcher for my truck", "dispatch for new MC number",
    "dispatch services for small trucking companies", "box truck dispatch services", "hotshot dispatch services",
    "dry van dispatch services", "reefer dispatch services", "flatbed dispatch services", "power only dispatch services",
    "dispatcher for semi trucks", "affordable truck dispatch services", "dispatch service no contract",
    "truck dispatching services USA", "best truck dispatch service for owner operators 2026",
    "refrigerated load dispatch", "26 ft box truck loads", "new authority truck dispatch",
    "loads for new authority carriers", "dispatch fee percentage", "flat rate truck dispatch",
    "cheapest truck dispatch service", "no contract truck dispatch", "no forced dispatch",
]

# -------------------------------------------------------------- FAQs (site-wide)
FAQS = [
    ("How much does a truck dispatcher cost?",
     "At Texas Solutions, semi trucks pay 5% of weekly gross, hotshots 7%, and box trucks and straight trucks 8%, for OTR operations. There is no flat rate, no setup fee and no monthly subscription. On a typical semi grossing $8,000-$10,000 a week, that is about $400-$500 a week."),
    ("What does a truck dispatcher do?",
     "A truck dispatcher searches load boards and broker networks for freight that fits your truck, negotiates the rate, confirms the load with you, completes broker setup paperwork and keeps rate confirmations organized, so you can spend your time driving."),
    ("Do you dispatch local routes or only OTR?",
     "Our published rates apply to OTR (over-the-road) operations. Local and regional work is quoted separately, so call or message us with your lanes."),
    ("Is there a flat weekly fee?",
     "No. Texas Solutions charges a percentage of weekly gross only, so you pay when your truck earns and nothing in a week it sits. There is no flat rate, no setup fee and no monthly subscription, and your first load is dispatched free."),
    ("What equipment do you dispatch?",
     "Dry van, reefer, flatbed, step deck, power only, hotshot, box truck and straight truck, for owner-operators and small fleets across the USA."),
    ("Is Texas Solutions a freight broker?",
     "No. Texas Solutions is a truck dispatch service that works for the carrier. We are not a motor carrier or freight broker. Loads are booked under your own authority, and you approve every load before it is booked."),
    ("Will I be forced to accept loads?",
     "No. You decide which loads, lanes and rates work for your business. Nothing is booked without your approval."),
    ("Do you guarantee rates or earnings?",
     "No. Freight volume, rates, operating costs and market conditions vary. Texas Solutions does not guarantee any specific load volume, rate, revenue or earnings."),
    ("Is there a long-term contract?",
     "No long-term contract. A signed dispatch agreement is still required: it sets your percentage, what is included and the notice period for ending service."),
    ("What do I need to get started?",
     "Your MC and DOT numbers, equipment type and preferred lanes. After the first call we collect your W-9, certificate of insurance and, if you factor, a notice of assignment."),
    ("How fast can I start dispatching?",
     "Most carriers start soon after the first call: we review your authority and lanes, sign the agreement, collect documents, and begin searching loads for your truck."),
    ("Can I talk to a dispatcher on WhatsApp?",
     "Yes. Tap the WhatsApp button on any page or message +1 (838) 910-3147 on WhatsApp."),
    ("Are your dispatchers available 24/7?",
     "Yes. Our dispatchers work remotely across US time zones and are available 24/7 by phone, text or WhatsApp at (838) 910-3147, including nights and weekends when loads, breakdowns and reloads come up."),
    ("Is there a free trial?",
     "Yes. Your first load is dispatched with no dispatch fee so you can see how we work. After that, the percentage in your signed dispatch agreement applies: 5% of weekly gross for OTR semis, 7% for hotshots, 8% for box trucks and straight trucks. Local and regional work is quoted separately."),
    ("Do you work with new MC authority?",
     "Yes, from day one. We work with brand-new MC numbers, help with broker setup packets and look for brokers that accept new authorities. See dispatch for new authority for details."),
    ("Do you handle paperwork and invoicing?",
     "Yes. Besides load search and rate negotiation we handle broker carrier packets, rate confirmations, invoicing and billing, detention and lumper fee collection, factoring setup, IFTA filing, DOT compliance help and MC authority setup."),
    ("What is the best truck dispatch service for owner-operators in the USA?",
     "The best fit is the one that matches your truck and authority: a clear percentage with no hidden fees, no long-term contract, no forced loads, help with paperwork, and real people you can reach. Texas Solutions charges 5% for semis, 7% for hotshots and 8% for box trucks, works with new MC, is available 24/7 and dispatches your first load free."),
    ("Which dispatch service charges the lowest percentage?",
     "Percentages vary by equipment and by what is included. Compare the total value, not only the rate: does the fee include broker setups, invoicing and negotiation, and is there a setup fee or contract? Texas Solutions charges 5% of weekly gross for OTR semis, with no setup fee or contract."),
    ("Do you dispatch small fleets with 3 to 5 trucks?",
     "Yes. Each truck is dispatched to its own equipment, lanes and home time, at the same percentage per truck. Fleet owners get one point of contact for every truck."),
    ("Is a truck dispatch service worth it?",
     "For many owner-operators, yes, when it saves hours on load boards, cuts deadhead and wins better rates by more than the fee. It is less useful if you already have steady direct freight. Results vary, so compare your weekly gross and empty miles before and after."),
    ("Do you dispatch nationwide or only in Texas?",
     "Nationwide. Our office is in Midland, Texas, but our service covers the entire USA: remote dispatchers across US time zones book loads for carriers from California and Washington to Florida, New Jersey and Illinois."),
    ("Do you work with carriers in Alaska or Hawaii?",
     "We dispatch across the mainland USA. Carriers based in Alaska or Hawaii can contact us about their mainland operations, and we will tell you plainly whether we can help."),
    ("Do you offer a flat-rate dispatch plan?",
     "No. We only charge a percentage of weekly gross, so a week the truck does not run costs you nothing. A flat weekly fee is due whether or not you haul; a percentage keeps the dispatcher paid only when your truck earns."),
    ("Is a truck dispatcher the same as a freight broker?",
     "No. A broker works for the shipper and earns the margin between what the shipper pays and what the carrier is paid. A dispatcher works for the carrier, books loads under the carrier's own authority and is paid a fee by the carrier."),
    ("Dispatcher vs self-dispatch: which is better?",
     "Self-dispatch saves the fee but costs hours on load boards and broker calls every day. A dispatcher makes sense when those hours, better rates and fewer deadhead miles are worth more than the percentage. Many carriers self-dispatch first, then hire a dispatcher once the phone time starts competing with driving time."),
    ("What is the cheapest truck dispatch service?",
     "The lowest percentage is not always the cheapest once setup fees, weekly minimums, contracts or extra charges for paperwork are added. Texas Solutions charges 5% of weekly gross for OTR semis, 7% for hotshots and 8% for box trucks, with no setup fee, no flat weekly fee and no long-term contract, and your first load is dispatched free."),
    ("Do you work with lease operators?",
     "Yes. Carriers with their own MC authority get regular dispatch. If you do not have your own authority yet, our MC lease program lets you lease on to an established partner carrier's authority for 18-20% of gross, with dispatch included. See MC lease for details."),
]

STEPS = [
    ("Send your details", "Name, a phone number or email, and your equipment. Call, text or request a callback if you prefer."),
    ("Talk to a dispatcher", "We review your authority, equipment, lanes and home-time needs on a quick call."),
    ("Sign and onboard", "Sign the dispatch agreement (no long-term contract) and send your MC authority, W-9 and insurance certificate."),
    ("First load free", "We search and negotiate your first load with no dispatch fee, and book nothing without your approval."),
]

FEATURES = [
    ("Rate negotiation on every load", "We negotiate with brokers before a load reaches you, and walk away from freight that does not pay."),
    ("Lane and deadhead planning", "Loads planned around your preferred lanes, home time and next-load position."),
    ("Broker setups, invoicing and paperwork", "Carrier packets, rate confirmations, invoicing, detention and lumper collection, and factoring paperwork handled for you."),
    ("You approve every load", "No forced dispatch. Your truck, your authority, your decision."),
    ("First load free, no upfront cost", "Try us on your first load at no charge. After that, a percentage of weekly gross only: no setup fee, no subscription, no flat rate."),
    ("24/7 dispatchers, direct line", "A remote team across US time zones answers by phone, text or WhatsApp, day or night. Not a ticket queue."),
]

# -------------------------------------------------------------- landing pages
def fee_line(kind):
    p = PRICING[kind]
    return f"{p['pct'][0]}-{p['pct'][1]}% of weekly gross"


LANDING = [
    {
        "file": "box-truck-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', 'Box length, door type and liftgate details (many loads need a liftgate or pallet jack)', 'GVWR of the truck: over 26,000 lbs generally needs a CDL; check FMCSA and your state'], "nav": "Box Truck Dispatch", "kind": "small",
        "title": "Box Truck Dispatch Service | 8% OTR Dispatch Fee | Texas Solutions",
        "description": "Box truck dispatch for owner-operators and small fleets: load search, rate negotiation and broker paperwork for box trucks and straight trucks. 8% of weekly gross, OTR, no flat fee.",
        "keywords": "box truck dispatch service, box truck dispatch services, box truck dispatcher, box truck dispatch company, 26ft box truck dispatch, 26 ft box truck loads, box truck loads, box truck loads near me, box truck load board, how to find box truck loads, dispatcher for box truck with new authority, non CDL box truck loads, straight truck dispatch",
        "h1": "Box Truck Dispatch Service",
        "lede": "We find, negotiate and book freight for box trucks and straight trucks, while you drive.",
        "answer": "Texas Solutions provides box truck dispatch for owner-operators and small fleets across the USA. Dispatchers search and negotiate loads, complete broker setups and keep paperwork organized. The fee is 8% of weekly gross for OTR box trucks and straight trucks, with no flat rate, no setup fee and your approval on every load.",
        "body": [
            "Box truck freight moves in smaller, more frequent loads, which means more calls, more broker setups and more paperwork for every dollar your truck earns. Our dispatchers work the box truck side of the load boards every day.",
            "We match freight to your box length, liftgate and payload, plan around your home time, and negotiate before anything reaches you. As a hypothetical example, a box truck grossing $7,000 to $9,000 in a week would pay $560 to $720 in dispatch fees.",
            "Need a straight truck dispatch service? Straight trucks are dispatched the same way at the same 8%. Whether you run a 26 ft box truck, a smaller non-CDL box truck or a straight truck, your box truck dispatcher handles load search, broker setups, invoicing and rate confirmations, and is reachable 24/7.",
        ],
        "faqs": [
            ("How much is box truck dispatch?", "8% of weekly gross for OTR box trucks and straight trucks. On $7,000-$9,000 weekly gross that is about $560-$720 a week. No flat rate and no setup fee."),
            ("Do you dispatch non-CDL box trucks?", "Yes, as long as you run under your own MC authority. Tell us your truck size and weight rating and we search freight that fits."),
            ("Do you dispatch 26 ft box trucks?", "Yes. 26 ft box trucks are the most common truck on our box truck desk. We match loads to your box length, liftgate and payload, and plan around your home time."),
            ("Can you dispatch a box truck with new authority?", "Yes. We work with new MC numbers from day one and look for brokers that accept new authorities for box truck freight. Your first load is dispatched free."),
            ("Is there a dispatcher for box truck with new authority?", "Yes. A dispatcher for box truck with new authority needs brokers that accept new MC numbers, and that is where we start: your packet goes to those brokers first, and your first load is dispatched free."),
            ("Is there box truck dispatch near me?", "Box truck dispatch near me no longer means an office down the road. Our dispatchers are remote and work 24/7 across US time zones, so wherever your truck is, the dispatcher searches loads that pick up near you."),
            ("How do I find box truck loads near me?", "Box truck freight is posted on load boards and handed out directly by brokers and regional shippers. Your dispatcher searches around your current location and home base, calls the brokers who move box truck freight, and lines up the next load before the current one delivers."),
        ],
    },
    {
        "file": "hotshot-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', 'Pickup and gooseneck or bumper-pull flatbed trailer, with deck length and payload', 'Straps, chains, binders and edge protection for open-deck securement', 'Combined weight rating: combinations over 26,000 lbs generally need a CDL'], "nav": "Hotshot Dispatch", "kind": "small",
        "title": "Hotshot Dispatch Service | 7% Dispatch Fee, $4-5/Mile Loads | Texas Solutions",
        "description": "Hotshot dispatch for owner-operators: expedited and partial loads, rate negotiation and broker paperwork. Hotshot loads often pay $4-5 a mile. Dispatch fee 7% of weekly gross, OTR.",
        "keywords": "hotshot dispatch services, hotshot dispatcher, hotshot dispatch company, hotshot trucking dispatch, dispatcher for hotshot trucks, hotshot loads, hot shot loads near me, hotshot load board, non CDL hotshot loads, gooseneck dispatch",
        "h1": "Hotshot Dispatch Service",
        "lede": "Time-sensitive hotshot freight found, negotiated and confirmed with you before it is booked.",
        "answer": "Texas Solutions is a hotshot dispatch company for owner-operators across the USA. Dispatchers find expedited and partial loads, negotiate rates that often run $4-5 a mile, and handle broker paperwork. The dispatch fee is 7% of weekly gross for OTR hotshots, with no flat rate.",
        "body": [
            "Hotshot freight is fast and time-critical: equipment, machinery, construction and oilfield materials that cannot wait for a full truckload. Winning it means answering brokers fast and knowing which lanes pay.",
            "Hotshot loads come from every region: oilfield and energy work in Texas, New Mexico and North Dakota, construction and equipment moves around fast-growing metros, and agricultural parts across the Plains and Midwest. Rough rates on hotshot loads commonly run $4 to $5 a mile.",
            "Instead of refreshing a hotshot load board all day, your dispatcher watches the boards and calls brokers for you, then brings back only the loads that fit your trailer length, weight limits and lanes.",
            "Your hot shot dispatcher works 24/7, because expedited freight does not wait for business hours, and handles broker packets, rate confirmations and invoicing so you can keep driving.",
        ],
        "faqs": [
            ("How much do hotshot loads pay per mile?", "As a rough guide, hotshot loads often pay about $4-5 a mile, depending on lane, urgency and season. Rates are not guaranteed."),
            ("What is the dispatch fee for hotshots?", "7% of weekly gross for OTR hotshot operations, with no flat rate, no setup fee and no monthly subscription. On $7,000-$9,000 weekly gross that is about $490-$630 a week."),
            ("Do you dispatch non-CDL hotshots?", "Yes, if you run under your own MC authority. A non-CDL setup has a lower combined weight rating, so we look for lighter freight that fits your limits."),
            ("How do I find hot shot loads near me?", "Load boards list hotshot freight by pickup area, and brokers who move expedited freight post it there first. A dispatcher searches those boards and calls brokers near your location, so you hear about nearby loads without watching the screen yourself."),
            ("Can I get a hotshot dispatcher without a contract?", "Yes. There is no long-term contract, no setup fee and no forced dispatch, and your first load is dispatched free. You approve every load."),
        ],
    },
    {
        "file": "flatbed-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', 'Flatbed or step deck trailer with deck length and height', 'Tarps, straps, chains, binders and edge protectors', 'Experience with securement rules for the freight you want to haul'], "nav": "Flatbed & Step Deck Dispatch", "kind": "semi",
        "title": "Flatbed Dispatch Service | 5% Fee, $5-7/Mile Loads | Texas Solutions",
        "description": "Flatbed and step deck dispatch for owner-operators and small fleets. Open-deck loads often pay $5-7 a mile. Dispatch fee 5% of weekly gross for OTR semis. No flat rate.",
        "keywords": "flatbed dispatch service, flatbed dispatch services, flatbed dispatcher, step deck dispatch, step deck dispatch services, flatbed loads, open deck dispatch, flatbed loads per mile, flatbed truck dispatch company",
        "h1": "Flatbed & Step Deck Dispatch",
        "lede": "Open-deck freight searched, sized up and negotiated for your flatbed or step deck.",
        "answer": "Texas Solutions provides flatbed and step deck dispatch for owner-operators and small fleets across the USA. Dispatchers find open-deck loads that often pay $5-7 a mile, confirm dimensions, weight and tarping, and handle broker paperwork. The fee is 5% of weekly gross for OTR semis, with no flat rate.",
        "body": [
            "Our flatbed dispatch services start with the details. Open-deck freight comes with more questions than a sealed trailer: dimensions, weight, tarps, straps and chains, and whether a step deck is needed for height. We ask those questions before the load reaches you.",
            "Open-deck freight moves in every region: steel from the Midwest and South, lumber from the Southeast and Pacific Northwest, building materials around every growing metro, and machinery and energy equipment from Texas to the Dakotas.",
        ],
        "faqs": [
            ("How much do flatbed loads pay per mile?", "As a rough guide, flatbed and step deck loads often pay about $5-7 a mile, depending on lane, tarping and season. Rates are not guaranteed."),
            ("What is the dispatch fee for flatbeds?", "5% of weekly gross for OTR flatbed and step deck semis. On $8,000-$10,000 weekly gross that is about $400-$500 a week."),
            ("Do you offer step deck dispatch services?", "Yes. Step deck is dispatched alongside flatbed: we find taller open-deck loads that need the lower deck height and confirm dimensions, weight and securement before you commit."),
        ],
    },
    {
        "file": "dry-van-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', '53 ft (or 48 ft) dry van trailer in good condition', 'Load locks or straps for partial and mixed loads', 'Clean, dry trailer floor for food-grade and retail freight'], "nav": "Dry Van Dispatch", "kind": "semi",
        "title": "Dry Van Dispatch Service | 5% OTR Dispatch Fee | Texas Solutions",
        "description": "Dry van dispatch for owner-operators and small fleets: lane planning, rate negotiation and broker paperwork. Dry van loads run about $3-5 a mile depending on local or OTR. Fee 5% of weekly gross.",
        "keywords": "dry van dispatch, dry van dispatch service, dry van dispatcher, dry van loads per mile, 53 ft dry van dispatch, dry van trucking dispatch",
        "h1": "Dry Van Dispatch Service",
        "lede": "Lanes planned, deadhead cut and every load negotiated, with you approving each booking.",
        "answer": "Texas Solutions provides dry van dispatch for owner-operators and small fleets across the USA. Dispatchers plan lanes to reduce deadhead, negotiate every load and handle broker paperwork. Dry van loads run roughly $3-5 a mile depending on local or OTR lanes, and the dispatch fee is 5% of weekly gross for OTR semis.",
        "body": [
            "Dry van is the most common trailer on the road, which means the most freight and the most competition for it. Good dry van dispatch is about lanes: booking the next load before this one delivers and avoiding markets that leave you stuck.",
        ],
        "faqs": [
            ("How much do dry van loads pay per mile?", "Roughly $3-5 a mile. Short local loads can pay more per mile, long OTR runs less per mile but more per load. Rates are not guaranteed."),
            ("How do I find the best paying loads for a dry van?", "Plan lanes, not single loads: book the next load before this one delivers, avoid markets with little outbound freight unless the rate covers it, and negotiate every rate. Our dry van dispatch services do this for you 24/7."),
        ],
    },
    {
        "file": "reefer-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', 'Reefer trailer with a working unit and temperature download', 'Ability to pre-cool and run continuous or cycle mode as the shipper asks', 'Clean, odor-free trailer for food freight; reefer breakdown coverage is often required'], "nav": "Reefer Dispatch", "kind": "semi",
        "title": "Reefer Dispatch Service | Refrigerated Truck Dispatch | Texas Solutions",
        "description": "Reefer dispatch for owner-operators and small fleets: temperature-controlled loads, appointment coordination, rate negotiation and paperwork. 5% of weekly gross for OTR semis.",
        "keywords": "reefer dispatch, reefer dispatch service, refrigerated truck dispatch, refrigerated load dispatch, reefer loads, reefer dispatcher, reefer rates per mile, produce loads, peak season reefer loads",
        "h1": "Reefer Dispatch Service",
        "lede": "Temperature-controlled freight negotiated for your reefer, with appointments confirmed before you commit.",
        "answer": "Texas Solutions provides reefer dispatch for owner-operators and small fleets across the USA. Dispatchers find temperature-controlled loads, confirm temperature and appointment requirements with brokers and handle paperwork. The fee is 5% of weekly gross for OTR reefer semis, with no flat rate.",
        "body": ["Reefer freight pays for precision: set temperatures and tight appointments. We confirm both with the broker before a load reaches you.",
                 "Our reefer dispatch services cover refrigerated truck dispatch across the USA, with dispatchers available 24/7 for the early appointments and overnight reloads reefer freight brings.",
                 "Refrigerated load dispatch is also about timing. Produce seasons move from Florida and Texas in spring to California, the Northwest and the Midwest through summer and fall, and the holiday peak season fills grocery and food-service lanes in November and December. We plan reefer lanes around those markets so the reload is lined up before you deliver."],
        "faqs": [("Do you check temperature requirements before booking?", "Yes. We confirm temperature, appointment times and special handling before presenting the load."),
                 ("Do you dispatch reefer trucks running the Midwest?", "Yes. We dispatch reefers nationwide, including Midwest lanes, and plan reloads around produce and food distribution markets so you are not stuck empty. Your first load is dispatched free."),
                 ("What are reefer rates per mile today?", "Our dispatchers plan around roughly $4-6 a mile for reefer freight (October 2026 planning range, not a market index or quote). The real rate depends on the lane, distance, season and how much outbound freight the delivery market has. We negotiate every load before it reaches you.")],
    },
    {
        "file": "power-only-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', 'Tractor in good condition; the trailer is supplied by the shipper or broker', 'Trailer interchange insurance, which many power only programs require', 'Approval in the broker or carrier power only programs you want to run'], "nav": "Power Only Dispatch", "kind": "semi",
        "title": "Power Only Dispatch Services | Texas Solutions",
        "description": "Power only dispatch for tractors without trailers: preloaded and drop-and-hook freight, rate negotiation and paperwork. 5% of weekly gross for OTR.",
        "keywords": "power only dispatch, power only dispatch service, power only loads, power only trucking dispatch",
        "h1": "Power Only Dispatch Service",
        "lede": "Preloaded trailers and drop-and-hook freight found and negotiated for your tractor.",
        "answer": "Texas Solutions provides power only dispatch for owner-operators with a tractor and no trailer. Dispatchers find preloaded and drop-and-hook loads, negotiate the rate and handle broker paperwork. The fee is 5% of weekly gross for OTR operations.",
        "body": ["Power only lets a tractor earn without the cost of a trailer. The work is finding enough of those loads in the right places, which is what we do.",
                 "Our power only dispatch services cover preloaded trailers, drop-and-hook programs and trailer pools, with broker setups and rate confirmations handled for you."],
        "faqs": [("Do I need a trailer for power only?", "No. The trailer is supplied by the shipper, broker or a carrier program. You provide the tractor and authority.")],
    },
    {
        "file": "owner-operator-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', 'Equipment type and any special features (liftgate, tarps, reefer unit)', 'Preferred lanes, home time and the minimum rate you want to run for'], "nav": "Owner-Operator Dispatch", "kind": "semi",
        "title": "Owner-Operator Dispatch Service | 5% Semi, 7% Hotshot, 8% Box Truck | Texas Solutions",
        "description": "Dispatch service for owner-operators and small fleets: load search, rate negotiation and paperwork. 5% of weekly gross for semis, 7% for hotshots, 8% for box trucks, OTR. No flat rate or upfront fee.",
        "keywords": "owner operator dispatch service, dispatch services for owner operators, dispatcher for owner operators, find a dispatcher for my truck, need a dispatcher for my truck, hire a truck dispatcher, independent truck dispatcher, owner operator dispatcher cost",
        "h1": "Dispatch for Owner-Operators",
        "lede": "You run the truck. We handle the boards, the brokers and the paperwork, and you approve every load.",
        "answer": "Texas Solutions is a dispatch service for owner-operators and small fleets. It handles load search, rate negotiation, broker communication and paperwork for 5% of weekly gross on OTR semis, 7% on hotshots and 8% on box trucks, with no flat rate, no upfront fee, no long-term contract and no forced loads.",
        "body": [
            "Owner-operators lose hours every day to load boards and broker calls. A dispatcher takes that work on without taking control: you set the lanes, the home time and your minimum, and you approve every load.",
            "Small fleets get the same service per truck, with each truck's equipment and lanes handled separately.",
            "Whether you run one truck, a small trucking company or a fleet of semis, hotshots and box trucks, you get a dispatcher for owner-operators who answers 24/7, works with new MC authority and dispatches your first load free.",
        ],
        "sections": [
            ("Who we dispatch for", [
                "Owner-operators running one truck under their own MC authority.",
                "Small fleets and small trucking companies with 2 to 10 trucks, each dispatched to its own lanes.",
                "Fleet owners who want one point of contact for every truck.",
                "New trucking companies and carriers with new authority, from day one.",
                "Semi trucks (dry van, reefer, flatbed, step deck, power only), hotshots, box trucks and straight trucks.",
            ]),
            ("Dispatch plus back office", [
                "Broker carrier packets, rate confirmations and carrier setup with brokers.",
                "Invoicing and billing, detention and lumper fee collection.",
                "Factoring setup, IFTA filing, DOT compliance help and MC authority setup.",
            ]),
        ],
        "faqs": [("Is a dispatcher worth it for an owner-operator?", "For many, yes, when the dispatcher saves time, cuts deadhead and negotiates better loads by more than the fee. Results vary and no dispatcher can guarantee earnings."),
                 ("How do I find a dispatcher for my truck?", "Look for a dispatcher who works for the carrier, not a broker, publishes the fee, has no long-term contract and lets you approve every load. You can reach a Texas Solutions dispatcher 24/7 by phone, text or WhatsApp at (838) 910-3147."),
                 ("I need a dispatcher for my truck. How do I start?", "Call, text or WhatsApp us with your MC number, truck type and the lanes you want to run. We send a short agreement, collect your W-9 and insurance certificate, and start searching loads, usually the same day. Your first load is dispatched free."),
                 ("Do you offer dispatch for one truck?", "Yes. Most of the carriers we work with run one truck. The fee is the same percentage of weekly gross, and your first load is dispatched free."),
                 ("Can you compare dispatch for a small fleet of 3 to 5 trucks?", "Each truck pays the same percentage of its own weekly gross: 5% for semis, 7% for hotshots, 8% for box trucks. There is no fleet setup fee, and each truck gets lanes planned for its equipment and home time.")],
    },
    {
        "file": "dispatch-for-new-authority.html", "nav": "New Authority Dispatch", "kind": "semi",
        "title": "Dispatch for New Authority & New MC Numbers | Texas Solutions",
        "description": "Truck dispatch for new authority and new MC numbers from day one: broker setups, brokers that accept new MCs, first load free, no long-term contract.",
        "keywords": "dispatch for new authority, dispatch service for new authority, dispatch for new MC number, dispatch services for new MC number, dispatcher for new trucking company, dispatch for carriers with new authority, dispatcher who works with new MC, brokers that work with new authority, how to get loads with new authority, new authority truck dispatch, loads for new authority carriers, how to get loads with new MC number, broker setup packet help",
        "h1": "Dispatch for New Authority",
        "lede": "A dispatch service for new authority that works with a new MC from day one: broker setups, the brokers that accept new authorities, and your first load dispatched free.",
        "answer": "Texas Solutions dispatches carriers with brand-new MC authority from day one. Dispatchers send your carrier packets, find brokers that accept new MC numbers, negotiate every load and handle rate confirmations and invoicing, 24/7. Your first load is dispatched free; after that the fee is 5% of weekly gross for semis, 7% for hotshots and 8% for box trucks.",
        "body": [
            "The first months with a new MC number are the hardest. Many brokers want a few months of authority history, insurance on file and a clean safety record before they book you, and every broker has its own setup packet. That is where most new trucking companies lose time and money.",
            "Our dispatchers work with new authority every day. We know which brokers accept new MCs, keep your packet ready to send, and build a lane history for your truck so more brokers open up as your authority ages.",
        ],
        "sections": [
            ("How we get loads for a new MC", [
                "Prepare one complete carrier packet: MC authority, W-9, certificate of insurance, and notice of assignment if you factor.",
                "Target brokers that work with new authority and set you up with them before you need a load.",
                "Start on lanes where new carriers get booked, then build repeat freight with brokers who see you deliver.",
                "Negotiate every rate: a new MC does not have to mean the lowest rate on the board.",
            ]),
            ("I have one truck and a 2-month-old MC. How do I get loads?", [
                "Get your packet and insurance certificate ready to send in minutes.",
                "Work load boards and call brokers that accept new authorities, not only the ones that post the most freight.",
                "Deliver on time and keep paperwork clean; brokers rebook carriers who make their job easy.",
                "Or let a dispatcher do the searching and setups while you drive. We dispatch your first load free.",
            ]),
        ],
        "includes": [
            "Carrier setup with brokers that accept new MC numbers",
            "Load search, rate negotiation and lane planning",
            "MC number and trucking authority setup help if you have not filed yet",
            "Invoicing, factoring setup and rate confirmations",
            "24/7 dispatchers by phone, text or WhatsApp",
            "First load dispatched free, no long-term contract, no setup fee",
        ],
        "faqs": [
            ("Do you dispatch new authority?", "Yes, from day one. We work with brand-new MC numbers and set you up with brokers that accept new authorities."),
            ("Which dispatch companies work with new MC authorities?", "Texas Solutions works with new MC authorities from day one, for dry van, reefer, flatbed, step deck, power only, hotshot, box truck and straight truck. The first load is dispatched free and there is no long-term contract."),
            ("Can you dispatch a box truck with new authority?", "Yes. Box trucks with new authority are a large part of our desk. We look for box truck freight from brokers that accept new MC numbers. The fee is 8% of weekly gross after your free first load."),
            ("How do I get loads with a new MC number?", "Have a complete broker setup packet ready, get set up with brokers that accept new authority before you need a load, start on lanes where new carriers get booked, and deliver on time so those brokers rebook you. New authority truck dispatch does this searching and setup work for you while you drive. Read our guide on loads for new authority carriers for the full steps."),
            ("Do you help with broker setup packets?", "Yes. Broker setup packet help is part of dispatch: we prepare your MC authority, W-9, certificate of insurance and notice of assignment once, then complete each broker's carrier packet so you can be booked quickly."),
            ("Why do some brokers not work with new authority?", "Many brokers set a minimum authority age or insurance history to manage risk. Others accept new carriers if the packet is complete and insurance is verified. Knowing which is which saves days of calls."),
        ],
    },
    {
        "file": "mc-lease.html", "nav": "MC Lease (Lease-On)", "kind": "lease",
        "requirements": ['A truck you own or lease-purchase, in good mechanical condition', 'A valid CDL where your truck requires one, and a driving record the partner carrier can insure', 'Truck title or lease, registration and a recent annual inspection', 'Equipment type, trailer details and the lanes you want to run', 'Willingness to follow the partner carrier\'s safety, ELD and paperwork rules'],
        "title": "MC Lease for Owner-Operators | Lease On, 18-20% | Texas Solutions",
        "description": "MC lease for owner-operators without authority: lease on to a partner carrier's MC with dispatch included. 18-20% of gross.",
        "keywords": "MC lease, lease on to a carrier, lease on trucking, lease your truck on to a carrier, owner operator lease on, lease onto authority, run under someone else's authority, MC lease percentage, lease on with dispatch, new owner operator without authority",
        "h1": "MC Lease for Owner-Operators",
        "lede": "No authority yet, or tired of waiting for a new MC to age? Lease on to an established partner carrier and start hauling, with dispatch included.",
        "answer": "Texas Solutions arranges MC leases for owner-operators: you lease your truck on to an established partner carrier and haul under that carrier's active authority and insurance filings, with Texas Solutions dispatchers finding and negotiating your loads. The fee is 18-20% of gross, depending on your equipment and what is included, and is set in a written lease agreement. Texas Solutions itself is a dispatch service, not a motor carrier.",
        "body": [
            "Getting your own MC takes time, and many brokers will not book a new authority for its first months. An MC lease skips that wait: the partner carrier's authority is already active and already set up with brokers, so you can start hauling sooner.",
            "You bring the truck and drive it; the partner carrier provides the operating authority; our dispatchers search, negotiate and book loads for you. One percentage covers the lease and the dispatch, so there is no separate dispatch fee.",
            "When you are ready for your own authority, we help you file it and move you to regular dispatch on your own MC.",
        ],
        "includes": [
            "Haul under an established partner carrier's active MC and USDOT authority",
            "The partner carrier's insurance filings, as set out in the lease agreement",
            "Dispatch included: load search, rate negotiation and lane planning",
            "Brokers already set up with the carrier, so no new-MC waiting period",
            "A written lease agreement that states the percentage and what is included",
            "Help moving to your own authority later, if you want it",
        ],
        "pricing_note": "MC lease is 18-20% of gross, depending on your equipment and what the lease includes. The exact percentage, what is deducted and how settlements are paid are written in your lease agreement before you haul. Earnings are not guaranteed.",
        "faqs": [
            ("What is an MC lease?", "An MC lease, or lease-on, means an owner-operator leases their truck to a motor carrier and hauls under that carrier's operating authority instead of their own MC number."),
            ("How much does an MC lease cost?", "18-20% of gross, depending on your equipment and what the lease includes. Dispatch is included in that percentage. The exact terms are in your written lease agreement."),
            ("Whose authority will I run under?", "An established partner carrier with active authority. Texas Solutions is a dispatch service, not a motor carrier; the partner carrier is named in your lease agreement."),
            ("Can I switch to my own authority later?", "Yes. We help you file for your own MC and USDOT numbers and then dispatch you on your own authority at the regular dispatch percentage."),
            ("Is dispatch included in the MC lease?", "Yes. Our dispatchers find, negotiate and book your loads, and you still approve every load."),
        ],
    },
    {
        "file": "trucking-back-office-services.html", "nav": "Back-Office Services", "kind": "semi",
        "pricing_note": "Factoring setup is $132 one-time, IFTA filing $83 per quarter, Form 2290 $50, bookkeeping setup $165, and collections are free for dispatch clients (11% of the amount recovered for others). Government fees, insurance premiums and taxes are paid directly by you.",
        "title": "Trucking Back-Office Services: Invoicing, IFTA & Setup",
        "description": "Trucking back-office services with dispatch: broker packets, invoicing, detention and lumper collection, factoring setup, IFTA filing, DOT help, MC setup.",
        "keywords": "trucking back office services, trucking paperwork services, rate negotiation for truckers, broker carrier packet setup, factoring for trucking companies, IFTA filing services, trucking compliance services, MC authority setup, trucking invoicing service, trucking billing services, factoring and dispatch services, IFTA filing service, trucking compliance services, DOT compliance help, MC authority setup service, detention and lumper fee collection, trucking accounting and dispatch, ELD and dispatch support, carrier setup with brokers",
        "h1": "Trucking Back-Office Services",
        "lede": "The paperwork behind every load, handled: broker setups, invoicing, detention and lumper collection, factoring, IFTA, DOT compliance and MC authority setup.",
        "answer": "Texas Solutions handles trucking back-office work alongside dispatch: broker carrier packets and carrier setup with brokers, rate confirmations, invoicing and billing, detention and lumper fee collection, factoring setup, IFTA filing, DOT compliance help and MC authority setup. Dispatchers are available 24/7, and the first load is dispatched free.",
        "body": [
            "These are trucking paperwork services and trucking compliance services in one place: rate negotiation for truckers, IFTA filing services, and factoring for trucking companies set up and coordinated by the same team. Hauling the load is half the job. The other half is the carrier packet before it, and the invoice, the detention claim and the fuel tax report after it. Missed paperwork means late pay and money left on the table.",
            "Our team handles that paperwork as part of dispatch, so the same people who booked the load make sure it gets billed and paid. Ask us what is included for your truck when you get your estimate.",
        ],
        "sections": [
            ("Broker setup and load paperwork", [
                "Broker carrier packet setup: MC authority, W-9, certificate of insurance, notice of assignment.",
                "Carrier setup with new brokers before you need the load.",
                "Rate confirmations checked against what was negotiated.",
            ]),
            ("Billing and getting paid", [
                "Invoicing and billing brokers with the rate confirmation, bill of lading and receipts.",
                "Detention and lumper fee collection, with times and receipts documented.",
                "Factoring setup and coordination with your factoring company, if you factor.",
            ]),
            ("Back-office prices", [
                "Factoring setup: $132 one-time.",
                "IFTA filing: $83 per quarter. Form 2290: $50.",
                "Collections: free for dispatch clients; 11% of the amount recovered for others.",
                "Bookkeeping setup: $165 one-time. Compliance and permits package: $165 one-time.",
                "Government fees, insurance premiums and taxes are paid directly by you.",
            ]),
            ("Compliance and authority", [
                "IFTA filing support: mileage and fuel records by state each quarter.",
                "DOT compliance help: keeping filings, insurance and records current.",
                "MC authority setup for new trucking companies.",
                "ELD and dispatch support: planning loads around your available hours.",
            ]),
        ],
        "includes": [
            "Broker carrier packets and carrier setup with brokers",
            "Rate confirmations, invoicing and billing",
            "Detention and lumper fee collection",
            "Factoring setup and coordination",
            "IFTA filing, DOT compliance help and MC authority setup",
            "Dispatchers available 24/7",
        ],
        "faqs": [
            ("Which dispatchers also handle paperwork and invoicing?", "Texas Solutions does. Along with load search and rate negotiation we handle broker packets, rate confirmations, invoicing, detention and lumper collection, factoring setup, IFTA filing, DOT compliance help and MC authority setup."),
            ("Do you offer factoring and dispatch together?", "We are not a factoring company, but we set up and coordinate factoring for you: notice of assignment in your broker packets and invoices sent to your factor."),
            ("Can you file my IFTA?", "Yes. We help prepare and file your quarterly IFTA return from your mileage and fuel records. Rates change each quarter, so we work from the current IFTA tax rate matrix."),
            ("Do you help with detention and lumper fees?", "Yes. We document check-in and check-out times and lumper receipts and bill them with the load. Detention pay depends on the terms in your rate confirmation; try the detention pay calculator to estimate it."),
        ],
    },
    {
        "file": "semi-truck-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', 'Tractor and trailer details: type, length, and any special equipment', 'Equipment you carry for the freight: load locks, straps, tarps or a reefer unit'], "nav": "Semi Truck Dispatch", "kind": "semi",
        "title": "Semi Truck Dispatch Services | Dispatcher for Semi Trucks",
        "description": "Semi truck dispatch across the USA for dry van, reefer, flatbed, step deck and power only. 5% of weekly gross, OTR, no flat rate, first load free, 24/7.",
        "keywords": "semi truck dispatch services, dispatcher for semi trucks, truck dispatch services USA, freight dispatch services, trucking dispatch company, dispatch services for trucks, dispatcher for truckers",
        "h1": "Semi Truck Dispatch Services",
        "lede": "One dispatcher for your tractor, whatever trailer is behind it: dry van, reefer, flatbed, step deck or power only.",
        "answer": "Texas Solutions provides semi truck dispatch services across the USA for owner-operators and small fleets running dry van, reefer, flatbed, step deck and power only. Dispatchers search loads, negotiate every rate, handle broker setups and plan lanes around your home time, for 5% of weekly gross on OTR semis with no flat rate.",
        "body": [
            "Our semi truck dispatch starts with the lane. Whatever you call it, truck dispatch is one job: keep your truck loaded on lanes you choose. A semi earns when it is loaded and moving in the right direction. Our dispatchers plan each week so the next load picks up close to where the last one delivers, which keeps deadhead down and your truck on the lanes you prefer.",
            "We match freight to your trailer and your limits before it reaches you: weight and dimensions for open deck, temperature and appointment times for reefer, drop-and-hook programs for power only, and live or drop for dry van.",
            "Most semis on our desk gross between $8,000 and $10,000 a week, though every lane and season is different and nothing is guaranteed. The fee is the same 5% of weekly gross whichever trailer you pull.",
        ],
        "sections": [
            ("Trailers we dispatch", [
                "Dry van: general freight, retail and consumer goods, live and drop loads.",
                "Reefer: produce, meat, dairy and frozen goods with temperature and appointment checks.",
                "Flatbed and step deck: steel, lumber, machinery and building materials with securement details confirmed.",
                "Power only: preloaded trailers and drop-and-hook programs for tractors without a trailer.",
            ]),
        ],
        "faqs": [
            ("How much does semi truck dispatch cost?", "5% of weekly gross for OTR semi trucks, whatever the trailer type. On $8,000-$10,000 weekly gross that is about $400-$500 a week. No flat rate, no setup fee and no long-term contract."),
            ("Can one dispatcher handle different trailer types?", "Yes. If you switch between a dry van and a reefer, or run power only between your own loads, the same dispatcher plans around whichever trailer you have that week."),
            ("Do you dispatch team trucks?", "Yes. Team semis can run longer lanes, so we plan loads around both drivers' hours and the miles a team can cover. The fee stays 5% of weekly gross."),
        ],
    },
    {
        "file": "small-fleet-dispatch.html", "requirements": ['Active MC authority and USDOT number in your own name', 'Certificate of insurance that brokers will accept (auto liability and cargo)', 'W-9, and a notice of assignment if you use factoring', 'A list of trucks with equipment type and the driver for each', 'Preferred lanes and home time per driver'], "nav": "Small Fleet Dispatch", "kind": "semi",
        "title": "Dispatch Services for Small Fleets & Trucking Companies",
        "description": "Dispatch for small trucking companies with 2-10 trucks: one contact, each truck on its own lanes, 5% semi, 7% hotshot, 8% box truck. No fleet setup fee.",
        "keywords": "dispatch service for small fleets, dispatch services for small trucking companies, trucking dispatch company, truck dispatch company, fleet dispatch service, best truck dispatch company",
        "h1": "Dispatch for Small Fleets and Small Trucking Companies",
        "lede": "Every truck planned on its own lanes and home time, with one point of contact for the owner.",
        "answer": "Texas Solutions dispatches small fleets and small trucking companies with roughly 2 to 10 trucks. Each truck is planned on its own equipment, lanes and driver home time, and the owner gets one point of contact and a weekly summary. The fee is per truck: 5% of weekly gross for semis, 7% for hotshots and 8% for box trucks, with no fleet setup fee.",
        "body": [
            "Our dispatch services for small trucking companies are built around the owner. As a dispatch service for small fleets, we plan every truck separately. Running a few trucks is a different job from running one. The owner ends up dispatching at night, answering drivers and chasing invoices instead of growing the business. A dispatch team takes the daily load search and broker calls off your desk while you stay in control of rates and lanes.",
            "Mixed fleets are normal for us. A company can run a dry van, a reefer and two box trucks, and each truck still gets freight that fits its equipment and its driver's schedule.",
            "When you add a truck, we add it to the plan. There is no extra setup fee and no long-term contract, and the first load on a new truck is planned with you before it is booked.",
        ],
        "sections": [
            ("What fleet owners get", [
                "A dispatcher who knows every truck, driver and preferred lane in your fleet.",
                "Loads planned to reduce empty miles between trucks and lanes.",
                "Driver check calls, appointment updates and rate confirmations handled for you.",
                "Invoicing, detention and lumper collection, and factoring paperwork for every load.",
                "A weekly gross and load summary for each truck.",
            ]),
        ],
        "faqs": [
            ("How is dispatch priced for a fleet?", "Per truck, as a percentage of that truck's weekly gross: 5% for semis, 7% for hotshots and 8% for box trucks and straight trucks. A truck that does not run that week pays nothing."),
            ("Do my drivers talk to the dispatcher directly?", "Yes, if you want them to. Many fleet owners have drivers call the dispatcher for load details and updates, while the owner approves rates and lanes."),
            ("What makes a good dispatch company for a small fleet?", "Clear percentage pricing with no setup fee, no long-term contract, people you can reach day and night, and paperwork handled along with the loads. Ask any dispatch company how they plan multiple trucks so they do not compete for the same freight."),
        ],
    },
    {
        "file": "trucking-authority-setup.html", "nav": "MC Number & Authority Setup", "kind": "semi",
        "title": "MC Number & Trucking Authority Setup | Texas Solutions",
        "description": "Get your MC number and trucking authority set up the right way: USDOT and MC filing help, BOC-3 and insurance coordination, then dispatch from day one.",
        "keywords": "mc number, motor carrier number, trucking authority, mc authority, motor carrier operating authority, dot and mc number, how to get mc number, trucking authority packages, carrier authority, how to get your own authority in trucking",
        "h1": "MC Number and Trucking Authority Setup",
        "lede": "From USDOT number to active MC authority, with a dispatcher ready to book your first load the day you can haul.",
        "answer": "An MC number is the motor carrier number FMCSA issues with for-hire operating authority, which lets you haul regulated freight for other companies across state lines. Texas Solutions helps new carriers through each step: USDOT and MC applications, the BOC-3 process agent filing, insurance filings, UCR and broker packets. Government and insurance costs are paid by the carrier, and we start dispatching as soon as your authority is active.",
        "body": [
            "Getting your own authority in trucking is a sequence of filings, and each one waits on the last. A missed insurance filing or a BOC-3 that never reaches FMCSA can leave a new carrier waiting weeks with a truck that cannot haul.",
            "We walk you through the order that saves the most time, check each filing before it goes in, and keep track of where your application stands. When the authority goes active, your broker packet is already prepared and your dispatcher is searching loads from brokers that accept new MC numbers.",
            "Think of it as a trucking authority package without the mystery: you see every government fee and every provider you pay, and you keep full control of your own USDOT and MC numbers.",
        ],
        "sections": [
            ("What is an MC number?", [
                "MC stands for motor carrier. The MC number is issued with your motor carrier operating authority.",
                "It shows brokers and shippers that you are allowed to haul regulated freight for hire across state lines.",
                "A USDOT number identifies your company for safety records; most for-hire interstate carriers need both a DOT and MC number.",
            ]),
            ("How to get your DOT and MC number, step by step", [
                "Form your business and get an EIN, so the authority is in the right legal name.",
                "Apply to FMCSA for a USDOT number and for-hire operating authority (the MC number) through the FMCSA registration system.",
                "File a BOC-3 so a process agent is on record in every state.",
                "Have your insurance company file proof of liability coverage with FMCSA.",
                "Register for UCR and set up IRP plates and IFTA in your base state if you run interstate.",
                "Wait out the protest period; when FMCSA shows your authority as active, you can haul.",
            ]),
            ("Where we help", [
                "A checklist for your truck type and the order to file in.",
                "Checking applications and filings before they are submitted.",
                "Coordinating with your insurance agent and BOC-3 provider so filings reach FMCSA.",
                "Broker packet ready the day your authority goes active.",
                "Dispatch for new authority from day one, with your first load free.",
            ]),
        ],
        "includes": [
            "Step-by-step USDOT and MC authority guidance",
            "BOC-3 and insurance filing coordination",
            "UCR, IRP and IFTA setup checklist",
            "Broker carrier packet prepared in advance",
            "Dispatch from day one of active authority",
            "First load dispatched free",
        ],
        "pricing_note": "MC authority setup is $275, one-time, for our help with the USDOT, MC, BOC-3 and UCR filings. Government fees, insurance and BOC-3 costs are paid directly by you, and FMCSA lists the current filing fees on its website. Once your authority is active, dispatch is 5% of weekly gross for semis, 7% for hotshots and 8% for box trucks.",
        "faqs": [
            ("What is a motor carrier number?", "A motor carrier number, or MC number, is the identifier FMCSA issues with your for-hire operating authority. Brokers check it before they book a carrier."),
            ("How long does it take to get trucking authority?", "Many carriers see their authority go active a few weeks after applying, once insurance and BOC-3 filings are on record and the protest period has passed. Timelines vary, so check your status on FMCSA."),
            ("What is in a trucking authority package?", "Usually guidance through the USDOT and MC applications, the BOC-3 filing, insurance filing coordination and registration checklists. Ask any provider which government fees are included and which you pay directly; with us, you pay all government and insurance costs yourself and keep full control of your numbers."),
            ("Can I get dispatched as soon as my MC is active?", "Yes. We work with brand-new authority from day one, send your packet to brokers that accept new MC numbers, and dispatch your first load free."),
        ],
    },
    {
        "file": "texas-truck-dispatch.html", "nav": "Texas Truck Dispatch", "kind": "semi", "hide_nav": True,
        "title": "Truck Dispatch Services Texas | Houston, Dallas, Midland",
        "description": "Truck dispatch services in Texas for owner-operators and small fleets: Houston hotshot, Dallas, San Antonio, Laredo and Permian Basin lanes, plus nationwide OTR.",
        "keywords": "truck dispatch services Texas, truck dispatch service Texas, hotshot dispatch Houston, truck dispatcher Dallas, Houston truck dispatch, San Antonio truck dispatch, Laredo truck dispatch, Midland TX truck dispatch, Permian Basin dispatch",
        "h1": "Truck Dispatch Services in Texas",
        "lede": "Dispatch for carriers based in or running through Texas, from the same nationwide team that books loads across the USA.",
        "answer": "Texas Solutions is a nationwide truck dispatch company with its head office at 401 W Kentucky Ave, Midland, Texas. For Texas carriers it dispatches lanes out of Houston, Dallas-Fort Worth, San Antonio, Laredo, El Paso and the Permian Basin, and anywhere those loads lead, for 5% of weekly gross on semis, 7% on hotshots and 8% on box trucks.",
        "body": [
            "Texas is one of the largest freight markets in the country, with energy, manufacturing, cross-border and port freight moving through it every day.",
            "Our head office is in Midland, and our remote dispatchers book Texas freight for flatbed, hotshot, dry van, reefer, power only and box trucks every day, alongside carriers in every other state.",
            "Carriers ask us most often for hotshot dispatch Houston lanes and for a truck dispatcher Dallas carriers can reach at night. Houston is one of the busiest hotshot markets in the country, with energy, petrochemical and construction equipment moving to job sites across the Gulf Coast. Dallas-Fort Worth is a national distribution hub for dry van and reefer freight, and Laredo is the largest truck crossing on the Mexico border.",
        ],
        "faqs": [("Where is Texas Solutions located?", "401 W Kentucky Ave, Midland, Texas. We dispatch carriers throughout the United States."),
                 ("Do you offer truck dispatch services in Houston and Dallas?", "Yes. We dispatch carriers based in Houston, Dallas-Fort Worth and across Texas, including hotshot dispatch in Texas and the Permian Basin, 24/7, with your first load dispatched free."),
                 ("Do you offer hotshot dispatch in Houston?", "Yes. Hotshot dispatch out of Houston is a large part of our Texas desk: energy, petrochemical and construction freight heading to the Gulf Coast, the Permian Basin and out of state. The fee is 7% of weekly gross, OTR."),
                 ("Is there a truck dispatcher in Dallas?", "Our dispatchers are remote, so Dallas-Fort Worth carriers reach one 24/7 by phone, text or WhatsApp. DFW dry van, reefer and box truck freight is booked the same way as every other lane we run."),
                 ("Is there a truck dispatcher near me in Texas?", "Our office is in Midland, and our dispatchers work remotely around the clock, so carriers anywhere in Texas reach a dispatcher by phone, text or WhatsApp at (838) 910-3147.")],
    },
    {
        "file": "what-does-a-truck-dispatcher-do.html", "nav": "What a Truck Dispatcher Does", "kind": "semi", "guide": True,
        "title": "What Does a Truck Dispatcher Do? Duties & Cost (2026 Guide) | Texas Solutions",
        "description": "What a truck dispatcher does, how much truck dispatch costs (5% for semis, 7% for hotshots, 8% for box trucks at Texas Solutions), dispatcher vs broker, and how to choose a dispatch service.",
        "keywords": "what does a truck dispatcher do, how much does a truck dispatcher cost, truck dispatcher fees, truck dispatcher percentage, dispatcher vs broker, how to choose a truck dispatch service",
        "h1": "What Does a Truck Dispatcher Do?",
        "lede": "The job, the usual fees, the difference from a broker, and what to check before you sign.",
        "answer": "A truck dispatcher finds and books freight for a carrier's trucks: searching load boards and brokers, negotiating rates, confirming loads with the driver, completing broker setup paperwork and organizing rate confirmations. Independent dispatchers usually charge a percentage of weekly gross; Texas Solutions charges 5% for OTR semis, 7% for hotshots and 8% for box trucks.",
        "body": [
            "Most owner-operators start by dispatching themselves. It works until the hours on the phone start competing with the hours behind the wheel.",
        ],
        "sections": [
            ("What is truck dispatching and how does it work?", [
                "Truck dispatching is finding, negotiating and booking freight for a carrier's trucks, then managing the paperwork until the load is paid.",
                "The carrier tells the dispatcher its equipment, lanes, home time and minimum rate.",
                "The dispatcher searches load boards and broker networks, negotiates, and presents loads; the carrier approves each one.",
                "The dispatcher sends the carrier packet, confirms the rate confirmation, and follows up on delivery, invoicing and payment.",
            ]),
            ("How do dispatchers find loads?", [
                "Load boards, where brokers post spot freight.",
                "Direct relationships with brokers who call back trusted carriers first.",
                "Planning the next load from where this one delivers, to cut deadhead miles.",
                "Repeat lanes and dedicated freight once a carrier proves reliable on a lane.",
            ]),
            ("The daily duties of a truck dispatcher", [
                "Search load boards and broker networks for freight that fits the truck and lanes.",
                "Negotiate rates with brokers before presenting a load.",
                "Plan the next load to reduce deadhead miles.",
                "Complete broker setup packets with the carrier's MC authority, W-9 and insurance.",
                "Keep rate confirmations and dispatch details organized.",
            ]),
            ("How much does a truck dispatcher cost?", [
                "Most independent dispatchers charge a percentage of the truck's weekly gross rather than a salary; commonly quoted ranges run from about 3% to 10% depending on equipment and services.",
                "Texas Solutions: 5% of weekly gross for OTR semi trucks, 7% for hotshots, 8% for box trucks and straight trucks.",
                "On a semi grossing $8,000-$10,000 a week, 5% is about $400-$500 a week.",
                "No flat rate, no setup fee and no monthly subscription.",
            ]),
            ("Truck dispatcher vs freight broker", [
                "A dispatcher works for the carrier and books freight under the carrier's authority.",
                "A freight broker works between shipper and carrier and holds its own broker authority.",
                "Texas Solutions is a dispatch service, not a motor carrier or freight broker.",
            ]),
            ("How to choose a truck dispatch service", [
                "You approve every load and are never forced to take freight.",
                "The fee is a clear percentage, with no hidden setup or monthly charges.",
                "No long-term contract and a clear notice period.",
                "Your application is never sold to lead buyers.",
                "Nobody guarantees rates or earnings; markets move.",
            ]),
        ],
        "faqs": [
            ("What is truck dispatch services?", "Truck dispatch services are a back-office service for carriers: a dispatcher finds and negotiates loads, handles broker setup and paperwork, and supports the driver on the road, for a fee paid by the carrier. Texas Solutions charges 5% of weekly gross for semis, 7% for hotshots and 8% for box trucks."),("Can a dispatcher guarantee my weekly gross?", "No. Rates and freight volume change with the market, and a reputable dispatcher will not guarantee earnings.")],
    },
]

# -------------------------------------------------------------- fuel calculator
# Fuel model, calibrated to published data (sources shown on the page):
#   gallons per mile = (1 / empty_mpg) * (1 + k * cargo_lbs / 1000)
# - Semis: k = 0.0055 from NACFE lightweighting (0.5-0.6% fuel per 1,000 lbs);
#   empty ~7.6 mpg gives ~6.3 mpg at 38,000 lbs, matching FHWA's 6.3 mpg
#   national combination-truck average and ATRI's 6-8 mpg range.
# - Hotshot: ~13.5 mpg empty, ~9.7 mpg at 9,000 lbs, ~8 mpg at 16,000 lbs
#   (operator-reported figures for 1-ton duallies pulling 40 ft goosenecks).
# - 26 ft box truck: ~11 mpg empty, ~9.6 at 5,000 lbs, ~8.5 fully loaded
#   (Penske / Ryder reported averages of 8-10 mpg).
# Calibration speed is 62 mph; above that, about 0.1 mpg is lost per mph
# for semis (DOE / industry rule of thumb), scaled by truck size below.
FUEL_TRUCKS = [
    # id, name, empty_mpg, k (fuel increase per 1,000 lbs), max cargo lbs, default cargo lbs, idle gal/hr, mpg lost per mph over 62
    ("dry-van", "Dry Van", 7.6, 0.0055, 45000, 38000, 0.8, 0.10),
    ("reefer", "Reefer", 7.3, 0.0055, 44000, 38000, 0.8, 0.10),
    ("flatbed", "Flatbed", 7.5, 0.0060, 48000, 40000, 0.8, 0.10),
    ("step-deck", "Step Deck", 7.4, 0.0060, 46000, 38000, 0.8, 0.10),
    ("power-only", "Power Only", 7.6, 0.0055, 45000, 38000, 0.8, 0.10),
    ("hotshot", "Hotshot", 13.5, 0.043, 16500, 12000, 0.4, 0.15),
    ("box-truck", "Box Truck", 11.0, 0.0294, 10000, 7000, 0.5, 0.12),
    ("straight-truck", "Straight Truck", 9.5, 0.0266, 12000, 8000, 0.6, 0.12),
]
FUEL_SOURCES = [
    ("FHWA Highway Statistics, Table VM-1 (via DOE Alternative Fuels Data Center): Class 8 trucks average about 6.3 mpg", "https://afdc.energy.gov/data/10310"),
    ("NACFE lightweighting research: 0.5-0.6% fuel savings per 1,000 lbs of weight", "https://nacfe.org/research/technology/chassis/lightweighting/"),
    ("ATRI Operational Costs of Trucking: long-haul tractors average about 7-8 mpg", "https://truckingresearch.org/about-atri/atri-research/operational-costs-of-trucking/"),
    ("U.S. Energy Information Administration: weekly retail on-highway diesel prices", "https://www.eia.gov/petroleum/gasdiesel/"),
]
REEFER_GAL_PER_HOUR = 0.8

# State -> EIA diesel region (PADD). EIA publishes California on its own.
STATE_REGION = {
    "AL": ("Alabama", "P3"), "AK": ("Alaska", "P5X"), "AZ": ("Arizona", "P5X"), "AR": ("Arkansas", "P3"),
    "CA": ("California", "CA"), "CO": ("Colorado", "P4"), "CT": ("Connecticut", "P1A"), "DE": ("Delaware", "P1B"),
    "DC": ("District of Columbia", "P1B"), "FL": ("Florida", "P1C"), "GA": ("Georgia", "P1C"), "HI": ("Hawaii", "P5X"),
    "ID": ("Idaho", "P4"), "IL": ("Illinois", "P2"), "IN": ("Indiana", "P2"), "IA": ("Iowa", "P2"),
    "KS": ("Kansas", "P2"), "KY": ("Kentucky", "P2"), "LA": ("Louisiana", "P3"), "ME": ("Maine", "P1A"),
    "MD": ("Maryland", "P1B"), "MA": ("Massachusetts", "P1A"), "MI": ("Michigan", "P2"), "MN": ("Minnesota", "P2"),
    "MS": ("Mississippi", "P3"), "MO": ("Missouri", "P2"), "MT": ("Montana", "P4"), "NE": ("Nebraska", "P2"),
    "NV": ("Nevada", "P5X"), "NH": ("New Hampshire", "P1A"), "NJ": ("New Jersey", "P1B"), "NM": ("New Mexico", "P3"),
    "NY": ("New York", "P1B"), "NC": ("North Carolina", "P1C"), "ND": ("North Dakota", "P2"), "OH": ("Ohio", "P2"),
    "OK": ("Oklahoma", "P2"), "OR": ("Oregon", "P5X"), "PA": ("Pennsylvania", "P1B"), "RI": ("Rhode Island", "P1A"),
    "SC": ("South Carolina", "P1C"), "SD": ("South Dakota", "P2"), "TN": ("Tennessee", "P2"), "TX": ("Texas", "P3"),
    "UT": ("Utah", "P4"), "VT": ("Vermont", "P1A"), "VA": ("Virginia", "P1C"), "WA": ("Washington", "P5X"),
    "WV": ("West Virginia", "P1C"), "WI": ("Wisconsin", "P2"), "WY": ("Wyoming", "P4"),
}

# SERP-length titles/descriptions per path, applied by page() (title <= ~60, description <= ~155 characters).
SEO = {
    '/': (
        'Truck Dispatch Services USA, 24/7 | Texas Solutions',
        'Nationwide truck dispatch for owner-operators and small fleets, 24/7: semi 5%, hotshot 7%, box truck 8% of weekly gross. First load free, new MC welcome.'),
    '/estimate.html': (
        'Truck Dispatch Fee Calculator & Free Quote | Texas Solutions',
        'Calculate your truck dispatch fee: semi 5%, hotshot 7%, box truck 8% of weekly gross, OTR. Pick your truck, set your own percentage, get a free quote.'),
    '/truck-dispatch-rates.html': (
        'Truck Dispatch Service Cost & Rates | Texas Solutions',
        'What truck dispatchers charge: 5% semi, 7% hotshot, 8% box truck of weekly gross. No flat rate, no long-term contract, no upfront fee, first load free.'),
    '/truck-fuel-cost-calculator.html': (
        'Truck Fuel Price Calculator & Diesel Prices Today',
        'Free truck fuel price calculator with diesel prices for all 50 states, updated daily. Estimate MPG, trip fuel cost and cost per mile for any truck type.'),
    '/tools.html': (
        'Free Trucking Calculators for Owner-Operators | Texas Solutions',
        'Free trucking calculators: dispatch fee, fuel cost, fuel surcharge, detention, cost per mile, load profit, break-even, deadhead, IFTA, HOS and more.'),
    '/fuel-surcharge-calculator.html': (
        'Fuel Surcharge Calculator for Trucking | Texas Solutions',
        "Free trucking fuel surcharge calculator: surcharge per mile and per trip from base price, current diesel price and MPG, or your contract's step table."),
    '/detention-pay-calculator.html': (
        'Truck Detention Pay Calculator | Texas Solutions',
        'Free detention pay calculator for truckers: arrival, release, free time, hourly rate and billing increment give eligible detention hours and estimated pay.'),
    '/break-even-calculator.html': (
        'Truck Break-Even Calculator (Miles & Rate) | Texas Solutions',
        'Free truck break-even calculator: enter fixed costs, cost per mile and rate to see the miles per month you need to break even and your profit at planned miles.'),
    '/cost-per-mile-calculator.html': (
        'Trucking Cost Per Mile Calculator (CPM) | Texas Solutions',
        'Free owner-operator cost per mile calculator: fixed and variable costs, your own pay shown separately, and cost per total mile and per loaded mile.'),
    '/deadhead-miles-calculator.html': (
        'Deadhead Miles Calculator (Effective Rate) | Texas Solutions',
        "Free deadhead miles calculator: see your deadhead percentage and effective rate per mile once empty miles are counted against a load's revenue."),
    '/driver-pay-calculator.html': (
        'Truck Driver Pay Calculator (Per Mile, Load, %) | Texas Solutions',
        'Free truck driver pay calculator: weekly, monthly and annual pay for per-mile, per-load, percentage of gross or hourly pay models.'),
    '/freight-class-calculator.html': (
        'Freight Class Calculator (NMFC Density) | Texas Solutions',
        'Free freight class calculator: estimate NMFC class from length, width, height and weight using the density table. Estimate only; confirm with your carrier.'),
    '/hours-of-service-calculator.html': (
        'Hours of Service Calculator: 11, 14 & 70-Hour Rules',
        'Free HOS calculator: estimate remaining drive time under the FMCSA 11-hour, 14-hour and 60/70-hour limits. Planning tool only, not a legal record.'),
    '/ifta-mileage-calculator.html': (
        'IFTA Mileage Calculator: Miles & Fuel by State | Texas Solutions',
        'Free IFTA mileage calculator: log miles and fuel by state, see gallons used and net taxable gallons for your own IFTA records.'),
    '/load-profitability-calculator.html': (
        'Is This Load Worth Taking? Load Profit Calculator',
        'Free load profitability calculator: dispatch and factoring fees, deadhead and return miles, CPM and expenses give estimated profit and the rate you need.'),
    '/truck-loan-calculator.html': (
        'Truck Loan Calculator: Monthly Payment | Texas Solutions',
        'Free truck loan calculator: enter the truck price, down payment, interest rate and term to see your monthly payment, total interest and total cost.'),
    '/box-truck-dispatch.html': (
        'Box Truck Dispatch Services & Box Truck Dispatcher',
        'Box truck dispatch for owner-operators: load search, rate negotiation and broker paperwork for box and straight trucks. 8% of weekly gross, OTR, no flat fee.'),
    '/hotshot-dispatch.html': (
        'Hotshot Dispatch Services & 24/7 Hot Shot Dispatcher',
        'Hotshot dispatch for owner-operators: expedited and partial loads, rate negotiation and paperwork. Loads often pay $4-5 a mile. 7% of weekly gross, OTR.'),
    '/flatbed-dispatch.html': (
        'Flatbed & Step Deck Dispatch Services | Texas Solutions',
        'Flatbed and step deck dispatch for owner-operators. Open-deck loads often pay $5-7 a mile. 5% of weekly gross for OTR semis, no flat rate.'),
    '/dry-van-dispatch.html': (
        'Dry Van Dispatch Services: 5% of Weekly Gross | Texas Solutions',
        'Dry van dispatch for owner-operators and small fleets: lane planning, rate negotiation and paperwork. Loads run about $3-5 a mile. 5% of weekly gross, OTR.'),
    '/reefer-dispatch.html': (
        'Reefer Dispatch Services, Refrigerated Truck Dispatch',
        'Reefer dispatch for owner-operators and small fleets: temperature-controlled loads, appointments, rate negotiation and paperwork. 5% of weekly gross, OTR.'),
    '/owner-operator-dispatch.html': (
        'Owner Operator Dispatch Service | Dispatcher for Owner Operators',
        'Dispatch for owner-operators and small fleets: load search, rate negotiation and paperwork. 5% semi, 7% hotshot, 8% box truck of weekly gross, OTR.'),
    '/texas-truck-dispatch.html': (
        'Truck Dispatch Services Texas | Houston, Dallas, Midland',
        'Truck dispatch services in Texas: Houston hotshot dispatch, Dallas-Fort Worth, San Antonio, Laredo and Permian Basin lanes, plus nationwide OTR.'),
    '/trucking-authority-setup.html': (
        'MC Number & Trucking Authority Setup | Texas Solutions',
        'What an MC number is and how to get your DOT and MC number: USDOT, MC authority, BOC-3 and insurance filing help, then dispatch from day one.'),
    '/semi-truck-dispatch.html': (
        'Semi Truck Dispatch Services | Dispatcher for Semi Trucks',
        'Semi truck dispatch across the USA: dry van, reefer, flatbed, step deck, power only. 5% of weekly gross, OTR, first load free.'),
    '/small-fleet-dispatch.html': (
        'Dispatch Services for Small Fleets & Trucking Companies',
        'Dispatch for small trucking companies with 2-10 trucks: one contact, each truck on its own lanes, 5% semi, 7% hotshot, 8% box truck. No fleet setup fee.'),
    '/what-does-a-truck-dispatcher-do.html': (
        'What Does a Truck Dispatcher Do? Duties & Cost | Texas Solutions',
        'What a truck dispatcher does, how much dispatch costs (5% semi, 7% hotshot, 8% box truck at Texas Solutions), dispatcher vs broker, and how to choose one.'),
    '/about.html': (
        'About Texas Solutions | Nationwide Truck Dispatch Company',
        'Texas Solutions: truck dispatch for owner-operators and small fleets across the USA. Office in Midland, Texas. Not a broker.'),
    '/contact.html': (
        'Contact a Truck Dispatcher | Call or WhatsApp | Texas Solutions',
        'Talk to a Texas Solutions truck dispatcher: call or WhatsApp (838) 910-3147, email dispatch@texassolutions.co, or send your details. Midland, TX.'),
    '/faq.html': (
        'Truck Dispatch FAQ: Cost, OTR & How It Works | Texas Solutions',
        'Answers about truck dispatch: what a dispatcher costs (5% semi, 7% hotshot, 8% box truck), OTR vs local, contracts, paperwork and getting started.'),
}

# -------------------------------------------------------------- business services (beyond dispatch)
# Shown on trucking-business-services.html. (name, description, link or None, price, price note).
# Prices are our own; government filing fees, insurance premiums and taxes are paid by the carrier.
BUSINESS_SERVICES = [
    ("Getting started", [
        ("MC authority setup", "USDOT, MC, BOC-3 and UCR filings in the right order, checked before they go in.", "trucking-authority-setup.html", "$275", "one-time"),
        ("MC lease (lease-on)", "No authority yet? Haul under an established partner carrier's MC, dispatch included.", "mc-lease.html", "18-20%", "of gross"),
        ("Compliance and permits", "IRP plates, IFTA account, state permits, drug-testing enrollment and a driver qualification file set up for you.", None, "$165", "one-time"),
        ("Factoring setup", "Compare factoring offers, set up the notice of assignment and get paid faster.", "trucking-back-office-services.html", "$132", "one-time"),
        ("Partner referrals", "Introductions to insurance agents, ELD providers, fuel cards and drug-testing consortiums.", None, "Free", ""),
    ]),
    ("Staying compliant", [
        ("IFTA and Form 2290 filing", "Quarterly fuel tax returns from your mileage and fuel records, and the annual heavy vehicle use tax.", "trucking-back-office-services.html", "$83", "per IFTA quarter, 2290 $50"),
        ("Safety audit preparation", "A mock new-entrant audit so your files, logs and maintenance records are ready before FMCSA asks.", None, "$219", "one-time"),
        ("ELD and logbooks", "ELD setup and regular log reviews to catch hours-of-service problems early.", None, "$110", "one-time"),
        ("DOT drug and alcohol testing", "Consortium enrollment, pre-employment testing and Clearinghouse queries through our partners.", None, "Free referral", "full setup in compliance package"),
    ]),
    ("Growing your business", [
        ("Accounting and bookkeeping", "Per-load income and expense tracking so you know what each truck and lane really earns.", None, "$165", "one-time setup"),
        ("Collections", "Follow-up on late invoices, detention, layover and TONU charges until they are paid.", "trucking-back-office-services.html", "Free", "for dispatch clients, 11% of recovered for others"),
        ("Driver hiring", "Screened CDL drivers with a driver qualification file, for solo and team trucks.", None, "$550", "solo driver, $825 team"),
        ("Carrier websites", "A clean website that makes your company look established to brokers, shippers and drivers.", None, "From $219", "+ $39/mo, free for dispatch clients"),
        ("Trucking SEO", "Search visibility so shippers and drivers find your company on Google.", None, "Custom quote", "after a free audit"),
        ("Trucking social media", "Regular posts that build trust with shippers and help you recruit drivers.", None, "Custom quote", ""),
    ]),
]

# -------------------------------------------------------------- dispatch agreement (sign-contract.html)
# One source for the on-page agreement and the signed PDF (js/contract.js reads it as JSON).
# Bump "version" whenever the wording changes; it is printed on every signed copy.
CONTRACT = {
    "version": "TSD-DSA-2026-10",
    "title": "Truck Dispatch Services Agreement",
    "dispatcher": {"name": "Texas Solutions Dispatch", "address": "401 W Kentucky Ave, Midland, Texas 79701",
                   "email": "dispatch@texassolutions.co", "phone": "(838) 910-3147"},
    "notify_email": "dispatch@texassolutions.co",
    "sections": [
        ("Purpose", [
            "The Carrier authorizes the Dispatcher to locate freight opportunities, negotiate rates, communicate with brokers and shippers, and provide dispatch-related administrative services.",
            "The Dispatcher acts solely as an independent dispatcher and is not a freight broker, motor carrier or freight forwarder.",
        ]),
        ("Services provided", ["The Dispatcher agrees to:", [
            "Search and negotiate loads.",
            "Communicate with freight brokers.",
            "Submit carrier packets.",
            "Schedule pickups and deliveries.",
            "Handle check calls and appointment updates.",
            "Provide rate confirmations.",
            "Assist with detention, TONU and layover requests.",
            "Assist with documentation when needed.",
        ]]),
        ("Carrier responsibilities", ["The Carrier agrees to:", [
            "Maintain active MC and USDOT authority.",
            "Carry all legally required insurance.",
            "Ensure vehicles comply with FMCSA regulations.",
            "Notify the Dispatcher immediately of delays, accidents, breakdowns or delivery issues.",
            "Deliver loads safely and on time.",
            "Provide signed PODs immediately after delivery.",
        ]]),
        ("Dispatch fee", [
            "The Carrier agrees to pay the Dispatcher {fee}% of the gross revenue for each completed load.",
            "Payment is due within 24 hours after the Carrier receives payment from the broker, unless otherwise agreed.",
        ]),
        ("Payment method", ["The Carrier may pay by ACH, Zelle, wire transfer, Cash App, check or another method agreed in writing. Selected method: {payment}."]),
        ("Non-circumvention", [
            "The Carrier agrees not to directly solicit or conduct business with any customer, broker or shipper introduced by the Dispatcher during this Agreement and for 12 months following termination.",
            "Violation may result in liquidated damages of $5,000 per occurrence plus legal costs.",
        ]),
        ("Governing law", [
            "This Agreement shall be governed by the laws of the State of Texas, United States.",
            "Any disputes shall be resolved in the appropriate courts located in Texas.",
        ]),
        ("Entire agreement", [
            "This Agreement constitutes the entire agreement between the parties and supersedes all prior discussions or agreements.",
            "Any amendments must be in writing and signed by both parties.",
        ]),
    ],
    "documents": ["Active MC authority", "Certificate of insurance (COI)", "W-9", "Notice of assignment (if applicable)",
                  "Copy of CDL (owner-operator, if applicable)", "Voided check or ACH information (if required)",
                  "Signed Dispatch Services Agreement"],
    "payment_methods": ["ACH", "Zelle", "Wire transfer", "Cash App", "Check", "Other"],
    # Optional uploads on the contract page, emailed with the signed PDF (Web3Forms Pro attachments,
    # one field per file, 5 MB max each; photos are resized in the browser first).
    # (field, label, required)
    "uploads": [("doc_mc_authority", "MC authority letter", True), ("doc_coi", "Certificate of insurance (COI)", True), ("doc_w9", "W-9", True),
                ("doc_noa", "Notice of assignment (if you factor)", False), ("doc_cdl", "CDL (owner-operator)", False),
                ("doc_void_check", "Voided check or ACH form", False)],
    "attorney_note": ("This template provides a solid commercial foundation, but for ongoing business operations, it is advisable to have "
                      "a U.S. attorney review it to ensure it complies with the laws of the state where your dispatch business operates "
                      "and to tailor clauses such as payment terms, non-circumvention and dispute resolution to your specific needs."),
    "dispatcher_signature": "Texas Solutions",
    "esign": ("By signing below, I agree that my electronic signature is the legal equivalent of my handwritten signature, "
              "that I am authorized to sign for the Carrier named above, and that I have read and agree to this Agreement."),
}
