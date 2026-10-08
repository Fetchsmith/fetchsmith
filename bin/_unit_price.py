#!/root/agent/venv/bin/python
"""Shared per-row unit-price derivation for the bin/_batch_price_*.py audit scripts.

Closes 0-TODO-h1348-backport-unit-price-helper (filed cycle 1348, done cycle 1396).

WHY THIS EXISTS. A competitor audit has to answer one question per rival listing:
"which of its charge events is the per-ROW rate comparable to ours?" The original
bin/_batch_price_*.py scripts printed every event and left that judgment to whoever
read the output, which is the recurring trap in LEARNINGS (cycle 1336; bit again at
1347 with 8 false positives). Cycle 1348's _batch_price_ted.py first decided it in
code. Every later audit then *copied* that file and fixed bugs in its own copy, so by
cycle 1396 there were 8 divergent versions and the original was the stalest of them:

  * cycle 1350 (found in _batch_price_asr.py's niche, 36/122 listings): Apify stores
    eventTieredPricingUsd in TWO shapes -- {"FREE": 0.006} (flat float) and
    {"FREE": {"tieredEventPriceUsd": 0.006}} (nested dict). ted's flat-only reader
    returned {} on every nested-shape listing, which is not an error and not
    AMBIGUOUS -- the listing simply goes INVISIBLE (no tiers, so no tier undercuts
    us, so it never appears in the findings). 6 of the 8 copies carried the fix;
    ted and its descendants-by-copy did not.
  * cycle 1388 (and cycle 1385 in check-price-superiority): `apify-actor-start` is
    Apify's own reserved key for the run-start charge. It is a start fee in substance
    even when its owner never set isOneTimeEvent, and even when its owner flags it
    isPrimaryEvent=true. Classifying purely on isOneTimeEvent (what ted and 6 of the
    8 copies do) reports that start fee as the rival's per-row price -- the exact bug
    that miscounted 20 rivals fleet-wide at 1385. Only _batch_price_asr.py had it.

So this module is the UNION of both fixes plus ted's original rules. Importers get
every fix at once and the next audit cannot inherit a half-fixed copy.

THE RULES (unchanged in substance from cycle 1348 -- see the TODO's "preserve exactly"):
  * one-time events are NEVER the unit price (we bill per row, not per run); they are
    reported separately as start_fee. `apify-actor-start` counts as one-time whatever
    its flags say.
  * among the remaining recurring events, prefer isPrimaryEvent.
  * fall back to a sole recurring event.
  * return AMBIGUOUS rather than guessing when several recurring events carry no
    primary flag -- cycle 1177's check-primary-event showed a flagged primary can
    itself be the wrong number, so a guess is not safe.
  * keep EVERY tier, not just FREE: a tiered rival's FREE price is not its real
    price (cycle 1220).
  * FREE-model / absent-pricingInfos rivals score $0 (cycle 1104) -- that is the
    CALLER's branch, kept out of here because it reads act_data, not events.

Does NOT retrofit any past audit's output: every finding those scripts produced was
hand-verified at the time. bin/_unit_price_selftest.py replays the saved
/tmp/*_prices.json cohorts through this module to show which verdicts the drift had
actually moved.
"""
import importlib.machinery
import importlib.util
import os

ROOT = "/root/agent"

# Apify's reserved key for the run-start charge. Always a start fee, never a per-row unit.
START_FEE_KEY = "apify-actor-start"


def _load_cps():
    path = os.path.join(ROOT, "bin/check-price-superiority")
    spec = importlib.util.spec_from_loader(
        "cps", importlib.machinery.SourceFileLoader("cps", path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cps = _load_cps()

TIERS = ("FREE", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND")


def tiers_of(ev):
    """All tier prices for one charge event, as {tier: usd}. {} if none resolve.

    Handles both eventTieredPricingUsd shapes (flat float and nested
    {"tieredEventPriceUsd": float}) -- see module docstring, cycle 1350. Falls back to
    cps.price_of for an untiered event, which reads eventPriceUsd.
    """
    t = ev.get("eventTieredPricingUsd") or ev.get("tieredEventPriceUsd")
    out = {}
    if isinstance(t, dict):
        for k, v in t.items():
            if isinstance(v, (int, float)):
                out[k] = v
            elif isinstance(v, dict) and isinstance(v.get("tieredEventPriceUsd"), (int, float)):
                out[k] = v["tieredEventPriceUsd"]
    if out:
        return out
    p = cps.price_of(ev)
    return {"FREE": p} if isinstance(p, (int, float)) else {}


def is_start_fee(key, ev):
    """True if this event bills at most once per run rather than per row.

    `apify-actor-start` is Apify's reserved key and is always a start fee, whatever its
    flags say (cycle 1385/1388). Otherwise we trust the owner's isOneTimeEvent -- EXCEPT
    when the event also carries a multi-tier volume ladder, which contradicts it.

    The tier-ladder discriminator (found cycle 1396, verified live on 8 `hipersoft`
    listings): eventTieredPricingUsd discounts by the subscription tier of a customer who
    buys VOLUME, so a ladder on a charge that can only ever bill once per run is
    meaningless. Every hipersoft Actor flags its real per-row event -- `app-scraped`,
    `job-scraped`, `product-scraped`, `game-scraped`, `review-scraped`, `article-scraped`,
    each with a full 6-tier descending ladder -- as isOneTimeEvent=True AND
    isPrimaryEvent=True. Taking that flag at face value demotes the rival's actual per-row
    rate to a "start fee" and promotes a cheap ancillary `api-request`/`store-page`/
    `feed-fetched` event ($0.0004-$0.001) to the unit price, understating the rival by 2-4x;
    where there is no second event it reads a per-ROW rate as a flat per-RUN fee, which
    understates it without bound. A genuine one-time fee has a single price and no ladder --
    `apify-actor-start` ($0.00005) and `second_coming/brand-mention-monitor`'s $0.02 `scan`
    (the real run-fee rival cycle 1392 hand-verified) both pass that test and stay held out.

    So: one tier = believe isOneTimeEvent; a ladder = the flag is the owner's error.
    """
    if key == START_FEE_KEY:
        return True
    if not ev.get("isOneTimeEvent"):
        return False
    return len(tiers_of(ev)) <= 1


def unit_price(events):
    """(unit_tiers, unit_key, start_fee, note) -- see module docstring for the rules."""
    onetime, recurring = {}, {}
    for k, v in events.items():
        (onetime if is_start_fee(k, v) else recurring)[k] = v
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
