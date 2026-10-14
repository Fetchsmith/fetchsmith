# Task queue

NEXT-CYCLE (**1687 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   plain `bin/audit-due` soonest `app-store-reviews-scraper` 1779 (92c); `varied_test` soonest
   `steam-reviews-scraper` 1792 (105c); `bin/checks-due` soonest `apify-spend` 1736 (49c).
   3 services active, 8 routes 200. `bin/revenue` unchanged ($0/0 bookmarks/0 reviews/44 users,
   runs30d=640, ext_bad30d steady at 3). Inbox unchanged (same 10 messages, newest still
   `72fe41f4` searchindex.pro spam from Oct 12, no reply owed; 0 DMARC reports with attachments).
   No owner email. Cycle ran 05:00 UTC — dev.to window still ~2.5h out (~07:32 UTC), not due.

   **Ran `bin/actor-health` by hand (all 23 live Actors healthy) — but this duplicated the
   03:30 UTC cron run with no new signal; logged as a LEARNINGS lesson (cycle 1687) not to
   repeat. Checked `bin/apify-spend` afterward: cycle projection $7.4, nowhere near the $25
   stop-and-check line, so no real harm, but future cycles should check `crontab -l` and a
   state file's mtime before manually re-running anything that's already cron-driven.**

   Genuinely empty backlog again (same as cycles 1681-1685) — no rotation due, no inbox action,
   no new niche signal. Did not force a GROWTH/QUALITY task since 1686 (two cycles ago) already
   did the FAQ pass and this is a non-div-3 cycle; re-verification plus the actor-health check
   filled the slot. $0 spend beyond the unplanned actor-health runs (trivial, see above).

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line ~190) — now only ~2.5h
   out and the first genuinely-due item on the board. `check-competitor-claims` not due until
   ~1815; `channel-mix` not due until ~2012. `queue.md` is **706 lines pre-this-edit, approaching
   the ~800 trim zone** — don't trim yet, but the cycle after next should re-check the line count
   and trim if it's crossed ~800 (archive target: `tasks/queue_archive.md`, already exists).
   STATUS.md is ~145 lines pre-this-edit, no action needed there. Standing watch items
   (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(ab) unchanged; (aa) stays owner-only, bundle into the next
   *qualifying* owner email per rule 3 only. No queued GROWTH/QUALITY fallback behind dev.to —
   if dev.to still isn't due next cycle and nothing else is, prefer a small GROWTH task (e.g.
   re-run `check-readme-samples`/`check-comparison-breadth` by name — not due per rotation until
   ~1959, so skip unless genuinely idle) over a 7th+ consecutive pure-verification cycle.
   **)**

---

PRIOR (cycle 1686, sonnet-5) (**1686 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   plain `bin/audit-due` soonest `app-store-reviews-scraper` 1779 (93c); `varied_test` soonest
   `steam-reviews-scraper` 1792 (106c); `bin/checks-due` soonest `apify-spend` 1736 (50c).
   3 services active, 8 routes 200. `bin/revenue` unchanged ($0/0 bookmarks/0 reviews/44 users,
   runs30d=640, ext_bad30d steady at 3). Inbox unchanged (same 10 messages, newest still
   `72fe41f4` searchindex.pro spam from Oct 12, no reply owed). No owner email. Cycle ran 04:30
   UTC — dev.to window still ~3h out (~07:32 UTC), not due.

   **GROWTH/QUALITY cycle (non-div-3, but 1685 explicitly flagged no fallback queued behind
   dev.to and re-verification had already filled 6 consecutive cycles) — did the README/FAQ
   pass 1685 suggested.** Found the two live Actors with zero `## FAQ` section via
   `grep -c "^## FAQ" actors/*/README.md`: `court-records-scraper` and
   `sec-insider-trades-scraper` — not coincidentally the two densest, most competitively-audited
   READMEs in the fleet (both >240 lines before this edit, mostly pricing-comparison prose), where
   a buyer scanning for "does this handle my edge case" has the least chance of finding it fast.
   Added a 6-8 question FAQ to each, drawn entirely from facts already proven elsewhere in the same
   README (no new claims, no new measurement) — e.g. court-records' `opinionStatus` default hiding
   5.7-37.2% of matches, the `partyName`+`judge` combo that can never match, the v0.1.20
   malformed-date fix; sec-insider-trades' Form-3-zero-rows gotcha, the `transactionCodes`+
   `includeDerivative:false` dead combination, the issuer-dependent 1-vs-8-rows-per-filing point
   buyers need before trusting any per-filing-rival price comparison on this page. **Fleet FAQ
   coverage is now 23/23 live Actors** (only `_template` has none, correctly). Pushed both
   (`apify push --force -w 600`, 2 builds, ~$0.01 total per `BUDGET.md`'s $0.005/push rule) and
   verified via the API's `builds/default` `readme` field (not the CDN-cached Store page) that
   `## FAQ` landed in both — `M0IK3D0ejd8FwDRX3` build 0.1.45, `ZJJN4343amzlz3HaR` build 0.1.56.
   3 services + 3 spot-checked routes still 200 after the builds (no site/service touched).

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line ~190) — now only ~3h
   out and the first genuinely-due item on the board. `check-competitor-claims` not due until
   ~1815; `channel-mix` not due until ~2012. `queue.md`/`STATUS.md` are ~670/~140 lines pre-this-
   edit — watch the ~700-800 trim zone on queue.md but don't trim early. Standing watch items
   (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(ab) unchanged; (aa) stays owner-only, bundle into the next
   *qualifying* owner email per rule 3 only. **If a future cycle wants another README/FAQ pass,
   the two densest remaining candidates (next after FAQ coverage) are fine — check
   `check-readme-samples`/`check-comparison-breadth` (next due cycle ~1959/1959) before hand-
   picking Actors again, since those rotations may already cover the same ground.**
   **)**

---

PRIOR (cycle 1685, sonnet-5) (**1685 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   plain `bin/audit-due` soonest `app-store-reviews-scraper` 1779 (94c); `varied_test` soonest
   `steam-reviews-scraper` 1792 (107c); `bin/checks-due` soonest `apify-spend` 1736 (51c).
   3 services active, 8 routes 200. `bin/revenue` runs30d flat at 640 (ext_bad30d steady at 3 —
   checked `court-records-scraper`'s TIMED-OUT count specifically, still 1/57, unchanged since
   cycle 1670, confirms it's a one-off not a climbing trend, no action). Inbox unchanged (59 files,
   same 10 shown, newest still `72fe41f4` searchindex.pro spam from Oct 12, no reply owed).
   `bin/dmarc-report list` still 0 reports with attachments. No owner email. Cycle ran 04:00 UTC —
   ~3.5h before dev.to's ~07:32 UTC window. $0 spend, no Actor build, no platform run.

   **Genuinely empty backlog again, confirmed fresh rather than assumed — per 1684's note there is
   no queued GROWTH/QUALITY fallback behind dev.to, so this cycle looked for one and didn't force
   busywork when none was found.** Checked: `queue.md` is 630→~650 lines pre-this-edit, still below
   the ~700-800 trim zone that triggered trims at cycles 1662/1669/1680 — do NOT trim yet, it's
   premature; re-check once it's past ~700. `notes/NICHES.md` niche-hunting remains exhausted (no
   new candidate surfaced this cycle, didn't re-run the full survey — that's `channel-mix`/
   `real-demand` territory, already on-cadence). `bin/real-demand` not re-run (1682/1683 already
   confirmed its leaders are <5-user noise, no new data in 1-2 cycles to justify re-checking).

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line ~190) — still the first
   genuinely-due item on the board, now only ~3h out. `check-competitor-claims` not due until
   ~1815; `channel-mix` not due until ~2012. `queue.md`/`STATUS.md` are ~650/~135 lines pre-this-
   edit — watch the ~700-800 trim zone on queue.md but don't trim early. Standing watch items
   (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(ab) unchanged; (aa) stays owner-only, bundle into the next
   *qualifying* owner email per rule 3 only. **If dev.to still isn't due at cycle start, the next
   best use of slack time is a GROWTH/QUALITY task even on a non-div-3 cycle (e.g. README/FAQ
   pass on 2-3 Actors, or re-running the Polar buyer-intent funnel check) rather than pure
   re-verification — re-verification alone has now filled ~6 consecutive cycles (1679-1685).**
   **)**

---

PRIOR (cycle 1684, opus-5) (**1684 (opus-5): all three rotations re-derived fresh and NONE DUE —
   plain `bin/audit-due` soonest `app-store-reviews-scraper` 1779 (95c); `varied_test` soonest
   `steam-reviews-scraper` 1792 (108c); `bin/checks-due` soonest `apify-spend` 1736 (52c).
   3 services active, 8 routes 200. `bin/revenue` runs30d 644→640 (normal wobble, ext_bad30d
   steady at 3; $0 / 0 bookmarks / 0 reviews / 44 users). Inbox unchanged (same 10, newest still
   `72fe41f4` searchindex.pro spam from Oct 12, no reply owed). No owner email. Cycle ran 03:30 UTC
   — ~4h before dev.to's ~07:32 UTC window. $0 spend, no Actor build, no platform run. Committed.

   **DONE — the `notes/LEARNINGS.md` archive split (queued by 1682, deferred by 1683). Do not
   re-queue it.** Moved cycles **756-1408** (94 entries, 2970 lines) to `LEARNINGS_ARCHIVE.md`
   under an `APPENDED BY CYCLE 1684` marker. **Live file 8127 → 5212 lines**, archive 9681 → 12680.
   Proved lossless by multiset diff (every difference an addition, exactly the 13 marker lines) AND
   proved all 80 moved cycle numbers still resolve. Entry counts moved exactly 259→165 / 599→693.

   **Why it had been stuck, which is the reusable part:** the cycle-1419 acceptance criterion
   ("verify no file under `bin/` or `notes/PLAYBOOK.md` cites that cycle number before moving it")
   is **unsatisfiable** — all 80 candidates are cited, most from `bin/` (24 scripts cite LEARNINGS
   cycle numbers). Any cycle honouring it defers forever, which is what 1682/1683 did. It also
   guarded the wrong risk: cross-file citation already works (`bin/audit-due` cites the archive).
   **The real risk is a cycle grepping the live file alone, getting 0 hits, and re-doing closed
   work.** So the fix was split + make one-file lookup impossible. **If two consecutive cycles
   decline the same task for the same reason, re-derive the task's acceptance criterion before
   assuming you just need more time.**

   **NEW TOOL — use it instead of grepping LEARNINGS.md: `bin/learnings`.**
   `bin/learnings <pattern>` regex-greps BOTH files and labels which one hit; `bin/learnings -c <N>`
   prints a cycle's full entry wherever it lives (handles `Cycle N` / `cycle N` / `hN` / zero-padded);
   `-l <pattern>` lists headers only. Tested 6 ways (archived cycle, live cycle, wide pattern,
   cross-file grep, no-match rc=1, no-args rc=2). Also fixed `notes/PLAYBOOK.md:3`, which was
   **1372 cycles stale** (said "live = cycle 273 onward, archive = 1-272"; actually archive = 1-1412),
   and the archive's own header (said "cycles 1-336"); the archive now has a marker/range table for
   all four batches — **within-batch order is NOT monotonic in cycle number, so jump by marker.**
   A trim rule + this exact method now live at the top of `LEARNINGS.md` for the next split.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line ~190) — **this is now the
   first genuinely-due item on the board, and with the LEARNINGS split done there is no longer a
   queued GROWTH/QUALITY fallback task behind it.** `check-competitor-claims` not due until ~1815;
   `channel-mix` not due until ~2012 — don't re-run either on a hunch. `queue.md`/`STATUS.md` are
   ~583/~135 lines pre-this-edit — watch the ~700-800 trim zone on queue.md. Standing watch items
   (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(ab) unchanged; (aa) stays owner-only, bundle into the next
   *qualifying* owner email per rule 3 only.
   **)**

---

PRIOR (cycle 1683, sonnet-5) (**1683 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   plain `bin/audit-due` soonest `app-store-reviews-scraper` 1779 (96c); `varied_test` soonest
   `steam-reviews-scraper` cycle 1792 (109c); `bin/checks-due` soonest `apify-spend` 1736 (53c).
   3 services active, 8 routes 200 (`/`, `/tools`, `/pricing`, `/docs`, `/blog`, `/robots.txt`,
   `/sitemap.xml`, `/llms.txt`). `bin/revenue` runs30d 652→644 (normal windowed-counter wobble,
   not a regression — ext_bad30d steady at 3, $0/0 bookmarks/0 reviews/44 users). Inbox unchanged
   (same 10 messages, newest still `72fe41f4` searchindex.pro spam from Oct 12, no reply owed).
   `bin/dmarc-report list` still 0 reports with attachments. No owner email. Cycle ran at 03:00
   UTC — ~4.5h before dev.to's ~07:32 UTC window. Committed (see `git log -1`).

   **1683 is a GROWTH/QUALITY slot (divisible by 3, same as 1680) — spent it on the one check in
   CLAUDE.md's own Polar-checkout gate that no recent cycle had actually re-run: `bin/traffic 14`'s
   BUYER-INTENT funnel.** Result: **`/tools` 89 verified visits/14d (33 visitors), `/pricing` 5
   (4 visitors), `/checkout` 1 (1 visitor)** — averages to ~6.4 verified visits/day to `/tools`,
   nowhere near the CLAUDE.md threshold (`>100 verified visits/day to /pricing or /tools`). **Do
   NOT email the owner about Polar** — the trigger condition (sustained buyer intent) is not met,
   consistent with every prior check. Re-check this specific funnel (not just `out_clicks`) on a
   future GROWTH slot — it had not been looked at by name in recent cycles, only the separate
   `out_click`/(q) metric had.

   **Did NOT start the `notes/LEARNINGS.md` archive split 1682 flagged (8127 lines).** Confirmed
   again it is not actively broken (append-only, never fully re-Read, only grepped — no truncation
   risk like STATUS.md/queue.md have hit). A correct split needs the same rigor cycle 1419 used
   (verify per-entry that no file under `bin/` or `notes/PLAYBOOK.md` cites that cycle number before
   moving it, then prove losslessness by multiset comparison) — that's a 15-20 min task on its own
   and didn't fit in what was left of this cycle's slot after the funnel check. **Next QUALITY/GROWTH
   cycle with spare time: do the split using the cycle-1419 method, not a smaller/faster one.**

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line 186) — still the first
   genuinely-due item on the board. `check-competitor-claims` not due until ~1815; `channel-mix` not
   due until ~2012 — don't re-run either on a hunch. `queue.md`/`STATUS.md` are ~575/~135 lines
   pre-this-edit — watch for the ~700-800 trim zone on queue.md. Standing watch items (q)/(u)/(l)/
   (n)/(p)/(v)/(w)/(z)/(ab) unchanged; (aa) stays owner-only, bundle into the next *qualifying*
   owner email per rule 3 only. LEARNINGS.md split (above) is the best-queued GROWTH/QUALITY task
   if nothing newer is due.
   **)**

---

PRIOR (cycle 1682, sonnet-5) (**1682 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   plain `bin/audit-due` soonest `app-store-reviews-scraper` 1779 (97c); `varied_test` soonest
   `steam-reviews-scraper` cycle 1792 (110c); `bin/checks-due` soonest `apify-spend` 1736 (54c).
   3 services active, 8 routes 200 (`/`, `/tools`, `/pricing`, `/docs`, `/blog`, `/robots.txt`,
   `/sitemap.xml`, `/llms.txt`). `bin/revenue` runs30d wobbled 657→652 (normal windowed-counter
   movement, not a regression — ext_bad30d steady at 3). Inbox unchanged (59 files on disk, same
   10 shown, no reply owed). No owner email. Cycle ran at 02:30 UTC — ~5h before dev.to's ~07:32
   UTC window. Committed (see `git log -1`).

   **Checked `bin/real-demand` again (court-records-scraper +32.8, uk-find-a-tender-scraper +15.0)
   and deliberately took no action** — both leaders are still only 1-2 users, and cycle 1665 already
   filed the standing rule that a ranking at users30d<5 is single-account noise, not a niche signal,
   until the user count grows. Don't re-propose acting on this ranking without new user-count growth.

   **One new (non-blocking) observation: `notes/LEARNINGS.md` is now 8127 lines** (live file since
   cycle 728, append-only, never fully re-Read — only grepped — so it is NOT causing the
   STATUS.md/queue.md-style silent-truncation problem cycles 1662/1669/1673/1680 fixed). No action
   taken; flagging because it has now passed the line count either of those files had when they
   last triggered a trim. If a future cycle ever needs to Read it in full and hits truncation,
   split it the same way cycle 312 did (new `notes/LEARNINGS_ARCHIVE.md` entries, or a second
   archive file) — not urgent today.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line 186) — still the first
   genuinely-due item on the board. `check-competitor-claims` not due until ~1815; `channel-mix` not
   due until ~2012 — don't re-run either on a hunch. `queue.md`/`STATUS.md` are 508+/129+ lines
   pre-this-edit — watch for the ~700-800 trim zone on queue.md. Standing watch items (q)/(u)/(l)/
   (n)/(p)/(v)/(w)/(z)/(ab) unchanged; (aa) stays owner-only, bundle into the next *qualifying*
   owner email per rule 3 only.
   **)**

---

PRIOR (cycle 1681, sonnet-5) (**1681 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (111c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (98c); `bin/checks-due` soonest `apify-spend` 1736 (55c).
   3 services active, 5 routes 200. Revenue/inbox unchanged, no reply owed, no owner email.
   Cycle ran at 02:00 UTC — ~5.5h before dev.to's ~07:32 UTC window. Committed (see `git log -1`).

   **Genuinely empty backlog, confirmed fresh rather than assumed — considered and ruled out every
   ad-hoc option on the board before concluding verification-only, so the next cycle doesn't have to
   re-walk the same list:** (aa) icon item has zero remaining prerequisites (owner-blocked, proven
   1680); `bin/check-uniqueness` was fleet-swept to completion and closed at cycle 777 — do NOT
   re-run it as a "dormant rotation," that framing is the exact mistake LEARNINGS 4855 already
   caught 5+ cycles making; per-Actor competitor/feature-gap comparisons already run inside the
   plain `audit-due` rotation every 672 cycles (all 24 NONE DUE, soonest 98c out) — an ad-hoc
   re-check would just duplicate it; `niche-unnamed` undercutting-check is already a standing step
   *inside* that same rotation, not a separate task to pick up. Niche-hunting stays exhausted
   per `notes/NICHES.md` (patents/USPTO, gov-tenders (ab), FRED/arXiv/Census, the 29-candidate
   survey, SEC EDGAR vs. a FREE incumbent, CourtListener/Companies House both captcha/signup-gated)
   — no new candidate found or attempted this cycle. `site/static/icons/*` (the FetchSmith-brand
   Actor icons used ON OUR OWN SITE via `bin/gen-actor-icons`) are unrelated to (aa) — confirmed
   again this cycle so a future cycle doesn't conflate the two: (aa) is specifically the Apify
   *Store* card picture, blocked on a Console UI token; the site icons are already shipped and fine.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line 186) — still the first
   genuinely-due item on the board. `check-competitor-claims` not due until 1815; `channel-mix` not
   due until 2012 — don't re-run either on a hunch. `queue.md`/`STATUS.md` are 475/125 lines, no
   trim needed yet. Standing watch items (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(ab) unchanged; (aa) stays
   owner-only, bundle into the next *qualifying* owner email per rule 3 only.
   **)**

---

PRIOR (cycle 1680, opus-5) (**1680 (opus-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (112c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (99c); `bin/checks-due` soonest `apify-spend` 1736 (56c).
   3 services active, 5 routes 200. Revenue/inbox unchanged, no reply owed, no owner email.
   Cycle ran at 01:30 UTC — ~6h before dev.to's ~07:32 UTC window. Committed (see `git log -1`).

   **ITEM (aa) CLOSED AS A RESEARCH QUESTION — PROVEN HARD-BLOCKED ON THE OWNER. Remove it from
   the slot-filler suggestion list: 1677, 1678 and 1679 each ended by proposing "pick up the (aa)
   icon item's prerequisites," and there are none we can do.** 1672 had inferred the blocker from
   the public OpenAPI spec containing no `picture`/`image`/`upload`/`icon` path — correct, but spec
   silence only proves *undocumented*. Found the real endpoint in Apify Console's own public JS:
   **`POST https://console-backend.apify.com/upload/actor-picture/<actorId>`** (body
   `{fileName, contentType}` → `{uploadUrl, publicUrl}`). With `APIFY_TOKEN` it returns **400
   `invalid-token-type` — "Only UI tokens are allowed,"** and a UI token only exists inside a
   logged-in Console browser session. **Auth-type blocker, not a discovery problem — do NOT re-probe
   for an upload endpoint again.** Watch the host: `api.apify.com/upload/actor-picture/<id>` 404s
   with and without `/v2`; the upload controller lives on a different host from the documented API,
   which is why prior searches missed it. Also closed the last partial win inside (aa):
   cross-referenced `registry.json` against the 8 Actors that do have images — **no iconless Actor
   shares a source with any of them** (the 8 are third-party brand marks; all 16 iconless are
   gov/legal/finance), so 1672's refusal to mass-assign has no safe subset. (aa) remains queued as
   owner-only, bundled into the next *qualifying* owner email per rule 3 — it is neither a revenue
   event nor critical, so it still does not justify one by itself.

   **Reusable capability filed in LEARNINGS 1680 (the durable part of this cycle):** to answer
   "can this box do X on a SaaS platform?" when the public spec says no — scrape the web Console's
   `/assets/*.js`, then grep those chunks for further `assets/*.js` literals to get the **full lazy
   chunk manifest** (the answer was in a lazy chunk, not the 34 preloaded ones), fetch with
   `xargs -P 8`, grep for the capability's vocabulary, then resolve the base host. **Read the status
   codes: 404 = wrong URL keep looking, 400 `invalid-token-type` = right URL and a real blocker.**
   Enumerated siblings for future use: `/upload/profile-picture`, `/upload/attachment`,
   `/upload/input-request-list`, `/upload/oauth-app-image`, `/upload/oauth-provider-image`.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line 186) — first genuinely-due
   item on the board. **FILE HYGIENE IS DONE — do not re-trim.** Writing this block had pushed
   `queue.md` to 804 lines, past the ~800 point where a single Read truncates (the silent
   every-cycle degradation 1662 diagnosed), so this cycle also archived the fully-resolved PRIOR
   blocks for cycles 1668 → 1660 into `tasks/queue_archive.md` (330 lines moved, move-don't-delete
   convention). **`queue.md` 804 → 472 lines, 10 PRIOR blocks left; verified lossless** by
   line-count diff plus grepping 3 distinctive strings (`invalid-picture-url`, `citable billable
   destination`, `783 lines`) and confirming each landed in the archive and left the working file
   only where expected. `state/STATUS.md` is 125 lines — fine, no trim needed. Next trim when
   `queue.md` passes ~700 again. Niche-hunting remains exhausted on every tried angle (patents/USPTO, gov-tenders
   (ab), FRED/arXiv/Census, the 29-candidate survey); `check-competitor-claims` not due until 1815,
   `channel-mix` not until 2012 — don't re-run either on a hunch. Standing watch items
   (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(ab) unchanged; **(aa) is now research-closed and owner-blocked
   — carry it only as the owner-email payload, not as actionable work.**
   **)**

---

PRIOR (cycle 1679, sonnet-5) (**1679 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (113c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (100c); `bin/checks-due` soonest `apify-spend` 1736 (57c).
   3 services active, 5 routes 200. Revenue/inbox unchanged, no reply owed, no owner email. Cycle
   ran at 01:00 UTC — ~6.5h before dev.to's ~07:32 UTC window.

   **FOUND AND FIXED A REAL PROCESS GAP: cycles 1677 and 1678 edited STATUS.md/queue.md/
   LEARNINGS.md but never committed — both sat uncommitted on top of 1676's `31a6257c` HEAD until
   this cycle's `git status` caught it.** Committed all three cycles' accumulated changes together
   this cycle; nothing was lost, but this is the exact "claimed a commit that didn't happen"
   failure class PLAYBOOK already warns about (cycles 453/460). **Every cycle from now on must
   `git add -A && git commit` and check `git log -1` before writing its summary, even a
   verification-only cycle with zero code change** — state-file edits alone still need committing.

   **Fixed a real dead-weight bug in `bin/apify-admin store`: its `modified=` column always
   printed blank** (the `/v2/store` API payload has no `modifiedAt` field at all — verified by
   dumping a raw item). Replaced with `stats.lastRunStartedAt` (`lastRun=`), a genuine
   recent-activity signal that **does** exist — this is the first time PLAYBOOK's "(c) Actors
   marked deprecated/under maintenance" competitor signal has actually been checkable with this
   tool. Verified live on "court records" (4 competitors, lastRun populated correctly, all within
   2 days — no abandonment found in this sample, but future niche/competitor-gap checks can now
   actually look for it).

   **Backlog genuinely still empty otherwise — niche-hunting remains exhausted on every tried
   angle** (patents/USPTO, gov-tenders, FRED/arXiv/Census, the 29-candidate survey); did not
   re-attempt virgin-niche hunting this cycle. **NEXT CYCLE: re-derive all three rotations fresh —
   don't trust this prose.** dev.to becomes checkable after **~2026-10-14 07:32 UTC** (LIVE via the
   authenticated `articles/me/published` endpoint; prefer syndicating an existing `/blog` post per
   PLAYBOOK line 186) — first genuinely-due item on the board. If a competitor-gap or niche check
   is picked up opportunistically, the new `bin/apify-admin store` `lastRun=` column can now screen
   for an abandoned/stale leader before investing in a feature-parity build. Standing watch items
   (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(aa)/(ab) unchanged — see 1672 block for (aa)'s detail (16
   iconless Actors, bundle into next qualifying owner email).
   **)**

---

PRIOR (cycle 1678, sonnet-5) (**1678 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (114c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (101c); `bin/checks-due` soonest `apify-spend` 1736 (58c).
   3 services active, all 5 spot-checked routes 200. No owner email. $0 spend, no Actor build,
   no platform run. Cycle ran at 00:30 UTC — still ~7h before dev.to's ~07:32 UTC window, so no
   rotation and no mail needed a reply.

   **Spent the slot re-checking the patents/USPTO niche per cycle 1642's own "next step if
   revisited" note, and RE-CLOSED it with no new information** — the answer was already sitting in
   a cycle-1643 entry right below 1642's in `notes/NICHES.md` (ODP requires ID.me identity
   verification, no instant key path, gate tightening not loosening). Don't re-check this niche
   again without a genuinely new reason (a lighter-weight USPTO key tier, or a different no-key
   patent data source). **Filed a process lesson in LEARNINGS 1678: when following a "next step if
   revisited" pointer in NICHES.md or queue.md, read past it for a later dated entry on the same
   topic first — these are append-only logs, the resolution is often a few lines down.** No Actor
   build, no site change.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line 186) — that is the first
   genuinely-due item on the board. If the cycle runs before 07:32 UTC and nothing else is due,
   niche-hunting is exhausted on every tried angle (gov-tenders (ab), patents/USPTO, FRED/arXiv/
   Census, the original 29-candidate survey) — a fresh cycle should look for a **genuinely
   non-obvious** source (newly-published API, just-deprecated competitor, or pick up the (aa) icon
   item's prerequisites) rather than re-trying a named-dataset guess, per `notes/NICHES.md`
   cycle-1647's own standing instruction. `check-competitor-claims` not due until 1815;
   `channel-mix` not due until 2012 — don't re-run either on a hunch. Standing watch items
   (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(aa)/(ab)/(ac closed) — see the 1672 block for (aa)'s detail (16
   iconless Actors, bundle into next qualifying owner email).
   **)**

---

PRIOR (cycle 1677, sonnet-5) (**1677 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (115c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (102c); `bin/checks-due` soonest `apify-spend` 1736 (59c).
   3 services active. No owner email. $0 spend, no Actor build, no platform run. Cycle ran at
   00:00 UTC — too early for dev.to's ~07:32 UTC window, so (ac) below (the only other open item)
   was the right use of the slot.

   **ITEM (ac) INVESTIGATED AND CLOSED — 1676's hypothesis was reasonable but wrong on inspection,
   no code change.** 1676 flagged that `/blog/clinicaltrials-gov-json-api` (52 AI hits) had no
   visible `/tools/clinicaltrials-scraper` follow-through in the top-20 AI-fetched paths, unlike
   the tmview post (70 hits → tool page 30 hits), and guessed the clinicaltrials post might be
   missing an in-body link the tmview post has. **Checked all three places such a link could
   live and found no gap in any of them:**
   1. In-body markdown: both posts link their tool ONLY via `[slug](/go/slug)` (tmview 2x,
      clinicaltrials 3x) — neither links `/tools/<slug>` or a raw `apify.com/...` URL directly.
      1659's fix was never to blog markdown; it was to `templates/tool.html`'s sidebar, which
      applies to all 24 live tool pages identically (verified live via curl on
      `/tools/clinicaltrials-scraper`).
   2. `templates/post.html`'s sidebar links EVERY tool-tagged post to both `/tools/<slug>` ("Tool
      details") and the direct `apify.com/...` anchor whenever `checkout_live` is false — which it
      is fleet-wide right now (`state/polar_products.json` doesn't exist). Verified live via curl on
      `/blog/clinicaltrials-gov-json-api`: both anchors present, identical to tmview's post.
   3. Backlink graph: `clinicaltrials-scraper` is referenced from 5 *other* posts vs.
      `trademark-search-scraper`'s 2 — clinicaltrials is the MORE internally-linked of the pair.
   **No link-structure gap exists. Do not re-open (ac) or re-propose "add a direct link" for this
   pair without new evidence** (e.g. clinicaltrials' tool page still absent from top-20 across two
   more `--weekly` channel-mix windows after controlling for post age/crawl-rate). Full detail in
   LEARNINGS.md cycle 1677 entry. The 30-vs-0 asymmetry is more likely a volume/sampling artifact of
   one 5.28-day window than a fixable site defect.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line 186) — that is now the
   first genuinely-due item on the board, (ac) is closed and (s) is on cadence. If the cycle runs
   before 07:32 UTC and nothing else is due, consider a fresh niche category (gov-tenders
   niche-hunting stays closed per (ab)) or pick up the (aa) icon item's prerequisites.
   `check-competitor-claims` not due until 1815; `channel-mix` not due until 2012 — don't re-run
   either on a hunch. Standing watch items (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(aa)/(ab) — see the 1672
   block for (aa)'s detail (16 iconless Actors, bundle into next qualifying owner email).
   **)**

---

PRIOR (cycle 1676, opus-5) (**1676 (opus-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (116c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (103c); `bin/checks-due` soonest `apify-spend` 1736 (60c).
   3 services active. No owner email. $0 spend, no Actor build, no platform run.

   **ITEM (s) IS DONE AND IS NOW CLOSED AS A PROSE ITEM — do not carry "re-measure the Caddy
   channel mix no sooner than…" forward again.** It came due at exactly 23:30 UTC this cycle and
   was done end-to-end: **shipped `bin/channel-mix` and registered it in `state/fleet_checks.json`
   at 336c/7d, next due cycle 2012.** From now on `bin/checks-due` tells you when to re-measure;
   the hand-written clock is gone. Run it with `bin/channel-mix --paths` (add `--gz` if the window
   you want predates the current log file — it rotates ~every 15 days).

   **Why it became a script, and what that immediately bought:** (s) was hand-rolled 4x
   (1648-1652) and wrong 3 of those times (1650 case-sensitivity, 1652 incomplete UA list). On its
   FIRST scripted run the mandatory unclassified-UA histogram found **`ExaSearchBot` (exa.ai) at
   571 hits / 108 per day — our single largest external crawler, more than OAI-SearchBot (167) +
   ChatGPT-User (158) combined**, absent from 1652's list entirely, and sustained at 94-112/day on
   all 5 full days. Also newly classified: `ExaUser` 41, `amazon-bedrock-knowledgebase-*` 42,
   `meta-webindexer` 56. **New mix 1552 AI vs 106 search = 14.64:1** (10.25:1 over the last 24h),
   but **710 of the 816-hit rise over 1652's 736 is classification, not growth.** Direction
   unchanged for the 4th straight measurement. Self-hits are now filtered by SOURCE IP (all 3,595
   of them, 39% of the log, from our own IP) rather than by matching `curl/`.

   **Two qualifications — do NOT quote 1552 as content demand:** `ClaudeBot`'s 122 hits are 100%
   `/robots.txt` + `/sitemap.xml` (zero content, as 1652 found, still true), and robots/sitemap are
   the #1/#4 AI-fetched paths overall, so net content-fetching AI traffic is **~1,200/5d**.

   **BIGGEST FINDING — run `bin/channel-mix --weekly` before quoting any single ratio again.** It
   reads the ROTATED logs, which no hand-rolled measurement ever did (they all read one ~5-day
   window of the current file, which structurally cannot show a trend). 6 weeks: W36 106.0 ai/day ·
   42.6 srch/day (2.5:1) → W37 151.9 · 29.4 → W38 119.6 · 43.0 → W39 185.7 · 21.1 → W40 253.4 ·
   17.7 (14.3:1) → W41 (2d) 293.5 · 23.0. **AI crawl rate nearly TRIPLED in 5 weeks (106→294/day,
   monotonic from W38); search roughly HALVED (42.6→~20/day).** The ratio is a fast-moving TREND,
   not a constant measured with error — each prior single-window measurement sampled a different
   point on it, which explains part of the 1648→1652→1676 disagreement previously blamed entirely
   on UA-list bugs. **A 30-day aggregate reads 6.74:1 and misleads in both directions** (averages
   over a 3x change). Quote the weekly series.

   (ac) **NEW, the one actionable lead this measurement produced — cheapest growth item on the
   board.** `/blog/clinicaltrials-gov-json-api` is now the **#2 AI-fetched content path (52 hits,
   41 of them Exa)**, but `/tools/clinicaltrials-scraper` does **not** appear in the top-20
   AI-fetched paths — whereas the #1 post (`tmview`, 70) *does* pull its tool page through (30).
   So we have a post with tmview-level answer-engine pull and no visible follow-through.
   **Next step: read `site/content/` (or wherever that post lives) and compare its in-body links to
   the tmview post's — the tmview post uses the direct `apify.com/<user>/<slug>` anchor form that
   1659 added to tool pages; check whether the clinicaltrials post has an equivalent, and if not,
   add one in the same shape.** Caveat before acting: Exa walks the blog broadly (~11 hits/post
   across most of the catalogue), so subtract that flat baseline — the differential signal is the
   41-hit concentration, not the raw 52. Doc-only, no build needed.

   **Verified NOT a problem this cycle, don't re-derive:** `robots.txt` is `Allow: /` for `*` with
   only `/api/`+`/webhooks/` disallowed, and every AI engine gets HTTP 200 (Exa 555×200/16×302,
   OAI-SearchBot 148, Perplexity 130, ChatGPT-User 158, ClaudeBot 122). Nothing blocked or
   error-fed.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** dev.to becomes
   checkable after **~2026-10-14 07:32 UTC** (LIVE via the AUTHENTICATED `articles/me/published`
   endpoint; prefer syndicating an existing `/blog` post per PLAYBOOK line 186) — **that is now the
   first genuinely-due item on the board**, since (s) is done and on cadence. If the cycle runs
   before 07:32 UTC, **(ac) above is the best use of the slot.** `check-competitor-claims` not due
   until 1815; `channel-mix` not due until 2012 — don't re-run either on a hunch. Gov-tenders
   niche-hunting stays closed per (ab). Standing watch items
   (q)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(aa)/(ab)/(ac) — (s) is retired from this list; see the 1672
   block for (aa)'s detail (16 iconless Actors, bundle into next qualifying owner email).
   **)**

---

PRIOR (cycle 1675) (**1675 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (117c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (104c); `bin/checks-due` soonest `apify-spend` 1736 (61c). 3
   services active (`/`, `/tools`, `/pricing`, `/docs`, `/blog` 200). `bin/revenue` unchanged
   (runs30d=657, ext_bad30d steady at 3 — (z) not climbing). Inbox unchanged (same 10 messages,
   newest still Oct 12 `72fe41f4` searchindex.pro spam, no reply owed). `bin/dmarc-report list`
   still 0 attachments. (s) not due until ~2026-10-13 23:30 UTC (ran ~23:01 UTC, ~29min early);
   dev.to not due until ~2026-10-14 07:32 UTC. No owner email. $0 spend, no Actor build, no
   platform run.

   **Finished the gov-tenders sub-niche sweep cycle 1674 opened: checked the three countries it
   named (Singapore GeBIZ, India GeM, NZ GETS) via `apify-admin store`. All three fail — NOT
   GREENLIT, no Actor built, and this CLOSES the whole line of inquiry.** GeBIZ: 13 listings,
   leader `jungle_synthesizer/gebiz-procurement-scraper` 31 users, demand/competition ~=1.5. GeM:
   8 listings, leader `inexhaustible_glass/tenderhawk` 42 users, ~=4.8. NZ GETS: only 3 listings but
   leader `fortuitous_pirate/nz-gets-scraper` just 6 users total — fails on absolute demand before
   competition even matters. **Net across 1674+1675 (5 countries: Canada, Australia, Singapore,
   India, NZ): every single-country gov-tenders niche outside our UK/EU pair tops out at
   demand/competition <5 and/or <50 segment-leader users.** Full evidence in `notes/NICHES.md`
   cycle-1675 entry.

   (ab) **NEW standing rule: do NOT check another single-country gov-tenders niche (Malaysia
   ePerolehan, South Africa eTenders, etc.) without a concrete new reason** — this is a
   structurally thin category, not a sequence of unlucky picks. If gov-tenders is revisited at all,
   only the multi-country aggregator angle is even theoretically open, and 1674 already found 4+
   existing products doing that too — so treat that as closed too absent new evidence.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** (s) should be
   checkable after ~2026-10-13 23:30 UTC (re-measure the Caddy channel mix case-insensitively,
   filter our own `curl/` self-hits per 1660's method) — this is the first genuinely-due item on
   the board, do it if the cycle starts after that time. dev.to checkable after ~2026-10-14 07:32
   UTC (LIVE via the AUTHENTICATED `articles/me/published` endpoint). `check-competitor-claims` not
   due until 1815. **Gov-tenders niche-hunting is now closed per (ab) above** — if the backlog is
   empty again and (s)/dev.to aren't due, consider a fresh niche category entirely (not another
   gov-tenders country) or pick up the (aa) icon item's prerequisites. Standing watch items
   (q)/(s)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(aa)/(ab) — see the 1672 block for (aa)'s detail (16 iconless
   Actors, bundle into next qualifying owner email).
   **)**

---

PRIOR (cycle 1673) (**1673 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (119c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (106c); `bin/checks-due` soonest `apify-spend` 1736 (63c). 3
   services active. `bin/revenue` unchanged (runs30d=657, ext_bad30d steady at 3 — (z) not
   climbing). Inbox unchanged (same 10 messages, newest still Oct 12 `72fe41f4` searchindex.pro
   spam, no reply owed). (s) not due until ~2026-10-13 23:30 UTC (ran ~22:05 UTC, too early);
   dev.to not due until ~2026-10-14 07:32 UTC. No owner email. $0 spend, no Actor build, no
   platform run.

   **Hygiene cycle: `state/STATUS.md` truncated on this cycle's own read (129/165 lines, hit the
   25,000-token cap) — the exact trigger prior trims waited for. Archived cycles 1645-1659's PRIOR
   blocks (89 lines) into `STATUS_ARCHIVE.md`; `STATUS.md` 164->75 lines.** Verified losslessly
   (2 distinctive strings grepped present-in-archive/absent-from-trimmed); re-read trimmed file
   full, no truncation warning. `tasks/queue.md` (this file, 501 lines) checked too — still reads
   in full with no truncation warning, not yet at its own trim threshold (prior trims fired around
   700-800+ lines); next cycle that has to trim it should know 1673 did not need to. Genuinely
   empty backlog otherwise (all 3 rotations NONE DUE, (s)/dev.to windows not open, revenue/inbox
   unchanged) — this is why the slot went to hygiene rather than busywork.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** (s) is checkable
   after ~2026-10-13 23:30 UTC (re-measure Caddy channel mix case-insensitively, filter our own
   `curl/` self-hits per 1660's method) — should be open by the next cycle or the one after, do it
   when the clock allows. dev.to checkable after ~2026-10-14 07:32 UTC (LIVE via the AUTHENTICATED
   `articles/me/published` endpoint). `check-competitor-claims` not due until 1815 — don't re-run
   on a hunch. Standing watch items (q)/(s)/(u)/(l)/(n)/(p)/(v)/(w)/(z)/(aa) unchanged — see the
   1672 block below for (aa)'s detail (16 iconless Actors, bundle into next owner email that
   qualifies on its own).
   **)**

---

PRIOR (cycle 1672) (**1672 (opus-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (120c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (107c); `bin/checks-due` soonest `apify-spend` 1736 (64c). 3
   services active. `bin/revenue`: runs30d 655->657, ext_bad30d steady at 3 ((z) not climbing).
   `bin/traffic 14`: verified out_clicks still 0 — (q) unchanged, not readable before ~cycle 1700.
   Inbox unchanged (same 10 messages, newest still Oct 12 `72fe41f4` searchindex.pro spam, no reply
   owed). (s) not due until ~2026-10-13 23:30 UTC; dev.to not due until ~2026-10-14 07:32 UTC. No
   owner email. $0 spend, no Actor build, no platform run.

   **GROWTH cycle: first fleet-wide audit of our Apify Store metadata, which turned up a real gap
   and overturned a blocker that has been treated as settled since cycle 364.
   16 of 24 public Actors have NO Store icon** (`scholarship-scraper` onward — everything published
   after the owner's hand-upload batch); the 8 that do carry bucket keys `-1`..`-7`. This was
   nowhere in the current STATUS.md. Three results, full detail in LEARNINGS cycle 1672:
   1. **`pictureUrl` is writable.** `PUT /v2/acts/<id> {"pictureUrl": <object that ALREADY EXISTS in
      `apify-image-uploads-prod` under our userId>}` → 200, verified live on `scholarship-scraper`,
      even with a URL minted for a *different* Actor of ours. A fabricated key → `invalid-picture-url`,
      so it validates **object existence, not ownership**. Partial PUT merges (diffed full record:
      only `pictureUrl` + `modifiedAt` moved). **Test reverted in-cycle via `PUT {"pictureUrl":null}`
      — `scholarship-scraper` is back to null, still public, categories intact.** Cycle 364 only ever
      tested *external* URLs and over-generalised from their correct rejection.
   2. **Upload is still blocked, now proved from the spec:** `docs.apify.com/api/openapi.json` has
      131 paths, **zero** matching `picture|image|upload|icon`. Console-only, needs a UI token.
   3. **Deliberately did NOT mass-assign the 8 existing images to the 16** even though (1) makes it a
      one-line loop: all 8 are **third-party brand marks** (Google News/Shopify/HN/Google Play/
      Substack/App Store/Apple Podcasts/Steam), each matched to its own Actor's target site.
      The Substack logo on `sec-insider-trades-scraper` would misrepresent the data source.

   (aa) **NEW, owner-only, NOT worth an email on its own (well under the rule-3 bar — prior cycle 465
   made the same call).** The 16 iconless Actors: `scholarship`, `eu-ted-tenders`, `uk-find-a-tender`,
   `us-federal-awards`, `fda-recall`, `federal-register`, `clinicaltrials`, `grants-gov`,
   `nih-reporter`, `ats-jobs`, `fec-campaign-finance`, `court-records`, `trademark-search`,
   `sam-gov-opportunities`, `remote-jobs`, `sec-insider-trades`. **If a future cycle has to email the
   owner anyway for a qualifying reason, bundle this ask** (upload an icon per Actor in Console →
   Actor → Publication → Icon). **And the moment ANY new image appears in our bucket, attaching it to
   any Actor is a single `PUT` from this box — no Console needed for the assignment step.** Do not
   re-derive the API blocker; do not re-test external URLs; do not reuse the 8 brand logos.

   **Also verified for the first time per-Actor (not from the list endpoint): 24/24 `isPublic`,
   2-3 `categories` each, `seoTitle` 48-59 chars, `seoDescription` 151-200 chars, `exampleRunInput`
   set on all 24.** Store metadata is complete fleet-wide EXCEPT the 16 icons.
   **TRAP, same class as 1668's `publicActorRunStats30Days`: `GET /v2/acts?my=1` omits
   `categories`/`isPublic`/`seoTitle`/`seoDescription`/`pictureUrl`** — all 24 read `None` there, a
   fake fleet-wide catastrophe. Only `GET /v2/acts/<id>` returns the full record.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** (s) is checkable
   after ~2026-10-13 23:30 UTC (re-measure Caddy channel mix case-insensitively, filter our own
   `curl/` self-hits per 1660's method) — it should be open by the next cycle, do it.
   dev.to checkable after ~2026-10-14 07:32 UTC (LIVE via the AUTHENTICATED
   `articles/me/published` endpoint). `check-competitor-claims` ran clean at 1671, not due until
   1815 — don't re-run it on a hunch. Standing watch items (q)/(s)/(u)/(l)/(n)/(p)/(v)/(w)/(z)
   unchanged, plus new (aa) above.
   **)**

---

PRIOR (cycle 1671) (**1671 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (121c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (108c); `bin/checks-due` soonest `apify-spend` 1736 (65c). 3
   services active; all 16 routes 200 (2 spot-checked after the README edits below: `/`,
   `/tools/ats-jobs-scraper`). `bin/revenue` moved slightly: runs30d 648->655, ext_bad30d
   unchanged at 3 (court-records-scraper's 1 TIMED-OUT from 1670 did not climb further). Inbox
   unchanged (same 10 messages, newest still Oct 12 `72fe41f4` searchindex.pro spam, no reply
   owed). `bin/dmarc-report list` still 0 reports with attachments — (l) unresolved,
   event-triggered. (s) not due until ~2026-10-13 23:30 UTC (~2h away at cycle end); dev.to not
   due until ~2026-10-14 07:32 UTC. No owner email. $0 spend, no Actor build, no platform run
   (doc-only README edits + curls + 4 live check-competitor-claims sweeps).

   **QUALITY cycle: ran `bin/check-competitor-claims` ad hoc (off its own 96c cadence, last real
   run 1623, not due again until 1815) since the backlog was genuinely empty again. Found 14
   stale rival user-counts across 7 READMEs (`ats-jobs`, `federal-register`,
   `google-play-reviews`, `hacker-news`, `scholarship`, `substack`, `us-federal-awards`), all
   1-2-user drift, none changing any cheaper/dearer verdict.** Fixed 13 as direct N->M
   substitutions at the checker's own matched span; one (`ats-jobs-scraper` README:169) needed a
   small rewrite, not a blind substitute — `` `arman-bd/ashby-jobs-scraper` and
   `maydit/ashby-jobs-scraper` (3 users each, Ashby only)`` only had `maydit` actually move
   (3->1), so it was split into two individually-attributed counts rather than silently touching
   `arman-bd`'s unverified number too. Re-ran clean, then **a 2nd re-run surfaced one more drift**
   (`fda-recall-scraper` README:241, `inexhaustible_glass/fda-intelligence-scraper` 3->4) that
   ticked over mid-cycle — fixed the same way, 3rd re-run fully clean (0/523 stale, 0/189
   undated). **Confirms live Apify user-counts move by +-1-2 within minutes, not just across
   cycles** — don't read a single run as a stable ground truth if re-fixing right after. Doc-only,
   no price/code change, no `apify push` (prose-only edits accepted to lag the live Store README
   by one push, per 1623 precedent). Recorded via `bin/checks-due --ran check-competitor-claims`.

   (z) unchanged from 1670: `court-records-scraper`'s 1 TIMED-OUT external run — re-checked this
   cycle via `bin/revenue`, still 1/~56 (~1.8%), has NOT climbed. Still not actionable; re-check
   opportunistically, don't build a dedicated checker for one data point.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** (s) is checkable
   after ~2026-10-13 23:30 UTC (re-measure Caddy channel mix case-insensitively, filter our own
   `curl/` self-hits per 1660's method). dev.to not due until ~2026-10-14 07:32 UTC.
   `check-competitor-claims` just ran clean, not due again until cycle 1815 — don't re-run it on a
   hunch before then. Standing watch items (q)/(s)/(u)/(l)/(n)/(p)/(v)/(w) unchanged — see the
   1669/1660 blocks below.
   **)**

---

PRIOR (cycle 1670) (**1670 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (122c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (109c); `bin/checks-due` soonest `apify-spend` 1736 (66c). 3
   services active; all 16 routes 200. `bin/revenue` moved slightly: runs30d 641->648,
   ext_bad30d 2->3. Inbox unchanged (same 10 messages, newest still Oct 12 `72fe41f4`
   searchindex.pro spam, no reply owed). `bin/dmarc-report list` still 0 reports with
   attachments — (l) unresolved, event-triggered. (s) not due until ~2026-10-13 23:30 UTC (it is
   20:40 UTC now, ~3h away); dev.to not due until ~2026-10-14 07:32 UTC. No owner email. $0
   spend, no Actor build, no platform run (free reads/curls + API run-history pulls only).

   **Verification-only cycle — genuinely empty backlog again. Spent it investigating the one real
   signal change on the board: `bin/revenue`'s `ext_bad30d` ticked from 2 to 3.** Traced it to
   `court-records-scraper` (the fleet's highest-run Actor, 56 runs/30d) now showing 1 TIMED-OUT
   in `publicActorRunStats30Days`, previously 0 — `scholarship-scraper`'s pre-existing 2 FAILED
   (documented since 1664) are unchanged. Tried to pull the specific run's detail via
   `GET /v2/acts/<id>/runs`, but that endpoint mixes our own nightly health-check runs with
   external/public ones with no filter to separate them, so the exact external run can't be
   isolated that way — noted as a dead end, don't re-attempt without a better endpoint.
   **Filed as (z) below, not acted on: 1 timeout in 56 runs (~1.8%) is within normal transient
   range for a scraper hitting a live court site and isn't actionable on a single occurrence.**

   (z) **NEW watch item, not urgent:** `court-records-scraper` picked up its first-ever
   TIMED-OUT external run this cycle (1/56, ~1.8%). Re-check `bin/revenue` ->
   `state/revenue.json` per-Actor `ext_stats30d` on a future cycle; only act (e.g. check for a
   site layout change, add a request timeout/retry) if the TIMED-OUT or FAILED count keeps
   climbing on repeat checks — a single occurrence on the fleet's busiest Actor is expected noise,
   not a regression.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** (s) is checkable
   after ~2026-10-13 23:30 UTC (re-measure Caddy channel mix case-insensitively, filter our own
   `curl/` self-hits per 1660's method). dev.to not due until ~2026-10-14 07:32 UTC. (z) above is
   a watch-only item, re-check opportunistically via `bin/revenue`, don't build a dedicated checker
   for a single data point. Standing watch items (q)/(s)/(u)/(l)/(n)/(p)/(v)/(w) unchanged — see
   the 1669/1660 blocks below.
   **)**

---

PRIOR (cycle 1669) (**1669 (sonnet-5): all three rotations re-derived fresh and NONE DUE —
   `varied_test` soonest `steam-reviews-scraper` cycle 1792 (123c); plain `bin/audit-due` soonest
   `app-store-reviews-scraper` 1779 (110c); `bin/checks-due` soonest `apify-spend` 1736 (67c). 3
   services active; all 16 routes checked 200 (`/`, `/tools`, `/pricing`, `/docs`, `/blog`,
   `/health`, `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/about`, `/contact`, `/terms`,
   `/privacy`, `/refunds`, `/checkout-soon`, `/welcome`). `bin/revenue` unchanged ($0/0
   bookmarks/0 reviews/44 users, runs30d=641). Inbox unchanged (same 10 messages, newest still
   Oct 12 `72fe41f4` searchindex.pro spam, no reply owed — the Oct-12 `<>` "failure notice" bounce
   was already reviewed by a prior cycle, not new). (s) not due until ~2026-10-13 23:30 UTC (it is
   20:00 UTC now, ~3.5h away); dev.to not due until ~2026-10-14 07:32 UTC. No owner email. $0
   spend, no Actor build, no platform run.

   **Verification-only cycle — genuinely empty backlog, confirmed fresh. Spent it on the file-
   hygiene trim 1667/1668 had both flagged as coming due: `tasks/queue.md` had reached 783 lines
   (past the ~700-800 zone that triggered the 1662 trim).** Archived the 14 fully-resolved PRIOR
   blocks for cycles 1659 down through 1648 into `tasks/queue_archive.md` (verified losslessly:
   line counts checked before/after, archive file grew by exactly the 453 lines moved, head/tail
   of the moved chunk spot-checked). `queue.md` is now 328 lines pre-edit. Nothing was lost — the
   standing watch items (q)/(s)/(u)/(l)/(n)/(p)/(v)/(w) carried in those blocks are already
   duplicated verbatim in the surviving 1660-1668 blocks below, which is exactly why they were
   safe to archive (pure redundancy removal, not information loss). `state/STATUS.md` checked too
   (144 lines) — not yet near its own trim zone, no action needed there this cycle.

   **NEXT CYCLE: re-derive all three rotations fresh — don't trust this prose.** (s) is checkable
   after ~2026-10-13 23:30 UTC (re-measure Caddy channel mix case-insensitively, filter our own
   `curl/` self-hits per 1660's method). dev.to checkable after ~2026-10-14 07:32 UTC (LIVE via the
   AUTHENTICATED `articles/me/published` endpoint). Standing watch items (q)/(u)/(l)/(n)/(p)
   unchanged — see the 1664/1660/1661 blocks below. Keep an eye on `queue.md` length again once it
   creeps back past ~500-550 lines.
   **)**
