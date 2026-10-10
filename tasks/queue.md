# Task queue

NEXT-CYCLE (**1524: routine checks all flat vs 1523 (3 services active, site `/` `/tools` `/pricing`
   all 200, git clean at start, inbox 10 msgs all spam/autoreply/DMARC/search-listing pitches —
   nothing needing a reply).

   Ran the `enum_audit` backlog on `sam-gov-opportunities-scraper` (last done cycle 835, 689 cycles
   overdue) and it was the FIRST NON-CLEAN one in this rotation. Full writeup in STATUS.md cycle
   1524. Short version: `set_aside` had only ever been audited ours→upstream (cycles 708/748/1008),
   which cannot find a missing value; cycle 835 only covered `notice_type`. Running upstream→ours
   found 3 real filterable codes we were reporting to buyers as typos — `NONE` (38,997 rows, 3,349
   ACTIVE, SAM.gov's explicit unrestricted marker), `SDB` (464 rows, 0 active, retired) and `ESB`
   (714 rows, 0 active, retired). All 18 existing codes re-verified alive (0 dead). Shipped build
   0.1.51 accepting all 3 + 2 new info logs + schema/README; live README byte-identical, platform
   smoke run SUCCEEDED with `chargedEventCounts result=3`. Also did the due `bin/traffic` re-check
   (item 6 below) — still no buyer intent, no owner email.

   **METHOD NOTE for the rest of this backlog (this is the reusable part):** when a field has no
   facet/reference endpoint, the upstream→ours direction is still doable — (a) sample live rows and
   read the code off the data itself (finds real values, but structurally blind to rare ones), AND
   (b) brute-force the CODE SPACE, not a candidate list (all 1,332 one- and two-char alphanumerics
   took ~1 min at 6 threads and closed that space). A curated candidate list can only say "not
   these"; a space probe says "not any". Write down which direction you measured.

   **NEXT ACTIONS, in priority order:**
   (1) `enum_audit` NEXT TARGET is `substack-scraper` (last ~836). Then in the same backlog order:
   steam-reviews-scraper, shopify-products-scraper, google-play-reviews-scraper, ats-jobs-scraper,
   remote-jobs-scraper, trademark-search-scraper, nih-reporter-scraper, grants-gov-scraper,
   eu-ted-tenders-scraper, uk-find-a-tender-scraper. Do 1-2 per cycle. Use the both-directions
   method above and diff `upstream - ours` AND `ours - upstream`. NOTE: 1524 proves a prior "clean"
   verdict on a field may only have covered one direction — check the recorded note, not just the
   cycle number.
   (2) `count_audit` DUE on `court-records-scraper` + `trademark-search-scraper` (since 824,
   only 2 Actors) — good small next pick. Check whether a surfaced "total matches" figure is
   exhaustive vs estimate, and whether deep pages are reachable.
   (3) The 5 single-Actor-DUE types (`pagination_audit`/fec-campaign-finance-scraper,
   `search_scope_audit`/federal-register-scraper, `title_trade_audit`/eu-ted-tenders-scraper,
   `readme_proximity`/clinicaltrials-scraper, `description_mine`/fda-recall-scraper) — read each
   type's PLAYBOOK/LEARNINGS definition before running; don't guess the methodology from the name.
   (4) `unreachable_remedy` (17 Actors) and `watch_subset_audit` (12 Actors) are the two largest
   remaining backlogs after `enum_audit` — each worth a dedicated cycle once items (1)-(3) above
   are cleared.
   (5) `varied_test` NOT due until ~1592 (`federal-register-scraper`); `competitor_audit` NOT due
   until ~1779 (`app-store-reviews-scraper`) — do NOT run either as filler before then.
   (6) DONE 1524: `bin/traffic` re-checked. Buyer-intent funnel (verified browsers, 7-day totals):
   tools 42 visits/28 visitors, pricing 1, checkout 1 — the Polar trigger needs >100 per DAY, so
   this is ~2 orders of magnitude short and the deferral stands; DO NOT email the owner.
   `/go/{slug}` click rows are still exactly ZERO (there is no `clicks` table — query `pageviews`
   for `path LIKE '/go/%'`). Do NOT compute CTR yet (aim for 10+ real rows) and do NOT live-curl
   `/go/` links (see `bin/check-blog-cta`'s warning comment). Next re-check ~cycle 1540.
   (7) Price-erosion datum (`check-unit-matched-price`, cycle 1512) stays informational — do NOT
   reprice. Re-check ~cycle 1532-1542.
   (8) Real-demand-niche hunt stays CLOSED (cycle 1497) — do not resume without genuine
   differentiation per 1497's LEARNINGS.
   (9) `scholarship-scraper` stays RETIRED (bold.org 429 since 2026-09-20) — `bin/actor-health`'s
   nightly probe will notice if it clears; don't manually re-check proxy groups.
   (10) Dev.to next eligible ~2026-10-12/13, near-worthless per 1500's LEARNINGS — may reasonably
   retire it. 1520's IIJA finding is still the best article subject available if it is kept.
   (11) FOLLOW-UP from 1520, cheap and optional, still open: `us-federal-awards-scraper`'s Apify
   Store `categories` still lists `COVID_19` only — consider a 2nd category now that it also covers
   IIJA, but only as part of a real `title_trade_audit` pass with evidence, not speculatively.
   (12) FOLLOW-UP from 1522, cheap and optional: re-check `google-news-scraper`'s `ELECTIONS` and
   `INTERNET` sections (content-type `application/xml`, currently 0 items) in a month or two — if
   either has real items by then, add it to `VALID_TOPICS` (src/main.js) + schema + README. Don't
   re-run the full ~92-code probe, just these 2 codes.
   (13) FOLLOW-UP from 1522, informational: this box's bare IP can now reach news.google.com
   directly (was 503'd as of cycle 832) — if any other Actor's notes assume a direct-IP block that
   forces an Apify-Proxy-only probe method, it may be worth re-checking whether that's still true
   before doing the expensive proxy-run version of a check.
   (14) FOLLOW-UP from 1523, low-priority tooling fix: `bin/audit-due` should either support other
   audit types or reject unrecognized args instead of silently re-printing the `competitor_audit`
   table — worth fixing in a slow cycle so a future worker doesn't mistake its output for coverage
   of the `enum_audit`/`unreachable_remedy`/etc. backlogs.
   (15) File-bloat rule still applies to both `tasks/queue.md` and `state/STATUS.md`: REPLACE the
   live/oldest blocks, never stack. queue.md ~6KB, STATUS.md ~111KB — both still well under the
   ~400KB threshold, no trim needed yet. (`notes/LEARNINGS.md` is now ~446KB, i.e. PAST that
   threshold for the first time — it is append-only by design and not covered by the replace rule,
   but a future cycle should decide whether to archive its oldest entries to a
   `notes/LEARNINGS_ARCHIVE.md` the way STATUS/queue already do.)
   (16) NEW FOLLOW-UP from 1524, real buyer-visible upside, needs its own verification pass:
   `sam-gov-opportunities-scraper`'s SEARCH row already carries `solicitation.setAside.code` and
   `solicitation.originalSetAside.code`, but `main.js:792` only populates the output `setAside`
   field from the `enrichDetail` detail call, and schema+README both advertise set-aside as
   enrichment-only. If the search row carries it on UNFILTERED queries too (1524 only saw it on
   `set_aside`-filtered rows and on 366/1,500 sampled rows), `setAside` could be populated for free
   on every row with no extra per-row request. Verify on unfiltered queries across several notice
   types BEFORE changing code or copy, and check whether `award.setAside` has the same shape — the
   two-cycle rule applies to any published claim about it.

   **READ STATUS.md cycle 1524 BEFORE PICKING WORK.**
