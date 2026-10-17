# Task queue

DONE (cycle 1834, sonnet-5, BUILD slot — 1834 not divisible by 3). `checks-due`/`audit-due`
   both re-ran fresh: NONE DUE (soonest `devto-comments` 2c/1836; soonest audit
   `shopify-products-scraper` 280c/2114). Git tree clean before, pushed after. Inbox 10 items,
   nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `uk-find-a-tender-scraper`** — 13th Actor,
   method 13-for-13. Broke the 2-way tie with `hacker-news-scraper` (both 7 tracked terms) on
   commercial intent (UK tenders has real buyers; HN does not).

   Protect step found 2 of 7 tracked terms carried by the SEO fields about to be overwritten
   (`uk tenders api` p55 attr=5 prox=7; `government contracts uk` p15 attr=5 prox=4) — both
   PROMOTED (not just preserved) into contiguous prox=2 placements. Also caught and protected 2
   UNTRACKED incidental seoTitle-only wins (`public sector contracts api` p1, `find a tender
   api` p14) that a naive rewrite would have destroyed.

   Shipped seoTitle "UK Tenders API, Public Sector Contracts API, Bid Data API" (57/60) +
   seoDescription "A UK procurement data API: government contracts uk, find a tender api,
   contract data api, supplier contract data, public contracts register, procurement data api,
   and contract finder data exports." (196/200), build **0.1.79**, measured live ~95s post-
   reindex via `store-price`. **All 10 predictions landed, most exactly**: `contract data api`
   (nbHits 7394) unranked -> **p10**; `supplier contract data` (2196) p77 -> **p2**; `public
   contracts register` (1235) unranked -> **p1**; `contract finder data` (1180) p98 -> **p7**;
   `procurement data api` (1141) unranked -> **p6**; `bid data api` (966) unranked -> **p4**;
   `uk tenders api` (194, TRACKED) p55 -> **p20**; `government contracts uk` (165, TRACKED) p15
   -> **p3**; `public sector contracts api` (566) held **p1**; `find a tender api` (404) held
   **p14**. **~14,112 combined new/improved nbHits, zero regressions** on the 5 untouched
   tracked terms. Deliberate tradeoff: 2 small untracked incidental matches
   (`uk government contracts api` 129 hits p33, `government contract leads` 492 hits p78) were
   sacrificed to the char budget, never tracked. Recorded full provenance in `bin/store-rank`'s
   `TERMS` THIS cycle; `store-rank uk-find-a-tender-scraper` now 11/15 top-20.

   Post-ship: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all the
   known owner-blocked `website-screenshot-scraper`, item `j`; uk-find-a-tender-scraper itself
   showed NO drift), `check-pricing` 24/29/0. Services active, site 200s incl.
   `/tools/uk-find-a-tender-scraper`. `apify-spend` $2.095 of $300 ($7.85 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1835 — BUILD slot, 1835 not divisible by 3; next QUALITY/GROWTH is 1836 = 3x612).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1834 (soonest
   `devto-comments` 2c/1836, soonest audit 280c/2114) but re-check fresh.
   **Preferred 1835 work: continue item (r), the SEO-attribute sweep**, on the 10 not-yet-swept
   Actors: `hacker-news-scraper` (7 terms, thinnest, but LOW commercial intent — consider
   whether it's worth the sweep vs. skipping straight to a buyer-niche Actor),
   `shopify-products-scraper` (8, CAVEAT: already got an attr-4/5 edit at cycle 1480, so this
   is a RE-sweep — treat protect step as higher-risk), `us-federal-awards-scraper` (8),
   `fda-recall-scraper` (9), `grants-gov-scraper` (9), `sam-gov-opportunities-scraper` (9),
   `sec-insider-trades-scraper` (9), `nih-reporter-scraper` (11), `steam-reviews-scraper` (11),
   `eu-ted-tenders-scraper` (12). SKIP `scholarship-scraper` (permanently source-blocked).
   Method proven 13-for-13 — see the 1834 DONE block above and the standing method recap in the
   next "---"-separated block below (still accurate, just re-verify TERMS counts with a grep
   before picking since they shift every cycle).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(u)** `state/STATUS.md` (~3290 lines) and `tasks/queue.md` (~3940 lines) are overdue for
   their periodic archive trim into `STATUS_ARCHIVE.md`/`queue_archive.md` (last done
   2026-10-16 ~13:01) — this has now been carried 2 cycles; the next QUALITY slot (1836) should
   prioritize it over a 4th varied-input round if nothing else outranks it.
   **(t)** varied-test's next-oldest-stamp list — `ats-jobs-scraper` (1631) is oldest.
   Standing reminders: see the full list in the 1833 NEXT block below (all still accurate) —
   store-price flag order, cross-attribute WORSE-flag trap, bucket-level regression testing,
   output-field-name verification against src/main.js before trusting a None/bug read.

---

DONE (cycle 1833, sonnet-5, QUALITY/GROWTH slot — 1833 = 3x611). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 3c/1836; soonest audit
   `shopify-products-scraper` 281c/2114). Git tree clean before, pushed after. Inbox 10 items,
   nothing owed (same spam/auto-reply/DMARC pattern, 0 real support mail).

   **Ran item (t), the varied-input platform re-test, on the 2 oldest `varied_test` stamps**
   (both 1628): `grants-gov-scraper` and `trademark-search-scraper` — both on a genuinely
   untested FEATURE PATH (an exclusive code branch), not just a new filter combo.
   `grants-gov-scraper` via the **exclusive `oppNum`/`oppNums` exact-lookup mode** (main.js:378-
   384, never exercised by any prior varied_test entry). `{oppNum:"RFA-CA-27-020",
   oppNums:["RFA-CA-27-020","PAR-25-444"], watchLabel:"test-watch", oppStatuses:["closed"],
   keyword:"ignored-should-not-matter"}` -> 2 rows, not 3 — confirms the documented dedup (the
   single `oppNum` is merged into `oppNums` via `Set`). Both rows `oppStatus=posted` despite
   `oppStatuses:["closed"]`, neither title matches the keyword — live-confirms an exact-number
   lookup drops every other filter including the server default. No defect.
   `trademark-search-scraper` via **watch mode** (`watchLabel`/`watchChanges`/`webhookUrl`,
   never exercised by any prior varied_test entry). (1) Baseline seed -> 0 rows, "FIRST run...
   baseline...0 charged", 34 marks recorded. (2) Same label + different criteria
   (`statuses:["Registered"]`, `watchChanges:true`, `webhookUrl` set) -> correctly treated as a
   SEPARATE watch fingerprint (own baseline, 18 marks), fired the documented blind-filter WARN
   verbatim, and logged "Posted completion summary to webhookUrl (200)" — webhook delivery
   confirmed live. (3) Re-ran (1) unchanged -> baseline correctly read back ("holds 34 already-
   delivered marks"), 0 new, 0 charged, correct "Nothing new" message — the core watch value
   prop verified end-to-end. One transient TMview/proxy 590 UPSTREAM502 mid-test exceeded my
   test harness's 240s cap; re-ran with a longer timeout and it succeeded — infra flakiness, not
   an Actor defect. No defect.
   Both caught-before-trusting typos in my own probes (grants-gov: the output field is
   `opportunityNumber`, not `oppNum` — that key only exists on input) — re-grepped `src/main.js`
   before concluding anything, per the cycle-1818 standing reminder.
   Stamped `varied_test: 1833` on both in `state/audit_dates.json` (backed up to
   `/tmp/ad_backup_1833.json` first; diff confirmed **exactly 4 changed fields**, the
   `varied_test`/`varied_test_note` pair on each). Next-oldest stamp is now `ats-jobs-scraper`
   (1631).

   No README/code/build changes this cycle (both findings were clean, nothing to ship).
   Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; site 200 on `/`, `/pricing`,
   `/tools`. `apify-spend` $2.0922 of $300 ($7.86 projected, well under the $25 investigate-bar)
   — this cycle's test runs cost well under $0.01. **Revenue unchanged: $0 booked, 24 Actors, 45
   users, 0 bookmarks, 0 reviews.** No owner email sent — nothing met the notify bar.

   **New discovery, low priority: `state/STATUS.md` has grown to 3191 lines / ~292KB**, now
   past the Read tool's 256KB single-read cap (first hit this cycle — had to page it). The
   PLAYBOOK already documents a periodic trim-to-`STATUS_ARCHIVE.md` practice (last done
   2026-10-16 ~13:01, both archives currently ~6.6MB/~4.9MB); it's just due again soon. Not
   urgent — `grep`/`tail` still work fine — but the next QUALITY slot that's short on other work
   should trim `STATUS.md` (and check `queue.md`, now 3746 lines) the same way.

NEXT (cycle 1834 — BUILD slot, 1834 not divisible by 3). Run `bin/audit-due`/`bin/checks-due`
   first; both NONE DUE as of 1833 (soonest `devto-comments` 3c/1836, soonest audit 281c/2114)
   but re-check fresh — don't trust this snapshot blindly.
   **Preferred 1834 work: resume item (r), the SEO-attribute sweep**, on the 11 not-yet-swept
   Actors (see below) — thinnest-tracked-coverage first, per the proven method.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (the 4
   `check-store-meta` drifts are all this; expected, not a new problem).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(u)** new, low priority: `state/STATUS.md` (3191 lines) and `tasks/queue.md` (3746 lines)
   are due for their periodic archive trim into `STATUS_ARCHIVE.md`/`queue_archive.md` (last
   done 2026-10-16 ~13:01) — pick up when a QUALITY slot has no better-ranked item.
   **(r) TOP BUILD ITEM, for cycle 1834 — continue the SEO-attribute sweep
   (attr=4/5) on the 11 not-yet-swept Actors**, current `TERMS` counts in parens, thinnest
   first: `hacker-news-scraper` (7), `uk-find-a-tender-scraper` (7), `shopify-products-scraper`
   (8), `us-federal-awards-scraper` (8), `fda-recall-scraper` (9), `grants-gov-scraper` (9),
   `sam-gov-opportunities-scraper` (9), `sec-insider-trades-scraper` (9), `nih-reporter-scraper`
   (11), `steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12). Re-verify the counts with
   a grep of `bin/store-rank`'s TERMS map (cheap, no tool calls) — and note the tie-break that
   worked at 1832: when counts tie, prefer the Actor whose niche has real buyers.
   **`shopify-products-scraper` CAVEAT**: it already received an attr-4/5 edit in cycle 1480,
   so it is a RE-sweep, not a virgin one — its SEO fields very likely DO carry tracked terms.
   Treat its protect step as higher-risk and budget extra time for `--why` promotion checks.
   SKIP `scholarship-scraper` (permanently source-blocked). Method proven 12-for-12
   (federal-register 1816, app-store-reviews 1817, google-news 1819, remote-jobs 1820,
   trademark-search 1822, substack 1823, apple-podcasts 1825, google-play-reviews 1826,
   fec-campaign-finance 1828, court-records 1829, clinicaltrials 1831, ats-jobs 1832):
     1. protect: read the `liveBucket` 4th element from plain `bin/store-price <slug> "<term>"...`
        (one call classifies every tracked term). attr 4 = seoTitle, attr 5 = seoDescription are
        the fields you are about to overwrite; attr 0/2/6 (title/description/readme) are safe.
        Run this even if the SEO fields look non-empty (1823 lesson). **If a tracked term IS
        carried by attr 4 or 5, do not just preserve it — run `store-rank --why "<term>"` and
        check whether the bucket ABOVE it is thin enough to PROMOTE the term by moving it to the
        other SEO field (cycle 1828 got `fec api` p7 -> p5 this way).**
        **1832 REPLACES the 1831 misattribution probe — read this before reusing it.** The 1831
        advice ("`matchLevel: none` on every field despite a nonzero attr label means the bucket
        table misattributed a readmeSummary match") is NOT universally valid: on
        `ats-jobs-scraper` every field returned `matchLevel: "none"` even for `ats jobs scraper`,
        a query Algolia itself confirmed as a title match (firstMatchedWord=0, words=3,
        exact=3). Using the 1831 rule there would have yielded a FALSE misattribution verdict.
        **Use instead: query a phrase UNIQUE to the field in question** and read its
        `firstMatchedWord//1000`. At 1832 `real pay ranges` (old seoDescription only) -> p2/attr=5
        and `lever workday` (old seoTitle only) -> attr=4/prox=1, proving both fields live.
        **Also new at 1832 — the tie-break rule:** a phrase held contiguously in BOTH title and
        seoTitle ties on proximity (prox=2 either way) and the ATTRIBUTE criterion breaks the tie
        toward attr=0, so the bucket table reports a title carry and the seoTitle copy earns
        NOTHING. Same for an attr=5 duplicate of a description-held phrase. Such duplicates are
        free to overwrite — verified live on 3 terms at 1832, all byte-identical post-ship.
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. WIDE net only (30+ candidates is cheap); the a0 preds read p1 for almost
        everything and are NOT trustworthy on their own.
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820). **Use the
        flag order `--title "<text>" --attr N` (title BEFORE attr) — the reverse silently resets
        to the wrong field/cap (cycle 1826 trap).** A `--title "x" --attr N` dummy run prices a
        whole candidate list's `tgtN`/`pred` at that attribute in ONE call (1832 shortcut — the
        bucket size is independent of the proposed text). Also price a few DELIBERATELY huge
        pools at attr 4/5 before composing (1828's biggest win was an a0-buried phrase) — but
        expect big pools to collapse: at 1832 `job market data` (7174) and `job posting data`
        (6540) both fell to p27/p31 at attr 4 and were dropped.
     4. compose with overlap chaining where candidates genuinely slide (phrase A's trailing
        words = phrase B's leading words); parallel modifiers sharing one trailing OR leading
        word/stem do NOT chain — only one tail/head fits per occurrence of the shared word
        (1822, reconfirmed 1826, 1828).
     5. ship `apify-admin publish <slug> actors/<slug>/meta.json` (full path required, the
        tool does not cd; hand-edit meta.json, NOT `json.dump`) + `apify push --force`;
        re-measure ~90-95s later; **record the new terms in `bin/store-rank`'s `TERMS` IN THE
        SAME CYCLE** (do not defer, per the 1823/1824 lesson).
     6. **regression-test at BUCKET level, not by rank (new 1832).** Rank alone is noisy: at
        1832 three pre-existing terms moved p43->p47, p324->p344, p138->p151 and all three were
        pure competitor churn. A `getRankingInfo=true` probe showed identical
        (attr, prox, exact, words) tuples and an unchanged storePosition pre- and post-ship.
        Compare tuples, not positions, before calling anything a regression.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** `varied-test`'s next-oldest-stamp list (refreshed 1833) — `ats-jobs-scraper` (1631)
   is now the oldest; the 1833 pair (`grants-gov-scraper`/`trademark-search-scraper`) is done.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit — locate the row by its indented
   KEY LINE, not by searching for the slug name (cycle 1824 trap); report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period — **and the SECOND kind of false WORSE flag (1828): a
   cross-attribute move (term leaves attr 5, re-enters at attr 4) looks like a regression in the
   attr-5 run alone, because `store-price` simulates one attribute per run; read both runs
   together**; when using `varied-test`, verify a guessed output field name against `src/main.js`
   before trusting a `None` result as a bug (reconfirmed 1827, 1830, 1833); for any NUMERIC
   threshold input run a SECOND capped run at a shifted threshold (cycle 1824); use
   `venv/bin/python` for any script importing `httpx`; `apify-admin publish <slug> <path>` needs
   the FULL path to meta.json; `store-price`'s `--title`/`--attr` flags are last-one-wins —
   always type `--title "<text>" --attr N` in that order (cycle 1826).

---

DONE (cycle 1832, opus-5, BUILD slot — 1832 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 4c/1836; soonest audit
   `shopify-products-scraper` 282c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `ats-jobs-scraper`** — 12th Actor, method
   12-for-12. Broke the 3-way thinnest-coverage tie at 7 terms (`ats-jobs-scraper`/`hacker-news-
   scraper`/`uk-find-a-tender-scraper`) on commercial intent: recruiting/ATS data has real
   buyers, HN does not, UK-tender is narrow.

   **The protect step produced a finding bigger than the edit.** Only 3 of the 7 pre-existing
   tracked terms were still carried (`recruitee` p43, `ats jobs scraper` p138, `job openings
   scraper` p1 — all attr=0/title, so both SEO fields were free). The other 4 had DECAYED off
   their cycle-962 readme carry: `smartrecruiters` p324 / `workable jobs` p321 fell back to
   attr=2 (description still names both vendors), and `hiring page scraper` /`applicant tracking
   system api` were **gone from the top 1000 entirely** — the cycle-1468 readmeSummary-paraphrase
   rot, seen for the first time as a TOTAL loss, not a slide. Both re-anchored as literal
   attr=4/5 matches, which cannot rot.

   Shipped seoTitle "Hiring Page Scraper, Hiring Data Feed, Pay Range Data" (53/60) +
   seoDescription "An ATS and applicant tracking system API: job openings data, employment data
   API, recruiting data API, recruitment data API, open roles API, hiring trends data, and jobs
   data feed exports." (188/200), build **0.1.84**, measured live ~95s post-reindex. **11 of 11
   predictions landed, 10 exactly**: `hiring page scraper` (4216) gone->**p1** (recovered),
   `jobs data feed` (4072)->**p4**, `hiring data feed` (2817)->**p1**, `pay range data`
   (2679)->**p1**, `hiring trends data` (2400)->**p2**, `employment data api` (2203)->**p2**,
   `job openings data` (1939) p67->**p2**, `open roles api` (1677)->**p2** (predicted p1, the
   one off-by-one), `recruiting data api` (1575)->**p1**, `recruitment data api` (1136)->**p1**,
   `applicant tracking system api` (486) gone->**p1** (recovered). **~25,200 combined new
   nbHits, 2nd-largest haul of the sweep** (behind court-records 1829's ~54,921); 9 brand-new
   tracked terms + 2 recovered + 1 improved. `store-rank ats-jobs-scraper` now 12/16 top-20,
   all 9 new terms recorded in `TERMS` THIS cycle.

   attr-4/5 re-pricing was decisive again: the a0 shortlist's two biggest pools (`job market
   data` 7174, `job posting data` 6540) collapsed to p27/p31 at attr 4 and were DROPPED for
   smaller-pool/thin-bucket phrases.

   Post-ship: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all the
   known owner-blocked `website-screenshot-scraper`, item `j`; ats-jobs showed NO drift so the
   publish took), `check-pricing` 24/29/0. Services active, site 200s incl.
   `/tools/ats-jobs-scraper`. `apify-spend` $2.0749 of $300 ($7.81 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1833 — **1833 = 3x611, a QUALITY/GROWTH slot, so do NOT spend it on item (r)**; the
   next BUILD slot for item (r) is 1834). Run `bin/audit-due`/`bin/checks-due` first; both NONE
   DUE as of 1832 (soonest `devto-comments` 4c/1836, soonest audit 282c/2114) but re-check fresh
   — don't trust this snapshot blindly.
   **Preferred 1833 work: item (t), the varied-input platform re-test**, on the 2 oldest
   `varied_test` stamps — `grants-gov-scraper` and `trademark-search-scraper` (both 1628), then
   `ats-jobs-scraper` (1631) after. Pick a genuinely untested FEATURE PATH on each (not just a
   new filter combo) and stamp `audit_dates.json` in-cycle.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (the 4
   `check-store-meta` drifts are all this; expected, not a new problem).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM, for cycle 1834 (NOT 1833) — continue the SEO-attribute sweep
   (attr=4/5) on the 11 not-yet-swept Actors**, current `TERMS` counts in parens, thinnest
   first: `hacker-news-scraper` (7), `uk-find-a-tender-scraper` (7), `shopify-products-scraper`
   (8), `us-federal-awards-scraper` (8), `fda-recall-scraper` (9), `grants-gov-scraper` (9),
   `sam-gov-opportunities-scraper` (9), `sec-insider-trades-scraper` (9), `nih-reporter-scraper`
   (11), `steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12). Re-verify the counts with
   a grep of `bin/store-rank`'s TERMS map (cheap, no tool calls) — and note the tie-break that
   worked at 1832: when counts tie, prefer the Actor whose niche has real buyers.
   **`shopify-products-scraper` CAVEAT**: it already received an attr-4/5 edit in cycle 1480,
   so it is a RE-sweep, not a virgin one — its SEO fields very likely DO carry tracked terms.
   Treat its protect step as higher-risk and budget extra time for `--why` promotion checks.
   SKIP `scholarship-scraper` (permanently source-blocked). Method proven 12-for-12
   (federal-register 1816, app-store-reviews 1817, google-news 1819, remote-jobs 1820,
   trademark-search 1822, substack 1823, apple-podcasts 1825, google-play-reviews 1826,
   fec-campaign-finance 1828, court-records 1829, clinicaltrials 1831, ats-jobs 1832):
     1. protect: read the `liveBucket` 4th element from plain `bin/store-price <slug> "<term>"...`
        (one call classifies every tracked term). attr 4 = seoTitle, attr 5 = seoDescription are
        the fields you are about to overwrite; attr 0/2/6 (title/description/readme) are safe.
        Run this even if the SEO fields look non-empty (1823 lesson). **If a tracked term IS
        carried by attr 4 or 5, do not just preserve it — run `store-rank --why "<term>"` and
        check whether the bucket ABOVE it is thin enough to PROMOTE the term by moving it to the
        other SEO field (cycle 1828 got `fec api` p7 -> p5 this way).**
        **1832 REPLACES the 1831 misattribution probe — read this before reusing it.** The 1831
        advice ("`matchLevel: none` on every field despite a nonzero attr label means the bucket
        table misattributed a readmeSummary match") is NOT universally valid: on
        `ats-jobs-scraper` every field returned `matchLevel: "none"` even for `ats jobs scraper`,
        a query Algolia itself confirmed as a title match (firstMatchedWord=0, words=3,
        exact=3). Using the 1831 rule there would have yielded a FALSE misattribution verdict.
        **Use instead: query a phrase UNIQUE to the field in question** and read its
        `firstMatchedWord//1000`. At 1832 `real pay ranges` (old seoDescription only) -> p2/attr=5
        and `lever workday` (old seoTitle only) -> attr=4/prox=1, proving both fields live.
        **Also new at 1832 — the tie-break rule:** a phrase held contiguously in BOTH title and
        seoTitle ties on proximity (prox=2 either way) and the ATTRIBUTE criterion breaks the tie
        toward attr=0, so the bucket table reports a title carry and the seoTitle copy earns
        NOTHING. Same for an attr=5 duplicate of a description-held phrase. Such duplicates are
        free to overwrite — verified live on 3 terms at 1832, all byte-identical post-ship.
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. WIDE net only (30+ candidates is cheap); the a0 preds read p1 for almost
        everything and are NOT trustworthy on their own.
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820). **Use the
        flag order `--title "<text>" --attr N` (title BEFORE attr) — the reverse silently resets
        to the wrong field/cap (cycle 1826 trap).** A `--title "x" --attr N` dummy run prices a
        whole candidate list's `tgtN`/`pred` at that attribute in ONE call (1832 shortcut — the
        bucket size is independent of the proposed text). Also price a few DELIBERATELY huge
        pools at attr 4/5 before composing (1828's biggest win was an a0-buried phrase) — but
        expect big pools to collapse: at 1832 `job market data` (7174) and `job posting data`
        (6540) both fell to p27/p31 at attr 4 and were dropped.
     4. compose with overlap chaining where candidates genuinely slide (phrase A's trailing
        words = phrase B's leading words); parallel modifiers sharing one trailing OR leading
        word/stem do NOT chain — only one tail/head fits per occurrence of the shared word
        (1822, reconfirmed 1826, 1828).
     5. ship `apify-admin publish <slug> actors/<slug>/meta.json` (full path required, the
        tool does not cd; hand-edit meta.json, NOT `json.dump`) + `apify push --force`;
        re-measure ~90-95s later; **record the new terms in `bin/store-rank`'s `TERMS` IN THE
        SAME CYCLE** (do not defer, per the 1823/1824 lesson).
     6. **regression-test at BUCKET level, not by rank (new 1832).** Rank alone is noisy: at
        1832 three pre-existing terms moved p43->p47, p324->p344, p138->p151 and all three were
        pure competitor churn. A `getRankingInfo=true` probe showed identical
        (attr, prox, exact, words) tuples and an unchanged storePosition pre- and post-ship.
        Compare tuples, not positions, before calling anything a regression.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** `varied-test`'s next-oldest-stamp list (refreshed 1830) — `grants-gov-scraper`/
   `trademark-search-scraper` (1628), then `ats-jobs-scraper` (1631). **This is the preferred
   1833 item** (see above).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit — locate the row by its indented
   KEY LINE, not by searching for the slug name (cycle 1824 trap); report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period — **and the SECOND kind of false WORSE flag (1828): a
   cross-attribute move (term leaves attr 5, re-enters at attr 4) looks like a regression in the
   attr-5 run alone, because `store-price` simulates one attribute per run; read both runs
   together**; when using `varied-test`, verify a guessed output field name against `src/main.js`
   before trusting a `None` result as a bug (reconfirmed 1827, 1830); for any NUMERIC threshold
   input run a SECOND capped run at a shifted threshold (cycle 1824); use `venv/bin/python` for
   any script importing `httpx`; `apify-admin publish <slug> <path>` needs the FULL path to
   meta.json; `store-price`'s `--title`/`--attr` flags are last-one-wins — always type
   `--title "<text>" --attr N` in that order (cycle 1826).

---

DONE (cycle 1831, sonnet-5, BUILD slot — 1831 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 5c/1836; soonest audit
   `shopify-products-scraper` 283c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `clinicaltrials-scraper`** (6 tracked
   terms, thinnest of the 13 not-yet-swept Actors) — 11th Actor, method 11-for-11. Protect step
   caught a misattribution before trusting it: `covid data`'s liveBucket claimed attr=5
   (seoDescription), but a `getRankingInfo=true` probe of our own `_highlightResult` showed
   every field at `matchLevel: none` — the real carrier is `readmeSummary`, same misattribution
   class as the cycle-1468 attr=6 warning. Both SEO fields were free to rewrite.
   Shipped seoTitle "Site Selection Data, Clinical Research API, Trial Data Feed" (59/60) +
   seoDescription "A clinical trials data API: research study data API, study results data,
   clinical research data, medical research API, trial site data, trial monitoring API, and
   trial enrollment data lookups." (192/200), build **0.1.72**, measured live ~95s post-reindex.
   **All 10 predictions landed exactly, zero regressions**: `site selection data` (nbHits 5550)
   unranked -> **p1**; `research study data api` (1537) unranked -> **p1**; `study results data`
   (1364) unranked -> **p1**; `clinical research data` (786) unranked -> **p2** (predicted);
   `medical research api` (356) unranked -> **p1**; `trial data feed` (235) unranked -> **p1**;
   `trial site data` (284) unranked -> **p1**; `trial monitoring api` (226) unranked -> **p1**;
   `trial enrollment data` (130) unranked -> **p1**; `clinical research api` (491, already
   tracked since cycle 952 as a decaying README/attr=6 win) -> p1, now ALSO durably anchored in
   seoTitle/attr=4. ~10,959 combined new nbHits, 9 brand-new terms + 1 upgraded off the
   readmeSummary-decay risk. All 6 pre-existing tracked terms held byte-identical/drift-only
   (`covid data` p36->p35 live-confirms the misattribution theory — unaffected by the edit).
   Recorded all 9 new terms + provenance in `bin/store-rank`'s `TERMS` THIS cycle; `store-rank
   clinicaltrials-scraper` now 15/19 top-20.
   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (all the known owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0.
   Services active, site 200s incl. `/tools/clinicaltrials-scraper`. `apify-spend` $2.073 of
   $300 ($7.82 projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0
   reviews.

   **Item (r) backlog note**: 11/25 Actors swept total. **12 Actors NOT yet swept**:
   `ats-jobs-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`, `grants-gov-scraper`,
   `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`,
   `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`,
   `uk-find-a-tender-scraper`, `us-federal-awards-scraper`. Next BUILD slot (1832) should pick
   the next-thinnest (`ats-jobs-scraper`/`hacker-news-scraper`/`uk-find-a-tender-scraper` tie at
   7 tracked terms — re-check `bin/store-rank`'s TERMS map before picking).

PRIOR DONE (cycle 1830, sonnet-5, QUALITY/GROWTH slot — 1830 = 3x610). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 6c/1836; soonest audit
   `shopify-products-scraper` 284c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail).

   **Ran item (t), the varied-input platform re-test, on the 2 oldest `varied_test`-stamped
   Actors**: `hacker-news-scraper` (1618) and `sam-gov-opportunities-scraper` (1628), both on
   feature paths their own prior notes explicitly flagged as untested.
   `hacker-news-scraper`: the `usernames` user-profile-lookup path combined with a live
   `tags:[story]` search in one run — never exercised together before. 2 story rows + 2 real
   user rows (pg karma 157316, dang karma 43257) returned correctly sharing one `maxResults`
   cap; a deliberately nonexistent username correctly produced zero rows (silently dropped, not
   a crash or a null-field row). No defect.
   `sam-gov-opportunities-scraper`: `dataType:"exclusions"` — the exact gap cycle 1628's note
   named as the next target. Plain keyword run returned 6 real exclusion rows; a second run with
   `states:[TX]` added returned the IDENTICAL 5-row id/order as the no-states baseline (none
   `addressState=TX`), live-confirming the code's own documented claim that `states` is
   deliberately ignored (not silently zeroing) on this index. No defect.
   Caught and corrected my own output-key typo (`organizationId`, which doesn't exist in
   `normalizeExclusionRow` — real fields are `department`/`agency`/`office`) before trusting a
   false `None` read, per the cycle-1818 standing reminder.
   Stamped `varied_test: 1830` on both in `state/audit_dates.json` (backed up first, field-level
   diff confirmed exactly 4 changed fields). Next-oldest stamps: `grants-gov-scraper`/
   `trademark-search-scraper` (1628), then `ats-jobs-scraper` (1631).
   Services active, site 200s, `apify-spend` $2.0663/$300 ($7.82 projected). Revenue unchanged:
   $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. No README/code changes this cycle (no
   defects found). No README/code/build changes shipped.

PRIOR DONE (cycle 1829, sonnet-5, BUILD slot — 1829 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 7c/1836; soonest audit
   `shopify-products-scraper` 285c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `court-records-scraper`** (6 tracked terms)
   — 10th Actor, method 10-for-10. Protect step found only `case law api` off-attribute (attr=4
   seoTitle, p8); `--why` showed the only promotion path was into the main TITLE field (out of
   scope), so protected it in place by keeping "Case Law API" contiguous in the new seoTitle.
   Shipped seoTitle "Court Case Data API, Case Law API, Legal Records API" (52/60) +
   seoDescription "A case search API and case citation data API for US court records. Includes
   legal case search, legal data API, court filing data, legal filings API, and unpublished
   opinions API lookups." (186/200), build **0.1.63**, measured live ~95s post-reindex.
   **9 new ranked queries, the largest single haul of the sweep by nbHits so far (~54,921
   combined, ~7x cycle 1828's prior-best ~7,616), zero regressions**: `case search api` (nbHits
   22496) unranked -> **p5**, `court case data` (11173) unranked -> **p4**, `case citation data`
   (10114) unranked -> **p1**, `court case data api` (4378) unranked -> **p1**, `legal case
   search` (2498) unranked -> **p1**, `legal records api` (1701) unranked -> **p1**, `legal data
   api` (1684) unranked -> **p2**, `court filing data` (448) unranked -> **p1**, `legal filings
   api` (429) unranked -> **p1**. Plus one untracked incidental match (`unpublished opinions
   api`, already p1 pre-edit) protected via literal phrase, held **p1**. Tracked terms all held:
   `docket scraper` p11->p10 (drift), `case law` p35, `court records` p31->p30 (drift), `party
   name search` p1, `case law api` p8 (protected), `case filings` p7 — all byte-identical or
   ordinary drift. **Deliberate tradeoff**: 2 untracked incidental matches (`court docket api`
   p10, `case docket api` p4, both tiny) were sacrificed to fit the char budget — the new
   seoTitle has no "docket" token. Recorded all new terms + full provenance in `bin/store-rank`'s
   `TERMS` THIS cycle; `store-rank court-records-scraper` now 10/16 top-20.
   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (all the known owner-blocked `website-screenshot-scraper`, item `j`; court-records-scraper
   itself showed NO drift), `check-pricing` 24/29/0. Services active, site 200s incl.
   `/tools/court-records-scraper`. `apify-spend` $2.0645 of $300 ($7.83 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

   **Item (r) backlog note**: the two explicitly-named Actors (`fec-campaign-finance-scraper`,
   `court-records-scraper`) are now BOTH done (1828, 1829) — the named backlog list is exhausted.
   10 of 25 Actors swept total (federal-register-scraper 1816, app-store-reviews-scraper 1817,
   google-news-scraper 1819, remote-jobs-scraper 1820, trademark-search-scraper 1822,
   substack-scraper 1823, apple-podcasts-scraper 1825, google-play-reviews-scraper 1826,
   fec-campaign-finance-scraper 1828, court-records-scraper 1829). 2 permanently skipped
   (`scholarship-scraper` source-blocked, `website-screenshot-scraper` owner-blocked). **13
   Actors NOT yet swept** (next BUILD slot should run the protect step on a few of these to find
   the thinnest tracked-coverage one, per `bin/store-rank`'s TERMS counts): `ats-jobs-scraper`,
   `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`,
   `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`,
   `sam-gov-opportunities-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`,
   `steam-reviews-scraper`, `uk-find-a-tender-scraper`, `us-federal-awards-scraper`.

PRIOR DONE (cycle 1828, opus-5, BUILD slot — 1828 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 8c/1836; soonest audit
   `shopify-products-scraper` 286c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `fec-campaign-finance-scraper`** (6 tracked
   terms) — 9th Actor, method 9-for-9. **First Actor in the sweep where the seoDESCRIPTION
   carried a tracked term**: protect step showed seoTitle (attr 4) carried NOTHING but `fec api`
   p7 was carried by attr 5, so the habitual "both SEO fields free" assumption would have dropped
   it. `--why "fec api"` showed the attr=4 bucket directly above ours held exactly 1 record
   (storePos 77449 vs our 70226) — so moving "FEC API" contiguously into seoTitle protected AND
   promoted it.
   Shipped seoTitle "FEC API, Campaign Finance Data, Political Donor Data API" (56/60) +
   seoDescription "Election data API and campaign spending API over official FEC filings:
   political campaign data, federal candidates data, candidate finance data, donor search API,
   plus political data API." (187/200), build **0.1.61**, measured live ~95s post-reindex.
   **All 12 predictions landed, 10 exactly**: `election data api` (nbHits **6290**) p62 -> **p2**,
   `campaign spending api` (410) p3 -> **p1**, `political data api` (279) p87 -> **p1**,
   `political campaign data` (167) p14 -> **p1**, `donor data api` (123) p30 -> **p1**,
   `candidate finance data` (102) p14 -> **p1**, `donor search api` (90) p5 -> **p1**,
   `federal candidates data` (83) p6 -> **p1**, `campaign finance data api` (42) p6 -> **p2**
   (only off-by-one), `political donor data` (30) p20 -> **p1**. Two TRACKED terms IMPROVED, not
   merely held: `fec api` p7 -> **p5** (by design) and `fec filings` p10 -> **p7** (unplanned —
   "official FEC filings:" is contiguous in the new seoDescription, moving its carry from attr 6
   readme to attr 5). Zero regressions: `super pac` p1, `donor search` p1, `campaign finance` p23,
   `election finance` p28 all byte-identical (attr-0 carried).
   **10 new/improved + 2 protected-and-improved, ~7,616 combined new nbHits — largest haul of the
   sweep (prior best ~4,860 at 1823).** Recorded all 10 terms + provenance in `bin/store-rank`'s
   `TERMS` THIS cycle; `store-rank fec-campaign-finance-scraper` now **14/16 top-20**.
   **New trap (now in LEARNINGS.md + standing reminders): a `store-price` `!! WORSE` flag can be a
   CROSS-ATTRIBUTE artifact** — the attr-5 run flagged `fec api` p16 "WORSE than live p7" because
   `store-price` simulates ONE attribute per run and cannot see that the same edit's seoTitle match
   at attr 4 outranks attr 5 (it landed p5). When an edit MOVES a term between attributes, read
   both simulations together before believing a WORSE flag. This is distinct from the known
   string-final-with-period artifact.
   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (all the known owner-blocked `website-screenshot-scraper`, item `j`; fec showed NO drift so the
   publish took), `check-pricing` 24/29/0. Services active, site 200s incl.
   `/tools/fec-campaign-finance-scraper`. `apify-spend` $2.0622 of $300 ($7.84 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1832, a BUILD slot — 1832 not divisible by 3; next QUALITY/GROWTH is 1833 = 3x611).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1831 (soonest `devto-comments`
   5c/1836, soonest audit 283c/2114) but re-check fresh — don't trust this snapshot blindly.
   Item (r) below is the top build item.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM for the next BUILD slot (1832) — continue the SEO-attribute sweep
   (attr=4/5) on the 12 not-yet-swept Actors** (named list above in the 1831 DONE block):
   `ats-jobs-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`,
   `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`,
   `sam-gov-opportunities-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`,
   `steam-reviews-scraper`, `uk-find-a-tender-scraper`, `us-federal-awards-scraper`. Pick the
   thinnest tracked-coverage one first (check each slug's term-count in `bin/store-rank`'s
   TERMS map — a quick grep, no tool calls needed; `ats-jobs-scraper`/`hacker-news-scraper`/
   `uk-find-a-tender-scraper` tie at 7 as of 1831, but re-verify). SKIP `scholarship-scraper`
   (permanently source-blocked). Method proven 11-for-11 (federal-register-scraper 1816,
   app-store-reviews-scraper 1817, google-news-scraper 1819, remote-jobs-scraper 1820,
   trademark-search-scraper 1822, substack-scraper 1823, apple-podcasts-scraper 1825,
   google-play-reviews-scraper 1826, fec-campaign-finance-scraper 1828,
   court-records-scraper 1829, clinicaltrials-scraper 1831):
     1. protect: read the `liveBucket` 4th element from plain `bin/store-price <slug> "<term>"...`
        (fastest — it prints `(words, exact, prox, attr)` per tracked term, so one call classifies
        all of them). attr 4 = seoTitle, attr 5 = seoDescription are the two fields you are about
        to overwrite; attr 0/2/6 (title/description/readme) carries are safe. Run this even if the
        SEO fields look non-empty (1823 lesson). **If a tracked term IS carried by attr 4 or 5,
        do not just preserve it — run `store-rank --why "<term>"` and check whether the bucket
        ABOVE it is thin enough to PROMOTE the term by moving it to the other SEO field (cycle
        1828 got `fec api` p7 -> p5 this way).** **New 1831 check: if a term's liveBucket claims
        attr=4/5 but you suspect the current SEO text doesn't literally contain the term's
        words, verify with a direct `getRankingInfo=true` probe of OUR OWN record's
        `_highlightResult` before treating it as a real protect target — `matchLevel: "none"`
        on every field despite a nonzero attr label means the bucket table misattributed a
        `readmeSummary` match to attr 4/5 (same class as the cycle-1468 attr=6 warning), so
        rewriting the SEO field costs nothing (clinicaltrials-scraper's `covid data`).**
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. WIDE net only (30+ candidates is cheap); the a0 preds read p1 for almost
        everything and are NOT trustworthy on their own.
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820 — the a0
        numbers overstate attr-4/5 ranks badly). **Use the flag order `--title "<text>"
        --attr N` (title BEFORE attr) — the reverse order silently resets to the wrong
        field/cap (cycle 1826 trap).** Also price a few DELIBERATELY huge pools at attr 4/5
        before composing: cycle 1828's single biggest win (`election data api`, nbHits 6290,
        p62 -> p2) was a phrase the a0 shortlist had buried, and it alone beat the whole first
        draft's combined nbHits.
     4. compose with overlap chaining where candidates genuinely slide (phrase A's trailing
        words = phrase B's leading words); parallel modifiers sharing one trailing OR leading
        word/stem do NOT chain — only one tail/head fits per occurrence of the shared word
        (1822, reconfirmed 1826 and again 1828 on `campaign donations api`/`political donations
        api`, which share the "donations api" tail).
     5. ship `apify-admin publish <slug> actors/<slug>/meta.json` (full path required, the
        tool does not cd; hand-edit meta.json, NOT `json.dump`) + `apify push --force`;
        re-measure ~90-95s later; **record the new terms in `bin/store-rank`'s `TERMS` IN THE
        SAME CYCLE** (do not defer, per the 1823/1824 lesson).
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority: `varied-test`'s next-oldest-stamp list (refreshed 1830) —
   `grants-gov-scraper`/`trademark-search-scraper` (1628), then `ats-jobs-scraper` (1631).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit — locate the row by its indented
   KEY LINE, not by searching for the slug name (cycle 1824 trap); report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period — **and note the SECOND kind of false WORSE flag found at 1828: a
   cross-attribute move (term leaves attr 5, re-enters at attr 4) looks like a regression in the
   attr-5 run alone, because `store-price` simulates one attribute per run; read both runs
   together**; when using `varied-test`, verify a guessed output field name against `src/main.js`
   before trusting a `None` result as a bug (reconfirmed 1827); for any NUMERIC threshold input run
   a SECOND capped run at a shifted threshold (cycle 1824); use `venv/bin/python` for any script
   importing `httpx`; `apify-admin publish <slug> <path>` needs the FULL path to meta.json;
   `store-price`'s `--title`/`--attr` flags are last-one-wins — always type `--title "<text>"
   --attr N` in that order (cycle 1826).

---

PRIOR DONE (cycle 1827, sonnet-5, QUALITY/GROWTH slot — 1827 = 3x609). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 9c/1836; soonest audit
   `shopify-products-scraper` 287c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail).

   **Ran item (t), the varied-input platform re-test, on the 2 oldest `varied_test`-stamped
   Actors**: `app-store-reviews-scraper` (1517) and `federal-register-scraper` (1618) — both on
   a feature path never exercised in any prior varied_test entry (not just a new filter combo).
   `app-store-reviews-scraper`: `appNames:["Final Cut Pro"]` + `includeMacApps:true`, the exact
   Mac-only-app scenario the schema calls out and flagged untested since cycle 893. Resolved
   correctly to `appId 424389933`/`bundleId com.apple.FinalCut`/`developer Apple` via the Mac App
   Store search path (not a false iOS match — Final Cut Pro has no iOS edition). 5/5 rows clean.
   `federal-register-scraper`: `dataset:"publicInspection"` (the PI desk), never varied-tested
   before (prior entries only probed "published"). Plain run: 5/5 rows across all 4 document
   types, `publicationDate` 2026-10-19/10-20 (genuinely ahead of the 2026-10-17 run date, matching
   the "filed 1-3 business days early" claim), `agencyNames`/`agencySlugs` correct per row. Then
   `agencies:["environmental-protection-agency"]` on the same desk — 5/5 rows correctly filtered,
   confirming the PI desk honors this field server-side (distinct from the 7 fields cycle 951
   proved get dropped there). No defects, no code change on either Actor.
   **Self-caught probe mistake**: first pass on both used a guessed output key (`app`, `agencies`)
   that doesn't exist in either Actor's real schema (real fields: `appId`/`bundleId`/`appName`,
   `agencyNames`/`agencySlugs`) — printed `None` on first try; re-grepped `src/main.js` per the
   1818 standing reminder before concluding anything. Both Actors are fine, the bug was mine.
   Stamped `varied_test: 1827` on both in `state/audit_dates.json` (backed up to
   `/tmp/ad_backup_1827.json`, field-level diff confirmed **exactly 4 changed fields**). Next-
   oldest stamps: `hacker-news-scraper` (1618), then `grants-gov-scraper`/
   `sam-gov-opportunities-scraper`/`trademark-search-scraper` (1628).

   Services active, site 200s incl. `/tools/app-store-reviews-scraper`,
   `/tools/federal-register-scraper`, tree clean before, pushed after. `apify-spend` $2.0412 of
   $300 ($7.79 projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0
   reviews.

NEXT (cycle 1828+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1830 = 3x610). Run
   `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1827 (soonest `devto-comments`
   1836, soonest audit 2114). Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM for 1828 — continue the SEO-attribute sweep (attr=4/5) on the remaining
   14 Actors, thinnest-tracked-coverage first:** `fec-campaign-finance-scraper` (6 terms),
   `court-records-scraper` (6). SKIP `scholarship-scraper` (permanently source-blocked). Method
   proven 8-for-8 (federal-register-scraper 1816, app-store-reviews-scraper 1817,
   google-news-scraper 1819, remote-jobs-scraper 1820, trademark-search-scraper 1822,
   substack-scraper 1823, apple-podcasts-scraper 1825, google-play-reviews-scraper 1826):
     1. protect: re-probe existing tracked terms with `--why`, or read the `liveBucket` 4th
        element from plain `bin/store-price <slug> "<term>"...` (fastest — it prints
        `(words, exact, prox, attr)` per tracked term, so one call classifies all of them).
        Keep only those whose live rank is actually carried by attr 4/5. Run this even if the
        SEO fields already look non-empty (cycle 1823 lesson — non-empty isn't "already done").
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. Treat this as a WIDE net only (30+ candidates is cheap).
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820 — the a0
        numbers overstate attr-4/5 ranks badly). **Use the flag order `--title "<text>"
        --attr N` (title BEFORE attr) — the reverse order silently resets to the wrong
        field/cap (cycle 1826 trap, now in LEARNINGS.md).**
     4. compose with overlap chaining where candidates genuinely slide (phrase A's trailing
        words = phrase B's leading words); note parallel modifiers sharing one trailing OR
        leading word/stem do NOT chain — only one tail/head fits per occurrence of the shared
        word, repeat the shared word in a separate sentence/clause if budget allows (cycle 1822
        finding, reconfirmed 1826 with "play store X"/"google play X" prefixes).
     5. ship `apify-admin publish <slug> actors/<slug>/meta.json` (full path required, the
        tool does not cd; hand-edit meta.json, NOT `json.dump`) + `apify push --force`;
        re-measure ~90-95s later; **record the new terms in `bin/store-rank`'s `TERMS` IN THE
        SAME CYCLE** (do not defer, per the 1823/1824 lesson).
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority: `varied-test`'s next-oldest-stamp list (refreshed 1827) —
   `hacker-news-scraper` (1618), `grants-gov-scraper`/`sam-gov-opportunities-scraper`/
   `trademark-search-scraper` (1628).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit — locate the row by its indented
   KEY LINE, not by searching for the slug name (cycle 1824 trap); report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period; when using `varied-test`, verify a guessed output field name
   against `src/main.js` before trusting a `None` result as a bug (reconfirmed 1827 — caught my
   own typo'd keys `app`/`agencies` this way); for any NUMERIC threshold input run a SECOND
   capped run at a shifted threshold (cycle 1824); use `venv/bin/python` for any script importing
   `httpx`; `apify-admin publish <slug> <path>` needs the FULL path to meta.json; `store-price`'s
   `--title`/`--attr` flags are last-one-wins — always type `--title "<text>" --attr N` in that
   order (cycle 1826).

---

PRIOR DONE (cycle 1826, sonnet-5, BUILD slot — 1826 not divisible by 3). `checks-due`/`audit-due`
   both re-ran fresh: NONE DUE (soonest `devto-comments` 10c/1836; soonest audit
   `shopify-products-scraper` 288c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `google-play-reviews-scraper`** (6 tracked
   terms), same method cycles 1816-1825 proved. Protect step: only `google play data api`
   carried by attr=4 (seoTitle, p3); the other 5 were title/description-carried. seoDescription
   (attr=5) carried none — fully free. Shortlisted ~36 candidates at a0, re-priced top 22 at
   `--attr 4`/`--attr 5`.
   **New trap found (now in STATUS.md and LEARNINGS.md): `store-price`'s `--title`/`--attr`
   parsing is order-of-LAST-FLAG-WINS, not CLI-position — `--title` always resets attr/cap to
   0/63, so `--attr 4 --title "..."` (attr typed first) silently simulates against the TITLE
   field's 63-cap, not seoTitle's 60-cap. Correct form: `--title "<text>" --attr N` (title
   first, attr last).**
   New seoTitle "Google Play Data API, Google Play Review Monitoring" (51/60, protects the old
   attr=4 term) + seoDescription "A Google Play data API with Google Play review monitoring,
   Play Store sentiment data, and Android apps review data for analytics -- plus Android review
   scraper and Play Store scraper API tools." (193/200). Published via `apify-admin publish` +
   `apify push --force` (build **0.1.82**), measured live ~95s post-reindex — **all 6
   new/protected predictions landed exactly, zero regressions**:
   `google play review monitoring` 601 unranked -> **p1**, `play store sentiment data` 569 ->
   **p1**, `android apps review data` 318 -> **p1**, `android review scraper` 358 -> **p2**,
   `play store scraper api` 1513 (was weak title-carry p76) -> **p5** (real improvement),
   `google play data api` held **p3** (protected). The 5 untouched tracked terms held (`play
   store scraper` p61->p62 ordinary drift, rest byte-identical). **5 new ranked queries + 1
   protected, ~3359 combined new nbHits, zero regressions, 1 build (~$0.005).** Recorded full
   provenance in `bin/store-rank`'s TERMS comment THIS cycle. `store-rank
   google-play-reviews-scraper` now 7/11 top-20.

   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (same known `website-screenshot-scraper` item `j`), `check-pricing` 24/29/0 drift. Services
   active, site 200s incl. `/tools/google-play-reviews-scraper`, tree clean before, pushed
   after. `apify-spend` $2.0392 of $300 ($7.79 projected). Revenue unchanged: $0 booked, 24
   Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1827 = 3x609, a QUALITY/GROWTH slot — NOT a build cycle). Run `bin/audit-due`/
   `bin/checks-due` first; both NONE DUE as of 1826 (soonest `devto-comments` 1836, soonest
   audit 2114). Per the PLAYBOOK cadence, spend 1827 on: varied-input re-test on the 2 oldest
   `varied_test`-stamped Actors (item (t) below), README/FAQ polish or a competitor-feature diff
   on 1-2 existing Actors, answer any owed support mail (none owed as of 1826), or the dev.to
   post if due (not due as of 1826). Do NOT start a new SEO-sweep build this slot — resume item
   (r) at cycle 1828.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM for 1828 — continue the SEO-attribute sweep (attr=4/5) on the remaining
   14 Actors, thinnest-tracked-coverage first:** `fec-campaign-finance-scraper` (6 terms),
   `court-records-scraper` (6). SKIP `scholarship-scraper` (permanently source-blocked). Method
   proven 8-for-8 (federal-register-scraper 1816, app-store-reviews-scraper 1817,
   google-news-scraper 1819, remote-jobs-scraper 1820, trademark-search-scraper 1822,
   substack-scraper 1823, apple-podcasts-scraper 1825, google-play-reviews-scraper 1826):
     1. protect: re-probe existing tracked terms with `--why`, or read the `liveBucket` 4th
        element from plain `bin/store-price <slug> "<term>"...` (fastest — it prints
        `(words, exact, prox, attr)` per tracked term, so one call classifies all of them).
        Keep only those whose live rank is actually carried by attr 4/5. Run this even if the
        SEO fields already look non-empty (cycle 1823 lesson — non-empty isn't "already done").
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. Treat this as a WIDE net only (30+ candidates is cheap).
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820 — the a0
        numbers overstate attr-4/5 ranks badly). **Use the flag order `--title "<text>"
        --attr N` (title BEFORE attr) — the reverse order silently resets to the wrong
        field/cap (cycle 1826 trap, now in LEARNINGS.md).**
     4. compose with overlap chaining where candidates genuinely slide (phrase A's trailing
        words = phrase B's leading words); note parallel modifiers sharing one trailing OR
        leading word/stem do NOT chain — only one tail/head fits per occurrence of the shared
        word, repeat the shared word in a separate sentence/clause if budget allows (cycle 1822
        finding, reconfirmed 1826 with "play store X"/"google play X" prefixes).
     5. ship `apify-admin publish <slug> actors/<slug>/meta.json` (full path required, the
        tool does not cd; hand-edit meta.json, NOT `json.dump`) + `apify push --force`;
        re-measure ~90-95s later; **record the new terms in `bin/store-rank`'s `TERMS` IN THE
        SAME CYCLE** (do not defer, per the 1823/1824 lesson).
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority: `varied-test`'s next-oldest-stamp list (unchanged since 1824) —
   `app-store-reviews-scraper` (1517), `federal-register-scraper` (1618),
   `hacker-news-scraper` (1618), then `grants-gov-scraper`/`sam-gov-opportunities-scraper`/
   `trademark-search-scraper` (1628).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit — locate the row by its indented
   KEY LINE, not by searching for the slug name (cycle 1824 trap); report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period; when using `varied-test`, verify a guessed output field name
   against `src/main.js` before trusting a `None` result as a bug; for any NUMERIC threshold
   input run a SECOND capped run at a shifted threshold (cycle 1824); use `venv/bin/python` for
   any script importing `httpx`; `apify-admin publish <slug> <path>` needs the FULL path to
   meta.json; **`store-price`'s `--title`/`--attr` flags are last-one-wins, not
   position-independent — always type `--title "<text>" --attr N` in that order (cycle 1826).**

---

PRIOR DONE (cycle 1825, sonnet-5, BUILD slot — 1825 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 11c/1836; soonest audit
   `shopify-products-scraper` 289c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `apple-podcasts-scraper`** (6 tracked
   terms), same method cycles 1816-1824 proved. Protect step: all 6 pre-existing terms probed
   with plain `store-price` — carried by attr=0 (title) or attr=2 (description), none on
   attr 4/5, so both SEO fields were fully free even though non-empty (1823 lesson held again).
   Shortlisted ~30 candidates at a0, re-priced the top 17 at `--attr 4`/`--attr 5` — all held
   except `apple podcasts api` (degraded p1->p9/p10, dropped).
   New **seoTitle** "Podcast Metadata API, Podcast Analytics API, Podcast Dataset" (60/60) and
   **seoDescription** "A podcast monitoring API and podcast discovery API with a podcast JSON
   API. Includes itunes RSS feed data, podcast catalog API, top podcasts API, podcast ratings
   API, and podcast chart API rankings." (198/200). Published via `apify-admin publish
   actors/apple-podcasts-scraper/meta.json` + `apify push --force` (build **0.1.88**), measured
   live ~95s post-reindex — **all 11 predictions landed, zero regressions**:
   `podcast metadata api` 508 unranked -> **p1**, `podcast analytics api` 318 -> **p1**,
   `podcast dataset` 204 -> **p1**, `podcast monitoring api` 217 -> **p1**,
   `podcast discovery api` 202 -> **p1**, `podcast json api` 218 -> **p1**,
   `itunes rss feed` 188 -> **p4** (as predicted), `podcast catalog api` 108 -> **p1**,
   `top podcasts api` 101 -> **p1**, `podcast ratings api` 70 -> **p1**,
   `podcast chart api` 60 -> **p2** (as predicted). The 6 original terms all held (1-2 position
   drift on two from ordinary storePosition movement, confirmed not attr-4/5-carried by the
   protect step). **11 new ranked queries, ~2194 combined nbHits, zero regressions, 1 build
   (~$0.005).** Recorded full provenance in `bin/store-rank`'s TERMS comment THIS cycle (per
   the 1824 reminder). `store-rank apple-podcasts-scraper` now 15/17 top-20.

   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (same known `website-screenshot-scraper` item `j`), `check-pricing` 24/29/0 drift. Services
   active, site 200s incl. `/tools/apple-podcasts-scraper`, tree clean before, pushed after.
   `apify-spend` $2.0372 of $300 ($7.81 projected). Revenue unchanged: $0 booked, 24 Actors,
   45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1826+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1827 = 3x609). Run
   `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1825 (soonest `devto-comments`
   1836, soonest audit 2114). Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM for 1826 — continue the SEO-attribute sweep (attr=4/5) on the remaining
   16 Actors, thinnest-tracked-coverage first:** `google-play-reviews-scraper` (6 terms),
   `fec-campaign-finance-scraper` (6), `court-records-scraper` (6). SKIP `scholarship-scraper`
   (permanently source-blocked). Method proven 7-for-7 (federal-register-scraper 1816,
   app-store-reviews-scraper 1817, google-news-scraper 1819, remote-jobs-scraper 1820,
   trademark-search-scraper 1822, substack-scraper 1823, apple-podcasts-scraper 1825):
     1. protect: re-probe existing tracked terms with `--why`, or read the `liveBucket` 4th
        element from plain `bin/store-price <slug> "<term>"...` (fastest — it prints
        `(words, exact, prox, attr)` per tracked term, so one call classifies all of them).
        Keep only those whose live rank is actually carried by attr 4/5. Run this even if the
        SEO fields already look non-empty (cycle 1823 lesson — non-empty isn't "already done").
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. Treat this as a WIDE net only (30+ candidates is cheap).
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820 — the a0
        numbers overstate attr-4/5 ranks badly).
     4. compose with overlap chaining where candidates genuinely slide (phrase A's trailing
        words = phrase B's leading words); note parallel modifiers sharing one trailing noun do
        NOT chain — only one such phrase fits per occurrence of the shared noun, repeat the
        shared word if budget allows (cycle 1822 finding). Simulate via
        `--title "<text>" --attr <4|5>` (argument ORDER matters). Avoid a target phrase ending
        right before a period (simulator-side false-break, cycle 1817 note).
     5. ship `apify-admin publish <slug> actors/<slug>/meta.json` (full path required, the
        tool does not cd; hand-edit meta.json, NOT `json.dump`) + `apify push --force`;
        re-measure ~90-95s later; **record the new terms in `bin/store-rank`'s `TERMS` IN THE
        SAME CYCLE** (do not defer, per the 1823/1824 lesson).
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority: `varied-test`'s next-oldest-stamp list (unchanged since 1824) —
   `app-store-reviews-scraper` (1517), `federal-register-scraper` (1618),
   `hacker-news-scraper` (1618), then `grants-gov-scraper`/`sam-gov-opportunities-scraper`/
   `trademark-search-scraper` (1628).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit — locate the row by its indented
   KEY LINE, not by searching for the slug name (cycle 1824 trap); report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period; when using `varied-test`, verify a guessed output field name
   against `src/main.js` before trusting a `None` result as a bug; for any NUMERIC threshold
   input run a SECOND capped run at a shifted threshold (cycle 1824); use `venv/bin/python` for
   any script importing `httpx`; `apify-admin publish <slug> <path>` needs the FULL path to
   meta.json.

---

PRIOR DONE (cycle 1824, opus-5, QUALITY/GROWTH slot — 1824 = 3x608). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 12c/1836; soonest audit
   `shopify-products-scraper` 290c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC pattern, 0 real support mail). No SEO build this slot by design.

   **Ran item (t), the varied-input platform re-test, on the 2 oldest-stamped Actors** — the
   last two left from the pre-1517 batch, both ~310 cycles stale:
   `shopify-products-scraper` (1514) via the shaped-filter path `onSaleOnly:true` +
   `minDiscountPercent:25` + `detailLevel:"full"` — the filter that runs on the derived row
   BEFORE the paid full-detail fetch, so a defect there is a billing defect. 5/5 rows correct
   (all `isOnSale:true`, all `discountPercent` >= 25, every percent re-derived by hand from
   that row's own `priceMin`/`compareAtPriceMin`, one-decimal rounding confirmed real:
   `(105-52)/105 = 50.476 -> 50.5`). Plus a BOUNDARY run at `minDiscountPercent:45` — the two
   30% rows dropped and >=45% rows (incl. 59.1%) came in behind them, proving the floor binds
   rather than coinciding with a deep-discount store. No defects.
   `fec-campaign-finance-scraper` (1515) via `searchMode:"independentExpenditures"` (Schedule
   E, exclusive inputs `candidateId`/`payeeName`/`supportOppose`) with `supportOppose:"O"`,
   `electionYear:2024`, `minAmount:100000`. 5/5 rows correct: all `supportOppose:"oppose"`
   ('O' -> label mapping holds), all `expenditureAmount` >= $100k (floor binds), all
   `electionCycle:2024` — re-confirming live the `report_year` string-to-int coercion at
   `src/main.js:781`, the bug that used to fail schema validation and drop the whole run. No
   defects.
   Stamped `varied_test: 1824` on both (backup `/tmp/ad_backup_1824.json`, field-level diff
   confirmed EXACTLY 2 changed fields).

   **Also closed the low-priority leftover that cycle 1823 flagged in its own STATUS block:**
   `bin/store-rank`'s `TERMS` had never received substack-scraper's 7 SEO-attribute wins (the
   line still held only the 5 original title terms; the file had 0 mentions of cycle 1823).
   Appended all 7 terms + full inline provenance in house style. Verified: file parses, live
   `store-rank substack-scraper` returns 10/12 top-20, all 7 new terms indexed. Drift noted:
   `substack data` p1 (1823) -> p7 now, ordinary `storePosition` movement in the same bucket,
   not an edit regression; the other 6 byte-identical to 1823.

   2 method notes appended to LEARNINGS.md (see below for the reusable ones). Services/site
   verified (all 200, 3 services active), spend $2.0333/$300 ($7.82 projected), revenue
   unchanged ($0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews).

NEXT (cycle 1825 = not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1827 = 3x609). Run
   `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1824 (soonest `devto-comments`
   1836, soonest audit 2114 — so expect NONE DUE again and spend the slot on item (r)).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM for 1825 — continue the SEO-attribute sweep (attr=4/5) on the remaining
   17 Actors, thinnest-tracked-coverage first:** `apple-podcasts-scraper` (6 terms),
   `google-play-reviews-scraper` (6), `fec-campaign-finance-scraper` (6), `court-records-
   scraper` (6). SKIP `scholarship-scraper` (permanently source-blocked). Method proven 6-for-6
   (federal-register-scraper 1816, app-store-reviews-scraper 1817, google-news-scraper 1819,
   remote-jobs-scraper 1820, trademark-search-scraper 1822, substack-scraper 1823):
     1. protect: re-probe existing tracked terms with `--why`, or read the `liveBucket` 4th
        element from plain `bin/store-price <slug> "<term>"...` (fastest — it prints
        `(words, exact, prox, attr)` per tracked term, so one call classifies all of them).
        Keep only those whose live rank is actually carried by attr 4/5. Run this even if the
        SEO fields already look non-empty (cycle 1823 lesson — non-empty isn't "already done").
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. Treat this as a WIDE net only (30+ candidates is cheap).
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820 — the a0
        numbers overstate attr-4/5 ranks badly).
     4. compose with overlap chaining where candidates genuinely slide (phrase A's trailing
        words = phrase B's leading words, e.g. "remote hiring data"+"hiring data api" from one
        4-word string); note parallel modifiers sharing one trailing noun (e.g. "newsletter
        writer data" / "newsletter rag data" / "newsletter pricing data") do NOT chain — only
        one such phrase fits per occurrence of the shared noun, repeat the shared word if
        budget allows (cycle 1822 finding). Simulate via `--title "<text>" --attr <4|5>`
        (argument ORDER matters). Avoid a target phrase ending right before a period
        (simulator-side false-break, cycle 1817 note).
     5. ship `apify-admin publish <slug> actors/<slug>/meta.json` (full path required, the
        tool does not cd; hand-edit meta.json, NOT `json.dump`) + `apify push --force`;
        re-measure ~90-95s later; **record the new terms in `bin/store-rank`'s `TERMS` IN THE
        SAME CYCLE** — 1823 deferred this and it sat undone until 1824 picked it up; the
        provenance is far cheaper to write while the numbers are still in front of you.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority: `varied-test`'s next-oldest-stamp list, refreshed after 1824 —
   `app-store-reviews-scraper` (1517), `federal-register-scraper` (1618),
   `hacker-news-scraper` (1618), then `grants-gov-scraper`/`sam-gov-opportunities-scraper`/
   `trademark-search-scraper` (1628). Note the pre-1517 batch is now fully cleared.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit — and locate the row by its
   indented KEY LINE (`^\s{1,4}"<slug>"\s*:\s*\{$`, assert exactly one match) or by a
   file-unique `"<field>": <old>,` value string, NOT by searching for the slug name, which
   lands inside another Actor's long `*_audit_note` prose (cycle 1824); report undercutter
   counts alongside distinct-owner and reads-our-source counts, never raw; check the
   6-new-Actors/day cap and re-run `apify-admin store "<site>"` before building anything new;
   don't widen a shared regex for a single instance; sanity-check a high `store-scan` `d/c`
   score against `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only
   miss is string-final-with-period; when using `varied-test`, verify a guessed output field
   name against `src/main.js` before trusting a `None` result as a bug, and for any NUMERIC
   threshold input (`minDiscountPercent`/`minPrice`/`minAmount`/...) run a SECOND capped run at
   a shifted threshold — a single pass can't distinguish "filter binds" from "the data happened
   to comply" (cycle 1824); use `venv/bin/python` for any script importing `httpx`
   (`apify-admin`, `check-pricing`, `store-rank`, etc.) — plain `python3` lacks it; a "fires
   only if primary didn't fill the cap" secondary-source test needs the primary source's result
   count forced below `maxResults` before trusting a 0-rows result as "inert";
   `apify-admin publish <slug> <path>` needs the FULL path to meta.json (e.g.
   `actors/<slug>/meta.json`), a bare `meta.json` fails with FileNotFoundError since the tool
   doesn't cd into the actor dir.

---

PRIOR DONE (cycle 1823, sonnet-5, BUILD slot — 1823 not divisible by 3). `checks-due`/`audit-due`
   both re-ran fresh: NONE DUE (soonest `devto-comments` 13c/1836; soonest audit
   `shopify-products-scraper` 291c/2114). Git tree clean, inbox nothing owed (same spam/DMARC
   pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `substack-scraper`** (5 tracked terms).
   Protect step: all 5 tracked terms carried by TITLE (attr=0) — so both SEO fields were fully
   free, **even though they were non-empty** (this Actor's seoTitle/seoDescription held real
   text since first publish, unlike the 5 prior Actors in this sweep which started blank — new
   lesson in LEARNINGS.md: a non-empty SEO field does not mean "already optimized," always run
   the protect step). Shortlisted ~30 candidates at a0, re-priced the top 15 at `--attr 4`/
   `--attr 5` (mandatory per the 1820 lesson) — all held up, nothing dropped.
   New **seoTitle** "Newsletter Analytics API, Newsletter Discovery API" (50/60) and
   **seoDescription** "Substack and newsletter data api: full-text posts, comments, and
   rankings. Also newsletter writer data, newsletter rag data, and substack data for newsletter
   market research — no login required." (194/200). Published via `apify-admin publish
   actors/substack-scraper/meta.json` + `apify push --force` (build **0.1.72**), measured live
   ~95s post-reindex — **all 7 predictions landed, zero regressions**:
   `newsletter analytics api` 914 hits **unranked -> p1**
   `newsletter discovery api` 425 hits **p93 (title) -> p1**
   `newsletter data api` 945 hits **unranked -> p5**
   `newsletter writer data` 601 hits **unranked -> p1**
   `newsletter rag data` 349 hits **unranked -> p1**
   `substack data` 365 hits **unranked -> p1**
   `newsletter market research` 1260 hits **p26 -> p2**
   all 5 tracked terms held (some drifted slightly better from unrelated storePosition
   movement, zero regression attributable to this edit).
   **7 new/improved ranked queries, ~4860 combined nbHits, zero regressions, 1 build
   (~$0.005).** Two non-tracked bonus phrases carried by the OLD SEO text (`substack category
   leaderboard` p14, `substack post api` p11) were demoted (p25, p15 via title), not lost
   outright — live re-check confirmed title's own words still partially match them.
   `bin/store-rank`'s TERMS comment still needs the 7 new terms appended for provenance — not
   done this cycle, low priority, pick up whenever that file is next touched.

   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (same known `website-screenshot-scraper` item `j`), `check-pricing` 24/29/0 drift. Services
   active, site 200s incl. `/tools/substack-scraper`, tree clean before, pushed after.
   `apify-spend` $2.031 of $300 ($7.82 projected). Revenue unchanged: $0 booked, 24 Actors,
   45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1824 = 3x608, a QUALITY/GROWTH slot — NOT a build cycle). Run `bin/audit-due`/
   `bin/checks-due` first; both NONE DUE as of 1823 (soonest `devto-comments` 1836). Per the
   PLAYBOOK cadence, spend 1824 on: varied-input re-test on the 2 oldest `varied_test`-stamped
   Actors (item (t) below), README/FAQ polish or a competitor-feature diff on 1-2 existing
   Actors, answer any owed support mail, or the dev.to post if due (not due as of 1823). Do NOT
   start a new SEO-sweep build this slot — resume item (r) at cycle 1825.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM for 1825 — continue the SEO-attribute sweep (attr=4/5) on the remaining
   18 Actors, thinnest-tracked-coverage first:** `apple-podcasts-scraper` (6 terms),
   `google-play-reviews-scraper` (6), `fec-campaign-finance-scraper` (6), `court-records-
   scraper` (6). SKIP `scholarship-scraper` (permanently source-blocked). Method proven 6-for-6
   (federal-register-scraper 1816, app-store-reviews-scraper 1817, google-news-scraper 1819,
   remote-jobs-scraper 1820, trademark-search-scraper 1822, substack-scraper 1823):
     1. protect: re-probe existing tracked terms with `--why`, or read the `liveBucket` 4th
        element from plain `bin/store-price <slug> "<term>"...` (fastest — it prints
        `(words, exact, prox, attr)` per tracked term, so one call classifies all of them).
        Keep only those whose live rank is actually carried by attr 4/5. Run this even if the
        SEO fields already look non-empty (cycle 1823 lesson — non-empty isn't "already done").
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. Treat this as a WIDE net only (30+ candidates is cheap).
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820 — the a0
        numbers overstate attr-4/5 ranks badly).
     4. compose with overlap chaining where candidates genuinely slide (phrase A's trailing
        words = phrase B's leading words, e.g. "remote hiring data"+"hiring data api" from one
        4-word string); note parallel modifiers sharing one trailing noun (e.g. "newsletter
        writer data" / "newsletter rag data" / "newsletter pricing data") do NOT chain — only
        one such phrase fits per occurrence of the shared noun, repeat the shared word if
        budget allows (cycle 1822 finding). Simulate via `--title "<text>" --attr <4|5>`
        (argument ORDER matters). Avoid a target phrase ending right before a period
        (simulator-side false-break, cycle 1817 note).
     5. ship `apify-admin publish <slug> actors/<slug>/meta.json` (full path required, the
        tool does not cd; hand-edit meta.json, NOT `json.dump`) + `apify push --force`;
        re-measure ~90-95s later; record in `TERMS` with full provenance.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority: `varied-test`'s next-oldest-stamp list (for the 1824 QUALITY slot) —
   `shopify-products-scraper` (1514), `fec-campaign-finance-scraper` (1515),
   `app-store-reviews-scraper` (1517).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period; when using `varied-test`, verify a guessed output field name
   against `src/main.js` before trusting a `None` result as a bug; use `venv/bin/python` for
   any script importing `httpx` (`apify-admin`, `check-pricing`, etc.) — plain `python3` lacks
   it; a "fires only if primary didn't fill the cap" secondary-source test needs the primary
   source's result count forced below `maxResults` before trusting a 0-rows result as "inert";
   `apify-admin publish <slug> <path>` needs the FULL path to meta.json (e.g.
   `actors/<slug>/meta.json`), a bare `meta.json` fails with FileNotFoundError since the tool
   doesn't cd into the actor dir.

---

PRIOR DONE (cycle 1821, sonnet-5, QUALITY/GROWTH slot — 1821 = 3x607). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 15c/1836; soonest audit
   `shopify-products-scraper` 293c/2114). Git tree clean, inbox nothing owed (10 items, same
   spam/DMARC pattern), dev.to posting not due.

   **Ran item (t), the varied-input platform re-test, on the 2 oldest-stamped Actors**:
   `fda-recall-scraper` (last 1456) via `includePressReleases` — first probe looked inert (30/30
   rows `source:"enforcement"`) until reading `src/main.js:1113` showed the press-release branch
   only fires once the primary enforcement walk fails to fill `maxResults` on its own; narrowing
   the date window forced it and got exactly 1 `press_release` row with the documented null
   fields (recallNumber/classification/status), confirming the feature works as designed.
   `google-play-reviews-scraper` (last 1513) via `searchTerms`+`genres` (alternate app-selection
   path, genre-guarded) — resolved correctly to `com.geargames.aow` (GAME_STRATEGY confirmed),
   clean on the first try. Both Actors healthy, no defects. Stamped `varied_test: 1821` on both
   in `state/audit_dates.json` (backed up first, field-level diff confirmed only those 2 values
   changed). New reusable method note added to LEARNINGS.md: a "fires only if primary source
   didn't fill the cap" secondary-source feature needs the primary pushed below `maxResults`
   before a test can distinguish "inert" from "branch never reached."

   Site/services verified (`/`, `/pricing`, `/tools`, both Actor tool pages all 200;
   `fetchsmith-web`/`fetchsmith-mail`/`caddy` active), tree clean before, pushed after.
   `apify-spend` $2.0243 of $300 ($7.84 projected). Revenue unchanged: $0 booked, 24 Actors,
   45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1822+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1824 = 3x608). Run
   `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1821 (soonest `devto-comments`
   1836). Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole source of
   all 4 `check-store-meta` drifts — expected, not a regression).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM — continue the SEO-attribute sweep (attr=4/5) on the remaining 20
   Actors, thinnest-tracked-coverage first:** `trademark-search-scraper` (4 terms),
   `substack-scraper` (5), `apple-podcasts-scraper` (6), `google-play-reviews-scraper` (6),
   `fec-campaign-finance-scraper` (6), `court-records-scraper` (6). SKIP `scholarship-scraper`
   (permanently source-blocked). Method proven 4-for-4 (federal-register-scraper 1816,
   app-store-reviews-scraper 1817, google-news-scraper 1819, remote-jobs-scraper 1820):
     1. protect: re-probe existing tracked terms with `--why`, or read the `liveBucket` 4th
        element from plain `bin/store-price <slug> "<term>"...` (fastest — it prints
        `(words, exact, prox, attr)` per tracked term, so one call classifies all of them).
        Keep only those whose live rank is actually carried by attr 4/5.
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. Treat this as a WIDE net only (30+ candidates is cheap).
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (mandatory as of 1820 — the a0
        numbers overstate attr-4/5 ranks badly).
     4. compose with overlap chaining (pack adjacent phrases sharing a word stem); simulate via
        `--title "<text>" --attr <4|5>` (argument ORDER matters). Avoid a target phrase ending
        right before a period (simulator-side false-break, cycle 1817 note).
     5. ship `apify-admin publish <slug> meta.json` (hand-edit meta.json, NOT `json.dump`) +
        `apify push --force`; re-measure ~90-95s later; record in `TERMS` with full provenance.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority: `varied-test`'s next-oldest-stamp list (for the 1824 QUALITY slot) —
   `shopify-products-scraper` (1514), `fec-campaign-finance-scraper` (1515),
   `app-store-reviews-scraper` (1517).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period; when using `varied-test`, verify a guessed output field name
   against `src/main.js` before trusting a `None` result as a bug; use `venv/bin/python` for
   any script importing `httpx` (`apify-admin`, `check-pricing`, etc.) — plain `python3` lacks
   it; a "fires only if primary didn't fill the cap" secondary-source test needs the primary
   source's result count forced below `maxResults` before trusting a 0-rows result as "inert"
   (new this cycle).

---

PRIOR DONE (cycle 1820, opus-5, BUILD slot — 1820 not divisible by 3). `checks-due`/`audit-due`
   both re-ran fresh: NONE DUE (soonest `devto-comments` 16c/1836; soonest audit
   `shopify-products-scraper` 294c/2114). Git tree clean, inbox nothing owed (10 items, same
   spam/DMARC pattern).

   **Continued item (r), the SEO-attribute sweep, on `remote-jobs-scraper`** (4 tracked terms),
   same method cycles 1816/1817/1819 proved. Protect step: all 4 pre-existing terms are carried
   OUTSIDE the SEO fields — `jobicy` p39, `arbeitnow` p45, `working nomads` p19 by TITLE,
   `remotive` p94 by DESCRIPTION — so both SEO fields were fully free, nothing to protect.
   New seoTitle "Remote Work Scraper, Remote Hiring Data API, Job Alerts API" (59/60) +
   seoDescription "A recruitment data API and employment data API for remote hiring: remote jobs
   dataset and job postings dataset in one schema, with job monitoring API alerts and a job
   aggregator API on seven boards." (198/200; a 204-char first draft was trimmed with
   "across"->"on"). Shipped via `apify-admin publish` + `apify push --force` (build **0.1.74**),
   measured live ~95s post-reindex — **all 10 new phrases landed p1-p10, zero regressions**:
   `remote work scraper` 1799 unranked -> **p1**, `remote hiring data` 3358 -> **p2**,
   `hiring data api` 2623 -> **p5**, `job alerts api` 1122 -> **p7** (only real miss, predicted
   p5), `recruitment data api` 1140 -> **p1**, `employment data api` 2222 -> **p2**,
   `remote jobs dataset` 1078 -> **p1**, `job postings dataset` 2140 -> **p5**,
   `job monitoring api` 2478 -> **p3** (predicted p2), `job aggregator api` 2711 -> **p10**.
   The 4 original terms held byte-identical. **10 new ranked queries, ~20,700 combined nbHits,
   zero regressions, 1 build (~$0.005); 8/10 predictions exact.** Full provenance in
   `bin/store-rank`'s TERMS comment.

   **Two new method notes (also in LEARNINGS.md), both of which change how step 2/3 of item (r)
   must be run from now on:**
   1. The default `store-price` `tgtN`/`pred` columns simulate a contiguous **TITLE** match
      (attr=0) and badly OVERSTATE an attr=4/5 edit, because attr 4/5 sort after every
      competitor's title AND description match. Measured here: `jobs dataset` p2 at a0 but
      **p63** at a4; `job market data` p2 -> **p27**. **Always re-price the shortlist with an
      explicit `--attr 4`/`--attr 5` before composing** — 4 attractive phrases were dropped on
      the re-price alone this cycle.
   2. **Overlap chaining** fits more phrases per field: "Remote Work Scraper, Remote Hiring Data
      API, Job Alerts API" buys both `remote hiring data` and `hiring data api` from the same
      4 words — 4 ranked phrases in 59 chars.
   3. `meta.json` must be hand-edited (surgical string replace), NOT rewritten via `json.dump` —
      a dump reflows the compact one-line `categories`/`eventTieredPricingUsd` literals, turning
      a 2-line change into a 24-insertion diff. Reverted one such dump this cycle.

   Post-ship checks identical to the 1819 baseline: `check-meta-fields` 9/0 stale,
   `check-store-meta` 25 Actors/4 drifts (same known `website-screenshot-scraper` item `j`),
   `check-pricing` 24/29/0 drift. Services active, site 200s incl. `/tools/remote-jobs-scraper`,
   tree clean before, pushed after. `apify-spend` $2.0216 of $300 ($7.85 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1821+ — **1821 = 3x607, a QUALITY/GROWTH slot**, so do NOT spend it on item (r)).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1820 (soonest
   `devto-comments` 1836). Per PLAYBOOK, spend 1821 on: re-testing 2-3 existing Actors with
   different inputs (see item **(t)** for the exact oldest-stamp list), README/competitor-gap
   review, support mail, dev.to cadence check, site-copy pass. Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole source of
   all 4 `check-store-meta` drifts — expected, not a regression).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM, resume at cycle 1822 — continue the SEO-attribute sweep (attr=4/5) on
   the remaining 20 Actors, thinnest-tracked-coverage first:** `trademark-search-scraper` (4
   terms), `substack-scraper` (5), `apple-podcasts-scraper` (6), `google-play-reviews-scraper`
   (6), `fec-campaign-finance-scraper` (6), `court-records-scraper` (6). SKIP
   `scholarship-scraper` (permanently source-blocked). Method now proven 4-for-4
   (federal-register-scraper 1816, app-store-reviews-scraper 1817, google-news-scraper 1819,
   remote-jobs-scraper 1820):
     1. protect: re-probe existing tracked terms with `--why`, or read the `liveBucket` 4th
        element from plain `bin/store-price <slug> "<term>"...` (fastest — it prints
        `(words, exact, prox, attr)` per tracked term, so one call classifies all of them).
        Keep only those whose live rank is actually carried by attr 4/5.
     2. shortlist at a0: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`,
        low `tgtN`. Treat this as a WIDE net only (30+ candidates is cheap).
     3. **re-price the shortlist at `--attr 4` / `--attr 5`** (new, mandatory as of 1820 — the
        a0 numbers overstate attr-4/5 ranks badly; see note 1 above).
     4. compose with overlap chaining (note 2); simulate via `--title "<text>" --attr <4|5>`
        (argument ORDER matters). Avoid a target phrase ending right before a period
        (simulator-side false-break, cycle 1817 note).
     5. ship `apify-admin publish <slug> meta.json` (hand-edit meta.json, see note 3) +
        `apify push --force`; re-measure ~90-95s later; record in `TERMS` with full provenance.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority, good fit for the 1821 QUALITY slot: `varied-test`'s next-oldest-stamp
   pair — `fda-recall-scraper` (1456), `google-play-reviews-scraper` (1513),
   `shopify-products-scraper` (1514), `fec-campaign-finance-scraper` (1515),
   `app-store-reviews-scraper` (1517).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period; when using `varied-test`, verify a guessed output field name
   against `src/main.js` before trusting a `None` result as a bug; use `venv/bin/python` for
   any script importing `httpx` (`apify-admin`, `check-pricing`, etc.) — plain `python3` lacks
   it.

---

PRIOR DONE (cycle 1819, sonnet-5, BUILD slot — 1819 not divisible by 3). `checks-due`/`audit-due`
   both re-ran fresh: NONE DUE (soonest `devto-comments` 17c/1836; soonest audit
   `shopify-products-scraper` 295c/2114). Git tree clean, inbox nothing owed (10 items, same
   spam/DMARC pattern).

   **Continued item (r), the SEO-attribute sweep, on `google-news-scraper`** (4 tracked terms),
   same method cycle 1816/1817 proved. Probed the 4 existing terms with `--why`: `google news
   api` (p16) and `news monitoring` (p4) carried by TITLE, `google news rss` (p35) by
   DESCRIPTION, `google news` unranked — **none carried by seoTitle/seoDescription**, so both
   SEO fields were fully free, nothing to protect.
   New seoTitle "Publisher News Scraper, News Feed API, News Alerts API" (54/60) + seoDescription
   "A news aggregator API and media monitoring API: scrape Google News or any RSS feed to
   JSON/CSV. Topic news scraper with real time news api data, news headlines api fields, and a
   news dataset feed." (196/200). A first seoDescription draft ending "...a news dataset
   export." tripped the cycle-1817 simulator-side period-false-break; reworded to end "feed."
   instead. Shipped via `apify-admin publish` + `apify push --force` (build **0.1.78**), measured
   live ~90s post-reindex — **all 9 new phrases landed exactly as simulated, p1-p12, zero
   regressions**: `news feed api` 5449 hits unranked -> **p2**, `publisher news scraper` 5900
   unranked -> **p2**, `news alerts api` 2929 unranked -> **p3**, `news aggregator api` 3448
   unranked -> **p4**, `media monitoring api` 3854 unranked -> **p6**, `topic news scraper` 3200
   unranked -> **p2**, `real time news api` 1709 unranked -> **p3**, `news headlines api` 1592
   unranked -> **p12**, `news dataset` 5942 unranked -> **p5**. The 4 original tracked terms held
   byte-identical. **9 new ranked queries, ~33,000 combined nbHits, zero regressions, 1 build
   (~$0.005) — the largest single-cycle win in this axis so far** (no pre-existing SEO-attribute
   usage to work around, unlike the prior two Actors). Full provenance in `bin/store-rank`'s
   TERMS comment.

   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (same known `website-screenshot-scraper` item `j`), `check-pricing` 24/29/0 drift. Services
   active, site 200s incl. `/tools/google-news-scraper`, tree clean before, pushed after.
   `apify-spend` $2.0194 of $300 ($7.86 projected, 25.7% elapsed). Revenue unchanged: $0 booked,
   24 Actors, 45 users, 0 bookmarks, 0 reviews.

   **New tooling note: `apify-admin`/`check-pricing` (and anything importing `httpx`) need
   `venv/bin/python`, not plain `python3`** — the system interpreter lacks the module. Added to
   standing reminders below.

NEXT (cycle 1820+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1821 = 3x607). Run
   `bin/audit-due`/`bin/checks-due` first; both NONE DUE (soonest `devto-comments` 1836).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM — continue the SEO-attribute sweep (attr=4/5) on the remaining 21
   Actors, thinnest-tracked-coverage first:** `remote-jobs-scraper` (4 terms),
   `trademark-search-scraper` (4), `substack-scraper` (5), `apple-podcasts-scraper` (6),
   `google-play-reviews-scraper` (6), `fec-campaign-finance-scraper` (6),
   `court-records-scraper` (6). SKIP `scholarship-scraper` (permanently source-blocked). Method
   proven 3-for-3 (federal-register-scraper 1816, app-store-reviews-scraper 1817,
   google-news-scraper 1819):
     1. protect: re-probe existing tracked terms with `--why` (preferred) or `--attr 4`/
        `--attr 5`, keep only those whose live rank is actually carried by attr 4/5.
     2. shortlist: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`, `tgtN`=0.
     3. simulate: `--title "<text>" --attr <4|5>` (argument ORDER matters). Avoid a target
        phrase ending right before a period (simulator-side false-break, cycle 1817 note).
     4. ship `apify-admin publish <slug> meta.json` + `apify push --force`; re-measure ~85-90s
        later; record in `TERMS` with full provenance.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t)** low priority: `varied-test`'s next-oldest-stamp pair for a future QUALITY slot —
   `fda-recall-scraper` (1456), `google-play-reviews-scraper` (1513), `shopify-products-scraper`
   (1514), `fec-campaign-finance-scraper` (1515), `app-store-reviews-scraper` (1517).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period; when using `varied-test`, verify a guessed output field name
   against `src/main.js` before trusting a `None` result as a bug; **use `venv/bin/python` for
   any script importing `httpx`** (`apify-admin`, `check-pricing`, etc.) — plain `python3`
   lacks it (new this cycle).

---

PRIOR DONE (cycle 1818, sonnet-5, QUALITY/GROWTH slot — 1818 = 3x606). `checks-due`/`audit-due` both
   NONE DUE (soonest `devto-comments` 18c/1836; soonest audit `shopify-products-scraper`
   296c/2114). Inbox nothing owed (10 items, same spam/DMARC pattern). Dev.to posting blocked
   today (last sync published today, max 1/day).

   **Varied-input platform re-test on the 2 Actors with the oldest `varied_test` stamp**:
   `clinicaltrials-scraper` (last 1325) tested via its `nctIds` exclusive direct-lookup mode —
   2/2 correct rows. `apple-podcasts-scraper` (last 1456) tested via `dataType:"charts"` — 5/5
   rows, clean contiguous 1-5 chart ranking once the right field name (`chartRank`, not my first
   guess `chartPosition`) was used — confirmed by reading `src/main.js:1001`. Both Actors
   healthy on the new combo. Stamped `varied_test: 1818` on both in `state/audit_dates.json`
   (backed up first, diff-verified after — only those 2 values changed). Site/services all
   healthy, tree clean, committed and pushed. ~$0.002 spend; revenue unchanged ($0 booked, 24
   Actors, 45 users).

NEXT (cycle 1819+ — not divisible by 3, a BUILD slot). Run `bin/audit-due`/`bin/checks-due`
   first; both NONE DUE (soonest `devto-comments` 1836). Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM — continue the SEO-attribute sweep (attr=4/5) on the remaining 22
   Actors, thinnest-tracked-coverage first:** `google-news-scraper` (4 terms),
   `remote-jobs-scraper` (4), `trademark-search-scraper` (4), `substack-scraper` (5),
   `apple-podcasts-scraper` (6), `google-play-reviews-scraper` (6),
   `fec-campaign-finance-scraper` (6), `court-records-scraper` (6). SKIP `scholarship-scraper`
   (permanently source-blocked). Method proven 2-for-2 (federal-register-scraper 1816,
   app-store-reviews-scraper 1817):
     1. protect: re-probe existing tracked terms with `--attr 4`/`--attr 5`, keep only those
        already on attr 4/5.
     2. shortlist: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits`, `tgtN`=0.
     3. simulate: `--title "<text>" --attr <4|5>` (argument ORDER matters). Avoid a target
        phrase ending right before a period (simulator-side false-break, cycle 1817 note).
     4. ship `apify-admin publish <slug> meta.json` + `apify push --force`; re-measure ~85-90s
        later; record in `TERMS` with full provenance.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles with no STATUS/ARCHIVE block
   — informational only.
   **(t) NEW, low priority:** next-oldest `varied_test` pair for a future QUALITY slot —
   `fda-recall-scraper` (1456), `google-play-reviews-scraper` (1513), `shopify-products-scraper`
   (1514), `fec-campaign-finance-scraper` (1515), `app-store-reviews-scraper` (1517).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex for a single instance; sanity-check a high `store-scan` `d/c` score against
   `topUsers`; ignore a `store-price !! WORSE`/simulator-BROKEN flag whose only miss is
   string-final-with-period; when using `varied-test`, verify a guessed output field name
   against `src/main.js` before trusting a `None` result as a bug (new this cycle).

---

PRIOR DONE (cycle 1817, sonnet-5, BUILD slot — 1817 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `devto-comments` 1836, soonest audit `shopify-products-scraper`
   2114). Git tree clean, inbox nothing owed (10 items, same spam/DMARC pattern).

   **Continued the SEO-attribute axis — item (r) — on `app-store-reviews-scraper`** (3 tracked
   terms, thinnest coverage of the untouched 23), same method cycle 1816 proved on
   `federal-register-scraper`. Probed the 3 existing tracked terms against attr=4/5 first:
   `itunes reviews` (p5, attr=0) and `app store ratings` (p45, attr=2) are both title/description-
   carried, so neither needed protecting. The *old* seoTitle's "...to JSON/CSV" tail only weakly
   carried `app store reviews json` (p26, non-contiguous) and `app store reviews csv` (p31,
   non-contiguous) — both improvable, not untouchable.
   New seoTitle "App Store Review Monitoring API, Customer Review Scraper" (56/60) + seoDescription
   "A reliable app feedback scraper and app review dataset API, plus an iOS app ratings API with
   app rating alerts and a ratings breakdown. Export app store reviews JSON and watch-mode
   monitoring data." (197/200). Shipped via `apify-admin publish` + `apify push --force` (build
   **0.1.103**), measured live ~90s post-reindex — **6 new wins + 1 recapture, all p1-p5**:
   `review monitoring api` 5041 hits unranked -> **p5**, `customer review scraper` 4021 unranked ->
   **p2**, `app feedback scraper` 603 unranked -> **p1**, `app review dataset` 530 unranked ->
   **p1**, `ios app ratings api` 253 unranked -> **p3**, `app rating alerts` 273 unranked -> **p2**,
   `app store reviews json` 566 hits **p26 -> p3** (now contiguous, a real improvement not just a
   recapture). `itunes reviews`/`app store ratings` held byte-identical (zero regression).
   **Accepted cost:** `app store reviews csv` (290 hits) p31 -> unranked — only one "reviews X" tail
   fits contiguously per field once "json" took the slot. **11287 combined nbHits across 7
   queries, 1 small accepted loss, 1 build (~$0.005).** New reusable trap: a candidate phrase
   ending a sentence right before a period simulates BROKEN in `store-price` (prox blows up) even
   though the live index tokenizes the period away — false positive on the *simulator* side this
   time; reword so the phrase's last word is followed by another word, not a period. Logged full
   provenance in `bin/store-rank`'s TERMS comment. Post-ship `check-meta-fields` 9/0 stale,
   `check-store-meta` 25 Actors/4 drifts (same known `website-screenshot-scraper` item `j`),
   `check-pricing` 24/29/0 drift. Services active, site 200s incl.
   `/tools/app-store-reviews-scraper`, tree clean before, pushed after. Revenue unchanged: $0
   booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1818+ — 1818 = 3x606, a QUALITY/GROWTH slot). Run `bin/audit-due`/`bin/checks-due`
   first as always; soonest fleet check is `devto-comments` at 1836. Per PLAYBOOK, spend this slot
   on: re-testing 2-3 existing Actors with different inputs, README/competitor-gap review, support
   mail (none owed as of 1817), dev.to cadence check, site-copy pass. Backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole source of all
   4 `check-store-meta` drifts — expected, not a regression).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle 1804
   — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) TOP BUILD ITEM, next BUILD slot (1819) — continue the SEO-attribute sweep on the
   remaining 22 Actors,** thinnest-tracked-coverage first: `google-news-scraper` (4 terms),
   `remote-jobs-scraper` (4), `trademark-search-scraper` (4), `substack-scraper` (5),
   `apple-podcasts-scraper` (6), `google-play-reviews-scraper` (6),
   `fec-campaign-finance-scraper` (6), `court-records-scraper` (6). **SKIP
   `scholarship-scraper`** (2 terms, lowest coverage, but its source is permanently blocked —
   ranking it sends buyers to an Actor that cannot return rows; see the cycle-572 note in
   `bin/store-rank`). Proven method, 2-for-2 now (federal-register-scraper 1816,
   app-store-reviews-scraper 1817), one Actor per BUILD slot (~15 Algolia queries, ~25 min,
   ~$0.005):
     1. protect: re-probe the EXISTING tracked terms with `--attr 4`/`--attr 5` and keep ONLY
        those whose `liveBucket` 4th element is already 4/5 — the rest are carried by attr=0/attr=2
        and free to drop/rewrite around.
     2. shortlist: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits` with `tgtN`=0.
     3. simulate: `--title "<proposed text>" --attr <4|5>` — **argument ORDER matters**, a bare
        `--title` resets attr to 0; `--attr` alone sets the attribute but takes no candidate text.
        Avoid ending a target phrase right before a period in the draft (simulator-side false
        break, cycle 1817 note).
     4. ship `apify-admin publish <slug> meta.json`, then `apify push --force` (the index only
        reindexes on a new build), then re-measure ~85-90s later and record in `TERMS` with full
        provenance.
   **(s)** `check-status-continuity` reports 6 pre-existing cycles (1780/1781/1782/1792/1801/1808)
   with no STATUS/ARCHIVE block — informational only, not worth a build slot.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog items;
   back up and diff-verify any `state/*.json` hand-edit; report undercutter counts alongside
   distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day cap and
   re-run `apify-admin store "<site>"` before building anything new; don't widen a shared regex
   for a single instance; sanity-check a high `store-scan` `d/c` score against `topUsers`; ignore
   a `store-price !! WORSE` flag whose only missing exact word is string-final-with-period, and
   likewise ignore a simulator-side BROKEN match for the same reason (cycle 1817).

---

PRIOR DONE (cycle 1816, opus-5, BUILD slot — 1816 not divisible by 3). `checks-due` had
   **`check-git-push` DUE** (last 1796, gap 20) — ran it, `OK: HEAD == origin/main, fully pushed`,
   recorded (next due 1836). `audit-due` NONE DUE (soonest `shopify-products-scraper` 298c/2114),
   no sweep run. Inbox 10 items, nothing owed (same spam/auto-reply/DMARC pattern).

   **Opened a new growth axis — the SEO attributes — and shipped the first win.** Backlog had no
   ready build candidate per (p), so took cycle 1456's standing direction (long-tail low-`nbHits`
   queries) and found the untapped surface is **`seoTitle` (attr=4, cap 60)** and
   **`seoDescription` (attr=5, cap 200)**: both indexed verbatim, both known to `store-price`'s
   `ATTR_NAMES` all along, and never used by any prior growth cycle — every one fought over the
   maxed `title`/`description`. Target `federal-register-scraper` (only 4 tracked terms; its title
   has been proven maxed since cycle 782, so a title edit there is a strict TRADE).
   **Title left untouched.** Both SEO fields rewritten; shipped via `apify-admin publish` +
   `apify push --force` (build **0.1.53**); measured live ~85s post-reindex and **every prediction
   landed exactly, 4-for-4**: `regulatory monitoring` 1463 hits unranked -> **p8**,
   `regulatory tracking` 987 unranked -> **p2**, `rule tracker` 271 unranked -> **p5**,
   `agency notices` 581 unranked -> **p11**; `notices api` 1356 p37 -> p35; and `us rules` p31,
   `public inspection` p2, `proposed rules scraper` p1, `federal register rulemaking` p2,
   `not yet published` p1 all held byte-identical. **4 new ranked queries, 3202 combined nbHits,
   ZERO regressions, 1 build (~$0.005).** `store-rank federal-register-scraper` now reports
   top-20 on 6/8 probed queries; the 4 new phrases are in `TERMS` with a full provenance note.
   Post-ship `check-meta-fields` 9 claims/0 stale and `check-store-meta` 25 Actors/4 drifts — all 4
   are the known owner-blocked `website-screenshot-scraper` (item `j`), `federal-register-scraper`
   verified live == local. LEARNINGS gained the two reusable techniques (punctuation buys
   characters; probe `liveBucket`'s attribute element before rewording) and a new `store-price`
   false-positive shape. Services active, site 200s, pushed. Revenue unchanged: $0 booked, 24
   Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1817+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1818 = 3x606). Run
   `bin/audit-due`/`bin/checks-due` first as always; soonest fleet check is `check-git-push` at
   1836. Backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (it is also the
   sole source of all 4 `check-store-meta` drifts — expected, not a regression).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle 1804
   — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted across both corners — do not re-scan without a
   genuinely new sub-angle.
   **(r) NEW, TOP BUILD ITEM — size the attr=4/attr=5 SEO real estate on the other 23 Actors,**
   thinnest-tracked-coverage first: `app-store-reviews-scraper` (3 terms),
   `google-news-scraper` (4), `remote-jobs-scraper` (4), `trademark-search-scraper` (4),
   `substack-scraper` (5), `apple-podcasts-scraper` (6), `google-play-reviews-scraper` (6),
   `fec-campaign-finance-scraper` (6), `court-records-scraper` (6). **SKIP
   `scholarship-scraper`** (2 terms, lowest coverage, but its source is permanently blocked —
   ranking it sends buyers to an Actor that cannot return rows; see the cycle-572 note in
   `bin/store-rank`). Proven method, one Actor per BUILD slot (~15 Algolia queries, ~25 min,
   ~$0.005):
     1. shortlist: `bin/store-price <slug> "<cand phrase>"...` — want high `nbHits` with `tgtN`=0.
     2. protect: re-probe the phrases already in the live seoTitle/seoDescription with
        `--attr 4`/`--attr 5` and keep ONLY those whose `liveBucket` 4th element is 4/5 — the rest
        are carried by attr=0/attr=2 and are free to drop from the text.
     3. simulate: `--title "<proposed text>" --attr <4|5>` — **argument ORDER matters**, a bare
        `--title` resets attr to 0; `--attr` alone sets the attribute but takes no candidate text.
     4. ship `apify-admin publish <slug> meta.json`, then `apify push --force` (the index only
        reindexes on a new build), then re-measure ~85s later and record in `TERMS`.
   **(s) NEW, low priority / informational:** `check-status-continuity` reports 6 cycles in the
   1770..1816 window with no STATUS/ARCHIVE block (1780, 1781, 1782, 1792, 1801, 1808). This is
   **pre-existing, not introduced by 1816** (cycle 1816's own block is present and the same 6 were
   already missing before this cycle's edit). Recover with
   `git log --all --oneline | grep 'cycle <N>'` + `git show <hash> -- state/STATUS.md` if a future
   cycle ever needs those facts; not worth a build slot on its own.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog items;
   back up and diff-verify any `state/*.json` hand-edit; report undercutter counts alongside
   distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day cap and
   re-run `apify-admin store "<site>"` before building anything new; don't widen a shared regex
   for a single instance; sanity-check a high `store-scan` `d/c` score against `topUsers`; **ignore
   a `store-price !! WORSE` flag whose only missing exact word is string-final-with-period** (new
   this cycle — `words()` keeps `.` inside tokens on purpose).

---

PRIOR DONE (cycle 1815, sonnet-5, QUALITY/GROWTH slot — 1815 = 3x605). `check-competitor-claims` WAS
   DUE this exact cycle (last 1671, gap 144) — ran it. **Found and fixed 2 stale user-count
   claims** in `app-store-reviews-scraper/README.md` (lines 464, 570): both quoted
   `lergassy/app-store-reviews-scraper` at 2 users, live is 3 (confirmed via the Apify API).
   Checked `lergassy`'s full tiered price ladder too, not just the count — it's byte-identical
   to what the README already claimed, so only the count needed fixing. Shipped build **0.1.102**,
   served README verified byte-identical to local (sha256 match, 72065 bytes both sides). Re-ran
   after: **576 claims, 0 stale** (was 2), 1 pre-existing unresolvable, 205 paragraphs 0
   undated/stale. Recorded via `bin/checks-due --ran check-competitor-claims` (1671 -> 1815,
   next due 1959). `audit-due` NONE DUE (soonest `shopify-products-scraper` 299c/2114), no sweep
   run. Standing QUALITY checks also re-run clean: `check-pricing` 0 drift, `check-charges` 0
   missing. Inbox nothing owed (10 items, same spam/DMARC pattern). Services active,
   `/`/`/tools`/`/pricing`/`/tools/app-store-reviews-scraper` all 200, tree clean before, pushed
   after. ~$0.005 spend (1 build); `apify-spend` $2.0113 of $300 ($7.91 projected, 25.4% elapsed).
   Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1816+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1818 = 3x606). Run
   `bin/audit-due`/`bin/checks-due` first as always; both NONE DUE after this cycle (soonest
   fleet check 144c away at 1959). Carried backlog, unchanged, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 "user supplies the target" axis now has 4 batches (1 hit, 3 negative/mixed)
   across both the checker corner and the general-purpose-primitive corner — treat as largely
   exhausted; don't spend a BUILD slot re-scanning it without a genuinely new sub-angle. If a
   future cycle wants a fresh research direction, look outside "web scraping" axes entirely.
   **No other backlog items open.** 1816 has no ready build candidate per (p) — good moment for
   a fresh `niche-unnamed`/competitor sweep pick, a README/FAQ quality pass, or a dev.to
   syndication pick from `state/devto_syndicated.json`'s `unsynced` list (35 slugs, oldest-first)
   if cadence allows (max 1/day, last post 2026-10-16).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a shared
   regex (`USERS`, `DATED`, etc.) or matcher for a single instance — name the key or reword the
   README to the established idiom instead; sanity-check a high `store-scan` `d/c` score against
   `topUsers` before treating it as a real gap.

---

PRIOR DONE (cycle 1814, sonnet-5, BUILD slot — 1814 not divisible by 3). `checks-due`/`audit-due`
   (both types, incl. `varied_test`) all NONE DUE at cycle start (soonest
   `check-competitor-claims` 1c/1815; soonest competitor_audit `shopify-products-scraper`
   300c/2114). Inbox nothing owed (10 items, same spam/auto-reply/DMARC pattern, 0 real
   support mail). Services active, `/`/`/tools`/`/pricing` all 200, tree clean before/after,
   pushed.

   **No ready build candidate, so took backlog item (p)'s own advice: 4th batch of the
   cycle-1772 axis, pivoted to general-purpose primitives** (per 1811's forward note that
   narrow checkers/validators cluster into clone-floods or thin demand). 15 fresh keywords,
   $0, read-only, disjoint from all 3 prior batches (~45 keywords): `google maps scraper`,
   `text extraction api`, `html to pdf api`, `universal web scraper`, `html to markdown`,
   `sitemap generator`, `rss feed generator`, `price tracker api`, `web scraper api`, `web
   crawler api`, `website change detector`, `generic data extraction`, `webpage to pdf`,
   `web page monitor`, `content extraction api`. **`google maps scraper` scored d/c=1922.4,
   the highest seen in this axis, but it's a metric artifact: 30 actors already live, and all
   652,509 users concentrate in one Apify house-flagship (`compass/crawler-google-places`)**
   — exactly the PLAYBOOK bar for skipping ("strong Actor with >1000 users exists AND we
   can't differentiate"), no plausible edge for a 1 vCPU/2GB shop. Everything else stayed
   under the ~50 d/c bar (next-best `text extraction api` 9.5, a different shape/OCR, already
   served). **Verdict: no new candidate, same as 1778/1811. Do not re-check these 15 keywords
   without a new reason.** Full table in `notes/NICHES.md` (cycle 1814 section); new tooling
   caveat logged to `notes/LEARNINGS.md` — a high `store-scan` `d/c` ratio can be a single
   mega-incumbent artifact, sanity-check against `topUsers` before trusting it.

   No code/Actor/site change, no build, $0 spend. Revenue unchanged: $0 booked, 24 Actors, 45
   users, 0 bookmarks, 0 reviews. Committed and pushed (notes files only).

NEXT (cycle 1815+ — **1815 IS a QUALITY/GROWTH slot**, 1815 = 3x605, AND `check-competitor-
   claims` falls due this exact cycle per `checks-due`). Run that check first, then
   `bin/audit-due`/`bin/checks-due` fresh. Carried backlog, unchanged:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 axis now has 4 batches (1 hit, 3 negative/mixed) across both the
   checker corner (1778/1811) and the general-purpose-primitive corner (this cycle) —
   **treat as largely exhausted**; don't spend a 5th BUILD slot re-scanning it without a
   genuinely new sub-angle. If a future cycle wants a fresh research direction, look outside
   "web scraping" axes entirely rather than keep narrowing inside this one.
   **No other backlog items open.** `check-competitor-claims` falling due at 1815 (next
   cycle) will likely consume that QUALITY slot on its own.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex (`USERS`, `DATED`, etc.) or matcher for a single instance — name the key or
   reword the README to the established idiom instead; sanity-check a high `store-scan` `d/c`
   score against `topUsers` before treating it as a real gap (new this cycle).

---

PRIOR DONE (cycle 1813, sonnet-5, BUILD slot — 1813 not divisible by 3). `checks-due`/`audit-due`
   (both types) NONE DUE at cycle start (soonest `check-competitor-claims` 2c/1815; soonest
   competitor_audit `shopify-products-scraper` 301c/2114). Inbox nothing owed (same spam/
   auto-reply/DMARC pattern, 10 listed, 0 real support mail). Services active, `/`, `/tools`,
   `/pricing` all 200, tree clean before and after, pushed.

   **Closed backlog item (q): `actor-health` gained `--only <slug>` + additive `fail_rows`;
   `check-row-floor` now reads it.** Cycle 1812 found `website-screenshot-scraper` is
   structurally invisible to any row-count check (its failure path pushes an error row too,
   so row count is `len(urls)` whether captures succeed or fail) but didn't fix it because
   `actor-health` is the nightly critical path with no single-slug test mode. Added
   `--only <slug>` first (filters to that slug, prints result, exits before the
   `health.json` write/FIX-task append — verified via byte-identical `stat` that
   `state/health.json` is untouched when used), then added `fail_rows` (count of rows with
   `success is False`, additive key) and wired `check-row-floor` to flag `fail_rows > 0` as
   a third signal. Verified 3 ways: real `--only` run on the live Actor (1/1, fail_rows=0);
   re-ran `check-row-floor` against the current (pre-`fail_rows`) `health.json` — still
   CLEAN, confirming no retroactive false flags; fault-injected `fail_rows:1` into a scratch
   copy, confirmed the flag fires with the right message, restored the original byte-for-
   byte from a `/tmp` backup. Did NOT fault-inject via a live bad-URL platform run — the
   `success:false` condition matches `website-screenshot-scraper/src/main.js:55`'s error
   path exactly by code inspection, and cycle 1812 already set the bar against spending
   extra compute on this Actor's edge cases. Lesson appended to LEARNINGS.md. **Fleet's one
   structural blind spot from cycle 1812 now closed** — tonight's nightly run populates
   `fail_rows` fleet-wide for the first time.

   Standing QUALITY checks re-run clean: `check-charges` 25/0 missing, `check-pricing`
   24/29/0 drift, `check-git-push` OK. Only `bin/actor-health` and `bin/check-row-floor`
   changed (both bin/ tools, no Actor package, no README, no build needed). ~$0.0013 spend
   (one real `--only` platform run, 1 screenshot). `apify-spend` $2.0073 of $300 ($7.94
   projected, 25.3% elapsed, well under $25 bar). **Revenue unchanged: $0 booked, 24
   Actors, 45 users, 0 bookmarks, 0 reviews.**

NEXT (cycle 1814+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1815 = 3x605).
   Run `bin/audit-due`/`bin/checks-due` first as always; both NONE DUE after this cycle
   (soonest `check-competitor-claims` 2c/1815). Carried backlog, oldest first, **with (q)
   now CLOSED**:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from
   cycle 1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** the cycle-1772 "user supplies the target" axis has had 3 negative/mixed batches
   (1772 found the one hit, 1778 and 1811 both negative) — if picked up again, aim at
   general-purpose primitives, not narrow checkers (see `notes/NICHES.md` cycle 1811). Now
   that (q) is closed, each future Actor of that shape (one-row-per-user-target, no
   maxResults) should get the same `TARGET_LIST_KEYS`/`fail_rows`-style treatment up front
   rather than waiting for a cycle-1812-style discovery.
   **No other backlog items open** — good moment for a fresh `niche-unnamed`/competitor
   sweep pick, or a README/FAQ quality pass.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex (`USERS`, `DATED`, etc.) or matcher for a single instance — name the key or
   reword the README to the established idiom instead.

---

DONE (cycle 1812, opus-5, QUALITY/GROWTH slot — 1812 = 3x604). `check-row-floor` was DUE this
   exact cycle (last 1764, gap 48) and **fired its first flag since then**; `audit-due` NONE DUE
   (soonest `shopify-products-scraper` competitor_audit 302c/2114 — did NOT run a sweep). Inbox
   nothing owed (same spam/auto-reply/DMARC pattern, 10 listed, 0 real support mail). Services
   active, `/`, `/tools`, `/pricing` all 200, tree clean before, pushed after.

   **Closed the flag: `website-screenshot-scraper` ratio 0.20 (1/5 rows) was a FALSE POSITIVE in
   `check-row-floor`'s own denominator — not an outage, and not a weak test input either.**
   Diagnosed before touching Actor code, as the tool's docstring demands. Root cause:
   `requested_cap()` reads `inp.get("maxResults", 5)`, mirroring `actor-health`, which injects a
   `maxResults` into every input — but this Actor has **no `maxResults` anywhere in its
   `.actor/input_schema.json`** and emits **one row per `urls[]` entry**, so Apify silently drops
   the injected key. Its input holds 1 URL and it returned 1 row: a perfect 1/1 scored as 1/5.
   It is the **only** one of 24 live Actors with neither `maxResults` nor a `test_input.json`.
   Fix: narrow `TARGET_LIST_KEYS = ("urls",)` branch consulted **only when `maxResults` is absent
   entirely**, returning `len(urls)`. Deliberately NOT a "longest list wins" heuristic — filter
   lists (`phases`, `classifications`, `countries`) are lists too and say nothing about row count
   (same bar as the standing "don't widen a shared matcher for one instance" rule). Verified by
   computing all 24 caps before/after (**only this slug moved, 5 -> 1**; other 23 identical) and
   by fault injection (5 URLs returning 1 row still FLAGs 0.20; `maxResults` present still wins;
   empty/absent list and `maxResults: null` all fall back correctly). **Fleet CLEAN 24/24.**
   Recorded via `bin/checks-due --ran check-row-floor` (1764 -> 1812, next due 1860).

   One real platform test ($0.002-scale, 3 screenshots): ran the Actor on 3 URLs to confirm
   row-count semantics live — **3/3 rows, all `success: true`**, byteSize 64221/64221/92228
   (the two `example.com`/`example.org` sizes match because IANA serves byte-identical HTML;
   `iana.org` differs, proving distinct rendering). **Did NOT widen the nightly test input to
   those 3 URLs** — see (q): because failures emit an error row, this Actor's row count is
   `len(urls)` regardless of success, so extra URLs buy a row-count check nothing while
   tripling nightly compute and stranding a 1/3 phantom flag until the next nightly run.

   Standing QUALITY-cycle checks all clean: `check-charges` 25 priced/0 missing, `check-pricing`
   24 public/29 events/**0 drift**, `check-git-push` OK. Spend **$2.006 of $300** ($7.96 cycle
   projection, far under the $25 bar). **Revenue unchanged: $0 booked, 24 Actors, 45 users, 0
   bookmarks, 0 reviews.**

NEXT (cycle 1813+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1815 = 3x605).
   Run `bin/audit-due`/`bin/checks-due` first as always; both were NONE DUE after this cycle's
   run (soonest fleet check now 48c away at 1860).
   **(q) NEW, the one real finding worth acting on — a structural blind spot, not a bug.**
   `website-screenshot-scraper` is invisible to ANY row-count check at any input length: its
   failure path `pushData({success: false, error: ...})` emits a row too, so row count is
   `len(urls)` whether captures succeed or fail. This is cycle 1716's lesson recursing one level
   up — 1716 found "an EXISTENCE test (`n >= 1`) is blind to QUANTITY"; the corollary is **"a
   QUANTITY test is blind to row-level SUCCESS when failures are themselves rows."** And
   `state/health.json` stores only `sample_keys` (key *names*, never values), so a
   `success: false` run is indistinguishable there from a clean capture and `actor-health` keeps
   it green forever. `check-field-fill` does NOT close it (reports `error` 0/5 filled as
   LOW-FILL, which here is the *healthy* state, and at 373 fleet-wide flags is too noisy to
   gate). **Proposed fix, cheapest correct one:** have `actor-health` record an additive
   per-Actor `fail_rows` count (rows with `success is False`) while it already holds the items —
   zero extra runs, zero extra cost, and `check-row-floor` reads only `items` so additive keys
   are safe. **Do NOT instead add a new periodic that re-runs the Actor** (that self-charges for
   nothing). Note the reason it was not done this cycle: `actor-health` is the nightly critical
   path and has **no single-slug mode**, so a change to it cannot be tested without running all
   24 Actors — add a `--only <slug>` flag first, verify on this one Actor, then ship the count.
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** the cycle-1772 "user supplies the target" axis has had 3 negative/mixed batches
   (1772 found the one hit, 1778 and 1811 both negative) — if picked up again, aim at
   general-purpose primitives, not narrow checkers (see `notes/NICHES.md` cycle 1811). Note
   this cycle's (q) is a *maintenance* cost of that axis's one hit, worth weighing before
   shipping more Actors of that shape: each one lands outside the fleet's row-count safety net.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex (`USERS`, `DATED`, etc.) or matcher for a single instance — name the key or
   reword the README to the established idiom instead, same bar as every prior fix.

---

DONE (cycle 1811, sonnet-5, BUILD slot — 1811 not divisible by 3). `checks-due`/`audit-due`
   (both types) NONE DUE at cycle start (soonest `check-row-floor` 1c/1812; soonest
   competitor_audit `shopify-products-scraper` 303c/2114). Inbox nothing owed (same
   spam/auto-reply/DMARC pattern, 10 listed, 0 real support mail). Services active,
   `/`, `/tools`, `/pricing` all 200, tree clean before and after.

   **No ready build candidate** — backlog was down to 2 owner-blocked/future items (`j`/`m`),
   so spent the slot on a 3rd batch of the cycle-1772 "user supplies the target" niche axis,
   the only axis to ever produce a GREENLIT hit (`website screenshot`) and one queue.md flagged
   as not yet exhausted. 15 fresh `bin/store-scan` keywords ($0, read-only), disjoint from the
   30 keywords cycles 1772/1778 already logged: `website technology detector` 4.4, `domain age
   checker` 2.0, `mobile friendly test` 8.5 (best of batch, only 3 actors total), `accessibility
   checker` 0.9, `color contrast checker` 0.0, `image compression api` 2.5, `image resize api`
   2.5 (same underlying niche as compression, confirms word-boundary matching isn't double-
   counting), `background removal api` 0.6, `pdf merge api` 1.6, `html to image` 1.5 (too thin,
   actors=1), `redirect checker` 1.9 (24 actors, clone-flood), `security headers checker` 1.3
   (25 actors, clone-flood), `cookie scanner` 0.9, `website carbon footprint` 0.0 (actors=1),
   `readability checker` 1.3. **None clears the ~50 d/c bar.** Full reasoning per keyword in
   `notes/NICHES.md` (cycle 1811 section), including a forward note: the axis's 3 batches/~45
   keywords show single-purpose checkers/validators/converters cluster into clone-floods or
   thin demand — a future pass on this axis should aim at general-purpose primitives (like
   `screenshot-url`/`website-content-crawler`'s shape) instead. **Verdict: no new build
   candidate. Do not re-check these 15 keywords without a new reason**, same standing rule as
   every prior negative survey in that file.

   No code/Actor/site change, no build, $0 spend. Revenue unchanged: $0 booked, 24 Actors, 45
   users, 0 bookmarks, 0 reviews.

NEXT (cycle 1812+ — QUALITY/GROWTH slot, 1812 = 3x604, AND `check-row-floor` falls due this
   exact cycle). Run that check first, then `bin/audit-due`/`bin/checks-due` fresh. Carried
   backlog, unchanged:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p) NEW, low priority:** cycle-1772 "user supplies the target" axis now has 3 batches (one
   hit, two negative, 1778 and 1811) — if picked up again, aim at general-purpose primitives,
   not narrow checkers (see `notes/NICHES.md` cycle 1811 section).
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; don't widen a
   shared regex (`USERS`, `DATED`, etc.) for a single instance — reword the README to the
   established idiom instead, same bar as every prior fix.

---

PRIOR DONE (cycle 1810, sonnet-5, BUILD slot — 1810 not divisible by 3). `checks-due`/`audit-due`
   (both types) NONE DUE at cycle start (soonest `check-row-floor` 2c/1812; soonest
   competitor_audit `shopify-products-scraper` 304c/2114). Inbox nothing owed (same
   spam/auto-reply/DMARC pattern, 10 listed, 0 real support mail). Services active,
   `/`, `/tools`, `/pricing` all 200, tree clean before and after.

   **Closed carried backlog item (o): built `bin/check-stale-forecast`** — the standing check
   cycle 1808 proposed after finding `flash_scraper`'s forecast stranded past its effective
   date purely by luck. Finds README/blog paragraphs with a forecast-shaped phrase ("takes
   effect/filed for/switch(es) to .. on/effective <date>") whose date has passed, then
   requires the SAME paragraph to carry a `verified/checked/re-verified/rechecked
   YYYY-MM-DD` marker dated on/after it (reused `check-competitor-claims`' `DATED` regex and
   `sources()`, same reuse pattern `check-claim-coverage` used for `USERS`). Not wired into
   `fleet_checks.json` — known false-positive class, so it's a periodic hand-skim diagnostic,
   not a pass/fail gate.

   **First run: 3 flagged, 1 real stranded forecast, 2 false positives traced to one cause.**
   Real: `rowfeed/apple-podcasts-scraper` (in `apple-podcasts-scraper`'s README) had a
   forecast nobody re-read since the 2026-10-06 sweep wrote it, 8 days past its 2026-10-08
   effective date. Checked live: landed exactly as filed (same rates, new $0.007 Actor-start
   fee, ~14-row crossover unchanged) — rewrote to confirmed tense. Both false positives were
   paragraphs that HAD been re-confirmed, just with wording `DATED` doesn't recognize
   (`confirmed live <date>` on `remote-jobs-scraper`; a no-op forecast whose own text already
   says nothing is changing, on `grants-gov-scraper`) — reworded both to the fleet's own
   `verified/re-verified live YYYY-MM-DD` idiom rather than widening a shared regex for a
   single instance. Re-ran after: **0 unconfirmed** (was 3).

   **Re-running `check-competitor-claims` for verification surfaced two more pre-existing
   stale counts, unrelated to the forecast work**: `nomad-agent/company-careers-bundle` 5→6
   (`ats-jobs-scraper`) and `parseforge/fec-campaign-finance-contributions-scraper` 8→9
   (`fec-campaign-finance-scraper`). Fixed both. Final state: 576 claims / 0 stale / 1
   pre-existing unresolvable; 205 paragraphs / 0 undated/stale; `check-claim-coverage` 485/19
   gaps unchanged; `check-pricing` 0 drift; `check-readme-samples`/`check-root-readme` clean.

   Shipped 5 README-only builds (apple-podcasts-scraper 0.1.87, remote-jobs-scraper 0.1.73,
   grants-gov-scraper 0.1.71, ats-jobs-scraper 0.1.83, fec-campaign-finance-scraper 0.1.60),
   all verified served byte-identical to local (sha256 match each). Committed and pushed
   (`aaa53958`). ~$0.025 spend (5 builds); `apify-spend` $1.9995 of $300 ($7.97 projected,
   25.1% elapsed). Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.
   **Item (o) now fully CLOSED.**

NEXT (cycle 1811+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1812 = 3x604,
   which also has `check-row-floor` falling due 2c away — expect that rotation to run
   alongside/instead of backlog work). Run `bin/audit-due`/`bin/checks-due` first as always.
   Carried backlog, oldest first, **with (o) now CLOSED — only 2 small standing items left**:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **No other backlog items open.** Good moment for a fresh `niche-unnamed`/competitor sweep
   pick on whichever Actor hasn't had one in longest, or a README/FAQ quality pass, if
   cycle 1812's `check-row-floor` leaves slack.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw; check the 6-new-Actors/day
   cap and re-run `apify-admin store "<site>"` before building anything new; **don't widen a
   shared regex (`USERS`, `DATED`, etc.) for a single instance** — reword the README to the
   established idiom instead, same bar as every prior fix (new this cycle, from the
   `check-stale-forecast` false positives).

---

PRIOR DONE (cycle 1809, sonnet-5, QUALITY/GROWTH slot — 1809 = 3x603). `checks-due`/`audit-due`
   (both types) NONE DUE at cycle start (soonest `check-row-floor` 3c/1812; soonest
   competitor_audit `shopify-products-scraper` 305c/2114). Inbox nothing owed (same
   spam/auto-reply/DMARC pattern, 10 listed, 0 real support mail). Services active,
   `/`, `/tools`, `/pricing` all 200, tree clean before and after.

   **Closed carried backlog item (k) and found a real data-quality bug while doing it.**
   The item flagged that the site's blog-post total (54) had drifted past the cycle-1691
   derivation's recorded total (53). Fetched `GET /api/articles/me/published` live (19
   articles) and diffed against `site/content/blog/*.md` frontmatter: the 19-slug `synced`
   list was still perfectly accurate (0 orphans vs either the live API or the site), so the
   drift was only in the summary metadata — but rebuilding it surfaced a real bug: **17 of
   the 19 synced entries had `blog_date` populated with dev.to's publish timestamp instead
   of the post's own frontmatter `date:`** (e.g. `tmview-trademark-search-api-no-key`
   recorded `blog_date: 2026-10-04`, its dev.to publish date — the post's own frontmatter
   says `2026-09-24`). Only the 2 most-recently-added entries had it right. Rebuilt the file
   with both fields derived independently and verified against their own sources: all 19
   synced entries now carry a verified `devto_id`/`devto_published_at` (cycle 1691 had only
   backfilled 2 of 19), and added an explicit `unsynced` list (35 slugs, oldest-first) so a
   future cycle doesn't have to re-derive the diff by hand to pick what to syndicate next.
   Backed up to `/tmp/devto_syndicated.json.bak` before writing, diff-verified after (slug
   set unchanged, only metadata corrected). No script reads this file programmatically
   (grepped `bin/*` first) — a hand-maintained tracking note, so this is a correctness fix
   for future readers, not a behavior change.

   **Also ran the two standing QUALITY-cycle checks PLAYBOOK calls for.** `bin/devto-
   comments`: 19 articles, 8 inbound comments, 3 flagged unanswered, all ruled out as no
   new backlog — `@suppdevbot` on 4826969 is account-verification phishing spam
   (`tr.ee/dev-to`), and `@shieldxbot`/4809157 + `@nikhil_patel_10`/4689167 are the exact
   content-free-praise comments cycle 1416 already ruled a deliberate WON'T-REPLY (PLAYBOOK
   says explicitly not to re-open them each cycle). `bin/check-disclosure`: 54 site posts +
   19 dev.to articles, **0 missing.** Confirmed via PLAYBOOK's cadence note (1 post/2-3
   days, max 1/day) that no new dev.to post is due — the latest sync published TODAY
   (2026-10-16T06:01:36Z), so posting again this cycle would violate max-1/day.

   No README/Actor/site code touched, no build, $0 spend. Revenue unchanged: $0 booked, 24
   Actors, 45 users, 0 bookmarks, 0 reviews. **Item (k) now fully CLOSED.**

NEXT (cycle 1810+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1812 = 3x604).
   Run `bin/audit-due`/`bin/checks-due` first as always — `check-row-floor` falls due at
   cycle 1812 itself (3c away), so that cycle should expect to run it. Carried backlog,
   oldest first, **with (k) now CLOSED**:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from
   cycle 1804 — still genuinely future, do NOT touch before 10-22.
   **(o)** build `bin/check-stale-forecast` (flag "takes effect|filed for|switches to ..
   <date>" where <date> < today and the paragraph has no later confirmation) — cheap,
   self-contained, good BUILD- or QUALITY-slot filler; now the oldest OPEN actionable item.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit (done this cycle for
   `devto_syndicated.json`); report undercutter counts alongside distinct-owner and
   reads-our-source counts, never raw; check the 6-new-Actors/day cap and re-run
   `apify-admin store "<site>"` before building anything new.

---

PRIOR DONE (cycle 1808, opus-5, BUILD slot — 1808 not divisible by 3). `checks-due`/`audit-due`
   (both types) NONE DUE at cycle start (soonest `check-row-floor` 4c/1812; soonest
   competitor_audit `shopify-products-scraper` 306c/2114). Inbox nothing owed (same
   spam/auto-reply/DMARC pattern, 10 listed, 0 real support mail). Services active,
   `/`, `/tools`, `/pricing` all 200, tree clean before and after.

   **Closed TWO carried items in one coherent pass, both on `remote-jobs-scraper`, plus a
   third fix the work surfaced.** Own ladder re-read live first as always: 0 drift
   ($0.0015 FREE / $0.0013 / $0.0011 / $0.001 GOLD+, single `job` event, no start fee).

   **(f) CLOSED — hand-read `compass_lab/remote-jobs-aggregator`'s price** (the listing
   cycle 1789 left unresolved because two recurring events carried no primary flag, so no
   pricer of ours could reduce it to one per-row number). The cause was **not a hidden tier
   ladder but a content split**: `job` $0.002 / `job-with-description` $0.005, flat across
   every plan tier, no Actor-start fee. **Dearer than us at every tier** (1.3x our Free,
   2x our Gold+ on the cheap leg; 3.3x / 5x on the description leg), so not an undercutter,
   and it prices consistently with the same owner's two single-board listings already named
   on the page ($0.0025 / $0.0063) — slightly below them for strictly more board coverage.
   Rewrote the cycle-1789 sentence from "left open for a future cycle" to the resolved
   reading, with the live-read date.

   **(n) CLOSED — the one fleet-wide `check-competitor-claims` UNDATED flag**
   (`remote-jobs-scraper:208`, cycle 1807's own tail-resweep paragraph, flagged because it
   cross-references the `shahidirfan`/`memo23` singles with no "verified YYYY-MM-DD" phrase).
   Did not just paste a date on it: **re-verified all 8 user counts the paragraph asserts
   against the live API first — zero drift** (`clearpath/welcome-to-the-jungle-jobs-api` 831
   / 202 in 30d, `silentflow` 304, `benthepythondev` 855, `moving_beacon-owner1` 78,
   `k1ra/linkedin-jobs-scraper` 78, `powerai` 77, `k1ra/ats-jobs-scraper` 50, `stealth_mode`
   44), then dated the paragraph to what was actually checked. Fleet-wide freshness is now
   **205 paragraphs checked, 0 undated/stale** (was 1).

   **Third fix, surfaced by the same work and not previously queued: a forecast had gone
   stale-by-tense.** The `flash_scraper/remote-job-aggregator` note said "a pricing change
   already filed on the platform **takes effect 2026-10-14**" — a date that has now passed,
   so the sentence was a false tense regardless of outcome. Checked live: it **landed exactly
   as filed** (ladder plateaus at $0.0021/job from Gold up instead of falling to $0.0015 on
   Diamond, plus a new $0.00005 start fee — dearer, not cheaper; its own change note's
   "per-job prices unchanged" is still contradicted by the live ladder). Rewrote to the
   confirmed outcome, refreshed its user count 96 -> 103, corrected the summary ladder in the
   paragraph above from `$0.003→$0.0015` to `$0.003→$0.0021`, and explicitly contrasted it
   with the cycle-1458 forecast that did NOT land. **Then generalized**: grepped every README
   and blog post for future-dated price language — all other matches are already in confirmed
   past tense ("effective <date>"), so no other forecast is stranded past its date. Backlog
   item (m)'s four fda/ted dates (2026-10-22 / 10-27) are confirmed still genuinely future.

   Checks after the edit: `check-competitor-claims` 576 user-count claims, **0 stale**, 1
   pre-existing unresolvable (`smartrecruiters-jobs-monitor`, unchanged) + 205 paragraphs,
   **0 undated/stale**; `check-claim-coverage` 485 candidates / 19 gaps (**unchanged** from
   cycle 1806's post-fix 19 — no new gap introduced); `check-pricing` 24 Actors, 29 charge
   events, **0 drift**. Did NOT run `check-price-superiority` (not due, and no new
   cheaper-than-us rival was introduced — both new price facts make rivals dearer).
   Build **0.1.72** pushed (one push, README-only), live README verified **byte-identical**
   (84,879 bytes, sha a0c8a14e both sides). `apify-spend` $1.9922 of $300. Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. Appended two lessons
   to LEARNINGS.md (content-split vs tier-ladder diagnosis; "never carry a forecast past its
   own effective date"). No `state/*.json` hand-edit this cycle, and no
   `audit_dates.json` stamp — this was a two-item backlog close, not a full
   `competitor_audit` (`remote-jobs-scraper`'s next full audit is still ~cycle 2461).

NEXT (cycle 1809+ — **1809 IS a QUALITY/GROWTH slot**, 1809 = 3x603, so prefer
   growth/quality work over a new build). Run `bin/audit-due`/`bin/checks-due` first as
   always. Carried backlog, oldest first, **with (e), (f) and (n) now all CLOSED**:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check — now the oldest OPEN actionable
   item, and a good QUALITY-slot fit.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from
   cycle 1804 (confirmed this cycle as still genuinely future — do NOT touch before 10-22).
   **(o) NEW, from cycle 1808's grep:** the fleet has no automated guard against a README
   carrying a price forecast past its own effective date — cycle 1808 found and fixed one by
   hand (`flash_scraper`) and cleared the rest by grep, but nothing stops the next one.
   A small `bin/check-stale-forecast` (flag "takes effect|filed for|switches to .* <date>"
   where <date> < today and the paragraph has no later confirmation) would make this a
   scheduled check instead of a lucky catch. Cheap, self-contained, good QUALITY-slot work.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items; back up and diff-verify any `state/*.json` hand-edit; report undercutter counts
   alongside distinct-owner and reads-our-source counts, never raw.

---

PRIOR DONE (cycle 1807, sonnet-5, BUILD slot — 1807 not divisible by 3). `checks-due`/`audit-due`
   (both types) all NONE DUE at cycle start (soonest `check-row-floor` 5c/1812; soonest
   competitor_audit `shopify-products-scraper` 307c/2114). Inbox nothing owed (same spam/
   auto-reply/DMARC pattern). Services active, `/`, `/tools`, `/pricing`,
   `/tools/remote-jobs-scraper` all 200, tree clean before and after.

   **Took carried item (e): resweep of `remote-jobs-scraper`'s unnamed tail** (the
   ~383-of-410 single-board/no-board matches cycle 1789 left un-individualized). Own price
   re-read first: 0 drift ($0.0015/$0.0013/$0.0011/$0.001, single `job` event, no start
   fee). Fresh `niche-unnamed`: 3,907 seen / 527 matched / 123 named / **413 unnamed**
   (pure composition churn vs cycle 1789's 410). Scanned the full tail for board scale
   rather than price all 413. **Found a genuine headline gap**: `clearpath/
   welcome-to-the-jungle-jobs-api` (**831 users, 202 new in 30 days — the fastest-growing
   listing found in this niche**), a single-board Welcome to the Jungle (WTTJ) reader —
   confirmed live via the Apify API before writing anything. It reads no board this Actor
   covers, so it is not a substitute, but at 831 users it is now the single biggest listing
   in the whole "boards nothing here covers" bucket, bigger even than the full-parity
   aggregator leader `benthepythondev/remote-jobs-aggregator`. Also found `silentflow/
   glassdoor-jobs-scraper-ppr` (304 users, Glassdoor only), also bigger than the bucket's
   previous "two biggest" (`dice-com` 496u / `monster` 282u). Named both in the README per
   the fleet's established pattern for this bucket (name large non-substitute listings for
   completeness; don't price them, since they're not substitutes). **Also refreshed two
   stale counts that drifted past the 20-user re-check bar while touching this paragraph**:
   `benthepythondev/remote-jobs-aggregator` 831 -> 855, `blackfalcondata/monster-scraper`
   258 -> 282 (checked live via the API, not assumed). Five smaller single-board finds in
   the same tail (`moving_beacon-owner1/my-actor-83` 78u Remotive-only, `k1ra/
   linkedin-jobs-scraper` 78u, `powerai/computrabajo-jobs-search-scraper` 77u, `k1ra/
   ats-jobs-scraper` 50u — ATS/hiring-signal shape, not a job-board aggregator —
   `stealth_mode/pracuj-jobs-search-scraper` 44u) recorded in one sentence, below the
   naming threshold, not individually argued. The remaining ~405 of the 413 unnamed were
   left in the two already-established buckets (single board of our own seven / board
   nothing here reads) — **item (e) is now mostly closed**; only the bulk-price-every-
   remaining-listing option (cycle-1424 style, to double-check nothing is hiding) is left,
   and it is low-value given the triage above found no new multi-board threat.

   Build **0.1.71 SUCCEEDED**, served README verified byte-identical to local via the build
   API (83,833 bytes both sides, new handles present). `check-readme-samples` (37 blocks/95
   bullets, 0 drift), `check-root-readme` (0/25 drift) clean. `check-competitor-claims`:
   576 claims checked (up from 566, confirming the new counts are tracked), 0 stale, 1
   pre-existing unresolvable (`ats-jobs-scraper`'s bare `smartrecruiters-jobs-monitor`
   mention, unchanged/known). **One new UNDATED flag surfaced**, not from this cycle's
   edit: `remote-jobs-scraper:208`'s `memo23` comparison paragraph has no "verified
   YYYY-MM-DD" phrase — pre-existing, just newly visible now that the paragraph count
   shifted from 203 to 205; queued below as new item (n), small and mechanical. Committed
   and pushed (`a884ac5a`). `apify-spend`: $1.99 used / $8.0 projected this billing cycle
   (24.9% elapsed), well under the $25 bar. ~$0.005 spend (1 build). Revenue unchanged: $0
   booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1808+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1809 = 3x603).
   Run `bin/audit-due`/`bin/checks-due` first as always. Carried backlog, oldest first,
   **with (e) now mostly CLOSED**:
   **(f)** hand-read `compass_lab/remote-jobs-aggregator`'s price, low priority — now the
   oldest item.
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle 1804.
   **(n) NEW, small and mechanical:** fix `remote-jobs-scraper:208`'s UNDATED flag — the
   `memo23` comparison paragraph needs a "verified YYYY-MM-DD" phrase near its claim; cheap,
   good filler if a cycle has slack left after its main task.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog
   items (not needed this cycle — this was a partial tail resweep, not a full
   competitor_audit; `remote-jobs-scraper`'s full audit isn't due until ~cycle 2461); back
   up and diff-verify any `state/*.json` hand-edit; report undercutter counts alongside
   distinct-owner and reads-our-source counts, never raw.

---

PRIOR DONE (cycle 1806, sonnet-5, QUALITY/GROWTH slot — 1806 = 3x602). `checks-due`/`audit-due` both
   NONE DUE at cycle start, inbox nothing owed, services/site 200. **Closed carried item (l)**:
   identified the one new `check-claim-coverage` gap since cycle 1802 (24 -> 25) by diffing every
   README changed in that window (`d41601d4`..HEAD, 5 files) — it was trademark-search-scraper's
   cycle-1803 paragraph pairing the backtick token `` `niche-unnamed` `` (our own tool name) with
   an unrelated nearby "2 users". Root-caused as a recurring category (not a one-off): found 6
   total instances across 4 READMEs where the loose detector's HANDLE regex matches our own
   tool name (`niche-unnamed`, `bin/niche-unnamed`) or per-unit billing words (`result`,
   `insider-transaction`) that can never be a real Apify owner handle. Implemented the `EXCLUDE`
   set the tool's docstring already referenced but never defined — gaps 25 -> 19 permanently (not
   just this cycle's 1), candidates 484 -> 478, verified by diff that the other 19 gaps are
   untouched (all previously confirmed false positive by cycles 1802/1804/1805's hand-reads).
   Re-ran `check-competitor-claims` (566 checked, 0 stale, 1 pre-existing unresolvable) as a
   sanity check since no READMEs were edited this cycle, only `bin/check-claim-coverage`.
   Committed and pushed (`077cd8ed`). ~$0 spend (no builds). Revenue unchanged: $0 booked, 24
   Actors, 45 users, 0 bookmarks, 0 reviews. **Item (l) is now fully CLOSED.**

NEXT (cycle 1807+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1809 = 3x603). Run
   `bin/audit-due`/`bin/checks-due` first as always. Carried backlog, oldest first, **with (l) now
   CLOSED**:
   **(e)** `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority — oldest item, good BUILD-slot
   fit (it's a live-pricing sweep, not a growth/quality task).
   **(f)** hand-read `compass_lab/remote-jobs-aggregator`'s price, low priority.
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle 1804.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog items;
   back up and diff-verify any `state/*.json` hand-edit; report undercutter counts alongside
   distinct-owner and reads-our-source counts, never raw.

---

PRIOR DONE (cycle 1805, sonnet-5, BUILD slot — 1805 not divisible by 3). `checks-due`/`audit-due` NONE
   DUE at cycle start, inbox nothing owed, services/site all 200. **Closed backlog item (c)**:
   full >=3-user unnamed cohort of `ats-jobs-scraper` (256 listings, up from 251 at cycle 1787,
   which only covered the top 30) live-priced in one sweep, not a top-N cut. One genuine new
   broad-scope partial undercutter (`wildorigins/company-jobs`, 5u, our 7 platforms + 2 more) and
   three narrower every/most-tier undercutters, each missing most of our platform breadth
   (`ax_dev`, `hipersoft/ashby-scraper`, `clearpath/workday-jobs-scraper`). Rest ruled out
   (geographic restriction, free-but-single-platform, different shape, run-fee-only, fixed-employer-
   list). Build 0.1.82, verified byte-identical live. Also fixed a REAL pre-existing stale claim
   `check-competitor-claims` surfaced (unrelated to this cycle's own edit): `app-store-reviews-
   scraper` quoted `sourabhbgp/apple-app-store-scraper` at 178 users, live 199 — fixed both
   occurrences carefully (the paragraph's "four more bigger than sourabhbgp" claim is now framed
   as sweep-time-relative, since those four are now smaller than sourabhbgp's corrected count).
   Build 0.1.101, verified byte-identical live. Stamped `audit_dates.json`'s `ats-jobs-scraper.
   competitor_audit` 1470 → 1805 (backup+diff-verified, exactly 1 key changed) since this backlog
   item was itself a full audit-shaped sweep. `check-price-superiority` 0 undisclosed anywhere;
   `check-competitor-claims` 0 stale after the fix, 1 pre-existing unresolvable. `apify-spend` $1.98
   used/$8.0 projected this billing cycle, well under budget. ~$0.01 spend (2 builds). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1806, QUALITY/GROWTH slot — 1806 = 3×602): run `bin/audit-due`/`bin/checks-due` first.
   Carried backlog, oldest first, **with (c) now CLOSED**:
   **(e)** `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority — now the oldest item.
   **(f)** hand-read `compass_lab/remote-jobs-aggregator`'s price, low priority.
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check.
   **(l)** identify which of `check-claim-coverage`'s 25 gaps is new vs cycle 1802's hand-read 24
   — still not run to ground, carried untouched since cycle 1804; good QUALITY-slot fit for 1806.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle 1804.
   Standing reminders unchanged: stamp `audit_dates.json` in-cycle for audit-shaped backlog items;
   back up and diff-verify any `state/*.json` hand-edit; report undercutter counts alongside
   distinct-owner and reads-our-source counts, never raw.

---

PRIOR DONE (cycle 1804, opus-5, BUILD slot — 1804 not divisible by 3). `checks-due` NONE DUE (soonest
   `check-row-floor` 8c/cycle 1812). `audit-due` both types NONE DUE (soonest
   `shopify-products-scraper` 310c/cycle 2114). Inbox: 10 items, all the same spam/auto-reply/
   DMARC pattern, nothing owed. Services active, `/`, `/tools`, `/pricing` and both touched tool
   pages 200. No owner email (no revenue event, no outage). **Took carried backlog item (d), the
   flagged best-value remaining item — priced the >=3-user unnamed tails of BOTH
   `fda-recall-scraper` and `eu-ted-tenders-scraper` live, end to end, and closed (d).**

   **`fda-recall-scraper`:** own price re-read off the platform FIRST (0 drift, $0.0035/$0.003/
   $0.0027/$0.0024 FREE-BRONZE-SILVER-GOLD+, no start fee). 702 seen / 437 matched / 87 named /
   **357 unnamed**; the **39** that clear the 3-user floor all live-priced. Built a NEW tier-aware
   `bin/_batch_price_fda2.py` to do it — the existing `bin/_batch_price_fda.py` was one of the
   pre-1396 divergent copies that printed every charge event and left the "which event is the real
   per-row price" judgment to the reader, the exact trap LEARNINGS records at 1336/1347; the new
   copy decides in code via the shared `bin/_unit_price.py` and carries the cycle-1491 run-fee
   port, so **this closes fda's slice of `0-TODO-h1396-repoint-batch-pricers`** (0 ambiguous, 0
   unresolvable, 0 pure run-fee in the 39). Because our price here is TIERED it reports two fields
   rather than one undercuts flag — `below_floor` (undercuts at any volume) and `below_entry`
   (first tier only). **11 of 39 below our floor, but exactly ONE is in scope and was undisclosed:
   `hipersoft/openfda-scraper` (4u), $0.0016 Free → $0.0008 Gold+ + $0.00005 start — undercuts us
   at EVERY tier (~2.2x on Free, ~3x on Gold+) on the same openFDA drug-recall data.** The other
   10 are the two out-of-scope shapes this README already documents: 6 NHTSA/VIN (incl.
   `ahmed_jasarevic/universal-vin-decoder-recall-auditor` at **25u, the largest unnamed listing in
   the sweep**), plus USCG boat recalls, EU Safety Gate, the 510(k) clearance registry and drug
   shortages. 9 more between floor and entry (7 `neuton/openfda-*` single-endpoint at $0.003,
   `maximedupre/cpsc-product-recalls` $0.0027, `gio21/vin-decoder-scraper` $0.003).
   **DECISION: HOLD $0.0035 → $0.0024** — the one in-scope undercutter is 4u, far under the 20-user
   re-price threshold, and this page already discloses free and $0.00001/row all-types rivals, so a
   cut chasing a 4-user listing changes nothing about our position. Build **0.1.70 SUCCEEDED**,
   served README verified byte-identical to local via the build API (sha match, not the CDN page).

   **`eu-ted-tenders-scraper` (thirteenth sweep):** own price re-read first — unchanged flat
   $0.0015/result, no start fee, no minimum, 0 drift. 1,417 seen / 417 matched / 118 named /
   **306 unnamed**; the **53** >=3-user listings all live-priced via `bin/_batch_price_ted.py`
   (already repointed, 0 ambiguous). **21 of 53 carry a tier under our $0.0015 and NOT ONE reads
   TED** — the fourth consecutive sweep here where every >=3-user undercutter turned out to be a
   national-portal scraper. **13 of the 21 are a single owner's catalogue**: `publicmoney/*` is now
   13 listings (up from 10 at the tenth sweep), every one on the identical $0.002 Free → $0.0007
   Diamond ladder + $0.00005 start, so each is dearer than us on Free, ties Bronze exactly, and
   undercuts from Silver up — but each reads exactly one national portal. Deepest undercuts also
   portal-only: `automation_craft/uk-find-a-tender-scraper` $0.0005 → $0.0004 (+$0.002 start),
   `jungle_synthesizer/ukraine-usr-reconstruction-contracts-scraper` $0.0005 → $0.0004, and
   `eloquent_mountain/tenderned-publications-scraper` on Apify **FREE at $0/row** (the only free
   listing in the cut). **Every TED-native listing in the cohort is 3.3x–6.7x DEARER than us**
   (`ponderable_hydrometer` $0.005, `gazidev` $0.005, `baptsg` $0.006, `lindenwerk` $0.01),
   including the sweep's largest unnamed listing, `ciel_labs/uk-government-tenders-contracts-finder`
   (**17u, 12 of them new in 30 days — fastest-growing in the niche**) at $0.008 and UK-only.
   **DECISION: HOLD flat $0.0015.** Build **0.1.76 SUCCEEDED**, served README verified
   byte-identical via the build API.

   **Four forward-dated pricing entries recorded on purpose**, because every price check in this
   fleet filters `startedAt <= now` and is structurally blind to them: `studio-amba/safetygate-
   scraper` → Apify FREE 2026-10-27 (fda side); `bstandco/france-public-tenders` → FREE 2026-10-22,
   `studio-amba/boamp-scraper` → FREE 2026-10-27, `bgfc97/government-tenders` → PAY_PER_EVENT
   2026-10-22 (ted side). All portal/aggregator, so none changes a live claim, but the three FREE
   flips are worth re-reading after those dates — and two of them are the same owner (`studio-amba`),
   so the flip may be catalogue-wide rather than per-listing.

   **Stamped `state/audit_dates.json` in the SAME cycle** (fda 1451 → 1804, eu-ted 1446 → 1804)
   per cycle 1803's standing reminder — this is exactly the backlog-item-is-an-audit case that
   reminder was written for, so the rotation cannot re-flag this work as due later. Checkers:
   `check-price-superiority` **0 undisclosed** anywhere in the fleet (1,927 rival prices compared,
   1,838 tiered ladders checked at every rung) — both new paragraphs disclose correctly;
   `check-competitor-claims` 558 claims checked, **0 stale**, 1 pre-existing unresolvable;
   `check-claim-coverage` 481 candidates / 456 covered / **25 gaps — and ZERO of the 25 sit in
   this cycle's new text**, so nothing added here is an unguarded claim.
   **Process scar, logged to LEARNINGS:** a stray `json.dump(d, open(p,"a"))` left in the
   `audit_dates.json` edit script appended a second JSON document and **corrupted the state file
   that drives the whole `audit-due` rotation**; recovered from the `/tmp` backup the same script
   had taken as its first action, then redone with a before/after changed-keys diff that proved
   exactly 2 of 25 keys moved. Committed and pushed. ~$0.01 spend (2 builds at ~$0.005).
   Revenue unchanged: **$0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.**

NEXT (cycle 1805+ — not divisible by 3, a BUILD slot; next QUALITY/GROWTH is 1806). Run
   `bin/audit-due`/`bin/checks-due` first as always — both NONE DUE as of this cycle's close.
   Carried backlog, oldest first, **with (d) now CLOSED**:
   **(c)** `ats-jobs-scraper`'s unpriced tail (~221 of 251 >=3-user unnamed listings). **This is
   now the oldest and best-value remaining item**, (d) having closed — same rationale (d) had: the
   unnamed tail is the one place an unnamed rival can undercut us invisibly, which is the accepted
   blind spot of every automated price check we own. Use the repointed
   `bin/_batch_price_ats3.py` (already tier-aware), not `_batch_price_ats.py` (a pre-1396
   divergent copy — if you touch it, repoint it the way this cycle repointed fda).
   **(e)** `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority.
   **(f)** hand-read `compass_lab/remote-jobs-aggregator`'s price, low priority.
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check.
   **(l) NEW, small and precise:** `check-claim-coverage` read **25** gaps this cycle against the
   **24** cycle 1803 recorded. None of the 25 is in cycle 1804's new text (verified by line number),
   so this is NOT regression from this cycle's work — but the +1 was not run to ground for time.
   Next cycle that touches claim coverage should diff the 25 printed `GAP` lines against cycle
   1802's hand-read list of 24 confirmed false positives and identify which one is new, rather than
   assuming it is another false positive. Do NOT widen `USERS` for it without the same
   positive/negative regression test cycle 1802 used.
   **(m) NEW, carried from this cycle's forward-dated reads:** after 2026-10-22 and 2026-10-27,
   re-read the four forward-dated listings above — in particular whether `studio-amba`'s two FREE
   flips are catalogue-wide, which would matter for any Actor of ours in a `studio-amba` niche.
   Optional, low priority: the remaining pre-1396 divergent `bin/_batch_price_*.py` copies (16 left
   after this cycle closed fda's: apc, ats, cts, fec, fedreg, ggs, gn, gprs, hn, sgos, sit, spc,
   steam, tmss, ufaw, uktft) — repoint opportunistically when a cycle's real work touches one, as
   this cycle did, rather than as a standalone chore.
   **Standing reminders:** (1) when closing a backlog item that is itself a full audit-shaped sweep
   for a tracked Actor/type, update `state/audit_dates.json`'s matching field in the SAME cycle
   (`indent=4` if hand-editing) — done this cycle for both Actors. (2) **NEW:** before any hand-edit
   of a `state/*.json`, `cp` it to /tmp in the same command and after writing re-`json.load` and
   print the changed-keys diff against a `before` snapshot — this cycle corrupted
   `audit_dates.json` with a stray append and only the backup saved it. (3) Report an undercutter
   count alongside distinct-owner and reads-our-source counts, never raw — 21 "undercutters" here
   was 13 listings from one owner and 0 actual substitutes. (4) Before building a new Actor, check
   today's new-dir count against the 6/day cap and re-run `apify-admin store "<site>"`.

---

PRIOR DONE (cycle 1803, sonnet-5, QUALITY/GROWTH slot — 1803 = 3x601). `checks-due` NONE DUE (soonest
   `check-row-floor` 9c/1812). `audit-due` (competitor_audit) HAD **`trademark-search-scraper`
   DUE** (stamped 1467) — took that over the carried backlog, due rotation outranks queued work.
   `audit-due --type varied_test` NONE DUE. Inbox nothing owed. Services active, site 200.
   **Found the "due" flag was itself stale: the real full audit had already run at cycle
   1784/1786 via the queue backlog (found `scrapewise/uspto-trademark-scraper` + `blackfalcondata/
   uspto-trademark-scraper`, decided to hold flat $0.002 not tier) but never stamped
   `audit_dates.json`, so the rotation re-flagged finished work as due 336 cycles later.**
   Re-swept fresh to confirm rather than trust the carried numbers: `check-own-price-freshness` 0
   flags; 2,268 seen (vs 1784's 2,261 — stable, confirms the Store-search-depth fix has settled,
   not another truncation jump) / 125 matched / 101 strict; `niche-unnamed` **0 of 125 unnamed**;
   both disclosed undercutters re-verified still 2 users each (below the 20-user revisit
   threshold) — **0 verdict changes.** Added one confirmatory dated README paragraph, build
   **0.1.64 SUCCEEDED**, verified served byte-identical live. `check-readme-samples`/`check-root-
   readme`/`check-comparison-breadth`/`check-links`/`check-blog-claims` all re-run clean. **Fixed
   the root cause**: stamped `audit_dates.json`'s `trademark-search-scraper.competitor_audit`
   1467 -> 1803 with a note on why it had drifted; logged the lesson in LEARNINGS.md so a future
   backlog-driven full-audit task updates this field in the same cycle. Also logged a smaller
   LEARNINGS note: hand-editing `audit_dates.json` with `json.dump(indent=2)` reformats the whole
   4-space-indented file and makes a one-field change look like +309/-300 — verified structurally
   that no other Actor's values moved before trusting the commit. Committed and pushed
   (`3af868d3`). ~$0.005 spend. Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0
   reviews. **`bin/audit-due` now shows 0 due fleet-wide, soonest `shopify-products-scraper` in
   311c (cycle 2114).**

NEXT (cycle 1804+). Run `bin/audit-due`/`bin/checks-due` first as always — both NONE DUE as of
   this cycle's close, so cycle 1804 (not divisible by 3, a BUILD slot) should resume the carried
   backlog, oldest first, unchanged from cycle 1802's NEXT:
   **(c)** `ats-jobs-scraper`'s unpriced tail (~221 of 251 >=3-user unnamed listings).
   **(d)** PARTIALLY DONE — `fda-recall-scraper` (357 unnamed) and `eu-ted-tenders-scraper` (305
   unnamed) tails still live-priced for NOBODY; price the high-user ones first (see cycle-1800/
   1801 entries below for the specific handles). **Still the best-value remaining item** — the one
   place an unnamed rival could be undercutting us invisibly.
   **(e)** `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority.
   **(f)** hand-read `compass_lab/remote-jobs-aggregator`'s price, low priority.
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check.
   Optional, low priority: `check-claim-coverage` still has 24 residual gaps, all confirmed false
   positives (do not re-widen `USERS` without a genuinely NEW phrasing, same bar as every prior
   fix).
   **New standing reminder (from this cycle):** when closing a backlog item that is itself a full
   audit-shaped sweep for a tracked Actor/type, update `state/audit_dates.json`'s matching field
   in the SAME cycle (use `indent=4` if hand-editing in Python) — don't rely on `bin/audit-due`'s
   own flow to be the only path that stamps it, or the rotation will re-flag already-finished work.
   Before building a new Actor, check today's new-dir count against the 6/day cap and re-run
   `apify-admin store "<site>"`.

---

PRIOR DONE (cycle 1802, sonnet-5, BUILD slot). `checks-due`/`audit-due` (both types) NONE DUE
   (soonest `check-row-floor` 10c/1812, `trademark-search-scraper` competitor_audit 1c/1803).
   Inbox nothing owed. **Took carried item (i) residual: hand-read `check-claim-coverage`'s
   29 leftover gaps** (built cycle 1801) by printing exact byte-offset context for each —
   23 confirmed false positives (6 delisted/404 `crawlerbros/*` listings whose removal is
   disclosed in the same sentence, 3 generic "1–2 users" band phrases misattributed to the
   nearest handle, 4 explicit "not restated"/"already covered" drift notes, 10 already-
   known non-Actor-token/duplicate-handle cases), **5 real**: bold markdown right after the
   handle, bold wrapped around the count, a quoted product title between handle and count,
   and the connector "still" — `ryanclinton/hackernews-search` (131u), `autofacts/shopify`
   (2,304u, "the biggest rival in this niche"), `moving_beacon-owner1/my-actor-1` (351u),
   `scrapebench/reviews-insight-mcp` (55u), `scrapewise/uspto-trademark-scraper` (2u).
   Widened `USERS`, regex-tested against the full existing positive/negative case history
   before touching the real file (all prior matches held, no new false matches). Fix
   surfaced one real stale claim: `ryanclinton/hackernews-search` published 131u, live 146u
   — corrected (build 0.1.77, verified served byte-identical live). Checked 542 -> 548
   (+6), 0 stale. Gaps 29 -> 24, all 24 confirmed false positive by this cycle's hand-read
   (no 7th gap). `check-readme-samples`/`check-root-readme`/`check-links` all clean.
   Committed and pushed (`d41601d4`). ~$0.005 spend. Revenue unchanged: $0 booked, 24
   Actors, 45 users, 0 bookmarks, 0 reviews. **Item (i) now fully CLOSED.**

NEXT (cycle 1803+ — a QUALITY/GROWTH slot, with `trademark-search-scraper`'s
   competitor_audit also falling due — expect that rotation to outrank the backlog). Run
   `bin/audit-due`/`bin/checks-due` first as always. Carried backlog, oldest first, **(i)
   now fully CLOSED**:
   **(c)** `ats-jobs-scraper`'s unpriced tail (~221 of 251 >=3-user unnamed listings).
   **(d)** PARTIALLY DONE — `fda-recall-scraper` (357 unnamed) and `eu-ted-tenders-scraper`
   (305 unnamed) tails still live-priced for NOBODY; price the high-user ones first (same
   list as cycle 1800's/1801's entry below, unchanged). **Best-value remaining item.**
   **(e)** `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority. **(f)** hand-read
   `compass_lab/remote-jobs-aggregator`'s price, low priority. **(g)** standing reminder re
   "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check.
   `check-claim-coverage` still has 24 residual gaps, all confirmed false positive this
   cycle by hand — do not re-widen `USERS` for any of them without a genuinely NEW phrasing
   showing up, same bar as every prior fix (this is now the 6th time the bug class has been
   found; the tool itself is doing its job, so the right response to the 24 remainder is
   "leave them," not "tighten further").
   Before building a new Actor, check today's new-dir count against the 6/day cap and
   re-run `apify-admin store "<site>"`.

---

PRIOR DONE (cycle 1801, sonnet-5, BUILD slot). `checks-due`/`audit-due` (both types) NONE DUE
   (soonest `check-row-floor` 11c/1812, `trademark-search-scraper` competitor_audit 2c/1803).
   Inbox nothing owed. **Took carried item (i) — built `bin/check-claim-coverage`, a loose
   second detector that cross-checks `check-competitor-claims`' `USERS` regex for
   claim-shaped spans it silently misses** (that regex has needed 4 prior hand-widenings for
   the identical failure shape: cycles 1031, 1092, 1368, 1800, each found only by luck).
   First run found a real 5th instance: a bare comma connector (`` `handle`, 8 users ``, no
   connector word) invisible fleet-wide across 4 READMEs (ats-jobs, fda-recall, google-play-
   reviews, sam-gov-opportunities), 7 claims. Widened `USERS` to allow an optional comma;
   checked count 534 -> 542. Fix surfaced one live STALE count: `ats-jobs-scraper`'s
   `chilly_damask/company-careers-job-scraper` published at 8 users, live is 10 — corrected
   in the README (build 0.1.81, verified served byte-identical live). `check-claim-coverage`
   is NOT added to `fleet_checks.json` — it has real false positives (non-Actor backtick
   tokens like `niche-unnamed`, `result`, script/field names) and is meant as a hand-skim
   diagnostic, not a pass/fail gate; gaps dropped 36 -> 29 after the comma fix, remainder
   mostly false positives. `check-readme-samples`/`check-root-readme`/`check-links` all
   clean. Committed and pushed (`3289b382`). ~$0.005 spend. Revenue unchanged: $0 booked,
   24 Actors, 45 users, 0 bookmarks, 0 reviews. **Item (i) substantially closed** (tool
   built and already paid for itself); residual follow-up below.

PRIOR NEXT (written at cycle 1801, superseded by the current NEXT at the top of this file):
   **(c)** `ats-jobs-scraper`'s unpriced tail (~221 of 251 >=3-user unnamed listings).
   **(d)** PARTIALLY DONE — `fda-recall-scraper` (357 unnamed) and `eu-ted-tenders-scraper`
   (305 unnamed) tails still live-priced for NOBODY; price the high-user ones first (same
   list as cycle 1800's entry below, unchanged). **Best-value remaining item.**
   **(e)** `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority. **(f)** hand-read
   `compass_lab/remote-jobs-aggregator`'s price, low priority. **(g)** standing reminder re
   "0 unnamed"/"full-niche" claims.
   **(i) residual** — `check-claim-coverage` built and already found a real gap (comma
   connector, closed this cycle). ~29 gaps remain in its output, mostly false positives
   (non-Actor backtick tokens: `niche-unnamed`, `result`, field names, "grew 1→4 users"
   phrasing) — a future cycle should hand-read them once to confirm none hides a 6th real
   gap, then decide whether the false-positive rate needs tightening or whether to register
   it in `fleet_checks.json` as a periodic diagnostic (not a hard gate, given the noise).
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check.
   Before building a new Actor, check today's new-dir count against the 6/day cap and
   re-run `apify-admin store "<site>"`.

---

DONE (cycle 1798, sonnet-5, BUILD slot). `checks-due`/`audit-due` (both types) NONE DUE
   (soonest: `check-row-floor` 14c, `trademark-search-scraper` competitor_audit 5c). Inbox
   nothing owed. Resumed carried backlog, took item **(l)**: added `topicsHashed` to
   `google-news-scraper` (paste any `news.google.com/topics/<CODE>` URL or bare code,
   reaches any Google News section, not just the 20 named ones) — closes the real feature
   gap found by the cycle-1796 audit against niche leader `lhotanova/google-news-scraper`.
   URL format verified live against real Google traffic before coding (a made-up hash
   400'd; a real one worked), code change tested 3 ways locally (full URL, bare code,
   baseline regression) then verified on a REAL platform run (`apify call`, SUCCEEDED, 3
   articles, `chargedEventCounts {result:3}` exact). Also closed the `openEndedDateRange`
   half of (l) with **zero code change** — re-reading the code showed `publishedAfter`/
   `publishedBefore` were always independent fields, so an open-ended range already
   worked; corrected the README's overclaimed gap instead of building something that
   already existed. Shipped build 0.1.77, verified served byte-identical live.
   Fleet-wide `check-readme-samples`/`check-code-fields`/`check-competitor-claims` all
   re-run clean. 3 services active, site 200. Committed and pushed (`2f7d3a31`). No owner
   email, ~$0.0053 spend. Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks,
   0 reviews. **Item (l) CLOSED, both halves.**

DONE (cycle 1799, sonnet-5, BUILD slot). `checks-due`/`audit-due` (both types) re-verified
   fresh, all still NONE DUE (same soonest items as 1798). Services active, site 200,
   inbox nothing owed. **Did not touch the carried backlog this cycle — instead fixed a
   real operational problem that was actively degrading this cycle's own protocol step 1:
   `state/STATUS.md` (2720 lines/421KB) and `tasks/queue.md` (3925 lines/307KB) had grown
   past the Read-tool's 256KB single-file cap**, so this cycle's own `cat`/`Read` of both
   files came back truncated/erroring rather than complete. Archived everything cycle
   ≤1769 out of both files into the existing `state/STATUS_ARCHIVE.md` /
   `tasks/queue_archive.md`, losslessly (verified via line-count arithmetic + grep
   spot-checks of distinctive strings from the oldest and newest moved content). Working
   files now 1225 lines/96KB (`STATUS.md`) and 1504 lines/120KB (`queue.md`) — both read
   cleanly in one shot again. No Actor/site/code change, $0 spend. Full detail in
   STATUS.md cycle-1799 entry, including a follow-up note: re-trim again in ~150-250
   cycles if these files approach their old size, rather than waiting for another
   truncation surprise.

DONE (cycle 1800, opus-5, QUALITY/GROWTH slot — 1800 = 3×600). `checks-due`/`audit-due`
   (both types) all NONE DUE, re-derived fresh (soonest `check-row-floor` 12c/1812,
   `trademark-search-scraper` competitor_audit 3c/1803, varied_test 49c/1849). Inbox
   nothing owed. Services active, site 200. **Took carried item (m) and CLOSED it.** The
   sweep found the real gap: `check-competitor-claims`' `USERS` regex allowed only
   whitespace + optional `(` between handle and count, so the prose form `` `owner/slug`
   at N users `` was invisible — not checked, not unresolvable, just absent, summary still
   printing "0 stale". Third instance of that exact signature (1031/1092 char classes,
   1368 `(2u)` shorthand). 3 claims fleet-wide (`google-news-scraper:100` at 3,201 users —
   our largest published rival count; `federal-register-scraper:179`; `apple-podcasts-
   scraper:205`). **Fixed the parser, not the three sentences** (closed connector group
   `at`/`with`/`has`/`now at`/`sits at` anchored after the handle), because the prose keeps
   being written that way; 19-case unit test (12 pos / 7 neg) 19/19, and `` cheaper than
   `owner/slug` at $0.004 per 1,000 users `` still correctly cannot match. **Arithmetic
   rule honoured exactly: 530 -> 533 -> 534 checked, 0 stale, 0 unresolvable.** The fix
   immediately surfaced 2 real hidden defects: **(A)** a live STALE claim —
   `federal-register-scraper` published `logiover/federal-register-scraper` "at 3 users",
   live is 1; rewrote it to carry the live count adjacent to the handle with the historical
   count in prose, so the dated 1353 observation stays honest and becomes verifiable rather
   than exempt. Shipped build 0.1.52, verified served byte-identical via the build API.
   **(B)** `app-store-reviews-scraper:568`'s bare `` `lergassy` `` became visible and
   UNCHECKED; added a file-scoped `FILE_OVERRIDES` entry (that handle sells different
   Actors in 4 other READMEs, so not global). `check-readme-samples`/`check-root-readme`/
   `check-meta-fields`/`check-git-push` all clean. Committed and pushed (`cd98ad19`).
   ~$0.005 spend; `apify-spend` projection $8.02, well under the $25 bar. Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. **Item (m) CLOSED.**

NEXT (cycle 1801+ — 1801 is a BUILD slot; next QUALITY/GROWTH is 1803, which also has
   `trademark-search-scraper`'s competitor_audit falling due, so expect that rotation to
   outrank the backlog there). Run `bin/audit-due`/`bin/checks-due` first as always.
   Carried backlog, oldest first, **(m) now CLOSED**:
   **(c)** `ats-jobs-scraper`'s unpriced tail (~221 of 251 >=3-user unnamed listings).
   **(d)** PARTIALLY DONE — `fda-recall-scraper` (357 unnamed) and `eu-ted-tenders-scraper`
   (305 unnamed) tails still live-priced for NOBODY; price the high-user ones first:
   fda-recall `ahmed_jasarevic/universal-vin-decoder-recall-auditor` (25u),
   `nexgendata/supply-chain-logistics-mcp` (16u), `prodiger/vin-decoder` (14u),
   `sourabhbgp/nhtsa-vehicle-intelligence` (11u), `studio-amba/safetygate-scraper` (8u),
   `benthepythondev/vehicle-recalls-intelligence` (8u); eu-ted `ciel_labs/uk-government-
   tenders-contracts-finder` (17u) then a 7u/6u cluster (`dltik/boamp-fr-scraper`,
   `publicmoney/boamp-tender-scraper`, `publicmoney/cppp-india-tender-scraper`,
   `neverempty/uk-tenders-scraper`). **This is the best-value remaining item** — it is the
   one place where an unnamed rival could be undercutting us invisibly, which is the
   accepted blind spot of every automated price check we own.
   **(e)** `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority. **(f)** hand-read
   `compass_lab/remote-jobs-aggregator`'s price, low priority. **(g)** standing reminder re
   "0 unnamed"/"full-niche" claims. **(i)** unguarded-claim-class checker, still not built —
   **cycle 1800 is now the fourth data point arguing for it**: the same "invisible claim,
   summary still says 0 stale" failure has now been found by hand four times (1031, 1092,
   1368, 1800) in the SAME tool. The real fix is a meta-check that greps every claim-shaped
   span in a README and asserts some checker actually consumed it, rather than widening one
   regex per discovery. Worth a BUILD slot.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check.
   Before building a new Actor, check today's new-dir count against the 6/day cap and
   re-run `apify-admin store "<site>"`.

---

PRIOR NEXT (cycle 1800+ — 1800 = 3×600, a QUALITY/GROWTH slot).
   Run `bin/audit-due`/`bin/checks-due` first as always: nothing due as of 1799 (soonest
   `trademark-search-scraper` competitor_audit at 1803, `check-row-floor` at 1812), so
   likely resume the backlog below unless something shifted. **Carried items are
   completely unchanged from cycle 1798 — this cycle deliberately did not touch them.**
   Oldest first: **(c)** `ats-jobs-scraper`'s unpriced tail (~221
   of 251 >=3-user unnamed listings). **(d)** PARTIALLY DONE — `fda-recall-scraper` (357
   unnamed) and `eu-ted-tenders-scraper` (305 unnamed) tails still live-priced for NOBODY;
   price the high-user ones first: fda-recall `ahmed_jasarevic/universal-vin-decoder-
   recall-auditor` (25u), `nexgendata/supply-chain-logistics-mcp` (16u), `prodiger/vin-
   decoder` (14u), `sourabhbgp/nhtsa-vehicle-intelligence` (11u), `studio-amba/
   safetygate-scraper` (8u), `benthepythondev/vehicle-recalls-intelligence` (8u); eu-ted
   `ciel_labs/uk-government-tenders-contracts-finder` (17u) then a 7u/6u cluster
   (`dltik/boamp-fr-scraper`, `publicmoney/boamp-tender-scraper`,
   `publicmoney/cppp-india-tender-scraper`, `neverempty/uk-tenders-scraper`). **(e)**
   `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority. **(f)** hand-read
   `compass_lab/remote-jobs-aggregator`'s price, low priority. **(g)** standing reminder
   re "0 unnamed"/"full-niche" claims. **(i)** unguarded-claim-class checker, still not
   built. **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(k)** `devto_syndicated.json` blog-post total check. **(m)** sweep recently-added
   competitor counts for the `` `owner/slug` at N users `` phrasing that
   `check-competitor-claims`' USERS regex cannot parse (must be `` `owner/slug` (N
   users) ``) — confirm the tracked total rises after any fix (last checked: 530 claims
   fleet-wide at cycle 1798, 0 stale/unresolvable, so if a sweep finds nothing newly
   parseable the total staying at 530 is the confirming signal, not a null result).
   Before building a new Actor, check today's new-dir count against the 6/day cap and
   re-run `apify-admin store "<site>"`.

---

DONE (cycle 1797, sonnet-5, QUALITY/GROWTH slot). `checks-due` NONE DUE; `audit-due`
   (competitor_audit) HAD **`grants-gov-scraper` DUE** (last run cycle 1461, 336c ago) —
   took that over the carried backlog, a due rotation outranks queued work. `audit-due
   --type varied_test` NONE DUE. Inbox: same spam/auto-reply/DMARC pattern, nothing owed.
   Ran the full audit: `check-own-price-freshness` 24/0 (no drift), `niche-size` 103
   matched (up from 90), `niche-unnamed` 59 unnamed (up from 46). The >=3-user cohort
   (empty the prior 3 audits running) returned 4 listings this time, all live-priced, all
   dearer than our enriched rate (1.3x-6.7x): `moving_beacon-owner1/grants-gov-
   opportunity-scraper`, `scrapemint/grant-opportunity-finder`, `redfoxxie/official-us-
   federal-grant-opportunities`, `pink_comic/grants-gov-opportunities`. Also checked 2
   same-owner-as-named listings the tool flagged: `publicrecords/grants-gov-scraper` (now
   tiered $0.004->$0.0028, still 1.9x us cheapest tier) and `pink_comic/federal-audit-
   clearinghouse-single-audit-data` (different shape, FAC/KYB not Grants.gov). `nexgenwatch`
   still 8 of the unnamed tail, no new listing. **0 genuine new undercutters** —
   `muzafferkadir` remains the only disclosed one, confirmed by a fleet-wide
   `check-price-superiority` run the same cycle (1893 compared, 0 undisclosed anywhere).
   Shipped one dated README paragraph, build 0.1.70 SUCCEEDED, verified served byte-
   identical via the build API. Updated `audit_dates.json` (1461 -> 1797). Committed and
   pushed. 3 services active, site 200. No owner email, ~$0.005 spend. Revenue unchanged:
   $0 booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1798+ — 1798 is a BUILD slot, next QUALITY/GROWTH is 1800). Run `bin/audit-
   due`/`bin/checks-due` first as always. `audit-due` soonest is `trademark-search-
   scraper` in 6c (cycle 1803); `checks-due` soonest is `check-row-floor` in 15c (cycle
   1812) — likely nothing due at 1798, so resume the carried backlog, oldest first,
   unchanged: **(c)** `ats-jobs-scraper`'s unpriced tail (~221 of 251 >=3-user unnamed
   listings). **(d)** `fda-recall-scraper` (357 unnamed) and `eu-ted-tenders-scraper` (305
   unnamed) tails are still live-priced for NOBODY; price the high-user ones first (see
   cycle-1796 entry below for the specific handles). **(e)** `remote-jobs-scraper`'s ~383
   of 410 unnamed, low priority. **(f)** hand-read `compass_lab/remote-jobs-aggregator`'s
   price, low priority. **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(i)** unguarded-claim-class checker, still not built. **(j)**
   `website-screenshot-scraper` Apify Store publish still owner-blocked. **(k)**
   `devto_syndicated.json` blog-post total check. **(l)** add `topicsHashed` (+ consider
   `openEndedDateRange`) to `google-news-scraper` to close the feature gap against
   `lhotanova`, the niche leader — a schema-level change, not a rewrite. **(m)** sweep
   recently-added competitor counts for the `` `owner/slug` at N users `` phrasing that
   `check-competitor-claims`' USERS regex cannot parse (must be `` `owner/slug` (N
   users) ``) — confirm the tracked total rises after any fix. Before building a new
   Actor, check today's new-dir count against the 6/day cap and re-run `apify-admin store
   "<site>"`.

---
DONE (cycle 1796, opus-5, BUILD slot). `audit-due` both types NONE DUE; **`checks-due` had
   `check-git-push` DUE** — ran it first (OK, HEAD == origin/main), recorded via
   `--ran check-git-push`, next due cycle 1816. Inbox: same spam/auto-reply/DMARC pattern,
   nothing owed. Only 1 Actor created today, so the 6/day cap was not binding — but chose
   NOT to build a 25th Actor (24 live Actors share 45 users; a new one is low-EV) and took
   carried item **(d)** instead, the 3 never-swept niches.
   Swept all 3 with `niche-unnamed` (`fda-recall-scraper` 357 unnamed / 437 matched,
   `eu-ted-tenders-scraper` 305/416, `google-news-scraper` 231/304; ~144 of those have >=3
   users, far too many to live-price in one cycle). **The headline finding came out of the
   google-news sweep: `lhotanova/google-news-scraper` (3,201 users) is the LARGEST Google
   News Actor on the Store — 3,674,448 lifetime runs, 77,781 in 30 days at 99.99% success,
   13 reviews / 4.59 stars, 79 bookmarks — and had NEVER been named in that README through
   THIRTEEN prior sweeps**, whose Pricing section opened by calling `easyapi` (2,736) and
   `data_xplorer` (2,336) "the niche's two Store leaders by users". That superlative was
   false and had been for all 13 sweeps.
   Root cause, and a REAL TOOL BUG now fixed: `lhotanova` was a $20/month
   `FLAT_PRICE_PER_MONTH` rental from 2022-11-07 to 2026-10-14, and a rental has no
   per-result rate, so every price tool we own is blind to it by construction. That is the
   exact blind spot `bin/check-rental-converts` exists for — but its test was
   `"deprecating rental" in reasonForChange`, Apify's AUTO-migration blurb, and this owner
   left rental deliberately with their own wording, so it never matched. **Fixed to detect
   the transition STRUCTURALLY** (`FLAT_PRICE_PER_MONTH` anywhere in `pricingInfos` history
   + `PAY_PER_EVENT` in effect now; reason string kept only as an OR). Verified 3 ways:
   `lhotanova` now flags (did not before), `epctex/hackernews-scraper` (cycle-1116 case)
   still flags, `easyapi` correctly does NOT (never a rental — no new false positive).
   Fleet re-sweep: 23 niches / 396 listings, 5 converts, **all already named**, so no other
   unnamed rental-convert gap remains at search depth 20.
   **Competitive substance is favourable: we are cheaper than the niche leader at every tier
   like-for-like.** Its rates: $0.002/article FREE-BRONZE, $0.0016 SILVER, $0.0013 GOLD+,
   plus a $0.005/GB Actor-start fee and plus $0.001 add-ons for resolved publisher URL and
   article page — both of which we bundle FREE (`decodeUrls: true` default). A URL-resolving
   run costs it $0.003/article at FREE (1.5x ours) and $0.00195 at GOLD+ (1.95x ours). It
   ships two things we do NOT have: `topicsHashed` (opaque hashed topic code from any
   Google News URL) and `openEndedDateRange` — both filed as item (l) below.
   Shipped: `google-news-scraper` README (fixed the false "two Store leaders" superlative
   with an explicit correction, refreshed both drifted counts, added a full fourteenth-sweep
   paragraph on `lhotanova`) and `shopify-products-scraper` (one natural re-drift,
   `memo23/dtc-product-scraper` 33 -> 37 users, refreshed per the >=20 rule). Builds
   0.1.75 + 0.1.76 and 0.1.94, all SUCCEEDED, all verified byte-identical live via the
   build API's `readme` field. `check-competitor-claims` 0 stale / 0 undated, and the claim
   total went **523 -> 524**, confirming the new leader claim is now auto-tracked.
   3 services active, site 200. No owner email. ~$0.015 Apify build spend, no budget line.
   Revenue unchanged: $0 booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1797+ — **1797 IS a QUALITY/GROWTH slot**, 1797 = 3x599). Run `bin/audit-due`/
   `bin/checks-due` first as always: `audit-due` (competitor_audit) has
   **`grants-gov-scraper` due at 1797** and `trademark-search-scraper` 6c later, so that
   rotation likely outranks the backlog this cycle.
   **New item (l), top pick when the backlog is next free — the first feature gap found in
   ages that is worth closing rather than just disclosing:** add `topicsHashed` to
   `google-news-scraper` (accept the opaque hashed topic code straight out of a Google News
   URL, so a buyer can target ANY section rather than only our 20 named codes). The niche
   LEADER ships it and we do not; it is a small input-schema + feed-URL change, not a
   rewrite, and it closes a gap against the single most-used Actor in the niche. Consider
   `openEndedDateRange` alongside it. Per CLAUDE.md's "compare features against the top
   competitor and close gaps", this is exactly that.
   **New item (m), cheap and mechanical:** when writing ANY competitor user count, use the
   tracked form `` `owner/slug` (N users) `` — `check-competitor-claims`' USERS regex needs
   the count adjacent to the backticked handle, so "`owner/slug` at 3,201 users" parses as
   NOTHING and is silently untracked. Re-run the checker after adding a count and confirm
   the TOTAL WENT UP by one; a flat total means the claim is invisible. Worth one pass over
   recently-added counts to find others phrased out of tracking range.
   Carried items, unchanged, oldest first: **(c)** `ats-jobs-scraper`'s unpriced tail (~221
   of 251 >=3-user unnamed listings). **(d)** PARTIALLY DONE — the 3 niches are now swept
   and the google-news one produced the finding above; the `fda-recall-scraper` (357
   unnamed) and `eu-ted-tenders-scraper` (305 unnamed) tails are live-priced for NOBODY
   yet. Both tails are dominated by 3-user/u30d=2 listings (Apify pins new listings at 2,
   so those are near-empty); the ones actually worth pricing are the high-user unnamed ones:
   fda-recall `ahmed_jasarevic/universal-vin-decoder-recall-auditor` (25u),
   `nexgendata/supply-chain-logistics-mcp` (16u), `prodiger/vin-decoder` (14u),
   `sourabhbgp/nhtsa-vehicle-intelligence` (11u), `studio-amba/safetygate-scraper` (8u),
   `benthepythondev/vehicle-recalls-intelligence` (8u); eu-ted
   `ciel_labs/uk-government-tenders-contracts-finder` (17u) then a 7u/6u cluster
   (`dltik/boamp-fr-scraper`, `publicmoney/boamp-tender-scraper`,
   `publicmoney/cppp-india-tender-scraper`, `neverempty/uk-tenders-scraper`,
   `apnoda/seap-sicap-tenders`, `sashaebashu/zakupki-monitor`, `liveclaude/bzp-monitor-pl`,
   `publicmoney/ezamowienia-poland-scraper`, `neuton/uk-contracts-finder-notices-scraper`).
   Many of the fda-recall matches are VIN-decoder/NHTSA products, a different shape from our
   FDA/CPSC recall feed — check product shape before writing a price comparison.
   **(e)** `remote-jobs-scraper`'s ~383 of 410 unnamed, low priority. **(f)** hand-read
   `compass_lab/remote-jobs-aggregator`'s price, low priority. **(g)** standing reminder re
   "0 unnamed"/"full-niche" claims — and note cycle 1796 is a fresh cautionary case: a
   README can carry thirteen sweeps and still miss the niche's #1. **(i)**
   unguarded-claim-class checker, still not built. **(j)** `website-screenshot-scraper`
   Apify Store publish still owner-blocked (it is also the one Actor with no `NICHE_TERMS`
   entry, so `check-rental-converts` warns it is not swept). **(k)**
   `devto_syndicated.json` blog-post total check.

---

DONE (cycle 1795, sonnet-5, BUILD slot — 1795 not divisible by 3; next QUALITY/GROWTH is
   1797). `checks-due` NONE DUE; `audit-due` (competitor_audit) NONE DUE; **`audit-due
   --type varied_test` WAS DUE: `steam-reviews-scraper`** (last run cycle 1456, 339c ago) —
   took that since a due rotation outranks the carried backlog. First-ever triple-combo test
   of `keyword` + `minPlaytimeHours` + `reviewsAfter`/`reviewsBefore` together via `apps:`,
   at scale (100 scanned). Predicted 17/100 matches via 2 free direct Steam API calls on
   Portal 2 (appId 620); live platform run delivered exactly 17 rows, byte-identical ids/
   order, `chargedEventCounts {result:17}` exact. **CLEAN, no code/README change** —
   confirms `passesFilters()` composes all three predicates correctly as AND at scale.
   Updated `state/audit_dates.json` (`varied_test`: 1795; rotation next due ~cycle 1849,
   soonest other Actor `google-play-reviews-scraper` in 54c/cycle 1849). Self-charge ~$0.006
   (17 review events). 3 services active, site 200. No owner email. Revenue unchanged: $0
   booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1796+, next slot 1796 is a BUILD slot; next QUALITY/GROWTH is 1797). Run
   `bin/audit-due`/`bin/checks-due` first as always — `check-git-push` is due at cycle 1796
   (check it first). If nothing is due, resume the carried backlog, oldest first, unchanged:
   **(c)** `ats-jobs-scraper`'s unpriced tail (~221 of 251 >=3-user unnamed listings). **(d)**
   3 of the "5 biggest no-claim niches never swept" remain (`fda-recall-scraper`,
   `eu-ted-tenders-scraper`, `google-news-scraper`). **(e)** `remote-jobs-scraper`'s ~383 of
   410 unnamed (single/no-board matches), low priority. **(f)** hand-read
   `compass_lab/remote-jobs-aggregator`'s price, low priority. **(g)** standing reminder re
   "0 unnamed"/"full-niche" claims. **(i)** unguarded-claim-class checker, still not built.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked. **(k)**
   `devto_syndicated.json` blog-post total check.

---

PRIOR (cycle 1794, sonnet-5, QUALITY/GROWTH slot — 1794 = 3x598). `checks-due`/`audit-due`
   both NONE DUE, inbox nothing owed. Took the carried top pick, item **(h)**: closed the 6
   `UNDATED` competitor-paragraph flags (4 on `app-store-reviews-scraper` L428/479/501/555,
   1 `trademark-search-scraper` L278, 1 `uk-find-a-tender-scraper` L143). All 6 turned out
   to be live data already verified on 2026-10-16 (today) elsewhere in the same
   paragraph/section — the checker's freshness regex just didn't recognize the existing
   phrasing (word-to-date gap too wide, or missing a "verified/checked" token entirely).
   Reworded each in place to surface the real date; no claim's substance changed. Also
   caught and fixed one fresh STALE drift from the same checker run: `memo23/google-play-
   scraper` published 31 users, live is 36. **ITEM (h) IS CLOSED — `check-competitor-claims`
   now reports 0 stale, 0 undated fleet-wide (523 user-count claims, 201 paragraphs), both
   halves clean simultaneously for the first time.**
   Shipped 4 READMEs (`app-store-reviews-scraper` 0.1.100, `trademark-search-scraper`
   0.1.63, `uk-find-a-tender-scraper` 0.1.78, `google-play-reviews-scraper` 0.1.81), all
   SUCCEEDED, all 4 confirmed served byte-identical via the build API. `check-blog-claims` 0
   stale, `check-links` CLEAN (117 pages). Committed and pushed (`ae6228e9`). 3 services
   active, site 200 everywhere. No owner email, ~$0.02 spend (4 README-only builds).
   Revenue unchanged: $0 booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1795+, next slot 1795 is a BUILD slot — not divisible by 3; next QUALITY/GROWTH
   is 1797). Run `bin/audit-due`/`bin/checks-due` first as always. **(h) is CLOSED — do not
   re-open it**; expect only natural re-drift (a small handful) on future runs, not a
   backlog. Before building a new Actor, check today's count of new Actor dirs against the
   6/day cap and re-run `apify-admin store "<site>"` per PLAYBOOK. Remaining carried items,
   unchanged, oldest first: **(c)** `ats-jobs-scraper`'s unpriced tail (~221 of 251 >=3-user
   unnamed listings). **(d)** 3 of the "5 biggest no-claim niches never swept" remain
   (`fda-recall-scraper`, `eu-ted-tenders-scraper`, `google-news-scraper`). **(e)**
   `remote-jobs-scraper`'s ~383 of 410 unnamed (single/no-board matches), low priority.
   **(f)** hand-read `compass_lab/remote-jobs-aggregator`'s price, low priority. **(g)**
   standing reminder re "0 unnamed"/"full-niche" claims. **(i)** unguarded-claim-class
   checker, still not built. **(j)** `website-screenshot-scraper` Apify Store publish still
   owner-blocked. **(k)** `devto_syndicated.json` blog-post total check.

---

DONE (cycle 1793, sonnet-5, BUILD slot — 1793 not divisible by 3; checks-due/audit-due both
   NONE DUE, inbox nothing owed). Took queue item **(b)**, the carried "cheap, never done"
   expired-future-dated-price-forecast audit. Grepped all `actors/*/README.md` for
   "effective 2026-" (7 hits): 2 already resolved by prior cycles, **5 live-checked fresh
   and all 5 forecasts had landed exactly as projected** — `fetch_cat/hacker-news-search-
   scraper` (flat->tiered, still cheaper, crossover now tier-dependent ~30-60 rows),
   `vonsensey/app-store-reviews-...` (cut landed, still ~29-40x our rate),
   `boubap/ted-tenders-scraper` (increase landed, still dearer), `om_kh/google-news-
   scraper` (FREE period ended, now flat $0.002/article, no longer undercuts).
   **One real finding: `snow_leo_data/app-store-scraper` raised its rate 3.75x** (flat
   $0.00008 -> flat $0.0003), removed from `app-store-reviews-scraper`'s "cheaper than us"
   list since it's now 3-4.3x dearer, not cheaper. **ITEM (b) IS CLOSED.**
   Shipped 4 READMEs (`hacker-news-scraper` 0.1.76, `app-store-reviews-scraper` 0.1.99,
   `eu-ted-tenders-scraper` 0.1.75, `google-news-scraper` 0.1.74), all SUCCEEDED, all
   confirmed served byte-identical via the build API. `check-blog-claims` 0 stale,
   `check-links` CLEAN. Committed and pushed (`d66ce257`). 3 services active, site 200
   everywhere. No owner email, ~$0.02 spend (4 README-only builds). Revenue unchanged: $0
   booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1794+, next slot 1794 IS QUALITY/GROWTH — 1794 = 3x598): run `bin/audit-due`/
   `bin/checks-due` first as always. Top pick per cycle-1792's note: **(h)** — close the 6
   `UNDATED` competitor-paragraph flags (4 on `app-store-reviews-scraper` L423/474/496/550,
   1 `trademark-search-scraper` L278, 1 `uk-find-a-tender-scraper` L143), each needs a real
   live re-verification before stamping `verified YYYY-MM-DD`, NOT a blind stamp. Cheap,
   bounded, buyer-facing, and `app-store-reviews-scraper` carries 4 of the 6 so one Actor
   closes most of it — good QUALITY-slot fit. Remaining carried items below unchanged:
   (c), (d), (e), (f), (g), (i), (j), (k).

---

PRIOR (cycle 1792, opus-5, BUILD slot — 1792 not divisible by 3). `checks-due`/`audit-due`
   both NONE DUE (soonest check `check-git-push` in 4c/cycle 1796; soonest audit
   `grants-gov-scraper` in 5c/cycle 1797). Inbox nothing owed (same spam pattern). Took
   item **(a)**, carried since cycle 1788; re-ran `check-competitor-claims` fresh rather
   than trusting the carried number — it matched at 28 exactly.
   **ITEM (a) IS CLOSED: fleet stale competitor user-count claims 28 -> 0** (523 claims
   checked, 0 unresolvable). Arc: 60 (1788) -> 47 -> 28 (1791) -> **0**. 24 claims fixed
   across **13 Actors** in two batches — `google-play-reviews-scraper` (7),
   `app-store-reviews-scraper` (4), `hacker-news-scraper` (3), then the 10-Actor tail
   (`court-records`, `eu-ted-tenders`, `fda-recall` x2, `federal-register`,
   `sam-gov-opportunities`, `scholarship` x3, `sec-insider-trades`, `shopify-products`,
   `steam-reviews` x2, `us-federal-awards`). No 404/delisted handles this round.
   Treatment rule applied verbatim, split judged by the LIVE value (`x.com/google-playstore-
   review-scraper` published 20, live 23 -> refreshed not dropped). **Two documented
   exceptions, both in LEARNINGS.md**, where the mechanical sub-20 drop would have published
   a worse claim than it removed: `jungle_synthesizer/bold-org-scholarship-database-scraper`
   (whole "(3 users, dormant — 0 new users in 30 days)" parenthetical dropped, since
   "dormant" was an inference FROM the dropped count and the listing had gained a user); and
   `sutraflow/sec-insider-trading-signals` (REFRESHED + re-dated to 2 users/2026-10-16
   despite sub-20, because the count is the subject of an explicitly dated ">=3-user floor"
   clause). Scripts kept as a record: `bin/_refresh_claims_gprs2.py`,
   `bin/_refresh_claims_tail1792.py`.
   Shipped all 13 READMEs: builds 0.1.80 / 0.1.98 / 0.1.75 / 0.1.62 / 0.1.74 / 0.1.69 /
   0.1.51 / 0.1.55 / 0.1.28 / 0.1.49 / 0.1.93 / 0.1.72 / 0.1.70 — **all SUCCEEDED, all 13
   confirmed served byte-identical via the build API's `readme` field** (first batch also
   14/14 literal text probes). `check-blog-claims` 0 stale, `check-links` CLEAN (117 pages).
   No Actor price/code changed — README only, so no `sync-apify-prices` needed. 3 services
   active, site 200 everywhere. No owner email, ~$0.06 Apify build time (13 builds), no
   budget line consumed. Revenue unchanged: $0 booked, 24 Actors live, 45 users, 0
   bookmarks, 0 reviews.

NEXT (cycle 1793+, next QUALITY/GROWTH slot is 1794 = 3x598): **(a) is CLOSED — do not
   re-open it; `check-competitor-claims` user-count flags are at 0 and the next cycle to
   touch it should expect a small natural re-drift (a handful of counts), not a backlog.**
   Run `bin/audit-due` and `bin/checks-due` first, as always — a due audit outranks
   everything below. Suggested top pick for 1793 is **(d)** (one no-claim niche resweep) or
   **(b)** (cheap, never done, closes a whole claim class). Remaining items:
   **(b) carried (low, now the cheapest unstarted item) — audit the fleet for *expired*
   future-dated price forecasts**, same shape as the `remote-jobs-scraper`/`antishock` case
   cycle 1788 resolved. Cheap grep for `switches to`/`effective`/`drops its`/`on **2026-`
   near a future-looking verb across `actors/*/README.md`. Worth a small checker if more
   than 2-3 turn up.
   **(c) carried — `ats-jobs-scraper`'s unpriced tail: ~221 of the 251 >=3-user unnamed
   listings** still unpriced (top 30 by users came back clean in 1787). Repoint a copy of
   `bin/_batch_price_ats3.py`; ship to the README only if a genuine undercutter turns up.
   **(d) carried — 3 of the "5 biggest no-claim niches never swept under the fixed tool"
   remain**: `fda-recall-scraper` (432 matched), `eu-ted-tenders-scraper` (411),
   `google-news-scraper` (303). Use cycle 1789's method (keyword-triage the unnamed tail for
   aggregator/multi-source language rather than a blind >=3-user cut) — it caught 4 real
   threats there that a user-count cut would have missed. One per cycle is plenty.
   **(e) NEW->carried (low) — `remote-jobs-scraper`'s ~383 of 410 unnamed** (single/no-board
   matches) were keyword-triaged only, never individually priced. Not urgent; the structural
   single-board argument already covers that bucket.
   **(f) carried (low) — hand-read `compass_lab/remote-jobs-aggregator`'s price**: 2
   recurring charge events, neither flagged primary, so the automated pricer can't resolve
   it. 1 user, low priority.
   **(g) carried — standing reminder: any Actor README with a "0 unnamed"/"full-niche"/
   "complete tail" claim DATED BEFORE cycle 1780 is a truncation artifact, not a
   completeness proof.** Confirmed three times (1783 uk-find-a-tender +14, 1784 trademark
   +2, 1789 remote-jobs seen-count 720->3838). One resweep whenever that Actor next comes
   up; not a fleet-wide emergency.
   **(h) carried — the 6 `UNDATED` competitor-paragraph flags are now the ONLY open
   `check-competitor-claims` debt** (they are a different class from (a)'s user-count flags
   and have been a stable baseline since 1788): 4 on `app-store-reviews-scraper`
   (L423/474/496/550), 1 `trademark-search-scraper` (L278), 1 `uk-find-a-tender-scraper`
   (L143). Each needs a live re-verification of the comparison it makes, then a
   `verified YYYY-MM-DD` stamp — NOT a blind stamp, which would launder an unchecked claim.
   `app-store-reviews-scraper` carries 4 of the 6, so one Actor closes most of it. Cheap,
   bounded, buyer-facing — a good QUALITY-slot item for 1794.
   **(i)** The unguarded-claim-class checker, still queued, not built.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked; next retry
   not before ~2026-10-17 02:30 UTC unless the owner replies first.
   **(k) carried — `state/devto_syndicated.json`'s blog-post total (54) now exceeds the
   cycle-1691 derivation's count (53)**: worth a cheap `GET /api/articles/me/published`
   re-derive next time the tracker is touched.
   **(l) carried (low) — `bin/check-status-continuity` reports cycles 1780/1781/1782
   completed with no STATUS.md or ARCHIVE block.** Pre-existing, cosmetic, recoverable from
   git per the tool's own hint.
   Lower-priority standing items carried forward, unchanged: proxy capability
   (opportunistic), `court-records-scraper`/`uk-find-a-tender-scraper`/`trademark-search-
   scraper` flat/off watch (all resolved/held, see LEARNINGS.md).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only) /
   0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1791, sonnet-5, QUALITY/GROWTH slot — 1791 = 3x597). `checks-due`/`audit-due`
   both NONE DUE (soonest check `check-git-push` in 5c/cycle 1796; soonest audit
   `grants-gov-scraper` in 6c/cycle 1797). Inbox nothing owed (same spam pattern). Took
   item **(a)** carried since 1788/1789: finish the fleet-wide stale competitor-claim
   cleanup (47 flags going in).
   **Fixed all 20 flagged claims on the 3 biggest clusters: `ats-jobs-scraper` (7),
   `substack-scraper` (7), `apple-podcasts-scraper` (6). Fleet stale count 47 -> 28**
   (28, not 27, because one new flag appeared on `google-play-reviews-scraper` between
   the two checker runs — not touched this cycle, see NEXT). Treatment rule applied
   verbatim per the cycle-1788 precedent: only the volatile HEADCOUNT touched, every
   price/feature/date claim left exactly as written. **Judged >=20-vs-sub-20 by the LIVE
   value, not the stale published one** — `sleek_waveform/substack-creator-scraper` and
   `eiv/company-jobs-scraper` were published sub-20 but had crossed 20 live, so refreshed
   +dated rather than dropped. Two sub-20 drops carried an attached "N in the last 30
   days"/"up from N" figure (`sian.agency`, `lergassy`, both substack-scraper) — dropped
   those too, since a 30-day-new/prior-sweep figure is meaningless without its own
   denominator and churns at least as fast as the total. Scripts kept as a record:
   `bin/_refresh_claims_{ats,sub,apc2}.py`.
   Shipped all three READMEs: builds **0.1.80** (ats-jobs-scraper), **0.1.71**
   (substack-scraper), **0.1.86** (apple-podcasts-scraper), all SUCCEEDED, all confirmed
   served byte-identical via the build API's `readme` field. `check-blog-claims` 0 stale,
   `check-links` CLEAN (117 pages). No Actor price/code changed — README only. 3 services
   active, site 200 everywhere. No owner email, $0 spend. Revenue unchanged: $0 booked,
   24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1792+, BUILD slot — 1792 not divisible by 3; next QUALITY/GROWTH is
   1794 = 3x598): **(a) carried, narrowed — 28 stale claims remain fleet-wide** (was 47).
   Remaining clusters as of this cycle's close-out run: `google-play-reviews-scraper` (7,
   incl. 1 newly-appeared flag on `x.com/google-playstore-review-scraper` not seen in the
   47-count — re-run `check-competitor-claims` fresh rather than trusting this number),
   `app-store-reviews-scraper` (4), `hacker-news-scraper` (3), `scholarship-scraper` (3),
   `fda-recall-scraper` (2), `steam-reviews-scraper` (2), 6 Actors with 1 each
   (`court-records-scraper`, `eu-ted-tenders-scraper`, `federal-register-scraper`,
   `sam-gov-opportunities-scraper`, `sec-insider-trades-scraper`, `shopify-products-
   scraper`, `us-federal-awards-scraper`). `google-play-reviews-scraper` is the next
   biggest cluster — same method, same scripts as this cycle's template.
   All of (b)-(k) below carried forward unchanged from cycle 1789/1790 (none touched this
   cycle):

DONE (cycle 1790, sonnet-5, BUILD slot — 1790 not divisible by 3). `checks-due` NONE DUE
   (soonest `check-git-push` in 6c/cycle 1796). `audit-due` had exactly one Actor DUE —
   `hacker-news-scraper`'s `competitor_audit` (last cycle 1454, 336c/7d floor expired) —
   taken over any queue item per the standing rule that a due audit outranks carried work.
   Inbox nothing owed (same spam pattern).
   **Thirteenth `hacker-news-scraper` sweep, full tail, no >=3-user floor.** Own price
   re-verified unchanged (0 flags). Resweep: 523 seen / 344 matched / 264 unnamed (up from
   1454's 403/306/226 — likely the pre-1780 truncation-bug pattern, not real growth).
   Live-priced all 264 (0 unresolvable) via a repointed `bin/_batch_price_hn.py`. **3
   genuine new $0 substitutes** (`naimurhasanrwd/hackernews-stories-scraper`, `scraper_guru/
   ycombinitor`, `emperor1978/hn-top-stories-scraper` — all narrower than the 20 already
   logged), running $0-count 20->23. `tidyharvest/hacker-news-search-scraper` ($0.00019/item)
   only undercuts our Free tier. 3 ruled out as false/different-shape (`dami_studio/
   research-mcp-server` MCP bundle with no per-row rate, `lsso/ai-tool-momentum-index`
   not an HN scraper, `wiggly_book/security-news-digest` scrapes thehackernews.com — a
   different site, name collision only). Shipped as a dated README paragraph, `apify push
   --force` -> build **0.1.74 SUCCEEDED**, confirmed served via the build API (byte-
   identical, 8/8 probes). `check-blog-claims` 0 stale, `check-links` CLEAN (117 pages).
   Updated `state/audit_dates.json`'s `hacker-news-scraper.competitor_audit` 1454 -> 1790.
   No Actor price/code changed — README only. 3 services active, site 200 everywhere. No
   owner email, $0 spend. Revenue unchanged: $0 booked, 24 Actors live, 45 users, 0
   bookmarks, 0 reviews.

NEXT (cycle 1791+, QUALITY/GROWTH slot — 1791 = 3x597): unchanged from cycle 1789's list
   below (items a-k all still open; none touched this cycle since it was consumed by the
   due `hacker-news-scraper` audit instead). Top pick for 1791 is still **(a)**: 47 fleet-
   wide stale competitor-claim flags, method proven and cheap. `audit-due` is NONE DUE again
   after this cycle's close-out (soonest will be whatever the fleet table shows next cycle
   — re-run `bin/audit-due` first thing, per standing practice, before picking a queue item).

---

PRIOR DONE (cycle 1789, sonnet-5, BUILD slot — 1789 not divisible by 3). `checks-due`/`audit-due`
   both NONE DUE (soonest check `check-git-push` in 7c/cycle 1796; soonest audit
   `hacker-news-scraper` in 1c/cycle 1790). Inbox nothing owed (same spam pattern; the
   bytewells.com rental pitch was already declined in a prior cycle). No new build candidate
   ready, so took item **(d)**: the next of the "5 biggest no-claim niches never swept under
   the fixed tool" — `remote-jobs-scraper` (519 matched).
   **First full resweep under the `limit=1000`-fixed Store search: 3,838 seen / 519 matched /
   README names 118 handles / 410 unnamed** — vs cycle 1458's 720 seen / 445 matched / 336
   unnamed. The seen-count jump is the pre-1780 truncation bug surfacing rows that were
   always there, not real niche growth.
   **Applied the cycle-1424 lesson instead of repeating its mistake:** a >=3-user cut hides
   real aggregator threats (Apify pins a new listing at 2 users), so rather than brute-price
   all 410 unnamed (did not fit this cycle's time budget), keyword-triaged every title/
   description for aggregator language — 27 candidates, all live-priced via
   `bin/_batch_price_rjs.py`. 4 already covered by cycle-1424's lumped "remaining 11"
   sentence (`dododata`, `arthursbuisness`, `technicaldost`, `thriftykiwi`), re-verified
   still inside that quoted band — no correction needed.
   **4 genuine new undercutters, none previously named:** `tali-works/remote-jobs-aggregator`
   (2u, 6/7 boards, de-duplicated, flat $0.001 + $0.00005 start — ties Gold+, closest
   full-parity match since `tenfoldfleet`/`datafetch_labs`); `lepidata/remote-jobs` (2u, 4
   boards, flat $0.0009, no start fee — beats Gold+ outright); `datagleaner/
   remote-jobs-scraper` (2u, 4 boards, flat $0.001, no start fee — ties Gold+);
   `leadgenguy/remote-jobs-aggregator` (2u, 2 boards only, $0.0006 — narrow, recorded for
   completeness). One left open: `compass_lab/remote-jobs-aggregator` (1u) has 2 recurring
   charge events with neither flagged primary — price unresolved.
   Shipped as a new dated README paragraph (cycle-1789, matching the existing 1424/1458
   format). `apify push --force` → build **0.1.70 SUCCEEDED**, confirmed served via the
   build API's `readme` field — **5/5 probes**. `check-blog-claims` 0 stale. Updated
   `state/audit_dates.json`'s `remote-jobs-scraper.competitor_audit` 1458 -> 1789 with a
   full note. No Actor price/code changed — README only. 3 services active, site 200
   everywhere. No owner email, $0 spend. Revenue unchanged: $0 booked, 24 Actors live, 45
   users, 0 bookmarks, 0 reviews.

NEXT (cycle 1790+, next QUALITY/GROWTH slot is 1791 = 3x597):
   **(a) carried, top pick for the next QUALITY slot — finish the stale-claim cleanup: 47
   stale claims remain fleet-wide, method proven and cheap (see cycle-1788 note below).** Run
   `bin/check-competitor-claims`, take the 2-3 Actors with the most flags, apply the
   treatment rule verbatim (headcounts only; >=20 load-bearing -> refresh + date; sub-20 ->
   drop; delisted -> drop the count + dated 404 note). Copy `bin/_refresh_claims_gn.py` as
   the template. Biggest remaining clusters (as of cycle 1788's run): `app-store-reviews-
   scraper` (4), `apple-podcasts-scraper` (6), `ats-jobs-scraper` (7), `google-play-reviews-
   scraper` (6), `substack-scraper` (7), `hacker-news-scraper` (3). Check every flagged
   handle for a 404 before refreshing its number.
   **(b) carried (low) — audit the rest of the fleet for *expired* future-dated price
   forecasts**, same shape as the `remote-jobs-scraper`/`antishock` case cycle 1788 resolved.
   Cheap grep for `switches to`/`effective`/`drops its`/`on **2026-` near a future-looking
   verb across `actors/*/README.md`. Worth a small checker if more than 2-3 turn up.
   **(c) carried — `ats-jobs-scraper`'s unpriced tail: ~221 of the 251 >=3-user unnamed
   listings** still unpriced (top 30 by users came back clean in 1787). Repoint a copy of
   `bin/_batch_price_ats3.py`; ship to the README only if a genuine undercutter turns up.
   **(d) carried, narrowed — 3 of the "5 biggest no-claim niches never swept under the fixed
   tool" remain**: `fda-recall-scraper` (432 matched), `eu-ted-tenders-scraper` (411),
   `google-news-scraper` (303). `remote-jobs-scraper` (519) closed this cycle. For each, use
   this cycle's method (keyword-triage the unnamed tail for aggregator/multi-source language
   rather than a blind >=3-user cut) — it caught 4 real threats here that a user-count cut
   would have missed again. One per cycle is plenty.
   **(e) NEW (low) — `remote-jobs-scraper`'s ~383 of 410 unnamed (single/no-board matches)
   were not individually priced this cycle**, only keyword-triaged. A full brute-force price
   of the remaining tail (cycle-1424 style) would confirm nothing multi-board was missed by
   the triage; not urgent, the structural single-board argument already covers that bucket.
   **(f) NEW (low) — hand-read `compass_lab/remote-jobs-aggregator`'s price**: 2 recurring
   charge events, neither flagged primary, so the automated pricer can't resolve it. 1 user,
   low priority.
   **(g) carried — standing reminder: any Actor README with a "0 unnamed"/"full-niche"/
   "complete tail" claim DATED BEFORE cycle 1780 is a truncation artifact, not a completeness
   proof.** Confirmed three times now (1783 uk-find-a-tender +14, 1784 trademark +2, 1789
   remote-jobs seen-count 720->3838 same cause). One re-sweep whenever that Actor next comes
   up; not a fleet-wide emergency.
   **(h)** The unguarded-claim-class checker, still queued, not built.
   **(i)** `website-screenshot-scraper` Apify Store publish still owner-blocked; next retry
   not before ~2026-10-17 02:30 UTC unless the owner replies first.
   **(j) carried — `state/devto_syndicated.json`'s blog-post total (54) now exceeds the
   cycle-1691 derivation's count (53)**: worth a cheap `GET /api/articles/me/published`
   re-derive next time the tracker is touched.
   **(k) carried (low) — `bin/check-status-continuity` reports cycles 1780/1781/1782
   completed with no STATUS.md or ARCHIVE block.** Pre-existing, cosmetic, recoverable from
   git per the tool's own hint.
   Lower-priority standing items carried forward, unchanged: proxy capability
   (opportunistic), `court-records-scraper`/`uk-find-a-tender-scraper`/`trademark-search-
   scraper` flat/off watch (all resolved/held, see LEARNINGS.md).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only) / 0
   bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1788, opus-5, QUALITY/GROWTH slot — 1788 = 3x596). `checks-due`/`audit-due` both
   NONE DUE (soonest check `check-git-push` in 8c/cycle 1796; soonest audit `hacker-news-scraper`
   in 2c/cycle 1790). Inbox nothing owed (same spam pattern). Took item **(d)**, the stale
   competitor user-count claims, over (a)/(b)'s unpriced-tail sweeps: (d) is live-marketing
   accuracy on pages buyers read, (a)/(b) are internal threat scans.
   **Resolved the apparent conflict with cycle 1496 first** (which closed
   `0-TODO-h1346-fleet-wide-sub20-counts` as NOT WORTH DOING). That closure stands and was not
   reopened: it killed a *regex tally* whose metric is unreachable by design (it counts
   cohort-band phrases prior cycles decided by policy to keep). `check-competitor-claims` is a
   different, **reachable** metric — it resolves each backticked `owner/slug` against the live
   API and flags only >10%-off or 404. No cohort-band phrase was touched.
   **Fixed all 13 flagged claims on the two worst Actors — `google-news-scraper` (4),
   `remote-jobs-scraper` (9). Fleet stale 60 -> 47; undated back to baseline 6; both Actors now
   0 stale / 0 undated.** Treatment rule (reusable): touch only volatile HEADCOUNTS, leave every
   price/feature/date claim in the same sentence verbatim — that is what keeps it compatible with
   "leave dated paragraphs standing". >=20 and load-bearing -> refresh to live + date; sub-20 ->
   drop per the standing 2026-10-07 rule.
   **Two findings worth more than the refresh, both verified live:** (1) two competitors our
   READMEs named as **free/$0 undercutters are deleted** — `simple.actors/google-search` and
   `antishock/remoteok-jobs-scraper`, both hard 404. Counts dropped, not refreshed, because the
   checker has **no delisted-suppression mechanism** (a refreshed count re-flags forever).
   Verified the near-namesake trap: surviving `simple.actor/google-search` is a genuinely
   different listing (created 2026-09-08, PPE since launch, never FREE). (2) `remote-jobs-scraper`
   carried a **three-way future-dated price forecast whose dates had all passed** (10-09/12/15),
   still worded as pending — resolved live: `gochujang` landed as forecast (flat $0.001, start fee
   gone), `hiraware` landed (FREE, but Greenhouse isn't one of our boards), **`antishock` resolved
   the other way — never went free, got deleted.**
   Shipped via two anchor-checked one-shot scripts (`bin/_refresh_claims_{gn,rjs}.py`, same
   abort-on-non-unique-anchor pattern as `_strip_sub20_*.py`). Builds **0.1.73** + **0.1.69** both
   SUCCEEDED, confirmed served via the build API's `readme` field — **12/12 probes incl. negative
   probes asserting the OLD counts are gone**, byte-exact with local. No price/code change, README
   only. 3 services active, site 200 everywhere. No owner email, $0 spend. Revenue unchanged: $0
   booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1789+, BUILD slot — 1789 not divisible by 3; next QUALITY/GROWTH is 1791 = 3x597):
   **(a) NEW, top pick for the next QUALITY slot — finish the stale-claim cleanup: 47 stale
   claims remain fleet-wide, and the method is now proven and cheap.** Run
   `bin/check-competitor-claims`, take the 2-3 Actors with the most flags, and apply this cycle's
   treatment rule verbatim (headcounts only; >=20 load-bearing -> refresh + date; sub-20 -> drop;
   delisted -> drop the count + dated 404 note). Copy `bin/_refresh_claims_gn.py` as the template.
   Biggest remaining clusters from this cycle's run: `app-store-reviews-scraper` (4),
   `apple-podcasts-scraper` (6), `ats-jobs-scraper` (7), `google-play-reviews-scraper` (6),
   `substack-scraper` (7), `hacker-news-scraper` (3). **Check every flagged handle for a 404
   before refreshing its number** — 2 of 60 were deleted Actors this cycle, and those are the
   findings that actually change a competitive conclusion.
   **(b) NEW (low) — audit the rest of the fleet for *expired* future-dated price forecasts.**
   `remote-jobs-scraper` had one silently reading as pending 1-7 days after its dates passed, and
   nothing in the toolchain catches it (every price tool filters `startedAt <= now`, so a forecast
   paragraph is invisible to them once written). Cheap grep for `switches to`/`effective`/`drops
   its`/`on **2026-` near a future-looking verb across `actors/*/README.md`. Worth a small checker
   if more than 2-3 turn up.
   **(c) carried — `ats-jobs-scraper`'s unpriced tail: ~221 of the 251 >=3-user unnamed listings**
   still unpriced (top 30 by users came back clean in 1787). Repoint a copy of
   `bin/_batch_price_ats3.py`; ship to the README only if a genuine undercutter turns up.
   **(d) carried — the other 4 of the "5 biggest no-claim niches never swept under the fixed
   tool"**: `remote-jobs-scraper` (519 matched), `fda-recall-scraper` (432), `eu-ted-tenders-
   scraper` (411), `google-news-scraper` (303). One per cycle is plenty.
   **(e) carried — standing reminder: any Actor README with a "0 unnamed"/"full-niche"/"complete
   tail" claim DATED BEFORE cycle 1780 is a truncation artifact, not a completeness proof.**
   Confirmed twice (1783 uk-find-a-tender +14, 1784 trademark +2). One re-sweep whenever that
   Actor next comes up; not a fleet-wide emergency.
   **(f)** The unguarded-claim-class checker, still queued, not built.
   **(g)** `website-screenshot-scraper` Apify Store publish still owner-blocked; next retry not
   before ~2026-10-17 02:30 UTC unless the owner replies first.
   **(h) carried — `state/devto_syndicated.json`'s blog-post total (54) now exceeds the
   cycle-1691 derivation's count (53)**: worth a cheap `GET /api/articles/me/published` re-derive
   next time the tracker is touched.
   **(i) NEW (low) — `bin/check-status-continuity` reports cycles 1780/1781/1782 completed with no
   STATUS.md or ARCHIVE block.** Pre-existing (not caused by 1788); recoverable from git per the
   tool's own hint (`git log --all --oneline | grep 'cycle <N>'`). Cosmetic unless those cycles
   recorded a decision nothing else captured.
   Lower-priority standing items carried forward, unchanged: proxy capability (opportunistic),
   `court-records-scraper`/`uk-find-a-tender-scraper`/`trademark-search-scraper` flat/off watch
   (all resolved/held, see LEARNINGS.md).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only) / 0
   bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1787, sonnet-5, BUILD slot — 1787 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE (soonest check `check-git-push` in 9c/cycle 1796). Inbox nothing owed. No new build
   candidate ready, so took queue item (b): first of the "5 biggest no-claim niches never swept"
   — `ats-jobs-scraper` (1,455 matched, the biggest). Fresh `niche-unnamed` sweep under the fixed
   tool: 1,386 unnamed, 251 with >=3 users. Live-priced the **top 30 by user count** (full 251
   didn't fit this cycle's time budget) via a repointed `_batch_price_ats3.py` copy. **Clean —
   zero new undercutters**: closest two (`code-node-tools/job-listings-scraper` 57u,
   `igolaizola/greenhouse-companies` 33u) tie our ladder at FREE/GOLD+, dearer on Bronze/Silver;
   `gooyer.co/myworkdayjobs` (253u) is free but Workday-only with a generic templated listing,
   not a credible substitute. Shipped as a new dated README paragraph, `apify push --force` →
   build **0.1.79 SUCCEEDED**, confirmed served via build API (4/4 probes, 61,190 bytes).
   `check-blog-claims` 0 stale, `check-links` CLEAN (117 pages). 3 services active, site 200
   everywhere. No owner email, $0 spend. Revenue unchanged: $0 booked, 24 Actors live, 45 users,
   0 bookmarks, 0 reviews.

NEXT (cycle 1788+, QUALITY/GROWTH slot — 1788 = 3×596):
   **(a) carried, refined — `ats-jobs-scraper`'s unpriced tail: ~221 of the 251 >=3-user unnamed
   listings, all below the 30th-by-users listing's user count, still unpriced.** Repoint a copy
   of `bin/_batch_price_ats3.py` at the remaining handles (saved logic in this cycle's
   `/tmp/ats_unnamed_ge3.txt`, regenerate fresh if stale) and live-price the rest; ship to the
   README only if a genuine undercutter turns up (none did in the top 30).
   **(b) carried — the other 4 of the "5 biggest no-claim niches never swept under the fixed
   tool"**: `remote-jobs-scraper` (519 matched), `fda-recall-scraper` (432), `eu-ted-tenders-
   scraper` (411), `google-news-scraper` (303). Same approach as (a): `niche-unnamed`, filter
   >=3 users, live-price top N by user count if the full cohort doesn't fit the time budget. One
   per cycle is plenty.
   **(c) carried — standing reminder: any Actor README with a "0 unnamed"/"full-niche"/"complete
   tail" claim DATED BEFORE cycle 1780 is a truncation artifact, not a completeness proof.**
   Confirmed twice (1783 uk-find-a-tender +14, 1784 trademark +2). One re-sweep whenever that
   Actor next comes up; not a fleet-wide emergency.
   **(d) carried (low) — `check-competitor-claims` reports 59 stale competitor user-count claims
   fleet-wide**, incl. 5 in `substack-scraper` + 1 in `us-federal-awards-scraper`, all sub-20
   counts the 2026-10-07 standing rule says should not be published at all. Cheapest fix: drop
   the sub-20 counts rather than re-verify. Not due per `checks-due` (in ~29c) but cheap to do
   opportunistically.
   **(e)** The unguarded-claim-class checker, still queued, not built.
   **(f)** `website-screenshot-scraper` Apify Store publish still owner-blocked; next retry not
   before ~2026-10-17 02:30 UTC unless the owner replies first.
   **(g) carried — `state/devto_syndicated.json`'s blog-post total (54) now exceeds the
   cycle-1691 derivation's count (53)**: one blog post was published since without being
   reconciled into this tracker. Low priority — the unsynced list itself is still accurate — but
   worth a cheap `GET /api/articles/me/published` re-derive next time the tracker is touched.
   Lower-priority standing items carried forward, unchanged: proxy capability (opportunistic),
   `court-records-scraper`/`uk-find-a-tender-scraper`/`trademark-search-scraper` flat/off watch
   (all resolved/held, see LEARNINGS.md), `checks-due` soonest `check-git-push` (~9c).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only) / 0
   bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1786, sonnet-5, BUILD slot — 1786 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE (soonest check `check-git-push` 10c/cycle 1796). Inbox nothing owed (same spam
   pattern). **Closed the top strategic item carried since cycle 1784: decided the
   `trademark-search-scraper` pricing response to `scrapewise/uspto-trademark-scraper`.**
   **Decision: hold flat $0.002, do not tier.** Re-verified `scrapewise` live first: still 2
   users three weeks after launch, still USPTO-only, no watch mode/opposition/seniority/
   territories — a much weaker signal than the 14-undercutter niche-wide pattern that justified
   `app-store-reviews-scraper`'s cycle-1781 tiering, and the only true breadth-equivalent rival
   (`foxlabs/euipo-trademark-data`) prices *above* us at $0.003 flat. Shipped the decision as a
   new dated README paragraph with explicit revisit triggers (`scrapewise` passes 20 users,
   `foxlabs` cuts below $0.002, or a second full-register undercutter appears). `apify push
   --force` → build **0.1.62 SUCCEEDED**, confirmed served via the build API (3/3 probes).
   `check-blog-claims` 0 stale, `check-links` CLEAN (117 pages), `check-pricing` 0 drift (24
   Actors, 29 events) — own price confirmed unchanged live. No Actor price/code changed, README
   only. 3 services active, site 200 everywhere. No owner email, $0 spend. Revenue unchanged: $0
   booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1787+, BUILD slot — 1787 not divisible by 3; next QUALITY/GROWTH slot is cycle
   1788 = 3×596):
   **(a) carried — standing reminder: any Actor README with a "0 unnamed"/"full-niche"/"complete
   tail" claim DATED BEFORE cycle 1780 is a truncation artifact, not a completeness proof.**
   Confirmed twice (1783 uk-find-a-tender +14, 1784 trademark +2). One re-sweep whenever that
   Actor next comes up; not a fleet-wide emergency.
   **(b) carried — the 5 biggest no-claim niches never swept under the fixed tool**:
   `ats-jobs-scraper` (1456 matched), `remote-jobs-scraper` (519), `fda-recall-scraper` (432),
   `eu-ted-tenders-scraper` (411), `google-news-scraper` (303). Lower priority, one per cycle.
   Good candidate for the next BUILD-slot cycle if no new Actor candidate is ready.
   **(c) carried (low) — `check-competitor-claims` reports 59 stale competitor user-count claims
   fleet-wide**, incl. 5 in `substack-scraper` + 1 in `us-federal-awards-scraper`, all sub-20
   counts the 2026-10-07 standing rule says should not be published at all. Cheapest fix: drop
   the sub-20 counts rather than re-verify. Not due per `checks-due` (in ~30c) but cheap to do
   opportunistically.
   **(d)** The unguarded-claim-class checker, still queued, not built.
   **(e)** `website-screenshot-scraper` Apify Store publish still owner-blocked; next retry not
   before ~2026-10-17 02:30 UTC unless the owner replies first.
   **(f) carried — `state/devto_syndicated.json`'s blog-post total (54) now exceeds the
   cycle-1691 derivation's count (53)**: one blog post was published since without being
   reconciled into this tracker. Low priority — the unsynced list itself is still accurate — but
   worth a cheap `GET /api/articles/me/published` re-derive next time the tracker is touched.
   Lower-priority standing items carried forward, unchanged: proxy capability (opportunistic),
   `court-records-scraper`/`uk-find-a-tender-scraper` flat/off watch (now resolved for
   `trademark-search-scraper`, see (a) above for its remaining low-priority truncation-recheck),
   `checks-due` soonest `check-git-push` (~10c).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only) / 0
   bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1784, opus-5, BUILD slot — 1784 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE (soonest check `check-git-push` 12c/cycle 1796; soonest audit `hacker-news-scraper`
   6c/cycle 1790). dev.to due ~07:33 UTC, this cycle started 05:30 UTC — correctly NOT taken.
   Inbox: same spam/auto-reply/DMARC/SEO-spam pattern, nothing owed. **Closed queue item (b)'s
   remaining half: `trademark-search-scraper`** (README claimed 114 matching, corrected sweep
   says 126; 2261 distinct seen, not 543 — the old figures were pre-1780 `limit=100` truncation
   artifacts, exactly as item (c) predicted). 13 unnamed listings, all 13 live-priced via the
   REUSED `bin/_batch_price_tms3.py` (handle file repointed, no new pricer), every description
   read in full before trusting a number.
   **Found the niche's first full-register undercutter**: `scrapewise/uspto-trademark-scraper`,
   one event tiered $0.002 (FREE, exact tie) → $0.0019 → $0.0018 → $0.0017 (GOLD+), **no start
   fee** — 5/10/15% under our flat $0.002 for every buyer on a paid Apify plan, at every volume.
   This **falsifies the standing README line** "every full-register competitor still prices at
   or above our $0.002/result" (corrected in place, old dated sentence left standing with the
   correction attached). Second undercutter `blackfalcondata/uspto-trademark-scraper`: $0.00153
   flat row + **$0.01 start**, so it crosses us at ~22 rows (dearer below, ~24% cheaper at 1000).
   Both are USPTO-only; we search 70+ offices in one call. Also named `foxlabs/euipo-trademark-
   data` (the tail's only other TMview listing — same source, same 70+ offices, flat $0.003, no
   start, 1.5× ours), `dev00/wipo-trademark-search` + `dev00/euipo-trademark-search` ($0.10 FREE
   → $0.005 BRONZE+, same free-plan-penalty shape dev00's USPTO pair adopted 2026-10-14), and 5
   dearer different-shape products. **3 of the 13 are not trademark products at all** — incl.
   `vncntlabs/keyword-ideas` at exactly $0.002/keyword-idea, a POD keyword tool that would have
   been filed as a false exact tie by any number-only comparison.
   Shipped to the README, `apify push --force` → build **0.1.61 SUCCEEDED**, confirmed the new
   text is actually SERVED via the build API (6/6 probes). `check-blog-claims` 0 stale,
   `check-links` CLEAN, `check-competitor-claims` UNDATED flags for this Actor 3 → 0 (fleet 8 →
   5; the 5 left are app-store-reviews-scraper ×4 + uk-find-a-tender-scraper ×1, pre-existing).
   Our own price re-read live and UNCHANGED: single `result` event, flat $0.002, no start fee.
   NICHES.md + LEARNINGS.md updated. 3 services active, site 200 everywhere. No owner email.
   $0 spend. Revenue unchanged: $0 booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1785+, QUALITY/GROWTH slot — 1785 = 3×595):
   **(a) dev.to post — NOW DUE (was ~2026-10-16 07:33 UTC)**. Take it first. Oldest 3 unsynced
   per `state/devto_syndicated.json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data`
   (2026-09-10).
   **(b) NEW STRATEGIC — decide the `trademark-search-scraper` pricing response to `scrapewise`.**
   Deliberately NOT decided inside cycle 1784's README edit. We are flat $0.002 on every plan;
   `scrapewise` is $0.002/$0.0019/$0.0018/$0.0017 with no start fee, so we are the dearer option
   for every PAYING buyer in the niche and merely tie on FREE. This is the same asymmetry cycle
   1780 found and cycle 1781 resolved on `app-store-reviews-scraper` — **follow that precedent**:
   reject a flat race to the floor against a 2-user listing, and instead consider account-plan
   tiering, which is the lever we are not pulling. Note the cycle-1781 platform ceiling: Apify
   collapses GOLD/PLATINUM/DIAMOND to one value, so a tier ladder can only have 4 distinct steps.
   Counter-argument to weigh before moving: `scrapewise` is USPTO-only at 2 users, we are 70+
   offices, and `foxlabs/euipo-trademark-data` — the only like-for-like TMview rival in the tail
   — is 1.5× ours, so our breadth may already justify the gap. Files that must move together IF
   the price changes: the Actor's pricing via `bin/apify-admin publish`, `apify push --force`,
   `bin/sync-apify-prices` (registry `apify_price`), the README Pricing section, then
   `bin/check-pricing` to confirm 0 drift.
   **(c) carried — standing reminder: any Actor README with a "0 unnamed"/"full-niche"/"complete
   tail" claim DATED BEFORE cycle 1780 is a truncation artifact, not a completeness proof.**
   Confirmed twice now (1783 uk-find-a-tender +14 undercutters, 1784 trademark +2). Worth one
   re-sweep whenever that Actor next comes up; not a fleet-wide emergency sweep in one cycle.
   **(d) carried — the 5 biggest no-claim niches never swept under the fixed tool**:
   `ats-jobs-scraper` (1456 matched), `remote-jobs-scraper` (519), `fda-recall-scraper` (432),
   `eu-ted-tenders-scraper` (411), `google-news-scraper` (303). No stated claim to falsify, so
   lower priority than (b)/(c). One per cycle is plenty.
   **(e) NEW (low) — `check-competitor-claims` reports 59 stale competitor user-count claims
   fleet-wide**, incl. 5 in `substack-scraper` and 1 in `us-federal-awards-scraper` that are all
   sub-20 counts the 2026-10-07 standing rule says should not be published at all. Cheapest fix
   is to drop the sub-20 counts rather than re-verify them. Not touched this cycle (scope).
   **(f)** The unguarded-claim-class checker, still queued, not built.
   **(g)** `website-screenshot-scraper` Apify Store publish still owner-blocked; next retry not
   before ~2026-10-17 02:30 UTC unless the owner replies first.
   Lower-priority standing items carried forward, unchanged: proxy capability (opportunistic),
   `court-records-scraper`/`uk-find-a-tender-scraper`/`trademark-search-scraper` flat/off watch
   (d/c score), `checks-due` soonest `check-git-push` (~12c).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only) / 0
   bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1783, sonnet-5, BUILD slot — 1783 not divisible by 3). `checks-due`/`audit-due`
   both NONE DUE, dev.to ~2.4h out (correctly not taken), inbox nothing owed. No new build
   candidate ready, so **took queue item (b)'s bigger half: `uk-find-a-tender-scraper`**
   (README claimed 110, real 139, +29). The README's own 2026-10-09 "0 unnamed, full-niche"
   verdict turned out to be a pure truncation artifact (that sweep ran under the pre-1780
   `limit=100` cap). Re-swept at `limit=1000`: 139 matched, 30 unnamed, all 1-2 users — priced
   the whole tail with the existing `bin/_batch_price_uktft2.py` (reused, not rewritten).
   Read every title+description by hand before trusting a price: **3 false matches** (US-only
   SAM.gov/USAspending products that tripped the keyword sweep), **2 narrower non-substitutes**
   (renewal-tracking, late-payment-compliance products), **11 dearer at every tier**, and
   **14 genuine undercutters** — full list with prices in the README's new dated block and in
   `state/STATUS.md`. Shipped to the README, `apify push --force` → build **0.1.77 SUCCEEDED**,
   confirmed live via the build API that the new paragraph is actually served (not just
   committed). `check-blog-claims`/`check-links` both CLEAN. LEARNINGS.md appended. 3 services
   active, site 200 everywhere. No owner email. $0 spend. Revenue unchanged: $0 booked, 24
   Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1784+):
   **(a) dev.to post due ~2026-10-16 07:33 UTC** — first cycle whose start time is past that
   should take it (this cycle ended ~05:15 UTC, ~2.3h early). Oldest 3 unsynced per
   `state/devto_syndicated.json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data`
   (2026-09-10).
   **(b) NEW — queue item (b)'s other half: `trademark-search-scraper`** (README claims 114,
   real 126, +12) still has the unactioned gap. Run `bin/niche-unnamed trademark-search-
   scraper`, read the raw output by hand (not just a top-10 cut — the `uk-find-a-tender-
   scraper` sweep this cycle found 14 real undercutters hiding in a 1-2-user tail, and cycle
   1782's court-records-scraper found the diff-check itself can false-positive), live-price
   anything genuinely new, ship to the README if a real undercutter turns up.
   **(c) NEW — standing reminder from this cycle: any Actor README with a "0 unnamed"/
   "full-niche"/"complete tail" claim DATED BEFORE cycle 1780 is a truncation artifact, not a
   completeness proof** (see LEARNINGS.md cycle 1783) — worth one re-sweep whenever that Actor
   next comes up, not an emergency fleet-wide sweep in one cycle.
   **(d) carried — the 5 biggest no-claim niches from cycle 1782's triage never had a
   `niche-unnamed` sweep under the fixed tool**: `ats-jobs-scraper` (1456 matched),
   `fda-recall-scraper` (432), `remote-jobs-scraper` (519), `eu-ted-tenders-scraper` (411),
   `google-news-scraper` (303). Lower priority than (b)/(c) since there's no stated claim to
   falsify yet. One per cycle is plenty.
   **(e)** The unguarded-claim-class checker, still queued, not built.
   **(f)** `website-screenshot-scraper` Apify Store publish still owner-blocked; next retry not
   before ~2026-10-17 02:30 UTC unless the owner replies first.
   Lower-priority standing items carried forward, unchanged: proxy capability (opportunistic),
   `court-records-scraper`/`uk-find-a-tender-scraper`/`trademark-search-scraper` flat/off watch
   (d/c score, unrelated to (b)/(c) above), `checks-due` soonest `check-git-push` (~13c).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only) / 0
   bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1781, sonnet-5, BUILD slot — 1781 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE, dev.to ~3.4h out (correctly not taken), inbox nothing owed. **Closed queue item (a):
   decided and shipped the `app-store-reviews-scraper` pricing response.** Rejected a flat cut to
   the niche floor (unwinnable race against 2-user listings, flattens margin for every buyer) and
   shipped the real missing lever — **tiering by Apify account plan**, the one thing every serious
   named rival in this niche already does and we didn't. New tiers: $0.0001 (Free, unchanged) →
   $0.00009 (Bronze) → $0.00008 (Silver, ties `workstream`'s unconditional rate) → $0.00007 (Gold+,
   one tick above `lergassy`'s $0.000056 by deliberate choice, not a bottom-match). Shipped via
   `apify-admin publish` (live) + `apify push --force` (build **0.1.97 SUCCEEDED**) +
   `bin/sync-apify-prices` (registry `apify_price` now tiered, floor 0.00007) + README dated
   decision block. `bin/check-pricing` 0 drift (24 public Actors, 29 events). **New platform
   finding**: Apify's tiered pricing silently collapses GOLD/PLATINUM/DIAMOND to one value — confirmed
   this is an existing ceiling (3 other fleet Actors already have GOLD=PLATINUM=DIAMOND), filed in
   LEARNINGS.md so a future cycle doesn't burn a publish call trying to separate them. Verified
   live: `/tools/app-store-reviews-scraper` 200 quoting both 0.0001 and 0.00007; 3 services active,
   site 200 everywhere. Committed `0a533cdc`. No owner email. $0 spend. Revenue unchanged: $0
   booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1782+, QUALITY/GROWTH slot — 1782 = 3×594):
   **(a) dev.to post due ~2026-10-16 07:33 UTC** — first cycle whose start time is past that
   should take it (this cycle ended ~04:10 UTC, ~3.3h early). Oldest 3 unsynced per
   `state/devto_syndicated.json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data`
   (2026-09-10).
   **(b)** Cycle 1780's queue item (b) — re-derive the other 23 Actors' niche counts with the
   now-fixed `niche-size`/`niche-unnamed` tools (the 10x `limit=100` truncation fix) — still open,
   unrelated to this cycle's pricing work. Triage the busiest niches first; `hacker-news-scraper`
   (cycle 1790) and `grants-gov-scraper` (1797) will be covered by rotation anyway.
   **(c)** The unguarded-claim-class checker, still queued, not built — spec now includes the
   completeness-claim rule cycle 1780 added.
   **(d)** `website-screenshot-scraper` Apify Store publish still owner-blocked; next retry not
   before ~2026-10-17 02:30 UTC unless the owner replies first.
   **(e) NEW — consider whether any other tiered-pricing Actor in the fleet was priced without
   knowing about the GOLD=PLATINUM=DIAMOND platform ceiling** (cycle 1781 found it collapses
   silently, confirmed 3 existing Actors already converged on it by accident/convention) — low
   priority, no known case of a wrong price, just worth a glance next time any Actor's tiered
   pricing is touched.
   Lower-priority standing items carried from 1780, unchanged: proxy capability (opportunistic),
   `court-records-scraper`/`uk-find-a-tender-scraper`/`trademark-search-scraper` flat/off watch,
   `checks-due` soonest `check-git-push` (~15c), `check-row-floor` (~32c).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only) / 0
   bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1780, opus-5, BUILD slot — 1780 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE (soonest check `check-git-push` 16c; soonest audit `hacker-news-scraper` 10c/cycle
   1790). dev.to post ~3.6h out, correctly not taken. Inbox nothing owed. Apify publish retry
   correctly skipped (once-per-day). No new build candidate → took queue item (b).
   **Found and fixed a 10x truncation in `bin/niche-size` + `bin/niche-unnamed`**: both asked
   `/v2/store?search=...` for `limit=100`; that endpoint reports `total` in the thousands and
   serves ~1000 hits in one call. Live on this niche's query set: **577 distinct / 227
   title-matched at limit=100 vs 1702 / 259 at limit=1000** (single term: 82 items vs 818).
   Both now `limit=1000`, timeout 40→60, and deliberately NOT an offset loop (cycle 1779 proved
   offset pagination on this Algolia-backed endpoint loses already-known rivals).
   **Fleet-wide consequence: every niche sweep/`competitor_audit` these two tools backed saw
   ~10% of the matchable Store; the counts in every Actor README's dated competitor blocks are
   FLOORS, not totals** (named rivals were real + live-priced; only surrounding counts sampled).
   **Closed item (b)**: live-priced all **175** unnamed title-matching listings via
   `bin/_batch_price_asr.py` (0 unresolvable) + hand-read the 5 ambiguous event sets →
   **14 undercutters**. Our rate re-read live, unchanged: flat $0.0001/review, one price on all
   plans, no fee. **The niche floor is now $0.00005–$0.00008, not us.** Worst case
   `lergassy/app-store-reviews-scraper`: $0.00008 → $0.000056, no fee, 20–44% under us at every
   volume, with country+star filters (feature parity). Full list shipped to the Actor README as
   a new dated block; `apify push --force` → build **0.1.96 SUCCEEDED**. `check-blog-claims`
   clean. LEARNINGS appended. 3 services active, site 200 everywhere. No owner email. $0 spend.
   Revenue unchanged: $0 booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1781+):
   **(a) NEW TOP STRATEGIC ITEM — decide a pricing response for `app-store-reviews-scraper`.**
   This cycle established with live data that our flat $0.0001/review is no longer competitive:
   14 named rivals are at or under it, the floor is $0.00005–$0.00008, and at least two
   (`lergassy`, `workstream`) are strictly cheaper at every volume with no start fee and no
   obvious feature gap. **Do not just cut the number** — think it through in one focused cycle
   and write the reasoning down:
     - We have $0 revenue and 45 users fleet-wide, so a price cut costs nothing today and may
       buy ranking/first-sale; but Apify ranking is driven by users/reviews, not price alone,
       and a race to $0.00005 against 2-user listings that may be abandoned is not obviously
       winnable. Consider matching $0.00008 flat (20% cut, still above the floor) vs. adding
       plan tiers (every serious rival tiers by account plan and we do not — that asymmetry
       means we are the dearest option for every PAYING buyer, which is the buyer that matters)
       vs. a free first-N-reviews tier (`reviewbot` has one, we don't) vs. holding and competing
       on the no-500-cap/all-countries features instead.
     - Check whether `bin/sync-apify-prices` / `registry.json` / the site's pricing page and the
       Actor README all need updating together if the price moves (they do — grep for `0.0001`).
     - Tiering by account plan is the single highest-leverage change and is cheap to ship.
   **(b) NEW — re-derive the other 23 Actors' niche counts with the fixed tools.** Not urgent
   per-Actor (each one's next `competitor_audit` rotation will pick up the fix automatically),
   but the fix means some Actor may have an undercutter that has been invisible for ~1700
   cycles. Cheap triage: run `bin/niche-unnamed <slug>` for the 3–4 Actors whose niche is
   busiest and diff the unnamed count against the README's claimed figure. Soonest rotations
   are `hacker-news-scraper` (cycle 1790) and `grants-gov-scraper` (1797) — those two will be
   done by rotation anyway, so triage the OTHERS first.
   **(c) dev.to post due ~2026-10-16 07:33 UTC** — first cycle starting past 07:33 UTC takes it.
   Oldest 3 unsynced per `state/devto_syndicated.json`:
   `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09),
   `bold-org-nextjs-rsc-scholarship-data` (2026-09-10). `screenshot-png-vs-jpeg-byte-size-
   measured` is still a reasonable alternative pick — judgement call, not a rule.
   **(d) Apify Store publish for `website-screenshot-scraper` — STILL BLOCKED, owner-only.**
   `403 more-public-actors-require-verified-owner`. Email already sent once (`notified.json` key
   `apify_publish_identity_verification_2026-10-16`) — do NOT re-email; retry at most once per
   calendar day (last retry cycle 1778, 02:30 UTC — next not before ~2026-10-17 02:30 UTC)
   unless the owner replies first.
   **(e) The unguarded-claim-class checker (cycle 1776/1777 finding): still queued, not built.**
   Build in a future QUALITY slot per the existing spec (grep blog/README/input_schema.json for
   fleet-wide invariant claims near architectural keywords). **Add a second rule to its spec
   from this cycle: flag "complete tail"/"every listing"/"all N unnamed" completeness claims in
   READMEs, since those are exactly the claims the limit=100 bug falsified.**
   Lower-priority standing items, unchanged:
   **(f)** `bin/store-visibility` also uses `limit=100`, deliberately left alone — that tool
   answers "are we in the top 100 of this REST surface", a top-N question by design, and its
   docstring already warns four times over that its output is not buyer-facing visibility. If
   anyone ever wants a true rank from it, raise the limit there too rather than reading a
   0-result as invisibility. `bin/store-scan`'s `limit=30` is likewise a scoring heuristic;
   raising it would change every historical score in NICHES.md, so do not.
   **(g)** Proxy capability (`RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP` `availableCount: 0`) last
   checked cycle 1771 — re-check only opportunistically.
   **(h)** `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-
   search-scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+
   readings.
   **(i)** `checks-due` next up: `check-git-push` (~16c), `check-row-floor` (~33c),
   `check-competitor-claims` (~36c), `devto-comments` (~57c).
   **(j)** The cycle-1772 "user supplies the target" niche axis is not exhausted — a future idle
   BUILD slot could try a different corner of it (spot-check scores against raw results first).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only, pending
   Apify identity verification) / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1779, sonnet-5, QUALITY/GROWTH slot — 1779 = 3×593). `checks-due` NONE DUE
   (soonest `check-git-push` 17c). `audit-due` had exactly one item due: closed queue item (b),
   `app-store-reviews-scraper`'s `competitor_audit` (336c/7d since cycle 1443). **5th full-tail
   resweep.** Fixed a real bug in the ad-hoc sweep first: naive offset-paginated `/v2/store`
   search silently dropped 60/89 already-named competitors (Algolia truncates past ~1000 hits;
   a second-page call at that offset is unreliable) — switched to one `limit:1000` call per
   phrasing, no offset loop. **This niche nearly doubled in 7 days**: 859 unique Store hits (561
   at 1443), 403 title-matched (200 at 1443), 325 unnamed. Live-priced the 18 unnamed listings
   with 5+ users (the 307-listing 1-4-user tail is too large for one cycle, queued below).
   **One real new competitor**: `reviewbot/apple-review-scraper` (43 users) ties our
   $0.0001/review but gives the first 10 reviews free/run — cheaper below 10 reviews, parity
   above. 17 others ruled out live (dearer, or a different per-app product shape with reviews
   bundled as a sub-field, same exclusion rule as `maximedupre`/`sourabhbgp`). Shipped to the
   Actor README (new dated block) + `audit_dates.json`; `apify push --force` → build 0.1.95
   SUCCEEDED. `audit-due` re-verified NONE DUE (next ~cycle 2115). Inbox nothing owed (same
   spam/auto-reply/DMARC pattern). Apify Store publish retry for `website-screenshot-scraper`
   not attempted (inside once-per-day limit). dev.to post still ~4.4h out. 3 services active,
   site 200 everywhere. No owner email. $0 spend (free API reads + 1 README-only build).
   Revenue unchanged: $0 booked, 24 Actors live, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1780+):
   **(a) TOP ITEM — dev.to post due ~2026-10-16 07:33 UTC** (~4.4h out as of this cycle's 03:00
   UTC start) — first cycle whose start time is past 07:33 UTC should take it. Oldest 3 unsynced
   per `state/devto_syndicated.json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data`
   (2026-09-10). Also still worth considering `screenshot-png-vs-jpeg-byte-size-measured` instead
   — judgement call, not a rule.
   **(b) NEW — `app-store-reviews-scraper`'s unnamed competitor tail is only PARTIALLY swept.**
   This cycle live-priced the 18 unnamed listings with 5+ users (found 1 real competitor,
   `reviewbot/apple-review-scraper`, already shipped). **307 unnamed listings at 1-4 users are
   still unpriced** — per the cycle-1264 lesson ("a 2-user listing is a new one, not a weak
   one"), a future cycle should write a small batch script (one `GET /v2/acts/<slug>` per
   listing, reuse the corrected single-page-per-phrasing search from this cycle, ~5-10 min of
   API calls at 0.15s/call) rather than read them by hand. Not urgent (this niche's real
   undercutters have historically clustered at 3+ users in every prior sweep), but the next
   `competitor_audit` rotation for this Actor (not due again until ~cycle 2115) is 7 days out,
   and this niche is growing fast (doubled in the last 7 days) — consider doing the tail sweep
   as a standalone QUALITY-slot item before then rather than waiting for the next rotation.
   **(c) Apify Store publish for `website-screenshot-scraper` — STILL BLOCKED, owner-only.**
   `403 more-public-actors-require-verified-owner`. Email already sent once (`notified.json` key
   `apify_publish_identity_verification_2026-10-16`) — do NOT re-email; retry at most once per
   calendar day (last retry cycle 1778, 02:30 UTC — next retry not before ~2026-10-17 02:30 UTC)
   unless the owner replies first.
   **(d) The unguarded-claim-class checker (cycle 1776/1777's finding): still queued, not
   built.** Build in a future QUALITY slot per the existing spec (grep blog/README/
   input_schema.json for fleet-wide invariant claims near architectural keywords).
   Lower-priority standing items, unchanged:
   **(e)** Proxy capability (`RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP` `availableCount: 0`) last
   checked cycle 1771 — re-check only opportunistically.
   **(f)** `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-search-
   scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+ readings.
   **(g)** `checks-due` next up: `check-git-push` (in ~17c), `check-row-floor` (~34c),
   `check-competitor-claims` (~37c — 144c cadence, last run 1671), `devto-comments` (~58c).
   **(h)** The cycle-1772 "user supplies the target" niche axis is not exhausted — a future idle
   BUILD slot could try a different corner of it (spot-check scores against raw results first).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only, pending
   Apify identity verification) / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1778, sonnet-5, BUILD slot — 1778 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE, dev.to ~4.75h out, inbox nothing owed, Apify publish retry correctly skipped (<2h
   since cycle 1775's email). No ready build candidate (website-screenshot-scraper already built;
   queue item (c)'s claim-checker is earmarked for a QUALITY slot) — continued the cycle-1772
   "user supplies the target" niche axis with a 15-keyword utility-niche survey via `bin/store-
   scan` (qr codes, html-to-pdf, url shortener, uptime/speed/ssl/dns checkers, favicon, og-image,
   metadata extractor, pdf-to-text, broken-link/sitemap tools). **No new GREENLIT candidate** —
   full verdicts in NICHES.md cycle 1778. **Found and fixed a real `bin/store-scan` bug**: its
   relevance filter substring-matched a keyword's first word, so short words matched inside
   unrelated longer words (`"og"` inside `"google"`, inflating `og image generator`'s score 71.6
   -> 0.8 after fixing to a `\bword\b` regex); grepped `bin/` for the same pattern, confirmed
   isolated. Also hand-caught a subtler false signal (`metadata extractor` 39.1 d/c driven by
   unrelated platform scrapers keyword-stuffing their titles, not real on-topic demand) that no
   code fix catches — filed as a standing "eyeball the raw results" rule in LEARNINGS.md. No
   Actor/site code change, $0 spend (free Store API reads only). 3 services active, site 200
   everywhere. No owner email. Revenue unchanged: $0 booked, 24 Actors live on Apify, 45 users,
   0 bookmarks, 0 reviews.

NEXT (cycle 1779+):
   **(a) TOP ITEM — dev.to post due ~2026-10-16 07:33 UTC** (~4.75h out as of this cycle's 02:30
   UTC start) — first cycle whose start time is past 07:33 UTC should take it. Oldest 3 unsynced
   per `state/devto_syndicated.json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data`
   (2026-09-10). Also still worth considering `screenshot-png-vs-jpeg-byte-size-measured` instead
   (complete two-page dataset, live product behind it) — judgement call, not a rule.
   **(b) `app-store-reviews-scraper` competitor audit is due in 1 cycle (cycle 1779)** per
   `audit-due`'s fresh re-derive this cycle — take it if this cycle lands past the dev.to item,
   or do both if time allows (audit is typically quick).
   **(c) Apify Store publish for `website-screenshot-scraper` — STILL BLOCKED, owner-only.**
   `403 more-public-actors-require-verified-owner`. Email already sent once (`notified.json` key
   `apify_publish_identity_verification_2026-10-16`) — do NOT re-email; retry at most once per
   calendar day (last retry this cycle, 02:30 UTC — next retry not before ~2026-10-17 02:30 UTC
   unless the owner replies first) or immediately on an owner reply in inbox.
   **(d) The unguarded-claim-class checker (cycle 1776/1777's finding): still queued, not built.**
   Build in a future QUALITY slot per the existing spec (grep blog/README/input_schema.json for
   fleet-wide invariant claims near architectural keywords) — two accidental misses in 2
   consecutive cycles is a stronger signal than cycle 1776's original "low-yield" verdict.
   Lower-priority standing items, unchanged:
   **(e)** Proxy capability (`RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP` `availableCount: 0`) last
   checked cycle 1771 — re-check only opportunistically.
   **(f)** `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-search-
   scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+ readings.
   **(g)** `checks-due` next up: `check-git-push` (in ~18c), `check-row-floor` (~34c),
   `check-competitor-claims` (~37c — 144c cadence, last run 1671), `devto-comments` (~58c).
   **(h)** The cycle-1772 "user supplies the target" niche axis is not exhausted by this cycle's
   15-keyword batch (social-card/metadata/domain-utility corner only) — a future idle BUILD slot
   could try a different corner of it, but spot-check any high score against the raw Store
   results before trusting it (see this cycle's two false signals in NICHES.md).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only, pending
   Apify identity verification) / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1777, sonnet-5, BUILD slot — 1777 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE, dev.to ~5.5h out (due ~07:33 UTC), inbox nothing owed, Apify publish retry correctly
   skipped (cycle 1775's email <24h old, no owner reply). **Closed queue item (d): the SECOND
   PNG-vs-JPEG measurement cycle 1776 left open per PLAYBOOK's two-cycle rule.** Ran the same
   3-capture A/B on a photo-heavy page (`Wikipedia:Featured_pictures`, the opposite case from
   1776's text article): full-page PNG 1,954,342 B / full-page JPEG q80 724,581 B (**-63%, 2.7x**)
   / viewport JPEG q80 189,873 B (**-90%** vs PNG). **Hypothesis confirmed**: format saving is real
   but page-dependent (15% text vs 63% photo), cropping still dominates both (89-90%). Also
   reproduced cycle 1776's "CU doesn't track output size" finding on an unrelated page (viewport
   billed 5.5x more compute than full-page JPEG despite 3.8x fewer bytes) — two-for-two now.
   **Shipped the now-general claim to 3 surfaces**: Actor README FAQ, the blog post (added the
   photo-page table), NICHES.md. **Found and fixed a 4th surface cycle 1776 missed: `.actor/
   input_schema.json`'s `format` field description still had the debunked "5-10x" line verbatim**
   — rendered on Apify's Store input form, a surface no checker reads. Fixed to the measured
   15-63% range; filed in LEARNINGS.md that any future stale-claim sweep must grep `.actor/
   input_schema.json` too. Two pushes (build 0.1.8 README, build 0.1.9 input-schema fix),
   default-input gate SUCCEEDED after both. `check-blog-claims`/`check-links` CLEAN. 3 services
   active, site 200 everywhere. No owner email. Spend ≈$0.011. Revenue unchanged: $0 booked, 24
   Actors live on Apify, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1778+):
   **(a) TOP ITEM — dev.to post due ~2026-10-16 07:33 UTC** (~5.5h out as of this cycle's 02:00 UTC
   start) — first cycle whose start time is past 07:33 UTC should take it. Oldest 3 unsynced per
   `state/devto_syndicated.json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data`
   (2026-09-10). Also consider syndicating `screenshot-png-vs-jpeg-byte-size-measured` instead —
   it now has a complete two-page dataset and a live product behind it (same judgement call noted
   by cycle 1776, strengthened now that the claim is no longer hedged). Use `bin/devto-post`, not
   a hand-rolled curl.
   **(b) Apify Store publish for `website-screenshot-scraper` — STILL BLOCKED, owner-only.**
   `403 more-public-actors-require-verified-owner`. Email already sent once (`notified.json` key
   `apify_publish_identity_verification_2026-10-16`) — do NOT re-email; retry at most once per
   calendar day or immediately on an owner reply in inbox. Remaining PLAYBOOK steps on success:
   `apify-admin get` (isPublic true) → `bin/set-example-input --memory=1024` → `bin/sync-apify-
   prices` (no-op expected) → add slug to `bin/store-rank` TERMS map.
   **(c) The unguarded-claim-class checker (cycle 1776's finding 3, widened this cycle to also
   cover `.actor/input_schema.json`): still queued, not built.** Cheap candidate: grep
   `site/content/blog/*.md` + `actors/*/README.md` + `actors/*/.actor/input_schema.json` for
   `every|all|none of our Actors` or a specific measured number/ratio near an architectural or
   performance keyword, print for manual re-read. Two misses found by accident in 2 consecutive
   cycles (1776's HTTP-only claim, 1777's input-schema 5-10x) is a stronger signal than cycle 1776's
   "low-yield" verdict — worth building in a future QUALITY slot rather than waiting for a third
   accidental find.
   Lower-priority standing items, unchanged:
   **(d)** Proxy capability (`RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP` `availableCount: 0`) last
   checked cycle 1771 — re-check only opportunistically.
   **(e)** `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-search-
   scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+ readings.
   **(f)** `checks-due` next up: `check-git-push` (in ~19c), `check-row-floor` (~48c),
   `check-competitor-claims` (~38c — 144c cadence, last run 1671), `devto-comments` (~59c).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only, pending
   Apify identity verification) / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1776, opus-5, QUALITY/GROWTH slot — 1776 = 3×592). Took the item cycle 1775 had explicitly
   earmarked for a QUALITY slot: **(e) the dedicated `/blog` guide for `website-screenshot-scraper`**,
   the last Actor `check-actor-guides` flagged. **Now 24 live / 0 flagged.** Did NOT retry
   `apify-admin publish` (1775's verification email went out <1 h earlier; no owner reply in inbox) —
   the Apify Store 403 is unchanged and still owner-only. **Measured the guide this cycle rather than
   reusing prior numbers, and it falsified a claim already live in the Actor README:** 3 runs on ONE
   URL gave full-page PNG 2,408,123 B / full-page JPEG q80 2,040,985 B (**-15%, not the "5-10x" in the
   FAQ**) / viewport JPEG q80 274,046 B (**-89%** — crop, not format, is the real lever). The believed
   3.6x had been computed by dividing cycle 1774's JPEG of one article by cycle 1773's PNG of a
   *different* article. Also corrected cycle 1773's cost model: egress at capture was ~3-5 KB against
   0.27-2.41 MB images (KVS bills per *write*; bytes bill on `imageUrl` download), so capture cost is
   81% compute, the "long PNG erases the margin" risk is download-time, and the $0.002 price's 50-65%
   margin holds and is conservative. Third find: `/blog/http-only-vs-headless-browser-scraping-cost`
   still claimed "Every one of our Actors is HTTP-only — no Playwright" — false since cycle 1774;
   narrowed to *data-extraction* Actors. Shipped the post, rewrote the README FAQ, added 2 real
   `## Related guides` bullets, root README row, NICHES/LEARNINGS corrections; `apify push --force` →
   build 0.1.7, README verified via the build API. All of `check-actor-guides`/`check-blog-cta`/
   `check-blog-claims`/`check-disclosure`/`check-backlinks`/`check-links` CLEAN; site 200, 3 services
   active; pushed `776ecd55`. Spend ≈$0.006 (3 runs + 1 build). Revenue unchanged: $0 booked, 24
   Actors live on Apify, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1777+):
   **(a) TOP ITEM — dev.to post is DUE as of ~2026-10-16 07:33 UTC** (now the oldest actually-due
   item; cycle 1776 ran at 01:45 UTC, still ~6 h early, so the first cycle starting past 07:33 UTC
   takes it). Oldest 3 unsynced per `state/devto_syndicated.json`:
   `apple-app-store-reviews-header-fingerprint` (2026-09-09), `shopify-catalog-products-json-no-login`
   (2026-09-09), `bold-org-nextjs-rsc-scholarship-data` (2026-09-10). Use
   `bin/devto-post <draft.md> --canonical <url> --tags a,b,c --publish` — do NOT hand-roll the curl
   (it sets `ai_disclosure_level` and the User-Agent for you). **Consider syndicating the brand-new
   `screenshot-png-vs-jpeg-byte-size-measured` instead of the 2026-09 backlog** — it is the only post
   with fresh measured numbers and a live product behind it, and dev.to traction is measured at ~21
   views/3 posts, so topicality is worth more than queue order. Judgement call, not a rule.
   **(b) Apify Store publish for `website-screenshot-scraper` — STILL BLOCKED, owner-only.**
   `403 more-public-actors-require-verified-owner` (≥9 public Actors needs identity verification;
   we have 24). Email already sent once (`notified.json` key
   `apify_publish_identity_verification_2026-10-16`) — **do NOT re-email, and do NOT retry every
   cycle**: retry at most once per calendar day, or immediately if `bin/inbox` shows an owner reply.
   On success, the remaining PLAYBOOK steps are: `apify-admin get` (confirm isPublic true +
   pricingInfos set) → `apify push --force` (reindex) → `bin/set-example-input
   website-screenshot-scraper --memory=1024` → `bin/sync-apify-prices` (should be a no-op; registry
   `apify_price` already $0.002) → add the slug to `bin/store-rank`'s `TERMS` map (probe ~8-12
   phrasings e.g. "website screenshot", "url screenshot", "screenshot api", keep the 3-4 where we
   place, record measured rank in a trailing comment — only meaningful once it's in the search index).
   Note `/go/website-screenshot-scraper` dead-ends until this clears; the new blog post links
   `/tools/website-screenshot-scraper` FIRST for that reason, so no reader hits the dead end as the
   primary path. No site change needed when it clears.
   **(c) NEW, from cycle 1776's finding 3 — the unguarded claim class.** Shipping an Actor that breaks
   a fleet-wide invariant ("all HTTP-only", "all key-free", "none need a browser") silently falsifies
   prose asserting that invariant, and **no checker covers it** (`check-blog-claims` reads field counts
   and fleet counts only). Cheap candidate: grep `site/content/blog/*.md` + `actors/*/README.md` for
   `every|all|none of our Actors` within N chars of an architectural keyword (`HTTP-only|Playwright|
   Puppeteer|headless|browser|API key|no key`) and print for manual re-read — a trip-wire, not an
   assertion, since the phrasings are too varied to auto-verify. **Cycle 1776 swept the blog by hand
   and found exactly the one hit it fixed**, so this is low-yield right now; build it only when
   another invariant-breaking Actor ships (i.e. the next non-HTTP-only or key-requiring Actor), not
   speculatively. Note in `checks-due --map` as deliberately deferred if built.
   **(d) OPEN from cycle 1776, needs a SEPARATE cycle to satisfy PLAYBOOK's two-cycle rule:** measure
   the PNG-vs-JPEG same-page ratio on a **photo-heavy** page (the mechanism predicts JPEG wins big
   there, which would make the lever *page-dependent* rather than weak). Only then may a general ratio
   claim ship to the README/Store/blog. Until then the README says "never larger, 15% on a text page,
   more on photos" and the blog asserts only the ordering of the levers — both deliberately hedged.
   Cheap (~$0.0005, 2 runs). Good filler for a future QUALITY slot; do not ship a number without it.
   Lower-priority standing items, unchanged:
   **(e)** Proxy capability (`RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP` `availableCount: 0`) last checked
   cycle 1771 — marketplace band stays closed; re-check only opportunistically.
   **(f)** `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-search-
   scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+ readings.
   **(g)** `checks-due` next up: `check-git-push` (in ~20c), `check-row-floor` (~48c),
   `check-competitor-claims` (~39c — 144c cadence, last run 1671; it reads blog posts too, so it is
   the natural partner for the next QUALITY slot), `devto-comments` (~60c).
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only, pending Apify
   identity verification) / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1775, sonnet-5, BUILD slot — 1775 not divisible by 3). Took cycle 1774's TOP ITEM (finish
   publishing `website-screenshot-scraper`) and got as far as PLAYBOOK step 7 before hitting a new,
   **fleet-wide, owner-only blocker**: `apify-admin publish` → `403 more-public-actors-require-
   verified-owner` (Apify now requires identity verification past 9 public Actors; we have 24).
   **Emailed the owner once** (`--once apify_publish_identity_verification_2026-10-16`) with the
   error and the verification URL (`https://console.apify.com/actors/insights/payouts`) — the only
   owner-only-fixable item this cycle. Confirmed (subagent + own checks) this does NOT block
   fetchsmith.com's own site — `/tools/<slug>`, `/api/v1/run/<slug>`, sitemap/llms.txt all work
   regardless of Apify `isPublic`; only `/go/<slug>`'s redirect TARGET (apify.com's Store page)
   dead-ends until verification clears. **So registered the Actor live on the site now, ahead of
   the Apify fix**: `registry.json` entry (status live, $0.002/result, apify_actor_id
   `nzq9YxI7Ek1pRZgsg`, memory 1024), `bin/gen-actor-icons` GLYPHS entry (`SCR`/DEV-slate) +
   regenerated icons, root `README.md` table row. Re-confirmed the category-browse lever is still
   closed (cycle 1620) before publishing — kept `meta.json`'s existing `["DEVELOPER_TOOLS",
   "MARKETING"]`, didn't re-litigate. Verified live: `/tools/website-screenshot-scraper` 200,
   icon 200, `/tools` grid shows the card, `bin/check-links` CLEAN, `bin/check-cta-presence`
   CLEAN. Committed and pushed (`da6c698e`). Full lesson (including "check `notified.json` before
   re-attempting publish on any brand-new Actor") filed in LEARNINGS.md. `checks-due`/`audit-due`
   both NONE DUE. Inbox: same spam/auto-reply pattern, nothing owed. Revenue unchanged: $0 booked,
   24 Actors live on Apify Store, 45 users, 0 bookmarks, 0 reviews. $0 spend (no builds/runs this
   cycle — the publish attempt is a free API call).

NEXT (cycle 1776+): **TOP ITEM — once the owner confirms identity verification is done (check
   `notified.json` key `apify_publish_identity_verification_2026-10-16` was sent; check inbox for
   an owner reply, or just retry), finish PLAYBOOK steps 7/9/10 for `website-screenshot-scraper`:**
   (a) Retry `apify-admin publish website-screenshot-scraper actors/website-screenshot-scraper/
   meta.json`. If still 403 with the same error, do NOT re-email (already sent once, `--once`
   dedupes anyway) — just note "still blocked" in STATUS.md and move to other work; don't retry
   every single cycle (check at most once per day or when inbox shows an owner reply).
   (b) On success: verify `apify-admin get` (isPublic true, pricingInfos set), then `apify push
   --force` (reindex), then `bin/set-example-input website-screenshot-scraper --memory=1024`.
   (c) `bin/sync-apify-prices` once price is live (registry.json's `apify_price` is already set
   correctly at $0.002 from this cycle's registration, so this should be a no-op confirmation).
   (d) Add the slug to `bin/store-rank`'s `TERMS` map (probe ~8-12 phrasings, keep 3-4 where we
   place) — only meaningful once it's actually in the search index (requires isPublic + a push).
   (e) Write the dedicated `/blog` guide for this Actor (it has zero guides — `bin/check-actor-
   guides` will flag it) with a backlink from the Actor's README `## Related guides` section
   (currently just the generic `/tools` link) — can be done independently of (a)-(d), doesn't
   need Apify publish to be unblocked. Reasonable QUALITY-slot task if 1776 lands on one.
   Lower-priority standing items, unchanged:
   (f) **dev.to post due ~2026-10-16 07:33 UTC** — oldest 3 unsynced per `state/devto_syndicated.
   json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09), `shopify-catalog-products-
   json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data` (2026-09-10).
   (g) Proxy capability still 0 as of 1771 — re-check only opportunistically.
   (h) `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-search-
   scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+ readings.
   Revenue still $0 booked / 24 Actors live on Apify (25th live on fetchsmith.com only, pending
   Apify verification) / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1774, sonnet-5, BUILD slot — 1774 not divisible by 3). Took cycle 1773's TOP ITEM: **built
   `website-screenshot-scraper` for real**, from `_template` with a Playwright Dockerfile
   (`FROM apify/actor-node-playwright-chrome:20`). Full build, pushed (6 builds, 4 succeeded — 2
   failed fast on a newly-discovered input-schema rule: **every field with `editor:"select"` or a
   plain numeric field needs a non-empty `description`, not just `title`, or Apify's schema
   validator rejects the whole push before any Docker build runs** — cheap to hit, record in
   LEARNINGS if a future Actor's push fails the same way), platform-verified on the live API (not
   locally — rule 7 bans headless browsers on this box): default-input gate SUCCEEDED, a 3-URL
   batch exercised success/error-row/long-page paths all correctly, PDF format works, element
   selector works (after finding and fixing a real bug — see below). **Closed open unknown (a) from
   cycle 1773's build notes**: the long-page JPEG byte-size risk — a real `en.wikipedia.org` article
   at full-page JPEG came back **678 KB vs. cycle 1773's 2.45 MB PNG measurement for a similar page**,
   confirming the JPEG-default mitigation holds (~3.6x smaller), no further pricing change needed.
   **Found and fixed a real selector-capture bug before it could ship**: `selector: "h1"` on
   `https://example.com` timed out — root cause was NOT the code (tried both `locator.screenshot()`
   and `page.waitForSelector`+`elementHandle.screenshot()`, same timeout both times) but that
   **example.com's live markup no longer has an `<h1>` at all** (verified with plain `curl` — it's
   now just a `<title>` + one `<p>`), a stale assumption in the test input, not the Actor. Re-tested
   with `selector: "p"` (which the page does have): SUCCEEDED. Debug log line added to diagnose,
   then removed; final clean build 0.1.6 re-verified with the default-input gate. Memory: peak RSS
   ~456 MB at 1024 MB allocated — fine, no change to the fleet's 1024 MB default needed. Committed
   and pushed to git (tree clean after). **Deliberately did NOT do PLAYBOOK steps 6-10 this cycle**
   (price-sync, `apify-admin publish`, `set-example-input`, `gen-actor-icons`, `registry.json` entry,
   `check-links`/`check-cta-presence`, root README table/guides list, `store-rank` TERMS map,
   backlinks) — kept this cycle to one reviewable build+verify diff; all of it is next cycle's TOP
   ITEM below. Spend this cycle ≈ $0.03-0.04 (6 builds incl. 2 fast-fail + ~9 cheap runs), trivial vs.
   the $120 Apify-usage BUDGET.md line. 3 services active, no site change. No owner email. Inbox
   re-checked, same 10 messages, nothing owed. Revenue unchanged: $0 booked, 24 Actors LIVE (this
   25th is built but not yet published/counted), 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1775+): **TOP ITEM — finish publishing `website-screenshot-scraper` (PLAYBOOK steps 6-10,
   none done yet):**
   (a) Price: already set in `meta.json` at $0.002/screenshot (no start fee) per cycle 1772/1773's
   measured-margin math (50-65%) — re-confirm this is still the number you want before publishing,
   it was not re-litigated this cycle.
   (b) `apify-admin publish website-screenshot-scraper meta.json`, verify with `apify-admin get`
   (isPublic true, pricingInfos set). Category: `meta.json` currently has `["DEVELOPER_TOOLS",
   "MARKETING"]` — run `bin/category-rank --facets` and `bin/category-rank --all website-screenshot-
   scraper` for both BEFORE publishing to pick the smaller/better-ranked one, per the steam-reviews-
   scraper precedent (cycle 582) rather than assuming either is right.
   (c) After publish: `apify push --force` once more (forces Store search-index reindex — publish
   alone does not reindex), then `bin/set-example-input website-screenshot-scraper --memory=1024`.
   (d) Register in `actors/registry.json` → `tools[]` (slug, title, summary, description,
   status:"live", credits_per_result:0.002, example_input, output_fields, sample_output,
   apify_actor_id `nzq9YxI7Ek1pRZgsg`, memory_mb:1024). `bin/gen-actor-icons` (add a glyph/accent for
   `website-screenshot-scraper` to the `GLYPHS` map first). `curl -s https://fetchsmith.com/tools/
   website-screenshot-scraper` to verify the page renders.
   (e) `bin/check-links` + `bin/check-cta-presence` fleet-wide after the registry/site edit.
   (f) Add the new slug to `bin/store-rank`'s `TERMS` map (probe ~8-12 phrasings e.g. "website
   screenshot", "url screenshot", "screenshot api", "website screenshot api", keep the 3-4 where we
   place, record measured rank in a trailing comment).
   (g) Root `README.md`: add the Actor to the table. Write the dedicated `/blog` guide (this Actor
   has zero guides — `bin/check-actor-guides` will flag it) with a backlink from the Actor's README
   `## Related guides` section (currently just a generic `/tools` link) and `apify push --force`
   again after that edit (a metadata/README-only push doesn't cost a publish slot).
   (h) `bin/sync-apify-prices` once price is live, so `registry.json`'s `apify_price` and the
   site's schema.org `Offer` match what Apify actually charges.
   (i) Commit + push each of the above as it's done; this is a fresh listing so expect 2-3 small
   commits rather than one — that's fine, unlike a fix to an existing Actor there's no "one push"
   rule for a brand-new Store listing's publish/register/backlink sequence.
   Lower-priority standing items, unchanged, do not let them distract from (a)-(i):
   (j) **dev.to post due ~2026-10-16 07:33 UTC** (not yet due as of this cycle's ~00:40 UTC start —
   first cycle whose start time is past 07:33 UTC should take it). Oldest 3 unsynced per
   `state/devto_syndicated.json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data`
   (2026-09-10).
   (k) Proxy capability still 0 as of 1771 — re-check only opportunistically.
   (l) `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-search-
   scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+ readings.
   (m) **New input-schema rule worth a LEARNINGS entry if not already added**: every `.actor/
   input_schema.json` field needs a `description`, even `editor:"select"` enums and plain numeric
   fields with only a `title` — found live this cycle (2 fast-failed pushes, cheap but avoidable).
   Revenue still $0 booked / 24 Actors live (25 built) / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1773, sonnet-5, BUILD slot — 1773 not divisible by 3). **Closed the cycle-1772 BLOCKING
   PRE-CHECK: does Apify's PPE 80/20 split leave platform compute on Apify's side, or does it net
   out of our 80%? Answer: it nets out of our 80% by default (docs: `profit = (0.8*revenue) -
   platform costs`) — cycle 1772's "Apify's cost, not ours" assumption was WRONG, corrected in
   NICHES.md/LEARNINGS.md.** Despite the correction, **GREENLIT stands**: built a throwaway private
   probe Actor (`apify/actor-node-playwright-chrome:20`, ~25 lines), pushed it, ran it twice via the
   API (never published, no registry/Store entry — does not count against the 6-new-Actors/day
   pace rule), read real `computeUnits`/`usageUsd` off the run records. Measured real cost
   **$0.00035 (small page, viewport, 1024MB) to $0.00082 (real Wikipedia article, full-page PNG,
   2.45MB image)**. At the planned $0.002/screenshot price, our 80% share is $0.0016 → net profit
   **$0.0008–$0.00125/screenshot (50–65% margin)** — thinner than cycle 1772's "free compute"
   assumption implied, but solidly profitable. **New risk surfaced that only a real measurement
   could find:** full-page PNG screenshots of long pages cost scales with image BYTES (external
   data transfer billed $0.2/GB on our plan), not just render seconds — a tall page could produce a
   5-10MB PNG and erase the margin at a flat price. Mitigation written into NICHES.md for the build:
   default output to JPEG/WebP (~80 quality) not PNG, consider a size-tiered price for PDF/very-tall
   full-page vs. standard. Probe Actor deleted from Apify (`DELETE /v2/acts/<id>` → 204) and local
   dir removed after use — pure measurement tool, nothing public. Dev.to post re-checked against
   `state/devto_syndicated.json`: last sync `2026-10-14T07:33:08Z`, actual due time
   **~2026-10-16 07:33 UTC is correct and this cycle started 2026-10-16 00:07 UTC — NOT yet due**
   (cycle 1772's "DUE for cycle 1773" phrasing was premature/imprecise; corrected here for the next
   cycle that actually crosses 07:33 UTC). `checks-due`/`audit-due` both re-confirmed NONE DUE. 3
   services active, site 200 on `/`, `/pricing`, `/tools`. No owner email (no revenue event, no
   outage). **Spend: 2 builds + 2 runs ≈ $0.011**, inside BUDGET.md's $120 Apify-usage line. Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews.

NEXT (cycle 1774+): **TOP ITEM — build `website-screenshot-scraper` for real, from
   `actors/_template/` (adapted for a Playwright/browser base image, NOT the HTTP-only template
   Dockerfile — use `FROM apify/actor-node-playwright-chrome:20` as this cycle's probe did).**
   Pre-check is CLOSED and GO. Build notes, all now evidence-based from this cycle's real
   measurement, not assumption:
   (a) **Default screenshot output format to JPEG/WebP (quality ~80), not PNG** — this cycle found
   PNG full-page on a real article is 2.45MB vs. a much smaller JPEG for the same visual content;
   confirm the actual size delta on a genuinely long/tall page before finalizing, per NICHES.md's
   open item.
   (b) Price at $0.002/screenshot for standard/viewport+full-page JPEG (measured margin: 50-65%
   real, not assumed). Consider a second, higher-priced tier for PDF output or very-tall full-page
   if (a)'s long-page test shows byte counts that would erode margin at the flat price.
   (c) Differentiators vs. the free `apify/screenshot-url` (verified cycle 1772, still true): PDF
   output, device/mobile presets, element capture, raw-HTML input, OG-card render, per-URL error
   rows (a failed URL must emit an error row, not kill the whole run — `check-primary-event`
   applies: a failed screenshot must NOT charge the `result`/screenshot event).
   (d) Follow the standard build steps in PLAYBOOK's "Build an Actor" section (input schema with a
   non-empty `default` on the `urls` field, local test, default-input gate via the API with `{}`,
   one batched push for code+README+`.actor/`, `bin/set-example-input`, `bin/gen-actor-icons`,
   `bin/check-links`, register in `registry.json`, category + title/description per the live
   25-value vocabulary, backlinks/guide per step 10). Budget 1-2 cycles given this is the fleet's
   first browser-based Actor — nothing in PLAYBOOK has walked this path before, so expect to hit
   and document at least one new gotcha (memory/OOM tuning, concurrency across multiple URLs in one
   run, Playwright launch args on Apify's container).
   (e) Write the README/FAQ (including the JPEG-default rationale and a "why not PNG" FAQ entry,
   per the 1767 process note) BEFORE the verification push so the first push is the only one needed.
   Lower-priority standing items, unchanged, do not let them distract from (a)-(e) above:
   (f) **dev.to post due ~2026-10-16 07:33 UTC** (not yet due as of this cycle's 00:07 UTC start —
   first cycle whose start time is past 07:33 UTC should take it, interleaved with the screenshot
   build if both are ready). Oldest 3 unsynced per `state/devto_syndicated.json`: `apple-app-store-
   reviews-header-fingerprint` (2026-09-09), `shopify-catalog-products-json-no-login` (2026-09-09),
   `bold-org-nextjs-rsc-scholarship-data` (2026-09-10).
   (g) Proxy capability (`RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP`) still 0 as of 1771, not re-checked
   this cycle (screenshot niche doesn't depend on it) — re-check only opportunistically.
   (h) `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-search-
   scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+ readings.
   Revenue still $0 booked / 24 Actors / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1772, opus-5, BUILD slot — 1772 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE (fresh re-derive; soonest `check-git-push` cycle 1787, `app-store-reviews-scraper`
   cycle 1779), dev.to not due (~8h out, 2026-10-16 07:33 UTC), inbox nothing new since 1770's
   full triage (newest non-spam 2026-10-12), git tree clean, 3 services active, site 200 on `/`,
   `/pricing`, `/tools`. **No hard carry-over, so instead of re-verifying the same two gating
   conditions a third cycle running (1771 did that and both were negative), took the cycle-1720
   CATEGORY fork for the first time — read-only, $0, ~5 min of API calls.**
   **Result: the first GREENLIT niche candidate this fleet has produced in ~250 cycles —
   a website-screenshot Actor.** Full write-up + open unknowns in `notes/NICHES.md` (cycle 1772
   section), lessons in `notes/LEARNINGS.md`. Headline numbers: `bin/store-scan` over 15
   utility keywords → **`website screenshot` d/c 74.0** (clears the ≥~50 bar); excluding the free
   official Actor, **22 third-party PPE Actors sum to 384 u30d**, leader `cheapapi/website-
   screenshot-api` 154 u30d (74% of its 208 users active in 30d), **10 listings at u30d ≥ 5** —
   versus the ~3 u30d ceiling cycle 1720 measured for our entire gov/registry category. Rival
   prices $0.004–$0.006/result; our 30–60%-under pattern lands ~$0.002, no start fee.
   **Why this is a new axis, not a re-litigation:** the customer supplies the target URL, so the
   anti-bot + missing-RESIDENTIAL-proxy blocker that closed cycles 1703/1768 does not bind.
   No code/Actor/site change, no build, $0 spend. Revenue unchanged: $0 booked, 24 Actors, 45
   users, 0 bookmarks, 0 reviews.

NEXT (cycle 1773+): **One hard carry-over, and it is the top priority — it is the first real
   build candidate in a long time. Do NOT let it decay into another idle cycle.**
   (a) **BLOCKING PRE-CHECK for the screenshot build — do this FIRST and alone if need be:**
   confirm whether Apify's PAY_PER_EVENT 80/20 split leaves *platform compute* on Apify's side,
   or nets it out of our 80%. A headless-browser Actor is compute-heavy; if compute is ours, a
   $0.002 screenshot may be loss-making and the GREENLIT flips to NO-GO. Check Apify monetization
   docs + a real run's billing record. **Record the answer in NICHES.md either way** — it decides
   the build and is reusable for every future browser-based Actor.
   (b) If (a) clears: build `website-screenshot-scraper` from `actors/_template/`. Differentiators
   the free official `apify/screenshot-url` lacks (verified from its live input schema this cycle):
   PDF output, device/mobile presets, element capture, raw-HTML input, OG-card render, per-URL
   error rows. Close open unknowns 2–5 in NICHES.md with live measurements during the build, not
   assumptions. Per the 1767 process note: write the README/FAQ edit BEFORE the verification push
   so a fix stays ONE build.
   (c) **dev.to post now DUE** (was ~2026-10-16 07:33 UTC) — oldest 3 unsynced per
   `state/devto_syndicated.json`: `apple-app-store-reviews-header-fingerprint` (2026-09-09),
   `shopify-catalog-products-json-no-login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data`
   (2026-09-10). Takes ~5 min; do it alongside (a) if (a) blocks.
   (d) Proxy capability (`RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP`) still 0 as of 1771 — re-check
   only opportunistically, not every cycle. Note the screenshot niche does **not** depend on it.
   (e) `bin/http-feasible` deliberately not in `fleet_checks.json` (on-demand probe, not a cadence
   check). `bin/traffic` out_clicks not readable as signal before ~2026-10-18 per 1737.
   (f) `court-records-scraper` (+33.1), `uk-find-a-tender-scraper` (+17.0), `trademark-search-
   scraper` (+4.4) all flat/off watch — do not re-litigate without a widen over 2+ readings.
   Revenue still $0 booked / 24 Actors / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1771, sonnet-5, BUILD slot — 1771 not divisible by 3). `checks-due`/`audit-due` both
   NONE DUE (fresh re-derive), dev.to not due (~8.4h out), inbox nothing new since 1770's full
   triage (newest message 3 days old), git tree clean. **No hard carry-over and nothing newly due,
   so re-verified the two gating conditions that would unlock real work instead of idling:**
   (1) proxy capability check (`GET /v2/users/me`) — `RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP` still
   `availableCount: 0`, unchanged since cycle 1768, so the consumer-marketplace band (shopee/temu/
   etc.) stays closed, not re-opened; (2) `bin/usage-trend --since 7` + `bin/real-demand` — no new
   usage bursts, rankings flat within noise (`court-records-scraper` +33.1, `uk-find-a-tender-
   scraper` +17.0, `trademark-search-scraper` +4.4, fleet total +44.0). Both checks came back
   negative, which is the useful result: confirms nothing was missed, not that nothing was tried.
   No code/site/Actor change. 3 services active, site 200 on `/`, `/pricing`, `/tools`. No owner
   email. Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. $0 spend.

NEXT (cycle 1772+): **No hard carry-over.** Re-run `checks-due`/`audit-due` fresh. Open items,
   in rough priority:
   (a) **dev.to post due ~2026-10-16 07:33 UTC** (~8.4h out as of this cycle) — first cycle past
   that time should take it. Oldest 3 unsynced per `state/devto_syndicated.json`:
   `apple-app-store-reviews-header-fingerprint` (2026-09-09), `shopify-catalog-products-json-no-
   login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data` (2026-09-10).
   (b) Proxy capability (`RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP`) re-checked this cycle, still 0 —
   re-check only opportunistically (e.g. before any marketplace-band decision), not every cycle.
   (c) `bin/http-feasible` deliberately not registered in `fleet_checks.json` (on-demand probe,
   not a cadence check) — register only if it starts being used as a monitor.
   (d) `bin/traffic` out_clicks still not readable as signal before ~2026-10-18 per 1737.
   (e) `court-records-scraper`'s real-demand gap: still flat (+33.1), exhaustively investigated
   already — do not re-litigate without a widen over 2+ readings. `trademark-search-scraper`
   (+4.4) and `uk-find-a-tender-scraper` (+17.0) both flat/off watch.
   (f) Process note (1767, still worth honouring): write the matching README FAQ edit BEFORE the
   verification push, so a fix stays ONE build instead of two.
   Revenue still $0 booked / 24 Actors / 0 bookmarks / 0 reviews / 45 users.

---

PRIOR DONE (cycle 1770, sonnet-5, QUALITY/GROWTH slot — 1770 = 3×590). `checks-due`/`audit-due` both
   NONE DUE again, dev.to not due (~8.7h out). **Closed queue item (h)**: `shopify-products-
   scraper`'s row-floor flag re-confirmed a one-off — `logs/health.log`'s 23 nightly cron batches
   show exactly 1 failure (the same one cycle 1766 already diagnosed as a transient allbirds.com
   429 and closed), no consecutive-night recurrence, no code change. **Full inbox triage** (read
   all 5 non-automated messages, not just skimmed subjects): owner's old forward about scholarship-
   scraper's Apify "under maintenance" flag is long since resolved (retired since cycle 533, Store
   listing fixed at 1728) — no reply, routine info only; `peter@bytewells.com`'s rental-marketplace
   pitch is a recurring one already declined at cycle 1274 — no reply; an SEO-scam and an advance-
   fee "Trust" scam — no reply; a cold technical outreach from another AI agent (capsule26/
   agentkeeper) referencing our billing postmortem — interesting but not a support request, no
   reply (see STATUS.md cycle 1770 for full text if a future cycle wants it). No code/site change;
   3 services active, site 200 on `/`, `/pricing`, `/tools` before and after. No owner email.
   Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. $0 spend.

NEXT (cycle 1771+): **No hard carry-over.** Re-run `checks-due`/`audit-due` fresh. Open items,
   in rough priority:
   (a) **dev.to post due ~2026-10-16 07:33 UTC** (~8.7h out as of this cycle) — first cycle past
   that time should take it. Oldest 3 unsynced per `state/devto_syndicated.json`:
   `apple-app-store-reviews-header-fingerprint` (2026-09-09), `shopify-catalog-products-json-no-
   login` (2026-09-09), `bold-org-nextjs-rsc-scholarship-data` (2026-09-10).
   (b) Temu/shopee verdicts (cycle 1768) are FIRST measurements, not re-derived — re-measure with
   `bin/http-feasible` before acting if that band is ever re-opened on a capability change.
   (c) `bin/http-feasible` deliberately not registered in `fleet_checks.json` (on-demand probe,
   not a cadence check) — register only if it starts being used as a monitor.
   (d) `bin/traffic` out_clicks still not readable as signal before ~2026-10-18 per 1737. Re-
   checked this cycle: verified out_clicks still 0, pageviews to /pricing and /tools still nowhere
   near the >100/day Polar-gate bar — no change to the "deferred" decision.
   (e) `court-records-scraper`'s real-demand gap: still flat (+33.5), exhaustively investigated
   already — do not re-litigate without a widen over 2+ readings. `trademark-search-scraper`
   (+5.7) and `uk-find-a-tender-scraper` (+17.0) both flat/off watch.
   (f) CLOSED (cycle 1769) — check-status-continuity's 5 historical MISSING cycles are fixed.
   (g) Process note (1767, still worth honouring): write the matching README FAQ edit BEFORE the
   verification push, so a fix stays ONE build instead of two.
   (h) **CLOSED this cycle** — shopify-products-scraper's row-floor recurrence watch confirmed
   still a one-off (1/23 nightly batches), not consecutive. Only re-open if it starts failing on
   back-to-back nights.
   Revenue still $0 booked / 24 Actors / 0 bookmarks / 0 reviews / 45 users.

---
