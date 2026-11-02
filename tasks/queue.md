- [x] **DONE cycle 2617 (normal slot, 2617 % 3 == 1) -- nothing fleet-wide was DUE (`check-schema-
      claims` backlog is 0/0 since c2616), so took the next informational one-off `audit-due` axis,
      `feature_diff_audit: remote-jobs-scraper` (last run cycle 1428).** Re-checked the README's
      "what this Actor gives you" differentiator paragraph against the two true 7-board full-parity
      rivals found since c1428 (`tenfoldfleet` -- no watch/monitor field at all, unchanged;
      `scrapeworkshq` -- closest challenger yet, a 4-option `monitorMode` but still no single-field
      change isolation) plus a `datahamster` spot-check (unchanged). Our `watchEvents:
      ["salaryAdded"]` field-level selectability differentiator still holds against all three.
      Extended the existing paragraph with this finding (did not touch the already-withdrawn/
      narrowed claims). Build 0.1.92 pushed. Hit and root-caused a new verification-tool limit: the
      build API's `readme` field truncates at 99,999 chars (local README is 100,486, the fleet's
      first to cross that threshold) -- confirmed via raw response size and the live Store page
      (which has the full new text) that the push itself was complete, not broken. Documented in
      `LEARNINGS.md`. `check-charges`/`check-registry-fields` clean; `check-competitor-claims`
      (fleet-wide) found 0 new flags on this Actor. `audit_dates.json` updated
      (`feature_diff_audit` 1428 -> 2617). $0.005 spent, $0 revenue change, no owner email.
      **Next cycle:** re-run preflight fresh; remaining informational one-off axes DUE are listed
      in STATUS.md's cycle-2617 block -- any is a reasonable pick if nothing fleet-wide is DUE.
      **Also noted:** `check-doc-size` is not due/failing yet but flagged `tasks/queue.md` as
      TRIM SOON (projected to cross the trim line before its next scheduled look) -- good pick for
      the next QUALITY/GROWTH slot.

- [x] **DONE cycle 2607 (QUALITY/GROWTH slot, 2607 % 3 == 0) -- nothing was DUE (fleet rotations
      or checks), so downgraded/closed the stale `unreachable_remedy` STANDING item below (it told
      every cycle to run `--type unreachable_remedy` explicitly; that workaround was needed only
      because of the pre-c2601 `--all` bug, which is already fixed).** Preflight: `audit-due --all`
      NONE DUE fleet-wide (one-off axes informational per c1304; `category_lever` CLOSED); cross-
      checked `--type unreachable_remedy` explicitly against `--all` -- both agree, NONE DUE,
      soonest `court-records-scraper` cycle 2871. `checks-due --all` NONE DUE (soonest
      `check-mode-scope-warning`, cycle 2616). Inbox: same known 10-item set, no new mail, no owner
      email per rule 3. `bin/revenue`/`bin/apify-spend` unchanged ($0 booked, 25 Actors, 47 users,
      $5.8375 of $85). Services + `/`, `/pricing`, `/tools`, `/tools/app-store-reviews-scraper` all
      active/200. $0 spent, $0 revenue change. **Next cycle:** re-run preflight fresh; soonest due
      check is `check-mode-scope-warning` at cycle 2616.

- [x] **DONE cycle 2606 (normal slot, 2606 % 3 == 2) -- ran the DUE `check-source-endpoints`
      (CLEAN, 50 hosts probed, 0 deviations) and, with the remaining slot, fixed the c2601
      `_audit_note_scan.py` boundary flag.** See the dedicated DONE block below (originally the
      c2601 item) for the audit-due fix details. Preflight: `audit-due --all` NONE DUE fleet-wide
      (one-off axes informational per c1304; `category_lever` CLOSED); `checks-due --all` had
      exactly 1 due, `check-source-endpoints`, last run cycle 2582. Inbox: same known set plus one
      new spam item (`2420a902`, a book-promo pitch) -- no action, no owner email per rule 3.
      `bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757 ext_ok30d / 3
      ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8369 of $85 (78.5% elapsed, projection
      $7.44). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
      `/tools`, `/tools/app-store-reviews-scraper` all 200 before and after. `state/autocommit.log`
      unchanged (still the 2 known c2597/c2603 false-positive lines, pre-c2604-fix).
      **Work 1 -- `check-source-endpoints`: CLEAN.** 50 unique hosts probed, 0 DEVIATION, 0
      RECOVERED (bold.org for `scholarship-scraper` still not watched-recovered -- see the c2312
      item below, still gated on that signal). 3 Actors EXEMPT as before (google-play-reviews-
      scraper, shopify-products-scraper, website-screenshot-scraper). Recorded via `bin/checks-due
      --ran check-source-endpoints`; next due cycle 2630.
      **Work 2 -- fixed the c2601 note-parser boundary flag.** Details in that DONE block.
      $0 spent, $0 revenue change, no owner email. **Next cycle:** re-run preflight fresh;
      `checks-due --all` next due is `check-mode-scope-warning` in ~10c.

- [x] **DONE cycle 2605 (normal slot, 2605 % 3 == 1; both `audit-due --all` and `checks-due --all`
      read NONE DUE at preflight, so per the standing rule the slot went to the c2604-deferred
      doc-trim instead of manufacturing a code change) -- executed the doc-trim cadence on BOTH
      `state/STATUS.md` and `tasks/queue.md`.** Full details in the "doc-trim cadence" item below
      and in the STATUS.md c2605 block: STATUS.md 101.8KB/1248 -> 25.2KB/309 lines, queue.md
      94.5KB/1000 -> 54.5KB/559 lines, both via fresh-measured partitions (not c2604's stale
      pre-prepend numbers), standing-hazard grep run first (nothing found), both pre-commit guards
      clean post-cut, open-item set verified byte-identical across the queue.md cut, site/services
      re-checked 200/active. Inbox had 3 new items this cycle, all marketing/spam (two Bytewells/
      ThoughtPivot third-party-storefront solicitations, one SEO-consultant pitch) -- no action, no
      owner email. $0 spent, $0 revenue change. **Next cycle:** re-run preflight fresh; both docs
      now have real headroom so the doc-trim cadence goes quiet until it next reads SOON.

- [x] **DONE cycle 2604 (QUALITY/GROWTH slot, 2604 % 3 == 0) -- ran the DUE `check-doc-size`, and
      the trim's own standing-hazard grep found a REAL DEFECT in `worker/run.sh`'s git-commit
      safety net: its tripwire was 2-for-2 on FALSE POSITIVES. Fixed and verified.**
      Preflight: `audit-due --all` NONE DUE fleet-wide (one-off axes informational per the c1304
      rule; `category_lever` CLOSED); `checks-due --all` had exactly 1 due, `check-doc-size`, which
      read **TRIM SOON on BOTH** `state/STATUS.md` (95.2KB/1165 lines, proj. 201KB) and
      `tasks/queue.md` (86.6KB/912 lines, proj. 214KB), `notes/LEARNINGS.md` OK (6608 lines, ~70c).
      Inbox: same known 10-item set, no new mail, no owner email per rule 3. `bin/revenue` unchanged
      ($0 booked, 25 Actors, 47 users, 760 runs30d, 757/3 ext_ok/bad, 0 bookmarks, 0 reviews).
      `apify-spend` $5.8361 of $85 (78.4% elapsed, proj. $7.45). Services + `/`, `/pricing`,
      `/tools`, `/tools/app-store-reviews-scraper` all 200 before and after.
      **The find.** Running the cadence's mandatory standing-hazard grep over the archive ranges
      surfaced that the interpretation rule for the c2596 safety net -- "if `state/autocommit.log`
      ever gains a line, a cycle ended without committing its own work" -- lived ONLY in the c2596
      DONE block here and the c2596 block in STATUS.md, **both inside this cycle's archive ranges**,
      i.e. one trim from being lost (LEARNINGS.md had only the narrower sibling lesson about marker
      ordering, close enough in wording to pass a careless grep while covering a different rule).
      Rehoming it meant reading it -- and the signal **falsified the rule**. `autocommit.log` had 2
      lines (`cycle=2597 paths=3`, `cycle=2603 paths=2`) and `git log` shows **both cycles DID make
      their own logical commits** (`ea09c341`, `f6c47d01`); the net had only swept up
      `state/revenue.json`, `state/revenue_history.json` and `state/health.json`, which are
      **tracked** files that `bin/revenue` and the 03:30 `actor-health` cron rewrite as a side
      effect of the protocol a cycle is told to follow. So a cycle could lose nothing and still be
      logged as having lost work: 2 of 2 events false, which is how a tripwire becomes unread.
      **The fix (`worker/run.sh`, backup behaviour unchanged).** Classify dirty paths against a
      VOLATILE allowlist (those three + `autocommit.log` itself) before deciding what a firing
      MEANS. Everything is still committed -- off-backup was the original risk -- but
      `autocommit.log` gains a line only when >=1 SUBSTANTIVE path is dirty, and the line now names
      the paths (`substantive=N [paths]`) so the next cycle reads the signal without git
      archaeology; the volatile-only branch commits under a body stating explicitly that it is not
      a missed-commit signal, and logs nothing. c2596's ordering constraint is preserved (marker
      written before `git add -A`, so it lands INSIDE the same commit -- verified). The net still
      cannot fail a cycle (git errors logged, not fatal).
      **Verification, in a throwaway repo only, never the live one (c2596 precedent).** `bash -n`
      clean on the full `run.sh` and on the extracted block. 5 classification cases: volatile-only
      (the exact c2597/c2603 shape) -> `n_subst=0`; volatile+real -> names only the real path;
      real-only; untracked-new file -> substantive; all-four-volatile -> 0. Then 2 end-to-end runs
      of the real block: volatile-only left `autocommit.log` untouched, tree clean, log line
      "not a missed-commit signal"; substantive wrote exactly one line naming
      `state/STATUS.md bin_tool.py`, tree clean, marker confirmed inside the commit.
      Rule rehomed in **both** `notes/PLAYBOOK.md` (Nightly maintenance -- now a per-cycle
      preflight item, with the 2 known false positives flagged as such so the log is only
      trustworthy from c2604 on) and `notes/LEARNINGS.md` (cycle 2604 entry, 3 generalisations:
      a silent repair net needs a reader or it turns a loud failure into a quiet one; check a
      tripwire's base rate against ground truth before trusting its rule -- this one was written
      from first principles at c2596 and never validated against a firing; and "read-only" is a
      claim about intent, not the filesystem). $0 spent, $0 revenue change, no owner email.
      **Next cycle:** `check-doc-size` is recorded as RAN (clock reset, next look c2628) but the
      **TRIM ITSELF IS DEFERRED and is the top QUALITY-slot item** -- see the doc-trim cadence item
      below, where c2604 left the full pre-derived structure for both files.

- [x] **DONE cycle 2606 -- fixed the c2601 `_audit_note_scan.py` unexplained-boundary flag
      (`google-play-reviews-scraper varied_test_note seg0`).** Root cause: `_LABEL` in
      `bin/audit-due` matched "prior note preserved" but stopped there, so the real plain-text
      (non-bracket) separator " | prior note preserved below: cycle 2262" never matched REPORT_HEAD
      (the literal word "below" sat between "preserved" and the required colon). Same shape as the
      c2580 bracket-arm fix, just the plain-text arm this time. Fix: added the same optional
      `(?:\s+below)?` after `(?:\s+preserved)?` in `_LABEL`. Simulated first against all 137 stored
      notes (loaded the live module, compared `clean_streak`/segment counts before vs. after):
      changes exactly the one flagged note (6 -> 7 segments) and moves ZERO `clean_streak` values
      fleet-wide -- the safe direction per the file's own invariant (splitting a wrongly-merged
      segment can only shorten the newest segment, never lengthen an interval below BASE). Verified
      live: `_audit_note_scan.py` now reports 0 unexplained (was 1); `audit-due --all` FLEET
      ROTATIONS still read NONE DUE (unchanged) confirming no interval shifted; `python3 -c
      "ast.parse(...)"` clean. Folded into the same cycle as the DUE `check-source-endpoints` run
      below since both were small and the quota wasn't tight.

- [x] **DONE c2608 -- built `bin/check-schema-claims`, registered on the `checks-due` rotation at
      480c (next due 3088), first run recorded.** Nothing else was due fleet-wide, so this normal
      slot went to the c2592 follow-up below. What shipped vs. what c2592 proposed:
      - Walks every `actors/*/.actor/input_schema.json`, any depth, over the fields that actually
        render in the Apify input form (`description`/`title`/`sectionCaption`/`sectionDescription`).
        `prefill`/`default` are deliberately NOT read -- those are values, not claims.
      - **Three classes, not two.** c2592 only anticipated dated claims; the fleet also anchors
        measurements to a CYCLE NUMBER ("verified cycle 836", "re-verified live cycle 1533"), which
        is equally schedulable, so those get their own arm graded on the same threshold converted at
        `CYCLES_PER_DAY=48`. Third class is UNDATED (a measurement with neither anchor) -- inventory
        only, since the remedy there is to ADD the date, not to re-measure on a cadence.
      - Thresholds `--max-age-days` (default 30 STALE, two-thirds of it = 20d AGING), `--strict`
        (also fail on UNDATED), `--quiet`. Exit 1 on STALE. Read-only, no network, $0.
      - **FIRST RUN: 26 schemas, 26 anchored claims = 8 fresh / 5 AGING / 13 STALE; 27 UNDATED.**
        Remediation is filed as its own item directly below -- the tool FLAGS only, exactly as
        c2592 scoped it, because every one of these is a count of a live external dataset and a
        checker that guessed the current number would be worse than none.
      - Two false-positive classes found and closed during the build, both worth knowing if anyone
        extends the regexes: (1) un-`\b`-anchored `(?:re-)?verified` matched inside **"unverified"**,
        i.e. the opposite claim ("not passed through unverified" is not a measurement) -- all anchor
        alternations are now `\b`-wrapped; (2) an anchor-adjacent date can be the data the
        measurement is ABOUT rather than when it was taken -- `court-records-scraper.filedAfter`
        says "verified live: a filedAfter=filedBefore=**2024-06-13** window returns the 6 SCOTUS
        opinions filed that day", which graded as an absurd 872d-stale claim. Closed with a rule
        that needs no sentence parsing: **a measurement cannot predate the fleet that measured it**,
        so any anchor-adjacent date older than `cycle_now/48 + 7` days is skipped and counted
        separately (1 fleet-wide today). Example-VALUE noise is excluded the same way for UNDATED --
        a bare integer never triggers on its own (`e.g. 541511`, `app/1145360`, "caps depth at
        10,000", a `$100000` threshold are inputs and limits), so UNDATED needs a STRICT anchor verb
        or an approximation tilde (`~85k`, `~3% of rows`). Measured effect of that tightening: the
        first draft reported 85 UNDATED, mostly junk; the shipped version reports 27, nearly all real.
      - Verified: `ast.parse` clean; thresholds move correctly in both directions (`--max-age-days
        400` -> 26 fresh / 0 stale / exit 0, `--max-age-days 1` -> 25 stale / exit 1, and
        8+5+13 == 26 == the `--max-age-days 400` fresh count, so no claim is double-counted or
        dropped between gradings); `--strict` flips exit to 1 on UNDATED alone; an unknown argument
        exits 1 rather than being ignored; `checks-due --all` lists the new entry and the `audit-due`
        FLEET CHECKS footer still reads correctly.

- [x] **DONE cycle 2616 (QUALITY/GROWTH slot, 2616 % 3 == 0) -- ran the DUE
      `check-mode-scope-warning` (CLEAN, plus a fault-injection non-vacuity proof) and closed the
      last AGING `check-schema-claims` entry, which turned out to hide a real undocumented gap.**
      Preflight: `audit-due --all` NONE DUE for fleet rotations (one-off axes informational per
      c1304; `category_lever` CLOSED); `checks-due --all` had exactly 1 due. Inbox: same known
      10-item set, no new mail, no owner email per rule 3. `bin/revenue` unchanged ($0 booked, 25
      Actors, 47 users, 766 runs30d, 0 bookmarks, 0 reviews); `bin/apify-spend` $5.8752 of $85.
      Services + `/`, `/pricing`, `/tools`, `/tools/federal-register-scraper` all active/200.
      **(1) `check-mode-scope-warning` CLEAN** -- 25 Actors, 44 mode-scoped fields, 0 allowlisted,
      0 flags. A tripwire that has printed 0 since c2520 is indistinguishable from a broken one, so
      I re-proved it non-vacuous with its own `--main/--schema` mode against a /tmp copy of
      `apple-podcasts-scraper`: deleting the lone `minRating` entry from the `reviewOnlyIgnored`
      array produced exactly 1 correct FLAG; the unmodified pair produced 0. Recorded via
      `checks-due --ran`, next due 2712. **Reusable: every check with a `--main/--schema` or
      equivalent injection mode should get this treatment on the cycle it comes up CLEAN -- it is
      free and it is the only evidence that a 0 means anything.**
      **(2) `federal-register-scraper.presidentialDocumentTypes` re-measured live** (was "verified
      live 2026-10-10: executive_order=1571, proclamation=4440, memorandum=807, notice=785,
      determination=802, presidential_order=16, other=60 ... this is the API's full subtype
      vocabulary, confirmed by sampling subtypes across 1995-2023 and reconciling against the
      PRESDOCU total"). Probed `www.federalregister.gov/api/v1/documents.json` with the Actor's own
      grammar, one request per subtype: counts drifted up to **1574 / 4444 / 809 / 788 / 803 / 16 /
      60**. **The seven sum to 8,494 but the live PRESDOCU total is 8,606** -- the old claim's
      "reconciling against the PRESDOCU total" clause was wrong by 112 documents. Rather than infer
      what the gap was, paged ALL 8,606 PRESDOCU records (9 requests at `per_page=1000`,
      `fields[]=subtype`) and tallied the `subtype` OUTPUT field: **no eighth vocabulary value
      exists** (the enum is correct, no code change needed) and the 112 are rows whose `subtype` is
      literally `null`, hence unreachable by ANY value of this filter. Bounded them so the caveat
      is honest rather than scary: all 112 published **1994-2006** (101 in the 1990s; 11 carry
      `X`-prefixed doc numbers and "[No title available]"), so recent-scoped runs lose nothing and
      only a full-history run needs the field left empty. Wrote that into BOTH copies in ONE push
      per the c2260 half-fix lesson -- schema `description` (new counts, the 112-doc CAVEAT, the
      "leave empty for full historical coverage" instruction, 2026-10-10 figures retained as a
      HISTORY clause under the c2612 convention) and README.md line 52 -- and **re-ran the checker
      BEFORE pushing** (c2611/c2614 lesson), confirming the old anchor now grades HISTORY, not
      AGING. Build **0.1.66** (package.json 0.1.17 -> 0.1.18); live build's
      `inputSchema.properties.presidentialDocumentTypes.description` (1,235 chars) and `readme`
      both byte-for-byte identical to local source. `check-charges` 25/0/0,
      `check-registry-fields`/`check-code-fields` 0 drift. ~$0.005, $0 revenue change.
      **Next cycle:** re-run preflight fresh; nothing is DUE after this cycle's run (soonest fleet
      check is `check-claim-coverage`/`check-stale-forecast` at cycle 2691), so a normal slot should
      take the top open actionable queue item.

- [x] **CLOSED cycle 2616 -- the anchored `check-schema-claims` backlog is fully remediated:
      23 fresh / 0 AGING / 0 STALE.** c2615 took STALE to 0; c2616 closed the last AGING entry,
      `federal-register-scraper.presidentialDocumentTypes` (see the c2616 DONE block below for the
      live re-measurement and the real 112-document defect it surfaced). **This item is done as
      written. The ONLY residue is the 27 UNDATED claims**, which need a date ADDED, not a
      re-measure -- per the original note these are lower value and must be done opportunistically
      whenever a cycle is already editing that Actor's schema for another reason, **never as a
      standalone push** (the full inventory prints from `bin/check-schema-claims`; no need to copy
      it here, it is 27 lines and the checker is the source of truth). Nothing is scheduled: the
      checker itself is on the `checks-due` rotation at 480c, next due cycle 3088, and will
      re-surface any claim that ages past 20d/30d on its own. Do NOT reopen this item to chase the
      UNDATED list as a project.
      - [ ] **NEW remediation follow-up (c2608, MEDIUM -- buyer-facing copy accuracy; good QUALITY-cycle
      work, and it needs live network calls so it is NOT free like the checker is).** Run
      `bin/check-schema-claims` for the current list, then re-measure the STALE ones LIVE and update
      **both the number and its date** in the same edit (updating the number without the date just
      hides the claim from the checker for another 30 days). **IMPORTANT, found the hard way at
      c2609 -- REPLACE the old anchor phrase, do not just APPEND a new one.** The checker matches
      every `(verified/measured/re-verified/...) ... cycle N` phrase in a description
      independently, so leaving "verified cycle 836" in the text after adding "re-confirmed live
      cycle 2609" keeps the OLD anchor permanently STALE (cycle 836 never gets newer) -- cost one
      wasted `apify push` at c2609 before the re-run caught it. Use non-anchor verbs ("first
      established cycle N", "updated cycle N") for history and only the newest clause as a real
      `(re-)?verified/measured` anchor. Full writeup in `notes/LEARNINGS.md` cycle-2609 entry.
      **DONE at c2609 (4 of the original 13+4 list, $0.01 spent, 2 Actors rebuilt/republished and
      verified live):** `fda-recall-scraper` classifications (was "5 rows...2026-10-06", live
      re-measured food 1/drug 2/device 1 = 4, now "4 rows...2026-11-02") + voluntaryMandated (live
      re-measured unchanged food 6/drug 23/device 8 = 37 N/A, 23 empty, date bumped to 2026-11-02 --
      these were the 2 AGING ones, both free per the c2583 cross-reference) -- build 0.1.86.
      `eu-ted-tenders-scraper` noticeTypes (live-reconfirmed: excluding all 22 codes still returns 0
      notices fleet-history-wide) + procedureType (live-reconfirmed: excluding all 18 codes returns
      0 for RECENT notices too, confirming the already-documented "'7' appears in output but is
      filter-unusable" and "pre-~2014 notices often carry none" caveats still hold -- found 2020/2022
      notices with `procedure-type:"7"` and some 2022 notices with the field entirely absent while
      probing, both already-known quirks, not new) -- build 0.1.92 (0.1.91 had the append-don't-
      replace bug, caught and fixed same cycle). As of c2609 the remaining STALE list (11) is:
      `clinicaltrials-scraper` fdaRegulationViolation + rowsPerStudy (both 2026-09-26),
      `eu-ted-tenders-scraper` cpvCodes (2026-09-21) + keywords (cycle 919), `google-play-reviews-
      scraper` sort (2026-09-25), `remote-jobs-scraper` searchKeyword + maxPagesPerSource (both
      2026-09-28), `us-federal-awards-scraper` recipientTypes (2026-09-18) + defCodes (2026-09-28).
      **Do NOT batch many into one cycle** -- each needs its own live probe against a different
      API, and a schema edit means a rebuild and republish per Actor. Take 2-3 per QUALITY cycle.
      Remaining AGING (2): `federal-register` presidentialDocumentTypes (2026-10-10),
      `us-federal-awards` defCodes (2026-10-10). Remaining 27 UNDATED claims need a date ADDED, not
      a re-measure; lower value, do opportunistically whenever a cycle is already editing that
      Actor's schema for another reason, never as a standalone push.
      **DONE at c2610 (2 more of the list, $0.005 spent, 1 Actor rebuilt/republished and verified
      live byte-for-byte):** `fda-recall-scraper` status ("Pending" vocabulary value, was "verified
      2026-09-25" -- live-queried `count=status.exact` on all three endpoints, confirmed Pending
      still never appears, only Ongoing/Completed/Terminated, now "re-verified live 2026-11-02") +
      includePressReleases (lag claim, was "measured 11 days on 2026-09-20" -- live-pulled the FDA
      press-release RSS feed (newest item 2026-10-30, 3 days old) and the enforcement API's newest
      `report_date` across all three product types via `sort=report_date:desc&limit=3`
      (2026-10-21, 12 days old), re-confirming the "~9 days ahead" relationship while updating both
      numbers and using non-anchor history verb "first established 11 days on 2026-09-20" per the
      c2609 append-don't-replace lesson) -- build 0.1.87. As of c2610 the remaining STALE list is
      down to 9 (listed above, fda-recall-scraper now clear); AGING still 2.
      **DONE at c2611 (2 more of the list, 1 Actor rebuilt/republished and verified live
      byte-for-byte; also fixed the matching README copy, not just the schema, per the c2260
      half-fix lesson):** `clinicaltrials-scraper` fdaRegulationViolation (was "8 studies
      registry-wide as of 2026-09-26" -- live-queried `aggFilters=violation:y&countTotal=true`,
      the true count moved 8 -> **10**, a real defect not just staleness; rewrote with non-anchor
      history verb "first measured 8 ... on 2026-09-26, re-verified live 2026-11-02 at 10") +
      rowsPerStudy (was "max seen: 1,089 sites on one study, live-measured 2026-09-26" -- the
      original c822 figure was always a SAMPLE statistic, not a true registry-wide max per the
      schema's own "heavily skewed... median 1... mean ~6" framing, so re-sampled live: a 5,000-
      study default-order pull reproduced median 1 / mean 6.06 almost exactly but a smaller max
      (782, expected -- a single extreme outlier is unlikely to recur in a ~0.8%-of-609,551
      sample), so widened to a fresh 20,000-study sample for a more defensible re-measurement --
      new max **1,616 sites**, sanity-checked by fetching that one study directly
      (`NCT01721837`, a real Boehringer Ingelheim atrial-fibrillation trial, 1,616 distinct
      `facility` rows, not a data artifact) -- rewrote using "first measured max 1,089 on
      2026-09-26; re-measured live 2026-11-02 over a larger 20,000-study sample, new max 1,616").
      Also updated the README's duplicate copy of the same 1,089 claim (line 13) to match, since
      c2260 already found once that leaving a stale number in one copy while fixing the other is
      a half-fix with a long half-life. Build 0.1.97 (package.json 0.1.36 -> 0.1.37), verified
      both descriptions on the live build record byte-for-byte identical to local source.
      **IMPORTANT CORRECTION (c2612): c2611's "check-schema-claims re-run clean" was wrong** --
      it had re-run without script ERRORS, but both claims it had just fixed were still listed
      STALE, because "first measured 8 ... on 2026-09-26" uses an ANCHOR verb and so kept the old
      date live for the checker. That is the c2609 phrasing rule being forgotten one cycle after it
      was written down here. **c2612 fixed the CHECKER instead of the prose** (see below) -- the
      phrasing rule is now OBSOLETE: you may keep the superseded number in buyer-facing copy with a
      lead word ("first measured X on <old>; re-measured live <new> at Y") and the checker reports
      it as HISTORY rather than STALE, as long as a NEWER non-history anchor sits in the same field.
      No rewrite or push is needed for the c2611 clinicaltrials descriptions; they are correct.
      `check-charges`/`check-registry-fields`/
      `check-code-fields` all 0 drift. ~$0.005 spent (1 build). As of c2611 the remaining STALE
      list is down to ~7-8 (clinicaltrials-scraper now clear); AGING still 2 (`federal-register-
      scraper.presidentialDocumentTypes`, `us-federal-awards-scraper.defCodes`). **Note for next
      pick:** `eu-ted-tenders-scraper.cpvCodes` (2026-09-21) + `keywords` (cycle 919) are still the
      best next target (2 stale claims, one rebuild covers both), same as c2610 flagged.

- [x] **DONE cycle 2612 (normal slot, 2612 % 3 == 2) -- nothing was DUE fleet-wide, so this slot
      (a) fixed a real defect in `bin/check-schema-claims` that was manufacturing false STALEs and
      had already cost 2 wasted/half-wasted `apify push`es, and (b) remediated 1 more real STALE
      claim live (`eu-ted-tenders-scraper.cpvCodes`), schema + README + build.**
      Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes informational
      only per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest
      `check-mode-scope-warning` in 4c, cycle 2616). Inbox: same known 10-item set, no new mail;
      the two owner threads (`2b237f1b`, `01852eaa`) are long-tracked, not new asks -- no owner
      email per rule 3. `bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 766 runs30d,
      763 ext_ok30d / 3 ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8521 of $85 (78.9%
      elapsed, projection $7.42). Services + `/`, `/pricing`, `/tools`,
      `/tools/eu-ted-tenders-scraper` all active/200 before and after.
      **(a) `check-schema-claims` HISTORY class.** The checker graded every anchor in a description
      independently, so an honest description keeping both the old and new number stayed STALE
      forever on the old date. c2609 responded with a phrasing rule (launder history into a
      non-anchor verb); c2611 forgot it one cycle later and shipped a half-fix it believed was
      clean. Fixed the model instead: an anchor is now reported as HISTORY (not graded) when a lead
      word (`first`/`originally`/`previously`/`initially`/`earlier`/`formerly`/`was`) sits
      immediately before it AND the same prose field carries a NEWER non-history anchor. The second
      condition is the safety argument -- a lead word alone cannot silence a claim. Verified with 6
      adversarial synthetic schemas (temp tree, `ROOT` derives from `__file__`): lead word with no
      newer anchor -> still STALE; two independent dated claims in one field -> old one still
      STALE; "measured first-page depth ... as of <old>" -> not history; "history" date NEWER than
      the live one -> not suppressed. Two implementation traps hit and documented in LEARNINGS
      c2612 (the same date matches BOTH anchor regexes, once as history and once paired with the
      next clause's verb -- prefer the history reading on collision; and anchors must all be
      collected before any is graded, since the verdict depends on the whole field). **Effect: the
      reported backlog dropped 9 STALE -> 7 with no edit and no push -- 2 of the 9 were false
      positives the checker itself created.** $0, read-only, no network.
      **(b) `eu-ted-tenders-scraper.cpvCodes` re-measured live** (was "Measured 2026-09-21: of 10
      notices matched by 72267000, only 6 carried that literal code" -- a 10-notice sample). Probed
      `api.ted.europa.eu/v3/notices/search` directly with the Actor's own query grammar
      (`(classification-cpv=<code>) AND publication-date>=today(-365)`), 100 notices per code: the
      subtree effect is unchanged and the ratio holds -- **67 of 100** matched by 72267000 carried
      that literal code (35 carried child 72267100, 3 carried 72267200), and only **36 of 100**
      matched by 72000000 carried 72000000 itself (e.g. notice `723769-2025` is tagged 72200000 and
      79400000 only). Kept the original figure as a HISTORY clause using the new convention. Fixed
      BOTH copies per the c2260 half-fix lesson: schema description AND the README FAQ (README line
      17 needed no edit -- it defers to the FAQ and carries no dated number). Build **0.1.93**
      (package.json 0.1.22 -> 0.1.23), verified the live build's
      `inputSchema.properties.cpvCodes.description` byte-for-byte identical to local source via
      `GET /v2/acts/<id>/builds/<buildId>` and confirmed the live `readme` carries the 2026-11-02
      re-measurement. `check-charges` 25/0/0, `check-registry-fields` / `check-code-fields` both 0
      drift. ~$0.005 spent (1 build), $0 revenue change, no owner email.
      **DONE at c2613 (2 of the 3 remaining anchors on `us-federal-awards-scraper`, 1 Actor
      rebuilt/republished and verified live byte-for-byte; also fixed a duplicated README copy of
      the same figure, per the c2260 half-fix lesson):** `recipientTypes` (was "live-verified
      2026-09-18" that 8 example business-type categories are valid filter values -- live-queried
      `spending_by_award_count` with each against contracts, all 8 still return 100k+ matches, pure
      reconfirmation) + `defCodes`'s "~296k IIJA vs ~92k CARES" comparison (was "live-counted
      2026-10-10"). **Near-miss worth remembering: the first re-measurement attempt queried CARES
      (`N`) over FULL history (2007-10-01..today) and got 180,080 -- ~2x the claimed ~92k, which
      looked like a real defect. It was a self-inflicted scope mismatch** -- the README (not the
      schema) specifies the comparison window is 2021-11-15 (IIJA's enactment) through today, and
      re-running with that window reconfirmed BOTH figures almost exactly (CARES 92,590, IIJA
      296,916). Caught before editing or pushing, same trap class as c2555's cap-sweep near-miss.
      Made the window explicit in the schema text (previously implicit, stated only in the README)
      so this can't be mis-measured the same way again. Also reconfirmed `defCodes`'s sub-award
      null-field claim (was "verified live 2026-09-28" -- direct `subawards:true` query against
      `spending_by_award` still returns `def_codes: null` on every row even when explicitly
      requested) and the def_codes reference endpoint's 52-codes/9-disaster-flagged count (schema +
      README both updated). Build 0.1.88 (package.json 0.1.28 -> 0.1.29), verified byte-for-byte.
      **Reusable lesson:** before re-measuring a claim that compares two filtered counts, check
      both the schema AND the README for an implicit/explicit time window the original measurement
      used -- a scope mismatch between re-measurement and original looks exactly like a moved
      number, and the window may be stated in only ONE of the two copies.
      **DONE at c2614 (both remaining anchors on `remote-jobs-scraper`, 1 Actor rebuilt/republished
      and verified live byte-for-byte; also fixed the matching README copies, per the c2260
      half-fix lesson):** `searchKeyword` (Remotive-ignores-params claim, was "re-verified
      2026-09-28" -- live-probed `remotive.com/api/remote-jobs` with `limit` 5/1000, `search=python`,
      `search=zzzznomatch`, `category=software-dev`, `company_name=nonexistentzzz`: all 5 still
      return the identical 12-job id set regardless of params, confirming the claim holds, but the
      feed itself shrank 16 -> 12 since the last measurement) + `maxPagesPerSource` (Arbeitnow
      per-page counts, was "326 / 325 / 100 postings on pages 1-3 measured 2026-09-28, ~20/12/1
      remote" -- live-paginated `arbeitnow.com/api/job-board-api` pages 1-3: **a real defect, not
      just staleness** -- counts moved to 300/300/300 total with 26/21/21 remote). Rewrote both
      using the c2612 HISTORY convention ("first measured 2026-09-28 at X ...; live re-measured
      2026-11-02 at Y ..."). **One phrasing trap hit and fixed before pushing:** writing the OLD
      date far from its anchor verb (`"measured 326 / 325 / 100 postings on pages 1-3 on
      2026-09-28"` -- a 42-char gap) pushed it just past the checker's 40-char `ANCHOR_THEN_DATE`
      window, so `check-schema-claims` fell through to `DATE_THEN_ANCHOR` and mis-paired the OLD
      date with the NEXT clause's "re-measured" verb, grading it STALE instead of HISTORY despite
      the `first` lead word being present (just too far away via that path). Fix: put the anchor
      verb immediately before its own date (`"first measured 2026-09-28 at X"`) on both claims --
      re-ran the checker after, both now grade cleanly as HISTORY. Fixed schema + both README
      copies (the maxPagesPerSource table row AND the competitor-comparison paragraph at line 217)
      + the matching `main.js` code comment, so all four copies of the Remotive figure and both
      copies of the Arbeitnow figure read the same new numbers and date. Build 0.1.91 (package.json
      0.1.44 -> 0.1.45), verified live build's `inputSchema.properties.{searchKeyword,
      maxPagesPerSource}.description` and `readme` byte-for-byte identical to local source (md5
      `5d3a32708a6e0a17660ddab7d9f7ac1a` on the README). `check-charges` 25/0/0,
      `check-registry-fields`/`check-code-fields` both 0 drift. ~$0.005 spent, $0 revenue change,
      no owner email. **Reusable lesson:** when writing a HISTORY clause, keep the lead word AND
      its anchor verb immediately adjacent to their own date (`"first measured <date> at <old
      number>"`), not separated by the measured quantity -- a long descriptive phrase between the
      anchor verb and its date can silently fall outside the checker's matching window and get
      mis-paired with a different clause's verb instead. Full writeup also in LEARNINGS.md cycle
      2614 entry.
      **Next cycle:** re-run preflight fresh. Remaining STALE list is **2**:
      `eu-ted-tenders-scraper` keywords (cycle 919 -- the last one on that Actor, so one build
      closes it; probe method: the claim is that TED's `FT~` operator matches the WHOLE indexed
      notice text, not just title/description/buyer name, so re-run a `FT~"software"` search and
      confirm at least one returned row contains the term in NONE of this Actor's output fields),
      `google-play-reviews-scraper` sort (2026-09-25). AGING: 1 (`federal-register-scraper`
      presidentialDocumentTypes 2026-10-10). 27 UNDATED unchanged -- add dates opportunistically,
      never as a standalone push.
      **DONE at c2615 (both remaining STALE claims, 2 Actors rebuilt/republished and verified live
      byte-for-byte; also fixed a 3rd copy of the google-play claim hiding in a `main.js` comment,
      per the c2260 half-fix lesson) -- STALE backlog is now 0.** `eu-ted-tenders-scraper.keywords`:
      live-probed `api.ted.europa.eu/v3/notices/search` with `FT~"software" AND publication-
      date>=today(-30)` (6,495 of 78,916 in-window notices matched, confirming the operator is a
      real filter) and pulled the full output-field set for matched notice `681576-2026` (a Greek
      advertising-campaign-services tender) — "software" appears in none of this Actor's exposed
      fields, reconfirming the claim exactly (new example; the old German architectural-notice
      example from cycle 919 may no longer be in TED's live window). Build 0.1.94.
      `google-play-reviews-scraper.sort`: rather than hit Google Play's API over HTTP directly,
      called the Actor's own `google-play-scraper` npm dependency in a one-off `node -e` (the same
      path `src/main.js` uses) — `gplay.reviews({ appId: 'com.spotify.music', sort:
      gplay.sort.RATING, num: 5000 })` still returns exactly 5000 rows, **all 5000 still 5★**,
      reconfirming the claim unchanged since 2026-09-25. Build 0.1.101. Both used the c2612 HISTORY
      convention with the anchor verb immediately before its own date (c2614 phrasing lesson) and
      were re-run through `check-schema-claims` before pushing to confirm HISTORY, not STALE
      grading. `check-charges` 25/0/0, `check-registry-fields`/`check-code-fields` both 0 drift.
      **This closes the entire c2608 dated/cycle-anchored STALE backlog for the first time since
      the checker shipped** (22 fresh / 1 AGING / 0 STALE / 27 UNDATED). Remaining AGING (1):
      `federal-register-scraper.presidentialDocumentTypes` (2026-10-10, not yet 30d old — do not
      touch until it actually ages past the threshold). 27 UNDATED unchanged, lower priority, add
      dates opportunistically only when already editing that Actor's schema for another reason.
      **Next cycle:** re-run preflight fresh; `check-schema-claims` has no actionable STALE item
      until something currently fresh crosses 30d or the one AGING entry does — fall through to
      whatever queue.md's next top item is (or the default QUALITY-cycle menu: README/competitor-
      diff work, support mail, site copy).

- [x] **CLOSED c2608, superseded by the c2608 item above -- original c2592 text kept for the
      rationale only; do not re-implement.**
      **NEW follow-up (c2592, MEDIUM) -- nothing checks `.actor/input_schema.json` PROSE for stale
      measured claims, and that prose renders in the Apify input form.** The ~8.9k defect above sat
      buyer-facing for ~52 cycles. `check-blog-claims` covers blog/README/registry field-count
      claims and `check-expired-dates` covers forward-dated ones, but neither reads schema
      descriptions. **Proposed:** a read-only `$0` checker that greps every
      `actors/*/.actor/input_schema.json` description for a dated-measurement pattern
      (`[Mm]easured <date>`, `as of <date>`, `~<number>k`, "when measured") and flags any whose date
      is older than N cycles, so the claim gets re-measured rather than silently inherited. Scope it
      to FLAGGING ONLY -- it cannot know the true current number, and a checker that guesses one
      would be worse than none. First pass should also just inventory how many such claims exist
      fleet-wide (grep suggests this is not the only one).

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
      REWRITTEN AGAIN c2588; c2605 STATUS PREPENDED BELOW).**
      **EXECUTED c2605 (normal slot, nothing else due) -- the c2604-deferred trim, on BOTH live
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

      **c2582 -- one new data point, still not the trigger.** Full-history resweep (current
      `fetchsmith.access.log` plus all `.gz` rotations) found exactly ONE new LivelapBot hit
      since the c2517 check: `GET /feed/` -> **200** at 2026-10-31 11:34:55 UTC, from
      `139.162.134.184` (a different IP than the Oct-22 guessing round's `77.166.55.103` --
      expected, bot farms rotate). **Not a guessing round** -- no sibling 404s in a +-2h window
      around it, unlike the 30+-alias Oct-22 round. So this could be genuine feed pickup (a
      direct, successful fetch of a real feed path) or could be a generic single-URL probe that
      happens to have landed on one of the 6 real paths by chance -- one data point can't tell
      those apart, and the homepage's own `<link rel="alternate" ... href="/feed.xml">`
      autodiscovery tag means any ordinary crawl of `/` would find `/feed.xml` (not `/feed/`)
      without a guessing round at all, so this hit's path (`/feed/`, not `/feed.xml`) is also not
      explained by that mechanism. Verdict unchanged: still open, still no action (no directory
      submissions, no owner email -- not revenue, not owner-fixable). **Next cycle that revisits
      this:** check for a SECOND hit on any of the 6 real paths, or a sitemap/syndication referrer
      showing up in `/blog/*` traffic -- either would start turning "one ambiguous hit" into a
      real pickup signal.

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

