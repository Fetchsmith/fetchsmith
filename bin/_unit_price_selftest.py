#!/root/agent/venv/bin/python
"""Replay every saved /tmp/*_prices*.json audit cohort through bin/_unit_price.py.

This is the verification 0-TODO-h1348-backport-unit-price-helper asked for ("re-price one
small past cohort and confirm the surviving undercutter set is unchanged"), run fleet-wide
instead of on one cohort -- and it doubles as a live-accuracy audit of the drift the
backport found (cycle 1396): 6 of the 8 divergent unit_price copies, plus every old-shape
cps.headline_price cohort before the cycle-1385 fix, classified start fees purely on
isOneTimeEvent. Any rival whose `apify-actor-start` was left unflagged therefore had its
START FEE reported as its per-row rate.

Two cohort schemas exist in /tmp and both are replayable, because both recorded the raw
per-event `primary`/`onetime` flags next to the price:

  TIERED  (the 8 bin/_batch_price_*.py scripts with their own unit_price, cycle 1348+):
          row has unit_event/unit_tiers; events[k] = {tiers: {tier: usd}, primary, onetime}
  FLAT    (the older cps.headline_price scripts): row has price/label;
          events[k] = {usd: float, primary, onetime}

What CANNOT be recovered is a price the writing script already lost: a TIERED script with
the flat-only tiers_of (cycle 1350 bug) stored `tiers: {}` for a nested-shape event, and
the live numbers are gone from the file. Those rows are reported UNREPLAYABLE -- they are
the invisible-listing bug class and need a live re-price, not a replay.

A MOVED verdict is not automatically a past mistake: these audits were hand-read at the
time, and the reader often caught what the script got wrong. MOVED means "this cohort's
machine verdict would change today" -- read each one before acting.

KNOWN LIMIT OF THE FLAT SCHEMA (cycle 1396). A FLAT cohort saved ONE number per event, so
a replay of it cannot see a tier ladder -- and the ladder is exactly what _unit_price's
is_start_fee() discriminator needs to recognise an owner's mis-set isOneTimeEvent. Every
`hipersoft/*` row still reported MOVED by a flat cohort is such a case: replayed from the
one saved number the helper demotes the real per-row event, but run against the LIVE record
(which has the ladder) it resolves correctly. Confirmed live for all 8 hipersoft listings at
cycle 1396. So for flat cohorts a MOVED row means "re-price this one live", not "the helper
disagrees"; the TIERED cohorts are the ones whose replay is conclusive.

Usage:  bin/_unit_price_selftest.py [cohort.json ...]      (default: /tmp/*_prices*.json)
Exit 0 = no verdict moved. Exit 1 = at least one verdict moved, read the report.
"""
import glob
import json
import sys

sys.path.insert(0, "/root/agent/bin")
import _unit_price as up  # noqa: E402


def classify(row):
    """Which saved schema is this row? -> 'tiered' | 'flat' | None."""
    if "unit_tiers" in row or "unit_event" in row:
        return "tiered"
    if "price" in row or "label" in row:
        return "flat"
    return None


def rebuild(saved_events, schema):
    """Saved per-event record -> (events dict unit_price() expects, lost_price_keys)."""
    out, lost = {}, []
    for key, e in saved_events.items():
        if not isinstance(e, dict):
            continue
        ev = {}
        if schema == "tiered":
            tiers = e.get("tiers")
            if isinstance(tiers, dict) and tiers:
                # saved tiers are already flat {tier: usd}; _unit_price reads that shape
                ev["eventTieredPricingUsd"] = dict(tiers)
            else:
                lost.append(key)
        else:
            usd = e.get("usd")
            if isinstance(usd, (int, float)):
                ev["eventPriceUsd"] = usd
            else:
                lost.append(key)
        if e.get("primary"):
            ev["isPrimaryEvent"] = True
        if e.get("onetime"):
            ev["isOneTimeEvent"] = True
        out[key] = ev
    return out, lost


def saved_verdict(row, schema):
    """(unit_key, unit_tiers, was_ambiguous) as the writing script recorded it."""
    if schema == "tiered":
        return (row.get("unit_event"), row.get("unit_tiers") or {},
                "AMBIGUOUS" in (row.get("note") or ""))
    price = row.get("price")
    tiers = {"FREE": price} if isinstance(price, (int, float)) else {}
    return row.get("label"), tiers, False


def main(paths):
    moved_total = lost_total = rows_total = files = 0
    for path in sorted(paths):
        try:
            rows = json.load(open(path))
        except (ValueError, OSError) as e:
            print(f"  skip  {path.split('/')[-1]:<26} unreadable: {e}")
            continue
        if not isinstance(rows, list) or not any(isinstance(r, dict) for r in rows):
            print(f"  skip  {path.split('/')[-1]:<26} not a cohort list")
            continue
        moved, lost, checked, schema = [], [], 0, None
        for row in rows:
            if not isinstance(row, dict) or row.get("error"):
                continue
            schema = schema or classify(row)
            events = row.get("events")
            if not schema or not isinstance(events, dict) or not events:
                continue
            # the caller's FREE-model / no-pricing-record branch bypasses unit_price
            note = (row.get("note") or row.get("label") or "")
            if note.startswith("FREE model") or "no pricing record" in note:
                continue
            rebuilt, lost_keys = rebuild(events, schema)
            if lost_keys:
                lost.append((row.get("handle"), lost_keys))
                continue
            checked += 1
            key, tiers, was_amb = saved_verdict(row, schema)
            ut, uk, fee, new_note = up.unit_price(rebuilt)
            now_amb = "AMBIGUOUS" in new_note
            if uk != key or ut != tiers or was_amb != now_amb:
                moved.append((row, key, tiers, was_amb, ut, uk, fee, new_note))
        files += 1
        rows_total += checked
        moved_total += len(moved)
        lost_total += len(lost)
        flag = "MOVED" if moved else "   ok"
        extra = f", {len(lost)} unreplayable" if lost else ""
        print(f"{flag}  {path.split('/')[-1]:<26} [{schema or '?':6}] {checked:>4} replayed, "
              f"{len(moved)} moved{extra}")
        for row, key, tiers, was_amb, ut, uk, fee, new_note in moved:
            print(f"        {row.get('handle')} ({row.get('users')}u)")
            print(f"          was: event={key} tiers={tiers}"
                  + (f" note={row.get('note')!r}" if row.get("note") else "")
                  + (f" undercuts={row.get('undercuts_tiers')}" if row.get("undercuts_tiers") else ""))
            print(f"          now: event={uk} tiers={ut} start_fee={fee} note={new_note!r}")
        for handle, keys in lost:
            print(f"        UNREPLAYABLE (price lost by writer: {','.join(keys)}): {handle}")
    print(f"\nTOTAL {files} cohorts, {rows_total} listings replayed, "
          f"{moved_total} verdict(s) moved, {lost_total} unreplayable")
    return 1 if moved_total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or glob.glob("/tmp/*_prices*.json")))
