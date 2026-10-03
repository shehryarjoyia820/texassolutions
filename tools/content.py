"""
All words and numbers for dispatch.texassolutions.co.
Edit here, then run:  python tools/site.py

Pricing (OTR only, no flat rate, % of weekly gross):
  Semi trucks (dry van, reefer, flatbed, step deck, power only): 5%,
      typical weekly gross $8,000-$10,000
  Box truck and straight truck: 10%; hotshot: 8%;
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
WEB3FORMS_KEY = "c66393e0-d742-483a-b9d0-a923d09baa97"

# -------------------------------------------------------------- pricing
PRICING = {
    "small": {
        "label": "Small trucks",
        "equipment": ["Box Truck", "Straight Truck", "Hotshot"],
        "pct": (8, 10),  # hotshot 8%, box and straight truck 10% (see EQ_PCT)
        "gross": (7000, 9000),
    },
    "semi": {
        "label": "Semi trucks",
        "equipment": ["Dry Van", "Reefer", "Flatbed", "Step Deck", "Power Only"],
        "pct": (5, 5),
        "gross": (8000, 10000),
    },
}
# Dispatch percentage for each truck type.
EQ_PCT = {"Dry Van": 5, "Reefer": 5, "Flatbed": 5, "Step Deck": 5, "Power Only": 5,
          "Box Truck": 10, "Straight Truck": 10, "Hotshot": 8}
PRICING_CONDITION = "Rates apply to OTR (over-the-road) operations. Local and regional work is quoted separately."
PRICING_NOTE = "Rough estimate only. Your final percentage is confirmed in your signed dispatch agreement. Your first load is dispatched free. No flat rate, no setup fee, no monthly subscription."

# Rough rate-per-mile guide by equipment (for the rate board and estimate page).
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
    ("Midland, TX", "Phoenix, AZ", "Flatbed", 872, "$5.60"),
    ("Odessa, TX", "Oklahoma City, OK", "Hotshot", 412, "$4.85"),
    ("Laredo, TX", "Atlanta, GA", "Dry Van", 1142, "$3.25"),
    ("Dallas, TX", "Denver, CO", "Flatbed", 793, "$6.40"),
    ("Houston, TX", "Memphis, TN", "Dry Van", 587, "$3.10"),
    ("Amarillo, TX", "Salt Lake City, UT", "Hotshot", 906, "$4.40"),
    ("El Paso, TX", "Los Angeles, CA", "Power Only", 801, "$3.45"),
    ("San Antonio, TX", "Nashville, TN", "Step Deck", 1024, "$5.90"),
    ("Fort Worth, TX", "Kansas City, MO", "Reefer", 520, "$4.80"),
    ("Houston, TX", "San Antonio, TX", "Dry Van", 197, "$4.60"),
    ("San Antonio, TX", "Shreveport, LA", "Hotshot", 392, "$4.30"),
    ("Dallas, TX", "Houston, TX", "Box Truck", 239, "$2.90"),
    ("Midland, TX", "San Antonio, TX", "Box Truck", 320, "$2.60"),
    ("Fort Worth, TX", "Oklahoma City, OK", "Box Truck", 205, "$3.10"),
    ("Houston, TX", "New Orleans, LA", "Box Truck", 348, "$2.40"),
    ("El Paso, TX", "Phoenix, AZ", "Box Truck", 430, "$2.20"),
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
    "power only dispatch", "step deck dispatch", "truck dispatch Texas", "dispatch service for small fleets",
    "how much does a truck dispatcher cost", "truck dispatch fee", "5% truck dispatch",
    "truck dispatch services", "trucking dispatch services", "truck dispatch company USA", "dispatch services for truckers",
    "hire a truck dispatcher", "truck dispatcher for hire", "24/7 truck dispatch service", "remote truck dispatcher",
    "dispatch for new authority", "semi truck dispatch services",
]

# -------------------------------------------------------------- FAQs (site-wide)
FAQS = [
    ("How much does a truck dispatcher cost?",
     "At Texas Solutions, semi trucks pay 5% of weekly gross, hotshots 8%, and box trucks and straight trucks 10%, for OTR operations. There is no flat rate, no setup fee and no monthly subscription. On a typical semi grossing $8,000-$10,000 a week, that is about $400-$500 a week."),
    ("What does a truck dispatcher do?",
     "A truck dispatcher searches load boards and broker networks for freight that fits your truck, negotiates the rate, confirms the load with you, completes broker setup paperwork and keeps rate confirmations organized, so you can spend your time driving."),
    ("Do you dispatch local routes or only OTR?",
     "Our published rates apply to OTR (over-the-road) operations. Local and regional work is quoted separately, so call or message us with your lanes."),
    ("Is there a flat weekly fee?",
     "No. Texas Solutions charges a percentage of weekly gross only, so you pay when your truck earns and nothing in a week it sits. There is no flat rate, no setup fee and no monthly subscription, and your first load is dispatched free."),
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
    ("Are your dispatchers available 24/7?",
     "Yes. Our dispatchers work remotely across US time zones and are available 24/7 by phone, text or WhatsApp at (838) 910-3147, including nights and weekends when loads, breakdowns and reloads come up."),
    ("Is there a free trial?",
     "Yes. Your first load is dispatched free so you can see how we work. After that the fee is a percentage of weekly gross: 5% for semis, 8% for hotshots, 10% for box trucks and straight trucks."),
    ("Do you work with new MC authority?",
     "Yes, from day one. We work with brand-new MC numbers, help with broker setup packets and look for brokers that accept new authorities. See dispatch for new authority for details."),
    ("Do you handle paperwork and invoicing?",
     "Yes. Besides load search and rate negotiation we handle broker carrier packets, rate confirmations, invoicing and billing, detention and lumper fee collection, factoring setup, IFTA filing, DOT compliance help and MC authority setup."),
    ("What is the best truck dispatch service for owner-operators in the USA?",
     "The best fit is the one that matches your truck and authority: a clear percentage with no hidden fees, no long-term contract, no forced loads, help with paperwork, and real people you can reach. Texas Solutions charges 5% for semis, 8% for hotshots and 10% for box trucks, works with new MC, is available 24/7 and dispatches your first load free."),
    ("Which dispatch service charges the lowest percentage?",
     "Percentages vary by equipment and by what is included. Compare the total value, not only the rate: does the fee include broker setups, invoicing and negotiation, and is there a setup fee or contract? Texas Solutions charges 5% of weekly gross for OTR semis, with no setup fee or contract."),
    ("Do you dispatch small fleets with 3 to 5 trucks?",
     "Yes. Each truck is dispatched to its own equipment, lanes and home time, at the same percentage per truck. Fleet owners get one point of contact for every truck."),
    ("Do you work with lease operators?",
     "We dispatch carriers that run under their own MC authority. If you are leased on to another carrier, that carrier normally dispatches you; talk to us when you get your own authority and we can help set it up."),
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
        "file": "box-truck-dispatch.html", "nav": "Box Truck Dispatch", "kind": "small",
        "title": "Box Truck Dispatch Service | 10% OTR Dispatch Fee | Texas Solutions",
        "description": "Box truck dispatch for owner-operators and small fleets: load search, rate negotiation and broker paperwork for box trucks and straight trucks. 10% of weekly gross, OTR, no flat fee.",
        "keywords": "box truck dispatch, box truck dispatch service, box truck dispatcher, straight truck dispatch, 26 ft box truck loads, box truck dispatch company, non CDL box truck dispatch",
        "h1": "Box Truck Dispatch Service",
        "lede": "We find, negotiate and book freight for box trucks and straight trucks, while you drive.",
        "answer": "Texas Solutions provides box truck dispatch for owner-operators and small fleets across the United States. Dispatchers search and negotiate loads, complete broker setups and keep paperwork organized. The fee is 10% of weekly gross for OTR box trucks and straight trucks, with no flat rate, no setup fee and your approval on every load.",
        "body": [
            "Box truck freight moves in smaller, more frequent loads, which means more calls, more broker setups and more paperwork for every dollar your truck earns. Our dispatchers work the box truck side of the load boards every day.",
            "We match freight to your box length, liftgate and payload, plan around your home time, and negotiate before anything reaches you. Typical OTR box trucks on our desk gross $7,000 to $9,000 a week.",
            "Whether you run a 26 ft box truck, a smaller non-CDL box truck or a straight truck, your box truck dispatcher handles load search, broker setups, invoicing and rate confirmations, and is reachable 24/7.",
        ],
        "faqs": [
            ("How much is box truck dispatch?", "10% of weekly gross for OTR box trucks and straight trucks. On $7,000-$9,000 weekly gross that is about $700-$900 a week. No flat rate and no setup fee."),
            ("Do you dispatch non-CDL box trucks?", "Yes, as long as you run under your own MC authority. Tell us your truck size and weight rating and we search freight that fits."),
            ("Do you dispatch 26 ft box trucks?", "Yes. 26 ft box trucks are the most common truck on our box truck desk. We match loads to your box length, liftgate and payload, and plan around your home time."),
            ("Can you dispatch a box truck with new authority?", "Yes. We work with new MC numbers from day one and look for brokers that accept new authorities for box truck freight. Your first load is dispatched free."),
        ],
    },
    {
        "file": "hotshot-dispatch.html", "nav": "Hotshot Dispatch", "kind": "small",
        "title": "Hotshot Dispatch Service | 8% Dispatch Fee, $4-5/Mile Loads | Texas Solutions",
        "description": "Hotshot dispatch for owner-operators: expedited and partial loads, rate negotiation and broker paperwork. Hotshot loads often pay $4-5 a mile. Dispatch fee 8% of weekly gross, OTR.",
        "keywords": "hotshot dispatch, hotshot dispatch service, hotshot dispatcher, hotshot trucking dispatch, hotshot loads, gooseneck dispatch, hotshot dispatch Texas, Permian Basin hotshot",
        "h1": "Hotshot Dispatch Service",
        "lede": "Time-sensitive hotshot freight found, negotiated and confirmed with you before it is booked.",
        "answer": "Texas Solutions dispatches hotshot trucks for owner-operators across the United States, including Texas and the Permian Basin. Dispatchers find expedited and partial loads, negotiate rates that often run $4-5 a mile, and handle broker paperwork. The dispatch fee is 8% of weekly gross for OTR hotshots, with no flat rate.",
        "body": [
            "Hotshot freight is fast and time-critical: equipment, machinery, construction and oilfield materials that cannot wait for a full truckload. Winning it means answering brokers fast and knowing which lanes pay.",
            "From our base in Midland, Texas, we see a lot of hotshot freight move through the Permian Basin and across Texas. Rough rates on hotshot loads commonly run $4 to $5 a mile.",
            "Your hot shot dispatcher works 24/7, because expedited freight does not wait for business hours, and handles broker packets, rate confirmations and invoicing so you can keep driving.",
        ],
        "faqs": [
            ("How much do hotshot loads pay per mile?", "As a rough guide, hotshot loads often pay about $4-5 a mile, depending on lane, urgency and season. Rates are not guaranteed."),
            ("What is the dispatch fee for hotshots?", "8% of weekly gross for OTR hotshot operations, with no flat rate, no setup fee and no monthly subscription. On $7,000-$9,000 weekly gross that is about $560-$720 a week."),
            ("Do you dispatch non-CDL hotshots?", "Yes, if you run under your own MC authority. A non-CDL setup has a lower combined weight rating, so we look for lighter freight that fits your limits."),
            ("Can I get a hotshot dispatcher without a contract?", "Yes. There is no long-term contract, no setup fee and no forced dispatch, and your first load is dispatched free. You approve every load."),
        ],
    },
    {
        "file": "flatbed-dispatch.html", "nav": "Flatbed & Step Deck Dispatch", "kind": "semi",
        "title": "Flatbed Dispatch Service | 5% Fee, $5-7/Mile Loads | Texas Solutions",
        "description": "Flatbed and step deck dispatch for owner-operators and small fleets. Open-deck loads often pay $5-7 a mile. Dispatch fee 5% of weekly gross for OTR semis. No flat rate.",
        "keywords": "flatbed dispatch, flatbed dispatch service, flatbed dispatcher, step deck dispatch, open deck dispatch, flatbed loads per mile, flatbed truck dispatch company",
        "h1": "Flatbed & Step Deck Dispatch",
        "lede": "Open-deck freight searched, sized up and negotiated for your flatbed or step deck.",
        "answer": "Texas Solutions provides flatbed and step deck dispatch for owner-operators and small fleets nationwide. Dispatchers find open-deck loads that often pay $5-7 a mile, confirm dimensions, weight and tarping, and handle broker paperwork. The fee is 5% of weekly gross for OTR semis, with no flat rate.",
        "body": [
            "Open-deck freight comes with more questions than a sealed trailer: dimensions, weight, tarps, straps and chains, and whether a step deck is needed for height. We ask those questions before the load reaches you.",
            "Texas and the Permian Basin move a large share of the country's open-deck freight, including steel, building materials, machinery and oilfield equipment.",
        ],
        "faqs": [
            ("How much do flatbed loads pay per mile?", "As a rough guide, flatbed and step deck loads often pay about $5-7 a mile, depending on lane, tarping and season. Rates are not guaranteed."),
            ("What is the dispatch fee for flatbeds?", "5% of weekly gross for OTR flatbed and step deck semis. On $8,000-$10,000 weekly gross that is about $400-$500 a week."),
            ("Do you offer step deck dispatch services?", "Yes. Step deck is dispatched alongside flatbed: we find taller open-deck loads that need the lower deck height and confirm dimensions, weight and securement before you commit."),
        ],
    },
    {
        "file": "dry-van-dispatch.html", "nav": "Dry Van Dispatch", "kind": "semi",
        "title": "Dry Van Dispatch Service | 5% OTR Dispatch Fee | Texas Solutions",
        "description": "Dry van dispatch for owner-operators and small fleets: lane planning, rate negotiation and broker paperwork. Dry van loads run about $3-5 a mile depending on local or OTR. Fee 5% of weekly gross.",
        "keywords": "dry van dispatch, dry van dispatch service, dry van dispatcher, dry van loads per mile, 53 ft dry van dispatch, dry van trucking dispatch",
        "h1": "Dry Van Dispatch Service",
        "lede": "Lanes planned, deadhead cut and every load negotiated, with you approving each booking.",
        "answer": "Texas Solutions provides dry van dispatch for owner-operators and small fleets nationwide. Dispatchers plan lanes to reduce deadhead, negotiate every load and handle broker paperwork. Dry van loads run roughly $3-5 a mile depending on local or OTR lanes, and the dispatch fee is 5% of weekly gross for OTR semis.",
        "body": [
            "Dry van is the most common trailer on the road, which means the most freight and the most competition for it. Good dry van dispatch is about lanes: booking the next load before this one delivers and avoiding markets that leave you stuck.",
        ],
        "faqs": [
            ("How much do dry van loads pay per mile?", "Roughly $3-5 a mile. Short local loads can pay more per mile, long OTR runs less per mile but more per load. Rates are not guaranteed."),
            ("How do I find the best paying loads for a dry van?", "Plan lanes, not single loads: book the next load before this one delivers, avoid markets with little outbound freight unless the rate covers it, and negotiate every rate. Our dry van dispatch services do this for you 24/7."),
        ],
    },
    {
        "file": "reefer-dispatch.html", "nav": "Reefer Dispatch", "kind": "semi",
        "title": "Reefer Dispatch Service | Refrigerated Truck Dispatch | Texas Solutions",
        "description": "Reefer dispatch for owner-operators and small fleets: temperature-controlled loads, appointment coordination, rate negotiation and paperwork. 5% of weekly gross for OTR semis.",
        "keywords": "reefer dispatch, reefer dispatch service, refrigerated truck dispatch, reefer loads, reefer dispatcher",
        "h1": "Reefer Dispatch Service",
        "lede": "Temperature-controlled freight negotiated for your reefer, with appointments confirmed before you commit.",
        "answer": "Texas Solutions provides reefer dispatch for owner-operators and small fleets nationwide. Dispatchers find temperature-controlled loads, confirm temperature and appointment requirements with brokers and handle paperwork. The fee is 5% of weekly gross for OTR reefer semis, with no flat rate.",
        "body": ["Reefer freight pays for precision: set temperatures and tight appointments. We confirm both with the broker before a load reaches you.",
                 "Our reefer dispatch services cover refrigerated truck dispatch nationwide, with dispatchers available 24/7 for the early appointments and overnight reloads reefer freight brings."],
        "faqs": [("Do you check temperature requirements before booking?", "Yes. We confirm temperature, appointment times and special handling before presenting the load."),
                 ("Do you dispatch reefer trucks running the Midwest?", "Yes. We dispatch reefers nationwide, including Midwest lanes, and plan reloads around produce and food distribution markets so you are not stuck empty. Your first load is dispatched free.")],
    },
    {
        "file": "power-only-dispatch.html", "nav": "Power Only Dispatch", "kind": "semi",
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
        "file": "owner-operator-dispatch.html", "nav": "Owner-Operator Dispatch", "kind": "semi",
        "title": "Owner-Operator Dispatch Service | 5% Semi, 8% Hotshot, 10% Box Truck | Texas Solutions",
        "description": "Dispatch service for owner-operators and small fleets: load search, rate negotiation and paperwork. 5% of weekly gross for semis, 8% for hotshots, 10% for box trucks, OTR. No flat rate or upfront fee.",
        "keywords": "owner operator dispatch service, dispatch service for owner operators, small fleet dispatch, dispatcher for owner operators, independent truck dispatch, owner operator dispatcher cost",
        "h1": "Dispatch for Owner-Operators",
        "lede": "You run the truck. We handle the boards, the brokers and the paperwork, and you approve every load.",
        "answer": "Texas Solutions is a dispatch service for owner-operators and small fleets. It handles load search, rate negotiation, broker communication and paperwork for 5% of weekly gross on OTR semis, 8% on hotshots and 10% on box trucks, with no flat rate, no upfront fee, no long-term contract and no forced loads.",
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
                 ("Do you offer dispatch for one truck?", "Yes. Most of the carriers we work with run one truck. The fee is the same percentage of weekly gross, and your first load is dispatched free."),
                 ("Can you compare dispatch for a small fleet of 3 to 5 trucks?", "Each truck pays the same percentage of its own weekly gross: 5% for semis, 8% for hotshots, 10% for box trucks. There is no fleet setup fee, and each truck gets lanes planned for its equipment and home time.")],
    },
    {
        "file": "dispatch-for-new-authority.html", "nav": "New Authority Dispatch", "kind": "semi",
        "title": "Dispatch for New Authority & New MC Numbers | Texas Solutions",
        "description": "Truck dispatch for new authority and new MC numbers from day one: broker setups, brokers that accept new MCs, first load free, 24/7 dispatchers, no contract.",
        "keywords": "dispatch for new authority, dispatch services for new MC number, dispatcher for new trucking company, dispatch for carriers with new authority, dispatcher who works with new MC, brokers that work with new authority, how to get loads with new authority",
        "h1": "Dispatch for New Authority",
        "lede": "A dispatcher who works with a new MC from day one: broker setups, the brokers that accept new authorities, and your first load dispatched free.",
        "answer": "Texas Solutions dispatches carriers with brand-new MC authority from day one. Dispatchers send your carrier packets, find brokers that accept new MC numbers, negotiate every load and handle rate confirmations and invoicing, 24/7. Your first load is dispatched free; after that the fee is 5% of weekly gross for semis, 8% for hotshots and 10% for box trucks.",
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
            "MC authority setup help if you have not filed yet",
            "Invoicing, factoring setup and rate confirmations",
            "24/7 dispatchers by phone, text or WhatsApp",
            "First load dispatched free, no contract, no setup fee",
        ],
        "faqs": [
            ("Do you dispatch new authority?", "Yes, from day one. We work with brand-new MC numbers and set you up with brokers that accept new authorities."),
            ("Which dispatch companies work with new MC authorities?", "Texas Solutions works with new MC authorities from day one, for dry van, reefer, flatbed, step deck, power only, hotshot, box truck and straight truck. The first load is dispatched free and there is no long-term contract."),
            ("Can you dispatch a box truck with new authority?", "Yes. Box trucks with new authority are a large part of our desk. We look for box truck freight from brokers that accept new MC numbers. The fee is 10% of weekly gross after your free first load."),
            ("Why do some brokers not work with new authority?", "Many brokers set a minimum authority age or insurance history to manage risk. Others accept new carriers if the packet is complete and insurance is verified. Knowing which is which saves days of calls."),
        ],
    },
    {
        "file": "trucking-back-office-services.html", "nav": "Back-Office Services", "kind": "semi",
        "title": "Trucking Back-Office Services: Invoicing, IFTA & Setup",
        "description": "Trucking back-office services with dispatch: broker packets, invoicing, detention and lumper collection, factoring setup, IFTA filing, DOT help, MC setup.",
        "keywords": "trucking back office services, trucking paperwork services, broker carrier packet setup, trucking invoicing service, trucking billing services, factoring and dispatch services, IFTA filing service, trucking compliance services, DOT compliance help, MC authority setup service, detention and lumper fee collection, trucking accounting and dispatch, ELD and dispatch support, carrier setup with brokers",
        "h1": "Trucking Back-Office Services",
        "lede": "The paperwork behind every load, handled: broker setups, invoicing, detention and lumper collection, factoring, IFTA, DOT compliance and MC authority setup.",
        "answer": "Texas Solutions handles trucking back-office work alongside dispatch: broker carrier packets and carrier setup with brokers, rate confirmations, invoicing and billing, detention and lumper fee collection, factoring setup, IFTA filing, DOT compliance help and MC authority setup. Dispatchers are available 24/7, and the first load is dispatched free.",
        "body": [
            "Hauling the load is half the job. The other half is the carrier packet before it, and the invoice, the detention claim and the fuel tax report after it. Missed paperwork means late pay and money left on the table.",
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
        "file": "texas-truck-dispatch.html", "nav": "Texas Truck Dispatch", "kind": "semi",
        "title": "Texas Truck Dispatch Service | Midland, Houston, Dallas | Texas Solutions",
        "description": "Truck dispatch company based in Midland, Texas, dispatching owner-operators on Texas lanes: Permian Basin, Houston, Dallas-Fort Worth, San Antonio, Laredo and El Paso, plus nationwide OTR.",
        "keywords": "truck dispatch Texas, truck dispatch service Texas, Midland TX truck dispatch, Permian Basin dispatch, Houston truck dispatch, Dallas truck dispatch, San Antonio truck dispatch, Texas hotshot dispatch",
        "h1": "Texas Truck Dispatch Service",
        "lede": "A Texas dispatch team for carriers who run Texas, and everywhere those loads lead.",
        "answer": "Texas Solutions is a truck dispatch company based at 401 W Kentucky Ave, Midland, Texas. It dispatches owner-operators and small fleets on Texas lanes, including the Permian Basin, Houston, Dallas-Fort Worth, San Antonio, Laredo and El Paso, and nationwide OTR, for 5% of weekly gross on semis, 8% on hotshots and 10% on box trucks.",
        "body": [
            "Texas is one of the largest freight markets in the country, with energy, manufacturing, cross-border and port freight moving through it every day.",
            "Our team is based in Midland, in the heart of the Permian Basin, and works with carriers running flatbed, hotshot, dry van, reefer and box trucks across Texas and beyond.",
        ],
        "faqs": [("Where is Texas Solutions located?", "401 W Kentucky Ave, Midland, Texas. We dispatch carriers throughout the United States."),
                 ("Do you offer truck dispatch services in Houston and Dallas?", "Yes. We dispatch carriers based in Houston, Dallas-Fort Worth and across Texas, including hotshot dispatch in Texas and the Permian Basin, 24/7, with your first load dispatched free."),
                 ("Is there a truck dispatcher near me in Texas?", "Our office is in Midland, and our dispatchers work remotely around the clock, so carriers anywhere in Texas reach a dispatcher by phone, text or WhatsApp at (838) 910-3147.")],
    },
    {
        "file": "what-does-a-truck-dispatcher-do.html", "nav": "What a Truck Dispatcher Does", "kind": "semi", "guide": True,
        "title": "What Does a Truck Dispatcher Do? Duties & Cost (2026 Guide) | Texas Solutions",
        "description": "What a truck dispatcher does, how much truck dispatch costs (5% for semis, 8% for hotshots, 10% for box trucks at Texas Solutions), dispatcher vs broker, and how to choose a dispatch service.",
        "keywords": "what does a truck dispatcher do, how much does a truck dispatcher cost, truck dispatcher fees, truck dispatcher percentage, dispatcher vs broker, how to choose a truck dispatch service",
        "h1": "What Does a Truck Dispatcher Do?",
        "lede": "The job, the usual fees, the difference from a broker, and what to check before you sign.",
        "answer": "A truck dispatcher finds and books freight for a carrier's trucks: searching load boards and brokers, negotiating rates, confirming loads with the driver, completing broker setup paperwork and organizing rate confirmations. Independent dispatchers usually charge a percentage of weekly gross; Texas Solutions charges 5% for OTR semis, 8% for hotshots and 10% for box trucks.",
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
                "Texas Solutions: 5% of weekly gross for OTR semi trucks, 8% for hotshots, 10% for box trucks and straight trucks.",
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
        "faqs": [("Can a dispatcher guarantee my weekly gross?", "No. Rates and freight volume change with the market, and a reputable dispatcher will not guarantee earnings.")],
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
        'Truck Dispatch Services, 24/7 | Texas Solutions USA',
        'USA truck dispatch services, 24/7: semi 5%, hotshot 8%, box truck 10% of weekly gross. First load free, new MC welcome, no contract. Plus free trucking tools.'),
    '/estimate.html': (
        'Truck Dispatch Fee Calculator & Free Quote | Texas Solutions',
        'Calculate your truck dispatch fee: semi 5%, hotshot 8%, box truck 10% of weekly gross, OTR. Pick your truck, set your own percentage, get a free quote.'),
    '/truck-dispatch-rates.html': (
        'Truck Dispatch Service Cost & Rates | Texas Solutions',
        'What truck dispatchers charge: 5% semi, 8% hotshot, 10% box truck of weekly gross. No flat rate, no contract, no upfront fee, first load free.'),
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
        'Box truck dispatch for owner-operators: load search, rate negotiation and broker paperwork for box and straight trucks. 10% of weekly gross, OTR, no flat fee.'),
    '/hotshot-dispatch.html': (
        'Hotshot Dispatch Services & 24/7 Hot Shot Dispatcher',
        'Hotshot dispatch for owner-operators: expedited and partial loads, rate negotiation and paperwork. Loads often pay $4-5 a mile. 8% of weekly gross, OTR.'),
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
        'Dispatch Service for Owner-Operators & Small Fleets',
        'Dispatch for owner-operators and small fleets: load search, rate negotiation and paperwork. 5% semi, 8% hotshot, 10% box truck of weekly gross, OTR.'),
    '/texas-truck-dispatch.html': (
        'Truck Dispatch Services in Texas | Midland, Houston, Dallas',
        'Truck dispatch based in Midland, Texas: Permian Basin, Houston, Dallas-Fort Worth, San Antonio, Laredo and El Paso lanes plus nationwide OTR.'),
    '/what-does-a-truck-dispatcher-do.html': (
        'What Does a Truck Dispatcher Do? Duties & Cost | Texas Solutions',
        'What a truck dispatcher does, how much dispatch costs (5% semi, 8% hotshot, 10% box truck at Texas Solutions), dispatcher vs broker, and how to choose one.'),
    '/about.html': (
        'About Texas Solutions | Truck Dispatch, Midland TX',
        'Texas Solutions is a truck dispatch company in Midland, Texas working for owner-operators and small fleets. Not a broker. No flat rate, no forced loads.'),
    '/contact.html': (
        'Contact a Truck Dispatcher | Call or WhatsApp | Texas Solutions',
        'Talk to a Texas Solutions truck dispatcher: call or WhatsApp (838) 910-3147, email dispatch@texassolutions.co, or send your details. Midland, TX.'),
    '/faq.html': (
        'Truck Dispatch FAQ: Cost, OTR & How It Works | Texas Solutions',
        'Answers about truck dispatch: what a dispatcher costs (5% semi, 8% hotshot, 10% box truck), OTR vs local, contracts, paperwork and getting started.'),
}
