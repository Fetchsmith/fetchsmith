# STATUS (update every cycle)
Updated: 2026-10-08 ~12:10 UTC by cycle 1413 (sonnet-5) — **24 live Actors, $0 revenue, ~$1.20 of $300 spent.**

## Cycle 1413 (2026-10-08, sonnet-5 — QUALITY/GROWTH slot: trimmed STATUS.md/queue.md, well past the 150KB standing threshold)

Took the due QUALITY/GROWTH slot (1412's handoff said 1413 should, not a third audit). Checked file
sizes first per the cycle-1219 standing rule and found both tracking files badly overdue: `STATUS.md`
had reached **406,770 bytes** (101 cycle entries, cycles 1304-1412) and `tasks/queue.md` **332,235
bytes** — both >2x the 150KB trim line, and large enough that the `Read` tool now hard-errors on them
(256KB max), meaning every future cycle reading this file for context was already degraded before
doing any real work.

**Trimmed both, verified lossless.** `STATUS.md`: moved cycles 1304-1399 (2,687 lines) into
`state/STATUS_ARCHIVE.md` under a new `## Archived 2026-10-08T12:01:51Z by cycle 1413` header,
prepended ahead of the existing archive content; live file now holds cycles 1400-1412 at **60,205
bytes**. `tasks/queue.md`: per the cycle-1225 standing note that superseded `NEXT-CYCLE` blocks have
**zero** remaining operational value once replaced (durable lessons belong in LEARNINGS.md, not here),
moved every `## Superseded:` block (lines 91-3824, all history back to ~cycle 780) into
`tasks/queue_archive.md`, leaving just the one live `NEXT-CYCLE` block at **8,029 bytes**. Verified
losslessness both ways by `cat`-ing the split files back together and diffing against a pre-edit
backup — byte-identical for both STATUS.md and queue.md. `notes/LEARNINGS.md` is also oversized
(792,264 bytes, 303 cycle entries) but is a different shape (lessons, not supersede-based) and needs
more careful curation than a mechanical split — left as a follow-up, not attempted this cycle.

**Also ran the dev.to comment poll** (cheap, high-yield per LEARNINGS cycle 641/863): 15 published
articles, 3 have comments (4809157: 1, 4689167: 3, 4627420: 1), all top-level with no reply posted
yet. One (`dododata` on 4689167) was already measured and deliberately left unreplied in
LEARNINGS_ARCHIVE:3516 (their fix doesn't apply to our already-correct stat). The other 3
(`shieldxbot`/4809157, `launchgatecheck` + `nikhil_patel_10`/4689167, `raknaos`/4627420) are generic
promotional-sounding praise from oddly-branded accounts (SaaS-product-like usernames) — plausible
engagement-farming, not evaluated deeply this cycle for time; flagged in queue.md rather than replied
to without checking whether a reply is actually warranted.

**Verified:** services (web/mail/caddy) active, site 200 on `/` and `/tools`. Revenue unchanged: $0,
44 users, 608 runs30d (604 ext_ok/4 ext_bad), 0 bookmarks/reviews. `bin/traffic`: `/tools` 7,
`/pricing` 3, `/contact` 10, `/docs` 5 — still far below the >100/day Polar gate, not raised. Inbox:
9 msgs, all pre-vetted noise (2 SEO pitches from `searchindex.pro`, 5 JP/CA/IT contact-form
autoreplies, 1 DMARC report, 1 bounce), nothing actionable, no owner email sent. $0 spent. No Actor
code touched, so no build/smoke run was needed; regular `competitor_audit` rotation untouched this
cycle, resumes next cycle exactly where 1412 left it.

## Cycle 1412 (2026-10-08, opus-5 — regular `competitor_audit` rotation on fleet-oldest `google-play-reviews-scraper`)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until **2026-10-20**, so the target was `google-play-reviews-scraper` (1378 → 1412).
**This audit produced the largest batch of undercutters any cycle on this fleet has found — because
it finally priced the 1-and-2-user tail that cycles 1338 and 1378 had both logged as a known
unpriced gap.** Own price re-verified live first: flat $0.0001/result, no start fee, no tiers, 0
drift. `niche-size` 467 seen / 268 matched (flat vs 467/271 at 1378). `niche-unnamed`: **224 unnamed
of 268, but only 62 clear the ≥3-user floor** — the ≥3u-only method prior cycles used was
structurally blind to 162 listings. Live-priced all 224 individually, 0 unresolvable.

**Fifteen previously-unnamed effective undercutters, and every single one sits at 1–2 users** (all 15
inside the skipped tail). Six carry **no start fee**, so they beat us at every run size with no
crossover in our favour: `scrapersdelight/google-play-reviews-scraper` at **$0.000045** (55% under
us, the cheapest honest per-review price in the niche), `steadyscrape/…` and `pappy-dev/google-play-
reviews` at $0.00005, `realai_pl/google-play-reviews-fast` and `peerless_columbine/…-api` at
$0.00008, `cheapapi/app-store-google-play-scraper` at $0.00009. Nine more sit behind only a $0.00005
(Apify default) or $0.0001 start fee — crossover **2–5 reviews**, below any real run, so reported as
plain undercutters, including `cirkit/google-play-store-scraper` whose $0.00008 review event is *not*
its Store-displayed primary ($0.0006/app record) and so was invisible to any headline comparison.
Two genuine crossovers remain: `superslowsloth` (67 reviews) and `tactful_anvil` ($0.00008 + $0.01
start = **500 reviews**, the one case where we are still the cheaper choice for small/medium pulls).

**Closed `0-TODO-h1392-runfee-in-batch-copies`' leg for the script in use and it paid off the same
cycle:** repointed `bin/_batch_price_gprs.py` at `bin/_apify_get.py` (its old unguarded `.json()`
turned a transient blip into `error: unresolvable` — a rival silently dropping out of the
comparison) and added `cps.runfee_price`, which automatically surfaced `second_coming/app-store-
review-analyzer`: flat **$0.02/scan**, no per-row event at all, crossover ~200 reviews. That is the
**second** run-fee-only rival from this same owner after `brand-mention-monitor` at 1384/1392.

**One ruled out, and it breaks an existing diagnostic tell:** `listless_adzuki/app-store-review-
scraper` shows $0.00001/row, but that is Apify's generic `apify-default-dataset-item` platform
charge sitting beside a named `review-result` event at $0.004 (40× us) — the same trap as `johnvc`
at 1378, **except that here the generic platform event is the one flagged `isPrimaryEvent`**. So
`primary` is not a reliable guide to what a rival bills. Written up as **`h1412` in LEARNINGS**,
whose generalizable rule is: **never apply a user-count floor in a niche with >100 matched listings
or an own-price at the compute floor** — in a commodity niche the only way a new entrant wins a
first customer is to launch *underneath* the incumbent price, so price aggression and low user
count are positively correlated, and a user-count floor filters out exactly the population it most
needs to see. 224 listings cost ~4 min of read-only GETs and $0.

**No claim was inverted** — this README already stated "we are not the cheapest per-review Actor in
this niche, and we are not even close to it", which is now far better evidenced. Added 2 dated
paragraphs, raised the running undercutter total 10 → 25, and replaced the stale "long tail of
1-and-2-user listings we have not priced one by one" caveat with the closed result.

**Verified:** build 0.1.69 pushed (package.json 0.1.18→0.1.19); live README confirmed via `GET
/v2/actor-builds/<buildId>` byte-identical to local (41,628 == 41,628) and containing all 6 probed
new strings — not the CDN-cached Store page, per the standing rule. `check-store-index` 0 stale,
index reindexed 11:39:05 vs build 11:39:27. `check-competitor-claims` fleet-wide 460 claims (up from
450 — the new handles) / **0 stale on this Actor** / 171 paragraphs / 0 undated. `check-pricing`
24/29/0, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0, `check-charges` 24/24,
`check-readme-samples` 35 blocks / 82 bullets / 0 drift — all identical to recorded baselines.
`_batch_price_gprs.py` `py_compile` clean. Services (web/mail/caddy) active, site 200 on `/` and
`/tools/google-play-reviews-scraper`. Revenue unchanged: $0, 44 users, 606 runs30d, 0
bookmarks/reviews. `bin/traffic` `/pricing` 3, `/tools` 7 — far below the >100/day gate, Polar NOT
raised. Inbox 10 msgs, all pre-vetted noise, nothing actionable, no owner email. $0 spent.
`audit_dates.json`'s `google-play-reviews-scraper.competitor_audit` bumped 1378 → 1412 with a new
note prepended (old chain preserved).

**Next cycle:** **a QUALITY/GROWTH slot is due (~1413)** — 1411 took the last one and 1412 was a
regular audit, so 1413 should take it rather than a third audit in a row. Then apply h1412 to the
rotation: the ≥3u floor was standard before ~1410, so the same blind spot plausibly hides
undercutters in the other large commodity niches — `hacker-news-scraper` (~248 matched) and
`remote-jobs-scraper` (~240) are the obvious candidates, worth prioritising over strict
oldest-first; price the FULL unnamed cohort from now on. Otherwise rotation resumes at fleet-oldest
(re-derive fresh; currently `apple-podcasts-scraper`, 1379, which also has an open
`0-TODO-h1400-unpromoted-niches` leg and a stale `spokentext` count to fix inside that audit).
Backlog: `0-TODO-h1392-runfee-in-batch-copies` (**24 of 26 copies left**), `0-TODO-h1368-newly-
visible-stale`, `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`.

## Cycle 1411 (2026-10-08, sonnet-5 — QUALITY/GROWTH slot, closed `0-TODO-h1396-ted-invisible-60`)

Closed the fleet's highest-priority open tool TODO: `bin/_batch_price_ted.py`'s cycle-1348
`eu-ted-tenders-scraper` audit had reported "no undercutters" over a cohort where **60 of 151
listings carried `tiers: {}`** from a since-fixed flat-only pricing-reader bug, so that
conclusion was unsupported for those 60. Extracted the exact 60 handles (matching
`bin/_unit_price_selftest.py`'s own lost-key logic), re-priced them live via the
already-repointed script, and merged the fresh data back into the full 151-row cohort —
`_unit_price_selftest.py` on that file now reports **0 unreplayable (was 60)**.

**Found and disclosed 2 genuine, previously-invisible undercutters:** `deriverge/public-
tenders-scraper` (2 users, explicitly reads TED + UK Find a Tender + Contracts Finder) is
tiered **$0.001 (Free) → $0.0005 (Gold+)** against our flat $0.0015, cheaper at *every* tier and
run size, no start fee. `humble-echidna/eu-ted-tenders` (3 users, same TED+UK scope) is tiered
$0.002 → **$0.0014 (Gold+)**, a partial undercut from Gold up. A third, `andok/eu-tenders-
scraper`, undercuts only on its hardest-to-reach Diamond tier and its $0.0028 start fee pushes
the real crossover to ~28 notices/run — noted but called immaterial. 5 of the 60 confirmed OUT
OF SCOPE (single-country portals, not TED); the rest price at or above our rate. Added as a new
"Twelfth sweep" README paragraph following the page's own established convention.

Also ran `_unit_price_selftest.py` with no args across all 29 saved cohorts (the TODO's own
suggested follow-up): **0 unreplayable fleet-wide** — `ted` was the only cohort with the
tiers-lost bug, confirming the cycle-1396 repoint already closed it everywhere else it could
recur. 30 MOVED verdicts turned up in 11 other, mostly FLAT-schema cohorts — expected per the
selftest's own documented FLAT-schema limitation (can't see a tier ladder), not a confirmed bug,
left for each Actor's next regular audit rather than chased now.

**Verified:** own price re-read live first (flat $0.0015/result, no start fee, 0 drift). Build
pushed (`eu-ted-tenders-scraper` package.json 0.1.10→0.1.11, Apify build 0.1.64); live README
confirmed via `GET /v2/actor-builds/<buildId>` (not the CDN-cached Store page) to contain the
new paragraph and both new handles. Fleet-wide `check-pricing` 24/29/0,
`check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0, `check-charges` 24/24 all
clean. `check-competitor-claims`: 450 claims/5 stale/1 unresolvable, **0 of the 5 on this
Actor** — the 5 are pre-existing 1-3-user drift on 4 unrelated Actors, left for opportunistic
fixing. Services (web/mail/caddy) active, site 200 on `/` and `/tools/eu-ted-tenders-scraper`.
Revenue unchanged: $0, 44 users, 606 runs30d, 0 bookmarks/reviews. `audit_dates.json`'s
`eu-ted-tenders-scraper.competitor_audit` bumped 1387→1411 with a new note prepended (old chain
preserved — this was a targeted TODO fix, not a fresh niche-size/niche-unnamed sweep, so the
regular rotation audit is still due separately). Inbox: 8 msgs, all pre-vetted noise, nothing
actionable, no owner email. $0 spent.

**Next cycle:** regular `competitor_audit` rotation resumes — re-derive fleet-oldest fresh from
`audit_dates.json` (currently `apple-podcasts-scraper`, 1379). Next QUALITY/GROWTH slot due
~1414. Remaining backlog: `0-TODO-h1392-runfee-in-batch-copies`, `0-TODO-h1368-newly-visible-
stale`, `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`.

## Cycle 1410 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on fleet-oldest `sec-insider-trades-scraper`)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20, so `sec-insider-trades-scraper` (1376) was next.

**Audit found a real, if small, disclosure gap — not a flat "clean negative."** `niche-size`:
256 seen / 108 matched (up from 254/108 at 1376, no change in matched count). `niche-unnamed`: 46
unnamed (down from 55, README now names 64 vs 53). Own price re-verified live first: flat
**$0.0018/`result`, no start fee**, unchanged. Only `sutraflow/sec-insider-trading-signals` (3
users) cleared the usual ≥3-user floor ($0.01 start + $0.01/txn — dearer, no undercut). Per the
standing full-cohort rule for this niche, live-priced the entire remaining 45-listing tail (0-1
users each) anyway: **0 new per-row undercutters**, modal price ~$0.003-$0.005/row, consistent
with every prior sweep.

**The real find: two volume-dependent near-misses, same class as the README's existing
per-filing break-even paragraphs, just on the per-search/per-ticker side instead.**
`m_ctim/insider-trading-alert` charges one flat `insider-search` fee ($0.007 FREE → $0.0055
DIAMOND) regardless of how many transactions a search returns — breaks even against our
$0.0018/row at **3.1-3.9 rows**, below the 8 rows this README's own Apple sample already pulled
from one accession. `zinin/insider-trading-tracker` charges per ticker delivered ($0.005 FREE →
$0.004 DIAMOND) covering that ticker's "bounded Form 3/4/5 activity" — breaks even at **2.2-2.8
rows/ticker**, again below Apple's 8 (though above MSFT/JPM's 1-row-per-filing sample). Neither
is a confirmed undercut (both 1 user, neither's listing claims the code-decode/signed-value/flag
fidelity this Actor leads on), but both price per-search/per-ticker rather than per-row, so a
buyer pulling a high-activity issuer would pay less there than here. Added as a new paragraph
disclosing both with their break-evens, following the README's own established convention for
this exact shape.

**Verified, caught and fixed my own slip:** `check-competitor-claims` (run after the first push)
flagged my own new paragraph — I'd written `sutraflow` as "2 users" when the live count was 3.
Fixed and re-pushed (build 0.1.38 → 0.1.39). The same check run also caught an unrelated
pre-existing stale claim on `app-store-reviews-scraper` (`apihq/app-store-reviews-scraper` stated
as 25 users, live 28) — fixed and pushed that Actor's build too (0.1.21 → 0.1.22). Live build
readme confirmed to contain the new text (`httpx`/API read of the `latest` build, not the
CDN-cached Store page). Fleet-wide `check-pricing` 24/29/0, `check-charges` 24/24,
`check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0, `check-readme-samples` 0 drift
— all clean, all identical to prior baselines. `check-competitor-claims` fleet-wide now 447
claims/**1 stale** (the pre-existing `apple-podcasts-scraper`→`spokentext` 2-vs-3-user drift,
found but left — ordinary single-user churn outside this cycle's scope, not chased)/1
unresolvable (the long-standing `scraper_guru` case) + 170 paragraphs/0 undated. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; site 200 on `/` and
`/tools/sec-insider-trades-scraper`. Revenue unchanged: $0, 44 users, 606 runs30d, 0
bookmarks/reviews. `bin/traffic`: `/pricing` 3, `/tools` 7 — below the >100/day Polar gate, so
per owner instructions Polar not raised. Inbox: 10 messages, all pre-vetted noise (2x
searchindex.pro SEO pitch, JP/CA/IT contact-form autoreplies, 1 DMARC report, 1 bounce) — nothing
actionable, no owner email sent. `audit_dates.json`'s `sec-insider-trades-scraper.competitor_audit`
bumped 1376 → 1410 with a new note prepended (old chain preserved). $0 spent.

**NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes — re-derive fleet-oldest fresh
from `state/audit_dates.json`, do not trust this guess: as of this edit it is
`google-play-reviews-scraper` (1378), then `apple-podcasts-scraper` (1379). `scholarship-scraper`
(1274) stays skip-listed until 2026-10-20. (2) `0-TODO-h1400-unpromoted-niches` is still **4 of
24** (unchanged this cycle — `sec-insider-trades-scraper` was already promoted into
`TERM_VARIANTS` as of the 1220/1376 work, this cycle just re-ran it): `apple-podcasts-scraper`,
`hacker-news-scraper`, `scholarship-scraper`, `us-federal-awards-scraper`. (3) The incidental
`apple-podcasts-scraper`→`spokentext` 2-vs-3-user staleness found by this cycle's
`check-competitor-claims` run is trivial and low-priority — fix opportunistically whenever that
Actor is next touched, not worth a dedicated cycle. (4) `ats-jobs-scraper`'s unread tail (~768 of
813 matched) is still open. (5) Backlog unchanged, priority order:
`0-TODO-h1396-ted-invisible-60`, `0-TODO-h1392-runfee-in-batch-copies`,
`0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
`0-TODO-h1346-fleet-wide-sub20-counts`. (6) A QUALITY/GROWTH slot is due ~1411 (1408 took the
last one, 1409/1410 were both regular audits).

## Cycle 1409 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on fleet-oldest `shopify-products-scraper`, also closed that Actor's leg of `0-TODO-h1400-unpromoted-niches`)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20, so `shopify-products-scraper` (1372) was next.

**Audit: clean negative.** `niche-size`/`niche-unnamed` (old 11-term auto sweep): 396 seen / 145
matched / 60 unnamed (README already names 106 handles). Only 4 unnamed listings cleared the
usual >=3-user noise floor — `hipersoft/shopify-product-scraper`, `jamhimself/shopify-products-
scraper`, `catalini82/shopify-price-restock-monitor`, `frabi/shopify-store-intelligence-scraper`
— all live-priced via `GET /v2/acts/<owner>~<slug>`, all dearer than our $0.001→$0.00085 tiered
rate at every tier (hipersoft $0.002→$0.001 tiered + a $0.001/store-page fee + $0.00005 start;
jamhimself flat $0.004/product; catalini82 flat $0.0015/result; frabi flat $0.002/product-
scraped). No undercutter, no README/build change needed.

**Also closed this Actor's leg of `0-TODO-h1400-unpromoted-niches` (now 4 of 24).** Promoted
`shopify-products-scraper` into `bin/niche-size`'s `TERM_VARIANTS` — a THIRD "no rescue needed"
instance after `nih-reporter-scraper` (1404) and `google-news-scraper` (1405): the base phrase
"shopify products" already stems to match "shopify product" and the matcher's name+title+
description blob already catches no-space/reworded titles. Went further than the previous two
promotions by actually testing 6 extra hand-picked terms from this niche's own cycle-1144
vocabulary (`shopify scraper`, `shopify store products`, `shopify catalog`, `shopify store`,
`shopify product`, `shopify ecommerce`) against the live Store search — they widened `seen` from
396 to 511 but added only 4 matches, 3 of them tiny (0-3 users) and dearer, and the 4th a **false
positive**: `mighty_monk/shopify-reviews-scraper` (65 users) scrapes Shopify **review widgets**
(Judge.me/Loox/Stamped/Yotpo/Okendo), not the product catalog — it only matched because its own
description happens to say "Shopify product pages". The real `mighty_monk` catalog rival
(`shopify-product-scraper`) is already named in the README. Kept the extra terms in the
hand-curated list anyway (documented, zero cost) but made **no README change** from them —
nothing real to disclose. `niche-size` now reports 148 matched under the 17-term hand-curated
list vs 145 under the old 11-term auto sweep; the 3-listing delta is exactly the 3 tiny dearer
rivals, not a coverage fix.

**Verified:** `bin/niche-size` `py_compile` clean; re-ran live post-edit and got 148 matched
(hand-curated, 17 queries) vs 145 pre-edit (auto-generated, 11 queries) — consistent with the
analysis above; `niche-unnamed` re-run post-edit reproduces the same top line
(`mighty_monk/shopify-reviews-scraper` at 63u, the false positive, then the 4 live-priced >=3u
listings). Fleet-wide `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth`
23/0, `check-own-price-freshness` 24/0 — all clean, all identical to prior baselines (no
regression from the `TERM_VARIANTS` edit). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; site 200 on `/` and `/tools`. Revenue unchanged: $0, 44 users, 606 runs30d,
0 bookmarks/reviews. Inbox: 9 messages, all pre-vetted noise (2x searchindex.pro SEO pitch, JP/
CA/IT contact-form autoreplies, 1 DMARC report) — nothing actionable, no owner email, no reply
sent. `audit_dates.json`'s `shopify-products-scraper.competitor_audit` bumped 1372 → 1409 with a
new note prepended (old chain preserved). No README/Actor build pushed this cycle (no code/
copy change was warranted — only `bin/niche-size` changed), $0 spent.

**NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes — re-derive fleet-oldest fresh
from `state/audit_dates.json`, do not trust this guess: as of this edit it is
`sec-insider-trades-scraper` (1376), then `google-play-reviews-scraper` (1378).
`scholarship-scraper` (1274) stays skip-listed until 2026-10-20. (2)
`0-TODO-h1400-unpromoted-niches` is now **4 of 24**: `apple-podcasts-scraper`,
`hacker-news-scraper`, `scholarship-scraper`, `us-federal-awards-scraper` — expect "no rescue
needed" to remain the common outcome (three consecutive instances now), but still worth the
`niche-unnamed` check each time since the *disclosure* side (new live-priced rivals) is the real
value, not the promotion itself. (3) `ats-jobs-scraper`'s unread tail (~768 of 813 matched) is
still open. (4) Backlog unchanged, priority order: `0-TODO-h1396-ted-invisible-60`,
`0-TODO-h1392-runfee-in-batch-copies`, `0-TODO-h1368-newly-visible-stale`,
`0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (5) A QUALITY/GROWTH
slot is due ~1411 (1408 took the last one).

## Cycle 1408 (2026-10-08, opus-5 — QUALITY/GROWTH slot: closed the 4-cycle `_apify_get` repoint, which surfaced a fleet-wide FALSE POSITIVE in `check-store-index`)

Took the due QUALITY/GROWTH slot (1405 took the last one). Closed queue item (4), the
`_apify_get` repoint carried over unfinished from 1404/1405/1406/1407 — and finishing it
exposed a real bug that had been hiding behind a never-run check.

**1. `_apify_get` repoint — DONE, item (4) closed.**
- `check-store-index`: all 3 Apify call sites repointed. Each `.json()["data"]` could raise
  `JSONDecodeError` *and* `KeyError`; more importantly each needed a *different* policy, not a
  blanket guard: the `?my=true` fleet listing is the tool's **denominator**, so a failure there
  now `sys.exit`s FATAL (an empty fleet would otherwise have printed a confident "0 stale");
  a 404/403 on a per-Actor record we just read out of our own listing is **not** a normal
  absence, so it prints `LIVE RECORD UNREADABLE` and joins a new `unknown` list; an unreadable
  build prints `readme=UNKNOWN(status)`. A new `WARNING: INCOMPLETE CHECK` line names every
  uncompared Actor (the cycle-1404 completeness rule).
- `check-disclosure`: the handoff's warning was right and understated — **both** call sites are
  dev.to, not Apify (lines 78 and 83). Repointed anyway (`get_json` is host-agnostic; only the
  `FINAL_MISSING`/`RETRY_STATUS` split is Apify-tuned, and that split is correct for dev.to too).
  The crash was not the real bug: one `try/except` wrapped the *whole* leg, so a blip on any
  single article aborted the rest while printing only "SKIPPED", and the verdict line
  "0 missing disclosure(s)" + exit 0 looked identical whether dev.to was fully checked or not
  checked at all. Per-article failures are now counted (`UNCHECKED`), and a
  `COVERAGE INCOMPLETE` line prints beside the verdict. Exit code deliberately stays 0 on an
  unreachable dev.to — offline usability is the documented design intent.

**2. The real find: `check-store-index` was reporting `stale=['readme']` on all 24 Actors, and
every one was a FALSE POSITIVE.** Apify **removed the `readme` attribute from the
`prod_PUBLIC_STORE` index** (hits now carry `readmeSummary`, an ~285-word AI-generated summary).
The cycle-972 compare did `norm(hit.get("readme")) != norm(bmd)` — `.get` on a *missing* key gave
`None`, `norm` made it `""`, and the tool diffed that against a 6,612-word build readme.
Guaranteed mismatch, every Actor, permanently. **Confirmed three ways:** dumped a hit's keys (no
`readme` key at all, `readmeSummary` present); `-v` showed "indexed 0 words vs build 6612 words";
and **re-ran the pre-edit file via `git show HEAD:bin/check-store-index`, which produced the
identical 24/24 — proving the bug predated this cycle's edits and that the repoint is
behaviour-neutral.** What exposed it was the contradiction with `LEARNINGS:168` ("fleet run after
the fix: 0 stale") — a fleet-wide *uniform* failure is nearly always the measurement, not the
fleet. `readmeSummary` is NOT substitutable (derived prose; word-diffing it is wrong by
construction), so the fix **reports the lost coverage** rather than retargeting the check at the
nearest-looking field to keep a green tick. Fleet now reads **0 stale / 24** with an explicit
`readme NOT CHECKED for 24 Actor(s)` note. This matters beyond cosmetics: `LEARNINGS:168` makes
"run `check-store-index <slug>` after every readme change" a standing rule and every h904
readme-proximity measurement is gated on "0 stale" — that gate was unsatisfiable.

**Verified (not assumed):** both tools `py_compile` clean; **fault-injected both new guards** —
a bogus token reproduces `FATAL: could not list our own Actors (status=401)` with **script exit
1**, and a deliberately-wrong slug reproduces `LIVE RECORD UNREADABLE (status=404)` plus the
`WARNING: INCOMPLETE CHECK` naming all 24. Live runs: `check-disclosure` 53 site posts + 15
dev.to articles / 0 missing / no COVERAGE INCOMPLETE line; `check-store-index` 0 stale / 24.
Standing checks all match recorded baselines exactly — `check-pricing` 24/29/0, `check-charges`
24/24, `check-own-price-freshness` 24/0, `check-competitor-claims` 446/0 stale + the 1
pre-existing unresolvable (`scraper_guru` in substack-scraper's README, unrelated) + 169/0
undated. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; site 200 on `/` and
`/tools`. Revenue unchanged: **$0, 44 users, 606 runs30d, 0 bookmarks / 0 reviews.** `bin/traffic`
checked for the Polar gate: `/pricing` 3 and `/tools` 7 hits — far below >100/day, so per owner
instructions Polar was **not** raised. Inbox: 10 messages, all the same pre-vetted noise (2x
searchindex.pro SEO pitch, JP/CA/IT contact-form autoreplies, 1 DMARC report, 1 bounce) —
nothing actionable, no owner email, no reply sent. **No README/Actor change, no build pushed,
$0 spent.** No `competitor_audit` ran (QUALITY slot), so `audit_dates.json` is untouched by
design.

**Deliberately NOT done:** the `shopify-products-scraper` leg of
`0-TODO-h1400-unpromoted-niches`. The `_apify_get` repoint was the older, 4-cycle-deferred item
and it opened into a live false-positive worth finishing properly; the niche leg is unblocked and
carried forward intact.

## Cycle 1407 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on re-derived fleet-oldest `us-federal-awards-scraper`)

Re-derived fleet-oldest fresh from `state/audit_dates.json`: `scholarship-scraper` (1274) still
skip-listed until 2026-10-20; next is `us-federal-awards-scraper` (1369).

**Clean negative — no new undercutter, no drift, no README/build change.** `niche-size`/
`niche-unnamed`: 147 seen / 126 matched / 40 unnamed (up from 145/125/38 at cycle 1369 — normal
churn in a heavily-templated niche). The unnamed tail's `>=3u` cut is thin (3 listings): 2 of
those 3 (`nasasurfer`, `carranza-tech`) are already covered by the README's bare-handle "tie our
Free tier" sentence, and the third (`crawlerbros/usaspending-scraper`, plus its sibling listing
`crawlerbros/usa-spending-federal-data`) ties $0.005 FREE → $0.003 GOLD+ + a $0.005 start fee —
dearer than our $0.004→$0.0025 ladder at every tier. Live-priced a 30-listing sample of the 2u
tail too: everything resolvable priced at $0.004+. The one listing that looked like a steal,
`datasignalslab/gov-contract-awards-monitor` ($0.00001 on the default dataset-item event), is
the same misleadingly-cheap-default-event trap the cycle-1218 note on this same Actor already
flagged on `omarchydev` — its real `isPrimaryEvent` is `company-analyzed` at $0.02, a different
shape (per-company risk score, not bulk award export), correctly left unnamed. Spot-checked 8
headline named rivals (`parseforge`, `benthepythondev`, `ryanclinton`, `copious_atoll`,
`fortuitous_pirate`, `pink_comic`, `jungle_synthesizer/samgov-scraper`, `datamule`) for drift —
every price that resolved matched the README exactly. Per the 1311/1353/1369 "nothing changed"
precedent, README left untouched, no build pushed. `audit_dates.json`'s
`us-federal-awards-scraper.competitor_audit` bumped 1369 → 1407 with a new note prepended (old
chain preserved).

- Verified fleet-wide: `check-competitor-claims` 446/0 stale + 1 pre-existing unresolvable
  (`substack_guru`, unrelated) + 169/0 undated; `check-price-superiority` 1673/557/**0
  undisclosed** (18 run-fee-only rivals held out, 0 undisclosed); `check-pricing` 24/29/0;
  `check-charges` 24/24 — all clean, all identical to the 1404-1406 baselines (no regression).
  Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, site 200 on `/` and
  `/tools`.
- `bin/traffic` checked for the Polar-checkout gate: no sustained >100/day hits to `/pricing` or
  `/tools` — per owner instructions, still do NOT raise Polar.
- Demand unchanged: revenue $0, 44 users, 606 runs30d, 0 bookmarks/reviews. Inbox: 9 messages,
  same pre-vetted noise (2x searchindex.pro SEO pitch, JP/CA/IT contact-form autoreplies, 1 DMARC
  report, 1 bounce) — nothing actionable, no owner email.
- Spend: $0 cash, no Actor runs beyond free live-pricing GETs, no build pushed.
- Next cycle resumes the regular `competitor_audit` rotation at the new fleet-oldest unblocked
  Actor — re-derive fresh, expected `shopify-products-scraper` (1372) then
  `sec-insider-trades-scraper` (1376), but VERIFY per the standing process lesson. Next
  QUALITY/GROWTH slot due ~1408.

## Cycle 1406 (2026-10-08, sonnet-5 — regular `competitor_audit` rotation on re-derived fleet-oldest `fec-campaign-finance-scraper`)

Re-derived fleet-oldest unblocked straight from `state/audit_dates.json` (sorted fresh, per the
standing 1403 process lesson) rather than trusting 1405's handoff guess: `fec-campaign-finance-
scraper` (1368), confirmed `scholarship-scraper` (1274) still skip-listed until 2026-10-20.

**Clean for a THIRD consecutive time.** `niche-size`/`niche-unnamed`: 460 seen / 42 matched / 0
unnamed — stable vs 459/42/0 at both cycle 1332 and 1368. Re-priced all 42 named rivals live in
parallel (`bin/_batch_price_fec.py`), then checked for price drift by locating each handle's own
README **paragraph** (blank-line-scoped) rather than a fixed-char window, which bleeds into
neighbouring rivals' numbers — exactly the trap the cycle-1332 note on this same Actor already
flagged. Every in-scope rival's live price matches a dollar figure in its own paragraph within
5%. The one non-match (`nexgendata/lda-lobbying-disclosure-scraper`, live $0.05) is one of the 4
listings this README explicitly excludes as out-of-scope (CA/NY state-level filings, 1 UK
scraper, 5 LDA-lobbying products) and correctly carries no price claim — not drift. **Zero real
price drift; no README/build change needed** (1311/1353 churn precedent). `audit_dates.json`
bumped `fec-campaign-finance-scraper.competitor_audit` 1368 -> 1406 with note prepended, old
chain preserved.

- Verified: fleet-wide `check-price-superiority` 1673/557/**0 undisclosed**,
  `check-competitor-claims` 446/0 stale + 1 pre-existing unresolvable + 169/0 undated,
  `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
  `check-comparison-breadth` 23/0 — all clean, all counts identical to cycles 1404/1405's
  baselines (no silent regression from the 1404 `_apify_get` repoint). Services
  (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, site 200 on `/` and `/tools`.
- `bin/traffic` checked for the Polar-checkout gate: no sustained >100/day hits to `/pricing` or
  `/tools` pages — per owner instructions, still do NOT raise Polar.
- Demand unchanged: revenue $0, 44 users, 606 runs30d, 0 bookmarks/reviews. Inbox: 9 messages,
  all pre-vetted noise (2x searchindex.pro SEO pitch, JP/CA/IT contact-form autoreplies, 1 DMARC
  report, 1 bounce) — nothing actionable, no owner email.
- Spend: $0 cash, no Actor runs beyond free live-pricing GETs, no build pushed.
- Next cycle resumes the regular `competitor_audit` rotation at the new fleet-oldest unblocked
  Actor — re-derive fresh, expected `us-federal-awards-scraper` (1369) then
  `shopify-products-scraper` (1372), but VERIFY per the standing process lesson. Next
  QUALITY/GROWTH slot due ~1408.

## Cycle 1405 (2026-10-08, sonnet-5 — due QUALITY/GROWTH slot; closed the `google-news-scraper` leg of `0-TODO-h1400-unpromoted-niches`, confirming it as the second "no rescue needed" outcome after nih-reporter)

Promoted `google-news-scraper` into `bin/niche-size`'s `TERM_VARIANTS` (its existing 11-term
`auto_variants()` sweep made explicit/hand-curated; no `MATCH_SYNONYMS` needed). Verified live
**before and after**: 389 seen / 232 matched, unchanged — this niche's base phrase "google news"
already is the product's own name (unlike CourtListener/Greenhouse-style niches where the base
phrase was wrong), and the matcher's name+title+description blob already catches no-space
name-field variants (`johnvc/GoogleNewsAPI`) via their spaced title field. Re-ran `niche-unnamed`:
top unnamed is 19u, below the fleet's >=20u disclosure threshold — nothing new for the README.
The niche's two known real gaps (DataForSEO's SERP tool, `simple.actor/google-search`) were found
by hand-reading descriptions in cycles 1260/1303/1347, not by keyword search, and no
`TERM_VARIANTS` entry can recover them — documented in the code comment so no future cycle
re-attempts that rescue. No code/README change, no build, $0 spent. `audit_dates.json`'s
`competitor_audit` bumped 1385 -> 1405 with note prepended (old note preserved). `0-TODO-
h1400-unpromoted-niches` now **5 of 24**: `apple-podcasts-scraper`, `hacker-news-scraper`,
`scholarship-scraper`, `shopify-products-scraper`, `us-federal-awards-scraper`.

- Verified: `bin/niche-size` syntax-checked clean; fleet-wide `check-pricing` 24/29/0 clean
  post-edit. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, site 200.
- Demand unchanged: revenue $0. Inbox: 9 messages, all noise (SEO "get listed" pitches, JP
  contact-form autoreplies/bounce, 1 DMARC report) — nothing actionable, no reply sent.
- Spend: $0 cash, no Actor runs, no build pushed.
- Next cycle resumes the regular `competitor_audit` rotation — re-derive fleet-oldest fresh from
  `state/audit_dates.json`, expected `fec-campaign-finance-scraper` (1368) then
  `us-federal-awards-scraper` (1369), but verify.

## Cycle 1404 (2026-10-08, opus-5 — ran the fleet-oldest `competitor_audit` (`nih-reporter-scraper`), which came back clean for the THIRD time; the real find was a transient-API-failure class that was silently corrupting the checks themselves)

**Audit (`nih-reporter-scraper`, 1366 -> 1404).** Re-derived fleet-oldest fresh from
`state/audit_dates.json` as 1403's handoff insisted (sorted the `competitor_audit` values at
read time rather than trusting a cached ordering — the exact bug 1403 fixed).
`scholarship-scraper` (1274) stays skip-listed until 2026-10-20, so `nih-reporter-scraper`
(1366) was next. `niche-size`: 277 seen / **51 matched**, README claims 51 and MATCHES.
`niche-unnamed`: **0 unnamed of 51**. That is the third consecutive clean sweep (1330, 1366,
1404) with an identical matched count, so README left untouched per the cycle-1353/1311
"date-only bump is churn" precedent. No build pushed, $0 spent.

**First negative result for the ats-jobs/court-records playbook.** Rather than re-confirm a
saturated sweep a fourth time, tested whether the MATCH RULE was under-matching, as it had been
on `ats-jobs-scraper` (200 -> 813 matched) and `court-records-scraper` (4.8x). **It was not.**
Dumped all 226 non-matching seen listings and read the 83 with >=3 users: the high-user
non-matches are noise dragged in by the deliberately wide `research funding` search term —
`apimaestro/linkedin-company-detail` (5,545u), `vulnv/crunchbase-scraper-pro` (484u),
`memo23/crunchbase-scraper` (289u), `datahyena/company-funding-rounds` (133u), Kickstarter
scrapers, and two *crypto* funding-rate Actors (`seralifatih/cex-funding-rate-arbitrage`,
`maximedupre/hyperliquid-funding-rates`). That is exactly why `MATCH_SYNONYMS` is held to the
two proper nouns `nih`/`reporter`: **a wide SEARCH term plus a narrow MATCH rule is the correct
design here, not an oversight.** The one genuinely adjacent cohort is ~25 federal-grant
scrapers on a *different source* (USASpending / Grants.gov / NSF, all at 3 users), and the
README already handles that boundary explicitly in prose — it names and live-prices the
cross-source cases that do reach the sweep (incl. `andrew_avina/sbir-intelligence-mcp` at
$0.0005 on USASpending SBIR data) and states plainly that neither side substitutes for the
other. Those are also the niches of our own `us-federal-awards-scraper`/`grants-gov-scraper`,
so folding them in would double-count. **No `TERM_VARIANTS`/`MATCH_SYNONYMS` change warranted;
the cycle-1140 promotion holds.** Recorded as a negative result so no future cycle re-tests it.

**The real deliverable: `bin/_apify_get.py`, a shared retrying JSON GET (+ 9-case selftest).**
`check-own-price-freshness` died mid-audit with a bare `JSONDecodeError: Expecting value: line
1 column 1 (char 0)` from its unguarded `httpx.get(...).json()`; the identical command seconds
later printed `24 public Actors, 0 flag(s)`. Nothing was wrong with the fleet — the API
returned one non-JSON body. Found **three failure shapes, ranked opposite to how dangerous they
are**: (a) CRASH, 6 tools with unguarded `.json()` — loud but costs a whole rotation when a
cycle writes the check off as "could not be completed", which is literally what the 1366 note on
this same Actor records for `check-price-superiority`; (b) **SILENT SKIP**,
`check-price-superiority:213`'s `... if r.status_code == 200 else None` — looks defensive, is
the worst: a transient 429 made a rival read as "no live record" and vanish from the comparison,
in the one tool whose job is catching a rival cheaper than us and which fires ~1600 GETs through
an 8-thread pool; (c) **SILENT UNDERCOUNT**, `niche-size`'s blanket `except Exception: continue`
— one bad search term dropped its entire 100-listing page while the sweep still printed a
confident "N matched", and `niche-unnamed` execs the same loop, so unnamed rivals went invisible
in the tool built to find them.

Helper retries 429/408/5xx, network errors and 200-with-non-JSON (exponential backoff), and
returns `(None, status)` **immediately without retrying** for 401/403/404/410 — a delisted
rival is a real final answer, and retrying it would make every audit of a niche with one dead
handle pay full backoff. Exhaustion raises a loud `ApifyGetError` naming URL/attempts/last
status, never a silent `None`. **Repointed 5 tools**: `check-own-price-freshness`,
`check-price-superiority`, `check-pricing`, `niche-size`, `niche-unnamed`. The two `niche-*`
tools keep their per-term `except` (an exhausted term must not kill a 7-term sweep) but now
count failures and print `WARNING: INCOMPLETE SWEEP -- N of M search term(s) failed after
retries ... do not record it as an audit result` — because **when a tool's job is
completeness, partial failure has to change the tool's own output, not just stderr.**

**Verified, not assumed.** Selftest PASSes all 9 cases including both real-bug reproductions
(200-non-JSON-then-200, and 429-then-200 proving the rival is retried rather than dropped) and
both 404/403 no-retry cases. Fault-injected `niche-size` against an unresolvable host and
confirmed the INCOMPLETE SWEEP warning fires and names all 7 failed terms (cycle 451's
"prove the check isn't a silent no-op" precedent). Every repointed tool reproduces its recorded
baseline exactly: `check-pricing` 24/29/0, `check-own-price-freshness` 24/0, `niche-size` 277
seen/51 matched, `niche-unnamed` 0 unnamed of 51, and `check-price-superiority` **1673 compared
/ 557 cheaper / 0 undisclosed / 18 run-fee-only, 0 undisclosed (77s)** — up from 1392's
1600/540, which is the right direction: a repoint that dropped rivals would show `compared`
**falling**. `ast.parse` clean on all 6 touched files.

**Also closed by observation:** the 1366 note's open TODO that `check-price-superiority` hangs
with zero output across three attempts — it ran in 77s this cycle, fixed by cycle 1384's
8-thread prefetch + progress line. **Still unguarded (follow-up):** `check-disclosure` (2 sites;
note one is the **dev.to** API, not Apify — re-read `FINAL_MISSING` for that host first) and
`check-store-index` (3 sites, all `.json()["data"]` with no `.get`, so they `KeyError` too).

**Standing checks all clean before finishing:** check-pricing 24/29/0, check-charges 24/24,
check-own-price-freshness 24/0, check-comparison-breadth 23/0, check-competitor-claims 446/0
stale + 1 pre-existing unresolvable (`substack_guru` on substack-scraper) + 169/0 undated,
check-price-superiority 1673/557/0. Services healthy (`fetchsmith-web`, `fetchsmith-mail`,
`caddy` all active; `/` and `/tools` both 200). Revenue unchanged: **$0**, 44 users, 606
runs30d, 0 bookmarks, 0 reviews. Inbox: same pre-vetted noise (searchindex.pro SEO pitch x2,
JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) — nothing actionable, no owner
email sent. $0 spent. `audit_dates.json` confirmed advanced to 1404 **in this same cycle** per
1403's standing process lesson.


## Cycle 1403 (2026-10-08, sonnet-5 — found and fixed a bookkeeping gap, then `competitor_audit`/niche-promotion on `clinicaltrials-scraper`)

Before picking a task, discovered cycle 1401's `ats-jobs-scraper` competitor_audit/TERM_VARIANTS
promotion was never recorded in `state/audit_dates.json` — the file still read `competitor_audit:
1363` despite 1401's STATUS.md entry and git commit clearly describing a full audit. This made
"fleet-oldest unblocked" tracking wrong by a full rotation. Fixed the field (1363 → 1401) with a
note explaining the gap, rather than silently re-auditing an Actor that was already done.

With that corrected, true fleet-oldest unblocked was `clinicaltrials-scraper` (1365) — one of the
7 remaining niches on `0-TODO-h1400-unpromoted-niches`. **Unlike `ats-jobs-scraper`/
`court-records-scraper`, this was NOT a false-clear.** This Actor's own manual `competitor_audit`
history (cycle 1104 onward) already hand-searched "clinical trials"/"clinical trial"/"nct"/
"patient recruitment" every cycle and has the fleet's most thoroughly audited README (40+ named
rivals, daily full-cohort sweeps 2026-10-03 through 2026-10-07) — `bin/niche-size`'s crude
single-word `"clinicaltrials"` base term was just a stale tool, not a stale audit. Promoted it into
`TERM_VARIANTS`/`MATCH_SYNONYMS` anyway (7 search terms, "clinical trials"/"patient recruitment" as
match synonyms) so the tool's own count (124→133 matched, 154 seen) finally matches what the
README already knows, rather than reading as a false "unpromoted" flag in every future queue scan.

Live-verified the promotion surfaced exactly **one** new ≥3-user listing not already named:
`fascinating_lentil/clinical-trials-drug-data-aggregator` — flat $0.002/record + $0.00005
Actor-start fee (pulled live via `GET /v2/acts`, 3 pricingInfos entries read, latest from
2026-07-29, no future-dated record pending), dearer than our $0.0015/study flat with no start fee
at every volume — not an undercutter. Spot-checked the niche's top 3 named rivals
(`parseforge`/`logiover`/`bovi`) directly against the live API: zero price or user-count drift.
Added a dated cycle-update paragraph to the README (matching this Actor's own established style)
documenting both findings. Build **0.1.61** shipped, live README verified via direct `diff` against
the build's `actorDefinition.readme` (byte-length mismatch was just UTF-8 multi-byte chars in
`len()` vs `wc -c` — `diff` itself found zero differences). Ran `check-pricing`/`check-charges`/
`check-competitor-claims`/`check-comparison-breadth` **before** the push per the cycle-1400 lesson:
24/29/0, 24/24, 446/0 stale + 1 pre-existing unresolvable (`substack-scraper`, unrelated) + 169/0
undated, 23/0 narrow — all clean, no second push needed.

Services verified healthy (`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active), site 200 on `/`,
`/tools`, and `/tools/clinicaltrials-scraper`. Revenue unchanged: `bin/revenue` 24 Actors, 44 users,
606 runs30d, 0 bookmarks/reviews, **$0**. Inbox: same pre-vetted noise (2x `searchindex.pro` SEO
pitch, JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) — nothing actionable, no owner
email. **$0 spent.**

**NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at the new fleet-oldest unblocked
Actor, **`nih-reporter-scraper` (1366)** — re-derive from `audit_dates.json` directly, don't trust
a cached ordering (this is exactly the bug just fixed). `scholarship-scraper` (1274) stays
skip-listed until 2026-10-20. (2) `0-TODO-h1400-unpromoted-niches` now **6 of 24 remaining**:
`apple-podcasts-scraper`, `google-news-scraper`, `hacker-news-scraper`, `scholarship-scraper`,
`shopify-products-scraper`, `us-federal-awards-scraper` — do `google-news-scraper` next
(source-named, likely the worst remaining case; note it may turn out like clinicaltrials rather
than like ats-jobs/court-records if its own manual audits already use wide terms — check the
Actor's `audit_dates.json` note history FIRST before assuming it's a false-clear).
(3) **`ats-jobs-scraper`'s own unread tail (~768 of 813 matched listings) is still open** — keep
pricing the top-by-users slice next time this Actor comes up. (4) **New process lesson**: after
any cycle that promotes a niche into `bin/niche-size` or otherwise claims "ran competitor_audit on
X", grep `state/audit_dates.json` for that slug's `competitor_audit` field value in the SAME cycle
to confirm it actually advanced — don't just trust the cycle's own narrative (same class of gap as
the cycle-1399 git-commit miss). (5) Remaining backlog, unchanged, in priority order:
`0-TODO-h1396-ted-invisible-60`, `0-TODO-h1392-runfee-in-batch-copies`,
`0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
`0-TODO-h1346-fleet-wide-sub20-counts`. (6) Next QUALITY/GROWTH slot due ~1405.

## Cycle 1402 (2026-10-08, sonnet-5 — owed QUALITY/GROWTH slot: closed `0-TODO-h1396-repoint-batch-pricers` fleet-wide)

Took the QUALITY/GROWTH slot 1401's handoff flagged as due at ~1402. Closed the tooling-hygiene
backlog item `0-TODO-h1396-repoint-batch-pricers`: repointed the last 7 of the 8 flagged
`bin/_batch_price_*.py` copies (`ted`, `substack`, `tms2`, `ats3`, `ggs2`, `sgos2`, `asr`) to
import the shared `bin/_unit_price.py` and alias `tiers_of`/`unit_price` to it, deleting each
file's own forked copy of those functions. `uktft2` was already done at cycle 1397, so this
closes the backlog item fleet-wide — `grep -rl "def tiers_of\|def unit_price"
bin/_batch_price_*.py` now returns nothing.

**Why it mattered, not just cleanup:** `ted`/`substack`/`tms2`/`ats3`/`ggs2`/`sgos2` classified
start fees purely on `isOneTimeEvent` — missing both the cycle-1388 `apify-actor-start` override
and the cycle-1396 tier-ladder discriminator — so re-running any of them today would still
mis-score a `hipersoft`-shaped rival (its real per-row event flagged `isOneTimeEvent=True` with
a 6-tier ladder) or an unflagged `apify-actor-start` fee as the headline price. `asr` already had
both those fixes (cycle 1350/1388) but not the ladder test. These scripts are historical
one-shots — their `/tmp/<niche>_unnamed_handles.txt` inputs are mostly gone — so the real payoff
is forward-looking: the next audit that copies one of these files now inherits every fix at
once instead of forking a 9th divergent version.

**Verification, no live API calls needed** (tooling hygiene, not a live-accuracy sweep, and no
handles files survive to replay against): `ast.parse` clean on all 7 edited files. Executed each
file's header (the import+alias block, stopped just before the `handles = open(...)` line) under
`venv/bin/python` and confirmed `tiers_of`/`unit_price` are literally bound to
`_unit_price.tiers_of`/`.unit_price` (`is up.unit_price? True` on all 7) and return the correct
`(tiers, key, start_fee, note)` tuple on a synthetic `apify-actor-start` + tiered-row fixture.
`git status --short` after the edits showed only the 7 intended files touched. Deliberately did
**not** treat `bin/_unit_price_selftest.py` as a before/after check for this change — read its
source first and confirmed it replays saved `/tmp/*_prices*.json` cohorts straight through
`_unit_price.py` directly; it never imports or calls into the batch-pricer copies at all, so it
cannot see this migration either way. Its existing MOVED verdicts (`ted_prices.json` 1 moved + 60
unreplayable, `substack_prices.json` 2 moved, `ggs_prices2.json`/`asr_prices.json` 1 moved each)
are the pre-existing live-accuracy fallout already tracked under `0-TODO-h1396-ted-invisible-60`
— unrelated to and unchanged by this cycle's edit.

Committed `63c0c763`. No README/pricing/Actor code changed, so no build pushed, no Actor run, **$0
spent**. Services verified healthy: `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active, `/` and
`/tools` both 200. Revenue/demand unchanged: `bin/revenue` 24 Actors, 44 users, 606 runs30d, 0
bookmarks/reviews, **$0** — far below the >100/day owner-email gate, no owner email sent. Inbox
(`bin/inbox list 10`): same pre-vetted noise classes (two `searchindex.pro` SEO-listing pitches,
JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) — nothing actionable.

**Next cycle:** resume the regular `competitor_audit`/niche-promotion rotation — re-derive
fleet-oldest from `audit_dates.json` directly. Fold in `0-TODO-h1400-unpromoted-niches` (7 left:
`apple-podcasts-scraper`, `clinicaltrials-scraper`, `google-news-scraper`, `hacker-news-scraper`,
`scholarship-scraper`, `shopify-products-scraper`, `us-federal-awards-scraper` — do
`google-news-scraper`/`clinicaltrials-scraper` next, source-named niches are the worst case per
1401's and this cycle's own lesson). `scholarship-scraper` stays skip-listed until 2026-10-20.
Remaining backlog in priority order: `0-TODO-h1396-ted-invisible-60` (now easier to act on since
`_batch_price_ted.py` is repointed — just needs a fresh `/tmp/ted_unnamed_handles.txt` and a live
run), `0-TODO-h1392-runfee-in-batch-copies` (the other ~18 `cps.headline_price`-style copies, a
separate backlog from the 8 just closed), `0-TODO-h1368-newly-visible-stale`,
`0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. Next QUALITY/GROWTH
slot due ~1405 (1402 just took one; 1403/1404 should be regular audit cycles).

## Cycle 1401 (2026-10-08, sonnet-5 — `competitor_audit` on `ats-jobs-scraper`: promoted it into `TERM_VARIANTS`/`MATCH_SYNONYMS`, which surfaced the single biggest listing in the whole niche, 16x bigger than the previous largest, invisible until now)

Picked up the fleet-oldest unblocked Actor (`ats-jobs-scraper`, last audited 1363) and the
highest-priority item on 1400's list in the same move: it was one of the **8 live Actors still
absent from `bin/niche-size`'s `TERM_VARIANTS`**, so every "clean resweep" this niche has recorded
since cycle 1281 (1327, 1363) ran on the bare base phrase `"ats jobs"` plus generic modifiers —
and this niche's own listings almost never write that phrase. They name the platforms instead
("Greenhouse Jobs Scraper", "Workday Job Scraper").

**Promoted with 11 `TERM_VARIANTS` search terms + 11 `MATCH_SYNONYMS` match-forms** (greenhouse,
ashby, lever job, workday jobs, recruitee, workable job, smartrecruiters, applicant tracking
system, multi-ats, career site job, career page job), each earned by a listing the bare phrase
could not see. Matched count jumped from 200 (auto-generated) to **813** — by far the largest
undercount gap measured yet in this fleet (beats court-records-scraper's 4.8x at cycle 1400; this
one went from "biggest rival is 490 users" to "biggest rival is 8,067 users", a listing the whole
audit history never knew existed).

**The finding: `fantastic-jobs/career-site-job-listing-api` (8,067 users, 1,552 new in 30 days) is
the single biggest listing in the entire niche** — 16x bigger than `bovi/greenhouse-lever-ashby-
job-scraper` (499u), which every prior audit called "bigger than every other rival named above
combined." It and 4 sibling listings from the same vendor (`career-site-job-listing-feed` 1,461u,
`greenhouse-jobs-api` 923u, `ashby-jobs-api` 491u, `jobs-scraper` 129u) are all dearer than us at
every tier ($0.012→$0.004 down to $0.0022→$0.001, plus start fees on 2 of the 5) despite the scale
— broader ATS coverage (58 platforms) and AI/LinkedIn enrichment is their pitch, not price.
`piotrv1001/company-career-page-scraper` (453u) covers 8 platforms including Oracle HCM (one more
than our 7), also dearer throughout. Two narrow, real undercutters: `shahidirfan/Workday-Job-
Scraper` (421u) ties our FREE per-row rate but its $0.0005 start fee only lets it win past ~50
jobs/run, dearer on every paid tier; `automation-lab/greenhouse-jobs-scraper` (217u, distinct from
the already-named `automation-lab/multi-ats-jobs-scraper`) only wins on DIAMOND past ~34 jobs/run
(its $0.01 start fee eats the per-row saving below that). A dozen more single-platform Workday/
Greenhouse/Lever specialists surfaced the same way, all dearer at every tier. Live-priced ~45 of
the ~813 matched listings (the biggest-by-users ones); **the long tail (~768 listings) is
unread — queued below, this is not a closed sweep like the smaller niches got.**

README updated (one new dated paragraph, `verified live 2026-10-08`), build **0.1.69** shipped
(pkg 0.1.18→0.1.19), live README verified **byte-identical** (47,202 bytes) via
`taggedBuilds.latest.buildId`. README-only, no source/logic change, so no Actor run was needed.
Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-readme-samples`
35/82/0, `check-comparison-breadth` 23/0, `check-competitor-claims` 446/0 stale + 1 pre-existing
unresolvable (`substack-scraper`, unrelated) + 168/0 undated, `check-own-price-freshness` 24/0,
`check-price-superiority` **1671 compared / 556 cheaper / 0 undisclosed** (up from 1662/556 — the
2 new narrow undercutters read correctly as disclosed via the new paragraph's own prose). 3
services active, 2 site pages spot-checked 200. Revenue unchanged at **$0** (44 users, 606
runs/30d), no owner email warranted, inbox only pre-vetted spam/auto-reply/dmarc noise. **$0
spent.**

**NEXT ACTIONS:** (1) **`ats-jobs-scraper`'s own long tail is now the single biggest open
item**: ~768 of the 813 matched listings are unread. Next time this Actor comes up for audit,
keep pulling the top-by-users slice of the unread tail (next candidates seen this cycle but not
yet priced: `memo23/career-site-ats-jobs-api` family already named, but un-priced others like
single-platform Lever/SmartRecruiters specialists below ~25 users were skipped this cycle for
time). (2) **`0-TODO-h1400-unpromoted-niches` now 7 of 24 remaining** (`apple-podcasts-scraper`,
`clinicaltrials-scraper`, `google-news-scraper`, `hacker-news-scraper`, `scholarship-scraper`,
`shopify-products-scraper`, `us-federal-awards-scraper`) — do `google-news-scraper` and
`clinicaltrials-scraper` next (source-named niches are the worst case, same lesson as this cycle
and court-records). (3) Regular rotation resumes at the fleet-oldest unblocked Actor after this
one. `scholarship-scraper` stays skip-listed until 2026-10-20. (4) Still open, in priority order:
`0-TODO-h1396-ted-invisible-60`, `0-TODO-h1396-repoint-batch-pricers` (3 of ~26 done),
`0-TODO-h1392-runfee-in-batch-copies`, `0-TODO-h1368-newly-visible-stale`,
`0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (5) A QUALITY/GROWTH
slot is due at ~1402.

## Cycle 1400 (2026-10-08, opus-5 — `competitor_audit` on `court-records-scraper`: the niche was 4.8x bigger than every previous sweep reported, with 11 unnamed undercutters)

Ran the fleet-oldest unblocked `competitor_audit` (`court-records-scraper`, 1362 → 1400). It was
the **opposite** of the no-op the last three audits of this niche recorded.

**Root cause: the niche had never been promoted into `bin/niche-size`'s `TERM_VARIANTS`.** Every
sweep since 1280 ran on the bare auto-generated base phrase `"court records"`, returned ~30 matched
/ 0 unnamed, and cycle 1362 wrote that down as *"completeness holds, no new rivals"*. It did not
hold. **This niche does not call itself "court records" — it calls itself CourtListener**; the
single most common title in it is literally "CourtListener Scraper", and the rival that undercuts us
on five of six plan tiers describes itself as "search US case law and court opinions via the free
CourtListener API", never writing the two contiguous words our search depended on.

Promoted it with **20 search terms + 14 `MATCH_SYNONYMS` forms**, each earned by a named listing the
old phrase could not see, with the deliberate exclusions (`court`, `legal` — too broad) documented
in the entry. `niche-size` now reports **682 seen / 144 matched** (was 437/30) and `niche-unnamed`
**107 unnamed** (was 0). **Worst `auto_variants()` understatement measured to date: 4.8x**, beating
federal-register's 24→90 at cycle 1124.

**Priced the full 107-listing tail live** via new `bin/_batch_price_crs.py` — built on the shared
`bin/_unit_price.py` from the start (closing its slice of `0-TODO-h1396-repoint-batch-pricers`
rather than inheriting a half-fixed fork) and extended to record **scheduled future
`pricingInfos`** per the cycle-1260 rule; 0 of the 107 has one pending.

**11 genuine in-scope undercutters, all previously unnamed. 7 beat us at EVERY tier with no paid
Apify plan:** `dami_studio/courtlistener-cases-scraper` ($0.0005/case, **a quarter of our rate**,
but the case index only — no filings, no opinions), `ninhothedev/courtlistener-scraper` ($0.0005),
`grokbob/courtlistener-search-batch-ppe` ($0.00075, opinions-only, $0 on an empty query),
`maximedupre/courtlistener` ($0.0009 over opinions + dockets + oral arguments, one index wider than
ours), `brick_joey_yto/federal-court-monitor` ($0.001), `getascraper/courtlistener-rag-extractor`
($0.00089→$0.00067 **per row, but billed in fixed-token chunks** — ~15x our rate per *opinion*; a
unit trap no price tool we own can see, stated both ways in the README), and
`parseforge/caselaw-access-scraper` (**FREE model, $0**, Caselaw Access Project corpus). **4 cross
under only on paid plans:** `scrapesage/courtlistener-scraper` (ties FREE then $0.0017→$0.0005, 5 of
6 tiers), `hipersoft/courtlistener-scraper` (Silver+), `logiover/courtlistener-scraper` (Gold+),
`parseforge/courtlistener-docket-scraper` (Gold+, queries all 6 CourtListener indexes).

The other ~96 are dearer or at parity (`parseforge`'s ~18 single-purpose CourtListener listings at
$0.004–$0.055, `nexgendata`'s 4 at a flat $0.05–$0.10 = 25–50x) or **out of scope on their live
description, not their title** — non-US case law across BR/IN/UK/FR/ES/NL/EU/RO, different US
datasets (EOIR case status, Doxpop Indiana, Ballotpedia, tax-sale/auction, class actions), and the
non-CourtListener US case-law sources, all dearer (Justia, FindLaw, Google Scholar, SCOTUS-only).
One mixed shape stated exactly: `jungle_synthesizer/google-scholar-case-law-scraper` is
$0.002→$0.0012/row **plus a $0.10 start fee**, so cheaper only past ~125 rows/run at Diamond and
never on Free.

The README's **"What we do not claim"** section was rewritten: **15** listings now beat us somewhere
in the plan range, and it explicitly tells a price-first buyer **not to start here**, naming where
to go instead. Own price re-verified first (`check-own-price-freshness` 24/0, flat $0.002/result,
unchanged).

**Builds 0.1.52 then 0.1.53** (pkg 0.1.16→0.1.18). The re-push was avoidable:
`check-competitor-claims` flagged 2 of the new paragraphs UNDATED *after* the first push — **run
that <1s offline check between the README edit and `apify push`, not after.** Live README verified
byte-identical both times (50,739 then 50,781 bytes) via `taggedBuilds.latest.buildId`. README-only,
no source or logic change, so no Actor run was needed.

**`check-price-superiority` 1662 compared / 556 cheaper / 0 undisclosed** (up from 1626/546 — all 11
new disclosures read correctly). Fleet clean: `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0, `check-readme-samples` 35/82/0, `check-competitor-claims` 438/0
stale + 1 pre-existing unresolvable + 167/0 undated. 3 services active, 4 site pages 200. Revenue
unchanged at **$0** (44 users, 604 runs/30d), no owner email warranted, inbox only pre-vetted
spam/auto-reply/dmarc noise. **$0 spent.**

**Filed `0-TODO-h1400-unpromoted-niches`, the highest-value open item:** 8 of 24 live Actors are
still absent from `TERM_VARIANTS` (`apple-podcasts`, `ats-jobs`, `clinicaltrials`, `google-news`,
`hacker-news`, `scholarship`, `shopify-products`, `us-federal-awards`), so **every "0 unnamed" ever
recorded for those 8 is UNMEASURED, not complete** — the same false clear that hid 11 undercutters
here for three consecutive audits. Promote one per audit cycle, source-named niches first.

