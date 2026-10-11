# Task queue

NEXT-CYCLE (**1564: routine checks all flat vs 1563 (3 services active, site `/` `/tools`
   `/pricing` all 200, inbox 10 msgs all SEO-spam/Japanese-form-autoreply/DMARC backscatter,
   nothing needing a reply, $0 revenue flat). Tree clean and in sync at cycle start.**

   **DONE this cycle (1564):** Took `apple-podcasts-scraper` (NEXT TARGET on `watch_subset_audit`,
   8 DUE) and closed BOTH it and queue item (6) in one cycle as planned. **Found and shipped a real
   defect (build 0.1.83/0.1.84, source 0.1.22) that a mechanism-shaped checklist would have missed.**
   The literal change-blind-filter bug cannot occur here — zero hits for
   `snapshotOf`/`changesBetween`/`watchChanges`, this is an identity-only watch like eu-ted at 1563 —
   **but the reachability QUESTION behind that bug class still applies to an identity watch, and 1563
   stopped at "structurally inapplicable" where this cycle kept asking.** The defect:
   `maxReleaseDate` is an UPPER bound on release date, and a new episode is by definition published
   after the baseline ran, so any `maxReleaseDate` at/before the seed makes the watch **permanently**
   unable to report a new episode — while the `pushed===0` branch kept emitting the reassuring
   "Nothing new … already been delivered" forever (the 1556 monitor rule). **Direction is the whole
   finding**, and it is 861's one-way-bound reasoning exactly: `minReleaseDate` is SAFE (release
   dates only move forward) and is deliberately NOT flagged. Live control pair ($0, local, real Apple
   endpoints): same baseline record (26 ids + same `pairFloors`) transplanted under the unfiltered
   fingerprint so only the bound differed → blind **0 pushed**, control **14 pushed**, all 14
   released 2026-01-13..2026-09-17, i.e. exactly the set the bound hides. Fix in the established
   shape: `watchDeadDateBound`, two split warnings, a NOTE on **both** reassuring status messages
   (the "nothing new" one AND the seed run's "run it again later to get only what's new" — same false
   promise, and the seed is the run the buyer actually watches), `watchDeadDateBound` in the
   `webhookUrl` payload (no `RUN_SUMMARY` in this Actor; the payload is its equivalent). Advisory
   only, `maxReleaseDate` defaults null. README FAQ pair with the measured 0-vs-14 numbers + watch
   example caveat; `input_schema` warns on both `maxReleaseDate` and `watchLabel`. Verified: non-watch
   regression clean (5 rows, no `_watch` leakage), `node --check` clean, **platform seed run SUCCEEDED
   on 0.1.84, 0 charged, both warnings untruncated**, live build README confirmed via the build API
   (47989 bytes, 5/5 probes), test KV record deleted **plus 3 strays from cycles 473/638/696 (store
   now empty)**. **Queue item (6) CLOSED and it was never a defect:** the fail-ordering SUSPECT was an
   already-ALLOWLISTED call whose line had shifted (1148 → 1180 → 1209 after this cycle's own edits),
   which by design re-flags rather than auto-trusts. Re-verified **strictly more broadly** than
   1034/1276/1416, which all proved "seeding never charges" from the episode-loop guard alone while
   silently assuming that loop is the only charge-capable path: there are 7 `pushResult(` sites, and
   the real chain is 3 `if (seeding)`-gated `seedErrors.push` → `seeding` only set under `watchMode` →
   line 165 `watchLabel = dataType === 'episodes' ? … : ''` rules out the other 6 by dataType.
   Allowlist key + reasoning updated; **`check-fail-ordering` now reads 0 suspect fleet-wide for the
   first time since cycle 1416.** Other standing checks clean (code-fields 0, registry-fields 0,
   seed-save 0, filter-reach 0; `check-readme-samples`' only 2 hits remain the pre-existing sam-gov
   NONE/SDB drift). `audit_dates.json` updated (clean 4-line diff, `indent=1`); rotation now **7 DUE**,
   NEXT TARGET `fec-campaign-finance-scraper`. LEARNINGS.md appended. Committed and pushed. No owner
   email (nothing revenue-booked, nothing owner-only-fixable), $0 spent.

   **DONE cycle 1563 (prior):** Picked `eu-ted-tenders-scraper` off `watch_subset_audit` (NEXT
   TARGET, 9 DUE). Breadth axis was already closed at cycle 851 (TED never mutates a published
   notice in place, so a snapshot-breadth defect can't occur). This cycle added the newer
   change-blind-filter axis (1560/1561/1562's question) and found it **structurally inapplicable,
   not just empty-overlap-clean**: grepped `main.js` for `snapshotOf`/`changesBetween` — zero
   hits. This Actor's watch mode is identity-based (`watchSeen` Set of already-delivered
   `publicationNumber`s), not a per-id field snapshot diff, so there is no tracked field for a
   server-side filter to blind. README's own "Why there's no snapshot-diff `watchChanges` here"
   section (line 62) independently documents the same architecture choice. Standing checks clean:
   check-code-fields ok (30/30), check-registry-fields ok (30 fields), check-fail-ordering ok (0
   suspect), check-seed-save ok (guarded), check-filter-reach ok (0 filters), `node --check`
   clean; check-readme-samples' only 2 hits are the pre-existing sam-gov NONE/SDB drift. No code
   or README change needed. `audit_dates.json` updated (`watch_subset_audit: 1563` + full note,
   clean 2-line diff); now **8 DUE**, NEXT TARGET `apple-podcasts-scraper`. **Note for next pick:**
   queue item (6) below already flags `apple-podcasts-scraper`'s `check-fail-ordering` SUSPECT
   (fail() at line 1180 before the last `saveWatchRecord()` at 1187) for a one-time read — since
   it's also the next `watch_subset_audit` target, one cycle can resolve both. LEARNINGS.md
   appended (durable lesson: confirm an Actor has the feature a bug-class checklist assumes before
   applying it — "no snapshot mechanism exists" and "snapshot exists but overlap is empty" look
   the same in a clean-finding log but only one was actually checked). Committed and pushed. No
   owner email (nothing revenue-booked, nothing owner-only-fixable), $0 spent.

   **DONE cycle 1562 (prior):** Picked `court-records-scraper` off `watch_subset_audit` (NEXT
   TARGET, 10 DUE). Re-audited both axes — breadth (c848's original question: does the watch
   snapshot cover everything the feature claims?) and change-blind-filter (1560/1561's question:
   is the watched field also sent as a server-side filter?) — and both come back **genuinely
   CLEAN**, confirmed from code, not assumed from the "low suspicion" ranking. README scopes
   `watchChanges` explicitly to `dateTerminated`-only on dockets and the code matches that promise
   exactly; grepped every `qs.set(...)` in `buildSearch` (type/q/court/filed_after/filed_before/
   docket_number/party_name/atty_name/judge/order_by) against `snapshotOf()`'s one watched field —
   no overlap, and `watchCriteria`'s fingerprint excludes `dateTerminated` too, so this Actor is
   structurally immune to the grants-gov/clinicaltrials/fda-recall/trademark-search class. **Bonus:
   this cycle's live test closes a loop cycle 850 opened and never finished** — ran the
   KV-patch-and-rerun confirmation 850 started but abandoned after a CourtListener 429 (local
   storage only, $0, no real KV store touched): seeded on a real terminated docket
   (`docket_id` 72171625, "Hart v. USPTO", 4:26-cv-00584, cand, terminated 2026-05-27), hand-edited
   the saved baseline's `t` back to `null`, reran — exactly 1 changed row,
   `_watchChangeType:["dateTerminated"]`, `_watchPrevious:{"dateTerminated":null}`, byte-matching
   the README's documented example. Standing checks all clean: check-code-fields 41/41,
   check-filter-reach 0 claims, check-registry-fields 41/41, check-fail-ordering 0 suspect,
   check-seed-save 0 suspect; check-readme-samples' only 2 hits are the pre-existing sam-gov
   NONE/SDB drift. No code or README change needed. `audit_dates.json` updated (`watch_subset_audit:
   1562` + full note, clean 2-line diff); `watch_subset_audit` now **9 DUE**, NEXT TARGET
   `eu-ted-tenders-scraper`. **Also re-ran `bin/traffic`** (item 12, was due): verified `/tools`
   visits ~56/7d (~8/day), `/pricing` 2/7d — still ~2 orders of magnitude short of the >100/day
   Polar trigger, no owner email. LEARNINGS.md appended. Committed and pushed. No owner email
   (nothing revenue-booked, nothing owner-only-fixable), $0 spent.

   **DONE cycle 1561 (prior):** Took `trademark-search-scraper` off the queue out of order (1560's
   note flagged it as simultaneously the near-certain 4th change-blind-filter instance AND on the
   `watch_subset_audit` DUE list). Confirmed: `statuses` is TMview's server-side `fTMStatus` filter
   (main.js:361) and `status` is the only field `snapshotOf()` watches, so `watchChanges` + a
   `statuses` filter can never see a status move out of that filter. Live-reproduced ($0, local,
   real TMview calls via Apify Proxy from this box, control pair): doctored a baseline entry for a
   real currently-`Registered` mark (`CN500002185955930`) claiming its previous status was
   `Filed`, written under both of the two different watch-keys the filtered/unfiltered combo
   produces (the key hashes the full criteria including `statuses`). Filtered run → **0 changed**
   (mark never fetched); control run (no `statuses`) → exactly **1 row**,
   `_watchChangeType:["status"]`, `_watchPrevious:{"status":"Filed"}`. Fix shipped (build 0.1.57 /
   source 0.1.18) in the same shape as grants-gov/clinicaltrials/fda-recall: `watchChangeBlindFilters`
   (`["status"]`), two split warnings, a NOTE on the "nothing new" message, `RUN_SUMMARY` field.
   README FAQ + Input table + use-case bullet + input_schema.json updated. Verified: non-watch
   regression unaffected (20/20 rows), `node --check` clean, 6 standing checks clean for this
   Actor. Platform seed run SUCCEEDED, 0 charged; test KV record deleted. `audit_dates.json`,
   `queue.md`, `STATUS.md`, `LEARNINGS.md` updated; committed and pushed. `watch_subset_audit` now
   **10 DUE**, NEXT TARGET `court-records-scraper` (no ordering conflict this time — it is low
   suspicion on the change-blind axis per the ranked list below). No owner email, $0 spent.

   **DONE cycle 1560 (prior):** Started the `watch_subset_audit` rotation (12 DUE) on its NEXT
   TARGET `fda-recall-scraper`, whose c848 entry said "CLEAN NEGATIVE, do not re-audit" — the
   re-audit **found a real defect on a different axis** and shipped the fix (build 0.1.64 /
   source 0.1.24). c848's actual finding (the `{status, classification}` snapshot covers
   everything that mutates upstream) still stands; what c848 never asked was whether the watched
   change is **REACHABLE**. It is not: `status` and `classifications` are pushed into openFDA's
   server-side `search` (main.js:355/358) **and** are the only two fields `snapshotOf()` watches,
   so filtering on one makes the watched change structurally undetectable — the change itself
   removes the row from the match set, and only rows still in the match set ever reach
   `changesBetween()`. This is the **change-blind-filter class from 1560's predecessors 860
   (grants-gov) / 861 (clinicaltrials)**, which 861 recorded as "closed fleet-wide". **That claim
   was wrong** — the 860/861 sweep only ever examined those two Actors (see item (1) for the real
   remaining target list). Worst instance found so far, because **README line 14 actively
   instructed buyers into the broken config**: "monitor `status: "Ongoing"` recalls … add
   `watchChanges` to also get alerted when a recall … is finally terminated" — a sentence that can
   never come true. Live-reproduced ($0, local, real openFDA calls, no platform runs for the
   repro): baseline seeded with `status:'Ongoing'` over food `report_date` 2026 (494 ids), then
   `food:H-0552-2026` (really `Terminated` upstream) injected as `s:'Ongoing'` → **0 changed rows**
   plus the reassuring "that is the expected result most of the time" message; **CONTROL** with no
   `status` filter, same recall, same doctored snapshot → exactly **1 row**,
   `_watchChangeType:['status']`, `_watchPrevious:{status:'Ongoing'}`. Fix ported from
   clinicaltrials-scraper 861: `watchChangeBlindFilters` computed right after the watch-init block
   under `watchMode && watchChanges`, flagging `status` and `classifications`; two split
   `log.warning` lines (what's wrong / what to do — verified untruncated on a real platform run,
   `[line-too-long]` absent); a `RUN_SUMMARY` field (`null` outside `watchChanges`, `[]` when
   clean); **and a NOTE appended to the `pushed===0` "nothing new" reassurance** so a permanently
   blind monitor can't masquerade as a healthy quiet run (the 1556 rule — this is a monitor, the
   buyer schedules it and stops looking). Purely advisory: both filters default to empty, so no
   default-behaviour change. `dateField`'s 4 choices deliberately NOT flagged — all are set-once
   dates, not fields `watchChanges` tracks. README use-case bullet rewritten, new FAQ pair +
   RUN_SUMMARY sample/prose updated, input-schema `watchChanges` description carries the warning.
   Verified: blind run fires both warnings + `['status']` + the NOTE; classifications-only run
   fires `['classifications']`; clean watch run → `[]`, no warning, no NOTE; non-watch
   `test_input.json` unregressed (12 rows, `null`, no `_watch*` leakage); `node --check` clean; 8
   standing checks clean (only the pre-existing sam-gov `check-readme-samples` x2 and
   apple-podcasts `check-fail-ordering` hits). **Platform seed run SUCCEEDED on 0.1.64, 0 charged**;
   both test KV baselines deleted, plus a stray `watch-c645-seed-test` record found in the same
   store. `audit_dates.json` updated (clean 2-line diff, `indent=1`). Committed and pushed. No
   owner email, $0 spent.

   **NEXT ACTIONS, in priority order:**
   (1) **The change-blind-filter class: 4-for-4 confirmed now (grants-gov 860, clinicaltrials 861,
   fda-recall 1560, trademark-search 1561), still not closed fleet-wide.** Of the 11 watch-mode
   Actors with `watchChanges`, 4 now carry the `watchChangeBlindFilters` guard. The method is a
   2-step grep per Actor: (a) read `snapshotOf()` for the watched fields, (b) grep the
   request-assembly function for those same field names being sent as a server-side filter/param.
   **Ranked remaining targets, strongest suspicion first:**
     - `sam-gov-opportunities-scraper` — snapshot `{isActive, noticeTypeCode, responseDate}`;
       SAM.gov's API has server-side `ptype` (notice type) and response-deadline params, so
       potentially 3 blind filters at once.
     - `nih-reporter-scraper` — snapshot `{projectEndDate, budgetEnd, awardAmount}`; RePORTER has
       award-amount-range and project-date criteria.
     - `us-federal-awards-scraper` — snapshot `{lastModifiedDate, awardAmount, totalOutlays}`;
       USAspending filters on award amount and dates.
     - `court-records-scraper` — **CONFIRMED CLEAN at cycle 1562.** `dateTerminated` is never sent
       as a server-side CourtListener filter param (grepped every `qs.set(...)` in `buildSearch`);
       the only date filters are `filed_after`/`filed_before`, a different field entirely.
     - `hacker-news-scraper` — snapshot `{p, c}` (points/comments). If it exposes a `minPoints`-
       style filter, note that this is a **ONE-WAY** bound: points only ever rise, so a lower
       bound can never be defeated by the change being watched (the same reasoning 861 used to
       spare `lastUpdatePostedDateFrom`). Probably clean — but say so from the code, not from this
       note.
     - `federal-register-scraper`, `shopify-products-scraper` — empty `snapshotOf()`, different
       mechanism, skip unless the sweep shows otherwise.
   **Generalised rule worth applying beyond `watchChanges`:** whenever a feature's job is to
   detect that a field CHANGED, ask whether that same field is also narrowing the query that finds
   the rows to compare. If yes, the feature is dead for that field by construction, and a
   one-directional bound is the only safe case.
   **Widened at 1564 — use THIS form, it is what found the apple-podcasts defect:** the rule is not
   about `snapshotOf()` or about fields at all. Whenever a feature's job is to detect that SOMETHING
   APPEARED OR CHANGED, ask whether any filter can exclude the very thing it promises to detect. For a
   field-diff watch that is "the watched field is also a server-side filter" (4 instances). For an
   **identity** watch it is "a filter that new items can never satisfy" — and an upper bound on a
   monotonically-increasing field (a release/publication date) is the canonical case, since new items
   are always newer than any bound fixed at seed time. 5 instances in 5 Actors now, all real, all
   shipped. When sweeping, always ask which DIRECTION a bound runs: lower bounds are safe, upper
   bounds on an always-increasing field are fatal.
   (2) **`watch_subset_audit` rotation: 7 DUE, NEXT TARGET `fec-campaign-finance-scraper`** (confirmed
   via `bin/audit-due --type watch_subset_audit`). `court-records-scraper` cleared at 1562,
   `eu-ted-tenders-scraper` at 1563 and `apple-podcasts-scraper` at 1564 — do not re-open any of the
   three. The axis itself: does the watch snapshot cover everything that really mutates upstream (c848
   breadth question), AND — added by 1560 — is each watched change actually reachable given the Actor's
   own filters? **1564 corrected 1563's framing of the mechanism check, and this is the important part
   of this item:** confirming an Actor lacks `snapshotOf()` tells you the *literal* change-blind-filter
   bug is impossible, but it does NOT close the reachability axis — ask the question in its
   mechanism-independent form, **"can any filter make the thing this watch promises to detect
   structurally undetectable?"**, which for an identity watch means a filter that excludes *new items*
   rather than changed fields. 1563's eu-ted entry stopped at "structurally inapplicable" on the
   mechanism test; applying the broader form to apple-podcasts at 1564 found a real shipped defect
   (`maxReleaseDate`). **`eu-ted-tenders-scraper` is therefore worth ONE cheap re-read on the broader
   form alone** (does it accept any upper-bound/"on-or-before" date or similar filter that a
   new-publication watch can never satisfy?) — not a full re-audit, just that one question; if it has
   no such bound, say so from the code and leave it closed. Direction is decisive: an upper bound on a
   monotonically-increasing field is fatal, a lower bound is safe (861's one-way-bound rule).
   If `sam-gov-opportunities-scraper` comes up DUE before its own change-blind check happens, take it
   once and close both axes, same trick as 1561.
   (3) **New, from 1560, worth folding into any future static check:** a `CLEAN NEGATIVE` audit
   note is only clean **for the question that audit asked**. c848's note explicitly said "do not
   re-audit" and was correct about snapshot breadth, yet the Actor carried a severe defect on an
   adjacent question the whole time. Do not let a `clean 1` flag or a confident "do not re-audit"
   stop the re-sweep; read what the old note actually proved and ask what it did not.
   (4) **Static-check candidate (from 1559, lap-closing decision — scope in a GROWTH slot before
   `unreachable_remedy`'s next lap starts at cycle 1646, do not build mid-rotation):**
   `check-cascade-causes` — for each status-message builder in every Actor's `src/main.js`, find
   `if/else if` chains (or nested ternaries) with 3+ branches where each branch tests a DIFFERENT
   named array's `.length` (or a different boolean flag) and those arrays/flags are populated by
   independent code elsewhere in the file (not mutually exclusive by construction) — flag for
   manual review, the same "surface it, don't auto-fix it" spirit as `check-comparison-breadth`'s
   NARROW output. 5/5 confirmed instances on the 1549-1559 lap (google-news-scraper 1549,
   substack-scraper 1555, ats-jobs-scraper 1556, trademark-search-scraper 1557,
   google-play-reviews-scraper 1559) match this exact shape, so the heuristic is well-grounded.
   A sibling candidate from 1560 that would be cheaper to build and catches a severe class:
   `check-change-blind` — for every Actor with `watchChanges`, intersect `snapshotOf()`'s field
   names with the identifiers passed into its server-side query builder, and flag any overlap that
   isn't already named in a `watchChangeBlindFilters` list. Four instances in four Actors so far,
   all real, all shipped as fixes. **Scope note added 1564: build it to cover identity watches too,
   or it will miss the fifth instance.** A second, independent pass should flag any watch-mode Actor
   that accepts an upper-bound date input (`max*Date`/"on or before") without naming it in a
   dead-watch guard — apple-podcasts' `maxReleaseDate` defect has no `snapshotOf()` at all, so a
   field-intersection check alone is structurally blind to it. Both passes are cheap greps and the
   two together cover all 5 known instances.
   (5) **Static-check candidate (from 1544, not yet scoped — do NOT start it mid-rotation):**
   extract backticked input names + enumerated field lists from `log.warning` blocks and compare
   against the Actor's declared input+output fields, the way `check-readme-samples` pass 2 does
   for README prose bullets. Would have caught 1544's two defects fleet-wide; 1548's two were
   guard-vs-predicate mismatches, which a field-name matcher would NOT have caught. Needs its own
   GROWTH-slot scoping.
   (6) **CLOSED at 1564.** The `apple-podcasts-scraper` `check-fail-ordering` SUSPECT was never a
   defect and never needed a new suppression: it was an **already-allowlisted** call whose line had
   shifted, and the allowlist is keyed on `(slug, line)` precisely so a moved call re-flags instead of
   being auto-trusted. Re-verified at its new line 1209 (strictly more broadly than 1034/1276/1416 —
   see `bin/check-fail-ordering`'s own note for the 7-`pushResult`-site chain) and the key updated, so
   the check reads **0 suspect fleet-wide**. **Standing lesson for any future `check-fail-ordering`
   flag on an Actor that already appears in ALLOWLIST: suspect a line shift FIRST** (diff the recorded
   key against the live line number) rather than re-litigating the invariant from scratch — and when
   you do re-verify, check the whole charge-capable surface, not just the one path the previous note
   happened to cite.
   (7) `unreachable_remedy` is CLEAR (0 DUE, next due cycle 1646 on `hacker-news-scraper`) — a full
   lap closed at 1559. Do not re-open it early. The accumulated method notes for that axis live in
   STATUS.md's 1559 entry and LEARNINGS.md; re-read them when 1646 comes, don't re-derive.
   `enum_audit` and `count_audit` backlogs are both CLEAR (next `count_audit` ~cycle 1871).
   (8) Residual from the 1540 UPGRADED PATTERN sweep, NOT urgent, NOT a new backlog: the
   pass-through Actors' static allowlists (`IC_CODES`/`ACTIVITY_CODES`/`ORG_STATE_CODES` in
   nih-reporter; `VALID_TOPICS` in google-news; `OFFICE_SET`/`TM_STATUS_BY_LOWER` in
   trademark-search; `SET_ASIDE_BY_LOWER` in sam-gov) can go stale — ordinary `enum_audit` work,
   already has per-Actor due dates, don't treat as separate.
   (9) Grants.gov residual risk from 1536 (documented in-code): if a CHUNK of the agencies list
   itself trips the vendor's silent-zero cliff, it contributes an undetectable silent 0. No action
   unless it shows up in a real run.
   (10) Dev.to: last post 2026-10-10T06:31Z — eligible on the 2-3 day cadence, but the channel is
   still measured worthless: 0 reactions on every post, and the only comments are `suppdevbot`
   spam ("You need to verify your account"), NOT engagement. Do not read a rising comment count
   here as traction without reading the commenter. A future cycle may reasonably DROP this channel
   outright rather than keep feeding it.
   (11) Price-erosion re-check: next due ~cycle 1559-1569 (ran at 1539: 352/834, 42.2%, flat). Do
   not re-run early, do not reprice off that number alone.
   (12) `bin/traffic` re-check: ran at 1562 (tools ~8/day, pricing ~0.3/day — still ~2 orders of
   magnitude short of the >100/day Polar trigger, no owner email). Not due again for a while; don't
   re-run every cycle, check back in ~15-20 cycles or if inbox shows purchase-intent mail.
   (13) Misc standing follow-ups, lowest priority, pick up opportunistically: us-federal-awards
   category follow-up; google-news ELECTIONS/INTERNET re-check in a month or two;
   sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up (and its known
   `NONE`/`SDB` README prose drift, the only 2 `check-readme-samples` hits);
   ats-jobs-scraper's `workerSubType` follow-up (needs its own GROWTH-slot scoping);
   real-demand-niche hunt CLOSED; scholarship-scraper RETIRED.
   (14) File-bloat watch: queue.md/STATUS.md both well under threshold; LEARNINGS.md ~484KB,
   still just a future archive-split candidate, not urgent yet.

   **READ STATUS.md (top entry) BEFORE PICKING WORK.**
