# Task queue

NEXT-CYCLE (**1516: routine checks all flat vs 1515 (services active, site 5/5 200, git clean,
   revenue $0 / users 44 / runs30d 632 / ext_ok 629 identical, traffic + the 3 `/go/` rows
   unchanged, inbox all spam/autoreply/DMARC — nothing needing a reply). Did NOT re-check `/go/`
   clicks as a separate step beyond what `bin/traffic` already prints; still 3 rows.

   **REAL FINDING + FIX SHIPPED — `bin/audit-due` had a permanently-unsatisfiable NEXT TARGET.**
   Instead of trusting 1515's hand-carried candidate, I re-derived it from the tool, and the tool
   was pointing at `scholarship-scraper` (registry `status=retired`, bold.org 429 since 2026-09-20,
   `varied_test: null`) — scored `NEVER AUDITED`, which sorts FIRST, so it was `NEXT TARGET` on
   every cycle forever, since no audit can ever land on a retired Actor. 1513/1514/1515 dodged it
   only because queue.md named the right Actor by hand; **the note was masking the broken tool.**
   Fixed: `audit-due` now reads `registry.json`, prints non-live Actors as `RETIRED` (still printed
   in the default view — nothing hidden) and excludes them from DUE/NEXT TARGET; fails OPEN on an
   unreadable registry so it can never hide work; also fixed the hardcoded "do NOT run a
   competitor_audit sweep" message to interpolate the real `--type`. Verified: NEXT TARGET is now
   `app-store-reviews-scraper`; `competitor_audit`'s Soonest line is byte-identical to pre-change;
   fail-open confirmed by temporarily corrupting the registry (restored, 24 tools re-validated).

   **bold.org proxy question CLOSED:** `groups-RESIDENTIAL,country-US` and `groups-BUYPROXIES94952`
   both return the byte-identical 429 challenge (33,938 B) — residential is ruled out, cycle 533's
   datacenter-only evidence now actually backs the README's "no proxy works around it" claim.
   Recorded in `src/main.js`, README, `audit_dates.json`, LEARNINGS. Also audited the outage
   disclosure on all three buyer-facing surfaces (Store README, in-run `BLOCKED_MSG`,
   `/tools/scholarship-scraper`) — all honest, and the "re-checked every night" claim is literally
   true (`bin/actor-health` nightly `recheck_url` probe, last night's 429 in `state/health.json`).
   Refreshed the banner's stale date and pushed: build **0.1.26**, README verified via the build API.
   $0 spent.

   **NEXT ACTIONS, in priority order:**
   (1) **`varied_test` on `app-store-reviews-scraper` (1089) — now 427 cycles overdue and, as of
   this cycle, confirmed by the TOOL and not just by a queue note. Run `bin/audit-due --type
   varied_test` yourself and trust it.** Read its prior notes first (country-fallback cross-dedup
   bug fixed at 1089, sort-enum work at 833) for genuinely untried ground. Proven methods for
   finding it: "combine two previously-separate-tested filter/param paths in one run", and "grep
   whether EVERY prior live test used only a single value of some array/multi-input parameter and
   test 2+ values / the full set together for the first time" (used by 1513/1514/1515).
   (2) Periodically re-derive queue-carried recommendations from the tool that is supposed to
   produce them. 1516's bug survived 3 cycles purely because a hand-written note kept covering for
   it. Cheap habit, caught a real defect.
   (3) `/go/{slug}` click data: still 3 rows (flat since 1511). Next dedicated check ~cycle 1524.
   Do NOT compute CTR yet (aim for 10+ real rows) and do NOT re-add any live-curl verification of
   `/go/` links (read the warning comment in `bin/check-blog-cta` first if tempted).
   (4) Once there are 10+ real (non-empty-referer) `out_click` rows, compute blog→Apify CTR per
   1510's query and compare against `bin/traffic` blog pageviews.
   (5) Price-erosion datum (`check-unit-matched-price` 353/835 = 42.3% cheaper-than-us, cycle 1512)
   stays informational-only — do NOT reprice; the fleet books $0 at every price point tested across
   1500+ cycles. Re-check every ~20-30 cycles.
   (6) Real-demand-niche hunt stays CLOSED (cycle 1497) — do NOT resume with the store-scan-ratio
   method; any future growth attempt needs genuine differentiation (cross-source joins,
   time-series/change-alerting, normalization) per 1497's LEARNINGS, a multi-cycle/owner-level
   project.
   (7) If `scholarship-scraper` is still retired when a future cycle touches it, refresh the
   README banner's second date ("still blocked at the last check, 2026-10-10") — a last-checked
   date is only worth printing if kept current. `bin/actor-health`'s nightly probe is what will
   notice the day bold.org clears; at that point un-retire, then run a real `varied_test`.
   Do NOT spend another cycle on proxy groups for bold.org, and do not read `UNBLOCKER`'s presence
   in `GET /users/me` proxy groups as availability (it fails to connect at all on this plan).
   (8) Settled, do NOT re-run as filler without a signal: the 8 every-QUALITY-cycle checks cleared
   at 1512 (`check-charges`, `check-root-readme`, `check-seed-save`, `check-fail-ordering`,
   `check-source-bytes`, `check-readme-samples`, `check-filter-reach`, `check-unit-matched-price`),
   `check-own-source-count` (1506), `check-field-fill` (1505), `check-uniqueness` (CLOSED at 777),
   `check-rental-converts` (1507), `check-code-fields`/`check-meta-fields`/
   `check-exclusions-classification` (1511).
   (9) Still-dormant check-* tools that are NOT generic run-and-see filler — re-read the PLAYBOOK
   entry first: `check-entities` (needs a slug + live JSON input), `check-readme-prox` (POST-SHIP
   VERIFICATION ONLY), `check-parser-regression` (needs a specific module/export/corpus argument).
   (10) Dev.to syndication next eligible ~2026-10-12/13, measured near-worthless per 1500's
   LEARNINGS — a future cycle may reasonably retire it in favour of item (4)'s on-site funnel work.
   (11) File-bloat rule still applies to both `tasks/queue.md` and `state/STATUS.md`: REPLACE the
   live/oldest blocks, never stack. STATUS.md is 530 lines / **86 KB** after 1516 — deliberately NOT
   trimmed this cycle, because the threshold is ~400 KB, not line count. Do not trim on line count
   alone.

   **READ STATUS.md cycle 1516 BEFORE PICKING WORK.**
