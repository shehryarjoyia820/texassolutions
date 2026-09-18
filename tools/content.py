"""
Content for dispatch.texassolutions.co SEO and AEO.

Facts here must match the live site: percentage-based pricing set in the
dispatch agreement (no published rate), no upfront or setup fee, no long-term
contract, no guaranteed loads, rates or earnings, carrier approves every load,
Texas Solutions is a dispatch service and not a motor carrier or broker.
"""

BASE = "https://dispatch.texassolutions.co"
MAIN_SITE = "https://texassolutions.co"
NAME = "Texas Solutions"
BRAND = "Texas Solutions Truck Dispatch"
PHONE = "(838) 910-3147"
PHONE_E164 = "+18389103147"
EMAIL = "info@texassolutions.co"
STREET = "401 W Kentucky Ave"
CITY = "Midland"
REGION = "TX"
COUNTRY = "US"

EQUIPMENT = [
    "Dry Van", "Reefer", "Flatbed", "Step Deck",
    "Power Only", "Hotshot", "Box Truck", "Straight Truck",
]

# --------------------------------------------------------------------------
# Existing pages: SEO titles and descriptions
# --------------------------------------------------------------------------
PAGES = {
    "index.html": {
        "title": "Truck Dispatch Services for Owner-Operators & Small Fleets | Texas Solutions",
        "description": "Truck dispatch service for owner-operators and small fleets: load search, rate negotiation, broker communication and paperwork for dry van, reefer, flatbed, hotshot, box truck and power only. No upfront cost, no long-term contract.",
        "keywords": "truck dispatch service, truck dispatching company, owner operator dispatch service, dispatch service for owner operators, box truck dispatch, hotshot dispatch, dry van dispatch, reefer dispatch, flatbed dispatch, power only dispatch, independent truck dispatcher",
        "path": "/",
    },
    "about.html": {
        "title": "About Texas Solutions | Direct Truck Dispatch Team, Not a Lead Broker",
        "description": "Texas Solutions is a truck dispatch team based in Midland, Texas, providing dispatch services directly to owner-operators and small fleets. We are not a freight broker and never sell your application.",
        "keywords": "truck dispatch company Texas, dispatch company Midland TX, direct truck dispatch service",
        "path": "/about.html",
    },
    "contact.html": {
        "title": "Contact a Truck Dispatcher | Texas Solutions Dispatch (838) 910-3147",
        "description": "Talk directly with a Texas Solutions truck dispatcher. Apply for dispatch services online or call (838) 910-3147. No upfront cost and no long-term contract.",
        "keywords": "contact truck dispatcher, hire a truck dispatcher, truck dispatch near me",
        "path": "/contact.html",
    },
    "faq.html": {
        "title": "Truck Dispatch FAQ | Fees, Contracts, Equipment & Onboarding | Texas Solutions",
        "description": "Answers about Texas Solutions truck dispatch services: how dispatch fees work, contracts, what a dispatcher does, equipment we dispatch, documents needed and how to get started.",
        "keywords": "truck dispatch FAQ, how much does a truck dispatcher cost, what does a truck dispatcher do, dispatch service contract",
        "path": "/faq.html",
    },
    "privacy.html": {
        "title": "Privacy Policy | Texas Solutions Truck Dispatch",
        "description": "How Texas Solutions collects, uses and protects carrier information and SMS consent for its truck dispatch services.",
        "path": "/privacy.html",
    },
    "terms.html": {
        "title": "Terms & Conditions | Texas Solutions Truck Dispatch",
        "description": "Terms and conditions for the Texas Solutions website and truck dispatch services.",
        "path": "/terms.html",
    },
}

# --------------------------------------------------------------------------
# Answer-engine FAQs added to the home page and the FAQ page
# --------------------------------------------------------------------------
EXTRA_FAQS = [
    ("What does a truck dispatcher do?",
     "A truck dispatcher searches load boards and broker networks for freight that fits your truck, negotiates the rate with the broker, confirms the load with you, handles broker setup paperwork and keeps rate confirmations and dispatch details organized, so you can spend your time driving."),
    ("Is Texas Solutions a freight broker?",
     "No. Texas Solutions is a truck dispatch service that works for the carrier. We are not a motor carrier or a freight broker. Loads are booked under your own authority, and you approve every load before it is booked."),
    ("Which states do you dispatch in?",
     "Texas Solutions supports owner-operators and small fleets throughout the United States. Tell us your home base, preferred lanes and home-time needs and we search freight that fits them."),
    ("Can I choose my own lanes and home time?",
     "Yes. You tell us your preferred lanes, destination markets and home-time schedule, and we search around them. You decide which loads, lanes and rates work for your business."),
    ("How do I start working with a truck dispatcher?",
     "Apply online or call (838) 910-3147. We review your authority, equipment and lanes, explain the dispatch agreement, collect your carrier documents, and then start searching loads for your truck."),
]

# --------------------------------------------------------------------------
# New landing pages
# --------------------------------------------------------------------------
LANDING = [
    {
        "file": "box-truck-dispatch.html",
        "nav": "Box Truck Dispatch",
        "title": "Box Truck Dispatch Service | Box & Straight Truck Loads | Texas Solutions",
        "description": "Box truck dispatch service for owner-operators and small fleets running box trucks and straight trucks. Load search, rate negotiation, broker setup and paperwork. No upfront cost.",
        "keywords": "box truck dispatch, box truck dispatch service, box truck dispatcher, straight truck dispatch, 26 ft box truck loads, box truck dispatching company",
        "eyebrow": "Box truck and straight truck dispatch",
        "h1": ["BOX TRUCK", "DISPATCH SERVICE"],
        "lede": "Dispatch for box trucks and straight trucks: we search freight that fits your truck, talk to the brokers, and keep the paperwork moving while you drive.",
        "answer_q": "What is a box truck dispatch service?",
        "answer": "A box truck dispatch service finds and negotiates loads for box trucks and straight trucks, communicates with brokers, handles setup paperwork and keeps rate confirmations organized. Texas Solutions dispatches box trucks for owner-operators and small fleets across the United States, with no upfront cost, a percentage-based fee set in your agreement, and your approval on every load.",
        "intro": [
            "Box truck freight moves differently from semi freight. Loads are smaller and often shorter, which means more calls, more broker setups and more paperwork for every dollar your truck earns. A dispatcher who knows the box truck side of the boards saves hours every day.",
            "We search load boards and broker contacts for freight that fits your truck's dimensions, liftgate and weight limits, compare the opportunities against your lanes, and negotiate before anything is booked.",
        ],
        "handles": [
            ("Load search for box trucks", "Freight matched to your box length, liftgate and payload limits."),
            ("Rate negotiation", "We negotiate with brokers before you see the load."),
            ("Broker setups", "Carrier packets, W-9 and certificate of insurance handled."),
            ("Paperwork support", "Rate confirmations and dispatch details kept organized."),
        ],
        "faqs": [
            ("Do you dispatch non-CDL box trucks?", "Yes. We dispatch box trucks and straight trucks run under your own authority. Tell us your truck's size and weight rating and we search freight that fits it."),
            ("Does a box truck need its own MC authority to use a dispatcher?", "Yes. A dispatcher books freight under your operating authority, so you need your own MC and DOT numbers and insurance. We handle broker setups using your documents."),
            ("How are box truck dispatch fees charged?", "Our fee is percentage-based under your signed dispatch agreement, with no setup fee and no monthly subscription. The percentage is explained before paid service begins."),
        ],
    },
    {
        "file": "hotshot-dispatch.html",
        "nav": "Hotshot Dispatch",
        "title": "Hotshot Dispatch Service | Hotshot Trucking Load Dispatch | Texas Solutions",
        "description": "Hotshot dispatch service for hotshot owner-operators: load search, rate negotiation and broker communication for gooseneck and flatbed hotshot rigs. No upfront cost, no long-term contract.",
        "keywords": "hotshot dispatch, hotshot dispatch service, hotshot dispatcher, hotshot trucking dispatch, hotshot loads, gooseneck dispatch",
        "eyebrow": "Hotshot trucking dispatch",
        "h1": ["HOTSHOT", "DISPATCH SERVICE"],
        "lede": "Dispatch for hotshot owner-operators: time-sensitive freight searched, negotiated and confirmed with you before it is booked.",
        "answer_q": "What does a hotshot dispatch service do?",
        "answer": "A hotshot dispatch service finds and negotiates time-sensitive, partial and expedited loads for hotshot rigs, communicates with brokers and handles setup paperwork. Texas Solutions dispatches hotshot trucks for owner-operators across the United States, including Texas and Permian Basin lanes, with no upfront cost and your approval on every load.",
        "intro": [
            "Hotshot freight is fast-moving and often time-critical: equipment, machinery, construction and oilfield materials that cannot wait for a full truckload. Winning those loads means watching the boards closely and answering brokers quickly.",
            "From our base in Midland, Texas, we know how much hotshot freight moves through Texas and the Permian Basin. We search it for you, negotiate the rate and keep your deadhead in mind.",
        ],
        "handles": [
            ("Time-sensitive load search", "Expedited and partial loads matched to your trailer and payload."),
            ("Rate negotiation", "Professional negotiation on every opportunity."),
            ("Deadhead planning", "Next loads reviewed with your position and home base in mind."),
            ("Broker communication", "Calls, confirmations and setup paperwork handled."),
        ],
        "faqs": [
            ("What kind of freight do hotshot trucks haul?", "Hotshot trucks typically haul smaller, time-sensitive loads such as equipment, machinery, construction materials and oilfield parts on gooseneck or flatbed trailers."),
            ("Do you dispatch hotshot trucks in the Permian Basin?", "Yes. Texas Solutions is based in Midland, Texas, and dispatches hotshot trucks on Texas and Permian Basin lanes as well as nationwide."),
            ("Will I have to take every hotshot load you find?", "No. You decide which loads, lanes and rates work for your business. Nothing is booked without your approval."),
        ],
    },
    {
        "file": "dry-van-dispatch.html",
        "nav": "Dry Van Dispatch",
        "title": "Dry Van Dispatch Service for Owner-Operators | Texas Solutions",
        "description": "Dry van dispatch service for owner-operators and small fleets. Load search, rate negotiation, lane and deadhead planning, broker setups and paperwork. No upfront cost.",
        "keywords": "dry van dispatch, dry van dispatch service, dry van dispatcher, dry van loads, 53 ft dry van dispatch",
        "eyebrow": "Dry van dispatch",
        "h1": ["DRY VAN", "DISPATCH SERVICE"],
        "lede": "Dry van dispatch that plans lanes, watches deadhead and negotiates every load, with you approving every booking.",
        "answer_q": "What is a dry van dispatch service?",
        "answer": "A dry van dispatch service searches and negotiates freight for 53-foot dry van trailers, plans lanes to reduce deadhead, communicates with brokers and handles paperwork. Texas Solutions dispatches dry vans for owner-operators and small fleets nationwide, with a percentage-based fee set in your agreement and no long-term contract.",
        "intro": [
            "Dry van is the most common trailer on the road, which means the most freight and the most competition for it. Good dry van dispatch is about lanes: booking the next load before this one delivers and avoiding markets that leave you stuck.",
        ],
        "handles": [
            ("Lane planning", "Loads reviewed against your preferred lanes and home time."),
            ("Deadhead control", "Next-load planning to reduce empty miles."),
            ("Rate negotiation", "Rates compared and negotiated before booking."),
            ("Paperwork support", "Broker packets and rate confirmations organized."),
        ],
        "faqs": [
            ("How do dispatchers reduce deadhead for dry vans?", "By planning the next load before the current one delivers and favouring destination markets with strong outbound freight, so the truck spends fewer miles empty."),
            ("Can you dispatch a small dry van fleet?", "Yes. We dispatch single trucks and small fleets, and review each truck's lanes and driver preferences separately."),
        ],
    },
    {
        "file": "reefer-dispatch.html",
        "nav": "Reefer Dispatch",
        "title": "Reefer Dispatch Service | Refrigerated Truck Dispatch | Texas Solutions",
        "description": "Reefer dispatch service for refrigerated trucks: temperature-controlled load search, rate negotiation, broker communication and paperwork for owner-operators and small fleets.",
        "keywords": "reefer dispatch, reefer dispatch service, refrigerated truck dispatch, reefer loads, reefer dispatcher",
        "eyebrow": "Reefer dispatch",
        "h1": ["REEFER", "DISPATCH SERVICE"],
        "lede": "Temperature-controlled freight searched and negotiated for your reefer, with appointment times and paperwork kept straight.",
        "answer_q": "What does a reefer dispatch service do?",
        "answer": "A reefer dispatch service finds and negotiates temperature-controlled loads for refrigerated trailers, confirms temperature and appointment requirements with brokers, and keeps rate confirmations organized. Texas Solutions dispatches reefers for owner-operators and small fleets nationwide, with no upfront cost and your approval on every load.",
        "intro": [
            "Reefer freight pays for precision: set temperatures, tight pickup and delivery appointments, and shippers who expect them to be met. We confirm those details with the broker before a load reaches you, so there are no surprises at the dock.",
        ],
        "handles": [
            ("Temperature-controlled loads", "Produce, food and other refrigerated freight matched to your unit."),
            ("Appointment coordination", "Pickup and delivery times confirmed with brokers."),
            ("Rate negotiation", "Negotiated before you commit."),
            ("Paperwork support", "Rate confirmations with temperature requirements kept on file."),
        ],
        "faqs": [
            ("Do reefer loads pay more than dry van?", "Reefer loads often pay more per mile than dry van because of the equipment and the handling they require, but rates vary by market and season, and no dispatcher can guarantee them."),
            ("Do you check temperature requirements before booking?", "Yes. We confirm the required temperature, appointment times and any special handling with the broker before presenting the load to you."),
        ],
    },
    {
        "file": "flatbed-dispatch.html",
        "nav": "Flatbed & Step Deck Dispatch",
        "title": "Flatbed & Step Deck Dispatch Service | Texas Solutions",
        "description": "Flatbed and step deck dispatch for owner-operators and small fleets: open-deck load search, rate negotiation, broker communication and paperwork. No upfront cost, no long-term contract.",
        "keywords": "flatbed dispatch, flatbed dispatch service, step deck dispatch, flatbed dispatcher, open deck dispatch, flatbed loads",
        "eyebrow": "Flatbed and step deck dispatch",
        "h1": ["FLATBED & STEP DECK", "DISPATCH SERVICE"],
        "lede": "Open-deck freight searched, sized up and negotiated for your flatbed or step deck, with load details confirmed before you commit.",
        "answer_q": "What is a flatbed dispatch service?",
        "answer": "A flatbed dispatch service finds and negotiates open-deck loads for flatbed and step deck trailers, confirms dimensions, weights and tarping requirements with brokers, and handles setup paperwork. Texas Solutions dispatches flatbeds and step decks nationwide for owner-operators and small fleets, with no upfront cost and your approval on every load.",
        "intro": [
            "Open-deck freight comes with more questions than a sealed van: dimensions, weight, tarps, straps and chains, and whether a step deck is needed for height. We ask those questions before the load reaches you.",
            "Texas and the Permian Basin move a large share of the country's open-deck freight, including building materials, steel, machinery and oilfield equipment, and we know those lanes from our Midland base.",
        ],
        "handles": [
            ("Open-deck load search", "Flatbed and step deck freight matched to your trailer."),
            ("Load detail checks", "Dimensions, weight and tarping confirmed with the broker."),
            ("Rate negotiation", "Negotiated with tarping and handling in mind."),
            ("Paperwork support", "Broker setups and rate confirmations organized."),
        ],
        "faqs": [
            ("What is the difference between flatbed and step deck freight?", "A step deck has a lower rear deck, which allows taller freight to stay within legal height limits. Loads that are too tall for a standard flatbed often move on a step deck."),
            ("Do you confirm tarping requirements?", "Yes. We confirm whether a load needs tarps and what securement is expected before we present it to you."),
        ],
    },
    {
        "file": "power-only-dispatch.html",
        "nav": "Power Only Dispatch",
        "title": "Power Only Dispatch Service | Texas Solutions",
        "description": "Power only dispatch for owner-operators with a tractor and no trailer: load search, rate negotiation and broker communication for power only freight. No upfront cost.",
        "keywords": "power only dispatch, power only dispatch service, power only loads, power only trucking dispatch",
        "eyebrow": "Power only dispatch",
        "h1": ["POWER ONLY", "DISPATCH SERVICE"],
        "lede": "Dispatch for tractors running power only: we find preloaded trailers and drop-and-hook freight and negotiate the rate for you.",
        "answer_q": "What is power only dispatch?",
        "answer": "Power only dispatch finds loads for a tractor without its own trailer, where the carrier hauls a trailer supplied by the shipper or broker. Texas Solutions searches and negotiates power only freight for owner-operators nationwide, handles broker communication and paperwork, and books nothing without your approval.",
        "intro": [
            "Power only lets a tractor earn without the cost of owning a trailer: you hook to a preloaded trailer, deliver it and drop it. The work is finding enough of those loads in the right places, which is exactly what a dispatcher does.",
        ],
        "handles": [
            ("Power only load search", "Preloaded and drop-and-hook freight found for your tractor."),
            ("Rate negotiation", "Rates negotiated before booking."),
            ("Broker communication", "Trailer pickup and drop details confirmed."),
            ("Paperwork support", "Rate confirmations and dispatch details organized."),
        ],
        "faqs": [
            ("Do I need a trailer for power only loads?", "No. Power only freight uses a trailer supplied by the shipper, broker or carrier program. You provide the tractor and the authority."),
        ],
    },
    {
        "file": "owner-operator-dispatch.html",
        "nav": "Owner-Operator Dispatch",
        "title": "Dispatch Service for Owner-Operators & Small Fleets | Texas Solutions",
        "description": "Truck dispatch service built for owner-operators and small fleets: load search, rate negotiation, broker communication and paperwork, with no upfront cost, no forced loads and no long-term contract.",
        "keywords": "owner operator dispatch service, dispatch service for owner operators, small fleet dispatch, dispatcher for owner operators, independent truck dispatch",
        "eyebrow": "For owner-operators and small fleets",
        "h1": ["DISPATCH FOR", "OWNER-OPERATORS"],
        "lede": "You run the truck. We handle the calls, the boards, the negotiation and the paperwork, and you approve every load.",
        "answer_q": "What is an owner-operator dispatch service?",
        "answer": "An owner-operator dispatch service handles load search, rate negotiation, broker communication and paperwork for independent truck owners and small fleets, so the owner can spend more time driving. Texas Solutions provides this directly, with a percentage-based fee set in your agreement, no upfront or setup fee, no long-term contract and no forced loads.",
        "intro": [
            "Owner-operators lose hours every day to load boards and broker calls, usually after a full day of driving. A dispatcher takes that work on without taking control: you set the lanes, the home time and the minimum you will accept, and you approve every load.",
            "Small fleets get the same service per truck, with each truck's equipment, lanes and driver preferences handled separately.",
        ],
        "handles": [
            ("No upfront cost", "No setup fee and no monthly subscription."),
            ("Carrier control", "You approve every load, lane and rate."),
            ("Direct service", "Your application is never sold to lead buyers."),
            ("No long-term contract", "Notice terms are stated in your agreement."),
        ],
        "faqs": [
            ("Is a truck dispatcher worth it for an owner-operator?", "For many owner-operators, yes, when the dispatcher saves time, reduces deadhead and negotiates better loads by more than the fee. Results vary with market conditions and carrier performance, and no dispatcher can guarantee earnings."),
            ("Can a small fleet use one dispatch service for every truck?", "Yes. We dispatch single trucks and small fleets, tracking each truck's equipment, lanes and schedule separately."),
        ],
    },
    {
        "file": "texas-truck-dispatch.html",
        "nav": "Texas Truck Dispatch",
        "title": "Texas Truck Dispatch Service | Midland & Permian Basin | Texas Solutions",
        "description": "Truck dispatch service based in Midland, Texas, for owner-operators running Texas lanes: Permian Basin, Houston, Dallas-Fort Worth, San Antonio, Laredo and El Paso, plus nationwide freight.",
        "keywords": "truck dispatch Texas, truck dispatch service Texas, Midland TX truck dispatch, Permian Basin dispatch, Houston truck dispatch, Dallas truck dispatch, Texas hotshot dispatch",
        "eyebrow": "Based in Midland, Texas",
        "h1": ["TEXAS TRUCK", "DISPATCH SERVICE"],
        "lede": "A Texas dispatch team for carriers who run Texas: the Permian Basin, Houston, Dallas-Fort Worth, San Antonio, Laredo and El Paso, and everywhere those loads lead.",
        "answer_q": "Is there a truck dispatch service based in Texas?",
        "answer": "Yes. Texas Solutions is a truck dispatch service based at 401 W Kentucky Ave, Midland, Texas. It dispatches owner-operators and small fleets on Texas lanes, including the Permian Basin, Houston, Dallas-Fort Worth, San Antonio, Laredo and El Paso, as well as nationwide, with no upfront cost and your approval on every load.",
        "intro": [
            "Texas is one of the largest freight markets in the country, with energy, manufacturing, cross-border and port freight moving through it every day. A dispatcher who knows Texas lanes helps you get into and out of the state without long empty runs.",
            "Our team is based in Midland, in the heart of the Permian Basin, and works with carriers running flatbed, hotshot, dry van, reefer and box trucks across Texas and beyond.",
        ],
        "handles": [
            ("Permian Basin freight", "Oilfield, equipment and materials loads around Midland and Odessa."),
            ("Houston and the Gulf Coast", "Port, petrochemical and distribution freight."),
            ("Dallas-Fort Worth", "Distribution and manufacturing lanes."),
            ("Laredo and El Paso", "Cross-border and southwest corridor freight."),
        ],
        "faqs": [
            ("Where is Texas Solutions located?", "Texas Solutions is located at 401 W Kentucky Ave, Midland, Texas, and supports carriers throughout the United States."),
            ("Do you only dispatch Texas loads?", "No. We dispatch nationwide. Texas lanes are a strength because of our location, but we search wherever your lanes and home time point."),
        ],
    },
    {
        "file": "what-does-a-truck-dispatcher-do.html",
        "nav": "What a Truck Dispatcher Does",
        "title": "What Does a Truck Dispatcher Do? Duties, Costs & How to Choose One | Texas Solutions",
        "description": "A plain-English guide to truck dispatchers: what they do, how dispatch fees usually work, dispatcher vs freight broker, and how owner-operators should choose a dispatch service.",
        "keywords": "what does a truck dispatcher do, how much does a truck dispatcher cost, truck dispatcher fees, dispatcher vs broker, how to choose a truck dispatch service",
        "eyebrow": "Guide",
        "h1": ["WHAT DOES A TRUCK", "DISPATCHER DO?"],
        "lede": "A plain-English guide for owner-operators: the job, the usual fee structures, the difference from a broker, and what to check before you sign.",
        "answer_q": "What does a truck dispatcher do?",
        "answer": "A truck dispatcher finds and books freight for a carrier's trucks. The dispatcher searches load boards and broker contacts, negotiates rates, confirms loads with the driver, completes broker setup paperwork and keeps rate confirmations organized. Independent dispatchers work for the carrier, usually for a percentage of each load's gross, and are different from freight brokers, who work between shippers and carriers.",
        "intro": [
            "Most owner-operators start by dispatching themselves. It works until the hours on the phone start competing with the hours behind the wheel. A dispatcher takes over the search, the negotiation and the paperwork so the driver can drive.",
        ],
        "sections": [
            ("The daily duties of a truck dispatcher", [
                "Searching load boards and broker networks for freight that fits the truck, equipment and lanes.",
                "Negotiating rates with brokers before presenting a load to the driver.",
                "Planning the next load to reduce deadhead miles.",
                "Completing broker setup packets with the carrier's MC authority, W-9 and insurance certificate.",
                "Keeping rate confirmations and dispatch details organized.",
                "Staying in contact with brokers about pickup, delivery and any changes.",
            ]),
            ("How much does a truck dispatcher cost?", [
                "Across the industry, independent dispatch services commonly charge a percentage of each load's gross, often somewhere between about 5% and 10%, while some charge a flat weekly fee.",
                "Texas Solutions charges a percentage set in your signed dispatch agreement, explained before paid service begins, with no setup fee and no monthly subscription.",
                "When comparing services, ask what the percentage applies to and what is included, such as broker setups and paperwork support.",
            ]),
            ("Truck dispatcher vs freight broker", [
                "A dispatcher works for the carrier and books freight under the carrier's own authority.",
                "A freight broker works between the shipper and the carrier and needs its own broker authority.",
                "Texas Solutions is a dispatch service. It is not a motor carrier or a freight broker.",
            ]),
            ("How to choose a truck dispatch service", [
                "Check that you approve every load and are never forced to take freight.",
                "Ask how the fee is charged and whether there are setup or monthly fees.",
                "Look for no long-term contract and a clear notice period.",
                "Make sure your application is not sold to lead buyers.",
                "Be wary of anyone who guarantees rates or earnings; markets move and no dispatcher can promise them.",
            ]),
        ],
        "faqs": [
            ("Do I need a dispatcher if I use load boards myself?", "Not necessarily. Many owner-operators dispatch themselves. A dispatcher makes sense when the time spent searching and negotiating starts to cost more than the fee."),
            ("Can a dispatcher guarantee my weekly gross?", "No. Freight volume, rates and market conditions change, and a reputable dispatch service will not guarantee loads, rates, revenue or earnings."),
        ],
    },
]
