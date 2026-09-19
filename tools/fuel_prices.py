"""
Fetches the latest weekly on-highway diesel prices from the U.S. Energy
Information Administration (EIA, public domain) and writes data/diesel-prices.json.

    python tools/fuel_prices.py

EIA publishes diesel by PADD region (plus California) every Monday; the
GitHub Action in .github/workflows/fuel-prices.yml runs this weekly and
commits the result, so the fuel calculator always shows the current week.
"""

import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epd2d_pte_dpgal_w.htm"
OUT = ROOT / "data" / "diesel-prices.json"

# EIA row label -> short key
REGIONS = {
    "U.S.": "US",
    "East Coast (PADD1)": "P1",
    "New England (PADD 1A)": "P1A",
    "Central Atlantic (PADD 1B)": "P1B",
    "Lower Atlantic (PADD 1C)": "P1C",
    "Midwest (PADD 2)": "P2",
    "Gulf Coast (PADD 3)": "P3",
    "Rocky Mountain (PADD 4)": "P4",
    "West Coast (PADD 5)": "P5",
    "West Coast less California": "P5X",
    "California": "CA",
}
NAMES = {
    "US": "U.S. average", "P1": "East Coast", "P1A": "New England", "P1B": "Central Atlantic",
    "P1C": "Lower Atlantic", "P2": "Midwest", "P3": "Gulf Coast", "P4": "Rocky Mountain",
    "P5": "West Coast", "P5X": "West Coast (excl. California)", "CA": "California",
}


def fetch():
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 (fuel price updater; dispatch.texassolutions.co)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def parse(page):
    page = re.sub(r"<script.*?</script>", "", page, flags=re.S)
    # Column dates, e.g. 09/15/26
    dates = re.findall(r"\b(\d{2}/\d{2}/\d{2})\b", page)
    text = html.unescape(re.sub(r"<[^>]+>", "|", page))
    text = re.sub(r"\s+", " ", re.sub(r"\|\s*(\|\s*)+", "|", text))
    prices = {}
    for label, key in REGIONS.items():
        m = re.search(r"\|\s*" + re.escape(label) + r"\s*\|((?:\s*[\d.]+\s*\|){1,8})", text)
        if not m:
            continue
        nums = [float(x) for x in re.findall(r"[\d.]+", m.group(1)) if x.count(".") == 1]
        if nums:
            prices[key] = {"name": NAMES[key], "price": round(nums[-1], 3),
                           "prev": round(nums[-2], 3) if len(nums) > 1 else None}
    week = dates[-1] if dates else None
    if week:
        week = datetime.strptime(week, "%m/%d/%y").date().isoformat()
    return week, prices


def main():
    week, prices = parse(fetch())
    if "US" not in prices or len(prices) < 8:
        print("EIA page format changed; keeping the previous file.", file=sys.stderr)
        sys.exit(0 if OUT.exists() else 1)
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        if old.get("week") == week and old.get("regions") == prices:
            print(f"diesel prices unchanged (week {week})")
            return
    data = {
        "week": week,
        "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "U.S. Energy Information Administration, weekly retail on-highway diesel prices",
        "sourceUrl": SOURCE,
        "unit": "USD per gallon, including taxes",
        "regions": prices,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"diesel prices for week {week}: US ${prices['US']['price']}")


if __name__ == "__main__":
    main()
