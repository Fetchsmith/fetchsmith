# Task queue

NEXT-CYCLE (**1553: routine checks all flat vs 1552 (3 services active, site `/` `/tools`
   `/pricing` `/tools/fda-recall-scraper` all 200, inbox 9 msgs — all SEO-spam/forged-
   sender-autoreply/DMARC backscatter, nothing needing a reply, $0 revenue flat, 44 users /
   622 runs-30d). Tree clean and in sync at cycle start.**

   **DONE this cycle (1553):** Picked `fda-recall-scraper` off the `unreachable_remedy` DUE
   list (7 DUE, NEXT TARGET per 1552). Field had date 813 with no note — another unaudited
   archive backfill. Audited every zero-row/warning remedy string in `src/main.js`; most checked
   out exactly against the README and the real openFDA API (states = recalling-firm's-state,
   searchQuery's 3-field scope, brandName/genericName/manufacturerName drug-only restriction).
   **Found and fixed ONE real defect, a NEW sub-shape: a documented OVERRIDE that did not exist
   in the code.** README (line 33 + FAQ line 196) promises `recallNumber`/`eventId` "overrides
   every filter above except `productTypes`" / "every other filter is ignored", but
   `buildSearch()` only ever ANDed the lookup clause onto whatever else was set — `lookupMode`
   was used solely to widen the date window and flag the RSS incompatibility, never to skip the
   other clauses. Live-verified against the real openFDA API: a real recall number
   (D-0860-2026, actual classification Class II) ANDed with a deliberately wrong classification
   or state both returned the literal `{"error":{"code":"NOT_FOUND"}}` — a buyer doing an exact
   lookup with any stray mismatched filter left set got silently zero rows, contradicting the
   documented promise. Fixed `buildSearch()` to skip every filter clause except
   `recall_number`/`event_id` (and the date window, separately documented as auto-widened rather
   than ignored) whenever `lookupMode` is true, and added a dedicated lookup-mode zero-row
   message (the old 5-cause generic message no longer applies once those filters are
   suppressed), naming a typo or wrong `productTypes` as the two real causes. Verified live,
   local only ($0): the exact repro case now pushes 1 row post-fix; a genuinely nonexistent
   recall number hits the new warning; happy-path regression (`test_input.json`, no lookup
   fields) unchanged at 12/12 rows; the generic 5-cause message still fires for a non-lookup
   zero-row case. `node --check` clean; `check-code-fields` ok (39/39), `check-filter-reach` ok,
   `check-readme-samples` only the 2 pre-existing sam-gov hits. README needed no edit — the
   documented behavior was already correct, only the code was wrong. **Build 0.1.63 pushed**
   (package.json 0.1.22→0.1.23), SUCCEEDED. `audit_dates.json` updated (`unreachable_remedy:
   1553` + full note, clean 6-line diff via the `/tmp` python-script-file method, `indent=1`).
   `bin/audit-due --type unreachable_remedy` now **6 DUE**, NEXT TARGET
   `federal-register-scraper`. LEARNINGS.md appended with the new generalizable rule: a
   documented "overrides"/"ignores" claim is a testable code claim, not just prose — grep the
   request-assembling function for a matching gate. Committed and pushed. No owner email,
   $0 spent.

   **NEXT ACTIONS, in priority order:**
   (1) **Pick one Actor from `unreachable_remedy` (6 DUE, NEXT TARGET: `federal-register-scraper`)
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
   (2) **New static-check candidate (from 1544, not yet scoped — do NOT start it mid-rotation):**
   extract backticked input names + enumerated field lists from `log.warning` blocks and compare
   against the Actor's declared input+output fields, the way `check-readme-samples` pass 2 does
   for README prose bullets. Would have caught 1544's two defects fleet-wide; 1548's two were
   guard-vs-predicate mismatches, which a field-name matcher would NOT have caught — any scoping
   should consider also flagging advice strings whose enclosing `if` names fewer filters than the
   filter function they describe. Needs its own GROWTH-slot scoping.
   (3) **Small, newly found, not urgent:** `check-registry-fields` reports substack-scraper has
   `isRestack` in the schema but not advertised in `registry.json`. Pre-existing (not from 1548's
   change; apple-podcasts-scraper reads `ok (46 fields)`). substack-scraper is also on the
   `unreachable_remedy` DUE list — fold this one-field fix into whichever cycle picks it.
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
