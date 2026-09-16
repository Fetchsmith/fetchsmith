---
title: Eight ways an "only new since last run" watch mode silently stops working
description: "New" is not a property of a public API — it's a property of your own history. Shipping incremental watch mode across fourteen Actors (government data, forums, job boards, tenders, campaign finance, app/game reviews) surfaced eight failure modes, and every one of them keeps the run log green while delivering nothing or delivering less than it should.
date: 2026-09-16
tags: webscraping, api, opendata, scheduling
---

Almost every buyer of a public-data scraper eventually wants the same thing: *don't send me the same 18,000 rows every morning, send me what changed.* That sounds like a filter. It isn't. Every public API we work with will happily tell you what **it** thinks is recent — and none of them know what **you** already received. "New" lives in your own history, which means a watch mode is a stateful feature bolted onto a stateless scraper, and that is where it goes wrong.

We shipped this mode (`watchLabel`) across 14 Actors: five government-data hosts ([NIH RePORTER](/tools/nih-reporter-scraper), the [Federal Register](/tools/federal-register-scraper), [Grants.gov](/tools/grants-gov-scraper), [openFDA recalls](/tools/fda-recall-scraper) and [ClinicalTrials.gov](/tools/clinicaltrials-scraper)), two tender/procurement hosts ([EU TED](/tools/eu-ted-tenders-scraper) and [UK Find a Tender](/tools/uk-find-a-tender-scraper)), two money hosts ([US federal awards](/tools/us-federal-awards-scraper) and [FEC campaign finance](/tools/fec-campaign-finance-scraper)), a forum ([Hacker News](/tools/hacker-news-scraper)), a job board aggregator ([ATS jobs](/tools/ats-jobs-scraper)) and three app/game review platforms ([Google Play](/tools/google-play-reviews-scraper), [the Apple App Store](/tools/app-store-reviews-scraper) and [Steam](/tools/steam-reviews-scraper)). The state machine copied across all fourteen almost unchanged. What did not copy were the eight traps below. Each one was found on a *different* host, each produces a run that exits 0 with a cheerful log line, and each delivers either zero rows forever or a silent under-count.

## Trap 0: the API's own "recent" flag is not your "new"

NIH RePORTER has a `newly_added_projects_only` boolean, and it is genuinely useful — but it means "recently added to the index", index-wide. Set it and you get roughly the same ~8,900 projects back on every run until they age out of the flag. That is a perfectly correct answer to a question nobody asked. A weekly alert needs "something new matched **my** query", and no server-side flag can answer that, because the server has no idea what you fetched last Tuesday.

So: you keep a baseline of ids you have already delivered, and you diff against it. Everything below is a consequence of that.

## Trap 1: your state store resets every run

On Apify, `Actor.openKeyValueStore()` with no argument gives you the **default** store, which is created fresh per run. Write your baseline there and every run starts from an empty set — so every row looks new, every run delivers everything, and on a per-result pricing model the buyer pays full freight forever. The log says `delivered 18458 new rows`, which is exactly what "working" looks like.

The fix is a *named* store, which persists on the caller's own account:

```js
const store = await Actor.openKeyValueStore('fetchsmith-nih-watch');
```

Two details that bit us:

- **The key needs the criteria baked in, not just the label.** We use `watch-<label>-<sha1(criteria).slice(0,10)>`. If the buyer widens a filter, that is a *different question*, and it deserves a fresh baseline — otherwise the first run after the edit dumps every row the old, narrower filter happened to exclude and bills it as "new".
- **Apify KV keys only allow `[a-zA-Z0-9!-_.'()]`.** The obvious separator, a colon, is invalid. Sanitise the label rather than passing it through.

## Trap 2: fingerprint what the user typed, not what your code computed

This one is the reason to write the post. The Federal Register Actor's publication-date window defaults to a rolling *last 90 days*; the openFDA one defaults to a rolling *last 365 days*. Both resolve that default to absolute dates at run start, from `new Date()`.

Hash the **resolved** dates into your criteria fingerprint and a scheduled daily watch gets a brand-new key every single day. Which means: it seeds a fresh baseline, correctly returns zero rows because a seed run is a baseline run, logs `seeded 51 ids, nothing new`, exits 0 — and does that tomorrow, and the day after, forever. It never delivers a row, it never errors, and it never charges anything, so there is no bill to notice and no alert to miss. It just quietly is not a product.

The rule that fixes it is one line long: **the fingerprint is built from the buyer's raw input, never from the value your code derived.** If they left the date window alone, the fingerprint entry is `null`. Any input with a relative default — `last N days`, `today`, "since the previous quarter" — has this trap.

## Trap 3: a baseline walk and a result walk need different paging

The first run has to enumerate the *entire* current match set, because anything it misses will be reported as new later. A normal run only has to satisfy `maxResults`. Those are different jobs, and reusing the result pager for the seed is where two real bugs came from:

- **Page size inherited from `maxResults`.** The Federal Register seed ran with `per_page = 50` and recorded 50 of 51 matching documents. The openFDA Actor derives its page size the same way (`min(1000, max(20, min(maxResults, 200)))`). A seed must pin page size to the API maximum — it is covering the whole set, not one page of it.
- **More than one shape of "next page".** `federalregister.gov/api/v1/documents.json` returns `next_page_url` as a `search_after_cursor` link for large walks **and** as a plain `?page=N` link for small result sets. Our pager only understood the cursor and broke out of the loop otherwise. That was harmless for normal runs — page one already satisfies `maxResults` — but fatal in watch mode, where nearly every row is skipped as already-seen and the walk *must* keep going to find the handful that aren't.

The check that catches both takes one line: compare your recorded seed count against the API's own `count`/total for the identical query. 50 versus 51 is invisible by eye and obvious by subtraction.

## Trap 4: a cheap seed still has to reproduce the exact predicate

Seeding is supposed to be cheap — you only need ids, so you skip the per-row detail fetch. On Grants.gov that would have been wrong, not just cheap. Its `minAwardAmount`/`maxAwardAmount` filter can only be evaluated *after* a per-opportunity detail fetch. An opportunity whose award ceiling is not yet populated at seed time doesn't match the filter — but ceilings do get filled in later (a real, observed field-level edit on that API), at which point it legitimately becomes a match. If the thin seed had dumped every raw hit id into the baseline, that opportunity would be marked "already seen" before it ever qualified, and would never surface.

So: **the seed must apply the same predicate a real run would, not a cheaper approximation of it.** Cost-cutting the seed is only safe for the parts of the filter that don't depend on an enrichment or join step. Where the filter is evaluated purely on fields the search endpoint already returns — openFDA's recall rows, for instance — an id-only seed is provably equivalent, and we checked that by reading the code rather than assuming it. When the filter is evaluated client-side after a full fetch — the UK Find a Tender Actor round-robins two portals and matches `cpvCodes`/`buyerName`/value bounds against the normalized row, not the raw list item — there is no cheaper seed at all: it has to run the exact same fetch-and-normalize pipeline as a real delivery, just routed into the baseline instead of the output.

## Trap 5: a scan cap and a delivery cap are the same variable until they aren't

This is the trap that took the longest to notice, because it doesn't break a fresh feature — it breaks watch mode by *reusing a cap that already existed and already worked*. The ATS job board Actor had `maxJobsPerCompany` (default 50), a perfectly sensible limit on a normal run: fetch a company's postings, stop after the buyer's cap of matching results. Once `watchLabel` exists, that same variable means something different. In watch mode almost every row scanned is already-delivered, so a buyer's `maxJobsPerCompany: 5` against a board with 39 currently-matching roles surfaced a new one only if it happened to sort into the first 5 — a job alert that silently misses most of what it's supposed to be watching for, on every single run, forever. The Hacker News Actor had the identical bug in a differently-shaped variable (`fetched < maxItemsPerQuery` counted items looked at, not items pushed), which is why grepping for one ternary shape didn't find both: the fix is to ask what the loop's stopping condition actually counts, not what the cap is called.

The fix, applied consistently once we knew to look for it: split every such cap into a **scan cap** (how far to look — raised for watch mode, seeding *and* incremental, not just seeding) and a **delivery cap** (how many rows to actually push and charge — stays exactly as the buyer set it, counted only against rows that clear the already-seen check). An already-seen row must cost a scan slot, never a delivery slot.

The corollary, found while auditing every later port for this exact bug: **not every cap needs splitting, and splitting a cap that doesn't need it is wasted risk.** A loop that already gates its stopping condition on rows *actually pushed* (`while (pushed < maxResults)`, with already-seen rows skipped before `pushed` increments) was never vulnerable — an already-seen row just costs one more free loop iteration, the scan keeps going regardless. Five of the eleven ports (TED, UK tender, FEC, US federal awards, and three of the original four) turned out to already have this shape and needed no change. And a cap can be an honestly-documented cost ceiling rather than a disguised delivery limit — US federal awards' `maxPagesPerCategory` says exactly what it does (bound how many pages a run scans, full stop) and applies identically whether or not watch mode is on; the tell is whether the cap is described as bounding *cost/reach* (leave it alone, just give the seed walk its own larger version) or is silently doing double duty as *how many results you get* (split it). Read what the variable is gating, not what it's named.

## Trap 6: not every query mode has a "new"

`watchLabel` presupposes the query describes a set that grows over time — new studies register, new documents publish, new stories get posted. Two of the eleven hosts have a second query mode that doesn't fit that shape at all. FEC's `candidates` search mode returns the same fixed roster of candidates for a given filter, indefinitely — there's no discrete "new candidate event" to diff against, so a baseline would either never gain anything (silently useless) or churn on irrelevant re-orderings. ClinicalTrials and US federal awards have the opposite version of the same problem: an exact `nctIds`/`awardIds` lookup returns exactly the studies or awards you named, every time, by definition — "new" has no meaning applied to a fixed id list.

The fix isn't clever: detect the incompatible mode and **reject the combination out loud** — a warning naming exactly why `watchLabel` was ignored — rather than silently accepting it and doing nothing, or worse, silently seeding a baseline against a set that will never produce a delta. A buyer who sets `watchLabel` on a mode that can't support it needs to know their alert isn't going to alert, not discover it by absence three weeks later. Steam's own `games` data type is a third instance of this: it returns one row per game, the same row every run, so a fourth host got a fourth independent confirmation of the same rule rather than a special case.

## Trap 7: a snapshot row riding along with real events still needs to not get billed every run

Google Play and the Apple App Store Actors don't fail Trap 6's test — their review rows genuinely are events with a real "new" — but every fetch also carries one extra row per app: a snapshot (title, rating, install count, price) that is identical on every run for an unchanged app. It has no natural id and no "new" of its own, same problem as Trap 6, but rejecting the whole Actor over it would be wrong here, because the README promises that metadata alongside the reviews and buyers depend on the output shape. Push it unconditionally instead, and a quiet hourly watch on an app with zero new reviews still delivers and bills for that one snapshot row 24 times a day — the same "log says delivered, that's what working looks like" failure as Trap 1, just smaller and per-target instead of per-run.

The fix: hold the snapshot in memory (`pendingAppRecord`) and push it only alongside the first genuinely new review of that app in that run. A run with nothing new delivers nothing at all, snapshot included; a run with three new reviews delivers the three reviews plus exactly one snapshot row. Whether a per-target extra row needs Trap 6's reject-the-mode fix or this cycle's defer-the-row fix comes down to one question: does *anything else* in that same fetch have a genuine "new"? Steam's `games` mode has nothing else riding along, so it's Trap 6; Google Play's and the App Store's snapshot rows ride along with reviews that do, so they're Trap 7.

## The one that isn't a trap: a "new id" is not the same thing as news

Every trap above is about getting the *set* of new ids right. There is a separate, larger hole underneath all of them, and it isn't a bug in any implementation — it's the premise: an incremental watch keyed on ids drops an already-seen id **unconditionally**, before any filter and before any charge. That is exactly right for a forum post or a review, which never change after publication. It is quietly wrong for anything whose *record* keeps living after it's published. A grant opportunity's close date gets extended. A forecast becomes a real posting. An FDA recall goes from `Ongoing` to `Terminated`, or gets reclassified from Class II to Class I. Every one of those is the thing a buyer actually set the alert for, and every one of them arrives attached to an id they already have — so a correct, fully-tested, green watch mode delivers nothing at all.

We only saw this by pricing the competition rather than reading our own code: one vendor sells *seven separate paid Actors* against a single grants API — deadline-amendment watch, funding-range-change watch, eligibility-change watch, forecast-to-posted watch, cancellation watch, document-change watch, general opportunity-change watch — which is a fairly loud market signal that "something I already have changed" is a different product from "something new appeared."

The fix is one optional boolean (`watchChanges`) and a change of state shape: the baseline stops being a `Set<id>` and becomes a `Map<id, snapshot>`, where the snapshot is a handful of mutable fields. An already-seen row whose snapshot differs is re-delivered — tagged with what changed and what the previous value was (`_watchChangeType`, `_watchPrevious`) so a downstream rule can act on the transition rather than re-diffing the row — and billed like any other delivered row. Three details decide whether this is safe:

- **Snapshot only fields that are always present.** Pick a field that is only populated when an `enrich`-style option is on and every run with enrichment off reads as a change, forever. The fields that work are the thin, unconditional ones (`status`, `classification`, `closeDate`).
- **Refresh the snapshot on every scan, whether or not the flag is on.** Otherwise the first run after a buyer enables `watchChanges` re-delivers — and charges for — a backlog of drift that accumulated while nobody was watching. Turning the flag on should start detecting *future* changes, not invoice the past.
- **Treat a pre-feature baseline as snapshot-unknown, not snapshot-empty.** Live records written before the feature existed store a flat array of bare id strings. Load code that coerces those to `{}` reports every one of them as changed on the next run. Detect the legacy shape and mark those ids `null` — no known previous value means no change event.

Live on [Grants.gov](/tools/grants-gov-scraper), [openFDA recalls](/tools/fda-recall-scraper) and [US federal awards](/tools/us-federal-awards-scraper), off by default on all three. Verified the same way as everything else here — on the real platform, by mutating stored state rather than trusting a unit test: seed a baseline (509 opportunities; 29 Class I recalls; 26 awards), `PUT` two altered snapshots straight into the key-value store via the API, rerun, and confirm that exactly those two rows come back with the right tags and that the run charged for exactly two rows. One of the recalls came back as `D-0827-2026` status→`Terminated`, the other as `D-0832-2026` classification→`Class III`, which is precisely the email a recall analyst wanted and would never have received.

On US federal awards the snapshot rides on USAspending's own `Last Modified Date` plus the amount fields (`awardAmount`/`totalOutlays`, or `loanValue`/`subsidyCost` on loans) and the period-of-performance end date — a contract modification that raises a ceiling or extends an end date is the whole reason a buyer watches that dataset. It is deliberately scoped to prime-award mode only: sub-award rows carry no reliable per-record drift signal, so asking for `watchChanges` there logs a named warning and falls back to a plain id watch, rather than pretending to detect changes it cannot see.

## The corollary nobody checks: confirm the record actually mutates

Having shipped that three times, the obvious next move was a fourth — the [Federal Register](/tools/federal-register-scraper), where a rule's effective date or comment deadline visibly gets extended all the time. We had it written down as the last candidate. It is wrong, and finding out cost one hour of reading real documents instead of one hour of writing code that would never have fired.

The Federal Register **never edits a published document.** Pull a real "Extension of Comment Period" notice (`2025-04129`, `2025-02237`, `2026-03798` all work), find the original rule it extends, refetch that original: its own `effective_on` and `comments_close_on` are byte-identical to the day it was published. The amendment is not a mutation of the original record, it's a *brand-new document* with its own `document_number`, whose free-text `dates`/`action` cites the original by its `"NN FR NNNNN"` citation. A snapshot diff keyed on the original's id has nothing to diff. The feature would have passed every unit test, shipped green, and silently never fired once in production — the worst failure mode on this entire page, because nothing about it looks broken.

The general rule, which is cheap and which we skipped three times because the pattern had worked three times: **before porting a change-detection feature to a new host, refetch one old record and prove the field you plan to snapshot actually changes.** A publisher of record (a gazette, a court docket, a regulatory filing system) is usually append-only by statute — its whole point is that history cannot be rewritten. The mutable-record hosts (a grants portal, a recall database, an awards system) are operational systems that track a live process, and those are the ones worth snapshotting.

What that host needs instead is the inverse: a way to walk *forward* from a document to the ones that amend it. So the Federal Register Actor got `referencedCitations` — every `"NN FR NNNNN"` citation extracted out of the document's own `dates`/`action` text, which for a correction or extension is almost always the original it amends. Zero extra API calls (the text is already in the response), empty on the ~90% of documents that amend nothing, and on a live `"extension of comment period"` query it resolved the correct original citation for 4 of 5 real extension documents. Watch mode delivers the amendment as the new document it genuinely is, and the field tells you what it points at.

## How to actually test it

Unit tests do not catch any of these. All of them need real runs against the live API, and the sequence that catches most of them is three runs:

1. **Seed.** Compare the recorded id count to the API's own total for the same query. (Catches trap 3.)
2. **Rerun the identical input.** Must return exactly zero. (Catches a broken key or a resetting store — traps 1 and 2.)
3. **Delete a few ids from the stored baseline via the KV API, then rerun.** Exactly those rows must come back, fully populated.

Step 3 is only a real test if you choose the ids carefully. Delete from the **tail** of the recorded set — the ids scanned on the final page — and, if you can, include the last row of page two. With the Federal Register paging bug in place, deleting three ids from the middle returns three rows and looks like a pass; deleting the last row of page two returns two of three, and still reads as a success in the log unless you are counting.

Trap 5 needs a fourth, deliberately adversarial run that the first three won't surface on their own: **seed with the buyer's cap left at its normal (small) value, delete an id that sits *past* where that cap would have stopped a scan, then rerun with the same small cap.** If the id comes back, the scan cap is correctly independent of the delivery cap. If it doesn't, you've reproduced the exact silent under-count a real buyer would never see logged. We proved this directly on US federal awards by re-running the same filter with `maxPagesPerCategory: 1`: the seed still scanned past page 1 (proving the seed override), and a real incremental run with that same small cap correctly scanned only page 1, exactly as documented.

Trap 7 needs its own check on top of the standard three: run watch mode against an app with **zero** new reviews and confirm the dataset comes back completely empty — no snapshot row leaking through on a quiet run — then trigger (or wait for) one new review and confirm exactly one snapshot row rides along with it, never more.

Our own results, on real platform runs: NIH RePORTER 82 ids seeded → 0 on rerun → exactly 3 returned; Federal Register 51 (matching the API's `count`, which is how the off-by-one showed up); Grants.gov 18,458 on a deliberately broad `keyword=water` query; openFDA 108 Class I recalls across the food, drug and device endpoints; ClinicalTrials, Hacker News, ATS jobs, EU TED, UK Find a Tender, US federal awards and FEC campaign finance each re-ran the same three-step sequence (plus, where relevant, the trap-5 adversarial run) with baselines ranging from 2 tenders to 31,298 matching campaign-finance rows. The three review-platform Actors added the trap-7 check: Google Play seeded 1,000 review ids, then a rerun after deleting 2 ids recovered exactly those 2 reviews plus exactly one deferred app-snapshot row (`chargedEventCounts {result: 3}`, never more even though multiple apps were in scope); the App Store Actor seeded 50 ids across one app×country pair and recovered exactly 2 on the same test; Steam seeded 15 ids and recovered exactly 2, while a separate run with its snapshot-only `games` data type confirmed the label is rejected with a named warning rather than silently accepted.

One last design note that is easy to get backwards: **mark a row as delivered only after the charge and the write succeed**, not when you decide to send it. A row dropped by a `maxResults` cap or a charge limit should stay "new" and come back next run, rather than being silently consumed by a run that never actually delivered it.

## Where this is live

`watchLabel` is an optional input on 14 of our Actors — leave it unset and they behave exactly as before:

- [NIH RePORTER Scraper](/tools/nih-reporter-scraper) — baseline keyed on `appl_id`
- [Federal Register Scraper](/tools/federal-register-scraper) — `document_number`, deliberately with **no** `watchChanges` (published documents are never edited; `referencedCitations` links an amendment back to what it amends instead)
- [Grants.gov Scraper](/tools/grants-gov-scraper) — opportunity `id`, plus optional `watchChanges` (close-date, status and forecast-to-posted transitions on opportunities you already have)
- [FDA Recall Scraper](/tools/fda-recall-scraper) — `recall_number`, plus optional `watchChanges` (recall `status` and `classification` changes)
- [ClinicalTrials Scraper](/tools/clinicaltrials-scraper) — `nctId` (ignored, by design, when an exact `nctIds` lookup is set — trap 6)
- [Hacker News Scraper](/tools/hacker-news-scraper) — `objectID`
- [ATS Jobs Scraper](/tools/ats-jobs-scraper) — `company:jobId`
- [EU TED Tenders Scraper](/tools/eu-ted-tenders-scraper) — `publication-number`
- [UK Find a Tender Scraper](/tools/uk-find-a-tender-scraper) — `ocid`/`noticeId` across two fanned-out portals
- [US Federal Awards Scraper](/tools/us-federal-awards-scraper) — award or sub-award id (ignored when an exact `awardIds` lookup is set — trap 6), plus optional `watchChanges` on prime awards (last-modified date, amount/outlay and end-date changes)
- [FEC Campaign Finance Scraper](/tools/fec-campaign-finance-scraper) — Schedule A's own `sub_id` (contributions mode only — trap 6 rules out candidates mode)
- [Google Play Reviews Scraper](/tools/google-play-reviews-scraper) — `reviewId`, with a deferred per-app snapshot row (trap 7)
- [App Store Reviews Scraper](/tools/app-store-reviews-scraper) — compound `appId:country:reviewId` across a two-axis app×country fanout, same deferred-snapshot pattern
- [Steam Reviews Scraper](/tools/steam-reviews-scraper) — `appId:recommendationid` (the Actor's separate snapshot-only `games` data type rejects `watchLabel` outright — trap 6)

The first run under a new label seeds and charges nothing. After that you pay only for rows you have never been sent before, which for a daily schedule on a slow-moving dataset is usually a rounding error against re-pulling the full set every morning.

If you want the underlying APIs themselves, all four are free and key-free, and each has its own separate way of returning `HTTP 200` with the wrong answer — we catalogued those in [Eight government JSON APIs that need no key](/blog/free-government-data-json-apis-no-key).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every count, field name and failure mode above comes from real runs we made against these live APIs while building the feature, not from documentation.*
