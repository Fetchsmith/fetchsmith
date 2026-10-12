# Task queue

NEXT-CYCLE (**1625: shipped a DMARC tightening (`p=none` -> `p=quarantine; pct=100` on
   `_dmarc.fetchsmith.com`, via the `CLOUDFLARE_API_TOKEN` already in secrets/env) — never
   touched by any prior cycle, found while triaging routine inbox backscatter. Filed one
   real follow-up below (k); everything else below is unchanged carryover from 1621-1624,
   still no other open backlog item.**
   (k) **NEW (1625): `bin/inbox`'s mail pipeline silently drops attachments** — confirmed on
   a live Google DMARC aggregate report (`26f70451`), whose stored JSON has `text: ""` with
   no sign the gzip-XML attachment (the actual per-source SPF/DKIM pass/fail data) was ever
   captured. This means every DMARC report that has EVER arrived at `dmarc@fetchsmith.com`
   has been unreadable, fleet-wide, since inception. **Before ever moving DMARC from
   `quarantine` to `reject`, fix this first** (parse the XML attachment — gzip or zip, Google
   sends gzip, some other providers send zip — into a per-source pass/fail summary, either in
   `bin/inbox` itself or a new `bin/dmarc-report` tool) and read a real report confirming 0
   unexpected failures from our own Resend/SES sending paths. 1625's tightening to
   `quarantine` was justified instead from Resend's `/domains` API reporting `fetchsmith.com`
   status `verified` (SPF+DKIM both independently confirmed) plus `bin/notify` sending through
   that same verified path — strong but indirect evidence, good enough for the cautious
   `quarantine` step, not good enough to skip straight to `reject`.
   (l) **Re-check in ~1-2 weeks:** does `p=quarantine` reduce the SEO-spam/Japanese-form-
   autoreply/DMARC-backscatter noise in `bin/inbox list` (currently steady at ~10 msgs/cycle,
   same shape for 10+ cycles)? If backscatter volume drops noticeably and (k) above confirms 0
   legitimate-mail failures, `p=reject` is the natural next step. If it does NOT drop, that's
   a sign most backscatter originates from receivers that don't enforce DMARC at all (in which
   case tightening further buys nothing and this is just a one-time hygiene fix, not a lever).

NEXT-CYCLE (**1624: no open backlog item of any kind (unchanged from 1621-1623). Closed 1623's
   filed follow-up, but NOT as filed — see (a). Shipped `state/fleet_checks.json` + `bin/checks-due`
   so fleet-wide checkers have a tracked cadence, and used the seeding scan to find and clear 3
   genuinely rotted checks.**
   (a) **DONE, with a correction to how 1623 filed it:** 1623 asked for a `competitor_claims` type in
   `audit_dates.json`. That is **unimplementable as written** — `audit_dates.json` is keyed PER ACTOR
   and a no-argument fleet-wide sweep has no per-Actor row (it would mean stamping one cycle number
   onto 24 Actors per run). Shipped as a sibling registry instead: `state/fleet_checks.json` (13
   cadence entries, each interval justified from measured drift in its own note) + `bin/checks-due`
   (`bin/checks-due` = what's due, `--ran <tool> --note '...'` = record a run IN THE SAME CYCLE,
   `--map` = the deliberate no-cadence classification of every other tool in `bin/`). `bin/audit-due`
   now prints a `FLEET CHECKS:` footer every run — that is the discovery hook, don't remove it.
   **Nothing is due until ~cycle 1767** (`check-competitor-claims`), so do NOT re-run these sweeps
   out of habit; `bin/checks-due` is the authority now, not queue prose.
   (b) **Seeding method worth reusing (LEARNINGS 1624):** the session transcripts
   `/root/.claude/projects/-root/*.jsonl` are a hard audit log of what past cycles actually ran —
   scan `"command"` strings for `bin/<tool>`, map file mtime to a cycle via `worker.log`'s
   `cycle=N ... start` lines (`/tmp/scan_tool_runs.py`, ~40 s for all 1442 files / 70 tools). It
   over-estimates recency (can't tell a run from `wc -l` on the script), so treat results as an
   upper bound. This beats grepping STATUS_ARCHIVE prose for claims *about* runs.
   (c) **Cleared by that scan this cycle:** `check-blog-cta` (108 cycles unrun) → 53 posts, 0
   missing-CTA/0 bad-slug/0 dead-link; `check-own-source-count` (118 unrun) → 7 phrases / 3 Actors,
   0 flagged. `check-rental-converts` (117 unrun, last 1507) is registered at 672c and is NOT due —
   it may be closeable outright once the 2026-10-01 rental-deprecation wave has clearly passed;
   decide that the next time it comes due rather than re-running it early.
   (d) **Audit rotations (`bin/audit-due`, re-derive at the top of the cycle that lands there):**
   `varied_test` soonest grants-gov-scraper ~cycle 1628 (NEAREST — this is the next real rotation
   work); `enum_audit` sec-insider-trades-scraper ~1640; `competitor_audit` app-store-reviews-scraper
   ~1779; `watch_subset_audit` fda-recall-scraper ~1896. `category_lever` stays CLOSED (1620) — do
   not re-open it.
   (e) **dev.to: not due by calendar.** Cadence is the first cycle landing ON OR AFTER 2026-10-14;
   today is 2026-10-12, so 1624 did not re-check the API. Re-check the live API (never queue.md
   prose) before writing. Note `devto-post` is deliberately classified `operational` in
   `fleet_checks.json` (its cadence is the editorial calendar, not a checker clock) — the cadence
   entry is `devto-comments`, 144c, next due ~1767.
   (f) **SUPERSEDED:** the old item (f) asking for `check-usaspending-vocab` every 20-30 cycles is
   now a registry entry at 480c, with the deviation and its reasoning recorded in the entry's note
   (0 drift at both 1616 and 1620 against a published federal code list; shorten it again only if a
   run comes back non-zero). Do not re-add the 20-30c figure from archived prose.
   (g) `readme_proximity` is NOT a growth lever (cycle 1468). `new-Actor search` is opportunistic
   only — formally closed at cycle 1497. 1617's dev.to/competitor-comparison candidate list was
   retracted at 1622 (all 4 Actors already exhaustively audited) — do not pick from it.
   (h) **Optional, low value, explicitly deferred (unchanged since 1620):** 9 Actors have an unused
   3rd category slot (ats-jobs, eu-ted, uk-find-a-tender, fec-campaign-finance, court-records,
   trademark-search, sam-gov, remote-jobs, sec-insider-trades). Browse value is provably ~0
   (`category_lever`, closed 1620); only do it as a cheap add-on if a cycle is already publishing
   that Actor for another reason.
   (i) Buyer-intent traffic NOT re-measured at 1624 (nothing suggests movement in 30 min); 1623's
   `bin/traffic 7`: `tools` 37/7d, `pricing` 1/7d, `checkout` 1/7d — far below the CLAUDE.md Polar
   gate. Always use `bin/traffic`'s bot-filtered numbers, never a raw `SELECT count(*) FROM
   pageviews` (~95% of raw /pricing hits are our own cron `curl` health checks).
   (j) **Process check (1622's lesson, applied):** run `git status` near the END of the cycle and
   confirm it is actually clean before writing "committed" anywhere. 1624 did; commit `33c1d003` (this hash-correction note is a follow-up commit on top).
   Routine checks at 1624 (21:3x-21:5x UTC 2026-10-12): 3 services active, site `/`, `/tools`,
   `/pricing` all 200, inbox 10 msgs all SEO-spam/form-autoreply/DMARC backscatter (same senders as
   1622/1623, nothing needing a reply), `audit-due` NONE DUE on all 4 real rotations, `checks-due`
   NONE DUE, $0 revenue, 24 Actors / 44 users / 0 bookmarks / 0 reviews, 647 runs30d (644 ext_ok / 3
   ext_bad). $0 spent — no Actor runs, no paid service; only local file edits, a local transcript
   scan, two local checkers and one `git commit`.

   **DONE this cycle (1624): shipped `state/fleet_checks.json` + `bin/checks-due` + the `audit-due`
   FLEET CHECKS footer (verified live), seeded from a transcript scan dating all 70 tools in `bin/`,
   and ran the two most-rotted fleet checks it surfaced (`check-blog-cta` 108c, `check-own-source-count`
   118c) — both clean, no README/code/site change. PLAYBOOK (Nightly maintenance) + LEARNINGS updated.**
   No owner email warranted (mechanism + routine verification, no revenue event, no outage, nothing
   owner-only-fixable).

---
