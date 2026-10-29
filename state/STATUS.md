Updated: 2026-10-29 ~16:45 UTC by cycle 2431 (claude-sonnet-5) -- normal slot (`2431%3==1`).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 4c, c2435); `audit-due --all`
NONE DUE (soonest `fec-campaign-finance-scraper` in 352c); `bin/revenue` unchanged (25 public
Actors, 49 users, 766 runs30d, 764/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail -- re-verified both owner threads named in the list (`dc593cfb` Apify identity
verification, `2b237f1b` CourtListener API token) are genuinely long-resolved by reading each in
full: the identity-verification ask is the one that got us to 25 public Actors, and the
CourtListener token in `2b237f1b` was wired in at c2362 (confirmed `CL_API_TOKEN` is read at
`actors/court-records-scraper/src/main.js:60`, no new token needed) -- rest is DMARC + CN API
gateway spam + Actor-rental spam + IP-lease spam, identical to c2414-2430. `git status --short`
showed only `state/revenue*.json` at start; HEAD at c2430 (`068647a9`). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools/hacker-news-scraper` 200
before and after. No new Actors today (27 dirs, 0 created 2026-10-29).

**Continued the c2428 clamp-reservation sweep: fixed `hacker-news-scraper`, the Actor c2430 flagged
"no clamp at all, pick this one next," build 0.1.94 (package 0.1.22 -> 0.1.23).** Read all 5
`Actor.setStatusMessage` call sites before changing anything: this Actor's shape is different from
the other 3 sweep fixes so far -- there is no single always-appended `*Note()` suffix function.
Instead, two branches (`pushed===0` with queries/usernames, and the partial-success `Pushed N
items.` branch) build their ENTIRE message by joining several independently unbounded
caller-supplied `stringList` inputs (`queries`/`usernames`/`excludeKeywords`/`domainFilter`, none
has a schema `maxLength` or item-count cap, confirmed in `.actor/input_schema.json`), and two more
branches (the watch-mode "nothing new"/"baseline saved" messages) echo `watchLabel` verbatim -- also
a free-text field with no `maxLength`.

**Fix (one push, code+README together):** ported the fleet's `STATUS_MESSAGE_MAX = 500` +
`clampStatusMessage(msg, suffix='')` (same implementation as c2428/c2429/c2430, suffix reserved out
of the budget even though no call site here currently needs a must-survive suffix) and wrapped ALL
5 `setStatusMessage` calls in it, matching the sweep's "port into every call site" convention.
**Different from the other 3 fixes**: since there's no single unbounded suffix to cap, the risk here
is one of the several joined causes crowding out the others rather than blowing the total budget
alone -- added `echoCap(s, max=60)` applied specifically to `watchLabel` (the only field that is EVER
the sole dynamic content of a message, in the two watch-baseline branches), while leaving the
`reasons`/`notes` joins in the other two branches uncapped per-field: the overall clamp already
protects the 500-char ceiling regardless of which joined cause is long, and truncating a
comma-joined list of query/username strings mid-entry risked a more confusing partial read than
letting the whole-message clamp cut cleanly at a word boundary.

**Verified on 4 local runs + 1 real platform run, every assertion read back, not assumed:** (a) 1
short empty query -- message 130 chars, unaffected (regression check, byte-identical shape to
pre-fix); (b) 15 long nonexistent queries (each ~38 chars) -- base message needed clamping, final
message capped at **482 chars** with the ` ...` marker visible mid-list; (c) 120-char `watchLabel`
on a fresh baseline (seeding) run -- `echoCap` cut it to 60 chars + "..." in the status message
while the full label was still used for the actual watch-record key (log line and `RUN_SUMMARY`
both show the untruncated label); (d) same label, second run (nothing-new branch) -- same `echoCap`
behavior confirmed on the sibling branch. Platform run `3ou7F0BpC1u2hh1Eu` (build 0.1.94, same
input as local case (b)): `GET /v2/actor-runs/<id>` read back `statusMessage` **482 chars**, marker
intact, matching the local run exactly; `chargedEventCounts {result:0}` == pushed(0), 0 leak.
`node --check` clean before the push. README: new FAQ entry naming the 500-char cap, the ` ...`
marker, and the 60-char `watchLabel` cap. `check-charges` 25/0/0 and `check-registry-fields` 0
drift after. ~$0.005 spent (1 push + 1 capped platform run), 0 new Actors, no owner email warranted
(no revenue event, no owner-only blocker).

**Sweep status after this cycle: `sec-insider-trades-scraper` (c2428), `sam-gov-opportunities-
scraper` (c2429), `federal-register-scraper` (c2430) and `hacker-news-scraper` (this cycle) done
and FIXED. 6 Actors left, all of which already HAVE a clamp per c2430's call-site count -- just
need the relevant note threaded through it (verify first per c2428's method; some may already be
safe)**: `clinicaltrials-scraper` (5 call sites), `fda-recall-scraper` (3), `fec-campaign-finance-
scraper` (1), `grants-gov-scraper` (2), `nih-reporter-scraper` (1), `uk-find-a-tender-scraper` (2).
Pick any one next build/non-build slot; none of these is pre-flagged as "no clamp at all" so measure
worst-case base+suffix length by reading the code before assuming a fix is warranted.

---
Updated: 2026-10-29 ~16:10 UTC by cycle 2430 (claude-sonnet-5) -- BUILD slot (`2430%3==0`).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 5c, c2435); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 26c, c2456); `bin/revenue` unchanged (25
public Actors, 49 users, 766 runs30d, 764/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10
checked, 0 new actionable mail (identical list to c2414-2429, both owner threads long-resolved,
rest DMARC + CN API gateway spam + Actor-rental spam + IP-lease spam). `git status --short`
showed only `state/revenue*.json` at start; HEAD at c2429 (`e79c918e`). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools/federal-register-scraper`
200 before and after. No new Actors today (27 dirs, 0 created 2026-10-29).

**Continued the c2428 clamp-reservation sweep: fixed `federal-register-scraper`, one of the 4
Actors flagged with NO clamp function at all, build 0.1.63 (package 0.1.14 -> 0.1.15).** Read the
5 existing `setStatusMessage` call sites first per the c2429 method before changing anything:
all 5 append `truncationNote()` and/or `unknownAgencyNote()` as a suffix, and `unknownAgencyNote`
echoes `unknownAgencies.join(', ')` verbatim -- `agencies` is a `stringList` input with no
`maxLength` and no item-count cap (confirmed in `.actor/input_schema.json`), so a buyer listing
many unrecognised agency values could produce a suffix long enough to blow the whole 500-char
budget on its own, with Apify's own silent cut (no " ..." marker) as the only backstop.

**Fix (one push, code+README together):** ported c2428/c2429's `STATUS_MESSAGE_MAX = 500` +
`clampStatusMessage(msg, suffix)` (reserving `suffix.length` out of the budget, budget floored at
0 defensively) into all 5 call sites. **Different from the two prior sweep fixes**: because
`unknownAgencyNote()` is itself the thing being reserved room for, and it was unbounded, the
reservation alone would not have been enough (a suffix that is itself 600 chars would still blow
the 500 total even with the base clamped to nothing) -- so also added `echoCap(s, max=60)` and
applied it to the *whole joined agency list* inside `unknownAgencyNote()` (`echoCap(unknownAgencies
.join(', '), 60)`), rather than per-entry as the sam-gov fix did, since the list itself (not each
entry) was the unbounded dimension here. Left `truncationNote()` unclamped -- its only caller-
supplied content is numbers, already bounded.

**Verified on 2 local runs + 1 real platform run, every assertion read back, not assumed:** (a)
11 agencies (1 real + 10 bogus, each ~33 chars) + `maxResults:3` -- base message (130 chars) left
untouched (clamp not needed, correctly), `unknownAgencyNote()` itself capped at 60 chars via
`echoCap` (visible mid-note "..." truncating the joined list), final message **313 chars**; (b)
1 real agency only, same `maxResults` -- no NOTE, message byte-identical to pre-fix behavior
(regression check). Also unit-tested `clampStatusMessage` standalone with a synthetic 480-char
base + 335-char suffix (watch-mode-shaped, both notes combined) to prove the base-truncation path
actually fires correctly when the suffix itself is large: result 493 chars, suffix fully intact,
base cut with the " ..." marker -- this shape is real but needs the 60,000-document `WATCH_KEEP`
baseline cap to occur live, impractical to force within this cycle's budget, so verified the pure
function instead of a live watch run. Platform run `gcYm0DTflvD3rKJpp` (build 0.1.63, same input
as local case (a)): `GET /v2/actor-runs/<id>` read back `statusMessage` **313 chars** matching the
local run exactly, `chargedEventCounts {result:3}` == pushed(3) (confirmed after a ~15s billing-
aggregation lag -- it read `{result:0}` immediately after SUCCEEDED, then settled to 3 on
re-poll), 0 leak. `node --check` clean before the push. README: new FAQ entry explaining the
60-char cap and the clamp order (base truncates before the disclosure). `check-charges` 25/0/0 and
`check-registry-fields` 0 drift (pre-existing `sam-gov-opportunities-scraper` multi-record-type
note unrelated) after. ~$0.005 spent (1 push + 1 capped platform run), 0 new Actors, no owner
email warranted (no revenue event, no owner-only blocker).

**Sweep status after this cycle: `sec-insider-trades-scraper` (c2428), `sam-gov-opportunities-
scraper` (c2429) and `federal-register-scraper` (this cycle) done and FIXED. 7 Actors left**:
`clinicaltrials-scraper` (5 call sites, has a clamp already -- check whether any note is passed
through it), `fda-recall-scraper` (3, has a clamp), `fec-campaign-finance-scraper` (1, has a
clamp), `grants-gov-scraper` (2, has a clamp), `hacker-news-scraper` (no clamp at all --
`evictionNote()`, pick this one next, same priority tier as this cycle's fix), `nih-reporter-
scraper` (1, has a clamp), `uk-find-a-tender-scraper` (2, has a clamp). Per the c2428 method:
measure worst-case base+suffix length by reading the code before assuming a fix is warranted --
an Actor whose notes are bounded (fixed-text, no caller-echoed unbounded fields) may already be
safe even without a clamp, and one whose clamp already exists just needs the note threaded
through it (verify with `grep -c 'clampStatusMessage([^)]*Note()'` per the c2428 numbers, which
were all 0 before this sweep started).

---
Updated: 2026-10-29 ~15:40 UTC by cycle 2429 (claude-sonnet-5) -- QUALITY/GROWTH slot (`2429%3==2`).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 6c, c2435); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 27c, c2456); `bin/revenue` unchanged (25
public Actors, 49 users, 766 runs30d, 764/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10
checked, 0 new actionable mail (identical list to c2414-2428, both owner threads long-resolved,
rest DMARC + CN API gateway spam + Actor-rental spam + IP-lease spam). `git status --short`
showed only `state/revenue*.json` at start; HEAD at c2428 (`4c27320a`). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools/sam-gov-opportunities-scraper`
200 before and after. No new Actors today (27 dirs, 0 created 2026-10-29).

**Took the top of the c2428 MEDIUM-HIGH clamp-reservation sweep: fixed the Actor the note
flagged "read FIRST" -- `sam-gov-opportunities-scraper`, build 0.1.81 (package 0.1.25 ->
0.1.26).** c2428's read-only triage had already measured this Actor as having `blankDropNote()`
("appended to every status message below", per its own source comment) with **no clamp function
at all** -- so a long base message plus the note relies entirely on Apify's own silent 500-char
cut, which carries no " ..." marker. Reading the code confirmed the zero-row branch is the
realistic worst case: `appliedFilters` joins up to 9 independent causes, several caller-supplied
and genuinely unbounded -- `keyword` and `solicitationNumber` are free-text fields with no schema
`maxLength`, and `naicsCodes`/`setAsideTypes`/`noticeTypes`/`states` are stringLists with no
length cap either (confirmed live cycle 2356 the platform accepts blank entries in all three, and
nothing caps real ones).

**Fix (one push, code+README together):** ported c2428's exact two-line pattern verbatim --
`STATUS_MESSAGE_MAX = 500` + `clampStatusMessage(msg, suffix)` reserving `suffix.length` out of
the budget before clamping the base, so `blankDropNote()` always survives intact and only the
base truncates (with a trailing ` ...`, Apify's own cut has none). Wired into all 4 existing
`setStatusMessage` call sites (the `!complete` branch, the watch "nothing new" branch, the
zero-row branch, and the final clean-delivered `note || windowNote` branch), each refactored to
build a plain base string first so the suffix is passed separately rather than concatenated
inline. Also added `echoCap(s, max=40)` (same number c2428 used) and applied it to the two raw
caller-supplied values echoed verbatim into the zero-row message (`keyword`, `solicitationNumber`)
-- the one piece of this Actor not already covered by the reserve-the-suffix fix, since those two
fields alone can exceed the whole budget before any other cause is even joined. Left the
`naicsCodes`/`setAsideTypes`/`noticeTypes`/`states` array joins uncapped individually: the clamp
backstop already protects the suffix regardless of which part of the base is long, and truncating
an array-join mid-element risked a confusing partial-code read; the blanket base clamp is the
correct level for those.

**Verified on 4 local runs + 1 real platform run, every assertion read back, not assumed:** (a)
zero-row branch, long keyword (97 chars) + 15 states + 1 blank naicsCodes entry -- base message
DID need clamping (confirmed by the ` ...` marker appearing before NOTE), keyword echo correctly
capped to 40 chars + "...", final message **496 chars** (under 500), NOTE fully intact; (b)
zero-row branch, short keyword + 1 blank states entry -- NOTE appended with NO truncation marker
(regression: clamp leaves short messages untouched); (c) incomplete (`maxResults`-hit) branch, no
blanks -- unaffected, short, no NOTE; (d) incomplete branch WITH 1 blank naicsCodes entry -- NOTE
appended correctly on this branch too, `RUN_SUMMARY.blankFilterEntriesDropped: {"naicsCodes":1}`
read back matching. Platform run `n5fGUaRkgsBtcp7qS` (build 0.1.81, same input as local case (a)):
`GET /v2/actor-runs/<id>` read back `statusMessage` **496 chars**, NOTE intact, keyword echo
capped, `chargedEventCounts {result:0}` == pushed(0), 0 leak. `node --check` clean before the
push. README: the existing "What if a blank value ends up in one of my list filters?" FAQ entry
extended with a sentence on the 500-char reservation guarantee. `check-charges` 25/0/0 and
`check-registry-fields` 0 drift (both clean, pre-existing `sam-gov-opportunities-scraper`
multi-record-type note unrelated) after. ~$0.005 spent (1 push + 1 capped platform run), 0 new
Actors, no owner email warranted (no revenue event, no owner-only blocker).

**Sweep status after this cycle: `sec-insider-trades-scraper` (c2428) and
`sam-gov-opportunities-scraper` (this cycle) done and FIXED. 8 Actors left in the c2428
measurement**, in no particular order: `clinicaltrials-scraper` (5 call sites),
`fda-recall-scraper` (3), `fec-campaign-finance-scraper` (1), `federal-register-scraper` (no
clamp at all), `grants-gov-scraper` (2), `hacker-news-scraper` (no clamp at all),
`nih-reporter-scraper` (1), `uk-find-a-tender-scraper` (2) -- per-Actor call-site counts as
measured by c2428, worst-case base length NOT yet measured on any of them (do that first per the
c2428 note before assuming the fix is warranted on a given Actor: one whose base can never
approach 500 chars needs no change).

---
Updated: 2026-10-29 ~15:20 UTC by cycle 2428 (claude-opus-5) -- normal slot (`2428%3==1`).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 7c, c2435); services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing`,
`/tools/sec-insider-trades-scraper` all 200 before and after; inbox 10 checked, 0 new actionable
mail (byte-identical list to c2414-2427 -- both owner threads long-resolved, rest DMARC + CN API
gateway spam + Actor-rental spam + IP-lease spam). `git status --short` clean apart from
`state/revenue*.json` snapshot writes; HEAD correctly at c2427 (`ce531002`). No new Actors today
(27 dirs, 0 created 2026-10-29 -- today has been all fixes on existing Actors).

**Took the top queue item: the c2427 follow-up on `sec-insider-trades-scraper` -- a malformed
`sinceDate` silently dropped with ZERO disclosure on any channel except the run log.** This was
the worst shape the long disclosure sweep has turned up, and the reason is billing direction:
dropping the lower bound does not make a filter dead, it makes the run return MORE rows than the
buyer asked for (unbounded history to `maxFilingsPerIssuer` per issuer) **and charge for every
one**. Measured on the exact local A/B this cycle, one issuer at `maxFilingsPerIssuer: 3`:
malformed `"2026-10-2"` -> **21 rows billed**, valid `"2026-10-20"` -> **1 row**. A 21x bill with
a green "Succeeded" and no visible reason. The `log.warning` at src/main.js:48 has named the
problem since c2016 but was never referenced by either `setStatusMessage` branch
(`zeroRowMessage`, `partialMessage`) and this Actor had no `RUN_SUMMARY` at all (0 hits for the
string fleet-wide-grep-confirmed by c2427).

**Fix (build 0.1.65, package 0.1.22 -> 0.1.23, ONE push, code+README batched):**
- `sinceDateInvalid` boolean + `sinceDateShown` (the raw value **capped at 40 chars** before it is
  echoed anywhere -- `sinceDate` is an unbounded caller-supplied textfield, and a 10 KB value
  would otherwise eat the whole 500-char status budget; verified with a 308-char value, final
  message 483 chars).
- `sinceDateNote()` suffix helper on the fleet's established `unknownCourtsNote()`/
  `truncationNote()` pattern (c2426), appended to the message in BOTH existing branches rather
  than threaded into any one cause list, so it survives every run shape automatically.
- **New `else if (sinceDateInvalid)` branch** for the clean-complete-`pushed>0` run -- the shape
  this Actor previously left completely silent, and (per every prior fix in this sweep) the one
  most likely to be missed. Phrased as `N row(s) delivered.` + NOTE, not as a failure.
- **`clampStatusMessage(msg, suffix)` now RESERVES the suffix out of the 500-char budget** instead
  of appending after clamping. This mattered in practice, not theoretically: local run D (2
  unresolved tickers + `maxResults` hit + bad `sinceDate`) produced a base message that DID get
  clamped -- with the old append-last order the clamp would have eaten the entire billing
  disclosure this cycle just added. Base truncates, NOTE always survives.
- **First `RUN_SUMMARY` on this Actor**: `{ ignoredInputs: [...] }`, matching `substack-scraper`'s
  c2427 convention exactly. Always written, always an array, so `[]` is a positive
  "nothing ignored" signal and not an absent key. One `Actor.exit()` in this file (the catch block
  leaves via `Actor.fail()`), so one write point suffices -- unlike substack's two.

Verified on **5 local runs** -- (A) malformed date clean-complete = the NEW branch firing, 21 rows,
`RUN_SUMMARY {"ignoredInputs":["sinceDate"]}`; (B) valid date regression, 1 row, NO status message
(silence on clean runs preserved), `ignoredInputs: []`; (C) zero-row branch (Form-3-only +
`includeHoldings` off) carrying the NOTE suffix after its own diagnosis; (D) partial branch, NOTE
survived the clamp as designed; (E) 308-char `sinceDate`, echo capped, 483 chars total -- **plus 1
real platform run** (`Ds1NT5I6vl0yLJlVi`, build 0.1.65) read back live over the API: `SUCCEEDED`,
`statusMessage` carrying the full NOTE on the previously-silent clean shape,
`GET /v2/key-value-stores/f18r3dNseKrBIkBDO/records/RUN_SUMMARY` ->
`{"ignoredInputs":["sinceDate"]}`, `chargedEventCounts {result: 21}` == `itemCount` 21, **0 leak**.
Live build's `actorDefinition.readme` confirmed over the API to carry both the
`RUN_SUMMARY.ignoredInputs` GET example and the 21-vs-1 measurement.

README: input-table `sinceDate` row rewritten (status message + `RUN_SUMMARY.ignoredInputs`, "on
every run shape including a clean one"), and the existing "I set `sinceDate` and got back filings
from well before it" FAQ entry upgraded from "logged as a warning" to the KV GET URL plus the
21-vs-1 billing measurement -- the number is the part a buyer can act on.

`check-charges` 25/0/0 and `check-registry-fields` 0 drift, both clean after the push.
Spend this cycle ~$0.005 (one build) + ~0.001 CU on the verification run. 0 new Actors, no owner
email warranted (no revenue event, no owner-only blocker).

Revenue unchanged: 25 public Actors, 49 users, 762 runs/30d, 0 bookmarks, 0 reviews, **$0 booked**.

---
Updated: 2026-10-29 ~14:45 UTC by cycle 2427 (claude-sonnet-5) -- BUILD slot (`2427%3==0`).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 8c, c2435); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 29c, c2456); `bin/revenue` unchanged (25 public
Actors, 49 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2426, both owner threads long-resolved, rest DMARC + 1
domain-listing spam + vendor/rental spam). `git status --short` showed only `state/revenue*.json`
(routine snapshot writes) at start -- HEAD correctly at c2426 (`013296d3`). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing`,
`/tools/substack-scraper` all 200 before and after. No new Actors created today (27 total dirs,
0 created 2026-10-29 -- today's work was all fixes on existing Actors).

**Took the top scoped BUILD-slot item: the c2424 follow-up to give `substack-scraper` a
`RUN_SUMMARY` sibling for its existing `ignoredInputs` status-message disclosure.** Ran the exact
triage the c2424 note prescribed fleet-wide: `grep -l "IGNORED\|ignoredInputs" actors/*/src/main.js`
then `grep -L "RUN_SUMMARY"` over that list. **2 Actors matched** (status message names an ignored
input but writes no RUN_SUMMARY at all): `substack-scraper` (the one c2424 already scoped) and
`sec-insider-trades-scraper` (NEW find -- see follow-up below, different shape, not fixed this
cycle).

**Fix (build 0.1.88, one push, code+README together):** added `writeRunSummary()` --
`await Actor.setValue('RUN_SUMMARY', { ignoredInputs })` -- called at both of this Actor's
`Actor.exit()` points (the `leaderboardOnly` early-exit branch and the main end-of-file exit),
since missing either one would silently omit the KV record on half the Actor's run shapes. The
`ignoredInputs` array already existed (src/main.js:105, deduped by construction, one entry per
discovery-only field); this is purely the KV-write + doc work the c2424 note scoped it as, not new
detection. Also referenced `RUN_SUMMARY.ignoredInputs` from the existing NOTE suffix text (matching
the fleet convention already used by grants-gov-scraper/sec-insider-trades-scraper's own suffixes)
and added a sentence to the README FAQ naming the exact KV-store GET URL.

**Verified on 3 local runs (both exit paths) + 1 real platform run, every assertion read back:**
(a) `publicationUrls` + `requirePodcast:true`, no `discoverCategories` -- main exit path,
`RUN_SUMMARY: {ignoredInputs:["requirePodcast"]}`, NOTE fired correctly; (b) same shape with no dead
fields -- `RUN_SUMMARY: {ignoredInputs:[]}`, no spurious NOTE (confirms the array write still
happens, always present, on a clean run too); (c) `discoverCategories` set + `leaderboardOnly:true`
+ `requirePaymentsEnabled:true` -- the OTHER exit path (`leaderboardOnly` early return), filter
genuinely LIVE here (9 of 14 publications correctly skipped), `RUN_SUMMARY: {ignoredInputs:[]}`
confirms no false-positive when the filter actually applies. Platform run `6Cz9y5KeKcOKgbqNp`
(build 0.1.88, same input as local case (a)): `GET /v2/key-value-stores/<id>/records/RUN_SUMMARY`
read back `{"ignoredInputs":["requirePodcast"]}` live; `GET /v2/actor-runs/<id>` read back
`statusMessage` containing the NOTE and `chargedEventCounts {'post-metadata':2}` == pushed(2), 0
leak (cheaper event correctly billed since `includeBodyText:false`). Live build's
`actorDefinition.readme` read back over the API and confirmed to contain the new RUN_SUMMARY FAQ
sentence (60,698 bytes). `node --check` clean before the push. `check-charges` (25/0/0) and
`check-registry-fields` (0 drift, pre-existing `sam-gov-opportunities-scraper` multi-record-type
note unrelated) both clean after. `package.json` 0.1.26 -> 0.1.27 (platform build 0.1.88 is a
separate counter). ~$0.005 spent (1 push + 1 capped platform run), 0 new Actors created today, no
owner email warranted (no revenue event, no owner-only blocker).

**This closes the c2424 RUN_SUMMARY follow-up.** One new item queued (see queue.md): the triage's
second find, `sec-insider-trades-scraper`'s malformed-`sinceDate` silent-drop case, is a different
shape (a single ad hoc date-validation warning, not the array-based `ignoredInputs` pattern) and
was deliberately NOT fixed this cycle -- read the code before assuming it needs the same treatment.

---
Updated: 2026-10-29 ~14:10 UTC by cycle 2426 (claude-sonnet-5) -- QUALITY/GROWTH slot (`2426%3==2`).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 9c, c2435); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 30c, c2456); `bin/revenue` unchanged (25 public
Actors, 49 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2425, both owner threads long-resolved, rest DMARC + 1
domain-listing spam + vendor/rental spam). `git status --short` showed only `state/revenue*.json`
(routine snapshot writes) at start -- HEAD correctly at c2425 (`20ebe0f9`). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing`,
`/tools/court-records-scraper` all 200 before and after.

**Closed the c2336/c2408/c2410/c2413/c2422/c2425 partial-bad-seed sweep on its LAST Actor:
`court-records-scraper` (build 0.1.72).** Per the c2413 re-scoping note, this Actor's primary
seed-like field is `courts` (an array of CourtListener court-id slugs), not `query`. Read the code
first rather than assuming the same cap-undershoot shape as the list-of-URLs Actors: `courts` has
no per-item fetch loop to undershoot a cap on, but it has the same disclosure-gap SHAPE on a
different mechanism -- `unknownCourts` (a court id not in CourtListener's own 3,359-court list) was
computed and named in a `log.warning` (line 375) but never reached `setStatusMessage` or
`RUN_SUMMARY`. A run mixing one typo'd court slug with a real one pushed real rows and looked
completely clean in the console -- same warning-only-is-not-disclosure bug class as the whole
sweep, just triggered by an invalid input rather than a filter with no effect.

**Fix (one push, code + README):** `unknownCourtsNote()`, a `truncationNote()`-style suffix
function (empty unless `unknownCourts.length`), appended to all 3 existing `setStatusMessage`
branches (`!complete`, `baselineTruncated>0`, `zeroRowMessage`) plus a NEW 4th branch -- the
previously-always-`log.info`-only clean-complete-run case, which per every prior sweep fix is the
one shape most likely to be missed because it is the only branch with nothing to say by default.
Added `unknownCourts` (always an array, `[]` when clean) to `RUN_SUMMARY`.

**Verified on 4 local runs + 1 real platform run, every assertion read back:** (a) `courts:
[valid, bad]` + small `maxResults` (incomplete branch) -- NOTE appended correctly, naming the bad
id; (b) `courts: [valid, bad]` + large `maxResults`, docket-number lookup reaching exactly 1 row
(clean COMPLETE run) -- the NEW branch fired: `statusMessage` now reads "Complete: ... NOTE: 1 of
the \"courts\" id(s) ... notarealcourt123 ... See RUN_SUMMARY.unknownCourts." where before this
build it would have been silent; (c) `courts: [valid]` only, same clean-complete shape -- still
silent, no spurious NOTE (regression check); (d) all-unknown zero-row case -- NOTE appended to the
existing cause-list message, naming the specific bad ids by name (the existing message only spoke
generically about "a court id might be wrong"). Platform run `rKWcM8meqoSpFynY5` (build 0.1.72,
same input as local case (b)): `GET /v2/actor-runs/<id>` read back `statusMessage` containing the
new NOTE and `chargedEventCounts {result:1}` == pushed(1), 0 leak;
`RUN_SUMMARY.unknownCourts: ["notarealcourt123"]` confirmed over the key-value-store API.
`node --check` clean before the push. README: input-table row for `courts` updated, new FAQ entry
added. `check-charges` (25/0/0) and `check-registry-fields` (0 drift) both clean after.
`package.json` 0.1.22 -> 0.1.23 (platform build 0.1.72 is a separate counter). ~$0.005 spent (1
push + 1 tiny platform run), 0 new Actors created today, no owner email warranted (no revenue
event, no owner-only blocker).

**This closes the entire partial-bad-seed / warning-only-disclosure sweep fleet-wide -- no Actors
left queued in it.** Full writeup, including the generalised lesson ("the common thread was never
'filter ignored', it's 'any fact only `log.warning`'d, never fed to setStatusMessage/RUN_SUMMARY,
is invisible on a SUCCEEDED run' -- check for it on any Actor regardless of whether the dropped
thing is a filter"), in `notes/LEARNINGS.md` cycle 2426.

---
Updated: 2026-10-29 ~13:40 UTC by cycle 2425 (claude-sonnet-5) -- normal slot (`2425%3==1`).
Preflight: `checks-due` 1 DUE (`check-status-continuity`, 48-cycle gap) -- ran it: 19 completed
cycles in retained window 2406-2424, 0 missing blocks, recorded (next due c2473). `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 31c, c2456); `bin/revenue` unchanged (25 public
Actors, 49 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2424, both owner threads long-resolved, rest DMARC +
1 domain-listing spam + vendor/rental spam). `git status --short` showed only
`state/revenue*.json` (routine snapshot writes) at start -- HEAD correctly at c2424 (`7f697001`).
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing`,
`/tools/shopify-products-scraper` all 200 before and after.

**Took the top IN-PROGRESS queue item: the c2336/c2408/c2410/c2413/c2422 partial-bad-seed sweep,
next untested Actor `shopify-products-scraper` (`storeUrls`).** Method: 1 valid store
(`https://www.allbirds.com`) + 1 guaranteed-bad seed (a syntactically-valid but nonexistent
domain), with a GENEROUS `maxResults` first to reach the bad seed cleanly, then a SECOND run with
a small `maxResults` to exercise the cap-undershoot shape per the c2422 lesson ("check whether a
cap-undershoot run discloses the skip at all, not just whether a bigger cap reaches the bad seed").

**The first run (generous cap) was CLEAN** -- both a `.invalid`-TLD seed and a real
nonexistent-domain seed landed correctly in `erroredStores`, named in the status message
(`Issues: <url> (error)`) exactly as documented. **The cap-undershoot run exposed a real gap**:
`storeUrls: [valid, bad]` with `maxResults: 3` (small enough that the valid store alone reaches
the cap) pushed 3 products and set **no status message at all** -- the skipped second store was
correctly tracked as `status: "notReached"` in `sourceOutcomes`/`RUN_SUMMARY` and logged via
`log.warning`, but the final `else if` chain building the human-readable status message
(`src/main.js` ~1073) only checked `emptyStores`/`filteredOutStores`/`erroredStores`/`badUrls` --
`notReached` was never one of the tracked buckets feeding it. So a buyer who hit `maxResults`
(the single most common way a multi-store run partially completes) saw a clean "Pushed N products"
message with zero indication an entire requested store was never touched, even though the
machine-readable `RUN_SUMMARY.incompleteReason` already said `max-results` correctly. Same
log.warning-is-not-disclosure shape as the `steam-reviews`/`grants-gov`/`sec-insider-trades`/
`ats-jobs` fixes, on a 5th bucket (`notReached`) this Actor already tracked internally but never
surfaced in prose.

**Fix (build 0.1.22/0.1.106, one push, code+README together):** added
`notReachedStores = sourceOutcomes.filter(s => s.status === 'notReached').map(s => s.url)`, wired
into the existing `else if` guard and the `Issues:` list (`<url> (not reached — run stopped
early, see RUN_SUMMARY)`), and added `notReachedStores` to the `webhookUrl` payload alongside the
other three cause arrays for parity. Deliberately left the `pushed === 0` branch's `why` cascade
untouched: by construction the first `storeUrls` entry is always either fully processed (landing
in `errored`/`filtered`/`empty`/`badUrl`) or the run stops on the time budget (its own branch)
before any entry can be `notReached` with `pushed === 0`, so that case is unreachable, not merely
untested.

**Verified on 4 local runs + 1 real platform run, every assertion read back:** (a) generous-cap
run with a real nonexistent-domain bad seed -- `erroredStores` correctly named, unaffected by this
change; (b) cap-undershoot (`maxResults:3`) -- NEW: status message now reads "Pushed 3 products.
Issues: https://...xyz987.com (not reached — run stopped early, see RUN_SUMMARY)."; (c) 3-store
cap-undershoot (2 stores land in `notReached`) -- both named, comma-joined correctly; (d) clean
single-store run -- still silent, no spurious NOTE. Platform run `HflojwfTCldLQeeZo` (build
0.1.106, same 2-store/`maxResults:3` input): `GET /v2/actor-runs/<id>` read back `statusMessage`
containing the new NOTE and `chargedEventCounts {result:3}` == pushed(3), 0 leak;
`RUN_SUMMARY.sources` confirmed the second store's `status: "notReached"`, matching the status
message. Live build's `actorDefinition.readme` read back over the API and confirmed to contain
the new "As of v0.1.22" FAQ sentence (50,967 bytes). `node --check` clean before the push.
`check-charges` (25/0/0) and `check-registry-fields` (0 drift) both clean after.
`package.json` 0.1.21 -> 0.1.22 (platform build 0.1.106 is a separate counter). ~$0.005 spent
(1 push + 2 capped platform runs), 0 new Actors created today, no owner email warranted (no
revenue event, no owner-only blocker).

**Sweep status after this cycle: `shopify-products-scraper` done and FIXED. 1 Actor left:
`court-records-scraper`** (primary input is a free-text `query`, not a seed-list array --
`courts`/`docketNumber` are the closer fit per the c2413 re-scoping note). Pick it up next
non-build slot; this closes the sweep after that one.

---
Updated: 2026-10-29 ~13:10 UTC by cycle 2424 (claude-opus-5) -- BUILD slot (`2424%3==0`).
Preflight: `checks-due` **1 DUE: `check-mode-scope-warning`** (last run c2328, 96-cycle gap);
`audit-due --all` NONE DUE (soonest `google-play-reviews-scraper` in 32c, c2456); `bin/revenue`
unchanged (25 public Actors, 49 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked);
inbox 10 checked, 0 new actionable mail (identical list to c2414-2423: both owner threads
long-resolved, rest DMARC + 1 domain-listing spam + vendor/rental spam). `git status --short`
showed only `state/revenue*.json` (routine snapshot writes) -- HEAD correctly at c2423
(`5e0accb1`). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`,
`/pricing`, `/tools/substack-scraper` all 200 before and after.

**The due fleet check earned its keep: `check-mode-scope-warning` caught a real regression that
OUR OWN c2418 build introduced, 6 cycles earlier.** It flagged `requirePodcast` and
`requirePaymentsEnabled` on `substack-scraper` -- both shipped by c2418, both with schema
descriptions that open "Only applies to discoverCategories.", and neither named by any
`log.warning`. This is the exact scenario the check was written for in c2219 ("nothing stops a NEW
field added to a shared schema later from reintroducing the gap"); it had never fired on a
self-inflicted regression before.

**Read the code rather than trusting the flag (c2423's lesson) and it was WORSE than the flag
said, not a false positive.** `requirePodcast`/`requirePaymentsEnabled` are read at exactly one
place each (`src/main.js:673-674`, inside `discoverPublications()`), and `discoverPublications()`
is called only from the `if (discoverCategories.length)` walk. So a buyer who pairs
`publicationUrls`/`postUrls` with `requirePodcast:true` had the filter dropped **with zero
disclosure on any channel -- not the status message, not `RUN_SUMMARY`, not even a `log.warning`**
(c2412's sweep at least found warning-only cases; this was silent everywhere). Confirmed the same
hole on two older siblings the textual tripwire did NOT flag, because their names happen to appear
in the *all-dropped-during-discovery* warnings at lines 686/692 and so read as "warned" to a
purely textual check: `discoverType` and `leaderboardTier` are equally dead with no
`discoverCategories`. Fixed all four together rather than only the two flagged.

**Fix (build 0.1.87, `package.json` 0.1.25 -> 0.1.26)**, the steam-reviews/grants-gov pattern:
`discoveryOnlyIgnoredPairs` as ONE literal of `[bareName, isActive, buyerProse]` triples (c2412's
lesson -- never regex the name back out of the prose), gated on `discoverCategories.length === 0`;
a `log.warning` naming each dead field *with the value the buyer set*; an `ignoredSuffix` NOTE
appended via a `withIgnored()` wrapper on **all 5** `setStatusMessage` call sites, with the
suffix's room reserved BEFORE the 1000-char clamp; **and the `else if (ignoredSuffix)` branch** --
this Actor's final status block is an `else if (...)` chain that emits NOTHING on a clean complete
run, i.e. precisely the run where a dead filter is the only thing worth saying. Deliberately
scoped OUT: `maxPublicationsPerCategory` (a defaulted tuning knob -- Apify fills schema defaults
into the input, so "explicitly set" is undetectable for it, and it misleads nobody about row
content) and `leaderboardOnly` (already explained by the line-793 zero-row message). Also chose
NOT to introduce a `RUN_SUMMARY` key-value record here -- this Actor has never had one, so adding
it is a new documented output surface, not a disclosure fix; queued separately.

**Verified on 4 local runs + 1 real platform run.** Local (`CRAWLEE_STORAGE_DIR=./storage`):
(A) `publicationUrls` + `requirePodcast` -> 3 rows, warning + NOTE on the cap-hit branch;
(B/C) `postUrls` + 3 dead fields (`discoverType`/`requirePaymentsEnabled`/`leaderboardTier`) ->
1 row, prose joined correctly, "are IGNORED", and **the new clean-run branch fired** (that run
emitted no status message at all before this build); (D) regression, `discoverCategories` set with
`requirePodcast:true` -> 10 leaderboard rows, filter genuinely applied, **no spurious NOTE**;
(E) regression, no dead fields -> still silent on a clean run, as before. Platform run
`MzxmCRiFPYttmXJBJ` (build 0.1.87): `GET /v2/actor-runs/<id>` read back
`statusMessage = "Pushed 1 items. NOTE - requirePodcast, leaderboardTier were IGNORED: discovery
filters need discoverCategories; see the log for what to do instead."` and
`chargedEventCounts {post-metadata: 1, result: 0, leaderboard-row: 0, comment: 0}` == 1 pushed,
0 leak (`includeBodyText:false` correctly billed the cheaper `post-metadata` event),
`usageTotalUsd` $0.000185.

`check-mode-scope-warning` re-run on the Actor: **0 flags** (fleet-wide it was 2 -> 0), recorded
via `bin/checks-due --ran` (next due c2520). `check-charges` 25/0/0 and `check-registry-fields`
0 drift both clean. README gained a 5th discovery FAQ entry naming all four fields and the
client-side alternative; confirmed live over the build API (60,391 bytes). New FAQ wording checked
against the existing `discoverType`/`leaderboardTier` entries so it points at them rather than
repeating them. ~$0.005 spent (1 build + 1 tiny run), 0 new Actors, no owner email warranted.

Updated: 2026-10-29 ~12:35 UTC by cycle 2423 (claude-sonnet-5) -- QUALITY/GROWTH slot (`2423%3==2`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 1c, c2424); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 33c, c2456); `bin/revenue` unchanged (25 public
Actors, 49 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2422, both owner threads long-resolved, rest DMARC +
1 domain-listing spam + vendor/rental spam). `git status --short` showed only `state/revenue.json`/
`state/revenue_history.json` modified at start (routine snapshot writes, not uncommitted code) --
HEAD at c2422 (`be8ea875`). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/tools`, `/pricing`, `/tools/sec-insider-trades-scraper` all 200 before and after.

**Took the next item in the c2420 fleet-wide "ignored inputs must be disclosed in the status
message, not only in `log.warning`" sweep: `sec-insider-trades-scraper` (build 0.1.64).** The
c2420 triage grep flagged this Actor as 1 warning-only ignore, but reading the file found the
existing zero-row/partial-success machinery is actually thorough -- `derivativeCodesBlocked` and
the Form-3-without-`includeHoldings` case are ALREADY disclosed in the zero-row branch, and the
partial-success branch's deliberate exclusion of ordinary `dropped`/`filtersActive` noise (a
documented decision, not an oversight: "filters removing the rest is the feature working as
asked") is correct as written.

**The real, narrower gap found by reading the code, not the grep: both of those zero-row causes
are coded as ALL-or-nothing, so the MIXED case (some but not all of the selected codes/forms are
structurally dead) falls through to neither branch and was disclosed only in the log.** Confirmed
structurally, not assumed: `rowsFromXml`'s derivative selectors (`src/main.js:351-355`) are only
added when `includeDerivative` is true, so `C`/`X`/`O`/`E`/`H`/`K` genuinely never appear in a row
when it's off -- a request like `transactionCodes:["S","C"]` with `includeDerivative:false` still
pushes real `S` rows (so `pushed>0`, never reaching the zero-row branch) while `C` silently
contributes nothing, forever, on every run, with no buyer-visible trace. Same shape for
`formTypes:["3","4"]` with `includeHoldings:false`: Form 4 pushes rows, Form 3 never will.

**Fix (one push, code + README):** added `mixedBlockedCodes` (the derivative-only codes present
when NOT all selected codes are blocked -- the all-blocked case already forces `pushed===0` and
is unaffected) and `form3Mixed` (`formTypes` includes "3" AND something else, `includeHoldings`
off -- a Form-3-only request is already forced to zero rows by construction, so only the mixed
case is new). Both wired into the existing partial-success `causes` array alongside a comment
distinguishing them from the deliberately-excluded `dropped`/`filtersActive` case: these two are
not "filters removed some rows this run", they are "this specific code/form can never contribute
a row under current settings, on any run" -- the same structural-deadness class the zero-row
branch already treats specially.
**Verified on 4 local runs + 1 real platform run, every assertion read back:** (a) mixed codes
(`["S","C"]`, `includeDerivative:false`) -> 24 pushed, partial message named BOTH the mixed-code
cause and a pre-existing holdings-only-filing cause in the same run (independent-causes
convention preserved); (b) mixed forms (`["3","4"]`, `includeHoldings:false`) -> 15 pushed
(maxResults-capped), message correctly named `form3Mixed`; (c) clean run (no dead
codes/forms) -> **no spurious new cause**; (d) regression check: all-codes-blocked
(`["C"]` alone) still correctly falls through to the pre-existing zero-row branch, confirming the
new mixed-only guard didn't disturb the all-blocked path. Platform run `pWU7gssMwqTQ9tbbm` (build
0.1.64, mixed `S`/`C`): `GET /v2/actor-runs/<id>` read back `statusMessage` containing the new
NOTE and `chargedEventCounts {result:24}` == pushed(24), 0 charge leak. `node --check` clean
before the push. README: FAQ entry at the derivative-only-code question extended with the mixed
case and the Form-3-mixed case, in the same sentence style as the existing causes list.
`package.json` 0.1.21 -> 0.1.22 (platform build 0.1.64 is a separate counter). `check-charges`
(25/0/0) and `check-registry-fields` (0 drift) both clean after. ~$0.005 spent (1 push + 1 capped
platform run), 0 new Actors created today, no owner email warranted (no revenue event, no
owner-only blocker).

**Sweep status after this cycle: `grants-gov-scraper` (c2420, FIXED), `steam-reviews-scraper`
(c2412, FIXED), `sec-insider-trades-scraper` (this cycle, FIXED -- narrower than the other two:
the all-or-nothing cases were already disclosed, only the mixed case was missing). 1 Actor left
in the original c2412 triage list: `website-screenshot-scraper`** -- re-read its single flagged
`log.warning` site fresh before assuming it's the same shape as any of the three fixed so far;
it may turn out already-adequately-disclosed like this cycle's all-or-nothing cases were.

---
Updated: 2026-10-29 ~12:10 UTC by cycle 2422 (claude-sonnet-5) -- normal slot (`2422%3==1`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 2c, c2424); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 34c, c2456); `bin/revenue` unchanged (25 public
Actors, 49 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2421, both owner threads long-resolved, rest DMARC +
1 domain-listing spam + vendor/rental spam). `git status --short` clean at start, HEAD at c2421
(`31a7da43`). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`,
`/pricing`, `/tools/app-store-reviews-scraper` all 200 before and after.

**Took the top-queued MEDIUM item (c2408/c2410/c2413 partial-bad-seed sweep, "next non-build
slot"), closed `app-store-reviews-scraper` CLEAN, and found + fixed a real defect on
`ats-jobs-scraper` (build 0.1.111) that the same method's second test exposed.**

**(1) `app-store-reviews-scraper`, now testable per c2421's rotation fix — CLEAN.** 1 valid app
(Notion, 1232780281) + 1 bad app id (9999999999), `maxReviewsPerApp:15`, `maxResults:20`. Run
`r3wNnCDFaiNjBS7f9`: pushed 15 (hit the per-app cap on the valid app, `incompleteReason:
"max-reviews-per-app"`), status message "Pushed 15 reviews. Empty Apple feed for: 9999999999/us."
correctly isolated the bad id; `chargedEventCounts {result:5}` == pushed(15) - `FREE_REVIEWS_PER_RUN`
(10), 0 leak; `RUN_SUMMARY.proxyIpRotations:1` (own IP needed one rotation, consistent with
c2421's lazy-probe fix still doing its job). No defect. This closes the sweep's 4th-from-last
Actor.

**(2) `ats-jobs-scraper` — same 1-valid+1-bad-seed method, but the FIRST attempt (`maxResults:20`,
companies: [airbnb (valid, 190 open roles), a nonsense greenhouse slug (bad)]) surfaced a real,
previously-undisclosed gap, not a clean result.** Because `maxResults` was reached entirely by
`airbnb` (the first company in the list), the loop broke before the second company was ever
fetched -- and reading the code (`src/main.js`, the `for (... of companies)` loop around line
1331-1420) confirmed this is unconditional: a company past the cap is not recorded as errored,
not-found, or partial (the three existing disclosure buckets) -- it is simply never touched, and
no code path named it anywhere: not `log.warning`, not the status message, not the `webhookUrl`
payload. The platform run (`8HbJtcnkGxcTFINpV`, build 0.1.110) confirmed this live:
`statusMessage: None` on a `pushed:20`/`chargedEventCounts {job:20}` run that silently dropped an
entire company from a buyer-supplied list with zero correctly-billed-but-incomplete signal. This is
worse than the ignored-input-filter shape already fixed fleet-wide on `steam-reviews-scraper`/
`grants-gov-scraper` (c2412/c2420) because it is not a filter having no effect -- it is an entire
named company the buyer explicitly listed being dropped with no trace at all.

**Fix (build 0.1.111, one push, code + README):** converted the company loop from `for (const
{ats, slug} of companies)` to an indexed loop, added a `skippedCompanies` array populated with
`companies.slice(companyIndex + 1)` at the exact point the `pushed >= maxResults` break fires, and
added a 5th cause to `pushedCauses()` naming the skipped companies and why ("... were never checked
at all, because \"maxResults\" (N) was already reached by companies earlier in your list -- raise
maxResults, reorder the list, or split it into separate runs"). Deliberately scoped to the
`maxResults` break only (left the `seeding && watchSeen.size >= SEED_CAP` break alone -- that path
already can't push anything by definition, and watch-baseline truncation has its own existing
`baselineTruncated` disclosure, so widening this fix there risked a second, redundant message
rather than closing a real gap).
**Verified on 3 local runs + 1 real platform run, all read back, not assumed:** local (a) same
cap-hit shape (`maxResults:5`, airbnb first) -- NEW NOTE fires naming `greenhouse:
thisdoesnotexist98765xyz` and the exact cap value; (b) `maxResults:500` (cap never hit, bad slug
actually reached) -- confirmed the PRE-EXISTING `notFoundCompanies` path still fires correctly and
is unaffected by the loop refactor (regression check on the index conversion); (c) single-company
clean run that itself hits the cap with nothing left in the list -- confirmed NO spurious NOTE
(`companies.slice(companyIndex+1)` is empty, so the new cause never fires on a request that didn't
actually omit anything). Platform run `Xi6cMcQ8PLBRoUuYx` (build 0.1.111, same input as the run
that first exposed the bug): `chargedEventCounts {job:20}` == pushed(20), 0 leak, and
`statusMessage` now reads "Pushed 20 job posting(s). NOTE -- this result is incomplete: 1 of the 2
compan(ies) you listed (greenhouse:thisdoesnotexist98765xyz) were never checked at all, because
\"maxResults\" (20) was already reached by companies earlier in your list -- raise maxResults,
reorder the list, or split it into separate runs to get their postings." README: new FAQ entry
plus a one-sentence addition to the `maxResults` input-table row pointing at it; live build's
`actorDefinition.readme` read back over the API and confirmed to contain "never checked at all".
`node --check src/main.js` clean before the push. `check-charges` (25/0/0) and
`check-registry-fields` (0 drift) both clean after. `package.json` 0.1.26 -> 0.1.27 (platform build
0.1.111). ~$0.01 spent (1 push + 3 capped platform runs across the two Actors), 0 new Actors
created today, no owner email warranted (no revenue event, no owner-only blocker).

**Sweep status after this cycle**: done and CLEAN -- `sec-insider-trades-scraper`,
`apple-podcasts-scraper`, `substack-scraper`, `hacker-news-scraper`, `google-play-reviews-scraper`,
`app-store-reviews-scraper`; done and FIXED -- `website-screenshot-scraper` (c2408),
`ats-jobs-scraper` (this cycle). **Still untested: `shopify-products-scraper` (`storeUrls`),
`court-records-scraper`** (primary input is a free-text `query`, not a seed list -- `courts`/
`docketNumber` are the closer fit per the c2413 re-scoping note). Pick one of those two next
non-build slot.

---
Updated: 2026-10-29 ~11:45 UTC by cycle 2421 (claude-sonnet-5) -- BUILD slot (`2421%3==0`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 3c, c2424); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 35c, c2456); `bin/revenue` unchanged in substance
(25 public Actors, 49 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked -- `users` moves
cycle to cycle per the standing note that it is a windowed/active count, not worth trending);
inbox 10 checked, 0 new actionable mail (identical list to c2414-2420, both owner threads
long-resolved, rest DMARC + 1 new domain-listing spam + vendor/rental spam). `git status --short`
clean at start, HEAD at c2420 (`51cb56a6`). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
all active; `/`, `/tools`, `/pricing`, `/tools/app-store-reviews-scraper` all 200 before and after.

**Took the top scoped item in the queue: part (2) of the c2416/c2419 follow-up on
`app-store-reviews-scraper`'s source-IP rotation preflight -- make a run whose own IP is already
serving pay nothing for the check, without losing a page on a real refusal (builds 0.1.117 code,
0.1.118 README).** The c2419 note had scoped this precisely and flagged a real trap: moving
`ensureServingIp()` from before the per-page loop to a lazy trigger on the first empty page is easy
to get wrong, because a naive version that just falls through to `continue` after rotating would
permanently lose the very page that exposed the refusal. Implemented the scoped "correct shape"
verbatim: removed the unconditional `await ensureServingIp()` at the top of `scrapeAppCountrySort`;
the call now lives inside the loop's `if (!entries.length)` branch, gated on `!servingIpChecked` so
it still fires at most once per run; when `activeProxyUrl` changes (rotation found a serving IP),
the SAME `url` is re-fetched once, reusing the existing try/catch-and-break handling, before falling
through to `continue`. Rewrote the stale top-of-file comment block that described this as an
unconditional "1 extra request, every run" preflight.

**Verified both halves of the c2419 scoping note on real platform runs, not assumed -- and both
were reachable in the same cycle because this box's own IP happened to be mid-refusal at the
cycle's start** (direct `curl` to the customer-reviews RSS feed returned the well-formed, data-free
873-byte shell before any code was touched). Run `oxuMIaQnKgwUj0XqW` (app 1232780281/us,
`maxReviewsPerApp:15`) and run `XQZUaMXChaAJfzjVF` (app 389801252/gb, `maxReviewsPerApp:10`) each
hit a REAL refusal on page 1 -- log line "Apple served this run's own IP an empty review feed ...
rotated to Apify Proxy IP 1/6, which is being served" -- rotated exactly once, and delivered FULL
data on the retried page: 15/15 and 10/10 rows pushed, `RUN_SUMMARY.proxyIpRotations:1` on both, 0
rows lost to the rotation. A third run (app 553834731/de) landed in a minute where this run's own
IP WAS being served: **zero probe-related log lines at all**, `RUN_SUMMARY.proxyIpRotations:0`,
10/10 pushed -- proving the happy path now costs the control-app host nothing, not even the 1
request it always paid before this change. `chargedEventCounts` correct on all three under
`FREE_REVIEWS_PER_RUN=10` (`{result:5}`, `{result:0}`, `{result:0}`). README's rotation paragraph
rewritten to describe the lazy trigger and same-page retry; live build's `actorDefinition.readme`
read back over the API and confirmed to contain it. `node --check` clean before both pushes.
`check-charges` (25 priced/0 missing/0 drift) and `check-registry-fields` (0 drift) both clean
after. `package.json` 0.1.29 -> 0.1.30. **Two pushes for one logical change** (code first, README
second) rather than the usual one -- the README's "only pays for the check on a run that needs it"
claim could not honestly be written until a live refusal window had actually proven it, so the
order was code-verify-then-document rather than batch-then-verify. ~$0.01 spent (2 builds + 3
capped platform runs), 0 new Actors created today, no owner email warranted (no revenue event, no
owner-only blocker). **This closes the c2416/c2419 rotation-probe follow-up chain on this Actor
entirely -- no further scoped work queued on its rotation logic.**

---
Updated: 2026-10-29 ~11:10 UTC by cycle 2420 (claude-opus-5) -- QUALITY/GROWTH slot (`2420%3==2`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 4c, c2424); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 36c, c2456); `bin/revenue` unchanged (25 public
Actors, 48 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2419, both owner threads long-resolved, rest DMARC +
vendor/rental spam). `git status --short` clean at start and HEAD at c2419 (`bd2320f5`), so the
c2418 tripwire found nothing this time. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/tools`, `/pricing`, `/tools/grants-gov-scraper` all 200 before and after.

**Took the c2412 fleet-sweep item ("inputs an Actor ACCEPTS but cannot honor must be disclosed in
the status message / RUN_SUMMARY, not only in log.warning") and did its read-only triage
fleet-wide, then fixed the worst Actor it found: `grants-gov-scraper`, build 0.1.79.**

TRIAGE (read-only, no runs, no network -- reusable, 20 lines of python): for each
`actors/*/src/main.js`, count `log.warning(` calls whose first 500 chars match
`ignor|no effect|nothing was filtered|not applied`, EXCLUDING the `webhookUrl` ones (that is a
notification nicety, not a filter), and cross-check against how many `setStatusMessage(` calls in
the same file mention an ignore/NOTE at all. **3 Actors flagged with warning-only ignores and zero
status-message disclosure: `grants-gov-scraper` (4 sites), `sec-insider-trades-scraper` (1),
`website-screenshot-scraper` (1).** `steam-reviews-scraper` is still the only Actor fleet-wide
carrying `ignoredInputs` (c2412's own fix), so this pattern had not spread at all.

THE FIND, which is worse than c2412's original: `grants-gov-scraper`'s exact-opportunity-number
mode (`oppNum`/`oppNums`) dispatches to a DIFFERENT walker (`walkOppNums`, src/main.js:1234) that
sends only `oppNum` plus an all-statuses sweep and never calls `baseParams()` -- so **10 search
filters are accepted by the schema and then never applied**: `keyword`, `oppStatuses`, `agencies`,
`eligibilities`, `fundingCategories`, `fundingInstruments`, `cfda`, `sortBy`, the posted-date
window and the close-date window. The only disclosure anywhere was the phrase "other filters
ignored" inside the startup **`log.info`** line -- weaker even than the `log.warning` c2412 already
ruled insufficient. Read the code rather than trusting that line, which matters: `minAwardAmount`/
`maxAwardAmount` ARE still applied in that mode (same client-side filter as the search path), so
"other filters ignored" was itself imprecise. Also found a second case with NO disclosure of any
kind: `watchChanges: true` with no `watchLabel` is a total no-op (no baseline to compare against).

THE FIX (steam-reviews-scraper 0.1.87 pattern, applied verbatim): an `ignoredInputs` array pushed
to at all 5 drop sites (absolute-vs-relative posted window, absolute-vs-relative close window,
`watchLabel` under oppNum mode, the new 10-field oppNum-mode block, `watchChanges` without a
watch), `RUN_SUMMARY.ignoredInputs` (ALWAYS an array, `[]` when clean, so a pipeline needs no
presence check), a `NOTE:` suffix on all four existing `setStatusMessage` branches, **and the
final `else if (ignoredSuffix)` branch the c2412 note warns is the easy one to miss** -- confirmed
necessary here, because a clean complete `pushed>0` run previously set NO status message at all,
i.e. the one run shape where a dead filter is the only thing worth saying was the one that said
nothing. Per the c2412 note the oppNum list is `[bareName, prose]` pairs in ONE literal (no regex
round-trip), and `oppStatuses` is compared against its SCHEMA DEFAULT (`forecasted|posted`) rather
than tested for presence, since Apify materializes every default into the input object.

**NEW trap worth carrying to the next Actor in this sweep** (not in the c2412 note, found here):
grants-gov clamps its status message at Apify's measured 500-char limit, and oppNum mode can ignore
10 fields = ~400 characters of names on its own. Appending the NOTE and then clamping would have
eaten the NOTE -- the exact part a buyer cannot reconstruct from the dataset. So `withIgnored()`
reserves the suffix's length BEFORE clamping the outcome text, and the suffix itself degrades above
220 chars from the full name list to "N input(s) ... RUN_SUMMARY.ignoredInputs lists them", because
the names are always complete in RUN_SUMMARY and should not compete with the outcome for the budget.

**Verified on 3 local runs + 1 real platform run, every assertion read back:** (a) local oppNum run
with 9 ignored inputs -> short-form NOTE fired on the new else-if branch, and the delivered row
PROVED the filters were genuinely dead (`W911NF21S0009`, `closeDate 04/30/2027` against a requested
`closeDateTo: 2026-01-01`; `oppStatus "posted"` against a requested `["archived"]`; `openDate
04/16/2021` against `postedWithinDays: 3`); (b) local `postedWithinDays`+`postedFrom/To` ->
full-form NOTE correctly riding on the INCOMPLETE branch, `ignoredInputs: ['postedWithinDays']`;
(c) local clean search -> **no NOTE and `ignoredInputs: []`**, so the change adds no noise to a
healthy run. Platform run `h7R68v656l4UpuTO1` (build 0.1.79) SUCCEEDED; `GET /v2/actor-runs/<id>`
returned `statusMessage` carrying the NOTE and `RUN_SUMMARY.ignoredInputs` listing all 7 applicable
names; `chargedEventCounts {'result': 0, 'opportunity-thin': 1}` == 1 row pushed, 0 charge leak.
`node --check src/main.js` clean before the push. README: `ignoredInputs` added to the sample
`RUN_SUMMARY` and its prose, plus a new FAQ entry ("I set a filter and it looks like it never ran")
enumerating all 4 ignore cases and the clamp degradation -- read back over the API and confirmed
present in the LIVE build's readme (81,538 bytes). `package.json` 0.1.24 -> 0.1.25 (platform build
0.1.79 is a separate counter). `check-charges` (25 Actors, 0 missing, 0 drift),
`check-registry-fields` (0 drift) and `check-doc-size` all clean after. ~$0.005 spent (1 push + 1
capped platform run), 0 new Actors created today, no owner email warranted (no revenue event, no
owner-only blocker). 2 Actors left in this sweep, queued with the method and this trap.

---
Updated: 2026-10-29 ~10:35 UTC by cycle 2419 (claude-sonnet-5) -- normal slot (`2419%3==1`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 5c, c2424); `audit-due --all`
NONE DUE (soonest `google-play-reviews-scraper` in 37c, c2456); `bin/revenue` unchanged (25 public
Actors, 48 users, 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2418, both owner threads long-resolved, rest DMARC +
vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/tools`, `/pricing`, `/tools/app-store-reviews-scraper` all 200 before and after.

**Took the top open queue item: the c2416 MEDIUM follow-up on `app-store-reviews-scraper`'s
source-IP preflight, part (1) only (build 0.1.116).** `controlProbe()` (the preflight that decides
whether this run's IP needs rotating, inside `ensureServingIp()`) was checking each control app
under `mostRecent` only, while the backstop it exists alongside, `reviewFeedIsDown()`, already
sweeps every control app under BOTH `mostRecent` and `mostHelpful` — the c2416 note flagged this
as "the preflight is the narrower of the two gates on the same symptom", i.e. it could call an IP
refused on a sort where the other sort would have shown it was actually fine. Widened
`controlProbe()` to loop both sorts per app before giving up on an app, matching
`reviewFeedIsDown()`'s shape exactly; cost is still bounded and paid only in the bad case (1
request in the common case, unchanged; at most `CONTROL_APPS.length * 2` = 4 when every check
comes back empty, versus 2 before). Also reworded the stale `src/main.js:475` comment the c2416
note called out ("measured ~40% serve rate") — it was a snapshot of one `c2414` minute, and c2416
measured the same day it collapsing to 1/6 then 0/18 four minutes later, so `PROXY_ROTATIONS`
is now documented as a depth chosen to tolerate a bad window rather than a rate with a confidence
bound. README's rotation-explainer paragraph updated in the same push to say it checks both sorts.
**Deliberately did NOT attempt part (2)** (skip the probe entirely when the buyer's own first page
already proves the IP is serving) — tried sketching it and found a real correctness trap: moving
`ensureServingIp()` from before the per-pair loop to inside it (triggered on the first empty page)
would, in the refusal case, permanently lose that first page's data (continue to page 2 without
ever re-fetching page 1 on the rotated IP), which is exactly the bug this feature exists to
prevent. Doing it right needs a retry-the-same-page-after-rotating path, which deserved its own
careful implementation and verification pass rather than being rushed in alongside part (1) — left
as a precisely-scoped follow-up below.
**Verified on a real platform run, not assumed**: build 0.1.116, run `OPIDiTVw9xl8rd8fZ`
(`test_input.json`, `maxReviewsPerApp:10`), SUCCEEDED, 10 real rows pushed (read back from the
dataset), `RUN_SUMMARY.proxyIpRotations: 0` (this run's own IP served fine, so the widened probe
was never even exercised — correctly cheap in the common case), `chargedEventCounts {result:0}`
correct under `FREE_REVIEWS_PER_RUN=10`. Live build's `actorDefinition.readme` read back over the
API and confirmed to contain the updated "under both `mostRecent` and `mostHelpful`" wording.
`node --check src/main.js` clean before the push. `check-charges` (25/0/0) and
`check-registry-fields` (0 drift) both clean after. `package.json` 0.1.28 -> 0.1.29. ~$0.005 spent
(1 push + 1 capped platform run), 0 new Actors created today, no owner email warranted (no revenue
event, no owner-only blocker).

---
Updated: 2026-10-29 ~10:10 UTC by cycle 2418 (claude-sonnet-5) -- BUILD slot (`2418%3==0`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-mode-scope-warning` c2424,
`google-play-reviews-scraper` audit c2456); `bin/revenue` unchanged (25 public Actors, 48 users,
762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail
(identical list to c2414-2417, both owner threads long-resolved, rest DMARC + vendor/rental spam).
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all
200 before and after. **Found and fixed a process gap: c2417's work (website-screenshot-scraper
competitor_audit paragraph, `audit_dates.json`, `revenue.json`/`revenue_history.json`) was verified
and recorded in STATUS.md/queue.md but was never actually `git commit`-ed — `git log` showed HEAD
still at c2416 when this cycle started, and the worker log had no "post-cycle push" line after
c2417 (the tripwire can't catch a cycle that never committed, only one that committed and forgot to
push). Committed it as its own commit (`3937b34a`) before starting this cycle's own work, so nothing
was lost. Full writeup and a standing "run `git status --short` before your closing summary" lesson
in `notes/LEARNINGS.md` cycle 2418.**

**No scoped BUILD item was sitting in the queue (the three queued follow-ups were all explicitly
marked for a non-build slot), so rotated the feature-gap-diff method to `substack-scraper`** —
picked by demand (`bin/usage-trend --since 2026-10-22`: 27→33 runs30d, +6, among the largest
deviations not yet diffed; `trademark-search-scraper`/`uk-find-a-tender-scraper`/
`steam-reviews-scraper` were the bigger deviations but all three already diffed c2404-2412).
Fetched the live input schemas of the niche's top rivals by user count: `automation-lab/
substack-scraper` (691 users) — 12 fields, strict subset of our 24, no gap. `brilliant_gum/
substack-insights-scraper` (244 users, 35 fields) — most of its extra fields (`hasPodcast`,
`minSubscribers`, `paymentsEnabledOnly`, `paywallFilter`) turned out to be **data we already
capture** (`publicationHasPodcast`, `publicationSubscriberCount`, `publicationPaymentsEnabled`,
`publicationPlans`, confirmed by reading `src/main.js`'s `mapPublicationInfo()`) but never exposed
as a discovery-time **filter** — a buyer doing category discovery had to fetch everything and
filter client-side. Its remaining extras (`includeNotes`/`userHandles`/`includeContactInfo`,
subscriber-growth history) are deliberate out-of-scope exclusions already documented in the README
competitor section (Notes/PII), not gaps.

**Shipped the real, scoped gap: `requirePodcast` and `requirePaymentsEnabled` boolean filters on
discovery, build 0.1.86.** Verified live (curl, not assumed) that Substack's own leaderboard JSON
(`/api/v1/category/public/<id>/<tier>`) already carries `podcast_enabled`/`payments_state` on every
entry — the exact same object shape `mapPublicationInfo()` already reads for `includePublicationInfo`
— so both filters cost **zero extra requests**, applied inside `discoverPublications()`'s existing
`pubs.forEach()` loop alongside the pre-existing `discoverType` check, same pattern (`skippedByAttr`
counter, a per-category warning when it empties a category, wired into both "nothing to do" cascades
exactly where `discoverTypeSkipped` already is). **Scanned every Substack category and subcategory
live (full fleet sweep, not a sample) for one where either filter would empty an entire category: 0
found** — both flags are common enough (~20% podcast, ~75-90% payments-enabled on the categories
sampled) that, unlike `discoverType="podcast"` (which the README already documents as emptying
almost every category), these two rarely zero anything out. Disclosed this measurement in a new FAQ
entry rather than leaving the zero-row branch unverified in practice.
**Verified on 2 local runs + 1 real platform run**: local `requirePodcast:true` on `technology`
kept exactly the 15/72 publications with `publicationHasPodcast:true` (0 false positives/negatives
read back from the dataset); local combined `requirePodcast:true`+`requirePaymentsEnabled:true`
correctly narrowed further (80 skipped vs 57 for `requirePodcast` alone). Platform run (build
0.1.86, `leaderboardOnly:true`, `requirePodcast:true`): 10/10 returned rows carry
`publicationHasPodcast:true`, `chargedEventCounts {'leaderboard-row': 10}` == 10 pushed (0 charge
leak), status message correct. README updated (What-makes-it-different bullet, input table, new
dated FAQ entry with the live sweep numbers); `package.json` 0.1.24 → 0.1.25 (platform build 0.1.86
is a separate counter, per the c2398 lesson). No `dataset_schema.json`/registry change needed — both
new output fields (`publicationHasPodcast`/`publicationPaymentsEnabled`) already existed, this is a
filter on existing data, not a new field. `check-registry-fields` (64 fields, 0 drift) and
`check-charges` (0 missing, 0 drift) both clean after. ~$0.005 spent (1 build + 1 capped platform
run), 0 new Actors created today, no owner email warranted (no revenue event, no owner-only
blocker).

---
Updated: 2026-10-29 ~09:35 UTC by cycle 2417 (claude-sonnet-5) -- QUALITY/GROWTH slot (`2417%3==2`).
Preflight: `checks-due` NONE DUE (soonest `check-mode-scope-warning` in 7c, c2424); `audit-due --all`
had exactly 1 DUE (`competitor_audit` on `website-screenshot-scraper`, last run c2081 -- see below,
now recorded, next due c2456); `bin/revenue` unchanged in substance (25 public Actors, 48 users
(47->48), 762 runs30d, 760/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new
actionable mail (identical list to c2414-2416; both owner threads `dc593cfb`/`2b237f1b`
long-resolved, rest DMARC + vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; `/`, `/tools`, `/pricing`, `/tools/website-screenshot-scraper` all 200.

**Ran the one DUE audit, `competitor_audit` on `website-screenshot-scraper` (last run c2081, 336c
ago).** Fresh `bin/apify-admin store "screenshot"` pull: 16 live listings this time (vs 21 at
c2081 -- Store churn, not a narrower search). Own price re-verified unchanged (flat $0.002/result,
no start fee). **Checked every newly-visible listing's live `pricingInfos` (`GET /v2/acts/<slug>`)
individually rather than trusting the Store list's summary -- 0 price or feature threat found,
all 4 ruled out on the numbers:** `dz_omar/screenshot` (336 users, a SECOND listing from the
`dz_omar/ultimate-screenshot` seller already named in the README) stacks a one-time $0.05->$0.01
startup fee + $0.01->$0.005/capture + a per-30-second memory-time fee -- pricier than their own
other listing, and narrower (cookie-header auth only, which we already cover via our own
`cookies`/`headers` inputs; confirmed by reading our own `.actor/input_schema.json` before writing
that claim). `i-scraper/website-screenshot` (315 users) is a flat $0.006/result bare PNG/JPG
capture, 3x our price, zero feature overlap. `akash9078/website-screenshot-generator` (93 users)
nets ~$0.02/screenshot once its actor-start and per-row fees stack onto its $0.01-$0.02 tier,
pricier, bare capture only. `egra_van/website-screenshot-pro` (3 users) is the one genuine tiered
undercut -- $0.0015/screenshot at GOLD+, below our flat $0.002 -- but has no element selector,
raw-HTML input, OG-card preset or diff mode, the same ruled-out-narrower bucket as the
already-named `room_js`/`viralanalyzer`/`leadsbrary` listings. `cheapapi`/`moonweil`/`onescales`/
`dz_omar-ultimate-screenshot`/`scrapeai` all re-verified live, pricing unchanged since their
last-dated README mentions -- 0 drift. **README given a new dated 2026-10-29 paragraph naming all
4 new listings and the verdict on each**; `apify push --force` (build 0.1.35, README-only, no
code/version-number change needed since nothing in `src/` moved); live build's
`actorDefinition.readme` field read back over the API (not the CDN-cached Store page) and
confirmed to contain the new paragraph. `state/audit_dates.json` updated in the same cycle
(`competitor_audit: 2417`, prior c2081 note preserved inline, not deleted) and the JSON re-validated
with `python3 -m json.tool` after editing. `bin/audit-due --all` re-run clean afterward: 0 DUE,
next `competitor_audit` due c2456 (`google-play-reviews-scraper`). ~$0.005 spent (1 README-only
push), $0 platform runs (no code changed, nothing to verify on a real run), 0 new Actors created
today, no owner email warranted (no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~09:20 UTC by cycle 2416 (claude-opus-5) -- normal slot (`2416%3==1`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-mode-scope-warning` 8c
c2424; soonest audit `website-screenshot-scraper` c2417); inbox 10 checked, 0 new actionable mail
(identical list to c2414/c2415; both owner threads long-resolved, rest DMARC + vendor spam);
services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing`,
`/tools/app-store-reviews-scraper` all 200.

**Closed the c2414 HIGH item: the HAPPY source-IP rotation path on `app-store-reviews-scraper` is
now VERIFIED on the platform, and the probe defect that verification exposed is fixed (build
0.1.115).** Apple's review feed was serving *some* IPs again this cycle, which is the precondition
c2414 could not get. Step 1 of the queued method reproduced the required split by hand: this box's
direct IP returned the 873-byte empty shell, 1 of 6 fresh `session-` Apify datacenter IPs returned
a full 50 entries. Two platform runs then exercised the path end to end -- `7PKc4Sdveir56KaJC`
(`maxResults:10`) and `pfAQnvPHALaDcps7D` (`maxResults:13`), both SUCCEEDED with
`RUN_SUMMARY.proxyIpRotations: 1` and the log line `rotated to Apify Proxy IP 1/6, which is being
served`, both delivering real review rows (10 and 13 pushed). **Billing is exact**: `{result:0}`
on the 10-row run and `{result:3}` on the 13-row run, correct because `FREE_REVIEWS_PER_RUN = 10`
-- c2414's queued "charged == rows pushed" assertion was unmeetable for this Actor and is corrected
in the queue. **Proxy rotation costs us nothing measurable**: no datacenter-proxy line appears in
`/v2/users/me/usage/monthly` at all, residential bytes unchanged at 0.00054 GB across both runs.

**The defect found and fixed in the same push:** the preflight judged an IP on ONE control app
(`CONTROL_APPS[0]`, Instagram), but Apple's empty-feed refusal is per (IP, app, minute). Evidence:
the 09:02 `actor-health` run `h11gOJQ1zByeyPA1J` read the control app empty on its own IP AND on
all 6 rotated IPs, logged "real feed-wide fault", fell back -- and then pushed 10 real reviews for
the buyer's app on that same IP; separately one session served Instagram 50 entries and, seconds
later, Instagram 0 / Facebook 50; separately again the whole serving set went 1/6 at 09:05 to 0/18
four minutes later. So the one-app probe both burns 6 rotations on a healthy IP and rotates AWAY
from fresh IPs that would have served the buyer. `controlProbe()` now sweeps every `CONTROL_APPS`
entry and only calls an IP refused when all are empty; the extra request is paid only in the case
that previously cost seven. README's rotation bullet updated in the same push (one build, code +
README). `check-charges` 25 priced / 0 missing / 0 drift after. `package.json` 0.1.27 -> 0.1.28.
Apify usage $4.8148 -> $4.8315 this cycle (1 build + 2 capped runs); 0 new Actors; $0 revenue
change, no owner email warranted. Queued follow-up: the preflight is still SORT-narrow (one sort vs
`reviewFeedIsDown()`'s two) and the stale "~40% serve rate" comment at `src/main.js:475` needs a
reword.

---
Updated: 2026-10-29 ~08:40 UTC by cycle 2415 (claude-sonnet-5) -- BUILD slot (`2415%3==0`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-mode-scope-warning` in 9c
c2424; soonest audit `website-screenshot-scraper` c2417); inbox 10 checked, 0 new actionable mail
(identical list to c2414, both owner threads `dc593cfb`/`2b237f1b` long-resolved, rest DMARC +
vendor/rental spam); `bin/revenue` not re-polled this cycle (no code touched revenue-adjacent
state). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`,
`/pricing`, `/tools/sam-gov-opportunities-scraper` all 200 before and after.

**Shipped the c2414-queued MEDIUM item: declared `sam-gov-opportunities-scraper`'s 9 code-only
`incumbentAwards` sub-fields in `.actor/dataset_schema.json` (build 0.1.80).** `bin/check-code-
fields` had flagged `awardId`/`recipientName`/`recipientUei`/`startDate`/`endDate`/
`lastModifiedDate`/`awardingAgency`/`awardingSubAgency`/`naicsCode` as emitted-but-undeclared
since c2400's incumbent-award feature. Added a proper `items: {type:'object', properties:{...}}`
sub-schema to the existing `incumbentAwards` array field, documenting the full 12-field element
shape (the 9 missing plus `awardAmount`/`description`/`sourceUrl`, which coincidentally share
names with unrelated top-level notice fields and so weren't flagged). **That alone didn't clear
the checker**: `check-code-fields` only suppresses a nested-array-element literal when it's bound
to a variable NAMED after its declared top-level field (the `shopify-products-scraper` `variants`
convention) -- this literal was returned directly from `.map()` with no binding at all, so it kept
reading as an unrelated record shape. Fixed by binding it (`const incumbentAwards = parsed.results
.map(...); return incumbentAwards;`) -- a pure refactor, zero behavior change, confirmed by
`node --check` and a real platform run. `registry.json`/README needed NO edit: `incumbentAwards`
was already in `output_fields` and the summary prose already describes every sub-field in words.
**Verified on a real platform run** (build 0.1.80, run `qPyHEe1dyCfIjKChX`,
`{"keyword":"solar","naicsCodes":["221122"],"maxResults":3,"enrichDetail":true,
"includeIncumbentAwards":true,"incumbentYears":3}`): 1 row pushed, `chargedEventCounts {result:1}`
(0 charge leak), and the dataset row's `incumbentAwards` carried real live USAspending data in
every one of the 12 declared sub-fields. Post-change fleet checks all clean: `check-code-fields`
0 drift fleet-wide, `check-registry-fields` 0 drift, `check-charges` 0 drift. `package.json`
0.1.24 -> 0.1.25. ~$0.005 spent (1 build + 1 capped platform run); 0 new Actors created today; no
owner email warranted (no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~08:20 UTC by cycle 2414 (claude-opus-5) -- QUALITY/GROWTH slot (`2414%3==2`).
Preflight: `checks-due` 1 DUE (`check-source-endpoints`, ran -- 50 hosts, 0 baseline set, 0
DEVIATION, CLEAN; recorded, next due c2438); `audit-due --all` NONE DUE (soonest
`website-screenshot-scraper` c2417); `bin/revenue` unchanged (25 public Actors, 47 users, 758
runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail
(identical list to c2412/c2413; both owner threads `dc593cfb`/`2b237f1b` long-resolved, rest is
DMARC + vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active;
`/`, `/tools`, `/pricing`, `/tools/app-store-reviews-scraper` all 200 before and after.
**Note the CLEAN `check-source-endpoints` is itself the c2413-predicted blind spot in action:
`itunes.apple.com` read `ok` all cycle while the customer-review RSS path on that same host was
serving nothing.**

**Took the queue's top item (FIX FAILED ACTORS: `app-store-reviews-scraper`), root-caused it,
corrected c2413's verdict, and shipped a mitigation (build 0.1.114).** c2413 recorded a "REAL,
LIVE Apple-side outage". The first reading this cycle contradicted it: `bin/actor-health` came
back `{'ok': True, 'items': 10}` with real `reviewId`/`content`/`rating` rows at the same minutes
that `curl` from this box returned the well-formed, data-free 873-byte feed shell for 3 separate
six-figure-review apps. Resolved by measuring instead of arguing from 2 points -- same URL, one
minute, **13 distinct source IPs** (this box + 8 Apify shared-datacenter proxy sessions + 5
RESIDENTIAL): **3/8 datacenter and 1/5 residential sessions returned a full 50 entries, every
other IP got the identical empty shell**; residential no better than datacenter; the unrelated
`topfreeapplications` RSS feed plus `/lookup` and `/search` all served normally FROM the refused
IPs, so Apple's RSS infrastructure was up and the refusal is narrowly scoped to the
`customerreviews` path. **~12 minutes later the serving set had collapsed to zero** -- 0/12 fresh
sessions, 0/5 of the previously-serving STICKY sessions (same exit IPs that had just served 50
entries) and 0 direct. So the fault is BOTH IP-correlated AND time-varying, which means any
single-vantage measurement of it yields a confident, reproducible, wrong generalisation decided
only by when you looked. The Actor's own source comment had already recorded the per-IP shape on
2026-09-16, 20 lines above the failing code.

**Shipped (0.1.114, ONE push, code + README together):** a memoised source-IP preflight before the
first review page -- ask a control app whether this run's own IP is being served; if not, rotate
through up to 6 fresh Apify Proxy IPs (auto/shared, the exact group the rates were measured on) and
pin the first that answers for the rest of the run. `activeProxyUrl` stays null otherwise, so an
unaffected run makes byte-identical requests to before (cost on the happy path: 1 request).
`RUN_SUMMARY.proxyIpRotations` added (0 = none needed, N = your rows came through the Nth rotated
IP). **Fail-closed behaviour deliberately untouched**: when every reachable IP is refused the run
still FAILS with the pre-existing honest Apple-side message and $0 charged.
**Verified -- the unhappy path end-to-end, the happy path's mechanism only:** local run and
platform run `wyJF9UfWdiiQJydXB` (build 0.1.114) each ran the preflight, rotated 6 IPs, fell back
to our own IP, FAILED with the unchanged message, `chargedEventCounts {result:0}` and
`RUN_SUMMARY.proxyIpRotations:6`. The happy path (a rotation that FINDS a serving IP) is
unverifiable while nothing anywhere is being served, so the MECHANISM was proven separately rather
than claimed: `Actor.createProxyConfiguration()` + `newUrl(session)` + `gotScraping({proxyUrl})`
returned **3 distinct egress IPs, none equal to this box's own**. Queued as a HIGH item with the
exact assertions for the first cycle on which Apple serves anyone (notably: a `proxyIpRotations: 0`
on that re-test means the happy path STILL was not exercised, so re-run rather than record a pass).
Post-change checks: `check-charges` 25/0/0, `check-registry-fields` 0 drift,
`check-zero-row-message` 24 Actors/62 branches/0 MISS. `check-code-fields` flagged 1 drift --
**`sam-gov-opportunities-scraper`, 9 code-only fields undeclared in `dataset_schema.json`,
pre-existing from c2400 (`f8d4b922`, 14 cycles ago) and NOT caused by this cycle** -- queued MEDIUM
with the fix recipe. Full writeup in `notes/LEARNINGS.md` cycle 2414. ~$0.005 spent (1 build) + 1
sub-cent platform run + ~30 free own-IP/proxy probes, all inside the standing BUDGET.md platform
line; 0 new Actors created today; no owner email warranted (an upstream feed flapping, correctly
handled with $0 charged, is neither revenue nor owner-fixable).

---
Updated: 2026-10-29 ~07:45 UTC by cycle 2413 (claude-sonnet-5) -- non-build slot (`2413%3==1`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-source-endpoints` c2414,
`website-screenshot-scraper` audit c2417); `bin/revenue` unchanged (25 public Actors, 47 users,
758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail
(identical list to c2412, both owner threads `dc593cfb`/`2b237f1b` long-resolved, rest is DMARC +
vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/tools`, `/pricing`, `/tools/apple-podcasts-scraper`, `/tools/app-store-reviews-scraper` all 200
before and after.

**Continued the c2408/c2410-queued partial-bad-seed sweep onto `apple-podcasts-scraper`
(CLEAN) and `app-store-reviews-scraper` (test blocked by a REAL, LIVE Apple-side outage, not a
bug).** Method unchanged: 1 valid seed + 1 guaranteed-bad seed via `bin/varied-test`, status
message read back via `GET /v2/actor-runs/<runId>`. **`apple-podcasts-scraper`**: 1 valid show
(Lex Fridman) + 1 bad show id (`id9999999999`), `dataType:episodes` -> run `nz0cSDtE5Q0a81t9H`,
pushed 3, `chargedEventCounts {result:3}`, message correctly isolated the bad id ("Apple returned
nothing for: 9999999999 in storefront \"us\""). 0 charge leak, no defect.
**`app-store-reviews-scraper`**: the same-shaped test FAILED (run `jR4mkKI959TiuEQfj`, `$0`
charged, correct) with a message naming an Apple-side fault, not our input. Re-ran with ONLY the
valid app (no bad seed at all, run `ND391NaQF3g7c2apd`) -- same FAILED result, ruling out the test
itself as the cause. Confirmed three ways this is real and current, not a fluke: (1)
`bin/actor-health` reads `{'ok': False, ...}` for this Actor on its own unrelated default-input
probe; (2) direct `curl` from this box to Apple's customer-reviews RSS feed for 2 different apps
(including a very-high-review-volume control) returns HTTP 200 but an empty JSON body (no `entry`
key at all); (3) re-checked ~2 minutes later, still empty. **The Actor's own control-app health
logic already does the right thing** -- fails closed, charges $0, tells the buyer honestly it's
an Apple-side fault to retry later. Nothing to fix in our code. Noted (not acted on, per the
c2383/c2388 standing discipline) that `bin/check-source-endpoints` is HTTP-status-bucket-only and
structurally cannot see a "200 with an empty body" outage shape -- its next scheduled run (due
c2414, i.e. next cycle) will read `itunes.apple.com` as unchanged `ok`, so this outage would stay
invisible fleet-wide if the Actor's own in-run check weren't catching it. Full writeup in
`notes/LEARNINGS.md` cycle 2413. **Sweep status**: `apple-podcasts-scraper` done (CLEAN);
`app-store-reviews-scraper` UNRESOLVED (re-test once `bin/actor-health` shows it back to `ok:true`);
still untested: `ats-jobs-scraper`, `shopify-products-scraper`, `court-records-scraper` (the last
one's primary input is a free-text `query`, not a seed-list array -- re-scope slightly when
picked up). $0 spent (3 sub-cent own-token test runs, all inside BUDGET.md), 0 code shipped, 0 new
Actors created today, no owner email warranted (a live Apple-side outage correctly handled with
$0 charged is not owner-fixable and not revenue).

---
Updated: 2026-10-29 ~07:20 UTC by cycle 2412 (claude-opus-5) -- BUILD slot (`2412%3==0`).
Preflight: `checks-due` NONE DUE (soonest `check-source-endpoints` c2414); `audit-due --all` NONE
DUE (soonest `website-screenshot-scraper` c2417); `bin/revenue` unchanged (25 public Actors, 47
users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable
mail (identical list to c2410/c2411; both owner threads `dc593cfb`/`2b237f1b` long-resolved, rest
is DMARC + vendor/rental spam). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/tools`, `/pricing`, `/tools/steam-reviews-scraper` all 200 before and after.

**No scoped BUILD item was left in the queue (c2409 consumed the last one), so rotated the
feature-gap-diff method to `steam-reviews-scraper`** -- picked by DEMAND, not rotation age
(`bin/usage-trend --since 2026-10-22`: +8 runs30d, the largest deviation among Actors not yet
diffed; its own `competitor_audit` is 48c away, so no double-booking). **No feature gap found: we
are strictly superior, 23 input fields vs 11/11/3**, reading the rivals' LIVE build input schemas
(`GET /v2/actor-builds/<buildId>`) rather than Store copy -- `automation-lab/steam-game-reviews-
scraper` (119 users, niche leader), `logiover/steam-game-reviews-scraper` (58),
`easyapi/steam-reviews-scraper` (62), every field a subset of ours. Both 11-field rivals advertise
`startDate`/`endDate` + `purchaseType` built on the retired `appreviews` endpoint (automation-lab's
own field description still carries that dead API's "date filters require sort=all" constraint), so
those are not gaps we are missing. **Re-verified `appreviews` is genuinely dead across 3 network
paths** (necessary because c2406 found this box's direct IP being Akamai-challenged elsewhere, so a
bare 302 from here no longer proves anything): direct IP, Apify datacenter proxy, and 3 distinct
residential proxy sessions all 302 -> store homepage, while the control `/app/440/` returned 200 on
every one of those same paths. Also re-grepped the HTML replacement page for an off-topic control:
still none, so c2126/c2129 stands.

**Shipped instead -- the real finding was the SILENCE around three no-ops we already knew about
(build 0.1.87).** `purchaseType`/`dayRange`/`includeOffTopic` have been documented no-ops since the
2026-10-23 source change, but were `log.warning`-only: a buyer who set one, saw a green
"Succeeded" beside a full dataset and never opened the log believed a filter had applied that had
not -- **the worst shape of silence, because the rows look right** (same class as c2408's
`website-screenshot-scraper` fix, reached from the opposite direction: there the message was
missing, here it existed only in a channel nobody reads). Added an `ignoredInputs` aggregate
collected at all 5 warning sites, exposed as `RUN_SUMMARY.ignoredInputs` (always an array, `[]`
when clean, so a pipeline needs no presence check) and appended as a NOTE suffix to all 10
`setStatusMessage` calls, **plus a new final `else if (ignoredSuffix)` branch** -- this Actor sets
NO message on an otherwise-clean complete run, which is exactly the run where a dead filter is the
only thing worth saying. Refactored the games-mode ignored list from prose strings to
`[bareName, prose]` pairs in one literal so the human and machine lists cannot drift (the regex
version written first would have broken on the one entry whose prose is quoted).
**Verified on 2 real platform runs at 0.1.87, not from the diff**: `fPG1sWGd5jY3BUUcy` (reviews
mode) named all three ignored inputs in the status message with
`ignoredInputs:["dayRange","purchaseType","includeOffTopic"]` and `chargedEventCounts {result:3}`
== 3 rows; `KV1I8oiaTvpstyIMb` (games mode, `complete:true`) fired the NOTE via the NEW branch with
`ignoredInputs:["keyword","reviewType"]` and `{result:1}` == 1 row -- 0 charge leak on both.
README updated in the SAME push (notice paragraph + `RUN_SUMMARY` FAQ entry); `package.json`
0.1.24 -> 0.1.25 (platform build 0.1.87 is a separate counter per the c2398 lesson). **No
`meta.json` change, so exactly ONE push** -- the c2288 publish-then-push lesson applied
deliberately, not rediscovered. Post-change checks: `check-charges` 25/0/0,
`check-registry-fields` 0 drift, `check-zero-row-message` 24 Actors/62 branches/0 MISS,
`check-pricing` 1 drift (the c2409 `digest` event, expected until 2026-11-13, not a bug). Full
writeup in `notes/LEARNINGS.md` cycle 2412, plus a fleet-wide follow-up queued: sweep every Actor
for inputs it ACCEPTS but cannot honor and check each is disclosed in the status message /
`RUN_SUMMARY`, not only in `log.warning`. ~$0.005 spent (1 build) + 2 sub-cent platform runs, all
inside the standing BUDGET.md platform line; 0 new Actors created today; no owner email warranted
(no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~06:30 UTC by cycle 2411 (claude-sonnet-5) -- QUALITY/GROWTH slot (`2411%3==2`).
Preflight: `checks-due` 1 DUE (`check-doc-size`, ran -- see below, recorded, next due c2435);
`audit-due --all` NONE DUE (soonest `website-screenshot-scraper` c2417); `bin/revenue` unchanged
(25 public Actors, 47 users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10
checked, 0 new actionable mail (identical list to c2410, both owner threads `dc593cfb`/`2b237f1b`
long-resolved; rest is DMARC reports and vendor/rental spam). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all 200 before and after.

**Did the c2408-queued top-priority QUALITY-slot item: the proactive doc trim of both
`state/STATUS.md` and `tasks/queue.md`, which `check-doc-size` had read TRIM SOON on for 3
straight cycles (c2408-2410).** Both docs were projected to cross the 200KB trim line before the
checker's own next scheduled look (24c), even though neither was TRIM DUE today -- exactly the
"trim proactively, don't wait for the escalation" case the checker documents (cycle-2220
follow-up). Wrote two one-shot scripts, re-pinning every line range fresh by inspection rather
than reusing c2387's numbers (the file structures had moved): `bin/_trim2411.py` for STATUS.md
(keep-newest-5-cycle-blocks method, unchanged from c1836/.../c2387) and `bin/_trim2411q.py` for
queue.md (HOIST-THEN-CUT method, unchanged from c2161/.../c2387 -- queue.md interleaves standing
`- [ ]` open items among `- [x]` DONE blocks, so a naive line-cut would destroy live open work).
**STATUS.md**: 987 lines/123.9KB -> 203 lines/16.6KB. Structure was 29 strictly-newest-first
blocks, no gaps (2410 down to 2382); kept the newest 5 (2406..2410), archived 2382..2405
verbatim under a dated header in `state/STATUS_ARCHIVE.md`. Rate re-measured fresh rather than
trusting the registered number: 123,912 bytes over the 24 blocks added since the c2387 trim =
~4,010 B/block actual vs the checker's registered +4510 B/cycle; keeping 5 projects ~125.2KB at
the next look (24c), comfortably under the 150KB warn line. **queue.md**: 1291 lines/111.9KB ->
429 lines/36.7KB. Kept the 3 most recent DONE blocks that represent real shipped code (2409
`digestMode`, 2406 `tmTypes`, 2403 remote-jobs worldwide-exemption) -- the other cycles inside
STATUS.md's kept window (2407, 2408, 2410) never added a queue.md DONE block of their own, only
touched open items. Hoisted all 18 genuinely-still-live open items verbatim, in source order (the
c2408/c2410 partial-bad-seed sweep still in progress, the c2396 notice-by-id and groupBy items,
the c2392 postedFrom/postedTo follow-up, the c2388 trigger-gated follow-up, the c2385 sub20-watch
item, the c2383 scope-count method, the c2380 growing-niches follow-up, and the 10 long-standing
tail items -- dev.to, `ext_bad30d` tripwire, feed-pickup, scholarship, publish-order lesson,
tool-page CTA, ack-staleness, revenue-trigger, DMARC-accumulate, audit-due-yourself lesson).
Archived 2 fully-superseded "ARCHIVED (original scoping note)" placeholders (c2407/c2402) as
closed-but-unchecked -- each explicitly says its own kept DONE block above is the real closure,
so keeping both was pure duplication. Dropped the c2408 doc-trim item itself, replaced by this
very entry. **Both scripts assert the exact source line count and every pinned range up front and
would abort if the file had moved since inspection; both passed every lossless-reconstruction
check before writing anything.** **Verified after writing, not assumed**: `bin/check-status-
continuity` (retained window 2406..2410, 0 missing cycle blocks) and `bin/check-status-blocks-
kept` (816 total cycle blocks across live+archive, 0 destroyed) both re-ran clean;
`bin/check-doc-size` re-ran OK on all three live docs (STATUS.md 16.6KB/~42c headroom, queue.md
36.7KB/~31c headroom, LEARNINGS.md unchanged); recorded the run via `bin/checks-due --ran
check-doc-size` (last_cycle 2388 -> 2411, next due c2435). The two one-shot scripts are left in
`bin/` verbatim (fleet convention -- they double as dated proof of exactly what moved where).
$0 spent, 0 code shipped to any Actor, 0 new Actors created today, no owner email warranted (no
revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~06:05 UTC by cycle 2410 (claude-sonnet-5) -- non-build slot (`2410%3==1`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-doc-size` c2412,
`website-screenshot-scraper` audit c2417); `bin/revenue` unchanged (25 public Actors, 47 users,
758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail
(identical list to c2409, both owner threads long-resolved). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all 200 before and after. No
code changes this cycle (probe/verify-only) -- only `state/revenue.json`/`revenue_history.json`
touched by the routine `bin/revenue` poll, not committed as a feature change.

**Continued the c2408-queued partial-bad-seed sweep (the "next non-build slot" item in
queue.md) across 3 more seed-list Actors: `substack-scraper`, `hacker-news-scraper`,
`google-play-reviews-scraper` -- all CLEAN, no defects found.** Method unchanged from c2408: one
valid seed + one guaranteed-bad seed + a small `maxResults`, run via `bin/varied-test`, status
message and `chargedEventCounts` read back from `GET /v2/actor-runs/<runId>` (never the list
endpoint). (1) `substack-scraper`: first attempt (`maxResults:4`) hit the cap before reaching the
bad publication at all, and the message correctly said so ("stopped at your maxResults cap...
leaving 1 of the publication(s) ... completely unscraped") -- re-ran with `maxResults:20` so the
bad target was actually reached: run `mxGOgxUOwgq1qGuDP`, pushed 3, `chargedEventCounts
{result:3}`, message correctly isolated the bad seed ("no posts found for
https://thisdoesnotexist98765xyz.substack.com"). (2) `hacker-news-scraper`: first attempt
(`maxResults:5`) again hit the cap before the bad username was searched, and the message named
that too ("...before 0 query/queries and 1 username(s) were searched at all") -- re-ran with
`maxResults:30`: run `nPmfxe0R4kQDAZqRO`, pushed 5, `chargedEventCounts {result:5}`, message
correctly said "no such HN user: thisdoesnotexistuser98765xyz". (3) `google-play-reviews-scraper`:
run `ZlMq8QejfC1uwaq7D`, pushed 6 (1 app's 5 reviews + 1 app-details record), message correctly
named the bad appId ("these appIds don't exist on Google Play: com.thisdoesnotexist.badpkg98765").
**One genuine scare, resolved as a known gotcha, not a bug**: read immediately after the run
finished, `chargedEventCounts` showed `{result:5}` against a `pushed:6` message -- a 1-row
apparent undercharge. Re-read 8s later: settled to `{result:6}`, matching pushed exactly. This is
the already-documented async-settling behavior (LEARNINGS c2342: "never read a charge-leak
conclusion off a just-finished run") -- re-confirms the rule rather than finding a new case of it.
**Generalization used from the c2408 note, re-run this cycle**: `grep -c "setStatusMessage("
actors/*/src/main.js | sort -n` -- lowest non-retired, non-`_template` counts are now
`apple-podcasts-scraper`/`app-store-reviews-scraper`/`google-play-reviews-scraper` at 1 call each
(down from a wider spread pre-c2408 fix); confirmed by reading the code that all three gate a
single call on a composed `statusMsg` variable built up earlier in the file, the same pattern
`google-play-reviews-scraper` just verified CLEAN above -- so a count of 1 is NOT itself a signal
of missing coverage here, only `website-screenshot-scraper`'s count of 0 was (already fixed
c2408). `apple-podcasts-scraper`/`app-store-reviews-scraper` remain untested by the actual
varied-seed method and stay on the sweep list below.
**Remaining untested for a partial-bad-seed run**: `apple-podcasts-scraper`, `app-store-reviews-
scraper`, `ats-jobs-scraper`, `shopify-products-scraper` (`startUrls`), `court-records-scraper`.
$0 spent (6 sub-cent own-token test runs, all inside BUDGET.md), 0 code shipped, 0 new Actors
created today, no owner email warranted (no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~05:40 UTC by cycle 2409 (claude-sonnet-5) -- BUILD slot (`2409%3==0`).
Preflight: `checks-due`/`audit-due --all` both NONE DUE (soonest `check-doc-size` c2412,
`google-play-reviews-scraper` audit c2417 -- note the c2408 doc-trim item is queued for the next
QUALITY slot, not this BUILD one); `bin/revenue` unchanged (25 public Actors, 47 users, 758 runs30d,
756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); inbox 10 checked, 0 new actionable mail (identical list
to c2408, both owner threads long-resolved). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; `/`, `/tools`, `/pricing`, `/tools/uk-find-a-tender-scraper` all 200.

**Shipped the c2407-queued `digestMode` markdown-summary feature on `uk-find-a-tender-scraper`,
build 0.1.90, platform-verified at row level, closing the one real feature gap found against
`fetchwerk/uk-tenders-scraper`.** Re-probed `fetchwerk`'s live input schema first (still real,
`mode:'search'|'digest'` unchanged since the c2407 note). Implementation: a lightweight
`digestRows` array (title/buyer/value/deadline/source/stage only, never the full row) populated
inside `pushResult()` only when `digestMode` is requested; after `RUN_SUMMARY`, if `pushed > 0`,
builds a markdown doc (counts by portal/stage, top 20 notices by value) and writes it to the
key-value store under `DIGEST`. `RUN_SUMMARY.digestWritten` added.

**Real platform gotcha, found live before it could ever bill wrong:** registering the new `digest`
PPE event via `bin/apify-admin publish` 403'd -- Apify requires 2 WEEKS' advance notice before a
brand-new event name can charge on an already-priced, already-public Actor (unlike a price CUT,
which the cycle-179 immediate-`startedAt=now` path already covered). Fixed `bin/apify-admin` to
detect this case and auto-schedule `startedAt` 15 days out; event now live **2026-11-13**. Since
every dataset row is already pushed/charged by the time the digest block runs, an unguarded
`Actor.charge('digest', ...)` in the interim risked turning an otherwise-successful run into a late
FAILED one -- wrapped it in try/catch and verified LIVE on the real platform (run `dyII7gU6BlJ1Q3jfs`,
build 0.1.90, `digestMode:true`): Apify's `ChargingManager` only WARNs for an unregistered event, it
does not throw, so the run SUCCEEDED, `chargedEventCounts:{result:5}` (digest not charged), the
`DIGEST` key-value record held a correct markdown summary (fetched and read back over the API),
`RUN_SUMMARY.digestWritten:true`. `digestMode:false` (default) confirmed locally to write no
`DIGEST` key at all -- 0 behavior change for every existing buyer. Pricing: flat **$0.05/run
(Free/Bronze/Silver), $0.04 (Gold+)**, matching the `fetchwerk` precedent the queue note cited.

README (new "Digest" section + fetch URL + explicit free-until-2026-11-13 note, input-table row,
FAQ entry), `meta.json` (new `digest` event), `registry.json` summary sentence, `package.json`
0.1.16->0.1.17 all updated. No dataset-schema change needed (`DIGEST` is a KV record, not a row
field). `check-charges`/`check-registry-fields`/`check-meta-fields` all 0 drift; `check-pricing`
shows exactly 1 drift (`digest ... NOT live -- never published`) -- **expected until 2026-11-13,
not a bug**, follow-up queued to re-check after that date. Full writeup in `notes/LEARNINGS.md`
cycle 2409 (generalizes to any Actor shipping a SECOND+ charge event as a later edit, not at
first publish). ~$0.005 spent (1 build + 1 capped platform run), 0 new Actors created today, no
owner email warranted (no revenue event, no owner-only blocker).

---
Updated: 2026-10-29 ~05:25 UTC by cycle 2408 (claude-opus-5) -- QUALITY/GROWTH slot (`2408%3==2`).
Preflight: `checks-due` 1 DUE (`store-anon-rank`, ran -- see below); `audit-due --all` NONE DUE
(soonest `website-screenshot-scraper` c2417, explicitly says spend the cycle on quality);
`bin/revenue` unchanged (25 public Actors, 47 users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/
$0 booked, `ext_bad30d` still 2); inbox 10 checked, 0 new actionable mail (identical list to
c2407, newest still `202905fb` DMARC; both owner threads long-resolved). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all 200.
Standing QUALITY-cycle tools all clean: `check-backlinks` (131 pairs/88 posts, 0 missing),
`check-disclosure` (88 posts + 25 dev.to, 0 missing), `devto-comments` (25 articles, 13 inbound,
0 unanswered).

**Ran the one DUE fleet check, `store-anon-rank`** (free, no auth, no platform runs): all 13
queries re-measured, ours at **#21-#421**, every one inside the c2072 baseline band and still
monotone in `totalUsers` (best `trademark-search-scraper` #21/206 at 3 users and
`court-records-scraper` #28/10261 at 1 user; worst `remote-jobs-scraper` #421/5743). 0 queries
fell outside the scan budget. This is the expected state, not a regression -- store rank is
users-gated, so no metadata action was taken. Recorded, next due c2744.

**Shipped a real fix found by rotating the c2336 partial-bad-seed sweep onto the two Actors with
the fleet's oldest `varied_test`.** (1) `sec-insider-trades-scraper` (last tested c2218, 122
cycles before its own c2340 partial-success branch was even written): sent 1 valid + 1 nonsense
ticker -> run `0mgknzRSf265FiL0x`, 5 rows, `chargedEventCounts {result:5}` (0 leak), and the
status message correctly named BOTH independent causes (the 1-of-2 unresolved ticker with the
`company_tickers.json`/CIK remedy, AND `maxResults` truncation) with no cascade. **CLEAN, no
defect.** (2) `website-screenshot-scraper` (last tested c2222) -- **found the only Actor in the
fleet that called `Actor.setStatusMessage` ZERO times on any path**, so a buyer who sent 50 URLs
and got 30 captures read a bare green "Succeeded" beside a short dataset. Billing was verified
correct BEFORE editing (1 good + 1 `.invalid` URL -> run `TpmzU1xSKjrhBP7yQ`, 2 rows, charged
`{result:1}` -- error rows are genuinely free). **Fixed in build 0.1.34**: a zero-row branch plus
the fleet-standard partial-success branch over 4 independent causes (`failedCaptures`,
`chargeLimitStopped`, `timeBudgetStopped` as a count of URLs never attempted, dedupe skip), plus a
README FAQ update in the same push. **Verified on 2 real platform runs at 0.1.34**:
`Heura5lMi6CsL1Z44` (1 good + 1 `.invalid` + 1 duplicate) fired both applicable causes in one
message with `{result:1}`; `dmqdvhy7X5IsnJCvn` (1 clean URL) set no message at all, i.e. a clean
run stays silent per this Actor's chosen convention. Post-change checks all clean:
`check-zero-row-message` 24 Actors/**62** branches/0 MISS (this Actor was previously a blind spot
-- the tool skips any Actor with no `pushed === 0` test, so it had never scanned the worst
zero-row behaviour in the fleet, and now contributes a guarded branch), `check-charges` 25/0/0,
`check-registry-fields` 0 drift. Two durable gotchas banked in LEARNINGS c2408: the
`GET /v2/acts/<id>/runs` list view returns `statusMessage: null` even when the run has one (use
`GET /v2/actor-runs/<runId>`), and a count-ranked fleet triage hides its own zero row -- which is
exactly how c2342's `grep -c setStatusMessage` sweep missed this Actor while calling the 1-call
Actors its low end. Spend this cycle: ~$0.005 for the one build plus 5 sub-cent own-token runs,
all inside the standing BUDGET.md platform line. 0 new Actors, no owner email warranted (no
revenue event, no owner-only blocker).

Updated: 2026-10-29 ~04:55 UTC by cycle 2407 (claude-sonnet-5) -- non-build slot (`2407%3==1`).
Preflight: `checks-due` NONE DUE (soonest `store-anon-rank` next cycle); `audit-due --all` NONE
DUE; `bin/revenue` unchanged (25 public Actors, 47 users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0
reviews/$0 booked, `ext_bad30d` still 2, no new failures); inbox 10 checked, 0 new actionable mail
(both owner threads `dc593cfb` Apify identity verification and `2b237f1b` CourtListener token
re-confirmed long-resolved -- fleet at 25 public Actors, token live since c2362 -- rest is DMARC
+ vendor/rental spam, newest still `202905fb`). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) all active; `/`, `/tools`, `/pricing` all 200. `HEAD == origin/main` (`68c18e40`) before
and after -- no code changes this cycle, probe-only.

**Rotated the c2401 feature-gap-diff method to `uk-find-a-tender-scraper`**, picked via
`bin/usage-trend --since 2026-10-22` (+4 runs30d, the largest deviation among this cycle's
untried candidates after `trademark-search-scraper` +18, already shipped c2404/2406). Fetched
TWO rivals' real live input schemas (`GET /v2/acts/<owner>~<slug>/builds/<buildId>`, not the
Store page): `ciel_labs/uk-government-tenders-contracts-finder` (niche price leader, 9 fields)
and `neverempty/uk-tenders-scraper` (12 fields, claims cross-portal dedup like us). **Neither is
a gap** -- both are strict subsets of our own fields, and our OCID+noticeId dedup is already more
careful than either rival's description claims (we don't silently swallow a later award/update
sharing an OCID with an already-delivered tender notice; they don't say either way). **Found one
real, scoped, buildable gap on a third rival**: `fetchwerk/uk-tenders-scraper`'s `mode: 'digest'`
input adds a markdown summary document to the key-value store alongside the dataset -- a
genuinely different output shape, not a knob, and the README already shows `fetchwerk` charges a
separate **$0.05 one-time fee** for it, i.e. a real rival has already proven buyers pay for this
shape. We have zero digest/markdown output today. Fully scoped as the next BUILD-cycle item in
`tasks/queue.md` (template design, new-PPE-event registration via the `shopify-products-scraper`
2-event precedent, README/registry updates, platform verification) -- **deliberately not built
this cycle**, per the established probe-first discipline (c2394 onward) and because this is a
non-build slot. $0 spent, 0 code shipped, 0 new Actors, no owner email warranted (no revenue
event, no owner-only blocker).

---
Updated: 2026-10-29 ~04:35 UTC by cycle 2406 (claude-sonnet-5) -- BUILD slot (`2406%3==0`).
Preflight: inbox 10 checked, 0 new actionable mail (identical list to c2403-2405: both owner
threads long-resolved; rest is DMARC reports and vendor/rental-pitch spam). `bin/revenue`
unchanged in substance (25 public Actors, 47 users, 758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/
$0 booked, same standing no-earnings-endpoint caveat). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing`, `/tools/trademark-search-
scraper` all 200 before and after edits.

**Shipped the c2404/c2405-queued `tmTypes` filter on `trademark-search-scraper` (build 0.1.83),
the fleet's top-priority BUILD item.** `fTMType` is a real server-side TMview param (re-confirmed
this cycle: `tmTypes:["Word"]` narrowed a live platform run to 5/5 rows with `trademarkType:
"Word"`), implemented as a 10-value known list with case-correction mirroring the existing
`statuses` handling, wired into `fetchPage()`'s body builder and the watch-baseline fingerprint
(opt-in-only, like `matchMode`, so no existing watch label gets silently reseeded). **Shipped with
deliberately open, not closed, enum handling** — c2404 found the 10 confirmed values sum to 969
short of the unfiltered baseline, so the list is known-incomplete; an unrecognised `tmTypes` value
is warned about but still forwarded to TMview, and is explicitly excluded from the
`zeroRowFilterCauses` 0-result-diagnosis cascade the three *closed* enums (`offices`/
`niceClasses`/`statuses`) feed. This makes the feature safe to ship without resolving the
ambiguity. **Could not resolve the ambiguity itself this cycle** — this box's direct IP to
`tmdn.org` now gets Akamai-challenged (used to work cleanly per cycle-513 comments), and a
proxied probe script hangs without the Actor's own `AbortSignal.timeout()` guard (got's
`timeout.request` alone doesn't fire on a hung proxy CONNECT) — both recorded in
`notes/LEARNINGS.md` cycle 2406, left open as a LOW-priority follow-up in `queue.md`.
**Verified live, not from the diff**: local run showed the case-correction + unrecognised-value
warning firing; two real Apify platform runs on build 0.1.83 confirmed the filter narrows results
(5/5 `trademarkType:"Word"`, dataset pulled back over the API) and the warning/`RUN_SUMMARY.
unknownTmTypes` path both fire correctly on an unrecognised value. README updated (feature bullet,
input-table row, new FAQ entry, 0-results FAQ cause list, `RUN_SUMMARY` field list, watch-
fingerprint paragraph); `package.json` 0.1.22 -> 0.1.23 (platform build counter 0.1.83 is a
separate, unrelated number per the c2398 lesson — read from the push result, not guessed). No
output-field/registry change needed (`trademarkType` already existed).
`check-pricing`/`check-registry-fields`/`check-readme-samples` all 0 drift. ~$0.01 spent (1 build
+ 2 capped platform runs), 0 new Actors created today, no owner email warranted (no revenue
event, no owner-only blocker).

---
