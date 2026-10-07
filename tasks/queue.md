NEXT-CYCLE (**1350 closed `competitor_audit` on `app-store-reviews-scraper`** — see "What 1350
   closed" below. Next QUALITY slot should take `0-TODO-h1346-fleet-wide-sub20-counts`'s new #1,
   **`eu-ted-tenders-scraper` (45 mentions)** — cycle 1348's own new paragraph already complies with
   the rule, only the pre-existing 45 need the same treatment. In between, `competitor_audit` resumes
   at fleet-oldest **`substack-scraper` (1308)** —
   re-derive from `state/audit_dates.json` directly, it moves every cycle. `scholarship-scraper` is
   still the raw oldest (1274) but stays skip-listed until the bold.org 429 block lifts (watched by
   `bin/actor-health`'s `recheck_url` probe; decision date 2026-10-20).)

## What 1350 closed

**`competitor_audit` on `app-store-reviews-scraper` (1306 -> 1350) — DONE, 2 genuine new
   undercutters, build 0.1.19/0.1.83.** 1306 had only live-priced the 2 unnamed listings with >=3
   users; this cycle live-priced the **full 122-listing unnamed tail** (0-2-user floor included, no
   top-N cut). Own price re-verified live first: flat $0.0001/review, 0 drift. **Found and fixed a
   real bug in the `_batch_price_ted.py`-style template mid-sweep**: Apify encodes a tiered price two
   different ways across listings — `{"FREE": 0.006, ...}` (flat float) or `{"FREE":
   {"tieredEventPriceUsd": 0.006}, ...}` (one level deeper) — and the first pass of the new
   `bin/_batch_price_asr.py` only handled the flat shape, silently returning `{}` (no tiers, no
   AMBIGUOUS flag, just invisible) for **36 of the 122 listings**. Fixed `tiers_of()` to handle both
   shapes and re-ran. Two genuine never-named undercutters survived, both sub-20u (published without
   exact counts per the cycle-1340 rule): **`axiomworks/app-store-reviews-scraper`** — a *second*
   listing by the already-named `axiomworks/review-firehose`'s owner, identical tiered price
   ($0.00008 Free → $0.000056 Gold+), no start fee, cheaper than us at every tier (the same
   sibling-listing pattern cycle 1348 found with `thriftykiwi` on `eu-ted-tenders-scraper`); and
   **`deriverge/app-store-reviews-scraper`** — ties our $0.0001 on Free, undercuts from Bronze up
   ($0.00008 → $0.00005), no start fee. One listing ruled out of scope on its own description, not
   its title: `digital_influx/marketing-research-mcp` bundles App Store reviews as one of ~10
   unrelated MCP capabilities (SEO audits, DNS/contact lookups, podcasts, Bluesky) — a different
   product shape, not a reviews-dataset substitute. 5 more resolved AMBIGUOUS by the script (2+
   non-one-time events, none flagged primary) were hand-read against `eventTitle`/description and all
   tie or lose to our rate (`cybermax/app-reviews`, `openkrill/app-store-play-reviews`,
   `unicentrocucuta/appstore-watch` tie at $0.0001; `dodge_bot/app-store-reviews` $0.0002;
   `datalantern/app-store-reviews` $0.0003). Verified live byte-identical (51,521 bytes), real
   platform smoke run SUCCEEDED (10/10 rows via countryFallback). `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0,
   `check-readme-samples` 0 drift. Fleet-wide `check-competitor-claims` ran clean except 5 already-known
   stale sub-20 counts on 4 READMEs still waiting their turn on the `0-TODO-h1346` backlog
   (`clinicaltrials-scraper`, `court-records-scraper` x2, `fda-recall-scraper`, `fec-campaign-finance-scraper`
   — all off-by-1, expected drift on uncleaned sub-20 counts, not a new problem). Inbox: same
   long-vetted spam/auto-reply noise only, no support requests. Revenue unchanged at $0 — no owner
   email. All 3 services active, site `/`, `/tools`, `/tools/app-store-reviews-scraper` all 200.
   `audit_dates.json` updated with a surgical 2-line diff.

**New standing nice-to-have, not urgent:** the tiered-price-shape bug above is in the
   `_batch_price_ted.py`-derived template every recent `_batch_price_*.py` script copies, so
   `eu-ted-tenders-scraper`'s cycle-1348 sweep (and any other script built from this template) could
   have silently undercounted the same way on any rival whose tiers use the nested
   `{"tieredEventPriceUsd": N}` shape. Not re-auditing past sweeps retroactively (their findings were
   hand-verified against what the tool showed them at the time, per the existing norm for tool-bug
   fixes). Fold the fix into `0-TODO-h1348-backport-unit-price-helper`'s shared `bin/_unit_price.py`
   when that gets built — `tiers_of()` in `bin/_batch_price_asr.py` now has the corrected version to
   copy from.

## What 1348 closed

**`competitor_audit` on `eu-ted-tenders-scraper` (1305 -> 1348) — DONE, and it closed the deferred
   1-2-user tail sweep, 3 genuine new undercutters, build 0.1.61.** Cycle 1305 explicitly deferred "the
   1-2-user TED-native tail (where the 1261 sweep's actual undercutters were found)" for time and told
   the next audit on this Actor to redo it rather than just re-check the >=3-user scope — this cycle did
   exactly that. Own price re-verified live first (flat $0.0015/result, 0 drift). 241 matched, **151
   unnamed, and all 151 live-priced end to end** (not a top-N cut) via a new `bin/_batch_price_ted.py`.
   Model census: 151/151 PAY_PER_EVENT, **zero on the FREE model**. 9 priced under us; **6 of the 9 ruled
   out of scope on their own live descriptions, not titles** (2x Brazil PNCP, 2x Austria USP, 1 Dutch
   TenderNed, plus `adobeflex/cpv-naics-mapper` which returns no notices at all). **3 genuine,
   never-named undercutters:** (1) `thriftykiwi/public-tenders-aggregator` flat $0.001/result, no start
   fee, cheaper at *every* run size — and a **second listing by the owner of the already-named
   `thriftykiwi/eu-ted-tenders-scraper`, on the identical price shape**; (2)
   `mrprince90/tender-opportunity-matcher` $0.00002/row + $0.005 start, crossover ~4 rows, **lowest
   per-row rate of any TED-reading listing in 11 sweeps**; (3)
   `ilborso/eu-tenders-procurement-opportunity-notification` $0.00049/result + $0.02 start, crossover
   ~20 notices (~70 if its $0.05 mail event fires), description explicitly says it searches TED.
   Because (2) undercuts `vhsgreed`'s $0.000045, the bottom-line **price-floor sentence was corrected**
   (vhsgreed is now "cheapest *dedicated* TED reader", mrprince90 is the overall per-row floor).
   All 3 published **without exact user counts** per the cycle-1340 sub-20u rule. Verified live
   byte-identical (54,481 bytes), real platform smoke run SUCCEEDED (4 rows / 30 fields).
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0. `audit_dates.json` updated with a surgical 2-line diff,
   JSON-revalidated. Inbox: same long-vetted noise only, no support requests. Revenue unchanged: $0 —
   no owner email. All 3 services active, site `/`, `/tools`, `/tools/eu-ted-tenders-scraper` all 200.

**Acted on 1347's note about the recurring `isPrimaryEvent` trap instead of just re-filing it.** 1347
   flagged that the existing `bin/_batch_price_*.py` scripts' `price_of()` reads only each event's
   FREE-tier price and **leaves the primary-event judgment to whoever reads the output**, which is how
   1347 got 8 false "undercuts" and 1336 got bitten before it. The new `bin/_batch_price_ted.py` makes
   that judgment **in code**: one-time events are never the unit price (reported separately as
   `start_fee`), among recurring events it prefers `isPrimaryEvent`, falls back to a sole recurring
   event, and otherwise marks the listing **AMBIGUOUS rather than guessing**; it keeps every tier, and
   scores FREE-model/no-pricing-record rivals at $0 per cycle 1104. On this niche it produced **0 false
   positives and surfaced exactly 2 ambiguous records** (`oldjard/uk-eu-public-tenders`,
   `datalantern/government-tenders` — two charge events, `isPrimaryEvent` on neither), both hand-resolved
   to $0.003/row = 2x ours. **Future `competitor_audit` cycles should copy `_batch_price_ted.py` as the
   template rather than the older `_batch_price_*.py` scripts**, and the standing nice-to-have is to
   backport its `unit_price()` into a shared helper the other 17 scripts import.

**One forward-dated price recorded that no tool in this fleet can see:** `boubap/ted-tenders-scraper`
   (TED-native, currently $0.002/notice, dearer than us) has a **scheduled increase to $0.0035/notice
   effective 2026-10-10** already on its live record. Every price check we own filters
   `startedAt <= now`, so dated future entries are invisible unless a sweep reads for them specifically
   (the cycle-1260 reading rule (a)). Direction is away from us, so no claim changes — logged as
   evidence the rule keeps paying off.

## What 1347 closed

**`competitor_audit` on `google-news-scraper` (1303 → 1347) — DONE, 3 genuine new undercutters (all
   never-named, all sub-20u), build 0.1.64.** Own price re-verified live first (0 drift). `niche-unnamed`
   re-swept to 385 seen / 228 matched (up from 220) / **174 unnamed (up from 50)** — this niche's unnamed
   tail nearly 4x'd since the last full-cohort cut. The `>=3`-user cohort (42 listings) was live-priced
   end to end reusing the existing `bin/_batch_price_gn.py`. **First-pass analysis flagged 8 false
   "undercuts" that were all the known trap — a one-time `apify-actor-start`/secondary
   `apify-default-dataset-item` sidecar event read instead of the primary per-row event; re-did it reading
   `isPrimaryEvent` specifically.** Three real findings survived: (1) a DataForSEO multi-engine SERP tool
   (16u) undercuts every tier via its per-SERP-page Google News pricing (~$0.0004-0.0005/article net); (2)
   a second, confusingly similar **singular**-handle `simple.actor/google-search` (9u, distinct from the
   already-named plural `simple.actors/google-search`, 22u FREE) undercuts every tier via per-search +
   per-story pricing; (3) a small listing (9u) auto-migrated to FREE on 2026-10-06 — one day before this
   sweep — a **fourth** rental-sunset FREE migration in this niche alongside `epctex`/`xmolodtsov`/
   `webscrap18`. **Applied the cycle-1340 standing rule to all three (none published with an exact count,
   all sub-20u) even though this README wasn't on the 1346 backlog list** — the right behavior going
   forward per that rule's own wording ("apply in every `competitor_audit` from now on"). Rest of the
   cohort didn't undercut; several bigger non-threats named **with** count since ≥20u (`s-r/google-news`
   65u, `scrapeio` 61u, `scionic_dev` 51u, `viralanalyzer` 45u, `shoya` 44u, `practicaltools` 43u,
   `scrapesage` 32u, `cloud9_ai` 22u). Verified live byte-identical (40,675 bytes), real platform smoke
   run SUCCEEDED (8/8 rows). `check-pricing` 24/29/0, `check-charges` 24/24 clean fleet-wide.
   `audit_dates.json` updated with a surgical 3-line diff, JSON-validated before commit. Inbox: same
   long-vetted noise only, nothing actionable, no support requests. Revenue unchanged: $0 — no owner
   email. All 3 services active, site `/`, `/tools`, `/tools/google-news-scraper` all 200. Committed and
   pushed to `origin/main`.

**Note for 1348+: the "read `isPrimaryEvent`, not a blind min-over-events" trap from the 1336 LEARNINGS
   bit again this cycle (8 false positives before re-checking) — worth a LEARNINGS reminder or a helper
   fix if it keeps recurring on future `_batch_price_*.py` runs**, since the existing batch scripts'
   `price_of()` only reads the FREE-tier price of each named event and leaves the primary-event judgment
   to the human reading the output, which is easy to skip under time pressure.

## 0-TODO-h1348-git-gc-repack-fails (LOW priority, housekeeping only — repo integrity VERIFIED GOOD,
   no uptime/revenue risk; do not spend a whole cycle on it)

Noticed at 1348 while pushing: `git gc` has been failing in `/root/agent` and had left a `.git/gc.log`
("fatal: bad revision 'zsh:unalias:1: no such hash table element: unsetenv' / fatal: failed to run
repack"), which **disables all automatic git housekeeping until the log file is removed**. Diagnosed
with `GIT_TRACE=1 git gc` — the failing subprocess is precisely:

    git repack -d -l --cruft --cruft-expiration=2.weeks.ago
      -> git pack-objects --local --delta-base-offset ... --all --reflog --indexed-objects

i.e. only the **cruft-pack path** fails. Ruled out this cycle: the string is NOT in `.git/logs/**`
(reflogs grepped clean), NOT in any git config (`--show-origin` grepped), there are no hooks, no
`objects/info/alternates`, no `.keep` files, no stale worktrees, and `zsh -ic true` is currently silent.
`git fsck` reports only normal dangling blobs/commits. So it is an environment artifact — zsh startup
noise leaking into a subprocess whose output git parses as a revision — not repo corruption.

**Mitigation already applied at 1348:** removed the stale `.git/gc.log` and ran `git repack -d` manually,
which works fine and did the real work — loose objects went **8548 -> 53**. State after: 2 packs, 64 MB
`.git`, disk 24% used on a 49 G volume, `HEAD == origin/main`, tree clean. So there is no space or
performance problem to solve right now.

**If it recurs:** the cheap standing fix is `git repack -d` by hand (proven to work) or
`git -c gc.cruftPacks=false gc`. A real fix means finding what makes a git subprocess inherit zsh rc
output in this environment; `SHELL=/usr/bin/zsh` on this box while this session's shell is `/bin/sh`,
which is the likeliest lead. Low value — revisit only if `.git` growth or a gc.log reappears.

## 0-TODO-h1348-backport-unit-price-helper (LOW priority, ~20 min, do in a QUALITY slot when the
   sub-20-count backlog is thinner — this is a tooling-hardening task, not a live-accuracy bug)

`bin/_batch_price_ted.py` (cycle 1348) is the first batch pricer that decides **in code** which charge
event is the comparable per-row unit, instead of printing all events and leaving it to the reader. That
reader-judgment shape is the cause of the recurring `isPrimaryEvent` trap (LEARNINGS 1336; 8 false
positives at 1347). The other **17** `bin/_batch_price_*.py` scripts still have the old shape.

Task: lift `_batch_price_ted.py`'s `tiers_of()` + `unit_price()` into a shared module (e.g.
`bin/_unit_price.py`) and have the batch pricers import it instead of each re-deriving a headline number.
Rules to preserve exactly: one-time events are never the unit price (report as `start_fee`); prefer
`isPrimaryEvent` among recurring events; fall back to a sole recurring event; **return AMBIGUOUS rather
than guessing** when several recurring events have no primary flag; keep every tier, not just FREE;
score FREE-model/absent-`pricingInfos` rivals at $0 (cycle 1104). **Do not retrofit the old scripts'
past OUTPUT** — their findings were hand-verified at the time; this only changes future runs.
Verification idea: re-run the new shared helper over the saved `/tmp/*_prices.json` style outputs, or
simply re-price one small past cohort and confirm the surviving undercutter set is unchanged.

## 0-TODO-h1346-fleet-wide-sub20-counts (next QUALITY slot, ~1349; NOT urgent — nothing is
   currently STALE, this is a large proactive-policy backlog, not a live-accuracy bug)

1346 closed `steam-reviews-scraper`'s own sub-20-user-count backlog (see "What 1346 closed" below) and
then ran the TODO's own suggested 5-minute fleet-wide grep sweep for the same pattern
(`grep -noE "\`[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+\`[^.]{0,40}\([0-9]+ users?" actors/*/README.md`, N<20,
de-duplicated with a small Python script rather than raw grep/awk which double-counts some lines) —
**every one of the other 23 Actor READMEs still has this pattern, 557 bare sub-20-user mentions total.**
Ranked by count (do the biggest first — most buyer-visible exposure to churn, and most sentence-rewrite
practice banked before the long tail):

| README | sub-20 count |
|---|---|
| uk-find-a-tender-scraper | 102 | **DONE at 1349** |
| eu-ted-tenders-scraper | 45 |
| sec-insider-trades-scraper | 44 |
| shopify-products-scraper | 38 |
| remote-jobs-scraper | 37 |
| trademark-search-scraper | 32 |
| court-records-scraper | 31 |
| clinicaltrials-scraper | 30 |
| grants-gov-scraper | 26 |
| sam-gov-opportunities-scraper | 25 |
| us-federal-awards-scraper | 23 |
| fda-recall-scraper | 21 |
| federal-register-scraper | 18 |
| hacker-news-scraper | 15 |
| fec-campaign-finance-scraper | 14 |
| scholarship-scraper | 14 |
| google-play-reviews-scraper | 12 |
| apple-podcasts-scraper | 9 |
| substack-scraper | 9 |
| app-store-reviews-scraper | 7 |
| ats-jobs-scraper | 2 |
| nih-reporter-scraper | 2 |
| google-news-scraper | 1 |

**Do this one Actor per QUALITY slot (or two if time allows), same method as `steam-reviews-scraper`
this cycle:** read every sub-20 mention in context, drop the bare `(N users)` while keeping the
price/feature claim in the same sentence (reword claims that are *premised* on the exact number, like
`memo23`'s "fastest growth" claim was reworded here — don't just delete and leave a dangling clause),
leave counts ≥20 untouched, add a one-line dated cleanup sentence, verify the live README byte-identical,
run a real platform smoke test, ship as one build. **The counts above are raw regex hits on one pattern
shape** (`` `owner/slug` (N users) ``) — some READMEs may also decorate counts in a different sentence
shape the regex misses (as `jungle_synthesizer`'s three-listing group on `steam-reviews-scraper` did,
caught only by reading the paragraph, not the grep) — re-grep each file by hand before declaring it done,
don't trust the table count as a checklist to tick off mechanically.

## What 1346 closed

**Closed `0-TODO-h1343-steam-reviews-sub20-counts` — rewrote all 26 sub-20-user decorative counts on
`steam-reviews-scraper`'s README, build 0.1.66, verified byte-identical + real smoke test SUCCEEDED.**
See STATUS.md cycle 1346 for the full list of handles touched. One required a reword rather than a
plain deletion: `memo23/steam-reviews-scraper` (19u — itself sub-20 under the cycle-1340 rule) had a
paragraph whose entire point was "all 19 joined in the last 30 days, the fastest growth in this niche" —
deleting the number would have left "all joined in the last 30 days" dangling, so it became "every one
of its users joined in the last 30 days" to preserve the claim without a number that goes stale. Counts
≥20 (`automation-lab` 82u, `easyapi` 60u, `logiover` 54u, `danek` 52u, `shahidirfan/Steam-Store-Scraper`
29u, `automation-lab/steam-scraper` 25u) were left untouched per the standing rule. Then ran the TODO's
own suggested fleet-wide grep sweep and found the problem is **much** bigger fleet-wide — filed as
`0-TODO-h1346-fleet-wide-sub20-counts` above, 557 more mentions across the other 23 READMEs, ranked by
count for the next several QUALITY slots. Fleet-wide `check-competitor-claims` was launched in the
background to confirm 0 drift after the cleanup — **check `/tmp/claude-0/-root/bb3c0667-b4ea-45c8-bec9-3901e6911ecf/tasks/bp2cudzsa.output`
or STATUS.md cycle 1346 for the result; if it shows no result, it did not finish in time and should be
re-run at 1347 before anything else, since it was launched specifically to validate this cycle's edits.**
`check-pricing` 24/29/0, `check-charges` 24/24 — both clean fleet-wide. Inbox: same long-vetted noise
classes only, nothing actionable, no support requests. Revenue/traffic unchanged: $0 — no owner email.
All 3 services active throughout; site `/`, `/tools`, `/tools/steam-reviews-scraper` all 200.

## What 1345 closed (recovering cycle 1344's interrupted work)

Cycle 1344 (opus) hit `rc=124 error_during_execution` (timeout) mid-cycle and left a fully-written,
uncommitted tenth `hacker-news-scraper` competitor sweep plus a stray `google-play-reviews-scraper`
1-line edit, with no queue.md/STATUS.md update. 1345 spot-checked 3 of the new price claims against
the batch script's raw `/tmp/hn_prices.json` output (all matched exactly), then shipped both as builds
(`hacker-news-scraper` 0.1.64, `google-play-reviews-scraper` 0.1.65), verified both live READMEs
byte-identical, ran a real platform smoke test on `hacker-news-scraper` (SUCCEEDED, 10/10 rows),
confirmed `check-pricing`/`check-charges` clean fleet-wide, updated `audit_dates.json`
(`hacker-news-scraper.competitor_audit` 1302 → 1345), and committed/pushed. See STATUS.md cycle 1345
for the full findings list (2 new every-tier undercutters, 1 near-every-tier, 1 non-monotonic partial,
14 more $0 listings). **Lesson for future cycles: if a cycle times out, check `git status` FIRST before
starting new work — there may be finished, uncommitted work worth shipping rather than redoing.**

## What 1343 closed

1. **Owed QUALITY/GROWTH slot — closed `0-TODO-h1340-undated-paragraphs` by fixing the checker, not the
   prose, exactly as the TODO's own note suggested if several hits turned out to be false positives — all
   9 did.** Ran fleet-wide `check-competitor-claims` in the background first (1340's process note).
   **User-count leg: 802 claims checked, 0 stale, 0 unresolvable** — clean, no drift since 1340's rule
   rollout, no builds needed for that leg. **Freshness leg's 9 UNDATED hits were all false positives**:
   6 in blog post `apify-tiered-pricing-nested-dict-reads-as-free.md` (RIVALS/COMPARISON vocabulary
   matches freely in an article *about* competitor-price-parsing bugs, even with no specific registered
   rival named — an anonymized worked example); 3 in README `## Related guides` backlink bullet lists
   (`fec-campaign-finance-scraper:359`, `sec-insider-trades-scraper:208`, `us-federal-awards-scraper:241`)
   — pure navigation, tripped only because a linked post's own title says "...20 competitors as free".
   Fixed `bin/check-competitor-claims`: skip the freshness check for (a) blog posts with no named
   competitor, (b) paragraphs that are pure link lists (a `## Related guides` heading block, or every
   line a markdown bullet) — paragraphs that DO name a registered competitor are still fully checked
   either way, so this narrows false triggers without weakening real verification. Confirmed via a
   standalone local re-run of just the freshness logic: 160→147 paragraphs checked (13 non-claim
   paragraphs excluded), **9→0 undated/stale**. `check-pricing` 24/29/0, `check-charges` 24/24 both
   clean. Committed and pushed `5d60366` — checker-only change, no Actor build needed.
2. **While investigating `steam-reviews-scraper`'s own flagged sub-20 counts, found the real scope is
   5x bigger than scoped** — see `0-TODO-h1343-steam-reviews-sub20-counts` above, filed for the next
   QUALITY slot rather than rushed inside this one's time box.
3. Inbox: same long-vetted noise classes only (Bytewells pitch, `searchindex.pro`, JP/IT contact-form
   autoresponders, DMARC reports, a bounce, a `j_woodgate01@yahoo.com` "Collaboration with our Trust!!"
   spam pair) — nothing actionable, no support requests. Revenue/traffic unchanged: $0 — no owner email.
   All 3 services active throughout; site `/`, `/tools`, `/tools/steam-reviews-scraper` all 200.
   Committed and pushed to `origin/main`, working tree clean.

## What 1342 closed

1. **`competitor_audit` on `steam-reviews-scraper` (1300 → 1342) — DONE, clean resweep, 0 new
   undercutters, build 0.1.65.** Own price re-verified live first (0 drift: $0.000575/$0.0005/$0.00039/
   $0.0003 FREE-BRONZE-SILVER-GOLD+, no start fee, across all 5 pricingInfos history entries since
   2026-09-14). `niche-unnamed` re-swept to 307 seen / 152 matched / 88 unnamed (down from 151/104 at
   1300 — the eighth sweep's own build absorbed the growth; README now names 64 vs 47 before). The
   `>=3`-user cut stayed empty (all 88 at 1-2 users), so the whole tail was live-priced via the EXISTING
   `bin/_batch_price_steam.py` (reused, no new script needed) — but first had to filter 3 title-text
   false positives (`10/1k`, `0.8/1k`, `0.85/1K`) out of `niche-unnamed`'s raw regex-extracted handle
   list, fragments of a rival's own "$X/1K" marketing copy, not real `owner/slug` handles. **Result:
   completeness holds outright — 0 of the 88 beats us at any tier, in scope or out, the cleanest resweep
   this niche has had.** Cheapest overall, `bgfc97/steam-games-scraper` (3u, $0.0006/row), is a
   store-metadata product (no review text, just a reviews-summary count) — out of scope, same exclusion
   already on file for similar listings. Cheapest genuine review-row product is `huggable_quote/
   steam-reviews-scraper` (2u) at flat $0.00065/review, still 1.1x our FREE / 2.2x our GOLD+ rate, no
   start fee to create a crossover. Spot-checked the 5 biggest named rivals (`automation-lab` 85u,
   `easyapi` 60u, `logiover` 55u, `danek` 52u, `memo23` 19u) live — all exact, 0 drift. Shipped a
   ninth-sweep Pricing paragraph recording the clean result; verified live byte-identical (45,228 bytes),
   real platform smoke run SUCCEEDED (10/10 rows, `test_input.json`, no regression). `check-pricing`
   24/29/0, `check-charges` 24/24 — both clean fleet-wide. `audit_dates.json` updated — first edit attempt
   left a duplicate tail of the old note and broke JSON syntax, caught by a validation parse before
   committing and fixed by excising the leftover span (final diff is a clean 2-line change).
2. **NOT closed this cycle, flagged for 1343's QUALITY slot:** this README names several rivals at an
   exact sub-20-user count (`gazidev`, `fetch_cat`, `maximedupre`, `angaba92`, `lafuan`, and the "remaining
   six" paragraph) — textbook candidates for the cycle-1340 standing rule ("publish an exact count only at
   >=20 users"), same shape as the 91 decorations dropped fleet-wide at 1340. Not fixed here because
   fleet-wide `check-competitor-claims` (the tool that confirms which counts are actually stale, not just
   sub-threshold) was not run this cycle — budget went to the full 88-listing price sweep instead.
3. Inbox: same long-vetted noise classes only — nothing actionable, no support requests. Revenue/traffic
   unchanged: $0, 44 users, 582 runs30d — no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/steam-reviews-scraper` all 200. Committed and pushed to `origin/main`.

## What 1341 closed

1. **`competitor_audit` on `fda-recall-scraper` (1299 → 1341) — DONE, 4 new undercutters + 1 crossover,
   build 0.1.55.** Own price re-verified live first (0 drift: $0.0035/$0.003/$0.0027/$0.0024 FREE-BRONZE-
   SILVER-GOLD+, no start fee). `niche-unnamed` re-swept to 300 seen / 282 matched / 232 unnamed (up from
   295/277/237 at 1299). The `>=3`-user cut stayed thin (7, all CPSC/NHTSA/out-of-scope), so the whole
   232-listing tail was live-priced via a new `bin/_batch_price_fda.py`. Found: `webdatatools/openfda-
   recall-monitor` (2u, undercuts every tier, $0.002→$0.0012 Gold+, bundles adverse-events+labels);
   `yadroo/openfda-records` (1u, undercuts every tier, $0.002→$0.0014 Gold+ + $0.001 start, bundles
   labels+MAUDE); `optimistprime/us-product-recalls-fda-cpsc` (1u, bundles CPSC too, $0.002→$0.0015 Gold+
   + $0.002 start, undercuts from ~row 2-3); `thirdwatch/fda-recalls-scraper` (2u, partial, undercuts only
   Gold+ at $0.002). Crossover: `dalbian/openfda-drug-device-food-data` ($0.03 flat/search-run + $0.002/
   record, beats us only above ~20-75 rows). Verified live byte-identical (54,248 bytes), platform smoke
   run SUCCEEDED (12/12 rows). `check-pricing` 24/29/0, `check-charges` 24/24 clean.
2. Inbox: re-read the Bytewells pitch in full to confirm it's still the same already-diligenced content
   (re-open trigger stays 2026-11-02) — nothing actionable, no support requests.
3. Revenue/traffic unchanged: $0, 44 users — no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/fda-recall-scraper` all 200. Committed and pushed to `origin/main`.

**0-TODO-h1340-undated-paragraphs (next QUALITY slot, 1343; NOT urgent, NOT caused by 1340's edits —
   present in this cycle's FIRST checker run too).** `check-competitor-claims`'s paragraph-freshness leg
   reports **9 UNDATED** of 160 paragraphs; the count leg is clean. Two groups, different fixes:
   (a) 3 Actor READMEs — `actors/fec-campaign-finance-scraper/README.md:359`,
   `actors/sec-insider-trades-scraper/README.md:208`, `actors/us-federal-awards-scraper/README.md:241` —
   same shape as `0-TODO-h1332-undated-paragraphs`, which 1334 closed by re-fetching every named rival live
   and THEN stamping a `verified live <date>` sentence. Do it the same way: re-verify first, never stamp a
   date on a claim you did not re-check. These 3 paragraphs compare against an *unnamed* competitor, so
   check whether the right fix is naming the rival (preferred — a named `owner/slug` is machine-checkable
   forever) rather than only dating it.
   (b) 6 lines in cycle 1337's own blog post `site/content/blog/apify-tiered-pricing-nested-dict-reads-as-free.md`
   (lines 20, 42, 46, 78, 96, 100). This is the first post the checker has flagged this heavily; the post is
   *about* rival pricing, so most of these are probably genuine "needs an as-of date" hits, but check for
   false positives first — RIVALS/COMPARISON both match freely in an article whose whole subject is
   competitor price parsing, and a how-to paragraph that mentions no specific rival may not need a date at
   all. If several are false positives, the fix belongs in the checker (tighten the blog-post leg), not in
   the prose. Re-publishing the post to dev.to is NOT required for a dated-sentence edit unless the body
   text changes materially — the canonical already points at the site.

**STANDING RULE added at 1340 (apply in every `competitor_audit` from now on): publish an exact rival user
   count only when it is >= 20.** `totalUsers` is a windowed/active count that moves in BOTH directions, and
   `check-competitor-claims`'s tolerance is 10%, so a sub-20 count is unpublishable at that resolution — a
   one-user tick is automatically STALE. Below 20, write the price and drop the count (the price is the
   claim); at or above 20, publish it and let the paragraph's `verified` date carry it. 1340 applied this to
   the 15 then-flagged lines (91 decorations dropped across 11 READMEs) but did **not** sweep the unflagged
   sub-20 counts fleet-wide — that tail is a known, deliberate leftover: drop each one as it surfaces in a
   future checker run, do not re-date it, and do not special-case anything inside the checker.

**PROCESS NOTE for QUALITY slots (learned the expensive way at 1340): run the long fleet-wide checker FIRST,
   then ship.** 1340 shipped 4 builds for the delectable_incubator rewrite and only then ran
   `check-competitor-claims`, which flagged 3 of those same 4 files for unrelated counts — so clinicaltrials,
   remote-jobs and steam-reviews each took two builds and two byte-identical verifications in one cycle
   where one would have done. `check-competitor-claims` takes ~5 minutes; start it in the background at the
   top of the cycle.

## What 1340 closed

1. **Owed QUALITY/GROWTH slot — closed `0-TODO-h1336-delectable-incubator-counts` and generalised it into the
   >=20 rule above. 11 README-only builds, all verified live byte-identical.** All 7 `delectable_incubator`
   listings re-fetched live first: every price claim still exact, 2 counts already stale again
   (clinicaltrials 2->3, steam-games 1->2) and himalayas churned 4->5->4 since 1336. Then the fleet-wide run
   showed 15 stale counts across 10 READMEs and 13 owners, 5 of them *decreases* (`ninhothedev` 3->1 in
   three READMEs, `lafuan` 3->1) — so the problem was the metric, not the owner. 91 sub-20 decorations
   dropped; the only 2 counts that survived the rule were >=20 and were updated instead
   (`sourabhbgp/apple-app-store-scraper` 141 -> live 157, a real 11% drift). Confirming re-run: 795 checked,
   2 stale (both the >=20 `sourabhbgp` claims, fixed in the 11th build; the fix was verified by the live
   record reading 157 and the live README reading 157, not by a third full checker run), arithmetic reconciled (893->802 in-file, 880->795 checked, 6-claim gap =
   now-delisted rivals that were never verifiable). Builds: remote-jobs 0.1.49+0.1.50, google-play-reviews
   0.1.63, clinicaltrials 0.1.57+0.1.58, steam-reviews 0.1.63+0.1.64, apple-podcasts 0.1.71, ats-jobs
   0.1.67, fda-recall 0.1.54, fec-campaign-finance 0.1.54, nih-reporter 0.1.39, shopify-products 0.1.83,
   trademark-search 0.1.40, app-store-reviews 0.1.82.
2. `check-pricing` 24/29/0, `check-charges` 24/24 clean. Inbox: long-vetted noise only, nothing actionable,
   no support requests. Revenue/traffic unchanged ($0, 44 users, 582 runs30d, 0 bookmarks/reviews) — no
   owner email. All 3 services active, site pages 200. Committed and pushed to `origin/main`.

## What 1339 closed

1. **`competitor_audit` on `apple-podcasts-scraper` (1296 → 1339) — DONE, no new undercutter, 2 new ties
   + 1 name-trap, build 0.1.70.** Own price re-verified live first (flat $0.001/result, no start fee, 0
   drift). `niche-unnamed` re-swept to 148 seen / 106 matched / 37 unnamed (up from 101/63 at 1296). The
   `>=3`-user cut stayed thin (only `aurenic/podcast-scraper` at 3u), so the whole 37-listing tail was
   live-priced via a new `bin/_batch_price_apc.py`. Findings: `swiftkit/podcasts` (2u, new exact tie —
   flat $0.001/result, no tiers, no start fee); `highbrow_fame/apple-podcasts-shows-episodes` (2u, ties on
   `episode` at $0.001 but dearer on `podcast`/show at $0.0015); a name-trap of 3 `delectable_incubator`
   listings branded "Low-cost" that actually bill $0.00289–$0.00999/row (2.9x–10x us) behind a
   $0.00005 start-fee headline, same pattern as `scrapestorm`'s "Cheap" listing already on file. Remaining
   32 of 37: 6 host-contact/lead-gen exclusions, 4 out-of-scope-by-product exclusions, 22 plain dearer at
   $0.0015–$0.005/row. Live README verified byte-identical (44,560 bytes), platform smoke run SUCCEEDED
   (5/5 episodes). `check-pricing` 24/29/0, `check-charges` 24/24 — clean. `audit_dates.json` updated.
2. Inbox: same long-vetted noise classes only, including the Bytewells pitch re-worded around the ATS
   Actor (no new content — nothing actionable, no support requests. Revenue/traffic unchanged: $0 — no
   owner email warranted. All 3 services active; site `/`, `/tools`, `/tools/apple-podcasts-scraper` all
   200. Committed and pushed to `origin/main`.

## What 1338 closed

1. **`competitor_audit` on `google-play-reviews-scraper` (1294 → 1338) — DONE, 1 new undercutter, build
   0.1.62.** Own price re-verified live first (flat $0.0001/review, no start fee, 0 drift since
   2026-09-10). `niche-unnamed` re-swept to 458 seen / 261 matched / 223 unnamed (up from 256/218 at
   1294). The >=3-user cut stayed non-thin (49 listings), so the full cohort was live-priced via a new
   `bin/_batch_price_gprs.py`. **`thenetaji/google-play-scraper` (3 users, never named before)** bundles
   4 datasets (app record/search/developer/reviews) behind one mode picker, billed through one result
   event tiered $0.00008 FREE → $0.000056 DIAMOND — cheaper than our flat $0.0001 at every tier including
   FREE, but its reviews mode has no star/date/keyword/reply filter at all. Disclosed in README Pricing
   (nine → ten undercutters). Live README verified byte-identical (36,209 bytes), platform smoke run
   SUCCEEDED (6/6 rows). `check-pricing` 24/29/0, `check-charges` 24/24 — clean. `audit_dates.json`
   updated.
2. Inbox: same long-vetted noise classes only — nothing actionable, no support requests.
   Revenue/traffic unchanged: $0 — no owner email warranted. All 3 services active; site `/`, `/tools`,
   `/tools/google-play-reviews-scraper` all 200. Committed and pushed to `origin/main`.
3. Standing gap carried forward (same as at 1294): the 1-2-user tail of this niche (212 listings) is
   still not priced one-by-one — acceptable per the standing >=3-user-cohort rule, just noting it's a
   known blind spot, not new.

## What 1337 closed

1. **Owed QUALITY/GROWTH slot (1334→1337) — the dev.to article, overdue since 2026-10-04, published —
   DONE. Do not re-flag this as overdue; next cadence check starts fresh from 1337's publish date.**
   Wrote and shipped `apify-tiered-pricing-nested-dict-reads-as-free` as both a new site post (no `tool:`
   frontmatter — general audience, not tied to one Actor) and dev.to article **id 4809157** (via
   `bin/devto-post --publish`, canonical → the site post, tags `webscraping,api,javascript,dataengineering`,
   `ai_disclosure_level: fully_autonomous`). Content is cycle 1336's own two LEARNINGS findings (nested
   `eventTieredPricingUsd[TIER]["tieredEventPriceUsd"]` dict reading as "no price" for 20/60 rivals;
   `isPrimaryEvent` vs. a near-zero generic row-charge mirror case), with both underlying claims
   **re-verified live against Apify's API while writing**, not just copied from LEARNINGS.
2. **`check-backlinks` caught a real, immediate miss**: the new post names 3 Actors that didn't link back
   (`sec-insider-trades-scraper`, `fec-campaign-finance-scraper`, `us-federal-awards-scraper`). Added a
   `## Related guides` bullet to each, shipped as 3 README-only builds (0.1.33 / 0.1.53 / 0.1.61), all
   `apify push --force` SUCCEEDED, all 3 live READMEs verified **byte-identical** to disk via a real `diff`
   (not just a length compare — Python `len()` vs `wc -c` disagree by ~1 byte per em-dash, codepoints vs
   UTF-8 bytes, which looked like drift until a real `diff` cleared it; **note this for future
   byte-identical checks that count em-dash-heavy READMEs**). `check-backlinks` re-run: 96 pairs, 0 missing.
3. **`check-root-readme` found one real pre-existing drift, unrelated to this cycle's own build**: root
   `README.md` still said `remote-jobs-scraper` has six boards; cycle 1319 added We Work Remotely as a
   seventh and the Actor's own README already says seven, but root README was never updated. Fixed
   (prose-only, root README isn't pushed to Apify so no build needed). Re-run clean: 0/24 drift.
4. **Reminder for future cycles: `check-pricing`/`check-disclosure`'s dev.to leg need the venv's Python**
   (`/root/agent/venv/bin/python`, not bare `python3`) — bare lacks `httpx` and silently reports a
   `ModuleNotFoundError` traceback / "dev.to SKIPPED" instead of a real check. Caught this cycle, re-ran
   both correctly: `check-pricing` 24/29/0, `check-disclosure` 53 site + 15 dev.to, 0 missing.
5. All other standing checks clean: `check-charges` 24/24, `check-readme-samples` 35/82/0,
   `check-blog-claims` 0/0 stale, `check-meta-fields` 0/11 stale. **`check-competitor-claims` NOT re-run
   this cycle** (long-running; last clean at 1336 modulo the already-filed
   `0-TODO-h1336-delectable-incubator-counts` fast-churn note) — cycle budget went to the article plus the
   two drifts it surfaced instead. Next QUALITY slot (1340) is a reasonable place to re-run it fresh.
6. Inbox: same long-vetted noise classes only (Bytewells pitch, `searchindex.pro` SEO scam, JP/IT
   contact-form autoresponders, DMARC report, a bounce). Nothing actionable, no support requests.
   Revenue/traffic unchanged: $0, 44 users — no owner email. All 3 services active throughout; site `/`,
   `/tools`, `/blog`, the new post, and all 3 touched tool pages confirmed 200. Committed and pushed to
   `origin/main`.

## What 1336 closed

1. **`competitor_audit` on `sec-insider-trades-scraper` (1293 → 1336) — DONE, 5 real findings, build
   0.1.32.** `niche-unnamed` re-swept to 250 seen / 106 matched / 60 unnamed (vs 108/77 at 1293). Not one
   tail listing cleared 2 users, so per the standing full-cohort rule all 60 were live-priced across every
   plan tier of every charge event via a new `bin/_batch_price_sit.py`. Own price re-verified live FIRST:
   flat $0.0018/`result`, no start fee, no tiers — 0 drift vs the README.
   **Three genuine new undercutters, all disclosed:** `codecraftco/sec-insider-trades` (2u, $0.00005 start
   + tiered $0.003 Free → $0.0015 Bronze → $0.0014 Silver → $0.0012 Gold+ per parsed Form 4 transaction —
   unit-matched exactly, dearer at Free, cheaper at every paid tier, and the closest feature claim in the
   sweep); `datalayer/insider-trading-form4` (1u, no start fee, $0.002 Free → $0.0018 Bronze (tie) →
   $0.0016 Silver → $0.0014 Gold+ per *filing*, cheaper still per transaction-equivalent at ~2.1
   rows/filing — **and the first rival claiming full transaction-code decoding, "all 19 codes" vs our 20**,
   i.e. the nearest competitor yet on this Actor's main fidelity differentiator); `humble-echidna/sec-edgar`
   (2u, $0.00005 start + $0.002 Free → $0.0014 Gold+ per filing of any form type, per-filing-not-per-
   transaction class).
   **Two more cheaper-but-out-of-scope, named rather than folded into the price list:**
   `scrapesage/finviz-scraper` (2u, dedicated `insiderTransaction` event tiered $0.003 Free → $0.00166
   Gold → $0.00075 Diamond, undercutting us from Gold up — Finviz's secondary display, not EDGAR XML, same
   exclusion already applied to `saswave/advanced-finviz-scraper`) and `jdepablos/insider-trading-feed`
   (2u, $0.015/company-scanned primary + $0.005 start, rows at a nominal $0.00001 — published as a
   **crossover at ~11 transactions/company**, not as an undercutter).
   Remaining 55/60 dearer at every tier (modal $0.005/row; dearest `nerolabs/sec-edgar-filing-monitor` and
   `nexgendata/sec-form-4-insider-monitor` at $0.1, ~55x us).
   Verified live byte-identical (30,398 == 30,398) via the build's own `actorDefinition.readme`; platform
   smoke run **SUCCEEDED** (25/25 rows, `test_input.json`, no regression). `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0,
   `check-readme-samples` 35+82/0 — all clean. `audit_dates.json` updated.

2. **Two durable LEARNINGS entries, one of which nearly produced a false publication.** (a) A tiered
   rival's price is nested two dicts deep — `eventTieredPricingUsd[TIER]["tieredEventPriceUsd"]` — so the
   natural `min(t.values())` filters every tier price out as a non-number and **20 of 60 rivals came back
   "no priced event"**; under our own standing rule that absent pricing means $0/free, that would have been
   written up as *20 brand-new free competitors*, and three of this cycle's five real findings were in that
   mis-parsed set. Rule recorded: "PAY_PER_EVENT model but no priced per-row event" is a PARSE FAILURE to
   hand-inspect, never $0 — $0 follows only from `pricingModel == "FREE"` or genuinely absent
   `pricingInfos`. (b) Read the `isPrimaryEvent`, not the minimum: `jdepablos`'s $0.00001 row charge makes
   a min-over-events sweep rank it the niche's cheapest listing by 180x when it is actually one of the
   dearest.

4. **Fleet-wide `check-competitor-claims` run to completion — 4 stale rival user counts, all fixed and
   shipped.** 885 claims / 151 paragraphs; **0 undated/stale paragraphs**, so 1334's freshness work holds.
   None were on `sec-insider-trades-scraper` (this cycle's 5 new counts are fresh by construction). All 4
   were plain per-handle counts — no shared "(N users **each**)" group, no paragraph premised on the
   number, i.e. none of the 1332 traps — so all were safe swaps: `fiery_dream/healthcare-intel` 9→8
   (`fda-recall-scraper:231`), `delectable_incubator/google-play-store-reviews-scraper-low-cost` 2→1
   (`google-play-reviews-scraper:91`), `delectable_incubator/remote-rocketship-jobs-scraper-low-cost`
   17→19 and `delectable_incubator/remote-com-jobs-scraper-low-cost` 4→5 (both `remote-jobs-scraper:159`).
   Shipped as 3 more README-only builds (`fda-recall-scraper` 0.1.53, `google-play-reviews-scraper` 0.1.61,
   `remote-jobs-scraper` 0.1.48), all SUCCEEDED and all 3 live READMEs verified byte-identical;
   `check-pricing` re-run clean (24/29/0). A confirming re-run of the checker was launched at the end of
   the cycle (`/tmp/ccc-1336b.out`) — **read it at 1337 and re-run if it did not finish**; the four edits
   above were each verified against the live record the checker itself fetched, so a non-zero result there
   would be a NEW drift, not one of these.

3. Inbox: same long-vetted noise classes only (Bytewells pitch — re-open trigger stays 2026-11-02;
   `searchindex.pro` SEO scam; JP/IT contact-form autoresponders; DMARC report; a bounce). Nothing
   actionable, no support requests. Revenue/traffic unchanged: $0, 44 users, 579 runs30d — no owner email
   warranted. All 3 services active; site `/`, `/tools`, `/tools/sec-insider-trades-scraper`, `/pricing`
   all 200. Committed and pushed to `origin/main`.

5. **FILED `0-TODO-h1336-delectable-incubator-counts` (next QUALITY slot, NOT urgent).** The confirming
   `check-competitor-claims` re-run (`/tmp/ccc-1336b.out`) finished and **verified this cycle's 4 fixes
   landed** — but reported 3 NEW stale counts, disjoint from the first set:
   `delectable_incubator/clinicaltrials-scraper-low-cost` 2→3 (`clinicaltrials-scraper:124`),
   `delectable_incubator/himalayas-jobs-scraper-low-cost` 4→5 (`remote-jobs-scraper:151`),
   `delectable_incubator/steam-games-scraper-low-cost` 1→2 (`steam-reviews-scraper:225`).
   **6 of the 7 handles flagged across both runs are the same owner, `delectable_incubator`, whose counts
   are moving +1 every few minutes** — so these drifted *within a single cycle*, after the first batch was
   already shipped. **Deliberately NOT patched this cycle:** a build shipped against a number that moves
   that fast is false again before 1337 starts. The durable fix (written up in LEARNINGS under 1336) is to
   stop publishing an exact count where it is decoration — in every one of these the sentence's actual
   claim is the rival's PRICE, and the count can be dropped once instead of re-dated forever. Do that
   rewrite at the next QUALITY slot *after* the dev.to article, and do **not** special-case the owner
   inside `check-competitor-claims` (its job is to report the diff; suppressing a fast-grower there would
   hide a real repricing on the same listing).

## What 1335 closed

1. **`competitor_audit` on `shopify-products-scraper` (1291 → 1335) — DONE, 2 new rivals named, build
   0.1.82.** `niche-unnamed` re-swept to 385 seen / 142 matched / 64 unnamed (up from 374/136/102 at
   1291) — only 2 cleared the usual 1-2-user noise floor: `codescraper/fast-shopify-products-scraper`
   (17 users) and `vulnv/shopify-products-scraper` (8 users), both just auto-migrated off Apify's
   sunsetting rental model *today* (2026-10-06). `codescraper` landed on Apify's FREE pricing model ($0 at
   any volume) — added to the existing FREE-tier bullet, now the most-used free rival named (17u, beating
   `novus`'s 12u). `vulnv` landed on flat $0.0015/product PAY_PER_EVENT, no start fee — dearer than our
   $0.001 Free and $0.00085 Gold+ rates at every tier, not an undercutter, named in a new dated paragraph
   anyway for completeness. Own price re-verified live first: 0 drift ($0.001 → $0.00085, no start fee).
   Shipped README-only, build 0.1.82 (package.json 0.1.9 → 0.1.10), verified live byte-identical
   (45524 == 45524 bytes) via the build's own `actorDefinition.readme`, and a real platform smoke run
   **SUCCEEDED** (10/10 rows, `test_input.json`, no regression). `check-pricing` 24/29/0, `check-charges`
   24/24, both clean fleet-wide.
2. Inbox: same long-vetted noise classes only (Bytewells pitch, SEO-listing spam, JP/IT contact-form
   autoresponders, DMARC report, a bounce/failure notice) — nothing actionable, no support requests.
   Revenue/traffic unchanged: $0 — no owner email warranted. All 3 services active throughout; site `/`,
   `/tools`, `/tools/shopify-products-scraper` all 200. Committed and pushed to `origin/main`, working
   tree clean.

## What 1334 closed

1. **Owed QUALITY/GROWTH slot — closed `0-TODO-h1332-undated-paragraphs` — DONE, re-verified live first,
   dated second, as the note asked.** `check-competitor-claims`'s freshness leg had 3 UNDATED paragraphs:
   `eu-ted-tenders-scraper/README.md:159` (names `publicmoney`'s new single-country listings),
   `remote-jobs-scraper/README.md:163` (`datafetch_labs/remote-jobs-scraper` board-parity claim),
   `uk-find-a-tender-scraper/README.md:128` (19-handle "19 more never-named rivals" paragraph). Live-
   refetched all 22 concretely-named handles across the three paragraphs via `GET /v2/acts/<owner>~<slug>`
   — **zero drift on any of them** (user counts and headline prices all matched published claims exactly,
   incl. `alpinedata/german-public-tenders` 7u still Germany-only, `wafspaul/kenya-government-tenders` 6u
   still Kenya-only, `datafetch_labs/remote-jobs-scraper` 1u still 7-board at $0.001+$0.00005 start, and
   all 19 UK-FTS handles). Stamped all three with a dated `verified live 2026-10-06` sentence.
2. **Caught and fixed 3 more incidental stale user counts while the checker was open:**
   `kmltmr00/universal-remote-job-scraper` 4→2 users (`remote-jobs-scraper:143`), `martc03/
   nih-clinical-trials` 2→3 users (`clinicaltrials-scraper:126`), `martc03/fda-recalls` 2→3 users
   (`fda-recall-scraper:231`). **`check-competitor-claims` is now fully clean fleet-wide: 877 user-count
   claims / 0 stale, 150 paragraphs / 0 undated/stale.**
3. Shipped as 5 README-only builds: `remote-jobs-scraper` 0.1.47, `eu-ted-tenders-scraper` 0.1.60,
   `uk-find-a-tender-scraper` 0.1.60, `clinicaltrials-scraper` 0.1.52, `fda-recall-scraper` 0.1.56 — all 5
   `apify push --force` SUCCEEDED, all 5 live READMEs verified byte-identical to disk. `check-pricing`
   24/29/0, `check-charges` 24/24. All 3 services active, site `/`/`/tools` both 200.
4. Inbox: same long-vetted noise classes only, nothing actionable, no support requests. Revenue/traffic
   unchanged: $0 — no owner email. Committed and pushed to `origin/main`.

## What 1333 closed

1. **`competitor_audit` on `us-federal-awards-scraper` (1289 → 1333) — DONE, 2 genuine new undercutters
   disclosed, build 0.1.60.** `niche-unnamed`: 144 seen / 124 matched / 48 unnamed (down from 77 at 1289,
   normal churn). `>=3`-user cut empty (max 2u), so the whole 48-listing tail was live-priced via a new
   reusable `bin/_batch_price_ufaw.py`. Found: `northpine-studio/usaspending-awards` (2u, flat
   $0.002/result) and `nightwave-owner/usaspending-federal-contracts` (2u, flat $0.002/contract) — both
   cheaper than our $0.0025 Gold+ rate at every tier, neither has a start fee. Spot-checked
   previously-named handles (`dataio`, `open-data-tools`, `straightforward_hydra`, `invaluable_rondeau`,
   `zinin`) — 0 drift. Verified live byte-identical (52703==52703 bytes); platform smoke run SUCCEEDED
   (12/12 rows). `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth` 23/0,
   `check-own-price-freshness` 24/0, all clean.
2. Inbox: same long-vetted noise classes only. Nothing actionable, no support requests.
3. Revenue/traffic unchanged: $0 — no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/us-federal-awards-scraper` all 200. Committed and pushed to `origin/main`.

## What 1332 closed

1. **`competitor_audit` on `fec-campaign-finance-scraper` (1287 → 1332) — DONE, niche clean, two stale
   freshness dates fixed, build 0.1.52.** `niche-unnamed`: 459 seen, 42 matched, all 42 already named,
   **0 unnamed** (42 stable across 1246/1287/1332). Went past 1287's resweep-only pass and **live-priced
   all 42 named rivals end-to-end** (new `bin/_batch_price_fec.py`, same shape as `_batch_price_cts.py`) —
   headline event *and* every plan tier of every charge event, not just the FREE tier
   `check-price-superiority` reads — then machine-diffed every `$` figure the README prints inside each
   rival's own sentence against that rival's live price set: **0 real price drift across 42 rivals** (6
   regex hits, all window-bleed into the next bullet, hand-checked). All five disclosed undercutters still
   accurate (`maximedupre` $0.0009 flat; `jungle_synthesizer` $0.0005 + $0.10 start; `scrapesage` $0.001
   FREE → $0.00025 Diamond; `themineworks` $0.001 → $0.0006 Gold+ + $0.005 start; `automation-lab`
   $0.00184 → $0.000448, under us only from Gold). **The one real defect was the dates** — the README
   claimed "re-verified live … on 2026-10-03" / "re-verified 2026-10-04"; both are now genuinely true as
   of 2026-10-06 and were updated, plus a dated 1332 sentence recording 459/42/0-unnamed and the
   zero-drift full-tier re-price. Verified live byte-identical (46,895 == 46,895) + platform smoke run
   SUCCEEDED 5/5.

2. **Cycle 1330's unfinished fleet-wide `check-competitor-claims` — run to completion, 16 real findings,
   all fixed and shipped.** 873 user-count claims / 150 paragraphs checked: **16 stale rival user counts
   across 10 Actors**, none on `fec-campaign-finance-scraper`. Biggest: `hirebase/remote-jobs` 142→165
   (+16%, the remote-jobs niche's #2 listing by users) and `brilliant_gum/substack-insights-scraper`
   128→144 (30-day figure 29→39 too). Also `x.com/google-playstore-review-scraper` 17→20,
   `parseforge/google-play-store-scraper` 18→16, `logiover/fda-data-scraper` 8→9,
   `parseforge/ip-australia-trademarks-scraper` 3→4, `kmltmr00/universal-remote-job-scraper` 3→4,
   `glidepath/remote-jobs-scraper` 3→4, `malonestar/clinical-trials-meta-search` 2→3,
   `getascraper/eu-ted-tender-monitor` 2→3, `koalastuff/eu-ted-tender-monitor` 2→3,
   `koalastuff/fda-enforcement-report-finder` 2→3, `getascraper/sec-form4-insider-monitor` 2→3, and three
   that FELL: `usta/remote-jobs-feeds` 3→1, `martc03/regulatory-monitor-mcp` 2→1,
   `riadh_chebbi/apple-app-store-reviews-scraper` 3→1. **Two could not be a blind number swap** (see
   LEARNINGS): `riadh_chebbi` lives in a paragraph premised on "every unnamed listing with 3+ users", so
   it became "(1 user today, 3 when that sweep ran)"; `eu-ted-tenders-scraper` grouped three handles under
   one shared "(2 users **each**…)" and only two of the three moved, so the shared count was split into
   three explicit per-handle counts. Shipped as 10 README-only builds, **all 11 builds (incl. FEC)
   SUCCEEDED with all 11 live READMEs byte-identical to disk**; checker re-run after: **875 claims, 0
   stale.**

3. Standing checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-readme-samples` 35+82/0,
   `check-comparison-breadth` 23/0, `check-own-price-freshness` 24/0. All 3 services active; site `/`,
   `/tools`, `/tools/fec-campaign-finance-scraper`, `/pricing` all 200. Inbox: long-vetted noise only.
   Revenue/traffic unchanged ($0, 44 users, 579 runs30d) — no owner email.

## What 1331 closed

1. **QUALITY/GROWTH slot — `enum_audit` on `apple-podcasts-scraper` (797 → 1331) — DONE, 91 missing
   `chartGenre` subgenre values found and shipped, build 0.1.69.** Re-derived fleet-oldest directly
   from `audit_dates.json`: `enum_audit` at 797 (never done on this Actor since launch) was by far the
   oldest entry across both real axes (`varied_test` fleet-oldest was 1075). Pulled Apple's own genre
   tree live (`ws/genres?id=26`) and found `chartGenre`'s whitelist had only the 19 TOP-LEVEL categories
   — Apple's tree has **91 more real leaf subgenres** underneath them (Christianity/Islam/Judaism under
   Religion & Spirituality; Soccer/Football/Basketball under Sports; Business News/Tech News/Politics
   under News; etc.), each with its own per-genre chart feed on the exact same endpoint our code already
   calls. **Verified live these are genuinely distinct charts, not a filtered view of the parent**:
   Judaism/Islam top-10s share zero titles with each other or the overall Religion & Spirituality chart;
   Soccer's top-10 shares zero titles with the overall Sports chart.
2. **Shipped all 91 as new `CHART_GENRE_IDS` map entries + matching `input_schema.json` enum/enumTitles**
   (111 values total incl. the existing `""` overall-chart option) — camelCase keys generated
   programmatically from Apple's subgenre names, checked for zero collisions against the existing 19 keys
   and each other before writing. Cross-verified main.js's key SET and the schema's key SET are exactly
   identical (not just same length) before shipping. README input table + FAQ updated to say 110 values
   (19 + 91), not the stale "19 genres" line.
3. **No other enum field on this Actor needed changes — recorded so it isn't re-derived:** `chartType`
   (shows/episodes) is Apple's only 2 chart types; `explicitFilter`/`sort` are this product's own filter
   vocabulary, not an Apple-API enum, so there's no external vocabulary to diff them against.
4. Verified live byte-identical (README 41,023==41,023 bytes; `chartGenre` enum/enumTitles both match disk
   exactly) via the build's own `actorDefinition`. **Platform-verified end-to-end**: default regression
   SUCCEEDED 5/5 unaffected; two NEW subgenre values (`christianity`, `soccer`) run live through the Actor
   matched the direct Apple API exactly; an unrecognized `chartGenre` still falls back cleanly with a
   warning (no crash). `check-pricing` 24/29/0, `check-charges` 24/24. `audit_dates.json` updated with
   `indent=1` (surgical 2-line diff — first `package.json` bump attempt via `json.dumps` reformatted the
   whole file, reverted before committing, same recurring trap as cycles 1327/1328).
5. Inbox checked: same long-vetted noise classes only, plus two more JP/IT-style contact-form
   autoresponders (`co-sol.ca`, `adkm.it`) — same noise class, not new. Nothing actionable, no support
   requests. Dev.to: last published 2026-10-04T19:02Z, 2 days out, right at the cadence edge, not clearly
   due — no article written this cycle (time-boxed).
6. Revenue/traffic unchanged: $0, no owner email warranted. All 3 services active, site `/`, `/tools`,
   `/tools/apple-podcasts-scraper` all 200.

## What 1330 closed

1. **`competitor_audit` on `nih-reporter-scraper` (1284 → 1330) — DONE, clean resweep + 1 user-count
   drift fixed, build 0.1.38.** `niche-unnamed` re-swept clean: 274 seen, 51 matched, README names all
   51 — 0 unnamed, no new listing since 1284. Live-priced all 51 named handles end to end (headline
   price + FULL `eventTieredPricingUsd` map per tiered listing, not just the FREE tier that
   `check-price-superiority`'s `price_of()` reads) via a one-off script reusing that script's helpers.
   Every cited price matched exactly, including both already-published full per-tier breakdowns
   (`themineworks/nih-reporter-grants` $0.001→$0.0006, `publicmoney/nih-reporter-grants-scraper`
   $0.002→$0.0007) and the `tagadanar/us-grants-monitor` citation (its `award-record` event, $0.003
   Free + $0.001 start, is correctly the one cited for NIH data even though Apify's Store
   `isPrimaryEvent` flag points at a DIFFERENT event on the same Actor, `opportunity-found`, which
   prices its separate Grants.gov-opportunities product — `isPrimaryEvent` is a Store-display choice,
   not a per-dataset truth, when one Actor sells two things). One real drift found:
   `mambalabs/public-award-monitor`'s user count moved 2 → 3 (+50%, past the 10% tolerance) — fixed;
   its tiered price map itself is unchanged. Shipped README-only, verified live byte-identical
   (35645==35645 bytes) via the build's own `actorDefinition.readme`; real platform smoke run
   SUCCEEDED (10/10 rows). `check-pricing` 24/29/0, `check-charges` 24/24. Fleet-wide
   `check-price-superiority` separately confirms 0 undisclosed cheaper rivals anywhere (1391 compared).
   `audit_dates.json` updated.
2. Inbox checked: same long-vetted noise classes only. Nothing actionable, no support requests.
3. Revenue/traffic unchanged: $0, no owner email warranted. All 3 services active, site `/`, `/tools`,
   `/tools/nih-reporter-scraper` all 200.

## What 1329 closed

1. **`competitor_audit` on `clinicaltrials-scraper` (1283 → 1329) — DONE, clean resweep + 2 new exact ties
   and 2 traps correctly handled, build 0.1.54.** Re-derived fleet-oldest from `audit_dates.json` directly
   (`scholarship-scraper` still correctly skip-listed until 2026-10-20). Fresh full-cohort sweep: 153 seen,
   121 matched, 74 unnamed (up from 152/120/85 at 2026-10-05) — **completeness holds, no real new
   undercutter.** The `>=3`-user cut cleared only `funnyvalentine69/fda-drug-pipeline-intelligence` (3u,
   $0.005/row) and `red.cars/drug-intelligence-mcp` (3u, $0.03/call) — both AI-synthesis/MCP multi-source
   products out of scope by shape and dearer anyway. Live-priced the full 74-listing unnamed tail via a new
   reusable `bin/_batch_price_cts.py`: two previously-unnamed exact ties at our $0.0015/study rate —
   `aurenic/clinicaltrials-scraper` (2u, ties the rate but also bills a $0.00005 start fee we don't charge,
   so dearer overall) and `realai_pl/recruiting-clinical-trials` (2u, no start fee but scoped to
   `overallStatus: RECRUITING` only, not a full substitute) — plus two sub-$0.002-headline traps correctly
   excluded (`malekh/clinical-trial-protocol-amendments` and `red.cars/clinical-trials-mcp`, both advertise
   a $0.00001 dataset-item event but their real charges are $0.05-$0.75 per non-row event). Spot-checked all
   previously-named headline rivals live (`parseforge`, `logiover`, `bovi`, `ryanclinton`, `pink_comic`,
   `devilscrapes`, `scrapepilot`, `alizarin_refrigerator-owner`, `quotient_variablebarrier`, both `labrat011`
   listings, `webdata_labs`) — all matched published figures exactly except `parseforge` ticking 46→47 users
   (inside the 10% tolerance, not restated). Shipped README-only, build 0.1.54 (package.json 0.1.14→0.1.15),
   verified live byte-identical (43,074==43,074 bytes) via the build's own `actorDefinition.readme`; real
   platform smoke run SUCCEEDED (12/12 rows, no regression). `check-pricing` 24/29/0, `check-charges` 24/24.
   `audit_dates.json` updated with `indent=1` preserved (diff checked — only the touched lines moved).
2. Inbox checked: same long-vetted noise classes only (Bytewells pitch, `searchindex.pro` SEO scam, JP/IT
   contact-form autoresponders, DMARC report, a bounce). Nothing actionable, no support requests.
3. Revenue/traffic unchanged: $0, no owner email warranted. All 3 services active, site `/`, `/tools`,
   `/tools/clinicaltrials-scraper` all 200. Committed (`29ef602`) and pushed to `origin/main`.

## What 1328 closed

1. **QUALITY/GROWTH slot — `enum_audit` on `fda-recall-scraper` (797 → 1328) — DONE, 3 MISSING enum values
   + 1 silent-row-loss disclosure found and shipped, build 0.1.50.** Re-derived the stalest axis fleet-wide
   from `audit_dates.json`: `enum_audit` (797, tied `apple-podcasts-scraper`/`fda-recall-scraper`) — picked
   the FDA one because openFDA's `count=<field>.exact` makes cycle 828's **bidirectional** facet-diff possible
   (the 797 pass predated that method and could only ever find *dead* values, never missing ones). 9 requests
   gave the complete live vocabulary for all 3 enum fields × 3 endpoints. Findings:
   - **`classifications` was missing a real 4th value `Not Yet Classified`** (food 2 / drug 2 / device 1):
     selecting Class I+II+III was **not** equivalent to leaving the filter empty, and those rows were
     unreachable through the filter entirely.
   - **`voluntaryMandated` was missing `N/A`** (6 / 23 / 8 = 37 rows), FDA's own value for an uncaptured
     initiating party. A further 23 rows (1/12/10) carry an **empty** value — documented as only reachable
     with the filter off, since our `''` option means "no filter".
   - **`dateField` was missing `center_classification_date`** — a real range-queryable *and* sortable date
     field on all 3 endpoints at ~99.99% coverage, i.e. **better covered than the `termination_date` we
     already shipped.**
   - **Disclosure gap (the highest-value find for buyers): `dateField=termination_date` silently shrinks the
     CORPUS, not just the window.** `_exists_` counts: food 27,958/29,471 (~5% lost), drug 14,810/18,002
     (~18%), device **25,491/40,113 (~36%)**. A row with no value in the chosen date field can never be
     returned however wide the window, so `termination_date` is the wrong field for any "how many recalls"
     total. Now a README FAQ table + input-table note + schema warning.
2. **Both new enum values needed the schema AND the client-side allowlist in `main.js` patched**
   (`CLASSIFICATIONS`, `VOLUNTARY_MANDATED`, `DATE_FIELDS`) — cycle 838's lesson, live again: the allowlist
   silently coerces an unrecognised value away, so a schema-only fix would have shipped a dead dropdown
   option. `riskScore` already scored an unknown classification with a neutral severity component (no change).
   Also fixed the now-misleading `order` enumTitles ("Newest **report date** first" → "Newest first (by the
   date field above)") since there are 4 date fields now.
3. **CLEAN/CLOSED on this Actor — do not re-derive:** `status` facets to exactly Ongoing/Completed/Terminated
   on all 3 endpoints, so `Pending` remains real-vocabulary-but-zero-data (existing warning is correct);
   every facet set reconciles **exactly** to the endpoint grand totals (29,471 / 18,002 / 40,113), proving
   there are no blank `status` or `classification` rows; `productTypes` is complete — openFDA's own
   `/download.json` manifest lists `enforcement` under food, drug and device **only**
   (tobacco/animalandveterinary/other all 404), so there is no 4th endpoint to add.
4. Verified live: 3 local runs proved each new value returns exactly the facet-predicted rows (5 for
   `Not Yet Classified`, the `N/A` rows in correct `center_classification_date` sort order); one apparent
   zero-row result was checked against the API directly and was a **genuine** zero (newest `N/A` drug row is
   2023-11-16, so a 2025 window correctly returns nothing) rather than a bug. Live README byte-identical
   (51,230 bytes) via the build's own `readme` field; **platform smoke run SUCCEEDED** (2/2/1 = 5 rows).
   `check-pricing` 24/29/0, `check-charges` 24/24. `audit_dates.json` updated with `indent=1` (this file's
   real indent). The `input_schema.json` edit was done with surgical `Edit` calls, not `json.dumps` — the
   first attempt reformatted the whole file (424 lines) because it hand-formats short arrays inline; caught
   and reverted before committing, same trap as cycle 1327.
5. Inbox: same long-vetted noise classes only (bytewells pitch, `searchindex.pro` SEO scam, JP/IT
   contact-form autoresponders, DMARC report, one bounce). Nothing actionable, no support requests.
   Revenue/traffic unchanged: $0, 44 users, 577 runs30d, 0 bookmarks/reviews — no owner email. All 3 services
   active, site `/`, `/tools`, `/tools/fda-recall-scraper` all 200.

## What 1327 closed

1. **`competitor_audit` on `ats-jobs-scraper` (1281 → 1327) — DONE, clean resweep + 1 stale user count
   fixed, build 0.1.66.** The >=3-user unnamed cohort (39 listings this time, composition changed from
   44) was fully live-priced via a new reusable `bin/_batch_price_ats.py` — **zero new undercutters**,
   every one dearer than our GOLD+ rate at every tier; `vnx0/lever-ats-job-scraper` and
   `chilly_damask/company-careers-job-scraper` (both 8u, flat $0.001/job) only tie our FREE tier, same
   shape as the already-named `wickfeed` tie.
2. **Resolved (as far as possible) the `illehius/ats-jobs-scraper` ambiguity flagged since 1281:**
   attempted a real test run to see which of its two charge events actually fires — got `403
   public-actor-disabled`, confirming **our Apify plan cannot run ANY public Actor at all**. This is
   permanent, not a "recheck when it grows users" item — documented so no future cycle retries it.
   User count updated 1→4 in the note regardless.
3. Spot-checked all 20 previously-named headline rivals' full tiered price maps live — all unchanged
   except `openclawai/career-site-ats-jobs-scraper`'s user count (19→22, +16%, past tolerance), fixed.
   Own price re-verified first, zero drift.
4. Verified live byte-identical via the build's own `readme` field (43,036 bytes); post-push smoke run
   SUCCEEDED (50/50 rows, no regression — this Actor's `companies` input is `{ats,slug}` objects, not
   `"provider:slug"` strings, learned the hard way on the first smoke-test attempt). `check-pricing`
   24/29/0, `check-charges` 24/24. `audit_dates.json` updated with `indent=1` (this file's real indent
   — caught an accidental `indent=2` whole-file reformat before committing, see LEARNINGS.md).
5. Inbox: same long-vetted noise classes only, nothing actionable. Revenue/traffic unchanged: $0, no
   owner email. All 3 services active, site `/`, `/tools`, `/tools/ats-jobs-scraper` all 200.

## What 1326 closed

1. **`competitor_audit` on `court-records-scraper` (1280 → 1326) — DONE, completeness holds, one real
   drift fixed, build 0.1.49.** `niche-unnamed` re-swept clean: 434 seen/30 matched, README names all
   40 handles, **0 unnamed** — no new rivals since 1280's full-cohort sweep. Live-reread `pricingInfos`
   for the 7 closest-named rivals rather than trusting the 1280 prose: 6/7 exact, but
   `haketa/federal-court-records-scraper` drifted on both counts it's named for — users 9→11 (+22%,
   past the 10% tolerance) and the tier claim was wrong. README said it undercuts us only on Diamond
   ($0.0018); the full `eventTieredPricingUsd` map shows GOLD and PLATINUM are also flat $0.0018 (below
   our $0.002 flat), so it undercuts from **GOLD up**, three tiers not one. Fixed both, dated
   2026-10-06. `pink_comic` ticked 15→16 users but stayed inside tolerance — left alone. Verified live
   byte-identical via the build's own `actorDefinition.readme` (41,042==41,042 bytes); real platform
   smoke run SUCCEEDED (12/12 rows, one transient upstream CourtListener timeout+retry, no regression).
   `audit_dates.json` updated — new fleet-oldest is `ats-jobs-scraper` (1281).
2. **Found and fixed a 2-cycle git commit backlog.** Cycles 1324 (`trademark-search-scraper`) and 1325
   (`clinicaltrials-scraper`) both shipped real Apify builds and updated state files, but neither
   cycle's working tree was ever committed — last commit on `main` was `ad2c727` (cycle 1323). Committed
   each backlogged fix separately (`29cb2b6` for 1324, `f9b0116` for 1325) plus this cycle's own fix
   (`163b25e`), then pushed all three to `origin/main`. **Lesson for future cycles: verify `git status`
   is clean (or commit your own diff) before ending every cycle — the STATUS.md/queue.md write-up alone
   does not guarantee the code change was committed.**
3. Inbox checked: same long-vetted noise classes only (Bytewells pitch — re-open trigger stays
   2026-11-02 — plus the usual SEO scam / JP/IT autoresponders / DMARC / bounce). No support requests.
4. Revenue/traffic unchanged: $0, no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/court-records-scraper` all 200.

## What 1325 closed

1. **Owed QUALITY/GROWTH slot — `varied_test` on `clinicaltrials-scraper` (1073 → 1325) — DONE, real
   bug found and fixed, build 0.1.53.** The file's own precedence comment claimed "a typed input for
   the same key overwrites" a `startUrl`'s `aggFilters` code, but that was only coded for 3 of the 10
   UI sidebar codes (`docs`/`results`/`violation`, which share one Map with their typed equivalents).
   The other 7 (`status`/`phase`/`studyType`/`sex`/`healthy`/`ages`/`funderType`) route through a
   separate mechanism (`filter.overallStatus` / `AREA[...]filter.advanced`) that never touched the
   `startUrl`'s code — so a pasted URL's `aggFilters=status:rec` plus a typed
   `overallStatus:["COMPLETED"]` silently ANDed into a contradiction instead of the typed value
   winning. **Verified 3 ways live:** direct CT.gov API (rec alone=18,747, COMPLETED alone=53,394,
   both=**0**); reproduced through the Actor pre-fix (`declaredMatches:0`, generic "No studies
   matched" advice, no mention of the real cause — same undisclosed-contradiction shape as cycle
   1028's `resultsAvailability`+`resultsFirstPostedDate` fix); post-fix the same combo returns 5/5
   genuinely-`COMPLETED` rows. Two regressions confirmed clean: non-conflicting `startUrl`
   (`status:rec,phase:3`, no typed override) still 5/5 `RECRUITING`+`PHASE3`; plain no-`startUrl`
   search still filters correctly. Fix: delete the `startUrl`'s aggFilter-code entry for any of the 7
   keys whose matching typed input is set, before the `aggFilters`/`AREA[...]` params are built.
   Shipped README (new FAQ entry + input-table note) + source, build 0.1.53 (source
   0.1.13→0.1.14), verified live byte-identical via the build's own `actorDefinition.readme`
   (40,810==40,810 bytes) + 3 phrase probes. `check-pricing` 24/29/0, `check-charges` 24/24.
   `audit_dates.json` updated — this Actor's `varied_test` note now documents the fix.
2. Inbox checked: `peter@bytewells.com` "monthly rentals for ats jobs scraper" looked new but is the
   same already-diligenced-and-declined Bytewells pitch, just worded around a different Actor —
   re-open trigger stays **2026-11-02**, not before. Everything else is the long-vetted noise classes.
   No support requests.
3. Dev.to cadence checked **by hitting the API directly**: last published 2026-10-04T19:02Z, cadence
   1/2-3 days, not clearly due — no article written this cycle (time-boxed; the bug fix above was the
   higher-value use of the cycle).
4. Revenue/traffic unchanged: $0, no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/clinicaltrials-scraper` all 200. $0 spent beyond the one build + a handful of small
   self-charged verification runs.

## What 1324 closed

1. **`competitor_audit` on `trademark-search-scraper` (1278 → 1324) — DONE, three stale whole-niche
   aggregates + one stale user count fixed, build 0.1.38.** Niche grew on BOTH counts: `niche-size`
   default 108 → **114** mentions, `--strict` 84 → **89** real trademark products (543 distinct seen).
   The README still published `108/84` AND the cycle-1212 bookkeeping *"names 37 of the niche's 84 …
   priced all 47 that it does not"* — re-derived mechanically (strict matched set minus full-handle
   substring match) that is **89 matched / 58 named / 31 unnamed**, i.e. three numbers wrong at once.
   All 31 live-priced end to end via a new reusable `bin/_batch_price_tmss.py` (55 default-mode unnamed
   priced; the 31 strict ones are the real niche). **COMPLETENESS HOLDS** — zero undercutters, the
   7-undercutter set is still the full set. Closest unnamed is
   `unrivaled_fortress/wipo-global-trademark-brand-watch` at $0.0026/row GOLD+ (1.3x ours, a new-filings
   feed not a register search), then `axiomworks` at $0.002975 GOLD+. **13 listings named for the first
   time** (10 never priced before + `friendlyapi`/`automation_studio`/`stefano_seggio`, which 1278 priced
   but never named by handle), incl. `devilscrapes/uspto-trademark-scraper` ($0.005/result + a **$0.20
   actor-start**, dearest start fee in the niche) and `neverempty/uspto-trademark-search-monitor` (closest
   in SHAPE — a real USPTO text/owner/class search + monitoring, $0.008→$0.005/row). Sub-$0.002 trap
   re-checked: 7 of the 31 advertise a sub-$0.002 event and **not one is a row price** (6 actor-start
   fees + `neverempty`'s $0.0005 monitoring check). Also fixed `dev00/uspto-trademark-api` 59 → **68**
   users (+15%, now past `check-competitor-claims`' 10% tolerance; was 62/within-tolerance at 1212) —
   that check now reports 14 stale fleet-wide, none on this Actor. Verified live byte-identical via the
   build's own `actorDefinition.readme` (32662 == 32662 bytes) + 5 phrase probes; post-push smoke run SUCCEEDED
   (solar/US+EM/class 9/Registered → 20 rows of 1,436 declared). `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-own-price-freshness` 0 flags. `audit_dates.json` updated. Full write-up
   in STATUS.md cycle 1324.
2. **WATCH ITEM re-verified live and STILL PENDING, do not re-derive it:** both `dev00` listings' filed
   change is still `startedAt 2026-10-14T16:43:52.372Z` and still **FREE-plan-only**
   (`uspto-trademark-api` trademark-verify flat $0.003 → FREE $0.10 / BRONZE+ $0.003;
   `uspto-trademark-text-check-api` $0.005 → FREE $0.10 / BRONZE+ $0.005). The README already states this
   with exact numbers — a cycle on/after **2026-10-14** need only flip the tense. Do **not** read it as a
   general price rise.
3. Inbox checked: same long-vetted noise classes only (bytewells pitch, `searchindex.pro` SEO scam,
   Japanese/Italian contact-form autoresponders, DMARC report, one bounce). Nothing actionable, no
   support requests.
4. Revenue/traffic unchanged: $0, 44 users, 564 runs30d, 0 bookmarks/reviews — no owner email. All 3
   services active, site `/`, `/tools`, `/tools/trademark-search-scraper` all 200.

**New standing note for this Actor (3-for-3 failure mode):** the stale-whole-niche-aggregate defect has
now hit `trademark-search-scraper` at 1212, 1278 and 1324. Its niche grows every ~45 cycles, and no
standing check we own catches a count sentence. **Always re-run `niche-size --strict` AND re-derive the
named/unnamed split mechanically before trusting any count in this README.**

## What 1323 closed

1. **`competitor_audit` on `uk-find-a-tender-scraper` (1277 → 1323) — DONE, 3 real undercutters found and
   disclosed, build 0.1.59.** Niche re-swept to 102 matched (up from 99); the `>=3`-user cut came back
   empty again (19 unnamed, all 1-2u), so the whole tail was live-priced via a new reusable
   `bin/_batch_price_uktft.py`. New finds: `jtpalms/gov-tenders-monitor` and
   `thriftykiwi/public-tenders-aggregator` (single-portal, cross over ~38-42 rows),
   `optimistprime/uk-eu-public-tenders` (genuine FTS+CF+TED 3-source substitute, crosses over ~129 rows
   on Gold+), plus `compass_lab/uk-tenders-scraper` (dual-portal, dearer). Two listings
   (`mikee368/eu-tender-monitor`, `dobus/eu-uk-public-tender-intelligence-api`) matched the sweep's search
   terms but read **no UK portal at all** on inspection of their own description — a title-only read would
   have miscounted both. Verified live via the build's own `readme` field; post-push smoke run SUCCEEDED
   (15/15 rows, no regression). `check-pricing`/`check-charges`/`check-own-price-freshness` all clean.
   `audit_dates.json` updated. Full write-up in STATUS.md cycle 1323.
2. Inbox checked: same long-vetted noise classes, nothing actionable, no new support requests.
3. Revenue/traffic unchanged: $0, 44 users, 564 runs30d — no owner email.

## What 1322 closed

1. **QUALITY/GROWTH slot — `varied_test` on `google-news-scraper` (1071 → 1322), DONE, real finding
   fixed.** Tested the never-before-tried combo `decodeUrls:false` + `fetchArticleBody:true`. Found
   `main.js` silently forces `decodeUrls` back on whenever `fetchArticleBody` is on (needs the real URL
   to fetch the body) — only logged as a run-log warning, never disclosed in README/schema. Proven live
   on a real `"Tesla"` query: `url` still came back fully resolved (`teslarati.com`, `futurism.com`)
   despite `decodeUrls:false`. Not a code bug (the override itself is correct and necessary) — fixed
   the disclosure: new FAQ entry + input-table/schema notes, pointing to `googleNewsUrl` as the escape
   hatch for the raw link. Shipped README/schema-only, build 0.1.63, verified live via the build's own
   `readme` field; post-push smoke run clean, no regression. `check-pricing`/`check-charges` both
   clean. Full write-up in STATUS.md cycle 1322 and `audit_dates.json`'s `varied_test_note`.
2. Checked dev.to cadence **by hitting the API directly**, not a copy-forwarded note (cycle-997
   lesson) — last published 2026-10-04T19:02Z, cadence is 1/2-3 days, genuinely not due. No article
   written this cycle.
3. Inbox checked: nothing actionable, same long-vetted noise (DMARC report, `searchindex.pro` SEO
   scam, Japanese/Italian contact-form autoresponders, a bounce). No new pitches, no support requests.
4. Revenue/traffic unchanged: $0, 44 users, 564 runs30d — no owner email.

## What 1321 closed

1. **`competitor_audit` on `sam-gov-opportunities-scraper` — DONE, clean (build 0.1.43).** Rotation
   moved 1275 → 1321. Niche grew 140 → 145 matched; the `>=3`-user cohort was empty again (max 2u), so
   per the standing full-cohort rule all 80 unnamed listings were live-priced via a new reusable
   `bin/_batch_price_sgos.py`. **Zero new findings** — no free rivals, no undercutters anywhere in the
   80. Also spot-checked the 6 headline undercutters already named in the README (`jungle_synthesizer`,
   `scrapesage`, `yourwingman`, `acid-base`, `bridged`, `gochujang`) live — zero drift on any of them.
   Shipped README-only, verified via the build's own `readme` field; post-push smoke run SUCCEEDED (1/1
   row, 1 charge, no regression). Full write-up in STATUS.md cycle 1321 and `audit_dates.json`'s
   `competitor_audit_note`.
2. Inbox checked: all noise classes already catalogued, plus one new one worth recording — a
   cold-outreach email from `capsule26.com` (self-described autonomous AI agent business) asking a
   genuine technical question about our watch-mode-rebilling postmortem. Not a support request, not
   revenue, no reply needed/sent. Another `bytewells.com` pitch also arrived (same pitch as before,
   still correctly declined per the 1316 diligence — re-open trigger not before 2026-11-02).
3. Revenue/traffic unchanged: $0, 44 users, 564 runs30d, 0 bookmarks/reviews — no owner email.

## What 1320 closed

**`competitor_audit` on `grants-gov-scraper` — DONE, two real README corrections shipped (build
   0.1.51).** Rotation moved 1273 → 1320. Priced the whole niche live, both halves: all **53 unnamed**
   listings AND all **34 already-named** rivals, every event and every tier (87 live GETs). Niche is now
   **87 matched** (was 85). Full write-up in STATUS.md cycle 1320 and `audit_dates.json`'s
   `competitor_audit_note`.
   - **Unnamed tail is CLEAN** — zero undercutters, zero FREE-model listings. **Do not re-flag
     `tagadanar/us-grants-monitor`**: its `$0.001` is an `actor-start` RUN FEE, not a row price; its real
     row event is `$0.004 → $0.0028` (GOLD+), 1.9–2.7x ours. Named in the README so it stays closed.
   - **Two named rivals were TIERED where we had published FLAT**, both fixed:
     `vhsgreed/us-federal-contracts` (`record` $0.00125/$0.00115/$0.00105/$0.00095 — our published "~8
     rows" break-even was its FREE tier only; really ~8/~5.7/~4.4/~3.6, so paid-plan buyers cross over
     twice as early as we said) and `upward_enterprises/grants-gov-opportunity-finder` (detail
     $0.003→$0.0024, summary $0.001→$0.0008; "dearer at both tiers" conclusion survives at every plan).
   - **Recurring failure mode worth remembering, not re-discovering:** this is the *second* time this
     Actor's README published a FREE-tier price as if it were flat (cycle 1233 self-corrected
     `shahidirfan`/`chorelet` the same way). When auditing ANY niche, read the full
     `eventTieredPricingUsd` map — `bin/check-price-superiority`'s `price_of()` returns the **FREE tier
     only**, which is exactly how both of these got published wrong.

## Open for 1324 (next BUILD/AUDIT cycle)

1. **`competitor_audit` fleet-oldest: `trademark-search-scraper` (1278)** < `court-records-scraper` (1280)
   < `ats-jobs-scraper` (1281) < `clinicaltrials-scraper` (1283) < `nih-reporter-scraper` (1284).
   **Re-derive from `audit_dates.json` directly rather than trusting this cached list** — it moves every
   time any Actor is audited.
2. **Other axes, fleet-oldest (for reference — `competitor_audit` is the live rotation):**
   `varied_test` → `google-news-scraper` (1071); `enum_audit` → `apple-podcasts-scraper` / `fda-recall-scraper`
   (both 797); `unreachable_remedy` → has **no never-done candidates left** (closed fleet-wide at 1318);
   re-ranking fleet-oldest among its 24 done entries is the only way to revisit it, and no re-sweep is
   due — **don't pick it as a top task.**
3. **Loose thread, not urgent, for a future `remote-jobs-scraper` `competitor_audit`** (carried from
   1319): verify live whether `datafetch_labs/remote-jobs-scraper` has a genuinely structured
   "region-style" location filter that our `locationKeyword` substring match does not match. Flagged
   honestly in that README as unverified rather than conceded. **The board-count gap itself is CLOSED
   (WWR added as a 7th board at 1319) — do not re-add WWR or re-litigate it.**

**Standing constraints, unchanged:**
- **SKIP `scholarship-scraper` entirely** (it is fleet-oldest on every axis and will keep surfacing):
  bold.org has 429'd it since 2026-09-20, decision point **2026-10-20** (cycle 1292). That date has NOT
  passed as of 2026-10-06 — check it before touching this Actor at all.
- **Axis-ranking rule, settled, stop re-litigating:** only `varied_test`, `enum_audit`,
  `unreachable_remedy`, `competitor_audit` are real fleet-wide rotations (24 entries each).
  `count_audit`, `input_error_advice`, `description_mine`, `watch_subset_audit`, `search_scope_audit`
  are one-off experiments (cycle-1304 LEARNINGS entry) — never rank them against the 4 real axes.
- **`competitor_audit` method:** run `bin/niche-unnamed` first; if the >=3-user cut is thin or empty,
  live-price the WHOLE unnamed tail, and if it is large, live-price the whole >=3-user cut anyway
  (reuse the `_batch_price_*.py` `SourceFileLoader` pattern with `raw_events` + `startedAt` so finalist
  tiers need no second round of calls); **never rule a listing out of scope on TITLE ALONE** — read the
  live Store description, and for anything that looks like a real substitute read its latest build's
  `actorDefinition.readme` + input schema too; verify full `pricingInfos` event maps by CURRENT
  `startedAt` across MULTIPLE tiers before naming anyone. A low price in a listing's TITLE is
  marketing, not a price. **Also distinguish a per-ROW event from an `actor-start` RUN FEE before
  calling anything an undercutter** (cycle 1320's `tagadanar` false positive — `isOneTimeEvent` is
  `false` on some start fees, so that flag alone will not save you). Diff published prose against live
  prices in BOTH directions, not just "did anyone undercut us" (cycle 1288).
- **Bytewells — DILIGENCED AND DECLINED at 1316. Stop re-flagging it.** Payout geography is
  dispositive (EU/EEA/UK only; owner is in Egypt), PPE unsupported at launch, and their API-key import
  wants full Apify account access. **RE-OPEN TRIGGER — not before 2026-11-02** (their stated public
  launch), and only if Egypt appears in the payout-country answer at
  `https://bytewells.com/developer-waitlist`. Their pitch mail keeps arriving; it is noise now.
- **Inbox:** nothing actionable as of 1320. All remaining mail is the long-vetted noise classes (DMARC
  reports, `searchindex.pro` SEO scam, Japanese/Italian contact-form autoresponders, the `j_woodgate01`
  advance-fee pitch, the `bytewells.com` pitch, the owner's stale scholarship-scraper forward, one
  bounce). No support requests outstanding.
- **Polar checkout stays deferred** by owner decision — do NOT ask for it unless `bin/traffic` shows
  >100 visits/day to `/pricing` or `/tools`, or a real purchase request lands in the inbox.
