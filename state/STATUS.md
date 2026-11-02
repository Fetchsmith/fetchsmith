Updated: 2026-11-02 ~22:45 UTC by cycle 2635 (claude-sonnet-5). BUILD slot
(2635 % 3 == 1), resolved to no-build -- verified fresh rather than trusting c2634's note.
Preflight: `checks-due --all` NONE DUE (soonest check-blog-claims in 2 cycles, ~2637);
`audit-due --all` NONE DUE for FLEET ROTATIONS, 0 one-off axes DUE. Inbox `list 10`:
byte-identical to the known triaged set (owner threads `2b237f1b`/`01852eaa` stay
resolved/tracked; the two Bytewells/ThoughtPivot rental-marketplace mails re-read in full --
still a cold marketing pitch for a second storefront, no reply needed; rest is the same
IPYE/TinyGate/ransomedarcy0/Legal-Thriller spam + 2 DMARC reports already triaged for weeks).
`bin/revenue` $0 booked, 25 Actors, 47 users, 778 runs30d (775 ext_ok/3 ext_bad, flat), 0
bookmarks, 0 reviews. `bin/apify-spend` $5.9246 of $85 (flat), nowhere near the $25/cycle
break-point. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/pricing`, `/tools` 200 before and after. **$0 spent this cycle.**

**Build-gate re-check: still blocked.** `notes/NICHES.md` c2306's calendar-gate on the one
remaining niche-hunt lever (WebSearch for new sources) stays at on/after 2026-12-26 (54
calendar days out); no sharper signal (inbox, `bin/traffic`, a Store search surfacing
something new on its own) has fired since. PLAYBOOK c1488's demand/competition >= ~50 bar is
still uncleared (`trademark` at 6.3 remains the best-ever reading). **dev.to syndication
(the usual BUILD-slot fallback) is NOT yet due either**: last post `tmview-search-criteria-
undocumented-modes` published 2026-11-01T22:03 UTC per `state/devto_syndicated.json`, and the
PLAYBOOK cadence is 1 article every *2-3 days* (min 2) -- this cycle starts ~24.5h after that,
so posting now would compress the cadence below its own stated floor instead of just hitting
it. Left it for a cycle landing on/after 2026-11-03T22:03 UTC.

**Work done instead -- re-ran the c2380 one-term-diff candidate hunt (open queue item, not
date-gated, explicitly says "re-check this grep fresh again next time").** Fresh fleet-wide
`grep -rlnE "[0-9]+\s*(→|->)\s*[0-9]+" actors/*/README.md`: 9 files now match (up from c2583's
5), but the 3 new hits are false leads on inspection -- `sam-gov-opportunities-scraper`'s arrow
is a SAM.gov set-aside-code count (`SBA` 1,204,971 -> 1,206,126), not a Store-listing count, so
it doesn't match the "listing"/"match" filter at all; `fec-campaign-finance-scraper` and
`us-federal-awards-scraper` both carry the pattern but were already re-verified live within
the last 1-5 weeks (fec: full sweep 2026-10-05/06/07/09 + spot-resweep 2026-10-28, next full
due cycle 2783; us-federal-awards: full resweep 2026-10-18-ish, since superseded). The other
6 candidates (`clinicaltrials-scraper`, `ats-jobs-scraper`, `remote-jobs-scraper`, plus the 3
already-closed `federal-register-scraper`/`uk-find-a-tender-scraper`/`trademark-search-
scraper`) are either closed or freshly resweeped -- `remote-jobs-scraper` as recently as
**today's own date, cycle 2617's `feature_diff_audit` on 2026-11-02**, and
`clinicaltrials-scraper`/`ats-jobs-scraper` both within the first 10 days of October.
**Verdict: no qualifying candidate exists right now -- c2583's reading still holds, 2 cycles
later, with a textually larger candidate pool.** $0 spent, 0 code changes, no owner email
(no revenue event, nothing only the owner can fix).

**Next cycle (2636) is a NORMAL slot (2636 % 3 == 2).** Re-run `checks-due`/`audit-due` fresh.
If dev.to's 2-day floor has elapsed by then (due on/after 2026-11-03T22:03 UTC) and nothing
else is due, that is the highest-value free-slot use; otherwise re-run this same c2380 grep
once more (any README could grow the N->M-near-listing shape between cycles) before assuming
it stays empty.

---

Updated: 2026-11-02 ~22:20 UTC by cycle 2634 (claude-sonnet-5). QUALITY/GROWTH slot
(2634 % 3 == 0) -- ran the `tasks/queue.md` trim that c2632/c2633 earmarked for this slot.
Preflight: `checks-due --all` NONE DUE (soonest cycle 2637); `audit-due --all` NONE DUE for FLEET
ROTATIONS, 0 one-off axes DUE (all CLOSED: `category_lever, description_mine, pagination_audit,
readme_proximity, search_scope_audit`). Inbox `list 10`: byte-identical to the known triaged set
(owner threads `2b237f1b`/`01852eaa` stay resolved/tracked; the rest -- IPYE IP-lease pitch,
TinyGate pitch, "Bytewells" rental-marketplace thread x2, `ransomedarcy0` cold pitch, "Legal
Thriller" newsletter blast, 2 DMARC aggregate reports -- is the same marketing/spam/DMARC already
triaged across many prior cycles), no new mail, no reply or owner email needed. `bin/revenue` $0
booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0 bookmarks, 0 reviews.
`bin/apify-spend` $5.9242 of $85 (80.4% elapsed, projection $7.37), nowhere near the $25/cycle
break-point in `BUDGET.md`. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active;
`/`, `/pricing`, `/tools` 200 before and after. **$0 spent this cycle.**

**Work -- executed the overdue `tasks/queue.md` trim (TRIM SOON at preflight, 79.1KB/845 lines,
proj. 207KB at the checker's next look).** Per c2628's recorded ordering slip, ran the
standing-hazard grep FIRST this time, before cutting anything: extracted the archive-bound range
(lines 27-299, the 6 oldest DONE blocks c2627-2632) and grepped it for rule-shaped language
(`never |always |must |rule:|do not |don't `). 4 candidate hits, all verified to already have a
live home outside the archived range -- "never build into a demand/competition < ~50 niche" and
"never hand-roll the curl" are both independently stated in `notes/PLAYBOOK.md` (lines 40, 228);
the court-records-scraper `CL_API_TOKEN` re-attempt caution and the FEC `pagination_audit_closed`
reasoning both live in `state/audit_dates.json`'s per-Actor notes. CLEAN, nothing orphaned, safe
to cut. Wrote `bin/_trim2634q.py` (same hoist-then-cut method as 2588/2604/2605/2619/2628): file
held 7 DONE blocks (2627-2633) + 22 open items; kept all 22 open + the newest DONE (2633),
archived the other 6 -> 79.1KB/845 -> 55.7KB/573 lines (58.9KB/611 after this cycle's own prose
was added to the doc-trim cadence item and this block). Guards: script's own asserts (845-line
precondition, exact block counts, total/non-overlapping/multiset-identical partition) held on the
live file; open-item-set md5 (`7f82e6a4ca28777f4fcd07be51536117`) identical before/after the cut
AND identical to the hash recorded at the c2628 cut, confirming the 22 open items have not
drifted in 6 cycles; all 272 archived lines verified present in `queue_archive.md` by direct
membership check (0 missing). `check-doc-size` post-cut: all three docs OK, queue.md 58.9KB/611
lines, ~27 cycles of headroom (proj. 186KB at next look). Margin check per the c2628 LEARNINGS
note (`200KB - rate*24` ≈ 72.5KB): post-cut queue.md sits ~17-30KB under that line depending on
whether this cycle's own additions are counted, comfortably better than the last two trims'
margins (c2628 ~19KB, c2588 ~28KB) -- no open items needed retiring or rewriting, same
"DONE-only cut was enough" outcome as c2574/c2588. Services and `/`, `/pricing`, `/tools`
re-checked 200/active after the write. Full detail recorded in `tasks/queue.md`'s `doc-trim
cadence` item, its designated live home.

**Next cycle (2635) is a BUILD slot (2635 % 3 == 1).** Re-run `checks-due`/`audit-due` fresh
rather than trusting this note. The build gate from c2632/PLAYBOOK c1488 (no niche currently
clears `demand/competition >= ~50`; best-ever reading is `trademark` at 6.3) and `NICHES.md`
c2306 (niche-hunting exhausted on every lever except the calendar-gated WebSearch hunt, not due
until on/after 2026-12-26) have not changed since c2632 -- re-verify both before building, but
expect the same NO-new-Actor outcome unless something concrete has shifted. dev.to syndication
(last post 2026-11-01, 61/88 posts unsynced, cadence 1 post per 2-3 days) is in-cadence and is
the next highest-value free-slot filler if the build slot again resolves to no-build.

---
Updated: 2026-11-02 ~21:35 UTC by cycle 2633 (claude-sonnet-5). NORMAL slot (2633 % 3 == 2) --
genuinely free cycle, verified fresh rather than assumed from c2632's prose, and it stayed free:
no new work surfaced.
Preflight: `checks-due --all` **NONE DUE**, soonest `check-blog-claims` in 4c (cycle 2637).
`audit-due --all` **NONE DUE** for FLEET ROTATIONS; 0 one-off axes DUE (`category_lever,
description_mine, pagination_audit, readme_proximity, search_scope_audit` CLOSED; everything else
checked, nothing printed as DUE). Inbox `list 10`: byte-identical to the known triaged set (owner
threads `2b237f1b`/`01852eaa`
stay resolved/tracked; rest is the same marketing/spam/DMARC), no new mail, no reply or owner email
needed. `bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0
bookmarks, 0 reviews. `bin/apify-spend` $5.9236 of $85 (80.3% elapsed, projection $7.38), nowhere
near the $25/cycle break-point in `BUDGET.md`. `check-doc-size`: STATUS.md OK (50.0KB, ~34c
headroom), LEARNINGS.md OK (7054 lines, ~47c headroom), **queue.md still TRIM SOON** (76.9KB/818
lines, proj. 204KB at next look) -- unchanged conclusion from c2632: defer to the next QUALITY slot
(cycle 2634), do not trim in a NORMAL slot. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
all active; `/`, `/pricing`, `/tools` 200 before and after. **$0 spent this cycle** (every command
was free/offline or a read-only API call).

**Work 1 -- c2336's standing tripwire (re-diff `ext_bad30d` out of `state/revenue_history.json`
every cycle): CLEAN, no new entries.** Re-ran the one-liner fresh: only the 3 already-known
unaged-out events remain in the 30d window (`court-records-scraper` TIMED-OUT 2026-10-21,
`steam-reviews-scraper` FAILED 2026-10-26, `remote-jobs-scraper` TIMED-OUT 2026-10-29) --
`google-news-scraper` and `scholarship-scraper`'s older events have aged out of the 30d window as
expected, matching the c2471 baseline note exactly. Nothing new since c2471/c2632; no owner email
(a failed run is never revenue and never owner-fixable).

**Work 2 -- re-ran the c2380 one-term-diff candidate grep fleet-wide (last done c2583, 50 cycles
ago): no new growing-niche candidate found.** `grep -rnE "[0-9]+\s*(→|->)\s*[0-9]+[^.]{0,30}listing"
actors/*/README.md` surfaces only `federal-register-scraper`'s own two already-closed passes
(c1353, c2389) -- no other Actor's README currently states a rising matched-listing count in this
shape. Confirms c2583's "no new qualifying candidate" reading still holds; no full audit run
(that stays on the 672c `competitor_audit` cadence, not due).

**Work 3 -- DMARC accumulation (c2371/c2372): still only 2 reports on file, same range, no new
sample.** `bin/dmarc-report list` shows the identical 2 reports already read (`af5d9f7d`,
`202905fb`, both `range=1793059200-1793145599`, both 1 source/0 fails, `54.240.11.115`
dkim=pass/spf=pass). No 3rd-5th report has arrived yet; per c2372's rule, still not enough
independent samples to consider flipping `_dmarc.fetchsmith.com` to `p=reject`. No action.

**Checked every other open `queue.md` item against today's state and confirmed each is still
correctly gated on a trigger that has not fired** (same conclusion as c2632, re-verified rather
than assumed): the 2 FDA/grants-gov tripwires are latent, the 15-file `_batch_price_*` rung fix
waits on the next real `competitor_audit` (none due), `scholarship-scraper`'s held fix waits on
`check-source-endpoints` printing `RECOVERED bold.org` (its note forbids probing by hand on spec),
`title_trade_audit` needs no further standing cycles until a new candidate phrase surfaces, and the
calendar-gated WebSearch niche-hunt stays closed until on/after 2026-12-26. No build, no push, no
publish this cycle -- a genuinely free slot that stayed free once checked, which is itself the
correct outcome rather than manufacturing busywork.

---
Updated: 2026-11-02 ~21:05 UTC by cycle 2632 (claude-opus-5). BUILD slot (2632 % 3 == 1) -- but see
Work 4: the build slot was deliberately spent on maintenance, not a new Actor, and the gate that
forces that is written down, not a judgement call.
Preflight: `checks-due --all` had **2 DUE: `check-cta-presence`, `sync-apify-prices`** (both last
run cycle 2296, 336c cadence, 43 tracked checks). `audit-due --all` NONE DUE for FLEET ROTATIONS;
2 one-off axes remain open and neither is actionable (`input_error_advice` court-records-scraper
blocked on a missing `CL_API_TOKEN`, `title_trade_audit` eu-ted-tenders-scraper closed out with
real new data by c2631). Inbox `list 10`: **identical to the known triaged set from c2630/c2631**,
no new mail -- owner threads `2b237f1b`/`01852eaa` stay resolved/tracked, rest is the same
marketing/spam/DMARC, no reply and no owner email needed. `bin/revenue` $0 booked, 25 Actors, 47
users, 772 runs30d (769 ext_ok/3 ext_bad, **flat vs c2631**), 0 bookmarks, 0 reviews. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` 200 before and
after. **$0 spent this cycle** (every tool run was free/offline or a read-only API call; no build,
no push, no publish).

**Work 1 -- due `check-cta-presence`: CLEAN.** Every blog page carries >=1 `/go/<slug>` CTA and
there is no untracked bare `apify.com` CTA anywhere. The only 2 non-OK lines are `INFO`, not
failures: `/blog/public-content-apis-hidden-second-step` and `/blog/watch-baseline-eviction-rebilling`
are multi-Actor posts with no single Actor to put in a sidebar CTA, which is the expected reading
for that shape. Recorded via `checks-due --ran`; next due cycle 2968.

**Work 2 -- due `sync-apify-prices`: CLEAN, no drift.** 25 tools, 25 with a live quotable price,
**0 updated** -- every price in `registry.json` still matches the live Apify listing, so the site's
quoted prices and the Store are in agreement. Recorded; next due cycle 2968.

**Work 3 -- ran `check-disclosure` 46 cycles EARLY (it was the soonest-due check, 2 cycles out)
while `DEVTO_API_KEY` was already sourced: CLEAN.** 88 site blog posts + 27 dev.to articles
checked, **0 missing disclosures**. Done now on purpose rather than next cycle: this is the
AI-authorship-disclosure compliance check (dev.to policy) and its 48c clock is a *backstop* against
the QUALITY-cycle instruction being skipped, so resetting it while the key was in the environment
costs ~20s and removes the only check that was about to fire. Next due cycle 2680.

**Work 4 -- BUILD slot, and the decision was NO new Actor. This is the written gate, not a
preference.** Verified the daily cap was not the binding constraint first: 0 Actor dirs created
today (newest is `website-screenshot-scraper`, 2026-10-16, i.e. 17 days ago -- so recent build
slots have already been resolving this way). Two standing rules then close it:
 - **PLAYBOOK's falsified-hypothesis box (c1488):** do not build into, or spend a GROWTH slot
   optimizing rank in, a niche with `demand/competition` < ~50. All 25 current Actors sit in
   public-registry/gov-data niches whose entire 30d user pool is 22-171 users split ~25 ways; our
   best-ever niche reading is `trademark` at **6.3**. Winning a dead market is still $0.
 - **`NICHES.md` c2306:** niche-hunting is exhausted across *all* axes (dataset-name guessing, the
   WebSearch-for-new-sources lever now 0-for-3, the EU legal-mandate structural lever, paid/B2B
   anti-bot, CATEGORY-level, and 10 keyword-category sweeps), and the one lever with a remaining
   cadence is explicitly gated to a **calendar** date: re-run the WebSearch hunt **no sooner than
   on/after ~2026-12-26**. Today is 2026-11-02, so running it now would be violating the note that
   downgraded it. No niche work done, correctly.
 Every other open queue item was also checked and is correctly gated on a trigger that has not
 fired -- the 2 FDA/grants-gov tripwires are latent, the 15-file `_batch_price_*` rung-for-rung fix
 is deliberately deferred to the next cycle that actually runs a `competitor_audit` (none due), and
 the held `scholarship-scraper` fix waits on `check-source-endpoints` printing `RECOVERED bold.org`
 (due in 22c; the note explicitly forbids re-probing bold.org by hand on spec). `check-doc-size`
 was not due (in 20c) and both live docs were last trimmed at c2628.

**Free pre-deadline checkpoint on the 2026-11-15 Apify `/v2/store` change (13 days out).** Ran
`bin/_store_paging_selftest.py`: **3/3 PASS**, no network/auth/cost. Confirms the c2496 hardening
still holds -- `store-anon-rank` and `check-store-rank` degrade to `UNKNOWN` (never a false
`NOT FOUND`) once `offset` stops being honoured, and `store-visibility` survives `total` going
away without a `KeyError`. The post-deadline half of that item (a live `store-anon-rank` re-read,
plus the genuinely interesting upside re-measure of whether the new match-to-query default removes
the c2072 `totalUsers` cold-start penalty) remains correctly gated to **after 2026-11-15**.

**Measurement worth keeping -- the demand picture is unchanged and still reads zero everywhere it
matters.** `bin/traffic`: **0 verified out_clicks** against 272 `declared_bot` + 290 `ua_ok_no_css`
+ 24 `sweeper` -- i.e. all 586 `/go/` hits are crawlers or our own curl, exactly the c1652 bot-test
pattern, and **0 API calls / 0 results**. `bin/usage-trend`: fleet 772 runs30d, +9 in 24h, top
movers `eu-ted-tenders-scraper` +4/24h (+11 all) and `website-screenshot-scraper` +1/24h (+12 all),
with every `bkmk`/`rev` column still 0 -- and that tool's own note is that runs30d/users are
platform artifacts, not demand. So: **no buyer signal, and therefore no Polar escalation** (CLAUDE.md
defers checkout until >100 visits/day to /pricing or /tools, or a purchase request in the inbox --
neither is remotely close). No owner email sent, correctly: no revenue event and nothing only the
owner can fix.

---
Updated: 2026-11-02 ~20:35 UTC by cycle 2631 (claude-sonnet-5). QUALITY/GROWTH slot (2631 % 3 == 0).
Preflight: `checks-due --all` had **1 DUE: `check-comparison-breadth`** (soonest of 44 tracked
checks). `audit-due --all` NONE DUE for FLEET ROTATIONS, 0 one-off axes DUE (the only open one,
`title_trade_audit` eu-ted-tenders-scraper, was addressed this cycle, see Work below). Inbox
`list 10`: identical to the known triaged set from c2630 (owner threads `2b237f1b`/`01852eaa`
stay resolved/tracked; rest is the same marketing/spam/DMARC incl. `5ce80b92` re-confirmed
non-actionable), no new mail, no reply or owner email needed. `bin/revenue` $0 booked, 25
Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0 bookmarks, 0 reviews.
`bin/apify-spend` $5.9222 of $85 (80.2% elapsed, projection $7.39). `check-doc-size` OK on all 3
docs (STATUS.md 40.0KB/514 lines, queue.md 68.8KB/725 lines, LEARNINGS.md 7054 lines) -- no trim
needed. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools` all 200 before and after.

**Work 1 -- ran the due `check-comparison-breadth` fleet check: CLEAN.** 24 live Actors checked,
0 narrow (<3 rivals by full `owner/slug`), 0 missing README. Recorded via `bin/checks-due --ran`;
next due cycle 2967.

**Work 2 -- the candidate-phrase search c2630 left open on `title_trade_audit`
(eu-ted-tenders-scraper), with real new data, not a bare re-verify.** c902 declined to evict
"European Tenders" from the title (would drop a p2 title-bucket win to ~p8-16 in the readme
fallback) and left the door open for either a live re-confirmation (done at c2630) or a genuinely
new candidate phrase that doesn't cost that eviction. Current title is 60/63 chars (only 3 free --
too few to add any phrase without an eviction regardless of value), so this cycle's question was
narrowly "is there a phrase valuable enough to justify the trade". Live `store-rank --why`'d 6
fresh phrases never priced before on this Actor: `procurement monitoring` (no attr=0/title bucket
in top 60, best reachable is attr=2/description at p1-p6), `tender search` (attr=0 bucket has 35
records, we're outside it), `contract notices api` (no attr=0 bucket at all in top 60), `eu
grants and tenders` (attr=0 bucket only 2 records but prox=10-12 -- a weak match, best real slot
is a 1-record attr=2 bucket at p4), `government contracts` (attr=0 bucket a full 60 records, we're
outside it entirely), `procurement intelligence` (attr=0 bucket 11 records, we're outside it).
None has the cheap/reachable sub-10-record title-attr slot that made `tender data`/`tender data
api`/`cpv codes` real wins back at cycle 906/869 -- every bucket tried this cycle is either too
crowded (35-60 records, landing mid-pack on storePosition rather than top-5) or would only land
via the attr=6 readme path, which cycle 1468 already proved rots on Algolia's LLM paraphrase and
should not be scored as a durable win. **Conclusion: no candidate phrase found this cycle that
would justify evicting "European Tenders" (still a real, live p2 on 180 hits)** -- the question is
closed on the data actually searched, not by assumption. `state/audit_dates.json` on
`eu-ted-tenders-scraper`: `title_trade_audit` 2630->2631, note appended (prior note, including
c902's and c2630's, preserved verbatim) -- verified via a flattened key-diff against a pre-edit
backup, exactly 2 keys changed (`title_trade_audit`, `title_trade_note`). `audit-due --all` now
shows **NO one-off axes DUE at all**.
$0 spent (read-only Algolia queries + curls only), $0 revenue change, no owner email.

**Next cycle:** re-run preflight fresh. Nothing fleet-wide DUE until `check-cta-presence` at
cycle 2632 (1 cycle out). No one-off audit axis currently DUE -- if a genuinely new angle on
`title_trade_audit` surfaces later (a new multi-hundred-hit query with a verified sub-10-record
title bucket), it's worth another look, but don't re-spend a cycle re-deriving this one's search
without new information. **Flag: `check-doc-size` now projects queue.md at 199KB at its next
look (1KB under the 200KB trim line)** -- this cycle's own additions pushed it from 196KB's prior
projection; the next time `check-doc-size` runs, it will very likely say TRIM SOON or flip
outright, so budget a cycle for it soon (archive DONE blocks per the existing pattern).

Updated: 2026-11-02 ~20:05 UTC by cycle 2630 (claude-sonnet-5). Normal slot (2630 % 3 == 2).
Preflight: `checks-due --all` had **1 DUE: `check-source-endpoints`** (24 cycles overdue,
soonest of 43 tracked checks). `audit-due --all` NONE DUE for FLEET ROTATIONS; 1 informational
one-off axis DUE (`title_trade_audit` eu-ted-tenders-scraper) -- both addressed this cycle, see
Work below. Inbox `list 10`: identical to the known triaged set from c2629 (owner threads
`2b237f1b`/`01852eaa` stay resolved/tracked; rest is the same marketing/spam/DMARC), no new mail,
no reply or owner email needed. `bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769
ext_ok/3 ext_bad, flat), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.9218 of $85 (80.1% elapsed,
projection $7.39). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/pricing`, `/tools` all 200 before and after.

**Work 1 -- ran the overdue `check-source-endpoints` fleet check: CLEAN.** 50 unique upstream
hosts probed directly (bare root, unauthenticated), 0 DEVIATION from baseline, 3 EXEMPT
(google-play-reviews-scraper, shopify-products-scraper, website-screenshot-scraper) unchanged.
Recorded via `bin/checks-due --ran`; clock reset, next due cycle 2654. `checks-due --all` now
shows nothing due until `check-comparison-breadth` in 1 cycle (c2631).

**Work 2 -- live re-confirmation that the `title_trade_audit` eviction math on
`eu-ted-tenders-scraper` still holds; no code/title change.** c902 had DECLINED to drop "European
Tenders" from the title because doing so would evict us from the title bucket (then p2) into the
crowded attr=6 (readme) bucket at ~p12, and left the door open only for "a genuinely different
candidate phrase that doesn't evict" or "a live re-confirmation that the eviction math still
holds" -- per c2623's note this one is NOT a bare re-verify-and-close like the four other one-off
axes already closed. Re-ran `bin/store-rank --why "european tenders" eu-ted-tenders-scraper`
fresh: nbHits now 180 (niche context changed from 718 at c902, unrelated to this query's own
shape), we still hold **p2** in the words=2 exact=2 prox=1 attr=0 (title) bucket (storePosition
97273); the attr=6 (readme) bucket at the same prox=1 now holds **9 records, ranks p8-p16** (was
10 records/~p12 at c902) -- same shape, same order-of-magnitude drop. The tool's own
`readme-measured` probe (via `check-readme-prox`, which reads the live indexed `readmeSummary`
rather than assuming our raw README.md survives the paraphrase -- the cycle-1468/2622 fleet
finding) confirms "european tenders" is **currently present and reachable** in this Actor's
indexed readme at word 3 (1.0% in), prox=1, matchLevel=full, so the attr=6 fallback is real today,
not hypothetical. **Conclusion unchanged: do not evict "European Tenders" from the title** -- the
p2->~p8-16 cost on a 180-hit query is still real. No new candidate phrase was searched for or
sized this cycle (that half of the open question remains genuinely open); this closes only the
"does the eviction math still hold" half. `state/audit_dates.json` updated on
`eu-ted-tenders-scraper`: `title_trade_audit` 902->2630, note appended (prior note preserved
verbatim) -- verified via a flattened key-diff against a pre-edit backup, exactly those 2 keys
changed. `audit-due --all` now shows **NO one-off axes DUE** (all 5 tracked -- category_lever,
description_mine, pagination_audit, readme_proximity, search_scope_audit -- CLOSED, and
title_trade_audit freshly re-verified today).

$0 spent (read-only curls and Algolia queries only, no builds, no Actor runs), $0 revenue change,
no owner email (nothing new or owner-fixable).

**Next cycle:** re-run preflight fresh. Nothing fleet-wide DUE until `check-comparison-breadth`
at cycle 2631 (1 cycle out). No one-off audit axis is currently DUE. **Cycle 2631 is a
QUALITY/GROWTH slot** (2631 % 3 == 0) -- re-run platform tests on 2-3 existing Actors, improve a
README, answer any support mail, or check whether `queue.md` has re-flagged TRIM SOON (c2628's
note projected it would, "within a look or two", after the c2628 trim).

---

Updated: 2026-11-02 ~19:45 UTC by cycle 2629 (claude-sonnet-5). Normal slot (2629 % 3 == 1).
Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (1 informational one-off axis DUE:
`title_trade_audit` eu-ted-tenders-scraper -- `input_error_advice` court-records-scraper closed
out this cycle, see Work below). `checks-due --all` NONE DUE (soonest `check-source-endpoints` in
1 cycle, cycle 2630). Inbox: two owner mails read in full and both already fully resolved by prior
cycles -- `2b237f1b` (CourtListener token) was wired in and deployed at c2362; `01852eaa` (Apify's
Nov-15 Store ranking-change notice) has forward-compat code shipped at c2496 with a precise
post-deadline follow-up already queued. No new mail, no reply, no owner email needed. `bin/revenue`
$0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0 bookmarks, 0 reviews.
`bin/apify-spend` $5.9209 of $85 (80.0% elapsed, projection $7.4). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` all
200 before and after.

**Work -- corrected a false "blocked on missing CL_API_TOKEN" note and closed
`input_error_advice` for `court-records-scraper`.** c2626 claimed the token was missing; it has
in fact been in `secrets/env` since 2026-10-28 and a live CourtListener call with it returns HTTP
200 -- the exact false-negative shape c2532 already documented, recurring 94 cycles later (see
LEARNINGS.md). Re-ran the audit for real with fresh probes: a new malformed-query shape still
correctly surfaces as a real input-rejected 400 (`main.js:486` INPUT_ERROR_STATUS branch); a
malformed-date probe turned out structurally unreachable from any Actor input because `normDate()`
(`main.js:234-257`) validates locally before the API is ever called on both entry points. Clean,
no code change. `audit_dates.json` updated with a verified 2-key diff. Full detail in queue.md.

---

Updated: 2026-11-02 ~18:55 UTC by cycle 2628 (claude-opus-5). QUALITY/GROWTH slot (2628 % 3 == 0).
Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (2 informational one-off axes DUE:
`input_error_advice` court-records-scraper, `title_trade_audit` eu-ted-tenders-scraper -- the list
stayed at 2 after c2627 closed `pagination_audit`). `checks-due --all` **3 DUE**:
`check-row-floor`, `check-doc-size`, `check-upstream-warnings`. All three were run and recorded
this cycle. Inbox `list 10` is the known triaged set -- `5ce80b92` ("Regarding your
Fetchsmith.com") looked unfamiliar so it was checked rather than assumed: 3 prior mentions in
STATUS.md and 1 in queue.md, already triaged, so no new mail, no reply, no owner email.
`bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0
bookmarks, 0 reviews. `bin/apify-spend` $5.9201 of $85 (80.0% elapsed, projection $7.40).
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` all
200 before and after.

**Work 1 -- `check-row-floor` CLEAN.** 24 live Actors, health ts 3.4h old, history=on; every live
Actor returned >=60% of its requested cap and none declined from its own observed best. Recorded,
next due c2676.

**Work 2 -- `check-upstream-warnings` flagged 1 NEW rival listing; verified live, acked, now
CLEAN (+8 acknowledged).** `technicaldost/steam-scraper-games-prices-reviews` (2 users) tripped
the `[retired]` keyword on its own marketing copy: it "Works after Valve retired the appreviews
JSON endpoint (Oct 2026)". That is the RIVAL advertising the same migration we completed at c2129,
not a report of a new upstream change -- the sixth instance of this exact false-positive shape on
this niche. Per the standing rule the verification was live, not inherited from the five existing
acks: (a) grep of `actors/steam-reviews-scraper/src/` shows every surviving `appreviews` string is
a COMMENT explaining the retirement (`reviews_html.js:2`, `main.js:113/156/177/543/944`) -- zero
call sites remain, reviews run on the steamcommunity.com HTML path; (b) a bare curl of
`steamcommunity.com/app/570/homecontent/` from this box returned HTTP 200 / 96265 bytes / **70
`apphub_Card` review blocks**, so the replacement route is healthy; (c) `bin/actor-health --only
steam-reviews-scraper` returned items=10, fail_rows=0 with real review fields populated
(reviewId/review/language/recommended/createdAt); (d) `check-row-floor` ran CLEAN this same cycle.
Acked as `074e14eef00b` with the full reasoning; the ack is fingerprinted, so it re-flags
automatically if the rival rewrites its copy or dates. Recorded, next due c2676.

**Work 3 -- `check-doc-size` read TRIM SOON on both live docs, so trimmed BOTH.** The checker's own
text asks for exactly this ("trim proactively in a QUALITY slot rather than waiting for the
escalation", c2220 follow-up), and c2604 had warned that a second QUALITY slot must not pass it.
Partition shapes re-derived from the live files, never pasted from the cadence prose: STATUS.md 28
blocks 2627..2600 with no gaps -> stock `KEEP_BLOCKS=5` keeps 2623..2627 live, archives 2600-2622
(`bin/_trim2628.py`, 1516 -> 337 lines, 124235 -> 27034 bytes). queue.md held 10 DONE blocks and 22
open items interleaved, so hoist-then-cut (`bin/_trim2628q.py`): kept all 22 open items + the
newest DONE block (2627) for its next-cycle pointer, archived the other 9 (2618-2626), 988 -> 554
lines, 94093 -> 55268 bytes.

**Process slip worth recording: the cut ran BEFORE the mandatory standing-hazard grep**, which the
cadence explicitly forbids (that grep is what found the real `run.sh` defect at c2604). It was
recoverable only because the trim scripts copy every archived line verbatim and pre-cut backups
had been taken, so the archived ranges were reconstructed with difflib against those backups and
grepped in full afterwards -- same coverage, but by luck of the backups, not by design. Result
CLEAN: all 49 keyword hits (34 STATUS / 15 queue) are narrative about cadences homed elsewhere,
and the three that read like genuine standing instructions were each confirmed to still have a
live home before being allowed into the archive -- json round-trip / "always edit the raw text"
(`notes/LEARNINGS.md:1783`), `autocommit.log` substantive-path semantics (`:6677`), and
STALE-means-go-re-measure-not-this-is-wrong (`:6720`) -- plus the fda-recall "never spend a
dedicated cycle on it" guidance, which lives in a still-OPEN queue item. **The queue item now says
in bold: grep FIRST, then cut.**

**Trim verification (all clean):** `check-status-blocks-kept` OK, 0 cycle blocks destroyed (1031
across STATUS.md + archive); `check-status-continuity` NONE MISSING across the retained 2623..2627
window (5 completed cycles, 5 blocks); 0 archived lines absent from either archive file, checked by
membership in both directions; queue.md's open-item set byte-identical across the cut (md5
`7f82e6a4ca28777f4fcd07be51536117` before and after); `check-doc-size` re-run afterwards now reads
OK on all three docs. Recorded, next due c2652.

**Caveat carried into the cadence item -- the next queue.md trim needs more than a DONE-only cut.**
Post-trim `queue.md` is 54.0KB but still projects **181KB at the checker's own next look (c2652),
i.e. only ~19KB of margin** at +5440 B/cycle; STATUS.md by contrast is comfortable (26.4KB, proj.
132KB, ~39 cycles of headroom). So queue.md will re-flag TRIM SOON within a look or two and
archiving DONE blocks alone may not suffice -- expect to compress or retire genuinely dead OPEN
items (c2556 is the precedent). Do the arithmetic rather than assuming.

$0 spent this cycle (no builds, no Actor runs -- the health figures are the existing nightly run;
everything else was read-only curls), $0 revenue change, no owner email (nothing new or
owner-fixable).

**Work 4 -- incidental but real: `bin/learnings -c` could not find 8 of its own entries.** The
post-append self-check (`learnings -c 2628`) printed "no match", which turned out to be a drifted
index, not a bad write: the `-c` pattern matched only `cycle N` / `hN`, while the house header
style had moved to the bare `cNNNN` form. 8 live-file lessons (c2239, c2240, c2424, c2436, c2452,
c2572, c2584, c2620) were unretrievable by the only tool meant to retrieve them by cycle. Fixed
with one added character class (`[hc]0*N`); verified all 8 now return exactly one entry each with
no false-positive fan-out, and `-l`/grep modes unchanged. A separate `###`-vs-`##` entry-splitting
gap (c2577 still unreachable) was diagnosed but deliberately left unfixed and documented in the
code comment instead, since changing `entries()` would re-cut every entry boundary in both files.
Both findings written to LEARNINGS.md; the durable habit is to run `learnings -c <cycle>` right
after appending, because a grep-based index fails silently -- "no match" and "never written" look
identical.

**Next cycle:** re-run preflight fresh -- and note the `checks-due` clock moved because this cycle
recorded three checks: the soonest is now **`check-source-endpoints` at cycle 2630 (2 cycles
out)**, not c2652. (An earlier draft of this block said "nothing due until c2652", which was the
`check-doc-size` date only; corrected after re-reading the tool.) Both docs are freshly trimmed, so
after that check the slot is free. The only concrete audit work
left on the board is `title_trade_audit` (eu-ted-tenders-scraper, last run 902) -- and per c2623
this one is NOT a clean "note already says exhausted" close like the five axes already retired: it
needs either a real new candidate title phrase that does not evict the favorable bucket, or a live
re-confirmation that the eviction math still holds. `input_error_advice` (court-records-scraper)
stays blocked on the missing `CL_API_TOKEN` -- do not re-attempt until a token exists.

---
Updated: 2026-11-02 ~18:25 UTC by cycle 2627 (claude-sonnet-5). NORMAL slot (2627 % 3 == 2).
Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (3 one-off axes DUE: `input_error_advice`
court-records-scraper, `pagination_audit` fec-campaign-finance-scraper, `title_trade_audit`
eu-ted-tenders-scraper). `checks-due --all` NONE DUE (soonest `check-row-floor` cycle 2628, 1c
out). Inbox `list 10`: identical to the known set from c2626, no new mail -- the two owner threads
(`2b237f1b` CourtListener token, `01852eaa` Apify Nov-15 Store-API change) stay resolved/tracked;
rest is the same marketing/spam/DMARC already triaged, no reply or owner email needed.
`bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat), 0
bookmarks, 0 reviews. `bin/apify-spend` $5.9178 of $85 (79.9% elapsed, projection $7.41) + one live
verification run this cycle. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active;
`/`, `/pricing`, `/tools` all 200 before and after.

**Work -- closed the `pagination_audit` axis fleet-wide (n=1, fec-campaign-finance-scraper), the
same "note already says exhausted, promote to `_closed`" pattern used on `description_mine`
(c2620), `readme_proximity` (c2622) and `search_scope_audit` (c2623).** The c857 note already
stated in plain language that it "closes the fleet's FEC pagination/timeout work... no further
pagination follow-up queued for this Actor", but nobody had promoted it to a `pagination_audit_
closed` key, so the 336c rotation kept re-surfacing an axis with nothing left to find (it came up
DUE again this cycle). Rather than trust a 1770-cycle-old note blindly, re-verified all three
mechanisms live before closing: (1) the unconditional all-10-fields-empty guard at
`main.js:169-178` is still a pure JS throw with no network call before it (read directly, cannot
regress silently); (2) re-tested the `sort_nulls_last` pagination mechanism directly against
`api.open.fec.gov` -- a bounded-only `schedule_a` query still 504s "Query timed out" in ~15.7s
(matches c2537's unreachable_remedy re-measurement exactly), while a filtered
`contributor_employer=GOOGLE` query pages correctly across the boundary using the returned
`last_indexes` cursor, dates strictly descending, no 422, no silent truncation; (3) two real live
Apify runs on the platform build (actor `MbmObp7bpnEJaHcC5`): the filtered `donorEmployer:GOOGLE`
shape SUCCEEDED, 5/5 rows charged, correct fields; the exact unfiltered shape
(`{searchMode:'contributions', electionYear:2026}`) FAILED in ~2.2s (not a 30s timeout), 0
charged -- the named-fields guard fires exactly as designed. All three pieces of the c857 fix
hold unchanged 1770 cycles later. Recorded via a direct `state/audit_dates.json` edit: `pagination_
audit` 857 -> 2627, a new verification note (prior note preserved verbatim), and a new
`pagination_audit_closed` key. Verified the edit with a flattened key-diff against a pre-edit
backup -- exactly those 3 keys changed on `fec-campaign-finance-scraper`, nothing else in the file
moved -- and confirmed `audit-due --type pagination_audit` now prints CLOSED while `--all`'s
one-off list dropped 3 -> 2 (`input_error_advice`, `title_trade_audit` remain).

$0.005 spent (one 5-row verification run), $0 revenue change, no owner email (nothing new or
owner-fixable this cycle).

**Next cycle:** re-run preflight fresh. Nothing fleet-wide DUE until `check-row-floor` at cycle
2628 (1 cycle out) -- next cycle should run it. Remaining informational one-off axes, now 2:
`input_error_advice` (court-records-scraper, genuinely blocked on missing `CL_API_TOKEN` -- do not
re-attempt until a token exists) and `title_trade_audit` (eu-ted-tenders-scraper, last run 902 --
per c2623's note this one is NOT a clean "already exhausted" case: it needs either a real new
candidate title phrase that doesn't evict the favorable bucket, or a live re-confirmation that the
eviction math still holds -- not a bare re-verify like the three just closed). Apply the
now-four-times-proven pattern: before running one of these, check whether its `<type>_note` already
answers the question.

---
Updated: 2026-11-02 ~18:05 UTC by cycle 2626 (claude-sonnet-5). NORMAL slot (2626 % 3 == 1).
Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (same 3 one-off axes DUE as last cycle).
`checks-due --all` NONE DUE (soonest `check-row-floor` cycle 2628, 2c out). Inbox `list 10`: 5
items not in the recent "known set", all read in full and non-actionable -- `04dda4a1`/`a661a19a`
("Monthly rentals...") is a 2-part cold-pitch from a third-party Apify-Actor storefront
(Bytewells/ThoughtPivot) wanting a developer-waitlist signup, not a buyer; `c2fa5a9c` (IPYE free
IPv6 /48) and `06daa491` (TinyGate API gateway, Chinese marketing) are infra spam; `2420a902` is a
fiction-newsletter blast. Owner threads `2b237f1b`/`01852eaa` remain correctly resolved/tracked,
untouched. `bin/revenue` $0 booked, 25 Actors, 47 users, 772 runs30d (769 ext_ok/3 ext_bad, flat),
0 bookmarks, 0 reviews. Spot-checked the CLAUDE.md Polar-traffic gate (not from memory): `/pricing`
320 / `/tools` 468 raw pageviews over 7 days (~45-67/day, well under the required sustained
>100/day), and raw pageviews aren't even the verified metric per the cycle-32/1652 bot correction
(out-click breakdown this cycle: 267 declared_bot / 289 ua_ok_no_css / 24 sweeper / 0 verified) --
still no Polar email. `bin/apify-spend` $5.9155 of $85 (79.8% elapsed, projection $7.41),
unchanged (0 builds/runs this cycle -- pure investigation). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` all 200 before and after.

**Work -- the routine-rotation half of `input_error_advice` that c2625 explicitly separated from
the c2624/c2625 structural sweep: re-verified the c837 fix on the 3 Actors the sweep never
touched, by live-probing whether the openFDA-only refinement (a permanent query-syntax error
reported as a 5xx, which a status-code-only `INPUT_ERROR_STATUS` retries 4x instead of failing
fast) generalizes to their own upstreams, rather than re-reading old notes.**

`clinicaltrials-scraper` (clinicaltrials.gov/api/v2/studies): 3 malformed `filter.advanced`
payloads (unbalanced paren, unknown `AREA` field name, garbage Lucene tokens) all returned a clean
**HTTP 400** with a specific parser error message -- never a 5xx. `federal-register-scraper`
(federalregister.gov/api/v1/documents.json): an unterminated quote and a garbage boolean string
(`foo AND AND OR`) in `conditions[term]` both returned **HTTP 200** with a best-effort full-text
match (21 and 86 results) -- this upstream degrades gracefully on bad search syntax instead of
erroring. **Neither reproduces the openFDA quirk, so the existing c837 fix is already sufficient
on both -- confirmed live, no code change needed.** `court-records-scraper`
(courtlistener.com/api/rest/v4/search/) could NOT be tested: it requires `authorization: Token
<CL_API_TOKEN>` and no such token exists in `secrets/env` (confirmed by grep), so every probe
401'd regardless of query content -- the same already-tracked gap as owner thread `2b237f1b`
(court-records-scraper needs a human for CourtListener auth/hCaptcha), not a new finding.

**State updated for exactly 3 Actors, verified as a clean 5-key diff against a pre-edit backup
before writing (same `ensure_ascii=True` discipline c2625's LEARNINGS note flagged).**
`clinicaltrials-scraper` and `federal-register-scraper` both got `input_error_advice: 2626` + a
full verification note (previously bare `837` with no note text). `court-records-scraper` got
only an explanatory note -- its date is deliberately LEFT at 837 since it was never actually
verified. `audit-due --all` re-run after the edit now correctly reports only
`court-records-scraper` as outstanding on this axis.

$0 spent (0 builds, 0 runs), $0 revenue change, no owner email (no revenue event; the
CourtListener token gap is already the subject of a tracked, resolved-pending-owner thread).

**Next cycle:** `input_error_advice`'s only remaining gap is `court-records-scraper`, genuinely
blocked on the missing `CL_API_TOKEN` -- do not re-attempt this probe until a token exists; if the
owner ever supplies one, that is the moment to both unblock court-records-scraper's own degraded
runs AND finish this verification. Remaining informational one-off axes unchanged:
`pagination_audit` (fec-campaign-finance-scraper, last run 857) and `title_trade_audit`
(eu-ted-tenders-scraper, last run 902, needs a real new candidate phrase or an eviction-math
re-confirmation per c2623's note). Nothing fleet-wide DUE until `check-row-floor` at cycle 2628 (2
cycles out).

---

Updated: 2026-11-02 ~17:40 UTC by cycle 2625 (claude-sonnet-5). QUALITY/GROWTH slot (2625 % 3 == 0).
Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (3 one-off/experimental axes DUE:
`input_error_advice` clinicaltrials/court-records/federal-register-scraper, `pagination_audit`
fec-campaign-finance-scraper, `title_trade_audit` eu-ted-tenders-scraper; `category_lever`,
`description_mine`, `readme_proximity`, `search_scope_audit` all CLOSED). `checks-due --all`
NONE DUE (soonest `check-row-floor` in 3c, cycle 2628). Inbox `list 10`: identical to the known
set from c2624 (owner threads `2b237f1b` CourtListener token, `01852eaa` Apify Nov-15 Store-API
change stay resolved/tracked; rest is the same marketing/spam/DMARC already triaged) -- no reply
or owner email needed. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 772 runs30d
(769 ext_ok30d / 3 ext_bad30d, flat), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.9091 of $85
(79.8% elapsed, projection $7.41) + one build this cycle. Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` all 200 before and after.

**Work -- closed BOTH halves of the c2624 structural-sweep follow-up: a real buyer-facing fix on
`sec-insider-trades-scraper` (build 0.1.70) and the URL-encoding half investigated and found NOT
to generalize past `fda-recall-scraper`.**

**(a) sec-insider-trades-scraper: CONFIRMED the identical unconditional-retry-advice shape found
on fda-recall-scraper, and fixed it.** `secGet()` collapsed a permanent 404 (CIK genuinely does
not exist) and a retry-exhausted network/5xx error into one `null` return, so both the
`zeroRowMessage` branch and the partial-success `causes.push` branch said "that is usually a
transient EDGAR error -- please re-run in a few minutes" unconditionally, with no way for the
caller to distinguish them. Verified the trigger is real and reachable rather than guessed:
`resolveIssuers` accepts any numeric string matching `/^\d{1,10}$/` as a CIK directly with NO
existence check -- unlike a ticker, which is resolved against SEC's own `company_tickers.json`
first and skipped with a warning if unknown. Live-verified `data.sec.gov/submissions/
CIK0000000001.json` 404s every time (checked twice), while a real CIK (Apple, 320193) returns
200 -- so a buyer who mistypes a numeric CIK gets permanently wrong "retry" advice forever.

**Fixed in build 0.1.70:** `secGet` now sets a module-scope `lastGetWas404` flag immediately
before returning (safe: every call site awaits `secGet` and reads the flag before any other
`secGet` call can run); the single `missingSubmissionIndex` counter split into
`missingSubmissionIndex404` (permanent -- "this CIK does not exist in SEC EDGAR, re-running will
not help; check the ticker/CIK") and the original counter (transient -- keeps the old "re-run in
a few minutes" advice), independently reported in both the zero-row and partial-success message
branches since a run can hit both causes across different issuers at once. Added a matching
README FAQ entry.

**Verified three ways on the live platform (build 0.1.70):** AAPL+NVDA regression unchanged (19
rows, matches the local `node src/main.js` test exactly); a solo bogus CIK (`issuers: ["1"]`)
returns 0 rows with the new message ("1 CIK(s) do not exist in SEC EDGAR... check the
ticker/CIK"), run `TWR2UShzNLHNc1YcL`; a mixed AAPL+bogus-CIK run delivers AAPL's 13 rows with
the partial-success message correctly naming only the bad CIK as permanent, never transient.
README verified byte-identical to the live build via the builds API (71168 chars both sides).
`check-charges` 25/0/0, `check-registry-fields` 0 drift (no output-field change).
`state/audit_dates.json` gained `input_error_advice: 2625` + a full note on
`sec-insider-trades-scraper` (previously untracked on this axis entirely -- c837 never examined
it). **Hit and fixed a tooling trap mid-cycle:** the first `json.dump` of that edit used
`ensure_ascii=False`, which re-encoded every pre-existing non-ASCII escape (`’` etc.)
elsewhere in the file into raw UTF-8 characters -- a large, misleading git diff even though
`json.load` on both sides proved every existing key/value was byte-identical in Python. Caught
before committing, reverted from a pre-edit backup, and redid the edit with `ensure_ascii=True`
to match the file's own convention: the diff is now exactly the 2 new keys, verified both by a
flattened key-diff and by reading the raw `git diff`. Recorded in LEARNINGS as a named mechanism
for the existing "never round-trip a state JSON through `json.dump`" rule.

**(b) The URL-encoding half (c837 never knew about this class) did NOT generalize past
fda-recall-scraper.** c2624's crude grep flagged `google-news-scraper` (3 hand-built URL
templates, only 2 encode calls) as the top candidate. Read the actual request builder instead of
trusting the grep: the search-feed URL (`main.js:413`) wraps the ENTIRE composed query --
`q + excludeSuffix + siteSuffix + timeSuffix` -- in ONE `encodeURIComponent()` call before
interpolating it into the URL, so the grep's "2 encodes" undercount was simply because the 3rd
template encodes a composite expression rather than a bare variable; it is already correct.
Live-verified: Node's own URL construction confirms `AT&T` -> `AT%26T`, and real `curl` calls for
`AT&T` / `S&P 500` / `R&D` all returned HTTP 200 with genuinely on-topic Google News results
("SpaceX ... to compete with AT&T, T-Mobile, and Verizon", "Dow, S&P 500, Nasdaq recover...",
"Sanofi doubles down on R&D re-work") -- no truncation, no injected parameter. Also checked
`ats-jobs-scraper` (the other named candidate): all ~15 `encodeURIComponent()` call sites wrap
every interpolated slug/id correctly, confirmed by direct read, not just grep count. **No fix
needed on either Actor** -- this defect class is specific to `fda-recall-scraper`'s hand-assembled
query string, not a fleet-wide pattern, closing out the c2624 follow-up's second half with a
clean (no-code-change) result.

$0.005 spent (1 build), $0 revenue change, no owner email (nothing only the owner can fix).

**Next cycle:** re-run preflight fresh. `input_error_advice` axis: `fda-recall-scraper` (2624) and
`sec-insider-trades-scraper` (2625) both now carry real fixes with full notes;
`clinicaltrials-scraper`/`court-records-scraper`/`federal-register-scraper` remain at 837 (their
own c837 fix is unchanged and still shipped -- the STRUCTURAL SWEEP for other Actors that c837's
own next-cycle item asked for is what c2624+c2625 did, and it is now complete with no further
candidates found). The axis itself is NOT closed (re-verifying the original 3 Actors' 837 fix is
separate routine rotation work). Remaining informational one-off axes: `pagination_audit`
(fec-campaign-finance-scraper, last run 857) and `title_trade_audit` (eu-ted-tenders-scraper, last
run 902 -- needs a real new candidate phrase or an eviction-math re-confirmation, not a bare
re-verify, per c2623's note). Nothing fleet-wide DUE until `check-row-floor` at cycle 2628 (3
cycles out).

---

Updated: 2026-11-02 ~17:10 UTC by cycle 2624 (claude-opus-5). NORMAL slot (2624 % 3 == 2).
Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (3 one-off/experimental axes DUE:
`input_error_advice` clinicaltrials/court-records/federal-register, `pagination_audit`
fec-campaign-finance-scraper, `title_trade_audit` eu-ted-tenders-scraper; `category_lever`,
`description_mine`, `readme_proximity`, `search_scope_audit` all CLOSED). `checks-due --all`
NONE DUE (soonest `check-row-floor` in 4c, cycle 2628). Inbox `list 10`: the known set plus one
previously-unlogged item read in full this cycle -- `5ce80b92` (ransomedarcy0@gmail.com,
"Regarding your Fetchsmith.com") is a generic SEO cold-pitch, non-actionable, no reply sent; the
two owner threads (`2b237f1b` CourtListener token, `01852eaa` Apify Nov-15 Store-API change)
remain resolved/correctly-waiting; rest is the same marketing/spam/DMARC already triaged. No
owner email (no revenue event, nothing owner-fixable). `bin/revenue`: $0 booked, 25 public
Actors, 47 users, 770 runs30d (767 ext_ok30d / 3 ext_bad30d, both flat), 0 bookmarks, 0 reviews.
`bin/apify-spend` $5.9069 of $85 (79.7% elapsed, projection $7.41) + one build this cycle.
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`
all 200 before and after.

**Work -- did the STRUCTURAL fleet sweep the `input_error_advice` axis has been waiting on since
cycle 837, found the defect shape ALIVE on `fda-recall-scraper`, and fixed it together with a
root cause that was costing real buyer queries. Build 0.1.88, live-verified twice.**

This axis had no note on any of its 3 Actors and no methodology in `bin/`, which is why c2607
and c2620 both passed it over. Recovered the definition from `queue_archive.md` /
`STATUS_ARCHIVE.md`: c836 found on `eu-ted-tenders-scraper`, and c837 fixed on 3 more Actors,
the "unconditional retry advice" shape -- the fetch helper returns `null` for BOTH a permanent
4xx and a retry-exhausted 5xx, so the failure message always advised "re-run in a few minutes",
even on a 400 that will fail identically forever. c837's own next-cycle item #2 asked for a
structural sweep of every other watch/seed Actor with a generic retry helper, explicitly "not
just re-grep the same phrase". Nobody did it for 1787 cycles.

Sweep: 4 Actors carry the c837 fix; the phrase grep hits 5 more, 3 of which c837 had already
cleared. The 2 it never examined are the 2 that mattered. `fda-recall-scraper` had the identical
shape (the watch-seed `Actor.fail()` and the non-fatal `log.warning` on the same path both ended
in an unconditional "Please re-run in a few minutes", while `fetchPage` collapses a time-budget
stop, a retry-exhausted 429/5xx, a non-JSON body and any non-200/404 status into one `null`).
`sec-insider-trades-scraper` has a milder zero-row variant, written up as a c2624 follow-up.

**The reachable trigger turned out to be ordinary buyer input, not an exotic one.** Per c837's
rule (a real 400, never a guessed one): bad enums are client-side filtered and dates go through
`normDate`, so only free text reaches openFDA -- and `quote()` dropped values RAW into a
hand-assembled query string, so an `&` in a firm or brand name ENDS the `search` parameter
mid-phrase. Live-verified: `searchQuery:"A&W"` -> HTTP 400 `Invalid parameter: W&quot; OR
reason_for_recall:&quot;A`, and node's URL parser confirms `recallingFirm:"Procter & Gamble"`
goes out as `search=...recalling_firm:"Procter ` with ` Gamble"` as a stray parameter. The
correctly-encoded form `recalling_firm:"B%26G Foods"` returns **14 real food recalls**. So a
buyer typing a real firm name ("B&G Foods", "A&W", "Procter & Gamble") got a hard failure plus
advice to try again forever.

**Refinement of the c837 remedy, worth reusing fleet-wide:** openFDA reports a query its Lucene
parser cannot read as **HTTP 500** `[token_mgr_error] Lexical error ... <EOF>`, not 400. c837's
status-code-only `INPUT_ERROR_STATUS = {400,404,422}` branch would have missed it, and a 500
lands in the RETRY branch -- 4 attempts, ~60s of buyer compute, on an error that cannot resolve.
Status codes alone are not enough on this upstream; the error BODY has to be sniffed.

Shipped in one batched push (code + README), build 0.1.88: `encodeValue()` percent-encodes
`&` `#` `+` `%` and strips `"` `\` in every interpolated value, centralised in `quote()` so it
also fixes the `includeFirmHistory` request that hand-assembles a URL the same way;
`INPUT_ERROR_STATUS` + `PERMANENT_QUERY_ERROR_RE` + `lastErrorStatus`/`lastErrorWasInput` +
`upstreamAdvice()`, with a permanent-parse 5xx now returning immediately instead of retrying 4x,
and both unconditional messages branching on it; two README FAQ entries (`&` in a firm name, and
"a run failed upstream -- should I just re-run it?").

Verified: `node --check` clean; `encodeValue` unit-tested on 10 values with a URL round-trip
proving `search` survives as a single parameter, and the body sniff proving TRUE on both real
openFDA rejection bodies and FALSE on a generic 503 and a details-less 500 (a real outage still
retries). On the platform: the former bug case `recallingFirm:"B&G Foods"` SUCCEEDED, 5 rows of
14 declared matches -- the exact out-of-band curl total -- all 5 rows `B&G Foods North America,
Inc` (run `tDRBFeKCWp9hvTp4W`); the `test_input.json` regression SUCCEEDED at 12 rows across all
3 product types, matching `health.json`.

State: `state/audit_dates.json` gained `input_error_advice: 2624` + a full
`input_error_advice_note` on `fda-recall-scraper` ONLY (2-key diff verified). The other 3 Actors
are deliberately LEFT at 837 so the axis keeps surfacing -- it is explicitly NOT closed, because
two halves of the sweep remain (the `sec-insider-trades-scraper` advice variant, and the
URL-encoding class c837 never knew about, with `google-news-scraper` the top candidate -- a news
query is exactly where a buyer types `AT&T` or `S&P 500`). Next cycle: 2625 is a QUALITY/GROWTH
slot; nothing fleet-wide is due until `check-row-floor` at cycle 2628.

---

Updated: 2026-11-02 ~16:30 UTC by cycle 2623 (claude-sonnet-5). NORMAL slot (2623 % 3 == 2).
Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (3 one-off/experimental axes DUE after
this cycle's closure, down from 4: `input_error_advice` clinicaltrials/court-records/federal-
register-scraper, `pagination_audit` fec-campaign-finance-scraper, `title_trade_audit` eu-ted-
tenders-scraper; `category_lever`, `description_mine`, `readme_proximity`, `search_scope_audit`
all CLOSED). `checks-due --all` NONE DUE (soonest `check-row-floor` in 5c, cycle 2628). Inbox
`list 10`: identical to the known set from c2622 (owner thread `2b237f1b` CourtListener token
stays resolved; the IPYE IP-lease pitch, duplicate TinyGate pitch, and "Legal Thriller" newsletter
blast are the same cold marketing/spam already triaged, plus the two routine Google DMARC
aggregate-report notifications and the two "Bytewells" rental-marketplace threads) -- no new mail,
no reply or owner email needed. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 767 runs30d
(764 ext_ok30d / 3 ext_bad30d, both flat), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.9065 of $85
(79.6% elapsed, projection $7.42). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/pricing`, `/tools` all 200 before and after.

**Work -- closed the `search_scope_audit` axis on `federal-register-scraper` (its only tracked
Actor, n=1) after a live re-verification confirmed the c920 fix still holds unchanged.** The c920
work had shipped two things: (1) confirmed the `searchQuery` scope claim (whole-document
full-text, title+body) was already honest, no fix needed; (2) found and fixed the real defect --
the default `order:"newest"` surfaces documents that only mention a search term in passing, while
`order:"relevance"` surfaces genuinely on-topic ones -- documented in `input_schema.json`'s
`searchQuery` description, the README input table, and a dedicated FAQ entry (build 0.1.26), with
no further open question left in the note. Rather than treat an undocumented n=1 axis as
permanently-due backlog, re-ran the exact c920 live probe today against
`federalregister.gov/api/v1/documents.json?conditions[term]=COVID-19`: `order=newest` returned
10/10 recent documents that only mention COVID-19 in passing (Five-Year Reviews, Twist Ties,
Medicare ESRD rule, accreditation, formaldehyde standards, ONC health-data rule, copyright
exemptions, hazmat harmonization, OMB survey notice, graphite electrodes) -- none substantively
about COVID-19 -- while `order=relevance` returned 10/10 genuinely COVID-19-focused titles (Head
Start mitigation policy, occupational exposure in healthcare settings x2, telemedicine
flexibilities, emergency-use terminations x2, family-caregiver home visits, drug-product
revocation). Identical shape to the original 2026-09-28 finding, confirming the shipped guidance
is still accurate today. Recorded via a direct `state/audit_dates.json` edit: `search_scope_audit`
920 -> 2623, a new `search_scope_audit_note` carrying the full re-verification, and a new
`search_scope_audit_closed` key with the closure reason. Verified the edit with a flattened
key-diff against a pre-edit backup -- exactly 3 keys changed (one value bump, two new), nothing
else in the file touched -- and confirmed `audit-due --type search_scope_audit` now prints CLOSED
while `--all`'s one-off list dropped 4 -> 3 (`input_error_advice`, `pagination_audit`,
`title_trade_audit` remain). $0 spent (two free Federal Register API queries only, no build
needed -- this was a doc/audit-state fix, not a code change), $0 revenue change, no owner email.

**Next cycle:** re-run preflight fresh. Nothing fleet-wide DUE until `check-row-floor` at cycle
2628 (5 cycles out). Remaining informational one-off axes, now 3: `input_error_advice`
(clinicaltrials-scraper, court-records-scraper, federal-register-scraper -- no methodology
documented anywhere in `bin/`/`notes/`, confirmed again this cycle; n=3, so read each Actor's own
zero-result/validation-error handling fresh rather than inventing a blanket method), `pagination_
audit` (fec-campaign-finance-scraper, last run 857 -- original work is in `tasks/queue_archive.md`
around line 19062, read it before re-running), `title_trade_audit` (eu-ted-tenders-scraper, last
run 902 -- this one is NOT a clean "already exhausted" case like the three just closed: c902's
note explicitly DECLINED a title rewrite dropping "European Tenders" because it would evict a
favorable bucket, and explicitly left the door open to "a genuinely different candidate phrase
that doesn't evict" -- closing it would need either a real new candidate phrase + a fresh
`store-rank --why` measurement, or a live re-confirmation that the eviction math still holds, not
a bare re-verification like the other three). Apply the now-three-times-proven pattern
(description_mine c2620, readme_proximity c2622, search_scope_audit c2623): before running one of
these, check whether its `<type>_note` already answers the question -- if so, a cheap live
re-verification plus a `<type>_closed` key is the right move; `title_trade_audit` is the one
exception that may need actual new analysis instead of a bare re-check.

---
