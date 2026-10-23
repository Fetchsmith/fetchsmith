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
import json
import os
import re

ROOT = "/root/agent"

# Apify's reserved key for the run-start charge. Always a start fee, never a per-row unit.
START_FEE_KEY = "apify-actor-start"


def current_cycle():
    """Last `cycle=NNNN ... start` line in worker.log, or None. Same regex as
    bin/audit-due's current_cycle() -- duplicated rather than imported because that file
    is a CLI entrypoint, not a module, and this one has no other reason to exec it."""
    try:
        with open(os.path.join(ROOT, "logs/worker.log")) as f:
            hits = re.findall(r"cycle=(\d+)\s+model=\S+\s+start", f.read())
        if hits:
            return int(hits[-1])
    except OSError:
        pass
    return None


def persist_sweep(niche, out):
    """Write a pricer sweep's full output to state/audit_data/c<cycle>_<niche>_prices.json
    IN ADDITION to whatever /tmp path the caller already writes -- do not replace that
    write, this is a second one.

    Added cycle 2149, closing the cleanup item c2148 filed: all 33 `_batch_price_*.py`
    scripts wrote only `/tmp/<abbrev>_prices.json`, which does not survive reboot, so every
    competitor_audit's full live-priced rival snapshot -- the most expensive data this
    business gathers, ~50-350 listings fetched one `GET /v2/acts/<handle>` at a time -- was
    thrown away. Exactly one sweep was ever kept by hand
    (`state/audit_data/c2124_steam_prices.json`), and c2148 then reused it twice in one
    cycle (a --selftest fixture AND, alongside the 22 stale /tmp leftovers that happened to
    still be on disk, a free 2202-listing precision corpus for check-upstream-warnings) --
    both uses this function exists to make available on purpose instead of by luck.

    Deliberately does NOT prune older files for this niche. The obvious "keep only the
    newest per niche" cleanup the filing queue item floated would have deleted
    `c2124_steam_prices.json` itself the next time steam-reviews-scraper's audit runs --
    check-upstream-warnings hardcodes that exact path as its --selftest fixture (see its
    FIXTURE constant), so an automatic prune is a live footgun, not a cleanup. Leave manual
    curation to whoever next needs the disk space (~85-190KB/sweep per c2148's own note).
    """
    cyc = current_cycle()
    tag = f"c{cyc}" if cyc is not None else "cUNKNOWN"
    path = os.path.join(ROOT, "state/audit_data", f"{tag}_{niche}_prices.json")
    json.dump(out, open(path, "w"), indent=1)
    return path


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


#  A charge that bills once per RUN (not once per row) regardless of its volume tier --
#  the vocabulary a rival owner actually uses for that event's key/eventTitle. Whole-word,
#  case-insensitive (see is_start_fee's cycle-2118 branch below). Deliberately does NOT
#  include "job": fault injection against the real `lepidata/remote-jobs` listing (flat
#  $0.0009 "Unique job" event, its ONLY charge, no volume discount offered) proved it
#  collides with a per-row noun -- both the fleet's own OUR_UNIT_SYNONYMS for
#  remote-jobs-scraper/ats-jobs-scraper and plenty of rivals bill PER job, not per RUN of
#  jobs, so "job" in a key/title is no evidence of run-scope at all. Only add a word here
#  with a real run-fee listing backing it, the same bar "start"/"run"/"scan" clear
#  (apify-actor-start, second_coming's $0.02 `scan`, hyperbach's $0.0011 `start`).
_RUN_SCOPE_RE = re.compile(r"\b(start|run|scan)\b", re.I)

#  Apify's own `eventDescription` text, when the owner wrote one, is ground truth about
#  billing frequency -- stronger than inferring it from the key/title vocabulary or the
#  ladder shape. Found cycle 2127 (substack-scraper audit): `hridayrungta/substack-scraper`'s
#  `actor-started` event is isOneTimeEvent=False with a DESCENDING 6-tier ladder (0.0017 ->
#  0.00119), so neither existing branch above fires (not flagged one-time, and the ladder
#  isn't flat) -- it reads as the recurring primary event, when its own eventDescription says
#  "One-time fee charged once per run, regardless of how many posts or comments it finds."
#  A one-time fee CAN legitimately vary by subscription tier (cheaper on higher plans) without
#  that being volume information, so "ladder = real per-row metering" is not actually true in
#  general -- only true in the absence of a stronger signal. Whole-phrase match, not a single
#  word, to avoid the same false-positive risk "job" had in _RUN_SCOPE_RE.
_ONCE_PER_RUN_RE = re.compile(r"once per run", re.I)


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

    Cycle 2116 found the error also runs the OTHER way (fixed cycle 2118): the
    `not ev.get("isOneTimeEvent")` branch returned False unconditionally, trusting a False
    flag with no override at all. `hyperbach/app-store-reviews-scraper`'s `start` event
    ("Run start", isOneTimeEvent=False) bills a flat $0.0011 on EVERY one of its 6 tiers --
    a FLAT ladder, which per the paragraph above carries no volume information and so
    cannot be evidence of real per-row metering, unlike hipersoft's genuinely descending
    one. Reclassifying flat+unflagged as recurring reads a per-RUN fee as this rival's
    per-ROW rate and hides the real fee entirely (it has a separate genuine per-row `review`
    event, so the $0.0011 just vanishes rather than being promoted -- the single-event case
    would instead understate the rival without bound, same failure shape as the flagged
    side). The override only fires when BOTH the ladder is flat (one distinct value --
    anything else is real volume information and must still win) AND the event's own
    key/title uses run-scope vocabulary (`start`/`run`/`scan`, see _RUN_SCOPE_RE -- "job"
    was tried and dropped, it collides with a real per-row noun) -- "one distinct value"
    alone is not enough, since a rival that simply charges the same per-row cost at every
    tier (no volume discount offered) is syntactically identical and must stay recurring.

    Cycle 2127 added a third override, checked before the ladder-shape heuristic: an explicit
    `eventDescription` saying "once per run" (see _ONCE_PER_RUN_RE above) settles it regardless
    of ladder shape, because a one-time fee can tier by plan without that implying per-row
    metering -- the ladder-shape heuristic below is a fallback for when the owner left no
    description, not a rule that overrides what Apify's own schema already states outright.
    """
    if key == START_FEE_KEY:
        return True
    tiers = tiers_of(ev)
    if ev.get("isOneTimeEvent"):
        return len(tiers) <= 1
    if _ONCE_PER_RUN_RE.search(ev.get("eventDescription") or ""):
        return True
    if len(tiers) > 1 and len(set(tiers.values())) == 1:
        ident = f"{key} {ev.get('eventTitle') or ''}"
        if _RUN_SCOPE_RE.search(ident):
            return True
    return False


DECOY_KEY = "apify-default-dataset-item"


def is_decoy_dataset_item(key, events):
    """True if `key` is Apify's RESERVED generic per-row event AND this listing ALSO has
    a different, named, non-start-fee event to prefer instead.

    Found cycle 2120 (google-play-reviews-scraper audit): `mattzer/google-play-reviews-
    scraper` and `byusuklu/app-store-google-play-app-data` both carry
    `apify-default-dataset-item` priced far below their real business -- $0.00001 vs
    `mattzer`'s named `review` primary at $0.0003 (3x DEARER) and `byusuklu`'s named
    `app-result` at $0.0025 (250x dearer). The generic event is real and billed (see
    container_mismatch's ROW_WORDS comment above -- it is a genuine per-row event by
    definition), so `unit_price()`'s own primary-event preference already gets this right
    when the named event is flagged isPrimaryEvent. The actual gap is in a full-cohort
    SWEEP that scans every non-start-fee event looking for the cheapest number (every
    `_batch_price_*.py` script's stated method, and `check-price-superiority`'s
    multi-event advisory scan below) -- that scan has no primary-event tie-break of its
    own, so it picks up the reserved key as if it were the listing's real per-row rate.

    Scoped narrowly: only fires when a DIFFERENT recurring event exists to prefer over
    it. A listing whose ONLY charge is the generic event has no decoy to prefer over --
    that IS its real (if generic) per-row price, same as any other sole recurring event,
    and must keep reading as such.
    """
    if key != DECOY_KEY:
        return False
    others = [k for k, v in events.items() if k != key and not is_start_fee(k, v)]
    return bool(others)


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


def all_events_all_tiers(events):
    """[(event_name, event_title, {tier: usd}, is_start_fee, is_decoy)] for EVERY live
    charge event. `is_decoy` added cycle 2122 -- see `is_decoy_dataset_item` above.

    Closes 0-TODO-h1452-multi-event-cheap-leg (filed cycle 1452, from the steam-reviews-
    scraper audit). `unit_price` above and `cps._select_event` both reduce a rival to ONE
    event -- the primary, or the cheapest non-one-time one -- so a multi-mode rival's cheap
    leg stays invisible behind its dear leg: a store-AND-reviews scraper's `review` event
    can undercut us while its naturally-dearer `game` event (the one `_select_event` picks)
    reads as several times pricier, and the single-number comparison never looks at the
    other event at all. This returns every event untouched instead of collapsing them, so a
    caller can scan each one's tiers independently.

    Deliberately does NOT decide which event is "the" per-row unit -- that the caller must
    still do, same as `unit_price`'s AMBIGUOUS case, because a cheap secondary event is very
    often a DIFFERENT unit, not a cheaper rate for the same one (0-TODO-h1448-unit-mismatch-
    rivals' container-noun shape: a $0.0003 `game-checked` "monitoring check" event bills
    once per poll, not once per review, so it is not comparably "cheaper" at all). Includes
    `event_title` (`eventTitle`) in the tuple for exactly that reason -- the unit judgement
    needs the free-text label, and re-fetching it after the fact is wasted work.

    Does not change `unit_price`, `headline_price` or `all_tiers`: every existing verdict
    those three produce stays byte-identical, per the 1392/1436 precedent of adding a new
    read path alongside the old one rather than editing it in place.
    """
    return [(k, v.get("eventTitle"), tiers_of(v), is_start_fee(k, v),
              is_decoy_dataset_item(k, events))
            for k, v in events.items()]


# One short tuple of nouns per slug, read off that Actor's OWN meta.json event
# description -- the thing we actually bill per row, not what a rival calls it.
#
# Moved here from bin/check-unit-matched-price at cycle 1492 (values byte-identical,
# asserted by bin/_unit_price_selftest.py) so the h1448 leg in check-price-superiority
# and check-unit-matched-price's own unit matching read ONE curated map. A second
# hand-curated copy is exactly the drift this module was created to end (see the
# docstring: 8 divergent _batch_price_*.py copies by cycle 1396) -- and a map keyed by
# our own slugs rots on every new Actor, so two copies would diverge on the first build.
OUR_UNIT_SYNONYMS = {
    "apple-podcasts-scraper": ("episode", "review", "podcast"),
    "app-store-reviews-scraper": ("review",),
    "ats-jobs-scraper": ("job", "posting"),
    "clinicaltrials-scraper": ("study", "trial"),
    "court-records-scraper": ("docket", "opinion", "case"),
    "eu-ted-tenders-scraper": ("tender", "procurement", "notice"),
    "fda-recall-scraper": ("recall",),
    "fec-campaign-finance-scraper": ("candidate", "contribution", "filing", "committee"),
    "federal-register-scraper": ("document", "rule", "notice"),
    "google-news-scraper": ("article", "news"),
    "google-play-reviews-scraper": ("review",),
    "grants-gov-scraper": ("opportunity", "grant"),
    "hacker-news-scraper": ("story", "comment"),
    "nih-reporter-scraper": ("project", "grant", "award"),
    "remote-jobs-scraper": ("job", "posting"),
    "sam-gov-opportunities-scraper": ("opportunity", "contract", "record"),
    "scholarship-scraper": ("scholarship",),
    "sec-insider-trades-scraper": ("transaction", "trade", "filing", "form"),
    "shopify-products-scraper": ("product",),
    "steam-reviews-scraper": ("review", "game"),
    "substack-scraper": ("post",),
    "trademark-search-scraper": ("trademark",),
    "uk-find-a-tender-scraper": ("tender", "procurement", "notice"),
    "us-federal-awards-scraper": ("award", "grant", "contract"),
}

# Words that denominate something OTHER than one of our rows, in two kinds, because they
# behave differently when one of OUR OWN unit nouns sits beside them in the same event name
# (see container_mismatch's docstring). Every entry was observed live on a real rival.
#
# ACTION: a charge per OPERATION -- one poll, one search, one request -- with the rows it
# returns not billed at all. Never our unit even when our noun is also present, because the
# noun is the operation's TARGET, not the thing billed: neverempty/steam-reviews-price-
# monitor's $0.0003 `game-checked` is one monitoring check of a game (cycle 1452), and
# datacach/steam-listing-search-by-keyword's $0.0005 is one `search_term` (cycle 1452).
#
# `scan` is deliberately NOT here even though `second_coming/brand-mention-monitor` bills a
# flat $0.02 `scan` (cycle 1392): as a participle, "scanned" is a row-PRODUCTION verb like
# "scraped"/"crawled"/"fetched" (a rival's `job-scanned` is one job row, exactly our unit),
# and nothing syntactic separates that from "game-checked" -- only the semantics of the verb
# do. Since that one real per-`scan` rival is run-scoped and already held out of the per-row
# comparison by `runfee_price`, including it here would buy no coverage and cost a false
# positive on every `*-scanned` per-row event. Same reason "scraped"/"crawled"/"fetched"/
# "found"/"returned" are absent: they denominate our row, not a container of it.
ACTION_NOUNS = ("check", "poll", "monitor", "search", "query", "request", "task",
                "term", "keyword")
# TARGET: a charge per CONTAINER of rows -- one app, one company, one profile. The filing
# case is alexmorain/app-store-play-store-scraper's $0.01 per `app` / "App scraped", whose
# own description says one app covers the "full review sweep, however many reviews that
# returns" (cycle 1448). Unlike an ACTION, a TARGET beside one of our own nouns usually IS
# our row sliced differently (`product-page` = one product), so that case stays silent.
TARGET_NOUNS = ("app", "game", "page", "url", "profile", "company", "channel", "account",
                "listing", "feed", "site", "domain")
CONTAINER_NOUNS = ACTION_NOUNS + TARGET_NOUNS

# Whole words only, with the suffixes Apify event names actually use -- they are
# overwhelmingly participial (`game-checked`, `app-scraped`, `review-returned`), and a
# plural-only `\bchecks?\b` silently misses every one of them (caught while testing the
# cycle-1452 `game-checked` case, which this function exists to catch). Punctuation is
# flattened to spaces first, so `game-checked`/`search_term` read as "game checked"/
# "search term"; the explicit suffix list keeps `page` off "pagerank" and `app` off
# "apply"/"appeal", which a loose `\w{0,3}` would both match.
_WORD = {n: re.compile(rf"\b{n}(s|es|ed|ing|ned|ning)?\b", re.I) for n in CONTAINER_NOUNS}
_PUNCT = re.compile(r"[^0-9A-Za-z]+")

# Words that denominate one element of the OUTPUT STREAM, which cancels a container
# reading: a `search-result` is one result OF a search, not one search, and
# `apify-default-dataset-item` is Apify's own per-row event by definition. Found by reading
# the first fleet-wide run of this check (cycle 1492): 6 of its 12 printed advisories were
# per-row events whose name merely mentioned an operation -- sian.agency/google-news-scraper
# `news-search-result` ("Charged per article returned by a News Search query"),
# quodlibetical_buffalo/hacker-news-mcp `search-result` ("for each result returned"),
# memo23/username-social-finder, luminar/hackernews-scraper-monitor `item_result`,
# tidytools/app-store-top-charts `chart-entry`, maximedupre/app-store-ratings-scraper
# `app-result`. Deliberately NOT including "record": a `company-record`/`profile-compiled`
# is a dossier ABOUT a target and so really is a container of our rows (foxlabs/
# usaspending-contractor-data charges $0.004 per company while we charge $0.004 per AWARD,
# and one company has many awards) -- those must keep firing.
ROW_WORDS = ("result", "row", "item", "entry")
_ROW_WORD = re.compile(rf"\b({'|'.join(ROW_WORDS)})s?\b", re.I)


def container_mismatch(our_slug, ev_name, ev_title, ev_desc):
    """(container_noun, blob_excerpt) when a rival's selected event looks denominated in a
    CONTAINER of our row, else (None, reason). Closes 0-TODO-h1448-unit-mismatch-rivals.

    THE BUG. Every price check we own compares the rival's selected event price to our
    per-row price as a RATIO, which is only meaningful when both sides bill the same unit.
    `alexmorain/app-store-play-store-scraper` (cycle 1448) bills $0.02 start + $0.01 per
    APP, and its own charge-event description says one app event covers the "full review
    sweep, however many reviews that returns. Reviews are never billed per unit." Against
    our $0.0001/review, `headline_price` compared $0.01 > $0.0001, called it 100x PRICIER
    and stayed silent -- while in truth ~$0.03 flat per app beats us on every app with more
    than ~300 reviews, and beats us without bound above that (a 50k-review app: $0.03 them,
    $5.00 us). `runfee_price` (the cycle-1392 fix for the per-RUN version of this error)
    correctly declines the listing because it HAS a per-row event -- the event is simply
    per-row in the wrong row. So this is the per-ROW analogue of h1356/h1392, and it points
    the same way: a false NEGATIVE on the one thing these checks exist to catch.

    The error also runs the other way, which is why the caller must stay advisory: cycle
    1452 hand-ruled-out TWO rivals whose cheap-looking number was a container charge
    (`game-checked` monitoring, `search_term`) while their real per-row rate was 1.7-4.3x
    DEARER than ours. Auto-flagging either direction would publish a wrong claim, and only
    the free-text `eventDescription` says which it is -- hence (noun, excerpt) for a human
    to read, never a verdict.

    THE TEST: a CONTAINER_NOUNS word in the event's NAME or TITLE, no ROW_WORDS word
    present, and the container noun is not itself one of OUR_UNIT_SYNONYMS[our_slug]. Every
    clause is load-bearing, and the obvious simpler versions are wrong on real listings:

      * Name and title only, never the DESCRIPTION, for the classification. The billed
        unit is what the event is NAMED (`app`, `game-checked`, `review-scraped`); the
        description is prose that mentions other nouns freely -- and in the filing case it
        mentions OUR noun precisely to deny billing it ("however many REVIEWS that
        returns. Reviews are never billed per unit"). An any-field scan therefore reads
        alexmorain's per-APP event as matching our `review` unit and stays silent on the
        very listing that filed the TODO. The description is still returned as the
        excerpt, because that free text is what a human needs to adjudicate.
      * An ACTION noun fires even when one of OUR nouns is present; a TARGET noun only
        fires when none is. Our nouns cannot simply veto, because a mismatched event often
        contains one -- `game-checked` is steam-reviews-scraper's own `game` (we bill per
        review-or-game) wrapped in `check`, and cycle 1452 hand-ruled it a mismatch for
        exactly that reason. But containers cannot simply win either: shopify-products-
        scraper's `product-page` is one page per PRODUCT, i.e. our row sliced differently,
        and flagging it would be a false positive. The split resolves both -- an operation
        charge is never our row no matter what it operates ON, while a target charge
        qualified by our own noun usually is.
      * A ROW_WORDS word anywhere in name/title cancels the whole test, checked FIRST. An
        operation noun appears just as often in the name of a genuine per-row event -- a
        `search-result` is one result OF a search -- and that shape was 6 of the 12
        advisories the first fleet-wide run printed (see ROW_WORDS above for the handles).

    An unrecognised noun is NOT assumed to be a mismatch -- silence means "no evidence of
    mismatch", matching `unit_price`'s AMBIGUOUS-rather-than-guess rule. The recall cost is
    a container noun nobody has met yet, which a later audit adds to the tuple above.
    Unknown slug (a new Actor with no synonyms entry) returns None: with our own unit
    unknown, every rival noun would read as leftover.
    """
    synonyms = OUR_UNIT_SYNONYMS.get(our_slug)
    if not synonyms:
        return None, f"no unit synonyms curated for {our_slug}"
    ident = _PUNCT.sub(" ", " ".join(x for x in (ev_name, ev_title) if x))
    if not ident.strip():
        return None, "event has no name/title text to denominate a unit"
    if _ROW_WORD.search(ident):
        return None, "names an output-stream element (result/row/item/entry), per-row"
    # Substring, not whole word, for OUR side -- the same test check-unit-matched-price has
    # used since cycle 1252, so "reviews"/"reviewer" still resolve to our `review` unit.
    low = ident.lower()
    ours = {s for s in synonyms if s in low}
    for noun in CONTAINER_NOUNS:
        if noun in ours or not _WORD[noun].search(ident):
            continue
        if noun in TARGET_NOUNS and ours:
            continue  # a target qualified by our own noun is our row sliced, see docstring
        blob = " ".join(" ".join(x.split()) for x in (ev_name, ev_title, ev_desc) if x)
        return noun, blob if len(blob) <= 160 else blob[:160].rstrip() + "..."
    return None, (f"only our own unit noun(s) {sorted(ours)} present" if ours
                  else "no container noun recognised")
