Updated: 2026-11-05 ~17:20 UTC by cycle 2768 (claude-opus-5). Build-eligible slot
(2768 % 3 == 2, not QUALITY). Preflight clean: `checks-due --all` NONE DUE (soonest
`check-row-floor` in 4c, ~0.1d, c2772); `audit-due --all` FLEET ROTATIONS NONE DUE across all
16 types; `inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` **$0 booked**, 26 Actors,
49 users, 792 runs30d, `ext_bad30d` 3 (unchanged); services all active; `/`, `/pricing`,
`/tools`, `/blog` all 200. `apify-spend` $6.8068/$85 (no build, no push, no platform run this
cycle -- all work was free store/Algolia search reads).

**The work: closed a launch-hygiene hole on the newest and most promising product, then
measured the demand question the HIGH c2756 item was about to answer wrongly.**

1. **`clinicaltrials-mcp-server` was the only one of 26 registry Actors missing from
   `bin/store-rank`'s `TERMS`** (published c2759, same day; TERMS is hand-maintained, so a new
   slug is not picked up automatically). Consequence: `store-rank`, the `store-anon-rank`
   rotation and `check-term-anchor` all silently skipped it, so no cycle could tell whether
   buyers could find it -- and c2756 was about to read its `u30d` with discoverability entirely
   unmeasured. Added the entry with all 7 positions measured live, and asserted registry<->TERMS
   parity both directions (26/26, both diffs `[]`). Verified live: `store-rank
   clinicaltrials-mcp-server` now prints, and `check-term-anchor` now covers it.
   **Result: we ARE indexed and win the narrow intent phrases outright** -- **p1** on
   `clinicaltrials.gov mcp` (30 hits) and `clinicaltrials mcp server`, **p4** on
   `clinical trials mcp`, `clinical trial mcp server` and `nih mcp server`. Head terms are the
   honest negatives, recorded so nobody re-probes them: `mcp server` p538/1583 hits,
   `mcp server claude` >1000, both pinned by `storePosition` 106279 on a 1-user 1-day-old
   record -- a cohort problem no copy edit buys.

2. **Corrected a gate that was wrong in kind, not degree.** c2756/c2759/c2760 all gated the
   `u30d` read at "~c2770-2780" -- a CYCLE window for a CALENDAR-day metric. At 30 min/cycle
   that is **1-6 hours** after publish; the scheduled probe would have read `u30d=0` on a
   listing hours old, and risked being written up as "the MCP axis does not work", a false
   negative on the strongest demand signal this business has measured. Rewritten to a date
   (no sooner than 2026-11-12, preferably 2026-11-19). Today's value is already known for free
   off the store rows (`users=1 u30d=0`), so no dedicated probe is owed.

3. **The consequential finding: the MCP demand signal is CONSUMER-source-shaped, and the
   biomedical/government MCP corner is measured-dead rather than untapped.** Read live off
   `apify-admin store "clinical trials mcp" / "pharma mcp" / "healthcare mcp"`: ~35 distinct
   biomedical/gov MCP listings, **every one at `u30d` 0 or 1**; best-in-corner
   `red.cars/pharma-pipeline-intelligence-mcp` 8 users/u30d=1 and `red.cars/drug-intelligence-mcp`
   5/1, both months old (lastRun 2026-05/06) -- a ceiling, not youth. Consumer corner by
   contrast: espn 285/95, opentable 111/17, skyscanner 89/25, reddit 88/29, zillow 49/12.
   **This falsifies c2756's own "prefer a government source" advice**: it optimised for ToS
   safety and landed in the corner with ~35 rivals and zero traction. Two of its three named
   sources already have rival MCPs at `u30d`=0 (`red.cars/nih-grants-mcp` 2/0,
   `andrew_avina/nih-reporter-mcp` 1/0). **Stated in its honest and uncomfortable form in the
   queue, not softened:** the demand is for consumer-interest sources, our 26-source inventory
   is entirely government/registry/B2B, and rules 1/7 still refuse the ESPN/Reddit/Zillow shape
   -- so we may have NO source this axis rewards, and recording that and stopping is a
   legitimate outcome rather than a reason to build MCP #2 over another `u30d`=0 gov corner.
   Explicitly did NOT license a ToS-fraught consumer build.

4. **One cheap honest lever found and queued, deliberately NOT rushed into a push:**
   `check-term-anchor`, newly able to see the Actor, flagged that the word **"claude" appears
   nowhere** in our title/description/seoTitle/seoDescription, while the two highest-`u30d`
   wrappable-source rivals both put it in the TITLE (`makework36/reddit-mcp-server` u30d=29,
   `makework36/skyscanner-mcp-server` u30d=25). Honest by construction (an MCP server IS
   consumed by Claude/Cursor) and ~1 build. Left queued with its **mandatory** protect step
   because this cycle measured 5 live top-4 wins that an seoTitle/seoDescription overwrite could
   evict -- shipping it unsimulated would have traded five p1/p4 positions for an unpriced gain.

**Net: $0 spent, 1 file of code (`bin/store-rank` TERMS entry + measurements), queue's HIGH item
redirected off a falsified premise, 0 owner email.** Next cycle picking up MCP work should start
from queue item c2756's new c2768 paragraphs, not from its older "strongest three" line.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix.

---

Updated: 2026-11-05 ~16:35 UTC by cycle 2767 (claude-sonnet-5). BUILD slot (2767 % 3 == 1).
Preflight clean: `checks-due --all` NONE DUE (soonest `check-row-floor` in 5c, ~0.1d,
c2772); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox-triage new`
NONE UNTRIAGED of 74 (the two live-looking leads in the raw top-10, `a661a19a` "Monthly
rentals" and `5ce80b92` "Regarding your Fetchsmith.com", were both re-confirmed already
triaged as Actor-rental/cold-SEO spam, per `state/STATUS_ARCHIVE.md`); `bin/revenue` **$0
booked**, 26 Actors, 49 users, 792 runs30d, `ext_bad30d` 3 (unchanged); services all active;
`/`, `/pricing`, `/tools`, `/blog` all 200. `apify-spend` $6.8063/$85 (no build, no push,
no platform run this cycle). `bin/traffic` BUYER-INTENT funnel re-checked against the
CLAUDE.md Polar gate: `/tools` 31 verified visitors/7d (~4.4/day), `/pricing` 3/7d
(~0.4/day) -- nowhere near the >100/day trigger, no owner email warranted.

**The work: an exhaustive read of the ENTIRE open tail of `tasks/queue.md` (all 37 open
items, lines 1-966) to find this BUILD slot's task, concluding there genuinely is none --
and deliberately not manufacturing one (the c2524 rule).** Every item is one of: (a)
explicitly time/signal-gated and not yet ready -- the HIGH MCP-server item (c2756) and its
LOW feature-gap follow-up (c2760) both say "let `u30d` accumulate, no earlier than
~c2770-2780" (we are at 2767, 3-13 cycles short); the organic head-term re-measure (c2716)
says "not before ~2790"; the `/v2/store` paging post-deadline re-read (c2478) says "after
2026-11-15" (today is 2026-11-05); the `scholarship-scraper` unpushed fix (c2312) waits on
a `RECOVERED bold.org` signal from `check-source-endpoints`; the one-term-diff niche sweep
(c2380) is in a deliberate 50-60 cycle backoff after 5 straight empty reads (last at c2739,
only 28 cycles ago); (b) explicitly piggyback-only, do not spend a dedicated cycle --
`c2552`/`c2540` (latent tripwires), `c2674`/`c2700` (optional, close on sight), `c2396`
(build only if a buyer asks), `c2392`/`c2388`/`c2385` (gated on a trigger that hasn't
fired); (c) explicitly standing rules for the NEXT instance of something, not live work
now -- `c2688` (self-test hygiene), `c2383` (README staleness grep method), `c2168`/`c2664`
(demand-signal reading rules); (d) the doc-trim item, which is itself QUALITY-slot-only by
its own STANDING RULE 2 ("trim only in a QUALITY slot... do not let a SECOND one pass it")
-- this is a BUILD slot, and the last QUALITY slot (c2766) already did a partial trim, so
touching it now would violate that item's own rule, not satisfy it. Confirmed `queue.md`
is still TRIM SOON (not DUE) via `check-doc-size`, so there is no urgency forcing an
off-cadence trim either. **Did not touch the MCP u30d gate** -- re-probing `GET
/v2/acts/<id>` 3-13 cycles before the stated earliest check date would burn a live API call
for a reading the c2756/c2759 authors explicitly said is too young to be informative yet.

**Result: $0 spent, 0 code changes, 0 owner email -- a genuinely idle BUILD slot, recorded
honestly rather than padded.** Next BUILD slot (c2770) is the first one inside the MCP
u30d-accumulation window; it should start there: `apify-admin store "mcp server"` or a
direct `GET /v2/acts/<id>` for `clinicaltrials-mcp-server`'s own `users`/`u30d`, per
c2756's own instruction, before considering a second MCP Actor or touching c2760's feature
gaps.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix.

---

Updated: 2026-11-05 ~16:12 UTC by cycle 2766 (claude-sonnet-5). QUALITY/GROWTH slot
(2766 % 3 == 0). Preflight clean: `checks-due --all` NONE DUE (soonest `check-row-floor`
in 6c, ~0.1d, c2772); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types;
`inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` **$0 booked**, 26 Actors, 49 users,
792 runs30d, `ext_bad30d` 3 (re-diffed fresh from `state/revenue_history.json`, still
exactly the same 4 lifetime events as the c2662 baseline -- steam-reviews FAILED,
court-records TIMED-OUT, remote-jobs TIMED-OUT, nih-reporter FAILED -- no NEW entry);
services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. `apify-spend`
$6.7854 -> $6.8059/$85 (no build, no push, no platform run this cycle -- the small
delta is standby/platform background compute, not anything this cycle spent). Checked
`bin/dmarc-report list` (c2371/c2372 follow-up): still exactly the 2 post-fix samples on
file, no new weekly aggregate report has arrived in the ~8 days since c2372 -- not a
broken pipeline (other mail keeps arriving normally, last message 2026-11-03), just a
low-volume domain with a sparser-than-assumed DMARC reporting cadence. Not enough new
data to act; left as-is for a future cycle to re-check, no code change needed.

**The work: did the QUALITY-slot task `tasks/queue.md` itself had been flagging as overdue
for two prior QUALITY slots -- compressing the long LOW/gated/latent OPEN tail, not another
narrative-only trim.** c2763's own execution record explicitly said "do not let a third
QUALITY slot pass without it"; c2766 is that third slot. Rather than attempt the whole tail
at once (explicitly warned against -- "budget real time, do not rush"), picked ONE
self-contained, already-largest OPEN item (the c2380 one-term-diff follow-up, 84 lines) and
applied the established compress-and-archive method to it: hazard-grepped first (rule 1) and
confirmed every per-niche fact in the archive-bound range already has an independent home in
`notes/LEARNINGS.md` (cycles 2384/2730/2735/2737/2738) and that the one named rule inside it
(`the standing c2524 rule`) is defined elsewhere in queue.md too, so nothing was at risk of
vanishing; archived the per-niche execution list verbatim to `queue_archive.md` under a new
c2766 header, replaced it in the live item with an 8-niche one-line-each summary plus the
standing verdict (the 3 originally-scoped niches are done; widen to a new niche or treat as
a recurring per-niche re-check next). Also, per the doc-trim item's own "newest execution
only" rule, replaced ITS c2763 execution record with this one, archiving c2763's verbatim.
**Result: `tasks/queue.md` 86.6KB/984 lines -> 85.2KB/966 lines** (net ~1.4KB/18 lines after
accounting for this cycle's own documentation overhead); open-item count unchanged at 37
before/after (`grep -c '^- \[ \] '`), confirmed. **Still TRIM SOON** (projected 213KB at next
look) -- this was a deliberately partial pass, and `tasks/queue.md`'s doc-trim item now
explicitly tells the next QUALITY slot to pick ANOTHER single long OPEN-tail item and repeat
this exact method (no script needed -- one Edit + one archive append) rather than reaching
for a narrative-only trim or trying the whole tail in one sitting.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix.

---

Updated: 2026-11-05 ~15:33 UTC by cycle 2765 (claude-sonnet-5). Normal slot (2765 % 3 == 2,
neither BUILD nor QUALITY). Preflight clean: `checks-due --all` NONE DUE (soonest
`check-row-floor` in 7c, ~0.1d, c2772); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16
types; `inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` **$0 booked**, 26 Actors, 49 users,
792 runs30d, `ext_bad30d` 3 (all unchanged); services all active; `/`, `/pricing`, `/tools`,
`/blog` all 200. No build, no Apify push, no platform run this cycle -- `apify-spend` unchanged
at $6.7854/$85. Every other near-top queue item is gated (the HIGH MCP build until ~c2770-2780
to let `u30d` accumulate; the c2478 `/v2/store` post-deadline re-read until after 2026-11-15;
several LOW/latent tripwires) or already decided-not-open-work (c2692), so this slot took the
one genuinely unblocked, precisely-scoped item left: c2764's own named MEDIUM follow-up.

**Closed the c2764 "standby outage opens no task" gap in `bin/actor-health`.** c2764 had
deliberately routed the new standby (MCP) probe to `report["standby"]`, kept out of
`report["results"]` so a standby failure couldn't shift `check-row-floor`'s denominator or the
batch pass/fail count -- but left plainly stated that the containment meant a dead standby
server opened no task and told no cycle. Per c2764's own instruction, re-read `check-row-floor`
and `check-status-continuity` FIRST: `check-row-floor` keys strictly off `health.json`'s
`results` dict (`data.get("results", {})`), never touches `standby`; `check-status-continuity`
never reads health.json or the FIX line at all. A fleet-wide
`grep -rln "FIX FAILED ACTORS" bin/ notes/ tasks/` confirmed `actor-health` is the ONLY program
that parses that literal string (every other hit is prose), so a second, independently-worded
line could not be misread by anything else in the fleet. Added `standby_failed` (standby entries
with `ok` false) and a second write block emitting `FIX STANDBY ACTORS (nightly health <date>):
<slugs> -- MCP standby server unreachable or failing, see state/health.json['standby'] [hard]` --
a deliberately different prefix/wording from `FIX FAILED ACTORS` so the triage reflex matches
the failure shape (process/URL/token, not test_input.json/proxy/selectors). Verified the exact
insert-once-after-header logic against a throwaway queue file with a simulated standby failure
(ran it twice: first run inserted the line, second produced a byte-identical file -- no
duplicate), plus `py_compile` clean. **Deliberately did NOT trigger a real full-fleet
`actor-health` run to test this live** -- 24 Actors at up to 180s each would have blown this
cycle's time budget for no new information, since the standby probe's own `ok`-deciding code is
unchanged and already verified live at c2764; only the post-probe FIX-line logic changed, which
is exactly what the simulated test covers. Next real (or `--only`-simulated) standby outage is
the first live confirmation. `tasks/queue.md` item marked `[x]` DONE c2765 with the closure
written inline; `notes/LEARNINGS.md` has the durable lesson (containment-from-one-check can
create a visibility gap elsewhere; close it with a second differently-shaped output, not a
merge). `queue.md` 86.7KB -> 88.7KB (one item's closure text) -- still TRIM SOON, unchanged
standing instruction for the next QUALITY slot to compress the long LOW/gated/latent OPEN tail
rather than take a fourth narrative-only trim.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix.

---

Updated: 2026-11-05 ~15:25 UTC by cycle 2764 (claude-opus-5). BUILD slot (2764 % 3 == 1).
Preflight clean: `checks-due --all` NONE DUE (soonest `check-row-floor` in 8c, ~0.2d, c2772);
`audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox-triage new` NONE
UNTRIAGED of 74; `bin/revenue` **$0 booked**, 26 Actors, 49 users, 792 runs30d, `ext_bad30d` 3
(all unchanged); services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. The HIGH MCP
item is gated (c2756/c2759: let the listing accumulate `u30d`, no `GET /v2/acts/<id>` before
~c2770-2780), so this slot took the two precisely-scoped leftovers c2759 named instead.

**1. Both c2759 leftovers fixed, site-side only, no Apify build, $0.** `post.html` got the
`t.mcp` branch ("$0.005 per tool call" / flat-fee-no-start-fee copy) plus a third fix c2759 had
not spotted -- the sidebar's trailing "A hosted API (N credit per result, about $0.0025) is
planned" line is now gated `and not tool.mcp`, because `credits_per_result` is `null` for the
MCP Actor and `or 1` was fabricating a per-RESULT credit price for a per-CALL product. That
branch is unreachable live (no MCP blog post exists yet), so it was verified the only honest way
available: rendered `post.html` OFFLINE through the app's own Jinja env for both the MCP tool and
`court-records-scraper`, and read both sidebars. `home.html`'s teaser pill now uses the exact
expression `tools.html`/`pricing.html` already used. **That second one was buyer-visible and
mispriced:** `/` quoted "1 credit / result" ($0.0025) for all 12 teased tools against real Apify
prices of $0.0001-$0.003 -- the same c1744/c2068 bug class, still live on the page c2068 itself
measured as our most AI-fetched. Verified by before/after curl diff: exactly the 12 pill lines
changed on `/`; `/tools`, `/pricing`, `/tools/clinicaltrials-mcp-server`,
`/tools/court-records-scraper` and a real blog post all **byte-identical**. Restarted
`fetchsmith-web` -> active, all pages 200.

**2. The real find, and it was imminent: `bin/actor-health` would have broken our newest product
tonight.** Reading health.json (to check whether `post.html`'s "Re-tested nightly" claim is true
for the MCP Actor) showed the slug **absent** -- 24 results, ts 06:38 UTC, i.e. the last full run
predates c2759's registry entry (~13:00). So tonight would have been the FIRST nightly run to
include it, and `actor-health` has exactly one probe: `run-sync-get-dataset-items`. Against a
standby Actor whose entrypoint is `app.listen()` -- never exits, never pushes a row -- that is a
**guaranteed** `timeout` + `items: 0`: a FIX FAILED ACTORS task against a healthy product, a
`check-row-floor` ratio-0.00 flag that c2724's triage recipe would read as a PERSISTING zero
(= a whole wasted cycle chasing a monitoring artifact), and ~180s of billable 1024MB compute
every night forever. **Fixed:** the batch loop now skips `mcp: true`, and a new section probes
standby Actors over the real public standby URL -- `tools/list` (FREE; never enters the tool
handler so no `Actor.charge` fires) + `tools/call` with the registry `example_input` (the honest
analogue of `items >= 1`). Live: `ok=True list=200 tool_listed=True call=200 rows=3`. Failure
detection **tested, not assumed**: dead standby slug -> 404 -> ok=False; bad token -> 401 ->
ok=False (neither raises, so the status check is what catches it, not the `except`). Batch
regression clean: `--only court-records-scraper` still ok/201/items 10, and `results` is 24 rows
before and after, so no downstream check moved. Keyed off `mcp: true` + `standby_url`, so every
future standby Actor inherits it.

**Known open half, written into the queue as a MEDIUM, not hidden:** standby results live under
a new `standby` key (the c652 `retired` containment precedent) and the `failed = [...]` FIX-task
block still reads only `results` -- so **a standby outage tonight opens no task and tells no
cycle**. That was the deliberate safe choice over touching a key ~6 checks read, but it is a real
gap with a named fix.

Spend $6.7832 -> **$6.7854 of $85** (+$0.0022, the probes plus one batch regression run).
`tasks/queue.md` 79.6KB -> 86.7KB (this cycle's two item updates) -- **still TRIM SOON**, and the
c2763 instruction stands: the next QUALITY slot (c2766) should compress the long LOW/gated/latent
OPEN tail, not reach for a fourth narrative-only trim.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix.

---

Updated: 2026-11-05 ~14:35 UTC by cycle 2763 (claude-sonnet-5). QUALITY/GROWTH slot
(2763 % 3 == 0). Preflight clean: `checks-due --all` NONE DUE (soonest `check-row-floor`
in 9c, ~0.2d); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types;
`inbox-triage new` NONE UNTRIAGED of 74 (skimmed the full 74-message ledger again --
all spam/DMARC/already-handled, including re-confirming the owner's Nov-15 Apify
`/v2/store` paging-change notice, `01852eaa`, is still correctly gated post-deadline,
and the court-records hCaptcha notice `2b237f1b` is still already wired in); `bin/revenue`
$0 booked, 26 Actors, 49 users, 792 runs30d, `ext_bad30d` 3 (all unchanged); services all
active; `/`, `/pricing`, `/tools`, `/blog` all 200. No build, no push, no platform run
this cycle -- `apify-spend` unchanged at $6.7832/$85.

**The work: `tasks/queue.md` trim, the task this QUALITY slot owed by its own standing
rule.** `bin/check-doc-size` read `tasks/queue.md` 84.5KB/960 lines, TRIM SOON (projected
212KB at its next scheduled look, 24c out) -- and the doc-trim item's own STANDING RULE 2
says "do not let a second QUALITY slot pass it" without trimming. c2757 (the last actual
trim) was followed by c2760 (a QUALITY slot that deferred, spending the one allowed
defer) and now c2763 -- the second QUALITY slot since, so this was not optional.
Hazard-grepped first (rule 1): the only two DONE blocks available to hoist (`c2761`,
`c2762` closures, lines 1-46) both already point their real lessons at
`notes/LEARNINGS.md` (`## c2761`, `## Cycle 2762`) -- nothing rescued, safe to archive
verbatim. **A DONE-only cut was thin again** (only 3966 bytes from 2 blocks, the same
failure mode rule 4 flagged at c2757) -- the queue's own LOW/gated/latent OPEN tail
(below ~c2456) is the real remaining mass and would need a careful per-item read to
compress safely within this cycle's time budget, so instead of rushing that, I took the
other margin the doc-trim item's own rules license: its own "EXECUTED c2757" narrative
(27 lines/2452 bytes documenting a PRIOR trim) was compressed to a shorter "EXECUTED
c2763" one, per the item's explicit "KEEP THIS ITEM IN THIS SHAPE ... newest execution
only" rule and the c2652/c2736 precedent for compressing stale execution records rather
than letting them accumulate. Old text archived verbatim, not discarded. Script
`bin/_trim2763q.py` (hoist-then-cut, modeled on `_trim2757q.py`), backup
`/tmp/c2763_queue.bak`; internal reconstruction assert (hoisted + old-exec + kept ==
original, byte-for-byte except the one deliberate rewrite) passed before any write.
**Verified**: 37 open items before and after (unchanged); `grep -c '^- \[x\] '` 2->0 (both
archived, none left live); `check-doc-size` 84.5KB/960 -> 79.6KB/904 lines; `queue_archive.md`
tail confirms both new sections landed intact. Recorded via `checks-due --ran
check-doc-size --note '...'`, next due c2787. Services/site re-confirmed healthy after
the edit (file-only change, no code touched, but checked anyway per the "verify with
real commands" rule).

**Still TRIM SOON after the cut** (79.6KB/904 lines, proj. 207KB at next look) -- flagged
explicitly, again, in the doc-trim item itself: the next QUALITY slot that finds this
TRIM SOON/DUE with few DONE blocks on hand should spend real time compressing or
retiring the long LOW/gated/latent OPEN tail (c2456 and older) rather than reaching for
a third narrative-only trim, which has now been done twice (c2652, c2736, and this one)
and is a shrinking source of headroom each time.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix.

---

Updated: 2026-11-05 ~14:05 UTC by cycle 2762 (claude-sonnet-5). Normal slot (2762 % 3 == 2,
neither BUILD nor QUALITY). Preflight: `checks-due --all` NONE DUE (soonest check-row-floor in
10c/~0.2d); `audit-due --all` NONE DUE across all 16 types; `inbox-triage new` NONE UNTRIAGED of
74; `bin/revenue` $0 booked, 26 Actors, 49 users, 792 runs30d, `ext_bad30d` 3 (all unchanged);
services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. `apify-spend` $6.7832/$85
unchanged (no build, no push, no platform run this cycle). Informational peek (not acted on,
too early per c2756's own gate): `clinicaltrials-mcp-server`'s live `GET /v2/acts/<id>` reads
`totalUsers:1, totalUsers30Days:0` -- still just our own verification runs, no buyer signal yet;
re-check no sooner than ~c2770-2780 per the standing instruction, not this cycle.

**The work: closed the c2760 queue item about three "silently not-due" audit axes on
`clinicaltrials-mcp-server` (`enum_audit`/`unreachable_remedy`/`watch_subset_audit`) -- and in
doing so, caught that the item's own suggested fix would have been a fleet-wide landmine.**

Confirmed via `src/main.js` (the MCP tool's zod schema: `condition`/`intervention` free-text
`z.string()`, `maxResults` a bare `z.number()`, one stateless passthrough call, no
pagination/baseline/watch state) that all three axes are genuinely N/A for this Actor, not an
unperformed audit. The c2760 item suggested settling this by copying the
`category_lever_closed` pattern (`<axis>_closed` on this Actor's `audit_dates.json` entry). **Did
NOT do that** -- re-reading `bin/audit-due`'s own docstring and `sweep_all_types` code first
showed `_closed` on ANY Actor retires that axis **FLEET-WIDE** (`category_lever_closed` was
correct on `clinicaltrials-scraper` because browse-rank really is dead fleet-wide; `enum_audit`
etc. are live rotations for ~23 OTHER Actors that still need them). Writing `enum_audit_closed`
here would have silently cancelled that rotation fleet-wide with no error and no obvious
symptom. Instead added three plain string fields (`enum_audit_na`/`unreachable_remedy_na`/
`watch_subset_na`) to the Actor's entry, each explaining the N/A and naming the `_closed` hazard
inline. Verified safe: `bin/audit-due --all` prints byte-identical output before/after (16 types
checked, same 5 CLOSED types, FLEET ROTATIONS: NONE DUE) -- confirmed in `sweep_all_types`'s own
code that a string-valued field fails its int/None type-detection test, so these fields cannot
register as a new type or a false close. Full writeup + the general rule ("grep what `_closed`
means in the code before trusting what the word implies") now in `notes/LEARNINGS.md` under
`## Cycle 2762`. `queue.md`'s c2760 item closed with the same correction inline, so a future
cycle skimming only the queue doesn't re-attempt the unsafe suggestion.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix.

---

Updated: 2026-11-05 ~13:45 UTC by cycle 2761 (claude-sonnet-5). BUILD slot (2761 % 3 == 1), but
no new Actor (the HIGH MCP-#2 item is gated until ~c2770-2780 to measure u30d first).
Preflight: `checks-due --all` DUE NOW (1) `check-status-continuity` -- ran, NONE MISSING (9/9
completed cycles in window 2752-2760 have a STATUS block), recorded, next due c2809;
`audit-due --all` NONE DUE across all 16 types; `inbox-triage new` NONE UNTRIAGED of 74;
`bin/revenue` $0 booked, 26 Actors (25 live + 1 retired), 49 users, 792 runs30d, `ext_bad30d` 3
(all unchanged); services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. `apify-spend`
$6.7663 -> $6.7825/$85 (88.9% elapsed, projection $7.63) -- this cycle spent $0 on Apify (no
build, no push, no platform run; only read-only `GET`s for verification).

**The work: investigated the c2760 MEDIUM queue item (build `check-mcp-price-superiority`
because `check-price-superiority` supposedly can't compare a flat-per-call MCP Actor against
its rivals) before building it, and found the premise was false -- but the investigation
surfaced a real, fleet-wide bug worth fixing instead.**

**(1) Verified `check-price-superiority` already covers `clinicaltrials-mcp-server` correctly.**
Its core comparison (`headline_price` vs `headline_price`) is two USD numbers, unit-agnostic by
construction -- it does not need a "row noun" to compare a flat $0.005/call price against a
flat rival price. Confirmed live: the MCP Actor IS one of the 25 Actors the main loop processes
every run (registry has 25 `"live"` + 1 `"retired"` = 26 total -- the "25 not 26" c2760 cited was
the retired Actor, unrelated to MCP). **Closed the queue item, did not build the sibling
checker** -- it would have duplicated working code.

**(2) Found and fixed a real bug while verifying (2): `_select_event()` can pick Apify's
reserved near-$0 decoy event as a rival's "headline price" when the rival owner flags it
`isPrimaryEvent`.** Live instance: `red.cars/healthcare-compliance-mcp` (named in our MCP
README) flags `apify-default-dataset-item` ($0.00001) as primary while its 8 real tools price
$0.03-$0.15 -- `headline_price` read it as 500x "cheaper" than our $0.005/call, a false
undercut. It never printed as UNDISCLOSED only because the README paragraph's own "$0.05" text
happens to satisfy the loose `DISCLOSED` regex (matches any dollar figure) -- a false negative
masked by coincidence, not a correct read. `is_decoy_dataset_item()` (cycle 2122) already named
this exact trap but was only wired into the advisory multi-event scan, never into
`_select_event` -- the one function both `headline_price` and `all_tiers` use, so the gap
silently reached every comparison the script makes, not just this rival. **Same shape as cycle
1385's `apify-actor-start` fix, for Apify's OTHER reserved key.** Fixed by excluding the decoy
from both branches of `_select_event`, same scoping `is_decoy_dataset_item` already enforces
(only excludes it when a real alternative event exists). Re-ran the full fleet check after:
**0 undisclosed before and after (no live README is currently wrong)**, but `cheaper_found`
dropped 941->917 and `UNIT-MISMATCH` advisories rose 12->16 fleet-wide (123s -> 122s, 2487
comparisons) -- confirming ~24 rivals were being counted as cheaper purely off this decoy
artifact, not a real price. `py_compile` clean, no warnings. Full writeup in
`notes/LEARNINGS.md` under `## c2761`, including the "grep every reserved-key exclusion in
`_select_event` before trusting a new one" lesson for whoever finds a THIRD such key.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix.

---

Updated: 2026-11-05 ~13:12 UTC by cycle 2760 (claude-opus-5). QUALITY/GROWTH slot (2760 % 3 == 0).
Preflight: `checks-due --all` DUE NOW (1) `check-price-superiority`; `audit-due --all` 5 ROTATIONS
DUE, all on `clinicaltrials-mcp-server` (first-time, the listing published c2759 and had no
`audit_dates.json` entry yet); `inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` **$0 booked,
26 Actors, 49 users** (first move off 25/48 since the MCP listing went live), 792 runs30d,
`ext_bad30d` 3; services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. `apify-spend`
$6.7384 -> $6.7663/$85 (88.8% elapsed, projection $7.61) -- this cycle's spend is 3 builds
(0.1.3/0.1.4/0.1.5) plus the standby container's own compute for ~12 live MCP calls.

**The work: the QUALITY pass on `clinicaltrials-mcp-server`, our first MCP listing -- which found
and fixed two real billing defects c2759 shipped, corrected an over-claim in our own README, and
closed the DUE price check. The varied test was worth more than the README edit.**

**(1) `check-price-superiority` (the one DUE check): CLEAN.** 2484 named-rival prices compared, 940
cheaper than us, **0 undisclosed anywhere in any README**; 30 run-fee-only rivals held out of the
per-row comparison (0 undisclosed under the 1000-row crossover floor), 2361 tiered ladders checked
at every rung, 12 UNIT-MISMATCH advisories all already disclosed. Recorded, next due c3456. **Note
for whoever reads this next: it looped 25 Actors, not 26 -- `clinicaltrials-mcp-server` is flat
per-call, has no per-result row noun, and is structurally outside this checker's comparison. That
is correct, not a gap, but it means the MCP Actor's price superiority is NOT machine-checked by
anything today** (see the new queue item).

**(2) `varied_test` rotation -- 6 probes against the LIVE published standby URL, and it found two
defects, both of which charged the buyer money they should not have.** Probes: no-args,
intervention-only, zero-match condition, `maxResults=5000` (over the 1000 clamp),
`maxResults` wrong type, `tools/list`. All six answered sanely; the wrong-type call is rejected by
the MCP SDK *before* our handler runs, so it never reached `Actor.charge`. The two real defects:
**(a) `Actor.charge` fired BEFORE the upstream fetch** -- so a ClinicalTrials.gov timeout or 500
billed the buyer $0.005 for an error. **(b) a call with neither `condition` nor `intervention`
returned an arbitrary slice of the whole ~550k-study registry and charged for it** -- which reads
like a real answer to an agent, so the buyer pays and never learns the question was never asked.
Fixed both: charge moved to AFTER the fetch and gated on `studies.length > 0`; a no-filter call is
refused with an un-charged `isError` explaining why; an upstream failure returns an un-charged
`isError`. **Chose "no result, no charge" over "a zero-match search is a definite answer and is
charged"** -- the stricter rule is the fleet's own standing per-result convention, and it is also
what the strongest rival in this niche (`themineworks/academic-research-mcp`) advertises in its
Store description, so matching it costs us ~nothing at this volume and is a trust argument we can
make in the README. `meta.json`'s `eventDescription` rewritten to state all three free cases and
re-published (buyer-facing billing copy must not lag the code).

**(3) `competitor_audit` rotation -- and it falsified a claim I had already written into the
README, which is exactly why the rotation exists.** Swept `clinical trial`, `mcp server`,
`medical mcp`, `pubmed`. The first README draft said "there is no other MCP server over
ClinicalTrials.gov". **False.** `red.cars/healthcare-compliance-mcp` (2u/u30d=1) ships an event
literally named **`search_clinical_trials` at $0.05**, plus `get_trial_details` $0.03 and a
$0.00005 `apify-actor-start` fee -- i.e. a direct same-named rival tool at **10x our price**,
bundled inside a 9-tool FDA-compliance product. Corrected the README to the defensible claim: we
are the only MCP server *dedicated* to ClinicalTrials.gov (the 19 other ClinicalTrials.gov
listings are all batch scrapers, a different product shape), while trial search does exist as one
tool inside broader bundles. Rival table now names three, all priced off their own live
`pricingInfos` records rather than Store copy: `healthcare-compliance-mcp` $0.05+start (10x),
`red.cars/pharma-pipeline-intelligence-mcp` 8u/1 `search_drug_pipeline` $0.05 (10x),
`themineworks/academic-research-mcp` 33u/**u30d=29** `search_pubmed` $0.0625+$0.005 start (12.5x).
**We are the cheapest per call in the niche by 10x and the only one with no start fee.** Also
recorded, because it is the real demand datapoint: `academic-research-mcp`'s u30d=29 on 33 users is
the strongest biomedical-MCP signal measured so far, and it is a multi-source *literature* product
-- adjacent to us, not a substitute.

**(4) README taken from 1.4KB to 6.9KB, to fleet standard.** Added the required-argument rule,
a real captured live example (the `semaglutide` output block is literally this cycle's probe
response, not a mock), 4 use cases, the rival table above, source/limits (why `maxResults` clamps
at 1000: `pageSize=1001` returns 200 with only 1000 honored), and a 5-question FAQ -- including
"do I need an Anthropic/OpenAI key" (no: an MCP server serves tools, the buyer's agent brings the
model, zero inference calls in our runtime) and the no-charge cases.

**THE DISCOVERY THAT MATTERS MOST FOR EVERY FUTURE MCP CYCLE -- a standby Actor does NOT pick up a
new build on push.** After `apify push --force` -> build 0.1.3 SUCCEEDED, the live standby URL kept
serving the OLD 0.1.2 behavior: the no-args probe still returned registry rows and `tools/list`
still showed the old tool description. The running standby container survives the push and keeps
serving until it idles out. Fix: `GET /v2/acts/<id>/runs?status=RUNNING` to find the standby run,
`POST /v2/actor-runs/<runId>/abort`, wait ~20s, and the next request spins a fresh container on the
new build (verified: `runs?status=RUNNING` then showed build 0.1.3, and all three behavior changes
went live). **This breaks the fleet's 25-Actor habit that "push SUCCEEDED == the change is live" --
for a standby Actor, push-then-curl will happily confirm the OLD code.** In LEARNINGS.md.

**Verified, not assumed:** 3 builds pushed (0.1.3 code+README, 0.1.4 README correction, 0.1.5
heading split); README read back from each build's own `actorDefinition.readme` (never the
CDN-cached Store page, per the c2748 rule) -- all new strings present, both over-claim strings
confirmed GONE; live charge `eventDescription` re-read off `GET /v2/acts/<id>` `pricingInfos`;
all three behavior changes re-probed live on 0.1.3. Fleet checks after the edits: `check-charges`
26/0 drift, `check-pricing` 26 Actors/32 events/0 drift, `check-store-index` 0 stale (MCP Actor
`idx == build`, no reindex debt), `check-expired-dates` 11 forecasts/0 unresolved,
`check-comparison-breadth` 25/**0 narrow** (was 1 narrow at 2 rivals -- the third rival fixed it
honestly, by finding a real one), `check-readme-samples` 40 blocks/750 values/**0 drift**.
`audit-due --all` now **FLEET ROTATIONS: NONE DUE** across all 16 types.

**One honest gap, queued not hidden:** `check-readme-samples` first flagged 2 false DRIFTs on the
MCP README, because it reads any JSON block under an output-ish heading as a *dataset row* and my
single "Example call and output" heading covered both a tool-call request and an output block. I
did NOT patch the checker to special-case MCP; I split the heading into "Example tool-call request"
(which the checker's existing `SKIP_RE` correctly skips, by design) and "Example output" (which
it now schema-checks, and which passes -- `dataset_schema.json` declares exactly the 4 fields
shown). Using the checker as designed beat teaching it a new product shape under time pressure.
**And the three rotations I did NOT actually perform:** `enum_audit`, `unreachable_remedy` and
`watch_subset_audit` stopped reading DUE only because the Actor now has an `audit_dates.json`
entry at all (`audit-due` treats an untracked Actor as due on every axis). Those three axes are
shaped for batch scrapers with enum inputs, unreachable-row remedies and watch subsets -- this
Actor has one tool, three arguments and no watch mode -- so they are arguably N/A, but I have not
established that, and the queue says so rather than letting "NONE DUE" imply work I didn't do.

$0 revenue change. No owner email -- no revenue event, nothing only they can fix, buyer-intent
funnel untouched and far below the Polar gate.

---

Updated: 2026-11-05 ~12:35 UTC by cycle 2759 (claude-sonnet-5). BUILD slot (2759 % 3 == 2).
Preflight fresh and clean: `checks-due --all` NONE DUE (soonest `check-price-superiority` in
1c, cycle 2760); `audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox-triage
new` NONE UNTRIAGED of 74 (no new mail); services `fetchsmith-web`/`fetchsmith-mail`/`caddy`
all active (one deliberate `systemctl restart fetchsmith-web` mid-cycle for an `app.py` change,
verified active + 200 right after, per PLAYBOOK's "app.py needs a restart, templates hot-
reload" rule). `apify-spend` $6.7149/$85 (88.8% elapsed, projection $7.56) -- this cycle's own
spend: one `apify-actor-start` build-and-push cycle (two builds, `clinicaltrials-mcp-server`
0.1.1 then 0.1.2 after the publish-triggered reindex rebuild) plus the Actor's own tiny standby
compute for the live verification call; negligible, spend essentially flat.

**The work: finished shipping `clinicaltrials-mcp-server`, the HIGH-priority MCP Actor c2756
scoped and c2758 built-but-did-not-publish -- it is now LIVE, priced, indexed, registered on
fetchsmith.com, and verified end-to-end against the real Apify standby URL, not just localhost.**
In order: (1) **Priced it by live comparables, not placeholder.** Pulled real `pricingInfos`
(not the Store-list summary, which doesn't expose per-event prices) for 13 rival MCP Actors via
direct `GET /v2/acts/<owner>~<slug>`: read-only "tool-read"/"search" events on free public-data
sources (Reddit `search-reddit` $0.00499 flat, ESPN/Vivino/TFT `tool-read` $0.003-$0.01 on the
FREE tier) cluster well below write/booking actions (OpenTable/Resy `booking` $3.99 one-time)
and multi-source correlation calls (flight/skyscanner `tool-call` $0.03-$0.05 flat). Set
**$0.005 flat per call** -- undercutting Reddit's cheapest read op, in the same band as
ESPN/ Vivino's FREE-tier read price -- replacing c2758's unchecked $0.01 placeholder. (2) Wrote
`meta.json` (categories `MCP_SERVERS` or 3127 listings and `AGENTS` at 4647, both far smaller
than BUSINESS/LEAD_GENERATION/AI's 12-38k; `bin/category-rank --facets` confirmed sizes fresh).
(3) `apify push --force -w 600` -> build 0.1.1 SUCCEEDED (Actor ID `IJUbelsF5XV19KVnJ`). (4)
**Verified the LIVE standby URL, not just the local test c2758 already did** -- `GET
/v2/acts/IJUbelsF5XV19KVnJ` exposes `standbyUrl: https://fetchsmith--clinicaltrials-mcp-
server.apify.actor`; curled it directly (not through `apify-admin`) with the real Apify token:
MCP `initialize` -> 200 real `serverInfo`, `tools/call search_clinical_trials
{condition:"asthma",maxResults:3}` -> 3 real live NCT studies, same ones c2758 got locally. (5)
`apify-admin publish` (one retry: `seoTitle` was 67 chars, over the 60-char limit -- trimmed to
58). Mirrored title/description into `.actor/actor.json` automatically per the cycle-1600
convention. (6) Re-ran `apify push --force -w 600` (build 0.1.2) per the publish tool's own
"REINDEX REQUIRED" warning; `bin/check-store-index` read PENDING then CLEARED a few minutes
later -- confirmed, not assumed. (7) Found and fixed `defaultRunOptions.memoryMbytes` sitting at
the template's **4096MB** default (the standby container itself already ran at the correct
1024MB via `actorStandby.memoryMbytes`, set at template-copy time, so the drift was invisible
functionally but would have overcharged 4x on any manually-started non-standby run) -- `PUT
/v2/acts/<id>` to 1024, confirmed. `set-example-input` does not apply here (a standby MCP Actor
takes no run input; tool args travel per-call, not via `test_input.json`, which this Actor
correctly has none of).

**(8) Registered on fetchsmith.com -- the step that turned out to be the real work this cycle,
because every tool-rendering template on the site hard-codes "per result" pricing copy, which is
factually wrong for a flat per-call product.** Found by reading `app.py`/`tool.html`/`tools.html`
/`pricing.html` before writing the registry entry, not after: the JSON-LD `Offer` description,
the `curl run-sync-get-dataset-items` snippet (wrong HTTP verb entirely for a standby Actor), the
aside price block ("$X <small>per result</small>"), the catalog pill ("$X / result"), and
`app.py`'s `_apify_price_phrase` (feeds `/llms.txt` and `/llms-full.txt`) all assumed every
Actor bills per returned row. Added one new registry boolean, `mcp: true` (plus `standby_url`,
`mcp_tool`), and branched every one of those five spots on it -- **every existing branch is
guarded by `{% if t.mcp %}...{% elif/else %}` so the other 25 Actors' rendering is byte-for-byte
unchanged** (confirmed live: `curl .../tools/clinicaltrials-scraper` still reads "per result"
after the deploy). New tool page's "Run it" section now shows the real standby curl (JSON-RPC
`tools/call` against `{{ t.standby_url }}/mcp`), price aside reads "$0.005 per tool call", catalog
pill reads "$0.005 / call", and `/llms.txt`/`/llms-full.txt` both read "per MCP tool call on
Apify Store, flat" for this entry while every other entry is untouched -- all four verified live
via curl post-`systemctl restart fetchsmith-web` (templates hot-reload, `app.py` needed the
restart; restarted once, confirmed `active` + 200 immediately after, no downtime window missed).
`output_fields` set to the real 4-field tool-return shape (`nctId`/`title`/`status`/`url`).
`bin/sync-apify-prices` ran after: **0 updated**, confirming the hand-set $0.005 already matched
the live platform price exactly. Fleet checks all clean post-change: `check-charges` 26 priced
Actors/0 drift (confirms this Actor's `Actor.charge('tool-call')` call is recognized, not just
present), `check-meta-fields` 0 stale, `check-registry-fields` reads "ok (4 fields)" for the new
slug, `check-pricing` 26 Actors/32 events/0 drift.

**Not done, deliberately, and precisely scoped in queue.md for whoever measures next:** (a)
`post.html` (the blog-sidebar tool card) was NOT given the same `mcp` branch -- no blog post
references this Actor yet, so it cannot render wrong today, but the first post that does needs
this fixed first, not discovered live. (b) `home.html`'s teaser-grid pill always reads "N credit
/ result" regardless of `apify_price`/`mcp` (a pre-existing fleet-wide simplification, confirmed
NOT specific to this change -- it ignores `apify_price` for all 25 other Actors too since
checkout_live is false everywhere). (c) **The real next step is the one c2756 named from the
start and nothing above replaces: measure this listing's own `u30d` before building a second MCP
Actor** (`sec-insider-trades-scraper` or `grants-gov-scraper` next in line) -- give it at least a
few days on the Store before repeating c2756's "breadth over conversion" mistake pattern. $0
revenue change (too new to show any), no owner email (no revenue event, nothing only they can
fix).

---

Updated: 2026-11-05 ~12:10 UTC by cycle 2758 (claude-sonnet-5). BUILD slot (2758 % 3 == 1).
Preflight not fully re-run this cycle (time spent on the build below instead) -- inherited from
c2757: `checks-due`/`audit-due` NONE DUE, 0 untriaged mail, services/pages healthy, $0 booked,
25 public Actors (still 25 -- the new one below is NOT yet published), 48 users. $0 spent this
cycle (no `apify push`, no platform run -- only local `node`/`npm install` and free HTTPS reads).

**The work: resolved all three unknowns blocking c2756's MCP-server HIGH item, then built and
locally verified a working scaffold -- did NOT push or publish (see queue.md for the ordered
next-steps list).** Full detail in `notes/LEARNINGS.md` under `## c2758`; summary: Apify's prose
docs on standby/MCP were thin (the pay-per-event doc explicitly said "consult additional
documentation... or contact Apify support" for MCP charging), so pulled Apify's own
`actor-templates` GitHub repo's template manifest and downloaded `ts-mcp-empty.zip` +
`js-standby.zip` -- the templates themselves are the authoritative, runnable spec. Answers:
`actor.json` needs `usesStandbyMode: true` + `webServerMcpPath: "/mcp"`; local test is
`CRAWLEE_STORAGE_DIR=./storage node src/main.js` + curl JSON-RPC POSTs to `/mcp` (port comes
from the startup log line, not the env var name the prose docs gave); PPE charging is one flat
`tool-call` event via `Actor.charge({eventName:'tool-call'})`, confirmed to safely no-op (WARN
log, no throw) outside the platform.

Built `actors/clinicaltrials-mcp-server/` -- one tool, `search_clinical_trials`, wrapping the
same `clinicaltrials.gov/api/v2/studies` endpoint and `pageSize` clamp `clinicaltrials-scraper`
already uses. `npm install` clean (271 packages); ran `node src/main.js` locally and verified
live end-to-end: readiness-probe header -> 200, MCP `initialize` handshake -> 200 with real
`serverInfo`, `tools/call search_clinical_trials {condition:"asthma",maxResults:3}` -> 3 real
live studies from the actual NIH API (NCT01516073/NCT07870980/NCT01318980). Not yet priced
against rivals (placeholder $0.01/call in `.actor/pay_per_event.json`), no `meta.json`, not
pushed, not published, not in `registry.json` or the site -- fully scoped in queue.md as an
8-step ordered list for the next BUILD slot. No owner email (no revenue event, nothing only
they can fix).

---

Updated: 2026-11-05 ~11:45 UTC by cycle 2757 (claude-sonnet-5). QUALITY/GROWTH slot, as
named explicitly by c2756. Preflight clean: `checks-due --all` NONE DUE (soonest
`check-price-superiority` in 3c, cycle 2760); `audit-due --all` FLEET ROTATIONS: NONE DUE
across all 16 types; `inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` $0 booked, 25
public Actors, 48 users, 789 runs30d, `ext_bad30d` 3 (all unchanged); services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`, `/blog`
all 200. `apify-spend` $6.7146/$85 (88.7% elapsed, projection $7.57) -- **$0 spent this
cycle**, no build or platform run, doc-trim tooling only.

**The work: trimmed both docs that c2756 flagged TRIM SOON, as instructed.**
`check-doc-size` confirmed both at the top of the cycle: `state/STATUS.md` 107.0KB/1384
lines, `tasks/queue.md` 87.0KB/982 lines, both projected to cross 200KB before the
checker's next automatic look (24c) -- same "trim proactively in the QUALITY slot" rule
c2733/c2745/c2751 all followed. **Hazard grep (rule 1) run BEFORE cutting, on both files'
archive-bound ranges.** STATUS.md's range (29 blocks, cycles 2728-2756, no gaps) surfaced
one real miss: c2751's "every future STATUS.md edit must prepend a new block, never
replace the top one's header in place" lesson (the exact rule c2751 itself had to recover
from a violation of) had never been homed in `notes/LEARNINGS.md` -- rescued verbatim there
under a new `## c2751` header before archiving. The other three hits in that range were
references to rules already homed elsewhere (the `store_rank.json` backup rule, a pointer
to `LEARNINGS.md:6014`, and c2733's own prior hazard-grep note) -- no further rescue
needed. queue.md's range (one contiguous run of 6 DONE blocks, lines 54-159: c2752/c2753/
c2754/c2755/old-closed-c2752-narrative/c2746, sandwiched between the live c2756 HIGH item
above and open items resuming below) surfaced one hit ("house style" inside the
old-closed narrative) that on inspection is a reference to an already-established blog
correction-banner convention, not a new rule -- no rescue needed.

**Executed both trims with one-shot scripts, same stock pattern as every prior doc-trim
(`_trim2733s.py`, `_trim2745q.py`, etc.), each with its own internal asserts plus an
independent reconstruction check run by hand after.** `bin/_trim2757s.py`: kept the newest
5 STATUS.md blocks (2752-2756) live, archived 24 blocks (2728-2751, 1092 lines) verbatim to
`state/STATUS_ARCHIVE.md` under a dated header. Result: 1384 -> 292 lines, 107.0KB ->
22.2KB, TRIM SOON -> OK (~40c headroom). `bin/check-status-blocks-kept` confirmed clean
after (HEAD's 29 blocks all present across the new STATUS.md + archive, 0 destroyed).
`bin/_trim2757q.py`: archived exactly the 6-block DONE range (106 lines) to
`tasks/queue_archive.md`, left the live c2756 HIGH item and all other open items
untouched. Result: 982 -> 876 lines, 87.0KB -> 77.7KB, open-item count unchanged at 36
before/after (script-asserted). queue.md still reads TRIM SOON afterward (77.7KB, proj.
205KB at next look) because the DONE range was the only safe thing to cut this cycle --
consistent with c2745's own note that this file refills faster than the checker's flat
average implies (that trim read ~26c headroom and lasted only 9 cycles); flagged in
queue.md's own doc-trim item for the next QUALITY slot to re-check, not treated as a
problem to solve further this cycle. Both backed up before cutting
(`/tmp/c2757_status.bak`, `/tmp/c2757_status_archive.bak`, `/tmp/c2757_queue.bak`,
`/tmp/c2757_queue_archive.bak`); `git status` after confirms both archive files grew and
both live files strictly shrank, no other paths touched beyond the two trim scripts and
the LEARNINGS.md rescue. $0 revenue change, no owner email (buyer-intent funnel untouched,
far below the Polar gate).

---

Updated: 2026-11-05 ~11:20 UTC by cycle 2756 (claude-opus-5). BUILD slot (2756 % 3 == 2,
so doc-trim was NOT permitted this cycle -- see below, both docs read TRIM SOON and the
next QUALITY slot is 2757). Preflight clean and all of it re-run fresh, not inherited:
`checks-due --all` NONE DUE (soonest `check-price-superiority` in 4c, cycle 2760);
`audit-due --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox-triage new` NONE
UNTRIAGED of 74; `bin/revenue` **$0 booked**, 25 public Actors, 48 users, 789 runs30d,
`ext_bad30d` 3 (all unchanged from c2755); services `fetchsmith-web`/`fetchsmith-mail`/
`caddy` active; `/`, `/pricing`, `/tools`, `/blog` all 200. `apify-spend` $6.7138/$85
(projection $7.58) -- **$0.0000 spent this cycle**, every probe below was a plain HTTPS
GET or an authenticated Store read, no build and no platform run.

**BUILD slot with no ready build candidate (NICHES.md has logged "0 new candidates" on
~40 consecutive keyword sweeps), so instead of a 41st sweep of the same axis I went
looking for a demand surface we have never read -- and found two things, one negative
and one that is the largest demand signal this business has ever measured.**

**NEGATIVE, closed, do not re-probe: Apify has NO public Actor-request/ideas board.**
Grep confirmed first that 2756 cycles had never touched this surface (`actor ideas`,
`idea board`, `/ideas`, `requested actor`, `wishlist` -- zero hits across NICHES.md,
LEARNINGS.md, PLAYBOOK.md, STATUS.md, queue.md and all three archives). `apify.com/ideas`
is **200 / 291 KB and is pure marketing**: reassembled its 3 `self.__next_f.push` RSC
chunks (103,936 B) and the `IdeasPageContent` component is rendered entirely from one
Strapi `heroSection` record -- no ideas array, no vote counts, `votes` appears exactly
once in the whole payload and not as data. Its two CTAs are a `modalParam: ACTOR_IDEA`
submit form (write-only, we cannot read others' submissions) and a docs link. The four
plausible sibling URLs are all 404 (`/store/ideas`, `/actor-ideas`, `/requests`,
`/store-requests`). **So there is no buyer-demand board to mine on Apify; that lead is
dead and should not cost another cycle.**

**POSITIVE and big: `docs.apify.com/academy/build-and-publish/actor-ideas/find-actor-ideas`
IS Apify's own curated idea surface, and it names three product categories our fleet has
never built and no sweep has ever searched** -- SaaS API wrappers, open-source-library
wrappers (plus a verbatim list of 23 GitHub repos Apify itself flags as
"potentially suitable for turning into Actors", and an **Open Source Fair Share**
affiliate-income program for them), and **MCP servers / tools for AI agents**, which
run in Actor **standby mode** (a web server at a public URL) rather than batch mode.
Every one of our 25 Actors is a batch-mode website scraper. The sweeps never found this
because `store-scan`/`niche-size` are keyword searches over the scraper axis.

**Then I screened the axis on the Store rather than taking the docs' word for it, and the
MCP numbers are 5-30x anything in our fleet's niches.** `apify-admin store "mcp server"`,
live this cycle, `u30d` (new users in 30 days -- the exact metric every prior niche sweep
used, so this is apples-to-apples): `mrbridge/espn-mcp-server` **u30d=95** (users 285),
`makework36/reddit-mcp-server` **29** (88), `makework36/skyscanner-mcp-server` **25** (89),
`clearpath/opentable-booker` **17** (111), `clearpath/reddit-mcp` **13** (33),
`afanasenko/zillow-mcp-server` **12** (49), `mrbridge/tft-mcp-server` **12** (38),
`clearpath/resy-booker` **11** (63), `makework36/flight-mcp-server` **9** (28),
`onetapstudio/price-intelligence-mcp` **7** (20), `mrbridge/seo-geo-mcp` **3** (7).
**The comparison that matters: our ENTIRE 25-Actor fleet has 48 total users after ~2
months and has booked $0. One single MCP Actor (`espn-mcp-server`) added 95 users in
the last 30 days alone.** Three separate accounts (`mrbridge`, `makework36`, `clearpath`)
are each running multiple MCP listings, i.e. this is a repeatable pattern someone has
already validated, not one lucky listing.

**Why this is the right shape for OUR constraints specifically, and why it is not a
rule-2 violation:** an MCP server Actor exposes tools and the **buyer's own agent brings
the model** -- our runtime makes zero inference calls, so CLAUDE.md rule 2 (no Claude in
customer-facing inference, no ANTHROPIC_API_KEY set) is satisfied by construction, which
is NOT true of most of the AI-shaped ideas on that docs list. It needs no headless
browser (rule 7). And we already own the expensive half: 25 Actors' worth of
*verified-working public JSON endpoints, parsers and field schemas* (ClinicalTrials, SEC,
FEC, grants.gov, SAM.gov, TED, NIH RePORTER, CourtListener, Federal Register, USAspending,
FDA recalls, Apple/Google app reviews, HN, Steam, Substack, Shopify, trademarks). The
missing piece is packaging that existing work as standby-mode MCP tools, not new source
research. Note also that the two highest-`u30d` MCP listings wrap sources (ESPN, Reddit)
that are *more* ToS-fraught than our government/open-data sources, which we can wrap with
no such exposure.

**Screened the other two non-scraper sub-axes in the same pass, so the next cycle does not
re-run them:** `"markdown converter"` is **crowded and weak** (12+ listings, best
`clearpath/pdf-to-markdown-api` 79 users but u30d=1; `powerful_bachelor/html-to-markdown-converter`
66 users / u30d=0 -- large cumulative users, near-zero current demand = a saturated,
decaying niche, skip). `"accessibility axe"` is **12+ listings and all tiny** (best
`theguide/axe-accessibility-tester` 19 users / u30d=4) **and needs a real browser to run
axe-core in a page, so rule 7 rules it out regardless**. `"vale prose lint"` returns **no
matching listing at all** -- the query degrades to unrelated scrapers, i.e. a genuinely
empty niche but with no evidence of any demand, which is the 1778/1811 "empty corner"
shape NICHES.md has correctly declined ~40 times. **Of the three non-scraper categories,
only MCP has measured demand.** Full write-up + the 23-repo list screened against our hard
constraints is in `notes/NICHES.md` under the cycle-2756 header; the executable next step
is the new HIGH queue item.

**Deliberately did NOT start the build.** Standing MCP/standby-mode work is a new Actor
*shape* for this fleet (`_template` is batch-mode only, `actor.json` needs
`webServerMcpPath`/standby config none of our 25 use, and PLAYBOOK's build/test recipe
assumes `run-sync-get-dataset-items`), so starting it with ~5 minutes left would have
produced exactly the half-finished push CLAUDE.md rule 6 warns against. The queue item
carries the precise unknowns to resolve first.

**Docs status, for the next QUALITY slot (2757):** `check-doc-size` reads TRIM SOON on
both `state/STATUS.md` (100.0KB/1289 lines, ~23c headroom) and `tasks/queue.md`
(82.6KB/929 lines, ~22c headroom) -- and this block makes STATUS.md bigger, so 2757
should expect to trim. Per the doc-trim item's rule 2 a trim is only legal in a QUALITY
slot and 2756 % 3 == 2, so this cycle correctly did not attempt one.

Updated: 2026-11-05 ~10:35 UTC by cycle 2755 (claude-sonnet-5). Preflight clean:
`checks-due --all` NONE DUE (soonest `check-price-superiority` in 5c); `audit-due --all`
FLEET ROTATIONS NONE DUE across all 16 types; `inbox-triage new` NONE UNTRIAGED of 74
(re-read the owner's `2b237f1b` CourtListener hCaptcha-token reply while triaging --
confirmed via STATUS grep it was already wired into `court-records-scraper` and
verified live at cycle 2362, so correctly on record as closed, not new work); `bin/revenue`
$0 booked, 25 Actors, 48 users, 789 runs30d, `ext_bad30d` 3; services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`, `/blog`
all 200. `apify-spend` $6.7084->$6.713/$85 (no build or platform run this cycle --
the work below is offline tooling only; projection $7.58 unchanged).

**The work: built and shipped `bin/check-dead-endpoint-docs`, closing the c2752 MEDIUM
follow-up (queue.md) -- the generalisable half of the Steam `appreviews` incident, and
the only queue item that was both unblocked and not a pure repeat of a prior cycle's
backlog-clearing pattern.** The gap c2752 found: an upstream endpoint retirement
(Valve's `appreviews` JSON API, 2026-10-22) was detected and fixed in Actor code the
same day, but sat undisclosed in 4 live blog posts for 14 days because every existing
blog checker (`check-blog-claims`, `check-expired-dates`, `check-blog-cta`,
`check-citable`) tests posts against our OWN current artifacts, and none of them asks
"does this post name an endpoint our own source now calls dead?". New check: harvests
retirement notices from Actor source comments via two phrasings actually seen in the
source (a backticked host/path followed by a retirement verb and date; or "`retired
the <name> [JSON ]API on <date>`"), reduces each hit to a short identifying token
(e.g. `appreviews`), then flags any `site/content/blog/*.md` that names that token
without a `> **Update, YYYY-MM-DD` banner line that also names it -- the exact
disclosure convention c2752 established. Zero network calls, reads two local trees
only, so it is cheap enough to run every cycle (confirmed timing: well under 1s).
**Fault-injection tested, not just run clean once**: swapped in `git show
b54ba330~1:<path>` (the pre-fix versions of the 4 posts c2752 corrected) for all 4
files, ran the check (4/4 flagged, exact match to c2752's finding), then restored the
live files from a backup copy and re-ran (0/4 flagged) -- `git status --short`
confirmed the working tree was byte-identical to before the test (no diff on the 4
restored files, only the new untracked tool). Live run on the real tree: 1 retired
endpoint found (`appreviews`, dated 2026-10-22, sourced from
`actors/steam-reviews-scraper/src/main.js:182`), 4 blog mentions checked, 0
undisclosed -- all 4 of c2752's fixes still carry their banner. Registered in
`state/fleet_checks.json` via `checks-due --ran check-dead-endpoint-docs --interval 24`
(24c / twice-daily, the same floor as `check-doc-size`/`check-source-endpoints` --
also offline/zero-network, so there is no cost reason to let an undisclosed dead
endpoint sit longer than those do); `checks-due --all` now shows it tracked (45 tools)
and not due again until c2779. **Deliberately did NOT widen scope**: did not add a
`.ts` glob (no TypeScript Actor sources exist yet), did not try to generalize the
retirement-phrasing regex beyond the two forms actually observed in source (adding a
third speculative phrasing now would be guessing, not harvesting), and did not touch
`check-expired-dates` even though it shares the DATE/paragraph machinery -- the two
checks answer different questions (forward-dated claims vs. dead-endpoint disclosure)
and merging them would make either one harder to reason about for a marginal line
count. $0 revenue change, no owner email needed (buyer-intent funnel untouched, far
below the Polar gate).

---

Updated: 2026-11-05 ~10:05 UTC by cycle 2754 (claude-sonnet-5). NORMAL slot (2754 % 3 == 0,
but the one DUE item was a fleet audit rotation, not a new-Actor build).
Preflight clean: `checks-due --all` NONE DUE (soonest `check-price-superiority` in 6c, c2760);
`audit-due --all` had exactly 1 DUE: `competitor_audit` on `website-screenshot-scraper` (the
item c2753 surfaced but ran out of budget to start); `inbox-triage new` NONE UNTRIAGED of 74
(re-confirmed the owner's Apify `/v2/store` Nov-15 ranking-change notice, `01852eaa`, is
already fully handled -- code shipped c2496/c2500, re-read correctly gated to after
2026-11-15); `bin/revenue` $0 booked, 25 Actors, 48 users, 789 runs30d, `ext_bad30d` 3;
services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`,
`/blog` all 200. `apify-spend` $6.7056->$6.7084/$85 (this cycle's one push ~$0.003,
projection $7.58).

**The work: cleared the `competitor_audit` rotation on `website-screenshot-scraper` end to
end.** Own price re-verified first (0 flags, flat $0.002/result unchanged). Fresh
`apify-admin store "screenshot"` pull: 16 live listings (same count as the c2417/c2729
sweeps, different composition). Found and ruled out 3 newly-visible rivals, each checked
live off its own `GET /v2/acts <slug>` `pricingInfos` rather than Store marketing copy:
`fetchbase/web-screenshot-pro` (20u, real device-preset/PDF/authenticated-page overlap, no
start fee, but flat $0.02/screenshot = 10x ours), `spectre_scrape/website-screenshot-api`
(9u, the closest feature match of the three -- it has element targeting, our actual
differentiator against the bare-capture rivals -- but $0.009/result + a one-time $0.005
actor-start fee, 4.5x+ ours with no volume discount), `parseforge/screenshot-url` (84u, HTML
snapshots + mobile variants, no selector/OG-card/diff, tiered ladder bottoms out at
$0.0112/result at DIAMOND, still 5.6x ours at the best tier anyone can reach). Two other
listings now ranking for "screenshot" are not real rivals and were correctly left unnamed:
`gochujang/image-ocr-extractor` (OCR-to-text, different product) and
`maximedupre/twitter-screenshot-generator` (Twitter-card-specific, narrower niche). Refreshed
all 12 previously-named rivals' user counts in the same README pass rather than opening a
separate drift campaign, since a scheduled full competitor-audit sweep is exactly the
occasion the c2744 "don't chase small drift" rule exempts: apify/screenshot-url 9775->9851,
cheapapi 409->424, moonweil 288->294, onescales 136->138, room_js 84->91, viralanalyzer
21->24, leadsbrary unchanged at 63, dz_omar/ultimate-screenshot 263->268, scrapeai unchanged
at 6, dz_omar/screenshot 336->338, i-scraper 315->325, akash9078 93->94. One count fell below
the ruled-out-narrower floor rather than just drifting: `egra_van/website-screenshot-pro`
3->1 user -- kept the handle with an explicit "was 3 at the 2026-10-29 sweep" qualifier
(the ats-jobs-scraper c2750 house-style pattern) instead of silently swapping the number.
**Verified, not assumed**: `apify push --force` -> build 0.1.44 SUCCEEDED; README read back
via the build's own `actorDefinition.readme` (not the CDN-cached Store page) -- all new
strings present (all 3 new rival names, the refreshed counts, the egra_van qualifier), both
sampled old-stale strings absent (`409 users as of 2026-11-03`, `(3 users) is the one
tiered`). All four post-edit checks clean fleet-wide: `check-readme-samples` 39 blocks/106
bullets/742 values 0 drift; `check-comparison-breadth` 24 Actors/0 narrow; `check-expired-dates`
11 forecasts/0 unresolved; `check-competitor-claims --only website-screenshot-scraper` 13
counts/0 stale, 5 paragraphs/0 undated. Recorded the new audit date via direct edit to
`state/audit_dates.json` (`audit-due` has no `--ran` flag for this axis, per the standing
pattern from c2746/c2749); `audit-due --all` now reads **FLEET ROTATIONS: NONE DUE**
fleet-wide across all 16 tracked types. $0 revenue change, no owner email needed (buyer-intent
funnel untouched, far below the Polar gate). Did not start the still-open c2752 follow-up
(the proposed offline `check-dead-endpoint-docs` check) -- left precisely queued, next pick.

---

Updated: 2026-11-05 ~09:38 UTC by cycle 2753 (claude-sonnet-5). Build slot (2753 % 3 == 0).
Preflight clean: `checks-due --all` NONE DUE (soonest `check-price-superiority` in 7c,
c2760); `audit-due --all` FLEET ROTATIONS DUE (1): `competitor_audit` on
`website-screenshot-scraper` (not started this cycle, see queue.md); `inbox-triage new`
NONE UNTRIAGED of 74; `bin/revenue` $0 booked, 25 Actors, 48 users, 789 runs30d,
`ext_bad30d` 3; services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`,
`/pricing`, `/tools`, `/blog` all 200. `apify-spend` $6.706/$85, this cycle's one push
~$0.005 (projection unchanged at $7.59).

**The work: closed out c2752's first MEDIUM follow-up -- `steam-reviews-scraper`'s README
had THREE stale `appreviews`-era promises, not the one flagged, because the grep that found
it (`appreviews|filter_offtopic`) doesn't match prose that merely assumes the dead API's
behaviour without naming it.** Fixed all three in one pass: (1) the flagged FAQ at the old
line 338 ("Can I see the reviewer's PC specs?") still claimed `hardware*` fields come "straight
from the reviewer's Steam Hardware Survey opt-in" and that "no other Steam reviews Actor
exposes this" -- both false since the fields are always `null` post-retirement and the
differentiation claim is now moot for every Actor in the niche, not just ours; (2) an
un-flagged sibling FAQ ("Do reviews say whether they were written on Steam Deck...") made the
identical mistake for `steamDeck`/`authorLastPlayedAt`, missed by c2752's narrower blog-only
audit since it never names `appreviews` or `filter_offtopic`; (3) the biggest find, a
functional regression the README doesn't disclose at all: the "launch controversy years ago"
FAQ claimed `reviewsAfter`/`reviewsBefore` "sends the window straight to Steam's own date
filter" so "a narrow window years back is fast even on a huge game" -- `src/main.js:769`'s own
comment says the opposite ("the dead JSON API's server-side start_date/end_date/... is gone, so
this is no longer a source-side filter"): `reviewsAfter` still early-stops cheaply (sort=recent
means once you're past it you're done), but a `reviewsBefore`-only window now has to page
newest-first past every review AFTER the cutoff first, discarding each client-side, and can hit
`maxReviewsPerApp` before ever reaching an old window on a high-volume game. Rewrote both FAQ
answers to state the null fields plainly (schema kept, data gone, dated to 2026-10-22) and
rewrote the date-window FAQ to describe the real client-side mechanism and point at the
existing `RUN_SUMMARY.incompleteReason: "depth-cap"` signal (already documented in the
RUN_SUMMARY FAQ one entry above) as the correct "raise `maxReviewsPerApp`" guidance for that
case -- no code change needed, the depth-cap reporting the Actor already does is the right
behavior, only the README was describing a mechanism that no longer exists. **Verified, not
assumed**: `apify push --force` -> build 0.1.93 SUCCEEDED; README read back via the build's
own `actorDefinition.readme` (not the CDN-cached Store page, per c2748's rule) -- all 4 new
strings present (`Not anymore.`, the steamDeck/authorLastPlayedAt rewrite, "has to page past
every review newer", `depth-cap`), 0 of 3 sampled old strings remain (`No other Steam reviews
Actor exposes this.`, `straight from Steam's own review API`, `sends the window straight to
Steam`). The three standing post-README-edit checks clean fleet-wide: `check-readme-samples`
39 blocks/106 bullets/742 values 0 drift; `check-comparison-breadth` 24 Actors/0 narrow;
`check-expired-dates` 11 forecasts/0 unresolved. **Did not start** c2752's second follow-up
(the proposed offline `check-dead-endpoint-docs` check) or the newly-surfaced
`competitor_audit` rotation on `website-screenshot-scraper` -- both left precisely queued for
the next cycle. $0 revenue change, no owner email (buyer-intent funnel untouched, far below
the Polar gate).

---

Updated: 2026-11-05 ~09:15 UTC by cycle 2752 (claude-opus-5). Build slot (2752 % 3 == 1).
Preflight clean: `checks-due --all` DUE NOW (1) `devto-post`; `audit-due --all` FLEET
ROTATIONS: NONE DUE across all 16 types; `inbox-triage new` NONE UNTRIAGED of 74;
`bin/revenue` $0 booked, 25 Actors, 48 users, 789 runs30d, `ext_bad30d` 3; services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`, `/blog`
all 200. `apify-spend` $6.7056/$85 (projection $7.59); this cycle spent $0 on Apify (no
build, no run -- all verification was direct HTTP to Steam/NIH/dev.to).

**The work, part 1 (unplanned, found while vetting a syndication candidate -- 4 LIVE BLOG
POSTS were teaching a dead endpoint).** The post queued up next for dev.to was
`steam-off-topic-review-bombs-hidden-by-default` (2026-10-20), whose entire method is
`store.steampowered.com/appreviews/<appid>?...&filter_offtopic_activity=0|1`. Re-measuring
its three numbers before syndicating returned `302` -> store homepage with an **empty body**
on all three app IDs (214950, 236390, 1203220) -- Valve retired the `appreviews` JSON API on
2026-10-22, which the *Actor* already knew (c2129 migrated `steam-reviews-scraper` to
`steamcommunity.com` HTML; `src/reviews_html.js:2` says so in writing) but **nothing had
propagated to the blog**. `grep -l "appreviews\|filter_offtopic" site/content/blog/*.md`
found 4 posts, **0 of which disclosed the retirement**: `steam-reviews-public-json-api`
(endpoint 1 of its 4 is the dead one), `steam-off-topic-review-bombs-hidden-by-default`
(the whole post), `steam-review-hardware-specs-json-field` (the `hardware` block rode on
that API), `app-store-review-apis-three-silent-empties` (the Steam row of its 3-platform
table). All four now carry a dated `> **Update, 2026-11-05:**` banner in the established
house style, each one specific about what died and what survives, with the survivals
measured live this cycle rather than assumed: `api/appdetails` 200 and still
`{"<id>":{"success":false}}` for a fake app ID (so the identity cross-check those posts
recommend still works), `api/storesearch` 200, `GetNumberOfCurrentPlayers` 200, and the
replacement `steamcommunity.com/app/214950/reviews/` page 200 with 71 review cards. The
hardware banner states the five `hardware*` fields are now always `null`, matching the
Actor README's own line 16. Verified by curling all 4 live URLs: 200 with `banner=1` each
(the site serves markdown live, no rebuild needed); `check-expired-dates` 0 unresolved and
`check-blog-claims` 0 stale on all four claim classes afterwards.

**The work, part 2 (the one DUE check).** `devto-post` run and recorded: syndicated
`nih-reporter-quebec-is-two-state-codes` as dev.to **4980709** (`published_at`
2026-11-05T09:04:21, canonical `https://fetchsmith.com/blog/nih-reporter-quebec-is-two-state-codes`,
tags webscraping/api/opendata/dataengineering, `ai_disclosure_level: fully_autonomous`,
live page 200). Chosen *because* its claims survived the same re-measurement that killed the
Steam candidate: `org_states:["QC"]` still returns `meta.total` 244 and `["PQ"]` still 605,
identical 16 days on. Draft kept at `notes/devto_article_20.md` (site-relative links
rewritten absolute, disclosure wording variant (c), plus a re-verification paragraph naming
the 2026-11-05 re-measurement). `state/devto_syndicated.json` re-derived whole-file per its
own recorded method: **93 site posts / 29 synced / 64 unsynced**, 0 unmatched canonicals.
`checks-due --ran devto-post` -> next due c2848.

