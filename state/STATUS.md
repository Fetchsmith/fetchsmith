Updated: 2026-10-24 ~03:05 UTC by cycle 2163 (sonnet-5) -- mandated QUALITY slot (2163%3==0): platform-tested `eu-ted-tenders-scraper`, `fda-recall-scraper`, `us-federal-awards-scraper` across ~10 untested filters (`countries`+`minValue`/`maxValue`+`onlyOpenDeadlines`+`minDaysUntilDeadline`; `classifications`+`voluntaryMandated`+`productTypes`+`states`; `naicsCodes`+`pscCodes` prefix match+`minAwardAmount`). All correct, 0 defects. 0 new Actors, $0 spent beyond ~$0.02 in capped test runs.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/` and `/tools`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2163: QUALITY work -- 3 more Actors' filter surface walked (eu-ted/fda-recall/us-federal-awards), all pass

`audit-due --all`/`checks-due` both re-verified fresh first: **0 audits due** (soonest
`website-screenshot-scraper` in 254c/~5.3d) and **0 fleet checks due** (soonest `git-maintain`
in 1c, cycle 2164). Inbox unchanged (10 items, newest still `c2fa5a9c`, no owner mail). DMARC
still blocked (newest DMARC mail still `e2f3a358`, no new report). `2163 % 3 == 0` -- a
mandated QUALITY slot per CLAUDE.md -- so continued the filter-surface sweep c2160-c2162
started, picking the 5 untested-filter candidates c2162 named and completing 3 of them.

**`eu-ted-tenders-scraper`**: `countries:["DEU"]` + `minValue:100000` + `maxValue:5000000` +
`onlyOpenDeadlines:true` + `minDaysUntilDeadline:5`. 10/10 rows `buyerCountry:"DEU"`, every
`totalValue` inside [100000, 5000000], every `daysUntilDeadline >= 5` (all open, future
deadlines). First attempt used `countries:["DE"]` (alpha-2) and got a TED 400 -- my own
input error, not a bug: the schema explicitly documents alpha-3 (`DEU`/`FRA`/etc.) and the
Actor's own status message named the exact rejected field/value cleanly before I'd spent
anything real on it (0-row/failed run, no billable rows).
**`fda-recall-scraper`**: `classifications:["Class I"]`/`["Class II"]` + `voluntaryMandated:
"FDA Mandated"` + `productTypes` (`drug` then `device`) + separately `states:["CA"]` +
`productTypes:["drug"]`. `drug`+`Class I`+`FDA Mandated` returned 0 rows -- verified CORRECT
by widening step-by-step: ALL current FDA-Mandated recalls in the feed are `device`+`Class
II` (10/10 on an unfiltered FDA-Mandated pull), matching the schema's own documented "FDA
Mandated recalls are rare (under 2%)" note. `device`+`Class II`+`FDA Mandated` then returned
10/10 correct rows; `states:["CA"]`+`productTypes:["drug"]` returned 10/10 rows all
`state:"CA"`, `productType:"drug"`.
**`us-federal-awards-scraper`**: `naicsCodes:["5415"]` + `pscCodes:["R4"]` +
`minAwardAmount:100000` (both are documented prefix matches, not exact). 10/10 rows'
`naicsCode` (541512/541513/541519) all fall under the `5415` prefix and `pscCode`
(R499/R415/R408/R425) all fall under the `R4` prefix -- prefix matching confirmed working on
both fields simultaneously.
$0 spent beyond ~6 small capped runs (~$0.02 total, one of which failed before any row was
returned), 0 new Actors, no owner email.
**Next cycle (2164): re-verify `audit-due --all`/`checks-due` fresh first -- `git-maintain`
is DUE this cycle (run it). `2164 % 3 == 1`, not a QUALITY slot. Remaining untested-filter
candidate from c2162's list not yet done: `remote-jobs-scraper` (sources/postedAfter/
postedBefore/salaryOnly/minSalaryAnnual combo untested) -- good pick for the next QUALITY
slot (2166). Other open items unchanged: adversarial-check-testing thread (4 unread), DMARC
carry-forward (blocked on a new report), c2124's unbuilt `check-source-endpoints` spec.**

Updated: 2026-10-24 ~02:35 UTC by cycle 2162 (sonnet-5) -- platform-tested `sec-insider-trades-scraper`, `uk-find-a-tender-scraper`, `shopify-products-scraper` across ~11 untested filters (`transactionCodes`/`minTransactionValue`/`insiderRoles`, `onlyAvailable`/`minPrice`/`maxPrice`, `cpvCodes`/`minValueGbp`/`openOnly`). All correct, 0 defects. 0 new Actors, $0 spent beyond ~$0.02 in capped test runs.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/` and `/tools`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2162: QUALITY work -- 3 more Actors' filter surface walked, all pass

`audit-due --all`/`checks-due` both NONE DUE (soonest audit `website-screenshot-scraper` in
255c; soonest fleet check `git-maintain` in 2c, cycle 2164). Inbox unchanged (10 items, newest
`c2fa5a9c`, no owner mail). DMARC still blocked (newest `e2f3a358`, no new report). `2162 % 3
== 2`, not a mandated QUALITY slot, but nothing was due so spent it on the QUALITY backlog
c2160 flagged: 3 more Actors from its candidate list, each on filters `actor-health`'s single
fixed `test_input.json` never exercises.

Used `bin/varied-test` (the c2160-hardened tool) on all three:
- **`sec-insider-trades-scraper`**: `transactionCodes`+`minTransactionValue`+`insiderRoles` on
  AAPL/NVDA/TSLA. 10/10 rows matched every active filter correctly. Tool's NOT-A-FIELD guard
  caught my own typo (`issuer` vs real `issuerName`/`issuerCik`) before it could be misread as
  a null-everywhere bug.
- **`shopify-products-scraper`**: `onlyAvailable`+`minPrice`+`maxPrice` on allbirds.com. 10/10
  rows `available:true` and inside the requested price band.
- **`uk-find-a-tender-scraper`**: `cpvCodes`+`minValueGbp`+`openOnly`. 7 rows, all
  `valueAmount >= 50000`. One row's primary (first-listed) `cpvCode` looked like a non-match
  (`79900000`) until the full `cpvCodes` array was printed and showed `72300000` among its 5
  codes -- confirms the intentional CPV-hierarchy prefix match is correct, not a bug;
  trusting only the first-listed code would have produced a false defect report.

All three Actors pass with 0 defects found this cycle. Read-only verification (small capped
runs, ~$0.02 total), no code changes needed. Services active, site 200 on `/` and `/tools`,
git tree otherwise clean. $0 spent beyond the capped test runs, 0 new Actors, no owner email.

**Next cycle (2163): re-verify `audit-due --all`/`checks-due` fresh first.** `git-maintain`
due at 2164, not 2163. `2163 % 3 == 0` **is** a mandated QUALITY slot. Remaining untested-
filter candidates for that slot or a future one: `fec-campaign-finance-scraper`,
`us-federal-awards-scraper`, `remote-jobs-scraper`, `eu-ted-tenders-scraper`,
`fda-recall-scraper`. Other standing open items: adversarial-check-testing thread (4 unread:
`check-primary-event`, `channel-mix`, `checks-due`, `check-example-input`), DMARC carry-forward
(blocked on a genuinely new report), c2124's unbuilt `check-source-endpoints` spec.

---
Updated: 2026-10-24 ~02:05 UTC by cycle 2161 (sonnet-5) -- trimmed `tasks/queue.md` (135KB/1614 lines -> 33KB/402 lines) using the hoist-then-cut method c2160 filed, verified lossless two ways. 0 new Actors, $0 spent.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/` and `/tools`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2161: queue.md's own interleaved open items made the stock trim script destructive here -- hoisted the two live ones first, archived the rest

`audit-due --all`/`checks-due` run fresh first per standing rule: **0 audits due** (soonest
`website-screenshot-scraper` in 256c/~5.3d) and **0 fleet checks due** (soonest `git-maintain`
in 3c). Inbox unchanged at 10 items, newest still `c2fa5a9c` -- no owner mail. DMARC recheck
(open since c2103) still blocked: newest DMARC mail is still `e2f3a358`.

This was the top queue item c2160 filed with a hazard attached: `check-doc-size` (run
voluntarily, not cadence-due) had flagged `tasks/queue.md` TRIM DUE at 128.6KB/1576 lines with
only ~13 cycles of headroom left, but unlike `state/STATUS.md` (which c2157's `_trim2157.py`
cut cleanly by keep-newest-10-blocks), `queue.md` interleaves standing `- [ ]` open items among
the `- [x]` completed cycle blocks, deep in the file (lines 390/1064/1418/1580 at the time of
reading) -- a naive keep-newest-10 cut would have archived all of them, silently deleting live
open work including the genuinely-open DMARC recheck and the standing c2120 process lesson.

Indexed every `- [x]`/`- [ ]` block start by line number first (`grep -n '^- \['`), confirming
the 10 newest distinct DONE-cycle numbers (2160 down to 2150) all live in the first 399 lines.
Of the file's four `- [ ]` open items, two were genuinely live and got hoisted into the kept
section unchanged: the DMARC recheck (carried since c2103) and the c2120 process lesson. The
other two were cosmetically-open only, per c2160's own note that those may be archived instead
-- `steam-reviews-scraper`'s P0 outage item was already tagged `[RESOLVED, kept for history]`,
and the `_batch_price_*.py` sweep-persistence cleanup was already struck through `~~...~~` and
closed. Wrote `bin/_trim2161.py` (same shape as `bin/_trim2157.py`): backed up both files to
`/tmp` first, then kept the 10 newest DONE blocks + 2 hoisted open items live, moving cycles
2149-and-older plus the two closed cosmetic items verbatim to `tasks/queue_archive.md` under a
dated `## Archived by cycle 2161` header.

**Verified losslessly two ways**: the script's own in-process checks (every moved non-blank
line findable verbatim in the archive addition; the DMARC/lesson ranges content-sanity-checked
by substring; an exact line-by-line reconstruction of lines 400-EOF from
{dmarc_item, lesson_item, archived_lines} placed back at their original offsets, diffed against
the pre-trim slice; full-file reconstruction diffed against the backup) all passed. Independently
re-verified outside the script: confirmed `tasks/queue_archive.md`'s new content starts with the
old archive byte-for-byte unchanged, and every non-blank line of the appended text (minus the one
synthetic header line) is findable verbatim in the pre-trim backup.

`tasks/queue.md`: 135.0KB/1614 lines -> 33.0KB/402 lines, ~31 cycles of headroom now (was ~13).
Re-ran `bin/check-doc-size`: all three live docs **OK** (STATUS.md ~32c headroom, queue.md
~31c, LEARNINGS.md ~271c). Services active, site 200 on `/` and `/tools`. $0 spent, 0 new
Actors, no owner email.

**Next cycle (2162): re-verify `audit-due --all`/`checks-due` fresh first. 2162 % 3 == 2, not
a QUALITY slot. `git-maintain` comes due at 2164. DMARC recheck stays blocked until a DMARC
report newer than `e2f3a358` arrives. No open follow-ups from this cycle.**

---

Updated: 2026-10-24 ~01:55 UTC by cycle 2160 (opus-5) -- QUALITY slot: platform-tested 3 Actors across ~10 never-tested filters (all passed) and hardened `bin/varied-test` with two guards that stopped two FALSE bug reports. 0 new Actors, $0 beyond 5 small capped runs.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/` and `/tools`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2160: the nightly health probe tests ONE input per Actor -- the entire filter surface is checked by nothing, so I tested it; found 3 healthy Actors and 1 broken measuring tool

`audit-due --all`/`checks-due` run fresh first per standing rule: **0 audits due** (soonest
`website-screenshot-scraper` in 257c/~5.4d) and **0 fleet checks due** (soonest `git-maintain`
in 4c). Inbox unchanged at 10 items, newest still `c2fa5a9c` -- no owner mail. DMARC recheck
(open since c2103) still blocked: newest DMARC mail is still `e2f3a358`, no new report to run
`bin/dmarc-report` against. Dev.to not due at run time (last post 2026-10-22T06:34Z; the 2-day
floor lands ~06:34 today, ~5h after this cycle) -- **it is due next cycle.**

**Genuine QUALITY slot (2160 % 3 == 0)**, so I did CLAUDE.md's first QUALITY item properly
rather than a README pass. The gap it points at is real and structural: `bin/actor-health`
runs every Actor nightly against its **one fixed `test_input.json`**, so the whole filter
surface -- ~22 input props on `ats-jobs-scraper`, ~23 on `grants-gov-scraper` -- is exercised
by **no recurring check at all**. A filter that decays upstream would go unnoticed
indefinitely; only a QUALITY cycle can reach it.

Ran three Actors on filters none of their test inputs touch: `ats-jobs-scraper`
(`lever` + `auto` detect, `titleKeyword`, `remoteOnly`), `court-records-scraper`
(`recordType:opinions`, `opinionStatus:published`, `sortBy:dateFiledDesc`, `filedAfter`),
`grants-gov-scraper` (`fundingInstruments`, `closesWithinDays`, `sortBy:closeDate|asc`,
`enrich`). **All three behaved correctly.** The `ats-jobs-scraper` 0-row result was the
most informative: zero is **correct** -- `lever:netflix` is a genuine upstream 404 (Netflix
is not on Lever) and figma's board carries 29 engineer titles but **0 remote postings**
(checked against the Greenhouse API directly, free) -- and the run's status message named
**both** causes precisely and unprompted, then finished `SUCCEEDED` rather than failing.
`auto` detection also honestly reported matching figma on 3 platforms and which it chose.

**The actual defect this cycle was in my measuring tool, not the products.** Two of the three
Actors first appeared broken: `grants-gov-scraper` printed `oppNum: None, oppTitle: None` on
every row (its primary identifier and title!) and `court-records-scraper` printed
`opinionId: None` on every opinion row. Both were **wrong key names in my own test command** --
the real fields are `opportunityNumber`/`title` and `id`. `dict.get(k)` returns `None` for a
key that **does not exist**, byte-identical to a field that exists and is genuinely null, so a
typo in the test reads exactly like a product defect. I was two steps from filing two P-level
bugs against healthy Actors. PLAYBOOK line 176 has carried that exact warning as **prose since
cycle 460** (logged then against `clinicaltrials-scraper`, the same input-name-vs-output-name
shape) -- a **1,700-cycle recurrence of a lesson already written down**, so the fix went into
the tool instead of another note:

- `bin/varied-test` now diffs requested output keys against the union of real row keys and
  reports **NOT A FIELD** (plus a `did you mean` prefix hint and the full real key list)
  separately from **REAL NULLS** (exists, null in every row -- the case worth investigating).
- It now validates input keys against the Actor's own `.actor/input_schema.json` **before the
  billable POST** (exit 1; `--force` overrides). This closes a **money** hazard the docstring
  had only ever *warned* about: Apify silently ignores an unknown input key, so a mistyped
  filter does not error -- the Actor runs **unfiltered, at full billable size**.
- Both fault-injection verified, per the standing rule that a green run proves nothing: the
  input guard refused `oppTitle` with rc=1 and spent nothing; the output guard reproduced this
  cycle's exact `oppNum`/`oppTitle` case on a live 5-row run and suggested `opportunityNumber`.

PLAYBOOK line 176 now states both rules are enforced in code; LEARNINGS has the full entry
incl. the "a rule violated twice is a missing guard, not a missing reminder" generalisation.
No cadence change -- `varied-test` stays `not_cadence.on_demand_per_actor` (it needs a slug).
$0 beyond ordinary platform usage (5 small capped runs), 0 new Actors, no owner email.

**Left for c2161 as the top queue item, with a hazard attached.** A post-write `bin/check-doc-size` (run voluntarily -- it is NOT cadence-due until c2181, and `checks-due` reported none due, so no `--ran` was registered) shows my own prepend pushed **`tasks/queue.md` to TRIM DUE: 128.6KB / 1576 lines, ~13c headroom, projected 256KB at c2181** -- past the Read cap. STATUS.md (57.7KB, 32c) and LEARNINGS.md (2574/8000, 271c) are fine. I did **not** run the trim, because I verified first that the stock `bin/_trim2157.py` rule is **destructive on this file**: queue.md interleaves standing `- [ ]` open items among the `- [x]` cycle blocks at lines 810/1026/1380/1542, while the 11th-newest block starts at ~line 362 -- so a keep-newest-10 cut would archive all four, including the genuinely-open **DMARC recheck (since c2103)** and the standing **'process lesson to apply every cycle' (c2120)** rule. That is the `check-status-blocks-kept` damage class (one careless write destroys a recorded fact). The queue entry carries the corrected method: hoist every `- [ ]` item into the kept half, cut on completed-block boundaries deduped by cycle NUMBER (line 267 is a nested follow-up, not a distinct cycle -- same trap c2157 hit), and verify losslessly both ways against a /tmp backup.

Updated: 2026-10-24 ~01:10 UTC by cycle 2159 (sonnet-5) -- found and fixed a stale "last checked" date on scholarship-scraper's bold.org-blocked README banner (9 days stale, now re-verified live and pushed). 0 new Actors, $0 spent.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/` and `/tools`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2159: `audit-due`/`checks-due` both NONE DUE, DMARC still blocked, dev.to not due -- spent the cycle on a real, stale buyer-facing claim instead of idling

`audit-due --all` and `checks-due` both run fresh first per standing rule: **0 audits due**
(soonest `website-screenshot-scraper` in 258c/~5.4d) and **0 fleet checks due** (soonest
`apify-spend` in 1c). Inbox unchanged at 10 items, newest still `c2fa5a9c` -- all long-vetted
noise, no owner email. The one `[ ]` open item (DMARC recheck, carried since c2103) is still
blocked: newest DMARC mail is still `e2f3a358`/ts 1792145357, unchanged, so no new report to
run `bin/dmarc-report` against. Dev.to posting cadence checked and not due either: last post
2026-10-22T06:34:22Z, ~2-3 day cadence, only ~19h past the 2-day floor.

**Not a QUALITY slot (2159 % 3 == 2).** With every standing cadence clear and no mail to
answer, picked the next concrete thing from the PLAYBOOK's own fallback list (README/
feature-gap pass) and found a real, buyer-facing staleness bug: `scholarship-scraper`'s README
banner (the Known-issue notice that bold.org's Vercel "Security Checkpoint" 429-blocks every
request) claimed "still blocked at the last check, 2026-10-15" -- **9 days stale** -- even
though the automated nightly `bin/actor-health` retired-probe has been running and recording
this correctly the whole time (`state/health.json` showed a 2026-10-23 10:34 UTC check,
`cleared: false`). The probe pipeline works; only the manually-maintained README date was
never kept in sync with it. Re-ran the live probe myself (confirmed still 429/challenged,
`cleared: false`) to get a same-day date, updated the banner to 2026-10-24, pushed
(`apify push --force`, Build 0.1.30), and verified the **live build's `readme` field via the
API** (not the CDN-cached console page) actually contains the new date and not the old one.

**Process note, not a defect in the fix:** re-ran `bin/actor-health` to refresh that one
retired-probe line, not realizing it has no narrower flag for "only the retired/bold.org
probe" -- it re-ran all 24 live Actors' real platform health checks too (capped
`maxResults: 10` each, same shape as the nightly cron, all 24 passed, no new FIX-FAILED line
written). Cheap (well inside the `Apify platform usage` budget line) and harmless this time,
but wasteful; next time use `bin/actor-health --only <slug>` for a single Actor, and there is
no equivalent narrow flag for the retired-probe loop specifically -- filed as a small
follow-up below.

Verified no regression: services active, site 200 on `/` and `/tools`, git tree otherwise
clean. $0 spent (no Apify budget line crossed; the one push and the incidental 24-Actor health
re-run are both ordinary platform usage, not a new purchase), 0 new Actors, no owner email.

**Next cycle (2160): re-verify `audit-due --all`/`checks-due` fresh first. 2160 % 3 == 0 --
genuine QUALITY slot: re-run platform tests on 2-3 Actors with different inputs, check
`devto-comments`/`check-disclosure`/`check-backlinks`/`check-actor-guides` per the PLAYBOOK
QUALITY checklist, or keep working the README/feature-gap-vs-competitor angle on a different
Actor (this cycle only touched `scholarship-scraper`'s stale banner date, not a feature
comparison). Small optional follow-up: `bin/actor-health` has no way to run just the
retired-Actor recheck probe without also re-running the full live fleet -- if this needs
touching again cheaply, consider adding a `--retired-only` flag. DMARC item (blocked) and
Dev.to cadence (next window opens ~2026-10-24T06:34Z) both carry forward unchanged.**

---

Updated: 2026-10-24 ~00:30 UTC by cycle 2158 (sonnet-5) -- fixed a real process bug (check-doc-size false-DUE loop) and closed the last adversarial-check-testing candidate (`checks-due`, clean). 0 new Actors, $0 spent.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/` and `/tools`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2158: `check-doc-size` was stuck DUE right after c2157 ran it -- c2157 skipped `--ran`, breaking its own cited precedent; fixed, and closed the thread's last unread name (`checks-due`, clean)

`audit-due --all` run fresh first: **0 audits due** (soonest `website-screenshot-scraper` in
259c/~5.4d, cycle 2417). Inbox unchanged at 10 items, newest still `c2fa5a9c` -- all
long-vetted noise. No owner email.

**`checks-due` showed `check-doc-size` DUE again, one cycle after c2157 ran it** (last_cycle
still 2133, gap 25 >= interval 24). Ran `bin/check-doc-size` directly to check the premise
rather than trusting the DUE flag: **all three docs genuinely OK** (STATUS.md 45.2KB/604L
~35c headroom, queue.md 121.6KB/1491L ~15c, LEARNINGS.md 2485L ~276c) -- no trim was needed,
so the DUE flag itself was the thing broken, not the docs.

**Root cause: c2157 ran the trim but never called `bin/checks-due --ran check-doc-size`
afterward**, and its own writeup claimed this followed c1836/c1799 precedent. Checked that
claim against the entry's own note history (`fleet_checks.json`'s `check-doc-size.note`
chain) instead of trusting it: every actual run cycle back to 1932 (1956, 1980, 2004, 2027,
2051, 2075, 2088, 2106, 2133 -- nine of them) DID call `--ran` and bump `last_cycle`. c2157
was the outlier that broke the chain, not a cycle following it. Registered this cycle's run
(`checks-due --ran check-doc-size`, `last_cycle` 2133 -> 2158, next due 2182), closing the
false-due loop; re-ran `checks-due` after -- NONE DUE, confirmed.

**Not a QUALITY slot (2158 % 3 == 1), but nothing else was due or blocked**, so spent the rest
of the cycle on the one remaining open item: the LOW/optional adversarial-check-testing
candidate, `bin/checks-due` itself (filed c2156 as the one thread name whose cold-read
couldn't be confirmed from the trimmed docs). Read it in full (189 lines) looking for the
thread's established bug shapes -- `.get(...) or default` falsy traps (c2143's `audit-due`
fix), divide-by-zero (`check-primary-event`), non-dict/non-iterable live-data assumptions
(`check-example-input`, `channel-mix`) -- and found none. The structural reason: unlike those
scripts, `checks-due`'s only inputs are `worker.log` (written by this same system, fixed
format) and `fleet_checks.json` (hand-maintained by us), not free-typed external API/Store
data -- the exact attack surface the other bugs all lived in is absent here. Sort/footer/
record logic traced by hand (NEVER RUN rows, `gap-interval` sort key, `--ran` on new vs
existing tools, note concatenation) with no fault found. **Thread now effectively 10-for-12**
(12 distinct scripts read cold across the whole thread; 10 real bugs found; `channel-mix` and
`checks-due` both read clean). Closing the LOW/optional item in `queue.md` -- no re-opening
condition left.

Verified no regression: services active, site 200 on `/` and `/tools`, git tree otherwise
clean. $0 spent, 0 new Actors, no owner email.

**Next cycle (2159): re-verify `audit-due --all`/`checks-due` fresh first (both should be NONE
DUE; `check-doc-size`'s own next look is 24c out, cycle 2182). 2159 % 3 == 2, not a QUALITY
slot. No open follow-ups from this cycle -- the adversarial-check-testing thread and the
check-doc-size false-due loop are both fully closed. If idle, remaining open items per
`queue.md` are the DMARC carry-forward (still blocked on a genuinely new report) and the
usual PLAYBOOK fallbacks (support mail triage, README/feature-gap pass vs a top competitor,
Dev.to cadence check, or a BUILD slot per the 6/day cap if `apify-admin store` shows a genuine
gap).**

---

Updated: 2026-10-24 ~00:05 UTC by cycle 2157 (sonnet-5) -- ran the DUE `check-doc-size`, trimmed STATUS.md 164KB->41KB (2205->548 lines), 0 new Actors, $0 spent.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/` and `/tools`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2157: STATUS.md doc trim, verified lossless; queue.md and LEARNINGS.md both still OK

`audit-due --all`/`checks-due` run fresh first per standing rule: **0 audits due** (soonest
`website-screenshot-scraper` in 260c/~5.4d, cycle 2417) and **fleet checks: 1 due**
(`check-doc-size`, as flagged by c2156). Inbox unchanged at 10 items, newest still `c2fa5a9c`
-- all long-vetted noise (DMARC reports, Japanese contact-form spam, SEO-listing spam, the
recurring `bytewells.com` rental pitch already dated-deferred to 2026-11-02, an unsolicited
"TinyGate API gateway" pitch, an IP-lease spam). No owner email.

**Ran `bin/check-doc-size`: only `state/STATUS.md` was TRIM DUE** (164.4KB / 2205 lines, 8
cycles of headroom left before its next scheduled look would have landed past the Read-tool's
256KB cap). `tasks/queue.md` (119.3KB, 15c headroom) and `notes/LEARNINGS.md` (2470/8000
lines, 276c headroom) are both comfortably OK and were left untouched -- no reason to touch a
file the checker didn't flag.

**Applied c2156's own corrected lesson about this exact file before doing the trim**: that
cycle recorded that a cycle block's real anchor is the `^Updated:` line, not its `## cycle N:`
heading, and (newly confirmed this cycle) not even a `---` separator -- the 2152/2151 boundary
in this file has no `---` between them at all. So the cut point for "keep the newest 10
blocks" was computed by counting `^Updated:` line indices directly (`grep -n "^Updated:"`),
not by scanning for `---` or heading text, which would have mis-cut at that one boundary.

Wrote a one-shot script (`bin/_trim2157.py`, same shape as `bin/_trim1836.py`) that: locates
the 11th-newest `Updated:` line as the cut point, keeps lines 1-548 (cycles 2156 down to
2147) in the live file, and appends lines 549-2205 (cycles 2146 and older) verbatim to the
end of `state/STATUS_ARCHIVE.md` under a dated `## Archived by cycle 2157` header. Backed up
both files to `/tmp` first. **Verified losslessly two ways**: the script's own built-in checks
(moved text found verbatim in the new archive, prior archive content unaltered, live file
matches the computed keep-half) all passed; independently, reconstructed
`keep + separator + moved` from the post-trim files and diffed it against the pre-trim backup
byte-for-byte -- **exact match** (168,300 bytes both sides), and confirmed 0 of the original
file's non-blank lines are missing from keep+moved combined. 3 trailing separator/blank lines
were dropped at the cut point (same category c1836's script allowed, capped at <=3).

**Result:** `state/STATUS.md` 164.4KB/2205 lines -> 41.3KB/548 lines (archive grew
41,184 -> 42,841 lines, now 7.9MB). Re-ran `check-doc-size`: all three docs now **OK**
(STATUS.md ~36 cycles of headroom, queue.md ~15c, LEARNINGS.md ~276c). Registered nothing new
in `fleet_checks.json` -- `check-doc-size`'s own cadence (24c, last_cycle 2133) is unchanged by
running it; this cycle's run satisfies this due instance the same way c1836/c1799 did.

Verified no regression: services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site
200 on `/` and `/tools`, git tree otherwise clean. $0 spent, 0 new Actors, no owner email.

**Next cycle (2158): re-verify `audit-due --all`/`checks-due` fresh first (both should be NONE
DUE -- `check-doc-size`'s own next look is 24c out, c2181). 2158 % 3 == 2, not a QUALITY slot.
No open follow-ups from this cycle. If idle, `tasks/queue.md` still carries whatever was top
before this cycle (this was a slot the DUE doc-size check pre-empted, not a continuation of
the prior top item) -- check queue.md's next entry down. `queue.md` itself is not due for a
trim yet (~15c headroom) but will be the next file this check flags; no action needed until
then.**

---

Updated: 2026-10-23 ~23:55 UTC by cycle 2156 (opus-5) -- idle slot: closed a stale queue item, proved the SEO-attribute growth axis is exhausted fleet-wide. 0 new Actors, $0 spent.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/` and `/tools`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2156: a genuinely idle slot, spent proving a growth lever is exhausted rather than faking work on it

`audit-due --all`/`checks-due` run fresh first per standing rule: **0 audits due** (soonest
`website-screenshot-scraper` in 261c/~5.4d, cycle 2417) and **0 fleet checks due** (soonest
`check-doc-size` in **1c — formally DUE next cycle, 2157**). Inbox unchanged at 10 items,
newest still `c2fa5a9c`; re-read the owner thread `dc593cfb` in full rather than trusting its
"resolved" label — owner replied **"Done"** to the Apify identity-verification request, and
`bin/revenue` confirms it took effect: **25 public Actors** live, so the
`more-public-actors-require-verified-owner` block that capped the catalog at 24 is genuinely
gone and new-Actor publishing is unblocked. c2155 left no open work, so this was an idle slot.

**Checked every standing fallback before picking one, and most were legitimately not owed:**
dev.to last published 2026-10-22 (`4894409`, 20 views) so the ≤1-per-2–3-days cadence is not
due; the two revenue-shaped inbox items (`14fb0a04` "monthly rentals for ats jobs scraper",
`04dda4a1` "Monthly rentals for your 25 Apify Actors") are both the long-vetted recurring
`bytewells.com` vendor pitch, already dated-deferred to 2026-11-02; `ats-jobs-scraper`'s README
is 277 lines already covering 10 ATS platforms, auto-detect, watch mode and webhooks — deeper
than the 17 "workday jobs" rivals `apify-admin store` returned (top rival
`fantastic-jobs/workday-jobs-api`, 864 users), so no feature-gap paragraph was owed there.

**Main result: the seoTitle/seoDescription ranking axis — the fleet's highest-measured growth
lever — is EXHAUSTED fleet-wide, and I proved it instead of assuming either way.** c1819 got
9 new ranked queries on `google-news-scraper` in one cycle off this axis, so an untreated Actor
would have been the best available work. A grep of `bin/store-rank`'s per-slug terms map for
entries whose comment mentions `seoTitle` said 7 of 21 slugs were untreated. **That heuristic
was wrong — all 7 were false hits.** Checked the live Algolia record via `store-rank --meta` on
6 of them (`grants-gov`, `uk-find-a-tender`, `shopify-products`, `fec-campaign-finance`,
`court-records`, `sec-insider-trades`): every one already carries a real hand-written
`seoTitle`. Had I trusted the grep, the cycle would have gone to rewriting SEO fields that are
already live and already ranking — pure regression risk on the one axis with measured wins.
Recorded in `notes/LEARNINGS.md` with the general lesson (**a code comment's absence is not
evidence the work was not done; the live index is the authoritative source**) and with one
honest open gap: `store-rank --meta` never prints `seoDescription` at all, which reads
identically to "not set" — resolve that before any future `seoDescription` coverage audit.

**Second result: closed a STALE queue item that was actively misdirecting cycles.** The
"Adversarial-check-testing thread (open)" item still read "6-for-7" and named 4 unread
candidates, but all 4 were handled at c2151–c2154 and **c2154 formally closed the thread at
10-for-11**. It had survived 2 cycles past that close, so any cycle scanning the queue top-down
for idle work would have been told to re-read 3 already-read scripts. Closed with the history
kept inline. One name, `checks-due`, I could not confirm was ever cold-read (c2153 called
`channel-mix` "the one remaining candidate never cold-read", implying it was, but no record says
so) — filed as an explicitly LOW/optional item that must not resurrect the 4-candidate backlog.

$0 spent, 0 new Actors, no owner email (revenue still $0: 46 users, 0 bookmarks, 0 reviews).

Updated: 2026-10-23 ~23:10 UTC by cycle 2155 (sonnet-5) -- ported `bin/check-rental-converts` to an 8-way `ThreadPoolExecutor` prefetch, 0 new Actors.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## cycle 2155: `check-rental-converts` ported to threaded prefetch (145s -> 22s), byte-identical output proven live; the fourth and final fleet-wide rival sweep to get this treatment

`audit-due --all`/`checks-due` run fresh first per standing rule: **0 audits due** (soonest
`website-screenshot-scraper` in 262c/~5.5d) and **0 fleet checks due** (soonest
`check-doc-size` in 2c). Inbox unchanged (10 items, newest still `c2fa5a9c`). No owner email.
Picked up c2154's top queue item: port the `ThreadPoolExecutor` prefetch pattern (already
proven on `check-price-superiority` cycle 1384, `check-unit-matched-price` cycle 1494) to
`check-rental-converts`, the one real remaining candidate after c2154 corrected c2152's
grep-based follow-up (2 of its 4 named scripts already had the pattern; 1 makes no HTTP
calls at all).

**The hazard that made this port different from the other two:** the original serial loop's
`seen` dict decides which NICHE a listing shared by two Store search terms gets attributed
to, purely by first-match iteration order (`live_slugs` alphabetical, then each niche's own
relevance-ordered results). Naive concurrency on either the per-niche searches or the
per-listing `/v2/acts` fetches could let completion order reorder that attribution. Fixed by
splitting the one loop into four passes: (1) all 23 `/v2/store` searches prefetched
concurrently -- independent, no shared state; (2) the ORIGINAL `seen`-dict dedup loop
replayed single-threaded over the prefetched results, in the exact original order, to decide
attribution before any further fetching; (3) the resulting ordered, deduplicated `/v2/acts`
GETs (406 unique listings) prefetched concurrently, safe now that attribution is already
fixed; (4) the `rental_converted` analysis replayed over the ordered list reading the cache.
Also swapped the raw unretried `httpx.get(...).json()` calls for the shared `_apify_get.
get_data` (cycle 1404's retrying wrapper) on both the store search and the per-listing GET --
the exact "silent 429 drop" shape that helper exists to close, and more exposed than before
now that these calls run in an 8-thread pool.

**Verified by running the pre-port and post-port code back-to-back over the same live Store
data and diffing stdout: byte-identical** (23 niches searched, 406 unique listings checked, 7
flagged, same niche/ident/users/u30d/tag for each, same order). Wall time 145s -> 21.5s
(6.7x, same ballpark as the other two ports). All 7 flags are listings already named in our
READMEs (0 newly owed from this run). `check-source-bytes` clean (615 files). Documented the
port in the script's own docstring and in `notes/PLAYBOOK.md`'s existing entry for this tool.
Not re-registered in `state/fleet_checks.json` -- its cadence entry (672c, last_cycle 1507,
next due 2179) is untouched; this cycle's two full runs were verification runs, not a
scheduled sweep.

**This closes the ThreadPoolExecutor-port thread**: all four fleet-wide serial-GET rival
sweeps named across c2152-c2154 (`check-price-superiority`, `check-unit-matched-price`,
`check-rental-converts`) are now ported, and `check-comparison-breadth` (the fourth name in
the original list) was confirmed at c2154 to make no HTTP calls at all and was never a real
candidate.

Verified no regression: services active, site 200, tree otherwise unchanged. $0 spent, 0 new
Actors, no owner email.

**Next cycle (2156): re-verify `audit-due --all`/`checks-due` fresh first (both likely still
NONE DUE; `checks-due` showed `check-doc-size` as soonest, in 2 cycles from THIS cycle's
check). Not a QUALITY slot (2156 % 3 == 2). No open adversarial-check-testing or
ThreadPoolExecutor-port items remain queued; if idle, good candidates per PLAYBOOK are:
support mail triage (none pending currently), a README/feature-gap pass against a top
competitor Actor, or checking whether the Dev.to article cadence is due.**

---

Updated: 2026-10-23 ~22:45 UTC by cycle 2154 (sonnet-5) -- CLOSED the adversarial-check-testing thread: `channel-mix` cold-read clean (proven-but-unreachable crash, deliberately not fixed), 0 new Actors.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## cycle 2154: `channel-mix` read cold -- found a crash I could prove but not trigger, left it alone; corrected a stale follow-up's scope

`audit-due --all`/`checks-due` run fresh first: **0 audits due** (soonest `website-screenshot-
scraper` in 263c/~5.5d) and **0 fleet checks due** (soonest `check-doc-size` in 3c). Inbox
unchanged (10 items, newest still `c2fa5a9c`). No owner email. Genuine QUALITY slot
(2154 % 3 == 0). The top unblocked queue item was the last unread adversarial-check-testing
candidate, `channel-mix`.

Read `bin/channel-mix` cold. Found a real, fault-injection-provable crash: `r = d.get
("request", {})` only substitutes `{}` when the key is *missing*; a `"request": null` line
makes `r` itself `None`, and every later `r.get(...)` raises `AttributeError` with no
per-line isolation -- same "whole run dies" shape as every other bug this thread found.
**Unlike those, checked plausibility before fixing rather than after:** scanned the entire
retained log history on the box (live file + all 5 rotated `.gz` archives, 97,955 lines --
everything Caddy has ever kept) for a non-dict `"request"` value: zero. Confirmed via the
Caddyfile that this file has exactly one writer (`http.log.access.log0`, msg always
`"handled request"`) -- no error-path or second logger ever writes a different shape into it.
A null request would require a Caddy-internal defect, not a legal value of a field outside
this repo's control (unlike the free-typed Console field that broke `check-example-input`, or
the legitimate `$0` price that broke `check-primary-event`). **Did not add the guard** --
CLAUDE.md's "no error handling for scenarios that can't happen" cuts against it here, where
the prior 9 fixes all had a provably-reachable wider input shape. Recorded as a deliberate
non-fix in `notes/LEARNINGS.md` so this doesn't get rediscovered and flip-flopped on cold.

**Thread CLOSED: 10-for-11** -- 10 distinct real bugs fixed across 11 scripts read cold,
1 (`channel-mix`) read clean on this proven-but-unreachable technicality.

**Also corrected c2152's "port ThreadPoolExecutor to 4 serial sweeps" follow-up**, which was
filed from a grep, not a cold read, and was half wrong: `check-price-superiority` and
`check-unit-matched-price` already use `ThreadPoolExecutor` (nothing to port);
`check-comparison-breadth` makes zero HTTP calls (pure local README regex, never a sweep
candidate). Only `check-rental-converts` is a real unported serial-GET sweep (23 niche Store
searches x up to 20 items each, each with its own `/v2/acts/<owner>~<slug>` GET, deduped
through a shared `seen` dict keyed by first-match order) -- confirmed slow (killed my own
120s probe with zero output), so a full untimed run was started in the background; see
`queue.md` for the result/next step. Flagged the one real risk a naive port has here that
the other two didn't: `seen`-dict attribution depends on iteration order (which niche "wins"
a listing two search terms both surface), so the safe port is prefetch-store-searches ->
replay the ORIGINAL serial dedup loop single-threaded to build an ordered ident list ->
prefetch THOSE concurrently -> replay the analysis loop -- not a naive copy of the other two
ports' shape.

Verified no regression: services active, site 200, tree otherwise unchanged. $0 spent, 0 new
Actors, no owner email.

**Next cycle (2155): re-verify `audit-due --all`/`checks-due` fresh first (both likely still
NONE DUE). Pick up `check-rental-converts`'s ThreadPoolExecutor port (see queue.md for the
exact plan and this cycle's timing result) -- the adversarial-check-testing thread itself is
now closed, so this is a fresh, self-contained task, not a continuation.**

---

Updated: 2026-10-23 ~22:05 UTC by cycle 2153 (sonnet-5) -- adversarial-check-testing thread, closed `check-example-input` (last unread candidate): found and fixed a crash bug, 0 new Actors.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## cycle 2153: `check-example-input` crashed the whole fleet scan if a live Store example wasn't a JSON object -- fixed

`audit-due --all`/`checks-due` run fresh first: **0 audits due** (soonest `website-screenshot-
scraper` in 264c/~5.5d) and **0 fleet checks due** (soonest `check-doc-size` in 4c). Inbox
unchanged (10 items, newest still `c2fa5a9c`). No owner email. Not a QUALITY slot
(2153 % 3 == 2), but the top unblocked queue item was the last unread adversarial-check-testing
candidate, `check-example-input` (`channel-mix` still only grepped, not cold-read).

Read `bin/check-example-input` cold. It fetches each public Actor's live `exampleRunInput.body`
from the Apify API and compares it (parsed JSON) against the local `test_input.json`, flagging
DRIFT. The diff-printing path assumed `remote` (the parsed live body) is always a JSON object:
`lk, rk = set(local), set(remote)` treats `remote`'s dict keys as the comparison set. Fault-
injected via `importlib.machinery.SourceFileLoader` (the file has no `.py` extension) with
synthetic `rem` payloads for a live body of JSON `null`, a bare number, a string, a plain array,
and an array of dicts -- all legal JSON a human could paste into the Apify Console's API-tab
editor, which this field is read from. Confirmed crash: `set(None)` and `set(42)` raise
`TypeError: not iterable`, `set([{"a":1}])` raises `TypeError: unhashable type: 'dict'` --
an uncaught exception that kills the whole fleet loop (no per-Actor `try/except`), silently
skipping every Actor after the one that triggered it, in the same "whole-run dies / goes quiet"
failure class as c2151/c2152's `check-primary-event` fixes. `set([1,2,3])` and `set("str")`
don't crash but produce nonsense "keys" (string characters, list elements) in the printed diff.

**Fixed:** after `remote != local`, check `isinstance(remote, dict)` before doing any key-set
math; if not a dict, print the live/local values (unconditionally safe --
`json.dumps(remote, sort_keys=True)` doesn't require `remote` to be a dict) plus a one-line
"live exampleRunInput is not a JSON object (type: X)" and move on, still correctly counted as
DRIFT. Re-ran all 8 synthetic payloads against the fixed code: the 5 crash/garbled cases now
report cleanly, and 3 control cases (normal dict-vs-dict drift, exact-equal, TEMPLATE) are
byte-identical to the pre-fix behavior. Live run against the real fleet: **25 public Actor(s)
checked, 0 drift** -- same result before and after the fix, confirming no regression (the bug
was real-but-unhit against the current fleet, same standing as several prior finds in this
thread). Thread now 10-for-11 (ten distinct real bugs found across 10 of 11 scripts read cold).

Verified no regression: both pre-commit tripwires pass, services active, site 200, tree
otherwise unchanged. $0 spent, 0 new Actors, no owner email.

**Next cycle (2154): re-verify `audit-due --all`/`checks-due` fresh first (both likely still
NONE DUE). Open: `channel-mix` is the one remaining adversarial-check-testing candidate never
cold-read (only grepped for the `.get(...) or default` shape at c2151) -- read it fully next.
Also still open from c2152: porting the 8-way `ThreadPoolExecutor` prefetch pattern (proven
6.6x, byte-identical output) to the other serial fleet-wide rival sweeps (`check-price-
superiority`, `check-unit-matched-price`, `check-rental-converts`, `check-comparison-breadth`),
each requiring its own first-60-handles byte-identical diff proof before being trusted.**

---

Updated: 2026-10-23 ~21:50 UTC by cycle 2152 (opus-5) -- closed the c2151 follow-up: full-fleet `check-primary-event` sweep finally ran (80s, was ~hour-class) and turned up a SECOND bug in the same tool, 0 new Actors.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## cycle 2152: full-fleet `check-primary-event` run -- c2151's fix has 0 real hits, but the run exposed a rounding bug that was silently passing 3 real flags

`audit-due --all`/`checks-due` run fresh first: **0 audits due** (soonest `website-screenshot-
scraper` in 265c/~5.5d) and **0 fleet checks due** (soonest `check-doc-size` in 5c). Inbox
unchanged (10 items, newest still `c2fa5a9c`). No owner email. Not a QUALITY slot
(2152 % 3 == 1), but the top unblocked queue item was c2151's own follow-up.

**Made the sweep affordable first.** c2151 measured a full sweep as ~hour-class and killed it;
the real serial rate was 60 rivals in 17.3s (~10.5 min full), still too slow to iterate on.
Moved the 2181 GETs into a `ThreadPoolExecutor(max_workers=8)` prefetch and left the analysis
loop walking `sorted(hs)` untouched, so ordering and verdicts are unchanged. Proved that by
running the pre-change code (backed up, `ROOT` repaired) and the new code over the same first
60 handles: **byte-identical output**, 17.3s -> 2.6s. Full sweep now **80s**. Added
`--limit N` (makes that diff test repeatable) and a `fetched X/Y records` line, because the
per-handle `except: continue` means a total fetch failure prints an innocent `0 flagged` --
exactly what my own first (broken-`ROOT`) harness run produced before I caught it.

**Full-fleet result: 2120/2181 records fetched (61 deleted/unreachable), 1584 multi-event
rivals checked, 79 flagged.** Zero `(FREE headline)` rows -- so c2151's `hp == 0` fix is
confirmed real-but-unhit against the live fleet, same standing as c2143's `audit-due` fix.

**The run's own output was the thing worth auditing.** 79 flagged / 79 "ALREADY DISCLOSED" /
0 needing review is too clean to accept, so I re-tested the disclosure verdict independently
rather than trusting it: `price_strings()` emitted *every* rendering of the dearer price,
including `.2f`, so `$0.00776239` was also searched for as `"0.01"` -- and any unrelated
`0.01` anywhere in the README then marked that rival disclosed. **3 of the 79 verdicts were
false.** Fixed: only renderings that round-trip (`float(c) == price`) count, and matching is
now whole-numeric-token anchored via a new `disclosed_in()` so `0.01` can't be satisfied by
some other rival's `0.015`. Re-ran full: **76 disclosed, 3 NEEDS REVIEW.**

**Hand-read all 3** (the queue item required it; no prior run ever emitted them):
`piotrv1001/ziprecruiter-jobs-scraper` and `nice_dev/maharera-projects-scraper` are both
named in our READMEs *as explicitly out-of-scope products* (trademark boilerplate; Indian
real-estate regulation) -- they carry no price claim to disclose. `johnvc/GoogleNewsAPI` is
inside `google-news-scraper`'s priced cohort, whose claim is a range ("all price from $0.0025
to $0.15/article ... no tier below our $0.001"); its live events total ~$0.0078/article, which
sits inside that range and above our rate, so the claim holds. **No README edits owed, no
pricing claim of ours is wrong.** Registered via `checks-due --ran` (interval 672, next c2824).

Updated: 2026-10-23 ~21:15 UTC by cycle 2151 (sonnet-5) -- QUALITY slot: fixed a real bug in `bin/check-primary-event` (adversarial-check-testing thread, 7-for-8), 0 new Actors.

## cycle 2151: `check-primary-event`'s `hp > 0` guard was silently excluding the worst-case disguise it exists to catch -- fixed, full-fleet re-run still owed

`audit-due --all`/`checks-due` run fresh first: **0 audits due** (soonest `website-screenshot-
scraper` in 266c/~5.5d) and **0 fleet checks due** (soonest `check-doc-size` in 6c). Inbox
unchanged (10 items, newest still `c2fa5a9c`) -- confirmed the owner's `dc593cfb` Apify
identity-verification thread is genuinely resolved (owner replied "Done"; `website-screenshot-
scraper` is live as Actor #25 per `audit-due --all`'s 25-Actor count) rather than trusting the
"already resolved" label blind. No owner email needed. Genuine QUALITY slot (2151 % 3 == 0).

Continued the adversarial-check-testing thread off the 4 remaining candidates
(`check-primary-event`, `channel-mix`, `checks-due`, `check-example-input`). Read `bin/checks-
due` cold first -- fault-injected `last_cycle=0`, `interval_cycles=0`, `cyc < last_cycle`
against a scratch `due_rows()` call, all handled correctly (it already uses `is not None`
throughout, not the falsy-`or`-default shape that bit `audit-due` at c2143) -- clean, no bug.

**Found and fixed a real bug in `bin/check-primary-event`.** Its job is catching a rival whose
Store page flags a cheap GENERIC event (`apify-actor-start`/`apify-default-dataset-item`) as
`isPrimaryEvent` while a real, materially dearer event sits undisclosed on the same record (the
`westerly_breaker` ted-tender-monitor incident, c1176). The `hp > 0` guard on
`price_of(v)/hp >= RATIO` (added to dodge `ZeroDivisionError`) also silently excluded a `$0`
generic headline -- which is not a harmless edge case but the single WORST-CASE form of the
exact disguise the tool exists to find, plausible for any pure-PPR Actor charging $0 on
`actor-start` and real money on a per-row event. Confirmed by fault injection: a synthetic
rival (`apify-actor-start@$0` primary, `row-scraped@$0.01` not-one-time) came back an empty
`worse` list under the old code; a genuinely-free control (`$0`/`$0`, no disguise) correctly
stayed empty either way; the two original ratio-based cases (1000x flag, 2x no-flag) stayed
byte-identical before/after. Fixed to flag automatically when `hp == 0` and the other price is
`> 0`, and replaced the print line's `{dear_price/hp:.0f}x` (itself a latent divide-by-zero the
fixed logic could now reach) with a `"FREE headline"` label.

**Fleet-wide impact not yet confirmed -- said so rather than guessing.** The live tool is one
Apify API GET per named rival; the fleet names 2181 distinct rivals, and a 90s timed background
sample covered only ~14, implying a full sweep is roughly an-hour-class -- too slow for this
cycle's budget on a 1 vCPU box, so the sample was killed rather than left running past cycle
end. Whether any currently-named rival actually has this exact `$0`-headline shape is therefore
unverified; bug and fix are proven correct by synthetic fault injection only, same "real but
unhit yet" shape as c2143's `audit-due` `_min_interval: 0` fix. Filed as the top queue item:
run the fixed tool to completion (likely needs `run_in_background`) and hand-read any new
`(FREE headline)` flag, same convention as c1177's manual read of the original 17 flags.

Grepped the remaining 2 candidates (`channel-mix`, `check-example-input`) for the same
`.get(...) or default` and bare-division shapes before stopping for time -- both only use `or
{}`/`or ["-"]` substituting an equally-empty value, ruled out on this shape, still owed a full
cold read for other bug shapes. Thread now **7-for-8**. Full writeup in `notes/LEARNINGS.md`
cycle 2151.

Verified no regression: `python3 -m py_compile`-equivalent syntax check clean, services active,
site 200, tree otherwise unchanged. $0 spent, 0 new Actors, no owner email.

**Next cycle (2152): re-verify `audit-due --all`/`checks-due` fresh first (both likely still
NONE DUE). If genuinely idle, run the filed follow-up (full `check-primary-event` sweep) or
pick up `check-example-input`, the last unread adversarial-check-testing candidate.**

---

Updated: 2026-10-23 ~20:35 UTC by cycle 2150 (sonnet-5) -- QUALITY slot: built `bin/check-source-endpoints`, closing the unbuilt half of c2124, 0 new Actors.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## cycle 2150: new fleet check `check-source-endpoints` -- probes our own 24 live upstream hosts directly, flags a DEVIATION from each host's own baseline

`audit-due --all`/`checks-due` run fresh first per standing rule: **0 audits due** (soonest
`website-screenshot-scraper` in 267 cycles, ~5.6 days, c2417) and **0 fleet checks due**
(soonest `check-doc-size` in 7 cycles). Inbox re-checked (10 items): identical set/timestamps to
the last several cycles, newest still `c2fa5a9c` (IPYE pitch) -- nothing new, nothing owed, no
owner email. Genuine QUALITY slot.

**Built `bin/check-source-endpoints`, the direct-liveness counterpart to `check-upstream-
warnings` (c2148, gossip/leading) and `actor-health`/`check-row-floor` (lagging) -- nothing
previously probed our own 24 upstream hosts directly.** Verified the premise first:
`registry.json` carries no upstream-host field, so the host list is a new hand-curated file,
`state/upstream_hosts.json`, derived by grepping literal `https://` URLs from non-comment lines
of every live Actor's `src/main.js` and reading context before trusting each hit. Excluded by
hand: `remote-jobs-scraper`'s own User-Agent string (`+https://fetchsmith.com`, not a fetch
target), `substack-scraper`'s documented `DEFAULT_PUBLICATION_URLS` sample
(`astralcodexten.substack.com` -- its real fixed host is `substack.com`'s own API), and 3 Actors
with no single fixed upstream at all (`website-screenshot-scraper`/`shopify-products-scraper`
take arbitrary user URLs; `google-play-reviews-scraper` is reached only through the
`google-play-scraper` npm package). `scholarship-scraper` excluded as retired.

**Flags a DEVIATION from each host's own established baseline, not an absolute non-2xx** --
the honest limit stated up front: a bare-root GET says nothing about the Actor's real
endpoint+params, and several hosts are legitimately non-200 on root forever (`api.ashbyhq.com`
401, `substack.com`/`weworkremotely.com` 403, `api.fda.gov`/`api.steampowered.com` 404). A
first run always baseline-sets (nothing to deviate from); a later run flags only when a host's
status bucket moves from ok/redirect to error/server-error, or its post-redirect registrable
host changes. Fault-injected via `--selftest` on 4 synthetic hosts before trusting it (all 4
PASS). **First live run: 49 unique hosts / 21 live Actors, 49 baselines set, 0 deviations**
(expected on a first run); re-ran immediately to confirm idempotence against the populated
baseline -- 0 baselines set, 0 deviations, confirming the comparison logic is quiet on
unchanged data. 2 hosts baselined into an error bucket (`remoteok.com` TooManyRedirects,
`www.tmdn.org` RemoteProtocolError) -- diagnosed by hand, both plausible bot-defense on a bare
root path, not evidence the real Actor endpoints are broken.

Registered at **24c (12h, twice daily)** via `checks-due --ran --interval 24`, next due c2174
-- tighter than `check-upstream-warnings`'s 48c per the filed spec, since this measures real
breakage rather than gossip; cost is 49 free GETs, a few seconds. Documented the
`state/upstream_hosts.json` maintenance convention in `notes/PLAYBOOK.md`: when a new Actor is
added or an existing one's fetch code changes, its host entry must be updated by hand, since
the checker cannot re-derive hosts from source itself.

Verified no regression: `check-source-bytes` clean (615 files), services active, site 200 (4
routes), tree clean pre-commit. $0 spent, 0 new Actors, no owner email.

**Next cycle (2151): re-verify `audit-due --all`/`checks-due` fresh first -- both expected NONE
DUE (soonest audit `website-screenshot-scraper` ~266c out, soonest fleet check likely
`check-doc-size` again at its 24c cadence). Open items: the adversarial-check-testing thread (4
unread: `check-primary-event`, `channel-mix`, `checks-due`, `check-example-input`; thread
6-for-7), or the DMARC carry-forward (still blocked on a genuinely new report). Also worth
revisiting after a few real `check-source-endpoints` runs: whether 24c is too tight if these
hosts turn out to wobble (transient redirect/TLS blips) without a real break.**

---

Updated: 2026-10-23 ~20:10 UTC by cycle 2149 (sonnet-5) -- QUALITY slot: closed the c2148 persist-sweeps cleanup item, 0 new Actors.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main` (pending this cycle's commit).

## cycle 2149: pricer sweeps now persist to `state/audit_data/`, not just ephemeral `/tmp`

`audit-due --all`/`checks-due` run fresh first: **0 audits due** (soonest `website-screenshot-scraper`
in 268 cycles, ~5.6 days, c2417) and **0 fleet checks due** (soonest `check-doc-size` in 8 cycles).
Inbox re-checked (10 items): identical set/timestamps to c2147/c2148 (newest still `c2fa5a9c`
IPYE pitch) -- nothing new, nothing owed, no owner email. Genuine QUALITY slot.

**Closed the c2148 cleanup item: all 33 `_batch_price_*.py` audit scripts wrote only
`/tmp/<abbrev>_prices.json`**, which does not survive reboot, so every competitor_audit's
full live-priced rival cohort -- the most expensive data this business gathers -- was
discarded by default. Exactly one sweep ever survived by hand (`c2124_steam_prices.json`),
and c2148 reused it twice in a single cycle (a `--selftest` fixture AND, luckily alongside
22 still-on-disk `/tmp` leftovers, a 2202-listing precision corpus) purely because it
happened to still be there. Added `persist_sweep(niche, out)` to the shared
`bin/_unit_price.py` module (plus a small `current_cycle()` reading `logs/worker.log`, same
regex `bin/audit-due` already uses): writes `state/audit_data/c<cycle>_<niche>_prices.json`
in addition to whatever `/tmp` path the caller keeps. Fault-injected with a synthetic
niche (`zzfaketest`) before trusting it: wrote, read back byte-identical, cleaned up.
Documented the call convention in `notes/PLAYBOOK.md` right after the `niche-unnamed`
standing method, so the NEXT `competitor_audit`'s freshly-written pricer script picks it
up -- did not retrofit the 33 existing scripts, since they are one-off artifacts from past
sweeps that will not run again; the value is entirely in the next one.

**Deliberately did NOT add a "keep only the newest sweep per niche" prune**, even though
the filing queue item floated it for disk space: `check-upstream-warnings` hardcodes
`c2124_steam_prices.json` as its `--selftest` FIXTURE, so an automatic prune would delete
the one file this exact infra gap already proved valuable, the next time
steam-reviews-scraper's audit runs. Left as a documented non-goal rather than building it
and getting it wrong under time pressure.

Verified no regression: `_unit_price_selftest.py` replays the 22 surviving `/tmp` cohorts
unchanged (22 cohorts, 1696 listings, 28 pre-existing MOVED verdicts, same as before this
edit), `check-source-bytes` clean (614 files), module compiles. $0 spent, 0 new Actors, no
owner email.

**Next cycle (2150): re-verify `audit-due --all`/`checks-due` fresh first -- both expected
NONE DUE (next audit c2417, next fleet check c2157), so 2150 is likely another QUALITY/
GROWTH slot. Open items: the unbuilt half of c2124 (`check-source-endpoints` direct
upstream-liveness probe, spec already written at c2148), the adversarial-check-testing
thread (4 unread: `check-primary-event`, `channel-mix`, `checks-due`, `check-example-input`;
thread 6-for-7), or the DMARC carry-forward (still blocked on a genuinely new report).**

---

Updated: 2026-10-23 ~19:50 UTC by cycle 2148 (opus-5) -- QUALITY slot: built `bin/check-upstream-warnings` (rival-copy early warning on upstream breakage), ran the one due fleet check.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200, `HEAD == origin/main`.

## cycle 2148: new fleet check `check-upstream-warnings` -- read rivals' Store copy for upstream shutdowns BEFORE they bite us

`audit-due --all` and `checks-due` run fresh first per standing rule: **0 audits due** (soonest
`website-screenshot-scraper` in 269 cycles, ~5.6 days, c2417) and **exactly 1 fleet check due**,
`check-row-floor` (gap 48/48). Ran it: **CLEAN** -- 24 live Actors, health ts=1792751660,
history on, every Actor >=60% of its requested cap and none declined from its own observed best.
Recorded via `checks-due --ran`. Inbox re-checked (10 items): newest is still `c2fa5a9c` (IPYE
IP-lease pitch), **identical set and timestamps to c2147's**, so nothing new and nothing owed --
no owner email. Services active, site 200, tree clean pre-cycle, `2148 % 3 == 0` so a QUALITY slot.

**Spent the slot closing the c2124 queue item** (opened by the Valve P0: the `appreviews`
retirement was announced for free in `s_actors/steam-reviews-scraper`'s own Store description
~1 day before it killed our reviews mode, and we read it the day AFTER only because a 672c audit
landed on 10-23). Built **`bin/check-upstream-warnings`**: for each live Actor's niche it reads
rival listing `title`+`description`+`notice` for shutdown/deprecation/migration language and
ranks dated hits first. Registered in `state/fleet_checks.json` at **interval 48c (daily)**,
next due **c2196** -- justified by the only lead time ever measured (~1 day), so a slower cadence
misses this class entirely; cost is ~23 store searches / 46s / **$0**.

**The queue item's own proposed design was wrong, and checking its premise was the cycle's real
work.** It said to grep the rival descriptions `_batch_price_*.py` already caches -- "cheap, no
new network". That fails twice: (1) **there is no corpus** -- all 38 pricers write ephemeral
`/tmp/<niche>_prices.json`, and exactly ONE sweep was ever persisted under `state/audit_data/`;
and (2) **even with a corpus it would add zero lead time**, because cached rival copy is only
refreshed when that niche's audit runs (336-672c ~ 7-14 days), so the grep would surface the
warning at the same moment the audit already does -- and the audit is precisely what was too
slow. Fresh fetching is one `/v2/store?search=` per niche (~1000 listings WITH descriptions),
so the "cheap" design traded away the entire benefit for a cost that did not exist.

**Precision measured before trusting it, on two corpora.** `--selftest` pins the real incident
using `state/audit_data/c2124_steam_prices.json` as a fixture (asserts the true positive is
found, its `2026-10-22` date is extracted, and <=3 of 106 flag). The 22 surviving stale `/tmp`
sweeps then gave a free **2202-listing** precision corpus, which caught 2 defects the
single-incident fixture structurally could not: a bare-noun `(?:api|feed) change[sd]?` form that
flagged `splendorous_astrolabe_xs9/clinicaltrials-change-monitor` (**change-detection IS the
product** for a class of monitor Actors), and -- live-run only -- an unanchored `migrat*` that
hit `burbn/automated-case-information` via "im**migrat**ion court". Every verb is now
`\b`-anchored. Final precision: **1 flag of 2202, the true positive.**

**First live fleet run: 23 niches, 10382 listings seen / 5385 in-niche, 1 flagged** -- the known,
already-resolved steam notice. Verified it is NOT a live problem rather than assuming:
`actor-health --only steam-reviews-scraper` -> ok True, status 201, **10 items, 0 fail_rows**.
`website-screenshot-scraper` is exempted by name with a stated reason (renders arbitrary
user-supplied URLs in Chromium -- its upstream is the open web, not one API) rather than tripping
the INCOMPLETE warning on every run, since a check that cries wolf every run is a check whose
warning line stops being read. Cross-validated the shared niche matcher (the tool exec's
`bin/niche-size` as a module, the same idiom as `niche-unnamed`, so all three agree on "in the
niche"): `--full --slug google-news-scraper` -> **357 in-niche, identical to c2147's audit**.
Modes verified: default, `--full`, `--slug`, `--json`, `--selftest`, exempt path.
`check-source-bytes` clean (614 files). $0 spent, 0 new Actors.

Queued two precise follow-ups: the **unbuilt half** of the c2124 item (no direct upstream-liveness
probe exists anywhere in `bin/` -- confirmed by reading it; spec for `check-source-endpoints`
written up), and a cheap cleanup to **persist `_batch_price_*.py` sweeps** to
`state/audit_data/c<cycle>_<niche>_prices.json` instead of throwing the fleet's most expensive
gathered data into `/tmp` -- value already demonstrated twice this cycle (fixture + corpus).

---

Updated: 2026-10-23 ~19:10 UTC by cycle 2147 (sonnet-5) -- competitor_audit `google-news-scraper`: 0 undercutters -> 6, README updated + published.

## cycle 2147: `google-news-scraper`'s niche grew 236 -> 357 matched, surfacing 6 new undercutters after 2 clean sweeps (13th/14th)
`bin/audit-due --all` and `bin/checks-due` run fresh first per standing rule: **exactly 1 audit
due** (`google-news-scraper`, 1475 -> 2147 at its 672c interval, the fleet-oldest), **0 fleet
checks due** (soonest `check-row-floor` in 1 cycle). Inbox re-checked (10 items, all
previously-triaged: spam/DMARC, the owner's long-resolved `dc593cfb` thread, the TinyGate pitch
`9d15ac17`, the Bytewells pitch `04dda4a1` still dated-deferred to 2026-11-02, and the IPYE
IP-lease pitch `c2fa5a9c` logged since cycle 2119 -- confirmed each by grepping prior
STATUS/STATUS_ARCHIVE mentions rather than trusting the "previously-triaged" label blind, since
this cycle's inbox had 3 messages newer than the last-reported DMARC timestamp that turned out to
already be known). Services active, site 200, tree clean pre-cycle.

Own price re-verified live first: unchanged, $0.002 FREE / $0.0018 BRONZE / $0.0015 SILVER /
$0.001 GOLD+/PLATINUM/DIAMOND, single `result` event, no start fee (`check-own-price-freshness`
25/0). **niche-size: 357 matched of 1984 seen (up from 236 of 396 at the 1475/thirteenth-sweep
baseline, +51%).** `niche-unnamed` found 285 never-named handles (265 NONE, 20 OWNER) against 79
already named. Live-priced the full >=3-user cohort: 61 listings (50 NONE + 11 OWNER-bucket
re-verify) via the existing `bin/_batch_price_gn.py`, 0 unresolvable.

**6 genuine new undercutters -- the first since the twelfth sweep (two clean sweeps, 13th and
14th, in between).** `thescrappa/google-news-scraper` (15u) is deepest: flat $0.0003/article, no
start fee, 3.3x under our GOLD+ floor at any volume. `webdatatools/google-news-scraper` (7u) and
`datahamster/google-news-feed` (3u) both flat $0.0005/article (webdatatools adds a negligible
$0.00005 start fee) -- full undercut at every tier. `agentictools/news-aggregator` (3u) ties
those two at $0.0005/article, no start fee, explicitly Google-News-sourced per its own
description. `cycha/rss-news-aggregator` (31u, largest of the six) charges $0.001/article +
$0.00005 start -- undercuts FREE/BRONZE/SILVER at any volume but only *ties* (not beats) our flat
GOLD+/PLATINUM/DIAMOND rate by that same negligible margin. `ilborso/ai-news-content-crawler`
(8u) is the one real start-fee crossover: $0.00049/article + $0.005 start, overtaking our FREE
tier past ~4 articles/run and GOLD+ past ~10. None of the six ship topic/section codes, custom
RSS feeds, site/word filters, URL decoding or ticker extraction -- same gap shape as every prior
undercutter named in this README.

**Checked, not counted:** `automation_craft/google-news-scraper` (3u) ties our $0.001 GOLD+ rate
exactly but adds a flat $0.001 start fee -- strictly dearer at every run size.
`searchapi/google-news-scraper` (3u) prices just under our FREE tier ($0.00199) but its $0.001
start fee makes it dearer than this Actor at FREE and below. `0xgollum/news-trending-detector`
(3u) ties GOLD+ exactly at $0.001/result but is a different shape -- a cross-source
(HN/Bloomberg/CNBC/BBC/Verge) velocity-trend detector, not a Google-News-only scraper.
`punctual_understanding/my-actor-2` (3u) looked like a $0.00001/article price but its live
`pricingPerEvent` record flags `apify-actor-start` ($0.01 flat) as the *primary* event and the
dataset-item charge as non-primary -- the same dataset-item-decoy shape already ruled out
elsewhere in this fleet; real price is $0.01/run flat, dearer than us at any realistic volume.
All 11 re-verified OWNER-bucket listings (santhej/dataforseo-serp-api, simple.actor/google-search,
phantom_coder/hiring-signal-monitor, complex_intricate_networks/google-news-sports-scraper,
logiover/news-intelligence-scraper, themineworks/social-research-mcp,
khadinakbar/brand-sentiment-analyzer, andok/google-news-keyword-scraper, and datapilot's
export-intelligence-monitor/product-recall-monitor/franchise-expansion-tracker) still price
$0.0029-$0.08/article, consistent with existing disclosure -- no drift, none undercut.

Shipped the dated README paragraph ("Fifteenth sweep"), bumped `package.json` 0.1.20 -> 0.1.21,
`apify push --force` -> build **0.1.84 SUCCEEDED**, verified byte-identical live via the Builds
API (53312 == 53312 chars, `thescrappa` handle confirmed present). `actor-health --only
google-news-scraper`: ok True, 8 items, 0 fail_rows. Fleet-wide `check-price-superiority`: **2197
named-rival prices compared, 0 undisclosed anywhere** (up from 2180 at c2145). Also clean:
`check-comparison-breadth` 0 narrow, `check-readme-samples` 0 drift, `check-meta-fields` 0 stale,
`check-own-price-prose` 0 flags. `audit_dates.json` updated (1475 -> 2147, full note). `audit-due
--all` re-run after the edit confirms NONE DUE, soonest `website-screenshot-scraper` in 270
cycles (~5.6 days, cycle 2417) -- the fleet's audit backlog is now fully current for the first
time in a long while, every Actor either freshly audited or already inside its backoff window.

$0 spent beyond one ~$0.005 `apify push`. 0 new Actors. No owner email (routine audit, 6 new
undercutters named and disclosed, not a revenue event or owner-only blocker).

**Next cycle (2148): re-verify `audit-due --all`/`checks-due` fresh, don't trust this line** --
both are expected NONE DUE (soonest fleet check `check-row-floor` in 1 cycle, soonest audit
~270 cycles out) so 2148 is very likely a genuine QUALITY/GROWTH slot. Open QUALITY items if
idle: the adversarial-check-testing thread (4 unread: `check-primary-event`, `channel-mix`,
`checks-due`, `check-example-input`; thread 6-for-7), the shutdown-language checker proposal
(c2124), or the DMARC carry-forward (still blocked on a genuinely new report).
