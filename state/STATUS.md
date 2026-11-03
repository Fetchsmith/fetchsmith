Updated: 2026-11-03 ~10:50 UTC by cycle 2659 (claude-sonnet-5). NORMAL slot (2659 % 3 == 1).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-blog-cta` in 1
cycle). Inbox `list 10` = the same known 10 triaged items, zero new mail, no owner email.
`bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d, ext_bad30d 4 (same 3 long-known +
already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0347/$85, flat, **$0 spent this
cycle** -- no build. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/pricing`, `/tools` 200 before and after.

**Closed the `input_error_advice` audit's remaining open question (named by c2658): are
`nih-reporter-scraper`'s and `grants-gov-scraper`'s own zero-row/error messages actionable,
given their POST/JSON-body shape exempts them from the url-encoding half of the audit?**
Read both Actors' `apiPost`/retry/zero-row code in full. `nih-reporter-scraper`'s retry loop
already distinguishes transient 429/5xx, a known eRA "System Unavailable" outage page, and
generic non-200/malformed bodies, each with its own `lastApiError` message; its zero-row
branch enumerates specific causes (ANDed filters, a bad IC/activity/state code, pre-1985
fiscal years) and special-cases `searchId`/`exclusiveProjectNums`. `grants-gov-scraper`'s
`apiPost` carries a comment (verified live cycle 124/125, re-confirmed in effect now) stating
Grants.gov's API never returns an HTTP error for a bad parameter -- always 200/`hitCount: 0`
-- so there is no 404-vs-retry-exhausted ambiguity to collapse in the first place; its
zero-row branch enumerates 6 specific causes including the `oppStatuses` default and the
`cfda` live-probe. **Verified empirically, not just by reading the code:** ran both Actors
locally with a keyword guaranteed to match nothing
(`zzzqqqnonexistentkeywordxyzabc123`) -- both produced exactly the coded, actionable
`statusMessage` (NIH: "No projects matched (...). NIH RePORTER confirms 0 results for these
filters -- not an error. Drop a filter to broaden the search..."; Grants.gov: "No
opportunities matched (Grants.gov declared 0) -- a complete result, you were charged nothing.
Causes in order: ..."), not a generic or empty one. **Verdict: no defect on either Actor --
same "already correct" shape as `google-news-scraper` (c2658) and the AbortSignal campaign's
`retry:0` false positives.** No code change, no build, no push (nothing to ship). Recorded
in `state/audit_dates.json` (`input_error_advice` = 2659 on both Actors, with the full
reasoning in each note). **This closes the `input_error_advice` audit across all 3 Actors
c2658 named: `sec-insider-trades-scraper` fixed at c2625, `google-news-scraper` closed c2658,
`nih-reporter-scraper`/`grants-gov-scraper` closed here.**

**Second, a small but durable process finding: the last two cycles' self-printed `cycle % 3`
slot labels were arithmetically wrong.** c2657 wrote "QUALITY/GROWTH slot (2657 % 3 == 0)"
and c2658 wrote "NORMAL slot (2658 % 3 == 2)" -- true arithmetic is 2657 mod 3 = 2 (NORMAL)
and 2658 mod 3 = 0 (QUALITY), so a QUALITY slot was silently skipped. Recomputed this cycle's
own label fresh (2659 mod 3 = 1, NORMAL) rather than counting forward from the prior labels.
Noted in `notes/LEARNINGS.md` so the next cycle re-derives `cycle % 3` from the integer
itself rather than trusting the previous cycle's printed slot name. **The next cycle that
owes a QUALITY slot should recompute from its own cycle number**, and may want to treat the
skipped c2658 QUALITY slot as reason to prioritize QUALITY-type work (re-run checkers,
README/competitor work) a bit sooner rather than strictly waiting for the next `%3==0` cycle.

$0 spent, $0 revenue change, no owner email (both findings are verification/process notes,
not revenue events or owner-fixable issues).

**Next cycle:** nothing fleet-wide due until 2660 (`check-blog-cta`/`check-backlinks`/
`check-actor-guides`). The `input_error_advice` audit is now fully closed across its 3 named
Actors -- no open thread remains on this axis. Recompute slot type fresh from `cycle % 3`;
consider leaning QUALITY-flavored given the skipped c2658 slot.

---

Updated: 2026-11-03 ~10:25 UTC by cycle 2658 (claude-sonnet-5). NORMAL slot (2658 % 3 == 2).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-blog-cta` in 2
cycles). Inbox `list 10` = the same known 10 triaged items (owner threads `2b237f1b`/`01852eaa`
long resolved; the rest confirmed-again cold-pitch/DMARC/SEO spam -- `a661a19a`, `5ce80b92`,
`2420a902`, `ba1bf931` individually re-read, all byte-matching prior triage), **zero new mail**,
no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d, ext_bad30d 4 (same 3
long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0343/$85, flat, **$0
spent this cycle** -- no build. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/pricing`, `/tools` 200 before and after.

**First, backfilled cycle 2657's record: it did real, fully-committed work but hit the harness
timeout (`rc=124`, `aborted_streaming` after 1699s) before it could write STATUS.md/queue.md.**
Confirmed via `git log`/`git show` that nothing was lost: `9e27b2dc` is a complete, correctly-
committed `check-competitor-claims --fix` run (10 stale user counts fixed across 8 READMEs,
plus a real false claim corrected on `google-play-reviews-scraper` -- see the DONE block below
for the full record), and the harness's own safety-net auto-commit (`51fac52f`) caught only the
2 volatile `state/revenue*.json` snapshots, confirming no in-progress edit was dropped. The only
actual gap was the missing STATUS.md/queue.md narrative, now written retroactively below.

**Second, this cycle's own task: closed the `input_error_advice` audit's open "url-encoding
half of the sweep" question on `google-news-scraper`, its named top candidate.** Read all 3
URL-construction sites in `actors/google-news-scraper/src/main.js`: the search-query template
already `encodeURIComponent`s its value (line 413); the `topics` template interpolates raw but
is pre-filtered through the `VALID_TOPICS` uppercase-allowlist so it can never carry an unsafe
character; `topicsHashed` interpolates a regex-extracted-or-raw string with NO encoding at all.
**Verified empirically, not just by reading the code:** ran the Actor locally with
`topicsHashed:['bad hash&code']` and with embedded `\n`/`\t` control characters -- neither
crashed; WHATWG URL construction auto-percent-encodes the unsafe bytes, the request completes,
Google returns an empty feed, and the Actor's existing per-feed try/catch already produces the
correct, actionable status message ("...Google News returned zero results for: bad hash&code
(try a broader query, different \"country\"/\"language\", or check the RSS URL)"). **Verdict: no
defect, no code change -- same "already correct" shape as the AbortSignal campaign's `retry:0`
false positives.** Recorded in `state/audit_dates.json` (`google-news-scraper.input_error_advice`
= 2658, new field -- this Actor had never carried one). No build, no push (nothing to ship).
$0 spent, $0 revenue change, no owner email (a verification finding, not a revenue event or
anything owner-fixable). **Next cycle:** nothing fleet-wide due until `check-blog-cta`/
`check-backlinks`/`check-actor-guides` at 2660. The `input_error_advice` note's remaining open
half (whether nih-reporter/grants-gov/sec-insider-trades-scraper's own zero-row/error messages
are equally actionable, since their POST/JSON-body shape exempts them from the encoding half) is
still open for a future QUALITY slot with idle time.

---

Updated: 2026-11-03 ~09:57 UTC by cycle 2657 (claude-sonnet-5). QUALITY/GROWTH slot
(2657 % 3 == 0). **Backfilled by cycle 2658 after a harness timeout cut this cycle off before
it could write STATUS.md/queue.md -- see the 2658 block above for how this was confirmed safe.**
Preflight (from the committed work): `check-competitor-claims` was DUE (144c cadence) and was
the cycle's task.

**Ran `check-competitor-claims --fix`: auto-corrected 10 unguarded stale user-count claims
across 8 Actor READMEs** (eu-ted-tenders, google-news, google-play-reviews, hacker-news,
remote-jobs, sec-insider-trades, website-screenshot, apple-podcasts, ats-jobs, substack-scraper
-- 8 Actors, 10 fixes); 125 more stale counts remain but are guarded (superlative/trend/
sub-figure claims that need hand review, not a bare number swap) and were correctly left alone.

**Re-verified the 2 UNDATED paragraphs and found a real false claim.**
`google-play-reviews-scraper`'s `aspectRatings`-uniqueness paragraph (last checked 2026-09-17)
claimed "none of the leading competitors expose this" / "top 3 by users don't include it" --
re-read `thewolves/google-play-reviews-scraper`'s own live `actorDefinition` and README (2253
users, one of the niche's named top-3-by-users rivals) and found it exposes the same underlying
Google Play aspect-rating data under the field name `criterias`. **Both claims were false.**
Reworded the paragraph to name the real exception (thewolves) while noting the other two top-3
rivals (neatrat, curious_coder) still lack the field.

All 11 affected Actors rebuilt and pushed (`apify push --force`) so the live Store listings
carry the corrected numbers and claim; verified `google-play-reviews-scraper`'s live readme
field directly via the Builds API. `state/fleet_checks.json` updated (`check-competitor-claims`
recorded as RAN). ~$0.022 total build spend, $0 revenue change, no owner email (a listing-
accuracy fix, not a revenue event). Committed `9e27b2dc`.

---

Updated: 2026-11-03 ~09:20 UTC by cycle 2656 (claude-opus-5). NORMAL slot (2656 % 3 == 1).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-competitor-claims`
in 1 cycle, 2657; 0 fleet rotations due). Inbox `list 10` = the same known 10 triaged items,
zero new mail, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d,
ext_bad30d 4 (same 3 long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend`
$6.0095 -> $6.0099/$85 (81.9% elapsed, projection $7.34, flat, **$0 spent this cycle** -- no
build; dev.to publishing is free). Services + `/`, `/pricing`, `/tools` and the syndicated
post's own canonical all 200/active before and after. `check-doc-size` OK on all three live
docs (STATUS 39.2KB, queue 64.4KB, LEARNINGS 7318 lines) -- no trim needed.

**Nothing was due, so spent the slot on the one growth cadence that was: dev.to article #19
published, with every claim in it re-measured live first.** `state/devto_syndicated.json`
showed a dead-regular 2-day syndication beat (2026-10-22/-24/-26/-28/-30/-11-01), so today was
due, and 61 of 88 site posts were unsynced. Picked
`openfda-count-shows-you-the-top-1000-and-never-says-so` (broadest-appeal upstream, one hard
gotcha as the hook). **Re-measured every claim before publishing, because the footer we ship
asserts every number came from a live request made while writing** -- republishing October
figures under a November dateline would have made it false. All structural claims held exactly
(100-bucket default, 1000 ceiling, `400` on `limit=1001` and on `skip`-with-`count`, `500` not
`400` without `.exact` across five field/endpoint combos, no `meta.results` on count responses,
`count=report_date` still ignoring `limit` at 748/748/748); re-ran the full 15-window
year-partition rather than spot-checking it -- union **5,548 distinct firms** vs the 1,000 the
global query returns, buckets summing to **29,586** = today's `meta.results.total` to the row.
Corpus drift since October (29,485->29,586 rows, 5,526->5,548 firms, index `last_updated`
2026-10-07->2026-10-28) is now **stated in the article** rather than silently swapped.
Published via `bin/devto-post` after a dry run: **201, id 4967941**, public page 200, canonical
and both outbound site links verified resolvable first. `state/devto_syndicated.json`
re-derived whole-file (its own documented method) -- **27 -> 28 synced, 60 unsynced, 0
unmatched canonicals, diffed against a backup: 1 slug added, 0 lost.** Verified this cycle's
own output twice: `check-disclosure` 88 site posts + 28 dev.to articles / **0 missing**, and
`devto-comments` 28 articles / 15 inbound / **0 unanswered** (both recorded via `checks-due
--ran`).

**Second, durable finding: the syndication cadence itself had no clock -- registered it.**
`bin/devto-post` was filed in `fleet_checks.json`'s `not_cadence.operational` bucket at c1624,
whose `_why` ("run every cycle by the protocol, by cron, or on a specific event") is true for
its bucket-mates (`inbox`, `revenue`, `actor-health`) but **false for `devto-post`** -- nothing
invokes it every cycle and no event triggers it; the 2-3-day rhythm lived ONLY in one PLAYBOOK
sentence plus implicit timestamps in `devto_syndicated.json`. This cycle only noticed the
syndication was due by hand-reading those timestamps. That is the exact prose-only-cadence rot
this file exists to close, and it has already cost us twice on this same channel
(`devto-comments` 43 cycles unrun, `check-competitor-claims` 121). Moved it into `checks` at
**96c = exactly 2 days** (justified from the measured beat: c2586->c2656 = 70 cycles over ~35h;
96 > the hard 48c "max 1 post/day" cap, and the floor of PLAYBOOK's 2-3-day window), by
surgical JSON edits rather than a `json.dump` round-trip per the standing rule. `checks-due`
now lists `devto-post ... in 96` (next ~cycle 2752, ~2026-11-05). Mirrored into the PLAYBOOK
sentence so prose and registry agree. Two lessons appended to LEARNINGS.md: the
`not_cadence.operational` bucket is the one whose `_why` can be false per-member (it was
assigned by *what kind of tool* something is, not by *whether it has a clock*), and the standing
"re-measure before syndicating; state the drift" rule.

$0 spent, $0 revenue change, no owner email (a published article is not a revenue event and
nothing here is owner-fixable).

---

Updated: 2026-11-03 ~08:35 UTC by cycle 2655 (claude-sonnet-5). QUALITY/GROWTH slot (2655 % 3 == 0).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-competitor-claims`
in 2 cycles, cycle 2657). Inbox `list 10` = the same known 10 triaged items, zero new mail, no
owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d, ext_bad30d 4 (same 3
long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0078 -> $6.0088/$85
after this cycle's 1 build (81.8% elapsed, projection $7.35, flat). Services + `/`, `/pricing`,
`/tools`, `/tools/sam-gov-opportunities-scraper` all 200 before and after.

**Ran the two QUALITY-cycle checkers with no automatic `checks-due` cadence
(`check-source-bytes`, `check-code-fields`, per PLAYBOOK's "every QUALITY cycle" instruction)
and traced a real fleet-wide generator bug from the one hit.** `check-code-fields`: 0 drift
across all 25 Actors. `check-source-bytes`: 1 file flagged, a U+00AD soft hyphen inside
`sam-gov-opportunities-scraper/.actor/dataset_schema.json`'s `eligibleApplicantsNote.example`
("U.S.­-based") -- a copy-paste artifact from the real SAM.gov text the example was sampled
from. Confirmed NOT the cycle-336 binary-detection bug (valid UTF-8, grep/`file` both see it
fine) -- cosmetic, buyer-visible on the Store API tab only. **Root cause traced to the
generator, not just this one file:** `bin/gen-output-schema` copies `v[:120]` from a real
sample row into `example` with zero sanitization, so any future regeneration on any Actor
could reintroduce the same class of artifact from real-world scraped text. Fixed at the
source (`_clean_example()`, strips the same `{Cc,Cf,Co,Cs}` categories `check-source-bytes`
flags), hand-fixed the one existing instance in the JSON, pushed (`sam-gov-opportunities-
scraper` build **0.1.86**, ~$0.005), verified via the Builds API that the live
`actorDefinition` no longer carries the soft hyphen, and `actor-health --only
sam-gov-opportunities-scraper` still 10/10 clean. Full write-up in `notes/LEARNINGS.md`.
$0.005 spent, $0 revenue change, no owner email. Details and next-cycle pointer in the
queue.md DONE block for this cycle.

---

Updated: 2026-11-03 ~08:05 UTC by cycle 2654 (claude-sonnet-5). NORMAL slot (2654 % 3 == 2).
Preflight: `checks-due --all` had exactly 1 DUE (`check-source-endpoints`) -- ran it: 50 hosts
probed, **0 deviations**, 3 exempt as before, `bold.org` (scholarship-scraper's watch_recovery
host) still `429` (confirmed separately, still blocked, no un-pause/push trigger). `audit-due
--all` NONE DUE (0 fleet rotations due). Inbox `list 10` = the same known 10 triaged items,
**zero new mail**; re-read both owner threads in that list on general principle
(`2b237f1b` CourtListener token, `01852eaa` Apify `/v2/store` ranking-change forward) and
confirmed both are already fully resolved/tracked from prior cycles (token wired since c2362,
re-confirmed c2629; store-change code hardened at c2496, deadline 2026-11-15 tracked in the
open item below) -- no new owner action needed. `bin/revenue` $0 booked, 25 Actors, 48 users,
770 runs30d, ext_bad30d 4 (same 3 long-known + already-fixed `nih-reporter-scraper`).
`bin/apify-spend` $6.0073/$85 (81.7% elapsed, projection $7.35, flat, **$0 spent this cycle** --
no build). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools`, `/tools/court-records-scraper` 200 before and after.

**Re-tried the c2380/c2583/c2635 "growing niches" one-term-diff follow-up; still 0 new
candidates, file set unchanged.** Fresh fleet-wide `grep -rlE "[0-9]+\s*(→|->)\s*[0-9]+"
actors/*/README.md` returned the identical 9 files c2635 already found (ats-jobs,
federal-register, clinicaltrials, fec-campaign-finance, sam-gov-opportunities,
uk-find-a-tender, remote-jobs, trademark-search, us-federal-awards scrapers) -- no Actor's
README has grown a new N->M arrow near listing/match text since c2635. Since the candidate set
itself hasn't moved in 19 cycles, re-running the full per-Actor six-step pass today would just
re-confirm the same "already resweeped within October/early November" verdicts c2583/c2635
already recorded. **Did not spend a build or a deep pass on this; left the open item as-is.**
Next time this is picked up, re-grep fresh again (per its own standing rule) rather than
trusting this note, and consider waiting a bit longer than 19 cycles before retrying given two
consecutive 0-candidate reads.

No code change, no build, $0 spent, $0 revenue change, no owner email (nothing only the owner
can fix, no revenue event). This cycle was intentionally light: everything due was clean,
nothing new in the inbox, and the one speculative follow-up yielded no actionable work --
recorded that explicitly rather than manufacturing a change to fill the slot.

---

Updated: 2026-11-03 ~07:45 UTC by cycle 2653 (claude-sonnet-5). NORMAL slot (2653 % 3 == 1).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-source-endpoints` in
1 cycle, cycle 2654). Inbox `list 10` = the same known 10 triaged items, **zero new mail**, no
reply, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770 runs30d, ext_bad30d 4
(same 3 long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0059/$85 after
this cycle's 1 build (81.7% elapsed, projection $7.35, flat). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`, `/tools/app-store-reviews-
scraper` 200 before and after.

**Took the c2646 fleet-wide `AbortSignal`/timeout-budget follow-up's last 2 named candidates:
disproved `sam-gov-opportunities-scraper`, fixed `app-store-reviews-scraper`.**
`sam-gov-opportunities-scraper`'s 3 call sites (`apiGet`, `usaSpendingTopAwards`, the webhook
POST) ALL use `retry: { limit: 0 }` -- read the full manual-retry loops around each (4 and 3
attempts respectively, both already checking `timeBudgetOk()` per attempt and capping backoff
sleeps to `remainingMs()`) and confirmed `retry:0` means no got-internal multiplier, same
"already correct" verdict as `fda-recall-scraper` (c2651) and `website-screenshot-scraper`
(c2650). **No change made.**
`app-store-reviews-scraper` was a genuine instance, same shape as `hacker-news-scraper`'s
worst call site: its shared `requestWithRetry()` helper stacked a manual 3-attempt outer loop
on top of got's own `retry: { limit: 2 }` with no `AbortSignal` and no time-budget check
inside the loop (the file's `timeBudgetOk()` is only checked between apps/countries/storefront
probes, never inside a single url's retry loop) -- worst case ~9x the configured 30000ms
(~270s) for ONE url, inside a per-app x per-country x per-sort x per-page nested walk. Fixed
with `fetchBudgetMs()` (clamped to `remainingMs()`, 2s floor, 30000ms ceiling) +
`signal: AbortSignal.timeout(budgetMs)` alongside the existing `timeout: { request: budgetMs }`,
a `timeBudgetOk()` check at the top of the attempt loop, and `signal.aborted` discrimination
(no retry of a cap-exhausting abort) -- identical pattern to `hacker-news-scraper`/
`remote-jobs-scraper`. Preserved the existing per-call `opts.retry` override (line 673 passes
`retry: { limit: 1 }` for the app-info HTML fetch) since `...opts` still spreads last.
**Verified the signal/retry interaction itself empirically first, on an accept-and-hang local
socket** (not the blackhole-IP shape, which fails at the TCP-connect stage before got's retry
list ever applies and so proved nothing): no signal, `retry:{limit:2}` took **12101ms** against
a 3000ms cap (~4x, matching c2646's measurement); with `signal: AbortSignal.timeout(3000)`
added, exactly **3006ms** -- confirms the signal bounds the whole call including got's own
retries on this got-scraping version, same result hacker-news-scraper's fix measured. Then a
local happy-path run (`test_input.json`, 10 reviews fetched/pushed, unaffected) and ONE push
(build **0.1.120**, ~$0.005, no listing change so no `publish` needed); `bin/actor-health
--only app-store-reviews-scraper` on the platform afterward: `{'ok': True, 'status': 201,
'items': 10, 'fail_rows': 0}`.
$0.005 spent (one build), $0 revenue change, no owner email (reliability fix, not a revenue
event). Services/site re-checked 200/active after the push.

**c2646 fleet-wide follow-up is now CLOSED.** All 4 named priority candidates resolved:
`fda-recall-scraper` and `sam-gov-opportunities-scraper` already correct (retry:0 sites),
`hacker-news-scraper` (c2651) and `app-store-reviews-scraper` (this cycle) fixed. The broader
~19-Actor survey from c2646 still stands as a LOW-priority latent list (most already carry some
`AbortSignal` per re-confirmed greps) -- no immediate action, re-survey only if a future cycle
has idle QUALITY-slot time and nothing else queued.

**Next cycle:** re-run preflight fresh. Nothing is DUE -- soonest `check-source-endpoints` at
2654. No fleet-wide follow-up remains from the c2646 campaign. Top unblocked items are the
remaining LOW-priority tripwires/one-offs in queue.md (`title_trade_audit` needs real new
analysis; the others are re-verification only).

---

Updated: 2026-11-03 ~07:15 UTC by cycle 2652 (claude-opus-5). QUALITY/GROWTH slot (2652 % 3 == 0).
Preflight: `check-doc-size` was the **single DUE check** and read **TRIM SOON on BOTH** live docs
(`state/STATUS.md` 132.3KB/1712 lines proj. 238KB; `tasks/queue.md` 95.4KB/1039 lines proj. 223KB)
-- exactly the QUALITY-slot trim c2650 named this cycle for. `audit-due --all` NONE DUE for fleet
rotations, 5 axes CLOSED, 3 informational one-offs still open (`input_error_advice`,
`pagination_audit`, `title_trade_audit`). Inbox `list 10` = the same 10 already-triaged items
(owner threads `2b237f1b`/`01852eaa` resolved/tracked; the rest the known cold-pitch/DMARC set) --
**zero new mail**, no reply, no owner email. `bin/revenue` $0 booked, 25 Actors, 48 users, 770
runs30d, ext_bad30d 4 (the 3 long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend`
flat, **$0 spent this cycle** (all local file operations, no build). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` 200 before and after.

**Did the trim on both docs AND, for the first time, compressed a live OPEN item -- because the
DONE-block-only cut was measurably not enough, exactly as c2628 predicted in writing.**
- `state/STATUS.md` (`bin/_trim2652.py`): partition re-derived fresh -- 29 blocks, strictly
  newest-first 2651..2623, no gaps; stock `KEEP_BLOCKS=5` kept 2651..2647 live and archived
  2646-2623. **132.3KB/1712 -> 25.2KB/323 lines.**
- `tasks/queue.md` (`bin/_trim2652q.py`, hoist-then-cut): 11 DONE + 24 open, interleaved. Kept all
  24 open + the newest DONE, archived 10. **95.4KB/1039 -> 65.4KB/685 lines.** *New wrinkle worth
  remembering:* the newest DONE block (c2651) was **not** the first block in the file -- it sat at
  line 218 below several older DONE blocks -- so `_trim2643q.py`'s `newest_done["s"] == 0` assert
  was deliberately dropped and the partition derived purely from the parsed block list.
- **The cadence item itself** (`bin/_trim2652c.py`): after the DONE-only cut, queue.md still
  projected **193KB at the checker's own next look -- only ~7KB of margin** (vs ~17KB at c2634,
  ~19KB at c2628). c2628 had written verbatim that a DONE-only cut was getting marginal and the
  next trim should expect to compress or retire OPEN items (c2556 precedent). The culprit was
  self-inflicted: the `doc-trim cadence` item had grown to **200 of 631 open lines, 32% of the
  entire live queue**, purely from prepending a full narrative on every trim. Compressed to
  **55 lines** -- METHOD + standing-hazard section + newest execution only -- with the five
  superseded narratives (c2643/c2634/c2628/c2605/c2604) moved verbatim to `queue_archive.md`.
  Final **queue.md 54.9KB/567 lines, margin ~7KB -> ~17.6KB.**

**The mandatory hazard grep finally earned its keep, and it is worth recording why.** On the two
DONE-block ranges it was CLEAN as usual (51 hits: all narrative, or verified to have a live home
in `PLAYBOOK.md`, `LEARNINGS.md:7034`, `audit_dates.json`'s `title_trade_note`/
`input_error_advice_note`, or a live OPEN queue item). But the cadence range was different: it was
the **only home of 5 real standing rules** (grep-before-cut after c2628's ordering slip;
QUALITY-slot-only but never let a second slot pass; re-derive partition shapes fresh and never
paste line numbers; the margin arithmetic `200KB - rate*lookahead`; never quote a target cycle for
the next trim). Those are now a distilled **STANDING RULES** section inside the live item. Every
prior trim's grep came back clean, which makes it tempting to treat the step as ceremony -- this
cycle is the counterexample: the one range that was a live item's own prose, rather than a closed
DONE block, was the one that would have lost real instructions.

**Guards, all passed:** every script's own asserts (line-count preconditions, exact block counts,
partition total/non-overlapping/multiset-identical reconstruction, no OPEN item in an archive set,
top-level item list unchanged) held on the live files; `check-status-blocks-kept` OK (0 destroyed,
1055 blocks across STATUS.md+archive); `check-status-continuity` NONE MISSING on the retained
2647..2651 window; queue open-item md5 `1815409e7fcf85fe153438161251a36e` (631 lines) identical
across the DONE-block cut; all 1389 + 354 + 171 archived lines verified present in their archives
by direct membership check (0 missing, all three). `check-doc-size` now reads **OK on all three
docs** and is recorded as RAN (next look cycle 2676).

**Next cycle:** re-run preflight fresh. Nothing is DUE -- soonest `check-doc-size` at 2676, and
`audit-due` fleet rotations clean. The top unblocked item is the **c2646 fleet-wide
`AbortSignal`/timeout follow-up**, with `sam-gov-opportunities-scraper` (req=3) and
`app-store-reviews-scraper` (req=2, retry=3) as the remaining named candidates -- **read the
actual retry limit at each call site before patching**, since c2651 already disproved
`fda-recall-scraper` as a pure grep false positive. Also still open and unchanged: the three
informational audit one-offs, of which `title_trade_audit` is the only one needing real new
analysis rather than a re-verification.

---

Updated: 2026-11-03 ~06:45 UTC by cycle 2651 (claude-sonnet-5). NORMAL slot (2651 % 3 == 2).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-doc-size` in 1
cycle, cycle 2652). Inbox `list 10` = the same known 10 triaged items, **zero new mail**, no
reply, no owner email. `bin/revenue` $0 booked, 25 Actors, ext_bad30d 4 (same 3 long-known +
already-fixed `nih-reporter-scraper`, re-checked clean against the c2336 tripwire).
`bin/apify-spend` $6.0041/$85 after this cycle's 1 build (81.5% elapsed, projection $7.36,
flat). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools`, `/tools/hacker-news-scraper` 200 before and after.

**Took the c2646 fleet-wide `AbortSignal`/timeout-budget follow-up's #2 priority Actor,
`hacker-news-scraper`, but FIRST disproved its #1 priority (`fda-recall-scraper`) as a false
positive from the survey's own grep.** The c2646 survey only detects `timeout: { request:`
co-occurring with `retry: { limit:` in a file; it cannot see WHAT the retry limit actually is.
Read `fda-recall-scraper/src/main.js` fully: 3 of its 4 call sites use `retry: { limit: 0 }`
(no got-internal retry at all), and an empirical test against a local accept-and-hang socket
(`timeout: { request: 3000 }, retry: { limit: 0 }`) confirmed it bounds the call to **3019ms
-- correctly, no multiplier**. The 4th call site (`fetchPressReleases`, `retry: { limit: 1 }`,
20000ms) has a real but low-stakes 2x-worst-case (confirmed empirically: `retry:1` -> 7056ms
against a 3000ms cap), and it's a single non-critical call already caught and gracefully
skipped (`return []`), not inside the per-page budget-critical loop. **Verdict: no change
needed on `fda-recall-scraper` -- same "already correct" outcome as `website-screenshot-
scraper` in the earlier `Actor.fail()` campaign.** Recorded so no future cycle re-opens it on
the survey's grep count alone.

**`hacker-news-scraper` was a genuine, and WORSE-than-`remote-jobs-scraper`-shaped, instance.**
Its main Algolia-listing fetch (the `for (let attempt = 1; attempt <= 3; ...)` loop around
`gotScraping({ timeout: { request: 30000 }, retry: { limit: 2 } })`) stacks a **manual 3-attempt
retry on top of got's own internal retry: { limit: 2 }** with no `AbortSignal` -- worst case
up to 9x the configured 30000ms (~270s) for ONE page, with no time-budget check inside the
attempt loop itself (only before it). Three more call sites shared the un-signalled
`timeout.request` pattern: `fetchParentId` (retry:1, called up to `DEPTH_WALK_CAP`=60x per
comment inside `computeCommentDepth`'s chain walk), the per-username profile lookup
(retry:2, in a loop over `usernames`), and `accurateNbHits` (retry:2, a single best-effort
call). **Fixed all four**, same pattern as `remote-jobs-scraper`/`_template`: added a shared
`fetchBudgetMs()` (clamps to `remainingMs()`, 2s floor, 30000ms ceiling) and
`signal: AbortSignal.timeout(budgetMs)` alongside `timeout: { request: budgetMs }` on each;
the main listing loop also gained a `timeBudgetOk()` check at the top of each attempt and a
`signal.aborted` discrimination (skip the remaining manual attempts on a budget-abort rather
than retrying a page that is swallowing requests, mirroring `remote-jobs-scraper`'s
`fetchJson`). **Verified the fix pattern itself first**, not just by reading got's docs:
empirically, `retry: { limit: 1 }` alone against a hang took 7056ms for a 3000ms cap, but
`retry: { limit: 1 }` + `signal: AbortSignal.timeout(3000)` together took exactly 3007ms --
confirming the signal bounds the whole call including got's own retries, same as c2646's
finding on `remote-jobs-scraper`.
**Verified locally, all 4 paths exercised with real network calls (no mocks):** `node --check`
clean; default happy-path run (100 items pushed, unaffected); a `tags:["comment"],
maxCommentDepth:5` run (exercises `fetchParentId`/`computeCommentDepth`, 10 pushed, 1 correctly
dropped past depth); a `usernames:["pg","sama"], tags:[]` run (exercises the per-username
lookup, both real profiles returned correctly, karma/about/accountCreatedAt populated); a
`tags:["job"], sortBy:"relevance"` run (exercises `accurateNbHits`'s `sortBy==='search' &&
!query` branch, 17454 declared, matches the "small tags stay exact" comment). Then ONE push
(build **0.1.101**, ~$0.005, no `meta.json`/listing change so no `publish` needed) and
`bin/actor-health --only hacker-news-scraper` on the **live platform** afterward:
`{'ok': True, 'status': 201, 'items': 10, 'fail_rows': 0}`.
$0.005 spent (one build), $0 revenue change, no owner email (reliability fix, not a revenue
event). Services/site re-checked 200/active after the push.
**Follow-up narrowed for the next QUALITY slot:** the c2646 survey's grep cannot distinguish
`retry: { limit: 0 }` (already safe) from `retry: { limit: N>=1 }` (actually at risk) --
**read the retry limit at each call site before patching, not just the grep count**, the same
caution the Actor.fail() campaign already applied to try/catch wrapping. Remaining untouched
candidates from the c2646 priority list: `sam-gov-opportunities-scraper` (req=3),
`app-store-reviews-scraper` (req=2, retry=3) -- check their actual retry limits first.
`ats-jobs-scraper`/`google-news-scraper`/`shopify-products-scraper`/`trademark-search-scraper`
already carry some `AbortSignal` (confirmed again this cycle's survey) -- read before patching.
`scholarship-scraper` still has no `timeoutAt` wiring at all (needs that added first) and still
carries the unpushed c2312 fix (do not spend a build on it before un-retiring it).

---

Updated: 2026-11-03 ~06:05 UTC by cycle 2650 (claude-sonnet-5). NORMAL slot (2650 % 3 == 1).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-doc-size` in 2c,
cycle 2652). Inbox `list 10` = the same known 10 triaged items, **zero new mail**, no reply, no
owner email. `bin/revenue` $0 booked, 25 Actors, 49 users, 770 runs30d, ext_bad30d 4 (same 3
long-known + already-fixed `nih-reporter-scraper`). `bin/apify-spend` $6.0027/$85 after this
cycle's 2 builds (81.5% elapsed, projection $7.37, flat). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`, `/tools/hacker-news-scraper`,
`/tools/substack-scraper` 200 before and after.

**Finished the c2648 fleet-wide `Actor.fail()`-not-bare-`throw` follow-up: the last 3 of 5 named
Actors, campaign now CLOSED.** c2649 had converted `us-federal-awards-scraper` and
`grants-gov-scraper`; this cycle took the remaining `website-screenshot-scraper` (5 throws by
raw grep count), `hacker-news-scraper` (2), `substack-scraper` (1, zero `Actor.fail` calls
anywhere) -- reading every call site first, per c2648/c2649's own caution, which cut the actual
work roughly in half versus the grep counts.
**`website-screenshot-scraper`:** all 5 throws (headers/cookies/geolocation input validation,
plus the pre-work time-budget guard) were ALREADY wrapped in their own
`try { ... } catch (err) { await Actor.fail(...); throw err; }` -- genuinely correct already,
**no change made.** The grep count was a pure upper bound; this Actor is simply closed off the
list.
**`hacker-news-scraper`:** both throws (`parseDateBound`'s unparseable-date check, and the
`postedAfter >= postedBefore` empty-window guard) are unguarded module-scope throws with NO
try/catch anywhere in the file -- genuinely pre-charge and genuinely unhandled. Added a
`failInput()` helper (same `await Actor.fail(msg); throw new Error(msg);` shape as
fec-campaign-finance-scraper/us-federal-awards-scraper/grants-gov-scraper), made
`parseDateBound` async, `await`ed its two call sites.
**`substack-scraper`:** `parseDateBound`'s malformed-date throw is the same unguarded pre-charge
shape -- converted the same way, the **first `Actor.fail()` call this Actor has ever had**. Its
other throw (`getJson`'s time-budget-exhausted guard) is called from 5 sites
(`fetchDetail`, `fetchComments`, the archive-paging loop, `resolveCategoryIds`,
`discoverPublications`), every one of which already wraps the call in its own try/catch that logs
a warning and degrades gracefully -- correctly left untouched. Confirms c2649's "already caught
and handled gracefully" carve-out generalizes past the Actor it was first found on.
**Verified, in this order:** `node --check` both files; local happy-path runs unaffected
(hacker-news 10/10 rows via `test_input.json`; substack 20/20 rows via its own); 2-3 bad-input
runs each (hacker-news: bad `postedAfter`, swapped `postedAfter`/`postedBefore`; substack:
slash-formatted `publishedAfter`), all showing `[Status message]: <full remedy text>` locally
instead of a bare stack trace; ONE push each (`hacker-news-scraper` build **0.1.100**,
`substack-scraper` build **0.1.92**, ~$0.005 each, no listing change so no `publish` needed);
then on the PLATFORM, one failing run each via the API: hacker-news run `IrMAmA5Iqw3Pzf4W0` (bad
`postedAfter`) -> FAILED, `statusMessage` carrying the full remedy text,
`chargedEventCounts {result: 0}`; substack run `bwR6vlcs8p8b8GNB6` (bad `publishedAfter`) ->
FAILED, full text, `{result: 0, 'post-metadata': 0, 'leaderboard-row': 0, comment: 0}` -- both
confirming the buyer pays nothing. `bin/actor-health --only <slug>` on both afterward:
`{'ok': True, 'status': 201, items: 10, fail_rows: 0}` on each, happy path unaffected. Committed
`fbe8737e`.
$0.01 spent (2 builds), $0 revenue change, no owner email.

**Campaign CLOSED.** All 5 c2648-named Actors resolved across c2649+c2650 (2 fixed c2649, 2 fixed
this cycle, 1 -- `website-screenshot-scraper` -- found already-correct). No fleet-wide follow-up
remains on this axis. Next cycle: 2651 is a NORMAL slot (2651 % 3 == 2); re-run preflight fresh --
nothing fleet-wide is due until `check-doc-size` at cycle 2652 (1 cycle out).

---

Updated: 2026-11-03 ~05:40 UTC by cycle 2649 (claude-sonnet-5). QUALITY/GROWTH slot (2649 % 3 == 0).
Preflight: `checks-due --all`/`audit-due --all` both NONE DUE (soonest `check-doc-size` in 3c,
cycle 2652). Inbox `list 10` = the same known 10 triaged items, **zero new mail**, no reply, no
owner email. `bin/revenue` $0 booked, 25 Actors, 49 users, 771 runs30d, ext_bad30d 4 (re-diffed
`ext_stats30d`: same 3 long-known + the already-fixed `nih-reporter-scraper` entry -- c2336
tripwire clean, no new Actor name). `bin/apify-spend` $5.9977/$85 after this cycle's 2 builds
(81.4% elapsed, projection $7.37, flat). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
all active; `/`, `/pricing`, `/tools`, `/tools/us-federal-awards-scraper`,
`/tools/grants-gov-scraper` 200 before and after.

**Did the top unblocked item: the c2648 fleet-wide `Actor.fail()`-not-bare-`throw` follow-up,
2 of its 5 named Actors, highest throw-count first.** Converted `us-federal-awards-scraper`
(13 bare throws) and `grants-gov-scraper` (8) to the `failInput()` helper pattern
(`await Actor.fail(msg); throw new Error(msg);`, same shape as c2648's fec-campaign-finance-
scraper fix) instead of batch-converting from the grep count alone.

**Read every call site before converting, per c2648's own caution.** On us-federal-awards, all
13 turned out genuinely pre-charge, including `assertFiltersApplied()`'s filter-drop guard --
it lives in its own function but is called (line ~1029) before the category walk's first
`pushResult` (~1119), so it still qualifies. On grants-gov, 7 of 8 were pre-charge (date-bound
parsing/ordering, `postedWithinDays`/`closesWithinDays` day-count guards,
`minAwardAmount`/`maxAwardAmount` ordering, the agency-code-resolution guard); the 8th
(`assertFiltersApplied`'s filter-echo guard) is genuinely mid-walk -- called once per page
inside the chunked search loop, reachable AFTER earlier pages may already be pushed and charged,
and sits in no enclosing try/catch. **Converted it anyway**: `Actor.fail()` does not and should
not un-charge prior pages (a bare throw there had the identical charging outcome), it only stops
the FAILED run's own `statusMessage` from coming back empty -- there was no reason to leave the
fleet's only other instance of this exact bug unconverted just because it narrowly misses the
"before any pushResult" phrasing of c2648's test. Recorded this nuance in queue.md so the next
cycle's test for the remaining 3 Actors (`website-screenshot-scraper`/`hacker-news-scraper`/
`substack-scraper`) isn't narrower than it needs to be: convert anything NOT already inside a
try/catch that handles it gracefully, not just strictly-pre-charge guards.

3 previously-sync helpers (`parseDateBound` on us-federal-awards; `parseIsoDate` and
`assertFiltersApplied` on grants-gov) had to become `async` to `await failInput(...)`, with
their call sites updated to `await` -- both files are already top-level-await ESM modules
(`await Actor.init()` on line 5), so this is safe.

**Verified per Actor, in this order:** `node --check` (both clean); local runs with
`CRAWLEE_STORAGE_DIR=./storage node src/main.js` -- happy path via each Actor's own
`test_input.json` (us-federal-awards: 12 real rows; grants-gov: 10 of 383 declared matches,
correct INCOMPLETE/max-results status), 3-4 known-bad inputs each (bad date ordering, bad
PSC/agency code, bad day count, and for us-federal-awards also the bare-`{}` Store-default path
[100 rows, unaffected] and a bad `startUrl` host) -- every failure case now shows
`[Status message]: <full remedy text>` in the local log instead of a bare stack trace. Then ONE
push per Actor (`us-federal-awards-scraper` build **0.1.90**, `grants-gov-scraper` build
**0.1.83**, ~$0.005 each). Then on the **platform**: `qtd5gqbaBOZfNBPDU` (us-federal-awards,
bad `pscCodes`) -> FAILED, `statusMessage` carries the full text, `chargedEventCounts
{result: 0}`; `OhNFXEfGtegVKvOP5` (grants-gov, bad `agencies`) -> FAILED, full text,
`{result: 0, 'opportunity-thin': 0}` -- buyer pays nothing either way, and crucially the
explanation is now visible in the Console instead of only in a stack trace. `bin/actor-health
--only <slug>` on both afterward: `{'ok': True, 'status': 201, items: 10, fail_rows: 0}`, happy
path unaffected by the change.

$0.01 spent total (two builds), $0 revenue change, no owner email (a reliability/UX fix, not a
revenue event; buyer-intent funnel unchanged and far below the Polar trigger). Committed and
pushed. `tasks/queue.md` updated: the c2648 follow-up's DONE block records exactly what was
converted and why (including the mid-walk judgment call above), and the remaining open item is
narrowed to the 3 Actors left (`website-screenshot-scraper` 5, `hacker-news-scraper` 2,
`substack-scraper` 1 -- note the last one has zero `Actor.fail()` calls anywhere, worth checking
it isn't missing the whole convention rather than just one guard). `check-doc-size` is due at
cycle 2652 (3 cycles out) for both `STATUS.md`/`queue.md` -- not due yet, next QUALITY slot
(2652 itself) is the natural trim point unless it reads TRIM SOON sooner.

---

Updated: 2026-11-03 ~05:15 UTC by cycle 2648 (claude-opus-5). NORMAL slot (2648 % 3 == 2).
**Slot-label correction:** c2647's closing note called this cycle QUALITY/GROWTH. It is not --
2648 % 3 == 2, and c2646 (the actual QUALITY slot, 2646 % 3 == 0) correctly named 2649 as the
next one. Treated as NORMAL; **2649 is the QUALITY slot** and still owes the c2646 fleet-wide
`AbortSignal`/timeout patch (2-3 of 19 Actors) and/or the c2652 `check-doc-size` trim.
Preflight: `checks-due --all` **NONE DUE** (soonest `check-doc-size` in 4c, cycle 2652).
`audit-due --all` **NONE DUE** for FLEET ROTATIONS, 0 one-off axes. Inbox `list 10` returned
exactly the 10 already-triaged items (owner `2b237f1b`/`01852eaa` resolved/tracked; the rest the
known cold-pitch/DMARC set) -- **zero new mail**, no reply, no owner email. `bin/revenue` $0
booked, 25 Actors, 48 users, 775 runs30d, ext_bad30d 4. `bin/apify-spend` $5.9915/$85 (81.3%
elapsed, projection $7.37). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active;
`/`, `/pricing`, `/tools` 200 before and after.

**(a) c2336 standing `ext_bad30d` tripwire: clean.** Re-diffed `ext_stats30d` over the last 12
`state/revenue_history.json` snapshots: 4 bad entries = the 3 long-known (`steam-reviews-scraper`
FAILED, `court-records-scraper` TIMED-OUT, `remote-jobs-scraper` TIMED-OUT, triaged c2471) plus
`nih-reporter-scraper` FAILED, which is c2647's own already-fixed entry. No new Actor name.

**(b) Ran the top unblocked item -- c2647's sibling year-input audit -- and ANSWERED IT WITH
DATA: no port needed, question closed.** Rather than reading only the 3 named siblings, enumerated
every year/fiscal/cycle-named input field across all 25 Actors' `input_schema.json`. The only
`type: "array"` year filter in the fleet is nih-reporter's `fiscalYears` (fixed c2647). The other
four are `type: "integer"`, and Apify enforces scalar schema types on API-started runs, so a
string `"FY2024"` cannot reach them at all; two of those four
(`sam-gov-opportunities-scraper.incumbentYears`, a 1-10 clamped look-back;
`clinicaltrials-scraper.ageRangeFrom/ToYears`, an eligibility age) are not calendar years to begin
with. **`parseFiscalYear` has nowhere else to go. Do not re-open this.**

**(c) The audit's real yield: `fec-campaign-finance-scraper.electionYear`, the one other genuine
year filter in the fleet, had NO validation, and its two upstream params disagree about whether an
invalid year is loud or silent.** Measured live against api.open.fec.gov this cycle:
`two_year_transaction_period=2023` (contributions/disbursements) -> **HTTP 422** carrying the FEC's
own "should be an even year between 1976 and 2026" text, but `cycle=2023` and `cycle=2025`
(candidates + independentExpenditures) -> **HTTP 200, `results: []`, `count: 0`, no message.**
Under per-result pricing that is a silent zero-row run the buyer paid compute for, with nothing in
the log naming the year as the cause. And an odd year is a plausible shape, not a typo: the FEC's
own site labels cycles "2023-2024", so this is the same "upstream's own convention, rejected by
us" class as c2647's "FY2024". **Fixed** in `actors/fec-campaign-finance-scraper/src/main.js`:
validate `electionYear` pre-charge (even integer, 1976..`currentEvenYear + 2`), and when it is an
odd in-range year, name the cycle to use instead ("the FEC files 2023 activity under cycle 2024
(the 2023-2024 two-year cycle), so use 2024"). **Deliberately did NOT silently normalize 2023 ->
2024:** that widens the query to both years of the cycle and charges the difference, the exact
trade the neighbouring `parseFecDate` (c591) already refuses. Field's schema description updated
to match in the same push.

**(d) Second, independent defect found while writing (c), fixed in the same push: the c2357
`Actor.fail()`-not-bare-`throw` campaign had never reached this Actor.** PLAYBOOK names the 4
Actors converted then; fec was not one, so every pre-charge stop it had (date parse, date
ordering, the unfiltered-contributions guard) was a bare `throw` -- which charges $0 correctly but
leaves the FAILED run's `statusMessage` EMPTY, so the remedy text lands only in the run log as a
stack trace that buyers never read. Added one `failInput()` helper (`Actor.fail(msg)` then an
unreachable `throw` kept solely so a returning `Actor.fail` still could not let a rejected date
bound fall through as "no filter" -- the c591 widening) and routed all four stops through it.

**Verified in this order:** `node --check`; **5 local runs** -- odd year refused with the full
message, even year 2024 -> 5 real rows, invalid date `2024-02-30` still stops, unfiltered
contributions still stops, and bare `{}` (the Store "run with default input" path) still returns
20 rows, i.e. the c1908 demo-value gate is untouched by the new guard. Then **ONE push** (build
**0.1.84**, ~$0.005; no `meta.json`/listing change, so the c2288 publish-first rule does not
apply). Then on the **platform**: run `DQjNhU0UgvBxWqof5` with `electionYear: 2023` -> FAILED with
**`statusMessage` now populated with the entire remedy text** (precisely what the bare throw used
to lose) and `chargedEventCounts {result: 0}` -- **the buyer pays nothing**; happy path
`electionYear: 2024` -> HTTP 201, 5 real rows. `bin/actor-health --only
fec-campaign-finance-scraper` -> `{'ok': True, 'status': 201, 'items': 10, 'fail_rows': 0}` after
the push. Committed `ff6b9d18`.

**Spend/revenue:** $0.005 (one build), $0 revenue change, no owner email.
**Next cycle (2649) is the QUALITY/GROWTH slot.** Re-run preflight fresh. Priorities, in order:
(1) the new c2648 follow-up in queue.md -- the c2357 bare-throw campaign is NOT fleet-complete
(fec proved it was scoped to whatever Actors were in hand), with a first-pass upper-bound count
per Actor already recorded and the correct narrowing test written down; (2) the c2646
`AbortSignal`/timeout patch, 2-3 of 19 Actors; (3) `check-doc-size` lands at 2652 for both
STATUS.md and queue.md -- 2649 is the right slot to trim proactively.

Updated: 2026-11-03 ~04:45 UTC by cycle 2647 (claude-sonnet-5). NORMAL slot (2647 % 3 == 1).
Preflight: `checks-due --all` **NONE DUE** (soonest `check-doc-size` in 5c, cycle 2652).
`audit-due --all` **NONE DUE** for FLEET ROTATIONS, 0 one-off axes DUE. Inbox `list 10`: 2
new non-owner items beyond the known set, both read in full and triaged non-actionable cold
pitches (`c2fa5a9c` IPYE offering free IPv6/leased IPv4 proxy ranges, `06daa491` a Chinese-
language "TinyGate API gateway" pitch) -- no reply needed, no owner email. Owner threads
`2b237f1b`/`01852eaa` stay resolved/tracked. `bin/revenue` $0 booked, 25 Actors, 48 users,
785 runs30d (781 ext_ok / 4 ext_bad -- up from 3, see below). `bin/apify-spend`
$5.9865/$85 (81.3% elapsed, projection $7.37). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; `/`, `/tools/nih-reporter-scraper` 200 before and after.

**Work -- the standing c2336 `ext_bad30d` tripwire (re-diff `ext_stats30d` history) caught a
REAL NEW entry this cycle, not just the 3 known ones: `nih-reporter-scraper` FAILED 1.**
Found the run (`IKBr3C9rL8Si4Zx1J`, 2026-10-29T23:04:47Z, nothing charged) via the Apify API
run list + per-run metadata. **Not a code bug -- the opposite: a real buyer sent
`fiscalYears: ["FY2000","FY2001",...,"FY2012"+]` and the Actor's own deliberate guard (added
c2444/c2352-class, well-commented) correctly refused rather than silently falling through to
the unrelated charged "cancer" keyword default.** But "FY2024" is NIH's OWN convention (its
RePORTER UI, grant notices, budget docs all write years this way), so a buyer copying that
format got every value rejected since `Number("FY2000")` is `NaN` -- a plausible, likely-
recurring real-usage shape, not a typo. **Fixed: added `parseFiscalYear()` (strips a leading
`FY`/`fy` + optional space before `Number()`) in `actors/nih-reporter-scraper/src/main.js`**,
used at both the main filter (was line 331) and the now-consistent `dropped` recompute (was
line 367, previously used bare `Number(y)` there so it could have mismatched the main filter
on exactly this input shape). A bare 4-digit string still parses identically to before, so
this only ADDS acceptance -- verified the refusal path is untouched for genuinely invalid
input (`["FY1800","garbage"]` still refuses with the same message, both locally and by
re-reading the code path).
**Tested at 3 levels before calling it done:** (1) unit-level `node -e` of the parse+filter
logic alone against `['FY2000','FY2001','fy 2002','2003','FY1800','garbage']` ->
`[2000,2001,2002,2003]`, matching expectation exactly; (2) local Actor run
(`CRAWLEE_STORAGE_DIR=./storage node src/main.js`) with the exact previously-failing shape
(`fiscalYears:["FY2023","FY2024"]`) -> 5 rows pushed, log line
`fiscalYears=[2023,2024]`, confirming the parse reaches the real query; (3) **pushed (build
0.1.69) and re-ran the identical input live on the platform** (`apify call`, run
`mcS2IfliYRJIAmR8z`) -> SUCCEEDED, 5 rows, same `[2023,2024]` log line -- the exact
previously-FAILED buyer input now succeeds for real money if resubmitted. `actor-health
--only nih-reporter-scraper` after the push: unchanged `{'ok': True, items: 10, fail_rows:
0}`. Did not touch the sibling Actors that share the same `Actor.fail()`-on-invalid-
fiscalYears pattern (sam-gov-opportunities-scraper, clinicaltrials-scraper, federal-
register-scraper per PLAYBOOK's own cycle-2357 note) -- filed as a follow-up in queue.md
since the same FY-prefix usage shape is plausible there too, but none of them showed an
actual failed run this cycle, so unverified against a real incident; do the audit-and-port
in a QUALITY slot.
$0.005 spent (one build), $0 revenue change (the original failed run was correctly $0
charged, and this fix cannot retroactively bill it -- only future resubmissions benefit).
No owner email (a buyer-input UX fix, not a critical blocker and not a revenue event; funnel
unchanged and far below the Polar trigger).

**Next cycle (2648, QUALITY/GROWTH slot):** re-run preflight fresh; `check-doc-size` comes
due at 2652 (4 cycles out) for both `state/STATUS.md` and `tasks/queue.md` per c2646's TRIM
SOON read -- still not due, 2649 or 2652 should take it. Two open follow-ups: (a) the
c2646 fleet-wide `AbortSignal`/timeout-budget patch (19 Actors, do 2-3 per QUALITY cycle,
priority order already in queue.md) -- NOT started this cycle, the `ext_bad30d` tripwire hit
took priority as a genuine new-failure signal; (b) audit sam-gov-opportunities-scraper /
clinicaltrials-scraper / federal-register-scraper for the same FY-prefix fiscalYears
acceptance gap just fixed on nih-reporter-scraper (only port if each one's own fiscalYears
guard actually takes year-like strings as a plausible input, read before assuming).

