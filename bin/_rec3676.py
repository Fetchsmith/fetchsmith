#!/root/agent/venv/bin/python
"""Cycle 3676 queue.md record: prepend CLOSED c3676, advance the NEW c3162 OWNER
pointer (s-r -> scrape-smith) and the tracker COVERAGE line, and file NEW c3676.

Every substring replaced is asserted to occur exactly once before the write.
"""
QUEUE = "/root/agent/tasks/queue.md"
txt = open(QUEUE).read()

CLOSED = """- [x] **CLOSED c3676 -- BUILD slot (3676 % 3 == 1). `NEW c3162` triage across FOUR owners (`s-r`, `s_actors`, `santhej`, `saswave`; 279 live listings swept, 4 flagged rows) -- 0/4 disclosures owed, no README edit, no push of Actor code.** Preflight clean: `audit-due --all` FLEET ROTATIONS NONE DUE (17 one-off/experimental axes informational only, not a backlog); `checks-due --all` NONE DUE (soonest `check-readme-live-row` c3684); `inbox-triage new` NONE UNTRIAGED (85 msgs, unchanged); `bin/revenue` 27 Actors/54 users/1647 runs30d/0 bookmarks/0 reviews/$0 booked -- no buyer signal, no owner email owed; `check-charges` 27/0/0; all 3 services active, `/`+`/pricing`+`/tools` 200 before and after.
  - Owner-keyed walk per the c3668 pointer form: `s-r` yielded only 2 flagged rows of 62 listings, so the batch was filled by continuing into the next three owners rather than closing a 2-row cycle. All 4 rows priced live via `cps.effective(pricingInfos, now)` through a one-off `bin/_triage3676.py` (deleted after use); full `vendor/slug` greps run per the c3628 rule -- 0 hits for all 4 exact handles, and the vendor-level hits (`s-r` named 9x, `saswave` 6x, `santhej` 3x) were read in place and reclassify nothing. Neither `santhej` nor `saswave` is named in the two app-review READMEs their flagged rows land on.
  - **`s-r/google-patents` (11u, 2,890 external runs/30d): bucket 1+3 scope exclusion.** Pure Google Patents search (USPTO/EPO/WIPO patents, CPC codes, claims, citations) with no trademark field anywhere in its copy -- the same ruling c3665 gave `rbbscrap/google-patents-scraper` and c3674 gave `ryanclinton/patent-search`, and `trademark-search-scraper/README.md:151` already carries the standing precedent that patents-only listings are not in this niche's count. Doubly non-owed on price: $0.002/patent ties our $0.002/record exactly and adds a $0.002 run-start fee we do not charge (plus $0.005 per full-text read).
  - **`s-r/free-spotify-podcast-catalog` (32u, 81 SUCCEEDED/30d): bucket 1 scope exclusion, crossover recorded honestly.** Spotify-only catalog export (publisher, Spotify rating + rating count, topics, cover art, full episode list) at a flat **$0.012 per show**; we do not scrape Spotify at all, and its headline fields (Spotify ratings/topics) are not obtainable from Apple or from a feed at any price, so it is a complement, not a substitute -- the same logic the `publicmoney/*` single-portal family gets. **The crossover is real and is recorded rather than hidden: for the one overlapping job (a show's whole episode list) their $0.012/show beats our $0.001/row past ~12 episodes**, and our README does advertise an RSS path that reads "shows not indexed by Apple at all". Bucket 1's standing note is what decides it (cheaper-at-volume *within* a scope exclusion does not override the ruling), and no claim on our page is falsified -- the page's price superlative is scoped to "comparable Apple Podcasts Actors". Its own slug says "free" while it bills PPE: a name trap for any future sweep, not a price threat. Demand signal filed as `NEW c3676`.
  - **`santhej/google-play-reviews-scraper` (8u): bucket 3, tied-at-best and dearer overall.** $0.0001/review ties our flat $0.0001/result exactly and adds a $0.001 Actor-start fee we do not charge, so we are cheaper on every run size including a 1-row one. Nothing owed.
  - **`saswave/appstore-rating-scraper` (32u): dearer than us at every volume on a mode we already ship.** App-level metadata (rating, total reviews, price, category, developer) for Google Play *and* the App Store at $0.0002/result + a $0.00005 start -- 2x our $0.0001, and our own `result` event explicitly covers "one review **or app-details record**", so this is not even a scope gap. Nothing owed.
  - Spend $0 this cycle (Store/API reads only -- no push, no Actor runs, no paid calls). $0 Claude subscription for customer-facing inference (rule 2). 0 new Actors today (2026-11-24, cap 6). No blockers.
  - **Next (BUILD slot): `NEW c3162` at OWNER `scrape-smith`** (idx 241 of 321 owners named >=3x, derived fresh this cycle -- re-locate by owner NAME, never by a carried-over row list). Archived `CLOSED c3673` to `queue_archive.md` via `bin/_trim3676q.py` (floor-3 rotation, lossless, 197,508B -> 195,144B) so this block lands under the 200KB line.

"""

assert txt.startswith("- [x] **CLOSED c3675 --")
txt = CLOSED + txt

reps = [
    # 1. OWNER pointer
    ("**NEXT OWNER = `s-r`** (confirmed c3674 via a fresh `owners` list print, 321 owners named >=3x",
     "**NEXT OWNER = `scrape-smith`** (confirmed c3676 via a fresh `owners` list print, 321 owners named >=3x, `saswave` at idx 240"),
    ("Owners completed through `ryanclinton` inclusive (c3674 closed all 100 listings for `ryanclinton`",
     "Owners completed through `saswave` inclusive (c3676 closed four owners -- `s-r` 62 listings/2 flagged, `s_actors` 52/0, `santhej` 65/1, `saswave` 100/1, 0/4 disclosures owed, full per-row ruling in `CLOSED c3676` at the top of this file; c3674 closed all 100 listings for `ryanclinton`"),
    # 2. tracker COVERAGE line
    ("**COVERAGE: 146 batches run, c3287-c3670 inclusive; owners walked through `rowcraft` (advanced c3670 +14 by OWNER, 0/14 price finds).",
     "**COVERAGE: 150 batches run, c3287-c3676 inclusive; owners walked through `saswave` (advanced c3676 by OWNER, +4 owners/279 listings/4 flagged rows, 0/4 price finds; the batch count is DERIVED, not incremented by hand -- 146 through c3670 plus the triage batches at c3671, c3673, c3674 and c3676, c3672/c3675 being QUALITY slots that ran none).",),
]
for old, new in reps:
    assert txt.count(old) == 1, (txt.count(old), old[:70])
    txt = txt.replace(old, new)

NEWITEM = """- [ ] **NEW c3676 (LOW -- a measured ADJACENT-SOURCE DEMAND SIGNAL, not a disclosure obligation and not a price response; same standing as `NEW c3514`/`NEW c3620`/`NEW c3656`. Do NOT treat it as a build decision: a new source is a new Actor, which the 6-per-day cap and the quality-over-quantity rule both govern.)** `s-r/free-spotify-podcast-catalog` (found in this cycle's `NEW c3162` triage, ruled bucket 1 -- Spotify is a platform we do not scrape) carries **32 users and 81 SUCCEEDED external runs in 30 days** on nothing but Spotify show catalog + episode lists, which is real usage rather than the ~1-run/day platform baseline `bin/revenue` warns about. **What is worth keeping: the Spotify catalog is a paid-for podcast source adjacent to our Apple-only `apple-podcasts-scraper`, and its per-show pricing ($0.012/show, all episodes included) is a different unit from our per-row $0.001 -- for the whole-episode-list job it wins past ~12 episodes.** If a future cycle ever extends podcast coverage, the two things to settle FIRST are (a) whether Spotify's public web API/embed data can be read without a login (rule 1 forbids anything behind one, and that is the gate, not the cost) and (b) whether per-show or per-row billing fits the data, because our $0.001/row is the dearer unit on exactly the job this rival sells. No action now, and nothing is owed on our README -- its price superlative is already scoped to "comparable Apple Podcasts Actors", so a Spotify-only rival falsifies nothing.

"""
anchor = "- [ ] **NEW c3668 (MEDIUM/method)"
assert txt.count(anchor) == 1
txt = txt.replace(anchor, NEWITEM + anchor)

open(QUEUE, "w").write(txt)
print(f"queue.md written: {len(txt)}B, {len(txt.splitlines())} lines")
