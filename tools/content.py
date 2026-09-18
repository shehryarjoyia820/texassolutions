"""
All words and numbers for dispatch.texassolutions.co.
Edit here, then run:  python tools/site.py

Pricing (rough estimate, OTR only, no flat rate):
  Small trucks (box truck, straight truck, hotshot): 8-10% of weekly gross,
      typical weekly gross $7,000-$9,000
  Semi trucks (dry van, reefer, flatbed, step deck, power only): 5-6% of
      weekly gross, typical weekly gross $8,000-$10,000
"""

BASE = "https://dispatch.texassolutions.co"
MAIN_SITE = "https://texassolutions.co"
NAME = "Texas Solutions"
BRAND = "Texas Solutions Truck Dispatch"
PHONE = "(838) 910-3147"
PHONE_E164 = "+18389103147"
WHATSAPP = "18389103147"
WHATSAPP_TEXT = "Hi Texas Solutions, I'd like to know more about your truck dispatch service."
EMAIL = "info@texassolutions.co"
STREET = "401 W Kentucky Ave"
CITY = "Midland"
REGION = "TX"
POSTAL = "79701"
COUNTRY = "US"
HOURS = "Call, text or WhatsApp a dispatcher"

# Web3Forms delivers form submissions by email (existing account).
WEB3FORMS_KEY = "c66393e0-d742-483a-b9d0-a923d09baa97"

# -------------------------------------------------------------- pricing
PRICING = {
    "small": {
        "label": "Small trucks",
        "equipment": ["Box Truck", "Straight Truck", "Hotshot"],
        "pct": (8, 10),
        "gross": (7000, 9000),
    },
    "semi": {
        "label": "Semi trucks",
        "equipment": ["Dry Van", "Reefer", "Flatbed", "Step Deck", "Power Only"],
        "pct": (5, 6),
        "gross": (8000, 10000),
    },
}
PRICING_CONDITION = "Rates apply to OTR (over-the-road) operations. Local and regional work is quoted separately."
PRICING_NOTE = "Rough estimate only. Your final percentage is confirmed in your signed dispatch agreement. No flat rate, no setup fee, no monthly subscription."

# Rough rate-per-mile guide by equipment (for the rate board and estimate page).
RATE_GUIDE = [
    ("Flatbed", "$5.00 - $6.00", "Open-deck OTR freight"),
    ("Hotshot", "$5.00 - $6.00", "Expedited and partial loads"),
    ("Dry Van", "$2.00 - $5.00", "Depends on local or OTR lanes"),
    ("Step Deck", "$2.50 - $3.20", "Taller open-deck freight"),
    ("Reefer", "$2.40 - $3.00", "Temperature-controlled"),
    ("Power Only", "$2.00 - $2.60", "Drop-and-hook trailers"),
    ("Box Truck", "$1.80 - $2.60", "Small-truck freight"),
]

# Sample lanes for the animated rate board (illustrative, not live).
LANES = [
    ("Midland, TX", "Phoenix, AZ", "Flatbed", 872, "$5.40"),
    ("Odessa, TX", "Oklahoma City, OK", "Hotshot", 412, "$5.85"),
    ("Laredo, TX", "Atlanta, GA", "Dry Van", 1142, "$2.65"),
    ("Dallas, TX", "Denver, CO", "Flatbed", 793, "$5.70"),
    ("Houston, TX", "Memphis, TN", "Dry Van", 587, "$3.10"),
    ("Amarillo, TX", "Salt Lake City, UT", "Hotshot", 906, "$5.20"),
    ("El Paso, TX", "Los Angeles, CA", "Power Only", 801, "$2.30"),
    ("San Antonio, TX", "Nashville, TN", "Step Deck", 1024, "$2.85"),
    ("Fort Worth, TX", "Kansas City, MO", "Reefer", 520, "$2.75"),
    ("Houston, TX", "San Antonio, TX", "Dry Van", 197, "$4.60"),
]

EQUIPMENT = ["Dry Van", "Reefer", "Flatbed", "Step Deck", "Power Only", "Hotshot", "Box Truck", "Straight Truck"]

# Kept verbatim from the live site (SMS registration wording).
SMS_CONSENT = (
    'I agree to receive conversational and service-related SMS messages from Texas Solutions, a brand operated by '
    'LeadFlow Marketing Inc. at the phone number provided, including responses to my inquiry and dispatch-related '
    'communications. Message frequency varies. Message and data rates may apply. Reply STOP to opt out and HELP for '
    'help. SMS consent is optional and is not a condition of receiving dispatch services. See our '
    '<a href="privacy.html">Privacy Policy</a> and <a href="terms.html">Terms &amp; Conditions</a>.'
)
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
    "power only dispatch", "step deck dispatch", "truck dispatch Texas", "dispatch service for small fleets",
    "how much does a truck dispatcher cost", "truck dispatch fee", "5% truck dispatch",
]

# -------------------------------------------------------------- FAQs (site-wide)
FAQS = [
    ("How much does a truck dispatcher cost?",
     "At Texas Solutions, semi trucks pay 5-6% of weekly gross and small trucks (box trucks, straight trucks and hotshots) pay 8-10% of weekly gross, for OTR operations. There is no flat rate, no setup fee and no monthly subscription. On a typical semi grossing $8,000-$10,000 a week, that is about $400-$600 a week."),
    ("What does a truck dispatcher do?",
     "A truck dispatcher searches load boards and broker networks for freight that fits your truck, negotiates the rate, confirms the load with you, completes broker setup paperwork and keeps rate confirmations organized, so you can spend your time driving."),
    ("Do you dispatch local routes or only OTR?",
     "Our published rates apply to OTR (over-the-road) operations. Local and regional work is quoted separately, so call or message us with your lanes."),
    ("Is there a flat weekly fee?",
     "No. Texas Solutions charges a percentage of weekly gross only. There is no flat rate, no setup fee and no monthly subscription."),
    ("What equipment do you dispatch?",
     "Dry van, reefer, flatbed, step deck, power only, hotshot, box truck and straight truck, for owner-operators and small fleets across the United States."),
    ("Is Texas Solutions a freight broker?",
     "No. Texas Solutions is a truck dispatch service that works for the carrier. We are not a motor carrier or freight broker. Loads are booked under your own authority, and you approve every load before it is booked."),
    ("Will I be forced to accept loads?",
     "No. You decide which loads, lanes and rates work for your business. Nothing is booked without your approval."),
    ("Do you guarantee rates or earnings?",
     "No. Freight volume, rates, operating costs and market conditions vary. Texas Solutions does not guarantee any specific load volume, rate, revenue or earnings."),
    ("Is there a long-term contract?",
     "No. The dispatch agreement sets the service terms and your percentage, and the notice period for ending service is stated in that agreement."),
    ("What do I need to get started?",
     "Your MC and DOT numbers, equipment type and preferred lanes. After the first call we collect your W-9, certificate of insurance and, if you factor, a notice of assignment."),
    ("How fast can I start dispatching?",
     "Most carriers start soon after the first call: we review your authority and lanes, sign the agreement, collect documents, and begin searching loads for your truck."),
    ("Can I talk to a dispatcher on WhatsApp?",
     "Yes. Tap the WhatsApp button on any page or message +1 (838) 910-3147 on WhatsApp."),
]

STEPS = [
    ("Get an estimate", "Use the calculator to see your dispatch fee on your weekly gross, or message us on WhatsApp."),
    ("Talk to a dispatcher", "We review your authority, equipment, lanes and home-time needs on a quick call."),
    ("Sign and onboard", "Sign the dispatch agreement and send your MC authority, W-9 and insurance certificate."),
    ("Start rolling", "We search and negotiate loads for your truck and book nothing without your approval."),
]

FEATURES = [
    ("Rate negotiation on every load", "We negotiate with brokers before a load reaches you, and walk away from freight that does not pay."),
    ("Lane and deadhead planning", "Loads planned around your preferred lanes, home time and next-load position."),
    ("Broker setups and paperwork", "Carrier packets, W-9, insurance certificates and rate confirmations handled for you."),
    ("You approve every load", "No forced dispatch. Your truck, your authority, your decision."),
    ("No upfront cost", "No setup fee, no monthly subscription, no flat rate. Percentage of weekly gross only."),
    ("Real dispatchers, direct line", "Talk to your dispatcher by phone or WhatsApp, not a ticket queue."),
]

# -------------------------------------------------------------- landing pages
def fee_line(kind):
    p = PRICING[kind]
    return f"{p['pct'][0]}-{p['pct'][1]}% of weekly gross"


LANDING = [
    {
        "file": "box-truck-dispatch.html", "nav": "Box Truck Dispatch", "kind": "small",
        "title": "Box Truck Dispatch Service | 8-10% OTR Dispatch | Texas Solutions",
        "description": "Box truck dispatch for owner-operators and small fleets: load search, rate negotiation and broker paperwork for box trucks and straight trucks. 8-10% of weekly gross, OTR, no flat fee.",
        "keywords": "box truck dispatch, box truck dispatch service, box truck dispatcher, straight truck dispatch, 26 ft box truck loads, box truck dispatch company, non CDL box truck dispatch",
        "h1": "Box Truck Dispatch Service",
        "lede": "We find, negotiate and book freight for box trucks and straight trucks, while you drive.",
        "answer": "Texas Solutions provides box truck dispatch for owner-operators and small fleets across the United States. Dispatchers search and negotiate loads, complete broker setups and keep paperwork organized. The fee is 8-10% of weekly gross for OTR box trucks and straight trucks, with no flat rate, no setup fee and your approval on every load.",
        "body": [
            "Box truck freight moves in smaller, more frequent loads, which means more calls, more broker setups and more paperwork for every dollar your truck earns. Our dispatchers work the box truck side of the load boards every day.",
            "We match freight to your box length, liftgate and payload, plan around your home time, and negotiate before anything reaches you. Typical OTR box trucks on our desk gross $7,000 to $9,000 a week.",
        ],
        "faqs": [
            ("How much is box truck dispatch?", "8-10% of weekly gross for OTR box trucks and straight trucks. On $7,000-$9,000 weekly gross that is about $560-$900 a week. No flat rate and no setup fee."),
            ("Do you dispatch non-CDL box trucks?", "Yes, as long as you run under your own MC authority. Tell us your truck size and weight rating and we search freight that fits."),
        ],
    },
    {
        "file": "hotshot-dispatch.html", "nav": "Hotshot Dispatch", "kind": "small",
        "title": "Hotshot Dispatch Service | $5-6/Mile Loads, 8-10% | Texas Solutions",
        "description": "Hotshot dispatch for owner-operators: expedited and partial loads, rate negotiation and broker paperwork. Hotshot loads often pay $5-6 a mile. Dispatch fee 8-10% of weekly gross, OTR.",
        "keywords": "hotshot dispatch, hotshot dispatch service, hotshot dispatcher, hotshot trucking dispatch, hotshot loads, gooseneck dispatch, hotshot dispatch Texas, Permian Basin hotshot",
        "h1": "Hotshot Dispatch Service",
        "lede": "Time-sensitive hotshot freight found, negotiated and confirmed with you before it is booked.",
        "answer": "Texas Solutions dispatches hotshot trucks for owner-operators across the United States, including Texas and the Permian Basin. Dispatchers find expedited and partial loads, negotiate rates that often run $5-6 a mile, and handle broker paperwork. The dispatch fee is 8-10% of weekly gross for OTR hotshots, with no flat rate.",
        "body": [
            "Hotshot freight is fast and time-critical: equipment, machinery, construction and oilfield materials that cannot wait for a full truckload. Winning it means answering brokers fast and knowing which lanes pay.",
            "From our base in Midland, Texas, we see a lot of hotshot freight move through the Permian Basin and across Texas. Rough rates on hotshot loads commonly run $5 to $6 a mile.",
        ],
        "faqs": [
            ("How much do hotshot loads pay per mile?", "As a rough guide, hotshot loads often pay about $5-6 a mile, depending on lane, urgency and season. Rates are not guaranteed."),
            ("What is the dispatch fee for hotshots?", "8-10% of weekly gross for OTR hotshot operations, with no flat rate, no setup fee and no monthly subscription."),
        ],
    },
    {
        "file": "flatbed-dispatch.html", "nav": "Flatbed & Step Deck Dispatch", "kind": "semi",
        "title": "Flatbed Dispatch Service | $5-6/Mile, 5-6% Fee | Texas Solutions",
        "description": "Flatbed and step deck dispatch for owner-operators and small fleets. Open-deck loads often pay $5-6 a mile. Dispatch fee 5-6% of weekly gross for OTR semis. No flat rate.",
        "keywords": "flatbed dispatch, flatbed dispatch service, flatbed dispatcher, step deck dispatch, open deck dispatch, flatbed loads per mile, flatbed truck dispatch company",
        "h1": "Flatbed & Step Deck Dispatch",
        "lede": "Open-deck freight searched, sized up and negotiated for your flatbed or step deck.",
        "answer": "Texas Solutions provides flatbed and step deck dispatch for owner-operators and small fleets nationwide. Dispatchers find open-deck loads that often pay $5-6 a mile, confirm dimensions, weight and tarping, and handle broker paperwork. The fee is 5-6% of weekly gross for OTR semis, with no flat rate.",
        "body": [
            "Open-deck freight comes with more questions than a sealed trailer: dimensions, weight, tarps, straps and chains, and whether a step deck is needed for height. We ask those questions before the load reaches you.",
            "Texas and the Permian Basin move a large share of the country's open-deck freight, including steel, building materials, machinery and oilfield equipment.",
        ],
        "faqs": [
            ("How much do flatbed loads pay per mile?", "As a rough guide, flatbed loads often pay about $5-6 a mile, depending on lane, tarping and season. Rates are not guaranteed."),
            ("What is the dispatch fee for flatbeds?", "5-6% of weekly gross for OTR flatbed and step deck semis. On $8,000-$10,000 weekly gross that is about $400-$600 a week."),
        ],
    },
    {
        "file": "dry-van-dispatch.html", "nav": "Dry Van Dispatch", "kind": "semi",
        "title": "Dry Van Dispatch Service | 5-6% OTR Fee | Texas Solutions",
        "description": "Dry van dispatch for owner-operators and small fleets: lane planning, rate negotiation and broker paperwork. Dry van loads run about $2-5 a mile depending on local or OTR. Fee 5-6% of weekly gross.",
        "keywords": "dry van dispatch, dry van dispatch service, dry van dispatcher, dry van loads per mile, 53 ft dry van dispatch, dry van trucking dispatch",
        "h1": "Dry Van Dispatch Service",
        "lede": "Lanes planned, deadhead cut and every load negotiated, with you approving each booking.",
        "answer": "Texas Solutions provides dry van dispatch for owner-operators and small fleets nationwide. Dispatchers plan lanes to reduce deadhead, negotiate every load and handle broker paperwork. Dry van loads run roughly $2-5 a mile depending on local or OTR lanes, and the dispatch fee is 5-6% of weekly gross for OTR semis.",
        "body": [
            "Dry van is the most common trailer on the road, which means the most freight and the most competition for it. Good dry van dispatch is about lanes: booking the next load before this one delivers and avoiding markets that leave you stuck.",
        ],
        "faqs": [
            ("How much do dry van loads pay per mile?", "Roughly $2-5 a mile. Short local loads can pay more per mile, long OTR runs less per mile but more per load. Rates are not guaranteed."),
        ],
    },
    {
        "file": "reefer-dispatch.html", "nav": "Reefer Dispatch", "kind": "semi",
        "title": "Reefer Dispatch Service | Refrigerated Truck Dispatch | Texas Solutions",
        "description": "Reefer dispatch for owner-operators and small fleets: temperature-controlled loads, appointment coordination, rate negotiation and paperwork. 5-6% of weekly gross for OTR semis.",
        "keywords": "reefer dispatch, reefer dispatch service, refrigerated truck dispatch, reefer loads, reefer dispatcher",
        "h1": "Reefer Dispatch Service",
        "lede": "Temperature-controlled freight negotiated for your reefer, with appointments confirmed before you commit.",
        "answer": "Texas Solutions provides reefer dispatch for owner-operators and small fleets nationwide. Dispatchers find temperature-controlled loads, confirm temperature and appointment requirements with brokers and handle paperwork. The fee is 5-6% of weekly gross for OTR reefer semis, with no flat rate.",
        "body": ["Reefer freight pays for precision: set temperatures and tight appointments. We confirm both with the broker before a load reaches you."],
        "faqs": [("Do you check temperature requirements before booking?", "Yes. We confirm temperature, appointment times and special handling before presenting the load.")],
    },
    {
        "file": "power-only-dispatch.html", "nav": "Power Only Dispatch", "kind": "semi",
        "title": "Power Only Dispatch Service | Texas Solutions",
        "description": "Power only dispatch for tractors without trailers: preloaded and drop-and-hook freight, rate negotiation and paperwork. 5-6% of weekly gross for OTR.",
        "keywords": "power only dispatch, power only dispatch service, power only loads, power only trucking dispatch",
        "h1": "Power Only Dispatch Service",
        "lede": "Preloaded trailers and drop-and-hook freight found and negotiated for your tractor.",
        "answer": "Texas Solutions provides power only dispatch for owner-operators with a tractor and no trailer. Dispatchers find preloaded and drop-and-hook loads, negotiate the rate and handle broker paperwork. The fee is 5-6% of weekly gross for OTR operations.",
        "body": ["Power only lets a tractor earn without the cost of a trailer. The work is finding enough of those loads in the right places, which is what we do."],
        "faqs": [("Do I need a trailer for power only?", "No. The trailer is supplied by the shipper, broker or a carrier program. You provide the tractor and authority.")],
    },
    {
        "file": "owner-operator-dispatch.html", "nav": "Owner-Operator Dispatch", "kind": "semi",
        "title": "Owner-Operator Dispatch Service | 5-6% Semi, 8-10% Small Truck | Texas Solutions",
        "description": "Dispatch service for owner-operators and small fleets: load search, rate negotiation and paperwork. 5-6% of weekly gross for semis, 8-10% for small trucks, OTR. No flat rate or upfront fee.",
        "keywords": "owner operator dispatch service, dispatch service for owner operators, small fleet dispatch, dispatcher for owner operators, independent truck dispatch, owner operator dispatcher cost",
        "h1": "Dispatch for Owner-Operators",
        "lede": "You run the truck. We handle the boards, the brokers and the paperwork, and you approve every load.",
        "answer": "Texas Solutions is a dispatch service for owner-operators and small fleets. It handles load search, rate negotiation, broker communication and paperwork for 5-6% of weekly gross on OTR semis and 8-10% on small trucks, with no flat rate, no upfront fee, no long-term contract and no forced loads.",
        "body": [
            "Owner-operators lose hours every day to load boards and broker calls. A dispatcher takes that work on without taking control: you set the lanes, the home time and your minimum, and you approve every load.",
            "Small fleets get the same service per truck, with each truck's equipment and lanes handled separately.",
        ],
        "faqs": [("Is a dispatcher worth it for an owner-operator?", "For many, yes, when the dispatcher saves time, cuts deadhead and negotiates better loads by more than the fee. Results vary and no dispatcher can guarantee earnings.")],
    },
    {
        "file": "texas-truck-dispatch.html", "nav": "Texas Truck Dispatch", "kind": "semi",
        "title": "Texas Truck Dispatch Service | Midland, Houston, Dallas | Texas Solutions",
        "description": "Truck dispatch company based in Midland, Texas, dispatching owner-operators on Texas lanes: Permian Basin, Houston, Dallas-Fort Worth, San Antonio, Laredo and El Paso, plus nationwide OTR.",
        "keywords": "truck dispatch Texas, truck dispatch service Texas, Midland TX truck dispatch, Permian Basin dispatch, Houston truck dispatch, Dallas truck dispatch, San Antonio truck dispatch, Texas hotshot dispatch",
        "h1": "Texas Truck Dispatch Service",
        "lede": "A Texas dispatch team for carriers who run Texas, and everywhere those loads lead.",
        "answer": "Texas Solutions is a truck dispatch company based at 401 W Kentucky Ave, Midland, Texas. It dispatches owner-operators and small fleets on Texas lanes, including the Permian Basin, Houston, Dallas-Fort Worth, San Antonio, Laredo and El Paso, and nationwide OTR, for 5-6% of weekly gross on semis and 8-10% on small trucks.",
        "body": [
            "Texas is one of the largest freight markets in the country, with energy, manufacturing, cross-border and port freight moving through it every day.",
            "Our team is based in Midland, in the heart of the Permian Basin, and works with carriers running flatbed, hotshot, dry van, reefer and box trucks across Texas and beyond.",
        ],
        "faqs": [("Where is Texas Solutions located?", "401 W Kentucky Ave, Midland, Texas. We dispatch carriers throughout the United States.")],
    },
    {
        "file": "what-does-a-truck-dispatcher-do.html", "nav": "What a Truck Dispatcher Does", "kind": "semi", "guide": True,
        "title": "What Does a Truck Dispatcher Do? Duties & Cost (2026 Guide) | Texas Solutions",
        "description": "What a truck dispatcher does, how much truck dispatch costs (5-6% for semis, 8-10% for small trucks at Texas Solutions), dispatcher vs broker, and how to choose a dispatch service.",
        "keywords": "what does a truck dispatcher do, how much does a truck dispatcher cost, truck dispatcher fees, truck dispatcher percentage, dispatcher vs broker, how to choose a truck dispatch service",
        "h1": "What Does a Truck Dispatcher Do?",
        "lede": "The job, the usual fees, the difference from a broker, and what to check before you sign.",
        "answer": "A truck dispatcher finds and books freight for a carrier's trucks: searching load boards and brokers, negotiating rates, confirming loads with the driver, completing broker setup paperwork and organizing rate confirmations. Independent dispatchers usually charge a percentage of weekly gross; Texas Solutions charges 5-6% for OTR semis and 8-10% for small trucks.",
        "body": [
            "Most owner-operators start by dispatching themselves. It works until the hours on the phone start competing with the hours behind the wheel.",
        ],
        "sections": [
            ("The daily duties of a truck dispatcher", [
                "Search load boards and broker networks for freight that fits the truck and lanes.",
                "Negotiate rates with brokers before presenting a load.",
                "Plan the next load to reduce deadhead miles.",
                "Complete broker setup packets with the carrier's MC authority, W-9 and insurance.",
                "Keep rate confirmations and dispatch details organized.",
            ]),
            ("How much does a truck dispatcher cost?", [
                "Most independent dispatchers charge a percentage of the truck's weekly gross rather than a salary.",
                "Texas Solutions: 5-6% of weekly gross for OTR semi trucks, 8-10% for OTR small trucks (box truck, straight truck, hotshot).",
                "On a semi grossing $8,000-$10,000 a week, 5-6% is about $400-$600 a week.",
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
        "faqs": [("Can a dispatcher guarantee my weekly gross?", "No. Rates and freight volume change with the market, and a reputable dispatcher will not guarantee earnings.")],
    },
]
