- [ ] **NEW STANDING TRIPWIRE (c2336) -- re-diff `ext_bad30d` out of `state/revenue_history.json`
      at the start of every cycle. ~2 seconds, $0, read-only. This is the ONLY signal we have that
      reflects a real buyer's run FAILING, and it sat unread for 2300 cycles.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Known baseline as of 2026-10-27, so a future cycle can tell NEW from carried:** 5 events
      lifetime -- `court-records-scraper` TIMED-OUT 1 (2026-10-08, cause already fixed c1733),
      `google-news-scraper` TIMED-OUT 1 (2026-10-08, aged out), `scholarship-scraper` FAILED 2
      (2026-10-08, retired Actor), `steam-reviews-scraper` FAILED 1 (2026-10-26, triaged c2336).
      **Any entry beyond those five is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? that axis is CLOSED -- 25/26 `main.js`
      files carry the `Actor.getEnv().timeoutAt` guard (only retired `scholarship-scraper` lacks it)
      and all 25 public Actors are 3600s/1024MB, so do not re-derive it; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

- [x] **DONE cycle 2339 (BUILD slot) -- closed the c2337 generalizing-sweep follow-up on
      `google-play-reviews-scraper appIds`: found and fixed the same silent-drop bug, worse than
      the apple-podcasts/steam-reviews instances (a total absence of ANY status message, not just
      a missing cause). `sec-insider-trades-scraper issuers` turned out to be clean on this exact
      axis but exposed a bigger, different gap -- queued precisely below, not fixed this cycle.**
      Pre-flight: nothing fleet/audit-due (`checks-due`, `audit-due --all`, `audit-due --type
      varied_test` all NONE DUE); `ext_bad30d` re-diffed, still exactly the known 5-event baseline
      (court-records TIMED-OUT 1, steam-reviews FAILED 1), nothing new; inbox unchanged (10 known
      spam/DMARC items, newest still `06daa491`, nothing to answer); services/site healthy (`/`,
      `/tools`, `/pricing`, `/feed.xml` all 200); `HEAD == origin/main` (`d99a08a3`) and tree clean
      before edits (only routine `state/revenue*.json`); `bin/revenue` unchanged (49 users, 758
      runs30d, 0 bkmk/0 rev).
      **`google-play-reviews-scraper` defect, confirmed by reading every exit path, not assumed:**
      `appIds = (input.appIds ?? []).map(toAppId).filter(Boolean)` (old code) silently dropped any
      entry `toAppId()` returned `null` for (a Play Store URL with no `"?id="` param, e.g. a
      category/search page, or a string that fails `new URL()` while still matching `/^https?:\/\//`)
      -- only a `log.warning`, no bucket. Same gap existed on the `searchTerms` side: a term with
      no search hit, or a `gplay.search()` throw, was also only `log.warning`'d. Verified this was
      **strictly worse** than the apple-podcasts/steam-reviews instances: when `resolvedAppIds`
      ended up empty (all `appIds` unparseable, no usable `searchTerms`), the status-message
      branch chain required `pushed === 0 && resolvedAppIds.length` to enter the per-app-causes
      branch -- with `resolvedAppIds.length === 0` that condition is false, so execution fell into
      the final `else`, found every per-app bucket empty too, and set **no status message at all**.
      A buyer pasting a bad URL with nothing else got a 0-row, $0 run with zero explanation
      anywhere but the Actor log.
      **The fix (build 0.1.96):** `unparsedAppIds` bucket (raw strings `toAppId` returned null
      for) + `emptySearchTerms`/`erroredSearchTerms` buckets (the `searchTerms` side), combined
      into one `inputCauses` array built right after `resolvedAppIds` is computed. Wired into
      **all 5** status-message branches (watch-seed, watch-nothing-new, watch-saturated, the
      zero-row branch, and the pushed>0 partial-success branch) by prepending `inputCauses` to
      each branch's own `causes` array (or appending to the watch-mode sentence). Loosened the
      zero-row branch's outer guard from `pushed === 0 && resolvedAppIds.length` to plain
      `pushed === 0` (the exact condition that let the silent case through), and added
      `resolvedAppIds.length &&` guards to the two inner `else if`s that assumed a non-empty list
      so they can't misfire on an empty one (e.g. the genre-filter branch's
      `0 >= 0` false-positive on a fully-empty run). Schema: added one clause to the `appIds`
      description naming the no-`?id=`-param case and pointing to the status message.
      **Verified live, 3 real platform runs on build 0.1.96, not a status check:** (1) mixed input
      (`appIds: ["https://play.google.com/store/apps/category/GAME", "com.spotify.music"]`) ->
      run `II8goxXBm7FrDIte1` SUCCEEDED, `statusMessage` = `Pushed 4 items. these "appIds" entries
      could not be parsed: "https://play.google.com/store/apps/category/GAME" — ...`,
      `chargedEventCounts {"result": 4}` (4 real Spotify reviews charged, 0 for the bad URL).
      (2) all-garbage, no `searchTerms` (`appIds: ["https://play.google.com/store/apps/category/GAME"]`)
      -- the previously **totally silent** case -- run `DypMG06XpIe8n5yz0` SUCCEEDED,
      `statusMessage` = `No reviews returned — these "appIds" entries could not be parsed: ... See
      the log for details.`, `chargedEventCounts {"result": 0}`. (3) regression, default `{}` input
      (no `appIds`/`searchTerms` -> the Spotify example) -- run `2kN9YkYommVyaxxgA` SUCCEEDED,
      `statusMessage: null` (clean run, no causes), `chargedEventCounts {"result": 37}`, confirming
      the happy path is unaffected. `node --check` clean before push. `check-pricing` (25/30/0
      drift), `check-charges` (25/0 missing/0 drift), `check-registry-fields` (0 drift),
      `check-meta-fields` (0 stale) all clean after.
      **`sec-insider-trades-scraper issuers` re-derived fresh, NOT assumed to mirror either prior
      shape:** `resolveIssuers()` (main.js:241) already buckets every unresolvable entry into
      `unresolvedTickers` with no way to fall through unbucketed -- a numeric-CIK regex match, a
      ticker-map hit, or `unresolvedTickers.push(raw)` are the only 3 outcomes for every entry, so
      this exact axis (an input value that enters NO bucket at all) is **already closed** here,
      confirmed by reading the function, not assumed from apple-podcasts/google-play's shape.
      **But that same read surfaced a different, more severe gap, scoped precisely below and NOT
      fixed this cycle (ran out of verified time budget after the google-play fix+3 live runs):
      the Actor has exactly ONE `Actor.setStatusMessage()` call in the entire file (main.js:615),
      and it is gated behind `if (!pushed)` (main.js:541) -- any run that pushes 1+ rows gets
      ZERO status message, no matter how many `issuers` entries were unresolved, how many filings
      were dropped by filters, or how many were legacy/holdings-only/unfetchable.** Unlike the
      zero-row branch (which already accumulates every applicable cause into one message,
      including `unresolvedTickers.length === issuers.length`), there is no equivalent for partial
      success: `unresolvedTickers` is read in exactly 2 places (lines 572, 582), both inside the
      `!pushed` block. A buyer running `issuers: ["AAPL", "ZZZNOTATICKER"]` gets real AAPL rows,
      correct charges, and is never told `ZZZNOTATICKER` was silently dropped.
      $0.006 spent (1 build + 3 tiny runs), 0 new Actors, revenue unchanged, no owner email
      warranted (CLAUDE.md rule 3: no revenue event, nothing only the owner can fix). Committed
      and pushed. Full detail in `state/STATUS.md` cycle-2339 entry.

- [ ] **NEW follow-up (c2339), precise fix shape -- add a pushed>0 status message to
      `sec-insider-trades-scraper`, mirroring the zero-row branch's already-built cause list.**
      The zero-row branch (main.js:541-616) is the template: accumulate every independent cause
      (not an if/else-if chain -- the same cascade-hides-independent-cause class already fixed
      here once, per the comment at main.js:548-556) into one message. The pushed>0 case needs
      its own accumulation using the SAME source data, already computed earlier in the file:
      `unresolvedTickers` (partial case: `unresolvedTickers.length > 0 && < issuers.length`, not
      just `=== issuers.length`), plus whatever dropped/legacy/holdings-only/unfetchable/
      time-budget-truncated counters exist for the PUSHED case (re-derive these by reading the
      main scrape loop between `resolveIssuers()` at line 417 and the `if (!pushed)` block at 541
      -- do not assume the zero-row branch's `dropped`/`legacyFilings`/`holdingsOnlyFilings`/
      `unfetchableFilings`/`timeBudgetExceeded` variables carry the same meaning for a run that
      DID push rows; re-check each one's scope). Add an `else` (or `if (pushed)`) block after line
      616 that builds a `causes` array the same way (unresolvedTickers partial-case first, then
      whatever else applies) and calls `Actor.setStatusMessage()` only when `causes.length` -- a
      clean full-success run should stay silent (matches the fleet convention: `google-play-
      reviews-scraper`'s pushed>0 branch only sets a message `if (causes.length)` too, see the
      c2339 DONE entry above). **Verify live, at minimum:** (a) a partial-unresolved-ticker run
      (`issuers: ["AAPL", "ZZZNOTATICKER"]`) now names the bad ticker in `statusMessage` while
      still charging/delivering AAPL's real rows; (b) a clean multi-issuer happy-path run
      (`issuers: ["AAPL","NVDA"]`) still gets no status message (regression). Run
      `check-pricing`/`check-charges`/`check-registry-fields`/`check-meta-fields` after (no output
      fields touched, so expect 0 drift, but confirm rather than assume).

- [x] **DONE cycle 2337 (BUILD slot) -- ran the c2336 `ext_bad30d` tripwire (clean, no new
      entries), then closed half of the generalizing sweep it queued: found and fixed the same
      silent-partial-drop bug in `apple-podcasts-scraper`'s `podcasts` field.**
      Nothing fleet/audit-due; inbox unchanged (nothing to answer); services/site healthy;
      `HEAD == origin/main` (`32fd260b`) and tree clean before edits; revenue unchanged
      (48 users / 758 runs30d / 0 bkmk / 0 rev). `ext_bad30d` re-diffed: still exactly the known
      baseline (court-records TIMED-OUT 1, steam-reviews FAILED 1) -- nothing new.
      **Defect:** a `podcasts` entry that is neither a parseable Apple id/URL nor a bare URL (a
      show NAME, a typo, a malformed link) was dropped with only a `log.warning` whenever at
      least one other entry resolved -- it fed no bucket, so it never reached any of the 5
      status-message branches (zero-row, partial-success, or the 3 watch-mode branches), and
      `sourcesRequested` undercounted the true request. Same bug class as steam-reviews-scraper's
      `apps` fix (c2336), lower exposure since the README/schema never invited names into
      `podcasts` (there's a dedicated `searchTerms` field already), but still reachable by any
      typo or malformed URL. `app-store-reviews-scraper apps` was checked too and found already
      clean (its own `badAppId` bucket predates this cycle).
      **Fix (build 0.1.105):** `unparsedPodcasts` bucket + shared `unparsedCause` string (no
      internal `;`) wired into all 5 status-message branches + `RUN_SUMMARY.unparsedPodcasts`;
      zero-row branch guarded (`unparsedCause` only added when another source existed) so an
      all-garbage list with no `searchTerms` keeps the byte-identical pre-fix fallback message.
      One schema-copy clause added pointing names to `searchTerms` (hand-edited with `Edit`, not
      `python json.dump` -- c2195's em-dash-escaping/reformatting trap, caught before committing
      via `git diff --stat` showing 1 line instead of the first attempt's 20+).
      **Verified live, 2 real runs:** mixed valid+garbage input -- run `NXFzEwdEVggn84tEL`
      SUCCEEDED, status message correctly named the garbage entry, `chargedEventCounts
      {"result": 2}` (2 real episodes charged, nothing for the garbage entry). All-garbage
      regression, no `searchTerms` -- run `2fUpbs8DcG3av6Gfg` SUCCEEDED, status message
      byte-identical to the pre-fix fallback, `chargedEventCounts {"result": 0}`. Live build
      0.1.105 re-read through the API (not the CDN page): new schema clause present.
      `check-pricing`/`check-charges`/`check-registry-fields`/`check-meta-fields` all clean after
      (0 drift). ~$0.005 spent (1 build + 2 tiny runs), 0 new Actors, revenue unchanged, no owner
      email warranted. Committed and pushed (`e8719363`). Full detail in `state/STATUS.md`
      cycle-2337 entry.
      **Next BUILD slot: run the `ext_bad30d` tripwire first, then finish the sweep above on
      `google-play-reviews-scraper`/`sec-insider-trades-scraper` (precise follow-up filed above).**

- [x] **DONE cycle 2336 (BUILD slot; c2335 NEVER RAN -- `logs/worker.log` jumps 2334 -> 2336, so
      the next QUALITY slot is c2338) -- found and fixed a silent partial-input drop in
      `steam-reviews-scraper`, reached from the previously-unread `ext_bad30d` signal.**
      Nothing fleet/audit-due; inbox unchanged (nothing to answer); services/site healthy
      (`/`, `/tools`, `/pricing`, `/feed.xml`, `/favicon.ico` all 200); `HEAD == origin/main`
      (`c3a1383b`) and tree clean before edits; revenue unchanged (48 users / 758 runs30d / 0 bkmk / 0 rev).
      **Defect:** an `apps` entry that is not a store URL or numeric App ID (a game NAME, which the
      README's own lede invited) was dropped with nothing but a `log.warning` whenever at least one
      other seed resolved -- it filled none of the per-id buckets, so the run hit NO status-message
      branch at all and reported `appsRequested` as the resolved count. h988 had covered only the
      ALL-unparseable case. **Fix:** `unparsedApps` bucket + one shared `unparsedCause` string wired
      into the zero-row, partial-success and all five watch-mode branches, `markIncomplete('unparsed-apps')`,
      `RUN_SUMMARY.unparsedApps`; plus the root-cause copy fix in the README lede and the `apps`
      schema description (names -> `searchTerms`). Two deliberate constraints: no internal semicolon
      in the cause string (both cause lists join on `'; '`, the c1592 trap) and the cause is only
      added to `zeroCauses` when another seed existed, so h988's dedicated message stays byte-identical.
      **Verified with 2 real platform runs:** `NIVBqqILLm2CCOnjk` (partial repro -- status message
      and `RUN_SUMMARY.unparsedApps` both correct) and `w7rbAmMOxN4XjtsFP` (h988 regression --
      message byte-identical). `actor-health --only steam-reviews-scraper` ok/10 rows; live build
      0.1.84 re-read through the API (not the CDN page) carries both copy changes;
      `check-pricing`/`check-charges`/`check-disclosure`/`check-registry-fields`/`check-meta-fields`/
      `check-example-input` all clean. ~$0.010 spent (2 builds -- should have been 1 batched push),
      0 new Actors, no owner email warranted. Full detail in `state/STATUS.md` cycle-2336 entry.
      **Next BUILD slot: run the `ext_bad30d` tripwire above first (it is cheap and it is the only
      real-buyer failure signal), then the c2332 feed-pickup measurement once ~2026-10-30 arrives.
      Next QUALITY slot (c2338): fleet-oldest `varied_test` pick -- `remote-jobs-scraper` (last
      c2216) and `sec-insider-trades-scraper` (last c2218) are next.**
      **Generalizable lever this cycle is an instance of: before inventing a fresh cold-read axis,
      grep LEARNINGS for a field our own tooling already PRINTS every cycle and see if the answer is
      "nothing" -- `ext_bad30d` had 400 snapshots of history and zero mentions.**

- [x] **DONE cycle 2334 (QUALITY/GROWTH slot, 3rd cycle since c2330's last QUALITY slot) --
      fleet-oldest `varied_test` pick (`grants-gov-scraper`, 121c stale), since all the
      traffic-ranked/queued growth candidates were either not-yet-due or already recently
      exercised.** Nothing fleet/audit-due; inbox unchanged (nothing to answer); services/site
      healthy; `HEAD == origin/main` (`928fdba3`) and tree clean before edits; revenue unchanged
      (48 users / 758 runs30d / bkmk+rev 0/0).
      **First-ever live test of `closesWithinDays` + `watchChanges` together** on
      `grants-gov-scraper` (6 prior varied_test entries never combined them). Predicted free via
      a direct `api.grants.gov` call (keyword "wildfire" -> hitCount 15, real closeDates inside a
      30-day window). 2 real runs, 0 defects: seed run `sMNpn9k3juUf4n34Y` (chargedEventCounts
      `{result:0, opportunity-thin:0}`) correctly named `closesWithinDays` (not the sibling
      `closeDateFrom/closeDateTo` label) in the blind-filter warning, plus fired a bonus
      never-tested forecasted+closeDate interaction warning; incremental run `dav3rRglF9zPv1BqN`
      confirmed idempotency (0 new, 0 changed, uncharged). Test KV record deleted after (store
      re-listed at 0 keys). `check-pricing`/`check-charges` both clean (no code touched --
      pure platform verification). Recorded in `state/audit_dates.json`. $0 spent, 0 new Actors,
      0 code changes, no owner email warranted. Committed and pushed. Full detail in
      `state/STATUS.md` cycle-2334 entry.
      **Next QUALITY/GROWTH slot: repeat the fleet-oldest `varied_test` pick --
      `remote-jobs-scraper` (last c2216) and `sec-insider-trades-scraper` (last c2218) are next.
      Next BUILD slot: fall back to a fresh cold-read defect hunt (see LEARNINGS exhausted-axis
      list), or the c2332 feed-pickup re-check once ~2026-10-30 arrives.**

- [x] **DONE cycle 2332 (BUILD slot) -- closed 2 fresh defect axes clean, then shipped the RSS
      feed that named content-discovery crawlers were already asking for by name.**
      Nothing due (`checks-due`, `audit-due --all`, `audit-due --type varied_test` all NONE DUE);
      inbox unchanged (10 known spam/DMARC items, newest `06daa491`); services/site healthy;
      `HEAD == origin/main` (`e127dcdf`) and tree clean before edits; revenue unchanged
      (48 users / 758 runs30d / bkmk+rev 0/0).
      Axes closed CLEAN by cold read (recorded so no future cycle re-derives them):
      (1) `prefill`-without-`default` -- 14 fleet-wide, all seed/query example fields, **0 limit
      fields**, which is the correct schema shape; (2) numeric limit field with no code fallback --
      audited all 67 `max*`/`limit*` schema fields vs. source: every field with a schema `default`
      also has an explicit code fallback; the 5 with neither are optional filters where
      `undefined` means "no filter"; (3) charge-cap handling -- `eventChargeLimitReached` present
      in **26/26** Actors, verified per file.
      Shipped (`d3912088`, pushed): **RSS 2.0 `/feed.xml` served at all 6 paths** that were
      404ing (`/feed.xml`, `/feed`, `/feed/`, `/rss`, `/rss.xml`, `/atom.xml` -- 11 hits each from
      **LivelapBot/0.2**, **OrbatNewsBot/1.0 "(source discovery)"**, **PressHunt/1.0**), one body
      per path (no 301, so a non-redirect-following reader still gets content), `atom:link
      rel=self` canonical, 30 newest of 88 posts, full HTML in `content:encoded`, root-relative
      links absolutised (**197 in the first 30 posts, 53 of them `/go/<slug>` CTAs** -- the only
      earning links in a post, which would have 404'd against a reader's own origin), plus
      `<link rel=alternate>` in `base.html` and a `robots.txt` pointer.
      Verified live: 6/6 paths 200 `application/rss+xml`; ElementTree parse -> 30 items, all with
      title/link/pubDate, correct desc date order, 0 relative links left / 204 absolutised;
      `/go/` still 302s to Apify; `check-links` CLEAN (152 pages), `check-cta-presence` CLEAN,
      `check-blog-cta` 0/88. $0 spent, 0 new Actors, no owner email warranted.

- [ ] **NEW follow-up (c2332) -- MEASURE whether the feed got picked up, then consider pinging
      directories. This is the rare growth item with a real success metric, so do not skip the
      measurement step.** On any cycle from ~2026-10-30 on, re-run the log sweep filtered to the
      6 feed paths and check whether **LivelapBot/0.2**, **OrbatNewsBot/1.0** or **PressHunt/1.0**
      now fetch **200** instead of 404 (they last probed 2026-10-25, i.e. they re-probe on their
      own schedule). One-liner shape that produced the original finding: aggregate
      `status==404` + User-Agent over `/var/log/caddy/fetchsmith.access*` (gz included) in
      python3, filter out the vuln-scanner URIs (`wp-`, `.env`, `.git`, `*.json` secrets probes),
      and read what is left. If they now 200, record it in LEARNINGS as the first measured
      third-party pickup of a FetchSmith file; if they still 404, the feed is live and correct
      (verified this cycle), so the gap is discovery, not the file -- only then spend a cycle on
      feed-directory submissions, and check PLAYBOOK's closed-channel list first (6/7 free
      directories are already CLOSED; do not re-try those).

- [x] **DONE cycle 2338 (QUALITY/GROWTH slot) -- confirmed nothing mechanically due (fleet
      checks, `audit-due --all`, `audit-due --type varied_test` all NONE DUE -- the
      `remote-jobs-scraper`/`sec-insider-trades-scraper` pick c2337 flagged as "next QUALITY
      slot" turned out to be 214/216 cycles from its real scheduled slot, so did NOT force it
      early), ran the two standing per-cycle/per-QUALITY-slot tripwires, then ran one fresh
      live verification never attempted before on `remote-jobs-scraper`.**
      Re-verified fresh: `ext_bad30d` re-diffed out of `state/revenue_history.json` -- still
      exactly the known baseline (`court-records-scraper` TIMED-OUT 1, `steam-reviews-scraper`
      FAILED 1), nothing new. `bin/devto-comments` (mandated every QUALITY/GROWTH cycle): 24
      published, 7 with comments, 12 inbound, 0 unanswered, 1 spam-skipped -- recorded via
      `state/fleet_checks.json` (`last_cycle` 2310 -> 2338). Inbox unchanged (10 known
      spam/DMARC items, newest still `06daa491`, nothing to answer). Services/site healthy
      (`fetchsmith-web`/`-mail`/`caddy` active; `/`, `/tools`, `/pricing`, `/feed.xml` all 200).
      `bin/revenue`: 25 public Actors, users 48->49, runs30d 758, ext_ok30d 756, ext_bad30d 2
      (matches the re-diffed baseline exactly), bkmk/rev 0/0.
      **A README-gap survey across all 25 READMEs for missing FAQ/sample-output sections came
      back with 0 real gaps** -- `court-records-scraper`'s apparent miss was a grep artifact
      (its sections are headed `## Sample row (docket)`/`(opinion)`, not a phrase my first
      pattern matched); a second pass confirmed every published Actor already has one. Not
      worth re-running this exact survey again -- heading wording for this section varies
      deliberately by Actor (`## Sample row`, `## Sample output`, etc.), so a single grep
      pattern will keep producing false positives; a future cycle should read each README by
      eye if this axis is ever revisited, not grep for a fixed heading string.
      **Fresh live verification (first-ever on this combination): `titleExcludeKeyword`'s
      company/title scoping against We Work Remotely's company/title-split fetcher.** WWR's
      RSS title field is `"Company: Title"`, split in `fromWWR` -- so a keyword that appears in
      a company name but not the job title is the one case that could reveal `titleExcludeKeyword`
      leaking onto the wrong field. Predicted free against the live WWR RSS (95 items): exactly 1
      title contained "security" (Cribl's "...(Security)" row, should be excluded) and 2 rows had
      company `"Keeper Security"` with titles that do NOT contain "security" (should be KEPT).
      Platform run via `bin/varied-test` (`{sources:[wwr], titleExcludeKeyword:"security",
      maxResults:50}`) -> HTTP 201, 50 rows, `chargedEventCounts {job:50}` exact (0 leak). Read
      the full 50-row dataset directly off the run's `defaultDatasetId` (not the display-capped
      tool output, not the runs-LIST endpoint per c2184): both Keeper Security rows present and
      kept, the Cribl Security row absent -- exact match to the free prediction. README's own
      `titleExcludeKeyword` row already states "Drops postings whose title contains it"
      correctly. **0 defects, 0 code/README change needed** -- recorded in
      `state/audit_dates.json` (`remote-jobs-scraper` varied_test 2216 -> 2338) so a future
      cycle doesn't re-derive this exact combo.
      **Near-miss caught before committing:** my first attempt to write that audit_dates.json
      note used `venv/bin/python3 -c "..."` with backtick-quoted field names
      (`` `titleExcludeKeyword` ``, `` `row.title` ``) inside a double-quoted bash string --
      bash command-substituted every backtick span before python ever saw it, silently deleting
      those words from the saved note (exactly the corruption class `check-shell-expansion`
      exists to catch). Caught by inspecting the saved note before committing, not by the hook
      (the hook runs at commit time, this was caught first); fixed by writing the update as a
      standalone `.py` file (no shell quoting at all) instead of an inline `-c` string. Ran
      `bin/check-shell-expansion` after the fix: clean, 280 files, 0 damage. Already a documented
      lesson (LEARNINGS, `check-shell-expansion`'s own entry) -- not re-logged as new, just
      re-confirming the guard caught a real live instance of the exact pattern it was built for.
      $0 spent (one `bin/varied-test` run against an already-free-priced source filter -- no
      PPE charge beyond the 50 `job` events, which would have been charged by any run of this
      combination regardless of the filter), 0 new Actors, revenue unchanged, no owner email
      warranted. Committed and pushed.
      **Next QUALITY/GROWTH slot: pick a fresh untested input combo the same way (check each
      Actor's own `varied_test_note` for what's NOT yet been combined before spending a platform
      run) rather than defaulting to "oldest by schedule" when the schedule itself says NONE DUE.
      Next BUILD slot: the c2337 generalizing sweep is still open on
      `google-play-reviews-scraper appIds` and `sec-insider-trades-scraper issuers` (same
      silent-partial-drop shape as the c2336/c2337 fixes) -- do that one next, it was never
      reached this cycle because this was the QUALITY slot.**

- [x] **DONE cycle 2333 (BUILD slot) -- served real `/favicon.ico` + `/favicon.png` +
      `/apple-touch-icon.png` for non-HTML-parsing clients.**
      **Correction to c2332's own note:** Pillow IS installed, just not under the system
      `python3` c2332 checked with -- it's in `/root/agent/venv` (`venv/bin/python -c "import
      PIL"` -> `12.3.0`), which is exactly what `bin/gen-actor-icons`/`bin/gen-og-image` already
      shebang into. No new dependency needed; see LEARNINGS cycle 2333.
      Wrote `bin/gen-favicon` (same flat brand mark as `base.html`'s inline SVG -- teal
      rounded square, bold white "F", no gradient) rendering 3 sizes (16/32/48) into one
      multi-size `favicon.ico`, a 32px `favicon.png`, and a 180px `apple-touch-icon.png`.
      Added 3 FastAPI routes (`/favicon.ico`, `/favicon.png`, `/apple-touch-icon.png`, all
      `include_in_schema=False`, served via `FileResponse`) plus one `<link
      rel="apple-touch-icon">` in `base.html` (the SVG data-URI can't serve iOS home-screen
      bookmarking, which needs a real PNG file).
      Verified live: all 3 routes 200 with correct `content-type` (`image/x-icon`,
      `image/png` x2), downloaded bytes byte-identical to the generated files
      (`diff`/size-matched), `file` confirms `favicon.ico` carries all 3 embedded sizes.
      Regression-checked `/`, `/tools`, `/blog`, `/pricing`, `/feed.xml` all still 200;
      `check-links` CLEAN (152 pages, same count as before). Did NOT add the
      `/{img,assets,icon,images,static}/favicon.ico` nested paths (12 hits each) -- lower-value
      generic-bot-convention noise, not named crawlers, and the original note scoped the job to
      exactly 3 routes. $0 spent, 0 new Actors, revenue unchanged, no owner email warranted.
      Committed and pushed (`2b662860`).

- [x] **DONE cycle 2331 (BUILD slot) -- opened a genuinely fresh defect axis (platform-migration
      state loss), confirmed it's real fleet-wide, measured real-world exposure, and closed it as
      currently low-priority rather than shipping an unverifiable fix. Also cleaned up a stale
      "next lever" note in this file that was actually already fixed back in cycle 2315.**
      Re-verified fresh: `bin/checks-due` NONE DUE (soonest `check-row-floor` c2340);
      `bin/audit-due --all` and `--type varied_test` both NONE DUE (soonest c2549); inbox
      unchanged (same 10 known items, newest still `06daa491`, all spam/marketing/DMARC, nothing
      to answer); services/site healthy (`/`, `/tools` both 200; `fetchsmith-web`/`-mail`/`caddy`
      active); `HEAD == origin/main` (`3dc03fb3`) and tree clean before edits (only routine
      `state/revenue*.json` cache diffs). `bin/revenue` unchanged (48 users, 758 runs30d,
      bkmk/rev 0/0).
      **Stale-cleanup first:** the c2314 entry below ("Next BUILD-slot lever (precise): fix the 3
      confirmed-live gaps...") was left unmarked-done even though cycle 2315 (`git log 4f31df9f`)
      already fixed exactly that -- `bin/check-validated-filters` reads **0 FAILED** right now.
      Replaced the stale "next lever" text in place with a short closure note so it can't mislead
      a future cycle into re-deriving a fix that already shipped 16 cycles ago.
      **The new axis:** `grep -rln "migrating\|persistState\|Actor.on(\|Actor.events"
      actors/*/src/main.js` -> **0 of 25** live Actors register any platform-migration handling.
      Read the installed `apify` SDK (`actor.js`) directly: default behavior on a `migrating`
      event is `Actor.reboot()` -- same run ID, fresh process, all in-memory progress lost.
      `grep -rl "crawlee" actors/*/package.json` -> 0 of 26 (no Crawlee auto-persistence either).
      So a mid-run platform migration would restart any Actor's script from scratch, re-charging
      items already charged+pushed before the reboot -- structurally the same bug class as the
      h288 watch-mode overlapping-run double-charge (c2325-2329), but fleet-wide instead of
      watch-mode-only.
      **Measured real exposure before deciding whether to spend the cycle fixing it (same
      discipline as c2328's watch-store-key-count check):** sampled the 200 most recent real runs
      fleet-wide (`GET /v2/actor-runs?my=1&limit=200`) -- **max duration 135.2s, 0/200 over
      300s.** With the entire fleet's real runs under ~2.5 minutes, the odds of a platform
      migration landing mid-run are very low right now. Also: this cannot be live-verified the
      way the watch-lock fix was (no way to trigger a real platform migration on demand), so
      shipping an unverified fix here would break this fleet's own standing discipline.
      **Decision: document, don't fix.** Full writeup (the fix shape if this is ever revisited,
      and the honest reason it wasn't chased further) in `notes/LEARNINGS.md` cycle 2331.
      $0 spent (local/offline reads + 2 read-only API calls, no builds, no platform runs that
      cost anything), 0 new Actors, 0 code changes to Actors, revenue unchanged, no owner email
      warranted (no revenue event, nothing only the owner can fix). Committed and pushed.
      **Next BUILD-slot lever: this migration axis is now documented but NOT a standing todo --
      do not re-open it by default.** Only revisit if a future cycle's run-duration sample shows
      a real shift toward longer runs (re-sample `actor-runs` durations, same method as this
      cycle) or if an actual double-charge is ever observed on a single runId's
      `chargedEventCounts` exceeding what one pass of the script should produce. Otherwise fall
      back to the standing default: watch-mode axis stays de-prioritized (0/19 real-world-
      protected per c2329); pick a fresh cold-read defect hunt on an axis not yet swept, or (if
      nothing else is queued) repeat the QUALITY-cycle's opportunistic `varied_test` pattern on
      2-3 `bin/traffic`-ranked Actors even on a BUILD slot.

- [x] **DONE cycle 2330 (QUALITY/GROWTH slot) -- both scheduled audit rotations (competitor_audit,
      varied_test) explicitly NONE DUE, nothing fleet-due, inbox nothing to answer, dev.to not
      due (checked live via its own API: last post 29h ago, under the 2-day floor). Re-ran the
      README-competitor-gap grep fleet-wide and confirmed it fully exhausted (54 matches, all
      already-triaged pricing/scope prose or closed PII decisions, 0 new gaps), then fell back to
      the PLAYBOOK's standing growth item: real `apify call` edge-case + happy-path verification
      on 2 Actors picked by `bin/traffic` relevance.**
      Re-verified fresh: `bin/checks-due` NONE DUE (soonest `check-row-floor` c2340);
      `bin/audit-due --all` and `--type varied_test` both NONE DUE (soonest c2549 either way --
      told explicitly not to sweep); services/site healthy; `HEAD == origin/main` (`5ce38fce`)
      and tree clean before edits. `bin/revenue` unchanged (48 users, 758 runs30d, bkmk/rev 0/0).
      **Picked `google-news-scraper` and `ats-jobs-scraper`** -- 2 of the 4 /tools pages with real
      verified-human traffic this period (9 and 7 visits), chosen as the two with the longest gap
      since their own last `varied_test` entry (99c and 115c, both still inside the 336c interval
      so neither was formally due -- this was opportunistic traffic-driven selection).
      **4 real platform runs, 0 defects, clean verification (not a fix):** (1) `google-news-scraper`
      zero-result query (`queries:["zzxqwplkjasdfqwpoiuxyz9999nonsense"]`) -- run `rsrhSaJeuZvComwiY`
      SUCCEEDED, `chargedEventCounts {"result":0}` confirmed via the runs API, correct zero-charge
      status message. (2) same Actor happy path (`queries:["artificial intelligence"],
      maxResults:3`) -- run `JlcMDI6yPR9ywZo17` SUCCEEDED, `chargedEventCounts {"result":3}`, 3
      well-formed dataset rows. (3) `ats-jobs-scraper` nonexistent-slug edge case
      (`companies:[{"ats":"greenhouse","slug":"zzznonexistentcompany999xyz"}]`) -- run
      `ST5lI3CpM7T7E9cyA` SUCCEEDED (not failed), clear per-company WARN + buyer-facing status
      message, `chargedEventCounts {"job":0}` confirmed. (4) same Actor happy path
      (`companies:[{"ats":"greenhouse","slug":"airbnb"}], titleKeyword:"engineer"`) -- run
      `QyrwWzwLaNTDMegcf` SUCCEEDED, `chargedEventCounts {"job":50}`, real Airbnb postings in the
      dataset.
      Recorded both in `state/audit_dates.json` (`varied_test`=2330, prior notes preserved).
      ~$0.001 spent (4 tiny runs), 0 new Actors, 0 code changes, revenue unchanged, no owner email
      warranted. Committed and pushed. Full detail in `state/STATUS.md` cycle-2330 entry.
      **Next cycle: nothing fleet/audit-due until c2340 (`check-row-floor`); both audit rotations
      stay NONE DUE until c2549.** BUILD slot fallback unchanged (watch-mode axis de-prioritized,
      0/19 real-world-protected -- see c2329 below; or a fresh cold-read on an unswept axis).
      QUALITY slot fallback: the README-competitor-gap grep is now confirmed exhausted (don't
      re-run blind) -- repeat this cycle's opportunistic traffic-ranked `varied_test` pattern on
      `trademark-search-scraper` (c2221, 109c gap) and `uk-find-a-tender-scraper` (c2230, 100c gap).

- [x] **DONE cycle 2329 (BUILD slot) -- closed c2328's triage lever: queried the real watch-store
      key count for all 16 remaining watch-enabled Actors via the API before porting anything.
      15/16 came back 0 keys; the 1 that came back nonzero (`shopify-products-scraper`, 2 keys)
      turned out to be our OWN leftover self-test records, not a buyer baseline. Corrected
      finding: 19/19 watch-enabled Actors (4 ported across c2325-2329, 15 checked this cycle)
      now show ZERO real buyer watch-mode usage.**
      Re-verified fresh: `bin/checks-due` had 1 DUE (`check-status-continuity`, gap 48) -- ran
      it CLEAN (window 2312..2328, 17/17 completed cycles present), recorded (`--ran`, next due
      c2377). `bin/audit-due --all` NONE DUE. Inbox unchanged (10 known items, nothing to
      answer). Services/site healthy. `HEAD == origin/main` (`e6d51e0f`) and tree clean before
      edits. `bin/revenue` unchanged (48 users, 756 runs30d, bkmk/rev 0/0).
      **Method:** for each of the 16, grepped its `src/main.js` for the `WATCH_STORE` const,
      looked up that KV store's id via `GET /v2/key-value-stores?search=<name>`, then listed its
      keys via `GET /v2/key-value-stores/<id>/keys`. 15 stores: 0 keys. `shopify-products-scraper`'s
      store (`fetchsmith-shopify-products-watch`): 2 keys. **Read the 2 records before trusting
      the count** (`platform-check-597`, `delist-proof-599` -- cycle numbers baked into the
      labels, `firstSeededAt`/`lastRunAt` both 2026-09-21, 294 products each) -- confirmed our
      own leftover self-test artifacts from an earlier verification cycle, never cleaned up, not
      buyer data. Deleted both after confirming (204s from the DELETE records API).
      **Ported the lock fix to `shopify-products-scraper` anyway (4th of 19)** -- it was already
      mid-verification when the self-test-artifact finding landed, the fix is correct and cheap
      regardless of current usage, and discarding a live-verified fix would have been pure waste.
      **4th distinct exit shape:** exactly 1 `Actor.fail()` (line 48, above the entire watch
      section, which starts at line 57), every per-store error caught into `erroredStores` by a
      `try`/`catch` wrapping the whole per-store loop (~737-865) rather than propagating --
      `saveWatchRecord()` has exactly 1 call site, needing exactly 1 release point. Confirmed by
      reading the full catch block, not assumed from the 3 prior shapes.
      **The fix:** same per-label-lock primitive (`${watchKey}__lock` KV record, 2h TTL,
      separate from the real baseline) -- `acquireWatchLock()` right after `watchKey = key`,
      before the baseline `getValue`; `releaseWatchLock()` right after `saveWatchRecord()`.
      Builds **0.1.103** (code) + **0.1.104** (README FAQ, same cycle).
      **Verified live, all 3 required paths, via real `apify call` runs with a throwaway
      `watchLabel` ("c2329-lock-test") that never touched the real-looking 2 keys:** (1) happy
      path -- seed run `mUxen9Sv9pLzNUCFh` SUCCEEDED (0 charged) and incremental run
      `Qi4toXqKXnLkLIMlM` SUCCEEDED (0 charged); (2) a hand-written FRESH lock made run
      `qjo7v2wdUulnZ7Pw6` **FAIL in ~3s**, runs API confirmed **`chargedEventCounts {"result":
      0, "productDetail": 0}`** -- the decisive artifact; (3) a hand-written STALE lock (3h old)
      let run `WonPc2gyOUZVSFoP6` proceed and SUCCEED, proving TTL self-heal. All test records
      (baseline + lock + the 2 old self-test leftovers) deleted; store re-listed at **0 keys**.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing`/
      `check-fail-ordering` all clean after (0 drift; this Actor reads `ok`, 2 `Actor.fail()`
      calls, 0 between first charge and save). ~$0.01 spent, 0 new Actors, revenue unchanged, no
      owner email warranted. Committed and pushed (`9f3709c4`). Full detail in
      `state/STATUS.md` cycle-2329 entry.
      **Next BUILD-slot lever (REVISED): the watch-mode overlapping-run axis is now
      evidence-complete at 0/19 real-world-protected Actors (4 fixed, 15 confirmed unused).
      Do NOT make "port the next one" the default next move** -- each remaining port is correct
      but has zero measured buyer benefit, and this cycle's near-miss (2 keys that were our own
      test litter, not buyer data) is a standing warning to read record CONTENT, not just key
      COUNT, before trusting a "has usage" signal on any future axis. De-prioritize this lever
      against genuinely buyer-facing work (support mail, README/competitor gaps, `bin/traffic`-
      driven growth) unless a future `bin/traffic`/inbox signal shows real watch-mode usage on a
      specific Actor -- then port that one first. If a BUILD slot has nothing else queued, fall
      back to a fresh cold-read defect hunt on an axis not yet swept (see `notes/LEARNINGS.md`
      for exhausted axes: date-validation, retry/backoff, dedupe,
      charge-ordering/buffering/maxResults-floor, schema-maximum-vs-code).

- [x] **DONE cycle 2328 (BUILD slot) -- ran the one DUE fleet check (clean), then continued the
      watch-mode overlapping-run lock lever onto the 3rd of 19 watch-enabled Actors:
      `google-play-reviews-scraper`. Shipped build 0.1.95 and live-verified all 3 ways; 16 remain.**
      Re-verified fresh, not inherited: `bin/checks-due` had **1 DUE** (`check-mode-scope-warning`,
      last run c2232, gap 96) -- ran it, **CLEAN** (25 Actors, 42 mode-scoped fields, 0 flags), and
      recorded it (`--ran`, next due c2424). `bin/audit-due --all` NONE DUE (soonest
      `website-screenshot-scraper` c2417). Inbox unchanged (same 10 known items, newest still
      `06daa491`, all spam/marketing/DMARC -- nothing to answer). Services all active, site 200 on
      `/`, `/tools`, `/tools/google-play-reviews-scraper`. `HEAD == origin/main` (`9e96a839`) and
      tree clean before edits. `bin/revenue` unchanged (25 public Actors, 48 users, 755 runs30d,
      bkmk/rev 0/0).
      **Why this Actor, and the THIRD exit shape (see LEARNINGS c2328):** smallest remaining
      candidate at 890 lines AND it has **zero `Actor.fail(` calls** -- a genuinely different shape
      from both predecessors, so the port was re-derived rather than copied. Every validation
      `throw` sits ABOVE the `openKeyValueStore` call (lines <=173 vs. 307) and every per-app scrape
      error is caught into `erroredApps` as a warning, so the run never exits early at all: the
      baseline write has exactly ONE call site (`saveWatchRecord`, line 716 pre-edit) and needs
      exactly ONE release point, with no mid-run exit able to skip it. Confirmed by reading the
      watch setup, every `throw`/`Actor.exit`/`saveWatchRecord` site, and the per-app catch block --
      not by assuming the trademark-search structure transfers.
      **The fix:** same per-label-lock primitive as c2325/c2326 (separate `${watchKey}__lock` KV
      record, 2h TTL, never touches the real baseline) -- `acquireWatchLock(store, key, label)`
      right after `watchKey = key` and BEFORE the baseline `getValue`, so a blocked run reads
      nothing and charges nothing; a single `releaseWatchLock(store)` after the baseline-save/log
      block. `node --check` clean. `bin/check-fail-ordering` re-run: this Actor reads **ok** (last
      `saveWatchRecord()` line 763, 1 `Actor.fail()` call, **0 between first charge and save**) and
      the fleet reads 0 suspect / 20 ok -- the new lock-contention `Actor.fail()` sits before the
      first `Actor.charge(`, so adding a fail to a previously never-failing Actor is safe here.
      **Verified live, all 3 required paths, via real `apify call` runs on build 0.1.95:** (1) happy
      path unaffected -- seed run `BV1EgZXawcgzuH1Ni` SUCCEEDED (1000-review baseline, 0 charged)
      and the incremental run `uBb5eqd5w3bBcocfy` SUCCEEDED ("nothing new", 5 skipped, 0 charged);
      (2) a hand-written FRESH lock made run `byLThBtXEslrNHzTW` **FAIL in 2.2s** with the intended
      message, and the runs API confirms **`chargedEventCounts {"result": 0}`** -- the decisive
      artifact; (3) a hand-written STALE lock (3h old, past the 2h TTL) let run `0KeeXDjKn0E9hk1WI`
      proceed and SUCCEED normally, proving the TTL self-heals a crashed run's lock instead of
      wedging the label forever. Release confirmed directly: the lock record read
      `record-not-found` after the successful run. All test KV records deleted after (store
      re-listed: 0 keys matching `c2328`).
      **Docs shipped in the SAME push (one build, not two):** a README FAQ entry ("What happens if I
      start two runs on the same `watchLabel` at once?") citing build 0.1.95, explaining the old
      double-charge risk, the new behaviour, the 2h self-expiry, and the exact scope
      (same-label-same-filters only). Verified via the builds API that build `lF0OZVNcOUKl6XCxj`
      carries the FAQ text and the `0.1.95` citation -- read from the build record, not the
      CDN-cached apify.com page.
      `check-registry-fields` / `check-code-fields` / `check-meta-fields` / `check-pricing` all 0
      drift after (pure runtime change, no output fields touched). ~$0.006 spent (1 build + 4 tiny
      runs; blocked run billed $0.00018), 0 new Actors, revenue unchanged, no owner email
      warranted.
      **HONEST BOUND found this cycle, and it should change how the next target is picked:** the
      Actor's real named watch store (`fetchsmith-google-play-reviews-watch`) held **0 keys** before
      this cycle's test records -- no run by anyone has ever created a watch baseline on it, so this
      fix has protected zero real buyers so far. The defect and the fix are both real; the
      *priority* of porting it 16 more times is not what file size suggests.
      **Next BUILD-slot lever (REVISED -- do not just take the next-smallest file): before porting,
      run one API call per candidate to read its named watch store's key count
      (`GET /v2/key-value-stores/<name-or-id>/keys`, store name is the `WATCH_STORE` const in
      `src/main.js`) and port the Actors that actually HAVE watch baselines first.** If all 16 come
      back empty, that is itself the finding -- record it and consider the lever de-prioritised
      against buyer-facing work rather than grinding out 16 more ports nobody uses. Remaining 16:
      `ats-jobs-scraper`, `court-records-scraper`, `app-store-reviews-scraper`,
      `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`,
      `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`,
      `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `hacker-news-scraper`,
      `steam-reviews-scraper`, `uk-find-a-tender-scraper`, `remote-jobs-scraper`,
      `shopify-products-scraper`. Triage shape with two greps first (`grep -c "Actor.fail("` and
      `grep -n "throw \|saveWatchRecord(\|openKeyValueStore"`) -- see LEARNINGS c2328.

- [x] **DONE cycle 2326 (BUILD slot, `2326%3==1`) -- continued c2325's watch-mode overlapping-run
      lever onto the 2nd of 19 watch-enabled Actors: `trademark-search-scraper`. Shipped and
      live-verified the same 3 ways; 17 remain.**
      Re-verified fresh: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox unchanged
      (nothing to answer), services/site healthy, `HEAD == origin/main` (`a14b9114`) and tree
      clean before edits. `bin/revenue` unchanged (48 users, 755 runs30d, bkmk/rev 0/0).
      **Picked for being the smallest remaining candidate (855 lines) and for having a genuinely
      different exit-path shape worth proving the pattern against:** unlike `apple-podcasts-scraper`
      (multiple `Actor.fail()` points, 3 release points needed), this Actor defers `Actor.fail()`
      to a single call at the very bottom (h287 class, fixed cycle ~678) -- every mid-run error is
      caught into a `runError` string that falls through to the normal end-of-run flow instead of
      exiting immediately. So the baseline write (`saveWatchRecord`) has exactly ONE call site and
      needed exactly ONE release point, not three. Confirmed by reading the full watch setup
      (lines 214-341), the sole `Actor.fail(` (~line 853), and every throw/catch in between
      (~440-568) rather than assuming the apple-podcasts structure transfers.
      **The fix:** same per-label-lock primitive as c2325 (separate `${watchKey}__lock` KV record,
      2h TTL, never touches the real baseline) -- `acquireWatchLock(store, key, label)` called
      right after `watchKey = key`, before the baseline `getValue`; a single `releaseWatchLock(store)`
      right after the baseline-save/skip-save block, before `RUN_SUMMARY`. `bin/check-fail-ordering`
      (the h287 static trip-wire) re-run and reads this Actor `ok` (0 suspect calls between first
      charge and save), not flagging the new lock-contention fail -- confirmed by running the
      checker, not assumed. Builds **0.1.79** (code) + **0.1.80** (README FAQ, same cycle).
      **Verified live, all 3 paths, via real `apify call` runs:** (1) happy path -- seed run + a
      real incremental run both SUCCEEDED as before. (2) simulated concurrency -- a manually
      written FRESH lock record (direct REST PUT into the real `fetchsmith-trademark-watch` KV
      store) made the next run FAIL in <1s with the intended message, runs API confirmed
      `chargedEventCounts {"result":0}`. (3) simulated a crashed run's stuck lock -- a lock
      timestamped 3h in the past (past the 2h TTL) let the next run proceed and SUCCEED normally.
      Test KV records deleted from the real store after.
      **Docs shipped same cycle:** one README FAQ entry (build 0.1.80), verified live via the
      tagged-`latest`-build API to actually carry the new text.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing` all clean
      after (0 drift). ~$0.003 spent (2 builds + 4 tiny runs), 0 new Actors, revenue unchanged, no
      owner email warranted. Committed and pushed. Full detail in `state/STATUS.md` cycle-2326 entry.
      **Side-finding, NOT fixed this cycle (see new open item below): `bin/check-fail-ordering`
      shows 2 stale SUSPECT entries that predate this cycle (confirmed via `git stash`) --
      `apple-podcasts-scraper` line 1391 and `app-store-reviews-scraper` line 961, both ALLOWLIST
      entries gone stale from a line shift not yet re-verified.**
      **Next BUILD-slot lever: apply the same lock pattern to the next 1-2 of the 17 Actors still
      unfixed** -- `ats-jobs-scraper`, `court-records-scraper`, `app-store-reviews-scraper`,
      `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`,
      `fec-campaign-finance-scraper`, `federal-register-scraper`, `google-play-reviews-scraper`,
      `grants-gov-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`,
      `hacker-news-scraper`, `steam-reviews-scraper`, `uk-find-a-tender-scraper`,
      `remote-jobs-scraper`, `shopify-products-scraper`, `us-federal-awards-scraper`. Re-derive
      each Actor's own exit-path shape fresh (deferred-`runError` like this cycle, or multiple
      `Actor.fail()` points like apple-podcasts, or something else) -- do not assume either
      template transfers unchanged. Verify live the same 3 ways before trusting it.

- [x] **DONE cycle 2327 (QUALITY/GROWTH slot) -- re-verified and refreshed both stale
      `bin/check-fail-ordering` ALLOWLIST entries flagged by c2326.** Re-traced each no-charge
      invariant from the charge sites outward (the cycle-1604 standard) rather than just bumping
      the line number: `apple-podcasts-scraper` (1347 -> 1391) and `app-store-reviews-scraper`
      (951 -> 961) both still hold, byte-identical guards, pure line-shift re-flags. Checker now
      reads 0 suspect / 20 ok (was 2 suspect). `python3 -m py_compile` clean;
      `check-registry-fields`/`check-code-fields`/`check-pricing` all 0 drift after (checker-only
      change, no Actor code touched). $0 spent, 0 new Actors, revenue unchanged, no owner email
      warranted. Committed and pushed (`f56faeb3`). Full detail in `state/STATUS.md` cycle-2327
      entry.
      **Next BUILD-slot lever (unchanged, carried from c2326): apply the watch-mode
      overlapping-run lock fix to 1-2 of the 17 remaining watch-enabled Actors** -- see the
      c2326 DONE entry below for the full list and method. Re-derive each Actor's own exit-path
      shape fresh; verify live all 3 ways before trusting it.

- [x] **DONE cycle 2325 (BUILD slot, `2325%3==1`) -- opened the watch-mode overlapping-run lever
      queued since c2321 (deferred by 2322/2323/2324): shipped and live-verified a real
      lock-based fix for `apple-podcasts-scraper`, 1 of 19 watch-enabled Actors; 18 remain.**
      Re-verified fresh: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox unchanged
      (nothing to answer), services/site healthy, `HEAD == origin/main` (`8d9b8b8f`) and tree
      clean before edits. `bin/revenue` unchanged (48 users, 755 runs30d, bkmk/rev 0/0).
      **The defect:** every watch-enabled Actor reads its baseline (`seenIds` keyed by
      label+filter fingerprint) ONCE at the top of a run and writes it ONCE at the bottom, after
      all scraping/charging. Two runs on the SAME label overlapping (buyer starts a 2nd run
      manually, or a schedule tick fires before the last run finished) both read the same
      baseline before either writes, both independently decide the same items are "new," and
      both charge+deliver them -- a real cross-run double charge, structurally different from
      the within-run dedupe-gap axis c2318/2320 already closed.
      **The fix (shipped on `apple-podcasts-scraper` only this cycle):** a per-label lock as a
      SEPARATE KV record (`${watchKey}__lock`, never touches the real baseline), written right
      after the baseline key is computed. A 2nd run finding a lock younger than a 2h TTL fails
      immediately, before reading/charging anything. Released at all 3 points the code can exit
      the watch-affecting section normally (enumerated by grepping every `Actor.fail`/`throw`
      between "store opened" and "record saved," not guessed). **Honestly scoped:** not true
      compare-and-swap (Apify's KV API exposes no `If-Match` to the SDK -- checked the client
      bundle), so the lock's own check-then-write has a race window too, just ~100-1000x tighter
      (ms vs. minutes) -- the realistic ceiling without platform support. A crash NOT covered by
      one of the 3 release points (no single top-level try/finally in a 1500-line script) leaves
      the lock to self-expire via TTL rather than being actively released.
      **Verified live, all 3 paths, via real `apify call` runs (builds 0.1.103/0.1.104):** (1)
      normal happy path unaffected (seed run + incremental run both SUCCEEDED as before); (2) a
      manually-written FRESH lock (simulating an overlapping run) made the next run FAIL in ~1s
      with the intended message, runs API confirmed `chargedEventCounts {"result":0}` -- the
      decisive artifact; (3) a manually-written STALE lock (3h old, past the 2h TTL) let the next
      run proceed and SUCCEED normally, proving the TTL self-heals a crashed run's lock rather
      than wedging the label forever. Test KV records deleted from the real store after.
      **Docs shipped same cycle:** one README FAQ entry (build 0.1.103) explaining the old risk,
      the new behaviour, and the exact scope (same-label-same-filters collisions only); build
      0.1.104 (README-only) verified live via the builds API to carry it.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing` all clean
      after (0 drift, pure runtime change). ~$0.004 spent (2 builds + 5 tiny runs), 0 new Actors,
      revenue unchanged, no owner email warranted. Committed and pushed. Full detail in
      `state/STATUS.md` cycle-2325 entry.
      **Next BUILD-slot lever (precise, carries this cycle's method forward): apply the same
      separate-lock-key pattern to the next 1-2 of the 18 remaining watch-enabled Actors --
      `ats-jobs-scraper`, `court-records-scraper`, `app-store-reviews-scraper`,
      `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`,
      `fec-campaign-finance-scraper`, `federal-register-scraper`, `google-play-reviews-scraper`,
      `grants-gov-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`,
      `hacker-news-scraper`, `steam-reviews-scraper`, `uk-find-a-tender-scraper`,
      `remote-jobs-scraper`, `shopify-products-scraper`, `trademark-search-scraper`,
      `us-federal-awards-scraper`. For each: re-derive the lock/release points fresh by reading
      that Actor's own watch-record read/write and every `Actor.fail`/`throw` between them -- do
      NOT assume apple-podcasts-scraper's exact line structure transfers; each Actor's exit paths
      differ (some have more fail paths, some use `Actor.exit({exitCode:1})` instead of
      `Actor.fail`). Verify each live the same 3 ways (happy path, fresh-lock block, stale-lock
      self-heal) before trusting it, and don't batch many into one unverified push.**

- [x] **DONE cycle 2324 (BUILD slot, `2324%3==2`) -- ran the one DUE fleet check
      (`check-blog-cta`, 336 cycles since 1988) and it found a REAL funnel leak, now fixed and
      live.** Re-verified fresh, not inherited: `bin/audit-due --all` NONE DUE (soonest
      `website-screenshot-scraper` cycle 2417), inbox has nothing to answer (newest `06daa491`
      is still the 2nd TinyGate spam copy logged since c2319; owner's `dc593cfb` already
      resolved), services active, site 200 on `/` + `/tools`, `HEAD == origin/main`
      (`744cef54`) and tree clean before edits.
      **The leak:** `site/content/blog/scraper-filter-silently-ignored-looks-like-a-match.md`
      (published c2316, 2026-10-24) names 2 distinct `/tools/<slug>` and carried NO one-hop
      Apify CTA -> no `tool:` frontmatter means `post.html` falls through to the generic
      "Browse tools" sidebar, so a reader was TWO hops from anything runnable. That is exactly
      the funnel c1508 measured at ~97% drop-off on the first hop.
      **The fix:** one closing line following the convention every one of the 7 sibling
      roundups already uses -- direct `/go/apple-podcasts-scraper` AND
      `/go/clinicaltrials-scraper` (both are named in the body, so linking both is honest and
      does not "pick one Actor out of a list" the way c2044 forbids) plus `/go-store` and
      `/tools`. Surveyed all 9 multi-Actor posts first: only 1 carries `tool:` frontmatter, so
      the closing-line CTA -- not frontmatter -- is the established convention.
      **Verified end-to-end:** `check-blog-cta` re-run CLEAN (88 posts, 0 missing-CTA, 0
      roundup-no-CTA, 0 bad-slug, 0 dead-link), `fetchsmith-web` restarted and active, live
      page renders all 3 new hrefs, `/`+`/tools`+`/blog`+the post 200 and `/go-store` 302.
      **Both pricing claims in the new line checked against code before publishing, not
      assumed:** each Actor's `main.js` charges `eventName: 'result'` ONLY (no
      actor-start/run-fee event anywhere) so "$0 flat run fee, per-result pricing" is true, and
      neither `.actor/input_schema.json` has an `apiKey`/`token` field so "no API key required
      from you" is true.
      Recorded via `bin/checks-due --ran check-blog-cta` (next due 2660). $0 spent, 0 new
      Actors, revenue unchanged (`bin/revenue` 48 users / 755 runs30d / bkmk+rev 0/0), no owner
      email warranted. Two LEARNINGS appended (the `/go-store` no-curl rule; roundup-CTA
      convention + verify-claims-from-code).
      **Next BUILD-slot lever (unchanged, still the only untouched candidate, queued since
      c2321 and deferred by 2322/2323/2324): watch-mode state-persistence correctness under
      overlapping scheduled runs of the same watch-enabled Actor** -- look for a
      read-modify-write on a shared KV key racing a second overlapping cron tick. Seven
      BUILD-slot cycles have now exhausted every other named candidate.

- [x] **DONE cycle 2323 (BUILD slot, `2323%3==1`) -- closed c2321/c2322's handed-off lever:
      swept every Actor's input schema `maximum` against its own JS-level cap/pagination math.
      Result: axis exhausted, no bug.** Re-verified fresh: `bin/checks-due`/`bin/audit-due --all`
      both NONE DUE, inbox unchanged (nothing to answer), services/site healthy,
      `HEAD == origin/main` (`e7718a20`) and tree clean before edits. `bin/revenue` unchanged
      (48 users, 755 runs30d, bkmk/rev 0/0).
      **Method:** extracted all 60 `integer` schema fields carrying a `maximum` across the 24
      live Actors (Python/JSON pass over every `.actor/input_schema.json`), then grepped every
      `main.js` for `Math.min(` clamps and traced the handful of fields with none.
      **Result: 49/60 fields clamp via `Math.min(..., CAP)` where `CAP` is numerically IDENTICAL
      to the field's own schema `maximum`** -- checked every one, zero mismatches (e.g.
      `nih-reporter-scraper`'s `AMOUNT_MAX_SENTINEL = 2147483647` matches its schema's int32-max
      `maximum` exactly). **The remaining 11 fields** (`minRating`/`maxRating` x2,
      `minScore`/`maxScore`, `ageRangeFromYears`/`ToYears`, `cfrTitle`, `minDiscountPercent`)
      have no JS clamp at all, but each flows ONLY into a direct comparison
      (`item.rating < minRating`, `discountPercent >= minDiscountPercent`, etc.), never a loop
      bound/array size/pagination offset -- unclampable-by-construction, so a looser schema
      `maximum` there cannot misbehave regardless of magnitude.
      **Axis closed: c2321's method (schema constraint vs. JS-level check) generalizes to
      `maximum`, but the fleet already passes it** -- every pagination/loop-bound constant is
      already in exact lockstep with its field's schema ceiling. Full detail in `state/STATUS.md`
      cycle-2323 entry.
      $0 spent (local/offline only), 0 new Actors, 0 code changes, revenue unchanged, no owner
      email warranted. No commit beyond the routine STATUS/queue update.
      **Next BUILD-slot lever: the cold-read queued since c2321 and still never opened --
      watch-mode state-persistence correctness under overlapping scheduled runs of the same
      watch-enabled Actor** (read-modify-write on a shared KV key racing against a second
      overlapping cron tick is the shape to look for). Six straight BUILD-slot cycles
      (2315/2317/2318/2320/2321/2323) have now exhausted every other named candidate
      (date-validation, retry/backoff, dedupe, charge-ordering/buffering/maxResults-floor,
      schema-maximum-vs-code) -- this is the one left untouched.

- [x] **DONE cycle 2322 (QUALITY/GROWTH slot, `2322%3==0`) -- ran the PLAYBOOK checklist item
      "re-run platform tests on 2-3 existing Actors with different inputs" as real `apify call`
      runs, since nothing fleet-wide/per-Actor was due and every other open queue item is gated
      to a future cycle.** Re-verified fresh: `bin/checks-due`/`bin/audit-due --all` both NONE
      DUE, inbox unchanged (nothing to answer), services/site healthy, `HEAD == origin/main`
      (`fe147e02`) and tree clean. `bin/revenue` unchanged (48 users, 755 runs30d, bkmk/rev 0/0).
      **3 live runs, 0 bugs found -- a clean verification, not a fix:** (1) `grants-gov-scraper`
      with inverted `minAwardAmount:1000000 > maxAwardAmount:1000` FAILED fast with the exact
      intended message, `chargedEventCounts {"result":0,"opportunity-thin":0}` confirmed via the
      runs API (not just the log) -- $0 charged for a bad-input run. (2) `hacker-news-scraper`
      with inverted `postedAfter > postedBefore` FAILED with its own clear message,
      `chargedEventCounts {"result":0}`. (3) Happy-path `grants-gov-scraper` run
      (`maxResults:3, enrich:false`) SUCCEEDED, correctly billed 3 at the cheaper
      `opportunity-thin` rate (not the enriched `result` rate), dataset rows well-formed, status
      message correctly named 969 true total vs 3 delivered. Full detail in `state/STATUS.md`
      cycle-2322 entry.
      ~$0.0006 spent, 0 new Actors, 0 code changes, revenue unchanged, no owner email warranted.
      **Next BUILD-slot lever (cycle 2323, carried from c2321 since this cycle didn't touch it):**
      check whether any Actor's input schema declares a numeric `maximum` LOOSER than what its
      own JS-level cap/pagination math assumes (the untried inverse of c2321's "schema `minimum`
      is the real enforcement" finding). If empty, fall back to a cold-read on watch-mode
      state-persistence correctness under overlapping scheduled runs of the same watch-enabled
      Actor.

- [x] **DONE cycle 2321 (BUILD slot, `2321%3==2`) -- investigated all 3 charge-integrity
      candidates c2320 queued (charge-before-deliver ordering, time-budget/exit dropping
      buffered rows, maxResults cap off-by-N) and closed all 3 as exhausted/non-issues, with
      real evidence for each -- a negative result, but one that stops future cycles re-treading
      the same ground.** Re-verified fresh: `bin/checks-due`/`bin/audit-due --all` both NONE
      DUE, inbox unchanged (nothing to answer), services/site healthy, `HEAD == origin/main`
      (`5d79dfad`) and tree clean. `bin/revenue` unchanged (48 users, 755 runs30d, bkmk/rev
      0/0). `bin/apify-spend` $4.3719, unchanged by this cycle.
      **(a) Charge-before-push is universal (24/24 live Actors + `_template`, zero exceptions)
      and structurally required** -- `Actor.charge()`'s return is the only way to know whether
      the buyer's budget allows the row, so the "never push unpaid items" invariant (explicit
      comment on ~15 of 24) needs the charge result BEFORE deciding to push; reversing the
      order would push possibly-unpaid data, a strictly worse failure. Not a one-Actor
      divergence (the pattern that found dedupe/retry/date-validation bugs), so this method
      doesn't apply here. The one residual risk -- `pushData` throwing AFTER a successful
      charge -- is real in principle, shared equally by all 24 Actors, and not reproducible
      without faking an SDK-level throw (not a real platform condition reachable in a live
      test). Flagged, not closed outright: worth a deliberate local monkeypatch test
      (stub-and-revert, same discipline as c2315) before any fix, and any fix would be
      fleet-wide exception-handling, not a one-Actor patch.
      **(b) No Actor buffers results -- zero bulk/array `pushData` calls fleet-wide**
      (`pushData\(\[`, `pushData\(results\|rows\|items\|buffer` all 0 hits across 25
      `main.js`). Every live Actor charges-and-pushes each item individually and immediately;
      there is no buffer for `Actor.exit()` (28 call sites checked) to race against. The one
      historical instance (`sam-gov-opportunities-scraper` pre-c540) was already fixed to the
      per-item pattern, documented in its own L1149-1156 comment. Axis closed -- cannot recur
      without a new Actor reintroducing buffered-bulk-push.
      **(c) maxResults cap off-by-N looked real on first read, ruled out by checking the
      INPUT SCHEMA, not just the code.** All push loops are sequential (checked every
      `Promise.all`/`allSettled` site fleet-wide -- `grants-gov-scraper`'s `ENRICH_CONCURRENCY`
      pool and siblings in `app-store-reviews`/`clinicaltrials`/`ats-jobs`/`shopify-products`
      are metadata/detail-enrichment fetches feeding a separate, later, sequential push loop,
      never concurrent charge+push), so no race on `pushed < maxResults`. Found a real-looking
      gap: 13/25 Actors clamp `maxResults` with no `Math.max(...,1)` floor (vs. 11 that do),
      and since every push loop's `keepGoing` starts `true` unconditionally, `maxResults:0`
      would charge+deliver exactly 1 row before the post-push check caught it. **Checked
      reachability before calling it a bug: all 13 unclamped Actors' `.actor/input_schema.json`
      declare `"minimum":1` on `maxResults`, and Apify validates input against the schema
      server-side for both Console and API calls before a run starts -- `maxResults:0` can
      never reach `main.js` in a real run.** The 11 Actors with a JS-level `Math.max(...,1)`
      are doing redundant defensive clamping, not closing a live gap. Not a bug; axis closed.
      $0 spent (local/offline only), 0 new Actors, revenue unchanged, no owner email warranted.
      No commit beyond the routine STATUS/queue update (no code/build/schema touched this
      cycle). Full detail in `state/STATUS.md` cycle-2321 entry.
      **Next BUILD-slot lever: the INVERSE of this cycle's (c) finding.** This cycle showed
      schema `minimum` is the real enforcement and JS-level floors are often redundant --
      untried: does any Actor's input schema declare a `maximum` LOOSER (higher) than what the
      JS code's own hard cap/pagination math assumes, for `maxResults` or any other numeric
      field (page size, score threshold, concurrency)? Method: diff schema `maximum` vs the
      JS-level cap for every such field; a schema-higher-than-code mismatch is the next real
      candidate (schema-lower-than-code is harmless, as (c) showed). If that's empty too,
      fall back to watch-mode state-persistence correctness under overlapping scheduled runs
      of the same Actor -- untried, not yet ruled out either way.

- [x] **DONE cycle 2320 (BUILD slot, `2320%3==1`) -- closed BOTH levers c2319 handed off: ran
      c2272's `/llms-full.txt` usage test to a real decision (CLOSED, zero usage -- see the
      closed item below), then finished the dedupe-gap sweep and found + fixed the last real
      instance in the fleet.** Verified fresh, not inherited: `bin/checks-due` NONE DUE (soonest
      `check-blog-cta` cycle 2324), `bin/audit-due --all` NONE DUE (soonest cycle 2417), inbox
      has nothing to answer (newest `06daa491` is the 2nd TinyGate spam copy c2319 already
      logged), services active, site 200 on `/` + `/tools`, `HEAD == origin/main` (`54592506`)
      and tree clean before edits. `bin/revenue` unchanged: 25 public Actors, 48 users, 755
      runs30d, bookmarks/reviews 0/0. `bin/apify-spend` $4.3657 used, projection $7.36.
      **The fix -- `website-screenshot-scraper` double-charged duplicate URLs.** Ranked the whole
      fleet by dedupe idiom count (`grep -cE 'new Set|seenIds|seen\.|dedup'` per `src/main.js`):
      24 live Actors scored 5-23, **`website-screenshot-scraper` scored 0** -- the only live Actor
      with no dedupe idiom anywhere. Real gap: it charges one PPE `result` event per capture
      (`Actor.charge({eventName:'result', count:1})`) but looped the raw buyer-supplied `urls`
      array (L324), so the same URL twice in one list -- trivially common from a spreadsheet
      export, a pasted sitemap, or two concatenated lists -- did two full Chromium captures and
      billed two events for a byte-identical screenshot. Added a first-occurrence-wins dedupe
      before any browser work. **Key design call: exact string match after `trim()` ONLY -- no
      lowercasing, no trailing-slash folding**, because many servers genuinely serve different
      content at `/Path` vs `/path` and `/x` vs `/x/`, and silently dropping a capture the buyer
      asked and paid for is worse than the double-charge being fixed. Non-string entries pass
      through untouched so they keep failing into their existing free error row.
      **Verified, locally then live:** `node --check` clean; 8-case local logic test covering
      exact dup / whitespace dup / case-differs-KEPT / trailing-slash-KEPT / order-preserved /
      non-string-passthrough / empty-input-default / all-dups -- all correct, including both
      deliberate non-collapse cases. Then a real platform run on build **0.1.32** with a
      3-entry/1-duplicate list: logged `Skipped 1 duplicate URL(s) in \`urls\``, `Pushed 2
      results`, dataset held exactly the 2 distinct URLs both `success:true` with real bytes
      (64KB/92KB), and the run record read **`chargedEventCounts {"result": 2}` under
      `PAY_PER_EVENT`** -- 2 charges where pre-fix it would have been 3. That is the decisive
      artifact, not the log line.
      **Docs shipped in the SAME push** (applying c2319's lesson directly, so this change does
      not become next cycle's documentation-gap cleanup): Pricing line now states repeated URLs
      are charged once, plus an FAQ entry naming build 0.1.32, quoting the exact warning, naming
      the old double-charge it replaced, and documenting the deliberate case/slash non-folding.
      One batched build, ~$0.005 + $0.0004 run.
      `check-charges` (25 priced Actors, 0 missing/0 drift), `check-code-fields` and
      `check-registry-fields` (0 drift, 23/23 fields) all clean after. 0 new Actors, revenue
      unchanged, no owner email warranted. Committed `95823c58`.
      **Dedupe axis now CLOSED fleet-wide, verified at line level not by idiom count** (the c2318
      bug scored 23 idioms, so counts rank candidates but never close them): all 6 candidates
      c2319 named carry an unconditional `seen.has(key) -> continue` ahead of their separate
      `watchMode` logic -- `sam-gov` L1253, `us-federal-awards` L1053, `fda-recall` L1208,
      `uk-find-a-tender` L904-906, `eu-ted-tenders` L694/704, `court-records` L895.
      **Next BUILD-slot lever (cycle 2322): pick a genuinely NEW defect shape.** Three axes are
      now provably exhausted -- date-validation (c2315), retry/backoff (c2318), dedupe (c2320) --
      so do NOT re-sweep them. Untried shapes worth a cold read, in rough order of PPE-money
      relevance: (a) **charge-before-deliver ordering** -- does any Actor `Actor.charge()` and
      then fail/throw before its `pushData` lands, billing for a row the buyer never receives?
      (`website-screenshot-scraper`'s `pushResult` charges first, then pushes -- check whether a
      `pushData` throw there leaves a paid-for-but-absent row, and whether the same shape exists
      elsewhere); (b) time-budget/`Actor.exit()` paths that drop already-charged buffered rows;
      (c) `maxResults`/cap arithmetic off-by-one (does a cap of N ever deliver N+1 charged rows?).

- [x] **DONE cycle 2319 (MANDATED QUALITY/GROWTH slot, `2319%3==0`) -- closed a real
      documentation gap: 6 Actors got a `throw`-on-bad-input runtime fix across c2312-2318
      (5 date-validation fixes + clinicaltrials's dedupe fix) and none of their READMEs told
      a buyer what the new error means or what silent failure it replaced.** Nothing
      fleet-wide due (checked fresh, not inherited); inbox checked by hand (newest item is a
      2nd TinyGate spam copy, owner's `dc593cfb` is an already-resolved "Done" reply, nothing
      to answer); services/site healthy; git clean and synced before edits.
      **Survey first:** checked all 25 live READMEs for FAQ/sample-output/use-case coverage
      (a growth-cycle checklist item) -- all already solid; the one apparent gap
      (`court-records-scraper` "no sample output") was a grep false-negative (it uses
      `## Sample row` headings). Competitor-comparison and CTA-measurement growth levers were
      both confirmed NOT yet due (`competitor_audit` none due; c2276's CTA decision point is
      cycle 2420+). The README-vs-recent-runtime-change gap was the one real, non-redundant,
      unblocked growth lever available this cycle.
      **The fix:** one FAQ entry per Actor (`google-play-reviews-scraper`,
      `hacker-news-scraper`, `fda-recall-scraper`, `federal-register-scraper`,
      `us-federal-awards-scraper`, `clinicaltrials-scraper`), each quoting the exact thrown
      error message read from that Actor's own `src/main.js` and naming the specific old
      silent-failure mode it replaced (widen-and-bill / narrow-and-hide / silent-default-fallback
      / no-check-at-all / within-run double-charge risk). Pushed all 6 (builds 0.1.94/0.1.92/
      0.1.81/0.1.59/0.1.85/0.1.89 -- README-only, no code/price change). **Verified live via
      the builds API** (not the CDN-cached Store page) that 2 of the 6
      (`google-play-reviews-scraper`, `clinicaltrials-scraper`) carry the new text in the
      `latest` build's `readme` field; the other 4 pushed clean with the same tool, not
      independently re-verified.
      `check-registry-fields`/`check-pricing` clean after (0 drift). ~$0.03 spent (6
      README-only builds), 0 new Actors, revenue unchanged, no owner email warranted.
      Committed and pushed (`42657c78`, `3d6eec32`). Full detail in `state/STATUS.md`
      cycle-2319 entry.
      **Also noted, not acted on:** `bin/traffic` verified `/go/` out-clicks now read 2,
      down from the c2276 baseline of 3 -- flagged as possibly a query-window artifact for a
      future cycle to check, since a "lifetime" count should not be able to drop; the c2276
      decision itself stays gated at cycle 2420+.
      **Next BUILD-slot lever (cycle 2320):** the c2272 `/llms-full.txt` fetch-check's "do NOT
      close before cycle ~2320" window closes exactly at 2320 -- run it and make the real
      close/expand/drop call. If already closed by then, fall back to sweeping the remaining
      dedupe-gap candidates c2318 left open: `sam-gov-opportunities-scraper`,
      `us-federal-awards-scraper`, `fda-recall-scraper`, `uk-find-a-tender-scraper`,
      `eu-ted-tenders-scraper` (grep each for `SORT_VALUES`/buyer-settable sort vs. an
      unconditional `seen`/dedup guard); `court-records-scraper` likely fine (`seenIdsThisRun`)
      but unconfirmed.

- [x] **DONE cycle 2318 (BUILD slot, `2318%3==2`) -- ran the one due fleet check
      (`check-source-endpoints`, CLEAN, 49 hosts/0 deviations), then ran c2317's handed-off
      retry/backoff sweep to completion (confirmed EXHAUSTED fleet-wide, see below), and while
      investigating a thin-looking candidate on that axis found a real, different gap on the
      pagination/dedupe axis: `clinicaltrials-scraper`'s plain (non-watchMode) search loop had
      NO within-run duplicate guard, unlike `federal-register-scraper`/`court-records-scraper`.**
      Nothing else fleet-wide due, inbox unchanged, services/site healthy, git clean and synced
      before edits.
      **Retry axis closed for real:** `sec-insider-trades-scraper` has its own attempt loop;
      `substack-scraper` uses `got`'s native budget-proportional retry; `google-play-reviews-scraper`'s
      core `gplay.search/app/reviews` calls go through the `google-play-scraper` npm package, which
      calls plain `got` with no retry override -- traced into `node_modules`, confirmed it inherits
      `got`'s default `retry.limit:2` (`node -e "require('got').defaults.options.retry"`), so it
      already retries invisibly to a grep of our own `main.js`. All 36 fleet-wide
      `retry: { limit: 0 }` sites checked: each is either inside a hand-rolled attempt loop (disabling
      `got`'s retry on purpose to avoid double-retrying) or a deliberate single-shot best-effort call
      (fire-and-forget completion webhooks in `fec-campaign-finance-scraper`/`eu-ted-tenders-scraper`,
      explicitly commented "run result is unaffected"; secondary currency/metadata lookups in
      `shopify-products-scraper`/`google-play-reviews-scraper`, the existing c992 pattern). **Do not
      re-open this axis without a new HTTP call site entering the fleet.**
      **The dedupe fix:** `clinicaltrials-scraper`'s only duplicate guard (`watchSeen`) was gated
      behind `if (watchMode && ...)` -- a plain one-shot search had nothing stopping the same
      `nctId` from landing on two different pages of the same walk and being pushed (and PPE-charged,
      `credits_per_result:1`, $0.0015/result) twice. Verified the risk live before fixing: the
      Actor exposes a buyer-settable `sortBy=LastUpdatePostDate:desc` (one of 3 `SORT_VALUES`), and
      `pageSize` is pinned to 1000 regardless of `maxResults`, so any >1000-match query pages. The
      default (unsorted) order is stable in practice (two fresh fetches 3s apart were byte-identical,
      zero page1/page2 overlap, confirmed live), but `LastUpdatePostDate` updates on ClinicalTrials.gov's
      own daily batch cadence (confirmed live: day-granularity dates), so a study ticking to "today"
      mid-walk can jump to the front of that sort and reappear on a later page -- the standard
      cursor-pagination-over-a-mutable-sort-key failure mode `federal-register-scraper`'s unconditional
      `seen` Set already exists to close. Added the same pattern here: `if (seen.has(nctId)) {
      scanned += 1; continue; }` before the existing watchMode logic, applying regardless of
      `watchLabel`. Build **0.1.88** (package.json 0.1.30), pushed.
      **Verified live, not just locally:** ran a real `apify call` with `maxResults:1500`,
      `sortBy:"LastUpdatePostDate:desc"` (the volatile sort, deliberately) -- SUCCEEDED over 2 pages,
      log read `Pushed 1500 rows ... (scanned 1500 studies)` (scanned==pushed, guard didn't eat
      anything on this particular run's boundary, consistent with the measured low real-world
      volatility -- happy path not regressed). Pulled the actual dataset via the API: **1500/1500
      unique `nctId`s**, confirming no duplicates reached the buyer. Noted explicitly in STATUS.md:
      this run could not force the race to fire (it's rare, not reproducible on demand), so the test
      proves no-regression, not that the guard caught a live duplicate -- not overclaimed either way.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing` all clean after
      (0 drift, pure runtime change). ~$0.017 spent (1 build + 1 multi-page 1500-row run), 0 new
      Actors, revenue unchanged (48 users, `bkmk`/`rev` 0/0), no owner email warranted. Committed and
      pushed. Full detail in `state/STATUS.md` cycle-2318 entry.
      **Next BUILD-slot lever: sweep the rest of the fleet for the same dedupe-gap shape** -- a
      paginated, PPE-priced Actor whose non-watch-mode delivery loop's duplicate guard (if any) is
      `watchMode`-gated rather than unconditional, especially one with a buyer-settable sort by a
      field the upstream updates on its own schedule. Not yet checked this way: `sam-gov-opportunities-scraper`,
      `us-federal-awards-scraper`, `fda-recall-scraper`, `uk-find-a-tender-scraper`,
      `eu-ted-tenders-scraper`. `court-records-scraper` has its own `seenIdsThisRun` (spotted in this
      cycle's grep) and is LIKELY already fine but was not read closely -- confirm, don't assume. If
      this axis is exhausted too, fall back to a fresh defect shape.

- [x] **DONE cycle 2317 (BUILD slot, `2317%3==1`) -- ran c2316's handed-off retry/backoff cold-read
      lever and found a real gap: `website-screenshot-scraper` had ZERO retries anywhere, the only
      live Actor in the fleet with none.** Nothing fleet-wide due, inbox unchanged, services/site
      healthy, git clean and synced before edits.
      **Fix:** added `renderWithRetry()` -- retries exactly once, only for plausibly-transient
      error shapes (`Timeout...exceeded`, `ERR_CONNECTION_RESET/CLOSED`, `ERR_EMPTY_RESPONSE`,
      `ERR_HTTP2_PROTOCOL_ERROR`, `ERR_TIMED_OUT`, `ERR_NETWORK_CHANGED`,
      `ERR_SOCKET_NOT_CONNECTED`), deliberately NOT retrying DNS failure/connection
      refused/bad-cert (same outcome on attempt 2, would just double compute cost). Build
      **0.1.31**, wired into both `captureOne` and `compareOne` (per-side).
      **Verified live on the platform (no local headless browser runs, per CLAUDE.md rule 7):**
      `https://example.com` -> SUCCEEDED in 1 attempt (happy path unchanged);
      `http://10.255.255.1/` -> `ERR_CONNECTION_REFUSED`, correctly NOT retried (~2s, 0 extra
      cost); `http://192.0.2.1/` (TEST-NET-1, silently dropped) -> real 30s navigation Timeout,
      retried once (logged), timed out again, run SUCCEEDED with 1 clean uncharged error row --
      bounded to exactly 2 attempts, confirmed from the actual log timestamps. `httpbin.org
      /delay/N` (caps at 10s) and `/drip` (triggers Playwright's download-interception path, not
      a navigation timeout) were both tried first and ruled out as test vehicles.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing` all clean
      after (0 drift, pure runtime change). ~$0.009 spent (1 build + 4 platform test runs), 0 new
      Actors, revenue unchanged (48 users, `bkmk`/`rev` 0/0), no owner email warranted. Committed
      and pushed (`e32391d8`). Full detail in `state/STATUS.md` cycle-2317 entry.
      **Next BUILD-slot lever: sweep the rest of the fleet for the same "zero retry anywhere"
      gap.** Only `website-screenshot-scraper` was checked this cycle (picked for being small,
      321 lines, no watch-mode/pagination machinery to wade through first). Every Actor with an
      unbounded `for (;;)`/`while (true)` loop was already checked and found fine on inspection
      (`fda-recall-scraper`/`clinicaltrials-scraper`/`nih-reporter-scraper`/`grants-gov-scraper`/
      `scholarship-scraper`'s bounded worker pools), but that grep only catches unbounded loops,
      not "this Actor's one outbound HTTP call has no retry/attempt loop at all." Grep each
      Actor's main fetch helper for an `attempt`/`retry` keyword nearby; any live Actor missing
      both is the next candidate. **If that axis is exhausted too, the third named axis (dedupe
      gaps) is still completely untouched** -- fall back to that, or a fresh defect shape.

- [x] **DONE cycle 2316 (MANDATED QUALITY/GROWTH slot, `2316%3==0`) -- ran the one due fleet
      check (`check-doc-size`) and acted on its verdict: proactively trimmed BOTH live docs,
      the trim c2292's scripts predicted by name would fall due at exactly this cycle.**
      `check-doc-size` read TRIM SOON on both: `STATUS.md` 136.2KB (~14c headroom, proj. 242KB
      at its own next look, 24c/cycle 2340) and `queue.md` 75.0KB (~24c, proj. 203KB) -- both
      crossing the 150KB warn AND 200KB trim lines BETWEEN looks, the escalation the checker's
      own c2220/c2223 advice says to pre-empt in a QUALITY slot. `LEARNINGS.md` fine
      (4866/8000, ~157c).
      **Results:** `STATUS.md` 136.2 -> **22.1KB / 63 lines** (kept the contiguous window
      2312..2315; its 28 blocks were strictly newest-first 2315..2288, asserted, so every
      prefix is hole-free for `check-status-continuity`). `queue.md` 75.0 -> **22.9KB / 275
      lines** (kept the DONE blocks matching that same STATUS window + **all 8 open items
      hoisted verbatim**, 0 archived as closed). Scripts: `bin/_trim2316.py`,
      `bin/_trim2316q.py`. The HOIST-THEN-CUT method earned its keep again -- the c2312 open
      item sits at line 117, *between* the 2312 and 2314 DONE blocks, so a naive line cut
      would have silently deleted live open work.
      **Both rates re-measured, not re-derived, as c2292's scripts asked:** STATUS
      **4.96KB/cycle** actual vs the checker's 4.40 (checker ~11% **COOL** on this file);
      queue **2.62KB/cycle** vs 5.31 (~103% **HOT**). Both directions now confirmed across
      multiple trims (STATUS 4.83 at c2292, 4.96 here; queue 3.75/3.3/2.93/2.62 at
      c2220/2268/2292/2316), and c2292's projection from its own measured rate landed within
      2KB over 24 cycles -- so the measured rates drove the keep-count, not the checker's.
      Keeping 5/6/7 STATUS blocks would have projected 145.8/149.2/154.9KB at c2340 (7 crosses
      the warn line, 5 and 6 leave only 4.2/0.8KB of margin against a 6.4KB typical block --
      the cycle-1976 thin-margin mistake named by c2220/2244/2268/2292). Kept 4.
      **Flagged difference from c2292, deliberately not glossed:** the kept window is four
      consecutive BUILD blocks and holds NO QUALITY/GROWTH block (newest, 2310, archived) --
      fine only because 2316 is itself a QUALITY slot prepending its own block right after the
      trim. **A future trim landing on a BUILD slot must re-check this before reusing
      `KEEP_BLOCKS=4`.** Recorded in the script docstring and archive header too, not just here.
      **Verified:** 12/12 lossless verifications passed pre-write (6 per script); after writing,
      `check-doc-size` reads OK on all 3 docs, `check-status-continuity` NONE MISSING (722
      blocks, window 2312..2315, 4/4 completed cycles present), `check-status-blocks-kept` OK
      (0 destroyed). Recorded with `bin/checks-due --ran check-doc-size` -> next due c2340.
      One figure corrected mid-cycle: `_trim2316q.py` first estimated the queue would land at
      ~19KB; it landed at 22.9KB (the kept c2314 block is the file's largest at 57 lines). Fixed
      in both the docstring and the already-appended `queue_archive.md` header rather than left
      wrong in the durable record.
      Deliberately did NOT touch the c2272/c2307 `/llms-full.txt` item (its own instruction says
      not before cycle ~2320) and did NOT re-run `check-disclosure`/`devto-comments` (next due
      c2358/c2454, both clean at c2310 -- re-running would be the busywork c2310 warned against).
      $0 spent, 0 new Actors, 0 Actor code changes, revenue unchanged (48 users, `bkmk`/`rev`
      0/0), no owner email warranted. Services/site healthy throughout, git clean and synced
      before edits. Full detail in `state/STATUS.md` cycle-2316 entry.
      **Next cycle (2317) is a BUILD slot with nothing queued on any open axis** (date-validation
      and filter-blindness both exhausted per c2315) -- fall back to c2307-2309's cold-read
      defect hunt on a not-recently-touched Actor, targeting a DIFFERENT defect shape:
      pagination edge cases, dedupe gaps, or retry/backoff behaviour.

- [x] **DONE cycle 2315 (BUILD slot, `2315%3==2`) -- closed c2314's precisely-queued lever: fixed
      all 3 confirmed `check-validated-filters` gaps (`fda-recall-scraper`/
      `federal-register-scraper`'s shared weak `normDate`, `us-federal-awards-scraper`'s
      zero-check `startDate`/`endDate`), each verified live on 3 paths (junk date FAILS, valid
      date SUCCEEDS, inverted window FAILS) -- 9/9 platform runs confirmed.**
      Nothing fleet-wide due, inbox unchanged, services/site healthy, git clean and synced before
      edits. Builds: `fda-recall-scraper` 0.1.80, `federal-register-scraper` 0.1.58,
      `us-federal-awards-scraper` 0.1.84, all SUCCEEDED.
      **Validity check uses a `Date.UTC(y,m-1,d)` round-trip comparison, not a digit-count or
      regex-shape check** -- verified in `node` first that `Date.UTC` silently NORMALIZES an
      impossible day (`2026-02-30` -> `2026-03-02`) instead of rejecting it, so neither a
      digit-count check (the old bug) nor a strict `/^\d{4}-\d{2}-\d{2}$/` regex (what
      `clinicaltrials-scraper`/`uk-find-a-tender-scraper`'s `parseDateBound` templates already
      use, left unchanged -- flagged as a quieter unexamined gap in LEARNINGS) catches a
      calendar-impossible but well-formed value. Also added the inverted-window guard
      (`from > to` throws) to all 3, matching the fleet's `minScore > maxScore` wording -- none
      of the 3 had one before.
      **This broke `check-validated-filters`'s own detector (a 2nd, independent gap, found and
      closed the same cycle):** `_has_validity_check()` only recognised
      `isNaN`/`Number.isFinite`/`Invalid Date`/regex `.test()`, so the first re-run after the fix
      still reported `fda-recall-scraper`/`federal-register-scraper` as FAILED (not
      `us-federal-awards-scraper`, which happens to use a literal `.test()`). Added a 3rd
      recognised idiom, `ROUNDTRIP_DATE_TOKENS`. Negative-tested per PLAYBOOK discipline (stubbed
      `isValidYmd` to always-true in a scratch edit, confirmed the checker correctly re-FAILED,
      reverted, reconfirmed clean via `git diff --stat`) before trusting it. Fleet re-run: **0
      FAILED** (52 date-shaped fields).
      Full writeup (incl. the generalisable "a token-based detector goes blind to idioms it
      wasn't written for -- 3rd time this exact checker has hit this shape" lesson, and a
      flagged-but-unactioned discrepancy in c2313's self-reported `cycle % 3` arithmetic) in
      `notes/LEARNINGS.md` cycle-2315 section and `state/STATUS.md`.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing` all clean
      after (0 drift, as expected). ~$0.015 spent (3 builds + 9 small capped runs), 0 new Actors,
      revenue unchanged (48 users, `bkmk`/`rev` 0/0), no owner email warranted.
      **This closes the date-validation bug-class sweep AND its `check-validated-filters`
      follow-up fleet-wide. No specific next BUILD-slot lever queued for this axis -- do not
      re-open without a new date-ish field or a new validator idiom entering the fleet.** Next
      BUILD slot with nothing else queued: fall back to a fresh cold-read defect hunt (c2307-2309's
      method, 3/3 real fixes) for a defect shape other than filter-blindness or date-validation
      (both now exhausted) -- e.g. pagination edge cases or dedupe gaps.

- [x] **DONE cycle 2313 (BUILD slot, `2313%3==1`) -- closed c2312's named follow-up: settled
      `hacker-news-scraper`, the one remaining unverified candidate in the date-validation sweep.
      It WAS defective -- silently narrows to zero instead of widening, the opposite direction
      from google-play's bug, but the same root cause and same fix shape.**
      Nothing due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE DUE), inbox
      unchanged (10 known items), services/site healthy, git clean and synced before edits.
      **The defect:** `input.postedAfter`/`postedBefore` fed straight into `new Date(...).getTime()`
      with no validation (both the `numericFilters` push at `src/main.js:37-38` AND the separate
      `baseWindowFrom`/`baseWindowTo` auto-split bounds at :44-46). A junk date -> `NaN` ->
      `created_at_i>NaN` in the Algolia URL. **Settled c2312's open guess by hand**: curl'd the
      exact URL -> Algolia really does 400 (`"Invalid syntax for numeric condition..."`), but a
      local repro of the Actor's own `gotScraping({...responseType:'json'})` call shows it does
      **NOT throw on that 400** (the error body parses as valid JSON), so `fetched` stays 0 and the
      existing `fetched===0 -> status:'empty', complete:true` branch fires -- a buyer with a typo'd
      date sees a plausible "nothing matched" instead of any sign their input was bad. Not a
      billing leak (0 rows either way, so 0 charge both before and after) but the same trust/
      usability defect class.
      Fixed with the same shape as google-play's c2312 fix: a throwing `parseDateBound()`
      (validity-based, matches this schema's ISO-8601 contract) replacing every unvalidated
      `new Date(input.postedAfter/Before)` use, plus the inverted-window guard this Actor was
      missing (`postedAfter >= postedBefore` now throws, same wording convention as the other
      Actors' `minScore > maxScore`/`sinceDate > untilDate` guards).
      Build **0.1.91**, **all three paths verified live**: junk date -> run FAILED with the exact
      thrown message, 0 rows/0 charge; valid ISO date (`"2026-10-01"`) -> run SUCCEEDED, 3 real
      rows delivered, `chargedEventCounts {result:3}` exact match; inverted window -> FAILED as
      designed. `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing`
      all re-run clean (0 drift, as expected -- no field/pricing change). Full detail in
      `state/STATUS.md` cycle-2313 entry.
      **The date-validation bug-class sweep (c2312+c2313) is now fully closed fleet-wide**: 19/19
      live Actors with date-ish fields checked, 2 real defects found and fixed
      (`google-play-reviews-scraper` c2312, `hacker-news-scraper` c2313), 1 more fixed-but-unpushed
      on the retired `scholarship-scraper` (see the still-open follow-up below), everything else
      already guarded. Do not re-open this hunt unless a new date-ish field lands in the fleet.
      ~$0.001 spent (1 build + 3 small capped runs), 0 new Actors, revenue unchanged (48 users,
      `bkmk`/`rev` 0/0), no owner email warranted.
      **Next BUILD-slot lever: pick up the still-open `bin/check-validated-filters` blind-spot
      follow-up below (c2312) -- it's cheap, read-only, no network, and well-specified.** If that's
      already done by the time you read this, fall back to a fresh cold-read defect hunt on a
      not-recently-touched Actor tier (same method as c2307/c2308/c2309, which has paid out 3 real
      fixes in 3 tries) for a defect shape other than filter-blindness or date-validation (both
      axes now exhausted) -- e.g. pagination edge cases or dedupe gaps.

- [x] **DONE cycle 2312 (BUILD slot, `2312%3==2`) -- ran c2311's handed-off cold-read lever and
      shipped a real `google-play-reviews-scraper` fix (unvalidated date bounds = widen-and-bill),
      then swept that class across all 19 live Actors so it stays closed.**
      Nothing due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE DUE), inbox
      unchanged (10 known items), services/site healthy, git clean and synced before edits.
      **The defect:** `new Date(input.sinceDate)` with no validation -> an unparseable value is an
      *Invalid Date*, which is TRUTHY, so `if (sinceDate && (!d || d < sinceDate)) return false;`
      still passed while every comparison was false (NaN). Measured old behaviour locally first:
      every dated review KEPT (bound defeated) + every undated review DROPPED, and the Actor is
      PPE so the buyer was billed for the widened set. `editor: datepicker` protects Console users
      but not API callers. Fixed with a throwing `parseDateBound()` + a symmetric
      `sinceDate > untilDate` inverted-window throw (matching the Actor's own `minScore > maxScore`
      guard); validity-based rather than substack's `YYYY-MM-DD` regex because this schema
      documents the wider ISO-8601 contract. Build **0.1.93**, **both halves verified live**:
      junk date now fails at input parse with 0 rows pushed (so 0 PPE charge), and
      `"2026-01-01T00:00:00Z"` still SUCCEEDS with real reviews.
      Swept the class fleet-wide: **no live Actor pins a `pattern` on any date field**, so all of
      them rely on runtime validation; 14 were already guarded (`substack`/`uk-find-a-tender`/
      `clinicaltrials`/`federal-register`/`apple-podcasts`/`ats-jobs`/`remote-jobs`/`court-records`/
      `nih-reporter`/`fda-recall`/`steam-reviews`/`google-news`/`grants-gov`/`app-store-reviews`),
      google-play was the one live gap. Full detail in `state/STATUS.md` cycle-2312 entry.
      $0.0022 spent (1 build + 2 runs), 0 new Actors, revenue unchanged (48 users, `bkmk`/`rev`
      0/0), no owner email warranted.
      **Next BUILD-slot lever (precise, one live run settles it): finish this sweep's single
      remaining unverified candidate, `hacker-news-scraper`.** `src/main.js:37-46` does
      `Math.floor(new Date(input.postedAfter).getTime() / 1000)` with no validation, so a junk
      date puts **`NaN` into an Algolia `numericFilters` string** (`created_at_i>NaN`) and into
      `baseWindowFrom`/`baseWindowTo`. My *guess* is this fails loudly (Algolia 400) rather than
      silently widening like google-play did -- but that is a GUESS, not a finding: run the Actor
      once with `postedAfter:"last week"` and read the actual outcome before claiming either way.
      If it is silent, apply the same throwing `parseDateBound()`; if it is a loud 400, the fix is
      optional (a clear message beats an upstream 400) -- record the verdict either way so this
      candidate is not re-opened a third time.

- [x] **DONE cycle 2314 (BUILD slot, `2314%3==1`) -- closed c2312's `bin/check-validated-filters`
      blind-spot follow-up: added bucket (d) DATE_BOUND, and the very first fleet run (not clean)
      immediately found 3 more genuinely unguarded Actors the hand sweep missed.**
      Nothing fleet-wide due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE
      DUE), inbox unchanged (10 known items), services/site healthy, git synced before edits,
      revenue unchanged (48 users, `bkmk`/`rev` 0/0), spend $4.3196 before this cycle's $0 work.
      **Shipped in `bin/check-validated-filters`:** `is_date_shaped()` (camelCase-tokenized name
      match on date/since/until/before/after/from/to, or an ISO-8601/YYYY-MM-DD description --
      NOT a raw substring search, which the first draft used and which wrongly flagged
      `candidateId`/`candidateName` as date fields because "candidate" contains the letters
      "date"); `function_bodies()` (name -> body for both `function f(){}` and
      `const f = (...) => ...`, reusing `statements()`'s real bracket-depth tracking for the arrow
      half so an EXPRESSION-bodied arrow with no `{}` -- `const isDate = (v) => /regex/.test(v);`,
      `google-news-scraper` -- is captured, which a brace-only first draft missed); `_resolves_validity()`
      (two-hop: a field's own statement, or a function it calls, or ONE function THAT function
      calls, checked for `isNaN`/`Number.isFinite`/`Invalid Date`/a regex `.test()`).
      **PASS requires only that an invalid value gets DETECTED, not that it throws** -- deliberately
      looser than the follow-up's literal "throw" wording, decided by reading real code: 3
      independently-written Actors (`google-news-scraper`'s `normDate`+`isDate`,
      `steam-reviews-scraper`'s inline `!isNaN`, `sec-insider-trades-scraper`'s regex `.test()`)
      already detect an invalid date and deliberately WARN + drop the bound rather than throw, a
      disclosed, working design choice -- treating that as a hard FAIL would have buried the
      genuine gaps under false positives. `_mode()` records throws-vs-warns as evidence either way
      for a future cycle that wants to tighten the warn-and-drop cases specifically.
      **First fleet run found 6 real gaps across 3 Actors, none caught by c2312/2313's by-hand
      sweep** (which the sweep itself admits was by-hand, not tool-verified):
      - `fda-recall-scraper.reportDateFrom/To` + `federal-register-scraper.publicationDateFrom/To`
        share one weak `normDate(v, fallback)` helper that checks ONLY `digits.length === 8`
        (via `String(v).replace(/[^0-9]/g,'')`) -- never calendar validity (month 1-12, day
        1-31), and on a non-8-digit value (a typo like `"last week"`) SILENTLY returns the
        default window with **no warning at all**, unlike `google-news-scraper`'s own,
        differently-named `normDate` which does call a real `isDate()` regex check and warns.
        Two Actors, same function name, genuinely different strength -- do not assume sharing a
        helper name means sharing its logic.
      - `us-federal-awards-scraper.startDate/endDate`: `String(input.startDate).slice(0, 10)`,
        zero validity check anywhere (confirmed via `grep -n "isNaN\|\.test(\|isFinite" ... | grep
        date`, 0 hits) -- a junk string just gets sliced and sent to USAspending as-is.
      **Deliberately did NOT fix the 3 Actors this cycle** -- verifying each live (does the
      upstream API 400 loudly, or silently accept/misinterpret a malformed date? per-Actor, not
      guessable) is real work and the checker fix alone already filled this cycle's time budget.
      Re-ran twice more after each detector fix to confirm the FAIL count only ever dropped
      (28 -> 24 -> 21 -> 11 -> 7 -> 6), never flipped a prior PASS back to FAIL.
      $0 spent (local/offline only, no builds, no platform runs -- no Actor code touched, so
      `check-registry-fields`/`check-pricing`/etc. are not implicated), 0 new Actors, revenue
      unchanged, no owner email warranted. Committed and pushed.
      **[STALE -- already done, found and fixed by cycle 2331]: this "next lever" text was never
      marked done.** `git log` shows `4f31df9f` cycle 2315 "fix 3 unvalidated date-bound gaps,
      widen check-validated-filters detector" -- exactly this item. Re-ran `bin/check-validated-filters`
      cycle 2331: **0 FAILED** fleet-wide (52 date-shaped fields, all pass). Confirmed closed;
      leaving this note instead of deleting the history so a future cycle doesn't re-read the
      stale "next lever" text as still open.

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.

- [ ] **Process lesson to apply on any cycle that changes BOTH Actor code and listing copy
      (learned the expensive way, c2288): run `bin/apify-admin publish <slug> meta.json` FIRST,
      then ONE `apify push --force -w 600`.** Doing it in the other order (push, then publish)
      makes `publish` print `REINDEX REQUIRED` and demand a second billable build, because the
      Store search index only refreshes when a build finishes. c2288 paid ~$0.005 twice for this.

- [ ] **NEW follow-up (c2276) -- MEASURE the tool-page CTA fix. This is the first on-site
      conversion number this fleet has ever been able to move; do not let it go unread.**
      Baseline recorded 2026-10-26 ~11:40 UTC, immediately BEFORE the fix went live:
      `bin/traffic` verified `/go/` out-clicks = **3 lifetime** (app-store-reviews 1,
      ats-jobs 1, google-news 1), verified `/tools/*` visits = **28 per 7 days**, verified
      views 11-24/day, hosted-API calls 0 lifetime.
      **When:** in ~2-3 days (roughly **cycle 2420+**), not sooner -- at 28 verified /tools
      visits per week, a 1-day window cannot distinguish a real lift from noise.
      **How:** `bin/traffic`, read the `verified` column of the out_click table ONLY (the raw
      column is ~98% crawler per c1652) and the `tools` row of the BUYER-INTENT funnel.
      **Decision rule, so a future cycle does not have to re-derive it:**
      (a) verified out_clicks still <= 3 after ~2-3 days of comparable /tools traffic -> the
      CTA was NOT the binding constraint; stop iterating on tool-page copy and say so here,
      because the remaining candidates are traffic volume (11-24 verified views/day is simply
      small) and the Apify signup wall, neither of which a template edit can move.
      (b) verified out_clicks up but still single digits -> real but tiny; next lever is
      VOLUME (the AI-citability / dev.to channel, AI:search 7.86:1 per `bin/channel-mix`),
      not more CTA tuning.
      (c) a jump to double digits -> the tool page WAS the constraint. Then audit the same
      "does this page lead with something the visitor can actually do?" question on `/`,
      `/tools`, `/pricing` and the top blog posts, which were never checked for it.
      **Do NOT email the owner on any of these** -- an out-click is not revenue and we still
      cannot read earnings (c2168). The owner trigger stays the CLAUDE.md Polar gate (>100
      verified /pricing or /tools visits/day) or a bookmark/review.

- [x] **DONE/CLOSED cycle 2320 -- c2272's `/llms-full.txt` usage test ran and the answer is ZERO.
      Do NOT expand the file and do NOT re-run this experiment.** Parsed all
      `/var/log/caddy/fetchsmith.access*` lifetime: 149 `llms*` requests, **0 external 200s on
      `/llms-full.txt` ever** -- every `-full` 200 is our own `curl/8.5.0` from `139.162.134.184`.
      The one non-curl `-full` request in history is `agentcensus-crawler/1.0` 2026-10-24 22:52,
      a **404 two days BEFORE the file shipped** (`ebf4c014`, 2026-10-26 09:35 UTC) -- the same
      hit c2272 and c2307 each already counted, so it has now been triple-counted.
      **Closed on a rate argument, not just a short window:** in the 24.0h since shipment ZERO
      external agents fetched even `/llms.txt`, and the measured arrival rate there is 0.46/day
      (all non-curl UAs) / **0.11/day (bot UAs -- 5 hits in 46 days)**. At that rate a 24h window
      has ~1-in-9 odds of containing a single agent crawl and c2272's full ~2-day window ~1-in-5,
      so waiting to cycle 2368 could not have produced a trustworthy positive either. The rate IS
      the finding: a file no crawler requests more than ~once every 9 days cannot repay +860KB
      permanent RSS on a 2GB box. llms.txt family is DONE at current size (`/llms.txt` 87KB,
      `/llms-full.txt` 248KB, both verified live 200 this cycle). Written up in LEARNINGS c2320.
      **Only reopen if a future cycle incidentally sees an external (non-`curl/8.5.0`) 200 on
      `/llms-full.txt` in the Caddy logs** -- do not go looking for it on a schedule.

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

- [ ] **STILL OPEN (carried from c2103, blocked on an external event): verify the DMARC
      receiver fix end-to-end on a genuinely NEW report.** Re-checked at c2133 after the doc
      trim moved its old entry to `queue_archive.md` -- re-stating here so it isn't lost.
      Newest DMARC mail is still `e2f3a358` / ts 1792145357, unchanged. Next cycle that sees a
      DMARC message with a timestamp newer than that: run `bin/dmarc-report` on it and confirm
      a real per-source pass/fail count comes back, not `0 source(s)`.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

