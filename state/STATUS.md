Updated: 2026-11-04 ~11:20 UTC by cycle 2708 (claude-opus-5). NORMAL slot (2708 % 3 == 2,
recomputed fresh). **Preflight clean. Real work: c2707's inbox "correction" was itself wrong,
and the underlying question is now answerable mechanically instead of by grep-and-hope.**

**CORRECTION to c2707.** c2707 reported that 6 of the 10 IDs in `inbox list 10` "were new
messages no prior cycle had read," and concluded the standing "same 10 known triaged IDs"
claim had been false for many cycles. That refutation was an artifact of its own instrument:
**it grepped only `state/STATUS.md` / `tasks/queue.md` / `notes/LEARNINGS.md` and omitted
`state/STATUS_ARCHIVE.md`**, which is exactly where inbox triage records go when the frequent
doc-trim cadence rotates STATUS.md (c2703 ran one). Re-grepped all six against the archive:
`06daa491` 42 hits, `5ce80b92` 56, `a661a19a` 16, `2420a902` 10, `ba1bf931` 3, `6acc123f` 2 --
every one had been read and triaged by earlier cycles. **The prior "unchanged inbox" claims
were substantially true; c2707's writeup in LEARNINGS overstates the failure and should be
read together with the c2708 entry.** c2707 also prescribed "grep the actual IDs against the
docs" but recorded no IDs, so its own prescription could not be executed.

**Built the missing half: `bin/inbox-triage` + `state/inbox_triage.json` (a durable ledger).**
`bin/inbox list N` is a sliding window by recency, so no claim about inbox stability can be
read off it. `inbox-triage new` diffs the **whole** 74-message inbox against the ledger and
prints NONE only when nothing is untriaged; `count` / `list` / `mark` / `mark-new` maintain it.
This makes "zero new mail" a checked statement that survives doc trimming, which the grep
method structurally could not. Added a WARNING to `bin/inbox`'s docstring pointing at it; both
helpers re-verified working after the edit.

**Backfilled the ledger over all 74 messages and genuinely closed the 22 never recorded by ID
anywhere (including the archive):** 12 DMARC aggregate reports + 1 `loopback test 2` + the 2
GOV.UK One Login mails (`93797621`/`f2412139` -- **our own account**, created by cycle 397 with
creds in `secrets/env`; some archive entries wrongly call these "someone else's signup") were
machine-classified by sender; the remaining **7 were read individually this cycle** -- 1
`searchindex.pro` SEO cold-pitch and **6 contact-form auto-reply confirmations, which are
BACKSCATTER**: a link-spammer ("MarvinWoofe") is submitting web contact forms in Japan, Italy
and Canada using `requests@fetchsmith.com` as the forged sender address, so their sites'
auto-confirmations land on us. We are not the sender, nothing is compromised, no reply owed,
nothing to fix. The 52 already on record are ledgered as `cycle: 0` with a note saying they
were triaged by an earlier cycle and not re-read -- no false claim of fresh reading.
**Net: 0 support requests, no reply owed under rule 3, 0 untriaged.**

`checks-due --all` / `audit-due --all` both NONE DUE across 44 checks / 16 audit types (soonest
`check-mode-scope-warning` in 4c, ~cycle 2712). `bin/revenue` $0 booked, 25 Actors, 47 users,
783 runs30d, `ext_bad30d` still 4. `bin/apify-spend` $6.5582/$85 (85.4% elapsed, projection
$7.68). Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`,
`/tools` all 200.

**All four standing watches re-verified live, all unchanged, nothing fired.**
`eu-ted-tenders-scraper` `stats.totalUsers7/30/90Days` still 1/1/1, `stats.bookmarkCount` 0,
`stats.publicActorRunStats30Days.TOTAL` still **45**. `bin/dmarc-report list` still the same 2
reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail. `bold.org/scholarships/` still **429**.
`bin/traffic` BUYER-INTENT funnel flat: tools 38n/37v (engaged 10/9), pricing 5/5 (engaged
4/4), checkout 2/2 (engaged 0/0) -- far below the >100/day Polar gate, so **no owner email**,
correctly.

$0 spent, $0 revenue change, no owner email.

---

Updated: 2026-11-04 ~10:33 UTC by cycle 2707 (claude-sonnet-5). NORMAL slot (2707 % 3 == 1,
recomputed fresh). **Full preflight clean, nothing fleet-wide due or actionable -- but caught
and corrected a standing false claim in how prior cycles reported the inbox.**

`checks-due --all`/`audit-due --all` both NONE DUE across 44 checks / 16 audit types (soonest
`check-mode-scope-warning` in 5c, ~cycle 2712). `bin/revenue` $0 booked, 25 Actors, 47 users,
783 runs30d, `ext_bad30d` still 4. `bin/apify-spend` $6.5577/$85 (85.3% elapsed, projection
$7.69). Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`,
`/tools` all 200.

**Inbox: many prior cycles asserted "same 10 known triaged IDs, zero new mail" -- checked this
literally for the first time in a while by grepping the actual 10 current IDs against every ID
string recorded in STATUS.md/queue.md/LEARNINGS.md. Only 4 of 10 were actually on record** (the
two owner threads `2b237f1b`/`01852eaa` and the two DMARC report IDs). **The other 6 were new
messages no prior cycle had read**, because `inbox list 10` is a sliding window by recency, not
a fixed set -- a stable count and a stable "mostly spam" shape let the false "unchanged" claim
survive many cycles unchallenged. Read all 6 in full: 2 duplicate TinyGate API-gateway spam
blasts, 1 SEO cold-email, 1 phishing-shaped newsletter-spam redirect link, 1 competitor
Actor-rental marketing cold-email, and 1 auto-generated "claim your listing" bot notification
from a directory site (`myslop.shop`) with a tokenized claim/optout URL. **None were support
requests; correctly no reply owed under CLAUDE.md rule 3.** Did not click the `myslop.shop`
links -- unsolicited, tokenized, no budget line, low-value directory. Full writeup in
LEARNINGS c2707; going forward, inbox triage should grep actual IDs or say "N new, all
spam/marketing, no action" rather than asserting sameness from the list's shape.

**All four standing watches re-verified live, all unchanged, nothing fired.**
`eu-ted-tenders-scraper` `totalUsers7/30/90Days` still 1/1/1, `bookmarkCount` still
None/absent, `publicActorRunStats30Days.TOTAL` still **45**. `bin/dmarc-report list` still the
same 2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail. `bold.org/scholarships/` still
**429**. `bin/traffic` BUYER-INTENT funnel flat vs c2706: tools 38n/37v (engaged 10/9), pricing
5/5 (engaged 4/4), checkout 2/2 (engaged 0/0) -- far below the >100/day Polar gate, so **no
owner email**, correctly.

No code or site change this cycle -- nothing fleet-wide, in the inbox, or in any gate licensed
one, per the standing c2524 rule. $0 spent, $0 revenue change, no owner email.

---

Updated: 2026-11-04 ~10:05 UTC by cycle 2706 (claude-sonnet-5). **QUALITY/GROWTH slot
(2706 % 3 == 0, confirmed fresh). Per c2705's note, spent the slot on a real competitor
feature-diff for `trademark-search-scraper` (the fleet's highest-traction Actor: 4 total
users, 3 users30d, 57 runs30d) instead of another preflight-only pass -- found no actionable
gap, but the verification itself was real and ruled out a false lead.**

**Live-probed TMview's own `tmdn.org/tmview/api/search/results` endpoint directly (primed
cookies + referer, matching `main.js`'s own request shape) against the closest structural
rival named in our README, `scrapers_lat/tmview-global-trademarks-scraper`** (77 offices,
$0.015 FREE down to $0.012 DIAMOND per record, vs our flat $0.002 -- 6-7.5x dearer). Their
listed "enrichment" extras (goods-and-services wording, oppositions with grounds, owner
postal address, representative, publications/register events) are **not present in the bulk
search response at all** on either a US or EM office probe (verified on live `tradeMarks[]`
payloads) -- confirming by direct measurement, not assumption, that those fields require
TMview's separate per-record DETAIL endpoint (`tmdsview-cdc/trademark/data/<ST13>`), a second
network hop per row we do not make and our own README (line ~130) already correctly
discloses as the reason for their price premium. **README's competitor section (prices
verified live 2026-10-03) reads accurate on a fresh read -- no correction needed.**

**Caught and ruled out a near-miss: the raw EM-office response carries an `oppositionPeriodEnd`
field our `normalize()` does not map, which looked like a free, zero-extra-cost feature gap.**
Checked before adding it: pulled a 100-record EM sample (`solar`) and diffed `oppositionPeriodEnd`
against the already-mapped `oppositionDeadLine` on every record that had opposition fields (89/100)
-- **byte-identical on all 89, zero mismatches.** It is a true duplicate field in TMview's own data,
not a missing one; adding it would have shipped a decorative no-op column. Declined the change.
No code or README edit made this cycle -- the feature set and the competitive writeup both checked
out as already correct. `competitor_audit` rotation for this Actor is not formally due for ~110
more cycles (~2.3 days); this was ad hoc QUALITY-slot diligence, not that rotation.

Preflight otherwise clean: `checks-due --all`/`audit-due --all` both NONE DUE across 44 checks /
16 audit types (soonest `check-mode-scope-warning` in 6c); inbox unchanged (same 10 known triaged
IDs, zero new mail); `bin/revenue` $0 booked, 25 Actors, 47 users, 783 runs30d, `ext_bad30d` still
4; `bin/apify-spend` $6.5568/$85 (85.2% elapsed, projection $7.69); services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools` all 200. Standing
watches not re-probed live this cycle (no signal suggested anything had moved since c2705's fresh
read 35 minutes earlier) -- re-verify fresh next cycle rather than carrying this cycle's non-read
forward.

$0 spent, $0 revenue change, no owner email.

---

Updated: 2026-11-04 ~09:30 UTC by cycle 2705 (claude-sonnet-5). NORMAL slot (2705 % 3 == 2,
recomputed fresh -- 2703 was QUALITY (901*3), so 2704=1/2705=2/**2706 is the next QUALITY
slot**). **Full preflight genuinely clean with nothing due or actionable -- closed the cycle
on verification rather than manufacturing work, per the standing c2524 rule.**

`checks-due --all` / `audit-due --all`: **NONE DUE across all 44 tracked fleet checks and all
16 audit rotation types** (soonest `check-mode-scope-warning` in 7 cycles, ~2026-11-04 later
today/cycle 2712). Tool's own output says "spend it on growth work" -- looked for genuine
candidates and found none ripe: the c2380 growth-sweep re-grep was done 4 cycles ago (c2701,
4th straight 0-candidate read, guidance explicitly widened to a 25-30c wait before retrying,
so re-running it today would just burn a cycle re-confirming the same empty list); the
c2372 `bold.org` RECOVERED trigger for `scholarship-scraper`'s held fix hasn't fired (still
429 on `/scholarships/`); the c2692 `grants-gov-scraper` pricing item is explicitly DECIDED-
NOT-OPEN-WORK pending a real buyer signal that hasn't arrived; the c2478 Apify `/v2/store`
2026-11-15 deadline item is already fully mitigated (c2496 patched all three exposed callers
to degrade honestly) and not due for its post-deadline re-check for 11 more days. No new
Actor built: with 25 public Actors / 47 users / 783 runs30d / $0 booked, the owner's own c2700
observation that discovery (not Actor quality) may be the binding constraint argues against
adding fleet surface on spec, and nothing in `apify-admin store` was checked today that would
license a confident differentiation case within this cycle's time budget -- left as an open
question for a future cycle with more runway, not a decision.

**Inbox: zero new mail, same 10 known triaged IDs** (`inbox list 10` unchanged from every
prior cycle's list, including both owner-originated threads `2b237f1b`/`01852eaa`, both long
since fully resolved and tracked in the queue). `bin/revenue` $0 booked, 25 Actors, 47 users,
783 runs30d, `ext_bad30d` still exactly 4 (no new entry). `bin/apify-spend` $6.5563/$85
(85.1% elapsed, projection $7.70). Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all
active; `/`, `/pricing`, `/tools` all 200.

**All four standing watches re-verified live, all unchanged, nothing fired.**
`eu-ted-tenders-scraper` `totalUsers7/30/90Days` still 1/1/1, `bookmarkCount` still 0,
`stats.publicActorRunStats30Days.TOTAL` still **45**. `bin/dmarc-report list` still the same
2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail. `bold.org/scholarships/` still
**429**. `bin/traffic` BUYER-INTENT funnel flat: tools 38n/37v (engaged 10/9), pricing 5/5
(engaged 4/4), checkout 2/2 (engaged 0/0) -- far below the >100/day Polar gate, so **no owner
email**, correctly. The stale `shopify-products-scraper` row-floor flag in `state/health.json`
is still correctly unresolved -- today is still 2026-11-04 and the nightly `actor-health`
cron that refreshes it fires 2026-11-05 03:30 UTC; next cycle after that should confirm it
cleared.

$0 spent, $0 revenue change, no owner email, spend well inside budget.

---

Updated: 2026-11-04 ~09:05 UTC by cycle 2704 (claude-opus-5). NORMAL slot (2704 % 3 == 1,
recomputed fresh -- 901*3=2703, so 2703 was correctly QUALITY and **2706 is the next QUALITY
slot**). **Ran the one due fleet check and then closed the c2696 crawler-shape re-read -- which
required noticing that the obvious way to execute it proves nothing.**

`check-disclosure` DUE and RAN CLEAN: 88 site blog posts + 28 dev.to articles checked, **0
missing disclosures** (next due c2752).

**CLOSED the c2696 follow-up (re-read the 92%-one-path / 90%-no-referrer crawler shape on a
later cycle before quoting the inflation figure).** Executing it literally would have been
self-deceiving: **at 48 cycles/day a 7-day window moves ~0.3% per cycle**, so re-running the
ratios 8 cycles (~4h) after c2696 queries ~98% the same rows -- and indeed it returned 138
vids / 127 one-path / **92.0%**, identical to the decimal, which reads as strong confirmation
but is only the measurement agreeing with itself. Got a real second sample by shifting the
window BACKWARDS instead of waiting a week (`ts > now-14d AND ts <= now-7d`, VERIFIED/NOTBOT/
PV_SWEEPER/PV_UA_ROTATOR predicates copied verbatim from `bin/traffic`): **118 verified vids,
117 one-path (99.2%), 120 verified views, 115 referrer-less (95.8%), 5 search referrers (4.2%),
30 distinct UAs / 118 vids.** The crawler shape **HOLDS on two disjoint windows and is more
extreme a week earlier** -- no drift toward parity, so there is no real human-traffic growth
signal hiding under it and the residential-proxy-crawl reading stands.
**Correction only the second window could expose: the "~4.3x inflation" figure is NOT a
constant** -- the same ENGAGED test on the prior week took tools 29n/29v -> 3n/3v (**~9.7x**).
A ratio measured on one window is a property of that window's crawler mix, not of the detector.
Edited `bin/traffic`'s c2696 comment block AND its printed funnel header to say "92-99%
one-path / 89-96% referrer-less (two independent windows, c2696+c2704), inflation 4-10x" in
place of three false constants. `bash -n` clean; `bin/traffic` re-run verified funnel output
unchanged. Detector logic deliberately untouched, per the item's own instruction. Lesson in
LEARNINGS c2704; generalised into a standing method in queue.md (a "re-read later" follow-up
must name a NON-OVERLAPPING window, and the data for one is usually already on disk).

Preflight otherwise clean: `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types
(5 types CLOSED, never a backlog); `inbox list 10` the same 10 known triaged IDs, zero new
mail; `bin/revenue` $0 booked, 25 Actors, 47 users, 783 runs30d, `ext_bad30d` still exactly 4;
`bin/apify-spend` $6.5555/$85 (85.1% elapsed, projection $7.70); services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active and `/`, `/pricing`, `/tools` all 200.
`state/health.json` snapshot `ts` re-read fresh = **1793775660 = 2026-11-04 07:01 UTC**, i.e.
still c2700's run, so the stale pre-fix `shopify-products-scraper` row-floor flag is still
correctly unresolved -- the nightly `actor-health` cron (03:30 UTC) has not fired since the
fix. It fires **2026-11-05 03:30 UTC**; that is ~33 cycles away, so **stop re-checking it every
cycle** -- the next cycle that runs after 03:30 UTC tomorrow should confirm it cleared.

**All four standing watches re-verified live, all unchanged, nothing fired.**
`eu-ted-tenders-scraper` `totalUsers7/30/90Days` still 1/1/1, `stats.bookmarkCount` still 0,
`stats.publicActorRunStats30Days.TOTAL` still **45** (flat for a 6th cycle; note the fields
live under `stats`, not top-level -- a top-level read returns `None` and must not be reported
as a change). `bin/dmarc-report list` still the same 2 reports (`af5d9f7d`/`202905fb`), both
1-source/0-fail. `bold.org/scholarships/` still **429**. `bin/traffic` BUYER-INTENT funnel
flat: tools 37n/36v (engaged 9/8), pricing 4/4 (engaged 3/3), checkout 2/2 (engaged 0/0) --
far below the >100/day Polar gate, so **no owner email**, correctly.

$0 spent, $0 revenue change, no owner email, spend well inside budget.

---

Updated: 2026-11-04 ~08:33 UTC by cycle 2703 (claude-sonnet-5). QUALITY/GROWTH slot
(2703 % 3 == 0, recomputed fresh). **Executed the doc-trim cadence item's designated work:
both STATUS.md and queue.md were TRIM SOON, both trimmed in this slot per the cadence's own
rule 2.** `state/STATUS.md` 103.2KB/1245 lines -> 15.9KB/220 lines (`bin/_trim2703s.py`,
kept cycles 2698-2702, archived 2671-2697). `tasks/queue.md` 80.2KB/750 lines -> 59.6KB/590
lines (`bin/_trim2703q.py`, kept all 33 open items + newest DONE c2702, archived 9 older
DONE blocks) -- margin still came out thin (~13KB) after the DONE-only cut since open items
now dominate the file's mass, so the doc-trim cadence item's own "newest execution only, do
not stack narratives" rule was applied to itself: its stale c2676 execution narrative was
replaced with this cycle's record instead of being prepended, recovering real margin without
touching any other open item. Hazard grep run FIRST on both archive-bound ranges per cadence
rule 1 (STATUS.md 1025 lines/16 hits, queue.md 151 lines/3 hits), every hit a citation of the
c2524 rule (homed in CLAUDE.md) or a cross-reference pointing at the cadence item itself, none
uniquely homed in the archived range -- CLEAN on both. Backed up all four live+archive docs to
`/tmp/c2703_*.bak` before either script ran. **Guards all passed:** both scripts' own asserts
(exact block/line counts, byte-for-byte partition reconstruction, archive-prefix preservation,
no open item in the archive set); independently re-verified losslessness by rebuilding each
original's non-blank line set and testing membership in live+archive -- 0 missing on both;
`check-status-blocks-kept` OK (0 destroyed); `check-status-continuity` NONE MISSING on the
retained 2698-2702 window; `check-doc-size` now reads **OK on all three live docs**
(STATUS.md ~42c headroom, queue.md ~26c headroom, LEARNINGS.md untouched, ~104c headroom).
**Flag for the next QUALITY slot (2706): queue.md's margin is still thin (~13KB vs the ~15KB
guide, projected 187KB at the checker's next look) because 33 open items now carry nearly all
of the file's mass and no DONE-only cut can touch them -- re-run `check-doc-size` fresh and, if
still thin, look for more open items whose detail duplicates a fuller home elsewhere (same
method as c2694's two compressions) rather than banking on volume alone.**

Preflight otherwise clean: `checks-due --all` NONE DUE (soonest `check-disclosure` in 1c,
cycle 2704); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox list 10`
the same 10 known triaged IDs, zero new mail; `bin/revenue` $0 booked, 25 Actors, 47 users,
783 runs30d, `ext_bad30d` still exactly 4; `bin/apify-spend` $6.5551/$85 (85.0% elapsed,
projection $7.71); services active and `/`, `/pricing`, `/tools` all 200.
`state/health.json` still carries the stale pre-fix `shopify-products-scraper` row-floor
flag (snapshot `ts` 07:01 UTC, pre-dates the nightly `actor-health` cron at 03:30 UTC) --
still correctly unresolved since it is still 2026-11-04 08:30 UTC and the cron fires tonight
at 2026-11-05 03:30 UTC. **Check again next cycle, after that run has actually fired.**

**All four standing watches re-verified live, all unchanged, nothing fired.** `eu-ted-tenders-
scraper` `totalUsers7/30/90Days` still 1/1/1, `bookmarkCount` still 0,
`publicActorRunStats30Days.TOTAL` still **45** (flat). `bin/dmarc-report list` still the same
2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail. `bold.org/scholarships/` still
**429**. `bin/traffic` BUYER-INTENT funnel essentially flat: tools 37n/36v (engaged 9/8),
pricing 4/4 (engaged 3/3), checkout 2/2 (engaged 0/0) -- nowhere near the >100/day Polar gate,
so no owner email.

$0 spent, $0 revenue change, no owner email, spend well inside budget.

---

Updated: 2026-11-04 ~08:10 UTC by cycle 2702 (claude-sonnet-5). NORMAL slot (2702 % 3 == 2,
recomputed fresh -- 2700 divisible by 3, so 2701/2702/2703 are 1/2/0; 2703 is QUALITY next).
**The due item this cycle was `check-source-endpoints`, and it found a real DEVIATION --
verified it as a transient blip, not an outage, before closing it out.** Probe of 50 unique
upstream hosts returned 1 deviation: `rss.marketingtools.apple.com` (apple-podcasts-scraper)
`ok -> error/ReadTimeout`. Did not take that at face value -- two immediate manual retries both
returned `200` in under a second, and `bin/actor-health --only apple-podcasts-scraper` confirmed
`ok: True, items: 5` with correct sample keys. One-off network timeout on our probe, not a real
upstream change. Recorded via `checks-due --ran check-source-endpoints` (next due cycle 2726).

Preflight otherwise clean: `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types;
`inbox list 10` the same 10 known triaged IDs, zero new mail; `bin/revenue` $0 booked, 25
Actors, 47 users, 783 runs30d, `ext_bad30d` still exactly 4 (no new entry); `bin/apify-spend`
$6.5545/$85 (84.9% elapsed, projection $7.72); services active and `/`, `/pricing`, `/tools`
all 200. `state/health.json` still carries the stale pre-fix `shopify-products-scraper`
row-floor flag -- correctly not yet cleared, since the nightly `actor-health` cron (03:30 UTC)
has not run since c2700's fix (today is still 2026-11-04 08:10 UTC; the run fires tonight,
2026-11-05 03:30 UTC) -- check again next cycle.

**All four standing watches re-verified live, all unchanged, nothing fired.** `eu-ted-tenders-
scraper` `totalUsers7/30/90Days` still 1/1/1, `bookmarkCount` still absent, `publicActorRunStats
30Days.TOTAL` still **45**. `bin/dmarc-report list` still the same 2 reports (`af5d9f7d`/
`202905fb`), both 1-source/0-fail. `bold.org/scholarships/` still **429**. `bin/traffic`
BUYER-INTENT funnel essentially flat: tools 37n/36v (engaged 9/8), pricing 4/4 (engaged 3/3),
checkout 2/2 (engaged 0/0) -- nowhere near the >100/day Polar gate, so no owner email.

`check-doc-size`/`check-row-floor`/`check-upstream-warnings` all still ~22c out, not due.
c2380 growth-sweep item is 1 cycle since its c2701 re-grep, nowhere near its ~25-30c window.
$0 spent, $0 revenue change, no owner email, spend well inside budget.

---

Updated: 2026-11-04 ~07:35 UTC by cycle 2701 (claude-sonnet-5). NORMAL slot (2701 % 3 == 1,
recomputed fresh -- 2700 is divisible by 3, confirming it was correctly the QUALITY slot and
2703 is next). Preflight entirely clean: `checks-due --all`/`audit-due --all` both NONE DUE
(soonest `check-source-endpoints` in 1c); `inbox list 10` the same 10 known triaged IDs, zero
new mail; `bin/revenue` $0 booked, 25 Actors, 47 users, 783 runs30d; `bin/apify-spend`
$6.5537/$85 (84.9% elapsed, projection $7.72); `check-doc-size` **TRIM SOON on STATUS.md
(98.2KB/1174 lines, ~23c headroom) and queue.md (75.0KB/690 lines, ~24c headroom) but correctly
deferred to the next QUALITY slot (2703) per the doc-trim cadence's own rule** (trim only in a
QUALITY slot); LEARNINGS OK (5914 lines, ~104c headroom); services active and `/`, `/pricing`,
`/tools` all 200.

**`state/health.json` still carries the stale pre-fix `shopify-products-scraper` row-floor flag
from c2700's fix-verification run (snapshot timestamp 07:01 UTC), which pre-dates the nightly
`actor-health` cron (03:30 UTC daily).** Per c2700's own follow-up, did NOT spend a full fleet
health run to force an early refresh -- expected to self-clear on tonight's 2026-11-05 03:30
UTC run; next cycle should check whether it cleared.

**All four standing watches re-verified live, all unchanged, nothing fired.** `eu-ted-tenders-
scraper` `totalUsers7/30/90Days` still 1/1/1, `bookmarkCount` still 0,
`publicActorRunStats30Days.TOTAL` still **45** -- no traction. `bin/dmarc-report list` still
the same 2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail. `bold.org/scholarships/`
still **429**. `bin/traffic` BUYER-INTENT funnel essentially flat: tools 37n/36v (engaged 9/8),
pricing 4/4 (engaged 3/3), checkout 2/2 (engaged 0/0) -- ~1.3 engaged visits/day against the
>100/day Polar gate, so **no owner email**.

**Re-ran the c2380 growth-sweep candidate re-grep fresh (20 cycles since c2681, inside the
guided 20-25c window) -- a 4th consecutive 0-candidate read.** Same method found 8 files with
a growing-listing-count shape (`ats-jobs-scraper`, `clinicaltrials-scraper`,
`fec-campaign-finance-scraper`, `federal-register-scraper`, `remote-jobs-scraper`,
`trademark-search-scraper`, `uk-find-a-tender-scraper`, `us-federal-awards-scraper`;
`sam-gov-opportunities-scraper` dropped off this time -- its only arrow-hit is an unrelated
set-aside-code count, not a matched-listing count), every README mtime touched 0-5 days ago by
an unrelated cadence, none sitting stale behind a rising live count. Widened the next-retry
guidance to ~25-30 cycles in queue.md given four straight empty reads.

$0 spent, $0 revenue change, no owner email, spend well inside budget.

---

Updated: 2026-11-04 ~07:15 UTC by cycle 2700 (claude-opus-5). **QUALITY/GROWTH slot --
`2700 % 3 == 0` verified fresh (900*3=2700), confirming c2699's correction of c2698. This was a
real build/fix cycle, not a watch-only one.**

**SHIPPED: fixed a live, buyer-facing, revenue-relevant bug in `shopify-products-scraper` that
was zeroing every default run.** `actor-health` opened a FIX FAILED ACTORS task (SUCCEEDED/201
but `items: 0`). The Actor code and the upstream source were both FINE -- the bug was **our own
`proxyConfiguration` default**. Measured decisively on the same build minutes apart:
`allbirds.com` and `deathwishcoffee.com` both **403 through Apify's shared DATACENTER proxy pool**
and both **200 with the proxy off**; `gymshark.com` 403s either way (bot-protected at the store
level). So the shipped default `{useApifyProxy: true}` was converting WORKING stores into
0-product runs for every Store user who just clicked Start. Fixed in all THREE places the default
is encoded -- `.actor/input_schema.json` `default`, `src/main.js`'s own
`?? { useApifyProxy: true }` fallback (the schema default alone is NOT enough: API callers who omit
the field hit the code path), and the README input table plus a new troubleshooting FAQ entry.
One batched push -> build **0.1.110**. **Verified end-to-end:** `bin/actor-health --only
shopify-products-scraper` -> `ok: True, items: 10` (10/10, at cap) from the UNCHANGED
`test_input.json`, i.e. the exact nightly path that was failing; `bin/check-charges` 25/25 clean,
0 missing `Actor.charge()`, 0 event-name drift.

**Deliberately did NOT generalize the fix, on measurement.** Audited every Actor with a
`proxyConfiguration` default: `ats-jobs-scraper` and `google-news-scraper` remain
`{useApifyProxy: true}`. `google-news-scraper` was *also* flagged by `check-row-floor` (declined
8->6 rows) and looked like the same mechanism -- but measured both ways it returns **8/8
identically**, so that flag is news-volume variance and its proxy-on default is harmless. The
datacenter block is a **Shopify-storefront** behavior, not an Apify-wide proxy failure; one cheap
measurement separated a real bug from a coincidence that would have cost two needless pushes.
A near-miss worth remembering: the FIRST probe of six candidate stores showed `deathwishcoffee`
returning products, which read as "allbirds specifically is blocked, just swap the example store"
-- a store swap would have greened the health test and left every customer's default broken.
Re-running `deathwishcoffee` alone returned **0**: the pool is blocked per-IP, so one green run
proves nothing. See LEARNINGS c2700.

**Preflight was otherwise clean.** Both due fleet checks RAN and PASSED (not deferred):
`check-doc-size` OK on all three live docs (STATUS 93.9KB/1117 lines ~24c headroom, queue.md
71.6KB/651 lines ~24c, LEARNINGS 5878 lines ~106c) -> next due c2724; `check-link-equity` 88
posts / 24 live Actors with **0 TRUE orphans** (min 3 `remote-jobs-scraper`, median 7, max 14
`ats-jobs-scraper`; 1 contextual orphan `bold-org-nextjs-rsc-scholarship-data`, whose Actor
`scholarship-scraper` is PAUSED/429 anyway) -> next due c3036. `audit-due --all` FLEET ROTATIONS
NONE DUE across all 16 types. `inbox list 10` the same 10 known triaged IDs, zero new mail.
`bin/revenue` $0 booked, 25 Actors, 48 users, 783 runs30d. `bin/apify-spend` $6.5206/$85 (84.8%
elapsed, projection $7.69) -- this cycle's probe runs plus one push are inside that figure.
Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools` all 200.

**All four standing watches re-verified live, all unchanged, nothing fired.** (1)
`eu-ted-tenders-scraper` fresh read: `totalUsers7/30/90Days` still exactly 1/1/1, `bookmarkCount`
still 0, `publicActorRunStats30Days.TOTAL` still **45** (flat for a 5th cycle since c2696's
42->45) -- no traction. (2) `bin/dmarc-report list` still exactly the same 2 reports
(`af5d9f7d`/`202905fb`), both 1-source/0-fail. (3) `bold.org/scholarships/` still **429** --
`scholarship-scraper`'s held fix stays unpushed per c2312. (4) `bin/traffic` BUYER-INTENT funnel
essentially flat: tools 38n/37v (engaged 9/8), pricing 4/4 (engaged 3/3), checkout 2/2 (engaged
0/0) -- ~1.3 engaged visits/day against the >100/day Polar gate, so **no owner email**, correctly.

$0 revenue change, no owner email, spend well inside budget.

---

Updated: 2026-11-04 ~06:30 UTC by cycle 2699 (claude-sonnet-5). NORMAL slot -- **corrected
2698's header: `2699 % 3 == 2` (899*3=2697, +2), not `== 0`; c2698 mislabeled next cycle as
QUALITY/GROWTH. QUALITY slots are 2694/2697/2700 (every 3rd starting at 2694), so 2699 is
NORMAL and 2700 is the next QUALITY slot.** Per the standing "recompute cycle % 3 fresh, do
not trust the previous header" rule -- this is exactly the failure mode that rule exists to
catch. Preflight entirely clean: `checks-due --all` NONE DUE (soonest `check-doc-size` in 1c,
cycle 2700); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox list 10`
the same 10 known triaged IDs, zero new mail; `bin/revenue` $0 booked, 25 Actors, 48 users,
783 runs30d (users ticked 49->48, within the tool's known noise band -- `totalUsers` is a
windowed/active count, not a trend); `bin/apify-spend` $6.5025/$85 (84.7% elapsed, projection
$7.67); `bin/check-doc-size` OK on all three live docs (STATUS 90.6KB/1070 lines ~25c
headroom, queue.md 70.0KB/631 lines ~24c headroom, LEARNINGS 5878 lines ~106c headroom);
`bin/actor-health` full fleet green (`scholarship-scraper` still PAUSED/429, held fix
unpushed per c2312); `bin/check-charges` 25/25 clean, 0 missing `Actor.charge()`, 0
event-name drift; services active and `/`, `/pricing`, `/tools` all 200.

**Re-verified all four standing watches live, all unchanged, nothing fired.** (1)
`eu-ted-tenders-scraper` fresh `GET /v2/acts/5LxaohNcO1zA86cEp`: `totalUsers7/30/90Days`
still exactly 1/1/1, `bookmarkCount` still 0 (field now reads `None`/absent rather than `0`
in the raw payload -- same meaning, not a new signal), `publicActorRunStats30Days.TOTAL`
still **45** (flat for a 4th cycle since c2696's 42->45 move) -- no new traction. (2)
`bin/dmarc-report list` still exactly the same 2 reports (`af5d9f7d`/`202905fb`), both
1-source/0-fail. (3) `bold.org/scholarships/` still **429** -- `scholarship-scraper`'s held
c2312 fix stays unpushed. (4) `bin/traffic` BUYER-INTENT funnel essentially flat vs c2696-98:
`tools` 39n/38v (engaged 9/8), `pricing` 4/4 (engaged 3/3), `checkout` 2/2 (engaged 0/0) --
nowhere near the >100/day Polar gate. The c2696 follow-up (re-read the 92%/90%
crawler-shape ratios on a later *non-adjacent* cycle) stays deferred -- 2699 is still
adjacent to 2698.

**Re-diffed the `ext_bad30d` tripwire (c2336) via `bin/revenue`:** still exactly 4 (matches
the known lifetime set: `steam-reviews-scraper` FAILED 1, `court-records-scraper` TIMED-OUT
1, `remote-jobs-scraper` TIMED-OUT 1, `nih-reporter-scraper` FAILED 1), no new entry.

**Scanned all open (`- [ ]`) queue items** -- all remain correctly gated behind triggers
that haven't fired (c2478 Apify Store deadline 2026-11-15, now 11 days out, not yet due for
re-check; c2380 growth-sweep candidate list at 18 cycles since its c2681 re-grep, still
under the ~20-25c wait guidance; c2692's grants-gov-scraper non-cut decision stands, no new
undercutter). Nothing licensed a code change, so per the standing c2524 rule none was
manufactured.

$0 spent, $0 revenue change, no owner email. STATUS.md and queue.md updated. **Next cycle
(2700, QUALITY/GROWTH slot, verify `2700 % 3 == 0` fresh before trusting this):**
`check-doc-size` comes due for its periodic re-check; re-verify the four standing watches;
c2380 growth-sweep item will be at 19 cycles since c2681, still just under the wait window.

---

Updated: 2026-11-04 ~06:04 UTC by cycle 2698 (claude-sonnet-5). NORMAL slot (2698 % 3 == 1,
recomputed fresh). Preflight entirely clean: `checks-due --all` NONE DUE (soonest `check-doc-size`
in 2c, cycle 2700); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox list 10`
the same 10 known triaged IDs, zero new mail; `bin/revenue` $0 booked, 25 Actors, 49 users, 783
runs30d (runs30d down slightly from 787, within the tool's known noise band, `bkmk`/`rev` still 0);
`bin/apify-spend` $6.5017/$85 (84.7% elapsed, projection $7.68); `check-doc-size` OK on all three
live docs (STATUS 87.2KB/1025 lines ~26c headroom, queue.md 68.2KB/608 lines ~25c headroom,
LEARNINGS 5878 lines ~106c headroom); services active and `/`, `/pricing`, `/tools` all 200.

**Re-verified all four standing watches live, all unchanged, nothing fired.** (1)
`eu-ted-tenders-scraper` fresh `GET /v2/acts/5LxaohNcO1zA86cEp`: `totalUsers7/30/90Days` still
exactly 1/1/1, `bookmarkCount` still 0, `publicActorRunStats30Days.TOTAL` still **45** (flat for a
3rd cycle since c2696's 42->45 move) -- no new traction. (2) `bin/dmarc-report list` still exactly
the same 2 reports (`af5d9f7d`/`202905fb`), both 1-source/0-fail. (3) `bold.org/scholarships/`
still **429** -- `scholarship-scraper`'s held c2312 fix stays unpushed. (4) `bin/traffic`
BUYER-INTENT funnel byte-identical to c2696/c2697: `tools` 39n/38v (engaged 9/8), `pricing` 4/4
(engaged 3/3), `checkout` 2/2 (engaged 0/0) -- flat, nowhere near the >100/day Polar gate. The
c2696 follow-up (re-read the 92%/90% crawler-shape ratios on a later *non-adjacent* cycle) stays
deferred -- 2698 is adjacent to 2697, still doesn't satisfy it.

**Re-diffed the `ext_bad30d` tripwire (c2336) fresh from `state/revenue_history.json`:** still
exactly the same 4 lifetime events (`steam-reviews-scraper` FAILED 1, `court-records-scraper`
TIMED-OUT 1, `remote-jobs-scraper` TIMED-OUT 1, `nih-reporter-scraper` FAILED 1), all previously
triaged, no new entry.

**Read both owner-originated inbox threads in full rather than trusting the cached verdict, since
they're the only two real human emails in the 10 known IDs.** `2b237f1b` is the owner's reply with
a CourtListener API token for `court-records-scraper` -- confirmed it has been live in
`secrets/env` as `CL_API_TOKEN` since 2026-10-28, wired into `main.js:514`'s `Authorization: Token`
header, and the whole episode (including a false "not configured" claim that recurred 94 cycles
later from grepping the wrong key name) is fully resolved per LEARNINGS c5251-5253 -- nothing
outstanding. `01852eaa` is the forwarded Apify `/v2/store` 2026-11-15 ranking-change notice --
already the subject of the c2478/c2496 queue item (all three exposed callers patched to degrade
honestly instead of lying, a self-test locked in, the upside re-measure plan written down for
after the deadline). Both threads are closed; no reply or action owed.

**Nothing fleet-wide, in the inbox, or in any re-checked gate licensed a code change, so per the
standing c2524 rule none was manufactured.** $0 spent, $0 revenue change, no owner email. **Next
cycle (2699, QUALITY/GROWTH slot, 2699 % 3 == 0):** recompute `checks-due`/`audit-due` fresh
(`check-doc-size` due cycle 2700, 1c out by then -- likely due); re-verify the four standing
watches; the c2380 growth-sweep item will be at 17-18 cycles since its c2681 re-grep, still under
the ~20-25c wait guidance.

---

