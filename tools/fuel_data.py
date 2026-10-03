"""
The one place that decides which fuel price a page shows and how it is
labelled. js/site.js mirrors resolve() and status() for the browser, so the
calculator and the static pages always agree.

A record is:
    {geo, name, fuel, price, level, cadence, source, sourceUrl, observed,
     fetched, status, fallback}
level is "state", "regional" or "national"; status is "fresh", "stale" or
"unavailable"; fallback is True when a state has no daily value and the EIA
weekly regional average is shown instead.
"""

import json
from datetime import date
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "data" / "fuel-prices.json"
# Older than this many days (after the observation date) means stale.
MAX_AGE = {"daily": 2, "weekly": 9}


def load():
    return json.loads(FILE.read_text(encoding="utf-8")) if FILE.exists() else None


def status(observed, cadence, today=None):
    if not observed:
        return "unavailable"
    age = ((today or date.today()) - date.fromisoformat(observed)).days
    return "fresh" if age <= MAX_AGE[cadence] else "stale"


def _rec(data, fuel, geo, name, level, raw, src, fallback=False, today=None):
    if not raw or raw.get("price") is None:
        return {"geo": geo, "name": name, "fuel": fuel, "price": None, "level": level, "status": "unavailable",
                "fallback": fallback, "source": src["name"], "sourceUrl": src["url"], "cadence": src["cadence"],
                "observed": None, "fetched": None}
    return {"geo": geo, "name": name, "fuel": fuel, "price": raw["price"], "level": level,
            "cadence": src["cadence"], "source": src["name"], "sourceUrl": src["url"],
            "observed": raw.get("observed"), "fetched": raw.get("fetched"), "fallback": fallback,
            "status": status(raw.get("observed"), src["cadence"], today)}


def national(data, fuel="diesel", today=None):
    f = (data or {}).get("fuels", {}).get(fuel, {})
    return _rec(data, fuel, "US", "U.S. average", "national", f.get("regions", {}).get("US"),
                f.get("sources", {}).get("region", {"name": "EIA", "url": "", "cadence": "weekly"}), today=today)


def resolve(data, code, fuel="diesel", today=None):
    """Best record for a state: its daily value (even if stale, labelled so), else the weekly regional fallback."""
    name, region = C.STATE_REGION[code]
    f = (data or {}).get("fuels", {}).get(fuel, {})
    srcs = f.get("sources", {})
    st = f.get("states", {}).get(code)
    if st:
        return _rec(data, fuel, code, name, "state", st, srcs["state"], today=today)
    reg = f.get("regions", {}).get(region)
    if reg:
        r = _rec(data, fuel, code, name, "regional", reg, srcs["region"], fallback=True, today=today)
        r["regionName"] = reg.get("name", region)
        return r
    return _rec(data, fuel, code, name, "state", None, srcs.get("state", {"name": "AAA", "url": "", "cadence": "daily"}), today=today)


def human(d):
    if not d:
        return ""
    x = date.fromisoformat(d)
    return f"{x.strftime('%B')} {x.day}, {x.year}"


def label(r):
    """One line of provenance, e.g. 'AAA daily state average, October 3, 2026'."""
    if r["status"] == "unavailable":
        return "No current price available; enter your pump price"
    what = r["source"] + (f" for the {r.get('regionName', '')} region (no daily {r['name']} value)" if r["fallback"] else "")
    when = ("week of " if r["cadence"] == "weekly" else "") + human(r["observed"])
    return f"{what}, {when}" + (" (stale: the source has not updated since)" if r["status"] == "stale" else "")
