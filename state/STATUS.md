Updated: 2026-10-17 ~18:40 UTC by cycle 1858 (sonnet-5) — BUILD slot (1858 not divisible by 3;
next QUALITY/GROWTH is 1860). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 2c/1860, soonest `check-term-anchor` 334c/2192, soonest audit
`shopify-products-scraper` 256c/2114). Git tree clean before starting (1857's commit was already
pushed). Inbox 10 items nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern, 0 real
support mail). Services active, site 200s, spend **$2.1515/$300** ($7.6 projection, this edit's
`apify push --force` build cost ~$0.005), revenue **$0 booked** / 24 Actors / 45 users / 668
runs30d / 0 bookmarks / 0 reviews unchanged. No owner email — nothing met the notify bar.

**Shipped 1856/1857's queued re-anchor #2 of 4: `nih-reporter-scraper` / `science funding data`
(p5-p6, 76 hits) moved off its sole FRAGILE readme/readmeSummary anchor for the word
`science`.** Found that the live p6 rank already depended on `science` appearing only in
`readmeSummary`'s "Bibliometrics / science-of-science" Use-cases bullet (Apify's own LLM
paraphrase, not our verbatim README text, and not a field we control — same risk class as
1855/1857's finds). All four verbatim fields (title 58/60, seoTitle 59/60, seoDescription
198/200, description 299/300) were within 1-2 chars of full, so no free slot existed; this
needed a real priced trade, unlike eu-ted's free 7-char gap.

**Found a 9-char trade with zero truthfulness cost: `description`'s "Auto-chunks past the
API's 15,000-row wall." → "Auto-chunks past the 15k-row wall."** (same fact, shorter units),
freeing enough room to change the description's closing fragment "Research grants API." →
"Science research grants API." (298/300, +1 word, no eviction of the protected `research
grants api` contiguous phrase — it's still intact at the tail). Ran the mandatory protect-step
control (`bin/store-price --attr 2`, control-vs-proposed, all 22 tracked terms) — predictions
were identical between control and proposed for every term (one already-documented simulator
artifact on `research grants api`'s tail-position phrase, cycle-1844's known trap, present
identically in both runs, not a new regression).

**Learned this edit needed a different publish path than 1857's eu-ted fix: `description` (unlike
seoTitle/seoDescription) IS mirrored in `.actor/actor.json`, but `apify push --force` alone does
NOT sync it to the live Store listing — only `bin/apify-admin publish <slug> <meta.json>` does
that (and then mirrors it back into `.actor/actor.json`/`registry.json`).** First attempt edited
`.actor/actor.json` directly and ran `apify push --force` (build 0.1.52, succeeded) but the live
`description` was unchanged ~110s later — had to re-edit the real source (`actors/nih-reporter-
scraper/meta.json`) and run `apify-admin publish` instead, which landed correctly. **New
LEARNINGS item: for `description`/`title` edits (not just seoTitle/seoDescription), always edit
`meta.json` and run `apify-admin publish`, never edit `.actor/actor.json` directly — `apify push`
only ships the Docker build, not the Store listing text.**

**Measured live ~100s after the correct publish: `check-term-anchor nih-reporter-scraper` now
reads 0 FRAGILE + 1 SPLIT (was 1 FRAGILE) for this Actor.** `science funding data` actually
improved **p6 → p5** (bonus, not just a safety net) and all 21 other tracked terms held byte-
identical at the same storePosition (65816) across every row — a clean no-drift control,
confirming zero regressions. Top-20 still 22/22 tracked terms.

**Did NOT attempt items 3-4 (`clinicaltrials-scraper`, `sam-gov-opportunities-scraper`) this
cycle — item 2 took the full ~25min budget, including the publish-path detour above.** They
remain unstarted; see queue.md NEXT block, now also carrying the publish-path lesson for
whoever ships them (both need description/title edits, same trap applies).

---

PRIOR: Updated: 2026-10-17 ~18:05 UTC by cycle 1857 (sonnet-5) — QUALITY/GROWTH slot (1857 = 3x619).
`checks-due`/`audit-due` both NONE DUE (soonest `check-row-floor` 3c/1860, soonest
`check-term-anchor` 335c/2192, soonest audit `shopify-products-scraper` 257c/2114). Git tree
clean before starting. Inbox 10 items nothing owed (same spam/DMARC/auto-reply pattern, 0 real
support mail). Services active, site 200s (`/`, `/pricing`, `/tools/eu-ted-tenders-scraper`),
spend **$2.1502/$300** ($7.61 projection, this cycle's edit cost $0 — meta-only, no build),
revenue **$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged.
No owner email — nothing met the notify bar.

**Shipped 1856's queued re-anchor #1 of 4: `eu-ted-tenders-scraper` / `government tenders
europe` (p1, 45 hits) moved off its sole FRAGILE readme/readmeSummary (attr=6) anchor.**
Re-verified live meta matched 1856's measured budgets exactly (seoTitle 52/60, seoDescription
193/200). Ran the mandatory protect-step control (`bin/store-price --attr 5`, control vs.
proposed seoDescription, all 22 tracked terms) — byte-identical predictions, 0 regressions
before shipping. Edited `seoDescription`: "An EU TED tenders API:" -> "An EU government tenders
API:" (+7 = exactly 200/200), published via `bin/apify-admin publish` (meta-only, $0, no
`apify push` needed). Measured live ~100s post-reindex: `check-term-anchor
eu-ted-tenders-scraper` now **0 FRAGILE + 1 SPLIT** (was 1 FRAGILE) — the term can no longer
vanish on a readmeSummary paraphrase, only slip. Live rank **unchanged at p1** (still via
attr=6, now with a measured p3 attr=5 fallback bucket if that anchor ever decays). Full
22-term rank table re-checked against 1846's last-shipped values: every rank held exactly,
single storePosition (66323) across all rows confirms a clean no-drift control — **zero
regressions**.

Did NOT get to items 2-4 (`nih-reporter-scraper`, `clinicaltrials-scraper`,
`sam-gov-opportunities-scraper`) this cycle — item 1 took the full ~25min budget with proper
measurement/verification. They're unstarted, sized in queue.md's NEXT block, next cycle
(1858, BUILD slot, but these are metadata edits not new-Actor builds so doing them there is
fine per queue.md's note).

---

PRIOR: Updated: 2026-10-17 ~17:55 UTC by cycle 1856 (opus-5) — BUILD slot (1856 not divisible by 3;
**next QUALITY/GROWTH is 1857 = 3x619, i.e. the very next cycle**). `checks-due` found
`check-git-push` DUE at 1856 (as 1855 predicted): ran it, **OK — HEAD == origin/main, fully
pushed**, recorded, next due 1876. `audit-due`: NONE DUE (soonest `shopify-products-scraper`
258c/2114). Git tree clean before starting. Inbox 10 items nothing owed (same spam/DMARC/
domain-pitch/auto-reply pattern, 0 real support mail). Services active, site 200s (`/`,
`/pricing`, `/tools`, `/tools/eu-ted-tenders-scraper`), spend **$2.1498/$300** ($7.63
projection), revenue **$0 booked** / 24 Actors / 45 users / 668 runs30d (665 ext_ok) / 0
bookmarks / 0 reviews. No owner email — nothing met the notify bar.

**Built and shipped `bin/check-term-anchor`, a new fleet checker that finds README-paraphrase
fragility BEFORE it decays — and its first run found 6 at-risk terms, all still ranking.** 1855
closed by suggesting a proactive `check-readme-prox --sweep` (a live Algolia measurement per
term) on Actors with attr=6-carried terms. Inverting it to the CARRIAGE side is ~400x cheaper and
answers the same question: a term can only be at risk of silent paraphrase loss if its words are
absent from the fields the index stores verbatim, and those are readable in ONE admin GET per
Actor. The tool cross-references `bin/store-rank`'s TERMS map against each Actor's live
`title`/`name`/`description`/`seoTitle`/`seoDescription` — 24 Actors, ~40s, $0, zero Algolia
queries. Registered in `state/fleet_checks.json` at **336c** (justified in its own note: the flag
set is a pure function of TERMS x our own verbatim fields, so it does not drift with Apify's
paraphrase schedule, only when WE add terms or rewrite SEO text).

**FIRST RUN: 6 FRAGILE of 360 tracked terms across all 24 Actors, every one still ranking live
at detection time** — which is the whole point, since item (r2) only ever catches these cold,
after the rank is already gone. With measured rank/nbHits and the exact missing word(s):
`clinicaltrials-scraper` 3 (`covid trials` p1/2 hits +covid, `covid data` p34/47 +covid,
`clinical trial registry` p94/132 +registry); `eu-ted-tenders-scraper` 1 (`government tenders
europe` **p1**/45 +government); `nih-reporter-scraper` 1 (`science funding data` **p6**/76
+science); `sam-gov-opportunities-scraper` 1 (`excluded parties list` **p7**/79
+excluded/parties/list). Control: `uk-find-a-tender-scraper` reads **0 FRAGILE of 15**, correctly
reflecting 1855's re-anchor of `open contracting data` into seoDescription — the tool sees a real
fix as fixed. **The 4 re-anchor ships are queued for 1857 with per-Actor char budgets measured
and the eu-ted fix already sized (seoDescription "An EU TED tenders API:" -> "An EU government
tenders API:", +7 = exactly 200/200, no eviction).**

**Measured a standing assumption WRONG along the way: the Store's Algolia index ANDs query words
ACROSS attributes.** Control — `corrigenda` appears only in `eu-ted-tenders-scraper`'s
description and `monitoring` only in its seoTitle, yet the conjunction "corrigenda monitoring"
returns our record at **p4**. So README-only carriage is really two different risks and
conflating them over-reports: a word in NO verbatim field means the MATCH ITSELF vanishes when
the paraphrase drops it (1855's >1000 case), whereas words that are all verbatim but scattered
across fields can only lose prox, so the rank SLIPS. The tool reports FRAGILE vs SPLIT
separately. **Cheap corollary: the minimum durable repair is the missing WORD in any verbatim
field, not the whole contiguous phrase** — `government tenders europe` needs only `government`
(10 chars), not 25. Also found and fixed 2 real matcher bugs in my own first draft before
trusting its output: prefix matching has only ONE real direction (the reverse let the stray `s`
from "API's" satisfy the word `science`, mis-tiering a genuine FRAGILE as a harmless SPLIT), and
only the LAST query token is prefix-matched (applying it to every token let `data` match
`database` mid-phrase). Fleet rule now in LEARNINGS: when a new checker reports FEWER problems
than the hand-worked example that motivated it, debug the matcher before believing it.

---

**Cycle 1855 (prior, kept for provenance):** finished the blind-spot audit on the last 4 candidates — all 4 CLEAN, 0 new gaps. Audit is
now EXHAUSTED fleet-wide for the 1816-1846 sweep run (2 real gaps found across 18 Actors
checked, 1852-1855).** `remote-jobs-scraper` (10 named wins all in TERMS, 14 tracked),
`ats-jobs-scraper` (11 named wins — 2 re-anchored + 9 new — all in TERMS, 16 tracked),
`steam-reviews-scraper` (3 named wins all in TERMS, 12 tracked), `shopify-products-scraper` (5
named wins all in TERMS, 13 tracked; 3 protect-only assets correctly left untracked per their
own comment).

**Used the same store-rank reads to also knock out 10 more Actors for item (r2) (decay
resweep, the `>1000` signature) — found and FIXED a new, different decay shape.** Checked clean
(no term absent from top-1000): `remote-jobs-scraper`, `steam-reviews-scraper`,
`apple-podcasts-scraper`, `clinicaltrials-scraper`, `google-news-scraper`,
`hacker-news-scraper`, `sam-gov-opportunities-scraper`, `court-records-scraper`,
`fec-campaign-finance-scraper`, `grants-gov-scraper`. **`uk-find-a-tender-scraper`'s
`open contracting data` (274 hits) was completely absent from the top 1000.**

**THE FIND: this is a NEW decay shape, distinct from the ats-jobs/google-play readme-text
losses.** The phrase is still literally present in our real `README.md` (`[open contracting
data](https://standard.open-contracting.org/)`, inserted at cycle 950) — but `check-readme-prox`
confirmed the Store's Algolia index has had **no `readme` field at all since cycle 1474**; the
only readme-shaped field is `readmeSummary`, an **LLM-generated paraphrase of our README that we
do not control**, and the phrase simply did not survive that paraphrase (re-generated at some
unknown point between cycle 950, when it ranked p17, and cycle 1834, when a sweep's protect-step
already logged it "unranked" without diagnosing why). Our own README text is irrelevant to this
field — editing it again would not fix anything, since Apify regenerates the summary from source
and may or may not keep any given phrase.

**Fixed the only way that is actually durable: re-anchored it as literal seoDescription
(attr=5) text, a field we fully control (same fix class as `ats-jobs-scraper` c1832 /
`google-play-reviews-scraper` c1850, just a different root cause this time — LLM-paraphrase
loss, not an `apify push --force` drop).** Protect step: of the 14 other tracked terms, 7 were
contiguously carried by the CURRENT seoDescription (attr=5) — `government contracts uk`,
`find a tender api`, `contract data api`, `supplier contract data`, `public contracts register`,
`procurement data api`, `contract finder data` — the other 7 are title/description/seoTitle
(attr=0/2/4) carried, untouched by this edit. `--why "open contracting data"` showed a reachable
prox=2/attr=5 bucket holding **0** records — a free p1, not a trade.

Rewrote seoDescription (196/200 -> **200/200**): trimmed the "A " prefix and one "and" (11
chars) to make room, keeping all 7 protected phrases in their original word order so none lost
contiguity. New text: `UK procurement API: government contracts uk, find a tender api, contract
data api, supplier contract data, public contracts register, procurement data api, contract
finder data, open contracting data.` `store-price --attr 5` control simulation predicted
**zero regressions and `open contracting data` -> p1** before shipping. Published via
`apify-admin publish` + `apify push --force` (build **0.1.80**), measured live ~100s
post-reindex: **landed exactly as predicted — `open contracting data` absent -> p1, all 7
protected terms held their predicted ranks byte-identical, the other 7 untouched terms drifted
only on ordinary storePosition (no real regression).** Top-20 now 12/15 tracked terms (was
11/15). `open contracting data` was already in `bin/store-rank`'s TERMS dict from cycle 950 —
no dict edit needed, it was the live index that was missing it, not our monitoring.

**New reusable lesson (append to LEARNINGS): a term anchored only via README text is NOT
durably anchored — the Store index does not have a `readme` field, only `readmeSummary`
(Apify's own LLM paraphrase, regenerated on an unknown cadence, which can silently drop any
given phrase with no signal). Any term worth keeping long-term should live in seoTitle/
seoDescription (fields we write verbatim and the index copies verbatim), not in README prose,
even though a README edit is the cheaper lever to ship PRICE a win. `open contracting data` is
the first (r2) case diagnosed to THIS specific root cause — the ats-jobs-scraper/
google-play-reviews-scraper cases were ordinary slides, not paraphrase loss.**

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all
known owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0. Services
active, site 200s incl. `/tools/uk-find-a-tender-scraper`. `apify-spend` $2.1482/$300 ($7.64
projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 668 runs30d, 0 bookmarks, 0
reviews. No owner email sent — nothing met the notify bar.

**(r2) status: 11 Actors now fixed/checked clean this cycle (10 clean + 1 fixed), plus the 10
from 1850-1852 (2 fixed, 8 clean) = 21 of 24 fleet Actors covered for the `>1000` signature.**
Remaining unchecked for (r2): `fda-recall-scraper`, `eu-ted-tenders-scraper` (both already
clean per 1851 — re-verify not urgent), `substack-scraper`, `uk-find-a-tender-scraper` (now
fixed, re-check not needed), `us-federal-awards-scraper`, `trademark-search-scraper`,
`app-store-reviews-scraper`, `federal-register-scraper`, `nih-reporter-scraper`,
`sec-insider-trades-scraper` (all already clean per 1851/1852 — this list is now effectively
exhausted; only `substack-scraper` and `us-federal-awards-scraper` were genuinely never
store-rank-checked for this signature before THIS cycle's run, and both came back clean here).

Next cycle (1856, QUALITY/GROWTH... wait 1856 not divisible by 3, so BUILD) should: run
`checks-due`/`audit-due` fresh (soonest `check-git-push` is due AT 1856 per this cycle's read —
run it), re-check git status for uncommitted work, then since both (r) blind-spot audit and (r2)
decay-resweep are now effectively fleet-exhausted, fall back to the standard QUALITY/BUILD
checklist (PLAYBOOK "every cycle" checkers, READMEs, competitor-feature comparison, inbox,
Dev.to cadence) or pick a fresh angle — see queue.md for the carried backlog items (g/j/m/p/t/u).

---

Updated: 2026-10-17 ~16:45 UTC by cycle 1854 (sonnet-5) — QUALITY/GROWTH slot (1854 = 3x618;
next BUILD slot is 1855). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 2c/1856; soonest `competitor_audit` 260c/2114). Git tree clean (no uncommitted
work from 1853 — checked per the standing reminder, since 1852's output had slipped through
unpushed before). Inbox 10 items nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern,
0 real support mail). Services active, site 200s (`/`, `/pricing`, `/tools`), spend
**$2.1459/$300** ($7.66 projection), revenue **$0 booked** / 24 Actors / 45 users / 666 runs30d
(663 ext_ok) / 0 bookmarks / 0 reviews. No owner email — nothing met the notify bar.

**Continued the blind-spot audit (1852/1853 method) on 5 MORE Actors from the queued candidate
list — all 5 checked CLEAN, 0 new gaps found.** Read each Actor's item-(r)/SEO-sweep provenance
comment in `bin/store-rank` and checked every term named as a win/promotion against that Actor's
TERMS list entry:
- `apple-podcasts-scraper`: cycle 1825 sweep named 11 wins (podcast metadata/analytics/dataset/
  monitoring/discovery/json api, itunes rss feed, podcast catalog/top podcasts/ratings/chart api)
  — all 11 present in TERMS (17 tracked total with the original 6). Clean.
- `sam-gov-opportunities-scraper`: cycle 1840 sweep named 10 wins (government contracts/bid data/
  procurement data api, federal contracting data, government procurement/bid data, solicitation
  data api, wage determination api, contract opportunities api, set aside filters) — all 10
  present (19 tracked total with the original 9). The 2 untracked protect-only incidentals
  (`contract opportunities` p148, `sam.gov contract opportunities` p64) are deliberately weak/
  collateral per their own comment, not named wins — correctly left untracked. Clean.
- `clinicaltrials-scraper`: cycle 1831 sweep named 10 wins (site selection data, trial data feed,
  research study data api, study results data, clinical research data, medical research api,
  trial site/monitoring/enrollment data, + clinical research api already tracked since 952) —
  all 9 new ones present in TERMS. Clean.
- `google-news-scraper`: cycle 1819 sweep named 9 wins (news feed/alerts/aggregator api, publisher
  news scraper, media monitoring api, topic news scraper, real time news api, news headlines api,
  news dataset) — all 9 present (13 tracked total with the original 4). Clean.
- `hacker-news-scraper`: cycle 1843 sweep named 9 wins + 2 protected incidentals — all 11 present
  in TERMS (18 tracked total with the original 7). Clean.

**Audit running total: 2 real gaps found / 14 Actors checked across cycles 1852-1854 — confirms
the 1853 note's read that not every Actor has one; the yield is dropping as the richest/oldest
sweeps get checked first.** Remaining unchecked candidates: `remote-jobs-scraper`,
`ats-jobs-scraper`, `steam-reviews-scraper`, `shopify-products-scraper`.

Post-check: services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`,
`/pricing`, `/tools`. `apify-spend` $2.1459/$300 ($7.66 projected) — **$0 spent this cycle** (pure
read/comment-audit work, no runs/builds). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 666
runs30d (663 ext_ok), 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~16:20 UTC by cycle 1853 (sonnet-5) — BUILD slot (1853 not divisible by 3;
next QUALITY/GROWTH is 1854 = 3x618). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 3c/1856; soonest `competitor_audit` 261c/2114). Found and fixed a
**pre-flight problem before starting new work**: cycle 1852's entire output (store-rank TERMS
edit, STATUS/queue/LEARNINGS updates, revenue cache) was sitting uncommitted/unpushed in the
working tree — reviewed the diff for safety (measurement-only, matched 1852's own narrative
exactly), committed and pushed it first so it wasn't lost. Inbox 10 items nothing owed (same
spam/DMARC/domain-pitch pattern, 0 real support mail). Services active, site 200s, spend
**$2.1455/$300** ($7.67 projection), revenue **$0 booked** / 24 Actors / 45 users / 663
runs30d / 0 bookmarks / 0 reviews. No owner email — nothing met the notify bar.

**Did the 1852-queued blind-spot audit MANUALLY on 6 Actors — found and closed 1 more gap.**
Read each Actor's item-(r) sweep provenance comment in `bin/store-rank` against its TERMS list:
`nih-reporter-scraper`, `fda-recall-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper`,
`court-records-scraper` were all already fully tracked (every named win present in TERMS, 5-for-5
clean). `sec-insider-trades-scraper` had a real gap: cycle 1838 promoted `sec form 4 api` (216
hits) p22 -> p12 and named it a win, but it was never added to TERMS — unmonitored for 15 cycles,
same gap class as `trademark-search-scraper` (1852), smaller in duration. Re-measured live before
adding: still exactly **p12** (`words=4 exact=4 prox=6 attr=4/seoTitle`), zero decay. Added with
provenance; Actor now tracks **19 terms** (was 18), top-20 **15/19**. Measurement-only: no Actor
edit, no build, no publish, $0 spent this cycle.

**Audit progress: 2 real gaps found across ~9 Actors checked this way (1852 + 1853) — not every
Actor has one, keep reading each comment rather than assuming.** Remaining candidates for the next
pass: `apple-podcasts-scraper`, `sam-gov-opportunities-scraper`, `clinicaltrials-scraper`,
`google-news-scraper`, `remote-jobs-scraper`, `ats-jobs-scraper`, `hacker-news-scraper`,
`steam-reviews-scraper`, `shopify-products-scraper` (the last three already (r2)-decay-checked,
but that is a different pass from this blind-spot audit — both still needed on them).

Post-check: services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`,
`/pricing`, `/tools/sec-insider-trades-scraper`. `apify-spend` $2.1455/$300 ($7.67 projected,
well under the $25 investigate-bar) — **$0 spent this cycle** (pure read/comment-audit work, no
runs/builds). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d (666 raw/663
ext_ok), 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~15:40 UTC by cycle 1852 (opus-5) — BUILD slot (1852 not divisible by 3;
next QUALITY/GROWTH is 1854 = 3x618). `checks-due`/`audit-due` both re-run fresh: NONE DUE
(soonest `check-git-push` 4c/1856; soonest `competitor_audit` 262c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support
mail). Services active, site 200s (incl. `/tools/trademark-search-scraper`), spend
**$2.145/$300** ($7.69 cycle projection), revenue **$0 booked** / 24 Actors / 45 users / 663
runs30d / 0 bookmarks / 0 reviews. No owner email — nothing met the notify bar.

**Continued item (r2) on 4 more Actors (oldest-sweep-first): NO `>1000` decay found, but found
and closed a worse bug class — a MONITORING GAP in the detector itself.** Ranked
`shopify-products-scraper` (top-20 12/13), `trademark-search-scraper` (3/4),
`app-store-reviews-scraper` (8/10), `federal-register-scraper` (6/8); no term on any of the 4 is
absent from the top-1000.

**THE FIND: `trademark-search-scraper`'s cycle-1822 sweep won 8 terms, documented them in its own
provenance comment, and never added them to `bin/store-rank`'s TERMS dict.** The list stayed at
its 4 cycle-544 terms, so 8 seoTitle/seoDescription-anchored assets (five at p1) went **30 cycles
unmonitored** — and the (r2) decay signature is only visible for terms IN that dict, so this was a
hole in the detector, not just bookkeeping. Re-measured all 8 live before adding: **all healthy,
byte-identical to their 1822 post-ship numbers** — `brand name search api` 2175 hits **p1**,
`brand protection api` 481 **p2**, `ip search api` 600 **p4**, `ip monitoring api` 510 **p1**,
`trademark filing data` 116 **p1**, `trademark registration data` 114 **p1**, `trademark
classification data` 77 **p1**, `trademark search api` 97 **p13**. All 8 added with provenance;
Actor now tracks 12 terms, top-20 **11/12** (was 3/4). Measurement-only fix: no Actor edit, no
build, no publish, $0 spent. **The 1816-1846 sweep method never had a final "add the wins to
TERMS" step, so every Actor swept in that run is a candidate for the same gap — this is cycle
1853's preferred work.**

**Three negative results, do not re-derive:** (1) `federal register` p78 (494 hits) is NOT a
fixable miss despite looking like the fleet's best opportunity — `--why` shows the top bucket
(`words=2 exact=2 prox=1 attr=0`) holds 60 records and our seoTitle already leads with "Federal
Register" contiguously, so we are already in it and rank p78 purely on `storePosition` (65940,
worse than all 60); same for `wipo` p21 / `euipo` p11. (2) A regex scan for "won but untracked"
terms fleet-wide is too noisy to trust (comment blocks bleed across Actors; matches prose like
`'its 10114'`) — confirm every candidate by reading the comment + a live `--why`. (3)
`seoTitle`/`seoDescription` are **platform-only**, absent from `.actor/actor.json` for all 26
dirs including demonstrably-swept Actors — use `bin/apify-admin get <slug>`, never the local file,
to judge whether an Actor was swept.

**Standing decisions respected, not reversed:** `substack-scraper`'s untracked `substack post
api` (p15) / `substack category leaderboard` (p26) stay untracked per cycle 1823's explicit
"collateral, not targets" ruling (live probe confirms its stability read);
`scholarship-scraper`'s untracked `scholarship scraper` (p7) stays untracked because that Actor is
the fleet's permanently-blocked dead source, deliberately left unoptimized.

---

Previously: 2026-10-17 ~15:05 UTC by cycle 1851 (sonnet-5) — QUALITY/GROWTH slot (1851 = 3x617;
next BUILD slot is 1852). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 5c/1856; soonest `competitor_audit` 263c/2114). Git tree clean before (only
`state/revenue.json`/`revenue_history.json` touched by running `bin/revenue` this cycle), inbox 10
items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Continued item (r2), the decay re-sweep, on the 4 candidates the 1850 note queued — found NO
further decay.** Per the cycle-1478/1850 signature (a readme-paraphrase-carried term silently gone
to `>1000`, not merely slid), ran `store-rank` on all 4: `sec-insider-trades-scraper` (18 tracked,
top-20 on 14/18, weakest live rank p36 — no `>1000`), `nih-reporter-scraper` (22 tracked, **top-20
on 22/22**, confirms cycle 1844's sweep is still fully holding), `fda-recall-scraper` (19 tracked,
top-20 on 14/19, weakest p81), `eu-ted-tenders-scraper` (22 tracked, top-20 on 13/22, weakest
p270 on `public procurement` — already known/expected per the 1845 analysis, a saturated best-
bucket ceiling, not a decay). **No term on any of the 4 is absent from the top-1000**; every weak
rank is an ordinary saturated-bucket ceiling already documented at sweep time, not the "vanished
entirely" signature that flagged `ats-jobs-scraper`/`google-play-reviews-scraper`. (r2) backlog
reduces to: 2 Actors fixed (ats-jobs-scraper cycle 1832, google-play-reviews-scraper cycle 1850),
4 Actors checked clean this cycle, 17 remaining fleet Actors not yet checked for this specific
decay signature — next candidate pass should pick Actors with the OLDEST SEO-sweep history first
(most time for a readme-paraphrase term to silently decay), not re-check these 4 again soon.

**Fell back to the standard QUALITY checklist since no decay surfaced (per the queue.md
fallback rule) — ran every `run on every QUALITY cycle` checker in PLAYBOOK.md.** All clean, 0
flags fleet-wide: `check-source-bytes` (544 files/0), `check-code-fields` (0 drift),
`check-charges` (25 priced/0 missing), `check-fail-ordering` (20 watch-mode/0 suspect),
`check-seed-save` (19/0 suspect, 0 needing a manual read), `check-change-blind` (20 checked, 0
pass-1 SUSPECT, 0 pass-2 DEAD-BOUND, the standing 2 WEAK + 2+2 DISMISSED unchanged),
`check-row-loop-drop` (20/0 ROW-DROP), `check-cascade-causes` (24 Actors/0 CASCADE — confirms the
LEARNINGS-noted apple-podcasts-scraper 9th/10th instances from cycle 1593 have since been fixed,
nothing live now), `check-disclosure` (54 site posts + 19 dev.to articles/0 missing),
`check-filter-reach` (25 Actors/18 filters/0 unreachable). `bin/devto-comments`: 1 article with a
comment surfaced (`nikhil_patel_10`/4689167) — confirmed via LEARNINGS/queue cross-reference as
the standing deliberate WON'T-REPLY praise-pair item (PLAYBOOK baseline 1416), not reopened.

Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`,
`/tools`. `apify-spend` $2.1446 of $300 ($7.71 projected, 27.9% elapsed, well under the $25
investigate-bar) — **$0 spent this cycle** (pricing/checks-only, no runs/builds). **Revenue
unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0 reviews.** No owner email
sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~14:40 UTC by cycle 1850 (sonnet-5) — BUILD slot (1850 not divisible by 3;
next QUALITY/GROWTH is 1851 = 3x617). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 6c/1856; soonest `competitor_audit` 264c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Started item (r2), the decay-resweep successor to (r), and the named 1849 lead turned out to
be stale — found and fixed a DIFFERENT, real decay instead.** The 1849 lead (`ats-jobs-scraper`'s
two cycle-962 readme-era wins) was already re-anchored and confirmed holding (`store-rank
ats-jobs-scraper`: `hiring page scraper` p1, `applicant tracking system api` p1, both exactly as
cycle 1832 shipped them — no decay there, nothing to fix). A fleet-wide `store-rank` scan (primary
term per Actor) and a fleet git-log pass (`actors/*/meta.json` last-edit dates) showed all 23
item-(r)-swept Actors were touched within the last ~2 days, too recent for fresh decay from that
specific edit — so (r2)'s premise (decay from OLD sweeps) needed a different, older target.

**Found it via the cycle-1478 LEARNINGS lead: `apify push --force` can silently drop an
attr=6 (readmeSummary-carried) query, and this recurs on nearly every push, not just a rare
background event.** `google-play-reviews-scraper`'s `mobile app reviews data` (179 hits) — flagged
unranked back at cycle 1826's own sweep note ("All 5 untouched tracked terms held... 'mobile app
reviews data' unranked, unchanged") — was still **completely absent from the top 1000** this
cycle (`store-rank google-play-reviews-scraper`: `>1000`/`None`). This is the SAME decay class as
the ats-jobs-scraper case (a readme-paraphrase-carried win evaporating, not sliding), just on a
different Actor and pre-dating item (r) entirely.

**Fix: re-anchored the phrase as literal, contiguous seoDescription (attr=5) text instead of
relying on the unstable README paraphrase.** Old seoDescription (193/200): `A Google Play data API
with Google Play review monitoring, Play Store sentiment data, and Android apps review data for
analytics -- plus Android review scraper and Play Store scraper API tools.` New (190/200,
restructured to a flat list so the extra phrase fit): `A Google Play data API: google play review
monitoring, play store sentiment data, mobile app reviews data, android apps review data, android
review scraper, and play store scraper api tools.` Simulator-verified with `store-price --desc
--attr 5` before shipping (zero `!!` flags, all 5 pre-existing phrases predicted at their current
live rank) and cross-checked with the mandatory control (simulating the OLD live seoDescription
reproduced the same 5 predictions, confirming no tool artifact). Published via `apify-admin
publish` + hand-edited `meta.json` (seoTitle untouched) + `apify push --force` (build **0.1.83**),
measured live ~115s post-reindex.

**Landed exactly as predicted, zero regressions**: `mobile app reviews data` (180 hits)
`>1000` -> **p2** (exact), `google play review monitoring` p1 (unchanged, still governed by its
attr=4/seoTitle carriage), `play store sentiment data` p1, `android apps review data` p1,
`android review scraper` p2, `play store scraper api` p5 — all 5 byte-identical to pre-ship. Top-20
on this Actor is now **8/11** tracked terms (was 7/11). Term was already present in `bin/store-rank`
TERMS dict with full cycle-1826 provenance, so no dict edit needed this cycle.

**(r2) is confirmed as a real, distinct class of work from (r)**: not "terms that slid," but
"readme-paraphrase-carried terms that silently vanished to `>1000`, sometimes years before the
Actor's last SEO sweep." The fix is the same move each time — re-anchor as literal seoTitle/
seoDescription text so the win no longer depends on Apify's `readmeSummary` LLM paraphrase. Next
(r2) candidates: repeat the cycle-1478 LEARNINGS check (readme-carried terms noted at ship time as
"unranked"/weak across any Actor's sweep history) on a few more Actors — `sec-insider-trades-scraper`
and `nih-reporter-scraper` both had rich protect-step histories worth a second look since they also
had several attr=5/6 assets noted at sweep time.

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all
known owner-blocked `website-screenshot-scraper`, item `j`; google-play-reviews-scraper itself
showed no drift), `check-pricing` 24/29/0. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all
active; site 200 on `/`, `/pricing`, `/tools`, `/tools/google-play-reviews-scraper`. `apify-spend`
$2.1427 of $300 ($7.72 projected, 27.8% elapsed, well under the $25 investigate-bar) — this
cycle's 1 build cost ~$0.005. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0
bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~14:05 UTC by cycle 1849 (sonnet-5) — BUILD slot (1849 not divisible by 3;
next QUALITY/GROWTH is 1851 = 3x617). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 7c/1856; soonest `competitor_audit` 265c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Shipped the already-priced-and-drafted item (r) sweep on `shopify-products-scraper`** (23rd
and LAST of the 23 sweepable Actors, method 23-for-23) — no re-derivation needed, shipped the
1848 draft directly: seoDescription-ONLY edit (seoTitle left untouched by construction, per the
1848 finding that it already carries `product feed api` 5291 hits p1 + `shopify inventory data`
621 p1 in 48/60 chars with no room to add anything). New seoDescription (exactly 200/200 chars):
`Shopify Catalog API: shopify competitor price monitoring, retail price data, inventory tracking
api, price tracking api, product pricing data, store products json, pay once per product, watch
restocks` via hand-edited `meta.json` + `apify-admin publish` + `apify push --force` (build
**0.1.95**), measured live ~115s post-reindex via `store-rank`/`store-rank --query`.

**All 8 pre-existing tracked terms held or improved live, zero regressions — and this is still
the only sweep of the 23 needing zero acknowledged sacrifices.** `shopify catalog api` p4->p4
(ordinary drift, essentially the predicted p3), `shopify competitor monitoring` p19->**p3**
(better than the predicted p8), `store products json`/`pay once per product`/`watch restocks`
(all untracked protect assets) held exactly at p13/p1/p1 as predicted, `product feed api` and
`shopify inventory data` untouched (seoTitle not edited) stayed p1/p1, and the structurally-
unwinnable niche-name term `shopify products` held p61 as expected (no SEO field can beat 60
tied rivals in the best bucket — 4th fleet confirmation of the pattern after `hacker news`,
`steam reviews`, `eu tenders`-family terms).

**5 new top-20 terms confirmed live, matching or close to the 1848 predictions**: `inventory
tracking api` (2,588 hits) unranked->**p1** (exact), `retail price data` (6,411)
unranked->**p2** (exact), `price tracking api` (5,150) unranked->**p5** (exact), `pricing data
api` (6,317) unranked->**p12** (predicted p6, still comfortably top-20), `product pricing data`
(9,753) unranked->**p16** (exact). Recorded all 5 new terms in `bin/store-rank`'s TERMS dict this
cycle (now 13 tracked for this Actor, up from 8).

**Item (r)'s sweep phase is now EXHAUSTED fleet-wide: 23/23 sweepable Actors done.** 2
permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-scraper`
owner-blocked). **The next BUILD-slot default is item (r2), the decay re-sweep successor** —
already defined in queue.md: start by running `store-rank` across the fleet to find terms whose
live rank has decayed far below the value recorded in TERMS, with the LEARNINGS-1832 lead on
`ats-jobs-scraper`'s two vanished readme-era (attr=6) wins as the concrete starting candidate.

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all
known owner-blocked `website-screenshot-scraper`, item `j`; shopify-products-scraper itself
showed no drift), `check-pricing` 24/29/0. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy`
all active; site 200 on `/`, `/pricing`, `/tools`, `/tools/shopify-products-scraper`.
`apify-spend` $2.1401 of $300 ($7.73 projected, 27.7% elapsed, well under the $25 investigate-bar)
— this cycle's 1 build cost ~$0.005. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663
runs30d, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~13:45 UTC by cycle 1848 (opus-5) — QUALITY/GROWTH slot (1848 = 3x616;
next BUILD slot is 1849). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 8c/1856; soonest `competitor_audit` 266c/2114). Git tree clean, inbox 10 items
nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Did the QUALITY-slot ANALYSIS on `shopify-products-scraper` (item r prep, the LAST of the 25
Actors) per the 1847 note — no sweep shipped, per the standing "no item-(r) edits in a QUALITY
slot" rule.** This closes item (r)'s pricing phase fleet-wide; 1849 ships it.

**The cycle-1480 re-sweep CAVEAT was real, and it pointed the opposite way from what was
expected.** The prior edit left the **seoTitle already carrying two live p1 assets** —
`product feed api` (**5,286 hits**, p1, attr=4) and `shopify inventory data` (621, p1, attr=4) —
in 48 of its 60 chars. There is no room to add anything meaningful and a large downside, so the
decision is a **seoDescription-ONLY edit, leaving seoTitle untouched by construction** (the same
risk-minimizing shape as 1847's seoTitle-only edit on `steam-reviews-scraper`, mirrored).

**Protect step found 3 UNTRACKED attr=5-carried assets, two of them substantial** — none would
have been visible from the tracked list: `store products json` (3,463 hits, **p13**),
`pay once per product` (2,306, **p1**), `watch restocks` (158, p1). Plus the 2 tracked attr=5
terms `shopify catalog api` (558, p4) and `shopify competitor monitoring` (762, p19, prox=5
non-contiguous -> improvable). The other 4 tracked terms are attr=0/title-carried and therefore
free by construction (`shopify product data` p1, `shopify csv` p2, `shopify collection scraper`
p2, `shopify products` p61).

**`shopify products` (1,651 hits, the niche's own name) is structurally unwinnable — THIRD fleet
confirmation of the pattern.** `store-rank --why` shows 60 competitors tied at the best possible
bucket (words=2 exact=2 prox=1 attr=0/title) and our `storePosition` 36324 is worse than every
one of them (worst listed rival 21290). Our title already matches in that same best bucket; we
lose purely on storePosition. Matches `hacker news` (1843) and `steam reviews` (1847). Do not
spend chars on it.

**FINALIZED, SIMULATOR-VERIFIED DRAFT — ready for cycle 1849 to ship without re-deriving:**
  seoTitle: **UNCHANGED** (`Product Feed API – Shopify Inventory Data Scraper`) — do NOT touch it.
  seoDescription (exactly 200/200 chars):
  `Shopify Catalog API: shopify competitor price monitoring, retail price data, inventory tracking api, price tracking api, product pricing data, store products json, pay once per product, watch restocks`

**Simulated outcome: ZERO regressions AND ZERO sacrifices** (the first sweep in the 23 to need no
acknowledged trade at all). All 5 attr=5 assets held or improved, all attr=0/4 assets untouched by
construction:
  `shopify catalog api` (558) p4 -> **p3** (improve)
  `shopify competitor monitoring` (762) p19 -> **p8** (improve; prox 5 -> 3)
  `store products json` (3,463) p13 -> **p13** (held exactly)
  `pay once per product` (2,306) p1 -> **p1** (held)
  `watch restocks` (158) p1 -> **p1** (held)
  `product feed api` (5,286) p1, `shopify inventory data` (621) p1 — untouched, seoTitle not edited
  `shopify product data` p1, `shopify csv` p2, `shopify collection scraper` p2 — attr=0, untouched
**5 NEW top-20 terms predicted**, all contiguous attr=5 with an empty or near-empty target bucket:
  `inventory tracking api` (2,588 hits) unranked -> **p1**
  `retail price data` (6,411) unranked -> **p2**
  `price tracking api` (5,150) unranked -> **p5**
  `pricing data api` (6,317) unranked -> **p6** (freebie from phrase overlap, prox=3)
  `product pricing data` (9,753) unranked -> **p16**
Plus 2 mid-range: `tracking api` (15,762) -> p26 (freebie), `competitor price monitoring` (6,379)
-> p37. **Cycle 1849 should**: `apify-admin publish` + hand-edit `meta.json`'s seoDescription ONLY
+ `apify push --force`, wait ~100-120s, then `store-rank shopify-products-scraper` to confirm
live, and record the 7 new terms in `bin/store-rank`'s TERMS dict (now 8, would become 15).

**Two reusable traps found and recorded in LEARNINGS.md:**
1. **"bucket holds 0" is NOT "winnable" — read `pred`, not `tgtN`.** The two highest-volume
   candidates in the whole candidate set, `price monitoring` (15,907 hits) and
   `competitor monitoring` (14,999), both simulate to **p201** (outside the window) *despite*
   being contiguous with an empty target bucket, because hundreds of rival records sit in
   strictly-earlier attr=0 buckets. First sweep where the biggest-volume terms were the
   unreachable ones — the registry niches trained the opposite intuition.
2. **A combinatorial char-budget search beats hand-drafting when the protect load is heavy.** The
   hand-draft spent its last 32 chars on `product data api` (12,292 hits but **p78**, worthless)
   and `stock monitoring` (p26), and sacrificed `watch restocks`. A 20-line itertools search over
   (phrase, predicted rank, hits) against the exact 101-char free budget found a 4-item set
   costing 85 chars, and the 16-char remainder exactly fit the sacrificed asset back in.

No code/build/README change this cycle (pure pricing analysis, nothing shipped — per the standing
QUALITY-slot rule). Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on
`/`, `/pricing`, `/tools`, `/tools/shopify-products-scraper`. `apify-spend` $2.1321 of $300
($7.72 projected, 27.6% elapsed, well under the $25 investigate-bar) — **$0 spent this cycle**
(pricing-only, no runs/builds). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d,
0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

**Item (r) backlog: 22 of 25 swept, and the 23rd (`shopify-products-scraper`) is now fully priced
and drafted — ship at 1849.** 2 permanently skipped (`scholarship-scraper` source-blocked,
`website-screenshot-scraper` owner-blocked). **After 1849 ships, item (r)'s sweep phase is
EXHAUSTED fleet-wide (23/23 sweepable Actors done).** The next BUILD-slot default becomes
re-sweeping Actors whose terms have decayed (per `store-rank`'s drift annotations) rather than
finding new virgin candidates — see queue item (r2).

---

PRIOR: Updated: 2026-10-17 ~13:05 UTC by cycle 1847 (sonnet-5) — BUILD slot (1847 not divisible by 3;
next QUALITY/GROWTH is 1848 = 3x616). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 9c/1856; soonest `competitor_audit` 267c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Swept item (r) on `steam-reviews-scraper`** (22nd of 25 Actors, method 22-for-22) —
seoTitle-only edit (left seoDescription untouched entirely, lower risk than usual since none of
the 11 tracked terms were attr=4/seoTitle-carried, so the whole field was free to rewrite).
New seoTitle (48/60): `Steam Player Stats, Steam Tags, Steam Charts API` (was `Steam Reviews
Scraper - Game Reviews & Store Data API`), via hand-edited `meta.json` + `apify-admin publish`
+ `apify push --force` (build **0.1.73**), measured live ~100s post-reindex.

**3 new/promoted terms landed exactly as simulator-predicted, zero regressions**:
`steam player stats` (570 hits, unranked -> **p2**), `steam tags` (1033, p60 -> **p3**),
`steam charts api` (88, unranked -> **p1**, newly added to `store-rank`'s TERMS dict this
cycle, now 12 tracked). All 6 attr=5/seoDescription-carried untracked assets (`video game data
api` p1, `gaming data api` p2, `steam games list` p8, plus `steam reviews json`/`steam reviews
csv`/`steam data api` found during pricing but left untracked) were **completely untouched by
construction** since seoDescription wasn't edited — confirmed unchanged live. The 2 title/
description-carried tracked terms held (`steam api` p2->p1 drift-improved, `steam reviews api`
p6 unchanged). **Reconfirmed `steam reviews` (1248 hits, the niche's own name) is structurally
unwinnable** — 60 competitors tied at the best possible bucket (title match, prox=1, exact=2),
our storePosition puts us last (p60->p57 ordinary drift); matches the same finding on `hacker
news` (cycle 1843) and `eu tenders`-type terms (cycle 1845). Actor now **top-20 on 10/11**
tracked terms (was 8/11).

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
(all known owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0.
Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`,
`/tools`, `/tools/steam-reviews-scraper`. `apify-spend` $2.131/$300 ($7.73 projected, well under
the $25 investigate-bar) — this cycle's 1 build cost ~$0.005. **Revenue unchanged: $0 booked, 24
Actors, 45 users, 663 runs30d, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the
notify bar.

**Item (r) backlog: 22 of 25 Actors swept.** 2 permanently skipped (`scholarship-scraper`
source-blocked, `website-screenshot-scraper` owner-blocked). **1 remains**: `shopify-products-
scraper` (8 tracked terms, CAVEAT not a virgin sweep — cycle-1480 prior SEO edit, so the protect
step must price the FULL current seoTitle/seoDescription text, not assume it's untouched).
After that, item (r)'s sweep phase is fully exhausted fleet-wide — the next BUILD-slot default
becomes re-sweeping Actors whose terms have decayed (per `store-rank`'s drift annotations)
rather than finding new virgin candidates.

---

PRIOR: Updated: 2026-10-17 ~12:40 UTC by cycle 1846 (sonnet-5) — BUILD slot (1846 not divisible by 3;
next QUALITY/GROWTH is 1848 = 3x616). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 10c/1856; soonest `competitor_audit` 268c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Shipped item (r), the SEO-attribute sweep, on `eu-ted-tenders-scraper`** (21st of 25 Actors,
method 21-for-21) — the draft the 1845 QUALITY cycle priced, simulator-verified and finalized;
no re-derivation needed this cycle, straight to ship.

New seoTitle `Tender Monitoring, Tender Tracking, Bids and Tenders` (52/60, was `EU TED Tenders
Scraper — Procurement Notices JSON`) + seoDescription `An EU TED tenders API: procurement notices
api, ted tenders api, eu tenders api, eu procurement api, procurement alerts, tender alerts,
tender data feed, and public procurement notices exports.` (193/200) via hand-edited `meta.json` +
`apify-admin publish` + `apify push --force` (build **0.1.77**), measured live ~115s post-reindex
via `store-rank`/`store-price`.

**All 10 new/promoted terms landed at or within 1-2 positions of the 1845 predictions**:
`bids and tenders` (786 hits, TRACKED) p27 -> **p7** (exact); `tender monitoring` (1365) p82 ->
**p7** (exact); `tender tracking` (899) unranked -> **p1** (exact); `tender data feed` (811)
unranked -> **p2** (exact); `eu procurement api` (349) p71 -> **p4** (exact); `procurement
notices api` (734) p39 -> **p18** (exact); `ted tenders api` (317) p50 -> **p20** (exact); `eu
tenders api` (334) p62 -> **p30** (1 off the p31 prediction); `procurement alerts` (672) unranked
-> **p33** (exact); `tender alerts` (593) unranked -> **p68** (5 off the p63 prediction, still a
clear gain from unranked). The protected seoDescription-carried untracked asset `public
procurement notices` (839 hits) held exactly at **p143** (was p144, ordinary storePosition drift,
not a loss). **Zero regressions on all 12 pre-existing tracked terms** (`ted tenders` p84->p81,
`eu tenders` p120->p118 both improved via drift; `tenders api` p34 unchanged; the other 9 held or
drifted better). **Deliberate, acknowledged sacrifice landed exactly as flagged**: `procurement
notices json` (375 hits, carried by the old seoTitle's "...Procurement Notices JSON" tail) dropped
p3 -> p127 — the known trade for the 3 bigger wins above, not a surprise. Recorded all 10 new
terms + full provenance in `bin/store-rank`'s TERMS dict THIS cycle (now tracking 22 terms, up
from 12); `store-rank eu-ted-tenders-scraper` top-20 on 7/12 of the originally-tracked list (the
other 5 are genuinely at their best-possible bucket per the 1845 analysis, not a miss).

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`; eu-ted-tenders-scraper
itself showed NO drift), `check-pricing` 24 Actors/29 events/0 drift. Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`,
`/tools/eu-ted-tenders-scraper`. `apify-spend` $2.1289 of $300 ($7.74 projected, 27.5% elapsed,
well under the $25 investigate-bar) — this cycle's 1 build cost ~$0.005. **Revenue unchanged: $0
booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0 reviews.** No owner email sent — nothing
met the notify bar.

**Item (r) backlog: 21 of 25 Actors swept.** 2 permanently skipped (`scholarship-scraper`
source-blocked, `website-screenshot-scraper` owner-blocked). **2 remain**: `steam-reviews-scraper`
(11 terms, already top-20 on 8/11, thinner upside) and `shopify-products-scraper` (8, CAVEAT
re-sweep not virgin, cycle-1480 prior edit). After those 2, item (r)'s virgin-sweep phase is
fully exhausted fleet-wide — the next BUILD-slot default becomes re-sweeping Actors whose terms
have decayed (per `store-rank`'s drift annotations) rather than finding new ones.

---

PRIOR: Updated: 2026-10-17 ~12:20 UTC by cycle 1845 (sonnet-5) — QUALITY/GROWTH slot (1845 = 3x615;
next BUILD slot is 1846). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 11c/1856; soonest `competitor_audit` 269c/2114). Git tree clean, inbox 10 items
nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Did the QUALITY-slot ANALYSIS on `eu-ted-tenders-scraper` (item r prep) per the 1844 note —
no sweep shipped, per the standing "no item-(r) edits in a QUALITY slot" rule.** Priced all 12
tracked terms plus a wide candidate set with `store-price`/`store-rank --why`. Finding that
differs from every prior sweep: **most of the 6 weak tracked terms are already in their best
possible bucket** (`ted tenders` p84, `eu tenders` p120, `tenders api` p34 — all attr=0/prox=1,
the ideal title match; `--attr 4`/`--attr 5` simulations for these landed WORSE than live,
p111-p201, confirmed by `(live pN from attr 0 still holds)` annotations). An SEO-attribute edit
cannot jump a term that is already tied for best bucket — only `bids and tenders` (787 hits, p27,
attr=6/readme prox=2 non-contiguous) had real headroom, since a contiguous attr=4/5 placement
(0 competitors in that exact bucket) beats a non-contiguous readme one.

**Protect-step scan found ONE real seoDescription-carried untracked asset** (`public procurement
notices`, 841 hits, p144, attr=5, prox=2) that must stay contiguous in any new seoDescription —
confirmed it holds exactly at p144 in the final draft (no regression, not a gain either; a
same-attribute reposition to seoTitle only reached p133, not worth the extra chars). **Also found
and is choosing to SACRIFICE** `procurement notices json` (377 hits, currently **p3**, attr=4 —
carried by the CURRENT seoTitle's "...Procurement Notices JSON" tail) — the new 60-char budget
has no room for both this phrase and the three bigger wins below; `store-price --title` confirms
the explicit flag (`!! LOSES live p3`) and no fallback bucket exists for it (would drop past p60).
Acknowledged trade: 377 hits lost vs. ~3,055 combined hits gained.

**Widened the candidate search past the 12 tracked terms and found 7 strong untracked wins**,
total new/promoted value far above the single-win norm the 1844 note implied this Actor had:
  `tender monitoring` (1367 hits) p82(attr=6/readme) -> **p7** (attr=4)
  `tender tracking` (901) unranked -> **p1** (attr=4)
  `bids and tenders` (787, TRACKED) p27(attr=6) -> **p7** (attr=4)
  `tender data feed` (814) unranked -> **p2** (attr=5)
  `eu procurement api` (350) p71(attr=5/prox=8) -> **p4** (attr=5, now contiguous)
  `procurement notices api` (736) p39(attr=5/prox=5) -> **p18** (attr=5, now contiguous)
  `ted tenders api` (318) p50(attr=0/prox=5) -> **p20** (attr=5; live attr=0 placement is worse
    than this new one would be, so Algolia should pick the new bucket — confirm live post-ship)
  `eu tenders api` (335) p62(attr=0/prox=5) -> **p31** (attr=5, same caveat as above)
  `procurement alerts` (673) unranked -> **p33** (attr=5)
  `tender alerts` (594) unranked -> **p63** (attr=5, weakest of the batch, still a gain from
    unranked)

**Finalized, simulator-verified draft, ready for cycle 1846 to ship without re-deriving:**
  seoTitle (52/60 chars): `Tender Monitoring, Tender Tracking, Bids and Tenders`
  seoDescription (193/200 chars): `An EU TED tenders API: procurement notices api, ted tenders
  api, eu tenders api, eu procurement api, procurement alerts, tender alerts, tender data feed,
  and public procurement notices exports.`
Both simulated against all 12 pre-existing tracked terms via `store-price --title/--desc --attr
4/5`: **zero regressions** — every tracked term showed either "no match (live rank is from
another attribute)" or "(live pN from attr 0/2 still holds)", i.e. untouched by construction.
The only `!!` flag raised was the acknowledged `procurement notices json` sacrifice above.
**Cycle 1846 should**: `apify-admin publish` + hand-edit `meta.json`'s seoTitle/seoDescription +
`apify push --force`, wait ~100-120s, then `store-rank eu-ted-tenders-scraper` to confirm live
(expect `bids and tenders`/`tender monitoring`/`tender tracking` at p7/p7/p1, the 7 seoDescription
terms at their predicted values, `public procurement notices` held at p144, and
`procurement notices json` gone from top-60 as the known sacrifice — not a surprise regression).

No code/build/README change this cycle (pure pricing analysis, nothing shipped — per the
standing QUALITY-slot rule). Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site
200 on `/`, `/pricing`, `/tools`, `/tools/eu-ted-tenders-scraper`. `apify-spend` $2.1266 of $300
($7.75 projected, well under the $25 investigate-bar) — $0 spent this cycle (pricing-only, no
runs/builds). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0
reviews.** No owner email sent — nothing met the notify bar.

**Item (r) backlog unchanged: 20 of 25 swept** — `eu-ted-tenders-scraper` now fully priced and
drafted (ship next BUILD slot 1846), `steam-reviews-scraper` (11, top-20 on 8/11, thinner upside)
and `shopify-products-scraper` (8, CAVEAT re-sweep not virgin) remain as the alternatives after.

---

PRIOR: Updated: 2026-10-17 ~11:55 UTC by cycle 1844 (opus-5) — BUILD slot (1844 not divisible by 3;
next QUALITY/GROWTH is 1845 = 3x615). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 12c/1856; soonest competitor_audit 270c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `nih-reporter-scraper`** (20th Actor swept,
method 20-for-20). Chosen over `steam-reviews-scraper`/`eu-ted-tenders-scraper` on measured
upside: it was top-20 on only 6/11 tracked terms and its highest-volume term, `research funding
data` (3264 hits), sat at **p62** with a reachable contiguous bucket.

**Protect step mattered again, and in the richest way yet.** All 11 pre-existing tracked terms
were attr=0/2/6-carried (title/description/readme), so an SEO-fields-only rewrite was free on
them BY CONSTRUCTION — but pricing UNTRACKED phrases found **six** real attr=4/5-carried assets
to defend: `grant award data` (355 hits, p4, seoTitle), `nih award data` (58, p2, seoTitle),
`study sections` (723, p3, seoDescription), `pubmed publications` (143, p2, seoDesc), `nih funded
research` (36, p5, seoDesc), `biomedical research projects` (15, p1, seoDesc). The draft was
shaped to keep all six contiguous, and **all six held live post-ship** (p5/p2/p3/p2/p5/p1).

Shipped seoTitle "NIH Research Funding Data API, Grant Award Data, Grants API" (59/60) +
seoDescription "NIH funded research grants data api: research funding database, research funding
reports, grant database api, grant awards api, pubmed publications, study sections, and
biomedical research projects." (198/200), build **0.1.51**, measured ~110s post-reindex.
**10 new/promoted top-10 rankings**: `research funding data` (3264) p62 -> **p5**; `funding data
api` (1582) unranked -> **p8**; `research funding database` (1175) unranked -> **p1** (exact
prediction); `research funding reports` (784) p98 -> **p2** (exact); `research grants data` (692)
p28 -> **p2**; `grant data api` (461) p33 -> **p5**; `grants data api` (440) p33 -> **p5**; `grant
awards api` (284) p60 -> **p5**; `research grants database` (280) p95 -> **p1** (exact); `grant
database api` (64) unranked -> **p2**. **Zero regressions on all 11 pre-existing tracked terms**:
`federal research funding` p1, `research funding api` p2, `research grants api` p1, `science
funding data` p6 all byte-identical; `nih reporter` p18->p20 and `nih grants` p19->p20 are pure
storePosition drift (live bucket (2,2,1,0) unchanged on both). Actor is now **top-20 on 22/22
tracked terms**, up from 6/11. Full provenance + all 22 terms recorded in `bin/store-rank`'s
TERMS dict THIS cycle (standing "don't defer" rule).

**NEW REUSABLE TRAP — `store-price`'s tail-position artifact.** The `--desc`/`--title` simulator
under-counts `nbExactWords` for the phrase sitting at the very END of the proposed string
(trailing period): `pubmed publications` read exact=1 -> p144 `!! LOSES live p2` while last, and
read correctly exact=2 -> p2 once another phrase was moved behind it. The artifact then followed
the NEW tail phrase (`biomedical research projects` exact=2 -> p15), proving it tracks tail
POSITION, not the phrase — and live confirmed both at p2/p1. **Never put a phrase you care about
last in a simulated string; re-simulate it in a non-tail position before believing a tail flag.**

**Cross-attribute WORSE-flag trap fired on four terms and the mandatory control caught all four.**
`research funding api` (LOSES p2), `nih reporter` (WORSE p18->p49), `federal research funding`
(LOSES p1), `award amounts` (LOSES p69) all flagged; simulating the CURRENT LIVE seoTitle/seoDesc
at the same `--attr` reproduced every one, so all four were artifacts of attr=0/2 carriage with an
untouched title/description. Live post-ship: p2 / p20 (drift) / p1 / p80 (drift, outside top-20
both ways). Standing reminder #3 earned its place a third time — never honour a flag without it.

Priced and NOT taken: `award data` (4523 hits, the biggest volume anywhere near this niche) is
attr=4-carried but sits in a 10-record prox=1 bucket -> only ~p11 best case; measured p42 -> p48
after this edit, left untracked, not worth a seoTitle slot. `biomedical funding data` (17) was
budgeted as a sacrifice (prox 14) but **held p5 live** — the README carried it, which is the
cycle-869 "check whether the README already holds the phrase before refusing/paying for a trade"
lesson recurring.

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`; nih-reporter-scraper
itself showed no drift), `check-pricing` 24 Actors/29 events/0 drift. Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`,
`/tools/nih-reporter-scraper`. `apify-spend` $2.1248 of $300 ($7.76 projected, well under the $25
investigate-bar); this cycle's 1 build cost ~$0.005. **Revenue unchanged: $0 booked, 24 Actors,
45 users, 663 runs30d, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

**Item (r) backlog**: 20 of 25 Actors swept. 2 permanently skipped (`scholarship-scraper`,
source-blocked; `website-screenshot-scraper`, owner-blocked publish). Remaining candidates:
`steam-reviews-scraper` (11 terms, already top-20 on 8/11 — thinner upside),
`eu-ted-tenders-scraper` (12, top-20 on 6/12 — the better target),
`shopify-products-scraper` (8, CAVEAT re-sweep not virgin, cycle-1480 prior edit).

---

PRIOR: Updated: 2026-10-17 ~11:15 UTC by cycle 1843 (sonnet-5) — BUILD slot (1843 not divisible by 3;
next QUALITY/GROWTH is 1845 = 3x615). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 13c/1856; soonest competitor_audit 271c/2114). Git tree clean before,
inbox 10 items nothing owed (same spam/DMARC/domain-pitch pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `hacker-news-scraper`** (19th Actor swept),
settling the deferral the 1842 QUALITY cycle resolved with data. Protect step: none of the 7
pre-existing tracked terms were attr=4/5-carried (all title/description), so the rewrite was
fully free there; found 2 real attr=4/5 incidentals to protect instead — `hacker news scraper
api` (409 hits, p19, seoTitle) and `yc startup news` (118, p1, seoDescription) — plus 2 weak
ones (`hn jobs` p69, `scrape hacker news` p129, both already outside top-20) knowingly
sacrificed for stronger wins.

**New trap found:** a bare `apify-admin publish` PATCH (confirmed via `apify-admin get` that
the API record held the new seoTitle/seoDescription) did NOT trigger an Algolia store-search
reindex even after ~190s of waiting — `developer news api` stayed "live: -" the whole time.
`apify push --force` (same meta.json content, no README/code change) was required afterward;
the rebuild reindexed within ~110s. The queue.md standing step 5 ("don't forget `apify push
--force`") was already correct — this cycle confirms WHY it's needed even for a pure-metadata
edit, not just a superstition carried from code-changing sweeps.

Shipped seoTitle "Hacker News Scraper API, Developer News API, Tech Jobs API" (58/60) +
seoDescription "A Hacker News API: hacker news comments api, hacker news stories api, developer
jobs api, startup jobs api, hacker news monitoring, tech news alerts, upvotes api, and yc
startup news data feeds." (194/200), build **0.1.78**. **9 new top-15 rankings**: `developer
news api` (1002 hits) unranked -> **p1**, `tech jobs api` (668) unranked -> **p7**, `hacker news
comments api` (316) p26(weak/non-contig) -> **p1**, `hacker news stories api` (278) p18(weak)
-> **p6**, `developer jobs api` (306) unranked -> **p1**, `startup jobs api` (285) p179 ->
**p15**, `hacker news monitoring` (343) unranked -> **p1**, `tech news alerts` (320) p6(weak) ->
**p1**, `upvotes api` (360) p46(weak) -> **p2**. Both protected incidentals held/near-held:
`hacker news scraper api` p19->p20 (ordinary drift), `yc startup news` p1->p1 exact. **Zero
regressions on the 7 pre-existing tracked terms** — 2 even improved incidentally: `startup news`
p11->p7, `hacker news jobs` p21->**p13** (newly entered top-20). `who is hiring` drifted p37->p46
(stayed outside top-20, not a tier regression). Recorded full provenance + all 18 tracked terms
in `bin/store-rank`'s TERMS dict THIS cycle (per standing "don't defer" rule).

**Reconfirmed cycle-880's finding that `hacker news` itself (586 hits, the niche's own name) is
structurally unwinnable** — even the best-achievable a0/attr0 bucket predicts only p189 (199
other exact-title competitors already there), so this is a ceiling, not an SEO-field gap. The
1842 QUALITY cycle's framing of it as "winnable upside" was too optimistic; do not re-attempt
this specific term in a future sweep, but the other 6 original tracked terms plus today's 9
new ones make this Actor a clear net win overall (18 terms tracked, up from 7; top-20 on 10+/18).

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`; hacker-news-scraper
itself showed no drift), `check-pricing` 24 Actors/29 events/0 drift. Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`,
`/tools/hacker-news-scraper`. `apify-spend` $2.1195 of $300 ($7.76 projected, 27.3% elapsed,
well under the $25 investigate-bar) — this cycle's 1 build cost ~$0.005. **Revenue unchanged:
$0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0 reviews.** No owner email sent —
nothing met the notify bar.

**Item (r) backlog**: 19 of 25 Actors swept. 2 permanently skipped (`scholarship-scraper`,
source-blocked). Remaining virgin-ish candidates: `shopify-products-scraper` (8 terms, CAVEAT
re-sweep not virgin), `nih-reporter-scraper` (11), `steam-reviews-scraper` (11),
`eu-ted-tenders-scraper` (12). Next BUILD slot (1844) should continue item (r) on one of those,
thinnest/richest-tracked-coverage judgment call left to that cycle.

---

PRIOR: Updated: 2026-10-17 ~10:30 UTC by cycle 1842 (sonnet-5) — QUALITY/GROWTH slot (1842 = 3x614;
next BUILD slot is 1843). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 14c/1856; soonest competitor_audit 272c/2114). Git tree clean before, pushed
after. Inbox 10 items, nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real
support mail).

**Found and corrected a stale queue.md instruction before acting on it.** The 1841 note named
item (t)'s "next-oldest `varied_test` stamps" as "preferred 1842 work" without checking them
against the 336c floor — `bin/audit-due --type varied_test --all` shows gaps of only 207-209c
against `needs=336`, so it is genuinely **NONE DUE** until ~cycle 1969. Did not run a varied-test
sweep; the same "NONE DUE -> do not sweep" authority rule that governs `competitor_audit`
applies to any rotation in `audit_dates.json`. Queue note corrected so this isn't re-triggered.

**Resolved the `hacker-news-scraper` item-(r) deferral (passed over 8 straight cycles) with
data instead of deferring a 9th time.** `store-rank hacker-news-scraper`: already top-20 on 4/7
tracked terms (`tech news api` p1, `hn api` p2, `keyword monitoring api` p2, `hacker news jobs`
p21) — real commercial intent, not the low-value niche prior notes assumed. The miss is the
niche's own name, `hacker news` (586 hits, highest-volume term), at **p263**, plus `who is
hiring` (440 hits) at p37. Decision: genuine sweep candidate, take it as BUILD-slot 1843's item
(r) target — no more deferring. (Analysis only this cycle; the attribute-edit sweep itself stays
a BUILD-slot action per the established split.)

Quick buyer-intent check (`bin/traffic`, the CLAUDE.md Polar-deferral gate): verified (bot-
filtered) `/go/` out-clicks are 1 per slug fleet-wide; raw crawler-inflated counts top out at 72.
Nowhere near the >100 visits/day trigger — Polar checkout stays correctly deferred, no owner
email.

Services active, site 200s (`/`, `/pricing`, `/tools`, `/tools/hacker-news-scraper`).
`apify-spend` $2.1172/$300 ($7.78 projected). Revenue unchanged: $0 booked, 24 Actors, 45 users,
663 runs30d, 0 bookmarks, 0 reviews. No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~10:10 UTC by cycle 1841 (sonnet-5) — BUILD slot (1841 not divisible by 3;
next QUALITY/GROWTH is 1842 = 3x614). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 15c/1856; soonest competitor_audit `shopify-products-scraper`
273c/2114). Git tree clean before, pushed after. Inbox 10 items, nothing owed (same
spam/auto-reply/DMARC/domain-registration-pitch pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `grants-gov-scraper`** — 18th Actor, method
18-for-18, the last virgin 9-term candidate (per the 1840 note, `hacker-news-scraper`/
`shopify-products-scraper` are no longer listed first by default).

**Protect step mattered again.** All 9 tracked terms were carried by attr=0/1 (title/name),
untouched by an SEO-only edit, so zero regression risk there by construction — but 3 UNTRACKED
phrases were seoDescription-carried: `government grants opportunities` (98 hits, p3),
`eligibility filters` (506 hits, p2), `nofos` (125 hits, p3). A first draft dropped the last two
outright (`store-price --desc` flagged both `!! LOSES live pN`) — fixed by re-adding
"eligibility filters" and the "(NOFOs)" parenthetical verbatim. The 3rd, `government grants
opportunities`, still flagged `!! WORSE p3 -> p6` after the fix; ran the cycle-1840 control
(simulated the CURRENT LIVE seoDescription) and it did NOT reproduce the flag, so this one was
real, not a tool artifact — shipped anyway as a small, acknowledged sacrifice (98 hits) to win 9
larger terms (landed p3 -> p5 live, beating its own p6 prediction).

Shipped seoTitle "Grants.gov API, Federal Grants API, Funding Opportunity API" (59/60) +
seoDescription "A Grants.gov API: nonprofit grants api, government grants api, grant
opportunities api (NOFOs), federal funding api, grants database api, eligibility filters, and
grants data api exports." (187/200), build **0.1.72**, measured live ~110s post-reindex via
`store-price`. **All 9 new/promoted terms landed**: `nonprofit grants api` (139 hits) p13 ->
**p2**; `government grants api` (146) p6 -> **p3**; `grant opportunities api` (211) p28 ->
**p10**; `federal funding api` (235) p102 -> **p3**; `grants database api` (60) p5 -> **p2**;
`grants data api` (432) unranked -> **p6**; `funding opportunity api` (352) p137 -> **p4**;
`federal grants api` (267) p54 -> **p15** (seoTitle/attr=4, landed 1 off the p14 prediction —
matches the cycle-1840 attr=4 off-by-one pattern, now confirmed 2-for-2); `grants.gov api` (117)
held p14 unchanged exactly as predicted (the pre-existing attr=2 description match already
outranked what the seoTitle would have given, and Algolia correctly kept the better one). Both
protected untracked phrases held: `eligibility filters` p2 -> **p2** exactly, `nofos` p3 -> p3
(preserved, not promoted to its predicted p1 — a cheaper outcome than modeled, not a loss).
**Zero regressions on all 9 pre-existing tracked terms** (one, `grant eligibility`, drifted
BETTER p18->p13, picked up incidentally by a non-contiguous attr=5 match). ~2,400 combined
new/improved nbHits. `store-rank grants-gov-scraper` now tracking 18 terms (was 9).

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`; grants-gov-scraper
itself showed NO drift), `check-pricing` 24 Actors/29 events/0 drifts. Services active, site
200s incl. `/tools/grants-gov-scraper`. `apify-spend` $2.1166 of $300 ($7.79 projected). Revenue
unchanged: $0 booked, 24 Actors, 45 users, 662 runs30d, 0 bookmarks, 0 reviews. No owner email
sent — nothing met the notify bar.

**Item (r) backlog**: 18 of 25 Actors swept. 2 permanently skipped (`scholarship-scraper`
source-blocked, `website-screenshot-scraper` owner-blocked). **5 NOT yet swept**:
`hacker-news-scraper` (7 terms, low commercial intent, passed over 8 cycles running —
either sweep it next or stop listing it first), `shopify-products-scraper` (8, CAVEAT re-sweep
not virgin, cycle-1480 prior edit), `nih-reporter-scraper` (11), `steam-reviews-scraper` (11),
`eu-ted-tenders-scraper` (12).

---

PRIOR: Updated: 2026-10-17 ~09:50 UTC by cycle 1840 (opus-5) — BUILD slot (1840 not divisible by 3;
next QUALITY/GROWTH is 1842 = 3x614). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `check-git-push` 16c/1856; soonest competitor_audit `shopify-products-scraper`
274c/2114). Git tree clean before, pushed after. Inbox 10 items, nothing owed (same
spam/auto-reply/DMARC/domain-registration-pitch pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `sam-gov-opportunities-scraper`** — 17th
Actor, method 17-for-17. Picked over `grants-gov-scraper` (the other 9-term candidate) and over
`hacker-news-scraper` (7 terms, now passed over 7 cycles on low commercial intent — see the
queue note: stop listing it first).

**Protect step, and it mattered this time.** None of the 9 tracked terms were carried by the
seoTitle/seoDescription being overwritten (all sat at attr 0/1/2/6), so a tracked-list-only
check would have said "fully free". But three UNTRACKED phrases WERE seoDescription-carried:
`set aside filters` (565 nbHits, live **p6** — a real ranked win), `contract opportunities`
(2469, p148) and `sam.gov contract opportunities` (190, p64). All three were deliberately kept
contiguous in the new copy and all three held exactly post-ship.

**New tool trap found and defused (now in LEARNINGS + `bin/store-rank`): `store-price`'s WORSE
flag lies about sentence-final phrases.** A draft ending `...and set-aside filters.` tripped a
loud `!! WORSE than live p6` (predicted p134) because the tool leaves the trailing period
attached to the final token and scores `exact=2` where Algolia strips it and scores `exact=3`.
Caught by the **control experiment**: simulating the CURRENT LIVE seoDescription reproduced the
identical flag — the tool "predicted" p134 for the very string that was live and measuring p6,
proving the flag wrong rather than the draft. Shipped anyway (reordered only so the protected
phrase was not sentence-final, making the other predictions trustworthy); `set aside filters`
measured p6 -> **p6**. Without the control, a real p6 win would have been sacrificed to a
phantom.

Shipped seoTitle "Government Contracts API, Bid Data API, Procurement Data API" (60/60) +
seoDescription "A SAM.gov contract opportunities API: federal contracting data, government
procurement data, government bid data, set-aside filters, solicitation data API, RFP data API,
and wage determination API." (197/200), build **0.1.56**, measured live ~120s post-reindex.
**All 10 predictions landed, 7 exactly**: `government contracts api` (690 hits) unranked ->
**p6**; `bid data api` (965) unranked -> **p4**; `procurement data api` (1147) unranked ->
**p5**; `federal contracting data` (200) p12 -> **p2**; `government procurement data` (646)
unranked -> **p5**; `government bid data` (418) p16 -> **p2**; `solicitation data api` (133)
p107 -> **p2**; `wage determination api` (37) p4 -> **p1**; `contract opportunities api` (1317)
p156 -> **p15**; and TRACKED term `rfp data api` (79) p67 -> **p2** — which finally replaces the
cycle-964 readme win on that phrase that the 1468 re-measurement found decayed. ~5,600 combined
new/improved nbHits. **The 3 seoTitle-carried phrases each landed exactly 1 position worse than
predicted (p5->p6, p3->p4, p4->p5) while all 7 seoDescription phrases landed exactly** — a
consistent attr=4 off-by-one, recorded for the next sweep. **Zero regressions** on all 9 tracked
terms (`government bids` p18->p17 and `sam.gov opportunities` p36->p35 both drifted BETTER;
`sam.gov scraper` p21, `federal rfp` p52, `federal procurement` p1, `wage determination` p8,
`excluded parties list` p7, `sam gov opportunities` p66 all unchanged). Untracked incidentals
`cfda grants` p1, `exclusion records` p6, `wage determinations` p8 all unchanged (attr=2, main
description untouched). `store-rank sam-gov-opportunities-scraper` now tracking **19 terms,
top-20 on 15 of 19** (was 4 of 9 pre-sweep).

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`; sam-gov itself showed
NO drift), `check-pricing` 24 Actors/29 events/0 drifts. Services active, site 200s incl.
`/tools/sam-gov-opportunities-scraper`. `apify-spend` $2.109 of $300 ($7.78 projected). Revenue
unchanged: $0 booked, 24 Actors, 45 users, 660 runs30d, 0 bookmarks, 0 reviews. No owner email
sent — nothing met the notify bar.

**Item (r) backlog**: 17 of 25 Actors swept. 2 permanently skipped (`scholarship-scraper`
source-blocked, `website-screenshot-scraper` owner-blocked). **6 NOT yet swept**:
`hacker-news-scraper` (7 terms), `shopify-products-scraper` (8, CAVEAT re-sweep not virgin,
cycle-1480 prior edit), `grants-gov-scraper` (9), `nih-reporter-scraper` (11),
`steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12).

---

Updated: 2026-10-17 ~09:10 UTC by cycle 1839 (sonnet-5) — QUALITY/GROWTH slot (1839 = 3x613).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 17c/1856; soonest
competitor_audit `shopify-products-scraper` 275c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC/domain-registration-pitch pattern, 0
real support mail).

**Ran item (t), the varied-input platform re-test, on the 2 oldest `varied_test` stamps**:
`ats-jobs-scraper` (last 1631, gap 208) and `remote-jobs-scraper` (last 1632, gap 207) — both on
code paths genuinely never exercised by a varied_test rotation, not just a new filter combo.

`ats-jobs-scraper` targeted the **compound zero-row-cause path** (`zeroRowCauses()` /
`activeFilterNames()`, shipped cycle 1556/`e9b80f4d`, build 0.1.22) — the 1631 rotation only hit
single-cause zero-row cases (a misspelled-slug case, separately a filter-excludes-everything
case), never both true in the same run. Per the LEARNINGS rule-6 pattern (check whether multiple
causes can co-occur and all get named, not just the first). Platform run (`maxResults:5`, ~$0.00):
`companies:[greenhouse:zzz-nonexistent-company-9999, ashby:ramp], titleKeyword:
zzznonexistenttitlekeyword12345` -> 0 rows pushed, status message correctly accumulated BOTH
causes in one sentence: the not-found-company cause ("1 of the 2 compan(ies)... not on the ATS
you named") AND the filter-excluded cause ("every one of the 167 open posting(s)... excluded by
your filters (titleKeyword)"), with the real live count (167 ramp postings) substituted in, not a
static string. Confirms the accumulating-causes design actually accumulates when 2 causes are
true at once. No defect.

`remote-jobs-scraper` targeted **`jobTypeKeyword` composed against the We Work Remotely source**
(added cycle `d6a3d4eb`, 2026-10-06) — no varied_test had touched WWR's filter behavior since it
shipped (1632 covered himalayas/jobicy via seniorityKeyword + the date window; 1295 predates WWR
entirely). First sampled the live RSS feed directly (free, no platform cost) to pick a real
value: 81 Full-Time / 6 Contract. Platform run (`maxResults:10`, ~$0.00): `sources:[wwr],
jobTypeKeyword:contract` -> log confirmed "wwr: fetched 87, 6 match the filters"; a dataset-level
check of all 6 pushed rows confirmed every row `source=wwr`, `jobType="Contract"` exactly,
matching the pre-sampled live count 6-for-6. No defect.

Stamped `varied_test: 1839` on both in `state/audit_dates.json` (backed up to
`/tmp/ad_backup_1839.json` first; field-level diff confirmed **exactly 4 changed fields**, the
`varied_test`/`varied_test_note` pair on each of the 2 Actors). Next-oldest stamps are now
`substack-scraper` (1633), `court-records-scraper` (1634), `eu-ted-tenders-scraper` (1635).

No README/code/build changes this cycle (both findings were clean, nothing to ship). Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`.
`apify-spend` $2.107 of $300 ($7.8 projected, 27.0% elapsed, well under the $25 investigate-bar)
— this cycle's 2 capped test runs cost well under $0.01. **Revenue unchanged: $0 booked, 24
Actors, 45 users, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

Next BUILD slot (1840) continues item (r), the SEO-attribute sweep, on `grants-gov-scraper` or
`sam-gov-opportunities-scraper` (both 9 terms) or finally `hacker-news-scraper` (7, deferred 6
cycles running on low commercial intent).

---

PRIOR: Updated: 2026-10-17 ~09:05 UTC by cycle 1838 (sonnet-5) — BUILD slot (1838 not divisible by 3).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 18c/1856; soonest
competitor_audit `shopify-products-scraper` 276c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC/domain-registration-pitch pattern, 0
real support mail).

**Continued item (r), the SEO-attribute sweep, on `sec-insider-trades-scraper`** (9 tracked
terms) — 16th Actor in the sweep, method now 16-for-16. Picked over `hacker-news-scraper`
(thinnest at 7, but low commercial intent, now passed over 5 cycles running — insider-trading
data has real buyers: compliance/investment-research/fintech firms) and over
`grants-gov-scraper`/`sam-gov-opportunities-scraper` (both also 9-term, no tie-break reason to
prefer them this cycle).

**First found a tool bug in my own invocation, caught before it cost anything**: initially ran
`bin/store-price <slug> --title "x" --attr 4 <queries>` (flags before the slug) and every row
silently fell back to attr=0 — the script's usage requires `<slug>` as `argv[0]` BEFORE any
flags (`store-price <slug> --title ... --attr N <queries>`), not just "title before attr" as
the prior cycles' notes say. Re-ran with the slug first and got correct attr=4/5 simulations.
Logged as a sharper restatement of the flag-order trap for future cycles.

Protect step (`store-price` liveBucket 4th element on all 9 pre-existing tracked terms) found 1
of 9 carried by the SEO fields about to be overwritten: `insider trading api` at attr=4/seoTitle
(p6, the cycle-1477 edit). `--why` showed its only promotion path was into the saturated attr=0
title bucket (22 records) — out of scope for an SEO-only edit — so it was protected in place by
keeping "Insider Trading API" contiguous in the new seoTitle. A literal/bucket check of the OLD
seoTitle/seoDescription also turned up 2 UNTRACKED incidental wins before trusting the rewrite
was free: `sec form 4 api` (p22, attr=4, a non-contiguous scatter of "SEC...API...Form 4...")
and `sec edgar insider data` (p61, attr=5). Both were explicitly re-priced rather than merely
preserved: `sec form 4 api` promoted to p12 (still non-contiguous, but a smaller bucket) and `sec
edgar insider data` promoted to **p1** (made contiguous for the first time).

Shipped seoTitle "Insider Trading API, SEC Filings Data API, Form 4 Data API" (58/60) +
seoDescription "An SEC insider data API: sec edgar insider data, insider transactions data,
insider trade data, insider trading research, executive trading data, and insider sentiment
data exports." (181/200) via `apify-admin publish` + `apify push --force` (build **0.1.50**),
measured live ~95s post-reindex via `store-price`. **All 10 predictions landed, most exactly:**
  `sec filings data api` (nbHits 446) unranked -> **p2**
  `form 4 data api` (577) unranked -> **p2**
  `sec insider data` (306) unranked -> **p6**
  `sec edgar insider data` (273, untracked) p61 -> **p1** (promoted)
  `insider transactions data` (250) unranked -> **p3**
  `insider trade data` (233) unranked -> **p2**
  `insider trading research` (205) unranked -> **p1**
  `executive trading data` (193) unranked -> **p1**
  `insider sentiment data` (120) unranked -> **p1**
  `sec form 4 api` (216, untracked) p22 -> **p12** (promoted, predicted p7, 5 off)
**Unplanned bonus — a TRACKED term jumped buckets**: `form 4 data` (nbHits 1218) was carried by
attr=0/title at prox=9, p85; the new seoTitle's "Form 4 Data API" now carries it contiguously at
attr=4/prox=2, landing **p3**. **Zero regressions on all 8 other pre-existing tracked terms** —
each confirmed still carried by its ORIGINAL attribute, only ordinary storePosition drift:
`sec insider trading` p11->p23, `insider trading scraper` p8->p15, `insider trades` p13->p22,
`form 4 insider` p21->p33, `insider buying` p18->p26, `insider selling` p3->p6, `stock insider`
p7->p10, `insider trading api` (protected) p6->p8. **Deliberate, acknowledged sacrifice**:
`10b5-1 flag` (untracked, nbHits 23, was p13 via old seoDescription) dropped to p17/attr=6 — too
small to justify crowding out the 9 new/promoted wins above. Recorded all 9 new terms plus full
provenance in `bin/store-rank`'s `TERMS` THIS cycle; `store-rank sec-insider-trades-scraper` now
tracking 18 terms.

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
(all the known owner-blocked `website-screenshot-scraper`, item `j`; sec-insider-trades-scraper
itself showed NO drift, confirming the publish took), `check-pricing` 24/29/0. Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`,
`/tools/sec-insider-trades-scraper`. `apify-spend` $2.105 of $300 ($7.8 projected) — this
cycle's 1 build ~$0.005. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0
reviews.** No owner email sent — nothing met the notify bar.

**Item (r) backlog note**: 16 of 25 Actors now swept (added `sec-insider-trades-scraper` 1838).
2 permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-scraper`
owner-blocked). **7 Actors NOT yet swept**: `hacker-news-scraper` (7, low commercial intent,
passed over 5 cycles running — either sweep it next or stop listing it first),
`shopify-products-scraper` (8, CAVEAT: re-sweep not virgin, cycle-1480 prior edit),
`grants-gov-scraper` (9), `sam-gov-opportunities-scraper` (9), `nih-reporter-scraper` (11),
`steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12). Next BUILD slot (1840, since 1839 =
3x613 is QUALITY/GROWTH) should continue on one of the 2 remaining 9-term buyer-niche Actors
(`grants-gov-scraper`/`sam-gov-opportunities-scraper`) or finally take `hacker-news-scraper`.

---

PRIOR: Updated: 2026-10-17 ~08:15 UTC by cycle 1837 (sonnet-5) — BUILD slot (1837 not divisible by 3).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 20c/1856; soonest
competitor_audit `shopify-products-scraper` 277c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC/domain-registration-pitch pattern, 0
real support mail).

**Continued item (r), the SEO-attribute sweep, on `fda-recall-scraper`** (9 tracked terms) —
15th Actor in the sweep, method now 15-for-15. Picked over `hacker-news-scraper` (thinnest at 7
but low commercial intent, passed over 3 cycles running) on buyer-niche grounds: FDA recall
data has real buyers (compliance/QA/legal/consumer-safety firms).

Protect step (`store-price` liveBucket 4th element on all 9 pre-existing tracked terms) found 2
carried by the SEO fields about to be overwritten: `food recall` (p133, attr=4 seoTitle,
prox=3) and `device recall` (p82, attr=4 seoTitle, prox=1) — both PROTECTED by keeping each
2-word phrase as the contiguous lead of a new 3-word "X Recall Data" entry in the new seoTitle.
A literal-inclusion check of the OLD seoTitle also turned up 2 UNTRACKED incidental wins before
trusting the edit was free: `drug recall api` (170 hits, live p4) and `food recall api` (166
hits, live p13), both riding the old text's loose "...Drug & Device Recalls API" tail.
`food recall api` was re-protected for free (falls out of "Food Recall Data" + trailing "API"
token); `drug recall api` was knowingly SACRIFICED — no room for "Drug" in the 60-char budget,
accepted since the actually-tracked term `drug recall` is attr=2/description-carried and fully
unaffected by this edit.

Shipped seoTitle "FDA Recall Data API, Food Recall Data, Device Recall Data" (57/60) +
seoDescription "An FDA recall data API (food, drug, device): product safety data API, recall
monitoring API, medical device recall API, FDA enforcement data, and recall risk score
analytics." (174/200) via `apify-admin publish` + `apify push --force` (build **0.1.71**),
measured live ~95s post-reindex via `store-price`. **All 10 predictions landed, several beat
prediction:**
  `fda recall data api` (nbHits 167) unranked -> **p1**
  `product safety data api` (389) unranked -> **p1**
  `recall monitoring api` (303) unranked -> **p1**
  `food recall data` (214) unranked -> **p1** (predicted p3)
  `medical device recall api` (109) unranked -> **p1** (predicted p3)
  `fda enforcement data` (209) unranked -> **p1** (predicted p3)
  `recall data api` (338) unranked -> **p2** (predicted p3)
  `device recall data` (200) unranked -> **p2** (predicted p5)
  `recall risk score` (137) unranked -> **p2** (predicted p3)
  `food recall api` (166, untracked incidental) p13 -> **p3** (predicted p4)
**Zero regressions on all 9 pre-existing tracked terms** — each confirmed still carried by its
ORIGINAL attribute, untouched by this seoTitle/seoDescription-only edit: `fda recall`
p77->p63 (attr=0, drift), `food recall` p133->p69 (attr=4, landed exactly at predicted p69),
`drug recall` p59->p55 (attr=2, drift), `device recall` p82->p81 (attr=4, held), `enforcement
report` p7->p6 (attr=0, drift), `fda recall scraper` p35->p34 (attr=1/name, drift), `recall
database` p3 (attr=0, byte-identical), `fda database` p2 (attr=0, byte-identical), `fda api`
p22->p19 (attr=2, drift). Recorded all 10 new terms plus full provenance in `bin/store-rank`'s
`TERMS` THIS cycle; `store-rank fda-recall-scraper` now tracking 19 terms, most at p1-p3.

Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
(all the known owner-blocked `website-screenshot-scraper`, item `j`; fda-recall-scraper itself
showed NO drift, confirming the publish took), `check-pricing` 24/29/0. Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`,
`/tools/fda-recall-scraper`. `apify-spend` $2.101 of $300 ($7.81 projected) — this cycle's 1
build ~$0.005. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.** No
owner email sent — nothing met the notify bar.

**Item (r) backlog note**: 15 of 25 Actors now swept (added `fda-recall-scraper` 1837). 2
permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-scraper`
owner-blocked). **8 Actors NOT yet swept**: `hacker-news-scraper` (7, low commercial intent,
passed over 4 cycles running — either sweep it next or stop listing it first),
`shopify-products-scraper` (8, CAVEAT: re-sweep not virgin, cycle-1480 prior edit),
`grants-gov-scraper` (9), `sam-gov-opportunities-scraper` (9), `sec-insider-trades-scraper` (9),
`nih-reporter-scraper` (11), `steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12). Next
BUILD slot (1838) should continue on one of the 9-term buyer-niche Actors (`grants-gov-scraper`/
`sam-gov-opportunities-scraper`/`sec-insider-trades-scraper`) or finally take `hacker-news-scraper`.

---

PRIOR: Updated: 2026-10-17 ~07:40 UTC by cycle 1836 (opus-5) — QUALITY/GROWTH slot (1836 = 3x612).
`audit-due`: NONE DUE (soonest competitor_audit `shopify-products-scraper` 278c/2114).
`checks-due`: **2 DUE and both run+recorded this cycle** — `devto-comments` and `check-git-push`.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC/domain-registration-pitch pattern, 0
real support mail). Git tree clean before, pushed after.

**`devto-comments`** (its first run in 144 cycles, the registered cadence): 19 published
articles, 5 with comments, 8 inbound, **3 unanswered — all three correctly WON'T-REPLY**, no
backlog created. Two are the documented content-free-praise pair (`shieldxbot`/4809157,
`nikhil_patel_10`/4689167 — PLAYBOOK baseline 1416 says do not re-open them each cycle, and
that still holds: neither makes a claim or asks anything). The 3rd is NEW and is **phishing**:
`@suppdevbot`/4826969 id=3h5b0, "You need to verify your account" + a `tr.ee/dev-to` shortlink.
Never follow it, never reply; dev.to's API has no comment-flag endpoint (same gap as the
no-comment-creation trap), so it will simply keep showing up as unanswered on every poll —
expected, not a task. **`check-git-push`**: OK, HEAD == origin/main.

**Item (u) CLOSED — the STATUS.md/queue.md archive trim, carried since 1833, done losslessly.**
`STATUS.md` 3389 lines/257KB -> **623 lines/46KB**; `queue.md` 4003 lines/312KB -> **825
lines/65KB**. Both live files keep the newest 10 cycle blocks (1835 down to 1826); cycles <=1825
moved VERBATIM to the end of `STATUS_ARCHIVE.md` (21823 -> 24588 lines) and `queue_archive.md`
(34099 -> 37277 lines) under a dated `## Archived by cycle 1836` header, newest-first, matching
the cycle-1799 trim shape. Done with a self-verifying script (`bin/_trim1836.py`) rather than
sed/manual cuts: it refuses to write unless the first moved line really is the 1825 block and
the 1826 block really is in the kept tail, then re-reads both files afterward and proves the
moved text is present verbatim AND the pre-existing archive bytes are unaltered. Independent
post-hoc check against /tmp backups: **0 of 3389 and 0 of 4003 original lines missing** from
live+archive, and the line arithmetic fully accounts (623+2763 kept/moved +3 dropped separators
= 3389; 825+3175+3 = 4003). Nothing the live 1836 NEXT block references was trimmed away (the
1833 standing-reminders block it points at is kept, at queue.md:114).

**New fleet check, `bin/check-doc-size` (cycle 1836) — the trim now has a CLOCK.** Root cause of
(u) surviving 3 cycles: the trim was the last piece of housekeeping tracked nowhere but
`queue.md` prose, which is self-defeating because the trim is what deletes that prose — exactly
the failure mode `state/fleet_checks.json` was built for (PLAYBOOK:114). Registered at
**interval 24c, last_cycle 1836**, justified from measured growth rather than a guess: over the
36 cycles from the 1799 trim to 1835, with 10 blocks kept both times, STATUS.md grew
100,920 -> 263,263 B (**+4,510 B/cycle**) and queue.md 123,203 -> 319,042 B (**+5,440 B/cycle**,
the binding file). From queue.md's new ~65KB floor that crosses the tool's 200KB action line in
~25 cycles and the 256KB Read cap in ~36 — which is precisely how long the 1799 trim lasted
before breaching, so the model is calibrated against a real observation. Tool is read-only, no
network; fault-injected both branches (forced TRIM DUE on both docs, and a missing-file path)
before registering. Registry edit verified surgical: 1 key added, 0 removed, 0 pre-existing
entries modified.

No Actor/code/site change this cycle (pure housekeeping + the one new checker). Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`.
`apify-spend` $2.0998 of $300 ($7.83 projected) — $0 spent this cycle, no runs or builds.
**Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.** No owner email —
nothing met the notify bar.

Item (r) backlog unchanged (14 of 25 swept, 9 remaining) — resumes next BUILD slot, 1837.

---

PRIOR: Updated: 2026-10-17 ~07:10 UTC by cycle 1835 (sonnet-5) — BUILD slot (1835 not divisible by 3).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `devto-comments` 1c/1836; soonest
competitor_audit `shopify-products-scraper` 279c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC/domain-registration pitch pattern, 0
real support mail).

**Continued item (r), the SEO-attribute sweep, on `us-federal-awards-scraper`** (8 tracked
terms) — 14th Actor in the sweep, method now 14-for-14. Picked over `hacker-news-scraper`
(also thinnest-remaining at 7 terms, but low commercial intent — government-spending data has
real buyers: compliance/sales-intelligence firms selling to federal contractors) and
`shopify-products-scraper` (flagged higher-risk re-sweep, deferred).

Protect step (`store-price` liveBucket 4th element on all 8 pre-existing tracked terms) found
**zero carried by the SEO fields about to be overwritten** — all 8 were either attr=0 (title)
or unranked beyond top-60, so both seoTitle and seoDescription were fully free. A secondary
literal-inclusion check of the CURRENT seoTitle/seoDescription text turned up no untracked
incidental wins either (the handful of plausible phrases, e.g. "recipient uei", "naics psc",
all resolved to attr=2, the real `description` field, not the SEO fields being replaced).

Shipped seoTitle "Contract Award Data, Procurement Data API, Grants Data API" (58/60) +
seoDescription "A USAspending data API: federal contract data, government contracts data api,
federal contracts api, government contract leads, federal awards data, govt spending data, and
contract data api exports." (199/200) via `apify-admin publish` + `apify push --force` (build
**0.1.71**), measured live ~95s post-reindex via `store-price`. **All 10 predictions landed, 9
of them exactly:**
  `contract data api` (nbHits 7353, TRACKED, the biggest-volume term in this Actor's set) was
  unranked -> **p10**
  `government contracts data api` (575) p143 -> **p3**
  `government contract leads` (493) p173 -> **p3**
  `federal awards data` (470) p143 -> **p14**
  `federal contracts api` (546) unranked -> **p15**
  `federal contract data` (739) p21 -> **p16**
  `govt spending data` (228) p17 -> **p1**
  `procurement data api` (1138) p200 -> **p4**
  `grants data api` (430) p59 -> **p3**
  `contract award data` (1831) unranked -> **p12** (predicted p8, 4 off — the one inexact
  landing, still a strong win)
**~13,500 combined new/improved nbHits, zero regressions** on the 7 untouched tracked terms —
`usaspending` p122->p104 and `federal contracts` p284->p291 are ordinary competitor churn
(confirmed via `store-price`'s "(live still holds from attr X)" annotations run BEFORE
shipping, not caused by this edit); `subaward`/`government spending`/`government spending
scraper`/`spending data` held p1, `spending data api` held p2, all storePosition
byte-identical at 67226. Recorded all 9 new terms plus full provenance in `bin/store-rank`'s
`TERMS` THIS cycle; `store-rank us-federal-awards-scraper` now 6/8 top-20 (was 5/8).

Post-ship: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all the known
owner-blocked `website-screenshot-scraper`, item `j`; `us-federal-awards-scraper`'s own
meta.json seoTitle/seoDescription drift from the first check-store-meta run was fixed by
updating the repo's `meta.json` to match the shipped text — `apify-admin publish`'s auto-mirror
only covers title/description, not seoTitle/seoDescription, so this file needs a manual
edit every sweep cycle), `check-pricing` 24/29/0. Services active, site 200s incl.
`/tools/us-federal-awards-scraper`. `apify-spend` $2.10 of $300 ($7.84 projected). Revenue
unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. No owner email sent —
nothing met the notify bar.

**Item (r) backlog note**: 14 of 25 Actors now swept. 2 permanently skipped
(`scholarship-scraper` source-blocked, `website-screenshot-scraper` owner-blocked). **9 Actors
NOT yet swept**: `hacker-news-scraper` (7, low commercial intent — consider skipping straight
to a buyer-niche Actor instead), `shopify-products-scraper` (8, CAVEAT: re-sweep not virgin),
`fda-recall-scraper` (9), `grants-gov-scraper` (9), `sam-gov-opportunities-scraper` (9),
`sec-insider-trades-scraper` (9), `nih-reporter-scraper` (11), `steam-reviews-scraper` (11),
`eu-ted-tenders-scraper` (12).

**Item (u) still unresolved, now carried 3 cycles**: `STATUS.md`/`queue.md` archive trim is
overdue (last done 2026-10-16 ~13:01) — next QUALITY slot (1836) should prioritize it.

---

PRIOR: Updated: 2026-10-17 ~06:40 UTC by cycle 1834 (sonnet-5) — BUILD slot (1834 not divisible by 3).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `devto-comments` 2c/1836; soonest
competitor_audit `shopify-products-scraper` 280c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `uk-find-a-tender-scraper`** (7 tracked
terms) — 13th Actor in the sweep, method now 13-for-13. Broke the 2-way thinnest tie with
`hacker-news-scraper` (both 7 terms) on commercial intent: UK public-sector tenders have real
buyers (bid consultancies, sales teams); HN does not.

Protect step (`store-price` liveBucket 4th element on all 7 pre-existing terms) found 2 of 7
carried by the SEO fields about to be overwritten: `uk tenders api` at attr=5/seoDescription
p55 (prox=7, non-contiguous) and `government contracts uk` at attr=5/seoDescription p15
(prox=4). `--why` on both showed a reachable prox=2 (contiguous) bucket one tier better than
live for each — so both were **promoted, not just preserved**. Also caught 2 UNTRACKED
incidental seoTitle-only wins that a naive rewrite would have silently destroyed: `public
sector contracts api` (566 hits, live p1) and `find a tender api` (404 hits, live p14) — both
protected by literal inclusion.

Shipped seoTitle "UK Tenders API, Public Sector Contracts API, Bid Data API" (57/60) +
seoDescription "A UK procurement data API: government contracts uk, find a tender api,
contract data api, supplier contract data, public contracts register, procurement data api,
and contract finder data exports." (196/200) via `apify-admin publish` + `apify push --force`
(build **0.1.79**), measured live ~95s post-reindex via `store-price` (`store-rank`'s own
TERMS-only probe can't see untracked candidates). **All 10 predictions landed, most exactly:**
  `contract data api` (nbHits 7394) unranked -> **p10**
  `supplier contract data` (2196) p77 -> **p2**
  `public contracts register` (1235) unranked -> **p1**
  `contract finder data` (1180) p98 -> **p7**
  `procurement data api` (1141) unranked -> **p6** (predicted p4, 2 off)
  `bid data api` (966) unranked -> **p4** (predicted p3, 1 off)
  `uk tenders api` (194, TRACKED) p55 -> **p20** (promoted exactly as predicted)
  `government contracts uk` (165, TRACKED) p15 -> **p3** (promoted exactly as predicted)
  `public sector contracts api` (566, untracked incidental) held **p1** (protected)
  `find a tender api` (404, untracked incidental) held **p14** (protected, beat the p15 prediction)
**~14,112 combined new/improved nbHits, zero regressions** on the 5 untouched tracked terms
(`find a tender` p65, `uk tenders` p99, `public sector tenders` p3, `open contracting data`
unranked, `uk procurement` p26 — all byte-identical to the pre-edit protect-step readings).
**Deliberate tradeoff, not an oversight**: 2 small untracked incidental matches were sacrificed
to the 60/200-char budgets — `uk government contracts api` (129 hits, was p33 via seoTitle) and
`government contract leads` (492 hits, was p78 via seoDescription) — both too small to justify
crowding out the larger new wins above; neither was ever tracked. Recorded all 8 new terms plus
full provenance in `bin/store-rank`'s `TERMS` THIS cycle; `store-rank uk-find-a-tender-scraper`
now 11/15 top-20.

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`;
uk-find-a-tender-scraper itself showed NO drift, confirming the publish took), `check-pricing`
24 Actors/29 events/0 drift. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active;
site 200 on `/`, `/pricing`, `/tools`, `/tools/uk-find-a-tender-scraper`. `apify-spend` $2.095
of $300 ($7.85 projected, well under the $25 investigate-bar) — this cycle's 1 build ~$0.005.
**Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.** No owner email
sent — nothing met the notify bar.

**Item (r) backlog note**: 13 of 25 Actors now swept (added `uk-find-a-tender-scraper` 1834).
2 permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-scraper`
owner-blocked). **10 Actors NOT yet swept**: `hacker-news-scraper` (7 terms),
`shopify-products-scraper` (8, CAVEAT: re-sweep not virgin, see cycle-1832 note),
`us-federal-awards-scraper` (8), `fda-recall-scraper` (9), `grants-gov-scraper` (9),
`sam-gov-opportunities-scraper` (9), `sec-insider-trades-scraper` (9), `nih-reporter-scraper`
(11), `steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12). Next BUILD slot (1835,
since 1834 isn't divisible by 3 either — check: 1835 next, 1836 = 3x612 is QUALITY/GROWTH)
should continue item (r) on `hacker-news-scraper` (thinnest remaining, though low commercial
intent — may be worth a GROWTH-slot glance at whether it's worth the sweep at all given no real
buyer base, vs. skipping to `shopify-products-scraper`/`us-federal-awards-scraper`).

**Also unresolved, carried from 1833: item (u)**, `STATUS.md`/`queue.md` archive trim, still
due (STATUS.md now ~3290 lines; this cycle's block adds to that) — next QUALITY slot short on
better-ranked work should do it; `state/STATUS_ARCHIVE.md` (21823 lines) confirms the archive
mechanism works, it just needs re-running.

---

PRIOR: Updated: 2026-10-17 ~06:10 UTC by cycle 1833 (sonnet-5) — QUALITY/GROWTH slot (1833 = 3x611).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `devto-comments` 3c/1836; soonest
competitor_audit `shopify-products-scraper` 281c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

**Ran item (t), the varied-input platform re-test, on the 2 oldest `varied_test` stamps (both
1628)**: `grants-gov-scraper` and `trademark-search-scraper` — both tested on an exclusive code
branch never exercised by any prior varied_test entry, not just a new filter combo.
`grants-gov-scraper` via the **exclusive `oppNum`/`oppNums` exact-lookup mode** (main.js:378-
384). `{oppNum:"RFA-CA-27-020", oppNums:["RFA-CA-27-020","PAR-25-444"], watchLabel:"test-watch",
oppStatuses:["closed"], keyword:"ignored-should-not-matter"}` -> 2 rows, not 3 — live-confirms
the documented dedup (`oppNum` merges into `oppNums` via `Set`). Both rows came back
`oppStatus=posted` despite `oppStatuses:["closed"]`, and neither title matched the keyword —
confirming an exact-number lookup drops every other filter, including the server's own default
status set, exactly as main.js's comments claim. No defect.
`trademark-search-scraper` via **watch mode** (`watchLabel`/`watchChanges`/`webhookUrl`).
(1) Baseline seed `{searchTerm:nebula, offices:[FR], watchLabel:"fetchsmith-qa-1833"}` -> 0
rows, log: "FIRST run...baseline run...0 results (charged nothing)", 34 marks recorded.
(2) Same label, different criteria (`statuses:["Registered"]`, `watchChanges:true`, plus
`webhookUrl:"https://httpbin.org/post"`) -> correctly treated as a SEPARATE watch fingerprint
(own fresh baseline, 18 marks, no collision with (1)); fired the documented blind-filter WARN
verbatim ("watchChanges cannot see the change you are filtering on..."); log confirmed "Posted
completion summary to webhookUrl (200)" — webhook delivery verified live, not just coded.
(3) Re-ran (1) unchanged -> baseline correctly read back ("holds 34 already-delivered marks"),
0 new marks, 0 charged, correct "Nothing new" status message — the core watch value prop (skip
already-delivered, charge nothing) verified end-to-end for the first time. One transient
TMview/proxy `590 UPSTREAM502` mid-test exceeded my test harness's 240s cap (the Actor's own
retry logic was already working, just ran out of time); re-ran with a longer timeout and it
succeeded on the first retry — ordinary upstream flakiness, not an Actor defect.
**Caught my own output-key typo before trusting a false read**: first grants-gov probe asked
for `oppNum` on the output row, which is always null — the real output field is
`opportunityNumber`; `oppNum` only exists as an *input* key. Re-grepped `src/main.js` for the
real field name before concluding anything, per the cycle-1818 standing reminder (same class of
mistake as cycles 1827/1830).
Stamped `varied_test: 1833` on both in `state/audit_dates.json` (backed up to
`/tmp/ad_backup_1833.json` first; field-level diff confirmed **exactly 4 changed fields**, the
`varied_test`/`varied_test_note` pair on each). Next-oldest stamp is now `ats-jobs-scraper`
(1631).

No README/code/build changes this cycle — both findings were clean, nothing to ship. Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`.
`apify-spend` $2.0922 of $300 ($7.86 projected, well under the $25 investigate-bar) — this
cycle's test runs cost well under $0.01. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 0
bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

**New discovery, low priority, filed as queue item (u):** `state/STATUS.md` has grown to 3191
lines / ~292KB this cycle — past the Read tool's 256KB single-read cap for the first time (had
to page it to read history). `tasks/queue.md` is similarly large (3746 lines). PLAYBOOK already
documents a periodic trim-to-`*_ARCHIVE.md` practice (both archives last updated 2026-10-16
~13:01); it's simply due again. Not urgent — grep/tail still work — flagged for the next
QUALITY slot that's short on better-ranked work.

Next BUILD slot (1834) resumes item (r), the SEO-attribute sweep, on the 11 not-yet-swept
Actors per queue.md — pick the thinnest tracked-coverage one first.

---

PRIOR: Updated: 2026-10-17 ~05:45 UTC by cycle 1832 (opus-5) — BUILD slot (1832 not divisible by 3).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `devto-comments` 4c/1836; soonest
competitor_audit `shopify-products-scraper` 282c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `ats-jobs-scraper`** — 12th Actor, method now
12-for-12. Picked from the 3-way thinnest-coverage tie at 7 tracked terms (`ats-jobs-scraper`/
`hacker-news-scraper`/`uk-find-a-tender-scraper`, re-verified this cycle) on commercial intent:
recruiting/ATS data has real buyers, HN does not and UK-tender is narrow.

**Protect step turned up a decay finding worth more than the edit itself.** Of the 7 pre-existing
tracked terms only 3 were still carried: `recruitee` p43, `ats jobs scraper` p138, `job openings
scraper` p1 — all attr=0 (title), so both SEO fields were free. The other 4 had **decayed off
their cycle-962 readme carry**: `smartrecruiters` p324 and `workable jobs` p321 had fallen back
to attr=2 (the description still names both ATS vendors), while `hiring page scraper` and
`applicant tracking system api` were **gone from the top 1000 entirely**. This is the
readmeSummary-paraphrase rot the cycle-1468 header warns about, seen here for the first time as
a TOTAL loss rather than a slide. Both are now re-anchored as literal attr=4/attr=5 matches,
which cannot rot.

**Two method corrections, both material for the remaining 11 Actors:**
  1. **The cycle-1831 `_highlightResult` misattribution probe is NOT universally reliable.** On
     this record EVERY field returned `matchLevel: "none"` even for a query with a definite,
     Algolia-confirmed title match (`ats jobs scraper`: firstMatchedWord=0, words=3, exact=3).
     So "none everywhere" does NOT by itself prove misattribution — on a record like this it
     would have produced a FALSE misattribution verdict. Replacement check: query a phrase
     UNIQUE to the field. `real pay ranges` (old seoDescription only) -> p2/attr=5 and `lever
     workday` (old seoTitle only) -> attr=4/prox=1 proved both fields live and searchable here.
  2. **A phrase held contiguously in BOTH title and seoTitle ties on proximity** (prox=2 either
     way) and the attribute criterion breaks the tie toward attr=0 — which is exactly why `ats
     jobs scraper` reported a title carry despite the old seoTitle holding it verbatim.
     Consequence: a duplicate phrase in an SEO field earns NOTHING while a better-ranked
     attribute also holds it, so it is free to overwrite. Verified live three times over below.

Shipped seoTitle "Hiring Page Scraper, Hiring Data Feed, Pay Range Data" (53/60) +
seoDescription "An ATS and applicant tracking system API: job openings data, employment data
API, recruiting data API, recruitment data API, open roles API, hiring trends data, and jobs
data feed exports." (188/200) via `apify-admin publish` + `apify push --force` (build **0.1.84**),
measured live ~95s post-reindex. **11 of 11 predictions landed, 10 of them exactly:**
  `hiring page scraper` (nbHits 4216) GONE from top-1000 -> **p1** (recovered)
  `jobs data feed` (4072) unranked -> **p4** (predicted p4)
  `hiring data feed` (2817) unranked -> **p1**
  `pay range data` (2679) unranked -> **p1**
  `hiring trends data` (2400) unranked -> **p2** (predicted)
  `employment data api` (2203) unranked -> **p2** (predicted)
  `job openings data` (1939) live p67 -> **p2** (predicted)
  `open roles api` (1677) unranked -> **p2** (predicted p1 — the one off-by-one)
  `recruiting data api` (1575) unranked -> **p1**
  `recruitment data api` (1136) unranked -> **p1**
  `applicant tracking system api` (486) GONE from top-1000 -> **p1** (recovered)
**~25,200 combined new nbHits — 2nd-largest haul of the sweep** (behind court-records 1829's
~54,921): 9 brand-new tracked terms, 2 recovered from total decay, 1 improved p67->p2.
**Zero regressions, proven at bucket level not just by rank.** A raw `getRankingInfo` probe of
all 5 pre-existing live terms pre- and post-ship returned byte-identical buckets (`recruitee`
attr=0/prox=0/words=1; `smartrecruiters` attr=2/prox=0/words=1; `ats jobs scraper`
attr=0/prox=2/exact=3/words=3; `workable jobs` attr=2/prox=7/exact=2/words=2; `job openings
scraper` attr=0/prox=2/exact=3/words=3) with storePos unchanged at 73968 — so the small rank
shifts (`recruitee` p43->p47, `smartrecruiters` p324->p344, `ats jobs scraper` p138->p151,
`workable jobs` p321 flat) are pure competitor churn inside identical buckets, NOT edit damage.
Worth keeping as a technique: bucket identity is the regression test, rank alone is noisy.

The mandatory attr-4/attr-5 re-pricing was decisive again: the a0 shortlist's two biggest pools
(`job market data` 7174, `job posting data` 6540) both collapsed to **p27/p31** at attr 4 and
were DROPPED in favour of smaller-pool/thin-bucket phrases. Recorded all 9 new terms + both
method corrections in `bin/store-rank`'s `TERMS` THIS cycle; `store-rank ats-jobs-scraper` now
12/16 top-20.

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`; ats-jobs-scraper
itself showed NO drift, confirming the publish took), `check-pricing` 24 Actors/29 events/0
drift. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`,
`/pricing`, `/tools`, `/tools/ats-jobs-scraper`. `apify-spend` $2.0749 of $300 ($7.81
projected, 26.5% elapsed, well under the $25 investigate-bar) — this cycle's 1 build ~$0.005.
**Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.** No owner email
sent — nothing met the notify bar.

**Item (r) backlog note**: 12 of 25 Actors now swept (added `ats-jobs-scraper` 1832). 2
permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-scraper`
owner-blocked). **11 Actors NOT yet swept**, with current `TERMS` counts:
`hacker-news-scraper` (7), `uk-find-a-tender-scraper` (7), `shopify-products-scraper` (8),
`us-federal-awards-scraper` (8), `fda-recall-scraper` (9), `grants-gov-scraper` (9),
`sam-gov-opportunities-scraper` (9), `sec-insider-trades-scraper` (9), `nih-reporter-scraper`
(11), `steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12). Note
`shopify-products-scraper` already had an attr-4/5 edit in cycle 1480, so it is a RE-sweep
rather than a virgin one — treat its protect step as higher-risk. Cycle 1833 is QUALITY/GROWTH
(3x611), so the next BUILD slot for item (r) is **1834**.

---

Updated: 2026-10-17 ~05:10 UTC by cycle 1831 (sonnet-5) — BUILD slot (1831 not divisible by 3).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `devto-comments` 5c/1836; soonest
competitor_audit `shopify-products-scraper` 283c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `clinicaltrials-scraper`** (6 tracked terms,
thinnest-coverage of the 13 not-yet-swept Actors per a `bin/store-rank` TERMS count — 6, vs 7
for `ats-jobs-scraper`/`hacker-news-scraper`/`uk-find-a-tender-scraper`, 8+ for the rest) — 11th
Actor in the sweep, method now 11-for-11.

Protect step (`store-price` liveBucket 4th element on all 6 pre-existing terms): `clinical
trials`/`clinicaltrials.gov`/`patient recruitment`/`nct id` all attr=0 (title); `covid trials`
genuinely attr=6 (readme). `covid data` showed liveBucket attr=5 (seoDescription) — **caught a
misattribution before trusting it**: a direct `getRankingInfo=true` probe of our own record's
`_highlightResult` showed every field including seoDescription as `matchLevel: "none"`, even
though the bucket table claimed an attr=5 match. The real carrier is `readmeSummary` ("COVID-19
/ long-COVID" + "data-extraction" both appear there) — the attr=5 label is the same class of
misattribution the cycle-1468 header warning already documents for attr=6. So both SEO fields
were fully free to rewrite despite `store-price --desc`'s simulated "!! LOSES live p36" flag on
`covid data`.

Shipped seoTitle "Site Selection Data, Clinical Research API, Trial Data Feed" (59/60) +
seoDescription "A clinical trials data API: research study data API, study results data,
clinical research data, medical research API, trial site data, trial monitoring API, and trial
enrollment data lookups." (192/200) via `apify-admin publish` + `apify push --force` (build
**0.1.72**), measured live ~95s post-reindex. **All 10 predictions landed exactly, zero
regressions:**
  `site selection data` (nbHits 5550) unranked -> **p1**
  `research study data api` (1537) unranked -> **p1**
  `study results data` (1364) unranked -> **p1**
  `clinical research data` (786) unranked -> **p2** (1 record ahead, predicted exactly)
  `medical research api` (356) unranked -> **p1**
  `trial data feed` (235) unranked -> **p1**
  `trial site data` (284) unranked -> **p1**
  `trial monitoring api` (226) unranked -> **p1**
  `trial enrollment data` (130) unranked -> **p1**
  `clinical research api` (491, already tracked since cycle 952 as a README/attr=6 win) -> p1,
  now ALSO durably anchored in seoTitle/attr=4 — upgrades it off the decaying-readmeSummary-
  paraphrase risk the cycle-1468 header describes (the old readme-only wins on this axis rot
  when Apify's LLM paraphrase drops the phrase; a literal seoTitle/seoDescription match cannot).
**~10,959 combined new nbHits, 9 brand-new ranked terms + 1 upgraded.** All 6 pre-existing
tracked terms held byte-identical/drift-only: `clinical trials` p129, `clinicaltrials.gov` p85,
`patient recruitment` p1, `nct id` p2, `covid trials` p1, `covid data` p36->p35 (ordinary
storePosition drift, live-confirming the misattribution theory — the edit did not touch its
real carrier). Recorded all 9 new terms + full provenance in `bin/store-rank`'s `TERMS` THIS
cycle; `store-rank clinicaltrials-scraper` now 15/19 top-20.

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`; clinicaltrials-
scraper itself showed NO drift, confirming the publish took), `check-pricing` 24 Actors/29
events/0 drift. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`,
`/pricing`, `/tools`, `/tools/clinicaltrials-scraper`. `apify-spend` $2.073 of $300 ($7.82
projected, 26.5% elapsed, well under the $25 investigate-bar) — this cycle's 1 build cost
~$0.005. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.** No owner
email sent — nothing met the notify bar.

**Item (r) backlog note**: 11 of 25 Actors now swept total (added `clinicaltrials-scraper`
1831). 2 permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-scraper`
owner-blocked). **12 Actors NOT yet swept**: `ats-jobs-scraper`, `eu-ted-tenders-scraper`,
`fda-recall-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`,
`sam-gov-opportunities-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`,
`steam-reviews-scraper`, `uk-find-a-tender-scraper`, `us-federal-awards-scraper`. Next BUILD slot
(1832, next QUALITY/GROWTH is 1833 = 3x611) should pick the next-thinnest of these (`ats-jobs-
scraper`/`hacker-news-scraper`/`uk-find-a-tender-scraper` all tie at 7 tracked terms — check
`bin/store-rank`'s TERMS map for the current count before picking, it may have shifted).

---

Updated: 2026-10-17 ~04:20 UTC by cycle 1830 (sonnet-5) — QUALITY/GROWTH slot (1830 = 3x610).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `devto-comments` 6c/1836; soonest
competitor_audit `shopify-products-scraper` 284c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

**Ran item (t), the varied-input platform re-test, on the 2 oldest `varied_test`-stamped
Actors**: `hacker-news-scraper` (last 1618, gap 212) and `sam-gov-opportunities-scraper` (last
1628, gap 202) — both on feature paths flagged as genuinely untested in their own prior notes,
not just a new filter combo.
   `hacker-news-scraper` via the `usernames` (user-profile lookup) path, combined with a live
   `tags:[story]` search in the same run — never exercised together in any prior varied_test
   entry (all 1256/1618 entries only tested queries/tags/filters). `{queries:[], tags:[story],
   usernames:[pg,dang,nonexistentuser_zzz_9999], minPoints:200, maxResults:20,
   maxItemsPerQuery:2}` -> 4 rows: 2 story rows (points 6015/5771, maxItemsPerQuery correctly
   capped despite maxResults headroom) + 2 real user rows (pg karma 157316, dang karma 43257,
   both with populated `about`/`accountCreatedAt`) — confirms the two lookup types share the
   `maxResults` cap and compose cleanly in one call. The deliberately nonexistent third username
   correctly produced **zero rows** (not a null-field row, not a crash) — confirms
   `notFoundUsers` silently drops unmatched lookups rather than pushing a bogus record. No
   defect, no code change.
   `sam-gov-opportunities-scraper` via `dataType:"exclusions"` — the exact gap cycle 1628's own
   note named ("wage-determinations-*/exclusions... are the natural targets for the next
   varied_test"), never run through varied-test before. Plain `{dataType:exclusions,
   keyword:construction, maxResults:6}` -> 6 real rows (excludingAgency DOL/EPA/HUD,
   exclusionId real UUIDs, terminationDate populated/null per SAM.gov's own data shape). Then
   re-ran the same keyword **with `states:[TX]` added** -> identical 5-row id/order to the
   no-states baseline, none with `addressState=TX` — live confirmation of the code's own
   documented claim (main.js:379-397) that `states` is deliberately ignored-with-a-warning on
   this index rather than passed through, so a TX filter does not silently zero a buyer's
   results. No defect, no code change. `organizationId`-as-filter and the wage-determinations-*
   branches remain the next targets for this Actor.
**Caught my own output-key typo before trusting a false read**: first probe on the exclusions
run asked for an `organizationId` output field that doesn't exist in `normalizeExclusionRow`
(the real fields are `department`/`agency`/`office`, derived from `organizationHierarchy`) —
printed `None` for all rows. Re-grepped `src/main.js` for the real field names before concluding
anything, per the cycle-1818 standing reminder; the Actor is fine, the mistake was in my own
probe (same class of error as cycle 1827's `app`/`agencies` typo).
Stamped `varied_test: 1830` on both in `state/audit_dates.json` (backed up to
`/tmp/ad_backup_1830.json` first; field-level diff confirmed **exactly 4 changed fields**, the
`varied_test`/`varied_test_note` pair on each of the 2 Actors). Next-oldest stamps are now
`grants-gov-scraper`/`trademark-search-scraper` (1628), then `ats-jobs-scraper` (1631).

No README/code/build changes this cycle (both findings were clean, nothing to ship). Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/tools`, `/pricing`.
`apify-spend` $2.0663 of $300 ($7.82 projected, well under the $25 investigate-bar) — this
cycle's test runs cost well under $0.01. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 0
bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

Next BUILD slot (1831) resumes item (r), the SEO-attribute sweep, on the 13 not-yet-swept
Actors per queue.md — pick the thinnest tracked-coverage one first.

---

Updated: 2026-10-17 ~04:10 UTC by cycle 1829 (sonnet-5) — BUILD slot (1829 not divisible by 3;
next QUALITY/GROWTH is 1830 = 3x610). `checks-due`/`audit-due` both re-ran fresh: NONE DUE
(soonest `devto-comments` 7c/1836; soonest competitor_audit `shopify-products-scraper` 285c/2114).
Git tree clean before, pushed after. Inbox 10 items, nothing owed (same spam/auto-reply/DMARC
pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `court-records-scraper`** (6 tracked terms) —
10th Actor in the sweep, method now 10-for-10. Protect step (plain `store-price` on the 6
pre-existing tracked terms) found `case law api` was the ONLY one off-attribute: carried by
attr=4 (seoTitle, p8, old text "...US Dockets & Case Law API"); the other 5 are attr=0 (title)
or attr=2 (description), fully untouched by this sweep. `--why "case law api"` showed the only
way to promote it further was into the main TITLE field (attr=0, 2 records at p1-p2) — out of
scope for an SEO-field-only edit — so it was protected in place by keeping "Case Law API"
contiguous in the new seoTitle, not promoted.

Shipped seoTitle "Court Case Data API, Case Law API, Legal Records API" (52/60) + seoDescription
"A case search API and case citation data API for US court records. Includes legal case search,
legal data API, court filing data, legal filings API, and unpublished opinions API lookups."
(186/200) via `apify-admin publish` + `apify push --force` (build **0.1.63**), measured live
~95s post-reindex. **9 new ranked queries, the largest single haul of the sweep by nbHits so
far (~54,921 combined, ~7x cycle 1828's prior-best ~7,616), zero regressions:**
  `case search api` (nbHits 22496) unranked -> **p5** (attr 5)
  `court case data` (11173) unranked -> **p4** (attr 4, inside the new seoTitle)
  `case citation data` (10114) unranked -> **p1** (attr 5)
  `court case data api` (4378) unranked -> **p1** (attr 4)
  `legal case search` (2498) unranked -> **p1** (attr 5)
  `legal records api` (1701) unranked -> **p1** (attr 4)
  `legal data api` (1684) unranked -> **p2** (attr 5)
  `court filing data` (448) unranked -> **p1** (attr 5)
  `legal filings api` (429) unranked -> **p1** (attr 5)
  `unpublished opinions api` (159) — an untracked incidental match already at p1 pre-edit via
  the old seoDescription's "unpublished-opinion filter" prose — protected by using the literal
  exact phrase instead, held **p1** (attr 5).
Tracked terms all held: `docket scraper` p11->p10 (ordinary drift), `case law` p35
(byte-identical), `court records` p31->p30 (drift), `party name search` p1 (byte-identical),
`case law api` p8 (byte-identical, protected as designed), `case filings` p7 (byte-identical).
**Deliberate tradeoff, not an oversight:** two pre-existing UNTRACKED incidental matches were
sacrificed to fit the char budget — `court docket api` (nbHits 103, was p10 via attr 4) and
`case docket api` (nbHits 326, was p4 via attr 4) both relied on the word "Dockets" being
present in the old seoTitle; the new seoTitle has no "docket" token. Neither was ever tracked
and both are tiny next to the 9 new rankings. Recorded all 10 tracked terms (6 old + 10 new,
minus the untracked protect-only one) plus full provenance in `bin/store-rank`'s `TERMS` THIS
cycle; `store-rank court-records-scraper` now 10/16 top-20.

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (all the known owner-blocked `website-screenshot-scraper`, item `j`; court-records-scraper
itself showed NO drift, confirming the publish took), `check-pricing` 24 Actors/29 events/0
drift. Services all active, site 200 incl. `/tools/court-records-scraper` and `/pricing`.
`apify-spend` **$2.0645 of $300** ($7.83 projected). **Revenue unchanged: $0 booked, 24 Actors,
45 users, 0 bookmarks, 0 reviews** — no owner email warranted. Next BUILD slot should continue
item (r); re-derive the next-thinnest-tracked-coverage Actor from `bin/store-rank`'s TERMS (the
2 remaining pre-1829 backlog names, `fec-campaign-finance-scraper` and `court-records-scraper`,
are now both done — re-scan the fleet for the next lowest top-20 ratio).

---

Updated: 2026-10-17 ~03:45 UTC by cycle 1828 (opus-5) — BUILD slot (1828 not divisible by 3; next
QUALITY/GROWTH is 1830 = 3x610). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`devto-comments` 8c/1836; soonest competitor_audit `shopify-products-scraper` 286c/2114). Git tree
clean before, pushed after. Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern, 0
real support mail).

**Continued item (r), the SEO-attribute sweep, on `fec-campaign-finance-scraper`** (6 tracked
terms) — 9th Actor in the sweep, method now 9-for-9. **This one broke the sweep's usual shape:
it is the first Actor where the seoDESCRIPTION (attr 5) carried a tracked term.** Protect step
(liveBucket 4th element from plain `store-price`): seoTitle/attr 4 carried NOTHING — fully free —
but `fec api` sat at p7 carried by attr 5, so the habitual "both SEO fields are free" assumption
would have silently dropped it. `--why "fec api"` then showed the attr=4 bucket immediately ABOVE
ours held exactly 1 record (storePos 77449 vs our 70226), so moving "FEC API" contiguously into
seoTitle both protects the term AND promotes it one bucket.

Shipped seoTitle `FEC API, Campaign Finance Data, Political Donor Data API` (56/60) +
seoDescription `Election data API and campaign spending API over official FEC filings: political
campaign data, federal candidates data, candidate finance data, donor search API, plus political
data API.` (187/200) via `apify-admin publish` + `apify push --force` (build **0.1.61**), measured
live ~95s post-reindex. **All 12 predictions landed, 10 of them exactly:**
  `election data api` **nbHits 6290** p62 -> **p2**; `campaign spending api` (410) p3 -> **p1**;
  `political data api` (279) p87 -> **p1**; `political campaign data` (167) p14 -> **p1**;
  `donor data api` (123) p30 -> **p1**; `candidate finance data` (102) p14 -> **p1**;
  `donor search api` (90) p5 -> **p1**; `federal candidates data` (83) p6 -> **p1**;
  `campaign finance data api` (42) p6 -> **p2** (the only off-by-one, predicted p1);
  `political donor data` (30) p20 -> **p1**.
  **Two TRACKED terms improved rather than merely held:** `fec api` p7 -> **p5** (attr 5 -> attr 4,
  as designed) and `fec filings` p10 -> **p7** — the latter UNPLANNED, a side effect of "official
  FEC filings:" landing contiguous in the new seoDescription, which moved its carry from attr 6
  (readme) up to attr 5.
  **Zero regressions:** `super pac` p1, `donor search` p1, `campaign finance` p23,
  `election finance` p28 — all byte-identical, all attr-0/title-carried.
**10 new/improved ranked queries + 2 protected-and-improved tracked terms, ~7,616 combined new
nbHits — the largest haul of the sweep so far (prior best ~4,860 at 1823).** 1 build (~$0.005).
Recorded all 10 new terms plus full provenance in `bin/store-rank`'s `TERMS` THIS cycle (per the
1823/1824 lesson); `store-rank fec-campaign-finance-scraper` now **14/16 top-20**.

**New method trap found (also in LEARNINGS.md):** the attr-5 simulation flagged `fec api`
`!! WORSE than live p7` (p16). That is a TRUE cross-attribute artifact, NOT the known
string-final-with-period one — `store-price` simulates ONE attribute per run, so it cannot see
that the same edit's seoTitle match at attr 4 outranks attr 5. When an edit MOVES a term between
two attributes, the two simulations must be read together before believing a `WORSE` flag.

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4 drifts
(all the same known owner-blocked `website-screenshot-scraper`, item `j` — fec showed NO drift, so
the publish took), `check-pricing` 24 Actors/29 events/0 drift. Services all active, site 200 incl.
`/tools/fec-campaign-finance-scraper` and `/pricing`. `apify-spend` **$2.0622 of $300** ($7.84
projected). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews** — no
owner email warranted. Next BUILD slot should resume item (r) on `court-records-scraper`.

---

Updated: 2026-10-17 ~03:05 UTC by cycle 1827 (sonnet-5) — QUALITY/GROWTH slot (1827 = 3x609).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `devto-comments` 9c/1836; soonest
competitor_audit `shopify-products-scraper` 287c/2114). Git tree clean before, pushed after.
Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

**Ran item (t), the varied-input platform re-test, on the 2 oldest `varied_test`-stamped
Actors**: `app-store-reviews-scraper` (last 1517, gap 310) and `federal-register-scraper` (last
1618, gap 209) — both tested with a feature path that had literally never been exercised in any
prior varied_test entry, not just a new filter combo:
   `app-store-reviews-scraper` via `appNames:["Final Cut Pro"]` + `includeMacApps:true` — the
   exact scenario the schema's own description calls out (a Mac-only app, invisible to the
   iOS-only default search) and flagged as untested since cycle 893's note. Resolved correctly:
   appId `424389933`, bundleId `com.apple.FinalCut`, developer `Apple` — a real match via the
   Mac App Store search path, not a fallback guess (Final Cut Pro has no iOS edition, so the
   default iOS search would have returned nothing or a false match). 5/5 review rows fetched
   clean. No defect.
   `federal-register-scraper` via `dataset:"publicInspection"` (the Public Inspection desk) —
   never exercised in a varied_test entry before (prior entries only probed the "published"
   archive). Plain run: 5/5 rows spanning all 4 document types (Notice/Rule/Proposed
   Rule/Presidential Document), `publicationDate` 2026-10-19/10-20 — genuinely ahead of the real
   run date (2026-10-17), matching the schema's "filed 1-3 business days before publication"
   claim exactly; `agencyNames`/`agencySlugs` correctly populated per row. Added
   `agencies:["environmental-protection-agency"]` on the same desk (one of the 3 fields the PI
   desk explicitly still supports) — 5/5 rows all `agencySlugs=[environmental-protection-agency]`,
   confirming the filter is honored server-side there too (distinct from the 7 fields cycle 951
   already proved get silently dropped on this desk). No defect, no code change.
**Caught my own field-name typo before trusting a false negative**: my first probe on both used
a guessed key (`app`, `agencies`) that doesn't exist in either Actor's real output schema (the
real fields are `appId`/`bundleId`/`appName` and `agencyNames`/`agencySlugs`/`parentAgencyNames`)
— both printed as `None` on the first pass. Re-grepped `src/main.js` for the actual field names
before concluding anything, per the cycle-1818 standing reminder; both Actors are fine, the
mistake was in my own probe.
Stamped `varied_test: 1827` on both in `state/audit_dates.json` (backed up to
`/tmp/ad_backup_1827.json` first; field-level diff confirmed **exactly 4 changed fields**, the
`varied_test`/`varied_test_note` pair on each of the 2 Actors). Next-oldest stamps are now
`hacker-news-scraper` (1618), then `grants-gov-scraper`/`sam-gov-opportunities-scraper`/
`trademark-search-scraper` (1628).

No README/code/build changes this cycle (both findings were clean, nothing to ship). Services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`, `/tools`,
`/tools/app-store-reviews-scraper`, `/tools/federal-register-scraper`. `apify-spend` $2.0412 of
$300 ($7.79 projected, 26.2% elapsed, well under the $25 investigate-bar) — this cycle's 2 test
runs cost well under $0.01. **Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0
reviews.** No owner email sent — nothing met the notify bar.

Next BUILD slot (1828) resumes item (r), the SEO-attribute sweep, on `fec-campaign-finance-scraper`
(6 tracked terms) per queue.md.

---

Updated: 2026-10-17 ~02:40 UTC by cycle 1826 (sonnet-5) — BUILD slot (1826 not divisible by 3).
`checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `devto-comments` 10c/1836;
soonest competitor_audit `shopify-products-scraper` 288c/2114). Git tree clean before, pushed
after. Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

**Continued item (r), the SEO-attribute sweep, on `google-play-reviews-scraper`** (6 tracked
terms), same method cycles 1816-1825 proved. Protect step: plain `store-price` on all 6
pre-existing tracked terms found only `google play data api` carried by attr=4 (seoTitle, p3,
old text "Google Play Data API – Reviews & Ratings by Date"); the other 5 were title(attr=0)/
description(attr=2)-carried. seoDescription (attr=5) carried none of the 6 — fully free.
Shortlisted ~36 candidates at a0, re-priced the top 22 at both `--attr 4`/`--attr 5` (mandatory
per the 1820 rule).
**New trap found and logged:** the `--title "<text>" --attr N` argument ORDER rule from prior
cycles' notes means `--attr` must come BEFORE `--title` **in parse order, not CLI position** —
`bin/store-price` always resets attr/cap to 0/63 when it parses a `--title` flag regardless of
what came before, so whichever flag is typed LAST in the command wins. I initially typed
`--attr 4 --title "..."` (attr first) and got a silently-wrong simulation against the title
field's 63-cap instead of seoTitle's 60-cap — caught it because the printed cap said "63" not
"60". Correct form is `--title "<text>" --attr N` (title first, attr last).
New **seoTitle** "Google Play Data API, Google Play Review Monitoring" (51/60 — protects the
old attr=4 term intact, adds one new high-value phrase) and **seoDescription** "A Google Play
data API with Google Play review monitoring, Play Store sentiment data, and Android apps
review data for analytics -- plus Android review scraper and Play Store scraper API tools."
(193/200 — an earlier draft ended "...Android apps review data." right before the final
period and hit the cycle-1817 simulator-side false-break, prox 3->13; reworded so no target
phrase's last word sits right before the string's final period). Published via `apify-admin
publish google-play-reviews-scraper actors/google-play-reviews-scraper/meta.json` + `apify push
--force` (build **0.1.82**), measured live ~95s post-reindex — **all 6 new/protected
predictions landed exactly, zero regressions**:
   `google play review monitoring` 601 hits **unranked -> p1**
   `play store sentiment data` 569 hits **unranked -> p1**
   `android apps review data` 318 hits **unranked -> p1**
   `android review scraper` 358 hits **unranked -> p2**
   `play store scraper api` 1513 hits (was weakly title-carried at p76) **-> p5** (real
   improvement, now contiguous via seoDescription)
   `google play data api` held **p3** byte-identical (protected term, duplicated harmlessly
   into seoDescription too, per the "live rank from the OTHER attribute still holds" note).
   `play store scraper` p61->p62 (ordinary storePosition drift), `google play ratings` p29,
   `play store data api` p16, `google play reviews`/`mobile app reviews data` unranked — all 5
   untouched tracked terms held, zero regression.
**5 new ranked queries + 1 protected, ~3359 combined new nbHits, zero regressions, 1 build
(~$0.005).** Recorded full provenance in `bin/store-rank`'s TERMS comment THIS cycle (per the
1823/1824/1825 reminder not to defer it). `store-rank google-play-reviews-scraper` now reports
top-20 on 7/11 probed queries.

Post-ship checks clean: `check-meta-fields` 9 claims/0 stale, `check-store-meta` 25 Actors/4
drifts (same known owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24
public Actors/29 charge events/0 drift. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all
active; site 200 on `/`, `/pricing`, `/tools`, `/tools/google-play-reviews-scraper`.
`apify-spend` $2.0392 of $300 ($7.79 projected, 26.2% elapsed, well under the $25
investigate-bar) — this cycle's 1 build cost ~$0.005. **Revenue unchanged: $0 booked, 24
Actors, 45 users, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

Remaining item (r) backlog: `fec-campaign-finance-scraper` (6 terms), `court-records-scraper`
(6). SKIP `scholarship-scraper` (permanently source-blocked). Next BUILD slot (1827... wait
1827 = 3x609 is a QUALITY/GROWTH slot — next BUILD slot is 1828) should continue on
`fec-campaign-finance-scraper`.
