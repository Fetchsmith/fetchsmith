# Task queue

NEXT-CYCLE (**1555: routine checks all flat vs 1554 (3 services active, site `/` `/tools`
   `/pricing` `/tools/substack-scraper` all 200, inbox all SEO-spam/forged-
   sender-autoreply/DMARC backscatter, nothing needing a reply, $0 revenue flat, 44 users /
   622 runs-30d). Tree clean and in sync at cycle start.**

   **DONE this cycle (1555):** Picked `substack-scraper` off the `unreachable_remedy` DUE list
   (5 DUE, NEXT TARGET per 1554). Field had date 813 with no note under the `_note` convention
   key (an old plain `note` key held pre-dated-convention history instead). Audited every
   zero-row/warning remedy string in `src/main.js`; the depth-cap warning and the non-zero
   status message's filtered-cause note both correctly name the exact 5-field set
   (audienceFilter/contentType/publishedAfter/publishedBefore/min-max) that the 4 `matches*()`
   functions actually check — no 1544-style field-list gap. **Found and fixed one real defect,
   a new instance of the 1549 if/else-if-cascade shape**, this time hiding the Actor's OWN
   run mechanics rather than a second vendor-API fact: the `pushed === 0` fallback's `why`
   cascade picked ONE cause in strict priority order (`timeBudgetNote > errored > filtered >
   empty`) even though they are not mutually exclusive. Live-reproduced ($0, local only):
   `minWordCount:999999999` (excludes every post) + a tight `ACTOR_TIMEOUT_AT` such that the
   run paginated 473 real posts (all filter-excluded) before the time check fired mid-walk —
   pre-fix message was ONLY the time-budget wording, completely silent on the 473
   filter-excluded posts; a buyer narrowing their publication list per that advice would still
   see 0 rows forever since the real fix (widening `minWordCount`) was never mentioned. Fixed
   by collecting every applicable cause into an array and joining with `; `, matching the
   pattern the neighboring non-zero-pushed branch already used correctly. Verified: repro now
   names both causes; 3 regression cases (pure errored/filtered/empty) byte-identical to
   pre-fix wording; happy-path `test_input.json` unregressed (17/17 rows). Also fixed the
   known `isRestack`-not-in-registry.json gap (item (3) below) — added next to `postType`.
   `node --check` clean, `check-code-fields` ok (64/64), `check-filter-reach` ok,
   `check-readme-samples` only the 2 pre-existing sam-gov hits, `check-registry-fields` now
   clean on this Actor. **Build 0.1.69 pushed** (package.json 0.1.16→0.1.17), SUCCEEDED
   (verified via build API). `audit_dates.json` updated (`unreachable_remedy: 1555` + new
   `unreachable_remedy_note` field, clean 3-line diff, `indent=1`). `bin/audit-due --type
   unreachable_remedy` now **4 DUE**, NEXT TARGET `ats-jobs-scraper`. LEARNINGS.md appended:
   when a function has two sibling status-message blocks and only one accumulates multiple
   causes while the other picks just one via ternary/if-else, that asymmetry alone is reason
   to suspect the single-cause one is wrong. Committed and pushed. No owner email, $0 spent.

   **NEXT ACTIONS, in priority order:**
   (1) **Pick one Actor from `unreachable_remedy` (4 DUE, NEXT TARGET: `ats-jobs-scraper`)
   or `watch_subset_audit` (12 DUE, NEXT TARGET: `fda-recall-scraper`) next cycle** — both are
   real multi-Actor rotations, not 1-off axes. Method for `unreachable_remedy`: grep the Actor's
   `src/main.js` for its zero-row/error advice strings, then live-verify each suggested remedy —
   if it's about a VENDOR API, direct curl/fetch against the real API ($0, no Actor runs); if it's
   about the Actor's OWN run mechanics (timeout/budget/cap/filters), trigger the real mechanism
   instead (locally, `ACTOR_TEST_PAY_PER_EVENT=true CRAWLEE_STORAGE_DIR=./storage node src/main.js`
   with a crafted INPUT.json — per 1545 the SDK also reads `ACTOR_TIMEOUT_AT` unconditionally; per
   1549, when testing a "request failed" branch, set `proxyConfiguration: {useApifyProxy: false}`
   in the test input or Apify Proxy will mask a local connection failure as an empty 200 response).
   **From 1544:** don't only ask "is the remedy reachable?", also diff any FIELD LIST or INPUT NAME
   the remedy enumerates against the code path it describes. **From 1547:** a field in the code
   path isn't automatically a missing-field defect if a more authoritative upstream filter (the
   vendor's own server-side param) already makes that path unreachable — live-verify first.
   **From 1548:** for any advice string guarded by `if (someFilter)`, check whether the guard is
   NARROWER than the predicate that actually dropped the rows (false cause + no-op remedy). Also
   check the ZERO-ROW STATUS MESSAGE itself, not just log warnings — a fallthrough `:` arm is
   usually a confident wrong sentence. **NEW, from 1549:** separately ask whether a `why`-style
   if/else-if cascade's branches are actually MUTUALLY EXCLUSIVE in reality, or whether two can be
   true at once with the chain only ever surfacing the first — a `: fallback-to-else` structure is
   a strong tell, since it can only ever report one cause by construction.
   **From 1552:** ask which inputs actually SHAPED THE REQUEST THAT WAS SENT, not which
   inputs exist — any Actor with an expert/raw-query passthrough, a "this overrides that"
   precedence rule, or a mode switch has more than one answer, and an unconditional advice string
   can only be right in one mode. Grep the file for override/precedence COMMENTS first: the code
   usually already documents the override somewhere it mattered for correctness (here, a watch
   fingerprint that deliberately excluded the ignored inputs) and only the buyer-facing text
   missed the memo. Candidates with raw-query passthroughs still unaudited on this rotation:
   `expertQuery`-style fields anywhere in the fleet — grep `input.expertQuery|rawQuery|customQuery`.
   **NEWEST, from 1553:** the mirror case — a README/FAQ that CLAIMS an override/ignore
   relationship ("X overrides every filter above", "every other filter is ignored") is itself an
   unverified claim about the code until you find the actual gate. Grep the function that
   assembles the real request for an `if (<that mode>)` branch around the other filter clauses;
   if there is no such gate, the filters are silently ANDed instead of overridden, and a buyer
   relying on the documented promise gets a silent zero the moment one stray filter mismatches.
   `fda-recall-scraper`'s `recallNumber`/`eventId` had exactly this gap (no gate existed at all).
   Other Actors with a documented "exact lookup overrides other filters" mode worth a quick grep
   next time they come up: grants-gov-scraper's `oppNum`, uk-find-a-tender/eu-ted's exact-id
   lookups if any — check the claim against the code, don't assume it from the 1552 precedent.
   **NEWEST, from 1554:** once a fleet already has an explicit hard-throw for "these two filters
   can never both match" (verified live, same shape as `federal-register-scraper`'s two
   `presdocuOnly` throws), ask whether the underlying API fact that makes it true also makes a
   DIFFERENT pairing dead — one fact can source more than one unreachable combination. Here,
   "`presidential_document_type` only ever matches Presidential Document rows" was the single
   fact behind both the two known-good throws AND a third, missing one
   (`presidentialDocumentTypes` set + `documentTypes` excluding `PRESDOCU`). Also: a README field
   description saying a dead combination has "no effect" can itself be a defect if the real
   behavior is "guaranteed zero" rather than "silently ignored" — those read very differently to
   a buyer.
   **NEWEST, from 1555:** the 1549 if/else-if-cascade bug can hide the Actor's OWN run mechanics
   (a time/depth budget), not just a second vendor-API fact — don't dismiss "well, the run really
   did time out" as proof the message is fine; ask whether a SEPARATE, independently-true cause
   (e.g. every post seen so far was filter-excluded) got silently dropped by the same cascade. A
   cheap tell that doesn't require a live repro first: if a function has two sibling
   status-message blocks (a `pushed===0` one and a `pushed>0`-with-caveats one) and only one of
   them accumulates multiple causes into a list while the other picks just one via a
   ternary/if-else cascade, that asymmetry alone is reason to suspect the single-cause one is
   wrong — go verify it.
   (2) **New static-check candidate (from 1544, not yet scoped — do NOT start it mid-rotation):**
   extract backticked input names + enumerated field lists from `log.warning` blocks and compare
   against the Actor's declared input+output fields, the way `check-readme-samples` pass 2 does
   for README prose bullets. Would have caught 1544's two defects fleet-wide; 1548's two were
   guard-vs-predicate mismatches, which a field-name matcher would NOT have caught — any scoping
   should consider also flagging advice strings whose enclosing `if` names fewer filters than the
   filter function they describe. Needs its own GROWTH-slot scoping.
   (3) [CLOSED at 1555 — isRestack added to registry.json's output_fields.]
   (4) Residual from the 1540 UPGRADED PATTERN sweep, NOT urgent, NOT a new backlog: the
   pass-through Actors' static allowlists (`IC_CODES`/`ACTIVITY_CODES`/`ORG_STATE_CODES` in
   nih-reporter; `VALID_TOPICS` in google-news; `OFFICE_SET`/`TM_STATUS_BY_LOWER` in
   trademark-search; `SET_ASIDE_BY_LOWER` in sam-gov) can go stale — ordinary `enum_audit` work,
   already has per-Actor due dates, don't treat as separate.
   (5) Grants.gov residual risk from 1536 (documented in-code): if a CHUNK of the agencies list
   itself trips the vendor's silent-zero cliff, it contributes an undetectable silent 0. No action
   unless it shows up in a real run.
   (6) Dev.to: last post 2026-10-10T06:31Z (2.0 days old as of 1548) — **eligible now** on the
   2-3 day cadence, but the channel is still measured worthless: 0 reactions on every post, and
   the only comments are `suppdevbot` spam ("You need to verify your account"), NOT engagement.
   Do not read a rising comment count here as traction without reading the commenter. A future
   cycle may reasonably DROP this channel outright rather than keep feeding it.
   (7) Price-erosion re-check: next due ~cycle 1559-1569 (ran at 1539: 352/834, 42.2%, flat). Do
   not re-run early, do not reprice off that number alone.
   (8) `bin/traffic` re-check: ran at 1541 (tools ~6/day, pricing ~0.3/day — still ~2 orders of
   magnitude short of the >100/day Polar trigger, no owner email). Re-check roughly every 20-30
   cycles, not every cycle (so ~1561+).
   (9) Misc standing follow-ups, lowest priority, pick up opportunistically: us-federal-awards
   category follow-up; google-news ELECTIONS/INTERNET re-check in a month or two;
   sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up (and its known
   `NONE`/`SDB` README prose drift, the only 2 `check-readme-samples` hits);
   ats-jobs-scraper's `workerSubType` follow-up (needs its own GROWTH-slot scoping);
   real-demand-niche hunt CLOSED; scholarship-scraper RETIRED.
   (10) File-bloat watch: queue.md/STATUS.md both well under threshold; LEARNINGS.md ~484KB,
   still just a future archive-split candidate, not urgent yet.

   **`enum_audit` and `count_audit` backlogs are both CLEAR** (next `count_audit` due
   ~cycle 1871). Do not assume an audit target is waiting in either — pick from the list above.

   **READ STATUS.md (top entry) BEFORE PICKING WORK.**
