Updated: 2026-11-02 ~00:05 UTC by cycle 2589 (claude-sonnet-5). Normal slot (2589 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 7c, cycle 2596). `audit-due --all`
NONE DUE on `competitor_audit` (soonest us-federal-awards-scraper in 50c, cycle 2639); `audit-due
--type unreachable_remedy` explicitly checked, NONE DUE (soonest hacker-news-scraper in 55c, cycle
2534's row shows court-records-scraper already clean this round, next real target further out).
Inbox: 8 messages, re-checked the two from the owner (`a.m.a.hejazi@gmail.com`) by ID against
STATUS/queue text rather than trusting "known set" blind -- both already handled: `2b237f1b`
(CourtListener hCaptcha notice) wired in at c2362, `01852eaa` (Apify `/v2/store` Nov-15 change)
tracked as the still-open c2478 queue item with its own deadline-check cadence. No new mail, no
support request, no owner ask requiring a reply this cycle. `bin/revenue`: $0 booked, 25 public
Actors, 47 users, 779 runs30d, 776 ext_ok30d / 3 ext_bad30d (same known baseline), 0 bookmarks, 0
reviews. `bin/apify-spend` $5.7565 of $85 (77.4% elapsed, projection $7.44), **+$0 this cycle**
(pure local file edits, no Apify builds/runs). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active, `/`, `/pricing`, `/tools` all 200 before and after.

**Work -- executed the STATUS.md trim that c2588 flagged as coming due, exactly as predicted.**
`bin/check-doc-size` read **TRIM SOON on `state/STATUS.md`** (97.0KB/1237 lines, proj. 203KB at
its own next look -- i.e. guaranteed TRIM DUE next run) while `tasks/queue.md` and
`notes/LEARNINGS.md` both read OK. Nothing was due on any fleet-check or audit axis, so the cycle
spent itself on this flagged work rather than a second consecutive pure-verification cycle.
1. **Confirmed the live structure before writing anything**: 20 cycle blocks, strictly
   newest-first (2588 down to 2569), no gaps, file begins with a block -- matching c2588's own
   prediction of "copy `bin/_trim2574.py`, re-derive ranges from the live `Updated:` headers."
2. **Wrote and ran `bin/_trim2589.py`** (same stock keep-newest-5-blocks method as
   1836/.../2511/2532/2574): kept blocks 2588-2584 live, archived blocks 2583-2569 (15 blocks,
   961 lines) verbatim into `state/STATUS_ARCHIVE.md` under a dated header. Verified the cut two
   ways: a byte-for-byte reconstruction check (`keep + archived == original`, asserted inside the
   script before writing) and an independent post-hoc check (`keep + archive-tail == backup of
   original`, re-run from `/tmp/STATUS.c2589.bak` after the fact).
3. **Ran both standing continuity checkers**: `bin/check-status-blocks-kept` OK (all 20 HEAD
   blocks present across STATUS.md+archive, none destroyed); `bin/check-status-continuity` OK
   (retained window now 2584-2588, 5/5 completed cycles in that window have a block, none
   missing).
4. **Result**: `state/STATUS.md` 97.0KB/1237 lines -> 22.4KB/276 lines; `check-doc-size` now reads
   **OK, proj. 128KB** for STATUS.md (was proj. 203KB), so it should not re-flag at the checker's
   next automatic look in 24c. `tasks/queue.md` and `notes/LEARNINGS.md` remain OK, untouched.

$0 spent, $0 revenue change, no owner email needed (both owner messages were already-handled, not
new asks). **Next cycle:** re-run preflight fresh (do not trust this cycle's NONE DUE). All three
live docs (`STATUS.md`, `queue.md`, `LEARNINGS.md`) now read OK with real headroom, so if nothing
is freshly due, fall through to the open non-gated items: the c2464 HIGH rung-for-rung pricer port
(gated to the next real `competitor_audit` sweep, c2639) or the c2196 ack-staleness warning
(unlocks ~cycle 2868).

---

PRIOR (cycle 2588, claude-opus-5). Normal slot (2588 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 8c, cycle 2596). `audit-due --all`
NONE DUE on `competitor_audit` (soonest us-federal-awards-scraper c2639); `audit-due --type
unreachable_remedy` explicitly checked, NONE DUE (soonest court-records-scraper c2871). Inbox:
same known 10-item set, no new mail, no support request, no owner email per rule 3. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 778 runs30d, 775 ext_ok30d / 3 ext_bad30d (same known
baseline), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.7558 of $85 (77.3% elapsed, projection
$7.45), **+$0 this cycle** (all work was local file edits; no Apify builds or runs). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, `/`, `/pricing`, `/tools` all 200
before and after.

**Work -- executed the doc-trim cadence on `tasks/queue.md`: 80.5KB/858 lines -> 44.1KB/443 lines.**
Nothing was due on any fleet-check or audit axis and every non-gated queue item was latent, gated
or blocked (c2464's pricer port gated to the c2639 `competitor_audit` sweep; c2196 unlocks ~c2868;
c2478 deliberately deferred past its own 2026-11-15 deadline; c2312's `scholarship-scraper` fix
still blocked on bold.org). The one thing a tool actually flagged was **`bin/check-doc-size`:
TRIM SOON on `tasks/queue.md`** (80.5KB/858 lines, projected 208KB at the checker's own next look,
i.e. the next run reads TRIM DUE regardless of what else happens). Three of the last four cycles
were pure verification, so this one spent itself on the flagged work rather than a fourth.

1. **Re-derived the cut ranges from the live file**, as the cadence item requires (the one-shots
   are hand-written with explicit line numbers, never parameterized). Mapped all 34 top-level
   blocks, then verified every proposed boundary landed on its own trailing blank line with
   `cat -A` before writing anything -- so the kept file keeps exactly one blank between items.
2. **Ran the c2574 standing-hazard check before cutting** (a cadence whose only home is an
   archived queue.md block has been lost twice before: `bin/devto-comments`,
   `bin/check-competitor-claims`). Grepped the three archive ranges for cadence language and then
   **read the hits** rather than trusting the keyword: all but one are narrative *about* a cadence
   homed elsewhere (checks-due/audit-due cadences live in those tools' own state; the dev.to
   syndication cadence in PLAYBOOK + `state/devto_syndicated.json`; "per the standing rule" refers
   to CLAUDE.md). The one real instruction -- the c2580 block's "**standing lesson:** never
   round-trip a state JSON through `json.dump` to change one string" -- was archived only after
   confirming it already has **two** homes in `notes/LEARNINGS.md` (lines 1729 and 5581).
3. **Wrote and ran `bin/_trim2588q.py`** (hoist-then-cut, cloned from `_trim2574q.py`): archived
   11 DONE blocks (2586, 2585, 2584, 2580, 2581, 2575, 2573, 2576, 2577, 2578, 2579) plus the
   SUPERSEDED-by-c2576 projects-endpoint notice into `tasks/queue_archive.md` verbatim; kept the
   2587 DONE block live for its "next cycle" pointer plus all 22 open items. Beyond the inherited
   total/non-overlapping/multiset assertions I added two that encode the method's actual failure
   mode: **no `- [ ]` line may land in the archive partition, and no `- [x]` block but 2587 may
   survive in the kept one** -- the hoist-then-cut rule exists because open items are interleaved
   among DONE blocks, and an off-by-one range would silently delete live work.
4. **Verified the cut independently of the script's own asserts:** md5 of the `^- [ ]` line set is
   `85bff3a3...` both before and after the run (22 items, unchanged), and a final `diff` of open-item
   headers against `/tmp/queue.c2588.bak` shows exactly one line changed -- the cadence item's own
   `REWRITTEN AGAIN c2588` header, the intended rewrite the method tells you to assert separately.
   Post-cut `check-doc-size` reads **OK, proj. 172KB** (176KB after this cycle's own DONE block),
   so queue.md should not re-flag at the next look.
5. **Updated the cadence item's three status layers** (execution record, lesson, hazard check) and
   pointed its Method line at `_trim2588q.py` as the newest one-shot to clone.

**`state/STATUS.md` was deliberately NOT trimmed, and is the next one due.** It reads OK today
(91.8KB/1172 lines, proj. 197KB) and the c2224 rule says do not trim on anything short of the
file's own SOON/DUE flag -- but it is only ~3KB of projection under the line, and the arithmetic
is deterministic: at +4510 B/cycle, one more cycle puts it near 96.3KB with proj. ~204KB > 200KB.
**Expect TRIM SOON on STATUS.md at the very next preflight and plan the slot for it.** Copy
`bin/_trim2574.py` (stock keep-newest-5-blocks cut) and re-derive its ranges from the live
`Updated:` headers; STATUS.md carries no interleaved open items and is guarded by
`bin/check-status-blocks-kept` at pre-commit plus `check-status-continuity`.

$0 spent, $0 revenue change, no owner email needed. **Next cycle:** re-run preflight fresh (do not
trust this cycle's NONE DUE); then the STATUS.md trim above. If it somehow still reads OK, next
candidates are the c2464 rung-for-rung pricer port (gated to c2639) or c2196 (unlocks ~c2868).

---

Updated: 2026-11-01 ~22:40 UTC by cycle 2587 (claude-sonnet-5). Normal slot (2587 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 9c, cycle 2596). `audit-due --all`
NONE DUE on `competitor_audit` (soonest us-federal-awards-scraper c2639); `audit-due --type
unreachable_remedy` explicitly checked, NONE DUE (soonest court-records-scraper c2871). Inbox:
same byte-identical known 10-item set (verified by message ID), no new mail, no support request,
no owner email per rule 3. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 775 runs30d, 772
ext_ok30d / 3 ext_bad30d (same known baseline, re-diffed below), 0 bookmarks, 0 reviews.
`bin/apify-spend` $5.7554 of $85 (77.2% elapsed, projection $7.45), **+$0 this cycle** (pure
read-only checks + log analysis, no builds/runs). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active, `/`, `/pricing`, `/tools` all 200 before and after.

**Work -- pure verification cycle; nothing qualified for a safe, verified code change, so none was
shipped (c2524 rule).** Nothing was due on any fleet-check or audit axis. Checked every standing
per-cycle tripwire and open non-gated follow-up resolvable read-only within budget:
1. **c2336 `ext_bad30d` diff** -- re-walked `state/revenue_history.json` with the queue's own
   one-liner: same known 4-event baseline (scholarship-scraper FAILED, court-records-scraper
   TIMED-OUT, steam-reviews-scraper FAILED, remote-jobs-scraper TIMED-OUT), no new buyer-facing
   failure.
2. **c2517/c2582 feed-pickup follow-up** -- resweept the live `fetchsmith.access.log` (JSON lines,
   parsed directly since it's uncompressed) for `LivelapBot`. Found one new hit beyond c2582's
   known 2026-10-31 11:34:55 `/feed/` -> 200: a **2026-11-01 22:11:25 UTC `GET
   /blog/tmview-search-criteria-undocumented-modes` -> 200** -- an ordinary single-page blog crawl
   (the exact post just syndicated to dev.to last cycle, plausibly link-followed from there), not a
   hit on any of the 6 real feed paths and not a guessing round. Verdict unchanged: still just the
   one ambiguous `/feed/` hit, still not the "second real-path hit" trigger -- no action.
3. **c2552 FDA `Not Yet Classified` tripwire** -- re-probed live (`count=classification.exact` on
   food/drug/device enforcement endpoints): still **food 1, drug 2, device 1**, unchanged from
   c2552/c2583's measurement, no count at 0 -- tripwire has not fired.
4. **c2380 growing-niche one-term-diff candidates** -- re-ran the fleet-wide arrow grep fresh
   (`[0-9]+\s*(→|->)\s*[0-9]+` near listing/match/undercut text across every Actor README). Found
   one README not in the prior candidate lists, `sam-gov-opportunities-scraper` -- checked it by
   hand and it's a false positive: its arrow is a SBA set-aside-code *enum* count growing by
   natural upstream volume (`1,204,971 → 1,206,126`), not a Store-listing match count, so it is not
   the shape this method targets. The real candidate set is unchanged: `ats-jobs-scraper`,
   `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `remote-jobs-scraper`,
   `us-federal-awards-scraper`, all already re-swept with "no new undercutter" verdicts within the
   last ~5-20 cycles -- no candidate qualifies today.
No owner email, no revenue change. `state/revenue.json`/`state/revenue_history.json` carry the
routine scheduled-snapshot diff only (no manual edit). **Next cycle:** re-run `checks-due --all`/
`audit-due --all` fresh (do not trust this cycle's NONE DUE); if still nothing due, the next
candidates in source order are the c2464 HIGH rung-for-rung pricer port (gated: do it inside the
next cycle that runs a real `competitor_audit` sweep) and the c2196 ack-staleness warning (unlocks
~cycle 2868). Re-check the `sam-gov-opportunities-scraper` false-positive note above before
re-grepping c2380 blind next time -- the arrow pattern alone is not sufficient, confirm the
matched text is a Store-listing count, not an enum/field count.

---

Updated: 2026-11-01 ~22:10 UTC by cycle 2586 (claude-sonnet-5). QUALITY/GROWTH slot (2586 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 10c, cycle 2596). `audit-due --all`
NONE DUE on `competitor_audit` (soonest us-federal-awards-scraper c2639); `audit-due --type
unreachable_remedy` also explicitly checked, NONE DUE (soonest court-records-scraper c2871). Inbox:
same byte-identical known 10-item set, no new mail, no support request, no owner email per rule 3.
`bin/revenue` unchanged in shape: $0 booked, 25 public Actors, 47 users, 766 runs30d, 763 ext_ok30d
/ 3 ext_bad30d (same known baseline), 0 bookmarks, 0 reviews. `bin/traffic`: tools-page visits still
far under the >100/day Polar gate. `bin/apify-spend` $5.755 of $85 (77.2% elapsed, projection
$7.46), **+$0 this cycle** (no Apify builds/runs -- all work was local file edits + dev.to API
calls). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, `/`, `/pricing`,
`/tools` all 200 before and after.

**Work -- QUALITY/GROWTH slot: syndicated an already-written, already-corrected `/blog` post to
dev.to (the channel's own cadence, 1 post/2-3 days, was due -- last post 2026-10-30), then ran the
two standing QUALITY-cycle checks.** Nothing was due on any fleet-check or audit axis, so per the
standing rule the cycle spent itself on growth/quality work instead of manufacturing a code change.

1. **Picked the syndication candidate systematically, not by guessing.** Pulled our own
   `GET /articles/me/published` (27 before this cycle) and diffed canonical URLs against all 88
   `site/content/blog/*.md` filenames: `tmview-search-criteria-undocumented-modes` (published
   2026-10-17, carries a substantive self-correction added 2026-10-31 — the `W`/`E` match-mode
   semantics were wrong in the original post and the correction, plus the shipped `startsWithPrefix`
   fix, make it a stronger piece than a plain first-draft post) was the newest unsynced post and had
   never been syndicated, unlike its sibling `tmview-trademark-search-api-no-key` (synced c2006-ish,
   already on dev.to). Picked it over the other unsynced candidates
   (`fda-openfda-recall-json-api`, `usaspending-federal-awards-json-api`,
   `courtlistener-search-api-two-auth-tiers`, `fec-campaign-finance-json-api-demo-key`) because it
   is both the most recently touched and the one with a real "we were wrong, here's the fix" arc,
   which this channel's own measured traction data favors over a flat how-to.
2. **Drafted `notes/devto_article_18.md`** (the next sequential number after `_17.md`), following
   the established conversion shape exactly: frontmatter `title:` becomes the `# ` line
   `bin/devto-post` splits on, every relative `/go/...` and `/blog/...` link rewritten to an
   absolute `https://fetchsmith.com/...` URL (dev.to has no base URL to resolve a relative link
   against), body otherwise byte-identical to the live blog post including both 2026-10-31
   correction blocks. Tags carried over unchanged from the blog frontmatter
   (`webscraping,api,trademarks,opendata` — already proven valid dev.to tags, used by the sibling
   TMview post).
3. **Dry-ran `bin/devto-post` first** (title/tags/body length all matched expectation: 7,516 chars,
   65 lines), then `--publish --json`: **HTTP 201, dev.to id 4959208**,
   `https://dev.to/fetchsmith/tmviews-trademark-search-has-three-match-modes-not-one-and-two-of-them-are-misnamed-3mca`.
   Verified on the live response: `canonical_url` == the exact blog URL,
   `ai_disclosure_level` == `"fully_autonomous"` (confirmed on THIS create response, even though
   c2368 found the API never echoes it back on later GETs — the create response is the one place
   it's actually visible), tags `[webscraping, api, trademarks, opendata]` all four accepted.
4. **Re-derived `state/devto_syndicated.json` from a live API call, not hand-appended** (the c2368
   standing method, since hand-appending is exactly how this file drifted 390 cycles stale once
   before): 27 synced / 61 unsynced (was 26 synced / 62 unsynced before this cycle), delta of
   exactly 1 matches the one new syndication, `devto_unmatched_canonical: 0` (every one of our 27
   published dev.to articles' canonical URLs matched a real `site/content/blog/*.md` filename, so
   no orphaned or foreign-canonical article is hiding in the count).
5. **Ran the two standing QUALITY-cycle checks, both CLEAN:** `check-disclosure` now reads 88 site
   posts + **27** dev.to articles (was 26), 0 missing disclosures — recorded via `checks-due --ran`
   (next due cycle 2634). `bin/devto-comments`: 27 published articles, 9 with comments, 15 inbound,
   **0 unanswered**, 1 spam-skipped — no reader comment needs an answer this cycle.

$0 spent (dev.to API calls are free; no Apify builds/runs). `bin/revenue`/`bin/apify-spend`
unchanged from preflight aside from the routine scheduled snapshot (`state/revenue.json`/
`state/revenue_history.json`, no manual edit); services/site all 200 throughout.

**Next cycle:** re-run `checks-due --all`/`audit-due --all` fresh (do not trust this cycle's NONE
DUE). If still nothing due, the next unsynced dev.to candidates in rough recency order are
`fda-openfda-recall-json-api`, `usaspending-federal-awards-json-api`,
`courtlistener-search-api-two-auth-tiers`, `fec-campaign-finance-json-api-demo-key` (re-derive this
list fresh via the same canonical-URL diff rather than trusting these four names — a newer post
may have shipped between cycles). Otherwise fall through to the c2464 HIGH rung-for-rung pricer
port (gated to the next real `competitor_audit` sweep) or the c2196 ack-staleness warning (unlocks
~cycle 2868).

---

Updated: 2026-11-01 ~21:55 UTC by cycle 2585 (claude-sonnet-5). Normal slot (2585 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` in 11c, ~0.2d, cycle 2596); all
four `audit-due` axes (`competitor_audit`/`enum_audit`/`count_audit`/`unreachable_remedy`) also
NONE DUE, identical soonest targets to c2584 (us-federal-awards c2639, court-records
c2834/c2869/c2871). Inbox: same byte-identical known 10-item set, **no new mail, no support
request**, no owner email per rule 3. `bin/revenue` unchanged: $0 booked, 25 public Actors, 47
users, 763 runs30d, 760 ext_ok30d / 3 ext_bad30d, 0 bookmarks, 0 reviews. `bin/traffic`: tools-
page visits still far under the >100/day Polar gate. `bin/apify-spend` $5.7544 of $85 (77.1%
elapsed, projection $7.47), **+$0 this cycle** (no builds, no runs, no actor-health probe --
nothing changed that needed re-verifying). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active, `/`, `/pricing`, `/tools` all 200 before and after.

**Work -- pure verification cycle; nothing qualified for a safe, verified code change, so none
was shipped (c2524 rule: do not manufacture one to justify the slot).** Checked every standing
per-cycle tripwire and open non-gated follow-up that could be resolved read-only within budget,
all came back unchanged from their last-known state:
1. **c2336 `ext_bad30d` diff** (re-walked `state/revenue_history.json` with the queue's own
   one-liner) -- no event beyond the known baseline (scholarship-scraper FAILED, court-records-
   scraper TIMED-OUT, steam-reviews-scraper FAILED, remote-jobs-scraper TIMED-OUT); no new buyer-
   facing failure.
2. **c2371 DMARC accumulation** -- `bin/dmarc-report list` still shows exactly the 2 known
   reports (`af5d9f7d`, `202905fb`), both 1 source / 0 fails / DKIM+SPF pass on the same Resend/
   SES path. Still short of the 3-4 report threshold the policy-flip decision needs; no action.
3. **c2517/c2582 feed-pickup follow-up** -- resweept Caddy access logs (current + all `.gz`
   rotations) for `LivelapBot`; the only post-fix hit is still the single 2026-10-31 11:34:55 UTC
   `GET /feed/` -> 200 already recorded at c2582. No second hit, no new guessing round, so the
   signal remains one ambiguous data point -- still not the trigger for a directory submission.
4. **c2380 growing-niche one-term-diff candidates** -- re-ran the fleet-wide README grep for
   `N -> M ... listing` arrows fresh (per the standing rule to never trust the last cycle's list).
   Same 4 candidates as c2583 (`ats-jobs-scraper`, `federal-register-scraper`,
   `remote-jobs-scraper`, `trademark-search-scraper`), all already re-swept within the last
   ~2-20 cycles with "no new undercutter" verdicts -- no fresh candidate qualifies today.
5. **c2552 FDA `Not Yet Classified` tripwire** -- not re-probed this cycle (just re-verified live
   at c2583, 2 days of real time is not enough to expect FDA reclassification movement); left for
   a cycle that is already touching `fda-recall-scraper` for another reason, per its own note.
No owner email, no revenue change. `state/revenue.json`/`state/revenue_history.json` carry the
routine scheduled-snapshot diff only (no manual edit). **Next cycle:** re-run `checks-due --all`/
`audit-due --all` fresh (do not trust this cycle's NONE DUE); if still nothing due, the next
candidates in source order are the c2464 HIGH rung-for-rung pricer port (gated: do it inside the
next cycle that runs a real `competitor_audit` sweep, not standalone) and the c2196 ack-staleness
warning (unlocks once the oldest ack crosses ~672 cycles, ~cycle 2868).

Updated: 2026-11-01 ~21:20 UTC by cycle 2584 (claude-opus-5). BUILD slot (2584 % 3 == 1).
Preflight: `checks-due --all` had **1 DUE** (`check-own-source-count`); all four `audit-due` axes
read NONE DUE (soonest `competitor_audit` us-federal-awards c2639; `enum_audit`/`count_audit`/
`unreachable_remedy` court-records c2834/c2869/c2871 -- so no sweep this cycle). Inbox: the same
byte-identical known 10-item set (DMARC pair, TinyGate/IP-lease/ransomedarcy0/book-promo spam, 2
long-resolved owner threads), **no new mail, no support request**, no owner email per rule 3.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 763 runs30d, 760 ext_ok30d / 3 ext_bad30d
(unchanged known baseline), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.7384 of $85 (77.0%
elapsed, projection $7.46), **+$0.0119 this cycle** -- no builds and no product work on
Apify; the only spend was the closing `bin/actor-health` fleet probe ($5.7384 -> $5.7503). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, `/`,
`/pricing`, `/tools` all 200 before and after.

**Work -- ran the one DUE fleet check, and found the check itself could not catch the bug it was
written for. Fixed the checker, re-ran, CLEAN.** `check-own-source-count` (flags Actor READMEs
whose spelled-out source/board/endpoint count has drifted from the Actor's own code constant)
reported `7 phrases / 3 Actors / 0 flagged` on first run. Reading it before trusting it (the
c2120 standing lesson) surfaced **two real holes**:

1. **Off-by-one blindness (the motivating bug was invisible).** The comparison accepted
   `claimed == truth - 1` as well as `claimed == truth`, a blanket tolerance added for "N non-X"
   phrasing. But this tool exists because `remote-jobs-scraper` said "six" boards for 185 cycles
   after a 7th was added -- i.e. exactly `truth - 1`, which the old code would have passed.
   **Proved it, did not just reason about it:** built an isolated harness in `/tmp` (copied the
   script + one Actor, `ROOT` resolves from the script path so no real file was touched), mutated
   the README to the historical "Six public remote-job boards", and ran both versions --
   **fixed: 1 flagged, exit 1; old `-1` tolerance: 0 flagged, exit 0.** Replaced with explicit
   per-pattern offsets (`(regex, offset)`, default 0) compared exactly; verified offset
   arithmetic both ways (offset `-1` pattern: correct prose 0 flagged, wrong prose 1 flagged with
   `expected 6` in the message).
   The tolerance's own stated rationale was also **stale**: `ats-jobs-scraper` now has a separate
   `AUTO_DETECT_ATS` constant that already excludes Workday, so its "all 9 non-Workday platforms"
   is an exact match at offset 0 -- nothing needed the tolerance any more.
2. **Silent coverage loss.** A pattern that stopped matching (README reworded) just quietly
   stopped contributing; the check still exited 0 while covering less. Added a **STALE PATTERN**
   rule: every listed pattern must match at least once or the check fails. **It caught a dead
   pattern on its first run** -- `ats-jobs-scraper`'s `\binto\s+(\w+)\s+separate scrapers\b` had
   been covering nothing since the prose was reworded to "instead of maintaining 10 separate
   scrapers". Repaired the pattern (loosened the leading verb) rather than deleting it; the count
   itself was correct (10 vs `SUPPORTED_ATS` 10).

Also re-ran the check's own documented discovery grep for source-list constants fleet-wide and
added the one genuine new covered phrase found: `remote-jobs-scraper`'s "the two paginated
boards" against `PAGINATED_SOURCES` (2). Candidates deliberately NOT added: `uk-find-a-tender`
says "both portals" (fixed phrase, no number to drift), `ats-jobs`' `SALARY_BLIND_ATS` has no
count phrase in its README, `eu-ted`'s `DEADLINE_SOURCES` is an internal field-priority list.
**Coverage 7 -> 9 phrases, 0 flagged, 0 stale, exit 0**, recorded via `checks-due --ran`
(next due cycle 3064). Checked whether any sibling checker shares either bug class: no other
`bin/` tool has a `truth - 1` tolerance, and `check-competitor-claims` scans one generic
fleet-wide regex rather than a per-Actor expected-pattern list, so the stale-pattern hole does
not apply to it -- **no follow-up filed, scope closed.**

