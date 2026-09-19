"""
Fetches diesel prices and writes data/diesel-prices.json:
- daily state averages from AAA (gasprices.aaa.com), and
- weekly regional averages from the U.S. Energy Information Administration
  (EIA, public domain), used as a fallback when a state price is missing.

    python tools/fuel_prices.py

The GitHub Action in .github/workflows/fuel-prices.yml runs this every
morning and commits the result when prices change. If a source fails, the
last good prices are kept.
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
AAA_SOURCE = "https://gasprices.aaa.com/state-gas-price-averages/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"
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


def fetch(url=SOURCE):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def parse_aaa(page):
    """State name -> diesel price, plus the 'Price as of' date."""
    sys.path.insert(0, str(Path(__file__).parent))
    import content as C
    by_name = {n: code for code, (n, _) in C.STATE_REGION.items()}
    by_name["Washington DC"] = by_name["District of Columbia"] = "DC"
    i = page.find("<table")
    table = page[i:page.find("</table>", i)]
    states = {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        if len(cells) >= 5 and cells[0] in by_name:
            m = re.search(r"[\d.]+", cells[4])
            if m:
                states[by_name[cells[0]]] = round(float(m.group(0)), 3)
    m = re.search(r"Price as of\s*(\d{1,2}/\d{1,2}/\d{2,4})", page)
    day = None
    if m:
        fmt = "%m/%d/%y" if len(m.group(1).split("/")[-1]) == 2 else "%m/%d/%Y"
        day = datetime.strptime(m.group(1), fmt).date().isoformat()
    return day, states


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
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    try:
        week, prices = parse(fetch())
    except Exception as e:  # keep last good EIA data
        print("EIA fetch failed:", e, file=sys.stderr)
        week, prices = old.get("week"), old.get("regions", {})
    if "US" not in prices or len(prices) < 8:
        print("EIA data unavailable; keeping the previous regional prices.", file=sys.stderr)
        week, prices = old.get("week"), old.get("regions", {})
    try:
        day, states = parse_aaa(fetch(AAA_SOURCE))
    except Exception as e:
        print("AAA fetch failed:", e, file=sys.stderr)
        day, states = None, {}
    if len(states) < 45:  # page changed or blocked: keep the last good daily prices
        print(f"AAA returned {len(states)} states; keeping previous daily prices.", file=sys.stderr)
        day, states = old.get("day"), old.get("states", {})
    if not prices and not states:
        sys.exit(1)
    if old.get("week") == week and old.get("regions") == prices and old.get("day") == day and old.get("states") == states:
        print(f"diesel prices unchanged (day {day}, week {week})")
        return
    data = {
        "day": day,
        "states": states,
        "statesSource": "AAA daily state averages (gasprices.aaa.com)",
        "statesSourceUrl": AAA_SOURCE,
        "week": week,
        "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "U.S. Energy Information Administration, weekly retail on-highway diesel prices",
        "sourceUrl": SOURCE,
        "unit": "USD per gallon, including taxes",
        "regions": prices,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"diesel: {len(states)} states for {day}; EIA week {week} US ${prices.get('US', {}).get('price')}")


if __name__ == "__main__":
    main()
