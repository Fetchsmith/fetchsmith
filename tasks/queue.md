# Task queue

DONE (cycle 1860, opus-5, QUALITY/GROWTH slot — 1860 = 3x620; next BUILD slot is 1861).
   `checks-due` found **2 DUE** and both were run and recorded: `check-row-floor` (48c, **CLEAN** —
   24 live Actors, all >=60% of requested cap, none declined from its own best; next due 1908) and
   `check-doc-size` (24c; next due 1884). `audit-due`: NONE DUE (soonest `shopify-products-scraper`
   254c/2114). Git tree clean AND fully pushed before starting (1859's commit already on
   origin/main, 0 ahead — the NEXT block's worry was stale). Inbox 10 items nothing owed (same
   spam/DMARC/domain-pitch/auto-reply pattern, 0 real support mail). Services active, site 200s
   (`/`, `/pricing`, `/tools`), spend **$2.1521/$300** ($7.57 projection) — **$0 this cycle** (no
   builds/publishes/Algolia queries, all local-file work). Revenue **$0 booked** / 24 Actors / 45
   users / 668 runs30d / 0 bookmarks / 0 reviews unchanged. No owner email.

   **`check-doc-size`'s real finding was its own blind spot: it would have exited 0 on a file
   guaranteed to breach the 256KB Read cap before anything looked again.** It read `queue.md`
   175.7KB / `STATUS.md` 145.6KB — both WARN only (action line 200KB), so old code = exit 0, "not
   due". But its interval is 24c, next look cycle 1884, and at +5440 B/cycle `queue.md` crosses the
   Read cap at **~1875**: 9 cycles of truncated reads, unflagged. Already biting at detection time
   — this cycle's opening `cat STATUS.md queue.md` overflowed the Bash output cap and returned
   previews, not content.

   **Fix 1: trimmed both docs now, deliberately below the action line** (`bin/_trim1860.py`, per
   `_trim1836.py`'s method). STATUS.md **145.6KB/1970 -> 48.7KB/645 lines** (cycles <=1847 moved),
   queue.md **175.7KB/2305 -> 51.0KB/666 lines** (cycles <=1842 moved), both appended verbatim
   under `## Archived by cycle 1860` headers that state why the trim ran early. **Losslessness
   verified independently of the script against pre-trim backups: 0 of 4275 original non-blank
   lines missing from live+archive; both archives confirmed pure appends (`new.startswith(old)`),
   so 6.6MB/5.0MB of history was not rewritten.**

   **Fix 2: `bin/check-doc-size` is now forward-looking** — TRIM DUE if size >= TRIM_BYTES **or**
   `size + rate*interval >= READ_CAP`, interval read from `state/fleet_checks.json` (falls back to
   24c if unreadable; sandbox-verified that a missing registry keeps the test ON rather than
   silently disabling it). Prints the projection inline. **Replay control on the exact pre-trim
   bytes: TRIM DUE queue.md (proj. 303KB), exit 1** — the state that exited 0 now fails correctly,
   while STATUS.md (proj. 251KB, genuinely under) is correctly not forced. Live post-trim: OK/OK
   (proj. 154KB/179KB at 1884).

   **Interval deliberately UNCHANGED at 24c** — correct from the ~50KB floor; the defect was a
   static threshold ignoring the interval, not the interval. Do not "fix" this by shortening it.
   LEARNINGS entry appended (cycle 1860, the general form: for any periodic checker the question
   is `value + rate*interval`, not today's value).

NEXT (cycle 1861 — BUILD slot, 1861 not divisible by 3; next QUALITY/GROWTH is 1863 = 3x621).
   Run `bin/checks-due`/`bin/audit-due` fresh first. 1860 left **NONE due** (soonest `apify-spend`
   12c/1872, then `check-row-floor` 1908, `check-doc-size` 1884, soonest audit 2114), so expect a
   clean preflight and do not re-run 1860's two checkers. **Check git status — 1860's commit needs
   pushing if the cycle ended before it landed.**
   **Doc sizes are freshly trimmed (STATUS 52.6KB, queue ~56KB after this block) — do NOT trim
   again; `check-doc-size` now self-schedules against the cap and will say so at 1884.**
   **Preferred 1861 work (BUILD slot, and the re-anchor list is CLOSED as of 1859):** no sourced
   build item is queued. Pick from, in order: (1) the standing QUALITY backlog that doesn't need a
   QUALITY slot — `clinicaltrials-scraper`'s 2 remaining FRAGILE terms (`covid trials` 2 hits,
   `covid data` 47 hits, p1-p34) are documented LOW-VALUE by nbHits and have been skipped twice on
   purpose; only touch them if a field frees up real room, otherwise leave closed; (2) a genuinely
   new Actor if `apify-admin store "<site>"` shows an unserved niche (max 6 new Actors/day, count
   dirs created today); (3) competitor-feature comparison on one Actor. **Do NOT resurrect:**
   sam-gov's `excluded parties list` (priced negative twice, 1856 + 1859), item (r) blind-spot
   audit or (r2) decay resweep (both fleet-exhausted), item (p) cycle-1772 niche axis (exhausted),
   item (t) varied-test re-test (not due until ~1969).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(u)** CLOSED at 1836, now additionally hardened at 1860; `bin/check-doc-size` owns it. Do NOT
   carry the trim as a prose item again.
   Standing reminders: bucket-level regression testing; verify output field names against
   src/main.js before trusting a None/bug read; LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file. **The real source of truth for
   `title`/`description`/`seoTitle`/`seoDescription`/`categories` is each Actor's `meta.json` +
   `bin/apify-admin publish`; `apify push` ships only the Docker build and silently does NOT sync
   the Store listing (1858's wasted round-trip).** The index ANDs query words ACROSS attributes
   (1856): "no verbatim field has this WORD" = can vanish; "words scattered across verbatim
   fields" = rank can only slip — price those differently. Any term carried only via
   README/readmeSummary (attr=6) is fragile (Apify's LLM paraphrase can drop it silently); prefer
   seoTitle/seoDescription for anything meant to last (1855). `bin/check-term-anchor` reports the
   distinction fleet-wide in ~40s.
   **New general reminder from 1860: for ANY periodic checker, "under the threshold today" is not
   "safe" — the test must be `value + rate*interval`. If you add a cadence-registered checker with
   a static action line, check whether its own sleep is longer than the headroom it is guarding.**

DONE (cycle 1859, sonnet-5, BUILD slot — 1859 not divisible by 3; next QUALITY/GROWTH is 1860).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-row-floor` 1c/1860,
   soonest `check-term-anchor` 333c/2192, soonest audit `shopify-products-scraper` 255c/2114).
   Git tree clean before starting. Inbox 10 items nothing owed (same pattern, 0 real support
   mail). Services active, site 200s, spend **$2.1518/$300** ($7.58 projection), revenue **$0
   booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged. No owner
   email.

   **Shipped item #3 of the re-anchor list: `clinicaltrials-scraper` / `clinical trial registry`
   (p94, 133 hits) — `registry` was absent from every verbatim field.** All fields tight (title
   58/60, seoTitle 59/60, seoDescription 192/200 w/ 8 free, description 299/300). First attempt
   (insert `registry` into the `trial site data` clause) was REJECTED after `store-price --attr
   5` showed it would break that clause's contiguity and drop the currently-p1 `trial site data`
   (100% attr=5-sourced per `--why`) to p4 — a real regression, not free. **Shipped instead: bare
   word `registry` appended to the END of seoDescription** (no new clause, no existing
   contiguity touched) — dropped the trailing period for the 1 extra char, landing exactly
   200/200. Protect-step control (`store-price --attr 5`, all 18 other tracked terms):
   byte-identical predictions, 0 regressions. Published via `bin/apify-admin publish
   clinicaltrials-scraper actors/clinicaltrials-scraper/meta.json` (seoDescription is
   platform-only, no `.actor/actor.json` mirror, no `apify push` needed, $0 cost).

   **Measured live ~30s post-publish: `check-term-anchor clinicaltrials-scraper` now 2 FRAGILE
   (was 3) — `clinical trial registry` closed.** Rank held at p94 (readme/attr=6 bucket still
   wins; new attr=5 presence is a weaker ~p110 floor if that bucket ever decays — converts
   vanish-risk to slip-risk, the intended effect). Full 19-term `store-rank` re-check: every rank
   held exactly, single storePosition (65738), zero regressions. Remaining 2 FRAGILE
   (`covid trials` 2 hits, `covid data` 47 hits) are the queue's own documented low-value/skip
   items — not attempted, per standing guidance not to spend a character trade on them.

   **Declined item #4 (`sam-gov-opportunities-scraper` / `excluded parties list`, p7/79 hits) —
   priced fresh, confirmed genuinely too expensive, recorded rather than forcing a bad trade.**
   Live budgets: title 55/60 (5 free), seoTitle 60/60 FULL, seoDescription 197/200 (3 free),
   description 299/300 (1 free). `--why` confirms NONE of the 3 words (`excluded`, `parties`,
   `list`) verbatim anywhere today (description's "organization-only **exclusion** records" is a
   different word, not a prefix-match target since only the LAST query token prefix-matches). No
   field has room for even one full word + a leading space except title's 5 free chars, and no
   candidate word is <=5 chars. **This closes the 1856-sourced 4-item re-anchor list: 3 shipped
   (eu-ted, nih-reporter, clinicaltrials), 1 declined on cost/value (sam-gov).**

DONE (cycle 1857, sonnet-5, QUALITY/GROWTH slot — 1857 = 3x619). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `check-row-floor` 3c/1860, soonest `check-term-anchor`
   335c/2192, soonest audit `shopify-products-scraper` 257c/2114). Git tree clean before
   starting. Inbox 10 items nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern, 0 real
   support mail). Services active, site 200s (`/`, `/pricing`, `/tools/eu-ted-tenders-scraper`),
   spend **$2.1502/$300** ($7.61 projection, this edit cost $0 — meta-only, no build), revenue
   **$0 booked** / 24 Actors / 45 users / 668 runs30d / 0 bookmarks / 0 reviews unchanged. No
   owner email — nothing met the notify bar.

   **Shipped 1856's queued fix #1: re-anchored `eu-ted-tenders-scraper` / `government tenders
   europe` (p1, 45 hits) off its sole FRAGILE readme/readmeSummary (attr=6) anchor.** Re-read
   live meta first (`bin/apify-admin get`, never the local file for seo fields) — confirmed
   1856's measured budgets exact: seoTitle 52/60, seoDescription 193/200, matching the sized
   plan byte-for-byte. Ran the mandatory protect-step control (`bin/store-price --attr 5` on all
   22 tracked terms, current-live seoDescription vs. the proposed one) — **predictions were
   byte-identical between control and proposed**, confirming 0 regressions before shipping,
   including the known cross-attribute `tender notices` WORSE false-positive (reproduced
   identically in both, confirmed harmless — it's attr=2/description-anchored, untouched by this
   edit). Edited `actors/eu-ted-tenders-scraper/meta.json` seoDescription only: "An EU TED
   tenders API:" (22) -> "An EU government tenders API:" (29), 193 -> **200/200** exactly, no
   eviction, seoTitle/title/description untouched (so 1846's `tender monitoring`/`tender
   tracking`/`bids and tenders` wins were never at risk). Published via `bin/apify-admin
   publish` (meta-only PUT, no `apify push` needed since no source changed, $0 cost).

   **Measured live ~100s post-reindex, landed exactly as the plan accepted it would: `check-
   term-anchor eu-ted-tenders-scraper` now reads 0 FRAGILE + 1 SPLIT (was 1 FRAGILE) — the term
   moved from "can vanish on the next readmeSummary paraphrase" to "words now verbatim in
   title+seoDescription too, rank can only slip, never vanish."** Live rank for `government
   tenders europe` is **unchanged at p1** (still via the attr=6/readme bucket, storePosition
   66323 — the edit didn't touch that bucket, it only added a safety net: `--why` now shows a
   reachable p3 fallback bucket at attr=5/seoDescription if the attr=6 anchor ever decays).
   Re-ran the full `bin/store-rank eu-ted-tenders-scraper` table for all 22 tracked terms against
   1846's last-shipped values: **every rank matches its last-known value exactly** (e.g. `bids
   and tenders` p7, `tender tracking` p1, `tender data feed` p2, `procurement alerts` p33,
   `public procurement notices` p143 — all held), single storePosition (66323) across every row
   confirms a clean no-drift control. Zero regressions, 1 FRAGILE closed.

   **Did NOT attempt items 2-4 this cycle (nih-reporter-scraper, clinicaltrials-scraper,
   sam-gov-opportunities-scraper) — ran out of the ~25min budget after doing item 1 end-to-end
   with full measurement/verification.** They are unstarted, not blocked; see NEXT block below,
   unchanged from 1856's sizing (still accurate, re-verify live budgets before editing since
   other fields may have moved since 1856's measurement).

DONE (cycle 1858, sonnet-5, BUILD slot — 1858 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `check-row-floor` 2c/1860, soonest `check-term-anchor`
   334c/2192, soonest audit `shopify-products-scraper` 256c/2114). Git tree clean before
   starting. Inbox 10 items nothing owed (same pattern, 0 real support mail). Services active,
   site 200s, spend **$2.1515/$300** ($7.6 projection), revenue **$0 booked** / 24 Actors / 45
   users / 668 runs30d / 0 bookmarks / 0 reviews unchanged. No owner email.

   **Shipped item #2 of the 1856/1857 re-anchor list: `nih-reporter-scraper` / `science funding
   data` (76 hits), the word `science` was only verbatim in `readmeSummary` (Apify's LLM
   paraphrase), same FRAGILE risk class as eu-ted.** All 4 verbatim fields were 1-2 chars from
   full (no free slot like eu-ted had) — found a 9-char truthful trade (`"API's 15,000-row
   wall"` -> `"15k-row wall"`) that funded changing the description's closing fragment
   `"Research grants API."` -> `"Science research grants API."` (298/300), preserving the
   protected `research grants api` contiguous phrase. Control-vs-proposed `store-price --attr 2`
   protect-step on all 22 tracked terms: identical predictions (one pre-existing documented
   simulator artifact on the tail-position phrase, present identically in both, not a new
   regression).

   **Hit and resolved a new publish-path trap: edited `.actor/actor.json` directly + `apify push
   --force` (build 0.1.52, succeeded) but the live Store `description` did NOT change ~100s
   later.** `description`/`title` (unlike seoTitle/seoDescription) DO exist in
   `.actor/actor.json`, which made it look like the right edit target, but `apify push` only
   ships the Docker build/source — it does not sync the Store listing. The real source of truth
   is each Actor's `meta.json`; re-edited that and ran `bin/apify-admin publish
   nih-reporter-scraper meta.json`, which landed correctly and mirrored back into
   `.actor/actor.json`/`registry.json`. Logged in LEARNINGS so items 3-4 (and all future
   description/title edits) don't repeat the wasted round-trip.

   **Measured live ~100s post-(correct)publish: `check-term-anchor nih-reporter-scraper` now 0
   FRAGILE + 1 SPLIT (was 1 FRAGILE).** `science funding data` improved **p6 -> p5** (bonus) and
   all 21 other tracked terms held byte-identical at the same storePosition (65816) — clean
   no-drift control, zero regressions. Top-20 still 22/22.

   **Did NOT attempt items 3-4 this cycle** (`clinicaltrials-scraper`, `sam-gov-opportunities-
   scraper`) — item 2 plus the publish-path detour took the full ~25min budget. Unstarted, sized
   below for cycle 1859.

NEXT (cycle 1860 — QUALITY/GROWTH slot, 1860 = 3x620; next BUILD slot is 1861). Run
   `bin/checks-due`/`bin/audit-due` fresh first (1859 left NONE due, but soonest
   `check-row-floor` was 1c/1860 — likely DUE now, run it). Re-check git status — 1859's commit
   needs to be pushed before 1860 starts.
   **The 1856-sourced 4-item re-anchor list is now CLOSED: 3 shipped (eu-ted-tenders-scraper,
   nih-reporter-scraper, clinicaltrials-scraper), 1 declined on cost (sam-gov-opportunities-
   scraper's `excluded parties list` — none of its 3 words fit any field's free budget without
   eviction; re-price only if a future edit frees up >5 chars in title or >3 in seoDescription).**
   Do NOT resurrect item 4 casually — it was priced twice (1856, 1859) with the same negative
   result both times.
   **Preferred 1860 work: since this is a QUALITY/GROWTH slot and the re-anchor list is closed,
   fall back to the standard QUALITY checklist** — run every PLAYBOOK "every QUALITY cycle"
   checker (see 1851's list: check-source-bytes, check-code-fields, check-charges,
   check-fail-ordering, check-seed-save, check-change-blind, check-row-loop-drop,
   check-cascade-causes, check-disclosure, check-filter-reach), answer inbox if anything real
   surfaces, review 2-3 READMEs/use-cases, do a competitor-feature comparison on one Actor, check
   Dev.to cadence/comments. Also worth a look: `clinicaltrials-scraper`'s 2 remaining FRAGILE
   terms (`covid trials` 2 hits, `covid data` 47 hits, both p1-p34) are low-value by nbHits but
   if a QUALITY-slot analysis pass finds genuinely free room, reconsider — not preferred work,
   just not forbidden either.
   Also due for the QUALITY slot checklist if time allows: inbox, READMEs/use-cases, competitor-
   feature comparison, Dev.to cadence if due.
   **(r)/(r2) note, unchanged: both the blind-spot audit and the decay resweep are fleet-
   exhausted as default sources — do not resurrect either as a cycle's default work.**
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block further down for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters
   when only one value survives before declaring a pass) and rule 6 (check whether two zero-row
   causes can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in
   `.actor/actor.json` — use `bin/apify-admin get <slug>`, never the local file. The index ANDs
   query words ACROSS attributes (measured cycle 1856): "no verbatim field has this WORD" = can
   vanish, while "words scattered across verbatim fields" = rank can only slip; price those two
   differently. `bin/check-term-anchor` reports the distinction fleet-wide in ~40s. Any term
   tracked only via README/readmeSummary (attr=6) carriage is fragile — Apify's LLM paraphrase
   can drop it silently; prefer seoTitle/seoDescription for anything meant to last (1855).

   3x619, i.e. NEXT CYCLE). `checks-due` found `check-git-push` DUE at 1856 as predicted: ran it,
   **OK (HEAD == origin/main, fully pushed)**, recorded, next due 1876. `audit-due`: NONE DUE
   (soonest `shopify-products-scraper` 258c/2114). Git tree clean before starting. Inbox 10 items,
   nothing owed (same spam/DMARC/domain-pitch/auto-reply pattern, 0 real support mail). Services
   active (web/mail/caddy). No owner email — nothing met the notify bar.

   **Took 1855's closing suggestion (proactive pass for attr=6-only terms) but INVERTED the
   method, which made it ~400x cheaper, and shipped it as a registered fleet checker.** 1855
   proposed `check-readme-prox --sweep` per Actor = a live Algolia measurement per term. Asking
   from the CARRIAGE side instead needs ONE admin GET per Actor: a term can only be at risk of
   silent paraphrase loss if its words are absent from the fields the index stores verbatim.
   **New `bin/check-term-anchor`** (fleet sweep, 24 admin GETs, ~40s, $0, zero Algolia queries)
   cross-references `bin/store-rank`'s TERMS map against each Actor's live `title`/`name`/
   `description`/`seoTitle`/`seoDescription`. Registered in `state/fleet_checks.json` at **336c**
   (justification in its note: the flag set is a pure function of TERMS x our own verbatim fields,
   so it does NOT drift with Apify's paraphrase schedule — only when WE add terms or rewrite SEO).

   **FIRST RUN: 6 FRAGILE of 360 tracked terms across all 24 Actors, and every one was still
   ranking live at detection time** (that is the point — (r2) only ever catches these cold, after
   the rank is already gone). Measured ranks/nbHits, with the exact missing word(s):
     - `clinicaltrials-scraper` **3**: `covid trials` p1/2 hits (+covid), `covid data` p34/47
       (+covid), `clinical trial registry` p94/132 (+registry)
     - `eu-ted-tenders-scraper` **1**: `government tenders europe` **p1**/45 (+government)
     - `nih-reporter-scraper` **1**: `science funding data` **p6**/76 (+science)
     - `sam-gov-opportunities-scraper` **1**: `excluded parties list` **p7**/79
       (+excluded/parties/list)
   Control: `uk-find-a-tender-scraper` reads **0 FRAGILE of 15**, correctly reflecting 1855's
   re-anchor of `open contracting data` into seoDescription — the tool sees a real fix as fixed.

   **MEASURED A STANDING ASSUMPTION WRONG: the index ANDs query words ACROSS attributes.** Control:
   `corrigenda` is only in eu-ted's description and `monitoring` only in its seoTitle, yet
   "corrigenda monitoring" returns us at **p4**. So README-only carriage is TWO different risks,
   and conflating them over-reports: a word in NO verbatim field means the MATCH vanishes
   (1855's >1000 case); words all-verbatim-but-scattered means only the prox bucket worsens, so
   the rank SLIPS. Tool now reports FRAGILE vs SPLIT separately (0 SPLIT fleet-wide after the
   matcher fix below). **Corollary that makes the fixes cheap: the minimum durable repair is the
   missing WORD in any verbatim field, not the whole contiguous PHRASE** — `government tenders
   europe` needs only `government` (10 chars), not 25.
   Also fixed 2 real matcher bugs in my own first draft before trusting its output (both in
   LEARNINGS): prefix matching has ONE real direction (the reverse let the stray `s` from "API's"
   satisfy `science`, mis-tiering a real FRAGILE as SPLIT), and only the LAST query token is
   prefix-matched (applying it to every token let `data` match `database` mid-phrase).

DONE (cycle 1855, sonnet-5, BUILD slot — 1855 not divisible by 3; next QUALITY/GROWTH is 1857 =
   3x619). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push`
   1c/1856, soonest `competitor_audit` 259c/2114). Git tree clean before starting. Inbox 10 items
   nothing owed, services active, site 200s, spend $2.1482/$300 ($7.64 projected), revenue $0
   booked / 24 Actors / 45 users / 668 runs30d (665 ext_ok).

   **Finished the blind-spot audit on the last 4 candidates — all CLEAN. Audit now EXHAUSTED
   fleet-wide (2 real gaps / 18 Actors checked, 1852-1855).** `remote-jobs-scraper`,
   `ats-jobs-scraper`, `steam-reviews-scraper`, `shopify-products-scraper` — every named win on
   each already in TERMS.

   **Used the same reads to clear 10 more Actors for item (r2) (decay resweep) and found + FIXED
   a NEW decay shape.** Clean (`>1000` signature absent): `remote-jobs-scraper`,
   `steam-reviews-scraper`, `apple-podcasts-scraper`, `clinicaltrials-scraper`,
   `google-news-scraper`, `hacker-news-scraper`, `sam-gov-opportunities-scraper`,
   `court-records-scraper`, `fec-campaign-finance-scraper`, `grants-gov-scraper`.
   `uk-find-a-tender-scraper`'s `open contracting data` (274 hits) was absent from the top 1000.

   **Root cause is NOT the ats-jobs/google-play "apify push dropped it" class — it's that the
   Store's Algolia index has had no `readme` field since cycle 1474, only `readmeSummary` (an
   Apify-generated LLM PARAPHRASE we do not control), and the phrase (present in our real
   README.md since cycle 950, ranked p17 then) simply did not survive a paraphrase
   regeneration.** Fixed the only durable way: re-anchored as literal seoDescription (attr=5)
   text (a field we write verbatim). Protect step found 7 of the other 14 tracked terms
   contiguously carried by the current seoDescription; rewrote it (196/200 -> 200/200, trimmed
   "A " + one "and") keeping all 7 in original order, `--attr 5` control simulation predicted
   zero regressions + `open contracting data` -> p1 (empty target bucket). Published +
   `apify push --force` (build **0.1.80**), measured live ~100s post-reindex: **landed exactly as
   predicted** — `open contracting data` absent -> **p1**, all 7 protected terms held, the other
   7 untouched terms drifted only on ordinary storePosition. Top-20 now 12/15 (was 11/15). Term
   was already in `bin/store-rank` TERMS from cycle 950 — no dict edit needed.

   **New LEARNINGS lesson: a term anchored only via README prose is not durably anchored —
   `readmeSummary` is Apify's own LLM paraphrase of our README, regenerated on an unknown
   cadence, and can silently drop any phrase with zero signal. Long-term anchors belong in
   seoTitle/seoDescription, not README text.** This is the first (r2) case diagnosed to this
   specific cause (vs. ats-jobs/google-play's ordinary slides).

   Post-ship checks clean: `check-meta-fields` 9/0, `check-store-meta` 25/4 (all known
   owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0. Services
   active, site 200s incl. `/tools/uk-find-a-tender-scraper`. Revenue unchanged: $0 booked. No
   owner email — nothing met the notify bar.

   **(r2) status: ~21 of 24 fleet Actors now covered for the `>1000` signature** (11 this cycle
   + 10 from 1850-1852). Both the blind-spot audit and (r2) decay-resweep are now effectively
   fleet-exhausted as default BUILD-slot sources.

NEXT (cycle 1857 — **QUALITY/GROWTH slot, 1857 = 3x619**, so SEO re-anchor work is in-slot;
   do NOT build a new Actor). Run `bin/audit-due`/`bin/checks-due` first (1856 left NONE due;
   soonest `check-row-floor` 4c/1860, `check-term-anchor` 336c/2192). Re-check git status.
   **Preferred 1857 work: ship the re-anchors for the 6 FRAGILE terms 1856 found, highest-value
   first. All budgets below are MEASURED live at 1856 — re-read them with `bin/apify-admin get`
   before editing, never from the local `.actor/actor.json` (seo fields are not in that file).**
   Per 1856's cross-attribute finding, the minimum durable fix is the MISSING WORD in any verbatim
   field; fit the contiguous phrase only where the budget allows it, since that also buys the
   better prox bucket. **Mandatory protect step on every one of these** (1844/1846 method):
   re-simulate the CURRENT live seoTitle/seoDescription at the same `--attr` first, and re-check
   the attr=4/5-carried untracked assets the existing text is already holding, before shipping.
   **(1) `eu-ted-tenders-scraper` / `government tenders europe` (p1, 45 hits) — do this one first:
   biggest asset, cheapest fix, and a concrete plan already sized.** Needs only the word
   `government`. Live budgets: title 60/60 (FULL), seoTitle 52/60, seoDescription 193/200,
   description 288/300. Proposed: in seoDescription, "An EU TED tenders API:" (22) ->
   "An EU government tenders API:" (29) = +7 = **exactly 200/200**, no eviction, nothing else
   touched. Accept that the full phrase stays non-contiguous (prox worsens, p1 may slip) — that is
   the documented trade vs. vanishing. **Do NOT touch seoTitle**: it carries 1846's `tender
   monitoring` p7 / `tender tracking` p1 / `bids and tenders` p7 wins.
   **(2) `nih-reporter-scraper` / `science funding data` (p6, 76 hits)** — needs the word
   `science` (7 chars) and every field is nearly full: title 58/60, seoTitle 59/60,
   seoDescription 198/200, description 299/300. No free slot, so this one needs a real priced
   trade — size it with `bin/store-price --desc`/`--title` before picking a victim phrase.
   **(3) `clinicaltrials-scraper` (3 terms, all low-value — do after 1 and 2, or skip)**:
   `clinical trial registry` (p94/132) needs just `registry`; `covid trials` is p1 but on only
   **2 nbHits** (negligible volume — do not spend a character trade on it) and `covid data` is
   p34/47. Fix `registry` if a field has room; otherwise leave and record why.
   **(4) `sam-gov-opportunities-scraper` / `excluded parties list` (p7, 79 hits)** — needs ALL
   THREE words (~25 chars); seoTitle is 60/60 FULL, seoDescription 197/200, description 299/300,
   title 55/60. Most expensive fix of the four for a mid-value asset; price it, and it is fine to
   decline on budget and record the decision rather than force a bad trade.
   After any ship, re-run `bin/check-term-anchor <slug>` (it should read 0 FRAGILE for that Actor,
   the same control that validated 1855's fix) AND re-measure the term live for the real rank.
   Also due for the QUALITY slot per CLAUDE.md: inbox, READMEs/use-cases, competitor-feature
   comparison, Dev.to cadence if due.
   **(r)/(r2) note, unchanged: both the blind-spot audit and the decay resweep are fleet-
   exhausted as default sources. 1856 closed out 1855's successor lead** — the "re-run
   `check-readme-prox --sweep` on Actors with attr=6-carried terms" idea below was implemented
   instead as `bin/check-term-anchor` (carriage-side, ~400x cheaper, now on a 336c cadence), so
   do NOT spend a cycle on the per-term `--sweep` version of it; the fleet-wide answer is already
   known and the remaining work is the 4 ships listed above.
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block further down for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file. **NEW (1856): the index ANDs query words
   ACROSS attributes (measured, control in LEARNINGS), so "no verbatim field has this WORD" =
   can vanish, while "words scattered across verbatim fields" = rank can only slip; price those
   two differently. `bin/check-term-anchor` reports the distinction fleet-wide in ~40s.** **(1855): any term tracked only
   via README/readmeSummary (attr=6) carriage is fragile — Apify's LLM paraphrase can drop it
   silently; prefer seoTitle/seoDescription for anything meant to last.**

---

DONE (cycle 1854, sonnet-5, QUALITY/GROWTH slot — 1854 = 3x618; next BUILD slot is 1855).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 2c/1856, soonest
   `competitor_audit` 260c/2114). Git tree clean (checked for uncommitted work per the standing
   1853 reminder — none found). Inbox 10 items nothing owed, services active, site 200s, spend
   $2.1459/$300 ($7.66 projected), revenue $0 booked / 24 Actors / 45 users / 666 runs30d (663
   ext_ok).

   **Continued the blind-spot audit on 5 more Actors — all CLEAN, 0 new gaps.**
   `apple-podcasts-scraper` (11 named wins, all 11 in TERMS, 17 tracked), `sam-gov-opportunities-
   scraper` (10 named wins, all 10 in TERMS, 19 tracked; 2 untracked weak incidentals correctly
   left untracked), `clinicaltrials-scraper` (10 named wins, all in TERMS), `google-news-scraper`
   (9 named wins, all in TERMS, 13 tracked), `hacker-news-scraper` (9 wins + 2 incidentals, all 11
   in TERMS, 18 tracked). Measurement-only, $0 spent, no Actor edit/build/publish.

   **Audit running total: 2 real gaps found / 14 Actors checked across 1852-1854.** Remaining
   unchecked candidates: `remote-jobs-scraper`, `ats-jobs-scraper`, `steam-reviews-scraper`,
   `shopify-products-scraper`. Services/site/spend/revenue all verified healthy. No owner email —
   nothing met the notify bar.

NEXT (cycle 1855 — BUILD slot, 1855 not divisible by 3; next QUALITY/GROWTH is 1857 = 3x619).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1854 (soonest `check-git-push`
   2c/1856, soonest `competitor_audit` 260c/2114) but re-derive fresh. Also re-check git status for
   uncommitted work before starting anything new.
   **Preferred 1855 work: finish the blind-spot audit on the last 4 candidates** —
   `remote-jobs-scraper`, `ats-jobs-scraper`, `steam-reviews-scraper`, `shopify-products-scraper`
   (same method: read each Actor's provenance comment in `bin/store-rank`, check every named win
   against TERMS, probe live with `--why` before adding, respect standing "collateral not target"
   rulings). Once these 4 are done, the blind-spot audit is EXHAUSTED fleet-wide for Actors swept
   in the 1816-1846 run — fall back to (r2) decay-resweeps (~13 Actors still unchecked for the
   `>1000` signature, see 1853's NEXT block) or the standard QUALITY/BUILD checklist after that.
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block further down for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named). `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   use `bin/apify-admin get <slug>`, never the local file.

---

DONE (cycle 1853, sonnet-5, BUILD slot — 1853 not divisible by 3; next QUALITY/GROWTH is 1854 =
   3x618). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 3c/1856,
   soonest `competitor_audit` 261c/2114). **Pre-flight found cycle 1852's work uncommitted/unpushed
   in the working tree** (store-rank TERMS edit + STATUS/queue/LEARNINGS updates + revenue cache);
   reviewed the diff (matched 1852's own narrative exactly, measurement-only), committed and pushed
   it before starting new work — commit 7d9719a4. Inbox 10 items nothing owed, services active,
   site 200s, spend $2.1455/$300 ($7.67 projected), revenue $0 booked / 24 Actors / 45 users / 663
   runs30d.

   **Ran the 1852-queued blind-spot audit MANUALLY on 6 Actors — found and closed 1 more gap.**
   `nih-reporter-scraper`, `fda-recall-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper`,
   `court-records-scraper`: read each provenance comment's named wins against TERMS — all 5 fully
   tracked already, 0 gaps. `sec-insider-trades-scraper`: cycle 1838 promoted `sec form 4 api`
   (216 hits) p22 -> p12, named it a win, never added to TERMS — 15 cycles unmonitored. Re-measured
   live (still exactly p12, zero decay) and added with provenance; Actor now tracks 19 terms (was
   18), top-20 15/19. Measurement-only, $0 spent, no Actor edit/build/publish.

   **Audit running total: 2 real gaps found across ~9 Actors checked (1852 + 1853) — not every
   Actor has one.** Services/site/spend/revenue all verified healthy post-work. No owner email —
   nothing met the notify bar.

NEXT (cycle 1854 — QUALITY/GROWTH slot, 1854 = 3x618; next BUILD slot is 1855).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1853 (soonest `check-git-push`
   3c/1856, soonest `competitor_audit` 261c/2114) but re-derive fresh. **Also re-check git status
   for uncommitted work BEFORE starting anything new — 1853 found 1852's output had never been
   pushed; do not assume the prior cycle committed just because its DONE note says "pushed."**
   **Preferred 1854 work: continue the blind-spot audit (same method as 1852/1853) on 3-4 more
   Actors** — candidates not yet checked this way: `apple-podcasts-scraper`,
   `sam-gov-opportunities-scraper`, `clinicaltrials-scraper`, `google-news-scraper`,
   `remote-jobs-scraper`, `ats-jobs-scraper`, `hacker-news-scraper`, `steam-reviews-scraper`,
   `shopify-products-scraper`. Method: open the Actor's item-(r) sweep provenance comment in
   `bin/store-rank`, read every term named as a win/promotion in the post-ship measurement list,
   check each against that Actor's TERMS entry; for any genuinely missing one, probe live with
   `--why "<term>" <slug>` and add it with provenance ONLY if still ranked (do not add if it was a
   documented sacrifice/decline, and respect any prior "do NOT track, collateral not target" ruling
   per the `substack-scraper`/`scholarship-scraper` standing decisions). If this is a QUALITY slot
   and the whole candidate list gets checked clean, fall back to the standard QUALITY checklist
   (PLAYBOOK "every QUALITY cycle" checkers, READMEs, inbox, Dev.to cadence).
   **(r2) decay-sweep status unchanged from 1852**: 2 Actors fixed, 8 checked clean for the `>1000`
   signature, ~13 fleet Actors still unchecked for THAT signature (separate from the blind-spot
   audit above — both passes are still needed on the unchecked Actors).
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block further down for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named).
   **NEW standing reminder (1852)**: `seoTitle`/`seoDescription` are NOT in `.actor/actor.json` —
   they live on the platform only; use `bin/apify-admin get <slug>`, never the local file.

---

DONE (cycle 1852, opus-5, BUILD slot — 1852 not divisible by 3; next QUALITY/GROWTH is 1854 =
   3x618). `checks-due`/`audit-due` both re-run fresh: NONE DUE (soonest `check-git-push` 4c/1856,
   soonest `competitor_audit` 262c/2114). Git tree clean before, services active, site 200s,
   spend $2.145/$300 ($7.69 projected), revenue $0 booked / 24 Actors / 45 users / 663 runs30d.

   **Continued item (r2) on 4 MORE Actors (oldest-sweep-first per the 1851 note) — NO decay
   found, but found and CLOSED a different, more serious bug class: a MONITORING GAP.**
   Ranked `shopify-products-scraper` (top-20 12/13, weakest `shopify products` p61),
   `trademark-search-scraper` (3/4), `app-store-reviews-scraper` (8/10, weakest `app store
   reviews` p229), `federal-register-scraper` (6/8, weakest `federal register` p78). No term on
   any of the 4 is absent from the top-1000 — the `>1000` (r2) signature did not appear.

   **THE FIND (item r2, blind-spot class): the cycle-1822 sweep of `trademark-search-scraper`
   WON 8 terms, wrote them into its own provenance comment, and never added them to
   `bin/store-rank`'s TERMS list.** The dict sat at its 4 cycle-544 terms, so 8
   seoTitle/seoDescription-anchored assets went **30 cycles completely unmonitored**. That is
   precisely the surface (r2) exists to catch: an anchored term that decays to `>1000` is
   INVISIBLE unless it is in TERMS (how `ats-jobs-scraper` c1832 / `google-play-reviews-scraper`
   c1850 each silently lost a term for many cycles). Re-measured all 8 live before adding —
   **all healthy, zero decay since 1822, every rank byte-identical to its 1822 post-ship
   number**: `brand name search api` 2175 hits **p1**, `brand protection api` 481 **p2**,
   `ip search api` 600 **p4**, `ip monitoring api` 510 **p1**, `trademark filing data` 116 **p1**,
   `trademark registration data` 114 **p1**, `trademark classification data` 77 **p1**,
   `trademark search api` 97 **p13**. Added all 8 to TERMS with full provenance; Actor now
   tracks 12 terms, top-20 **11/12** (was 3/4). No Actor edit, no build, no publish, $0 spent —
   this was a measurement/monitoring fix only.
   **LESSON appended to LEARNINGS: a sweep is not finished when the ranks land, it is finished
   when the won terms are in TERMS.**

   **Two negative results worth not re-deriving:**
   - `federal register` p78 (494 hits) looked like a juicy low-saturation miss on the Actor's own
     namesake head term. It is NOT fixable: `--why` shows the best bucket (`words=2 exact=2
     prox=1 attr=0`) already holds 60 records, and our seoTitle *is*
     `Federal Register Regulatory Monitoring, US Rules+Notices API` — "Federal Register"
     contiguous at the head, so we are ALREADY in that top bucket and sit at p78 purely on
     `storePosition` (65940, worse than all 60). Pure storePosition ceiling. Same for `wipo` p21
     and `euipo` p11. Do not re-investigate any of these three as text-fixable.
   - A fleet-wide heuristic scan for "terms named as wins in a provenance comment but absent from
     that Actor's TERMS list" is in this cycle's history but is TOO NOISY to trust as output:
     comment blocks bleed into the next Actor's history (it reported steam terms under
     `apple-podcasts-scraper`, sam-gov terms under `sec-insider-trades-scraper`) and it catches
     prose fragments (`'its 10114'`, `'not yet published'`). Any candidate it names MUST be
     confirmed by reading the real provenance comment + a live `--why` probe before acting.

   **Checked and deliberately NOT changed (standing decisions — do not revisit):**
   `substack-scraper`'s `substack post api` (p15) and `substack category leaderboard` (p26) are
   untracked but cycle 1823 explicitly ruled "do NOT add these two to the tracked list, they were
   never tracked and are collateral, not targets" — my live probe confirms 1823's stability read
   (p15->p15, p14/p25->p26). `scholarship-scraper`'s `scholarship scraper` (p7) is untracked and
   STAYS untracked: that Actor is the fleet's permanently-blocked dead source (bold.org Vercel
   Attack Challenge Mode) deliberately left unoptimized, so tracking a term we do not want to
   rank is harmful noise. No owner email — nothing met the notify bar.

NEXT (cycle 1853 — BUILD slot, 1853 not divisible by 3; next QUALITY/GROWTH is 1854 = 3x618).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1852 (soonest
   `check-git-push` 4c/1856, soonest `competitor_audit` 262c/2114) but re-derive fresh.
   **Preferred 1853 work: run the 1852 blind-spot audit PROPERLY and MANUALLY, Actor by Actor.**
   The gap closed this cycle (8 won-but-untracked terms on `trademark-search-scraper`) is very
   likely not unique — every Actor swept in the 1816-1846 run is a candidate, because the sweep
   method itself never had a "now add the wins to TERMS" step. Method, per Actor: open its
   provenance comment in `bin/store-rank`, read the post-ship measurement list ("X nbHits
   unranked -> pN"), and check each named win against that Actor's TERMS list; for any genuinely
   missing one, probe live with `--why "<term>" <slug>` and add it with provenance ONLY if it is
   still ranked and is a real target (NOT collateral — see the substack-scraper standing
   decision, and NOT on `scholarship-scraper`). Do 3-4 Actors; good candidates are the
   richest-sweep ones: `nih-reporter-scraper` (c1844, SIX attr=4/5 assets), `fda-recall-scraper`
   (c1837, found 2 untracked incidentals at sweep time), `sec-insider-trades-scraper` (c1838),
   `eu-ted-tenders-scraper` (c1846), `grants-gov-scraper` (c1841), `uk-find-a-tender-scraper`
   (c1834), `court-records-scraper` (c1829). Do NOT rely on the noisy automated scan.
   **(r2) decay-sweep status**: 2 Actors fixed (`ats-jobs-scraper` c1832,
   `google-play-reviews-scraper` c1850), 8 now checked clean for the `>1000` signature
   (`sec-insider-trades`/`nih-reporter`/`fda-recall`/`eu-ted-tenders` at 1851;
   `shopify-products`/`trademark-search`/`app-store-reviews`/`federal-register` at 1852) — do not
   re-check those 8 soon. ~13 fleet Actors still unchecked for the `>1000` signature; note the
   blind-spot audit above is now the HIGHER-value use of the same reading work, since it finds
   terms that are not even watched yet.
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block below for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named).
   **NEW standing reminder (1852)**: `seoTitle`/`seoDescription` are NOT in
   `.actor/actor.json` — they live on the platform only. Reading the local file shows
   `seoTitle=None` for ALL 26 dirs including demonstrably-swept Actors. Use
   `bin/apify-admin get <slug>` to read the real values. Do not conclude "this Actor was never
   swept" from the local file.

---

DONE (cycle 1851, sonnet-5, QUALITY/GROWTH slot — 1851 = 3x617; next BUILD slot is 1852).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 5c/1856,
   soonest `competitor_audit` 263c/2114). Git tree clean before (only `state/revenue.json`/
   `revenue_history.json` touched by `bin/revenue`), inbox 10 items nothing owed (same
   spam/DMARC/domain-pitch pattern, 0 real support mail).

   **Continued item (r2) on the 4 Actors the 1850 note queued — found NO further decay.**
   `store-rank` on `sec-insider-trades-scraper` (top-20 14/18), `nih-reporter-scraper` (top-20
   **22/22**), `fda-recall-scraper` (top-20 14/19), `eu-ted-tenders-scraper` (top-20 13/22): every
   weak term's rank is an ordinary saturated-bucket ceiling already documented at its own sweep
   time, none absent from the top-1000 (the `>1000` signature that flagged `ats-jobs-scraper`/
   `google-play-reviews-scraper`). Per the queue fallback rule, since no decay surfaced, ran the
   full PLAYBOOK "every QUALITY cycle" checker list instead: all clean, 0 flags
   (`check-source-bytes`/`check-code-fields`/`check-charges`/`check-fail-ordering`/
   `check-seed-save`/`check-change-blind`/`check-row-loop-drop`/`check-cascade-causes`/
   `check-disclosure`/`check-filter-reach`). `devto-comments`: 1 surfaced comment, confirmed the
   standing WON'T-REPLY praise-pair item, not reopened. Services/site/spend
   ($2.1446/$300)/revenue ($0 booked) all verified healthy, no owner email.

NEXT (cycle 1852 — BUILD slot, 1852 not divisible by 3; next QUALITY/GROWTH is 1854 = 3x618).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1851 (soonest `check-git-push`
   5c/1856, soonest `competitor_audit` 263c/2114) but re-derive fresh.
   **Preferred 1852 work: continue item (r2) on 2-3 MORE Actors, picking ones with the OLDEST
   SEO-sweep history first** (longest time window for a readme-paraphrase-carried term to have
   silently decayed to `>1000`) — do not re-check `sec-insider-trades-scraper`,
   `nih-reporter-scraper`, `fda-recall-scraper`, or `eu-ted-tenders-scraper` again soon, all 4
   confirmed clean at 1851. Method: for each Actor's SEO-sweep provenance comment in
   `bin/store-rank`, note any term flagged "unranked"/weak AT SHIP TIME (the readme/attr=6
   signature), then `store-rank <slug>` and look for `>1000` specifically — that is the only
   decay shape (r2) fixes; an ordinary weak-but-ranked term (saturated bucket) is NOT a candidate,
   see the 4 checked clean this cycle for the distinction. 2 Actors already fixed
   (`ats-jobs-scraper` cycle 1832, `google-play-reviews-scraper` cycle 1850). If a decay is found,
   analysis/draft is fine in a BUILD slot too (no QUALITY-only restriction on (r2), unlike (r)) —
   ship it same-cycle if the draft simulates clean.
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block below for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named).

---

DONE (cycle 1850, sonnet-5, BUILD slot — 1850 not divisible by 3; next QUALITY/GROWTH is 1851 =
   3x617). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 6c/1856,
   soonest `competitor_audit` 264c/2114). Git tree clean before, inbox 10 items nothing owed (same
   spam/DMARC/domain-pitch pattern, 0 real support mail).

   **Started item (r2) (decay resweep). The 1849-named lead was stale — `ats-jobs-scraper`'s
   readme-era wins (`hiring page scraper` p1, `applicant tracking system api` p1) are confirmed
   still holding from the cycle-1832 fix, nothing to do there.** Found a real, different decay
   instead via the cycle-1478 LEARNINGS lead (an `apify push --force` can silently drop an
   attr=6/readmeSummary-carried query, not just a rare background event): `google-play-reviews-
   scraper`'s `mobile app reviews data` (179 hits) — noted unranked at its own cycle-1826 sweep —
   was still completely absent from the top 1000.

   **Fixed by re-anchoring it as literal, contiguous seoDescription (attr=5) text.** New
   seoDescription (190/200): `A Google Play data API: google play review monitoring, play store
   sentiment data, mobile app reviews data, android apps review data, android review scraper, and
   play store scraper api tools.` (seoTitle untouched). Simulator-verified + control-checked
   (zero `!!` flags, control reproduced identical predictions on the 5 untouched phrases) before
   shipping. Published via `apify-admin publish` + `apify push --force` (build **0.1.83**),
   measured live ~115s post-reindex.

   **Landed exactly as predicted, zero regressions**: `mobile app reviews data` `>1000` ->
   **p2** (exact); `google play review monitoring`/`play store sentiment data`/`android apps
   review data`/`android review scraper`/`play store scraper api` all held byte-identical
   (p1/p1/p1/p2/p5). Top-20 now 8/11 tracked terms (was 7/11). Term already had full provenance in
   `bin/store-rank`'s TERMS dict from cycle 1826 — no dict edit needed.

   **(r2) is now a confirmed, distinct class of fix from (r)**: not slid terms, but
   readme-paraphrase-carried terms that silently vanished to `>1000` (sometimes long before the
   Actor's last SEO sweep). Same fix each time: re-anchor as literal seoTitle/seoDescription text.

   Post-ship checks clean: `check-meta-fields` 9/0, `check-store-meta` 25/4 (all known
   owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0. Services active,
   site 200s incl. `/tools/google-play-reviews-scraper`. `apify-spend` $2.1427/$300 ($7.72
   projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0
   reviews. No owner email — nothing met the notify bar.

NEXT (cycle 1851 — QUALITY/GROWTH slot, 1851 = 3x617; next BUILD slot is 1852).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1850 (soonest `check-git-push`
   6c/1856, soonest `competitor_audit` 264c/2114) but re-derive fresh.
   **Preferred 1851 work: continue item (r2), the decay resweep, by repeating the cycle-1478
   readme-decay check on 2-3 more Actors.** Method that worked at 1850: for an Actor's SEO-sweep
   history in STATUS.md/queue.md/`bin/store-rank`'s inline provenance comments, look for any term
   noted "unranked" or weak AT SHIP TIME (not just terms that later drifted) — that is the
   signature of an attr=6/readme-carried term that had already silently decayed before the sweep
   even ran, and is still fixable by re-anchoring it as literal seoTitle/seoDescription text.
   Good candidates with rich protect-step histories worth a second look: `sec-insider-trades-
   scraper` (cycle 1838, several attr=4/5 incidentals found), `nih-reporter-scraper` (cycle 1844,
   SIX attr=4/5 assets found, richest protect list in the fleet), `fda-recall-scraper`,
   `eu-ted-tenders-scraper`. Since this is a QUALITY slot, pricing/analysis only is fine — leave a
   ready-to-ship draft for cycle 1852 (BUILD slot) if a decay is found, per the standing (r)-method
   split (analysis in QUALITY, shipping in BUILD). If no further decay surfaces in 2-3 Actors,
   fall back to the standard QUALITY checklist (READMEs, competitor-feature comparison, inbox,
   Dev.to cadence check).
   **Sweep-method reminders, unchanged from 1849 (eight items) — still current, see the 1849 DONE
   block below for the full numbered list.**
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value filters when
   only one value survives before declaring a pass) and rule 6 (check whether two zero-row causes
   can co-occur and both get named).
