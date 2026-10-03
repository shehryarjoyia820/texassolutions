"""
Fetches fuel prices and writes data/fuel-prices.json, the one fuel-data file
used by the fuel calculator, the fuel surcharge calculator and the 51 state
diesel pages:

- daily state averages from AAA (gasprices.aaa.com): diesel and regular
  gasoline, and
- weekly regional and U.S. averages from the U.S. Energy Information
  Administration (EIA, public domain): on-highway diesel and regular
  gasoline. A weekly regional value is only used for a state that has no
  daily value, and is always labelled as a weekly regional fallback.

    python tools/fuel_prices.py

Every record keeps its own observation date ("observed") and the time it was
fetched ("fetched"). When a source fails, or returns too few rows, the last
good records are kept with their original dates, so pages show them as stale
instead of presenting old prices as today's. Nothing is ever invented: a
missing value stays missing and the calculators ask for a manual price.

The GitHub Action in .github/workflows/fuel-prices.yml runs this twice a day
and commits the result when prices change. See tools/fuel_data.py for how a
record is chosen and how fresh/stale/unavailable is decided.
"""

import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "fuel-prices.json"
LEGACY = ROOT / "data" / "diesel-prices.json"  # pre-October 2026 format, migrated once
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"
AAA_SOURCE = "https://gasprices.aaa.com/state-gas-price-averages/"

# fuel -> (AAA table column, EIA weekly page)
FUELS = {
    "diesel": (4, "https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epd2d_pte_dpgal_w.htm"),
    "gasoline": (1, "https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epmr_pte_dpgal_w.htm"),
}
SOURCES = {
    "diesel": {
        "state": {"name": "AAA daily state average", "url": AAA_SOURCE, "cadence": "daily"},
        "region": {"name": "U.S. Energy Information Administration (EIA) weekly on-highway diesel price",
                   "url": "https://www.eia.gov/petroleum/gasdiesel/", "cadence": "weekly"},
    },
    "gasoline": {
        "state": {"name": "AAA daily state average (regular)", "url": AAA_SOURCE, "cadence": "daily"},
        "region": {"name": "U.S. Energy Information Administration (EIA) weekly regular gasoline price",
                   "url": "https://www.eia.gov/petroleum/gasdiesel/", "cadence": "weekly"},
    },
}

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


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def parse_aaa(page):
    """{fuel: {state code: price}} plus the 'Price as of' date."""
    sys.path.insert(0, str(Path(__file__).parent))
    import content as C
    by_name = {n: code for code, (n, _) in C.STATE_REGION.items()}
    by_name["Washington DC"] = by_name["District of Columbia"] = "DC"
    i = page.find("<table")
    table = page[i:page.find("</table>", i)]
    out = {fuel: {} for fuel in FUELS}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        if len(cells) >= 5 and cells[0] in by_name:
            for fuel, (col, _) in FUELS.items():
                m = re.search(r"[\d.]+", cells[col])
                if m:
                    out[fuel][by_name[cells[0]]] = round(float(m.group(0)), 3)
    m = re.search(r"Price as of\s*(\d{1,2}/\d{1,2}/\d{2,4})", page)
    day = None
    if m:
        fmt = "%m/%d/%y" if len(m.group(1).split("/")[-1]) == 2 else "%m/%d/%Y"
        day = datetime.strptime(m.group(1), fmt).date().isoformat()
    return day, out


def parse_eia(page):
    """EIA weekly table -> (week date, {region key: {name, price, prev}})."""
    page = re.sub(r"<script.*?</script>", "", page, flags=re.S)
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
    week = datetime.strptime(dates[-1], "%m/%d/%y").date().isoformat() if dates else None
    return week, prices


def empty():
    return {"schema": 1, "unit": "USD per gallon, including taxes",
            "fuels": {f: {"sources": SOURCES[f], "states": {}, "regions": {}} for f in FUELS}}


def migrate_legacy():
    """Turn the old diesel-prices.json into the new record format (keeps real dates)."""
    data = empty()
    if not LEGACY.exists():
        return data
    old = json.loads(LEGACY.read_text(encoding="utf-8"))
    fetched = old.get("fetched")
    d = data["fuels"]["diesel"]
    for code, price in (old.get("states") or {}).items():
        d["states"][code] = {"price": price, "observed": old.get("day"), "fetched": fetched}
    for key, r in (old.get("regions") or {}).items():
        d["regions"][key] = dict(r, observed=old.get("week"), fetched=fetched)
    return data


def main():
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else migrate_legacy()
    data = json.loads(json.dumps(old))
    for f in FUELS:  # keep the source descriptions current
        data["fuels"].setdefault(f, {"states": {}, "regions": {}})["sources"] = SOURCES[f]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    problems = []

    # Weekly EIA regional and U.S. averages
    for fuel, (_, eia_url) in FUELS.items():
        try:
            week, prices = parse_eia(fetch(eia_url))
        except Exception as e:
            week, prices = None, {}
            problems.append(f"EIA {fuel} fetch failed: {e}")
        if "US" not in prices or len(prices) < 8 or not week:
            problems.append(f"EIA {fuel}: {len(prices)} regions; keeping previous records")
            continue
        regions = data["fuels"][fuel]["regions"]
        for key, r in prices.items():
            prev = regions.get(key)
            same = prev and prev.get("price") == r["price"] and prev.get("observed") == week
            regions[key] = prev if same else dict(r, observed=week, fetched=now)

    # Daily AAA state averages
    try:
        day, by_fuel = parse_aaa(fetch(AAA_SOURCE))
    except Exception as e:
        day, by_fuel = None, {}
        problems.append(f"AAA fetch failed: {e}")
    for fuel in FUELS:
        got = by_fuel.get(fuel, {})
        if len(got) < 45 or not day:  # page changed or blocked: keep the last good daily prices
            problems.append(f"AAA {fuel}: {len(got)} states; keeping previous records")
            continue
        states = data["fuels"][fuel]["states"]
        for code, price in got.items():
            prev = states.get(code)
            same = prev and prev.get("price") == price and prev.get("observed") == day
            states[code] = prev if same else {"price": price, "observed": day, "fetched": now}

    for p in problems:
        print(p, file=sys.stderr)
    if not any(data["fuels"][f]["states"] or data["fuels"][f]["regions"] for f in FUELS):
        sys.exit(1)
    if data == old and OUT.exists():
        print("fuel prices unchanged")
        return
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if LEGACY.exists():
        LEGACY.unlink()
    for fuel in FUELS:
        fd = data["fuels"][fuel]
        print(f"{fuel}: {len(fd['states'])} states, {len(fd['regions'])} regions, "
              f"U.S. ${fd['regions'].get('US', {}).get('price')}")


if __name__ == "__main__":
    main()
