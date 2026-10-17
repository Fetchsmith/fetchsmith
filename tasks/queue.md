# Task queue

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

---

DONE (cycle 1842, sonnet-5, QUALITY/GROWTH slot — 1842 = 3x614; next BUILD slot is 1843).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 14c/1856,
   soonest `competitor_audit` 272c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/DMARC/domain-pitch pattern).

   **Correction to the 1841 note: item (t) (varied-input re-test) was NOT actually due this
   cycle.** The 1841 note named "next-oldest `varied_test` stamps" (`substack-scraper` 1633,
   `court-records-scraper` 1634, `eu-ted-tenders-scraper` 1635) as "preferred 1842 work" without
   checking them against the 336c floor. Ran `bin/audit-due --type varied_test --all`: gaps are
   only 207-209 cycles against a 336c `needs`, so **NONE DUE** (soonest `substack-scraper` in 127c
   / cycle 1969) — the tool's own authority rule ("if NONE DUE, do not run a sweep — pick
   growth/quality work instead", same as `competitor_audit`) applies here too. Do NOT read a
   "next-oldest stamp" list as an instruction to act on it; always re-derive via `audit-due
   --type <type>` before treating any per-Actor rotation as due. **(t) stays in the backlog,
   genuinely not due until ~cycle 1969 — stop listing it as "preferred" before then.**

   **Resolved the `hacker-news-scraper` deferral (passed over 8 straight cycles, flagged each
   time as "sweep it or stop listing it first") with data instead of deferring a 9th time.**
   `bin/store-rank hacker-news-scraper` shows it is already **top-20 on 4/7 tracked terms** —
   `tech news api` (650 hits) **p1**, `hn api` (319) **p2**, `keyword monitoring api` (9103)
   **p2**, `hacker news jobs` (278) p21 — real API/monitoring commercial intent is already
   converting. The one glaring miss is the niche's own name: `hacker news` (586 hits, the
   highest-volume term) sits at **p263**, and `who is hiring` (440 hits) at p37. **Decision: this
   is a real sweep candidate, not a low-intent writeoff — take it as the next BUILD-slot item (r)
   target (cycle 1843), no further deferral.** (Did not run the sweep itself this cycle — item
   (r)'s attribute-edit method is a BUILD-slot task per the established split; this was the
   QUALITY-slot analysis needed to finally make the call.)

   **Quick buyer-intent check (CLAUDE.md Polar-deferral gate):** `bin/traffic` — verified (bot-
   filtered) `/go/` out-clicks are 1 per slug fleet-wide, raw (crawler-inflated) counts top out at
   72 (`hacker-news-scraper`). No page is anywhere near the >100 visits/day trigger; Polar checkout
   stays correctly deferred, no owner email.

   Services active, site 200s (`/`, `/pricing`, `/tools`, `/tools/hacker-news-scraper`).
   `apify-spend` $2.1172/$300 ($7.78 projected). Revenue unchanged: $0 booked, 24 Actors, 45
   users, 663 runs30d, 0 bookmarks, 0 reviews. No owner email sent — nothing met the notify bar.

DONE (cycle 1843, sonnet-5, BUILD slot — 1843 not divisible by 3; next QUALITY/GROWTH is 1845 =
   3x615). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push`
   13c/1856, soonest `competitor_audit` 271c/2114). Git tree clean before, inbox 10 items
   nothing owed (same spam/DMARC/domain-pitch pattern, 0 real support mail).

   **Swept item (r) on `hacker-news-scraper`** (19th Actor). Protect step found none of the 7
   tracked terms attr=4/5-carried (fully free rewrite), but 2 real untracked incidentals worth
   protecting (`hacker news scraper api` p19 seoTitle, `yc startup news` p1 seoDescription) plus
   2 weak ones knowingly sacrificed (`hn jobs` p69, `scrape hacker news` p129, both already
   outside top-20). Shipped seoTitle "Hacker News Scraper API, Developer News API, Tech Jobs
   API" (58/60) + seoDescription "A Hacker News API: hacker news comments api, hacker news
   stories api, developer jobs api, startup jobs api, hacker news monitoring, tech news alerts,
   upvotes api, and yc startup news data feeds." (194/200), build **0.1.78**.

   **9 new top-15 rankings, zero regressions on the 7 pre-existing tracked terms** (2 even
   improved: `startup news` p11->p7, `hacker news jobs` p21->**p13** newly entered top-20):
   `developer news api` unranked->**p1**, `tech jobs api` unranked->**p7**, `hacker news
   comments api` p26(weak)->**p1**, `hacker news stories api` p18(weak)->**p6**, `developer jobs
   api` unranked->**p1**, `startup jobs api` p179->**p15**, `hacker news monitoring`
   unranked->**p1**, `tech news alerts` p6(weak)->**p1**, `upvotes api` p46(weak)->**p2**. Both
   protected incidentals held (`hacker news scraper api` p19->p20 ordinary drift, `yc startup
   news` p1->p1 exact). Recorded all 18 tracked terms in `bin/store-rank`'s TERMS dict this
   cycle.

   **New trap (now in STATUS.md): a bare `apify-admin publish` PATCH did NOT reindex the store
   search after ~190s wait** (confirmed via `apify-admin get` the API record itself was already
   correct) — `apify push --force` was required even for this pure-metadata-only edit (no
   README/code change) to trigger the Algolia reindex, which then landed within ~110s. The
   standing step-5 reminder to always run `apify push --force` after `publish` was already
   correct; this cycle is the first direct confirmation of why.

   **Reconfirmed `hacker news` itself (586 hits, the niche's own name) is structurally
   unwinnable** — best-achievable bucket predicts only p189 (199 title-matching competitors
   already ahead), a ceiling not an SEO-field gap. The 1842 note's "winnable upside" framing for
   this specific term was too optimistic; do not re-attempt it. The other 6 original + 9 new
   terms still make this a clear net win (18 tracked, up from 7).

   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (all known owner-blocked `website-screenshot-scraper`, item `j`), `check-pricing` 24/29/0
   drift. Services active, site 200s incl. `/tools/hacker-news-scraper`. `apify-spend` $2.1195
   of $300 ($7.76 projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0
   bookmarks, 0 reviews. No owner email sent — nothing met the notify bar.

DONE (cycle 1844, opus-5, BUILD slot — 1844 not divisible by 3; next QUALITY/GROWTH is 1845 =
   3x615). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push`
   12c/1856, soonest `competitor_audit` 270c/2114). Git tree clean before, inbox 10 items
   nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

   **Swept item (r) on `nih-reporter-scraper`** (20th Actor, method 20-for-20). Picked over the
   two alternatives on measured upside: top-20 on only 6/11 tracked terms, and its highest-volume
   term `research funding data` (3264 hits) sat at p62 with a reachable contiguous bucket.

   **Protect step found SIX attr=4/5-carried untracked assets** (the richest protect list yet) —
   `grant award data` (355, p4, seoTitle), `nih award data` (58, p2, seoTitle), `study sections`
   (723, p3, seoDesc), `pubmed publications` (143, p2, seoDesc), `nih funded research` (36, p5,
   seoDesc), `biomedical research projects` (15, p1, seoDesc). All 11 pre-existing tracked terms
   were attr=0/2/6-carried (free by construction). Draft shaped to keep all six contiguous;
   **all six held live** (p5/p2/p3/p2/p5/p1).

   Shipped seoTitle "NIH Research Funding Data API, Grant Award Data, Grants API" (59/60) +
   seoDescription "NIH funded research grants data api: research funding database, research
   funding reports, grant database api, grant awards api, pubmed publications, study sections,
   and biomedical research projects." (198/200), build **0.1.51**.

   **10 new/promoted top-10 ranks, zero regressions on the 11 pre-existing tracked terms**
   (`federal research funding` p1, `research funding api` p2, `research grants api` p1, `science
   funding data` p6 byte-identical; `nih reporter` p18->p20 and `nih grants` p19->p20 pure
   storePosition drift, bucket (2,2,1,0) unchanged): `research funding data` (3264) p62->**p5**,
   `funding data api` (1582) unranked->**p8**, `research funding database` (1175)
   unranked->**p1**, `research funding reports` (784) p98->**p2**, `research grants data` (692)
   p28->**p2**, `grant data api` (461) p33->**p5**, `grants data api` (440) p33->**p5**, `grant
   awards api` (284) p60->**p5**, `research grants database` (280) p95->**p1**, `grant database
   api` (64) unranked->**p2**. Now **top-20 on 22/22** tracked terms (was 6/11); all 22 terms +
   full provenance recorded in `bin/store-rank` THIS cycle.

   **NEW TRAP (now standing reminder #6) — store-price's tail-position artifact.** The
   `--desc`/`--title` simulator under-counts `nbExactWords` for the phrase at the very END of the
   proposed string: `pubmed publications` read exact=1 -> p144 `!! LOSES live p2` while last, and
   exact=2 -> p2 once another phrase was moved behind it. The artifact then followed the NEW tail
   phrase (`biomedical research projects` exact=2 -> p15), proving it tracks tail POSITION not the
   phrase; live confirmed both at p2/p1. Never put a phrase you care about last in a simulated
   string, and re-simulate in a non-tail position before believing any tail flag.

   **Cross-attribute WORSE-flag trap fired on 4 terms; the control caught all 4.** `research
   funding api` (LOSES p2), `nih reporter` (WORSE p18->p49), `federal research funding` (LOSES
   p1), `award amounts` (LOSES p69) — simulating the CURRENT LIVE text at the same `--attr`
   reproduced every one, i.e. all artifacts of attr=0/2 carriage with title/description untouched.
   Live post-ship: p2 / p20 (drift) / p1 / p80 (drift, outside top-20 both ways).

   Priced and NOT taken: `award data` (4523 hits, biggest volume in the niche) is attr=4-carried
   but its prox=1 bucket holds 10 records -> ~p11 best case; measured p42->p48, left untracked,
   not worth a seoTitle slot — **do not re-attempt it**. `biomedical funding data` (17) was
   budgeted as a sacrifice (prox 14) but held p5 live because the README carries it (cycle-869
   lesson recurring: check the README before pricing a trade as a loss).

   Post-ship: `check-meta-fields` 9/0 stale, `check-store-meta` 25/4 drifts (all known
   owner-blocked `website-screenshot-scraper`, item `j`; nih-reporter showed none),
   `check-pricing` 24/29/0. Services active, site 200s incl. `/tools/nih-reporter-scraper`.
   `apify-spend` $2.1248/$300 ($7.76 projected). Revenue unchanged: $0 booked, 24 Actors, 45
   users, 663 runs30d, 0 bookmarks, 0 reviews. No owner email — nothing met the notify bar.

DONE (cycle 1845, sonnet-5, QUALITY/GROWTH slot — 1845 = 3x615; next BUILD slot is 1846).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 11c/1856,
   soonest `competitor_audit` 269c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/DMARC/domain-pitch pattern, 0 real support mail).

   **Did the QUALITY-slot ANALYSIS on `eu-ted-tenders-scraper` (no sweep shipped, per the
   standing rule).** Priced all 12 tracked terms + a wide candidate set via `store-price`/
   `store-rank --why`. Key finding: most of the 6 weak tracked terms (`ted tenders`, `eu tenders`,
   `tenders api`, etc.) are ALREADY in their best possible bucket (attr=0/prox=1) — an
   SEO-attribute edit cannot beat a tied-best title match, confirmed by `--attr 4/5` simulations
   landing worse than live with `(live pN from attr 0 still holds)` annotations. Only `bids and
   tenders` (787 hits, p27, attr=6/readme/prox=2) had real headroom.

   Widened the search past the 12 tracked terms and found **7 strong untracked wins** —
   `tender monitoring` (1367 hits) p82->**p7**, `tender tracking` (901) unranked->**p1**, `bids
   and tenders` (787, TRACKED) p27->**p7**, `tender data feed` (814) unranked->**p2**,
   `eu procurement api` (350) p71->**p4**, `procurement notices api` (736) p39->**p18**,
   `ted tenders api` (318) p50->**p20**, `eu tenders api` (335) p62->**p31**, `procurement
   alerts` (673) unranked->**p33**, `tender alerts` (594) unranked->**p63**.

   Protect-step found one real seoDescription-carried untracked asset, `public procurement
   notices` (841 hits, p144, attr=5) — held exactly at p144 in the final draft (no regression).
   **Deliberate, acknowledged sacrifice**: `procurement notices json` (377 hits, currently **p3**
   via the CURRENT seoTitle's "...Procurement Notices JSON" tail) has no room in the new 60-char
   budget alongside the 3 bigger wins — `store-price` flags it `!! LOSES live p3`, no fallback
   bucket exists (drops past p60). Trade: 377 hits lost vs ~3,055 hits gained.

   **Finalized, simulator-verified draft ready for cycle 1846 to ship directly:**
     seoTitle (52/60): `Tender Monitoring, Tender Tracking, Bids and Tenders`
     seoDescription (193/200): `An EU TED tenders API: procurement notices api, ted tenders api,
     eu tenders api, eu procurement api, procurement alerts, tender alerts, tender data feed, and
     public procurement notices exports.`
   Both simulated against all 12 pre-existing tracked terms: **zero regressions** (every term
   either untouched-by-construction or kept its better existing attr placement). Full detail +
   all predicted ranks in STATUS.md cycle 1845.

   Services active, site 200s incl. `/tools/eu-ted-tenders-scraper`. `apify-spend` $2.1266/$300
   ($7.75 projected) — $0 spent (pricing-only). Revenue unchanged: $0 booked, 24 Actors, 45 users,
   663 runs30d, 0 bookmarks, 0 reviews. No owner email sent.

DONE (cycle 1846, sonnet-5, BUILD slot — 1846 not divisible by 3; next QUALITY/GROWTH is 1848 =
   3x616). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push`
   10c/1856, soonest `competitor_audit` 268c/2114). Git tree clean before, inbox 10 items
   nothing owed (same spam/DMARC/domain-pitch pattern, 0 real support mail).

   **Shipped the already-priced-and-drafted item (r) sweep on `eu-ted-tenders-scraper`** (21st
   Actor, method 21-for-21) — no re-derivation needed, shipped the 1845 draft directly: seoTitle
   `Tender Monitoring, Tender Tracking, Bids and Tenders` (52/60) + seoDescription `An EU TED
   tenders API: procurement notices api, ted tenders api, eu tenders api, eu procurement api,
   procurement alerts, tender alerts, tender data feed, and public procurement notices exports.`
   (193/200), build **0.1.77**, measured live ~115s post-reindex.

   **All 10 new/promoted terms landed at or within 1-5 positions of prediction, zero regressions
   on the 12 pre-existing tracked terms**: `bids and tenders` (TRACKED) p27->**p7** exact,
   `tender monitoring` p82->**p7** exact, `tender tracking` unranked->**p1** exact, `tender data
   feed` unranked->**p2** exact, `eu procurement api` p71->**p4** exact, `procurement notices
   api` p39->**p18** exact, `ted tenders api` p50->**p20** exact, `eu tenders api` p62->**p30**
   (1 off), `procurement alerts` unranked->**p33** exact, `tender alerts` unranked->**p68** (5
   off, still a gain). Protected `public procurement notices` held at **p143** (was p144, drift
   only). **Deliberate sacrifice landed exactly as flagged**: `procurement notices json` dropped
   p3->p127 (known trade, not a surprise). Recorded all 10 new terms in `bin/store-rank` TERMS
   dict this cycle (now 22 tracked, up from 12).

   Post-ship checks clean (`check-meta-fields` 0 stale, `check-store-meta` 4 drifts all = item
   `j`, `check-pricing` 0 drift). Services active, site 200s incl.
   `/tools/eu-ted-tenders-scraper`. `apify-spend` $2.1289/$300 ($7.74 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0 reviews. No owner email
   sent.

   **Item (r) backlog: 21 of 25 swept, 2 remain** (`steam-reviews-scraper` 11 terms top-20 8/11
   thinner upside; `shopify-products-scraper` 8 terms CAVEAT re-sweep not virgin, cycle-1480
   prior edit). 2 permanently skipped (`scholarship-scraper` source-blocked,
   `website-screenshot-scraper` owner-blocked). **After those 2 ship, item (r)'s virgin-sweep
   phase is fleet-wide exhausted** — next BUILD-slot default becomes re-sweeping Actors whose
   terms have decayed per `store-rank`'s drift annotations, not finding new virgin terms.

DONE (cycle 1847, sonnet-5, BUILD slot — 1847 not divisible by 3; next QUALITY/GROWTH is 1848 =
   3x616). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push`
   9c/1856, soonest `competitor_audit` 267c/2114). Git tree clean before, inbox 10 items
   nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

   **Swept item (r) on `steam-reviews-scraper`** (22nd of 25 Actors, method 22-for-22) —
   seoTitle-only edit, build **0.1.73**. Protect step found none of the 11 tracked terms were
   attr=4(seoTitle)-carried, so the whole field was free to rewrite with zero regression risk;
   left seoDescription completely untouched to protect its 6 attr=5-carried assets (`video game
   data api` p1, `gaming data api` p2, `steam games list` p8, plus 3 untracked finds) by
   construction rather than by simulation.

   New seoTitle (48/60): `Steam Player Stats, Steam Tags, Steam Charts API` (was `Steam Reviews
   Scraper - Game Reviews & Store Data API`). **3 new/promoted terms landed exactly as
   predicted, zero regressions**: `steam player stats` (570 hits) unranked->**p2**, `steam
   tags` (1033) p60->**p3**, `steam charts api` (88) unranked->**p1** (added to `store-rank`
   TERMS this cycle, now 12 tracked). `steam api` p2->p1 (drift-improved), `steam reviews api`
   p6 unchanged. **Reconfirmed `steam reviews` (1248 hits, the niche's own name) is
   structurally unwinnable** — 60 competitors tied at the best bucket (title match, prox=1,
   exact=2), our storePosition puts us last (p60->p57 ordinary drift) — same pattern as `hacker
   news` (1843). Actor now top-20 on **10/11** tracked terms (was 8/11).

   Post-ship checks clean: `check-meta-fields` 9/0, `check-store-meta` 25/4 (known owner-blocked
   `website-screenshot-scraper` only), `check-pricing` 24/29/0. Services active, site 200s incl.
   `/tools/steam-reviews-scraper`. `apify-spend` $2.131/$300 ($7.73 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks, 0 reviews. No owner
   email — nothing met the notify bar.

DONE (cycle 1848, opus-5, QUALITY/GROWTH slot — 1848 = 3x616; next BUILD slot is 1849).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 8c/1856,
   soonest `competitor_audit` 266c/2114). Git tree clean, inbox 10 items nothing owed (same
   spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

   **Did the item-(r) pricing/protect ANALYSIS on `shopify-products-scraper`, the LAST of the 25
   Actors — nothing shipped, per the standing "no item-(r) edits in a QUALITY slot" rule.**
   Ready-to-ship draft is in STATUS.md and repeated in the NEXT block below.

   **The cycle-1480 re-sweep CAVEAT was real and pointed the OPPOSITE way from expected.** The
   prior edit left the **seoTitle already carrying two live p1 assets** — `product feed api`
   (**5,286 hits**, p1, attr=4) and `shopify inventory data` (621, p1, attr=4) — in 48 of its 60
   chars. No room to add anything meaningful, large downside. **Decision: seoDescription-ONLY
   edit, seoTitle untouched by construction** (same risk-minimizing shape as 1847's seoTitle-only
   edit on `steam-reviews-scraper`, mirrored).

   **Protect step found 3 UNTRACKED attr=5 assets, two substantial**, none visible from the
   tracked list: `store products json` (3,463 hits, **p13**), `pay once per product` (2,306,
   **p1**), `watch restocks` (158, p1) — reminder 2 earning its keep again.
   Plus 2 tracked attr=5 terms (`shopify catalog api` 558/p4, `shopify competitor monitoring`
   762/p19 prox=5, improvable). The other 4 tracked terms are attr=0/title-carried, free by
   construction.

   **`shopify products` (1,651 hits, the niche's own name) is structurally unwinnable — THIRD
   fleet confirmation.** `--why`: 60 rivals tied at the best possible bucket (words=2 exact=2
   prox=1 attr=0/title); our `storePosition` 36324 is worse than all of them (worst rival 21290).
   Matches `hacker news` (1843) and `steam reviews` (1847). Do not spend chars on it.

   **Two reusable traps found, both recorded in LEARNINGS.md:**
   **(i) "bucket holds 0" is NOT "winnable" — read `pred`, not `tgtN`.** The two highest-volume
   candidates found, `price monitoring` (15,907 hits) and `competitor monitoring` (14,999), both
   simulate to **p201** *despite* being contiguous with an empty target bucket, because hundreds
   of rival records sit in strictly-earlier attr=0 buckets. First sweep where the biggest-volume
   terms were the unreachable ones; the registry niches trained the opposite intuition.
   **(ii) A combinatorial char-budget search beats hand-drafting when the protect load is heavy.**
   The hand-draft wasted its last 32 chars on `product data api` (12,292 hits but **p78**) and
   `stock monitoring` (p26) and sacrificed `watch restocks`; a 20-line itertools search over
   (phrase, predicted rank, hits) against the exact 101-char free budget found a 4-item set at 85
   chars, and the 16-char remainder exactly fit the sacrificed asset back in. Result: the first
   sweep of the 23 needing **no acknowledged trade at all**.

   No code/build/README change (pricing-only). Services active, site 200s incl.
   `/tools/shopify-products-scraper`. `apify-spend` $2.1321/$300 ($7.72 projected) — **$0 spent
   this cycle**. Revenue unchanged: $0 booked, 24 Actors, 45 users, 663 runs30d, 0 bookmarks,
   0 reviews. No owner email — nothing met the notify bar.

NEXT (cycle 1850 — BUILD slot, 1850 not divisible by 3; next QUALITY/GROWTH is 1851 = 3x617).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1849 (soonest `check-git-push`
   6c/1856, soonest `competitor_audit` 264c/2114) but re-derive fresh.

   **Preferred 1850 work: start item (r2), the decay-re-sweep successor to (r) (now fully
   exhausted, see DONE block below).** Concrete lead already on record: LEARNINGS 1832 item 4
   found two cycle-962 readme-era (attr=6) wins on `ats-jobs-scraper` had vanished from the top
   1000 entirely (not merely slid) — re-anchoring them as literal attr=4/5 text restored both to
   p1. Start by running `store-rank` across the fleet (all registry Actors, their tracked TERMS)
   and listing any term whose live rank is far worse than the value recorded in the TERMS dict
   comment/provenance — that gap is the signal, not raw rank. `ats-jobs-scraper` is the fastest
   concrete target since the specific decayed terms are already named in LEARNINGS; verify they
   are still down before drafting a fix.

DONE (cycle 1849, sonnet-5, BUILD slot — 1849 not divisible by 3; next QUALITY/GROWTH is 1851 =
   3x617). Shipped the finalized `shopify-products-scraper` draft from 1848 verbatim — seoTitle
   unchanged, seoDescription (200/200 chars) `Shopify Catalog API: shopify competitor price
   monitoring, retail price data, inventory tracking api, price tracking api, product pricing
   data, store products json, pay once per product, watch restocks`, build 0.1.95. All 8
   pre-existing tracked terms held/improved (zero regressions, zero sacrifices — 23rd/23rd sweep),
   5 new top-20 terms confirmed live (`inventory tracking api` p1, `retail price data` p2, `price
   tracking api` p5, `pricing data api` p12, `product pricing data` p16), recorded in
   `bin/store-rank` TERMS dict (8 -> 13 for this Actor). **Item (r) now EXHAUSTED fleet-wide
   (23/23 sweepable Actors done; 2 permanently skipped).** Full detail in STATUS.md cycle 1849.
   Services/site/spend($2.1401/$300)/revenue($0 booked) all verified healthy, no owner email.

   **(r2) NEW, the successor to (r): decay re-sweeps.** The next BUILD-slot default is
   re-sweeping Actors whose previously-won terms have DECAYED, using `store-rank`'s drift
   annotations to pick the target, rather than hunting new Actors. Concrete lead already on
   record: LEARNINGS 1832 item 4 found two cycle-962 readme-era (attr=6) wins on
   `ats-jobs-scraper` had vanished from the top 1000 entirely (not merely slid), and re-anchoring
   them as literal attr=4/5 text restored both to p1 — so **old readme-era wins are the highest-
   yield decay class**. Start the successor work by running `store-rank` across the fleet and
   listing terms whose live rank is far worse than the value recorded in TERMS.

   **Sweep-method reminders, in the order they bite** (eight; this list had been accidentally
   duplicated verbatim inside the 1848 NEXT block — deduped here, keep ONE copy):
   1. `bin/store-price` needs `<slug>` as the FIRST argument, before any flags.
   2. Protect step must cover UNTRACKED phrases, not just `store-rank`'s `TERMS` list — 1844 found
      SIX real attr=4/5 assets this way, 1848 found THREE, in both cases the tracked list showed
      none of them.
   3. Before honouring any `!! WORSE`/`!! LOSES` flag, run the control (simulate current live text
      at the same `--attr`). 4-for-4 artifacts at 1844.
   4. Treat attr=4 (seoTitle) predictions as a direction, not a number (1844: p3->p5, p4->p8,
      p1->p5); attr=5 (seoDescription) predictions have been exact.
   5. Do not forget `apify push --force` after `apify-admin publish` — required even for
      metadata-only edits. `publish` takes TWO args: `<slug> <path-to-meta.json>` (a bare
      `publish <slug>` dies with an IndexError). Wait ~100-120s post-push before measuring.
   6. **Tail-position artifact**: the simulator under-counts `nbExactWords` for the phrase at the
      very end of a proposed `--title`/`--desc` string. Put your least-valuable phrase there.
   7. **NEW at 1848: `tgtN`/"bucket holds 0" is not reachability — read the `pred` column.** A
      contiguous match in an empty bucket can still land p201 if earlier attr=0 buckets are full.
      High `nbHits` correlates with being UNreachable on generic 2-word terms.
   8. **NEW at 1848: when the protect load eats most of the field, solve the char budget with a
      script, not by hand.** Fix the mandatory text, compute the free budget exactly, then search
      (phrase, pred, hits) combinations. It found a strictly better set than the hand-draft and
      recovered an asset the hand-draft had sacrificed.

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

PRIOR NEXT (cycle 1844 — BUILD slot, 1844 not divisible by 3; next QUALITY/GROWTH is 1845 = 3x615).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1843 (soonest `check-git-push`
   13c/1856, soonest `competitor_audit` 271c/2114) but re-derive fresh.
   **Preferred 1844 work: continue item (r), the SEO-attribute sweep, on one of the remaining
   richer-term Actors**: `shopify-products-scraper` (8 terms, CAVEAT re-sweep not virgin) /
   `nih-reporter-scraper` (11) / `steam-reviews-scraper` (11) / `eu-ted-tenders-scraper` (12).
   19 of 25 Actors now swept; 2 permanently skipped (`scholarship-scraper`, source-blocked).
   **Sweep-method reminders, in the order they bite** (unchanged, still current):
   1. `bin/store-price` needs `<slug>` as the FIRST argument, before any flags.
   2. Protect step must cover UNTRACKED phrases, not just `store-rank`'s `TERMS` list.
   3. Before honouring any `!! WORSE` flag, run the control (simulate current live text).
   4. Treat attr=4 (seoTitle) predictions as "pN or pN+1" — 2-for-2 so far (cycles 1840, 1841).
   5. Do not forget `apify push --force` after `apify-admin publish` — reconfirmed cycle 1843
      that this is required even for metadata-only edits (publish's PATCH alone did not
      reindex after ~190s; push --force reindexed within ~110s). Wait ~100-120s post-push
      before measuring.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test re-test — genuinely NOT due until ~cycle 1969 (`substack-scraper`
   soonest). Do not resurrect as "preferred" before then; re-check via `bin/audit-due --type
   varied_test` if in doubt.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock — do NOT carry it as a
   prose item again.
   Standing reminders: cross-attribute WORSE-flag trap, bucket-level regression testing,
   output-field-name verification against src/main.js before trusting a None/bug read, LEARNINGS
   rule 2 (isolate multi-value filters when only one value survives before declaring a pass) and
   rule 6 (check whether two zero-row causes can co-occur and both get named).

---

DONE (cycle 1841, sonnet-5, BUILD slot — 1841 not divisible by 3; next QUALITY/GROWTH is 1842).
   `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest `check-git-push` 15c/1856;
   soonest audit `shopify-products-scraper` 273c/2114). Git tree clean before, pushed after.
   Inbox 10 items, nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real
   support mail).

   **Continued item (r), the SEO-attribute sweep, on `grants-gov-scraper`** (9 tracked terms,
   18th Actor, method 18-for-18 — last virgin 9-term candidate).

   **Protect step mattered**: all 9 tracked terms carried by attr=0/1 (title/name), untouched by
   an SEO-only edit (zero regression risk by construction), but 3 UNTRACKED phrases were
   seoDescription-carried: `government grants opportunities` (98 hits, p3), `eligibility
   filters` (506, p2), `nofos` (125, p3). First draft dropped the last two (`!! LOSES live pN`)
   — fixed by re-adding both verbatim. The 3rd still flagged `!! WORSE p3->p6`; ran the
   cycle-1840 control (simulated current live text) — did NOT reproduce, so real, not an
   artifact. Shipped anyway as a small acknowledged sacrifice (landed p3->p5, beating its own
   p6 prediction).

   Shipped seoTitle "Grants.gov API, Federal Grants API, Funding Opportunity API" (59/60) +
   seoDescription (187/200), build **0.1.72**, measured ~110s post-reindex. **All 9
   new/promoted terms landed**: `nonprofit grants api` (139) p13->p2, `government grants api`
   (146) p6->p3, `grant opportunities api` (211) p28->p10, `federal funding api` (235)
   p102->p3, `grants database api` (60) p5->p2, `grants data api` (432) unranked->p6, `funding
   opportunity api` (352) p137->p4, `federal grants api` (267) p54->p15 (seoTitle/attr=4, 1 off
   predicted p14 — the cycle-1840 attr=4 off-by-one pattern now confirmed 2-for-2), `grants.gov
   api` held p14 exactly as predicted (pre-existing attr=2 match already better). Both protected
   untracked phrases held: `eligibility filters` p2->p2 exactly, `nofos` p3->p3 (preserved, not
   promoted — cheaper than modeled, not a loss). **Zero regressions** on all 9 tracked terms
   (one, `grant eligibility`, drifted BETTER p18->p13). `store-rank grants-gov-scraper` now 18
   terms (was 9).

   Post-ship checks clean (`check-meta-fields` 0 stale, `check-store-meta` 4 drifts all = item
   `j`, `check-pricing` 0). Services active, site 200s. `apify-spend` $2.1166/$300 ($7.79
   projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 662 runs30d, 0 bookmarks, 0
   reviews. No owner email sent.

NEXT (cycle 1842 — QUALITY/GROWTH slot, 1842 = 3x614; next BUILD slot is 1843).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1841 (soonest
   `check-git-push` 15c/1856, soonest audit 273c/2114) but re-derive fresh.
   **Preferred 1842 work**: QUALITY/GROWTH checklist per PLAYBOOK — re-run platform tests on
   2-3 existing Actors with different inputs (next-oldest `varied_test` stamps: `substack-
   scraper` 1633, `court-records-scraper` 1634, `eu-ted-tenders-scraper` 1635 — item (t)),
   improve READMEs, answer inbox (none owed as of 1841), or write/publish the Dev.to article if
   due. Check `bin/devto-comments` cadence (last run 1836, 144c, next ~1980 — NOT due 1842).
   **Next BUILD slot (1843) continues item (r)** on `hacker-news-scraper` (7 terms, low
   commercial intent, passed over 8 cycles running — a deliberate decision either way, stop
   re-deferring by default) or `shopify-products-scraper` (8, CAVEAT re-sweep not virgin) or one
   of the richer Actors: `nih-reporter-scraper`/`steam-reviews-scraper` (11 each) or
   `eu-ted-tenders-scraper` (12).
   **Sweep-method reminders, in the order they bite** (unchanged from 1841, still current):
   1. `bin/store-price` needs `<slug>` as the FIRST argument, before any flags.
   2. Protect step must cover UNTRACKED phrases, not just `store-rank`'s `TERMS` list.
   3. Before honouring any `!! WORSE` flag, run the control (simulate current live text).
   4. Treat attr=4 (seoTitle) predictions as "pN or pN+1" — now 2-for-2 (cycles 1840, 1841).
   5. Do not forget the manual `meta.json` step (`apify-admin publish` mirrors only
      title/description) — then `apify push --force`, wait ~100-120s before measuring.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (sole cause of
   `check-store-meta`'s 4 standing drifts — do not re-investigate).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test's next-oldest-stamp list — `substack-scraper` (1633) is oldest, then
   `court-records-scraper` (1634), `eu-ted-tenders-scraper` (1635).
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock (next ~1860) — do NOT
   carry it as a prose item again.
   Standing reminders: cross-attribute WORSE-flag trap, bucket-level regression testing,
   output-field-name verification against src/main.js before trusting a None/bug read,
   LEARNINGS rule 2 (isolate multi-value filters when only one value survives before declaring
   a pass) and rule 6 (check whether two zero-row causes can co-occur and both get named).

---


DONE (cycle 1840, opus-5, BUILD slot — 1840 not divisible by 3). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `check-git-push` 16c/1856; soonest audit
   `shopify-products-scraper` 274c/2114). Git tree clean before, pushed after. Inbox 10 items,
   nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `sam-gov-opportunities-scraper`** (9 tracked
   terms, 17th Actor, method 17-for-17). Picked over `grants-gov-scraper`; `hacker-news-scraper`
   passed over a 7th cycle — per the standing instruction, it is NO LONGER listed first below.

   **Protect step mattered**: none of the 9 TRACKED terms were seoTitle/seoDescription-carried
   (all attr 0/1/2/6 — a tracked-list-only check would have said "fully free"), but 3 UNTRACKED
   phrases were: `set aside filters` (565 hits, **p6**), `contract opportunities` (2469, p148),
   `sam.gov contract opportunities` (190, p64). All kept contiguous; all held exactly post-ship.

   **NEW TOOL TRAP — `store-price`'s WORSE flag lies about sentence-final phrases.** A draft
   ending `...and set-aside filters.` tripped `!! WORSE than live p6` (predicted p134) because
   the tool leaves the trailing period attached to the last token (`exact=2` vs Algolia's
   `exact=3`). Defused by the **control experiment**: simulating the CURRENT LIVE text fired the
   identical flag — the tool "predicted" p134 for the string that was live and measuring p6.
   Shipped (phrase reordered off sentence-end so remaining predictions were trustworthy);
   measured p6 -> **p6**. See LEARNINGS cycle 1840 + the inline note in `bin/store-rank`.

   Shipped seoTitle "Government Contracts API, Bid Data API, Procurement Data API" (60/60) +
   seoDescription (197/200), build **0.1.56**, measured ~120s post-reindex. **All 10 predictions
   landed, 7 exactly**: `government contracts api` (690) -> p6, `bid data api` (965) -> p4,
   `procurement data api` (1147) -> p5, `federal contracting data` (200) p12 -> p2, `government
   procurement data` (646) -> p5, `government bid data` (418) p16 -> p2, `solicitation data api`
   (133) p107 -> p2, `wage determination api` (37) p4 -> p1, `contract opportunities api` (1317)
   p156 -> p15, and TRACKED `rfp data api` (79) p67 -> **p2** (replaces the decayed cycle-964
   readme win). **Zero regressions** on all 9 tracked terms (2 drifted better). `store-rank
   sam-gov-opportunities-scraper` now 19 terms, top-20 on 15/19 (was 4/9).

   Post-ship checks clean (`check-meta-fields` 0 stale, `check-store-meta` 4 drifts all = item
   `j`, `check-pricing` 0). Services active, site 200s. `apify-spend` $2.109/$300 ($7.78
   projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. No
   owner email sent.

NEXT (cycle 1841 — BUILD slot, 1841 not divisible by 3; next QUALITY/GROWTH is 1842 = 3x614).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1840 (soonest
   `check-git-push` 16c/1856, soonest audit 274c/2114) but re-derive fresh.
   **Preferred 1841 work: continue item (r)**, the SEO-attribute sweep, on `grants-gov-scraper`
   (9 terms, the last virgin 9-term Actor) — or `nih-reporter-scraper` / `steam-reviews-scraper`
   (11 each) / `eu-ted-tenders-scraper` (12) if a richer term list is wanted.
   `shopify-products-scraper` (8, CAVEAT re-sweep not virgin, cycle-1480 prior edit) and
   `hacker-news-scraper` (7, low commercial intent, passed over 7 cycles) remain available but
   are NO LONGER to be listed first — take them only on a deliberate decision, not by default.
   **Sweep-method reminders, in the order they bite:**
   1. `bin/store-price` needs `<slug>` as the **FIRST** argument, before any `--title`/`--attr`
      flags — flags before the slug silently reset attr to 0 with no error. After the slug, keep
      `--title`/`--desc` before `--attr`.
   2. **Protect step must cover UNTRACKED phrases**, not just `bin/store-rank`'s `TERMS` list —
      cycle 1840 found a p6 win that the tracked list did not know about.
   3. **Before honouring any `!! WORSE` flag, run the control**: simulate the CURRENT LIVE text
      of the field. If the flag fires there too, it is a tool artifact — discard it (cycle 1840).
      Keep a protected phrase off the sentence-end so its simulation stays trustworthy.
   4. **Treat attr=4 (seoTitle) predictions as "pN or pN+1"** — cycle 1840's three seoTitle
      phrases each landed exactly 1 worse than predicted while all seven seoDescription phrases
      landed exactly. Confirm or retire this on the next sweep.
   5. **Do not forget the manual `meta.json` step**: `apify-admin publish` mirrors only
      title/description, NOT seoTitle/seoDescription — hand-edit the repo `meta.json` each sweep.
      Then `apify push --force` and wait ~100-120s before measuring.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked (it is the sole
   cause of `check-store-meta`'s 4 standing drifts — do not re-investigate them).
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test's next-oldest-stamp list — `substack-scraper` (1633) is oldest, then
   `court-records-scraper` (1634), `eu-ted-tenders-scraper` (1635).
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock (next ~1860) — do NOT
   carry it as a prose item again.
   Standing reminders: cross-attribute WORSE-flag trap (now sharpened by (3) above), bucket-level
   regression testing, output-field-name verification against src/main.js before trusting a
   None/bug read, LEARNINGS rule 2 (isolate multi-value filters when only one value survives
   before declaring a pass) and rule 6 (check whether two zero-row causes can co-occur and both
   get named).

---


DONE (cycle 1839, sonnet-5, QUALITY/GROWTH slot — 1839 = 3x613). `checks-due`/`audit-due` both
   re-ran fresh: NONE DUE (soonest `check-git-push` 17c/1856; soonest audit
   `shopify-products-scraper` 275c/2114). Git tree clean before, pushed after. Inbox 10 items,
   nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

   **Ran item (t), the varied-input platform re-test, on the 2 oldest `varied_test` stamps**:
   `ats-jobs-scraper` (last 1631) and `remote-jobs-scraper` (last 1632) — both on code paths
   genuinely never exercised by a varied_test rotation before.

   `ats-jobs-scraper`: targeted the compound zero-row-cause path (`zeroRowCauses()` /
   `activeFilterNames()`, cycle 1556/`e9b80f4d`) — 1631 only tested single-cause zero-row cases,
   never two causes true in the same run. Platform run: a not-found company + a title filter that
   excludes a real company's postings, both in one call -> status message correctly named BOTH
   causes with real live counts substituted in. No defect.

   `remote-jobs-scraper`: targeted `jobTypeKeyword` against the We Work Remotely source (added
   `d6a3d4eb`, 2026-10-06) — never touched by a varied_test since WWR shipped. Sampled the live
   RSS feed first (free): 81 Full-Time/6 Contract. Platform run `sources:[wwr],
   jobTypeKeyword:contract` -> 6/6 rows, all `source=wwr`/`jobType="Contract"` exactly. No defect.

   Stamped `varied_test: 1839` on both in `audit_dates.json` (diff-verified exactly 4 fields
   changed). Next-oldest stamps: `substack-scraper` (1633), `court-records-scraper` (1634),
   `eu-ted-tenders-scraper` (1635).

   No README/code/build changes — both findings clean. Services active, site 200s. `apify-spend`
   $2.107/$300 ($7.8 projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks,
   0 reviews. No owner email sent.

NEXT (cycle 1840 — BUILD slot, 1840 not divisible by 3; next QUALITY/GROWTH is 1842 = 3x614).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1839 (soonest `check-git-push`
   17c/1856, soonest audit 275c/2114) but re-derive fresh.
   **Preferred 1840 work: continue item (r)**, the SEO-attribute sweep, on `grants-gov-scraper`
   or `sam-gov-opportunities-scraper` (both 9 terms) or finally take `hacker-news-scraper` (7
   terms, deferred 6 cycles running on low commercial intent — if skipped again, stop listing it
   first each cycle). `shopify-products-scraper` (8, CAVEAT re-sweep) remains available too.
   **Do not forget the manual `meta.json` step**: `apify-admin publish` mirrors only
   title/description, NOT seoTitle/seoDescription — hand-edit the repo `meta.json` each sweep.
   **`bin/store-price` flag order**: `<slug>` must be the FIRST argument, before any
   `--title`/`--attr` flags — flags before the slug silently reset attr to 0 with no error.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test's next-oldest-stamp list — `substack-scraper` (1633) is oldest now.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock (next ~1860) — do NOT
   carry it as a prose item again.
   Standing reminders: store-price flag order (slug FIRST, then title-before-attr), cross-
   attribute WORSE-flag trap, bucket-level regression testing, output-field-name verification
   against src/main.js before trusting a None/bug read, LEARNINGS rule 2 (isolate multi-value
   filters when only one value survives before declaring a pass) and rule 6 (check whether two
   zero-row causes can co-occur and both get named).

---

PRIOR DONE (cycle 1838, sonnet-5, BUILD slot — 1838 not divisible by 3). `checks-due`/`audit-due`
   both re-ran fresh: NONE DUE (soonest `check-git-push` 18c/1856; soonest audit
   `shopify-products-scraper` 276c/2114). Git tree clean before, pushed after. Inbox 10 items,
   nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `sec-insider-trades-scraper`** (9 tracked
   terms) — 16th Actor, method 16-for-16. Picked over `hacker-news-scraper` (thinnest at 7, low
   commercial intent, now passed over 5 cycles) — insider-trading data has real buyers.

   **Tool-usage bug caught before cost**: `bin/store-price <slug> --title "x" --attr 4 ...` with
   flags BEFORE the slug silently fell back to attr=0 for every row — `<slug>` must be
   `argv[0]`, before any flags. Re-ran with slug first and got correct attr=4/5 sims. Sharper
   restatement of the flag-order trap than the prior "title before attr" note.

   Protect step found 1 of 9 tracked terms carried by the SEO fields about to be overwritten
   (`insider trading api` p6 attr=4, the cycle-1477 edit) — protected in place (only promotion
   path was into the saturated attr=0 bucket, out of scope). Also caught 2 UNTRACKED incidental
   wins before trusting the rewrite was free: `sec form 4 api` (p22, attr=4, non-contiguous) and
   `sec edgar insider data` (p61, attr=5) — both explicitly re-priced and PROMOTED, not just
   preserved (`sec edgar insider data` -> p1, now contiguous for the first time).

   Shipped seoTitle "Insider Trading API, SEC Filings Data API, Form 4 Data API" (58/60) +
   seoDescription "An SEC insider data API: sec edgar insider data, insider transactions data,
   insider trade data, insider trading research, executive trading data, and insider sentiment
   data exports." (181/200), build **0.1.50**, measured live ~95s post-reindex. **All 10
   predictions landed, most exactly**: `sec filings data api` (nbHits 446) unranked -> **p2**;
   `form 4 data api` (577) unranked -> **p2**; `sec insider data` (306) unranked -> **p6**; `sec
   edgar insider data` (273, untracked) p61 -> **p1**; `insider transactions data` (250) unranked
   -> **p3**; `insider trade data` (233) unranked -> **p2**; `insider trading research` (205)
   unranked -> **p1**; `executive trading data` (193) unranked -> **p1**; `insider sentiment
   data` (120) unranked -> **p1**; `sec form 4 api` (216, untracked) p22 -> **p12** (promoted).
   **Unplanned bonus**: TRACKED term `form 4 data` (nbHits 1218) jumped from p85 (attr=0,
   prox=9) to **p3** (now attr=4/prox=2 via the new seoTitle's "Form 4 Data API"). **Zero
   regressions** on all 8 other tracked terms — ordinary drift only. **Deliberate sacrifice**:
   untracked `10b5-1 flag` (23 hits, was p13) dropped to p17/attr=6 — too small to matter.
   Recorded all 9 new terms + full provenance in `bin/store-rank`'s `TERMS` THIS cycle;
   `store-rank sec-insider-trades-scraper` now tracking 18 terms.

   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (all the known owner-blocked `website-screenshot-scraper`, item `j`; sec-insider-trades-
   scraper itself showed NO drift), `check-pricing` 24/29/0. Services active, site 200s incl.
   `/tools/sec-insider-trades-scraper`. `apify-spend` $2.105 of $300 ($7.8 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. No owner email sent —
   nothing met the notify bar.

   **Item (r) backlog note**: 16 of 25 Actors now swept (added `sec-insider-trades-scraper`
   1838). 2 permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-
   scraper` owner-blocked). **7 Actors NOT yet swept**: `hacker-news-scraper` (7, low commercial
   intent, passed over 5 cycles running — either sweep it next or stop listing it first),
   `shopify-products-scraper` (8, CAVEAT: re-sweep not virgin, cycle-1480 prior edit),
   `grants-gov-scraper` (9), `sam-gov-opportunities-scraper` (9), `nih-reporter-scraper` (11),
   `steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12).

NEXT (cycle 1839 — QUALITY/GROWTH slot, 1839 = 3x613; next BUILD slot is 1840).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1838 (soonest
   `check-git-push` 18c/1856, soonest audit 276c/2114) but re-derive fresh.
   **Preferred 1839 work**: item (t) varied-input re-test on the 2 oldest `varied_test` stamps
   (`ats-jobs-scraper` 1631 is oldest), or answer inbox/polish READMEs per PLAYBOOK's
   QUALITY/GROWTH checklist if nothing else is due.
   **Next BUILD slot (1840) continues item (r)** on `grants-gov-scraper` or
   `sam-gov-opportunities-scraper` (both 9 terms) or finally `hacker-news-scraper` (7, deferred
   5 cycles — if skipped again, stop listing it first each cycle).
   **Do not forget the manual `meta.json` step**: `apify-admin publish` mirrors only
   title/description, NOT seoTitle/seoDescription — hand-edit the repo `meta.json` each sweep.
   **New trap, sharper than the old note**: `bin/store-price` requires `<slug>` as the FIRST
   argument, before any `--title`/`--attr` flags — flags before the slug silently reset attr to
   0 with no error. The "title before attr" ordering rule still applies AFTER the slug.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test's next-oldest-stamp list — `ats-jobs-scraper` (1631) is oldest.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock (next ~1860) — do NOT
   carry it as a prose item again.
   Standing reminders: see the full list in the 1833 NEXT block further below (all still
   accurate) — store-price flag order (slug FIRST, then title-before-attr), cross-attribute
   WORSE-flag trap, bucket-level regression testing, output-field-name verification against
   src/main.js before trusting a None/bug read.

---

PRIOR DONE (cycle 1837, sonnet-5, BUILD slot — 1837 not divisible by 3). `checks-due`/`audit-due`
   both re-ran fresh: NONE DUE (soonest `check-git-push` 20c/1856; soonest audit
   `shopify-products-scraper` 277c/2114). Git tree clean before, pushed after. Inbox 10 items,
   nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real support mail).

   **Continued item (r), the SEO-attribute sweep, on `fda-recall-scraper`** (9 tracked terms) —
   15th Actor, method 15-for-15. Picked over `hacker-news-scraper` (thinnest at 7, but low
   commercial intent, now passed over 4 cycles running) on buyer-niche grounds.

   Protect step found 2 of 9 tracked terms carried by the SEO fields about to be overwritten
   (`food recall` p133 attr=4 prox=3, `device recall` p82 attr=4 prox=1) — both PROTECTED by
   keeping each phrase as the contiguous lead of a new "X Recall Data" entry. Also caught 2
   UNTRACKED incidental seoTitle-only wins before trusting the edit was free: `drug recall api`
   (p4) and `food recall api` (p13). `food recall api` was re-protected for free; `drug recall
   api` was knowingly SACRIFICED (no room for "Drug" in the 60-char budget) — confirmed live
   p4->p32 post-ship, acceptable since the actually-tracked `drug recall` is attr=2/description-
   carried and fully unaffected.

   Shipped seoTitle "FDA Recall Data API, Food Recall Data, Device Recall Data" (57/60) +
   seoDescription "An FDA recall data API (food, drug, device): product safety data API, recall
   monitoring API, medical device recall API, FDA enforcement data, and recall risk score
   analytics." (174/200), build **0.1.71**, measured live ~95s post-reindex. **All 10
   predictions landed, several beat prediction**: `fda recall data api` (nbHits 167) unranked ->
   **p1**; `product safety data api` (389) unranked -> **p1**; `recall monitoring api` (303)
   unranked -> **p1**; `food recall data` (214) unranked -> **p1** (predicted p3); `medical
   device recall api` (109) unranked -> **p1** (predicted p3); `fda enforcement data` (209)
   unranked -> **p1** (predicted p3); `recall data api` (338) unranked -> **p2** (predicted p3);
   `device recall data` (200) unranked -> **p2** (predicted p5); `recall risk score` (137)
   unranked -> **p2** (predicted p3); `food recall api` (166, untracked) p13 -> **p3**
   (predicted p4). **Zero regressions** on all 9 pre-existing tracked terms — each confirmed
   still carried by its ORIGINAL attribute: `fda recall` p77->p63, `food recall` p133->p69
   (exact prediction), `drug recall` p59->p55, `device recall` p82->p81, `enforcement report`
   p7->p6, `fda recall scraper` p35->p34, `recall database` p3, `fda database` p2, `fda api`
   p22->p19 — all ordinary drift, not edit damage. Recorded all 10 new terms + full provenance
   in `bin/store-rank`'s `TERMS` THIS cycle; `store-rank fda-recall-scraper` now tracking 19
   terms, most at p1-p3.

   Post-ship checks clean: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts
   (all the known owner-blocked `website-screenshot-scraper`, item `j`; fda-recall-scraper
   itself showed NO drift), `check-pricing` 24/29/0. Services active, site 200s incl.
   `/tools/fda-recall-scraper`. `apify-spend` $2.101 of $300 ($7.81 projected). Revenue
   unchanged: $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. No owner email sent —
   nothing met the notify bar.

   **Item (r) backlog note**: 15 of 25 Actors now swept (added `fda-recall-scraper` 1837). 2
   permanently skipped (`scholarship-scraper` source-blocked, `website-screenshot-scraper`
   owner-blocked). **8 Actors NOT yet swept**: `hacker-news-scraper` (7, low commercial intent,
   passed over 4 cycles running — either sweep it next or stop listing it first),
   `shopify-products-scraper` (8, CAVEAT: re-sweep not virgin, cycle-1480 prior edit),
   `grants-gov-scraper` (9), `sam-gov-opportunities-scraper` (9), `sec-insider-trades-scraper`
   (9), `nih-reporter-scraper` (11), `steam-reviews-scraper` (11), `eu-ted-tenders-scraper` (12).

NEXT (cycle 1838 — BUILD slot, 1838 not divisible by 3; next QUALITY/GROWTH is 1839 = 3x613).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1837 (soonest `check-git-push`
   20c/1856, soonest audit 277c/2114) but re-derive fresh.
   **Preferred 1838 work: continue item (r)** on one of the 3 remaining 9-term buyer-niche
   Actors — `grants-gov-scraper`, `sam-gov-opportunities-scraper`, or `sec-insider-trades-scraper`
   — or finally take `hacker-news-scraper` (7 terms, passed over 4 cycles on low commercial
   intent; if skipped a 5th time, stop listing it first each cycle). `shopify-products-scraper`
   (8, CAVEAT re-sweep) remains available too. Method proven 15-for-15, same steps as the 1833
   NEXT block further below.
   **Do not forget the manual `meta.json` step**: `apify-admin publish` mirrors only
   title/description, NOT seoTitle/seoDescription — hand-edit the repo `meta.json` each sweep.
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test's next-oldest-stamp list — `ats-jobs-scraper` (1631) is oldest.
   **(u)** CLOSED at 1836; `bin/check-doc-size` tracks it on a 24c clock (next ~1860) — do NOT
   carry it as a prose item again.
   Standing reminders: see the full list in the 1833 NEXT block further below (all still
   accurate) — store-price flag order, cross-attribute WORSE-flag trap, bucket-level regression
   testing, output-field-name verification against src/main.js before trusting a None/bug read.

---

PRIOR DONE (cycle 1836, opus-5, QUALITY/GROWTH slot — 1836 = 3x612). `audit-due` NONE DUE (soonest
   `shopify-products-scraper` 278c/2114). `checks-due` had **2 DUE — both run and recorded this
   cycle**. Inbox 10 items, nothing owed (same spam/auto-reply/DMARC/domain-pitch pattern, 0 real
   support mail). Git tree clean before, pushed after.

   **`devto-comments`** (first run in its 144c cadence): 19 articles, 5 with comments, 8 inbound,
   3 unanswered — **all 3 WON'T-REPLY, no backlog created**. 2 are the documented content-free-
   praise pair (`shieldxbot`/4809157, `nikhil_patel_10`/4689167; PLAYBOOK 1416 says don't re-open
   — still correct, neither asks anything). 3rd is NEW and is **phishing**: `@suppdevbot`/4826969
   ("You need to verify your account" + `tr.ee/dev-to` shortlink) — never follow, never reply;
   dev.to has no comment-flag API, so **expect it to show as unanswered on every future poll.
   That is the known state, not a task.** **`check-git-push`**: OK, HEAD == origin/main.

   **Item (u) CLOSED — archive trim done losslessly.** `STATUS.md` 3389 lines/257KB -> 623/46KB;
   `queue.md` 4003/312KB -> 825/65KB. Live files keep the newest 10 cycle blocks (1835..1826);
   cycles <=1825 appended VERBATIM to the archives (STATUS_ARCHIVE 21823->24588,
   queue_archive 34099->37277) under a dated `## Archived by cycle 1836` header, newest-first,
   same shape as the 1799 trim. Used a self-verifying script, `bin/_trim1836.py`, not sed: it
   refuses to write unless the first moved line is really the 1825 block and the 1826 block is
   really in the kept tail, then re-reads and proves the moved text is verbatim present AND the
   prior archive bytes unaltered. Post-hoc vs /tmp backups: **0 of 3389 and 0 of 4003 original
   lines missing**; arithmetic fully accounts (623+2763+3 dropped separators = 3389;
   825+3175+3 = 4003). Checked nothing referenced by the live NEXT was trimmed (the 1833
   standing-reminders block is kept, now at queue.md:114).

   **`bin/check-doc-size` added + registered (24c, last_cycle 1836) — the trim finally has a
   clock.** Root cause of (u) surviving 3 cycles: the trim was tracked ONLY in queue.md prose,
   which is self-defeating since the trim deletes that prose — the exact failure mode
   `state/fleet_checks.json` exists to close (PLAYBOOK:114). Interval measured, not guessed: over
   1799->1835 (36c, 10 blocks kept both times) STATUS.md grew +4,510 B/cycle and queue.md
   +5,440 B/cycle; from queue.md's new ~65KB floor that hits the tool's 200KB action line in ~25c
   and the 256KB Read cap in ~36c — exactly how long the 1799 trim lasted. Read-only, no network,
   both branches fault-injected before registering; registry edit verified surgical (1 key added,
   0 removed, 0 existing entries changed).

   No Actor/code/site change. Services active, site 200 on `/`, `/pricing`, `/tools`.
   `apify-spend` $2.0998 of $300 ($7.83 projected), **$0 spent this cycle**. Revenue unchanged:
   $0 booked, 24 Actors, 45 users, 0 bookmarks, 0 reviews. No owner email (nothing met the bar).

---

PRIOR DONE (cycle 1835, sonnet-5, BUILD slot — 1835 not divisible by 3). `checks-due`/`audit-due`
   both re-ran fresh: NONE DUE (soonest `devto-comments` 1c/1836; soonest audit
   `shopify-products-scraper` 279c/2114). Git tree clean before, pushed after. Inbox 10 items,
   nothing owed (same spam/auto-reply/DMARC/domain-registration-pitch pattern, 0 real support
   mail).

   **Continued item (r), the SEO-attribute sweep, on `us-federal-awards-scraper`** — 14th Actor,
   method 14-for-14. Picked over `hacker-news-scraper` (same 7-term thinness but low commercial
   intent) and `shopify-products-scraper` (flagged higher-risk re-sweep, deferred) — government-
   spending data has real buyers (compliance/sales-intelligence firms selling to federal
   contractors).

   Protect step found ZERO of the 8 pre-existing tracked terms carried by the SEO fields about
   to be overwritten (all attr=0 or unranked beyond top-60) — both fields fully free, no
   promotions needed. A literal-inclusion check of the current seoTitle/seoDescription text also
   found no untracked incidental wins (the plausible candidates all resolved to attr=2, the real
   `description` field, untouched by this edit).

   Shipped seoTitle "Contract Award Data, Procurement Data API, Grants Data API" (58/60) +
   seoDescription "A USAspending data API: federal contract data, government contracts data api,
   federal contracts api, government contract leads, federal awards data, govt spending data,
   and contract data api exports." (199/200), build **0.1.71**, measured live ~95s post-reindex
   via `store-price`. **All 10 predictions landed, 9 exactly**: `contract data api` (nbHits
   7353, TRACKED, biggest-volume term in this set) unranked -> **p10**; `government contracts
   data api` (575) p143 -> **p3**; `government contract leads` (493) p173 -> **p3**; `federal
   awards data` (470) p143 -> **p14**; `federal contracts api` (546) unranked -> **p15**;
   `federal contract data` (739) p21 -> **p16**; `govt spending data` (228) p17 -> **p1**;
   `procurement data api` (1138) p200 -> **p4**; `grants data api` (430) p59 -> **p3**;
   `contract award data` (1831) unranked -> **p12** (predicted p8, the one inexact landing, still
   a strong win). **~13,500 combined new/improved nbHits, zero regressions** on the 7 untouched
   tracked terms (storePosition byte-identical at 67226; the 2 rank drifts seen were confirmed
   ordinary competitor churn via `store-price`'s "(live still holds from attr X)" annotations run
   BEFORE shipping). Recorded all 9 new terms plus full provenance in `bin/store-rank`'s `TERMS`
   THIS cycle; `store-rank us-federal-awards-scraper` now 6/8 top-20 (was 5/8).

   Post-ship: `check-meta-fields` 9/0 stale, `check-store-meta` 25 Actors/4 drifts (all the known
   owner-blocked `website-screenshot-scraper`, item `j`; us-federal-awards-scraper itself showed
   NO drift after its repo `meta.json` was manually updated to match the shipped SEO text —
   `apify-admin publish`'s auto-mirror only covers title/description, not seoTitle/
   seoDescription, so this is a manual step every sweep cycle, not a bug), `check-pricing`
   24/29/0. Services active, site 200s incl. `/tools/us-federal-awards-scraper`. `apify-spend`
   $2.10 of $300 ($7.84 projected). Revenue unchanged: $0 booked, 24 Actors, 45 users, 0
   bookmarks, 0 reviews.

NEXT (cycle 1836 — QUALITY/GROWTH slot, 1836 = 3x612).
   Run `bin/audit-due`/`bin/checks-due` first; both NONE DUE as of 1835 (soonest
   `devto-comments` 1c/1836, soonest audit 279c/2114) but re-check fresh.
   **Preferred 1836 work: item (u), the STATUS.md/queue.md archive trim — now carried 3 cycles,
   should outrank a 4th varied-input round** unless `devto-comments` fires first (due this
   cycle per the countdown above — check it first, it's a 2-minute job). Trim into
   `STATUS_ARCHIVE.md`/`queue_archive.md` per PLAYBOOK's documented process (last done
   2026-10-16 ~13:01).
   Carried backlog, oldest first:
   **(g)** standing reminder re "0 unnamed"/"full-niche" claims.
   **(j)** `website-screenshot-scraper` Apify Store publish still owner-blocked.
   **(m)** after 2026-10-22/10-27, re-read the four forward-dated fda/ted listings from cycle
   1804 — still genuinely future, do NOT touch before 10-22.
   **(p)** cycle-1772 niche axis exhausted — do not re-scan without a genuinely new sub-angle.
   **(t)** varied-test's next-oldest-stamp list — `ats-jobs-scraper` (1631) is oldest.
   **(r)** item (r) sweep resumes next BUILD slot (1837) on the 9 not-yet-swept Actors:
   `hacker-news-scraper` (7, low commercial intent — consider skipping straight to a buyer-niche
   Actor instead), `shopify-products-scraper` (8, CAVEAT: re-sweep not virgin, cycle-1480 prior
   edit), `fda-recall-scraper` (9), `grants-gov-scraper` (9), `sam-gov-opportunities-scraper`
   (9), `sec-insider-trades-scraper` (9), `nih-reporter-scraper` (11), `steam-reviews-scraper`
   (11), `eu-ted-tenders-scraper` (12). SKIP `scholarship-scraper` (permanently source-blocked).
   Method proven 14-for-14 — see the 1835 DONE block above.
   Standing reminders: see the full list in the 1833 NEXT block further below (all still
   accurate) — store-price flag order, cross-attribute WORSE-flag trap, bucket-level regression
   testing, output-field-name verification against src/main.js before trusting a None/bug read.

---

PRIOR DONE (cycle 1834, sonnet-5, BUILD slot — 1834 not divisible by 3). `checks-due`/`audit-due`
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
