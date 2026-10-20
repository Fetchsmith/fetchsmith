---
title: "Does a watchChanges deadline alert actually fire? We seeded 711 opportunities and forced it to find out"
description: "grants-gov-scraper's watchChanges re-delivers a saved opportunity if its deadline, status, forecast/posted type, award range or eligibility text moved. Live baseline of 711 posted opportunities, one stored snapshot deliberately altered, and the exact JSON the next run returned."
date: 2026-10-20
tags: webscraping, api, opendata, govtech
tool: grants-gov-scraper
---

Our [Grants.gov scraper](/tools/grants-gov-scraper) has a `watchLabel` mode: name a saved search, and every run after the first returns only the opportunities you haven't already been charged for. Turn on `watchChanges` too, and it also re-delivers an opportunity you already have if its deadline, posted/forecast status, award ceiling or floor, last-updated timestamp or eligibility text changed since you last saw it — tagged with `_watchChangeType` and `_watchPrevious` so a buyer doesn't have to diff the row themselves. That's the promise in the README. We wanted to see the mechanism actually produce that output against the real API, not just read the code and trust it.

## Seeding the baseline, live

A first run on a new watch label is a free baseline — it records every current match and returns nothing:

```
keyword="cancer research"  oppStatuses=[posted]  watchLabel="blogdemo2010"  watchChanges=true

Baseline walk: 711 opportunity id(s) recorded.
Baseline saved for watch label "blogdemo2010": 711 opportunity(ies) recorded as already-seen,
0 results returned, 0 charged.
```

711 live `posted`-status opportunities matching that keyword, fetched directly from Grants.gov's own `search2` API, each one's id and trackable fields (`closeDate`, `docType`, `oppStatus` — the fields a thin baseline walk can see without paying for a detail lookup) stored in an Apify key-value store under this label's key.

## Forcing the change path

We can't wait around for a real agency to extend a real deadline on cue, so we tested the mechanism the same way its own developers would: open the stored baseline record and deliberately alter one opportunity's snapshot, then let the Actor's normal comparison logic run against Grants.gov's live, unaltered data. We picked `357002` — PAR-24-311, "Molecular Imaging of Inflammation in Cancer," the same opportunity used as the README's own sample row — and rewrote its stored `closeDate` from the real `01/07/2028` to a fabricated `10/01/2027`, simulating what the record would look like if we'd seeded the baseline before a deadline extension happened.

Re-running the identical label and filters against the live API (no code changes, nothing else touched):

```
Watch label "blogdemo2010": 0 new opportunity(ies) and 1 changed opportunity(ies)
(deadline/status/forecast/funding/eligibility/last-updated) since the last run
(710 already-delivered, unchanged row(s) skipped, uncharged); baseline now holds 711.

Pushed 1 opportunities (scanned 711 rows). Charged 1 as enriched "result"
and 0 at the cheaper "opportunity-thin" rate.
```

Exactly one row came back, and it's the one we touched. The pushed JSON carries the real, live, current record — title, synopsis, eligibility text, attachments, everything — plus two extra fields naming exactly what moved:

```json
{
  "id": "357002",
  "opportunityNumber": "PAR-24-311",
  "closeDate": "01/07/2028",
  "...": "...(the full current record, same shape as any other row)...",
  "_watchChangeType": ["closeDate"],
  "_watchPrevious": { "closeDate": "10/01/2027" }
}
```

The other 710 opportunities in the baseline were compared too — the log line says so explicitly — and correctly produced no change, no charge, nothing pushed. Standard incremental-watch mechanics (skip what hasn't moved, re-deliver what has) held up against the real dataset, not a mock.

## A warning the run gave us for free

The same run logged something worth repeating here, because it's easy to set up by accident. `oppStatuses` defaulted to `["posted"]` for this test, and `watchChanges` tracks `oppStatus` transitions (posted → closed/archived) — so the Actor flagged its own run:

```
WARN  watchChanges is ON but 1 of this run's filter(s) narrow on a field it tracks, so those
changes can NEVER be reported -- the change itself removes the opportunity from the match set:
oppStatuses (excludes forecasted, closed, archived; blinds oppStatus/docType changes INTO those
statuses).
```

If you only ever query `oppStatuses: ["posted"]`, a closed-out opportunity simply stops matching your search before `watchChanges` ever gets to compare it — so the one transition people most want a grants alert for (deadline passed, now closed) is silently invisible unless you widen the status filter or run a second, status-agnostic label. This is the same class of trap covered in more general terms across our fleet in [eight ways a watch mode silently stops working](/blog/incremental-api-watch-mode-four-traps); seeing the actual advisory fire on a live run, naming the exact filter and the exact statuses it blinds, is the concrete version of that warning.

## Packaged version

Live now on [grants-gov-scraper](/go/grants-gov-scraper) — see [Watch mode](/tools/grants-gov-scraper#watchchanges----also-catch-a-deadline-extension) in the Actor's own README for the full field list `watchChanges` tracks, and [eight ways a watch mode silently stops working](/blog/incremental-api-watch-mode-four-traps) for the same mechanism measured across the rest of our fleet.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned. The baseline count, warning text and current record above all came from a live run against Grants.gov's real API while writing this post; the "previous" closeDate is a snapshot we deliberately altered ourselves to exercise the change path, not an organically observed drift — stated plainly rather than presented as a coincidence.*
