#!/root/agent/venv/bin/python
"""Cycle 1348: live-price the FULL unnamed tail (incl. the 1-2-user floor) of
eu-ted-tenders-scraper's niche -- the sweep cycle 1305 deferred for time.

Unlike the earlier bin/_batch_price_*.py scripts, this one decides WHICH event is
the comparable per-row charge *in code* instead of printing every event and leaving
the judgment to whoever reads the output. That judgment is the recurring trap in
LEARNINGS (cycle 1336, bit again at 1347 with 8 false positives): a one-time
apify-actor-start fee or a vestigial secondary apify-default-dataset-item event gets
read as the rival's real price. Rules here:

  * one-time events are NEVER the unit price (we bill per row, not per run) -- they
    are reported separately as start_fee.
  * among non-one-time events, prefer isPrimaryEvent; if none is flagged and there is
    exactly one candidate, use it; if none is flagged and several exist, mark the
    listing AMBIGUOUS rather than guessing (cycle 1177's check-primary-event showed a
    flagged primary can itself be the wrong number, so a guess is not safe).
  * every tier is kept (eventTieredPricingUsd), not just the FREE-tier headline --
    a tiered rival's FREE price is not its real price (cycle 1220).
"""
import datetime
import importlib.machinery
import importlib.util
import json
import os
import sys

import httpx

ROOT = "/root/agent"
_path = os.path.join(ROOT, "bin/check-price-superiority")
spec = importlib.util.spec_from_loader("cps", importlib.machinery.SourceFileLoader("cps", _path))
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)

H = {"Authorization": "Bearer " + cps.token()}
API = "https://api.apify.com/v2"
NOW = datetime.datetime.now(datetime.timezone.utc)

# our own live price, flat per result, re-verified live at the top of cycle 1348
OURS = 0.0015
TIERS = ("FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND")


def tiers_of(ev):
    """All tier prices for one charge event, FREE-tier price as the fallback."""
    t = ev.get("eventTieredPricingUsd") or ev.get("tieredEventPriceUsd")
    if isinstance(t, dict) and t:
        return {k: v for k, v in t.items() if isinstance(v, (int, float))}
    p = cps.price_of(ev)
    return {"FREE": p} if isinstance(p, (int, float)) else {}


def unit_price(events):
    """(unit_tiers, unit_key, start_fee, note) -- see module docstring for the rules."""
    onetime, recurring = {}, {}
    for k, v in events.items():
        (onetime if v.get("isOneTimeEvent") else recurring)[k] = v
    start_fee = max((min(tiers_of(v).values(), default=0.0) for v in onetime.values()),
                    default=0.0)
    if not recurring:
        return {}, None, start_fee, "no recurring event -- one-time/start-fee only"
    primary = [k for k, v in recurring.items() if v.get("isPrimaryEvent")]
    if len(primary) == 1:
        k = primary[0]
        return tiers_of(recurring[k]), k, start_fee, "primary event"
    if len(recurring) == 1:
        k = next(iter(recurring))
        return tiers_of(recurring[k]), k, start_fee, "sole recurring event (no primary flag)"
    if primary:
        k = min(primary, key=lambda k: min(tiers_of(recurring[k]).values(), default=9e9))
        return tiers_of(recurring[k]), k, start_fee, f"AMBIGUOUS: {len(primary)} primaries"
    return {}, None, start_fee, f"AMBIGUOUS: {len(recurring)} recurring, no primary flag"


handles = [l.strip() for l in open("/tmp/ted_unnamed_handles.txt") if l.strip()]
out = []
for i, h in enumerate(handles, 1):
    u, n = h.split("/", 1)
    try:
        r = httpx.get(f"{API}/acts/{u}~{n}", headers=H, timeout=30)
        d = r.json().get("data") if r.status_code == 200 else None
    except Exception as e:
        d = None
        print(f"ERR {h}: {e}", file=sys.stderr)
    if not d:
        out.append({"handle": h, "error": "unresolvable"})
        continue
    cur = cps.effective(d.get("pricingInfos"), NOW) or {}
    events = (cur.get("pricingPerEvent", {}) or {}).get("actorChargeEvents", {}) or {}
    model = cur.get("pricingModel")
    ut, uk, fee, note = unit_price(events)
    # a rival with no pricing record at all, or on Apify's FREE model, bills $0 (cycle 1104)
    if not d.get("pricingInfos") or model == "FREE":
        ut, uk, note = {"FREE": 0.0}, None, "FREE model / no pricing record -- $0"
    # scheduled future entries are invisible to every tool that filters startedAt<=now
    future = [{"startedAt": p.get("startedAt"), "model": p.get("pricingModel")}
              for p in (d.get("pricingInfos") or [])
              if p.get("startedAt") and p["startedAt"] > NOW.isoformat()]
    undercuts = sorted(t for t, v in ut.items() if v < OURS)
    out.append({
        "handle": h,
        "title": d.get("title"),
        "users": (d.get("stats") or {}).get("totalUsers"),
        "model": model,
        "unit_event": uk,
        "unit_tiers": ut,
        "start_fee": fee,
        "note": note,
        "undercuts_tiers": undercuts,
        "every_tier": bool(ut) and all(v < OURS for v in ut.values()),
        "future_pricing": future,
        "events": {k: {"tiers": tiers_of(v), "primary": v.get("isPrimaryEvent"),
                       "onetime": v.get("isOneTimeEvent"), "title": v.get("eventTitle")}
                   for k, v in events.items()},
        "desc": (d.get("description") or "")[:500],
    })
    if i % 20 == 0:
        print(f"  ...{i}/{len(handles)}", file=sys.stderr)

json.dump(out, open("/tmp/ted_prices.json", "w"), indent=1)
amb = [o for o in out if "AMBIGUOUS" in (o.get("note") or "")]
print(f"priced {len(out)} listings -> /tmp/ted_prices.json ({len(amb)} ambiguous, need hand-reading)")
