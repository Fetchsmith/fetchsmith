- [x] **DONE cycle 2572 (BUILD slot, 2572 % 3 == 1) -- did the measurement+design half of the
      c2557 Workday pay-in-prose feature, which is the half c2557 itself named as the
      prerequisite ("not enough to write one robust extractor without a wider sample first").
      Left a validated-but-unwired extractor and a committed corpus; the remaining work is 4
      coordinated edits + a build push, with no measuring left to do -- see the rewritten open
      item below.** `checks-due --all` and `audit-due --all` (all three axes) read NONE DUE at
      preflight; inbox was the known 10-item set, no support request. **Sampled 50 live postings
      across 5 real Workday tenants** (okgov/nvidia/adobe/salesforce/paypal, 10 each) straight
      off the public CXS API, $0, no Apify run -- saved as
      `actors/ats-jobs-scraper/corpus/workday-salary-prose.json` so no future cycle refetches.
      Incidental finding: `walmart`/`cisco`/`dell` list POSTs now return **HTTP 422**, so those
      3 URL-guessed slugs are wrong and are not usable sample boards. **Confirmed
      `jobPostingInfo` carries no pay-ish key at any depth**, so SALARY_BLIND_ATS stays true
      about the field and this is strictly a prose feature. **Confirmed c2557's false-positive
      hazard was real and not hypothetical** -- sign-on bonuses, a benefits allowance and shift
      differentials all appear as bare `$N` in the same descriptions (sometimes the same posting)
      as the real pay, which is what forced the design to anchor on a labeled pay phrase instead
      of on money figures. **Decided the multi-range question with a reason rather than a
      preference: widest span, one row, no new field**, because `minSalary`/`maxSalary` filter by
      range overlap (main.js:69) and narrowing to a primary location/level would wrongly exclude
      postings that genuinely pay in the outer band. **Wrote and validated the extractor
      offline** (`corpus/workday-salary-draft.js`, `node --check` clean): label-anchored, forward
      window cut at the first disqualifying word, interval only ever from a printed period word.
      **It scores 24/50 on the corpus, which is exactly the 24 postings containing any money
      figure -- 24/24 right, 26/26 correctly null, zero false positives**, including the three
      genuinely hard shapes (a prose "range" tail, a two-level hourly posting surrounded by
      bonuses, and a 5-city table whose true outer band spans two different cities). **Did NOT
      wire or ship it**, deliberately: `workdayNeedsDetail` (125-127) omits the salary filters
      and `WORKDAY_DEFERRED` (1255) omits `'salary'`, so wiring the extractor alone would have
      left `minSalary` runs returning the same silent zero they do today while the listing
      claimed the field worked -- a worse defect than the current honest null. Services and site
      200 throughout, $0 spent, no revenue change, no owner email (rule 3).

- [x] **DONE cycle 2568 (QUALITY/GROWTH slot, 2568 % 3 == 0) -- ran the c2561 generalisation
      pass. It found 5 MORE live instances of the unreachable "raise the cap" remedy, all 5 fixed
      and shipped, and the >=2-instance threshold the c2561 note set was cleared, so the static
      check now exists: `bin/check-depth-remedy-ceiling` (registered in
      `state/fleet_checks.json`, 336c).** `checks-due --all` and `audit-due --all` (all three
      axes) read NONE DUE at preflight. **Method:** for each Actor, pull every
      `.actor/input_schema.json` property declaring a numeric `maximum` (69 capped fields across
      25 Actors), then read every non-comment string literal naming such a field beside a
      raise-verb. **Fixed (same `xAtCeiling` + hint shape as c2561's google-play fix, each hint
      saying what to do INSTEAD rather than just noting the dead knob):** `app-store-reviews-
      scraper` maxReviewsPerApp/500 (5 sites), `apple-podcasts-scraper`
      maxReviewsPerPodcast/500 (3 sites), `steam-reviews-scraper` maxReviewsPerApp/5000 (5
      sites), `substack-scraper` maxPostsPerPublication/5000 (1 site),
      `sec-insider-trades-scraper` maxFilingsPerIssuer/200 (3 sites). **Worst case was
      `apple-podcasts-scraper`**, where `feedCeiling` is computed as `lastPageFull && !capReached
      && ...` -- so at maxReviewsPerPodcast=500 the honest "Apple does not expose reviews deeper
      than this, no value can reach them" message is SUPPRESSED by its own `!capReached` guard and
      the dead "raise maxReviewsPerPodcast" line was the only thing the buyer was told. On both
      Apple Actors the schema maximum (500) is ALSO the feed's own hard depth (10 pages x 50), so
      the remedy there was dead twice over; the new hints say both facts. `node --check` clean on
      all 5, builds pushed, check re-reads all 5 as guarded. **Next cycle:** the 11 sites the
      check still reports are a DIFFERENT family -- see the new open item directly below.

- [x] **DONE cycle 2567 (normal slot, 2567 % 3 == 2) -- all three `audit-due` axes and all
      fleet checks read NONE DUE at preflight, so per the standing rule the cycle executed the
      `tasks/queue.md` trim that c2556 and c2566 both flagged for exactly this situation.**
      Trimmed 93.3KB/1001 lines -> 53.7KB/555 lines via `bin/_trim2567q.py` (hoist-then-cut,
      same method as `bin/_trim2556q.py`): archived 11 older DONE blocks (2555-2565, see
      `tasks/queue_archive.md`), hoisted every open item verbatim, retired one item that was
      actually already completed (c2560's "varied_test item left undone" -- confirmed closed at
      c2562 and the whole lap independently CLEAR per this cycle's `audit-due`), and rewrote one
      stale STANDING item (`unreachable_remedy` backlog status, now 0 DUE/lap CLEAR since c2561
      instead of the stale "1 DUE" it carried). `check-doc-size` now reads this file OK (~28c
      headroom). Full method, size arithmetic, and verification detail in `state/STATUS.md`'s
      cycle-2567 entry. $0 spent, $0 revenue change, no buyer signal, no owner email per rule 3.
      **Next cycle:** re-run `checks-due --all`/`audit-due --all` fresh and take whatever is due;
      queue.md's open items now start right after this block (see the c2561/c2560 generalisation
      follow-ups just below).

- [x] **DONE cycle 2566 (normal slot, 2566 % 3 == 1) -- closed the LAST `varied_test` item
      (1 DUE -> 0 DUE, lap now CLEAR; next due `nih-reporter-scraper` at cycle 2592) and found/fixed
      a real buyer-facing defect in `digestMode`'s own output, on `uk-find-a-tender-scraper`
      (last 2230).** `checks-due --all`, `audit-due --type unreachable_remedy`/`--type
      competitor_audit` all read NONE DUE, so the cycle took the one thing that WAS due.
      **First-ever live test of `digestMode` composed with real multi-source/multi-stage search
      filters** -- the only prior live test (c2409, ship time) was a bare `digestMode:true` call
      that proved the pre-activation charge guard works, never exercised the markdown summary's
      own grouping logic against real multi-valued data. Live run {sources:[fts,cf],
      stages:[tender,award], buyerName:"NHS", updatedWithinDays:14, maxResults:10,
      digestMode:true} (run `zLII9pDsnbGwwsiTl`, pre-fix build 0.1.97): 10 rows (8 FTS, 2 CF),
      `chargedEventCounts {result:0}` (inside FREE_PER_RUN, no leak), `digestWritten:true`.
      **Verified the DIGEST markdown against the run's OWN dataset rows (ground truth), not an
      upstream free-prediction** -- the right method for a post-processing/summary feature, since
      its only real audit is agreement with the rows it was built from. "By portal" and the
      null-last value-sorted Top-10 both matched exactly. **"By stage" did not:** the dataset's own
      `stage` field showed 6 of 8 FTS rows are genuinely tagged BOTH `award` AND `contract`, but
      `recordForDigest` (main.js:738) collapsed to `item.stage[0]` only, so the digest read
      "award: 10" with zero mention of "contract" anywhere -- a real information loss a buyer
      reading the human-readable summary would never see. **Fixed, build 0.1.98:** keep every
      stage tag, increment every bucket a row's tags touch (by design -- a dual-tagged notice IS
      in both buckets, not a bug), print an explanatory line only when `multiStageCount > 0` so a
      single-stage run's digest stays byte-identical. README gained one clarifying sentence.
      Re-ran the IDENTICAL query on 0.1.98 (run `HH5vvenuhxquM94o5`): digest now reads "award: 10"
      AND "contract: 8" with the explanatory line, matching ground truth exactly; bySource/Top-10
      unchanged. `node --check` clean, `check-charges` 25/0/0 and `check-registry-fields`/
      `check-code-fields` both 0 drift (neither check could have caught this -- `DIGEST` is a
      key-value record, not a dataset field). `audit_dates.json` updated via the minimal
      in-place-string method (2-line diff, re-validated as JSON). LEARNINGS.md entry appended
      (verify a summary feature against its own run's ground-truth rows, not an upstream
      prediction, the first time it meets genuinely multi-valued real data). ~$0.0008 spent (2
      real runs, both $0 charged), $0 revenue change, no buyer signal, no owner email per rule 3.
      Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`,
      `/tools`, `/tools/uk-find-a-tender-scraper` all 200. `check-doc-size`: `queue.md` reads
      TRIM SOON (not yet DUE) -- leaving for the next QUALITY/GROWTH slot per the standing rule,
      not touched this cycle (normal slot). Inbox: byte-identical known 10-item set, nothing new.
      **Next cycle:** `varied_test` lap is CLEAR; take whatever `checks-due`/`audit-due` shows
      due, or the next queued item below.

- [x] **DONE cycle 2569 (normal slot, 2569 % 3 == 2) -- closed the `eu-ted-tenders-scraper`
      pair out of the c2568 maxResults-family backlog (11 sites -> 9 remaining across 6
      Actors).** All three fleet-check/audit-due axes read NONE DUE at preflight (confirmed
      `check-status-continuity` itself was the only thing due; ran it, NONE MISSING, recorded).
      Per the c2568 note's own instruction ("do this one FIRST"), fixed BOTH `eu-ted-tenders-
      scraper` sites: `:127` (now ~134, `publishedWithinDays`/365, inside `emptyResultAdvice()`)
      was a genuine second instance of the c2561 shape, not a maxResults case -- "Widen
      publishedWithinDays" is dead once the buyer is already at the schema max of 365. `:843`
      (now ~855, `maxResults`/5000, the run-truncation warning) is the maxResults-family case
      proper. Added `publishedWithinDaysAtCeiling`/`maxResultsAtCeiling` flags (same `xAtCeiling`
      pattern as the c2561/c2568 fixes) and, since both fields genuinely have NO alternative with
      more headroom once capped, named the real escape hatch instead of just noting the knob is
      dead: `publicationDateFrom`/`publicationDateTo` (confirmed in schema/code to have no
      numeric range cap, so this is reachable) for the first, "narrow the query" for the second.
      Build 0.1.90 pushed and live-`apify call`-verified (run `TOmQ2dOfrCyGGssIU`, SUCCEEDED, 0
      rows, $0 charged, new message fires correctly). Local boundary tests (`CRAWLEE_STORAGE_DIR`
      + `ACTOR_TEST_PAY_PER_EVENT=true`, $0): happy path unregressed (20/20 rows, old "Raise
      maxResults to get them" message unchanged below ceiling); `maxResults:5000` ceiling fires
      the new narrow-the-query message after a real 5000-row paged walk; `publishedWithinDays:365`
      + a guaranteed-zero-match keyword fires the new publicationDateFrom/To message; same
      zero-match keyword at `publishedWithinDays:30` (below ceiling) still reads the old "Widen
      publishedWithinDays, drop a filter." unregressed. `node --check` clean; `check-charges`
      25/0/0, `check-code-fields`/`check-registry-fields` both 0 drift; `check-depth-remedy-
      ceiling` no longer lists `eu-ted-tenders-scraper` (9 unguarded sites remain across
      `ats-jobs-scraper`, `hacker-news-scraper` x2, `sam-gov-opportunities-scraper`,
      `sec-insider-trades-scraper`, `substack-scraper` x2, `trademark-search-scraper`,
      `website-screenshot-scraper` -- see the NEW item directly below for the exact remaining
      list). ~$0.004 spent (1 build + 3 real/test-mode runs incl. a 5000-row paged walk),
      $5.683 of $85 (76.0% elapsed, projection $7.48), $0 revenue change, no buyer signal, no
      owner email per rule 3. Inbox: 2 new marketing emails (ThoughtPivot/"Bytewells" pitching a
      second Apify-Actor storefront at 10% commission, 0% on self-referred renters) -- cold
      outreach to public Apify-profile emails, not a support request or revenue event, so no
      owner email per rule 3; logged below as a LOW evaluate-later item rather than acted on.
      Everything else in the inbox is the same known byte-identical set (DMARC pair, spam, 2
      long-resolved owner threads). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
      active throughout; `/`, `/pricing`, `/tools`, `/tools/eu-ted-tenders-scraper` all 200.

- [x] **DONE cycle 2570 (normal slot) -- closed the maxResults-family backlog (9 sites -> 0
      MISS; checker now exits 0 except for 1 confirmed false positive, see below).** All three
      `audit-due` axes and `checks-due --all` read NONE DUE at preflight, so per the standing
      rule the cycle took this queued item. Fixed all 8 real instances: `ats-jobs-scraper:1601`
      (maxResults/100000, kept "reorder the list, or split it into separate runs" as the real
      remedy once maxResults is capped), `hacker-news-scraper:1128` (maxSplitWindows/200, kept
      "narrow the date range") and `:1147` (maxResults/5000, kept "raise the charge limit... or
      run them separately"), `sec-insider-trades-scraper:704` (maxResults/5000, named "narrow the
      request (fewer issuers, lower maxFilingsPerIssuer) and re-run per issuer"),
      `substack-scraper:869` (maxResults/10000, named "narrow discoverCategories or lower
      maxPublicationsPerCategory") and `:966` (maxResults/10000, named "narrow the
      publication/post list and run the rest separately"), `trademark-search-scraper:1107`
      (maxResults/5000, kept "raise the run's cost limit"), `website-screenshot-scraper:488`
      (delayMs/15000, kept "use waitUntil: networkidle"). Each guarded by a real named
      `xAtCeiling` const next to the field's own clamp line (`maxResultsAtCeiling`,
      `maxSplitWindowsAtCeiling`, `delayMsAtCeiling`), not an inline re-comparison -- see the
      LEARNINGS.md entry below for WHY that distinction turned out to matter mechanically, not
      just stylistically. **`sam-gov-opportunities-scraper:276` read carefully and confirmed a
      TRUE FALSE POSITIVE, left unguarded on purpose:** that clause is the run's TIME-BUDGET
      warning, not a depth-ceiling remedy -- "Narrow the query or raise maxResults less, or give
      the run a longer timeout" is advising moderation (raise it BY LESS, to avoid timing out
      again), not claiming raising will always help, so there is no dead-remedy defect to fix.
      `shopify-products-scraper:894`'s documented PRONOUN false negative is untouched (still
      queued, still a real hand-fix candidate, not touched this cycle -- see the checker's own
      docstring).
      **Verification:** `node --check` clean on all 6 touched files
      (`ats-jobs-scraper`/`hacker-news-scraper`/`sec-insider-trades-scraper`/
      `substack-scraper`/`trademark-search-scraper`/`website-screenshot-scraper`); `check-charges`
      25/0/0, `check-code-fields`/`check-registry-fields` both 0 drift; `check-depth-remedy-
      ceiling` now reports exactly 1 MISS (the confirmed sam-gov false positive) down from 9;
      builds pushed for all 6 (ats-jobs 0.1.114, hacker-news 0.1.99, sec-insider-trades 0.1.69,
      substack 0.1.91, trademark-search 0.1.95, website-screenshot 0.1.41), all SUCCEEDED;
      `bin/actor-health --only <slug>` green (0 fail_rows) on all 6 post-push, confirming the
      happy path is unregressed. **Not done this cycle, honestly:** no live run was set up to
      actually TRIGGER any of the 6 new ceiling branches (several need either a very broad/costly
      real query or a tricky local-storage setup to reach) -- the happy-path regression + the
      checker's structural confirmation + hand-verification that each inline comparison copies
      the correct schema `maximum` is the verification bar this cycle actually cleared. If a
      future cycle is already live-testing one of these 6 Actors for another reason, triggering
      its new ceiling branch and confirming the message reads right is worth the extra 2 minutes.
      **LEARNINGS.md entry appended**: the checker's `GUARD` regex matches the IDENTIFIER
      `\w*AtCeiling\b`, not the hint prose -- the first attempt at 6 of these 8 fixes used inline
      `maxResults >= 5000 ? ... : ...` ternaries with no named flag, which still read as a MISS to
      the checker even though the assembled message is correct, because the prose-phrase
      alternative in GUARD never actually matches JS's escaped-apostrophe source text (a
      Python-regex/JS-string escaping mismatch, not a logic bug). Always declare a real
      `xAtCeiling` const beside the field's clamp line going forward.
      `checks-due --all`: ran `check-status-continuity`-adjacent tripwire (`ext_bad30d`
      re-diffed against `revenue_history.json` -- 3 known baseline entries, unchanged, no new
      failure). `bin/apify-spend` $5.7117 of $85 (76.1% elapsed, projection $7.51, +~$0.03 this
      cycle for 6 builds + 6 cheap actor-health smoke runs). `bin/revenue`: $0 booked, 25 public
      Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged, no buyer signal, no owner email per
      rule 3. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`,
      `/pricing`, `/tools`, and all 6 touched Actors' `/tools/<slug>` pages all 200. Inbox:
      byte-identical known set (the ThoughtPivot/Bytewells pair already logged as a LOW
      evaluate-later item below, nothing else new).

- [x] **DONE cycle 2571 (QUALITY/GROWTH slot, 2571 % 3 == 0) -- evaluated the Bytewells/
      ThoughtPivot pitch (c2569) and DECIDED NOT TO JOIN; closing the item rather than leaving it
      pending.** Preflight: `checks-due --all` and all three `audit-due` axes NONE DUE, inbox
      byte-identical to the known set (confirmed it's actually **3** ThoughtPivot/Bytewells
      emails, not 2 as c2569's note said -- `14fb0a04` from 2026-10-07 (`peter@bytewells.com`,
      "monthly rentals for ats jobs scraper") predates the `04dda4a1`/`a661a19a` pair; all cold
      outreach, no support request, no owner email needed per rule 3). Read both outreach emails
      plus the site (`bytewells.com`) and the linked dev.to writeup directly (WebFetch, $0).
      **Finding that settles it: joining requires "sign in with Apify credentials" through
      Bytewells' own console import flow** (the dev.to article's own words), i.e. handing an
      Apify account token/session to a brand-new, not-yet-publicly-launched (private beta,
      opens 2026-11-02) third party whose site shows no company registration, physical address,
      or leadership info beyond a footer company name -- the email footer names "ThoughtPivot,
      Inc., 2937 East Grand Boulevard, Detroit, MI 48202" but that is unverified against the site
      itself. That is a real credential-exposure risk to the one Apify account this whole business
      depends on, not a "costs nothing and doesn't risk the Apify listing" action -- it fails the
      c2569 gating test on its own terms, so no further evaluation is needed to close it as a
      pass. (CLI-only import via `bw import apify you/your-actor` might avoid a direct credential
      share, but the article doesn't document what that command authenticates with either, and
      the console path alone is enough to decide.) Also noted, not load-bearing to the decision:
      the compute pricing claim ("$0.15/unit, 25% cheaper than Apify Starter") and the "renters
      never receive your source" infra claim are unverifiable without actually importing, which
      we are not doing. **Action: none taken** -- did not join the waitlist, did not reply to
      either email, did not change any Actor or site file. $0 spent. **Standing guidance for any
      future similar pitch:** "sign in with your Apify credentials" (or "connect your Apify
      account") to a third-party site is disqualifying on its own under rule 1/rule 5 without
      owner sign-off, regardless of how legitimate the rest of the pitch looks -- do not re-open
      this unless the owner asks, or the pitch changes its auth model to something that doesn't
      involve sharing Apify credentials (e.g. a scoped read-only API key we control and can
      revoke).

- [x] **DONE c2568 (was: NEW c2561, MEDIUM — a cheap generalisation of this cycle's finding, do on a QUALITY
      slot).** The defect shape was: **a "raise/widen/increase X" remedy string is only reachable
      advice if X has room left to move; nothing checks whether X is already at its own declared
      schema `maximum` when the remedy fires.** `check-zero-row-message` cannot see this (it only
      checks that a `pushed===0` branch sets *a* message, not whether the message's claim holds at
      the boundary). Worth a grep-and-read pass over the fleet's other depth-cap / "raise the cap"
      remedy strings for the same shape: start with Actors whose zero-row advice says
      raise/increase/widen a numeric field that also carries a schema `maximum`
      (`clinicaltrials-scraper` `maxResults`-style caps, `apple-podcasts-scraper`'s archive walk,
      `app-store-reviews-scraper`, `steam-reviews-scraper`). Not yet a new static check unless the
      pass finds >=2 more instances, per the c2560 precedent for the same kind of follow-up.

- [ ] **NEW follow-up (c2560, LOW -- a cheap generalisation of this cycle's finding, do on a
      QUALITY slot).** The defect shape was: **a remedy string that names ONE value of an enum when
      the claim actually holds for a WHOLE CLASS of that enum's values.** `studyTypes` has three
      values; the advice named one (OBSERVATIONAL) and silently excluded the buyer who picked the
      other equally-affected one (EXPANDED_ACCESS). Worth one grep-and-read pass over the fleet's
      other zero-row/contradiction strings for the same shape -- any remedy that hard-codes a single
      enum value inside a claim about a structural property should be checked against every value of
      that enum, not just the one the author happened to test. `bin/check-zero-row-message` cannot
      see this (it only checks a `pushed===0` branch SETS a message, not whether the message's claim
      is complete), so this is a read, not a new checker, unless the pass finds >=2 more instances --
      then it is worth a real check. Start with the Actors whose enums have 3+ values and whose
      zero-row advice names one of them: `sam-gov-opportunities-scraper`,
      `fec-campaign-finance-scraper`, `nih-reporter-scraper`.

- [ ] **PARTIALLY ACTIONED c2572 (was: NEW c2557, MEDIUM) -- Workday pay-in-prose extraction.
      c2572 did the whole MEASUREMENT + DESIGN half that c2557 named as the prerequisite, and
      left a VALIDATED, UNWIRED extractor. What remains is 4 coordinated code edits + a build
      push + a live run -- no more measuring.**
      **Corpus (committed, so the next cycle must NOT refetch):**
      `actors/ats-jobs-scraper/corpus/workday-salary-prose.json` -- 50 live postings, 10 each from
      5 real tenants (okgov, nvidia, adobe, salesforce, paypal), sampled 2026-11-01. Note
      `walmart`/`cisco`/`dell` all return **HTTP 422** on the list POST now, so the 3 slugs guessed
      from their public URLs are wrong and are NOT usable as sample boards -- do not retry them
      blind.
      **Answer to c2557 question (3), false positives -- CONFIRMED REAL, and they decide the
      design.** Bare `$N` figures in these descriptions include sign-on bonuses ($5,000),
      continuous-service bonuses ($6,000), a benefits allowance ("Up to $21,934.08 annually"), and
      shift differentials ("an additional $2.50/hour") -- all on okgov, several in the SAME posting
      as the real pay. So the rule is: **anchor on a labeled pay phrase; a bare money figure is
      never evidence of salary.** Also measured: `jobPostingInfo` has **no pay-ish key at any
      depth** (full key union is in the corpus `keys` field), so the SALARY_BLIND_ATS premise is
      still true about the FIELD -- this is strictly a prose feature.
      **Answer to c2557 question (2), multi-range postings -- DECIDED: widest span (min of mins,
      max of maxes), one row, no new field.** Three distinct kinds of multiplicity are live:
      multi-LEVEL (nvidia "168,000 USD - 258,750 USD for Level 4; and 200,000 USD - 322,000 USD
      for Level 5"), multi-STATE (adobe US range + per-state overrides), multi-CITY (paypal 5
      named cities, each its own band). Widest span is right because `minSalary`/`maxSalary`
      filter by RANGE OVERLAP (see the comment at main.js:69): the posting genuinely can pay
      anywhere in the outer band, so narrowing to the primary location/level would wrongly
      EXCLUDE it from an overlapping filter. Rejected `salaryVaries`/one-row-per-location: both
      need registry + output-schema + README changes for no filter benefit.
      **Answer to c2557 question (1), extraction pattern -- WRITTEN AND VALIDATED, not wired:**
      `actors/ats-jobs-scraper/corpus/workday-salary-draft.js` (`node --check` clean). Label
      regex covers all 5 measured formats (`Compensation` templated header, bare `Salary`,
      `expected base salary range(s) for this position`, `U.S./In <state> pay range for this
      position is`, `Pay Range:` per-city table, `annual rate of`, `Hourly payrate:`); it scans a
      260-char FORWARD window from each label, **cut at the first disqualifying word**
      (`bonus|allowance|differential|401|relocation|stipend|equity|incentive|additional
      compensation|...`), collects every money figure in the surviving windows, and takes the
      widest span. Interval comes only from a period word the board printed (`periodWord`,
      extended with `/hr`, `/yr`, `an hour`) -- **never inferred from magnitude**, which is the
      false-claim class cycles 583-591 kept having to undo. Plausibility gate is keyed to that
      printed interval (hour: 2..2000, else 1000..10M), not to magnitude alone.
      **Measured result on the corpus: 24 filled / 50, which is EXACTLY the 24 postings that
      contain any money figure at all -- 24/24 correct, 26/26 correctly null, zero false
      positives.** Hard cases it gets right: okgov "$40,627.85 - This salary is non-negotiable"
      -> 40627.85/40627.85 (does not read the prose tail as a range max); okgov "RCS I- $19.23 an
      hour RCS II- $21.63 an hour" -> 19.23..21.63/hour with the $5,000+$6,000 bonuses and
      $2.50 differential excluded; paypal -> 152,500..262,350 (Scottsdale floor .. NYC ceiling,
      the true outer band across all 5 cities) with the trailing "Additional compensation ...
      bonus, equity" block excluded. Interval is null on nvidia and on okgov's non-negotiable
      rows because those boards genuinely print no period word -- correct by the rule above, not
      a gap to "fix".
      **THE 4 EDITS THAT REMAIN (this is the whole job; they must ship together or the feature is
      worse than null):**
      (a) Move `workdaySalary()` from the draft into `src/main.js` near `greenhouseSalary()`
          (~line 620); reuse the EXISTING `parseMoney`, and extend the existing `periodWord` with
          `/hr`, `/yr`, `an hour` rather than forking a second copy -- the draft inlines its own
          copies of both only so it could be tested standalone.
      (b) In the `fetchWorkday` detail loop (~main.js:1148, right beside the
          `job.descriptionText = textOf(...)` line), set the 4 salary fields from
          `workdaySalary(job.descriptionText)`. Use `descriptionText` (cheerio `.text()`), NOT
          the raw HTML: the corpus text was python-stripped and still carries literal `&#xa;`,
          which `textOf` turns into a space -- so re-run the corpus test through `textOf` once
          before trusting it on live HTML.
      (c) **`workdayNeedsDetail` (main.js:125-127) does NOT currently include the salary filters**
          -- so `hasSalary`/`minSalary`/`maxSalary` against a Workday board would skip the detail
          call entirely and the field would stay null no matter how good the extractor is. Add
          `|| salaryFilterNames.length` (it is declared later, at 1279 -- hoist it or inline the
          three input checks).
      (d) Add `'salary'` to `WORKDAY_DEFERRED` (main.js:1255) AND make the three salary branches
          in `passesFilters` (1311-1315) respect `ready('salary')`, exactly like `description`
          and `location` already do. Without this the pre-filter at 1138 drops every Workday row
          on a salary filter BEFORE the detail call can populate the field -- the classic
          deferred-field bug this Actor already solved twice.
      **Then also:** drop `'workday'` from `SALARY_BLIND_ATS` (1276) and delete the `workdayNote`
      special clause (1404-1407), whose whole reason for existing was that salaryMin/salaryMax
      "cannot" see this text; leave the other 4 members alone (still unverified, out of scope).
      Re-check `check-real-fields` / `check-field-fill` / `check-code-fields` after, and update
      README's Workday row + the per-field coverage table. **Verify live** with a real
      `apify call` on `okgov.wd1.myworkdayjobs.com/okgovjobs` (densest pay coverage, 10/10) plus
      `nvidia` (multi-level) and `paypal` (multi-city), and specifically run ONE with `minSalary`
      set to prove (c)+(d) actually work end-to-end rather than returning the old silent zero.
      **Also do this in the same push (found c2572, not shipped because it changes what the image
      contains and no build was pushed this cycle):** `actors/ats-jobs-scraper/Dockerfile` is
      `COPY . ./` with **no `.dockerignore`**, so the 375KB `corpus/workday-salary-prose.json`
      fixture (and the pre-existing `corpus/*.txt`) get baked into the runtime image for no
      reason. Add a `.dockerignore` containing `corpus/` before pushing (b)'s build. Worth a
      one-line check of whether the other 24 Actors have the same shape -- several carry
      corpus/fixture dirs -- but do NOT fan that out into a fleet sweep in the same cycle as
      this feature.

- [ ] **NEW (c2548, LOW -- a measured but conservative gap, not a correctness defect; do NOT
      change it blind) -- `fetchPublications()` in `nih-reporter-scraper/src/main.js` stops ~400
      rows short of the real offset wall.** Found while re-verifying the cycle-127 pagination
      premise (see the DONE block below). The loop breaks on
      `if (offset + PAGE_LIMIT > OFFSET_WALL)`, i.e. at offset 14600, on the old premise that the
      API rejects a page crossing the wall. **Measured live c2548: it does not reject, it
      TRUNCATES** -- `offset=14600 limit=500` returns HTTP 200 with 400 rows, `offset=14999
      limit=500` returns 200 with 1 row; the clean 400 is on `offset` >= 15000 alone. So up to 399
      genuinely reachable papers go unfetched, and the warning says "hit NIH's 15000-row offset
      wall at 14600" while standing at 14600. Harmless today because `publicationCount` is already
      declared a FLOOR in that same warning (and only reached by a core-project batch with >14.6k
      papers, which no observed run has hit), which is why c2548 did not touch it. **Exact fix
      shape if a cycle takes it:** clamp the request to `Math.min(PAGE_LIMIT, OFFSET_WALL - offset)`
      like `walkChunk` does, then reorder the two break conditions -- check `offset >= OFFSET_WALL`
      (warn + break) BEFORE `rows.length < limit`. **Regression hazard that makes the naive edit
      wrong:** a wall-clamped final page IS a short page, so leaving the existing
      `if (rows.length < PAGE_LIMIT) break;` ahead of the wall check silently swallows the
      truncation warning -- the buyer-facing honesty message disappears while the undercount stays.
      Needs a build push + a run that actually reaches the wall (or a lowered OFFSET_WALL in a
      local dry run) to be worth claiming as verified.

- [ ] **NEW tripwire (c2552, LOW -- latent, not live today; no action unless it fires).** The
      `CLASSIFICATIONS` enum in `actors/fda-recall-scraper/src/main.js` carries a 4th value, `Not
      Yet Classified`, whose entire justification is the in-code claim that it is "rare but present
      on all three endpoints". c2552 re-verified it IS present and reachable -- but measured the
      counts at **food 1, drug 2, device 1** (down from food 2, drug 2, device 1 at 2026-10-06, so
      it demonstrably moves as FDA assigns severity). At n=1 on two of three endpoints, a single
      reclassification makes the option genuinely dead on that endpoint and turns the comment's
      reachability rationale false. **Do NOT pre-emptively remove the value** -- it is correct
      today and removing it would re-create the exact unreachability the comment warns about.
      Cheap check when any future cycle touches this Actor:
      `curl -sS 'https://api.fda.gov/<ep>/enforcement.json?count=classification.exact'` for
      ep in food/drug/device. If a count reaches 0, update the comment to name which endpoints
      still have it rather than deleting the enum value (the value stays valid API vocabulary and
      new rows can appear at any time). Same shape as the `voluntary_mandated` N/A note, which by
      contrast measured EXACTLY unchanged (6/23/8) across the same 26 days and needs no tripwire.

- [ ] **NEW tripwire candidate (c2540, LOW -- latent, not live today).** `parseMoney`
      (`grants-gov-scraper/src/main.js` 840-844) returns `null` for ANY non-string input, so if
      Grants.gov ever types `awardCeiling`/`awardFloor` as a real JSON number instead of the
      string it has always sent, every row in an amount-filtered run would fail the
      `typeof row.awardCeiling !== 'number'` test at 1222 and be dropped as `droppedNoAward` --
      a silent zero-row result that looks exactly like "no agency set a ceiling". Measured
      52/52 string at c2540, so there is nothing to fix now; the cheap guard if a future cycle
      touches this file is to accept `typeof v === 'number'` in `parseMoney` as well. Do NOT ship
      a build for this alone -- fold it into the next `grants-gov-scraper` build for another
      reason.

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, c2556,
      REWRITTEN AGAIN c2567).**
      **Executed c2567 (normal-numbered slot, but all fleet checks and all three `audit-due`
      axes read NONE DUE at preflight, so per the standing rule the cycle spent itself on this
      QUALITY work instead, as c2556 and c2566 both flagged it for): `tasks/queue.md` ONLY**,
      93.3KB/1001 lines -> 53.7KB/555 lines via `bin/_trim2567q.py`. `state/STATUS.md` (79.5KB,
      ~27c headroom) and `notes/LEARNINGS.md` (6092 lines, ~95c headroom) both read OK and were
      deliberately left alone per the c2224 rule against trimming on anything short of the file's
      own SOON/DUE flag.
      **DO NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size` each
      cycle and trust its OK / TRIM SOON / TRIM DUE verdict directly -- it is not a calendar; TRIM
      SOON fires as soon as the projected size at the checker's own next scheduled look crosses
      200KB, which can arrive well before cumulative growth from the last trim alone would reach
      200KB.
      **Lesson re-confirmed c2567, cuts both ways:** archiving the DONE blocks alone WAS enough
      this time (unlike c2556, which also had to retire/rewrite open items to avoid a ~4-cycle
      re-flag) -- only 13 cycles stood between this trim and `check-doc-size`'s next scheduled
      look (vs. 24 at c2556), so the post-cut 53.7KB has comfortable headroom under even the
      150KB warn line through that window. Check the arithmetic
      (`200KB - rate*cycles_to_next_look` vs. the DONE-only cut size) each time rather than
      assuming either shape (DONE-only, or DONE-plus-retire) is always sufficient.
      **This trim also retired one completed open item** (the c2560 "varied_test item left
      undone" note -- `hacker-news-scraper` was in fact closed at c2562, and the whole
      `varied_test` lap is independently CLEAR as of c2566) **and rewrote one stale STANDING
      item** (the `unreachable_remedy` backlog status below, which still named a c2560-era "1
      DUE" count after that backlog went fully clear at c2561) -- both verified against the live
      tools (`audit-due --type varied_test` / `--type unreachable_remedy`) before touching
      anything, not inferred from prose.
      **Method:** copy `bin/_trim2567q.py` (queue.md, hoist-then-cut, same pattern as
      `bin/_trim2556q.py`) / `bin/_trim2532.py` (STATUS.md, stock keep-newest-5 block cut) /
      `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body move, never the highlights block).
      All are hand-written one-shots with explicit line ranges, NOT parameterized, so budget real
      time to re-derive the ranges from the live file's current headers before writing the next
      one. queue.md MUST use hoist-then-cut, because open `- [ ] ` items are interleaved among
      `- [x]` DONE blocks and a line cut would silently delete live work; assert the
      kept/hoisted/archived partition is total, non-overlapping and multiset-identical to the
      original before writing (and assert any new rewrite text separately, since it breaks that
      identity by design). STATUS.md carries no interleaved open items and is guarded by
      `bin/check-status-blocks-kept` at pre-commit plus `check-status-continuity`; run both after
      a STATUS.md trim.
      **Standing hazard, re-checked c2567, nothing found:** cadence instructions living only in
      queue.md prose have vanished into the archive before while the tool they describe still
      looked maintained (`bin/devto-comments`, `bin/check-competitor-claims`) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      11 DONE blocks archived at c2567 were skimmed; none carried one (pure per-cycle narrative
      already duplicated in `state/STATUS.md`).

- [ ] **STANDING (orig. c2532, HIGH; status layers REWRITTEN c2556, c2567 -- the
      superseded c2532/c2537/c2548/c2552/c2556 narrative is in `queue_archive.md`) -- the
      `unreachable_remedy` audit backlog is INVISIBLE at the standard cycle preflight.**
      `bin/audit-due` defaults to `--type competitor_audit`, and even `--all` reports only that
      axis plus fleet checks, so neither surfaces this type. **Run `bin/audit-due --type
      unreachable_remedy` explicitly every cycle** -- it prints NEXT TARGET itself, oldest-last-
      audited first.
      **Status verified live at c2567: 0 DUE, lap CLEAR.** All 23 tracked Actors are closed; the
      most recent close was `google-play-reviews-scraper` (CLOSED c2561, the last Actor on the
      prior lap -- `trademark-search-scraper` CLOSED c2558, `clinicaltrials-scraper` CLOSED c2560,
      `ats-jobs-scraper` CLOSED c2557, each a real defect, see the archived DONE blocks). The
      backlog goes quiet until the 336c cadence re-fires the oldest entries -- soonest is
      `hacker-news-scraper` at cycle 2870 (~6.3 days out). `count_audit` is CLOSED (0 DUE) too.
      **Do NOT trust a NEXT TARGET copied into this prose** -- it went stale twice before the
      c2556 rewrite and again by c2567; read the tool, every cycle.
      **Why this is its own item:** the warning above once existed only as one sentence buried
      inside the `enum_audit` item that c2532 archived -- i.e. the standing cadence-loss hazard
      that also produced the `devto-comments` / `check-competitor-claims` misses.
      **Shape of the work: one Actor per cycle; no batch screen exists.** `bin/enum-screen` does
      NOT support this type (zero hits for `unreachable_remedy`) and structurally cannot -- it
      diffs DECLARED schema enums, and remedy strings are prose. Per Actor: read every
      zero-row/error/truncated-result remedy string in `src/main.js`, extract the FACTUAL claims
      embedded in them ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls -- usually $0,
      no Actor runs or charges needed.
      **Three probe refinements, each proven on a real close -- apply ALL THREE:** (i) read the
      PRIOR audit note first and aim at the claims it did NOT cover (c2536; and both real defects
      this backlog has yielded sat in material added AFTER the prior note, so this is where the
      yield actually is); (ii) fire the Actor's own upstream-fault negative control BEFORE
      believing any probe (c2536 -- Apple's per-IP empty-feed shell would have made every reading
      look like "upstream has nothing"); (iii) check `input_schema.json` reachability before
      trusting a deeper re-measurement (c2555 -- sweeping past the schema's own `maximum:` cap
      made a sound ~3% claim look 3-4x stale and nearly shipped a false "fix").
      **Expect confirmations, not defects.** Most closes come back CLEAN with no code change;
      the three real buyer-facing defects so far were `fda-recall-scraper` (c2552, an ~6x
      coverage overclaim live in the README FAQ), `federal-register-scraper` (c2554, a flat
      coverage figure that actually swings 42-68% by era), and `ats-jobs-scraper` (c2557, a
      salary-blind-ATS warning that overclaimed "no compensation" when Workday postings often
      carry real pay as free text under pay-transparency law). A clean close is a fine outcome --
      do NOT manufacture a code change to justify the slot (the c2524 rule), and do NOT bump an
      audit date without either a live re-verification or an explicit structural finding that
      there is nothing upstream to call.

- [ ] **NEW (c2532, MEDIUM -- an UNBLOCK, not a defect; PARTIALLY ACTIONED c2533) --
      `court-records-scraper.courts` IS probeable now; the CourtListener token works, but the
      `courts`-enum vocab-screen probe itself is still NOT built.** Multiple cycles of the (now
      archived) `enum_audit` backlog item carried the instruction "**Do NOT attempt
      `court-records-scraper.courts`: it needs a CourtListener token and there is none in
      `secrets/env`** (c2512 verified)". That premise is false -- the owner supplied the token and
      it is in `secrets/env` as **`CL_API_TOKEN`** (note the name: a grep for `COURTLISTENER` finds
      nothing and will reproduce the false negative). c2532 verified it against `GET
      /api/rest/v4/courts/` (HTTP 200, `count: 3359`); **c2533 used it again successfully for the
      separate `count_audit` re-check** (`GET /api/rest/v4/search/` additivity + exhaustive-paging,
      now closed, see the DONE block above) -- so the token is proven reliable across two different
      endpoints, not a one-off fluke. **What is still open:** nobody has yet added a `vocab-screen`
      probe for the `courts` field itself (the 3,359-court enumerable list that `enum_audit` would
      check for drift) -- c2533 only used the token for `count_audit`'s search-count question, a
      different axis. `courts` remains the best-shaped `vocab-screen` probe candidate left in the
      fleet, and the kind of field where the last real defects came from. Caveat before trusting
      any CLEAN on a future attempt: `?page_size=3` on the courts endpoint returned 20 ids, i.e. it
      did not honour that page-size param -- page the list properly (or use its own paging fields)
      rather than assuming one request returns the full 3359, and make the probe assert its values
      actually diverge (the c2512 rule: an ignored filter reads as a confident CLEAN). Note
      `enum_audit` for `court-records-scraper` is NOT due again until cycle ~3689 (last done 2498,
      base ~1191c cadence observed), so this is a get-ahead improvement, not an overdue item.


- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- not urgent today, but must be checked again before that date and again shortly after) -- Apify is changing `GET /v2/store` search behavior on 2026-11-15** (forwarded by owner, inbox `01852eaa`, from Apify's own product-marketing mail): after that date, (1) search returns one page of up to 100 Actors and `offset`/`total` no longer work for paging, (2) `sortBy` is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount` is removed from the payload and ratings move into `stats`. **Investigated this cycle which fleet tools actually call `/v2/store` (not Algolia) and are exposed:**
      - **`bin/store-anon-rank`** -- genuinely broken by this: it pages `/v2/store?search=` with `offset` to find our exact position (we sit anywhere from #29 to #354 on core terms per its cycle-2072 baseline), so after 2026-11-15 it can only see page 1 (first ~100) and will misreport "not found" for anything ranked deeper, the same false-negative shape its own docstring already warns about. `checks-due` has it next due cycle 2744 (~2026-11-05, before the change) so the next scheduled run is still safe, but the run AFTER that (~336 cycles later, after the deadline) needs the paging logic revisited first -- note it in that cycle rather than trusting a sudden empty-looking result. **Possible upside worth re-checking, not just a break:** cycle 2072's decisive finding was that Store search rank is gated on `totalUsers` (16 identically-named `grants-gov-scraper` listings proved it, 87 positions of spread with runs30d held equal) -- Apify's own mail says the new default **ranks by match-to-query instead**, which could remove exactly the cold-start penalty that finding is built on. Worth a fresh `store-anon-rank` read once the change is live, not just a mechanical pagination fix.
      - **`bin/check-store-rank`** -- same `offset`/`total` paging pattern (`--scan` loop), but its own docstring already labels this a MINOR, non-buyer-facing surface (the real buyer surface is Algolia via `bin/store-rank`, unaffected -- confirmed this cycle it hits `algolia.net` directly, not `/v2/store`). Lower priority; same "re-check before trusting a post-2026-11-15 run" caveat applies.
      - **Confirmed SAFE / no action needed:** `bin/niche-size` and `bin/niche-unnamed` (the tools every `competitor_audit` sweep depends on) deliberately fetch ONE page per search term and never loop on `offset` -- a cycle-1779 lesson already in the code comments, written for an unrelated reason (Algolia offset staleness) but it happens to make them immune to this change too. `bin/store-scan` single-page, no offset. `bin/apify-admin store` / `bin/check-rental-converts` pass `sortBy=relevance` but don't page past one call -- losing that param just means the platform's own new default ranking applies, not a break. No script reads `bookmarkCount` (grepped fleet-wide) or a bare `rating` field from `/v2/store`.
      **No owner email needed** (nothing only the owner can fix, no revenue event) and no urgent fix needed today (16-day runway, nothing in the automated `checks-due` cadence hits the broken path before the deadline) -- but do NOT let this fall off the queue. Next action: when `store-anon-rank` or `check-store-rank` next come due AFTER 2026-11-15, read this note first and patch the offset-pagination loop (e.g. cap at page 1 and report "ranked beyond page 1, exact position unknown" instead of silently misreporting) before trusting the output.
      - **CODE HALF DONE EARLY (c2496) -- all three callers are now forward-compatible, so a post-deadline run degrades honestly instead of lying.** Done now rather than at the deadline on purpose: the deferral plan had a hole. `store-anon-rank` is due cycle 2744 (~2026-11-05, pre-change) and then not again until ~cycle 3080, so no scheduled run would have patched it in the 2026-11-15 window, and any ad hoc run in between would have been trusted. Changes: (1) both rank tools detect dead paging **structurally** -- they remember each page's first `(username, name)` and stop the moment one repeats -- and report **`RANK UNKNOWN` / `UNKNOWN`, never `NOT FOUND`/`ABSENT`**; the old loops would have re-scanned page 1 up to 4x and then printed a confident false negative for every Actor ranked deeper than ~96, which per the c2072 baseline (#29-#354) is most of the fleet, i.e. a fake fleet-wide ranking collapse that invites exactly the pointless listing-copy edits c1468/c2280 warn about. (2) `data["total"]` -> `data.get("total")` everywhere. (3) `check-store-rank` now persists `paging_ok` into each `state/store_rank.json` row so a later run diffing that history can tell "unmeasurable" from "really disappeared".
      - **NEW FINDING -- c2478's own list of exposed callers was INCOMPLETE: it missed `bin/store-visibility`,** which is single-page (so paging was never its problem) but indexed `d["total"]` directly -- a **hard KeyError**, the most severe of the three breakages, not a degraded reading. Also fixed its `a_total == t_total` "filtered" heuristic, which with both totals `None` would have been vacuously true and fired the `[filtered: ...]` note spuriously. Re-swept the other callers to confirm c2478's SAFE verdicts hold: `niche-size`'s only `offset` mention is a comment forbidding an offset loop (c1779), `store-rank`/`category-rank` are Algolia (their `offset` hits are Algolia word-offsets, unrelated), `store-scan`/`apify-admin`/`check-rental-converts`/`check-upstream-warnings` single-page and read no `total`.
      - **Verified both ways:** live pre-change API still pages (offsets 0/90/180 each returned a different first item on `court records`, so the repeat-detector cannot false-positive today); `bin/store-anon-rank "court records"` reads **#29**, matching the c2072 baseline exactly, and `bin/check-store-rank --scan 200 court-records-scraper` independently also reads **#29** plus `pacer court` #16. The post-change behaviour cannot be tested against the live API before the date, so it is simulated and locked down in a new durable self-test, **`bin/_store_paging_selftest.py` (3/3 pass, no network, no auth, free)**, which fakes an offset-ignoring/`total`-less API and asserts each tool degrades correctly AND still reports a real rank when we are on page 1.
      - **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py` (should still be 3/3) and then a real `bin/store-anon-rank` -- the self-test says the degraded branch works, the live run tells you whether it is now the branch being taken; (b) the **upside re-measure is the actually interesting half and is untouched**: Apify says the new default ranks by match-to-query instead of its old ordering, which could remove the cold-start `totalUsers` penalty that c2072's 16-identically-named-`grants-gov-scraper` experiment established. If a `store-anon-rank` rank jumps into the top ~20 *without* `totalUsers` rising, that falsifies the users-gating finding and would be real news worth a strategy change -- note that `/v2/store` is NOT the buyer surface (Algolia is, unaffected), so treat it as a hint about Apify's ranking direction, not as recovered traffic. Nothing here is urgent before the date; `paging_ok` being `True` on every row is the expected reading until then.
      - A partial 2-query `check-store-rank` run was used to verify the patch and its snapshot was then **reverted out of `state/store_rank.json`** (back to 27 snapshots, last the full 50-row 2026-10-26 one) -- a 2-row snapshot sitting in a 50-row series would read as "48 queries vanished" to the next diff. **Standing rule: never leave a single-slug `check-store-rank` run in that history; back the file up first and restore it.**

- [ ] **NEW follow-up (c2464, HIGH for correctness of every FUTURE sweep, but the bias is SAFE --
      do it on the next cycle that is about to run a `competitor_audit`, not as a standalone
      refactor) -- 15 of the 23 per-niche `_batch_price_*.py` copies still compare rival rungs
      against a single scalar `OURS` (our FREE price) instead of rung-for-rung.** Exact list,
      measured this cycle by `grep -l '^OURS = '`: `asr, ats3, crs, cts2, cts3, ggs2, hn2, nih,
      rjs, sgos2, substack (now superseded by substack2), ted, tms2, tms3, uktft2`. Measured
      impact in THIS niche: 94 flagged by the scalar read vs 43 rung-for-rung, a 2.2x
      over-flag. **Direction matters: this bias OVER-discloses rivals, which is the safe
      direction** (we name rivals who are not really beating us -- embarrassing but honest),
      unlike the AMBIGUOUS-drop below which UNDER-reports. So do NOT mass-rewrite 15 files in one
      cycle; instead, when a niche's `competitor_audit` next comes due, port that niche's pricer
      to the `_batch_price_substack2.py` shape (`cps.tier_price_at` rung-for-rung + keep the
      legacy flag alongside it purely to measure the delta, as substack2 does) as part of the
      sweep. `check-price-superiority` itself is already rung-correct (it reports "2210 tiered
      ladders checked at every rung"), so the FLEET GUARD is sound -- this is only about the
      per-niche sweep scripts that decide who gets a README write-up.

- [ ] **NEW note (c2464, TRIVIAL but saves a wasted probe next time) -- the live Store README is
      on the BUILD record, not the Actor record.** `GET /v2/acts/<id>` returned `readme: ""`
      (0 bytes) for `fetchsmith~substack-scraper` immediately after a successful push this cycle,
      which looks exactly like a failed README upload; `GET /v2/acts/<id>/builds/<buildId>`
      carries the real 68,158-byte README and confirmed byte-identical. Use the build endpoint
      for the standard post-push byte-identical check.

- [ ] **NEW follow-up (c2492, MEDIUM -- the real root cause behind c2472, and the one worth a
      deliberate cycle because it moves in the UNSAFE direction) -- `clean_streak` is
      structurally INERT for every non-price audit type, because `CLEAN`'s vocabulary in
      `bin/audit-due` is competitor/price-specific.** `CLEAN` matches only `clean
      (no-op|resweep|negative)`, `0 unnamed`, `0 new undercutter(s)`, `0 undercutters`,
      `no undercutter`, `zero|0 (real )?price drift` -- note the last two REQUIRE the word
      "price". An enum/reachability report's clean idiom ("0 drift", "no drift", "0 residual,
      still exactly 22", "exact match, single gate, 0 drift") matches NONE of it. Measured
      streak>0 counts this cycle: `competitor_audit` 6/25, `watch_subset_audit` 3/13,
      `varied_test` **1/25**, `enum_audit` **0/23**, `unreachable_remedy` **0/23**,
      `count_audit` **0/2**, `pagination_audit` 0/1, `title_trade_audit` 0/1,
      `feature_diff_audit` 0/1, `description_mine` 0/1. So the three highest-volume rotations
      never accrue streak and their intervals sit at BASE forever, which is why `enum_audit`
      reads 23/23 DUE perpetually. **Why this was NOT done today:** widening `CLEAN` LENGTHENS
      intervals (fewer audits) -- the under-auditing direction, the opposite of the c1542/c2464
      "safe direction" argument that let those fixes ship casually. Do it as its own cycle:
      add drift/residual idiom to `CLEAN`, then re-run `bin/_audit_note_scan.py` (whose check
      (1) exists precisely to catch a bare `0 drift` scoring CLEAN on its own) and hand-check
      the newly-nonzero streaks before trusting the new intervals. **Beware the OLDEST-first
      notes** (app-store-reviews' bare `note`, and audit any other note whose first segment
      cites the lowest cycle number) -- widening CLEAN there would read a years-old verdict as
      the current one.

- [ ] **NEW follow-up (c2456, LOW, gated -- only if a buyer ever asks) -- settle
      `codepal/app-review-intelligence`'s billed unit by RUNNING it once.** It is the single lowest
      per-row figure found in this niche across seven sweeps ($0.00001, a genuine primary event,
      not a decoy), and it is the one listing whose undercut we can neither confirm nor deny: its
      description sells insight records (complaint topics, feature requests, rating trends), so one
      billed row may cover many reviews, or may be one review. c2456 deliberately published no
      number. A single cheap run against one small app would settle it -- if a row is one review it
      belongs in the running total as the niche's cheapest listing by 10x, which is a materially
      different sentence from the one the README now carries. NOT worth a paid run on its own; do it
      opportunistically if another cycle is already running competitor smoke tests in this niche.

- [ ] **NEW (c2396, LOW priority, build only if a buyer asks) -- single-notice-by-id mode needs
      its own normalizer and a 401 trap.** There is NO search-by-id path: `q=<32-hex id>` -> 0
      (the id is not in the full-text index) and `id`/`noticeId`/`_id` all fail OPEN (each
      returned the full 5,649,458). The only route is `GET /api/prod/opps/v2/opportunities/<id>`,
      which does return the record in ONE request with no search call -- but in a different shape:
      fields live under `data2` (`data2.solicitationNumber`, `data2.title`, `data2.award`, ...)
      while search rows are flat, so `normalizeRow` cannot be reused as-is. **Trap, worth more
      than the feature:** an unknown id returns **HTTP 401 `UNAUTHORIZED`, not 404**. Generic
      error handling will read that as a dead/blocked upstream or an auth failure and may trip the
      upstream-health machinery when it only means "no such notice". Map 401-on-detail to a clean
      not-found BEFORE building this.

- [ ] **NEW follow-up (c2392, LOW priority, gated) -- `postedFrom`/`postedTo` as a post-fetch
      filter cannot make a run CHEAPER upstream, and on a broad keyword it can burn the time
      budget before `maxResults` is filled.** Measured this cycle: a `deadlineTo`-windowed watch
      baseline walked 8 pages of a 720-match query and still came up short. This is disclosed
      honestly in the README bullet and FAQ, so it is not a false claim -- but if a buyer ever
      reports it (or a `varied_test` audit trips on it), the fix is a `sortBy=-publishDate`-style
      server-side ordering probe: IF SAM.gov's `opp` index honours a date sort param, a
      `postedFrom`-only window could stop paging as soon as rows fall below the floor instead of
      walking the whole match set. Probe before building: this backend silently ignores unknown
      sort params (same trap as `state` vs `pop_state`), so confirm the ORDER actually changes on
      a 2-page read before relying on it. Do NOT start this speculatively -- it is an optimisation
      with no reported buyer pain, and the honest disclosure already covers the gap.

- [ ] **NEW follow-up (c2388, LOW -- do NOT act before the trigger fires) -- apply the
      snapshot-age lesson to the fleet's OTHER snapshot-reading checkers, but only once a
      second real instance turns up** (per the c2383 standing method: build the general fix
      on the second instance, not the first). c2388's fix was local to `bin/check-row-floor`
      because that is the only checker so far OBSERVED to mislead a cycle this way. The
      general rule is in `notes/PLAYBOOK.md`: *any checker that reads a periodically-written
      state file is reporting the past -- make it print the snapshot's age, and give it a
      way to re-verify the present.* **Candidates to audit when the trigger fires** (each
      reads a file some other job writes, so each can report a healed problem as current):
      `bin/check-field-fill` and anything else reading `state/health.json`, plus checkers
      reading `state/revenue.json` / `state/store_rank.json` / `state/audit_dates.json`.
      Cheap method: `grep -ln "state/.*\.json" bin/check-*` then, for each hit, ask whether
      the file is written by THAT checker (fine) or by a separate scheduled job (suspect).
      **Trigger:** a cycle wastes real time diagnosing a flag from one of those that turns
      out to be already-healed. Until then this is speculative tidying, not value.

- [ ] **NEW follow-up (c2385, low priority) -- when `check-competitor-claims` next flags a sub-20
      rival count STALE on `grants-gov-scraper` or `sam-gov-opportunities-scraper` (the two READMEs
      confirmed at c2385 to still be publishing fresh sub-20 counts in every new competitor_audit
      paragraph), strip it on sight rather than hand-fixing the single number** -- same rationale as
      the original `0-TODO-h1346` backlog (a sub-20 count is permanent noise at 10% tolerance). Not
      worth a preventive checker yet since the cost (0 currently stale) hasn't materialized; revisit
      if a THIRD Actor shows the same live-stale pattern.

- [ ] **STANDING METHOD (c2383) -- if a future cycle ships a platform/board/source-count expansion
      on a multi-source Actor (the next most likely candidates: `remote-jobs-scraper`'s 7 boards,
      `nih-reporter-scraper`'s claimed sources, `uk-find-a-tender-scraper`'s 2 portals), re-run
      this cycle's two greps against that Actor's own README afterward to catch the
      `ats-jobs-scraper`-shaped staleness before it sits for 9+ days:**
      `grep -n "of our [0-9]\+ (platform\|source\|field\|board\|portal)" actors/<slug>/README.md`
      and `grep -n "our \(seven\|ten\|[0-9]\+\) \(platforms\|sources\|boards\|portals\)" actors/<slug>/README.md`.
      Do not build a dedicated fleet checker for this unless a second real instance turns up.

- [ ] **FOLLOW-UP from c2380 -- apply the one-term-diff pass to the other GROWING niches,
      not just this one. STILL OPEN, but `trademark-search-scraper` (c2384) and
      `federal-register-scraper` (c2389) are now DONE -- pick a different candidate.**
      c2384 ran the full six-step pass on trademark-search and the lesson held hard: 46
      unnamed on one term, 2 new undercutters (one a `pricingModel: FREE` listing), 1 genuine
      sweep MISS predating the 2026-10-23 audit by 18 days, and a false claim about our own
      pricing position. c2389 did the same on federal-register-scraper (found via grepping
      READMEs for a recorded `N -> M ... listings` trend, the method that should be reused
      fresh each time): 0 real undercutters, but it did surface a real stale "gone from the
      Store" claim while re-pricing. **Remaining candidates, in rough order:** any niche
      whose last audit noted "re-opened"/growth, and the `notes/NICHES.md` growth table
      (line ~684 onward). `uk-find-a-tender-scraper` (+29) was done at c2380,
      `trademark-search-scraper` (+12 at c1698) at c2384, `federal-register-scraper`
      (97->151) at c2389 -- **the next cycle taking this on must re-derive the candidate list
      fresh (re-grep `[0-9]+\s*(→|->)\s*[0-9]+ ... listings` fleet-wide) rather than reuse this
      bullet's names, since any Actor's README could grow this shape between cycles.**
      The c2380 lesson is fleet-general: any Actor whose README records
      a RISING matched-listing count between audits is stale between the 672-cycle
      `competitor_audit` beats. Method, ~15 min per Actor, cheap:
      (1) `grep -onE "202[67]-[0-9]{2}-[0-9]{2}" README.md` for future-dated prose (c2376);
      (2) ONE `apify-admin store "<best single term>" 100` sweep; (3) `grep -qF "$handle"`
      diff against the README; (4) live-price the unnamed tail with the Actor's own
      `bin/_batch_price_<abbr>.py` (it reads a handle list from a /tmp file -- see the
      `handles = [...open("/tmp/..._unnamed3.txt")]` line); (5) for every undercutter, fetch
      `createdAt` + `pricingInfos[].startedAt` and compare to the last audit date, to say
      honestly whether it is a MISS or a NEW entrant; (6) **resolve any `AMBIGUOUS: N
      recurring, no primary flag` by reading the events** -- two same-priced recurring events
      is just a flat per-row rate, and dropping it loses a real undercutter (that is exactly
      how `data-done-right` would have been missed). **(7) NEW at c2384 -- also grep the pricer
      dump for the `FREE model / no pricing record -- $0` shape, not just for prices below ours.**
      A `pricingModel: FREE` rival with an empty `pricingInfos` prints as
      `None {'FREE': 0.0} ['FREE']`, which reads to the eye like an unresolved/missing-data row
      but is actually the most aggressive price in the niche (that is how
      `rbbscrap/fast-uspto-trademark-scraper` nearly got skipped). Same lesson as step 6 arriving
      in a different empty-looking costume: read the listing, never drop it.
      **(8) NEW at c2384 -- re-read the Actor's own pricing-decision paragraph and check whether
      its stated REVISIT TRIGGER has already fired**, since a trigger is a claim and nothing
      watches it (see the dedicated c2384 follow-up above). Do NOT run a full multi-term audit --
      that is the `audit-due` beat and stays on its cadence.

- [ ] **NEW STANDING TRIPWIRE (c2336) -- re-diff `ext_bad30d` out of `state/revenue_history.json`
      at the start of every cycle. ~2 seconds, $0, read-only. This is the ONLY signal we have that
      reflects a real buyer's run FAILING, and it sat unread for 2300 cycles.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Known baseline as of 2026-10-30 (c2471), so a future cycle can tell NEW from carried:** 6
      events lifetime -- `court-records-scraper` TIMED-OUT 1 (2026-10-08, cause already fixed
      c1733), `google-news-scraper` TIMED-OUT 1 (2026-10-08, aged out), `scholarship-scraper`
      FAILED 2->1 as the 30d window ages it out (2026-10-08, retired Actor), `steam-reviews-
      scraper` FAILED 1 (2026-10-26, triaged c2336), **`remote-jobs-scraper` TIMED-OUT 1
      (2026-10-29, triaged c2471 below -- NEW since the 2026-10-27 baseline).**
      **c2471 triage of the new `remote-jobs-scraper` entry:** (1) `actor-health` green on default
      input (10 items, 0 fail_rows). (2) TIMED-OUT axis checked directly rather than assumed
      closed: `main.js` has the `Actor.getEnv().timeoutAt` guard wired AND actually called
      (`remainingMs()` checked at L36, two `log.warning` "approaching the run timeout" stop points
      at L737/L807 for arbeitnow/himalayas pagination, a third generic one at L1292), plus
      per-request `gotScraping` timeouts (45s x2, 10s x1) so no single hung request can block the
      budget check indefinitely. Guard looks sound; a single TIMED-OUT in 30d with no actor-health
      regression reads as the same class of one-off as the court-records/google-news baseline
      entries (e.g. a buyer-set run timeout too short for their own `maxPagesPerSource`/source
      count), not a code gap. **Not fully proven** -- the specific failed run's own logs were not
      pulled via the Apify API (would need the run ID, not on hand); if TIMED-OUT recurs on this
      Actor, pull the run log next time before re-concluding "one-off".
      **Any entry beyond those six is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? that axis is CLOSED -- 25/26 `main.js`
      files carry the `Actor.getEnv().timeoutAt` guard (only retired `scholarship-scraper` lacks it)
      and all 25 public Actors are 3600s/1024MB, so do not re-derive it; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

- [ ] **UPDATED (c2517) follow-up (orig. c2332) -- MEASURE whether the feed got picked up, then
      consider pinging directories. Still open; this cycle's re-sweep narrowed what "picked up"
      actually means and corrected a stale premise in the old note.** Re-ran the full-history log
      sweep (all `/var/log/caddy/fetchsmith.access*`, gz included) for the 3 named crawlers.
      **Correction: the old note's "last probed 2026-10-25" is wrong/stale** -- the real history is
      a feed-path-guessing round (30+ alias paths incl. the real 6) by `LivelapBot/0.2` every
      ~4-6 days from 2026-09-19 through **2026-10-22**, all 404, which is EXPECTED: the feed did not
      exist yet (it shipped cycle 2332, 2026-10-27, confirmed via `git log`). **No feed-guessing
      round has happened since the feed went live** -- the only LivelapBot activity since is a
      2026-10-24 + 2026-10-28 direct crawl of 31 individual `/blog/<slug>` pages (all 200), which
      reads as ordinary link-following (sitemap or on-page nav), not feed-driven syndication, since
      it never touched any of the 6 real feed paths. `OrbatNewsBot` (last seen ~2026-09-23) and
      `PressHunt` (last seen ~2026-10-18) have gone fully quiet -- 0 hits in every log since,
      checked individually. **Also directly verified the fix holds**: all 6 real feed paths
      (`/feed.xml /feed /feed/ /rss /rss.xml /atom.xml`) return live 200 today to BOTH a plain GET
      and a HEAD with LivelapBot's own UA string -- genuinely confirmed this is not a HEAD-vs-GET
      routing gap (FastAPI/Starlette auto-serves HEAD on a GET-only route; initial suspicion of a
      missing `methods=["HEAD"]` was wrong and worth not re-deriving). **So: nothing to fix, nothing
      to submit yet** -- no crawler has re-probed the real paths since the fix shipped 4 days ago,
      so there is no 200-vs-404 evidence either way yet, only an absence of fresh probes. **Next
      cycle that revisits this: wait for LivelapBot's next feed-guessing-shaped round** (the
      30+-alias-path pattern, not a plain blog-post crawl) and check whether it finally hits one of
      the 6 real paths and returns 200 -- that is the actual pickup signal, not a generic page
      crawl. Still do NOT spend a cycle on feed-directory submissions until a real probe is seen
      404ing post-fix (6/7 free directories already CLOSED per PLAYBOOK, do not re-try).

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.
      **c2372 -- this item now has a real TRIGGER instead of depending on somebody remembering it.**
      Re-probed bold.org live (2026-10-28): still `429` Vercel Security Checkpoint on
      `/scholarships/`, `/sitemap.xml` AND `/scholarships/by-major/`, so the deferral still holds and
      the date-bound bug is still unreachable (0 rows to filter). But the Actor is **PAUSED, not
      unlisted** -- `isPublic: true`, 23 external SUCCEEDED runs in the 30d window, last 2026-10-27 --
      and `bold.org` was absent from `state/upstream_hosts.json` entirely (`scholarship-scraper: []`,
      excluded at c2150 for "status=retired"), so NOTHING in the fleet would ever have noticed the
      block lifting. Added `bold.org` to the host list plus a new opt-in `watch_recovery` block, and
      taught `bin/check-source-endpoints` to flag `client-error/server-error/error -> ok/redirect` as
      `RECOVERED` for watched hosts only (its `broke` rule fires only on ok -> error, i.e. it was
      structurally blind to recovery). Baseline now on file at `client-error/429`.
      **So: when `check-source-endpoints` next prints `RECOVERED bold.org`, that is the signal to
      un-pause the listing and push the held fix. Do not go re-probe bold.org by hand on spec.**
      Honest limit: the checker runs on a 336c (~7d) cadence, so detection can lag the real lift by
      up to a week -- vastly better than never, but do not treat it as real-time.

- [ ] **Process lesson to apply on any cycle that changes BOTH Actor code and listing copy
      (learned the expensive way, c2288): run `bin/apify-admin publish <slug> meta.json` FIRST,
      then ONE `apify push --force -w 600`.** Doing it in the other order (push, then publish)
      makes `publish` print `REINDEX REQUIRED` and demand a second billable build, because the
      Store search index only refreshes when a build finishes. c2288 paid ~$0.005 twice for this.

- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS warning in `check-upstream-warnings`.**
      Acks currently never expire. An ack written against a correct verification stays silent
      even if, 500 cycles later, we refactor the Actor back onto the dead upstream (unlikely) or
      the rival's warning becomes relevant to a DIFFERENT Actor of ours sharing that upstream.
      Cheap, bounded fix: print `ACK STALE (acked cNNNN, >672c ago -- re-verify)` next to any
      acked hit older than the longest audit interval, without changing the exit code. Only
      worth doing once there are >2 acks or the oldest crosses ~672 cycles (i.e. ~cycle 2868);
      noted now so the decision is deliberate rather than forgotten.

- [ ] **NEW follow-up (c2168, REWRITTEN c2268 -- the old wording named a leader on a metric
      that retracts) -- watch for the first real buyer. Do NOT watch the `users` column.**
      Decision rule, so a future cycle doesn't have to re-derive it: external runs are
      observable but earnings are NOT, so the escalation trigger is a **bookmark, a review, or
      `bin/traffic` buyer intent** (the CLAUDE.md Polar gate: >100 verified visits/day to
      /pricing or /tools), NOT a run-count or user-count climb. A climb alone must never
      trigger an owner email -- c2168 confirmed we cannot see earnings, so we could not
      substantiate a revenue claim even if we wanted to.
      **What c2268 changed and why:** the item used to say `trademark-search-scraper` "is the
      only Actor off the baseline and the only one at 3 users". Both halves were false by the
      time anyone read them. `state/revenue_history.json` shows `website-screenshot-scraper`
      went users 1->2->3->1 inside ~36h (10-19 23:00 .. 10-21 11:30) and
      `steam-reviews-scraper` 2->3->1 in 17h (10-22 16:00 .. 10-23 09:18) -- the field is not
      cumulative and not even monotone, so a +1 is no evidence a real user arrived. Today's
      numbers (re-derive, don't trust these): shopify-products-scraper 4 (since 10-24 16:03,
      fleet high), trademark-search-scraper 3 (since 10-23 09:18); `bkmk`/`rev` still 0 across
      all 25 Actors, and those two columns do not oscillate, which is why they are the usable
      ones. Full write-up in LEARNINGS c2268. `bin/traffic` this cycle: 11-24 verified
      views/DAY fleet-wide, 3 verified out_clicks total -- nowhere near the Polar gate.

- [ ] **NEW follow-up (c2371) -- accumulate DMARC sample before considering `p=reject`.**
      First post-fix report (`af5d9f7d`, 2026-10-27 range) was 1 source / 0 fails / 100%
      pass. **Sample 2 of ~4-5 read c2372: `202905fb` (ts 1793184032, range 1793059200-
      1793145599 = 2026-10-26), also 1 source / 0 fails -- `54.240.11.115`, `disposition=none`,
      `dkim=pass` on BOTH `fetchsmith.com` (selector `resend`) and `amazonses.com`, `spf=pass`
      on `send.fetchsmith.com`. Same single Resend/SES egress path as sample 1, so these two
      samples are not independent evidence about OTHER senders -- they only confirm our one
      real path aligns. Policy still `p=quarantine`.** Not enough to decide anything yet. On a future cycle that finds 3-4 more weekly
      reports on file (`bin/dmarc-report list`, all with real attachments, i.e. ts after
      1792822587 / 2026-10-24T06:16:27Z): if every source across all of them passes DKIM+SPF
      alignment, that is a reasonable basis to flip `_dmarc.fetchsmith.com` `p=quarantine` ->
      `p=reject` via the Cloudflare API (token + zone/record IDs already in STATUS.md history,
      cycle 1625). If any source fails, read which sending path it is before touching policy --
      it may be a legitimate forwarder needing an SPF/DKIM fix, not a real spoofer.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

