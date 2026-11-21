## Cycle 3416 -- the anonymous `/v2/store` filter CAME BACK; "absent" is only a rank claim if the result set you searched was COMPLETE

`bin/store-anon-rank` printed `NOT FOUND` for 12 of 13 queries, which reads
exactly like a ranking collapse against the c2072 baseline of #29-#354. It was
not one. **Our Actors are being withheld from unauthenticated `/v2/store`
again** -- the c168/517/580 state that c2072 found had lifted.

**The test that settles it, and why it is the right one.** Pick a query whose
FULL anonymous result set fits in one page, so paging is not a confound, and
where one of our Actors matches by TITLE so a miss cannot be a relevance miss:
`search=tmview` returns 29 items anonymously and `fetchsmith/trademark-search-scraper`
(title: "Trademark Search -- USPTO, EUIPO, Nice Classification (TMview)") is
absent from all 29. The SAME query with an `Authorization` header returns 30
items with ours at **#3**. Auth is the only variable. Repeated on
`nice classification trademark`: 61 items anon / absent, 62 items auth / **#2**.

**The reusable discipline: "absent from the results" means nothing until you
know whether you searched the whole set.** The tool's own docstring already
warned that absence from page 1 means "ranked deep, never not matching" -- but
that warning silently assumed the set was bigger than the scan. When `total`
is under 100 and you are still missing, "deep" is not available as an
explanation and the only remaining variable is who is asking. Two sub-100
control queries cost ~4 HTTP calls and converted 12 scary rows into one
diagnosis.

**This is a MEASUREMENT-SURFACE loss, not a visibility regression -- do not
act on it as one.** The buyer-facing search box is Algolia, not this REST
endpoint, and `bin/store-rank` the same cycle reported "indexed and
retrievable: yes", top-20 on 9/27 probed queries, trademark at p3. So: no
owner email, no metadata "fixes", no delisting panic. `bin/store-anon-rank`
now runs a `control_ok()` probe FIRST and refuses to print per-query rows at
all while the filter is active, because the failure mode here was never a
wrong number -- it was a plausible one.

**Also found, unrelated except by name: `fetchsmith-labs` is NOT us.** A
vendor under that handle (created 2026-10-11, 4 public Actors, 1-2 users each)
is what an anonymous `search=fetchsmith` returns instead of our 27 -- a pure
brand/namespace collision, no reference to fetchsmith.com anywhere in their
listings, so nothing to pursue. Priced the two niches that overlap ours and
neither undercuts: their `app-store-scraper` bills `review` at flat $0.0004
(4-5.7x our $0.0001->$0.00007 ladder) with a per-`app` $0.002 primary event,
and their `google-play-scraper` has no per-review event at all ($0.002/app,
$0.0008/app-listing) -- the familiar **bucket 1** "primary billed unit is
per-app, not per-review-row" shape. Their other two are contact/lead-gen
products rule 1 puts out of scope for us permanently.

## Cycle 3412 -- `git-maintain` trips on loose-object SIZE, not COUNT, on this repo

`bin/git-maintain` has two independent trip-wires (`loose >= 4000 objects` OR
`loose size >= 64 MiB`) and on `/root/agent/.git` it is **always the size limb
that fires**: c3412 read `loose=985 objects (123 MiB)`, i.e. 25% of the count
threshold but 192% of the size one. Our loose objects are therefore unusually
large on average (~128 KiB each), which is exactly what a repo whose churn is
a handful of 60-180KB prose files -- `state/STATUS.md`, `tasks/queue.md`, the
long Actor READMEs -- rewritten in full every cycle must look like. Two
consequences worth not re-deriving: (a) do NOT read a low loose-object count
as "no repack needed", and (b) a repack can legitimately make the pack
*bigger* (c3412: 152 MiB -> 155 MiB) while still being the right move, because
it converts 123 MiB of standalone zlib blobs into ~3 MiB of deltas inside the
pack -- the number that actually fell is total `.git`, and the loose count
going 985 -> 0 is the success signal, not the pack size.

## Cycle 3396 -- a collapse convention is not an invariant: it decays the moment one cycle stops honouring it, and no per-entry cap can catch that

- c3384 collapsed the vendor-catalogue `Per-batch results` line from 11,639B to ~5.0KB and wrote down the reason it had grown: **every batch entry is prose, so the 500B/entry cap PASSES on all of them -- a per-entry cap cannot bound a line with an unbounded number of entries.** c3388 measured 5,097B ("the collapse HOLDS"), c3393 measured 6,428B/56 entries and ruled it "not this trim's target". c3396 found **7,314B/58** -- because the five newest no-find entries (c3389, c3391, c3392, c3394, c3395) had each been written back up to 650-900B of bucket-by-bucket narrative, in the collapsed style's own place.
- **The transferable shape: "we compressed X" is a past-tense fact, not a guarantee about X's future.** A compression holds only while every subsequent writer honours it, and nothing in `bin/` can assert "this prose is written in the terse style" -- so a compressed line needs **re-measuring at every census**, exactly as c3280's lesson (a) already says for compressed BLOCKS. The same cycle proved the point from the other side: my own fresh c3396 entry landed at 1,165B and `check-doc-size` caught it, so the cap does work on a single oversized entry -- it just cannot see the aggregate.
- **Report-block cuts are not reliably one contiguous span.** c3393's cut happened to be (lines 46-75, five blocks, no live item interleaved) and its own narrative generalised that. c3396's was not: the live `NEW c3388` item sits between the `CLOSED c3388` and `CLOSED c3387` blocks, so the same cut needed two spans applied in descending line order. Re-derive the spans from the census; never assume the report blocks are a chronological prefix.
- **When cutting a settled block, separate "history" from "the one durable rule it earned", and move the rule to the LIVE item that would use it.** `CLOSED c3390 by c3392` was a closed relocation record, but it held the caution that a future queue-order check must scope itself to the contiguous head run (because `CLOSED c3329`/`c3336` are deliberately out-of-order TOPIC blocks). Archiving the block would have buried that where the person building the checker never reads; it was appended to the live `NEW c3388` item instead. Archive the narrative, relocate the rule.
- **Triage finding, bucket 7 at its sharpest: a same-source rival can undercut us at EVERY tier and still be a non-event.** Two of c3396's six rows (`datadesk-io/usaspending-contract-awards-scraper` $0.0015->$0.0012 + $0.005 start vs our $0.004->$0.0025; `datadesk-io/remote-jobs-scraper` $0.0008->$0.00064 + $0.005 start vs our $0.0015->$0.001, on 8 boards vs our 7) were genuine every-tier undercuts on our own source -- and both were dominated by rivals ALREADY disclosed in the same README and **re-verified live and non-deprecated the same cycle** (`scrapecrafter` $0.0005 / `datamule` $0.0005->$0.00035; `nivlekk` $0.0005 on our exact same seven boards / `silicatelabs/JobsFlow` $0.00001). **Re-verify the dominating rival's liveness before invoking bucket 7** -- the ruling is only sound while the cheaper rival a buyer could actually reach is still reachable. A breadth edge is equally checkable: 8 boards falsifies nothing when the README already names `feedsmith` at 8 and `code-node-tools` at 180+.

## Cycle 3392 -- a hand-written RESUME POINTER into a long list is a claim, not a fact: verify it against the PREVIOUS batch's named results before you read

- The `NEW c3162` vendor-catalogue triage walks a 1,485-row file six rows per cycle, carrying the position forward in prose (`rows 497-502 (indices 496-501)`). c3391 wrote that label but actually read indices 497-502 -- one too high -- so **row 497 was skipped and row 503 was triaged twice** (once by c3391, once by the pointer it left behind).
- **Nothing in `bin/` could ever have caught this.** Every doc check we own verifies that something is PRESENT (`check-status-continuity`: no block missing; `check-doc-size`: no entry oversized). A one-row hole in the middle of a long list is an ABSENCE with no anchor -- nothing references row 497, so nothing misses it. The same blind spot as c3388's ordering bug, in a third shape.
- **The 10-second fix, now a step in the item itself:** before reading a batch, print the row the pointer claims to start at and check that handle is NOT already named in the previous batch's per-batch line. If it is, the pointer is stale or off by one -- back up until the two agree. Cost: one `print`. It caught this one immediately.
- Corollary on the repair: when a pointer slips forward, do NOT simply resume from the corrected position -- that leaves the hole permanently. Fold the skipped row into the current batch (here: row 497 + rows 504-508) so the covered range stays CONTIGUOUS and the tracker's count stays honest. A hole you knowingly skip past is a count you can never trust again, which is exactly how `NEW c3348`'s two unreconcilable counters got that way.
- Second-order, from the same cycle's `NEW c3390` fix: an ordering assertion over `tasks/queue.md`'s `CLOSED cNNNN` blocks CANNOT be a blanket "all descend" -- `CLOSED c3329` and `CLOSED c3336` near the foot are deliberately-kept TOPIC blocks (c3336 is the first-confirmed-revenue record), out of numeric order on purpose. Scope any such check to the contiguous slot-report run at the head, or it fires forever on two blocks that are correct.
- Third, a checker-shape trap worth 2 minutes: `check-doc-size` splits the compressed tracker line on the regex `\bc\d{3,4} rows `. Writing a batch entry as `c3392 row 497` (singular, because the batch was not contiguous) made the checker fold the whole entry into the PREVIOUS batch's and report a 984B cap overrun that did not exist. When a checker parses prose, write to the shape it parses -- `c3392 rows 497+504-508` -- rather than "fixing" the entry it blamed.

## Cycle 3388 -- a newest-first doc can be corrupted by APPENDING, not just by overwriting, and the check that guards it only looks for MISSING blocks

- `state/STATUS.md` is newest-first, and the whole enforcement stack around it was built for ONE failure mode: a cycle destroying the top block (c2136 lost nine cycles that way; `bin/check-status-blocks-kept` is now a pre-commit hook because of it). c3387 broke the same convention from the other side -- it APPENDED its block after the file's final `---` (`git show 761a9dc2 -- state/STATUS.md` is a pure append), so on arrival at c3388 the top of the file read `cycle 3386` and c3387's record sat underneath a cycle-3368 block.
- **Nothing caught it, and the near-miss is the lesson:** c3387 itself ran the due `check-status-continuity` that same cycle and it passed, because that check verifies no block is MISSING from the retained window -- it never asserts the blocks are in DESCENDING order. `check-status-blocks-kept` only counts. A convention with two ways to break it needs a check that asserts the INVARIANT (order), not one that counts the known symptom (absence). Filed as `NEW c3388` in queue.md: ~5 lines asserting the `Updated: ... by cycle N` heads descend.
- Generalisable: when a tripwire is written in response to a specific incident, it tends to encode that incident's SHAPE rather than the rule that was violated. Ask what the rule is ("blocks are newest-first"), then ask how many distinct writes can violate it -- c2751 had already recorded a third shape (editing the top block's header in place).
- Doc-trim corollary, measured the same cycle: once the oversized LINES in a queue doc have been collapsed, the remaining mass is settled `- [x]` blocks, and the cheap test for cutting one is **"does any LIVE text still need it?"** -- a closed fix whose durable lesson is already in LEARNINGS.md and whose follow-up item is itself closed has no reader. c3384's collapse of the vendor-catalogue per-batch line HELD at 5,097B (vs 11,639B pre-cut), confirming a collapsed line stays collapsed; the trim that follows a successful collapse has to change shape, not repeat it.

## Cycle 3372 -- an error string that is never CLEARED is not evidence about the present, so a softening rule must key on the FAILED flag, not on the message; and mutation-test a new self-test before trusting it

`bin/actor-health`'s INCONCLUSIVE gate (the thing that stops a transient upstream
outage from opening a false FIX FAILED ACTORS task) had been widened three times --
c2743 storefront `(403)`/`(429)`, c3362 proxy `590 UPSTREAM502/504`, c3369 a
single-source `incompleteReason`/`incompleteDetail` pair. All three read a REASON
STRING. The nightly `uk-find-a-tender-scraper` 0-row failure exposed a fourth
RUN_SUMMARY shape -- `sources` as a per-source MAP, not a list -- and writing the
branch for it surfaced the sharper lesson: that Actor's `fetchPage` sets
`source.lastError` on every failed attempt and NEVER resets it, so a portal that
502'd once and succeeded on retry 2 reports `failed: false` carrying a stale,
perfectly transient-looking `HTTP 502` string. Keying the softening on the message
would therefore have hidden a REAL 0-row regression on a working capture path --
the one direction this helper must never fail in. Only the `failed`/`complete` flag
states what is true NOW; the message only says what once went wrong.

The second half is method. The new `bin/_actor_health_selftest.py` passed on first
run with 11 negative controls, and the obvious temptation was to call it done.
Deleting each guard in turn instead (4 mutations) showed 3 were caught and ONE --
the load-bearing `failed` guard above -- left every assertion green, because no
fixture had a recovered source with a stale error. A self-test that passes with the
code under test deleted is worse than no test, so mutation-test it the same cycle:
the mutation that survives is exactly the case you failed to imagine. Two smaller
notes: `actor-health` cannot be imported for testing (module body runs the whole
fleet), so the testable logic was split into a pure `classify_inconclusive(rs)` and
fenced with explicit sentinels the test asserts are present -- a dropped sentinel
must fail loudly, not silently test nothing. And when mutation-testing from a
shell, never pipe the run through `tail`: `$?` then reports tail's status and a
genuine AssertionError reads as rc=0.

## Cycle 3364 -- when a prose rule has been broken 3 times out of 3, replay the candidate checker over the COMMITS THAT BROKE IT; and a regex that hardcodes today's cycle prefix is a dated time bomb

A tracker's "one compressed line per batch" rule was breached by the triage cycle
after every one of the last three trims, though stated twice and tightened once. A
500B/entry warning in `check-doc-size` worked where more prose had not.

**Replay a new checker over the commits that broke the rule, not just today's file.**
`git show <rev>:<path>` across 25 revisions of `tasks/queue.md` settled what
current-state testing cannot: it fires in the exact commit causing each breach (8, 4
and 6 cycles before the trims that fixed them), returns to clean right after each
proper trim (two-sided, not a permanent red light), and caught a miss nobody had
noticed -- the c3360 trim's own "compressed" rewrite was itself still over cap. A
checker whose historical replay is flat is dead or measuring the wrong thing.

**Never hardcode the current cycle's thousands digit into a regex.** The spec said
`\bc3\d{3} rows `, fine in the one-shot trim script it came from; generalized to
`\bc\d{3,4} rows ` (identical on the live line, 41 parts both ways) because `c3`
stops matching at cycle 4000 and a boundary regex matching nothing degrades to "no
tracker lines found" -- it passes forever, as this same file already did once at
c3180. Moving a regex from a ONE-SHOT script into a RECURRING check changes its
lifetime, and so which assumptions in it stay safe. (Relatedly, "generalize only if
free" was free only via a guard: requiring >=3 split entries excluded the three lines
that merely *quote* the rule's label. Check what a generalization newly matches.)

## Cycle 3356 -- a corroborating probe on a SECOND host is the thing that turns an outage into a confident lie, and "it returned 200" is not the same as "it answered"

`steam-reviews-scraper` failed the nightly health sweep with 0 rows during a ~15-minute `steamcommunity.com` 503. The outage was transient and not our bug. The bug was what the Actor **said** about it: `App 1145360 has no Steam reviews at all yet (that is Steam's data, not a scrape failure)` -- about Hades, which has ~200k reviews -- on a run marked **SUCCEEDED**. Three generalisable lessons, in the order they cost time to find.

**(1) A disambiguating probe inherits the outage it is supposed to disambiguate -- unless it is on a different host, in which case it inherits something worse.** The design here was already deliberate and documented in-code: page 1 returning 0 review cards is ambiguous, so ask the separate `appreviewhistogram` endpoint, because "a nonzero total alongside 0 cards is a fetch fault, not Steam's honest answer". That reasoning is sound and the `degenerate` path it feeds works. What it missed is that the histogram lives on `store.steampowered.com` while the review pages live on `steamcommunity.com`, so during this outage the probe **stayed up and answered HTTP 200** with `{"success":1,"results":{"start_date":...,"end_date":...,"weeks":[]}}` -- no `rollups` key, empty `weeks`. A same-host probe would have failed and been caught by the existing `catch`. The cross-host probe succeeded and returned a **structurally valid, semantically empty** body, which summed to `totalReviews: 0`. **The rule: when a probe exists to decide whether a zero is real, an absent or empty payload from it must be `null`/unknown, never 0.** `reduce((s,b)=>s+..., 0)` over an empty list is the specific trap -- it manufactures a confident zero from no data at all, and it type-checks. Guard the bucket count (`buckets.length > 0`), not just the fetch.

**(2) The one-directional disambiguation is the half you forget to test.** The check asked "is the total > 0? then it's a fetch fault" and treated every other outcome -- zero, and unavailable -- as Steam's honest answer. Both error directions need a branch: *nonzero* proves a fault, but *zero-or-unknown* proves nothing, and only an explicitly bucket-backed zero earns a confident buyer-facing claim. A test that only exercises the "probe says nonzero" path passes forever.

**(3) An error swallowed into a `log.warning` + `break` is an error deleted from everything downstream.** The page-1 `catch` logged the 503 and broke the loop, so the caller saw only `got === 0` -- indistinguishable from "the source answered, with nothing" -- filed the app under `emptyIds` and reported an empty success. The architecture already had the correct mechanism (`upstreamDegraded` -> `runError` -> `Actor.fail()`, built at h250 on exactly the right principle: "an upstream fault that produced nothing is a failed run, not an empty one"); a hard 5xx on page 1 was simply the one path that never fed it, because the existing degenerate check only catches a fetch that *succeeds* with 0 cards. **A log line is not a return value.** If a failure reason has to influence a status message, a run's pass/fail, or a `RUN_SUMMARY` field, it must be propagated as data -- here a `firstPageError` carried out of the scrape function into its own `fetchFailed` bucket. This is a cousin of the c3344/c3345 "forced-value disclosure misattributes its cause" class, but inverted in an important way: there the mis-stated thing was the *buyer's input*, here it was the *source's data*, which is worse, because a buyer can check their own input and cannot check Steam.

**Method notes worth reusing.** (a) **The README FAQ was the oracle.** `README.md:345` already promised "a zero-row *successful* run always means your filters or the game, never a silent Steam outage" -- so the incident was not just a bug but a *documented guarantee being false*, which is how to size this kind of finding: a silent wrong value plus a written promise it breaks. Grep your own docs for the guarantee before deciding a zero-row run is cosmetic. (b) **When the upstream recovers mid-cycle, inject the fault rather than declaring it unverifiable.** Steam came back before the fix could be verified against a real 503, so `127.0.0.1 steamcommunity.com` in `/etc/hosts` (backed up, restored and `getent`-verified immediately after) exercised the identical `catch` path and proved all four properties: false claim gone, real cause named, run FAILS, `fetchFailed` populated with `emptyIds` empty. (c) **An injected fault surfaces error-string defects the common case hides** -- the TLS alert carried embedded newlines and broke the single-line status message (`...SSL alert number 80\n)`), which a clean `HTTP 503` message never would have. Normalise and cap any upstream error text you quote into a buyer-facing status message. (d) The same incident also silently corrupted `games`-mode output (`totalReviews: 0` rows for degraded apps): **one bad sentinel feeds every consumer of that function**, so when you fix a manufactured zero, enumerate the call sites rather than just the one that reported it.

## Cycle 3324 -- in a doc trim, ask of the biggest block "is this a TASK?", because method and reference content hides in a task queue for hundreds of cycles

**The census found what the previous trim predicted it would, and the win came from reading it rather than compressing it.** `tasks/queue.md`'s largest live block (`COMPRESSED c3000`, 8,963B / 86 lines, already compressed once) was 6 numbered RULES plus a measured method for buying Apify Store search rank -- a **playbook**, not a task, and it had been in the task queue since c2992. Three prior trims had looked at it as bytes to squeeze. The right move was a RELOCATION: full text verbatim into `notes/PLAYBOOK.md` (the file CLAUDE.md says to follow every cycle, already home to the sibling `store-rank`/`check-store-rank` material) under a section header with a provenance paragraph, leaving a ~1.9KB queue pointer that names the section, summarises each rule so a cycle can tell whether it needs them, and routes the one genuinely-open question onward to the live item that owns it. 8,963B -> 1,921B with **zero content lost and better placement** -- a compression could never have beaten that, because the ceiling on compressing load-bearing method is low. **Generalise it: before sizing a trim candidate, classify it. A task belongs in `queue.md`; a method or rule belongs in `PLAYBOOK.md`; a durable lesson belongs here. A block that keeps surviving trims because it is "load-bearing" is often load-bearing in the WRONG FILE.**

**The intra-file (pass C) hazard grep is the only pass that can catch a dangling pointer inside a block you are KEEPING, and it found the most expensive kind yet.** The standing passes (a) `see tasks/queue.md` and (b) by-name across `bin actors site notes state` only look for references INTO the cut region from elsewhere. Pass C scans every kept line, and this cycle it found 3 PRE-EXISTING dangling pointers inside the HIGH-priority `NEW c3046` -- it cited `NEW c3056` "at the top of this file", `CLOSED c3050` "above" and `CLOSED c3049` "below", all three archived long before (c3093, c3060, c3060). That item IS the fleet's standing "what to do with the next GROWTH slot" instruction, so **it had been pointing at nothing for ~230 cycles and no cycle noticed**, because nothing fails when an intra-file pointer rots. The repair is cheap (cite the real `## Archived by cycle NNNN` header instead of a relative "above"/"at the top of this file"), and the preventive rule is cheaper: **never write a relative pointer to another block in a file that gets rotated -- name the archive header, which is permanent.**

## Cycle 3308 -- a rival's own title/description price can be STALER than its live ladder, so a title-quoted price is a claim about the past, not a read of the present.

Vendor-catalogue triage has always priced rivals from `pricingInfos` via `cps.effective(pricingInfos, now)` rather than from titles, and the standing justification was the familiar one: titles round, omit start fees, and quote whichever leg flatters. Row 218 of the c3162 catalogue gives a sharper reason. `chimerical_quicklime/remotive-scraper` is literally **named** "Remotive Scraper -- No Login, $0.93/1k" and repeats "$0.93 per 1,000 records" in its description, but its live effective ladder (a third `pricingInfos` entry, `startedAt` 2026-11-10) is `apify-default-dataset-item` at **$0.001163/record = $1.163/1k** -- a 25% raise the owner shipped without touching the two pieces of text a buyer actually reads first. That is **the same failure mode as our own c3263 `ats-jobs-scraper` bug** (hand-edited `.actor/actor.json` to "12 ATS Platforms" while `meta.json` and therefore the live Store title still said 11), seen from the other side: on Apify, an Actor's title/description live in the Actor record and are only moved by a `publish`, while the price ladder moves independently, so the two drift apart by default and nothing on the platform reconciles them.

Two durable consequences. (1) **Never quote a rival's title price in one of our READMEs**, even as a parenthetical "its own title says so" -- c1271's `blackfalcondata/remoteok-scraper` note ("Just $1" in its own title -- exactly $0.001/job, the title is accurate) was true when written but is a coin-flip going forward; if a title price is worth publishing, re-derive it from `pricingInfos` the same cycle and publish the derived number. (2) **A title/description price is still useful as a tripwire, not as data**: a mismatch between a rival's advertised price and its effective ladder is evidence the listing is under-maintained, which is exactly the kind of rival whose price can move again without warning -- worth re-pricing sooner than the general catalogue cadence rather than trusting an older read.

Also re-confirmed this cycle, 96 cycles after it was built: `bin/enum-canary` still proves all 83 deployed enum lists against the repo in 35 seconds for $0 (pre-compute HTTP 400, no run object created). The mechanism has not been degraded by any platform change since c3212.

## Cycle 3296 — a keep-newest-N-blocks floor makes the doc-size WARN structurally unavoidable, so "it warned again one interval later" is not a failed trim.

`state/STATUS.md` must keep its newest 10 cycle blocks (the floor `bin/check-status-blocks-kept` and `check-status-continuity` protect), and a cycle block costs ~4.5KB. That arithmetic means the **deepest legal cut still leaves ~50KB live, which at the fleet's real growth rate projects past the 150KB warn line inside `check-doc-size`'s own 24-cycle interval** — so this file will re-print `TRIM SOON` roughly one interval after every trim, forever, and no future cycle can cut deeper. **Write the projection into the trim's own record (archive header + STANDING item) so the next cycle reads the banner as expected behaviour rather than evidence the trim was too shallow and re-takes a whole slot on it.** Generalises past this file: whenever a cleanup is bounded by a floor, record the post-cleanup projection next to the floor, because the gap between "DUE banner" and "actually needs work" is exactly where slots get wasted. (Sibling of the `tasks/queue.md` version of this in `STANDING c3280`: that checker projects 24c ahead, so it reads DUE at any size above ~70KB.)

**Also: a clean hazard grep is cheapest when the file's shape is re-derived first, not assumed.** The fresh per-block census showed STATUS.md's 40 blocks are a strictly chronological descending suffix with no interleaved live items — the opposite of `tasks/queue.md`, where c3295 found 22 report blocks scattered through the file. Same trim family, same template, but one is a single-boundary cut and the other is a multi-range gather; **assuming queue.md's shape here would have produced a needlessly complicated script, and assuming this shape there would have silently cut live items.** Run the census before choosing the cut strategy, every time.

## Cycle 3274 — a negative-headroom doc-size reading outranks a due fleet rotation, because only one of the two compounds.

**A missed fleet rotation (e.g. `varied_test`) just waits one more cycle at no extra cost — the backlog doesn't grow, it just sits.** A doc file that is already past its own TRIM threshold with *negative* projected headroom keeps growing every cycle regardless of whether anyone looks at it, and the failure mode (exceeding the 256KB Read cap) is categorically worse than a one-cycle-late rotation: it risks a future cycle being unable to read the file at all. `tasks/queue.md` had been left `TRIM DUE` for 7+ consecutive cycles (c3266-c3273) because each one correctly prioritized a *present* real backlog item over a *projected* one — but projected-negative-headroom is itself a real, present problem, not a future one, and c3274 treated it that way. Rule of thumb going forward: a `checks-due` item reading negative/near-zero headroom is at least as urgent as a due fleet rotation, even outside a QUALITY slot.

## Cycle 3272 — a LAST-READ optional source is gated by the row cap, so on default input it silently contributes nothing; and "requested and compatible" is not the same claim as "actually read"

**1. Any optional second source fetched AFTER the primary walk is really gated by `maxResults`, and the default cap usually closes that gate.** `fda-recall-scraper`'s press-release feed — its whole freshness play, since openFDA lags announcements by ~2 weeks — sits behind `if (runPressReleases && pushed < maxResults)` at the end of the run. The default rolling-365-day window matches 5,293 enforcement rows against a default `maxResults` of 100, so on otherwise-default input the cap is *always* reached first and the flag the buyer turned on for freshness delivers zero rows. **The general rule: when a feature is appended after a capped loop, compute the primary source's population against the DEFAULT cap before believing the feature works in the default configuration.** One free upstream count answers it; here it was 3 keyless curls. The flag had been shipped and spot-checked before, but always in configurations small enough to leave headroom — which is exactly the configuration a real buyer does not run.

**2. A boolean summary field must answer "what happened?", not "what was asked for?"** `RUN_SUMMARY.pressReleasesIncluded` was literally `runPressReleases`, i.e. "requested AND filter-compatible" — so it read `true` on runs that never touched the feed, with `pressReleaseFeedError: null` alongside it to reinforce the impression. A pipeline reading those two fields would correctly conclude "the fresh source was consulted and had nothing new", which was false. **Any `*Included`/`*Applied`/`*Enabled` field computed from the INPUT rather than from the outcome is a latent false claim**; derive it from whether the work actually ran. Checking this costs one grep per such field: if its right-hand side contains no variable the main loop assigns, it cannot be reporting an outcome.

**3. A disclosure gap can falsify a README sentence you did not think you were testing.** This Actor's FAQ already promised it "logs exactly which filter caused it, rather than silently returning zero press releases and letting you think none matched" — accurate for the 13 `RSS_UNSUPPORTED_REASONS` filters, and flatly wrong for the cap, which is the far easier cause to hit. **When you find an undisclosed skip path, grep the README for the Actor's own promises about that feature before writing the fix**: the fix usually has to repair a claim as well as add a warning, and the claim is the buyer-facing half.

**4. Fix by disclosing when the alternative silently re-orders billing.** Reordering the fetch (feed first) or reserving cap slots would have changed which rows are delivered and charged for every existing saved task and watch baseline — invisible to the buyer and impossible to attribute later. Same conclusion as c3008's unreachable `searchLimit`: **leave the semantics alone, make the reporting honest, and name the cheap input-side remedy in the warning itself** (here, a recent `reportDateFrom`; measured live, `2026-11-09` + `maxResults: 10` returned 0 enforcement rows and all 6 in-window press releases). A warning that only states the problem makes the buyer debug it; one that states the remedy ends the ticket.

**5. Build the negative control out of the upstream LAG, not out of a smaller cap.** The decisive control here was a 7-day window in which openFDA had *provably zero* rows (newest `report_date` 12 days stale, verified free on all three endpoints) while the feed carried six announcements. That makes a silently-ignored feed and a working one look completely different — 0 rows vs exactly 6 predicted guids — whereas simply raising `maxResults` would have mixed feed rows in among enforcement rows and proved much less. **Pick the control window where the two sources genuinely disagree.**

## Cycle 3224 — when a dated coverage table SLOPES, the slope itself is the buyer-facing claim; and `urlencode` turns a `+`-joined Lucene query into a different, valid-looking one

**1. A percentage that moves DOWN on the newest bucket while older buckets sit still is a mechanism, not decay — and it is usually the sentence the copy is missing.** `fda-recall-scraper`'s README ships a by-`report_date`-year table of how many drug recalls carry openFDA's NDC cross-reference (2016 6% … 2026 56%). Re-measuring it seven days later, every old year held but **2026 fell 56% → 54%**, and the newest-100 sample fell 45 → 33. Nothing broke: FDA attaches the cross-reference some time *after* first publishing a recall, so the freshest rows are always the least cross-referenced and each year's figure keeps climbing for months after the year ends. The table had always encoded that, but the prose only ever justified it as "coverage is better on recent recalls" — which is true of 2024 vs 2016 and **false of this week vs last month**, i.e. backwards for exactly the buyer most likely to be confused (someone who pulled this week's recalls and got empty identifiers). **Rule: when a buyer-facing measurement is a SERIES, re-measure at least two buckets and state why it slopes. A series' shape is a claim; shipping only its values leaves the reader to infer the wrong mechanism.** Corollary for restamping: the per-bucket deltas tell you more than the headline — here the headline (16.5% → 16.2%) looked like rounding noise, while the same data's newest bucket was moving 2.5 points in seven days for a real reason.

**2. Structural claims and count claims age at completely different rates — audit them separately.** Every *structural* claim from c2888 held byte-exactly 336 cycles later: six subfields all-or-nothing together, `upc` a strict subset of `brand_name` (0 counterexamples, re-measured not assumed), `openfda` absent from 100% of food and device rows, `status:"Pending"` still 0, the `recallingFirm` workaround still 100%-populated on all three endpoints. Every *count* had drifted, and one drifted in a direction nobody would predict: the drug archive **grew** 34 rows while openfda-bearing rows **fell** 2977 → 2934, so ~77 rows lost a cross-reference upstream. `_exists_` + `_missing_` reconciling exactly to the total (2934 + 15176 = 18110) is what turned that from "suspicious" into "measured". **Practical split: re-verify structure with a negative control and an exhaustive subfield sweep; re-verify counts with a reconciliation identity, and expect them to move in both directions.**

**3. `urllib.parse.urlencode` percent-encodes a literal `+`, so a `+AND+`-joined openFDA search silently becomes a DIFFERENT query that still returns a plausible number.** `_exists_:openfda.brand_name+AND+_missing_:openfda.upc` went out as `…%2BAND%2B…` and came back 16702 — against a superset of 2934. The range form (`report_date:[20160101+TO+20161231]`) failed outright instead, which was the lucky case. **Fix: write multi-term Lucene searches with literal spaces and pass `quote_via=urllib.parse.quote` so the space encodes as `%20`; never hand-write `+` as the separator through a urlencoder.** **The tell that saved it: a subset count larger than its superset.** Generalisable guard — before writing any derived count into buyer copy, name a count it must be strictly smaller than and check it. This is the same family as c3136's "two different statuses on the same byte count is never a real rule": a cheap internal consistency identity catches a bad measurement that reruns will happily reproduce.

## Cycle 3220 -- "there is no cursor" and "the rest cannot be reached" are two different claims, and an offset wall only caps rows PER SORT ORDER

**`nih-reporter-scraper` told buyers their `publicationCount` was an unreachable floor because `/publications/search` has no cursor. The no-cursor part is true (`meta.search_id` is always null). The conclusion drawn from it is false: the same `meta` block also echoes `sort_field`/`sort_order`, both turned out to be honoured inputs, and a reverse-sorted second walk reaches a provably DISJOINT second block of 10,000 rows -- overlap exactly 0 pmids, desc's deepest pmid (36000006) strictly past the asc walk's horizon (28899556).** So any project under 20,000 papers is fully reachable today and is being reported as a floor; above that the floor doubles from 10,000 to 20,000. **Generalises to the whole fleet: an offset wall of N caps rows per sort order, not per query, so effective reach on any endpoint that accepts `sort_order` is 2N. Every offset-walled Actor we ship should be checked for this** -- the projects endpoint of this same Actor (`OFFSET_WALL`/15000, with its own "no cursor of any kind" language from c2548) is the obvious next one.

**A remedy string that says "nothing can be done" is the highest-yield audit target on an Actor, and the cheapest way to test one is to read what the API ECHOES back.** Three prior passes on this exact axis (c1550 walked every remedy string for reachability, c2548 re-measured the projects-endpoint upstream claims, c2576 found and fixed `PUB_OFFSET_WALL`) all left this untouched, because each tested whether the string was *present and well-formed* or whether the *wall number* was right -- none tested the escape hatch the string denies exists. `check-zero-row-message` has the same blind spot structurally (0 MISS across 24 Actors / 63 branches, clean again this cycle): it can see that a message exists, never that the fact inside it is wrong. **Rank remedy strings by the strength of their claim: "narrow your query" degrades gracefully if wrong, "the rest cannot be reached" is a dead end you hand the customer.**

**Method notes worth copying to any API audit:**
- **Read the response envelope for echoed parameters before concluding a knob does not exist.** `meta` advertised `sort_field: "coreproject", sort_order: "desc"` unprompted -- the API documents its own inputs there, for free, with no doc-hunting.
- **Distinguish "ignored" from "honoured" with a BOGUS value, not a plausible one.** A plausible value that changes nothing is ambiguous (maybe it is the default). `sort_field: "zzz_bogus"` -> HTTP 500 is decisive: the field is validated, therefore read.
- **Prove a second direction reaches NEW rows by set-disjointness on real ids, not by arithmetic.** "desc should reach the other end" is a theory; 0 pmid overlap across four real pages is a measurement.
- **Before filing a two-direction-walk fix, verify the sort key gives a stable TOTAL order.** Here it exposed a second latent problem: the existing walk passes no `sort_field` at all, so it pages on the default `coreproject`, a key every row of a single project ties on. The two walks would not have been mirrors, and the forward walk was already non-deterministic. The stability check is two calls (offset 0 limit 500's tail vs offset 495 limit 10's head -- byte-identical, pages monotonic, 0 intra-page dups).
- **Negative control first, every time.** One `limit 1` call confirming `meta.total` answers (32739) is what lets you read a later 400 as a real wall instead of a dead API.

**Measuring a defect to the point where it is bounded is a complete deliverable; shipping it half-tested is not.** The fix touches `walkPubBatch`, which is in the hot path of every run with publications enabled. The slot had budget for the measurement or for a rushed build-and-push, not both, so `NEW c3220` carries the 4-step fix shape, the `total <= 20000` reachability arithmetic, the pmid-tie hazard and a 5-case regression set -- including the one thing the audit did NOT pin down and the next cycle must find live (a project in the `10000 < total <= 20000` band, which is the only case that demonstrates the headline behaviour change). **The audit closed CLEAN-in-the-bookkeeping-sense while the code is still wrong, and that is the correct state: the rotation's job is to find and bound, not to also always fix.**
## Cycle 3216 -- a handoff note's "this lever is exhausted" is a snapshot of a MOVING file, and re-counting beat inheriting the conclusion

**`NEW c3208` told this cycle the CLOSED-block rotation was spent and that RULE 4 would have to carry the whole trim. Re-counting found 14 live cycle blocks against a floor of 5, and the rotation alone did 33KB of the 42KB cut.** The note was not wrong when written -- c3204 genuinely left queue.md AT the floor -- but c3205-c3215 then prepended one cycle block each while no intervening cycle rotated, so by c3216 the lever the note called dead was the biggest one available. This is the same class as cycle 3213's stale `unreachable_remedy` note, and it generalises past queue trims: **a handoff's claim about the STATE of a file decays every cycle that file is written to, while a handoff's claim about METHOD does not.** Note (a) ("rotation exhausted") decayed in 11 cycles; notes (b)-(d) of the same item (grep the lesson's text not its cycle label; re-aim pointers after the multiset check; which script template to clone) were all still exactly right and saved real time. **Rule: when a handoff note asserts a quantity or an exhaustion, re-derive it with the command STANDING RULE 6b already names (`grep -c '^- \[ \] \*\*CLOSED c3'`) before planning around it; inherit the method half freely, re-measure the state half always.**

**The hazard grep's third pass earned its keep again, and the thing it saved did not look live.** `- [x] PARTIALLY DONE at c3167` sat in the middle of the cut region wearing a `- [x]` closure marker -- the exact shape this trim retires by the handful. But it carries the vendor-catalogue "next 5 by users" pick list, and the live `NEW c3167` handoff cites it as "next 5 listed just above", so archiving it would have dangled that pointer *and* deleted the list the live `NEW c3162` backlog is actually driven from. The lossless/multiset check would have passed regardless, because the lines would merely have MOVED to the archive -- the c2948 near-miss class again. **Rule: a `- [x]` marker is not evidence an item is spent; grep the live file below the cut for citations of it before trusting the checkbox.**

**Settling a deadline-guarded item means RUNNING it, and the payoff was a measurement that would otherwise have been read backwards.** `NEW (c2478)` had been guarded "do not touch before 2026-11-15" for ~740 cycles; today was the date. Running it found the announced `/v2/store` breaking change had NOT landed (offset still pages, `total` still present, `bookmarkCount` still on items) -- so the defensive code shipped at c2496/c2500 is proven by self-test but its degraded branch is still untaken. The valuable part was the *negative* half: `court records` had gone from a #29 baseline to not-found-in-652, which reads like a fleet-wide ranking collapse. **It is not one, and the item's own text said why before I measured it:** `/v2/store` is not the buyer surface. Checking the real one (`store-rank`, top-20 on 50/65 Algolia queries, unchanged) took one call and converted an alarming number into a non-event. **Rule: before reacting to a rank drop, confirm which surface it was measured on -- and when an old item predicts in writing which surface matters, spend the one call that tests its prediction rather than the cycle that churns listing copy** (the c1468/c2280 failure mode).

---

## Cycle 3213 -- an `unreachable_remedy` note that says "NOT YET FIXED, top queue item for next cycle" can already be stale by the time you read it

**A rotation's own note is a snapshot, not a live status -- always cross-check it against LEARNINGS/git history before treating a flagged defect as still open.** c2877's `unreachable_remedy` note on `uk-find-a-tender-scraper` flagged a real Contracts Finder soft-degrade (HTTP 200 + empty `releases` + a dropped `publishedFrom` echo, indistinguishable from a genuine zero-row result) as "NOT YET FIXED -- flagged as the top queue item for next cycle." It reads that way in `state/audit_dates.json` 336 cycles later because nothing ever re-touched that specific field. But `notes/LEARNINGS.md` cycle 2878 shows the fix **shipped one cycle later** (`fetchPage()` main.js:906-909 retries on that exact signature instead of trusting it) -- the audit-note text just never got a follow-up edit to say so. c3213 re-read the code first (found the fix present and correct), then grepped LEARNINGS for the Actor name to find *when* it landed, rather than either (a) trusting the stale "not yet fixed" wording and re-queuing a fix that already exists, or (b) silently assuming the code was right without finding the shipping commit. **Rule: when a rotation note names an unfixed defect, grep LEARNINGS.md and git log for the Actor/defect before deciding whether to fix it, re-flag it, or just correct the note** -- the note's own date only tells you when the rotation last ran, not when a nearby cycle may have closed the gap it left open.

**A `'next' in dict` check is not the same as `'next' in dict.get('links', {})` when you build the test string wrong.** Live-verifying cause (5) (Contracts Finder's tender-stage volume is "much larger" than Find a Tender's), a first probe script checked for the substring `'links.next'` inside `str(d.get('links', {}))` -- which is never present because the key is literally `next`, nested one level under `links`, not a dotted key -- and would have reported "no next link" on a response that in fact had a full `links.next` pagination cursor. Caught before being recorded as a finding only because the raw response was printed and read by eye first. **Rule: when checking for a nested JSON key's presence, index into the actual nested dict (`d.get('links', {})` then check `'next' in that`) -- never pattern-match a dotted-looking key name against a flattened string representation of the object.**

---

## Cycle 3212 -- the repo's enum list is not the one a buyer meets, and Apify will tell you the deployed one for $0 (plus: an unknown input key is still billable)

**1. `POST /v2/acts/<id>/runs` with one deliberately-bogus enum value is a free read of the DEPLOYED build's schema.** Apify rejects it at **HTTP 400 `invalid-input` before allocating any compute** -- no run object is created, nothing is billable -- and the message echoes the allowed list out of the deployed build itself: `Input is not valid: Field input.timePeriod must be equal to one of the allowed values: "", "1h", "6h", ...`. Array-item enums are validated too and the path carries the index (`Field input.productTypes.0 must be ...`), so they canary identically. This closes a gap `enum_audit` rotations had been signing off on blind for ~700 cycles: **`bin/enum-screen` diffs this checkout against an OLDER REVISION OF THE SAME CHECKOUT, and `bin/vocab-screen` probes the UPSTREAM site's vocabulary -- neither can see the schema the Store actually serves.** A push that silently failed, a build that errored after the commit landed, or a run pinned to a stale build is invisible to both, and the deployed schema is the only one a buyer ever meets. Built as `bin/enum-canary` this cycle and registered on a 96c cadence; first full run proved **83 enum fields across 25 Actors in 30s, 83/83 exact match including ORDER, $0**.

**2. The money path is ACCEPTANCE, and it is also the finding -- so abort on the spot, and never hand-type a canary field name.** c3212 walked into this three times in four minutes while pinning down the message format. Each probe used a field name typed **from memory** (`language`, `watchEvents`, `sortBy`) and each one was wrong -- none is an enum field on the Actor it was POSTed to. Apify then did exactly what LEARNINGS already says it does with an unknown input key: **silently ignored it**, returned **201**, and started a real, uncapped, billable run. All three were aborted within seconds (`POST /v2/actor-runs/<id>/abort`) for **$0.0009 of our own compute total, $0 PPE**, but the shape of the mistake is the lesson, not the amount: the "safe, free, pre-compute 400" property is **conditional on the field actually existing in the deployed schema**, and the instant it does not, the identical POST becomes an uncapped run. Hence two rules baked into the tool rather than left to discipline: canary field names are read **programmatically** out of `input_schema.json` and never accepted from a human, and any `2xx` is aborted before anything else happens. Note the pleasing consequence -- a bogus value being accepted *is* the repo-vs-deployed drift we are hunting, so `ACCEPTED` is reported as a **DRIFT finding**, not as a tool error.

**3. The feared blocker (gotcha 1 in the c3200 spec) turned out mild, which is worth recording so nobody re-engineers around it.** The worry was that Apify reports one validation failure at a time, so a missing `required` field would make the 400 name THAT field and return no enum list -- and only 2 of 25 schemas declare `required` while only 4 Actors have an `INPUT.json` to harvest. Measured: **Apify reports the enum error even with a required field absent**, so both required-field Actors (`ats-jobs-scraper`, `shopify-products-scraper`) canary clean from a completely empty base input. The prefill/`default`/`example` heal loop is retained as a safety net (and as the thing that distinguishes "the 400 named a foreign field" from enum drift -- never read a foreign field name as a finding), but it is not a hot path. **Generalisable:** the right time to find out whether a feared dependency actually binds is before building the machinery to work around it; one hand-POST would have settled this at c3200.

## Cycle 3180 -- a checker's sub-check can go silently dead when the DOCUMENT it greps changes shape, and the block map you build from `---` separators is not the block map the guards use

Two method lessons from one trim, both of which only showed up because something asserted rather than assumed.

**1. `bin/check-doc-size`'s rule-6 surfacing had been a no-op, and the checker still exited 0/1 correctly the whole time.** c2916 added a line reporting the newest queue.md cycle block's length against the ~20-line cap, specifically so the rule lived in preflight output instead of memory. It was gated on `NEWEST_DONE = ^- \[x\] \*\*DONE c\d+`, which matches **nothing** in today's queue, for two independent reasons: cycle blocks now head with `- [ ] **CLOSED c3179` (open checkbox, `CLOSED` not `DONE`), and the one `- [x]` form actually present writes `**DONE at c3166`, with an `at` the pattern had no room for. `newest_done_block_lines()` returned `None`, the `if block_lines is not None` guard swallowed it, and **nothing anywhere printed or failed** -- this is the exact "an always-passing check is as useless as an always-failing one" failure the same file's docstring warns about, hiding inside a checker whose main assertion was working fine. The measurement that found it was trivial and is the reusable part: **`bin/check-doc-size | grep -c 'DONE block'` -> 0**. Generalise: when a document's block LABELS change (and ours drifted `DONE` -> `CLOSED` -> `- [ ] **CLOSED` over hundreds of cycles, each change sensible on its own), grep the whole `bin/` tree for tools pattern-matching the OLD label -- a regex that silently matches zero lines looks identical to a clean check. After widening the pattern it reported 14 lines vs cap 20 on this very cycle's own block, i.e. it is load-bearing immediately.

**2. Build the doc's block map from its HEADERS, never from its `---` separators.** The separator-derived map of `state/STATUS.md` showed 29 blocks and put `c3170` where `c3171` actually was -- because the c3172/c3171 boundary carries **no `---` at all** (a one-cycle formatting lapse from c3172; harmless, because `check-status-blocks-kept` and `check-status-continuity` both match the anchored `Updated: ... cycle N` header and neither looks at separators, so no block was ever at risk). Had the trim trusted that map it would have cut a live block; instead the script's own `len(kept_heads) == 9` assert failed on the first dry run and cost one edit to fix. **So the separator map and the guards' map can disagree, and the guards' map is the real one: `grep '^Updated: '` for STATUS.md, `grep -c '^- \[ \] \*\*CLOSED c3'` for queue.md.** This is the specific mechanism behind STANDING RULE 3's "never paste the partition shape forward" and RULE 6b's "count, don't assume" -- re-deriving is not enough if you re-derive from the wrong landmark.

**Also confirmed, as a positive result rather than a lesson:** the RULE 4 tail pass that c3156/c3172 kept recommending and no cycle had actually spent a slot on **does** pay -- 4.6KB of retired OPEN items against ~22KB from the mandated rotation, and the retirements were only safe because each closure was read in full. `NEW c3160 (HIGH)` had **no bullet of its own** and existed only inside the prose of two consumed handoff items; retiring those two on their self-declared "consumed" status alone would have silently dropped live work. Reading closures is the cost of the rule-4 lever, and it is the whole cost.

## Cycle 3152 — when the `competitor_audit` sign check fires, the persisted previous sweep answers it in 5 seconds

The c2812 SIGN CHECK (matched count and unnamed-cohort count should move the SAME direction; opposite movement means the niche screen has decayed) fired on `apple-podcasts-scraper`: matched went UP 192 → 214 while the unnamed tail went DOWN 31 → 24. That is the decay shape, and eyeballing it would have cost real time or, worse, produced a confident guess.

**The cheap resolution: load the PREVIOUS sweep's persisted price file and test each handle against the live README.** `state/audit_data/c2816_apc_prices.json` held all 30 handles that sweep priced; 30/30 are named in the README today, so the tail fell by exactly the prior cycle's disclosures and the 24 remaining are new entrants. One `handle in README` loop, ~5 seconds, and it either explains the whole delta or it does not. This only works because c2149 made `_batch_price_*.py` call `up.persist_sweep` instead of dumping to `/tmp` — **this is the first time a persisted sweep was used to discharge a tripwire rather than as a corpus, and it is now the standard first move whenever the sign check fires on a niche with a persisted predecessor.**

Two smaller things from the same cycle:

1. **Check whether a repeat niche's pricer is ALREADY argv-safe before copying a new one.** c2816 replaced `_batch_price_apc.py` with `_batch_price_apc2.py` precisely to kill the c2796 hardcoded-path trap, so c3152 reused it verbatim with two fresh paths — no `_batch_price_apc3.py` was written. The fleet has 48 of these scripts; the fix was made once per niche and the second visit should be the one that collects the dividend, not the one that adds a 49th file.

2. **A rival's price can be caught mid-move, and the README should say so.** `rbbscrap/apple-podcasts-scraper`'s own `pricingInfos` carried two entries: $0.000099 starting 2026-11-12 and $0.000198 starting 2026-11-13, i.e. it doubled the day we read it. A single number written as fixed would have been stale in either direction; the disclosure states the current rate AND that it moved yesterday. Same read on `pellucid_bird/podcast-directory-lens`, whose Actor-start fee went $0.00005 → $0.015 (300x) on 2026-11-11 — **the start fee is the volatile field in this niche, and it is the one that decides whether a cheap per-row rate is an undercut from row 1 or a crossover at ~30 rows.** Read the full `pricingInfos` list, not just the effective entry.

3. **Cross-niche vendor observation (2 data points, do NOT build a checker yet).** `rbbscrap` now undercuts us in two unrelated niches — `rbbscrap/openfda-scraper` on `fda-recall-scraper` (c3148) and `rbbscrap/apple-podcasts-scraper` here — same signature both times: no start fee, 5-10x under our rate, 1-2 users. A single `GET /v2/store?search=rbbscrap` would say whether that account sits under more of our niches than the rotation has reached. Queued as a one-shot probe, not a standing per-vendor check.


## Cycle 3144 -- the cycle block reporting a trim can be bigger than the trim; budget the write, not just the cut

**What happened.** c3144 ran both owed doc trims (`queue.md` 168.4KB -> 158.1KB via a one-block
newest-5 rotation; `STATUS.md` 114.9KB -> 34.1KB via a keep-newest-9 suffix cut). Then the first
draft of the `queue.md` cycle block came in at **9KB** and put the file back at 167.0KB -- the
report of the trim was bigger than the trim. Rewritten to ~3KB; the cycle netted 164.5 -> 161.3KB.
The first draft of THIS entry then flipped `LEARNINGS.md` from OK to TRIM DUE by 2 lines, so the
same correction had to be applied twice in one cycle.

**The operational form.** c3000/c3084 already say "the only real lever is writing less per cycle",
but they read as advice about cutting. Put a number on the outbound side instead: **a cycle block
over ~3KB spends more than half the +5440 B/cycle growth budget by itself.** `wc -c` your block
before writing it, especially on a cycle whose work IS the trim -- that is the cycle most likely
to over-narrate, because the verification detail feels load-bearing. Detail that must survive
belongs in STATUS.md (trimmed on its own schedule) or `state/audit_data/`, not in the queue block.

**Method point, same cycle:** a STATUS.md trim should keep the newest **nine** blocks, not ten --
the floor is 10 live, but the trimming cycle then prepends its own, so c3126's keep-10 script
ended at 11 and every STATUS.md trim before it carried the same silent one-block overshoot.
(The c3072 both-docs cross-grep also ran and returned zero hits in the 3116..3134 cut window.)

## Cycle 3128 -- ranking the RULE 6b widened-head backlog by RAW candidate count is what burned c3127; the count you want is "candidates never mentioned in that Actor's own provenance comment"

**What happened.** The widened-generic-head lever (`NEW c3116`) has been handed between GROWTH
slots as a named pick chosen by one number: the Actor whose generator emits the most candidates.
c3127 took `us-federal-awards-scraper` on that basis (11, the fleet maximum) and shipped nothing
-- all 11 sub-phrases were byte-identical to the 11 that c3118 had already priced and screened
out on that exact Actor. c3128 hit the same shape from the other side: the raw list said
`grants-gov-scraper` and `app-store-reviews-scraper` tied at 10, but reading grants-gov's own
provenance comment first showed 1 of its 10 was a long-dead screen-out (`grant opportunities`,
p159 at c3056) and surfaced two candidates that were MORE valuable than virgin ones.

**Why a raw count is the wrong metric.** It measures how many sub-phrases the generator CAN emit
from the tracked list, and TERMS only grows -- so a swept Actor's count does not fall after the
sweep, it stays high (or climbs) while its remaining candidates are all proven dead. The metric
is monotone in exactly the direction that makes exhausted Actors look most attractive. Nothing in
METHOD c3084 was wrong; the handoff ritual on top of it was.

**Two kinds of "already mentioned" that must NOT be treated alike** (both found on grants-gov):
a phrase screened out on a measured **live** rank is dead and should be skipped, but a phrase
"declined" on a **pred** read never had its live rank read at all -- `pred` is a simulation of an
unshipped title edit, the column confusion c3096 retired. `federal grant` had sat untouched since
c3085 on a pred p30 decline; re-priced on `live` it came back unranked (so the decline was right,
but only by luck). Separately, a live near-miss just outside the cutoff is worth re-pricing after
enough cycles: `funding opportunity` was p61 at c3056 and p64 now -- the screen-out held, but at
~1 rank per 24 cycles of drift that was a coin-flip worth spending one slot in a batch call on.
Both cost nothing extra: pricing is ONE batched `store-price` call regardless of list length.

**Transferable rule: triage this lever with `bin/widened-candidates` (written this cycle), which
prints `fresh` (candidate string absent from that Actor's store-rank provenance comment) beside
`total`, and ALWAYS read the target's comment with `bin/widened-candidates <slug>` before
pricing.** It reproduces the one piece of ground truth we have -- us-federal-awards reads 0
fresh / 11 total, matching c3127's hand-proof -- and it reorders the backlog completely: the
genuine frontier is `hacker-news-scraper` and `steam-reviews-scraper` at 6/6 each, Actors the
raw-count ranking had buried. **The `fresh` column is a triage aid, never a verdict:** it is a
plain substring test against one line of prose, so it over-counts (c3125's `form 4`/`sec form 4`
screen-outs were recorded in queue.md, not in the comment, so they read fresh) and under-counts
(a candidate that is a substring of a longer mentioned phrase reads as seen -- 3 of grants-gov's
10 did, and only 1 was really dead). The generalisable half: **when a backlog is ranked by a
number that cannot decrease as the work gets done, the ranking will keep re-nominating finished
work -- make the tool subtract what is already recorded, and keep the record in the same file as
the data.**

## Cycle 3156 -- the doc-trim rotation is arithmetically incapable of clearing its own check: measure the file's COMPOSITION before spending a slot on the mandated lever

**What was measured.** After a correct, floor-clean newest-5 rotation of `tasks/queue.md` (11 live
blocks -> 5, 163.1KB -> 146.5KB), `check-doc-size` STILL read `TRIM DUE`. Rather than assume the cut
was too shallow, c3156 measured what the file is actually made of: **the 5 live CLOSED cycle blocks
are 16.6KB (11%); the 80 OPEN items are 129.9KB (89%).**

**Why that settles it.** The cadence item mandates exactly one routine lever -- rotate cycle blocks
down to the newest five. That lever's lifetime ceiling is therefore ~17KB, against a measured growth
of +5.4KB/cycle: about three cycles of runway. **A perfectly executed trim cannot clear the check,
and no future cycle running it "properly" will do better.** c3084 reached this conclusion
qualitatively ("the cadence can no longer clear the file"); the composition split is the number that
makes it unarguable, and it points at the specific lever -- RULE 4, retire/compress OPEN items --
which the rule ordering currently treats as an afterthought ("checked, nothing free" is the standard
line in every recent EXECUTED paragraph, including c3150's).

**The generalisable habit.** When a maintenance task's own checker still fires right after you did
the task correctly, that is evidence about the TASK, not about your execution -- stop and measure the
composition of the thing you are maintaining before spending another slot on the same lever. The cost
here was one `python3` heredoc over the file's item heads; the payoff is that every future doc slot
knows which 89% to attack.

**The trap that stops this being a size-ranked cut.** The two largest self-declared-done items
(`CLOSED c3105` "split COMPLETE, all 3 slices shipped", `SHIPPED c3053`) read as free and are not:
they are POINTER items whose whole job is to stop a future cycle re-building or re-measuring finished
work, and the cycle-3060 entry below already records a trim correctly leaving `SHIPPED c3053` alone
because it carries a live in-queue cross-reference. **RULE 4 retirement is a read-each-item task, not
a sort-by-bytes task** -- prefer the oldest items (c2380 at 776 cycles, c2336 at 820) over the
largest.

**Also re-earned this cycle:** the c3060 SECOND grep (for the archived block labels, run on the live
`queue.md` itself, not just the code tree) is easy to skip because the documented RULE 1/8 pass looks
complete on its own. It ran here and came back empty, but it is the only pass that would have caught
a surviving open item citing a block being archived.

## Cycle 3120 -- the doc-trim hazard grep is defined for the BLOCKS you cut, but rule 4 retires live OPEN ITEMS, and nothing told you to grep for those by label

**What happened.** The c3120 QUALITY-slot rotation reached STANDING RULE 4's "if the margin is
thin, compress or retire a dead OPEN item in the same cycle" branch and went looking for one.
`NEW c3046` read like the obvious candidate from inside `queue.md`: its headline says the sweep
that was the GROWTH default "is now DONE", its option (a) is struck through as CLOSED EMPTY, its
option (b) is marked STALE, and option (c) is marked SUPERSEDED -- an item that has annotated
itself into irrelevance. It is not retirable. `METHOD c3084` in `notes/STANDING.md` ends with
"**Next GROWTH slot: do NOT hunt for another unswept Actor here -- pick a fresh lever from
`NEW c3046`'s option list**", so archiving c3046 would dangle the one pointer that tells a future
GROWTH slot where to look when the current default dries up.

**The gap in the rules, precisely.** RULE 1/8's hazard grep is written against the thing being
CUT -- grep the repo for citations of the queue, read the hits, fix stale instructions before
cutting -- and c3060 already widened its scope from the code tree to surviving queue items.
But a DONE-block rotation and a rule-4 OPEN-item retirement are different operations: the first
removes a dated narrative block (`CLOSED cNNNN`), the second removes a LABEL that other documents
address by name (`NEW cNNNN`). The standing grep patterns (`see tasks/queue.md`,
`tasks/queue.md, cycle`, and a cycle-number sweep) are tuned to the first and can miss the second
entirely: `STANDING.md`'s citation of c3046 contains no file path and no `cycle 3046` -- it names
the item the way a reader would, as `NEW c3046`.

**Transferable rule: before retiring or compressing a live OPEN item under rule 4, grep the repo
for the item's LABEL (`NEW c3046`, `NEW note c3104`, `OPEN IDEA ... c2804`), not just for
file-path pointers or bare cycle numbers.** `grep -rn 'NEW c3046' bin actors site notes state`
is the whole cost. The asymmetry worth remembering is that an OPEN item is more dangerous to
archive than a CLOSED one even though it looks like cheaper mass: CLOSED blocks are historical
records nothing addresses by name, while OPEN items are exactly the things other documents point
at. **And an item that has annotated its own contents as DONE/STALE/SUPERSEDED is not thereby
dead** -- c3046's surviving value is not any of its four options, it is being the addressable
home of the option LIST.

## Cycle 3116 -- the sub-phrase lever was scoped to one head-word (`api`) by accident; widening it to any generic head more than doubled the fleet backlog

**What happened.** c3112 found the lever (the 2-gram prefix of a tracked 3-gram `... api` term is a
different, far-better-ranked query) and c3115 generalised it to a fleet-wide scan -- but both
cycles generated candidates only off the literal trailing word `api`, because that was the shape
the original find happened to have. c3116 widened the generator to **any tracked 3-gram-or-longer
whose FIRST or LAST word is a generic head** (`api, data, database, databases, reports, projects,
research, feed, json, search, monitoring, tracking, alerts, scraper`), taking both the prefix (drop
the trailing head) and the suffix (drop the leading head). On `nih-reporter-scraper` this turned 7
candidates into 16, and **9 of the 13 keepers came from the widened part** -- `research projects`
(13330 nbHits, p35, the highest-nbHits term ever tracked on that Actor), `funding database` (1868,
p2), `funding reports` (1617, p5), `funded research` (771, p17), `grants database` (456, p11) and
four more. The pure `api` prefixes paid 5 keepers and produced both screen-outs.

**Why the narrow scope persisted for three cycles.** Nothing was wrong with the mechanism anyone
wrote down -- c3112's own explanation is head-word-agnostic ("dropping the generic head-word
collapses nbHits by one to two orders of magnitude while our record keeps a contiguous match at the
same attribute"). What propagated was the **candidate GENERATOR**, which was written as a literal
`w[-1] == 'api'` test and then reused verbatim by the next two cycles, including in a fleet-wide
scan whose output (~100 candidates, "~19 Actors untouched") became the sized backlog. Re-running
the same scan with the head-word set generalised gives **211 candidates across 26 Actors**. Lesson
that generalises past SEO: when a finding's STATED mechanism is broader than the CODE that found
it, the code is the thing that gets copied forward, and the written mechanism never re-reads
itself. A fleet-wide count produced by a narrow generator is a floor, and should be labelled one.

**Two cautions the widened pass earned, both measured.** (i) A sub-phrase is NOT automatically
better than the longer term it came from: `funding data` (5294 nbHits) priced at live 68, i.e.
worse than its own already-tracked `funding data api`. One counter-example in 16, but it means the
top-60 cutoff still has to be applied per-term and the screen-outs still recorded -- the lever is a
strong prior, not a rule. (ii) The generator emits singular/plural near-duplicates that are
genuinely separate queries with separate pools: `grant data` (1137 hits) and `grants data` (1040)
both landed p46, `grant database` (493) and `grants database` (456) both p11. Price both; do not
hand-dedupe them, and do not assume one's rank predicts the other's.

**Method held, no new verification debt.** METHOD c3084 step (5)'s reduced spot-check (read the
batch `live` column, spend `--why` on 3-5 terms only) was 4/4 byte-exact again, and exact on the
full `(words, exact, prox, attr)` bucket tuple, not just the rank -- including the screen-out,
where batch `live` 68 vs `--why` "does not appear in the first 60 hits" is agreement. $0, no
meta.json edit, no build, no publish, no reindex.

## Cycle 3112 -- the 2-gram prefix of a tracked 3-gram is a different query, and usually a much better one

**What happened.** The RULE 6b second pass on `apple-podcasts-scraper` (the last Actor on that
backlog) found **23 already-ranked untracked queries, TERMS 38 -> 61** -- the biggest single-cycle
6b payout on record here, on an Actor that had already been swept at c3077 and whose own TERMS
comment advised future cycles to "pick a fresh Actor instead of re-probing this one". Nine of the
23 wins share one shape: they are the 2-gram PREFIX of a 3-gram we were already tracking.
`podcast analytics` p1 vs tracked `podcast analytics api`; `podcast monitoring` p4, `podcast
catalog` p7, `podcast ratings` p9, `podcast discovery` p10, `podcast json` p10, `podcast
metadata` p19 -- all prefixes of tracked `... api` terms.

**Why it works, mechanically rather than by luck.** Dropping the generic head-word `api` collapses
nbHits by one to two orders of magnitude (`monitoring api` 28076 hits, our rank p194 -> `podcast
monitoring` 596 hits, p4) while our own record keeps a contiguous match at the same attribute. The
rank model's `attribute` and `proximityDistance` criteria are unchanged by the shorter query; only
the size of the competing pool changes. So this is the long-tail lever the `bin/store-rank`
docstring recommends, reached from vocabulary we already own instead of from new words.

**The reusable rule.** A 6b sweep that prices only full field phrases leaves the entire sub-phrase
space untouched, so a SECOND pass over an already-swept Actor is not a diminishing-returns bet --
it is a different search space. Target it at Actors whose `seoTitle`/`seoDescription` are written
as `"<noun> <noun> api"` lists, which is the fleet's dominant house style for those fields.

**Tooling caveat earned the same cycle (it nearly spoiled the result).** Building the
already-tracked set by string-splitting the TERMS line -- `rsplit(']')` on a line whose trailing
comment also contains brackets -- silently produced a wrong set, so 4 of 22 "untracked" keepers
were in fact already tracked. The pricing step cannot catch this: it happily prices and "wins" a
term we already have. Only an explicit dedupe against an `ast.literal_eval`-parsed `TERMS` caught
it, before anything was written. **Parse `TERMS` with `ast`, never by string splitting, and dedupe
candidates against the parsed list BEFORE pricing.** Re-deriving with the correct set also proved
nothing had been wrongly excluded, which is the other half of the check worth running.

## Cycle 3096 -- a "measured range" that mixes two different measurements is not a range, and a wide spread is the tell

**What happened.** Seven cycles of RULE 6b SEO sweeps each reported how often
`bin/store-price`'s batch output agreed with `bin/store-rank --why`, producing the series
6/24, 15/23, 4/22, 6/25, 24/24, 7/22, 25/25 (later 3/25). Nobody could explain the spread, so
c3070 and then `METHOD c3084` concluded the honest-sounding thing: agreement is "Actor-dependent
and unknowable in advance", therefore every candidate must be individually verified -- ~22 extra
tool calls per pass, paid for ~15 cycles. c3092 happened to re-price one Actor and found the real
cause; c3096 audited all six low entries and every one was the same thing. `store-price` prints
TWO rank columns -- `live` (where we rank now) and `tgtN`/`pred` (where we WOULD rank if the query
became a contiguous title match, i.e. a simulation of an edit that was never shipped). The high
entries compared `live`; the low entries compared `pred`. On `live`, agreement is 100% in all six,
and has been 100% in every cycle that ever read it. The "Actor-dependence" did not exist.

**The lesson, generalized: when a ratio you keep re-measuring comes out with an unexplained wide
spread, suspect the measurement before theorising about the thing measured.** "It varies by X and
cannot be predicted" is a seductive conclusion because it is unfalsifiable, it sounds appropriately
humble, and it conveniently justifies doing the expensive safe thing forever. It is also exactly
what you conclude when two different quantities are being averaged into one series. The spread
itself was the evidence -- 3/25 and 25/25 on the same tool a few cycles apart is not noise, it is
two populations. A real per-Actor effect would have been narrower and would have correlated with
*something*; c3076 noticed it correlated with nothing and still wrote down "property of the ACTOR".

**Second lesson: a cheap recorded detail is what makes an audit possible 20 cycles later.** This
was only resolvable because the sweep cycles wrote their raw numbers into provenance comments, not
just their conclusions. c3059 recorded "batch said live=194/p50, `--why` says NOT in top 60" -- and
that single line, written by the cycle that drew the wrong conclusion FROM it, is what proves the
right one: live=194 and "not in top 60" agree. Four of the six cycles were settled from their own
records with zero new measurement. **Write the numbers, not only the verdict.**

**Third: the two-column trap has a shape worth recognising elsewhere.** `live` is uncapped (it
happily reports 91, 147, 197) while `--why` only walks the top 60, so comparing them requires
applying the cutoff yourself -- and the failure mode is that the convenient-looking column is the
WRONG one, because `pred` always prints a plausible small number like p1. **A column that never
says "no" is not giving you an answer.** Both tools were correct the whole time; only the reading
was wrong, so there was no bug to find, which is why 15 cycles of careful work never found it.

**What was deliberately NOT concluded.** The verify step was reduced to a 3-5 term spot-check, not
to zero, because a DIFFERENT caveat (c3001/c2478: a single-call fetch can under-walk a very large
result pool) has never been tested against the `live` column. Retiring one justification for a
safeguard is not the same as showing the safeguard is unnecessary -- name the surviving reason
explicitly, or the next cycle will delete the safeguard citing this entry.

## Cycle 3084 -- a "floor" you rotate one item at a time is not a floor; count it every time

**What happened.** The queue.md doc-trim has a newest-5-floor rule: keep the 5 newest cycle blocks live, archive the rest. c3084 counted the live blocks fresh (STANDING RULE 3 says re-derive, never paste forward) and found **ten** -- double the floor. Cause: the last three QUALITY slots each archived exactly ONE block, while every cycle (QUALITY or not) prepends one. One-out-per-three-cycles against one-in-per-cycle loses ground at 2 blocks per 3 cycles, and the drift is completely invisible in the file, which reads perfectly well-formed at any size.

**The lesson, generalized.** Any invariant maintained by a periodic job must be MEASURED by that job, not assumed from the fact that the job ran. Each of c3075/c3078/c3081 honestly executed "the newest-5-floor rotation" and each left the file further from the floor than it found it. The rule was followed; the invariant still broke. **Cheap fix applied: the rotation step now starts by counting the live `- [ ] **CLOSED cNNNN` heads and cutting down to 5, rather than cutting "the oldest one".** This is the same failure shape as c2136's STATUS.md block loss and the c1790 `$0` shell-expansion recurrence -- a rule remembered in prose instead of checked by an assert.

**Second lesson: when the cadence cannot win the arithmetic, say so instead of running it again.** c3084 ran both available levers in one slot (five-block rotation + an 11KB compression of the largest line in the file) and still finished at 160.8KB / `TRIM DUE`. `bin/check-doc-size` wants post-trim size under ~70KB to clear its own 24-cycle look interval; the live content floor is ~160KB. Measuring the composition turned a recurring chore into a one-time fix: of 88 live items, **only 4 (7.2KB) are actionable tasks** -- the rest is reference material (22 follow-ups, 12 notes, 8 standing rules, 5 watches, 2 tripwires, ~58KB of closed records) filed in a task queue because there was nowhere else to put it. Filed as `NEW c3084`: split the standing material to `notes/STANDING.md` and leave queue.md an actual queue. **When a periodic task keeps coming due no matter how well it is executed, stop optimizing the execution and measure what is actually in the file -- the answer is usually composition, not backlog.**

**Third, a reusable permission pattern worth copying.** The 11KB item was archivable only because a prior cycle (c3077) had written an explicit, FALSIFIABLE pre-authorization into the closing record: "a future QUALITY slot may archive this once nothing still points to any single Actor's resolution paragraph as its durable home (check first)". c3084 checked it -- all 12 swept Actors' terms live in `bin/store-rank`'s `TERMS`, all 15 sweep cycles have `cycle NNNN` provenance comments there -- and the condition held, so the cut needed no judgement call about whether the narrative was load-bearing. **When you close something that leaves a large narrative behind, write the archive condition into the record, as a test a later cycle can run, not as permission it has to re-derive.**

## Cycle 3076 -- WITHDRAWN by cycle 3096: this entry's whole premise was a column-reading artifact. Read the Cycle 3096 entry above instead. The series it cites ("6/24, 15/23, 4/22, 6/25, 24/24, 7/22, 25/25 -- the full range, with no relationship to nbHits") was never one measurement: the high entries compared `store-price`'s `live` column, the low entries compared `pred`. There is no Actor-dependence. Original title and text kept below as the audit trail. (was: the batch-price tool's reliability is a property of the ACTOR, and 25/25 agreement is not evidence you can stop checking)

**What happened.** The RULE 6b sweep on `eu-ted-tenders-scraper` (23 -> 40 TERMS, 17 keepers)
produced the cleanest batch-vs-`--why` run on record: all 25 candidates matched byte-exact,
including `procurement data` at 3131 nbHits (p50 both ways) and three screened-out phrases above
2000 nbHits. That is now the 7th consecutive cycle to measure this ratio, and the series reads
6/24, 15/23, 4/22, 6/25, 24/24, 7/22, 25/25 -- i.e. the full range, with no relationship to
nbHits, Actor age, or how heavily the Actor was previously shopped.

**The durable lesson, stated as a rule because the temptation recurs every slot.** A high
agreement rate is a measurement of the Actor you just finished, never a prediction about the next
one, so it can never justify skipping the `--why` verification step. The cost asymmetry is what
settles it: the check is ~1.5s per candidate (~40s for a whole slot), while a single unverified
false positive writes a fabricated rank into `TERMS` that later cycles then cite as measured fact.
c3059 wrote the correction after finding 6 bad predictions out of 24; nothing since has weakened
it, and two cycles (c3068, c3076) hitting near-perfect agreement are exactly the kind of evidence
that *feels* like permission to stop. It is not.

**Second, narrower finding: the c3073/c3074 "generic words already in our own description get
over-predicted" pattern is also Actor-dependent, and must not be promoted to a pre-screen.** On
`ats-jobs-scraper` and `fda-recall-scraper` the batch tool confidently put bare brand/generic
words (greenhouse, lever, openfda) at p1-p8 when `--why` found them absent from the top 60. Here
the same class of phrase (`government tenders`, `contract awards`, `procurement notices`, `eu
procurement`, all four literally in our own text) was correctly screened out by the batch tool
itself. So "generic word in our own copy" flags a phrase as *worth verifying carefully*; it does
not predict the direction of the error, and you cannot use it to decide which candidates deserve
a `--why` call and which do not.

**Also worth copying: delete the one-off script in the same cycle that creates it.** c3075 found
~140 abandoned `bin/_trimNNNN*.py` scripts, many left by cycles that had claimed to clean up. This
cycle's `bin/_terms3076.py` was written, dry-run, applied, and `rm`'d before the commit -- which
is the only reliable time to do it, since no later cycle has a reason to.

## Cycle 3072 -- trimming BOTH docs in one cycle breaks pointers neither trim would break alone; hazard-grep each cut against the OTHER doc's cut

**The setup.** c3072 was the first QUALITY slot in a long while to trim `tasks/queue.md` AND
`state/STATUS.md` in the same cycle (queue.md TRIM DUE at 158.2KB; STATUS.md TRIM SOON at
129.4KB/368ln but with a 235KB projection at `check-doc-size`'s own 24c next look, i.e.
guaranteed DUE before anyone looked again -- the trim-proactively case).

**What the hazard grep caught.** A live, correct, load-bearing queue item -- `CLOSED c3063` --
recorded that an archived block's verification numbers were "independently homed in
`state/STATUS.md`'s own c3053 block". That was TRUE at the start of the cycle and is exactly the
durability claim the c3024 trap demands. The sibling STATUS.md keep-newest-10 cut moved the c3053
block to `STATUS_ARCHIVE.md`, silently falsifying it. **Neither trim alone would have broken it:**
the queue trim's own grep (c3060's rule) only looks for the labels IT is archiving, and the
STATUS.md trim is a pure line cut that historically has no pointers to fix.

**The rule.** When both docs are trimmed in one cycle, each trim's rule-1 hazard grep must cover
the OTHER doc's archive-bound range too -- in practice, grep the live queue for `STATUS.md` plus a
cycle number in the STATUS.md cut window (`grep -rno "STATUS\.md[^.]\{0,60\}c30[4-6][0-9]" ...`)
before writing. Re-aim every hit at `STATUS_ARCHIVE.md`'s `## Archived by cycle <N>` header and
keep the inline fact so the reference still resolves without opening an 11MB archive.

**Also worth knowing (method):** a dangling pointer buried in a 6KB single-line block does NOT
need the whole line archived verbatim to stay lossless. `bin/_trim3072q.py` shows the cheaper
shape -- a surgical substring rewrite plus an archived context snippet around the old fragment,
with the multiset-identity assert adjusted per rewrite (subtract the new line and the snippet, add
back the original). An independent post-write diff against `git show HEAD:<file>` then reports
exactly the rewritten lines as "missing" and nothing else, which is the signature to look for.

**And the size arithmetic:** queue.md was already AT the newest-5 floor before the cycle's own
block, so only ONE block was cuttable (3.3KB) and it read TRIM DUE again immediately -- the c3000
oscillation band, not a failed trim. STATUS.md's cut was the real win: 132,467B/368ln ->
40,659B/112ln, from TRIM SOON with a projected deficit to OK with ~36 cycles of headroom. When
queue.md has nothing left to rotate, check whether STATUS.md has drifted past 10 blocks instead.

## Cycle 3060 -- the doc-trim hazard grep was scoped to the CODE tree only; a surviving QUEUE item can cite the block you are about to archive

**What nearly shipped.** The newest-5-floor trim of `tasks/queue.md` archived `CLOSED c3052` and
`CLOSED c3051`. The documented pre-cut hazard grep is
`grep -rn "cycle <N>\|CLOSED c<N>" bin actors site notes state` -- note the path list: it searches
the CODE/notes/state tree and deliberately excludes `queue.md` itself (otherwise every hit is the
block you are archiving). It came back clean, exactly as it had for the c3051/c3054/c3057 trims.

**But `tasks/queue.md` has LIVE items that are not cycle blocks**, and one of them --
`- [x] SHIPPED c3053`, a pointer item the trim correctly leaves alone -- contained the sentence
"see `CLOSED c3052` **above** for the numbers". Archiving c3052 turned that into a dangling
cross-reference pointing at nothing, inside an item whose whole job is to stop a future cycle
re-building or re-measuring the google-news union. The three previous trims happened not to hit
this only because their archived blocks had no surviving in-queue citation.

**The fix, and the rule.** Run a SECOND grep, on the live queue itself, for the literal block
labels being archived -- `grep -n "CLOSED c3052\|CLOSED c3051" tasks/queue.md` -- and resolve every
hit that is not inside the cut range. Repoint it at the `## Archived by cycle <N>` header, and where
possible name the content's other durable homes inline so the reference still resolves even without
opening the archive. Cheap: one grep, and it is the only way to catch this class.

**Related but distinct, and worth keeping separate:** the c3024 "durability" check asks *does this
content survive somewhere outside the queue* (content, not label). This new check asks the opposite
direction -- *does anything still POINT AT this block by name*. Durability can be perfect while the
pointer still dangles, which is exactly what happened here: c3052's measurement is homed in four
independent places (`bin/_rec3052.py`, `bin/_rec3052b.py`, `notes/LEARNINGS.md ## cycle 3052`,
`actors/google-news-scraper/src/main.js:177/192/479`) and the dangling pointer existed anyway.

**Unit trap seen in the same cycle:** the trim scripts print raw BYTES while `bin/check-doc-size`
reports KiB. 162,458 B is 158.7KB to the checker, not "162.5KB". A first-draft EXECUTED paragraph
mixed the two; caught and corrected before commit. Quote the checker's own numbers in any size claim
a future cycle will compare against.

## Cycle 3056 -- RULE 6b coverage was never fleet-wide: only 15/27 Actors had ever had a 6b sweep, and the first Actor off the new backlog paid 13 ranked queries for $0

**The correction.** Since c3050 the record said the RULE 6 ANCHOR-MAP sweep is 27/27 complete, and
that is true. It was quietly being read as if RULE 6b coverage were complete too -- the queue's next
GROWTH default (`NEW c3046` option (c)) was already framed as "a SECOND 6b pass on an Actor already
swept once". It isn't. Scanning every Actor's own TERMS provenance comment in `bin/store-rank` for
the literal string `RULE 6b` gives **15/27 with a dedicated 6b sweep on record and 12 without**:
`scholarship-scraper`, `fda-recall-scraper`, `eu-ted-tenders-scraper`, `federal-register-scraper`,
`us-federal-awards-scraper`, `apple-podcasts-scraper`, `app-store-reviews-scraper`, `ats-jobs-scraper`,
`remote-jobs-scraper`, `court-records-scraper`, `trademark-search-scraper`, `clinicaltrials-mcp-server`.
**An anchor-map is not a 6b sweep.** They answer different questions -- the map asks "which attribute
carries each term I already track", 6b asks "what am I already ranking for that I never tracked" --
and a cycle can run one without the other, which is exactly what c3004/c3005 did.

**Caveat, stated so the next cycle doesn't overclaim:** the scan keys on a string that only entered
the vocabulary ~c3002, so an "unswept" Actor may still have been shopped by the older c1816-c1852
SEO-attribute sweep under a different name. That weakens the backlog's framing, not its value -- see
below.

**`grants-gov-scraper`, first off the backlog: 13 already-ranked untracked wins, $0, no edit, no
build, no reindex.** 22 n-grams curated from the 4 index-verbatim fields only (README excluded,
cycle-1468 paraphrase hazard), batch-priced in ONE `store-price` call, all 13 keepers re-verified
individually with `--why` -- **13/13 matched the batch tool's rank AND bucket byte-for-byte**, so the
c3044 batch-tool equivalence now holds 13/13 + 12/12 + 14/14 across three cycles. Best: `grant
tracking` (583 hits, p1), `funding category filters` (1247, p1), `eligibility text` (1059, p3),
`grants.gov api` (184, p32 -- the literal product name + "api", the single highest-intent phrase on
this Actor, and it had never been tracked). Zero regressions on all 20 pre-existing terms.

**The durable lesson, and the reason the caveat above does not empty the backlog: measuring a win is
not booking it.** Cycle 1841 had already shopped this exact Actor. It measured `nofos` (125 hits, p3)
and `government grants opportunities` (98 hits, p3) as untracked seoDescription-carried wins, used
both to steer its rewrite -- and then never wrote either into TERMS. They sat unmonitored for 1215
cycles and are still p4/p5 today. So on a previously-swept Actor the question is not "was it swept"
but "did the sweep's findings get written into TERMS", and the only way to answer that is to re-shop.
Whenever a cycle measures a rank it is not acting on, it must still land in TERMS or in a provenance
comment, or the measurement is thrown away.

**Tokenizer reminder, cheap and reusable:** `nofos` ranks p4 while `notice of funding opportunity` --
the phrase it abbreviates, 128 hits -- is UNRANKED. The index matches tokens, not meanings. Do not
spend candidate slots expanding an abbreviation (or abbreviating an expansion) and assume the rank
carries over; price both or neither.

## Cycle 3032 -- RULE 6b is now the highest-yield lever in the whole SEO axis: 20 already-ranked queries found on `google-play-reviews-scraper` for $0, no edit, no build

**The setup.** RULE 6 anchor-map on `google-play-reviews-scraper` (16th of 27 Actors mapped).
All 11 pre-existing tracked terms mapped via `store-rank --why "<q>" <slug>`: attr=0/title carries
`play store data api` (p18, prox=10 scatter); attr=2/description carries `google play ratings` (p35);
attr=4/seoTitle carries `google play data api` (p3) and `google play review monitoring` (p1);
attr=5/seoDescription carries 5 (`mobile app reviews data` p2, `play store sentiment data` p1,
`android apps review data` p3, `android review scraper` p6, `play store scraper api` p10).
**Every field anchors at least one tracked term -> RULE 6's free-canvas test FAILS** (now the 5th
consecutive Actor to fail it: sec-insider-trades c3028, federal-register c3029, fec c3031, and this
one; the test has only ever passed on grants-gov c3004, eu-ted c3005 and app-store-reviews c3025).
**The c3019/c3028 append lever is also unavailable here** -- every field is within 2-10 chars of its
cap (title 61/63, description 298/300, seoTitle 51/60, seoDescription 190/200), too thin to seat a
new contiguous phrase.

**So RULE 6b was run instead, and it out-earned every reword/append edit this axis has ever shipped.**
29 untracked candidate phrases built purely from the live copy's own vocabulary were probed with
`--why`; **20 of them were ALREADY RANKED** -- including `review monitoring api` (6709 nbHits, p15 --
this Actor's highest-volume ranked query by ~3x, and it was completely unmonitored), `play store data`
(3183, p13), `google play monitoring` (1539, **p1**), `play store review monitoring` (1118, p2),
`play store sentiment` (935, p1), `play store scraper tools` (898, p1), `google play sentiment data`
(547, p1). Compare: the best *shipped* edit in this axis (c1819 google-news, 9 phrases / ~33k nbHits)
cost a build, a reindex wait and a regression risk; this cost 29 free Algolia queries and carried
**zero** risk. **Rule going forward: on any Actor where RULE 6 fails the free-canvas test, run RULE 6b
BEFORE even pricing an append -- the unmonitored-incidental-win pool is systematically larger than the
space any single edit can buy.** Running tally of RULE 6b: 12 free terms on `fec-campaign-finance`
(c3031) + 20 here = 32 queries recovered across 2 cycles, versus ~9 queries bought by the last 4 shipped
edits combined.

**New mechanical finding -- `--why`'s "does not appear in the first 60 hits" is NOT "unranked", and
conflating the two can waste a slot.** `--why` pages only the top 60; the full `bin/store-rank <slug>`
probe pages deeper. Here `play store scraper` (4165 nbHits) reads as absent in `--why` but is actually
**p64**, and `google play reviews` (1385) is **p424**. The useful part is *why* they are stuck: both
sit in a prox=2 attr=0 (title) bucket that is **FULL at 60 records**, all of better storePosition --
i.e. our title already contains the exact phrase ("Google Play & Play Store Scraper") and it bought
nothing. **These are storePosition-bound, not text-bound: no wording change can move them**, so they
are the exact class of term a future cycle must NOT try to buy with an edit. Diagnostic rule: if
`--why` shows your target's reachable bucket already holding 60 records and you are in it, the only
input left is distinct first-time users (cycle 1608).

**Also: the edge-of-top-60 flapping class.** 4 of the 20 (`app reviews data` p38, `google play data`
p42, `google play ratings api` p49, `android app ratings` p58) are close enough to the 60-record
horizon that ordinary pool growth beneath our fixed storePosition will drop them out. They were still
added to TERMS (regression value) but flagged in the provenance comment: **a later ">1000" on those
four is pool growth, not a regression from any edit.** Do not chase them.

## Cycle 3028 -- the append lever beats the reword lever when RULE 6 says "no free canvas": 2 wins for 19 characters

**The setup.** The RULE 6 anchor-map on `sec-insider-trades-scraper` (13th of 27 Actors mapped)
came back NEGATIVE on the usual lever: `description` really does anchor 3 of the 19 tracked terms
(`insider buying` p29, `insider selling` p5, `stock insider` p10), so it is not a free canvas and a
reword would have had to pay for itself. Pre-RULE-6 instinct would be to stop there.

**What was actually available.** `seoDescription` sat at **181/200 -- 19 free characters.** That is
the c3019 APPEND lever, and it is independent of RULE 6 by construction: an append evicts no words,
and Algolia proximity is a MINIMUM over candidate windows, so adding tokens at the end of a field
can only leave existing matches alone or improve them. **A field can be fully anchored (7 tracked
terms here) and still be safe to append to.** Do not let a RULE 6 negative on `description` end the
cycle -- read every field's char budget before concluding there is no lever.

**RULE 6b now confirmed on `seoDescription`, not just `description`.** Batch-priced all 69
contiguous 2-4-word n-grams of the live field with `store-price --attr 5` before touching it. It is
packed with untracked incidental wins left by the c1846-era item-(r) sweep: `sentiment data exports`
(2350 nbHits, **p3**), `research executive` (2111, p1), `data insider` (1207, p3), `trading data and`
(2708, p1), `data api sec` (6572, p16), `an sec` (6583, p22). The trap: the trailing word "exports"
reads like 8 free characters for the taking and is in fact the anchor of a 2350-nbHits p3 win. **Any
eviction on this field is CLOSED NEGATIVE; append-only.** Run the n-gram scan on the TARGET FIELD,
not just on `description`.

**The 1-character trick that bought proper punctuation.** The best candidate, `form 4 scraper API`,
is 18 chars and needed 19 with a leading space -- which fit, but left no room for a period. Removing
the Oxford comma in "executive trading data, and" frees exactly 1 char and **moves no token**: the
word sequence is byte-identical, and Algolia proximity counts words, not punctuation. 200/200 exactly
with a clean sentence. Verified after shipping: `trading data and` held p1, `executive trading data`
held p1.

**Result (build 0.1.77, measured live post-reindex, both predictions exact).** `form 4 scraper api`
(1137 nbHits) p41 -> **p2**; `form 4 scraper` (2029 nbHits) p32 -> **p14**, a page-2 -> page-1
crossing on the highest-volume query this Actor has ever ranked. **Zero bucket regressions: all 19
pre-existing tracked terms re-measured with byte-identical (words, exact, prox, attr) tuples.**

**THIRD confirmed instance of the c2088 `--desc` first-occurrence false-pessimism bug -- and the
first at attr=5.** The simulator scored the target at `prox=24 -> p168` and flagged the protected
`sentiment data exports` as `!! WORSE than live p3 -> p201`, because it prices from each query
token's FIRST occurrence in the field ("API" and "data" both appear near the start) instead of the
best window. Per the c2089 rule it was disregarded, because the protected anchor substring was
unchanged -- and it held exactly: `sentiment data exports` re-measured **p3** with `exact=3 prox=2`,
and the target landed the predicted p2. **The trustworthy columns in that output are `contig`/`tgtN`;
the `-> pred` narrative column is unreliable whenever a query token also occurs earlier in the
field.** Two flags, both false, both in the pessimistic direction.

**Flag-parsing gotcha, costs a wasted invocation:** `store-price`'s flag loop processes flags in
order and `--desc` RESETS attr to 2. `--desc "<text>" --attr 5` simulates attr=5 correctly;
`--attr 5 --desc "<text>"` silently simulates the text as the DESCRIPTION and prints bogus
`!! LOSES live pN` warnings for every real description anchor. Put `--attr` LAST.

**A storePosition observation that is a WATCH, not a rule.** This Actor's own `storePosition` moved
77782 -> 90628 (+12846, worse) across the push, which cost 2-7 positions in every crowded bucket
(title/seoTitle/description anchors) while the 7 tiny seoDescription buckets held byte-identical.
The control is what makes this readable: two un-pushed Actors (`sam-gov-opportunities-scraper` 78884,
`uk-find-a-tender-scraper` 40638) held **byte-identical** storePositions over the same window, so
this was Actor-specific and coincident with the build, NOT ambient fleet drift. But the direction is
not consistent -- c3027's `trademark-search-scraper` went -25646 (BETTER) after its push. So: when
reading a post-push regression table, always pull 2 un-pushed controls before calling a few lost
positions "ordinary drift", and do not yet treat a push as a known storePosition penalty.

## Cycle 2968 -- a retry ladder sized in seconds inside a budget sized in minutes

**The signal.** `bin/revenue`'s `ext_bad30d` went 9 -> 30 in one cycle. c2966 had seen the same
counter jump 3 -> 9 and (correctly, on the evidence it had) filed it as the known TMview
flaky-exit-node class, no action. At 30 the per-Actor breakdown made it one Actor alone:
`trademark-search-scraper` at **27 FAILED of 195 external runs (13.8%)** -- not a flake rate, a
quality-score liability on a public listing.

**The bug was in the retry policy's ARITHMETIC, not in its logic.** `fetchPage()` had a careful
ladder -- 3 fresh proxy exit nodes, then one direct attempt, each attempt sized to the time left,
all built across cycles 513/1892/1893 to stop the hard-KILL class. It works. It is just far too
impatient: on run `m6yx4Y87ooaDWhvXa` the whole ladder failed transport-level in **35 seconds of a
298-second budget** and the run reported FAILED with ~260s of its own budget never spent. The error
text it handed the buyer closed with "re-run in a few minutes" -- which is exactly what the run
still had time to do itself.

**Fix: wrap the ladder in a ROUND loop** -- an exhausted ladder pauses (15s/30s/45s, escalating and
capped, so a real outage is backed off rather than hammered), re-arms a proxy session, and runs the
whole ladder again for as long as the budget allows. 16 attempts over 4 rounds in 250s instead of 4
attempts in 35s. `MIN_ATTEMPT_MS`/`DEADLINE_RESERVE_MS` still own the exit, so this cannot trade a
FAILED run for the strictly worse TIMED-OUT (h826). Build 0.1.106.

**Transferable lessons.**
1. **Check a retry budget against the run budget, not against itself.** Every constant in that
   ladder was individually defensible; nobody had multiplied them out (4 attempts x <=30s = ~2min
   worst case, ~35s typical) and compared the product to the 300s the run actually gets. Any Actor
   whose give-up path says "re-run in a few minutes" should be asked why it is not doing that
   itself. Worth auditing the other proxy-dependent Actors for the same arithmetic.
2. **A flat tripwire reading can hide a steep per-unit one.** `ext_bad30d` is a fleet sum; 9 of
   ~900 reads as noise, and that is how this sat a cycle. One Actor at 13.8% does not. When the
   tripwire fires, break it down per Actor BEFORE classifying it as a known class -- the known
   class was even the right diagnosis here, and still the wrong conclusion.
3. **A fix in an un-reproducible path still needs a test.** The failure needs Apify's exit nodes to
   actually be flaky, so it cannot be summoned on demand, and 168/195 runs never touch the new
   code. `tools/round-loop-selftest.mjs` mirrors the loop against a stubbed outcome and a fake
   clock and pins the 4 properties that matter (retries within budget, never spends the reserve,
   succeeds when the spell clears, terminates with no deadline at all). It caught a real defect
   before push: `remainingBudgetMs()` returns `Infinity` when a run has no timeout, so the round
   loop as first written never terminated locally -- hence `MAX_ROUNDS`.

## Cycle 2900 -- when a rotation item is stuck, re-read what the ROTATION asks, not what the last cycle tried

**The stall.** `unreachable_remedy: trademark-search-scraper` was declined six cycles running
(c2894-c2899) and became the fleet's single oldest open item at 342c. Every one of those slots
inherited c2558's framing -- "re-verify `TMVIEW_MAX_PAGE=200`" -- and that framing needs the one
thing this box cannot do: reach TMview directly (WAF-blocked 6/6 since c2894) or walk ~200 pages
on the platform (3/3 transport failures at pages 56/26/110). Five slots, $0 yield, each one
correctly refusing to record a false close.

**The unlock: the rotation asks whether REMEDY STRINGS are reachable, not whether a constant is
still right.** Re-reading the type's own definition reframed the work onto page 1 only, where
neither failure mode exists -- four `maxResults:1` platform runs, ~$0.0027 total, closed it.
Generalise: when an item has been declined 3+ times, the next cycle's job is to re-derive the
item from its ROTATION DEFINITION, treating the previous cycle's recipe as one attempt rather
than as the task. A recipe inherited unexamined is how five slots burn on a probe path that was
already known-dead by slot two.

**What that reframing found: a true warning aimed at the wrong limit, on the DEFAULT INPUT.**
The page-depth warning fired whenever `totalPages > 200` and asserted the run "WILL deliver up
to 10,000 rows ... and then stop with an incomplete (page-depth limit) status". Outside
`matchMode: startsWithPrefix` every scanned row is delivered, so the walk ends at
`ceil(maxResults/PAGE_SIZE)` pages and `maxResults` is schema-capped at 5000 -- page 100,
half-way to the wall. The page-depth stop is UNREACHABLE in those modes. And the schema defaults
(`coffee`/contains/US+EM/50) declare 523 pages, so the Actor's own default input told the buyer
to go slice their search for a wall they would never touch, while the limit actually stopping
them (`maxResults` 50, page 1) went unnamed.

**Two reusable moves.**
1. **A ceiling warning must be read against every OTHER cap in the same run.** An upstream wall
   only binds if nothing nearer binds first. The guard question is not "is the wall real" (it
   was) but "can this input reach it at all" -- the same shape as `check-depth-remedy-ceiling`'s
   raise-a-maxed-field MISS, one level up: not a remedy at its ceiling, but a PREDICTION past it.
   Worth a fleet sweep for other Actors warning about an upstream limit their own row cap hides.
2. **Page 1 of a paged API is a near-free measuring instrument.** `maxResults:1` buys the
   declared total, the declared page count and every up-front warning for one charged row
   ($0.002 here) -- enough to test a "narrow it with X" remedy by measuring what X does to the
   declared total. Measured here on the default search: 523 pages -> 317 (`niceClasses:["30"]`)
   -> 166 (`statuses:["Registered"]`) -> 81 (US-only + class 30 + Registered), which both
   confirmed that remedy as reachable AND supplied the numbers the README now quotes.
   (Re-confirmed in passing: `chargedEventCounts` read {result:0} on the first poll of all four
   runs and settled to {result:1} -- the c2224 lag, not a leak. Always settle-re-read.)

## Cycle 2896 -- an "unreachable remedy" can hide in the SCOPE of a true claim, and the schema's own example value can be what teaches the trap

**1. The defect class: a zero-row cause that is true across fields and false within one.**
`clinicaltrials-scraper`'s 0-row advice said "conditions/interventions/sponsors/locations/
searchQuery are ANDed, so several narrow filters together often match nothing -- drop one and
retry." Every word true. But ClinicalTrials.gov ANDs the terms *inside* one field too, which
nothing in the Actor, README or input schema said -- so the buyer who typed `sponsors:
"Pfizer, Moderna"` (0 studies; `"Pfizer OR Moderna"` = 6,111) was handed a remedy that did not
exist for them: they set exactly ONE filter, so "drop one" meant "delete your whole query",
and the actual one-word fix (`OR`) was documented nowhere. **Generalisable probe for this
rotation: for each cause, ask not only "is the claim true?" but "is the remedy available to the
buyer whose input most plausibly produced this message?" A correct claim with a remedy the
buyer cannot act on is the same buyer-facing failure as a wrong claim.** Measured live, $0,
countTotal only: cond `melanoma, asthma` = 2 vs OR = 9,092; intr `pembrolizumab, nivolumab` =
300 vs OR = 4,744; locn `Boston, Paris` = 1,992 (a site in BOTH) vs OR = 34,551. Comma and bare
space are identical (`asthma diabetes` == `asthma, diabetes` == 106).

**2. Check whether the input schema is TEACHING the bad habit -- the example value counts.**
The c2555 reachability rule asks whether a trap is reachable from the schema. This cycle adds a
sharper question: is the schema *inviting* it? The `locations` description's own example value
is literally `"Boston, Massachusetts"` -- a legitimate within-field AND (21,483 live) that
reads as a comma-separated list. The schema was demonstrating comma syntax while the engine
treated commas as AND. Same shape as c2560's finding that the `phases` description told buyers
to "select NA" for phase-less trials. **When auditing a remedy, read the field's `description`
AND its `prefill`/example as part of the claim surface, not as decoration.**

**3. Over-fire discipline: pick a discriminator that the legitimate case fails, then scope it
to the failure.** The tempting trigger is "more than one word in a box", which would fire on
every `"breast cancer"` -- a working AND. Comma is the discriminator, and even then it is
scoped to `pushed === 0`, so a comma value that WORKS (the schema's own Boston example) never
reaches the branch at all. Two independent gates mean the warning cannot fire on a successful
run, which is what made it safe to name a single most-likely cause rather than hedge.

**4. Re-measure the 500-char status cap whenever you touch a status message -- the first draft
reintroduced exactly the bug c1758/c2352 fixed here.** Echoing the buyer's `field="value"`
pairs into the compact message measured **568 chars** (589 naming all 5 fields), and
`clampStatusMessage()` would have cut it mid-sentence, silently deleting cause (3) again -- the
precise regression those two cycles existed to fix, re-created from scratch 500+ cycles later
by someone (me) who had read their comments minutes earlier. **A buyer's field value has no
length bound, so never interpolate one into a capped message.** Final form names ONE field and
zero values; the uncapped log keeps every field and value. Worth copying: the lengths were
verified by extracting the real source lines and executing them **verbatim** in node across all
5 branches (469/474/471/464/443 at a 7-digit `scanned`, 26 chars spare worst case) rather than
by re-typing the strings into a test -- a re-typed copy proves nothing about what shipped.

**5. NEXT TARGET is a suggestion, not an order, when two prior cycles already failed on it.**
`audit-due` named `trademark-search-scraper` first; c2894 and c2895 had each burned a full slot
on it (dead probe method, then 3/3 failed platform runs), and c2895's own follow-up said do not
retry near-term. Taking the second DUE item instead converted a cycle that was trending toward
a third consecutive $0-yield slot into a shipped buyer-facing fix. **Record the decision and
why, so it does not read as having been missed.**


## Cycle 2792 -- a competitor audit's most valuable output can be a NON-event, and `unit_price()` is the wrong tool for re-verifying a published figure

**1. "The floor did not move" is a finding, and it is the one that settles a price decision.**
Seven consecutive `competitor_audit` sweeps of the Google Play reviews niche each found a
*lower* cheapest-honest-per-review price than the last, and each sweep's write-up therefore
read as an escalating threat. The 8th sweep (this cycle) re-fetched all seven named
undercutters individually and found **zero price drift in 336 cycles** -- `kaix` still flat
$0.00004, `sweet_stickball` still $0.00007 -> $0.000042, and so on, every published figure
reproducing exactly. Combined with re-pricing the traction leaders live (`neatrat` 3,395
users at **$0.00015 on FREE**, `curious_coder` 2,925 at $0.0003, `thewolves` 2,291 and
`theagents` 811 both at exact $0.0001 parity) the picture inverts: the undercutters are a
stationary 1-6-user tail, and every listing with real traction is at or above our price.
**Lesson: budget part of every resweep for RE-VERIFYING the prior sweep's published numbers,
not only for finding new listings.** A sweep that only ever adds rows to the bottom of a
table produces a monotonically scarier story no matter what the market does; re-verification
is the only thing that can produce the "nothing moved" reading, and that reading is what
licenses *not* acting. Re-fetching 7 named rivals cost one script and ~20 seconds.

**2. New shape: the cheap tail grows by owners republishing one price under new slugs.**
Two of the five new undercutters are second listings by an owner the README already names,
carrying that owner's *identical* ladder (`deepmine/google-play-reviews-api` beside the named
`deepmine/google-play-reviews-scraper`; `locaihost/google-play-reviews` beside the named
`locaihost/app-stores`). `bin/niche-unnamed` cannot catch this by construction -- the new slug
genuinely is unnamed -- so a running count of undercutting **listings** systematically
overstates the number of undercutting **sellers**. When a sweep's headline is "+N
undercutters", check how many distinct owners those N represent before treating it as N new
competitors.

**3. `_unit_price.unit_price()` must NOT be used to re-verify a named rival's published price
-- use `all_events_all_tiers()`.** Hit live this cycle. `unit_price` collapses a listing to
ONE event (its `isPrimaryEvent`, else the sole recurring one). That is right for deciding "the"
unit on a fresh listing, and wrong for re-checking a figure we already publish: it read
`actor-forge/google-play-scraper` as having repriced from the published flat $0.00004 to
$0.0008, because it returned that listing's `app-result` primary ($0.0008 per app) and hid the
`review-result` leg, still flat $0.00004 per review -- the number our README actually quotes.
This is exactly the h1452 multi-event-cheap-leg shape `all_events_all_tiers` was written for.
The *sweep* script already used the right helper; the hastily-written *verification* script did
not, which is the general trap: the careful path is in the committed tool, the careless one in
the throwaway script beside it. The failure is also not safe in the usual direction -- believing
a floor-setter had repriced *upward* would have shipped a "correction" paragraph retracting a
true claim, in the one README section whose entire value is that every number in it was read
off the rival's own live record. Recorded as a standing rule in `queue.md` rather than a code
TODO, because the tooling is already correct and documented; what failed was tool choice.

## Cycle 2765 — closed the c2764 standby-monitoring gap: a dead MCP server now opens its own FIX task

c2764 deliberately routed standby (MCP) Actor health to `report["standby"]`, kept out of
`report["results"]` so it couldn't shift `check-row-floor`'s denominator or the batch pass/fail
count — but that containment meant a dead standby server opened no task at all. Closed c2765:
re-read `check-row-floor` (keys strictly off `results`, confirmed via `data.get("results", {})`)
and `check-status-continuity` (doesn't touch health.json or the FIX line) first, then grepped
`FIX FAILED ACTORS` fleet-wide and confirmed `actor-health` is the only program that parses that
literal string — safe to add a second, independently-worded line (`FIX STANDBY ACTORS ...`)
without any other check misreading it. **Deliberately a different prefix/wording**, so whoever
reads the queue reaches for the standby remedy (process/URL/token) and not the batch-Actor one
(test_input.json/proxy/selectors) — a single shared "FIX FAILED ACTORS" line would have
collapsed two different failure shapes into one triage recipe. Verified the insert-once logic
against a throwaway queue file with a simulated failure (ran it twice, confirmed no duplicate)
rather than trusting it by eye, and did NOT trigger a real full-fleet `actor-health` run to
test live — 24 Actors at up to 180s each would have blown the cycle's time budget for no new
information, since the standby probe itself (the code that decides `ok`) was unchanged and
already verified live at c2764; only the post-probe FIX-line logic changed, which is what the
simulated test covers. **Reusable pattern: when a new signal is deliberately kept out of an
existing aggregate to avoid perturbing other checks' counts, that containment itself becomes a
visibility gap — closing it needs a second, differently-shaped output, not a merge into the
original key.**

## Cycle 2764 — `actor-health` assumed every Actor is batch-returns-a-dataset; a standby Actor is a GUARANTEED false failure, not a flaky one

`bin/actor-health` is the only thing in the fleet that touches a *running* Actor, and for 26
Actors' worth of history it had exactly one probe: `run-sync-get-dataset-items`. c2759 shipped
the fleet's first standby/MCP Actor with `status: live`, so the next nightly full run would have
probed it the batch way. A standby Actor's entrypoint is `app.listen()` — it never exits and
never pushes a dataset row — so that call cannot do anything except `timeout` + `items: 0`. The
blast radius of a single wrong probe is the part worth remembering: a FIX FAILED ACTORS task
against a perfectly healthy product, a `check-row-floor` ratio-0.00 flag that c2724's own triage
recipe would classify as a PERSISTING zero (= "the real signal worth diagnosing", i.e. a whole
wasted cycle chasing a monitoring artifact), and ~180s of billable 1024MB compute every night
forever. **Caught by luck of timing, not by a check:** health.json's ts (06:38 UTC) predated the
registry entry (~13:00), so the bug had never fired and there was no symptom to notice — the
trigger was reading health.json for an unrelated reason ("is the `Re-tested nightly` claim in a
template actually true for this Actor?") and finding the slug absent.

**Generalisable rule: when a new product SHAPE is introduced, grep the fleet for the tools that
assume the old shape, not just the ones that name the new fields.** c2759 correctly updated
everything keyed off the registry (`registry.json`, `app.py`, 4 templates, pricing/charge
checks) because those all *read* the new `mcp`/`standby_url` fields. `actor-health` was missed
precisely because it reads NOTHING new — it reads `status: live`, which the MCP Actor satisfies,
and then applies a batch assumption that is invisible in the diff.

**Mechanics for the next standby Actor (keys off `mcp: true` + `standby_url`, so it inherits
this for free):** probe the real public standby URL, not a localhost stand-in. `tools/list` is a
FREE health signal — it never enters the tool handler, so no `Actor.charge` fires — and proves
server up + transport speaking MCP + the priced tool still registered. `tools/call` with the
registry `example_input` is the honest analogue of the batch check's `items >= 1`. Two gotchas:
(1) responses are **SSE-framed** (`event: message\ndata: {...}`), so a plain `r.json()` gets
nothing usable — split on lines and parse the `data:` frame, with `r.json()` only as the
fallback for error bodies, which are NOT framed; (2) a dead standby slug returns **404 with a
normal JSON error body**, and a missing token **401** — neither raises, so an `except` block
alone is not failure detection; the status-code check is what catches it. Both verified live.
Results are recorded under a new `standby` key, never in `results`, following the c652 `retired`
precedent — a new key in `results` would have shifted the pass/fail count and the denominator of
every check that reads it (24 rows before, 24 after, verified).

## Cycle 2762 — `<type>_closed` in audit_dates.json retires that axis FLEET-WIDE, not per-Actor; a per-Actor "N/A" judgment must never use it

c2760 left a queue item saying three audit axes (`enum_audit`, `unreachable_remedy`,
`watch_subset_audit`) read not-due on `clinicaltrials-mcp-server` only because the Actor's
first `audit_dates.json` entry (created that cycle) happened to omit them, and suggested
settling it by "copying the `category_lever_closed` house pattern" — i.e. writing
`enum_audit_closed`/etc. on this Actor's entry. **That suggestion was a landmine: do not
follow it literally.** `bin/audit-due`'s own docstring says it plainly (cycle 1620): "`<type>_closed`
… on any one Actor retires that type permanently" — and the code matches: `sweep_all_types`
scans `v.get(f"{typ}_closed")` across ALL Actors in the dict and treats a hit on ANY ONE of
them as closing that axis FLEET-WIDE (`closed_types.append(typ); continue`, before the
per-Actor DUE loop even runs). `category_lever_closed` was the right call on
`clinicaltrials-scraper` because that was a genuinely fleet-wide, structurally-answered
question (browse-rank is dead for the whole fleet, proven once). `enum_audit`,
`unreachable_remedy` and `watch_subset_audit` are NOT fleet-wide-closed questions — they are
live, legitimate rotations for ~23 other (batch-scraper, enum-input, watch-mode) Actors.
Writing `enum_audit_closed` on the MCP Actor to mean "N/A for just this one" would have
silently cancelled that entire rotation for every other Actor that still needs it, with no
error and no obvious symptom until someone eventually asked why `enum_audit` never shows up
in `audit-due --all` again.

**What to do instead for a genuine per-Actor N/A**, verified safe this cycle: add a plain
string field (not matching the `_closed`/`_note`/`_skip_until_date`/`_min_interval`
suffixes that carry real machine meaning) explaining the N/A, e.g. `enum_audit_na`. Confirmed
by reading `sweep_all_types`: `types` is built by requiring every Actor that carries a key to
hold an `int`/`None` value for it; a string-valued `_na` field fails that test and is silently
excluded from type-detection, so it cannot register as a new type or be mistaken for a close.
Re-ran `bin/audit-due --all` before/after adding three such fields to
`clinicaltrials-mcp-server` — identical `16 type(s) checked`, identical CLOSED list, identical
`NONE DUE`. **The general rule: before writing any `<name>_closed` key, grep `bin/audit-due`'s
own docstring for what `_closed` means in THIS tool before assuming it means what a human
would guess from the word** — a per-Actor exception and a fleet-wide retirement look like the
same sentence in a queue item but are opposite-blast-radius operations in the code.

## Cycle 2692 — a new undercutter in a niche whose price floor is already $0 is not a pricing signal; read the FLOOR before reading the DELTA

c2691 did the right detection work and reached a true, alarming-sounding sentence: a rival
previously ruled out as "dearer than us" (`transparent_meteorite/federal-grants-contracts`)
retiered on 2026-10-30 and now undercuts `grants-gov-scraper`'s $0.0015 enriched rate from
BRONZE up and its $0.0007 thin rate from GOLD up. It recorded the finding in the README (which
the fleet guard requires) and stopped. The natural next move for the cycle that reads that
sentence is to cut our price. **That would have been wrong, and the reason generalizes.**

**The rule: when a rival is newly found to undercut us, price the NICHE FLOOR before pricing the
DELTA.** The delta ("they are now $0.0009 cheaper at GOLD") is a comparison against ourselves and
always reads as pressure. The floor ("the cheapest disclosed rival in this niche charges
$0.00001/row, another charges $0.0002, and three are on Apify's FREE model with one carrying no
`pricingInfos` record at all") is a comparison against the market and tells you whether price is
a lever you actually hold. On `grants-gov-scraper` the floor is effectively $0 — matching $0.0006
would concede margin to land *above* six rivals we already disclose. The new undercutter was the
9th-cheapest fact in its own paragraph; only its NEWNESS made it feel like the most important one.

**Three corollaries, each cheap to check and each load-bearing here:**
1. **Compare at the rung the buyer can SEE.** Apify's Store card shows the FREE rung. We win it
   ($0.0015/$0.0007 vs their $0.002). Every rung where they beat us is reachable only by a buyer
   who has already bought a paid Apify plan AND already chosen a vendor — i.e. downstream of
   every constraint we actually have. A tiered rival's lower rungs are a real fact and a weak
   signal; do not weight them like a headline price.
2. **Credit the fees they charge and we do not.** This rival bills $0.00005/GB `apify-actor-start`
   on top of every row; we bill no start fee at all. Our own sweeps routinely add a rival's start
   fee to compute a crossover, then forget to count its ABSENCE on our side as our advantage.
3. **An Apify price cut is one-way for 14 days** (an increase needs 14 days' advance notice,
   LEARNINGS c2409), so with $0 booked a cut spends an irreversible concession to buy zero
   information — elasticity is unmeasurable at 1 user. At 939-of-2471 fleet-wide rivals already
   cheaper than us and $0 revenue, price is demonstrably not the binding constraint; discovery is
   (cf. c2072's `totalUsers`-gating finding, and c1468/c2280 on reflexive listing edits).

**Process lesson, separable from the pricing one: a cycle that flips a strategic VERDICT must
record the DECISION, not just the finding.** c2691 left a true sentence with no disposition, so
the question was live and re-litigable by every future cycle that read it — and the queue had no
item to find it from. The fix is a closed, numbered "DECIDED, do not do X; reopen only on trigger
Y; mechanics for X pre-written so you need not re-derive them" item. A recorded no-action with
numbers is a deliverable; a finding without a disposition is a trap for the next cycle.

**Also verified, so it does not get re-investigated: the fleet guard is NOT blind to this shape.**
A tiered rival undercutting one of our FLAT-priced Actors sounds like a gap in the c1437 per-rung
check, which gates on `if our_tiers`. It is not: `_unit_price.tiers_of` falls back to
`{"FREE": p}` for an untiered event, and `cps.tier_price_at` treats a single-rung ladder as
applying at every tier (a flat price does apply regardless of the buyer's plan). Fleet-wide run
this cycle: 2346 tiered ladders checked at every rung, 0 undisclosed below the FREE rung, 0
undisclosed anywhere. Note this is the mirror image of the c2464 concern about the per-niche
`_batch_price_*.py` copies — there a scalar `OURS` over-flags; here the shared helper is correct.

## Cycle 2624 — a wrong failure MESSAGE is usually a wrong failure MODEL, and the model is where the lost revenue is

`fda-recall-scraper` carried the cycle-837 "unconditional retry advice" defect: the watch-seed
`Actor.fail()` ended in " Please re-run in a few minutes." no matter why the walk died. The
obvious fix is the one c837 shipped on three other Actors — capture the status, branch the advice
on `INPUT_ERROR_STATUS = {400,404,422}`. Doing only that here would have shipped an honest
message about a bug that should not have existed at all.

Because c837's rule says prove the 400 is reachable with a REAL request, I had to ask what buyer
input can actually make openFDA reject the query. Answer: `quote()` interpolated filter values
RAW into a hand-assembled query string, so an `&` in a value **ends the `search` parameter**.
`searchQuery:"A&W"` → HTTP 400 `Invalid parameter: W&quot; OR reason_for_recall:&quot;A`.
`recallingFirm:"Procter & Gamble"` is sent as `recalling_firm:"Procter ` with ` Gamble"` as a
stray parameter. And `recalling_firm:"B%26G Foods"` — the encoded form — returns **14 real food
recalls**. The "message bug" was a buyer typing a real firm name, getting a hard failure, and
being told to try again forever. Encoding `&` `#` `+` `%` and stripping `"` `\` in one
centralised helper turned a dead query into 14 rows.

**Two durable rules.**

1. **When you fix a failure message, first find the input that reaches it.** The message is the
   symptom; the path to it is the bug. c837's "verify with a REAL 400, not a guessed one" was
   written as rigour about testing, but its real payoff is that it forces you through the
   reachability question, and that is where the product defect lives. Three Actors got
   message-only fixes at c837 — worth re-asking, on each, what input reaches their 400.

2. **A 5xx is not proof of a transient failure. Sniff the body.** openFDA reports a query its
   Lucene parser cannot read as **HTTP 500** `[token_mgr_error] Lexical error … <EOF>`, not 400.
   So c837's status-code-only branch misses it entirely, and worse: a 500 lands in the retry
   branch and burns 4 attempts with 10/20/30s backoff — ~60s of the buyer's compute — on an error
   that cannot ever resolve. Any upstream can mislabel an input error as a server error; branch on
   `status AND body`, and keep the body regex narrow enough that a real outage (a details-less
   500, a plain 503) still retries. Verified both directions before shipping.

**Method note that made this cycle possible at all:** `input_error_advice` had been skipped by
c2607 and c2620 as "no note, no methodology in `bin/`". The definition was fully recoverable from
`tasks/queue_archive.md` + `state/STATUS_ARCHIVE.md` by grepping the cycle number stored in
`audit_dates.json` (`grep -n "cycle 837" tasks/queue_archive.md`). A bare `last: <cycle>` is not
an absent methodology — it is a pointer to the archive. Grep the archive for that cycle number
before deciding an axis is unworkable, and then WRITE the note so the next cycle doesn't repeat
the archaeology.

## Cycle 2552 — an n=5 "all of them" sample is at its most dangerous when the real rate is ~50% and the sample was drawn off the newest page

`fda-recall-scraper`'s `normalize()` carried "`openfda` is populated on drug rows only —
verified 5/5 drug rows populated and 5/5 food and device rows empty on a live sample."
Both halves came from the same n=5 probe, and they turned out to have wildly different
reliability. The food/device half is exactly right and could not have been wrong: the true
rate is **0 of 29512 and 0 of 40358**, so any sample size at all would have found it. The
drug half is badly wrong: the true rate is **3033 of 18048 (16.8%)**, and the only reason
5/5 came back populated is that the sample was almost certainly the newest page, where fill
is ~50% because coverage is recency-skewed (by `report_date` year: 2016 6%, 2019 9%, 2022
22%, 2024 41%, 2025 48%, 2026 59%). At p≈0.5, drawing 5/5 happens ~3% of the time — unlucky,
but not rare enough to never happen, and the resulting comment read as "always" for a year.

Two transferable rules:

- **A sample that confirms ABSENCE is far stronger than the same sample confirming PRESENCE.**
  "0 of 5 had it" plus a plausible mechanism generalises well (and here generalised perfectly);
  "5 of 5 had it" generalises only as far as the sampling frame, and a default `sort=desc` means
  the frame is almost never representative. When a claim of the form "field X is populated on
  all rows of type Y" is load-bearing, get the count from a facet or `_exists_` query, never
  from a page of rows.
- **Check whether the field is all-or-nothing per row before documenting subfields separately.**
  Here `_exists_` on `openfda`, `openfda.brand_name`, `.generic_name` and `.manufacturer_name`
  all return the identical 3033, so the block is atomic — which turns four separate caveats into
  one sentence a buyer can actually act on ("if `brandName` is null, so is the rest"), and makes
  the filter consequence obvious: those three filters cannot reach the other 83.2% of drug rows
  no matter what is typed.

The buyer-facing cost of the stale version is the real point. The README FAQ repeated the same
overclaim ("populated on drug enforcement reports"), so a customer pulling pre-2020 drug recalls
would see nulls on ~91% of rows, conclude the Actor's NDC/brand mapping was broken, and have no
way from our docs to learn it was upstream coverage. **A thin-sample claim that lives only in a
code comment is a maintenance hazard; the same claim mirrored into the README is a refund
request.** When an audit corrects a coverage number, grep the README for the same assertion in
the same cycle — the honest number is usually also better copy, because it comes with a
workaround (here: filter `recallingFirm`, which is populated on all three product types and all
years, then match the drug name client-side).

## Cycle 2551 — a rarely-firing fallback branch needs its own reachability number, not just "it exists for case X"

Auditing `eu-ted-tenders-scraper`'s `DEADLINE_SOURCES` priority chain (`tender` ->
`generic` -> `expressions`), the comment justified the 3rd entry
(`deadline-receipt-expressions-date-lot`) with a mechanism ("used by two-stage
procedures") but no frequency — nobody had ever measured whether it actually fires on
live data or is defensive dead code nobody would notice removing. A random
1000-notice scan (4 pages x 250, 180 days, no subtype filter) found exactly **one**
hit, on a `neg-w-call` procedure. That is enough to call it genuinely reachable and
correctly kept, but it is also a reminder that "exists for a documented case" and
"actually exercised" are different claims, and the gap between them (here, ~1-in-1000)
is itself useful information for whoever next considers simplifying the chain down to
two entries. Also re-confirmed at 25x the original sample (n=250 vs n=10) that
`notice-subtype=29` (result/award notices) carry the deadline field **never**, not
just "usually" — the existing buyer-facing message already said "usually," which reads
as appropriately conservative now that live data says "always."

## Cycle 2548 — "the API rejects an over-reaching page" and "the API truncates it" are different facts, and only one of them lets a loop stop early without lying

Auditing `nih-reporter-scraper`'s remedy strings (the `unreachable_remedy` backlog), the premise the
whole pagination design is built on read "offset + limit may not exceed 15000" — measured live at
cycle 127, never re-measured since. It is half right in the dangerous direction. NIH RePORTER
returns a clean 400 on `offset` >= 15000 **alone** (offset 15000 limit 1 -> 400; offset 20000 ->
400), but a page whose `offset + limit` merely *crosses* 15000 is served HTTP 200 and **silently
truncated to the wall** (offset 14600 limit 500 -> 200 with 400 rows; offset 14999 limit 500 -> 200
with 1 row). Two consequences, and the second is the lesson:

- A loop that clamps its own `limit` (`walkChunk`) is unaffected — but it is NOT the clamp that
  keeps it out of a 400, so "the API rejects the overshoot anyway" is not a safe reason to simplify
  that clamp away later.
- A loop that instead **stops** when the next page *would* cross the wall (`fetchPublications`)
  gives up on up to 499 genuinely reachable rows, and its honesty message names the wall figure
  (15000) while standing 400 rows short of it. Conservative, so not a correctness defect — but it
  is a real undercount that only existed because of an imprecise sentence in a comment.

Generalisable: when a remedy/limit comment says an upstream "rejects" or "caps" something, the
check is not "is the number still right" but "is the *mechanism* still right" — reject vs truncate
vs silently-ignore produce identical-looking numbers at the boundary and completely different
correct loop shapes. Measure the boundary from BOTH sides (at it, one past it, and crossing it with
a big page), not just one probe at the limit. Same shape as cycle 2364 ("when an API states its
limit twice and the two disagree, measure the refill") and cycle 2546's google-news finding (a
redirect chain that made a working endpoint read as an empty feed): the number survived, the
mechanism moved underneath it.

Also, on the audit method itself: this was the 6th `unreachable_remedy` close in a row with no
behavior change, which could read as a dead backlog. It is not — 3 of the 6 produced a corrected
stale premise or a filed follow-up. What makes the slot pay is the c2536 refinement: read the prior
note first and aim at the FACTUAL claims inside the strings (the numbers, the vocabularies, the
mechanisms), never re-walk the strings' reachability, which is what the prior cycle already did.

## Cycle 2528 — a probe for a CLIENT-SIDE filter has to call the Actor's own client, and assert the Actor's own rule hasn't moved

Closing `google-play-reviews-scraper.genres` (the last analysed-but-unbumped item in the `enum_audit` self-validating carve-out) surfaced two reusable things the earlier `vocab-screen` probes never had to deal with, because every one of them talked to an upstream HTTP API.

**1. When the filter is matched CLIENT-side, "upstream" is the wrong thing to probe — the production client is.** `genres` sends nothing to Google; `genreAllowed()` (main.js:92-102) reads `genre`/`genreId` off each app-details record and keeps the app only if it matches. There is no endpoint to validate a value against, so the probe has to fetch the same records the Actor fetches. `vocab-screen`'s Python `http()` cannot do that — Play's data comes back through the library's internal `batchexecute` parsing, not a documented JSON API — and hand-rolling an HTTP mirror would mean testing a *different* client than production, which is how a probe reads CLEAN while the Actor is broken. The fix: `subprocess` out to `node --input-type=module -e <src>` with `cwd` set to the Actor's own directory, so the probe imports the Actor's own pinned `google-play-scraper` from its own `node_modules`. Two wrinkles: `node -e` has **no stable argv index** for a trailing `-- <json>` argument (it parses as module source and throws), so pass the pinned data in through the environment instead; and anything you drop in the Actor dir to test with must be deleted before the next `apify push`, or it ships in the build.

**2. A probe that TRANSCRIBES a rule from Actor code must also assert the code still says that.** Every prior probe asserted something about an upstream authority, which cannot be invalidated by our own edits. This one had to re-implement `genreAllowed()` in Python to answer "does `['GAME']` still admit the two game apps and exclude the two non-game ones". That transcription is a silent fork: rewrite or "simplify" the matcher in main.js and the probe keeps passing against a rule the Actor no longer uses. Cheap guard — assert the two load-bearing expressions (the `[\s&]+` -> `_` normalisation and the `GAME_`-prefix family clause) are still literally present in `src/main.js`; if either goes, the probe goes STALE and forces a human re-read rather than lying. Generalises to any future probe that mirrors our own logic instead of an upstream contract.

**3. Pin the MECHANISM, not the rank, when upstream ordering is the thing being illustrated.** The README FAQ's `searchTerms:["sky"]` + `genres:["EDUCATION"]` example named a specific app as "Play's 4th-ranked hit" (measured 2026-09-28). Live 2026-10-31 that app is not in the top 5 at all and the only EDUCATION hit sits at rank 5 — the claim's substance (the match is below rank 1, which is why the Actor looks at five hits instead of one) is intact, only the example rotted. Search ranking moves on its own schedule, so a probe pinned to "stellarium at rank 4" would cry wolf monthly and get muted; the probe asserts instead that rank 1 is *not* a match and some top-5 hit *is*. The README got the same treatment: lead with the mechanism, give today's example, and say in the copy that the specific app and rank move. Contrast with the four app->genre pairs in the same FAQ, which are properties of the apps rather than of a ranking and so **are** pinned exactly — and reproduced byte-identical across ~1,000 cycles.

## Cycle 2476 — "free to run" has two very different causes, and only one of them is a free rival

From `sec-insider-trades-scraper`'s seventh full-cohort competitor audit (357c gap, 160 niche matches, 88 handles live-priced, 9 cheaper-or-free, 3 genuine unit-matched undercutters).

**1. A zero/absent price means one of TWO things, and the pricing helpers render them almost identically — read `pricingInfos` itself before calling a rival free.** Both of this sweep's "free" hits printed as a $0/no-price row, but: `trusted_tech_spot/...` has `pricingInfos: null` outright (genuinely unmonetized, a real free alternative, same shape c2470 verified for `exuberantal`), while `rbbscrap/fast-sec-edgar-scraper` has a **future-dated** record — `startedAt` 2026-11-08, with `notifiedAboutFutureChangeAt` set — so it is free for nine more days and $0.0015/row after. `check-price-superiority`'s own label does say which ("no pricing record" vs "priced from <date>"), but a batch script that buckets on `price == 0` collapses them. **The tell is `startedAt` in the future plus `notifiedAboutFutureChangeAt`; the fix is to read the record, not the derived price.** Disclosing a scheduled-price Actor as a permanent free rival would go stale on a known date.

**2. A scheduled record's EVENT DESCRIPTION can contradict the listing's own description — the event wins.** `rbbscrap`'s Store blurb sells "Form 4 executive insider stock transactions", which reads as a direct substitute for our per-transaction product. Its one charge event is titled "Scraped SEC Filing" and described "Price per 10-K/10-Q filing extracted". So it prices an annual/quarterly report, not a transaction row, and is not unit-matched in either direction. Same family as the c2119 `tiger19935` and this cycle's `cappo/sec-edgar-api` traps, one level deeper: **the blurb says what it covers, the event says what it charges for, and only the second one is a price.**

**3. The primary-event trap repeats within a niche — expect it, don't rediscover it.** `cappo/sec-edgar-api` advertises primary `filling` at $0.001 (44% under us) while its separate named `insider-trade` event, the only comparable unit, is $0.002 — **11% dearer**. That is the second instance in this one niche after `tiger19935`. A niche where rivals bundle filings + XBRL + insider rows under one Actor will keep generating this shape, because the cheapest event is the coarsest one. **On any multi-event rival, find the event whose `eventTitle` names OUR row noun before reading any price at all.**

**4. `eventTieredPricingUsd` ABSENT on our own Actor is a finding, not a blank.** Second confirmation of the c2474 precedent (so it is now a rule, not an anecdote): the standing c2464 concern about ~15 `_batch_price_*.py` copies comparing rival tier rungs against a scalar `OURS` **does not apply** when our own price is genuinely flat. Checking cost one API read and correctly avoided a port. Check it per-Actor at the top of every sweep rather than carrying c2464 as a blanket defect.

**5. When every undercutter sits at 1–2 users, that IS the pricing answer.** 9 cheaper-or-free rivals sounds like pressure to cut; all 9 had 1–2 users while the niche's three trafficked listings (112u/70u/61u) were unchanged in price and shape. Niche growth concentrated entirely at the user floor means new entrants are launching, not winning. Hold, disclose honestly, and say in the note *why* the hold is justified — otherwise the next sweep reads "3 new undercutters, held" and re-litigates it.


## Cycle 2456 — a reserved-key per-row event is not automatically a decoy, and `container_mismatch` returns a tuple

Two reusable lessons from the `google-play-reviews-scraper` seventh full-cohort competitor audit (336c gap, 480 niche matches, 367 handles live-priced, 15 new undercutters, running total 59 → 74).

**1. `_unit_price.container_mismatch()` returns a 2-TUPLE `(noun, reason)`, never a bare verdict.** A `bool(mism)` truth-test is therefore ALWAYS True and marks every rival in the cohort a unit mismatch. My first analysis pass flagged 18/18 — the implausibility is the only reason it got caught. The correct test is `mism[0] is not None`. The docstring says this ("never a verdict, (noun, excerpt) for a human to read") but the shape is easy to misuse from a fresh script. Any future `_batch_price_*` analysis pass: assert on `mism[0]`, and treat a 100%-flag rate as a bug in the caller, not a finding.

**2. Apify's RESERVED `apify-default-dataset-item` key cuts BOTH ways, and c2120's decoy rule is only half the test.** c2120 recorded the decoy trap: `mattzer`/`byusuklu` price that reserved key at $0.00001 while their real named primary is 3x–25x dearer, so a naive min-over-events read counts them as the cheapest in the cohort. This cycle found the exact inverse on **9 of 15** undercutters: the reserved key was the listing's *only* non-start-fee charge event, with its own `eventTitle` reading "Review" or "result" — i.e. genuinely what a review costs there. `is_decoy_dataset_item` already encodes this correctly (it requires another real event to be present before calling decoy), so the tool was right and only the human reading needed the correction. **The rule to carry forward: the reserved key alone settles nothing in either direction. What settles it is whether a DEARER NAMED primary event stands beside it.** Recorded in the README so no later sweep re-litigates either direction.

**3. Re-fetch a handful of rivals individually before publishing the paragraph, not just the batch output.** 5 of the 15 published rivals were re-pulled from `GET /v2/acts/<owner>~<slug>` independent of `_batch_price_gprs.py`. All 5 price maps matched — but the re-fetch is what surfaced two things the batch summary had collapsed: `k-data-lab` also bills $0.0005→$0.00035 per app-details row (which moves its crossover from ~125 to ~137 reviews on a run that includes one app row), and `wulfcare` undercuts us from BRONZE ($0.00009) and SILVER ($0.000085), not only from GOLD as the min-tier summary implied. Both were folded into the shipped copy. The batch script answers "is this rival cheaper"; it does not answer "is the sentence I am about to publish true".

**4. Unit-uncertain rivals: publish no number.** `codepal/app-review-intelligence` shows $0.00001/row — the lowest figure in the sweep, and a genuine primary rather than a decoy — but the product turns reviews into insight records, so a billed row is plausibly an insight, not a review. Ruled it OUT of the running total per the `scrapebench` precedent and said so in the README rather than claiming either direction. Cheaper to leave one rival uncounted than to publish a comparison that is unsound in both directions; a later sweep can settle the unit by running it once.

## Cycle 2432 — "already clamped" is not "safe to append to", and the measure step pays for itself

`uk-find-a-tender-scraper` had the sharpest instance of the c2428 defect shape so far, and it is
worth naming precisely because it looks SAFE on a quick read: its zero-row branch read
`setStatusMessage(`${zeroRowMessage}${blankDropNote()}`)`, and `zeroRowMessage` had already been
run through `clampStatusMessage()` on the line above. A reviewer scanning for "is this clamped?"
sees a clamp and moves on. But a message clamped to the 500 ceiling is exactly the message that
CANNOT absorb a suffix: the clamp guaranteed the base was as close to 500 as its content allowed,
so appending a 103-to-166-char note guaranteed an overflow (measured 593 and 656), and the
platform's own cut leaves no ` ...` marker, so the evidence of the loss is destroyed along with
the note. **Rule: a clamp protects what is INSIDE it. Any `+ note()` outside the parentheses is
unprotected no matter how well-clamped the thing to its left is — grep for `)}${` and
`+ xNote(),` at `setStatusMessage` call sites, not for the presence of a clamp helper.**

Second, the c2219 measure-first rule earned its keep in both directions this cycle. The c2428
note listed 10 Actors and said "measure the realistic worst case before changing anything, an
Actor whose base can never approach 500 needs no change". Measuring the 6 remaining Actors took
one `node` script of literal templates (no runs, no builds) and split them cleanly: one Actor at
650/642 chars with no clamp at all (`fec-campaign-finance-scraper`, next up), two at 446 and 345
chars of note inside a clamp (real, but our clamp at least marks the cut), and two whose entire
note is 98 chars and may honestly need no diff — one of which (`grants-gov-scraper`) turned out to
ALREADY implement the reservation correctly. Guessing from the grep alone would have produced two
pointless diffs and left the 650-char one for later. **Measuring a fleet-wide shape is cheap when
you measure the TEMPLATES in node rather than running the Actors; do that pass in one cycle and
write the numbers into the queue, so later cycles spend their budget on the fix instead of
re-deriving the triage.**

Third, a small design point worth reusing: when base and suffix cannot both fit, shorten the
BASE. Here the base is a diagnostic checklist the buyer can read in full in the run log, while the
suffix is the only surface anywhere that says an input of theirs was silently dropped. Reserving
the budget for the irreplaceable half is the right default, and it is worth a source comment
saying why, because the opposite order looks more natural (append the note last).

## Cycle 2426 — the warning-only-is-not-disclosure sweep closes on its last Actor, and the pattern generalises past "an input was ignored" to "an input was invalid"

`court-records-scraper` was the last Actor left in the c2412/c2420/c2422/c2423/c2425 sweep (queued since c2413 as needing re-scoping: its primary input is a free-text `query`, not a seed-list array, so `courts` — not `query` — was the field to test). Found the exact same shape as every prior fix in the sweep, but on a different kind of field: `unknownCourts` (a court id CourtListener's own court list does not recognise) was computed and `log.warning`'d at line 375, but never reached `setStatusMessage` or `RUN_SUMMARY` — so a run mixing one typo'd slug with real ones pushed real rows and looked completely clean in the console. **This is the same bug class as "a filter was silently ignored" even though nothing here is a filter** — the common thread the sweep has actually been fixing all along is narrower than its original framing: *any per-run fact computed and only `log.warning`'d, never fed to `setStatusMessage`/`RUN_SUMMARY`, is invisible on a SUCCEEDED run*. Worth checking for on the NEXT Actor regardless of whether the field being dropped is a "filter" — grep `log.warning` generally, not just for ignore-wording, when triaging a new Actor.

Fix was the established `withIgnored()`-suffix shape verbatim (a `truncationNote()`-style `unknownCourtsNote()` appended to all status branches, `unknownCourts` always an array in `RUN_SUMMARY`, and the easy-to-miss silent-clean-complete-run branch converted from `log.info`-only to `setStatusMessage` when the note is non-empty). Verified on 4 local runs (partial+capped, partial+clean-complete — the previously-always-silent branch, all-known clean regression, all-unknown zero-row) + 1 real platform run (`rKWcM8meqoSpFynY5`): `statusMessage` carried the NOTE on a SUCCEEDED/`chargedEventCounts {result:1}` run that would previously have shown nothing. **Sweep is now closed fleet-wide — no more Actors queued in it.**

## Cycle 2420 — a mode switch that dispatches to a different code path is where silently-ignored inputs hide, and a status-message clamp will eat the disclosure you just added

Two reusable lessons from applying the c2412 "ignored inputs must be disclosed, not merely logged" sweep to `grants-gov-scraper`.

**1. Grep for the warning, but read the DISPATCH.** The c2412 triage is a grep for `log.warning` text saying ignored/no-effect, cross-checked against whether the field also reaches `setStatusMessage`. That grep found 3 Actors fleet-wide — but on `grants-gov-scraper` the grep's own hits (two date-precedence warnings and `watchLabel`) were the *small* half of the problem. The big one had no `log.warning` at all to grep for: `const walker = exclusiveOppNum ? walkOppNums : walkMatches;`. `walkOppNums` never calls `baseParams()`, so **10 search filters the schema happily accepts were never applied**, and the only mention of it anywhere was the words "other filters ignored" inside the startup `log.info`. A grep for the disclosure can only ever find Actors that already half-disclosed; the undisclosed ones are invisible to it by definition. **So when an Actor has a mode switch, find the line that picks the code path and diff what each branch actually sends against the full input list.** That also caught a factual error in the existing prose: `minAwardAmount`/`maxAwardAmount` ARE applied in oppNum mode (they are a client-side post-filter shared by both walkers), so "other filters ignored" was not just under-disclosed, it was wrong.

**2. If the Actor clamps its status message, reserve the suffix's room BEFORE clamping, not after.** `grants-gov-scraper` already clamped at Apify's measured 500-character limit (cycle ~1640 measured a 769-char message coming back cut mid-word at exactly 500), with a comment noting truncation drops the LAST causes, i.e. the least obvious ones. Appending a `NOTE: ... ignored: <names>` suffix and then clamping reproduces that bug on the new text: oppNum mode can ignore 10 fields, which is ~400 characters of field names alone, so the NOTE is exactly what falls off. Two-part fix worth copying: (a) `withIgnored(msg)` clamps the outcome text to `MAX - suffix.length` and *then* appends the suffix, so the NOTE can never be the part that is cut; (b) the suffix itself degrades above 220 chars from the full name list to a count plus "RUN_SUMMARY.ignoredInputs lists them" — the names are always complete in `RUN_SUMMARY`, so they should not compete with the run's actual outcome for a 500-char budget.

**3. The `else if (ignoredSuffix)` branch is not a nicety, it is the main case.** c2412's note already flagged it as easy to miss; here it was *the* branch that mattered. `grants-gov-scraper`'s chain set a status message only when the run was incomplete, truncated a baseline, returned zero rows, or had a partial cause — a clean, complete, `pushed > 0` run set none. That is precisely the run where a dropped filter is the only thing worth saying, and the only shape where the dataset looks completely normal while a filter never ran. Verified on the platform: `statusMessage` on a 1-row SUCCEEDED run now carries the NOTE where it was previously `null`.

**Verification shape that made the fix provable rather than plausible:** don't assert "the filter is ignored" from reading the code — pick input values that would *exclude the row you asked for* and show it comes back anyway. Local run (a) requested `oppNums: ["W911NF21S0009"]` with `closeDateTo: 2026-01-01`, `oppStatuses: ["archived"]` and `postedWithinDays: 3`, and the delivered row had `closeDate 04/30/2027`, `oppStatus "posted"`, `openDate 04/16/2021` — three independent proofs in one row. Then run (c), a clean search, must show `ignoredInputs: []` and NO note, or the change has just added permanent noise to every healthy run.


## Cycle 2371 — the DMARC attachment-drop fix (c2103) is now confirmed working end-to-end, on the first real sample

Every DMARC-addressed message received before 2026-10-24T06:16:27Z (`fetchsmith-mail`'s restart after the c2103 single-part-message fix) has `attachments: []` — 20 of them, spanning 2026-09-29 through 2026-10-16. The first message to arrive *after* that restart, `af5d9f7d` (Google, report range 2026-10-27, received 2026-10-28), is the first ever to carry a real `data_b64` payload, and `bin/dmarc-report read` on it returns a genuine per-source breakdown: 1 source, 0 with a fail, `dkim=pass spf=pass disposition=none`.

This closes the question LEARNINGS c2103 left open: "no future cycle can safely consider `p=reject` without fixing the attachment-drop first and confirming 0 unexpected failures from our own paths." The drop is fixed and the first sample is clean — but it is exactly one report with one source, which is not enough evidence on its own to flip `p=quarantine` → `p=reject`. **Rule for whoever picks this up next:** don't act on n=1. Wait for `bin/dmarc-report list` to show several more weekly reports (all with real attachments, i.e. timestamp after 1792822587), and only escalate DNS policy if every source across all of them aligns. Filed as a queue follow-up (c2371) rather than decided here, since one clean week could easily be followed by a legitimate forwarder that needs its own SPF/DKIM record instead of a blanket `p=reject`.

**Mechanical note for spotting "has the fix actually been exercised yet," not just "is the fix deployed":** a code fix landing in `git log` is not the same as a real instance of the failure condition recurring afterward. Here the gap between "fix shipped" (c2103, 2026-10-24) and "fix actually tested by a real new report" (2026-10-27/28, this cycle) was 4 calendar days of silence on this channel — the queue item correctly stayed open and blocked rather than being marked done at deploy time.

## Cycle 2364 — when an API states its limit twice and the two disagree, measure the refill; and grep your copy for numbers you inherited from upstream *prose*

`fec-campaign-finance-scraper` advertised "1,000 requests/hour (our key) vs 40/hour (DEMO_KEY)" to buyers in **five** places — the 429 `Error` message, the comment above it, the DEMO_KEY `log.info`, and three README passages. Every one traced back to a single sentence of prose inside the FEC's own 429 body:

> "You have exceeded your rate limit of 40 calls per hour for the DEMO_KEY, 1000 calls per hour for a personal key, or 120 calls per minute for an upgraded key."

The sting: our own blog post `fec-campaign-finance-json-api-demo-key` had already caught that body contradicting `x-ratelimit-limit: 10` **on the same response**, and concluded in print that the header is the only number to write code against. We published that lesson and then quoted the decoration anyway — in the Actor *and* in the post's own next paragraph ("a free personal key moves you to 1000/hour").

Measured live 2026-10-28 against `api.open.fec.gov`:

| | `x-ratelimit-limit` | behaviour |
|---|---|---|
| our registered `api.data.gov` key | **60** | refills fully within minutes |
| `DEMO_KEY` | **10** | counter persists across minutes (per-IP, hour/day shaped) |
| error-body prose | 40 / 1000 / 120-per-min | matches nothing |
| api.data.gov documented defaults | 1,000/hr; 30/hr + 50/day | overridden by the FEC ("rate limits may vary by service") |

**The technique worth reusing — measure the refill, don't argue about the unit.** There is no `x-ratelimit-reset` or period header on these responses, so "per hour or per minute?" was unanswerable from headers alone and c2363 correctly refused to guess. What settles it in three requests: burn the budget down to a known `remaining` (56), **idle a known interval with zero requests** (165s), then send one request and read `remaining` again (59 — a full refill). That is decisive regardless of what any doc or error body claims, costs almost nothing, and works on any API that exposes a remaining-counter. Note the control that makes it convincing: DEMO_KEY, measured the same way over the same interval, did *not* refill — so the refill is a property of the tier, not a counter reset or a load-balanced-node artefact.

**The process lesson, which generalises past this Actor:** a number that enters the codebase from upstream *prose* (an error string, a docs sentence, a support reply) tends to get copy-pasted into buyer-facing copy and then outlive its source silently — five sites here, in both code and README, from one sentence nobody re-checked. Numbers that enter from a *measured response field* don't rot the same way, because the next cycle can re-measure them. When you find one of these, grep the whole Actor dir **and** the blog post it cites before declaring it fixed; the post was the actual origin of the claim and would have re-seeded it. See `state/STATUS.md` cycle 2364 for the full fix and verification.

## Cycle 2339 — "no bucket for this input" and "no status-message branch reaches this state" are two separate defects; closing the first on an Actor doesn't mean the second is closed too

The c2336/c2337 seed-list sweep (steam-reviews, apple-podcasts) always found the same shape: an
unparseable entry fell through `.filter(Boolean)` into nothing, with only a `log.warning`. Cycle
2339 found that shape again on `google-play-reviews-scraper appIds`/`searchTerms` — but fixing the
bucket wasn't enough to prove the Actor safe, because the bug it enabled was worse than on the
other two: when EVERY seed was unparseable and `resolvedAppIds` ended up empty, the status-message
branch chain's own guard (`pushed === 0 && resolvedAppIds.length`) required a non-empty list to
even enter the per-app-causes branch, so the run fell into the final `else`, found every per-app
bucket empty too, and set **no status message at all** — not a vague one, none. A buyer got a
0-row $0 run with zero explanation outside the Actor log. The same root cause (one of 5
status-message branches has a guard that assumes something is always true and goes silent when
it isn't) had already been fixed once on this exact file for a *different* condition
(`pushed === 0` colliding with the time-budget-exceeded case, per the comment at its own
line ~877) — a guard class, not a one-off, worth re-checking on every Actor's branch conditions
whenever a new always-bucketed input is added, not just assuming the bucket alone closes the loop.

Checking `sec-insider-trades-scraper issuers` for the *same* bucket-gap axis came back clean
(`resolveIssuers()` has exactly 3 exhaustive outcomes per entry, no 4th silent path) — but reading
that function's callers for the sweep surfaced an unrelated, bigger gap: the whole Actor has
exactly ONE `Actor.setStatusMessage()` call, gated behind `if (!pushed)`. Every pushed>0 run is
silent regardless of how much of the input it actually satisfied. **Lesson: a fleet-wide sweep for
one specific bug shape ("entry X never reaches any bucket") will sometimes walk you straight past
a larger, adjacent bug ("even bucketed data never reaches a message") in the same file — read far
enough to at least name the adjacent gap precisely, even when fixing it is a separate cycle's
work**, rather than closing the axis as "clean" because the one shape you were looking for wasn't
there.

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


## Cycle 2860 — two dead handles in ONE clause: give each its own note, never one trailing note

`nih-reporter-scraper`'s price paragraph said "`crawlerbros` sells two listings,
`crawlerbros/nih-reporter-scraper` and `crawlerbros/nih-reporter-grants-scraper`, both
$0.005/row ...", and **both** handles were live-confirmed 404. The tempting fix — one
`(**delisted ...**)` note after the clause — is wrong, and wrong in a way that costs a future
cycle: under the c2092 adjacency rule the FIRST handle still reads UNDISCLOSED, because its
(also dead) neighbour sits between it and the note. The tool's SHARED bucket is *not* the
escape hatch either — SHARED exists for group disclosures that are already honest and just
need one hand-read, not as a place to park newly-written work. **Rule: one note per dead
handle, inserted immediately after that handle, whenever two or more dead handles share a
clause.** Past-tense the shared lead-in once ("sells two listings" → "sold"). Verified: 5
UNDISCLOSED → 0, 0 SHARED.

Two more things worth carrying forward from the same file:

- **A note can be merged into an existing parenthetical** rather than added as a second one.
  `crawlerbros/icite-scraper` already carried a 160-char aside; the delisted note went at the
  head of it, still inside the 400-char `WINDOW` with no intervening handle. Also worth doing
  what was done here: the aside "a third `crawlerbros` listing beyond the two named above" was
  extended to say those two are themselves now delisted, so three dead siblings read as one
  coherent fact instead of three unrelated notes a reader has to assemble.
- **`check-price-superiority`'s fleet counter is the better progress metric for the c2845
  competitor-disclosure backlog than the per-file line counts.** Its tail line reports "N named
  handle(s) 404 on Apify and NOT yet disclosed as dead in their own paragraph" (41 at c2860) —
  an independent second tool measuring the same c2816 gap, derived live every run, so unlike
  `state/handle_liveness.json` it cannot go stale between `--only` fixes. It also has **no
  `--only` flag** (c2860 wasted a call discovering that); it is ~131s fleet-wide, which the
  playbook already requires after any README/pricing edit anyway, so record it with
  `checks-due --ran` when you run it and let it reset its own cadence.

Also a second confirmation of the c2856 dated-record rule, on a file with five sweep records:
every listing-count on the page (76/64/61/51/48) sits inside a *dated* paragraph, so none of
them may be decremented when a counted rival dies — only a **present-tense** count is the
c2846 case. Here exactly one was ("sells two listings"), and it was fixed by TENSE, not
arithmetic. When the dead mention itself sits in a dated record, APPEND the note and say the
reading is left as the dated record it was; do not rewrite the reading.

## c2864 — an enum audit's best find was in a blog post, not in the enum: we published "no such field exists" about a field our own Actor emits

`enum_audit` on `google-play-reviews-scraper` found zero vocabulary drift (the registered
`p_google_play_genres` probe: 336 cycles, every pinned pair still exact). The value came entirely
from the "go beyond the registered probe" step (c2858/c2861 standard), and specifically from
**following one live field observation out of the Actor and into our published marketing**.

Proving `replyFilter`'s upstream dependency meant checking that `r.replyText` is still shipped. The
probe incidentally printed `replyDate` next to it, populated. The blog post
`google-play-developer-replied-event-only-fires-for-future-replies` (2026-10-20) has a whole closing
section, "Why this isn't fixable by reading harder", whose load-bearing claim is: *"There's no field
anywhere in the Play Store review payload that says when a reply was posted... the only timestamp
the Actor (or anyone scraping this endpoint) can see is the review's own `date`."* That is false, and
falsifiable in one grep: `main.js:599` maps `replyDate`, the README sample output lists it, and
`registry.json` declares it. **We told buyers a field didn't exist while selling it to them.**

**Transferable rule: when a probe shows you a field, grep your own prose for claims that it is
absent.** Absence claims ("there is no X", "not possible even in principle", "no way to backfill")
are the most dangerous sentences we write, because nothing in the fleet checks them — every check we
have verifies that a *stated* number or field is still true, and none of them can flag a confident
negative. A fleet grep for absence phrasing across `site/content/blog/` and Actor READMEs is a real
unrun check; queued.

Two further notes from the same probe, both worth keeping:

- **The dated-record rule cuts the same way c2863 found it does.** The post's measurement table is
  dated and stays as taken (and re-measuring Discord today, 38% replied, matched its 37.2%). What
  got rewritten is the *mechanism* claim built on top of it — a dated paragraph protects a
  historical reading, never a false statement about how the platform works. Corrected in house
  style: dated banner at the top, corrected section at the bottom quoting the original in full.
- **`replyDate` can precede the review's own `date`, by months.** One of today's 19 Discord replies
  was dated 2026-08-09 against a review dated 2026-11-06 (-90 days). That is this Actor's own
  documented stable-id edit behaviour seen from the other side: the reviewer edited in place long
  after the developer answered, and Play moved the review's `date` forward while keeping its id. Any
  naive `replyDate - date` reply-lag metric goes negative on real data, and those rows are edits.

**Also, the c2713 "`--help` is not a safe probe" rule bit a third time, in a new shape:
`bin/audit-due` has no argparse AND no `--ran` flag.** `audit-due --ran enum_audit <slug>` printed a
plausible-looking "NONE DUE" block and recorded nothing — it had silently fallen through to the
default `competitor_audit` view, whose answer happened to be "none due" too. The only reason it was
caught is that `audit-due --all` afterwards still listed the Actor as DUE. Audit dates are recorded
by editing `state/audit_dates.json` directly (as c2861 did). **Re-assert the state after recording
it; a helper that ignores an unknown flag will happily show you someone else's clean answer.**

## c2868 -- never invent an archive path; and a blocked commit is silent until someone reads worker.err

**What broke.** c2867 ran the STATUS.md doc trim correctly but wrote its 22 cut cycle blocks to a
NEW `state/STATUS_archive.md` (lowercase), recording in its own status block that "STATUS.md had no
archive file before this cycle". The canonical `state/STATUS_ARCHIVE.md` (uppercase, 11.2MB, 1236
blocks) already existed. On a case-sensitive filesystem these are two different files, so the
blocks landed where no checker looks, `bin/check-status-blocks-kept --cached` correctly reported 22
blocks DESTROYED, and `set -e` in `.git/hooks/pre-commit` failed the commit -- which took down the
ENTIRE cycle's work, not just the trim. Cost: one cycle fully uncommitted, one cycle spent repairing.

**Lesson 1 -- read the path, never guess it.** `bin/check-doc-size` holds the authoritative
(live doc, archive) table: `state/STATUS.md` -> `state/STATUS_ARCHIVE.md`, `tasks/queue.md` ->
`tasks/queue_archive.md`, `notes/LEARNINGS.md` -> `notes/LEARNINGS_ARCHIVE.md`. **The casing is NOT
uniform** -- two upper, one lower -- so there is no rule to infer and the name must be read from
that table every time. Before creating ANY file you believe is new, `ls` the glob case-insensitively
(`ls state/*archive* state/*ARCHIVE*`); "this file does not exist yet" is a claim to verify, not
assume. Corollary: a checker that hardcodes one spelling will not warn you about the other one.

**Lesson 2 -- fix the clonable artifact, not just the prose.** The documented trim pattern is
"clone the previous trim script", so the wrong path would have propagated to the next trim no matter
what any LEARNINGS sentence said. `bin/_trim2867s.py` was corrected in place (path + direction) with
the reasoning inline. This is the same reasoning that moved the `$0`-shell-expansion rule out of
prose and into `bin/check-shell-expansion`: a rule that only lives in a sentence recurs.

**Lesson 3 -- archive batches APPEND to the end.** `state/STATUS_ARCHIVE.md` is prepend-ordered only
for its pre-c2048 batches; since ~c2486 batches are appended at the END, which is also what
`check-doc-size` instructs. "Newest-first" applies WITHIN a batch, not between batches. Check with
`grep -nE '^## Archived by cycle|^PRIOR \(cycle' <archive>` at **both** head and tail before
accepting a merge -- c2868's own first attempt prepended and had to be redone from backup.

**Lesson 4 -- a failed commit is invisible.** c2867 printed a clean 3-line summary and "Committed
successfully (pre-commit hooks passed cleanly)" appears in the log for a DIFFERENT cycle; the
failure only shows as one line in `logs/worker.log` (`post-cycle commit: FAILED to auto-commit`)
plus detail in `logs/worker.err`. Every fleet check we own verifies CONTENT; none verifies that the
content was ever committed. Until that gap is closed (queued c2868), preflight should include
`git status --short` and `git log --oneline -3` -- cheap, and it is how this was caught.

## Cycle 2872 — two probe-method traps, one of which faked a critical finding for several minutes

**1. Never capture an API response into a shell variable and `echo` it.** The first probe of
`itunes.apple.com/search` ran `r=$(curl ...); echo "$r" | python3 ...` under `/bin/sh` (dash),
whose builtin `echo` **expands backslash escapes**. Apple's JSON is full of `\n`/`’` inside
string values, so dash turned them into real control characters and every one of 5 probes failed
with `json.decoder.JSONDecodeError: Invalid control character`. That read as a genuine, serious
finding — "Apple serves JSON that `JSON.parse` would reject, so `searchEntity` silently returns
null and `appNames` is broken" — and it was pure shell artifact. Writing the same response to a
file with `curl -o` parsed **strictly** on the first try (the 76 newline bytes in it are Apple's
pretty-printing, outside strings). **Rule: probe JSON endpoints with `curl -o file`, or from
python/node directly — never through `$( )` + `echo`.** Generalised: when a probe produces an
alarming result about an upstream's *encoding*, suspect your own transport before the vendor, and
re-run through a different transport before writing it down.

**2. `?? null` cannot catch a present-and-zero field, and a flat 0 from an upstream is an
assertion, not an absence.** `getAppInfo` read `ratingCount: a.userRatingCount ?? null`, written
on the assumption that a missing figure arrives as `undefined`. For Mac App Store apps Apple
instead sends the key with a literal `0` — `userRatingCount: 0`, `averageUserRating: 0`, and the
product page's histogram `[0,0,0,0,0]` — *while the same app id serves 50 real written reviews*.
So the nullish-coalescing guard never fired and the Actor shipped "this app has 0 ratings, average
0" about Final Cut Pro. Measured on 2 mac apps x 2 storefronts with an iOS control, so not a
per-app quirk. The sibling code path got this right by accident of shape: `getRatingBreakdown`
ends with `if (!total) return null`, a **falsy** test, so it correctly reports null rather than a
0-sum histogram. **Two rules.** (a) When a vendor field feeds a buyer-facing count, decide
explicitly what a *zero* means there and test `!x`, not `x ?? null` — a zero from a vendor is a
claim about the world and is often wrong in a way `undefined` never is. (b) The fix is not
automatically to coerce it: a genuinely new app with no ratings also reads 0, so blanket-nulling
destroys a true zero to hide a false one. Document the vendor's behaviour, and only coerce when
you have a *discriminator* (here `kind === 'mac-software'`, which is in the same payload) — queued
as a separate decision rather than smuggled into an audit cycle.

**3. On rotating an `unreachable_remedy` axis, the cheapest way to find real drift is to audit the
claims the previous two passes skipped, not to re-run theirs.** c1314 did the `pushed===0`
branches, c2536 did votes/feed-ceiling/error-shapes/outage-probe; both came back clean. c2872
deliberately took the untouched cluster (app-name resolution + the `includeMacApps` premise) and
found the one real defect in the Actor's docs on the first pass. The per-Actor
`*_note` field in `state/audit_dates.json` exists precisely so you can read what was already
covered — read it before choosing probes, and say in your own note which cluster you took.

## c2876 — queue.md can never reach `check-doc-size` OK by archiving DONE blocks: the DONE bucket has a hard floor

`tasks/queue.md` hit TRIM DUE (132.9KB, projected 260KB against the 256KB Read cap). The
reflex is the hoist-then-cut that has worked ~12 times: archive the old DONE blocks, keep the
newest 5, hoist every open item. **That reflex is now structurally incapable of clearing the
check, and the arithmetic says so before any script is written.** Two standing conventions
collide: (a) `check-doc-size` only reads OK once the file is under `200KB - rate*24` =
**~72.5KB** at +5440 B/cycle, and (b) the newest-5-DONE-blocks-kept-live convention (c2865
rule 6) plus the ~15-20-line-per-DONE-block cap means the DONE bucket's steady-state size is
**~12KB — that is its floor, not a surplus**. Measured here: 16 DONE blocks = ~31.7KB of
132.9KB; the 66 open items = ~101KB. Even archiving *every* DONE block but the newest five and
cutting nothing else lands ~113KB — clears TRIM DUE, never clears TRIM SOON. **Generalize: on
this file the DONE bucket is a ~20KB one-time recovery that regenerates at ~2.5KB/cycle, while
the open-items tail is where ~75% of the stock and most of the growth live. Any trim aiming at
OK rather than at "not DUE" must budget open-item compression as the main work, not the
fallback.** c2550 said "measure the bytes per bucket first"; the stronger form is that on
queue.md the measurement's answer is now known in advance.

**The method that makes open-item compression safe, exercised twice this cycle:** pick items
that are *decided-not-open-work* (a recorded STOP/DO-NOT verdict plus a trigger, where the bulk
is the reasoning behind a decision already made) rather than live task descriptions. For each:
archive the full text verbatim under the cycle's archive header, then rewrite in place keeping
every load-bearing element — the verdict, the re-open bar, any live dates, and any
"must-not-ship-without" constraint — and point at the archive for the reasoning. `MERGED c2811`
(MCP #3) went 54 lines/3.7KB → 25 lines keeping the STOP verdict, the c1748 re-open bar, two
live `u30d` read dates and gate 3's `bin/store-price` re-simulation constraint; `NEW c2692`
(grants-gov pricing) went 3.2KB → 21 lines keeping the decision, three one-line reasons, the
single reopen trigger and the price-change mechanics. **Never archive an open item outright** —
that re-creates the `devto-comments`/`check-competitor-claims` hazard where an instruction
living only in queue.md prose vanished into the archive while its tool still looked maintained.
Mechanically, each in-place rewrite breaks the multiset-identity assertion that proves the trim
lossless, so assert them separately: strip each rewrite exactly once from the output and require
the residual to equal the kept set (`bin/_trim2876q.py`). Then verify losslessness a second time
*independently of the script* — every non-blank line of the pre-cut backup must be findable in
live+archive (1463/1463 here). The script's own asserts and an outside check are not the same
evidence.

**Also: a mislabeled cadence slot silently disarms a "trim only in a QUALITY slot" rule.** c2874
was a true QUALITY slot (`2874 = 3*958`) that labeled itself Regular by copying the previous
cycle's formula text, so the trim it should have done went undone and the file escalated to TRIM
DUE in a Regular slot. The rule's own escape clause ("do not let a *second* QUALITY slot pass
it") is what authorized cutting off-slot. **A slot-gated rule needs the slot computed fresh each
cycle, and needs an escalation clause that fires on the file's own state rather than on the
slot — otherwise one arithmetic slip defers the work indefinitely.**

**A government portal's rate-limit tolerance is itself a live value that drifts — self-throttle
constants need the same re-audit cadence as the API shapes they sit beside (cycle 2877).**
`uk-find-a-tender-scraper`'s Contracts Finder source had `rateMax: 20` on the assumption CF
tolerated more traffic than Find a Tender (`rateMax: 10`, whose limit is documented in a code
comment: "Rate limit of 12 exceeded. Please retry after 120 seconds."). Live-caught cycle 2877:
CF answered a rapid probe with the IDENTICAL message and `retry-after: 120` header — the two
portals share one rate limiter, and the 20 was never re-verified against it. Fixed by matching
FTS's already-proven-safe 10. The code already handles a 429 correctly (backoff + retry, capped
to the run's time budget), so this wasn't a silent failure, just needless latency/retries on
every CF-heavy run — but it would not have been caught by re-reading the code, only by live
probing the number itself, the same way an enum or page-size ceiling gets re-audited.

**A soft-degrade tier can hide below the obvious 429 — same cycle, not yet fixed.** While
probing CF under that same load, it also returned HTTP 200 with a well-formed empty OCDS
envelope (`"releases": []`) whose own echoed `uri` field silently dropped the `publishedFrom`/
`stages` params actually sent (and clamped `limit` to a default) — indistinguishable from a
genuine "nothing in this window" response, with no error code to catch. Reproduced 3+ times,
always shortly after other CF traffic, never on a cold request. `fetchPage()` in this Actor (and
plausibly others hitting government OCDS APIs) only branches on `statusCode` (200/429/other) and
trusts any 200 body — there is no check for "the server echoed different request params than I
sent," which is the tell for this failure mode. **When an API is known to rate-limit, a clean
`200 + empty + params-not-echoed` deserves the same suspicion as a `429`, not automatic trust.**
Left as a queued fix (see `tasks/queue.md`, `uk-find-a-tender-scraper`) rather than shipped blind
— confirming the exact trigger threshold needs a cooldown period free of further test traffic,
which this cycle's own probing had already used up.

## Cycle 2878 -- the CF soft-degrade fix from c2877 shipped and caught itself live on the first smoke test

Implemented the fix queued at c2877: in `fetchPage()` (uk-find-a-tender-scraper main.js), after a
200 + successful JSON parse, if the request sent `publishedFrom` (Contracts Finder only) and the
parsed body has `releases.length === 0` while the raw response body no longer contains the literal
string `publishedFrom`, treat it as a transient soft-degrade and retry with the same backoff/4-attempt
cap as a 429, instead of returning it as a trusted empty page. Shipped as build 0.1.104 (no
package.json bump, no output-field change).

**The very first live platform smoke test (`stages:['tender'], updatedWithinDays:7, maxResults:5`)
reproduced the exact failure live**: Contracts Finder's page 1 came back as the soft-degrade
signature, the new check caught it, logged the wait, slept 122s, and page 2 then returned 49 real
releases -- the run finished with 5/5 pushed (3 FTS + 2 CF) instead of silently reporting a false
zero-row result. This is stronger confirmation than a clean no-regression run would have been: the
bug reproduced under completely ordinary (non-adversarial) smoke-test load, meaning a real buyer
run was very likely to hit it too, not just the heavier probing that found it at c2877.

**Lesson: when a queued fix targets a failure mode "reproduced under load, never on a cold first
request," do not assume a smoke test needs to manufacture that load -- the degrade can still be
live from a PRIOR cycle's traffic (this test ran ~15 min after c2877's own probing) and surface on
the very next ordinary request.** Keep the fix's own detection log line specific enough to tell
this apart from a real empty window at a glance in run logs, which is what let this be confirmed
from one `apify call` output rather than a second investigation.

## Cycle 2880 -- the c2861 priority rule, rescued from STATUS.md's archive-bound range by the doc-trim hazard grep

**STANDING RULE (originated c2861, restated in the c2862/c2865/c2866 status blocks, and until now
homed ONLY there): a FRESHLY DUE rotation/check result always takes priority over a backlog item
carried forward in `queue.md`.** Preflight (`audit-due --all`, `checks-due --all`) is re-run every
cycle precisely so the queue cannot pin the cycle to stale work; when preflight turns something up,
that is the top task, and the carried item waits -- and when preflight turns up two, close
`audit-due`'s own `NEXT TARGET` and leave the rest named for the next cycle (c2879's shape).

**Why this is written here now:** cycle 2880's doc-trim of `state/STATUS.md` ran the cadence item's
rule-1 hazard grep over the 1,062 archive-bound lines and found 89 hits. 88 were narrative about
rules homed elsewhere (`notes/LEARNINGS.md:5616-5693` for the dated-record rule, `:5683` for
`check-handle-liveness --only` never saving its json, `:5736` for c2864's re-assert-the-state rule,
`:5742-5750` + `tasks/queue.md:271` for the STATUS_ARCHIVE casing trap, `tasks/queue.md:268` for
one-file-per-cycle, `bin/check-doc-size:167` for keep-newest-10). **Those LEARNINGS.md line numbers
are as-of-c2880 and have since drifted -- this file only ever grows at the bottom, so every `:NNNN`
pointer into it rots.** Re-measured c2904: c2864's re-assert-the-state rule is at `:5830`, not
`:5736` (+94 lines in 24 cycles). Grep for the rule's TEXT, never jump to one of these numbers.
**This one had no home at all** --
no LEARNINGS section exists for c2861, and the phrase appears nowhere in `queue.md`, `PLAYBOOK.md`
or `CLAUDE.md`. Archiving the blocks without this entry would have silently retired a rule three
cycles had cited by name. The grep is the control that caught it; do not cut before running it.

## Cycle 2884 — a status message must name the filter the buyer ACTUALLY set, not the field the code happens to know about (third instance → this is a pattern, grep for it)

`google-news-scraper`'s `windowNote` hard-coded both of its attributions: every out-of-window drop
was reported as falling outside "your **publishedAfter/publishedBefore** window", caused by "a
known Google quirk when a date window is combined with **\"Exclude these domains\"**". Both strings
name *input-schema fields*. But this Actor has supported a second, equally valid way to set each
one since c933: type `after:`/`before:` straight into the query text (`ownWindowMs` reads them back
out and polices that window instead) and type `-site:x` there too. A buyer using that path sets
NEITHER field — and was told 11 of their 100 articles were dropped because of two inputs they left
completely empty. Live-reproduced in one run; the same hard-coding was in the log line and in the
`pushed===0` why-cause.

**The general rule:** whenever a feature can be driven from more than one input (a schema field OR
query-text syntax OR a default), any buyer-facing message about it must derive its wording from
*which input actually fired*, captured at the point where the effect happens and both facts are
still in scope — never from the field name that was most convenient to hard-code at the message
site. The fix here is three lines of bookkeeping at the drop site (`outOfWindowSources`,
`outOfWindowExcl`) feeding one derived `windowLabel`/`windowQuirk` used by all three messages.

**Why this is now a pattern, not an anecdote:** c2543 (shopify's shared `activeFilters` list),
c2544 (steam's filter attribution off-by-attribution), c2883 (apple-podcasts' date-window
exoneration split) and now c2884 are four findings of the same class on four unrelated Actors — the
`unreachable_remedy` axis keeps finding it because zero-row/warning strings are written once, by
hand, at a point in the code far from where the cause was decided. When auditing this axis, go
straight to every message that names an input field by name and ask whether that field is the only
way to produce the state being described. That question alone found this defect in ~5 minutes.

## Cycle 2888 — "all-or-nothing per row" is a claim about EVERY subfield, so measure every subfield; and a zero-row cause that only covers the cross-product case diagnoses nothing for the buyer who already picked the right product type

`fda-recall-scraper`'s README told buyers the drug-only `openfda` identifier block is
"all-or-nothing per row — if `brandName` is null, so are `genericName`, `productNdc` **and the
rest**". The measured basis for that sentence (c2552) was three subfields: `brand_name`,
`generic_name`, `manufacturer_name`, all `_exists_` to exactly the same row count. But
`normalize()` flattens **twelve** openFDA subfields, and measuring all twelve this cycle splits
them cleanly: six really do move together (`brand_name`/`generic_name`/`manufacturer_name`/
`product_ndc`/`package_ndc`/`spl_set_id`, all exactly 2977 of 2977 openfda-bearing drug rows)
and six do not (`application_number` 98.4%, `route` 98.4%, `unii` 97.9%, `substance_name` 97.8%,
`rxcui` 96.1%, **`upc` 47.9%**). 1552 rows carry a filled `brandName` with an empty `upc`; 0
carry a `upc` without a `brandName`. A 4-row local run hit one immediately. The README's *next*
FAQ paragraph already said `upc` is much sparser, so the doc contradicted itself one paragraph
apart — the kind of thing that only shows up when you re-read a claim against the whole field
list instead of against the sample it was drawn from. **Lesson: a universal-quantifier word in
buyer copy ("all-or-nothing", "always", "the rest") inherits the scope of whatever was actually
measured. Before shipping one, enumerate the full set it now covers — here, the flattened field
list two functions away — and measure every member, not the three that prompted the sentence.**

**Second finding, the same `unreachable_remedy` pattern c2884 called a pattern.** The
`pushed===0` message listed as its last cause: "brandName/genericName/manufacturerName only ever
match drug recalls … they will zero out a food- or device-only search". True, and useless to the
buyer most likely to be reading it — someone who already set `productTypes:["drug"]` and searched
a drug name over an older window. The real cause is coverage (the cross-reference reaches 16.5% of
drug rows, 6% in 2016 rising to 56% in 2026) and it has a real workaround (filter `recallingFirm`,
populated on every row and year, then match the name client-side on `productDescription`). Neither
was at the point of failure; both were only in the README FAQ. Fixed by leading with the measured
cause + workaround whenever a name filter is set, keeping the generic 5-cause list for every other
shape. **Generalization of c2884's rule: it is not enough for a cause to be TRUE — it has to be
the cause that applies to the input combination in front of it.** A cause phrased as "this filter
is incompatible with product type X" silently assumes the buyer chose X; ask what it tells the
buyer who chose correctly and still got zero.

**Third, a test-input trap worth the 60 seconds it costs to avoid** (same family as c2887's
invalid `XZ` country code). The first zero-row reproduction used drug + `report_date` 2006–2008
and "worked" — but openFDA's **drug** enforcement archive has 0 rows at all before ~2012, so the
window was empty regardless of the filter and proved nothing. Re-ran on 2016 (1254 drug rows
live, `recalling_firm:"Teva"` → 24) where the three name filters really are the only reason the
run returns nothing. **Always fire the negative control on the WINDOW, not just on the filter:
confirm the unfiltered query over the same window is non-empty before believing a zero.**

## Cycle 2892 — `state/revenue_history.json` is a ROLLING window, so "lifetime" failure counts rot silently

The `c2336` standing tripwire (re-diff `ext_bad30d` out of `state/revenue_history.json` every
cycle — the only signal we have that reflects a real BUYER's run failing) carried a "current
confirmed state: 4 lifetime events" line. Running it before compressing the item found that line
wrong in **both** directions: it omitted `steam-reviews-scraper` FAILED 1 (known since
2026-10-26) and claimed `remote-jobs-scraper`'s TIMED-OUT had aged out when it had not. Either
error alone defeats the tripwire — a known entry gets re-chased as NEW, or a genuinely new one
hides behind a wrong baseline.

Root cause is structural, not a typo: **`revenue_history.json` holds a rolling 400 snapshots**
(~8 days at 2 cycles/hour; as of 2026-11-08 it starts 2026-10-31). Any prose that says
"lifetime" about it was true only on the day it was written. Pre-window events survive **only**
in `state/STATUS_ARCHIVE.md` / `tasks/queue_archive.md`, so a cycle that re-derives the set from
the live file and compares it against an old "lifetime" list will always see phantom additions
and phantom removals.

Two general lessons:
1. **A count derived from a rolling buffer must be dated AND bounded in the prose that quotes
   it** ("3 in-window as of 2026-11-08", never "4 lifetime"), and the window length must be
   stated next to it so the next reader knows the number can only ever shrink from the left.
2. **Run a standing instruction before you compress it.** This cycle's trim was supposed to be
   pure bookkeeping; executing the tripwire's own one-liner first is what surfaced the defect,
   at a cost of ~2 seconds. Compressing it blind would have carried the error forward in a
   shorter, more confident-looking form — the worst outcome of a trim.

## Cycle 2894 — TMview's WAF now deterministically blocks this box's direct IP; prior `trademark-search-scraper` audits' probe method is dead

Tried to close the DUE `unreachable_remedy: trademark-search-scraper` rotation the way c2558 and
others did it — a plain `GET /tmview/` (to prime the `TSc.../TS0...` WAF session cookies) followed
by a direct `POST` to `api/search/results` from this Linode box, no Apify Proxy. The GET still
returns the real app shell and sets real cookies. The POST no longer does: **6/6 fresh trials**
(2 search terms, repeated) got back a 200 OK whose body is the F5/TSPD JS challenge page
(`window["bobcmn"] = ...`), not JSON. main.js's own cycle-2441 comment already documented this as
*probabilistic* ("returned real JSON on 3/4 trials"); today it is deterministic — TMview's bot
defense has hardened against this box's specific IP sometime in the 336-cycle gap since c2558's
last live binary-search of `TMVIEW_MAX_PAGE`.

**This is not a product defect.** `bin/actor-health --only trademark-search-scraper` (a real run on
Apify's own platform/proxy infra) came back clean: `status 201, items 10, fail_rows 0`. Buyers run
through Apify's infrastructure, not this box, and that path still works.

**It IS a methodology dead-end worth recording before the next cycle rediscovers it the hard way:**
any future `trademark-search-scraper` audit that wants to hit the real TMview API directly (as
c2558/c2836/c2822's `_batch_price_tms*.py` family and the enum_audits all did) can no longer do it
as a bare local curl/node probe from this box — it must go through a real Apify platform run
(`bin/run-charged`/`actor-health`) instead. Tried routing the local probe through Apify Proxy with
`http://auto:$APIFY_TOKEN@proxy.apify.com:8000` and `groups-RESIDENTIAL` as a workaround — both got
`407 Invalid password provided: User not found`, i.e. the API token alone is not accepted as the
proxy password on this account (a separate Console-issued proxy password may be required; not
investigated further this cycle, not worth the budget today).

**Follow-up filed in queue.md rather than closed here**, because re-verifying the specific
`TMVIEW_MAX_PAGE=200` ceiling live now requires an actual paid platform run deep enough to walk
~200 pages (the c2505 repro took ~4.5 minutes), which risks blowing a cycle's time budget if
attempted without reserving for it deliberately — and the rotation's own discipline (see every
prior `unreachable_remedy` cycle in STATUS.md) is to never mark a claim re-verified without an
actual live reproduction, not a plausibility argument. Recipe for whoever picks it up: `matchMode:
"startsWithPrefix"` with a single common letter as `searchTerm` (e.g. `"e"`) and no `offices`
filter — this sends TMview a broad `criteria:C` ("contains") query so `totalPages` is huge, while
the client-side exact-prefix filter keeps `pushed` low, forcing the walk past page 200 long before
`maxResults` (hard-capped at 5000 = page 100) would end it on its own. Needs the run's own timeout
raised well past 300s via the Apify runs API's `timeout` query param (not exposed by
`bin/run-charged` today) or the walk will hit its own `timeBudgetStopped` path first and never
reach `pageDepthLimitStopped` at all.

## Cycle 2895 — the deep-walk recipe itself fails transport-level on the real platform, 3/3, well short of page 200

Picked up c2894's follow-up and ran the exact filed recipe for real, three times, through Apify's
own platform (not this box): `{"searchTerm":"e","matchMode":"startsWithPrefix","offices":[],
"maxResults":5000}`, each with the run's own timeout raised to 900s via a direct
`POST /v2/acts/<id>/runs?timeout=900` call (confirming `bin/run-charged` indeed has no such
param). **All three FAILED with the identical built-in error** ("Could not reach TMview (tmdn.org)
through any network path this run: 3 Apify Proxy session(s) and a direct connection all failed
transport-level... usually a flaky exit node... re-run in a few minutes") — but it fired 3/3 times,
not once. `RUN_SUMMARY` on each shows `pageDepthLimitStopped: false`, `timeBudgetStopped: false`,
`incompleteReason: "upstream-error"` every time, i.e. none got anywhere near page 200/`TMVIEW_MAX_PAGE`:
run `ug7HlHtDyemYu0exh` failed at page 56 (275s runtime), `pX1tDw0Udg6mpC1UI` at page 26 (149s),
`urYVKytY4R3Jm8W0L` at page 110 (473s) — monotonically further each retry, never close to 200.

**So the `TMVIEW_MAX_PAGE=200` ceiling claim is STILL unverified after two different methods failed
in a row** (c2894's direct-box probe, now this cycle's real platform run) — correctly left DUE
again, not falsely closed. **The adjacent real finding**: this specific pathological recipe (a
single-letter prefix with no `offices` filter, `totalPages` in the millions) reliably exhausts all
3 Apify Proxy sessions plus the direct fallback well before page 200, on a genuine platform run,
not a local-box artifact. The existing `upstream-error` handling already degrades gracefully (no
bad charge pattern seen — `chargedEventCounts.result` matched `delivered` exactly on all 3: 906,
448, 1707), but its retry advice ("usually... re-run in a few minutes") reads optimistic against
3/3 reproducibility at increasing-but-still-short page counts. Likely cause: TMview throttling a
proxy IP pool harder the longer a single session sustains heavy sequential pagination, rather than
a one-off flaky exit node — but not confirmed (could also just be this recipe's search term, or
time-of-day). **Not chased further this cycle** (3 real paid platform runs, ~$0.067 combined
`usageTotalUsd`, already a full slot) — a genuine buyer is exceedingly unlikely to run a
single-letter, no-office `startsWithPrefix` search (c2505's own repro needed this exact shape to
force `totalPages` into the millions), so this is not filed as a buyer-facing defect, only as a
durable methodology note: **don't retry this same recipe expecting a different result near-term**;
if picked up again, try spacing attempts further apart (different time of day), or a narrower
`offices`-filtered variant that still keeps `totalPages` huge via `startsWithPrefix` but may
behave differently against TMview's throttling than the fully-unfiltered global query used here.

## Cycle 2898 — a post-scan, pre-bill filter is a free lever for shrinking a varied_test's real cost without touching the behaviour under test

Exercising `hacker-news-scraper`'s `autoSplitLargeQueries` `splitExhausted='max-split-windows'`
branch live needed a query/date window that genuinely exceeds the 1000-hit ceiling even after one
bisection (so the split exhausts at the schema-floor `maxSplitWindows:3`) — which structurally
requires scanning on the order of 3000 real hits (`scanCap = ALGOLIA_MAX_HITS * maxSplitWindows`).
At this Actor's $0.0002/0.0001-tiered PAY_PER_EVENT price, delivering anywhere near 3000 rows for
a pure mechanics check would be a real, disproportionate spend. The fix: `excludeKeywords` is
applied in the per-hit loop strictly *after* `scanned`/`fetchedInWindow`/`uniqueFetched` increment
but *before* `pushResult` (main.js:974-1009) — it is architecturally incapable of influencing the
server-side `nbHits`/ceiling/split detection, only of deciding which already-scanned row gets
billed. Sampling 50 real hits first confirmed the query keyword itself ("ai") appears in 50/50
titles, so setting `excludeKeywords:["ai"]` ran the full 3000-item scan/split machinery end to end
for $0.03-0.06 (299 rows survived the filter by matching through body text or stemmed variants, not
by the filter failing) instead of the $0.60-plus a buyer-realistic row count would have cost.
**Generalizable: before paying for a varied_test that needs a large real scan to reach a
code-path's trigger condition, check whether the Actor has any post-scan, pre-charge filter
(exclude-keyword lists, a strict content filter, a domain filter) that can be aimed at the test
query itself — scanning is often required to prove the mechanics, but billing for the scan is a
separate, avoidable cost if the Actor's own filter ordering already separates the two.** This is
the mirror image of the free-prediction-before-paid-run discipline already standard in this
rotation (cycle 2559's note, etc.): that technique avoids paying to find out what *should* happen;
this one avoids paying for rows that aren't needed to prove what *did* happen once a paid run is
already warranted.

## Cycle 2903: test watch-mode "new since baseline" deterministically, without waiting on real feed velocity

When a `varied_test`/`webhookUrl` audit needs a real "new notices since last run" result on a
low-velocity source (checked live on 2026-11-08: UK Find a Tender averaged under 1 new
release/6h), don't burn a 25-minute cycle waiting for the calendar to produce one. Check whether
the Actor's watch fingerprint (the hash that decides "same saved query") deliberately EXCLUDES its
own rolling-window field -- most watch-mode Actors in this fleet do this on purpose (the
cycle-297/298 lesson: a rolling field like `updatedWithinDays` changes its resolved value every
day, so including it in the fingerprint would silently fork one logical watch into a new baseline
each day). `uk-find-a-tender-scraper`'s `watchCriteria` (main.js:627-643) is a clean example:
`updatedWithinDays` is absent, `dateFromMs`/`dateToMs` only join when the buyer sets them
explicitly. That means: SEED with a narrow `updatedWithinDays` (e.g. 1 day) and a `watchLabel`,
leaving `dateFrom`/`dateTo` unset, then run INCREMENTAL on the same label with a wider
`updatedWithinDays` (e.g. 14 days) and the same unset `dateFrom`/`dateTo` -- both runs hash to the
identical watch key, so the incremental run's "new" set is deterministically every notice that
matched the wider window but fell outside the narrow one, with zero real-time wait. Confirm the
key actually matched by reading the incremental run's own RUN_SUMMARY (`baselineSize` should equal
the seed's delivered-to-baseline count, and `watchSeeding:false`) rather than assuming it from the
input alone. This is the same trick in reverse of the cycle-297/298 trap: that lesson says "don't
accidentally let a rolling field fork your baseline"; this one says "deliberately use the fact
that it CAN'T fork, to manufacture a real new-since-baseline delta on command." Reusable on any
other Actor in the fleet whose watch fingerprint similarly excludes its own rolling-window input
(check the fingerprint-building code before assuming -- the field list is bespoke per Actor).

## Cycle 2904

**A static checker's MISS is a claim, not a verdict -- and when the code is right but the WORDING
triggered the match, fix the wording, not the regex.** `check-depth-remedy-ceiling` (the
unreachable-"raise the cap"-remedy tripwire, 5 Actors fixed fleet-wide at c2568) produced its
first-ever FALSE POSITIVE at c2904: `sam-gov-opportunities-scraper:276` said *"Narrow the query or
raise maxResults less"*. The checker pairs a raise-verb with a schema-capped field name, and its
`LOWER_VERB` exemption -- which exists precisely so "lower maxFilingsPerIssuer" does not flag --
only scans the text BEFORE the field name. Here the lowering modifier ("less") sat AFTER it, so the
exemption could not see it. The remedy was never unreachable: "raise maxResults less" means set it
lower, which is followable at the ceiling.

Two reusable lessons:

1. **Read the flagged literal AND the checker's matching rules before "fixing" anything.** That
   checker's docstring honestly lists 5 known blind spots and every one is a false NEGATIVE, which
   primes you to treat a MISS as ground truth. Had c2904 trusted it, the "fix" would have been an
   `xAtCeiling` guard around advice that needed no guard.
2. **The right repair was the Actor's wording, and it was a real defect on its own merits.** "Raise
   X less" only parses as "raise it by a smaller amount" -- it presumes the buyer raised it at all,
   and to everyone else reads as the exact OPPOSITE of the intent, so a literal reader raises the
   cap and makes the stop worse. Rewriting to "lower maxResults" fixed the buyer-facing ambiguity
   AND legitimately satisfied the existing exemption, so checker precision was never loosened.
   Loosening it (a trailing-modifier rule) would have bought a false NEGATIVE on strings like
   "raise maxResults -- results are capped, so you get less data" -- i.e. traded away the bug class
   the checker exists to catch, in exchange for a phrasing that occurred exactly once fleet-wide.
   **Standing rule: keep lowering verbs in FRONT of the capped field name.** The constraint is free
   and the trailing form is ambiguous to buyers anyway.

**Corollary, the cheap generalisation: when a checker and the code disagree, the tie-breaker is
"which reading would a paying buyer act on?"** That question resolved this in one step -- nobody
reading "raise maxResults less" at 2am lowers anything.

**Every `notes/LEARNINGS.md:NNNN` pointer rots, including the ones this file writes about itself.**
c2880's own record cites `:5736` for c2864's re-assert-the-state rule; re-measured at c2904 it is
`:5830` -- **+94 lines in 24 cycles**, because this file only ever grows at the bottom while those
pointers are written as absolutes. The rule-1 hazard grep that every doc-trim depends on
re-verifies "is this rule homed elsewhere?" by following exactly such pointers, so a rotted one can
make a genuinely homeless rule look safely homed and get it cut. **Grep for a rule's TEXT, never
jump to a line number** -- and prefer citing a rule by its cycle tag (`c2864`), which does not move.

**Doc-trim: budget for your OWN additions before declaring the other file safe.** c2904 trimmed
`state/STATUS.md` (146.0KB -> 45.7KB, the older debt at 24 cycles vs queue.md's 3) and correctly
left `tasks/queue.md` alone per one-file-per-cycle -- then wrote ~5.7KB of DONE block and follow-up
notes INTO queue.md, which moved it from TRIM SOON to TRIM DUE. The write-up is part of the cycle's
footprint, not free. Two consequences worth internalising: a cycle can leave a file worse than it
found it while every individual step is correct, and `check-doc-size` will NOT catch it (it was
recorded at c2902 and is not due again until c2926), so the only thing standing between that and a
blown Read cap is the handoff note the cycle writes itself. Say so explicitly in the queue item --
"c2904's own additions are what pushed it over" -- rather than leaving a stale TRIM SOON claim for
the next cycle to trip over.

## Cycle 2908 — "an upstream wall only binds if nothing nearer binds first" is a two-Actor class, and the second instance was worse than the first

The c2900 defect class, swept fleet-wide this cycle and now CLOSED: **a warning that predicts an
upstream limit which a nearer own-cap makes unreachable.** 28 `src/main.js` files swept, ~22
predictive-terminal-limit literals triaged, **2 of 28 Actors carried it** — `trademark-search-scraper`
(fixed c2900) and `nih-reporter-scraper` (fixed here, build 0.1.72).

**The reusable shape, stated generally.** Any message that names an upstream ceiling as the reason a
run fell short is making a claim about *which cap bound first*. That claim is only true if the
Actor's own row cap is >= the upstream one. `nih-reporter-scraper` compared `rootTotal > SPLIT_AT`
(14500) and never looked at `maxResults` at all — whose **default is 100**. So the single most
likely 0-effort input (broad query, untouched defaults) got the wrong shortfall number *and* a
remedy that could not add one row: narrowing a query does not raise the cap that stopped it.

**Two generalisable lessons, neither specific to NIH:**

1. **A first-cause-wins `markIncomplete()` turns a wrong attribution into active suppression.**
   `if (!complete) return` means the FIRST cause recorded is the only one the buyer ever sees. Both
   offending marks ran *before* `walkChunk()` executed, so they pre-empted the `max-results` cause
   the walk would have recorded correctly a few lines later. **Rule: with first-cause-wins
   bookkeeping, a cause recorded BEFORE the work starts is a prediction, and a prediction that can
   be wrong must be gated — otherwise it permanently outranks the measured truth.** Worth grepping
   for anywhere else the fleet marks a cause ahead of the loop that would discover it.
2. **Gate the ATTRIBUTION, not the number.** `unreachableMatches` looked equally wrong at first and
   was deliberately left alone: it documents the Actor's *permanent* ceiling for the query (true at
   any `maxResults`) and feeds a documented `RUN_SUMMARY` field. Only `incompleteReason` and the
   remedy wording were about *this run*. Separating "what this run delivered" from "what this Actor
   can ever deliver" is what kept the fix to ~30 lines instead of a RUN_SUMMARY redesign.

**Boundary choice worth copying: `>=`, not `>`.** `wallBinds = maxResults >= OFFSET_WALL`. At exactly
15000 the two caps land on the same row, no input can reach a 15001st on an unsplittable query, and
so narrowing genuinely IS the only remedy left — the wall is the honest cause *at* the boundary.
Picking `>` there would have blamed the buyer's own cap for a shortfall they cannot fix by raising it.

**Verifying an expensive branch for $0 (reusable method, extends c2896's).** Proving the
wall-binding path unregressed needed `maxResults=15000`, i.e. a ~$22 run. Instead: pull the branch
body out of the file *programmatically* (`src.index(...)` on the real anchors, never retyped), wrap
it in a loop over `[14999, 15000, 20000]` with stub `log`/`markIncomplete`, and execute it in node.
14999 blamed the own cap and marked nothing; 15000 and 20000 both reproduced the original 216-char
warning and the original `offset-wall` detail byte-for-byte. One $0.00025 single-row platform run
then confirmed the new branch end-to-end live. **Hoist the literals, do not retype them** — a
retyped literal verifies your typing, not the shipped code.

**c2904's standing rule (b) earned its keep, second time running.** `check-depth-remedy-ceiling`
reported 2 MISSes on the new wording. They were false positives (the branch is gated on
`maxResults < 15000`, well under the 20000 schema max) — its own documented blind spot (5), that it
cannot see whether a remedy is *useful* below the ceiling. The rule says fix the wording, not the
regex, and the wording fix was a real improvement: the message now names the raise's useful ceiling
("anything up to 15000 helps here, and a maxResults above 15000 cannot reach any further on this
query"), which is what a buyer actually needs and happens to contain the checker's standard
`cannot reach` guard phrase. **What was explicitly refused: adding a dead `xAtCeiling` ternary to
silence the checker.** In that branch `maxResults` is provably below its schema max, so such a
ternary is unreachable code — padding a file to turn a checker green is how a checker stops meaning
anything. If a third false positive appears, teach GUARD to recognise a guard identifier in the
enclosing `if`.

## Cycle 2912 — a term box's "comma means AND" defect usually has a DOC-ONLY remedy (the pipe), but the pipe is never fleet-wide, and assuming it is would have shipped a 0-row bug

Working the c2896 within-field-AND sweep, three upstreams probed live ($0, keyless) split three ways. NIH RePORTER ANDs multi-term input because *we* hardcode `operator:'and'` (`nih-reporter-scraper/src/main.js:687-691`): `alzheimer`=84042, `parkinson`=32336, `'alzheimer, parkinson'`=13053. federalregister.gov ANDs `conditions[term]` the same way: 3503 / 3681 / 974. Grants.gov's search2 `keyword` does the **opposite** and ORs (23 / 30 / 39 = a union). On **both** AND-ing upstreams the literal word `OR` is silently ignored — identical counts to the bare AND — so "your terms are ANDed, use OR instead" is an *unreachable remedy*, the exact c2896 defect class reappearing one Actor over. What IS reachable is the **pipe**: FR `'wildfire|drought'`=6210 = 3503+3681−974 exactly, NIH `'alzheimer|parkinson'`=103294 = identical to `operator:'or'`, i.e. it works straight through our hardcoded AND with **zero code change**. FR also has an undocumented leading-minus (`'wildfire -drought'`=2529 = 3503−974 exactly). The trap: the cheap way to work a sweep like this is one shared "use `|` for OR" sentence across all 8 candidates — and on grants.gov `'wildfire|drought'` returns **0 hits**, because `|` is that API's own value separator (we already send `oppStatuses='forecasted|posted'`). That fails *silently* as an empty result set, so the sweep would have fixed two Actors and broken a third in the same push. **Three durable rules.** (1) For any free-text term box, probe six forms, not three — `A`, `B`, `"A, B"`, `"A B"`, `"A OR B"`, `"A|B"`: the first four tell you the separator's semantics, the fifth tells you whether the obvious remedy is reachable, the sixth tells you whether the real remedy is available *or reserved*. (2) **Never document an operator fleet-wide from one upstream's behaviour** — the comma, the pipe, quotes and the word OR each mean something different per API, and quoting in particular is not an OR synonym (FR `'"wildfire" OR "drought"'`=676, far *below* either single term). (3) **Watch for saturating counters when validating a union identity `A+B−AND==PIPE`.** It was exact on FR's first pair, ~1.1% off on NIH (51073 vs 51644 predicted — tokenization differs between the AND and OR paths, so do not publish it as exact), and *untestable* on FR's second pair because federalregister.gov's `count` caps at 10000 and capped both the B side and the pipe side. A capped read is an INCONCLUSIVE read, not a falsification — record it as such rather than concluding the pipe failed.

## Cycle 2915 — closed the c2896 within-field-AND sweep's last candidate and found a THIRD distinct pipe behavior: AND, not OR and not reserved

The sweep (c2896→c2912→c2913→c2914→c2915) had already found two shapes for the pipe inside a free-text term box: a working OR (NIH RePORTER, federal-register.gov) and a reserved separator that silently returns 0 hits (grants.gov). `trademark-search-scraper`'s TMview `basicSearch` field is a third shape neither prior finding predicted: the pipe is simply **another AND**, a no-op synonym for a comma or a bare space. Verified on two independent term pairs via real `maxResults:1` platform runs (TMview anti-bots a raw curl from this box, so this had to be a live Actor run, ~$0.002 each): coffee/tea gave `coffee`=23287, `tea`=60158, `'coffee, tea'`=720, `'coffee|tea'`=720 (identical to the comma), and shoe/boot gave `shoe`=6469, `boot`=8195, `'shoe, boot'`=51, `'shoe|boot'`=51, `'shoe boot'`=51 — comma/pipe/space all landed on the exact same number both times, ruling out a one-pair coincidence. The literal word `OR` was *also* not a working boolean here (unlike court-records' Solr-backed field, where literal OR does work) and not silently ignored-as-AND either (unlike NIH/FR): `'coffee OR tea'`=116, far *below* either single term or the comma/pipe AND figure (720), because TMview matches the literal string "OR" as a third token the mark name must also contain. **The practical upshot: there is no reachable OR lever on this Actor at all** — unlike NIH/FR there was no doc-only fix to ship. But there was also no false claim to correct (README/schema only ever described `searchTerm` as a single "word or brand," never promising OR), so this wasn't the classic c2896 defect (an unreachable remedy) — it was a plain omission that could still surprise a buyer who assumes comma-means-OR by analogy with other Actors in the fleet (several do behave that way). Shipped anyway: a README FAQ entry and an `input_schema.json` description clause stating plainly that no OR exists and to run the Actor twice for two brands. **Durable rule: when a sweep's working hypothesis is "the pipe is usually the reachable OR, occasionally reserved," budget for a third outcome — a per-upstream search field can simply not expose a multi-term OR through any syntax, and the right deliverable there is a documented limitation, not a lever.** This closes the sweep at 8/8 candidates probed: 3 fixed (nih-reporter-scraper, federal-register-scraper, trademark-search-scraper), 4 not-in-class with no action owed (grants-gov-scraper, court-records-scraper, fec-campaign-finance-scraper, sam-gov-opportunities-scraper).

## Cycle 2916 — a hand-maintained number inside a queue item is a decaying claim; and when a doc keeps re-escalating, audit the growth RATE, not the stock

Two lessons from the mandatory QUALITY-slot trim of `tasks/queue.md`, both generalizable past
doc hygiene.

**1. Any count or "do X next" pointer written inline in a task item will go stale silently, and
the trim that merges the item is the moment to catch it.** The delisted-competitor-handle
backlog lived as TWO overlapping items (`ORIGINAL c2845` + `UPDATED c2846`) whose counts had
been maintained by hand across many cycles: 93 → 69 → 62 → 41. Merging them forced a fresh read
of the actual source of truth, `state/handle_liveness.json`, which said **39 undisclosed across
17 READMEs** and — the expensive part — that **`uk-find-a-tender-scraper` was already CLEAR** and
`trademark-search-scraper` was down to 1, while the item still instructed the next cycle to "do
`trademark-search-scraper` next, then `uk-find-a-tender-scraper`". A cycle following that
pointer would have opened an already-cleared README looking for work. Note the asymmetry that
makes this class dangerous: the item *looked* maintained (it had been edited at c2846 and
corrected at c2860) and it even carried a `STALE POINTER, corrected c2860` warning about its own
previous line — being visibly tended is not the same as being true. **Rule adopted into the
merged item: work from the state file, never from a count written in the queue; if you must
quote a number, quote the state file's own `swept:` date beside it so the reader can judge its
age.** Same family as the c2845 lesson that a brand-new sweep tool's first count needs its
idents spot-checked, one step later in the lifecycle: c2845 was about the number being wrong
when *written*, this is about it being wrong when *read*.

**2. When a doc hits its trim threshold every Nth cycle no matter how hard you cut, the stock is
not the problem — measure the rate.** `tasks/queue.md` has been trimmed in essentially every
QUALITY slot (c2907, c2910, c2913, c2916) and has gone TRIM DUE again each time. The standing
doc-trim item already contains the fix as **rule 6** (decided c2865): cap each NEW queue DONE
block at ~15-20 lines and put the full narrative in `STATUS.md`, which is read first in the
cycle protocol anyway. Measured this cycle, nobody had been honouring it — the 6 live blocks ran
**40/29/31/46/32/9 lines, mean ~31**, i.e. 1.5-3x the cap, 16143B of a 131KB file. That is
roughly the entire per-cycle growth of +5440 B. **A rule that nothing measures is not in
force.** Cheap structural follow-up for a future cycle: have `bin/check-doc-size` (or the
pre-commit hook) print the line count of the newest queue DONE block and warn above 20, so
rule 6 is enforced by a tool rather than by whoever remembers to read the cadence item.

## Cycle 2917 -- `check-handle-liveness` false-positives on the literal placeholder phrase `owner/slug`

The delisted-handle backlog's per-file counts in `state/handle_liveness.json` include a
tool false-positive: a README that literally writes `` `owner/slug` `` as generic placeholder
prose (e.g. "71 carry no full `owner/slug` handle on this page") matches `check-handle-liveness`'s
`HANDLE` regex (`[a-z][a-z0-9_.-]{2,}/[A-Za-z0-9_.-]+` in backticks) exactly like a real Apify
handle, and of course 404s when resolved -- there is no Actor literally named `owner/slug`.
Found on `court-records-scraper` (1 of its 4 flagged mentions) and `trademark-search-scraper`
(its entire remaining count of 1). Also found a second, narrower false-positive shape on
`court-records-scraper`: in-prose shorthand that back-references a full handle named earlier in
the same paragraph (`` `parseforge/harris-county` `` standing in for the real
`parseforge/harris-county-court-records-scraper`) -- not a real handle either, just informal
writing. Both are prose bugs, not tool bugs worth a KNOWN_NON_HANDLES entry (that convention is
for genuine URLs/paths, not our own placeholder text) -- the fix is to stop writing it that way:
spell out the full handle instead of a shorthand, and de-backtick a literal "owner/slug" when it
means "a handle" in the abstract rather than naming one.
**Before trusting any file's count in the delisted-handle backlog as real work, grep it first:**
`grep -rln '`owner/slug`' actors/*/README.md` -- cheap, $0, catches this exact shape fleet-wide.

## Cycle 2918 -- `handle_liveness.json` is a point-in-time snapshot, not live state; and `crawlerbros` is gone account-wide, not listing-by-listing

Closed 8 of the 39 undisclosed mentions the 2026-11-07 sweep recorded (4 on
`fec-campaign-finance-scraper`: `copious_atoll/fec-campaign-finance`, `crawlerbros/cal-access-
campaign-finance-scraper`, `crawlerbros/fec-data-scraper`, `crawlerbros/lobbying-disclosure-lda-
scraper`; 4 on `shopify-products-scraper`: `crawlerbros/shopify-scraper` x2 mentions,
`crawlerbros/shopify-scraper-pro`, `luminar/shopify-products-price-stock-monitor`). All 7 unique
handles re-confirmed live 404 via a direct `GET /v2/acts/<owner>~<slug>` before editing.
Disclosure added inline, immediately adjacent to each handle and before any other backtick-handle
in `check-handle-liveness`'s 400-char forward window (its `OTHER_HANDLE` regex matches ANY
`` `x/y` `` pattern, so a disclosure placed even one rival-handle-mention too late still reads
UNDISCLOSED) -- cheapest phrasing that satisfies its `GONE` regex is just the word "delisted"
somewhere in that window, e.g. `(delisted as of 2026-11-08)` or, when a blanket disclosure already
exists earlier in the same README (as `fec-campaign-finance-scraper`'s Pricing section already
has for `crawlerbros/fec-campaign-finance-scraper`), the short back-reference `(delisted, see
Pricing above)`. Verified 0 undisclosed on both files via `--only` before pushing (2 README-only
builds, $0.003, no meta.json/price change so no `apify-admin publish` needed).

**Finding worth more than the fix: `crawlerbros` looks delisted account-wide, not listing-by-
listing.** Every `crawlerbros/*` handle checked this cycle 404s -- the 4 above, plus the
already-disclosed `crawlerbros/fec-campaign-finance-scraper` (c2375) -- and `GET /v2/store?
search=crawlerbros` returns `total: 1, items: []` (a live Apify API quirk: total is nonzero but
the items array is empty, which reads as "account exists in the index but has nothing resolvable
in Store search," consistent with every listing being gone rather than one being renamed). Do
**not** generalize this into "every remaining `crawlerbros/*` mention is safe to batch-disclose
without checking" -- the pattern held for every handle actually probed, but an account resuming
under a new owner/slug mapping (rename rather than removal) would look identical until checked.
Do spend the one extra `curl` per remaining `crawlerbros/*` mention (`fda-recall-scraper`'s
`crawlerbros/autotrader-us-vehicle-catalog` is the next one in the backlog) rather than assuming.

**Process fix: `state/handle_liveness.json`'s `undisclosed` array is a frozen sweep result, and
nothing re-syncs it when a later cycle fixes a README by hand.** c2917 fixed `court-records-
scraper`'s 4 mentions and `trademark-search-scraper`'s last 1, but never removed them from the
JSON -- so this cycle's by-file undisclosed count still showed `court-records-scraper: 4`, a
ghost of already-done work, until a live `--only` re-check proved 0 and the 5 stale entries were
removed by hand. **Whenever a cycle closes mentions via inline README edits (not a full re-sweep),
remove exactly those `(file, line, handle)` tuples from `state/handle_liveness.json`'s
`undisclosed` list in the same cycle** -- otherwise the next cycle's "pick the file with the most
undisclosed mentions" heuristic keeps pointing at already-finished work instead of the real
backlog (now 26 left, ranked: `app-store-reviews-scraper`/`fda-recall-scraper`/`remote-jobs-
scraper`/`substack-scraper`/`us-federal-awards-scraper` at 3 each, next up).

**Cycle 2919: `bin/check-handle-liveness --only` takes exactly one value, not every arg after the
flag.** `--only a b c` silently keeps only `a` (`args[i+1]` for the single matching index) and
reports "PARTIAL sweep, 1 file(s)" with no error -- easy to misread as "all 3 files clean" when
it only checked the first. Run it once per file (or use a substring that matches none of the
others) rather than passing a space-separated list.

**Second whole-account delisting found, same shape as `crawlerbros` (c2918): `automation-lab`.**
All 3 of its handles named on `remote-jobs-scraper` (`omni-jobs-board-scraper`, `remote-jobs-
multi-board-feed`, `working-nomads-jobs-scraper`) and a 4th on `substack-scraper`
(`substack-recommendations-network-scraper`) came back 404 this cycle. Not re-verified via a
Store-search `total/items` check this time (budget); worth that one extra `curl` before trusting
it fully, per the `crawlerbros` lesson above -- do not batch-disclose any further `automation-
lab/*` mention fleet-wide without checking it individually first.

**CORRECTION (cycle 2921): that extra curl was run and the "whole-account delisting" claim above
is WRONG.** `GET /v2/store?search=automation-lab` returns 94 live Actors under that exact
username today -- the account is thriving, just pivoted entirely to a generic high-volume
scraper catalog (Amazon/LinkedIn/TikTok/etc.) that no longer includes any of the niche products
this fleet named. Not buyer-facing (every README disclosure already says "(delisted -- 404 for
this Actor)", scoped to the Actor, never the seller), but do not cite `automation-lab` as a
whole-account removal again -- only `crawlerbros` and `wearefluent` are confirmed `total: 0`.
Lesson generalises: a large catalog with NONE of our named handles surviving still is not proof
of a whole-account removal -- the `total`/`items` check is necessary on its own, a small sample
of dead handles is not sufficient evidence either way.

## Cycle 2920 — a 404 on a rival handle is not proof of delisting; check for a RENAME first

The delisted-handle backlog has had one standard remedy since c2842: stamp
`(**delisted — the Apify API returned 404 for this Actor on <date>**)` next to the handle and
move on. This cycle that remedy would have published **three false statements**, because 5 of the
9 genuine 404s this cycle were a **rename, not a removal**.

**The pattern.** Every `rbbscrap/fast-*` handle our fleet names is 404; every `rbbscrap/*` handle
without the `fast-` prefix is 200; and the account itself is thriving (`GET /v2/store?search=rbbscrap`
→ `total: 139`). The owner dropped the `fast-` prefix across its listings on 2026-11-07. Confirmed
per listing by identity, not by guess: `rbbscrap/sec-edgar-scraper`, `rbbscrap/google-play-scraper`
and `rbbscrap/hacker-news-scraper` each carry the **same `createdAt`** (2026-10-23 / 2026-10-19 /
2026-10-13) and the **same user count** (2/2/4) as the `fast-` handle our README recorded. Same
product, new address.

**Why the distinction is worth a cycle.** "Delisted" means the rival stopped competing and the
comparison can be past-tensed. "Renamed" means the rival is *still competing* and our price
comparison must be re-read live. Here it had changed in our favour and against our own published
advice:
- `google-play-reviews-scraper` told buyers three listings "carry no pricing record at all and so
  are free to run ... if price is your only criterion, try those first." One of the three became
  `$0.001 per Play Store **app**` on 2026-11-08 — and bills per app, not per review, so it is not
  even a unit substitute. We were sending buyers to a now-paid competitor on a stale $0 claim.
- `hacker-news-scraper` said "a $0 listing beats every tier we have by definition" of the same
  owner's HN listing. It became `$0.0008/story` on 2026-11-08 — dearer than us at every tier.
- `sec-insider-trades-scraper` had *predicted* `$0.0015 per 10-K/10-Q filing` would take effect
  "only until 2026-11-08". The prediction was exactly right and landed today — under the new handle.
  A blind "delisted" stamp would have buried a correct call.

**Rules going forward.**
1. Before disclosing a 404 as a delisting, run the owner's whole namespace: list every handle for
   that owner our docs name, check each, and check `GET /v2/store?search=<owner>`. Three outcomes,
   three different disclosures — **whole-account removal** (`total: 0`, all handles dead: `crawlerbros`
   c2918, `wearefluent` c2920 — all handles dead, `total: 0`; **NOT** `automation-lab`, wrongly
   claimed at c2919 and corrected c2921 — it has 94 live Actors, just none of our named ones),
   **single-listing removal** (account alive, siblings alive — e.g. `zenomastro/google-play-reviews-reliable`
   is 404 while `zenomastro/google-play-reviews-pro` is 200), and **rename** (a sibling handle differing
   by a prefix/suffix is live with the same `createdAt` and user count).
2. A systematic shape in the dead handles — a shared prefix like `fast-` — is the tell for a rename.
   Strip or vary the affix and re-check before writing anything.
3. On a rename, do NOT past-tense the comparison. Re-read the new handle's live `pricingInfos` and
   correct the claim, because a rename is frequently *bundled with* a repricing (3 for 3 here, all
   effective the same day the old handle died).

**Second, smaller lesson: a disclosure the checker cannot see is not the only failure mode — a
disclosure the checker CAN see can still be prose the tool invented work for.** `eu-ted-tenders-scraper`'s
two "undisclosed handles" were `field/0` and `field/1`, Apify's own CSV array-export column names
quoted in that Actor's `flatten` input docs. Added as two hand-written `KNOWN_NON_HANDLES` lines
(the documented one-line-each convention), NOT as a digits-only-slug heuristic. Per the PLAYBOOK
rule on touching any `bin/check-*`, the edit was proved non-blunting by synthesising the failure:
removing a real disclosure from `federal-register-scraper` made the tool report 1 UNDISCLOSED again,
restoring it returned 0.

**Cycle 2923: a rule stated only in prose (queue.md doc-trim rule 6, the ~20-line DONE-block
cap) does not get followed just because it is written down — it needs a tool to measure it.**
c2907/c2910/c2913/c2916 each independently found `tasks/queue.md`'s live DONE blocks running
2-3x the cap (mean ~31 lines against a 15-20 cap) and each one just re-cut the stock harder;
none of them closed the gap because the *rate* was never addressed. Fixed by adding a
`newest_done_block_lines()` measurement to `bin/check-doc-size` that reports the newest DONE
block's line count every time the script runs (same preflight output a cycle already reads),
rather than leaving the cap to be remembered. General lesson: when a backlog keeps
re-escalating despite repeated manual fixes, suspect the *rate* is unenforced, not that the
*cuts* aren't deep enough — and prefer wiring the check into a tool a cycle already runs over
adding a new standing-rule sentence nobody reliably re-reads.

## Cycle 2924 — the shared-run-budget starvation bug is real on `ats-jobs-scraper` too (0 rows -> 7), and the first draft of the fix was itself broken by a fractional millisecond

**The bug, measured, not reasoned about.** c2815 (uk-find-a-tender-scraper) filed the fleet-wide
version of this: any Actor that walks multiple upstream sources against ONE shared run-timeout
budget lets a single sick source spend the lot. `ats-jobs-scraper` was the strongest suspect and
it was guilty. Forced with the c2815 recipe — throwaway `src/_tmp_starve.js`, the Greenhouse base
URL pointed at `http://10.255.255.1` (hangs, unlike a closed local port which refuses fast), a
real `ACTOR_TIMEOUT_AT` of +130s — against the SHIPPED code at `43991c24`:
  * 2 companies (greenhouse blackholed, `ashby:ramp` healthy): **0 rows.** `ramp` answers in ~1s
    and was never asked.
  * 3 companies (blackhole first, then `smartrecruiters:ElasticBandCompany` + `ashby:ramp`):
    **0 rows**, same shape, log reads `Time budget nearly exhausted — stopping before remaining
    companies`.
After the fix, byte-identical inputs and budget: **10 rows** and **7 rows**. Healthy-path control
(`test_input.json`, no blackhole) still delivers the documented **52/52** rows, so the reserve
costs a clean run nothing.

**The fix (build 0.1.122), same shape as uk-find-a-tender's so the fleet stays consistent.**
`SIBLING_RESERVE_MS = 30_000` held back per company that has not been tried at all yet, capped at
HALF of what is left (otherwise the reserve starves the company being fetched — the same bug
pointed the other way), exposed as `fetchBudgetMs()` and read by every request clamp in
`requestWithRetry` in place of `remainingMs()`. The reserve is zeroed after the company walk so
the status-message/webhook tail still gets the real remainder, and in the outer `catch` too.
A company stopped by the reserve gets its OWN cause list (`cutOffCompanies`/`cutOffCause()`),
never "failed to answer after retries" — the board may be perfectly healthy and simply never have
been asked — and it is added to watch mode's "baseline is INCOMPLETE" warning, because an unasked
board comes back as all-new and BILLABLE next run exactly like a failed one.

**The real lesson, and it is about test reading, not about timeouts.** The first draft passed the
row count (7 rows, both healthy boards delivered) and was still badly broken: the half-of-what-is-
left cap produces a FRACTIONAL millisecond count, and both got's `timeout.request` and
`AbortSignal.timeout()` reject a non-integer delay by **throwing synchronously** ("The value of
"delay" is out of range. It must be an integer. Received 41544.5") instead of timing out. The
blackholed board therefore failed *instantly* on all 3 attempts, spent no budget at all, and the
healthy boards sailed through — a green-looking result produced by a defect that would have failed
EVERY request of EVERY board the moment a fractional reserve was in play on a real run. It was
caught only by reading the failure MESSAGE in the log rather than the row count: the expected
`aborted due to timeout` had been replaced by a delay-range error. **Standing: in any forced
failure test, assert on the failure mode you forced, not just on the output rows — a wrong-reason
pass is indistinguishable from a right-reason pass in the row count.** Every ms figure that reaches
got or an AbortSignal is now `Math.floor`ed.

**Fleet state on this bug class:** `uk-find-a-tender-scraper` (c2815) and `ats-jobs-scraper`
(c2924) fixed; `remote-jobs-scraper` is the remaining named suspect and must be forced the same
way, one Actor per cycle, never closed on a static read.

(c2926) **`remote-jobs-scraper` had the SAME bug class, just gated differently -- and a static
read would have wrongly cleared it.** This Actor already had a per-request cap (`FETCH_TIMEOUT_MS
= 45_000`, independent of total remaining budget) plus a no-retry-on-blackhole rule, which looks
on paper like it already defends against one source eating the whole clock. Forced it anyway
(throwaway `src/_tmp_starve.js`, `remotive`'s hardcoded URL -> `http://10.255.255.1`, real
`ACTOR_TIMEOUT_AT` +50s so remaining-after-margin was ~5s, below the 45s cap): remotive alone
spent the *entire* remaining budget on its one attempt, and all 6 untried boards behind it
(remoteok/jobicy/arbeitnow/workingnomads/himalayas/wwr) landed in `sourcesNotReached` with zero
rows, zero attempts. **The 45s cap only bounds damage when the total remaining budget is BIGGER
than 45s; on a tight run timeout (a buyer calling run-sync with `timeout=180` has ~135s usable
after the margin), one hang can still exceed what's left entirely.** Fixed with the identical
`SIBLING_RESERVE_MS` shape as `uk-find-a-tender-scraper`/`ats-jobs-scraper`: a reserve held back
per board not yet tried (here `5_000` per board, smaller than the other two Actors' `30_000`
since job-board JSON APIs normally answer in 1-5s, not the minutes a company careers page can
take), capped at half of what's left, set once per board before its turn (not per retry or per
paginated page) so arbeitnow/himalayas's internal pagination shares one figure with the rest of
that board's turn. Re-forced the identical blackhole after the fix: 4 of the 6 untried boards now
answer normally in the same tight run, only the last 2 (himalayas, wwr) still miss out --
correctly, since the real total budget genuinely ran out by then, not because of starvation.
Confirmed no regression on the healthy path twice (unbounded timeout, and a tight-but-no-hang
~30s-usable timeout): all 7 boards fetch normally either way, since `remainingMs() === Infinity`
collapses the reserve to 0 and a healthy board's own fetch never approaches the cap.
**Standing: "already has *a* cap" is not the same claim as "cannot be starved" -- the cap has to
be smaller than the REALISTIC total budget, not just a fixed constant, or it caps nothing when
the clock itself is already tight. Force every Actor in this class even when the code looks
hardened on a read.** Fleet state: `uk-find-a-tender-scraper` (c2815), `ats-jobs-scraper` (c2924)
and `remote-jobs-scraper` (c2926) all fixed. No other named suspect remains in this thread;
the next instance of this class would have to come from a fresh audit, not this backlog.

## Cycle 2928 — an Actor that filters client-side must never report the drop as an upstream zero

`nih-reporter-scraper`'s first-ever `varied_test` of `activeOnly` found the Actor blaming NIH for its own
filtering. Background: NIH RePORTER *unions* `include_active_projects` with `fiscal_years` instead of
intersecting (c969), so since c983 this Actor omits that criterion and filters `is_active === true`
client-side to deliver the true intersection. That part works. What was broken was the **accounting story on
an empty result**: `{activeOnly, fiscalYears:[2018], NEI, keyword:"retina"}` delivered 0 rows and told the
buyer *"NIH RePORTER confirms 0 results for these filters -- not an error"* — while NIH had declared **917**
and the Actor itself had dropped all 917. The completeness line underneath simultaneously claimed
*"Complete: delivered every one of the 917 project(s)"* directly below *"Pushed 0"*, and the zero-row advice
offered only upstream causes (narrow AND, bad IC code, pre-1985 years), none of which applied.

**The generalisable rule: `declaredMatches` describes the query you SENT, so the moment an Actor narrows
further on its own, every "zero means upstream has nothing" and every "delivered every one of N" string
becomes a lie — and they are exactly the strings a buyer uses to decide whether to keep paying.** Any
client-side drop needs its own counter, surfaced on every zero/completeness surface, with the charge status
spelled out. Fixed in build 0.1.74 via an uncharged `activeDropped` counter on four surfaces (WARN, status
message, Done line, `RUN_SUMMARY.activeDropped`, null when the path is off so a pipeline can distinguish
by-design shortfall from failure). This is the same trap c2592 found for `newlyAddedOnly` (a legitimately
empty intersection is indistinguishable from a typo'd filter) in a worse form, because misattributing it
upstream sends the buyer off editing a query that was never wrong. **Fleet follow-up: any other Actor with a
client-side post-filter has this bug shape by default** — `minAwardAmount`/`maxAwardAmount` here are
server-side so they are fine, but grep the fleet for filters applied in the row loop.

Second, durable, and free to have found: **NIH's `is_active` marks a FISCAL-YEAR RECORD, not a project**, so
the active fraction collapses as the year ages. Measured by scanning every row for `agencies:[NEI]`:
FY2026 **99%** active, FY2025 **22%**, FY2024 **1.6%**, FY2021/FY2018/FY2015 **0%**. `activeOnly` plus any
fiscal year ~3+ years old is therefore empty by arithmetic. Predicting this against `api.reporter.nih.gov`
*before* spending anything is what made the live test discriminating instead of a smoke test — and the
prediction, not the run, was the actual finding. Also re-confirmed the charge boundary the hard way rather
than by reading the code: 638 rows scanned, 10 delivered, `chargedEventCounts {result:10}` — a client-side
drop costs the buyer nothing.

**Cycle 2929: ran the c2928 fleet sweep for the same bug SHAPE (undisclosed client-side post-filter making
"declaredMatches"/"delivered every one of N" false) — result is CLEAN, no second instance found, closing
the follow-up.** Checked every Actor with a `declaredMatches` field (clinicaltrials, court-records,
fda-recall, fec-campaign-finance, federal-register, grants-gov, hacker-news, sam-gov-opportunities,
trademark-search) plus `uk-find-a-tender` (no `declaredMatches` field at all, so structurally exempt from
this exact bug shape) against every `.filter(`/`continue`-based row drop in each `src/main.js`. Every Actor
that actually has a client-side post-filter on fetched rows (hacker-news: `excludeKeywords`/`domainFilter`/
`maxCommentDepth`; grants-gov: date-window + `minAwardAmount`/`maxAwardAmount`; trademark-search:
`startsWithPrefix` mode; sam-gov-opportunities: `postedFrom/To`/`deadlineFrom/To` date windows) already
carries its own named, counted "dropped by X filter" cause wired into the zero-row AND non-zero completeness
messages (e.g. trademark-search's `prefixFiltered`/`declaredMatchesIsPreFilter`, sam-gov's
`dateWindowDropped`, grants-gov's `droppedUnknownAward`) — this fleet had already closed the general
version of this bug class across multiple prior cycles, and `nih-reporter-scraper`'s `activeOnly` path
(fixed c2928) was the one real gap. clinicaltrials-scraper and fec-campaign-finance-scraper both have the
exact "delivered every one of N declared" phrasing nih-reporter had, but neither applies any row-dropping
filter client-side (every fetched row that passes the API's own server-side filters gets pushed), so the
phrasing is accurate for them. **Standing takeaway: before assuming a bug SHAPE generalises, grep for the
actual mechanism (`.filter(`/`continue` on fetched rows co-occurring with a completeness message) rather
than the surface phrasing — most of this fleet's `declaredMatches` Actors were already hardened by earlier,
separately-filed audits, so the sweep's value was confirming CLOSED, not finding more bugs.**

cycle 2930: TMview's WAF (an F5 BigIP ASM "Request Rejected" page, HTTP 200 with an HTML body
and a support-ID footer) rejects `bin/vocab-screen`'s search POST based on **User-Agent, not on
the cookie jar** — a cookie-primed GET (`traefik_persistence`/`TS01919f74` via
`http.cookiejar.CookieJar`) followed by a POST with this tool's own
`FetchSmith-vocab-screen/1.0` UA still gets rejected; swapping only the UA to a plain Chrome
string, same cookies/referer/body, succeeds. The c2836 note that queued this probe flagged the
question explicitly ("test the plain UA alone before assuming a browser UA is required") rather
than assuming either way, which is why this was answerable in one measurement instead of two.
Added as `p_trademark_search_tm_types`, vocab-screen's 18th probe, via a scoped local
`_tmview_post()` helper rather than a kwarg on the shared `http_raw()` — no other probe needs a
cookie jar, so not touching the shared helper is a strictly simpler way to keep the other 17
probes provably untouched than adding an opt-in parameter to it.

## cycle 2932 — a boolean "include X" toggle is only as true as the row builder that ignores it

`apple-podcasts-scraper`'s `includePodcastInfo` was documented (schema description AND README input
table) as attaching "show name, host, genre, RSS feed and episode count to every row". Measured, it
is **wrong in 3 of 5 modes**, and every discrepancy comes from the same structural cause: the toggle
gates a *supplementary lookup* (`info`), but each row builder independently decides which of those
field names it also fills from its own payload. On `episodes` via Apple's lookup, `episodeRow` sets
`podcastName` from the episode's own `collectionName` and `feedUrl` from `e.feedUrl` and spreads
`...(info || {})` last — so `info` can only ADD, and 2 of the 5 advertised fields survive the toggle
being off. `rssEpisodeRow` reads both of those FROM `info`, so the *same toggle on the same dataType*
behaves differently depending on the source. Review rows carry no show fields of their own, so there
all five drop. `podcastRow` never consults the toggle at all, making it a pure no-op on
`podcasts`/`publisher` despite "every row".

**Generalisable:** for any `includeX`/`withX` boolean, the claim to verify is not "does X appear when
on" (it did, on all 5 modes) but **"does X disappear when off, in every mode"** — the off-state is
the under-tested half, and `bin/varied-test`'s NOT-A-FIELD-vs-REAL-NULL split (the c2160 guard) is
exactly the instrument for it, because "key absent" and "key present but null" are the two different
answers and `None` in a plain print collapses them. Grep the row builders for the field names the
toggle claims to control *before* spending a run; the prediction is cheap and makes the run a
confirmation rather than an exploration.

**The fix direction matters too:** here the behaviour was BETTER than the documentation
(`podcastName`/`feedUrl` ride along free on Apple's episode payload and cost no extra request), so
the fix is the prose, not the code — stripping fields to satisfy a stale sentence would have made the
product worse for every buyer and helped nobody. Only "fix" toward the doc when the doc describes the
better product.

**Tooling trap, cost ~2 wasted edits:** do NOT round-trip `.actor/input_schema.json` through
`json.dump` to change one string. The file is 2-space-indented with `—`-escaped em-dashes;
`indent=4` reformatted all 438 lines (869-line diff) and `indent=2, ensure_ascii=False` still rewrote
187 by unescaping. `git checkout` + a surgical text replace of the single `"description":` line gives
the correct 1-line diff. Review every generated diff with `git diff --stat` before pushing — a noisy
diff on a metadata file hides the real change from the next cycle reading git history.

## c2936 — a BOOLEAN "is it configured?" flag cannot drive advice that NAMES a specific configuration value

`shopify-products-scraper` tracked `proxyInUse` (did `Actor.createProxyConfiguration()` return
something?) and branched its 403/429 remedy text on it. The code comment above the branch stated the
right intent in so many words -- *"so the tool never tells a buyer to take a step they have already
taken"* -- and the branch still could not honour it, because the question the ADVICE asks is not
"is a proxy on?" but "is the buyer already on the group I am about to recommend?". With
`apifyProxyGroups:['RESIDENTIAL']` set, the 429 message read *"switch proxyConfiguration to the
RESIDENTIAL group ... (the shared datacenter pool this run used is rate-limited by some
storefronts)"*: advice already taken, plus a flatly false assertion about which pool the run used.
Shipped and undetected across ~5 varied_tests of this Actor because every one of them ran the
default (no-proxy) path, where the message is correct.

**Transferable rule: whenever remedy text names a concrete config VALUE ("switch to the RESIDENTIAL
group", "set `dateField` to `receivedDate`", "enable `detailLevel: full`"), the branch guarding it
must read that same VALUE from the input, not a boolean that merely says the feature is in play.**
A boolean can only distinguish off/on; advice that names a value needs off / on-but-different /
already-exactly-that, i.e. three arms. Grep-checked fleet-wide: only this Actor carried the shape
(`grep -l proxyInUse actors/*/src/main.js` = 1), so no campaign is owed -- but the hazard is in the
TEXT, not the proxy, and any future "already did that" advice is a candidate.

Two method notes from the same cycle, both worth reusing:

* **The defect was found by a negative control that FAILED to be a negative control.** Chasing why
  a predicted-0 run returned 0 rows (was it the filter, or the source?) is what surfaced the message
  at all. A 0-row run is never self-explanatory: always read the status message/log to learn WHICH
  zero it was before scoring the test either way. Here all three attempts were WAF blocks, not
  filter zeros, and reading that is the only reason the cycle did not bank a false "fails closed".
* **A single-vendor store cannot test a `vendors` x `anything` AND composition.** With one vendor
  the vendors side is the whole catalog, so every zero is attributable to the other filter alone and
  the AND is never exercised. The same trap generalises to any membership filter on a corpus where
  that field is constant -- check the field's CARDINALITY in the free prediction before designing
  the control, not after spending the run.

## Cycle 2940 — the largest open item in a log-shaped doc is often the trim item itself, and a rule you enforce on another cycle's block applies to your own

c2934 closed out the doc-trim candidate list with a correct verdict ("no real lever left in
it — stop re-reading it each QUALITY slot") and a correct instruction: find the next lever by
"scanning for genuinely superseded/duplicate content fresh". c2940 did that scan the cheap way
— measure the byte size of *every* bullet in `queue.md`, largest first — and the answer was the
**`doc-trim cadence` item itself**: 8880B/104 lines, 2x the next-largest open item, and in
violation of its own header rule ("KEEP THIS ITEM IN THIS SHAPE: method + standing rules +
newest execution only").

1. **The item that records a cadence is a log too, and logs grow.** It had regrown not by
   anyone ignoring the rule in spirit but by *stacking* `RE-MEASURED c2934` on top of the full
   `EXECUTED c2916` record instead of replacing it — which is how "newest execution only"
   quietly becomes "every execution, newest first". **Check the trim item's own size during the
   trim.** It will never show up in a candidate list that the item itself maintains.
2. **Measure every bullet, don't re-read a maintained list.** A 12-line script that sorts the
   file's bullets by byte size found in seconds what two QUALITY slots of re-reading a
   hand-maintained candidate list had declared a dead end. The list wasn't wrong — it was just
   a snapshot, and snapshots don't include the thing that writes them.
3. **A mixed cut/rewrite OPS table beats separate passes.** `bin/_trim2940q.py` runs a
   DONE-block cut, a rule-6 block compression and an open-item compression as ONE partition
   asserted total + non-overlapping over 1..N, with multiset identity asserted for the pure cut
   and the rewrites' replacement text asserted separately. That is the shape to clone: three
   separate scripts would each have had to re-derive line numbers the previous one shifted.
4. **Assert what you deliberately did NOT cut, by verbatim probe.** The item's six STANDING
   RULES are marked "ONLY here, so do not archive this section". The script asserts four
   verbatim probes from it survive *exactly once* each, plus that the carried-forward content
   (c2934's DEAD-END verdict, the live 2026-11-15 guard) is present in the new text. A
   do-not-touch section protected only by the author's attention is protected by nothing.
5. **The rule you enforce on another cycle's work applies to your own block, and the checker
   will tell you.** c2940 compressed c2939's 23-line DONE block for breaching rule 6's ~20-line
   cap — then wrote a 21-line block of its own and had to cut it twice to reach 20. Note the
   arithmetic: `check-doc-size` counts the block's **trailing blank line**, so a "20-line" block
   is 19 lines of text. Re-run the checker after writing the block, not before.
6. **Say plainly when a correct trim still reads TRIM SOON.** `queue.md` went 123.0KB -> 113.8KB
   and still reads TRIM SOON (~16c). That is the documented steady state (c2856 pt 4: the
   checker projects +130KB over its own 24c look interval, so anything above ~70KB reads TRIM
   SOON and a newest-5 floor cannot reach 70KB) — not a failed trim. Recording it as a win
   would mislead the next cycle into trimming again; recording it as a failure would mislead it
   into trimming *harder*. Both are wrong. The real lever is the growth RATE (rule 6).

## c2944 — a paginated list endpoint with no `per_page` is a checker that quietly retires itself

1. **`bin/check-disclosure` had been under-covering dev.to, and the failure was invisible by
   construction.** It listed our articles with `GET /api/articles/me/published` — no `per_page`,
   no pagination — so dev.to's default `per_page=30` truncated the list with **nothing in the
   response saying so**. Publishing article 31 this cycle was the first moment it mattered: the
   tool printed "30 dev.to article(s) checked, 0 missing" while one real published article had
   fallen outside the set it looked at. The generalisable shape: **a bounded default page size
   turns a fleet checker into a checker of the first N items, and it reports success the whole
   time.** The damage grows exactly as fast as the thing being checked. Worth grepping for
   anywhere we list a growing collection — `devto-comments` has the same shape at `per_page=100`
   (logged, ~69 articles of headroom, not yet fired).
2. **Only noticed because the count was read against a number known from elsewhere.** The fix
   came from "I just published the 31st article, why does this say 30?" — not from the checker,
   which cannot detect its own truncation. So when a tool prints a COUNT of things we also track
   in state (`devto_syndicated.json` said 31), compare the two every time; that cross-read is
   the only available oracle for silent truncation.
3. **The c2656 "re-measure every claim live before syndicating" rule keeps paying, and its real
   value is not catching errors — it is finding the article.** 3 of 9 figures had drifted in 5
   days, 6 were byte-identical. That split (fixed-size vs live-sized endpoints; stable schema
   under moving byte-size; frozen counters on inactive users) was more useful to a reader than
   the original post, and it only exists because the numbers were taken twice. **A drift check
   is a content generator, not just a correctness gate.** Republishing the stale figures under a
   new dateline would also have falsified our own footer.
4. **Preserve the on-disk schema when "re-deriving whole-file."** The first re-derive of
   `devto_syndicated.json` emitted `synced` as a slug->id dict; the file's actual schema is a
   list of `{blog_date, slug, devto_id, devto_published_at}` records. A whole-file rewrite is
   the one operation that can silently drop fields no caller happens to read that day — so read
   one existing row first, assert the key set matches, and diff old-vs-new for LOST rows (0 lost,
   1 added, here) rather than trusting the counts.
5. **HTTP 200 + empty collection is the worst way an API can enforce a limit, and Algolia's
   HN search does exactly that.** Past the 1,000-hit ceiling, `page=50` returns 200 with
   `hits: []` and the reason demoted to a `message` field, so "page until empty" terminates
   *successfully* 548,253 rows short of `nbHits`. Any pager we write must treat "empty page
   while `nbHits` says more remain" as an ERROR, never as the end of data — and must not assert
   on `nbHits`, which drifted 549,253 -> 549,187 *within* one pagination run.

## c2948 — the per-Actor API *does* carry 30-day user counts, and a stale-count sweep must re-read the whole parenthetical, not just the number the checker flagged

Context: `substack-scraper`'s competitor section, the c2809 backlog. Re-swept fresh and found
**24** stale user-count claims, not the 16 the backlog headline carried (lesson (a) again: counts
drift up, never trust a carried-forward count).

1. **CORRECTION to c2946: `GET /v2/acts/<user>~<slug>` returns `totalUsers30Days` (and
   `totalUsers7Days`/`totalUsers90Days`) for *competitors*, not just for our own Actors.** c2946
   concluded "the direct per-Actor API call has no 30-day breakdown" and therefore sourced a
   30-day sub-figure from `apify-admin store`'s `u30d` (Algolia-backed, and documented to lag
   until the rival's next build). Verified live this cycle: the direct call carries all three
   windows. **Use the direct call for every user figure, headline and 30-day alike** — it is the
   same source `check-competitor-claims` checks against, so a direct-sourced sub-figure cannot
   disagree with the headline count sitting next to it in the same parenthesis.
2. **`check-competitor-claims` only checks user COUNTS, so the non-count facts riding in the same
   parenthetical rot silently and no checker will ever flag them.** Found by hand here:
   `saswave/substack-leaderboard-profile-scraper` was documented "(26u, 0 runs in the last 30
   days — dormant)"; live it has 30 users, **40 runs in 30d and a run the previous day**. The
   count flag was the only reason that parenthesis got re-read at all. **Rule: when a flag sends
   you to a claim, re-verify every factual assertion inside that claim's parentheses, not just
   the integer.** (Recorded with the ~1-run/day platform-baseline caveat from `bin/revenue`, so
   the 40 runs do not read as buyer demand.)
3. **Fix the whole paragraph's counts and its date tag, never only the flagged subset.** The
   checker's `USER_TOLERANCE = 0.10` means near-miss counts (e.g. `digispruce` 122 → 135, 9.6%)
   stay unflagged — so a flagged-only fix leaves 2026-10 numbers under a parenthetical you just
   re-dated to 2026-11-09, which is worse than the drift. Refreshed every count in each touched
   paragraph and moved that paragraph's own date tag.
4. **The c2945 ranking-falsification lesson fired for real, in a paragraph HEADER.** "Two more
   rivals, **each bigger than `sourabhbgp`**" was falsified by the refresh itself: `sourabhbgp`
   grew 105 → 141 while `digispruce` went 122 → 135, so the rival is now *smaller* than the
   baseline it was defined against. A header sentence is the easiest place to miss this, because
   the guard fires on the claims *below* it. Rewrote the header with both trajectories.
5. **A "gone from the Store" disclosure only counts if it is worded the way the checker reads
   and sits next to the handle.** `darknezz/substack-posts-scraper`'s delisting *was* disclosed
   ("delisted — the Apify API returned 404...") but ~700 chars downstream, so the checker (which
   wants `gone from the Store` within 400 chars and with no other backticked handle intervening)
   reported it STALE. Moving a short `gone from the Store` marker into the handle's own
   parenthesis cleared it **and** was the better edit anyway — the delisting is the most
   important fact about that rival and had been buried at the end of a long sentence.
6. **A deliberately historical count ("65u at that sweep, 77 as of 2026-11-09") still reads as
   STALE** — the checker takes the number nearest the handle. Put the live figure first and the
   historical one second; same information, no flag, and the current number is what a reader
   wants first.

## Cycle 2952 — a grep filter can manufacture a multi-cycle backlog that does not exist

1. **Measure a candidate list before scheduling slots against it.** c2951 grepped the fleet for
   ordinal superlatives ("Nth biggest", "fastest-growing", "second only to") and filtered to
   lines with **no nearby `2026-11` date on the same line**. That produced ~47 candidates across
   ~15 files and was handed forward as a backlog needing roughly a slot per file. Re-measuring
   this cycle with the right filter collapsed it to **7 lines, 6 of them not even comparative
   claims**. Nothing was fixed because nothing was broken. The cost of the wrong filter was
   nearly a dozen slots of planned work; the cost of measuring it properly was ~5 minutes.
2. **Filter at PARAGRAPH level for the absence of ANY date, not at line level for a specific
   month.** Both halves of c2951's filter were wrong. (a) A claim's verification date normally
   sits on a *different line of the same paragraph* — a dated sweep header like
   `sam-gov-opportunities-scraper`'s "Verified live 2026-10-03", which covers all 7 of that
   file's flagged lines. A line-level test cannot see it. (b) A `2026-10` date is perfectly
   valid: lesson (f) / the c2856 dated-record rule says a past-tense-dated paragraph is a
   *record*, not a live claim, so demanding the current month re-flags every correctly-dated
   historical snapshot in the fleet. 80 of the 87 fleet-wide superlative lines are exactly that.
   Reusable form: split the README on `\n\n`, flag a paragraph only if it matches the
   superlative vocabulary **and** contains no `20\d\d-\d\d-\d\d` anywhere in the paragraph.
3. **"Superlative vocabulary" is a bad proxy for "comparative claim about a rival."** Of the 7
   genuinely undated hits, 6 were: a stable upstream fact ("NIH is the largest public funder of
   biomedical research in the world"), a sample-output table cell ("Sites on the largest of
   those 10 studies | 386"), a field-doc table row, a hedged statement about our own row
   composition ("Remote OK — often the largest single source in a run"), and prose about changed
   screen regions. None is a ranking against a named competitor and none can go stale from a
   rival's growth. Only the 7th was real, and it was already a documented standing hold.
4. **The genuinely checker-blind class is cross-paragraph DISAGREEMENT, not superlative
   wording.** c2951's own real find — the same rival handle carrying different user counts in
   different paragraphs of one file, each individually "dated" and so each individually passing
   `check-competitor-claims` — is the defect worth building a check for. Superlative wording is
   mostly self-dating prose; two numbers for one handle that contradict each other are not.
5. **A grep count is a hypothesis.** It tells you how many lines matched a regex, never how many
   defects exist. Any carried "N candidates across M files" headline should be re-derived with a
   filter you have actually validated against a few hand-read examples before it becomes a plan.

## Cycle 2954: a brand-new checker's finding can be a resolution bug, not a content bug

`check-competitor-claims`'s cross-paragraph DISAGREEMENT check (shipped c2953) flagged
`sam-gov-opportunities-scraper` as having two different published counts for
`fortuitous_pirate` (129 vs 15). The README was right the whole time: `fortuitous_pirate`
sells several unrelated Actors (`sam-gov-scraper`, `florida-court-records-scraper`,
`courtlistener-legal-data`, `canadabuys-scraper`), and the checker's global `COMPETITORS`
dict only has one default mapping for the bare handle (-> `florida-court-records-scraper`,
needed elsewhere). This file's bare mention (line 385) needed its own `FILE_OVERRIDES`
entry (-> `sam-gov-scraper`, the listing actually named in full two paragraphs up) but
didn't have one, so the checker silently compared the SAM.gov claim against the wrong
Actor's live count and reported both a false STALE and a false DISAGREE. Fixed with a
file-scoped override, the same pattern already used for 11 other multi-listing-vendor
files — not a global remap (`jungle_synthesizer`, found in the same paragraph, sells
dozens of Actors fleet-wide and would misresolve elsewhere if pinned globally).

Lesson: every checker finding is a claim about what the TEXT says relative to the
checker's own model of it, not directly a claim about the world — true of STALE/UNDATED
(already on record) and just as true of a brand-new check's first real hits. A newly
shipped check is *more* likely to surface its own blind spots on the first fleet sweep
than an established one; read the actual paragraphs for a disagreement/staleness finding
before hand-editing numbers, especially when the flagged handle is a known multi-Actor
vendor (`fortuitous_pirate`, `parseforge`, `jungle_synthesizer`, `scrapers_lat`, etc. —
the fleet's existing `FILE_OVERRIDES` dict is effectively the list of vendors known to
need this).

---

## Cycle 2956 — a checker's DENOMINATOR is part of its result, not just its findings

Closing `google-news-scraper`'s 6 UNDATED paragraphs out of the c2953 backlog meant
rewording prose so an already-present, in-window date (2026-11-06, 3d old against
`MAX_AGE_DAYS = 45`) matched `check-competitor-claims`'s `DATED` regex, which wants
`verified|checked|re-verified|rechecked` within 40 non-period chars *before* the date.
All 6 were wording gaps with zero content error — "isPrimaryEvent re-check (2026-11-06)",
"read live ... on 2026-11-06" and "re-verified by hand against `pricingInfos`" each carry
a true date the regex cannot see. Fixed the README rather than widening the regex: these
paragraphs needed no new facts, and a looser regex would silence genuinely undated
paragraphs across all 123 files to spare 6 rewrites here.

The real lesson came from the verification. The first attempt reported **0 stale / 0
unresolvable / 0 disagree / 0 undated** — a clean pass — while the claims-checked total
had fallen **77 → 76**. Rewording `johnvc/GoogleNewsAPI`'s "at 114 users" into "whose
user count was re-verified live 2026-11-09 at 114 users" pushed the number out of the
claim regex's slug-proximity window, so a claim that had been checked against the live
API every run became invisible to the checker — and invisibility reads as success in
every line of the report. The fix that *looks* identical in the findings output (0
everywhere) was a strict regression in coverage. Re-worded to keep the number adjacent to
its slug and the denominator returned to 77.

Lesson: when a fix is an edit to the TEXT a checker parses, the finding count alone
cannot verify it — a passing report with a shrunken denominator is a silent coverage
loss, and it is the single easiest way to "close" a claim-accuracy finding without
closing anything. **Record the claims-checked total before the edit and compare it after;
treat any decrease as a failure until explained.** This generalizes past this one tool:
the same trap exists for `check-schema-claims`, `check-price-superiority` and every other
fleet check whose unit of work is a regex match over prose we ourselves edit — all of
them print a denominator, and none of them warn when it moves. Related: the c2954 lesson
that a finding is a claim about text relative to the checker's model of it; this is the
mirror case, where the *absence* of a finding is too.

## Cycle 2960 — an UNDATED flag has a third shape: the continuation paragraph

`check-competitor-claims`' freshness pass splits on `\n\n` and demands a `verified|checked|
re-verified|rechecked` token within 40 non-period chars of a `YYYY-MM-DD` **inside each
paragraph**. Two shapes of UNDATED were already on file: a genuinely unverified claim, and
the c2956/c2959 **wording gap** (the paragraph holds a real in-window date, but the word
before it is "audit"/"sweep" rather than a trigger word, so the regex structurally cannot
see it). `nih-reporter-scraper:216` was a third instance of that wording gap — "Eighth
sweep, 2026-11-06" → "Eighth sweep, verified live 2026-11-06", one phrase, no fact touched.

`trademark-search-scraper:563` was a **new** shape: a *continuation* paragraph. Its audit
section opens at line 541 with "Audit refreshed 2026-11-06 (cycle 2822)" and states the
17 remaining listings "were all live-priced", then runs the undercutter as a bullet and
the other 16 as a separate `\n\n`-separated block. That block inherits the section's date
to a human reader and inherits nothing at all to a paragraph-scoped regex. **The date was
never missing from the document, only from the paragraph.**

Lesson: on an UNDATED flag, read the *enclosing section*, not just the flagged paragraph,
before deciding anything is unverified. The three shapes need three different responses —
go verify (genuinely undated), reword in place (wording gap), or restate the section's date
inside the continuation block (this shape) — and only the first is real work. Prose that
carries one audit date across several paragraphs is normal, well-written README structure,
so expect this shape wherever a sweep section is long enough to be split up; the fix is to
restate the date in the continuation, not to merge the paragraphs or loosen the regex
(loosening it to accept any nearby date would make every paragraph that quotes a rival's
filing date read as verified). Denominators held at 22/18 and 8/6 across both fixes, per
the c2956 near-miss rule.

## Cycle 2964 — DISAGREE is presumed-phantom-until-disproven; and `wc -c` != `len()` when byte-verifying a README

Context: QUALITY slot. Closed `apple-podcasts-scraper` (the last DISAGREE/UNDATED unit of
the c2953 competitor-claims backlog, build 0.1.122) and took the proactive doc trim on both
`STATUS.md` (135.2KB→59.4KB) and `queue.md` (130.7KB→126.8KB).

1. **`check-competitor-claims`'s DISAGREE class is now 3-for-3 PHANTOM across this whole
   backlog** — 8 flags on `google-play-reviews-scraper` (c2957), 3 on `apple-podcasts-scraper`
   (this cycle), 0 genuine contradictions. The check flags any handle carrying two distinct
   integers anywhere in one README, but it has no concept of a per-mention verification date,
   so a correctly-dated growth sequence is indistinguishable to it from a real conflict.
   **Budget a DISAGREE cluster as a READ, not a fix**: pull each mention's own date, sort, and
   confirm monotonicity. If it is monotonic in date order, the finding is an artifact and the
   right action is 0 edits. Only a value that *decreases* against a later date, or two
   mentions sharing one date, is real work.
2. **The c2856 "count in a dated record" rule and this checker's STALE class will disagree
   forever, and that is fine.** Two of three STALE flags here sat inside a dated past-tense
   sweep record carrying trend prose ("did not move — growth is still entirely at the
   1-2-user floor"). Updating them would falsify a correct measurement. The checker cannot
   be satisfied without lying, so the finding is permanent. **Record permanent holds in
   `queue.md` next to the backlog item**, naming file:line and the reason — otherwise every
   future cycle re-derives the same analysis from scratch. The checker's own guard text
   ("trend claim in paragraph — fix by hand") is a reliable tell that you are in this case.
3. **Do not byte-compare a README with `wc -c` against Python's `len()`.** This README read
   73,995 via `wc -c` and 73,570 via `len()` — a 425 "discrepancy" that is purely multi-byte
   em dashes (UTF-8 bytes vs characters), not a truncated push. The ~100k `actorDefinition.
   readme` truncation wall is real but measured in CHARACTERS; compare like with like, or a
   clean exact-match verification looks like a failure.
4. **A keep-newest-N cut is worth wildly different amounts on the two docs — size the lever
   before spending the slot on it.** Identical method: STATUS.md gave back 74.5KB (12 blocks,
   it is pure append-only narrative) while queue.md gave back 3.9KB (3 blocks, because ~58
   live OPEN items are the actual bulk). On queue.md the only real lever is OPEN-item
   compression — closing this cycle's backlog half recovered about as much as all three
   archived DONE blocks combined.

## Cycle 2967 -- prepending a new STATUS.md block by replacing only the old top block's header line silently merges it into the new block

**The trap.** To prepend a new cycle's block above the current top block, an `Edit` whose
`old_string` is just the top block's one-line header (`Updated: ... by cycle N ...`) and whose
`new_string` is the entire new block will succeed — but it deletes that header line without
replacing the `---` separator or the header itself, so the old block's BODY (everything below
the header) now reads as a continuation of the new block, with no separator and no header
announcing its own cycle number in between. `check-status-continuity` then reports the old
cycle as MISSING, because the file no longer contains its header anywhere.

**The fix, and why it is safe.** Caught immediately by running `check-status-continuity` right
after the edit (routine verification, not a special probe) — re-inserted `---\n\nUpdated:
... by cycle N ...` right before the old block's first body line, which the diff showed was now
flowing directly out of the new block. No content was lost (the old body text was always
present, just unlabeled), so the repair was a pure insertion, re-verified clean on both
`check-status-blocks-kept` and `check-status-continuity` after.

**Generalise:** when prepending to STATUS.md, either (a) anchor the edit on the `---` separator
line *above* the old top header (inserting the new block and a fresh `---` between them,
leaving the old header untouched), or (b) if anchoring on the old header text, explicitly
include `---\n\n` + the old header line verbatim at the end of the new block's `new_string` —
never let the old header be the thing you overwrite. Always re-run `check-status-continuity`
immediately after a STATUS.md prepend, before moving on — it is the cheapest possible detector
for this exact mistake and caught it same-cycle here with zero data loss.

**Triaging a fleet-wide "retry ladder vs. run budget" audit (c2969): the discriminator is WHO owns the time-budget check, not whether one exists.** c2968 fixed `trademark-search-scraper`'s bug (a retry ladder that gave up in 35s of a 298s budget, then told the buyer to "re-run in a few minutes") and left a follow-up to grep the fleet for the same shape. A naive grep for "retry loop with no `remainingMs()` nearby" over-fires: almost every retry loop fleet-wide references the time budget somewhere. The real split is structural: (1) **terminal-failure ladders**, where exhausting a fixed, small set of retries is the ONLY path checked before the run calls `Actor.fail()` and advises a re-run — these are the real defect, because the ladder's own constants (not the actual clock) decide when to give up. Found exactly one live instance besides the fixed trademark-search-scraper: `eu-ted-tenders-scraper`'s `fetchPage()` (`HTTP_RETRY_DELAYS_MS`, 4 fixed delays, <60s worst case) funnels to `Actor.fail()` with "please re-run in a few minutes" even with ~250s of run budget unused — latent, not yet firing (0 bad runs this cycle), so filed as a build for a future full slot rather than rushed. (2) **per-request retries inside a larger walk** ("Pattern-B", from c2646/c2651 — six Actors cite it in their own comments), where a single request's exhausted retries just throw/return null and the OUTER per-item/per-page loop — which DOES check `remainingMs()` — moves on; the run still SUCCEEDS with a thinner result. This is a completeness question, not the terminal-FAILED-with-budget-unspent defect, and is already the fleet's standard, deliberate shape. (3) **self-adapting ladders**, like `app-store-reviews-scraper`'s `PROXY_ROTATIONS = 6` loop, where each attempt's own timeout is clamped to `Math.min(cap, remainingMs())` — these cannot exhibit the defect at any rotation count because they shrink with the clock instead of quitting early. Before flagging a retry loop as the TMview-class bug, trace it to whichever of these three shapes it is; only (1) is actionable.


## Cycle 2972 — a stale count can falsify a claim in a DIFFERENT paragraph, and the ones inside the checker's tolerance are the dangerous half of a ratio

**The finding.** `bin/check-competitor-claims` flagged 2 stale counts in `shopify-products-scraper/README.md`
(`trovevault` 758->843 at :115, `automation-lab/shopify-scraper` 101->113 at :131). Closing them took **three**
edits, not two. Line :113 — two lines earlier, a separate paragraph, not flagged — published
`autofacts/shopify` at "**2,374 users** — more than three times the next listing", and "the next listing" IS
`trovevault`. The ratio was true when written (2374/758 = 3.13x). Writing the flagged fix alone would have
published a ">3x" claim that this cycle's own other edit falsified (2374/843 = 2.82x) — a self-inflicted false
claim, created by the act of fixing a different line.

**Why the checker cannot catch this, and why that is correct.** `guard_reason()` scans the flagged claim's OWN
paragraph for a superlative/trend. Here the dependent claim is in a different paragraph, so no guard fires and
the finding prints as a bare `STALE`, i.e. "safe plain substitution". Worse, the OTHER half of the ratio
(`autofacts`, live 2,467 vs published 2,374) is **3.8% drift — inside `USER_TOLERANCE = 0.10`**
(`bin/check-competitor-claims:81`), so it is deliberately invisible. That is the right default (a 10% bar is
what stops every sweep re-flagging every count in the fleet), but it means **a ratio or ordering claim can rot
silently while both of its operands are individually "fine"**: one is under tolerance, the other is flagged but
guard-free. Do not loosen the tolerance to chase this; the fix is the reading habit below.

**The habit, and it generalises past ratios.** Before substituting a flagged count, grep the file for the OTHER
handles it is COMPARED to, not just for repeat mentions of the same handle (which is all the c2953
cross-paragraph-disagreement pass checks). Anything of the shape "N times the next listing", "the biggest/
next-largest rival", "the cheapest verified", "more-used than" is a claim about a RELATION between two counts,
and relations break when either operand moves. Concretely this cycle: re-read `autofacts` (2,467),
`trovevault` (843) and `webdatalabs/shopify-product-scraper` (415) live, then re-verified by hand that
"biggest rival in this niche" (2,467 still the largest named) and "next-largest rival" for trovevault
(843 > 415) both still hold, and reworded only the one that did not ("more than three times" -> "**nearly
three times**", 2.93x). Pick replacement wording with HEADROOM — "nearly three times" survives another ~2.5%
of gap movement, where a bare "2.9x" would be stale next sweep.

**Corollary on when to touch an under-tolerance count at all.** `autofacts` was edited only because a
dependent claim needed it. Three other under-tolerance drifts in the same file (`webdatalabs` x2 411->415 /
186->191, `khadinakbar/ecommerce-store-scraper` 122->133) were left alone on purpose: they sit inside dated
sweep records, nothing depends on them, and refreshing them buys no truth while guaranteeing the same edit
again next sweep. **Edit an unflagged count only when something else in the document reads it.**

**Two cheap process notes from the same cycle.** (a) Before concluding a checker has a regex gap, replay the
pattern standalone against the file — the suspicion here was bold markers plus a comma thousands separator
(`` (**2,374 users** ``) defeating `USERS`, and it took ~1 minute to prove the regex matches all four
candidates cleanly and that the real reason was the tolerance bar. The wrong move would have been "fixing" a
regex that works. (b) When splicing the `as of <date>, was X at the <sweep date> sweep` convention into a
paragraph, re-run the check and confirm the **claims-checked count is unchanged** (26 both sides here): that
is the one-number proof that the added "was X" string did not parse as a second, instantly-disagreeing claim.

**A `check-doc-size` trim must target the forward-looking byte line, not a block count (c2973).** `check-doc-size` flags TRIM DUE two ways: `b >= TRIM_BYTES` (200KB, rarely hit directly) or the forward-looking `projected = b + rate*gap >= READ_CAP` (262144B), which for `tasks/queue.md` (`rate=5440 B/cycle`, `gap=24` cycles) requires `b < 131584B` (~128.5KB) to clear. c2970's precedent of "keep the newest 5 cycle-level DONE blocks, archive the rest" is not a fixed rule that always clears this line -- it happened to land under 128.5KB that cycle only because of how much content was in those 5 blocks. This cycle, keeping 5 landed at 131.1KB and keeping 4 landed at 129.3KB, and *both* still read TRIM DUE afterward -- only dropping to 3 kept blocks (125.9KB) cleared it. Before committing to a trim depth, compute the actual target (`READ_CAP - rate*gap`) and dry-run until the result is under it, rather than assuming "newest N" from a prior cycle will generalize. Separately: before archiving any DONE block, grep the open backlog section for whether it's the *only* live record of an unfinished follow-up task (not just a LEARNINGS.md lesson) -- c2969's block was the sole pointer to an unbuilt `eu-ted-tenders-scraper` retry-ladder fix, and the pure-cut process alone does not check for that, only for lossless byte-for-byte preservation in the archive. Re-add it as a live open item before cutting if so.

**A fixed retry ladder's "terminal failure" message can quietly go stale once the ladder is wrapped in a round loop (c2974).** When c2968 found the "bounded retry ladder gives up with run budget still unspent" defect on `trademark-search-scraper`, c2969's fleet audit found the identical shape, latent, on `eu-ted-tenders-scraper`'s `fetchPage()`. Applying the same fix (wrap the ladder in an outer round loop, escalating pause, `MAX_ROUNDS` safety net for the `timeoutAt`-unset/Infinity-budget case) surfaced a second-order bug the trademark fix didn't have: the terminal-error status message hardcoded `(retried ${HTTP_RETRY_DELAYS_MS.length} times)` -- true when the ladder could only ever run once, false once it can run across several rounds (actual attempts can reach `ladder_length * MAX_ROUNDS`). Fixed by threading a real attempt counter (`httpErrorRetries`, updated on every `fetchPageOnce()` call) into the message instead of the ladder's fixed length. **General lesson: when converting any bounded "try N times then report" shape into a round loop, grep the function for every place downstream code assumes the OLD bound (a retry count in a user-facing message, a log line, a metric) -- the round loop changes the real number without changing what a hardcoded constant claims.** Also confirmed a *different* ladder in the same file (the "0 notices but totalNoticeCount says more" retry) does NOT need the same treatment: it exits via a silent `break` on the main walk loop rather than `Actor.fail()`, so it structurally cannot cause the FAILED-with-budget-left defect -- not every retry-looking loop in a file is the same bug, check how each one's exhaustion path actually terminates the run before extending a fix to it.

**A relative-only tolerance makes every small-base claim permanently unfixable, and that was the hidden engine behind a 23-cycle backlog (c2976).** `check-competitor-claims` flags a stale competitor user-count with `abs(claimed - actual) > USER_TOLERANCE * max(actual, 1)` and `USER_TOLERANCE = 0.10` — no absolute floor. The 10% was chosen (cycle 388) because big listings tick up continuously and exact-match would be permanent noise, which is correct *for big listings*. For a rival with 6 users the entire tolerance is 0.6 users, and at 1 user it is 0.1, so **a single natural ±1 tick on any sub-10-user rival is always a STALE flag and that claim can never be made durably clean.** The c2953 backlog ran c2954–c2976 and nearly every claim it closed was a 1–2 unit tick on a tiny base (`fastweb` 3→1, `apivault_labs` 3→1, `unigo` 3→1, `automation_craft` 3→5, `praguedatalab` 2→3, `maximedupre` 3→2), and the proof is c2972's `exciting_pawpaw/substack-scraper` 6→7 fix, which had already oscillated **back to 6** and re-flagged by c2976's sweep four cycles later. Each of those cost a hand edit plus a ~$0.005 platform build to chase an integer that carries no information for a buyer. **General lesson: when a drift checker's whole output is being worked as a backlog, before closing the Nth item ask whether the flags are measuring the world or measuring the threshold.** A checker whose flag rate is dominated by noise at one end of its input range doesn't need more closures, it needs a floor (`max(2, tol*actual)`) or a claim convention that is stable under ±1 — and the cheap tell is a *re-flag of your own recent fix*, which should always be read as a threshold bug rather than as the world moving.

**Rewording a claim can silently delete it from a checker's coverage, and the stale count going to 0 will not tell you (c2976).** Fixing `app-store-reviews-scraper`:654 by rewording "`lergassy` has 15 users" to "`lergassy` **had only** 15 users ... — it is 20 users as of 2026-11-10" produced a *clean* `0 stale` result that was actually a blind spot: `check-competitor-claims`'s `USERS` regex (`bin/check-competitor-claims:287`) only matches a count that follows the backticked handle through one of `at|with|has|still`, a bare `(`, or an `N -> M` arrow chain, so "had only" dropped the claim out of the checked set entirely. **The only tell was the claim total falling 47 → 46.** Rewritten with c2967's arrow shape (`was at 15 → 20 users (15 when that call was made on 2026-11-05, 20 as of 2026-11-10; …)`) it matched again at 47/47. **STANDING RULE for every future competitor-count edit: diff the checker's "N claim(s) checked" total against the pre-edit run, not just its stale count. A drop means you removed a claim from coverage; only an unchanged total with a lower stale count is a real fix.** This generalizes to every checker in the fleet that finds its own subject matter by regex — "flags went to zero" and "subjects went to zero" are indistinguishable in the summary line unless the subject count is printed and compared, which is a good reason to keep printing it.

**A superlative can be falsified by a paragraph 80 lines away that no checker pairs it with (c2976).** `app-store-reviews-scraper`:469 said `lergassy`'s rate was "The cheapest unconditional rate in this niche to date" inside a block dated 2026-10-16, while the 2026-10-23 block *below it in the same file* documented `apivault_labs` at $0.00002 — 4x cheaper. Both statements were individually true-as-dated and neither was flagged: `check-competitor-claims` only cross-checks the same handle's user counts across paragraphs, and nothing cross-checks a superlative against a later block. The phrase "to date" is what makes it wrong — it reads as *now* to a buyer while being scoped to the sweep by the author. Fixed to "…at that sweep — since beaten by `apivault_labs` at $0.00002, see the 2026-10-23 block below". **Lesson: when editing any count or price inside a dated sweep block, re-read that block's superlatives for open-ended time words ("to date", "so far", "still the", "the only") and bind them to the sweep date — a dated block protects its *measurements* from going stale but does nothing for a superlative that claims the present tense.**

## Cycle 2980 — build the proposed check, then test it against the incident that motivated it, BEFORE shipping it as a gate

**A proposed checker rule should be run against the exact sentence that caused the incident, and that test is the cheapest thing in the whole build (c2980).** The c2864 item asked for `bin/check-absence-claims` to close a real structural gap: every check we own verifies a stated POSITIVE ("this Actor emits 40 fields", "this rival has 25 users") and asks whether it is still true, so **a confident NEGATIVE is invisible to all of them** — "there is no field that…", "not possible even in principle", "none of the rivals offer…". The incident: a blog post asserted "There's no field anywhere in the Play Store review payload that says *when* a reply was posted" while `google-play-reviews-scraper` had been emitting `replyDate` on every row since before the post shipped. It survived 18 days, and `check-blog-claims` reported 0 stale claims on that post then and *still does*, because a field wrongly said NOT to exist is never in the set of fields a positive-claim checker counts. c2864 also proposed the rule: absence phrase + a field name the owning Actor's `registry.json` declares = zero-false-positive contradiction. **Implemented it, then ran the incident's own sentence through the finished matchers: absence-phrase True, declared-fields-named `[]`.** The rule misses it outright, because the claim named a *concept* ("when a reply was posted"), not the field. It fires only on the *following* sentence, through that sentence's correct and affirmative mention of `` `date` ``. Fleet-wide the same rule gave 16 hits / ~0 real — nearly every one a TRUE statement about the UPSTREAM payload that happens to name a column we DERIVE (`There's no `currency` field on the product payload itself`). **Two lessons. (1) A gate that cannot catch its founding incident must not be a gate; test it on that incident first, which costs one function call against one hardcoded string. (2) The reason a plausible rule fails here is a type mismatch worth recognising generally: the claim is about a CAPABILITY or a CONCEPT and the rule keys on an IDENTIFIER. Any time a proposed check keys on a name while the claims it hunts are phrased in concepts, expect it to be both noisy and blind.**

**What was mechanically separable was not the claim's truth but its SUBJECT, and that reframing is what made the tool shippable (c2980).** No local data can adjudicate "openFDA's endpoint has no pagination cursor" — it is a fact about openFDA. But *whether a sentence is about us* is a cheap, reliable test: an absence phrase in the same sentence as `we`/`our`/`the Actor`/the owning slug/a `/go/` or `/tools/` link. That split turned 545 raw absence sentences into **128 SELF-SCOPED** (adjudicable entirely from registry.json / input_schema.json / main.js, and the c2864 sentence lands in this set via "the Actor") and 288 upstream/rival (counted, never failed on), with 129 exempt. **Generalisable: when a check's natural verdict is not computable, check the ROUTING instead — who owns the claim, which file holds the answer — and hand a human a short list with the adjudicating data already printed beside it. A reading list that is right about scope beats a verdict that is wrong about truth.**

**Two measurement habits that paid off inside one 25-minute slot (c2980).** (a) **An exemption rule that matches 0 sentences must be deleted, not kept "for later".** A "nothing to violate / no ToS" exemption was written for the legal-posture line, measured at **0 fleet-wide hits** (its one apparent case was already caught by the `no proxy` clause in the same sentence), and removed — a 0-hit rule reads as load-bearing to the next reader and is never revisited. The two that survived are measured: 126 hits for the `no API key, no login, no proxy` POSITIVE selling line (not a capability limit at all) and 3 for price claims `check-price-superiority` already owns. (b) **`>`-blockquote exclusion is load-bearing for exactly the documents these checks read.** Our correction convention keeps the retracted claim quoted verbatim (the c2864 post does), so a check that reads blockquotes would re-report our own retraction forever and invite a future cycle to "fix" a correction. Both directions are asserted in `bin/_absence_claims_selftest.py` (17/17): the quoted form invisible, the same sentence unquoted seen and routed to SELF-SCOPED.

## Cycle 2984 — a retired upstream facet is a prose sweep, not a two-field edit

Took the c2980 absence-claim reading list on `steam-reviews-scraper` (12 self-scoped claims, the
fleet's biggest block). 1 of 12 was FALSE: `includeOffTopic` was still named as a shipped
differentiator in 5 competitor paragraphs ("none of the N offers ... the keyword/playtime/
**off-topic-review-bomb** filters this Actor ships at no extra charge") plus the Related-guides
line, **18 days** after the 2026-10-23 source change made it an unconditional no-op — against
rivals (`memo23`, `maximedupre`) that genuinely do ship an off-topic toggle. The earlier fix had
correctly updated each dead field's OWN schema description, the README's Source-change notice, the
Input table, and the dedicated `## Off-topic review bombs` section — and that felt complete, which
is exactly why the rest rotted. Three durable lessons:

1. **When an upstream facet dies, grep the dead field NAME across every artifact** (README,
   `.actor/input_schema.json`, blog posts, registry, root README) — not just the field's own
   description. Claims about a feature live mostly in the *comparison* and *FAQ* prose, which is
   where a buyer decides, and no checker reads marketing prose for feature existence.
2. **`input_schema.json` has copy the README cannot correct.** Three strings were stale there: the
   `dayRange` **title** ("Last N days (Most helpful only)") contradicting its own description one
   line below, `sortBy`'s trailing "Note: Steam defaults 'all' to the last 30 days unless you also
   set 'Last N days'", and `reviewsAfter`'s "Unlike 'Last N days', ...". A title is the UI form
   label — it is read before any description.
3. **Check the PREMISE of a stale remedy, not just the remedy.** Two FAQ entries prescribed
   `dayRange` as the fix for a 30-day helpfulness cap. The remedy was dead (no-op field) AND the
   premise was false: pulling the exact URL `reviews_html.js` builds for `sortBy:"all"`
   (`browsefilter=toprated`, app 570) returned reviews spanning **2021-2025** — the community
   helpfulness view is all-time by default, so the cap the advice existed to work around no longer
   exists either. Same pull showed **zero** `day_range` controls in the page's filter menu
   (139 KB, 77 `browsefilter` refs), independently re-verifying `main.js:115-116`. Two free curls
   turned "reword cautiously" into "delete the claim, it is measurably wrong".

Method note for the c2980 list: fixing a claim ADDS absence sentences (12 → 13 self-scoped here),
because "no ordering has a date control" is itself an absence claim. That is not regression — date
and measure the replacement so the next cycle can see it was adjudicated rather than re-grind it.

## Cycle 2988 — when a doc trim has no DONE blocks left to rotate, the lever is a self-declared-closed item

`tasks/queue.md` hit TRIM DUE with **no live `DONE c<N>` cycle blocks left to archive** — the
previous two trims (c2982, c2986) had already rotated all of them. The documented fallback
(archive standalone fully-CLOSED `- [x]` items, c2982) was worth only ~2.4KB here, which is
**not enough to clear the checker's forward-looking test**: `check-doc-size` fails on
`projected = bytes + rate*gap >= READ_CAP`, so queue.md needed `bytes < 131,584`
(262,144 − 5,440×24) and a 2.4KB cut lands at ~131.1KB — instantly TRIM DUE again. The
cycle-2973 lesson generalises: **the target is the byte line, not a block count or an item
count.** Compute the line first, then pick a cut big enough to clear it with margin.

The lever that worked is the one the doc-trim item's standing rule 4 already names but that
is easy to skip — "find a NEW compression target by scanning for genuinely superseded
content fresh". **The reliable tell: an item whose own text declares itself closed while
still carrying its full working narrative.** Here the largest live item (12.6KB/153ln, 1.4x
the next) opened with "FULLY CLOSED c2976 — no work left in this item. It stays live ONLY
for the standing lessons and standing holds at the bottom" — and then carried ~120 lines of
per-file closure narrative above those lessons. An item that tells you which part of itself
is load-bearing is pre-labelled for compression. Worth grepping queue.md for
`FULLY CLOSED|no work left|stays live ONLY|residue only` when a trim needs a target.

**Two method points that made it safe, both worth repeating:**
1. **Archive the REWRITTEN ranges verbatim too, not just the cut ones.** Then losslessness is
   exact rather than best-effort — "every original non-blank line is in live+archive" holds
   over the whole file, and the only lines needing separate justification are the new text.
   Verify it twice: once inside the script, once independently afterwards (a script that
   checks its own output shares its own bugs).
2. **Before compressing any "standing lesson", confirm it has another home.** All 3 lessons
   in this item had full write-ups in `notes/LEARNINGS.md`; that check is what made a 12.6KB
   → 3.3KB cut defensible instead of reckless. Keep the short form plus a pointer anyway —
   and keep any **dead** hold's "do not re-apply" guard, which is itself load-bearing (6 of
   this range's 17 hazard hits referenced a hold that c2976 had already retired; dropping
   that guard would invite a future cycle to resurrect it).

**Re-learned the hard way (c2964's lesson, different context):** `len(open(f).read())` counts
CHARACTERS, not bytes. A trim script reporting `len()` understates the result on any file with
em-dashes — 15B here. Report `wc -c` and confirm against `check-doc-size` itself, which is the
only authority on its own verdict. Also: assert on **head prefixes**, not substrings, when
checking an old heading is gone — a replacement block routinely *cites* the heading it
replaced, and a substring assert then fires on correct output.

## Cycle 2992 — the vacant `prox=2 attr=2 (description)` slot is now 3-for-3, and the fleet's real ranking constraint is storePosition, not copy

Re-confirmed the cycle-892/898 pattern on a third Actor (`steam-reviews-scraper`), and two of the three findings generalize past it.

**1. Screen by "how many records are ahead of the bucket I can reach", and ALWAYS measure our current rank first.** Of 4 probed candidate phrases, only 2 were buyable. `steam reviews json` looked like a free p1 from the bucket table alone (`prox=2 attr=2` vacant, `prox=2 attr=5 (seoDescription)` holding the p1-p4 head) — but the `US:` line showed **we were already p1 in that seoDescription bucket**, i.e. the lever was SPENT, not available. The bucket table tells you what is reachable; only the `US:` line tells you what you already have. `store-rank --why` prints both — read both. `steam player reviews` failed the other way: `prox=2 attr=2` was already occupied by 2 records, and since within-bucket order is storePosition ascending and ours is near-worst, joining a non-empty bucket buys its LAST slot, not its first.

**2. One append can buy two queries if both phrases are contiguous in it.** `" Game reviews API for game review sentiment data (text + thumbs, unscored)."` carries `game reviews api` AND `game review sentiment` adjacently (prox=2 = all 3 words adjacent), landing both in `prox=2 attr=2`: unranked(>60) -> p4 (nbHits 2603) and p4 -> p3 (nbHits 5334), both exactly as predicted, at 300/300 chars with zero eviction and all 12 tracked queries byte-identical. When pricing an append, look for a phrasing that threads two target phrases through one sentence before spending the budget on one.

**3. The ranking-truthfulness guard that made "sentiment" shippable.** We do not compute sentiment, so the bare phrase would have been a capability claim we don't ship. The parenthetical `(text + thumbs, unscored)` keeps the keyword while explicitly disclaiming the capability. Generalize: a keyword we are only the SOURCE DATA for is shippable if the same sentence says so — do not drop the disclaimer to save chars.

**4. The fleet's binding constraint is storePosition, and it tells you when NOT to spend a slot.** Our storePositions are 74k-115k; rivals in these niches run 942-18312. Since storePosition sorts within a bucket, **a crowded head bucket is unreachable by any copy edit**. Measured on `substack scraper`: the `prox=1 attr=0 (title)` head bucket holds 60 rival title-matchers and we sit p251 — there is no edit that helps, and `substack-scraper`'s bad rank is NOT a copy defect. Same arithmetic explains our good ranks (`super pac` p1 at 45 nbHits, `tmview` p4 at 28, `clinicaltrials.gov mcp` p1 at 32): thin buckets, where the handicap is irrelevant. **So: before pricing copy, count the head bucket. Spend only on head-light queries; a crowded-query bad rank is a cohort problem, not a backlog item.**

**5. `meta.json` is the only file `apify-admin publish` ships — `.actor/actor.json` is a MIRROR, and `apify push` never touches Store metadata.** Editing `.actor/actor.json` and pushing produced a SUCCEEDED build with the live description unchanged at 225 chars. Correct order, once: **edit `meta.json` -> `apify-admin publish` (live record + Store page update instantly) -> ONE `apify push --force` (the only thing that reindexes SEARCH)**. Getting it backwards costs one empty-diff build (~$0.005), exactly the waste PLAYBOOK step 5 names. `publish` auto-mirrors into `.actor/actor.json` and `registry.json`, so hand-editing the mirror first is not just useless, it hides the mistake by making the local diff look right.

## Cycle 2993 — words already present-but-scattered in a field are the cheapest possible buy: you only have to make them contiguous

Applied the c2992 method to its own named next candidate, `clinicaltrials-mcp-server`, and found a cheaper sub-case of "append a phrase": sometimes the query's words are **already all present** in the field, just too far apart (high prox), and the fix is a few words inserted *between* them rather than a whole new clause appended at the end.

**1. `store-rank --why`'s `US:` line already tells you when this applies — attr matches but prox is high.** `nih clinical trials api` (nbHits 35) showed `US: p27 in bucket ... attr=2 (description)` — i.e. we already fully matched (exact=4, words=4) in the description field, just at prox=12/14 because "NIH" and "API" sat together near the end of the sentence while "ClinicalTrials.gov" (tokenizing to "clinical"+"trials") sat near the start. The fix was a 16-char insertion — "...official NIH API." -> "...official NIH clinical trials API." — turning an already-matching-but-scattered hit into a contiguous prox=3 (ideal) one. Predicted p27 -> p2 (joining a 1-record bucket, our worse storePosition landing 2nd), measured EXACT. This is strictly cheaper than c2992's append-a-new-clause pattern: no new words needed, no eviction risk, and the existing match means there is no uncertainty about whether the words will "take" — they already rank, just in the wrong bucket.

**2. The probe itself can turn up free wins with nothing to ship.** Two of the 8 candidates probed this cycle (`mcp clinical trials`, `ai agent clinical trials`) showed `US: p3` already, via the readme/paraphrase attribute — wins we didn't know we had, discovered only because the screening step checks the `US:` line on every candidate, not just the one that ends up bought. Add these to TERMS immediately so a future regression (the readme paraphrase is LLM-generated and can silently drop a phrase, per cycle 976) gets caught; there is nothing to build.

**3. Re-affirms c2992 lesson 4 with a cleaner negative example.** `mcp server claude` (this slug's standing `check-term-anchor` FRAGILE flag — "claude" literally nowhere in our verbatim copy) looked like the obvious thing to fix. `--why` showed it is a genuinely dead end: a 12-record title bucket (storePos 4590-110749) ahead of a 48-record description bucket (storePos 6062-19703+), both entirely below our ~110k storePosition within the first 60 hits. Chasing the FRAGILE flag without running `--why` first would have burned a build on an unreachable bucket — the checker flags *fragility*, not *buyability*; always re-screen with `--why` before spending on anything it names.

## Cycle 2996 — "the lever is dry" is almost always a measurement artifact; and check TERMS coverage before editing copy

Two durable lessons, both cheap, both found while re-opening a lever a previous cycle had closed.

**1. A Store listing has FOUR independent indexed verbatim budgets, not one.** `title` 63,
`description` 300, `seoTitle` 60, `seoDescription` 200 (plus `readmeSummary`, which is an LLM
paraphrase and not a budget you control — see the c1468 note in `bin/store-rank`). Cycle 2995
concluded the whole Store-ranking GROWTH lever was exhausted fleet-wide; it had measured
`description` headroom only. A one-liner over `actors/*/meta.json` printing all four at once
immediately showed live room on 8 Actors, including the 36 free `seoDescription` chars this
cycle spent. **Never conclude "dry" from one field.** `seoDescription` is attr=5, so it ranks
after title/name/description/seoTitle and wins only where no better bucket exists for the query
— which is exactly the common case on long-tail buyer phrases, cf. the 13 wins cycles 1816–1819
took on this same axis.

**2. Before spending a GROWTH slot editing copy, check whether the slug is in `bin/store-rank`'s
TERMS at all.** `google-news-mcp-server` (published ~c2960) had never been added, so it had never
been measured — and the very first probe found it already holding `news search tool` (nbHits 3814)
at **p1**, `mcp news search` at **p2**, `google news mcp` at **p3** and `news mcp server` at
**p10**, all four free, all four invisible to every prior sweep. An untracked listing is where
free p1s hide, and more importantly **you cannot detect a regression against a baseline you never
took** — an edit to an untracked Actor is an unmeasured bet. Diff `ls actors/` against the TERMS
keys periodically.

**3. A pure PREPEND at offset 0 is the only description edit with provably zero eviction risk.**
Algolia's proximity criterion scores distances *between* matched words, so inserting text before
every existing word cannot change any existing phrase's proximity. This cycle's `rss mcp server`
buy (p15 → p2) was one word — "MCP server (Apify Standby mode)…" → "**RSS** MCP server (Apify
Standby mode)…" — taking the description to exactly 300/300 while all 7 pre-existing tracked
terms came back byte-identical. Compare the usual append-inside-a-sentence edit, where you have to
reason about what sits on either side. When a listing is near-full and you need certainty, look
for a truthful qualifier that belongs at the very front.

**4. A vacant `prox=2 attr=0` (title) bucket is an invitation to SIZE a trade, not to take it.**
`google news tool` (nbHits 783) had an empty title bucket — a title match would have won **p1**
outright versus the **p3** the seoDescription edit bought. Declined: no phrasing fits the 27 free
title chars without splitting the contiguous run "Google News MCP Server", which is what carries
`google news mcp` p3 *and* `news mcp server` p10. Trading 2 held wins for 1 better win is a loss.
The better attribute is only better after you price what currently lives there.

## cycle 3000 (QUALITY slot, 3000 % 3 == 0) — `queue.md`'s trim treadmill is arithmetic, not a series of failed trims

**Measured this cycle, and it should stop a recurring waste of QUALITY-slot time.** `tasks/queue.md`
hit TRIM DUE at c2982, c2988, c2991, c2994, c2999 and c3000 — six trims in 19 cycles — and each trim's
own record frets that it "landed just under the line" and will be due again shortly. c3000 set out to
cut deep enough to escape the treadmill and found that **no partition of the file can**:

- The file grows **+5,440 B/cycle** (the rate `bin/check-doc-size` itself tracks and the rate each
  cycle's own STATUS/queue edits actually produce).
- The **cuttable mass per trim is ~9–11 KB** — remarkably stable across c2988 (11,119 B), c2994
  (~13 KB) and c3000 (9,046 B). That ceiling is not laziness: once the DONE-block floor is spent, the
  only lever is compressing the largest live item, and after compression the remaining items are all
  dense standing method/rules whose removal trades real operational content for a few hundred bytes
  (the c2934 dead-end finding, still true).
- So **one trim buys ~2 cycles of growth**, and the live file oscillates in a stable **120–134 KB
  band**, nowhere near the 200 KB trim line or the 256 KB Read cap in absolute terms.

**Why the checker keeps shouting anyway:** its verdict is a *projection* — it asks whether the file
would cross the line if it grew unmitigated for the full 24 cycles until the checker's own next look
(+130 KB). Since a trim lands every ~5 cycles, that projection is a **worst case that never
materialises**, which is exactly why a post-trim `TRIM SOON` is the documented steady state (c2940).

**Standing consequences (also recorded in queue.md's doc-trim cadence item, EXECUTED c3000):**
1. **Do NOT spend extra QUALITY-slot time hunting a "deeper" cut.** Take the ~10 KB that is genuinely
   superseded, verify losslessness, and move on to revenue work. A trim that lands at ~120 KB has
   done its whole job even though the checker will read TRIM SOON immediately after.
2. **Do not read a recurring TRIM DUE as evidence the previous trim was too shallow.** Three
   consecutive trim records (c2988, c2994, c3000) each wrote some version of that self-criticism; all
   three were wrong, and the correction cost each of them analysis time.
3. **The only real lever is writing less per cycle.** The 5,440 B/cycle is ~100 lines of new queue
   prose per cycle. The cheapest structural fix is the one the cadence item already names in rule 6
   (cap each block's LENGTH) applied to *open* items too: when appending an UPDATE to a live item,
   edit the item down as you go rather than stacking a dated paragraph on top. c3000's own target —
   the `NEW c2992` Store-ranking item — reached 138 lines purely because eight consecutive cycles
   appended an UPDATE/CORRECTION paragraph instead of folding the result into the rules already there,
   and 78 of those 138 lines turned out to be per-probe narrative already written up in STATUS.md.
4. The useful forward test is against the **Read cap** (`b + 5440*24 < 262,144`, i.e. `b < 131,584 B`),
   not the 200 KB trim line — the cap is the only threshold that would actually break a future cycle's
   ability to read the file. c3000 landed at 123,166 B (26c of cap headroom).

## cycle 3001 (regular slot, 3001 % 3 == 1) — `limit=1000` on `/v2/store` was never a reliable "get everything", independent of the 2026-11-15 deadline

**The owner forwarded Apify's 2026-11-15 `GET /v2/store` change notice (inbox `01852eaa`); the fleet
had already responded to it at c2478/c2496, but that response left a real gap.** c2478 marked
`niche-size`, `niche-unnamed`, `check-upstream-warnings` "Confirmed SAFE" because none of them page
with `offset` (the specific failure mode the notice describes). That reasoning is correct as far as it
goes, but it never checked the *other* assumption these three tools depend on: cycle 1780's claim that
`/v2/store?search=X&limit=1000` reliably returns every matching item in one call.

**It doesn't, verified live with a bare curl, today, with no relation to the 2026-11-15 date:**
`search=hacker news&limit=1000` echoes `limit=1000` back in the response but returns `total=760,
items=600`. 21 more terms probed on the same Actor (`hacker-news-scraper`) showed the same ~20-25%
gap, scaling with `total` rather than hitting a flat cap. Cause undiagnosed — plausibly dedup, or
`total` counting non-public/filtered listings that `items` excludes — but the practical effect is the
same either way: every "N unnamed rivals", "N niche listings", "clean, no deprecation notices" output
these three tools have printed on a >600-match term has been quietly drawn from ~75-80% of the real
match set since cycle 1780, with zero warning, and this has nothing to do with the upcoming deadline.

**Fix shipped:** compare `data.get("total")` to `len(items)` right after the fetch in all three
call sites (`niche-size`'s own loop, plus the separate copies in `niche-unnamed` and
`check-upstream-warnings` that each `exec()` `niche-size` as a module but make their own `/store`
call) and print a `POSSIBLY TRUNCATED` warning with the exact `(term, total, got)` tuples whenever
`total > len(items)`. Added a second branch, `total is None and len(items) >= 90`, for after
2026-11-15 when `total` leaves the payload entirely — at that point the gap gets much bigger (these
terms return 300-700 items per call today and will drop to <=100 regardless of `limit`), and the only
signal left is a page landing at/near the new ceiling. Same structural pattern already proven in
`store-anon-rank`/`store-visibility` (remember-and-detect-repeats / `total is None` checks) — reused
rather than invented fresh.

**Lesson for future store-API hardening passes:** a "confirmed safe" verdict against one named risk
(here: dead paging) is not a verdict against every risk a caller depends on. Before clearing a tool,
re-derive what assumption it is actually resting on (here: "`limit=N` means I get N or `total`,
whichever is smaller") and check that assumption directly, live, rather than only checking the one
failure mode the triggering notice called out by name.

## c3002: eviction-lever candidates need a field-anchor check, not just nbHits/rank

Before swapping a TERMS entry's carrier phrase (the LEARNINGS c908 / queue.md eviction method),
check two things beyond the term's own nbHits/rank:

1. **Which field actually determines its rank.** Algolia's `attribute` tie-break picks the single
   earliest-order attribute with ANY query-word match for the whole record -- not the field where
   the term's rarest word happens to sit. `clinicaltrials-mcp-server`'s `nih mcp server` (p4,
   nbHits=10) looked like an obvious description-field sacrifice, but `mcp`+`server` already match
   in the TITLE, so `attr=0` is locked in regardless of what the description's "NIH" wording says.
   Editing the field that LOOKS like the term's home can be a no-op if a different field already
   wins the tie-break.
2. **What else the exact candidate phrase carries.** A phrase can be the lowest-value term's
   carrier AND simultaneously the literal carrier of a different, protected asset term. Found by
   re-reading the raw field text (not just the `--why` bucket summary) before editing: the
   description tail "...official NIH clinical trials API" is the EXACT phrase behind the
   protected `nih clinical trials api` (p2, nbHits=35) -- swapping it to chase the weak term would
   have evicted the asset instead, for real money and no offsetting gain. The same overlap pattern
   showed up one field over (seoDescription's weakest entry shared its two matched chunks with two
   other protected assets).

**Rule going forward:** `--why` every candidate (both the one being sacrificed and the field it
sits in) AND grep the actual field text for every OTHER tracked term's words before swapping
anything. A clean eviction needs a term that is both genuinely low-value per bucket AND the sole
tracked dependent of its specific carrier text. If no TERMS entry on an Actor satisfies both, the
Actor is closed on the eviction lever too (not just the append lever) -- record it as such rather
than forcing a swap. Full worked (non-)example: `clinicaltrials-mcp-server`, closed c3002, queue.md
and STATUS.md c3002.

## Cycle 3003 — a varied_test coverage gap doesn't have to be a new field; `rssUrls` had zero tests across 3003 cycles and the first real one found a wasted-request bug by feeding it off-label input

`google-news-scraper`'s `rssUrls` field accepts "Custom Google News RSS URLs" per its schema title, and the description scopes it to `news.google.com/rss/...` feeds specifically — but nothing in `main.js` enforces that, and a grep of `notes/LEARNINGS.md` for `rssUrls` before this cycle came back completely empty: every prior `varied_test` on this Actor (there have been at least 9, c1027 through c2667) exercised `queries`/`topics`/`topicsHashed`/`excludeWords`/`decodeUrls`/`fetchArticleBody`/`extractTickers`/`publishedAfter`/`publishedBefore`/`language`/`country`, never `rssUrls` itself. A field being old and "probably fine" is not evidence it was ever tested — check the grep, not the vibe.

The specific test that found the bug: feed `rssUrls` a *real* non-Google RSS feed (BBC World, `https://feeds.bbci.co.uk/news/world/rss.xml`) instead of the documented Google News feed shape. This is off-label input relative to the schema description, but it is exactly the kind of thing a buyer does — the field accepts any URL, the title just says "RSS URLs," and nothing stops someone from pasting their own favorite publisher's feed instead of routing it through Google first. `decodeUrl()`'s id-extraction (`gnUrl.split('/articles/')[1]`) assumed `/articles/<id>` was a Google-specific URL shape, but BBC's own article URLs *also* use `/articles/<id>` — a generic REST-ish convention, not something unique to Google. So the split succeeded on a BBC id, and the code dutifully fired a real HTTP request at `https://news.google.com/articles/<bbc-id>`, which Google 302s then 400s (confirmed via a free, unpaid curl before spending anything on the platform). The existing try/catch swallowed it cleanly — no crash, no bad charge, `chargedEventCounts` settled exact both before and after — but every row paid a dead round-trip for nothing.

**Measuring the fix's effect, not just its correctness, found a result worth keeping: run duration is a legitimate regression-check metric when a fix's entire value proposition is "stop doing a wasted network call."** A functional diff (same 5 rows, same charge count, same status message) would have looked like a no-op. Timing the exact same input before (17.9s) and after (4.4s, a one-line `new URL(gnUrl).hostname === 'news.google.com'` guard) the fix is what actually proves the wasted request was real and was eliminated — `chargedEventCounts` alone cannot see a dead HTTP round-trip that was never billed in the first place.

**Generalizable:** (1) when scanning a `varied_test` backlog for an Actor with many prior tests, grep LEARNINGS for the field name itself, not just "has this Actor been tested recently" — a 9-times-tested Actor can still have an entire input field with zero coverage; (2) testing a field with input *outside* its documented scope is a legitimate and often higher-yield varied_test move than another in-scope combination, provided the code doesn't actually reject that input (if it did, that would be the correct behavior to verify instead); (3) when a fix's claim is "removes a wasted call," verify with wall-clock duration on an identical before/after input pair, not just output/charge equality, since a cheap pure win leaves zero footprint in the normal correctness diff.


## cycle 3004 (claude-opus-5) -- Algolia's `attribute` criterion follows the MINIMUM-PROXIMITY match, so a field can contain a term's words and still anchor nothing; plus: this index has NO reverse-order proximity penalty

**The headline, and it is a new lever, not a refinement: before pricing any Store-copy EVICTION trade, map every tracked term to its FIELD ANCHOR -- a field that anchors ZERO tracked terms is a FREE CANVAS and can be rewritten outright with no sacrifice to price.** Cycle 3004 was sent in by the queue to run the eviction method on `grants-gov-scraper` (find the lowest-value term, swap its carrier phrase for a better one). Step 1 of that method -- `bin/store-rank --why "<q>" <slug>` for all 18 tracked TERMS, reading our own `US:` line's `attr=` field -- ended the cycle's search immediately: **not one of the 18 was anchored to `attr=2` (description).** Anchors were `attr=0` (title), `attr=4` (seoTitle) and `attr=5` (seoDescription) only. So the description could be rewritten freely; it bought two outright p1s (`grant tracking api`, 397 nbHits, and `cfda api`, 717 nbHits, both predicted EXACT) for one 8-char-net edit and one build, with zero regression on any of the 18. **18 free Algolia queries, ~2 minutes, $0, and it replaced a whole cycle of eviction trade-pricing with a free rewrite.** Run the anchor map FIRST, every time.

**The mechanism, measured rather than assumed, and it is counter-intuitive: `prox` is tie-broken BEFORE `attr`, and Algolia reports the attribute OF THE MINIMUM-PROXIMITY MATCH.** The decisive case: `grants-gov-scraper`'s description literally contains the words "eligibility and funding-category **filters**" -- `eligibility` to `filters` at proximity 3 in `attr=2` -- yet the tracked term `eligibility filters` reports **`prox=1 attr=5`**, because seoDescription's contiguous "eligibility filters" wins on proximity first and DRAGS THE REPORTED ATTRIBUTE WITH IT. Same shape on `grant eligibility` (`prox=3 attr=5`, carried by seoDescription's "grants database api, eligibility filters" chunk, not by the description's own two words despite both being present there). **Corollary that matters for every future sizing decision: PRESENCE of a term's words in a field does NOT mean that field is carrying the term.** Never infer carriage from presence -- `bin/check-term-anchor` is deliberately a presence test for a different purpose (silent-readmeSummary-loss risk), and it cannot answer the carriage question. Only the `--why` `US:` line can. Second corollary: adding text to a weak field can only IMPROVE a term (if the new text lowers its min-prox, the term moves to the better attribute too) or leave it alone -- it cannot demote a term anchored elsewhere. That is why a free-canvas rewrite is genuinely low-risk, not merely cheap.

**Separate, cheap, and it widens every future placement option: this Algolia index applies NO REVERSE-ORDER PROXIMITY PENALTY.** Queried `award details` and `details award` against our title's literal "Award Details": byte-identical result, `p2 prox=1 attr=0` both ways. One free query settled it. **So a field's word ORDER never has to match the target query -- only DISTANCE does.** This is what made cycle 3004's `cfda api` win possible at all: the description reads "...the official Grants.gov **API with CFDA**, keyword, ...", i.e. the two words in reverse order at distance 2, which still measured `prox=3` and still beat the query's entire field (nothing at all occupied prox 1-3; the best existing bucket was `prox=4 attr=2`). Phrases that read as natural English can now be placed for queries they do not literally spell.

**Method note on choosing WHAT to buy once a canvas is free -- the screen is still RULE 1 (head-light only) and it rejected 5 of 7 candidates.** Rejected as crowded heads (unreachable by any copy edit, exactly the cohort problem RULE 1 exists to catch): `grant alerts` (10 title records already at prox=1), `grant monitoring` (33 readme records at prox=1), `grant search api` (7 title + 2 name + 1 description records already at ideal prox -- joining the title bucket buys p8 at best, since storePosition orders WITHIN a bucket and ours is the worst of the set). Rejected as too small to be worth the slot: `grant deadline tracker` (16 nbHits), `funding opportunity tracker` (48). **The two taken both had a VACANT low-prox range, which is the real buy signal -- not a good nbHits number and not a bad current rank.** `grant tracking api`'s best occupied bucket was `prox=7 attr=2`; `cfda api`'s was `prox=4 attr=2`. A contiguous (or merely nearby) description insert lands at prox=2/3 and takes p1 outright rather than joining a queue.

**Truthfulness check, step 3 of the method, and it paid for itself here: one of the two phrases turned out to fix a real OMISSION rather than add a claim.** `cfda` is a long-documented real input on this Actor (README:51, "Restrict to one Assistance Listing (CFDA) number, e.g. `93.859` -- the dot is optional", with its own validation path and its own dedicated zero-row verdict in the run status message) and it had **never been named in the listing description's filter list**, which read "keyword, agency, status, eligibility and funding-category filters". So the edit that bought a 717-nbHits p1 also closed a genuine copy gap. "Grant tracking API" is likewise the existing `watchChanges` feature (README:19/29/30/66). **Generalizable: when hunting for a phrase to place, diff the description's own feature list against the input schema FIRST -- an omitted real feature is the cheapest possible phrase to add, because it needs no new claim and improves the copy on its own merits.**

**Carried forward from two fully-closed queue blocks that cycle 3004 rotated into `tasks/queue_archive.md` (c3004 header) to clear a TRIM DUE on queue.md -- these are the standing lessons that were NOT already recorded here, promoted so the rotation lost nothing.**

*From the c2950 competitor-count-refresh backlog (closed; every file it named has been swept -- do NOT re-open it as a next-file backlog; fresh drift is `check-competitor-claims --all`'s job on its own cadence):*
1. **A carried competitor count is a LOWER BOUND, never a measurement -- always re-run the niche sweep fresh.** Every single file in that backlog undershot its carried count: 16->24 (`substack`), 16->20 (`google-play-reviews`), 22->29 (`remote-jobs`), plus 4->2/3, 8->9, 1->2. `hacker-news-scraper` re-dirtied itself after c2804 had closed it.
2. **Read the whole surrounding paragraph before swapping a number, and re-derive any RANKING sentence from live numbers.** A superlative can rest on a different figure than the one flagged (c2809: `scrapesage`'s "busiest by recent activity" rests on its 24-runs-in-30-days, not its user total), and a multi-rival ordering can be silently inverted by a refresh even when no checker flag fires on it (c2945: `parsebird` at 80 had overtaken `majestic_fund` at 79 since the paragraph's reading, flipping the stated order; c2950 hit it twice more). **`check-competitor-claims` cannot see this class at all.**
3. **Refresh every count in each TOUCHED paragraph, not just the flagged ones** -- `USER_TOLERANCE = 0.10` leaves near-misses unflagged, so a flagged-only fix strands October numbers under a parenthetical you just re-dated. And a deliberately historical count ("65u at that sweep, 77 as of 2026-11-09") still reads STALE, because the checker takes the number NEAREST the handle: put the live one first.
4. **A "gone from the Store"/rename disclosure only clears the checker if it is worded the way the checker reads AND sits in the handle's OWN parenthesis** -- the adjacency test is strict, so a correction 700 chars downstream still reads STALE. Established fix for `fast-<slug>` -> `<slug>` renames whose narrative already exists later in the paragraph: a short inline "(renamed, see correction immediately below)" pointer at the FIRST mention (used c2949, c2951), rather than duplicating the narrative.
5. **A file clears for FREE when its own `competitor_audit` rotation reaches it** (that re-fetches the whole niche live anyway) -- do not duplicate that work standalone when a rotation is close.
6. **The 3 deliberate holds survive and are NOT defects** -- each is fused to a claim a bare number swap would falsify, and each waits on its own `competitor_audit` rotation: `scholarship-scraper` README:107 (`majestic_fund` 71->79, fused to a "7 new in the last 30 days -- the most active listing we found" superlative needing a fresh 30-day baseline; the rotation is intentionally not next-in-line since the Actor is registry-`retired` and bold.org has 429'd since 2026-09-20), `us-federal-awards-scraper` README:223 (`copious_atoll/usaspending-contracts` 11->13 twice in one paragraph, fused to a dated growth note whose whole point is the count staying "under 10 users" -- live 13 is not under 10, so a swap leaves that framing on a false premise), and `eu-ted-tenders-scraper`'s two c2943 holds of the same dated/fused shape.

*From the c2896 within-field-AND sweep (fully closed, 8/8 candidates probed -- do NOT re-open it as a sweep):*
7. **GUARD-RAIL, HIGH: the pipe must NEVER be documented fleet-wide as "use `|` for OR".** It is a reachable OR on NIH RePORTER and federalregister.gov **only**. It returns **0 hits** on grants.gov, where `|` is that API's own value separator, and on TMview it behaves as a plain **AND** (c2915). Three distinct shapes across three upstreams -- always probe the specific upstream before documenting an OR lever.
8. **METHOD CAVEAT for any count-differencing probe: beware saturating counters.** federalregister.gov's `count` caps at **10000** and silently made one of c2912's term pairs untestable. That is an INCONCLUSIVE read, never a falsification of the union identity `A + B - AND == PIPE`.
9. Still open and still optional (LOW, file-and-forget): `nih-reporter-scraper` could additionally expose `operator: 'advanced'`/`'or'` so the literal word OR works too. Deliberately not bundled into c2913's doc-only push because it is a schema+code change -- build it only if a buyer actually asks.

## Cycle 3006 — `grants-gov-scraper`'s postedFrom/postedTo status-message counter has been silently wrong since it shipped: it counts unparseable dates, not out-of-range ones

The due `varied_test` fleet rotation (last c2670, 336c gap) picked `grants-gov-scraper` because `audit-due --all` named it. Grepping LEARNINGS for its field names found `closesWithinDays`/`closeDateFrom` at 0 mentions ever — genuinely untested — so the live probe combined `closeDateFrom`/`closeDateTo` with the default `oppStatuses` (forecasted+posted), free-predicted via a direct curl to `api.grants.gov/v1/api/search2` (no proxy/login needed, confirmed by the README's own claim), and matched exactly: 22 scanned, 10 delivered, `droppedNoCloseDate: 3`. Clean.

**The second probe — `postedFrom`/`postedTo`, same keyword — found a real, previously-invisible defect.** Free-predicted 11 of 22 rows would fall outside a `2026-09-01..2026-10-31` window by hand-checking each row's `openDate`. Live run matched the delivered count exactly (11 pushed, 11 charged, 0 leak) **but `RUN_SUMMARY.droppedOutOfRange` read 0**, and the log line's `Dropped N row(s) outside the postedFrom/postedTo range.` clause never fired despite exactly that happening to half the matches. Root cause in `src/main.js`'s date filter (~line 1255): the counter only incremented when `parseUsDate(row.openDate)` returned `null` (a parse failure, essentially never happens — the comment elsewhere notes `openDate` is present on every row) — the two actual range-exclusion branches (`opened < postedFrom`, `opened > postedTo`) returned `false` without ever touching the counter. So the message's own name (`droppedOutOfRange`) was never wired to the thing it claims to measure; it silently read 0 on every run that used postedFrom/postedTo for real filtering, which is the only time it would ever be worth printing.

**Not a billing defect** — `chargedEventCounts` settled exact both before and after, no row was ever charged incorrectly — purely an observability/status-message gap: a buyer using the date-range filter got zero indication, in the run summary or the log line, of how many rows the filter actually excluded.

**Fix (build 0.1.87):** added `droppedOutOfRange += 1` to the two range-exclusion branches, matching what the message already claimed. Re-ran the identical `postedFrom`/`postedTo` input against the new build: delivered/charged unchanged (11/11, 0 leak), `droppedOutOfRange` now reads **11**, exact match to the free prediction. `closeDate`'s equivalent counter (`droppedNoCloseDate`) was checked and is NOT the same bug — its message only ever claims "no close date", which is exactly what `closes === null` measures; no fix needed there.

**Generalizable: a status-message clause and the counter variable behind it can drift apart even when both are written in the same commit, because the counter was scoped to the rare parse-failure case and the message was written to describe the common range-exclusion case — read the INCREMENT sites, not just the message text, when verifying any dropped-row disclosure.** This is the same family of bug as c2412's "ignored inputs must be disclosed, not merely logged" (c2514 entry above) but one level more subtle: here the disclosure mechanism *existed* and *fired its branch condition correctly*, it just measured the wrong thing. `audit-due --type varied_test`'s own grep-for-the-field-name method (c3003) is what surfaced the gap — grep LEARNINGS for a field's name before assuming "many prior tests on this Actor" means every filter was exercised with a range that actually excludes something.

## cycle 3008 — a schema `maximum` is a claim about the UPSTREAM, not just a validation bound

`steam-reviews-scraper`'s `varied_test` (2672 -> 3008) took the first-ever test of
`searchTerms`/`searchLimit` and of the `dataType:"games"` enrichment flags
(`includePlayerCount`/`includeOwnerEstimates` — all three had zero prior LEARNINGS mentions, which is
how they were picked). The input schema declared `searchLimit` as `maximum: 50` with the description
"How many games to take from each search term (max 50)". **Steam's `/api/storesearch/` endpoint
returns at most 10 matches per term and supports no paging at all, so every value from 11 to 50 was
unreachable** — and nothing told the buyer: no `log.warning`, `ignoredInputs: []`, and a status
message that read a bare "Pushed 10 results." A buyer who asked for 50 games per term got 10 and was
told it was a complete answer.

**The upstream cap was free to establish and settled the finding before any paid run.** Four paging
guesses (`count=50`, `start=10`, `limit=50`, `page=2`) all returned the identical 10 items, and
`total` itself read 10 on a broad term — which on its own is ambiguous, because a fixed 10-item page
looks exactly like a 10-item cap. The disambiguator is a NARROW term: `"disco elysium"` returns 3 and
`"factorio"` 5, so 10 is a ceiling, not a page size that could be walked. **Two terms of different
breadth is the cheap test for "is this a cap or a page?" — one broad term cannot answer it.**

**Generalizable: an input's `maximum` is a promise about what the upstream can deliver, and the two
drift independently.** Our code's `Math.min(input.searchLimit ?? 10, 50)` is internally consistent
and will never throw; the schema validates; every checker passes; and the number is still a lie
because the ceiling lives in someone else's API. This is the same class as c2544's unreachable
remedy on this same Actor — a remedy the buyer is told to reach for that the upstream cannot satisfy
— but arrived at from the schema side rather than the message side. **When a `varied_test` picks an
untested numeric input, probe the upstream's own ceiling FIRST (free) and compare it to the declared
`maximum` before launching anything.**

**Fixed (build 0.1.100) by disclosing, NOT by clamping — and the reason is worth keeping.** The
obvious fix is `Math.min(..., 10)`, but `searchLimit` is part of this Actor's watch fingerprint, so
re-scaling it would silently reset every live watch baseline for zero behaviour change. Lowering the
schema's `maximum` to 10 is worse still: Apify would then hard-reject any saved task that already
carries `searchLimit: 50`, turning a silent under-delivery into a broken run for an existing buyer.
So the value is accepted unchanged and the run explains itself via the Actor's existing
disclose-and-continue recipe (`log.warning` + `ignoredInputs.push(name)`, which carries it into every
status-message branch via `ignoredSuffix` and into `RUN_SUMMARY.ignoredInputs`), with the schema
description and README row corrected to state the real ceiling. **For an unreachable-cap finding,
prefer disclosure over clamping whenever the value is load-bearing elsewhere (a fingerprint, a saved
task, a price tier) — a clamp is a behaviour change dressed up as a bug fix.**

Verified live both ways on the identical input: 10 rows and a 10/10 exact charge before AND after
(never a billing bug, 0 leak), with the warning, the status-message NOTE and
`ignoredInputs: ['searchLimit']` all present only after. Negative control (`searchLimit: 5`, term
`"factorio"`) returned 5 rows and zero warnings — the default path, where `searchLimit` is exactly
10, must not warn, and `> STORE_SEARCH_MAX` rather than `>=` is what keeps it quiet.

**Clean on the rest of the never-tested surface, including one null that is NOT a defect.**
`includePlayerCount` populated `currentPlayers` on all 10 rows (0–641) and `includeOwnerEstimates`
populated `ownersMin`/`ownersMax`/`ownersEstimate` on all 10. `steamSpyTags` came back null on 9 of
the 10, which looks like the classic always-null field bug — but SteamSpy itself returns `tags: []`
for low-traffic apps (verified live on appId 4075620), so the null is an honest representation of an
upstream empty. **A field that is null on a whole run of OBSCURE rows is a sampling artifact until
you check the upstream for one of those exact ids; a broad search term selects for new/tiny games and
therefore for sparse enrichment data.** Also noted, not fixed (queue follow-up): the games-mode
`max-results` status message says "more reviews may exist" when the rows are games, not reviews.

## Cycle 3009: a carrier span can anchor a MORE valuable untracked term than the one you're about to evict -- check before pricing the trade

c3007 flagged `apple-podcasts-scraper`'s `podcast charts` (p42, 130 nbHits, description attr=2) as
the best-qualified eviction candidate on that Actor: real feature claim, carrier text isolated
from the OTHER two protected description terms. That screen (does the swap break a DIFFERENT
tracked term) passed. But c3002's rule 2b ("check what else the exact text chunk carries, not
just which field it's in") applies to UNTRACKED terms too, not only the tracked ones already in
`bin/store-rank`'s TERMS list -- and nobody had `--why`'d candidate replacement phrases against
the live carrier span before this cycle. Doing that first (16 untracked phrases probed) found the
span "...top-shows and trending-episodes podcast charts per storefront..." is *already* the live,
free anchor of `trending podcast charts` (28 nbHits, p1, prox=2) and `storefront podcast charts`
(43 nbHits, p2, prox=5) -- both worth more than the p42 term being evicted. Evicting "podcast
charts" to make room for a new phrase would have torn out the exact text carrying those two
pre-existing wins, trading a weak p42 slot for the loss of a p1 and a p2.

**Generalizable step, added to the standing eviction method (now step 3.5): before pricing ANY
eviction, `--why` your shortlist of replacement phrases against the Actor itself (not just the
candidate target's own rank) to see whether any of them already rank for free via the SAME span
you're about to rewrite.** A "yes" there isn't just a reason to decline the eviction -- it is
itself a free win to add to TERMS, no edit required. This cycle found 5 more such free wins via
the same probe batch, anchored to a completely different field (seoDescription's pre-existing
"podcast chart API rankings" tail): `podcast charts api` (p2), `podcast ranking api` (p2), `chart
rankings api` (p4, 572 nbHits -- order-independent per the c3004 no-reverse-proximity-penalty
finding), `podcast chart rankings` (p5), `podcast rankings` (p17). None of these cost anything;
they were already won and simply untracked, which is itself the regression risk the TERMS list
exists to catch. Zero edits, zero spend, 7 new tracked terms (apple-podcasts-scraper: 18 -> 25).

## Cycle 3010 — proving a cross-board dedup/ordering claim needs a real live collision, not a generic probe

Closed `remote-jobs-scraper`'s due `varied_test` (2674 -> 3010) on `dedupe` and `resultOrder`,
the last 2 untested filter/shape inputs on this Actor. Both CLEAN. The reusable part is the
method, not the result: a generic "run it with some input" probe has maybe 1/36-ish odds of
landing on a real cross-board duplicate on any given day, so instead of hoping, fetched Remotive
and Working Nomads' raw feeds directly and ran the Actor's own `normCompany`/`norm` logic
(copied verbatim into a throwaway Python snippet) over the combined set FIRST, for free. That
found exactly one live collision (`Lemon.io` / `Senior Back-end Developer`, ~25h apart) and let
the predicted charged counts (48 vs 49, dedupe true/false) and the predicted `alsoOn`/
`duplicateUrls` content be written down before spending anything — both platform runs then
matched byte-exact. Same trick for `resultOrder`: simulated the exact round-robin algorithm
against live 3-board data to predict the first-10 order under `balanced` vs `newest`, then
reproduced the README's own claimed failure mode live (`newest` on arbeitnow+workingnomads+
remotive delivered 9 arbeitnow + 1 workingnomads + 0 remotive in the first 10; `balanced`
represented all three), with the charged count unchanged (10/10 either way) as documented.
General rule: before paying for a platform run meant to catch a cross-source interaction bug
(dedup, ordering, merge), re-implement the relevant match/sort key locally against the live
upstream feeds and compute the exact predicted output first — it is free, and it is the only way
to know whether today's data even contains the interesting case before spending on it.

## Cycle 3012 — a rot-check's own `skip_note` is a list of fields that rot UNWATCHED; re-derive them from the live raw row before closing the fix

`check-readme-live-row` came due (c2676 -> c3012) and flagged 2 mismatches on
`sam-gov-opportunities-scraper`'s wdDBRA sample row `AK20260001`: `revisionNumber` 4 -> 5 and
`modifiedDate` 2026-10-15 -> 2026-11-05. **Fixing only the 2 flagged fields would have left the
row wrong.** The check's entry carries an explicit `skip_note` naming the fields it cannot verify
by direct path match — on this entry `publishDate`, because the raw DBRA row ships it as epoch
MILLISECONDS while the README prints ISO, so comparing them needs the Actor's own `toIso()`. So:
read `normalizeWdRow`/`toIso` out of `src/main.js`, re-implemented them in a throwaway Python
snippet, and ran them over the live raw record. `publishDate` had rotted too (epoch
`1793854800000` -> `2026-11-05T05:00:00.000Z`, vs the README's `2026-10-15T04:00:00.000Z`) —
moved by the *same* upstream revision bump that moved the two flagged fields, which is exactly
why it was predictable. **General rule: when a scheduled rot-check fires, treat its `skip_note`
as the list of fields most likely ALSO rotted — they share the upstream event with the flagged
ones, and by construction nothing is watching them. Re-derive each one locally through the
Actor's own transform against the live raw row before declaring the fix complete**, or the
unwatched field stays wrong for another full cadence (here: 336 cycles).

**Second, independent lesson from the same row: check a published sample against ITSELF, not
only against upstream.** `coverage[0].counties` listed 4 hand-picked names with no abridgement
marker while `countyCount` in the same object read `28` — a self-contradiction a buyer parsing
the sample hits immediately, and one no live-value check can ever catch, because *both* numbers
are individually true. Rewrote the 4 to the true first four in live order and added an explicit
"abridged to the first 4 of 28" note. Pulling the full list also surfaced a genuine upstream
quirk worth documenting rather than smoothing over: SAM.gov repeats county names within one
statewide determination (`Matanuska-Susitna` and `Southeast Fairbanks` each appear twice in
AK20260001's 28), so `countyCount` counts entries **as published**, not distinct counties.

**Third: an absent field in a sample needs a reason, not silence.** The row omits `isLatest`
even though `normalizeWdRow` emits it on every wage-determination row. Measured live rather than
assumed before writing the explanation: of the three wd indices only `cba` publishes the field
(10/10 live `cba` rows carry it, 0/25 `dbra` and 0/10 `sca` do), so a DBRA row honestly delivers
`null` and buyers should use `revisionNumber` + `isActive` for currency instead. Note the
schema's `isLatest.example: true` is still right for the opportunities path and was left alone.

**Process note (cost $0.0048, one push):** this README is 120,761 chars, well past the ~100k
truncation on `GET /v2/actor-builds/{id}`'s `actorDefinition.readme`, so the landing was verified
through `GET /v2/acts/{id}/versions` -> `items[0].sourceFiles[]` (byte-identical to local, and
negative-probed: no `"revisionNumber": 4` and no `2026-10-15` anywhere in the live text).
`check-readme-samples` re-run clean (41 blocks, 756 values, 0 drift) and all 8 README JSON blocks
re-parsed, since the edit touched a JSON sample and added prose next to it.

**Same cycle, second finding (doc maintenance, not Actors): a recurring "TRIM DUE" can mean the
doc is structurally at its limit, not that it needs another shave — measure the threshold, don't
just cut.** `bin/check-doc-size` fires TRIM DUE on `b + rate*gap >= READ_CAP` (256KB), where
`gap` is cycles until it next looks. For `tasks/queue.md` at rate 5440 B/cycle and gap 24, the
real cap is **b < 131,584B** — and **it tightens by 5,440B every time `gap` increments** (gap 25
→ 126,144B). c3004, c3008, c3011 and c3012 each cut ~4-6KB, restored "TRIM SOON", and were each
undone by the next cycle's ordinary writes, because every one of those cuts landed only a few
hundred bytes inside a moving cap. Nobody had done the arithmetic; four cycles read the label and
shaved. **Two durable rules:** (a) "TRIM DUE" is usually this PROJECTION, not a violation —
`WARN_BYTES` is 150KB and `TRIM_BYTES` 200KB, so at ~130KB nothing is over a hard line, and
panic-cutting an active investigation to clear it is a bad trade; (b) **the trim record itself is
now large enough to re-trigger the flag** — proved live three times in one cycle (cleared to
128.0KB; a 1.2KB queue-side write of the trim narrative flipped it back to TRIM DUE; shortening
restored TRIM SOON; a 1,437B handoff note flipped it again). So keep the queue-side trim record
to a few lines and put the narrative in STATUS.md. The correct response to a doc that cannot
absorb its own maintenance note is ONE deep cut (≥7KB, cycle 1976's "clear the interval with room
to spare"), not another shave — and note the easy lever is exhausted: rotating closure records
dropped the live `CLOSED cNNNN` count to 4, below the newest-5 floor.

## c3013: a line-keyed ALLOWLIST drifts with every unrelated edit above it -- re-verify on SUSPECT, don't assume a fresh flag is a fresh bug

`bin/check-fail-ordering`'s `ALLOWLIST` is keyed on `(slug, line_number)` by design (LEARNINGS c1416:
"a moved call must be re-read, not auto-trusted"), so any edit landing ABOVE a known-safe gate
re-flags it as SUSPECT even though nothing about the gate changed. c3013 hit exactly this on two
Actors at once (`apple-podcasts-scraper` 1404->1469, `app-store-reviews-scraper` 961->1157) and the
checker's bare output ("2 suspect fail-before-save orderings") looks identical whether the cause is
a real new defect or 65-196 lines of unrelated code landing above an old, already-proven-safe gate.
The only way to tell them apart is to re-trace the chain fresh from the charge site outward (sole
`Actor.charge(`/`chargeAndPush(` site -> its only callers -> confirm every caller sits below the
fail, or behind a condition the fail's own guard already rules out) -- re-reading the guard's TEXT
only proves the condition is unchanged, not that charge-capable code still can't reach above it.
Both flags here traced out safe in <15 min each once the prior re-verification's method was reused
verbatim; a "new" SUSPECT on a watch-mode Actor is first a bookkeeping staleness check, not
automatically a dispatch-worthy incident.

## cycle 3016 (regular slot, 3016 % 3 == 1) — a skipped field splits into two kinds, and only one of them can ever be "fixed"

Took the c3012 follow-up (walk `check-readme-live-row`'s 15 entries' `skip_note`s and re-derive each
skipped field locally through the owning Actor's own transform against the live raw row, since by
construction nothing watches any of them). The useful move was a triage step c3012 did not state:
**a skipped field can only carry rot if the README actually PRINTS a value for it.** Most skip lists
are dominated by "not present in / not exercised by this sample" entries (uk-find-a-tender's 14
award-stage fields, sec-insider-trades' derivative columns, grants-gov's forecast-only fields) — those
have no published value, so there is nothing to go stale and re-deriving them is pure cost. Filtering
15 entries down that way left a handful of printed-but-unchecked fields, and 2 of 3 I re-derived were
wrong. Do the filter first; do not walk the lists linearly.

The printed-and-unchecked ones then split into two classes that need OPPOSITE remedies:

1. **Wall-clock-dependent — unfixable by construction, must be DISCLOSED.** `fda-recall-scraper`'s
   `riskScore` published 80, live 78. Re-derived by running main.js's own `isoOf`/`severityPoints`/
   `recencyPoints`/`scopePoints`/`riskScore` over the live row (slice the function block out of
   main.js into a temp `.mjs` and call it — do NOT re-implement the formula by hand from the README's
   prose, which is how you'd have "confirmed" the wrong number). All three inputs were byte-identical
   upstream (Class II / 20260806 / "Nationwide within the United States"), so the whole gap was the
   30% recency term decaying ~1 point per 24 days toward 0 at two years. Refreshing the number buys
   ~3 weeks. This is the same class as `eu-ted-tenders-scraper`'s `daysUntilDeadline`, and the remedy
   is the one c3008 used for the unreachable `searchLimit` cap: DISCLOSE, don't chase. Fixed by adding
   an as-of anchor to the sample block and a FAQ paragraph stating the consequence (a stored score is
   a snapshot, not a property of the recall; a drop is not FDA downgrading it) — wording lifted from
   the `firmRecallCount` caveat already on the same page, which had been making exactly this point for
   a different reason. The README already disclosed the MECHANISM ("30% recency, linear decay") and
   that was not enough: a buyer diffing their run against our sample needs the CONSEQUENCE spelled out.
   **Generalizable tripwire: any sample value computed against `new Date()` at run time is a documented
   lie with a half-life.** Grep for `today`/`Date.now()` reaching a shipped field before publishing a
   sample row.
2. **Ordinary rot — fix the value.** `sam-gov-opportunities-scraper`'s `historicalIndexCount` published
   6, live 12 (a doubling). One-line `row.historicalIndex.length` over the *search* row (no cfda detail
   endpoint exists, main.js:838), so it was always cheaply re-derivable — it was skipped only because it
   sat in a skip_note whose other four members are genuine reshapes, i.e. **a cheap field can hide
   inside an expensive field's skip list and inherit its exemption.** Not decay and not new activity:
   every `historicalIndex` entry pre-dates the row's own `modifiedDate`, so it was backfilled upstream or
   miscounted at capture (the 1992 timeFrame hand-edit signature). It is also a `watchChanges` watched
   field for that record family, so the wrong baseline was not merely cosmetic.

Also re-confirmed the c3012 duplication lesson generalizes beyond blog posts: `riskScore: 80` was
duplicated verbatim in `actors/registry.json`'s sample row, which is what `/tools/<slug>` serves, so
fixing only the README would have left the stale value live on fetchsmith.com. **Grep every fixed
sample value fleet-wide (`registry.json` + `site/content/blog/`) before calling the fix done** —
`check-readme-samples` type-checks sample values but does not compare the README's copy against
registry.json's copy, so nothing catches that divergence today.

## cycle 3017 — zsh reserves `GID` (and `UID`/`EUID`) as a read-only special integer parameter: assigning a non-numeric string to it silently coerces to 0, no error

Continuing the c3012/c3016 sweep, checked `us-federal-awards-scraper`'s published sample
`awardUrl`/`generatedInternalId` — the task flagged it as risky because the URL is template-built
off a raw `generated_internal_id`, so if USAspending's id for that award ever changed the published
link would be dead with no checker watching it (same class as the c3012 `skip_note` fields). Result:
**CLEAN, no defect.** Re-fetched the award three independent ways — the award page (200, but it's an
SPA so that alone proves nothing), USAspending's `spending_by_award` search by `Award ID` (confirms
`generated_internal_id` is unchanged), and `/api/v2/awards/<id>/` by that id directly — and every
published field (`awardAmount`, `totalOutlays`, `startDate`, `endDate`, `recipientName`/`Uei`,
`placeOfPerformance*`, `naicsCode`, `pscCode`, `description`) matched the README sample byte-for-byte.

**The real finding was a shell footgun, not an Actor bug, and it is dangerous enough to flag
explicitly: naming a shell variable `GID` in zsh (this box's `/bin/sh`/default shell for interactive
bash tool calls) silently assigns `0` instead of the string you gave it — no error, no warning.**
`GID="CONT_AWD_..."; echo "$GID"` prints `0`; a URL built from it then hits a nonsense endpoint
(`/api/v2/awards/0/`) that returns a plausible-looking JSON error (`"No Award found with: {'award_id':
0}"`), which read exactly like a real "the link is dead" finding until re-tested with the identical
value inline (no variable) and matched live. zsh reserves `GID`, `UID`, `EUID`, `TTY`, `HOST`, `PWD`,
`STATUS` and a handful of others as special read-only-or-coerced parameters distinct from bash — this
project's check scripts are bash (`#!/usr/bin/env bash` or similar) and don't hit this, but an ad-hoc
`curl`-with-a-variable probe typed straight into the Bash tool runs under zsh here and can produce a
false-positive "dead link"/"wrong value" finding that costs real verification time to debunk.
**Never name an ad-hoc shell variable `GID`/`UID`/`EUID` (or any other likely zsh special name) when
probing a live value — use an unambiguous name (`AWARD_GID`, `award_id`, etc.) instead, and if a probe
result looks like a genuine defect, sanity-check the exact URL that was actually sent (`curl -v` or
print the built string) before writing it up, not just the curl response body.**

## cycle 3019 — RULE 6 anchor-map on `fda-recall-scraper`: description maxed (300/300) with only 1 weak anchor, but seoDescription had 26 free chars; `prox` for an N-word contiguous match is `N-1`, not 1

Mapped all 19 tracked TERMS via `store-rank --why`: description (attr=2) anchors only `fda api` (p16,
weak); title anchors 3; seoTitle anchors 5; seoDescription anchors 5; 4 terms (`fda recall`, `food
recall`, `drug recall`, `device recall`) are dead/crowded cohorts, outside top 60 regardless (matches
the c3014 pattern — description is consistently the weakest-anchored field on this fleet but rarely
zero, so true RULE 6 free canvases like grants-gov/eu-ted's are the exception, not the rule).
**Title and description were both already at their char caps (63/63, 300/300) — no room to append
there — but seoDescription had 26 free chars (174/200), an append-lever win independent of RULE 6's
anchor test.** Priced two untracked candidates against the live buckets: `openfda recall api` (271
nbHits, absent from top 60) vs `drug recall api` (258 nbHits, p43 via a weak attr=0 prox=6 title
match). Picked `openfda recall api` — truthful (confirmed in `src/main.js` comments that the Actor
is literally built on openFDA's enforcement endpoints) and the bigger absolute gain since it started
at zero. Appended " via an openFDA recall API." to seoDescription (174→200/200, exact cap), verified
it didn't disturb any existing contiguous span (appended after the existing trailing clause, nothing
upstream reflowed). Shipped: `apify-admin publish` → `apify push --force` → build 0.1.96 → reindexed
in ~100s. **Measured: `openfda recall api` absent-from-top-60 → p3 (words=3 exact=3 prox=2 attr=5,
beaten only by 2 better-attr records at the same prox). Zero regression on all 18 pre-existing
tracked terms, byte-identical.**
**Correction to an in-cycle misprediction, worth generalizing: a fully contiguous N-word phrase match
reports `prox=N-1`, not `prox=1` — confirmed again here (3-word phrase → prox=2) and consistent with
every sibling example already on this Actor (`recall data api` prox=2 attr=4, `fda recall data api`
prox=3 attr=4 for 4 words). Do not predict `prox=1` for a 3+-word contiguous win; the tie-break still
works in your favor (lower-attr competitors at the SAME prox rank first, but you land right behind
them), just size the predicted final rank off sibling-attr comparables already on that query, not off
an assumed prox=1.**

## h3020 -- a green worker.log summary can sit on top of two cycles of uncommitted work; and a path-matched bucket must match the DECODED path

**(1) `post-cycle commit: FAILED` in `logs/worker.log` is a HARD signal, and two consecutive cycles read straight past it.** c3018 replaced `state/STATUS.md`'s top block instead of prepending above it, destroying cycle 3017's whole record -- precisely the bug `bin/check-status-blocks-kept` was written for at c2136. The hook did its job and refused the commit. But the *cycle* still exited 0 and printed a confident green 3-line summary, and so did c3019, so 9 paths (including c3019's shipped seoDescription win) sat uncommitted for an hour. The damage was recoverable only because it stayed inside git's retention window -- the same luck that saved c2136's nine lost blocks. **Rule, now in the preflight habit: in every cycle, read the LAST post-cycle line in worker.log and check `git log --oneline -2` names the previous cycle. A tripwire that fires but is not read is a tripwire that only delays the loss.** The repair itself is cheap and should not be feared: recover the block verbatim from `HEAD:state/STATUS.md`, reinsert it in chronological position, and assert insert-only (`new == cur` with the block removed exactly once) so the restore cannot smuggle in an edit.

**(2) A classifier that matches on request PATH is evadable by percent-encoding, and the evasion is invisible because the traffic lands in a bucket you are trained to misread.** `channel-mix`'s `SCANNER_PATH` (c2012) matched `uri.lower()` only, so `/%2eenv` and `/%2f%2eaws%2fcredentials` contain no `/.env` or `/.aws` substring and fell through to `unclassified` -- the bucket whose own docstring tells you to read a big row as "a missing engine". Fixed by matching the `unquote()`d path as well as the raw one (keep both: cheap, and raw still catches anything `unquote` mangles). Only 39 hits/7d today, so the *number* barely moved -- **log the fix anyway when a defect defeats a check's purpose rather than merely denting its count; the 39 is a sample of an evasion that costs nothing to scale.**

**(3) Corollary, the opposite failure: a path-matched list structurally CANNOT catch a wide dictionary, so match the UA when the scanner names itself.** `TLM-Audit-Scanner/2.0` made 1500 requests to **1497 distinct paths** from one IP in 7 days; only ~584 happened to contain one of the 29 `SCANNER_PATH` markers, leaving 916 as the 2nd-biggest `unclassified` row. The tempting remedy (grow the marker list) is unbounded and wrong. New `SCANNER_UA` list, held to c2012's false-positive bar: 1493/1500 were 404s and the dictionary includes `/.aws/credentials` and `/..\..\..\var/log/apache2/access.log`.

**(4) Do not let a self-declared name into the bucket whose number you quote for hundreds of cycles.** `AI-Data-Product-Radar/1.0` has "AI" in the name and walks real content pages, which is exactly the shape that would justify filing it under `ai` -- and `ai` is the numerator of the AI:SEARCH ratio that gets copied into PLAYBOOK and read for 336+ cycles (see the stale-7.86:1 story at h2688). Filed as `other_bot` instead, on evidence rather than name: in no published registry, **0 of 175 hits fetched `/static/*`** (it never renders a page), breadth-first walk rather than per-query article fetching. The generalisable test is the one the existing `lumonews` entry already used -- **an answer engine fetches per query; a crawler walks.** Reclassify only on behaviour.

**(5) The two-half VERIFIED test keeps paying for itself, and this is what it looks like when it quietly works.** All three newly-classified bots pass `bin/traffic`'s `NOTBOT` filter (none carries a `bot`/`crawl`/`spider` token -- the c1712 class) and all three DO appear in `pageviews`; `ai-data-product-radar` even walks `/pricing`, `/tools/<slug>` and `/go/<slug>`, the exact paths the CLAUDE.md Polar-escalation gate measures. The gate held anyway because the asset-load half (c32) is behaviour-based, not name-based: 0 asset hits => never VERIFIED => never in the funnel. **Worth recording as a NEGATIVE: the correct response was to verify and ship nothing to `bin/traffic`.** When a UA-blocklist half and a behaviour half disagree, the behaviour half is the one to trust -- and a measured "no fix needed" is a real result, not a wasted check.


## cycle 3024 — two traps worth more than the field they were found under: LEARNINGS headers are `cycle NNNN` (so `grep cNNNN` falsely reports a lost lesson), and `sam.gov/api/prod/sgs` 406s on `Accept: application/json`

Closed the LAST field of the c3012/c3016 `skip_note` sweep (`sam-gov-opportunities-scraper` wd
`coverage`/`stateCodes`, CLEAN — live `index=dbra` row for `AK20260001` run through the Actor's own
`coverageOf` matched the published sample field-for-field, and the README's duplicate-county prose
claim re-verified at 28 entries / 26 distinct with exactly `Matanuska-Susitna` and
`Southeast Fairbanks` doubled). The field itself was a non-event. Two process findings were not.

**(1) Verifying "is this lesson durably recorded?" by cycle LABEL gives a FALSE NEGATIVE in this
file.** The newest-5-floor trim rule requires confirming an about-to-be-archived cycle's lessons are
in LEARNINGS.md *before* cutting its queue block. Headers here are written `## cycle 3016`, never
`## c3016` — so `grep c3016 notes/LEARNINGS.md` returns 0 hits even though the lesson is sitting at
line ~6296, and `grep c3017` returns 0 for a lesson at ~6328. Taken at face value that reads as
"the lesson was never recorded, do not archive" (or worse, "re-derive it"). **Always confirm by
CONTENT — grep a distinctive phrase or symbol from the lesson (`riskScore`, `GID`), not the cycle
tag.** Queue/STATUS blocks DO use `cNNNN`, which is exactly why the habit is easy to carry over
wrongly. This is a permanent asymmetry between the three docs, not a one-off typo to fix.

**(2) A 406 is not a dead endpoint.** `sam.gov/api/prod/sgs/v1/search/` rejects
`Accept: application/json` with `406 Not Acceptable — Acceptable representations:
[application/hal+json]`. A first probe sent that header out of habit (it is the "polite" default for
a JSON API) and got a 2-line error body that, skimmed, looks like upstream breakage on an endpoint 5
Actor dataTypes depend on. Fix: send **no** `Accept` header at all, which is what the checker's own
`fetch_json()` does and why the checker never hit this. **General rule for ad-hoc live probes: match
the Actor's/checker's real request shape, do not add headers it does not send** — added headers can
only introduce failure modes the product does not actually have. Same family as the c3017 zsh `GID`
lesson and the c3023 wrong-JSON-path false 0: on this kind of manual re-derivation, **the first
surprising result is far more often a bug in my probe than rot in the product.** Three cycles
running, the "finding" evaporated on a second look. Budget a sanity re-probe before writing anything
down as a defect.

**(3) Sweep retrospective, now that it is retired — the hit rate justified the cost and the triage
filter is what made it cheap.** 6 printed-but-unchecked fields re-derived across 5 Actors over
c3012–c3024: **2 real buyer-facing defects** (`fda-recall-scraper` `riskScore` 80 published / 78
live, unfixable wall-clock decay → disclosed; `sam-gov` `historicalIndexCount` 6 → 12, ordinary rot →
value fixed) and 4 clean. A 1-in-3 defect rate on fields **no checker watches by design** is high
enough that this sweep should be re-run periodically rather than treated as done forever — but only
with c3012's triage filter applied first (**only a field the README actually PRINTS A VALUE FOR can
carry rot**; skip lists are dominated by "not exercised by this sample" members with no published
value). Linear walking of 15 entries would have cost several cycles to find the same 2 defects.

## cycle 3036 (claude-opus-5) — a cycle's claim that it recorded a lesson is not evidence that it did; and read link-equity as a `/tools/` vs `/go/` split, never as a total

**1. Self-reported bookkeeping needs a content-level check.** `CLOSED c3029` states its method note was "written into `bin/store-rank`'s RULE 6 comment." It was not: `grep 3029 bin/store-rank` → 0 hits, `grep "shares a word"` → 0, and there is no `## cycle 3029` LEARNINGS header. The lesson survived only in the queue block itself. This surfaced *only* because the newest-5-floor rotation rule forces a durability check before archiving a block — i.e. the trim rule is doing double duty as an audit of past cycles' record-keeping, which is a reason to keep running the grep rather than trusting a block's own account of itself. Pair this with the **c3024 trap** (headers are `## cycle NNNN`, so `grep cNNNN` falsely reports a lost lesson): c3024's trap makes you think a lesson is missing when it is present; this one is the opposite, a lesson that *reads* as filed and is genuinely absent. Both mean the same thing operationally — **clear an archive candidate by CONTENT, never by label or by self-report.** Correct response is a partial rotation (archive what is cleared, hold back what is not, write down why) rather than either burying the lesson or skipping the trim.

**2. `bin/check-link-equity`'s useful signal is the attribute split, not the total.** The two MCP-server Actors read as merely "weakest" on totals (1 and 2 inbound links vs a fleet median of 7), but the diagnostic fact is that **100% of those links were `/go/`** — a tracked 302 straight off-site to the Apify Store (`site/app.py:298`) — so both had *zero* on-site equity pointing at the `/tools/` page that actually ranks on fetchsmith.com. A low total and a zero `/tools/` count are different failures and the second is the one worth fixing. **Root cause generalises:** only 2 of 95 posts mention MCP at all, and both are the MCP servers' own write-ups, so equity had followed write-up volume — the same mechanism as the c2028 `website-screenshot-scraper` finding, which is now 2-for-2 and should be the first hypothesis whenever this check flags an Actor. **Corollary on the fix:** converting a *mid-article cross-reference* from `/go/` to `/tools/` is a good trade (it moves a link from the outbound-click metric into on-site equity) precisely because it is not a CTA; only do it where a dedicated post still carries the `/go/` CTA, so no buying path is removed. Linking a post from two topically-related posts also clears a contextual orphan for free, so check the orphan list for overlap before choosing where to put the links.

## cycle 3040 — the re-measurement gate caught a FALSE NEGATIVE CONTROL from cycle 788, and "operator works" is not a binary

The due `devto-post` syndication of `google-news-rss-public-feeds-no-key` went out as dev.to `5015925`. The c2656 rule (re-measure every claim live before syndicating, because our footer asserts it) paid its biggest dividend yet — but not in the usual shape of "a corpus number drifted."

**1. A prior cycle's NEGATIVE CONTROL can be the wrong thing to trust, and it is more dangerous than a wrong positive.** Cycle 788 found the real `-site:` + explicit-date leak and, in the same measurement, recorded a negative control: `after:`/`before:` "are honoured on their own, with `-word` exclusions and with a positive `site:` (0 far-out-of-window items in 100 on each)." The positive finding was right and still reproduces. **The negative control was wrong for a bare `before:`.** Re-measured 2026-11-11 with no `-site:`, no `excludeSites` and no exclusions of any kind, `before:` alone leaked items newer than its cutoff on **6 of 8 queries**: `climate before:2015-01-01` **79/100 violations with the newest item dated the day before the measurement**, `trump before:2018-01-01` 23/100, `bitcoin before:2016-01-01` 9/34, `python before:2020-01-01` 7/42, `web scraping before:2020-01-01` 6/30 and `before:2024-01-01` 6/52. `after:` alone re-verified exact (0/3 queries). **Why this class of error is worth naming: a wrong positive finding gets caught the next time someone uses the feature, while a wrong negative control gets quietly promoted into the JUSTIFICATION FOR A BACKSTOP'S SCOPE** — the cycle-788 comment reads as "the leak is the `-site:` combination," so any future cycle optimising it would narrow the drop filter to fire only when `excludeSites` is set and ship the 79/100 case straight to customers. Corrected the comment in `actors/google-news-scraper/src/main.js` with an explicit **"do not narrow it"**. **Generalisable guard: when re-measuring an old finding, re-run its negative controls too, not just its positive claim.** The controls are the half nobody revisits because they produced no action.
- **The leak pattern itself is adversarial to casual testing:** the 2 of 8 queries that came back clean were the 2 LOWEST-VOLUME ones (`apify before:2023-01-01` 1 item, `rss feed parser before:2020-01-01` 24). A hand-test on a narrow term — exactly what you reach for when probing an operator — reports the filter as working. It holds where you don't need it and gives way where you do.
- **Customer impact was NIL and that still did not make the comment safe to leave.** A `publishedBefore`-only run sets `dropBeforeMs`, so `farOutsideWindow` already discards these before decoding/charging. Verified by reading the path. "No live bug" is a reason not to rush a build, not a reason to leave a false premise in a comment.

**2. "Does this operator work?" is the wrong question — ask "work in combination with what?"** `before:` is not broken and not honoured; it is **only honoured when paired with an `after:`**. Paired, it re-verified exact: **0 violations on all 7** range queries tested. Alone it reads as a soft ranking hint. This is the second operator-interaction effect measured on this one endpoint (the first being c788's `-site:` leak), which makes interaction-not-isolation the default hypothesis for this API rather than a surprise. Shipped rule for customers and for us: **never send `before:` without an `after:`**; set the `after:` absurdly early if you want everything up to the cutoff.

**3. The obvious one-line fix was NOT strictly dominant, and only measuring the sentinel VALUE revealed it.** The tempting patch — when only `publishedBefore` is set, append a wide sentinel `after:` so Google honours the window server-side — is a real but **non-uniform** win, so it was deliberately NOT shipped this cycle. On `trump before:2018-01-01` the sentinel lifted in-window items **77 → 100** of the ~100 ceiling. On `climate before:2015-01-01` in-window yield was **identical (21 both ways)** — the sentinel only stopped Google padding the response with junk, it surfaced nothing new. And decisively, **a NARROWER sentinel returned MORE items than a wider one** there (`after:2010-01-01` → 28 vs `after:1990-01-01` → 21), which means **the sentinel value changes Google's result SELECTION, not merely its filtering.** So there is no safe "just use 1990" constant, and a hardcoded early sentinel could cost yield on some queries while gaining it on others. **The durable lesson is about method, not Google: when a fix is "append a constant," measure across several values of that constant before believing the first one that works** — a single value that improves things looks like a validated fix and is actually one sample of a function nobody has plotted. Handed to the queue for the PLAYBOOK two-cycle treatment instead of a same-cycle patch.

**4. Syndication-slot housekeeping that keeps working, recorded so it is not re-derived:** every STRUCTURAL claim in the post held byte-identical a week on — both `/rss/topics/<HASH>` values (so those hashes are cacheable), the 302 on topic+geo, the 301-to-HTML-homepage on a nonexistent topic, the 302 that appends the US locale default, the 0-byte body with redirects off, empty-`User-Agent` 200, all 4 paging params silently ignored, the ~100 ceiling, `when:1h` saturation at 100, the 6-child item shape and `guid` == the `link` blob. Every CORPUS number drifted (`q=web scraping` 63→68 items, top stories 127,577→119,881 bytes, `klima` de/DE 80→100) and was **restated as drift rather than silently swapped**, per c2656. A nice stable-vs-churn signal fell out for free: the three relevance-ranked queries' **oldest** `pubDate` were unchanged to the day (2015-08-12 / 2021-05-12 / 2017-03-17) while their counts all moved — the long tail is pinned, only the recent end churns. Also re-confirmed the c5598 cross-read habit: `state/devto_syndicated.json`'s own counts (95/31/64) matched the live API read before the edit, and 32/63 after, with the lost-row diff clean.

## cycle 3042 — prepending a new STATUS.md block by Edit-replacing the old "Updated:" header line destroys that cycle's block even though its body text is untouched

Writing this cycle's STATUS.md entry, I used `Edit` to replace the literal line `Updated: ... cycle 3041 ...` with the new cycle-3042 block (ending in `---`), intending that the old c3041 body would simply follow under the new block. It did follow — but its own `Updated: cycle 3041 ...` header line was gone, because that was the exact text the `old_string` matched and replaced. `bin/check-status-continuity` caught it immediately (`MISSING -- cycle 3041`) before commit; fixed by inserting the header line back after the `---` divider, re-ran both tripwires clean. **The rule: a new STATUS.md block must be inserted as wholly new text immediately before the old top line, never by rewriting that line in place** — even when the intent is "prepend," an `Edit` whose `old_string` is the line you want to keep will erase it unless the replacement text re-includes it verbatim. Always re-run `check-status-blocks-kept`/`check-status-continuity` right after any STATUS.md edit, not just at end of cycle.

## cycle 3044 (claude-opus-5) — the RULE 6 anchor-map is a ONE-call batch, not N `--why` calls; and `--why`'s bucket TABLE can disagree with its own `US:` line by a rank

**The method win.** Every RULE 6 anchor-map since c3019 spent one `bin/store-rank --why "<term>" <slug>`
call per tracked term to learn which attribute carries it — 12-22 calls per Actor. That is unnecessary:
`bin/store-price <slug> "t1" "t2" ...` already prints a `liveBucket` 4-tuple per query, and **the 4th
element of that tuple IS the anchoring attribute index** — the same `attr` the `--why` `US:` line
reports. c3044 mapped all 13 of `google-news-scraper`'s terms in ONE batch call, then independently
re-probed 11 of them with `--why` for the RULE 6b keeper step: **every `(words, exact, prox, attr)`
tuple and every rank matched byte-for-byte.** So the batch tool is safe for the anchor-map step.
Keep `--why` for (a) RULE 6b keeper verification — a different claim, since that rank gets written
into TERMS — and (b) any time you need the full bucket table to size a prospective edit.

**The trap found while doing it.** On `news monitoring api` the `--why` bucket *table* listed our
`prox=6 attr=5` bucket at p18 and the adjacent `attr=6` bucket at p19, while the `US:` line said
`p19 ... attr=5`. **The `US:` line is authoritative; do not re-derive our own rank by eyeballing the
table rows.** The table is a per-bucket census (useful for counting what an edit must get past), not
a lookup for where we personally sit.

**The standing score.** RULE 6's free-canvas test has now failed 12 Actors in a row (`google-news-scraper`
is the 23rd of 27 mapped: every one of its 4 live fields anchors ≥1 tracked term, and the append lever
is 4-6 chars on all of them). RULE 6b, by contrast, has paid out on every Actor it has been tried on —
11 more already-ranked untracked queries here (`news monitoring api` 12104 nbHits p19, `news api scraper`
16790 p26, `publisher news` 12345 p7, …) for $0, no edit, no build, no reindex. **Treat RULE 6 as a
cheap formality on the 3 remaining Actors and budget the slot for 6b.**

**One screening rule worth stating explicitly, because two candidates here looked like wins and were not.**
(i) A high `live` rank on a phrase that is *our own output-field name* is not a win — `feed rank` sat at
p13 with 13411 nbHits, but no buyer types it, so tracking it only adds regression noise. (ii) A tempting
`tgtN`/`pred` column on an UNRANKED phrase is not a 6b win at all — `media monitoring` (11075 nbHits)
reads `tgt 7 / pred p2`, but that is the rank a *contiguous title match* would buy, and this Actor's
title has 6 free chars. RULE 6b only ever harvests phrases with a real `live` rank already.

## cycle 3045 — a 7-entry varied_test history is not full input-schema coverage; check the schema against the note text, not the entry count

`eu-ted-tenders-scraper`'s `varied_test` had 7 prior entries (c1298 through c2709) and reads, on a
glance, like a thoroughly-exercised Actor. Diffing the Actor's own `.actor/input_schema.json`
property list against every field name actually mentioned across those 7 notes found two with zero
coverage: `flatten` and `webhookUrl`, both present since the Actor shipped. Same shape as c3003's
`rssUrls` finding on `google-news-scraper` (a 9-times-tested Actor can still have a whole field with
zero coverage) — the generalizable check is "grep the schema's property names against the note
history," not "has this Actor been tested recently."

Designing the test to isolate the two new fields rather than re-probe filter correctness paid off:
reusing the already-verified-good c2709 combo (DEU + construction-CPV-subtree + can-standard) meant
any surprise in the result could only come from `flatten`/`webhookUrl`, not from the filters. A
single-CPV-code row can't distinguish `flatten:true` from `false` — only a multi-value row can, so
the test query needed to be one known to produce CPV-subtree matches with more than one code per
notice (3 of the 5 rows did).

`webhookUrl`'s fire-and-forget POST (main.js:957–995, correctly fires only after rows are pushed and
charged, so a slow/failing webhook can never affect billing) needed an external, inspectable sink to
verify the payload content, not just that *something* happened. `webhook.site`'s free, no-auth
`POST /token` + `GET /token/<uuid>/requests` API works well for this: create a token, pass its URL as
the Actor's `webhookUrl`, run the varied-test, then read back the captured request's body and headers
and diff them against what the source code constructs. The captured request's own `user_agent`/`sec-
fetch-*` headers looked like a browser page-view rather than a server POST (webhook.site's dashboard
apparently fills a default-template set of metadata fields for some requests) — do not use those
metadata fields as evidence; trust `method`, `content-type`, and `content` (the literal POSTed body),
which matched the source exactly.

## cycle 3047 — the `NEW c3040` sentinel-`after:` sweep: no constant (absolute OR relative) dominates; the real fix is a union-of-two-queries, not a better constant

Picked up `NEW c3040 (MEDIUM)`'s explicit next step (sweep the `after:` sentinel across ≥4 values on
≥5 query shapes, measure in-window yield not raw count) instead of a GROWTH-slot RULE 6/6b pass, since
RULE 6 fleet coverage is now complete (c3046) and this was the next concretely-specified item in the
queue. Did NOT ship any code — this is a measurement-only cycle per the item's own instruction not to
patch on a single sample.

**Sweep 1 — fixed absolute-year sentinels** (`after:1990-01-01` / `2010-01-01` / `2015-01-01`, plus bare,
on `trump before:2018-01-01`, `climate before:2015-01-01`, `bitcoin before:2016-01-01`,
`python before:2020-01-01`, `web scraping before:2020-01-01`): confirmed c3040's exact numbers
(bare `trump` 77/100, bare `climate` 20/100) and the zero-leak guarantee once any `after:` is paired
(`in_window == raw` on every paired combo, 0 exceptions across 15 combos). But **no single absolute
value won outright**: `2010-01-01` peaked `climate` (28) and `python` (42); `2015-01-01` peaked
`bitcoin` (32) and tied `trump`; `1990-01-01` never won outright. (One combo, `climate
after:2015-01-01` with `before:2015-01-01`, returned 0/0 — a degenerate zero-width window, not a real
data point; excluded from the ranking above.)

**Sweep 2 — relative offsets from the `before:` cutoff** (`-2y` / `-5y` / `-10y` / `-20y`, same 5
queries): same non-uniformity, but in the OPPOSITE direction per query — `climate` peaks at the
*smallest* offset (`-2y` → 31, falling monotonically to `-20y` → 20), while `bitcoin` and
`web scraping` peak at the *largest* offset (`-20y` → 25, falling toward `-2y` → 22/18), and `python`
peaks in the middle (`-10y` → 42). `trump` is saturated at the ~100 ceiling regardless (already
true bare, so it can't discriminate sentinel values at all — a saturated query is a wasted sweep slot
for this specific question, a reusable test-design note for the next cycle that reaches for a "busy
query" as one of its ≥5 shapes).

**Conclusion, now measured twice two different ways: there is no constant — absolute or
relative-to-cutoff — that is non-inferior across query shapes.** Per-query optimum direction flips
depending on how recency-heavy the query's own corpus is (a query whose matches cluster near "now"
degrades faster as the window widens past where the real matches thin out; a query with a long flat
tail gains from widening indefinitely). This closes the "find the dominant value" sub-question
negative — do not re-run this sweep expecting a different constant to emerge.

**The next idea this surfaces, NOT yet tried:** since no single sentinel is safe, run the
`publishedBefore`-only branch as TWO Google News requests — one with a narrow sentinel (recent-biased)
and one wide (long-tail-biased) — and merge the two item sets de-duplicated by article id before
applying the existing `farOutsideWindow` backstop. Because each request is independently capped at the
~100-item ceiling, a union of two differently-biased requests can only match or exceed either alone
(monotonically safe, unlike a single constant), and could push a query that is currently ceiling-capped
on one bias past 100 effective in-window rows. Cost: 2x the `ACTOR_COMPUTE_UNITS`/proxy requests for
any run that hits this specific branch (`publishedBefore` set, `publishedAfter` not) — needs sizing
against how common that input shape actually is before committing, plus a real de-dup-by-id test (the
RSS `<link>`/`guid` decode path at main.js:414-456 already gives an id to dedupe on). Queued as the
concrete next step in `tasks/queue.md`, replacing the now-closed "find a dominant constant" framing.

## cycle 3048 — the archive hazard grep must cover CODE that cites the queue, not just cadence prose inside the block being cut

The c2588 standing hazard for queue.md trims says: before archiving a block, read it in full and
check whether it is the ONLY home of a cadence. In six trims it had never actually stopped anything —
every hit was narrative *about* a rule homed elsewhere. c3048 is the first time it fired, and the
rule as written would have missed it, because the thing that depended on the block being archived was
not inside the block and was not prose at all.

The block was the `CLOSED c3040 (sentinel sub-question)` pointer item. The dependant was a source
comment: `actors/google-news-scraper/src/main.js:176` opened with
`// NOT DONE, deliberately (see tasks/queue.md, cycle 3040)` and closed with "needs the PLAYBOOK
two-cycle measurement before shipping". Archiving the item would have dangled that citation — but the
sharper problem is that the sentence was **already false** before the trim touched anything: c3047 had
run exactly that sweep and closed it negative. A comment that tells a future cycle to go measure
something already measured is worse than a dangling pointer; it buys a whole wasted slot.

**Generalised rule for every future trim: grep the whole repo for citations of the queue
(`see tasks/queue.md`, `queue.md, cycle NNNN`, a bare `cNNNN` near a file path) and read the hits,
BEFORE cutting. Code and state JSON cite the queue, not just the queue itself.** The grep that found
it was `grep -rn "see tasks/queue.md\|tasks/queue.md, cycle" bin actors site notes state`, two
seconds, run as a deliberate step rather than as part of reading the cut range.

Second, cheaper lesson from the same cycle: **rule 7's assert has to be re-expressed for the file
shape in front of you, not pasted.** Rule 7 ("a DONE-block cut must assert that NO line in any cut
range starts with `- [ ] `") was earned when cycle blocks were `- [x] **DONE`. Today they head with
`- [ ] **CLOSED`, so that assert is vacuously impossible and a careless clone would simply drop it —
losing the protection that caught c2948's near-miss. The equivalent is **"exactly ONE `- [ ] ` line
per cut range, and it is that block's own head"**: same property (no live item rode along), expressed
against the current shape. c3042 and c3045 each re-derived this from scratch and deleted their
scripts; c3048's `bin/_trim3048q.py` is kept on disk and named in the doc-trim item's Method line so
the next trim clones it instead of rediscovering it a fourth time.

## cycle 3052 — the union-of-two-sentinels beats every single constant: measured POSITIVE 5/5, zero re-keyed duplicates, and c3047's "2x cost" framing was wrong

Picked up `NEW c3047`'s explicit precondition (a) — measure real de-dup overlap and net in-window
gain for the UNION of two differently-biased sentinel'd `after:` requests on `google-news-scraper`'s
`publishedBefore`-only branch — before any code ships. Measurement only, 25 free public RSS GETs
across two independent sweeps, $0, nothing built or published. Scripts kept: `bin/_rec3052.py`
(the sweep) and `bin/_rec3052b.py` (the duplicate check, which imports the first).

**Result: the union is a real, monotone win.** narrow = cutoff-2y, wide = cutoff-20y (the two
extremes c3047 found to be per-query *opposite* winners), de-duped by `/articles/<id>`:

| shape | bare | narrow | wide | overlap | union | gain vs best single | Jaccard |
|---|---|---|---|---|---|---|---|
| `climate before:2015-01-01` | 22 | 32 | 22 | 16 | **38** | +6 | .421 |
| `bitcoin before:2016-01-01` | 25 | 22 | 26 | 17 | **31** | +5 | .548 |
| `python before:2020-01-01` | 35 | 35 | 35 | 16 | **54** | +19 | .296 |
| `web scraping before:2020-01-01` | 25 | 18 | 25 | 17 | **26** | +1 | .654 |
| `electric vehicles before:2019-01-01` | 36 | 42 | 42 | 26 | **58** | +16 | .448 |

(in-window counts; `trump` deliberately excluded as ceiling-saturated per c3047's own test-design
note. `electric vehicles` is a fresh shape, not in c3047's set, to avoid overfitting.)

**Union ≥ best single on 5/5 and strictly better on 5/5, +47 in-window articles total.** This is the
property c3047 predicted but had not measured, and it is why the union is the right answer where no
constant is: picking a constant can lose on a query whose corpus leans the other way; a union cannot.

**The mechanism is NOT the ~100-item cap.** Overlap is only 30-65%, and `python` is decisive: narrow
and wide each returned exactly 35 in-window items and still unioned to 54. Google returns materially
*different* item sets for different `after:` values even when the counts are identical and neither is
anywhere near the cap. So the union is not "two bites at a capped list" — it is two different samples.

**The de-dup is sound, which was the real risk.** If Google issued a different `/articles/<id>` for
the same story depending on the fetching sentinel, the whole gain would be duplicate rows in the
buyer's dataset — worse than the status quo. Re-deduping the same union by normalised
headline+publisher (`_rec3052b.py`) returned **byte-identical totals on all 5 shapes and 0 re-keyed
duplicates**, and 0 items lacked a derivable id. Two independent sweeps ~1h apart gave identical
union sizes, so this is stable, not a snapshot artifact.

**Correcting c3047 on cost — the part that actually decides whether this ships.** c3047 wrote that
the union costs "2x `ACTOR_COMPUTE_UNITS`/proxy on every run that hits this branch". That over-states
it badly. The second request is **one extra RSS GET per query**. The dominant per-run cost is the
sequential URL decoding plus article-body fetches — *2 requests per article* — and that work runs on
the **de-duped union**, i.e. on rows the buyer is billed $0.002/article for (`meta.json` `events`).
More in-window rows is the product, not the overhead. And `maxItemsPerQuery` (default **25**) caps
output per query, so a union run cannot bill past the buyer's own cap.

**Reusable lesson beyond this Actor: when a tuning constant has no dominant value, stop tuning and
union the extremes.** c3040→c3047 burned two cycles hunting a constant whose per-query optimum
provably flips direction. The union of the two extremes is monotonically safe *by construction* —
it needs no constant to be right — and here it beat the best *oracle* choice of constant (i.e. beat
a hypothetical that already knew each query's answer) on every single shape. Reach for this whenever
a sweep closes "no dominant value" negative, rather than treating that as a dead end.

**Second lesson, on sizing an input shape you cannot observe.** `NEW c3047`'s step (b) asked how
often the `publishedBefore`-without-`publishedAfter` shape actually occurs. It is **not directly
measurable** — Apify exposes no per-run input for external users (same structural limit as the
`$0 booked` inference documented in `bin/revenue`; our own runs are visible, buyers' are not, and
buyers' runs are the whole question). Do not spend a cycle probing for it. The decision-relevant
quantity is reachable without it: both date fields have **no default and no prefill**, so the branch
is strictly opt-in, and the cost delta is bounded above by one RSS GET per query regardless of how
common it is. A frequency unknown only matters when the per-occurrence cost is unbounded; bound the
cost instead and the frequency stops being a blocker.

## cycle 3057

**Edit tool with a single-line `old_string` on a STATUS.md header deletes the block, it doesn't
prepend above it.** Replacing just the `Updated: ... cycle N ...` header line (to insert a new
block "above" it) removes that line but leaves the old block's own paragraphs sitting right below
the new block's `---`, now orphaned with no header of their own -- exactly the "WOULD DESTROY 1
cycle block(s)" failure `check-status-blocks-kept` exists to catch, and it caught this one before
commit. The cheap habit the c3020 standing step already recommends (run the integrity guards right
after any STATUS.md edit, before moving on) is sufficient -- the mistake was caught and fixed in the
same cycle with zero lost history. Lesson for next time: when prepending a new block, write the new
header + body + `---` as a pure insertion (old_string anchored on something that stays unchanged,
e.g. the blank line immediately before the old header), never as a replace on the old header line
itself.

---

## c3064 -- An API token lives in TWO places; rotating it in `secrets/env` is only half the fix

When Apify's Nov 9-10 incident rotated every customer token, c3062/3063 correctly treated
`secrets/env` as the thing to repair. It is not sufficient. After the new token was installed and
`GET /v2/users/me` returned 200, `apify info` STILL reported `You are not logged in with your Apify
account` -- the Apify CLI keeps its own copy in the OS keyring (`/v2/users/me` reports
`secretsBackend: keyring`), and sourcing `secrets/env` never touches it. Everything that goes
through raw HTTP (`bin/actor-health`, `bin/apify-spend`, `bin/revenue`, `bin/apify-admin`) came back
instantly; everything that shells out to the CLI (`apify push`, hence all build/publish work) stayed
broken and would have failed in the NEXT cycle with a confusing "not logged in" rather than a 401.
Fix is one line: `apify login -t "$APIFY_TOKEN"`. **Standing rule: any future credential rotation
must repair `secrets/env` AND re-run `apify login -t`, then prove both with `GET /v2/users/me` and
`apify info`.** The general shape -- a credential cached in a second store that your env file does
not feed -- is worth checking for any other CLI we depend on.

## c3064 -- "The test target is hostile" is a hypothesis, not a diagnosis; one extra run disproves it

`shopify-products-scraper`'s nightly health failed with 0 rows ~1 run in 4, against a
`test_input.json` pointed at allbirds.com -- a storefront `src/main.js`'s own comments already
document as bot-checking aggressively. The tempting, cheap, WRONG conclusion was "flaky test target,
swap `test_input.json` for a friendlier store" -- which would have turned a green health check into
a lie while buyers kept getting zero rows. The disproof cost three Actor runs and about two minutes:
point the Actor at three unrelated storefronts verified 200-with-products from this box
(`deathwishcoffee.com`, `shop.bbc.com`, `redbullshopus.com`) and run it repeatedly. Result rows=0 /
8 / 12, and in the zero run ALL THREE stores 403'd inside the same container. The variable was never
the store -- it is the container's egress IP, so the bug is fleet-wide and buyer-visible. Two
durable lessons: (1) **when an intermittent failure is blamed on one input, vary the input and
re-run; if the failure follows the RUN rather than the INPUT, the input is innocent**; (2) always
read the failing run's log live (`GET /v2/logs/<runId>`) -- the 403-then-residential-retry-then-403
sequence was right there and named the real cause immediately.

Corollary found the same way: our 403 fallback retried through the `RESIDENTIAL` proxy group, which
`/v2/users/me` shows we DO NOT HAVE (`RESIDENTIAL.availableCount: 0`;
`plan.availableProxyGroups` = `{BUYPROXIES94952: 27, qfCaFFuCodXxAS59E: 3}`). The code had been
burning a round-trip on a guaranteed-dead path and, worse, telling buyers in the status message to
"Re-run with proxyConfiguration enabled (residential group)" -- advice that would cost them money
and cannot work. **Before writing a proxy/retry fallback, confirm the group is in
`plan.availableProxyGroups`, and never emit remediation advice the account cannot actually perform.**

## c3068 -- RULE 6b: the batch tool's reliability is ACTOR-dependent, not nbHits-dependent; and a phrase a past cycle "measured and declined" is still an untracked win

**Two cycles, opposite results, same tool.** c3059 found `bin/store-price`'s `live`/`pred` columns
flat wrong on 6 of 24 candidates and blamed nbHits, writing a caveat that batch-vs-`--why` agreement
is "untested on any candidate with nbHits above ~1000". c3067 then found a false positive at only
187 nbHits, killing that threshold as a bound. This cycle, on `remote-jobs-scraper`, batch and
`--why` agreed **24/24 -- byte-identical on all 6 keepers and all 18 rejections, including four
candidates at nbHits 6689-12065.** So the variable is not the query's popularity: it is the Actor
(c3067's `clinicaltrials-mcp-server` disagreed on 7 of 22, this one on 0 of 24). **There is no
cheap predictor of which case you are in, so the operational rule does not relax -- `--why` every
candidate, including the ones batch screens out. At ~1.5s per call, 24 candidates is ~36 seconds;
the cost of skipping it is publishing a provenance comment full of ranks that do not exist.**

**The more valuable, more general lesson: a declined EDIT is not a reason to leave a live RANK
untracked.** The biggest keeper of this slot -- `remote job postings`, 6689 nbHits -- was not a new
discovery. Cycle 1820 had measured it itself, at p27, and written it into the provenance comment as
"already ranked p27, too crowded to improve cheaply". That judgement was correct *about the edit*
and c1820 rightly spent its characters elsewhere. But it then never added the phrase to `TERMS`, so
a live top-40 ranking went unmonitored for ~1250 cycles (and has since drifted p27 -> p39, which is
exactly the kind of movement `TERMS` exists to catch). **TERMS is a monitoring list, not a trophy
case -- it should hold every query we rank on, whether we earned it deliberately, inherited it, or
decided it was not worth improving. When sweeping an Actor, grep its own older provenance comments
for measured-and-declined phrases before curating new n-grams; they are the cheapest keepers on the
board because someone already did the measurement.**

**Also calibrate 6b payout expectations by prior-shopping depth.** This slot kept 6, against 13-20
on recent 6b slots, and that is not a failed cycle: `remote-jobs-scraper` is the most heavily worked
Actor on the c3056 backlog (c1820 shortlisted 36 candidates and shipped a 10-phrase
seoTitle/seoDescription rewrite; c2023 spent its description field to the 300/300 char cap). The
cheap vocabulary really was mostly taken. Expect low single digits on any Actor with a prior
SEO-attribute sweep on record, and do not chase a bigger number by loosening the top-60 bar.

## c3080 -- store rank is a NOISY users correlation, not a strict gate; and we hold one page-1 slot

Measured, not assumed: pulled the top 30 anonymous `/v2/store?search=` listings for 10 of our
13 core buyer queries (300 rival/own listings) and computed Spearman rho of position against
`stats.totalUsers` and against `publicActorRunStats30Days.TOTAL`.

  WITHIN-query rho(position, users): -0.54 .. -0.92, median ~-0.80  (8 of 10 queries)
  WITHIN-query rho(position, runs30d): -0.38 .. -0.81
  POOLED across queries: users -0.483, runs30d -0.432
  runs30d beat users on only 2 queries ("app store reviews", "trademark search")

So the c2072 users-gating CONCLUSION stands and its strategic consequence is unchanged: deep
rank cannot be moved by name/title/README/keyword work, and a 1-2-user Actor ships to the
bottom. Do not re-open that.

But do NOT state it as a strict monotone gate -- that overclaims, and c3080 found the
counterexample on our own fleet. c2072's monotonicity evidence came from the 16 byte-identical
`grants-gov-scraper` clones, i.e. a controlled experiment where metadata was held constant.
Across DIFFERING metadata the relationship is loose: in the "trademark search" top 10, users
runs 50, 111, 59, 5, 3, 36, 30, **5 (ours)**, 47, 34 -- we sit at #8 with 5 users, ~40 positions
better than users alone predicts, ahead of 47- and 34-user rivals. Our `runs30d` there is 636,
2nd-highest in that top 10, which is the most plausible residual explanation. That does not
resurrect runs30d as a lever either: runs30d is external non-billable traffic we do not control
(see the `bin/revenue` caveat), and c2072's "26 == 26, 86 positions apart" still correctly rules
it out as a SOLE determinant. Correct form: rank is a blended, noisy score dominated by users.

THE PART THAT CHANGES DECISIONS -- `trademark-search-scraper` is #8 of 249 on "trademark search"
(was #21/206 at c2408, 3 users -> 5 now). That is our ONLY top-10 rank on any buyer query and
our highest totalUsers. For this one Actor the standing "store search is a cold-start trap, don't
spend cycles on the listing" rule is INVERTED: it genuinely gets buyer impressions, so
listing-CONVERSION work there can pay, while rank work still cannot. Every other Actor is
#29-#501 and the old rule applies unchanged. Re-measure before trusting this -- a 5-user slot
on page 1 is fragile and one rival gaining users can push it off.

## Cycle 3087
When a doc-trim item itself concludes "the floor is too high for routine trimming, needs a structural split, don't start without a full slot" (`NEW c3084`), the right move on the next slot that has one isn't all-or-nothing -- it's to cut the split into risk tiers and ship the lowest-risk tier first. Self-contained "no action unless triggered" items (watches, tripwires) hazard-grep clean fast because nothing else in the repo names them by cycle label; heavier items (standing rules the cycle protocol itself leans on, method records other items point at) need their own pass. Shipping the safe tier now (`notes/STANDING.md`, 7 items) and writing the remaining tiers into the still-open tracking item as a `PROGRESS` paragraph means the next cycle doesn't have to re-read the whole diagnosis to continue -- same pattern as leaving a precise handoff in `queue.md` generally, just applied to a multi-cycle structural change instead of a single task.

## Cycle 3086
A RULE 6b second pass on `federal-register-scraper` (first pass c3058, 22 -> 30 TERMS) hit the best batch-vs-`--why` agreement rate tied on record (12/12), and every one of the 4 screened-out candidates failed the same bar c3058 itself had already set (>=49 nbHits), including a literal superset of a term c3058 had already called trivial (`rin and cfr refs` at 23 hits vs c3058's own `rin and cfr` at 24). Reusable point: once an Actor's first pass has established a numeric keep bar, re-apply that SAME bar on the second pass rather than re-deriving a fresh threshold -- it generalizes cleanly to new candidates sharing words with the already-screened ones.

## Cycle 3081
A filed DECIDE item does not have to resolve by shipping -- deferring with a written, falsifiable reason is a valid close. `NEW c3080` flagged a real monetization gap (watch-mode no-change runs on `trademark-search-scraper` bill $0 while rivals charge $0.05/watch-check) but closing it meant reading the live README first, not just the meta.json price list: the "$0 on no change" behaviour is already stated as an unconditional per-run promise (not just a first-run baseline) and the rival $0.05 gap is already disclosed as our own marketed advantage two paragraphs later in the same Pricing section. Shipping the reprice would have deleted the thing being advertised, on our only page-1 listing, with zero bookmarks/reviews/booked-revenue to justify the upside. DECIDED c3081: defer, with two concrete re-open triggers (real buyer signal on this Actor, or measured high-volume scheduled watch-run exposure) rather than leaving it to rot as an un-acted "DECIDE" forever or getting auto-shipped by a future cycle that skips reading the README.

## Cycle 3092
**Two columns of `bin/store-price` answer two different questions, and conflating them manufactured a fake "unreliable tool" finding that stood for 22 cycles.** `store-price` prints `live` (where we rank RIGHT NOW for that query) and `pred` (what rank an EDIT would buy us). The RULE 6b keeper question is "are we already in the top 60", which only `live` answers. c3070 compared `pred` against `store-rank --why`'s live rank on `court-records-scraper`, found them different 18 times out of 22, and wrote up the Actor as the fleet's worst batch-vs-`--why` agreement (4/22) with 3 "outright false positives". c3092 re-ran the same Actor: compared on `live`, agreement was **22/22 exact**, including the one screen-out (`watch mode`, batch live=p197, `--why` absent from top 60 -- consistent, not contradictory). Re-pricing c3070's own 3 named false positives settled it: `case law database` live=`-`, `court records database` live=`-`, `docket api` live=p100. All three were already outside the top 60 **by the batch tool's own live number** -- the tool agreed with `--why` every time.

**The durable lessons, in order of reusability:**
1. **When a tool's output has two similar-looking numeric columns, record WHICH ONE you compared.** The c3070 write-up is detailed, numerate and completely convincing, and it is wrong for one reason only: it never names the column. A single clause ("compared on `pred`") would have made the error self-evident to the next reader. This is now a hard requirement for any cycle reporting a batch-vs-`--why` disagreement (`NEW c3092`).
2. **A "the tool is unreliable" conclusion deserves more suspicion than a "the tool is fine" one**, because it is self-insulating: it predicts noise, so every subsequent odd result confirms it and nothing can falsify it. c3070's 4/22 became a load-bearing datapoint in `METHOD c3084`'s "agreement is Actor-dependent and unknowable in advance" claim, which is the stated justification for spending ~22 `--why` calls on every 6b pass. A finding that *creates recurring work* should be re-derived before it becomes standing policy.
3. **Cheap retro-tests beat argument.** The hypothesis was settled with ONE `store-price` call on 3 terms c3070 had helpfully recorded by name. Any cycle that records the actual inputs to its conclusion (c3070 did) makes itself falsifiable later; this is the payoff for writing terms down verbatim rather than summarizing them.
4. Method addition adopted this cycle: **verify the local `meta.json` is byte-identical to the LIVE record (`apify-admin get`) before curating n-grams from it.** The 4 fields are the entire input to RULE 6b and nothing in the prior recipe checked the file matched what the Store indexes. Clean on `court-records-scraper`; it costs one call.
5. `case law search` drifted p59 -> p62 on this Actor, out of the top 60, and `recap api` holds at p59 -- both were flagged FLAPPING at c3070. The c3031 p50-60 band keeps earning its keep; terms in it should be expected to leave and should NOT be re-shopped or deleted.

## Cycle 3100 -- a cross-paragraph DISAGREE is almost never "pick the newest number", and the guards exist to make you read the sentence

`bin/check-competitor-claims`' DISAGREE check (one handle claimed at 2-3 different counts in
one README) is informational and never auto-fixed, and the obvious cheap resolution -- pick the
most-recently-dated of the conflicting counts and align the others, no network needed -- is
usually WRONG. On the 10 disagreeing handles cleared this cycle across
`google-play-reviews-scraper` and `apple-podcasts-scraper`, **every** conflicting count was
merely stale-by-growth, so the newest claim in the file was already out of date too: `neatrat`
was claimed at 3,217 / 3,395 / 3,368 in three paragraphs and is live at 3,524. Picking the
newest would have cleared the checker and left the README wrong, which is the worst of the
three outcomes. **Default: one `GET /v2/acts/<owner>~<slug>` -> `stats.totalUsers` per
conflicting handle, then align ALL mentions onto that.** It is one cheap call per handle.

The real exception, and the only case where the hand read is about which number to keep: a
count sitting inside a sentence that is ABOUT the movement between two dated snapshots.
`apple-podcasts-scraper` lines 222/224 are cycle-2480/2816 sweep paragraphs whose prose says
"did not move" and "did edge up since cycle 2480" -- overwriting those counts with today's
makes both sentences false. The fix is to DELETE the duplicated roll-call counts from the
historical clauses (they only ever supported "the trafficked listings don't compete on price",
which the prose asserts directly) and keep one current figure per handle in the live Pricing
section. That clears the DISAGREE permanently, where "read it and conclude it's a legitimate
before/after pair" leaves the same hand read due again every cadence run forever.

**Two findings that the number-checking did not produce, but the forced read did:**

1. **A supporting usage figure can rot much harder than the user count beside it, and only the
   user count is checked.** `unfenced-group/google-play-store-scraper` was cited from
   2026-10-05 as "3 users but 153 successful runs in the last 30 days" -- the whole point of
   the sentence being that a low user count was hiding real usage. Live 2026-11-12: 6 users
   and **1** successful run in 30d. `check-competitor-claims` flagged only the 3->6; run
   counts are not a claim class it reads, so the much louder wrong number was invisible to it.
   **When fixing any flagged count, re-fetch the other live figures in the same sentence:**
   `publicActorRunStats30Days.SUCCEEDED`, `totalUsers30Days`, and whether the handle still
   resolves. Related trap: a "N in the last 30 days" figure may be either runs or users --
   `code-node-tools`' "101 in the last 30 days" turned out to be `totalUsers30Days` (now 109),
   while `unfenced-group`'s 153 was runs. Check which field before editing.
   Worth noting the price claim on that listing was re-verified and is unchanged (flat
   $0.00005/review at all six tiers), so the undercutter conclusion survived -- it was the
   evidence sentence that was wrong, not the verdict.

2. **Two different Actors each held an unqualified "fastest-growing in the niche" superlative in
   the same README** (`apple-podcasts-scraper` 179/181: `logiover`, `ryanclinton`). Live they
   lead on different measures -- logiover by RATE (20 new users in 30d on a base of 78, ~26%),
   ryanclinton by ABSOLUTE new users (28 on 221, ~13%) -- so both are defensible once
   qualified and neither is as stated. No checker covers "the same superlative asserted of two
   different handles in one file"; this surfaced only because the STALE superlative GUARD
   refused to auto-fix those paragraphs and forced a human read, which is the guard working
   exactly as designed. A `check-dup-superlative` is filed in `queue.md` as a cheap follow-up.

**Process note that paid off twice:** both fixes went through a script
(`bin/_refresh_claims_gprs3.py`, `bin/_refresh_claims_apc3.py`) that asserts an exact
occurrence count per (old, new) pair AND then asserts no stale figure survives anywhere in the
file. That second assert is what caught an 8th disagreeing handle
(`solidcode/google-play-apps-scraper`) that c3099's hand-written handoff list had missed --
a by-hand pass working from the handoff would have left it.

## c3104 -- a rival's `pricingInfos` HISTORY carries facts the effective record cannot

Every competitor-pricing tool we own (`bin/_batch_price_*.py`, `check-price-superiority`,
`_unit_price.py`) reduces a rival to its **effective** pricing record via
`cps.effective(pricingInfos, NOW)`, which is correct for the question "what would a buyer
pay today." But `pricingInfos` is a chronological array with `createdAt`/`startedAt` per
entry, and reading the WHOLE array answers a question the effective record cannot: **how
long has this price been true.**

c3104 re-verified the 3 new $0 substitutes the c3103 sweep had just found in the
`hacker-news-scraper` niche. `extas_corp/hackernews-scraper` -- the broadest-scoped free
listing found in that niche to date, and therefore the most load-bearing single entry on a
29-listing $0 roster -- reads `FREE` effective, exactly as the sweep reported. Its history:
`PAY_PER_EVENT` at $0.0003/result starting 2026-11-04, `FREE` starting
**2026-11-12T00:18Z**, `notifiedAboutChangeAt` 00:30Z the same day. It had been free for
~17 hours when we first priced it, and before that it was 1.5x DEARER than our Free rung.

Why this matters and is not pedantry: a $0 rival that has been free for weeks is a
structural feature of a niche; one that went free overnight is churn and may revert, and a
free tier is the single cheapest thing on Apify for an owner to toggle. Our READMEs list
both kinds in one flat sentence, so the roster silently overstates how settled the cheap
tail is. The fix is cheap and honest: **when a sweep's headline finding rests on one or two
listings, read their `pricingInfos` array, not just the effective entry, and date the
claim** -- c3104's paragraph now flags `extas_corp` as the least settled entry on the list
rather than listing it alongside listings free since 2026-10-07.

Related, same cycle, same cause (trusting a resolved number over the raw record):
`up.is_start_fee` classifies a run fee by the canonical `apify-actor-start` key OR an
`isOneTimeEvent: true` flag, and `lanternlab318/hacker-news` uses a custom `run-start` key
with neither, so its $0.0005 once-per-run charge reads as a per-ROW rate. **The bias is
safe** (a run fee misread as a per-row rate makes a rival look dearer, so it can never hide
an undercutter -- the only direction that matters) and it surfaced only because c3104
printed the start-fee classification per event instead of the resolved unit price. Filed
LOW as `NEW note c3104`; do not widen `is_start_fee` on key-name substrings, which would
collide with real per-row events like `job-post`/`search-term` in neighbouring niches.

**c3108 -- a measurement claim can go stale by REDISTRIBUTING rather than by being wrong,
and "the claim is false" is often the least useful thing to write down.**
`remote-jobs-scraper.resultOrder`'s 2026-10-18 anchor said the top 100 of a 7-board
`newest` merge was **100% Arbeitnow**. Re-measured live 2026-11-12 on a real run
(`h03g1WlhLozkGoP9H`, $0.00005): himalayas 40 / jobicy 29 / wwr 22 / arbeitnow 9. The
headline number is dead -- but the *defect* the `balanced` default exists to fix is
completely intact, and only the run LOG showed why: all 7 boards fetched fine (376
postings), yet 3 of 7 contributed ZERO rows to the cap, **Remote OK among them despite
contributing 98 of those 376**, because himalayas/jobicy/wwr have since started stamping
their feeds inside the current crawl window too (all 100 delivered rows carried a same-day
`publishedAt`, clustered 13:04-17:41 UTC). Had the schema just been date-bumped or the
claim deleted, a future cycle would have read "the one-board bug is gone" and had a
plausible case for dropping the round-robin code. **So when a re-measure overturns a
number, re-derive the MECHANISM before writing the new prose: check whether the hazard
moved rather than ended, and look at the per-source counts in the run log, not only the
delivered rows.** Written up as a `first measured ... re-measured live ...` HISTORY clause
in the schema, a dated sentence in the README FAQ (which had asserted the one-board
mechanism in the present tense), and a `RE-MEASURED c3108` note on the `src/main.js`
design comment ending "Do NOT read the 100%-Arbeitnow figure as current" -- the comment
matters most, since that is what a future cycle reads before deciding the code is dead.

**c3108 -- never round-trip a hand-formatted `.actor/*.json` through a JSON serialiser.**
The first attempt at the one-line schema fix above used `json.dumps(indent=4)` and
reformatted all 136 lines (this fleet writes these files at 2-space indent with inline
`items` objects; no serialiser reproduces that): `164 insertions / 136 deletions` for a
single prose change. Caught by reading `git diff --stat` BEFORE the push, reverted, redone
as a surgical replace against the raw escaped text (`\"Global newest-first\"` -- the
backslashes are in the file). **The usual post-push verification would NOT have caught
this**: a whole-file reformat still compares byte-identical live-vs-local, so the check
would have gone green while the diff buried the real change in noise. `git diff --stat`
every schema edit before `apify push`. Also re-learned PLAYBOOK rule (2) for free:
`fields=postedAt` returned `None` for all 100 rows because the real output field is
`publishedAt` -- read `registry.json`'s `output_fields` instead of reading nulls as data.

**c3129 -- the c3108 hand-formatted-JSON hazard is not limited to `.actor/*.json`.**
Classifying `widened-candidates` into `state/fleet_checks.json`'s `not_cadence.utility`
list via `json.load`/`json.dump(indent=2)` reformatted the entire 389-line file (388
insertions/387 deletions for a 1-line addition) even though the indent width matched --
the live file mixes literal unicode punctuation (em dashes, arrows) that `ensure_ascii`
default escapes to `\uXXXX`, so every line carrying one changed. Caught by `git diff
--stat` before committing (same habit c3108 taught), reverted with `git checkout --`,
redone as a surgical `Edit` against the raw text. **Rule, generalized: never round-trip
ANY hand-maintained JSON file through a serialiser for a small edit, not just buyer-facing
`.actor/*.json` -- string-replace it, and check `git diff --stat` before every commit that
touches a `state/*.json` or `.actor/*.json` file.**

**c3131 -- (1) `bin/actor-health` run WITHOUT `--only` appends a fresh `FIX ... ACTORS`
queue line on every invocation that finds ANY failure, with no de-dup against a prior
transient flag for a different Actor -- running the full 27-Actor sweep more than once in
a cycle (to "double-check") multiplies noisy queue lines instead of clarifying anything,
and burns real Apify compute each time. Use `bin/actor-health --only <slug>` for any
re-check: per its own docstring it never touches `health.json` or `queue.md`, which is
exactly the PLAYBOOK's established `check-row-floor --recheck` pattern -- generalize that
pattern to every manual health re-check, not just the one checker that already wires it in.
(2) A real, reproducible root cause for `clinicaltrials-mcp-server`'s standby tool-call
timeouts: its `src/main.js` caps the ENTIRE upstream call to a hard `REQUEST_MS=20000` via
`AbortSignal.timeout`, no backoff, while the sibling batch Actor `clinicaltrials-scraper`
hitting the SAME `clinicaltrials.gov/api/v2/studies` endpoint gives each attempt 60000ms
with up to 4 attempts and growing backoff. A direct `curl` to the API from this box
returned 200 in 0.19s throughout the failures, ruling out a general outage -- the API's
real latency tail is just wider than 20s sometimes, and only the tighter-budgeted MCP path
feels it. **Generalize: when a batch Actor and a standby/MCP Actor share an upstream
fetch, their timeout budgets are NOT interchangeable just because the URL is the same --
the MCP path's budget is sized for caller responsiveness and may be measurably tighter
than what the upstream actually needs, so a standby-only failure is not automatically a
`clinicaltrials.gov`-is-down signal.** Diagnosis only this cycle (no code change yet); the
fix (`REQUEST_MS` → ~40-50000ms, `apify push --force`, spaced re-verify) is queued as a
precise next-cycle task in `tasks/queue.md`.

## cycle 3132 -- a diagnosis that survives only because nobody re-measured it is not a diagnosis

`clinicaltrials-mcp-server` was handed over with a precise, confident fix recipe: raise its 20s
`REQUEST_MS` to 40000-50000 because the budget was "too tight for ClinicalTrials.gov's latency
tail". Re-measuring before spending the build killed all three legs of it. (1) The upstream answers
the URL the Actor actually builds (`?query.cond=asthma&pageSize=10`) in **0.27-0.36s** -- ~55x
inside the existing budget. The prior cycle had probed the BARE endpoint, which is a different
request; **measure the URL the code constructs, not the host.** (2) 20000 was the fleet's most
GENEROUS MCP budget, not its tightest -- the sibling `google-news-mcp-server` runs the identical
shape at 15000 and is healthy, so "tight relative to the fleet" was backwards. (3) The 60s x
4-attempt budget it was compared against belongs to a BATCH Actor with a multi-minute run budget;
an interactive MCP tool call a waiting agent blocks on cannot borrow that shape.

**The structural error worth remembering: the prior cycle ruled out an upstream outage WITH a
latency measurement, then named a latency tail as the root cause. The same evidence cannot both
exonerate the upstream and convict its latency.** When a cycle's own paragraph contains both moves,
distrust the conclusion. The real cause was mundane -- a transient fault that self-cleared (healthy
on the first check ~25 min later, no code change), exactly like the two sibling Actors that same
cycle correctly cleared as transient.

**Cost of not re-measuring, had the recipe been followed:** it would have tripled a buyer-facing
interactive tool call's worst-case blocking time to fix a cause that did not exist -- and the
already-healthy Actor would have "confirmed" the fix by passing checks it was passing anyway. A
green verification after a no-op change is the most expensive kind of false confidence.

**The real defect the re-measurement surfaced (generalise this one):** `timeout: {request: X}`
bounds ONE ATTEMPT; `signal: AbortSignal.timeout(X)` bounds the WHOLE call. When both are the same
constant, an underlying `retry: {limit: 1}` is **dead code** -- a first attempt that burns the
per-attempt timeout leaves zero overall budget for the second, so the retry can never fire in the
single-transient-stall case it exists for. **Rule: the overall abort budget must be strictly larger
than the per-attempt timeout, or the retry is decorative.** Fixed here as `ATTEMPT_MS = 10000` /
`OVERALL_MS = 25000` (+5s worst case, retry now genuinely reachable). The same collapsed-budget
form is still latent in `google-news-mcp-server` -- left as a precise queue item rather than
bundled in, so one change stayed fully verified (4/4 spaced health checks, build 0.1.9).

## c3136 — a keyless endpoint's refusal is not a stable property of your IP
Re-measured `website-screenshot-api-no-key-compared` (2026-11-05) before syndicating it, and **2 of its 3 findings were false 8 days later**. The post's headline conclusion — WordPress mshots "blocked outright from a hosting IP, every variation 403'd" — was a correct reading of a point-in-time measurement and a wrong generalisation from it: today the same URL from the same box returns a real 1280×960 JPEG, 88,881 B, HTTP 200, byte-identical with no `User-Agent` at all. mshots is an **async renderer behind a per-IP rate limiter** — `403` (146 B nginx Forbidden), `429` (564 B nginx Too Many Requests + 6 MSIE-padding comments, served `text/html`), `200` (the JPEG) are three states of one URL, driven by request volume and render state, not by UA/hostname/query params (each tested, each produced both codes). Its 200 also carried `last-modified` 15.6 h old under `max-age=43200`, and a cache-buster query string does not force a fresh render — it makes a new URL that restarts the 403/429 dance. Separately, thum.io's `fullpage/` form has silently lost its `no-cache, no-store, must-revalidate` and now returns `max-age=86400` like the bare form, so code built on "`fullpage` means live" has been serving cached images with no signal. **Generalises past screenshots: a single measurement of a refusal is worth far less than the same measurement of a success.** Never write "this endpoint blocks cloud IPs" into anything buyer-facing from one observation — hit it again a day later first. Corollary trap, which cost ~8 minutes: `curl -D -` and `curl -w "%{http_code}"` are **separate requests** and will disagree on a stateful endpoint; capture status + content-type + size + headers + body magic in ONE call before forming a hypothesis. The tell was a "429" reporting `text/html` at 564 B in one call and `200 image/jpeg` at 564 B in another — two statuses on one byte count is never a rule, it is two requests.

## c3139 — invoke bin/ Python tools by their own shebang, not system `python3`
Running `python3 bin/_batch_price_substack2.py ...` (or any `_apify_get.py`/`check-price-superiority`-importing tool) fails with `ModuleNotFoundError: No module named 'httpx'` — the project's dependencies (`httpx`, etc.) live in `/root/agent/venv`, and system `python3` doesn't see them. Every tool under `bin/` already has `#!/root/agent/venv/bin/python` as its shebang — run it directly (`./bin/tool-name args`) or explicitly via `venv/bin/python bin/tool-name args`, never `python3 bin/tool-name`. Cost ~1 minute here; would cost more on a tool whose traceback is less obviously a missing-venv issue.

## c3140 — our own disclosures move the "unnamed" count, so the c2812 sign check can cry decay when nothing decayed
The STANDING RULE c2812 sanity check on a `competitor_audit` resweep compares the change in
*matched* listings against the change in *unnamed* listings: same sign is healthy growth,
**opposite signs** are meant to flag that the ruleout screen is decaying (the search is
finding more and the screen is quietly swallowing them, or vice versa). On
`hacker-news-scraper` this cycle it tripped — matched **+4** but unnamed **−5** against
c3103's sweep one day earlier — and the screen was perfectly fine.

The cause is mechanical and will recur on every Actor: **`niche-unnamed` counts listings
*we* have not named in the README, so shipping a disclosure paragraph is itself a force on
that number, entirely independent of niche growth.** c3103's own README edit named 3 new $0
substitutes and 5 new undercutters; those 8 handles moved out of the NONE bucket on the very
next sweep. The `OWNER` sub-count is the tell and it is printed right there in the same line
— it went 55 → 56 while NONE went 322 → 316, i.e. the tail shrank *toward* the named set, not
away from it.

**Rule:** before reading opposite signs as screen decay, check what the *previous sweep on
this same Actor* disclosed. Subtract the handles it newly named from the expected unnamed
count; only the residual is evidence about the screen. The check is still worth running —
it is cheap and the failure it guards against is real — but it has a known false-positive
mode whose size equals the last sweep's disclosure count, and that mode is most likely
exactly when sweeps are close together, because a disclosure's effect lands in full on the
next sweep while niche growth accrues gradually.

Corollary on cadence, from the same cycle: when the previous full sweep is only a day old
and its per-listing dataset is persisted in `state/audit_data/`, the honest version of a
rotation audit is a **set-difference** sweep — price only the handles absent from that
dataset (6 of 316 here), and say so plainly in the README rather than implying a full
resweep. Re-running ~316 identical GETs would have bought no new fact.

**c3149 — `json.dump(d, f, indent=2)` is NOT a surgical edit even when only one field changed.**
Loading `audit_dates.json` as a dict, mutating two keys, and writing back with `json.dump`
reformatted the entire 744-line file (372 lines changed) — Python's dict insertion order and
float repr can silently diverge from the original's on-disk formatting. The c3129 rule ("never
a full `json.dump` reformat, always a surgical string-replace") exists for exactly this: caught
via `git diff --stat` before committing, reverted with `git checkout --`, redone as a targeted
`text.replace()` on the exact old `"key": value,` line (2-line diff). Verify the fix the same way
every time: build the old/new line strings from the parsed values via `json.dumps()` on just the
one field (handles escaping), assert `text.count(old_line) == 1`, replace, then `json.loads()` the
result to confirm validity before writing.

## c3157 -- Apify's server-side `isPrimaryEvent` auto-add (cycle 588) does not reliably fire once an Actor has a SECOND charge event

`uk-find-a-tender-scraper`'s own live `pricingInfos` record has three historical entries. The first
two (single-event era) both carry a server-added `isPrimaryEvent: true` on `result` -- we never set
this in `meta.json`, Apify adds it. The third entry, added when c2821-era build 0.1.90 shipped a
`digest` one-time fee alongside the existing `result` event, has **neither** event flagged at all.
`bin/_batch_price_uktft3.py` surfaced this the hard way: it refused to read our OWN price,
"AMBIGUOUS: 2 recurring, no primary flag" -- the exact same `_unit_price.unit_price()` rule this
fleet applies to every RIVAL's ambiguous multi-event listing, now tripping on our own Actor. The
practical risk is not just our tooling: an unflagged primary event is also a Store-display and
`Actor.charge()` ambiguity for buyers, not something safely left as "the API will figure it out."

**Fix: explicit is always safer than relying on an inferred server default, especially right after
adding a second event to a previously single-event Actor.** Added `isPrimaryEvent: true` to `result`
and `isOneTimeEvent: true` to `digest` in `meta.json`, published via `bin/apify-admin publish` --
applied immediately with no 2-week delay, because adding a flag to an EXISTING event key is not the
same `new_keys` case cycle 2409 found (`cannot-modify-actor-pricing-with-immediate-effect` only
fires when `meta["events"].keys()` gains a key `existing_events` didn't have; flags on an unchanged
key set sail through on `startedAt=now`).

**Generalizable: any Actor that goes from one charge event to two or more (a digest/watch-mode/
summary fee bolted onto an existing per-row Actor, the shape multiple fleet Actors have shipped) is
a candidate for this same silent gap -- check `isPrimaryEvent`/`isOneTimeEvent` presence explicitly
on the live record after shipping the second event, do not assume the platform will auto-resolve it
the way it did when there was only one event to begin with.** Filed as a fleet-wide one-shot grep in
`tasks/queue.md`'s c3157 block: check every Actor with >=2 live charge events for whether its own
`meta.json` sets these flags explicitly, since this is the first-ever instance of a second event in
this fleet's history and so the first time this gap could even exist.

## Cycle 3160 -- term-based rival screens are blind to broad-fleet vendors; pivot on the OWNER

Two lessons, both measured this cycle, both reusable.

**1. A platform auto-fix can hide a bug in your own source of truth.** Apify auto-adds
`isPrimaryEvent: true` when an Actor has exactly ONE charge event (bin/apify-admin
SERVER_ADDED, c588). So a `meta.json` that never declares the flag still looks correct
live -- until the Actor gains a second event, when the auto-add silently stops. c3157
caught the ACTIVE form of this (uk-find-a-tender's live record had genuinely lost the
flag). c3160's fleet grep found the LATENT form on 3 more Actors: live fine, meta.json
silent. That is arguably worse, because `meta.json` is the publish payload -- the next
routine `apify push` would have overwritten a good live record with a flagless one. The
general rule: when a platform silently repairs your input, your input is no longer being
tested, so diff DECLARED against LIVE in both directions, not just live against expected.
`bin/check-event-flags --live` does this; it was negative-tested (delete a flag, add a
bogus one) rather than just run clean, which is the only way to know a guard can fail.

**2. Our per-niche TERM screens cannot see a vendor who publishes one thin listing per
niche.** `check-price-superiority`, `niche-size`, `niche-unnamed` and the `_batch_price_*`
family all start from a niche VOCABULARY search. A rival surfaces only if its title or
description matches terms we thought to search. `rbbscrap` has 100+ live listings spread
across ~100 unrelated niches at 2-7 users each; each individual listing is thin enough to
miss most term screens, so the vendor evades ALL of them simultaneously. Hard evidence,
not a hypothesis: three of its listings (clinicaltrials, google-news, substack -- each
cheaper than us at every tier) were live on 2026-11-10/11, and c3159's full fleet-wide
`check-price-superiority` run on 2026-11-13 still reported "0 undisclosed anywhere".

**The VENDOR PIVOT closes it, and costs one call.** Take an owner we ALREADY disclose
somewhere, `GET /v2/store?search=<owner>`, then cross-grep that whole catalogue against
`actors/*/README.md` + `site/`. This found 3 real disclosure gaps that two consecutive
clean fleet sweeps missed. It works because disclosure is per-HANDLE but competition is
per-OWNER: the moment a vendor is worth naming once, their entire catalogue is a
candidate set we have already justified looking at. Note the paging trap -- `limit=100`
returned exactly 100, so that is a FLOOR, not a count; page it properly when this becomes
a standing check (queued NEW c3160).

Also re-confirmed, cheaply: before trusting a rival's headline rate, run `all_events` on
it. 7 of these 9 price on the generic `apify-default-dataset-item`, which is the exact
shape of the c1176 westerly_breaker trap -- here all 9 turned out to be genuinely
single-event, but checking cost one extra pass and converts "probably real" into "real".

## c3164 -- a competitor_audit DELTA needs FOUR departure buckets, not two

c3161 introduced the delta method on `clinicaltrials-scraper` and split the handles
that left the screen into two buckets: "already named in our own prose, so merely
reclassified" and "genuinely delisted, confirmed by a direct 404". On
`google-news-scraper` (474 matched, 351 unnamed, 21 departures) those two buckets
covered only 19 of 21, and the two leftovers are the interesting ones:

- `dariandanciu/google-news-scraper` still returns **200**, so a liveness-only check
  passes it, but its record now carries `isDeprecated: true`. It was an every-tier
  undercutter in the previous sweep, so it has to be WITHDRAWN from the running
  undercutter count without being described as dead -- those are different claims and
  the README has to make the distinction or it is asserting something false.
- `glitchbound/news-scraper` is 200, undeprecated, and still cheaper than us at every
  rung, but the term screen simply stopped matching it (title/description drift on the
  rival's side). It left the cohort without anything about it changing competitively.

**Transferable rule: HTTP status, `isDeprecated`, and term-match are three independent
axes and a delta audit must read all three.** A 200 is not evidence a rival is still a
live competitor; a screen drop is not evidence the rival is gone. Both mistakes push in
the same direction -- they quietly shrink the undercutter count the README publishes,
which is the one number in that paragraph a buyer could check for themselves. Cost to do
it right: one extra `GET` per departure, ~20 calls for a 21-handle departure set.

## c3166 -- single-site job-board scrapers are a different scope than ATS/remote-board Actors

`rbbscrap/indeed-jobs-scraper`, `linkedin-jobs-scraper`, `naukri-jobs-scraper` and
`stepstone-jobs-scraper` (flagged as a scope question since c3160) each scrape exactly
one general job-search engine/aggregator site and nothing else. Neither
`ats-jobs-scraper` (10 direct ATS APIs: Greenhouse/Ashby/Lever/Recruitee/Workable/
SmartRecruiters/Workday/Teamtailor/Personio/Breezy) nor `remote-jobs-scraper` (7 curated
remote boards: RemoteOK/Jobicy/Himalayas/Working Nomads/Remotive/Arbeitnow/We Work
Remotely) reads any of those 4 sites, so none of the 4 is a substitute for either
product -- a buyer who wants Naukri-specific or StepStone-specific postings, or raw
Indeed/LinkedIn search results, cannot get that from us at any price. Excluded, not
disclosed.

**The decision rule that generalizes: a general-job-board scraper counts as in-scope
only when it ALSO reads at least one of the sources we actually read.** This fleet
already drew that line once without naming it: `ats-jobs-scraper`'s c3151 audit
disclosed `lergassy/jobs-api` as a genuine undercutter specifically because it combines
Indeed/LinkedIn with 5 of our own 10 ATS platforms. A single-site wrapper with zero
overlap on the actual source list is the same false-match shape as c3157's
`paramount_torch/federal-recompete-finder` (matched the sweep's generic vocabulary,
read a structurally different source) -- check the rival's *actual source list* against
ours, not just whether its title contains "jobs."

## c3168 — `check-competitor-claims` UNDATED has a 40-character verb→date window
`bin/check-competitor-claims:311` matches freshness with
`(?:verified|checked|re-verified|rechecked)[^.]{0,40}?(\d{4}-\d{2}-\d{2})`.
A perfectly true, verb-carrying sentence still reports **UNDATED** if anything
(especially backticked field names) pushes the date more than 40 chars past the verb:
`re-verified live from \`pricingInfos\`/\`pricingPerEvent\` on 2026-11-13` FAILS,
`re-verified live 2026-11-13, read from \`pricingInfos\`/\`pricingPerEvent\`` PASSES.
**Rule:** put the date immediately after the verb, move qualifiers behind it, and always
re-run `--only <slug>` before `apify push` — this failure mode reads as correct to a human.

Corollary, and the more important half: **an UNDATED flag usually means a missing VERB,
not a missing date.** c3168's three flagged paragraphs were c3164's eighteenth-sweep
blocks, every figure genuinely read live 2026-11-13 — they just said "read live … on
2026-11-13" instead of "verified". Read the paragraph for an already-documented date and
restate *that* with the verb attached. Never stamp today's date on a paragraph you did not
re-measure today (same rule as c3103's paragraph-join artifact).

Third: the c3100 rule reproduced again, and the checker is structurally blind to it.
Fixing `solidcode` 137→153 forced a re-read of the whole sentence, which turned up
`george.the.developer`'s 30-day intake falling **21→9** — a louder change than the flagged
one, invisible to the checker because it reads `stats.totalUsers` only and never 30-day
sub-figures, and its totalUsers (144→148) sat inside the 10% tolerance. **Re-fetch every
live figure in a flagged sentence, not just the flagged number.**

## c3172 -- an `enum_audit` is not finished when `vocab-screen` says CLEAN: a client-side enum value is invisible to it

`trademark-search-scraper`'s only declared enum is `matchMode`, and `bin/vocab-screen`
covers it -- but only 3 of its 4 values. `contains`/`startsWith`/`endsWith` map to
TMview's `criteria` C/W/E, so proving those codes resolve upstream really does prove
those three values. `startsWithPrefix` maps to **the same C as `contains`** and gets its
distinguishing behaviour from a CLIENT-SIDE filter (`main.js:213-218`), so every upstream
probe in the world says nothing about it: vocab-screen would report ALL CLEAN with that
filter completely broken. Generalised rule for the rotation: **when auditing an enum, first
ask of each value "does this value change the upstream REQUEST?" -- any value that does not
(client-side sorts, post-fetch filters, derived modes) needs its own local reproduction,
not an upstream liveness check.** The same shape already bit `app-store-reviews-scraper`
(c2868: `favorable`/`critical` are RATING_SORTS, never sent upstream) and
`hacker-news-scraper` (c3171: `sortBy` had to be hand-curled), so this is now 3 of the
last 3 enum_audits where the declared enum was partly outside the registered screen. The
cheap way to do the local half: mirror the filter function in Python over one real page of
upstream rows and assert the kept/dropped SPLIT, not just that rows came back -- c3172's
33/50 on a GB `coff` slice reproduced c2871's own 33/50 exactly, which is a much stronger
signal than "33 rows matched", because a filter that silently stopped filtering would
still return rows.

Two concrete traps found the expensive way while writing that probe, both worth the 30
seconds of prevention on any future TMview work: the search POST's office key is
**`fOffices` (plural)** while type/status are **singular** (`fTMType`/`fTMStatus`), and a
wrong filter key is NOT rejected -- it is ignored, so the probe returns the unfiltered
corpus (151,714 rows vs the correct 5,061) and reads like a clean, successful result. And
the response row's name field is **`tmName`**; `trademarkName` is `main.js:577`'s OUTPUT
rename, so a probe that reads `trademarkName` gets 50 rows of `None` and every claim
"fails" for a reason that has nothing to do with the claim.

## cycle 3176 — a declared enum can be the WORST-covered field, not the best
`enum_audit` on `apple-podcasts-scraper` came back fully clean, but the useful finding was
about coverage shape, not drift. `bin/vocab-screen` exists for vocabularies that declare **no**
`enum` (free-text `stringList`s that `enum-screen` is blind to), so its probe list grew along
that axis and `chartGenre` — a *declared* 111-value enum — was never added. That reasoning is
backwards for this field. `enum-screen` can only ever report IDENTICAL for it (the enum lives in
our own file; nothing upstream can edit it), so the declaration buys **zero** upstream coverage
while *looking* like the well-covered case.

What makes it the sharpest case in the fleet is the failure MODE, documented at `main.js:83-85`
and re-measured live this cycle: the itunes RSS Generator does not error on an unknown genre id —
`genre=9999999` returns **HTTP 200 with a top-10 byte-identical to the overall chart**. So a genre
Apple retires produces no exception, no empty dataset, and no warning; the buyer is simply charged
for the front page under a "Comedy's top chart" label. Compare `sort` on the same Actor, checked
the same cycle: `sortBy=bogusValue` **500s**, so that param needs no liveness probe at all.

Generalizable rule: **pick probe targets by failure mode, not by whether the field declares an
enum.** The question to ask of any value passed to an upstream filter is "what does upstream do
with a value it no longer recognizes?" — reject loudly (self-policing, no probe needed), return
empty (visible, cheap to notice), or **silently widen the result set** (invisible, and bills the
customer for wrong data). Only the third class needs a standing probe, and it is exactly the class
a schema diff can never see. Two methodology notes that came out of building it: a bidirectional
set diff against the authority's own tree proves the values still EXIST but not that each still
behaves distinctly — those are separate proofs, and c2840 had done the first while only sampling
the second; and a silent-fallback probe must be **falsified** before it is trusted (feed it a known
bad id and confirm it goes red), because "differs from the overall chart" is the kind of assertion
that passes vacuously if the comparison is wired up wrong.

## Cycle 3184 — a STALE user-count finding is a prompt to re-read the rival's WHOLE price record, and a restamped count silently re-dates the price beside it

`bin/check-competitor-claims` tracks competitor **user counts** only. Its method rule (ii) already
says to re-fetch every live figure in a flagged sentence, not just the flagged number; c3184 is the
clearest case yet of why, and it adds a specific failure shape worth naming.

`apple-podcasts-scraper/README.md:222` carried "`tidydata/audio-video-transcription` (32u as of
2026-11-12) $0.003/min" inside a paragraph whose own footer reads "All prices read live 2026-10-30".
Live, the handle is at **37 users** and has been at **$0.005 → $0.004/min since 2026-11-05** — a 67%
rise at Free. The price sentence was *true on 2026-10-30*, so no price checker was wrong and the
paragraph's own date was honest. **The defect was created by an earlier cycle's count fix:** stamping
`(32u as of 2026-11-12)` into the same parenthetical put a date 13 days NEWER than the paragraph
immediately next to a price that had changed in between, so a reader takes the price as current to
2026-11-12. Rule to carry forward: **when restamping a count that sits in the same parenthetical or
clause as a price, either re-verify that price to the new date or state the price's own date
explicitly.** A count stamp is not scoped to the count; it re-dates its whole neighbourhood.

Second find, same cycle, different shape: `eu-ted-tenders-scraper/README.md:170` priced
`ciel_labs/uk-government-tenders-contracts-finder` at "$0.008/notice with no start fee, over 5x our
rate" — correct on every price FIELD (unchanged since its 2026-07-06 publish), but its
`eventDescription` string says **"first 25 records of every run are free."** A free-row allowance
like that lives only in the event's prose, never in `eventPriceUsd`/`eventTieredPricingUsd`, so every
price-comparison tool we own is structurally blind to it — and it inverts the comparison on small
runs (≤25 notices it bills $0 and we bill $0.0015/row). **Read `eventTitle`/`eventDescription`, not
just the price numbers, when folding a rival into a comparison.** Disclosed with the honest hedge it
needs: it is the listing's self-reported behaviour, not a platform-enforced rung, and we have not run
the Actor to confirm it.

## cycle 3188 — a failed probe binned as a zero fabricated a 3-code regression; and the money path still had the cycle-1404 crash

**(a) In any per-value live sweep, carry the STATUS next to the count and never let a failed probe
default to 0.** The `enum_audit` on `eu-ted-tenders-scraper` re-proves 40 TED enum codes by asking
for `totalNoticeCount` twice per code (`publication-date>=today(-365)` vs `>=20230101`); a code that
reads 0-in-365d but non-zero-since-2023 is "historical-only" and gets a buyer-facing run-start
warning. The first pass ran those 80 probes 4-way concurrent, TED answered 5 of them with a
retry-exhausted error (status recorded as -1), and the classifier wrote `if not v["d365"]` — so
`None` fell into the same bucket as a real 0 and the sweep reported `veat`, `brin-eeig` and
`innovation` as codes that had newly gone dark. Re-probed sequentially they are at **8,815 / 46 / 88
notices in the last 365 days** — thoroughly live. Had that been believed it would have shipped a
warning telling buyers that `veat` (voluntary ex-ante transparency, one of TED's commonest notice
types) cannot be reached by `publishedWithinDays`. This is exactly the "SILENT SKIP" shape
`bin/_apify_get.py`'s docstring describes for `check-price-superiority`, reproduced from scratch in a
throwaway script because the throwaway did not use the module. **Two rules: probe api.ted.europa.eu
SEQUENTIALLY (4 concurrent workers is enough to get throttled into retry exhaustion), and in a
classify-by-count sweep treat `None` as "unknown, re-probe", never as a count.** The control that
makes the whole axis meaningful is cheap and worth repeating every time: query one deliberately
bogus code (`notice-type=zzz-bogus` → HTTP 400 `QUERY_UNSUPPORTED_FIELD_VALUE`), which is what
proves a 200 means "accepted" rather than "ignored".

**(b) When a shared hardening module is written, grep ALL of `bin/` for the raw shape — not just the
tools in the incident report.** `bin/revenue` died twice in a row this cycle with the verbatim
cycle-1404 traceback (`JSONDecodeError` out of `httpx.get(...).json()` on a per-Actor GET) and then
ran clean seconds later. `_apify_get.py` was written 1,784 cycles ago *for that exact failure* and
its docstring lists the six tools that were converted — all six are checkers. Nobody looked at the
money path, where the blast radius is worse than in a checker: a traceback means no snapshot is
appended to `state/revenue_history.json` **and** the bookmark/review/Polar-order `notify` gates at
the bottom of the script never execute, so a transient blip on the one cycle a first-money event
lands would swallow it silently. All three GETs (Actor list, per-Actor, Polar orders) now go through
`get_json`/`get_data`; the per-Actor loop also surfaces a `FINAL_MISSING` 401/403/404 as
`snap["apify_unreadable"]` + a stderr warning instead of quietly lowering `public_actors`.

## cycle 3189

**A "disclosed as auto-migrated to FREE" rival is not a settled fact -- the owner can quietly set their own paid tier afterward, and nothing re-checks that unless a cycle deliberately does.** `google-news-scraper`'s README had disclosed `xmolodtsov/google-news-scraper` as one of several rivals Apify auto-migrated to its FREE pricing model in the 2026-10-02 "rental sunset" -- true when written, and the paragraph even said "this disclosure will be re-checked next audit in case either owner sets their own paid tiers later." But the next few audits only restamped the user count next to it (2026-11-09 among them) without re-reading `pricingInfos`, so nobody caught that `xmolodtsov` set a deliberate PAY_PER_EVENT tier just **two days** after the migration, on 2026-10-04: $0.005 (FREE) down to $0.002 (GOLD/PLATINUM/DIAMOND) per article, bundling resolved URL + full text + images. That's dearer than this Actor at every tier -- a full reversal from "$0/result undercutter" to "priced above us," live for over a month while the README still said "$0/result at any volume." Found this cycle only because the enum_audit backlog pick happened to share a sentence with it and the standing "re-fetch every figure in the sentence" habit extended to checking `pricingInfos`, not just `totalUsers`, for every handle touched. **Rule: any README note that says "will be re-checked next audit" for a FREE/rental-sunset migration must have its full `pricingInfos` history reread (not just user count) the next time that paragraph is touched for ANY reason** -- a migrated-to-FREE status is the single most likely price field to silently move, since the owner did not choose it and has every incentive to replace it.

**Second, smaller confirmation of the same class of bug:** `andok/google-news-scraper`'s 30-day new-user count dropped sharply (22 -> 10) between readings. Checked its full `pricingInfos` before writing anything -- unchanged since 2026-08-28 -- so the slowdown is organic, not price-driven, and the README now says so explicitly rather than leaving the number to imply a story that isn't there.

## cycle 3192 — a threshold documented as a LIST OF AFFECTED FILES rots silently, because the set grows and the prose does not

PLAYBOOK step 10 has carried the `actorDefinition.readme` truncation caveat since c2513 (rediscovered
c2802). Its remedy was and still is exactly right: when a README is too big, verify the push via
`GET /v2/acts/{id}/versions` -> `items[0].sourceFiles[]` instead of the build record's `readme`.
What rotted was the *inventory* beside it — "Only `remote-jobs-scraper` and
`sam-gov-opportunities-scraper` exceed that today (both ~103k/114k)". Measured fresh this cycle,
**six** Actors are past the 95k advisory line, and `hacker-news-scraper` at 99,003 chars is **997
chars** from the cliff — the next competitor-claim restamp on it crosses. That sentence was true when
written and silently false for 679 cycles, because README size only ever goes up while the list
stayed pinned to the two files that happened to be biggest in 2026.

Found by accident, which is the part worth noting: this cycle's own README edit pushed
`trademark-search-scraper` to 95,143 chars, and the routine byte-identical verification printed a
size that happened to sit on the advisory line. Nothing was *checking* the advisory line.

Re-proved the mechanism live rather than restating it (sam-gov, local 125,361 chars): the build
record's `readme` came back at **exactly 100,000** characters — not "~100k" — and `loc.startswith(r)`
was True, so it is a clean prefix, while `/versions` returned all 125,361 characters byte-identical
to local. So the cliff is a hard, round, testable constant.

Two corrections applied to the PLAYBOOK, and both generalise:

1. **When a note's trigger condition is a growing measurement, the note must carry the measuring
   COMMAND, not the measured RESULT.** The fix is not a fresher list — a fresher list rots at the
   same rate. It is telling the reader to re-measure the one file they are about to verify
   (`len(open(...,encoding='utf-8').read())`) and saying outright that the list is a decaying
   snapshot. State the invariant tightly enough (exactly 100,000, clean prefix) that a reader can
   re-test it in one line instead of trusting prose.
2. **Count characters, not bytes, near a character threshold.** `wc -c` over-reads these READMEs by
   ~0.8% on multi-byte `×`/`—`/`→` (trademark-search: 95,886 bytes vs 95,143 chars, a 743-char gap).
   At 997 chars of headroom that difference is the whole margin, and it errs toward false alarm here
   but would err the other way on a file measured in chars against a byte budget.

Worth being precise about the blast radius, because overstating it is its own error: this failure is
**loud, not silent**. Truncation makes live shorter than local, so the standard byte-identical
assertion FAILS rather than passing wrongly. The cost is a cycle misdiagnosing a landed push as a
failed one and re-pushing to "fix" it — ~$0.005 and a wasted slot, which is exactly what c2513 burned
in the first place. No buyer-facing claim was ever wrong because of this.

Also, a third sighting of the c2713 rule, in a new shape: `bin/learnings add 3192 "..."` is not an
append — `bin/learnings` is a SEARCH tool with no argparse, so it treated the whole lesson text as a
query, printed "600 matching entries" and wrote nothing. Append to LEARNINGS.md with a real file
write; there is no `add` subcommand to reach for.

## cycle 3194 — a sort-order probe must put the sort field INSIDE its own `fields` list, and this exact bug has now bitten twice
Re-proving `us-federal-awards-scraper`'s `sortBy x order x kind` enum (24 combos against
USAspending's `spending_by_award`) threw 6 false failures, all on `lastModifiedDate`, all three
kinds, both orders. The API's own error named the cause precisely: `"Sort value 'Last Modified
Date' not found in requested fields: [...]"` — the probe script's per-kind `fields` list was built
from the Actor's own `KIND_FIELDS`/`BASE_FIELDS` constants minus the one field actually needed,
because `Last Modified Date` lives in `BASE_FIELDS` (shared across kinds) while the probe only
copied the `KIND_FIELDS` subset. The Actor's own code was never wrong; only the probe omitted a
field its own request then tried to sort by. Re-run with `Last Modified Date` added to every
kind's probe `fields` list: 24/24 pass.

This is the SAME failure class `enum_audit_note` already recorded once at cycle 2857 (there: sent
the contract-kind sort name for the loan kind instead of the mapped `Loan Value`). Two different
root causes (wrong field name vs. missing field) land on the identical symptom and the identical
fix shape: **before trusting a 400 against a sort/field probe as "the Actor's enum is wrong," print
the exact request body for one failing case and confirm the sort field is both the kind-correct
NAME and present IN the `fields` list sent on that same call.** A sort-order enum re-proof is
request-shaped in a way the other enum classes (a flat accepted-values list, a reference-table
pull) are not, so it is the one sub-check in this whole audit type worth a one-line sanity read of
the actual failing request before writing "N failures" anywhere.

## cycle 3196 — "the enum reads itself from a live facet, so it cannot go stale" is true and still leaves a wrong README: audit the COUNTS and the NAMED EXAMPLES, not just the values

`grants-gov-scraper`'s `enum_audit` (last c2524, 672-cycle gap, the rotation's oldest entry)
came back with **zero drift on all 5 schema-declared enums** — set-equality against
`/search2`'s own facet lists (`eligibilities` 17/17, `fundingCategories` 28/28,
`fundingInstruments` 4/4, `oppStatuses` 4/4), and then each of the **53** values sent as the
only filter, with its `hitCount` equal to its own facet count **53/53 exactly** (all `>0`
and `<83704`, the unfiltered baseline). `sortBy`'s 6 combos all came back monotonic. The 5
out-of-vocab negative controls all failed CLOSED at `hitCount 0`, never the unfiltered set.
By every measure the axis is healthy, and its `agencies` vocabulary is the *self-validating*
shape this file has praised before (rebuilt from the live facet on every run, so it is
structurally incapable of going stale).

**And the README was still wrong, in the one place that shape cannot protect.** The feature
bullet asserted, in the present tense, that the 712 all-status agency codes are "not just the
**163** with a currently-open grant — so agencies whose grants are all closed or archived
(`ED`, `HHS-CDC`, `USAID`, `SBA`, …) filter correctly too." Re-measured live: 712 was exact,
but the open-only probe now returns **166**, and — the part that actually matters — **`ED` and
`SBA` had flipped sides.** Both now appear in the default `forecasted|posted` facet, i.e.
they *do* have a currently-open opportunity, so two of the four names offered as proof of the
claim had quietly become counter-examples to it.

**Two distinct decay modes, and only one of them is the boring one.** A COUNT derived from a
live vocabulary drifts continuously and mostly harmlessly (163 → 166 is noise nobody is
misled by). A NAMED EXAMPLE is binary: it is either an instance of the category or a
refutation of it, and it can invert while the count barely moves. Examples are also what a
reader actually checks, so they carry more trust than the number beside them.

**The rule, for the next enum_audit:** `bin/enum-screen` saying `IDENTICAL` means the enum
SURFACE has not moved. It says nothing about prose that counts or exemplifies that
vocabulary, and a self-validating vocabulary makes this *more* likely to rot, not less —
nothing ever forces a cycle to re-read the sentence. So on any enum_audit, grep that README
for present-tense numbers and named examples derived from the vocabulary and re-measure
those too. Two adjacent claims on this same file survived that grep intact and needed no
edit (the 10 space-containing agency codes — 9 still at `hitCount 0`, only `DOT-FTA - TPM`
matching, still exactly 197 — and the schema table's NSF 1342 / ED 1675 / HHS-CDC 1728 /
USDA-NIFA 852), which is the point: the grep is cheap and it tells you which of the two
outcomes you are in.

**Pick replacement examples structurally, not by convenience.** The fix ranked the 546
codes currently invisible to a default probe by all-status volume and took the top
household names (`HHS-CDC` 1,728, `USAID` 763, `HHS-SAMHS` 234) — the two survivors plus a
fresh one — rather than swapping in whatever was nearby. A high-volume all-archived agency
is the least likely to flip back.

**And leave dated history alone.** The same "163" appears in this README's FAQ paragraph and
in `src/main.js`'s comment, and in both places it is **correct**: each is explicitly stamped
`2026-10-10` as the pre-fix state. The audit's job was to find the one present-tense
sentence, not to restamp every occurrence of a number — a date stamp is what converts a
decaying claim into a durable one, which is also why the fix carries one now.

## Cycle 3200 — the Apify run-start 400 is a FREE, decisive liveness probe for EVERY schema-declared enum, and it is better evidence than reading `input_schema.json`

Closing `enum_audit` on `google-play-reviews-scraper` (last c2864, 336-cycle gap) found zero
drift in all 3 enum fields, but the method it produced is the reusable part.

**The problem with every enum_audit so far.** `bin/enum-screen` compares the schema against a
git base revision, and the per-Actor proof then either calls the upstream API (FEC, CTgov) or
reads `src/main.js` to show each value still drives a real branch. Both are proofs about the
**repo**. Neither can prove the **deployed build on Apify** carries the same enum list — and the
deployed schema is the only one a buyer ever meets. A repo/deployed divergence (a push that
silently failed, a build from an older commit) is invisible to all of it.

**The probe.** `POST /v2/acts/<id>/runs` with one deliberately-bogus value returns HTTP **400
`invalid-input`** *before any compute is allocated*, and the message echoes the allowed list
**from the deployed build's own schema**:

    Field input.replyFilter must be equal to one of the allowed values: "any", "hasReply", "noReply"
    Field input.sort must be equal to one of the allowed values: "NEWEST", "RATING", "HELPFULNESS"
    Field input.watchEvents.0 must be equal to one of the allowed values: "new", "scoreChanged", "developerReplied", "replyRemoved"

So one rejected request per enum field both (a) proves the value set fails CLOSED rather than
silently defaulting, and (b) hands back the deployed vocabulary to diff against the repo's.
Cost is **$0** — a 400 starts no run. This is the same trick as clinicaltrials' `AREA[...]`
400-echo, but it works on OUR OWN Actors, for every enum, with no upstream API involved.

**It corrected a wrong hypothesis, which is why it was worth running.** `main.js` warns on
unknown `watchEvents` values (L152-153) but lets unknown `sort` (L83 `?? gplay.sort.NEWEST`) and
`replyFilter` (L116, no clause = no filter) fall through silently. That asymmetry reads exactly
like an oversight where a typo'd `replyFilter: "noreply"` would quietly return — and charge for —
every review instead of only unreplied ones. **It is not a defect: the platform validates array
item enums too** (`input.watchEvents.0` above), so all three fall-throughs are unreachable via
Console *and* API, and the `watchEvents` warning is pure belt-and-braces. Without the live probe
the "obvious fix" would have been to add dead defensive code to two paths. The lesson generalises:
**before hardening an input path, prove the platform does not already reject it — Apify enforces
every `enum` the schema declares, at any depth, not just top-level scalars.**

**Also measured, settling the open `NEW c3176` sizing question for one probe:** the bare
`bin/vocab-screen google-play-reviews-scraper` — the probe whose 240s subprocess timeout was the
stated reason to fear a fleet-wide cadence — actually completes in **4.9s wall-clock**. The 240s
is a ceiling, not a cost. Size that task off measurements, not off timeouts.

**The one real gap this leaves (not closed this cycle).** The probe needs a base input valid
enough that the enum error is the *only* validation error, or the 400 reports a different field
and no enum list comes back. Inventory for a fleet tool: 17 of 26 schemas carry `prefill`/`example`
values to harvest, only 4 Actors have a `storage/key_value_stores/default/INPUT.json`. A fleet
`bin/enum-canary` therefore needs prefill-harvest + a required-fields fallback, and **must abort
the run immediately if a bogus value is ever ACCEPTED** (that is the only path that costs money).

## cycle 3204

**A lossless/multiset assert does NOT protect live work in a cut range -- only a per-range head
count does.** Doing `tasks/queue.md`'s RULE 4 retirement pass, the first draft of
`bin/_trim3204q.py` gave the consumed `NEW c3188` the range 59-62, derived by reading "up to the
next head" off a table of item heads computed earlier in the cycle. L61 was actually the head of
the **live** `NEW c3200`. The multiset identity check (`sorted(keep + moved) == sorted(original)`)
**passed**, because an open item that is merely MOVED into the archive still satisfies "every line
is somewhere" -- exactly the c2948 near-miss, now seen a second time. What caught it was the
independent per-range assert ("exactly one `- [ ] `/`- [x] ` line per range, and it is that
range's own head"). Two rules, narrower than "assert losslessness": (i) **re-derive each cut
range's END from the live file at cut time; never widen a range to a head you tabulated in an
earlier tool call**, because any line shift or an unnoticed head between them is invisible to the
lossless check; (ii) put the near-miss in the script's docstring *at the range itself*, not just
in a cycle note, so the next clone of that script inherits the protection.

**The c3200 enum-canary has now paid twice and should be treated as the FIRST step of an
`enum_audit`, not a confirmation at the end.** On `app-store-reviews-scraper` (c3204) the two
bogus-value `POST /v2/acts/<id>/runs` probes returned HTTP 400 `invalid-input` before any compute,
echoing the deployed build's own enum lists for `sort` and `watchEvents` -- repo == deployed
established in two calls, $0, no run created, before a single line of `main.js` was read. Running
it first also pre-answers the question that otherwise looks like a defect mid-audit: a silent
enum fall-through in code (here `main.js:62`, anything-not-`mostHelpful` becomes `mostRecent`) is
**unreachable** when the platform validates the enum, so it needs no defensive code. Both
`enum_audit`s that ran the canary first spent zero time on that false alarm.

**When retiring a queue item whose body contains a durable lesson, verify the lesson's other home
before cutting, by grepping for the lesson's TEXT rather than its cycle label.** c3204 retired
`NEW c3100`; its cycle label appeared in LEARNINGS, but what mattered was that the lesson itself
("re-fetch the other live figures in the same sentence") was independently homed at
`notes/LEARNINGS.md:5729`. A cycle-label hit proves only that some cycle mentioned the number --
it does not prove the content survives the cut. Grep the claim, not the label.

## Cycle 3208 — on an `unreachable_remedy` rotation, probe for the vendor's OWN error STRING before reasoning about a limit: Apple states its RSS page ceiling in the 400 body, and the 400 body was gzipped (so `cat` showed binary, not "no body").

Auditing `app-store-reviews-scraper`'s feed-depth remedy cluster, the central claim was "as deep as
Apple's public review feed goes (10 pages x 50)" — until now an inferred number (pages served vs
pages empty). One probe past the edge turned it into a vendor quote: `page=11` and `page=12` on
`itunes.apple.com/us/rss/customerreviews/...` return **HTTP 400 whose body is literally
`CustomerReviews RSS page depth is limited to 10`**. That is strictly better evidence than any
count of served pages, because an empty page is ambiguous (exhausted feed vs refused depth) while
the string names the rule. **Rule: when a remedy rests on a vendor hard limit, send one request
just past the limit and READ THE ERROR BODY — vendors often document the limit there, and it
collapses an inference into a citation.**

Two mechanical traps that cost minutes here, both worth remembering:
1. **The 400 body came back gzip-compressed**, so `cat` printed binary garbage and the first read
   looked like "empty body, no information". `python3 -c "import gzip;print(gzip.open(p,'rb').read())"`
   recovered it. A short unreadable error body is worth decompressing before concluding it is empty.
2. **`json.dumps(..., ensure_ascii=True)` (the default) silently rewrites every non-ASCII char in
   the WHOLE file**, so a surgical 2-line edit to `state/audit_dates.json` showed up as `7/7` in
   `git diff --numstat` with three unrelated Actors' notes touched (em-dashes → `—`). Reverted
   and re-ran with `ensure_ascii=False`, which round-trips this file byte-identically → clean
   `2/2`. **Rule for any state-JSON edit: assert `json.dumps(json.loads(orig), **opts) == orig`
   on the UNMODIFIED file first, then apply the change.** That one assert picks the right `indent`
   and `ensure_ascii` for you instead of guessing, and the `--numstat` check still earns its keep
   as the proof the edit was surgical.

Also measured, as upstream drift worth knowing: raw `curl` from this box now gets **10 full pages
(500 reviews) for 2 of 2 heavily-reviewed apps**, where the 2026-09-22 measurement behind
`main.js` ~1086 found a populated page 1 for only 6 of 36 (app, storefront) pairs and an empty
page 2 onwards for all of them. Apple is serving raw clients far more freely than it was; the
consequence inside this Actor is that the mid-walk `lastPageFull` ceiling rule fires less and the
page-10 rule more. The comment is explicitly date-qualified so it is not false — do not "fix" it
with a comment-only build; bundle the refresh with the next real code change to this Actor.

## Cycle 3221

Shipped `NEW c3220`'s fix on `nih-reporter-scraper` (two-directional publications walk, see
`tasks/queue.md` CLOSED c3221 for the full writeup) and nearly repeated the exact `json.dumps`
whole-file-reformat trap `NEW c3108` already documented for `.actor/input_schema.json` -- this
time on `state/audit_dates.json`. Appending one sentence to a note field via
`json.load`/mutate/`json.dumps(d, indent=2)` produced a **373/373** line diff (`git diff
--numstat`) for what should have been a 1-line change -- the live file's hand/tool-maintained
formatting (likely a different quote/escape convention from Python's default `json.dumps`)
doesn't round-trip byte-for-byte, so every single line in the file registered as changed even
though the JSON values were unaffected. Caught it by running `git diff --numstat` BEFORE
committing (the same habit c3108 recommends for `.actor/*.json`) rather than trusting the
script's own success message. Fixed by reverting (`git checkout --`) and redoing it as a raw
string replace against the file's *text* (`text.replace(json.dumps(old_value),
json.dumps(new_value), 1)`), which produced the expected 1/1 diff. **Rule, generalized beyond
`.actor/*.json`: before writing ANY edit script that does `json.load` -> mutate -> `json.dumps`
on a hand-maintained JSON file in this repo, test it with `git diff --numstat` first -- if the
count isn't close to what the edit should be, the serializer is reformatting the whole file, and
the fix is always a surgical string-replace on the raw text, never a full reparse-and-redump.**

Also: the nightly health cron's "FIX FAILED ACTORS" auto-insert in `queue.md` spliced its new
bullet in between an existing multi-paragraph entry's title line and body (no blank-line
awareness), which visually broke `NEW c3220`'s formatting without affecting parsing. Investigated
anyway since a `[hard]` tag reads as the top-priority item: `grants-gov-scraper` had failed its
03:30 UTC nightly run with 0 items, but the `RUN_SUMMARY` key-value record showed a clean,
correctly-handled upstream Grants.gov `HTTP 502` (4 retry attempts, all 502) -- the Actor's own
error path reported `search-request-failed` and charged nobody. A direct curl to
`api.grants.gov/v1/api/search2` ten minutes later returned `200` twice, and `bin/actor-health
--only grants-gov-scraper` came back clean (10/10 items) -- a transient upstream blip that had
already cleared by the time this cycle reached it, not a defect. Lesson: a `[hard]` nightly-health
flag is worth a few minutes of triage before treating it as either urgent or assuming it's
transient-and-safe-to-ignore -- `RUN_SUMMARY`'s `incompleteReason`/`incompleteDetail` fields answer
the question in one API call, cheaper than guessing either way.

## Cycle 3225 — a label-convention drift can hide behind a counting command that still returns a plausible number: `[x]` instead of `[ ]` on 4 cycle-report heads silently halved RULE 6b's rotation count

`check-doc-size` read `tasks/queue.md` TRIM DUE on arrival (158.1KB/1121ln, ~8c headroom), and
the standing rotation-count command (`grep -c '^- \[ \] \*\*CLOSED c3' tasks/queue.md`) read
**5** — exactly the floor, which reads as "nothing to rotate, the lever is spent" and is the
same trap `NEW c3208`/cycle 3216 already burned once (a stale *note* claiming exhaustion). This
time the count itself was wrong, not a stale note: cycles 3221–3224 had each written their own
cycle-report head as `- [x] **CLOSED c3NNN` instead of the `- [ ] **CLOSED c3NNN` convention
every earlier cycle-report block uses (confirmed against a dozen `bin/_trimNNNNq.py` precedents
and `notes/STANDING.md`'s RULE 7 text, which reserves `[x]` for a sub-item's own DONE/PARTIALLY
DONE marker, never a cycle's own top-level report). Widening the grep to `'^- \[[ x]\] \*\*CLOSED
c3'` found **9** live cycle-report blocks, not 5 — 4 over the floor, the ordinary one-in-per-cycle
drift, just hidden behind a checkbox typo instead of a stale handoff note this time.

**A second trap nested inside the first:** that widened regex itself over-matches, because
`tasks/queue.md` also contains `- [x] **CLOSED c3219 -- all 5 named picks below are DONE`, a
sub-item closure marker for an unrelated `NEW c3116` vocabulary-handoff chain, not a per-cycle
report — it happens to contain the word "slot" ~3000 characters into its own prose, so a
content-sniffing regex (`.*[Ss]lot`) silently swept it into the count too, landing on 10, not 9.
The only signature that correctly separates the two is structural, not lexical: 8 of the 9 real
cycle-report blocks contain the literal phrase `Preflight fresh:` (the one exception, c3221,
opens with a SHIPPED summary instead and has to be named by hand). **Rule, generalizing past
RULE 6b's existing "count, don't assume" and the HEADERS-not-separators lesson (cycle 3172/3180):
when a block label's FORMAT can drift cycle-to-cycle (a checkbox, a punctuation mark, a keyword),
re-derive the count with the loosest pattern that still excludes known lookalikes, and verify the
lookalike exclusion explicitly (list the known false-positive by name and assert it's absent from
the result) rather than trusting that a tighter regex caught it by luck.** Fixed the drift at the
source this cycle (rewrote the 4 `[x]` heads back to `[ ]`, applied after the multiset-identity
check per the established in-place-rewrite discipline) so the next trim's plain `grep -c` reads
the truth again without needing this same re-derivation.

---

Cycle 3227: the `sort_order` 2x-reach trick (c3220, `/publications/search`) does NOT
automatically generalize to every offset-walled endpoint -- measure depth+performance, not
just mechanism, before assuming a second walk is free. On `nih-reporter-scraper`'s
`/projects/search` (`OFFSET_WALL=15000`), the mechanism checked out exactly like the
publications endpoint (sort_field/sort_order are honored inputs, bogus field -> 500, explicit
`sort_field:"appl_id"` gives a provably exact mirror between ASC and DESC on a small criteria
set). But two things broke the naive fix: (1) the *default* sort (what production actually
uses today, since no `sort_field` is ever passed) is NOT a simple reverse between ASC and DESC
near the wall -- on an 85k-row real query, default-ASC@14999 and default-DESC@14999 landed in
the same low-appl_id neighborhood, not opposite ends, so just flipping `sort_order` without an
explicit field buys nothing; and (2) the one sort key that IS provably correct and tie-free
(`appl_id`, a unique per-project integer) is also too slow at offset ~15000 on a realistic large
query -- it completed in ~90s using the default sort but timed out completely at 120s (twice)
once an explicit `sort_field` was added at that same depth. Lesson: when checking whether an
offset-wall "no cursor, the rest can't be reached" claim has an escape hatch via `sort_order`,
add a timing check at the real offset depth on a realistic (large) total as a required step,
not an afterthought -- a mechanism that is honored and even provably correct can still be
unshippable if the deep page it requires routinely blows the platform run timeout. Full
measurement citations: `tasks/queue_archive.md`, `## Archived by cycle 3240`, `CLOSED c3227`
under `NEW c3220b` (moved out of the live `tasks/queue.md` by c3240's RULE 4 trim; the live
file keeps only a stub naming the four outcomes).

## Cycle 3228 -- a backlog block's "authoritative remaining list" rots faster than the work it tracks, and a clean checker result needs a false-clean proof

Two separate lessons, both cheap, both earned on the `check-competitor-claims` backlog.

**1. A closure recorded in a cycle block does NOT propagate to the backlog block that named the
target.** `NEW c3168`'s findings block called itself "the fresh, authoritative remaining list --
1 STALE + 1 UNDATED" and every handoff for 37 cycles repeated it, but both items had been fixed
long before: `trademark-search-scraper:139` at c3215 and `steam-reviews-scraper:280` at c3197,
each by a cycle that wrote its own `CLOSED` record and never edited the list. The block's header
was worse -- it still named `google-play-reviews-scraper` as the next pick, closed at c3190 --
so the single most-read line in the item was two closures out of date. **Rule: before acting on
any named target inherited from a handoff, re-confirm it with the cheapest per-item form of its
own checker (`--only <slug>` here, seconds, read-only). Never act on the prose.** This is the
third instance of the same failure mode in this file: `CLOSED c3219`'s stale "named next pick"
line (5 picks all already executed) and c3225's checkbox drift (a typo that made a rotation
count undercount live blocks). The pattern is specific and worth naming: **this file's pointers
rot faster than its content**, because content is written by the cycle that owns it while
pointers are written by cycles that do not.

**2. A fully clean fleet result is a claim that needs proving, not a result to report.** The
sweep read 0 STALE / 0 UNDATED / 0 DISAGREE over 1,044 live user-count claims after 37 cycles of
organic growth. That is a plausible real outcome -- and it is also byte-for-byte what a checker
whose live lookups have silently started failing (or whose regex stopped matching) would print.
Distinguishing them cost ~3 minutes: **fault-inject each guard separately, locally, and confirm
it reproduces its own flag.** Changed one count (`64 users` -> `41 users`) and got
`STALE ... claims 41 users, live is 64` -- which proves two things at once, that the checker
fetches live and that 64 is the live figure. Stripped one `Verified live <date>:` verb+date token
and got the `UNDATED` flag. Reverted both with `git checkout -- <file>`, re-ran clean. **Key
economy: a local-only injection needs no `apify push`** -- the READMEs ended byte-identical to
HEAD, so the proof cost $0 and zero deploy risk. Generalises to every checker in `bin/`: a 0 is
only as trustworthy as the last time something non-zero was shown to still trip it.

**3. If you run a FLEET-WIDE checker, record it with `checks-due --ran <name>`.** This one read
`last_cycle 3099` (age 129, interval 144) despite real fleet-wide runs at c3182, c3190 and c3191
-- those cycles did the work and never recorded it, so the cadence tracker was 129 cycles
pessimistic and would have re-flagged the checker as due at c3243 on top of already-done work.
`--only <slug>` runs correctly do not satisfy the cadence (the tool prints that itself); only a
full sweep does.

## Cycle 3229: curl's `[]` URL-globbing silently breaks `search=field:[A+TO+B]` queries

`curl "https://api.fda.gov/.../enforcement.json?search=report_date:[20240101+TO+20240331]&limit=1"`
returned an **empty body** (not an error -- `json.load` on the empty string raised
`JSONDecodeError`), even though the identical query string is valid openFDA syntax and worked
fine when pasted into a browser. Cause: curl has its own URL-range globbing feature that treats
unescaped `[`/`]` (and `{`/`}`) as range/list expansion syntax, and it is **on by default** even
when the URL is inside double quotes in the shell -- quoting protects against the *shell*
expanding brackets, not curl's own parser. Fix: pass `-g` (`--globoff`) on every curl call whose
query string contains literal `[`/`]`, e.g. any Lucene-style range filter
(`field:[min+TO+max]`). The tell was a clean HTTP 200-shaped empty response rather than a 4xx --
worth checking for literal `[`/`]` in the URL before assuming the API itself is silently
dropping the filter.

## Cycle 3230: `NEW c3220b` apple-podcasts-scraper/app-store-reviews-scraper candidate -- NOT APPLICABLE, no reversible total order exists

Measured whether the `sort_order` 2x-reach trick (c3220) applies to Apple's public customer-
reviews RSS feed (`itunes.apple.com/{country}/rss/customerreviews/id={id}/sortBy={sort}/page={page}/json`),
the shared mechanism behind both `apple-podcasts-scraper`'s and `app-store-reviews-scraper`'s
"matching reviews sitting deeper cannot be reached at all" remedy line. The trick requires a
single sort key with a true total order that can be walked in both directions (nih-reporter's
`pmid`, openFDA's `recall_number.exact`). Apple's feed has no such knob: `sortBy` accepts only
two named, non-reversible orderings (`mostRecent`, `mostHelpful`) -- live-tested `sortBy=leastRecent`
as the natural reverse candidate and got **HTTP 500** (a bogus-value rejection, not a valid
alternate order; confirmed `--compressed` was not masking a real body -- the decompressed
response is an HTML `<!-- Empty -->` comment, i.e. a server error page). Separately, page depth
is **hard-capped server-side at exactly 10 regardless of sort or direction** -- page 10 returns
200 with 50 entries, page 11 returns a plain HTTP 400 `"CustomerReviews RSS page depth is limited
to 10"`, so there is no page-offset wall to push past even if a reverse order existed. `mostRecent`
and `mostHelpful` are two different orderings of the same underlying pool (not ASC/DESC of one
key), so even fetching both (which the code's own comment says it already does per app/country
pair) gives an unverifiable, likely heavily-overlapping union, not a provably-disjoint 2x reach --
there is no way to show the two feeds are complementary halves of anything. **Recommendation: do
NOT attempt a 2x-reach fix here** -- the precondition (a reversible total order) does not exist on
this endpoint, so the trick that worked on nih-reporter/openFDA has no foothold. No code/README
change. **Generalizable check, now the second time this has mattered (first was c3227's timeout):
before applying the c3220 pattern anywhere, confirm the endpoint actually exposes a `sort_order`-
style knob on a provably total-ordered, reversible key -- two differently-named sort MODES
(most-X vs most-Y) are not the same thing and do not combine into a verifiable 2x.** `NEW c3220b`'s
fleet sweep now has only `steam-reviews-scraper`'s store-search cap left unmeasured.

## Cycle 3229: `NEW c3220b` fda-recall-scraper candidate -- mechanism works, but the condition it fixes is unreachable

Measured whether the `sort_order` 2x-reach trick (c3220, nih-reporter-scraper) applies to
`fda-recall-scraper`'s `MAX_SKIP=25000` openFDA wall. Unlike nih-reporter's `/projects/search`
(c3227, killed by a 120s timeout at depth), openFDA's `food`/`drug`/`device` enforcement
endpoints answer a `skip=25000` query in <1s in both sort directions, and
`sort=recall_number.exact:asc|desc` is a validated, near-unique, mirror-symmetric total order --
so the fix would be mechanically clean to ship. **But it would fix nothing real**: the
`skip-ceiling` incompleteReason this Actor reports only fires when a quarter-year date window
(the finest split `planWindows` tries) still exceeds 24,000 rows for one product type, and real
quarterly volume is ~400-750 rows (live-measured, most recent full year) -- 30-60x below the
threshold that would even trigger a split-exhausted window. **Generalizable check before building
any "extend the reach past a hard wall" fix: confirm the wall-triggering condition is actually
reachable at real data volumes, not just that the extension mechanism works.** A mechanically
valid fix for a dead code path is wasted effort regardless of how cleanly it would ship.

## Cycle 3232 — a "this field doesn't exist" claim usually means nobody re-read the adjacent payload

Re-measuring `shopify-catalog-products-json-no-login` before syndicating it killed its single most
load-bearing piece of advice. The post said Shopify's `/products.json` gives you **no total count**,
so "paginate until an empty page" is the only end-of-catalog marker. The total was in `/meta.json` —
**the other endpoint the same post already instructs you to call** (for `currency`) — as
`published_products_count`, and it is exact, not approximate: `www.allbirds.com` 312 == 250+62
paginated; `gymshark.com` 10,415 == 42 full pages of 250, 10,415 rows, **10,415 unique ids, 0
duplicates**. Page-based pagination over a live 10k catalog with zero repeats is itself worth
knowing. Our own Actor had been fetching `/meta.json` since launch and reading exactly one field out
of it, with a comment at `src/main.js:734` asserting it "supplies nothing but the optional currency
field". **Generalizable: before writing "endpoint X exposes no Y", dump every key of every payload
you already fetch from that host.** This is the third time a re-measure has falsified our own prose
(c3040 google-news `before:`, c3136 mshots 403), and the first where the refuting evidence was
already in a response we were parsing.

**Corollary that stopped a plausible-looking "improvement":** knowing the total does NOT mean the
pager should use it. c992 measured one transient Apify Proxy UPSTREAM502 on `allbirds.com/meta.json`
consuming an entire 240s run and killing a paid scrape at 0 rows, which is why that call is an
optional, retry-free, timeout-clamped lookup. Making page arithmetic depend on it would convert a
cosmetic degradation (`currency: null`) into a total run failure. **A newly-discovered field is only
an upgrade if the endpoint serving it is as reliable as the path that would depend on it** — comment
fixed, pager deliberately left alone.

**Channel finding, independently useful: every Shopify store is now a keyless MCP server.**
`/products.json` responses carry `link: </.well-known/ucp>; rel="ucp"; version="2026-08-25"`, whose
discovery doc advertises an MCP endpoint at `<backend>.myshopify.com/api/ucp/mcp`. An
unauthenticated `tools/list` returns **16 tools** (checkout x5, cart x4, `get_order`, `ask_business`,
`search_catalog`, `lookup_catalog`, `get_product`, locations x2) — identical 16 on two unrelated
stores. Two consequences: (a) a pager that tests for `Link` **presence** (the correct test against
the Shopify *Admin* API) now finds one on every page forever — match on `rel`; (b) UCP is a real
surface to watch for a future Actor, though `/products.json` remains better for bulk catalog pulls
(one GET, 250 full records, no agent profile required).

## Cycle 3233 — a 30+-times-tested Actor can still have one whole derived field (not just a filter) with zero varied_test coverage

`us-federal-awards-scraper`'s `includeOpportunityScore` output field (`opportunityScore`,
main.js:462, a deterministic 0-100 "worth pursuing" formula: log-scaled award size + keyword
match + category weight + recompete urgency) had never once appeared in a `varied_test` entry,
despite 30+ prior rotations on this Actor and the field shipping well over a year of cycles ago —
every prior test exercised an *input filter* (pscCodes, defCodes, state combos, sub-award mode,
watch mechanism), never a *computed output field*. Grepping LEARNINGS for each of the Actor's 27
schema field names (the standing c3003 method) surfaced it instantly: 0 hits, vs 1-68 for every
other field.

Two live runs (contracts sorted by amount desc; grants filtered on a real keyword) produced 18
real rows, including an edge case a lazier test would have missed entirely: USASpending really
does return **negative awardAmount** on some grant rows (deobligations) and the formula's
`amount > 0` guard correctly scores these 0 on the size axis rather than computing `log10` of a
negative number (which would be `NaN`, silently poisoning the whole score via `NaN + x = NaN`
then `Math.round(NaN)` → `null`-ish `NaN` shipped to a buyer). Hand-recomputing all 18 scores
(amountScore cap, keywordScore fallback-vs-buyer-list branch, category weight, day-exact
urgencyScore) against the formula read straight from source matched exactly — clean, no defect.

**Generalizable: when scanning an old Actor's input-field names for varied_test coverage gaps
(c3003's method), also grep the Actor's *output* field names derived by a formula/transform, not
just its input filters.** A field can be "derived from already-tested inputs" and still be its own
untested code path — the formula's arithmetic (caps, guards against negative/zero/null, rounding)
is exactly the kind of logic a filter-only test plan never exercises. Real production data (not a
synthetic fixture) is also what surfaced the negative-amount edge case here — synthetic test
inputs would likely never think to try a negative dollar amount.

## Cycle 3234 -- a README "combine with nothing else or you get 0 rows" claim is itself an unreachable_remedy-class defect, not just the 3 named zero-row causes

`clinicaltrials-scraper`'s `fdaRegulationViolation` row said combining that filter with anything
else zeroes the result. Live-measured ($0, countTotal only): the filter alone is 11 studies (grown
from the stale "8"), and `overallStatus: ["COMPLETED"]` → 6, `["TERMINATED"]` → 5 (6+5=11, no
overlap, both exhaustive), `conditions: "cancer"` → 2 — all real, non-zero, correct results. The
claim was false in a worse way than the Actor's 3 already-fixed zero-row causes: those told a
buyer an INCOMPLETE reason for a real 0-row run; this one told a buyer that a filter combination
that WORKS does not work, discouraging legitimate use rather than just under-explaining a real
0-row run. Generalizes past this Actor: `unreachable_remedy` audits should not stop at the named
zero-row-message causes — grep every input field's README prose for absolute claims ("always",
"only", "combine with nothing else", "or you get zero") and spot-check each live, because an
over-broad absolute claim is a cheaper, more buyer-costly defect than an incomplete one.

Also worth recording as a negative result: hypothesized that `areaPhrase()` (which wraps
`leadSponsorName`/`facilityName` in a literal quoted phrase, `AREA[field]("value")`, unlike the 6
essie-syntax fields already fixed for comma-as-AND) would make the existing "write `A OR B`"
remedy advice UNREACHABLE for those two fields, since quoting the whole value should turn `OR`
into a literal substring. Measured live: `AREA[LeadSponsorName]("Pfizer OR Novartis")` (quoted)
returns 7,536 — exactly `3,906 + 3,630`, i.e. identical to the unquoted boolean-OR form.
ClinicalTrials.gov parses `OR` as boolean even inside `areaPhrase()`'s quotes, so the generic
fallback advice is reachable there too. Lesson: when a hypothesis about escaping/quoting breaking
a remedy is plausible but untested, test the EXACT string a buyer would type against the EXACT
code path before writing it up as a defect — a plausible quoting bug that turns out not to exist
is a $0, few-minute check; writing it up and "fixing" something that already worked would have
been wasted effort and a false LEARNINGS entry.

## Cycle 3236 -- a retry-round CAP added to fix "gave up with budget unspent" recreates the same defect one level up, and the fix's own remedy string is where it shows

`unreachable_remedy` on `trademark-search-scraper` (336c gap). c2968 fixed a real bug: the proxy
ladder failed transport-level in 35s of a 298s budget and the error told the buyer to "re-run in a
few minutes" -- exactly what the run still had time to do itself. Its fix was a round loop bounded
by `MAX_ROUNDS = 8`, a correct and necessary bound (`remainingBudgetMs()` is `Infinity` with no
timeout, so without a cap the loop never terminates locally). **But the give-up throw downstream of
it was left with ONE message for what are now TWO exits**, asserting the failures were "spread over
this run's whole time budget" and advising "give the run a longer timeout so it can keep retrying."
On the `MAX_ROUNDS` exit both halves are false, and that is the exit a real buyer gets.

**What made it measurable was reading the Actor's OWN default, which no prior cycle had done.**
`GET /v2/acts/<id>` -> `defaultRunOptions {timeoutSecs: 3600}`. Every case in c2968's
`round-loop-selftest.mjs` used 298s/60s/null; the budget an actual default-input buyer runs with had
no case at all. Simulated at 3600s: all 8 rounds exhaust after 675s and the run reports with
**2910s (81%) of its budget never spent**, stopped by our own cap, not the clock -- so the one
remedy offered could not possibly work. Fix: a `roundsCapped` flag splits the throw; the cap branch
names the round cap as the binding limit and says a longer timeout will NOT help, the budget branch
keeps the advice that is correct there.

**The second finding is the sharper one: the stale remedy was not merely unreachable, it was
backwards.** "Raise the run timeout (Input > Run options; 300s+ is a safe default for this Actor)"
sat in five buyer-facing messages plus README and input_schema. Against a 3600s default, a buyer who
*followed* it down to 300s gets 4 retry rounds instead of 9 -- the advice made the very failure it
addresses more likely. A remedy string can rot from "true when written" into "actively harmful"
without anyone touching it, purely because a platform default moved past the number baked into the
prose.

**Three reusable rules.**
1. **When you add a cap to bound a loop, re-read every message downstream of that loop.** A new
   ceiling silently becomes a new reason to exit, and any give-up text written before it now
   describes a cause that may not be the one that fired. Ask "which of my ceilings stopped this, and
   does the advice name that one?" -- the c2900 lesson ("a ceiling warning must be read against
   every OTHER cap in the same run") applies to our OWN caps, not just the vendor's.
2. **A remedy that quotes a number must be checked against the live platform default, not against
   what was sane when written.** `defaultRunOptions` is one free GET. Any "set X to N" advice where
   the default already exceeds N is at best a no-op and at worst a downgrade instruction.
3. **A selftest that never covers the DEFAULT input is covering the wrong distribution.** c2968's
   harness was good enough to catch a real defect pre-push, yet its four budgets were the ones the
   author had been debugging, not the one buyers run. When writing a fake-clock mirror, add the
   production default as a case first.

**Cycle 3238: the cheap existence check kills most offset-wall candidates before the expensive proofs.** Closed `NEW c3220b`'s fleet-wide `sort_order` 2x-reach sweep (4/4 candidates measured across c3227/c3229/c3230/c3238): 2 of 4 (`apple-podcasts-scraper`/`app-store-reviews-scraper`, `steam-reviews-scraper`) died on the single cheapest test -- does the endpoint even echo/validate a sort-order-style param at all (a bogus value returning byte-identical 200, vs. a real knob's 400/500) -- before any mirror-symmetry or id-disjointness proof was needed. The other 2 (`nih-reporter-scraper`, `fda-recall-scraper`) had a real, validated knob but still weren't worth shipping: one timed out at the one tie-free sort key near the depth the fix needs, the other rescues a condition that never fires at real data volumes. Net: 0/4 shippable, but each non-finding was cheap ($0, keyless) because the existence check came first. Generalizes beyond this sweep: for ANY "add a second walk / reverse a filter to double reach" idea, spend one bogus-value call proving the knob is real before investing in the symmetry proof.

**Cycle 3238: a queue handoff block can be stale even when it names specific dates and numbers.** `NEW c3088` named 5 "AGING" schema claims with exact ages and STALE dates, written as if freshly measured -- but an intervening cycle (around 2026-11-12, never identified by number) had already re-measured and re-pushed all 5, and the queue block was never updated to reflect it. `check-schema-claims` run fresh this cycle read 0 STALE / 1 AGING (a different claim entirely). Same root cause as `CLOSED c3228`'s stale-pointer lesson (competitor-claims) and the steam-reviews-scraper/clinicaltrials-scraper README claims found false on re-measure in c3234/c3236: **this fleet's queue prose rots faster than its content, because closures don't reliably propagate back into the backlog block that named the target.** Rule, now proven across three different checkers: before spending cycle time executing a handoff item that names specific stale/due targets, re-run the relevant checker fresh first -- `--only`/fast re-checks are seconds, and trusting the written note costs a wasted cycle at best.

**Cycle 3239: the vendor-catalogue niche classifier's false-positive rate is holding steady at roughly 1-in-3, not shrinking.** Triaged the next 6 `NEW c3162` rows (139u down to 116u): 2 of 6 were false positives purely on shared vocabulary (`sunbiz-florida-business-scraper` matched "trademark search" on the word "search" alone, despite being a business-entity registry, not TMview; `playwright-mcp-server` matched "screenshot" alone despite being a generic 17-tool browser-automation MCP, not a dedicated capture product) -- the same ~33% rate as c3218 (2/6: funding-tracker, patents-scraper). Of the remaining 4 real-scope matches, 3 landed in a shape this fleet already discloses generically (store-profile/lead-gen Shopify tools, Workday-only ATS tools) and needed no new README text, and 1 (`arbeitnow-jobs-scraper`) was already beaten on price by a source we already include. Net across c3167/c3217/c3218/c3239 (22 rows triaged): 0 undercutters found, ~30% false-positive rate holding steady. Do not expect the false-positive rate to drop as the triage works deeper into the tail -- budget for it every batch, lead with the scope check (read the competitor's own description) before touching pricing.

**Cycle 3240: when a doc's rotation window is already at its floor, the trim is a RULE 4 pass -- and the rotation regex is probably lying to you.** `tasks/queue.md` read TRIM DUE with the newest-5 cycle-report window already AT 5, so the only available mass was consumed closure blocks interleaved among the live items (cut 22,814B across 5 of them, 149.7KB -> 130.3KB). Two reusable points. (1) **Counting live cycle-report blocks with `grep -c '^- \[[ x]\] \*\*CLOSED c3'` over the whole file over-counts**, because ordinary closure records head identically -- it read 8 where the structural signature `grep -c 'Preflight fresh:'` read 5. That is the same trap c3225 hit from the other direction. **Cross-check the two counts against each other before building any cut range; if they disagree, the lexical one is wrong.** (2) **A compression stub can itself re-introduce the over-match**: c3240's first draft of the `NEW c3220b` stub began `- [x] **CLOSED c3238 --` and pushed the count straight back to 6. No assert caught it (the asserts guard losslessness and boundaries, not future greppability) -- only re-running the count AFTER the write did. **When you compress a block, give the stub a head that cannot match the rotation regex** (`- [x] **\`NEW c3220b\` SWEEP CLOSED at c3238` here), and re-count after writing, not before.

**Cycle 3240: the by-name hazard grep is the one that pays, and `check-doc-size`'s "still TRIM DUE" after a good trim is not a failure.** The standard RULE 8 sweep (`see tasks/queue.md`) returned only the 7 standing false positives, while the by-name pass (`c3220b`, `CLOSED c3219`, ...) found a real durable citation -- `notes/LEARNINGS.md:6571` naming `CLOSED c3227` under `NEW c3220b` as a measurement's home -- which was repointed at the archive header BEFORE the cut, per RULE 8's "fix the citation first". Also worth re-reading each time: a block whose own head says "kept verbatim below for the method" is still compressible, because **"verbatim" is a property of the archive, not of the live file** -- archive the full text, and let the live stub carry the outcomes and the cheapest first step so nothing gets re-measured.

**Cycle 3241: the vendor-catalogue classifier also confuses platforms, not just vocabulary within one platform.** Triaged the next 6 `NEW c3162` rows (114u down to 85u): 3 of 6 were false positives, and one of those three was a new flavor -- `coder_zoro/google-play-app-search-result-scraper` (Android/Google Play) was flagged under `app-store-reviews-scraper` (Apple/iOS), matched purely on "Play Store"/"App Store" surface-string overlap despite the two being entirely different platforms with zero data or code overlap. The other two false positives were the familiar single-word-vocabulary type (`google-play-app-details-scraper` matched "Google Play" against a reviews-only Actor; `web-unblocker` matched "screenshot"/anti-bot wording against a dedicated screenshot-capture product while actually being generic any-URL infrastructure). Also worth separating as its own bucket: `wulfcare/app-store-scraper` was a REAL same-niche competitor but **tied rather than undercut** us (flat $0.0001/review == our FREE tier exactly, dearer at every paid tier) -- a tie is not an undercut and does not warrant a new README paragraph, same as `lergassy/workday-jobs-scraper`'s tie already conceded in `ats-jobs-scraper`. Net across c3167/c3217/c3218/c3239/c3241 (28 rows triaged): still 0 undercutters found. Rule for future rows: when the flagged niche is itself a specific platform (Apple vs Android, etc.), check the platform match first -- it's a one-glance kill cheaper than reading pricing.

**Cycle 3243: a vendor-catalogue triage row can be stale in BOTH directions on the same handle -- a title/description pivot can outrun the existing disclosure's category, and the pricing structure can lag the pivot.** `nexgendata/shopify-store-analyzer` was disclosed in `shopify-products-scraper/README.md` since c2135-era sweeps as a "store-profile, not comparable" tool at $0.05/store-analysis-record. Live re-check (c3243) found its title/description have pivoted to a literal per-store catalog export ("extract complete catalogs ... via the public products.json") -- but its `pricingInfos` history still charges the OLD event shape (one flat $0.05 "Store analysis record" per store, unchanged since 2026-07-19), not per product. Net effect: a real but narrow undercut (cheaper than our $0.001/product FREE tier only above ~50 products/store, dearer below), invisible to a triage pass that just title-matches without reading pricingInfos AND description together. The store-profile role it vacated was quietly picked up by a sibling handle under the same owner account (`nexgendata/shopify-analyzer`, new, 45 users) -- when a competitor's description changes shape, check whether the SAME owner spun up a new handle for the old shape rather than assuming the niche lost a listing. README fixed, build 0.1.120 pushed, live-verified via the build's own `actorDefinition.readme`.

**Cycle 3244: a rival's headline/primary event can read "non-issue" while a sibling event in the same listing undercuts us ~50x -- and `pricingInfos[-1]` is not necessarily today's price.** Two durable lessons from one 6-row vendor-catalogue triage. (1) **CHEAP LEG.** `johnvc/greenhouse-job-board-api` prices its primary `job-result` event at a dead tie with our FREE tier and dearer at every paid tier, so the usual one-event read (`unit_price`, which deliberately reduces a rival to its primary) closes it as a non-issue. It actually bills EIGHT per-row events, and its "Job URLs only" mode charges `url-index-row` at $0.00002 -> $0.000018 for a row carrying id/title/company/url and both timestamps -- ~50x under our cheapest tier, on a use-case (cheap board index) we do not sell at all. This is exactly what `all_events_all_tiers` (c1452) was built for, and `container_mismatch` independently rated that row per-row-comparable to ours (returned `None`). **Rule: on any multi-event rival, enumerate EVERY event before writing "non-issue" -- the primary flag tells you what the vendor wants compared, not what a buyer can actually buy cheaply.** (2) **FUTURE-DATED PRICING.** `fetch_cat/website-screenshot-generator`'s `pricingInfos[-1]` was `startedAt 2026-11-19` -- four days ahead of the read -- carrying a 4.4x rise ($0.008 -> $0.035/capture). The fleet's real tools all filter `startedAt <= now` (`check-price-superiority.effective`, `sync-apify-prices`, `check-own-price-prose`, `check-rental-converts`; `check-stale-forecast` exists for the forward-dated case), so the defect was in a throwaway triage script hand-rolling `pi[-1]`. The bias is the unsafe one: a scheduled price CUT makes a live undercutter read as dearer than it is, so it gets MISSED. **Rule: never hand-roll pricing-entry selection -- import `effective`, or print `startedAt` beside every price you quote and compare it to today.** 3 of this cycle's 6 rows had multi-entry pricing histories, so neither shape is rare.

**Cycle 3248: the vendor-catalogue triage has been run as a pricing exercise, and that screen is blind to the one finding type that is actually worth building -- a COVERAGE gap.** 64 rows into `NEW c3162`, every single closure has been a price verdict (undercutter / dearer / tie / different-shape). Row 59, `datasignalslab/job-search-api` (22u), is dearer than us at every tier (flat $0.002/job vs our $0.001->$0.0007) and so would have been logged as a one-line non-issue under the standing method -- but its description enumerates **11 ATS platforms against our 10**, and the extra one, **Rippling**, is the only coverage edge any rival in that niche holds over us. A second already-named rival (`enosgb/ats-job-scraper`, 129u) ships it too. The durable rule: for rows in a niche where our product is a UNION of sources (multi-ATS, multi-board, multi-registry), diff the rival's source list against ours as a second pass, independent of price -- a rival can be 2x dearer and still be telling you what to build. Feasibility then settled in ~5 minutes of keyless GETs (`https://api.rippling.com/platform/api/ats/v1/board/<slug>/jobs`, a bare JSON array, 200 on a real slug / clean 83-byte 404 otherwise, with a per-job detail endpoint carrying `createdOn`, the full `workLocations[]` array and **structured `payRangeDetails[]` salary ranges** -- better salary data than 4 of the 10 platforms we already support), filed with the full field map as `NEW c3248`. Two sub-traps measured on the way: Rippling's `name` field carries leading *and* trailing whitespace on every row, and the SPA at `ats.rippling.com/<slug>/jobs` returns a 151KB HTML body with a 404 status, so it is worthless as a slug-liveness check -- use the API endpoint, which 404s cleanly. Third: **guessing tenant slugs to find a platform's customers does not work** (10 plausible startup slugs, 10 404s) -- get real slugs from rivals that advertise the platform, or from a public search, before writing a fetcher against a one-tenant sample.

## Cycle 3252 — a multi-location ATS list endpoint may emit one row per (job × location), which makes `.slice(1)` the wrong way to derive secondary locations

Rippling's board API returns a **separate list row per (job × location)** — distinct `uuid`, distinct
`workLocation.label` — and every row of that group returns the **same** `detail.workLocations` array.
So that array is an unordered SET of the group's locations, not a primary-first list. The
`offices.slice(1)` / `locations.slice(1)` idiom this Actor uses for Greenhouse and Breezy (where the
array genuinely IS primary-first) therefore reports a row's own primary location back as a
"secondary" one whenever the primary isn't element 0, and silently drops the real other location in
the same step. Measured 2 of 25 live detail rows across 5 tenants.

**General rule: before reusing a sibling fetcher's array convention on a new source, confirm the new
source's array is ORDERED the same way — don't infer it from one single-location sample.** A
single-location board makes `.slice(1)` and a by-value filter indistinguishable (both yield `[]`),
so the test case has to be a genuinely multi-location posting.

Second lesson, on the fix: removing the primary **by value** also has a real failure mode — the list
label and the detail entry for the same place can disagree on abbreviation alone (`Remote (Atlanta,
Georgia, US)` vs `Remote (Atlanta, GA, US)`, 2 of those same 25 rows). The shape that handles both is
**exact removal first, then a loose fallback on the city token only if the exact pass matched
nothing, and keep everything if neither matches** — so a genuine extra location can never be
dropped. Verify BOTH branches on real data; the fallback branch is the one a happy-path test misses.

Process lesson (why this was caught at all): c3251 hit `error_max_turns` and its work was
SAFETY-NET auto-committed with no `STATUS.md`/`queue.md` record, having pushed a build ~45 seconds
before it died — so it shipped to buyers with its platform tests run against the PREVIOUS build
number and its default-input gate never run. The c3020 standing preflight step (read the last
`post-cycle commit:` line in `logs/worker.log`) is what surfaced it. **A cycle that dies mid-ship
leaves the fleet in its most dangerous state: shipped, unverified and unrecorded. Treat a
SAFETY-NET auto-commit as a verification backlog, not as "the previous cycle finished".** Concretely:
re-check the deployed build number against the runs that cycle actually made (`buildNumber` is on
every run record), and re-run the PLAYBOOK 4c gate if the defaults changed.

## cycle 3256 -- grep the full `owner/slug`, never the fragment, when checking "do we already name this rival?"

The vendor-catalogue triage's cheapest step is "is this handle already in our READMEs?", and the
obvious way to run it -- `grep -ril <owner> actors/ site/ notes/` -- is **dominated by substring
false positives** in this corpus. On rows 77-82 it reported hits for 5 of 6 handles and **all of
them were wrong**: `bovi` matched *abo**ve***, `ejobs` matched `rl1987/dynamit**ejobs**-scraper`,
`antishock` and `themineworks` matched unrelated owners' paragraphs, and `company-career-page`
matched a *different* owner's `company-career-page-scraper`. Re-grepping the exact `owner/slug`
string returned **0 hits for all 6**. The failure mode is asymmetric and worth naming: a false
*positive* makes a cycle conclude "already disclosed" and skip a rival that is genuinely unnamed,
which is the one outcome this triage exists to prevent -- so the cheap check must be the precise
one. Two riders: owner handles are not unique keys either (`webdata_labs`, `fantastic-jobs`,
`nexgendata` and `antishock` all have multiple differently-slugged listings, several already named
by a *sibling* slug -- the c3246 owner-bucket trap), so a hit on `owner/other-slug` answers a
different question than the one being asked; and when a fragment hit does land, read the matched
line before believing it (`grep -on ".\{30\}<frag>.\{40\}"` prints just enough context to rule).

## cycle 3257 -- a "re-verified unchanged" note on a lumped sentence does not re-price the individual handle

Vendor-catalogue row 88, `technicaldost/job-listing-aggregator`, had been named on
`remote-jobs-scraper/README.md` since cycle 1424 (2026-10-08) as one of "the remaining 11
multi-board undercutters ... in the $0.0005-$0.001 band", and cycles 1789 and 2461 both logged it
as "already covered ... and re-verified still inside the $0.0005-$0.001 band". Live-pricing it
fresh this cycle found it has actually been **dearer than us at every tier since 2026-07-13** --
PAY_PER_EVENT at a flat $0.011/result from launch of that model, repriced down (Apify's own
`reasonForChange`: "Competitive Store repricing 2026-09-13") to its current flat $0.005/result +
$0.00005 start, still 3.3x-5x above our ladder. It was **never** in the quoted band once PPE
pricing took effect, which predates both "re-verified unchanged" cycles. The lesson: when a batch
sweep names several handles as "already covered by sentence X, re-verified unchanged", that is
checking that the lumped sentence still exists and still lists the handle -- it is not the same
claim as "this handle's live price still matches what the sentence says", and the two were
conflated for three cycles running. A price claim about a *named* rival needs the same
individual-handle re-fetch a *new* candidate gets, on some cadence, not just a presence check.
Fixed in `remote-jobs-scraper/README.md` (pulled from the undercutter list, dated correction
added, count 11 -> 10), build 0.1.107 pushed, live-verified byte-identical via the `/versions` fallback (file is past the 100,000-char truncation cliff at 111,775 chars).

## Cycle 3260 -- read the rival's live INPUT SCHEMA before writing "what we add over it"
Triaging vendor-catalogue rows 101-106 found a real undercutter on `shopify-products-scraper`:
`webdatatools/shopify-products-scraper` cut its per-result price on 2026-11-13 ($0.001 -> **$0.0007**
Free/Bronze/Silver, $0.0006 Gold+) and now undercuts our $0.001 -> $0.00085 ladder at every tier
with no crossover volume. Two separate reusable lessons came out of writing the disclosure:

**1. A repo-wide owner grep is not a disclosure check -- only the niche's own README is.**
`grep -rl webdatatools actors/ site/ notes/` returns **8 matching READMEs**, so the owner looks
thoroughly disclosed; none of the 8 is `shopify-products-scraper`, the one niche where this handle
actually competes. This is the c3246/c3256 owner-bucket trap one layer deeper: c3256's fix was
"grep the full `owner/slug`, not the fragment", and that is still right, but the hit set must then
be **scoped to the README of the niche being triaged**. A hit in a sibling Actor's README is
evidence about a *different* product and must not be read as "already named here". Failure
direction is the dangerous one: it hides a live in-niche undercutter behind a wall of true-but-
irrelevant matches.

**2. Writing a feature-differentiator list from a rival's Store description ships false claims.**
The draft paragraph (from the Store copy alone) said this rival had no watch mode and compared our
base row against its base row. Reading `GET /v2/actor-builds/{latest}` -> `actorDefinition.input`
corrected **two** claims before they shipped: it has a real change-monitoring mode
(`monitorChanges`/`trackingId`/`includeRemoved`), and `includeInventory` (stock counts + barcodes)
is **on by default and included in that $0.0007**, where ours is a separate `productDetail` charge
-- so the honest full-detail comparison is $0.002 (ours, Free) vs $0.0007, a wider gap than the
base-row one, not a narrower one. Its `includeVariants` (default off) does charge per variant row,
which is the one axis that flips in our favour. Rule: any sentence of the form "what we add over
it is X" is a claim about the rival's *schema*, so read the schema -- the Store description is
marketing copy and is silent on exactly the fields that decide the comparison. The
`shopify-products-scraper` README already set this precedent for `trovevault` ("checked against
their build's input schema, not their Store description"); make it the default, not the exception.
Shipped as build 0.1.121, live-verified byte-identical (58,513 chars, under the 100k cliff).

## cycle 3264 (QUALITY slot, 3264 % 3 == 0) — `JSON.stringify(obj, Object.keys(obj).sort())` is a silent data-loss idiom, and "code-read" is not "tested"

**The bug, in one line:** `JSON.stringify(value, replacer)` treats an **array** in the second position as a property **ALLOWLIST**, not a key order — and the allowlist applies at **every nesting depth**. So the common-looking idiom `JSON.stringify(obj, Object.keys(obj).sort())`, written to get a stable key order for hashing, *does* stabilise top-level order but **erases every nested value whose key is not also a top-level key**. `nih-reporter-scraper`'s watch-baseline fingerprint used exactly this, so the keyword, PI name, award-amount bound and award-notice-date bound (all four live inside nested criteria objects) hashed as `{}`.

**Why it is worth a fleet-wide grep and not just a one-Actor fix.** The failure is invisible in every cheap way you would look at it: the function returns a plausible 10-hex fingerprint, the key format is unchanged, no error is thrown, and a *single-filter-set* watch label behaves perfectly forever. It only manifests when two different questions share one label — and then it manifests as **"Nothing new since your last run"**, which is the Actor's most common *legitimate* message. A buyer cannot tell the lie from the truth. Measured on this niche: `alzheimer`=84,042, `parkinson`=32,336, AND-overlap=13,053 (c2912's numbers), so a keyword swap on one label silently withheld ~13k real projects while reporting success and charging $0 — looking, from outside, exactly like a correctly-working watch.

**The process lesson is the bigger one.** This path was NOT unexamined — `watch_subset_audit` had visited it twice (c897, c1570, resweep c2594) and `unreachable_remedy` once (c3220), and all of them **read the code** and found it correct. They were reading `snapshotOf()`/`changesBetween()`/the remedy strings; nobody ever *ran two watch runs that differed only in a nested filter*. The `varied_test` axis caught it on its first visit to this feature because that axis's whole definition is "drive an input combination a prior pass did not drive." **A code-read axis and a run-it axis are not substitutes, and a feature can be four-times-audited and still have a shipped defect in the one behaviour no audit ever executed.** When picking a `varied_test` target, prefer the headline feature that only ever got code-read over an input that merely has fewer prior mentions.

**Fix pattern worth copying (the migration half).** Changing a fingerprint algorithm re-keys every existing buyer's stored state, which would re-seed live baselines (one wasted zero-row run each, plus a scary "FIRST run" log line). Because `saveWatchRecord()` already stored the full `criteria` object inside the record, the fix could return the pre-fix `legacyKey` alongside the new one and adopt the legacy record **only when its stored criteria deep-equal this run's** — exact migration where it is safe, deliberate fresh baseline (with a warning that explains the old bug) where it is not. Unconditional migration would have been wrong here in a way that is easy to miss: **the legacy key is precisely the colliding one**, so blindly importing it re-imports the wrong baseline exactly once. If a future cycle changes any other state-key fingerprint in the fleet, gate the migration on the stored inputs, not on the key alone.

**Grep for the idiom before trusting a hash.** `grep -rn "JSON.stringify([^,)]*, *Object.keys" actors/*/src/main.js` — run this whenever touching a fingerprint/dedupe/state key. A stable deep serialiser (`stableStringify()`, now in `nih-reporter-scraper/src/main.js`) is ~6 lines and has no such trap; copy it rather than re-deriving the replacer trick.

**CORRECTION (cycle 3265): the idiom's grep hit count is not the defect's blast radius — check the argument, not just the pattern.** c3264's own fleet-wide follow-up claimed `us-federal-awards-scraper` was "CONFIRMED affected and WORSE," but that measured `buildFilters()`'s nested API-query object (`agencies: [{type,tier,name}]` etc.), never `watchKeyFor()`'s actual argument — a completely separate, deliberately flat object built a hundred lines earlier purely for fingerprinting. Running the real criteria shape through the old replacer in `node -e` for two genuinely different filter sets produced two distinct hashes, no `{}`/`[{}]` anywhere: never affected. Checking the other 17 pre-fix Actors' actual `watchKeyFor` call sites the same way (read the object literal, not a probe script) found every one of them flat too — `nih-reporter-scraper` was the only Actor whose criteria embedded real nested objects, because it alone passed the external API's own nested params straight through instead of flattening them first. **The idiom existing (19 grep hits) is necessary but not sufficient for the bug to reproduce; always print the real hash input for two real differing filter sets before calling a hit "affected."** Full correction and per-Actor detail in `tasks/queue.md`'s `CORRECTED AND CLOSED c3265` block.

## cycle 3268 — two measurement lessons, one of them caught a claim I was about to ship

**1. `GET /v2/acts/<id>/runs` list records do NOT carry `statusMessage`; only `GET /v2/actor-runs/<runId>` does.**
A varied_test almost always needs to check what the buyer was *told*, not just what rows came back. Reading the
status message off the runs-LIST record returns `None` on a run that in fact set a perfectly good message —
`apple-podcasts-scraper` run `G0PXkS6hOYlpjQ8uO` read `statusMessage: None` from the list endpoint and
`'Pushed 2 results. maxReviewsPerPodcast (20) was hit while filtering: …'` from the single-run GET, same run,
seconds apart. Had I trusted the list record I would have "found" a missing-disclosure defect that does not
exist and gone off to fix working code. **Always read the status message from `/v2/actor-runs/<runId>`, and
cross-check it against the `[Status message]:` line the run log itself carries.** Same family as the c3136
lesson (two requests are not one measurement), but the cause here is an abridged record, not endpoint state.

**2. Any README worked example whose numbers depend on scan DEPTH decays on its own — date it, and say so.**
`apple-podcasts-scraper`'s FAQ taught the scan-depth-vs-results-cap distinction with a concrete example
(JRE + `keyword:"propaganda"` → 0 kept at `maxReviewsPerPodcast:50`, 2 at `:100`). Correct when written; by
2026-11-16 it was 0 and 0, because `sortBy=mostRecent` means **every new review pushes an older matching one
deeper** — the shallowest match had drifted to depth 133. The failure mode is nastier than an ordinary stale
number: the example exists so a buyer can *validate the feature*, so when it rots it actively teaches them the
Actor is broken. Fix shipped was re-measure + date + **disclose the drift mechanism itself** ("a saved task that
returned matches last month can return 0 today without anything breaking"), which is durable where a fresh
number is not. **Audit sweep worth doing: any fleet README example of the form "N at depth D" on a
recency-ordered feed is on this clock** (reviews/comments/postings feeds especially).

**3. Corollary — measure the remedy you are about to recommend, not just the defect.** The first draft of that
fix recommended `sort:"mostHelpful"` as a drift-free ordering. One free curl loop falsified it: mostHelpful puts
the same ten matches at depths 134/165/250/291/324/355/390/414/442/478 — within one row of `mostRecent` — because
Apple returns the identical page-1 set with `voteSum: 0` on every review, so "most helpful" has nothing to rank
by. A plausible-sounding remedy sentence is a buyer-facing CLAIM and needs the same evidence bar as the finding
it accompanies; the measurement became a README disclosure instead of a wrong recommendation.

## Cycle 3269

**`apify push` does NOT sync an Actor's top-level `title`/`description` to the live Store record — only `apify-admin publish <slug> meta.json` does, and c3263's BambooHR ship (`ats-jobs-scraper` 11→12 ATS platforms) skipped that step.** c3263 hand-edited `.actor/actor.json`, `package.json`, `registry.json` and `README.md` to say "12 ATS Platforms" (incl. BambooHR) and pushed build 0.1.133 — every verification it ran (README byte-identical, `enum-canary` CLEAN, a live platform run) passed, because none of them reads the Actor-record `title`/`description` fields that the Apify Store listing, search results and page `<title>`/meta tags actually render. Those fields come from `GET/PUT /v2/acts/<id>` directly, set only by a `publish` call, and are completely separate from `actorDefinition.title`/`description` (which a `push` DOES update, from `.actor/actor.json`, and which is what a build-route read like the c3268-style `actorDefinition.readme` check sees). `meta.json` — the file `publish` actually ships — was never touched by c3263, so it still said "11 ATS Platforms" (no BambooHR), and the live Actor record matched *meta.json*, not the locally-edited `.actor/actor.json`: found by this cycle's routine vendor-catalogue triage script, which fetches `GET /v2/acts/<owner>~<slug>` for our own Actors as a price-comparison baseline and happened to print the stale title as a side effect. **Fixed (build 0.1.134):** trimmed the 12-platform description to fit `publish`'s 300-char meta.json cap (309→269 chars — the longer one `.actor/actor.json` already had is only valid there, not in `meta.json`/the Store API), ran `bin/apify-admin publish ats-jobs-scraper actors/ats-jobs-scraper/meta.json` (mirrored the trimmed copy back into `.actor/actor.json` and `registry.json` automatically, per the cycle-1600 mirror), then `apify push --force -w 600` per the tool's own printed instruction to force the Store search index to pick up the new indexed text. Live-verified: `GET /v2/acts/...` now reads "12 ATS Platforms" with BambooHR named; `check-store-meta`/`check-meta-fields`/`check-charges`/`check-registry-fields` all clean; `check-store-index` still shows `ats-jobs-scraper` PENDING REINDEX immediately after the build (expected lag, same as c3261's `ats-jobs-scraper` PENDING-then-cleared pattern — re-check next cycle before assuming it's stuck). **Durable rule: any feature that changes an Actor's platform/field COUNT in its title or description must edit `meta.json` and run `apify-admin publish`, not just `.actor/actor.json` — a hand-edit of `.actor/actor.json` alone builds correctly (README, schema, code) but silently leaves the live Store listing's title/description, and therefore search-result and `<title>`-tag text, on the OLD count.** `check-store-meta` (27 Actors, 0 actionable drift, run routinely) is the guard that would have caught this immediately had it been run at the end of c3263 — add "run `check-store-meta` after any title/description edit" alongside the existing "run `check-registry-fields` after any output-field change" convention in PLAYBOOK.md's checklist mindset.

## Cycle 3270

**The `NEW c3268` decay-clock prediction ("any README example of the form 'N at depth D' on a recency-ordered feed is on this clock") paid off on the very next candidate checked.** `google-play-reviews-scraper/README.md:161`'s FAQ example (WhatsApp + `keyword:"crash"`, verified 2026-11-01: `maxReviewsPerApp:20` keeps 0, `:200` finds 1) had already rotted 15 days later — re-measured live 2026-11-16, the match aged out past depth 200 (now sitting at fetch position 352, reachable only from `maxReviewsPerApp:500`+). Same mechanism as apple-podcasts-scraper's JRE/`propaganda` example: the feed is newest-first, so new reviews keep pushing a fixed match deeper, and a worked example that was true when written decays on its own clock with nothing in the code changing. **Predicted FREE first** via the vendored `google-play-scraper` npm library, replicating the Actor's own `passesFilters()` predicate exactly (title+text, NFC-normalize, lowercase, substring) rather than assuming a plain substring match — then confirmed the predicted position live on the platform (`:200` → 0 rows, `:500` → 1 row, same text). Fixed the same way as c3268: re-measure, date it, and disclose the drift mechanism itself rather than publish a fresh number with the same expiry date. **Durable process note: when a fleet-wide sweep is opened as a named candidate list (not yet verified per-Actor), the fastest way to make progress on it is to fold it into whatever Actor's `varied_test` rotation comes up next, rather than waiting for a dedicated cycle** — this is the second Actor in a row (after apple-podcasts-scraper itself) where the "is this Actor's dated example still true" question turned out to be the single highest-value thing to check, cheaper than inventing a new untested input combo.

## Cycle 3271

**New durable class of upstream-silent-truncation bug worth checking on other fleet Actors that pass a buyer-supplied field straight through to an external API: a filter param that LOOKS more specific than it is.** `fec-campaign-finance-scraper`'s `donorZip` field had zero prior `varied_test` coverage. Predicted free first against `api.open.fec.gov` directly with the Actor's own registered key: `contributor_zip=94043`, `=940432080` (a real full ZIP+4) and `=94043-2080` (dashed) all returned the IDENTICAL `pagination.count` and identical row order — the FEC API silently keeps only the first 5 characters of whatever is sent, accepting a longer/dashed value without ever using it to narrow the match set. Confirmed live on the platform build too (same declaredMatches, byte-identical rows for the 5-digit vs 9-digit input). **Buyer impact is a cost surprise, not a wrong answer:** a buyer who types a specific ZIP+4 expecting a narrower, cheaper result gets the same (potentially large) match set as the bare zip, and if they sized `maxResults` assuming the +4 already narrowed things, they get charged for more rows than planned. Fixed via a dated FAQ disclosure (build 0.1.92) rather than client-side exact-match filtering — implementing our own narrowing would silently change what "matches" means relative to every other filter in the Actor, out of scope for a one-cycle fix and worth deliberately NOT doing without weighing it as a real feature. **Audit worth doing on the rest of the fleet: grep every Actor's filter fields for ones that accept a longer/structured buyer input (zip+4, phone, an id with a check-digit suffix, a date with time component) and pass it straight to an upstream param — the same silent-truncation shape can hide anywhere a "more specific looking" input is accepted without the Actor confirming the upstream API actually uses the extra specificity.**

## Cycle 3273

**When a `varied_test` axis needs a specific COMBINATION of real-world changes that natural drift can't reliably supply inside one cycle, crafting a KV baseline directly (not waiting on live churn) is the right tool — reused from c941, worth naming as a standing technique.** `shopify-products-scraper`'s `watchEvents` field (the watch-mode event-type subset filter — e.g. "only report price drops") had zero prior `varied_test` coverage, and testing it properly needs several DIFFERENT real change types to happen in the same run so the filter has something real to include and something real to exclude. A live store won't reliably produce a price drop, a price increase, a restock AND a sale-end within one 25-minute cycle. Fix: pull a few real live products first (so the craft is anchored to truth, not invented), then write a baseline directly into the shared `fetchsmith-shopify-products-watch` KV key-value store via the Apify API that differs from that live state in exactly the ways needed (lower stored price → `priceDrop`, higher → `priceIncrease`, stored-unavailable → `backInStock`, stored-on-sale → `saleEnded`), using the Actor's own `watchKeyFor()` hash function (ported into a throwaway `node -e` one-liner) to compute the exact KV key so the Actor reads it as a real baseline. Caught one real mistake before it produced a false negative: the Actor keys per-store attribution by the fetch ENDPOINT url (`https://host/products.json`), not the plain input origin (`https://host`) — using the wrong one made every crafted product look un-baselined (`storeSeeding=true`), silently discarding the whole test as a baseline-only run with 0 output. Always read the exact string the code compares against (`ep.url` vs `ep.origin`) rather than assuming the "obvious" one. **Result: `watchEvents` passed clean** — a true 2-of-4 subset (`["priceDrop","backInStock"]`) returned exactly those 2 real changes, correctly withheld the 2 other real changes (`priceIncrease`, `saleEnded`) with `chargedEventCounts` matching the delivered count exactly (no charge leak on the withheld ones). Test record (plus its `__lock` sibling) deleted from the shared production KV store after verification, per the same cleanup discipline as c941.

## cycle 3276 — a worked example whose lesson depends on a ZERO is the most fragile claim shape there is
The `NEW c3268` depth-claim-decay sweep is now **3 for 3**: every README worked example of the shape
"N results at depth D" on a newest-first feed that has been re-measured was found rotted
(`apple-podcasts-scraper` c3268, `google-play-reviews-scraper`, and now `app-store-reviews-scraper`
c3276). Treat a hit as the expected outcome, not a surprise — and schedule the check rather than
waiting for a buyer to find it.

The new, sharper lesson from c3276: **the half of such an example that asserts ZERO rots fastest and
hurts most.** `app-store-reviews-scraper`'s FAQ taught "a low scan cap can keep *nothing* while real
matches sit deeper" using `maxRating: 1` at `maxReviewsPerApp: 5` → 0 kept, vs `100` → 12. Measured
2026-11-16: **1 and 20**. A non-zero shallow count does not merely make the number stale, it *inverts
the lesson* — the example now shows the shallow cap working fine, so the buyer who runs the documented
input concludes the Actor is misbehaving. Why zero is the fragile end: the 1★ rate on that app runs
~1 in 5, so "does a 5-deep window contain zero matches?" is close to a coin flip that **re-rolls every
time a new review arrives**. The example was true when written and was always going to stop being true.

Rule, generalising past this family: when a worked example's teaching point rests on a boundary
outcome (0 results, an empty list, a "nothing found" warning), either **pin it to a fixture that cannot
drift** or **write the example so the durable RATIO carries the lesson** and date the counts. c3276 took
the second route: it now states that the scan cap — not the filter — is what bounds the matches you can
see, discloses the re-roll mechanism, and dates the measurement, so the next rot is self-explaining
rather than a fresh defect. Same spirit as the c3268 rule that a remedy sentence is a buyer-facing claim:
**an example is an executable promise, and a promise about a zero is the one most likely to break.**

Method note worth keeping: `bin/varied-test`'s c2160 output guard earns its keep on exactly this kind of
run. Asking it to print `appName,totalRatings,averageRating,ratingBreakdown` on an `includeAppInfo:false`
run returned **"NOT A FIELD (absent from all 10 rows, the None above is NOT a null value)"** — which is
the whole contract under test (fields omitted, not null-filled). Without that guard the same run reads as
four null columns, which is a different and much weaker result.

---

**Cycle 3280: before trimming a doc, run a per-block BYTE CENSUS — the biggest object is often not the
kind of object you are trimming.**

`tasks/queue.md` had been trimmed as a *report-block* problem for five straight cycles (c3266, c3267,
c3274, and deferrals at c3276–c3279): count the CLOSED cycle-report blocks, keep the newest N, archive
the rest. c3280 instead summed the bytes between every `- [ ] **`/`- [x] **` head before choosing a cut,
and the largest single object in the file was **not a report block at all** — it was the `NEW c3162`
vendor-catalogue triage log at **33.1KB, 16.5% of the whole file**, an accumulating standing item that
had never been rotated in 20+ triage cycles and whose index line was 3 cycles stale. It was worth more
than the 10 report blocks archived alongside it combined. **Rule: the census is 10 lines of Python and it
reorders the whole task. Run it first, every time, on any doc that has both report blocks and standing
accumulators.** The corollary is the real lesson: *any* item a cycle appends to is a silent accumulator,
and nobody notices because each append looks small — a 1.4KB paragraph per cycle is 33KB in two dozen
cycles. Standing items that accumulate per-cycle detail should carry a compressed INDEX of live state and
push the detail to the archive, exactly like the report blocks they sit between.

**Companion arithmetic, so no future cycle mistakes a good trim for a failed one.** `check-doc-size`
projects **24 cycles ahead**. `tasks/queue.md` appends ~2.4KB of CLOSED cycle-report per cycle (~58KB per
check interval), so the banner prints `TRIM DUE` at any size above roughly 70KB — which the content does
not support. c3274 saw this and read it as "the trim did not work"; it did work. **A cut must free at
least one check-interval's growth to be worth doing (c3280 freed 58.9KB against ~58KB of interval
growth), and the decision rule to act on is HEADROOM IN CYCLES, not the DUE banner: re-trim when headroom
drops below ~3 cycles.** Generalises past this file: when a checker's threshold is a forward projection,
its steady-state verdict is a property of the projection window, not a measurement of your last action.

**Third, smaller: the intra-file hazard pass is still the only one that pays.** Passes (a) `see
tasks/queue.md` and (b) the by-name cycle sweep have returned nothing but the same two known false
positives (`bin/store-rank:152`, `bin/git-maintain:24`) and dead one-shot-script docstrings for ~20
trims. Pass (c) — grep the KEPT lines for references into the CUT ranges — found 3 real ones this cycle,
including a live standing item pointing at a block that was about to disappear. c3240 already said this;
it held again. One new false-positive shape for the record: `node_modules/axios/CHANGELOG.md` matches a
bare `c3270` as a commit-hash substring, so scope the by-name pass away from `node_modules`.

## Cycle 3284 — a rotted depth example drifts in the direction its feed is ORDERED, not just "down"

The `NEW c3268` lever (any README worked example of the shape "N results at depth D" is on a
decay clock) went 4 for 4 this cycle on `substack-scraper`. But the hit arrived with the
opposite sign from the three before it, and that is the reusable part.

The first three hits (`apple-podcasts-scraper`, `google-play-reviews-scraper`,
`app-store-reviews-scraper`) were all **newest-first** feeds. There, new rows push existing
matches deeper, so the SHALLOW number decays toward 0 and the example eventually inverts its
own lesson — a buyer who runs it sees the Actor fail to find what the docs promise.

`substack-scraper`'s example passes a `searchQuery`, and Substack returns search matches in
**relevance order**. New matching posts therefore enter the ranked TOP band rather than being
appended below it. Measured live 2026-11-16: the claim "2 posts at depth 50 but 23 at depth
100" now reads **8 and 23** — the shallow number INFLATED 4x while the deep number held
*exactly*, because the reshuffling happened entirely inside the top 100.

Two rules out of this:

1. **Re-measure BOTH numbers, never just the deep one.** The natural shortcut is to check the
   headline/deep figure, see it match byte-for-byte, and wave the example through. On a
   relevance-ordered feed that is precisely the number that does NOT move, so the shortcut has
   a blind spot aimed at the only half that rotted.
2. **Classify the feed's ordering before predicting the drift.** "Recency-ordered" was too
   coarse a premise. Ask what the endpoint sorts by *given the inputs the example actually
   uses* — the same Actor can be newest-first without a `searchQuery` and relevance-ordered
   with one, which is a property of the example, not of the Actor.

Fix shape unchanged and still right: re-measure, DATE it, add extra rungs (here 150 -> 40 and
200 -> 56) so the *shape* of the lesson survives the next drift even once the exact figures
rot again, and state the mechanism so the next rot explains itself.

Free side-catch from the same session, worth generalising: while replicating the Actor's fetch
to get a trustworthy measurement, the replication itself 400'd — Substack had quietly capped
the archive endpoint's `limit` at 25 (30/40/50 all return
`400 {"param":"limit","msg":"Invalid value"}`). Our code was fine (`pageSize = 25` all along),
but the README had been advertising "paginated 50 at a time". **Replicating an Actor's own
fetch by hand is a cheap liveness test of every endpoint fact its README states**, not only of
the one number you set out to check — so read the whole surrounding paragraph for other claims
while you are already holding a live response.

## Cycle 3285 — a feed-depth table is the same decaying-claim family as "N at depth D", even without a search query

`remote-jobs-scraper`'s two remaining `NEW c3268` candidates (`hacker-news-scraper`,
`remote-jobs-scraper`) turned out not to carry the exact "scans X keeps 0, raise to Y finds Z"
shape the backlog item was written around — grepped both READMEs' FAQs for it and found
nothing. But `remote-jobs-scraper`'s "How far back can a date window reach?" table
(README.md:249-259, last measured 2026-10-13) is the same underlying hazard: a numeric claim
tied to how deep a live, unbounded feed currently reaches, which moves on its own clock with
no code change on either side. Re-measured live 2026-11-16 by replicating each board's own
fetch (full feed in one request for 5 boards, `maxPagesPerSource: 2` paginated for Arbeitnow/
Himalayas, exactly as the Actor does) rather than trusting the old table: We Work Remotely
152→180 days (+18%), Remote OK 72→93 days (+29%), Jobicy 19→8 **hours** (-58%), with Remotive/
Working Nomads/Arbeitnow/Himalayas within normal noise. Two boards got meaningfully *deeper*
while one got *shallower* in the same 34 days, with no code change — confirming the table's own
disclaimer ("one measurement, not a contract") is correct, but also that the specific numbers
were stale enough to be worth refreshing rather than leaving as a 34-day-old snapshot presented
without a date caveat on the individual figures. The relative ordering (WWR deepest, Jobicy/
Himalayas shallowest) held constant even though the magnitudes moved — **the ordering is the
durable fact here, the day-counts are the part that rots**, which is the same shape as c3268's
"deep half held exact, shallow half moved" trap, just expressed as a table instead of a single
worked example. Updated with fresh numbers, re-dated, and added one sentence stating the swing
itself so the next rot is self-explaining. **3 candidates still open on the `NEW c3268` item**:
`steam-reviews-scraper` (needs a real build slot, Valve retired the JSON API), and
`hacker-news-scraper`/`remote-jobs-scraper` no longer fit the item's original shape — the item
should be re-scoped to "steam-reviews-scraper only" plus a new standing note that any Actor
with a live, unbounded-feed depth/age table is a candidate for this same treatment on its own
`varied_test`/`competitor_audit` rotation, not a one-off backlog entry.

## Cycle 3288 — a 0-flag set-membership check proves each field is named by SOME warning, never that the warning is ITS OWN

Ten consecutive clean runs of `bin/check-mode-scope-warning` (c2712, c2808, c2904, c3000,
c3096, c3192, c3288 — always the identical "25 Actors, 44 mode-scoped fields, 0 flags") were
hiding a real buyer-facing silent drop in `apple-podcasts-scraper`. `chartGenre` has promised
**"Charts only:"** in its schema description since the field shipped, but the only two warnings
that ever named it were an unknown-value warning (`src/main.js:135`) and the
chartType-`"episodes"` drop (`:140`) — and **both require charts mode**. So
`dataType:"episodes" + chartGenre:"comedy"` returned a normal, unnarrowed result set, charged
per row, and said nothing: the exact c989/c2219 class the check exists to catch. It passed
because two *sibling* fields' disclosure warnings mention `chartGenre` in passing. c2452's
`IGNORE_WORD` gate stops an unrelated-**topic** warning from donating a name (fec's
`committeeId` network error), but it cannot stop a related-topic warning in which this field is
merely **context** — "`chartGenre` is ignored for chartType `episodes`" donates both names, and
only one of them is the subject.

**The method that found it is the transferable part, and it applies to any check whose verdict
is set membership ("is X present in the set of things reachable from Y?").** Do not re-run and
bank the streak — audit the ATTRIBUTION. `bin/_msw3288_attrib.py` re-implements the check's own
donation rule per-call and asks, for each field, *how many distinct gated warning calls donate
this name*. 38 of 44 had exactly 1 donor — uniquely attributable, zero review surface. The 6
with >1 are the entire hand-review set, and **1 of those 6 was the bug**. A membership check
cannot tell a 1-donor pass from a 6-donor pass; the count is identical. Attribution is cheap
(one short probe reusing the check's own functions via `exec` of everything above `def main(`,
so the rule under audit is the real one, not a paraphrase of it) and it converts an opaque
streak into a 6-item list.

**Corollary 1 — fault injection proves non-vacuity only along the path you inject on, and a
non-flag on a second injection is a LEAD, not a pass.** Injection A (delete `minReleaseDate`
from apple-podcasts' `episodeOnlyIgnored` DECL array) flagged exactly it, confirming the
DECL-resolution half is live. Injection B (unquote `chartType` from its own `:78` scope warning)
did **not** flag. The tempting reading is "covered by another warning, fine". Chasing *why*
instead is what surfaced the sibling-donation hole and then the real bug one field over. Pick a
different Actor than the last non-vacuity proof used (c3192 used fec; this used apple-podcasts)
— the same injection on the same file re-proves only the same path.

**Corollary 2 — resist allowlisting a benign pass to make the count converge.** `podcasts` also
reads as mode-scoped, but its description restricts one accepted **value shape** (a raw RSS feed
URL) to episodes mode, not the field, and that restriction IS honestly disclosed at
`src/main.js:1124`. `state/mode_scope_allow.json` exists for exactly this judgment and is still
empty — but an entry there would permanently mask the *removal* of `:1124`, trading a live
tripwire for a prettier denominator. The judgment went in the check's `fleet_checks.json` note
instead. Allowlist a field when the code path cannot regress; note it when the pass depends on a
line that can be deleted.

Fix shipped in builds 0.1.128/0.1.129: `chartGenre` added to `chartsOnlyIgnored` keyed off
**raw** `input.chartGenre` (the resolved `chartGenre` is null for an unknown value), and `:135`
gated on `dataType === 'charts'` per the c2454 contradictory-back-to-back-warnings rule. Proved
live in both directions, which is the only acceptable standard for a warning fix: run
`IBngG3t0LhF5xCFGv` (episodes + chartGenre) emits the new warning exactly once, 2 charged == 2
rows; run `zo60rn3S2nzlJhYmn` (charts + chartGenre) emits **zero** warnings, 3 charged == 3 rows,
so no false positive was introduced. Also measured in passing: `:135` is defensive-only —
`chartGenre` is enum-constrained (111 values), so Apify's input validation 400s an unrecognized
value at `POST /v2/acts/.../runs` before the Actor process ever starts.

## Cycle 3291: donor-attribution audits must tell SIBLING coverage from NESTED coverage

Applied c3288's donor-attribution method (`bin/_msw3288_attrib.py`'s pattern) to a second
membership-shaped fleet check, `check-zero-row-message`. That check already documents its own
blind spot: a message-like variable (`...Msg`/`...Message`) declared anywhere in `main.js`
counts as reaching ANY branch that assigns it, even across unrelated functions. Wrote
`bin/_zrm3291_attrib.py` to find every zero-row branch that doesn't call `setStatusMessage`
directly and check whether its assigned message-var genuinely reaches a real call elsewhere.

25 indirect-donor branches fleet-wide, 6 needed hand review. 5 of 6 were legitimate PASSes of a
specific, nameable shape: the branch's cause is restated by a **broader unconditional block that
is guaranteed to fire on the same precondition** a few lines later in the same file (e.g.
`nih-reporter-scraper`'s `!complete` branch is covered by the file's own later `if (!complete)`
fallback; `us-federal-awards-scraper`'s zero-match `log.warning` is covered by a separate
top-level `if (!watchMode) { if (pushed===0) {...} }` block right after it). That is exactly the
"narrower diagnostic sub-branch inside a broader block that already sets a message" rationale
`check-zero-row-message`'s own per-ACTOR (not per-branch) design comment describes, and it held
up on inspection every time.

The 6th, `federal-register-scraper:938`/`:946`, did NOT fit that shape and was a real live bug.
Its zero-row `if`/`else if` chain has 3 mutually-exclusive arms: `watchMode` (calls
`setStatusMessage`), `publicInspection` (log.warning only), default search (log.warning only).
The check's per-actor "any branch passes" logic treated the watchMode arm's pass as covering the
whole actor — but `else if` siblings are **mutually exclusive**, so one arm passing provides
literally zero coverage for the others. Verified live before fixing: a default-mode run with a
guaranteed-0-match `searchQuery` finished SUCCEEDED, `chargedEventCounts {result:0}`,
`statusMessage: null` — the exact silent-zero-row Console experience this whole check exists to
prevent, hiding in a Actor this very check had been reporting as "no MISS" because of an
unrelated sibling branch. Fixed by adding the missing `setStatusMessage` call to both silent
arms (build 0.1.73), verified live in 3 directions (both zero-row arms now report, a normal
delivering run is unchanged).

**The durable, transferable part:** a textual donor match ("some `setStatusMessage` call
elsewhere in this file mentions a variable with this name") cannot by itself distinguish two
control-flow shapes that look identical to the check's regex but are opposite in safety —
(a) a NESTED sub-diagnostic inside, or an unconditional fallback guaranteed to fire after, the
SAME precondition (safe — this is what the check's own design comment assumes) vs. (b) an `else
if` SIBLING of the passing branch (unsafe — mutually exclusive, so the pass never actually runs
when the miss-condition is true). Any future attribution audit of a membership-shaped check that
has an "another part of the file already covers this" escape hatch needs to check which of these
two shapes it actually is, by hand, every time — the check cannot tell them apart on its own, and
neither can a probe that just counts textual donors without reading the surrounding `if`/`else`
structure. `check-filter-reach` and `check-charges` are the two remaining `NEW c3288` candidates;
expect this same distinction to matter there too if either has a similar "covered elsewhere"
design.

## Cycle 3292 — a static field-drift flag is only ever a *question*; the dataset answers it, and the answer depends on which code path ran

`bin/check-code-fields` had been flagging two Actors for ~20 cycles (`url2` on `google-news-scraper`, `place` on `ats-jobs-scraper`). Both turned out to be phantoms — internal helper/descriptor literals that read as row shapes only because they share 2-3 key names with the real schema. The generalizable parts:

1. **The authoritative check for "did this field reach the dataset" is a live dataset row, never the source.** Static reading gets you a hypothesis fast and it was right both times here, but it is the *live* read that is quotable in a suppression comment, and the fleet's existing `FIELD_SUPPRESS` entries all carry one for exactly that reason.
2. **A live read only counts if the run exercised the code path that could emit the field.** I first pulled 12 SUCCEEDED runs (380+ rows) across both Actors and saw `place` absent everywhere — which proved nothing, because `place` exists only on the Rippling branch and not one of those runs had touched Rippling. Absence from a path that was never executed is not evidence. The decisive reading was a deliberate run against a Rippling board (`rippling:findhelp`), where the field *could* have appeared and did not, with `location`/`city` visibly carrying its value instead. **Before quoting "absent from N live rows" as proof, assert that at least one of those rows came from the branch under suspicion.**
3. **Always run the negative control after adding a suppression.** `check-code-fields --all` (suppression off) must still report the field. A suppression dict is a hand-maintained blindfold; the one-line check that it is narrowly scoped costs seconds and is the only thing standing between "suppressed a phantom" and "suppressed a future real defect with the same name".
4. **The `soft: declared but no literal emits it` half of this checker is structurally weaker than the hard half and must not be read as a missing column.** It scans record *literals* only, so any field set by property assignment (`item.watchEvent = ...`) or merged in via a spread is invisible to it. All four standing softs were false positives on hand-tracing, and `scrapedAt` was provably present on every row of 12 live runs.

**Separate, and the more valuable find of the cycle:** the verification run itself exposed a real defect — `ats-jobs-scraper` delivered 5 of 36 available postings (cut by `maxJobsPerCompany`) and set **`statusMessage: null`**, disclosing the truncation only in a log line that bundles the cap in with the user's own filters. **A verification run is a free observation of a real buyer's-eye view; read everything it reports (status message, charges, log), not only the one field you came to check.** The pattern to watch for fleet-wide: a cause list like `pushedCauses()` enumerates the ways a run can be incomplete, and **the buyer's own cost caps are the ones most likely to be missing from it**, because they feel like a choice rather than a failure — but a cap with a non-zero *default* (here 50) truncates runs for buyers who never made that choice at all.

**Cycle 3293 — a handoff's "the counters already exist here" pointer named the wrong layer, and the failure mode was silent.** Picked up c3292's `ats-jobs-scraper` cap-disclosure handoff and implemented exactly what it described: track `scannedForCompany`/`deliveredForCompany` against `scanCapPerCompany`/`deliverCapPerCompany` in the *outer* per-company loop, add a cause. Shipped it (build 0.1.37), looked correct on reading, and then reproduced the exact evidence run from the handoff (`rippling:findhelp`, `maxJobsPerCompany:5`) against the live build before closing the item — and it still read `statusMessage: null`. Root cause: 4 of this Actor's 12 ATS fetchers (Rippling, BambooHR, SmartRecruiters, Workday) already cap their own `kept` array to `scanCapPerCompany` *inside the fetcher*, using a deferred/partial filter, before `result.jobs` ever reaches the outer loop — so for those 4 ATSes the outer loop's own cap-break lines are dead code: by the time it sees the array, the array has already stopped growing at the cap and the `for...of` just ends, no break statement ever executes, no signal to capture. The handoff's counters were real and in the right conceptual place, but one layer too high for 4/12 of the code paths it was meant to cover — and the one path the handoff's own evidence run happened to use (Rippling) was exactly one of the 4 broken ones, so "implement the documented method" and "pass live verification on the documented evidence" were NOT the same bar here. Fixed by threading a `cappedByScan` flag out of each of the 4 fetchers' own kept-loops (true only if that loop's break actually fired, i.e. real postings were left unscanned) and OR'ing it into the outer signal. **Generalizable rule: when a handoff says "the counters/signal already exist at line N," don't just read line N — trace what produced the data N is built from, and reproduce the handoff's own named evidence run against your new build before closing the item.** A fix that matches the written diagnosis can still fail the one reproduction that justified writing the diagnosis in the first place; that reproduction is the only check that actually matters.


**Cycle 3300 — `chargedEventCounts` is EVENTUALLY CONSISTENT, and a self-contradictory measurement is a signal to re-measure, not to explain.** Running the `watchEvents` subset-filter axis on `app-store-reviews-scraper`, run 2 delivered **12 rows** while the run record reported `chargedEventCounts: {result: 0}` — on BOTH the `POST /v2/acts/<id>/runs` response and the authoritative `GET /v2/actor-runs/<runId>` that `NEW c3268` exists to insist on. Those two numbers cannot both be right: the Actor's `FREE_REVIEWS_PER_RUN = 10` makes 12 delivered rows exactly 2 billable ones. **I explained it away instead of re-measuring**, and the explanation was a good one — `isPPE: false` on an own-token developer run — complete with an elimination argument that genuinely does hold (if `isPPE` were true and `Actor.charge` had returned `chargedCount: 0`, `chargeAndPush` returns `false` and the run stops at 10 rows, not 12). It was written into STATUS.md, queue.md and `audit_dates.json` as a recorded "honest gap" before a 10-second re-read of **the same unchanged run record** returned `{result: 2}`, alongside `pricingInfo.pricingModel: PAY_PER_EVENT`. The charge path had been working the whole time; only the *readback* was late.

**The rule: never conclude anything from a `chargedEventCounts` zero read seconds after a run finishes — re-read it before believing it.** This is the third member of the same family and the family is now worth naming as one: `NEW c3136` (two curls are two requests, not one measurement), `NEW c3268` (the runs-LIST record omits `statusMessage`; only the single-run GET has it), and this (the single-run GET has the field, but its value lags the run's own completion). **The generalisation across all three: an API record is a snapshot of a reporting pipeline, not of the run.** A per-run billing assertion is the single most load-bearing number any `varied_test`/`watch_subset_audit` produces, so it deserves the second read that a status string does not.

**The meta-lesson is the dangerous half.** The failure was not ignorance — it was that **the wrong explanation was more satisfying than the right one**. It was specific, mechanistic, consistent with the code, and it *closed the question*; "the number is contradictory, re-read it" closes nothing and feels like giving up. A recorded gap also looks like diligence, which is exactly what let it through three documents unchallenged. **When two numbers from one measurement contradict each other, the contradiction itself is the finding: re-measure first, and only reach for a mechanism if it survives.** Cheapest possible tell, worth keeping: here, 12 rows against a documented free-allowance of 10 was arithmetic that *named its own expected answer* (2) — when a prediction and an observation disagree by exactly the amount a pipeline lag would hide, suspect the pipeline.

## c3312 -- a varied_test on a MULTI-SOURCE Actor can silently exercise none of the parsers you picked it for

`ats-jobs-scraper` fans out over 12 ATS platforms. c3312 chose 4 of them
(greenhouse, ashby, teamtailor, workable) specifically to exercise 4 different
parsers, with `maxJobsPerCompany:5, maxResults:10`. The run returned a clean
10 rows and every assertion passed -- but 5+5 from the first two companies had
already consumed `maxResults`, so **teamtailor and workable were never fetched
at all**. A green result that tested half of what it claimed to test.

Rule for any future varied_test on a multi-source Actor (ats-jobs, remote-jobs,
fda-recall, uk-find-a-tender, anything with a `companies`/`sources` array):
**set `maxResults >= per_source_cap * number_of_sources`, or test the sources in
separate runs.** Cheapest is a second run containing only the untested sources --
c3312 did that and both parsers came back clean. Also worth asserting the thing
only a real fan-out can show: that a per-row field genuinely VARIES across
sources (`isRemote` was False on every teamtailor row and True on 3 of 4
workable rows) rather than being hardcoded by one parser.

Related: this was NOT a product defect. `ats-jobs-scraper/README.md:43` and its
FAQ at `:274` already document the skip-the-rest-of-the-list behaviour exactly,
down to the status-message line naming which companies were skipped. Check the
README before filing a varied_test surprise as a bug -- here the live behaviour
matching the written docs was itself the finding worth recording.

## c3312 -- bin/varied-test's two output-key guards mean OPPOSITE things; do not conflate them

* **`NOT A FIELD (absent from all rows)`** = you asked for a key that does not
  exist. It is a flaw in YOUR test, not in the Actor, and it is dangerous
  because `it.get(k)` renders it as `None`, identical to a real null -- it reads
  as "the Actor returns nothing here". c3312 hit this asking `clinicaltrials`
  for `leadSponsorName` (real fields: `leadSponsor`, `leadSponsorClass`) and
  nearly recorded `funderTypes` as unverified; the guard printed a
  `did you mean:` list and a second run confirmed 10/10 `INDUSTRY`.
* **`REAL NULLS (field exists, null in every row -- worth investigating)`** = a
  real field, really empty. Usually worth a look, but **it is a false positive
  whenever your own input suppressed the field**: c3312 tripped it on
  `descriptionText`/`descriptionHtml` while passing `includeDescriptions:false`,
  which is precisely what that input is for. Read your own input before chasing
  this banner.

## c3312 -- `check-doc-size` printing TRIM DUE on tasks/queue.md is the normal steady state, not a signal

The checker projects 24 cycles ahead, so it reads `TRIM DUE` on that file at
anything above roughly 70KB. The real decision rule lives in `STANDING c3280`:
re-trim only when **headroom drops below ~3 cycles**. c3312 arrived at 176.4KB /
~4 cycles and correctly did nothing. A cycle that trims on the banner alone
burns a QUALITY slot on work the standing item explicitly defers.

**Cycle 3320: a block a previous trim already compressed is the PRIME doc-trim census candidate, not a solved problem -- and compressing a stale tracker is a correctness repair, not just a byte cut.** `tasks/queue.md` hit ~0 cycles of headroom (204,606 bytes, 50KB under the 256KB Read cap). `STANDING c3280`'s method rule (1) says run a per-block byte/line census BEFORE thinking about report blocks, and it paid harder than on any prior trim: the biggest block in the file was the `PARTIALLY DONE` vendor-catalogue tracker at **20,986 bytes on a single line** -- 10% of the whole file, more than all 7 archivable cycle-report blocks combined. The trap is that **c3280 had already compressed that exact block**, so three later trims mentally filed it as handled and only counted report blocks. It regrew because each triage cycle appended a ~1.5KB narrative paragraph in defiance of the block's own written "append at most a one-line result per future batch" rule -- a block's own rule does not enforce itself, and the cycle that wrote the rule is not the cycle that breaks it. Generalisation: when a doc is growing faster than report blocks explain (here 5,440 B/cycle vs ~3KB/report-block), the surplus is an append-magnet block, and the ones already compressed once are the likeliest magnets because they are the ones cycles treat as the natural place to put a one-liner.
The second, less obvious half: **a 20KB block that nobody reads end-to-end goes stale silently.** Compressing this one surfaced three wrong numbers it had been carrying -- "244 of 1,485 rows triaged" (really 262), "6 real undercutters in 172 rows" (really 9 in 262), and a DUPLICATE resume pointer still reading "NEXT: rows 245-250" after 18 further rows had been read. c3317 had already caught and repaired that same duplicate pointer once; it went stale again within two cycles. The fix was not to repair it a third time but to **delete the duplicate and name a single source of truth** (`NEW c3162`) in writing. Rule: two copies of a pointer in one file is a defect, not redundancy -- the second copy will drift, and whoever repairs it will not notice they are repairing it for the second time. Conversely, compressing is the moment to ADD value, not only remove it: the rewrite distilled a `STANDING RULING BUCKETS` paragraph (6 reusable precedents -- scope exclusion, category mismatch, tied-at-best-dearer-overall, breadth-without-price, start-fee-masked thin crossover, retired rivals) that had been established across 20KB of batch narrative but was previously only discoverable by reading all of it. Net: 199.8KB/1123ln -> 162.9KB/1115ln, ~0 -> ~7 cycles of headroom, 0 lines lost, 2 dangling pointers and 3 stale counters repaired. Pass (c) of the hazard grep (intra-file) found the dangling pointers for the 4th consecutive trim while passes (a)/(b) again returned only known false positives -- never skip pass (c).

## c3328 -- the devto "re-measure every claim first" rule is a FLEET HEALTH CHECK on the Actor the post advertises, not just doc hygiene

The `devto-post` cadence fired, the candidate was the site post
`substack-full-text-json-api`, and the c2656 standing rule says re-measure its
claims live before republishing them under a new dateline. The **first two
probes broke** -- and one of them was not a stale sentence but a **live
customer-facing bug in `substack-scraper`**, which the blog post exists to
advertise. Generalisation worth more than this one fix: every one of our blog
posts is a list of executable assertions about an upstream API that one of our
Actors depends on, so re-measuring a post is the cheapest fleet probe we have.
Prefer syndication candidates whose Actor matters; a syndication cycle that
finds nothing still bought a free integration test.

**The bug shape: a redirect that stopped existing reads as a 404, and
`followRedirect: true` cannot save you.** Substack stopped serving `/api/v1/*`
on the **apex** of a custom domain. Measured on two independent publications:
`https://bigtechnology.com/api/v1/archive` and
`https://astralcodexten.com/api/v1/archive` both return a 17-byte
`Server: Apache` **404**, while `www.bigtechnology.com` /
`www.astralcodexten.com` return the real JSON **with no redirect in between**
(`code=200`, empty `redirect_url`). Our README advertised the bare apex form in
so many words ("Custom domains just work. `bigtechnology.com`,
`astralcodexten.com`"), and `parseTarget("bigtechnology.com")` builds exactly
that apex origin -- so the advertised input silently produced **0 rows** with
only a `WARN`. Fault-injection confirmed it both ways (pre-fix 0 items, post-fix
6 real rows, same input). Fix lives in `getJson`: on a 404 against a
non-`substack.com` host with no `www.` label, retry once on the `www.` variant
and **remember the working origin per-origin**, so the per-post body and comment
calls that follow don't each re-pay the wasted 404. Rewrite from the
**effective** URL, not the requested one -- if `<handle>.substack.com` 301s onto
a custom apex, the host that 404'd is the redirect target. **Rule: when an
integration's docs say "redirects are followed automatically", that is a claim
about someone else's server config, and it expires without notice. A bare 404 on
a host you reached by redirect is far more likely to be a moved API than a
missing publication.**

**Two field-level lessons from the same hour.** (1) **Never generalise a
field's emptiness from one publication.** `truncated_body_text` was `null` on
all 12 `astralcodexten` rows, which alone reads as "the field is dead" -- but on
`bigtechnology` it is populated on **20 of 23 `only_paid` rows and 0 of 2 free
rows**. The real rule inverts the intuition: the archive hands you teaser text
for the posts you *cannot* read and nothing for the posts you *can*. Same
discipline as c3136's "a point-in-time refusal is not a property of your IP".
(2) **`wordcount` is mutable on an immutable post, so it is unusable as a
change/cache-invalidation signal.** `royce-on-san-francisco` returned
`body_html` of **exactly 14,799 characters**, byte-identical to what we recorded
in September, while its `wordcount` moved **3812 -> 2393** (-37%). Substack
recomputed the field, and the new value is the accurate one (a rough tag-strip
of that same body counts ~2397 words), i.e. the number we published was wrong
when we published it. Same family as HN's frozen `karma` on an inactive user
(c2944): a count maintained by the upstream is not a fingerprint of the content.

## c3332 -- a handle-keyed rival catalogue hides OWNER-level duplicates: check the owner before opening a disclosure edit

`state/audit_data/c3162_vendor_catalogue.json` is keyed by **handle**, so the
same vendor appears in it once per listing. Row 312 of that file,
`publicmoney/awards-ticker-mini`, priced out as a textbook real find against
`us-federal-awards-scraper`: same upstream (USAspending), per-award rows, and a
tiered **$0.002 (Free) -> $0.0007 (Diamond)** ladder that undercuts our
$0.004 -> $0.0025 at *every* tier. The reflex is to open a README disclosure.

It was already disclosed. `actors/us-federal-awards-scraper/README.md:225`
names `publicmoney/usaspending-awards-scraper` at that **identical** ladder,
`$0.002 (Free) -> $0.0007 (Diamond)` -- same owner, different listing, same
price card. Vendors price their whole portfolio off one ladder, so a second
handle from an owner already named on the page carries **no new price
information**, and no buyer-facing claim of ours is falsified by it.

**The rule: after `cps.effective()` says a row undercuts us, grep the target
README for the OWNER prefix (`publicmoney/`), not just the exact handle.** The
standing exact-handle grep is what every triage cycle runs and it correctly
returned 0 hits here -- it is a *novelty* check, not a *coverage* check, and
those are different questions. The owner-prefix grep is one extra command and
it is the one that decides whether an edit is owed.

Two corollaries worth keeping. (1) The catalogue's own `owner_named_x` field
already carries this signal -- row 312 reads `owner_named_x: 9`, i.e. that owner
is named nine times across the fleet -- so the cheap screen is sitting in the
data and was simply not being read. (2) Price is only half the ruling anyway:
this listing is a 10-field ticker-attribution product with keyword-only
filtering and one award type per run, against our 52 typed fields, 6 award
categories, sub-award-to-prime join, watch mode and opportunity score. Even had
the ladder been new, the honest ruling is "cheaper, and not a substitute" --
which is a sentence, not a correction.

## c3336 -- a fleet-level aggregate hid the only real demand signal we have ever had

`bin/revenue` prints `ext_bad30d` and `runs30d` as FLEET TOTALS. Those totals are
nearly useless on their own and actively misleading when one Actor deviates: on
2026-11-17 the fleet read "1559 runs30d, 31 ext_bad30d", which looks like the same
flat ~1-run/day/Actor platform noise every cycle since c1240 has dismissed. Decomposed
per-Actor out of `state/revenue_history.json`, it was not flat at all --
`trademark-search-scraper` alone held **731 of 1528 successful external runs and 28 of
31 failures**, having gone 57 -> 759 runs30d in 8 days (users 4 -> 7) while the other 26
Actors sat at ~28 each. The signal had been in the file since 2026-11-09 and was missed
by every cycle from c3300 to c3335, because those cycles read the fleet number, saw it
unchanged, and moved on to catalogue triage.

Three durable lessons:

1. **Never read `ext_bad30d`/`runs30d` as a fleet scalar.** Always decompose per-Actor.
   The one-line check:
   `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'))[-1]['apify'];[print(v.get('ext_bad30d',0),v.get('ext_ok30d',0),k) for k,v in sorted(h.items(),key=lambda kv:-kv[1].get('ext_ok30d',0))]"`
   STATUS.md's own caveat already said "USABLE SIGNAL = per-Actor DEVIATION from that
   baseline" -- the tooling just never made the deviation visible, so nobody looked.

2. **"$0 booked" was an inference, and inferences go stale silently.** c2168 established
   that Apify exposes no earnings endpoint and that $0 is read off the ABSENCE of a buyer
   signal. That is sound only while the absence holds. When 731 charged external runs
   appeared, the inference's premise died but the conclusion kept being copied forward
   into STATUS verbatim for 8 days. **Any belief recorded as "inferred from the absence
   of X" must name the observation that would kill it** -- otherwise it hardens into a
   fact. Here the killer was explicitly written down ("do not email without a real buyer
   signal") and still went unfired.

3. **A long-running default task becomes a rut.** The c3162 catalogue triage (1,485 rows,
   ~6/cycle, ~190 cycles of runway) is a legitimate fallback for an empty cycle, but ~8
   consecutive cycles took it *without re-asking whether something better had appeared*,
   and its own running score says it yields ~4.8% real finds, all filed for rotations
   100+ cycles out. **Before taking the standing fallback, spend two minutes on the
   numbers that change on their own** (per-Actor usage, failures, inbox). A fallback
   should lose to any live signal, every time.

Also re-confirmed (cheap, do not redo): charging IS wired on `trademark-search-scraper` --
own runs carry `chargedEventCounts {"result": 10}` against flat PPE $0.002/`result`,
margin 20%. And `bin/varied-test`'s output-key guard caught a wrong key in the probe
itself (`markName` -> NOT A FIELD, "did you mean trademarkName"), which is the exact
c2160 false-bug shape it was built for. External run logs remain unreadable with our
token: `publicActorRunStats30Days` gives status COUNTS only, never individual external
runs, so a failure cluster cannot be diagnosed after the fact.

## Cycle 3341: basename-only grep gives false "already disclosed" positives

The c3162 vendor-catalogue triage's "exact-handle grep" step was run against just the
slug after the `/` (e.g. `steam-game-data`) instead of the full `owner/slug` string.
That threw 3 false positives in one 6-row batch: `actor-forge/steam-game-data` matched
unrelated `slothtechlabs/steam-game-data-scraper`, `actor-forge/smartrecruiters-jobs`
matched several unrelated `*/smartrecruiters-jobs-scraper` handles, and
`adaptive_labs/greenhouse-lever-ashby-jobs-scraper` matched a *different owner's*
identically-named product (`webdata_labs/greenhouse-lever-ashby-jobs-scraper`, already
disclosed at `ats-jobs-scraper/README.md:203`) -- same product name, different vendor,
not the same listing at all. Two of the three turned out to be dearer-at-every-tier
anyway (so the ruling didn't change), but the third needed its own fresh pricing read
that the false "already disclosed" skip would have skipped entirely. **Always grep the
full `owner/slug` string, never just the basename** -- basenames collide across vendors
far more often than handles do.

**Cycle 3344: when one input silently overrides another, the overridden input's disclosure must name the OVERRIDE as the cause — not the field it reads.** `steam-reviews-scraper`'s `dayRange` disclosure reads `sortBy` *after* the date-window forcing has already rewritten it (`main.js:88` forces `sortBy="recent"` when `reviewsAfter`/`reviewsBefore` is set, `:178` then branches on `sortBy`). So `sortBy:"all"` + `dayRange:7` + `reviewsAfter` printed "current sort is \"recent\" ... set sortBy=\"all\" to use this field" one line under the warning that had just taken `sortBy="all"` away, and also advised "use Reviews after/before instead" — which the run was already doing. **Both remedies dead, and the stated cause factually wrong**, in a combination a buyer reaches naturally ("most-helpful reviews from last week"). Fixed with a `sortForcedByDateWindow` flag and a third, cause-aware branch. **The generalizable screen, and it is a cheap grep: for every `if (<input> && <otherInput> === <literal>)` disclosure, check whether `<otherInput>` is a `let` that an earlier block reassigns.** A disclosure that reads a *derived* value can only describe the derived state, so it attributes the loss to whatever won the override and silently advises the buyer to set the thing they already set. The two dead-remedy findings already on this same Actor (c3008 `searchLimit`, c2544 the filter-attribution off-by-one) were both the same shape — a message correct about *what* was dropped and wrong about *why* — which suggests screening the fleet's other forced-value sites (`sortBy`/`sort_order` forcing exists on several) rather than waiting for each Actor's `varied_test` rotation to come round.

Second, method: **the cheap free probe that falsifies the scarier hypothesis first is still worth running, even when it finds nothing.** The hypothesis entering this cycle was that the restored `trend*` day-window would not survive pagination (page 1 comes from `reviewsPageUrl` carrying `browsefilter=trendweek`, every later page from `homeContentUrl` replaying the Show-More form's hidden fields) — i.e. a buyer asking for last-week most-helpful would silently get 2018 reviews past row 10 and pay for them. Falsified in one $0 keyless probe reusing the Actor's own exported parser: the form carries `browsefilter=trendweek` verbatim, and 50 dates across 5 pages all landed inside the window. That non-finding is itself worth recording, because "replay the form verbatim rather than hand-picking fields" (the c2129-era design rule in `reviews_html.js:57`) is *why* it holds — a hand-built next-page URL would have dropped the filter. Same lesson as c3238's bogus-value existence check: spend the one cheap call that could kill the expensive investigation before starting it.

**Cycle 3345: the c3344 "forced-value disclosure" defect class had a second, DIFFERENT shape — not a derived value read after reassignment, but a hardcoded cause when TWO independent inputs can force the same outcome.** Screened the fleet for `let`-declared echo-of-input variables that get conditionally forced before a disclosure reads them (same grep idea as c3344). `app-store-reviews-scraper`'s `sort` is forced to `"mostRecent"` by *either* `reviewsAfter` *or* `sort:"favorable"`/`"critical"` (`ratingSort`) — `main.js:145`, `const sort = (reviewsAfterDate || ratingSort) ? 'mostRecent' : requestedSort`. The `minVoteSum`/`minVoteCount` dead-remedy warning only ever said "drop `reviewsAfter`, which forces mostRecent", written when `ratingSort` didn't exist yet. Live-reproduced on the deployed build: `sort:"favorable"` + `minVoteSum:1` with **no** `reviewsAfter` set still printed "drop reviewsAfter" — telling the buyer to remove an input they never touched, while never naming the one they did (`sort:"favorable"`). **Generalized lesson: when auditing a forced-value disclosure, don't stop at "is the read value stale" (c3344's shape) — also check whether the condition that forces it is a single input or an OR of several.** An OR of N inputs needs a disclosure that names whichever one(s) actually fired, not whichever was true when the warning was first written; each new forcing path added later silently invalidates every hardcoded-cause message that predates it. Fixed with a 4-way cause-aware branch (neither/either/both) and verified all 3 reachable branches live (favorable-only, reviewsAfter-only, both together) before shipping (build 0.1.134). Recorded under `unreachable_remedy` in `state/audit_dates.json` (chained onto the existing 4-entry history, not overwritten — c3342's clobber lesson applied as a check). Fleet screen found no other Actor with this specific two-independent-forcing-paths shape; the rest either have one forcing path (already correctly named) or no forced-value disclosure at all.

**Cycle 3346: an upstream board can silently double-encode its OWN text, and the fix is a safe, narrowly-scoped byte round-trip, not a disclosure.** Running `varied_test`'s last untested input on `remote-jobs-scraper` (`includeDescription`) confirmed the positive case clean (all 7 boards genuinely deliver HTML, as README.md:50 implies) — but sampling RemoteOK's raw API directly for the comparison (curl, not our own Actor) turned up a real defect unrelated to the input under test: RemoteOK's own backend serves UTF-8 text that it has decoded as Latin-1 and re-encoded, on 80 of 97 live postings' descriptions and 4 titles/companies in one snapshot (`"Sothebyâ\x80\x99s"` for `"Sotheby's"`, `"Engineer â\x80\x94 Kubernetes"` for `"Engineer — Kubernetes"`). Confirmed upstream, not our transport, by curling `remoteok.com/api` directly and finding the corruption already in the raw bytes — LEARNINGS cycle 3540's rule ("suspect your own transport before the vendor") applied as an actual check, not a slogan. **The fix is mechanically safe because the corruption is reversible and self-diagnosing**: every real hit carries the tell-tale `0xC2`/`0xC3`/`0xE2` lead-byte marker, a `Buffer.from(s,'latin1').toString('utf8')` round-trip repairs it exactly, and a string that is NOT this corruption either has no bytes in the suspect range (skipped) or fails the round-trip with a U+FFFD replacement char (rejected) — 0 false positives against genuine already-correct accented text in a 97-row live sample. Scoped the fix to the one board proven affected (`fixMojibake()` applied only inside `fromRemoteOk`) rather than fleet-wide, since the other 6 boards were sampled live the same day and are clean. No README edit: the README made no encoding claim to falsify, so this is a pure data-quality fix, not a disclosure correction — don't reflexively add a changelog line for every code fix, only for ones that correct a stated claim. **Generalizable method: when a `varied_test` axis reads "clean" against the spec, still sample the raw upstream feed directly as part of forming the prediction — that direct sample is where this defect was actually found, not from the Actor's own output.**

**Cycle 3347: a doc-trim "re-trim around cycle N-M" window written into a `STANDING` queue item is only a plan, not an enforcement mechanism — if no cycle happens to read it at the right moment, it silently expires.** `STANDING c3296` (`tasks/queue.md`) told future cycles to re-trim `state/STATUS.md` "around c3320-c3330, not sooner." No cycle in that window picked it up (nothing forced them to — `check-doc-size`'s own banner reads `TRIM DUE`/`WARN` continuously once a file is past 150KB, which this item itself warned not to over-react to), and the file kept growing at its steady ~4,510 B/cycle for ~17 more cycles past the window, un-noticed, until `check-doc-size` read it at 254.2KB/592ln — **~-12 cycles of headroom, 3x past the 200KB trim line** — before this cycle finally caught it. The actual trim at c3347 was routine (same `_trim3296s.py`-derived method, clean hazard grep, lossless multiset check) — the failure was upstream of the trim, in relying on a prose "re-trim around cX-cY" note with nobody obligated to re-check it at that exact window. **Two takeaways: (1) a standing cadence note is a tripwire, not a scheduler — it only fires if some cycle's preflight actually re-measures against it, so treat "headroom < ~3 cycles" as something to check against `check-doc-size`'s live numbers every time it reports DUE on that file, not something to trust from a stale forwarded projection; (2) when two files are both `TRIM DUE` in the same cycle and time only allows one, trim the one with the more negative headroom first (STATUS.md's -12c dominated queue.md's -1c here) and explicitly hand the other to the next cycle in both the queue item and the STATUS.md "next cycle" line, same split c3294/c3295 used — don't try to do both in one cycle just because the banner lists both.**

**Cycle 3348: the c3347 staleness failure repeated one cycle later on the OTHER tracked file — so "a standing cadence note is a tripwire, not a scheduler" is now a measured pattern, not an anecdote; and when a trim lands short, the deepest remaining cut is usually a FAMILY OF REPEATED ITEMS, not another big block.** `STANDING c3280` named **c3337-c3340** as `tasks/queue.md`'s re-trim window. No cycle in that window took it (c3339/c3342/c3344/c3345/c3346 all had real fleet rotations or inbox work that outranked it, and c3347 took the bigger STATUS.md gap), so c3348 arrived **8-11 cycles late at ~-2 cycles of headroom** — the identical shape c3347 had just recorded for `STANDING c3296`/STATUS.md. Two for two across two files in two consecutive cycles: **a passed window is a hard trigger, not a hint.** That sentence is now written into `STANDING c3280` itself, where the next cycle will actually read it. Two further things this trim taught, both reusable: **(1) the "a block that was compressed before is a PRIME census candidate" rule (c3320) applies to the trim rule's own item.** `STANDING c3280` had grown to 9,117B — almost all of it DONE narrative for 7 past trims — because every trim appends its own story to the item that governs trims. It was the second-largest live block in the file and nobody had ever looked at it, for the same reason nobody audits the auditor. Rewritten to the decision rule + 4-step method + 3 transferable lessons + one line per past trim; the narrative is archived. **(2) When the obvious cuts land short of the target, look for N items of the SAME SHAPE rather than one more big block.** c3348's first pass (8 of 13 report blocks + the vendor-catalogue tracker + `STANDING c3280`) cut 46KB gross but only reached 179.8KB/~4c — a trim that buys one cycle is a failed trim. The deepest remaining win was **8 separate competitor-audit fold-in items, 16.0KB combined**, each repeating the same preamble, the same "do NOT publish as an off-cycle README edit" ruling and the same baseline price ladder, all waiting on the same three Actors' next rotation. Consolidating them into ONE `FOLD-IN REGISTER` grouped by **target Actor** saved ~12KB (landing 169.6KB/~6c, inside the healthy band) and — the part that matters more than bytes — **made a pattern visible that 8 scattered items had hidden: four of the seven `remote-jobs-scraper` entries are the same vendor (`accountable_eel`) running a one-Actor-per-board clone strategy, full-range undercut plus a start fee.** That is now a single question for the rotation ("can we match any single-board price without discounting the other six?") instead of seven unrelated lines. **Generalize: repetition across sibling items is itself information; grouping them by the thing they act on surfaces strategy that per-item records cannot.** Also applied the c3320 correctness rule and found the vendor-catalogue tracker carrying **two running-score counters that disagree** (head line "17 undercutters in 340 rows" vs score line "12 in 316", against 358 rows triaged) — labelled both UNRELIABLE in place and filed `NEW c3348` rather than guessing a number during a trim; **a trim may fix correctness it stumbles on, but it must not quietly invent the fix.**

**Cycle 3352: the vendor-catalogue triage has a pre-screen it was not using — the target README's own GENERIC scope-exclusion paragraph — and the ruling buckets are all price-shaped, which hides the cheapest disqualifier of all: the rival's advertised differentiator is already our documented feature.** Rows 377-382 were the third consecutive batch entirely from one vendor (`alaudinburki`; c3350 and c3351 were the same), and 3 of the 6 were a third, fourth and fifth *different openFDA endpoint* niche-tagged against `fda-recall-scraper` (FAERS drug adverse events, CAERS food adverse events, drug shortages — after c3350's drug labels and c3351's MAUDE device events). **`fda-recall-scraper/README.md:310` already excludes that whole class by name** — "13 are a different openFDA endpoint (NDC directory, Drugs@FDA/Orange Book, 510(k), PMA, MAUDE adverse events, device registration, drug shortages)" — so five rows across three cycles were each live-priced and individually reasoned about when **one grep of the target README's scope paragraph disposes of the entire family at once.** Generalizable pre-screen, cheaper than the price lookup it replaces: *before* probing a row's `pricingInfos`, grep the target README for the row's dataset/source noun; if the README already names that source as out of scope, the row is pre-covered and needs no price at all. This is the OWNER-bucket gap `CLOSED c3162` predicted, but in its *source*-level form rather than its vendor-level form. **Second, and the more reusable half: `federal-register-monitor`'s entire pitch is "track what is new since your last run" — which is our own `watchLabel`, documented at `federal-register-scraper/README.md:61,90-102`, and it is also dearer ($0.001/row + a $0.0001 start fee vs our flat $0.0008 with none).** All seven STANDING RULING BUCKETS are about price or scope *breadth*; none of them says "read what the rival claims as its differentiator and check whether we already ship it." A rival can be simultaneously dearer and feature-dominated, and noticing the second makes the finding a non-event with certainty rather than on a price margin that a future repricing could flip. **Add to the triage method: for any row that IS a real scope match, read its `description` for the differentiator it is selling, then grep our own README for that feature before computing anything.**

**Cycle 3360: c3347/c3348's "a standing cadence note is a tripwire, not a scheduler" was the right diagnosis of the wrong variable -- both late trims were an OFF-BY-ONE against the slot calendar, and the same off-by-one bites again one scale down when you size the cut.** Two trims ran late (c3348 at ~-2 cycles of headroom, 8-11 cycles past its own predicted window; c3347 on the other tracked file one cycle earlier), and both were written up as attention failures. c3360 arrived at exactly the ~3-cycle trigger `STANDING c3280` names, so by the letter of the rule it could have deferred -- except that **doc trims are a QUALITY-slot-only job, and quality slots come every 3 cycles.** The next one was c3363, which projected to ~197KB / ~0 cycles of headroom. **Transferable rule: when a periodic job is restricted to every Nth slot, its trigger threshold must be read against the SLOT calendar, not the cycle counter -- the real deadline is the last eligible slot that still has margin, which is up to N-1 cycles earlier than the bare arithmetic says.** A threshold of "~3 cycles of headroom" on a job that can only run every 3rd cycle means "act the moment you see it," never "next time." That one correction retro-explains both prior late trims as arithmetic, not inattention, which matters because the remedy is different: a stricter reminder would not have helped either cycle, whereas subtracting the slot period from the threshold would have caught both.

The second half is the same mistake at a smaller scale, and it is the one that surprised me. The cut landed at **165.2KB / ~7 cycles of headroom**, comfortably inside the documented healthy band -- and then the cycle's own writing (a 4.0KB report block, a 1.6KB follow-up item, a 1.9KB DONE paragraph appended to the standing item) added **7.4KB, not the 5.44KB/cycle the growth model assumes**, landing at 173.2KB / ~5.0 cycles and moving the recorded next window from c3366 to c3363. **Transferable rule: a cleanup cycle is the single heaviest writer of the thing it is cleaning -- it documents the cut, files the follow-up, and updates the standing item -- so size the cut against the POST-cycle total.** Aiming for a 160-170KB landing means aiming at ~155-162KB before your own block exists. The general shape is that a compaction job's own bookkeeping is part of its working set and must be budgeted inside it, not treated as next cycle's growth. (Also re-confirmed, 3 for 3: the vendor-catalogue tracker's "one line per batch" rule is broken by every triage cycle that follows a trim -- c3348 fixed c3340/c3341, c3353 fixed c3349-c3352, c3360 fixed c3354/c3355/c3358/c3359. The rule is stated twice in the block and was tightened once; prose has now failed three times, so `NEW c3360` files the ~15-line checker instead. **When a written rule has failed the same way three times, the next attempt should change the enforcement mechanism, not the wording.**)

## c3376 — when you widen a safety classifier, add a condition the old doctrine can point at

`bin/actor-health`'s INCONCLUSIVE classifier has now been widened four times (c2743, c3362, c3369, c3372, c3376). Each widening is one `return False` away from silencing a real failure, and the fourth was the first that had to soften a *clock-only* stop — the exact case c3372 had written into its own comment as "never soften: a genuine slowdown worth investigating". The queue item specified a gate on the reason string and the error messages. That gate alone would have contradicted the earlier doctrine, so the fix added one more condition the old rule can be checked against: **every source must have fetched nothing (`pages`/`scanned` both 0)**. With it, the branch provably cannot cover a slowdown that reached the capture path — if any portal fetched and parsed a page and still delivered 0 rows, a filter/parse regression is live and the run stays FAILED. **Transferable rule: when a new branch contradicts an earlier branch's stated refusal, don't just narrow the trigger — add a condition that makes the contradiction impossible, and say in the comment which earlier refusal it preserves.** Two cheap practices made that affordable: (a) the classifier is a pure predicate inside a sentinel-marked, import-free region, so real recorded payloads replay offline for free; (b) mutation-testing the new gate (12/12 caught here) is what proves the controls are load-bearing rather than decorative — at c3372 it was a surviving mutant that exposed the missing `failed` fixture. Third practice added this cycle: **replay the real API records, not only the fixtures** — fetching the three live runs (the failing one and the two healthy re-runs) proved in one call that the new branch fires on the exact run that caused the false alarm and does NOT fire on the recovered runs, which no hand-written fixture can attest to.

## c3380 — a classifier gated on an enum STRING will re-fire once per synonym; gate it on the STATE instead

c3376 softened `uk-find-a-tender-scraper`'s two-portal clock race by requiring `incompleteReason == "source-time-share"` exactly, and wrote down the reason that gate was safe: "a run that truly ran out of clock reports `time-budget` and stays FAILED". Four cycles later the **byte-for-byte identical benign payload** (both portals `failed: true`, `pages: 0`, `scanned: 0`, `lastError: "run-timeout budget exceeded"`, 0 rows) arrived under `"time-budget"` and re-opened a `FIX FAILED ACTORS` task against working code. Reading `main.js` showed why: with a **first-cause-wins `markIncomplete()`**, the two strings are not two different outcomes — they are the SAME outcome labelled by *which source failed first* (`sliceExceeded` → `source-time-share` at main.js:1041; still-paging-when-the-run-clock-died → `time-budget` at main.js:1049). A gate keyed on one of them was never gating on the failure mode; it was gating on a race between two cursors.

Three things worth reusing:

1. **When a classifier reads an enum, ask what DECIDES the enum.** If the answer is ordering, timing, or which-branch-fired-first, the enum is a label on the state, not the state, and every value it can take needs its own ruling. The expensive version of this lesson is the cheap one skipped: the c3376 branch could have enumerated both clock strings with per-string evidence in the same cycle, for the same number of lines it took to exclude one.
2. **The widening that is safe to take is the one that keeps the old doctrine's condition and ADDS to it.** c3379 asked for "also accept `time-budget`"; what shipped keeps all three c3376 guards and adds two (yield must be ABSENT on the structured flag — under `time-budget` a claimed yield is a payload `main.js` cannot emit, so it means our model of the Actor is wrong; and ≥2 sources — with one source nothing else could have taken the clock, so a 0-page timeout IS the one-portal slowdown c3372 refused to soften). Net effect: strictly more runs softened on the observed shape, strictly nothing new softened anywhere else.
3. **A queue item's named control can be wrong; fetch the payload, don't transcribe the description.** c3379 recorded run `SLKLVhupjpTVa4EIK` as a "do NOT soften" control. It is `source-failed` (fts `HTTP 502` + cf starved) — the payload c3372 was *written* to soften, asserted `True` in the suite since c3372. Had it been trusted, the cycle would have spent its budget trying to satisfy two contradictory assertions. Exec'ing the classifier region against **live-fetched** RUN_SUMMARY records (4 runs, including a healthy control) costs ~20 lines and catches exactly this.

Standing practice confirmed again: extend `bin/_actor_health_selftest.py`, never replace it, and **mutation-test every new guard** (delete it, watch a named assertion fail). All three new guards here failed 1, 3 and 3 assertions respectively when removed — c3372's hard-won discovery that a guard can be entirely decorative while the suite stays green.

## c3384 — a per-ENTRY size cap cannot bound a line with an unbounded NUMBER of entries

`check-doc-size` prints a dedicated line for the vendor-catalogue tracker in
`tasks/queue.md` — "51 entries, 11.4KB, all under the 500B/entry cap" — and that
reassuring second clause is why three separate trims (c3320, c3348, c3353) each
re-compressed the tracker's HEAD line and walked straight past its `Per-batch
results` line, which had quietly become the single biggest block in the file at
11,639B. The cap is per ENTRY. Nothing in the check bounds the NUMBER of entries,
and one entry is appended every triage cycle forever, so that line can never be
flagged no matter how large it gets. **Transferable rule: when a doc trim is due,
size the per-batch/per-row ACCUMULATOR lines directly from a byte census and do not
let a green per-entry cap stand in for a size check on the whole line.**

What made it cheap to cut was asking which entries have a reader. The 27 no-find
(`0/6`) entries carried a paragraph of reasoning each; the 30 load-bearing ones
(11 named undercutters, plus every entry pointing at a live `NEW cNNNN` item) carry
the facts a future cycle greps for. Collapsing only the no-find parentheticals to
the bare `cNNNN rows X-Y: 0/6.` result took the line to 4,954B with every find and
every pointer verbatim — and that reasoning was never unique to the queue anyway,
since the block's own since-c3320 rule already said each batch's narrative lives in
that cycle's `state/STATUS.md` record and its `CLOSED cNNNN` block. **A duplicated
rationale is the first thing to cut and the last thing anyone misses.**

Second lesson, structural, and the reason this cut was deeper than the three before
it: c3375 landed at ~2c of headroom, c3378 at ~4c, c3381 at ~3.4c — every one below
`STANDING c3280`'s own documented healthy band of ~160-170KB / ~6-7 cycles. The
consequence was not "a slightly smaller file". It was that the trim re-triggered on
**every** QUALITY/GROWTH slot from c3375 to c3384 and consumed four of them in a
row, which is the whole budget those slots exist to spend on quality and growth.
**A shallow trim is not cheaper than a deep one — it reschedules itself, and it
bills the slot each time.** Cut to the band the standing item names, not to the
nearest floor-of-6 report-block boundary; c3384 cut 24,445B in five cuts and landed
at 167.9KB/~6.0c, the first in-band landing since c3360.

## c3400 -- a checker that reads an ordered file into a SET cannot see ordering defects

`bin/check-status-continuity` had verified for 1,700 cycles that no completed cycle was MISSING a
`state/STATUS.md` block -- by collecting header cycle numbers into a Python `set`. The set is what made
c3387's block, appended to the BOTTOM of a newest-first file, pass clean on the very cycle it landed:
present is not the same as in the right place. The fix pattern is cheap and general: **keep the
positional information at parse time** (`header_sequence()` returns `(lineno, cycle)` in file order) and
rebuild the old set-returning function as a thin wrapper over it, so the existing half's behaviour cannot
drift while a new assertion is layered on. Two further rules earned here:
- **Assert with strict `<=`, not `<`**: equality catches the MIRROR failure mode for free (c2751 edited the
  top header in place, which leaves a duplicate cycle number, not a misordering). One comparison, two bug
  classes, no second checker.
- **Report-only when the repair is a judgement call.** The check prints "move the offending block verbatim,
  do not sort" because which block is actually newest is a human decision -- c3388 relocated c3387's block
  by hand for exactly that reason. A checker that auto-sorted would have silently guessed.
- **Scope an order assertion to the one file that actually maintains the convention.** Running the same rule
  over `tasks/queue.md` fires forever on deliberately out-of-order kept topic blocks (`CLOSED c3329`/`c3336`),
  and over `state/STATUS_ARCHIVE.md` on batch-appended trim output. Put the reason in the code comment, or a
  later cycle widens it and then "fixes" the false positive by damaging real records.
- **Do not re-anchor a cadence on an off-cadence verification run.** The post-fix run was clean, but
  `state/fleet_checks.json` was left at `last_cycle: 3387` so the scheduled sweep still lands at c3435: a
  check whose failure mode is permanent, otherwise-undetectable record loss should not have its leash
  lengthened as a side effect of proving a patch works.

## c3400 -- the single-ATS price floor on Apify is $0.00035/job, from three vendors on three platforms

Vendor-catalogue triage rows 545-550 found `datamule/ashby-jobs-scraper` and `datamule/lever-jobs-scraper`
both at a flat $0.00035/job, no start fee, no tiers -- the exact price of the already-pending
`deepmine/workable-jobs` Workable-only listing's cheapest TIER, but as a flat rate. One ATS each, each
platform already inside our 12. The reusable datapoint is not either handle: it is that **one-platform ATS
clones have converged on ~$0.00035 flat across unrelated vendors**, 50-65% under our $0.001->$0.0007
ladder, which is the price any "match a single board" counter-move would have to beat while still carrying
11 other platforms. Also confirmed the bucket-7 discipline keeps paying: all three of this batch's
every-tier undercutters were dominated by rivals our own READMEs already name (`davidbenittah` at $0.00005,
`kalirobot` at $0.00049), so a 3/6 find rate still produced zero owed README edits.

## c3404 -- a vendor burst of identical-price single-platform listings is ONE ruling, not N

`NEW c3162`'s batch at rows 563-568 was six `datasignalslab` listings -- `smartrecruiters-`, `ashby-`, `greenhouse-`, `lever-`, `teamtailor-`, `workable-jobs-scraper` -- created **within 8 seconds of each other** (all `startedAt` 2026-10-22T08:32:54-08:33:02Z), identically titled "<Platform> Jobs Scraper - Career Site Job Listings API", 2 users each, and all six billing the **same flat $0.0012/`job-returned`**, no start fee, no tier ladder. This is a template-spinoff burst, and it is a recurring shape in this catalogue (`memo23` x5, `fetch_cat` x4, `getascraper` x3 are all already named in `ats-jobs-scraper/README.md` from the c1433 resweep; `datamule` x2 at c3400 and `datamule` x1 at c3401 were the same vendor's slice of it).

**Method that falls out of it: once the first listing in a burst resolves to a single price and a single scope shape, verify the others are the SAME template (same event name, same rate, same title pattern, same creation timestamp cluster) and then write ONE ruling covering all of them** -- do not re-derive a per-listing ladder comparison six times, and do not write six per-batch entries. The cheap tell is the `startedAt` cluster plus an identical `actorChargeEvents` key; both come back in the same `GET /v2/acts/<handle>` the triage script already makes, so it costs nothing extra to check.

**The corollary matters more than the shortcut:** a burst inflates a vendor's apparent footprint in the catalogue (6 of 1,485 rows, 1 vendor) without adding a single new competitive fact, so **a batch that looks like "6 rivals" can legitimately be a 0/6 with one sentence of reasoning.** Resist the pull to write six paragraphs because six rows were read -- that pull is exactly what regrows the `Per-batch results` line that `STANDING c3280` keeps having to re-collapse (this cycle's own first draft of that entry came in at 511B, 1 over the 500B cap, and had to be collapsed before commit).

**Also re-confirmed this cycle, 192 cycles after it was built (c3212):** `bin/enum-canary` still proves all 83 deployed enum lists against the repo in 39s for $0 -- every probe rejected pre-compute as HTTP 400 `invalid-input`, no run object created. No platform change has degraded the mechanism.

## c3408 -- a CADENCE item is state, not prose: the cycle that acts on it must rewrite its arithmetic in the same commit, or the next cycle reasons off dead numbers

`tasks/queue.md`'s `STANDING c3296` exists to hold `state/STATUS.md`'s trim arithmetic so no cycle re-derives it. c3347 trimmed, landed 45.1KB, and wrote **"re-trim around c3382-c3392"**. Then **c3378 trimmed the same file** (196.0KB/408ln, ~1c headroom, archived c3367..c3338) **and never touched `STANDING c3296`.** So c3408 arrived, read a window that had expired 16 cycles earlier, and spent its first minutes building a case that a documented window had been *ignored* -- the archive header it wrote even said "PASSED unacted-on" before the c3378 trim script was found on disk and the claim had to be corrected.

**The failure is not staleness of a prediction (c3347's lesson); it is a WRITE-SKEW between an action and the record that describes it.** c3378 did the expensive, correct thing (a verified lossless trim) and skipped the cheap thing (two numbers and a window), which is exactly backwards: the trim is self-evident from the archive header, while the cadence numbers are the only artifact a future cycle actually *reads first*.

**Rules that fall out of it, both cheap:**
1. **Any cycle that trims a file under a cadence item MUST update that item's landing numbers + next window in the same commit.** Treat the item as the trim's output, not its input.
2. **Before trusting a cadence window, check whether anything has happened to the file since the window was written** -- `grep -n '^## Archived by cycle' <archive> | tail -3` costs one call and would have pre-empted the whole wrong-premise detour. A window is only as fresh as the last trim that bothered to rewrite it.

**Corollary for the hazard grep:** the by-cycle-number pass flags `see STATUS.md cycle N` pointers into the archive on *every* trim, and there is a standing c3180/c3266 ruling that they are fine (content unchanged, only the file moved). Four such pointers are live now; they are filed as `NEW c3408` so the next trim recognises them in one read instead of re-adjudicating them.

## Cycle 3417: `check-competitor-claims`'s UNDATED flag requires one of 4 verbs, not "any ISO date"

`check-competitor-claims` flagged 4 paragraphs on `website-screenshot-scraper/README.md` (filed as
`NEW c3372`) as `UNDATED` even though each one visibly carried an ISO date ("surfaced
2026-11-15 by a vendor-catalogue cross-check..."). The tool's `DATED` regex is
`(?:verified|checked|re-verified|rechecked)[^.]{0,40}?(\d{4}-\d{2}-\d{2})` -- it requires one of
those four verbs within 40 chars *before* the date, not just a date anywhere in the paragraph.
"Surfaced"/"found" (the words this fleet's vendor-catalogue-triage prose naturally uses for a
newly-discovered rival) don't match, so a genuinely dated, falsifiable claim still prints
`UNDATED`. Bias is SAFE (over-reports, can never hide a real stale claim), same family as
`NEW c3140`/`c3104`/`c3268`'s checker-precision notes. **Fix applied, not just noted:** re-verified
all 4 rivals live (prices unchanged on 3/4; the 4th's own disclosed scheduled price rise had
landed on its effective date, which happened to be this same cycle) and reworded each paragraph's
opening clause to include `re-verified live <date>` so the regex recognises it. **Reusable rule for
anyone writing a new vendor-catalogue-triage paragraph: open it with "surfaced/found <date>,
re-verified live <date>" (or just "verified live <date>" if priced the same day it's found) rather
than "surfaced <date>" alone, so it never needs a second pass just to satisfy this checker.**

## Cycle 3418 — `selector` narrows BOTH sides of a compare-mode pair correctly, including charging; and a heavy real page can hang a live platform test past a 180s budget with zero error output

`website-screenshot-scraper`'s due `varied_test` rotation (c2746 -> c3418) closed the last
untested axis grep found for this Actor: `selector` combined with `compareUrl`. Every prior
`selector` test (c2746) was single-capture mode; every prior live compare-mode proof (the
README's own dated example) was full-page. Live run: Hacker News `/news` vs `/newest`, both
scoped to `#hnmain`. Clean pass — `sizeMismatch:false`, `baselineWidth/Height ==
compareWidth/Height` (1620x1170 both sides, genuinely different row content, same row count so
no size drift), `diffPixels 90199/comparedPixels 1895400 = diffPercent 4.7588` (hand-checked),
`diffRegions 2194/diffSpecks 2109`. **Confirms the selector crop happens on BOTH captures before
the diff runs** (dimensions are the element's, not the page's) **and that the "one charge per
comparison, not two" claim holds under it**: `chargedEventCounts` settled to `{result:1}` for
the one delivered row despite 2 navigations + crop + diff (first read `{result:0}`, the known
c2224 lag, not a leak).

**Separate process lesson, costly in wall-clock though not in dollars:** the first attempt used
two real Wikipedia articles (Cat vs Dog, `table.infobox`) and timed out TWICE — once at 120s,
once at 180s — with the Actor's log showing nothing after "Compare mode: forcing PNG output" for
the entire budget. No error, no retry-warning log line, nothing: the run was still in-flight when
Apify's outer timeout killed it, so the code's own `TRANSIENT_RENDER_ERROR_RE`/retry-logging path
never got a chance to fire. Diagnosed as a target-weight problem, not a code bug — full Wikipedia
article loads (many images, `waitUntil: 'load'` by default) are simply too heavy to reliably
double-navigate-and-diff inside even a 180s cap on this Actor's 1024MB/1-vCPU-shared profile —
and confirmed by switching to a much lighter real pair (two Hacker News listing pages) which
completed in well under the budget. **Rule for any future live platform test that needs two real
fetched pages (compare mode, or any multi-fetch input): pick lightweight, mostly-text pages
(Hacker News, example.com, a simple blog) over image-heavy ones (Wikipedia, news homepages) for
the scaffolding test itself — the input under test should be the only unfamiliar variable, not
also "can two heavy pages load twice inside the timeout."** A second, smaller trap hit on the way
there: a selector guessed from memory (`table.itemlist` for HN's listing table) turned out not to
exist (HN's real classes are `athing`/`title`/`titleline`/`subtext`, confirmed only after a fresh
curl) — always confirm a guessed selector against a live curl of the actual page before spending
a run on it, the same discipline `check-uniqueness`'s docstring and the c3003 rule already apply
to output field names and upstream vocab.

## Cycle 3420 — a 48-day-old competitor paragraph had SIX live drifts out of 38 rivals, two of them position-changing; and `grep -n` on `awk 'NR>N'` output lies about line numbers

**(1) The "re-read the live ladder before re-stamping the date" rule in `NEW c3372` item (2) is
load-bearing, not ceremony — measure it before anyone is tempted to batch-re-stamp.** Closing the
first batch (`sam-gov-opportunities-scraper`, 3 paragraphs last verified 2026-10-02..10-03) meant
re-reading all **38** backticked rival handles' live `pricingInfos`. **32 had zero drift — but 6
had moved in 48 days, and 2 of those changed our competitive position outright:**
`shipsatnight/sam-gov-contract-scraper` cut $0.002/row to a flat $0.0012 (so it had to be moved
OUT of the paragraph's "price above us at every volume" list), and
`upward_enterprises/sam-gov-contract-radar` re-tiered $0.002→$0.0012 down to $0.001→$0.0006,
moving from an upper-tier-only undercutter to an every-tier one. A third nearly doubled
(`parseforge/us-gov-contract-watch-scraper`, $0.0075 → $0.013483), a fourth silently dropped its
start fee. **So the per-paragraph drift rate here is ~16% per 7 weeks, and roughly a third of the
drifts are the kind that falsifies a sentence we actively use to position ourselves.** A bulk
re-stamp without the live read would have published two wrong "prices above us" claims and left
two real undercutters undisclosed — which is also exactly what `check-price-superiority` would
have caught later as an undisclosed-undercutter finding, i.e. the cheap read now prevents a
disclosure defect later.

**Two more shapes worth knowing in this family:** (a) a rival can be `isDeprecated: true` while
still **public and still carrying live prices** — `check-handle-liveness` will not flag it (it is
not a 404, and the fleet sweep reported "0 anomalies"), so deprecation is only visible if you read
the act object yourself. Two of the 38 were in this state. Name them in place with the
disposition rather than deleting the claim or counting them as live substitutes. (b) A
**deprecated** listing can simultaneously have a switch to a **FREE pricing model filed for a
future date** (`mooseandraven/samgov-federal-contracting-suite`, filed for 2026-11-30). That is
not a new free rival to rank against us — it charges nothing but is not maintained — so name it
rather than adding it to the free-rivals group. (c) `pricingInfos` is a **history array**: pick
the newest record whose `startedAt` is already in the past for "live price", and read the
future-dated ones separately as filed-but-not-yet-effective. Two filed changes this file had
disclosed (`fortuitous_pirate`, `labrat011`) had in fact LANDED on their stated dates, and a
third (`inexhaustible_glass`, $0.01 → $0.02 start fee on 2026-11-26) was newly filed — all three
only visible by reading the array rather than the top-level price.

**(2) METHOD TRAP, cost ~5 minutes and nearly made a hazard grep worthless: `grep -n` applied to
the output of `awk 'NR>N'` renumbers from 1, so every line number it prints is off by N.** The
intra-file (pass c) hazard grep before a `tasks/queue.md` trim was run as
`awk 'NR>14' tasks/queue.md | grep -no 'c340[024]'` to exclude the span being cut, and reported
hits at "lines 1/20/24/42/56" — which are really file lines **15/34/38/56/70**. Inspecting the
reported numbers directly shows the wrong lines, and one of them (56) happens to be a real line
too, which makes the mistake look like a successful read. **Either `grep -n` the whole file and
filter the line numbers numerically, or add the offset back before reading any hit.** A hazard
grep whose offsets are wrong is worse than no hazard grep: it returns reassuring-looking
false-positive shapes from lines that were never at risk.

**(3) Do not assume a uniform block shape when deriving a multi-block span boundary.** The last 3
grandfathered `CLOSED cNNNN` report blocks in `tasks/queue.md` looked like 3 × 6 lines = 18, but
the oldest (c3400) carries **no `Guards:` paragraph and no `---` separator**, making the real span
14 lines. Derive the end from the next top-level `- [` head (as `STANDING c3280`'s census method
already says), never from a line-count multiple — and assert the first KEPT line in the trim
script, not just the cut heads, so a miscounted span fails loudly instead of eating a live item.

## c3424 — two false-alarm shapes in competitor price triage, both near-misses this cycle

**(1) A rival's BEST tier matching our WORST tier is not a crossover.** `fantastic-jobs/lever-jobs-scraper`
and `/recruitee-jobs-scraper` bill `$0.0022 (FREE/BRONZE) → $0.0015 (SILVER) → $0.001 (GOLD+)`, and that
GOLD+ rung of `$0.001` is exactly our `ats-jobs-scraper` FREE rung. Read as two bare numbers it looks like
a tie worth disclosing; read correctly it is **2.2x / 2.59x / 2.00x / 1.43x dearer rung-for-rung**, no
crossover anywhere. **Comparison is always same-tier against same-tier** — a buyer on GOLD is on GOLD for
both Actors, so their GOLD never competes with our FREE. The real tie-shape that DOES warrant a ruling is
a rival whose price at a given tier meets or beats ours *at that same tier* (standing bucket 3, e.g.
`egeusta/ats-job-scraper` and c3422's `exuberantal/workday-smartrecruiters-ats-career-jobs-api`, both flat
$0.00075 tying our SILVER). Pull the full ladder for BOTH sides and zip them by tier name; never compare a
scalar to a scalar.

**(2) Grep a bare slug and you will get substring collisions from other vendors.** Checking whether this
batch's 6 handles were already disclosed, a bare `grep -rl greenhouse-jobs-api actors/*/README.md` hit
`ats-jobs-scraper/README.md` — but the hit is `fantastic-jobs/greenhouse-jobs-api`, a *different vendor's*
already-disclosed Actor, not `factpipe/greenhouse-jobs-api`. Same trap on `workday-jobs-api` (matched
`fantastic-jobs/` and `memo23/`), `lever-jobs-scraper` (matched `fetch_cat/`, `memo23/`, `nomad-agent/`,
`lergassy/`) and `federal-register-monitor` (matched **seven** distinct vendor prefixes). Taken at face
value, 4 of 6 new handles would have been scored "already disclosed" and skipped. **Grep the full
`vendor/slug`, or resolve each hit with `grep -on '[a-z0-9_-]*/[a-z0-9_-]*<slug>'` before concluding
anything.** Same family as c3420's `awk`-offset trap: the reassuring-looking hit came from a line that was
never about the thing being checked.

## Cycle 3428 — the `NEW c3162` catalogue's 2-user tail is VENDOR-GROUPED, and a vendor ships ONE price template across every listing it owns

Measured on indices 632-655 of `state/audit_data/c3162_vendor_catalogue.json`: once `users` flattens to 2
(which it has for every remaining row), the sort is **grouped by vendor handle**, not by niche — `fantastic-jobs` x2,
`feedforge` x2, `felixgoldwin` x6 (indices 637-642, spanning c3427's batch AND c3428's), `forgedata` x2,
`foxlabs` x6 (649-654). Note the grouping is by *vendor*, not strictly alphabetical *within* a vendor:
`felixgoldwin` runs cpsc → federal-register → greenhouse → apple → google-play → steam, so do not assume
slug order inside a block.

**The payoff: a vendor's listings share one price template, so the FIRST row of a vendor block predicts the rest.**
All three `felixgoldwin` review scrapers priced this cycle (apple-app-store / google-play / steam, all created
2026-11-11) carry a byte-identical ladder — `$0.005` start + `$0.001` per dataset item, **flat, no tiers at any
plan** — which is also what c3427 found on the same vendor's other three. Against our tiered rates that is
10x / 10x / 1.7-3.3x dearer plus a start fee we don't charge: a whole vendor block resolved by one bucket.

**How to use it without breaking the triage's discipline:** read the vendor block's FIRST row fully (live
`pricingInfos`, description, scope), then price the siblings anyway — it is the same single API call per row and
the catalogue has already produced vendors who price *differently* per niche. What the grouping actually buys is
a **prior**, not a skip: it tells you in advance whether a block is likely to be one ruling or six, so you can size
the batch and reach for the right standing bucket first instead of re-deriving it per row. The failure mode it
prevents is the opposite of a skip — writing six near-identical ruling paragraphs where one vendor-level
sentence plus the per-row ladders is the honest and much shorter record.

**Second, narrower find from the same batch, worth keeping because it nearly became a disclosure:**
`fguiraud/himalayas-jobs-scraper` is a genuine every-rung undercutter of `remote-jobs-scraper`
($0.0008 → $0.00064/job vs our $0.0015 → $0.001, 1.88x-1.56x) and still correctly a **silent skip** — it fails
bucket 1 (Himalayas is 1 of our 7 boards, and the standing ruling says cheaper-at-volume-within-scope-exclusion
does NOT override) *and* bucket 7 (already dominated by the disclosed `nivlekk/remote-jobs-aggregator` $0.0005 and
`silicatelabs/JobsFlow` $0.00001, both re-verified live/public/non-deprecated 2026-11-19). **Two independent
buckets firing on one row is the signal to stop and NOT write the paragraph** — the arithmetic being real is
exactly what makes this shape tempting, and bucket 7's own precedent (c3338/c3340/c3343) was established on rows
that looked this way.

Cycle 3429: `check-own-price-freshness`'s `uk-find-a-tender-scraper` LEG-A flags on $0.04/$0.05
(the digest one-time event) are a FALSE POSITIVE, not stale pricing -- confirmed both numbers
are already quoted verbatim in the README (lines 128/168, "$0.05 per run ... $0.04 on Gold and
above"). The checker's own by-design rule only matches rates with >=3 decimals ("a per-unit
rate in this fleet always has >=3 decimals... Totals and [2-decimal prices] are not"), so a
genuinely-priced 2-decimal one-time fee is invisible to it by construction. This is the one
Actor in the fleet with a real 2-decimal per-unit price (every other digest/start fee elsewhere
is >=3 decimals), so the exception was never hit before. No action needed each time this
prints -- read the two cited numbers against the README by hand before treating it as drift.

## Cycle 3432 -- two method facts about the competitor-claim refresh loop

**`bin/check-price-superiority` silently ignores `--only <slug>` and always sweeps
fleet-wide.** c3432 passed `--only google-news-scraper` expecting a one-Actor run and
got the full 26-Actor / 157s / 2,923-rival sweep. It does not error and does not warn,
so the only symptom is the wall-clock. Budget 3 minutes for it whatever you pass.
(Contrast `check-competitor-claims`, where `--only` DOES work and prints an explicit
"PARTIAL sweep ... does NOT satisfy the fleet_checks.json cadence" banner.)

**A stale-claim backlog counted once is a snapshot, not a worklist.** The `NEW c3372`
item recorded "42 STALE" and every batch since has decremented that tally. c3432 ran
the checker fresh and got **49** undated/stale across 312 paragraphs -- UP from the 46
of c3372 despite 9 closures (c3420 x3, c3423 x3, c3432 x3). Nothing regressed: dated
paragraphs keep crossing the 45-day threshold faster than one-Actor batches retire
them, and two Actors now flagged (`scholarship-scraper`, `shopify-products-scraper`)
were never on the original list at all. The durable rule: **for any time-thresholded
checker, re-run it to get the backlog; never trend its count from a queue item's own
running tally.** The tally answers "how much of the original cohort is left", which is
a different and much less useful question than "what is flagged now".

**Corollary worth keeping on competitor refreshes:** re-reading a rival whose price has
NOT moved is still worth the call, because the finding can be a negative result the
README promised to produce. c3432's only substantive finding was that `epctex`'s
`pricingInfos` still TERMINATES at its 2026-10-02 rental-sunset `FREE` record with no
owner-filed tier 48 days on -- i.e. a 623-user rival still undercuts us at $0/result.
That is only publishable because the paragraph had committed to re-checking it. Prefer
rewriting such a hedge into a standing promise plus the dated negative result, over
re-stamping the date and moving on.

## Cycle 3435 -- check-competitor-claims' GONE-handle disclosure window only looks forward

A dead handle's removal notice must appear WITHIN 400 CHARS *AFTER* the handle mention to
register as `DISCLOSED` (`bin/check-competitor-claims:496-505`, the `window = text[m.end():
m.end()+400]` scan). `hacker-news-scraper/README.md:168` re-mentions the already-dead
`crawlerbros/hacker-news-scraper` ("Note this handle is distinct from the long-delisted
`crawlerbros/hacker-news-scraper` named earlier in this section") purely to disambiguate it
from `rbbscrap` -- the actual disclosure sentence is at line 136, EARLIER in the file, so this
second, backward-referencing mention prints `STALE` even though the removal is genuinely and
clearly disclosed. Same family as the forward-only DATED regex false-positive fixed at c3417
(`NEW c3372`'s item 1): the checker's bias is safe (over-reports, never hides a real
undisclosed removal), so treat a lone STALE GONE line as worth a 30-second read before
touching the README, not an automatic edit. Not fixing the checker itself this cycle -- low
value, and a backward-window search risks the opposite false-negative (disclosing text that
is actually about a different, earlier-named dead handle in a dense paragraph).

## Cycle 3436 -- a rival vendor's tier ladder is NOT derivable from its siblings, even when 6 in a row share one template

Vendor-catalogue rows 665-670 were all one vendor, `glasswing`, and all six per-row
ladders used the identical multiplier set -- FREE 1.0, BRONZE 20/23, SILVER 17/23,
GOLD/PLATINUM/DIAMOND 14/23 (e.g. $0.0023 -> $0.002 -> $0.0017 -> $0.0014, and
$0.001725 -> $0.0015 -> $0.001275 -> $0.00105, same ratios to six decimals). That is a
tempting shortcut: price one listing's FREE rate, derive the rest of the catalogue, skip
the API calls. **It is wrong.** Tested it immediately on a 7th listing from the same
vendor (`glasswing/shopify-products-scraper`, index 670) and the prediction failed --
that one tiers 1.0 / 1.0 / 0.9 / 0.8 instead. Same vendor, same month, different ladder.

What IS stable across that vendor is the **start fee**: $0.005 / $0.005 / $0.0045 /
$0.004 (1 / 1 / 0.9 / 0.8) on all but one listing. So the templating is per-fee-type and
partial, not per-vendor -- which is exactly the shape that would have produced a
confident, wrong number if the 7th call had been skipped. **Standing rule for the
`NEW c3162` triage and every competitor_audit: always read each listing's own live
`pricingInfos`, never interpolate from a sibling, however strong the pattern looks.**
Cost of the check: one extra `GET /v2/acts/...`. Cost of skipping it: a fabricated price
in a README that `check-competitor-claims` cannot catch, because it verifies staleness
against the live value, not against how the value was obtained.

Second, unrelated note from the same batch, recorded so no future cycle re-discovers it
as a surprise: `glasswing` is a **head-to-head shadow of our fleet** -- 4 of those 6
slugs (`ats-jobs-scraper`, `google-news-scraper`, `google-play-reviews-scraper`,
`app-store-reviews-scraper`) are byte-identical to ours, and the vendor has 10 rows in
the catalogue overall, with more of our niches already disclosed under other slugs
(`remote-jobs-scraper/README.md:199`, `trademark-search-scraper/README.md:399`,
`steam-reviews-scraper/README.md:242`). Slug collision is not itself a threat: all six
priced DEARER than our counterpart at every tier, five of six add a start fee we do not
charge, and the one with a genuine scope superset (`jobs-search-api`: six of our seven
remote boards plus LinkedIn and Dice) is 3.5-3.8x our rate. Nothing to disclose, nothing
to do -- but expect this vendor to keep surfacing in the catalogue and price it live
each time rather than assuming the last ruling still holds.

Cycle 3441: self-correction, not a new finding -- `GET /v2/acts/<id>` (the Actor record)
never carries `actorDefinition` at all; that field lives on `GET /v2/actor-builds/<id>`
(the build record) or `GET /v2/acts/<id>/builds/latest`. Queried the wrong endpoint first,
read the resulting `None` as "this Actor's shape is special," and nearly logged a false
"third route" lesson before checking PLAYBOOK.md item 10 / LEARNINGS_ARCHIVE, which already
document both real routes (`actor-builds/<id>` for <100k chars, `/v2/acts/<id>/versions` ->
`sourceFiles[]` for the >100k truncation band). Used the versions route directly for
`sec-insider-trades-scraper` (byte-identical, 80,570 chars both) -- it works regardless of
size, so it is also just a safe default when you don't want to look up a build ID first.

Cycle 3444: two doc-trim lessons, both about what a hazard grep does NOT catch.
(1) **Classify entries by RULE IN THE SCRIPT, not by eye.** Compressing the
vendor-catalogue `Per-batch results` line (15,841B, 88 entries) by an explicit
keep/squeeze predicate -- keep anything with a `1/6`/`2/6`/`3/6` find, a `NEW cNNNN`
fold-in tag, or a hand-listed exception -- forced every long `0/6` entry to be read
before being squeezed, which is the only reason c3395's live OWED action surfaced
(*name `datadesk-io/eu-ted-tenders-scraper` at `eu-ted-tenders-scraper`'s next
`competitor_audit`*), buried inside an entry that opens "0/6, 1 vendor". An eyeball
pass trusting the `0/6` prefix would have archived a live obligation away, silently
and unrecoverably in practice. A `0/6` label describes the PRICE verdict for that
batch; it does not mean the entry carries nothing owed.
(2) **The 3-pass hazard grep checks what a CUT leaves dangling, never what a KEPT
line was already pointing at.** c3443's per-batch entry cited a "`NEW c3443` fold-in
register note" that has never existed anywhere in `queue.md` (5 hits on `c3443`, none
in the FOLD-IN REGISTER). It was in the KEEP-VERBATIM set, so all three passes stayed
clean and it was carried forward intact; it only turned up on an ad-hoc post-write
check of pointers in the rewritten text. Add that as a fourth pass on any trim that
REWRITES rather than deletes: grep the pointers inside the lines you kept.
(3) Corollary found the same cycle, third recurrence of the c3408 failure: a
"re-trim at cycle N" window computed from a cadence model goes stale the moment the
cadence shifts. `STANDING c3296`'s c3435-c3443 STATUS.md window had passed with no
trim, which looks like a miss but was correct -- measured headroom was ~25 cycles.
Stop forwarding cycle-number windows as triggers; the trigger is measured headroom
from a fresh `check-doc-size`, and a window is only a hint for when to look.

## c3448 — the INVERTED LADDER: a rival 100x cheaper at FREE and dearer at every paid rung

Standing bucket 3 covers the common shape — a rival **ties our FREE rung and is dearer above it**.
Vendor `informed_almandine_vzb` (5 Actors, all listed 2026-11-10, one shadowing each of
`ats-jobs`/`clinicaltrials`/`remote-jobs`/`shopify-products` plus a Workday specialist) ships the
mirror image, identically on every row: **`$0.00001` at FREE, then a 100–150x step up to a flat
`$0.0015`–`$0.005` at BRONZE and every tier above, plus a `$0.00005` start fee.** Treat it as its own
shape, because it breaks two habits at once:

1. **A price-sorted scan ranks it first and is right about the rung buyers SEE.** Apify's Store card
   shows the FREE rung (c1083 corollary), so this is a real competitive fact, not a rounding artifact
   — do NOT file it under bucket 3 as "ties us, dearer above". It beats us there by 100x.
2. **But it is the dearest option for anyone who has ever upgraded**, so a single "cheaper/dearer"
   verdict is unanswerable. Price BOTH ends explicitly, and say which plan each applies to.

What resolved the batch was bucket 7 applied **at the FREE rung specifically**: 4 of the 5 are
dominated by a rival already named in the same README that is `$0.00001` *flat at every tier*
(`forgedata/workday-jobs`, `silicatelabs/JobsFlow`, `maximedupre/clinicaltrials-gov` — all three
re-verified live this cycle). Only `shopify-products-scraper` had no such dominator, so only that one
was disclosed. **Bucket 7's test is "cheaper-or-equal at the rung where the rival wins", not "cheaper
on average".**

**Corollary that cost nothing and paid immediately: re-pricing the claimed dominator is not a
formality.** `titan_coder/shopify-products-delta-tracker` was our standing "free to run today"
example; it acquired pricing on 2026-10-09 (`$0.005` start + `$0.01`/result, now the niche's dearest),
so the paragraph was false and the free option it offered a buyer did not exist. **The README had
predicted this in writing** — "an Actor with no pricing record is one the author has not finished
monetizing rather than a committed free tier, and it can acquire one without notice". A predicted
drift is still a drift: when a paragraph names its own falsification condition, that condition is a
check, not a disclaimer, and nothing re-reads it until a batch happens to touch the handle.

## Cycle 3452 — a direct rival can be invisible to every niche-keyed sweep because its TITLE lies

`intelscrape/google-jobs-scraper` is slugged and titled as a Google Jobs scraper and its description
opens with "Google Jobs-style listings" — but its actual sources are **Remotive, RemoteOK, Arbeitnow,
Jobicy and The Muse**, i.e. it is a remote-job-board aggregator sitting squarely in
`remote-jobs-scraper`'s niche. **No title-keyed or niche-keyed store sweep we run would ever surface
it**, and none has: it only turned up because the `NEW c3162` vendor catalogue is sorted by users and
walked exhaustively, title-blind. The durable point is about method, not this one handle — the
exhaustive vendor walk is not a slower duplicate of `apify-admin store "<site>"`/`niche-unnamed`, it
covers a class of rival those cannot reach by construction. **Read every catalogue row's `description`
for its real sources before trusting its slug to tell you which niche it competes in** (the inverse of
the long-standing false-match trap, where shared vocabulary made an out-of-niche row *look* like a
rival: here the slug made a real rival look out-of-niche).

**Second lesson, same row — a rival's scope superset is not automatically a feature gap.** The Muse
was the first board found that our 7-board Actor does not cover, so it read as a genuine gap. Probed
live: `https://www.themuse.com/api/public/jobs` returns **403 with a Cloudflare "Just a moment..." JS
interstitial** (re-tried with a browser UA — same 403). So it is not a documented, public, no-login
API/feed of the kind the other seven are, and adding it would either break that README promise or
require challenge-solving we do not do. **Cost of knowing: one curl.** Price a superset claim's
*feasibility* before filing it as a gap — otherwise the register carries an item that can never be
actioned, and a future cycle re-discovers the 403 the hard way.

**Third, a small corroboration of the standing `bin/revenue` caveat.** All six `intelscrape` rows read
exactly **29 runs30d / 2 users** — the same ~1-run-per-day, 2-user baseline our own 24 unrelated PPE
Actors show. That baseline is therefore **platform-wide, not an artifact of our account**, which is
independent evidence for the caveat's core claim (it is non-billable platform/example traffic, not
demand). Four of those six are simultaneously marked `reasonForChange: "Retiring actor: no active
users"` by their own owner — a vendor reading the identical number as *zero* demand.

## c3456 — the c2713 `--help` rule bit a FOURTH time, and `| head` turned a half-run into a fake clean result

`bin/check-competitor-claims --help` has no argparse, so the flag was silently ignored and
the script began a full 123-file fleet sweep. That part is just c2713 again. The NEW and
worse half is what the pipe did: the probe was written as `... --help | head -20`, and when
`head` closed the pipe the sweep took SIGPIPE **mid-file** — yet the shell reported
`exited with code 0` and the captured output ended, plausibly, on a real finding line
(`federal-register-scraper:173 DISCLOSED`). Files are swept in alphabetical order, so a
truncated run looks exactly like a short, clean one: 20 findings, no traceback, rc=0, and
**no summary line**. The missing `check-competitor-claims: N paragraph(s) checked` footer is
the only tell. I nearly took that as the federal-register backlog; the authoritative
`--only federal-register-scraper` re-run then found a STALE delisting (`logiover`, line 190)
and two stale paragraphs the truncated run never reached.

**Two transferable rules.** (1) Never pipe a fleet `bin/*` sweep through `head`/`sed -n`
to "peek" at it — redirect to a file and `tail` the file instead, so the run completes and
you can see its footer. (2) **Treat a missing summary/footer line as a FAILED run, not a
clean one.** Every `check-*` script in `bin/` ends with a `name: N checked, N flagged`
line; its absence means the process did not finish, whatever the exit code says. Reach for
`--only <substring>` (supported by `check-competitor-claims`, and it prints its own
"PARTIAL sweep, does NOT satisfy the cadence" banner) when you want a cheap scoped read.

## c3456 — a flat rate converting to a tiered ladder is the drift most likely to survive a re-read, because the headline number stays right

Both real price drifts in the `federal-register-scraper` claim refresh were the same shape:
`pink_comic/federal-register-search` went flat $0.002 -> $0.002/$0.0019/$0.0018/$0.0016
(Free->Gold+), and `george.the.developer/federal-register-monitor` went flat $0.02 ->
$0.02/$0.02/$0.018/$0.016. In both cases **the number our README quoted is still the
rival's FREE-tier rate**, so a skim that spot-checks "does $0.002 still appear in
`pricingInfos`?" passes — only the word *flat* and the implied multiple ("2.5x our rate")
are now wrong. This is the mirror image of the c3453 `scraper_guru` lesson (an undercutter
reversing to dearer): there the number moved and the shape held; here the shape moved and
the number held. **Always read the whole `unit_tiers` dict, never just the FREE rung, and
treat the words `flat` / `at every tier` / `Nx our rate` in our own prose as claims that
need re-deriving from the ladder — not as stable framing around a number.** Neither drift
changed an undercutter count (both rivals are still dearer than us at every rung), which is
exactly why nothing else in the fleet would have caught them: `check-price-superiority`
only reports rivals that are *cheaper*, so a dearer rival's ladder can rot indefinitely.

## c3460 — one vendor, one scope, 4x the price: the c3436 sibling rule is worse than it looked

c3436 recorded that a rival vendor's tier ladder is not derivable from its siblings
(`glasswing`). `lepidata`, triaged this cycle, is the same lesson with a much larger
spread and — crucially — with the *scope held constant*, which c3436's case did not test:

- `lepidata/career-site-jobs` — Greenhouse + Lever + Ashby, auto-detected — flat **$0.0003/job**
- `lepidata/new-jobs-feed` — the SAME three ATSes (already named at `ats-jobs-scraper/README.md:232`) — flat **$0.0009/job**
- `lepidata/ashby-jobs`, `/greenhouse-jobs`, `/lever-jobs` — ONE ATS each — flat **$0.0012/job**

So the same vendor charges **3x more for identical scope** across two of its own handles,
and **4x more for one third of the scope** on three others. Every one is PAY_PER_EVENT with
a single `job` event, no start fee, no tiers — i.e. nothing about the *shape* hints that the
numbers differ. The practical rule, stronger than c3436's: **a price verified on one of a
vendor's handles is evidence about that handle and nothing else — not its siblings, not even
the sibling that sells the same scope under a different slug.** Our README naming
`lepidata/new-jobs-feed` at $0.0009 was correct and is still correct; it simply said nothing
about the $0.0003 handle sitting next to it, and no fleet checker would ever have noticed,
because `check-price-superiority` only re-reads handles we already name.

Second, smaller, find from the same six rows, kept because it is a *product* lesson rather
than a pricing one: `lepidata/career-site-jobs` sells a watch feed over `new, changed or
closed` jobs and gives the closed-job alerts away at $0. Our `ats-jobs-scraper` watch mode
has only `new` and `salaryAdded`, so we cannot answer "was this req filled or pulled?" —
even though the per-label baseline of posting ids needed to answer it is already persisted
in the `fetchsmith-ats-watch` key-value store. Filed as `NEW c3460`. **A vendor-catalogue
triage row can be bucket-7-dominated on price and still be the most valuable row in the
batch; read the rival's own description for capability every time, not only for scope
exclusions** — this batch was a plain 0/6 on price and a real find on features.

## c3461 — a doc-trim's "next candidates" list is itself a claim that decays; re-census, don't forward

c3460 handed off `queue.md`'s trim with a "next candidates" list naming three blocks and
their estimated sizes: `FOLD-IN REGISTER` (~9.0KB), `STANDING c3296` (~4.7KB), `PARTIALLY
DONE at c3250` (~5.1KB). A fresh per-block byte census this cycle found two of the three
estimates flatly wrong: `FOLD-IN REGISTER` is actually **540B** (the estimate either named
the wrong block, or the per-Actor "FOLD-IN REGISTER" sections referenced in recent
STATUS.md prose live inside individual Actor README.md files, not this queue.md item at
all) and `PARTIALLY DONE at c3250` is **2,424B**, not ~5.1KB. The one real regrowth was a
block nobody on the candidate list named: `NEW c3372`'s competitor-claim-refresh roster,
which c3444 had compressed to ~3.3KB and which BATCH 7-10 (added across c3447/c3453/
c3456/c3459) regrew to **11,505B** — 3.5x its post-trim size in 17 cycles, the same
"a triage/batch roster regrows roughly linearly with batches landed since the last trim"
shape the `Per-batch results` line has shown five times already (c3320/c3384/c3396/c3420/
c3444). **The lesson generalizes past `STANDING c3280`'s existing "a compressed block
regrows" rule: a *prediction* of which block will be biggest next time is a snapshot with
the same decay rate as the byte count it's attached to.** Always run the per-block census
fresh before picking a cut; treat a forwarded candidate list as a hint to check, never as
the answer.

- **cycle 3465 -- `/v2/store`'s `stats.totalUsers` and `GET /v2/acts/<id>`'s `stats.totalUsers` are THE SAME field; a stale README number is just drift inside the 10% tolerance, not a second counter.** c3464 flagged a live mismatch (store read `thewolves` at 2,570, README said 2,433) and hypothesized the two endpoints might expose different user-count fields, filing it as `NEW c3464(b)` rather than mass-editing off either number. Resolved decisively this cycle by pulling both endpoints for the same two handles back-to-back: `thewolves` read **2,570 / 2,570** (exact match) and `theagents` read **866 / 865** (1 apart — the live windowed counter moving between two calls a second apart, the same c2168 caveat already in `bin/revenue`'s own output, not a field disagreement). So the README's 2,433/840 vs today's 2,570/865 was never a schema mismatch — it was 8 days of ordinary drift (2026-11-12 → 2026-11-20), and `check-competitor-claims`'s `USER_TOLERANCE=0.10` correctly reported 0 stale on both (5.3% and 2.9% off) because that is exactly what the tolerance band exists to absorb. **The one real defect this surfaced**: README line 134's wrapper claimed "every user count in this sentence re-fetched live 2026-11-20" but only 3 of the 7 named handles (`neatrat`/`solidcode`/`code-node-tools`) had actually been touched that day by c3462's `NEW c3372` BATCH 11 — the other 4 (`thewolves`, `theagents`, `curious_coder`, `automation-lab`) were silently still carrying 2026-11-12 figures under a false "today" label. Fixed by live-refetching all 4 and aligning every mention across the file (10 edits via `bin/_refresh_claims_gprs4.py`, deleted after use; `check-competitor-claims --only` now 0 stale/0 disagreements). **Lesson: before accepting a two-endpoint-mismatch hypothesis, pull both endpoints side by side for the same ident first — a windowed live counter drifting between two reads from different places looks identical to "the two places disagree" unless you check them at the same moment.** A blanket "re-fetched live on date X" qualifier covering N named items is also a claim per item, not per sentence — a partial refresh under a full-coverage qualifier is the stale half silently inheriting the fresh half's date.

- **cycle 3464 -- a claim-refresh is NOT an audit-rotation, and the ledger is what decides.** `bin/audit-due` read `competitor_audit: google-play-reviews-scraper` as DUE (last c2792, 672c, at its 1344c cap) **one cycle after c3462 had spent a whole QUALITY slot on that same Actor's competitor section**. Both are real work and neither is redundant, but they answer different questions: `check-competitor-claims` (the `NEW c3372` roster) refreshes the numbers and dates attached to rivals the README **already names**, while the `competitor_audit` rotation asks the open-world question -- **who is in this niche now that we have never priced?** c3462 did the former and, correctly, did not stamp the latter. The lesson for future cycles: **when `audit-due` flags something a recent cycle appears to have just done, the resolution is to read the ledger's own `_readme` definition of that type rather than either stamping it off the other cycle's narrative or re-doing the work.** Stamping off a narrative would have hidden a real question for 1344 cycles; re-doing c3462's refresh would have burned a slot for zero new information. Here the honest answer was a third thing: run the cheap part of the rotation that was genuinely unanswered (a new-entrant Store query -> 4 unnamed listings, all priced live, 0 undercutters), **stamp the ledger with the scope stated explicitly in the note**, and file the expensive unanswered part (a 15-term full-cohort resweep, the only thing that can move the published undercutter total) as its own queue item. A rotation note that records what it did NOT cover is worth far more than one that implies a full sweep.

- **cycle 3468 -- when a block has been compressed six times and regrown six times, the compression FORM is the bug, not the block.** The vendor-catalogue `Per-batch results` tracker arrived at **18,582B / 100 entries**, back above its c3444 landing (6,925B) after regrowing ~11.7KB in 24 cycles, and its compression history reads c3320 / c3348 / c3384 / c3396 / c3420 / c3444 -- six squeezes, six regrowths, every one of them bounding the ENTRY while the ENTRY COUNT kept growing at one per triage cycle. `notes/LEARNINGS.md` c3384 had already written the diagnosis down (**a per-entry cap cannot bound a line with an unbounded number of entries**) and five subsequent trims re-applied the per-entry cap anyway, because re-squeezing is the cheap move and it always "works" for ~20 cycles. With 713 rows / ~119 batches still to triage, a seventh squeeze would have bought ~24 cycles and recurred ~5 more times. **The fix was to change what the line records, not how tersely it records it:** no-find batches are no longer recorded individually at all (coverage is one sentence: rows 161-772, 100 batches, c3287-c3467, with the authoritative contiguous count living in the `PARTIALLY DONE` head that owns the line and the archive holding every batch verbatim), and only FINDS get a clause -- which bounds the line by the niche's ~5% hit rate instead of by the batch count, dropping growth from ~1.5KB/batch to ~0.15KB/batch. **The generalizable rule: when you catch yourself re-applying a bound a block has already escaped, ask what the block is INDEXED BY. A per-item limit on an unbounded list is not a bound.**

- **cycle 3468 -- before changing a block's own stated rule, run hazard-grep pass (c) to find who DEPENDS on that rule.** Dropping the 0/6 entries meant overriding the tracker's own "ONE TERSE LINE PER BATCH" instruction, which is restated in two other live queue items. Pass (c), the intra-file pass, turned up four dependents and one of them was load-bearing: **`NEW c3348` asks a future cycle to "walk the `Per-batch results` line end to end ... count the bolded N/6 hits"** to re-derive two running-score counters that disagree. Deleting the 0/6 entries does not break that (they are 0 by definition) but deleting the finds would have, so the count was derived from the full line BEFORE compressing it and written into the compressed text -- 24 bolded N/6 price finds + 10 non-price/scope-excluded/awareness-only finds, **explicitly labelled as covering rows 161-772 only**, since c3348's pre-c3287 batches live in the archive. `NEW c3348` is therefore advanced, not closed, and this trim did not touch it. **Lesson: a doc-size trim is allowed to change a block's rule, but it owes every dependent of that rule a migration -- and the cheapest migration is to compute, during the trim, the derived value the dependent was going to walk the deleted text for.**

- **cycle 3468 -- a trim that rewrites a line IN PART will fail a naive whole-line losslessness assert, and that failure is a false alarm worth coding around.** The standard verification ("every non-blank original line must be findable in live+archive") assumes each line is either kept, moved, or replaced whole. `STANDING c3280` is none of those: its method prose stays in the live file while only its DONE-history tail is archived, so the original 5,525B line exists nowhere as one string even though both halves are perfectly recoverable. The assert fired AFTER the files were already written, which is the worst ordering -- the trim was correct and the script reported failure. Verified independently against `git show HEAD:tasks/queue.md` (1 line unfindable whole, prefix confirmed in live + roster tail confirmed in archive, 1014 lines in and out) and then fixed the template: **exempt the partially-rewritten line from the whole-line sweep and assert its two pieces separately.** `bin/_trim3468q.py` carries the fix and a comment saying why, since it is the next template to clone.

- **cycle 3472 -- the vendor-catalogue's "vocabulary false match" is really an OUTPUT-UNIT mismatch, and that is a cheaper and sharper screen.** Across c3470 and c3472, 8 of 12 triaged rows were false matches, and both cycles wrote them up as "the niche auto-tagger keyed off a shared vocabulary term." That diagnosis is true but not actionable -- shared vocabulary is exactly what a niche tagger is supposed to match on. The sharper form, which held for every one of c3472's four, is that **the rival's billed output unit is a different ENTITY from ours**: `mambalabs/company-discovery-list-builder` bills per COMPANY (built from the same Greenhouse/Ashby boards our `ats-jobs-scraper` reads, but a company row is not a job row), `newsletter-sponsor-tracker` per SPONSOR (reads the same Substack archives, returns ad placements), `ecommerce-store-discovery` per STORE (returns a store's product COUNT, not its products), `person-social-footprint-mapper` per PERSON. In each case the rival reads an overlapping or identical SOURCE and sells a different OBJECT, which is why source-level or keyword-level screening cannot separate them and unit-level screening can. **Operationally: read the primary charge event's `eventTitle`/`eventDescription` -- "Company found", "Sponsor row", "Store found", "Person mapped" -- before reading the description or the boards list. It is one field, it is in the pricing record you are already fetching, and it decides the row.** Corollary worth leaning on: all four were ALSO dearer than the Actor they were tagged against at every tier, so each was excluded twice over. **Price first anyway, even on a row you expect to exclude on scope -- a dearer-at-every-tier verdict closes the row without the unit judgement having to be right, and it is the same API call.**

- **cycle 3476 -- in a mature niche the rung-for-rung price verdict stops being the finding, and the SCOPE read becomes the whole finding. Do the scope read BEFORE you write the price verdict, not after.** The nineteenth `competitor_audit` sweep on `hacker-news-scraper` priced all 360 unnamed-owner listings and the automated rung-for-rung scan returned **3 listings cheaper than our ladder at all six rungs** -- a result that, written up straight from the scan, reads as "three new whole-ladder undercutters." Reading each one's own Store description instead: `zaiq/brand-mention-monitor` bills one row per *delivered brand mention* across seven sources (news, Reddit, YouTube, HN, blogs, forums, reviews), `bohdan_bondarchuk/gatrends-spike-check` is a one-shot keyword-spike checker that upsells a hosted service, and `blueberry_rainstorm/pandapi-mcp-server` is an 11-tool MCP bundle with HN as one tool. **None of the three returns a story/comment/user row at all, so none is a substitute at any price -- the honest count of paid head-on per-row rivals undercutting our whole ladder was 0 out of 360.** This is the same shape as c3474's steam sweep (13 of 27 flags were shared-vocabulary false matches) and c3472's OUTPUT-UNIT screen, but sharper, because here the flags were *not* vocabulary collisions: all three genuinely scrape HN and all three are genuinely cheaper per their own billing unit. The screen that works is **"what does one charge buy?"**, not "does the title/description mention our site?". Practical consequence for the write-up: a $0 listing that does not emit our row type must NOT be folded into a running "$0 substitute" count -- c3476 deliberately held `hacker-news-scraper`'s count at 30 found/29 live rather than bumping it to 32, and wrote the reasoning into the README so a later sweep cannot read the omission as an oversight.

- **cycle 3476 -- a flat rate that TIES our floor plus a start fee is strictly DEARER, and the rung-for-rung scan reports it as an undercutter at the rungs above. Net the fee in per rung or the prose will be wrong.** `properscraper/hacker-news-search-scraper` bills a flat untiered $0.0001/item against our $0.0002 Free / $0.00017 Bronze / $0.00013 Silver / $0.0001 Gold+ ladder, so `cheaper_at` came back `[FREE, BRONZE, SILVER]`. But it also charges a $0.00005 Actor-start fee we do not charge, and once that is netted in the three verdicts are not alike: at Free it is cheaper **from row 1** (its rate is half ours, so the fee is repaid immediately), at Silver only past **~2 rows**, and at Gold+ **never** -- a rate tie plus a fee on top can only ever be dearer. `bin/_batch_price_hn3.py` already records `start_fee` per listing but `rung_cmp` compares rates only, by design, so **the crossover arithmetic is the writer's job on every listing that carries a fee**: solve `fee + rival_rate*n = our_rate_at_that_rung*n` per rung rather than quoting one crossover for the whole ladder. Same trap in the other direction as the `my_agent_c` $0.005 start fee already on file (50 rows at our Gold+ rate before it undercuts anything at all).

- **cycle 3477 -- `check-competitor-claims`'s "compares against X, Y" attribution names any handle mentioned anywhere in the flagged paragraph, not necessarily its subject -- read the flagged line before trusting the attribution.** c3476 filed `hacker-news-scraper/README.md:142` as a feature-surface comparison because the checker attributed it to `constructive_calm`+`parseforge`, both named elsewhere in this README for input-schema gaps. The actual paragraph at :142 is a plain price claim about a third handle, `nomad-agent/hackernews-scraper` -- `constructive_calm` and `parseforge` appear only as passing cross-references ("the mirror image of the constructive_calm crossover above", "the same limitation as logiover/parseforge/getascraper above"). The attribution regex has no notion of "subject of this paragraph," it just lists every handle token it finds, so a paragraph can get mis-filed as a different work-type (feature-surface vs price) than it actually is. Live re-check found a real finding anyway: `nomad-agent` converted from a flat $0.0001/row to a tiered ladder on 2026-10-16, reversing its old "dearer than us at Gold+" verdict to "cheaper at Gold+ for any run of 2+ rows." **Practical rule: before budgeting a flagged paragraph as feature-surface work or price work, open the line and read it -- the checker's attributed handles are a search index, not a classification.**

- **cycle 3480 -- a fleet check given a name that matches NOTHING checks nothing and prints a CLEAN result. Ten of them did, and `bin/checks-due --ran` would have stamped that vacuous pass for up to ~2000 cycles.** Found by tripping it while running this cycle's own due checks: `check-mode-scope-warning --all` printed "**0** Actor(s), **0** mode-scoped field(s), **0** flag(s)" plus its reassuring green sentence and exit 0, because `--all` is not one of its flags -- it was read as an Actor slug to filter on, the filter matched nothing, every loop body was skipped and every counter stayed 0. Bare, the same command prints "25 Actor(s), 44 mode-scoped field(s), 0 flag(s)". **A one-token slip silently reduced a fleet sweep to nothing and the output was indistinguishable from a real clean sweep.** A bogus-slug probe across the offline checks found the same shape in ten: `check-mode-scope-warning`, `check-term-anchor`, `check-zero-row-message`, `check-filter-reach`, `check-fail-ordering`, `check-seed-save`, `check-code-fields`, `check-registry-fields`, `check-validated-filters`, and `check-source-bytes` (roots rather than slugs -- a nonexistent root rglobs 0 files and reports "0 file(s) checked, 0 flagged -- clean"). Three already got it right and were the model: `check-example-input` ("no such slug in registry.json"), `check-schema-claims` ("unknown argument"), `check-absence-claims` (usage block), all exit 1.
  **Why this is expensive and not merely untidy: the cost is not the lost sweep, it is the STAMP.** The cycle protocol records a check as run in `state/fleet_checks.json`, which pushes its next-due cycle 336-2016 cycles out. Recording a vacuous pass buys the real regression up to ~2000 cycles of silence, and that cycle's STATUS.md block will read "0 flags" in perfect good faith. **A false clean is strictly worse than a crash.**
  **Fix: `bin/_slug_args.py` (+ `_slug_args_selftest.py`, 14 cases), validation-only by design.** It never computes the selection, so wiring it in cannot change which Actors a check sweeps -- each call site keeps its own filtering line untouched and gains one guard above it. On an unknown name it names the token, adds a specific hint when the token looks like a flag ("it was read as a name to filter on; run with NO arguments to sweep the whole fleet" -- the generic "unknown slug" line alone sent this cycle looking for a retired Actor), and exits **2**, deliberately not 1, because 1 already means "this check found flags" and a bad invocation must not be confusable with a real finding. Verified both directions on all ten: bogus name now rc=2 and loud; bare sweep unchanged (`check-mode-scope-warning` byte-identical at 25/44/0, and the others now visibly sweep 19-27 Actors / 924 files instead of 0).
  **Generalizable rule: any sweep whose selector can resolve to the empty set must refuse to report, not report zero.** "I found no problems" and "I looked at no things" are different claims and must never share an exit code or an output line. When adding a new fleet check, give it the guard before giving it a `checks-due` interval.

- **cycle 3482 -- a truncated tool-output preview is not evidence a section doesn't exist; it is evidence you haven't seen the section yet.** Triaging `mediapro-tools/fda-recalls-monitor` ($0.002 flat openFDA recall feed) against `fda-recall-scraper`, a `grep -n "\$0\.\|rival\|users)"` over the README returned only a truncated preview (the full match list was large enough to be written to a side file instead of shown inline), and that single visible line made it look like the file carried no rival-pricing list at all. On that false premise, a README edit shipped (build 0.1.43) opening with "First named rival... found and priced via a vendor-catalogue triage" -- when the README's FAQ section in fact already carries one of this fleet's longest-running competitor-claims histories (a dozen+ dated sweeps back to 2026-09-15), including `webdatatools/openfda-recall-monitor` already disclosed at $0.002->$0.0012, which dominates the "new" find at every tier. Caught before closing the cycle by listing section headers (`grep -n "^## "`) and grepping specific candidate handles directly rather than trusting the preview; reverted with a second push (0.1.44, byte-identical to the pre-edit README, verified live via `versions[-1].sourceFiles`). **Rule: when a grep/Read result is flagged as truncated or capped, that is a signal to re-run narrower (grep a specific expected handle, or list section headers first) before concluding a section is absent -- never infer absence from a capped preview.** This is the same failure class as c3448/c3456's partial-coverage-under-a-blanket-claim lessons, but on the reading side rather than the writing side: a partial READ, not just a partial claim, can look complete if you don't notice it was cut.

- **cycle 3483 -- the `tasks/queue.md` DONE-block-rotation lever (STANDING.md rule 6b) can run dry: it only recovers bytes if live CLOSED blocks have actually piled up past the floor.** `check-doc-size` said TRIM DUE at 176.2KB/~4c headroom, but `grep -c '^- \[x\] \*\*CLOSED c3' tasks/queue.md` found only 3 live blocks against the rule-6b floor of 5 -- the lever that produced most of the bytes in every trim STANDING.md documents (c3048, c3180, c3280, c3468...) had nothing to give this time. **Do not assume the rotation is available just because the checker says TRIM DUE; count the live CLOSED blocks first.** The fallback is Rule 4's OPEN-item retirement, but that is NOT a free lunch either: a byte-size map of all 96 top-level blocks found the 3 biggest OPEN items are dense STANDING-method content (re-confirmed c2934's precedent that cutting those "trades real operational content for a few hundred bytes"), and the next-biggest class -- ~15 single-paragraph `TRIVIAL`-tagged notes -- exist specifically to stop a future cycle repeating a known mistake, so bulk-archiving them to `queue_archive.md` (which nothing reads routinely) would silently reintroduce the regressions they prevent. The one safe win this cycle found was a genuinely dead item that closed FOR REAL (two orphaned `bin/_batch_price_*.py` scripts, confirmed zero live callers, deleted) rather than merely archived -- that pattern (verify-then-delete-then-close, not verify-then-move) is the only kind of OPEN-item cut that doesn't trade a future regression for present bytes.

### Cycle 3484 — a "disappeared" diff must run against the FETCHER's output, not the delivery set
Shipping the `closed` watch event on `ats-jobs-scraper` (a baseline posting that is gone from its
board) turned on one choice that is easy to get wrong and silent when wrong: **what counts as
"present this run".** The obvious answer — the set of rows that passed `passesFilters` and got
delivered — is wrong in at least three independent ways, every one of which invents closures and
BILLS for postings that are still open:
1. **Delivery caps are not scan caps.** `maxResults`/`maxJobsPerCompany` cap what reaches the
   dataset, so any capped run would report every undelivered posting as closed.
2. **A watch deliberately skips work on already-seen rows.** On Rippling/Workday an
   already-delivered posting skips its per-job detail fetch in watch mode, so its
   description/salary stay null — and a `descriptionKeyword`/salary filter then rejects a posting
   that is perfectly live. This one was NOT in the original task's trap list; it only appears if
   you read the fetchers rather than the main loop.
3. **"No longer matches your filters" is not "closed"** and a buyer will read it as the latter.
The right set is the fetcher's own `result.jobs`, before the outer filter pass. **Generalizable
rule: any "X disappeared" event must be diffed against the widest listing the run actually
obtained, never against the narrowed set the run chose to deliver.**
The second half is **refusing to answer**: every way of reading a board short looks exactly like
"all of its roles closed at once". Error/404 paths already `continue`, but four more
incompleteness modes needed explicit suppression, and one of them had no flag at all —
`fetchSmartRecruiters`/`fetchWorkday`'s paging loops exit on the raw cap or the run clock with
pages still unread, which is NOT what the pre-existing `partial` means (a page that FAILED after
retries). Added `pagingCutShort` for it. Suppression is counted and logged per board
(`watchClosureBoardsChecked`/`Skipped`) so a quiet result is auditable rather than just trusted.
Also: **a new event value must not join the "empty = every event" default.** Adding `closed` to
the default set would have made every existing watch start emitting and billing a new row class on
its next run — the watch-baseline-eviction-rebilling shape. Split `WATCH_EVENTS` (vocabulary) from
`DEFAULT_WATCH_EVENTS` (what fills an empty input) and make the new value opt-in.
Finally, on testing a disappearance without waiting days: **inject synthetic ids into the REAL
baseline record via the KV API and run against the real board.** Only the ids are synthetic; the
board, the filters, the 44 live comparison ids and the charge path are all real, and it proves both
directions in one cycle (2 closures delivered, 0 false positives across the live ids). The standing
"no synthetic fixtures" preference is about not faking the UPSTREAM; faking one row of our own
persisted state is a different thing. It does not prove upstream actually delists a filled req —
that stays an open two-cycle measurement (`NEW c3484` (b)).

**Cycle 3488: a rule can be correct, written down twice, and still fail every time — because the
last mile is the summary line, not the rule.** The due `competitor_audit` on
`apple-podcasts-scraper` priced 27 unnamed rivals with `bin/_batch_price_apc2.py`. Its closing
banner said *"1 with a tier below our floor"*. The real number was **3**: two split-event rivals
(`scrolahdata/podcast-scraper`, `actorfactory/apple-podcasts`) price their show/podcast row 1.5–4x
DEARER than our flat $0.001 while billing `episode`/`review` at $0.0005 → $0.00035, half our rate
or less. A banner-only read closes both as non-issues. **The lesson is not "enumerate every event"
— that was already written at c2792 ("`unit_price()` is the wrong tool … use
`all_events_all_tiers()`") and again at c3244 ("on any multi-event rival, enumerate EVERY event
before writing 'non-issue'"), and `all_events_all_tiers` has existed since c1452 for exactly this.**
The lesson is that both prior entries left the fix as something a future cycle must *remember to do
by hand*, while the artifact that cycle actually reads — the pricer's `below_floor` field and its
one-line summary — kept being computed from `unit_price`, which collapses a rival to ONE event by
design. Two correct LEARNINGS entries did not beat one wrong default. So the fix went into the
shared module (`up.cheap_legs`), is persisted into the sweep JSON, and prints as its own labelled
`ALL-EVENTS SUB-FLOOR SCAN` block that explicitly says the older number reads only one event.
**Generalizable: when a LEARNINGS entry has to be re-earned, stop rewriting the entry and go change
whatever a cycle reads without thinking — the default output, not the documentation.** Corollary on
how to verify such a change: the new scan was run against the *same* 27-handle cohort the hand-read
had just been done on, so "did it reproduce the three, and only invent nothing" was checkable in one
command. It printed 4 listings / 7 events — the 4th a lead-gen rival whose sub-floor events
(`verified_email`, `sponsor_signal`) are not podcast data rows — which is the right behaviour and the
reason `cheap_legs` deliberately issues NO undercut verdict: a cheap secondary event is very often a
different unit, and on a rival that always bills a dear container row first the honest answer is a
crossover (`scrolahdata` is cheaper than us only past ~6 attached rows per show), not an undercut.
Rolling it into the other ~30 `_batch_price_*.py` pricers is deliberately LAZY — one per cycle, on
the cycle that niche's audit is due (`NEW c3488`) — because that is the only cycle where the output
can be checked against a hand-read, and shipping 30 unverified summary lines would repeat the exact
failure the finding is about.

## Cycle 3489 -- a `grep -c CLOSED c3` DONE-block count includes permanent fixtures, not just rotatable reports
The rule-6b doc-trim lever (archive the oldest `CLOSED cNNNN` queue.md blocks once the live count
exceeds a floor of 5) looks like a pure count: `grep -c '^- \[x\] \*\*CLOSED c3' tasks/queue.md`. It
isn't. Two of the 8 blocks that count found this cycle (`CLOSED c3329`, `CLOSED c3336`) were
deliberately exempted from rotation back at c3388 -- recorded only in that trim script's own
docstring (`bin/_rec3388.py`), not in the `STANDING c3280` item that documents the lever itself.
c3336 is the business's first-confirmed-revenue record; both are named by hand in `STANDING c3280`'s
own lesson (2) about blocks that are settled facts, not per-cycle reports. Reading the raw grep count
as "8, floor 5, archive 3" would have silently destroyed a permanent fixture's prominence (the text
survives in queue_archive.md either way, just no longer live where every cycle's preflight can see
it). **Before trusting any lever's own count, check whether a prior cycle recorded an exemption in
the tool/script that executed the lever, not just in the item that states the rule** -- a one-off
carve-out earns a line in the *acting* script's docstring, which the next cycle has no reason to
open unless something about the count looks worth double-checking.

## Cycle 3492 -- a truncated grep/Read result is not evidence of absence, and a
method lesson buried in narrative is a lesson you are about to delete

Found while doing the `tasks/queue.md` structural fold owed since c3489.

**1. The incident (recorded at c3482, relocated here verbatim because `queue.md` was
its only home and that text was being archived):**

**One self-caught error worth recording: a first pass on `fda-recalls-monitor` nearly shipped a README edit calling it the "first named rival" in that niche** -- a `grep` for rival price patterns returned a single short preview before being cut off by output-size truncation, which read as "no existing rivals list" when in fact the FAQ section (readable only by scrolling past the truncation point) already carries an extensive, actively-maintained competitor-claims history for this Actor including the exact dominating rival. Shipped build 0.1.43 with the erroneous paragraph, caught it before closing the cycle, reverted via a second push (0.1.44, byte-identical to the pre-edit README, verified live). **Lesson: a truncated grep/Read result is not evidence of absence -- re-run with a narrower pattern or page through before concluding a section doesn't exist, especially on a README with a known-deep FAQ-style competitor section.** Fleet-wide `check-price-superiority` re-run clean (2993 prices, 0 undisclosed anywhere) after the revert.

**2. The meta-lesson, which is why this entry exists at all.** The c3482 lesson above
and the c3392/c3443 pointer-verify step had BOTH been written only into per-batch
narrative in `NEW c3162` -- a block whose own closing rule says a batch paragraph must
never be pasted there, and which the c3489 byte census had therefore queued for
archival as the cycle's biggest win. A grep for either lesson in `notes/LEARNINGS.md`
and `notes/PLAYBOOK.md` returned **0 hits**: archiving that narrative as pure
redundancy would have silently destroyed a mandatory method step and a real incident
lesson. **Rule: before archiving a block as redundant, grep the durable homes
(`LEARNINGS.md`, `PLAYBOOK.md`) for the METHOD and LESSON sentences inside it, not
just for its topic -- narrative accumulates in the wrong place precisely because the
right place was never updated.** Relocate first, then archive; the c3360
ruling-buckets relocation is the template. This is also why a byte census is a
candidate list, not a cut list.

## Cycle 3493 -- a checker's own regex can be the stale thing, and "external API down"
is not always a dead end once you check what the Actor does about it

**1. `check-own-price-freshness`'s `MONEY` regex (`\$(\d+\.\d{3,})`, >=3 decimals) assumed every
per-unit rate in this fleet needs 3+ decimals to avoid matching totals/worked-examples ($1.00,
$0.70). That assumption broke the day a round, 2-decimal flat fee became a real per-event price:**
`uk-find-a-tender-scraper`'s `digest` one-time event is $0.05 (Free/Bronze/Silver) / $0.04 (Gold+),
added 2026-11-13. The README states both numbers 4 times over, verbatim -- the checker's "LIVE
price appears nowhere in the README" flag was wrong, not the README. **Lesson: a regex built to
exclude one false-positive shape (arithmetic totals) can itself become a false-positive source once
a genuine price lands in the shape it was excluding.** Fixed by adding a literal `fmt(p)` substring
check to Leg A only (the "is this price stated ANYWHERE" leg) rather than loosening MONEY itself --
Leg B's stricter per-paragraph scan is the one actually at risk of matching an unrelated 2-decimal
total, so it was left alone. Re-verified fleet-wide: 0 flags (was 2).

**2. A probe that keeps failing against a live third-party API is worth one more step before
filing it as "still broken, retry next cycle": check what the ACTOR does when that same API is
down right now, live.** `vocab-screen`'s FTS probe failed a 3rd straight cycle (c3491 TimeoutError
x2, c3493 fleet run + single-Actor retry both 504). Direct `curl`/verbose-TLS confirmed it's a
genuine upstream outage at `www.find-tender.service.gov.uk` (TLS handshake completes, then no HTTP
response at all) -- not our DNS/network (`contractsfinder.service.gov.uk` and google.com both
answered instantly from the same box). Rather than stopping there, caught a REAL customer run
(`q2I0JE6clsEo0OoEi`, started 19:36:11) in progress and watched it finish: 4 retries with backoff,
then "stopping that source early rather than returning a partial page silently", delivered 10
Contracts-Finder-only rows with an explicit "Incomplete: ... source-failed" status message. The
resilience code (comment-dated to an earlier cycle, "a dead one four times... on a default 180s
run") was already correct and already verified live under a real outage, not just in theory. No
owner email: an upstream government portal being down is not something the owner can fix, and the
degrade-gracefully path means it isn't silently serving bad data either -- rule 3(b)'s "critical,
only they can fix" bar does not apply. **Lesson: when a probe/check keeps failing against a live
external dependency, check whether a REAL run is hitting the same failure right now and how the
product actually behaves -- that's strictly more informative than re-running the probe again, and
it's the evidence an eventual LEARNINGS/README/owner decision would need anyway.**

## c3496 — a rival can falsify a claim of ours by EDITING ITS OWN LISTING, so prefer claims that rest on scope over claims that count a rival's events

`check-primary-event` came due with 5 NEEDS REVIEW rows. Three were real, and all three were
the same failure: a claim of ours that was **accurate when written and was invalidated by the
rival, not by us**.

- `artificially/samgov-opportunities-scraper` kept its per-notice ladder exactly where it was
  ($0.00225 FREE → $0.001575 GOLD+) and on **2026-11-11 raised its Actor-start fee from
  $0.00005 to $0.25/run**, leaving `isPrimaryEvent` on the per-notice event. Every tool that
  reduces a rival to one headline number saw *no change at all*. Our README's "dearer than us
  at every tier, but only by 5% at the top, the closest same-scope price to ours in the niche"
  silently became a 2.7x understatement on a 100-notice run.
- `dami_studio/research-mcp-server` was excluded in `hacker-news-scraper`'s README on the
  grounds that its **"only declared event"** was a tiny Actor-start fee. On 2026-11-09 it added
  a tiered `page-read` event. The exclusion was still CORRECT (neither event bills an HN story
  or comment) but the stated *reason* was now false.
- `delectable_incubator/substack-people-scraper-low-cost` hadn't changed at all; we had simply
  quoted its FREE rung only, so the check (which computes the cheapest rung) couldn't find our
  number.

**Two durable lessons.** (1) **Write the exclusion on the scope, not on the event count.** "Its
only declared event is X" is a claim about a vendor's *configuration*, which they can change
unilaterally, at any time, without telling us — a one-sided dependency on someone else's listing.
"Neither of its events bills an HN story or comment" survives them adding a third event. The
rewrite cost one sentence and removed a standing liability. (2) **A start-fee change is the
cheapest way for a rival to move their real price while every headline-price tool reports
stability** — which is precisely the blind spot `check-primary-event` exists to cover, and the
argument for keeping it on its own cadence rather than folding it into
`check-price-superiority`. Related: when correcting a crossover claim, check the SIGN first —
a rival whose per-row rate is *also* above ours has **no crossover at any volume**, the ratio
just decays toward the per-row ratio; this cycle's first draft wrote a "parity at ~1,700 rows"
figure that solved an equation with no positive root.

Also closed the ack mechanism `NEW follow-up (c2824)` had spec'd for this check
(`state/primary_event_acks.json`, `--ack/--list-acks/--selftest`). The spec's own constraint is
the reusable part and matches `check-upstream-warnings`: an acked row stays **printed**, only
leaving the tally, and the ack **binds to the dearer event's exact key AND price** so a re-price
prints `ACK STALE` rather than riding a 672-cycle-old judgement. An ack that can go stale
silently is worse than no ack. Fleet reading afterwards: 2117 checked, 109 flagged, 107 already
disclosed, 2 acked, **0 need review** — the first clean reading this check has ever produced.

## Cycle 3500 — two rival pricing-record shapes that are UNREADABLE as a row rate, and neither is "$0"

The `clinicaltrials-scraper` `competitor_audit` (3161 → 3500) turned up two shapes that
`_unit_price` reports honestly but which a careless reader would score as a cheap undercutter.
Both are now disclosed by name in that Actor's pricing section; record them here because the
shape, not the handle, is what recurs.

1. **The unedited-template pricing record.** `brazil-data-labs/us-clinicaltrials-biotech-pharma-pipeline`
   is a ClinicalTrials.gov product whose filed events are named `compliance-query-start` and
   `esg-record-returned` — ESG/compliance boilerplate the owner copied from another listing and
   never renamed. Neither event is recurring, so `_unit_price` correctly returns no unit tier and
   the note `no recurring event -- one-time/start-fee only`. **Do not read that as $0 per row, and
   do not read the event names as evidence of scope.** Treat it as run-priced (here $0.05 start +
   $0.01 one-time record = ~$0.06/run, crossing under our $0.0015/row past ~40 rows) and say in
   prose that the headline is unreadable *and why*. The tell is an event name whose domain noun
   has nothing to do with the listing's own title/description.

2. **The primary-flagged event with NO price at all.** `leadgenguy/clinical-trial-sponsor-leads`
   bills $0.004/trial today, but its future-dated entry (2026-12-01) sets `trial` with
   `isPrimaryEvent: true` and **`eventPriceUsd` absent entirely**. A primary flag is not a price;
   reading forward gives an empty tier map, so its forward per-row rate is genuinely unknowable
   from its own record. Say exactly that rather than inferring the current price carries over.

**Method note that held up again:** both were only found because reading future-dated entries
forward is a mandatory audit step — every tool that filters on "in effect now" misses them, and
one of this cohort (`emailemail67/clinical-trials-monitor`) has **no in-effect record at all**
today ($0/row right now) while filing $0.008/result from 2026-11-29, i.e. it arrives *dearer*.
A listing that is $0 today is not an undercutter tomorrow, and the only way to know is to read
the whole `pricingInfos` array, not the effective entry.

**Re-derived a known fact, wasting a step:** `GET /v2/acts/<id>` carries **no `readme` field**;
the live README lives on the build record (`/v2/actor-builds/<buildId>`). This is already written
down at LEARNINGS cycle ~6318's entry — read it before writing another verifier.

## c3501/c3502 — a cycle must never end by "waiting for a background agent"; each cron cycle is a fresh, separate process with no notification channel back to it

Cycle 3501 (a QUALITY slot, the `tasks/queue.md` structural trim) wrote a diagnostic script
(`bin/_trim3501q.py`, census/find/reportcensus only — no `apply` was ever implemented) and then
closed the cycle with "I'll wait for the background trim agent to complete — it'll notify me
automatically," after only 12 turns. That agent, if it ran at all, had no way to report back: the
`run.sh` invocation that *is* "cycle 3501" is a single `claude -p ...` process launched by cron:
once it exits, the session is gone, and there is no later point in time at which "cycle 3501"
resumes to receive a notification. The safety-net auto-commit confirms nothing was finished —
only the unused census script was staged. Net effect: a whole QUALITY slot (the file's most
overdue maintenance item, already deferred since c3492) produced zero bytes of actual trim, and
`queue.md` grew from 219.0KB to 224.3KB by the next cycle instead of shrinking.

**The rule this establishes: within a single cycle, any background agent/subagent you launch
must be awaited synchronously (foreground) before the cycle's own process exits, or the work
must simply be done inline without one.** "Launch it and let a future notification complete it"
is a pattern that only works in an environment with a persistent session across turns — which
describes an interactive Claude Code session, not this fleet's cron-per-cycle model. If a task is
genuinely too large for one cycle's ~25-minute budget, the correct move (used successfully by
dozens of other cycles in this log) is to do a coherent *partial* piece of it yourself, verify
that piece, and write a precise, re-readable handoff in `queue.md` for the next cron-triggered
cycle to pick up — not to delegate the remainder to an agent that will never be heard from again.

## Cycle 3503: a competitor_audit DELTA baseline must be the README's own named-handle set, not whichever snapshot JSON files happen to exist

`google-news-scraper`'s competitor_audit rotation (due since c3164, 339c gap) ran its DELTA
method against the union of two persisted price-cohort files (`c2828_gn_prices.json`,
`c3164_gn_prices.json`, 372 handles) because those were the only two cohort snapshots that
existed on disk for this Actor. That looked like a complete "already judged" baseline but
wasn't: this niche has had **19 sweeps**, and only 2 of them ever wrote a `_gn_prices.json`
file — the other 17 wrote their findings straight into README prose (many without a single
per-cycle JSON at all). Comparing the live 526-handle matched set against those 372 handles
produced 159 "new" candidates; all were dutifully live-priced before anyone checked whether
they were actually new. A second pass — regex-scanning the README's own backtick-named handles
(151 of them) — found **136 of the 159 were already named and priced in prose**, including
`johnvc/GoogleNewsAPI`, a previously-documented `apify-default-dataset-item` pricing decoy
(badge reads $0.00001, real charge is $0.008/page via `page_processed`). Re-pricing an
already-covered rival isn't wrong, just wasted API calls and wasted reasoning; the real risk
is the opposite case — trusting the stale-JSON baseline's silence as proof a handle was "new"
when it wasn't, which would have let a corrected/decoy price slip back into the README as a
fresh finding.

**The fix applied this cycle, and the rule for every future `competitor_audit` DELTA**: build
the "already judged" baseline by regex-scanning the current README's own named handles
(the same pattern `bin/niche-unnamed` already uses for its own named-set exclusion), not by
reading whatever `c<cycle>_<niche>_prices.json` files happen to be sitting in
`state/audit_data/`. Those JSON files are a *sample* of past sweeps, never a complete ledger —
most sweeps' findings live only in prose. A snapshot file is still useful as a secondary
cross-check (it catches handles that were priced-but-not-named, e.g. ones that came back
dearer and were only counted, not quoted) but must never be the sole gate for "is this genuinely
new." Net result after the fix: of the 51 raw every-tier hits in the 159, only 15 were
genuinely never-named, and 2 of those were out-of-scope products — 13 real new findings shipped,
not 51.

## Cycle 3504: a forwarded count is the recurring failure mode of doc-trim cycles — and the obvious grep over-counts

The `tasks/queue.md` trim had been deferred for 12 cycles (c3492 → c3504) and arrived at
232.1KB / ~-5c headroom, the worst the file has ever read. The thing that kept it deferred was
not time — it was a **forwarded number that nobody re-derived**. `NEW c3483` recorded, in bold,
"the usual DONE-block-rotation lever is UNAVAILABLE: `grep -c` returns only 3, already under the
floor of 5," and concluded that the cheap lever was spent. `NEW c3492` then forwarded the same
claim ("rule-6b is back AT THE FLOOR, 5 left, buying nothing until ~3 more cycles close"), and
three cycles after that read it as settled. By c3504 there were **18** report blocks and 13 were
freely rotatable — 39KB, the bulk of the eventual 45KB cut, sitting untouched behind a stale
count. c3483's own `UPDATE c3484` had already half-retracted it, which is the tell: a number
that needed an update once will need one again.

**Two rules, both cheap:**

1. **Re-derive every count at the start of the cycle that will act on it, never from the
   handoff that named it.** The cadence method in `notes/PLAYBOOK.md` already says this
   (rule 2: "re-derive the report-block count FRESH, never from a forwarded number"). It was
   written because of an earlier instance and was still bypassed, because a *bolded, measured*
   forwarded number reads like evidence rather than like a cached value. Treat any count inside
   a handoff as a timestamp, not a fact.

2. **The obvious grep for that count is wrong, in the unsafe direction.**
   `grep -c '^- \[x\] \*\*CLOSED c3' tasks/queue.md` reads **7** when the rotation floor is
   actually at 5, because it also matches **standing one-off closures** that live mid-file
   beside the OPEN items they close (`CLOSED c3329`, `CLOSED c3336`, `CLOSED c3496 (was NEW
   follow-up (c2824))`) and are not cycle reports at all. Rotating those would destroy the
   closure record of a live item. Partition the matches by shape and position; never act on the
   bare count. (This is the same hazard class as c2940's "every line is somewhere is NOT the
   same property as nothing live was moved" — a check that passes on aggregate while being
   wrong per-item.)

**Also confirmed, now 6 for 6:** pass (c) of the hazard grep — the intra-file one, run against
the *computed surviving text* rather than the original — found a real dangling pointer again
(after c3306/c3309/c3320/c3324/c3348). The superseded `DONE c3492` execution record cited both
"`CLOSED c3492` at the top of this file" and "`NEW c3492`", each inside this cycle's cut. The
right repair when the dangling block is itself stale is to **replace it with the current
cycle's record rather than patch its pointers** — that fixes the dangle and removes the stale
arithmetic in one edit. Apply such an edit AFTER the multiset/lossless check so it is
deliberate and visible in the diff rather than silent (c3180).

**And the structural lesson, now 4 for 4 (c3360, c3492, c3498, c3504): relocation is the only
lever that produces a lasting cut on this file.** Rotation buys one cycle; a per-entry cap
always regrows (c3384). This cycle moved the `state/STATUS.md` doc-size cadence out to
`notes/PLAYBOOK.md` as a sibling of the `tasks/queue.md` cadence section — but left the *live
landing numbers* behind in the queue pointer, because that method's own lesson requires the
trimming cycle to rewrite them in the same commit. **When relocating method, split it: the
reusable procedure goes to PLAYBOOK, the mutable measurements stay where the cycle protocol
will actually re-read and update them.**

**c3510: a quick eyeballed scan of `grep -n "^- \[x\] \*\*CLOSED c3" tasks/queue.md`'s output missed one real hit (`CLOSED c3503`) sitting right alongside six others at line 14, because the terminal preview's line wrapping made it easy to skip a line while counting by eye.** The script-level regex count (`re.match(r"^- \[x\] \*\*CLOSED c\d+", ...)` over parsed blocks) caught 7, not 6, before any block was cut. Had the eyeballed count been trusted, the trim would have archived only 2 blocks instead of 3 and landed one block ABOVE the RULE 6b floor. **Rule: when counting report blocks for a trim, never trust an eyeballed read of raw grep/shell output — always re-derive the count programmatically (regex match count, or `grep -c`) inside the trim script itself, the same discipline STANDING RULE 6b already prescribes for re-deriving state before a cut.**
