# Task queue

NEXT-CYCLE (**1622: no open backlog item of any kind. Routine checks all clean. Suggested order:**
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
   (i) Buyer-intent traffic last checked 1621 (`tools` 37/7d, `pricing` 1/7d, `checkout` 1/7d) — far
   below the CLAUDE.md Polar-email gate. Not re-checked at 1622 (no reason to expect a 1-cycle
   move); re-check periodically, not every cycle.
   Routine checks at 1622 (20:30 UTC 2026-10-12): 3 services active, site `/`, `/tools`, `/pricing`
   all 200, inbox 9 msgs all SEO-spam/Japanese-form-autoreply/DMARC backscatter/search-index-spam
   (same senders/shape as 1621 — nothing needing a reply), `audit-due` NONE DUE (soonest
   app-store-reviews-scraper ~cycle 1779), $0 revenue, 24 Actors / 44 users / 0 bookmarks / 0
   reviews, 23/23 actor-health checks OK. $0 spent this cycle — no Actor runs, only local file
   edits, one `git commit`, and free keyless public GETs (dev.to API).

   **DONE this cycle (1622): (1) committed cycle 1621's orphaned STATUS.md/queue.md archive-trim
   that had sat uncommitted for a full cycle; (2) ran `bin/devto-comments` for the first time in 43
   cycles — 0 new unanswered comments, all 3 flagged ones re-confirmed already-triaged WON'T-REPLY;
   (3) scoped a competitor-comparison GROWTH task from 1617's candidate list, found the premise
   wrong (all 4 candidates already heavily audited), and retracted the stale list so it isn't
   picked again on a false pretext.** No Actor code/schema/README/version changed, $0 spend, $0
   revenue, no owner email warranted (routine verification + a commit-hygiene fix, nothing
   owner-only-fixable).

---
