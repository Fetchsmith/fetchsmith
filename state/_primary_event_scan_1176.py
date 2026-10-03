#!/usr/bin/env python3
"""Cycle 1176 fleet scan for the `isPrimaryEvent` trap found on
westerly_breaker/ted-tender-monitor.

Signature: a named rival's in-effect pricing record flags a GENERIC platform-default
event (apify-default-dataset-item / apify-actor-start / "result") as primary at a token
price, while a DIFFERENT non-one-time event on the same record is materially dearer.
check-price-superiority collapses each rival to the isPrimaryEvent price, so such a
rival is scored as dirt-cheap when its own README may document the dearer event as the
real charge. A flag means "go read that rival's own pricing table", not "false claim".

Read-only GET /v2/acts/<owner>~<slug>.
"""
import datetime, glob, json, os, re, urllib.error, urllib.request

TOKEN = os.environ["APIFY_TOKEN"]
NOW = datetime.datetime.now(datetime.timezone.utc)
GENERIC = {"apify-default-dataset-item", "apify-actor-start"}
RATIO = 3.0

SKIP_PREFIX = ("bin/", "cpvCodes/", "field/", "src/", "state/", "actors/", "notes/", "logs/")


def our_handles():
    hs = {}
    for p in sorted(glob.glob("/root/agent/actors/*/README.md")):
        slug = p.split("/")[-2]
        txt = open(p).read()
        for h in set(re.findall(r"`([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)`", txt)):
            if h.startswith(SKIP_PREFIX) or "." in h.split("/")[0]:
                continue
            hs.setdefault(h, []).append(slug)
    return hs


def effective(infos):
    best = None
    for p in infos or []:
        s = p.get("startedAt")
        if not s:
            continue
        try:
            t = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            continue
        if t <= NOW and (best is None or t > best[0]):
            best = (t, p)
    return best[1] if best else None


def price_of(d):
    """Headline numeric price of one charge-event dict (flat or cheapest tier)."""
    if d.get("eventPriceUsd") is not None:
        return float(d["eventPriceUsd"])
    tiers = d.get("eventTieredPricingUsd") or {}
    vals = [v.get("tieredEventPriceUsd") for v in tiers.values()
            if v.get("tieredEventPriceUsd") is not None]
    return float(min(vals)) if vals else None


def main():
    hs = our_handles()
    print(f"scanning {len(hs)} distinct named rivals across the fleet\n")
    flagged = checked = 0
    for h in sorted(hs):
        owner, slug = h.split("/", 1)
        try:
            with urllib.request.urlopen(
                f"https://api.apify.com/v2/acts/{owner}~{slug}?token={TOKEN}", timeout=30
            ) as r:
                d = json.load(r)["data"]
        except Exception:
            continue
        p = effective(d.get("pricingInfos"))
        if not p or p.get("pricingModel") != "PAY_PER_EVENT":
            continue
        evs = p.get("pricingPerEvent", {}).get("actorChargeEvents", {}) or {}
        if len(evs) < 2:
            continue
        checked += 1
        primary = [k for k, v in evs.items() if v.get("isPrimaryEvent")]
        # headline event the price checks would pick: primary, else cheapest non-one-time
        if primary:
            head = primary[0]
        else:
            cands = [(price_of(v), k) for k, v in evs.items()
                     if not v.get("isOneTimeEvent") and price_of(v) is not None]
            if not cands:
                continue
            head = min(cands)[1]
        hp = price_of(evs[head])
        if hp is None:
            continue
        # any materially dearer per-row (non-one-time) event on the same record?
        worse = [(k, price_of(v)) for k, v in evs.items()
                 if k != head and not v.get("isOneTimeEvent")
                 and price_of(v) is not None and hp > 0 and price_of(v) / hp >= RATIO]
        if worse and head in GENERIC:
            flagged += 1
            print(f"FLAG {h}  (named in: {', '.join(hs[h])})")
            print(f"     headline event picked = {head} @ ${hp}  <- generic platform default")
            for k, v in sorted(worse, key=lambda x: -x[1]):
                print(f"     dearer live non-one-time event: {k} @ ${v}  ({v/hp:.0f}x)")
    print(f"\nscan: {checked} multi-event rivals checked, {flagged} flagged "
          f"(generic primary + a >={RATIO:g}x dearer live per-row event)")


main()
