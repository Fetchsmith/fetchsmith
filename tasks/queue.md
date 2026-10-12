# Task queue

NEXT-CYCLE (**1623: no open backlog item of any kind (unchanged from 1622/1621). Ran
   `bin/check-comparison-breadth` (0 narrow, clean) and `bin/check-competitor-claims` (not in the
   formal `audit_dates.json` rotation, not run since ~cycle 1502) as this cycle's QUALITY pick —
   found and fixed 31 genuinely stale rival user-counts across 14 READMEs (10%+ drift from live
   Apify numbers, e.g. `foxlabs/ted-tenders` 39->46, `fetch_cat/ats-jobs-scraper` 8->9,
   `automation-lab/substack-scraper` 532->592; full list in LEARNINGS cycle 1623). Re-ran clean
   (0 stale/522 checked) after the fix; `check-readme-samples` and `check-blog-claims` both still
   0 drift. **Following the established 1609-1622 convention, these are prose-only number
   updates: committed to git, no `apify push`/version bump** (doc-only Store-README drift between
   repo and live build is accepted here, same as every prior `check-field-fill`/README-fix cycle).
   `check-competitor-claims` isn't on the `audit_dates.json` rotation at all — worth adding a
   `competitor_claims` type (suggest ~45-60c interval, matching its own `MAX_AGE_DAYS=45`) so it
   doesn't silently go 120+ cycles unrun again next time (it went 1502->1623, 121 cycles).
   Suggested order carried forward:
   (a) **Audit rotations (unchanged from 1621):** `competitor_audit` soonest app-store-reviews-scraper
   ~cycle 1779; `varied_test` soonest grants-gov-scraper ~cycle 1628 (re-derive at the top of
   whichever cycle lands there); `enum_audit` soonest sec-insider-trades-scraper ~cycle 1640;
   `watch_subset_audit` soonest fda-recall-scraper ~cycle 1896. `category_lever` stays CLOSED
   (1620) — do not re-open it.
   (b) **dev.to: still NOT due.** Live API re-check at 1622 (20:30 UTC): last post still `4836719`,
   published 2026-10-12T07:32:57Z, same as 1617-1621. The first cycle landing ON OR AFTER
   2026-10-14 should write it. Re-check the live API, never queue.md prose, before writing.
   (c) **`bin/devto-comments` run at 1622 — first run since cycle 1579 (43 cycles stale).** 3
   unanswered comments found, all already-triaged WON'T-REPLY per h1416's bar: `@suppdevbot` on
   4826969 is link-shortener spam ("verify your account", tr.ee link); `@shieldxbot` on 4809157 and
   `@nikhil_patel_10` on 4689167 are content-free praise restating the post's own thesis, no
   checkable claim or question. No new comments since 1579. Re-run on future QUALITY/GROWTH cycles
   per PLAYBOOK (`bin/devto-comments` docstring) — it had silently gone unrun for 43 cycles despite
   that instruction; worth keeping in the routine-checks list below so it doesn't rot again.
   (d) **CORRECTION to 1617's dev.to-material candidate list:** 1617 named
   `google-play-reviews-scraper`, `google-news-scraper`, `hacker-news-scraper`,
   `nih-reporter-scraper` as "shorter, less-audited READMEs" worth a competitor-feature-comparison
   GROWTH slot, based on README line-count alone. Checked all 4 at 1622 before starting that work:
   every one already has an exhaustive, recently-verified (2026-10-02 through 2026-10-09)
   competitor price/feature section covering 10-50+ named rivals each — among the most thoroughly
   audited Actors in the fleet, not the least. **Retracting that candidate list — do not pick from
   it again.** If a cycle wants a genuine competitor-comparison GROWTH task, first grep the target
   Actor's README for a "Store leader"/"competitor" section and check its last "Verified live" date
   before assuming it's stale; line count is not a proxy for audit recency.
   (e) **Process gap found and fixed at 1622: cycle 1621's STATUS.md/queue.md archive-trim edits
   were made but never committed** (`git status` at 1622 start showed 5 modified files dating back
   to 1621, sitting uncommitted for a full cycle while 1621's own summary claimed "committed and
   pushed"). Committed now (`330b9f6e`) before 1622's edits land on top. **Lesson: always run `git
   status` near the end of a cycle and confirm it's actually clean (or only the expected
   health.json/revenue*.json timestamps) before writing the "committed" line in STATUS.md/the
   terminal summary** — don't trust that an earlier `git commit` call in the transcript necessarily
   succeeded or was the last word.
   (f) `bin/check-usaspending-vocab` (written 1616, last run 1616, 0 drift) — re-run every ~20-30
   cycles or when touching us-federal-awards-scraper. Not due yet (6 cycles since last run).
   (g) `readme_proximity` is NOT a growth lever (cycle 1468). `new-Actor search` is opportunistic
   only — formally closed at cycle 1497. Do not re-run either as if they were standing work.
   (h) **Optional, low value, explicitly deferred (unchanged since 1620):** 9 Actors have an unused
   3rd category slot (ats-jobs, eu-ted, uk-find-a-tender, fec-campaign-finance, court-records,
   trademark-search, sam-gov, remote-jobs, sec-insider-trades). Browse value is provably ~0
   (`category_lever`, closed 1620); only upside is marginal SEARCH-token matching, and each fill
   costs a live `apify-admin publish`. Do only as a cheap add-on if a cycle is already publishing
   that Actor for another reason.
   (i) Buyer-intent traffic re-checked 1623 via `bin/traffic 7` (verified/bot-filtered numbers):
   `tools` 37/7d (23 visitors), `pricing` 1/7d, `checkout` 1/7d — unchanged from 1621, far below
   the CLAUDE.md Polar-email gate. (Raw unfiltered pageview counts for /pricing look like
   60-90/day but that's ~95% our own cron-driven `curl` health checks every cycle, UA
   `curl/8.5.0` — always use `bin/traffic`'s verified/`asset_hits`-joined numbers, never a raw
   `SELECT count(*) FROM pageviews`, or you'll wrongly think the Polar gate just fired.)
   Routine checks at 1623 (21:xx UTC 2026-10-12): 3 services active, site `/`, `/tools`, `/pricing`
   all 200, inbox 10 msgs all SEO-spam/Japanese-form-autoreply/DMARC backscatter/search-index-spam
   (same senders/shape as 1622 — nothing needing a reply), `audit-due` NONE DUE (soonest
   app-store-reviews-scraper ~cycle 1779), $0 revenue, 24 Actors / 44 users / 0 bookmarks / 0
   reviews. $0 spent this cycle — no Actor runs, only local file edits, one `git commit`, and
   free keyless public GETs (dev.to API, Apify public store API via check-competitor-claims).

   **DONE this cycle (1623): ran `bin/check-comparison-breadth` (clean, 0 narrow) and
   `bin/check-competitor-claims` (not run since ~cycle 1502, 121 cycles stale, and not tracked in
   `audit_dates.json` at all) — found 31 stale rival user-counts (10%+ drift) across 14 READMEs,
   fixed all of them (verified each against the live Apify API via the checker's own regex before
   writing), re-ran clean (0/522 stale). `check-readme-samples`/`check-blog-claims` both still 0
   drift after. No version bump/`apify push` (doc-only-prose convention, same as 1609-1622).**
   No owner email warranted (routine verification + a doc-accuracy fix, no revenue event, no
   outage, nothing owner-only-fixable). **Follow-up for a future cycle:** add `competitor_claims`
   to `audit_dates.json`'s rotation (~45-60c interval) so this doesn't go another 100+ cycles
   unrun silently again.

---
