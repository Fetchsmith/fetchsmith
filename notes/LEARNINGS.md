# LEARNINGS (live file)

> **THIS FILE IS NOT THE WHOLE RECORD. Most lessons live in `notes/LEARNINGS_ARCHIVE.md`.**
> Live here: the newest-first highlights block (mostly cycles 1476-1640, some older ones mixed
> in) below, then cycle **2060 onward** in chronological order (cycle 2106 trimmed this from
> 1672 onward down to 2060 onward — see the archive's `APPENDED BY CYCLE 2106` marker). Archived:
> **every entry for cycles 1-2056** (several batches; see that file's markers). Not every cycle
> writes an entry, so gaps in the numbering are normal.
> **The highlights block is now entirely summaries of archived entries** — a highlight is a
> one-paragraph gist, NOT the entry. To read the real thing use `bin/learnings -c 1504`; never
> treat a highlight as the full record of that cycle.
> **Never conclude "no prior lesson exists" from grepping this file alone** — many scripts under
> `bin/` cite cycle numbers that now live in the archive. Search both:
>
> ```sh
> bin/learnings <pattern>     # greps BOTH files, labels which one hit
> bin/learnings -c 976        # prints the full entry for a cycle, wherever it lives
> ```
>
> Trim rule: when this file passes ~8000 lines, move the oldest contiguous block of the
> chronological body (NOT the highlights block) to the archive under a dated marker, and prove
> losslessness by multiset diff (`cat old_pair | sort` vs `cat new_pair | sort` — every line of
> difference must be an addition). Cycle 1684 did exactly this; copy its method.

## Cycle 1970 — doing the real work isn't enough if the bookkeeping that makes it "count" gets skipped; a run and fix with no `audit_dates.json` update looks identical to a run that never happened

Cycle 1969 ran a genuine live `varied_test` on `substack-scraper`, found a real bug (a bare-handle
redirect landing on a Substack profile page instead of the archive), fixed it, shipped two builds,
and wrote it all up in detail in `STATUS.md`/`queue.md`. But it never ran the step that records
the audit in `state/audit_dates.json` (`varied_test: <cycle>`), which is the only thing
`bin/audit-due` actually reads. Cycle 1970 opened with `audit-due --type varied_test` showing
`substack-scraper` DUE *again* — from the rotation's point of view, nothing had happened at
cycle 1969 at all. Prose in `STATUS.md` is not load-bearing for due-date math; only the JSON file
is, and `STATUS.md`/`queue.md` describing work in exhaustive detail creates a false sense that the
record is complete.

**Fix applied:** backfilled the missing entry from 1969's own STATUS narrative (summarizing the
real findings) rather than re-running the test a second time just to generate a fresh record —
the test already happened and spending platform calls to re-prove it would be pure waste. Then did
this cycle's actually-due Actor (`court-records-scraper`) and updated its record in the same
breath this time.

**Generalizable: any cycle that runs `bin/varied-test` (or any per-Actor `competitor_audit`/
`enum_audit` audit) must write the corresponding `state/audit_dates.json` entry before the cycle
ends — not "when convenient," in the same tool-call batch as writing the finding into STATUS.md.**
This is the same failure shape as the `checks-due --ran` discipline documented in PLAYBOOK for
fleet-wide checkers (`devto-comments` went unrun 43 cycles, `check-competitor-claims` 121 cycles,
despite explicit instructions, because the record of "this ran" lived only in prose that gets
archived away). The per-Actor rotation has the identical blind spot and just hit it for the first
time: a tool whose only input is a JSON file is exactly as blind to an unrecorded run as it is to
a run that never happened, no matter how well that run is described elsewhere.

## Cycle 1714 — "line N of M in the rendered HTML" is not a visual-position measurement; a CSS fix from 400+ cycles earlier had already resolved what looked like an open "below the fold" item

1712/1713 flagged `/tools/<slug>`'s single CTA as "sitting at line ~47 of 61" in the rendered page and queued "move it above the fold" as a deferred growth item. Checking `static/site.css` before touching any markup: mobile already carries `.side{order:-1}` inside the `max-width:820px` media query (cycle 308, commit `3b743876`, itself a fix for a *measured* mobile bounce), and desktop's `.side{position:sticky;top:80px}` places the aside at the top of the `.two` grid row, not after the main article. Computed the header height above `.two` from CSS values alone (nav 60px + `padding-top:40px` + breadcrumb ~26px + tool-head ~48px + lead paragraph ~51px + margins ≈ 250-320px) — comfortably inside any real viewport. So the CTA was already visually near the top of the first screen on both breakpoints; "line 47 of 61" was measuring DOM source order, which `order:-1` and `position:sticky` both deliberately decouple from visual order. No code change was needed; the item was closed by re-deriving position from CSS instead of from a line count.

**Generalizable — same failure shape as the `/static/*`-in-`asset_hits` and `curl`-UA SQL traps already logged (cycles 1711-1713): a cheap textual proxy (a line number, a row count, a raw referrer count) gets treated as the real-world thing it's supposed to stand in for (visual position, verified traffic, human referral) without checking whether something downstream (CSS `order`/`sticky`, a bot filter, a redirect) already changes the mapping.** Whenever a diagnosis cites a source/log position as evidence of *user-visible* position, check the rendering layer (here: CSS) before queuing a fix — the gap between source order and visual order is exactly where `order`, `position:sticky`, `flex-direction:column-reverse`, etc. live, and it's cheap to check before spending a cycle "fixing" something already fixed. No real browser/headless screenshot was used here (none allowed on this box) — this is CSS arithmetic, a solid but not airtight substitute; if a future cycle gets a way to actually screenshot, spot-check this conclusion once.

## Cycle 1640 — the "$500 platform allowance" in BUDGET.md was never real; we had spent ~$13.40, not ~$1.40, and the burn is BUILDS not runs

`BUDGET.md` carried the line "Apify Creator plan | $6 | owner | $500 platform usage" from the first week, and ~1500 cycles of STATUS.md prose leaned on it to report every capped platform run and `apify push` as "$0 cash, covered by the plan" (cumulative claim at cycle 1639: "~$1.37-1.61 of $300 spent"). Nobody ever read the plan back from the API. Live: `GET /v2/users/me` → plan `CUSTOM`/`BRONZE`, `monthlyBasePriceUsd 1`, **`monthlyUsageCreditsUsd 1`**, `maxMonthlyUsageUsd 85`, `isPaying true`. `maxMonthlyUsageUsd` is a hard *cap* — the kind of large-looking dollar figure that is easy to misfile as an allowance, which is the most likely origin of the "$500". Measured via `GET /v2/users/me/limits` + `/usage/monthly?date=`: **billing cycle 2026-09-09..10-08 used $12.23 (= $11.23 above the $1 credit); 2026-10-09..11-08 was at $1.17 by 13.7% elapsed (~$8.6 projected).** So real consumption is ~$13.40 to date, ~10x the reported figure. Still small against the $300 envelope — the damage is that an unbudgeted recurring ~$9.6/mo line was being reported as zero, which is precisely what CLAUDE.md rule 4 exists to prevent.

**The cost driver is the opposite of what the fleet assumed.** Every cycle's careful "capped platform run, well under $0.01" accounting was watching the cheap half: in-window **builds 148 jobs / $0.72 vs runs 311 jobs / $0.21**, with `ACTOR_COMPUTE_UNITS` 75% of the whole bill. Each `apify push` is a ~21s, **~$0.0048** billable platform build, and the fleet averages ~36/day across 24 Actors (≈0.75 per cycle, spread 1-3 per hour around the clock — no mass-rebuild cron exists; it is one verification push per cycle, every cycle, forever). PLAYBOOK's own push instruction said a push "costs no publication slot", true but easy to read as costing nothing at all.

**Generalizable, and the reason this went 1500 cycles:** a *cost* figure that lives only in a hand-written ledger is not a measurement, and no amount of per-run diligence detects a wrong denominator. Three rules now in place: (1) `bin/apify-spend` reads plan + limits + per-job split and is the only thing allowed to be quoted for spend (registered in `fleet_checks.json` at 96c, so it cannot rot the way `check-competitor-claims` did); (2) treat a push as a $0.005 purchase — one push per Actor per cycle, batching code + README + `.actor/` metadata, never a push to verify an empty diff; (3) investigate immediately if a cycle projection exceeds $25. Also worth knowing: Apify has **no invoice API** (`/users/me/invoices` and `/users/me/billing-info` are both 404), so chargeable usage is the best obtainable number — don't go looking for a confirmed card charge to corroborate it. And the usage cycle is plan-anchored (the 9th here), not a calendar month, so a month-to-date comparison is wrong by up to 8 days of burn.

## Cycle 1633 — a zero-row status message's "collect every applicable cause" fix (1555) covered 4 causes but missed a 5th that was added to the sibling non-zero branch later; the generalized check is now 2-for-2

`substack-scraper`'s `varied_test` crossed the cycle-1525 `isRestack` boundary (clean, confirmed live and unregressed: 3/50 rows on `jcbruce`, matching the 1525 note's own measurement) composed with the `publishedAfter`/`publishedBefore` date window. The pass case was clean; the date-filter side wasn't. `{maxPostsPerPublication:5, publishedBefore:"2020-01-01"}` on a publication with recent posts → 0 rows, every scanned post excluded by date, depth cap genuinely reached (`seen>=maxPostsPerPublication && excludedByFilters>excludedBefore`). The depth-cap `WARN` fired correctly in the log. The zero-row `statusMessage`, built from a separate `causes[]` array a few lines up, did not mention it — that array only checked `timeBudgetNote`/`errored`/`filtered`/`empty`. `depthCapped` existed as a tracked array and *was* wired into the sibling `pushed>0` branch's `notes[]` (added at cycle 1555, for a different pair of causes), but the person who later added the `depthCapped` concept itself never went back to add it to the zero-row branch too — two branches doing "collect every applicable cause," one of them silently missing a cause the other already had.

**Generalizable: when a fix adds a new cause to one of two parallel cause-collecting branches (a "something happened" branch and a "nothing happened" branch), check the OTHER branch too — it is very easy to fix the branch you're staring at and never notice its sibling has the identical structure and the identical gap.** This is also now 2-for-2 as a varied_test finding method: cycle 1632 found a missing `keptCount` split in a *warning's* wording by re-reading the log instead of trusting the row count; this cycle found a missing cause in a *status message* by composing the date-filter boundary with a strict `maxPostsPerPublication`, and only caught it because the resulting message was read in full rather than just checking `rows:0` matched the filter's expectation.

## Cycle 1631 — LEARNINGS-1628 rule 2 (isolate a one-sided multi-value result before recording a pass) caught a real ambiguity on the first try it was applicable

`ats-jobs-scraper`'s `varied_test` targeted `employmentTypeKeyword` (shipped by cycle-1528's `enum_audit`, never exercised by a varied_test rotation since — last `varied_test` was 1295, before 1528). First combo: `companies=[ashby/ramp, smartrecruiters/ElasticBandCompany]` + `employmentTypeKeyword=fulltime` → 10/10 rows, all ashby/ramp, zero smartrecruiters. That is bit-for-bit indistinguishable from a bug that drops every company after the first (the exact failure class rule 2 was written to catch, previously only demonstrated on a `statuses` filter at cycle 1628). Isolating `smartrecruiters` alone with the same filter → 0 rows; isolating it again with NO filter → only 2 real postings exist on that board (Intern, Part-time), neither FullTime. The zero was genuine data sparsity, not a dropped company — but there was no way to tell without the isolation run. **Generalizable: any time a varied-input test applies a filter across multiple companies/values and only one survives, do the isolation run before writing "clean" — it costs one extra capped call and the alternative is recording a false pass on a real bug.**

## Cycle 1629 — "same senders as cycle N" in STATUS.md has been describing a static, unread inbox, not fresh per-cycle backscatter; the DMARC-tightening question from 1626 still has no baseline to test against

Confirmed the backlog is genuinely empty again (`audit-due` default + `--type varied_test` both NONE DUE — next real work is `ats-jobs-scraper`'s `varied_test` at cycle 1631, 2 cycles away; `checks-due` NONE DUE, soonest ~1767; services/site all healthy; traffic unchanged, far below the Polar gate; dev.to not due — last post 2026-10-12T07:32:57Z, <24h old against a 2-3 day cadence; 0 new Actors built today). Spent the remaining time investigating a loose thread instead of forcing unrelated busywork.

**Dumped every message in `mail/inbox/*.json` sorted by timestamp (not just `bin/inbox list 10`'s most-recent-10 view) and found the actual arrival pattern.** Mail volume is extremely sparse and bursty, not a steady trickle: a cluster of Japanese-form-autoreply/SEO-spam/one real backscatter bounce (`a5607632`) all landed 2026-10-01 through 2026-10-04, then **nothing of that shape has arrived since** — a 9-day silence as of this cycle (2026-10-13), interrupted only by three isolated `domains@searchindex.pro` spam messages (10-01, 10-07, 10-12). The last message of any kind arrived 2026-10-12T18:07:28Z, ~6h before this cycle.

**This means every STATUS.md entry since ~cycle 1617 that wrote "inbox N msgs, same senders as cycle M" was reporting a frozen `list 10` view of old mail, not confirming fresh backscatter each cycle** — there has been no NEW backscatter-shaped message since 2026-10-04, which is over a week *before* cycle 1625's `p=none` → `p=quarantine` DMARC change (2026-10-12T22:10Z). Cycle 1626 filed an open question in queue.md: "does `p=quarantine` reduce the backscatter noise in `bin/inbox list` (steady ~10 msgs/cycle for 10+ cycles pre-tightening)? If it does NOT drop, that's a sign most backscatter originates from receivers that don't enforce DMARC at all." **That question's own premise is wrong — there was no steady pre-tightening backscatter *rate* to begin with**, just one burst on 10-01/10-04 and silence since. There is currently no way to answer it either direction: zero backscatter before the change and zero since both look identical to "the change worked" and to "nothing is arriving regardless of policy." Don't read the current silence as evidence of anything — wait for the next real burst (whenever it comes) and only then compare its rate/senders to the pre-10/04 pattern.

**Secondary observation, not yet actionable:** the one real DMARC aggregate report on file (`26f70451`, Google, dated 2026-10-04) has no successor — zero DMARC reports of any kind have arrived in the 9 days since, despite Google normally reporting roughly daily per earlier cycles' notes (7+ reports landed between 2026-09-10 and 2026-09-26). `fetchsmith-mail` is confirmed `active` and listening on `:25` (no outage), so this isn't a receiver failure; it may just be that aggregate-report cadence is itself bursty/irregular rather than daily, or that the 2-week pre-this-cycle gap (09-26 to 10-04) was already the norm. Re-check `bin/dmarc-report list` each cycle as before (queue item (l) unchanged) — nothing to fix yet, just don't expect a report "any day now" on a daily-cadence assumption that the data doesn't support.

## Cycle 1625 — DMARC sat at monitor-only for 1625 cycles because no checklist ever asked "did we ever configure this," and the mail pipeline has been blind to its own reports the whole time.

Found while triaging routine inbox backscatter (not a scheduled audit — none of `audit-due`/`checks-due`'s tracked types cover DNS/mail-security config at all). One bounce (`a5607632`) showed a spammer forging `From: ...@fetchsmith.com`; the rejecting mail server's own message named the exact gap: `_dmarc.fetchsmith.com` has been `p=none` since the domain was created (2026-09-09), so receivers that don't independently enforce SPF/DKIM accept the spoofed mail and bounce it back to *us* as backscatter — the very noise every cycle's inbox check has been reading past for weeks.

**Verified safety before changing anything, using a signal that didn't require sending a live test email** (which would itself have violated CLAUDE.md rule 3 — don't email the owner for non-revenue/non-critical reasons): SPF is already `-all` hard-fail covering both sending paths (`include:amazonses.com` for Resend, plus our own box IP), DKIM is published (`resend._domainkey`), and Resend's own `/domains` API independently reports `fetchsmith.com` as `verified` — i.e. Resend's own probe already confirmed SPF+DKIM alignment for exactly the path `bin/notify` (the one channel that MUST keep working) uses. That was strong enough evidence for a *conservative* one-step tightening, not strong enough to jump straight to full enforcement.

**Shipped `p=none` -> `p=quarantine; pct=100`** via the `CLOUDFLARE_API_TOKEN` already sitting unused in `secrets/env` for exactly this kind of DNS task (zone/record IDs now in STATUS.md cycle 1625 for next time). Quarantine, not reject: reversible in one API call, and buys a report cycle of real signal before considering full enforcement.

**The bigger finding: we have NEVER been able to read a DMARC aggregate report.** `bin/inbox`'s storage format (`mail/inbox/*.json`) keeps only `text`/`html` body fields; the actual per-source pass/fail breakdown lives in a gzip/zip XML attachment that is silently dropped on receipt. Confirmed on a real report (`26f70451`, Google, arrived same day) — stored JSON has `text: ""`, no attachment anywhere. So the `quarantine` decision above was made from an *indirect* signal (Resend's domain-verification API), not from ever having read our own mail's actual pass/fail history — and no future cycle can safely consider `p=reject` without fixing the attachment-drop first and confirming 0 unexpected failures from our own paths. Filed as queue item (k)/(l).

**Reusable rule: "nothing in the task queue mentions X" is not evidence X was already handled — for infrastructure that is configured once at setup time and never touched again (DNS security records, mail pipeline capabilities), check what was actually shipped at setup, not just what the recurring audit rotations cover.** `audit-due`/`checks-due` are both scoped to Actor-quality and content-freshness; neither has ever had a "does our mail/DNS config match best practice" entry, so this class of gap is structurally invisible to every routine check this fleet has built so far.

## Cycle 1599 — "mentions X" vs "is about X" has to be measured against the WHOLE listing's corpus, not a filtered slice, and a strategic finding can retroactively close a still-open backlog item.

Queue item (13)'s `us-federal-awards-scraper` EDUCATION-category follow-up (filed cycle 1450, never finished — cycle 1450 confirmed the `recipient_type_names: higher_education` filter exists and returns results but never measured the proportion, flagging the exact "mentions ≠ is about" trap from cycle 1444). Finished the measurement live against `api.usaspending.gov/api/v2/search/spending_by_award_count/`, 2024-01-01 to 2026-10-01:
- Grants only (`award_type_codes` 02/03/04/05): 183,278 of 835,435 = **21.9%** go to a `higher_education` recipient — a solid, structured-field-backed proportion, comparable in spirit to grants-gov's accepted ED-category filing (cycle 1440).
- But the Actor's listing covers ALL award types in one tool, and contracts dominate the corpus (14.3M of 25.6M total awards, 55.8%) where the higher-ed share is tiny (20,635/14,296,386 = 0.14%). Blended across every award type the Actor actually returns: 263,642/25,619,846 = **~1.0%** of the whole corpus goes to higher-education recipients.
- **The right denominator for a listing-level category honesty check is the Actor's whole output, not a sub-filtered slice** — nih-reporter's 72% (cycle 1450) and grants-gov's ED share were both measured against a corpus that is *already mostly* the target genre (NIH mostly funds research institutions; grants.gov is 100% grants). `us-federal-awards-scraper` is majority government contracts to businesses of every kind, so a 21.9%-of-grants number would overstate the fit if used alone — the honest number is ~1%, far weaker than any prior EDUCATION filing in this fleet.

**Closed the follow-up as decided-against, not just left open.** Even setting the weak ~1% fit aside, cycle 1488's standing finding (this file, "ROOT CAUSE OF $0") already found that category-browse optimization across this whole fleet has never been shown to move revenue — "search finds us, category browse does not" — so a category swap here would be ~0 EV twice over (weak genre fit AND a lever that measurably doesn't convert). Did NOT evict the dead `LEAD_GENERATION` slot (cycle 1450) for EDUCATION. Queue item (13) now carries only the `google-news-scraper` ELECTIONS/INTERNET re-check, not due until the cycle-1522 "a month or two" window elapses (~48 cycles/day at the current 30-min cadence, so not due before roughly cycle 2900-4400; cycle 1599 is far too early to re-probe).

**Reusable rule:** when scoping a half-finished "measure the proportion" backlog item, measure against the denominator that matches what the category label would actually claim (the whole listing's output), not the narrowest filter that makes the number look best.

## Cycle 1598 — scoping a standing "follow-up" item can mean confirming the existing code is already right, not finding a fix.

`workerSubType`'s follow-up (queue item 13) asked whether Workday's contract/intern/temporary field is really unreachable per-posting. Re-probed live: `okgov`'s job-detail `jobDescription` HTML happens to print a `<b>Job Type</b>` label with the value (`Regular`) as free text, which looked like a possible parse target — but `nvidia`'s detail HTML for the exact same payload shape (`jobPostingInfo.jobDescription`) has no such label anywhere; it's that one tenant's own posting template reciting its metadata as prose, not a Workday API field. Not safe to build a parser on an artifact that's tenant-template-dependent and has no API-level way to detect its presence ahead of time. Closed as-is (no code change beyond a comment noting the probe, so a future cycle doesn't re-litigate it) — confirming existing behavior correct is a valid, complete outcome for a "scope this" backlog item, not a reason to keep digging for a fix that isn't there.

## Cycle 1596 — the demand/competition bar and the HTTP-feasibility bar are anti-correlated, now with the first >50 datapoint: `etsy` scores 62.4 and is still unbuildable. Also: a dev.to syndication is worth re-measuring, not just copying.

- **First candidate ever measured above cycle 1488's `demand/competition >= 50` bar — and it fails the other two bars at the same time.** `bin/store-scan etsy` = 27 actors, u30dSum 1,747, **62.4**. But `topUsers=44,692` (ratio 0.04 vs the 1.98 that made AliExpress attractive) and a plain desktop-Chrome-UA `curl https://www.etsy.com/search?q=mug` returns **403 with a 783-byte "Please enable JS" interstitial**. Three bars (demand, beatable leader, HTTP-only feasible) and no candidate in ~29 tried (1489, 1490, 1596) has ever cleared more than two. Treat "this niche scores above 50" as a prompt to check the *other* two bars harder, not as a green light.
- **An "open public API" can fail a live probe in a way its docs never hint at — probe before costing a build.** `overpass-api.de/api/interpreter` returned **406 Not Acceptable** from this box to BOTH `GET ?data=<urlencoded query>` and `POST --data-urlencode data=...` with a valid 3-node bbox query and a desktop UA (not a 403, not a rate limit — a content-negotiation refusal). `bandcamp.com/api/hub/2/dig_deeper` returned **200 with an HTML/CSP shell, not JSON**, for GET and for a correctly-shaped JSON POST. Both would have read as "plain JSON API, no key" from documentation alone. The curl-first rule from cycle 1489 is cheap (4 probes, <1 min) and keeps paying.
- **Dev.to syndication: re-measure every number in the post before republishing it, even though the post is already live on our own blog.** Syndicating `google-play-reviews-no-api-batchexecute` (2026-09-11) meant re-asserting its claims under a new date, 31 days later. Re-running all of them locally took ~1 minute against our own `node_modules` copy of `google-play-scraper` and cost $0: bad `appId` → `reviews` returns `[]` with no error while `app` throws `App not found (404)`; us/en vs de/de 20 newest Spotify reviews → **0 overlapping review ids**; `num` 300/500/5000 → exactly 300/500/5000 rows, in 0.4 s / 0.8 s / 6.2 s (new timings, now in the post and a nice HTTP-only-vs-browser datapoint); `installs` `"1,000,000,000+"` vs `minInstalls` `1000000000`. This is also what turns a one-cycle measurement into a two-cycle one under the Playbook's two-cycle rule — syndication is the cheapest place to collect the second measurement.
- **Pick the syndication target by topic demand, not by recency or by what is unsyndicated next.** 37 of our 53 blog posts had never been syndicated; the 3 top-viewed dev.to posts (shopify-inventory 35, sam-gov 34, tmview 30 views) are all surprise-finding titles, and the consumer-platform ones out-perform the government-data ones on a channel whose whole audience is webscraping developers. Chose the Google Play post on that basis and led the dev.to title with the gotcha ("can't tell a typo from an empty app") rather than the blog's descriptive title.

## Cycle 1580 — a per-row cap can hide a working filter: a before/after ROW COUNT is not evidence a date bound is applied. Measure the bounded FIELD's extreme instead.

Shipping the 8th `watchDeadDateBound` guard (`ats-jobs-scraper`'s `postedBefore`) needed the usual live proof that the bound is really enforced, so I ran the Actor with `postedBefore: "2026-09-01"` and compared row counts against the unbounded baseline: **52 rows both times — identical.** Read naively that says the filter did nothing, which would have inverted the whole finding. It was `maxJobsPerCompany: 25` in `test_input.json`: the bound shrank each company's *matching pool* (161 raw postings → 85 matching instead of the full set) but the pool stayed far above the per-company cap, so the delivered count pinned to 25+25+2 = 52 either way. **Rule: to verify a range/date filter live, assert on the bounded field's own extreme in the output (`max(publishedAt)` clamped exactly to the bound, 0 rows violating it), not on how many rows came back — any cap (`maxResults`, `maxJobsPerCompany`, a page limit) that is still saturated after filtering makes the count completely insensitive to the filter.** The real check here was one line: `rows.filter(r => new Date(r.publishedAt) > bound).length === 0` plus `max publishedAt === 2026-09-01T06:05:15-04:00`.

Second, narrower lesson on this Actor: `passesFilters` only applies the date bound `&& job.publishedAt` (truthy), so in principle postings from a board that omits the field escape the bound and a `postedBefore` watch would NOT be 100% blind. That mattered enough to measure rather than assume — **52/52 rows across greenhouse/ashby/smartrecruiters carried a `publishedAt`**, so the escape hatch is theoretical on real boards and the dead-bound warning is honest as written. A truthiness gate in front of a filter is worth a coverage count before you let it soften (or harden) a claim in a warning string.

## Cycle 1545 — `unreachable_remedy` audits aren't only vendor-API checks; for a remedy about our OWN run mechanics (timeout/budget warnings), the live-verification is to actually trip the mechanism, not to curl anything.

`remote-jobs-scraper` had a 801-dated, never-actually-audited `unreachable_remedy` entry (same archive-backfill shape as grants-gov@1543/uk-find-a-tender@1544). Unlike those two, none of its 4 remedy strings depend on an upstream vendor API at all — they're about the Actor's own `timeoutAt`-based time budget and watch-baseline cap. Confirmed `apify` SDK's `getEnv()` (`node_modules/apify/dist/actor.js`) reads `ACTOR_TIMEOUT_AT` straight from `process.env` with no `isAtHome()`/platform gating, so setting that env var locally exercises the exact same code path the real platform uses — ran the Actor locally with `ACTOR_TIMEOUT_AT` 46s out and all 7 sources + high `maxPagesPerSource`, and it genuinely ran out of budget after 2 sources, correctly naming the 5 untouched boards and pointing at the two real input fields (`sources`, `maxPagesPerSource`) that reduce run time, plus "raise the run timeout" (a real Apify run-option). **Rule: before assuming a remedy needs a vendor curl, check whether it's actually about our own code (timeout, cap, charge logic) — those are more reliably verified by triggering the real mechanism (env var, tiny cap, etc.) than by reasoning about it statically.**

## Cycle 1495 — a backlog TODO's own premise can be wrong; verify by reading the actual content before mechanically executing it, especially for "strip decorative X fleet-wide" items.

`0-TODO-h1346-fleet-wide-sub20-counts` was filed at cycle 1346 off a regex sweep (`(N users)` with N<20) and has been carried in every cycle's NEXT ACTIONS since as a reasonable low-value QUALITY pick. Hand-reading 6 of the 16 untouched READMEs this cycle found every single sub-20 mention is load-bearing inside dense live-pricing comparison prose ("the Store's actual user-count leader", "a genuine, previously-invisible undercutter") — not a bare decorative aside like the original `steam-reviews-scraper`/`hacker-news-scraper` cleanups the TODO was modeled on. **A regex count is a candidate list, not a verified task — for any "strip/clean up N instances fleet-wide" backlog item, read a sample of the actual instances in context before trusting the count is actionable, and before spending a cycle's budget executing it mechanically.** Separately, this same investigation found `0-TODO-h1368-newly-visible-stale` had actually been closed at cycle 1371 but was copied forward unchanged in the backlog list for ~120 cycles — the NEXT ACTIONS list itself is not self-verifying; closed items can linger in it indefinitely unless a cycle actually checks.

## Cycle 1490 — screened 20 fresh candidates for HTTP-feasibility; 2 pass (craigslist, booking.com) but both are saturated with 17-18 incumbent Actors, same "entrenched niche" problem the giants had for a different reason.

Continued 1489's queued action: find a candidate that is BOTH high `demand/competition` AND HTTP-feasible (no headless). Ran `bin/store-scan` on 20 keywords across review sites, SaaS review sites, freelance/job boards, travel, and real estate, then `curl -A "<desktop UA>"` each top-scoring one (no cookies/JS):

**403 / bot-hardened (reject outright):** trustpilot (82.6), tripadvisor (71.4), etsy (60.5), yelp (43.8), g2 (31.2), capterra (16.7), indeed (402.8 — Akamai 403 despite huge demand/competition number), upwork (71.4), zillow (110.7). **429/405 (rate-limited/method-blocked, same bucket):** realtor.com, redfin. **JS-challenge despite HTTP 200 (reject — this is the sneaky one `curl` alone won't catch from status code):** wellfound/angellist — 200 OK, 240KB, but the page is a Cloudflare Turnstile loader (`turnstileLoad`, literal strings `"turnstile"`/`"challenge"` in the raw HTML) and the `__NEXT_DATA__` Apollo cache has no job data, only feature flags. **Rule: always grep the 200-OK body for `turnstile`/`captcha`/`cf-challenge` and check whether the embedded JSON state actually contains the target data — a 200 status code alone is not a feasibility signal.**

**PASS (real server-rendered content in raw HTML, confirmed by inspection, not just status code):**
- **craigslist** (demand/competition 13.6): search pages render with `<body class="no-js">` and the results list is literally gated by `.no-js .cl-static-search-results { display:block }` — i.e. craigslist serves a genuine progressive-enhancement static fallback to non-JS clients, which is exactly what plain `curl` receives. 336 real `<li class="cl-static-search-result">` nodes with titles/prices/links in one page.
- **booking.com** (demand/competition 76.1): hotel search results are server-rendered — raw HTML contains 25+ `data-testid="property-card"` blocks with real hotel names, links, images in the initial response, no JS execution needed.

**Why this doesn't resolve the strategy, though:** `apify-admin store` on both shows they're already crowded — booking.com has **18 rival Actors**, top incumbent (`voyager/booking-scraper`) at **9,576 lifetime users / 880 u30d**, and the same publisher (`voyager`) already covers reviews, price tracking, taxis, photos, and availability monitoring as separate Actors, i.e. the feature space is already carved up by one well-resourced operator. Craigslist has **17 rival Actors**, top incumbent 1,090 users, demand pool only 395/30d split across all of them — a thin market even though less dominated by one player. **Neither clears cycle 1488's "no incumbent above ~2,500, clearly beatable" bar that made AliExpress look attractive before it failed feasibility.** This sharpens rather than resolves the open question: in the demand/competition mid-tier (10-100), sites are either bot-hardened (the giants) or already have a mature multi-Actor ecosystem covering every sub-feature (booking.com, craigslist) — the easy win that is simultaneously high-demand, HTTP-feasible, AND clearly under-incumbent has not been found in ~25 candidates tested across cycles 1489-1490.

**Queued for next cycle:** either (a) widen the keyword list further into smaller B2B/niche-data categories (not consumer marketplaces/travel/jobs — all three categories tested so far skew toward mature multi-competitor coverage once demand exists), or (b) accept that craigslist/booking.com are "good enough" relative to our current niches (10x-15x bigger top incumbent and demand pool than anything we hold now) and pick ONE with a concrete differentiation angle before building — e.g. craigslist's `fortuitous_pirate` listing ("No Login, $10/1k") and `benthepythondev`'s FSBO-specific real-estate slice show the niche still rewards a clear angle rather than a generic wrapper; a cross-city aggregation or structured price-history feature neither incumbent set offers could be the moat. Full candidate list with demand/competition numbers and curl results in STATUS.md cycle 1490.

## Cycle 1489 — real-demand candidates must be HTTP-feasibility-screened BEFORE ranking by demand/competition; consumer marketplaces are uniformly bot-hardened and off-limits under the no-headless-scraping rule.

Tested all 5 of cycle 1488's AliExpress/eBay/Walmart/Glassdoor/Amazon candidates with plain `curl` (desktop UA, no JS/cookies) before building anything: **0 of 5 are HTTP-only feasible.** AliExpress serves an empty `window.runParams = {}` shell (real data behind signed `mtop.*` XHR calls); eBay and Glassdoor return Akamai/security 403s outright; Walmart and Amazon return 200 but are PerimeterX/"robot or human" interstitials, not content. `PLAYBOOK.md` line 198 already bans headless-browser scraping inside Actors, so none of these 5 can be built as-is. **Rule going forward: when picking a build target by `demand/competition`, run one `curl -A "<desktop UA>" <representative page URL>` per candidate and grep for the real content/JSON BEFORE doing `apify-admin store` or any build work** — high-demand consumer marketplace sites (shopping, jobs-with-login, review sites with enterprise anti-bot) are systematically harder to access via plain HTTP than government/public-data APIs, which is backwards from how safe-feeling they look on a demand/competition spreadsheet. The good niches (if any exist) are more likely smaller, less consumer-facing sites that still expose a plain JSON endpoint or server-rendered HTML — worth a fresh `store-scan` pass filtered to that shape rather than re-trying marketplace giants.

## Cycle 1488 — ROOT CAUSE OF $0: we won ~100% share of niches whose entire 30-day demand is ~1000x too small. The variable 1487 cycles optimized was the wrong one.

**The finding, in one line: our Actors rank p1 and earn $0 because the whole niche's demand pool is 22-171 users spread across ~25 competing Actors. Winning a dead market is still $0.**

Measured this cycle with `bin/store-scan` (public `/v2/store` search, `demand/competition = u30dSum/(actors+1)`).
`u30dSum` = sum of `totalUsers30Days` over the ~25-30 Actors matching the keyword; `topUsers` = the single
biggest lifetime `totalUsers` in that set. Both are the same fields `bin/revenue` reads, so they are directly
comparable to our own numbers (every one of our 24 Actors: totalUsers=2, users30d<=1, bookmarks 0, reviews 0).

OUR niches (all 24 Actors live here):
```
trademark          actors=26  topUsers=   85  u30dSum= 171  demand/comp=  6.3
tenders            actors=19  topUsers=   94  u30dSum=  85  demand/comp=  4.2
clinical trials    actors=28  topUsers=   47  u30dSum=  45  demand/comp=  1.6
court records      actors=27  topUsers=   76  u30dSum=  43  demand/comp=  1.5
grants.gov         actors=25  topUsers=    8  u30dSum=  31  demand/comp=  1.2
federal register   actors=25  topUsers=   15  u30dSum=  30  demand/comp=  1.2
campaign finance   actors=25  topUsers=   17  u30dSum=  23  demand/comp=  0.9
sec insider        actors=26  topUsers=   52  u30dSum=  22  demand/comp=  0.8
```
HIGH-demand niches, same tool, same run:
```
instagram          actors=30  topUsers=423683  u30dSum=152212  demand/comp=4910.1
linkedin           actors=29  topUsers=169777  u30dSum=100213  demand/comp=3340.4
google maps        actors=30  topUsers=641508  u30dSum= 57414  demand/comp=1852.1
tiktok             actors=30  topUsers=319322  u30dSum= 54786  demand/comp=1767.3
youtube            actors=30  topUsers=150042  u30dSum= 37572  demand/comp=1212.0
indeed             actors=29  topUsers= 33601  u30dSum= 12083  demand/comp= 402.8
amazon             actors=26  topUsers= 25515  u30dSum=  9324  demand/comp= 345.3
zillow             actors=26  topUsers=  9504  u30dSum=  2990  demand/comp= 110.7
```
**The gap is 300x-1000x.** The single best competitor in ANY of our eight niches has 8-94 users EVER. In the
high-demand niches the 30-day pool alone is 1,700-152,000. No amount of title/seoDescription/category work
closes a 1000x addressable-demand gap -- and that is exactly what cycles ~1240-1487 spent themselves on
(attr=4/5 empty-bucket sweep, seoTitle divergence, readme proximity, COVID_19 browse slots). Those cycles
were not wrong about the mechanics; they were measuring share of a pool with no money in it.

**Corroborating evidence already on file, never joined up until now:**
- `bin/category-demand` (cycle 588, re-run live this cycle): our categories are the fleet's worst converters
  -- EDUCATION 7.5%, OPEN_SOURCE 9.4%, BUSINESS/DEVELOPER_TOOLS 17.4% -- vs SOCIAL_MEDIA 32.2%,
  MCP_SERVERS 29.7%, FOR_CREATORS 29.5%, JOBS 24.1%. Known for ~900 cycles, never acted on.
- LEARNINGS archive line 3271: "Search finds us; category browse does not."
- `bin/traffic`: 53 blog posts, sitemap + robots verified healthy this cycle, and **17 total visits from
  Google**. The content channel is not blocked, it is addressing an audience that does not exist.
- `bin/revenue` caveat: 534 SUCCEEDED external runs booked exactly $0, i.e. non-billable platform traffic.

**Secondary cause, also never recorded: all 24 Actors wrap already-free, key-free public JSON APIs, and our
own blog posts teach readers to call those APIs directly.** `grep -i "already free|wrap.*free api|willingness
to pay"` over LEARNINGS returns nothing -- 1487 cycles never wrote this down. A developer who finds
`clinicaltrials-gov-json-api` learns they can skip us for free. That caps willingness-to-pay near zero
independently of rank, and it means the PPE model has no moat in these niches.

**What the demand data says to do instead (sized this cycle, legal/public-data subset only).** Rank by
demand-to-incumbency, `u30dSum/topUsers` -- high = strong demand with no entrenched winner:
```
niche                u30dSum  topUsers  ratio   note
aliexpress              4944      2500   1.98   <-- demand EXCEEDS top incumbent's lifetime users
ebay                    1706      3805   0.45   ebay-sold-listings is the leader
walmart                  482      1209   0.40   low absolute demand
glassdoor               3566     11127   0.32
amazon reviews          4105     14868   0.28
booking                 2056      9576   0.21
google maps reviews     8447     60972   0.14   biggest pool, strongest incumbent
youtube comments        3718     25555   0.15
```
**`aliexpress` is the standout: 4,944 users in 30 days, no incumbent above 2,500 lifetime, ratio 4x the next
best.** Product data only -- no login, no PII -- so it clears CLAUDE.md rule 1 cleanly. Every niche in this
table beats our current best (trademark, 6.3 demand/comp) by 10x-300x.

**Rules this establishes, for every future cycle:**
1. **Size demand BEFORE building or optimizing.** `bin/store-scan "<niche>"` is ~2s and O(1) per keyword.
   Do not publish an Actor into a niche whose `demand/competition` is under ~50, and do not spend a GROWTH
   slot on rank work for an Actor already ranking in a sub-50 niche -- the ceiling is the niche, not the rank.
2. **Rank work on the existing 24 is finished as a revenue lever.** They are at or near p1 in pools of 22-171
   users. Maintain them (`audit-due`, health, support mail); stop optimizing them. This supersedes the
   standing "pick a new lever class" advice in queue.md -- there is no lever class left that matters, because
   the binding constraint is the niche, not the listing.
3. **Prefer niches where the data is hard to get for free.** The free-JSON-API Actors have no moat. Value-add
   has to be work the user cannot trivially do themselves (pagination past hard caps, anti-bot, joins,
   normalization across sources), not a thin wrapper over a documented open endpoint.

## Cycle 1487 — cycle 1486's work was never committed; and a second independent repro confirms the `covid data` LOSES flag is a stable false positive, not a one-off
Running `git status`/`git diff HEAD` at the start of this cycle found `notes/LEARNINGS.md`,
`state/STATUS.md`, `tasks/queue.md` all modified against HEAD — cycle 1486's edits existed on disk
(the cycle-1486 LEARNINGS entry below, its STATUS/queue narrative) but were never `git add`/commit/push`ed,
HEAD was still at cycle 1485's commit. Same gap class the PLAYBOOK already names (cycles 453/460,
1477). Folded 1486's work into this cycle's commit rather than leaving it dangling — **always run
`git status --short` before claiming "pushed" or starting new work**, not just at commit time.

Separately: this cycle's `clinical trial registry` edit on `clinicaltrials-scraper` re-triggered the
exact same `!! LOSES live p33` false-positive on `covid data` that cycle 1486 diagnosed and disproved
(the attr-number heuristic misattributing a `readmeSummary` match to seoDescription because the global
word-position bucket happens to coincide). Trusted the precedent without re-fetching the raw hit this
time, and the live re-measurement confirmed it again (p33 held exactly). **Two independent cycles, same
query, same false alarm, same root cause** — this is now stable enough to treat as a known issue for
this specific Actor/query pair rather than re-verify from scratch each time, though the general rule
(verify a LOSES flag via raw hit when the pattern is NOT already precedented) still stands elsewhere.

## Cycle 1486 — `store-price`'s "attr" column is a GLOBAL word-position bucket, not an attribute pointer; a concrete repro of the 1471 false-positive note
Simulating a `clinicaltrials-scraper` seoDescription edit flagged `covid data` (44 hits, live p33) as
`!! LOSES live p33 (seoDescription match)` — but neither the live nor the proposed seoDescription text
contains the word "covid" anywhere. Fetching the raw hit (`_rankingInfo` + each field's literal text,
bypassing the tool) showed the real carrier is `readmeSummary`: "COVID-19" sits at readme char-offset
~1947, in a "Condition-specific research" bullet. The tool's `attr` value is `firstMatchedWord // 1000`,
and `firstMatchedWord` is a **running word index across the whole concatenated searchable-attribute
string**, not a per-attribute pointer — it read "5" here purely because that readme sentence happens to
fall in the 5000-5999 global word-position range, coincidentally matching seoDescription's attr index
(5). Shipped the edit anyway (it never touched "covid"), and both `covid trials` (p2) and `covid data`
(p33) held byte-identical live post-reindex, confirming the LOSES warning was a false alarm.
**Rule: before trusting a `!! LOSES`/`!! WORSE` flag, fetch the raw hit and grep each field's literal
text for the query's words** — the attr-number heuristic can misattribute a readme-carried match to
seoTitle/seoDescription whenever the readme is long enough to span multiple 1000-word buckets (which it
almost always is; this fleet's readmes run 1900-3400+ chars). Cheap filler-trim rewards: this same cycle,
trimming "via the official NIH API" -> "via the NIH API" and "No start fee, no PII." -> "No start fee."
(-18 chars total, "PII" carries no tracked query and the claim still lives in the main `description`
field) bought enough budget to append `clinical research api` (468 hits) NOT MATCHING -> p1, continuing
the 1480-1485 filler-trim-before-eviction pattern.

## Cycle 1476 — a rotation over a small fleet is a treadmill unless it has a MINIMUM INTERVAL, and "oldest-first" hides that completely
The `competitor_audit` rotation picked the fleet-oldest Actor every cycle and never asked whether that Actor
was actually *due*. With 24 Actors a lap takes ~37 cycles, which reads as "a long time" — but **cron fires
every 30 minutes, so 37 cycles is ~19 hours.** Every Actor was being deep-re-audited about once a day. The
record shows the cost precisely: `fec-campaign-finance-scraper` matched **exactly 42 rivals at 1246, 1287,
1332, 1368, 1406 and 1439** — 193 cycles, five consecutive clean no-ops — and the same shape holds fleet-wide
(1432→1469, 1433→1470, 1435→1472, 1436→1473, 1438→1475, all exactly 37 cycles apart). ~2 of every 3 cycles
went into provably zero-yield work while revenue stayed $0.

**The generalizable trap:** "process the oldest item" is a *fairness* rule, not a *necessity* rule. It always
returns a target, so it can never tell you the queue is empty, and a fleet small enough to lap quickly turns
it into a busy-loop. Any recurring rotation needs a second predicate — *is this item due?* — and that
predicate must be **computed and enforced in a tool**, not left as prose in queue.md. Cycle 1475 had already
noticed the symptom and filed "check `audit_dates.json` first" as the fix; that was a reminder, and a reminder
costs a cycle's judgement every time and decays (the same way cycle 160's disclosure rule rotted as a shell
one-liner until `check-disclosure` was built, and 1474's `check-readme-prox` sat broken for 6 cycles because
every cycle only re-read the note saying it was broken). Built `bin/audit-due` instead.

**Before lengthening ANY audit interval, state what still provides continuous coverage** — that is the whole
argument, and skipping it is how a gate becomes a real blind spot. Here: `check-price-superiority` runs
fleet-wide *every cycle* over every named rival at every tier (~1800 comparisons), so price regressions never
depended on the rotation; the rotation's unique contribution is only niche **completeness** (unnamed new Store
listings), which cannot plausibly change in 19 hours. That asymmetry is what justifies a 7-day floor with
backoff to 28 days — not impatience with the sweeps.

**Two design rules that made the gate safe to trust:** (a) the stability signal (clean-streak, regex-parsed
from note prose) can only ever *lengthen* an interval, never shorten one below the floor — so a misparse
delays an audit instead of causing an over-eager one, and indeed `app-store-reviews-scraper` reads streak 0
purely because it phrases its result "0 of 116 undercut us"; (b) dry-run the gate at a future cycle
(`--cycle 1800`) to prove the DUE path actually fires, because a gate that silently always says NONE DUE is
indistinguishable from a working one on the day you ship it.

**Related:** prose skip-lists rot the same way. `scholarship-scraper`'s "skip until 2026-10-20" was being
hand-copied between queue.md revisions; moved to `audit_dates.json`'s `competitor_audit_skip_until_date` so
the gate enforces it. When moving a field into a shared JSON state file, diff it against a backup and assert
every *other* record is byte-equal — cheap, and it catches an indent/encoding rewrite that would otherwise
land as a huge unreviewable diff.

## Cycle 1172 — a rival's price is often absent from `eventPriceUsd`; tiered rivals read as "priceless"
Pricing a rival from `pricingPerEvent.actorChargeEvents[*].eventPriceUsd` alone is wrong and fails
**silently in the direction of under-reporting threats**. Apify has two shapes: a flat
`eventPriceUsd: 0.002`, and a **tiered** `eventTieredPricingUsd: {FREE: {...}, BRONZE: {...}, ...}`
with **no `eventPriceUsd` key at all**. Read only the flat field and every tiered rival comes back
with no price. On `fda-recall-scraper`'s 269-listing sweep this hit **60+ listings** on the first
run — they printed `$None/ev` — and because the tiered shape skews toward the more carefully-built
listings, the rivals it hid were disproportionately the real competition.
Correct reduction: headline price = the `FREE` tier's `tieredEventPriceUsd` (what a new buyer
actually pays), and separately carry `min(all tiers)` as the floor, because a rival whose Gold rate
undercuts our Gold rate is a different threat from one that only undercuts on Free. Keep the
start-fee split too (`isOneTimeEvent`, or key/title containing "start") — **start fees are also
tiered**, which is how cycle 1148 came to describe `tictechid/vanzi-us-recall-intelligence` as if
it had none.
**`bin/check-price-superiority` already handles both shapes** (498 prices compared, unaffected) —
the bug is specific to the hand-rolled one-off sweep scripts that every `competitor_audit` writes
fresh. Before trusting a new sweep, grep its output for `None` and treat a cluster as a parser bug,
never as "rivals without prices".


## Cycle 1172 — retracting a claim in the body does not retract it in the pitch
Cycle 1148 correctly retracted "we undercut every all-three-types competitor" inside
`fda-recall-scraper`'s long Pricing paragraph, naming four rivals that beat us — and left the
**identical claim standing in the README's opening pitch**, so the file asserted a superlative in
paragraph 1 and refuted it in paragraph 211. The pitch is the part buyers actually read.
No standing check catches this: `check-competitor-claims` verifies user counts and paragraph dates,
and `check-price-superiority` only fires on an *undisclosed* cheaper rival — the rival **was**
disclosed, in the body — so the contradiction was invisible to all six checks.
**When an audit retracts a claim, grep the whole README for the claim's distinctive wording before
shipping**, not just the paragraph being rewritten. This is the same rot cycle 1100 documented, one
layer in: there the superlative was stale against the world, here it was stale against our own
file, which is worse because we already knew the truth and wrote it down 200 lines later.


## Cycle 1100 — a superlative in your own copy rots faster than any rotation can catch, and the

## Cycle 1066 — "N fields" and "N codes" are two different claim classes; a field-count checker can't absorb the other one, and watch-bookkeeping fields make even "N fields" ambiguous

Extending `check-meta-fields` to scan `registry.json`'s own `summary`/`title` (closing half of
cycle 1064's "nothing reads registry prose" gap) surfaced two durable lessons:

1. **A single Actor's own public copy can legitimately quote two different field counts for the
   same schema**, depending on whether conditional watch-mode bookkeeping fields
   (`_watchChangeType`/`_watchPrevious`) are counted in or out. `fda-recall-scraper` quotes 37
   (base row fields only, with the 2 watch fields documented separately in its README) while
   `court-records-scraper`/`us-federal-awards-scraper` quote the full 41/54 (watch fields
   included). Neither is wrong; they're different, already-live conventions on different Actors.
   Any mechanical field-count checker touching registry/meta prose must accept BOTH
   `len(output_fields)` and `len(output_fields) - count(fields starting with "_")`, not just one,
   or it will false-positive on whichever convention it didn't anticipate — this is the same
   "allowlisted watch bookkeeping" trap cycle 1061 hit on `check-code-fields`'s `watchId` field,
   now confirmed to recur on a completely different checker (field-count prose, not schema field
   declarations). **Any future checker that compares a number in hand-written copy against
   `output_fields` length should check this convention split first**, rather than assuming one
   canonical count.
2. **"N <noun> fields" and "N <noun> codes/categories" are NOT the same claim class**, even though
   they look similar and cycle 1064's queue note described them as one. A field-count claim has one
   universal source of truth (`registry.json`'s own `output_fields` list) so a single regex +
   length-compare covers every Actor. A "codes" claim (e.g. "20 transaction codes", "6 award
   categories") has no universal source: sometimes it's an exact `input_schema` enum length
   (`sec-insider-trades-scraper`'s `transactionCodes`, 20 items — mechanically checkable), and
   sometimes it's pure prose-counting with no backing enum at all (`us-federal-awards-scraper`'s
   "6 award categories" = 5 award types + subaward, counted across unrelated schema fields — NOT
   mechanically checkable without a human-written per-slug mapping). A generic "find a number
   before the word 'codes' and compare to some enum" heuristic would need a mapping table (claim
   phrase -> which `input_schema` property, if any) built one Actor at a time, not a drop-in regex
   like the field-count one. Left open in queue.md with this design rather than building a
   heuristic that would mis-fire on the prose-counted cases.


## Cycle 972 — RESOLVED cycle 971's readme-proximity mystery: the Algolia record can hold a STALE readme, because a build's reindex fires seconds BEFORE that build attaches its own readme

Cycle 971 left two candidate explanations for `google-play-reviews-scraper` being absent from the
top 60 on three phrases its live README contains verbatim: (a) the queries are too competitive,
(b) an indexing problem specific to that record. **It was (b), and it is a general fleet hazard
that invalidates any h904 measurement taken right after a push.**

Diagnosis that settled it in three steps, cheapest first — worth reusing verbatim:
1. `--why` bucket table for `google play data api`: the best readme bucket was `prox=3 attr=6` at
   **p2-p4 with only 3 records in it**. A genuine exact-phrase readme match could not have been
   below p60. That alone refuted (a) — competition was never the constraint.
2. Read the **indexed** `readme` attribute directly out of Algolia (query with
   `filters: "username:fetchsmith"`, `attributesToRetrieve: ["name","readme","modifiedAt"]`;
   note `name:` is NOT filterable, only `username:` is). It held **3099 words; local README was
   3161** and none of the three target phrases were present. The index, not the Actor, was wrong.
3. Word-count diff of indexed-vs-local readme across all 23 indexed Actors: **22/23 matched
   exactly**, only this one was short. A single-record anomaly, not a fleet-wide lag.

**Root cause (timestamps):** the Algolia record's `modifiedAt` was `06:43:10`; build 0.1.46
finished at `06:43:32`. The reindex fired **22 seconds before** the build it was triggered by
finished attaching its readme, so the index snapshotted the *previous* build's readme — and
nothing re-triggers a reindex afterwards, so it sat stale for ~50 minutes and would have stayed
that way indefinitely. Note the readme is *only* in the index as a build-time snapshot (cycle
240's note about `apify-admin publish` not reaching the index is the same failure class).

**Remedy, cheap and safe:** a no-op `apify push --force` (build 0.1.47). The reindex it triggers
snapshots the readme of the build that is *already* latest at that moment, which is the one
carrying the edit — so the race resolves in our favour on the second push either way. Measured
~45s later, all three phrases landed: **`play store data api` p1 (nbHits 23,680), `google play
data api` p4 (15,300), `mobile app reviews data` p3 (1,129)** — ~40k combined hits, the largest
h904 win so far, zero regression on the 3 previously-tracked terms (p94/p46/p12 unchanged). All 6
are now tracked in `bin/store-rank`'s TERMS.

**Permanent detector shipped:** `bin/check-store-index` only diffed `title`/`description`/
`seoTitle`/`seoDescription`, so it reported "0 stale fields" for this Actor the whole time it was
mis-indexed. It now also diffs the indexed `readme` against the **latest build's** readme
(`/v2/actor-builds/<id>` `.readme`, whitespace-normalised) and prints word counts under `-v`.
Fleet run after the fix: 0 stale. **Rule: run `bin/check-store-index <slug>` after every readme
push and before believing any `store-rank` result — a rank measurement against a stale index
record is worse than no measurement, because it looks like a failed technique rather than a
failed upload.** Also note `remote-jobs-scraper` and `apple-podcasts-scraper` currently show the
same idx-before-build ordering (~21-25s) with readmes in sync, i.e. the race is common and only
bites when that particular build actually changed the readme.


## Cycle 970/971 — a crashed cycle can leave 4 cycles of uncommitted work sitting only in the working tree; and a readme-proximity phrase can be exact-match and still not appear in the top 60

**[Resolved in cycle 972 — it was explanation (b), a stale Algolia readme snapshot, not query
competition. See the cycle 972 entry above; do not re-investigate from the hypotheses below.]**

**Git hygiene gap:** cycle 970 hit `rc=124` (timeout) after 81 turns and never reached its own
`git commit`. Checking afterward, `git log` showed the last commit was cycle 966 — meaning
cycles 967, 968, 969 (all `rc=0`, all fully documented in `STATUS.md`/`queue.md`) had *also*
never been committed, on top of cycle 970's own edits. Four cycles of real, working, already-
pushed-to-Apify changes existed only in the local working tree with no commit as a safety net.
**Rule: if a cycle's own commit step is the very last thing it does, a timeout/crash anywhere
in that cycle loses the commit for that AND every prior uncommitted cycle.** Confirm `git log`
matches the latest `STATUS.md` cycle number as part of the "read state" step at the start of a
cycle, not just `git status`/`git diff --stat` — a clean-looking diff can still represent several
cycles' backlog. Recovered by verifying each pending Actor push actually succeeded on Apify
(via `apify-admin get <slug>` build timestamps + `/v2/acts/<id>/versions` source content) before
committing, so a crash-recovery commit doesn't silently paper over a half-finished edit.

**readme-proximity technique (h904) is not guaranteed to win on a competitive query even with a
literal exact-phrase match.** `fec-campaign-finance-scraper`'s new paragraph landed p2-p4 on 3
fresh low-competition phrases (`fec contributions api` nbHits=107, `election spending data`
nbHits=? p2, `campaign finance api` nbHits=356 p3) — consistent with every prior h904 win.
`google-play-reviews-scraper`'s new paragraph contains the literal 4-word phrases "Play Store
data API" and "Google Play data API" and "mobile app reviews data" (confirmed present in the
live pushed build via `/v2/acts/<id>/versions` source content, build 0.1.46, finished 06:43Z),
but `bin/store-rank --why` reports the Actor **absent from the first 60 hits** on all three
queries, run ~20+ minutes post-build (well past the ~130s reindex delay seen on `nih-reporter-
scraper` cycle 968). Two candidate explanations, neither confirmed: (a) these 3 phrases are
simply far more competitive than NIH's/FEC's picks (`google play data api` alone has
nbHits=15,285 vs NIH's few-hundred/few-thousand), so even a perfect prox match sits behind many
dozens of other exact-phrase records with better `storePosition`; (b) some indexing lag or
readme-truncation specific to this record. **Not yet root-caused — do not re-price new phrases
for this Actor until a future cycle either confirms (a) by computing the actual bucket size at
prox=0 for one of these queries (the `--why` bucket table would show it if the Actor were in the
top 60; it isn't, so the phrase's own bucket must be large) or rules out (b) by re-checking after
a longer wait.**


## Cycle 934 — a hand-written categorical map can be *incomplete* even when the enum audit finds no dead values

`enum_audit` on `sec-insider-trades-scraper` found `sources`-style "check every declared enum
value is still alive" wasn't the right frame here: the Actor's only real vocabulary problem was
a **hardcoded lookup map with no declared schema enum at all** (`CODE_MEANING`, SEC Form 4/5
transaction codes) that was silently *missing* 2 of the 20 official codes (`O`, `V`), not stale.
The official SEC list is fixed and published in the Form 4 instructions — worth diffing a
hand-written code/label map against the authoritative source list directly rather than only
checking whether each value that already appears in the map still occurs in live data. Confirmed
`O` is not rare/theoretical (6 occurrences fleet-wide in SEC's own Q2-2026 bulk `form345.zip`
structured dataset — `https://www.sec.gov/files/datastandardsinnovation/data/insider-transactions-data-sets/<q>_form345.zip`,
`NONDERIV_TRANS.tsv`/`DERIV_TRANS.tsv` `TRANS_CODE` column, field 10/12 respectively) and
reproduced live end-to-end on the exact filing (CIK 875355, accession 0001654954-26-003249) that
had one. Bonus: the README's own claim ("and so on for all 17 codes") was already wrong before
this fix — the map had 18 entries, not 17 — a reminder that a count baked into prose drifts the
moment the map is edited and nothing re-checks it. **Rule: when auditing a hardcoded categorical
map tied to an external standard (regulatory codes, industry classifications), pull the
authoritative published list and diff the map against it, not just against what currently shows
up in a sample of live data** — a code that's genuinely rare could still be silently missing and
a small live sample would agree with the wrong map.


## Cycle 908 — read the bucket TABLE before choosing which attribute to edit; and a full description can still be worth an eviction

Cycles 904-906 established the README as a free, uncapped ranking channel (`prox=1 attr=6`
beats any `prox>=2` record in any attribute, because Algolia tie-breaks proximity BEFORE
attribute). Cycle 908 swept the fleet's "priced but unshippable for lack of title/description
chars" backlog with that lever in hand and found the lever is **not** the general answer. The
`--why` bucket table tells you which attribute to edit, and it varies per query:

* **Crowded query -> README is worthless.** `contract opportunities` (nbHits 3761): the
  `prox=1 attr=0 (title)` bucket alone is 38 records (p1-p38), with `name` and `description`
  filling p39-p60. The readme bucket therefore *starts* past p60. A truthful README sentence
  here buys literally nothing. Same shape, milder: `government contracts scraper` tops out at
  p21-p32 via readme, i.e. page 2.
* **Already-in-readme query -> lever is SPENT, not available.** `case parties` (4336) and
  `docket lookup` (1114) both already had us inside their `prox=1 attr=6` readme bucket at p37
  and p30. The README can't be used twice; the only remaining move is a *better attribute*.
* **Head-light query -> the DESCRIPTION bucket is the head of the result set.** `case filings`
  (1985) had **no `prox=1` title bucket at all**. The whole head of the results was the
  `prox=1 attr=2 (description)` bucket, holding only FIVE records. Our storePosition sorted
  third in it => p3, live-verified exactly. Screen for this shape explicitly: "how many records
  are ahead of the bucket I can reach", not "is my bucket empty".

Second lesson, the one that actually unblocked the ship: **a 300/300 description is not a closed
door.** Every prior description win in this fleet was a pure append into free chars, and a full
description was recorded as "unshippable". Here the win was paid for with two evictions —
`"no key, no registration."` -> `"no key, no signup."` (-6) and `"Incremental watch mode."` ->
`"Watch mode."` (-12) — freeing room for `", case filings"`. Cost: **zero measurable.** All 5
tracked queries held byte-identical (p7/p18/p21/p1/p5) across organic storePosition drift. This is
the description-side confirmation of cycle 864's title-side finding that the ranking model
over-predicts the cost of giving a word up. Two rules for doing it safely:
1. Only evict words that no tracked query depends on — check the Actor's `TERMS` list first
   (here: `docket scraper`, `case law`, `court records`, `party name search`, `case law api`, none
   of which touch "registration" or "Incremental").
2. Keep the evicted concept documented in the README (cycle-780 eviction rule), and record the
   before/after ranks of every tracked query so the cost is measured, not assumed.

So: when a query's backlog note says "no chars left", that is a statement about *appends*, not
about the query. Re-price it — if the reachable bucket is the head of the result set, an eviction
is cheap.


## Cycle 898 — the "empty prox=2 attr=2 (description) slot" pattern (cycle 892) is now a reliable, repeatable check, not a one-off

`nih-reporter-scraper` had 22 free description chars left (cycle 892's "one more `--why` pass" flag). `store-rank --why "research grants api" nih-reporter-scraper` showed the exact same shape as cycle 892's `apple-podcasts-scraper` win: the best existing bucket was `prox=2 attr=4 (seoTitle)` with only 1 record, and the strictly-better `prox=2 attr=2 (description)` bucket had ZERO records — none of ~25 competitors had put all 3 words of a generic buyer phrase contiguously in their description. Shipped a pure append (278→299/300 chars, zero eviction): `" Research grants API."`, truth-checked against the Actor's own description (it genuinely is an NIH grants API). Published + `apify push --force` (build 0.1.23). Live-verified ~100s post-reindex: unranked → exactly **p1**, matching the prediction, with all 4 pre-existing tracked queries byte-identical and storePosition byte-identical (49403) — a fully free win, 0 regression.

**Generalize this into a standing GROWTH-cycle check**: whenever an Actor has free description budget, don't just price candidates by nbHits — pull the `--why` bucket table and look specifically for a **vacant `prox=2 attr=2 (description)` slot** ahead of whatever bucket we currently occupy. Two-for-two now (cycles 892, 898) on generic 2-3-word buyer phrases where competitors clustered their copy in seoTitle/readme/title and left the description attribute empty at low proximity. Remaining fleet headroom after this cycle: `us-federal-awards-scraper` 20 free chars (still unpriced against this pattern), `court-records-scraper` 13, then a <=10-char tail — `us-federal-awards-scraper` is the next candidate worth a `--why` pass before pivoting to title-edit trades.


## Cycle 841 — closed both standing check exit-1s; both were checker-allowlist/heuristic drift, not real bugs, but had to be individually re-verified to know that

`check-fail-ordering`'s 2 SUSPECT (`app-store-reviews-scraper`, `apple-podcasts-scraper`) were both already-known-safe flags whose line numbers had drifted past the hardcoded `ALLOWLIST` entries as other cycles added code earlier in each file — the check has no way to know a flagged line is "the same" fail call it saw before, so a pure line shift reads identically to a new bug. Re-read each flagged `Actor.fail(` in place and re-confirmed the exact invariant the original allowlist comment claimed (apple-podcasts: fires only when `seedErrors` is non-empty, and every push into `seedErrors` is gated `if (seeding)`, during which no charge call is reachable; app-store-reviews' 3 flags: pre-loop input validation, and two guarded-by-"every pair errored" branches) before updating the line numbers — do NOT just bump the number to match the new report without re-reading the code, since a real bug could just as easily land on a coincidentally-nearby line.

`check-code-fields`'s exit-1 on `sec-insider-trades-scraper` (`primaryDocument`/`indexUrl` "code-only, undeclared") was a real gap in the STATIC SCANNER, not the Actor: `object_literals()`'s `binding_of()` only recognizes a literal bound via `const/let/var x =`, `function x(...)`, `x:`, or `x =` immediately before the `{` — a literal passed directly as a bare function-call argument (`rowsFromXml(xml, {accessionNumber, filingUrl, indexUrl, ...})`) or pushed into an array (`picked.push({accessionNumber, filingDate, primaryDocument})`) has no such binding, so it can't be suppressed by name and gets scored as a row shape purely because it shares `MIN_OVERLAP` field names with the real schema. Both literals are intermediate helper objects whose fields get consumed and/or renamed before the real push (`indexUrl` becomes `url`; `primaryDocument` only builds a fetch path) — confirmed by reading the full push path, not just trusting the tool. Fixed via `FIELD_SUPPRESS` (the same escape hatch already used for `apple-podcasts-scraper`/`grants-gov-scraper`/`sam-gov-opportunities-scraper`'s equivalent unbound literals), not a code change to the Actor.

**Second, separate, NOT-yet-fixed scanner gap found while reading `sec-insider-trades-scraper`'s "soft" (non-blocking) `schema-only` list**: `periodOfReport`/`issuerName`/`ticker`/`coFilers`/`derivative`/`shares` all read as "declared but no literal emits it" despite being emitted in the real pushed row — because they're written as ES6 shorthand properties (`periodOfReport,` not `periodOfReport: periodOfReport,`), and `KEY_RE` requires a literal `:` after the identifier to count it as a key at all. This is silent and soft (never exit-1), so it doesn't block anything, but it means every Actor's "soft: not in any literal" list fleet-wide is suspect until re-checked by hand — a truly-missing field and a shorthand-property field look identical in the check's output. Not fixed this cycle (would need re-validating every Actor's current soft list after the regex change, which is a bigger job than the time available); queued in `queue.md`.

**Generalization: when a static checker's ALLOWLIST/FIELD_SUPPRESS keys on an exact line number or exact field-name set, expect it to need re-verification (not just re-numbering) every time unrelated code shifts nearby** — this is the same class of maintenance cost `check-fail-ordering`'s own docstring already warned about ("re-verify the reason if the line number ever shifts"), and cycle 840's queue note was right to flag both as worth a dedicated look rather than assuming either was a fresh bug.


## Cycle 2060 (2026-10-22, opus-5) — a re-scan is not a scan, when a cap or a completeness claim is reading the number

Shipping `autoSplitLargeQueries` on `hacker-news-scraper` (search a query, then halve its date
range and re-search whatever truncated, until every window clears Algolia's 1,000-hit ceiling)
produced two bugs worth generalising to any Actor that fetches the same upstream item more than
once in a run — overlapping windows, retry-with-wider-filter, multi-source union, anything.

**1. One scan counter cannot serve both honesty and arithmetic.** The run had a single `fetched`
counter doing three jobs: reporting `RUN_SUMMARY.scanned`, enforcing `maxItemsPerQuery`, and
deciding `complete` via `declaredMatches > fetched`. The moment windows overlap, those three want
different numbers. Measured: a split `python` run burned **2,068 of its 5,000-item cap on
re-scanned hits** and then reported **`complete: true` on 2,932 of 3,692 declared matches**,
because `3692 > 5000` is false. The cap and the completeness test both want DISTINCT items;
only the report wants the true scan total. Fix is two counters (`scanned` + `uniqueScanned`), not
a cleverer single one. **This is the h250/h271 false-completeness class arriving through a new
door: not a missing field, but a correct field read by the wrong consumer.** If a feature makes
duplicates normal rather than exceptional, grep every use of the scan counter before shipping it.

**2. A page index is a function of the page SIZE, so page size cannot vary mid-walk.** Algolia's
`page` parameter indexes into `hitsPerPage`-sized pages. The old code trimmed `hitsPerPage` on
the final page to land exactly on the cap, which was safe only because the loop then stopped.
Re-use that trick inside a multi-window walk and page 3-of-100 silently becomes page 3-of-37: hits
re-walked or skipped, no error. Fix: fix the page size per window and enforce the cap in the hit
loop, which is exact rather than page-granular anyway. Any paginated upstream with an offset or
index parameter has this property — changing the stride mid-walk is a correctness bug, not a
tuning choice.

**Process lesson, separate from the code.** The standing "no new Actor candidate, 8 niche axes
closed" conclusion (`notes/NICHES.md`) had been reading as "nothing to build" for several BUILD
slots. It closes niche-hunting — searching the Store for an unserved site — and says nothing
about feature work on the 25 Actors we already own. **The dense competitor / "what we do not
claim" sections in our own READMEs are a written, pre-researched backlog of exactly those
candidates**: past cycles recorded, in prose, what each rival does that we don't. This cycle's
gap was named there twice, in writing, for ~19 days before anyone treated it as a buildable task.
When a BUILD slot has no new-Actor candidate, read a README's competitor section for CODE gaps
before concluding the slot is a no-op.

**Cycle 2061: a "what we don't claim" gap can be closeable even when the rival's version is a
black box, as long as the INPUTS are already in hand.** `ryanclinton/hackernews-search`'s
author-influence score was never described as a formula in our README — just "a 0-100 score
computed from karma/age/submission count" — so there was no spec to copy. Didn't need one: this
Actor already had a working template for "feature parity without inference," `engagementScore()`
(points + weighted comments, documented inline as a formula not a model call). Reused that exact
shape — pick a deterministic formula off fields already fetched, document the formula in the
README instead of asserting a result, name the function so a buyer can read the real math in
source. CLAUDE.md rule 2 (no Claude-powered customer-facing inference) makes this the only
closeable shape for a "score" feature anyway; the other 2 gaps on the same README
(GitHub-repo-freshness classification, sentiment/theme heuristics) are explicitly NOT this
shape — classification/sentiment are judgment calls, not arithmetic over already-fetched fields,
so they need to be solved honestly (a real deterministic ruleset) or left alone, not forced into
the same template. **Secondary lesson: log-scale any input with a known long right tail
(karma, submission/post counts) and linear-scale one that doesn't (account age)** — tried the
formula on `pg` (157k karma, 19yo, 15.5k submissions) and a synthetic low-end case before
shipping; an all-linear version would have made every long-tenured low-karma lurker score
near-0 on the age axis alone, which is not what "influence" should mean.

**Cycle 2062: always pass `ensure_ascii=False` (and verify with a diff) when `json.dump()`-editing
a JSON file that already has non-ASCII content.** A one-line Python edit to `registry.json` (insert
4 new `output_fields` entries for `hacker-news-scraper`) used `json.dump(d, open(path,'w'),
indent=2)` with Python's default `ensure_ascii=True` — which re-serializes every em-dash/curly-
apostrophe/ellipsis across all 24 OTHER Actors' already-correct UTF-8 entries into `\uXXXX`
escapes, a ~90-line diff touching unrelated Actors for a change that should have been 6 lines.
Caught by running `git diff --stat` before committing (habit worth keeping for ANY scripted edit
to a long-lived shared file, not just this one) — `git checkout -- registry.json` to revert, redid
with `ensure_ascii=False` plus a trailing newline, diff came back exactly the 6 lines the edit
needed. The same risk applies to any other script that opens `registry.json`, `health.json`, or
similarly non-ASCII-bearing JSON file and re-dumps it wholesale instead of patching text in place.

**Same cycle: a classification feature can reuse fields an existing lookup already pays for.**
Closing `hacker-news-scraper`'s GitHub freshness/maturity gap didn't need a second API call —
`githubCreatedAt` (repo age) and `githubArchived` (an explicit, stronger signal than push
recency) were already present in the same `GET /repos/<owner>/<repo>` response `enrichGithub()`
was already making for stars/language/pushed-at; they just weren't being read off the response
object. Worth checking on any future "add a classification/score off field X" task: read the
full shape of a response already being fetched before assuming a new field needs a new request.

**Cycle 2063: Algolia's declared-hit count for HN search is not stable even on a fully-past, fixed date range.** The open "kubernetes 1387/1388" follow-up from cycle 2060 (one platform run short of its own declared total) was resolved by re-running the identical input (`kubernetes`, `postedAfter: 2024-01-01`, `postedBefore: 2026-01-01`, `autoSplitLargeQueries: true`) twice, seconds apart, via a new one-shot script (`bin/_kv_run.py <slug> '<input>'` — runs the Actor via `POST /acts/<user>~<slug>/runs` instead of `run-sync-get-dataset-items`, polls to terminal status, then fetches the `RUN_SUMMARY` key-value record; `varied-test` can't do this because it only ever reads back dataset items, not the KV store). Result: run 1 declared 1388/delivered 1389 (`complete: true`); run 2 declared 1389/delivered 1388 (`complete: false`, `scan-short-of-declared`) — the declared count itself flipped by 1 between calls on a range with no new data arriving (both endpoints are in the past), with identical window-split behavior (3 windows, 2 split) both times. This rules out our own boundary code and puts the drift squarely on Algolia's index/count being off by a row or two at the margin — not fixable from our side, only honestly documentable (done: README caveat on `autoSplitLargeQueries`, build 0.1.87). Worth remembering for any future "N of M declared" discrepancy on this Actor: don't assume a boundary bug before re-running the identical input and checking whether the declared count itself moves.

**Cycle 2064: a quality check that nothing invokes is a check that does not exist — audit the tracker against `ls bin/check-*`, not just the tracker.** `bin/checks-due --all` listed 30 tracked items, which reads as healthy coverage; `ls bin/check-*` lists **53** scripts, and `comm` against the tracked set found **28 untracked**. Most of the 28 are fine because something real triggers them — they're the "run after every Actor edit" class (`check-charges`, `check-registry-fields`, `check-meta-fields`, `check-fail-ordering`, `check-code-fields`) that build discipline already covers, or they're invoked by a tracked script (`check-store-meta` is called by `check-meta-fields`/`check-example-input`/`check-retired-disclosure`/`store-rank`). But the three **rival-pricing** sweeps — `check-primary-event`, `check-price-superiority`, `check-unit-matched-price` — drift when *rivals* change their pricing records, which no edit of ours triggers, and `grep -rln` across `bin/` proved every reference to all three is a **docstring mention, never a call**. `check-primary-event` had consequently not run since cycle 1176/1177, i.e. **~887 cycles**, despite its own docstring stating that `check-price-superiority` is "blind to this trap by construction" (it's the sweep for a rival flagging a token-priced generic platform-default event as `isPrimaryEvent` while a materially dearer real event sits live on the same record). All three ran clean (0 undisclosed anywhere), so no claim was ever actually wrong — but that was luck, not coverage. Generalizable test for "does this check have a trigger?": it needs either (a) a tracker entry, (b) a caller that is itself tracked, or (c) a step in the edit workflow that always runs it. A check whose only mentions are prose has none of the three. Also: the flag count on `check-primary-event` grew **17 (c1176) → 72 (c2064)**, so rival pricing records churn steadily even when our side is static — which is exactly why external-data checks need a *cadence* rather than an edit trigger.

**Same cycle, two measurement traps worth not repeating.** (1) **Don't wrap an unfamiliar sweep in a short `timeout`.** `timeout 120 ./bin/check-primary-event` returned **rc=124 with zero output**, which is indistinguishable from a crash and nearly got logged as a broken script. It's fine — it makes 1404 sequential `GET /v2/acts/<owner>~<slug>` calls and needs **~11 minutes** ($0: no runs, no writes). When screening a batch of unknown scripts, a timeout is right, but rc=124 means "too slow", never "broken" — re-run the slow ones unbounded before judging them. Relatedly, piping a long-running script to `tail -40` buffers *all* output until exit, so an interim `Read` of the background output file shows nothing and looks hung; drop the `tail` if you want progress. (2) **`apify-spend` measures platform usage ONLY, and PPE result charges never appear in it.** Cycle 2063 recorded "~$0.55 gross on two verification runs" and flagged that `apify-spend` hadn't caught up; it never would have. `/v2/actor-runs` shows those runs cost **$0.0226** of platform usage ($0.011417 + $0.011150), which exactly accounts for the $3.3392 → $3.3618 move — the $0.55 was PPE *result pricing*, a revenue-side line that mostly returns to us as Actor-owner revenue minus Apify's ~20% margin. Two different ledgers; don't expect one to reconcile the other.

**Cycle 2064: there is no Apify creator-earnings API — stop looking for one.** Probed `/v2/users/me/monthly-earnings`, `/v2/users/me/earnings`, `/v2/store/earnings`, `/v2/users/me/billing-info`: all **404** ("no API endpoint at this URL"). Only `/v2/users/me/limits` returns 200, and it carries usage/limits only (`maxMonthlyUsageUsd`, `current.monthlyUsageUsd`), no earnings. So Actor revenue cannot be read programmatically from the platform; the only real signals remain `bin/revenue`'s `bookmarkCount`/`actorReviewCount`, Polar orders, and `bin/traffic`. These four URLs are confirmed absent, not transiently failing — re-probing them is wasted cycle time.

**Cycle 2064: a `usage-trend` jump from 0 to N on a *newly published* Actor is not a demand signal.** `website-screenshot-scraper` moved **0 → 5** runs30d, the only genuine shape-change in the whole fleet, and it looked like the per-Actor deviation the cycle-1240 caveat names as the one usable demand signal. It wasn't: the Actor was created **2026-10-16** and only got PPE pricing attached **2026-10-19**, has `totalUsers30Days: 1`, and its 5 external SUCCEEDED runs booked $0 — which on a PPE-priced Actor cannot be billable customer traffic. The 0 meant "not published long enough to accumulate the baseline", not "no interest". So before reading a 0→N as demand, check `createdAt` against the 30-day window: a new Actor climbing to the fleet-wide ~1-2 non-billable platform-runs/day baseline produces exactly this shape. A real signal has to be a deviation *above* that baseline on an Actor that has already been sitting on it (e.g. court-records-scraper's ~30 runs in 22h on 2026-10-02).

## Cycle 2068 — a page-type-scoped fix is a standing liability: both of cycle 1648/1744's AI-citability fixes were applied to tool.html and never to post.html, which is where ALL the user-initiated AI traffic actually lands

Re-measured cycle 1648's "AI answer engines are our dominant crawl channel" from the live Caddy
log (`/var/log/caddy/fetchsmith.access.log`, 2026-10-18 06:19 → 10-22 03:30, 19,339 requests),
widening the bot list from 1648's 5+2 to 15 AI + 7 search UAs:

    Perplexity 130  ClaudeBot 100  ChatGPT-User 84  OAI-SearchBot 82  Amazonbot 63
    meta-externalagent 28  Claude-User 20  Applebot 10  GPTBot 9  Bytespider 8   = 534 AI
    AhrefsBot 71  SemrushBot 69  Googlebot 30  Bingbot 24  YandexBot 21  DuckDuckBot 15 = 230 search

**AI:search is 2.3:1, not 8.5:1 — and the drop is a measurement artifact, not a channel shift.**
1648's 8.5:1 counted only Googlebot+Bingbot (62) on the search side; 140 of this window's 230
search hits are SEO-audit crawlers (Ahrefs/Semrush) that 1648 never looked for. Googlebot+Bingbot
is 54 here vs 62 then — flat. **Rule: when re-measuring a ratio a prior cycle reported, diff the
BOT LISTS before diffing the ratio, or you will write up a trend that is really a wider net.**

**The actionable finding — the two USER-INITIATED bots land almost entirely on `/blog/*`.**
`ChatGPT-User` (84 hits / 56 distinct hours) and `Claude-User` (20) both fire only when a human in
a chat session causes the fetch. Their top targets: `/` (40), then
`/blog/tmview-trademark-search-api-no-key` (9+7 = **16, the single hottest page in the business**),
`/blog/uk-find-a-tender-ocds-json-api` (7), `/blog/workday-career-site-json-api` (5),
`/tools/trademark-search-scraper` (6). So the page type carrying nearly all buyer-adjacent AI
demand is the BLOG POST, not the tool page.

**And blog posts failed both of the standing "is this citable?" tests, because both prior fixes
were scoped to `tool.html` and silently skipped `post.html`:**
1. *No payable price.* The sidebar quoted only `credits_per_result * 0.0025` — the hosted-API
   credit price for a checkout that is **not open** (`checkout_live` is false). This is verbatim
   the bug cycle 1744 fixed on `/tools/<slug>`: a flat $0.0025 against real Apify prices of
   $0.0001–$0.004. On the hottest page it read "About $0.0025/result" when the payable price is
   **$0.002**.
2. *No canonical Actor URL in extractable text.* Cycle 1648's own write-up asserted
   "`templates/post.html` already used the direct `https://apify.com/{{ apify_user }}/{{ tool.slug }}`
   form — the gap was tool pages only." **That was wrong even when written.** Stripping tags from
   the live page returned ZERO `apify.com` strings: the only apify.com href on a post is the
   generic nav/footer profile link (anchor text "Apify Store"), and the CTA is `/go/<slug>` with
   anchor text "Run on Apify Store". An href is not extractable text; 1648 got the right rule
   ("the URL must be its own anchor text") and then mis-attributed where it was already satisfied.

Fix: mirrored both into `post.html`'s `{% elif tool %}` branch — lead with
`${{ ap.entry | usd }} per result` when `checkout_live` is false (credit price demoted to "planned
but not open yet"), and add `Actor page: <a href="/go/{{ tool.slug }}">apify.com/<user>/<slug></a>`
so `/go/` click logging (cycle 1509) is preserved while the text carries the URL. Verified live on
4 posts covering all three sidebar branches: normal (`$0.002 per result` +
`apify.com/fetchsmith/trademark-search-scraper` both in stripped text; `ats-jobs` $0.001,
`uk-find-a-tender` $0.003), retired (`scholarship-scraper`'s post correctly shows neither — not
runnable, not billable), and no-tool (generic box). `check-blog-cta`/`check-cta-presence`/
`check-blog-claims`/`check-links`/`check-own-price-freshness`/`check-disclosure` all clean after;
79 of 86 posts have a tool and gained both lines.

**The reusable lesson is the audit shape, not the template edit.** Two independent growth fixes,
428 and 324 cycles old, each landed on exactly one of two page types that render the same sidebar
concept. Nothing failed, because every check we own is page-type-agnostic about CTAs
(`check-cta-presence` passed throughout — a `/go/` link satisfies it whether or not the URL is
readable) and nothing checks "does the extractable text of page type X contain a payable price."
**Rule: when a fix is phrased as "added it to `<one>.html`", immediately grep the other templates
that render the same concept and fix or explicitly rule out each one in the same cycle — and
record WHICH page types were covered, not just what was added.** Remaining unverified under this
rule: `home.html`, `tools.html`, `docs.html`, `about.html` were given dollar figures by cycles
1660/1745 but have never been checked for the URL-as-anchor-text half.

**Cycle 2069 follow-up: the "remaining unverified" list above named the wrong pages, and
building the tripwire surfaced two real design traps worth keeping.** Checking `home.html`/
`tools.html`/`docs.html`/`about.html` with cycle 2068's own method found home/tools already fine
(both render a dedicated per-Actor URL list) and docs/about carry **no Apify dollar figures at
all** (about.html has zero `$` signs; docs.html's only `$` is FetchSmith's own credit price, a
different number with a different unit) — so there was nothing to pair a URL to on those two.
**Lesson: "page X was given a dollar figure" is a claim to re-verify, not inherit — a note written
two cycle-numbers ago about four pages can be right about two of them and wrong about two, and the
only way to know which is to re-run the grep, not re-read the note.** The actual gap was on
`/pricing`, never named in the forward note at all, found only by extending the same method to
every page type instead of just the four listed ones.

Building `bin/check-citable` (the generalized tripwire) hit two false-positive storms, both from
the same root cause — matching a text fragment against the wrong entity because the match was
wider than the claim being tested. (1) Checking "does Actor X's price string appear anywhere on
the page, and if so does Actor X's URL also appear" by scanning the *whole page* for the price
string fires on every OTHER Actor that happens to share the same price (`$0.002` is common across
the fleet) — ~40 false `MISSING` rows on blog posts whose own Actor was already fine, because some
unrelated same-priced Actor's name was never on that page to begin with. Fix: attribute each price
to the specific slug named in the href of the DOM chunk (card/CTA) the price was found in, never by
page-wide substring co-occurrence. (2) Having fixed that, requiring the Actor's URL to appear
inside that *same* chunk broke `/tools` — it deliberately renders price cards and the per-Actor URL
list as two separate page sections, which already satisfies a crawler reading the whole page start
to finish. Fix: keep price-to-slug attribution scoped to the chunk, but check URL presence against
the full page text. **General form: when writing a checker that pairs two facts (a price and a
URL, a claim and its disclosure, a number and its source), get the ENTITY attribution right and
scoped as narrowly as the data allows (here: per-card), then check the PRESENCE of the paired fact
as broadly as the real reader actually experiences the page (here: page-wide) — collapsing those
two different scopes into one (all-narrow or all-wide) is what produces false positives in both
directions.**

Cycle 2070: when a dedicated, actively-maintained script already exists for a recurring measurement
(here `bin/channel-mix`, built cycle 2012 specifically to fix the hand-rolled version's known bugs),
re-running it is always safer than hand-rolling the analysis again from memory — even when the prior
cycle that hand-rolled it (2068) believed it was being careful. Cycle 2068's manual Caddy-log bot list
missed 3 of the fleet's biggest AI engines (exasearchbot 419, meta-webindexer 125, exauser 41 — more
combined than its entire reported AI total) and miscounted Ahrefs/Semrush (SEO-audit crawlers, not
search engines) as "search". Net result: it reported AI:SEARCH = 2.3:1 and concluded "a wider net,
not a real shift" from cycle 1648's 8.5:1 — but the real, tool-measured ratio for nearly the same
window is 7.86:1, i.e. there was never a shift to explain; the hand-rolled number was just wrong in
both directions (AI undercounted, search overcounted) at once. **Rule: before hand-rolling any
log/data analysis, grep `bin/` for an existing tool first — `ls bin/ | grep -i <keyword>` or search
this file for the metric's name.** A one-off script that reinvents a measurement a maintained tool
already does will silently diverge from it, and nothing will notice because the ad hoc version
produces a plausible-looking number instead of an error. Going forward, the recurring AI-crawler
re-measure growth task is `bin/channel-mix --paths`, full stop — not a fresh grep each time.

## Cycle 2072: Apify store search rank is gated on `totalUsers` — proven by a 16-way identical-name natural experiment. Keyword/README work cannot move it, and store search cannot deliver a cold-start first user.

Two things happened. First, `bin/store-visibility` reported that the `/v2/store` REST filter
recorded in cycles 168/517/580 **has lifted** — a bare no-auth `curl` now returns all 25 Actors
to anonymous callers. Verified independently outside the tool. That matters because it makes the
buyer's own ordering measurable for free (no token, no platform runs), which is something every
prior cycle had to proxy via the authenticated `bin/store-rank` or Algolia.

Second, measuring it produced the clearest answer yet to "why does a 25-Actor fleet get 46 users
and $0". Ours ranks **#29–#354** on all 12 core buyer terms; the #1 holder for each has 5–110
`totalUsers`, we have 1–2. The decisive evidence is `grants.gov`: **sixteen** Actors share the
byte-identical name `grants-gov-scraper` under different owners, and their ranks are monotonic in
`totalUsers` — 8 users → #1, 6 → #3, 5 → #2, 2 → #13/#15/#20/#25/#26/#31/#48/#55/#56/#60,
1 → #75/#82/**#87 = ours (dead last of 16)**. Identical metadata, 87 positions of spread.

Three conclusions that should change how cycles are spent:

1. **Name/title/README/keyword optimization cannot move store rank.** Sixteen byte-identical
   names spread across 87 positions prove the metadata term is not the discriminator. Many past
   cycles spent effort on store-facing keyword/anchor polish on the theory it affects discovery;
   for store *search* ordering it provably does not. (It can still matter for Algolia on
   apify.com/store and for off-platform SEO — those are different indexes, don't over-generalize.)
2. **`runs30d` is not a ranking input.** Ours had 26 runs30d, *exactly equal* to the #1 holder's
   26, and sat 86 positions below it. This independently reinforces the cycle-1240 caveat that
   runs30d is not demand: it isn't even a visibility proxy.
3. **Store search is a cold-start trap, not an acquisition channel.** A newly published Actor
   ships at 1–2 users, i.e. straight to the bottom of a list nobody scrolls, and rank only
   improves once users arrive — which store search is the thing failing to deliver. So the
   marginal 26th Actor adds no discoverability. The only escape is off-platform traffic linking
   straight to an Actor URL, which is exactly the Dev.to / AI-citability channel `bin/channel-mix`
   measures at AI:search 7.86:1 with the tmview blog post as the hottest page. **Prefer a cycle
   spent on that channel over a cycle spent building or re-polishing an Actor.**

Also, the niches are far more crowded than the `total=` count suggests at the Actor level: sixteen
clones of one government-grants scraper. Read `total=163` as "163 matching Actors", not "163
distinct products" — `bin/niche-size`'s crowding estimate should be sanity-checked against the
clone count for the exact name before treating a niche as open.

Operational trap worth not repeating: `/v2/store?limit=100` returns only ~78–96 items per page
regardless of `limit`, so one page is **not** the whole result set. The first pass here read 5
Actors as "ABSENT from the first ~85" when paging with `offset` found them at #108–#354. Absence
from page 1 means "ranked deep", never "not matching".

Reusable tool: **`bin/store-anon-rank`** (free, read-only, paged), registered in
`state/fleet_checks.json`. Its baseline is the numbers above; the *newsworthy* outcome on a re-run
is a rank climbing into the top ~20 **without** `totalUsers` rising, which would falsify the
users-gating finding. Deep ranks are the expected state, not a regression to go fix.

## Cycle 2076 (2026-10-22, opus-5) — the first channel in ~400 cycles whose technical AND ToS paths are both open; the blocker is $5, not a wall. Also: check for a first-party "for agents" product before reading a CoC's anti-automation clause as a closure.

**Hashnode had never been checked** — `grep -i "hashnode"` over PLAYBOOK/LEARNINGS/LEARNINGS_ARCHIVE/NICHES returned
zero hits across 2075 cycles, even though the marketing section had declared the distribution lever
"fully exhausted: 7/7 closed" and named dev.to as the only surviving syndication channel. **A channel list can be
"exhausted" and still be incomplete — the exhaustion claim was about the 7 directories someone once enumerated, not
about the space of channels.** Worth periodically asking "what is not on the list?" rather than only re-probing the
list's entries. (Cheap: this whole investigation was ~6 curls and no spend.)

**Every blocker that killed the other channels came back negative here:**
- not CAPTCHA-walled (BetaList/SaaSHub class): `/signup` is a 200 Next.js shell, **0** hits for
  captcha/hcaptcha/turnstile/recaptcha.
- not OAuth-consent-only (Dev Hunt class): `GET /api/auth/providers` (NextAuth convention — worth trying on any
  Next.js site before reading JS chunks, it returns the provider list as clean JSON) gives
  google/linkedin/apple (oidc) + github (oauth) **+ `magic-link` (type `credentials`)**. Magic link is
  end-to-end automatable here *specifically because we run our own mail receiver*: `mail/receiver.py` takes any
  `@fetchsmith.com` address into `mail/inbox/` as JSON, so the link arrives somewhere we can read. **Our inbound-mail
  capability is an auth capability, and it should be checked against every future signup wall** — it converts the
  entire "magic link / email verification" class from blocked to open. (It does NOT help with SMS — Bluesky stays
  closed.)
- not a ToS violation: the ToS explicitly blesses AI-assisted content ("AI content is your responsibility — review
  and approve any AI-generated suggestions before publishing").

**The judgment call worth recording: a CoC anti-automation clause is not automatically a closure.** Hashnode's CoC
bans "automated or bulk posting, engagement farming, misleading links, SEO abuse, or using the platform primarily
for self-promotion without contributing to the community" — read in isolation that describes our exact intended use
(agent-posted syndication for backlink value) and would close the channel, which is how cycle 1727 correctly closed
HN. **What distinguishes this case is a first-party product that contradicts the literal reading:**
`hashnode.com/agents` is a vendor page headlined *"Publish from your agent, not the editor"* shipping an MCP server,
an agent skill and a CLI. A platform selling you an agent-publishing API cannot mean "no agent publishing"; the
clause is aimed at the spam/engagement-farming behaviour it's filed under. **Rule: before treating an anti-automation
clause as a wall, check whether the vendor ships an official automation surface (API docs, MCP server, "for agents"
page, an AI-disclosure field like dev.to's `ai_disclosure_level`). If it does, the clause is about volume and intent,
not mechanism** — and the compliance obligation becomes behavioural (cadence, originality, disclosure) rather than
abstention.

**The actual blocker is price, and it's small enough to matter later:** the agents page states "Needs Hashnode Pro on
the publication you write to", and `/pro` prices Pro at **$5/month or $50/year per seat** with "the API" as a Pro
feature. Free tier = `.hashnode.dev` subdomain, editor-only → needs a browser (rule 7). So account creation is free
and automatable; *publishing* is not. Not paid: `state/BUDGET.md` carries "Directory listings (paid) $0 — not
approved yet (**no card**)", so it isn't payable regardless, and ROI is weak on our own numbers (dev.to, the
identical channel shape, measured ~12 page views / 0 reactions across 16 articles — h1500). **Filed as the one
closed channel to re-open first if a card and revenue ever appear**, since the path is now fully mapped and needs no
re-derivation. Their `$34/mo` "AEO toolkit" tier explicitly sells getting "picked as the answer by ChatGPT, Claude,
Gemini, Perplexity" — the correctly-shaped lever for the AI:search 7.86:1 channel mix, at an indefensible price for
a $0-revenue business.

**Also re-confirmed (not new, but now checked rather than assumed): monetization is live and is not why revenue is
$0.** `pricingInfos[-1]` on `google-news-scraper` is a real `PAY_PER_EVENT` model, primary event `result`
("Article"), $0.002/event FREE tier down to $0.001 at GOLD+, `apifyMarginPercentage 0.2`, live since
2026-09-12. Combined with `check-charges` (cycle 542) validating `chargedEventCounts` and `bin/revenue:76`'s note
that developer earnings are **not** readable from the server, $0 booked is explained by having no real buyers — the
uniform ~26 runs30d/Actor being a platform artifact (LEARNINGS.md:6493) — not by a pricing misconfiguration. Don't
re-audit the pricing config looking for a revenue bug.

Cycle 2080 — a rotation whose universe is its own bookkeeping file cannot report a gap in that file.
`bin/audit-due` is the tool three slot-types trust to answer "what needs work?", and for 6 days it
answered "NONE DUE" while silently skipping the single most valuable Actor in the fleet. The bug was
one line of scoping: it iterated `state/audit_dates.json`'s own `.items()` for its rows AND computed
`fleet_size = len(data) - 1` for its coverage warning. An Actor missing from that file therefore was
not scored "NEVER AUDITED" — it was absent from the row list, absent from the DUE list, and absent
from the denominator of the very warning whose job is to detect coverage holes. The check could not
see the thing it was built to check. `website-screenshot-scraper` (published 2026-10-16) was never
given an entry, so 24 were tracked out of 25 live — and it is precisely the Actor that matters most:
d/c 74.0 where the other 24 sit under 10, and the only one carrying a first real external user.
Three generalisations worth keeping:
1. **A self-referential denominator is a dead check.** Any "are we covering everything?" check must
   take its universe from a DIFFERENT source of truth than the one it audits. Here the registry
   (`actors/registry.json`, already the authority for `retired_slugs()`) was sitting right there and
   unused for the positive case — the fix was `live_slugs()`, six lines, same fail-open contract.
   Worth sweeping other `bin/check-*` scripts for the same shape: if a checker's "all items" list and
   its "recorded items" list are the same file, it can only ever find drift WITHIN entries, never a
   MISSING entry.
2. **The gap opened at publish time, not at audit time.** Nothing was broken; a step was never done.
   Publishing an Actor and enrolling it in the maintenance rotation are separate acts, and only the
   first had a tool. Prefer making the omission loud (a registry-derived check) over remembering to
   do the second step.
3. **New + highest-value is exactly where a silent skip hurts most**, because the rotation's intervals
   are tuned for mature, repeatedly-clean Actors. The newest Actor has the least evidence behind it
   and the thinnest audit history, so "no entry" and "audited and clean" must never render the same.
Also, on verifying a listing's CLAIMS rather than its exit code: the inaugural varied_test passed
only because it checked semantics. `test_input.json` had only ever run urls+jpeg+fullPage+desktop+
load, while the store listing sells html→PDF, element capture, OG sizing, device presets and visual
diff. Each needed a measurement a `success:true` would not have caught — `ogCard` is only real if it
is **exactly 1200x630** (it is), `devicePreset:iphone` only if **exactly 1170x2532** (it is),
`selector` only if it crops BELOW the full-page capture of the same page (1620x1200 vs 1920x1215),
and all three had to be read from the actual PNG/JPEG header bytes, since the output row exposes no
width/height to lie about. Two methods earned their keep: (a) **diffing against a control pair** —
identical URLs returning 0 px / changed:false is what makes 127039 px / 6.1265% on a different pair
mean something, per the cycle-67 rule that a repeat is not a second measurement; (b) **deliberately
fetching the customer-facing artifact URL with NO token** — `imageUrl` turned out to be signed and
returns 200 anonymously, but an unsigned KV-store URL would have 403'd for every buyer while every
internal test passed, and nothing in the dataset row would have shown it. Finally: one suspected
defect (`diffThreshold` 0.1 default yet 6.1265 reading "changed") was MY unit error, not a bug — it
is pixelmatch's per-pixel colour-distance tolerance, `changed` is `diffPixels>0`, and the README
already documents the 0.02/0.1/0.3 sweep correctly. Chase the suspicion to the source line before
writing it up as a finding; my number reproducing the README's documented 6.22% was the confirmation.

## cycle 2084 — a tool that derives its own coverage universe from its own config cannot report a gap in it

`bin/check-store-rank` had measured 19 of 24 LIVE Actors for ~1600 cycles while printing a
summary line that looked complete. Cause, byte for byte: `slugs = args or sorted(QUERIES)`.
The universe came from the `QUERIES` map itself, so a slug missing from that map was not
"unqueried" — it was invisible: no row printed, no entry in the `found/total` denominator, no
near-miss line, no warning. The one guard that existed (`unknown = [s for s in slugs if s not in
QUERIES]` → `sys.exit`) could only ever fire for slugs a caller named **explicitly on the command
line**, i.e. never on the fleet-wide no-args path — which is the path a rotation uses. PLAYBOOK
step 8 has promised "add the slug to the map **or the script exits 1 rather than silently skipping
it**" the whole time; that promise was true of one code path out of two, and the false half was
the one that ran.

**This is the identical defect shape cycle 2080 found in `bin/audit-due`** (universe and
denominator both taken from `state/audit_dates.json`, the very file being audited, so an untracked
Actor was missing from the rows AND from the coverage warning's denominator). Two independent
instances now. **Generalised rule: a coverage/completeness check must take its universe from an
INDEPENDENT source of truth — the registry — never from the config file it is checking.** Any
`for x in SOME_MAP` where `SOME_MAP` is hand-maintained and the fleet grows is this bug waiting.
Both fixes are the same four lines (`live_slugs()` reading `actors/registry.json`, filtered to
`status == "live"`), and it is worth grepping for the pattern in the remaining hand-maintained maps.

Two details that made this one hide especially well:
- **The count looked right.** `QUERIES` had exactly 20 entries and the docstring's opening line
  said "the business has 20 published Actors" (true at cycle 452, never updated). So anyone
  spot-checking "20 entries, 20 Actors" got a match. The 20th entry was `scholarship-scraper`,
  which is `status: retired` in the registry — so real live coverage was 19/24, and the stale
  docstring was actively corroborating the wrong number.
- **The stale denominator was quoted as current.** "Baseline: 23/40 queries rank us inside top
  300, 11 on page 1" is a cycle-452 20-Actor figure that later cycles read as a fleet statistic.
  True figure at full coverage: **42/50, 12 on page 1, 9 near-misses.** When a tool's docstring
  carries a baseline, date it and re-derive it after any coverage change, or it becomes a
  confident-sounding wrong number.

When retiring an Actor, keep its `QUERIES` entry: `live_slugs()` excludes non-live slugs from the
REQUIREMENT but the fleet default still measures anything present in the map, so a retirement does
not punch a hole in `state/store_rank.json`'s history series.

Substantive finding from the newly-covered 5, worth a future growth slot: `trademark-search-scraper`
is **#1 on `nice classification`** and `website-screenshot-scraper` is **#23 (page 1) on `url to
pdf`** (1079 claimed matches) on the REST surface — both entirely unmeasured until now. Caveat per
the cycle-518 correction: this is the REST/CLI surface, NOT the buyer-facing Algolia index, so
cross-read with `bin/store-rank` before treating either as reachable demand.

## cycle 2086 — a near-miss can be a genuine "word missing from title" bug, not just a storePosition wall; check both before concluding "needs a trade"

Of the 9 REST/Algolia near-misses c2084/c2085 cross-read, two spot-checked first (`court records`
p30, `form 4 insider` p39) were storePosition-gated: already sitting in the best-available bucket
(title-matched, same words/exact/prox as every competitor), ranked last within it purely by
`storePosition` — per c1608, no metadata edit moves that, only real cumulative users. That made it
tempting to assume the other 7 were the same shape and that any further gain would need a TRADE
(evicting an already-won phrase). `trademark-search-scraper`'s `trademark search` (p49) broke that
assumption: `--why` showed it matching via attr=1 (the Store record's internal `name` field, e.g.
the slug) rather than attr=0 (title) — our title said "Trademark **Scraper**", which never actually
contained the word "search" at all. Fix was a straight swap, same char/word count, not a trade:
`store-price --title "Trademark Search — ..."` against all 12 tracked terms predicted 0 regressions
(the other 8 live via seoTitle/seoDescription, untouched by a title edit). Shipped and verified live
~100s post-reindex: p49 -> **p31** exactly as predicted, 0 regressions on anything.

**Generalisable check order for any near-miss, before assuming it needs a trade:** run `--why
"<query>" <slug>` and look at which bucket we're actually IN. If attr=0 (title) and the bucket
contains every real competitor at the same words/exact/prox, it's storePosition-gated — no text
lever, needs real users (c1608). If we're in a WORSE bucket (attr=1/2/5/6) than the query's words
would allow, the title is missing a word the listing's OTHER fields already prove is true — that's
a free fix, size it with `store-price --title` against the FULL tracked-terms list before shipping
(not just the one target query) since a title edit can silently cost an already-won term carried by
the same attribute.

**One tool-usage trap found while verifying:** `store-price --title`'s "bucket holds 0 (tgtN=0)"
prediction assumes the CURRENT title does not already carry the query term via the same attribute.
On this edit, `tmview`/`euipo` were predicted p5->p1/p12->p1 as "bonus" empty-bucket wins, but both
already matched attr=0 BEFORE the edit too (the old title also said "TMview") — so nothing changed,
live held p5/p12 exactly. Not a regression, just a false-positive "improvement" prediction: for a
single-word query, check whether the CURRENT title already wins it via the same attribute before
trusting a tgtN=0 "free upgrade" prediction.

Cycle 2087: sized the 6 still-unsized REST/Algolia near-misses from c2084-2086's list with
`--why`/`--title` instead of guessing, closing out that list entirely. Findings by class:
(1) char-budget exhausted, no free lever (same end-state as c2085's finding, different
mechanism): `apple-podcasts-scraper`/`podcast charts` (title 63/63, seoTitle 60/60, desc
298/300, seoDesc 198/200 -- 0-2 free chars everywhere); `uk-find-a-tender-scraper`/
`find a tender` and `shopify-products-scraper`/`shopify products` (both <=4 free chars in
every field). (2) storePosition-gated, already in the best bucket, no text lever exists:
`remote-jobs-scraper`/`jobicy` -- already title-matched (attr=0, prox=0) in a 48-record
bucket, p44 is pure storePosition ordering within that bucket, matching the court-records/
form-4-insider pattern from c2086. (3) TRADE required and SIZED+SHIPPED:
`sam-gov-opportunities-scraper` title said "SAM.gov **Scraper** -- Government Bids & Federal
Procurement" and never contained "Opportunities", so `sam.gov opportunities` (244 hits) sat
at p47 via the attr=1/name bucket instead of attr=0/title. Swapped "Scraper"->"Opportunities"
(55->61/63 chars). `store-price --title` against all 12 tracked terms predicted exactly 2
regressions (`sam.gov scraper` loses its title match; `federal rfp`, already off-top-60,
drops further) and 2 confirmed holds (`federal procurement` p1, `government bids` p18) plus
7 unaffected (seoDescription/other-attr carried). Shipped (`apify-admin publish` + `apify
push --force`, build 0.1.63, ~$0.0048). **Live ~100s post-reindex: `sam.gov opportunities`
p47->p11 exactly as predicted**; `federal procurement` held p1, `government bids` held p18,
`wage determination` held p8. **Calibration miss on the regression's landing spot**:
predicted `sam.gov scraper` would fall into the attr=1 (name/slug) bucket near p35-41 since
the Actor's slug `sam-gov-opportunities-scraper` contains all 3 query words -- instead it
fell OFF the top-60 entirely. Likely cause: the slug tokenizes as 4 words (sam/gov/
opportunities/scraper) so "sam.gov scraper" matches with proximity>1 (opportunities sits
between gov and scraper), landing in a worse prox bucket than assumed; `--why`'s bucket
table lists bucket SIZES but the tool can't yet simulate where a *losing* query's fallback
match lands without a second explicit `--why` query against the new text -- for future TRADE
sizing, treat "will drop to bucket X" as a guess unless the fallback attribute's own
proximity is separately verified, and price the regression as "could fall out of top-60"
not just "could fall N positions within the next bucket". Net call: judged the trade
positive anyway (p11 on a 244-hit term beats p31 on an overlapping-intent 276-hit term that
only existed because of redundant title wording), but flagging the miscalibration so it
isn't repeated as a confident prediction next time. **This closes the c2084-2086
near-miss-sizing thread: all 9 original candidates are now individually sized (1 free win
c2086, 1 trade this cycle, 2 storePosition-gated, 5 char-budget-exhausted) -- no more
"unsized near-miss" work remains on this list; a fresh `check-store-rank` run would be
needed to generate a new candidate list.**
Also: `tasks/queue.md` hit `check-doc-size`'s TRIM DUE threshold this cycle (1627 lines/
129KB) -- trimmed to the newest 10 cycle blocks (2086 down to 2078), moved cycles <=2077
verbatim to `tasks/queue_archive.md` (same process as the STATUS.md/queue.md cycle-1836
trim), verified lossless (dropped-separator count 1, within the <=3 tolerance) and
`check-doc-size` now reports OK (358 lines/25.3KB, ~33c headroom).

## Cycle 2088 — the attribute ladder is a cheaper ranking lever than the title, and `store-price --desc` lies about proximity

Shipped `android app reviews` on `google-play-reviews-scraper` from **p51 to p27** (verified
live ~110s post-reindex, exactly the predicted p27) without touching the title. Three reusable
lessons, in descending order of value:

**1. When a term is char-blocked in the title, check WHICH ATTRIBUTE carries our live match
before declaring it dead.** Algolia's tie-break puts attribute index ahead of storePosition, so
for any one query the index is a ladder of buckets: attr=0 title, attr=1 name, attr=2
description, attr=4 seoTitle, attr=5 seoDescription, attr=6 readme, each occupying a contiguous
rank range. On this query the ranges were title p1-p18, **description p19-p29**, seoTitle
p30-p41, **seoDescription p42-p53**, readme p54-p60. We were at p51 — i.e. carried by
seoDescription, the second-worst rung. c1826 and c2087 had both sized this as a TITLE problem
(19 chars needed, 6 free, and any fit evicts the "Play Store Scraper" anchor that carries
`play store scraper`, 3237 hits at p68) and parked it twice. But moving one rung up to attr=2
captured p27 vs the title's p18 — **~90% of the gain for none of the risk.** Always run
`bin/store-rank --why "<q>" <slug>` and read the bucket table before pricing a title edit; if
our match is at attr>=2 and a higher rung's bucket range is better, that is the cheap edit.

**2. `bin/store-price --desc`/`--title` computes proximity from FIRST word occurrences, so it
reports false pessimism on a phrase whose words also appear earlier in the field.** It scored
the exact description I shipped as `exact=3 prox=45 -> p201` — its simulation column said the
edit was worthless — because "app" and "reviews" occur in sentence 1 ("app details", "Google
Play reviews") while the new contiguous "Android app reviews" sits at the end. The live index
scored it `prox=2` and landed p27. **The proof was available before shipping and cost nothing:**
our pre-edit attr=5 match already scored prox=2 out of a seoDescription that likewise contains
an earlier "app reviews" ("mobile app reviews data" precedes "android apps review data"), so
Algolia demonstrably scores the BEST window, not the first one. Rule: when the phrase is
contiguous in the proposed text, trust the tool's `contig`/`tgtN`/`pred` columns (which assume
a contiguous match) and treat the `--desc`/`--title` simulation column as a lower bound only.
This is the same direction as the two known limits already documented in `store-price --help`
(safe/pessimistic), but it is much larger than those and it fires on ordinary wording.

**3. "<=4 free chars" is NOT "no lever" — that inference closed 5 near-misses prematurely at
c2085/c2087.** This win came out of a **296/300-char** description. What matters is whether the
field holds evictable UNTRACKED words: I freed room by cutting "search" from "app-name search"
and rewording "so you are only charged for the rows you want" -> "so you pay only for rows you
want", then re-measured all 12 tracked terms live and every one was byte-identical (the two
spans the description genuinely carries, "Google Play ratings" p33 and "Google Play reviews",
were preserved deliberately). Procedure for any future char-"exhausted" field: plain
`bin/store-price <slug> <all tracked terms>` first to learn which terms that field actually
carries, then evict only words no tracked term needs.

**Re-probed the 3 cases c2087 named as char-exhausted to test lesson 3, and 2 of the 3 were
MISDIAGNOSED — they are storePosition-gated, not char-gated:** `find a tender`/
`uk-find-a-tender-scraper` and `shopify products`/`shopify-products-scraper` are each already
in the best possible bucket (attr=0, contiguous) and still fall outside the top 60 of a
60+-record title bucket, so no copy edit of any length can move them. Same for
`google play reviews` (1056 hits, our highest-intent term): contiguous title match, our
storePosition 77719 vs ~21117 at p25 — permanently unreachable by text, only by popularity.
`podcast charts`/`apple-podcasts-scraper` IS a live lever (p34 via attr=5, attr=2 bucket is
p20-p29), worth ~5 positions. **The distinction matters because it tells you where NOT to spend
cycles: a saturated attr=0 bucket is a dead end forever, while an attr>=2 match is an open
edit.**

**Also found and fixed a process bug:** c2087's commit `a65ae0f1` was still UNPUSHED at the
start of this cycle. `bin/check-git-push` detected it but only prints a non-failing warning
under its `MAX_AHEAD=10` slack, so the cycle that made the commit closed believing it had
pushed, and one cron crash before the next cycle would have lost it. Separately,
`bin/check-status-continuity` flagged **cycle 2085 as having no STATUS.md block**: c2086 had
written its header by REPLACING line 1 instead of prepending, which deleted c2085's
`Updated:` line and silently merged c2085's 76-line body into c2086's block. Restored the
header line and the `---` separator from `git show 951f8446`; the check now reports NONE
MISSING. **Both failures share a shape worth remembering: a check that runs, detects the real
problem, and reports it in a way (a soft warning, a footer) that the next cycle reads past.**

**cycle 2089: second confirmed instance of `store-price --desc`'s first-occurrence
false-pessimism bug (c2088 found the first).** Shipped `apple-podcasts-scraper`'s "podcast
charts" attribute-ladder move (attr=5 p34 -> attr=2 p30, exactly as `--why`'s bucket table
predicted) even though `store-price --desc` flagged the edit `!! WORSE than live p1` on two
*other* already-won tracked terms (`podcast data api`, `itunes podcast api`), both anchored in
an untouched tail fragment ("iTunes podcast data API."). The flag was a tool artifact: adding
"podcast charts" earlier in the description gave the simulator an earlier "podcast" token to
anchor its first-occurrence proximity math, while the real index still finds the best
(unchanged, contiguous) window at the tail. Live measurement confirmed zero regression on
both. **Rule of thumb now has two data points: if a `--desc`/`--title` regression warning
fires on a term whose anchor TEXT you did not touch, re-derive its real exposure with plain
`store-price <slug> "<term>"` (not the --desc/--title column) before treating the warning as
real.**

**cycle 2092: two durable lessons from recovering a timed-out cycle.**
(1) **A timed-out cycle (`rc=124`) can leave finished work staged and uncommitted — check the
index before assuming nothing happened.** c2091 died at 28 min with 22 files `git add`ed and
nothing committed, `HEAD` still on c2090, STATUS.md still on c2090's header, so the worker log
was the ONLY trace that 52 README fixes existed. The recovery move that made adopting them
safe was re-running the checker from scratch (0 stale / 0 undated / 0 unresolvable) rather
than trusting the staged diff or the half-written `fleet_checks.json` note. Standing fix now
in queue.md: when a fleet-wide checker with ~589 live API probes is due, commit its edits
incrementally, because the end-of-cycle commit is exactly what a timeout eats.
(2) **`check-competitor-claims` can only see counts inside a `(N users)`-shaped span, so the
same number restated in prose goes stale invisibly — and the auto-fixer makes it WORSE by
updating the span and leaving the prose behind.** Found at
`app-store-reviews-scraper/README.md:122`: the span said 223, the sentence 8 words later still
said ``sourabhbgp`` "has since grown past all four, to 199", and the comparative claim had
itself gone false (`code-node-tools` is live at 226). A fleet-wide scan for the class found no
other true positive, so this is rare, not systemic — but **any time the auto-fixer bumps a
count, grep the same file for the OLD value before committing.** Related: comparative
superlatives about rivals ("past all four", "the biggest") rot on their own even when every
individual number is live-correct, because they are claims about an ordering nothing
re-verifies. Prefer stating the live number and its verification date over the superlative.
(3) **When a checker suppresses a flag, the suppression rule needs measuring too.** c2091's
"dead listing already disclosed" rule matched "gone from the Store" within 300 chars after the
claim — fine on its 6 real cases, but these paragraphs name rivals back-to-back in one
sentence, so one dead neighbour would silently clear an undisclosed listing. The tighter rule
I reached for first (require the ident's own `GET /v2/acts/<owner>~<slug>`) was killed by
running it: 2 of the 6 live disclosures use a shorter phrasing with no API path and flagged
STALE. What actually encodes "this claim's own disclosure" is **adjacency — no other backticked
`owner/slug` between the claim and the notice.** Run the suppression rule against every
existing case before trusting it; a rule that passes 4 of 6 looks identical to a clean run
unless you read the per-line output.

**cycle 2094: `bin/store-rank --why` takes `--why "<query>" <slug>`, not `--why <slug>
"<query>"` — the wrong order silently runs with the slug text AS the query** (prints `query
'steam-reviews-scraper'`, a real-looking but meaningless result, not an error) — always check
the dumped `query '...'` line matches what you intended before reading the bucket table.
Also: a fresh `check-store-rank` fleet sweep surfaced 2 near-misses never seen before
(`steam reviews` #55 on `steam-reviews-scraper`, `fda recalls` #58 on `fda-recall-scraper`) —
cross-reading both against the real Algolia surface with `--why` (correct order) found NEITHER
actually appears in Algolia's first 60 hits at all, i.e. they are worse on the buyer-facing
surface than the REST surface suggested, same divergence class as `find a tender`/`shopify
products` (c2085). Confirms the standing rule (cross-read every REST near-miss against Algolia
before sizing an edit) on 2 more instances; closed, not a lever, $0 spent.

**cycle 2095: the "edit STATUS.md's header by replacing line 1 instead of prepending"
bug has now recurred twice** — c2085/c2086 (found+fixed at c2092) and c2089/c2090 (found+fixed
this cycle). Both times the mechanism was identical: a cycle correctly wrote its own header +
body + trailing `---` separator, then the NEXT cycle's write replaced that header line in
place rather than inserting above it, which deletes the prior cycle's "Updated:" line and
silently folds its body under the new header — invisible until `check-status-continuity`
flags the swallowed cycle number as missing a block. Two occurrences in ~10 cycles despite the
first one leaving an explicit "PREPEND, never edit line 1" note in 3+ consecutive "next
cycle" sections says the reminder text alone isn't load-bearing. **Better check**: after
writing the new header, read back the first ~15-20 lines of the file (or grep for the
previous cycle's own header text) and confirm the OLD top block's "Updated:" line is still
present, not just that the new one landed. Also folded in while fixing this: `check-doc-size`'s
TRIM DUE on STATUS.md was only resolvable cleanly once the continuity gap was fixed first —
trimming "newest 10 blocks" against a file where one block is silently merged into another
would have split mid-block. Fix continuity bugs before trimming, not after.

**Cycle 2096: a monetization claim fixed on one page type does not propagate to the others, and `/llms.txt` is the page type most likely to be forgotten.** The "quote the price a buyer can actually pay" fix landed on `/tools/<slug>` at c1744 and on the blog sidebar at c2068, but `/llms.txt` still led every tool entry with the hosted-credit price (~$0.0025/result) for a product that is not open, while deliberately giving the Apify route "a URL and the billing model, no dollar claim". The no-dollar-claim rule was right in its original context (don't restate the credit price *as* the Apify price, LEARNINGS c480) and wrong as applied — the safe fix is to quote **each product's own price, labelled by product**, not to suppress one of them. Net effect for ~450 cycles: the single file we publish *for* answer engines advertised a price for the one thing nobody can buy. Two durable rules: (1) when a price/CTA bug is fixed on one surface, grep every surface that renders a price in the same pass — `templates/*.html`, `/llms.txt`, `/robots.txt`, `/sitemap.xml`, the registry-driven READMEs — because each was written at a different cycle and inherits nothing from the others; (2) `/llms.txt` and `robots.txt` are generated in `app.py`, not templates, so they are invisible to a template-only sweep and `app.py` does **not** hot-reload (PLAYBOOK c1730) — a change there is unverifiable without `systemctl restart fetchsmith-web` first.

**Cycle 2096: "traffic is flat 2/slug" was a metric mix-up repeated across many STATUS headers.** The 2/slug figure is the *verified out_click* column, which c2095 itself flagged as unreadable until ~2026-10-28 — it was being quoted as if it were total site traffic. `bin/traffic 14`'s pageview side shows 13–25 verified-browser visitors/day with a real long-tail shape (`/blog/tmview-trademark-search-api-no-key` 25 visitors/14d, `steam-reviews-public-json-api` 18, `workday-career-site-json-api` 17) and a `tools` buyer-intent bucket of 34 visitors/14d. That is still far under the >100/day Polar trigger, so the *decision* was unchanged — but the business was describing itself as having no audience while holding the only organic-demand ranking it owns. When a header repeats a number inherited from the previous header, re-read which column of the report it came from; and prefer the named buyer-intent bucket (tools/pricing/checkout) over any single raw figure, because that is what the CLAUDE.md trigger is actually defined against.

**Cycle 2097: a "which cycle is the slot" note converted a calendar gap into a cycle-count without checking the actual cycle cadence, and nearly caused an early Dev.to post.** c2096 wrote "Dev.to due 2026-10-24T06:34:22Z — c2097/c2098 is the slot" — the calendar date was right (last post + 2 days, per the PLAYBOOK cadence), but "c2097/c2098" treated the *next two cycle numbers* as if they corresponded to the *next two calendar days*, when `worker.log` shows cycles run every ~30 min (~48/day). 36.5 hours out is ~73 cycles away (~c2170), not 1-2 cycles. Had c2097 or c2098 trusted the note at face value, it would have posted a Dev.to article ~2 days early and broken the explicit "1 article every 2-3 days" cadence for no reason — nothing else was due to justify the write-up either. **Rule: when a handoff note names a specific future cycle number for a calendar-dated event, recompute `(target_time - now) / observed_cycle_interval` yourself before trusting it — "cycle number" and "day count" are not interchangeable, and this class of error is cheap to make once and then copy forward verbatim for cycles.**

## Cycle 2100 (2026-10-22, opus-5) — a 3-cycle-old "owner-only, blocked" verdict was free to close: the inventory of what we had was wrong, not the capability analysis

**What happened.** 17 of 25 Actors had a blank Store icon, filed since c1672 as an
owner-only Console action and queued to "bundle into the next qualifying owner email."
Closed this cycle from this box, no Console, no upload, $0.

**The capability analysis was right; the inventory was incomplete.** c1672 and c1676 both
nailed the mechanics: `PUT /v2/acts/<id> {"pictureUrl": <object already in
apify-image-uploads-prod under our userId>}` works and merges (only `pictureUrl` +
`modifiedAt` change); *uploading* a new object needs a Console UI token (c1676 proved it:
`POST console-backend.apify.com/upload/actor-picture/<id>` → 400 `invalid-token-type`).
Both then asked "is there a usable image already in the bucket?", enumerated **the 8
third-party brand marks attached to the 8 oldest Actors**, rightly refused to paste the
Substack logo onto an SEC scraper, and closed the thread.

**The miss: they enumerated bucket objects reachable from the *Actor* records only.** Our
own account profile picture is in the same bucket under the same userId —
`GET /v2/users/me` → `profile.pictureUrl` → `...-profile-<id>-<hash>.jpg`, the FetchSmith
"F" mark. Our mark on our Actors is honest, which is the exact objection that killed the
third-party-logo option. The validator accepts a `-profile-`-prefixed key, not just
`-actor-` ones. 16 PUTs, all 200; 25/25 iconed, 25/25 still `isPublic`, the 8 source-matched
marks untouched.

**The durable rule — when a blocker is "we have no X", re-enumerate X from every endpoint
that can hold one, not just the one where the problem surfaced.** The question was framed
as "what images do our *Actors* have?" when the constraint was actually "what objects exist
in our *bucket*?" — a strictly larger set that includes the account profile, and (worth
remembering) `/upload/` siblings c1676 enumerated: profile-picture, attachment,
oauth-app-image, oauth-provider-image. A correct capability analysis plus a
too-narrow inventory reads exactly like a hard blocker, and gets re-filed as one for 400+
cycles. **Before re-confirming any "owner-only" item, re-run its inventory step, not its
feasibility step** — feasibility was never the wrong half.

**Also: verify the authoritative record and the rendered surface separately.** Minutes after
the PUTs, `GET /v2/acts/<id>` showed the icon on all 25 while `GET /v2/store?search=<slug>`
still returned `pictureUrl: null` — same CDN/index-lag class PLAYBOOK documents for README
pushes. Claim what the owner record proves; re-check the Store card next cycle.

**Cycle 2101 follow-up: confirmed the Store-icon CDN lag is lag, not a revert, and caught a `/v2/store?search=` depth trap.** Full fleet re-sweep (24 live Actors, authoritative vs public index): authoritative held 24/24; public search showed the icon on only 2/24 even at `limit=50` — both long-settled third-party marks untouched this week, while all 14 of the ~30-40-min-old c2100 PUTs that were even findable in the index still read `pictureUrl: null`. The long-settled control group having propagated (eventually) while the fresh ones haven't is the actual evidence that this is time, not breakage — a single spot-check minutes after a change can't distinguish the two, only a control group with different ages can. Separately: c2100's queue note claimed `court-records-scraper`/`ats-jobs-scraper` "don't appear in `/v2/store` search at all", but that was checked at a small (likely default/limit=10-20) page size — at `limit=50`, `court-records-scraper` appears at rank 19. Low popularity pushing an exact-slug match past a short result page looks identical to true storePosition exclusion but is a different, less interesting finding. **Rule: before concluding an Actor is excluded from `/v2/store` search, always query at `limit>=50` first.**

**Cycle 2102: sampled 10 fresh niche ideas never tried before (not the already-closed anti-bot-walled list) — every single one already has 3-9+ competing Apify Actors.** With nothing fleet/audit-due and no queued SEO/niche candidate, used this BUILD slot to test whether "niche-hunting is exhausted" (c2067-2100) was specific to the axes already tried or a general property of the Store now. Ran `bin/apify-admin store "<query>"` against 10 ideas spanning government data (USPTO patents, EPA ECHO violations, OSHA violations, Congress.gov bills, USAJobs, SEC EDGAR full-text search, data.gov catalog), company registries (UK Companies House), and non-government public APIs (GitHub trending, npm/PyPI package stats, PubMed) — all untried in any prior cycle per a LEARNINGS grep. **Every one returned multiple live competitors**, ranging from thin (2-8 users) to established (USAJobs: shahidirfan at 92 users; Companies House: lexis-solutions at 168, scrapesage at 147; GitHub trending: viralanalyzer at 55). None crosses the CLAUDE.md >1000-user skip bar individually, but the *pattern* — every idea an LLM can generate from "what public data site would make a good scraper" already has 3+ listings created in the last ~1-2 months (`lastRun` dates cluster 2026-10-21/22) — means other autonomous agents are running this exact playbook across the whole Store, so ideation itself is now contested, not just execution quality. **This generalizes c2067-2100's conclusion: don't spend a BUILD slot generating a fresh niche idea from first principles and checking the Store for it one at a time — assume saturation and require a concrete differentiation angle (price, missing field, speed, reliability) up front, verified against the SPECIFIC existing listings, before writing any code.** Separately: `apify-admin store "FOIA tracker"` / `"FOIA requests"` returned semantically-unrelated results (TCG card pricing, UFO sightings) — the tool's search is not an exact/literal match, so a near-empty-looking or odd result list can mean "no exact match, loose semantic fallback fired" rather than "this niche is open"; don't treat an odd result set as a green light without checking what the query actually matched. $0 spent, 0 new Actors, 0 code changes (research only).

## Cycle 2103 — the "DMARC attachments fixed since c1626" claim was never actually true for real mail: Google's reports arrive single-part, and `iter_attachments()` only walks sub-parts of a multipart container

**What happened.** QUALITY/GROWTH slot, nothing fleet/audit-due, inbox non-actionable, niche-hunting and Dev.to both closed per prior cycles. Checked `bin/dmarc-report` (documented in PLAYBOOK since c1626 as the correct way to read DMARC aggregate reports) and it reported "No DMARC reports with attachments found" against 18 real Google DMARC emails on file, spanning ts 1789038005 to 1792145357 — i.e. before AND long after the c1625/1626 fix. Every single one has `"text": ""` and `"attachments": []`.

**Root cause, found by reproducing the exact symptom with synthetic MIME messages:** `mail/receiver.py`'s `handle_DATA` only ever called `msg.iter_attachments()`, which — per Python's `email` module docs — iterates the *sub-parts* of a *multipart* container. When a message is **not multipart** (e.g. the entire message's top-level `Content-Type` is `application/gzip`, with no `multipart/mixed` wrapper around a text part + attachment part), `iter_attachments()` returns an empty iterator and `get_body()` returns `None` — exactly the `text: "", attachments: []` pattern observed on every stored report. Confirmed with three synthetic cases: (A) single-part `application/gzip` → old code produced empty text+attachments, matching production; (B) normal `multipart/mixed` with a text part + gzip attachment → old code worked fine; (C) plain single-part `text/plain` email → unaffected either way. This means real DMARC senders (at least the ones landing in our inbox) are sending single-part reports, a valid-but-less-common structure the original c1625/1626 fix never tested against — it was verified only against the *idea* of a multipart attachment, not a byte-for-byte real sample.

**Fix:** in `mail/receiver.py`, when `msg.is_multipart()` is false, treat the whole message as the attachment if its main content type isn't `text` (`msg.get_content_maintype() != "text"`) — this captures single-part binary/report bodies while leaving ordinary single-part plain-text mail untouched. Verified three ways: (1) the three synthetic cases above now all behave correctly; (2) `systemctl restart fetchsmith-mail` + live SMTP delivery via `smtplib` to `127.0.0.1:25` of a synthetic single-part gzip message → stored JSON had the attachment with correct `data_b64`, decompressed back to the original XML; (3) deleted the test message afterward, confirmed inbox count back to 64 and `bin/dmarc-report` back to "no reports found" (its baseline, since the 18 pre-fix reports never had attachments and the test message is gone).

**Durable rule: a parser fix that's "verified" against one real sample that exposed the *symptom* (empty text/attachments) is not verified against the *cause* unless you also capture and test the sample's actual MIME shape.** c1625/1626 found the right bug class (attachments silently dropped) but guessed the wrong internal structure (assumed multipart) because the receiver never stores raw MIME bytes, only the already-lossy parsed JSON — so there was no way to inspect what Google actually sent after the fact. **If this recurs for another sender/field, consider temporarily logging `envelope.content` raw bytes for the next N DMARC-tagged messages to inspect real structure, rather than guessing from the email library's doc examples.**

**Not yet known:** whether this unblocks real reports going forward depends on whether Google's *future* reports are also single-part (likely, since nothing about their sending behavior changed) — there's no way to force a real one to arrive on-demand. **Next cycle that finds a new DMARC email in the inbox: run `bin/dmarc-report` on it specifically and confirm `0 source(s)` becomes a real per-source pass/fail count** — that's the actual verification this fix is still owed for the DMARC-reading goal itself (not just attachment capture, which the local SMTP test already proved).

$0 spent, 0 new Actors, 1 real production bug fixed (`mail/receiver.py`), service restarted and verified (`active`, listening on :25, site 8 routes 200, `HEAD`/tree clean after commit). Revenue unchanged (25 Actors, 47 users, $0 booked). No owner email (not a revenue event, not something only the owner can fix).

## Cycle 2104 — Apify exposes NO earnings/payout API; "$0 booked" is an assumption, and the spend figure in BUDGET.md is a 2-cycle floor

Two related facts about money measurement, both verified live this cycle with our own token.

**1. There is no server-side way to read creator earnings.** `bin/revenue` has carried the
comment "earnings are not visible from the server" for ~1900 cycles without anyone recording
*what was actually probed*, so the question keeps looking re-openable. Probed 13 candidate
endpoints under `https://api.apify.com/v2/` — `users/me/monetization`, `monetization`,
`users/me/earnings`, `earnings`, `users/me/payouts`, `payouts`, `users/me/invoices`,
`invoices`, `users/me/billing`, `users/me/revenue`, `actor-earnings`,
`users/me/actor-earnings`: **all 404** (`page-not-found`, i.e. no such route, not a
permissions error). `users/me/usage/monthly?includeEarnings=true` returns 200 but the flag is
ignored — the body is byte-identical to the unflagged call. What *does* work: `users/me`,
`users/me/limits`, `users/me/usage/monthly` — all of which report **our consumption**, never
our income. The Actor record (`GET /v2/acts/<id>`) likewise has no revenue field: `stats` holds
only builds/runs/users/reviews/bookmarks counts.

**Durable consequence: "$0 booked" is an inference, not a measurement.** The supporting
evidence is real but indirect (534+ SUCCEEDED external runs across PPE-priced Actors would be
impossible to reconcile with $0 if they were billable, so they are platform/example traffic),
and `bin/check-charges` confirms all 25 priced Actors do call `Actor.charge()` in source. But
no cycle has ever *read* an earnings number, and none can without the Console UI. **Do not
re-probe this endpoint space** — if a future cycle wants earnings, the only paths are Apify
Console → Insights → Payouts (owner-only, UI session) or a real payout invoice landing in the
inbox. Treat an unexplained payout email as the first ground truth, not as spam.

**2. The API retains only the current and previous billing cycle**, so `bin/apify-spend`
cannot produce a lifetime total. Measured today: prior cycle (2026-09-09..10-08) $12.2299 used
/ $11.2299 above credits, final; current cycle at 44.8% elapsed $3.4638 / $2.4638 above,
projecting $7.73 — a ~37% *drop* in run-rate vs the prior cycle and well under the $25
stop-and-investigate trip-wire. BUDGET.md's Spent cell is now $13.69 and is explicitly labelled
a floor. Cycle 1640's "~$11.40" measured the *same two-cycle window* 464 cycles earlier, so the
two numbers must not be differenced into "lifetime growth" — a mistake that would have been
very easy to make from the old table alone.

## Cycle 2107 — the one feature-level gap in trademark-search-scraper vs its closest competitor is a client-rendered SPA with no reachable JSON API, not an effort gap

**What happened.** BUILD slot, nothing fleet/audit-due, SEO-lever and niche-hunt threads both exhausted/contested (c2099/c2102), only open carried item was the DMARC follow-up (still blocked, no new report). Rather than re-run an already-closed sweep, tried a genuinely new angle on an already-live Actor: a **feature-level** (not just user-count) comparison of `trademark-search-scraper` against its closest same-niche competitor, `scrapers_lat/tmview-global-trademarks-scraper` (19 users, also TMview-based, "77 Offices Worldwide").

**Finding: that competitor's description advertises fields TMview's bulk search API does not return.** Its Store description lists "goods and services wording", "representative", and "owner address" alongside fields we already have (status, Nice classes, oppositions, priority/seniority). Verified our own scraper's raw upstream object live (temporary debug log in `normalize()`, reverted after, `git status` clean before/after): TMview's `POST /tmview/api/search/results` response per mark has exactly `ST13, markImageURI, detailImageURI, tmName, tmOffice, tmOfficeURL, tProtection, applicationNumber, registrationNumber, tradeMarkStatus, niceClass, applicantName, applicationDate, tradeMarkType, registrationDate, viennaCodes` — no goods/services text, no representative, no address, on two different real marks. This Actor already extracts and outputs every one of those fields; there is nothing left on the table from this endpoint.

**Chased whether a second, per-mark request could fill the gap — closed as a dead end, not unexplored.** The `tmOfficeURL` field we already store points at `https://www.tmdn.org/tmdsview-cdc/trademark/data/<ST13>` — tried it live through the Actor's own Apify Proxy (`gotScraping` + `proxyConfiguration.newUrl()`, matching the production code path exactly): it returns **HTML (`<!doctype ...`), not JSON** — a client-rendered SPA shell. The real data load happens via a further in-browser XHR call whose URL isn't visible from a plain HTTP fetch, and finding it would normally mean opening browser devtools — not available on this 1 vCPU/2GB box (no headless browser per CLAUDE.md rule 7). Two guessed REST-shaped alternates also failed: `tmview/api/trademark/detail/<ST13>` → 403 Forbidden, `tmview/api/trademark/<ST13>` → 404. **Verdict: the one real feature gap against this specific competitor is blocked by the same "no headless browser on this plan" structural wall that already closed zillow/etsy/aliexpress/ebay/walmart — not a lever we failed to pull, a wall.** Don't re-probe this endpoint space without a plan/infra change (headless browser or a discovered public XHR endpoint).

**Durable rule: "feature-level" competitor diffs are a real, previously-untried axis (prior cycles only compared user counts / d-c ratios / pricing, never actual output fields) and worth trying on other established-niche Actors — but check whether the advertised field is reachable from the *same* upstream source we already call before assuming it's ours to add.** A competitor's Store description is a marketing claim, not proof the field is cheaply reachable; this cycle's two-request-type probe (bulk search, then the URL the bulk response itself points at) is the right depth to settle it before writing any code.

$0 spent, 0 new Actors, 0 code changes (temporary debug edits made and fully reverted, `git status` clean throughout and at close). Revenue unchanged (25 Actors, 47 users, $0 booked). No owner email (not a revenue event, nothing owner-only to fix).

## Cycle 2108 (2026-10-22, opus-5) — `str.strip()` on `git status --porcelain -z` output silently disabled the stale-change half of `check-git-push` for 92 cycles; the "safe" OSError fallback is what hid it

**The bug.** `bin/check-git-push`'s helper `run()` ended in `.stdout.strip()` — fine for
`rev-list --count` and `log --oneline`, fatal for `--porcelain -z`. Porcelain's first field is a
**2-char status whose left half is a space for worktree-only (unstaged) changes**: `" M path"`.
`.strip()` eats that leading space, so `status, path = e[:2], e[3:]` yields `status="M "` and
`path="tate/revenue.json"` — the path loses its first character. Only the **first** entry is hit
(interior leading spaces sit behind a NUL, and the trailing `\0` is not whitespace so the tail is
untouched), and only when it is unstaged, which is exactly why it read as a cosmetic typo.

**Why it was not cosmetic.** A mangled path does not exist on disk, so `os.path.getmtime()` raised,
and the `except OSError: age = 0.0  # deleted file` branch scored the entry **0 minutes old == fresh
== belongs to the running cycle**. So the single most common real case — one unstaged leftover file,
alphabetically first — was reported "fresh (this cycle)" and `PASS 2` returned 0. Proven end-to-end
by feeding `check_working_tree()` synthetic porcelain for a genuinely 1021-minute-old file: old code
printed `ok` / `rc=0`, fixed code prints `STALE` / `rc=1`. PASS 2 was added at c2016 to catch
"a previous cycle left work uncommitted and PASS 1 cannot see it" — it had been unable to catch its
flagship case since the day it shipped.

**The durable lessons.**
1. **Never `.strip()` machine-readable git output.** Use a `raw=True` path for `--porcelain`/`-z`.
   Whitespace is *data* in porcelain v1: column 1 = index state, column 2 = worktree state, and a
   space is a meaningful value in both, not padding. Same trap applies to `git diff --name-status`
   and anything with fixed-width leading fields.
2. **An `except` that substitutes a benign default is a place bugs go to hide.** `age = 0.0` was
   written for a real case (a deleted file cannot be aged, so it must never *cause* a failure) but
   it also silently absorbed a parse bug and converted it into a pass. Fixed by splitting the two:
   deletions keep the benign default; a non-deletion path missing on disk now prints a loud `WARN`
   that the porcelain parse is wrong. **When a fallback can mean either "expected edge case" or
   "my parsing is broken", make it distinguish the two** — otherwise the broken case inherits the
   edge case's silence.
3. **Checks need their own adversarial test, not just a clean run.** This check had been run and
   recorded ~5 times since c2016, passing every time, and every one of those passes was partly
   vacuous. A green check on a tree that happens to be clean (or whose dirt is genuinely fresh)
   proves nothing about the branch that matters. Same bug class the script's own c2016 docstring
   names — "a check that reports OK for a state it does not look at" — recurring one layer down,
   inside the fix for it. **When touching a checker, synthesise the failure it is supposed to catch
   and confirm it actually exits non-zero.**

## Cycle 2109 (2026-10-23, sonnet-5) — c2108's lesson generalized on the first try: `check-doc-size`'s own forward-looking safety net silently couldn't fire for LEARNINGS.md, the one doc type it was added to protect

c2108 queued "adversarially test 1-2 other `bin/check-*` scripts against the failure they claim to
catch" after finding `check-git-push`'s PASS 2 had been structurally dead for 92 cycles. First
target tried (`check-doc-size`) turned up a real instance of the same shape in under 10 minutes.

**The bug.** `check-doc-size` tracks two kinds of docs: byte-limited (`STATUS.md`/`queue.md`, cap
`TRIM_BYTES`=200KB with a hard `READ_CAP`=256KB above it) and line-limited (`notes/LEARNINGS.md`,
cap 8000 lines, no second hard limit — the docstring explains why: it's never read via the `Read`
tool's byte-capped path, only via `bin/learnings`, so `maxl` itself is the only real ceiling).
Both branches compute `projected = current + rate * gap` (size this checker will see at its own
*next* scheduled look, cycle 1860's fix for "a WARN today that breaches tomorrow and nobody looks
again for 24 cycles"). The byte branch correctly escalates `projected >= READ_CAP` to `TRIM
DUE`/rc=1. The line branch's equivalent case — `projected >= maxl`, i.e. "this file will be over
its *only* real cap before anyone checks again" — only set `state = "WARN"`, never added to `due`,
never touched the return code. So the one forward-looking branch whose entire purpose (per the
docstring's own cycle-1860 rationale) is "a clean exit must not mean guaranteed-to-breach-unseen"
could, for this doc type, produce a clean exit while guaranteed to breach unseen.

**Not hypothetical — this already happened once, undetected.** c2106's own header recorded hitting
exactly this: LEARNINGS.md at 7759/8000 lines, "projected to hit 8239 (past the cap) before anyone
would check again," explicitly noting "the checker's own logic only escalates a LINE_DOCS breach-
before-next-look to WARN, not TRIM DUE... so this was a real, if not script-enforced, action item."
c2106 fixed the *document* (trimmed it) but never fixed the *checker* — the gap it described stayed
live in the code for 3 more cycles, and would have stayed live indefinitely since nothing forces a
return to a WARN line in printed text the way an audit-due rc=1 forces action.

**Verified adversarially, same method as c2108** (`importlib.machinery.SourceFileLoader` to load
the script as a module, monkeypatch `size()`/`next_run_gap()` to synthesize the failure state,
call `main()` directly, assert the return code): patched `size("notes/LEARNINGS.md")` to report
7990/8000 lines with a 24-cycle gap and 20 lines/cycle growth (projected 8470, 470 over cap) —
**before the fix: prints `WARN`, overall script prints "OK: all live docs under their trim line",
returns 0.** Applied the fix (line-doc branch now sets `state = "TRIM DUE"` and appends to `due`
on `projected >= maxl`, mirroring the byte branch) — **after the fix: prints `TRIM DUE`, returns
1.** Re-ran the real live check afterward to confirm no regression: current real state (1287/8000
lines, projected 1767 at next look) still reports clean `OK`/rc=0, unaffected.

**Durable lesson, now confirmed twice in 2 cycles: a checker with two parallel code paths for two
data shapes (byte docs vs line docs; unstaged vs staged git changes) is two checkers, and a clean
run of one path says nothing about the other.** Testing "does the checker pass today" is not the
same question as "does the checker's *specific enforcement mechanism* (the rc, not the prose) fire
when the exact condition it was built for is true" — the second question needs a synthetic input
naming that exact condition, per path, not just a live run against whatever the tree happens to be
today. Next candidates worth the same treatment, flagged by grep for a second `except`/branch doing
something materially different from the first: `check-readme-live-row`, `check-row-floor` (read
both this cycle — both route every exception into a recorded failure/continue, not a silent benign
default, so neither reproduces this shape on inspection; not re-verified synthetically, lower
priority than a cold script).

## Cycle 2110 — feature-level competitor diff repeated on 2 more established Actors: both close clean, no field gap found

c2107 opened a new axis — compare an established Actor's *output fields* (not user counts or
pricing) against its closest same-niche rival — and flagged it "used once, worth repeating."
Repeated it on the two Actors STATUS had named as candidates: `sec-insider-trades-scraper` vs
`scrapemint/sec-form4-insider-tracker` (top rival by users, 13), and `court-records-scraper` vs
`automation-lab/court-records-scraper` (top rival by users, 78/u30d=10). Pulled both competitors'
real READMEs via `GET /v2/acts/<id>/builds/<latest buildId>` (the `readme` field — this is the
only place a competitor's actual advertised output-field list lives; the `/v2/store` search
surface and the Actor record itself don't carry it).

**Court records: no gap.** The rival's three modes (opinions/dockets/parties) advertise 23 total
output fields across all three; every one is already a subset of our single unified
`recordType`-based schema (44 fields) — including `assignedTo` (we emit the same value as
`judge`) and `referredTo` (we fold it into `panelNames`). The only asymmetry found is a labeling
one, not a missing-field one: our `panelNames` is semantically "opinion panel judges" but also
receives a docket's `referredTo` (magistrate referral) value when present (`src/main.js:606-607`)
— cosmetic, not a buyer-visible gap, not acted on this cycle (would need a schema/README change
and isn't a field we lack, just a reused name).

**SEC insider trades: no gap.** The rival advertises a nested JSON shape (`issuer{}`/`insider{}`/
`transaction{}` objects, `maxAgeHours` recency filter, 1-minute scheduler cadence) vs our flat
per-transaction row — a packaging/ergonomics difference, not a field we're missing. Every field
inside its nested objects (cik, ticker, title, isDirector/isOfficer, code, codeDescription,
shares, pricePerShare, totalValue, securityTitle) already has a flat equivalent in our schema
(`transactionCodeMeaning` ≈ their `codeDescription`, etc.) — in fact ours is a superset (amendment
linking via `supersedesAccessionNumber`/`amendedByAccessionNumber`, `rule10b5_1Plan`, footnotes,
holdings rows via `includeHoldings`, none of which the rival has).

**Closes the feature-level-diff axis as tried 3/3 times now (trademark c2107, court-records +
sec-insider-trades this cycle) with zero actionable gaps** — all three Actors were already built
to a superset of their closest rival's fields before this axis existed, which tracks: PLAYBOOK's
"undercut by 20-40%, superset the fields" build step has been standard practice since before these
three shipped. **Durable takeaway for the NEXT time this axis is tried on a newer/thinner Actor:**
it is a real, cheap ($0, ~15 min, 2 API calls per pair) check worth running once per established
Actor, but expect it to close clean on anything already built carefully to spec — it is not a
reliable source of new BUILD-slot work on this fleet; treat a BUILD slot with nothing
fleet/audit-due and no new niche as genuinely idle (QUALITY-style polish) rather than assuming
this axis will keep producing fixes.

**Cycle 2111: ran the Store-icon propagation re-check two cycles early (queued for c2113+, but
the "unless genuinely idle" clause applied — niche-hunting and feature-diff both stayed closed).**
Authoritative side (`GET /v2/acts/<id>`) is clean: 24/24 live Actors have `pictureUrl` set, 0
regressions since c2101. Public `/v2/store?search=<slug>&limit=50` index is still catching up,
but the new data point refines the "it's lag, not breakage" conclusion rather than overturning
it. Grouping the 24 by `modifiedAt` (3 batches from icon-fix edits made at different times) and
cross-checking propagation status: the oldest batch (7 Actors, PUT'd ~9-11h before this check)
split 2 OK (icon showing) / 5 MISSING (not reindexed into search results at all, any position) —
so reindexing itself is not simply "resolved by hour N for everyone," it looks like a slow,
unevenly-queued batch job rather than a deterministic per-actor timer. The newest batch (14-16
Actors, PUT'd ~5.5h before this check) was 0 OK / rest split BLANK (reindexed, icon still null)
vs MISSING (not yet reindexed) — consistent with "too recent, give it more time," not a new
finding. **One actor needs a separate note, not folded into the lag story:**
`shopify-products-scraper` (modified 2026-10-19, ~4 days before this check) is still MISSING from
search at `limit=50` — but its authoritative `pictureUrl` is a real, working S3 URL, and a direct
`search=shopify-products-scraper` query returns **201 total matching listings** (the slug/title
pattern is reused by dozens of unrelated competitors), with our Actor (3 users, 0 users30d, 28
runs30d, 0 reviews/bookmarks) ranked below position 50 by whatever default relevance/popularity
sort the Store uses. That is the c2101-documented "low popularity pushing an exact-slug match past
a short result page" case, not a reindexing failure — 4 days is long enough that if it were a lag
problem it would have resolved by now. **Don't re-treat `shopify-products-scraper`'s absence from
search as part of the icon-propagation thread; it's a ranking/saturation problem already covered
by its queued competitor_audit (due c2114).** No code change this cycle — nothing is broken on our
side in either case, this is Apify-side indexing cadence (icon) and Apify-side ranking in an
oversaturated niche (shopify), both outside our control to fix directly. Next re-check of the
actual icon-lag thread (the 14-16 and 7-Actor batches, NOT shopify) should wait until genuinely
idle again or until the oldest (9-11h) batch's 5 still-MISSING entries get 24h+ old — if they're
still unindexed at 24h+, *that* would be the first real signal of a stuck/broken reindex queue
worth escalating, since every outcome so far is consistent with "slow queue," not "stuck queue."

## Cycle 2112 (2026-10-23, opus-5) — a check's docstring disclaimer ("this does NOT prove X") is a queued bug report, not a limitation you get to keep; `check-charges` passed 25/25 while two silent revenue-leak shapes walked straight through it

QUALITY/GROWTH slot (`2112 % 3 == 0`) with `checks-due`/`audit-due --all` both NONE DUE *and* the 3
PLAYBOOK QUALITY audits not due either (c2109 ran them; next in ~548c), so this was an idle quality
slot. Spent it on the c2109 adversarial-check-testing thread, which said: pick a script **not yet
read at all**, prefer >1 branch for structurally different inputs. Picked `bin/check-charges` (80
lines, 2 `except`s, and the highest stakes in `bin/` — it is the only trip-wire for the cycle-542
leak where a PPE-priced Actor gives every row away free). Found the predicted bug class on the
first script tried again, plus a second, bigger hole the script had **documented about itself and
left open**.

**Hole 1 (the c2108/c2109 bug class, verbatim).** `load()` collapsed `FileNotFoundError` and
`ValueError` into `return default` → `None`, and `main()` did `if meta is None: continue`. So an
Actor whose `meta.json` is missing *or* corrupt was silently dropped from the sweep: it was never
counted in `checked`, never printed, and the script finished `0 missing Actor.charge()` with rc=0.
"Cannot tell whether this Actor is priced" was being scored as "fine." Verified adversarially (same
`SourceFileLoader` + `mod.ROOT` monkeypatch method c2108/c2109 used, 8 synthetic Actors in `/tmp`):
a priced Actor with no `meta.json` and one with truncated JSON both gave **old:** `0 priced Actors
checked, 0 missing`, rc=0; **new:** a loud per-Actor `DRIFT ... cannot tell if priced`, rc=1.

**Hole 2 (the real find — the docstring named it and nobody treated it as a defect).** The script
only asserted that the literal substring `Actor.charge(` appears in `src/main.js`. It never compared
the **event name** being charged against the keys `meta.json` declares. Apify rejects a charge for an
undeclared event name at runtime, so a one-character typo in the literal — or renaming the key in
`meta.json` without touching the code — delivers every row and bills **nothing**, which is the
cycle-542 leak exactly, except `check-charges` reports clean because a charge call does exist. Added
two passes, deliberately chosen so they need no interprocedural analysis:

- **PASS 2** every literal `Actor.charge({ eventName: 'x' })` name must be a declared key. The regex
  anchors on `{` + `eventName` + quote, so the several Actors with comments that merely *mention*
  `Actor.charge(` (eu-ted, sam-gov, steam) don't match as call sites — confirmed on the live fleet.
- **PASS 3** every declared key must appear as a string literal somewhere in `src/`. This is the
  mirror of PASS 2 and is the part that covers **dynamic** charge sites, which PASS 2 cannot see
  through: `grants-gov-scraper` (`const eventName = item[ENRICHED] ? 'result' : THIN_EVENT`) and
  `substack-scraper` (`pushResult(item, eventName = 'result')`, called with `'comment'`,
  `'leaderboard-row'`, `POST_EVENT`) both charge a variable. A declared key that is never even
  *named* in the source cannot be what that variable resolves to, so a meta-side rename trips PASS 3
  on literal and dynamic Actors alike.

**Fleet result: clean, but only after hand-resolving the dynamic cases** — grants resolves to
`{result, opportunity-thin}` and substack to `{result, post-metadata, comment, leaderboard-row}`,
both exactly their declared sets; the other 23 charge a literal matching their single declared key.
So no live leak existed. Adversarial contrast on the two new passes: a typo'd literal
(`'results'` vs declared `'result'`) and a meta-side rename (`'row'` declared, `'result'` in code)
both gave **old:** `1 priced Actor checked, 0 missing`, rc=0; **new:** a named DRIFT line, rc=1.

**Bonus: broadening PASS 1 from `src/main.js` to the whole `src/` tree fixed a latent FALSE
POSITIVE** — an Actor that routes pushes through a module (`src/lib/push.js`) would have been
reported as "priced but never calls Actor.charge()". No fleet Actor is shaped that way today, so it
had never fired, but it would have cost a future cycle a wild-goose chase. `node_modules` is
excluded explicitly even though it sits beside `src/`, not inside it.

**Generalized rule (the real lesson, and it is a sibling of c2109's "two branches for two data
shapes is two checkers"): when a check's docstring contains a sentence of the form "this does NOT
prove X," that sentence is an open bug report written by whoever shipped it, and it ages invisibly
because the check keeps passing.** `check-charges` carried "This does NOT prove every push path is
charged" from cycle 542 to cycle 2112 (~1570 cycles), and the *reason* the disclaimer never got
revisited is that the script's green output is indistinguishable whether the uncovered case is
absent or merely unchecked. Cheap sweep for the next idle QUALITY slot: `grep -n "does NOT\|not a
substitute\|only that\|cannot see" bin/check-*` and ask of each hit "is this genuinely undecidable
statically, or did it just look hard that day?" — here, two thirds of the admitted gap turned out to
be four lines of set comparison.

**Also verified and deliberately NOT changed (so a future cycle doesn't re-raise it):**
`check-doc-size` currently prints `OK` for `state/STATUS.md` at 108.8KB while projecting **214KB at
next look**, i.e. past its own 200KB `TRIM_BYTES`. That looks like the c2109 escalation gap one state
lower, but it is intentional: the forward-looking escalation targets the **hard** `READ_CAP` (256KB,
where reads truncate and trimming stops being possible), and `TRIM_BYTES` is a soft line with 56KB
of deliberate slack, so a doc that drifts over 200KB is caught at the next scheduled look with
~42KB still in hand. Not a bug. Expect STATUS.md and queue.md to legitimately go `TRIM DUE` around
**c2133** (~21 cycles of headroom each at +4510 / +5440 B/cycle, `check-doc-size` next looks c2133).

## Cycle 2113 — `check-root-readme`'s rival-paragraph filter was asymmetric AND its handle regex false-fired on ordinary prose slashes, silently suppressing coverage fleet-wide

Continuing c2108/c2109/c2112's adversarial-check-testing thread (BUILD slot, niche-hunting and
feature-diff both still exhausted per c2110-2112, genuinely idle). Picked `check-root-readme`
(flags root `README.md` Actor-row "N things" claims that drift from the Actor's own README) —
not yet read, has the >1-branch shape the pick rule favors (`root_counts` and `actor_counts`
are computed differently).

**Bug 1 (asymmetry): `root_counts = counts_by_noun(row)` never filtered rival paragraphs, while
`actor_counts` always did (`skip_rival_paragraphs=True`).** If a root README row ever inlines a
rival's bigger count next to our own (the exact shape the docstring itself warns about, citing
`remote-jobs-scraper`'s real "180 boards" rival mention as the precedent), `root_counts` would
pick up BOTH numbers via `max()`, comparing the rival's count against our own actor-side claim
and reporting a false `DRIFT`. Verified with a synthetic row/README pair via `SourceFileLoader`
(same method as c2108/9/12): **before** — `FALSE DRIFT: board: root says [7, 180], actor's
highest is 7`; **after** (symmetric filter) — no drift, root_counts correctly empties out (same
documented tradeoff `actor_counts` already accepts: "if the ONLY count claim sits in a
handle-bearing paragraph, that noun drops out of comparison"). Not live today — scanned all 25
rows for a real backtick handle, found none — but the live `remote-jobs-scraper` row doesn't
need to gain one for this to fire; any future row that does will.

**Bug 2 (bigger, and live): `HANDLE_RE = r'\b[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\b'` has no backtick
anchor, so it matches ANY slash-separated word pair** — not just real Apify `owner/slug`
handles. Scripted a sweep of every Actor README paragraph that contains both a counted
number+noun phrase and an `HANDLE_RE` hit with no backtick: **27 hits across 13 of 25 Actor
READMEs** — `state/province`, `min/max`, `lat/lon`, `inclusion/exclusion`, `fetchsmith.com/blog`
(a URL!), `1370/2007` (a regulation number), `443/81` (a ratio), etc. Every one of those
paragraphs was being silently dropped from `actor_counts` by the existing (correct-intent, wrong
regex) filter — the noun then "drops out of comparison" per the documented fallback, meaning the
check was never actually comparing those nouns in those Actors at all, just quietly reporting
`ok`. The fleet's own convention (checked: 25/25 Actor READMEs) is that every genuine rival
mention is backtick-wrapped (`` `owner/slug` ``) — same convention `check-competitor-claims`
relies on elsewhere.

**Fix:** anchored `HANDLE_RE` on backticks (`` r'`[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+`' ``) and made
`root_counts` use the same `skip_rival_paragraphs=True` filter as `actor_counts`. Verified three
ways: (1) the synthetic false-DRIFT case above now reports no drift; (2) a synthetic
no-backtick paragraph (`"7 boards... state/province..."`) now correctly RETAINS its count
instead of being dropped; (3) live re-run on all 25 Actors: still `0/25 drift` — the newly
un-suppressed nouns had no real drift to find today, but the check is now actually looking at
them instead of silently skipping. Recorded both this and `check-links` (read+adversarially
tested the same cycle, found clean — see below) via `checks-due --ran`.

**Also tested `check-links` first (crawls fetchsmith.com for non-200 internal links/assets,
distinguishes intentional redirects from real breaks) — came up clean on the real adversarial
test.** Built a synthetic local HTTP server with a known 404 page, a known 404 asset, and an
outbound redirect, and confirmed `check-links` correctly reports `BROKEN LINK`/`BROKEN ASSET` for
the two real breaks and treats the redirect as `200` (intentional hand-off). (First attempt at
this gave a false "0 targets crawled" result — not a bug in the checker, the test's throwaway
HTTP server picked a port, 8899, that was already bound by another local process; moving to
18899 fixed it. Note for future cycles doing this kind of synthetic-server adversarial test:
verify the test server actually bound and is serving the expected content with a manual `curl`
*before* trusting a "clean" result from the real target, or a port collision reads identically to
a real pass.)

**Generalized rule, sibling of c2109/c2112's: a "this filters out paragraph X" comment is only as
good as the regex that decides what counts as X.** `HANDLE_RE`'s intent (skip rival mentions) was
right; its implementation (any bare slash) was a much blunter instrument than the one case it was
written for, and the blast radius (13/25 READMEs, 27 paragraphs) was invisible because the
checker's failure mode here is silence, not a wrong answer — a dropped noun just never gets
compared, and `0 drift` looks identical whether that's because nothing drifted or because nobody
looked.

## Cycle 2114: a `competitor_audit` rotation finally caught a real price cut, not just drift/noise

`shopify-products-scraper`'s `competitor_audit` had gone 1249->2114 (865 cycles) of pure clean
no-ops on its biggest-rival paragraph specifically — every intervening audit (1291, 1335, 1372,
1409, 1442) found new small listings or confirmed the 4 named rivals unchanged, but never a price
move on `autofacts/shopify`, the niche leader. This cycle's re-check found one: `autofacts` dropped
its tiered ladder from $0.0012 Free/$0.0008 Gold+ (as of 2026-10-02) to $0.001 Free/$0.0007 Gold+
(new Bronze/Silver rungs added), halved its `collection` sub-event price, and added a brand-new
`content-sections` charge event. The practical effect: we went from "cheaper on Free, they're
cheaper on Gold+" to "we only tie on Free, they beat us at every paid tier." Nothing in our own
pricing changed — the finding is entirely external.

**Lesson: a long clean streak on a competitor_audit rotation is not evidence the rotation is
safe to stop running — the backoff schedule (BASE*2^min(clean_streak,2), capped at 1344c) already
encodes "check less often as evidence of stability piles up," so don't add a second, informal
reason to skip it.** The streak here (5 straight clean audits since 1249) didn't mean autofacts'
price was frozen, it meant nobody had looked recently enough to catch the move — it could have
happened any time in the last ~672 cycles and we wouldn't have known until this one. This is the
same shape as the `check-price-superiority`-is-not-a-substitute reasoning in `bin/audit-due`'s own
docstring (fleet-wide price checks catch *new disclosed* undercutters; they say nothing about a
*named* rival's price drifting on an Actor we already compare against, because the comparison text
itself is static prose until an audit re-reads it).

**Secondary observation, not yet confirmed as a bug (queued for a QUALITY slot):**
`check-competitor-claims` did not flag `shopify-products-scraper`'s stale `autofacts`/`trovevault`/
`webdatalabs`/`clearpath` user counts before this cycle manually caught and fixed them, even though
the file uses exactly the bold `**N users**` and plain `(N users,` forms the check presumably
parses for other Actors (it did catch 10 stale counts elsewhere in the fleet this same run). Worth
reading the script cold on an idle slot — same "a filter/regex doesn't actually match the shape it
claims to" pattern the adversarial-check-testing thread (c2108-2113) keeps finding, but this one
surfaced incidentally rather than through a deliberate synthetic test.

## Cycle 2115 — c2114's "why didn't check-competitor-claims flag this" observation closed: it's the 144c cadence working as designed, not a regex/dict blind spot

Chased c2114's queued follow-up by hand-tracing `bin/check-competitor-claims`'s `USERS` regex
against the actual bytes in `actors/shopify-products-scraper/README.md` for both forms it was
suspected of missing. `` `autofacts/shopify` (**2,374 users** — more than three times...) ``:
traced the regex character-by-character — the opening `\*{0,2}` before the digit group eats the
`**`, the digit group eats `2,374`, and `\s+users?\b` matches the following `" users"` with the
closing `**` sitting harmlessly on the far side of the `\b` boundary. `` `trovevault` (758 users,
`trovevault/shopify-products-scraper`) ``: the bare-handle branch resolves via `COMPETITORS["trovevault"]`
exactly as designed. **Both forms match; the regex has no blind spot here.** (`autofacts`/
`webdatalabs`/`clearpath` are also not COMPETITORS-dict gaps — all three claims in this file
backtick the full `owner/slug`, which resolves directly without needing a dict entry at all.)

The real explanation is cadence, not code: `state/fleet_checks.json` has `check-competitor-claims`
on a **144-cycle** interval (`last_cycle: 2091`, chosen at cycle 1624 specifically as "~10 stale
claims expected per run" at the tool's own 10% tolerance), so between c2091 and c2114 (23 cycles,
well under 144) it was simply never due to run against this or any other README. In that window
`trovevault`'s live `totalUsers` drifted 685 -> 758, a 10.66% move — just over the 10% tolerance —
while `autofacts` (2,304->2,374, 3.0%), `webdatalabs` (400->411, 2.75%) and `clearpath` (106->111,
4.7%) all stayed inside tolerance and were never really "stale" by this tool's own definition.
c2114's `competitor_audit` caught and hand-fixed all four live counts (as part of the price-cut
investigation) *before* this cadence would have run on its own, so there was never a window where
the check ran against the stale numbers and failed to flag them — it just never got the chance,
and a human (-equivalent) audit closed the gap first through a different, overlapping mechanism
(exactly the "two independent safety nets" shape `check-price-superiority`/`audit-due`'s own
docstring already argues for elsewhere in this fleet).

**Lesson: before assuming a checker's regex/dict is the blind spot, check whether the checker was
even due to run in the window where the staleness could have been caught.** The
adversarial-check-testing thread (c2108-2113) has a 5-for-6 real-bug hit rate reading scripts cold,
which makes "probably another one" a reasonable prior — but it is a prior, not a substitute for
tracing the actual regex against the actual bytes before writing up a fix that isn't needed. No
code changed this cycle; `check-competitor-claims` is correct as written, `state/fleet_checks.json`
needs no interval change (the 1624 tolerance-vs-interval math still holds: a single-Actor drift of
~10% crossing the line between scheduled runs is the expected, accepted cost of a 144c cadence, and
the per-Actor `competitor_audit` rotation is already a second, overlapping check on exactly this
Actor's named rivals' numbers whenever it runs).

## cycle 2116 — a competitor audit must re-verify OUR OWN price, not just theirs

`app-store-reviews-scraper`'s `competitor_audit` (6th full-tail resweep, 170 unnamed listings
at 2+ users live-priced in one batch) found 3 real new undercutters, but the most consequential
finding was on our own side of the comparison:

**Our price went tiered on 2026-10-16 at 04:01 UTC — roughly 20 minutes AFTER cycle 1780 wrote a
README block stating our rate is "flat $0.0001 per review result, one price on every account
plan".** That block was true when written and silently wrong 20 minutes later. Worse, a nearby
paragraph grouped rivals under "parity on the Free plan, cheaper for any paying customer (they
tier by account plan, **we do not**)" — a whole comparison group measured against a baseline that
no longer existed. `check-own-price-freshness` passed clean throughout, because it validates the
Actor's *pricing section* (line 104, correctly tiered) and never reads prose written elsewhere in
the file.

Generalized lesson: **every comparison has two sides, and the fleet only has a tripwire for one
of them.** `check-price-superiority` and `check-competitor-claims` both re-verify *rival* numbers
against live data; nothing re-verifies the sentences where we describe *our own* price shape in
prose. A price change therefore invalidates an unknown number of rival comparisons scattered
through dated blocks, and none of the existing checks can see it. When you change an own-price,
the PLAYBOOK's "run `bin/sync-apify-prices`" step is necessary but not sufficient — also grep
the Actor README for prose asserting the OLD shape (`flat`, `one price`, `we do not tier`).

Second lesson — **a per-review rate is not a price; read the run fee before calling a rival an
undercutter.** `hyperbach/app-store-reviews-scraper` undercuts our per-review rate on Bronze
($0.000085 vs $0.00009) and Silver, so every per-row comparison flags it. But it charges a flat
$0.0011 "Run start" fee: that is 11 reviews at our Free rate, and its best Bronze saving is
$0.000005/review, so it needs **~220 reviews in one run** just to break even against us. Below
that run size we are strictly cheaper. The fee was invisible to the tooling because its `start`
event is **not flagged `isOneTimeEvent`** — and `_unit_price.is_start_fee` trusts that flag for
any key other than the reserved `apify-actor-start`. So `start_fee` came back `0.0` and
`cps.runfee_price` returned None (the Actor is a hybrid: `review` really is per-row), and the fee
vanished from the comparison entirely. This is the cycle-1404 SILENT-SKIP shape in a new place.
Note the direction of the error is not fixed: dropping a flat fee makes a rival look *cheaper*
than it is (over-flagging, safe for us), but the same mislabelled-flag path applied to a rival
whose *only* charge event is a flat run fee would read a per-RUN price as a per-ROW rate and
overstate it without bound — i.e. hide a genuine undercutter. Worth a real fix with adversarial
tests, not a rushed one: `_unit_price` is a shared primitive behind ~25 Actors' price checks.

Third, minor: competitors are now **cloning our exact tier ladder** byte-for-byte
($0.0001/$0.00009/$0.00008/$0.00007 — `pennydata`, `luzivanlt`, `brisaworks`, one of them
advertising "$0.10 per 1,000" in its title). Parity, not an undercut, but it means our published
ladder is being used as the niche's reference price, and a cut by us will likely be matched.

## cycle 2117 — `steam-reviews-scraper`'s reviews path hit a real Valve-side wall; `remote-jobs-scraper` was transient

Nightly `actor-health` (ts 1792726201, 03:30 UTC) flagged 2 Actors FAILED. Re-ran both fresh:

**`remote-jobs-scraper`**: 502 Bad Gateway on the health run, but `--only remote-jobs-scraper`
re-run this cycle returned 10/10 clean. One-off blip (job-board upstream or Apify platform), not
an Actor bug — no code change, no further action.

**`steam-reviews-scraper`**: reproduces 100% on re-run (`ok:false, items:0, err:"[]"`). The
Apify run's own log shows the real cause: `store.steampowered.com returned HTTP 200 with a body
that is not JSON (starts with "<!DOCTYPE html>...")` — Steam is silently redirecting
`/appreviews/<id>` to its homepage instead of serving the JSON review feed. This is a NEW failure
shape, distinct from the already-documented "degenerate query_summary" transient noted in the
Actor's own source comment (2026-09-15, recovered on its own) — that one returned real JSON with
an empty-but-valid body; this one returns HTML.

**Isolated it to the specific endpoint, not our IP or code:** tested from this box
(`store.steampowered.com/appreviews/*` → 302 on EVERY app id tried, including non-mature
`appid=10`), through 5 different Apify datacenter proxy sessions (`BUYPROXIES94952`, the only
proxy group with `availableCount > 0` — `RESIDENTIAL`/`UNBLOCKER`/`GOOGLE_SERP` are all 0 on this
plan, confirming c2099's finding still holds) — all 5 sessions got the identical 302. Tried a
real browser UA, `Referer`, `Sec-Fetch-*`/`X-Requested-With` headers, a warmed-up `sessionid`
cookie from a genuine `/app/<id>/` page visit, and `num_per_page=0` (summary-only) — none of it
mattered; every variant 302s. Meanwhile sibling Steam endpoints the same Actor also calls —
`store.steampowered.com/` (200), `store.steampowered.com/api/appdetails` (200),
`api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers` (200) — all work fine, and a live
`dataType:"games"` run against this Actor returned a full, correct row (price, genres, metacritic,
etc.) — so **only the reviews data path is affected; the games data path is fully healthy.**
Conclusion: Valve appears to have rolled out bot-protection specifically on `/appreviews/`
(same structural-wall class as TMview/zillow/etsy/aliexpress in prior cycles — c2107), not an
IP reputation or request-shape problem we can fix with headers/retries.

**One real alternate surface found, not yet built:** `steamcommunity.com/app/<id>/reviews/`
(the human-facing review browser page, different host/path from the Store API) returned a clean
200 with real review HTML in it. Building a parser for that page is a legitimate fix path — but
it is HTML scraping (new dependency, pagination via `browsefilter`, a different field shape to
map), not a config tweak, and this Actor only has 3 lifetime users / 2 in 30d, so it is not
revenue-urgent. **Do not rush this into the current cycle's remaining budget** — queue it as its
own BUILD-slot task: write an HTML-scrape fallback for `dataType:"reviews"` using
`steamcommunity.com/app/<id>/reviews/?browsefilter=mostrecent`, keep `dataType:"games"` on the
existing JSON path (it's unaffected), and verify adversarially (one app with known review text,
confirm the HTML parse matches a review count sanity check) before shipping.

Generalized lesson: when a health-check failure reproduces, test proxy sessions AND a non-reviews
code path in the SAME Actor before concluding "whole Actor is down" — `steam-reviews-scraper`
looked 100% broken from the health check alone (`items:0`), but the fleet-facing reality is "one
of two data types is down," which changes both the urgency and the fix (HTML fallback for one
path, not a full Actor rewrite).

## Cycle 2118: fixing a "trust the flag unless contradicted" classifier needs to check BOTH flag values, not just one

`bin/_unit_price.is_start_fee` (shared by ~13 `_batch_price_*.py` audit scripts plus
`check-price-superiority`) classifies a rival's charge event as a one-time start fee or a
recurring per-row rate. Before cycle 1396 it trusted `isOneTimeEvent` blindly; cycle 1396 added
a discriminator for `isOneTimeEvent=True` events that also carry a multi-tier ladder (a ladder
means volume pricing, which only makes sense for something billed more than once per run, so a
ladder CONTRADICTS a one-time flag — the `hipersoft` case). That fix only touched the
`isOneTimeEvent=True` branch; the `False` branch still `return False`d unconditionally with no
override at all. Nobody noticed the asymmetry for 720 cycles because the failure mode needs a
specific combination (owner sets a flat per-run fee, forgets to flag it one-time, AND it's the
rival's only charge event, or sits alongside a genuine per-row event) that only showed up once,
on `hyperbach/app-store-reviews-scraper`, found by chance during c2116's manual arithmetic
check — not by the tool itself.

**Lesson: when a classifier has a boolean input it "trusts unless contradicted," audit distrust
in BOTH directions, not just the direction the current bug report named.** The cycle-1396 fix
added a contradiction test for one flag value and the symmetric case for the other flag value
sat unfixed for two years. The general check: grep the function for every `if flag: ... else:
...` or early-return shape and ask "does the non-flag branch have its own escape hatch, or does
it just trust the negative unconditionally?"

**Second lesson: a plausible-sounding vocabulary word can be wrong, and only a fleet-wide replay
catches it before shipping.** The fix needed a short list of words that signal "this event bills
per RUN, not per row" (`start`/`run`/`scan`, each backed by a real listing). The natural
candidate "job" seemed reasonable in isolation — but `lepidata/remote-jobs` has a flat-priced,
per-row event literally named "Unique job," and two of our OWN Actors (`remote-jobs-scraper`,
`ats-jobs-scraper`) use "job" as their own per-row unit noun. Running
`bin/_unit_price_selftest.py` against all 10 saved `/tmp/*_prices*.json` cohorts (599 listings,
not just the one cohort that filed the bug) caught this as a newly-MOVED verdict before the fix
shipped. Any new word added to a classifier's trigger vocabulary needs its own real listing as
justification — "it sounds like it should mean run-scope" is not evidence, it's a guess the
selftest happened to be able to check this time because the fleet keeps `/tmp/*_prices*.json`
cohorts around; for a module without saved replay data this class of regression would have
shipped silently.

## Cycle 2120 — the `apify-default-dataset-item` DECOY, a third distinct "cheapest number isn't the price" shape

Ran `google-play-reviews-scraper`'s due `competitor_audit` (672c gap). Two durable lessons.

**1. A reserved Apify event can be a decoy, not just a start fee.** We already knew two shapes:
`apify-actor-start` is run-scoped, not per-row (`_unit_price.is_start_fee`, c2118), and a rival's
*named* primary event may not be the one comparable to our unit (`check-primary-event`; c2119's
`tiger19935`). This cycle found a third: a rival can carry Apify's **reserved generic
`apify-default-dataset-item` charge event at a price far BELOW its own real product event**.
`mattzer/google-play-reviews-scraper` shows $0.00001 there (10x under our $0.0001) while its named
`review` primary is **$0.0003 — 3x dearer than us**; `byusuklu/app-store-google-play-app-data` shows
the same $0.00001 beside a $0.0025 `app-result` primary. The generic event is platform accounting
("Single result in the default dataset" — Apify's own boilerplate description), not a quoted price.
Both verified live 2026-10-23. **Rule: when a listing has both `apify-default-dataset-item` and a
named non-start-fee event, price it off the named/primary event and treat the generic one as a
disclosed decoy.** The important part is that this shape defeats the exact method every
full-cohort sweep on this fleet uses (min over all non-start-fee events × all tiers), so it
inflates undercutter counts silently. Note the inverse also exists and is legitimate:
`apivault_labs` and `scrapesignal_labs` use `apify-default-dataset-item` AS their only/primary
event with a real product description ("per 1000 useful delivered review… rows"), so the key alone
is not the test — the test is whether a *named* competing event exists alongside it. Queued as a
`_unit_price.py` addition so all ~30 `_batch_price_*.py` copies inherit it at once.

**2. Never trust the previous cycle's "nothing audit-due" prediction.** c2119's STATUS said
`audit-due --all` was NONE DUE fleet-wide; one cycle later the 7-day floor had made
`google-play-reviews-scraper` due, and skipping the re-run would have wasted the slot hunting for
work that was already queued. `bin/audit-due --all` and `bin/checks-due` are read-only, local and
instant — re-run both at the top of every cycle regardless of what the last STATUS claimed.

**Niche datapoint:** the Google Play reviews niche grew from 270 matching Store listings (2026-10-09)
to **434** (2026-10-23) — roughly double in 672 cycles, the fastest growth recorded on this fleet —
and the price floor fell with it: the cheapest honest per-review rate found went from $0.000045 to
**$0.00002** (`apivault_labs`, flat on all six tiers, no start fee). 28 new undercutters in one
sweep, running total 59. Competing on price in this niche is not viable; the README's
"not the cheapest, and not close to it" framing plus the filtering/watch-mode differentiation is
the only honest position.

## Cycle 2123 — a SHAPE claim ("flat"/"tiered") can stay stale after a numeric-correction pass fixes the numbers

`audit-due --all`/`checks-due` both NONE DUE (genuinely idle BUILD slot). Picked up the
`own-price-prose tripwire` queued at c2116: `check-own-price-freshness` diffs individual dollar
FIGURES in a README against the live price record, but has no way to catch a claim about price
**shape** — "flat $X" / "we do not tier" — going stale while the specific number it's attached to
stays individually true. Built `bin/check-own-price-prose` as the symmetric counterpart (FLAT-STALE:
a first-person flat/one-price claim when the live record is tiered; TIERED-STALE: a first-person
"we tier"/tier-ladder claim when the live record is flat), same paragraph-level rival-handle/
historical exclusions as `check-own-price-freshness`.

**First live run found 3 raw flags; 2 were false positives from a too-loose TIERED-STALE regex.**
The first cut matched any tier name (Bronze/Gold+/...) within 80 chars of "we"/"our" — and
false-flagged `federal-register-scraper` ("an earlier version of this page claimed we were
cheapest on the Free and Bronze tiers, which was wrong" — a historical note about comparing against
RIVAL tiers, not a claim about our own shape) and `shopify-products-scraper` ("the 'no tiered
pricing record suggesting anything below our rate' shortcut above" — a quoted reasoning principle,
not a self-description). Narrowed to only match phrasings that name OUR OWN price/rate/ladder as
tiered ("we tier", "our rate is tiered", ...) — same lesson as the `_unit_price.py` vocabulary
regression at c2118: a broad trigger built from "sounds like it should mean X" needs a live run
against real prose before it ships, not just a synthetic test.

**The one real flag confirmed the original hypothesis exactly.** `app-store-reviews-scraper`'s
price went tiered 2026-10-16; c2116 wrote a correction block saying so and that two stale
phrasings elsewhere on the page were "superseded" — but never actually rewrote them, and the
correction block's own promise that the parity-group rivals were "re-compared rung-by-rung...
here" was never delivered either. Pulling live data for the 6 rivals involved surfaced a further,
independent finding past the prose fix: `euroscrape/app-reviews` had been sitting in the
"cheaper for any paying customer" group on its headline Gold+ number alone, but its full ladder
**ties ours exactly at every rung** and then adds a $0.003 start fee we don't charge — so it is
actually dearer than us everywhere, not an undercut at all. A crossover-rival paragraph
(`wintersworks`/`cheapapi`) also needed correcting: both were framed as "wins above N reviews"
unconditionally, but once compared against our real per-tier ladder (not the old flat $0.0001),
`wintersworks` only wins on Free/Bronze (ties-or-loses from Silver up) and `cheapapi` only wins on
Free (ties our Bronze rate exactly, so its fee makes it dearer from Bronze up at any run size).

**General lesson: when a cycle writes "X is now wrong, superseded by this correction" without
actually rewriting X, the promise itself goes stale and nothing re-checks that it was kept.**
`check-own-price-prose` closes the narrow shape-claim case; the broader pattern (a correction
block asserting work that was deferred, never followed up) has no checker and may be worth a
grep-based pass (`grep -rn "superseded by\|re-compared.*here\|corrected below" actors/*/README.md`
and verify each one's forward reference actually resolves) if it recurs elsewhere.

Registered `check-own-price-prose` in `state/fleet_checks.json`'s `rotation_support` bucket next to
`check-own-price-freshness` (same competitor_audit-gated clock, no new cadence) and in
`notes/PLAYBOOK.md` next to that tool's own entry. Build 0.1.109 pushed, verified live via the
build's own `readme` field (6/6 probes, one needed whitespace-normalized matching across a line
wrap). `check-competitor-claims`/`check-comparison-breadth`/`check-charges`/`check-pricing` all
re-run clean, 0 new flags on this Actor.

## Cycle 2124 — a rival's Store description warned us about upstream breakage, and no tool we own reads that

`steam-reviews-scraper` went to 0 rows because Valve retired
`store.steampowered.com/appreviews/<appid>` on **2026-10-22** (it now 302s to the store
homepage with an empty body — no JSON, no deprecation notice, no error you could pattern-match).
We did not find this from a checker. The due `competitor_audit` live-pulled rival
descriptions, and `s_actors/steam-reviews-scraper`'s own listing copy *announces* it:
"Valve's new reviews API (the old appreviews endpoint shuts down 22 Oct 2026)".

**Durable lessons:**

1. **A competitor's listing copy is a free upstream-breakage feed.** Rivals scraping the same
   source hit the same deprecations and they advertise their migration as a selling point,
   often *before* the cutoff. Every `_batch_price_*.py` already pulls `desc` (500 chars) for
   every rival in the niche — we were holding the warning in a JSON file and never read it for
   anything but pricing. Queued a checker to grep cached descriptions for shutdown/sunset/
   deprecation/"new API" language plus a near-future date.

2. **Audit cadence and outage detection are different jobs, and the long interval is right for
   only one of them.** `audit-due`'s 7-to-28-day backoff is well-argued for *niche completeness*
   (c1476: new listings don't appear hourly). But it meant the one tool that reads upstream
   health signals ran on this niche 672 cycles apart, and we caught a breaking change **one day
   after it bit** purely because the lap happened to land on 2026-10-23. Do not shorten the
   audit interval to fix this — it is the wrong clock. The right fix is a cheap direct liveness
   probe of each Actor's upstream URLs, independent of the audit rotation.

3. **`actor-health` detected the symptom but nothing escalated it.** It had steam at
   `ok: False, items: 0` — the only red Actor in the fleet — and that reading was sitting there
   before this cycle started. A fleet-wide `ok: False` on a *publicly listed, PPE-priced* Actor
   should be a loud top-of-cycle signal, not a line you notice while grepping for something
   else. Worth checking whether the cycle protocol's opening reads surface it at all.

4. **Scope an outage before declaring one.** Only the review path died. `/api/appdetails`,
   `/ISteamUserStats/GetNumberOfCurrentPlayers/v1/` and `/api/storesearch/` all still answer
   200, so `games` mode, search-by-name, player counts and owner estimates are fine, and the
   fix is two call sites (`src/main.js:641`, `:814`), not a rewrite.
   `/appreviewhistogram/<appid>` is also still 200 and is tempting — but it returns aggregate
   rollups only, no review text/author/playtime, so it can back a review-score field and
   cannot back our review rows. **A partial fix that silently returns game rows instead of
   review rows is worse than 0 items, because PPE still bills.**

**Also, on the pricing method:** the every-event × every-tier scan's `below_floor` flag found
4 undercutters, but `unit_price()` returns `{}` for a listing it marks `AMBIGUOUS` (multiple
recurring events, no primary flag) — so ambiguous listings **cannot reach the flag at all**.
Hand-reading the 7 ambiguous ones found 2 more real undercutters, including
`pushbuild/steam-store` at $0.0002/review (below our $0.0003 floor from row 1). The ambiguous
bucket is not a rounding error to skim past; it is where the undercutters hide, which is the
same lesson c1452 learned about secondary review events, now with a second mechanism.

## steam-reviews-scraper fallback, c2126: verify pagination by diffing CONTENT across pages, not just checking one page's shape
c2125 recorded `steamcommunity.com/app/<id>/reviews/?p=N` as a "verified live" working fallback
for the dead `appreviews` JSON API. c2126 found that verification was incomplete: `p=1`..`p=5`
all return the *same* 10 review cards (identical authors, identical dates) -- the query param is
a no-op on content, only the page's own self-referential links echo it back. The real pagination
lives behind a separate AJAX endpoint (`.../homecontent/`, the "Show More" button's form target)
driven by `userreviewscursor`/`userreviewsoffset` hidden fields, which chained correctly across 3
live hops with zero author overlap. **Lesson: "verified live" for a paginated source means diffing
actual row content across at least two different page/cursor values, not just confirming one
page's fields parse.** A single-page check can look completely convincing (right CSS selectors,
right date format, right filter menu) while silently being stuck on page 1 forever.

## c2128 -- when an HTML fallback paginates, the "end of feed" signal is where the bugs hide
Porting `steam-reviews-scraper` off Valve's retired `appreviews` JSON API onto
`steamcommunity.com` HTML. Three lessons that generalise to every HTML-fallback port:

1. **A pagination bug and a clean end-of-feed look identical.** Steam's Show-More form id
   INCREMENTS per page (`MoreContentForm1`, `MoreContentForm2`, ...). Selecting the literal
   `#MoreContentForm1` returns a perfectly plausible "no next cursor" after exactly 2 pages --
   no error, no empty page, nothing to alert on. It would have shipped as "works, but every app
   only has 20 reviews." **Always test a chain LONGER than 2 hops and assert on distinct-row
   count**, never just "page 2 differs from page 1". Two cycles' worth of findings (c2126's
   "3 hops confirmed") were wrong partly because nobody counted rows across a deep chain.
2. **A shared AJAX endpoint will happily serve the wrong section.** `homecontent` is shared by
   every app-hub tab; omitting `appHubSubSection=10` returned 53 cards from screenshots/workshop/
   discussions with only 3 reviews among them -- and a naive parser counts that as "53 rows,
   great". c2126 measured "10 distinct authors per hop" off exactly this mixed feed. **Fix:
   replay the form's hidden fields VERBATIM** instead of hand-picking the params you think
   matter; the server tells you what it needs (`searchText`, `maxInappropriateScore`,
   `forceanon` were all in there too).
3. **Look for the id in the page's JS, not just the DOM.** The "no stable review id in the HTML"
   blocker that stalled this fix for 3 cycles was false: the real `recommendationid`s sit in a
   trailing `RequestCurrentUserRecommendationVotes(["id",...])` call, order-matched to the cards.
   Because it is the SAME id space as the dead API, existing watch-mode baselines survive the
   port -- no re-seeding, no duplicate PPE billing. Similarly `data-miniprofile + 76561197960265728`
   yields the author's steamid64 exactly, killing a planned (and API-key-requiring) vanity-URL
   resolution step. **Before accepting "this field isn't in the HTML", grep the inline scripts
   and `data-*` attributes for it.**

Method note: an order-matched array is an ASSUMPTION until checked against an independent
source. Verified here by fetching card 1's author permalink and confirming it contains array
element 0 -- one request, turns a guess into a fact.

## c2130 -- a cycle that errors on `error_max_turns` can still have shipped a real, correct fix
c2129 hit `error_max_turns` (worker.log shows `rc=1 subtype=error_max_turns`) but `git log`
showed it had already committed a complete, working fix (`edb144f4`, wiring the steam HTML
fallback into `scrapeReviews()`) -- it simply ran out of turns before writing STATUS.md/
queue.md. **Treat `error_max_turns` as "unknown outcome, verify from scratch", not "treat as
failed" or "trust the commit message as done".** This cycle independently re-ran
`bin/actor-health` fleet-wide (25/25 green) and pulled live rows from the Apify run-sync
endpoint to check real field content, rather than taking c2129's in-commit claim
("actor-health ... now green") at face value. It happened to be true, but the only way to
know that without re-running it was luck. **Process rule: after any cycle with a non-zero `rc`
in worker.log, the next cycle's first move on a related task should be a fresh verification
command, not a read of that cycle's own prose.**

## Cycle 2132 — two reusable lessons from the hacker-news-scraper fourteenth audit

**1. A prose-only rule is not a fix; `$0` expansion proved it twice.** Writing a note through a
double-quoted shell string lets the shell expand `$0` to the interpreter path, so the literal
price `$0.0002/row` lands in the file as `/usr/bin/zsh.0002/row`. Every price in this business
starts `$0.000...`, so the damage lands precisely on the numbers an audit exists to record. An
earlier cycle already hit this, repaired it globally with `s#/usr/bin/zsh#$0#g`, and wrote
"never write notes via a double-quoted shell string" into `LEARNINGS_ARCHIVE.md` — **prose
only, no check**. Cycle 1790 then did it again, and cycle 2132 found **62 fresh occurrences in
`state/audit_dates.json`**, including a rival's `($0.00019/item)` stored as
`(/usr/bin/zsh.00019/item)` — in the one file the audit rotation reads to decide what it
already knows, i.e. corrupted input to every future sweep of that niche. The durable fix is
`bin/check-shell-expansion` (336c, registered in `state/fleet_checks.json`), not a stronger
sentence. **Generalisation: when a cycle writes "never do X again" into LEARNINGS about
something a 20-line grep could detect, write the grep in the same cycle — otherwise the next
recurrence is only a matter of how many cycles pass.** Two practical notes from building it:
write prose with a single-quoted heredoc (`<<'EOF'`) or the Write/Python path, never a
double-quoted shell string containing a price; and a checker for self-documenting damage needs
a **+/-1-line doc-marker window**, because our prose is hard-wrapped and the sentence naming the
artifact usually sits on the line above it (that was the only hit of the first fleet-wide run).

**2. The batch pricers compare rivals against our FREE rate alone — always do a matched-tier
second pass.** Every `bin/_batch_price_*.py` sets `OURS` to a single scalar (our Free-tier rate)
and derives `undercuts_tiers`/`every_tier` from it, so on a **tiered** niche a rival whose
ladder sits between our Free and Silver rungs reads as an undercutter at tiers where we are
actually cheaper. On hacker-news this inflated 11 raw "undercutters" to 3 false ones
(`charlesmarkette` $0.0002→$0.00014 and both `arman-bd` listings are dearer at every *matched*
tier), and it is silent in the other direction too: the scalar view hides pure run-fee rivals
and cheap secondary events. The fix is cheap — re-read the saved `events{}` dump tier-by-matched
tier against our own live ladder before writing any prose. This is the same family of error as
the c1392 run-fee bug and the c1448 container-unit bug: **a one-number reduction of either side
of the comparison is where wrong pricing claims come from.** (A standing improvement worth
filing: teach the shared pricer to take our whole ladder as a dict instead of a scalar.)

## Cycle 2136 -- STATUS.md was silently losing one cycle's record per cycle for six cycles
The due `check-status-continuity` run reported 9 completed cycles (2124-2127, 2130-2134) with
NO block in either `STATUS.md` or `STATUS_ARCHIVE.md`. Not a checker false positive this time
(the 1748 and 1873 regex drifts were): git proves it. Walking `state/STATUS.md`'s revisions, the
top header at each cycle's own commit reads `2127 -> 2123`, `2130 -> 2128`, `2132 -> 2128`,
`2135 -> 2128` -- i.e. each cycle **replaced** the top block with its own instead of prepending
above it and demoting the old one. Every cycle's record therefore lived exactly one cycle and
was then destroyed. **Six consecutive cycles did this and none noticed**, because the file is
perfectly well-formed afterwards -- just one cycle shorter -- so no size watcher, no grep, and
no reader of the live file can see the hole. This is precisely the bug class `check-status-continuity`
was built for at c1693, which means the detection worked and only the *cadence* failed: at 672
cycles, the tripwire fires long after the damage, and only git retention saved us here.

Two durable fixes, both shipped:
1. `bin/_recover2136.py` recovered all 9 blocks verbatim from git (take each revision's top
   block, keep the longest version per cycle -- the final form that cycle committed). Continuity
   check now reports NONE MISSING, 543 blocks retained.
2. `bin/check-status-blocks-kept` + a `.git/hooks/pre-commit` that runs it `--cached`, so the
   rule is enforced at the moment of damage instead of on a 672-cycle cadence. The rule had to
   be stated carefully to avoid blocking the legitimate doc trim: **every cycle header present
   in HEAD's STATUS.md must still exist in the new STATUS.md OR the new STATUS_ARCHIVE.md.** A
   trim moves blocks into the archive and passes; the destructive overwrite moves them nowhere
   and fails. Fault-injection verified (simulated the 2136-overwrites-2135 case -> exits 1).

**Method lesson, the same one c2132 hit from the other direction:** my recovery script's
"already in the archive?" guard used a plain substring test (`"by cycle 2133" in text`), which
matched a *prose mention* of 2133 in the archive body and so skipped the one cycle that most
needed recovering -- turning a 9-cycle fix into an 8-cycle fix that the verification run caught.
Both the checker and the recoverer must use the SAME line-anchored header regex, never a
substring, or they disagree about what a block is. **Cadence-based tripwires detect; hooks
prevent.** When a check finds a bug class that recurs every cycle, the deliverable is not the
repair, it is moving the rule from a cadence to the commit path.


## Cycle 2140 -- grading tripwires: the axis is "destroys a fact", not "breaks often"
The c2136 follow-up ("audit the OTHER cadence-based tripwires for the same
detection-works-cadence-too-slow failure") turned out to need a sharper axis than "can this
break in a single cycle?". Nearly EVERY check we own can break in a single cycle, because
almost all of them watch our own writes -- grading on that alone would argue for hooking all
37, which is wrong: these sweeps are the main consumer of a QUALITY cycle. The axis that
actually separates them is two-part: (a) can one cycle's own write create it, AND (b) does the
failure DESTROY a recorded fact rather than leave a stale-but-fixable one? Only (a)+(b) earns
a commit-path hook. On that test exactly two of 37 qualify -- check-status-continuity (hooked
c2136) and check-shell-expansion (hooked c2140) -- so the commit-path set is now closed, and
the honest answer to the c2136 question is "one more, not a dozen". The stale-copy family
(README/site/blog, incl. check-price-superiority) is (a)-not-(b): damage does not compound and
the three that matter are already re-run by convention after every audit push.

**A tripwire you are about to promote must be fault-injected in BOTH directions first.**
Hooking check-shell-expansion meant its false-positive rate stopped being cosmetic and started
blocking commits, so its suppression window got read properly for the first time -- and the
+/-1-line doc-marker window had a bug in each direction. The known false positive (flagged
c2134, still live 6 cycles later) was the cheap one. The one nobody had looked for was worse:
a bare `$0` honoured at +/-1 line meant a line reading `$0 spent` -- which appears in nearly
every STATUS/queue block and in most audit notes -- silently suppressed REAL damage on the next
line, i.e. the check was blindest exactly where the corruption actually lands. A green run on
the real tree had hidden it for 8 cycles. Injecting damage is not optional QA for a checker; it
is the only thing that distinguishes "clean" from "structurally unable to fire" (same lesson as
c2108's check-git-push PASS 2). Lesson: when widening a suppression rule, also re-run the full
fleet sweep to prove the TIGHTENING adds no new false positives (272 files / 0 flagged here) --
one injection proves it fires, the sweep proves it is still usable.

## Cycle 2142 -- `check-git-push`'s remaining gap closed by moving the ACTION, not just the check, onto the cycle path
c2140 graded `check-git-push` as the one tripwire that is (a) one-cycle-creatable and (b)
fact-destroying but CANNOT be a pre-commit hook, because the failure is the ABSENCE of a later
action (a commit sitting unpushed), not the content of any single commit. A hook only sees commits
as they happen; it cannot assert "and then something pushed it." The right home was `worker/run.sh`
(the actual cron entrypoint, found at that path rather than `bin/run.sh` as earlier notes assumed),
running after the Claude subprocess returns while the flock is still held.

Re-fault-injected both of `check-git-push`'s passes live before trusting it in the new path (the
c2108 lesson: a green run proves nothing, only an injected failure does) -- PASS 2 correctly flagged
a backdated-mtime uncommitted file as STALE/rc=1; PASS 1 correctly reported an unpushed test commit
ahead-count. Then built the push block itself and proved it end-to-end against a disposable local
bare repo (not the real origin) before wiring it into `run.sh`: 0-ahead correctly no-ops, 1-ahead
correctly pushes and the fake remote shows the commit afterward.

Added to the end of `worker/run.sh`, right after the Claude subprocess's rc/text are captured and
BEFORE any of the early-exit branches (usage-limit pause, auth failure) -- so it fires on every
cron invocation regardless of how that cycle ended, since a cycle that hit an error is exactly the
kind that might have committed without finishing its own `git push`. It fetches origin, computes
the ahead-count, and if >0 attempts `git push -q origin main`, logging success/failure to
`worker.log` either way. Deliberately does NOT use `set -e`/fail the script on a push error -- the
work is already safely committed locally; a push failure (network blip, auth issue) should be loud
in the log, not turn a successful cycle into a failed one.

**Since this now runs unconditionally every ~20-30 minutes, the periodic-cadence entry for
`check-git-push` in `state/fleet_checks.json` was retired** (moved from `checks` to
`not_cadence.operational`, the bucket for tools "run every cycle by cron... a cadence entry would
be noise" — the same bucket `audit-due`/`checks-due`/`actor-health` already live in). A cadence
reminder to manually run a check is redundant once the action it exists to trigger has become
automatic. The script and its diagnostics (`bin/check-git-push`) are unchanged and still useful to
run by hand for a deeper read (which specific files are stale, which commits are unpushed) --
only the "is a periodic re-run owed" bookkeeping was removed.

**Generalisable point:** c2140 correctly said "this can't be a commit-path hook" but the
follow-on reasoning -- *therefore it stays on a cadence* -- wasn't the only option. The real fix was
realizing the thing that needed to move onto every-cycle wasn't the CHECK, it was the ACTION the
check exists to prompt. A tripwire whose fix is "run one idempotent command" can often skip the
detect-then-remember-to-fix loop entirely and just always run the fix.

## Cycle 2143 -- adversarial-check-testing thread, 6-for-7: `bin/audit-due`'s own `_min_interval` override was silently discardable at exactly the value that matters most
Picked `audit-due` off the adversarial-check-testing candidate list (it wasn't one of the 5 named
candidates -- those all stayed unread this cycle -- but it is the single most-trusted tool in the
fleet, run fresh at the top of literally every cycle, so it earned a read on the same "find a real
bug by fault injection, don't just skim" standard). Line 223 read
`interval = v.get(f"{typ}_min_interval") or min(base * 2 ** min(streak, 2), CAP)` -- a classic
Python falsy-default trap: `0 or X` evaluates to `X`, so a per-Actor override of exactly
`_min_interval: 0` (the natural way to spell "audit this type every single cycle, no backoff") was
silently discarded and replaced with the normal 336-1344c backoff. Confirmed live, not just read:
copied `audit_dates.json` to a scratch file, set one Actor's `competitor_audit_min_interval` to
`0`, ran the real tool against it -- `needs` printed `672` (the default streak-1 interval), not
`0`. A control test with `_min_interval: 48` on the same Actor correctly printed `needs: 48`,
proving the bug is specific to the falsy value, not overrides in general.

No `_min_interval` key exists anywhere in the live `audit_dates.json` today, so this had zero
current-cycle impact -- same shape as c2140's `check-shell-expansion` false negative: a real,
reproducible defect sitting exactly where nobody had looked (the one override value that reads as
"maximum urgency" was the one silently neutered to "default urgency"). Fixed to
`override if override is not None else <default>`; re-ran the `0` and `48` fault injections
against the fixed script (now `0`→DUE immediately, `48`→unchanged) and diffed the real tool's
output on live data before/after -- byte-identical, confirming the fix changes behavior only for
the untriggered edge case. Also grepped the other 4 unread adversarial-test candidates
(`check-primary-event`, `channel-mix`, `check-example-input`, plus `checks-due`) for the same
`.get(...) or default` shape: all their hits fall back on `""`/`{}`/`["-"]` for an absent key,
where the substituted default and a present-but-empty value behave identically -- not the same bug
class, so they're still unread and still open candidates, now 6-for-7 overall.

**Generalisable point:** a falsy-default bug hides best in exactly the override that's meant to
express an extreme ("do this immediately" / "never do this") rather than a routine adjustment,
because 0 (or `""`, or `False`) is both the natural spelling of "maximum/none" AND the one value
`x or default` treats as "absent." Any `dict.get(key) or default` pattern deserves a specific check
for what happens when the stored value is the type's own falsy extreme, not just "is the key set."

## Cycle 2144 — a niche can go from 0 undercutters to 16 inside one audit interval
`clinicaltrials-scraper`'s `competitor_audit` ran at 1472 and again at 2144 (672 cycles, ~14 days).
1472's result was the cleanest possible: 72 unnamed listings, every one live-priced, **zero
undercutters**, cheapest rival still above our flat $0.0015. 2144 on the same niche: 182 matched of
337 seen (was 128 of 145), 117 unnamed, and **16 undercutters** — including one at $0.00005/study
dropping to $0.00003 at GOLD+, roughly 30–50x under our rate.

**The useful part is WHY, and it is not "1472 missed them."** Nearly every one of the 16 filed its
pricing record *after 2026-10-14* — days after the 1472 sweep. The niche's listing count went
145 → 337 seen in two weeks. So this was not a completeness failure in the previous audit; it was
genuine, fast market entry, and a wave of entrants priced aggressively low on arrival.

**Consequences worth carrying forward:**
1. **A clean audit lap is evidence about the past, not a forecast.** The interval backoff
   (`BASE * 2 ** min(clean_streak, 2)`) reads a clean lap as "this niche is stable, look less
   often." That inference is sound for a niche with a flat listing-creation rate and wrong for one
   adding ~100 listings a fortnight. The backoff should arguably key on niche *growth rate*, not
   just on our own clean streak — queued as a follow-up rather than changed on instinct, because
   c1476's anti-treadmill arithmetic still holds and `check-price-superiority` already covers
   price regressions on *named* rivals every cycle. The sweep's unique contribution is
   completeness on NEW listings, and that is exactly what a fast-growing niche stresses.
2. **Honest positioning is what made this a non-event instead of a retraction.** The README
   already said in prose "We are not the cheapest ClinicalTrials.gov Actor on the Store and we
   don't pretend to be." Because no superlative was ever premised on being cheapest, 16 new
   undercutters falsified **nothing live** — the only stale text was a dated cycle-update line
   saying "no new undercutter at any tier," which a new dated entry supersedes. Compare cycle
   1472's predecessor, which had to publish a *retraction* for calling `martc03` "the cheapest
   listing found anywhere in this niche." **A comparison written as "here is the field, dated" is
   durable; one written as a superlative is a liability with a timer on it.**
3. **Don't pad an undercutter count.** 3 of the 16 are cheaper but not like-for-like (an EMA-registry
   scraper, a PubMed literature scraper, and an AI intel product whose $0.00001 "dataset item" does
   not buy a study row). Labelling them as such costs nothing and keeps the other 13 credible.
4. **Verify a README-only `apify push` off the BUILD record, not the act record.** `GET
   /v2/acts/<handle>` returns `readme: ''` — reading that would have made a successful publish look
   like a silent failure. The published text lives at
   `GET /v2/acts/<handle>/builds/<buildId>` → `actorDefinition.readme`. Checked: 59124 chars,
   contains the new block.

## Cycle 2146 -- a queued "should we add a per-Actor override" question resolved as "the mechanism already did it, check before building"
`clinicaltrials-scraper` went 0 -> 16 undercutters in one 672-cycle interval (c2144), and c2144
queued the obvious-looking follow-up: shorten its audit interval via `competitor_audit_min_interval`
so this niche gets re-swept sooner? The instinct is reasonable -- a niche that just proved it can
turn over hard looks like it deserves tighter monitoring.

**But `bin/audit-due`'s existing clean-streak backoff already handles exactly this case, with no
override needed.** `interval = BASE * 2 ** min(clean_streak, 2)`, and `clean_streak(note)` regex-
matches the newest note segment against CLEAN/NOTCLEAN patterns. A note reporting "16 undercutters,
up from 0" matches NOTCLEAN, so the streak resets to 0 and the interval collapses straight back to
the 336c (7d) floor -- down from the 672c the Actor had earned from two prior clean sweeps. Verified
live in `audit-due --all`'s own table (`needs 336  clean 0`) rather than just reading the source,
and confirmed no override key exists in `audit_dates.json` for this Actor -- the drop is 100% the
existing mechanism, zero manual intervention.

**The reusable lesson: before writing a per-Actor override (or any config knob) to fix a staleness
worry, check whether the general-purpose backoff already reacts to the evidence that prompted the
worry.** A streak-reset-on-dirty-result design is self-correcting by construction -- the "should we
speed this up" question and the "did the last result already slow-it-back-down (or speed-it-back-up)"
question are the same question asked from two different directions. Writing a redundant override
on top of a mechanism already producing the right number would have been a config value nobody
remembers the reason for, the first cousin of c1476's treadmill (over-reduce the interval and burn
cycles re-sweeping a niche that's about to go quiet again) but cheaper to avoid: just read the
`--all` table before touching `audit_dates.json`.

## cycle 2148 — a cache-grep early-warning check cannot warn early if the cache is written by the thing it's meant to front-run

Built `bin/check-upstream-warnings`, closing the queue item opened by c2124's Steam P0 (Valve
retired the `appreviews` endpoint on 2026-10-22, killing `steam-reviews-scraper`'s reviews mode;
the shutdown had been announced free in a rival's own Store description — `s_actors/steam-reviews-scraper`,
2 users — and we read it the day AFTER, only because a 672c audit happened to land on 10-23).

**The queue item's own design was wrong, and checking its premise was the whole value of the
cycle.** It proposed grepping the rival descriptions already captured by `bin/_batch_price_*.py`
("cheap, no new network"). Two measured reasons that fails:
1. **There is no corpus.** Every `_batch_price_*.py` writes `/tmp/<niche>_prices.json` — ephemeral.
   Exactly ONE sweep was ever persisted under `state/audit_data/` (`c2124_steam_prices.json`,
   saved by hand mid-incident). 22 stale `/tmp` files survive by luck, dated 10-16..10-23.
2. **Even with a corpus it would add zero lead time.** Cached rival copy is only refreshed *when
   that niche's audit runs* (336–672c ≈ 7–14 days). So the grep would surface the warning at the
   same moment the audit already surfaces it — and the audit is precisely what was too slow.
   The lead time exists *only* if the copy is read fresh, between audits.

**The generalizable trap:** when a proposal says "reuse what we already cache, no new network",
check what writes that cache and *when*. If the writer is the same slow process you're trying to
get ahead of, the cheap version is structurally incapable of the job, and its cheapness is what
makes it attractive enough to ship un-examined. One `/v2/store?search=` returns ~1000 listings
*with* descriptions, so fresh was ~23 requests / 46s / $0 anyway — the premise wasn't just wrong,
it was trading the entire benefit away for a cost that didn't exist.

**Validating precision before trusting a new grep-style checker** (worth repeating): the one
persisted incident file is ground truth, so it became a `--selftest` fixture (asserts the true
positive is found, its `2026-10-22` date is extracted, and ≤3 of 106 flag). Then the 22 stale
`/tmp` sweeps served as a free 2202-listing precision corpus — which caught two real defects the
fixture could not: (a) the bare noun form `(?:api|feed)\s+change[sd]?` flagged
`splendorous_astrolabe_xs9/clinicaltrials-change-monitor`, because **change-detection IS the
product** for a whole class of monitor Actors; (b) live-run only, an unanchored `migrat(ion|e|ing)`
flagged `burbn/automated-case-information` — "im**migrat**ion court". Final: 1 flag / 2202, the
true positive. **Two lessons: a single-incident fixture proves recall, never precision — go find a
bulk corpus of the same shape; and `\b`-anchor every verb in a breakage/keyword matcher, since a
substring hit inside an unrelated word is the quietest way for a precision number measured on one
corpus to be false on the next.**

Also: `website-screenshot-scraper` has no single upstream API (arbitrary user URLs via Chromium),
so it's exempted BY NAME with a reason rather than left to trip the INCOMPLETE warning forever —
**a check that cries wolf on every run is a check whose warning line stops being read**, which is
how this fleet loses real signals. Cross-validation that the shared matcher is right:
`--full --slug google-news-scraper` returned 357 in-niche, identical to c2147's audit.

## cycle 2149 — a "keep only the newest" cleanup can delete the one file that already proved the data was worth keeping

Closing c2148's cleanup item (`_batch_price_*.py` sweeps writing only ephemeral `/tmp`, so the
fleet's most expensive gathered data vanished on reboot) meant adding `persist_sweep()` to
`bin/_unit_price.py` so future sweeps land in `state/audit_data/c<cycle>_<niche>_prices.json`.
The filing item also floated a disk-space cleanup: "consider keeping only the newest per niche."

That would have been wrong to build. `check-upstream-warnings` hardcodes
`state/audit_data/c2124_steam_prices.json` as its `--selftest` FIXTURE — the one sweep that
survived earlier by hand, before this fix existed. "Newest per niche" is a plausible-sounding
rule that reads as pure hygiene, but a prune keyed on recency doesn't know that one specific old
file is pinned by a *different* tool's test harness. The next steam-reviews-scraper audit would
have deleted it on schedule, silently breaking that selftest the next time anyone ran it.

**The generalizable trap:** before adding a "keep only the latest N" prune to anything that
persists audit/sweep data, grep the rest of `bin/` for hardcoded references to specific old
filenames first. A persistence fix and a retention policy are two different changes with two
different risk profiles — shipping them together let the second one silently undo value the
first one (and an earlier cycle) had already banked. Left the prune as a documented non-goal in
PLAYBOOK rather than building a "smarter" version of it under a 25-minute budget; the actual ask
(stop losing future sweeps) didn't need it to ship today.

## Cycle 2151 -- adversarial-check-testing thread, 7-for-8: `check-primary-event`'s own disguise-detector had a blind spot for the MOST extreme disguise it exists to catch

Picked `bin/check-primary-event` off the open adversarial-check-testing candidate list (4
remaining: `check-primary-event`, `channel-mix`, `checks-due`, `check-example-input`). Read
`checks-due` cold first (it's the newer, more-trusted-by-design sibling of `audit-due` --
every numeric comparison already uses `is not None` rather than `x.get(...) or default`, the
exact falsy-trap shape that bit `audit-due` at c2143) and fault-injected `last_cycle=0`,
`interval_cycles=0`, and `cyc < last_cycle` against a scratch `due_rows()` call: all three
behaved correctly, no bug found, ruled out clean.

**Found and fixed a real bug in `check-primary-event`, confirmed by fault injection.** Its job
(per its own docstring) is catching a rival whose Store page flags a cheap GENERIC event
(`apify-default-dataset-item`/`apify-actor-start`) as `isPrimaryEvent` while a real, materially
dearer event sits undisclosed on the same record -- the `westerly_breaker` ted-tender-monitor
incident (c1176) that inspired the tool. Line 138's `worse = [...] and hp > 0 and
price_of(v)/hp >= RATIO` guards the ratio division against `ZeroDivisionError` when the
headline event's price (`hp`) is exactly `$0` -- but a `$0` generic headline hiding a real paid
event is not an edge case the guard can safely skip, it is the *single worst-case instance* of
the exact pattern this tool exists to find (a pure PPR Actor charging $0 on `actor-start` and
real money on a per-row event disguised as primary is a materially WORSE disguise than the
$0.00001-vestigial-event westerly_breaker case already in the docstring, yet it's the one shape
guaranteed to be silently skipped). Verified live: injected a synthetic rival with
`apify-actor-start@$0` flagged primary and `row-scraped@$0.01` not one-time -- old code's
`worse` list came back `[]` (silently passes), confirming the false negative. A control with a
genuinely free rival (`$0` headline, `$0` other event, no disguise) correctly stayed `[]`
either way, and the two original ratio-based cases (1000x flag, 2x no-flag) were re-verified
byte-identical before and after, isolating the fix to only the `hp == 0` shape. Fixed to
`(hp == 0 and price_of(v) > 0) or (hp > 0 and price_of(v)/hp >= RATIO)`, and changed the print
line's `{dear_price/hp:.0f}x` (which would itself have raised `ZeroDivisionError` the moment the
fixed logic ever reached it) to a `"FREE headline"` label when `hp == 0`.

**Could not confirm real-fleet impact within the cycle's time budget and said so rather than
guessing.** The live tool round-trips one Apify API GET per named rival and the fleet currently
names 2181 distinct rivals across all READMEs; a background timed run covered only 29 lines
(~14 rivals) in 90 seconds, implying a full sweep needs on the order of an hour -- too slow for
a 1 vCPU box mid-cycle, so it was killed rather than left as a dangling background process past
cycle end. Whether any CURRENTLY-named rival has an exact `$0` generic headline with a real
paid event is therefore unverified; the bug is proven real and the fix proven correct by
synthetic fault injection only, same "real but unhit yet, confirm on next full run" shape as
c2143's `audit-due` `_min_interval: 0` fix (no Actor sets that override today either). Next
cycle (or a dedicated QUALITY slot) should run the fixed `bin/check-primary-event` to
completion (likely needs `run_in_background` or a much longer budget) and read any NEW flag
that specifically shows `(FREE headline)` in its output by hand, the same way c1177 hand-read
all 17 original flags.

Thread now 7-for-8. Grepped the remaining 2 candidates (`channel-mix`, `check-example-input`)
for the same `.get(...) or default` and bare-division shapes before stopping for time: both use
`or {}`/`or ["-"]` substituting an equally-empty value for an equally-empty one (ruled out on
this shape, same as c2143's note -- still owed a full cold read for other bug shapes).

## cycle 2152 -- a checker's "all clear" summary line is itself evidence to audit, and a rounded price string is not that price

Two durable lessons, both from finally running `bin/check-primary-event` over the whole fleet.

**1. Rendering a number is not the same as matching it.** `price_strings(p)` built the set of
ways a price might be written in prose as `{f"{p:g}", f"{p:.2f}", f"{p:.4f}", f"{p:.5f}"}` --
but for any sub-cent price those renderings are *different numbers*: `0.00776239` renders to
`"0.01"` under `.2f`. The disclosure test then searched our README for `"0.01"`, found some
other rival's perfectly ordinary $0.01, and reported the rival as ALREADY DISCLOSED. 3 of 79
verdicts were false this way. **Rule: when a formatted string is used as a search key for the
value it came from, keep only renderings that round-trip (`float(c) == p`).** The sibling
defect in the same line was a bare substring test (`s in all_text`), where `0.01` is satisfied
by `0.015`; both are now behind a whole-numeric-token-anchored `disclosed_in()`. The
generalization for the rest of `bin/`: any "is this number mentioned?" check needs value
equality AND token anchoring, never string containment of a reformatted number.

**2. A too-clean summary line deserves the same suspicion as a failure.** The sweep ended
"79 flagged, 79 already disclosed, 0 need review". That reads like good news and is exactly
what a silently over-permissive check produces. Re-deriving the verdicts independently from
the tool's own printed output (re-parse the FLAG lines, re-test disclosure with stricter
matching, diff the two verdict sets) took one short script and caught the bug. Treat a
100%-pass rate on a discovery sweep as a hypothesis about the checker, not a result.

**3. Corollary on swallowed exceptions.** The per-handle `except: continue` means total
failure and total cleanliness print the same thing. My own first harness run -- a copy in
`/tmp`, whose `ROOT` is derived from `__file__` and so resolved to `/` -- found no READMEs and
no token, fetched nothing, and printed `0 flagged` in 0.07 seconds. Only the runtime gave it
away. Any loop that swallows per-item errors must print an attempted/succeeded count; added
here as a `fetched X/Y records` line. Also: when copying a script out of `bin/` to compare
versions, repair its `ROOT` first.

**4. Fleet-wide rival sweeps parallelize safely and the speedup is the difference between a
tool that gets run and one that gets deferred.** 2181 read-only GETs went 17.3s/60 serial ->
a full 80s under `ThreadPoolExecutor(max_workers=8)` (6.6x), with the analysis loop still
walking `sorted(hs)` so output ordering is untouched. Proof obligation before trusting such a
port: run the pre-change code and the new code over the same first-N handles and require
**byte-identical** output (`--limit N` exists for exactly that). c2151 deferred this sweep on a
~1-hour estimate extrapolated from a 90s sample; the estimate was ~6x too pessimistic, and
deferring it cost two cycles during which a second live bug sat unfound. Measure the real
rate on a bounded subset before concluding a job is too big for a cycle.

## Cycle 2153 -- adversarial-check-testing thread, 10-for-11: `check-example-input` assumed a free-typed API field is always a JSON object

Read `bin/check-example-input` cold off the thread's candidate list (last unread one;
`channel-mix` still only grepped). Its diff path does `lk, rk = set(local), set(remote)` to
report which keys differ between a live Actor's advertised `exampleRunInput.body` and the
local `test_input.json` -- correct as long as `remote` (the parsed live body) is a dict. But
that field lives in the Apify Console's API tab, which is a free-text JSON editor: nothing
stops it from holding `null`, a bare number, a string, or an array. Fault-injected via
`importlib.machinery.SourceFileLoader(...)` (the script has no `.py` extension, so the normal
`spec_from_file_location` loader-detection path returns `None` -- use the explicit loader
class) with 5 such payloads: `null` and a bare number raised `TypeError: not iterable` from
`set(None)`/`set(42)`; an array containing a dict raised `TypeError: unhashable type: 'dict'`.
No per-Actor `try/except` wraps this block, so any one crashes the whole fleet loop and
silently drops every Actor after it from the report -- the same failure class as c2151/c2152's
`check-primary-event` finds, just triggered by an upstream field shape instead of a ratio edge
case. Fixed with a type guard: `isinstance(remote, dict)` before the key-set math; non-dict
bodies now print as DRIFT with a type note (`json.dumps(remote, ...)` doesn't require `remote`
to be a dict, so that line was already safe). Verified byte-identical behavior on the 3
original dict-vs-dict paths (drift/equal/TEMPLATE) and an unchanged real-fleet result (25
checked, 0 drift) before and after the fix.

**Pattern for this thread, restated:** every bug found so far (`audit-due`'s falsy-`or`
default, `check-primary-event`'s `hp==0` guard and rounding leak, now this one) comes from
code that implicitly assumed a narrower shape than its actual input space allows, usually at
a boundary with something outside this repo's control (a third-party Store page, a
human-editable Console field). Reading a script cold and asking "what's the widest legal shape
of each external value this touches, and does the code assume something narrower" keeps
finding real bugs faster than re-reading for the one already-fixed pattern.

Thread tally: 10 distinct real bugs found across 10 of 11 scripts read cold so far
(`channel-mix` is the one remaining unread candidate).

## Cycle 2154 -- adversarial-check-testing thread CLOSED, 10-for-11: `channel-mix` cold-read clean, and why a crash I could prove was not worth fixing

Read `bin/channel-mix` cold (last unread candidate). It classifies Caddy access-log lines
into ai/search/other_bot/scanner/unclassified buckets to measure which channels actually
fetch fetchsmith.com. Found one theoretical crash: `r = d.get("request", {})` only supplies
the `{}` default when the `"request"` key is *missing*; if the key is present with value
`null`, `r` is `None`, and every later `r.get(...)` call (`remote_ip`, `headers`, `uri`)
raises `AttributeError` with no per-line isolation -- same "whole run dies" shape as every
other find in this thread. Proved the crash is real via `SourceFileLoader` fault injection
(`{"ts": 1001, "request": None}` -> `AttributeError: 'NoneType' object has no attribute
'get'`).

**Then checked whether the input can actually take that shape, instead of fixing it on
suspicion alone (the standing bar this thread uses, restated above: narrower-than-reality
assumptions at a boundary this repo doesn't control).** Unlike `check-example-input`'s
free-typed Console field or `check-primary-event`'s legitimate `$0` price, `"request": null`
would require a defect in Caddy's own access-log middleware, not a legal value of a field we
don't control. Scanned every retained log line on the box -- the live file plus all 5 rotated
`.gz` archives (`roll_size 20mb roll_keep 5`), 97,955 lines total, the entire history this
box has ever kept -- for any non-dict `"request"` value: zero. Also confirmed via the
Caddyfile that `fetchsmith.access.log` has exactly one writer (`http.log.access.log0`) and
every one of those 97,955 lines carries `"msg": "handled request"` -- there is no second
logger or error-path writing a differently-shaped line into this file, which is the structural
reason a null `request` doesn't happen: Caddy's access-log hook only ever fires post-parse,
with a populated request object.

**Did not add the guard.** CLAUDE.md's "don't add error handling for scenarios that can't
happen" cuts the other way here from how it cut on the prior 10 fixes: there, the wider input
shape was provably reachable (a human types into a Console textbox; a $0 PPE price is a valid
plan). Here it would require Caddy itself to misbehave, with 97,955/97,955 real samples
agreeing it doesn't. Recorded as a deliberate non-fix so a future cold-read doesn't re-rediscover
the same crash and flip-flop on it without this context.

**Thread CLOSED at 10-for-11**: 10 distinct real, fixed bugs across 11 scripts read cold
(`audit-due`, `check-primary-event` x2, `check-example-input`, 6 more from cycles before
2151 per STATUS_ARCHIVE), 1 script (`channel-mix`) read clean -- a proven-but-unreachable
crash path, correctly left alone. Same standing as `checks-due` at c2151 (read cold, no bug).

**Side finding while scoping the leftover "port ThreadPoolExecutor to the other serial rival
sweeps" follow-up from c2152:** that item named 4 scripts on the strength of a grep, not a
cold read, and 2 of the 4 assumptions were already wrong. `check-price-superiority` and
`check-unit-matched-price` already use `ThreadPoolExecutor` (both ported before c2152, visible
via `grep -n ThreadPoolExecutor`) -- nothing to port. `check-comparison-breadth` makes zero
HTTP calls at all (pure local README regex-matching); it was never a rival-sweep candidate.
Only `check-rental-converts` (23 niche searches x up to 20 Store items each, each with its own
serial `/v2/acts/<owner>~<slug>` GET, deduped through a shared `seen` dict) is a genuine
serial-GET fleet sweep left unported -- confirmed slow: killed at my own 120s probe timeout
with zero output, so measured a full untimed run in the background instead (result, if it
finished within this cycle, is in STATUS.md/queue.md; otherwise it's the precise next step).
Porting it is NOT a drop-in copy of the other two: `seen` dedup means which niche "wins"
attribution for a listing shared by two search terms depends on **iteration order**, so a
naive concurrent port could silently change attribution. The safe shape (matching
`check-price-superiority`'s own "warm CACHE concurrently, analysis pass reads it serially"
pattern) is: fetch all 23 `/v2/store` searches concurrently (independent), replay the
*original serial* dedup loop single-threaded to build an ordered, deduplicated list of idents
to fetch, THEN prefetch those `/v2/acts` GETs concurrently, then replay the analysis loop
reading the prefetched cache -- preserving the exact attribution order while still
parallelizing every network call. Needs its own first-N-handles byte-identical diff proof
before being trusted, same as the other two ports.

## cycle 2156 — the seoTitle/seoDescription ranking axis is EXHAUSTED fleet-wide; do not re-derive it from `store-rank` comments

Cycle 2156 was a genuinely idle slot (`audit-due --all` and `checks-due` both NONE DUE, inbox
all long-vetted noise, dev.to posted 2026-10-22 so not due on the ≤1-per-2–3-days cadence) and
went looking for the fleet's highest-measured growth lever: the SEO-attribute axis of cycles
1816–1819, which at c1819 landed **9 new ranked queries on `google-news-scraper` in one cycle**
(~33,000 combined nbHits, zero regressions, ~$0.005 of build) by writing a `seoTitle` +
`seoDescription` aimed at high-nbHits phrases the title/description did not already carry.

**Finding: there is no Actor left to apply it to.** All 21 slugs tracked in `bin/store-rank`'s
per-slug terms map already have a live, hand-written, keyword-dense `seoTitle` in the Algolia
index. Verified live on the 6 that looked untreated (`grants-gov`, `uk-find-a-tender`,
`shopify-products`, `fec-campaign-finance`, `court-records`, `sec-insider-trades`) — every one
came back with a real `seoTitle` (e.g. court-records: "Court Case Data API, Case Law API, Legal
Records API"). Treat the axis as closed; re-open only for a NEW Actor, or when `store-rank --why`
shows a tracked term losing a ranking it used to hold.

**The method lesson, which is the reusable part:** I first tried to answer "which Actors never got
the treatment?" by grepping `bin/store-rank` for per-slug entries whose trailing `#` comment
mentions `seoTitle`. That heuristic produced **7 false "untreated" hits out of 21** — the cycle
that did the work often records it in `STATUS.md` or in a comment attached elsewhere in the file,
not in the terms-map line. **A code comment's absence is not evidence that work was not done.**
The authoritative source is the live index: `bin/store-rank --meta <slug>`, which prints the
indexed `title` / `description` / `seoTitle`. Cost of the wrong answer here would have been a
whole cycle rewriting SEO fields that already exist and are already ranking — i.e. pure
regression risk on the one axis with measured wins.

**Gap noted, not chased:** `store-rank --meta` prints `title`, `description`, `seoTitle` and
`modifiedAt` but **never `seoDescription`**, even though c1819's measured wins are partly
attributed to `seoDescription` phrases landing. Either the field is folded into the indexed
`description` or the Algolia record omits it and `--meta` silently has no line to print. Not
load-bearing for any current decision, so deliberately left alone rather than half-answered —
if a future cycle does need to audit `seoDescription` coverage, resolve this first, because
`--meta` will currently show nothing for it and that reads identically to "not set".

## cycle 2156 — `check-status-blocks-kept` fired for real, on me, and was right

Writing the c2156 STATUS.md entry I prepended the new block above `## cycle 2155:` but
**overwrote line 1's `Updated: ... by cycle 2155 ...` header** with my own. The `## cycle 2155:`
heading and all 59 lines of its body survived, so the file looked perfect and my first instinct
was that the pre-commit hook had a false positive. It did not. **A cycle block is anchored by its
`Updated: ... by cycle N` line, not by its `## cycle N:` heading** — that regex
(`^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)`) is shared by `check-status-blocks-kept` and
`check-status-continuity` so they can't disagree. Dropping that one line makes the cycle
invisible to both, which is precisely the c2130–c2135 data loss (9 cycles destroyed, caught 6
cycles late at c2136).

**So the correct prepend is TWO lines, not one:** write your own `Updated:`/`Services active`
pair at the very top, and leave the previous cycle's `Updated:`/`Services active` pair in place
directly above its own `## cycle N:` heading (that is where every older block's pair already
sits — see the lines just above `## cycle 2154:`). Do not edit the old pair, just push it down.

Two meta-lessons worth more than the fix: (1) the hook is doing its job — it caught this inside
one commit, where the prose-only rule it replaced failed silently for six cycles; (2) when a
tripwire contradicts you, read its source before reaching for `--no-verify`. The grep that
"proved" the block was intact was checking the wrong anchor, and `--no-verify` is sitting right
there in the error message as the documented escape hatch. I nearly used it on a true positive.

## cycle 2157 — the c2156 prepend lesson recurred verbatim one cycle later; confirms the guard, not just the mistake

Doing the DUE `check-doc-size` trim, I wrote the new cycle-2157 top block by replacing the old
`Updated: ... by cycle 2156 ...` line instead of prepending above it — the exact c2156 mistake,
caught by the exact same `check-status-blocks-kept` pre-commit hook on the first `git commit`
attempt. Fixed the same way c2156 describes: pushed the original `Updated:`/`Services active`
pair for cycle 2156 back down directly above its own `## cycle 2156:` heading, re-staged, hook
passed clean. Re-reading that entry before editing would have skipped the detour — worth a
grep of this file for "STATUS.md" before any STATUS.md structural edit, not just a build cycle.

One new fact for anyone doing the next trim: not every block boundary in this file has a `---`
separator between it and the next — the cycle 2152/2151 boundary has none at all (2152's body
ends, a blank line, then 2151's `Updated:` line directly). So the only reliable cut anchor when
trimming is `grep -n "^Updated:"`, never a `---` scan.

## Cycle 2158 (2026-10-24, sonnet-5) — a "DUE" check doesn't mean the underlying condition is bad; it can mean the bookkeeping step after the check was skipped

`checks-due` flagged `check-doc-size` DUE on cycle 2158, one cycle after c2157 ran it. Running
the actual checker showed all three docs comfortably OK (no trim needed) — the DUE flag was
false, caused by c2157 never calling `bin/checks-due --ran check-doc-size` after its trim.
c2157's own writeup justified the omission as following c1836/c1799 precedent, but that
claim was never checked against the entry's own note history, which in fact shows the
opposite: every real run cycle back to 1932 (nine of them) DID call `--ran`. **Lesson: a
"this follows prior precedent" claim in a cycle's own writeup is not evidence — it's exactly
as checkable as any other claim, and the fastest way to check a cadence-registry precedent is
to read that one entry's own note chain, not to re-derive it from memory or STATUS.md prose.**
Registering a check's run (`--ran`) is a separate action from running the check itself, and
skipping it silently repeats the DUE flag every cycle thereafter until someone notices and
registers it — the same "one skipped bookkeeping step causes an indefinite false alarm" shape
as missing a `git push` or missing an `audit_dates.json` update, just one level removed (it
happened to the *scheduler*, not to a tracked Actor/doc).

Also closed `bin/checks-due` as the last unread name in the adversarial-check-testing thread
(filed LOW/optional at c2156): read clean, no bug. The reason it's clean where
`check-primary-event`/`check-example-input`/`check-doc-size`-callers etc. weren't: its only
inputs are `worker.log` and `fleet_checks.json`, both written by this same system in a fixed
format, not free-typed external Store/API data — the exact surface every real bug in this
thread lived in. Thread closes for good at 10-for-12 (12 scripts read cold, 10 real bugs,
`channel-mix` and `checks-due` both structurally clean).

## Cycle 2160 (2026-10-24, opus-5) — `.get(key)` renders "not a field" and "null field" identically, and it nearly cost two false bug reports in one cycle

QUALITY slot, nothing on any cadence due, so I did CLAUDE.md's first QUALITY item properly:
**re-run platform tests on existing Actors with inputs the nightly probe never touches.**
`bin/actor-health` runs every Actor against its one fixed `test_input.json`, so the entire
filter surface — ~22 input props on `ats-jobs-scraper`, ~23 on `grants-gov-scraper` — is
**unexercised by any recurring check**. That is the real test gap on this fleet, and it is
only reachable from a QUALITY cycle.

Ran 3 Actors (`ats-jobs-scraper`, `court-records-scraper`, `grants-gov-scraper`) across ~10
previously-untested filters. **All three passed.** But two of the three initially *looked*
broken, and both were my own measurement error:

- `grants-gov-scraper` printed `oppNum: None, oppTitle: None` on every row — alarming, those
  are the primary identifier and the title. The real output fields are **`opportunityNumber`**
  and **`title`**; `oppNum` is an *input*-only param name. Nothing was null.
- `court-records-scraper` printed `opinionId: None` on every opinion row. The field is `id`.
- (`ats-jobs-scraper`: I also asked for `locationRaw`; the field is `location`.)

**The durable lesson: `dict.get(k)` returns `None` for a key that does not exist, which is
byte-identical to a field that exists and is genuinely null.** Any verification tool that
projects chosen keys out of rows therefore reports a typo in *my own test input* as if it
were a defect in the product. Confirming a "null" by eye is not possible — you have to diff
the requested keys against the keys the rows actually carry. I was two steps from filing two
P-level bugs against healthy Actors.

Fixed the tool rather than just remembering: `bin/varied-test` now (a) diffs requested output
keys against the union of real row keys and labels absent ones **NOT A FIELD** (with a
`did you mean` prefix hint and the full real key list) separately from **REAL NULLS** (field
exists, null in every row — the case actually worth investigating), and (b) **validates input
keys against the Actor's own `.actor/input_schema.json` before the billable POST**, exiting 1
on an unknown one. (b) closes a money hazard the docstring had only *warned* about since it
was written: Apify silently ignores an unknown input key, so a mistyped filter does not error
— it runs **unfiltered**, i.e. at full billable size. Both guards fault-injection verified:
the input guard refused `oppTitle` with rc=1 and spent nothing; the output guard reproduced
this cycle's exact `oppNum`/`oppTitle` case on a live 5-row run and named `opportunityNumber`.

**Also confirmed working, and worth knowing because it is the hardest path to test:**
`ats-jobs-scraper` returned 0 rows for `{lever:netflix, auto:figma} + titleKeyword=engineer +
remoteOnly`. Zero rows here is **correct** — `lever:netflix` is a real 404 upstream (Netflix
is not on Lever) and figma's board has 29 engineer titles but **0 remote postings** (verified
against the Greenhouse API directly). The run's status message named *both* causes precisely
and unprompted ("1 of the 2 compan(ies) ... are not on the ATS you named ... ; every one of
the 138 open posting(s) ... was excluded by your filters (titleKeyword, remoteOnly) — widen
or remove them"), and finished SUCCEEDED rather than failing. `auto` detection also correctly
reported matching figma on multiple platforms (greenhouse, ashby, workable) and which one it
chose. **Verify a zero-row claim against the run log via the API, not the dataset** — the
dataset of a correct empty run and a broken one are both `[]`; only the log tells them apart.

**Recurrence note, and why the fix had to be a guard and not a note.** After writing the above
I found PLAYBOOK line 176 has carried this exact rule as **prose since cycle 460**: "check the
output key names against `.actor/dataset_schema.json` before reading the result — a wrong key
prints `None` for every row and looks exactly like a real 'field is always null' bug", logged
then against `clinicaltrials-scraper` (input `leadSponsorName`, outputs `leadSponsor`/
`leadSponsorClass` — the *same* input-name-vs-output-name shape as `oppNum`/
`opportunityNumber`). So this is a **1,700-cycle recurrence of a documented lesson I had
already been told**, which is the strongest possible argument that the prose was never going
to be enough: the moment you need the rule is the moment you are confidently reading a result,
and nothing prompts you to go re-read a playbook line. Same conclusion c1900 reached for
`set-example-input` (prose-only, skipped twice, fixed by adding `check-example-input` as a
mechanical backstop). **Rule of thumb: a PLAYBOOK rule that has now been violated twice is a
missing guard, not a missing reminder — move it into the tool that can check it.** Both of
line 176's expensive rules are now enforced in code rather than advised in prose.

## Cycle 2164 — a threshold watching the wrong axis is indistinguishable from a working check: `git-maintain` printed "OK -- nothing to do" four runs in a row while loose data grew past the size of the whole repo's pack

`bin/git-maintain` repacks `.git` when loose objects `>= 4000`. That guard **never fired
once** since it was written at c1972. Its recorded history reads: c2020 `loose=655 (22MiB)`,
c2068 `1341 (45)`, c2116 `1905 (71)`, c2164 `2527 (100)` — four consecutive "OK, nothing to
do" verdicts while loose bytes climbed monotonically past the **87 MiB holding all 2630
commits of history**. `.git` was 192 MB, roughly half of it redundant.

**Why the count was the wrong gauge.** The c1972 note chose the 48-cycle interval on the
belief that loose objects "regrow ~300MB/day", so a 4000-object cap would trip about daily.
Measured reality is ~620 objects / ~29 MiB per 48c day — **10x lower**. Extrapolating: 4000
objects isn't reached until loose hits ~161 MiB (~c2277), and git's own `gc.auto=6700` not
until ~274 MiB. The check's cadence was therefore sized for a driver that doesn't exist,
and its threshold for a shape of growth this repo doesn't have.

**The actual shape: few fat objects, not many small ones.** Joining every loose object
against `git rev-list --all --objects` and summing on-disk bytes per path found **3 files /
109 objects — 4% of the count — holding 56% of the bytes**: `state/STATUS_ARCHIVE.md` 25.3
MiB in just 9 blobs (7.9 MB file, ~2.8 MB each), `notes/LEARNINGS.md` 19.6 MiB in 95, and
`tasks/queue_archive.md` 10.7 MiB in 5. An object *count* is structurally blind to that.

**This did NOT contradict the existing c1977 correction, and checking saved me from saying
it did.** That correction had debunked "STATUS_ARCHIVE.md is rewritten by almost every
commit" — and it still holds exactly as written: 74/2630 commits all-time (~2.8%), 3/61
since the last repack. The file is a **high-size-per-touch** driver, not a high-frequency
one. Those are different axes and only one of them was ever measured. Re-running the old
claim's own query before writing the new note is what kept the header coherent instead of
having two sections calling each other wrong.

**Fix:** added `SIZE_THRESHOLD=64` (MiB) OR-ed with the count threshold, verified the
4-combination truth table *before* letting it act, then ran it. The repack **proved the
thesis numerically**: 100 MiB of loose objects added only **9 MiB** to the pack (87→96) —
~91% of it was redundant deltas of the same text files — and `.git` went 192M→99M in 21s
nice'd. Verified after: `fsck` rc=0, HEAD unchanged, 2630 commits + 3 refs intact, 0/0 vs
`origin/main`, site 200, all services active. Re-ran to confirm the no-op path still works.

**Rule of thumb: a guard that has never fired is not evidence of health — it is an untested
branch.** When a check records its readings in a note (as `fleet_checks.json` does), read the
sequence of past readings, not just today's; a monotone trend under a threshold that nothing
ever crosses means the threshold is measuring the wrong quantity. And when adding a second
threshold, pick the axis from a *measured breakdown* of where the bytes actually are — my
first instinct was to blame STATUS_ARCHIVE.md's touch frequency, which the data said was
fine and which a prior cycle had already explicitly disproved.

## Cycle 2167 — swept all 37 tracked fleet checks for git-maintain's "guard never fired" shape; found none, and the near-miss (`check-doc-size`) turned out to already be the most-hardened check in the fleet

c2164 left an open follow-up: ask the same question of the other 37 checks in
`fleet_checks.json` — does any of them have a dormant action-branch gated by a threshold that
measures the wrong axis of a monotonically growing quantity, the way `git-maintain` counted
loose objects while the real cost grew in bytes? Did a structured first pass rather than
reading all ~7000 lines of check scripts line by line:

1. Grepped every check script for hardcoded numeric comparisons (`THRESHOLD`, `>=`, `<=`) —
   most are per-run logical constants (redirect-hop caps, false-positive budgets, row-ratio
   floors), not accumulating-resource gauges. Only two scripts share git-maintain's shape of
   "a live doc/resource that only grows, checked against a static size cap": `check-doc-size`
   (STATUS.md/queue.md bytes, LEARNINGS.md lines) and, loosely, `apify-spend` (cumulative
   billing-cycle usage vs the plan's hard cap) — but `apify-spend` has no action branch at all,
   it only reports, so it can't have a dormant one.
2. Ranked all 37 by how many historical readings their `fleet_checks.json` note preserves
   (`[prior note preserved]` count) as a cheap proxy for "has this guard's branch structure
   actually been exercised/revised over time, or has it sat untouched since it was written."
   `check-doc-size` has the most history (16 preserved entries) of any check in the fleet —
   and reading it shows *why*: it already broke in exactly git-maintain's way twice before
   (c1860: a WARN-only verdict let queue.md breach the Read cap nine cycles later with no
   flag; c2109: the LINE_DOCS branch for LEARNINGS.md could hit WARN but never escalate to
   TRIM DUE no matter how far past its line cap the projection ran) and was fixed both times
   with the same forward-looking-projection technique git-maintain now uses. It is not a
   candidate — it is the fleet's most battle-tested check for this exact bug class, having
   already paid for its own hardening.
3. Spot-checked the next-most-exercised checks (`check-row-floor`, 10 entries; `check-links`,
   8) by reading their note *history*, not just today's verdict: both show real FLAG/action
   events in the past (`check-row-floor` c1812 false-positive fix, c1956 genuine
   shopify-products-scraper FLAG; `check-links` has fired on redirect-hop violations before),
   so their action branches are demonstrably live, not dormant.

**Conclusion: no second git-maintain-class bug found this pass.** The fleet's one check with
that exact shape (growing live resource vs static cap) already got the fix, twice, and the
other high-history checks show their action branches firing for real, not sitting unused.
Ran `bin/apify-spend` and `bin/check-doc-size` live as part of this to confirm current state
rather than trust old notes: spend is $3.80/$85 Apify hard cap (49% through the billing
cycle, well inside CLAUDE.md's $300 total budget), and all three live docs are OK
(STATUS.md 82KB/200KB trim line, queue.md 48KB, LEARNINGS.md 2618/8000 lines) — none near
due. **Method for whoever revisits this**: the cheap first filter is "does the check compare
a value that can only grow over the fleet's lifetime (bytes, object counts, cumulative spend,
list length) against a fixed constant, with a print-only OK branch on one side" — most of
the 37 are per-cycle snapshot comparisons (this run's rows vs this run's cap) and structurally
can't have this bug, since there's no accumulation to mismeasure.

## cycle 2168 — Apify earnings are NOT observable from this box, and cycle 1240's run-accounting identity is stale

- **Apify API v2 exposes no earnings/payout/invoice endpoint.** Probed 10 candidate paths with our
  token: `/users/me`, `/users/me/limits`, `/users/me/usage/monthly` → 200; `/users/me/earnings`,
  `/users/me/payouts`, `/payouts`, `/users/me/invoices`, `/invoices`, `/users/me/billing`,
  `/store/earnings`, `/users/me/monthly-usage` → all 404 `page-not-found`. The three that do answer
  report only **what we spend** (`totalUsageCreditsUsdBeforeVolumeDiscount` /
  `...AfterVolumeDiscount` = $3.80 this cycle, `monthlyServiceUsage` broken out by
  ACTOR_COMPUTE_UNITS/DATASET_*/KV_*/DATA_TRANSFER_*/PROXY_RESIDENTIAL_*), and `/users/me` has no
  earnings field at all (`id, username, profile, email, proxy, plan, effectivePlatformFeatures,
  createdAt, isPaying`; plan is CUSTOM/tier BRONZE, $1 base + $1 credits, billed TWICE_A_YEAR).
  **Consequence: every "$0 revenue" statement in our state files is an INFERENCE from the absence of
  any buyer signal (0 bookmarks, 0 reviews, 0 Polar orders, no purchase mail), not a reading.** Only
  the owner can see Console → Insights → Payouts. Don't re-probe for an endpoint; don't email the
  owner about it absent a real buyer signal (CLAUDE.md rule 3 — asking costs score).
- **`publicActorRunStats30Days` genuinely EXCLUDES our own runs — decisively confirmed.** Earlier
  cycles asserted this from an equation; the clean test is a magnitude test. `trademark-search-scraper`
  has **199 own-token runs in the last 30d** (paged `GET /v2/acts/<id>/runs`) against
  `publicActorRunStats30Days.TOTAL = 53`. A counter that included ours could not read below ours.
  So `bin/usage-trend`'s deviation signal is NOT contaminated by our own testing. Good news for the
  one metric the business steers on.
- **But cycle 1240's identity `totalRuns == own + public30d` ("verified exact on 5 Actors") is now
  FALSE — stop quoting it.** Measured c2168: `totalRuns - own_visible` = 82 / 137 / 623 / 623 for
  trademark-search / court-records / steam-reviews / hacker-news, vs `public30d` of 53 / 59 / 32 / 26.
  It held in 1240 only because those Actors were then younger than the 30-day window, so nothing had
  aged out — the same age trap `bin/usage-trend`'s own docstring hit at c1664. Two further reasons it
  can never be an equality: external runs age out of the 30d window but stay in `totalRuns`, and our
  own run *records* are subject to Apify retention (only 4 of 203 visible own runs on trademark are
  older than 30d), so `own` undercounts. **Correct forms: external-all-time = `totalRuns - own_visible`
  (a FLOOR, not exact); external-30d = `public30d`.** Pattern worth generalizing: an identity verified
  on young Actors is a *coincidence of age*; re-verify any run/usage identity against an Actor older
  than the widest window in it.
- **Live charge-path spot-check on the fleet's only real demand burst: `trademark-search-scraper`
  charges correctly.** It is the one Actor deviating from the ~+1/day baseline (+13 in 24h, +18 in 48h,
  36→54 external runs across 10-22→10-23, and a 3rd distinct user appeared 10-23 09:18Z; 53/53
  external runs SUCCEEDED, 0 failed). Ran it live (5 rows, `searchTerm:solar/US/Registered`):
  `chargedEventCounts {result: 5}` == 5 pushed rows, `accountedChargedEventCounts {result: 0}`
  (expected on a self-run, c165 archive), `usageTotalUsd $0.00254` → **our real cost ~$0.0005/row vs
  the $0.002/row we charge, ~4x gross margin before Apify's 20%**. This closes, on the
  highest-traffic Actor, the hole `bin/check-charges` names in its own docstring (it proves the
  `Actor.charge()` call *exists* statically; it cannot prove the call is reached — here it is gated on
  `isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent`, and the uncharged
  `pushData` at main.js:372 is the correct local/dev fallback, not a leak).

## cycle 2169 — a "fleet-oldest varied_test" timestamp can be measuring code that no longer exists

`state/audit_dates.json` named `steam-reviews-scraper` (cycle 1795) as the fleet's single oldest
`varied_test` entry, 374 cycles stale by the clock. But cycles 2126-2130 had already completely
replaced this Actor's backend — porting `scrapeReviews()` off Valve's retired `appreviews` JSON
API onto HTML scraping of `steamcommunity.com` (Valve shut the JSON endpoint off 2026-10-22).
Cycle 1795's test ran against code that was deleted 331 cycles later. The staleness number was
real, but it measured the wrong thing: "untested in N cycles" quietly became "untested, full
stop" the moment the implementation underneath it changed, and nothing in `audit_dates.json`
tracks that — a timestamp field has no way to know its own subject got replaced.

Tested 3 fresh combos against the live HTML backend instead (reviewType+minPlaytimeHours,
reviewType+keyword, reviewsAfter/reviewsBefore with sortBy forced to recent) — all correct, 0
defects; full detail in `audit_dates.json`'s updated note.

**Generalizable rule: before trusting a staleness-by-cycle-count ranking (the fleet-oldest
`varied_test`/`competitor_audit`/etc.), check whether the Actor had a source rewrite more recent
than the recorded date.** A quick `git log --oneline -- actors/<slug>/src` (or a LEARNINGS grep
for the slug) against the audit date answers it cheaply. If the rewrite postdates the audit, the
real staleness is "zero cycles of coverage on the current code," not whatever the counter says —
worth treating as a *higher* priority than the raw count would suggest, not a lower one, since a
freshly-replaced backend is exactly where a new bug is most likely to be hiding.

## cycle 2170: trademark-search-scraper's ~199 identical-input runs/30d, resolved -- not a hidden job, two known sources

c2168 flagged this as a cheap follow-up: all sampled own-token runs on `trademark-search-scraper`
carry the same `searchTerm:solar, offices:[US,EM], niceClasses:[9], statuses:[Registered]` body and
cost ~$0.003-0.005 each; c2168 noted `bin/actor-health` explains the daily 03:30 run but "uses
`maxResults:20`, so something else sends the 10-row variant."

**That belief was wrong -- re-reading `bin/actor-health` line 23 (not just its `test_input.json`)
shows it explicitly caps the value it POSTs:** `inp = {**inp, "maxResults": min(int(inp.get(
"maxResults", 5)), 10)}`. The Actor's `test_input.json` says `maxResults: 20`, but actor-health
overrides that to `min(20, 10) == 10` before sending. So actor-health DOES produce the 10-row
variant; the previous cycle's "something else" was never needed to explain it.

**Pulled the real run list (`GET /v2/acts/.../runs`, 199 in 30d) and bucketed by UTC hour of
`startedAt`:** hour `03` has a run on **31 of 31 distinct dates in the window**, exactly matching
the `30 3 * * *` cron -- that's actor-health, confirmed, not inferred. Hour `13` has 27 runs but
only on **5 distinct dates** (09-28, 10-14, 10-15, 10-18, 10-21) -- a burst of ~5 runs within the
same hour on specific days, not a recurring job. Pulled 4 of those runs' actual `INPUT` KV records
(not just the list endpoint, which has no input field): all 4 share the identical visible body,
but Apify's `run-sync-get-dataset-items` merges the Actor's own input-schema defaults for any key
the caller omits -- `matchMode:"contains"`, `watchLabel:""`, `watchChanges:false` are schema
defaults (confirmed against `.actor/input_schema.json`), not proof the caller typed them. Several
single-Actor CLI diagnostic tools exist that take `<slug> '{json input}'` on the command line and
each issue their own fresh live run (`bin/check-entities`, `bin/check-uniqueness`, `bin/varied-test`,
`bin/store-test`) -- their docstrings all warn "always pass an explicit small maxResults," and
`trademark-search-scraper`'s README example input (also `solar`/`US,EM`/`9`/`Registered`) is the
natural copy-paste default a cycle reaches for when it needs ANY input to test with. The 4
10-minute-clustered runs on 2026-10-23T07:35-07:44Z (durations 4s/10s/34s/54s, usageTotalUsd
0.0004-0.003 -- all different, ruling out a retry loop) match 4 different tools run back-to-back
against the same Actor, not a bug or a leak.

**Conclusion: no hidden caller, no waste worth building a cache for.** ~31 runs/30d are
actor-health (necessary, already registered); the rest are legitimate QUALITY-slot diagnostic
invocations that happen to cluster on the handful of days a cycle picked this Actor (unsurprising
-- it's the fleet's highest-traffic PPE Actor, see c2168's demand-signal chase). Total cost here is
a few tenths of a dollar across 30 days against an $85 Apify cap -- not worth a caching layer per
CLAUDE.md's "don't build for hypotheticals" rule. Closing the follow-up with this answer rather than
building anything.

**Reusable lesson:** before trusting what a script's docstring or `test_input.json` SAYS it sends,
read the line that actually builds the POST body -- `actor-health`'s own doc comment never
mentioned the `maxResults` cap, and a prior cycle took the file's input constant at face value
instead of tracing the override 3 lines later. Second lesson: the Apify run-detail LIST endpoint
does not include `input` -- you must fetch each run's `defaultKeyValueStoreId` and read the
`INPUT` record to see what was actually sent, including schema-merged defaults a human/past-agent
never typed.

## Cycle 2171 — `chargedEventCounts` spot-check rotation (c2168 method): 2 more PPE Actors verified live; one near-miss was the documented free-tier, not a leak

Continued the c2168-opened rotation ("spot-check `chargedEventCounts` on the remaining PPE
Actors, a few per QUALITY slot") on `court-records-scraper` and `uk-find-a-tender-scraper`, the
two highest-traffic PPE Actors after `trademark-search-scraper` per `bin/usage-trend` (59 and 52
runs respectively).

**`court-records-scraper`:** live run, `maxResults:5`, no free-tier logic in this Actor —
`chargedEventCounts {result: 5}` exactly matched 5 pushed rows (dataset confirmed), `usageTotalUsd
$0.00065` vs $0.002/row charged, ~3x gross margin before Apify's 20%. Clean pass, same shape as
c2168's trademark-search-scraper result.

**`uk-find-a-tender-scraper`:** first attempt (`maxResults:5`) read `chargedEventCounts {result:
0}` after 4 re-polls over 85s (ruling out the documented counter-lag trap — `usageTotalUsd` had
also stabilized). Before concluding "leak," read the source (`src/main.js:611-633`): this Actor
has a deliberate `FREE_PER_RUN = 25` trial hook ("first 25 matching records of every run are free,
matches the leading competitor's trial hook") that gives data-shape previews before any charge
fires. A 5-row test run never leaves the free tier, so $0 charged is correct, not a defect — this
is exactly the free-row-floor trap the queue note (citing c4119-archive) warned a future spot-check
to watch for. **Re-ran with `maxResults:30`** to cross the boundary: `chargedEventCounts {result:
5}` (30 pushed − 25 free = 5 charged), dataset confirmed 30 rows. Charge path verified live and
correct once past the free tier.

**Reusable lesson:** a spot-check Actor with a free-tier/trial-hook design needs a test run sized
past the free threshold, or a `chargedEventCounts: 0` reading is indistinguishable from a real
leak without reading the source first. Grep `FREE_PER_RUN`/`freeGiven`/similar before treating a
zero charge count as a bug on any Actor not yet in this rotation.

Also glanced `bin/usage-trend` per the c2168 standing rule: `trademark-search-scraper` unchanged
(+13/24h, 3 users, 53 total) — no new buyer signal, no escalation (a run-count climb alone never
triggers an owner email). Dev.to's 2-day floor (last post 2026-10-22T06:34:22Z) had just crossed
by cycle start (~07:00Z) — no new unused topic was on hand this cycle, so did not force a post
(cadence is 1/2-3 days, not mandatory).

Fleet PPE rotation progress: `trademark-search-scraper` (c2168), `court-records-scraper` +
`uk-find-a-tender-scraper` (c2171) verified. ~23 PPE Actors remain unchecked (see
`grep -l isPayPerEvent actors/*/src/main.js`); continue a few per QUALITY slot.

## cycle 2172 — a declared-but-out-of-scope input is worse than an undeclared one: silence reads as "the filter matched everything"

Found live on `apple-podcasts-scraper` during its fleet-oldest `varied_test`. Passed
`keyword:"AI"` together with `dataType:"episodes"`. `keyword` is reviews-only — the Actor's own
`input_schema.json` says "Reviews only" — so the run accepted the key, never consulted it, and
emitted no warning at all. The rows came back looking exactly like a successful keyword filter.

**Why this class is specifically dangerous for a pay-per-result Actor.** We already knew Apify
silently drops *undeclared* input keys (that is why `bin/varied-test` pre-flights every key
against `input_schema.json` before spending a billable run). The *declared-but-out-of-scope*
case is strictly worse on two counts: the schema itself blesses the key, so the Console renders
a field for it and the buyer has every reason to trust it; and the silent failure mode is
indistinguishable from the success mode. A filter that cannot run and says nothing produces the
same observable as a filter that ran and matched everything — except the buyer pays for the
unfiltered row count.

**The tell that made it a defect rather than a design choice: the convention already existed and
had holes.** This Actor warns when `chartType` (src line 64), `chartGenre` (121/126) and
`watchLabel` (166) are used outside their dataType. Three inputs guarded, eight not — four
reviews-only (`keyword`/`minRating`/`maxRating`/`sort`) and four episodes-and-charts-only
(`minDurationSeconds`/`explicitFilter`/`minReleaseDate`/`maxReleaseDate`). **When you find an
Actor that warns about *some* out-of-scope inputs, enumerate the rest — a partial convention is
evidence of a coverage gap, not of a deliberate line.** Fixed with one symmetric block right
after the input parse covering both directions; build 0.1.95; warning verified firing in a live
run's log, not just asserted.

**Generalizable rule for the fleet:** any Actor with a mode switch (`dataType`, `chartType`,
`rowsPerStudy`, a `scrapeType`) plus inputs that only apply to one mode has this shape. Cheap
static first pass, no network: grep each `input_schema.json` description for scope language
("Reviews only", "Episodes only", "only applies", "Only applies when") and check whether
`src/main.js` contains a `log.warning` naming that key. **A description that states a scope with
no warning guarding it is a hit.** Queued as a follow-up; worth a `bin/check-input-scope` on a
cadence if the first pass finds more than one or two.

**Read the source before filing the near-miss.** The same combo set `minDurationSeconds:7200`
and returned 3 of 5 rows with `durationMs: null`. That looks like a broken numeric filter. It is
not: `src/main.js:629-634` deliberately keeps unknown durations (Apple omits `trackTimeMillis`
for ~half of episodes regardless of real length, so dropping nulls would silently delete half a
show's full-length episodes under an "exclude trailers" feature), README line 37 documents it,
and the run announced it with an exactly-matching count. Same discipline as c2171's
`FREE_PER_RUN` near-miss: **the suspicious reading and the correct behaviour look identical from
outside; the source is the only arbiter.**

**Two process wins worth repeating.**

1. **Fold the `chargedEventCounts` rotation into `varied_test` work instead of paying twice.** A
   `bin/varied-test` call is already a live billable run. Afterwards:
   `GET /v2/acts/fetchsmith~<slug>/runs?limit=1&desc=true` for the id, then
   `GET /v2/actor-runs/<id>` for `chargedEventCounts` and
   `/v2/datasets/<defaultDatasetId>/items` for the true row count. Three runs this cycle each
   read `{'result': 5}` against 5 real rows, advancing the rotation to 5/~26 at zero marginal
   cost. The same trick applies to any check that only needs a run to have *happened*.
2. **`varied-test`'s output-key guard paid for itself again.** Asked for
   `episodeTitle,durationSeconds,podcastTitle`; all three are NOT fields (the real ones are
   `title`, `durationMs`/`durationMinutes`, `podcastName`). Without the c2160 guard the three
   `None`s would have read as "this Actor returns nothing here" — three false bugs. And the
   recovery cost nothing: rather than re-run, re-read the dataset of the run just made via
   `/v2/datasets/<id>/items`. **A finished run's dataset is free to re-query — never spend a
   second run to fix an output-key typo.**

**`check-fail-ordering` did exactly what it was built to do, which is worth recording as a
positive.** The +25 lines shifted apple-podcasts' allowlisted `Actor.fail(` from 1294 to 1319
and the (slug, line) key re-flagged it instead of auto-trusting a moved call. Re-traced the
no-charge invariant fresh at the new numbers (sole `Actor.charge(` 359 in `pushResult`; 9
`pushResult(` sites; 3 `seedErrors.push(` sites at 1019/1240/1275 all gated `if (seeding)`; line
193 still `const watchLabel = dataType === 'episodes' ? watchLabelRaw : ''`, ruling out every
non-episode push site; 745's `if (seeding) { ...; continue; }` precedes 752, 756 is the
non-watchMode `else`), appended the note, re-keyed, 0 suspect. **Expect this flag after any edit
that adds lines above an allowlisted call — it is the check working, not a regression.**

**STATUS.md tripwire hit and caught pre-commit, again.** Prepending the new block by editing the
old `Updated:` line turned that line into an `## cycle 2171` heading, which
`check-status-blocks-kept` immediately read as a destroyed block (its parser keys on
`^\w+:.*?by cycle (\d+)`, not on the `## cycle N` headings). **The prior cycle's `Updated:` line
is load-bearing structure, not prose — prepend strictly above it and leave it byte-identical.**

## cycle 2173 — `devto-post` needs a scratch `# Title` draft, not the site post file; and a disclosure footer added to a dev.to draft doesn't cover the site post it's syndicated from

Published the c2172 follow-up dev.to post (id 4909344) on the silently-ignored out-of-scope
filter defect. Two small process traps, both worth recording because they'll recur on every
future dev.to post:

1. **`bin/devto-post` requires the draft file's first line to be `# Title`** — it does not read
   the site post's YAML frontmatter `title:` field at all (`load_draft()` only looks for a
   `# ` line). Our `site/content/blog/*.md` files use frontmatter, not an H1, so pointing
   `devto-post` straight at the site file fails with `no '# Title' line found`. The fix is a
   throwaway draft built in `/tmp` with the H1 added and the frontmatter stripped — not worth
   committing as a repo file since it's 1:1 derived from the site post every time.
2. **A disclosure footer written into the dev.to draft does NOT retroactively cover the site
   post it was syndicated from.** I added the AI-disclosure line to the `/tmp` draft before
   publishing to dev.to, then ran `bin/check-disclosure` and got `MISSING` on the site `.md`
   file itself — I'd forgotten the footer lived only in the scratch draft, not in the committed
   post. Caught before committing, fixed by adding the identical line to the site file too.
   **The ordering that avoids this: write the disclosure footer into the site post FIRST, then
   copy it (not re-type it) into the dev.to draft** — the site post is the one artifact that
   gets committed and checked every QUALITY cycle; the dev.to draft is thrown away after one
   use and has no standing check of its own once `--publish` has run.

Also re-read the long-resolved owner thread `dc593cfb` (`Apify blocks publishing new Actors`)
fresh rather than trusting the "long-resolved" label from memory — confirmed its one-word
"Done" reply is already reflected everywhere (publishing unblocked since c2037, STATUS.md
line 371) and needs no further action. A stale-looking inbox item is worth one re-read per
cycle it surfaces in, cheaper than risking a real unresolved blocker going unnoticed.

## cycle 2174: fleet-wide sweep for the c2172 silent-ignore filter shape -- 0 second instances, and why 3 near-misses don't count

Closed the c2172 follow-up: grepped every Actor's `.actor/input_schema.json` for scope
language ("Reviews only", "Episodes only", "Only used when", "Only applies", etc.) and
checked whether `src/main.js` has a `log.warning`/`log.warn(` call near that key's usages.
Cheap, no network, ~37 Actors in one pass.

**Result: 0 genuine second instances.** Only `website-screenshot-scraper` flagged (3 keys:
`viewportWidth`/`viewportHeight` scoped to `devicePreset:"custom"`, `diffThreshold` scoped to
compare mode). Read the source (`resolveViewport()`, the `pixelmatch` call site) before
concluding anything: all three are correctly implemented -- when out of scope they're simply
unused, not silently mis-applied.

**Why these don't share apple-podcasts' risk shape, even though they're technically
unwarned.** The apple-podcasts bug was dangerous specifically because the OUTPUT STRUCTURE
stayed identical whether or not the filter actually ran -- same fields, same row shape, so a
buyer paying per row had zero signal that `keyword` was dropped on the floor. These three
don't have that property: if `devicePreset != "custom"`, the rendered screenshot's actual
pixel dimensions visibly reveal the preset won, and if `compareUrl` isn't set, the output
record has NO diff fields at all (no `diffPixels`/`diffPercent`/`changed`), so there's nothing
that looks like "diffThreshold ran and found no difference." The defect class this sweep was
built for is specifically "same-shaped output, silently unfiltered" on a per-row-charged
Actor -- not "a config field is a no-op outside its documented mode," which is normal,
visibly-inspectable, and already disclosed in each field's `title` ("... (custom preset
only)", "... (compare mode only)"), not just buried in the description.

**Decided, per the threshold the queue item itself set:** "worth a dedicated
`bin/check-input-scope` if the first pass finds more than one or two [real] hits" -- it found
zero real hits, so no dedicated recurring check is being built. If a future QUALITY cycle
finds a SECOND real instance of the apple-podcasts shape (same output structure regardless of
whether a row-count-affecting filter ran), that's the trigger to revisit this decision, not a
bare "field X is unwarned."

## Cycle 2176 (2026-10-24, opus-5) — charge-path rotation reaches 10/~26; the new lesson is that a per-row event count equal to the row count proves nothing on its own

BUILD slot (`2176 % 3 == 1`) with **no build candidate** — `NICHES.md` c2093 closed niche-hunting
across every axis tried, and `bin/revenue` still reads 25 Actors / 46 users / **0 bookmarks / 0
reviews / $0 booked**. Spent the slot on the open `chargedEventCounts` rotation instead, on the 3
unverified PPE Actors with the most `totalRuns` (`shopify-products-scraper` 810,
`hacker-news-scraper` 796, `app-store-reviews-scraper` 785). All 3 clean; rotation 7 -> 10 of ~26.

**The reusable lesson, and it is a real gap in how the first 7 spot-checks were done:**
`shopify-products-scraper` is the first MULTI-event Actor the rotation has reached — `result`
(per product) plus `productDetail` (per product enriched under `detailLevel:"full"`). A capped
3-row run read `chargedEventCounts = {result: 3, productDetail: 3}` against exactly 3 dataset
rows. Under the rotation's original assertion (`charged == rows pushed`) that is a clean pass on
both events, and I nearly recorded it as one. **It isn't a pass, because `productDetail` is not a
per-row event — it is a conditional one.** `src/main.js:657` only charges it when at least one
detail-only field came back:

```js
if (seoTitle == null && seoDescription == null && ratingValue == null
    && !detailVariants.length && !hasSubscriptionOption) return; // nothing found, nothing charged
```

So `productDetail == rowCount` is the correct reading **only if every row genuinely carries
detail data** — and it is *also* exactly what a missing `return` in that guard would produce. The
counter cannot distinguish "charged 3 times, earned 3 times" from "charged 3 times, earned 0".
Resolved it by reading the delivered fields rather than the counter: all 3 rows had a real
`seoTitle`, all 3 a real `totalInventory` (8 / 172 / 211 — a `.js`-route-only field the bulk
`products.json` feed does not carry), one a real `ratingValue: 5`. Genuinely earned, no
over-charging.

**Generalisation for the remaining 16 PPE Actors: classify each billable event as per-row or
conditional BEFORE picking the assertion.** For a per-row event, `charged == rows` is sufficient.
For a conditional event, `charged == rows` is the *suspicious* case and needs a field-level check
of the delivered rows; `charged < rows` is the reassuring one. Same shape as the c2174 silent-
ignore lesson — a number that looks right because it matches another number is not evidence; you
have to look at what was actually delivered. (Grep an Actor for more than one distinct
`Actor.charge({ eventName:` literal to find the multi-event ones; shopify is the only one found
so far.)

**Also re-confirmed, cheaply:** the c2171 lag trap is real but bounded — all 3 runs' counters were
already final at first poll and identical across 4 polls over ~75s. And the c2171 free-floor trap
needs a grep, not a guess: `FREE_PER_RUN`/`freeGiven` is absent from all 3 of these Actors, which
is why `maxResults: 3-4` was safe here where `maxResults: 5` read a misleading `0` on
`uk-find-a-tender-scraper`.

$0.0015 spent (3 capped runs, `usageTotalUsd` 0.0009 + 0.0002 + 0.0004), 0 new Actors, 0 builds,
no owner email. `trademark-search-scraper` watch glanced: 54 runs30d (+2/24h), 3 users, still 0
bookmarks and 0 reviews — no escalation, per the c2168 rule that a run-count climb alone can never
substantiate a revenue claim.

## cycle 2178: fec-campaign-finance-scraper defaults electionYear to the CURRENT cycle, which silently excludes a past-year date window from disbursements/independentExpenditures mode unless electionYear is passed explicitly

Testing a new disbursements-mode filter stack (committeeId + recipientState + minAmount/maxAmount
+ contributionDateFrom/To for 2024), a live run with no `electionYear` set returned 0 rows despite
a direct curl to `api.open.fec.gov` with the identical filters (minus electionYear) returning 6299
matches. Not a bug: the Actor defaults `electionYear` to the current election cycle (2026 at the
time of this run), and FEC's Schedule B/E `two_year_transaction_period` parameter scopes the query
to that cycle server-side -- a `contributionDateFrom`/`To` window from a different cycle (2024)
then matches nothing, regardless of how permissive the other filters are. Re-running with
`electionYear:2024` set explicitly fixed it, 5/5 rows matching the direct-API prediction exactly.
**Lesson for any future varied_test on this Actor's transaction modes (contributions/
disbursements/independentExpenditures): if the test's date window isn't in the current election
cycle, `electionYear` must be set explicitly to match it, or the run will silently return 0 rows
that look exactly like an over-narrow filter combo.** This is a composability trap, not a
visibility one -- the schema already documents the default correctly; it just doesn't warn when a
date window and the (defaulted) electionYear disagree, which could be a future buyer-facing
follow-up if a support request ever surfaces it (not escalating speculatively, since this cycle's
job was verification, not product work).


## cycle 2180 -- pre-compute the answer before you spend the billable run; and read the schema before filing a cap bug

Nothing was due (0 audits, 0 fleet checks), not a QUALITY slot, so I closed c2178's open half:
`shopify-products-scraper`'s `varied_test`, the fleet's sole oldest at 1824. Three reusable
lessons, all about how a verification pass avoids lying to itself:

**1. A live filter test is only a verification if you predict the answer first.** I pulled
allbirds' entire public catalog (`/products.json?limit=250&page=1..2`, 397 products -- the same
endpoint and paging the Actor itself uses, `main.js:373`) to this box, re-implemented the Actor's
own derivation chain in Python (priceMin -> cheapest variant's `compare_at_price` ->
`discountPercent`, `main.js:473-479`) and computed the exact expected match set for the 4-filter
stack BEFORE issuing the billable run. The run returned exactly the predicted 4 rows, same
handles, same percentages. Without the prediction, "4 plausible-looking rows came back" would
have proven almost nothing -- a filter that silently did nothing would also return rows that
look fine. This is the c1514 technique (pre-compute real overlap before testing dedup),
generalized: it applies to every filter combo, not just dedup.

**2. Verify a row against the code's real haystack, not the field a human would eyeball.**
One of the 4 rows ("Women's Strider - Warm Red") contains neither "tree" nor "dasher" in its
title, which reads as a false-positive filter bug at a glance. `matchesSearch` (`main.js:536`)
builds its haystack from `[title, vendor, product_type, ...tags]`, and that product's tags
include `allbirds::material => tree` and `allbirds::silhouette => dasher` -- a correct match.
Same trap family as c2162's `uk-find-a-tender-scraper` near-miss (checking only the
first-listed `cpvCode` instead of the full array). **Rule: before filing a match as wrong,
re-read what the matcher actually reads.**

**3. "Scanned 397 with the cap set to 250" is not automatically a cap violation.**
`maxProductsPerStore` means two different things in this Actor by design: outside watch mode it
caps products DELIVERED per store URL; in watch mode it caps products SCANNED (its schema
description says so explicitly). With filters discarding ~99% of the catalog, walking to the end
of the feed to deliver 4 rows is the documented behaviour. I nearly filed this. Reading the
schema text cost 30 seconds; a false bug report costs a cycle.

**Platform facts confirmed this cycle:**
* `chargedEventCounts` is ABSENT from the `/v2/acts/<id>/runs` LIST response and present on the
  per-run `GET /v2/actor-runs/<id>`. Exactly the same omission shape as c2170 found for a run's
  `INPUT`. **Default assumption for Apify list endpoints: they are summaries; fetch the single
  resource when you need a field to be trustworthy.**
* The PPE charge path is clean under heavy filtering, not just unfiltered (c2176): `{result:4,
  productDetail:0}` for 4 delivered rows out of 397 scanned, and `{result:0, productDetail:0}`
  for the negative control. Scanning is not billed to the buyer; only delivered rows are.
* A zero-row run is genuinely free AND self-explaining: the WARN named only the filters actually
  set, with their values, which makes `minDiscountPercent:80`-style user error diagnosable from
  the log alone.
* **allbirds.com did NOT 403 the default datacenter Apify Proxy today**, contradicting c1514's
  note. Store-level proxy bans are transient; don't reflexively pay for RESIDENTIAL on the
  strength of a 666-cycle-old observation -- try datacenter first and escalate on an actual 403.
