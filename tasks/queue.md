- [x] **DONE cycle 2647 (NORMAL slot, 2647 % 3 == 1) -- the standing c2336 `ext_bad30d`
      tripwire caught a genuine NEW entry (`nih-reporter-scraper` FAILED 1, not one of the 3
      previously-known), diagnosed to root cause and fixed, not just re-run.**
      Preflight: `checks-due`/`audit-due` both NONE DUE. Inbox had 2 new non-owner items
      beyond the known set (`c2fa5a9c` IPYE proxy-IP-lease cold pitch, `06daa491` Chinese
      "TinyGate" API-gateway cold pitch), both read in full, both non-actionable spam -- no
      reply, no owner email. Revenue/spend otherwise flat. Services/site all green before and
      after.
      The failed run (`IKBr3C9rL8Si4Zx1J`, 2026-10-29, $0 charged) was a real buyer sending
      `fiscalYears: ["FY2000",...,"FY2012"+]`. The Actor's existing input guard correctly
      refused (per its own well-commented c2444/c2352-class design, to avoid silently falling
      through to a different charged query) -- but "FY2024" is NIH's own stated convention, so
      this is a plausible real-usage shape being rejected, not a buyer typo. **Fixed**: added
      `parseFiscalYear()` (strips a leading `FY`/`fy`) in `actors/nih-reporter-scraper/src/
      main.js`, applied consistently at both the main filter and the `dropped`-value recompute
      (the latter previously used a bare `Number(y)`, a second, subtler instance of the same
      gap). Verified 3 ways: unit-level parse test, local Actor run with the exact failing
      input shape (5 rows, correct `[2023,2024]`), and a live platform re-run after push
      (build 0.1.69, run `mcS2IfliYRJIAmR8z`, SUCCEEDED/5 rows) -- the exact previously-failed
      input now works for real. Confirmed the refusal path is untouched for truly invalid
      input (`["FY1800","garbage"]` still refuses, same message). `actor-health` unchanged
      after the push. $0.005 spent (one build), $0 revenue change (original failed run stays
      $0, fix only helps future resubmissions), no owner email.
      Full detail in `state/STATUS.md` cycle-2647 entry.

- [ ] **NEW follow-up (c2647, LOW -- audit before porting, do not assume) -- check whether the
      sibling Actors that share the same `Actor.fail()`-on-invalid-`fiscalYears`-or-similar-
      year-filter pattern (`sam-gov-opportunities-scraper`, `clinicaltrials-scraper`,
      `federal-register-scraper` -- named in PLAYBOOK's cycle-2357 note as having the same
      bare-throw-to-`Actor.fail()` fix applied together with nih-reporter-scraper) have an
      analogous year-string input that could plausibly arrive "FY-prefixed" or otherwise
      year-like-but-not-a-bare-number, and whether their own fiscal/date filter guard would
      reject it today the same way nih-reporter-scraper's did before this cycle's fix.** Only
      port the `parseFiscalYear`-style normalization to the ones where (a) the field is
      actually a year/fiscal-year filter (not, e.g., a free-text date range already handled
      differently) and (b) you can point to a real plausible input shape, the same bar this
      fix cleared via an actual failed run -- do not blanket-apply without that signal.

- [x] **DONE cycle 2645 (NORMAL slot, 2645 % 3 == 2) -- genuinely clean preflight (checks-due
      and audit-due both NONE DUE, build gate still calendar-blocked to 2026-12-26, no new
      mail), so did not manufacture a code change (c2524 rule); instead ran the standing
      tripwire and a real verification.**
      Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 7c, cycle 2652).
      `audit-due --all` NONE DUE for fleet rotations / 0 one-off axes. Inbox `list 10` has 4
      non-owner items read in full this cycle, all triaged non-actionable: `a661a19a` is the
      Bytewells sender's own follow-up to its already-known `04dda4a1` pitch (same rental-
      marketplace cold outreach, not a reply needed), `5ce80b92` and `2420a902` are the same
      SEO-cold-pitch/newsletter-spam classes already triaged at c2624/c2623, plus a routine
      Google DMARC aggregate-report pair. Owner threads `2b237f1b`/`01852eaa` stay
      resolved/tracked. `bin/revenue` $0 booked, 25 Actors, 48 users, 787 runs30d (flat vs
      c2644), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.935/$85 (flat). Services all active;
      `/`, `/pricing`, `/tools` 200 before and after.
      **(a) Ran the c2336 standing `ext_bad30d` tripwire** (re-diff `state/revenue_history.json`'s
      `ext_stats30d` history) -- only the three already-known entries surface (`court-records-
      scraper` TIMED-OUT, `steam-reviews-scraper` FAILED 2026-10-26, `remote-jobs-scraper`
      TIMED-OUT 2026-10-29, triaged c2471), no new Actor name, clean.
      **(b) Live-verified the `2b237f1b` CourtListener fix is actually working**, not just
      claimed-resolved in prior STATUS prose: `bin/actor-health --only court-records-scraper`
      -> `{'ok': True, 'status': 201, 'items': 10, 'fail_rows': 0}`.
      **(c) Re-checked the c2644 `OC_UA_ROTATOR` blocker**: only 2 ip-bearing `out_click` rows
      exist now (was 1 at c2644) -- still far too few to scope a test on, correctly left
      deferred; see that open follow-up below, unchanged.
      $0 spent, $0 revenue change, no owner email. Next cycle: re-run preflight fresh; nothing
      fleet-wide due until `check-doc-size` at cycle 2652.

- [ ] **NEW follow-up (c2646, MEDIUM -- latent fleet-wide, same bug class just fixed on
      `remote-jobs-scraper`; do 2-3 per QUALITY cycle, do NOT batch-push 19 Actors at once).**
      `timeout: { request: ms }` bounds ONE HTTP attempt, not one fetch-helper CALL: got retries
      internally (`retry: { limit: 2 }`), so a host that accepts the TCP connection and then never
      answers costs **~4x** the configured timeout per call, and ~12x on helpers that retry on top.
      Measured c2646 against a socket that accepts and never replies: a `3000ms` `timeout.request`
      took **12.2s**; with `signal: AbortSignal.timeout(3000)` it took exactly **3.0s** (an
      AbortSignal bounds the whole call *including got's own retries*; `timeout.request` cannot).
      **Survey of the fleet (c2646, one-liner below): ~19 of 26 Actor dirs pair
      `timeout: { request: }` with `retry: { limit: }` and have NO `AbortSignal`, while all of them
      already have the `timeoutAt`/`remainingMs()` time budget** -- i.e. the identical structure
      that killed `remote-jobs-scraper`'s run (budget checked *between* sources, but one call can
      overrun the whole budget from inside). `_template` had it too and is **already fixed this
      cycle**, so new Actors no longer inherit it.
      Re-run the survey with:
      `cd /root/agent/actors && for d in */; do s=${d%/}; [ -f "$s/src/main.js" ] || continue; printf "%-34s req=%s retry=%s signal=%s\n" "$s" "$(grep -c 'timeout: { request:' $s/src/main.js)" "$(grep -c 'retry: { limit:' $s/src/main.js)" "$(grep -c AbortSignal $s/src/main.js)"; done`
      **Patch shape (copy from `remote-jobs-scraper/src/main.js`, the reference implementation):**
      (1) a `fetchBudgetMs()` helper clamping the cap to `remainingMs()` with a 2s floor; (2)
      `timeout: { request: budgetMs }` + `signal: AbortSignal.timeout(budgetMs)` on the gotScraping
      call; (3) a budget check at the top of the retry loop; (4) in the catch, discriminate with
      **`signal.aborted`** -- NOT the error's name/code: `AbortSignal.timeout` rejects with a
      DOMException named `TimeoutError` whose `code` is the NUMBER `23` (logs as a bare "23"), and
      got's own request timeout is *also* named `TimeoutError` (code `'ETIMEDOUT'`), so neither
      field tells them apart; (5) do **not** retry a cap-exhausting abort (the blips the retry loop
      exists for fail in milliseconds and still get all 3 attempts) -- on `remote-jobs-scraper`
      that was the difference between losing 1 board and losing 4 of 6.
      **Priority order: multi-source / paginated Actors first** (biggest blast radius, since they
      push only after every source is walked): `fda-recall-scraper` (req=4), `hacker-news-scraper`
      (req=6), `sam-gov-opportunities-scraper` (req=3), `app-store-reviews-scraper` (req=2,
      retry=3), then the 2-call ones. `ats-jobs-scraper`, `google-news-scraper`,
      `shopify-products-scraper`, `trademark-search-scraper` already have some `AbortSignal` use --
      **read before patching, they may already be covered** (do not assume from the grep count).
      Note `scholarship-scraper` has `budget=0` (no `timeoutAt` wiring at all) -- it needs the time
      budget added first, and it also still carries the UNPUSHED c2312 code fix (see that item).

- [x] **DONE cycle 2646 (QUALITY/GROWTH slot, 2646 % 3 == 0) -- the nightly FIX FAILED ACTORS task,
      both Actors diagnosed to root cause rather than just re-run until green.**
      Preflight: `checks-due --all` **NONE DUE** (soonest `check-doc-size` in 6c, cycle 2652),
      `audit-due --all` **NONE DUE** (fleet rotations + 0 one-off axes). Inbox `list 10` identical
      to the known triaged set (owner threads `2b237f1b`/`01852eaa` stay resolved/tracked; the 4
      non-owner items are the same spam/cold-pitch/DMARC classes) -- no new mail, no reply, no
      owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 787 runs30d (784 ext_ok / 3
      ext_bad, flat), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.9716/$85 (81.2% elapsed,
      projection $7.36). Services active; `/`, `/pricing`, `/tools`, `/tools/remote-jobs-scraper`
      200 before and after.
      **(a) `substack-scraper` was a TRANSIENT upstream 502** (`502 Bad Gateway` HTML from the
      edge, not our code). Re-ran `actor-health --only substack-scraper` -> `{'ok': True, 'status':
      201, 'items': 10, 'fail_rows': 0}` in 6.4s. No code change, correctly nothing to fix.
      **(b) `remote-jobs-scraper` was a REPRODUCIBLE TIMED-OUT and a real defect -- fixed, pushed
      (build 0.1.93) and verified against the live failing condition.** Re-ran first to confirm it
      reproduced (run `fDouBg3byhYIDjUUj`, TIMED-OUT again at 180s), then read the Apify run log:
      `remotive` and `remoteok` had already returned **111 rows by t+0.6s**, then
      `jobicy.com/api/v2/remote-jobs` sat in ONE `fetchJson` call for **113s** before the platform
      hard-killed the run -- so the buyer got **0 rows out of 111 already collected**, because
      pushing only starts after every source is walked. **jobicy is NOT down: it answers this box
      200 in 0.17s, twice** -- it has started blackholing Apify's egress specifically (accepts the
      connection, never replies), so this will recur and is not waitable-out.
      Root cause was NOT a missing per-source guard (the Actor already had per-source try/catch AND
      a `timeoutAt` budget check before each board): `timeout: { request: 45000 }` bounds one HTTP
      attempt, but got's internal `retry: { limit: 2 }` re-runs it, so a single call costs ~4x that
      (measured 12.2s for a 3000ms setting against a local accept-and-hang socket) -- ~180s, the
      entire default run, from *inside* a budget check that only runs *between* boards.
      Fix: `fetchBudgetMs()` + `AbortSignal.timeout()` clamped to the remaining budget on both
      `fetchJson` and `fetchText`, no retry of a cap-exhausting abort, and a log line that names
      the real cause. **Verified on the live failing condition** (run `JhqQIFPlhaCPGWKwp`): jobicy
      aborted at exactly 45000ms with
      `gave up after 45000ms (the remaining run time budget), host accepted but never answered.
      Not retrying a board that is swallowing requests`, then **all 5 other boards ran** (previously
      arbeitnow/workingnomads/wwr never got a turn) -> 264 matching / 253 unique rows, `Pushed 10
      job posting(s). (request failed for: jobicy)` -- so the buyer now gets rows AND the failure
      disclosed in the status message. `actor-health` 180s hard-kill -> `{'ok': True, items: 10}`
      in 53s.
      **(c) Fixed `actors/_template/src/main.js` too** -- it shipped the same unbounded
      `timeout`+`retry` pair, so every future Actor inherited the bug; no push needed (template is
      never deployed). Fleet survey found ~19 more Actors with the same shape -- filed as the
      follow-up item directly above with the patch shape and priority order, deliberately NOT
      batch-pushed this cycle.
      $0.005 spent (one build). Next cycle: nothing fleet-wide due until `check-doc-size` at 2652.
- [x] **DONE cycle 2644 (NORMAL slot) -- two things: the DUE `git-maintain` repack, and the
      c2642 follow-up closed out by shipping the FIRST exclusion that uses the `ip` column.**
      Preflight: `checks-due --all` 1 DUE (`git-maintain`, predicted by c2643), `audit-due --all`
      NONE DUE for fleet rotations / 0 one-off axes. Inbox `list 10` byte-identical to the known
      triaged set (owner threads `2b237f1b`/`01852eaa` stay resolved/tracked) -- no new mail, no
      reply, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 787 runs30d (784
      ext_ok/3 ext_bad, flat vs c2643), 0 bookmarks, 0 reviews. Services all active; `/`,
      `/pricing`, `/tools` 200 before and after. Disk 28%, mem 580/1967 MB used.
      **(a) `git-maintain` -- TRIPPED ON SIZE, repacked.** loose 1284 objects / 97 MiB (well
      under the 4000-OBJECT threshold, so the size gauge added at c2164 is what fired again --
      it keeps earning its place). After: 0 loose, pack 116 -> 120 MiB, `.git` 213 -> 124 MiB
      total. Services active after. c1972 failure-mode diagnostics both clean: `/dev/null` is a
      proper `crw-rw-rw- 1, 3` char device and there is NO `.git/gc.log`, so auto-gc is not
      silently disabled. Recorded via `checks-due --ran`; next due cycle 2692.
      **(b) c2642's open follow-up -- RESOLVED, and NOT the way c2641 proposed.** c2641 wanted
      an ASN/CIDR exclusion scoped tighter than `51.0.0.0/8` once `ip` samples existed. 33
      ip-bearing pageviews now exist (~1h, 2026-11-03 02:03-03:01) and they contain **ZERO
      51.x traffic**, so there was nothing to scope: **the CIDR idea is DROPPED, not deferred**
      (hardcoded ranges need upkeep as scanner IPs churn and risk excluding a real hosted
      small-business buyer). What the sample DID expose is a structural hole worth fixing:
      `vid = sha256(salt|day|ip|ua)`, so a scanner that **rotates its UA gets a new vid per
      request** and every per-vid test is blind to it -- `PV_SWEEPER` needs >=15 hits on ONE
      vid. Measured: `45.138.12.46` fetched `/` 4x in the SAME SECOND with 4 plausible browser
      UAs (no bot/crawl/spider token, so `NOTBOT` passed all 4) = 4 "visitors", caught today
      only by the `asset_hits` half -- a single point of failure that on `/pricing`/`/tools`
      could have forged the CLAUDE.md Polar trigger. Shipped `PV_UA_ROTATOR` in `bin/traffic`
      (>=3 distinct UAs from one ip within ONE second; 1s and not 60s deliberately, so 3 real
      people behind one office/CGNAT egress are not excluded). **Verified a no-op on ship**:
      isolates exactly those 4 vids, 0 of which pass `asset_hits`, and `bin/traffic` output is
      byte-identical before/after (diffed against `git show HEAD:bin/traffic`), exit 0. Only
      touches rows with `ip` populated, so pre-c2642 history is not retroactively reclassified.
      Committed `d664154e`. Buyer-intent funnel read this cycle (7d): tools 38 / pricing 4 /
      checkout 3 -- about 5/day vs the >100/day trigger, so **no owner email**, correctly.
      Full detail in `notes/LEARNINGS.md` under the c2644 heading.

- [ ] **NEW follow-up (c2644, LOW -- SAFE direction, do not rush) -- `vid` is unstable within a
      single session when the visitor's egress IP rotates, which makes `VERIFIED` UNDERCOUNT
      real humans.** Same c2644 sample, opposite direction to the overcount fixed above: one
      session's pageview came from `74.7.228.187` and its `out_click` 2 seconds later from
      `74.7.228.253` -- same /24, different /32, so `sha256(salt|day|ip|ua)` produced a
      DIFFERENT vid for one continuous visitor. Consequence: for anyone behind a rotating
      egress pool (corporate proxy, CGNAT, mobile carrier) the `/static/*` fetch can land under
      a different vid than the pageview, so `vid IN (SELECT vid FROM asset_hits)` -- the oldest
      and most load-bearing half of `VERIFIED` -- fails for a GENUINE human. **Why this is not
      urgent:** the bias is an undercount, so it cannot forge a Polar escalation; it can only
      hide real buyer intent. **Do NOT change `visitor_token()` to /24 granularity on this one
      observation** -- the only sample is a single OAI-SearchBot session (its UA carries
      `OAI-SearchBot/1.4` appended after a Chrome string, so it was correctly excluded anyway),
      i.e. there is as yet NO evidence a real human was undercounted. Cheap check for a future
      cycle once more `ip` data has accumulated: count distinct vids per (ip /24, day) where
      the UAs are IDENTICAL -- identical UA + same /24 + different /32 is the rotating-egress
      signature. Only if that shows a material number of human-looking sessions is it worth
      hashing the /24 instead of the /32 (and note that widening the hash input also widens the
      UA-rotator blind spot above, so the two must be re-tuned together).

- [ ] **NEW follow-up (c2644, LOW, blocked on sample size) -- mirror `PV_UA_ROTATOR` on the
      out_click side once `ip` data exists there.** The same UA-rotation blind spot applies to
      `OC_SWEEPER` for exactly the same reason (it groups by `$.vid`, and a UA-rotating scanner
      gets one vid per click), so `OC_VERIFIED` has the identical single-point-of-failure on its
      `asset_hits` half. NOT shipped this cycle because **only 1 `out_click` row carries an `ip`
      key so far** (the 02:05:02 OAI-SearchBot row, ip `74.7.228.253`) -- that is not a sample,
      and c2642's own standing guidance is to write the clause only once one exists. When
      revisiting: `sqlite3 data/fetchsmith.db "SELECT COUNT(*) FROM events WHERE kind LIKE
      'out_click%' AND payload LIKE '%\"ip\"%'"`; with a few dozen rows, port the same
      one-second / >=3-distinct-UA test over `json_extract(payload,'$.ip')` and
      `json_extract(payload,'$.ua')`, and verify it is a no-op on ship the same way c2644 did
      (diff full `bin/traffic` output against `git show HEAD:bin/traffic`).

- [x] **DONE cycle 2643 (QUALITY/GROWTH slot, 2643 % 3 == 0) -- ran the `tasks/queue.md` trim
      `check-doc-size` flagged TRIM SOON at c2641/c2642 and correctly deferred to this slot.**
      Preflight: `checks-due --all` **NONE DUE** (soonest `git-maintain` in 1 cycle, cycle 2644).
      `audit-due --all` **NONE DUE** for FLEET ROTATIONS, 0 one-off axes DUE. Inbox `list 10`
      byte-identical to the known triaged set (owner threads `2b237f1b`/`01852eaa` stay
      resolved/tracked; rest the same marketing/spam/DMARC triaged for weeks) -- no new mail,
      no reply, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 787 runs30d (784
      ext_ok/3 ext_bad, flat), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.9325/$85 (flat,
      cycle projection $7.33). `check-doc-size` pre-trim: STATUS.md/LEARNINGS.md OK, queue.md
      TRIM SOON (80.1KB/867 lines, proj. 208KB at next look) -- the trigger for this cycle's
      work. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
      `/tools` 200 before and after.
      **Work -- executed the trim (standing-hazard grep FIRST, then hoist-then-cut via
      `bin/_trim2643q.py`): 80.1KB/867 -> 55.7KB/573 lines.** Structure was 11 DONE blocks + 21
      open, and unlike every prior trim the DONE blocks were NOT all contiguous -- two older
      `DONE/CLOSED c2636` blocks (the feed-syndication resolution and the `/blog/null` closed
      bug) sat interleaved further down among the open items rather than at the top with the
      other 9. Generalized the script to find the newest-by-cycle-number DONE block (2642, kept
      for its "next cycle" pointer) and archive the other 10 regardless of position, rather than
      assuming a single contiguous archive-bound range. **Standing-hazard grep (run first, on
      all 10 to-be-archived blocks, not a contiguous line range this time): 6 hits, all CLEAN.**
      The feed-syndication "do not re-litigate" language already has a live home at
      `notes/LEARNINGS.md:7058-7066`; the "6/7 free directories closed, do not retry" fact
      already lives at `notes/PLAYBOOK.md:231`; the `/blog/null` "do not re-investigate" footnote
      has no separate live home but is low-risk (closed, verified-fixed bug, full text survives
      verbatim in the archive). Nothing needed rehoming beyond what already has one.
      **Guards, all passed:** script's own asserts (867-line precondition, exact block counts
      11 DONE/21 open, newest-DONE cycle 2642, partition is total/non-overlapping, multiset-
      identical reconstruction of the original file) all held on the live file; open-item set
      md5 `abda932f07f0f23a4710e71f298f5a24` identical before and after; all 294 archived lines
      verified present in `queue_archive.md` by direct membership check via `difflib` opcode
      diff (0 missing). `check-doc-size` post-cut reads OK on all three docs (queue.md
      55.7KB/573 lines, proj. 183KB at next look, ~27c headroom). Services + `/`, `/pricing`,
      `/tools` re-checked 200/active after the write.
      **No open items needed retiring or rewriting** -- same "DONE-only cut was enough" outcome
      as c2634/c2574/c2588.
      $0 spent (all read-only/local file operations). Next trim: do NOT quote a target cycle --
      re-run `check-doc-size` and trust its verdict.

- [x] **DONE cycle 2642 (NORMAL slot) -- half of the c2641 follow-up shipped: `pageviews` and
      the two `out_click` payloads now carry the client IP.** `site/app.py`: new `client_ip()`
      helper (factored out of `visitor_token()`, which previously computed and discarded it);
      `ip` column added to `pageviews` via the same `PRAGMA table_info` + `ALTER TABLE` guard
      `vid` used; `"ip"` key added to the `out_click` JSON payloads in `/go/{slug}` and
      `/go-store`. Verified live: `py_compile` clean, `systemctl restart fetchsmith-web` OK,
      `/`, `/pricing`, `/tools` 200 before/after, `PRAGMA table_info(pageviews)` shows the new
      column, a live curl produced a pageview + out_click row with this box's real IP
      populated, `bin/traffic` runs unchanged against the new schema. Self-test rows deleted
      after verification. Committed `328e6e4c` (not left for the safety-net). Existing rows
      (incl. the c2641 16 OVH events) stay NULL for `ip` -- no backfill attempted, expected.
      **NOT done, still open -- the ASN/CIDR exclusion itself:** c2641 explicitly flagged
      `51.0.0.0/8` as too broad and said to scope tighter once more samples exist. Only one
      cycle's worth of real-traffic `ip` data exists now (this cycle's restart); the next
      cycle that revisits this should check how many NEW out_click/pageview rows have a
      populated, non-self `ip` by then, and only write a `bin/traffic` `VERIFIED`/`OC_VERIFIED`
      exclusion clause once there's enough of a sample to scope it to the narrowest range that
      covers observed bot IPs without risking excluding a real OVH-hosted small-business buyer.
      Full evidence (timestamps, IPs, UA) in STATUS.md's c2641 block and `notes/LEARNINGS.md`.

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
      **Re-checked live cycle 2583 (2026-11-01): still food 1, drug 2, device 1 -- unchanged from
      c2552's measurement, no count at 0, tripwire has not fired, no action taken.**
      **Re-checked live cycle 2620 (2026-11-02): still food 1, drug 2, device 1 -- EXACTLY
      unchanged for a third consecutive reading (c2552, c2583, c2620), no count at 0, tripwire has
      not fired, no action taken.** Worth noting the stability: the c2552 rationale for the
      tripwire was that the counts "demonstrably move" (food went 2 -> 1 between 2026-10-06 and
      c2552), but across the 32 days since they have not moved at all, so the practical risk is
      lower than c2552 assumed. Keep the tripwire (n=1 on food and device still means one
      reclassification kills the value), but do NOT spend a dedicated cycle on it -- piggyback the
      3 curls on any cycle that already touches this Actor, as c2620 did.

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

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, c2556, c2567, c2574,
      REWRITTEN AGAIN c2588; c2628/c2634/c2643 STATUS PREPENDED BELOW).**
      **EXECUTED c2643 (QUALITY/GROWTH slot, 2643 % 3 == 0) -- `tasks/queue.md` ONLY, full
      detail in this cycle's own DONE block at the top of the file.** `check-doc-size` read
      TRIM SOON at preflight (80.1KB/867 lines); this trim's DONE blocks were the first NOT all
      contiguous (two older `DONE/CLOSED c2636` blocks sat interleaved among open items), so
      `bin/_trim2643q.py` generalized the hoist-then-cut to find the newest-by-cycle-number DONE
      block rather than assume a single archive-bound range. Standing-hazard grep (6 hits, all
      CLEAN -- each either already lives in PLAYBOOK.md/LEARNINGS.md or is a low-risk closed-bug
      footnote preserved verbatim in the archive) run first. 80.1KB/867 -> 55.7KB/573 lines,
      ~27c headroom. Open-item md5 unchanged, all 294 archived lines verified present in
      `queue_archive.md`. No open items needed retiring.
      **EXECUTED c2634 (QUALITY/GROWTH slot, 2634 % 3 == 0) -- `tasks/queue.md` ONLY** (STATUS.md
      and LEARNINGS.md both read OK at preflight, ~33c/~47c headroom respectively, so per the
      c2224 rule only queue.md was in scope). `check-doc-size` read TRIM SOON at preflight
      (79.1KB/845 lines, proj. 207KB at the checker's next look). **Standing-hazard grep run
      FIRST, correctly ordered this time (per c2628's recorded ordering slip):** extracted the
      archive-bound range (lines 27-299, the 6 oldest DONE blocks c2627-2632) to `/tmp` and
      grepped for rule-shaped language (`never |always |must |rule:|do not |don't `) before
      cutting anything. 4 candidate hits, all verified to already have a live home outside the
      archived range: "never build into a demand/competition<~50 niche" and "never hand-roll the
      curl" are both stated in `notes/PLAYBOOK.md` (lines 40 and 228); the court-records-scraper
      `CL_API_TOKEN` re-attempt caution and the `pagination_audit_closed` reasoning both live in
      `state/audit_dates.json` per-Actor notes (`input_error_advice_note`, `pagination_audit_
      closed`), independent of queue.md. CLEAN, nothing rehomed.
      **Cut:** hoist-then-cut (`bin/_trim2634q.py`, same method as 2588/2604/2605/2619/2628):
      file held 7 DONE blocks (2627-2633) + 22 open items, interleaved in exactly the shape prior
      trims leave behind (newest DONE at the top, older DONE immediately after, open items as the
      tail). Kept all 22 open + newest DONE (2633), archived the other 6 (2627-2632) ->
      79.1KB/845 -> 55.7KB/573 lines.
      **Guards, all passed:** script's own asserts (845-line precondition, exact block counts,
      partition is total/non-overlapping, multiset-identical reconstruction of the original file)
      all held on the live file, not just in the abstract; open-item-set md5
      `7f82e6a4ca28777f4fcd07be51536117` identical before and after (and identical to the hash
      recorded at the c2628 cut, confirming the 22 open items have not drifted since); every one
      of the 272 archived lines verified present in `queue_archive.md` by direct membership check
      (0 missing); `check-doc-size` post-cut reads OK on all three docs (queue.md 55.7KB/573
      lines, proj. 183KB at next look, ~27c headroom). Services (`fetchsmith-web`,
      `fetchsmith-mail`, `caddy`) and `/`, `/pricing`, `/tools` re-checked 200/active after the
      write.
      **Margin check (per the c2628 LEARNINGS note -- don't trust a DONE-only cut blindly):**
      `200KB - rate*24` = `200 - 5440*24/1024` ≈ 72.5KB trim-line-equivalent; post-cut queue.md
      sits at 55.7KB, ~17KB under that line -- comfortably better margin than the last two cuts
      (c2628 had only ~19KB, c2588 only ~28KB against a lower rate), because this cut's
      archive-bound range (6 DONE blocks) was proportionally larger relative to the open-item tail
      than at c2628. **No open items needed retiring or rewriting** -- same "DONE-only cut was
      enough" outcome as c2574/c2588, not the c2556 shape.
      $0 spent (all read-only/local file operations). Next trim: do NOT quote a target cycle --
      re-run `check-doc-size` and trust its verdict; it will likely read OK for a long stretch
      given the margin above.
      **PRIOR EXECUTED c2628 (QUALITY/GROWTH slot, 2628 % 3 == 0) -- BOTH live docs, in the QUALITY slot
      the checker itself asked for.** `check-doc-size` read TRIM SOON on both at preflight and said
      verbatim "trim proactively in a QUALITY slot rather than waiting for the escalation (cycle
      2220 follow-up)", and c2604's note that a second QUALITY slot must not pass it was honored.
      Partition shape re-derived fresh from the live files, never pasted: `state/STATUS.md` 28
      blocks 2627..2600 no gaps, stock `KEEP_BLOCKS=5` -> 121.3KB/1516 -> 26.4KB/337 lines
      (`bin/_trim2628.py`, archived cycles 2600-2622). `tasks/queue.md` held 10 DONE / 22 open
      interleaved, so hoist-then-cut (`bin/_trim2628q.py`): kept all 22 open + newest DONE (2627),
      archived the other 9 (2618-2626) -> 91.9KB/988 -> 54.0KB/554 lines.
      **Standing-hazard grep: CLEAN, but note the ORDERING SLIP -- the cut ran BEFORE the grep this
      cycle, which the cadence says not to do.** It was recoverable only because the archives keep
      every line verbatim and pre-cut backups existed, so the archived ranges were reconstructed by
      difflib against the backups and grepped in full afterwards. All 49 keyword hits (34 STATUS /
      15 queue) were narrative; the three that read like real instructions were each verified to
      still have a live home: json round-trip / "always edit the raw text" (`LEARNINGS.md:1783`),
      `autocommit.log` substantive-path semantics (`:6677`), STALE-reads-the-DATE-not-the-NUMBER
      (`:6720`), plus the fda-recall "never spend a dedicated cycle" guidance which is in a live
      OPEN queue item. **Next cycle doing this: grep FIRST, then cut -- do not rely on the backups
      bailing you out twice.**
      **Guards after:** `check-status-blocks-kept` OK (0 destroyed, 1031 blocks across
      STATUS.md+archive), `check-status-continuity` NONE MISSING on the retained 2623..2627 window,
      0 archived lines missing from either archive file (checked by membership, both directions),
      queue open-item set byte-identical across the cut (md5 `7f82e6a4ca28777f4fcd07be51536117`
      before and after), `check-doc-size` now OK on all three docs. Services + `/`, `/pricing`,
      `/tools` re-checked 200/active.
      **CAVEAT for the next trim -- do the arithmetic, a DONE-only cut is getting marginal.**
      Post-cut `queue.md` still projects **181KB at the checker's own next look (c2652), only ~19KB
      of margin** at +5440 B/cycle; STATUS.md is comfortable (proj. 132KB, ~39c headroom). So
      queue.md will re-flag TRIM SOON within a look or two, and archiving DONE blocks alone may no
      longer be enough -- expect to have to retire or compress genuinely dead OPEN items too (c2556
      is the precedent for needing more than a DONE-only cut).
      **SUPERSEDED c2605 execution, kept for rate context (normal slot, nothing else due) -- the
      c2604-deferred trim, on BOTH live
      docs.** Re-derived the partition shape fresh (did not trust c2604's pre-prepend numbers, as
      instructed): `state/STATUS.md` 21 blocks 2604..2584 no gaps, stock `KEEP_BLOCKS=5` ->
      101.8KB/1248 -> 25.2KB/309 lines (`bin/_trim2605.py`). `tasks/queue.md` actually held 19 DONE
      blocks / 24 open items (not 18/24 -- one more DONE block had landed since c2604 measured it),
      so `bin/_trim2605q.py` parses the live block list generically rather than hand-picking line
      ranges: kept all 24 open items + only the newest DONE block (2604) live, archived the other
      18 -> 94.5KB/1000 -> 54.5KB/559 lines. Standing-hazard grep run on both archive ranges first,
      per the mandatory step: nothing found (every hit was narrative about a cadence homed
      elsewhere, or the original c2593 finding, intentionally superseded by c2604's rehoming).
      Verified: open-item set byte-identical across the queue.md cut (diff empty), both scripts
      assert keep+archive reconstructs the original file exactly, both pre-commit guards
      (`check-status-blocks-kept`, `check-status-continuity`) clean post-cut, site/services
      re-checked 200/active. Both docs now read OK with ~22-27 cycles of headroom -- full
      numbers in the STATUS.md c2605 block. **Next cycle: do NOT re-trim until `check-doc-size`
      reads SOON again; this cadence item goes quiet until then.**
      **c2604 (QUALITY slot, superseded by the above): `check-doc-size` read TRIM SOON on BOTH live
      docs. The check is recorded as RAN (clock reset, next look c2628) but THE TRIM WAS NOT DONE**
      -- the cadence's
      own mandatory standing-hazard grep turned up a real `worker/run.sh` defect (see the DONE 2604
      block at the top of this file) and the slot went there instead. **This was then the top
      QUALITY-slot item.** Both files will read TRIM DUE at c2628 regardless. Nothing is lost by
      the delay, but do NOT let a second QUALITY slot pass it.
      **Pre-derived structure, measured at c2604 -- re-run the two greps first, because THIS
      CYCLE'S OWN BLOCKS SHIFTED EVERY LINE NUMBER (queue.md 912 -> 963 lines; STATUS.md gained a
      2604 block at the top). The line numbers below are the c2604 PRE-prepend values and are
      recorded for the PARTITION SHAPE only; re-derive the integers, never paste them.**
      - `state/STATUS.md` (was 95.2KB/1165 lines, proj. 201KB): grep
        `^Updated:.*by cycle [0-9]+|^PRIOR \(cycle [0-9]+` -> **20 blocks, strictly newest-first,
        2603 down to 2584, NO GAPS** (note one is a `PRIOR (cycle 2588` header, which the stock
        regex in `bin/_trim2574.py` already handles). Stock `KEEP_BLOCKS = 5` keeps 2603..2599 live
        and archives 2584-2598; the cut landed on the `2598` header (pre-prepend line 281), and
        pre-prepend lines 279/280 are `---` + blank, so the block boundary is clean. Post-cut is
        ~280 lines / ~23KB, i.e. far under the 200KB-minus-24-cycles-of-growth line. Clone
        `bin/_trim2574.py` verbatim and change only `NLINES`, the block count, the expected cycle
        range and the archive header. **Add +1 to KEEP_BLOCKS if the 2604 block is to stay live.**
      - `tasks/queue.md` (was 86.6KB/912 lines, proj. 214KB -- the worse of the two): MUST use
        hoist-then-cut (`bin/_trim2588q.py`), because open items are interleaved among DONE blocks.
        At c2604 the file held **24 open `- [ ]` items and 18 DONE `- [x]` blocks**, interleaved in
        exactly 4 runs: `[DONE 2603] [DONE 2602..2592 + 2601] [open c2601, c2592] [DONE 2591,
        2590, 2589, 2588, 2587] [open c2552 .. c2120 to EOF]`. So the partition is only 3 archive
        ranges and 4 kept ranges, and **every range boundary was verified to be a blank line**
        (pre-prepend 26/27, 342/343, 364/365, 462/463, 912). Keep the newest DONE block live for
        its "next cycle" pointer, archive the other 17. Assert the partition is total,
        non-overlapping and multiset-identical before writing, and assert no `- [ ]` lands in the
        archive -- the script already does all three.
      - `notes/LEARNINGS.md` read OK (6608 lines, ~70c headroom at +20 lines/cycle) and is left
        alone per the c2224 rule against trimming anything short of its own SOON/DUE flag. c2604
        appended ~45 lines to it, so budget that.
      **Standing-hazard check is NOT optional and c2604 is the proof.** It is the step that found
      the `run.sh` defect, and it found a rule genuinely about to be lost (the autocommit.log
      interpretation rule, homed only in the c2596 blocks in BOTH files' archive ranges). Both
      archive sets this cycle contained it. Do the grep, read every hit in full, and rehome
      anything whose only home is an archive-bound block BEFORE cutting.
      **Executed c2588 (normal slot, 2588 % 3 == 2; `checks-due --all` and all three `audit-due`
      axes read NONE DUE at preflight and every non-gated queue item was blocked or latent, so
      per the standing rule the cycle spent itself on this QUALITY work): `tasks/queue.md` ONLY.**
      80.5KB/858 lines -> 44.1KB/443 lines via `bin/_trim2588q.py` (hoist-then-cut), archiving 11
      DONE blocks (2586, 2585, 2584, 2580, 2581, 2575, 2573, 2576, 2577, 2578, 2579) plus the
      SUPERSEDED-by-c2576 projects-endpoint notice; the 2587 DONE block stayed live for its
      "next cycle" pointer. All 22 open items verified byte-identical across the cut by md5 of
      the `^- [ ]` line set (`85bff3a3...` before and after), and the script asserts no open item
      lands in the archive partition and no DONE block but 2587 survives in the kept one.
      Post-cut `check-doc-size` reads OK with proj. 172KB at its own next look (vs. 208KB before),
      so queue.md should NOT re-flag at the next look.
      **`state/STATUS.md` was deliberately NOT trimmed and is the next one due.** It read OK
      (91.8KB/1172 lines, proj. 197KB) per the c2224 rule against trimming on anything short of
      the file's own SOON/DUE flag -- but it is only ~3KB of projection under the line, and the
      arithmetic says it flips next cycle: at +4510 B/cycle, one more cycle puts it at ~96.3KB
      with proj. ~204KB > 200KB. **Expect STATUS.md to read TRIM SOON at the very next preflight
      and plan the slot for it** (copy `bin/_trim2574.py`, the stock keep-newest-5-blocks cut --
      re-derive the line ranges from the live file's own `Updated:` headers first, they are
      hand-written, not parameterized). `notes/LEARNINGS.md` (6339 lines, ~83c headroom) read OK
      and was left alone for the same c2224 reason.
      **Prior execution, for rate context (c2574, QUALITY/GROWTH slot): BOTH files**, since both
      independently read TRIM SOON then. `queue.md`: 73.6KB/785 lines -> 51.8KB/532 lines via
      `bin/_trim2574q.py`. `STATUS.md`: 116.9KB/1427 lines -> 27.8KB/357 lines via
      `bin/_trim2574.py`, archiving cycles 2548-2568.
      **DO NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size` each
      cycle and trust its OK / TRIM SOON / TRIM DUE verdict directly -- it is not a calendar; TRIM
      SOON fires as soon as the projected size at the checker's own next scheduled look crosses
      200KB, which can arrive well before cumulative growth from the last trim alone would reach
      200KB.
      **Lesson re-confirmed c2588 (and c2574 before it): archiving DONE blocks alone was again
      enough** -- no open item needed retiring or rewriting beyond this cadence item's own status
      update, on either cycle. But c2588 is also the cycle that shows a DONE-only cut is NOT
      automatically comfortable: 44.1KB post-cut still projects 172KB at the next look, i.e. only
      ~28KB of projection margin, because the growth rate itself (+5440 B/cycle) has risen with
      the per-cycle narrative. Check the arithmetic (`200KB - rate*cycles_to_next_look` vs. the
      post-cut size) every time rather than assuming a DONE-only cut suffices -- c2556 needed
      more than that, and if the rate keeps climbing the next queue.md trim will too.
      **Method:** copy `bin/_trim2588q.py` (queue.md, hoist-then-cut, newest one-shot and the one
      to clone) / `bin/_trim2574.py` (STATUS.md, stock keep-newest-5 block cut, same pattern as
      `bin/_trim2532.py`) / `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body
      move, never the highlights block). All are hand-written one-shots with explicit line
      ranges, NOT parameterized, so budget real time to re-derive the ranges from the live
      file's current headers before writing the next one. queue.md MUST use hoist-then-cut,
      because open `- [ ] ` items are interleaved among `- [x]` DONE blocks and a line cut
      would silently delete live work; assert the kept/hoisted/archived partition is total,
      non-overlapping and multiset-identical to the original before writing (and assert any new
      rewrite text separately, since it breaks that identity by design). STATUS.md carries no
      interleaved open items and is guarded by `bin/check-status-blocks-kept` at pre-commit plus
      `check-status-continuity`; both ran clean after this trim (0 blocks destroyed, NONE
      MISSING on the retained window).
      **Standing hazard, re-checked c2588, nothing found:** cadence instructions living only in
      queue.md prose have vanished into the archive before while the tool they describe still
      looked maintained (`bin/devto-comments`, `bin/check-competitor-claims`) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      12 blocks archived at c2588 were checked this way (c2574 did the same for its 8): every
      "standing"/"cadence" phrase inside them is narrative *about* a cadence homed elsewhere --
      the checks-due/audit-due cadences live in those tools' own state, the dev.to syndication
      cadence in PLAYBOOK + `state/devto_syndicated.json`, and the one phrase that genuinely read
      like an instruction (the c2580 block's "**standing lesson:** never round-trip a state JSON
      through `json.dump` to change one string") was only archived after confirming it already
      has two homes in `notes/LEARNINGS.md` (lines 1729 and 5581). **Do the grep, then read the
      hits** -- the keyword alone over-matches, since nearly every DONE block says "per the
      standing rule" about a rule that lives in CLAUDE.md.

- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556, c2567; DOWNGRADED FROM HIGH c2607 --
      superseded c2532/c2537/c2548/c2552/c2556 narrative is in `queue_archive.md`).**
      **The original complaint -- that bare `bin/audit-due --all` silently defaulted to
      `competitor_audit` and never surfaced `unreachable_remedy` -- was fixed at c2601
      (`sweep_all_types()`), so the "run `--type unreachable_remedy` explicitly every cycle"
      workaround below is no longer necessary.** Re-verified live at c2607: bare `--all`'s FLEET
      ROTATIONS bucket and an explicit `--type unreachable_remedy` call agree (`NONE DUE`, soonest
      `court-records-scraper` in 264c / cycle 2871 by direct call -- matches `--all`'s own NONE DUE
      verdict for this axis). **Trust bare `--all` going forward; the explicit by-name call is only
      needed if you want this axis's own NEXT TARGET printed, not for correctness.**
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
      **c2583 re-derived the candidate list fresh (fleet-wide `grep -rnE "[0-9]+\s*(→|->)\s*
      [0-9]+" actors/*/README.md`) and found no new qualifying candidate: the only Actors whose
      README carries ANY N->M arrow near "listing"/"match" text are `ats-jobs-scraper`,
      `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `remote-jobs-scraper` and
      `us-federal-awards-scraper`, and all five show "no new undercutter" narratives from spot-
      resweeps within the last ~5-20 cycles (remote-jobs-scraper cycle 2376, fec cycle 2375,
      clinicaltrials/us-federal-awards/ats-jobs all re-verified within October) rather than the
      specific "stated README count is stale behind a RISING live total" gap this method targets.
      None had a parseable stale count worth a fresh six-step pass today. Re-check this grep
      fresh again next time rather than trusting this list -- any README could grow the shape
      between cycles.
      **c2635 re-ran the grep fresh: 9 files now match (up from 5), but still no qualifying
      candidate.** The 3 new hits are all false leads or already-covered: `sam-gov-
      opportunities-scraper`'s arrow is a SAM.gov set-aside-code count growth (`SBA` 1,204,971
      -> 1,206,126), not a Store-listing count, so it never matched the "listing"/"match" text
      filter; `fec-campaign-finance-scraper` was already spot-resweeped 2026-10-28 (next full
      due cycle 2783) and `us-federal-awards-scraper` was fully resweeped ~2026-10-18 (since
      superseded). Of the original 5, `remote-jobs-scraper` was freshly resweeped as recently
      as cycle 2617 (2026-11-02, same calendar day as this check), and `clinicaltrials-scraper`
      /`ats-jobs-scraper` both within the first 10 days of October. **Still 0-for-2 across
      c2583 and c2635** -- the method remains sound (re-grep fresh every time, don't trust a
      cached list) but this niche-set appears to be staying well-covered on its own cadence;
      worth trying again in another ~5-10 cycles rather than every cycle.
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

