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

Cycle 1492 added a second, cheap leg that runs FIRST and needs no cohorts:
`container_mismatch`'s MISMATCH_CASES table (the h1448 unit-mismatch classifier) plus an
assertion that bin/check-unit-matched-price still imports the shared OUR_UNIT_SYNONYMS
rather than re-growing its own copy. Run this after touching either.

Usage:  bin/_unit_price_selftest.py [cohort.json ...]      (default: /tmp/*_prices*.json)
Exit 0 = no verdict moved and every classifier case passes. Exit 1 = at least one moved or
failed, read the report.
"""
import glob
import json
import os
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


# (our_slug, event name, eventTitle, eventDescription, expected container noun or None).
# Every row is a real live charge event met in an audit, not an invented string -- the
# handle is named in the comment. Added cycle 1492 with container_mismatch (closes
# 0-TODO-h1448-unit-mismatch-rivals): the function is a hand-curated word classifier whose
# two failure directions each already cost a wrong published claim (cycles 1448, 1452), and
# unlike unit_price there is no saved cohort to replay it against, so the cases ARE the
# regression test. Add a row here whenever a noun is added to CONTAINER_NOUNS/ROW_WORDS.
MISMATCH_CASES = [
    # alexmorain/app-store-play-store-scraper -- the listing that filed h1448. Its
    # description mentions "reviews" only to deny billing them, so classifying on the
    # description would read this as OUR unit and stay silent on the filing case itself.
    ("google-play-reviews-scraper", "app", "App scraped",
     "One app -- full review sweep, however many reviews that returns. Reviews are never "
     "billed per unit.", "app"),
    # neverempty/steam-reviews-price-monitor (cycle 1452): our own `game` noun wrapped in an
    # ACTION noun. Participial, so a plural-only \bchecks?\b regex misses it entirely.
    ("steam-reviews-scraper", "game-checked", "Game checked",
     "One monitoring check of a game's review count", "check"),
    # datacach/steam-listing-search-by-keyword (cycle 1452)
    ("steam-reviews-scraper", "search_term", "Search term", "One keyword search performed",
     "search"),
    # scrapesage/steam-scraper's real per-row leg, and its plain container sibling: `game`
    # is a genuine unit of steam-reviews-scraper, so neither may fire.
    ("steam-reviews-scraper", "review-scraped", "Review scraped", "One review record", None),
    ("steam-reviews-scraper", "game", "Game record", "One game record", None),
    # glistening_film/uspto-trademark-lookup -- one phrase, ALL its matches: a true container
    # at exactly our own price, which the ratio comparison reads as a dead tie.
    ("trademark-search-scraper", "phrase-checked", "Phrase checked",
     "Charged once per phrase looked up successfully (all its matches).", "check"),
    # foxlabs/usaspending-contractor-data: "record" is deliberately NOT a ROW_WORD -- a
    # dossier about a company contains many of our award rows.
    ("us-federal-awards-scraper", "company-record", "Company record",
     "One company successfully returned from the source", "company"),
    # sian.agency/google-news-scraper and quodlibetical_buffalo/hacker-news-mcp: an ACTION
    # noun in the name of a genuine per-row event (one result OF a search).
    ("google-news-scraper", "news-search-result", "News Search Result",
     "Charged per article returned by a News Search query.", None),
    # memo23/username-social-finder: Apify's own generic per-row event, "check" in its title.
    ("substack-scraper", "apify-default-dataset-item", "Platform check",
     "Charged once per result row -- one username checked on one platform.", None),
    # a TARGET noun qualified by our own unit noun is our row sliced differently.
    ("shopify-products-scraper", "product-page", "Product page", "One product page", None),
    # suffix false positives the explicit suffix list exists to prevent.
    ("google-news-scraper", "pagerank-computed", "Pagerank computed", None, None),
    ("fda-recall-scraper", "apply-filter", None, None, None),
    # a slug with no curated unit nouns cannot be classified at all.
    ("not-a-live-actor", "app", "App", "per app", None),
]


def check_mismatch_cases():
    """container_mismatch's case table + the OUR_UNIT_SYNONYMS move. Returns failure count."""
    bad = 0
    for slug, name, title, desc, expected in MISMATCH_CASES:
        got, why = up.container_mismatch(slug, name, title, desc)
        if got != expected:
            bad += 1
            print(f"  FAIL  container_mismatch({slug}, {name}) "
                  f"expected {expected!r}, got {got!r} ({why})")
    # The map moved out of bin/check-unit-matched-price at cycle 1492; that tool must still
    # be reading the same 24 curated entries and not a second copy of its own.
    cump = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check-unit-matched-price")
    src = open(cump).read()
    if "OUR_UNIT_SYNONYMS = {" in src:
        bad += 1
        print("  FAIL  check-unit-matched-price has its own OUR_UNIT_SYNONYMS literal again "
              "-- it must import the one in _unit_price.py (cycle 1492), or the two maps "
              "will diverge on the next Actor added to only one of them")
    print(f"{'  FAIL' if bad else '   ok'}  container_mismatch: "
          f"{len(MISMATCH_CASES) - bad}/{len(MISMATCH_CASES)} case(s) pass, "
          f"{len(up.OUR_UNIT_SYNONYMS)} curated unit-noun entries read from _unit_price.py")
    return bad


def main(paths):
    moved_total = lost_total = rows_total = files = 0
    case_failures = check_mismatch_cases()
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
          f"{moved_total} verdict(s) moved, {lost_total} unreplayable, "
          f"{case_failures} container_mismatch case failure(s)")
    return 1 if (moved_total or case_failures) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or glob.glob("/tmp/*_prices*.json")))
