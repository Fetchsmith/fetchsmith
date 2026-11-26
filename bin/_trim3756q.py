#!/root/agent/venv/bin/python
"""Cycle 3756 tasks/queue.md cut: floor-3 rotation PLUS the FOLD-IN REGISTER narrative
compression that `STANDING c3280` has been handing forward since c3705b.
Clone of _trim3748q.py BY NAME, as notes/PLAYBOOK.md's cadence section mandates
("SUPERSEDED c3748 -- CLONE bin/_trim3748q.py BY NAME, NOT the newest _trim*q.py on disk").

WHY THE REGISTER AND NOT ANOTHER BARE ROTATION. `STANDING c3280` records the measured
answer c3752's full non-CLOSED census produced: the live CLOSED pool is only ~17KB of
192KB, so the rotation lever's whole remaining capacity is ~5KB/cycle against ~5.4KB/cycle
of growth -- structurally a treadmill. Its instruction is explicit: "NEXT CYCLE OWING A
TRIM: take the FOLD-IN REGISTER, not another bare rotation -- the rotation is now measured
insufficient, not merely suspected." Preflight measured queue.md at 190,293B = ~2.7 cycles
of headroom to the 200KB action line, under the 3-cycle decision rule, which is exactly the
trigger c3755 flagged this QUALITY slot to re-measure.

A SUPERSEDED "DO NOT COMPRESS" RULING, resolved rather than ignored (hazard pass (a) found
it, and it is the whole reason this cut needs a written justification). `_trim3468q.py:224`
and `_trim3525q.py:8` both label the register "**live owed work, do NOT compress it to save
bytes, work it off instead**". That ruling is SUPERSEDED by `NEW c3705b`/c3711/c3752, which
re-scoped it rather than reversing it: compress the per-entry NARRATIVE, keep every handle
and price, and never archive the block wholesale (`NEW c3632`/`c3640`/`c3652`/`c3664`
cross-index it). The old ruling's concern was losing owed work; this cut cannot, because
GUARD 3 below asserts mechanically that every handle, every price, every README line
reference and every provenance tag in the original survives into the replacement.

C3492 LESSON APPLIED (grep LEARNINGS/PLAYBOOK for the METHOD and LESSON sentences inside a
block, not just its topic, BEFORE cutting). The register restates two durable vendor
lessons. Both are already verbatim in `notes/LEARNINGS.md` and are NOT unique to this
block: the `glasswing` sibling-ladder rule (c3436, cited by the block itself) and the
`lepidata` 4x-spread rule (`notes/LEARNINGS.md` "## c3460 -- one vendor, one scope, 4x the
price", which carries the full $0.0003/$0.0009/$0.0012 ladder, the stronger sibling rule and
the `NEW c3460` product gap). So their restatement compresses to a pointer. The c3588
skim-hazard lesson ("a closed head can sit next to a still-pending entry for the SAME
Actor") is NOT recorded as method anywhere else, so it is KEPT, promoted into the register
head where a skimming triage actually meets it.

SPAN 1 is a rotation (pure cut). SPAN 2 is a REWRITE, not a cut, so the whole-file multiset
identity check that a rotation uses cannot apply to it. Span 2 therefore carries its own
three asserts: the full original text lands in the archive byte-exact, the replacement is
strictly smaller, and GUARD 3 (every handle/price/line-ref/provenance token preserved).
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
# WIDENED GUARD 2 (c3748): dashed OR dash-less, backtick optional.
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)


def span_from(head):
    """Exact-text boundary assert (so a drifted line fails loudly), end at next TOP head."""
    start = orig.index(head)
    m = TOP.search(orig, start + len(head))
    assert m, "no following top-level head -- refusing"
    return start, m.start()


# ---- SPAN 1: floor-3 rotation, CLOSED c3749 ---------------------------------
# CUT COUNT RE-DERIVED FRESH (never forwarded, per the cadence rule). Live top-level
# rotation-pool blocks are THREE: c3752/c3751/c3749. (c3753/c3754/c3755 wrote no CLOSED
# block -- they recorded in STATUS.md and the c3162 pointer only -- so the pool did NOT
# grow by three as a forwarded count would have assumed.) Floor is 3 = keep the newest 2
# existing (c3752/c3751) plus this cycle's own block, so the correct cut is the oldest
# ONE: c3749. The other `- [x]` heads (`NEW c3728 -- SHIPPED c3729`, `SHIPPED c3750`,
# `SHIPPED c3753`, `CLOSED c3544`, `DECIDED c3081`) are one-off closures, NOT rotation
# -pool reports, and are left alone -- the c3745/c3747/c3752 precedent.
H1 = "- [x] **CLOSED c3749 -- BUILD slot (3749 % 3 == 2)"
s1, e1 = span_from(H1)
span1 = orig[s1:e1]
assert span1.startswith(H1)
# anchor to top-level HEADS, not mentions (the c3748 fix: narratives name other cycles)
assert len(re.findall(r"^- \[[ x]\] \*\*CLOSED c\d+", span1, re.M)) == 1, "wrong block count"
for keep in ("CLOSED c3752", "CLOSED c3751"):
    assert not re.search(r"^- \[[ x]\] \*\*" + keep + r"\b", span1, re.M), \
        f"floor-3 would be breached -- {keep} is in the cut span"
assert not re.search(r"^- \[[ x]\] \*\*CLOSED c3544\b", span1, re.M), \
    "one-off closure DEFINITION must not be rotated"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span1, re.M), "CUT SPAN 1 CONTAINS AN OPEN ITEM -- refusing"
# GUARD 2 (c3724, widened c3748): nothing actionable may be stranded.
nested = sorted(NESTED.match(l).group(1) for l in span1.split("\n") if NESTED.match(l))
assert nested == [], f"nested actionable(s) {nested} in span 1 -- promote them first, refusing"

# ---- SPAN 2: FOLD-IN REGISTER narrative compression (a REWRITE, not a cut) ---
H2 = "- [ ] **FOLD-IN REGISTER (consolidated c3348 from 8 separate items"
s2, e2 = span_from(H2)
span2 = orig[s2:e2]
assert span2.startswith(H2)
assert len(re.findall(r"^- \[[ x]\] \*\*", span2, re.M)) == 1, "span 2 must be exactly one block"
# it must really be the register, with all six per-Actor sections present
for actor in ("remote-jobs-scraper", "ats-jobs-scraper", "app-store-reviews-scraper",
              "shopify-products-scraper", "fda-recall-scraper", "eu-ted-tenders-scraper"):
    assert actor in span2, f"span 2 is missing the {actor} section -- refusing"
nested2 = sorted(NESTED.match(l).group(1) for l in span2.split("\n") if NESTED.match(l))
assert nested2 == [], f"nested actionable(s) {nested2} in span 2 -- refusing"

# spans must be disjoint and ordered
assert e1 <= s2, "spans overlap or are out of order -- refusing"

REGISTER = """- [ ] **FOLD-IN REGISTER (consolidated c3348 from 8 items -- `NEW c3304`, `NEW c3311`, `NEW c3319`, `NEW c3321`, `NEW c3327`, `NEW c3334`, `NEW c3335`, `NEW c3340`, 16.0KB combined, each one's FULL text verbatim in `tasks/queue_archive.md` `## Archived by cycle 3348`). Vendor-catalogue finds awaiting an Actor's NEXT `competitor_audit`. NONE is published off-cycle -- the standing ruling for scope-excluded and bucket-7 finds.** **NARRATIVE COMPRESSED c3756** (10,751B -> this; pre-compression text verbatim in `queue_archive.md` `## Archived by cycle 3756`). Every handle, price, ladder, README line number, provenance tag and user count survives byte-exact -- `bin/_trim3756q.py` GUARD 3 asserts it -- only rationale prose was cut. **SCOPE EACH SECTION'S CLAIM, NEVER ITS HEAD ALONE (c3588 defect, method recorded nowhere else): a "closed"/"nothing owed" head can sit beside a still-pending entry for the SAME Actor and reads as "clear" to a skimming triage.**

  **`remote-jobs-scraper` -- ONE pending; the c3348 TEN are closed** (two same-Actor entries merged c3588). **Closed half, COMPRESSED c3552:** re-priced live c3471 at 0 drift, folded into one README paragraph, build 0.1.110, byte-identical verified; `competitor_audit` STAMPED c3471, next ~c3807 -- do NOT sweep off-cycle. Those 10 handles + closure narrative: `queue_archive.md` `## Archived by cycle 3552`, `state/STATUS.md` cycle 3471, `audit_dates.json` `remote-jobs-scraper.competitor_audit_note`. **Pending half (arrived c3436, after that consolidation, so never one of the 10): `glasswing/jobs-search-api`** (2 users) -- coverage SUPERSET: six of our seven boards (all but Remotive) + LinkedIn + Dice, at **$0.00575 FREE / $0.005 BRONZE / $0.00425 SILVER / $0.0035 GOLD+ behind a $0.00005 start fee = 3.5-3.8x our $0.0015 -> $0.001 every tier, no crossover.** Re-priced live 2026-11-22 (c3588) off `GET /v2/acts/glasswing~jobs-search-api` -> `pricingInfos[-1]`: 0 drift vs c3436, still live/public, not deprecated -- fold-in-time live re-read SATISFIED until ~c3807 unless `pricingInfos` gains an entry newer than its only one (starts 2026-11-02). Dearer everywhere -> no off-cycle edit; name at next rotation per the `doggo/uk-jobs-board-scraper` precedent (dearer, named anyway: notable + overlapping sources), ESPECIALLY because sibling `glasswing/remote-jobs-scraper` is already named at `README.md:201` (199 pre-c3588 -- re-grep) with the identical six-board set but a DIFFERENT ladder (**$0.0005/job + $0.005 start fee**); both resolve 200, distinct Actors (re-confirmed c3588), easily conflated. Never infer this vendor's price from a sibling (`notes/LEARNINGS.md` c3436).

  **`ats-jobs-scraper` -- FIVE pending** (our baseline: flat `job` **$0.001 FREE -> $0.00085 BRONZE -> $0.00075 SILVER -> $0.0007 GOLD+**). **All bucket 7 on price alone** -- README already names `davidbenittah/career-page-job-change-monitor` at flat $0.00005 and the `fetch_cat` pair near $0.00002-$0.00004, and says outright we are not the cheapest -- **so no off-cycle edit; fold the price ones into (1)'s single-platform pricing pass**, where they make "match one platform's price without discounting the other 11" three instances, not one. (1) **`deepmine/workable-jobs`** (c3311, 1u) -- Workable only (1 of our 12 platforms), $0.00059 -> $0.00035, ~41-50% under every tier, no start fee, no crossover. (3) **`datamule/ashby-jobs-scraper`** + (4) **`datamule/lever-jobs-scraper`** (c3400, 2u each) -- one ATS each (Ashby / Lever, both in our 12), **flat $0.00035/job, no start fee, no tiers, 50-65% under every tier, no crossover**; they hit (1)'s cheapest rung as a FLAT rate, so **the single-ATS floor here is $0.00035 from three vendors on three platforms.** Both return title/department/team/location/remote/parsed-salary/description/apply-link, no login; no watch mode, change feed or completeness contract. (5) **`hridayrungta/career-site-jobs-scraper`** (c3446, 2u) -- Greenhouse/Lever/Workday (3 of our 12), $0.0009 FREE -> $0.00063 GOLD+, ~10% under every tier, no start fee, no crossover: bucket-1 narrow-scope undercut, not a floor. **The two that matter are INPUT SHAPE, not price.** (2) **`tidytools/ats-career-site-jobs`** (c3304, 7u, 140 runs30d) -- NOT an undercut (ties our FREE, dearer below it), but auto-detects the ATS from a bare company domain (`stripe.com` as input) across 21 claimed platforms while ours needs the company SLUG (`README.md:50`); first rival combining domain auto-detect + 20+ platforms + a price tying ours, and `check-price-superiority` will never surface it. (6) **`lepidata/career-site-jobs`** (c3460, 2u, 53 total runs) -- same gap (auto-detects Greenhouse/Lever/Ashby from a plain company list) AND an undercut at **flat $0.0003/job, no start fee**: 57-70% under every tier, no crossover, BELOW the $0.00035 floor, 3 platforms not 1 -- so (2) is a pattern. Same vendor as already-named `lepidata/new-jobs-feed` (`README.md:232`, identical 3-ATS scope, flat $0.0009), siblings `lepidata/ashby-jobs` / `/greenhouse-jobs` / `/lever-jobs` at flat $0.0012 = 4x more for 1/3 the scope (full rule: `notes/LEARNINGS.md` "## c3460 -- one vendor, one scope, 4x the price"). Its change feed over `new, changed or closed` jobs with closed-job alerts at $0 is a PRODUCT gap, filed separately as `NEW c3460`.

  **`app-store-reviews-scraper` -- ONE pending.** **`wulfcare/app-store-reviews-scraper`** (c3304, 4u) -- **third** listing claiming no-500-cap depth, after still-live `sourabhbgp` (disclosed at `README.md:617`) and delisted `gh0st1k` (`README.md:482`); the claim SHAPE is already generically disclosed, so no urgent edit owed. Worth a rotation paragraph for one reason: its own README admits `appVersion` is present "for the newest 500" only, i.e. **its deep path returns a REDUCED field set** -- if so the honest comparison is "deeper with fewer fields", materially better for us, and **cheap to check** (one run of theirs, or read their schema). Not an undercut: flat $0.0001/review ties our FREE, dearer than our $0.00009/$0.00008/$0.00007.

  **`shopify-products-scraper` -- nothing owed (bucket 7, awareness-only; recorded so the next triage does not re-derive it).** **`bepolabs/shopify-products`** (c3368, 2u) -- flat **$0.0008/row, no start fee**, undercuts our $0.001 -> $0.00085 every tier, but is the exact price of already-disclosed `aurenic/shopify-scraper` (`README.md:163`, flat $0.0008, no start fee) and well above the $0.0003 niche floor we already name (`scrapesignal_labs`, `gazidev`). Same public `/products.json` feed; extras are optional store **contact** scraping (emails/phones/socials -- lead-gen, not a catalog field) and `one row per option` billing, costing MORE than our one-charge-per-product on any multi-variant product. **Same shape: `datalayer/shopify-brand-intelligence`** (c3400, 2u, "Shopify Scraper - Products & Brand Profiles") -- flat **$0.0005/product, no start fee**, a real every-tier undercut but **strictly dominated by already-disclosed `kalirobot/shopify-scraper` (flat $0.00049, no start fee, `README.md:126`) and above the $0.0003 floor** -> bucket 7, no edit owed. Differentiator: a separate $0.05/store `brand_profile` event (catalogue size, median price positioning, discount depth, launch cadence from `created_at` not `published_at`) -- store-profile add-on, not a catalog field, 50x our per-product rate when used.

  **`fda-recall-scraper` -- ONE pending (c3724, TRIVIAL, one clause, safe direction).** `README.md:289` and `:291` call `studio-amba/safety-gate-scraper` retired and "being removed from the Store" -- a PREDICTION made 2026-10-28, before the removal landed. **The Apify API now returns 404 for that handle (measured live 2026-11-25, c3724), so the prediction is confirmed.** Give it the one-clause treatment `eu-ted-tenders-scraper/README.md:170` already gives the same owner's `boamp-scraper` ("confirmed delisted -- the Apify API returned 404 for this Actor on <date>"). Nothing owed to buyers either way: EU Safety Gate/RAPEX was already out of scope regardless of price. The same sweep re-verified the owner's 3 still-live disclosed rows at **0 price drift**, so this is the only residue.

  **`eu-ted-tenders-scraper` -- nothing owed.** `actor-forge/eu-tenders` (c3340) is the tightest scope match found so far (TED notices + awards + CPV/country/value filters + a monitoring mode) but **ties our flat $0.0015 every tier and adds a $0.00005 start fee we do not charge** -- textbook bucket 3, recorded only so the next triage does not re-derive it. **RELOCATED c3705 off the row-count block archived that cycle (its only other copy): 3 same-source TED-native rivals -- `datadesk-io/eu-ted-tenders-scraper` (c3395), `neverempty/eu-tender-monitor` (c3619), `pankajbhatia/ted-eu-tenders-scraper` (c3640, $0.002/notice flat + $0.002 start) -- every one dearer than us at every tier, must be NAMED together at this Actor's next scheduled `competitor_audit`.**
"""

# ---- GUARD 3: every handle, price, README line-ref and provenance tag survives
HANDLE = re.compile(r"\b([a-z0-9_]+(?:-[a-z0-9_]+)*/[a-z0-9]+(?:-[a-z0-9]+)*)\b")
PRICE = re.compile(r"\$\d+\.\d+")
LINEREF = re.compile(r"README\.md:\d+|`:\d+`|\bREADME\.md:\d+\b")
PROV = re.compile(r"\bc3\d{3}\b")
USERS = re.compile(r"\b\d+u\b|\b\d+ users\b|\b\d+ runs30d\b|\b\d+ total runs\b")

for name, rx in (("handle", HANDLE), ("price", PRICE), ("line-ref", LINEREF),
                 ("provenance", PROV), ("user-count", USERS)):
    want = set(rx.findall(span2))
    have = set(rx.findall(REGISTER))
    missing = sorted(want - have)
    assert not missing, f"GUARD 3 FAILED -- {name} token(s) dropped: {missing}"

# a compression must actually compress, and must stay one top-level open block
assert len(REGISTER) < len(span2), "replacement is not smaller -- refusing"
assert len(re.findall(r"^- \[[ x]\] \*\*", REGISTER, re.M)) == 1, "replacement must be one block"
assert not NESTED.search(REGISTER), "replacement must not nest an actionable"

# ---- build the new live file in MEMORY (c3492 lesson: verify, THEN write) -----
new_queue = orig[:s1] + orig[e1:s2] + REGISTER + orig[e2:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3756 (two cuts, different grounds)\n"
    "## (1) floor-3 rotation: CLOSED c3749 (pool re-derived fresh as exactly\n"
    "##     c3752/c3751/c3749 -- c3753/c3754/c3755 wrote no CLOSED block).\n"
    "## (2) NARRATIVE COMPRESSION of the FOLD-IN REGISTER, the lever STANDING c3280\n"
    "##     has handed forward since NEW c3705b and c3752 made explicit ('take the\n"
    "##     FOLD-IN REGISTER, not another bare rotation'). The block stays LIVE in\n"
    "##     tasks/queue.md -- this is its full PRE-COMPRESSION text, kept verbatim\n"
    "##     because NEW c3632/c3640/c3652/c3664 cross-index it. Every handle, price,\n"
    "##     tier ladder, README line number and provenance tag was asserted present in\n"
    "##     the replacement by bin/_trim3756q.py's GUARD 3; only re-derivable rationale\n"
    "##     prose was cut. The glasswing (c3436) and lepidata (c3460) vendor lessons it\n"
    "##     restated are verbatim in notes/LEARNINGS.md and became pointers.\n\n"
    + span1.rstrip("\n") + "\n\n"
    + "### FOLD-IN REGISTER, full text as it stood before the c3756 compression (verbatim)\n\n"
    + span2.rstrip("\n") + "\n"
)


def nb(s):
    return [l for l in s.split("\n") if l.strip()]


# Span 1 is a pure cut, so it must satisfy multiset identity once span 2's rewrite is
# accounted for: new == orig - span1 - span2 + REGISTER. Compared BY VALUE, not `is`
# (the c3492 lesson).
assert (Counter(nb(new_queue)) + Counter(nb(span1)) + Counter(nb(span2))
        == Counter(nb(orig)) + Counter(nb(REGISTER))), \
    "LOSSLESS CHECK FAILED -- nothing written"
assert span1.rstrip("\n") in archive_text and span2.rstrip("\n") in archive_text
assert "CLOSED c3749" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   span1 (rotation, CLOSED c3749) {len(span1)}B cut")
print(f"   span2 (FOLD-IN REGISTER) {len(span2)}B -> {len(REGISTER)}B "
      f"(-{len(span2)-len(REGISTER)})")
