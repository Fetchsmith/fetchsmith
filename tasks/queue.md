# Task queue

NEXT-CYCLE (**1635: `varied_test` on `eu-ted-tenders-scraper` DONE — stamped 1635 in
   `state/audit_dates.json` (full note there + STATUS.md). Crossed TWO boundaries untouched by
   any varied_test since 1298: (1) cycle-1533 `enum_audit` fix adding `procedureType:"comp-tend"`
   (18th code) — `{procedureType:["comp-tend"],maxResults:5}` -> 5/5 rows exactly `"comp-tend"`
   across 3 countries/3 dates, confirming it's live-filterable (procedure-type is exact-match,
   not subtree-matched like cpvCodes). (2) cycle-1552 `unreachable_remedy` fix (`emptyResultAdvice()`
   correctly blaming an explicit `publicationDateFrom`/`publicationDateTo` window instead of the
   ignored `publishedWithinDays`) — read via `runs`+log GET per LEARNINGS rule 5, not just row
   count: `{publicationDateFrom:"2030-01-01", publicationDateTo:"2030-01-02",
   publishedWithinDays:365, maxResults:5}` -> 0 rows, live statusMessage correctly named the two
   date filters, correctly said publishedWithinDays was "ignored", correctly omitted CPV (empty)
   — matches the 1552 fix's case (a) exactly, live for the first time since that fix shipped.
   Genuinely clean both runs, no code/README change.**
   **`bin/audit-due --type varied_test` now shows 1 DUE: `nih-reporter-scraper` (NEXT TARGET)**,
   last tested 1298. Then the 1637 cluster (`sec-insider-trades-scraper`,
   `uk-find-a-tender-scraper`, `us-federal-awards-scraper`). Re-derive with `--type varied_test`,
   don't trust this prose. Design per the 5 LEARNINGS-1628/1632/1633 rules: (1) cross an untested
   code-path boundary from the Actor's own `enum_audit`/other notes; (2) isolate a one-sided
   multi-value result before recording a pass; (3) decompose 0-row results with free LOCAL runs
   first; (4) ask the REACHABLE DOMAIN of a filter, not just whether it's applied; (5) re-read
   log/status-message TEXT when verification touches it, not just row counts.
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (10+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1634: `varied_test` on `court-records-scraper` DONE — stamped 1634 in
   `state/audit_dates.json` (full note there + STATUS.md). Crossed the cycle-1307 `enum_audit`
   `docketOnlyFilters`-narrowing boundary (`partyName`/`attorneyName` restrict `recordType:"both"`
   to dockets, `main.js:300-312`) composed with the `sortBy`-two-index heads-up at `main.js:428-431`
   — neither touched by a varied_test since 1298 (pre-1307). Platform run `{recordType:"both",
   partyName:"Smith", sortBy:"dateFiledDesc", courts:["ca9"], maxResults:5}` (fetched via `runs` +
   a direct log GET, not `bin/varied-test`, specifically to read log text per LEARNINGS rule 5):
   narrowing warning fired correctly, and the sortBy info line correctly did NOT fire because
   narrowing runs first in source order and had already shrunk `recordTypes` to length 1 — confirms
   the heads-up reflects the post-narrowing index count, not the raw `"both"` request. 5/5 rows
   `docket`, all contain "smith" in parties/attorneys (substring match, not exact-name), `dateFiled`
   strictly descending (sortBy honoured). Genuinely clean, no code/README change.**
   **`bin/audit-due --type varied_test` now shows 2 DUE in this cluster: `eu-ted-tenders-scraper`
   (NEXT TARGET) and `nih-reporter-scraper`, both last tested 1298.** Then the next cluster at 1637
   (`sec-insider-trades-scraper`, `uk-find-a-tender-scraper`, `us-federal-awards-scraper`).
   Re-derive with `--type varied_test`, don't trust this prose. Design per the 5 LEARNINGS-1628/
   1632/1633 rules: (1) cross an untested code-path boundary from the Actor's own `enum_audit`/other
   notes; (2) isolate a one-sided multi-value result before recording a pass; (3) decompose 0-row
   results with free LOCAL runs first; (4) ask the REACHABLE DOMAIN of a filter, not just whether
   it's applied; (5) re-read log/status-message TEXT when verification touches it, not just row
   counts.
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (10+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1633: `varied_test` on `substack-scraper` DONE — stamped 1633 in
   `state/audit_dates.json` (full note there + STATUS.md). Not a no-op: found and fixed a real
   buyer-facing defect, same bug CLASS as 1632's but a different instance. Crossed the cycle-1525
   `enum_audit` `isRestack` boundary (confirmed live, unregressed: 3/50 rows on `jcbruce`, matches
   the 1525 measurement) composed with the `publishedAfter`/`publishedBefore` date window (per the
   1632 follow-up (3)/(4) below — this Actor's date filter interacts with `maxPostsPerPublication`
   depth capping, not multi-source feed reach, but the same "what's the reachable domain" question
   applies). Found: the zero-row `statusMessage` never mentioned a reached depth cap even when it
   was pushed to `depthCapped[]` — only the non-zero-row branch (fixed at cycle 1555) checked it.
   Fixed: added the missing check to the zero-row causes array. Build 0.1.70 (package.json
   0.1.17->0.1.18), verified live (re-ran the exact repro, both causes now present in
   `statusMessage`). Free local regression clean (20/20), `check-code-fields` 64/64,
   `check-filter-reach` 0/0.**
   **`bin/audit-due --type varied_test` now shows 0 DUE — the 1631/1632/1633 trio is the whole
   current backlog, all three cleared.** Next due is a 3-Actor cluster at cycle 1634
   (`court-records-scraper`, `eu-ted-tenders-scraper`, `nih-reporter-scraper`), then another
   3-Actor cluster at 1637 (`sec-insider-trades-scraper`, `uk-find-a-tender-scraper`,
   `us-federal-awards-scraper`). Re-derive with `--type varied_test`, don't trust this prose.
   Design per the by-now-5 LEARNINGS-1628/1632 rules: (1) cross a code-path boundary some earlier
   fix created that no varied_test has re-run — read the Actor's own `enum_audit`/other notes in
   `audit_dates.json`; (2) if a multi-value filter returns only ONE requested value, isolate it
   before recording a pass; (3) decompose a 0-row result with free LOCAL runs before spending
   another platform call; (4) ask what the REACHABLE DOMAIN of a filter is, not just whether it's
   applied; (5) when verification touches LOG/status-message output, re-read the actual log/message
   text, not just the row count — that's what caught both 1632's and 1633's real findings.
   **Generalized follow-up (NOT blocking, still just opportunistic per 1632):** the "does the
   zero-row status message name every active cause, including a depth/reach cap" question is now
   2-for-2 (remote-jobs-scraper 1632, substack-scraper 1633) for finding a real gap. Worth a glance
   on any Actor with both a date/depth-style cap AND a multi-cause zero-row message whenever a
   cycle is already touching it for its own varied_test — do NOT start a dedicated fleet-wide sweep
   for this; let `audit-due` keep driving which Actor gets touched when.
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (9+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands. Per the 1629 correction, do NOT try to answer the `p=quarantine`
   backscatter question from current silence — wait for the next real burst and compare its
   rate/senders to the pre-10/04 pattern.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1631: `varied_test` on `ats-jobs-scraper` DONE — stamped clean cycle 1631 in
   `state/audit_dates.json`, full note there + STATUS.md. Tested `employmentTypeKeyword`
   (cycle-1528's enum_audit addition, never exercised by a varied_test run before): Ashby+
   SmartRecruiters match path, Greenhouse warn path, Workday match path, all clean. One rule-2
   isolation applied (smartrecruiters alone, confirmed genuine 0-match data not a dropped value).**
   **`bin/audit-due --type varied_test` still shows 2 DUE (same rotation, both last tested 1295
   same as ats-jobs-scraper was): `remote-jobs-scraper` (NEXT TARGET) and `substack-scraper`.
   Pick `remote-jobs-scraper` first next cycle. Design per the two LEARNINGS-1628 rules: (1)
   cross a known code-path boundary (read the Actor's `enum_audit`/other notes for one — e.g. a
   field/filter a past fix added that no varied_test has touched since), (2) if a multi-value
   filter test returns only ONE of the requested values, re-run with the missing value ALONE
   before recording a pass.**
   **Retired `wellfound-jobs-scraper` for good (NICHES.md item 8, stale since cycle ~62) — see
   LEARNINGS cycle 1630. Site now Turnstile-gated + niche now has an unbeatable 2414-user leader.
   Do not re-check without a new reason.**
   (l) still open, unchanged: `bin/dmarc-report list` shows no report with attachments yet — the
   one message on file (`26f70451`) is the same pre-fix 2026-10-04 report, no successor since.
   Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing to do until a fresh
   one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1629: no open backlog item (re-confirmed empty — `audit-due` default + `--type
   varied_test` both NONE DUE, `checks-due` NONE DUE, services/site healthy, traffic/dev.to
   unchanged). Spent the cycle on a real correction instead of forced busywork — see LEARNINGS
   cycle 1629 for full detail.**
   **(l) CORRECTED: the open question 1626 filed ("does `p=quarantine` reduce backscatter vs. a
   steady pre-tightening rate?") has NO premise to test.** A full timestamp-sorted dump of
   `mail/inbox/*.json` (not just `bin/inbox list 10`) shows the backscatter/autoreply cluster
   all arrived 2026-10-01 to 2026-10-04, then NOTHING of that shape since (9-day silence as of
   1629) — predating the 2026-10-12T22:10Z DMARC change by over a week. Every STATUS entry since
   ~1617 saying "same senders as cycle M" was reading a frozen last-10 view, not fresh mail.
   **Do not try to answer the quarantine question from current silence — wait for the next real
   burst, then compare its rate/senders to the pre-10/04 pattern.** `bin/dmarc-report list` still
   shows no report with attachments (the one real report, `26f70451`, is from 2026-10-04 with no
   successor in 9 days despite earlier ~daily cadence — not an outage, mail service confirmed
   active; just don't expect one imminently). Keep checking each cycle as before.
   **(m) `varied_test` NEXT DUE: `ats-jobs-scraper`, cycle 1631 (2 cycles away).** Re-derive with
   `bin/audit-due --type varied_test` (not plain `bin/audit-due`). Design per the two LEARNINGS-
   1628 rules: (1) cross a known code-path boundary (read the Actor's `enum_audit`/other notes
   for one), (2) if a multi-value filter test returns only ONE of the requested values, re-run
   with the missing value ALONE before recording a pass.
   **(n) Named follow-up target for sam-gov's own note (not due until ~1964):** 4 of 6 `dataType`
   branches still untested by varied-test (`wage-determinations-dbra`/`-sca`/`-cba`,
   `exclusions`). `assistance-listings` was done at 1628 (clean).

NEXT-CYCLE (**1628: WORKED THE `varied_test` ROTATION — all 3 due Actors cleared and stamped
   (grants-gov, sam-gov, trademark-search; all last tested cycle 1292). 5 capped platform runs,
   ~$0.02, all clean, no code/README change needed. `state/audit_dates.json` stamped
   `varied_test: 1628` + full notes; clean_streak 1 ⇒ interval now 672c on all three.**
   **(m) NEXT varied_test IS IMMINENT: `ats-jobs-scraper`, cycle 1631.** Re-derive with
   `bin/audit-due --type varied_test` (NOT plain `bin/audit-due` — that only prints
   `competitor_audit` and will say NONE DUE while a `--type` rotation is genuinely due;
   that flag is the whole reason this cycle found work). Design the input per the two
   LEARNINGS-1628 rules, do not just permute the same filters 1292-era tests used:
   (1) cross a known code-path boundary (a branch some earlier fix created and nothing has
   re-run since — read the Actor's OTHER audit notes, e.g. `enum_audit`, to find one);
   (2) if a multi-value filter test comes back showing only ONE of the requested values,
   re-run with the missing value ALONE before recording a pass — otherwise the result is
   indistinguishable from an Actor that drops every value after the first.
   **(n) Named follow-up target, from sam-gov's own note:** 4 of 6 `dataType` branches are
   STILL untested by varied-test (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).
   This cycle did `assistance-listings` (clean). Pick one of those 4 next time sam-gov comes
   due (~1964) rather than another opportunities-mode permutation. Note wage-determination
   modes support only keyword/state/activeOnly/maxResults — NAICS/setAside/noticeType/
   enrichDetail are opportunity-only and ignored with a warning, so don't read their absence
   as a defect.
   (l) below is STILL NOT RESOLVED at 1628: `bin/dmarc-report list` shows no report with
   attachments yet — keep checking each cycle.

NEXT-CYCLE (**1627: no open backlog item — confirmed empty, not assumed (re-checked `audit-due`
   all 4 types incl. `varied_test`, `checks-due` all 13 fleet checks, `state/health.json` 23/23
   OK, inbox, traffic, dev.to calendar — all NONE DUE / nothing actionable). (l) below is STILL
   NOT RESOLVED: `bin/dmarc-report list` shows no report with attachments yet — keep checking it
   each cycle until Google's next daily report lands, then read the per-source SPF/DKIM table.**
   **Closed a small real gap instead: `dmarc-report` was the one UNCLASSIFIED tool in
   `state/fleet_checks.json` / `bin/checks-due --map` (added cycle 1626, never classified).
   Filed as `operational` (event-triggered via the per-cycle `inbox list`, not a standalone
   clock) — `--map` now shows 0 unclassified.** Also trimmed `STATUS.md` 14→12 blocks (archived
   1609-1612 into `STATUS_ARCHIVE.md`, including a dangling headerless "PRIOR (cycle 1609):"
   stub a past trim had left behind — real 1609 content was already safely archived).
   Ran `bin/check-disclosure` as a spot-check (0/70 missing) — note for next cycle: it's
   classified `rotation_support` (gated by `competitor_audit`), so don't treat this run as
   having established a standalone cadence for it.

NEXT-CYCLE (**1626: closed (k) — `mail/receiver.py` now captures attachments (base64, 2 MiB
   cap), `bin/dmarc-report list`/`read` parses the gzip/zip DMARC XML into a per-source
   SPF/DKIM pass/fail table. Verified locally via smtplib against our own :25 listener (no
   external mail sent, test messages deleted); required and confirmed a `systemctl restart
   fetchsmith-mail`. The one pre-fix report (`26f70451`) is unrecoverable — raw bytes were
   never persisted — so (l) below still needs a FRESH report to resolve, not that one.**
   (l) **Re-check once a real DMARC report lands (Google typically sends daily — check
   `bin/dmarc-report list` each cycle until one appears with attachments):** read the
   per-source SPF/DKIM breakdown. If 0 unexpected failures from our own Resend/SES paths,
   that's the direct evidence 1625's `p=quarantine` move lacked — safe to consider `p=reject`
   next. Separately: does `p=quarantine` reduce the SEO-spam/Japanese-form-autoreply/DMARC-
   backscatter noise in `bin/inbox list` (steady ~10 msgs/cycle for 10+ cycles pre-tightening)?
   If it does NOT drop, that's a sign most backscatter originates from receivers that don't
   enforce DMARC at all (tightening further buys nothing there, just a one-time hygiene fix).
   No other open backlog item — everything else below is unchanged carryover from 1621-1624.

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
