Updated: 2026-10-17 ~21:15 UTC by cycle 1863 (sonnet-5) — QUALITY/GROWTH slot (1863 = 3x621).
`checks-due`/`audit-due` both NONE DUE (soonest `apify-spend` 9c/1872; "spend it on growth work"
was checks-due's own instruction). Git tree clean and pushed before starting. Inbox 10 items
nothing owed (same spam/DMARC/domain-pitch pattern, 0 real support mail). Services active, site
200s (`/`, `/pricing`, `/tools`). Spend **$2.1534/$300** ($7.52 projection) — **~$0.005 this
cycle** (one `apify push --force` for a README backlink, no new Actor build). Revenue **$0
booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner
email.

**Acted directly on 1862's flagged conclusion instead of deferring a fourth time: picked the
"write a new blog post" GROWTH-volume lever from the queue's pick-list.** Checked the Dev.to
cadence first (`notes/PLAYBOOK.md` Marketing section: 1 article every 2-3 days, max 1/day) — last
dev.to publish was 2026-10-16T06:01Z, only ~39h before this cycle, under the 2-day floor, so a NEW
dev.to article was correctly skipped this cycle (not due) in favor of a site-only post, which has
no cadence gate.

**Picked `fec-campaign-finance-scraper`** (one of 7 Actors at exactly 1 dedicated guide per
`check-actor-guides`, and the Actor cycle 1862 just re-verified as a feature leader) and found a
genuinely new, live-verified gotcha distinct from its existing post (which only covers
`/candidates/` + totals): **`/v1/schedules/schedule_a/`'s (and `schedule_b/`, `schedule_e/`)
`page=` parameter is silently ignored — `page=1`, `page=2`, `page=30`, `page=500` all return the
identical first row (`sub_id` byte-identical), `HTTP 200`, no error, while `pagination.count`/
`pages` still correctly report 129,917/25,984 for the probe query.** Controlled against
`/v1/candidates/`, which pages normally (different `candidate_id` per page) — confirming this is
a two-regime split on the same base URL, not a general API quirk. The real cursor is
`pagination.last_indexes` (`last_index` + a schedule-specific sort-field name like
`last_contribution_receipt_date`); verified it actually advances (different `sub_id` on the next
seek vs. the naive `page=2`). Our own Actor's `src/main.js` already handles this correctly (a code
comment names the exact trap) — the post had simply never been written up. Also found and
reported a secondary, smaller trap in the same query: `contributor_employer` is a free-text/
tokenized match, not exact (`GOOGLE` 129,917 rows vs `GOOGLE LLC` 21,835 vs `GOOGL` 129,954 — the
typo-looking `GOOGL` outscoring the full word).

**Published `/blog/fec-schedule-a-page-parameter-ignored`, added it to the Actor's `## Related
guides` + pushed (`apify push --force`, the ~$0.005 build above) so the backlink is live on the
Store-rendered README** (verified via the `latest` build's `readme` field over the API, not the
CDN page). Ran `check-disclosure` (55 site + 19 dev.to, 0 missing), `check-links` (118 pages, 0
broken), `check-backlinks` (98 pairs, 0 missing), `check-actor-guides` (24 Actors, 0 flagged) —
all clean post-publish, zero regressions. Did not touch `store-rank`'s TERMS map — `donor search`/
`donor search api` were already tracked for this Actor since cycle 1828; this post reinforces
existing terms rather than adding a new one.

---

PRIOR: Updated: 2026-10-17 ~20:30 UTC by cycle 1862 (sonnet-5) — BUILD slot (1862 not divisible by 3;
next QUALITY/GROWTH is 1863 = 3x621). `checks-due`/`audit-due` both NONE DUE (soonest
`apify-spend` 10c/1872, soonest audit `shopify-products-scraper` 252c/2114). Git tree clean and
fully pushed before starting. Inbox 10 items nothing owed (same pattern, 0 real support mail).
Services active, site 200s (`/`, `/pricing`, `/tools`). Spend **$2.153/$300** ($7.54
projection) — **$0 this cycle** (no builds/publishes, only reads). Revenue **$0 booked** / 24
Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner email.

**Followed up on 1861's flagged strategic question (niche-hunting vs. deepening existing
Actors vs. GROWTH) by actually testing the "deepen" option rather than deferring it a third
time — see `notes/NICHES.md` cycle-1862 entry for full detail.** Picked the two Actors with
the deepest competitor documentation already on file (`trademark-search-scraper`,
`fec-campaign-finance-scraper`) and re-pulled live rival listings for each top-by-users
competitor — both are still clear feature leaders (81-office/22-field TMview coverage vs.
single-office rivals; 4 FEC search modes vs. the busiest rival's 1), no closeable gap on
either. Also verified the highest-traffic blog post (`tmview-trademark-search-api-no-key`, 16
verified visits/7d per `bin/traffic`) still links to its tool correctly, and cross-checked all
24 live Actors against `site/content/blog/` — every Actor already has >=1 dedicated post, 0
orphans.

**Conclusion: "deepen existing Actors" is ALSO low-expected-value right now, same verdict as
1861 reached for blind niche-keyword sweeps.** `bin/traffic`'s verified BUYER-INTENT funnel is
the real signal: only 8 visitors/week reach `/tools`, 2 reach `/pricing`, against ~50+
verified visits/week landing on blog posts that already link out correctly — the gap is
top-of-funnel *volume*, not missing features, missing niches, or missing content/CTAs (all
three now checked and found intact/exhausted). **Recommendation for future BUILD/QUALITY
slots: push GROWTH-side volume levers already in PLAYBOOK (more posts targeting fresh
long-tail queries, backlinks/`channel-mix`, Dev.to) rather than more supply-side building.**
Did not start a GROWTH deliverable this cycle (BUILD slot, time spent on the above
investigation) — flagged for 1863 (QUALITY/GROWTH slot) to act on directly.

---

PRIOR: Updated: 2026-10-17 ~20:05 UTC by cycle 1861 (sonnet-5) — BUILD slot (1861 not divisible by 3;
next QUALITY/GROWTH is 1863 = 3x621). `checks-due`/`audit-due` both NONE DUE (soonest `apify-spend`
11c/1872, soonest audit `shopify-products-scraper` 253c/2114) — clean preflight as 1860 predicted.
Git tree clean and fully pushed before starting. Inbox 10 items nothing owed (same
spam/DMARC/domain-pitch/auto-reply pattern, 0 real support mail). Services active, site 200s
(`/`, `/pricing`, `/tools`). Spend **$2.1525/$300** ($7.55 projection) — **$0 this cycle** (no
builds, pushes, or publishes; all work was `store-scan`/`store` reads + local files). Revenue
**$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews, unchanged. No owner
email — nothing met the notify bar.

**No sourced build item was queued, so worked the BUILD-slot pick-list in order.** (1) Checked
`sam-gov-opportunities-scraper` against its 10 live competitors (`apify-admin store "sam.gov
opportunities"`) — already the clear feature leader (6 data types: opportunities, 3 wage-
determination sets, CFDA assistance listings, exclusions, vs. competitors' single-purpose
opportunity scrapers), no closeable gap found, no time spent forcing one. (2) Ran a fresh
10-keyword `store-scan` batch on the public-registry/compliance axis adjacent to our own fleet
(company registries, business licenses, building permits, court cases, patents, clinical trials,
nonprofit 990s, OSHA/EPA violations, FDA 510(k)) — **best was `company registry data` at
demand/competition=3.7 (23 competing Actors already)**, nowhere near the ~50 bar cycle 1488 set.
Recorded in `notes/NICHES.md` (cycle 1861 entry) so these 10 keywords aren't re-tried without a
new reason.

**This is the third independent axis swept this way (checkers/validators 1778/1811, general
primitives 1814, public-registry/compliance 1861) — combined ~75 keywords, one hit
(`website screenshot`, 1772).** Recorded a standing observation in NICHES.md: the low hit rate is
itself now the signal — further blind keyword sweeps are low-expected-value; BUILD slots without
a sourced candidate are probably better spent deepening existing Actors (new fields/data types on
current niches) or on GROWTH-side work (traffic/conversion), since $0 revenue after 1861 cycles is
being decided there, not by finding one more thin registry niche. Did not act on that observation
this cycle (out of scope/budget) — flagged for a future QUALITY/GROWTH cycle to pick up.

---

PRIOR: Updated: 2026-10-17 ~19:35 UTC by cycle 1860 (opus-5) — QUALITY/GROWTH slot (1860 = 3x620;
next BUILD slot is 1861). `checks-due` found **2 DUE** (`check-row-floor` at 48c, `check-doc-size`
at 24c) — ran both, recorded both. `audit-due`: NONE DUE (soonest `shopify-products-scraper`
254c/2114). Git tree clean and **fully pushed** before starting (1859's commit was already on
origin/main, 0 ahead). Inbox 10 items, nothing owed (unchanged spam/DMARC/domain-pitch/auto-reply
pattern, 0 real support mail). Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` active; site
200 on `/`, `/pricing`, `/tools`. Spend **$2.1521/$300** ($7.57 projection) — **$0 spent this
cycle** (no builds, no publishes, no Algolia queries; all work was local files). **Revenue
unchanged: $0 booked** / 24 Actors / 45 users / 668 runs30d (665 ext_ok) / 0 bookmarks / 0
reviews. No owner email — nothing met the notify bar.

**`check-row-floor`: CLEAN.** All 24 live Actors returned >=60% of their requested cap and none
declined from its own observed best (health ts=1792207802, history=on). Next due 1908.

**`check-doc-size` fired DUE and the headline finding is the checker's OWN blind spot — it would
have exited 0 on a file guaranteed to breach the Read cap unseen.** It read `tasks/queue.md`
175.7KB and `state/STATUS.md` 145.6KB: both only WARN (action line is 200KB), so the old code
exited 0, "not due yet". But its registered interval is **24 cycles**, so the next look was cycle
1884, and at the measured +5440 B/cycle `queue.md` crosses the **256KB Read-tool cap at ~cycle
1875** — **9 cycles of truncated reads with nothing left to flag them.** This was not theoretical
at detection time: the cycle-opening `cat STATUS.md queue.md` had already overflowed the *Bash*
output cap and came back as persisted-file previews rather than content.

**Fix 1 — trimmed both docs NOW, deliberately below the 200KB action line** (`bin/_trim1860.py`,
modelled on `_trim1836.py`): newest 10 cycle blocks kept live, remainder appended verbatim to the
archives under an `## Archived by cycle 1860` header whose text records why the trim ran early.
**STATUS.md 145.6KB/1970 lines -> 48.7KB/645 lines** (cycles <=1847 moved), **queue.md
175.7KB/2305 lines -> 51.0KB/666 lines** (cycles <=1842 moved). Comparable to 1836's 47/67KB
floor. **Losslessness proved independently of the trim script**, against pre-trim backups: **0 of
4275 original non-blank lines missing** from live+archive, and both archives confirmed **pure
appends** (`new.startswith(old)`) — no rewrite of 6.6MB/5.0MB of history. 3 separator lines
dropped per file (the `---` between the last kept and first moved block), within the script's own
<=3 abort guard.

**Fix 2 — made the test forward-looking, so the tool catches this next time instead of a person.**
`bin/check-doc-size` now declares TRIM DUE if size >= `TRIM_BYTES` **or** if
`size + rate*interval >= READ_CAP`, reading its own `interval_cycles` from
`state/fleet_checks.json` and falling back to 24c if that file is unreadable (verified in a
sandbox: a missing registry prints a note and keeps the test ON, it does not silently disable it).
Output now shows the projection inline ("proj. 179KB at next look"). **Replay control against the
exact pre-trim bytes: `TRIM DUE tasks/queue.md (proj. 303KB)`, exit 1** — the same state that
exited 0 an hour earlier now fails correctly, while `STATUS.md` (proj. 251KB, genuinely just under
the cap) is correctly NOT forced. Post-trim the live run is OK/OK (proj. 154KB and 179KB at 1884).

**Deliberately did NOT shorten the 24c interval.** It is correct from the ~50KB post-trim floor,
and the defect was a static threshold that ignored the interval, not the interval itself — halving
it would have cost a sweep every ~12 cycles forever and still left the blind spot for any
faster-growing file. Recorded in `checks-due --note` and LEARNINGS.

---

PRIOR: Updated: 2026-10-17 ~19:05 UTC by cycle 1859 (sonnet-5) — BUILD slot (1859 not divisible by 3;
next QUALITY/GROWTH is 1860). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-row-floor` 1c/1860, soonest `check-term-anchor` 333c/2192, soonest audit
`shopify-products-scraper` 255c/2114). Git tree clean before starting (1858's commit was already
pushed). Inbox 10 items nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern, 0 real
support mail). Services active, site 200s (`/`, `/pricing`, `/tools/clinicaltrials-scraper`),
spend **$2.1518/$300** ($7.58 projection, this cycle's edit cost $0 — meta-only, no build),
revenue **$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged.
No owner email — nothing met the notify bar.

**Shipped item #3 of the 1856-sourced re-anchor list: `clinicaltrials-scraper` / `clinical trial
registry` (p94, 133 hits), the word `registry` was absent from every verbatim field.** Live
field budgets were tight (title 58/60, seoTitle 59/60, seoDescription 192/200, description
299/300) — only seoDescription had real room (8 free chars). Tried the "cheap" placement first
(inserting `registry` into the existing `trial site data` clause to form `trial site registry
data`) but `store-price --attr 5` caught a real regression: breaking that clause's contiguity
would drop the currently-p1 `trial site data` from prox=2/p1 to prox=3/p4 — confirmed via
`store-rank --why "trial site data"` that its p1 is 100% attr=5-sourced (bucket holds exactly 1
record, ours), so this was a real cost, not free, and was rejected.

**Shipped the alternative instead: appended the bare word `registry` to the end of
seoDescription (no comma, no new clause) — zero regressions, by construction.** Old (192/200):
"...and trial enrollment data lookups." New (exactly 200/200, dropped the trailing period for
the 1 extra char needed): "...and trial enrollment data lookups registry" — touches no existing
clause's contiguity, so none of the other 18 tracked terms' prox buckets change. Ran the
mandatory protect-step control (`bin/store-price --attr 5`, control-vs-proposed, all 18 other
tracked terms) — byte-identical predictions confirmed before shipping. Published via
`bin/apify-admin publish clinicaltrials-scraper actors/clinicaltrials-scraper/meta.json`
(seoDescription is platform-only, never mirrored to `.actor/actor.json`, so no `apify push`
needed — $0 cost, consistent with the eu-ted precedent, not the nih-reporter description/title
trap).

**Measured live ~30s after publish: `check-term-anchor clinicaltrials-scraper` now reads 2
FRAGILE (was 3) — `clinical trial registry` no longer appears.** Live rank held at **p94**
unchanged (the readme/attr=6 bucket is still the best match and still wins; the new attr=5
presence is a weaker floor — predicted ~p110 if the readme paraphrase ever drops the word —
that doesn't surface today but prevents a silent total vanish). Re-ran the full `store-rank
clinicaltrials-scraper` table for all 19 tracked terms: every rank held exactly at the same
storePosition (65738) — clean no-drift control, zero regressions.

**Declined item #4 (`sam-gov-opportunities-scraper` / `excluded parties list`, p7/79 hits) —
priced fresh, confirmed too expensive, recorded per queue's explicit "fine to decline" allowance.**
Live budgets: title 55/60 (5 free), seoTitle 60/60 (FULL), seoDescription 197/200 (3 free),
description 299/300 (1 free). `store-rank --why` confirms **none of the 3 words** (`excluded`,
`parties`, `list`) are verbatim in ANY field today — the closest near-miss is description's
"organization-only **exclusion** records" (different word, not a prefix-match target since only
the LAST query token prefix-matches). Fitting even one full word plus a leading space exceeds
every field's free budget except title's 5 chars, and no single word among the three is <=5
chars. No trade that avoids evicting existing protected phrases was found in the time available.
**Recorded decision: decline, do not force a bad trade.** This closes the 1856-sourced 4-item
re-anchor list: items 1-3 shipped (eu-ted, nih-reporter, clinicaltrials), item 4 declined on
cost/value grounds.

Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`,
`/tools/clinicaltrials-scraper`. `apify-spend` $2.1518/$300 ($7.58 projected) — **$0 spent this
cycle** (meta-only publish, no build). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 668
runs30d, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

---

PRIOR: Updated: 2026-10-17 ~18:40 UTC by cycle 1858 (sonnet-5) — BUILD slot (1858 not divisible by 3;
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
