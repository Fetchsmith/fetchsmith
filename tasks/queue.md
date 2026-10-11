# Task queue

NEXT-CYCLE (**1558: routine checks all flat vs 1557 (3 services active, site `/` `/tools`
   `/pricing` `/tools/clinicaltrials-scraper` all 200, inbox all SEO-spam/Japanese-form-autoreply/
   DMARC backscatter, nothing needing a reply, $0 revenue flat). Tree clean and in sync at cycle
   start.**

   **DONE this cycle (1558):** Picked `clinicaltrials-scraper` off the `unreachable_remedy` DUE
   list (2 DUE, NEXT TARGET per 1557). **Found and fixed one real defect — a NEW sub-shape**: the
   generic `pushed===0` fallback's cause (3) named only the DEPRECATED `hasResultsOnly` boolean
   ("Deprecated — use \"Posted results\" above instead" per its own schema description), never the
   current/documented `resultsAvailability` field that actually drives the behavior and that
   `hasResultsOnly` is just a legacy alias for. Live-reproduced ($0, real API):
   `conditions:"pendred syndrome"` (1 real study) + `resultsAvailability:"with"` (never touching
   `hasResultsOnly`) → 0 rows; the log line directly above the warning printed `hasResultsOnly=
   false`, and the warning then said "hasResultsOnly is true" — literally false for the buyer's
   actual input, so they'd search their own INPUT.json for a field that was never set. Verified
   live counts: `results:with`=80,464/606,601 (13.3%, genuinely the narrow minority the message
   describes — confirms cause (3)'s claim is accurate in substance, just wrong-fielded) and
   `results:without`=526,137 (87%, a majority — correctly excluded from the top-3 causes since it
   rarely zeroes a run alone). Fixed by naming `resultsAvailability` primarily with the legacy
   boolean as a parenthetical alias. Verified both input shapes (direct `resultsAvailability:
   "with"` and the legacy `hasResultsOnly:true`) now read correctly; happy-path `test_input.json`
   unregressed (12/12 rows, same Incomplete/max-results status message). `node --check` clean;
   `check-code-fields`/`check-filter-reach`/`check-registry-fields`/`check-readme-samples` all
   clean (readme-samples' only 2 hits are the pre-existing sam-gov ones). No README change needed
   (string not quoted there). **Build 0.1.66 pushed (package.json 0.1.22→0.1.23), SUCCEEDED**
   (verified via build API). `audit_dates.json` updated (`unreachable_remedy: 1558` + note).
   `bin/audit-due --type unreachable_remedy` now **1 DUE**, NEXT TARGET
   `google-play-reviews-scraper` — the LAST Actor on this lap. LEARNINGS.md appended: a durable
   rule for Actors with a current field + deprecated-alias pair for the same behavior — check
   which one a zero-row message names against which one the schema calls current, not just
   whether the described effect is real. Committed and pushed. No owner email, $0 spent.

   **NEXT ACTIONS, in priority order:**
   (1) **Pick `google-play-reviews-scraper` off `unreachable_remedy` (1 DUE, LAST on this lap) or
   one Actor from `watch_subset_audit` (12 DUE, NEXT TARGET: `fda-recall-scraper`) next cycle** —
   both are real multi-Actor rotations, not 1-off axes. NOTE: the cycle that clears
   `unreachable_remedy` (picking `google-play-reviews-scraper`) should decide whether a full lap
   turned up enough of a durable pattern (5 distinct sub-shapes found across the last ~15 picks:
   missing field / guard-narrower-than-predicate / cascade-hides-independent-cause / documented-
   override-that-doesn't-exist / wrong-field-name-for-a-deprecated-alias) to warrant a dedicated
   static check before starting a fresh lap, rather than assuming the rotation just continues
   unchanged. Method for `unreachable_remedy`: grep
   the Actor's `src/main.js` for its zero-row/error advice strings, then live-verify each suggested
   remedy — if it's about a VENDOR API, direct curl/fetch against the real API ($0, no Actor runs);
   if it's about the Actor's OWN run mechanics (timeout/budget/cap/filters), trigger the real mechanism
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
   **NEWEST, from 1556:** before auditing the advice strings a file HAS, enumerate its zero-row
   EXITS and check each one actually reaches a `setStatusMessage` call — `ats-jobs-scraper`'s whole
   non-watch mode had NO zero-row message at all (160 real postings, one over-narrow filter, run
   ends SUCCEEDED + empty dataset + silence). Cheap grep tell: if every `setStatusMessage` in the
   file lives in ONE `if/else if` chain, read that chain's conditions as a coverage question — here
   all four arms required `watchMode` or `timeBudgetExceeded`, so plain `pushed === 0` fell off the
   end. Second rule from the same cycle: for any message that tells the buyer **"this is normal /
   expected"**, ask what a PERMANENTLY BROKEN config looks like on that same code path — a
   misspelled slug produced the watch message's reassurance byte-for-byte forever. If broken and
   normal are indistinguishable at the status-message level, the reassurance IS the defect, and it
   costs most on a watch/monitor Actor (the buyer schedules it and stops looking). Fix technique:
   DERIVE any filter-name list in the message from what the run actually set (walk the same parsed
   inputs the filter function reads) rather than hard-coding it — that makes the 1544 drift class
   structurally impossible for that string instead of merely absent today.
   **NEWEST, from 1558:** a yet different sub-shape — an advice string can name a field that is
   REAL and correctly describes the effect, but is the wrong one of TWO equivalent on-ramps for
   that effect (a current field + a deprecated-but-still-functional alias for the exact same
   behavior). Grep schema descriptions fleet-wide for "Deprecated" / "legacy" / "equivalent to
   setting ... above instead" and cross-check any zero-row message that names one of the pair
   against which one the schema calls current — `clinicaltrials-scraper`'s cause (3) named
   `hasResultsOnly` when the schema says it's deprecated in favor of `resultsAvailability`, so a
   buyer using the current field saw a message naming a field their input never touched (and the
   log line directly above it even printed that field as `false`).
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
